#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): stitch a block of painted chunks (the R-C9-151 chunk test) and lay it beside
its zone map and sketch A, for Matt's look.

    python3 tools/bvp_testblock.py "7_5 8_5 7_6 8_6 7_7 8_7" NAME
-> paint/test/NAME_stitched.png (the block, stitched exactly as the full plate will be: linear ramps across the
   256 px overlaps toward painted neighbours only), NAME_compare.jpg (zone map | painted | sketch A), NAME_seams.jpg
   (the stitched block with the chunk seams marked, so a join can be judged).
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
A9 = os.path.join(os.path.dirname(BV2), "artifacts")
Image.MAX_IMAGE_PIXELS = None
CW, CH, SX, SY = 1536, 1024, 1280, 768; OV = CW - SX


def src(k):
    for d in (f"BVP-{k}-r3", f"BVP-{k}-r2", f"BVP-{k}-r1", f"BVP-{k}"):
        p = os.path.join(A9, d, f"BVP-{k}.png")
        if os.path.exists(p):
            return p


def main():
    keys = sys.argv[1].split(); name = sys.argv[2]
    cr = [tuple(map(int, k.split("_"))) for k in keys]
    c0, c1 = min(c for c, _ in cr), max(c for c, _ in cr); r0, r1 = min(r for _, r in cr), max(r for _, r in cr)
    X0, Y0 = c0 * SX, r0 * SY
    Wb, Hb = (c1 - c0) * SX + CW, (r1 - r0) * SY + CH
    acc = np.zeros((Hb, Wb, 3), np.float32); ws = np.zeros((Hb, Wb), np.float32)
    up = (np.arange(OV) + 0.5) / OV
    have = set(cr)
    for c, r in cr:
        im = np.asarray(Image.open(src(f"{c}_{r}")).convert("RGB"), np.float32)
        wx, wy = np.ones(CW, np.float32), np.ones(CH, np.float32)
        if (c - 1, r) in have: wx[:OV] *= up
        if (c + 1, r) in have: wx[CW - OV:] *= up[::-1]
        if (c, r - 1) in have: wy[:OV] *= up
        if (c, r + 1) in have: wy[CH - OV:] *= up[::-1]
        w = np.outer(wy, wx); x, y = c * SX - X0, r * SY - Y0
        acc[y:y + CH, x:x + CW] += im * w[..., None]; ws[y:y + CH, x:x + CW] += w
    out = (acc / np.maximum(ws, 1e-6)[..., None]).clip(0, 255).astype(np.uint8)
    d = os.path.join(BV2, "paint", "test"); os.makedirs(d, exist_ok=True)
    st = Image.fromarray(out); st.save(os.path.join(d, f"{name}_stitched.png"))
    zm = Image.open(os.path.join(BV2, "paint", "barrow_v2_zonemap.png")).crop((X0, Y0, X0 + Wb, Y0 + Hb)).convert("RGB")
    sk = Image.open(os.path.join(BV2, "sites", "BV3r2-A.png")).convert("RGB")
    h = 1000
    a = zm.resize((round(Wb * h / Hb), h)); b = st.resize((round(Wb * h / Hb), h)); s = sk.resize((round(sk.width * h / sk.height), h))
    cmp_ = Image.new("RGB", (a.width + b.width + s.width + 40, h + 50), (250, 250, 248))
    cmp_.paste(a, (0, 50)); cmp_.paste(b, (a.width + 20, 50)); cmp_.paste(s, (a.width + b.width + 40, 50))
    dr = ImageDraw.Draw(cmp_)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
    except Exception:
        f = ImageFont.load_default()
    dr.text((10, 12), "zone map (placement only)", fill=(0, 0, 0), font=f)
    dr.text((a.width + 30, 12), f"painted chunks {keys[0]}..{keys[-1]}, stitched (true scale: 1 m = 100 px)", fill=(0, 0, 0), font=f)
    dr.text((a.width + b.width + 50, 12), "sketch A (the look of record; whole site, not to scale)", fill=(0, 0, 0), font=f)
    cmp_.save(os.path.join(d, f"{name}_compare.jpg"), quality=88)
    sm = st.copy(); dr2 = ImageDraw.Draw(sm)
    for c, r in cr:
        x, y = c * SX - X0, r * SY - Y0
        for xx in (x + OV // 2,) if (c - 1, r) in have else ():
            dr2.line([(xx, y), (xx, y + CH)], fill=(255, 0, 180), width=3)
        for yy in (y + OV // 2,) if (c, r - 1) in have else ():
            dr2.line([(x, yy), (x + CW, yy)], fill=(255, 0, 180), width=3)
    sm.thumbnail((2000, 2000)); sm.save(os.path.join(d, f"{name}_seams.jpg"), quality=86)
    print(d, st.size)


if __name__ == "__main__":
    main()
