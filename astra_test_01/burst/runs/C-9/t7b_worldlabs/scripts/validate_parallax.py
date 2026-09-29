#!/usr/bin/env python3
"""T7-B: check compose_cliffside_b.py's parallax maths against the engine.

frames/horizon_rows.json (R-C9-41) holds on-screen rows measured by RENDERING each
parallax layer alone through Godot at two Keeper positions -- ground truth that does
not come from the scroll maths.  This predicts the same rows from the maths and prints
the residual.

The discriminating layer is far_ruins: a hard ridge line against a keyed sky, so
"first row with any alpha" and "first row >50% opaque" are both crisp.  forest_valley
(ragged treeline) and mist (soft alpha, and measured in the composite rather than on
the layer) carry threshold noise and are printed for information only.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

import compose_cliffside_b as C

Image.MAX_IMAGE_PIXELS = None


def rows(path):
    a = np.asarray(Image.open(path).convert("RGBA"))[:, :, 3]
    first = int(np.argmax((a > 0).any(axis=1))) if (a > 0).any() else None
    cov = (a > 128).mean(axis=1)
    solid = int(np.argmax(cov > 0.5)) if (cov > 0.5).any() else None
    return first, solid


def main():
    gt = json.loads((C.PROJ / "frames" / "horizon_rows.json").read_text())["cameras"]
    offb = json.loads((C.PROJ / "parallax" / "layers_b" / "offsets.json").read_text())["offsets"]
    hard = []
    print(f"{'reg':3s} {'layer':14s} {'cam':8s} {'Cy':>7s} "
          f"{'pred_first':>10s} {'meas_first':>10s} {'pred_solid':>10s} {'meas_solid':>10s}  note")
    for reg, sub, off in (("A", "layers", {k: 0.0 for k, _, _ in C.LAYERS}),
                          ("B", "layers_b", offb)):
        for name, s, so in C.LAYERS:
            first, solid = rows(C.PROJ / "parallax" / sub / f"{name}.png")
            for cam, g in gt.items():
                Cy = C.camera_topleft(g["camera_px"], C.VIEW)[1]
                base = so[1] - s * Cy + off[name]
                m = g["layers"][name][reg]
                pf = base + first if first is not None else None
                ps = base + solid if solid is not None else None

                def clip(v):
                    # the engine reports row 0 for anything at or above the top edge,
                    # and cannot report a row for content that is off-screen
                    return None if v is None or v >= C.VIEW[1] else max(0.0, v)

                pf, ps = clip(pf), clip(ps)
                note = ""
                if name == "far_ruins":
                    for p, mv in ((pf, m["first_row"]), (ps, m["solid_row"])):
                        if p is not None:
                            hard.append(abs(p - mv))
                    note = "HARD EDGE -- discriminating"
                elif name == "mist":
                    note = "soft alpha; engine measured in composite, not on layer"
                else:
                    note = "ragged treeline; threshold noise"
                fs = f"{pf:10.1f}" if pf is not None else f"{'offscr':>10s}"
                ss = f"{ps:10.1f}" if ps is not None else f"{'offscr':>10s}"
                print(f"{reg:3s} {name:14s} {cam:8s} {Cy:7.1f} {fs} {m['first_row']:10d} "
                      f"{ss} {m['solid_row']:10d}  {note}")
    print(f"\nfar_ruins residuals (px): {[round(h,1) for h in hard]}")
    print(f"max {max(hard):.1f} px, mean {sum(hard)/len(hard):.1f} px over {len(hard)} comparisons")


if __name__ == "__main__":
    main()
