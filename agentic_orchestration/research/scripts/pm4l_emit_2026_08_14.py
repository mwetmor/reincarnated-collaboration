#!/usr/bin/env python3
"""KC2-PM4 · Lap L · THE PLAYER-OFFENSE DECODE  (ruling R-PM4-24, charter row L-20).

READ-ONLY on every source.  OUTCOME-FIREWALLED: this instrument reads NO sim output, NO gamora
landing note, NO baton.  Its substrate is (a) the Grim Dawn Edition-III `.arz`/`.arc` corpus,
(b) Matt's PLAYED save `player.gdc`, (c) Lap A's camera-measured character sheet, (d) Lap D's
own per-record/per-wave roster emission.  Nothing is fitted to any observed clear time.

GL-12 decode-never-estimate.  NOTE-9: every emitted quantity carries its own basis.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import math
import pathlib
import sys

ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4g_lib_2026_08_13 import (                                       # noqa: E402
    E3, rec, arc_of, at_rank, read_skill_block, walk_blocks, reader_at,
    PLAYED_SAVE, LAP_A_SHEET, GAMEENGINE, sheet_skill_bonuses,
)
from pm4d_lib_2026_08_13 import is_body, survival_life_modifier_array, G_at   # noqa: E402
from pm4i_lib_2026_08_13 import survival_arrays, surv_at, difficulty_pak      # noqa: E402
from gamora_kc2_c1_closure_ed3_2026_08_08 import resolve, ev                  # noqa: E402

OUT = META / "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-l-player-offense"
LAPD = META / "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp"
LAPI = META / "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense"

EOR = "records/skills/playerclass09/eyeofreckoning1.dbr"
EOR_MOD = "records/skills/playerclass09/eyeofreckoning2.dbr"
WEAPON = "records/items/gearweapons/melee2h/d107_blunt2h.dbr"
WARBORN = "records/items/lootsets/itemset_d025b.dbr"
COMBATF = "records/game/combatformulas.dbr"

log_lines: list[str] = []


def L(msg: str) -> None:
    print(msg)
    log_lines.append(msg)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 0 -- THE EQUIPMENT ARRAY, recovered from the played save's DESYNCED block 3
# ══════════════════════════════════════════════════════════════════════════════════════════════
# Blocks 3 (inventory) and 4 (stash) carry NESTED no-bump length ints, so Lap G's blanket u8 sweep
# reports `clean = False` and Lap G declared them unparsed (cliff C-G6, inherited from Lap A C-4).
# THE CLIFF IS CLOSED HERE, and the method is measured rather than guessed: because both the true
# reader and the blanket sweep advance the key by the SAME rule (`key ^= t[raw]` per raw byte), a
# missed no-bump int introduces a key error D that is CONSTANT for the rest of the regime; and a
# u8 read consumes only `key & 0xFF`, so every byte of a desynced regime is the TRUE byte XORed
# with ONE constant mask m = D & 0xFF.  Recovering the strings is then a 256-way search, and a
# candidate is accepted only if the whole path decodes to the legal record charset.  The masks
# partition block 3 into exactly 7 regimes = the nested sub-blocks, and the LAST regime is the
# equipment array, whose weapon slot reproduces Lap A's independently camera-read component
# (Seal of Might) and augment (Potent Oleron's Fervor) EXACTLY.

LEGAL = set(b"abcdefghijklmnopqrstuvwxyz0123456789_/.-%")


def recover_block_items(path: pathlib.Path, block_id: int):
    buf = path.read_bytes()
    _h, bl = walk_blocks(buf)
    b = [x for x in bl if x["id"] == block_id][0]
    g = reader_at(buf, b)
    end = int(b["payload"]) + int(b["len"])
    dec = bytearray()
    while g.p < end:
        dec.append(g.u8())
    dec = bytes(dec)
    hits = []
    for m in range(256):
        pat = bytes(c ^ m for c in b"records/items/")
        i = 0
        while True:
            i = dec.find(pat, i)
            if i < 0:
                break
            j, s = i, bytearray()
            while j < len(dec):
                c = dec[j] ^ m
                if c not in LEGAL:
                    break
                s.append(c)
                j += 1
            t = bytes(s)
            while t and not t.endswith(b".dbr"):
                t = t[:-1]
            if t.endswith(b".dbr"):
                hits.append((i, m, t.decode()))
            i += 1
    hits.sort()
    return b, hits


#: The equipment array as recovered above (slot label assigned from the item record's OWN gear
#: directory -- never from a positional guess).
EQUIP = [
    ("head",      "records/items/upgraded/gearhead/d028_head.dbr",
     ["records/items/lootaffixes/crafting/ad201_slowresist.dbr"],
     "records/items/materia/compb_arcanediamond.dbr",
     "records/items/enchants/c203a_enchant.dbr"),
    ("neck",      "records/items/gearaccessories/necklaces/b201e_necklace.dbr",
     ["records/items/lootaffixes/prefix/b_ar024_ar_f.dbr",
      "records/items/lootaffixes/suffix/a014b_ch_speedattack_03_je.dbr"],
     "records/items/materia/compb_sealannihilation.dbr",
     "records/items/enchants/b130a_enchant.dbr"),
    ("chest",     "records/items/upgraded/geartorso/d026_torso.dbr", [],
     "records/items/materia/compb_chainsofoleron.dbr",
     "records/items/enchants/c104a_enchant.dbr"),
    ("legs",      "records/items/gearlegs/b002e_legs.dbr",
     ["records/items/lootaffixes/prefix/b_ar007_ar_f.dbr",
      "records/items/lootaffixes/suffix/a007b_ch_att_all_10.dbr"],
     "records/items/materia/compb_ancientarmorplate.dbr",
     "records/items/enchants/c06a_enchant.dbr"),
    ("feet",      "records/items/upgraded/gearfeet/d007_feet.dbr",
     ["records/items/lootaffixes/crafting/ad201_slowresist.dbr"],
     "records/items/materia/compa_spellscorchedplating.dbr",
     "records/items/enchants/c14a_enchant.dbr"),
    ("hands",     "records/items/gearhands/d206_hands.dbr", [],
     "records/items/materia/compa_restlessremains.dbr",
     "records/items/enchants/c14a_enchant.dbr"),
    ("ring1",     "records/items/gearaccessories/rings/d110_ring.dbr", [],
     "records/items/materia/compa_runeboundtopaz.dbr",
     "records/items/enchants/b126a_enchant.dbr"),
    ("ring2",     "records/items/gearaccessories/rings/b103e_ring.dbr",
     ["records/items/lootaffixes/prefix/aa009b_oamod_01.dbr",
      "records/items/lootaffixes/suffix/b_ar051_je_f.dbr"],
     "records/items/materia/compa_bloodiedcrystal.dbr",
     "records/items/enchants/b130a_enchant.dbr"),
    ("waist",     "records/items/gearaccessories/waist/d108_waist.dbr", [],
     "records/items/materia/compa_spellscorchedplating.dbr",
     "records/items/enchants/c203a_enchant.dbr"),
    ("shoulders", "records/items/upgraded/gearshoulders/d026_shoulder.dbr",
     ["records/items/lootaffixes/crafting/ao14_oa.dbr"],
     "records/items/materia/compb_livingarmor.dbr",
     "records/items/enchants/c203a_enchant.dbr"),
    ("medal",     "records/items/gearaccessories/medals/b016e_medal.dbr",
     ["records/items/lootaffixes/prefix/b_ar024_ar_f.dbr",
      "records/items/lootaffixes/suffix/a028b_off_dmg%phys_09_je.dbr"],
     "records/items/materia/compb_arcanespark.dbr",
     "records/items/enchants/runes/d203_rune.dbr"),
    ("relic",     "records/items/gearrelic/d114_relic.dbr",
     ["records/items/lootaffixes/completionrelics/ao17a_oa.dbr"], None, None),
    ("weapon",    WEAPON, [], "records/items/materia/compa_sealmight.dbr",
     "records/items/enchants/b06a_enchant.dbr"),
]

#: Skill_Modifier records whose PARENT is an always-on aura/passive, so their stats ride the aura.
AURA_MODS = {"records/skills/playerclass01/fieldcommand2.dbr",
             "records/skills/playerclass09/presenceofvirtue2.dbr",
             "records/skills/playerclass09/presenceofvirtue3.dbr"}
ALWAYS_ON = {"Skill_Passive", "Skill_Mastery", "Skill_BuffSelfToggled", "Skill_BuffRadiusToggled"}
#: Always-on item-granted skills (both are permanent: a toggled component aura and a 2h passive).
ITEM_PASSIVES = (("records/skills/itemskillsgdx1/legendary/gladiatorpersistence.dbr", 2),
                 ("records/skills/itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr", 1))
#: CHANCE-GATED, therefore NOT part of the permanent stack.  Named so the exclusion is visible.
CHANCE_GATED = {("gear:weapon:augment", "offensiveTotalDamageModifier")}

STAT_PREFIX = ("offensive", "character", "augment", "retaliation", "weaponDamagePct",
               "conversion", "skillManaCostReduction")


def build_stack():
    """Return (acc, prov) -- the permanent offensive/defensive modifier stack composed from the
    save's ACTUAL allocations and the item records they name."""
    _h, _b8, _v, _n, rows, _isc, _t = read_skill_block(PLAYED_SAVE)
    bonuses = sheet_skill_bonuses()
    acc: dict[str, float] = collections.defaultdict(float)
    prov: dict[str, list] = collections.defaultdict(list)

    def add(src, r, rank=1):
        if not r:
            return
        for k, v in r.items():
            if not k.startswith(STAT_PREFIX):
                continue
            if (src, k) in CHANCE_GATED:
                continue
            if isinstance(v, list):
                if not v or not isinstance(v[0], (int, float)) or isinstance(v[0], bool):
                    continue
                vv, how = at_rank(v, rank)
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                vv, how = v, "scalar"
            else:
                continue
            if not vv:
                continue
            acc[k] += float(vv)
            prov[k].append((src, float(vv), how, rank))

    for slot, base, affixes, comp, aug in EQUIP:
        add(f"gear:{slot}:base", rec(base))
        for a in affixes:
            add(f"gear:{slot}:affix", rec(a))
        if comp:
            add(f"gear:{slot}:component", rec(comp))
        if aug:
            add(f"gear:{slot}:augment", rec(aug))

    # Warborn: 3 of the 4 set members are equipped -> the set arrays are read at index pieces-1 = 2
    sr = rec(WARBORN)
    for k, v in sr.items():
        if k.startswith(STAT_PREFIX) and isinstance(v, list) and v \
                and isinstance(v[0], (int, float)) and not isinstance(v[0], bool) and len(v) >= 3:
            if v[2]:
                acc[k] += float(v[2])
                prov[k].append(("set:warborn@3pc", float(v[2]), "set-index=pieces-1=2", 3))

    for r in rows:
        p = r["record"]
        if p.startswith("records/skills/devotion/") and r["rank_allocated"] == 1:
            rr = rec(p)
            if rr.get("Class") == "Skill_Passive":
                add("devotion:" + p.split("/")[-1], rr, 1)

    mdir = {"playerclass01": "bonus_soldier_skills", "playerclass09": "bonus_oathkeeper_skills"}
    for r in rows:
        p = r["record"]
        if not p.startswith("records/skills/playerclass") or r["rank_allocated"] <= 0:
            continue
        eff = (r["rank_allocated"] + bonuses.get("bonus_all_skills", 0)
               + bonuses.get(mdir.get(p.split("/")[2], "_"), 0))
        rr = rec(p)
        if rr.get("Class") in ALWAYS_ON:
            tgt = rr.get("buffSkillName")
            add(f"skill:{p.split('/')[-1]}", rec(tgt) if tgt else rr, eff)
        elif p in AURA_MODS:
            add(f"auramod:{p.split('/')[-1]}", rr, eff)

    for gp, lvl in ITEM_PASSIVES:
        add("itemskill:" + gp.split("/")[-1], rec(gp), lvl)
    return acc, prov, rows, bonuses


def sheet() -> dict:
    d = {}
    with LAP_A_SHEET.open() as f:
        for row in csv.reader(f):
            if row and row[0] != "stat":
                d[row[0]] = row[1]
    return d


def dump(name: str, rows, cols) -> tuple[str, int]:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return hashlib.sha256(p.read_bytes()).hexdigest(), len(rows)


def main() -> None:
    S = sheet()
    acc, prov, skrows, bonuses = build_stack()
    digests, counts, verify = {}, {}, []

    def chk(name, ok, detail):
        verify.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
        L(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # L1 -- EoR PER-HIT ARITHMETIC
    # ══════════════════════════════════════════════════════════════════════════════════════════
    L("\n=== L1 -- EoR per-hit arithmetic ===")
    e = rec(EOR)
    w = rec(WEAPON)
    gm = rec("records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr")
    hm = rec("records/skills/itemskillsgdx2/skillmodifiers/legendary/hands_d206_eyeofreckoning.dbr")
    hd = rec("records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/head_d028_eyeofreckoning.dbr")
    st = rec("records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/set_d025_eyeofreckoning.dbr")
    ge = rec(GAMEENGINE)

    alloc = {r["record"]: r["rank_allocated"] for r in skrows}
    a_eor = alloc.get(EOR, 0)
    # ⚑ IS-L1.  The rank algebra, from THREE measured surfaces, not two.
    plus_all = bonuses.get("bonus_all_skills", 0)          # Lap A sheet frame 512
    plus_oath = bonuses.get("bonus_oathkeeper_skills", 0)  # Lap A sheet frame 512
    # Gutsmasher's SKILL-SPECIFIC augment -- the term IS-G1 missed and Lap A's prose half-saw.
    aug_specific = 0
    for i in (1, 2, 3, 4, 5):
        if w.get(f"augmentSkillName{i}") == EOR:
            aug_specific = int(w.get(f"augmentSkillLevel{i}") or 0)
    eff16 = a_eor + plus_all + plus_oath
    eff20 = eff16 + aug_specific
    L(f"  EoR allocated={a_eor}  +all={plus_all}  +oathkeeper={plus_oath} "
      f"+item-specific={aug_specific}  ->  effective={eff20}  (IS-G1 said {eff16})")
    chk("L1-rank-ceiling", eff20 <= int(e.get("skillUltimateLevel") or 0),
        f"effective {eff20} <= skillUltimateLevel {e.get('skillUltimateLevel')} "
        f"(skillMaxLevel {e.get('skillMaxLevel')})")

    rows1 = []

    def q(quantity, value, unit, srec, sfield, idx, grade, note=""):
        rows1.append(dict(quantity=quantity, value=value, unit=unit, source_record=srec,
                          source_field=sfield, index=idx, grade=grade,
                          source_archive=arc_of(srec) if srec.startswith("records/") else "",
                          note=note))

    q("eor_rank_allocated", a_eor, "rank", "player.gdc block 8", "rank_allocated", "",
      "MEASURED", "sha256 b8e6f510...bfa5, 98,101 bytes")
    q("eor_rank_bonus_all_skills", plus_all, "rank", str(LAP_A_SHEET.name), "bonus_all_skills",
      "frame 512", "MEASURED", "Lap A camera sheet")
    q("eor_rank_bonus_oathkeeper", plus_oath, "rank", str(LAP_A_SHEET.name),
      "bonus_oathkeeper_skills", "frame 512", "MEASURED", "")
    q("eor_rank_bonus_item_specific", aug_specific, "rank", WEAPON, "augmentSkillLevel2", "",
      "MEASURED", "augmentSkillName2 == eyeofreckoning1.dbr -- IS-L1, the term IS-G1 dropped")
    q("eor_rank_effective", eff20, "rank", "(composed)", "", "",
      "DERIVED-SUM", "15+1+0+4; ceiling is skillUltimateLevel=26")

    for rk, lbl in ((eff16, "candidate_rank16"), (eff20, "run_of_record_rank20")):
        wd, how = at_rank(e["weaponDamagePct"], rk)
        pmin, _ = at_rank(e["offensivePhysicalMin"], rk)
        pmax, _ = at_rank(e["offensivePhysicalMax"], rk)
        fmin, _ = at_rank(e["offensiveFireMin"], rk)
        mana, _ = at_rank(e["skillManaCost"], rk)
        q(f"{lbl}:weaponDamagePct_skill", wd, "percent", EOR, "weaponDamagePct", rk - 1,
          "MEASURED", how)
        q(f"{lbl}:weaponDamagePct_total", wd + float(gm.get("weaponDamagePct") or 0),
          "percent", "(composed)", "weaponDamagePct", "",
          "DERIVED-SUM", "skill + Gutsmasher EoR-modifier +14; Warborn's +5 needs 4 pieces, he has 3")
        q(f"{lbl}:flat_physical_min", pmin, "damage", EOR, "offensivePhysicalMin", rk - 1, "MEASURED", "")
        q(f"{lbl}:flat_physical_max", pmax, "damage", EOR, "offensivePhysicalMax", rk - 1, "MEASURED", "")
        q(f"{lbl}:flat_fire_min", fmin, "damage", EOR, "offensiveFireMin", rk - 1, "MEASURED",
          "100% converted to physical by the Gutsmasher EoR modifier")
        q(f"{lbl}:mana_per_tick", mana, "energy", EOR, "skillManaCost", rk - 1, "MEASURED", "")

    q("eor_flat_physical_add_gear", hm.get("offensivePhysicalMin"), "damage",
      "records/skills/itemskillsgdx2/skillmodifiers/legendary/hands_d206_eyeofreckoning.dbr",
      "offensivePhysicalMin", "", "MEASURED", "Sandreaver Bracers, EoR-scoped")
    q("eor_crit_damage_add_gear", hd.get("offensiveCritDamageModifier"), "percent",
      "records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/head_d028_eyeofreckoning.dbr",
      "offensiveCritDamageModifier", "", "MEASURED", "Warborn Visor, EoR-scoped")
    q("eor_set_weaponDamagePct_INACTIVE", st.get("weaponDamagePct"), "percent",
      "records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/set_d025_eyeofreckoning.dbr",
      "weaponDamagePct", "", "MEASURED-INACTIVE",
      "itemSkillModifierControl=[0,0,0,1] -> 4-piece gate; 3 pieces equipped")
    q("eor_bleed_flat_gear", gm.get("offensiveSlowBleedingMin"), "damage_over_time",
      "records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr",
      "offensiveSlowBleedingMin", "", "MEASURED",
      f"duration {gm.get('offensiveSlowBleedingDurationMin')}s; + hands {hm.get('offensiveSlowBleedingMin')}")

    q("weapon_base_physical_min", w["offensivePhysicalMin"], "damage", WEAPON,
      "offensivePhysicalMin", "", "MEASURED", "Gutsmasher; Lap A camera read 144-740 EXACT")
    q("weapon_base_physical_max", w["offensivePhysicalMax"], "damage", WEAPON,
      "offensivePhysicalMax", "", "MEASURED", "")
    q("weapon_bonus_physical_min", w["offensiveBonusPhysicalMin"], "damage", WEAPON,
      "offensiveBonusPhysicalMin", "", "MEASURED", "")
    q("weapon_bonus_physical_max", w["offensiveBonusPhysicalMax"], "damage", WEAPON,
      "offensiveBonusPhysicalMax", "", "MEASURED", "")
    q("weapon_conversion_1", f"{w['conversionInType']}->{w['conversionOutType']} "
      f"{w['conversionPercentage']}%", "conversion", WEAPON, "conversionPercentage", "",
      "MEASURED", "Lap A camera read 55% -- record says 50%; camera and table DISAGREE (see method)")
    q("weapon_conversion_2", f"{w['conversionInType2']}->{w['conversionOutType2']} "
      f"{w['conversionPercentage2']}%", "conversion", WEAPON, "conversionPercentage2", "",
      "MEASURED", "Lap A camera read 46%")
    q("eor_conversion_skill_scoped", f"{gm['conversionInType']}->{gm['conversionOutType']} "
      f"{gm['conversionPercentage']}%", "conversion",
      "records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr",
      "conversionPercentage", "", "MEASURED", "EoR-scoped: all EoR fire damage becomes physical")
    q("component_conversion", "Aether->Physical 25%", "conversion",
      "records/items/materia/compa_sealmight.dbr", "conversionPercentage", "", "MEASURED", "")

    # ---- the channel cadence law -------------------------------------------------------------
    tba = float(e["timeBetweenAttacks"])
    period_100 = tba * 0.0008
    as_stat_pct = float(S["attack_speed"])                  # 196  (sheet stat line)
    aps_sheet = float(S["attacks_per_second"])              # 2.66 (sheet, same page)
    wpn_aps = float(S["weapon_attacks_per_second"])         # 1.46 (item tooltip)
    as_impl = aps_sheet / wpn_aps                           # 1.8219...  implied multiplier
    q("channel_timeBetweenAttacks", tba, "0.8ms_quanta", EOR, "timeBetweenAttacks", "",
      "MEASURED", "template: 'Time between hits to enemies along the path'")
    q("channel_period_at_100pct_AS", round(period_100, 6), "seconds", "(composed)",
      "timeBetweenAttacks*0.0008", "", "DERIVED",
      "quantum established at PE-1 across the whole spin/beam family")
    q("attack_speed_stat_line", as_stat_pct, "percent", str(LAP_A_SHEET.name), "attack_speed",
      "frame 511", "MEASURED", "")
    q("attack_speed_implied_by_APS", round(as_impl * 100, 4), "percent", str(LAP_A_SHEET.name),
      "attacks_per_second / weapon_attacks_per_second", "frames 511/495", "MEASURED-DERIVED",
      "the sheet's own two readings do NOT agree; both carried, LO/HI per R-PM4-2 (monotone scalar)")
    for lbl, mult in (("LO", as_impl), ("HI", as_stat_pct / 100.0)):
        q(f"channel_hit_period_{lbl}", round(period_100 / mult, 6), "seconds", "(composed)",
          "period_at_100pct / attack_speed_multiplier", "", "DERIVED-BRACKET", "")
        q(f"channel_hit_rate_{lbl}", round(mult / period_100, 4), "hits_per_second", "(composed)",
          "1 / hit_period", "", "DERIVED-BRACKET", "")
    q("channel_duration", e["duration"], "seconds", EOR, "duration", "", "MEASURED",
      "channel re-arm window; useResetsDuration=True")
    q("channel_rotationSpeedMultiplier", round(float(e["rotationSpeedMultiplier"]), 4), "ratio",
      EOR, "rotationSpeedMultiplier", "", "MEASURED", "turning cost while channelling")
    q("channel_canUseWhileMoving", e["canUseWhileMoving"], "bool", EOR, "canUseWhileMoving", "",
      "MEASURED", "Lap G positive control -- reproduced from this seat")
    q("sheet_eor_damage_per_hit", S["eye_of_reckoning_damage_per_hit"], "damage",
      str(LAP_A_SHEET.name), "eye_of_reckoning_damage_per_hit", "frame 511",
      "MEASURED-BY-CAMERA", "the GAME'S OWN composed per-hit figure -- the run-of-record magnitude")
    q("sheet_weapon_damage_per_hit", S["weapon_damage_per_hit"], "damage", str(LAP_A_SHEET.name),
      "weapon_damage_per_hit", "frame 511", "MEASURED-BY-CAMERA", "")

    d, n = dump("pm4l_eor_per_hit.csv", rows1,
                ["quantity", "value", "unit", "source_record", "source_archive", "source_field",
                 "index", "grade", "note"])
    digests["pm4l_eor_per_hit.csv"], counts["pm4l_eor_per_hit.csv"] = d, n
    chk("L1-canUseWhileMoving-positive-control", e["canUseWhileMoving"] is True,
        "eyeofreckoning1.canUseWhileMoving == 1, reproducing Lap G § 7 clause 1")
    chk("L1-weapon-base-vs-camera",
        float(w["offensivePhysicalMin"]) == 144.0 and float(w["offensivePhysicalMax"]) == 740.0,
        "Gutsmasher offensivePhysical 144-740 == Lap A camera read 144-740 (independent surfaces)")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # L2 -- THE MODIFIER STACK  +  the composition law, verified against the game's own sheet
    # ══════════════════════════════════════════════════════════════════════════════════════════
    L("\n=== L2 -- the modifier stack ===")
    rows2 = []
    for stat in sorted(prov):
        for src, val, how, rank in prov[stat]:
            rows2.append(dict(stat=stat, value=val, source=src, source_kind=src.split(":")[0],
                              rank_used=rank, index_note=how, grade="MEASURED",
                              basis="record field read at the save's own allocation"))
    for stat in sorted(acc):
        rows2.append(dict(stat=stat, value=round(acc[stat], 4), source="__SUM__",
                          source_kind="composed", rank_used="", index_note="",
                          grade="DERIVED-SUM-ADDITIVE-WITHIN-FIELD",
                          basis="additive within field (the L-65 life-chain law, re-verified in L2.1)"))

    # ---- L2.1  THE COMPOSITION LAW, discriminated against the camera sheet -------------------
    # Candidate A: sheet %type = SUM(type-specific) + SUM(offensiveTotalDamageModifier)   [additive]
    # Candidate B: sheet %type = SUM(type-specific), total applied multiplicatively later  [mult]
    # The discriminator is any damage type where the type-specific sum is KNOWN-SMALL: if A holds,
    # sheet-minus-typespecific is the SAME constant for every such type.
    tot = acc.get("offensiveTotalDamageModifier", 0.0)
    elem = acc.get("offensiveElementalModifier", 0.0)
    law_rows = [
        ("aether",         "offensiveAetherModifier",        float(S["aether_modifier"]),        acc.get("offensiveAetherModifier", 0.0)),
        ("vitality",       "offensiveLifeModifier",          float(S["vitality_modifier"]),      acc.get("offensiveLifeModifier", 0.0)),
        ("cold",           "offensiveColdModifier",          float(S["cold_modifier"]),          acc.get("offensiveColdModifier", 0.0) + elem),
        ("lightning",      "offensiveLightningModifier",     float(S["lightning_modifier"]),     acc.get("offensiveLightningModifier", 0.0) + elem),
        ("acid_poison",    "offensivePoisonModifier",        float(S["acid_modifier"]),          acc.get("offensivePoisonModifier", 0.0)),
        ("electrocute",    "offensiveSlowLightningModifier", float(S["electrocute_modifier"]),   acc.get("offensiveSlowLightningModifier", 0.0)),
        ("vitality_decay", "offensiveSlowLifeModifier",      float(S["vitality_decay_modifier"]), acc.get("offensiveSlowLifeModifier", 0.0)),
        ("pierce",         "offensivePierceModifier",        float(S["pierce_modifier"]),        acc.get("offensivePierceModifier", 0.0)),
        ("fire",           "offensiveFireModifier",          float(S["fire_modifier"]),          acc.get("offensiveFireModifier", 0.0) + elem),
        ("bleed",          "offensiveSlowBleedingModifier",  float(S["bleed_modifier"]),         acc.get("offensiveSlowBleedingModifier", 0.0)),
        ("trauma",         "offensiveSlowPhysicalModifier",  float(S["trauma_modifier"]),        acc.get("offensiveSlowPhysicalModifier", 0.0)),
        ("physical",       "offensivePhysicalModifier",      float(S["physical_modifier"]),      acc.get("offensivePhysicalModifier", 0.0)),
    ]
    implied = [(nm, sh - own) for nm, _f, sh, own in law_rows]
    exact = [nm for nm, v in implied if abs(v - 337.0) < 0.5]
    L(f"  implied global term per type: " + ", ".join(f"{nm}={v:+.0f}" for nm, v in implied))
    L(f"  EXACT at 337 on: {exact}")
    for nm, fld, sh, own in law_rows:
        rows2.append(dict(stat=fld, value=round(sh, 4), source="__SHEET_CAMERA__",
                          source_kind="corroboration", rank_used="frame 513-516",
                          index_note=f"{nm}: sheet {sh:.0f} - table-sum {own:.0f} = {sh-own:+.0f}",
                          grade="MEASURED-BY-CAMERA",
                          basis="Lap A measured-player-sheet.csv"))
    rows2.append(dict(stat="__LAW__global_total_damage_term", value=337.0, source="__INVERSION__",
                      source_kind="composed", rank_used="",
                      index_note=f"EXACT on {len(exact)} independent damage types: {','.join(exact)}",
                      grade="MEASURED-BY-INVERSION",
                      basis="sheet%type - table-sum(type) is the SAME constant 337 on those types "
                            "=> the total-damage term is ADDITIVE with the type term, not multiplicative"))
    rows2.append(dict(stat="__LAW__table_sum_offensiveTotalDamageModifier", value=round(tot, 4),
                      source="__SUM__", source_kind="composed", rank_used="",
                      index_note="chance-gated weapon-augment line EXCLUDED (see CHANCE_GATED)",
                      grade="DERIVED-SUM",
                      basis=f"reaches {tot:.0f} of the inverted 337 -- residual {337-tot:+.0f} DECLARED (D-L2)"))
    d, n = dump("pm4l_modifier_stack.csv", rows2,
                ["stat", "value", "source", "source_kind", "rank_used", "index_note", "grade", "basis"])
    digests["pm4l_modifier_stack.csv"], counts["pm4l_modifier_stack.csv"] = d, n
    chk("L2-composition-law-exact-count", len(exact) >= 4,
        f"{len(exact)} damage types reproduce the SAME global term 337 EXACTLY: {exact}")
    chk("L2-devotion-count", sum(1 for r in skrows
                                 if r["record"].startswith("records/skills/devotion/")
                                 and r["rank_allocated"] == 1) == int(S["devotion_points_spent"]),
        f"55 devotion rows carry rank_allocated==1 == sheet devotion_points_spent "
        f"{S['devotion_points_spent']} (devotion_level is NOT the allocation flag -- 285 rows carry it)")
    chk("L2-crit-damage-within-1pt",
        abs(acc.get("offensiveCritDamageModifier", 0) - float(S["critical_damage"])) <= 1.0,
        f"table {acc.get('offensiveCritDamageModifier')} vs sheet {S['critical_damage']}")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # L3 -- TARGET MULTIPLICITY
    # ══════════════════════════════════════════════════════════════════════════════════════════
    L("\n=== L3 -- target multiplicity ===")
    rows3 = []

    def t(field, value, srec, grade, note):
        rows3.append(dict(field=field, value=value, source_record=srec,
                          source_archive=arc_of(srec) if srec.startswith("records/") else "",
                          grade=grade, note=note))

    t("skillTargetRadius", e["skillTargetRadius"], EOR, "MEASURED",
      "metres, Lap-F display contract; == the sim's EOR_RADIUS_M")
    t("targetingMode", e["targetingMode"], EOR, "MEASURED", "'Point' -- centred on the caster")
    for f in ("skillTargetNumber", "skillMaxTargets", "targetTypeMax", "skillProjectileNumber",
              "skillTargetAngle", "skillTargetAngleMax", "numTargets", "maxTargets"):
        t(f, e.get(f, "ABSENT"), EOR, "MEASURED-ABSENT" if e.get(f) is None else "MEASURED",
          "no target-count field is declared on the record")
    t("meleeTargetDistance", ge["meleeTargetDistance"], GAMEENGINE, "MEASURED",
      "the engine's own melee contact distance == the sim's D_ENGAGE_M")
    t("meleeAutoTargetDistance", ge["meleeAutoTargetDistance"], GAMEENGINE, "MEASURED", "")
    t("eor_modifier_projectilePeriod", rec(EOR_MOD).get("projectilePeriod"), EOR_MOD, "MEASURED",
      "Soulfire, the allocated EoR modifier: an ORBITING projectile, 1 per period, pierces 100%")
    t("eor_modifier_skillProjectileNumber", rec(EOR_MOD).get("skillProjectileNumber"), EOR_MOD,
      "MEASURED", "")
    d, n = dump("pm4l_target_multiplicity.csv", rows3,
                ["field", "value", "source_record", "source_archive", "grade", "note"])
    digests["pm4l_target_multiplicity.csv"], counts["pm4l_target_multiplicity.csv"] = d, n
    chk("L3-no-target-cap-field",
        all(e.get(f) is None for f in ("skillTargetNumber", "skillMaxTargets", "numTargets",
                                       "maxTargets")),
        "Skill_AttackRadiusSpin declares NO target-count field -> multiplicity is GEOMETRIC "
        "(every body whose centre lies within skillTargetRadius), i.e. DENSITY-DEPENDENT and uncapped")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # L4 -- MONSTER-SIDE MITIGATION, per body, per wave
    # ══════════════════════════════════════════════════════════════════════════════════════════
    L("\n=== L4 -- monster-side mitigation ===")
    cf = rec(COMBATF)
    board = collections.defaultdict(dict)
    with (LAPD / "pm4d_band_b_ehp_by_wave.csv").open() as f:
        for r in csv.DictReader(f):
            if not r.get("wave"):
                continue
            wv = int(r["wave"])
            if 151 <= wv <= 170 and is_body(r["record"]):
                board[r["record"]][wv] = (int(r["level_lo"]), int(r["level_hi"]),
                                          r["ehp_lo"], r["ehp_hi"])
    bandc = collections.defaultdict(dict)
    with (LAPI / "pm4i_band_c_ehp_by_wave.csv").open() as f:
        for r in csv.DictReader(f):
            if not r.get("wave"):
                continue
            wv = int(r["wave"])
            if 171 <= wv <= 180 and is_body(r["record"]):
                bandc[r["record"]][wv] = (int(r["level_lo"]), int(r["level_hi"]),
                                          r["ehp_lo"], r["ehp_hi"])
    for k, v in bandc.items():
        board[k].update(v)
    L(f"  bodies on the 151-180 board: {len(board)}")

    surv = survival_arrays("03")
    RES = ("Physical", "Pierce", "Fire", "Cold", "Lightning", "Poison", "Life", "Aether",
           "Chaos", "Bleeding")
    dpak, dflat, _dwhich = difficulty_pak()

    def defense_of(record: str, Lv: float):
        """Armour + absorption + per-type resist + DA, composed exactly like the life chain:
        bio equation (level-driven) + every `skillName{i}` passive read at its own
        `skillLevel{i}` equation.  Same reader (whole-record replacement), same failure taxonomy."""
        r, _arc = E3.winner(record)
        c = resolve(E3, record)
        out = {k: 0.0 for k in ("armor", "absorption_mod", "DA")}
        for k in RES:
            out["res" + k] = 0.0
        srcs = []
        if not c.ok:
            return None, c.reason, srcs
        bio, _ = E3.winner(c.bio)
        if bio:
            if bio.get("defensiveProtection"):
                out["armor"] += ev(bio["defensiveProtection"], Lv); srcs.append("bio.defensiveProtection")
            if bio.get("characterDefensiveAbility"):
                out["DA"] += ev(bio["characterDefensiveAbility"], Lv); srcs.append("bio.characterDefensiveAbility")

        def take(src_rec, rank_expr):
            s, _ = E3.winner(src_rec)
            if not s:
                return
            idx = max(0, int(ev(rank_expr, Lv)) - 1) if rank_expr is not None else 0
            for field, key in ([("defensiveProtection", "armor"),
                                ("defensiveAbsorptionModifier", "absorption_mod"),
                                ("characterDefensiveAbility", "DA")]
                               + [("defensive" + k, "res" + k) for k in RES]):
                v = s.get(field)
                if v is None:
                    continue
                if isinstance(v, list):
                    if not v or not isinstance(v[0], (int, float)):
                        continue
                    j = min(idx, len(v) - 1)
                    if v[j]:
                        out[key] += float(v[j]); srcs.append(f"{src_rec.split('/')[-1]}.{field}[{j}]")
                elif isinstance(v, (int, float)) and not isinstance(v, bool) and v:
                    out[key] += float(v); srcs.append(f"{src_rec.split('/')[-1]}.{field}")

        take(record, None)
        for sn, sl in c.passives:
            take(sn, sl)
        return out, "OK", srcs

    absorb_default = float(ge["armorDefensiveAbsorption"])
    rows4, rows5 = [], []
    OA = float(S["offensive_ability"])
    crit_dmg_pct = float(S["critical_damage"])
    pth_th = [float(cf[f"pthThreshold{i}"]) for i in range(1, 7)]
    pth_mu = [float(cf[f"pthDamageModifier{i}"]) for i in range(1, 7)]
    pth_min = float(cf["pthMinimum"])

    def pth(oa, da):
        return ((((oa / ((da / 3.5) + oa)) * 300) * 0.3)
                + (((((oa * 3.25) + 10000) - (da * 3.25)) / 100) * 0.7)) - 50

    def crit_tier(p):
        m, tier = 1.0, 0
        for i in range(6):
            if p >= pth_th[i]:
                m, tier = pth_mu[i], i + 1
        return m, tier

    # the run-of-record per-revolution PHYSICAL magnitude (pre-mitigation), from the game's own
    # sheet -- carried as LO/HI over the sheet's printed min-max (monotone scalar, R-PM4-2 legal)
    ph_lo, ph_hi = (float(x) for x in S["eye_of_reckoning_damage_per_hit"].split("-"))
    gaps = 0
    for record in sorted(board):
        for wv in sorted(board[record]):
            lo, hi, ehp_lo, ehp_hi = board[record][wv]
            dfn, why, srcs = defense_of(record, float(lo))
            wave_da = surv_at(surv["characterDefensiveAbility"], wv)
            wave_dam = surv_at(surv["characterDefensiveAbilityModifier"], wv)
            if dfn is None:
                gaps += 1
                rows4.append(dict(record=record, wave=wv, level=lo, armor="", absorption_pct="",
                                  DA="", grade=f"ABSENT:{why}", basis=""))
                continue
            DA = (dfn["DA"] + wave_da) * (1 + (wave_dam + float(dflat.get(
                "characterDefensiveAbilityModifier", 0.0) or 0.0)) / 100.0)
            absorb = absorb_default + dfn["absorption_mod"]
            row4 = dict(record=record, wave=wv, level=lo,
                        armor=round(dfn["armor"], 2),
                        absorption_pct=round(absorb, 2),
                        DA=round(DA, 2),
                        DA_bio=round(dfn["DA"], 2),
                        DA_wave_flat=wave_da, DA_wave_pct=wave_dam,
                        grade="MEASURED",
                        basis="bio equation @ level_lo + every skillName{i} passive at its own "
                              "skillLevel{i}; armour absorption default from gameengine.dbr")
            for k in RES:
                row4["res_" + k.lower()] = round(dfn["res" + k], 2)
            rows4.append(row4)

            p = pth(OA, DA)
            hit_chance = min(1.0, max(0.0, p / 70.0))
            mult, tier = crit_tier(p)
            resphys = dfn["resPhysical"]
            # ⚑ CLAMP, DECLARED not silent: a resistance above 100 is IMMUNITY, not healing.  No
            # corpus field expresses the clamp, so it is graded and flagged on every affected row.
            immune = resphys >= 100.0
            resfac = max(0.0, 1 - resphys / 100.0)
            for lbl, raw in (("LO", ph_lo), ("HI", ph_hi)):
                # GD armour law, verbatim from combatformulas.dbr (see method.md § L4.2)
                if raw <= dfn["armor"]:
                    after_armor = raw * (1 - absorb / 100.0)
                else:
                    after_armor = (dfn["armor"] * (1 - absorb / 100.0)) + (raw - dfn["armor"])
                applied = after_armor * resfac
                # crit tier is a STRUCTURAL unknown (the roll rule is engine-internal); the
                # MULTIPLIER it selects is a monotone scalar, so it brackets legally per R-PM4-25.
                for clbl, cm in (("critLO", 1.0), ("critHI", mult)):
                    exp = applied * hit_chance * cm
                    ehp = float(ehp_lo if lbl == "LO" else ehp_hi)
                    rows5.append(dict(record=record, wave=wv, level=lo, limb=lbl, crit_limb=clbl,
                                      raw_physical_per_rev=round(raw, 2),
                                      armor=round(dfn["armor"], 2),
                                      absorption_pct=round(absorb, 2),
                                      res_physical_pct=round(resphys, 2),
                                      immune_physical=immune,
                                      after_armor=round(after_armor, 2),
                                      applied_per_rev=round(applied, 2),
                                      DA=round(DA, 2), PTH=round(p, 3),
                                      hit_chance=round(hit_chance, 5),
                                      crit_tier_max=tier, crit_multiplier=cm,
                                      expected_applied_per_rev=round(exp, 2),
                                      ehp=ehp,
                                      revs_to_kill=(round(ehp / exp, 3) if exp > 0 else ""),
                                      grade="DERIVED-FROM-MEASURED" if not immune
                                            else "DERIVED-CLAMPED:IMMUNE",
                                      basis="armour law = combatformulas.physicalDamageDefenseEquation*; "
                                            "PTH = combatformulas.probabilityToHitEquation; "
                                            "hit = normalPTHEquation (PTH/70); crit tier = pthThreshold*"))
    d, n = dump("pm4l_mitigation_by_body.csv", rows4,
                ["record", "wave", "level", "armor", "absorption_pct", "DA", "DA_bio",
                 "DA_wave_flat", "DA_wave_pct"] + ["res_" + k.lower() for k in RES]
                + ["grade", "basis"])
    digests["pm4l_mitigation_by_body.csv"], counts["pm4l_mitigation_by_body.csv"] = d, n
    d, n = dump("pm4l_applied_damage_by_body.csv", rows5,
                ["record", "wave", "level", "limb", "crit_limb", "raw_physical_per_rev", "armor",
                 "absorption_pct", "res_physical_pct", "immune_physical", "after_armor",
                 "applied_per_rev", "DA", "PTH", "hit_chance", "crit_tier_max", "crit_multiplier",
                 "expected_applied_per_rev", "ehp", "revs_to_kill", "grade", "basis"])
    digests["pm4l_applied_damage_by_body.csv"], counts["pm4l_applied_damage_by_body.csv"] = d, n
    L(f"  mitigation rows {counts['pm4l_mitigation_by_body.csv']}, "
      f"applied rows {counts['pm4l_applied_damage_by_body.csv']}, named gaps {gaps}")

    ref = [r for r in rows5 if 151 <= r["wave"] <= 160]
    ap = [r["applied_per_rev"] for r in ref if not r["immune_physical"]]
    hc = [r["hit_chance"] for r in ref]
    rk = sorted(r["revs_to_kill"] for r in ref
                if r["crit_limb"] == "critHI" and r["limb"] == "LO" and r["revs_to_kill"] != "")
    L(f"  waves 151-160 applied-per-rev range (non-immune): {min(ap):.0f} .. {max(ap):.0f}")
    L(f"  waves 151-160 hit-chance range: {min(hc):.4f} .. {max(hc):.4f}")
    L(f"  waves 151-160 immune-physical rows: {sum(1 for r in ref if r['immune_physical'])}"
      f" of {len(ref)}")
    L(f"  waves 151-160 revs_to_kill (LO dmg / HI crit): min {rk[0]} med {rk[len(rk)//2]} "
      f"max {rk[-1]}")
    chk("L4-no-negative-applied", min(ap) >= 0.0, f"minimum applied_per_rev = {min(ap):.2f}")
    chk("L4-player-cannot-miss-this-board", min(hc) >= 1.0,
        f"normalPTHEquation = PTH/70 and the board's minimum PTH is "
        f"{min(r['PTH'] for r in ref):.1f} -> hit chance saturates at 1.0 on EVERY body/wave")
    chk("L4-armor-law-source", "physicalDamageDefenseEquationDGP" in cf,
        "armour law read verbatim from combatformulas.dbr, both branches present")
    chk("L4-absorption-closes-lapA-gap", absorb_default == 70.0,
        "gameengine.armorDefensiveAbsorption = 70.0 -- Lap A's armor_absorption_pct GAP is CLOSED")
    chk("L4-two-slot-crit-law", len(pth_th) == 6 and len(pth_mu) == 6,
        f"pthThreshold1..6 = {pth_th}; pthDamageModifier1..6 = {pth_mu}; pthMinimum = {pth_min}")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    json.dump({"digests": digests, "row_counts": counts, "checks": verify,
               "board_bodies": len(board), "named_gaps": gaps,
               "eor_effective_rank": eff20, "is_g1_rank": eff16,
               "global_total_damage_term_inverted": 337.0,
               "global_total_damage_term_table_sum": round(tot, 4),
               "law_exact_types": exact,
               "armor_absorption_pct": absorb_default,
               "hit_period_s_LO": round(period_100 / as_impl, 6),
               "hit_period_s_HI": round(period_100 / (as_stat_pct / 100.0), 6)},
              (OUT / "pm4l_emit_summary.json").open("w"), indent=1)
    (OUT / "emit.log").write_text("\n".join(log_lines) + "\n")
    L("\n=== DIGESTS ===")
    for k in sorted(digests):
        L(f"  {k}  rows={counts[k]}  sha256={digests[k]}")


if __name__ == "__main__":
    main()
