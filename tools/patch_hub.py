import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = f"{ROOT}/index.html"
s = open(f, encoding="utf-8").read()
orig = s

# 1) CSS: 썸네일 레이어. iframe 라이브 미리보기가 켜지면 자연스럽게 사라진다.
CSS_ANCHOR = ".shot iframe.is-ready{opacity:1}"
CSS_NEW = (CSS_ANCHOR +
  "\n.shot-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"
  "object-position:top center;display:block;z-index:1;transition:opacity .3s}"
  "\n.shot iframe.is-ready ~ .shot-img{opacity:0}")
if ".shot-img{" not in s:
    assert CSS_ANCHOR in s, "CSS 앵커를 찾지 못함"
    s = s.replace(CSS_ANCHOR, CSS_NEW, 1)

# 2) 각 .shot 의 iframe 뒤에 썸네일 <img> 삽입 (data-slug 로 파일명 결정)
SHOT = re.compile(r'(<div class="shot"[^>]*data-slug="([a-z0-9-]+)"[^>]*>)(.*?)(<span class="ph">)', re.S)
added = []
def ins(m):
    head, slug, mid, ph = m.groups()
    if "shot-img" in mid: return m.group(0)
    if not os.path.isfile(f"{ROOT}/shots/{slug}.webp"):
        print(f"  !! 썸네일 없음: {slug}"); return m.group(0)
    added.append(slug)
    img = (f'<img class="shot-img" src="shots/{slug}.webp" alt="" width="960" height="600" '
           f'loading="lazy" decoding="async">')
    return head + mid + img + ph
s = SHOT.sub(ins, s)

if s != orig:
    open(f, "w", encoding="utf-8").write(s)
print(f"썸네일 삽입: {len(added)}개")
missing = [d for d in sorted(os.listdir(f"{ROOT}/sites"))
           if os.path.isdir(f"{ROOT}/sites/{d}") and d not in added]
print("삽입 안 된 사이트:", missing or "없음")
