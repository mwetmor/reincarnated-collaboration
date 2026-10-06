#!/usr/bin/env python3
"""barrow_v2 SW level (R-C9-159, lane BS): the ground painting, joined.

    v2sw_stitch.py   -> barrow_full/godot/data/barrow_v2_sw/painted/{ground.png, lit.png}
                        + paint/v1cam/{ground_preview.jpg, seams.json}

1. EVERY TILE COLOUR-MATCHED TO THE ONE MASTER (R-C9-159 clause 2): a low-frequency transfer -- the tile keeps
   its own detail (tile - blur(tile)) and takes the master's colour and light at that scale (blur(master)), a
   Gaussian of SIGMA px at the tile's density, so two tiles can no longer disagree about the snow's colour.
2. FEATHERED IN THE OVERLAPS: the partition-of-unity ramps of conductor_scripts/guided_stitch.py over every
   256 px overlap (weights summing to exactly 1), now between tiles that already agree at low frequency.
seams.json: per overlap, the mean absolute difference between the two neighbours before and after the transfer.
"""
import json, pathlib, hashlib, shutil
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[1]
PD = ROOT / "paint/v1cam"
A9 = ROOT.parent / "artifacts"
OUT = ROOT.parent / "barrow_full/godot/data/barrow_v2_sw/painted"
OUT.mkdir(parents=True, exist_ok=True)
cfg = json.load(open(PD / "cfg_v2sw.json"))
P, COLS, ROWS = cfg["prefix"], cfg["cols"], cfg["rows"]
G = Image.open(cfg["guide"]).convert("RGB")
GW, GH = G.size
W, H, SX, SY = 1536, 1024, 1280, 768
OV = W - SX
SIGMA = 40.0
MASTER = np.asarray(Image.open(PD / "master.png").convert("RGB").resize((GW, GH), Image.BICUBIC), np.float64)


def src(k):
    for d in (f"{P}-{k}-r3", f"{P}-{k}-r2", f"{P}-{k}-r1", f"{P}-{k}"):
        p = A9 / d / f"{P}-{k}.png"
        if p.exists():
            return p
    return None


def lf(a):
    return np.stack([gaussian_filter(a[..., c], SIGMA, mode="nearest") for c in range(3)], -1)


acc = np.zeros((GH, GW, 3))
wsum = np.zeros((GH, GW))
up = np.linspace(0, 1, OV, endpoint=False) + 0.5 / OV
raw, cor = {}, {}
for r in range(ROWS):
    for c in range(COLS):
        k = f"{c}_{r}"
        y0, x0 = r * SY, c * SX
        m = MASTER[y0:y0 + H, x0:x0 + W]
        p = src(k)
        if p is None:
            im = m.copy()
        else:
            t = Image.open(p).convert("RGB")
            if t.size != (W, H):
                t = t.resize((W, H), Image.LANCZOS)
            t = np.asarray(t, np.float64)
            raw[k] = t
            im = t - lf(t) + lf(m)
            cor[k] = im
        wx, wy = np.ones(W), np.ones(H)
        if c > 0: wx[:OV] *= up
        if c < COLS - 1: wx[W - OV:] *= up[::-1]
        if r > 0: wy[:OV] *= up
        if r < ROWS - 1: wy[H - OV:] *= up[::-1]
        w = np.outer(wy, wx)
        acc[y0:y0 + H, x0:x0 + W] += im * w[..., None]
        wsum[y0:y0 + H, x0:x0 + W] += w
assert abs(wsum.min() - 1) < 1e-9 and abs(wsum.max() - 1) < 1e-9
img = Image.fromarray((acc / wsum[..., None]).clip(0, 255).round().astype(np.uint8))
img.save(OUT / "ground.png", optimize=True)
img.resize((GW // 3, GH // 3), Image.LANCZOS).save(PD / "ground_preview.jpg", quality=86)
shutil.copyfile(ROOT / "section_v1cam/guide2/v2sw_lit.png", OUT / "lit.png")
seams = {}
for k in raw:
    c, r = map(int, k.split("_"))
    for dc, dr in ((1, 0), (0, 1)):
        n = f"{c + dc}_{r + dr}"
        if n not in raw:
            continue
        sl = (np.s_[:, W - OV:], np.s_[:, :OV]) if dc else (np.s_[H - OV:, :], np.s_[:OV, :])
        seams[f"{k}|{n}"] = {"raw": round(float(np.abs(raw[k][sl[0]] - raw[n][sl[1]]).mean()), 2),
                             "matched": round(float(np.abs(cor[k][sl[0]] - cor[n][sl[1]]).mean()), 2)}
json.dump({"painted": sorted(raw), "sigma_px": SIGMA, "overlap_mean_abs_diff_0_255": seams,
           "sha256": hashlib.sha256((OUT / "ground.png").read_bytes()).hexdigest()}, open(PD / "seams.json", "w"), indent=1)
print("ground.png", img.size, "tiles", len(raw), "seams", seams)
