#!/usr/bin/env python3
"""KC2-PM4 Lap M -- Q1 emitter: the wave-159/160 ONE-SHOT CANDIDATE TABLE.

For every body that the Crucible's own spawn pools can place on waves 159 and 160 (plus the full
summon closure of those bodies), for every skill in that body's skill closure, this emits the
complete arithmetic chain from the `.dbr` flat magnitude to POST-MITIGATION damage against the
camera-measured player defence sheet -- and the maximum single-sim-tick delivery under three
named mechanism classes:

  single-hit      one application of one skill
  volley-overlap  `projectileLaunchNumber` co-landing projectiles (the geometric condition is
                  NAMED on the row; the table does not assert that the geometry occurs)
  ground-burst    radius/wave skills whose whole magnitude lands at once in an area

READ-ONLY.  OUTCOME-FIREWALLED.  GL-12: every emitted quantity carries its basis.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pm4m_lib_2026_08_14 import (  # noqa: E402
    E3, PLAYER, PLAYER_RES, INSTANT_STEMS, WAVES, WAVE_OF_DEATH,
    applied_to_player, attr_mult, body_stats, combatformulas, crit_tier,
    dump_csv, ev, hit_chance, pth, pth_effective, read_at_rank, sha256_of,
    skill_instant_damage, skill_stat_sum, _idx,
)
from pm4i_lib_2026_08_13 import (  # noqa: E402
    pool_population, level_sets, rolled_actors, surv_at, survival_arrays,
    difficulty_pak, skill_closure, creature_skill_slots, own_total_damage_modifier,
    summon_closure_extended, is_body,
)

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-m-death-mechanism")
OUT.mkdir(parents=True, exist_ok=True)

#: Skill classes whose damage is WEAPON-based (the creature's own passive weapon damage rides
#: along).  Enumerated from the class census of this population, not spelled from memory.
WEAPON_CLASSES = {
    "Skill_AttackWeapon", "Skill_AttackWeaponCharge", "Skill_AttackWeaponBlink",
    "Skill_WPAttack_BasicAttack", "Skill_WPAttack_AttackWave", "Skill_AttackPattern",
    "Skill_WeaponPool_BasicAttack", "Skill_WeaponPool_ChargedFinale",
    "Skill_WeaponPool_ChargedLinear", "Skill_WeaponPool_ChargedScaling",
    "Skill_AttackRadiusLeap", "Skill_AttackPathCharge",
}
RING_CLASSES = {"Skill_AttackProjectileRing", "SkillSecondary_AttackProjectileRing",
                "Skill_AttackProjectileFan", "Skill_AttackProjectileBurst",
                "Skill_AttackProjectile", "Skill_AttackProjectileAreaEffect",
                "SkillSecondary_AttackProjectileAreaEffect", "Skill_AttackProjectileDrop",
                "Skill_AttackProjectileSpawnPet"}
AREA_CLASSES = {"Skill_AttackRadius", "Skill_AttackWave", "Skill_AttackRadiusLightning",
                "Skill_AttackRadiusTeleport", "Skill_AttackSpellChaos",
                "Skill_AttackSpellTeleport", "Skill_AttackSpellChaosSpawnPet",
                "Skill_AttackBuffRadius", "Skill_BuffAttackRadiusDrop",
                "Skill_OnHitAttackRadius", "Skill_CharonGeysers"}


def _s(v):
    if isinstance(v, list):
        return v[0] if v else None
    return v


def base_weapon_damage(record: str, L: float):
    """The creature's own innate (unarmed/weapon) damage: SIGMA over depth-0 PASSIVE slots of the
    instant damage families at that slot's rank.  This is what a weapon-class skill adds to."""
    out = collections.defaultdict(lambda: [0.0, 0.0])
    srcs = []
    for sn, sl in creature_skill_slots(record):
        s, _ = E3.winner(sn)
        if not s:
            continue
        cls = str(s.get("Class") or "")
        if not cls.startswith("Skill_Passive") and cls not in ("SkillBuff_Passive",):
            continue
        try:
            rank = int(ev(sl, L)) if sl is not None else 1
        except Exception:
            rank = 1
        d = skill_instant_damage(sn, rank)
        for stem, (lo, hi, idx, st) in d.items():
            out[stem][0] += lo
            out[stem][1] += hi
            srcs.append(f"{sn.split('/')[-1]}:{stem}[{idx}]={lo:.0f}-{hi:.0f}")
    return {k: tuple(v) for k, v in out.items()}, srcs


def own_type_modifier(record: str, L: float, stem: str):
    """SIGMA_i skill_i.offensive<STEM>Modifier[rank_i(L)] over the body's OWN depth-0 slots, with
    `...ModifierChance` carried so a proc-gated modifier is visibly proc-gated."""
    total, chanced, src = 0.0, 0.0, []
    for sn, sl in creature_skill_slots(record):
        s, _ = E3.winner(sn)
        if not s:
            continue
        v = s.get(f"offensive{stem}Modifier")
        if v is None:
            continue
        try:
            rank = int(ev(sl, L)) if sl is not None else 1
        except Exception:
            rank = 1
        val, idx, _st = read_at_rank(v, rank)
        if not val:
            continue
        ch = s.get(f"offensive{stem}ModifierChance")
        ch = float(_s(ch) or 0)
        if ch:
            chanced += val
        else:
            total += val
        src.append(f"{sn.split('/')[-1]}[{idx}]={val:g}" + (f"@{ch:g}%" if ch else ""))
    return total, chanced, src


def main() -> None:
    surv = survival_arrays()
    pak, _pscal, _parc = difficulty_pak()
    cf = combatformulas()

    rec_pools, rec_waves, rec_slot, rec_kind, pools = pool_population(WAVES[0], WAVES[1])
    lvsets, proxies, _lvt = level_sets(pools, rec_pools)
    seeds = set(rec_pools)
    bodies, layers, via = summon_closure_extended(seeds)

    rolled = collections.defaultdict(set)
    for a in rolled_actors(WAVES[0], WAVES[1]):
        rolled[str(a.get("record_path", "")).lower().replace("\\", "/")].add(int(a["wave"]))

    # in-game display names, DECODED from the game's own text (never spelled from memory)
    from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file
    VEND = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
    NAMES = {}
    for sub in ("mods/survivalmode", "survivalmode3", "survivalmode1", "gdx3", "gdx2", "gdx1", ""):
        ap = VEND / sub / "resources" / "Text_EN.arc"
        if not ap.exists():
            continue
        _arc = ArcArchive(ap)
        for f in _arc.names():
            if not str(f).endswith(".txt"):
                continue
            try:
                for k, v in parse_tag_file(_arc.read_file(f)):
                    NAMES.setdefault(k, v)
            except Exception:
                pass

    def disp(rec: str) -> str:
        r, _ = E3.winner(rec)
        tag = _s((r or {}).get("description")) or ""
        return NAMES.get(str(tag), "")

    # inherit a summon's level set from its summoner
    for _ in range(6):
        for parent, kids in via.items():
            if parent not in lvsets:
                continue
            for k in kids:
                if k in bodies and k not in lvsets:
                    lvsets[k] = lvsets[parent]

    ult_total = float(pak["offensiveTotalDamageModifier"][8])
    wave_total = surv_at(surv["offensiveTotalDamageModifier"], WAVE_OF_DEATH)
    crit_dmg_mod = surv_at(surv["offensiveCritDamageModifier"], WAVE_OF_DEATH)

    rows = []
    body_rows = []
    for rec in sorted(bodies):
        lv = lvsets.get(rec)
        if not lv:
            body_rows.append(dict(body_record=rec, level_grade="NO-LEVEL-SOURCE"))
            continue
        L = float(max(lv))                       # HI level limb = the deadliest, which is the
        L_lo = float(min(lv))                    # question this lap asks
        st = body_stats(rec, L, WAVE_OF_DEATH, surv, pak)
        p_raw = pth(st["oa"], PLAYER["DA"])
        p_eff = pth_effective(st["oa"], PLAYER["DA"])
        tier, cmult = crit_tier(p_eff)
        own_total, own_total_src = own_total_damage_modifier(rec, L)
        total_mod = 1.0 + (ult_total + wave_total + own_total) / 100.0
        base_dmg, base_src = base_weapon_damage(rec, L)
        rrec, _ = E3.winner(rec)
        body_rows.append(dict(
            body_record=rec, level_grade="MEASURED-SET", level_lo=int(L_lo), level_hi=int(L),
            in_pool_waves="|".join(str(w) for w in sorted(rec_waves.get(rec, []))),
            pool_kind="|".join(sorted(rec_kind.get(rec, []))) or "SUMMON",
            in_frozen_baton_roll=("|".join(str(w) for w in sorted(rolled[rec])) or "NO"),
            monster_classification=str((rrec or {}).get("monsterClassification") or ""),
            description_tag=str((rrec or {}).get("description") or ""),
            display_name=disp(rec),
            bio_record=st["bio"], dexterity=round(st["dex"], 3), intelligence=round(st["intel"], 3),
            oa=round(st["oa"], 3), player_DA=PLAYER["DA"],
            pth_raw=round(p_raw, 4), pth_effective=round(p_eff, 4),
            hit_chance=round(hit_chance(p_eff), 6), crit_tier=tier, crit_mult=cmult,
            own_total_damage_modifier_pct=own_total,
            own_total_damage_modifier_sources="; ".join(own_total_src),
            total_damage_modifier_pct=ult_total + wave_total + own_total,
            base_weapon_damage="; ".join(base_src),
            attack_period_s=(float(_s((rrec or {}).get("characterAttackSpeed")) or 0) or ""),
        ))

        closure = skill_closure(rec, L)
        for sn, (rank, depth, rgrade, rvia) in sorted(closure.items()):
            s, sarc = E3.winner(sn)
            if not s:
                continue
            cls = str(s.get("Class") or "")
            dmg = skill_instant_damage(sn, rank)
            wdp = _s(s.get("weaponDamagePct"))
            wdp = float(wdp) if wdp else (100.0 if cls in WEAPON_CLASSES else 0.0)
            if not dmg and wdp <= 0:
                continue
            nproj = int(_s(s.get("projectileLaunchNumber")) or 0)
            nfragmin = int(_s(s.get("projectileFragmentsLaunchNumberMin")) or 0)
            nfragmax = int(_s(s.get("projectileFragmentsLaunchNumberMax")) or 0)
            rot = float(_s(s.get("projectileLaunchRotation")) or 0)
            pierce_ch = float(_s(s.get("projectilePiercingChance")) or 0)
            r1s = float(_s(s.get("projectileDamageRange1Scale")) or 0)
            r1max = float(_s(s.get("projectileDamageRange1Max")) or 0)
            r3s = float(_s(s.get("projectileDamageRange3Scale")) or 0)
            radius = float(_s(s.get("skillTargetRadius")) or 0)
            tgtnum = int(_s(s.get("skillTargetNumber")) or 0)
            cooldown = float(_s(s.get("skillCooldownTime")) or 0)
            pcl_min = float(_s(s.get("offensivePercentCurrentLifeMin")) or 0)
            pcl_max = float(_s(s.get("offensivePercentCurrentLifeMax")) or 0)

            if cls in RING_CLASSES:
                mech = "volley-overlap" if max(nproj, nfragmax) > 1 else "single-hit"
            elif cls in AREA_CLASSES:
                mech = "ground-burst"
            elif cls in WEAPON_CLASSES:
                mech = "single-hit"
            else:
                mech = "single-hit"

            # ---- the arithmetic chain, per damage family -------------------------------------
            per_type = {}
            applied_lo = applied_hi = 0.0
            applied_hi_noattr = 0.0
            raw_hi_total = 0.0
            clamped = []
            chain_bits = []
            stems = set(dmg) | (set(base_dmg) if wdp > 0 else set())
            for stem in sorted(stems):
                f_lo, f_hi = dmg.get(stem, (0.0, 0.0))[:2] if stem in dmg else (0.0, 0.0)
                b_lo, b_hi = base_dmg.get(stem, (0.0, 0.0)) if wdp > 0 else (0.0, 0.0)
                flat_lo = f_lo + b_lo * wdp / 100.0
                flat_hi = f_hi + b_hi * wdp / 100.0
                if flat_hi <= 0:
                    continue
                am = attr_mult(stem, st["dex"], st["intel"])
                own_t, own_t_ch, _src = own_type_modifier(rec, L, stem)
                wave_t = surv_at(surv[f"offensive{stem}Modifier"], WAVE_OF_DEATH) \
                    if f"offensive{stem}Modifier" in surv else 0.0
                ult_t = float(pak[f"offensive{stem}Modifier"][8]) \
                    if f"offensive{stem}Modifier" in pak else 0.0
                tmod_raw = 1.0 + (own_t + wave_t + ult_t) / 100.0
                tmod = max(0.0, tmod_raw)      # DERIVED-CLAMPED: a damage multiplier < 0 is 0
                if tmod_raw < 0:
                    clamped.append(f"{stem}({tmod_raw:+.2f})")
                raw_lo = flat_lo * am * total_mod * tmod
                raw_hi = flat_hi * am * total_mod * tmod
                a_lo = applied_to_player(stem, raw_lo)
                a_hi = applied_to_player(stem, raw_hi)
                a_hi_na = applied_to_player(stem, flat_hi * total_mod * tmod)
                per_type[stem] = (flat_hi, raw_hi, a_hi)
                applied_lo += a_lo
                applied_hi += a_hi
                applied_hi_noattr += a_hi_na
                raw_hi_total += raw_hi
                chain_bits.append(
                    f"{stem}: flat {flat_lo:.0f}-{flat_hi:.0f} x attr {am:.4f} x total "
                    f"{total_mod:.4f} x type {tmod:.4f}"
                    + (f" [CLAMPED from {tmod_raw:.4f}]" if tmod_raw < 0 else "")
                    + f" = raw {raw_hi:.0f} -> applied {a_hi:.0f}")
            # percent-current-life rides on top; at FULL health it is pct x 20005
            pcl_applied = PLAYER["hp_buffed"] * max(pcl_min, pcl_max) / 100.0
            if pcl_applied:
                chain_bits.append(
                    f"PercentCurrentLife: {max(pcl_min, pcl_max):g}% x 20005 (at full) "
                    f"= {pcl_applied:.0f}  [no resistance field known -- DECLARED]")

            if applied_hi <= 0 and pcl_applied <= 0:
                continue

            n_co = max(nproj, nfragmax, 1)
            single_lo = applied_lo + pcl_applied
            single_hi = applied_hi + pcl_applied
            single_hi_noattr = applied_hi_noattr + pcl_applied
            # projectile range-band scaling: band 1 is the melee-adjacent band an EoR player
            # occupies; band 3 is the far band.  Both carried; neither asserted as "the" case.
            r1 = (r1s / 100.0) if r1s else 1.0
            r3 = (r3s / 100.0) if r3s else 1.0
            import math as _m

            def _need(x):
                return _m.ceil(20005.0 / x) if x > 0 else ""
            rows.append(dict(
                body_record=rec,
                body_display_name=disp(rec),
                body_waves="|".join(str(w) for w in sorted(rec_waves.get(rec, []))) or "SUMMON",
                in_frozen_baton_roll=("|".join(str(w) for w in sorted(rolled[rec])) or "NO"),
                skill_record=sn, skill_archive=sarc, skill_class=cls,
                skill_depth=depth, rank=rank, rank_grade=rgrade,
                mechanism_class=mech,
                weapon_damage_pct=wdp,
                damage_families="|".join(sorted(per_type)),
                raw_total_hi=round(raw_hi_total, 2),
                applied_single_lo=round(single_lo, 2),
                applied_single_hi=round(single_hi, 2),
                applied_single_hi_crit=round(single_hi * cmult, 2),
                applied_single_hi_crit_ATTROFF=round(single_hi_noattr * cmult, 2),
                applied_volley_hi_crit_ATTROFF=round(single_hi_noattr * n_co * cmult, 2),
                type_modifier_clamped_to_zero=("|".join(clamped) or "NO"),
                crit_mult=cmult, crit_tier=crit_tier(pth_effective(st["oa"], PLAYER["DA"]))[0],
                projectile_launch_number=nproj,
                projectile_fragments_min=nfragmin, projectile_fragments_max=nfragmax,
                projectile_launch_rotation=rot, projectile_piercing_chance=pierce_ch,
                n_coincident_max=n_co,
                applied_volley_hi=round(single_hi * n_co, 2),
                applied_volley_hi_crit=round(single_hi * n_co * cmult, 2),
                applied_volley_hi_crit_r1scaled=round(single_hi * n_co * cmult * r1, 2),
                applied_single_hi_crit_r1=round(single_hi * cmult * r1, 2),
                applied_single_hi_crit_r3=round(single_hi * cmult * r3, 2),
                n_projectiles_needed_r2=_need(single_hi * cmult),
                n_projectiles_needed_r1=_need(single_hi * cmult * r1),
                n_projectiles_needed_r3=_need(single_hi * cmult * r3),
                n_projectiles_needed_ATTROFF_r2=_need(single_hi_noattr * cmult),
                n_projectiles_needed_ATTROFF_r3=_need(single_hi_noattr * cmult * r3),
                range1_scale_pct=r1s, range1_max_m=r1max, range3_scale_pct=r3s,
                skill_target_radius=radius, skill_target_number=tgtnum,
                skill_cooldown_s=cooldown,
                percent_current_life_pct=max(pcl_min, pcl_max),
                percent_current_life_at_full=round(pcl_applied, 2),
                reaches_20005_single=("YES" if single_hi * cmult >= 20005 else "NO"),
                reaches_20005_volley=("YES" if single_hi * n_co * cmult >= 20005 else "NO"),
                fraction_of_20005_single=round(single_hi * cmult / 20005.0, 5),
                fraction_of_20005_volley=round(single_hi * n_co * cmult / 20005.0, 5),
                arithmetic_chain=" | ".join(chain_bits),
            ))

    cand_cols = list(rows[0].keys())
    rows.sort(key=lambda r: -r["applied_volley_hi_crit"])
    d1 = dump_csv(OUT / "pm4m_candidate_table.csv", rows, cand_cols)
    body_cols = sorted({k for r in body_rows for k in r})
    body_cols = ["body_record", "level_grade", "level_lo", "level_hi", "in_pool_waves",
                 "pool_kind", "in_frozen_baton_roll", "monster_classification",
                 "description_tag", "display_name", "bio_record", "dexterity", "intelligence", "oa",
                 "player_DA", "pth_raw", "pth_effective", "hit_chance", "crit_tier",
                 "crit_mult", "own_total_damage_modifier_pct",
                 "own_total_damage_modifier_sources", "total_damage_modifier_pct",
                 "base_weapon_damage", "attack_period_s"]
    d2 = dump_csv(OUT / "pm4m_body_chain.csv", body_rows, body_cols)

    summary = dict(
        pool_records=len(rec_pools), bodies_with_summons=len(bodies), closure_layers=layers,
        candidate_rows=len(rows),
        wave_total_damage_modifier_pct=wave_total, ultimate_total_damage_modifier_pct=ult_total,
        wave_crit_damage_modifier_pct=crit_dmg_mod,
        max_applied_single_crit=max(r["applied_single_hi_crit"] for r in rows),
        max_applied_volley_crit=max(r["applied_volley_hi_crit"] for r in rows),
        n_single_reaching=sum(1 for r in rows if r["reaches_20005_single"] == "YES"),
        n_volley_reaching=sum(1 for r in rows if r["reaches_20005_volley"] == "YES"),
        digests={"pm4m_candidate_table.csv": d1, "pm4m_body_chain.csv": d2},
    )
    (OUT / "pm4m_emit_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print("\nTOP 25 by volley-crit:")
    for r in rows[:25]:
        print(f"  {r['applied_volley_hi_crit']:12,.0f}  x{r['n_coincident_max']:<3d} "
              f"{r['applied_single_hi_crit']:11,.0f}  {r['mechanism_class']:<15s} "
              f"{r['body_record'].split('/')[-1]:<38s} {r['skill_record'].split('/')[-1]}")


if __name__ == "__main__":
    main()
