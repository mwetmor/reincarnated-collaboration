# Count silhouette height / width / area from the renders.
#   python3 scripts/20_count_sil.py <dir> <label> <out.json>
import json, os, sys
import numpy as np
from PIL import Image
D, LABEL, OUTJ = sys.argv[1], sys.argv[2], sys.argv[3]
rows = {}
for pose in ("rest", "walk_pass"):
    for f in ("S", "SE", "E", "NE", "N", "NW", "W", "SW"):
        p = os.path.join(D, "%s_%s.png" % (pose, f))
        if not os.path.exists(p):
            continue
        A = np.array(Image.open(p).convert("RGBA"))[..., 3] > 8
        ys, xs = np.where(A)
        rows.setdefault(pose, {})[f] = dict(
            h=int(ys.max() - ys.min() + 1), w=int(xs.max() - xs.min() + 1),
            area=int(A.sum()))
for pose, d in rows.items():
    hs = [v["h"] for v in d.values()]; ws = [v["w"] for v in d.values()]
    ar = [v["area"] for v in d.values()]
    print("%s / %s" % (LABEL, pose))
    print("   %-4s %6s %6s %8s" % ("dir", "h px", "w px", "area px"))
    for f, v in d.items():
        print("   %-4s %6d %6d %8d" % (f, v["h"], v["w"], v["area"]))
    print("   spread: height %d..%d (%.1f%%), width %d..%d (%.1f%%), "
          "area %d..%d (%.1f%%)"
          % (min(hs), max(hs), 100 * (max(hs) / min(hs) - 1),
             min(ws), max(ws), 100 * (max(ws) / min(ws) - 1),
             min(ar), max(ar), 100 * (max(ar) / min(ar) - 1)))
json.dump(dict(label=LABEL, rows=rows), open(OUTJ, "w"), indent=1)
