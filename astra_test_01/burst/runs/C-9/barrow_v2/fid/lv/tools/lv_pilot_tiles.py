#!/usr/bin/env python3
"""BV2F LV (R-C9-189): the 9 PAINT-PILOT guide tiles (r00-r02 x c00-c02 of the 5 x 5 grid), BEFORE and AFTER a re-render.

    python3 fid/lv/tools/lv_pilot_tiles.py      -> fid/lv/art/pilot_tiles.json (+ the table on stdout); exit 1 if any moved

BEFORE = lane PT's pins (fid/pt/pilot/pins.json, pinned from LV's published tiles before the stair change);
AFTER  = fid/lv/guide_art/tiles_5x5/ now. Also: the full guide inside the pilot window (x < 4096, y < 2560) against
PT's pinned guide copy, pixel by pixel, and -- for information -- the ID and class maps inside the same window.
"""
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
FID = os.path.dirname(LV)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    pins = json.load(open(os.path.join(FID, "pt", "pilot", "pins.json")))
    rows, moved = [], 0
    for k, t in sorted(pins["tiles"].items(), key=lambda kv: kv[1]["file"]):
        p = os.path.join(FID, t["file"].replace("fid/", "", 1))
        now = sha(p) if os.path.exists(p) else None
        same = now == t["sha256"]
        moved += 0 if same else 1
        rows.append({"tile": os.path.basename(p), "before_sha256": t["sha256"], "after_sha256": now, "identical": same})
    g_now = os.path.join(LV, "guide_art", "guide_art.png")
    g_pin = os.path.join(FID, pins["guide"]["pinned_copy"].replace("fid/", "", 1))
    a = np.asarray(Image.open(g_now).convert("RGB"))
    b = np.asarray(Image.open(g_pin).convert("RGB"))
    win = (slice(0, 2560), slice(0, 4096))
    diff = np.any(a != b, axis=2)
    out = {"_what": __doc__.split("\n")[0], "pins": "fid/pt/pilot/pins.json (pinned %s)" % pins["pinned_utc"], "tiles": rows, "moved": moved,
           "guide": {"before_sha256": pins["guide"]["sha256"], "after_sha256": sha(g_now),
                     "pilot_window_pixels_differing": int(diff[win].sum()),
                     "whole_guide_pixels_differing": int(diff.sum()),
                     "differing_bbox_px": None if not diff.any() else [int(np.where(diff.any(0))[0].min()), int(np.where(diff.any(1))[0].min()),
                                                                       int(np.where(diff.any(0))[0].max()), int(np.where(diff.any(1))[0].max())]}}
    for nm, key in (("ids_art.png", "ids"), ("class_art.png", "class")):
        cur = os.path.join(LV, "guide_art", nm)
        out[key] = {"before_sha256": pins[key]["sha256"], "after_sha256": sha(cur)}
    json.dump(out, open(os.path.join(LV, "art", "pilot_tiles.json"), "w"), indent=1)
    for r in rows:
        print("  %s  %s -> %s  %s" % (r["tile"], r["before_sha256"][:12], (r["after_sha256"] or "MISSING")[:12], "identical" if r["identical"] else "MOVED"))
    print("[pilot] %d of 9 tiles moved; guide inside the pilot window: %d px differ (whole guide: %d px, bbox %s)" % (
        moved, out["guide"]["pilot_window_pixels_differing"], out["guide"]["whole_guide_pixels_differing"], out["guide"]["differing_bbox_px"]))
    return 1 if moved else 0


if __name__ == "__main__":
    sys.exit(main())
