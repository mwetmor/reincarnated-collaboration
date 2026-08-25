#!/usr/bin/env python3
"""
stage_adequacy.py — galadriel — 2026-08-24

Derives the two stage-adequacy quantities named in
`galadriel/notes/2026-08-24-s2-minted-gate-procedure.md` § 1.9, on ONE instrument,
so the s2a bare stage and any candidate stage are measured the same way.

Quantities
----------
  structured_frac : fraction of frame where Sobel gradient magnitude on Rec.709
                    luma exceeds THR_GRAD (default 10). Its complement is the
                    "near-uniform floor" figure. This is the SCREEN.

  hlf_pct         : register-2 High-Luminance Fraction, luma/255 > 0.80, i.e. the
                    same definition as `pipeline/register-metrics.mjs` used for the
                    14.4 % graybox / 9.35 % cathedral anchors.

  hlf_off         : hlf_pct measured on a VFX-FREE frame of the same stage. This is
                    the quantity that decides whether HLF is a statement about the
                    EFFECT or a statement about the STAGE.

  structured_locality : share of structured pixels falling inside the largest
                    connected structured island, and that island's bbox. A stage can
                    clear the global screen while parking all its geometry in one
                    corner far from the effect; s2a is the exhibit (190x200 island).

Normalisation
-------------
Reported at NATIVE resolution and at 960w inside-fit. The register-2 anchors were
computed at 960w inside-fit; the s2 harness renders 1920x1080. A gradient threshold
is not resolution-invariant, so both are reported and neither is hidden.

Usage:  python3 stage_adequacy.py <png> [<png> ...]
"""

import sys
import json
import numpy as np
from PIL import Image

THR_GRAD = 10.0
THR_HLF = 0.80  # luma fraction, per register-metrics.mjs


def luma(img: Image.Image) -> np.ndarray:
    a = np.asarray(img.convert("RGB"), dtype=np.float64)
    return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]


def sobel_mag(y: np.ndarray) -> np.ndarray:
    kx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=np.float64)
    ky = kx.T
    # explicit 3x3 correlation, no scipy dependency
    p = np.pad(y, 1, mode="edge")
    gx = np.zeros_like(y)
    gy = np.zeros_like(y)
    for i in range(3):
        for j in range(3):
            w = p[i:i + y.shape[0], j:j + y.shape[1]]
            gx += kx[i, j] * w
            gy += ky[i, j] * w
    return np.hypot(gx, gy)


def largest_island(mask: np.ndarray):
    """Flood-fill 4-connectivity, iterative. Returns (px, bbox t,b,l,r)."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    best = (0, None)
    ys, xs = np.nonzero(mask)
    for sy, sx in zip(ys, xs):
        if seen[sy, sx]:
            continue
        stack = [(sy, sx)]
        seen[sy, sx] = True
        cells = []
        while stack:
            cy, cx = stack.pop()
            cells.append((cy, cx))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if len(cells) > best[0]:
            arr = np.array(cells)
            best = (len(cells), (int(arr[:, 0].min()), int(arr[:, 0].max()),
                                 int(arr[:, 1].min()), int(arr[:, 1].max())))
    return best


def measure(path: str, fit960: bool, do_island: bool) -> dict:
    img = Image.open(path)
    native = img.size
    if fit960 and img.size[0] != 960:
        h = round(img.size[1] * 960 / img.size[0])
        img = img.resize((960, h), Image.LANCZOS)
    y = luma(img)
    n = y.size
    g = sobel_mag(y)
    smask = g > THR_GRAD
    spx = int(smask.sum())
    out = {
        "file": path.rsplit("/", 1)[-1],
        "native": f"{native[0]}x{native[1]}",
        "measured_at": f"{img.size[0]}x{img.size[1]}",
        "structured_px": spx,
        "structured_frac_pct": round(100.0 * spx / n, 4),
        "near_uniform_floor_pct": round(100.0 * (1 - spx / n), 4),
        "hlf_pct": round(100.0 * float((y / 255.0 > THR_HLF).sum()) / n, 4),
        "luma_p25_p75_spread": round(float(np.percentile(y, 75) - np.percentile(y, 25)), 4),
    }
    if do_island and 0 < spx <= 400000:
        px, bbox = largest_island(smask)
        out["largest_island_px"] = px
        out["largest_island_share_pct"] = round(100.0 * px / spx, 2)
        if bbox:
            t, b, l, r = bbox
            out["largest_island_bbox"] = f"y{t}-{b} x{l}-{r} ({r - l + 1}x{b - t + 1})"
    return out


if __name__ == "__main__":
    res = []
    for p in sys.argv[1:]:
        for fit in (False, True):
            res.append(measure(p, fit960=fit, do_island=not fit))
    print(json.dumps(res, indent=2))
