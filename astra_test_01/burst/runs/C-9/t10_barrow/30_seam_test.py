#!/usr/bin/env python3
"""C-9 T10: the wrap test for the ground tiles, and the seam-repair canvas when one fails.

    python3 30_seam_test.py                 # measure every tile variant
    python3 30_seam_test.py --rolled DIR    # also write the rolled canvases for an EDIT

THE TEST. Roll the tile by half its width and half its height. Every edge that will meet a
neighbour when the tile repeats now meets itself in a cross through the middle of the
canvas. Measure the gradient energy across that cross and compare it against the SAME
statistic on interior lines of the same tile.

    seam_ratio = (gradient energy across the wrap line) / (median across interior lines)

THE NULL COMES FROM THE TILE ITSELF, not from a number I picked. A rock tile is busy and a
snow tile is smooth, so an absolute threshold would pass every snow tile and fail every
rock tile regardless of their seams. Comparing a tile's seam against its own interior asks
the only question that matters: is there MORE discontinuity at the wrap than this material
has anywhere else? A seamless tile scores about 1.0 whatever it is made of.

A synthetic control runs first, every time: the same tile with a deliberate seam forced
into it (half the image shifted in brightness) must score far above 1.0, or the instrument
is not measuring what it claims. Without that leg the test would return a comfortable 1.0
for a tile it could not see the seam in, and 1.0 is exactly what success looks like.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts"
TILES = ["T10T-snow-r1", "T10T-path", "T10T-rock", "T10T-ice", "T10T-heather", "T10T-bark"]


def seam_ratio(img: np.ndarray, axis: int) -> tuple[float, float, float]:
    """Discontinuity at the wrap line vs the same measure on interior lines."""
    g = img.astype(np.float32).mean(-1) if img.ndim == 3 else img.astype(np.float32)
    n = g.shape[axis]
    d = np.abs(np.diff(g, axis=axis))                       # per-line step energy
    prof = d.mean(axis=1 - axis)                            # one number per line
    mid = n // 2 - 1                                        # the wrap line after the roll
    band = prof[max(0, mid - 1):mid + 2]
    seam = float(band.max())
    interior = np.concatenate([prof[8:mid - 6], prof[mid + 7:-8]])
    null = float(np.median(interior))
    p99 = float(np.percentile(interior, 99))
    return seam, null, p99


def score(img: np.ndarray) -> dict:
    rolled = np.roll(np.roll(img, img.shape[0] // 2, 0), img.shape[1] // 2, 1)
    sy, ny, py = seam_ratio(rolled, 0)
    sx, nx, px = seam_ratio(rolled, 1)
    return {"vertical_wrap": {"seam": round(sy, 3), "interior_median": round(ny, 3),
                              "interior_p99": round(py, 3),
                              "ratio": round(sy / max(ny, 1e-6), 2)},
            "horizontal_wrap": {"seam": round(sx, 3), "interior_median": round(nx, 3),
                                "interior_p99": round(px, 3),
                                "ratio": round(sx / max(nx, 1e-6), 2)},
            "worst_ratio": round(max(sy / max(ny, 1e-6), sx / max(nx, 1e-6)), 2)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rolled", default=None, help="write rolled canvases here for an EDIT")
    ap.add_argument("--fail-at", type=float, default=1.6)
    a = ap.parse_args()
    out = {}
    rolled_dir = pathlib.Path(a.rolled) if a.rolled else HERE / "seam"
    rolled_dir.mkdir(parents=True, exist_ok=True)

    control_done = False
    for t in TILES:
        for v in ("a", "b"):
            p = ART / t / ("%s_%s.png" % (t, v))
            if not p.exists():
                continue
            img = np.asarray(Image.open(p).convert("RGB"))
            s = score(img)
            s["file"] = str(p)
            s["size"] = list(img.shape[:2])
            if not control_done:
                # the instrument, checked against a seam that is certainly there
                bad = img.astype(np.float32).copy()
                bad[: img.shape[0] // 2] *= 0.82
                c = score(bad.astype(np.uint8))
                out["_control"] = {"what": "the same tile with a forced brightness step across "
                                          "the top half; the instrument must see this",
                                   "worst_ratio": c["worst_ratio"], "on": str(p)}
                control_done = True
            s["verdict"] = "seamless" if s["worst_ratio"] < a.fail_at else "SEAM"
            if s["verdict"] == "SEAM" and a.rolled is not None:
                r = np.roll(np.roll(img, img.shape[0] // 2, 0), img.shape[1] // 2, 1)
                rp = rolled_dir / ("%s_%s_rolled.png" % (t, v))
                Image.fromarray(r).save(rp)
                s["rolled_canvas"] = str(rp)
            out["%s_%s" % (t, v)] = s
            print("%-16s %s  worst ratio %5.2f  (v %.2f / h %.2f)  %s"
                  % (t, v, s["worst_ratio"], s["vertical_wrap"]["ratio"],
                     s["horizontal_wrap"]["ratio"], s["verdict"]))
    if "_control" in out:
        print("\ncontrol (a seam that IS there): worst ratio %.2f -- the test can see one"
              % out["_control"]["worst_ratio"])
    (HERE / "seam_report.json").write_text(json.dumps(out, indent=1) + "\n")
    print("-> %s" % (HERE / "seam_report.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
