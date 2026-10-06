#!/usr/bin/env python3
"""barrow_v2 SW level (R-C9-159, lane BS): Matt's sheets -- each view at v1's camera beside sketch A's matching area AND
beside a still of the live v1 Barrow (barrow_full scenes/barrow_painted.tscn, tools/v2sw_run.gd -- v1stills).
    v2sw_sheets.py -> section_v1cam/look/R-C9-159_<view>_vs_sketchA_vs_v1.jpg"""
import pathlib
from PIL import Image, ImageDraw, ImageFont
ROOT = pathlib.Path(__file__).resolve().parents[1]
S, V1, LOOK = ROOT / "section_v1cam/stills", ROOT / "section_v1cam/v1ref", ROOT / "section_v1cam/look"
LOOK.mkdir(parents=True, exist_ok=True)
SKA = Image.open(ROOT / "sites/BV3r2-A.png").convert("RGB")
BOX = {"S1_wreck": (0, 270, 520, 563), "S2_coast": (150, 560, 670, 853), "S3_cave_stair": (380, 560, 900, 853)}
V1S = {"S1_wreck": "V1_tarn", "S2_coast": "V1_ring", "S3_cave_stair": "V1_door"}
LAB = {"S1_wreck": "the wreck (p01)", "S2_coast": "the coast and its cliff", "S3_cave_stair": "the sea cave and the stair (p03)"}
F = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26); f2 = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
for k in BOX:
    a = SKA.crop(BOX[k]).resize((960, 540), Image.LANCZOS)
    b = Image.open(S / f"{k}.png").convert("RGB")
    b.save(LOOK / f"R-C9-159_{k}_1920.jpg", quality=92)
    b = b.resize((960, 540), Image.LANCZOS)
    c = Image.open(V1 / f"{V1S[k]}.png").convert("RGB").resize((960, 540), Image.LANCZOS)
    W = Image.new("RGB", (2920, 630), (246, 244, 238)); d = ImageDraw.Draw(W)
    d.text((12, 10), f"R-C9-159 barrow_v2 SW as a level of the v1 Barrow -- {LAB[k]}   (v1 camera: ortho, pitch 52.95, yaw 47, plate 100.6 px/m)", fill=(20, 30, 60), font=F)
    for i, (im, cap) in enumerate(((a, "sketch A (look of record), matching area -- not to scale"), (b, "barrow_v2 SW, live in the v1 engine (painted ground, baked models, 3D heather, snow, water)"), (c, "the v1 Barrow, live, same camera and engine (for consistency)"))):
        W.paste(im, (10 + i * 970, 50)); d.text((14 + i * 970, 595), cap, fill=(40, 40, 40), font=f2)
    W.save(LOOK / f"R-C9-159_{k}_vs_sketchA_vs_v1.jpg", quality=90)
    print("sheet", k)
