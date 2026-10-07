#!/usr/bin/env python3
"""BV2F Phase 2' pilot pin check (lane PT, R-C9-189). Exit 0 = the pinned guide copy is intact AND LV's current
pilot tiles (fid/lv/guide_art/tiles_5x5, cols 0-2 x rows 0-2) still equal their pins. Exit 1 = a pin moved:
  - pinned guide copy changed           -> HALT (the pilot cfg would paint from a different guide)
  - an LV pilot tile changed            -> R-C9-189: repaint that chunk (report which)
Also reports whether LV's CURRENT full guide still agrees with the pinned copy inside the pilot window (pixel-exact).
    python3 fid/pt/tools/pilot_pins_check.py
"""
import hashlib, json, os, sys
import numpy as np
from PIL import Image

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
pins = json.load(open(os.path.join(FID, "pt", "pilot", "pins.json")))
bad = []
g = os.path.join(FID, pins["guide"]["pinned_copy"].replace("fid/", "", 1))
if sha(g) != pins["guide"]["sha256"]:
    bad.append("pinned guide copy changed: %s" % g)
ki = pins.get("known_inert", {})
for k, t in pins["tiles"].items():
    p = os.path.join(FID, t["file"].replace("fid/", "", 1))
    if not os.path.exists(p) or sha(p) != t["sha256"]:
        if k in ki.get("tiles", []):
            print("[pins] note: LV tile %s differs (known, inert: %s) -- checked pixel-wise below" % (k, ki.get("ruling")))
        else:
            bad.append("pilot tile %s changed in LV's guide (%s) -> repaint per R-C9-189" % (k, t["file"]))
cur = os.path.join(FID, "lv", "guide_art", "guide_art.png")
if os.path.exists(cur) and sha(cur) != pins["guide"]["sha256"]:
    a = np.asarray(Image.open(cur).convert("RGB"))[:2560, :4096]
    b = np.asarray(Image.open(g).convert("RGB"))[:2560, :4096]
    d = (a != b).any(-1) if a.shape == b.shape else None
    if d is None:
        bad.append("LV's current guide has a different size")
    elif d.any():
        ys, xs = np.nonzero(d)
        x0, y0, x1, y1 = ki.get("box_px", [0, 0, -1, -1])
        inside = bool(xs.min() >= x0 and xs.max() <= x1 and ys.min() >= y0 and ys.max() <= y1)
        print("[pins] LV's guide differs inside the pilot window: %d px in x %d-%d, y %d-%d -> %s" % (d.sum(), xs.min(), xs.max(), ys.min(), ys.max(), "inside the known-inert box (%s)" % ki.get("ruling") if inside else "OUTSIDE the known-inert box"))
        if not inside:
            bad.append("LV's current guide differs inside the pilot window outside the known-inert box")
for b in bad:
    print("[pins] FAIL:", b)
if not bad:
    print("[pins] OK: pinned guide %s + 9 pilot tiles unchanged" % pins["guide"]["sha256"][:12])
sys.exit(1 if bad else 0)
