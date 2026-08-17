import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_candidates as fc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRA = {  # 부족한 쿼리 -> 보충용 대체 검색어
 'architecture studio desk': ['architect drawing desk', 'blueprint drafting'],
 'hot tub outdoor': ['outdoor bath spa', 'wooden bathtub'],
 'rattan chair': ['wicker chair', 'rattan furniture'],
 'yoga studio': ['yoga mat pose'],
}
cands = json.load(open(os.path.join(ROOT,'tools','candidates.json')))
for target, alts in EXTRA.items():
    have = {c['id'] for c in cands.get(target, [])}
    for alt in alts:
        try:
            d, cached = fc.fetch(alt, True)
            if not cached: time.sleep(3.3)
            got = [r for r in d.get('results', []) if fc.usable(r)]
            if len(got) < 3:
                d2, cached2 = fc.fetch(alt, False)
                if not cached2: time.sleep(3.3)
                got += [r for r in d2.get('results', []) if fc.usable(r) and r['id'] not in {g['id'] for g in got}]
            new = [r for r in got if r['id'] not in have]
            cands.setdefault(target, []).extend(new)
            have |= {r['id'] for r in new}
            print(f"{target!r} += {len(new)} from {alt!r} -> total {len(cands[target])}", flush=True)
        except Exception as e:
            print(f"{alt!r} failed: {e}", flush=True)
        if len(cands.get(target, [])) >= 6: break
json.dump(cands, open(os.path.join(ROOT,'tools','candidates.json'),'w'), ensure_ascii=False)
print('\n최종:', {k: len(cands.get(k,[])) for k in EXTRA})
