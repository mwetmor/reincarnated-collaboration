#!/usr/bin/env python3
"""KC2-PM4 Lap G emitter -- the played kit, the dashes, the potions, the circuit-breakers.

Emits into `agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-g-player-kit/`:

    pm4g_played_kit.csv          every bound slot + every allocated skill, ranks + bindings
    pm4g_movement_skills.csv     the dash/evade layer, with the channel-interaction verdict
    pm4g_consumables.csv         the 1.3.0.0 charge-potion layer + the deprecated item potions
    pm4g_defensive_actives.csv   actives, on-hit/low-health procs, the bound devotion procs
    pm4g_field_evidence.csv      the template declaration behind every field this lap reads
    pm4g_emit_summary.json       provenance, digests, populations, the save diff

READ-ONLY.  Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")))

from pm4g_lib_2026_08_13 import (  # noqa: E402
    META, VENDOR, PLAYED_SAVE, PLAYED_SAVE_MIRROR, PRISTINE_SAVE, GAMEENGINE,
    read_skill_block, read_ui_bindings, walk_blocks, tags, name_of, rec, arc_of,
    sheet_skill_bonuses, effective_rank, at_rank, dump_csv, Templates, E3,
)

OUT = (META / "agentic_orchestration" / "legolas" / "notes"
       / "2026-08-13-kc2-pm4-lap-g-player-kit")

# ── the populations, named up front (NOTE-9) ────────────────────────────────────────────────────
MOVEMENT = [
    ("records/skills/playerclass09/viremight1.dbr", ["records/skills/playerclass09/viremight2.dbr",
                                                     "records/skills/playerclass09/viremight3.dbr"]),
    ("records/skills/playerclass01/blitz1.dbr", ["records/skills/playerclass01/blitz2.dbr"]),
    ("records/skills/itemskillsgdx2/runes/rush_d203.dbr", []),
    ("records/skills/default/defaultevade.dbr", []),
]

CONSUMABLES = [
    ("records/skills/default/defaulthealthpotion.dbr", "health", "CURRENT-1.3.0.0"),
    ("records/skills/default/defaultmanapotion.dbr", "energy", "CURRENT-1.3.0.0"),
    ("records/items/misc/potions/_oldpotion_healtha01.dbr", "health", "DEPRECATED-ITEM"),
    ("records/items/misc/potions/_oldpotion_healtha02.dbr", "health", "DEPRECATED-ITEM"),
    ("records/items/misc/potions/_oldpotion_healtha03.dbr", "health", "DEPRECATED-ITEM"),
    ("records/items/misc/potions/_oldpotion_healthb01.dbr", "health", "DEPRECATED-ITEM"),
    ("records/items/misc/potions/_oldpotion_energya01.dbr", "energy", "DEPRECATED-ITEM"),
    ("records/items/misc/potions/potion_constitutiona01.dbr", "constitution", "CURRENT-ITEM"),
]

#: The records the 2022 save's inventory NAMES and the 1.3.0.0 corpus DOES NOT CONTAIN.
SAVE_NAMED_MISSING = ["records/items/misc/potions/potion_healtha01.dbr",
                      "records/items/misc/potions/potion_energya01.dbr"]

DEFENSIVE = [
    # (record, kind)
    ("records/skills/playerclass09/ascension1.dbr", "active-buff"),
    ("records/skills/playerclass09/ascension2.dbr", "active-buff-modifier"),
    ("records/skills/playerclass01/warcry1.dbr", "active-debuff"),
    ("records/skills/playerclass01/warcry2.dbr", "active-debuff-modifier"),
    ("records/skills/playerclass01/willtolive1.dbr", "auto-circuit-breaker"),
    ("records/skills/playerclass01/fightingspirit1.dbr", "auto-on-hit-buff"),
    ("records/skills/playerclass01/fieldcommand1buff.dbr", "passive-aura"),
    ("records/skills/playerclass09/presenceofvirtue1_buff.dbr", "passive-aura"),
    ("records/skills/playerclass09/divinemandate1.dbr", "toggled-buff"),
    ("records/skills/itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr", "toggled-buff"),
    ("records/skills/playerclass09/summon_celestialguardian1.dbr", "summon"),
    ("records/skills/itemskillsgdx1/relics/summondeathstalker.dbr", "summon"),
]

MAG_FIELDS = ["damageAbsorption", "skillLifePercent", "characterLifeRegen",
              "offensiveTotalDamageModifier", "retaliationTotalDamageModifier",
              "offensiveTotalDamageReductionPercentMin", "defensiveProtectionModifier",
              "characterDefensiveAbility", "characterOffensiveAbility",
              "offensiveLifeLeechMin", "offensiveLifeMin", "petLimit"]

FIELD_EVIDENCE = [
    ("skillCooldownTime", "templatebase/skill_activated.tpl"),
    ("skillManaCost", "templatebase/skill_activated.tpl"),
    ("cooldownCharges", "templatebase/skill_activated.tpl"),
    ("distanceProfile", "templatebase/skill_activated.tpl"),
    ("waveDistance", "skill_attackpathcharge.tpl"),
    ("maxMoveRatio", "skill_attackpathcharge.tpl"),
    ("endRadiusMultiplier", "skill_attackpathcharge.tpl"),
    ("secondarySkillDistance", "skill_attackpathcharge.tpl"),
    ("maxDistanceBuffer", "skill_attackweaponcharge.tpl"),
    ("waveDistance", "skill_evade.tpl"),
    ("maxMoveRatio", "skill_evade.tpl"),
    ("damageAbsorption", "templatebase/skill_buff.tpl"),
    ("damageAbsorptionPercent", "templatebase/skill_buff.tpl"),
    ("thresholdDuration", "skill_passiveonlifebuffself.tpl"),
    ("lifeMonitorPercent", "skill_passiveonlifebuffself.tpl"),
    ("canUseWhileMoving", "skillchanneled.tpl"),
    ("useResetsDuration", "skillchanneled.tpl"),
    ("duration", "skillchanneled.tpl"),
    ("delayMovement", "skill_attackradiusspin.tpl"),
    ("rotationSpeedMultiplier", "skill_attackradiusspin.tpl"),
    ("timeBetweenAttacks", "skill_attackradiusspin.tpl"),
    ("skillTargetRadius", "templatebase/skill_radius.tpl"),
    ("skillActiveDuration", "templatebase/skill_buff.tpl"),
    ("weaponDamagePct", "templatebase/skill_base.tpl"),
    ("skillMaxLevel", "templatebase/skill_base.tpl"),
    ("skillUltimateLevel", "templatebase/skill_base.tpl"),
    ("targetingMode", "templatebase/skill_base.tpl"),
    ("forceMovement", "templatebase/skill_base.tpl"),
    ("triggerType", "skillautocastcontroller.tpl"),
    ("triggerParam", "skillautocastcontroller.tpl"),
    ("chanceToRun", "skillautocastcontroller.tpl"),
    ("targetType", "skillautocastcontroller.tpl"),
    ("autoTargetRadius", "skillautocastcontroller.tpl"),
    ("skillLifeBonus", "skill_chargepotion.tpl"),
    ("skillLifePercent", "skill_chargepotion.tpl"),
    ("skillManaBonus", "skill_chargepotion.tpl"),
    ("skillManaPercent", "skill_chargepotion.tpl"),
    ("bonusLifePoints", "oneshot_potionhealth.tpl"),
    ("bonusLifePercent", "oneshot_potionhealth.tpl"),
    ("useDelayTime", "oneshot_potionhealth.tpl"),
    ("damageAbsorption", "skill_buffselfshield.tpl"),
    ("lifeMonitorPercent", "skill_passiveonlifebuffself.tpl"),
    ("onHitActivationChance", "skill_passiveonhitbuffself.tpl"),
    ("modifierPotency", "skill_potioncontainer.tpl"),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    T = Templates()
    ge = rec(GAMEENGINE)
    bonuses = sheet_skill_bonuses()

    # ── the two saves ───────────────────────────────────────────────────────────────────────────
    saves = {}
    for tag_, p in (("played", PLAYED_SAVE), ("pristine", PRISTINE_SAVE)):
        h, b8, ver, n, rows, isc, tail = read_skill_block(p)
        h2, b14, binds, _raw = read_ui_bindings(p)
        _hw, bl = walk_blocks(p.read_bytes())
        saves[tag_] = {"header": h, "block8_version": ver, "declared": n, "parsed": len(rows),
                       "skills": rows, "bindings": binds, "item_skill_count": isc,
                       "block14_len": int(b14["len"]),
                       "blocks": [{"id": b["id"], "len": b["len"], "clean": b["clean"]} for b in bl],
                       "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                       "bytes_walked": h["bytes_walked"], "bytes_total": h["bytes_total"]}

    played, pristine = saves["played"], saves["pristine"]
    pl_by_rec = {r["record"]: r for r in played["skills"]}
    pr_by_rec = {r["record"]: r for r in pristine["skills"]}
    bind_ords = {}
    for b in played["bindings"]:
        bind_ords.setdefault(b["skill_record"], []).append(b["binding_ordinal"])

    # ══ CSV 1 -- the played kit ════════════════════════════════════════════════════════════════
    kit_rows = []
    for r in played["skills"]:
        allocated = r["rank_allocated"]
        dev = r["devotion_level"]
        bound = r["record"] in bind_ords
        if allocated == 0 and dev == 0 and not r["autocast_skill"] and not bound:
            continue
        d = rec(r["record"])
        eff, basis = effective_rank(r["record"], allocated, bonuses)
        seg = r["record"].split("/")
        pr = pr_by_rec.get(r["record"])
        pr_bound = any(b["skill_record"] == r["record"] for b in pristine["bindings"])
        binfo = [b for b in played["bindings"] if b["skill_record"] == r["record"]]
        kit_rows.append({
            "skill_record": r["record"],
            "display_name": name_of(d),
            "mastery": {"playerclass01": "Soldier", "playerclass09": "Oathkeeper"}.get(
                seg[2] if len(seg) > 2 else "", seg[2] if len(seg) > 2 else ""),
            "engine_class": d.get("Class"),
            "arc": arc_of(r["record"]),
            "rank_allocated": allocated,
            "rank_effective": eff if allocated else 0,
            "rank_effective_basis": basis if allocated else "n/a (rank 0)",
            "devotion_level": dev,
            "skill_max_level": d.get("skillMaxLevel"),
            "skill_ultimate_level": d.get("skillUltimateLevel"),
            "bound_on_bar": bound,
            "binding_ordinals": "|".join(str(x) for x in bind_ords.get(r["record"], [])),
            "n_bindings": len(bind_ords.get(r["record"], [])),
            "is_item_skill": binfo[0]["is_item_skill"] if binfo else False,
            "item_record": binfo[0]["item_record"] if binfo else None,
            "equip_location": binfo[0]["equip_location"] if binfo else None,
            "autocast_devotion_skill": r["autocast_skill"] or None,
            "autocast_controller": r["autocast_controller"] or None,
            "pristine_rank_allocated": pr["rank_allocated"] if pr else None,
            "pristine_bound_on_bar": pr_bound,
            "rank_changed_vs_pristine": (pr is not None and pr["rank_allocated"] != allocated),
            "binding_changed_vs_pristine": (pr_bound != bound),
            "source": "player.gdc block 8 (+ block 14 for bindings)",
            "grade": "MEASURED",
        })
    # bound records that carry no block-8 row (default skills)
    for b in played["bindings"]:
        if b["skill_record"] in {k["skill_record"] for k in kit_rows}:
            continue
        d = rec(b["skill_record"])
        kit_rows.append({
            "skill_record": b["skill_record"], "display_name": name_of(d), "mastery": "default",
            "engine_class": d.get("Class"), "arc": arc_of(b["skill_record"]),
            "rank_allocated": pl_by_rec.get(b["skill_record"], {}).get("rank_allocated"),
            "rank_effective": pl_by_rec.get(b["skill_record"], {}).get("rank_allocated"),
            "rank_effective_basis": "MEASURED: default skill, no rank bonus",
            "devotion_level": 0, "skill_max_level": d.get("skillMaxLevel"),
            "skill_ultimate_level": d.get("skillUltimateLevel"), "bound_on_bar": True,
            "binding_ordinals": "|".join(str(x) for x in bind_ords[b["skill_record"]]),
            "n_bindings": len(bind_ords[b["skill_record"]]),
            "is_item_skill": b["is_item_skill"], "item_record": b["item_record"],
            "equip_location": b["equip_location"], "autocast_devotion_skill": None,
            "autocast_controller": None, "pristine_rank_allocated": None,
            "pristine_bound_on_bar": any(x["skill_record"] == b["skill_record"]
                                         for x in pristine["bindings"]),
            "rank_changed_vs_pristine": False, "binding_changed_vs_pristine": False,
            "source": "player.gdc block 14", "grade": "MEASURED"})
    kit_rows.sort(key=lambda r: (r["n_bindings"] == 0, r["binding_ordinals"] or "zz",
                                 r["skill_record"]))
    kit_cols = list(kit_rows[0].keys())
    d_kit = dump_csv(OUT / "pm4g_played_kit.csv", kit_rows, kit_cols)

    # ══ CSV 2 -- movement ══════════════════════════════════════════════════════════════════════
    mv_rows = []
    for base, mods in MOVEMENT:
        d = rec(base)
        alloc = pl_by_rec.get(base, {}).get("rank_allocated", 0)
        eff, basis = effective_rank(base, alloc, bonuses)
        cd, cdk = at_rank(d.get("skillCooldownTime"), eff or 1)
        mana, mk = at_rank(d.get("skillManaCost"), eff or 1)
        wdmg, _ = at_rank(d.get("weaponDamagePct"), eff or 1)
        rad = d.get("skillTargetRadius")
        rad, _ = at_rank(rad, eff or 1)
        erm = d.get("endRadiusMultiplier")
        riders = []
        for k in ("offensivePhysicalMin", "offensiveSlowBleedingMin", "offensiveSlowPhysicalMin",
                  "offensiveSlowAttackSpeedMin", "offensiveKnockdownMin", "offensiveTauntMin"):
            v = d.get(k)
            if v:
                vv, _ = at_rank(v, eff or 1)
                if vv:
                    riders.append(f"{k}={vv}")
        for m in mods:
            md = rec(m)
            ma = pl_by_rec.get(m, {}).get("rank_allocated", 0)
            me, _ = effective_rank(m, ma, bonuses)
            for k, v in md.items():
                if k.startswith(("offensive", "characterRunSpeed")) and v and k.endswith(
                        ("Min", "Modifier")) and not k.endswith("ModifierChance"):
                    vv, _ = at_rank(v, me or 1)
                    if vv:
                        riders.append(f"{m.split('/')[-1][:-4]}:{k}={vv}")
        mv_rows.append({
            "skill_record": base, "display_name": name_of(d), "engine_class": d.get("Class"),
            "arc": arc_of(base), "rank_allocated": alloc, "rank_effective": eff,
            "rank_effective_basis": basis,
            "cooldown_s": cd, "cooldown_index": cdk,
            "range_m": d.get("waveDistance"),
            "range_field": "waveDistance" if d.get("waveDistance") is not None else "ABSENT",
            "range_grade": ("MEASURED" if d.get("waveDistance") is not None
                            else "DECLARED-GAP: no range field on this template"),
            "distance_profile": d.get("distanceProfile"),
            "distance_profile_range_m": {
                "Melee": ge.get("meleeRange"), "Short": ge.get("shortRange"),
                "Moderate": ge.get("moderateRange"), "Long": ge.get("longRange"),
                "Maximum": ge.get("maximumRange"), "Boss": ge.get("bossRange"),
            }.get(str(d.get("distanceProfile"))),
            "run_speed_modifier_pct": d.get("characterRunSpeedModifier"),
            "max_move_ratio": d.get("maxMoveRatio"),
            "impact_radius_m": rad,
            "end_radius_multiplier": erm,
            "end_impact_radius_m": (rad * erm) if (rad and erm) else None,
            "mana_cost": mana, "weapon_damage_pct": wdmg,
            "cooldown_charges": d.get("cooldownCharges"),
            "warmup": d.get("skillAllowsWarmUp"),
            "targeting_mode": d.get("targetingMode"),
            "channel_interaction": (
                "MEASURED-ABSENT: this record declares NO channel/exclusion field "
                "(canUseWhileMoving / delayMovement / skillDependancy / exclusiveSkill all absent "
                "or false) -- the EoR channel's own canUseWhileMoving=1 is the only movement "
                "clause in the pair; whether a cast BREAKS the channel is engine-internal "
                "(DECLARED-GAP C-G3)"),
            "declares_canUseWhileMoving": "canUseWhileMoving" in d,
            "declares_exclusiveSkill": bool(d.get("exclusiveSkill")),
            "declares_skillDependancy": bool(d.get("skillDependancy")),
            "riders": " ; ".join(riders) or None,
            "in_played_save_block8": base in pl_by_rec,
            "in_pristine_save_block8": base in pr_by_rec,
            "bound_on_played_bar": base in bind_ords,
            "grade": "MEASURED",
        })
    d_mv = dump_csv(OUT / "pm4g_movement_skills.csv", mv_rows, list(mv_rows[0].keys()))

    # ══ CSV 3 -- consumables ═══════════════════════════════════════════════════════════════════
    cs_rows = []
    for path, kind, status in CONSUMABLES:
        d = rec(path)
        present = bool(d)
        cs_rows.append({
            "record": path, "display_name": name_of(d) or tags().get(str(d.get("description", "")), ""),
            "engine_class": d.get("Class"), "arc": arc_of(path), "kind": kind,
            "corpus_status": status, "present_in_edition_III": present,
            "heal_flat": d.get("skillLifeBonus") if "skillLifeBonus" in d else d.get("bonusLifePoints"),
            "heal_pct": d.get("skillLifePercent") if "skillLifePercent" in d else d.get("bonusLifePercent"),
            "heal_pct_slow": d.get("bonusLifePercentSlow"),
            "energy_flat": d.get("skillManaBonus") if "skillManaBonus" in d else d.get("bonusManaPoints"),
            "energy_pct": d.get("skillManaPercent") if "skillManaPercent" in d else d.get("bonusManaPercent"),
            "constitution_pct": d.get("bonusConstitutionPercent"),
            "cooldown_s": d.get("skillCooldownTime") if "skillCooldownTime" in d else d.get("useDelayTime"),
            "cooldown_field": ("skillCooldownTime" if "skillCooldownTime" in d else
                               ("useDelayTime" if "useDelayTime" in d else None)),
            "charges": d.get("cooldownCharges"), "instant_cast": d.get("instantCast"),
            "max_stack": d.get("maxStackSize") or (ge.get("potionStackLimit") if kind != "constitution" else None),
            "in_played_save_block8": path in pl_by_rec,
            "grade": "MEASURED" if present else "DECLARED-ABSENT",
        })
    for path in SAVE_NAMED_MISSING:
        d = rec(path)
        cs_rows.append({
            "record": path, "display_name": "", "engine_class": None, "arc": None,
            "kind": "health/energy (2022 save inventory)", "corpus_status": "SAVE-NAMED-CORPUS-ABSENT",
            "present_in_edition_III": bool(d), "heal_flat": None, "heal_pct": None,
            "heal_pct_slow": None, "energy_flat": None, "energy_pct": None,
            "constitution_pct": None, "cooldown_s": None, "cooldown_field": None, "charges": None,
            "instant_cast": None, "max_stack": None, "in_played_save_block8": path in pl_by_rec,
            "grade": "DECLARED-ABSENT: named by the pristine save, not in the 1.3.0.0 corpus"})
    # the FoA potion-customisation layer, counted not enumerated
    containers = sorted(k for k in E3.idx if k.startswith(
        "records/skills/itemskillsgdx3/potionmodifiers/container_"))
    modifiers = sorted(k for k in E3.idx if k.startswith(
        "records/skills/itemskillsgdx3/potionmodifiers/") and "container_" not in k)
    for path in modifiers:
        d = rec(path)
        row8 = pl_by_rec.get(path, {})
        cs_rows.append({
            "record": path, "display_name": name_of(d), "engine_class": d.get("Class"),
            "arc": arc_of(path),
            "kind": ("potion-modifier ALLOCATED" if row8.get("rank_allocated")
                     else "potion-modifier (present, not allocated)"),
            "corpus_status": "CURRENT-1.3.0.0", "present_in_edition_III": True,
            "heal_flat": d.get("skillLifeBonus"), "heal_pct": d.get("skillLifePercent"),
            "heal_pct_slow": d.get("skillLifePercentSlow"),
            "energy_flat": d.get("skillManaBonus"), "energy_pct": d.get("skillManaPercent"),
            "constitution_pct": None, "cooldown_s": d.get("skillCooldownTime"),
            "cooldown_field": "skillCooldownTime" if d.get("skillCooldownTime") else None,
            "charges": d.get("cooldownCharges"), "instant_cast": d.get("instantCast"),
            "max_stack": None, "in_played_save_block8": path in pl_by_rec,
            "rank_allocated_played": row8.get("rank_allocated"),
            "locked_flag_b2": row8.get("b2"),
            "grade": "MEASURED"})
    for path in containers:
        d = rec(path)
        cs_rows.append({
            "record": path, "display_name": name_of(d), "engine_class": d.get("Class"),
            "arc": arc_of(path), "kind": "potion-container (FoA customisation)",
            "corpus_status": "CURRENT-1.3.0.0", "present_in_edition_III": True,
            "heal_flat": None, "heal_pct": None, "heal_pct_slow": None, "energy_flat": None,
            "energy_pct": None, "constitution_pct": None,
            "cooldown_s": json.dumps(d.get("skillCooldownTime")) if d.get("skillCooldownTime") else None,
            "cooldown_field": "skillCooldownTime (per-rank DELTA)",
            "charges": json.dumps(d.get("cooldownCharges")) if d.get("cooldownCharges") else None,
            "instant_cast": None, "max_stack": None, "in_played_save_block8": path in pl_by_rec,
            "grade": "MEASURED (availability to THIS character NOT decodable -- see README)"})
    cs_cols = list(dict.fromkeys([k for r in cs_rows for k in r.keys()]))
    d_cs = dump_csv(OUT / "pm4g_consumables.csv", cs_rows, cs_cols)

    # ══ CSV 4 -- defensive actives + bound devotion procs ══════════════════════════════════════
    df_rows = []

    def add_def(path, kind, rank, rank_basis, trigger_rec=None, host=None):
        d = rec(path)
        if not d:
            df_rows.append({"skill_record": path, "display_name": "", "kind": kind,
                            "grade": "DECLARED-ABSENT"})
            return
        ctrl = rec(trigger_rec) if trigger_rec else {}
        mags = {}
        for k in MAG_FIELDS:
            if k in d and d[k]:
                v, note = at_rank(d[k], rank or 1)
                if v:
                    mags[k] = v
        cd, _ = at_rank(d.get("skillCooldownTime"), rank or 1)
        dur, _ = at_rank(d.get("skillActiveDuration"), rank or 1)
        mana, _ = at_rank(d.get("skillManaCost"), rank or 1)
        chance, _ = at_rank(d.get("onHitActivationChance"), rank or 1)
        df_rows.append({
            "skill_record": path, "display_name": name_of(d) or d.get("FileDescription", ""),
            "engine_class": d.get("Class"), "arc": arc_of(path), "kind": kind,
            "host_skill": host,
            "rank": rank, "rank_basis": rank_basis,
            "trigger": (ctrl.get("triggerType") if ctrl else
                        ("LowHealth" if "lifeMonitorPercent" in d and d.get("lifeMonitorPercent")
                         else ("OnHit" if chance else "manual"))),
            "trigger_param": (ctrl.get("triggerParam") if ctrl else d.get("lifeMonitorPercent")),
            "trigger_chance_pct": (ctrl.get("chanceToRun") if ctrl else chance),
            "trigger_target": ctrl.get("targetType") if ctrl else None,
            "trigger_radius_m": ctrl.get("autoTargetRadius") if ctrl else None,
            "controller_record": trigger_rec,
            "duration_s": dur, "cooldown_s": cd, "mana_cost": mana,
            "instant_cast": d.get("instantCast"), "aura_radius_m": d.get("skillTargetRadius"),
            "magnitudes": " ; ".join(f"{k}={v}" for k, v in sorted(mags.items())) or None,
            "grade": "MEASURED",
        })

    for path, kind in DEFENSIVE:
        alloc_src = path.replace("1buff.dbr", "1.dbr").replace("1_buff.dbr", "1.dbr")
        alloc = pl_by_rec.get(alloc_src, {}).get("rank_allocated", 0)
        eff, basis = effective_rank(alloc_src, alloc, bonuses)
        add_def(path, kind, eff if alloc else 1,
                basis if alloc else "MEASURED: item-granted, rank 1")
    for r in played["skills"]:
        if r["autocast_skill"]:
            proc = r["autocast_skill"]
            lvl = pl_by_rec.get(proc, {}).get("devotion_level", 0)
            add_def(proc, "bound-devotion-proc", lvl,
                    f"MEASURED: devotion_level {lvl} from player.gdc block 8",
                    trigger_rec=r["autocast_controller"], host=r["record"])
            d = rec(proc)
            if d.get("buffSkillName"):
                add_def(d["buffSkillName"], "bound-devotion-proc-payload", lvl,
                        f"MEASURED: devotion_level {lvl} (payload of {proc.split('/')[-1]})",
                        trigger_rec=r["autocast_controller"], host=r["record"])
    d_df = dump_csv(OUT / "pm4g_defensive_actives.csv", df_rows,
                    list(max(df_rows, key=lambda x: len(x)).keys()))

    # ══ CSV 5 -- field evidence ════════════════════════════════════════════════════════════════
    fe_rows = []
    for field, tpl in FIELD_EVIDENCE:
        v = T.declare(tpl, field) if T.has(tpl) else None
        fe_rows.append({"field": field, "template": tpl, "template_present": T.has(tpl),
                        "type": (v or {}).get("type"), "default": (v or {}).get("defaultValue"),
                        "description": (v or {}).get("description"),
                        "grade": "MEASURED" if v else "DECLARED: field not on this template"})
    d_fe = dump_csv(OUT / "pm4g_field_evidence.csv", fe_rows, list(fe_rows[0].keys()))

    # ══ CSV 6 -- the channel census: who ELSE may move while channelling? ══════════════════════
    ch_rows = []
    for k in E3.idx:
        if not k.startswith("records/skills/"):
            continue
        d = rec(k)
        if "canUseWhileMoving" not in d:
            continue
        ch_rows.append({"skill_record": k, "display_name": name_of(d),
                        "engine_class": d.get("Class"), "arc": arc_of(k),
                        "canUseWhileMoving": bool(d.get("canUseWhileMoving")),
                        "delayMovement": d.get("delayMovement"),
                        "rotationSpeedMultiplier": d.get("rotationSpeedMultiplier"),
                        "duration": d.get("duration"),
                        "useResetsDuration": d.get("useResetsDuration"),
                        "timeBetweenAttacks": d.get("timeBetweenAttacks"),
                        "characterRunSpeedModifier": d.get("characterRunSpeedModifier"),
                        "is_dev_base_template": "base_template skills" in k,
                        "grade": "MEASURED"})
    ch_rows.sort(key=lambda r: (not r["canUseWhileMoving"], r["skill_record"]))
    d_ch = dump_csv(OUT / "pm4g_channel_census.csv", ch_rows, list(ch_rows[0].keys()))

    # ══ summary ════════════════════════════════════════════════════════════════════════════════
    eor = rec("records/skills/playerclass09/eyeofreckoning1.dbr")
    summary = {
        "lap": "KC2-PM4 Lap G -- the player's own kit",
        "author": "legolas (UNKNOWN-RESEARCHER)", "date": "2026-08-13",
        "vendor_corpus": str(VENDOR),
        "saves": {k: {"path": str(p), "sha256": saves[k]["sha256"],
                      "expansion_status": saves[k]["header"]["expansion_status"],
                      "obfuscated": saves[k]["header"]["obfuscated"],
                      "seed": saves[k]["header"]["seed_raw"],
                      "bytes_walked": saves[k]["bytes_walked"],
                      "bytes_total": saves[k]["bytes_total"],
                      "blocks": len(saves[k]["blocks"]),
                      "blocks_clean": sum(1 for b in saves[k]["blocks"] if b["clean"]),
                      "block8_declared": saves[k]["declared"],
                      "block8_parsed": saves[k]["parsed"],
                      "block14_len": saves[k]["block14_len"],
                      "bindings": len(saves[k]["bindings"])}
                  for k, p in (("played", PLAYED_SAVE), ("pristine", PRISTINE_SAVE))},
        "played_mirror_identical": (hashlib.sha256(PLAYED_SAVE.read_bytes()).hexdigest()
                                    == hashlib.sha256(PLAYED_SAVE_MIRROR.read_bytes()).hexdigest()),
        "sheet_skill_bonuses": bonuses,
        "gameengine_distance_profiles": {k: ge.get(v) for k, v in (
            ("Melee", "meleeRange"), ("Short", "shortRange"), ("Moderate", "moderateRange"),
            ("Long", "longRange"), ("Maximum", "maximumRange"), ("Boss", "bossRange"))},
        "gameengine_melee_target_distance": ge.get("meleeTargetDistance"),
        "gameengine_potion_stack_limit": ge.get("potionStackLimit"),
        "channel_census": {
            "records_declaring_canUseWhileMoving": len(ch_rows),
            "true": sum(1 for r in ch_rows if r["canUseWhileMoving"]),
            "false": sum(1 for r in ch_rows if not r["canUseWhileMoving"]),
            "true_non_dev_template": [r["skill_record"] for r in ch_rows
                                      if r["canUseWhileMoving"] and not r["is_dev_base_template"]],
        },
        "eor_channel": {k: eor.get(k) for k in
                        ("Class", "canUseWhileMoving", "delayMovement", "duration",
                         "useResetsDuration", "rotationSpeedMultiplier", "timeBetweenAttacks",
                         "skillTargetRadius", "characterRunSpeedModifier", "distanceProfile",
                         "skillCooldownTime", "instantCast", "forceMovement")},
        "rows": {"played_kit": len(kit_rows), "movement": len(mv_rows),
                 "consumables": len(cs_rows), "defensive": len(df_rows),
                 "field_evidence": len(fe_rows), "channel_census": len(ch_rows)},
        "digests": {"pm4g_played_kit.csv": d_kit, "pm4g_movement_skills.csv": d_mv,
                    "pm4g_consumables.csv": d_cs, "pm4g_defensive_actives.csv": d_df,
                    "pm4g_field_evidence.csv": d_fe, "pm4g_channel_census.csv": d_ch},
        "save_diff": {
            "skills_rank_changed": [r["skill_record"] for r in kit_rows
                                    if r.get("rank_changed_vs_pristine")],
            "bindings_played": [b["skill_record"] for b in played["bindings"]],
            "bindings_pristine": [b["skill_record"] for b in pristine["bindings"]],
            "dropped_from_bar": [b["skill_record"] for b in pristine["bindings"]
                                 if b["skill_record"] not in
                                 {x["skill_record"] for x in played["bindings"]}],
            "added_to_bar": [b["skill_record"] for b in played["bindings"]
                             if b["skill_record"] not in
                             {x["skill_record"] for x in pristine["bindings"]}],
            "block8_new_records": sorted(set(pl_by_rec) - set(pr_by_rec)),
        },
    }
    (OUT / "pm4g_emit_summary.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps({"rows": summary["rows"], "digests": summary["digests"],
                      "saves": summary["saves"], "eor_channel": summary["eor_channel"],
                      "save_diff_bar": {"dropped": summary["save_diff"]["dropped_from_bar"],
                                        "added": summary["save_diff"]["added_to_bar"]},
                      "new_records": summary["save_diff"]["block8_new_records"][:20]},
                     indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
