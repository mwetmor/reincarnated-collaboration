#!/usr/bin/env python3
"""C-14 stage 4 (gamora ADDENDUM-9): the R1 monster chill-effectiveness distribution (MonStats coldeffect(H)) and the
integer freeze/chill length table for her Frozen Armor (slvl 16: 75 frames) by target cold resist. Read-only."""
import csv, json, statistics, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
C13 = P.parent / "2026-10-14-join1-c13-enemy-anchor"
ms = {r["Id"]: r for r in csv.DictReader(open(RAW / "MonStats.txt", encoding="latin-1"), delimiter="\t") if r["Id"]}
dl = {r["Name"]: r for r in csv.DictReader(open(RAW / "DifficultyLevels.txt", encoding="latin-1"), delimiter="\t")}
FD, CD = int(dl["Hell"]["MonsterFreezeDivisor"]), int(dl["Hell"]["MonsterColdDivisor"])
rows = json.loads((C13 / "d2_enemy_quantities.json").read_text())["rules"]["R1_alvl85_all"]["rows"]
ce = []
for r in rows:
    m = ms[r["id"]]
    v = int(m["coldeffect(H)"]) if m["coldeffect(H)"].strip() not in ("",) else None
    ce.append({"id": r["id"], "coldeffect_H": v, "cold_res_H": int(m["ResCo(H)"] or 0), "slot_weight": r["slot_weight"]})
vals = [x["coldeffect_H"] for x in ce if x["coldeffect_H"] is not None]
def q(v):
    v = sorted(v); qs = statistics.quantiles(v, n=4, method="inclusive")
    return {"n": len(v), "median": statistics.median(v), "p25": qs[0], "p75": qs[2], "min": v[0], "max": v[-1]}
from collections import Counter
FA = 75   # Frozen Armor slvl 16 freeze length, frames (c14_stage3.json)
def frz(res):
    v = FA if res == 0 else (FA * (100 - min(res, 100)) // 100)
    return v
table = []
for res in (-50, -25, 0, 20, 33, 40, 50, 60, 75, 99, 100):
    after_res = frz(res) if res < 100 else 0
    table.append({"target_cold_res": res, "after_resist_frames": after_res,
                  "normal_or_minion_frozen_frames_Hell": after_res // FD,
                  "chilled_frames_Hell (unique/boss/hireling; coldeffect<0)": max(after_res // CD, 1) if after_res > 0 else 0})
doc = {"hell_freeze_divisor": FD, "hell_cold_divisor": CD,
       "chill_effectiveness_R1": {"dist": q(vals), "counts": dict(Counter(vals)), "n_zero_or_positive_(no_chill/no_freeze)": sum(1 for v in vals if v >= 0),
                                  "rows": ce},
       "frozen_armor_freeze_frames_slvl16": FA, "rounding_table": table,
       "order": "floor(L x (100 - coldres)/100) [CalculateTotalDamage stat table row 'Flen'] -> Cannot Be Frozen = 0 / Half Freeze Duration /2 (monsters normally have neither) -> ApplyFreezeState: if MonStats coldeffect(H) >= 0 no freeze; else floor(.. / MonsterFreezeDivisor); boss/unique/hireling -> ApplyColdState: floor(.. / MonsterColdDivisor), min 1"}
(P / "c14_stage4.json").write_text(json.dumps(doc, indent=1))
print(doc["chill_effectiveness_R1"]["dist"], doc["chill_effectiveness_R1"]["counts"], "no-chill", doc["chill_effectiveness_R1"]["n_zero_or_positive_(no_chill/no_freeze)"])
for t in table: print(t)
