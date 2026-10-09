#!/usr/bin/env python3
"""BV2F PT (R-C9-301): P-2b RE-RUN with DEV-24 LAYER 4 (read_zone pins) on the 5 x 5 STAND-IN (BV2F-PS4SI, R-C9-272):
DEV-26 pin + the 4-layer DEV-24 block -> the pilot identity zone (x < 3840, y < 2304) must be byte-identical to the
layer-4 pilot painting (fid/pt/dev24/painting_dev24_l4.png). Control: the same zone in a stitch WITHOUT layer 4 differs."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
SCR = sys.argv[1]
GS = FID + "/v1tools/tierB/conductor_scripts/guided_stitch.py"
c = json.load(open(FID + "/pt/pilot/cfg_bv2a_pilot_ps4.json"))
c["prefix"], c["cols"], c["rows"] = "BV2F-PS4SI", 5, 5
c["dev26_pin"] = {"file": FID + "/pt/r272/fullsite/dev26_paths_pilot.json", "x_len": 2304, "y_len": 3840}
import hashlib; c["dev26_pin"]["sha256"] = hashlib.sha256(open(c["dev26_pin"]["file"], "rb").read()).hexdigest()
res = {}
for name, blk in (("l4", json.load(open(FID + "/pt/dev24/dev24_block_l4.json"))), ("l1_3", json.load(open(FID + "/pt/r272/fullsite/dev24_block_readpins.json")))):
    c["dev24"] = blk; p = SCR + "/p2b_%s_cfg.json" % name; json.dump(c, open(p, "w"))
    r = subprocess.run(["python3", GS, p, SCR + "/p2b_%s.png" % name], env=dict(os.environ, BV2F_DEV24="1"), capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stdout[-1500:] + r.stderr[-1500:])
    res[name] = np.asarray(Image.open(SCR + "/p2b_%s.png" % name).convert("RGB"))
ref = np.asarray(Image.open(FID + "/pt/dev24/painting_dev24_l4.png").convert("RGB"))
z = (slice(0, 2304), slice(0, 3840))
d = (res["l4"][z] != ref[z]).any(-1); d3 = (res["l1_3"][z] != ref[z]).any(-1)
out = {"_what": __doc__.split("\n")[0], "zone": [0, 0, 3840, 2304], "l4_zone_identical_to_painting_dev24_l4": bool(not d.any()), "l4_px_changed": int(d.sum()),
       "control_without_l4_px_differ": int(d3.sum()), "pass": bool(not d.any() and d3.any())}
json.dump(out, open(FID + "/pt/r272/fullsite/p2b_l4.json", "w"), indent=1); print(json.dumps(out))
