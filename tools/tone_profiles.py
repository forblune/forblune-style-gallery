# 사이트별 목표 색조 (sat=채도, val=명도, warm=따뜻함 R-B, contrast=명암 대비)
# 각 페이지의 디자인 방향(허브 표 기준)에 맞춘 값.
P = {
 'editorial-perfume':      dict(sat=.15, val=.72, warm=.10, contrast=.16),
 'editorial-select':       dict(sat=.12, val=.78, warm=.05, contrast=.14),
 'editorial-stay':         dict(sat=.20, val=.56, warm=.08, contrast=.20),
 'cinematic-architecture': dict(sat=.12, val=.46, warm=.02, contrast=.22),
 'cinematic-chef':         dict(sat=.34, val=.36, warm=.15, contrast=.22),
 'cinematic-photographer': dict(sat=.10, val=.42, warm=.02, contrast=.20),
 'commerce-booking':       dict(sat=.24, val=.68, warm=.06, contrast=.17),
 'commerce-furniture':     dict(sat=.18, val=.66, warm=.10, contrast=.16),
 'commerce-grocery':       dict(sat=.44, val=.58, warm=.12, contrast=.20),
 'corporate-b2b':          dict(sat=.18, val=.46, warm=-.04, contrast=.20),
 'corporate-hospital':     dict(sat=.17, val=.72, warm=-.02, contrast=.16),
 'corporate-lawfirm':      dict(sat=.16, val=.52, warm=.06, contrast=.19),
 'experimental-art':       dict(sat=.52, val=.30, warm=.00, contrast=.24),
 'experimental-campaign':  dict(sat=.30, val=.46, warm=-.04, contrast=.20),
 'kinetic-esports':        dict(sat=.44, val=.29, warm=-.04, contrast=.23),
 'kinetic-festival':       dict(sat=.50, val=.30, warm=.02, contrast=.25),
 'kinetic-sneaker':        dict(sat=.34, val=.42, warm=.02, contrast=.22),
}
W = dict(sat=2.2, val=1.6, warm=1.2, contrast=0.6)
def distance(site, t):
    p = P.get(site)
    if not p or not t: return 0.5
    return sum(W[k] * abs(t.get(k, 0) - p[k]) for k in p)

# 전면 히어로 이미지 위에 밝은 카피가 얹히는 페이지 — 히어로는 어두운 사진이라야 글자가 읽힌다.
TEXT_OVER_HERO = {'cinematic-architecture','cinematic-chef','editorial-stay',
                  'kinetic-esports','kinetic-festival','kinetic-sneaker','commerce-booking'}

def distance_hero(site, t, is_hero=False):
    p = P.get(site)
    if not p: return 0.5
    if not t: return 3.0    # 미측정 후보는 회피
    w = W
    if is_hero and site in TEXT_OVER_HERO:
        # 카피 가독성이 걸린 자리라 명도를 사실상 결정 요인으로 둔다
        p = dict(p, val=min(p['val'], 0.34))
        w = dict(W, val=6.0)
    return sum(w[k] * abs(t.get(k, 0) - p[k]) for k in p)
