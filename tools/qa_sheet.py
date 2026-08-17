import sys, os, json, glob
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site, out = sys.argv[1], sys.argv[2]
plan = json.load(open(f"{ROOT}/tools/plan.json"))
items = [p for p in plan if p["site"] == site]
items.sort(key=lambda p: p["name"])
cell, cols = 165, 6
rows = (len(items)+cols-1)//cols
sheet = Image.new("RGB", (cols*cell, rows*cell), (18,18,22)); d = ImageDraw.Draw(sheet)
for i, p in enumerate(items):
    f = f"{ROOT}/sites/{site}/assets/img/{p['name']}.webp"
    im = Image.open(f).convert("RGB"); sq = min(im.width, im.height)
    im = im.crop(((im.width-sq)//2,(im.height-sq)//2,(im.width-sq)//2+sq,(im.height-sq)//2+sq)).resize((cell,cell))
    x, y = (i%cols)*cell, (i//cols)*cell
    sheet.paste(im, (x,y))
    d.rectangle([x+2,y+2,x+30,y+18], fill=(0,0,0))
    d.text((x+6,y+5), str(i), fill=(255,235,120))
sheet.save(out, quality=88)
print(f"--- {site} ({len(items)}) -> {out}")
for i, p in enumerate(items):
    print(f"{i:>3}  {p['name']:<34} kw={p['kw']:<24} {(p.get('title') or '')[:46]}")
