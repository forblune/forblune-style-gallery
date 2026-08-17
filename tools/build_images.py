import json, os, sys, re, io, urllib.request, collections, concurrent.futures as cf
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queries import query_for
from photofilter import is_photo, rank
from tone_profiles import distance_hero as tone_dist
from relevance import filter_pool, score as rel_score

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "forblune-style-gallery/1.0"
slots = json.load(open(f"{ROOT}/tools/slots.json"))
TONES = json.load(open(f"{ROOT}/tools/tones.json"))
cands = json.load(open(f"{ROOT}/tools/candidates.json"))

FURNITURE = [("sofa,fabric",3101),("oak,table",3102),("leather,armchair",3103),("bed,linen",3104),
 ("dining,chair",3105),("bookshelf,metal",3106),("wooden,table",3107),("sofa,living",3108),
 ("dresser,drawer",3109),("dining,table",3110),("wooden,bed",3111),("rattan,chair",3112)]

def kwslug(kw): return re.sub(r'[^a-z0-9]+', '-', kw.lower()).strip('-')
def orig_url(s): return f"https://loremflickr.com/{s['w']}/{s['h']}/{s['kw']}?lock={s['lock']}"

# ---- 1) 렌디션 그룹화: 같은 사진(site,kw,lock)이라도 비율이 다르면 별도 파일 ----
groups = collections.OrderedDict()   # (site,kw,lock,ar) -> {w,h,urls[]}
for s in slots:
    ar = round(s["w"] / s["h"], 2)
    k = (s["site"], s["kw"], str(s["lock"]), ar)
    g = groups.setdefault(k, dict(site=s["site"], kw=s["kw"], lock=str(s["lock"]), ar=ar, w=0, h=0, urls=[]))
    if s["w"] * s["h"] > g["w"] * g["h"]: g["w"], g["h"] = s["w"], s["h"]
    g["urls"].append(orig_url(s))

# (site,kw,lock) 당 비율 그룹이 2개 이상이면 파일명에 크기를 덧붙여 구분
per_photo = collections.Counter((g["site"], g["kw"], g["lock"]) for g in groups.values())
for g in groups.values():
    base = f'{kwslug(g["kw"])}-{g["lock"]}'
    g["name"] = base if per_photo[(g["site"], g["kw"], g["lock"])] == 1 else f'{base}-{g["w"]}x{g["h"]}'

for kw, lock in FURNITURE:
    k = ("commerce-furniture", kw, str(lock), 1.0)
    if k in groups:  # 이미 리터럴 슬롯이 있으면 재사용하되, JS가 600px 로 그리므로 해상도를 올린다
        groups[k]["furn"] = True
        groups[k]["w"] = max(groups[k]["w"], 1200); groups[k]["h"] = max(groups[k]["h"], 1200)
    else:
        groups[k] = dict(site="commerce-furniture", kw=kw, lock=str(lock), ar=1.0, w=1200, h=1200,
                         urls=[], name=f"{kwslug(kw)}-{lock}", furn=True)

print(f"렌디션 {len(groups)}개 (원본 슬롯 {len(slots)} + furniture {len(FURNITURE)})")

# ---- 2) 사진 배정 (사이트 내 중복 금지, 전역 분산 우선) ----
used_global, plan = set(), []
for site in sorted({g["site"] for g in groups.values()}):
    used_here = set()
    gs = [g for g in groups.values() if g["site"] == site]
    hero_area = max(g["w"] * g["h"] for g in gs)
    for g in gs: g["is_hero"] = (g["w"] * g["h"] == hero_area and g["w"] >= 1000)
    for g in sorted(gs, key=lambda x: (x["kw"], int(x["lock"]), x["ar"])):
        q = query_for(g["kw"])
        strict = [c for c in cands.get(q, []) if is_photo(c)]
        pool = filter_pool(strict or cands.get(q, []), q)   # 관련성 우선, 비면 원본 풀로 폴백
        # 사실상 단색인 후보는 화면에서 "빈칸"으로 보이므로 배제
        lively = [c for c in pool if (TONES.get(c["id"]) or {}).get("contrast", 0) >= 0.03]
        pool = lively or pool
        if site.startswith("editorial"):          # 에디토리얼 톤에 안 맞는 소재 배제
            block = {"laptop","computer","technology","office","keyboard"}
            filt = [c for c in pool
                    if not ({(t.get("name") or "").lower() for t in (c.get("tags") or [])} & block)]
            pool = filt or pool
        def sc(c):                                # 1순위 관련성, 2순위 톤 적합도
            return (-rel_score(c, q),
                    tone_dist(site, TONES.get(c["id"]), g.get("is_hero"))
                    + (0.35 if c["id"] in used_global else 0)
                    + 0.04 * rank(c)[0])
        avail = [c for c in pool if c["id"] not in used_here] or \
                [c for c in cands.get(q, []) if c["id"] not in used_here]
        pick = min(avail, key=sc) if avail else None
        if not pick:
            print(f"  !! 후보 없음: {site} {g['kw']}"); continue
        used_here.add(pick["id"]); used_global.add(pick["id"])
        plan.append(dict(g, cand=pick))
print(f"배정 {len(plan)}개, 고유 사진 {len(used_global)}장")

# ---- 3) 다운로드 + 중앙 크롭 + WebP ----
def target_size(w, h):
    lo = max(w, h); scale = 2 if lo <= 500 else (1.5 if lo <= 900 else 1)
    t = min(max(int(lo * scale), 400), 1600)
    return (t, max(1, round(t * h / w))) if w >= h else (max(1, round(t * w / h)), t)

raw = f"{ROOT}/tools/raw"; os.makedirs(raw, exist_ok=True)
def fetch_raw(url, cid):
    p = f"{raw}/{cid}.bin"
    if os.path.exists(p) and os.path.getsize(p) > 1000: return open(p,"rb").read()
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":UA}), timeout=90) as r:
        d = r.read()
    open(p,"wb").write(d); return d

def crop_resize(im, tw, th):
    sr, tr = im.width/im.height, tw/th
    if sr > tr:
        nw = int(im.height*tr); x = (im.width-nw)//2; im = im.crop((x,0,x+nw,im.height))
    elif sr < tr:
        nh = int(im.width/tr); y = (im.height-nh)//2; im = im.crop((0,y,im.width,y+nh))
    return im.resize((tw,th), Image.LANCZOS)

def process(g):
    outdir = f"{ROOT}/sites/{g['site']}/assets/img"; os.makedirs(outdir, exist_ok=True)
    try:
        im = Image.open(io.BytesIO(fetch_raw(g["cand"]["url"], g["cand"]["id"]))).convert("RGB")
        tw, th = target_size(g["w"], g["h"])
        crop_resize(im, tw, th).save(f"{outdir}/{g['name']}.webp", "WEBP", quality=80, method=6)
        if g.get("furn"):
            crop_resize(im, 288, 288).save(f"{outdir}/{g['name']}-thumb.webp", "WEBP", quality=80, method=6)
        return "ok", None
    except Exception as e:
        return "fail", f"{g['site']}/{g['name']}: {e}"

os.system(f"rm -rf {ROOT}/sites/*/assets")
res = []
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for i, r in enumerate(ex.map(process, plan), 1):
        res.append(r)
        if i % 40 == 0: print(f"  {i}/{len(plan)}", flush=True)
print(collections.Counter(r[0] for r in res))
for st, m in res:
    if st == "fail": print("FAIL:", m)

# ---- 4) 산출물: URL 치환 맵 + 크레딧 ----
urlmap = collections.defaultdict(dict)
for g in plan:
    for u in g["urls"]: urlmap[g["site"]][u] = f"assets/img/{g['name']}.webp"
json.dump(urlmap, open(f"{ROOT}/tools/urlmap.json","w"), ensure_ascii=False, indent=1)
json.dump([{k:v for k,v in g.items() if k!="cand"} | {
    "cand_id":g["cand"]["id"], "cand_url":g["cand"]["url"], "source":g["cand"].get("source"),
    "creator":g["cand"].get("creator"), "license":g["cand"].get("license"),
    "landing":g["cand"].get("foreign_landing_url"), "title":g["cand"].get("title")} for g in plan],
    open(f"{ROOT}/tools/plan.json","w"), ensure_ascii=False, indent=1)
print("urlmap 항목:", sum(len(v) for v in urlmap.values()))
