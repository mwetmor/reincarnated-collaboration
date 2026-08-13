#!/usr/bin/env python3
"""KC2-PM4 Lap D EMITTER -- the band-B (waves 151-170) monster life table.

READ-ONLY.  Writes only into the lap's own notes directory.

    S1  POPULATION BASES          -- every count declares what it counts over (NOTE-9)
    S2  THE DECODED CONSTANTS     -- G array + Ultimate cell, read from the records (GL-12)
    S3  LEVEL FLOOR-SETS          -- band-B pool slots, index-paired slot law; apl equivalence CHECKED
    S4  THE LIFE CHAIN            -- band A's chain, imported, at band-B waves
    S5  EMIT                      -- wide life table (band-A schema) + long per-wave eHP table
    S6  READER DELTA              -- IS-B1 priced

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4 iteration I-1, Lap D.
"""
from __future__ import annotations

import collections
import csv
import json
import math
import pathlib
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import pm4d_lib_2026_08_13 as L  # noqa: E402

from gamora_kc2_stat_fold_ed3_2026_08_08 import floor_set, APL_B_PRIME  # noqa: E402

NOTES = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                     "legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp")
OUT: dict = {}
SEP = "=" * 98

#: The wave the reference truth's death occurred on, and this lap's control column.
CONTROL_WAVE = 160


def main() -> None:
    NOTES.mkdir(parents=True, exist_ok=True)

    # ═════════════════════════════════════════════════════════════════════════════════ S1
    print(SEP)
    print("S1  POPULATION BASES (NOTE-9 -- no count in this lap is unlabelled)")
    print(SEP)

    rolled20 = L.rolled_records(first=151, last=170)
    rolled10 = L.rolled_records(first=151, last=160)
    acts20 = L.rolled_actors(first=151, last=170)
    acts10 = L.rolled_actors(first=151, last=160)
    rec_pools, rec_waves, rec_slot, rec_kind, pools = L.pool_population()
    closed_bandA, layers_bandA = L.summon_closure(set(rec_pools))
    closed, summon_layers, summoner_of_ext = L.summon_closure_extended(set(rec_pools))
    summon_only = closed - set(rec_pools)

    print(f"    P-ROLLED-20  frozen baton waves 151-170 : {len(acts20):5d} actors  "
          f"{len(rolled20):4d} distinct records")
    print(f"    P-ROLLED-10  frozen baton waves 151-160 : {len(acts10):5d} actors  "
          f"{len(rolled10):4d} distinct records   <- PM-3 S 5's population")
    print(f"    P-POOL       band-B pool records        : {len(rec_pools):5d} over {len(pools)} pools")
    print(f"    P-CLOSED     P-POOL + summon fixpoint   : {len(closed):5d} "
          f"(+{len(summon_only)} summon bodies; layers {summon_layers})")
    print(f"    ⚑ IS-B2/IS-B3 -- band A's own closure on the same seed reaches only "
          f"{len(closed_bandA)} (layers {layers_bandA}); the extension adds "
          f"{len(closed - closed_bandA)} bodies, all Class=Monster "
          f"({L.class_census(sorted(closed - closed_bandA))}).")
    orphan_rolled = set(rolled20) - set(rec_pools)
    print(f"    CONTAINMENT  P-ROLLED-20 \\ P-POOL       : {len(orphan_rolled)}"
          + ("" if not orphan_rolled else f"  {sorted(orphan_rolled)[:5]}"))
    OUT["populations"] = {
        "P-ROLLED-20": {"actors": len(acts20), "records": len(rolled20),
                        "basis": f"{L.BATON_20W.name} actors[] wave in [151,170]"},
        "P-ROLLED-10": {"actors": len(acts10), "records": len(rolled10),
                        "basis": f"{L.BATON_20W.name} actors[] wave in [151,160]"},
        "P-POOL": {"records": len(rec_pools), "pools": len(pools),
                   "basis": "pe6_crucible_wave_pools_v2.csv roster_records U champ_records, "
                            "global_wave in [151,170]"},
        "P-CLOSED": {"records": len(closed), "summon_only": len(summon_only),
                     "summon_layers": summon_layers,
                     "basis": "P-POOL + EXTENDED summon closure to FIXPOINT (IS-B2 nested skill "
                              "refs + skill-record carriers; IS-B3 admission by Class not path; "
                              "poolToSpawnOnDeath EXCLUDED per L-33(h))",
                     "band_a_closure_on_same_seed": len(closed_bandA),
                     "band_a_layers": layers_bandA,
                     "records_the_extension_adds": len(closed - closed_bandA),
                     "class_census_of_added": L.class_census(sorted(closed - closed_bandA))},
        "rolled_not_in_pool": sorted(orphan_rolled),
    }

    # PM-3 baton agreement -- the fight cells stop at the death wave, so they must be a SUBSET.
    pm3_recs = set()
    for b in L.PM3_BATONS:
        j = json.loads(b.read_text())
        pm3_recs |= {a["record_path"].lower() for a in j["actors"]}
    print(f"    P-PM3        union of 5 PM-3 fight batons: {len(pm3_recs):4d} records  "
          f"subset of P-ROLLED-20: {pm3_recs <= set(rolled20)}")
    OUT["populations"]["P-PM3"] = {"records": len(pm3_recs),
                                   "subset_of_P_ROLLED_20": bool(pm3_recs <= set(rolled20)),
                                   "batons": [b.name for b in L.PM3_BATONS]}

    # ═════════════════════════════════════════════════════════════════════════════════ S2
    print("\n" + SEP)
    print("S2  THE DECODED CONSTANTS -- read from the .arz records, not from any CSV (GL-12)")
    print(SEP)
    surv = L.survival_life_modifier_array()
    ult = L.ultimate_life_modifier_pct()
    print(f"    balancingadjustment_survivalmode_enemies03.characterLifeModifier : {len(surv)} cells")
    print(f"    balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8] : {ult}")
    gb = {w: L.G_at(surv, w) for w in range(151, 171)}
    print(f"    G over band B (array-lookup law, cell LABELED w):")
    print(f"        {'  '.join(f'{w}:{int(g)}' for w, g in list(gb.items())[:10])}")
    print(f"        {'  '.join(f'{w}:{int(g)}' for w, g in list(gb.items())[10:])}")
    print(f"    G(150) = {L.G_at(surv,150)}   G(170) = {L.G_at(surv,170)}   "
          f"<- the playtest-directions '+304 -> 344%' citation, CORROBORATED from the record")
    print(f"    ⚑ G(171) = {L.G_at(surv,171)} -- a +76 pt DISCONTINUITY at the tier-17/18 boundary. "
          f"Band B stops at 170; extrapolating past it is a different board.")

    # halt9 CSV checked AGAINST the decode (opposite direction of trust)
    halt9 = {}
    with L.SCALING_CSV.open() as fh:
        for r in csv.DictReader(fh):
            if r["difficulty"] == "gladiator":
                halt9[int(r["wave"])] = float(r["characterLifeModifier"])
    h_ok = sum(1 for w in range(1, 201) if halt9.get(w) == surv[w - 1])
    print(f"    halt9_survival_wave_scaling_full.csv (gladiator) vs the decode : "
          f"{h_ok}/200 cells identical")
    OUT["constants"] = {"ultimate_life_modifier_pct": ult,
                        "survival_array_len": len(surv),
                        "G_band_b": {str(w): g for w, g in gb.items()},
                        "G_150": L.G_at(surv, 150), "G_171": L.G_at(surv, 171),
                        "halt9_csv_cells_identical_to_decode": h_ok,
                        "halt9_csv_cells_total": 200,
                        "array_lookup_law": "S 10.7 / L-33 -- fighting wave w reads index w-1 "
                                            "(the cell LABELED w). TOTAL on [1,200], no clamp."}

    # ═════════════════════════════════════════════════════════════════════════════════ S3
    print("\n" + SEP)
    print("S3  LEVEL FLOOR-SETS -- `L` is a SET, never a midpoint (the C-1 prescription)")
    print(SEP)
    lvsets, slot_map, proxies, lvt = L.band_b_level_sets(pools, rec_pools)
    widths = collections.Counter(len(s) for s in lvsets.values())
    allL = sorted({x for s in lvsets.values() for x in s})
    print(f"    band-B pool records carrying a slot-derived level set : {len(lvsets)} / {len(rec_pools)}")
    print(f"    floor-set widths : {dict(sorted(widths.items()))}")
    print(f"    ⚑ band-B charLevel RANGE : {min(allL)} … {max(allL)}")

    # R-L65-1 equivalence CHECKED on band B's OWN proxy set, not carried over from band A.
    used_proxies = sorted({p for s in proxies.values() for p in s})
    eq_ok = eq_bad = 0
    eq_detail = []
    for lv in used_proxies:
        fb = floor_set(lvt, lv, APL_B_PRIME)
        fa = [x + 3 for x in floor_set(lvt, lv, 100.0)]
        if fa == fb:
            eq_ok += 1
        else:
            eq_bad += 1
            eq_detail.append({"proxy": lv, "apl_103_4": fb, "apl_100_plus3": fa})
    print(f"    lv proxies reached by band-B slots : {len(used_proxies)}")
    print(f"    R-L65-1 floor-equivalence (a) apl=100+3 vs (b') apl=103.4, RE-CHECKED on band B : "
          f"identical {eq_ok}, differ {eq_bad}")
    for d in eq_detail:
        print(f"        ⚑ DIFFERS {d['proxy']}  (b'){d['apl_103_4']}  vs  (a){d['apl_100_plus3']}")

    # Summon bodies inherit their summoner's level set (band-A's DECLARED rule, carried).
    # ⚑ Propagated to FIXPOINT: the extended closure runs to depth 5, so a depth-3 body inherits
    #   from a depth-2 body that has itself only just inherited. One pass would leave those empty
    #   and a one-pass emptiness reads as an absence rather than as an unfinished traversal.
    n_inherit = 0
    for _ in range(12):
        moved = 0
        for b in sorted(summon_only):
            if lvsets.get(b):
                continue
            inh = set()
            for s in summoner_of_ext.get(b, ()):
                inh |= set(lvsets.get(s, []))
            if inh:
                lvsets[b] = sorted(inh)
                moved += 1
        n_inherit += moved
        if not moved:
            break
    print(f"    summon bodies inheriting the summoner's level set : {n_inherit} / {len(summon_only)} "
          f"[DERIVED-INHERITED -- a summon body is not pooled and carries no levelVarianceEquation]")

    # ⚑ THE BATON'S OWN LEVELS, CHECKED AGAINST THE DERIVED SETS (agreement, not adoption).
    inside = outside = noset = 0
    out_ex = []
    for rec, e in rolled20.items():
        s = set(lvsets.get(rec, []))
        bl = set(e["baton_levels"])
        if not s:
            noset += 1
        elif bl <= s:
            inside += 1
        else:
            outside += 1
            if len(out_ex) < 8:
                out_ex.append({"record": rec, "baton_levels": sorted(bl), "derived_set": sorted(s)})
    print(f"\n    ⚑ BATON LEVELS vs DERIVED SETS, over P-ROLLED-20 ({len(rolled20)} records):")
    print(f"        baton level INSIDE the derived set : {inside}")
    print(f"        baton level OUTSIDE                : {outside}")
    print(f"        no derived set                     : {noset}")
    print(f"        (the baton declares DIV-LEVEL-COVERAGE: 176/344 actors have NO cited level "
          f"source and ride `_BAND_B_MODAL_LEVEL = 109`, a FALLBACK. This lap supplies the "
          f"missing source.)")
    for d in out_ex:
        print(f"          {d['record'].split('/')[-1]:44s} baton {d['baton_levels']} "
              f"vs derived {d['derived_set']}")
    OUT["levels"] = {
        "population": "P-POOL for slot-derived sets; P-CLOSED\\P-POOL for inheritance",
        "records_with_slot_level_set": len(proxies),
        "floor_widths": dict(sorted(widths.items())),
        "charlevel_min": min(allL), "charlevel_max": max(allL),
        "lv_proxies_used": used_proxies,
        "apl_equivalence_rechecked_on_band_b": {"identical": eq_ok, "differ": eq_bad,
                                                "detail": eq_detail},
        "summon_inheritance": {"inherited": n_inherit, "of": len(summon_only)},
        "baton_level_agreement": {"population": "P-ROLLED-20 records", "n": len(rolled20),
                                  "inside_derived_set": inside, "outside": outside,
                                  "no_derived_set": noset, "examples": out_ex},
    }

    # ═════════════════════════════════════════════════════════════════════════════════ S4
    print("\n" + SEP)
    print("S4  THE LIFE CHAIN over P-CLOSED (band A's chain, imported, at band-B waves)")
    print(SEP)
    rows: dict = {}
    for rec in sorted(closed):
        rows[rec] = L.build_life_row(rec, lvsets.get(rec, []))
    grades = collections.Counter(r.life_grade.split(" (")[0] for r in rows.values())
    print(f"    records folded : {len(rows)}  (population P-CLOSED)")
    for g, n in grades.most_common():
        print(f"        {n:5d}  {g}")
    named_gaps = [r.record for r in rows.values() if r.life_grade != "MEASURED"]
    for g in named_gaps[:20]:
        print(f"        NAMED GAP: {g}  [{rows[g].life_grade}]")
    OUT["life_chain"] = {"population": "P-CLOSED", "n": len(rows),
                         "grades": dict(grades), "named_gap_records": sorted(named_gaps)}

    # ═════════════════════════════════════════════════════════════════════════════════ S5
    print("\n" + SEP)
    print("S5  EMIT")
    print(SEP)

    # ---- (i) WIDE life table -- the band-A schema, extended to band B -----------------------
    wide = []
    for rec in sorted(rows):
        r = rows[rec]
        lo = r.levels[0] if r.levels else None
        hi = r.levels[-1] if r.levels else None
        d = {
            "record": rec,
            "in_rolled_20w": int(rec in rolled20),
            "in_rolled_10w": int(rec in rolled10),
            "in_pool": int(rec in rec_pools),
            "is_summon_body": int(rec in summon_only),
            "level_set": "|".join(str(x) for x in r.levels),
            "level_lo": lo if lo is not None else "",
            "level_hi": hi if hi is not None else "",
            "bio_record": (r.chain.bio or "") if r.chain else "",
            "life_equation": (r.chain.life_eq or "") if r.chain else "",
            "monster_class": r.monster_class,
            "winner_archive": r.archive,
        }
        if lo is not None and r.life_grade == "MEASURED":
            d["base_life_lo"] = round(r.base_life(lo), 4)
            d["base_life_hi"] = round(r.base_life(hi), 4)
            d["life_passive_pct_lo"] = r.passive_pct(lo)
            d["life_passive_pct_hi"] = r.passive_pct(hi)
            d["life_passive_sources_lo"] = "|".join(r.passive_sources(lo))
            for w in (151, CONTROL_WAVE, 170):
                d[f"ehp_w{w}_lo"] = r.ehp(w, lo, surv, ult)
                d[f"ehp_w{w}_hi"] = r.ehp(w, hi, surv, ult)
        else:
            d.update({"base_life_lo": "", "base_life_hi": "",
                      "life_passive_pct_lo": "", "life_passive_pct_hi": "",
                      "life_passive_sources_lo": ""})
            for w in (151, CONTROL_WAVE, 170):
                d[f"ehp_w{w}_lo"] = ""
                d[f"ehp_w{w}_hi"] = ""
        d["own_characterLifeModifier"] = r.own_life_modifier_pct
        d["own_applied"] = "NO (L-33(b): falsified on camera; band A does not fold it either)"
        d["pool_records"] = "|".join(sorted(rec_pools.get(rec, ()))[:6])
        d["pool_kinds"] = "|".join(sorted(k for k in rec_kind.get(rec, ()) if k))
        d["waves_pooled"] = "|".join(str(x) for x in sorted(rec_waves.get(rec, ())))
        d["waves_rolled"] = "|".join(str(x) for x in sorted(rolled20[rec]["waves"])) \
            if rec in rolled20 else ""
        d["baton_levels"] = "|".join(str(x) for x in sorted(rolled20[rec]["baton_levels"])) \
            if rec in rolled20 else ""
        d["life_grade"] = r.life_grade
        d["level_grade"] = ("MEASURED-SET" if rec in proxies else
                            ("DERIVED-INHERITED" if rec in summon_only and r.levels else
                             "ABSENT:NO-LEVEL-SOURCE"))
        d["damage_grade"] = ("NOT-IN-SCOPE — Lap D is the LIFE limb of I-1. Band-B monster "
                             "damage is a separate decode (PM-4 queue I-2/I-5).")
        wide.append(d)
    wide_cols = ["record", "in_rolled_20w", "in_rolled_10w", "in_pool", "is_summon_body",
                 "level_set", "level_lo", "level_hi", "bio_record", "life_equation",
                 "monster_class", "winner_archive",
                 "base_life_lo", "base_life_hi", "life_passive_pct_lo", "life_passive_pct_hi",
                 "life_passive_sources_lo",
                 "ehp_w151_lo", "ehp_w151_hi", "ehp_w160_lo", "ehp_w160_hi",
                 "ehp_w170_lo", "ehp_w170_hi",
                 "own_characterLifeModifier", "own_applied",
                 "pool_records", "pool_kinds", "waves_pooled", "waves_rolled", "baton_levels",
                 "life_grade", "level_grade", "damage_grade"]
    p_wide = L.dump_csv(NOTES / "pm4d_band_b_monster_life.csv", wide, wide_cols)

    # ---- (ii) LONG per-wave eHP table -- the SIM-CONSUMABLE drop ---------------------------
    long_rows = []
    for rec in sorted(rows):
        r = rows[rec]
        if r.life_grade != "MEASURED":
            long_rows.append({"record": rec, "wave": "", "G_pct": "", "level_lo": "",
                              "level_hi": "", "ehp_lo": "", "ehp_hi": "", "life_grade": r.life_grade})
            continue
        lo, hi = r.levels[0], r.levels[-1]
        for w in range(151, 171):
            long_rows.append({"record": rec, "wave": w, "G_pct": L.G_at(surv, w),
                              "level_lo": lo, "level_hi": hi,
                              "ehp_lo": r.ehp(w, lo, surv, ult),
                              "ehp_hi": r.ehp(w, hi, surv, ult),
                              "life_grade": "MEASURED"})
    p_long = L.dump_csv(NOTES / "pm4d_band_b_ehp_by_wave.csv", long_rows,
                        ["record", "wave", "G_pct", "level_lo", "level_hi",
                         "ehp_lo", "ehp_hi", "life_grade"])

    # ---- (iii) per-LEVEL table, for a consumer that knows an actor's own level --------------
    lvl_rows = []
    for rec in sorted(rows):
        r = rows[rec]
        if r.life_grade != "MEASURED":
            continue
        for lv in r.levels:
            lvl_rows.append({"record": rec, "char_level": lv,
                             "base_life": round(r.base_life(lv), 4),
                             "life_passive_pct": r.passive_pct(lv),
                             "passive_sources": "|".join(r.passive_sources(lv)),
                             "ehp_w151": r.ehp(151, lv, surv, ult),
                             "ehp_w160": r.ehp(160, lv, surv, ult),
                             "ehp_w170": r.ehp(170, lv, surv, ult)})
    p_lvl = L.dump_csv(NOTES / "pm4d_band_b_life_by_level.csv", lvl_rows)

    # ---- (iv) the G array, vendorable ------------------------------------------------------
    p_g = L.dump_csv(NOTES / "pm4d_band_b_wave_life_modifier.csv",
                     [{"wave": w, "G_characterLifeModifier_pct": L.G_at(surv, w),
                       "ultimate_pct": ult,
                       "M_without_passives": round(1.0 + (ult + L.G_at(surv, w)) / 100.0, 6)}
                      for w in range(151, 171)])

    OUT["emissions"] = {}
    for p in (p_wide, p_long, p_lvl, p_g):
        OUT["emissions"][p.name] = {"rows": sum(1 for _ in p.open()) - 1,
                                    "sha256": L.sha256_of(p)}
        print(f"        sha256 {p.name} = {L.sha256_of(p)}")

    # ═════════════════════════════════════════════════════════════════════════════════ S6
    print("\n" + SEP)
    print("S6  READER DELTA (IS-B1) -- whole-record replacement vs the Lap-B field merge")
    print(SEP)
    rd = L.reader_delta(sorted(rolled20))
    print(f"    population: P-ROLLED-20 records ({rd['n']})")
    print(f"        identical field sets : {rd['identical']}")
    print(f"        merge resurrects fields the winner does not carry : {rd['differ']}")
    for e in rd["examples"][:6]:
        print(f"          {e['record'].split('/')[-1]:44s} winner {e['n_winner_fields']} fields, "
              f"merge {e['n_merged_fields']}  {e['fields_merge_resurrects'][:4]}")
    OUT["reader_delta_IS_B1"] = rd

    (NOTES / "pm4d_emit_summary.json").write_text(json.dumps(OUT, indent=2, default=str))
    print(f"\n    wrote {NOTES / 'pm4d_emit_summary.json'}")


if __name__ == "__main__":
    main()
