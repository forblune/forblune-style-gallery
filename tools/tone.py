import json, os, sys, io, urllib.request, colorsys, concurrent.futures as cf
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/tools")
from photofilter import is_photo, rank

RAW = f"{ROOT}/tools/raw"; os.makedirs(RAW, exist_ok=True)
UA = "forblune-style-gallery/1.0"
TONEF = f"{ROOT}/tools/tones.json"
tones = json.load(open(TONEF)) if os.path.exists(TONEF) else {}

def grab(r):
    cid = r["id"]; p = f"{RAW}/{cid}.bin"
    if os.path.exists(p) and os.path.getsize(p) > 1000: return open(p,"rb").read()
    with urllib.request.urlopen(urllib.request.Request(r["url"], headers={"User-Agent":UA}), timeout=60) as h:
        d = h.read()
    open(p,"wb").write(d); return d

def measure(r):
    if r["id"] in tones: return r["id"], tones[r["id"]]
    try:
        im = Image.open(io.BytesIO(grab(r))).convert("RGB").resize((48,48), Image.BILINEAR)
        px = list(im.getdata())
        s = v = warm = 0.0; vs = []
        for R,G,B in px:
            h_,s_,v_ = colorsys.rgb_to_hsv(R/255, G/255, B/255)
            s += s_; v += v_; vs.append(v_); warm += (R-B)/255
        n = len(px)
        s/=n; v/=n; warm/=n
        mean = sum(vs)/n
        contrast = (sum((x-mean)**2 for x in vs)/n) ** 0.5
        return r["id"], dict(sat=round(s,4), val=round(v,4), warm=round(warm,4), contrast=round(contrast,4))
    except Exception as e:
        return r["id"], None

cands = json.load(open(f"{ROOT}/tools/candidates.json"))
todo, seen = [], set()
for q, v in cands.items():
    for r in sorted([x for x in v if is_photo(x)], key=rank):   # 전체 후보 측정
        if r["id"] not in seen and r["id"] not in tones:
            seen.add(r["id"]); todo.append(r)
print(f"측정 대상 {len(todo)}장 (캐시 {len(tones)})", flush=True)
done = 0
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for cid, t in ex.map(measure, todo):
        if t: tones[cid] = t
        done += 1
        if done % 100 == 0:
            print(f"  {done}/{len(todo)}", flush=True); json.dump(tones, open(TONEF,"w"))
json.dump(tones, open(TONEF,"w"))
print("측정 완료:", len(tones))
