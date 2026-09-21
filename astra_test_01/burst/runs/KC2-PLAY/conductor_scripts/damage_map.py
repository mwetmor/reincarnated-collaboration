#!/usr/bin/env python3
"""Conductor glue (not lane code): render a DAMAGE MAP for a chunk from an authored EVENT LIST (crack law § 3).
Deterministic (seeded). Outputs: <out>/b1d_damage_annot.png (guide + overlay + legend), <out>/b1d_damage_mask.png (class colours), <out>/b1d_events.json."""
import json, math, random, sys
from PIL import Image, ImageDraw, ImageFont
guide, out = sys.argv[1], sys.argv[2]
PX_E, PX_S = 100.617553710938, 80.307624765   # px per metre east / south (drax b1a_manifest)
GATE = (768.0, 798.72)
rng = random.Random(20260920)
def m2px(dx_m, dy_m): return (dx_m*PX_E, dy_m*PX_S)
events = [
 {"id":"E1","kind":"blast","at_m":[0.0,0.0],"r_crater_m":1.2,"rays":11,"ray_len_m":[2.2,4.5],"ejecta_dir_deg":-90,"ejecta_lambda_m":4.0,"note":"demon-gate opened AT the gate; crater; radial cracks; ejecta thrown NORTH up the dais steps"},
 {"id":"E2","kind":"fire","at_m":[3.8,-3.0],"fuel_m":[2.6,1.6],"wind_deg":-80,"note":"choir stalls burned (east side); scorch = fuel map; soot V-plume up the east wall; NO floor cracks"},
 {"id":"E3","kind":"pier_failure","at_m":[4.1,-5.8],"talus_r_m":2.4,"n_blocks":9,"note":"apse NE pier gave; vault wedge fell; talus cone at ~35 deg repose; ONE impact fracture under each block"},
 {"id":"E4","kind":"breach","at_m":[-5.9,-2.5],"span_m":3.2,"debris_lambda_m":3.0,"n_debris":14,"note":"west wall broken INWARD from outside; debris fan east; sunset floods in"},
]
im = Image.open(guide).convert("RGB"); W,H = im.size
mask = Image.new("RGB",(W,H),(0,0,0)); md = ImageDraw.Draw(mask); ad = ImageDraw.Draw(im)
C = {"crater":(120,0,120),"spall_ring":(200,80,200),"crack_line":(255,255,255),"impact_fracture":(255,200,0),"scorch":(60,60,60),"blast_scorch":(30,30,30),"soot_plume":(90,90,90),"debris":(0,160,255),"talus":(0,90,180)}
def P(m): x,y = m2px(m[0],m[1]); return (GATE[0]+x, GATE[1]+y)
def ell(d, c, rx, ry, fill=None, outline=None, w=1): d.ellipse([c[0]-rx,c[1]-ry,c[0]+rx,c[1]+ry], fill=fill, outline=outline, width=w)
for e in events:
    c = P(e["at_m"])
    if e["kind"]=="blast":
        rx,ry = e["r_crater_m"]*PX_E, e["r_crater_m"]*PX_S
        ell(md,c,2*rx,2*ry,fill=C["blast_scorch"]); ell(md,c,1.6*rx,1.6*ry,fill=C["spall_ring"]); ell(md,c,rx,ry,fill=C["crater"])
        ell(ad,c,2*rx,2*ry,outline=(40,40,40),w=3); ell(ad,c,rx,ry,outline=(160,0,160),w=4)
        for i in range(e["rays"]):
            th = 2*math.pi*i/e["rays"] + rng.uniform(-0.18,0.18); L = rng.uniform(*e["ray_len_m"])
            pts=[c]; x,y = 0.0,0.0; seg = L/6
            for k in range(6):
                th2 = th + rng.uniform(-0.35,0.35)
                x += seg*math.cos(th2); y += seg*math.sin(th2); pts.append((c[0]+x*PX_E, c[1]+y*PX_S))
            wdt = 3 if L>3.4 else 2
            md.line(pts, fill=C["crack_line"], width=wdt); ad.line(pts, fill=(255,255,255), width=wdt)
        # ejecta: cosine about ejecta_dir, exp decay
        base = math.radians(e["ejecta_dir_deg"])
        for _ in range(140):
            phi = rng.gauss(0,0.55); r = -e["ejecta_lambda_m"]*math.log(rng.random()+1e-9)*0.6+e["r_crater_m"]
            x = c[0]+r*math.cos(base+phi)*PX_E; y = c[1]+r*math.sin(base+phi)*PX_S
            s = rng.uniform(3,9); ell(md,(x,y),s,s*0.8,fill=C["debris"]); ell(ad,(x,y),s,s*0.8,fill=(0,160,255))
    elif e["kind"]=="fire":
        fx,fy = e["fuel_m"][0]*PX_E, e["fuel_m"][1]*PX_S
        ell(md,c,fx,fy,fill=C["scorch"]); ell(ad,c,fx,fy,outline=(255,120,0),w=3)
        # soot V-plume rising (up-screen) from the seat, opening upward
        apex=(c[0],c[1]-fy*0.6); top=apex[1]-3.5*PX_S
        poly=[apex,(apex[0]-1.6*PX_E,top),(apex[0]+1.6*PX_E,top)]
        md.polygon(poly, fill=C["soot_plume"]); ad.polygon(poly, outline=(120,120,120), width=2)
    elif e["kind"]=="pier_failure":
        tr = e["talus_r_m"]; ell(md,c,tr*PX_E,tr*PX_S,fill=C["talus"]); ell(ad,c,tr*PX_E,tr*PX_S,outline=(0,90,180),w=3)
        for _ in range(e["n_blocks"]):
            r = rng.uniform(0.3,1.0)*tr; th = rng.uniform(0,2*math.pi)
            x = c[0]+r*math.cos(th)*PX_E; y = c[1]+r*math.sin(th)*PX_S
            s = rng.uniform(10,22); ell(md,(x,y),s,s*0.8,fill=C["debris"]); ell(ad,(x,y),s,s*0.8,fill=(0,160,255))
            for k in range(rng.choice([1,2,3])):   # impact fracture: 1-3 short rays under the block only
                t2 = rng.uniform(0,2*math.pi); L = rng.uniform(0.25,0.6)
                p2=(x+L*math.cos(t2)*PX_E, y+L*math.sin(t2)*PX_S); md.line([(x,y),p2],fill=C["impact_fracture"],width=2); ad.line([(x,y),p2],fill=(255,200,0),width=2)
    elif e["kind"]=="breach":
        sp = e["span_m"]*PX_S; md.rectangle([c[0]-40,c[1]-sp/2,c[0]+40,c[1]+sp/2], fill=C["crater"]); ad.rectangle([c[0]-40,c[1]-sp/2,c[0]+40,c[1]+sp/2], outline=(160,0,160), width=4)
        for _ in range(e["n_debris"]):
            r = -e["debris_lambda_m"]*math.log(rng.random()+1e-9)*0.7; y = c[1]+rng.gauss(0,sp/3)
            x = c[0]+40+r*PX_E; s = max(4, 18-3*r)
            ell(md,(x,y),s,s*0.8,fill=C["debris"]); ell(ad,(x,y),s,s*0.8,fill=(0,160,255))
            if s>8:
                t2 = rng.uniform(0,2*math.pi); p2=(x+0.4*math.cos(t2)*PX_E, y+0.4*math.sin(t2)*PX_S)
                md.line([(x,y),p2],fill=C["impact_fracture"],width=2); ad.line([(x,y),p2],fill=(255,200,0),width=2)
# legend
ad.rectangle([8,8,600,150], fill=(0,0,0)); f = ImageFont.load_default()
lines = ["DAMAGE MAP (authored events; crack law): cracks ONLY where drawn; every other stone SMOOTH + WHOLE",
 "white = crack lines (blast radials)   yellow = impact fractures under fallen blocks   magenta = crater / breach",
 "blue = debris (ejecta / talus / breach fan)   orange ring = fire scorch (NO cracks)   grey V = soot plume up the wall",
 "E1 blast at the gate   E2 fire in the east stalls   E3 NE pier failed, vault fell   E4 west wall breached inward"]
for i,l in enumerate(lines): ad.text((14,14+i*32), l, fill=(255,255,255), font=f)
im.save(f"{out}/b1d_damage_annot.png"); mask.save(f"{out}/b1d_damage_mask.png")
json.dump({"px_per_m_east":PX_E,"px_per_m_south":PX_S,"gate_px":GATE,"seed":20260920,"events":events,"classes":C}, open(f"{out}/b1d_events.json","w"), indent=1)
print("damage map written")
