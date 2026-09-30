#!/usr/bin/env python3
"""C-9 T10-1e: make room in kit/ for the re-issue, without losing the first issue.

    python3 67_kit_migrate.py

The re-issued rocks, stump and skull take the plain names, because the plain names are
what a scene file will ask for. The first issue is not deleted: its numbers are the
evidence that the re-issue was needed (rocks 0.53 m across against a brief of 1.10; the
skull on its antler tips). So each first-issue asset moves to kit/retired/ under a
versioned name and keeps its manifest entry under that name, with its status saying why.

Idempotent: an asset already migrated is left alone, so a re-run cannot move a NEW build
into retired/ by mistake -- the one failure this step exists to avoid.
"""
import json
import pathlib
import shutil

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE / "kit"
RET = KIT / "retired"
MOVES = {
    # old key -> (new key, file now, file after, status, why)
    "rocks": ("rocks_v1", KIT / "rocks.glb", RET / "rocks_v1.glb", "superseded",
              "first issue: the sheet stacked the three rocks into one pile, 0.53 m across "
              "against a brief of 1.10; replaced by the T10K-A2 rocks"),
    "stump": ("stump_v1", KIT / "stump.glb", RET / "stump_v1.glb", "superseded",
              "first issue: a tall stump with a tight root ball, roots 0.53 m across "
              "against 1.20, ~40% of the root fingers lost in the build; replaced by the "
              "T10K-A2 stump"),
    "skull": ("skull_upright", RET / "skull.glb", RET / "skull_upright.glb", "retired",
              "retired on POSE: an elk skull balanced on its antler tips reads as a "
              "generator tell; replaced by the T10K-D skull lying on its side"),
}


def main() -> None:
    f = KIT / "kit_assets.json"
    doc = json.loads(f.read_text())
    mods = doc["models"]
    RET.mkdir(exist_ok=True)
    for old, (new, src, dst, status, why) in MOVES.items():
        if new in mods:
            print("%-6s already migrated to %s" % (old, new))
            continue
        e = mods.pop(old)
        if src.exists():
            shutil.move(str(src), str(dst))
        e["status"] = status
        e["retired_because"] = why
        e["glb"] = "res://models/barrow/kit/retired/%s" % dst.name
        mods[new] = e
        print("%-6s -> %-14s %s  (%s)" % (old, new, dst.relative_to(HERE), status))
    f.write_text(json.dumps(doc, indent=1) + "\n")


if __name__ == "__main__":
    main()
