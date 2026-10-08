#!/usr/bin/env python3
"""BV2F LV: placed_fit_bv2art.json -- every placed instance of the ART level AS BUILT, from the running scene
(barrow_full/godot/tools/bv2f/export_fit.gd, BV2F_VARIANT=art; heavy lock), summarised per slot (P6' / principle 3:
one uniform scale per real model, anisotropy <= 1.10; procedural pieces at true dimensions are N/A).

    python3 fid/lv/tools/lv_placed_fit.py          (runs export_fit.gd, then writes fid/lv/placed_fit_bv2art.json)
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
C9 = os.path.normpath(os.path.join(LV, "..", "..", ".."))
BF = os.path.join(C9, "barrow_full", "godot")
LOCK = os.path.join(HERE, "lv_guard_lock.py")          # R-C9-226: heavy lock + wall-clock timeout + quit on a script error
GODOT = os.environ.get("GODOT", "/Applications/Godot.app/Contents/MacOS/Godot")


def main():
    raw = os.path.join(LV, "art", "export_fit_raw.json")
    if "--no-run" not in sys.argv:
        if shutil.disk_usage("/System/Volumes/Data").free / 2 ** 30 < 21:
            sys.exit("[fit] HALT: disk < 21 GiB")
        rc = subprocess.run(["python3", LOCK, "C-9", "--", GODOT, "--path", BF, "--resolution", "640x360", "--script", "tools/bv2f/export_fit.gd", "--", raw],
                            cwd=BF, env=dict(os.environ, BV2F_VARIANT="art"), capture_output=True, text=True)
        if rc.returncode != 0 or not os.path.exists(raw):
            sys.exit("[fit] export_fit.gd rc=%d\n%s" % (rc.returncode, rc.stdout[-2000:]))
    d = json.load(open(raw))
    prev = json.load(open(os.path.join(LV, "placed_fit_bv2art.json")))
    per = {}
    for r in d["instances"]:
        slot = r.get("slot", r["instance"])
        p = per.setdefault(slot, {"instances": 0, "kind": r["kind"], "anisotropy_max": 1.0, "over_1_10": 0})
        p["instances"] += 1
        a = float(r.get("anisotropy_max_over_min", 1.0))
        p["anisotropy_max"] = round(max(p["anisotropy_max"], a), 4)
        if r["kind"] == "box" and a > 1.10:
            p["over_1_10"] += 1
        if r["kind"] != p["kind"]:
            p["kind"] = "mixed: " + ", ".join(sorted({p["kind"].replace("mixed: ", ""), r["kind"]}))
    out = {"_what": prev["_what"].replace("stair treads)", "stair treads, the cave hood)"), "layout": prev["layout"],
           "per_slot": dict(sorted(per.items())), "instances": d["instances"], "r186_presence_fix": prev.get("r186_presence_fix"),
           "r188_189": "the sea-cave route: cliff faces cliff_2/3/4 not placed (the shelf and the cave hood stand there); the cave hood = 4 procedural rock "
                       "boxes at true size (in slot cliff_faces, kind procedural_cave_hood); the stair = 27 procedural treads 5.5 m wide; the hall's +X "
                       "gable end closed by a plank panel riding the hall's own uniform scale"}
    json.dump(out, open(os.path.join(LV, "placed_fit_bv2art.json"), "w"), indent=1)
    box = [r for r in d["instances"] if r["kind"] == "box"]
    print("[fit] %d instances; %d real-model boxes; max anisotropy %.4f; over 1.10: %d" % (
        len(d["instances"]), len(box), max(float(r.get("anisotropy_max_over_min", 1)) for r in box), sum(p["over_1_10"] for p in per.values())))


if __name__ == "__main__":
    main()
