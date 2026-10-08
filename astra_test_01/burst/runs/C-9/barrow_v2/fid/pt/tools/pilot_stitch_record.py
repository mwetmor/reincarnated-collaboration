#!/usr/bin/env python3
"""BV2F PT: fid/pt/pilot/stitch_record.json for the stitched pilot -- the painting's sha, each canvas (artifact + sha, the
retry's when there was one: guided_stitch.py's own src() rule), and the overlap MAD of every neighbour pair (1-px
mean abs over the shared 256-px strip, the stitch's partition of unity aside)."""
import hashlib, json, os
import numpy as np
from PIL import Image
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(FID, "pt", "pilot")
A9 = os.path.abspath(os.path.join(FID, "..", "..", "artifacts"))
cfg = json.load(open(os.environ.get("PT_CFG", os.path.join(P, "cfg_bv2a_pilot.json"))))   # R-C9-264: the cfg being built
PX, C, R = cfg["prefix"], cfg["cols"], cfg["rows"]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def src(k):
    for d in ("%s-%s-r1" % (PX, k), "%s-%s" % (PX, k)):
        p = os.path.join(A9, d, "%s-%s.png" % (PX, k))
        if os.path.exists(p):
            return p
im, can = {}, {}
for r in range(R):
    for c in range(C):
        k = "%d_%d" % (c, r)
        p = src(k)
        im[k] = np.asarray(Image.open(p).convert("RGB")).astype(np.float64)
        can[k] = {"artifact": os.path.relpath(p, os.path.dirname(A9)), "sha256": sha(p)}
mad = {}
for r in range(R):
    for c in range(C):
        k = "%d_%d" % (c, r)
        if c + 1 < C:
            mad["%s|%d_%d" % (k, c + 1, r)] = round(float(np.abs(im[k][:, 1280:] - im["%d_%d" % (c + 1, r)][:, :256]).mean()), 2)
        if r + 1 < R:
            mad["%s/%d_%d" % (k, c, r + 1)] = round(float(np.abs(im[k][768:, :] - im["%d_%d" % (c, r + 1)][:256, :]).mean()), 2)
pp = os.path.join(P, "painting.png")
json.dump({"_what": "BV2F PT pilot stitch record (the TIER-B guided_stitch.py: v1 + DEV-23/25/26/27 [+ DEV-24 post-stitch], flags below; partition of unity) -- R-C9-232, label fixed R-C9-268 (jack-ryan pilot-4 Gate-2 s5(b))",
           "painting": "fid/pt/pilot/painting.png", "sha256": sha(pp), "prefix": PX, "canvases": can,
           "overlap_mad": mad, "flags": {f: (os.environ.get("BV2F_" + f, "1" if f != "DEV24" else "0") != "0") for f in ("DEV23", "DEV25", "DEV26", "DEV27", "DEV24")}, "overlap_mad_range": [min(mad.values()), max(mad.values())],
           "_ref": "Phase 2' 5.29-11.97; v1 2.7-13.1"}, open(os.path.join(P, "stitch_record.json"), "w"), indent=1)
print(json.dumps({"sha": sha(pp)[:12], "mad": [min(mad.values()), max(mad.values())]}))
