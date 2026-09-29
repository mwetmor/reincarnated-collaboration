#!/usr/bin/env python3
"""C-9 T10-1a: identity plates for the barrow's unique assets, cut from the concept.

    python3 24_identity_plates.py --variant a

Each plate is the concept's own pixels for that asset, at NATIVE resolution, matted onto
flat #00ff00 -- the same shape of reference the T9 props were built from, and for the same
reason: the sheet has to be four views of THIS object, not of a similar one.

The plates are also the scale record. Every height on them is a ruler reading off the
screen through K = 140.86 px/m, which the barbarian fixes at 1.85 m; no depth model is
involved, so these numbers carry none of the terrain's 1.71x calibration spread.

ASSETS ARE GROUPED BY WHAT THEY ARE, not by which mask found them. SAM2's automatic
proposals cover the stones, rocks, ice and heather and never isolated the figure, the
birches or the juniper (best overlap 0.00, 0.00, 0.01 across all 68 of them); evf-sam's
prompts found those but returned one birch out of several, the wrong region for "rock",
the open snow for "path" and the figure for "raven". Neither segmenter alone produces this
list, which is why both were run.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts" / "T10C-barrow"
WORK = HERE / "work"
OUT = HERE / "plates"
GREEN = (0, 255, 0)
COS_P = 0.602462172508240

# asset -> (source, selector). "sam2" picks from the object list by class and rank;
# "evf" takes a connected component of a prompted mask.
ASSETS = {
    "standing_stone_tall":  ("sam2", "standing_stones", 0),
    "standing_stone_mid":   ("sam2", "standing_stones", 1),
    "standing_stone_short": ("sam2", "standing_stones", 2),   # rank 3 is a clipped sliver
    "barrow_lintel":        ("sam2", "barrow_door", 0),
    "barrow_post":          ("sam2", "barrow_door", 1),
    "rock_outcrop_large":   ("sam2", "rock_outcrop", 0),
    "rock_outcrop_small":   ("sam2", "rock_outcrop", 6),
    "dead_birch":           ("evf", "trees", 0),
    "juniper_bush":         ("evf", "juniper", 1),   # rank 0 is a 2.56 m CLUMP, not a bush
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="a")
    ap.add_argument("--pad", type=int, default=10)
    a = ap.parse_args()
    v = a.variant
    OUT.mkdir(parents=True, exist_ok=True)

    rgb = np.asarray(Image.open(ART / ("T10C-barrow_%s.png" % v)).convert("RGB"))
    objs = json.loads((HERE / "out" / ("objects_%s.json" % v)).read_text())
    K = objs["px_per_metre"]

    by_class = {}
    for o in objs["objects"]:
        by_class.setdefault(o["class"], []).append(o)
    for k in by_class:
        by_class[k].sort(key=lambda o: -o["area_px"])

    man = {"variant": v, "px_per_metre": K,
           "scale_note": "height_m = bbox_px / (K * cos(pitch)); width_m = bbox_px / K; "
                         "K fixed by the barbarian at 1.85 m. No depth model involved.",
           "assets": {}}

    for name, (src, key, rank) in ASSETS.items():
        if src == "sam2":
            lst = by_class.get(key, [])
            if rank >= len(lst):
                print("skip %-22s (only %d of class %s)" % (name, len(lst), key))
                continue
            o = lst[rank]
            m = np.asarray(Image.open(WORK / ("sam2_%s_%s" % (v, o["mask"].split("_")[-1]))
                                      ).convert("L")) > 127
            x0, y0, x1, y1 = o["screen_bbox"]
        else:
            p = WORK / ("evf_%s_%s.png" % (v, key))
            full = np.asarray(Image.open(p).convert("L")) > 127
            lab, n = ndimage.label(full)
            sizes = ndimage.sum(full, lab, range(1, n + 1))
            order = np.argsort(-sizes)
            if rank >= len(order):
                continue
            m = lab == (1 + int(order[rank]))
            ys, xs = np.nonzero(m)
            x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

        lab2, n2 = ndimage.label(m)
        if n2 > 1:
            sz = ndimage.sum(m, lab2, range(1, n2 + 1))
            m = lab2 == (1 + int(np.argmax(sz)))
            ys, xs = np.nonzero(m)
            x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

        p_ = a.pad
        cx0, cy0 = max(0, x0 - p_), max(0, y0 - p_)
        cx1, cy1 = min(rgb.shape[1], x1 + p_ + 1), min(rgb.shape[0], y1 + p_ + 1)
        crop = rgb[cy0:cy1, cx0:cx1].copy()
        cm = m[cy0:cy1, cx0:cx1]
        crop[~cm] = GREEN
        path = OUT / ("T10_%s.png" % name)
        Image.fromarray(crop).save(path)

        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        man["assets"][name] = {
            "plate": str(path.relative_to(HERE)),
            "source": "%s:%s#%d" % (src, key, rank),
            "screen_bbox": [x0, y0, x1, y1], "crop_px": [cx1 - cx0, cy1 - cy0],
            "height_m": round(bh / (K * COS_P), 2), "width_m": round(bw / K, 2),
            "mask_px": int(m.sum()),
        }
        print("%-22s %4dx%-4d px  ->  %5.2f m tall, %5.2f m wide"
              % (name, bw, bh, man["assets"][name]["height_m"], man["assets"][name]["width_m"]))

    man["reuse"] = {"raven": "T9 build at runs/C-9/t9_props/reduced/raven.glb, 0.28 m"}
    (HERE / "asset_plates.json").write_text(json.dumps(man, indent=1) + "\n")
    print("-> %s" % (HERE / "asset_plates.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
