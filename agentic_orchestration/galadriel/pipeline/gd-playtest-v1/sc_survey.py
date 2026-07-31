#!/usr/bin/env python3
"""SHADOW-CAL: keyframe census — where is it dark, where are the warm sources.

Input: the 640x360 keyframe JPEGs (one every 250 source frames = 4.1667 s).
Output: survey.json + contact sheets.

Warm-source candidate = bright, strongly orange pixel cluster inside the
gameplay region (HUD rows excluded).  Torches/braziers/campfires read this way;
so do fire VFX and the health globe, which is why the HUD band is cut and why
the sheets get looked at before anything is believed.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

# gameplay region in 640x360 coords (HUD top plate + bottom globes/skillbar cut)
GX0, GX1 = 0, 640
GY0, GY1 = 20, 316


def census(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im, np.float32)
    g = a[GY0:GY1, GX0:GX1]
    L = 0.2126 * g[..., 0] + 0.7152 * g[..., 1] + 0.0722 * g[..., 2]
    warm = (g[..., 0] > 195) & (g[..., 0] - g[..., 2] > 85) & (g[..., 1] < 235)
    lab, n = ndimage.label(warm)
    blobs = []
    if n:
        sizes = ndimage.sum(warm, lab, range(1, n + 1))
        cy, cx = np.array(ndimage.center_of_mass(warm, lab, range(1, n + 1))).T
        for i in range(n):
            if sizes[i] >= 4:
                blobs.append([float(cx[i]) + GX0, float(cy[i]) + GY0,
                              float(sizes[i])])
    return {
        "luma_mean": float(L.mean()),
        "luma_p10": float(np.percentile(L, 10)),
        "luma_p90": float(np.percentile(L, 90)),
        "sat_mean": float((g.max(-1) - g.min(-1)).mean()),
        "warm_px": int(warm.sum()),
        "warm_blobs": blobs[:24],
        "n_warm_blobs": len(blobs),
    }


def sheet(paths, out, cols=12, w=160, labels=None):
    ims = [Image.open(p).convert("RGB").resize((w, int(w * 9 / 16)),
                                               Image.LANCZOS) for p in paths]
    h = ims[0].height
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * w, rows * h), (18, 18, 18))
    d = ImageDraw.Draw(canvas)
    for i, im in enumerate(ims):
        r, c = divmod(i, cols)
        canvas.paste(im, (c * w, r * h))
        if labels:
            d.text((c * w + 3, r * h + 2), labels[i], fill=(255, 240, 0))
    canvas.save(out, quality=80)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sheets", default=None)
    ap.add_argument("--fps", type=float, default=60.0)
    a = ap.parse_args()

    files = sorted(f for f in os.listdir(a.dir) if f.endswith(".jpg"))
    rec = []
    for f in files:
        n = int(f[1:-4])
        r = census(os.path.join(a.dir, f))
        r["frame"] = n
        r["t"] = n / a.fps
        r["file"] = f
        rec.append(r)
    with open(a.out, "w") as fh:
        json.dump(rec, fh)
    print(f"{len(rec)} keyframes -> {a.out}")

    if a.sheets:
        os.makedirs(a.sheets, exist_ok=True)
        per = 120
        for i in range(0, len(files), per):
            chunk = files[i:i + per]
            labs = [f"{rec[i + j]['t']:.0f}s" for j in range(len(chunk))]
            sheet([os.path.join(a.dir, c) for c in chunk],
                  os.path.join(a.sheets, f"sheet{i // per:02d}.jpg"),
                  labels=labs)
        print("sheets ->", a.sheets)
