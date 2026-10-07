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
L = json.load(open(os.path.join(LV, "layout_v7c.json")))
try:
    F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    FS = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
    FT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 40)
except Exception:
    F = FS = FT = ImageFont.load_default()
SKPT = json.load(open(os.path.join(LV, "frame_proof", "sketch_anchor_px.json")))
HERO_PX = {"p01": (160, 400), "p02": (815, 135), "p03": (570, 790), "p04": (1290, 420), "p05": (650, 365), "p06": (1420, 560), "start": (780, 452)}
VAR = "v7c"


def sketch_crop(pt, w=600, h=400):
    im = Image.open(SK).convert("RGB")
    x0 = min(max(0, pt[0] - w // 2), im.width - w)
    y0 = min(max(0, pt[1] - h // 2), im.height - h)
    return im.crop((x0, y0, x0 + w, y0 + h)), (pt[0] - x0, pt[1] - y0)


def sketch_pt(s):
    p = s.get("point", "start")
    if s["name"].startswith("1") and "_disc_" in s["name"] and p in SKPT:
        return SKPT[p]
    if s["name"].startswith("14"):
        return HERO_PX["p03"]
    return HERO_PX.get(p, HERO_PX["start"])


def _sk(s, cw, rh):
    cr, p = sketch_crop([int(v) for v in sketch_pt(s)])
    cr = cr.resize((cw, rh), Image.LANCZOS)
    dc = ImageDraw.Draw(cr)
    px, py = p[0] * cw / 600, p[1] * rh / 400
    dc.ellipse([px - 9, py - 9, px + 9, py + 9], outline=(255, 40, 40), width=4)
    return cr


def stills_sheets():
    spec = {s["name"]: s for s in json.load(open(os.path.join(M1, "stills_spec_v7c.json"))) if "topdown" not in s}
    names = sorted(spec)
    hg = [n for n in names if spec[n].get("point") in ("p04", "p06")]
    rest = [n for n in names if n not in hg]
    out = []
    # v7c beside sketch A
    for si, chunk in enumerate([rest[i:i + 4] for i in range(0, len(rest), 4)]):
        rh, sw, cw = 450, 800, 675
        sheet = Image.new("RGB", (sw + cw + 30, 60 + len(chunk) * (rh + 50)), (24, 24, 28))
        d = ImageDraw.Draw(sheet)
        d.text((10, 12), "barrow_v2 v7c at the PLAY camera (v1 camera + zoom), framed on the hero  |  sketch A, same area (NOT to scale)", fill=(255, 255, 255), font=FS)
        for i, n in enumerate(chunk):
            s = spec[n]
            y = 60 + i * (rh + 50)
            sheet.paste(Image.open(os.path.join(M1, "stills_raw_v7c", n + ".png")).convert("RGB").resize((sw, rh), Image.LANCZOS), (10, y + 36))
            sheet.paste(_sk(s, cw, rh), (20 + sw, y + 36))
            d.text((10, y + 2), "%s -- %s" % (n[:2], s["what"]), fill=(255, 225, 120), font=F)
        p = os.path.join(M1, "M1_stills_%s.jpg" % "ABCD"[si])
        sheet.save(p, quality=88)
        out.append(p)
    # the hall + gable views: v7c | v7b | sketch A
    rh, sw, cw = 360, 640, 540
    sheet = Image.new("RGB", (2 * sw + cw + 40, 60 + len(hg) * (rh + 50)), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    d.text((10, 12), "HALL + GABLE:  v7c (RECOMMENDED: hall on the NE edge, door to the camera; gable its own ruin)  |  v7b (v6 heading)  |  sketch A", fill=(255, 255, 255), font=FS)
    for i, n in enumerate(hg):
        s = spec[n]
        y = 60 + i * (rh + 50)
        sheet.paste(Image.open(os.path.join(M1, "stills_raw_v7c", n + ".png")).convert("RGB").resize((sw, rh), Image.LANCZOS), (10, y + 36))
        sheet.paste(Image.open(os.path.join(M1, "stills_raw_v7b", n + ".png")).convert("RGB").resize((sw, rh), Image.LANCZOS), (20 + sw, y + 36))
        sheet.paste(_sk(s, cw, rh), (30 + 2 * sw, y + 36))
        d.text((10, y + 2), "%s -- %s   (left v7c, middle v7b)" % (n[:2], s["what"]), fill=(255, 225, 120), font=FS)
    p = os.path.join(M1, "M1_stills_hall_gable_v7c_v7b.jpg")
    sheet.save(p, quality=88)
    out.append(p)
    return out


def map_sheet():
    RAWV = os.path.join(M1, "stills_raw_v7c")
    st = json.load(open(os.path.join(RAWV, "stills.json")))
    td = next(s for s in st["stills"] if s["name"] == "map_topdown")
    cu, cv, hm = td["topdown"]
    im = Image.open(os.path.join(RAWV, "map_topdown.png")).convert("RGB")
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
    for o in json.load(open(os.path.join(LV, "guide_v7c", "declared_openings.json")))["openings"]:
        q = P(*o["centre_sim_xy"])
        d.rectangle([q[0] - 8, q[1] - 8, q[0] + 8, q[1] + 8], fill=(220, 30, 200))
    d.text((20, 20), "barrow_v2 layout v7c -- top-down (north up). Gold: the six 8 m spawn discs. Magenta: the deliverer openings. Black line: the walkable edge.",
           fill=(255, 255, 255), font=FS, stroke_width=3, stroke_fill=(0, 0, 0))
    im.thumbnail((2000, 2000))
    p = os.path.join(M1, "M1_map_v7c.jpg")
    im.save(p, quality=88)
    return p


def guide_sheet():
    a = Image.open(os.path.join(LV, "guide_v7c", "guide_v7c_preview.jpg")).convert("RGB")
    b = Image.open(os.path.join(LV, "guide_v7c", "class_v7c_preview.jpg")).convert("RGB")
    a.thumbnail((1990, 1500))
    b.thumbnail((1990, 1500))
    s = Image.new("RGB", (2000, a.height + b.height + 110), (24, 24, 28))
    d = ImageDraw.Draw(s)
    d.text((10, 10), "the class-tinted GUIDE of v7c (v1's recipe, frozen Tier-B tools; 11,776 x 8,704 at v1's px/m)", fill=(255, 255, 255), font=FS)
    s.paste(a, (5, 50))
    d.text((10, a.height + 58), "its CLASS map (snow, path, ice, shrub, rock, mound, shingle, shore ice, stream, ash, char, wood, sea, door-dark)", fill=(255, 255, 255), font=FS)
    s.paste(b, (5, a.height + 100))
    p = os.path.join(M1, "M1_guide_v7c.jpg")
    s.save(p, quality=86)
    return p


def divergence():
    B = json.load(open(os.path.join(LV, "frame_proof", "bearings.json")))
    sb, rb, dd = B["sketch_bearing_deg"], B["renders"]["fixed"]["bearing_deg"], B["renders"]["fixed"]["delta_deg"]
    rows = []
    for k in ["p01", "p02", "p03", "p04", "p05", "p06"]:
        flag = "REGISTERED sketch-vs-oracle divergence #1 (R-C9-165)" if abs(dd[k]) > 15 else "within 15 deg"
        rows.append("%s  sketch %5.1f  v7c %5.1f  delta %+5.1f  -- %s" % (k, sb[k], rb[k], dd[k], flag))
    rows.append("hall  sketch: upper-left -> lower-right, door toward the start  |  v7c: upper-left -> lower-right on the NE edge, door faces SW to the camera + p04  |  v7b: v6 heading, door faces NW (away)")
    rows.append("gable  sketch: the hall's lower-right end  |  v7c: its OWN ruin on p06's ray (the hall cannot reach p06's ray, R-C9-174)  |  v7b: the hall's SW end")
    im = Image.new("RGB", (2000, 120 + 52 * len(rows)), (24, 24, 28))
    d = ImageDraw.Draw(im)
    d.text((14, 14), "Layout v7c vs sketch A: anchor bearings from the start, on screen (deg CCW from screen-right)", fill=(255, 255, 255), font=F)
    for i, r in enumerate(rows):
        d.text((14, 80 + 52 * i), r, fill=(255, 225, 120) if "divergence" in r else (220, 220, 220), font=FS)
    p = os.path.join(M1, "M1_divergence.jpg")
    im.save(p, quality=90)
    return p, rows


if __name__ == "__main__":
    print(stills_sheets(), map_sheet(), guide_sheet(), divergence()[0])
