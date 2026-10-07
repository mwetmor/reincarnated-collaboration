#!/usr/bin/env python3
"""BV2F R-C9-210 (3): v1 control shas (the file list of pc/control_shas_m2.json) -- `before` or `after` the pc6 run.
    python3 fid/pt/tools/pc6_control_shas.py before|after"""
import datetime, hashlib, json, os, sys
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BF = os.path.abspath(os.path.join(FID, "..", "..", "barrow_full"))
OUTF = os.path.join(FID, "pc", "control_shas_phase2pp.json")
ref = json.load(open(os.path.join(FID, "pc", "control_shas_m2.json")))
files = sorted(ref["before"]["files"])
snap = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "files": {f: hashlib.sha256(open(os.path.join(BF, f), "rb").read()).hexdigest() for f in files}}
d = json.load(open(OUTF)) if os.path.exists(OUTF) else {"_what": "BV2F R-C9-210 (3) control shas before/after", "root": "runs/C-9/barrow_full"}
d[sys.argv[1]] = snap
d["before_equals_m2"] = d.get("before", {}).get("files") == ref["before"]["files"]
if "before" in d and "after" in d:
    d["identical"] = d["before"]["files"] == d["after"]["files"]
json.dump(d, open(OUTF, "w"), indent=1)
print({k: v for k, v in d.items() if k not in ("before", "after")})
