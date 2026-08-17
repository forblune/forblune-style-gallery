"""한국어 페이지에서 영문판을 생성한다.
- sites/<slug>/en/index.html 로 출력하고 assets/ 경로를 ../assets/ 로 올린다
- 텍스트 노드와 지정한 속성만 사전으로 치환한다 (구조·스타일은 건드리지 않음)
- 사전에 없는 한국어가 남으면 실패로 보고한다
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ATTRS = ("alt", "title", "aria-label", "placeholder", "content", "data-caption", "value")

SWITCH_CSS = """<style id="lang-switch-style">
.langswitch{position:fixed;bottom:14px;right:14px;z-index:99999;display:flex;gap:1px;
font:600 11px/1 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.06em;
background:rgba(20,20,24,.78);border-radius:999px;padding:3px;backdrop-filter:blur(6px);
box-shadow:0 2px 10px rgba(0,0,0,.22)}
.langswitch a{display:block;padding:5px 9px;border-radius:999px;color:rgba(255,255,255,.62);
text-decoration:none}
.langswitch a[aria-current="true"]{background:rgba(255,255,255,.92);color:#15181d}
.langswitch a:focus-visible{outline:2px solid #8fb0ee;outline-offset:2px}
@media print{.langswitch{display:none}}
</style>"""

def switch_html(ko_href, en_href, current):
    ko = ' aria-current="true"' if current == "ko" else ""
    en = ' aria-current="true"' if current == "en" else ""
    return (f'<div class="langswitch" role="group" aria-label="Language">'
            f'<a href="{ko_href}" hreflang="ko" lang="ko"{ko}>KO</a>'
            f'<a href="{en_href}" hreflang="en" lang="en"{en}>EN</a></div>')

def has_ko(t): return bool(re.search(r"[가-힣]", t))

def translate_html(src, table, missing):
    def sub_text(m):
        raw = m.group(1)
        key = " ".join(raw.split())
        if not has_ko(key): return m.group(0)
        if key in table:
            lead = raw[:len(raw) - len(raw.lstrip())]
            trail = raw[len(raw.rstrip()):]
            return ">" + lead + table[key] + trail + "<"
        missing.add(key); return m.group(0)

    def sub_js(block):
        """JS 문자열 리터럴 중 사전에 정확히 일치하는 것만 교체한다."""
        def repl(m):
            q, body = m.group(1), m.group(2)
            if not has_ko(body): return m.group(0)
            key = " ".join(body.split())
            if key not in table:
                missing.add(key); return m.group(0)
            v = table[key].replace("\\", "\\\\").replace(q, "\\" + q)
            return q + v + q
        return re.sub(r"([\'\"`])((?:[^\\\n]|\\.)*?)\1", repl, block)

    parts = re.split(r"(<script[\s\S]*?</script>|<style[\s\S]*?</style>)", src)
    for i in range(1, len(parts), 2):
        if parts[i].lstrip().lower().startswith("<script"):
            parts[i] = sub_js(parts[i])
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r">([^<>]+)<", sub_text, parts[i])
        for a in ATTRS:
            def sub_attr(m, a=a):
                v = m.group(1)
                if not has_ko(v): return m.group(0)
                key = " ".join(v.split())
                if key in table: return f'{a}="{table[key]}"'
                missing.add(key); return m.group(0)
            parts[i] = re.sub(rf'{a}="([^"]*)"', sub_attr, parts[i])
    return "".join(parts)

def build(slug, table, js_patches=()):
    src_path = f"{ROOT}/sites/{slug}/index.html"
    s = open(src_path, encoding="utf-8").read()
    missing = set()

    # 날짜·통화 포맷처럼 문자열 치환으로는 자연스러워지지 않는 코드는 먼저 갈아끼운다
    pre = s
    for find, repl in js_patches:
        if find not in pre:
            raise SystemExit(f"js_patch 대상을 찾지 못함: {find[:70]}")
        pre = pre.replace(find, repl)
    en = translate_html(pre, table, missing)
    # 한 단계 깊어지므로 상대 경로를 올린다 (HTML 속성 + JS 문자열 모두)
    en = en.replace('="assets/', '="../assets/')
    en = en.replace("'assets/", "'../assets/").replace('"assets/', '"../assets/')
    en = re.sub(r'<html([^>]*)\blang="ko"', r'<html\1lang="en"', en, count=1)
    if "langswitch" not in en:
        en = en.replace("</head>", SWITCH_CSS + "\n</head>", 1)
        en = en.replace("<body", switch_html("../", "./", "en") + "\n<body", 1) \
            if "<body" not in en else en
        # body 바로 뒤에 넣는 편이 안전
        en = re.sub(r"(<body[^>]*>)", r"\1" + switch_html("../", "./", "en"), en, count=1)
        en = en.replace(switch_html("../", "./", "en") + "\n<body", "<body")
    os.makedirs(f"{ROOT}/sites/{slug}/en", exist_ok=True)
    open(f"{ROOT}/sites/{slug}/en/index.html", "w", encoding="utf-8").write(en)

    # 한국어 원본에도 스위치를 달아 준다
    ko = s
    if "langswitch" not in ko:
        ko = ko.replace("</head>", SWITCH_CSS + "\n</head>", 1)
        ko = re.sub(r"(<body[^>]*>)", r"\1" + switch_html("./", "en/", "ko"), ko, count=1)
        open(src_path, "w", encoding="utf-8").write(ko)
    return missing

if __name__ == "__main__":
    slug = sys.argv[1]
    table = json.load(open(f"{ROOT}/tools/i18n/{slug}.json", encoding="utf-8"))
    patch_path = f"{ROOT}/tools/i18n/{slug}.patches.json"
    patches = json.load(open(patch_path, encoding="utf-8")) if os.path.exists(patch_path) else []
    missing = build(slug, table, [(p["find"], p["replace"]) for p in patches])
    print(f"{slug}: 사전 {len(table)}개 적용")
    if missing:
        print(f"  !! 번역 누락 {len(missing)}개")
        for m in sorted(missing)[:25]: print("   -", m)
    else:
        print("  누락 없음")
