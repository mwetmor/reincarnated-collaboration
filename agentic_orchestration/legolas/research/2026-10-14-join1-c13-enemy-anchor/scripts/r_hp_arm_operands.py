#!/usr/bin/env python3
"""C-13: the J4b r_HP sensitivity-arm operand file (R2 and non-ladder), for binding by sha256.
Basis identical to the primary r_HP R1 (pack RB-A-anchor_r_hp = 40.54578785101241): GD BOARD trash body-weighted median
hp_lo / D2 normal-monster median hp_mid, equal weight per distinct (MonStats Id, alvl). Read-only; derived only from
committed C-13 files."""
import hashlib, json, statistics
from pathlib import Path
P = Path(__file__).resolve().parents[1]
sha = lambda f: hashlib.sha256((P / f).read_bytes()).hexdigest()
rt = json.loads((P / "ratio_table.json").read_text())
gd = rt["gd_role_split"]["weight_board_actors"]["trash"]["hp_lo"]
lad = json.loads((P / "d2_enemy_quantities.json").read_text())["rules"]
cla = json.loads((P / "d2_enemy_quantities_nonladder.json").read_text())["rules"]
def arm(rules, rk, colset):
    rows = sorted(rules[rk]["rows"], key=lambda r: r["hp_mid"])
    vals = [r["hp_mid"] for r in rows]
    med = statistics.median(vals)
    n = len(vals)
    mid_rows = rows[(n - 1) // 2: n // 2 + 1]
    return {"population_rule": rk, "d2_column_set": colset, "n_types": n, "d2_median_hp_mid": med,
            "median_rows": [{"id": r["id"], "alvl": r["alvl"], "hp_min": r["hp_min"], "hp_max": r["hp_max"], "hp_mid": r["hp_mid"]} for r in mid_rows],
            "gd_median_hp_lo": gd["median"], "r_hp": gd["median"] / med}
R1 = arm(lad, "R1_alvl85_all", "ladder/single-player L-HP(H)")
R2 = arm(lad, "R2_chaos_sanctum", "ladder/single-player L-HP(H)")
NL = arm(cla, "R1_alvl85_all", "non-ladder Battle.net HP(H)")
assert R1["r_hp"] == 40.54578785101241, R1["r_hp"]          # = pack RB-A-anchor_r_hp
assert R2["r_hp"] == 29.152836858187047, R2["r_hp"]         # = value gamora cites as registered (ADDENDUM-4 § 1.1)
assert R1["r_hp"] == rt["ratios_gd_over_d2"]["R1_alvl85_all"]["HP_trash_vs_normal"]["ratio_median"]
assert R2["r_hp"] == rt["ratios_gd_over_d2"]["R2_chaos_sanctum"]["HP_trash_vs_normal"]["ratio_median"]
doc = {
    "what": "JOIN-1 J4b r_HP sensitivity-arm operands (legolas C-13); binding instrument for the arms pack v5.1 does not carry",
    "statistic": "r_HP = median(GD BOARD trash hp_lo, body-weighted by n_actors_this_wave) / median(D2 normal-monster hp_mid, equal weight per distinct (MonStats Id, alvl)); D2 hp_mid = (MinHP(H)+MaxHP(H))/2 after MonLvl scaling at the area level (Hell, players-1)",
    "gd_numerator": {"value": gd["median"], "source": "gd_enemy_quantities.json per_cell hp_lo (oracle monster_stats.ehp_lookup_band_b, LO limb), BOARD population pm4o_oa_da.csv monster rows, role trash, weight n_actors_this_wave; via ratio_table.json gd_role_split"},
    "reference_primary": {"name": "R1 (pack RB-A-anchor_r_hp)", **R1},
    "operands": {
        "anchor_r_hp_R2": {**R2, "status": "CONFIRMED: equals the value gamora cites as registered (29.152836858187047)",
                            "derivation": "Chaos Sanctum (Levels.txt Id 108) nmon types doomknight3, fingermage3, megademon3 at alvl 85; median of 3 = doomknight3"},
        "anchor_r_hp_nonladder": {**NL, "status": "EXACT value (replaces the approximation R1/0.75 = 54.06105046801655)",
                                   "derivation": "R1 population (every Hell area at alvl 85, 70 types) re-run with the non-ladder MonLvl life column HP(H) in place of L-HP(H); median of 70 = mean of the 35th/36th rows"},
    },
    "grades": {"inputs": "DATAMINED (J-S7 pins re-verified by scripts/d2_enemy_anchor.py)", "scaling": "MODEL-VERIFIED (D2MOO CalculateMonsterStatsByLevel; Basin MonLvl)", "ratio": "INFERRED (as the primary)"},
    "blindness": "derived only from committed C-13 inputs; no J4b graded-margin result file was opened",
    "inputs_sha256": {f: sha(f) for f in ("ratio_table.json", "gd_enemy_quantities.json", "d2_enemy_quantities.json", "d2_enemy_quantities_nonladder.json", "scripts/d2_enemy_anchor.py")},
}
(P / "j4b_r_hp_arm_operands.json").write_text(json.dumps(doc, indent=1) + "\n")
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ("r_hp", "d2_median_hp_mid", "median_rows")} for k, v in doc["operands"].items()}, indent=1))
