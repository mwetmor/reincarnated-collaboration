#!/usr/bin/env python3
"""C-13 stage 4 — bind r_DMG = reconciled GD per-hit (gd_damage_reconcile.json) / D2 per-hit (d2_skill_damage.json).
Pairing (as r_HP): GD BOARD trash (body-weighted) <-> D2 normal monsters, per rule R1..R4. Read-only."""
import hashlib, json, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
g = json.loads((P / "gd_damage_reconcile.json").read_text())
d = json.loads((P / "d2_skill_damage.json").read_text())
gs = g["static_summaries"]["weight_board_actors"]["trash"]
gdyn = g["dynamic"]["summaries"]["trash"]["per_landed_hit_raw_direct"]
gd = {"PRIMARY static record max-slot (body-weighted, 43 cells)": gs["record_max_slot"],
      "SENS static record basic swing (16 cells with a basic swing)": gs["record_basic_hit"],
      "SENS dynamic per landed hit, use-weighted by oracle slot choice (1 salt, M0, 425 trash hits)": gdyn}
out = {"gd": gd, "rules": {}, "inputs_sha256": {f: hashlib.sha256((P / f).read_bytes()).hexdigest()
                                                 for f in ("gd_damage_reconcile.json", "d2_skill_damage.json")}}
for rk, R in d["rules"].items():
    best = R["dist_equal"]["best_hit_mid_all_attacks"]; mean = R["dist_equal"]["mean_hit_mid_all_damaging_attacks"]
    prim = gd["PRIMARY static record max-slot (body-weighted, 43 cells)"]
    dyn = gd["SENS dynamic per landed hit, use-weighted by oracle slot choice (1 salt, M0, 425 trash hits)"]
    bas = gd["SENS static record basic swing (16 cells with a basic swing)"]
    out["rules"][rk] = {
        "d2_best": best, "d2_mean": mean,
        "r_DMG_primary": prim["median"] / best["median"],
        "r_DMG_primary_iqr_ratio": [prim["p25"] / best["p25"], prim["p75"] / best["p75"]],
        "sens_mean_attack (static max-slot / D2 mean)": prim["median"] / mean["median"],
        "sens_use_weighted (dynamic / D2 mean)": dyn["median"] / mean["median"],
        "sens_use_weighted_iqr_ratio": [dyn["p25"] / mean["p25"], dyn["p75"] / mean["p75"]],
        "sens_basic_swing (static basic / D2 best)": bas["median"] / best["median"],
    }
(P / "r_dmg.json").write_text(json.dumps(out, indent=1))
for rk, v in out["rules"].items():
    print(rk, "r_DMG %.1f [%.1f-%.1f]" % (v["r_DMG_primary"], *v["r_DMG_primary_iqr_ratio"]),
          "| mean-attack %.1f | use-weighted %.1f [%.1f-%.1f] | basic %.1f" % (
              v["sens_mean_attack (static max-slot / D2 mean)"], v["sens_use_weighted (dynamic / D2 mean)"],
              *v["sens_use_weighted_iqr_ratio"], v["sens_basic_swing (static basic / D2 best)"]))
