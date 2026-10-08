#!/usr/bin/env python3
"""BV2F PT (R-C9-241): the TONE STEP at every internal join of a stitched pilot painting -- where each chunk's pasted
context (its LEFT 256 columns / TOP 256 rows) meets the paint it made new: vertical joins at x = 1280c + 256 (c >= 1),
horizontal at y = 768r + 256 (r >= 1), inside each chunk's span. Measured on the LOW-FREQUENCY field (Gaussian sigma 6 px)
as the Lab difference (dE76) between the mean of the band 8-16 px before the join and 8-16 px after it, per 64-px segment,
on ice/snow pixels only (LV's guide class map: snow, ice, shore_ice, tide_ice, ice_mid, mound); and, as the control, the
same measure 128 px further into the chunk (no join there). Writes <out>/join_steps.json + <out>/joins/<join>.jpg crops.
    python3 fid/pt/tools/join_steps.py <painting.png> <out dir> [--cfg cfg.json]"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAINT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(OUT, "joins"), exist_ok=True)
P8 = np.asarray(Image.open(PAINT).convert("RGB"))
H, W = P8.shape[:2]
CM = json.load(open(FID + "/lv/guide_art/guide_manifest.json"))["class"]
CL = np.asarray(Image.open(FID + "/lv/guide_art/class_art.png"))
CL = (CL[..., 0] if CL.ndim == 3 else CL)[:H, :W]
names = CM["classes"]
ok = np.isin(CL, [names.index(n) for n in ("snow", "ice", "shore_ice", "tide_ice", "ice_mid", "mound") if n in names])


def lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


LB = lab(P8.astype(np.float64) / 255.0)
LF = np.stack([ndimage.gaussian_filter(LB[..., i], 6) for i in range(3)], -1)


def step(axis, pos, a0, a1):
    """per 64-px segment along the join: dE between the bands [pos-16, pos-8) and [pos+8, pos+16)."""
    segs = []
    for s in range(a0, a1, 64):
        e = min(s + 64, a1)
        if axis == "x":
            A, B = LF[s:e, pos - 16:pos - 8], LF[s:e, pos + 8:pos + 16]
            mk = ok[s:e, pos - 16:pos - 8] & ok[s:e, pos + 8:pos + 16]
        else:
            A, B = LF[pos - 16:pos - 8, s:e], LF[pos + 8:pos + 16, s:e]
            mk = ok[pos - 16:pos - 8, s:e] & ok[pos + 8:pos + 16, s:e]
        if mk.mean() < 0.6:
            continue
        d = np.linalg.norm(A[mk].mean(0) - B[mk].mean(0))
        dl = float(B[mk].mean(0)[0] - A[mk].mean(0)[0])
        segs.append({"at": [s, e], "dE": round(float(d), 2), "dL": round(dl, 2)})
    return segs


cfg = json.load(open(sys.argv[sys.argv.index("--cfg") + 1])) if "--cfg" in sys.argv else {"cols": 3, "rows": 3}
C, R = cfg["cols"], cfg["rows"]
res = {}
for r in range(R):
    for c in range(C):
        y0, y1 = r * 768, r * 768 + 1024
        x0, x1 = c * 1280, c * 1280 + 1536
        if c > 0:
            k = "%d_%d|x%d" % (c, r, x0 + 256)
            res[k] = {"join": step("x", x0 + 256, y0, y1), "control": step("x", x0 + 384, y0, y1)}
            cx = x0 + 256
            Image.fromarray(P8[y0:y1, cx - 160:cx + 160]).save(os.path.join(OUT, "joins", "%d_%d_x.jpg" % (c, r)), quality=88)
        if r > 0:
            k = "%d_%d|y%d" % (c, r, y0 + 256)
            res[k] = {"join": step("y", y0 + 256, x0, x1), "control": step("y", y0 + 384, x0, x1)}
            cy = y0 + 256
            Image.fromarray(P8[cy - 160:cy + 160, x0:x1]).save(os.path.join(OUT, "joins", "%d_%d_y.jpg" % (c, r)), quality=88)
summ = {}
for k, v in res.items():
    j = [s["dE"] for s in v["join"]]
    q = [s["dE"] for s in v["control"]]
    summ[k] = {"join_dE_max": max(j) if j else None, "join_dE_median": float(np.median(j)) if j else None,
               "control_dE_max": max(q) if q else None, "control_dE_median": float(np.median(q)) if q else None, "segments": len(j)}
json.dump({"_what": __doc__.strip().splitlines()[0], "painting": PAINT, "summary": summ, "detail": res},
          open(os.path.join(OUT, "join_steps.json"), "w"), indent=1)
for k, v in summ.items():
    print(k, v)
