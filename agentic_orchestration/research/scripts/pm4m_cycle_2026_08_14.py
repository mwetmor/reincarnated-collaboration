#!/usr/bin/env python3
"""KC2-PM4 Lap M -- Q3 emitter: the ATTACK-CYCLE table for the wave-159/160 board.

Every body's `specialAttack{N}` slots decoded verbatim -- SkillName / Chance / Delay / Timeout /
Range -- plus the skill-side timing fields, so the referent's measured timing structure
(wave-160 arrival + 25.95 s; 1.6166 s of full health before the kill) can be read against a
candidate's own cadence.  READ-ONLY, MEASURED, no inference in the table.
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pm4m_lib_2026_08_14 import E3, dump_csv, ev, _idx           # noqa: E402
from pm4i_lib_2026_08_13 import (                                 # noqa: E402
    pool_population, level_sets, rolled_actors, summon_closure_extended,
)
from pm4m_emit_2026_08_14 import _s, OUT                          # noqa: E402

TIMING_FIELDS = ("skillCooldownTime", "skillActiveDuration", "skillChargeDuration",
                 "skillChargeLevel", "skillWindUpTime", "chargeDuration",
                 "skillProjectileSpeed", "projectileSpeed", "skillTargetRadius",
                 "projectileExplosionRadius", "dropHeight", "dropRadius",
                 "projectileLaunchNumber", "skillTargetNumber")


def main() -> None:
    rec_pools, rec_waves, rec_slot, rec_kind, pools = pool_population(159, 160)
    lvsets, _prox, _lvt = level_sets(pools, rec_pools)
    bodies, _layers, _via = summon_closure_extended(set(rec_pools))
    rolled = {}
    for a in rolled_actors(159, 160):
        rolled.setdefault(str(a.get("record", "")).lower().replace("\\", "/"), set()).add(int(a["wave"]))

    rows = []
    for rec in sorted(rec_pools):
        r, _arc = E3.winner(rec)
        if not r:
            continue
        L = float(max(lvsets.get(rec, [109])))
        slots = [("attackSkillName", "", "basic")]
        slots.append(("specialAttackSkillName", "", "special1"))
        for n in range(2, 9):
            slots.append((f"specialAttack{n}SkillName", str(n), f"special{n}"))
        for field, n, label in slots:
            sk = _s(r.get(field))
            if not isinstance(sk, str) or not sk.lower().endswith(".dbr"):
                continue
            sk = sk.lower().replace("\\", "/")
            s, sarc = E3.winner(sk)
            pre = "specialAttack" + n if label.startswith("special") else ""
            row = dict(
                body_record=rec,
                in_pool_waves="|".join(str(w) for w in sorted(rec_waves.get(rec, []))),
                in_frozen_baton_roll="|".join(str(w) for w in sorted(rolled.get(rec, []))) or "NO",
                slot=label, slot_field=field, skill_record=sk,
                skill_archive=sarc or "ABSENT",
                skill_class=str((s or {}).get("Class") or ""),
                chance_pct=_s(r.get(pre + "Chance")) if pre else "",
                delay_s=_s(r.get(pre + "Delay")) if pre else "",
                timeout_s=_s(r.get(pre + "Timeout")) if pre else "",
                range_band=_s(r.get(pre + "Range")) if pre else "",
                character_attack_speed=_s(r.get("characterAttackSpeed")),
                short_range_max=_s(r.get("shortRangeMax")),
                medium_range_max=_s(r.get("mediumRangeMax")),
                long_range_max=_s(r.get("longRangeMax")),
            )
            for f in TIMING_FIELDS:
                v = (s or {}).get(f)
                if isinstance(v, list):
                    v = v[0] if v else None
                row[f] = v if v else ""
            rows.append(row)

    cols = list(rows[0].keys())
    d = dump_csv(OUT / "pm4m_attack_cycle.csv", rows, cols)
    print(json.dumps(dict(rows=len(rows), digest=d), indent=2))
    for r in rows:
        if r["body_record"].split("/")[-1] in (
                "nemesis_wendigo_01.dbr", "nemesis_aetherial_01.dbr",
                "nemesis_aetherialvanguard_01.dbr", "nemesis_orderdeathsvigil_01.dbr",
                "statue_korvaaktombguardian.dbr", "nemesis_kymon_01.dbr",
                "aetherialcolossus_galakros.dbr"):
            print(f"  {r['body_record'].split('/')[-1]:<38s} {r['slot']:<9s} "
                  f"chance={str(r['chance_pct']):>6s} delay={str(r['delay_s']):>6s} "
                  f"timeout={str(r['timeout_s']):>6s} range={str(r['range_band']):<12s} "
                  f"{r['skill_record'].split('/')[-1]}")


if __name__ == "__main__":
    main()
