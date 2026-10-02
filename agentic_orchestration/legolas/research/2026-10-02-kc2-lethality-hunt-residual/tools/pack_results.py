"""Pack compact per-arm results (summary, paired delta vs control, per-wave, instruments) for commit."""
import glob
import json
import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(__file__))
from analyse_geometry import summarise as geo  # noqa: E402
from analyse_timing import referent  # noqa: E402

H = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
ref = referent()
ctrl = json.load(open(f"{H}/out/CTRL2.json"))
C = ctrl["summary"]["per_salt_ratio"]
table = []
for p in sorted(glob.glob(f"{H}/out/*.json")):
    name = os.path.basename(p)[:-5]
    if name in ("CTRL",) or name.startswith(("geom", "prediction", "swing", "perwave")) or name.endswith("_timing"):
        continue
    d = json.load(open(p))
    if "summary" not in d:
        continue
    s = d["summary"]
    x = s["per_salt_ratio"]
    dd = [a - b for a, b in zip(x, C)]
    m = st.mean(dd)
    se = st.stdev(dd) / math.sqrt(len(dd)) if len(set(dd)) > 1 else 0.0
    fh = {}
    for w in range(151, 161):
        v = [r["ext"]["first_hit"]["t"] for R in d["rows"].values() for r in R
             if r["wave"] == w and r["ext"]["first_hit"]]
        fh[w] = {"oracle_median_s": round(st.median(v), 3) if v else None,
                 "referent_first_decrement_ge100_s": ref[w]["first_dec_ge100"]}
    g = geo(p)
    rec = {"arm": d["arm"], "arm_doc": d.get("arm_doc"), "artifact_class": d["artifact_class"],
           "salts": d["salts"], "summary": s, "fold_reports": d.get("fold_reports"),
           "paired_delta_vs_control": {"mean": round(m, 4), "ci95": [round(m - 2.093 * se, 4), round(m + 2.093 * se, 4)]},
           "first_hit_by_wave": fh, "standoff": g}
    if d["arm"] == "ROSTER" or d["arm"].endswith("|R"):
        y = x[1:]
        rec["salts_1_19_redrawn_rosters"] = {"mean": round(st.mean(y), 4), "sd": round(st.stdev(y), 4),
                                             "min": min(y), "max": max(y)}
    json.dump(rec, open(f"{OUT}/arm_{name.replace('|', '_R').replace('+', '_')}.json", "w"), indent=1, default=str)
    table.append({"arm": d["arm"], "ratio": s["ratio_vs_referent"], "delta": rec["paired_delta_vs_control"],
                  "mean_first_death_wave": s["mean_leg_a_wave"], "first_death_in_160": s["n_first_death_in_160"],
                  "survive_160": s["n_survive_160"], "leg_a_terminals": s["leg_a_terminals"],
                  "t_into_wave_s": s["leg_a_t_into_wave_s"], "redrawn": rec.get("salts_1_19_redrawn_rosters")})
json.dump(table, open(f"{OUT}/results_table.json", "w"), indent=1)
print(len(table), "arms packed")
