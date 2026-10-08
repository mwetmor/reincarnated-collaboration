#!/usr/bin/env python3
"""BV2F PT: PIN the pilot LEVEL for a (re)build -- LV's art level AS COMMITTED at <lv_commit> into
barrow_full/godot/data/bv2f/<set>/level/ (the scene reads ONLY this when BV2F_PILOT=<tag>), as the R-C9-245 pin did by hand:
  level.json            from git at the commit (the working copy must equal it)
  every file level.json names (carved_*.f32, terrain_h / walk, classes_png.bin) from data/bv2f/art/, each checked against
                        the sha256 level.json records for it where it records one
  classes.png           from data/bv2f/art/ (sha recorded in PIN.json)
  stair_treads.json, reed_beds.json   from fid/lv/art/ AS COMMITTED at the commit
    python3 fid/pt/tools/pilot_level_pin.py <lv_commit> <set dir name, e.g. pilot_rp4> <ruling>"""
import hashlib, json, os, re, shutil, subprocess, sys

C9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
REPO = "/Users/admin/Games/reincarnated-collaboration"
REL = "astra_test_01/burst/runs/C-9"
commit, setname, ruling = sys.argv[1:4]
ART = C9 + "/barrow_full/godot/data/bv2f/art"
DST = C9 + "/barrow_full/godot/data/bv2f/%s/level" % setname
sha = lambda b: hashlib.sha256(b).hexdigest()
show = lambda p: subprocess.check_output(["git", "-C", REPO, "show", "%s:%s/%s" % (commit, REL, p)])
os.makedirs(DST, exist_ok=False)
lvl = show("barrow_full/godot/data/bv2f/art/level.json")
assert open(ART + "/level.json", "rb").read() == lvl, "LV's working level.json != the commit"
open(DST + "/level.json", "wb").write(lvl)
files = {"level.json": {"sha256": sha(lvl), "source": "git %s" % commit}}
txt = lvl.decode()
names = sorted(set(re.findall(r'"([A-Za-z0-9_]+\.(?:f32|bin))"', txt)))
for n in names:
    b = open(os.path.join(ART, n), "rb").read()
    # the sha level.json records in the same object (the first "sha256" after the name inside its braces), if any
    i = txt.index('"%s"' % n)
    j = txt.find("}", i)
    m = re.search(r'"sha256":\s*"([0-9a-f]{64})"', txt[i:j])
    ok = None if m is None else (m.group(1) == sha(b))
    assert ok is not False, "%s: sha %s != level.json's %s" % (n, sha(b)[:12], m.group(1)[:12])
    open(os.path.join(DST, n), "wb").write(b)
    files[n] = {"sha256": sha(b), **({} if ok is None else {"recorded_sha_ok": True})}
shutil.copyfile(ART + "/classes.png", DST + "/classes.png")
files["classes.png"] = {"sha256": sha(open(DST + "/classes.png", "rb").read())}
for n in ("stair_treads.json", "reed_beds.json"):
    b = show("barrow_v2/fid/lv/art/" + n)
    open(os.path.join(DST, n), "wb").write(b)
    files[n] = {"sha256": sha(b), "source": "git %s fid/lv/art/%s" % (commit, n)}
json.dump({"_what": "%s: pilot level, pinned from LV %s" % (ruling, commit), "lv_commit": commit, "files": files},
          open(DST + "/PIN.json", "w"), indent=1)
print(json.dumps({k: v["sha256"][:12] for k, v in files.items()}))
