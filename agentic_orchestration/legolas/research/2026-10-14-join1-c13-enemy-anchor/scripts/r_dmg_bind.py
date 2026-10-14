#!/usr/bin/env python3
"""C-13 stage 4 — bind r_DMG = reconciled GD per-hit (gd_damage_reconcile.json) / D2 per-hit (d2_skill_damage.json).
Pairing (as r_HP): GD BOARD trash (body-weighted) <-> D2 normal monsters, per rule R1..R4. Read-only."""
import hashlib, json, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
g = json.loads((P / "gd_damage_reconcile.json").read_text())
d = json.loads((P / "d2_skill_damage.json").read_text())
# Stage 5: the ENGINE-NATIVE block (E5 = record; composed with the salt-0 M0 run's own ThreatEngine folds, checked
# 684/688 against the dynamic capture) supersedes the stage-4 reconstruction `static_summaries` (re-loaded roster).
en = g["engine_native_static_summaries"]["weight_board_actors"]["trash"]
gdyn = g["dynamic"]["summaries"]["trash"]["per_landed_hit_raw_direct"]
gd = {"PRIMARY engine-native E5 max slot (body-weighted, 47 cells)": en["E5_max_slot"],
      "SENS engine-native E5 basic slot": en["E5_basic"],
      "SENS engine-native E5 mean damaging slot": en["E5_mean_damaging_slot"],
      "SENS dynamic per landed hit, use-weighted by oracle slot choice (1 salt, M0, 309 trash hits)": gdyn}
out = {"gd": gd, "rules": {}, "inputs_sha256": {f: hashlib.sha256((P / f).read_bytes()).hexdigest()
                                                 for f in ("gd_damage_reconcile.json", "d2_skill_damage.json")}}
for rk, R in d["rules"].items():
    best = R["dist_equal"]["best_hit_mid_all_attacks"]; mean = R["dist_equal"]["mean_hit_mid_all_damaging_attacks"]
    prim = gd["PRIMARY engine-native E5 max slot (body-weighted, 47 cells)"]
    dyn = gd["SENS dynamic per landed hit, use-weighted by oracle slot choice (1 salt, M0, 309 trash hits)"]
    bas = gd["SENS engine-native E5 basic slot"]
    gmean = gd["SENS engine-native E5 mean damaging slot"]
    out["rules"][rk] = {
        "d2_best": best, "d2_mean": mean,
        "r_DMG_primary": prim["median"] / best["median"],
        "r_DMG_primary_iqr_ratio": [prim["p25"] / best["p25"], prim["p75"] / best["p75"]],
        "sens_mean_attack (static max-slot / D2 mean)": prim["median"] / mean["median"],
        "sens_mean_vs_mean (E5 mean damaging slot / D2 mean)": gmean["median"] / mean["median"],
        "sens_use_weighted (dynamic / D2 mean)": dyn["median"] / mean["median"],
        "sens_use_weighted_iqr_ratio": [dyn["p25"] / mean["p25"], dyn["p75"] / mean["p75"]],
        "sens_basic_swing (static basic / D2 best)": bas["median"] / best["median"],
    }
(P / "r_dmg.json").write_text(json.dumps(out, indent=1))
for rk, v in out["rules"].items():
    print(rk, "r_DMG %.1f [%.1f-%.1f]" % (v["r_DMG_primary"], *v["r_DMG_primary_iqr_ratio"]),
          "| maxslot/D2mean %.1f | mean/mean %.1f | use-weighted %.1f [%.1f-%.1f] | basic/D2best %.1f" % (
              v["sens_mean_attack (static max-slot / D2 mean)"], v["sens_mean_vs_mean (E5 mean damaging slot / D2 mean)"],
              v["sens_use_weighted (dynamic / D2 mean)"],
              *v["sens_use_weighted_iqr_ratio"], v["sens_basic_swing (static basic / D2 best)"]))
