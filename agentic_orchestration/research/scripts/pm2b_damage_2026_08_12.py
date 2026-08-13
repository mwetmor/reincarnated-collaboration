#!/usr/bin/env python3
"""KC2-PM2 Lap B / task 1 -- per-rank damage MAGNITUDES for the E-s09-cp150 roster.

Emits `tg2_attack_damage.csv`: one row per
    (identity, surface, slot-or-tree-index, skill record, offensive family)
carrying the value at the rank the Crucible actually assigns, the full rank table, and a
provenance + grade column on every quantity.

Joins: `record` + `skill` against tg2_attack_slots.csv / tg2_skill_tree.csv;
       `record` against tg2_monster_timing.csv / tg2_monster_stats.csv.

Pets are included when --pets is passed (actor_kind=pet, owner_record populated), so the
fight cell reads ONE damage table for every body that can hit the player.

READ-ONLY.
"""
import sys
import argparse

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm2b_lib_2026_08_12 import (E3, roster, num, as_list, offensive_families, n_ranks,
                                 at_rank, tree_of, tree_entries, resolve_rank, evaleq,
                                 SLOT_FIELDS, CHAIN_FIELDS, dump_csv, spawn_targets,
                                 nested_refs)

MAXRANKDUMP = 60   # full table emitted up to this many ranks; beyond it, head+tail


def rank_table(v, limit=MAXRANKDUMP):
    vals = as_list(v)
    if not vals:
        return ""
    if len(vals) <= limit:
        return "|".join(("%g" % x) for x in vals)
    return "|".join(("%g" % x) for x in vals[:limit]) + "|...(%d more)" % (len(vals) - limit)


def emit_for_actor(rows, stat, rec_path, creature, char_level, actor_kind,
                   owner_record="", display_name="", stratum=""):
    """Walk both skill surfaces of ONE creature record and emit every damage-bearing family."""
    tree = tree_of(creature)
    # ALTERNATE RANK BASIS (residual R-2 in the lap README): the creature record carries its own
    # `charLevel` equation. Whether the baton's per-actor level is already post-equation is not
    # decidable from the corpus, so BOTH bases are computed and the divergence is counted.
    char_level_eq = creature.get("charLevel") if isinstance(creature.get("charLevel"), str) else ""
    char_level_adj = evaleq(char_level_eq, char_level) if (
        char_level_eq and char_level is not None) else None

    surfaces = []
    for slot, fld in SLOT_FIELDS + CHAIN_FIELDS:
        p = creature.get(fld)
        if isinstance(p, str) and p.lower().endswith(".dbr"):
            # a slot's rank is carried ONLY by its tree twin (663/667 slots are in the tree)
            surfaces.append(("slot", slot, "", p.lower(),
                             tree[p.lower()][1] if p.lower() in tree else None,
                             "TREE-LEVEL-EQUATION" if p.lower() in tree else "SLOT-NOT-IN-TREE"))
    for idx, p, lvl in tree_entries(creature):
        surfaces.append(("tree", "", idx, p, lvl, "TREE-LEVEL-EQUATION"))

    # IS-4: each top-level surface skill is expanded into its nested chain
    # (buffSkillName / autoCastSkill), depth-first, cycle-guarded.
    expanded = []
    for surface, slot, tree_index, skill_path, lvl_eq, rank_source in surfaces:
        stack = [(skill_path, 0, "", "")]
        seen_chain = {skill_path}
        while stack:
            p, depth, via, parent = stack.pop()
            expanded.append((surface, slot, tree_index, skill_path, lvl_eq, rank_source,
                             p, depth, via, parent))
            s2, _ = E3.merged(p)
            if s2 is None:
                continue
            for f, q in nested_refs(s2):
                if q in seen_chain:
                    stat["nest_CYCLE-BLOCKED"] += 1
                    continue
                seen_chain.add(q)
                stack.append((q, depth + 1, f, p))

    for (surface, slot, tree_index, root_skill, lvl_eq, rank_source,
         skill_path, nest_depth, nest_via, nest_parent) in expanded:
        s, own = E3.merged(skill_path)
        if s is None:
            stat["skill_UNRESOLVED-IN-ARZ"] += 1
            rows.append(dict(actor_kind=actor_kind, owner_record=owner_record, record=rec_path,
                             display_name=display_name, stratum=stratum, level_used=char_level,
                             surface=surface, slot=slot, tree_index=tree_index,
                             skill=skill_path, nest_depth=nest_depth, nest_via_field=nest_via,
                             nest_parent_skill=nest_parent, root_skill=root_skill,
                             status="SKILL-UNRESOLVED-IN-ARZ"))
            continue

        fams = offensive_families(s)
        nr = n_ranks(s)

        # ---- IS-2 rank assignment: the tree entry is the ONLY rank carrier in the corpus.
        rank_raw, rank_used, rank_grade = resolve_rank(lvl_eq, char_level, nr)
        if rank_source == "SLOT-NOT-IN-TREE":
            rank_grade = "SLOT-RANK-UNASSIGNED"
        if nest_depth:
            # DECLARED: a nested skill carries no level equation of its own anywhere in this
            # corpus; it is resolved at the rank of the surface skill that invoked it.
            rank_source = "INHERITED-FROM-PARENT-RANK"
        stat["rank_" + rank_grade] += 1
        _, rank_alt, _ = resolve_rank(lvl_eq, char_level_adj, nr) if (
            char_level_adj is not None) else (None, None, "")
        if rank_used is not None and rank_alt is not None and rank_alt != rank_used:
            stat["rank_ALT-BASIS-DIVERGES"] += 1

        if not fams:
            stat["skill_no_damage_family"] += 1
            continue
        stat["skill_with_damage"] += 1

        # ---- delivery geometry + wind-up, for F-4 telegraph identification.
        # Census correction: `skillTargetRadius` (84 of 506 damage skills) is NOT the roster's
        # main AOE carrier. `projectileExplosionRadius` covers 140, and the expanding-wave block
        # (waveStartWidth/waveEndWidth/waveDepth/waveDistance/waveTime/expansionTime) another
        # ~51. A telegraph rule keyed on skillTargetRadius alone sees under a third of the AOE.
        pn = s.get("skillProjectileName")
        pvel = pdist = plaunch = None
        if isinstance(pn, str) and pn.lower().endswith(".dbr"):
            pr, _ = E3.merged(pn)
            if pr:
                pvel = num(pr.get("projectileVelocity"))
                pdist = num(pr.get("projectileDistance"))
                plaunch = num(pr.get("launchAngle"))
        geom = dict(
            projectile=pn if isinstance(pn, str) else "",
            projectile_velocity=pvel, projectile_distance=pdist,
            projectile_launch_angle=plaunch,
            projectile_explosion_radius=num(s.get("projectileExplosionRadius")),
            projectile_number=num(s.get("skillProjectileNumber")),
            projectile_launch_number=num(s.get("projectileLaunchNumber")),
            projectile_piercing_chance=num(s.get("projectilePiercingChance")),
            projectile_dmg_range1_min=num(s.get("projectileDamageRange1Min")),
            projectile_dmg_range1_max=num(s.get("projectileDamageRange1Max")),
            projectile_dmg_range1_scale=num(s.get("projectileDamageRange1Scale")),
            projectile_dmg_range2_min=num(s.get("projectileDamageRange2Min")),
            projectile_dmg_range2_max=num(s.get("projectileDamageRange2Max")),
            projectile_dmg_range2_scale=num(s.get("projectileDamageRange2Scale")),
            projectile_dmg_range3_min=num(s.get("projectileDamageRange3Min")),
            projectile_dmg_range3_max=num(s.get("projectileDamageRange3Max")),
            projectile_dmg_range3_scale=num(s.get("projectileDamageRange3Scale")),
            wave_start_width=num(s.get("waveStartWidth")),
            wave_end_width=num(s.get("waveEndWidth")),
            wave_depth=num(s.get("waveDepth")),
            wave_distance=num(s.get("waveDistance")),
            wave_time_s=num(s.get("waveTime")),
            expansion_time_s=num(s.get("expansionTime")),
            skill_allows_warmup=s.get("skillAllowsWarmUp", ""),
            warmup_effect=s.get("warmUpEffectName", ""),
            skill_charge_level=num(s.get("skillChargeLevel")),
            camera_shake_duration_s=num(s.get("cameraShakeDurationSecs")),
            weapon_damage_pct=num(s.get("weaponDamagePct")),
            instant_cast=s.get("instantCast", ""),
            distance_profile=s.get("distanceProfile", ""),
        )

        for famkey, d in sorted(fams.items()):
            grp, kind = d["__group__"], d["__kind__"]
            vmin, gmin = at_rank(d.get("Min"), rank_used)
            vmax, gmax = at_rank(d.get("Max"), rank_used)
            dmin, gdmin = at_rank(d.get("DurationMin"), rank_used)
            dmax, _ = at_rank(d.get("DurationMax"), rank_used)
            chance, _ = at_rank(d.get("Chance"), rank_used)
            modif, _ = at_rank(d.get("Modifier"), rank_used)

            # Declared rule: a zero/absent Max means "no roll range"; the Min is the fixed value.
            max_eff = vmax if (vmax not in (None, 0.0)) else vmin

            # DoT: the .arz stores value + duration. Which of the two readings the engine uses
            # is NOT declared anywhere in the corpus (see hit-math.md SEM-1) -- BOTH are emitted.
            dot_dur = dmin if dmin not in (None, 0.0) else None
            dot_a = vmin if kind == "dot" else None                       # raw is per-second
            dot_b = (vmin / dot_dur) if (kind == "dot" and vmin is not None
                                         and dot_dur) else None            # raw is the total

            rows.append(dict(
                actor_kind=actor_kind, owner_record=owner_record,
                record=rec_path, display_name=display_name, stratum=stratum,
                level_used=char_level,
                surface=surface, slot=slot, tree_index=tree_index,
                skill=skill_path, skill_class=s.get("Class", ""),
                root_skill=root_skill, nest_depth=nest_depth,
                nest_via_field=nest_via, nest_parent_skill=nest_parent,
                provenance_dbr_path=skill_path, arz_owners="|".join(own),
                damage_type=famkey.replace("offensive", ""),
                template_group=grp, kind=kind,
                rank_source=rank_source, skill_level_equation=lvl_eq if lvl_eq is not None else "",
                rank_raw=round(rank_raw, 4) if rank_raw is not None else "",
                rank_used=rank_used if rank_used is not None else "",
                n_ranks=nr, rank_grade=rank_grade,
                char_level_equation=char_level_eq,
                char_level_adjusted=round(char_level_adj, 3) if char_level_adj is not None else "",
                rank_used_alt_basis=rank_alt if rank_alt is not None else "",
                min=vmin, max=vmax, max_effective=max_eff,
                min_grade=gmin, max_grade=gmax,
                dot_duration_s=dot_dur, dot_duration_max_s=dmax,
                dot_dps_if_field_is_per_second=dot_a,
                dot_dps_if_field_is_total=round(dot_b, 4) if dot_b is not None else None,
                chance_pct=chance,
                is_global=d.get("Global", ""), is_xor=d.get("XOR", ""),
                modifier_pct=modif,
                skill_cooldown_s=num(s.get("skillCooldownTime")),
                skill_charge_duration_s=num(s.get("skillChargeDuration")),
                skill_active_duration_s=num(s.get("skillActiveDuration")),
                skill_target_radius=num(s.get("skillTargetRadius")),
                skill_target_number=num(s.get("skillTargetNumber")),
                skill_target_angle=num(s.get("skillTargetAngle")),
                skill_target_interval_s=num(s.get("skillTargetInterval")),
                time_between_attacks_ms=num(s.get("timeBetweenAttacks")),
                rank_table_min=rank_table(d.get("Min")),
                rank_table_max=rank_table(d.get("Max")),
                rank_table_duration=rank_table(d.get("DurationMin")),
                status="OK",
                **geom,
            ))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/leg_pm2b/tg2_attack_damage.csv")
    ap.add_argument("--pets", action="store_true",
                    help="also walk every Class=Monster spawn target (F-6 gate substrate)")
    a = ap.parse_args()

    import collections
    rows, stat = [], collections.Counter()

    ros = roster()
    for r in ros:
        rec, _ = E3.merged(r["record"])
        if rec is None:
            stat["record_UNRESOLVED"] += 1
            continue
        lvl = r["level_min"] if r["level_min"] != "" else None
        emit_for_actor(rows, stat, r["record"], rec, lvl, "roster",
                       display_name=r["display_name"], stratum=r["stratum"])

    if a.pets:
        # one hop: owner -> spawning skill -> Class=Monster target. Pet char level is
        # DECLARED as the owner's level (GD pets inherit the summoner's level); the pet's own
        # charLevel equation is carried on the pet-chain CSV so the assumption is auditable.
        def monster_spawns(creature):
            """Class=Monster spawn targets of one body, across BOTH skill surfaces and the
            IS-4 nested chain (spawner turrets hide their generator one pointer down)."""
            roots = set(tree_of(creature)) | {creature[f].lower()
                                              for _, f in SLOT_FIELDS + CHAIN_FIELDS
                                              if isinstance(creature.get(f), str)
                                              and creature[f].lower().endswith(".dbr")}
            out, seen, stack = set(), set(), list(roots)
            while stack:
                p = stack.pop()
                if p in seen:
                    continue
                seen.add(p)
                s, _ = E3.merged(p)
                if not s:
                    continue
                stack += [q for _f, q in nested_refs(s)]
                for _fld, tgt in spawn_targets(s):
                    t, _ = E3.merged(tgt)
                    if t is not None and t.get("Class") == "Monster":
                        out.add(tgt)
            return out

        # Pet char level is DECLARED as the ROOT owner's level (GD pets inherit the summoner's
        # level); the pet's own charLevel equation rides tg2_pet_chain.csv so the assumption is
        # auditable. Depth 2 is walked because 9 chain rows are spawner turrets whose progeny
        # carry all of the threat (e.g. Korvaak's Eldritch Rift -> servant generator).
        pets, frontier, depth = {}, [], 1
        for r in ros:
            rec, _ = E3.merged(r["record"])
            if rec is None:
                continue
            lvl = r["level_min"] if r["level_min"] != "" else None
            for tgt in monster_spawns(rec):
                frontier.append((tgt, r["record"], lvl, 1))
        while frontier and depth <= 3:
            nxt = []
            for tgt, owner, lvl, d in frontier:
                if (tgt, owner) in pets:
                    continue
                t, _ = E3.merged(tgt)
                if t is None:
                    continue
                pets[(tgt, owner)] = (t, lvl, d)
                for t2 in monster_spawns(t):
                    nxt.append((t2, owner, lvl, d + 1))
            frontier = nxt
            depth += 1
        for (tgt, owner), (t, lvl, d) in sorted(pets.items()):
            emit_for_actor(rows, stat, tgt, t, lvl, "pet", owner_record=owner,
                           display_name=t.get("description", "") if isinstance(
                               t.get("description"), str) else "",
                           stratum="pet_depth%d" % d)
        stat["pet_actor_rows"] = len(pets)
        stat["pet_bodies_distinct"] = len({k[0] for k in pets})

    dump_csv(a.out, rows)
    print("stats:", dict(sorted(stat.items())))


if __name__ == "__main__":
    main()
