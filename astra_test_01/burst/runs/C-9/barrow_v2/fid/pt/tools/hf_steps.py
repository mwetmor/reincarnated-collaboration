#!/usr/bin/env python3
"""BV2F PT (R-C9-242): the TEXTURE step at every internal join -- the high-frequency amplitude (std of luminance minus its
Gaussian sigma-3 blur) in the 32 px before vs the 32 px after each context boundary (x = 1280c + 256, y = 768r + 256), on
ice/snow pixels (LV's class map), per join: ratio after/before (1.0 = same grain). Control: the same 128 px further in.
    python3 fid/pt/tools/hf_steps.py <painting.png> [out.json]"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = np.asarray(Image.open(sys.argv[1]).convert("L")).astype(np.float64)
H, W = P.shape
CM = json.load(open(FID + "/lv/guide_art/guide_manifest.json"))["class"]
CL = np.asarray(Image.open(FID + "/lv/guide_art/class_art.png"))
CL = (CL[..., 0] if CL.ndim == 3 else CL)[:H, :W]
ok = np.isin(CL, [CM["classes"].index(n) for n in ("snow", "ice", "shore_ice", "tide_ice", "ice_mid", "mound") if n in CM["classes"]])
hf = P - ndimage.gaussian_filter(P, 3)
out = {}
def ratio(a, b, ma, mb):
    if ma.sum() < 500 or mb.sum() < 500:
        return None
    return round(float(b[mb].std() / max(a[ma].std(), 1e-6)), 3)
for r in range(3):
    for c in range(3):
        y0, x0 = r * 768, c * 1280
        if c > 0:
            x = x0 + 256; ys = slice(y0, y0 + 1024)
            out["%d_%d|x%d" % (c, r, x)] = {"join": ratio(hf[ys, x - 32:x], hf[ys, x:x + 32], ok[ys, x - 32:x], ok[ys, x:x + 32]),
                                            "control": ratio(hf[ys, x + 96:x + 128], hf[ys, x + 128:x + 160], ok[ys, x + 96:x + 128], ok[ys, x + 128:x + 160])}
        if r > 0:
            y = y0 + 256; xs = slice(x0, x0 + 1536)
            out["%d_%d|y%d" % (c, r, y)] = {"join": ratio(hf[y - 32:y, xs], hf[y:y + 32, xs], ok[y - 32:y, xs], ok[y:y + 32, xs]),
                                            "control": ratio(hf[y + 96:y + 128, xs], hf[y + 128:y + 160, xs], ok[y + 96:y + 128, xs], ok[y + 128:y + 160, xs])}
for k, v in out.items():
    print(k, v)
if len(sys.argv) > 2:
    json.dump({"_what": __doc__.strip().splitlines()[0], "painting": sys.argv[1], "hf_ratio": out}, open(sys.argv[2], "w"), indent=1)
