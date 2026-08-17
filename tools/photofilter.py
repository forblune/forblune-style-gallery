import re
BAD_TAGS = {'vintage','clip art','clipart','png','illustration','vintage illustrations','drawing','cartoon',
 'sticker','collage','art print','chromolithograph','watercolor','sketch','engraving','psd',
 'transparent background','lithograph','painting','antique','retro','poster','vector','ai generated'}
MUSEUM_RE = re.compile(r'\(\s*(c\.|ca\.|circa)?\s*1[6-9]\d\d|\b1[6-9]\d\d\s*/\s*1[6-9]\d\d|\(\s*20[01]\d\s*\)')
BAD_TITLE = ('png','psd','sticker','clipart','clip art','illustration','vintage','drawing',
 'transparent background','vector','ai generated','ai-generated','remixed by','original public domain',
 'painting','fragment','tiraz','cruet','museum','engraved','etching','watercolour','portrait of','manuscript')
PREF = ['stocksnap','rawpixel','wordpress','flickr']

# 기관 소장품 디지털화 이미지 — 카테고리는 photograph 지만 실제로는 유물 촬영본이라
# 현대 웹디자인 페이지에 넣으면 "빈 박스" 나 골동품처럼 읽힌다.
BAD_CREATORS = {'libraryofcongress','thegetty','artinstitutechicago','themet','rijksmuseum',
 'nationalgalleryofart','lacma','museumofnewzealand','clevelandart','smithsonian','nasa',
 'wellcomecollection','nationalarchives','britishlibrary','nypl','europeana','digitaltmuseum',
 'smk','biodiversityheritagelibrary','sciencemuseum','brooklynmuseum','cooperhewitt'}

def is_photo(r):
    if r.get('category') != 'photograph': return False
    tags = {(t.get('name') or '').lower() for t in (r.get('tags') or [])}
    if tags & BAD_TAGS: return False
    ti = (r.get('title') or '').lower()
    if any(b in ti for b in BAD_TITLE): return False
    if MUSEUM_RE.search(r.get('title') or ''): return False   # 박물관 소장품 표기(연도)
    if tags & {'museum','artifact','ancient','medieval','archive','19th century','18th century'}: return False
    if (r.get('creator') or '').lower() in BAD_CREATORS: return False
    if {'art','textiles'} <= tags: return False        # 직물 유물 스캔
    if (r.get('width') or 0) < 800 or (r.get('height') or 0) < 600: return False
    return True

def rank(r):
    return (PREF.index(r['source']) if r.get('source') in PREF else 9,
            -min(r.get('width') or 0, 4000))
