#!/usr/bin/env python3
"""barrow_v2 SECTION SW (R-C9-158, lane BS): stitching.

    section_sw_stitch.py guide <tiles_dir>        -> paint/section_sw/section_sw_guide.png (+ _preview.jpg)
    section_sw_stitch.py paint                    -> paint/section_sw/section_sw_painted.png (+ _preview.jpg, seams.json)

paint = conductor_scripts/guided_stitch.py's partition-of-unity blend (linear ramps over every 256 px overlap, the
weights summing to exactly 1), extended by one thing: a SKIPPED chunk (cfg skip: outside every still and the film's
camera) contributes the GUIDE's own pixels, so the painting is complete as a texture. seams.json measures each
overlap: the mean absolute difference between the two painted neighbours over their shared strip (a seam check).
"""
import json, sys, pathlib, hashlib
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[1]
PD = ROOT / "paint/section_sw"
A9 = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts')
TW, TH = 1984, 1216

if sys.argv[1] == "guide":
    td = pathlib.Path(sys.argv[2])
    tiles = sorted(td.glob("tile_*_*.png"))
    nx = 1 + max(int(p.stem.split("_")[1]) for p in tiles)
    ny = 1 + max(int(p.stem.split("_")[2]) for p in tiles)
    out = Image.new("RGB", (nx * TW, ny * TH))
    for p in tiles:
        i, j = int(p.stem.split("_")[1]), int(p.stem.split("_")[2])
        im = Image.open(p).convert("RGB")
        assert im.size == (TW, TH), (p, im.size)
        out.paste(im, (i * TW, j * TH))
    dst = PD / "section_sw_guide.png"
    out.save(dst, optimize=True)
    out.resize((out.width // 4, out.height // 4), Image.LANCZOS).save(PD / "section_sw_guide_preview.jpg", quality=86)
    print(dst.name, out.size, "sha256", hashlib.sha256(dst.read_bytes()).hexdigest())
    sys.exit()

cfg = json.load(open(PD / "cfg_section_sw.json"))
P, COLS, ROWS, SKIP = cfg["prefix"], cfg["cols"], cfg["rows"], set(cfg["skip"])
GUIDE = np.asarray(Image.open(cfg["guide"]).convert("RGB"), dtype=np.float64)
W, H, SX, SY = 1536, 1024, 1280, 768
OV = W - SX


def src(k):
    for d in (f'{P}-{k}-r3', f'{P}-{k}-r2', f'{P}-{k}-r1', f'{P}-{k}'):
        p = A9 / d / f'{P}-{k}.png'
        if p.exists():
            return p
    return None


acc = np.zeros(((ROWS - 1) * SY + H, (COLS - 1) * SX + W, 3))
wsum = np.zeros(acc.shape[:2])
up = np.linspace(0, 1, OV, endpoint=False) + 0.5 / OV
ims = {}
for r in range(ROWS):
    for c in range(COLS):
        k = f"{c}_{r}"
        if k in SKIP or src(k) is None:
            im = GUIDE[r * SY:r * SY + H, c * SX:c * SX + W]
        else:
            pim = Image.open(src(k)).convert("RGB")
            if pim.size != (W, H):
                pim = pim.resize((W, H), Image.LANCZOS)
            im = np.asarray(pim, dtype=np.float64)
            ims[k] = im
        wx, wy = np.ones(W), np.ones(H)
        if c > 0: wx[:OV] *= up
        if c < COLS - 1: wx[W - OV:] *= up[::-1]
        if r > 0: wy[:OV] *= up
        if r < ROWS - 1: wy[H - OV:] *= up[::-1]
        w = np.outer(wy, wx)
        acc[r * SY:r * SY + H, c * SX:c * SX + W] += im * w[..., None]
        wsum[r * SY:r * SY + H, c * SX:c * SX + W] += w
assert abs(wsum.min() - 1) < 1e-9 and abs(wsum.max() - 1) < 1e-9
out = Image.fromarray((acc / wsum[..., None]).clip(0, 255).round().astype(np.uint8))
dst = PD / "section_sw_painted.png"
out.save(dst, optimize=True)
out.resize((out.width // 4, out.height // 4), Image.LANCZOS).save(PD / "section_sw_painted_preview.jpg", quality=86)
seams = {}
for k, im in ims.items():
    c, r = map(int, k.split("_"))
    for dc, dr in ((1, 0), (0, 1)):
        n = f"{c + dc}_{r + dr}"
        if n not in ims:
            continue
        o = ims[n]
        if dc:
            a, b = im[:, W - OV:], o[:, :OV]
        else:
            a, b = im[H - OV:, :], o[:OV, :]
        seams[f"{k}|{n}"] = round(float(np.abs(a - b).mean()), 2)
painted = sorted(ims)
json.dump({"painted": painted, "skipped_or_missing_use_guide": sorted(set(f"{c}_{r}" for r in range(ROWS) for c in range(COLS)) - set(painted)),
           "overlap_mean_abs_diff_0_255": seams, "sha256": hashlib.sha256(dst.read_bytes()).hexdigest()},
          open(PD / "seams.json", "w"), indent=1)
print(dst.name, out.size, "painted", len(painted), "seams max", max(seams.values()) if seams else None)
