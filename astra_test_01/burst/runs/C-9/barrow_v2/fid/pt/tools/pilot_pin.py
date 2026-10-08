#!/usr/bin/env python3
"""BV2F PT: PIN the pilot guide for a (re)paint -- the pinned COPY of LV's guide (so LV's later re-renders cannot reach the
paint) and the 9 pilot tiles (cols 0-2, rows 0-2), each checked against LV's guide_manifest AT A GIVEN COMMIT.
    python3 fid/pt/tools/pilot_pin.py <lv_commit> <ruling> [--copy fid/pt/pilot/guide_art_pinned_v2.png]
The previous pins.json is kept as pins_<prev tag>.json by the caller. Check afterwards: pilot_pins_check.py."""
import datetime, hashlib, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO = os.path.abspath(os.path.join(FID, "..", "..", "..", "..", "..", ".."))
commit, ruling = sys.argv[1], sys.argv[2]
copy_rel = sys.argv[sys.argv.index("--copy") + 1] if "--copy" in sys.argv else "fid/pt/pilot/guide_art_pinned_v2.png"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rel_fid = os.path.relpath(FID, REPO)
m = json.loads(subprocess.check_output(["git", "-C", REPO, "show", "%s:%s/lv/guide_art/guide_manifest.json" % (commit, rel_fid)]))
LV = os.path.join(FID, "lv")
bad = [k for k in ("guide", "ids", "class") if sha(os.path.join(LV, m[k]["file"])) != m[k]["sha256"]]
assert not bad, "LV's working files differ from the manifest at %s: %s" % (commit, bad)
g = os.path.join(LV, m["guide"]["file"])
dst = os.path.join(FID, copy_rel.replace("fid/", "", 1))
shutil.copyfile(g, dst)
assert sha(dst) == m["guide"]["sha256"]
G = np.asarray(Image.open(dst).convert("RGB"))
cw, ch = m["canvas"]
sx, sy = m["stride"]
tiles = {}
for t in m["tiles"]:
    if t["row"] > 2 or t["col"] > 2:
        continue
    p = os.path.join(LV, t["file"])
    assert sha(p) == t["sha256"], "tile %s differs from the manifest at %s" % (t["file"], commit)
    T = np.asarray(Image.open(p).convert("RGB"))
    x0, y0 = t["px"]
    crop = G[y0:y0 + T.shape[0], x0:x0 + T.shape[1]]
    tiles["%d_%d" % (t["col"], t["row"])] = {"file": "fid/lv/" + t["file"], "sha256": t["sha256"], "manifest_sha256_agrees": True,
                                             "equals_crop_of_pinned_guide": bool(crop.shape == T.shape and (crop == T).all())}
# R-C9-258 standing practice: the ID and class renders are pinned as COPIES with every guide (DEV-28 and the class masks read them)
side = {}
for k in ("ids", "class"):
    d2 = dst.replace("guide_art_pinned", "%s_art_pinned" % k)
    assert d2 != dst, "the --copy name must contain 'guide_art_pinned'"
    shutil.copyfile(os.path.join(LV, m[k]["file"]), d2)
    assert sha(d2) == m[k]["sha256"]
    side[k] = os.path.relpath(d2, os.path.dirname(FID))
pins = {"_what": "BV2F PILOT REPAINT pins (%s): the guide the pilot cfg paints from (a pinned COPY of LV's guide at %s) and the 9 pilot tiles (cols 0-2, rows 0-2) as LV published them. A changed pilot tile in LV's guide after this = paint from the newer tiles. Check: python3 fid/pt/tools/pilot_pins_check.py" % (ruling, commit),
        "pinned_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "lv_commit": commit,
        "guide": {"pinned_copy": copy_rel, "source": "fid/lv/" + m["guide"]["file"], "sha256": m["guide"]["sha256"],
                  "manifest_sha256": m["guide"]["sha256"], "px": list(G.shape[1::-1])},
        "ids": {"pinned_copy": side["ids"], "source": "fid/lv/" + m["ids"]["file"], "sha256": m["ids"]["sha256"]},
        "class": {"pinned_copy": side["class"], "source": "fid/lv/" + m["class"]["file"], "sha256": m["class"]["sha256"]},
        "tiles": tiles}
json.dump(pins, open(os.path.join(FID, "pt", "pilot", "pins.json"), "w"), indent=1)
print(json.dumps({"guide": m["guide"]["sha256"][:12], "tiles": {k: [v["sha256"][:12], v["equals_crop_of_pinned_guide"]] for k, v in tiles.items()}}))
