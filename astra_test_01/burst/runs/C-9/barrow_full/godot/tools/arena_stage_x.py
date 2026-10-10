#!/usr/bin/env python3
"""C-9 BV2F ARENA (R-C9-366): stage a VARIANT JOIN-1 pack root (e.g. gd-eor-warlord-eor4x) for the arena, with
kc2_play/tools/stage_join1.py's OWN functions (imported read-only; reincarnated-godot is not written): the same sha check,
alpha-union crop, 2:1 premultiplied reduction, strip packing and per-kit index.json -- written to the arena's gitignored
godot/kc2/art_x/<kit>/ instead of kc2_play/art/join1/.
usage: python3 tools/arena_stage_x.py gd-eor-warlord-eor4x"""
import importlib.util, json, os, sys
SRC = "/Users/admin/Games/reincarnated-godot/kc2_play/tools/stage_join1.py"
spec = importlib.util.spec_from_file_location("stage_join1", SRC)
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kc2", "art_x")
S.OUT = OUT
kit = sys.argv[1]
root = os.path.join(S.PACKS, kit)
mi_path = os.path.join(root, "matrix_index.json")
mi = json.load(open(mi_path))
assert mi.get("complete") == mi.get("expected"), (mi.get("complete"), mi.get("expected"))
assert list(mi["camera"]["anchor_px"]) == list(S.ANCHOR)
states, jobs = {}, []
for st, sv in mi["states"].items():
    states[st] = {k: sv.get(k) for k in ("kind", "role", "frames", "t_s", "release_index", "release_s", "hold_last",
                                         "stride_m_per_cycle", "skill")}
    states[st]["duration_s"] = sv["clip"]["duration_s"]
    for d in S.DIRS:
        cid = "%s/%s" % (st, d)
        c = mi["cells"][cid]
        assert c.get("status") == "COMPLETE", cid
        files = [(os.path.join(root, "cells", st, d, f["name"]), f["sha256"]) for f in c["files"]]
        jobs.append({"kind": "cell", "kit": kit, "key": "%s|%s" % (kit, cid), "files": files, "anchor": S.ANCHOR,
                     "scale": S.STAGE_SCALE, "index_bbox": c.get("alpha_union_bbox"),
                     "out": os.path.join(OUT, kit, "%s_%s.png" % (st, d))})
meta = {"kit": kit, "pack_root": root, "matrix_index_sha256": S.sha256_file(mi_path),
        "h_model_m": (mi.get("source") or {}).get("h_model_m"), "ppm_render": mi["camera"]["ppm_render"],
        "stage_scale": S.STAGE_SCALE, "directions": S.DIRS,
        "facing_ground_bearing_deg": mi["directions"]["facing_ground_bearing_deg"], "states": states, "cells": {}}
for j in jobs:
    r = S.stage_cell(j)
    if "error" in r:
        sys.exit("REFUSE %s: %s" % (r["key"], r["error"]))
    meta["cells"][r["key"].split("|", 1)[1]] = r["rec"]
os.makedirs(os.path.join(OUT, kit), exist_ok=True)
json.dump(meta, open(os.path.join(OUT, kit, "index.json"), "w"), indent=1, sort_keys=True)
print("staged %s: %d cells -> %s" % (kit, len(jobs), os.path.join(OUT, kit)))
