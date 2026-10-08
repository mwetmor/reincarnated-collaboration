#!/usr/bin/env python3
"""BV2F PT (R-C9-250) DEV-27 constructed test, 0 images: a real chunk (BV2F-PS3A-2_0) with a SYNTHETIC +8 L* step added to
its whole NEW paint (x >= 256) -> DEV-27's block (exec'd from the shipped Tier-B stitch, nothing copied) -> (1) the step at
x = 256 (low-pass Lab dE on ground pixels, 8-16 px each side) before/after; (2) a REAL painted edge crossing the boundary
(the shoreline: ice vs snow, the largest-contrast ground edge within x 256..400) must keep its contrast; (3) object pixels
(warm/dark) are moved only by the smooth field. Writes fid/pt/dev27/test.json + crops."""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ST = FID + "/v1tools/tierB/conductor_scripts/guided_stitch.py"
src = open(ST).read()
blk = src[src.index("# BV2F-BEGIN DEV-27"):src.index("# BV2F-BEGIN DEV-26")]
g = {"np": np, "ndimage": ndimage, "os": os, "W": 1536, "H": 1024, "OV": 256}
exec(blk, g)
A9 = os.path.abspath(FID + "/../../artifacts")
im = np.asarray(Image.open(A9 + "/BV2F-PS3A-2_0/BV2F-PS3A-2_0.png").convert("RGB")).astype(np.float64)


def lab(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def unlab(L):
    fy = (L[..., 0] + 16) / 116; fx = fy + L[..., 1] / 500; fz = fy - L[..., 2] / 200
    e = 6 / 29
    f = lambda t: np.where(t > e, t ** 3, 3 * e * e * (t - 4 / 29))
    xyz = np.stack([f(fx) * 0.95047, f(fy), f(fz) * 1.08883], -1)
    m = np.linalg.inv(np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]]))
    c = xyz @ m.T
    c = np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055)
    return np.clip(c * 255.0, 0, 255)


Lb = lab(im)
syn = Lb.copy(); syn[:, 256:, 0] += 8.0
syn_rgb = unlab(syn)
fixed = g["_bv2f_poisson"](syn_rgb.copy(), 1, 0)
gm = g["_dev27_ground"](im) > 0


def step(a):
    LF = ndimage.gaussian_filter(lab(a), (6, 6, 0))
    m = gm[:, 240:248] & gm[:, 264:272]
    rows = m.mean(1) > 0.6
    d = np.linalg.norm(LF[rows, 240:248].mean(1) - LF[rows, 264:272].mean(1), axis=-1)
    return round(float(np.median(d)), 2), round(float(np.percentile(d, 90)), 2)


# the real edge: the strongest ground-luminance edge in x 300..420 (a shoreline crossing toward the boundary)
L0 = lab(im)[..., 0]
gy = np.abs(ndimage.sobel(ndimage.gaussian_filter(L0, 2), 0)) + np.abs(ndimage.sobel(ndimage.gaussian_filter(L0, 2), 1))
win = gy[:, 300:420] * gm[:, 300:420]
yy, xx = np.unravel_index(np.argmax(ndimage.uniform_filter(win, 15)), win.shape)
xx += 300
def contrast(a):
    G = lab(a)[..., 0]
    g2 = np.abs(ndimage.sobel(ndimage.gaussian_filter(G, 2), 0)) + np.abs(ndimage.sobel(ndimage.gaussian_filter(G, 2), 1))
    return round(float(g2[yy - 10:yy + 10, xx - 10:xx + 10].mean()), 2)
obj = ~gm
fld = fixed - syn_rgb
hf_obj = fld - np.stack([ndimage.gaussian_filter(fld[..., i], 6) for i in range(3)], -1)
res = {"synthetic_step_L": 8.0,
       "step_dE_median_p90": {"original": step(im), "with_synthetic_+8": step(syn_rgb), "after_DEV27": step(fixed)},
       "real_edge_at": [int(xx), int(yy)],
       "real_edge_contrast": {"original": contrast(im), "with_synthetic_+8": contrast(syn_rgb), "after_DEV27": contrast(fixed)},
       "field_high_frequency_on_objects_max_abs": round(float(np.abs(hf_obj[:, 256:][obj[:, 256:]]).max()), 3),
       "report": g["DEV27_REP"]}
os.makedirs(FID + "/pt/dev27", exist_ok=True)
json.dump(res, open(FID + "/pt/dev27/test.json", "w"), indent=1)
for nm, a in (("original", im), ("synthetic", syn_rgb), ("after", fixed)):
    Image.fromarray(a[:, 96:608].astype(np.uint8)).resize((256, 512)).save(FID + "/pt/dev27/test_%s.jpg" % nm, quality=88)
print(json.dumps(res))
