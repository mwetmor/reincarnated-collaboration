#!/usr/bin/env python3
"""KC2-PM4 Lap E emitter -- pet eHP under the DECODED fold, per (pet record, wave).

EMISSIONS (declared schema, and every magnitude traces to a `.dbr` field -- GL-12)

 1. `pm4e_pet_ehp_by_wave.csv`   (record, wave) x 20 waves -- THE SIM-CONSUMABLE DROP
      record, wave, level_lo, level_hi, ehp_lo, ehp_hi, ult_pct, g_pct,
      passive_pct_lo, passive_pct_hi, lapb_life, hardening_ratio_lo, life_grade, level_grade

 2. `pm4e_pet_life_decode.csv`   one row per pet body -- THE EVIDENCE ROW
      record, body_class, template_name, pak_binding, is_lapb_70, summoners, n_summoners,
      level_set, level_lo, level_hi, bio_record, life_equation, base_life_lo/hi,
      passive_pct_lo/hi, ehp_w151/w160/w170 lo+hi, lapb_life, hardening_ratio_lo,
      own_characterLifeModifier, own_applied, life_grade, level_grade

 3. `pm4e_positive_control.csv`  the four camera-measured skill-spawned pets, recomputed FOUR ways

 4. `pm4e_dispatch_evidence.csv` the decoded pak/adjustment binding surface (L1/L3)

Consumption (gamora), identical in shape to Lap D's:

    pet_hp = {rec: ehp_lo for (rec, w), (ehp_lo, ehp_hi) in table.items() if w == wave}

`ehp_lo` is the LO limb, carrying R-PM4-2 (LO by explicit column selection, never row order).

READ-ONLY on every input.  Author: legolas, 2026-08-13.  Run KC2-PM4, iteration I-2, Lap E.
"""
from __future__ import annotations

import collections
import json
import pathlib
import statistics
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")

from pm4d_lib_2026_08_13 import (  # noqa: E402
    E3, BAND_B_FIRST, BAND_B_LAST, build_life_row, dump_csv, G_at, sha256_of,
    survival_life_modifier_array, ultimate_life_modifier_pct,
)
from pm4e_lib_2026_08_13 import (  # noqa: E402
    MONSTER_PAK_CLASSES, PET_PAK_CLASSES, body_class, control_table, lapb_life,
    lapb_pet_bodies, lapb_pet_rows, owner_level_sets, pak_dispatch, pak_life_pct,
    summon_only_bodies, survival_dispatch,
)

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "notes/2026-08-13-kc2-pm4-lap-e-pet-life")
DIFFICULTY_INDEX = 8   # Ultimate / solo -- the same cell band A and Lap D read


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict = {}

    # ── the decoded constants ──────────────────────────────────────────────────────────────
    surv = survival_life_modifier_array()
    ULT = ultimate_life_modifier_pct()
    waves = list(range(BAND_B_FIRST, BAND_B_LAST + 1))
    print(f"  ULT(Ultimate/solo, index {DIFFICULTY_INDEX}) = {ULT}")
    print(f"  G over band B: {G_at(surv, 151)} .. {G_at(surv, 170)}")

    # ── L1 / L3: the dispatch surface ──────────────────────────────────────────────────────
    paks = pak_dispatch()
    surv_binding = survival_dispatch()
    disp_rows = []
    for field, rec in sorted(paks.items()):
        disp_rows.append(dict(
            binding_record="records/game/gameengine.dbr", binding_field=field,
            target_record=rec, target_class=str((E3.winner(rec)[0] or {}).get("Class") or ""),
            life_pct_at_ultimate_solo=pak_life_pct(rec, DIFFICULTY_INDEX)
            if isinstance((E3.winner(rec)[0] or {}).get("characterLifeModifier"), list)
            else pak_life_pct(rec, 0),
            note="class-scoped difficulty pak (12 cells = 3 difficulties x 4 player counts)"))
    for field, rec in sorted(surv_binding.items()):
        r, _ = E3.winner(rec)
        arr = (r or {}).get("characterLifeModifier")
        disp_rows.append(dict(
            binding_record="records/game/survivalinfo.dbr", binding_field=field,
            target_record=rec, target_class=str((r or {}).get("Class") or ""),
            life_pct_at_ultimate_solo=(float(arr[159]) if isinstance(arr, list) else ""),
            note="GameAdjustment (attributepak.tpl + 4 spawn-COUNT fields); NO class dispatch, "
                 "NO pet variant, NO player variant -- survivalinfo.tpl carries exactly 3"))
    dump_csv(OUT / "pm4e_dispatch_evidence.csv", disp_rows)

    # ── L4: the positive control ───────────────────────────────────────────────────────────
    ctrl = control_table(160)
    dump_csv(OUT / "pm4e_positive_control.csv", ctrl)
    n_exact = sum(1 for c in ctrl if c.get("verdict") == "EXACT")
    print(f"  positive control: {n_exact}/{len(ctrl)} camera-measured pets EXACT under the full fold")
    for c in ctrl:
        print(f"     {c['body'][:22]:24s} L={c['level']} measured={c['measured']:>9,} "
              f"full={c['ehp_full']:>9,} noULT={c['ehp_without_ultimate']:>9,} "
              f"noG={c['ehp_without_g']:>9,} lapB={c['ehp_lapb_passives_only']:>9,} -> {c['verdict']}")
    summary["positive_control"] = dict(n=len(ctrl), exact=n_exact, rows=ctrl)

    # ── the population + levels ────────────────────────────────────────────────────────────
    # ⚑ IS-E1: the emission covers P-SUMMON-128 (the true summon-only population), and marks
    # which rows are in P-PET-70 (Lap B's chain output, the commission's declared basis) so
    # BOTH bases stay legible in ONE table rather than drifting across two (NOTE-9).
    pets, lapb_missed = summon_only_bodies()
    lapb70 = set(lapb_pet_bodies())
    lvsets, summoner_of = owner_level_sets()
    lb = lapb_life(lapb_pet_rows())
    print(f"  P-SUMMON-128 (summon-only bodies over the 663 band-B pool records): {len(pets)}")
    print(f"  P-PET-70     (Lap B chain output, subset): {len(lapb70)}  "
          f"⚑ Lap B misses {len(lapb_missed)} summon bodies")

    wide, long_rows = [], []
    grades = collections.Counter()
    lvgrades = collections.Counter()
    ratios_w160 = []

    for rec in pets:
        levels = lvsets.get(rec, [])
        row = build_life_row(rec, levels)
        cls = body_class(rec)
        pak = ("monsterAttributePak -> " + paks["monsterAttributePak"]) if cls in MONSTER_PAK_CLASSES \
            else (("petAttributePak -> " + paks["petAttributePak"]) if cls in PET_PAK_CLASSES
                  else "NO-PAK-BINDING-DECODED")
        r_rec, arc = E3.winner(rec)

        if not levels:
            # GL-12: no modal fill, no sibling fill. A pet whose owner carries no band-B pool slot
            # has NO level source and therefore NO magnitude.
            row.level_grade = "DECLARED-GAP:NO-OWNER-LEVEL-SOURCE"
            row.life_grade = row.life_grade if not row.chain or not row.chain.ok else \
                "DECLARED-GAP:NO-OWNER-LEVEL-SOURCE"
        else:
            row.level_grade = "DERIVED-INHERITED-FROM-SUMMONER"

        lo = levels[0] if levels else None
        hi = levels[-1] if levels else None
        base_lo = row.base_life(lo) if lo is not None else None
        base_hi = row.base_life(hi) if hi is not None else None
        pas_lo = row.passive_pct(lo) if lo is not None else None
        pas_hi = row.passive_pct(hi) if hi is not None else None
        ok = base_lo is not None and pas_lo is not None

        grades[row.life_grade] += 1
        lvgrades[row.level_grade] += 1
        lapb_v = lb.get(rec)

        e = {}
        for w in waves:
            elo = row.ehp(w, lo, surv, ULT) if ok else None
            ehi = row.ehp(w, hi, surv, ULT) if ok else None
            e[w] = (elo, ehi)
            ratio = (elo / lapb_v) if (elo is not None and lapb_v) else None
            long_rows.append(dict(
                record=rec, wave=w, level_lo=lo, level_hi=hi, ehp_lo=elo, ehp_hi=ehi,
                ult_pct=ULT, g_pct=G_at(surv, w),
                passive_pct_lo=pas_lo, passive_pct_hi=pas_hi,
                lapb_life=lapb_v, hardening_ratio_lo=round(ratio, 4) if ratio else None,
                is_lapb_70=(rec in lapb70),
                life_grade=row.life_grade, level_grade=row.level_grade))
            if w == 160 and ratio:
                ratios_w160.append(ratio)

        wide.append(dict(
            record=rec, body_class=cls, template_name=str((r_rec or {}).get("templateName") or ""),
            pak_binding=pak, is_lapb_70=(rec in lapb70),
            summoners="|".join(sorted(summoner_of.get(rec, ()))[:6]),
            n_summoners=len(summoner_of.get(rec, ())),
            level_set="|".join(str(x) for x in levels), level_lo=lo, level_hi=hi,
            bio_record=(row.chain.bio or "") if row.chain else "",
            life_equation=(row.chain.life_eq or "") if row.chain else "",
            winner_archive=arc or "",
            base_life_lo=round(base_lo, 4) if base_lo is not None else None,
            base_life_hi=round(base_hi, 4) if base_hi is not None else None,
            passive_pct_lo=pas_lo, passive_pct_hi=pas_hi,
            ehp_w151_lo=e[151][0], ehp_w151_hi=e[151][1],
            ehp_w160_lo=e[160][0], ehp_w160_hi=e[160][1],
            ehp_w170_lo=e[170][0], ehp_w170_hi=e[170][1],
            lapb_life=lapb_v,
            hardening_ratio_lo=round(e[160][0] / lapb_v, 4) if (e[160][0] and lapb_v) else None,
            own_characterLifeModifier=row.own_life_modifier_pct, own_applied="NO",
            life_grade=row.life_grade, level_grade=row.level_grade))

    p1 = dump_csv(OUT / "pm4e_pet_ehp_by_wave.csv", long_rows)
    p2 = dump_csv(OUT / "pm4e_pet_life_decode.csv", wide)
    p3 = OUT / "pm4e_positive_control.csv"
    p4 = OUT / "pm4e_dispatch_evidence.csv"

    print(f"\n  life_grade : {dict(grades)}")
    print(f"  level_grade: {dict(lvgrades)}")
    if ratios_w160:
        print(f"\n  ⚑ HARDENING RATIO vs Lap-B (wave 160, LO limb, n={len(ratios_w160)} records): "
              f"min {min(ratios_w160):.2f} / median {statistics.median(ratios_w160):.2f} / "
              f"max {max(ratios_w160):.2f}")
        summary["hardening_w160"] = dict(
            basis="P-PET-70 records with both a LO eHP and a Lap-B value",
            n=len(ratios_w160), min=round(min(ratios_w160), 4),
            median=round(statistics.median(ratios_w160), 4), max=round(max(ratios_w160), 4))

    summary["constants"] = dict(ultimate_pct=ULT, g_151=G_at(surv, 151), g_160=G_at(surv, 160),
                                g_170=G_at(surv, 170), survival_cells=len(surv))
    summary["population"] = dict(P_SUMMON_128=len(pets), P_PET_70=len(lapb70),
                                 lapb_missed=len(lapb_missed),
                                 long_rows=len(long_rows), waves=len(waves))
    summary["lapb_missed_records"] = lapb_missed
    summary["grades"] = dict(life=dict(grades), level=dict(lvgrades))
    summary["digests"] = {p.name: sha256_of(p) for p in (p1, p2, p3, p4)}
    (OUT / "pm4e_emit_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print("\n  === SHA-256 PINS ===")
    for k, v in summary["digests"].items():
        print(f"    {k:34s} {v}")


if __name__ == "__main__":
    main()
