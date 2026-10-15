#!/usr/bin/env python3
"""C-13 non-ladder r_HP arm (owed per gamora J4b ADDENDUM-4 § 1.1 / NO-VERDICT-ARMS § 3b).
Same basis as the primary r_HP (ratio_table.json R1 HP_trash_vs_normal): GD BOARD trash body-weighted median hp_lo
(gd_enemy_quantities.json via ratio_table.json gd_role_split) / D2 R1 normal-monster median hp_mid, equal weight per
distinct (MonStats Id, alvl). Only the D2 HP column set changes: HP(H) (non-ladder) instead of L-HP(H)."""
import hashlib, json
from pathlib import Path
P = Path(__file__).resolve().parents[1]
rt = json.loads((P / "ratio_table.json").read_text())
prim = rt["ratios_gd_over_d2"]["R1_alvl85_all"]["HP_trash_vs_normal"]
gd = rt["gd_role_split"]["weight_board_actors"]["trash"]["hp_lo"]
nl = json.loads((P / "d2_enemy_quantities_nonladder.json").read_text())
assert nl.get("column_set", "").startswith("classic")
d = nl["rules"]["R1_alvl85_all"]["distributions_normal"]["hp_mid"]
assert gd["median"] == prim["gd_median"]
out = {"basis": "identical to primary r_HP R1 (GD BOARD trash body-weighted median hp_lo / D2 R1 normal median hp_mid, equal per type); only D2 HP column set differs",
       "gd_median_hp_lo": gd["median"], "gd_p25": gd["p25"], "gd_p75": gd["p75"],
       "d2_nonladder_median_hp_mid": d["equal"]["median"], "d2_nonladder_p25": d["equal"]["p25"], "d2_nonladder_p75": d["equal"]["p75"],
       "d2_nonladder_slot_weighted_median": d["slot"]["median"],
       "r_hp_nonladder": gd["median"] / d["equal"]["median"],
       "r_hp_nonladder_iqr_ratio": [gd["p25"] / d["equal"]["p25"], gd["p75"] / d["equal"]["p75"]],
       "r_hp_primary_R1": prim["ratio_median"], "d2_primary_median_hp_mid": prim["d2_median"],
       "ratio_nonladder_over_primary": (gd["median"] / d["equal"]["median"]) / prim["ratio_median"],
       "approx_R1_over_0.75": prim["ratio_median"] / 0.75,
       "inputs_sha256": {f: hashlib.sha256((P / f).read_bytes()).hexdigest() for f in ("ratio_table.json", "d2_enemy_quantities_nonladder.json", "d2_enemy_quantities.json", "gd_enemy_quantities.json")}}
(P / "r_hp_nonladder.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "inputs_sha256"}, indent=1))
