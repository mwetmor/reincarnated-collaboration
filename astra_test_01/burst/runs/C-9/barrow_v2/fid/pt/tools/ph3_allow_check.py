#!/usr/bin/env python3
"""BV2F PT (R-C9-321): the PILOT re-base check against LV's MASK allowlist. Every guide / class / ids pixel of the pilot
window (plate x < 4096, y < 2560) that differs between LV's pinned render at <new> and PT's previous pins at <old> must lie
inside the allowlist = LV's mask (255) UNION every rectangle of LV's allowlist json (spar, W1, rubble, beach_reveal) UNION
the extra rects named on the command line (R-C9-321: the accepted waterline [1234,2186,1825,2473]). Exit 1 on ANY pixel
outside (HALT). Writes the union as a PNG (the pilot zone the sea pass may change) and a JSON record.
    python3 fid/pt/tools/ph3_allow_check.py --old 023686e3c --new bac035332 --allow-json fid/lv/art/pilot_allowlist_319.json \
        --extra '{"waterline": [[1234,2186,1825,2473]]}' --out fid/pt/ph3/allow_321    [--cur-guide <png> (test hook)]
"""
import hashlib, json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
REPO = "/Users/admin/Games/reincarnated-collaboration"
PW, PH_ = 4096, 2560
a = sys.argv
arg = lambda k, d=None: a[a.index(k) + 1] if k in a else d
old, new, out = arg("--old"), arg("--new"), arg("--out")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
aj_rel = arg("--allow-json")
AJ = json.loads(subprocess.check_output(["git", "-C", REPO, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/%s" % (new, aj_rel)]))
mask_rel = "fid/lv/" + AJ["mask"]
mask_bytes = subprocess.check_output(["git", "-C", REPO, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/%s" % (new, mask_rel)])
mask_path = os.path.join(os.path.dirname(FID), mask_rel)
assert hashlib.sha256(mask_bytes).hexdigest() == sha(mask_path), "LV's working mask differs from the mask at %s" % new
rects = dict(AJ["rects"])
for k, v in json.loads(arg("--extra", "{}")).items():
    rects[k] = rects.get(k, []) + v
allow = np.asarray(Image.open(mask_path))[:PH_, :PW] > 0
for nm, rl in rects.items():
    for r in rl:
        x0, y0, x1, y1 = [int(round(v)) for v in r]
        allow[max(0, y0):max(0, min(PH_, y1)), max(0, x0):max(0, min(PW, x1))] = True
oldp = json.load(open(FID + "/pt/ph3/pins_ph3_%s.json" % old)) if os.path.exists(FID + "/pt/ph3/pins_ph3_%s.json" % old) else None
newp = json.load(open(FID + "/pt/ph3/pins_ph3.json"))
assert newp["lv_commit"] == new, "pins_ph3.json is not at %s (run ph3_pin.py first)" % new
rec = {"_what": "BV2F PT pilot re-base check (R-C9-321): %s -> %s, pilot window, allowlist = LV mask + rects + extra" % (old, new),
       "mask": mask_rel, "mask_sha256": sha(mask_path), "rects": rects, "allow_px": int(allow.sum()),
       "allow_share_pct": round(100 * float(allow.mean()), 2)}
cls = json.loads(subprocess.check_output(["git", "-C", REPO, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % new]))["class"]["classes"]
ok = True
for nm in ("guide", "class", "ids"):
    pa = os.path.join(os.path.dirname(FID), newp[nm]["pinned_copy"])
    pb = os.path.join(os.path.dirname(FID), oldp[nm]["pinned_copy"]) if oldp else FID + "/pt/ph3/%s_art_pinned_%s.png" % (nm, old)
    if nm == "guide" and arg("--cur-guide"):
        pa = arg("--cur-guide")
    A = np.asarray(Image.open(pa))[:PH_, :PW]
    B = np.asarray(Image.open(pb))[:PH_, :PW]
    d = A != B
    d = d.any(2) if d.ndim == 3 else d
    o = d & ~allow
    cl = []
    if o.any():
        lab, n = ndimage.label(ndimage.binary_dilation(o, iterations=6))
        for k, s in enumerate(ndimage.find_objects(lab)):
            sub = o[s] & (lab[s] == k + 1)
            if sub.any():
                cl.append({"bbox_px": [int(s[1].start), int(s[0].start), int(s[1].stop), int(s[0].stop)], "px": int(sub.sum())})
    rec[nm] = {"new": os.path.relpath(pa, os.path.dirname(FID)), "old": os.path.relpath(pb, os.path.dirname(FID)),
               "changed_px": int(d.sum()), "changed_inside_px": int((d & allow).sum()), "changed_outside_px": int(o.sum()),
               "outside_clusters": cl[:40]}
    ok &= not o.any()
    print("[allow] %s: %d changed pilot px, %d inside, %d OUTSIDE" % (nm, d.sum(), (d & allow).sum(), o.sum()))
rec["PASS"] = bool(ok)
if out:
    Image.fromarray((allow * 255).astype(np.uint8)).save(out + ".png")
    rec["allow_png"] = os.path.relpath(out + ".png", os.path.dirname(FID)); rec["allow_png_sha256"] = sha(out + ".png")
    json.dump(rec, open(out + ".json", "w"), indent=1)
print("[allow] PASS" if ok else "[allow] HALT: pilot pixels changed outside the allowlist")
sys.exit(0 if ok else 1)
