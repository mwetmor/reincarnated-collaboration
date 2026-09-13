"""Conductor eyeball sheet: the band around each painted strip's inner edge (row 256 / col 256) of a chunk, full res.
usage: join_sheet.py out.png chunk.png [chunk.png ...]  (TOP band 1536x160 -> shown at 768x80; LEFT band rotated)"""
import sys
from PIL import Image, ImageDraw
rows=[]
for f in sys.argv[2:]:
    im=Image.open(f).convert('RGB')
    top=im.crop((0,176,1536,336)).resize((1152,120))
    left=im.crop((176,0,336,1024)).rotate(90,expand=True).resize((768,120))
    r=Image.new('RGB',(1152+768+8,132),(30,30,30)); r.paste(top,(0,12)); r.paste(left,(1160,12))
    d=ImageDraw.Draw(r); d.text((2,0),f.split('/')[-2],fill=(255,255,0))
    d.line([(0,72),(1152,72)],fill=(255,0,0)); d.line([(1160,72),(1928,72)],fill=(255,0,0))
    rows.append(r)
sheet=Image.new('RGB',(1928,132*len(rows)))
for i,r in enumerate(rows): sheet.paste(r,(0,i*132))
sheet.save(sys.argv[1]); print(sys.argv[1])
