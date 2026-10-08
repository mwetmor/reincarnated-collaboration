#!/usr/bin/env python3
"""BV2F PT (R-C9-232): the M2'' sheet -- the REPAINTED pilot, built in-engine (left), beside SKETCH A at the same frame
(middle: sites/BV3r2-A.png, the layout of record's own map u = (x - 780) / 24, v = (452 - y) / (24 sin pitch) at z = 0,
upscaled) and barrow v1 at the same zoom (right). Phone-sized (<= 2000 px wide). No image spend.
    python3 fid/pt/tools/m2pp_sheets.py <stills dir> [rows json]"""
import json, math, os, sys
from PIL import Image, ImageDraw
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C9 = os.path.dirname(os.path.dirname(FID))
ST = sys.argv[1]
V1 = FID + "/pc/v1_stills"
OUT = FID + "/pt/m2pp"
os.makedirs(OUT, exist_ok=True)
SPEC = {s["name"]: s for s in json.load(open(FID + "/ph/pilot_p11_spec.json"))["stills"]}
ROWS = json.loads(sys.argv[2]) if len(sys.argv) > 2 else [
    ["the mere", "pilot_02", "mere"], ["the barrow door", "pilot_04", "barrow_door"],
    ["the stone circle", "pilot_12", "stone_ring"], ["shingle + the wreck", "pilot_05", "shore"],
    ["the cove cliffs + the stair", "pilot_11", "outcrop_field"], ["heather", "pilot_08", "start"]]
SK = Image.open(C9 + "/barrow_v2/sites/BV3r2-A.png").convert("RGB")
P = math.radians(52.95354112560294)
PPM = 100.617553710938
W, H = 640, 360
BG = (245, 243, 238)
sh = Image.new("RGB", (3 * W + 40, len(ROWS) * (H + 34) + 46), BG)
d = ImageDraw.Draw(sh)
d.text((12, 12), "M2'' -- BV2F pilot REPAINT (left: built in-engine) | sketch A, same frame (middle) | barrow v1, same zoom (right)",
       fill=(20, 20, 20))
for i, (cap, pn, v1n) in enumerate(ROWS):
    y = 40 + i * (H + 34)
    uc, vc = SPEC[pn]["camera_centre_ground_uv"]
    hu, hv = 1920 / PPM / 2, 1080 / (PPM * math.sin(P)) / 2
    box = (780 + 24 * (uc - hu), 452 - 24 * math.sin(P) * (vc + hv), 780 + 24 * (uc + hu), 452 - 24 * math.sin(P) * (vc - hv))
    sk = SK.crop(tuple(int(round(b)) for b in box)).resize((W, H), Image.LANCZOS)
    d.text((12, y), "pilot: %s (%s)" % (cap, pn), fill=(20, 20, 20))
    d.text((W + 22, y), "sketch A, same frame", fill=(20, 20, 20))
    d.text((2 * W + 32, y), "v1: %s" % v1n, fill=(20, 20, 20))
    sh.paste(Image.open("%s/%s.png" % (ST, pn)).convert("RGB").resize((W, H)), (10, y + 16))
    sh.paste(sk, (W + 20, y + 16))
    sh.paste(Image.open("%s/%s.png" % (V1, v1n)).convert("RGB").resize((W, H)), (2 * W + 30, y + 16))
sh.save(OUT + "/M2pp_pilot_sketchA_v1.jpg", quality=86)
print(OUT + "/M2pp_pilot_sketchA_v1.jpg")
