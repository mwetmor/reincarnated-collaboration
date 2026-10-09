#!/usr/bin/env python3
"""BV2F LV (R-C9-319): the pilot re-base check against a MASK -- every guide / class / ids pixel of the pilot window
(plate x < 4096, y < 2560) that changed vs PT's pinned renders must lie inside the allowlist = the mask (255) plus the
declared rectangles. Changed pixels outside are clustered and reported with their pinned class.

    python3 fid/lv/tools/lv_pilot_allowlist_mask.py --tag 023686e3c --mask art/pilot_sea_allow_319.png \
        --rects '{"spar": [[581,1832,849,2334]], ...}'      -> fid/lv/art/pilot_allowlist_319.json ; exit 1 on any outside
"""
import json
import os
import sys
from collections import Counter

import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
FID = os.path.dirname(LV)
PW, PH_ = 4096, 2560


def main():
    a = sys.argv
    tag = a[a.index("--tag") + 1]
    mask = np.asarray(Image.open(os.path.join(LV, a[a.index("--mask") + 1])))[:PH_, :PW] > 0
    rects = json.loads(a[a.index("--rects") + 1])
    allow = mask.copy()
    for nm, rl in rects.items():
        for r in rl:
            x0, y0, x1, y1 = [int(round(v)) for v in r]
            allow[max(0, y0):max(0, min(PH_, y1)), max(0, x0):max(0, min(PW, x1))] = True
    m = json.load(open(os.path.join(LV, "guide_art", "guide_manifest.json")))
    cls = m["class"]["classes"]
    Cp = np.asarray(Image.open(os.path.join(FID, "pt", "ph3", "class_art_pinned_%s.png" % tag)))[:PH_, :PW]
    out = {"_what": __doc__.split("\n")[0], "tag": tag, "mask": a[a.index("--mask") + 1], "rects": rects,
           "allow_share_of_pilot_pct": round(100 * float(allow.mean()), 2)}
    ok = True
    for nm in ("guide", "class", "ids"):
        A = np.asarray(Image.open(os.path.join(LV, "guide_art", "%s_art.png" % nm)))[:PH_, :PW]
        B = np.asarray(Image.open(os.path.join(FID, "pt", "ph3", "%s_art_pinned_%s.png" % (nm, tag))))[:PH_, :PW]
        d = A != B
        if d.ndim == 3:
            d = d.any(2)
        o = d & ~allow
        lab, n = ndimage.label(ndimage.binary_dilation(o, iterations=6))
        cl = []
        for k, s in enumerate(ndimage.find_objects(lab)):
            sub = o[s] & (lab[s] == k + 1)
            if sub.any():
                cl.append({"bbox_px": [int(s[1].start), int(s[0].start), int(s[1].stop), int(s[0].stop)], "px": int(sub.sum()),
                           "pinned_class": dict(Counter(cls[v] for v in Cp[s][sub]).most_common(3))})
        out[nm] = {"changed_px": int(d.sum()), "changed_outside_px": int(o.sum()), "outside_clusters": cl}
        ok &= int(o.sum()) == 0
    out["PASS"] = bool(ok)
    json.dump(out, open(os.path.join(LV, "art", "pilot_allowlist_319.json"), "w"), indent=1)
    print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk != "outside_clusters"} if isinstance(v, dict) and "changed_px" in v else v) for k, v in out.items() if k in ("guide", "class", "ids", "PASS", "allow_share_of_pilot_pct")}, indent=1))
    for nm in ("guide", "class", "ids"):
        for c in out[nm]["outside_clusters"][:12]:
            print(nm, c)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
