#!/usr/bin/env python3
"""BV2F PT (R-C9-278 B-2): PHASE 3' PINS from LV's blockout of record <lv_commit> (b5894d440), as COPIES (standing practice
since R-C9-258): the guide + ID + class renders (the PS4 copies are reused when their sha equals the manifest's -- the
same commit -- else copied anew under fid/pt/ph3/), and ALL 25 tiles of the 5 x 5 grid checked against the manifest at the
commit and against crops of the pinned guide. Then the R-C9-189 rule: the 9 PILOT tiles must equal fid/pt/pilot/pins.json
(else HALT: a changed pilot tile means a repaint). Writes fid/pt/ph3/pins_ph3.json. Read-only on LV; no render.
    python3 fid/pt/tools/ph3_pin.py <lv_commit> <ruling>      (then: python3 fid/pt/tools/pilot_pins_check.py)"""
import datetime, hashlib, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
REPO = "/Users/admin/Games/reincarnated-collaboration"
commit, ruling = sys.argv[1], sys.argv[2]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
m = json.loads(subprocess.check_output(["git", "-C", REPO, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % commit]))
OUT = FID + "/pt/ph3"
os.makedirs(OUT, exist_ok=True)
pilot = json.load(open(FID + "/pt/pilot/pins.json"))
copies = {}
for k in ("guide", "ids", "class"):
    want = m[k]["sha256"]
    ps4 = FID + "/pt/pilot/%s_art_pinned_ps4.png" % k
    if os.path.exists(ps4) and sha(ps4) == want:
        copies[k] = {"pinned_copy": os.path.relpath(ps4, os.path.dirname(FID)), "sha256": want, "reused": "PS4 copy (same commit)"}
    else:
        src = os.path.join(FID, "lv", m[k]["file"])
        assert sha(src) == want, "LV's working %s differs from the manifest at %s" % (k, commit)
        dst = OUT + "/%s_art_pinned_%s.png" % (k, commit)   # R-C9-297: named by LV commit (an earlier pin is never overwritten)
        shutil.copyfile(src, dst)
        assert sha(dst) == want
        copies[k] = {"pinned_copy": os.path.relpath(dst, os.path.dirname(FID)), "sha256": want}
G = np.asarray(Image.open(os.path.join(os.path.dirname(FID), copies["guide"]["pinned_copy"])).convert("RGB"))
tiles, bad = {}, []
for t in m["tiles"]:
    p = os.path.join(FID, "lv", t["file"])
    key = "%d_%d" % (t["col"], t["row"])
    ok_sha = os.path.exists(p) and sha(p) == t["sha256"]
    T = np.asarray(Image.open(p).convert("RGB")) if os.path.exists(p) else None
    x0, y0 = t["px"]
    crop_ok = T is not None and bool((G[y0:y0 + T.shape[0], x0:x0 + T.shape[1]] == T).all())
    tiles[key] = {"file": "fid/lv/" + t["file"], "sha256": t["sha256"], "manifest_sha256_agrees": ok_sha, "equals_crop_of_pinned_guide": crop_ok,
                  "pilot": t["row"] <= 2 and t["col"] <= 2}
    if not (ok_sha and crop_ok):
        bad.append(key)
pil_changed = [k for k, v in pilot["tiles"].items() if tiles.get(k, {}).get("sha256") != v["sha256"]]
rec = {"_what": "BV2F PHASE 3' pins (%s): guide + ID + class COPIES and the 25 tiles of the 5 x 5, from LV %s" % (ruling, commit),
       "pinned_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "lv_commit": commit, **copies, "tiles": tiles,
       "tiles_bad": bad, "pilot_tiles_changed_vs_pilot_pins": pil_changed,
       "r_c9_189": "PASS: the 9 pilot tiles equal the pilot pins" if not pil_changed else "HALT: pilot tiles changed -> repaint (R-C9-189)"}
json.dump(rec, open(OUT + "/pins_ph3.json", "w"), indent=1)
print(json.dumps({"guide": copies["guide"]["sha256"][:12], "tiles": len(tiles), "bad": bad, "pilot_changed": pil_changed}))
# R-C9-295: with --allow <rects.json>, changed PILOT tiles are not a HALT here -- pilot_pins_check.py --allow judges them
# pixel-wise against the declared rectangles (run it next); without --allow, R-C9-189 as before
sys.exit(1 if (bad or (pil_changed and "--allow" not in sys.argv)) else 0)
