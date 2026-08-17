import json, os, sys, time, urllib.parse, urllib.request, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from queries import query_for, QMAP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", "cache"); os.makedirs(CACHE, exist_ok=True)
UA = "forblune-style-gallery/1.0 (self-hosting CC0 stock for a design demo)"

# 박물관/표본 아카이브는 현대 웹디자인 톤과 맞지 않아 제외
BAD_SOURCES = {"met","clevelandmuseum","smithsonian_national_museum_of_natural_history","rijksmuseum",
 "brooklynmuseum","europeana","digitaltmuseum","sciencemuseum","wellcome_collection","smk","bio_diversity",
 "inaturalist","finnish_heritage_agency","museumsvictoria","smithsonian_cooper_hewitt_museum","svgsilh",
 "sketchfab","thingiverse","geographorguk","nasa","science_museum"}
GOOD_ORDER = ["stocksnap","rawpixel","wordpress","flickr","wikimedia"]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

def fetch(q, source_filter=True):
    key = hashlib.md5((q + ("|src" if source_filter else "|any")).encode()).hexdigest()[:16]
    path = os.path.join(CACHE, f"{key}.json")
    if os.path.exists(path):
        return json.load(open(path)), True
    params = {"q": q, "license": "cc0", "page_size": "20", "mature": "false"}
    if source_filter: params["source"] = "stocksnap,rawpixel"
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params)
    d = get(url)
    d["_query"] = q; d["_source_filter"] = source_filter
    json.dump(d, open(path, "w"), ensure_ascii=False)
    return d, False

def usable(r):
    if r.get("source") in BAD_SOURCES: return False
    if not r.get("url"): return False
    if str(r.get("url","")).lower().endswith((".tif",".tiff",".svg")): return False
    w,h = r.get("width") or 0, r.get("height") or 0
    return w >= 700 and h >= 500

def main():
    slots = json.load(open(os.path.join(ROOT,"tools","slots.json")))
    queries = sorted({query_for(r["kw"]) for r in slots} |
                     {QMAP[h] for h in ["leather","dining","wooden","dresser","rattan"]})
    print(f"queries: {len(queries)}", flush=True)
    out, calls = {}, 0
    for i, q in enumerate(queries, 1):
        try:
            d, cached = fetch(q, True)
            if not cached: calls += 1; time.sleep(3.3)
            cands = [r for r in d.get("results", []) if usable(r)]
            if len(cands) < 3:
                d2, cached2 = fetch(q, False)
                if not cached2: calls += 1; time.sleep(3.3)
                seen = {c["id"] for c in cands}
                cands += [r for r in d2.get("results", []) if usable(r) and r["id"] not in seen]
            cands.sort(key=lambda r: GOOD_ORDER.index(r["source"]) if r.get("source") in GOOD_ORDER else 99)
            out[q] = cands
            print(f"[{i}/{len(queries)}] {q!r} -> {len(cands)} (api calls {calls})", flush=True)
        except Exception as e:
            print(f"[{i}/{len(queries)}] {q!r} FAILED: {e}", flush=True)
            out[q] = []
        json.dump(out, open(os.path.join(ROOT,"tools","candidates.json"),"w"), ensure_ascii=False)
    empty = [q for q,v in out.items() if len(v) < 2]
    print(f"\nDONE. api calls={calls}. thin/empty queries ({len(empty)}): {empty}")

main()
