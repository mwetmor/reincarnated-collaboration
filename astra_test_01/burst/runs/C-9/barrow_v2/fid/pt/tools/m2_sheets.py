#!/usr/bin/env python3
"""BV2F PT (R-C9-202): the M2' sheets from the CURRENT build's stills (no image spend), phone-sized (<= 2000 px wide).
    python3 fid/pt/tools/m2_sheets.py <stills dir of the current build>"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C9 = os.path.dirname(os.path.dirname(FID))
ST = sys.argv[1]
V1 = FID + "/pc/v1_stills"
OUT = FID + "/pt/m2"
os.makedirs(OUT, exist_ok=True)
BG = (245, 243, 238)
def lab(d, xy, s):
    d.text(xy, s, fill=(20, 20, 20))
# (1) pilot | v1, same zoom
rows = [("the mere", "pilot_02", "mere (v1's tarn)"), ("the barrow door", "pilot_04", "barrow_door"),
        ("the stone ring", "pilot_12", "stone_ring"), ("shingle + the wreck", "pilot_06", "shore (v1's shore rocks)"),
        ("the sea cliff + moving water", "pilot_09", "outcrop_field (v1's nearest: outcrops)"),
        ("a heather patch", "pilot_08", "start (v1's heather)")]
W, H = 960, 540
sh = Image.new("RGB", (2 * W + 30, len(rows) * (H + 34) + 46), BG)
d = ImageDraw.Draw(sh)
lab(d, (12, 12), "M2' -- BV2F pilot (left: built in-engine, painted, build 186743b58) | barrow v1 (right) -- same play camera, same zoom (ortho 10.7337 m)")
for i, (cap, pn, v1n) in enumerate(rows):
    y = 40 + i * (H + 34)
    lab(d, (12, y), "pilot: %s (%s)" % (cap, pn)); lab(d, (W + 22, y), "v1: %s" % v1n)
    sh.paste(Image.open("%s/%s.png" % (ST, pn)).convert("RGB").resize((W, H)), (10, y + 16))
    sh.paste(Image.open("%s/%s.png" % (V1, v1n.split(" ")[0])).convert("RGB").resize((W, H)), (W + 20, y + 16))
sh.save(OUT + "/M2p_pilot_beside_v1.jpg", quality=86)
# (2) ice + snow
PW, PH = 640, 360
s2 = Image.new("RGB", (3 * PW + 40, 2 * (PH + 34) + 46), BG)
d = ImageDraw.Draw(s2)
lab(d, (12, 12), "M2' -- ICE: the pilot's mere | v1's tarn | sketch A's mere.   SNOW: coastal chunks 0_2/1_2 | neighbouring chunk 2_1 | v1 (painting crops, 1:1 px)")
def fit(im, w, h):
    im = im.convert("RGB"); r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)))
    x0, y0 = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))
p02 = Image.open(ST + "/pilot_02.png"); v1m = Image.open(V1 + "/mere.png")
sk = Image.open(C9 + "/barrow_v2/sites/BV3r2-A.png").crop((75, 72, 662, 374))
for j, (im, cap) in enumerate([(p02.crop((0, 300, 1920, 1080)), "pilot mere (pilot_02, in-engine)"), (v1m.crop((0, 120, 1920, 900)), "v1 tarn (in-engine)"), (sk, "sketch A mere (BV3r2-A)")]):
    x = 10 + j * (PW + 10); lab(d, (x, 40), cap); s2.paste(fit(im, PW, PH), (x, 56))
# snow crops: the pilot painting / v1 painting, windows of mostly open snow
P = np.asarray(Image.open(FID + "/pt/pilot/painting.png").convert("RGB"))
I = json.load(open(FID + "/pt/pilot/ids_built/ids.json"))["placements"]
ID8 = np.asarray(Image.open(FID + "/pt/pilot/ids_built.png").convert("RGB")).astype(int)
idx = np.where(ID8[..., 2] > 100, np.clip(np.round((ID8[..., 1] - 8) / 16), 0, 15).astype(int) * 16 + np.clip(np.round((ID8[..., 0] - 8) / 16), 0, 15).astype(int), 0)
snow = idx == {v["id"]: int(k) for k, v in I.items()}["ground_snow"]
def best(mask, x0, y0, x1, y1):
    bestv, bxy = -1, None
    for y in range(y0, y1 - PH, 40):
        for x in range(x0, x1 - PW, 40):
            v = mask[y:y + PH, x:x + PW].mean()
            if v > bestv: bestv, bxy = v, (x, y)
    return bxy, bestv
(a, va) = best(snow, 0, 1536, 2816, 2560)
(b, vb) = best(snow, 2816, 768, 4096, 1792)
V1P = np.asarray(Image.open(C9 + "/barrow_full/paint/barrow_full_painted.png").convert("RGB"))
gu = np.asarray(Image.open(C9 + "/barrow_full/take/ground/ground_uv.png")); gu = gu[..., 0] if gu.ndim == 3 else gu
V1I = np.asarray(Image.open(C9 + "/barrow_full/take/ids/ids.png").convert("RGB"))
ground = V1I[..., 2] <= 100
ys, xs = np.mgrid[0:V1P.shape[0], 0:V1P.shape[1]]
uu = -28.715 + (xs + 0.5) / 100.617553710938; vv = 17.7203 - (ys + 0.5) / 80.3076
gi = np.clip(((uu + 28.715) * 20).astype(int), 0, gu.shape[1] - 1); gj = np.clip(((17.7203 - vv) * 20).astype(int), 0, gu.shape[0] - 1)
v1snow = ground & (gu[gj, gi] == 0)
(c, vc) = best(v1snow, 0, 0, V1P.shape[1], V1P.shape[0])
for j, (src, xy, share, cap) in enumerate([(P, a, va, "pilot coastal snow (chunks 0_2/1_2)"), (P, b, vb, "pilot snow, chunk 2_1"), (V1P, c, vc, "v1 open snow")]):
    x = 10 + j * (PW + 10); y = 56 + PH + 34
    lab(d, (x, y - 16), "%s  px %s, snow %.0f%%" % (cap, list(xy), 100 * share))
    s2.paste(Image.fromarray(src[xy[1]:xy[1] + PH, xy[0]:xy[0] + PW]), (x, y))
s2.save(OUT + "/M2p_ice_snow.jpg", quality=88)
# (3) slopes: the mound flank (the northern rise, DEV-18) at 1:1 from the play-camera stills
s3 = Image.new("RGB", (2 * W + 30, H + 70), BG)
d = ImageDraw.Draw(s3)
lab(d, (12, 12), "M2' -- SLOPES (R-C9-193 look check): the northern rise / mound flank at 1:1 px -- DEV-18 3D heather + snow layer on the terrain")
for j, (pn, box, cap) in enumerate([("pilot_02", (480, 0, 1440, 540), "pilot_02 top: the rise above the mere"), ("pilot_03", (480, 0, 1440, 540), "pilot_03 top: the mound flank by the stream")]):
    x = 10 + j * (W + 10); lab(d, (x, 36), cap)
    s3.paste(Image.open("%s/%s.png" % (ST, pn)).convert("RGB").crop(box), (x, 54))
s3.save(OUT + "/M2p_slopes.jpg", quality=88)
for f in ("M2p_pilot_beside_v1.jpg", "M2p_ice_snow.jpg", "M2p_slopes.jpg"):
    print(f, Image.open(OUT + "/" + f).size)
