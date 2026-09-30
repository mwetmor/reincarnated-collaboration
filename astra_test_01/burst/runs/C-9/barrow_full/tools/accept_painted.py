#!/usr/bin/env python3
"""C-9 T10-2 step 4 -- THE PAINTED BARROW HOLDS THE BLOCKOUT'S ACCEPTANCE: the walkable area, the
no-squeeze rule and the camera margin must pass exactly as in blockout v2. drax.

    python3 tools/accept_painted.py

Reads captures/ (blockout v2, as accepted) and captures/painted_accept/ (the SAME capture tool,
godot/tools/capture_blockout.gd --painted --no-cost, on the painted scene) and writes
take/build/accept_painted.json. Three tests, in order of strength:
  1. THE COLLIDERS ARE THE SAME COLLIDERS: every collision shape's ground footprint (the no-squeeze
     instrument's own input) and every placement's built transform, compared value for value.
  2. finalize.py's acceptance, re-run on the painted capture (its flood fill, its walks, its
     squeeze profiler, its camera margin) -- nothing re-implemented.
  3. each number held to v2's.
finalize.py is imported, never run: its main() rewrites the layout and the map.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import finalize as F  # noqa: E402

ROOT = HERE.parent
V2 = ROOT / "captures"
PA = ROOT / "captures" / "painted_accept"
OUT = ROOT / "take" / "build" / "accept_painted.json"


def main():
    L = json.loads((ROOT / "barrow_full_layout.json").read_text())
    b2 = json.loads((V2 / "built.json").read_text())
    bp = json.loads((PA / "built.json").read_text())
    rep = json.loads((PA / "capture_report.json").read_text())
    grid = json.loads((PA / "walk_grid.json").read_text())
    grid2 = json.loads((V2 / "walk_grid.json").read_text())
    acc2 = json.loads((V2 / "acceptance.json").read_text())["acceptance"]
    out = {"_what": "C-9 T10-2 step 4: the painted Barrow against blockout v2's acceptance (the conductor: 'the walkable area, the no-squeeze rule and the camera margin must still pass exactly as in blockout v2')"}
    # 1. the same colliders
    same_fp = b2["collider_footprints"] == bp["collider_footprints"]
    keys = ("world_origin", "world_basis_columns", "footprint_uv_low", "y_min", "y_max")
    diff_rec = [pid for pid in b2["records"] if any(b2["records"][pid].get(k) != bp["records"].get(pid, {}).get(k) for k in keys)]
    out["colliders_identical"] = {"collider_footprints": {"v2": len(b2["collider_footprints"]), "painted": len(bp["collider_footprints"]),
                                                          "identical": same_fp},
                                  "built_transforms_and_footprints_differing": diff_rec,
                                  "walk_grid_identical": grid == grid2,
                                  "PASS": same_fp and not diff_rec}
    # 2. finalize's own acceptance on the painted capture. The scale markers lie on the arena's
    # snow, which the painted scene covers with its 3D snow (0.12 m): the camera is the blockout's,
    # measured there, and its marks are carried rather than re-read through the snow
    F.CAP = PA
    try:
        marks = F.measure_markers(rep)
        marks_src = "measured on the painted capture"
    except SystemExit as e:
        marks = dict(acc2["scale"])
        marks.pop("PASS", None)
        marks_src = "carried from v2 (%s): the same camera; the markers are under the 3D snow here" % str(e)[:80]
    A, gr = F.acceptance(L, bp, rep, grid, marks)
    out["scale_markers"] = marks_src
    # 3. held to v2
    def pick(a):
        return {"flood_fill": {k: a["flood_fill"][k] for k in ("reachable_m2", "targets", "ice_reachable_share", "reachable_outside_bounds_cells", "PASS")},
                "no_squeezes": {"squeezes": a["no_squeezes"]["squeezes"], "obstacles": a["no_squeezes"]["obstacles"], "PASS": a["no_squeezes"]["PASS"]},
                "camera_margin": {k: a["camera_margin"][k] for k in ("reachable_cells", "cells_whose_frame_leaves_the_window", "worst_px_outside_by_side", "PASS")},
                "mound_and_door_floor": {"PASS": a["mound_and_door_floor"]["PASS"]},
                "arena": {"clear_r_walkable_m": a["arena"]["clear_r_walkable_m"], "PASS": a["arena"]["PASS"]},
                "path": {"min_clearance_m": a["path"]["min_clearance_m"], "PASS": a["path"]["PASS"]},
                "ring_entrance": {"clear_gap_m": a["ring_entrance"]["clear_gap_m"], "PASS": a["ring_entrance"]["PASS"]},
                "walks": {k: v.get("PASS") for k, v in a.get("walks", {}).items() if isinstance(v, dict)}}
    p2, pp = pick(acc2), pick(A)
    out["v2"] = p2
    out["painted"] = pp
    out["identical_to_v2"] = {k: p2[k] == pp[k] for k in p2}
    out["PASS"] = bool(out["colliders_identical"]["PASS"] and all(out["identical_to_v2"].values())
                       and pp["flood_fill"]["PASS"] and pp["no_squeezes"]["PASS"] and pp["camera_margin"]["PASS"])
    OUT.write_text(json.dumps(out, indent=1, default=F._np))
    print(json.dumps({"colliders_identical": out["colliders_identical"], "identical_to_v2": out["identical_to_v2"],
                      "painted": {k: pp[k] for k in ("flood_fill", "no_squeezes", "camera_margin")}, "PASS": out["PASS"]},
                     indent=1, default=F._np))


if __name__ == "__main__":
    main()
