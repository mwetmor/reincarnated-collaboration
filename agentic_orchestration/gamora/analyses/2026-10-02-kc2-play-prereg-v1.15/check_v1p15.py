#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.15 · the law (a) verdict on the two restated rows, from audit_v1p15.py's five outputs.

Run: python3 check_v1p15.py [--ingest <scratch dir>]  -> results_v1p15.json; exit 0 iff completeness holds on 25/25
(a STOP otherwise). The verdict on each row is printed; a FAIL is reported, never adjusted.
"""
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
if len(sys.argv) > 2 and sys.argv[1] == "--ingest":
    (HERE / "audit_out").mkdir(exist_ok=True)
    for a in ARMS:
        (HERE / "audit_out" / f"audit_{a}.json.gz").write_bytes(
            gzip.compress((Path(sys.argv[2]) / f"audit_{a}.json").read_bytes(), mtime=0))
D = {a: json.loads(gzip.decompress((HERE / "audit_out" / f"audit_{a}.json.gz").read_bytes())) for a in ARMS}
cells, stop = {}, []
for a in ARMS:
    for s in range(5):
        x = D[a]["salts"][str(s)]
        if not x["complete"]:
            stop.append(f"{a}|{s}")
        t = x["t30"]
        fails30 = {k: v for k, v in t.items() if k.startswith("fail:")}
        t29 = x["t29"]
        fails29 = {k: v for k, v in t29.items() if k.startswith("FAIL")}
        inst = x["t29_instances"]
        cells[f"{a}|{s}"] = {
            "complete": x["complete"], "terminal": next((w for w, o, _ in x["waves"] if o == "player_death"), "cleared_w160"),
            "TA-X-30(a')": {"steps_checked": t.get("n_checked", 0), "unclipped": t.get("n_unclipped", 0),
                            "clipped": t.get("n_clipped", 0), "held": t.get("n_held", 0),
                            "waypoint": t.get("n_waypoint_steps", 0), "fails": fails30,
                            "pet_steps": t.get("pet_steps", 0), "pet_no_travel_by_law": t.get("pet_steps_no_travel_by_law", 0),
                            "pet_moved_exact": t.get("pet_moved_law_exact", 0) + t.get("pet_moved_law_exact_ghost(next-tick read)", 0),
                            "pet_moved_clipped_shorter": t.get("pet_moved_clipped_shorter", 0),
                            "pet_moved_unobserved": t.get("pet_moved_by_law_but_unobserved", 0),
                            "op_classes": x["op_classes"], "holds": t.get("n_fail", 0) == 0 and t.get("n_checked", 0) > 0},
            "TA-X-30(b) R-G4-V311": {"n_bodies_halted_beyond_d_engage": x["R-G4-V311 n_bodies_halted_beyond_d_engage"],
                                     "arena_armed_waves": x["arena_armed_waves"], "arena_clamp_calls": x["arena_clamp_calls"],
                                     "vacuous": x["arena_armed_waves"] == 0,
                                     "holds": x["R-G4-V311 n_bodies_halted_beyond_d_engage"] == 0},
            "TA-X-29(b')": {"families": {k: v for k, v in t29.items() if not k.startswith("FAIL") and k != "z5_form_differs"},
                            "rows_where_the_Z5_form_differs": t29.get("z5_form_differs", 0),
                            "instances": inst, "fails": fails29,
                            "holds": not fails29 and sum(v for k, v in t29.items() if k.startswith(("instant:", "dot:"))) > 0
                            and set(inst) <= {"instant|limb=LO|divisor=True", "dot|limb=LO|divisor=True"}},
            "examples": {"t30": x["t30_fail_examples"], "t29": x["t29_fail_examples"]}}
allc = list(cells.values())
agg = lambda key, sub: sum(c[key][sub] for c in allc)
R = {"cells": cells, "STOP": stop, "constants": D["W1"]["constants"],
     "TA-X-30(a')": {"holds": all(c["TA-X-30(a')"]["holds"] for c in allc),
                     "n_pass": sum(c["TA-X-30(a')"]["holds"] for c in allc),
                     "steps_checked": agg("TA-X-30(a')", "steps_checked"), "unclipped": agg("TA-X-30(a')", "unclipped"),
                     "clipped": agg("TA-X-30(a')", "clipped"), "held": agg("TA-X-30(a')", "held"),
                     "waypoint": agg("TA-X-30(a')", "waypoint"),
                     "pet_steps": agg("TA-X-30(a')", "pet_steps"), "pet_no_travel_by_law": agg("TA-X-30(a')", "pet_no_travel_by_law"),
                     "pet_moved_exact": agg("TA-X-30(a')", "pet_moved_exact"),
                     "pet_moved_clipped_shorter": agg("TA-X-30(a')", "pet_moved_clipped_shorter"),
                     "pet_moved_unobserved": agg("TA-X-30(a')", "pet_moved_unobserved"),
                     "op_classes": dict(sum((Counter(c["TA-X-30(a')"]["op_classes"]) for c in allc), Counter()))},
     "TA-X-30(b)": {"holds": all(c["TA-X-30(b) R-G4-V311"]["holds"] for c in allc),
                    "n_pass": sum(c["TA-X-30(b) R-G4-V311"]["holds"] for c in allc),
                    "vacuous_cells": [k for k, c in cells.items() if c["TA-X-30(b) R-G4-V311"]["vacuous"]]},
     "TA-X-29(b')": {"holds": all(c["TA-X-29(b')"]["holds"] for c in allc),
                     "n_pass": sum(c["TA-X-29(b')"]["holds"] for c in allc),
                     "families": dict(sum((Counter(c["TA-X-29(b')"]["families"]) for c in allc), Counter())),
                     "rows_where_the_Z5_form_differs": sum(c["TA-X-29(b')"]["rows_where_the_Z5_form_differs"] for c in allc),
                     "instances": dict(sum((Counter(c["TA-X-29(b')"]["instances"]) for c in allc), Counter()))}}
(HERE / "results_v1p15.json").write_text(json.dumps(R, indent=1, sort_keys=True, default=str) + "\n")
print("STOP", stop)
for k in ("TA-X-30(a')", "TA-X-30(b)", "TA-X-29(b')"):
    print(k, json.dumps(R[k], default=str)[:900])
sys.exit(2 if stop else 0)
