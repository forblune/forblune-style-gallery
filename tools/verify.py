import json, os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True

# 1) loremflickr 잔존 여부
hits = []
for dp, _, fns in os.walk(f"{ROOT}/sites"):
    for fn in fns:
        if fn.endswith((".html", ".js", ".css")):   # 배포되는 파일만 (meta.json 은 deploy.sh 가 제외)
            p = os.path.join(dp, fn)
            for i, line in enumerate(open(p, encoding="utf-8", errors="ignore"), 1):
                if "loremflickr" in line: hits.append(f"{p}:{i}")
print(f"1) loremflickr 잔존 참조: {len(hits)}")
for h in hits[:10]: print("   ", h)
ok &= not hits

# 2) HTML 이 참조하는 로컬 이미지가 실제로 있는지
REF = re.compile(r'assets/img/([A-Za-z0-9._-]+\.webp)')
missing = collections.defaultdict(list)
refs = 0
for site in sorted(os.listdir(f"{ROOT}/sites")):
    f = f"{ROOT}/sites/{site}/index.html"
    if not os.path.isfile(f): continue
    s = open(f, encoding="utf-8").read()
    for name in set(REF.findall(s)):
        refs += 1
        if not os.path.isfile(f"{ROOT}/sites/{site}/assets/img/{name}"):
            missing[site].append(name)
print(f"2) HTML 참조 이미지 {refs}종, 없는 파일 {sum(len(v) for v in missing.values())}")
for s, v in missing.items(): print("   ", s, v[:5])
ok &= not missing

# 3) furniture JS 가 만들 경로가 실제로 있는지 (상품 데이터에서 직접 재구성)
fur = f"{ROOT}/sites/commerce-furniture/index.html"
s = open(fur, encoding="utf-8").read()
prods = re.findall(r"img:'([^']+)',\s*lock:(\d+)", s)
print(f"3) furniture 상품 {len(prods)}개")
bad = []
for img, lock in prods:
    base = re.sub(r'[^a-z0-9]+', '-', img, flags=re.I)
    for suffix in ("", "-thumb"):
        p = f"{ROOT}/sites/commerce-furniture/assets/img/{base}-{lock}{suffix}.webp"
        if not os.path.isfile(p): bad.append(os.path.basename(p))
print(f"   없는 파일 {len(bad)}: {bad[:6]}")
ok &= not bad

# 4) 고아 파일(참조되지 않는 이미지)
orphan = 0
for site in sorted(os.listdir(f"{ROOT}/sites")):
    d = f"{ROOT}/sites/{site}/assets/img"
    if not os.path.isdir(d): continue
    s = open(f"{ROOT}/sites/{site}/index.html", encoding="utf-8").read()
    used = set(REF.findall(s))
    if site == "commerce-furniture":
        for img, lock in prods:
            b = re.sub(r'[^a-z0-9]+', '-', img, flags=re.I)
            used |= {f"{b}-{lock}.webp", f"{b}-{lock}-thumb.webp"}
    for fn in os.listdir(d):
        if fn not in used: orphan += 1; print(f"   고아: {site}/{fn}")
print(f"4) 참조되지 않는 이미지: {orphan}")

# 5) 이미지 무결성
from PIL import Image
bad_img = []
for dp, _, fns in os.walk(f"{ROOT}/sites"):
    for fn in fns:
        if fn.endswith(".webp"):
            try:
                im = Image.open(os.path.join(dp, fn)); im.verify()
            except Exception as e: bad_img.append(f"{fn}: {e}")
print(f"5) 손상된 이미지: {len(bad_img)} {bad_img[:3]}")
ok &= not bad_img
print("\n=== 검증", "통과" if ok else "실패", "===")
sys.exit(0 if ok else 1)
