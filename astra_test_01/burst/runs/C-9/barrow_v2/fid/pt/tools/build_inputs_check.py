#!/usr/bin/env python3
"""BV2F PT (R-C9-310 R-1): BUILD-INPUTS CHECK -- every gitignored file the Phase 3' build consumes (and the M3' evidence)
must exist with its recorded sha256. Exit 0 = all present and matching; exit 1 = any missing or mismatched (each printed).
    python3 fid/pt/tools/build_inputs_check.py [fid/pt/ph3/final/build_inputs_manifest.json]"""
import hashlib, json, os, sys
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
C9 = os.path.dirname(os.path.dirname(FID))
m = json.load(open(sys.argv[1] if len(sys.argv) > 1 else FID + "/pt/ph3/final/build_inputs_manifest.json"))
bad, n = [], 0
for grp, rows in m["files"].items():
    for r in rows:
        n += 1
        p = os.path.join(C9, r["path"])
        if not os.path.exists(p):
            bad.append("MISSING  %s  %s" % (grp, r["path"])); continue
        if hashlib.sha256(open(p, "rb").read()).hexdigest() != r["sha256"]:
            bad.append("SHA MISMATCH  %s  %s" % (grp, r["path"]))
for b in bad:
    print("[build_inputs] FAIL:", b)
print("[build_inputs] %s: %d files, %d bad" % ("OK" if not bad else "FAIL", n, len(bad)))
sys.exit(1 if bad else 0)
