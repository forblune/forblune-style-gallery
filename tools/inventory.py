import re, os, json, collections
ROOT = "/Users/gh/Documents/forblune/forblune-style-gallery-work"
SITES = os.path.join(ROOT, "sites")

LIT = re.compile(r'https://loremflickr\.com/(\d+)/(\d+)/([^"\'?\s]+)\?lock=(\d+)')
ANY = re.compile(r'loremflickr')

rows = []
tmpl = collections.defaultdict(list)
for site in sorted(os.listdir(SITES)):
    f = os.path.join(SITES, site, "index.html")
    if not os.path.isfile(f): continue
    s = open(f, encoding="utf-8").read()
    lits = LIT.findall(s)
    for w,h,kw,lock in lits:
        rows.append(dict(site=site, w=int(w), h=int(h), kw=kw, lock=lock))
    # any loremflickr mention not matched by literal
    total = len(ANY.findall(s))
    if total != len(lits):
        for i, line in enumerate(s.split("\n"), 1):
            if "loremflickr" in line and not LIT.search(line):
                tmpl[site].append((i, line.strip()[:200]))

print("=== literal URL slots per site ===")
c = collections.Counter(r["site"] for r in rows)
for k,v in sorted(c.items(), key=lambda x:-x[1]): print(f"{v:>4}  {k}")
print("TOTAL literal slots:", len(rows))
print("UNIQUE literal urls:", len({(r['w'],r['h'],r['kw'],r['lock']) for r in rows}))
print()
print("=== unmatched / template lines ===")
for site, lines in tmpl.items():
    print(f"-- {site}")
    for i,l in lines: print(f"   {i}: {l}")
json.dump(rows, open(os.path.join(ROOT,"tools","slots.json"),"w"), ensure_ascii=False, indent=1)
