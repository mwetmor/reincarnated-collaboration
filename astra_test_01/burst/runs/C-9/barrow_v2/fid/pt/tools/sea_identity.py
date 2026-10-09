#!/usr/bin/env python3
"""BV2F PT sea pass (R-C9-321): the PILOT-IDENTITY proof + the land proof, on the re-stitched painting vs the reviewed final.
  (1) pilot window (x < 4096, y < 2560): every changed px lies inside the R-C9-321 allowlist (fid/pt/ph3/allow_321.png =
      LV's 319 mask + spar/W1/rubble/beach_reveal + the accepted waterline rect);
  (2) the whole plate: every changed px lies inside the sea pass PASTE mask (fid/pt/ph3/sea/PC_full.png = water/ice
      classes, ice that changed class, the accepted pilot rects) -- land that is land in both maps is byte-identical.
Exit 1 on any px outside.   python3 fid/pt/tools/sea_identity.py <new.png> [--control]"""
import hashlib, json, sys
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
import os
RND = os.environ.get("SEA_ROUND", "r321")   # R-C9-328: round r328 = vs the r321 painting, its allowlist and its paste mask
OLD = FID + ("/pt/ph3/final/painting_ph3_full.png" if RND == "r321" else "/pt/ph3/final/painting_ph3_sea_full.png")
SEA = FID + ("/pt/ph3/sea/" if RND == "r321" else "/pt/ph3/sea_%s/" % RND)
ALW = FID + ("/pt/ph3/allow_321.png" if RND == "r321" else "/pt/ph3/allow_330.png")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
new_p = sys.argv[1]
a = np.asarray(Image.open(OLD).convert("RGB")); b = np.asarray(Image.open(new_p).convert("RGB")).copy()
PC = np.asarray(Image.open(SEA + "PC_full.png")) > 0
allow = np.zeros(PC.shape, bool); allow[:2560, :4096] = np.asarray(Image.open(ALW)) > 0
if "--control" in sys.argv:   # constructed RED: one land px in the pilot (outside both masks) and one outside the pilot
    for y, x in ((300, 3000), (1000, 6000)):
        assert not PC[y, x] and not allow[y, x]
        b[y, x] = 255 - b[y, x]
d = (a != b).any(-1)
pil = np.zeros_like(d); pil[:2560, :4096] = True
out1 = d & pil & ~allow
out2 = d & ~PC
rec = {"_what": __doc__.split("\n")[0], "old": OLD, "old_sha256": sha(OLD), "new": new_p, "new_sha256": sha(new_p),
       "changed_px": int(d.sum()), "pilot_changed_px": int((d & pil).sum()), "pilot_changed_outside_allowlist_px": int(out1.sum()),
       "changed_outside_paste_mask_px": int(out2.sum()), "allow_png_sha256": sha(ALW),
       "paste_mask_sha256": sha(SEA + "PC_full.png"), "control": "--control" in sys.argv}
rec["PASS"] = not out1.any() and not out2.any()
print(json.dumps(rec, indent=1))
if "--control" not in sys.argv:
    json.dump(rec, open(SEA + "identity_proof.json", "w"), indent=1)
sys.exit(0 if rec["PASS"] else 1)
