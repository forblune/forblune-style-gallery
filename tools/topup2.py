import json, os, sys, time, urllib.parse, urllib.request, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/tools")
from queries import query_for, QMAP, KWMAP
CACHE = f"{ROOT}/tools/cache"
UA = "forblune-style-gallery/1.0"
BAD_SOURCES = {"met","clevelandmuseum","smithsonian_national_museum_of_natural_history","rijksmuseum","brooklynmuseum",
 "europeana","digitaltmuseum","sciencemuseum","wellcome_collection","smk","bio_diversity","inaturalist",
 "finnish_heritage_agency","museumsvictoria","smithsonian_cooper_hewitt_museum","svgsilh","sketchfab","thingiverse",
 "geographorguk","nasa"}
def usable(r):
    return (r.get("source") not in BAD_SOURCES and r.get("url")
            and not str(r["url"]).lower().endswith((".tif",".tiff",".svg"))
            and (r.get("width") or 0) >= 700 and (r.get("height") or 0) >= 500)
def fetch(q, sf=True):
    key = hashlib.md5((q + ("|src" if sf else "|any")).encode()).hexdigest()[:16]
    p = f"{CACHE}/{key}.json"
    if os.path.exists(p): return json.load(open(p)), True
    params = {"q": q, "license": "cc0", "page_size": "20", "mature": "false"}
    if sf: params["source"] = "stocksnap,rawpixel"
    req = urllib.request.Request("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r: d = json.load(r)
    json.dump(d, open(p,"w"), ensure_ascii=False); return d, False

cands = json.load(open(f"{ROOT}/tools/candidates.json"))
# KWMAP 이 만들어낸 새 쿼리 + 부족분 보강 쿼리
BOOST = {
 'perfume bottle':['perfume','fragrance glass bottle','cosmetic bottle'],
 'office desk professional':['office desk'],'business portrait person':['professional portrait'],
 'shellfish':['seafood shell'],'oyster shell seafood':['oyster'],'shoes street style':['sneakers'],
 'pilates studio':['pilates exercise'],'fitness trainer':['personal trainer gym'],
 'massage therapy':['physiotherapy treatment'],'wooden dining table':['oak table wood'],
 'brass gold object':['brass'],'laboratory glassware':['laboratory glass'],'glass bottles':['glass bottle'],
 'glass bottle':['glass bottle'],
}
targets = sorted(set(KWMAP.values()) | set(BOOST.keys()))
calls = 0
for q in targets:
    for probe in [q] + BOOST.get(q, []):
        try:
            d, cached = fetch(probe, True)
            if not cached: calls += 1; time.sleep(3.3)
            got = [r for r in d.get("results", []) if usable(r)]
            have = {c["id"] for c in cands.get(q, [])}
            new = [r for r in got if r["id"] not in have]
            cands.setdefault(q, []).extend(new)
            print(f"{q!r} += {len(new)} (probe {probe!r}) -> {len(cands[q])}  [calls {calls}]", flush=True)
        except Exception as e:
            print(f"{q!r} probe {probe!r} FAILED: {e}", flush=True)
        json.dump(cands, open(f"{ROOT}/tools/candidates.json","w"), ensure_ascii=False)
print("api calls:", calls)
