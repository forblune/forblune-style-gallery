import re
STOP = {'a','the','of','and','with'}
def toks(q): return [t for t in re.split(r'[^a-z]+', q.lower()) if t and t not in STOP]
def hay(r):
    return ((r.get('title') or '') + ' ' + ' '.join((t.get('name') or '') for t in (r.get('tags') or []))).lower()
def score(r, q):
    h = hay(r); return sum(1 for t in toks(q) if t in h)
def filter_pool(pool, q):
    """관련성 점수 내림차순 전체 목록. 강한 매치를 앞에 두되 풀이 마르지 않게 한다."""
    scored = [(score(r, q), r) for r in pool]
    hit = [x for x in scored if x[0] >= 1]
    return [r for _, r in sorted(hit or scored, key=lambda x: -x[0])]
