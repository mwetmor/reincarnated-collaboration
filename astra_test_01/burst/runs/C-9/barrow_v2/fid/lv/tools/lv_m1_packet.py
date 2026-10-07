#!/usr/bin/env python3
"""BV2F LV Phase 1.4: the M1 packet sheets (v7b only, R-C9-174). Phone-sized jpgs (<= 2000 px wide) in fid/lv/M1/.

    python3 fid/lv/tools/lv_m1_packet.py

M1_stills_A/B/C.jpg  the 12 play-camera stills (v1 camera + zoom), each beside sketch A's matching area (not to scale)
M1_map_v7b.jpg       the labelled top-down map of v7b (anchors + 8 m discs, deliverers, the start)
M1_guide_v7b.jpg     the class-tinted guide (whole envelope) beside its class map
M1_divergence.jpg    R-C9-165 bearing table (anchor bearings vs sketch A) + the hall line
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
M1 = os.path.join(LV, "M1")
RAW = os.path.join(M1, "stills_raw")
SK = os.path.normpath(os.path.join(LV, "..", "..", "sites", "BV3r2-A.png"))
SKS = os.path.normpath(os.path.join(LV, "..", "..", "sites", "BV3r2-A_spawns.png"))
L = json.load(open(os.path.join(LV, "layout_v7b.json")))
try:
    F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    FS = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
    FT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 40)
except Exception:
    F = FS = FT = ImageFont.load_default()
SKPT = json.load(open(os.path.join(LV, "frame_proof", "sketch_anchor_px.json")))
DOOR = {"barrow_front": (815, 135), "hall_porch": (1290, 420), "fallen_gable": (1420, 560), "sea_cave_stair": (570, 790), "wreck": (160, 400)}


def sketch_crop(pt, w=600, h=400):
    im = Image.open(SK).convert("RGB")
    x0 = min(max(0, pt[0] - w // 2), im.width - w)
    y0 = min(max(0, pt[1] - h // 2), im.height - h)
    return im.crop((x0, y0, x0 + w, y0 + h)), (pt[0] - x0, pt[1] - y0)


def sketch_pt(name):
    if name.startswith("01_start"):
        return SKPT["start"]
    if "_disc_" in name:
        return SKPT[name.split("_disc_")[1][:3]]
    return DOOR[name.split("approach_")[1]]


def stills_sheets():
    spec = [s for s in json.load(open(os.path.join(M1, "stills_spec.json"))) if "topdown" not in s]
    out = []
    for si, chunk in enumerate([spec[0:4], spec[4:8], spec[8:12]]):
        rh, sw, cw = 450, 800, 675
        W = sw + cw + 30
        sheet = Image.new("RGB", (W, 60 + len(chunk) * (rh + 50)), (24, 24, 28))
        d = ImageDraw.Draw(sheet)
        d.text((10, 12), "barrow_v2 v7b at the PLAY camera (v1 camera + zoom)  |  sketch A, same area (NOT to scale)", fill=(255, 255, 255), font=FS)
        for i, s in enumerate(chunk):
            y = 60 + i * (rh + 50)
            st = Image.open(os.path.join(RAW, s["name"] + ".png")).convert("RGB").resize((sw, rh), Image.LANCZOS)
            cr, p = sketch_crop([int(v) for v in sketch_pt(s["name"])])
            cr = cr.resize((cw, rh), Image.LANCZOS)
            dc = ImageDraw.Draw(cr)
            px, py = p[0] * cw / 600, p[1] * rh / 400
            dc.ellipse([px - 9, py - 9, px + 9, py + 9], outline=(255, 40, 40), width=4)
            sheet.paste(st, (10, y + 36))
            sheet.paste(cr, (20 + sw, y + 36))
            d.text((10, y + 2), "%s -- %s" % (s["name"][:2], s["what"]), fill=(255, 225, 120), font=F)
        p = os.path.join(M1, "M1_stills_%s.jpg" % "ABC"[si])
        sheet.save(p, quality=88)
        out.append(p)
    return out


def map_sheet():
    st = json.load(open(os.path.join(RAW, "stills.json")))
    td = next(s for s in st["stills"] if s["name"] == "map_topdown")
    cu, cv, hm = td["topdown"]
    im = Image.open(os.path.join(RAW, "map_topdown.png")).convert("RGB")
    k = im.height / hm

    def P(x, y):
        return (im.width / 2 + (x - cu) * k, im.height / 2 - ((-y) - cv) * k)
    d = ImageDraw.Draw(im)
    d.line([P(*q) for q in L["floor"]["polygon"]] + [P(*L["floor"]["polygon"][0])], fill=(20, 20, 20), width=3)
    names = {"p01": "p01 wreck", "p02": "p02 barrow door", "p03": "p03 sea cave + stair", "p04": "p04 hall great door", "p05": "p05 mere ambush", "p06": "p06 fallen gable"}
    for a in L["anchors"]["points"]:
        c = P(a["x"], a["y"])
        r = 8 * k
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=(230, 150, 20), width=5)
        d.text((c[0] - 60, c[1] - 18), names[a["id"]], fill=(255, 240, 200), font=F, stroke_width=4, stroke_fill=(0, 0, 0))
    c = P(0, 0)
    d.line([c[0] - 20, c[1], c[0] + 20, c[1]], fill=(0, 0, 0), width=5)
    d.line([c[0], c[1] - 20, c[0], c[1] + 20], fill=(0, 0, 0), width=5)
    d.text((c[0] + 14, c[1] + 10), "start", fill=(255, 255, 255), font=F, stroke_width=4, stroke_fill=(0, 0, 0))
    for o in json.load(open(os.path.join(LV, "guide", "declared_openings.json")))["openings"]:
        q = P(*o["centre_sim_xy"])
        d.rectangle([q[0] - 8, q[1] - 8, q[0] + 8, q[1] + 8], fill=(220, 30, 200))
    d.text((20, 20), "barrow_v2 layout v7b -- top-down (north up). Gold: the six 8 m spawn discs. Magenta: the deliverer openings. Black line: the walkable edge.",
           fill=(255, 255, 255), font=FS, stroke_width=3, stroke_fill=(0, 0, 0))
    im.thumbnail((2000, 2000))
    p = os.path.join(M1, "M1_map_v7b.jpg")
    im.save(p, quality=88)
    return p


def guide_sheet():
    a = Image.open(os.path.join(LV, "guide", "guide_v7b_preview.jpg")).convert("RGB")
    b = Image.open(os.path.join(LV, "guide", "class_v7b_preview.jpg")).convert("RGB")
    a.thumbnail((1990, 1500))
    b.thumbnail((1990, 1500))
    s = Image.new("RGB", (2000, a.height + b.height + 110), (24, 24, 28))
    d = ImageDraw.Draw(s)
    d.text((10, 10), "the class-tinted GUIDE of v7b (v1's recipe, frozen Tier-B tools; 11,776 x 8,704 at v1's px/m)", fill=(255, 255, 255), font=FS)
    s.paste(a, (5, 50))
    d.text((10, a.height + 58), "its CLASS map (snow, path, ice, shrub, rock, mound, shingle, shore ice, stream, ash, char, wood, sea, door-dark)", fill=(255, 255, 255), font=FS)
    s.paste(b, (5, a.height + 100))
    p = os.path.join(M1, "M1_guide_v7b.jpg")
    s.save(p, quality=86)
    return p


def divergence():
    B = json.load(open(os.path.join(LV, "frame_proof", "bearings.json")))
    sb, rb, dd = B["sketch_bearing_deg"], B["renders"]["fixed"]["bearing_deg"], B["renders"]["fixed"]["delta_deg"]
    rows = []
    for k in ["p01", "p02", "p03", "p04", "p05", "p06"]:
        flag = "REGISTERED sketch-vs-oracle divergence #1 (R-C9-165)" if abs(dd[k]) > 15 else "within 15 deg"
        rows.append("%s  sketch %5.1f  v7b %5.1f  delta %+5.1f  -- %s" % (k, sb[k], rb[k], dd[k], flag))
    rows.append("hall  sketch: upper-left -> lower-right, door toward the start  |  v7b: v6 heading, door faces NW (away from the camera)  -- divergence #2 (R-C9-174)")
    im = Image.new("RGB", (2000, 120 + 52 * len(rows)), (24, 24, 28))
    d = ImageDraw.Draw(im)
    d.text((14, 14), "Layout v7b vs sketch A: anchor bearings from the start, on screen (deg CCW from screen-right)", fill=(255, 255, 255), font=F)
    for i, r in enumerate(rows):
        d.text((14, 80 + 52 * i), r, fill=(255, 225, 120) if "divergence" in r else (220, 220, 220), font=FS)
    p = os.path.join(M1, "M1_divergence.jpg")
    im.save(p, quality=90)
    return p, rows


if __name__ == "__main__":
    print(stills_sheets(), map_sheet(), guide_sheet(), divergence()[0])
