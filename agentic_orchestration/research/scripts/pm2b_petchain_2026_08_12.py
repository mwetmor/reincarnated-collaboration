#!/usr/bin/env python3
"""KC2-PM2 Lap B / task 3 -- THE F-6 GATE. The summon-skill -> pet-record chain.

Emits `tg2_pet_chain.csv`: one row per (owner identity, spawning skill, spawned record),
carrying the spawn contract (cap / burst / period / TTL / weight), the spawned body's own
stats (life via the same bio chain A6 validated, OA/DA, speeds, mesh, controller), its attack
surface counts, and a depth-2 flag for pets that themselves summon.

Damage magnitudes for these bodies ride `tg2_attack_damage.csv` (actor_kind=pet), so the
fight cell reads ONE damage table.

IS-3 (declared): spawn targets are classified by the TARGET RECORD'S `Class`, not by its path.
15 of the pet bodies live under `records/skills/.../pets/` while carrying `Class = Monster`;
83 spawn references resolve to `Class = Destructible` / `FixedItemContainer` (loot chests on
death) and are NOT threat. Both errors are in the prior lap's path-blind "92 identities summon".

READ-ONLY.
"""
import sys
import json
import argparse
import collections

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm2b_lib_2026_08_12 import (E3, roster, num, evaleq, tree_entries, tree_of, resolve_rank,
                                 n_ranks, offensive_families, bio_stats, declared_life_mods,
                                 spawn_targets, SPAWN_WEIGHT_FIELDS, SLOT_FIELDS, CHAIN_FIELDS,
                                 dump_csv, nested_refs)

ANM = json.load(open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                     "legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json"))
FPS = 30.0


def frames(ref):
    r = (ref or "").lower().replace("\\", "/")
    k = r[len("creatures/"):] if r.startswith("creatures/") else r
    e = ANM.get(k)
    return e["frames"] if e else None


def swing_period(creature):
    """Weighted unarmed basic-attack period, identical method to s2_extract (08-08 lineage)."""
    tbl = creature.get("charAnimationTableName")
    trec, _ = E3.merged(tbl) if isinstance(tbl, str) else (None, None)
    if not trec:
        return None, None
    dur, wt = [], []
    for i in (1, 2, 3):
        an = trec.get("unarmedAttackAnim%d" % i)
        if not (isinstance(an, str) and an.lower().endswith(".anm")):
            continue
        f = frames(an)
        sp = num(creature.get("unarmedAttackAnimSpeed%d" % i), 1.0) or 1.0
        w = num(creature.get("unarmedAttackAnimWeight%d" % i), 0.0) or 0.0
        if f:
            dur.append(f / FPS / sp)
            wt.append(w)
    if not dur:
        return None, tbl
    ws = sum(wt)
    base = (sum(d * w for d, w in zip(dur, wt)) / ws) if ws else sum(dur) / len(dur)
    cas = num(creature.get("characterAttackSpeed"), 1.0) or 1.0
    return base / cas, tbl


def attack_surface(creature):
    """(n_slots, n_tree, n_damage_bearing_skills) -- IS-4 aware: the nested
    buffSkillName / autoCastSkill chain is walked, because ground-effect pets (blood pools,
    voids, molten pools) carry ALL of their damage one pointer down."""
    slots = [creature[f] for _s, f in SLOT_FIELDS + CHAIN_FIELDS
             if isinstance(creature.get(f), str) and creature[f].lower().endswith(".dbr")]
    tre = tree_entries(creature)
    roots = set([x.lower() for x in slots] + [t[1] for t in tre])
    dmg, seen = 0, set()
    stack = list(roots)
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        s, _ = E3.merged(p)
        if not s:
            continue
        if offensive_families(s):
            dmg += 1
        stack += [q for _f, q in nested_refs(s)]
    return len(slots), len(tre), dmg


def spawn_refs(creature):
    """[(surface, slot_or_index, skill_path, level_eq)] for every skill on either surface."""
    out = []
    for slot, fld in SLOT_FIELDS + CHAIN_FIELDS:
        p = creature.get(fld)
        if isinstance(p, str) and p.lower().endswith(".dbr"):
            out.append(("slot", slot, p.lower(), None))
    tr = tree_of(creature)
    for idx, p, lvl in tree_entries(creature):
        out.append(("tree", idx, p, lvl))
    # a slot's rank is carried by its tree twin
    out = [(sf, sl, p, (lvl if lvl is not None else (tr[p][1] if p in tr else None)))
           for sf, sl, p, lvl in out]
    # IS-4: expand the nested chain so a spawn hidden behind buffSkillName / autoCastSkill
    # is still found; the nested skill inherits its parent's rank.
    seen = {p for _sf, _sl, p, _l in out}
    stack = list(out)
    while stack:
        sf, sl, p, lvl = stack.pop()
        s, _ = E3.merged(p)
        if not s:
            continue
        for _f, q in nested_refs(s):
            if q in seen:
                continue
            seen.add(q)
            ent = (sf + "+nested", sl, q, lvl)
            out.append(ent)
            stack.append(ent)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/leg_pm2b/tg2_pet_chain.csv")
    a = ap.parse_args()

    rows = []
    stat = collections.Counter()
    owners_monster, owners_nonmonster = set(), set()
    pet_records = set()

    # Frontier walk: roster identities at chain_depth 1, their pets' own summons at depth 2, ...
    # 9 pet bodies are spawner TURRETS that deal no damage themselves (Korvaak's Eldritch Rift is
    # the type case); their progeny carries the threat, so a depth-1-only chain would report those
    # summoners as harmless. Depth is bounded at 3 and every row states its own depth.
    frontier = [(r, None, 1) for r in roster()]
    walked = set()
    while frontier:
        r, parent_pet, chain_depth = frontier.pop(0)
        if chain_depth > 3:
            continue
        owner, _ = E3.merged(r["record"])
        if owner is None or (r["record"], parent_pet) in walked:
            continue
        walked.add((r["record"], parent_pet))
        lvl = r["level_min"] if r["level_min"] != "" else None
        seen = set()
        for surface, slot_or_idx, skill_path, lvl_eq in spawn_refs(owner):
            s, sown = E3.merged(skill_path)
            if s is None:
                continue
            tg = spawn_targets(s)
            if not tg:
                continue
            nr = n_ranks(s)
            rank_raw, rank_used, rank_grade = resolve_rank(lvl_eq, lvl, nr)
            for fld, tgt in tg:
                key = (r["record"], skill_path, tgt, surface, slot_or_idx)
                if key in seen:
                    continue
                seen.add(key)
                t, town = E3.merged(tgt)
                if t is None:
                    stat["spawn_target_UNRESOLVED"] += 1
                    rows.append(dict(owner_record=r["record"], spawn_skill=skill_path,
                                     spawn_target=tgt, status="SPAWN-TARGET-UNRESOLVED-IN-ARZ"))
                    continue
                cls = t.get("Class", "")
                stat["d%d_target_class_%s" % (chain_depth, cls or "EMPTY")] += 1
                if cls != "Monster":
                    if chain_depth == 1:
                        owners_nonmonster.add(r["record"])
                    rows.append(dict(
                        chain_depth=chain_depth, parent_pet_record=parent_pet or "",
                        owner_record=r["record"], owner_display_name=r["display_name"],
                        owner_stratum=r["stratum"], owner_level=lvl,
                        spawn_surface=surface, spawn_slot_or_tree_index=slot_or_idx,
                        spawn_skill=skill_path, spawn_skill_class=s.get("Class", ""),
                        spawn_field=fld, spawn_target=tgt, target_class=cls,
                        is_threat_actor=False,
                        status="NON-MONSTER-SPAWN (loot/destructible; not threat)"))
                    continue

                if chain_depth == 1:
                    owners_monster.add(r["record"])
                pet_records.add(tgt)
                frontier.append((dict(record=tgt,
                                      display_name=(tgt.rsplit("/", 1)[-1].replace(".dbr", "")),
                                      stratum="pet_of:" + r["stratum"],
                                      level_min=lvl, level_max=lvl),
                                 tgt, chain_depth + 1))

                weights = s.get(SPAWN_WEIGHT_FIELDS.get(fld, ""), None)
                pbio, plife, pda, poa = bio_stats(t, lvl)
                own_pct, own_flat, tree_pct = declared_life_mods(t)
                life_tot = (plife * (1 + (own_pct + tree_pct) / 100.0) + own_flat
                            if plife is not None else None)
                sw, tbl = swing_period(t)
                nslot, ntree, ndmg = attack_surface(t)

                # depth-2: does this pet itself spawn a Monster?
                nested = []
                for _sf, _si, p2, _lv in spawn_refs(t):
                    s2, _ = E3.merged(p2)
                    if not s2:
                        continue
                    for _f2, t2 in spawn_targets(s2):
                        r2, _ = E3.merged(t2)
                        if r2 is not None and r2.get("Class") == "Monster":
                            nested.append(t2)

                rows.append(dict(
                    chain_depth=chain_depth, parent_pet_record=parent_pet or "",
                    owner_record=r["record"], owner_display_name=r["display_name"],
                    owner_stratum=r["stratum"], owner_level=lvl,
                    spawn_surface=surface, spawn_slot_or_tree_index=slot_or_idx,
                    spawn_skill=skill_path, spawn_skill_class=s.get("Class", ""),
                    spawn_skill_arz_owners="|".join(sown),
                    spawn_skill_level_equation=lvl_eq if lvl_eq is not None else "",
                    spawn_skill_rank_used=rank_used if rank_used is not None else "",
                    spawn_skill_n_ranks=nr, spawn_skill_rank_grade=rank_grade,
                    spawn_field=fld, spawn_weight=weights if isinstance(weights, (int, float)) else
                    ("|".join(str(x) for x in weights) if isinstance(weights, list) else ""),
                    pet_record=tgt, target_class=cls, is_threat_actor=True,
                    pet_arz_owners="|".join(town),
                    # ---- spawn contract
                    pet_limit=num(s.get("petLimit")),
                    pet_burst_spawn=num(s.get("petBurstSpawn")),
                    pet_period_s=num(s.get("petPeriod")),
                    spawn_ttl_s=num(s.get("spawnObjectsTimeToLive")),
                    spawn_radius=num(s.get("spawnRadius")),
                    spawn_max_pet_count=num(s.get("spawnMaxPetCount")),
                    skill_cooldown_s=num(s.get("skillCooldownTime")),
                    skill_charge_duration_s=num(s.get("skillChargeDuration")),
                    skill_active_duration_s=num(s.get("skillActiveDuration")),
                    # ---- spawned body
                    pet_bio_record=pbio,
                    pet_char_level_equation=t.get("charLevel") if isinstance(
                        t.get("charLevel"), str) else "",
                    pet_base_life=round(plife) if plife is not None else "",
                    pet_life_own_mod_pct=own_pct, pet_life_tree_mod_pct=round(tree_pct, 2),
                    pet_life_at_owner_level=round(life_tot) if life_tot is not None else "",
                    pet_offensive_ability=round(poa, 2) if poa is not None else "",
                    pet_defensive_ability=round(pda, 2) if pda is not None else "",
                    pet_run_speed=num(t.get("characterRunSpeed")),
                    pet_attack_speed=num(t.get("characterAttackSpeed")),
                    pet_spellcast_speed=num(t.get("characterSpellCastSpeed")),
                    pet_dodge_pct=num(t.get("characterDodgePercent")),
                    pet_basic_swing_period_s=round(sw, 4) if sw else "",
                    pet_anim_table=tbl or "",
                    pet_controller=t.get("controller") if isinstance(
                        t.get("controller"), str) else "",
                    pet_mesh=t.get("mesh") if isinstance(t.get("mesh"), str) else "",
                    pet_scale=num(t.get("scale")),
                    pet_monster_classification=t.get("monsterClassification", ""),
                    pet_n_attack_slots=nslot, pet_n_tree_skills=ntree,
                    pet_n_damage_bearing_skills=ndmg,
                    pet_spawns_nested_monsters="|".join(sorted(set(nested))),
                    life_grade="MEASURED" if plife is not None else (
                        "BIO-EQ-UNEVALUABLE" if pbio else "NO-BIO-RECORD"),
                    oada_grade="MEASURED" if (poa is not None and pda is not None)
                    else "BIO-EQ-UNEVALUABLE",
                    swing_grade="MEASURED" if sw else "ANIM-NOT-RESOLVED",
                    status="OK",
                ))

    rows.sort(key=lambda x: (x.get("chain_depth", 9), x.get("owner_record", ""),
                             str(x.get("spawn_skill", "")), str(x.get("pet_record", ""))))
    dump_csv(a.out, rows)
    ok = [r for r in rows if r.get("status") == "OK"]
    print("stats:", dict(sorted(stat.items())))
    print("chain depth distribution (OK rows):",
          dict(collections.Counter(r["chain_depth"] for r in ok)))
    print("identities spawning a Class=Monster actor : %d / 169" % len(owners_monster))
    print("identities whose only spawns are non-Monster: %d"
          % len(owners_nonmonster - owners_monster))
    print("distinct pet Monster records               : %d" % len(pet_records))
    print("pet rows OK                                : %d" % len(ok))
    for g in ("life_grade", "oada_grade", "swing_grade"):
        print("  %-12s %s" % (g, dict(collections.Counter(r[g] for r in ok))))
    print("  pet_limit present  : %d/%d" % (sum(1 for r in ok if r["pet_limit"] not in (None, "")), len(ok)))
    print("  ttl present        : %d/%d" % (sum(1 for r in ok if r["spawn_ttl_s"] not in (None, "")), len(ok)))
    print("  pets with >=1 damage-bearing skill: %d/%d"
          % (sum(1 for r in ok if r["pet_n_damage_bearing_skills"]), len(ok)))
    nested = [r for r in ok if r["pet_spawns_nested_monsters"]]
    print("  depth-2 (pet summons a pet) rows   : %d" % len(nested))


if __name__ == "__main__":
    main()
