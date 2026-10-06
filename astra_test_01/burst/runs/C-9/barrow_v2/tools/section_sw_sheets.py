#!/usr/bin/env python3
"""barrow_v2 SECTION SW (R-C9-158, lane BS): Matt's comparison sheets.

    section_sw_sheets.py   -> section_sw/look/R-C9-158_<still>_vs_sketchA.jpg  (sketch-A crop | unpainted guide | painted)
                              section_sw/look/R-C9-158_section_overview.jpg  (the whole painted section over its guide)
The sketch-A crop is found the way the paint briefs find their sketch detail: inverse-distance interpolation between
the six anchors + the start read off the spawn plan (cfg_barrow_v2.json sketch_detail.ties); sketch A is not to scale,
so the crop is sized to the game window at sketch A's local scale (about 11 px per metre near the coast).
"""
import json, pathlib
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[1]
SD = ROOT / "section_sw"
LOOK = SD / "look"
LOOK.mkdir(parents=True, exist_ok=True)
SKA = Image.open(ROOT / "sites/BV3r2-A.png").convert("RGB")
TIES = json.load(open(ROOT / "paint/cfg_barrow_v2.json"))["sketch_detail"]["ties"]
SEC = json.load(open(ROOT / "godot/data/section_sw/section.json"))
STILLS = [("S1_V3_wreck", "V3 -- the wreck (p01)"), ("S2_coast", "between -- the coast and its cliff"), ("S3_V7_cave_stair", "V7 -- the sea cave and the stair (p03)")]
try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    SMALL = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
except Exception:
    FONT = SMALL = ImageFont.load_default()


def sk_crop(x, y, w_m=25.37, h_m=17.88, ppm_sk=11.2):
    ws = [(1.0 / ((x - q[0]) ** 2 + (y - q[1]) ** 2 + 4.0), q) for q in TIES]
    tw = sum(w for w, _ in ws)
    u = sum(w * q[2] for w, q in ws) / tw
    v = sum(w * q[3] for w, q in ws) / tw
    cw, ch = w_m * ppm_sk, h_m * ppm_sk
    u = min(max(u, cw / 2), SKA.width - cw / 2)
    v = min(max(v, ch / 2), SKA.height - ch / 2)
    return SKA.crop((int(u - cw / 2), int(v - ch / 2), int(u + cw / 2), int(v + ch / 2))).resize((960, 540), Image.LANCZOS)


targets = SEC["stills_targets"]
for (sid, label), t in zip(STILLS, targets):
    g = Image.open(SD / "stills_guide" / f"{sid}.png").convert("RGB").resize((960, 540), Image.LANCZOS)
    p = Image.open(SD / "stills_painted" / f"{sid}.png").convert("RGB")
    p.save(LOOK / f"R-C9-158_{sid}_painted_1920.jpg", quality=92)
    p = p.resize((960, 540), Image.LANCZOS)
    s = sk_crop(*t)
    W = Image.new("RGB", (960 * 3 + 40, 540 + 90), (246, 244, 238))
    d = ImageDraw.Draw(W)
    d.text((12, 10), f"R-C9-158 barrow_v2 SECTION SW -- {label}   (game camera: ortho, pitch 52.95, yaw 0; ZOOM-GD 25.4 x 17.9 m window)", fill=(20, 30, 60), font=FONT)
    for i, (im, cap) in enumerate(((s, "sketch A (look of record), matching area -- not to scale"), (g, "the 3D section, UNPAINTED (the guide the painter followed)"), (p, "the 3D section, PAINTED (the paint-over projected through the fixed camera) + hero"))):
        W.paste(im, (10 + i * 970, 50))
        d.text((14 + i * 970, 50 + 545), cap, fill=(40, 40, 40), font=SMALL)
    W.save(LOOK / f"R-C9-158_{sid}_vs_sketchA.jpg", quality=90)
    print("sheet", sid)

pg = ROOT / "paint/section_sw/section_sw_painted_preview.jpg"
gg = ROOT / "paint/section_sw/section_sw_guide_preview.jpg"
if pg.exists() and gg.exists():
    a, b = Image.open(gg).convert("RGB"), Image.open(pg).convert("RGB")
    W = Image.new("RGB", (a.width, a.height * 2 + 20), (246, 244, 238))
    W.paste(a, (0, 0))
    W.paste(b, (0, a.height + 20))
    W.save(LOOK / "R-C9-158_section_guide_over_painted.jpg", quality=88)
    print("overview sheet")
