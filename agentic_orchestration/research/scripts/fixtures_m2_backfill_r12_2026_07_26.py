#!/usr/bin/env python3
"""
fixtures.db — MILESTONE 2: rounds 1 and 2 backfill (UNCERTIFIED rows)
=====================================================================
Backfills `research/curated/fixtures.db` per draft sec 7.2 exactly:
  - two-set split at the 5->6 level-up
  - contamination flag on the off-trial ledger discontinuity
  - session-scoped trace rows (trial_id IS NULL)
  - monster identity `assumed-unverified` on every set
  => none of these rows appear in v_fixture_bank_certified. That is the point (O-8).
Plus O-10: the round-1 playstats-panel.png re-read at FULL RESOLUTION and banked
as a `no-fight-baseline` trial, giving the bank a pre-trial baseline reading.

Agent: elrond. Commissioner: gandalf (GD program, gap 5).
Run AFTER fixtures_m1_landing_2026_07_26.py. Idempotent (deletes its own rows first).

PROVENANCE OF THE NUMBERS IN THIS FILE
--------------------------------------
Round-2 panel readings: draft sec 7.1, the full-resolution re-read that corrected
nine numbers in the probe-2 synthesis. gandalf independently re-cropped panels
(13)(16)(17) at full res before ACCEPT; every spot-check held.

Round-1 panel reading: read at this milestone, by me, from
live-probe-1/playstats-panel.png via
    sips -c 290 360 --cropOffset 45 1395   (+ 4x upscale)
    sips -c  34 520 --cropOffset 278 1400  (+ 4x upscale, skills line)
A FIRST, WIDER, LESS-UPSCALED CROP OF THE SAME PANEL MISREAD
`Max. level achieved` as 1; the tighter 4x crop reads 2. Only the 4x reading is
banked. This is the method law demonstrating itself on its first use of the day.

CORRECTION C10 (this milestone, raw evidence governs over the draft)
--------------------------------------------------------------------
Draft sec 7.2 states the AlertBeforePursue beat observations are "duration_s 2-3
(close) and ~3 (far)". `live-probe-1/GD-console-notes-matt-raw.md` carries NO
numeric beat for round 1 - it says verbatim "I haven't found enough instances of
AlertBeforePursue to yet determine if the beat is longer". Only round 2 carries a
number (~3 s, far). The round-1 trace row is therefore banked with duration_s
NULL. No number is invented to match the draft's prose.
"""

import hashlib
import os
import sqlite3

REPO = "/Users/admin/Games/reincarnated-collaboration"
DB = os.path.join(REPO, "agentic_orchestration/research/curated/fixtures.db")
KB = "agentic_orchestration/research/knowledge/gd"
P1 = os.path.join(REPO, KB, "live-probe-1")
P2 = os.path.join(REPO, KB, "live-probe-2")

S1 = "gd-live-2026-07-25-s1"
S2 = "gd-live-2026-07-25-s2"

FULLRES = "screenshot-fullres"
HAND_B = "hand-noted-band"
HAND_P = "hand-noted-point"

# --- round-2 panel ledger, draft sec 7.1 -----------------------------------
# capture -> (play_time_s, verbatim_playtime, deaths, kills, hpot, mpot, maxlvl,
#             dps, kick, weaponattack, life_healed)
R2 = {
    "s2/13": (8268, "137 min 48 sec", 0, 161, 0, 0, 5, 0.00, 1, 427, 2245.44),
    "s2/14": (8274, "137 min 54 sec", 0, 162, 0, 0, 5, 19.17, 1, 429, 2245.44),
    "s2/15": (8452, "140 min 52 sec", 0, 162, 0, 0, 6, 0.00, 1, 429, 2258.09),
    "s2/16": (8507, "141 min 47 sec", 0, 163, 0, 0, 6, 0.00, 1, 431, 2292.86),
    "s2/17": (8557, "142 min 37 sec", 0, 164, 0, 0, 6, 0.00, 1, 433, 2311.37),
    "s2/18": (8563, "142 min 43 sec", 0, 165, 0, 0, 6, 19.43, 1, 435, 2311.37),
}
WA = "records/skills/default/defaultweaponattack.dbr"
KICK = "records/skills/default/defaultkickattack.dbr"

CAPTURES = [
    # (capture_id, session, relpath, kind, label, notes)
    (S1 + "/playstats", S1, KB + "/live-probe-1/playstats-panel.png", "playstats-panel",
     "playstats-panel.png", "O-10 pre-trial baseline panel; re-read at full resolution 2026-07-26."),
    (S1 + "/spawn-attempt", S1, KB + "/live-probe-1/spawn-zombie01-attempt.png", "other",
     "spawn-zombie01-attempt.png", "game.Spawn argument-error evidence."),
    (S2 + "/13", S2, KB + "/live-probe-2/Screenshot (13).png", "playstats-panel",
     "Screenshot (13)", "T1 before."),
    (S2 + "/14", S2, KB + "/live-probe-2/Screenshot (14).png", "playstats-panel",
     "Screenshot (14)", "T1 after."),
    (S2 + "/15", S2, KB + "/live-probe-2/Screenshot (15).png", "playstats-panel",
     "Screenshot (15)", "T2 before. First shot showing level 6."),
    (S2 + "/16", S2, KB + "/live-probe-2/Screenshot (16).png", "playstats-panel",
     "Screenshot (16)", "T2 after. dps_field window expired."),
    (S2 + "/17", S2, KB + "/live-probe-2/Screenshot (17).png", "playstats-panel",
     "Screenshot (17)", "T3 before. HP globe reads 282/282."),
    (S2 + "/18", S2, KB + "/live-probe-2/Screenshot (18).png", "playstats-panel",
     "Screenshot (18)", "T3 after."),
    (S2 + "/console-fight", S2, KB + "/live-probe-2/colsole-fight-data-test.png", "console-log",
     "colsole-fight-data-test.png",
     "The killMonsters sweep test - a DIFFERENT event from the three trials. "
     "Source of the six LogData tokens, which is why those trace rows are session-scoped."),
    (S2 + "/spawned-zombie", S2, KB + "/live-probe-2/spawned_zombie.png", "world-view",
     "spawned_zombie.png",
     "Evidence that game.Spawn \"records/creatures/enemies/zombie_a01.dbr\" works. "
     "NOT tied by any note to any of the three trials - see O-5."),
]


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
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    # ---- idempotency: clear anything this script owns --------------------
    for sid in (S1, S2):
        cur.execute("DELETE FROM trial_trace WHERE session_id=?", (sid,))
        cur.execute(
            "DELETE FROM trial_measurement WHERE trial_id IN (SELECT t.trial_id "
            "FROM fixture_trial t JOIN fixture_set s USING(fixture_set_id) WHERE s.session_id=?)",
            (sid,))
        cur.execute(
            "DELETE FROM fixture_trial WHERE fixture_set_id IN "
            "(SELECT fixture_set_id FROM fixture_set WHERE session_id=?)", (sid,))
        cur.execute(
            "DELETE FROM fixture_set_constraint WHERE fixture_set_id IN "
            "(SELECT fixture_set_id FROM fixture_set WHERE session_id=?)", (sid,))
        cur.execute("DELETE FROM fixture_set WHERE session_id=?", (sid,))
        cur.execute("DELETE FROM character_stat WHERE character_id IN "
                    "(SELECT character_id FROM fixture_character WHERE session_id=?)", (sid,))
        cur.execute("DELETE FROM fixture_character WHERE session_id=?", (sid,))
        cur.execute("DELETE FROM capture WHERE session_id=?", (sid,))
        cur.execute("DELETE FROM fixture_session WHERE session_id=?", (sid,))

    # ---- sessions --------------------------------------------------------
    cur.execute(
        "INSERT INTO fixture_session (session_id,lane,session_date,operator,game_edition_pin,"
        "game_build_string,difficulty,container,save_identity,console_flags,rig_version,"
        "raw_notes_path,capture_dir,sim_config_ref,notes,adapter,schema_version) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (S1, "gd-live", "2026-07-25", "matt", None, None, None, "main-campaign", None,
         '{"PlayStats":true,"ShowAngerLevels":true,"WarpCursor":true}',
         "gandalf/pc-handoff/2026-07-25-gd-probe2-SIMPLE-checklist.md",
         KB + "/live-probe-1/GD-console-notes-matt-raw.md", KB + "/live-probe-1/",
         None,
         "Round 1: rig-verification sitting. NO trials fought. Its one panel screenshot is "
         "banked as a no-fight baseline per O-10. difficulty NOT CAPTURED. "
         "Continuity with s2 is NOT asserted: 22 min of play time separate the two panels and "
         "carry +145 kills / +418 weapon attacks / +2239 life healed, consistent with the "
         "killMonsters sweeps Matt describes, but nothing attests it.",
         "elrond/fixtures_m2_backfill_r12_2026_07_26.py", "fixtures-v0.1"))

    cur.execute(
        "INSERT INTO fixture_session (session_id,lane,session_date,operator,game_edition_pin,"
        "game_build_string,difficulty,container,save_identity,console_flags,rig_version,"
        "raw_notes_path,capture_dir,sim_config_ref,notes,adapter,schema_version) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (S2, "gd-live", "2026-07-25", "matt", None, None, None, "main-campaign", None,
         '{"LogData":true,"PlayStats":true}',
         "gandalf/pc-handoff/2026-07-25-gd-probe3-SIMPLE-v2.md",
         KB + "/live-probe-2/GD-console-notes-v2-raw.md", KB + "/live-probe-2/",
         None,
         "Round 2: three trials. difficulty NOT CAPTURED - materially changes monster stats. "
         "container 'main-campaign' is INFERRED from the quest tracker; confidence low. "
         "The player levelled 5->6 mid-sitting, so the trials split across two fixture_sets.",
         "elrond/fixtures_m2_backfill_r12_2026_07_26.py", "fixtures-v0.1"))

    # ---- captures --------------------------------------------------------
    for cid, sid, rel, kind, label, notes in CAPTURES:
        ap = os.path.join(REPO, rel)
        w, h = png_dims(ap)
        cur.execute(
            "INSERT INTO capture (capture_id,session_id,path,kind,label,sha256,mtime_utc,"
            "pixel_w,pixel_h,notes) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (cid, sid, rel, kind, label, sha256_file(ap), None, w, h, notes))

    # ---- characters ------------------------------------------------------
    cur.execute(
        "INSERT INTO fixture_character (character_id,session_id,snapshot_ordinal,"
        "valid_from_playtime_s,char_level,hp_max,completeness,capture_id,notes) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (S1 + "/c1", S1, 1, 6927, 2, None, "level-only", S1 + "/playstats",
         "Level 2 read from 'Max. level achieved' at 4x crop. A wider, less-upscaled crop of "
         "the same pixels misread it as 1; that reading is discarded, not banked."))
    cur.execute(
        "INSERT INTO fixture_character (character_id,session_id,snapshot_ordinal,"
        "valid_from_playtime_s,char_level,hp_max,completeness,capture_id,notes) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (S2 + "/c1", S2, 1, 8268, 5, None, "level-only", S2 + "/13",
         "In force for trial 1 only. Draft correction C2: the probe-2 synthesis said level 6 "
         "throughout; shots (13)/(14) read 5."))
    cur.execute(
        "INSERT INTO fixture_character (character_id,session_id,snapshot_ordinal,"
        "valid_from_playtime_s,char_level,hp_max,completeness,capture_id,notes) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (S2 + "/c2", S2, 2, 8452, 6, 282.0, "level-and-hp-only", S2 + "/17",
         "hp_max 282 read from the HP globe in shot (17). OA/DA/weapon/resists all unknown - "
         "no character sheet exists for this sitting. That gap is what O-4 closes."))

    # ---- sets ------------------------------------------------------------
    ID_EVIDENCE = (
        "Matt's raw notes record game.Spawn \"records/creatures/enemies/zombie_a01.dbr\" under "
        "a SEPARATE heading from the trials. No note, and no nameplate in any of the six panel "
        "screenshots, states which monster each trial fought. Identifying these trials with "
        "zombie_a01 is an assumption, not an attestation.")

    sets = [
        (S1 + "/baseline", S1, S1 + "/c1", None, 1, 0,
         "O-10 pre-trial baseline holder. No fight occurred; this set exists only to hang the "
         "round-1 no-fight-baseline panel reading on. Not a fixture in the measurement sense.",
         None),
        ("L0-gd-s2-set1", S2, S2 + "/c1", None, 1, 1,
         "Trial 1, fought at character level 5. Split from set2 by the level-up (draft sec 8.2).",
         "wilderness - minimap visibly differs from set 2; area not named in any note"),
        ("L0-gd-s2-set2", S2, S2 + "/c2", None, 2, 2,
         "Trials 2-3, fought at character level 6.",
         "Devil's Crossing vicinity (inferred from quest tracker; not attested)"),
    ]
    for sid_, sess, chid, mrec, intended, actual, purpose, area in sets:
        cur.execute(
            "INSERT INTO fixture_set (fixture_set_id,session_id,character_id,ladder_rung,"
            "monster_record,monster_display_name,monster_identity_method,"
            "monster_identity_evidence,monster_level,monster_level_method,monster_source,"
            "pack_size,engagement_mode,area_name,intended_n,actual_n,purpose) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (sid_, sess, chid, "L0", mrec, None, "assumed-unverified", ID_EVIDENCE,
             None, "unknown", "unknown", None, "unknown", area, intended, actual, purpose))

    # ---- constraints -----------------------------------------------------
    common = [
        ("single-monster", "unknown", "no world-view screenshot at engagement"),
        ("melee-only", "unknown", "monster identity unattested"),
        ("no-pack", "unknown", "not observed"),
        ("no-flee", "unknown", "not observed"),
        ("fight-to-death", "held", "kills counter advances +1 per trial"),
        ("pre-aggroed", "unknown", "not noted"),
        ("no-potions", "held", "both potion counters static at 0 across all six panels"),
        ("no-player-death", "held", "deaths counter static at 0 across all six panels"),
        ("no-CC-test-character", "expired",
         "Retired constraint, expired 2026-07-25. Carried per O-9: an expired constraint is "
         "interpretive context for the rows fought under it, not noise to be deleted."),
    ]
    for setid in ("L0-gd-s2-set1", "L0-gd-s2-set2"):
        for k, held, ev in common:
            cur.execute("INSERT INTO fixture_set_constraint VALUES (?,?,?,?)",
                        (setid, k, held, ev))
    cur.execute("INSERT INTO fixture_set_constraint VALUES (?,?,?,?)",
                ("L0-gd-s2-set2", "no-off-trial-activity", "violated",
                 "Between T2-after and T3-before: kills 163->164, defaultweaponattack 431->433, "
                 "life_healed 2292.86->2311.37. One kill, two attacks and 18.51 HP of healing "
                 "happened outside any trial. Visible ONLY because before(n+1) and after(n) are "
                 "both stored as readings (draft sec 8.1)."))
    for k, held, ev in [("single-monster", "unknown", "no fight occurred"),
                        ("no-potions", "held", "potion counters read 0"),
                        ("no-player-death", "held", "deaths counter reads 0")]:
        cur.execute("INSERT INTO fixture_set_constraint VALUES (?,?,?,?)",
                    (S1 + "/baseline", k, held, ev))

    # ---- trials ----------------------------------------------------------
    trials = [
        (S1 + "/baseline/t0", S1 + "/baseline", 0, "no-fight-baseline", 6927, 6927,
         S1 + "/playstats", None, 0, None,
         "O-10. A single panel reading with no fight. Banked so the bank has a pre-trial "
         "baseline of the same counters. outcome='no-fight-baseline' (extension E2) keeps it "
         "out of every delta and spread view."),
        ("L0-gd-s2-set1/t1", "L0-gd-s2-set1", 1, "monster-killed", 8268, 8274,
         S2 + "/13", S2 + "/14", 0, None, None),
        ("L0-gd-s2-set2/t1", "L0-gd-s2-set2", 1, "monster-killed", 8452, 8507,
         S2 + "/15", S2 + "/16", 0, None,
         "55 s between the before and after shots for a 1-2 s fight. The dps_field window "
         "expired inside that gap; see the window-expired flag on the after reading."),
        ("L0-gd-s2-set2/t2", "L0-gd-s2-set2", 2, "monster-killed", 8557, 8563,
         S2 + "/17", S2 + "/18", 1, "ledger-discontinuity",
         "Contaminated UPSTREAM: the counters advanced between this trial's before-shot and the "
         "previous trial's after-shot. The trial's own deltas are clean (+1 kill, +2 attacks); "
         "what is not clean is the interval preceding it."),
    ]
    for row in trials:
        cur.execute(
            "INSERT INTO fixture_trial (trial_id,fixture_set_id,trial_ordinal,lane,outcome,"
            "t_start_playtime_s,t_end_playtime_s,before_capture_id,after_capture_id,"
            "contaminated,contamination_reason,notes) VALUES (?,?,?,'gd-live',?,?,?,?,?,?,?,?)",
            row)

    # ---- measurements ----------------------------------------------------
    M = []

    def add(trial, key, phase, num, hi, text, unit, rm, unc, cap, verb,
            flag="valid", note=None, sub=""):
        M.append((trial, key, sub, phase, num, hi, text, unit, rm, unc, cap, verb, flag, note))

    # round-1 baseline panel (this milestone's own full-res read)
    B = S1 + "/baseline/t0"
    BC = S1 + "/playstats"
    for key, num, verb, unit in [
            ("play_time", 6927, "115 min 27 sec", "s"),
            ("total_score", 0, "0", "pts"),
            ("deaths", 0, "0", "count"),
            ("kills", 16, "16", "count"),
            ("health_potions_used", 0, "0", "count"),
            ("mana_potions_used", 0, "0", "count"),
            ("max_level_achieved", 2, "2", "level"),
            ("dps_field", 0.00, "0.00", "dmg/s"),
            ("life_healed", 6.34, "6.34", "HP"),
            ("shield_block_chance", 15.00, "15.00", "pct")]:
        add(B, key, "before", num, None, None, unit, FULLRES, 0, BC, verb)
    add(B, "skill_use_count", "before", 9, None, None, "count", FULLRES, 0, BC,
        "records/skills/default/defaultweaponattack.dbr : 9", sub=WA)
    # the kick line is ABSENT from the round-1 panel, and absence is a reading
    add(B, "skill_use_count", "before", None, None, None, "count", "absent", None, BC,
        None, "valid",
        "The defaultkickattack line does not appear on the round-1 panel at all. GD's "
        "PlayStats lists only skills that have been used at least once, so absence here is "
        "evidence the kick had never fired by 115 min - consistent with its counter reading a "
        "static 1 throughout round 2.", KICK)

    # round-2 trials
    r2map = [("L0-gd-s2-set1/t1", "s2/13", "s2/14", S2 + "/13", S2 + "/14"),
             ("L0-gd-s2-set2/t1", "s2/15", "s2/16", S2 + "/15", S2 + "/16"),
             ("L0-gd-s2-set2/t2", "s2/17", "s2/18", S2 + "/17", S2 + "/18")]
    for trial, kb_, ka_, cb, ca in r2map:
        for phase, k, cap in (("before", kb_, cb), ("after", ka_, ca)):
            (pt, ptv, deaths, kills, hpot, mpot, mlvl, dps, kick, wa, healed) = R2[k]
            add(trial, "play_time", phase, pt, None, None, "s", FULLRES, 0, cap, ptv)
            add(trial, "deaths", phase, deaths, None, None, "count", FULLRES, 0, cap, str(deaths))
            add(trial, "kills", phase, kills, None, None, "count", FULLRES, 0, cap, str(kills))
            add(trial, "health_potions_used", phase, hpot, None, None, "count", FULLRES, 0, cap, str(hpot))
            add(trial, "mana_potions_used", phase, mpot, None, None, "count", FULLRES, 0, cap, str(mpot))
            add(trial, "max_level_achieved", phase, mlvl, None, None, "level", FULLRES, 0, cap, str(mlvl))
            expired = (trial == "L0-gd-s2-set2/t1" and phase == "after")
            add(trial, "dps_field", phase, dps, None, None, "dmg/s", FULLRES, 0, cap,
                "%.2f" % dps,
                "window-expired" if expired else "valid",
                ("Reads 0.00 after a kill that the kills counter confirms happened. The meter "
                 "reports over a recent window which had lapsed by the time this shot was taken "
                 "(~53 s after the fight). This is a FALSE ZERO, not an observation of zero "
                 "damage. O-6 keeps dps_field out of the G3 comparable set for exactly this "
                 "reason.") if expired else
                ("Pre-fight idle reading; the window is genuinely empty here." if phase == "before" else None))
            add(trial, "life_healed", phase, healed, None, None, "HP", FULLRES, 0, cap, "%.2f" % healed)
            add(trial, "skill_use_count", phase, wa, None, None, "count", FULLRES, 0, cap,
                ": %d" % wa, sub=WA)
            add(trial, "skill_use_count", phase, kick, None, None, "count", FULLRES, 0, cap,
                ": %d" % kick, sub=KICK)

    # HP globe, shot (17) only
    add("L0-gd-s2-set2/t2", "hp_current", "before", 282, None, None, "HP", FULLRES, 0,
        S2 + "/17", "282/282")
    add("L0-gd-s2-set2/t2", "hp_max", "before", 282, None, None, "HP", FULLRES, 0,
        S2 + "/17", "282/282")

    # hand notes
    hand = [("L0-gd-s2-set1/t1", 1, 2, 0, 0, "Trial 1: 1-2s, HP cost 0", "none"),
            ("L0-gd-s2-set2/t1", 1, 2, 15, 20, "Trial 2: 1-2s, HP cost 15-20", None),
            ("L0-gd-s2-set2/t2", 1, 2, 0, 0, "Trial 3: 1-2s, HP cost 0", "none")]
    for trial, fs_lo, fs_hi, hp_lo, hp_hi, verb, band in hand:
        add(trial, "fight_seconds", "during", fs_lo, fs_hi, None, "s", HAND_B, 0.5, None, verb)
        add(trial, "hp_cost_abs", "during", hp_lo, hp_hi, None, "HP",
            HAND_B if hp_hi != hp_lo else HAND_P, None, None, verb)
        if band:
            add(trial, "hp_cost_band", "during", None, None, band, None, HAND_P, None, None, verb)

    # O-7: the panel's damage-taken proxy DISAGREES with Matt's hand note on set2/t1.
    # Both stand. Neither is reconciled.
    add("L0-gd-s2-set2/t1", "life_healed", "derived", 34.77, None, None, "HP", "derived",
        None, None, "2258.09 -> 2292.86", "valid",
        "O-7: the panel delta (+34.77 HP healed, ~12.3% of the 282 pool) and Matt's hand-noted "
        "HP cost of 15-20 (~5-7%) disagree by roughly 2x. BOTH ARE BANKED. Neither is adjusted "
        "to the other. The panel figure spans 55 s and therefore includes post-fight regen; the "
        "hand note is a glance at the globe. The schema's job here is to preserve the "
        "disagreement, not to resolve it.")

    # capture_latency, derived - the condition on which dps validity depends (draft sec 8.4)
    for trial, gap in (("L0-gd-s2-set1/t1", 6), ("L0-gd-s2-set2/t1", 55), ("L0-gd-s2-set2/t2", 6)):
        add(trial, "capture_latency", "derived", gap - 2, None, None, "s", "derived", 1.0, None,
            "play_time delta %d s minus hand-noted fight upper bound 2 s" % gap, "valid",
            "DERIVED, not observed: (after play_time - before play_time) - fight_seconds_hi. "
            "Explains the dps_field validity pattern exactly - the two trials with ~4 s latency "
            "carry live DPS readings; the one with ~53 s reads a false 0.00.")

    cur.executemany(
        "INSERT INTO trial_measurement (trial_id,measure_key,measure_subkey,phase,value_num,"
        "value_num_hi,value_text,unit,read_method,uncertainty_abs,capture_id,verbatim,"
        "validity_flag,validity_note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", M)

    # ---- traces (ALL session-scoped: trial_id IS NULL) -------------------
    T = []

    def tr(sid, seq, ch, ent, tok, cs, ms, vs, dur, dur_hi, dm, cap, line):
        T.append((sid, None, seq, ch, ent, tok, cs, ms, vs, None, dur, dur_hi, dm, cap, line))

    tr(S1, 1, "anger-overlay", "zombie", "AlertBeforePursue", "AlertBeforePursue",
       "identity", "in-roster-33", None, None, None, None,
       "The word: AlertBeforePursue (confirmed). Beat length NOT quantified in round 1 - Matt: "
       "\"I haven't found enough instances of AlertBeforePursue to yet determine if the beat is "
       "longer when it spots me from further away\". Correction C10: the draft sec 7.2 prose "
       "attributes a 2-3 s close-range beat to round 1; the raw notes carry no such number.")
    tr(S1, 2, "anger-overlay", "zombie-buried", "Startup", "Startup", "identity",
       "in-roster-33", None, None, None, None,
       "Zombies buried or lying on the ground displayed Startup while they rose, before they "
       "attacked. Matt: \"Startup is very common\".")
    tr(S1, 3, "anger-overlay", "boss-monster", "followtheleader", "FollowLeader",
       "case-normalized", "in-roster-33", None, None, None, None,
       "\"I did also see followtheleader when I fought a boss monster.\"")
    tr(S2, 4, "anger-overlay", "zombie", "AlertBeforePursue", "AlertBeforePursue",
       "identity", "in-roster-33", 3.0, None, HAND_B, None,
       "Zombie Yell / Beat length: ~3s - Spotted you from: far. The ONLY numeric beat in the "
       "record. Range-dependence remains untested: there is no matched close-range measurement.")
    for seq, tok, cs, ms, vs, note in [
        (5, "Idle", "Idle", "identity", "in-roster-33", None),
        (6, "Attack", "Attack", "identity", "in-roster-33", None),
        (7, "Dying", "Dying", "identity", "in-roster-33", None),
        (8, "Moving", "Move", "inferred-mapping", "in-roster-33",
         "NEAR-MISS, not identity: the 40-state ControllerMonster table has 'Move', not "
         "'Moving'. The mapping is an inference."),
        (9, "Fidget", None, "unmapped", "not-in-40-state-table",
         "ABSENT from all 40 ControllerMonster rows. Plausibly the animation-layer name behind "
         "'Emote' (row 39) - INFERENCE, NOT BANKED. The probe-2 synthesis banked this token as "
         "census confirmation #4; that claim was withdrawn (O-3). Fidget cannot confirm a census "
         "row it is not in."),
        (10, "Flying", None, "unmapped", "not-in-40-state-table",
         "ABSENT from all 40 ControllerMonster rows. Unexplained."),
    ]:
        tr(S2, seq, "logdata-console", "unattributed", tok, cs, ms, vs, None, None, None,
           S2 + "/console-fight",
           (note + " " if note else "") +
           "SESSION-SCOPED (trial_id NULL): these tokens come from colsole-fight-data-test.png, "
           "the killMonsters sweep - a different event from the three trials. Attributing them "
           "to a trial would be a fabrication. The LogData channel also appears to emit from an "
           "animation/actor-state layer, NOT from ControllerMonster (draft sec 6.3) - which is "
           "why trace_token and controller_state are two columns.")

    cur.executemany(
        "INSERT INTO trial_trace (session_id,trial_id,seq,channel,entity_ref,trace_token,"
        "controller_state,mapping_status,vocab_status,t_offset_s,duration_s,duration_s_hi,"
        "duration_method,capture_id,verbatim_line) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", T)

    con.commit()

    # ---- verification ----------------------------------------------------
    print("=== M2 backfill: rounds 1-2 ===")
    for t in ("fixture_session", "capture", "fixture_character", "fixture_set",
              "fixture_set_constraint", "fixture_trial", "trial_measurement", "trial_trace"):
        print("  %-24s %d" % (t, con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]))
    print("\nforeign_key_check: %s" %
          ("CLEAN" if not con.execute("PRAGMA foreign_key_check").fetchall() else "FAIL"))

    print("\n-- v_fixture_bank_certified (MUST be empty: every set is assumed-unverified) --")
    rows = con.execute("SELECT trial_id FROM v_fixture_bank_certified").fetchall()
    print("  rows: %d  %s" % (len(rows), "OK" if not rows else "UNEXPECTED: %s" % rows))

    print("\n-- v_ledger_continuity (the off-trial-activity detector) --")
    for r in con.execute(
            "SELECT fixture_set_id,prev_ordinal,next_ordinal,measure_key,measure_subkey,"
            "after_prev,before_next,gap_delta,verdict FROM v_ledger_continuity "
            "WHERE verdict='DISCONTINUOUS'"):
        print("  %s t%d->t%d %s%s: %s -> %s (gap %+g)  %s" %
              (r[0], r[1], r[2], r[3],
               "[" + r[4].rsplit("/", 1)[-1] + "]" if r[4] else "", r[5], r[6], r[7], r[8]))

    print("\n-- v_set_spread on kills (N-trial spread; Q47's instrument) --")
    for r in con.execute("SELECT fixture_set_id,n,min_delta,max_delta,mean_delta,range_delta,"
                         "stdev_delta FROM v_set_spread WHERE measure_key='kills'"):
        print("  %-16s n=%d min=%g max=%g mean=%g range=%g stdev=%s" %
              (r[0], r[1], r[2], r[3], r[4], r[5],
               "n/a" if r[6] is None else "%.3f" % r[6]))
    con.close()


if __name__ == "__main__":
    main()
