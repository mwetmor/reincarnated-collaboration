#!/usr/bin/env python3
"""C-9 T4 close-out: what does a drift number of N actually MEAN?

    python3 sensitivity.py            # writes sensitivity.json

fallback_check.py answers "is this the same instrument as 21_drift.py".  This
answers the question a reader of the table will ask next: a helm drift of 2.4
is worse than one of 1.3, but is either of them something a player would see?

A KNOWN PERTURBATION, ON A SEQUENCE THAT HAS NO DRIFT.  The drive is one unlit
texture on one rigged mesh, so every frame is the same helm.  Its helm is then
deliberately broken by a known amount, per frame, independently:

  scale    the helm is resized about its own centre by a random +-m percent --
           a helm that swells and shrinks between frames, which is the shape of
           Matt's complaint
  rotate   the helm is turned about its own centre by a random +-m degrees --
           a visor that swings
  tone     the helm's luma is shifted by a random +-m of 255 -- a helm that is
           relit or re-shaded between frames

and the same frame-to-frame measurement is run over the result.  The output is
a conversion table: this much visible change reads as this much drift.

WHY RANDOM AND PER FRAME: a smooth perturbation would be absorbed as animation
by anything, and the failure being modelled is incoherence between adjacent
frames, not a slow trend.
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t4lib as L
import measure as M

HERE = os.path.dirname(os.path.abspath(__file__))
N = 60                     # drive frames; enough for a stable median, cheap
LAG = 3                    # the drive's own one-twelfth-of-a-stride lag (34/12)


def warp(rgb, m, scale=1.0, rot=0.0, tone=0.0):
    h, w = m.shape
    c = (np.array([h, w]) - 1) / 2.0
    th = np.deg2rad(rot)
    R = np.array([[np.cos(th), -np.sin(th)],
                  [np.sin(th), np.cos(th)]])
    A = R / scale
    off = c - A @ c
    out = np.stack([ndi.affine_transform(rgb[..., k], A, offset=off, order=1,
                                         mode="nearest") for k in range(3)], -1)
    mm = ndi.affine_transform(m.astype(np.float64), A, offset=off, order=1,
                              mode="constant", cval=0.0) > 0.5
    return np.clip(out + tone, 0, 255), mm


def run(cfg, kind, rng, **kw):
    patches = []
    for p in cfg[:N]:
        g = L.frame_geometry(p, kind)
        y0, y1, x0, x1 = L.helm_box(g["rgb"], g["mask"], g["body"], g["crown"],
                                    g["neck"], g["sole"])
        r = L.crop_pad(g["rgb"], y0, y1, x0, x1)
        mm = L.crop_pad(g["body"].astype(np.uint8), y0, y1, x0, x1).astype(bool)
        del g
        if kw:
            amp = {k: float(rng.uniform(-v, v)) for k, v in kw.items()}
            r, mm = warp(r, mm,
                         scale=1.0 + amp.get("scale_pct", 0.0) / 100.0,
                         rot=amp.get("rot_deg", 0.0),
                         tone=amp.get("tone", 0.0))
        patches.append(L.prepped(r, mm, L.HELM_H))
    vals = []
    for k in range(LAG, len(patches)):
        a, b = patches[k], patches[k - LAG]
        vals.append(L.residual(a[0], a[1], b[0], b[1])[0])
    return L.stats(vals)


def main():
    drive = [os.path.join(L.RUNS, "fal_t4", "drive", "d_%04d.png" % i)
             for i in range(N)]
    rows = [("none (the floor)", {}),
            ("helm scale +-1%", dict(scale_pct=1.0)),
            ("helm scale +-2%", dict(scale_pct=2.0)),
            ("helm scale +-4%", dict(scale_pct=4.0)),
            ("helm rotate +-1 deg", dict(rot_deg=1.0)),
            ("helm rotate +-2 deg", dict(rot_deg=2.0)),
            ("helm rotate +-4 deg", dict(rot_deg=4.0)),
            ("helm tone +-4/255", dict(tone=4.0)),
            ("helm tone +-8/255", dict(tone=8.0))]
    rep = dict(what=__doc__.strip().splitlines()[0],
               base="fal_t4/drive (a rigged render: no drift by construction)",
               frames=N, lag_frames=LAG,
               lag_note="the drive's own one twelfth of a stride (period 34), so "
                        "these numbers sit on the same scale as the "
                        "helm_drift_phase_matched column of drift.json",
               rows={})
    print("%-24s %8s %8s %8s" % ("perturbation", "median", "p90", "max"))
    for name, kw in rows:
        rng = np.random.default_rng(11)
        s = run(drive, "alpha", rng, **kw)
        rep["rows"][name] = s
        print("%-24s %8.2f %8.2f %8.2f" % (name, s["median"], s["p90"], s["max"]))
    with open(os.path.join(HERE, "sensitivity.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote sensitivity.json")


if __name__ == "__main__":
    main()
