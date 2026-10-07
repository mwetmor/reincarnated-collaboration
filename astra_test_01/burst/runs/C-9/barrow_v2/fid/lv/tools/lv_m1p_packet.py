#!/usr/bin/env python3
"""BV2F LV Phase 1' M1' packet (fid/lv/M1p/): phone sheets of the ART blockout.
    python3 fid/lv/tools/lv_m1p_packet.py
M1p_stills_A/B/C.jpg   12 play-camera stills, each beside sketch A's matching area (not to scale)
M1p_map.jpg            the labelled top-down map
M1p_guide.jpg          the class-tinted guide + its class map
M1p_cover.jpg          one phone screen: three asks, one recommendation each"""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
M = os.path.join(LV, "M1p"); RAW = os.path.join(M, "stills_raw")
SK = os.path.normpath(os.path.join(LV, "..", "..", "sites", "BV3r2-A.png"))
B = lambda n: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", n)
R = lambda n: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", n)
spec = [s for s in json.load(open(os.path.join(M, "stills_spec.json"))) if "topdown" not in s]
L = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))


def crop(pt, w=600, h=338):
    im = Image.open(SK).convert("RGB")
    x0 = int(min(max(0, pt[0] - w // 2), im.width - w)); y0 = int(min(max(0, pt[1] - h // 2), im.height - h))
    c = im.crop((x0, y0, x0 + w, y0 + h)); d = ImageDraw.Draw(c)
    px, py = pt[0] - x0, pt[1] - y0
    d.ellipse([px - 7, py - 7, px + 7, py + 7], outline=(255, 40, 40), width=3)
    return c


def stills():
    out = []
    for si, ch in enumerate([spec[i:i + 4] for i in range(0, len(spec), 4)]):
        rh, sw, cw = 450, 800, 675
        sh = Image.new("RGB", (sw + cw + 30, 60 + len(ch) * (rh + 50)), (24, 24, 28)); d = ImageDraw.Draw(sh)
        d.text((10, 12), "barrow_v2 ART blockout at the PLAY camera (v1 camera + zoom)  |  sketch A, same area", fill=(255, 255, 255), font=B(24))
        for i, s in enumerate(ch):
            y = 60 + i * (rh + 50)
            sh.paste(Image.open(os.path.join(RAW, s["name"] + ".png")).convert("RGB").resize((sw, rh), Image.LANCZOS), (10, y + 36))
            sh.paste(crop(s["sketch_px"]).resize((cw, rh), Image.LANCZOS), (20 + sw, y + 36))
            d.text((10, y + 2), "%s -- %s" % (s["name"][:2], s["what"]), fill=(255, 225, 120), font=B(30))
        p = os.path.join(M, "M1p_stills_%s.jpg" % "ABC"[si]); sh.save(p, quality=88); out.append(p)
    return out


def map_sheet():
    st = json.load(open(os.path.join(RAW, "stills.json")))
    td = next(s for s in st["stills"] if s["name"] == "map_topdown")
    cu, cv, hm = td["topdown"]
    im = Image.open(os.path.join(RAW, "map_topdown.png")).convert("RGB"); d = ImageDraw.Draw(im)
    k = im.height / hm
    P = lambda u, v: (im.width / 2 + (u - cu) * k, im.height / 2 - (v - cv) * k)
    labels = []
    for pl in L["placements"]:
        if pl["id"] in ("wreck", "barrow_front", "longhall", "fallen_gable"):
            labels.append(({"wreck": "the wreck", "barrow_front": "barrow door", "longhall": "burnt hall + great door", "fallen_gable": "fallen gable"}[pl["id"]], pl["uv"]))
    mer = L["regions"]["mere"]
    labels.append(("frozen mere", [sum(q[0] for q in mer) / len(mer), sum(q[1] for q in mer) / len(mer)]))
    cav = next(o for o in L["openings"] if o["id"] == "sea_cave_mouth")["centre_sim"]
    labels += [("sea cave + stair", [cav[0], -cav[1]]), ("stone ring / start", [0.0, 0.0])]
    for t, (u, v) in labels:
        x, y = P(u, v)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(230, 40, 200))
        tw = d.textlength(t, font=B(40))
        tx = x + 14 if x + 14 + tw < im.width - 10 else x - 14 - tw
        d.text((tx, y - 22), t, fill=(255, 255, 255), font=B(40), stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((20, 20), "barrow_v2 ART blockout -- top-down, screen-up = up-screen (v), 66 x 51 m window", fill=(255, 255, 255), font=B(30), stroke_width=4, stroke_fill=(0, 0, 0))
    im.thumbnail((2000, 2000)); p = os.path.join(M, "M1p_map.jpg"); im.save(p, quality=88); return p


def guide():
    a = Image.open(os.path.join(LV, "guide_art", "guide_art_preview.jpg")).convert("RGB")
    b = Image.open(os.path.join(LV, "guide_art", "class_art_preview.jpg")).convert("RGB")
    s = Image.new("RGB", (2000, a.height + b.height + 110), (24, 24, 28)); d = ImageDraw.Draw(s)
    d.text((10, 10), "the class-tinted GUIDE (v1's recipe, frozen Tier-B tools; 6,656 x 4,096 = 5 x 5 canvases)", fill=(255, 255, 255), font=B(24))
    s.paste(a, (0, 50)); d.text((10, a.height + 58), "its class map", fill=(255, 255, 255), font=B(24)); s.paste(b, (0, a.height + 100))
    p = os.path.join(M, "M1p_guide.jpg"); s.save(p, quality=86); return p


def cover():
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), (22, 22, 26)); d = ImageDraw.Draw(im)
    y = 40
    d.text((40, y), "barrow_v2 - M1' (art blockout)", fill=(255, 255, 255), font=B(56)); y += 84
    mp = Image.open(os.path.join(M, "M1p_map.jpg")).convert("RGB"); mp.thumbnail((1000, 640))
    im.paste(mp, ((W - mp.width) // 2, y)); y += mp.height + 30
    asks = [("1. The composition: approve it for paint?", "RECOMMENDED: yes -- start the paint pilot on the home ground.",
             "Built from sketch A as drawn: wreck W, cave + stair SW, barrow door N with the stream to the mere, the stone ring at the start, the hall facing you E, the fallen gable its own ruin SE. 66 × 51 m, painted as 25 canvases (v1: 53 × 41 m, 16)."),
            ("2. The burnt hall: closed sides or an open ruin?", "RECOMMENDED: closed sides except the great door.",
             "The burnt walls stay walls, so the painter cannot read gaps as extra entrances (no false doorways)."),
            ("3. How do you walk it?", "RECOMMENDED: the .command on the Mac now.", "Double-click 'Walk barrow_v2 art.command'. A packaged .app can follow later.")]
    for t, rec, why in asks:
        d.text((40, y), t, fill=(255, 225, 120), font=B(40)); y += 54
        for line in textwrap.wrap(rec, 44):
            d.text((60, y), line, fill=(140, 230, 140), font=B(34)); y += 44
        for line in textwrap.wrap(why, 56):
            d.text((60, y), line, fill=(225, 225, 225), font=R(30)); y += 38
        y += 22
    d.rectangle([30, y, W - 30, y + 110], outline=(120, 180, 255), width=4)
    for i, line in enumerate(textwrap.wrap("Geometry check P6\u2032: PASS \u2014 present, in place, true proportions (PH 51d955677)", 54)[:2]):
        d.text((50, y + 16 + 42 * i), line, fill=(170, 210, 255), font=R(32))
    y += 110
    p = os.path.join(M, "M1p_cover.jpg"); im.save(p, quality=90); print("cover px used", y); return p


if __name__ == "__main__":
    print(stills(), map_sheet(), guide(), cover())
