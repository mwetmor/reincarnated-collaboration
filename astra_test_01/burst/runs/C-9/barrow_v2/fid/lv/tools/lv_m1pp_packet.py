#!/usr/bin/env python3
"""BV2F LV Phase 1'' M1'' packet (fid/lv/M1pp/): phone sheets of the re-built coast, water and cave (R-C9-204/205/206).
    python3 fid/lv/tools/lv_m1pp_packet.py
M1pp_stills_A.jpg / _B.jpg   8 play-camera stills, each beside sketch A's matching area (not to scale)
M1pp_section.jpg             the beach / cliff / cave-route cross-sections with their heights (off the terrain itself)
M1pp_map.jpg                 the labelled top-down map
M1pp_guide.jpg               the class-tinted guide + its class map
M1pp_cover.jpg               one phone screen: three asks, one recommendation each"""
import json, math, os, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
M = os.path.join(LV, "M1pp"); RAW = os.path.join(M, "stills_raw")
SK = os.path.normpath(os.path.join(LV, "..", "..", "sites", "BV3r2-A.png"))
BFD = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", "art"))
B = lambda n: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", n)
R = lambda n: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", n)
spec = [s for s in json.load(open(os.path.join(M, "stills_spec.json"))) if "topdown" not in s]
L = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))
LEV = L["levels_m"]


def crop(pt, w=600, h=338):
    im = Image.open(SK).convert("RGB")
    x0 = int(min(max(0, pt[0] - w // 2), im.width - w)); y0 = int(min(max(0, pt[1] - h // 2), im.height - h))
    c = im.crop((x0, y0, x0 + w, y0 + h)); d = ImageDraw.Draw(c)
    px, py = pt[0] - x0, pt[1] - y0
    d.ellipse([px - 7, py - 7, px + 7, py + 7], outline=(255, 40, 40), width=3)
    return c


def stills():
    out = []
    for si, ch in enumerate([spec[i:i + 5] for i in range(0, len(spec), 5)]):
        rh, sw, cw = 450, 800, 675
        sh = Image.new("RGB", (sw + cw + 30, 60 + len(ch) * (rh + 50)), (24, 24, 28)); d = ImageDraw.Draw(sh)
        d.text((10, 12), "barrow_v2 Phase 1'' close-out (R-C9-226) at the PLAY camera (v1 camera + zoom)  |  sketch A, the SAME feature", fill=(255, 255, 255), font=B(24))
        for i, s in enumerate(ch):
            y = 60 + i * (rh + 50)
            sh.paste(Image.open(os.path.join(RAW, s["name"] + ".png")).convert("RGB").resize((sw, rh), Image.LANCZOS), (10, y + 36))
            sh.paste(crop(s["sketch_px"]).resize((cw, rh), Image.LANCZOS), (20 + sw, y + 36))
            d.text((10, y + 2), "%s -- %s" % (s["name"][:2], s["what"]), fill=(255, 225, 120), font=B(26))
        p = os.path.join(M, "M1pp_stills_%s.jpg" % "ABC"[si]); sh.save(p, quality=88); out.append(p)
    return out


def section():
    """three profiles straight off terrain_h.f32 (the walk surface) + the stair's nosing line and the kit's crest"""
    lv = json.load(open(os.path.join(BFD, "level.json"))); hf = lv["sim"]["heightfield"]; H, W = hf["shape"]; ex = hf["extent_sim_m"]
    Z = np.fromfile(os.path.join(BFD, "terrain_h.f32"), "<f4").reshape(H, W)
    zat = lambda u, v: float(Z[min(max(int(round((-v - ex["y0"]) * 4)), 0), H - 1), min(max(int(round((u - ex["x0"]) * 4)), 0), W - 1)])
    F = L["route"]["frame"]; o, dd = F["origin_uv"], F["along_uv"]; nn = (dd[1], -dd[0])
    fr = lambda t, s: (o[0] + dd[0] * t + nn[0] * s, o[1] + dd[1] * t + nn[1] * s)
    wr = L["placements"][[p["id"] for p in L["placements"]].index("wreck")]["uv"]
    profs = [("W: the plateau -> the shingle beach -> the shore ice (the wreck)", (-8.0, wr[1]), (-38.0, wr[1]), [("wreck", math.dist((-8.0, wr[1]), wr))]),
             ("S: the clifftop -> the sea cliff -> the shore-fast ice", (12.0, -8.0), (12.0, -27.0), []),
             ("THE ROUTE: inside the cave -> the iced landing -> the stair cleft, climbing inland -> the clifftop", None, None, [])]
    Wd, Hd = 1600, 1560
    im = Image.new("RGB", (Wd, Hd), (250, 248, 243)); d = ImageDraw.Draw(im)
    d.text((30, 20), "barrow_v2 Phase 1'' -- cross-sections (metres, off the terrain the knight walks; true scale, no exaggeration)", fill=(20, 20, 20), font=B(28))
    y0 = 90
    for k, (title, a, b, marks) in enumerate(profs):
        if a is None:
            RP = L["route"]["points_uv"]
            Zw = np.fromfile(os.path.join(BFD, hf["walk_file"]), "<f4").reshape(H, W)
            zw = lambda u, v: float(Zw[min(max(int(round((-v - ex["y0"]) * 4)), 0), H - 1), min(max(int(round((u - ex["x0"]) * 4)), 0), W - 1)])
            names_ = ["cave_back", "cave_mouth", "shelf_mid", "bottom_landing", "stair_foot", "stair_top", "landing", "clifftop"]
            seq = [tuple(RP[k]) for k in names_]
            Fs = L["route"]["frame"]
            dist, zs, acc, marks = [], [], 0.0, []
            for k_, (p0, p1) in enumerate(zip(seq[:-1], seq[1:])):
                marks.append((names_[k_].replace("_", " "), acc))
                n_ = max(1, int(math.dist(p0, p1) / 0.1))
                for i in range(n_):
                    f = i / n_
                    p = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
                    dist.append(acc + math.dist(p0, p))
                    if names_[k_] == "stair_foot":
                        zs.append(L["levels_m"]["shelf"] + f * (Fs["top_z"] - L["levels_m"]["shelf"]))
                    else:
                        zs.append(zw(*p))
                acc += math.dist(p0, p1)
            marks = [m for m in marks if m[0] in ("cave mouth", "stair foot", "stair top")]
        else:
            n_ = int(math.dist(a, b) / 0.1)
            dist = [math.dist(a, b) * i / n_ for i in range(n_ + 1)]
            zs = [zat(a[0] + (b[0] - a[0]) * i / n_, a[1] + (b[1] - a[1]) * i / n_) for i in range(n_ + 1)]
        L_ = max(dist)
        sx = min(28.0, (Wd - 300) / L_)
        sz = sx
        zmin, zmax = -7.0, 5.0
        ph = int((zmax - zmin) * sz) + 20
        top = y0 + 40
        d.text((30, y0), title, fill=(30, 30, 90), font=B(26))
        X = lambda x: 100 + x * sx
        Y = lambda z: top + (zmax - z) * sz
        sea = LEV["sea"]
        d.rectangle([X(0), Y(sea), X(L_), Y(zmin)], fill=(60, 85, 115))
        poly = [(X(x), Y(z)) for x, z in zip(dist, zs)] + [(X(L_), Y(zmin)), (X(0), Y(zmin))]
        d.polygon(poly, fill=(205, 198, 186), outline=(60, 50, 40))
        for z, lab in ((0.0, "plateau 0"), (LEV["shore_ice_top"], "shore ice %.1f" % LEV["shore_ice_top"]), (sea, "sea %.1f" % sea), (LEV["shelf"], "iced landing %.1f" % LEV["shelf"]),
                       (2.5, "crest +2.5")):
            d.line([X(0), Y(z), X(L_), Y(z)], fill=(150, 150, 150), width=1)
            d.text((X(L_) + 6, Y(z) - 10), lab, fill=(80, 80, 80), font=R(18))
        for lab, x in marks:
            d.line([X(x), Y(zmax), X(x), Y(zmin)], fill=(200, 60, 60), width=2)
            d.text((X(x) + 6, Y(zmax) + 4), lab, fill=(200, 60, 60), font=R(20))
        for m in range(0, int(L_) + 1, 5):
            d.line([X(m), Y(zmin), X(m), Y(zmin) + 8], fill=(0, 0, 0)); d.text((X(m) - 6, Y(zmin) + 10), str(m), fill=(0, 0, 0), font=R(16))
        y0 = top + ph + 70
    d.text((30, Hd - 60), "Levels: plateau 0 | clifftop crest %.1f..%.1f | sea cliffs %.1f-%.1f m | beach drop %.1f m over %.0f m | shore ice %.1f | sea %.1f | shelf %.1f" % (
        LEV["clifftop_crest"][0], LEV["clifftop_crest"][1], LEV["sea_cliff_height_m"][0], LEV["sea_cliff_height_m"][1], LEV["beach_drop_m"], LEV["beach_width_m"],
        LEV["shore_ice_top"], LEV["sea"], LEV["shelf"]), fill=(20, 20, 20), font=R(22))
    p = os.path.join(M, "M1pp_section.jpg"); im.save(p, quality=90); return p


def map_sheet():
    st = json.load(open(os.path.join(RAW, "stills.json")))
    td = next(s for s in st["stills"] if s["name"] == "map_topdown")
    im = Image.open(os.path.join(RAW, "map_topdown.png")).convert("RGB"); d = ImageDraw.Draw(im)
    cu, cv, hm = td["topdown"]; ppm = td["px_per_m"]
    P = lambda u, v: (im.width / 2 + (u - cu) * ppm, im.height / 2 - (v - cv) * ppm)
    pl = {p["id"]: p for p in L["placements"]}
    RP = L["route"]["points_uv"]
    mere = L["regions"]["mere_outline"]
    labels = [("the wreck (on the shore ice)", pl["wreck"]["uv"]), ("barrow door", pl["barrow_front"]["uv"]), ("burnt hall", pl["longhall"]["uv"]),
              ("fallen gable", pl["fallen_gable"]["uv"]), ("sea cave", RP["cave_mouth"]), ("stair (inland)", RP["stair_top"]), ("start / stone ring", [0.0, 0.0]),
              ("mere ~%.0f m2" % L["route"]["mere_area_m2"], [sum(q[0] for q in mere) / len(mere), sum(q[1] for q in mere) / len(mere)]), ("river", [-27.6, 20.0]),
              ("shingle beach", [-22.0, 1.0]),
              ("shore-fast ice", [-24.0, -10.0]), ("pack ice + floes", [-10.0, -26.0]), ("sea cliffs 6-8 m", [16.0, -20.0])]
    for t, q in labels:
        x, y = P(*q)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 60, 60))
        d.text((x + 14, y - 16), t, fill=(0, 0, 0), font=B(34), stroke_width=4, stroke_fill=(255, 255, 255))
    for s in spec:
        x, y = P(*s["aim_uv"])
        d.rectangle([x - 22, y - 18, x + 22, y + 18], outline=(30, 30, 200), width=4)
        d.text((x - 16, y - 16), s["name"][:2], fill=(30, 30, 200), font=B(28))
    im.thumbnail((2000, 2000)); p = os.path.join(M, "M1pp_map.jpg"); im.save(p, quality=88); return p


def guide():
    a = Image.open(os.path.join(LV, "guide_art", "guide_art_preview.jpg")).convert("RGB")
    b = Image.open(os.path.join(LV, "guide_art", "class_art_preview.jpg")).convert("RGB")
    w = 1600; a = a.resize((w, int(a.height * w / a.width))); b = b.resize((w, int(b.height * w / b.width)))
    s = Image.new("RGB", (w, a.height + b.height + 20), (24, 24, 28)); s.paste(a, (0, 0)); s.paste(b, (0, a.height + 20))
    p = os.path.join(M, "M1pp_guide.jpg"); s.save(p, quality=86); return p


def cover():
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), (22, 22, 26)); d = ImageDraw.Draw(im)
    y = 40
    d.text((40, y), "barrow_v2 - M1'' close-out (cave, mere, river)", fill=(255, 255, 255), font=B(48)); y += 80
    mp = Image.open(os.path.join(M, "M1pp_map.jpg")).convert("RGB"); mp.thumbnail((1000, 600))
    im.paste(mp, ((W - mp.width) // 2, y)); y += mp.height + 26
    si = L["regions"]["sea_ice"]
    R_ = L["route"]
    asks = [("1. Cave + stair (R-C9-228): approve?", "RECOMMENDED: yes.",
             "No cove: the cliff line is continuous; the cave is an arch worn into the face at the waterline, facing the camera; the stair climbs inland in a natural gully between rock columns, every tread its own stone. Walk-checked PASS."),
            ("2. The iced ledge at the mouth is ~11 x 5 m because the route bar is 5 m wide (big monsters). Keep the bar?", "RECOMMENDED: keep it.",
             "A narrower bar would let the ledge shrink to the mouth itself."),
            ("3. Mere, river, sea (R-C9-227): right?", "RECOMMENDED: yes.",
             "Mere mostly continuous ice with a few branching cracks; the river a tiny open-water ribbon; the pack irregular (huge/tiny plates, rubble, leads of every width), ~2/3 ice; the wreck's ice ragged.")]
    for t, rec, why in asks:
        d.text((40, y), t, fill=(255, 225, 120), font=B(38)); y += 50
        for line in textwrap.wrap(rec, 46):
            d.text((60, y), line, fill=(140, 230, 140), font=B(32)); y += 42
        for line in textwrap.wrap(why, 58):
            d.text((60, y), line, fill=(225, 225, 225), font=R(28)); y += 35
        y += 18
    p = os.path.join(M, "M1pp_cover.jpg"); im.save(p, quality=90); print("cover px used", y); return p


if __name__ == "__main__":
    print(stills(), section(), map_sheet(), guide(), cover())
