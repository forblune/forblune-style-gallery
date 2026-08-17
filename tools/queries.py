# loremflickr 대표어 -> Openverse 검색 쿼리. 동의어는 같은 쿼리로 합쳐 요청 수를 줄인다.
QMAP = {
 'abalone':'shellfish seafood','apartment':'apartment building construction','architect':'architecture studio desk',
 'architecture':'concrete architecture','arena':'stadium lights crowd','bathroom':'bathroom interior',
 'bed':'bed linen bedroom','bedroom':'bedroom interior','beef':'beef steak meat','blueberry':'blueberry',
 'book':'book','books':'books shelf','bookshelf':'bookshelf','brass':'brass metal object','building':'building facade',
 'cabin':'wooden cabin forest','cap':'black cap hat','cave':'cave rock','cedar':'cedar wood','ceramic':'ceramic pottery',
 'chef':'chef kitchen','citrus':'citrus fruit glass','cnc':'factory machine metal','concert':'concert lights',
 'corn':'corn','desk':'desk workspace','dj':'dj stage','doctor':'doctor portrait','documentary':'portrait people',
 'eggs':'eggs','envelope':'envelope paper','esports':'gaming computer','factory':'factory industrial',
 'farmer':'farmer field','festival':'festival crowd','fire':'fire grill','fish':'fish market',
 'fisherman':'fishing boat sea','fountainpen':'fountain pen writing','fragrance':'perfume bottle','fruit':'fresh fruit',
 'furniture':'furniture sofa','gaming':'gaming keyboard','garden':'garden chair','hands':'hands coffee cup',
 'harbor':'harbor port boat','hoodie':'black hoodie','hospital':'hospital doctor','hottub':'hot tub outdoor',
 'ink':'ink pen writing','interior':'interior light','jeju':'stone wall','kimchi':'korean food','kitchen':'kitchen table',
 'law':'law books','lawyer':'lawyer office','light':'light installation','linen':'linen fabric',
 'medical':'medical equipment','meeting':'meeting room','melon':'melon','metal':'metal surface','milk':'milk dairy',
 'neon':'neon light','notebook':'notebook paper','oak':'oak wood table','omakase':'sushi','paper':'paper texture',
 'paperclip':'paper clip desk','peach':'peach fruit','pen':'pen','pencils':'pencils desk','perfume':'perfume bottle',
 'physiotherapy':'physical therapy','pilates':'pilates','plum':'plum fruit','potato':'potato',
 'precision':'machine parts metal','projection':'projection light dark','restaurant':'restaurant counter',
 'rice':'rice grain','sandalwood':'wood texture','sauce':'sauce jar','shop':'shop interior',
 'skateboard':'skateboard street','sneaker':'sneaker shoes','sneakers':'sneakers streetwear','sofa':'sofa living room',
 'spring':'stream water','stationery':'stationery notebook','stonewall':'stone wall','stretching':'stretching exercise',
 'sweetpotato':'sweet potato','tomato':'tomato','vegetables':'vegetables market','village':'village rural house',
 'water':'water drop','woman':'woman portrait','wood':'wood texture','yoga':'yoga studio',
 # commerce-furniture JS 상품
 'leather':'leather armchair','dining':'dining chair table','wooden':'wooden table',
 'dresser':'dresser drawer furniture','rattan':'rattan chair',
}
def query_for(kw):
    head = kw.split(',')[0].strip().lower()
    return QMAP.get(head, head)

# 대표어만으로는 너무 뭉뚱그려지는 키워드에 대한 전체-키워드 우선 매핑
KWMAP = {
 'perfume,bedroom':'bedroom interior','perfume,books':'books shelf','perfume,citrus':'citrus fruit glass',
 'perfume,linen':'linen fabric','perfume,wood':'wood texture','perfume,shop':'shop interior',
 'perfume,laboratory':'laboratory glassware','perfume,vials':'glass bottles','fragrance,glass':'glass bottle',
 'perfume,bottles':'perfume bottle','fragrance,bottle':'perfume bottle','perfume,bottle':'perfume bottle',
 'lawyer,office':'office desk professional','lawyer,portrait':'business portrait person',
 'law,books':'law books','meeting,room':'meeting room',
 'abalone,seafood':'oyster shell seafood','abalone,shellfish':'shellfish',
 'sneakers,streetwear':'shoes street style','sneaker,closeup':'sneaker shoes',
 'pilates,reformer':'pilates studio','pilates,instructor':'fitness trainer','physiotherapy,clinic':'massage therapy',
 'oak,table':'wooden dining table','brass,clip':'brass gold object',
}
_orig_query_for = query_for
def query_for(kw):
    k = kw.strip().lower()
    if k in KWMAP: return KWMAP[k]
    return _orig_query_for(kw)

KWMAP.update({
 'esports,gaming':'gaming setup computer','esports,jersey':'esports jersey','gaming,keyboard':'keyboard',
 'hoodie,black':'hoodie','cap,black':'cap hat','arena,lights':'stadium crowd',
 'architect,studio':'drafting table blueprint','medical,equipment':'medical equipment',
})

# CC0 풀에 실물이 없는 주제(게이밍 셋업 등)는 존재하는 인접 소재로 현실화
KWMAP.update({
 'esports,gaming':'keyboard','esports,jersey':'hoodie','gaming,keyboard':'keyboard',
 'arena,lights':'stadium crowd','cap,black':'cap hat','hoodie,black':'hoodie',
})

KWMAP.update({
 'cedar,wood':'wood texture','sandalwood,wood':'wood texture',
 'citrus,glass':'citrus fruit','perfume,citrus':'citrus fruit',
 'perfume,laboratory':'glass bottles','perfume,vials':'glass bottles','perfume,bottles':'perfume bottle',
 'hottub,forest':'wooden bathtub','garden,chair':'garden chair',
})

KWMAP.update({'fragrance,glass':'perfume bottle','perfume,bedroom':'bedroom interior'})
