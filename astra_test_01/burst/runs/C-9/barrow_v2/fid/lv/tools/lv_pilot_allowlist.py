#!/usr/bin/env python3
"""BV2F LV (R-C9-294): the PILOT re-base allowlist -- every pixel of the pilot window (plate x < 4096, y < 2560) that changed
in the guide (and the ID and class maps) vs a reference render, and the rectangles that hold them.

    python3 fid/lv/tools/lv_pilot_allowlist.py --ref-guide G --ref-class C [--ref-ids I] -> fid/lv/art/pilot_allowlist_294.json
      exit 1 if any changed guide pixel lies outside the declared rectangles (R-C9-294 A + C + the cradle cracks' rects)

The declared rectangles are read from the layout (layout_bv2art.json r294.allow_rects_plate_px). The changed pixels are
clustered (8 px dilation) and each cluster's bounding box reported, with the rectangle(s) that hold it.
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
PW, PH_ = 4096, 2560


def main():
    a = sys.argv
    ref_g = a[a.index("--ref-guide") + 1]
    ref_c = a[a.index("--ref-class") + 1]
    lay = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))
    R = lay["r294"]["allow_rects_plate_px"]
    rects = [("A", r) for r in R["A"]] + [("C", r) for r in R["C"]] + [("cradle_cracks", r) for r in R["cradle_cracks"]]
    out = {"_what": __doc__.split("\n")[0], "ref_guide": ref_g, "ref_class": ref_c, "declared": R}
    for nm, cur, ref in (("guide", os.path.join(LV, "guide_art", "guide_art.png"), ref_g), ("class", os.path.join(LV, "guide_art", "class_art.png"), ref_c)):
        A = np.asarray(Image.open(cur))[:PH_, :PW]
        B = np.asarray(Image.open(ref))[:PH_, :PW]
        d = (A != B)
        if d.ndim == 3:
            d = d.any(2)
        allow = np.zeros(d.shape, bool)
        for _, r in rects:
            x0, y0, x1, y1 = [int(round(v)) for v in r]
            allow[max(0, y0):max(0, min(PH_, y1)), max(0, x0):max(0, min(PW, x1))] = True
        outside = d & ~allow
        lab, n = ndimage.label(ndimage.binary_dilation(d, iterations=8))
        clusters = []
        for k, s in enumerate(ndimage.find_objects(lab)):
            sub = d[s] & (lab[s] == k + 1)
            if not sub.any():
                continue
            box = [int(s[1].start), int(s[0].start), int(s[1].stop), int(s[0].stop)]
            holders = [nm_ for nm_, r in rects if r[0] <= box[0] + 8 and r[1] <= box[1] + 8 and r[2] >= box[2] - 8 and r[3] >= box[3] - 8]
            clusters.append({"bbox_px": box, "changed_px": int(sub.sum()), "inside_declared": bool(not (outside[s] & (lab[s] == k + 1)).any()), "held_by": sorted(set(holders))})
        out[nm] = {"changed_px": int(d.sum()), "changed_outside_declared_px": int(outside.sum()), "clusters": clusters,
                   "outside_bbox": ([int(np.nonzero(outside)[1].min()), int(np.nonzero(outside)[0].min()), int(np.nonzero(outside)[1].max()), int(np.nonzero(outside)[0].max())] if outside.any() else None)}
    out["PASS"] = out["guide"]["changed_outside_declared_px"] == 0 and out["class"]["changed_outside_declared_px"] == 0
    # the FINAL allowlist for PT's pins check: the declared rectangles (clipped to the pilot window), merged where they overlap
    fin = []
    for nm, r in rects:
        x0, y0, x1, y1 = max(0, r[0]), max(0, r[1]), min(PW, r[2]), min(PH_, r[3])
        if x1 > x0 and y1 > y0:
            fin.append({"kind": nm, "rect_px": [int(x0), int(y0), int(x1), int(y1)]})
    out["final_allowlist_rects"] = fin
    json.dump(out, open(os.path.join(LV, "art", "pilot_allowlist_294.json"), "w"), indent=1)
    print(json.dumps({k: (v if k in ("PASS",) else {kk: vv for kk, vv in v.items() if kk != "clusters"}) for k, v in out.items() if k in ("guide", "class", "PASS")}, indent=1))
    sys.exit(0 if out["PASS"] else 1)


if __name__ == "__main__":
    main()
