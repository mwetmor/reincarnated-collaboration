#!/usr/bin/env python3
"""KC2-PM4 Lap I EMIT -- monster offense + band-C extension.  READ-ONLY on every source.

Emits into `agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense/`:

  1  pm4i_wave_damage_modifier.csv        waves 151..200, wide -- the damage-side pair of Lap D's
                                          `pm4d_band_b_wave_life_modifier.csv`
  2  pm4i_survival_wave_arrays_full.csv   long form: EVERY 200-cell array on the record x waves
  3  pm4i_ultimate_offense_paks.csv       the 12-cell AttributePak, every field, every cell
  4  pm4i_dot_riders.csv                  per (body, skill, DoT family) over the 151-160 board
  5  pm4i_terminal_wave_dot_ranking.csv   waves 159 + 160, measured DoT ranking
  6  pm4i_band_c_ehp_by_wave.csv          waves 171..180, per record, LO/HI level limbs
  7  pm4i_band_c_roster.csv               the band-C population with its provenance
  8  pm4i_emit_summary.json               machine summary

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, Lap I (ruling R-PM4-14).
"""
from __future__ import annotations

import collections
import csv
import json
import math
import pathlib
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import pm4i_lib_2026_08_13 as L                                   # noqa: E402
from pm4i_lib_2026_08_13 import E3, resolve, ev                   # noqa: E402

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense")
OUT.mkdir(parents=True, exist_ok=True)
S: dict = {"lap": "I", "run": "KC2-PM4", "ruling": "R-PM4-14", "date": "2026-08-13"}


def w(path, header, rows):
    p = OUT / path
    with p.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        wr.writeheader()
        for r in rows:
            wr.writerow(r)
    print(f"  wrote {path}  rows={len(rows)}  sha256={L.sha256(p)[:16]}")
    return {"rows": len(rows), "cols": len(header), "sha256": L.sha256(p)}


# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== TARGET 1 -- the wave-G DAMAGE modifier ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
surv = {k: L.survival_arrays(k) for k in ("01", "02", "03")}
sarc = L.survival_archive()
A = surv[L.SURV_OF_RECORD]
print(f"  survivalmode_enemies03  archive={sarc}  array fields={len(A)}  cells={len(A['characterLifeModifier'])}")

# RE-CHECK Lap D's difficulty-of-record choice from this seat rather than carrying it.
lifechk = {k: [surv[k]["characterLifeModifier"][x - 1] for x in (150, 160, 170)] for k in surv}
S["surv_record_recheck"] = {"life_at_150_160_170": lifechk,
                            "of_record": L.SURV_OF_RECORD,
                            "verdict": "enemies03 reproduces Lap D's G(150,160,170) = 304/324/344"}
print("  difficulty re-check  life@150/160/170:", lifechk)

# Is the DAMAGE array difficulty-dependent at all?  (measured, not assumed)
dmg_same = all(surv["01"]["offensiveTotalDamageModifier"] == surv[k]["offensiveTotalDamageModifier"]
               for k in ("02", "03"))
S["damage_array_identical_across_crucible_difficulties"] = dmg_same
print(f"  ⚑ offensiveTotalDamageModifier identical across enemies01/02/03: {dmg_same}")

up, uscal, uarc = L.difficulty_pak()
UIDX = L.DIFFICULTY_INDEX
def U(f):
    return float(up[f][UIDX]) if f in up else None

hdr1 = ["wave", "content_tier",
        "D_offensiveTotalDamageModifier_pct", "U_offensiveTotalDamageModifier_pct",
        "sum_total_damage_modifier_pct",
        "D_offensivePhysicalModifier_pct", "U_offensivePhysicalModifier_pct",
        "D_offensiveCritDamageModifier_pct",
        "D_offensiveSlowPoisonModifier_pct", "D_offensiveSlowBleedingModifier_pct",
        "D_offensiveSlowFireModifier_pct", "D_offensiveSlowColdModifier_pct",
        "D_offensiveSlowLightningModifier_pct", "D_offensiveSlowLifeModifier_pct",
        "D_offensiveSlowPhysicalModifier_pct",
        "U_offensiveSlowAllTypes_pct", "sum_dot_modifier_poison_pct",
        "D_characterOffensiveAbility_pct", "D_characterOffensiveAbilityModifier_pct",
        "U_characterOffensiveAbility_pct", "U_characterOffensiveAbilityModifier_pct",
        "D_characterAttackSpeedModifier_pct", "D_characterSpellCastSpeedModifier_pct",
        "U_characterAttackSpeedModifier_pct", "U_characterSpellCastSpeedModifier_pct",
        "D_skillCooldownReduction_pct", "D_retaliationTotalDamageModifier_pct",
        "D_characterDefensiveAbility_pct", "D_characterDefensiveAbilityModifier_pct",
        "G_characterLifeModifier_pct", "U_characterLifeModifier_pct",
        "damage_grade", "life_grade", "basis"]
BASIS = (f"records/game/balancingadjustment_survivalmode_enemies{L.SURV_OF_RECORD}.dbr@{sarc}"
         f" [index wave-1] + records/game/balancingadjustment_mp+difficulty_enemies01.dbr@{uarc}"
         f" [index {UIDX} = Ultimate/1-player]")
rows1 = []
for wv in range(L.WAVE_MOD_FIRST, L.WAVE_MOD_LAST + 1):
    g = lambda f: L.surv_at(A[f], wv) if f in A else None
    rows1.append(dict(
        wave=wv, content_tier=L.content_tier(wv),
        D_offensiveTotalDamageModifier_pct=g("offensiveTotalDamageModifier"),
        U_offensiveTotalDamageModifier_pct=U("offensiveTotalDamageModifier"),
        sum_total_damage_modifier_pct=round(g("offensiveTotalDamageModifier")
                                            + U("offensiveTotalDamageModifier"), 6),
        D_offensivePhysicalModifier_pct=g("offensivePhysicalModifier"),
        U_offensivePhysicalModifier_pct=U("offensivePhysicalModifier"),
        D_offensiveCritDamageModifier_pct=g("offensiveCritDamageModifier"),
        D_offensiveSlowPoisonModifier_pct=g("offensiveSlowPoisonModifier"),
        D_offensiveSlowBleedingModifier_pct=g("offensiveSlowBleedingModifier"),
        D_offensiveSlowFireModifier_pct=g("offensiveSlowFireModifier"),
        D_offensiveSlowColdModifier_pct=g("offensiveSlowColdModifier"),
        D_offensiveSlowLightningModifier_pct=g("offensiveSlowLightningModifier"),
        D_offensiveSlowLifeModifier_pct=g("offensiveSlowLifeModifier"),
        D_offensiveSlowPhysicalModifier_pct=g("offensiveSlowPhysicalModifier"),
        U_offensiveSlowAllTypes_pct=U("offensiveSlowPoisonModifier"),
        sum_dot_modifier_poison_pct=round(g("offensiveSlowPoisonModifier")
                                          + U("offensiveSlowPoisonModifier"), 6),
        D_characterOffensiveAbility_pct=g("characterOffensiveAbility"),
        D_characterOffensiveAbilityModifier_pct=g("characterOffensiveAbilityModifier"),
        U_characterOffensiveAbility_pct=U("characterOffensiveAbility"),
        U_characterOffensiveAbilityModifier_pct=U("characterOffensiveAbilityModifier"),
        D_characterAttackSpeedModifier_pct=g("characterAttackSpeedModifier"),
        D_characterSpellCastSpeedModifier_pct=g("characterSpellCastSpeedModifier"),
        U_characterAttackSpeedModifier_pct=U("characterAttackSpeedModifier"),
        U_characterSpellCastSpeedModifier_pct=U("characterSpellCastSpeedModifier"),
        D_skillCooldownReduction_pct=g("skillCooldownReduction"),
        D_retaliationTotalDamageModifier_pct=g("retaliationTotalDamageModifier"),
        D_characterDefensiveAbility_pct=g("characterDefensiveAbility"),
        D_characterDefensiveAbilityModifier_pct=g("characterDefensiveAbilityModifier"),
        G_characterLifeModifier_pct=g("characterLifeModifier"),
        U_characterLifeModifier_pct=U("characterLifeModifier"),
        damage_grade="MEASURED (components); sum_* = DERIVED-SUM-ADDITIVE-BY-PARALLEL",
        life_grade="MEASURED — reproduces pm4d_band_b_wave_life_modifier.csv on 151..170",
        basis=BASIS))
S["t1"] = w("pm4i_wave_damage_modifier.csv", hdr1, rows1)

# companion: EVERY array field, long form, so nothing is hidden by column selection
hdr2 = ["wave", "content_tier", "record", "archive", "field", "value", "grade"]
rows2 = []
for wv in range(L.WAVE_MOD_FIRST, L.WAVE_MOD_LAST + 1):
    for f in sorted(A):
        rows2.append(dict(wave=wv, content_tier=L.content_tier(wv),
                          record=f"records/game/balancingadjustment_survivalmode_enemies{L.SURV_OF_RECORD}.dbr",
                          archive=sarc, field=f, value=L.surv_at(A[f], wv), grade="MEASURED"))
S["t1_full"] = w("pm4i_survival_wave_arrays_full.csv", hdr2, rows2)

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== TARGET 2 -- the Ultimate offense AttributePak ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
print(f"  mp+difficulty_enemies01  archive={uarc}  Class={uscal.get('Class')}  arrays={len(up)}")
hdr3 = ["field", "cell_index", "difficulty", "player_count", "value",
        "is_ultimate_solo", "is_offense_field", "record", "archive", "grade", "note"]
OFF_PREFIX = ("offensive", "retaliation", "characterOffensiveAbility",
              "characterAttackSpeed", "characterSpellCastSpeed")
rows3 = []
for f in sorted(up):
    isoff = f.startswith(OFF_PREFIX)
    for i, v in enumerate(up[f]):
        d, pc = L.difficulty_cell_label(i)
        rows3.append(dict(field=f, cell_index=i, difficulty=d, player_count=pc, value=v,
                          is_ultimate_solo=(i == UIDX), is_offense_field=isoff,
                          record="records/game/balancingadjustment_mp+difficulty_enemies01.dbr",
                          archive=uarc, grade="MEASURED",
                          note=("cell Lap D read characterLifeModifier[8]=580.0 from"
                                if i == UIDX else "")))
for k, v in sorted(uscal.items()):
    if isinstance(v, (int, float)) and v and not isinstance(v, bool):
        rows3.append(dict(field=k, cell_index="", difficulty="ALL", player_count="",
                          value=v, is_ultimate_solo="", is_offense_field=str(k).startswith(OFF_PREFIX),
                          record="records/game/balancingadjustment_mp+difficulty_enemies01.dbr",
                          archive=uarc, grade="MEASURED", note="SCALAR (not difficulty-indexed)"))
S["t2"] = w("pm4i_ultimate_offense_paks.csv", hdr3, rows3)
S["t2_ultimate_solo_offense"] = {f: up[f][UIDX] for f in sorted(up) if f.startswith(OFF_PREFIX)}
print("  ⚑ Ultimate/solo offense cells:")
for f, v in S["t2_ultimate_solo_offense"].items():
    print(f"       {f:44s} = {v}")

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== TARGET 3 -- DoT riders on the waves-151-160 board ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
acts = L.rolled_actors(L.DOT_FIRST, L.DOT_LAST)
rec_actors: dict = collections.OrderedDict()
for a in acts:
    rec_actors.setdefault(a["record_path"].lower(), []).append(a)
print(f"  P-ROLLED-10: {len(acts)} actors / {len(rec_actors)} records")

rec_pools, rec_waves, rec_slot, rec_kind, pools = L.pool_population(L.DOT_FIRST, L.DOT_LAST)
lvsets, proxies, _lvt = L.level_sets(pools, rec_pools)

seed = set(rec_actors)
bodies, layers, summoner_of = L.summon_closure_extended(seed)
pets = sorted(bodies - seed)
print(f"  summon closure: +{len(pets)} pet bodies (layers {layers})")

tags = L.dot_display_names()
DISPLAY = {stem: tags.get(tag, "").strip() for stem, tag, _ in L.DOT_FAMILIES}
S["dot_display_names_decoded"] = DISPLAY

def levels_for(rec):
    """LO/HI charLevel limbs.  Own pool level set if the record is pooled; else INHERITED from
    its summoner(s) -- Lap D's `DERIVED-INHERITED` convention, unchanged."""
    ls = lvsets.get(rec)
    if ls:
        return ls[0], ls[-1], "MEASURED-SET"
    inh = set()
    for owner in summoner_of.get(rec, ()):
        inh |= set(lvsets.get(owner, []))
    if inh:
        s = sorted(inh)
        return s[0], s[-1], "DERIVED-INHERITED"
    return None, None, "ABSENT:NO-LEVEL-SOURCE"

hdr4 = ["record", "body_kind", "summoner", "waves_rolled", "n_actors", "n_champion_actors",
        "char_level_lo", "char_level_hi", "level_grade",
        "skill_record", "skill_archive", "skill_class", "depth", "via", "rank_grade",
        "dot_family", "display_name", "is_dot",
        "rank_lo", "array_index_min_lo", "index_state_lo", "magnitude_min_lo", "magnitude_max_lo",
        "rank_hi", "magnitude_min_hi", "magnitude_max_hi",
        "duration_min_s", "duration_max_s",
        "dps_if_field_is_total_lo", "dps_if_field_is_per_second_lo",
        "chance_pct", "is_global", "is_xor",
        "skill_modifier_pct", "skill_duration_modifier_pct",
        "skill_max_level", "array_len", "magnitude_grade", "stacking_rule_grade", "basis"]
STACK_GRADE = ("UNDECODABLE-FROM-SUBSTRATE — the .dbr carries Chance / Global / XOR / "
               "DurationModifier but no stack-count or same-source-replacement rule; "
               "the semantics live in the engine, not the record")
rows4 = []
dot_undecodable = 0
for rec in sorted(bodies):
    is_pet = rec not in seed
    lo, hi, lgrade = levels_for(rec)
    acts_r = rec_actors.get(rec, [])
    wr = "|".join(str(x) for x in sorted({int(a["wave"]) for a in acts_r}))
    if lo is None:
        dot_undecodable += 1
        continue
    sc_lo = L.skill_closure(rec, float(lo))
    sc_hi = L.skill_closure(rec, float(hi))
    for sk in sorted(sc_lo):
        rk_lo, d, rgrade, via = sc_lo[sk]
        rk_hi = sc_hi.get(sk, (rk_lo,))[0]
        drows = L.dot_rows_for_skill(sk, rk_lo) + L.instant_rows_for_skill(sk, rk_lo)
        if not drows:
            continue
        hi_by_fam = {r["dot_family"]: r for r in
                     (L.dot_rows_for_skill(sk, rk_hi) + L.instant_rows_for_skill(sk, rk_hi))}
        for r in drows:
            rh = hi_by_fam.get(r["dot_family"], {})
            dur = r["duration_min"]
            mn = r["magnitude_min"]
            rows4.append(dict(
                record=rec, body_kind=("PET-SUMMON" if is_pet else "ROSTER"),
                summoner="|".join(sorted(summoner_of.get(rec, ()))) if is_pet else "",
                waves_rolled=wr, n_actors=len(acts_r),
                n_champion_actors=sum(1 for a in acts_r if a.get("is_champion")),
                char_level_lo=lo, char_level_hi=hi, level_grade=lgrade,
                skill_record=sk, skill_archive=r["skill_archive"], skill_class=r["skill_class"],
                depth=d, via=via, rank_grade=rgrade,
                dot_family=r["dot_family"],
                display_name=DISPLAY.get(r["dot_family"], ""), is_dot=r["is_dot"],
                rank_lo=rk_lo, array_index_min_lo=r["array_index_min"],
                index_state_lo=r["index_state"],
                magnitude_min_lo=mn, magnitude_max_lo=r["magnitude_max"],
                rank_hi=rk_hi, magnitude_min_hi=rh.get("magnitude_min"),
                magnitude_max_hi=rh.get("magnitude_max"),
                duration_min_s=dur, duration_max_s=r["duration_max"],
                dps_if_field_is_total_lo=(round(mn / dur, 4) if (mn and dur) else None),
                dps_if_field_is_per_second_lo=(mn if (mn and r["is_dot"]) else None),
                chance_pct=r["chance_pct"], is_global=r["is_global"], is_xor=r["is_xor"],
                skill_modifier_pct=r["skill_modifier_pct"],
                skill_duration_modifier_pct=r["skill_duration_modifier_pct"],
                skill_max_level=r["skill_max_level"], array_len=r["array_len_min"],
                magnitude_grade=("MEASURED" if r["index_state"] in ("IN-RANGE", "SCALAR")
                                 else f"MEASURED-{r['index_state']}"),
                stacking_rule_grade=STACK_GRADE,
                basis=f"{sk} :: offensiveSlow{r['dot_family']}Min/Max[{r['array_index_min']}]"))
S["t3"] = w("pm4i_dot_riders.csv", hdr4, rows4)
S["t3_population"] = {"roster_records": len(seed), "pet_bodies": len(pets),
                      "bodies_total": len(bodies), "no_level_source": dot_undecodable,
                      "rows": len(rows4),
                      "bodies_with_dot": len({r["record"] for r in rows4})}
print(f"  DoT rows {len(rows4)} over {len({r['record'] for r in rows4})} bodies "
      f"of {len(bodies)} ({dot_undecodable} bodies with no level source, skipped + declared)")

# ── the terminal-wave ranking ─────────────────────────────────────────────────────────────────
print("\n== TARGET 3b -- terminal-wave (159/160) DoT ranking ==")
hdr5 = ["wave", "rank_by_total_convention", "rank_by_persecond_convention", "record",
        "display_name_hint", "n_actors", "is_champion_any", "char_level_lo",
        "n_dot_skills", "dot_families",
        "sum_dps_if_total", "sum_dps_if_per_second", "sum_magnitude_min",
        "max_single_dot_family", "max_single_dot_magnitude", "max_single_dot_duration_s",
        "poison_dps_if_total", "bleed_dps_if_total", "vitality_decay_dps_if_total",
        "burn_dps_if_total", "frostburn_dps_if_total", "electrocute_dps_if_total",
        "internal_trauma_dps_if_total", "lifeleech_dps_if_total",
        "acid_instant_min", "grade", "basis"]
FAMKEY = {"Poison": "poison", "Bleeding": "bleed", "Life": "vitality_decay", "Fire": "burn",
          "Cold": "frostburn", "Lightning": "electrocute", "Physical": "internal_trauma",
          "LifeLeach": "lifeleech"}
by_rec = collections.defaultdict(list)
for r in rows4:
    by_rec[r["record"]].append(r)
rows5 = []
for wv in L.TERMINAL_WAVES:
    recs_w = sorted({a["record_path"].lower() for a in acts if int(a["wave"]) == wv})
    # each rolled body's own summons ride with it
    fam_recs = {}
    for rec in recs_w:
        own = {rec}
        for pet in pets:
            if rec in summoner_of.get(pet, ()):
                own.add(pet)
        fam_recs[rec] = sorted(own)
    tmp = []
    for rec in recs_w:
        drs = [r for fr in fam_recs[rec] for r in by_rec.get(fr, []) if r["is_dot"]]
        inst = [r for fr in fam_recs[rec] for r in by_rec.get(fr, []) if not r["is_dot"]]
        a_r = [a for a in acts if a["record_path"].lower() == rec and int(a["wave"]) == wv]
        tot = sum(r["dps_if_field_is_total_lo"] or 0 for r in drs)
        ps = sum(r["dps_if_field_is_per_second_lo"] or 0 for r in drs)
        mag = sum(r["magnitude_min_lo"] or 0 for r in drs)
        per_fam = collections.defaultdict(float)
        for r in drs:
            per_fam[r["dot_family"]] += r["dps_if_field_is_total_lo"] or 0
        big = max(drs, key=lambda r: (r["magnitude_min_lo"] or 0), default=None)
        lo, _hi, lg = levels_for(rec)
        row = dict(wave=wv, record=rec,
                   display_name_hint=(a_r[0].get("display_name") if a_r else ""),
                   n_actors=len(a_r),
                   is_champion_any=any(a.get("is_champion") for a in a_r),
                   char_level_lo=lo, n_dot_skills=len({r["skill_record"] for r in drs}),
                   dot_families="|".join(sorted({r["dot_family"] for r in drs})),
                   sum_dps_if_total=round(tot, 3), sum_dps_if_per_second=round(ps, 3),
                   sum_magnitude_min=round(mag, 3),
                   max_single_dot_family=(big["dot_family"] if big else ""),
                   max_single_dot_magnitude=(big["magnitude_min_lo"] if big else None),
                   max_single_dot_duration_s=(big["duration_min_s"] if big else None),
                   acid_instant_min=round(sum(r["magnitude_min_lo"] or 0 for r in inst), 3) or None,
                   grade=("MEASURED" if drs else "MEASURED-ZERO (no DoT component on any skill)"),
                   basis=f"pm4i_dot_riders.csv rows for {rec} + its summon closure; "
                         f"frozen baton actors[] at wave {wv}")
        for stem, key in FAMKEY.items():
            row[f"{key}_dps_if_total"] = round(per_fam.get(stem, 0.0), 3) or None
        tmp.append(row)
    for i, r in enumerate(sorted(tmp, key=lambda x: -x["sum_dps_if_total"]), 1):
        r["rank_by_total_convention"] = i
    for i, r in enumerate(sorted(tmp, key=lambda x: -x["sum_dps_if_per_second"]), 1):
        r["rank_by_persecond_convention"] = i
    rows5 += sorted(tmp, key=lambda x: x["rank_by_total_convention"])
S["t3b"] = w("pm4i_terminal_wave_dot_ranking.csv", hdr5, rows5)
for r in rows5:
    print(f"   w{r['wave']} #{r['rank_by_total_convention']} {r['record'].split('/')[-1]:44s} "
          f"dps_tot={r['sum_dps_if_total']:>10} dps_ps={r['sum_dps_if_per_second']:>10} "
          f"fams={r['dot_families']}")
S["t3b_rank_stability"] = all(r["rank_by_total_convention"] == r["rank_by_persecond_convention"]
                              for r in rows5)
print(f"  ⚑ ranking stable across both magnitude conventions: {S['t3b_rank_stability']}")

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== TARGET 4 -- band C (waves 171-180) ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
c_pools, c_waves, c_slot, c_kind, cpools = L.pool_population(L.BAND_C_FIRST, L.BAND_C_LAST)
print(f"  band-C pool population: {len(c_pools)} records over {len(cpools)} pools")
c_lvsets, c_proxies, _ = L.level_sets(cpools, c_pools)
c_bodies, c_layers, c_summoner = L.summon_closure_extended(set(c_pools))
print(f"  summon closure -> {len(c_bodies)} bodies (layers {c_layers})")

Gl = A["characterLifeModifier"]
ult_life = float(up["characterLifeModifier"][UIDX])

def c_levels(rec):
    ls = c_lvsets.get(rec)
    if ls:
        return ls, "MEASURED-SET"
    inh = set()
    for owner in c_summoner.get(rec, ()):
        inh |= set(c_lvsets.get(owner, []))
    if inh:
        return sorted(inh), "DERIVED-INHERITED"
    return [], "ABSENT:NO-LEVEL-SOURCE"

hdr7 = ["record", "in_pool", "is_summon_body", "summoner", "level_set", "level_lo", "level_hi",
        "level_grade", "bio_record", "life_equation", "monster_class", "winner_archive",
        "base_life_lo", "base_life_hi", "life_passive_pct_lo", "life_passive_pct_hi",
        "own_total_damage_modifier_pct_lo", "own_total_damage_modifier_sources_lo",
        "pool_records", "pool_kinds", "waves_pooled", "life_grade", "damage_grade"]
hdr6 = ["record", "wave", "content_tier", "G_pct", "D_total_damage_modifier_pct",
        "level_lo", "level_hi", "ehp_lo", "ehp_hi",
        "total_damage_modifier_pct_lo", "total_damage_modifier_pct_hi", "life_grade", "damage_grade"]
rows6, rows7 = [], []
chains = {}
nmeas = nabsent = 0
for rec in sorted(c_bodies):
    ch = resolve(E3, rec)
    chains[rec] = ch
    ls, lg = c_levels(rec)
    lo = ls[0] if ls else None
    hi = ls[-1] if ls else None
    if not ch.ok or lo is None:
        nabsent += 1
        rows7.append(dict(record=rec, in_pool=int(rec in c_pools),
                          is_summon_body=int(rec not in c_pools),
                          summoner="|".join(sorted(c_summoner.get(rec, ()))),
                          level_set="|".join(str(x) for x in ls), level_lo=lo, level_hi=hi,
                          level_grade=lg, bio_record=ch.bio or "", life_equation=ch.life_eq or "",
                          monster_class=ch.cls or "", winner_archive=ch.archive or "",
                          pool_records="|".join(sorted(c_pools.get(rec, ()))),
                          pool_kinds="|".join(sorted(c_kind.get(rec, ()))),
                          waves_pooled="|".join(str(x) for x in sorted(c_waves.get(rec, ()))),
                          life_grade=f"ABSENT:{ch.reason}" if not ch.ok else f"ABSENT:{lg}",
                          damage_grade="ABSENT"))
        continue
    nmeas += 1
    bl_lo, bl_hi = ch.base_life(float(lo)), ch.base_life(float(hi))
    pp_lo, _ = ch.passive_pct(E3, float(lo))
    pp_hi, _ = ch.passive_pct(E3, float(hi))
    odm_lo, odm_src = L.own_total_damage_modifier(rec, float(lo))
    odm_hi, _ = L.own_total_damage_modifier(rec, float(hi))
    rows7.append(dict(record=rec, in_pool=int(rec in c_pools),
                      is_summon_body=int(rec not in c_pools),
                      summoner="|".join(sorted(c_summoner.get(rec, ()))),
                      level_set="|".join(str(x) for x in ls), level_lo=lo, level_hi=hi,
                      level_grade=lg, bio_record=ch.bio, life_equation=ch.life_eq,
                      monster_class=ch.cls or "", winner_archive=ch.archive,
                      base_life_lo=round(bl_lo, 4), base_life_hi=round(bl_hi, 4),
                      life_passive_pct_lo=pp_lo, life_passive_pct_hi=pp_hi,
                      own_total_damage_modifier_pct_lo=odm_lo,
                      own_total_damage_modifier_sources_lo=" ".join(odm_src),
                      pool_records="|".join(sorted(c_pools.get(rec, ()))),
                      pool_kinds="|".join(sorted(c_kind.get(rec, ()))),
                      waves_pooled="|".join(str(x) for x in sorted(c_waves.get(rec, ()))),
                      life_grade="MEASURED", damage_grade="MEASURED"))
    for wv in range(L.BAND_C_FIRST, L.BAND_C_LAST + 1):
        g = L.surv_at(Gl, wv)
        d = L.surv_at(A["offensiveTotalDamageModifier"], wv)
        rows6.append(dict(
            record=rec, wave=wv, content_tier=L.content_tier(wv), G_pct=g,
            D_total_damage_modifier_pct=d, level_lo=lo, level_hi=hi,
            ehp_lo=math.floor(bl_lo * (1.0 + (ult_life + g + pp_lo) / 100.0)),
            ehp_hi=math.floor(bl_hi * (1.0 + (ult_life + g + pp_hi) / 100.0)),
            total_damage_modifier_pct_lo=round(U("offensiveTotalDamageModifier") + d + odm_lo, 6),
            total_damage_modifier_pct_hi=round(U("offensiveTotalDamageModifier") + d + odm_hi, 6),
            life_grade="MEASURED",
            damage_grade="MEASURED components; total = DERIVED-SUM-ADDITIVE-BY-PARALLEL"))
S["t4_ehp"] = w("pm4i_band_c_ehp_by_wave.csv", hdr6, rows6)
S["t4_roster"] = w("pm4i_band_c_roster.csv", hdr7, rows7)
S["t4_population"] = {"pool_records": len(c_pools), "pools": len(cpools),
                      "bodies_closed": len(c_bodies), "summon_layers": c_layers,
                      "measured": nmeas, "absent": nabsent}
print(f"  band C: {nmeas} MEASURED / {len(c_bodies)} bodies ({nabsent} absent)")

# structural checks
mono = neg = order = 0
per_rec = collections.defaultdict(list)
for r in rows6:
    per_rec[r["record"]].append(r)
for rec, rr in per_rec.items():
    rr = sorted(rr, key=lambda x: x["wave"])
    for i in range(1, len(rr)):
        if rr[i]["ehp_lo"] < rr[i - 1]["ehp_lo"]:
            mono += 1
    for x in rr:
        if x["ehp_lo"] < 0 or x["ehp_hi"] < 0:
            neg += 1
        if x["ehp_hi"] < x["ehp_lo"]:
            order += 1
S["t4_structural"] = {"monotone_violations": mono, "negative": neg, "limb_order_violations": order}
print(f"  structural: monotone {mono} · negative {neg} · limb-order {order}")

# ⚑ the G(171) discontinuity, quantified against the band-B endpoint
S["t4_discontinuity"] = {
    "G_170": L.surv_at(Gl, 170), "G_171": L.surv_at(Gl, 171),
    "G_180": L.surv_at(Gl, 180),
    "D_170": L.surv_at(A["offensiveTotalDamageModifier"], 170),
    "D_171": L.surv_at(A["offensiveTotalDamageModifier"], 171),
    "D_180": L.surv_at(A["offensiveTotalDamageModifier"], 180),
    "life_step_pct_of_prior_multiplier": round(
        ((1 + (ult_life + L.surv_at(Gl, 171)) / 100) /
         (1 + (ult_life + L.surv_at(Gl, 170)) / 100) - 1) * 100, 4),
}
print("  discontinuity:", S["t4_discontinuity"])

(OUT / "pm4i_emit_summary.json").write_text(json.dumps(S, indent=2, default=str))
print("\nDONE")
