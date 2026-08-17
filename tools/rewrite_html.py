import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlmap = json.load(open(f"{ROOT}/tools/urlmap.json"))
LIT = re.compile(r'https://loremflickr\.com/(\d+)/(\d+)/([^"\'?\s]+)\?lock=(\d+)')

# commerce-furniture 의 JS URL 빌더 -> 로컬 경로 (w<=200 이면 썸네일)
OLD_JS = "var imgURL = function(p, w, h){ return 'https://loremflickr.com/' + w + '/' + h + '/' + p.img + '?lock=' + p.lock; };"
NEW_JS = ("var imgURL = function(p, w, h){ return 'assets/img/' + p.img.replace(/[^a-z0-9]+/gi, '-') "
          "+ '-' + p.lock + (w <= 200 ? '-thumb' : '') + '.webp'; };")

total = miss = 0
for site, m in sorted(urlmap.items()):
    f = f"{ROOT}/sites/{site}/index.html"
    s = open(f, encoding="utf-8").read()
    orig = s
    def sub(mo):
        global total, miss
        u = mo.group(0)
        if u in m: total += 1; return m[u]
        miss += 1; print(f"  !! 매핑 없음: {site} {u}"); return u
    s = LIT.sub(sub, s)
    if site == "commerce-furniture":            # 재실행 가능하도록 idempotent 처리
        if OLD_JS in s: s = s.replace(OLD_JS, NEW_JS)
        elif NEW_JS not in s: raise SystemExit("furniture JS 템플릿을 찾지 못함")
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)
        print(f"{site}: 치환 완료")
print(f"\n총 치환 {total}건, 매핑 누락 {miss}건")
