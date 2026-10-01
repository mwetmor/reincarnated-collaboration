#!/usr/bin/env python3
"""C-9 MIX v2 -- B'S DARKENED ROCK AGAINST A'S PAINTED HEAD, the same fall frames, the play camera. drax.

  python3 tools/rock_match.py --a work/mix2/ref_a --b work/mix2/rock4 [--json OUT]

Both directories come from godot/tools/probe_rock_match.gd (A: -- --meteor mix1, B: the default MIX v2),
on the phone page's look (--as-web, Compatibility). Frames are paired by the fall's own clock t.

Per frame, per lane:
  NUCLEUS  -- the dark rock: the largest connected blob of near-black pixels (L* < 22, its seams closed
              over, 3 px, then opened 4 px so the ink outlines drop off) near the head
              (A's rock_at node is A's anchor, not where its head is drawn, so the blob is found in the
              image, not projected). Its area (px), and the fraction of the blob ring that is glowing seam.
  HEAD     -- every effect pixel (chroma > 28 or L* < 30: the snow, its warm fall light and the shadow are
              low-chroma and light) in a disc of R_HEAD px round the nucleus centre: the fractions in the
              value bands dark (L* < 30) / mid / bright (L* > 80), and the mean L*.
The comparison is the per-band difference of the means over the paired frames, and the nucleus area ratio.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

R_HEAD = 130          # px at 1920 x 1080: A's head (nucleus + its wrapping fire) fits inside
DARK_L, BRIGHT_L = 30.0, 80.0
NUC_L = 22.0


def lab(img):
    a = np.asarray(img.convert("RGB"), dtype=np.float64) / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = lin @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16
    A = 500 * (f[..., 0] - f[..., 1])
    B = 200 * (f[..., 1] - f[..., 2])
    return L, np.hypot(A, B)


def measure(path, guess, search):
    L, C = lab(Image.open(path))
    h, w = L.shape
    yy, xx = np.mgrid[0:h, 0:w]
    near = (xx - guess[0]) ** 2 + (yy - guess[1]) ** 2 < search ** 2
    dark = (L < NUC_L) & near
    # the glowing seams cut the nucleus into facets: close them over before taking the blob
    # and the ink outlines (a few px wide) opened away, so the flame's outline does not join the nucleus
    dark = ndimage.binary_opening(ndimage.binary_closing(dark, iterations=3), iterations=4) & near
    lbl, n = ndimage.label(dark)
    if n == 0:
        return None
    sizes = ndimage.sum(dark, lbl, range(1, n + 1))
    k = int(np.argmax(sizes)) + 1
    blob = lbl == k
    if blob.sum() < 40:
        return None
    cy, cx = ndimage.center_of_mass(blob)
    # the seams: warm bright pixels inside the blob's filled hull (the cracks cut the dark blob apart)
    filled = ndimage.binary_closing(blob, iterations=4)
    filled = ndimage.binary_fill_holes(filled)
    seam = filled & ~blob & (L > 45) & (C > 40)
    disc = (xx - cx) ** 2 + (yy - cy) ** 2 < R_HEAD ** 2
    fx = disc & ((C > 28) | (L < 30))
    Lf = L[fx]
    if Lf.size == 0:
        return None
    return {"nucleus_px": int(blob.sum()), "nucleus_hull_px": int(filled.sum()),
            "seam_frac": round(float(seam.sum()) / max(1, int(filled.sum())), 4),
            "centre": [round(cx, 1), round(cy, 1)], "effect_px": int(fx.sum()),
            "dark": float((Lf < DARK_L).mean()), "bright": float((Lf > BRIGHT_L).mean()),
            "mid": float(((Lf >= DARK_L) & (Lf <= BRIGHT_L)).mean()), "mean_L": float(Lf.mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--json")
    ap.add_argument("--search", type=float, default=260.0)
    o = ap.parse_args()
    A = json.load(open(os.path.join(o.a, "rock_frames.json")))
    B = json.load(open(os.path.join(o.b, "rock_frames.json")))
    at = {round(f["t"], 3): f for f in A["frames"]}
    rows = []
    for fb in B["frames"]:
        fa = at.get(round(fb["t"], 3))
        if fa is None:
            continue
        mb = measure(os.path.join(o.b, fb["file"]), fb["rock_px"], o.search)
        ma = measure(os.path.join(o.a, fa["file"]), fa["rock_px"], o.search)
        if ma is None or mb is None:
            continue
        rows.append({"t": round(fb["t"], 3), "a": ma, "b": mb})
    keys = ["dark", "mid", "bright", "mean_L", "nucleus_px", "seam_frac"]
    mean = {lane: {k: round(float(np.mean([r[lane][k] for r in rows])), 4) for k in keys} for lane in ("a", "b")}
    delta = {k: round(mean["b"][k] - mean["a"][k], 4) for k in ("dark", "mid", "bright", "mean_L", "seam_frac")}
    out = {"what": "C-9 MIX v2: B's darkened rock + corona against A's painted head, same fall frames (paired by t), "
                   "play camera, phone page look", "a_dir": o.a, "b_dir": o.b, "a_mode": A["mode"], "b_mode": B["mode"],
           "paired_frames": len(rows), "r_head_px": R_HEAD,
           "bands": {"dark": "L* < %g" % DARK_L, "bright": "L* > %g" % BRIGHT_L, "nucleus": "L* < %g blob" % NUC_L},
           "mean": mean, "delta_b_minus_a": delta,
           "nucleus_area_ratio_b_over_a": round(mean["b"]["nucleus_px"] / max(1e-6, mean["a"]["nucleus_px"]), 3),
           "rows": rows}
    print(json.dumps({k: out[k] for k in ("paired_frames", "mean", "delta_b_minus_a", "nucleus_area_ratio_b_over_a")}, indent=1))
    if o.json:
        json.dump(out, open(o.json, "w"), indent=1)


if __name__ == "__main__":
    main()
