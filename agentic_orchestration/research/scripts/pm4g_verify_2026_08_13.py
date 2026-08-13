#!/usr/bin/env python3
"""KC2-PM4 Lap G verifier -- the FOUR PRE-NAMED HOOKS, plus the reader's own self-checks.

Pre-named in the commission BEFORE the decode ran:
  (a) kit coverage      -- every quickbar slot accounted
  (b) build-guide       -- followed / deviated per slot
  (c) the dash          -- cooldown + range stated with .dbr field evidence
  (d) potion magnitude  -- cross-checked against two independent record paths if they exist

Every hook prints PASS/FAIL with its numbers.  READ-ONLY.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")))

from pm4g_lib_2026_08_13 import (  # noqa: E402
    META, PLAYED_SAVE, PLAYED_SAVE_MIRROR, PRISTINE_SAVE,
    walk_blocks, read_skill_block, read_ui_bindings, rec, Templates, E3,
)

OUT = (META / "agentic_orchestration" / "legolas" / "notes"
       / "2026-08-13-kc2-pm4-lap-g-player-kit")

R = {"checks": [], "pass": 0, "fail": 0}


def check(name, ok, detail):
    R["checks"].append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    R["pass" if ok else "fail"] += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def main() -> int:
    T = Templates()

    # ── R0  the reader proves itself on BOTH saves ─────────────────────────────────────────────
    for tag, p in (("played", PLAYED_SAVE), ("pristine", PRISTINE_SAVE)):
        h, bl = walk_blocks(p.read_bytes())
        check(f"R0.{tag} full-file walk",
              h["bytes_walked"] == h["bytes_total"] and len(bl) == 15,
              f"{h['bytes_walked']}/{h['bytes_total']} bytes, {len(bl)} blocks, "
              f"{sum(1 for b in bl if b['clean'])}/{len(bl)} clean "
              f"(unclean = {[b['id'] for b in bl if not b['clean']]}), seed {h['seed_raw']}")
        ids = {b["id"] for b in bl}
        check(f"R0.{tag} blocks 8+14 self-verified",
              all(b["clean"] for b in bl if b["id"] in (8, 14)) and {8, 14} <= ids,
              "block 8 (skills) and block 14 (UI settings) each reproduced their own zero "
              "end-marker under the blanket key advance -- no nested no-bump ints inside them")

    check("R0.mirror byte-identical",
          hashlib.sha256(PLAYED_SAVE.read_bytes()).hexdigest()
          == hashlib.sha256(PLAYED_SAVE_MIRROR.read_bytes()).hexdigest(),
          "matt-notes-from-pc copy == GD-matt-test/eor-test-2 copy")

    # ── HOOK (a)  KIT COVERAGE ─────────────────────────────────────────────────────────────────
    _h, _b8, _v, n_dec, sk, _isc, _t = read_skill_block(PLAYED_SAVE)
    _h2, b14, binds, _raw = read_ui_bindings(PLAYED_SAVE)
    check("(a) block-8 declared == parsed", n_dec == len(sk), f"{n_dec} declared, {len(sk)} parsed")
    ords = [b["binding_ordinal"] for b in binds]
    check("(a) binding ordinals contiguous from 0",
          ords == list(range(len(binds))), f"{len(binds)} slots, ordinals {ords}")
    missing = [b["skill_record"] for b in binds if not rec(b["skill_record"])]
    check("(a) every bound slot resolves to a corpus record",
          not missing, f"{len(binds)}/{len(binds)} resolve" if not missing else f"missing {missing}")
    item_slots = [b for b in binds if b["is_item_skill"]]
    check("(a) item-skill slots carry item + equip location",
          all(b["item_record"] and b["equip_location"] is not None for b in item_slots),
          "; ".join(f"{b['skill_record'].split('/')[-1]} <- {b['item_record'].split('/')[-1]} "
                    f"@slot {b['equip_location']}" for b in item_slots))
    kit = list(csv.DictReader((OUT / "pm4g_played_kit.csv").open()))
    bound_rows = [r for r in kit if r["bound_on_bar"] == "True"]
    check("(a) CSV bound rows == save bindings (distinct records)",
          len({r["skill_record"] for r in bound_rows}) == len({b["skill_record"] for b in binds}),
          f"{len(bound_rows)} CSV rows / {len(binds)} slots "
          f"({len({b['skill_record'] for b in binds})} distinct records; "
          f"eyeofreckoning1 occupies 2 slots)")
    unresolved = [r["skill_record"] for r in kit if not r["engine_class"]]
    check("(a) every kit row has an engine Class",
          not unresolved, f"{len(kit)} rows, {len(unresolved)} without Class")

    # ── HOOK (b)  BUILD-GUIDE CROSS-CHECK ──────────────────────────────────────────────────────
    # The governing ruling R-V3-2 (playtest directions v3 § 2) is savefile-primary: the forum post
    # states the pristine zip IS the b28gD0KN build-of-record.  grimtools is robots-blocked, so the
    # DECIDABLE cross-check is played-save vs build-of-record-savefile, slot by slot.
    _hp, _b8p, _vp, _np, skp, _iscp, _tp = read_skill_block(PRISTINE_SAVE)
    pr = {r["record"]: r for r in skp}
    pl = {r["record"]: r for r in sk}
    rank_deltas = [(k, pr[k]["rank_allocated"], pl[k]["rank_allocated"])
                   for k in pr if k in pl and pr[k]["rank_allocated"] != pl[k]["rank_allocated"]]
    check("(b) skill allocation UNCHANGED vs the build-of-record savefile",
          not rank_deltas,
          f"{sum(1 for r in skp if r['rank_allocated'] > 0)} allocated skills, "
          f"0 rank deltas" if not rank_deltas else str(rank_deltas))
    dev_deltas = [(k, pr[k]["devotion_level"], pl[k]["devotion_level"])
                  for k in pr if k in pl and pr[k]["devotion_level"] != pl[k]["devotion_level"]]
    check("(b) devotion allocation UNCHANGED",
          not dev_deltas,
          f"{sum(1 for r in skp if r['devotion_level'] > 0)} devotion nodes, 0 deltas"
          if not dev_deltas else str(dev_deltas))
    pr_ac = {k: (v["autocast_skill"], v["autocast_controller"]) for k, v in pr.items()
             if v["autocast_skill"]}
    pl_ac = {k: (v["autocast_skill"], v["autocast_controller"]) for k, v in pl.items()
             if v["autocast_skill"]}
    check("(b) devotion-proc BINDINGS survived the 1.2.1.5 migration intact",
          pr_ac == pl_ac,
          f"{len(pl_ac)}/{len(pr_ac)} proc bindings identical -- the v1.2.1.5 two-hander "
          f"unbind risk named in the playtest directions did NOT materialise (or was re-bound "
          f"exactly): " + ", ".join(sorted(k.split('/')[-1] for k in pl_ac)))
    _h3, _b14p, bindp, _r3 = read_ui_bindings(PRISTINE_SAVE)
    pset, lset = {b["skill_record"] for b in bindp}, {b["skill_record"] for b in binds}
    dropped, added = sorted(pset - lset), sorted(lset - pset)
    check("(b) per-slot bar diff enumerated",
          True,
          f"pristine {len(bindp)} slots -> played {len(binds)} slots; DROPPED "
          f"{[x.split('/')[-1] for x in dropped]}; ADDED {[x.split('/')[-1] for x in added]}; "
          f"eyeofreckoning1 now occupies "
          f"{sum(1 for b in binds if 'eyeofreckoning1' in b['skill_record'])} slots "
          f"(was {sum(1 for b in bindp if 'eyeofreckoning1' in b['skill_record'])})")
    dropped_kinds = {x: rec(x).get("Class") for x in dropped}
    check("(b) every DROPPED slot is a passive/toggled aura, not an active",
          all(str(c).startswith(("Skill_BuffRadiusToggled", "Skill_BuffSelfToggled"))
              for c in dropped_kinds.values()),
          "; ".join(f"{k.split('/')[-1]}={v}" for k, v in dropped_kinds.items()))

    # ── HOOK (c)  THE DASH: cooldown + range, with field evidence ──────────────────────────────
    for path, exp_cd, exp_range in (
            ("records/skills/playerclass09/viremight1.dbr", 3.5999999046325684, 12.0),
            ("records/skills/itemskillsgdx2/runes/rush_d203.dbr", 2.5, 16.0),
            ("records/skills/default/defaultevade.dbr", 3.0, 10.0)):
        d = rec(path)
        tpl = str(d.get("templateName", "")).split("/")[-1]
        cd_decl = T.declare("templatebase/skill_activated.tpl", "skillCooldownTime")
        rg_decl = T.declare(tpl, "waveDistance")
        ok = (d.get("skillCooldownTime") == exp_cd and d.get("waveDistance") == exp_range
              and cd_decl and rg_decl)
        check(f"(c) {path.split('/')[-1]} cooldown+range with template evidence", bool(ok),
              f"skillCooldownTime={d.get('skillCooldownTime')} s "
              f"[{cd_decl and cd_decl.get('type')}, desc={cd_decl and cd_decl.get('description')!r}, "
              f"templatebase/skill_activated.tpl] · "
              f"waveDistance={d.get('waveDistance')} m "
              f"[{rg_decl and rg_decl.get('type')}, desc={rg_decl and rg_decl.get('description')!r}, "
              f"{tpl}] · unit = metre by the Lap-F display-contract ruling")
    blitz = rec("records/skills/playerclass01/blitz1.dbr")
    check("(c) Blitz range is DECLARED-GAP, and the gap is named",
          "waveDistance" not in blitz
          and not T.declare("skill_attackweaponcharge.tpl", "waveDistance"),
          "Skill_AttackWeaponCharge declares NO range field (only maxDistanceBuffer, whose "
          "description is about MONSTERS); blitz1.dbr carries distanceProfile='Melee' and the "
          "six distanceProfile names match six gameengine.dbr range scalars 6/6 by name, but the "
          "engine's use of that join is not decodable from the corpus -- DECLARED, not estimated")

    # ── HOOK (d)  POTION MAGNITUDE ACROSS TWO INDEPENDENT RECORD PATHS ─────────────────────────
    skill = rec("records/skills/default/defaulthealthpotion.dbr")
    item = rec("records/items/misc/potions/_oldpotion_healtha01.dbr")
    trio = [(skill.get("skillLifeBonus"), item.get("bonusLifePoints"), "flat"),
            (skill.get("skillLifePercent"), item.get("bonusLifePercent"), "percent"),
            (skill.get("skillCooldownTime"), item.get("useDelayTime"), "cooldown_s")]
    ok = all(a == b for a, b, _ in trio)
    check("(d) HEALTH potion agrees across two independent authoring surfaces", ok,
          " · ".join(f"{k}: skill {a} vs item {b} {'EXACT' if a == b else 'DIFFER'}"
                     for a, b, k in trio)
          + "  [skill = gdx3 Skill_ChargePotion; item = base OneShot_PotionHealth, deprecated]")
    eskill = rec("records/skills/default/defaultmanapotion.dbr")
    eitem = rec("records/items/misc/potions/_oldpotion_energya01.dbr")
    etrio = [(eskill.get("skillManaBonus"), eitem.get("bonusManaPoints"), "flat"),
             (eskill.get("skillManaPercent"), eitem.get("bonusManaPercent"), "percent"),
             (eskill.get("skillCooldownTime"), eitem.get("useDelayTime"), "cooldown_s")]
    check("(d) ENERGY potion DIFFERS across the two surfaces -- reported, not averaged",
          not all(a == b for a, b, _ in etrio),
          " · ".join(f"{k}: skill {a} vs item {b}" for a, b, k in etrio)
          + "  -> the energy potion was REBALANCED between the two eras; the health potion was not")
    absent = [p for p in ("records/items/misc/potions/potion_healtha01.dbr",
                          "records/items/misc/potions/potion_energya01.dbr")
              if p not in E3.idx]
    check("(d) the 2022 save's own potion records are ABSENT from the 1.3.0.0 corpus",
          len(absent) == 2,
          f"{absent} named by the pristine save's inventory, not present in any of the 8 archives; "
          f"the only OneShot_PotionHealth records in the whole corpus are the 4 `_oldpotion_*`")

    # ── (d+) THE THIRD CORROBORATION: base charge-potion + the ONE allocated modifier reproduces
    #        the deprecated item potion EXACTLY, term for term ────────────────────────────────
    hot = rec("records/skills/itemskillsgdx3/potionmodifiers/healthpotion_healovertime.dbr")
    check("(d+) 1.3.0.0 potion + heal-over-time modifier == the 2022 item potion, term for term",
          (skill.get("skillLifeBonus") == item.get("bonusLifePoints")
           and skill.get("skillLifePercent") == item.get("bonusLifePercent")
           and hot.get("skillLifePercentSlow") == item.get("bonusLifePercentSlow")
           and skill.get("skillCooldownTime") == item.get("useDelayTime")),
          f"flat {skill.get('skillLifeBonus')} · instant {skill.get('skillLifePercent')}% · "
          f"over-time {hot.get('skillLifePercentSlow')}% (from the modifier) · "
          f"cd {skill.get('skillCooldownTime')} s  ==  item 800 / 25% / "
          f"{item.get('bonusLifePercentSlow')}% / {item.get('useDelayTime')} s")

    # ── (a+) THE 1.3 EXTRA SKILL-BLOCK BYTE IS THE POTION-MODIFIER LOCK FLAG ──────────────────
    b2set = {r["record"] for r in sk if r["b2"] == 1}
    mods = {r["record"] for r in sk
            if "potionmodifiers/" in r["record"] and "/container_" not in r["record"]}
    selected = {r["record"] for r in sk if r["record"] in mods and r["rank_allocated"] > 0}
    check("(a+) block-8 byte `b2` == the FoA potion-modifier LOCK flag",
          b2set <= mods and len(b2set) == 38 and len(mods) == 40 and not (b2set - mods),
          f"b2==1 on exactly {len(b2set)} of the {len(mods)} potion-modifier records and on ZERO "
          f"of the other {len(sk) - len(mods)} rows in the 367-row block; the two exceptions are "
          f"the health+energy heal-over-time pair (the default-unlocked modifiers). "
          f"ALLOCATED modifier(s): {[x.split('/')[-1] for x in sorted(selected)]}")

    # ── digests ────────────────────────────────────────────────────────────────────────────────
    summ = json.loads((OUT / "pm4g_emit_summary.json").read_text())
    for fn, want in summ["digests"].items():
        got = hashlib.sha256((OUT / fn).read_bytes()).hexdigest()
        check(f"digest {fn}", got == want, f"{got[:16]}… {'EXACT' if got == want else 'DRIFT'}")

    print(f"\n{R['pass']} PASS / {R['fail']} FAIL")
    (OUT / "pm4g_verify_summary.json").write_text(json.dumps(R, indent=1))
    return 0 if R["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
