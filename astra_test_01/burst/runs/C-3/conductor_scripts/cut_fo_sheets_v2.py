"""Conductor glue (style card v0 §1): cut a 6×4 greyscale effect sheet into painted-pixel phase frames —
per-cell haze removal, downsample to the native effect size (area), posterise to 4 value bands, alpha from the
posterised body, nearest-upscale preview. usage: cut_fo_sheets.py SHEET.png OUT_DIR [native_px=64]"""
import sys, json, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage
sheet = np.array(Image.open(sys.argv[1]).convert('L')).astype(np.float32); OUT = pathlib.Path(sys.argv[2]); N = int(sys.argv[3]) if len(sys.argv) > 3 else 64
OUT.mkdir(parents=True, exist_ok=True)
H, W = sheet.shape; cw, ch = W // 6, H // 4
ROWS = ['cast', 'travel', 'impact', 'residual']; LEVELS = [0.0, 0.18, 0.42, 0.68, 1.0]   # transparent, dark, mid, light, white
rec = {}
for r, phase in enumerate(ROWS):
    for c in range(6):
        cell = sheet[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw]
        haze = ndimage.gaussian_filter(ndimage.grey_opening(cell, size=(131, 131)), 12)   # radial glow haze (window larger than any drawing)
        body = np.clip(cell - haze, 0, 255); body[:18] = body[-18:] = 0; body[:, :18] = body[:, -18:] = 0   # cell-border bleed
        top = max(np.percentile(body, 99.5), 1.0); body = np.clip(body / top, 0, 1)
        small = np.array(Image.fromarray((body * 255).astype(np.uint8)).resize((N, N), Image.BOX)).astype(np.float32) / 255.0
        lvl = np.zeros_like(small); a = np.zeros_like(small)
        TH = [float(x) for x in (sys.argv[4] if len(sys.argv) > 4 else '0.72,0.5,0.33,0.21').split(',')]
        for lo, v in zip(TH, (1.0, 0.68, 0.42, 0.18)):
            sel = (small >= lo) & (lvl == 0); lvl[sel] = v; a[sel] = 1.0
        lvl = np.where(a > 0, lvl, 0)
        # drop stray single pixels; keep the largest body + any group ≥ 3 px
        lab, n = ndimage.label(a > 0); sizes = ndimage.sum(a > 0, lab, range(1, n + 1))
        keep = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz >= 3]); a = a * keep; lvl = lvl * keep
        grey = (lvl * 255).astype(np.uint8); alpha = (a * 255).astype(np.uint8)
        img = np.dstack([grey, grey, grey, alpha]); name = f'{phase}_{c:02d}.png'
        Image.fromarray(img, 'RGBA').save(OUT / name)
        rec[name] = {'opaque_px': int((a > 0).sum()), 'white_frac': round(float(((lvl >= 0.99) & (a > 0)).sum() / max(1, (a > 0).sum())), 3), 'bands': int(len(set(np.unique(lvl[a > 0]).tolist())))}
json.dump(rec, open(OUT / 'frames.json', 'w'), indent=1)
# preview: nearest ×4, on dark grey, 6×4
prev = Image.new('RGB', (6 * N * 4, 4 * N * 4), (40, 42, 50))
for r, phase in enumerate(ROWS):
    for c in range(6):
        im = Image.open(OUT / f'{phase}_{c:02d}.png').resize((N * 4, N * 4), Image.NEAREST); prev.paste(im, (c * N * 4, r * N * 4), im)
prev.save(OUT / 'preview_x4.png'); print(json.dumps({k: v for k, v in list(rec.items())[:4]}))
