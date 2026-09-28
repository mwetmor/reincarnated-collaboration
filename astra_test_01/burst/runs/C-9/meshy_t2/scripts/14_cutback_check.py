#!/usr/bin/env python3
"""C-9 meshy_t2 step 10b: prove the cut-back is the inverse of the build.

    python3 scripts/14_cutback_check.py

Every layout claims `crop the painted cell, resize to crop[2] x crop[3], paste
at (crop[0], crop[1]) into a 512 x 512 frame`. This runs that claim on the
UNPAINTED sheets and measures the error against the frame they were built
from, because the moment Astra returns a painted sheet the ground truth is
gone and the only thing standing between a good paint and a misplaced sprite
is that sentence being exactly true.

The resample is lossy by design (512 crop -> 384 cell -> back), so the test is
not "identical" but "lands on the same pixels": IoU of the silhouette and the
centroid offset in pixels. A cut-back that is geometrically right gives IoU
above ~0.97 and a centroid within a fraction of a pixel; one that is off by a
row or a scale factor does not.
"""
import glob, json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASTRA = os.path.join(ROOT, "astra_in")
FRAME = 512


def alpha_of(p):
    im = Image.open(p).convert("RGBA")
    return np.array(im.getchannel("A")) > 100


def main():
    rows = []
    for lp in sorted(glob.glob(os.path.join(ASTRA, "*_sheet_layout.json"))):
        lay = json.load(open(lp))
        sheet = Image.open(os.path.join(ASTRA, lay["sheet"])).convert("RGB")
        arr = np.array(sheet)
        for c in lay["cells"]:
            if not c.get("source"):
                continue
            cell = sheet.crop((c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"]))
            back = cell.resize((c["crop"][2], c["crop"][3]), Image.LANCZOS)
            canvas = Image.new("RGB", (FRAME, FRAME), (0, 255, 0))
            canvas.paste(back, (c["crop"][0], c["crop"][1]))
            g = np.array(canvas).astype(np.int16)
            # the plate is pure green; anything that is not the plate is figure
            got = ~((np.abs(g[..., 0]) < 40) & (g[..., 1] > 200) & (g[..., 2] < 40))
            want = alpha_of(os.path.join(ROOT, c["source"]))
            inter = float((got & want).sum()); union = float((got | want).sum())
            iou = inter / max(union, 1)
            def centroid(m):
                ys, xs = np.nonzero(m)
                return (float(xs.mean()), float(ys.mean())) if len(xs) else (0.0, 0.0)
            cg, cw = centroid(got), centroid(want)
            rows.append(dict(sheet=lay["sheet"], cell=c["cell"], src=c["source"],
                             iou=round(iou, 4),
                             dx=round(cg[0] - cw[0], 3), dy=round(cg[1] - cw[1], 3)))
    ious = [r["iou"] for r in rows]
    dmax = max(max(abs(r["dx"]), abs(r["dy"])) for r in rows)
    rep = dict(cells=len(rows), iou_min=round(min(ious), 4),
               iou_mean=round(float(np.mean(ious)), 4),
               centroid_max_px=round(dmax, 3),
               verdict=("PASS" if min(ious) > 0.95 and dmax < 1.0 else "FAIL"),
               rows=rows)
    json.dump(rep, open(os.path.join(ROOT, "work", "cutback_check.json"), "w"), indent=1)
    print("cut-back round trip over %d cells: IoU min %.4f mean %.4f, "
          "centroid max %.3f px  -> %s"
          % (len(rows), rep["iou_min"], rep["iou_mean"], dmax, rep["verdict"]))
    worst = sorted(rows, key=lambda r: r["iou"])[:3]
    for r in worst:
        print("   worst: %s cell %d  IoU %.4f  d(%.2f, %.2f)"
              % (r["sheet"], r["cell"], r["iou"], r["dx"], r["dy"]))


if __name__ == "__main__":
    main()
