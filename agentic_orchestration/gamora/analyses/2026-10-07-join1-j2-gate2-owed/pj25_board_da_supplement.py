"""P-J2-5 SUPPLEMENTARY READING (declared POST-HOC, after pj25.json; not a prediction and not the row of record).

pj25.json (the row as preregistered: DA from pm4o_oa_da.csv) covers 74 of the 196 (record, wave) pairs the player's
offense addressed in the 25 J-S8 cells; 122 are absent from that 95-row table (112 records never in it).
This reading takes DA from the mitigation board's own `DA` column (pm4l_mitigation_by_body.csv, the WORLD board
the oracle reads -- the pack's `summon_board`), for EVERY path pair, and reports p = probability_to_hit(3259, DA)
plus DA* (the DA at which p = 100 exactly, by bisection on the sealed equation).
Run (sealed kc2 on the path): PYTHONPATH=<sealed src> python3 <this> <dynamic dir> <out.json>
"""
import glob
import json
import sys

from reincarnated.simulation.kc2 import summon_offense as so, threat as th

dyn, out = sys.argv[1], sys.argv[2]
path = set()
for f in glob.glob(dyn + "/JOIN_*.json"):
    if not f.endswith(".cell.json"):
        path |= {(r, w) for r, w in json.load(open(f))["path"]}
board = so._full_board()
lo, hi = 0.0, 20000.0
for _ in range(200):
    m = (lo + hi) / 2
    if th.probability_to_hit(3259.0, m) >= 100.0:
        lo = m
    else:
        hi = m
per, missing = {}, []
for r, w in sorted(path):
    row = board.get((r, w))
    if row is None or row.get("DA") in (None, ""):
        missing.append([r, w])
        continue
    da = float(row["DA"])
    per[f"{r}|{w}"] = {"DA": da, "p": th.probability_to_hit(3259.0, da)}
mn = min(per, key=lambda k: per[k]["p"]) if per else None
rep = {"n_path": len(path), "n_with_board_DA": len(per), "n_missing_board_DA": len(missing), "missing": missing,
       "DA_star_p_eq_100": lo, "max_DA_on_path": max(v["DA"] for v in per.values()) if per else None,
       "min_p": per[mn]["p"] if mn else None, "min_p_at": mn,
       "n_p_below_100": sum(1 for v in per.values() if v["p"] < 100.0),
       "below_100": {k: v for k, v in per.items() if v["p"] < 100.0}}
open(out, "w").write(json.dumps(rep, indent=1, sort_keys=True))
print(json.dumps({k: rep[k] for k in rep if k not in ("missing", "below_100")}))
