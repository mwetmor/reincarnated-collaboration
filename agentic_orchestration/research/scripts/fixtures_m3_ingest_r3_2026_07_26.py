#!/usr/bin/env python3
"""
fixtures.db - MILESTONE 3: round-3 ingestion, the first CERTIFIED candidate set
===============================================================================
Ingests `research/knowledge/gd/live-probe-3/` - 12 character-sheet shots,
6 trial shots, GD-console-notes-v3-raw.md, matt-addendum-timing-uncertainty.md.

Agent: elrond. Commissioner: gandalf (GD program, gap 5).
Run AFTER m1 + m2. Idempotent.

METHOD LAW (non-negotiable for this milestone)
----------------------------------------------
Every banked digit comes from a FULL-RESOLUTION crop of the native 1920x1080 PNG:
    sips -c <h> <w> --cropOffset <y> <x>   then upscale 3x-7x
never from a downscaled full frame. Crops were taken by
`research/scripts/gd_fullres_crop_2026_07_26.py`, which crops FIRST (from original
pixels) and only then resamples upward. Downscaled full frames were used exactly
twice, for REGION LOCATION only; no value in this file comes from one.

The law earned its keep three times today:
  1. A 3x crop of the round-3 nameplate starting at y=48 read "Aether Corruption".
     The name line sits at y~22-42 and was OUTSIDE the crop. Widening to y=18
     revealed "Walking Dead" above the bar - the identity the whole certification
     turns on. The first read was not wrong about its pixels; it was wrong about
     its frame.
  2. A 1.6x crop of the entity overlay read "Level 6 / Anim State Move". At 4x the
     same pixels read "Pursue / [68957] Action State: Move". Two different claims.
  3. (M2) The round-1 panel read "Max. level achieved: 1" wide, "2" tight.

CROP GEOMETRIES USED (reproducible, all against the native PNGs)
---------------------------------------------------------------
  nameplate  -c  88 360 --cropOffset  18  800   @3.6x   (name + level + sub-line)
  PlayStats  -c 290 460 --cropOffset  45 1440   @2.6x   (T1e,T2s,T2e,T3s)
             -c 375 535 --cropOffset  35 1385   @2.8x   (T1s)
             -c 285 440 --cropOffset  48 1445   @3.6x   (T3e, re-verified)
  HP globe   -c  40 115 --cropOffset 1005 595   @7x
  entity lbl -c  36 250 --cropOffset  <per shot>@4x
  char sheet -c 500 300 --cropOffset 195 1005   @3.4x   (S20-S30)
             -c 500 450 --cropOffset 195 1000   @3x     (S19)
"""

import hashlib
import os
import sqlite3

REPO = "/Users/admin/Games/reincarnated-collaboration"
DB = os.path.join(REPO, "agentic_orchestration/research/curated/fixtures.db")
KB = "agentic_orchestration/research/knowledge/gd/live-probe-3"
S3 = "gd-live-2026-07-26-s3"
CH = S3 + "/c1"
SET = "L0-gd-s3-set1"
FULLRES = "screenshot-fullres"
ADDENDUM = ("matt-addendum-timing-uncertainty.md: Matt, verbatim - \"it was probably 2 seconds "
            "because it took me one second for each screenshot.. hard to say at that level.\" "
            "The hand-noted seconds therefore INCLUDE ~1 s per screenshot of capture overhead: "
            "systematic bias UPWARD, real engagement plausibly ~2-3 s. Banked with "
            "uncertainty_abs = 2.0 s per that addendum.")

# --- panel ledger, all read at full res this milestone ----------------------
# shot -> (play_time_s, verbatim, total_score, deaths, kills, hpot, mpot, maxlvl,
#          dps, weaponattack, life_healed)
PANEL = {
    "t1b": (8735, "145 min 35 sec", 0, 0, 172, 0, 0, 6, 0.00, 22, 0.00),
    "t1a": (8740, "145 min 40 sec", 0, 0, 173, 0, 0, 6, 23.57, 24, 0.00),
    "t2b": (8864, "147 min 44 sec", 0, 0, 174, 0, 0, 6, 0.00, 26, 4.24),
    "t2a": (8869, "147 min 49 sec", 0, 0, 175, 0, 0, 6, 22.88, 28, 20.28),
    "t3b": (8943, "149 min 3 sec", 0, 0, 175, 0, 0, 6, 0.00, 28, 24.42),
    "t3a": (8947, "149 min 7 sec", 0, 0, 176, 0, 0, 6, 26.96, 31, 25.37),
}
WA = "records/skills/default/defaultweaponattack.dbr"
KICK = "records/skills/default/defaultkickattack.dbr"

TRIAL_SHOTS = [
    ("zombie-01-start.png", "t1s"), ("zombie-01-end.png", "t1e"),
    ("zombie_02_start.png", "t2s"), ("zombie_02_end.png", "t2e"),
    ("zombie-03-start.png", "t3s"), ("zombie-03-end.png", "t3e"),
]

# --- character sheet, exhaustive (12 shots, tab I + tab III scroll) ---------
# (stat_key, group, panel_label, verbatim, num, num_hi, text, unit, capture_label)
def _sheet():
    R = []

    def s(k, grp, label, verb, num=None, hi=None, txt=None, unit=None, cap="S19"):
        R.append((k, grp, label, verb, num, hi, txt, unit, cap))

    # ---- S19, tab I ----
    s("character_name", "header", "VAUGHT", "VAUGHT", txt="VAUGHT")
    s("char_level", "header", "Level", "Level 6", 6, unit="level")
    s("available_attribute_points", "attributes", "Available Points", "5 Available Points", 5)
    s("physique", "attributes", "Physique", "58", 58)
    s("cunning", "attributes", "Cunning", "56", 56)
    s("spirit", "attributes", "Spirit", "54", 54)
    s("health", "attributes", "Health", "282 / 282", 282, unit="hp")
    s("health_max", "attributes", "Health", "282 / 282", 282, unit="hp")
    s("energy", "attributes", "Energy", "258 / 258", 258, unit="energy")
    s("energy_max", "attributes", "Energy", "258 / 258", 258, unit="energy")
    s("offensive_ability", "combat", "Offensive Ability (?)", "218", 218)
    s("defensive_ability", "combat", "Defensive Ability (?)", "225", 225)
    s("damage_per_second", "combat", "Damage Per Second (?)", "66", 66, unit="dmg/s")
    s("armor_rating", "combat", "Armor Rating (?)", "16", 16)
    # resistance icon grid: 2 rows x 5. Icon->channel mapping is INFERRED from GD's
    # standard icon order; the POSITION is what was observed.
    for i, (k, v) in enumerate([("fire", 0), ("cold", 0), ("lightning", 11),
                                ("poison_acid", 14), ("pierce", 0), ("bleeding", 0),
                                ("vitality", 0), ("aether", 0), ("chaos", 0), ("stun", 0)]):
        s("resist.%s" % k, "resistances",
          "RESISTANCES icon grid position %d (row %d, col %d)" % (i + 1, i // 5 + 1, i % 5 + 1),
          "%d%%" % v, v, unit="pct")

    # ---- S20, tab III top ----
    s("weapon_attack_min", "damage-per-hit", "Weapon Attack", "31 - 83", 31, 83, unit="dmg", cap="S20")
    s("weapon_attack_max", "damage-per-hit", "Weapon Attack", "31 - 83", 83, unit="dmg", cap="S20")
    s("damage_per_hit.na", "damage-per-hit", "N/A", "0", 0, cap="S20")
    s("weapon_damage_min", "damage-per-hit", "Weapon Damage", "31 - 83", 31, 83, unit="dmg", cap="S20")
    s("weapon_damage_max", "damage-per-hit", "Weapon Damage", "31 - 83", 83, unit="dmg", cap="S20")
    s("attacks_per_second", "character", "Attacks per Second", "1.15", 1.15, unit="per-s", cap="S20")
    s("attack_speed", "character", "Attack Speed", "85%", 85, unit="pct", cap="S20")
    s("critical_damage", "character", "Critical Damage", "+ 0%", 0, unit="pct", cap="S20")
    s("run_speed", "character", "Run Speed", "100%", 100, unit="pct", cap="S20")
    s("healing_increase", "character", "Healing Increase", "+ 0%", 0, unit="pct", cap="S20")
    s("health_regeneration", "character", "Health Regeneration", "0.33", 0.33, unit="hp/s", cap="S20")
    s("energy_regeneration", "character", "Energy Regeneration", "6.54", 6.54, unit="energy/s", cap="S20")
    s("energy_absorption", "character", "Energy Absorption", "0%", 0, unit="pct", cap="S20")
    # ---- S21 ----
    s("constitution_bonus", "character", "Constitution Bonus", "+ 0%", 0, unit="pct", cap="S21")
    s("experience_gained", "character", "Experience Gained", "+ 0%", 0, unit="pct", cap="S21")
    s("light_radius", "character", "Light Radius", "+ 0%", 0, unit="pct", cap="S21")
    for m in ["All", "Soldier", "Demolitionist", "Occultist", "Nightblade", "Arcanist",
              "Shaman", "Inquisitor", "Necromancer", "Oathkeeper", "Berserker"]:
        s("skill_bonus.%s" % m.lower(), "skill-bonuses", "%s Skills" % m, "0", 0, cap="S21")
    s("physical_damage_min", "physical", "Physical Damage", "31 - 83", 31, 83, unit="dmg", cap="S21")
    s("physical_damage_max", "physical", "Physical Damage", "31 - 83", 83, unit="dmg", cap="S21")
    s("physical_modifier", "physical", "Physical Modifier", "+ 26%", 26, unit="pct", cap="S21")
    # ---- S22 ----
    for k, lbl, verb, v in [
        ("pierce_damage", "Pierce Damage", "0", 0), ("pierce_modifier", "Pierce Modifier", "+ 0%", 0),
        ("bleed_damage", "Bleed Damage", "0", 0), ("bleed_modifier", "Bleed Modifier", "+ 6%", 6),
        ("bleed_duration", "Bleed Duration", "+ 0%", 0),
        ("trauma_damage", "Trauma Damage", "0", 0), ("trauma_modifier", "Trauma Modifier", "+ 28%", 28),
        ("trauma_duration", "Trauma Duration", "+ 0%", 0),
        ("life_steal", "Life Steal", "0%", 0)]:
        s(k, "physical", lbl, verb, v, unit="pct" if "%" in verb else None, cap="S22")
    for k, lbl, verb, v in [
        ("cast_speed", "Cast Speed", "100%", 100), ("cooldown_reduction", "Cooldown Reduction", "+ 0%", 0),
        ("skill_energy_cost", "Skill Energy Cost", "- 0%", 0),
        ("health_damage", "Health Damage", "0%", 0),
        ("fire_damage", "Fire Damage", "0", 0), ("fire_modifier", "Fire Modifier", "+ 0%", 0)]:
        s(k, "magical", lbl, verb, v, unit="pct" if "%" in verb else None, cap="S22")
    # ---- S23 ----
    for k, lbl, verb, v in [
        ("cold_damage", "Cold Damage", "0", 0), ("cold_modifier", "Cold Modifier", "+ 0%", 0),
        ("lightning_damage", "Lightning Damage", "0", 0), ("lightning_modifier", "Lightning Modifier", "+ 0%", 0),
        ("acid_damage", "Acid Damage", "0", 0), ("acid_modifier", "Acid Modifier", "+ 0%", 0),
        ("vitality_damage", "Vitality Damage", "0", 0), ("vitality_modifier", "Vitality Modifier", "+ 0%", 0),
        ("aether_damage", "Aether Damage", "0", 0), ("aether_modifier", "Aether Modifier", "+ 0%", 0),
        ("chaos_damage", "Chaos Damage", "0", 0), ("chaos_modifier", "Chaos Modifier", "+ 8%", 8),
        ("burn_damage", "Burn Damage", "0", 0), ("burn_modifier", "Burn Modifier", "+ 0%", 0)]:
        s(k, "magical", lbl, verb, v, unit="pct" if "%" in verb else None, cap="S23")
    # ---- S24 ----
    for k, lbl, verb, v in [
        ("burn_duration", "Burn Duration", "+ 0%", 0),
        ("frostburn_damage", "Frostburn Damage", "0", 0), ("frostburn_modifier", "Frostburn Modifier", "+ 0%", 0),
        ("frostburn_duration", "Frostburn Duration", "+ 0%", 0),
        ("electrocute_damage", "Electrocute Damage", "0", 0), ("electrocute_modifier", "Electrocute Modifier", "+ 0%", 0),
        ("electrocute_duration", "Electrocute Duration", "+ 0%", 0),
        ("poison_damage", "Poison Damage", "0", 0), ("poison_modifier", "Poison Modifier", "+ 0%", 0),
        ("poison_duration", "Poison Duration", "+ 0%", 0),
        ("vitality_decay_damage", "Vitality Decay Damage", "0", 0),
        ("vitality_decay_modifier", "Vitality Decay Modifier", "+ 0%", 0),
        ("vitality_decay_duration", "Vitality Decay Duration", "+ 0%", 0)]:
        s(k, "magical", lbl, verb, v, unit="pct" if "%" in verb else None, cap="S24")
    s("pet_bonus.life", "pet-bonuses", "Life", "+ 0%", 0, unit="pct", cap="S24")
    s("pet_bonus.damage_s24", "pet-bonuses", "Damage", "+ 0%", 0, unit="pct", cap="S24")
    # ---- S25 / S26 pet bonuses ----
    for k in ["damage", "critical_damage", "attack_speed", "cast_speed", "run_speed",
              "offensive_ability", "defensive_ability", "physical_resist", "fire_resist",
              "cold_resist", "lightning_resist", "poison_acid_resist", "pierce_resist",
              "bleeding_resist", "vitality_resist", "aether_resist", "chaos_resist",
              "stun_resist", "trap_resist"]:
        s("pet_bonus.%s" % k, "pet-bonuses", k.replace("_", " ").title(), "+ 0%", 0,
          unit="pct", cap="S25")
    for k in ["petrify_resist", "freeze_resist", "sleep_resist", "slow_resist"]:
        s("pet_bonus.%s" % k, "pet-bonuses", k.replace("_", " ").title(), "+ 0%", 0,
          unit="pct", cap="S26")
    # ---- S27 defense ----
    for k, lbl, verb, v in [
        ("chance_to_block", "Chance to Block", "0%", 0), ("damage_blocked", "Damage Blocked", "0", 0),
        ("block_recovery", "Block Recovery", "0%", 0), ("dodge_chance", "Dodge Chance", "0%", 0),
        ("deflect_chance", "Deflect Chance", "0%", 0), ("stun_resist", "Stun Resist", "0%", 0),
        ("disruption_resist", "Disruption Resist", "0%", 0),
        ("life_leech_resist", "Life Leech Resist", "0%", 0),
        ("energy_leech_resist", "Energy Leech Resist", "0%", 0),
        ("trap_resist", "Trap Resist", "0%", 0), ("petrify_resist", "Petrify Resist", "0%", 0),
        ("freeze_resist", "Freeze Resist", "0%", 0), ("slow_resist", "Slow Resist", "0%", 0),
        ("reflect_resist", "Reflect Resist", "0%", 0)]:
        s("defense.%s" % k, "defense", lbl, verb, v, unit="pct" if "%" in verb else None, cap="S27")
    # ---- S27/S28/S29/S30 retaliation ----
    s("retaliation.physical", "retaliation", "Physical", "0", 0, cap="S27")
    for k, lbl, cap in [("physical_modifier", "Physical Modifier", "S28"),
                        ("pierce", "Pierce", "S28"), ("pierce_modifier", "Pierce Modifier", "S28"),
                        ("bleed", "Bleed", "S28"), ("bleed_modifier", "Bleed Modifier", "S28"),
                        ("trauma", "Trauma", "S28"), ("trauma_modifier", "Trauma Modifier", "S28"),
                        ("fire", "Fire", "S28"), ("fire_modifier", "Fire Modifier", "S28"),
                        ("cold", "Cold", "S28"), ("cold_modifier", "Cold Modifier", "S28"),
                        ("lightning", "Lightning", "S28"), ("lightning_modifier", "Lightning Modifier", "S28"),
                        ("acid", "Acid", "S28"), ("acid_modifier", "Acid Modifier", "S28"),
                        ("vitality", "Vitality", "S29"), ("vitality_modifier", "Vitality Modifier", "S29"),
                        ("aether", "Aether", "S29"), ("aether_modifier", "Aether Modifier", "S29"),
                        ("chaos", "Chaos", "S29"), ("chaos_modifier", "Chaos Modifier", "S29"),
                        ("burn", "Burn", "S29"), ("burn_modifier", "Burn Modifier", "S29"),
                        ("frostburn", "Frostburn", "S29"), ("frostburn_modifier", "Frostburn Modifier", "S29"),
                        ("electrocute", "Electrocute", "S30"), ("electrocute_modifier", "Electrocute Modifier", "S30"),
                        ("poison", "Poison", "S30"), ("poison_modifier", "Poison Modifier", "S30"),
                        ("vitality_decay", "Vitality Decay", "S30"),
                        ("vitality_decay_modifier", "Vitality Decay Modifier", "S30")]:
        verb = "+ 0%" if "modifier" in k else "0"
        s("retaliation.%s" % k, "retaliation", lbl, verb, 0,
          unit="pct" if "modifier" in k else None, cap=cap)
    # ---- S30 STATS ----
    s("stats.average_item_level", "stats", "Average Item Level", "1", 1, cap="S30")
    s("stats.elapsed_time", "stats", "Elapsed Time", "0:2:21", 8460, txt="0:2:21", unit="s", cap="S30")
    s("stats.monsters_killed", "stats", "Monsters Killed", "162", 162, cap="S30")
    s("stats.bosses_and_heroes_killed", "stats", "Bosses and Heroes Killed", "2", 2, cap="S30")
    s("stats.damage_dealt", "stats", "Damage Dealt", "80", 80, cap="S30")
    s("stats.damage_taken", "stats", "Damage Taken", "47", 47, cap="S30")
    s("stats.total_deaths", "stats", "Total Deaths", "0", 0, cap="S30")
    s("stats.greatest_monster_killed", "stats", "Greatest Monster Killed",
      "Kyzogg the Reanimator", txt="Kyzogg the Reanimator", cap="S30")
    return R


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def png_dims(path):
    import struct
    with open(path, "rb") as fh:
        head = fh.read(33)
    return struct.unpack(">II", head[16:24]) if head[:8] == b"\x89PNG\r\n\x1a\n" else (None, None)


def main():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    cur.execute("DELETE FROM trial_trace WHERE session_id=?", (S3,))
    cur.execute("DELETE FROM trial_measurement WHERE trial_id IN (SELECT t.trial_id FROM "
                "fixture_trial t JOIN fixture_set s USING(fixture_set_id) WHERE s.session_id=?)", (S3,))
    cur.execute("DELETE FROM fixture_trial WHERE fixture_set_id IN "
                "(SELECT fixture_set_id FROM fixture_set WHERE session_id=?)", (S3,))
    cur.execute("DELETE FROM fixture_set_constraint WHERE fixture_set_id IN "
                "(SELECT fixture_set_id FROM fixture_set WHERE session_id=?)", (S3,))
    cur.execute("DELETE FROM fixture_set WHERE session_id=?", (S3,))
    cur.execute("DELETE FROM character_stat WHERE character_id IN "
                "(SELECT character_id FROM fixture_character WHERE session_id=?)", (S3,))
    cur.execute("DELETE FROM fixture_character WHERE session_id=?", (S3,))
    cur.execute("DELETE FROM capture WHERE session_id=?", (S3,))
    cur.execute("DELETE FROM fixture_session WHERE session_id=?", (S3,))

    # ---- session ---------------------------------------------------------
    cur.execute(
        "INSERT INTO fixture_session (session_id,lane,session_date,operator,game_edition_pin,"
        "game_build_string,difficulty,container,save_identity,console_flags,rig_version,"
        "raw_notes_path,capture_dir,sim_config_ref,notes,adapter,schema_version) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (S3, "gd-live", "2026-07-26", "matt", None, None, "normal", "main-campaign", "VAUGHT",
         '{"LogData":true,"PlayStats":true,"ShowAngerLevels":true}',
         "gandalf/pc-handoff/2026-07-25-gd-trial-sheet-v3.md",
         KB + "/GD-console-notes-v3-raw.md", KB + "/",
         None,
         "Round 3: the first sitting run under the v3 sheet, and the first that closes O-4 "
         "(a character sheet exists) and attests difficulty. save_identity 'VAUGHT' is read "
         "from the character sheet header - the first time the continuity key has a value. "
         "console_flags: both overlay lines render on every entity (controller state AND "
         "'[id] Action State: X'), so ShowAngerLevels and LogData were both on. "
         "STRUCTURAL FINDING: the PlayStats panel mixes SAVE-cumulative counters (play time, "
         "kills, deaths, potions, max level - all continuous with round 2) and SESSION-"
         "cumulative counters (skills used, life healed, DPS - all RESET between round 2 and "
         "round 3: weaponattack 435 -> 22, life_healed 2311.37 -> 0.00). Cross-session deltas "
         "are therefore valid for the first group and meaningless for the second.",
         "elrond/fixtures_m3_ingest_r3_2026_07_26.py", "fixtures-v0.1"))

    # ---- captures --------------------------------------------------------
    for n in range(19, 31):
        f = "Screenshot (%d).png" % n
        ap = os.path.join(REPO, KB, f)
        w, h = png_dims(ap)
        cur.execute("INSERT INTO capture VALUES (?,?,?,?,?,?,?,?,?,?)",
                    ("%s/S%d" % (S3, n), S3, KB + "/" + f, "character-sheet", "S%d" % n,
                     sha256_file(ap), None, w, h,
                     "Character-sheet scroll position %d of 12. S19 = tab I (attributes / "
                     "combat stats / resistance grid); S20-S30 = tab III scrolled top to "
                     "bottom." % (n - 18)))
    for f, tag in TRIAL_SHOTS:
        ap = os.path.join(REPO, KB, f)
        w, h = png_dims(ap)
        cur.execute("INSERT INTO capture VALUES (?,?,?,?,?,?,?,?,?,?)",
                    ("%s/%s" % (S3, tag), S3, KB + "/" + f, "trial-frame", f,
                     sha256_file(ap), None, w, h,
                     "One frame carrying PlayStats panel + world view + entity overlay "
                     "(+ nameplate on start shots, HP globe throughout). Extension E3."))

    # ---- character -------------------------------------------------------
    cur.execute(
        "INSERT INTO fixture_character (character_id,session_id,snapshot_ordinal,"
        "valid_from_playtime_s,char_level,hp_max,energy_max,oa,da,armor_avg,"
        "weapon_dmg_min,weapon_dmg_max,attack_speed_pct,resist_json,completeness,"
        "capture_id,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (CH, S3, 1, 8460, 6, 282.0, 258.0, 218.0, 225.0, 16.0, 31.0, 83.0, 85.0,
         '{"fire":0,"cold":0,"lightning":11,"poison_acid":14,"pierce":0,"bleeding":0,'
         '"vitality":0,"aether":0,"chaos":0,"stun":0}',
         "full-sheet", S3 + "/S19",
         "VAUGHT, level 6. This is the G-5 conversion key's INPUT DOCUMENT - the first "
         "character sheet the programme has. valid_from_playtime_s 8460 comes from the "
         "sheet's own 'Elapsed Time 0:2:21' (= 141 min), which sits BELOW the trial window "
         "(145:35-149:07): either the sheet was shot before the trials, or the sheet's "
         "Elapsed Time and the panel's Play Time are different clocks. Recorded, not "
         "reconciled. The sheet still describes the character in force: its Health 282/282 "
         "and Level 6 match the trial-shot HP globes and panel exactly. "
         "COVERAGE GAP: the tab-III scroll jumps from 'Energy Absorption' (end of S20) to "
         "'Constitution Bonus' (start of S21); any lines between were not captured. "
         "WEAPON: the equipment doll shows a two-handed firearm, and the only skill counter "
         "that moves is defaultweaponattack - so this character's basic attack is RANGED, "
         "not melee. That is load-bearing for the L0 rung and is recorded as a constraint."))

    for k, grp, label, verb, num, hi, txt, unit, cap in _sheet():
        cur.execute(
            "INSERT INTO character_stat (character_id,stat_key,stat_group,value_num,"
            "value_num_hi,value_text,unit,panel_label,verbatim,read_method,uncertainty_abs,"
            "capture_id,validity_flag,validity_note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (CH, k, grp, num, hi, txt, unit, label, verb, FULLRES, 0,
             "%s/%s" % (S3, cap), "valid",
             "Resistance channel names are INFERRED from GD's standard icon order; what was "
             "observed is the grid POSITION and the percentage. panel_label records the "
             "position so the inference is reversible."
             if k.startswith("resist.") else None))

    # ---- set -------------------------------------------------------------
    cur.execute(
        "INSERT INTO fixture_set (fixture_set_id,session_id,character_id,ladder_rung,"
        "monster_record,monster_display_name,monster_identity_method,monster_identity_evidence,"
        "monster_level,monster_level_method,monster_source,pack_size,engagement_mode,"
        "area_name,intended_n,actual_n,purpose) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (SET, S3, CH, "L0", None, "Walking Dead", "screenshot-nameplate",
         "Target frame on all three start shots reads, top to bottom: 'Walking Dead' / a full "
         "health bar carrying the level numeral '6' / 'Aether Corruption'. Read at 3.6x from a "
         "full-resolution crop, -c 88 360 --cropOffset 18 800. The monster's OWN level is "
         "therefore attested at 6 - this is the charLevel the J4 bio formulas take, not the "
         "player's level (which also happens to be 6). "
         "TWO OPEN ITEMS, both recorded rather than resolved: (1) monster_record stays NULL - "
         "nothing in the curated corpus maps the display name 'Walking Dead' to a .dbr path, "
         "so the join to the .arz is a pending gap, not an attestation; (2) the sub-line "
         "'Aether Corruption' is unexplained. If it denotes an affix or aura on the creature, "
         "these are NOT vanilla zombie statlines and the fixture is a modified variant. That "
         "must be settled before any per-hit damage inference is drawn from this set.",
         6, "nameplate", "world", 1, "pre-aggroed",
         "Vicinity of The Coffinmakers (the signpost is legible in the end frames)",
         3, 3,
         "First CERTIFIED candidate set. Three consecutive kills of a level-6 Walking Dead by "
         "VAUGHT at level 6, on Normal, with nameplate identity, a full character sheet, and "
         "no level-up anywhere in the set."))

    for k, held, ev in [
        ("single-monster", "held",
         "Exactly +1 kill per trial, and exactly one entity per start frame carries the "
         "'Pursue' controller state. The three entity ids are DISTINCT (68957 / 75289 / "
         "77775), so three separate monsters were fought, one per trial."),
        ("melee-only", "unknown",
         "Ambiguous key. The MONSTER (Walking Dead) is a melee zombie by nature but nothing "
         "attests its attack mode here. For the PLAYER side see player-melee-only."),
        ("player-melee-only", "violated",
         "The equipment doll shows a two-handed firearm and the only advancing skill counter "
         "is defaultweaponattack. This character's basic attack is RANGED. Any time-to-kill "
         "from this set includes projectile travel and standoff distance, and is NOT a melee "
         "TTK. New constraint key introduced at this ingestion."),
        ("no-pack", "unknown", "A second entity is visible in the frames but it is screen-"
         "centred (entity 17677) and is most likely the player; unattested either way."),
        ("no-flee", "held", "Each trial ends with kills +1: the monster died rather than fled."),
        ("fight-to-death", "held", "kills counter advances +1 per trial."),
        ("pre-aggroed", "held",
         "The start frames for trials 1 and 3 show the monster in controller state 'Pursue' - "
         "already aggroed at capture. Trial 2's controller line was outside the crop and is "
         "not attested; its action state 'Move' is."),
        ("no-potions", "held", "Both potion counters read 0 across all six panels."),
        ("no-player-death", "held", "deaths counter reads 0 across all six panels."),
        ("no-off-trial-activity", "violated",
         "Between T1-after and T2-before: kills 173 -> 174 and defaultweaponattack 24 -> 26. "
         "One kill and two attacks outside any trial. T2-before to T3-after is clean."),
        ("no-mid-set-level-up", "held",
         "max_level_achieved reads 6 on all six panels, and the set is pinned to a single "
         "character snapshot."),
        ("no-CC-test-character", "expired",
         "Retired constraint, expired 2026-07-25. Carried per O-9 as interpretive context."),
    ]:
        cur.execute("INSERT INTO fixture_set_constraint VALUES (?,?,?,?)", (SET, k, held, ev))

    # ---- trials ----------------------------------------------------------
    for tid, ordn, t0, t1, cb, ca, ent, contam, reason, note in [
        (SET + "/t1", 1, 8735, 8740, "t1s", "t1e", "68957", 0, None, None),
        (SET + "/t2", 2, 8864, 8869, "t2s", "t2e", "75289", 1, "ledger-discontinuity",
         "Contaminated UPSTREAM only: +1 kill and +2 weapon attacks fell between T1-after and "
         "this trial's before-shot. The trial's own deltas (+1 kill, +2 attacks) are clean."),
        (SET + "/t3", 3, 8943, 8947, "t3s", "t3e", "77775", 0, None,
         "The only trial that cost HP: globe 269/282 at the end shot, matching Matt's hand-"
         "noted 13. Also the only trial needing THREE weapon attacks rather than two."),
    ]:
        cur.execute(
            "INSERT INTO fixture_trial (trial_id,fixture_set_id,trial_ordinal,lane,outcome,"
            "t_start_playtime_s,t_end_playtime_s,before_capture_id,after_capture_id,"
            "monster_entity_id,contaminated,contamination_reason,notes) "
            "VALUES (?,?,?,'gd-live','monster-killed',?,?,?,?,?,?,?,?)",
            (tid, SET, ordn, t0, t1, "%s/%s" % (S3, cb), "%s/%s" % (S3, ca), ent,
             contam, reason, note))

    # ---- measurements ----------------------------------------------------
    M = []

    def add(trial, key, phase, num, hi, text, unit, rm, unc, cap, verb,
            flag="valid", note=None, sub=""):
        M.append((trial, key, sub, phase, num, hi, text, unit, rm, unc, cap, verb, flag, note))

    for n, (bk, ak, bc, ac) in enumerate(
            [("t1b", "t1a", "t1s", "t1e"), ("t2b", "t2a", "t2s", "t2e"),
             ("t3b", "t3a", "t3s", "t3e")], start=1):
        trial = "%s/t%d" % (SET, n)
        for phase, k, cap in (("before", bk, bc), ("after", ak, ac)):
            (pt, ptv, ts, dth, kl, hp_, mp_, mlvl, dps, wa, healed) = PANEL[k]
            capid = "%s/%s" % (S3, cap)
            for key, val, verb, unit in [
                    ("play_time", pt, ptv, "s"), ("total_score", ts, str(ts), "pts"),
                    ("deaths", dth, str(dth), "count"), ("kills", kl, str(kl), "count"),
                    ("health_potions_used", hp_, str(hp_), "count"),
                    ("mana_potions_used", mp_, str(mp_), "count"),
                    ("max_level_achieved", mlvl, str(mlvl), "level"),
                    ("dps_field", dps, "%.2f" % dps, "dmg/s"),
                    ("life_healed", healed, "%.2f" % healed, "HP")]:
                add(trial, key, phase, val, None, None, unit, FULLRES, 0, capid, verb,
                    "valid",
                    ("O-6: oracle-side colour only, not in the G3 comparable set. Unlike round "
                     "2, every round-3 after-shot carries a LIVE reading (23.57 / 22.88 / "
                     "26.96) because capture latency was ~0 - the window had not lapsed."
                     if key == "dps_field" and phase == "after" else None))
            add(trial, "skill_use_count", phase, wa, None, None, "count", FULLRES, 0, capid,
                "records/skills/default/defaultweaponattack.dbr : %d" % wa, sub=WA)
            add(trial, "skill_use_count", phase, None, None, None, "count", "absent", None,
                capid, None, "valid",
                "The defaultkickattack line is ABSENT from every round-3 panel. GD lists only "
                "skills used at least once, and this counter reset with the session (it read a "
                "static 1 throughout round 2). Absence is the reading.", KICK)
            add(trial, "shield_block_chance", phase, None, None, None, "pct", "absent", None,
                capid, None, "valid",
                "The Shield block chance line is ABSENT from every round-3 panel. It was "
                "present on the round-1 panel (15.00). Consistent with the character sheet: "
                "Chance to Block 0%, and a two-handed firearm equipped - no shield.")

    # HP globes, end shots. Matt's hand notes AGREE exactly; both instruments recorded.
    for n, (hp_cur, cap) in enumerate([(282, "t1e"), (282, "t2e"), (269, "t3e")], start=1):
        trial = "%s/t%d" % (SET, n)
        add(trial, "hp_current", "after", hp_cur, None, None, "HP", FULLRES, 0,
            "%s/%s" % (S3, cap), "%d/282" % hp_cur, "valid",
            "Globe read at 7x from a full-resolution crop. AGREES exactly with Matt's hand "
            "note for this trial - the two instruments concur on all three.")
        add(trial, "hp_max", "after", 282, None, None, "HP", FULLRES, 0,
            "%s/%s" % (S3, cap), "%d/282" % hp_cur)

    # hand notes (GD-console-notes-v3-raw.md) + the timing addendum
    for n, (secs, hp_cost) in enumerate([(5, 0), (5, 0), (4, 13)], start=1):
        trial = "%s/t%d" % (SET, n)
        add(trial, "fight_seconds", "during", secs, None, None, "s", "hand-noted-point", 2.0,
            None, "Trial %d: %ds" % (n, secs), "valid", ADDENDUM)
        add(trial, "hp_cost_abs", "during", hp_cost, None, None, "HP", "hand-noted-point",
            None, None, "HP cost %d" % hp_cost, "valid",
            "Matt's post-kill globe glance. For trial 2 this DISAGREES with the panel's "
            "life_healed delta of +16.04 - see the derived row. O-7: both stand."
            if hp_cost == 0 and n == 2 else None)
        add(trial, "hp_cost_band", "during", None, None,
            "none" if hp_cost == 0 else "sliver", None, "hand-noted-point", None, None,
            "HP cost %d" % hp_cost)

    # derived: life_healed delta - the damage-taken proxy, and the O-7 disagreement
    for n, (lo, hi_, note) in enumerate([
        (0.00, 0.00, "Zero healing across the trial window AND a full globe at the end: this "
                     "trial genuinely cost no HP. Panel and hand note agree."),
        (4.24, 20.28, "+16.04 HP healed across a 5 s window in which Matt's post-kill globe "
                      "read a FULL 282/282 and his hand note says 'HP cost 0'. Both readings "
                      "stand (O-7) and they are not in fact contradictory - they are "
                      "measuring different things. The globe is a snapshot AFTER regeneration "
                      "has run; life_healed integrates over the window. Read together they "
                      "say the trial cost roughly 16 HP and it was regenerated before the "
                      "shutter. This is the single strongest argument in the bank for keeping "
                      "the panel counters rather than trusting the globe alone."),
        (24.42, 25.37, "+0.95 only - and the globe ends DOWN 13 at 269/282. Consistent: the "
                       "damage had not yet been regenerated when the shot was taken, so "
                       "life_healed had not yet counted it. The proxy lags the damage.")],
            start=1):
        add("%s/t%d" % (SET, n), "life_healed", "derived", round(hi_ - lo, 2), None, None,
            "HP", "derived", None, None, "%.2f -> %.2f" % (lo, hi_), "valid", note)

    # derived: capture latency
    for n in (1, 2, 3):
        add("%s/t%d" % (SET, n), "capture_latency", "derived", 0, None, None, "s", "derived",
            1.0, None, "play_time delta equals the hand-noted fight duration", "valid",
            "DERIVED: (after play_time - before play_time) - hand-noted fight_seconds = 0 for "
            "all three trials (5-5, 5-5, 4-4). Matt shot the after-frame immediately. That is "
            "why every round-3 dps_field reading is live, where round 2's 55 s latency "
            "produced a false 0.00. It ALSO means the panel does not independently corroborate "
            "the fight duration: both instruments measure the same capture interval and carry "
            "the same ~1 s/screenshot overhead the addendum describes.")

    cur.executemany(
        "INSERT INTO trial_measurement (trial_id,measure_key,measure_subkey,phase,value_num,"
        "value_num_hi,value_text,unit,read_method,uncertainty_abs,capture_id,verbatim,"
        "validity_flag,validity_note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", M)

    # ---- traces ----------------------------------------------------------
    PAIR = ("FINDING - the overlay renders BOTH channels simultaneously, per entity: a "
            "controller-state line above an '[entityId] Action State: X' line. Round 2 could "
            "only see them separately, which is why draft 6.3 had to keep trace_token and "
            "controller_state apart. Round 3 supplies live (controller, action) PAIRS with an "
            "entity id attached - direct evidence for the gap-9 mapping table, from the game "
            "itself rather than from inference.")
    T = []
    for n, (ent, cap) in enumerate([("68957", "t1s"), ("75289", "t2s"), ("77775", "t3s")], start=1):
        trial = "%s/t%d" % (SET, n)
        capid = "%s/%s" % (S3, cap)
        if n != 2:   # trial 2's controller line fell outside the crop; not attested
            T.append((S3, trial, n * 10, "anger-overlay", "monster-" + ent, "Pursue", "Pursue",
                      "identity", "in-roster-33", 0.0, None, None, None, capid,
                      "Pursue / [%s] Action State: Move. LIVE ATTESTATION of census row 4 "
                      "(Pursue, DATA-ATTESTED, 100%% of the bestiary, IN-both). Unlike round "
                      "2's Fidget, this token IS a census row and does confirm one. %s"
                      % (ent, PAIR)))
        T.append((S3, trial, n * 10 + 1, "logdata-console", "monster-" + ent, "Move", "Move",
                  "identity", "in-roster-33", 0.0, None, None, None, capid,
                  "[%s] Action State: Move. Note the rendering differs from round 2's console, "
                  "which printed 'Moving' for what is presumably the same thing; the on-screen "
                  "overlay prints 'Move', which matches 40-state-table row 18 exactly. The "
                  "round-2 near-miss may have been a console-formatting artefact rather than a "
                  "different token. %s" % (ent, PAIR)))
    T.append((S3, None, 90, "anger-overlay", "entity-17677", "LongIdle", None, "unmapped",
              "not-in-40-state-table", None, None, None, None, S3 + "/t1s",
              "LongIdle / [17677] Action State: Fidget. ABSENT from the 40-state "
              "ControllerMonster table. Session-scoped, not trial-scoped: this entity is "
              "screen-centred in every frame and is most likely the PLAYER, in which case it "
              "is not a ControllerMonster observation at all. Unattested either way, so it is "
              "banked unmapped rather than assigned."))
    T.append((S3, None, 91, "logdata-console", "entity-17677", "Fidget", None, "unmapped",
              "not-in-40-state-table", None, None, None, None, S3 + "/t1s",
              "[17677] Action State: Fidget. Same token round 2 saw, still absent from all 40 "
              "ControllerMonster rows, still unmapped. Round 3 adds one fact: it is paired "
              "with controller state 'LongIdle' on the same entity in the same frame."))
    cur.executemany(
        "INSERT INTO trial_trace (session_id,trial_id,seq,channel,entity_ref,trace_token,"
        "controller_state,mapping_status,vocab_status,t_offset_s,duration_s,duration_s_hi,"
        "duration_method,capture_id,verbatim_line) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", T)

    con.commit()

    # ---- verification + certification verdict ----------------------------
    print("=== M3: round-3 ingestion ===")
    for t in ("fixture_session", "capture", "fixture_character", "character_stat",
              "fixture_set", "fixture_set_constraint", "fixture_trial",
              "trial_measurement", "trial_trace"):
        tot = con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
        print("  %-24s total %4d" % (t, tot))
    print("  fk check: %s" %
          ("CLEAN" if not con.execute("PRAGMA foreign_key_check").fetchall() else "FAIL"))

    print("\n-- v_fixture_bank_certified --")
    for r in con.execute("SELECT trial_id, monster_display_name, monster_level, char_level, "
                         "contaminated FROM v_fixture_bank_certified ORDER BY trial_id"):
        print("   %-22s %-14s mLvl=%s pLvl=%s contaminated=%d" % r)

    print("\n-- ledger continuity within the certified set --")
    for r in con.execute("SELECT prev_ordinal,next_ordinal,measure_key,measure_subkey,"
                         "after_prev,before_next,gap_delta,verdict FROM v_ledger_continuity "
                         "WHERE fixture_set_id=? AND verdict='DISCONTINUOUS' "
                         "AND after_prev IS NOT NULL", (SET,)):
        print("   t%d->t%d %s%s: %g -> %g (%+g)" %
              (r[0], r[1], r[2], "[" + r[3].rsplit("/", 1)[-1] + "]" if r[3] else "",
               r[4], r[5], r[6]))

    print("\n-- Q47 instrument: spread over the CERTIFIED trials only --")
    q = """
      SELECT d.measure_key, d.measure_subkey, COUNT(*) n,
             MIN(d.delta), MAX(d.delta), AVG(d.delta),
             MAX(d.delta)-MIN(d.delta)
      FROM v_trial_delta d
      JOIN v_fixture_bank_certified c ON c.trial_id = d.trial_id
      WHERE d.delta IS NOT NULL
      GROUP BY d.measure_key, d.measure_subkey HAVING n > 1 ORDER BY 1"""
    for k, sub, n, lo, hi, mean, rng in con.execute(q):
        pct = (rng / mean * 100) if mean else float("nan")
        print("   %-18s%-26s n=%d  min=%g max=%g mean=%.3f range=%g (%.1f%% of mean)"
              % (k, "[" + sub.rsplit("/", 1)[-1] + "]" if sub else "", n, lo, hi, mean, rng, pct))
    print("\n   fight_seconds (hand, uncertainty +/-2 s each): %s" %
          [r[0] for r in con.execute(
              "SELECT m.value_num FROM trial_measurement m JOIN v_fixture_bank_certified c "
              "ON c.trial_id=m.trial_id WHERE m.measure_key='fight_seconds' ORDER BY m.trial_id")])
    print("   hp_cost_abs (hand):                            %s" %
          [r[0] for r in con.execute(
              "SELECT m.value_num FROM trial_measurement m JOIN v_fixture_bank_certified c "
              "ON c.trial_id=m.trial_id WHERE m.measure_key='hp_cost_abs' ORDER BY m.trial_id")])
    con.close()


if __name__ == "__main__":
    main()
