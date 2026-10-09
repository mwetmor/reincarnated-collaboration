#!/usr/bin/env python3
"""P9c v3 -- RE-INSTRUMENTED per R-C9-336 (s56; the s55 discriminator read INSTRUMENT). No bar change (<= 0.25 px).
Inputs (ph_life.gd life ... --floe-null <mode> --floe-ids --floe-solo --floe-pairs 5): floe_m0/m1[_k].png (the marker:
R = 0.95 silhouette, G = noise texture, B = 0.5), floe_id0/id1[_k].png (each bobbing floe a flat unshaded palette colour
at the SAME pose), hide_floe.png (everything but the floes hidden too: --floe-solo, extending s31 A1, so no static
neighbour can occlude a bobbing silhouette).
Per floe j and pair k:
  labels   L_t = nearest palette entry (L1 distance <= 6) where the ID shot differs from hide_floe by > 30
  others   O = dilate((L0 > 0 & L0 != j) | (L1 > 0 & L1 != j), 6)            -- touching floes never mix into j
  alpha    a_t = clip((Rb_t - Rb_hide) / (median Rb on j's interior - Rb_hide), 0, 1), Rb = R - B; a_t[O] = 0
  sil      LK(G_1.5 a0, G_1.5 a1) weighted on dilate(boundary(L0 == j), 5) & ~O
  tex      LK(G_1.0 G0, G_1.0 G1) weighted on G_2(erode((L0 == j) & (L1 == j), 6) & ~O)
  drift    |sil - tex|, motion |sil|; floes whose box (+16 px) leaves the screen are skipped; >= 1500 px
Statistic (unchanged): median drift over samples with motion >= 0.25 px.
  site_p9c_v3.py <render_dir> [label] -> prints / returns the reading"""
import math
import os
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa
from pilot_harness import _lk_shift  # noqa

PAL = np.array([[(j % 6) * 51, ((j // 6) % 6) * 51, ((j // 36) % 2) * 255] for j in range(1, 73)], np.float32)


def labels(idimg, hf):
    d = np.abs(idimg[..., None, :] - PAL[None, None]).sum(-1)
    j = d.argmin(-1) + 1
    ok = (d.min(-1) <= 6) & (np.abs(idimg - hf).sum(-1) > 30)
    return np.where(ok, j, 0)


def pair(dirp, sfx, min_px=1500, pad=16):
    m0, m1 = load_rgb(dirp / ("floe_m0%s.png" % sfx)), load_rgb(dirp / ("floe_m1%s.png" % sfx))
    hf = load_rgb(dirp / "hide_floe.png")
    L0, L1 = labels(load_rgb(dirp / ("floe_id0%s.png" % sfx)), hf), labels(load_rgb(dirp / ("floe_id1%s.png" % sfx)), hf)
    Hh, Ww = L0.shape
    out = []
    for j in np.unique(L0[L0 > 0]):
        f0 = L0 == j
        if f0.sum() < min_px:
            continue
        ys, xs = np.nonzero(f0 | (L1 == j))
        y0, y1, x0, x1 = ys.min() - pad, ys.max() + pad + 1, xs.min() - pad, xs.max() + pad + 1
        if y0 < 0 or x0 < 0 or y1 > Hh or x1 > Ww:
            continue
        sl = (slice(y0, y1), slice(x0, x1))
        p0, p1 = f0[sl], (L1 == j)[sl]
        O = ndimage.binary_dilation(((L0[sl] > 0) & (L0[sl] != j)) | ((L1[sl] > 0) & (L1[sl] != j)), iterations=6)
        Rb0 = m0[sl][..., 0] - m0[sl][..., 2]
        Rb1 = m1[sl][..., 0] - m1[sl][..., 2]
        Rbh = hf[sl][..., 0] - hf[sl][..., 2]
        inner = ndimage.binary_erosion(p0, iterations=4)
        if inner.sum() < 500:
            continue
        den = np.maximum(float(np.median(Rb0[inner])) - Rbh, 10.0)
        a0, a1 = np.clip((Rb0 - Rbh) / den, 0, 1), np.clip((Rb1 - Rbh) / den, 0, 1)
        a0[O], a1[O] = 0.0, 0.0
        edge = ndimage.binary_dilation(p0 ^ ndimage.binary_erosion(p0), iterations=5) & ~O
        if edge.sum() < 200:
            continue
        sil = _lk_shift(ndimage.gaussian_filter(a0, 1.5), ndimage.gaussian_filter(a1, 1.5), edge.astype(float))
        core = ndimage.binary_erosion(p0 & p1, iterations=6) & ~O
        if core.sum() < 500:
            continue
        t = _lk_shift(ndimage.gaussian_filter(m0[sl][..., 1], 1.0), ndimage.gaussian_filter(m1[sl][..., 1], 1.0),
                      ndimage.gaussian_filter(core.astype(float), 2))
        out.append({"floe": int(j), "px": int(p0.sum()), "edge_px": int(edge.sum()), "edge_excluded_near_other_px": int((ndimage.binary_dilation(p0 ^ ndimage.binary_erosion(p0), iterations=5) & O).sum()),
                    "silhouette_shift": [round(sil[0], 3), round(sil[1], 3)], "texture_shift": [round(t[0], 3), round(t[1], 3)],
                    "drift": round(math.hypot(sil[0] - t[0], sil[1] - t[1]), 3), "motion": round(math.hypot(*sil), 3)})
    return out


def read(dirp, n_pairs=5, min_motion=0.25):
    dirp = pathlib.Path(dirp)
    rows = []
    for k in range(n_pairs):
        for r in pair(dirp, "" if k == 0 else "_%d" % k):
            rows.append(dict(r, pair=k))
    s = [r["drift"] for r in rows if r["motion"] >= min_motion]
    return {"dir": str(dirp.relative_to(FID)) if str(dirp).startswith(str(FID)) else str(dirp), "floes": len({r["floe"] for r in rows}),
            "rows": rows, "samples_counted": len(s), "median_drift_px": round(float(np.median(s)), 3) if s else None,
            "p90_drift_px": round(float(np.percentile(s, 90)), 3) if s else None,
            "max_abs_r_px": round(float(max([r["drift"] for r in rows] or [0])), 3)}


if __name__ == "__main__":
    r = read(sys.argv[1])
    print({k: v for k, v in r.items() if k != "rows"})
