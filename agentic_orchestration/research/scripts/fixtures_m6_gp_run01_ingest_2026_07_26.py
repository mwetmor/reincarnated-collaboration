#!/usr/bin/env python3
"""
fixtures.db - MILESTONE 6: GP run 01 ingest (the first real general-play recorded run)
======================================================================================
Artifacts: /Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/
  recorded_videos/play_test_2026-07-26.mp4   1920x1080 h264 60/1 CFR  6816.516667 s  15.4 Mbps
  recorded_videos/smoke_test_2026-07-26.mp4  26.65 s gate check
  screenshots/Screenshot (40..352).png       313 PNG, contiguous, 1920x1080

Agent: elrond. Commissioner: gandalf (protocol sec 5 data contract).
Run AFTER fixtures_m5_v0_3_schema_2026_07_26.py. Idempotent.

WHAT THIS MILESTONE DOES AND DELIBERATELY DOES NOT DO
-----------------------------------------------------
DOES:  the SPINE. 315 capture rows with sha256 + mtime + video-timeline placement;
       the clock anchors and the piecewise clock map; the segmentation breaks; the
       session controls; every panel digit that has actually been READ by a human at
       full resolution (gandalf's verification, sec 2 / 3 / 6 / 6b).
DOES NOT: invent a single number. No fixture_character, no fixture_set, no
       fixture_trial rows are created. Those require monster identity and character
       sheets, which require the OCR pass galadriel owns. A fixture_set with a
       hypothesised monster would poison exactly the oracle this bank exists to be.

THE ONE THING THAT MUST NOT BE SMOOTHED OVER
--------------------------------------------
play_time_ms is the join key, and it is KNOWN for 4 of 313 screenshots.
pts_ms (video offset) is known for all 315 artifacts by mtime arithmetic - exact,
cheap, proven. But pts_ms is the CAMERA clock. Converting it to play_time via the
clock map carries up to +/-19 s of unallocated frozen loading time INSIDE a segment,
and an engagement lasts ~5 s. So the map cannot substitute for a panel read at
engagement resolution, and this script leaves play_time_ms NULL wherever it was not
read. `play_time_method='absent'` is the honest marker. Filling it by interpolation
would be a silent transformation of the join key itself.

THE OTHER THING THAT MUST NOT BE SMOOTHED OVER
-----------------------------------------------
The run's counters do not start at zero. At pts=14.5 the panel already reads kills=2,
defaultweaponattack=8, life_healed=16.33 - carried in from the sec 2.0 smoke gate. Every
bookend delta must subtract that baseline: kills 880 (not 882), total skill uses 684 (not
692), life_healed 12451.73 (not 12468.06). Two frames were read to establish it (run @
pts 14.5, smoke @ t 25); both are banked, and both sessions exist as rows.

BLOCKED BY CONSTRUCTION
-----------------------
`attacks_per_kill` is INGEST-BLOCKED in measure_dict (M5) pending the sec 6b
swings-vs-activations verdict. The raw per-skill counts below are OBSERVED values and
are ingested; nothing derived from them is. The block is a trigger, not a promise.
"""

import datetime
import os
import re
import sqlite3
import sys

REPO = "/Users/admin/Games/reincarnated-collaboration"
DB = os.path.join(REPO, "agentic_orchestration/research/curated/fixtures.db")
SHARE = "//mwetmor@reincarnated-pi.local/reincarnated"
ROOT = "share:reincarnated"
BASE = "visual-artifacts/GD-matt-test/play-test-v1"
ABS = "/Volumes/reincarnated/" + BASE

S = "GP-gd-2026-07-26-s1"
SM = "GP-gd-2026-07-26-smoke"      # the sec 2.0 smoke gate: a SEPARATE session by A6
SM_START = 1785095669.0 - 26.65   # smoke video mtime - duration
VSTART = 1785096216.5           # gandalf verification sec 2, PROVEN at 4 independent points
VDUR = 6816.516667
BURST_GAP_S = 8.0               # capture-burst grouping threshold (stated, not hidden)
EPOCH_MIN_N = 10                # epoch-boundary CANDIDATE rule: >=10 shots ...
EPOCH_MIN_DUR = 25.0            # ... spanning >=25 s. A hypothesis, not an observation.

# Precomputed by gp_run01_precompute_2026_07_26.sh and COMMITTED - a rebuild must not
# have to re-read 13.2 GB over SMB at ~3.5 MB/s.
MAN = os.path.join(REPO, "agentic_orchestration/research/curated/gp-run01-manifest")
SHA_PNG = os.path.join(MAN, "sha256-png.txt")
SHA_MP4 = os.path.join(MAN, "sha256-mp4.txt")
STAT = os.path.join(MAN, "stat-png.txt")     # stills AND both videos
DIM_PNG = os.path.join(MAN, "dim-png.txt")

VERIF = "gandalf/notes/2026-07-26-gd-playtest-v1-artifact-verification.md"
PROTO = "gandalf/notes/2026-07-26-gd-general-play-run-protocol.md"

# ---------------------------------------------------------------------------
# CLOCK ANCHORS - (pts_s, play_time_s, source, capture_label, co_agreeing, evidence)
# Every one of these is a HUMAN read of a full-resolution crop. None is OCR.
# ---------------------------------------------------------------------------
ANCHORS = [
    (14.5,   371,  "screenshot-panel",  "Screenshot (40)",  "play_time",
     VERIF + " sec 2 table row 40 - EXACT match screenshot vs video frame"),
    (300.0,  653,  "video-frame-panel", None, "play_time", VERIF + " sec 3 divergence table"),
    (900.0,  1252, "video-frame-panel", None, "play_time", VERIF + " sec 3 divergence table"),
    (1500.0, 1833, "video-frame-panel", None, "play_time", VERIF + " sec 3 divergence table"),
    (3259.0, 3576, "screenshot-panel",  "Screenshot (200)",
     "play_time,kills,deaths,max_level_achieved",
     VERIF + " sec 2 - four fields co-agree screenshot vs video frame"),
    (3289.0, 3606, "video-frame-panel", None, "play_time",
     VERIF + " sec 2 seek-accuracy check: +30 s seek advanced the ledger by exactly +30 s"),
    (3349.0, 3665, "video-frame-panel", None, "play_time",
     VERIF + " sec 2 seek-accuracy check; ALSO the observed zone transition interval"),
    (5071.5, 5372, "screenshot-panel",  "Screenshot (280)", "play_time",
     VERIF + " sec 2 - consistent on the fitted curve"),
    (5600.0, 5892, "video-frame-panel", None, "play_time", VERIF + " sec 3 divergence table"),
    (6805.5, 7088, "screenshot-panel",  "Screenshot (352)",
     "play_time,kills,deaths,max_level_achieved",
     VERIF + " sec 2 - four fields co-agree; END BLOCK"),
]

# ---------------------------------------------------------------------------
# ATTESTED PANEL READS -> session_ledger
# (capture_label_or_None, pts_s, play_time_s, measure_key, subkey, num, verbatim,
#  read_method, cross_check_status, cross_check_fields, occluded, note)
# ---------------------------------------------------------------------------
SKILLS_352 = [
    ("records/skills/default/defaultkickattack.dbr", 19),
    ("records/skills/default/defaultweaponattack.dbr", 74),
    ("records/skills/playerclass10/onslaught.dbr", 54),
    ("records/skills/playerclass10/werewolf1.dbr", 12),
    ("records/skills/playerclass10/werewolf1_skill01_claws.dbr", 358),
    ("records/skills/playerclass10/werewolf1_skill02_charge.dbr", 175),
]
CO4 = "play_time,kills,deaths,max_level_achieved"
UNITS = dict(play_time="s", kills="count", deaths="count", life_healed="HP",
             shield_block_chance="pct", health_potions_used="count",
             mana_potions_used="count", total_score="pts", dps_field="dmg/s",
             max_level_achieved="level", skill_use_count="count")


# ---------------------------------------------------------------------------
# THE RUN BASELINE - read by elrond from the video head frame at pts=14.5, and the
# same panel at the END of the smoke clip. Tight crops (430x90 / 520x80 native) at
# 1.6x, per the D-1 geometry law.
#
# WHY THIS MATTERS MORE THAN ANYTHING ELSE IN THIS FILE
# ------------------------------------------------------
# The run's counters DO NOT START AT ZERO. At pts=14.5 the panel already reads
# kills=2, defaultweaponattack=8, life_healed=16.33 - the sec 2.0 smoke gate's two
# monsters, carried in. Every bookend delta must subtract this baseline:
#
#   kills                882 -> RUN DELTA 880       (gandalf sec 6/6b used 882)
#   total skill uses     692 -> RUN DELTA 684       (gandalf sec 6b used 692)
#   defaultweaponattack   74 -> RUN DELTA  66
#   life_healed     12468.06 -> RUN DELTA 12451.73  (gandalf sec 8 used 12468.06)
#
# It also settles an A6 question. `kills` reads 2 at the smoke's END and 2 at the
# run's START, so kills is SAVE-cumulative as A6 declares. But skill_use_count (8) and
# life_healed (16.33) ALSO carried across that boundary, and A6 classifies BOTH as
# SESSION-scoped and resettable by a return to the main menu. Either the smoke and the
# run were one continuous session, or the A6 classification is wrong. Unresolved here;
# flagged, and either way the baseline is non-zero.
#
# AND a live D-1 demonstration, mine: a 460x290 crop at 2.5x read `Number of kills: 0`.
# The same pixels at 430x90 / 1.6x read `2`. Legible and wrong, exactly as gandalf
# warned. Only the tight reads are banked.
# ---------------------------------------------------------------------------
D1 = ("Read from a TIGHT crop at modest upscale per gandalf D-1 (sips -c 90 430 "
      "--cropOffset 74 1440, then 1.6x). A 460x290 crop of the SAME pixels at 2.5x "
      "read this counter WRONG - D-1 reproduced live during this ingest.")

BASELINE = [  # (measure_key, subkey, value, verbatim, occluded, note)
    ("play_time", "", 371.0, "6 min 11 sec", 0,
     "Independently reproduces gandalf's sec 2 anchor for Screenshot (40) EXACTLY, from "
     "the video side. " + D1),
    ("total_score", "", 0.0, "0", 0, "D-3 dead field, confirmed at t0 as well as at the end."),
    ("deaths", "", 0.0, "0", 0, D1),
    ("kills", "", 2.0, "2", 0,
     "NON-ZERO BASELINE. The sec 2.0 smoke gate's two monsters. The run's kill delta is "
     "882 - 2 = 880. " + D1),
    ("health_potions_used", "", 0.0, "0", 0, "Zero-potion control confirmed at t0."),
    ("mana_potions_used", "", 0.0, "0", 0, "Zero-potion control confirmed at t0."),
    ("max_level_achieved", "", 1.0, "1", 0,
     "Character starts the run at level 1; ends at 12. Eleven level-ups, each an epoch "
     "boundary by sec 2.3."),
    ("dps_field", "", 0.0, "0.00", 0, "D-3 dead field, confirmed at t0."),
    ("skill_use_count", "records/skills/default/defaultweaponattack.dbr", 8.0, "8", 0,
     "NON-ZERO BASELINE, and the only skill listed at t0. Run delta 74 - 8 = 66. Total "
     "skill-use delta for the run is 692 - 8 = 684, not 692."),
    ("life_healed", "", 16.33, "16.33", 0,
     "NON-ZERO BASELINE. The run's endogenous healing is 12468.06 - 16.33 = 12451.73."),
    ("shield_block_chance", "", 15.00, "15.00", 1,
     "15.00 at t0 vs 18.00 at the end - it moved with gear/level, which is correct for an "
     "'invariant-within-character' measure across 11 character epochs. Partially overlapped "
     "by the quest tracker (D-2) but legible."),
]

SMOKE_LEDGER = [  # same panel at the smoke clip's t=25 s
    ("play_time", "", 358.0, "5 min 58 sec", 0, ""),
    ("total_score", "", 0.0, "0", 0, ""),
    ("deaths", "", 0.0, "0", 0, ""),
    ("kills", "", 2.0, "2", 0,
     "The sec 2.0 gate item 5 ('Kill 2 monsters') WAS performed. Identical to the run's "
     "t0 value, which is what makes kills SAVE-cumulative per A6."),
    ("max_level_achieved", "", 1.0, "1", 0, ""),
    ("skill_use_count", "records/skills/default/defaultweaponattack.dbr", 8.0, "8", 0,
     "Identical to the run's t0 value. A6 declares skill_use_count SESSION-scoped and "
     "resettable by a menu return; it did not reset across this boundary."),
    ("life_healed", "", 16.33, "16.33", 0,
     "Identical to the run's t0 value. Same A6 question as skill_use_count."),
    ("shield_block_chance", "", 15.00, "15.00", 0, ""),
]


def ledger_rows():
    R = []
    # -- run baseline, pts=14.5 (video-frame-human) -------------------------
    for mk, sub, v, vb, occ, note in BASELINE:
        R.append((None, 14.5, 371, mk, sub, v, vb, "video-frame-human",
                  "co-agree" if mk == "play_time" else "single-field-only",
                  "play_time(Screenshot 40)" if mk == "play_time" else mk, occ,
                  "RUN BASELINE t0. " + note))
    # -- Screenshot (40): START BLOCK ---------------------------------------
    R.append(("Screenshot (40)", 14.5, 371, "play_time", "", 371.0, "6 min 11 sec",
              "screenshot-fullres", "co-agree", "play_time(video-frame)", 0,
              VERIF + " sec 2: EXACT agreement with the video frame at the same offset."))
    # -- Screenshot (200) ---------------------------------------------------
    for k, v, vb in (("play_time", 3576.0, "59 min 36 sec"), ("kills", 271.0, "271"),
                     ("deaths", 1.0, "1"), ("max_level_achieved", 8.0, "8")):
        R.append(("Screenshot (200)", 3259.5, 3576, k, "", v, vb,
                  "screenshot-fullres", "co-agree", CO4, 0,
                  VERIF + " sec 2: four fields co-agree, screenshot vs video frame."))
    # -- Screenshot (280) ---------------------------------------------------
    R.append(("Screenshot (280)", 5071.5, 5372, "play_time", "", 5372.0, "89 min 32 sec",
              "screenshot-fullres", "single-field-only", "play_time", 0,
              VERIF + " sec 2: consistent with the fitted curve; not independently co-checked."))
    # -- Screenshot (352): END BLOCK, the full panel ------------------------
    end = [("play_time", "", 7088.0, "118 min 8 sec"),
           ("kills", "", 882.0, "882"),
           ("deaths", "", 2.0, "2"),
           ("max_level_achieved", "", 12.0, "12"),
           ("life_healed", "", 12468.06, "12468.06"),
           ("shield_block_chance", "", 18.00, "18.00"),
           ("health_potions_used", "", 0.0, "0"),
           ("mana_potions_used", "", 0.0, "0"),
           ("total_score", "", 0.0, "0"),
           ("dps_field", "", 0.00, "0.00")]
    for sk, cnt in SKILLS_352:
        end.append(("skill_use_count", sk, float(cnt), str(cnt)))
    for k, sub, v, vb in end:
        cc, ccf = ("co-agree", CO4) if k in ("play_time", "kills", "deaths",
                                             "max_level_achieved") else ("single-field-only", k)
        note = VERIF + " sec 6b: complete Skills Used block read from the NATIVE STILL - " \
                       "the video frame had onslaught.dbr occluded by the quest tracker (D-2)." \
            if k == "skill_use_count" else VERIF + " sec 2 / sec 6b end-of-run panel."
        if k in ("total_score", "dps_field"):
            note = VERIF + " sec D-3: DEAD FIELD. Reads 0 for the entire run. Do not model."
        if k in ("health_potions_used", "mana_potions_used"):
            note = (VERIF + " sec D-3 RESOLVED: the counter is LIVE and CORRECT. Matt ran the "
                            "session with zero potions as a deliberate oracle control "
                            "(2026-07-26). See session_control.no-potions.")
        R.append(("Screenshot (352)", 6805.5, 7088, k, sub, v, vb,
                  "screenshot-fullres", cc, ccf, 0, note))
    # -- video-frame human reads (the sec 3 divergence table) ---------------
    for pts, pt in ((300.0, 653), (900.0, 1252), (1500.0, 1833),
                    (3289.0, 3606), (3349.0, 3665), (5600.0, 5892)):
        R.append((None, pts, pt, "play_time", "", float(pt),
                  "%d min %d sec" % (pt // 60, pt % 60),
                  "video-frame-human", "single-field-only", "play_time", 0,
                  VERIF + " sec 3 divergence table / sec 2 seek-accuracy check. Human read of a "
                          "full-resolution crop of an extracted frame - NOT an OCR read."))
    # -- deaths bracket, from sec 8 -----------------------------------------
    R.append((None, 900.0, 1252, "deaths", "", 0.0, "0", "video-frame-human",
              "single-field-only", "deaths", 0,
              VERIF + " sec 8: the panel samples bracket the two deaths (0 by t=900)."))
    R.append((None, 5600.0, 5892, "deaths", "", 2.0, "2", "video-frame-human",
              "single-field-only", "deaths", 0,
              VERIF + " sec 8: 2 by t=5600."))
    return R


# ---------------------------------------------------------------------------
# SESSION CONTROLS
# ---------------------------------------------------------------------------
CONTROLS = [
    ("no-potions", "held", "deliberate-control", "life_healed", "confound-retired",
     "With potions at zero, life_healed 12468.06 is ENTIRELY ENDOGENOUS: regeneration, "
     "lifesteal, devotion procs. No exogenous step-functions in the series. ~106 HP/min, "
     "~18.5 max-health pools (peak 672) over 113 min with no player-triggered heal. Under any "
     "potion usage this field is the sum of two unrelated processes and is worth nothing. A "
     "future run WITH potions produces a life_healed that means something completely different; "
     "THIS ROW is what distinguishes them.",
     "Matt verbatim 2026-07-26: 'I decided not to use any potions for the run so that it could "
     "be a more controlled oracle.' Confirmed on the end panel: Health potions used 0 / Mana 0.",
     "Matt", "2026-07-26"),
    ("no-potions", "held", "deliberate-control", "hp_current", "confound-retired",
     "Every downward move in the HP series is incoming damage; every upward move is endogenous "
     "recovery. No annotation pass is required to strip player heals.",
     VERIF + " sec 8.", "Matt", "2026-07-26"),
    ("no-potions", "held", "deliberate-control", "health_potions_used", "none",
     "The counter is live and correct at 0. NOT a dead field - D-3 resolved.",
     VERIF + " sec 5 D-3 / sec 8.", "Matt", "2026-07-26"),
    ("panel-always-on", "held", "protocol-requirement", "", "measure-enabled",
     "PlayStats visible in every frame, so every video frame carries the counter ledger. This "
     "is what makes the whole run a time series rather than a set of snapshots.",
     PROTO + " sec 1.1 / sec 2.2; " + VERIF + " sec 4 legibility PASS.", "gandalf", "2026-07-26"),
    ("no-menu-return", "held", "protocol-requirement", "skill_use_count", "measure-enabled",
     "skill_use_count and life_healed are SESSION-scoped (A6) and reset on a return to the main "
     "menu. One continuous session is what makes their bookend deltas meaningful.",
     PROTO + " sec 2.6; the monotone ledger trajectory in " + VERIF + " sec 6 is consistent with "
     "no reset.", "gandalf", "2026-07-26"),
    ("no-menu-return", "held", "protocol-requirement", "life_healed", "measure-enabled",
     "Same A6 session-scoping argument.", PROTO + " sec 2.6.", "gandalf", "2026-07-26"),
    ("counters-start-at-zero", "violated", "incidental", "kills", "confound-introduced",
     "The run's counters carry a non-zero baseline from the sec 2.0 smoke gate: kills=2 at "
     "pts=14.5. The run's kill delta is 880, not 882. Nothing in the protocol asked for a t0 "
     "panel read on the RUN video (sec 2.1 asks for a panel bookend, which Matt delivered as "
     "Screenshot (40)) - so this was recoverable, but only because the panel is on from frame "
     "one. It should be an explicit sec 2.1 step, not a lucky consequence.",
     "elrond tight-crop read of play_test_2026-07-26.mp4 @ pts=14.5 and of "
     "smoke_test_2026-07-26.mp4 @ t=25; both read kills=2.", "elrond", "2026-07-26"),
    ("counters-start-at-zero", "violated", "incidental", "skill_use_count",
     "confound-introduced",
     "defaultweaponattack=8 at t0. Total skill-use delta for the run is 684, not 692. "
     "sec 6b's ratio becomes 684/880 = 0.777 (it read 692/882 = 0.784). The CONCLUSION is "
     "unchanged - still fewer activations than corpses - but the number moves.",
     "As above.", "elrond", "2026-07-26"),
    ("counters-start-at-zero", "violated", "incidental", "life_healed",
     "confound-introduced",
     "life_healed=16.33 at t0. The run's endogenous healing is 12451.73, not 12468.06 - a "
     "0.13% correction to the sec 8 sustain figure. Small, and the point is not its size: a "
     "session-scoped counter with an unexamined t0 is a class of error, and this one happened "
     "to be small.", "As above.", "elrond", "2026-07-26"),
    ("panel-occluded-by-anger-overlay", "violated", "incidental", "health_potions_used",
     "confound-introduced",
     "SECOND occlusion source, distinct from D-2's quest tracker: the green ShowAngerLevels "
     "'[entityId] Action State: X' text renders OVER the PlayStats digits. In the smoke clip "
     "at t=25 it makes the potion counters unreadable. Priority order under conflict is "
     "already PlayStats > LogData > ShowAngerLevels (sec 3.4); this is the evidence that the "
     "conflict is real and not hypothetical.",
     "elrond tight-crop read of smoke_test_2026-07-26.mp4 @ t=25.", "elrond", "2026-07-26"),
    ("orb-numerals-always-shown", "held", "protocol-requirement", "hp_current", "measure-enabled",
     "Numerals ARE the E3 instrument; fill-fraction pixel reading is REJECTED (galadriel "
     "calibration 2026-07-26: 4.6 pp signal vs a 90.5 pp null band).",
     VERIF + " sec 4: orb numerals PASS at 2x - '672/672', '283/333'.", "gandalf", "2026-07-26"),
    ("level-matched-content-only", "not-attempted", "deliberate-control", "", "none",
     "F-3 lean: RECORD EVERYTHING, FILTER AT ANALYSIS. Off-level engagements are free "
     "calibration points on the level-differential axis.",
     PROTO + " sec 7 F-3.", "gandalf", "2026-07-26"),
    ("no-state-modifying-console", "unknown", "protocol-requirement", "", "none",
     "sec 2.2 forbids Spawn/killMonsters/God/Teleport/etc during the run. NOT ATTESTED for this "
     "session: no notes.md was delivered with the artifacts, so there is no record either way. "
     "Nothing in the verification contradicts compliance; nothing confirms it.",
     "ABSENT - protocol sec 3.5 notes.md not present in the delivered artifact tree.",
     "elrond", "2026-07-26"),
    ("difficulty-declared", "unknown", "protocol-requirement", "", "none",
     "sec 2.1 item 9 asks Matt to write down Difficulty / Starting area / Character level. Not "
     "delivered. difficulty is therefore NULL on the session row, not guessed.",
     "ABSENT - notes.md not present.", "elrond", "2026-07-26"),
    ("quest-tracker-collapsed", "violated", "protocol-requirement", "skill_use_count",
     "confound-introduced",
     "The quest tracker renders over the right edge of the PlayStats panel and occluded the "
     "onslaught.dbr count at t=6805 in the VIDEO (not in the native still). Costs an unknown "
     "small number of skill_use_count reads at arbitrary moments. v2 smoke-gate item.",
     VERIF + " sec 5 D-2 - present identically in screenshot and video, so it is game-UI "
             "layering, not compression.", "gandalf", "2026-07-26"),
    ("bitrate-ge-25mbps", "violated", "protocol-requirement", "", "none",
     "15.4 Mbps delivered against the sec 3.2 >=25 Mbps recommendation. ACCEPTED: the "
     "~10-14 px green overlay text - the highest-risk pixels - were checked directly and "
     "survive, entity IDs included. Not a gate; did not bind.",
     VERIF + " sec 4.", "gandalf", "2026-07-26"),
]

# ---------------------------------------------------------------------------
# BREAKS that are not derived from the anchors
# ---------------------------------------------------------------------------
AREAS = "Lower Crossing -> Devil's Crossing -> The Old Dump (areas traversed on sampled frames)"


def playtime_at(pts_s, anchors):
    """Left-anchor slope-1 extrapolation. USED ONLY for break BRACKETS, never to
    populate a join key. Returns ms."""
    best = anchors[0]
    for a in anchors:
        if a[0] <= pts_s:
            best = a
    return int(round((best[1] + (pts_s - best[0])) * 1000))


def main():
    for f in (SHA_PNG, SHA_MP4, STAT, DIM_PNG):
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            sys.exit(f"missing/empty precomputed input: {f}")

    sha = {}
    for path in (SHA_PNG, SHA_MP4):
        for line in open(path):
            h, p = line.rstrip("\n").split("  ", 1)
            sha[p] = h
    mt, sz = {}, {}
    for line in open(STAT):
        p, m, z = line.rstrip("\n").rsplit("|", 2)
        mt[p], sz[p] = float(m), int(z)
    dim = {}
    for line in open(DIM_PNG):
        p, w, h = line.rstrip("\n").split("|")
        dim["screenshots/" + p] = (int(w), int(h))

    shots = sorted(((int(re.search(r"\((\d+)\)", p).group(1)), p)
                    for p in mt if p.startswith("screenshots/")), key=lambda t: t[0])
    assert len(shots) == 313, len(shots)
    assert [n for n, _ in shots] == list(range(40, 353)), "contiguity broken"

    # --- capture bursts (structural fact: the grouping is real regardless of
    # --- what the shots turn out to CONTAIN) --------------------------------
    bursts, cur = [], [shots[0]]
    for i in range(1, len(shots)):
        if mt[shots[i][1]] - mt[shots[i - 1][1]] <= BURST_GAP_S:
            cur.append(shots[i])
        else:
            bursts.append(cur); cur = [shots[i]]
    bursts.append(cur)

    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys=ON")

    # --- amendment: capture.kind needs 'unclassified'. 313 stills whose CONTENT
    # --- role has not been determined must not be labelled 'other' (which asserts
    # --- a determination) nor 'playstats-panel' (true but lossy for sheet shots).
    kchk = cx.execute("SELECT sql FROM sqlite_master WHERE name='capture'").fetchone()[0]
    if "'unclassified'" not in kchk:
        cx.execute("PRAGMA foreign_keys=OFF"); cx.execute("PRAGMA legacy_alter_table=ON")
        # NB: a prior ALTER ... RENAME leaves the stored DDL as `CREATE TABLE "capture"`,
        # quoted. Match both forms.
        new_ddl = re.sub(r'CREATE TABLE "?capture"?', "CREATE TABLE capture_v2", kchk, count=1)
        # target the `kind` CHECK specifically - `media_kind`'s list also ends in 'other'
        assert "'nameplate-tooltip','other')" in new_ddl
        new_ddl = new_ddl.replace("'nameplate-tooltip','other')",
                                  "'nameplate-tooltip','other','unclassified')", 1)
        assert "'unclassified'" in new_ddl and "capture_v2" in new_ddl, new_ddl[:200]
        cx.executescript(new_ddl)
        c = [r[1] for r in cx.execute("PRAGMA table_info(capture)")]
        cx.execute(f"INSERT INTO capture_v2 ({','.join(c)}) SELECT {','.join(c)} FROM capture")
        cx.execute("DROP TABLE capture")
        cx.execute("ALTER TABLE capture_v2 RENAME TO capture")
        cx.execute("PRAGMA foreign_keys=ON")
        print("  amended capture.kind CHECK += 'unclassified'")

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # --- 1. sessions ------------------------------------------------------
    for sid in (S, SM):
        for tbl in ("session_ledger", "session_break", "session_control",
                    "clock_anchor", "clock_map", "capture"):
            cx.execute(f"DELETE FROM {tbl} WHERE session_id=?", (sid,))
        cx.execute("DELETE FROM fixture_session WHERE session_id=?", (sid,))
    cx.execute("""INSERT INTO fixture_session
      (session_id,lane,session_date,operator,capture_dir,capture_clock_source,notes,
       adapter,schema_version,created_date,wallclock_seconds)
      VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (
        SM, "gd-live", "2026-07-26", "Matt", BASE, "in-game-playtime",
        "protocol sec 2.0 SMOKE GATE, 26.65 s. Banked as its own session because sec 2.0 "
        "permits it ('The smoke may be its own session - quitting to menu after it is fine') "
        "and A6 makes that boundary semantically load-bearing: skill_use_count and "
        "life_healed are declared SESSION-scoped and resettable there.\n"
        "FINDING: they did NOT reset. The panel reads defaultweaponattack=8 and "
        "life_healed=16.33 at BOTH the smoke's t=25 s and the run's pts=14.5 s. kills reads 2 "
        "at both, which is consistent with A6's SAVE-cumulative classification for kills but "
        "NOT with its SESSION-scoped classification for the other two. Either Matt did not "
        "return to the menu between the smoke and the run, or A6's split is wrong. "
        "DECIDABLE: 550.9 s of wallclock separates the two clips while play_time advanced "
        "only 13 s (358 -> 371), which is a lot of frozen time for a continuous session.\n"
        "Consequence either way: the RUN'S COUNTERS DO NOT START AT ZERO. See "
        "session_ledger rows for GP-gd-2026-07-26-s1 at play_time_ms=371000.",
        "elrond/fixtures_m6_gp_run01_ingest_2026_07_26.py", "fixtures-v0.3", "2026-07-26",
        26.65))
    cx.execute("""INSERT INTO fixture_session
      (session_id,lane,session_date,operator,game_edition_pin,game_build_string,difficulty,
       container,save_identity,console_flags,rig_version,raw_notes_path,capture_dir,
       capture_clock_source,sim_config_ref,notes,adapter,schema_version,created_date,
       video_start_epoch,video_start_epoch_method,video_start_epoch_uncertainty_s,
       playtime_banked_prefix_s,wallclock_seconds,playtime_seconds)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
        S, "gd-live", "2026-07-26", "Matt", None, None,
        None,                       # difficulty NOT ATTESTED - notes.md absent
        "mp4", None,
        '{"game.PlayStats": {"state": true, "evidence": "panel legible in every sampled frame"},'
        ' "character.LogData": {"state": true, "evidence": "gandalf verification sec 6b"},'
        ' "character.ShowAngerLevels": {"state": "presumed-true",'
        ' "evidence": "green [entityId] Action State overlay legible at 3x; flag not separately attested"}}',
        None,
        None,                       # raw_notes_path - NONE DELIVERED
        BASE,
        "in-game-playtime",
        None,
        "GP RUN 01. First general-play recorded run. lane='gd-live' is the ORACLE lane "
        "(protocol sec 5.1 says lane='oracle'; the store's discriminator value for the oracle "
        "lane is 'gd-live' and v_differential keys on it).\n"
        "A6 CLOCK SPLIT: play_time / kills / deaths / potions / max_level_achieved are "
        "declared SAVE-cumulative; skill_use_count / life_healed are declared SESSION-scoped. "
        "Both groups are usable here because this is one continuous session.\n"
        "*** NON-ZERO BASELINE - READ THIS BEFORE COMPUTING ANY DELTA ***\n"
        "The run's counters do NOT start at zero. At pts=14.5 s the panel already reads "
        "kills=2, defaultweaponattack=8, life_healed=16.33 - carried in from the sec 2.0 smoke "
        "gate (session GP-gd-2026-07-26-smoke), where the same three read 2 / 8 / 16.33. "
        "Bookend deltas for THIS RUN are: kills 880 (not 882), total skill uses 684 (not 692), "
        "defaultweaponattack 66 (not 74), life_healed 12451.73 (not 12468.06). "
        "That skill_use_count and life_healed survived the smoke->run boundary at all "
        "contradicts A6's SESSION-scoped classification for those two, unless the smoke and "
        "the run were one unbroken session. Open question; the baseline stands either way.\n"
        "TWO CLOCKS: play_time (game state) leads video offset by +356.5 s at the head "
        "(banked prefix - creation, smoke test, menus before recording) and loses ~73.5 s over "
        "the run in DISCRETE STEPS at zone transitions. play_time_ms is the JOIN KEY; pts_ms is "
        "the camera clock and is for frame retrieval only.\n"
        "THREE QUALIFICATIONS ON THE JOIN KEY, none of which retire it:\n"
        " (a) GRANULARITY. The panel renders play_time to whole seconds, so play_time_ms is "
        "quantised at 1000 ms. An engagement lasts ~5 s and an AoE multi-kill puts several "
        "kills inside ONE tick. play_time therefore CANNOT ORDER EVENTS within a second, and "
        "S1 kill-to-kill segmentation is precisely about ordering kill increments. Use the "
        "COMPOSITE (play_time_ms, pts_ms): play_time is the correctness axis (it is the only "
        "one that survives the loading discontinuity), pts_ms at 16.7 ms is the ordering axis "
        "within a clock segment. Every session_ledger and capture row carries both.\n"
        " (b) NOT INJECTIVE. play_time freezes during loading, so many video frames map to one "
        "play_time_ms across a zone transition. A lookup by play_time alone is one-to-many "
        "exactly at the breaks, which is where it matters most.\n"
        " (c) SAVE-SCOPED, NOT SESSION-SCOPED. play_time is SAVE-cumulative, so the true key is "
        "(save_identity, play_time_ms). A second run on THIS save continues from ~7088 s and "
        "orders correctly; a run on a NEW character restarts at 0 and COLLIDES. "
        "fixture_session.save_identity is NULL here because it was not attested - protocol "
        "sec 2.1 item 9 does not ask for it. It should.\n"
        "CONSTRAINTS: sec 5.3 declares every L0 constraint violated by construction. Those are "
        "per-fixture_set rows and are written when sets exist.\n"
        "OBS: 1920x1080, h264, 60/1 CFR, 15.4 Mbps (below the sec 3.2 >=25 Mbps recommendation; "
        "accepted - see session_control.bitrate-ge-25mbps). Audio present.\n"
        "NOT DELIVERED: notes.md (protocol sec 3.5). Difficulty, starting area, per-boundary "
        "play_time jots and per-transition area names are therefore ABSENT, not inferred.",
        "elrond/fixtures_m6_gp_run01_ingest_2026_07_26.py", "fixtures-v0.3",
        "2026-07-26",
        VSTART, "mtime(video) - duration; PROVEN exact at 4 independent points against the "
                "on-screen ledger (shots 40/200/280/352, co-agreeing on play_time, kills, "
                "deaths and max_level_achieved simultaneously). "
                "NOTE: fractional mtime 1785103033.4488 - 6816.516667 = 1785096216.932, which "
                "is 0.43 s later than the banked constant. gandalf's 1785096216.5 is banked as "
                "directed; the 0.43 s sits inside the recorded uncertainty.",
        0.5, 356.5, VDUR, 6717.0))

    # --- 2. controls ------------------------------------------------------
    cx.executemany("""INSERT INTO session_control
      (session_id,control_key,held,intent,affects_measure_key,effect_on_measure,effect_note,
       evidence,ruled_by,ruled_date) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                   [(S,) + c for c in CONTROLS])

    # --- 3. captures ------------------------------------------------------
    anchors_by_label = {a[3]: a for a in ANCHORS if a[3]}
    burst_of = {}
    for bi, b in enumerate(bursts):
        for oi, (n, p) in enumerate(b):
            burst_of[p] = (f"{S}/burst-{bi:02d}", oi)
    rows = []
    for n, p in shots:
        rel = p            # STAT_PNG keys already carry the 'screenshots/' prefix
        pts_ms = int(round((mt[p] - VSTART) * 1000))
        lbl = f"Screenshot ({n})"
        a = anchors_by_label.get(lbl)
        w, h = dim.get(rel, (None, None))
        bid, bo = burst_of[p]
        rows.append((
            f"{S}/shot-{n:03d}", S, f"{BASE}/{rel}", ROOT, "still", "unclassified", lbl,
            sha[rel], datetime.datetime.fromtimestamp(mt[p], datetime.timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%S.%f+00:00"),
            "capture-time-attested", mt[p],
            pts_ms, "mtime-arithmetic", 500,
            int(a[1] * 1000) if a else None,
            "screenshot-fullres" if a else "absent",
            0 if a else None,
            bid, bo, None, None, w, h,
            "kind='unclassified': the CONTENT role of this still (playstats-panel vs "
            "character-sheet vs equipment-doll vs world-view) has not been determined. "
            "galadriel's pass assigns it. Every still carries the PlayStats panel by protocol "
            "sec 2.2, but that is not the whole of what each one is."
            if not a else
            "ANCHOR SHOT. play_time_ms read by hand at full resolution; see clock_anchor."))
    cx.executemany("""INSERT INTO capture
      (capture_id,session_id,path,storage_root,media_kind,kind,label,sha256,mtime_utc,
       mtime_semantics,mtime_epoch,pts_ms,pts_method,pts_uncertainty_ms,play_time_ms,
       play_time_method,play_time_uncertainty_ms,burst_id,burst_ordinal,duration_s,
       parent_capture_id,pixel_w,pixel_h,notes)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)

    vid = "recorded_videos/play_test_2026-07-26.mp4"
    smoke = "recorded_videos/smoke_test_2026-07-26.mp4"
    cx.executemany("""INSERT INTO capture
      (capture_id,session_id,path,storage_root,media_kind,kind,label,sha256,mtime_utc,
       mtime_semantics,mtime_epoch,pts_ms,pts_method,pts_uncertainty_ms,play_time_ms,
       play_time_method,play_time_uncertainty_ms,duration_s,pixel_w,pixel_h,notes)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", [
        (f"{S}/video-session", S, f"{BASE}/{vid}", ROOT, "video", "video-session",
         "play_test_2026-07-26.mp4", sha[vid],
         datetime.datetime.fromtimestamp(mt[vid], datetime.timezone.utc)
         .strftime("%Y-%m-%dT%H:%M:%S.%f+00:00"), "capture-time-attested", mt[vid],
         0, "container-origin", 0,
         356500, "derived-from-anchor", 15000, VDUR, 1920, 1080,
         "THE primary instrument. h264, r_frame_rate=avg_frame_rate=60/1 (CFR), "
         "nb_frames=408991, 13,119,968,478 B, 15.4 Mbps, AAC present (319,524 frames). "
         "pts_ms=0 by definition; play_time_ms at pts=0 is EXTRAPOLATED slope-1 from the first "
         "anchor (shot 40 at pts 14.5 s / play_time 371 s), giving 356.5 s - gandalf's banked "
         "prefix.\n"
         "AND THE EXTRAPOLATION IS DEMONSTRABLY LOW. The smoke clip reads play_time 358 s at its "
         "t=25 of 26.65, so play_time was >= 359.65 s when the smoke ended - which is BEFORE "
         "this recording started. play_time is monotonic, so play_time(pts=0) >= 359.65 s, not "
         "356.5 s. The gap means >= 3.15 s of the first 14.5 s of this recording was frozen "
         "(OBS start / alt-tab back into the game), so slope was NOT 1 there.\n"
         "Nothing is broken by this: the true prefix lies in [359.65, 371] and every anchor "
         "from shot 40 onward is a direct read. It is a live demonstration that slope-1 "
         "extrapolation into an UNANCHORED region is unsound, which is exactly why "
         "play_time_method='derived-from-anchor' is banked here and is not a join key."),
        (f"{SM}/video-smoke", SM, f"{BASE}/{smoke}", ROOT, "video", "video-session",
         "smoke_test_2026-07-26.mp4", sha[smoke],
         datetime.datetime.fromtimestamp(mt[smoke], datetime.timezone.utc)
         .strftime("%Y-%m-%dT%H:%M:%S.%f+00:00"), "capture-time-attested", mt[smoke],
         None, "absent", None, None, "absent", None, 26.65, 1920, 1080,
         "protocol sec 2.0 smoke gate clip, 17.9 Mbps. Banked under its OWN session "
         "(GP-gd-2026-07-26-smoke) because sec 2.0 permits the smoke to be a separate "
         "session and A6 makes that boundary semantically load-bearing. It is NOT on the run "
         "timeline (it ends 547.5 s before video_start_epoch) and carries no pts_ms."),
    ])

    # --- 3b. the smoke session + its end-of-clip panel ---------------------
    for mk, sub, v, vb, occ, note in SMOKE_LEDGER:
        unit = UNITS.get(mk)
        cx.execute("""INSERT INTO session_ledger
          (session_id,play_time_ms,play_time_method,play_time_uncertainty_ms,pts_ms,
           measure_key,measure_subkey,value_num,unit,verbatim,read_method,read_confidence,
           uncertainty_abs,capture_id,cross_check_status,cross_check_fields,occluded,
           validity_flag,validity_note)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                   (SM, 358000, "video-frame-human", 1000, 25000, mk, sub, v, unit, vb,
                    "video-frame-human", None, 0.0, f"{SM}/video-smoke",
                    "single-field-only", mk, occ, "valid",
                    "Smoke clip at t=25 s, read by elrond from a tight crop at 1.6x. " + note))
    cx.execute("""INSERT INTO session_control
      (session_id,control_key,held,intent,affects_measure_key,effect_on_measure,effect_note,
       evidence,ruled_by,ruled_date) VALUES (?,?,?,?,?,?,?,?,?,?)""",
               (SM, "smoke-gate-performed", "held", "protocol-requirement", "kills", "none",
                "sec 2.0 item 5 ('Record 60 seconds. Kill 2 monsters.') was performed: the "
                "panel reads kills=2 at t=25 s of a 26.65 s clip.",
                "elrond tight-crop read of smoke_test_2026-07-26.mp4 @ t=25.",
                "elrond", "2026-07-26"))

    # --- 4. clock anchors + piecewise map ---------------------------------
    for pts, pt, src, lbl, co, ev in ANCHORS:
        cid = None
        if lbl:
            cid = cx.execute("SELECT capture_id FROM capture WHERE session_id=? AND label=?",
                             (S, lbl)).fetchone()
            cid = cid[0] if cid else None
        elif src == "video-frame-panel":
            cid = f"{S}/video-session"
        cx.execute("""INSERT INTO clock_anchor
          (session_id,pts_ms,play_time_ms,source,capture_id,read_method,co_agreeing_fields,
           uncertainty_ms,evidence) VALUES (?,?,?,?,?,?,?,?,?)""",
                   (S, int(pts * 1000), int(pt * 1000), src, cid,
                    "screenshot-fullres" if src == "screenshot-panel" else "video-frame-human",
                    co, 1000, ev))

    for i in range(len(ANCHORS) - 1):
        p0, t0 = ANCHORS[i][0], ANCHORS[i][1]
        p1, t1 = ANCHORS[i + 1][0], ANCHORS[i + 1][1]
        off0 = t0 - p0
        off1 = t1 - p1
        loss_ms = int(round((off0 - off1) * 1000))
        cx.execute("""INSERT INTO clock_map
          (session_id,segment_ordinal,pts_ms_from,pts_ms_to,offset_ms,slope,fit_method,
           n_anchors,residual_max_ms,status,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                   (S, i, int(p0 * 1000), int(p1 * 1000), int(round(off0 * 1000)), 1.0,
                    "anchor-pair-slope1", 2, loss_ms, "provisional",
                    f"PROVISIONAL. Slope is exactly 1 WITHIN a segment (gandalf sec 3), but "
                    f"{loss_ms} ms of frozen loading time is unallocated somewhere inside this "
                    f"interval and is NOT yet located. Using the left-anchor offset across the "
                    f"whole interval therefore carries up to {loss_ms} ms of error. An engagement "
                    f"lasts ~5000 ms. Refit with knots at the located zone transitions once the "
                    f"2 fps panel OCR lands."))

    # --- 5. session breaks -------------------------------------------------
    A = [(a[0], a[1]) for a in ANCHORS]
    B = []
    # 5a. the two deaths, located to the brackets the panel samples give
    B.append((f"{S}/break-death-1", "death",
              playtime_at(900.0, A), playtime_at(3259.0, A), 900000, 3259000, None,
              1, 0, 0, 1, "panel-counter-delta", "attested", None, None,
              "Death 1. The deaths counter is 0 at pts 900 and 1 at pts 3259 (screenshot 200 "
              "co-agreeing on four fields). The DEATH IS ATTESTED; its LOCATION is a 2359 s "
              "bracket. An HP reset AND a position reset - a hard segmentation break. Exclude "
              "any continuous-series fit that spans it. Narrow this with the 2 fps ledger pass, "
              "or with the audio track (v2 protocol asks Matt to call each death aloud).",
              None))
    B.append((f"{S}/break-death-2", "death",
              playtime_at(3259.0, A), playtime_at(5600.0, A), 3259000, 5600000, None,
              1, 0, 0, 1, "panel-counter-delta", "attested", None, None,
              "Death 2. deaths=1 at pts 3259, =2 at pts 5600. Same disposition as death 1; "
              "2341 s bracket.", None))
    # 5b. the one zone transition observed on camera
    B.append((f"{S}/break-zone-observed-1", "zone-transition",
              playtime_at(3289.0, A), playtime_at(3349.0, A), 3289000, 3349000, 1000,
              1, 1, 0, 1, "video-observed", "attested", "Devil's Crossing", "The Old Dump",
              "The mechanism caught on camera (gandalf sec 3): between pts 3289 (Devil's "
              "Crossing) and pts 3349 (The Old Dump) the ledger advanced 3606->3665 s while "
              "wallclock advanced 60 s - 1 s of frozen time. Breaks combat continuity AND the "
              "clock affine map.", None))
    # 5c. an area transition known to exist but not located
    B.append((f"{S}/break-zone-inferred-1", "zone-transition",
              None, None, None, None, None, 1, 1, 0, 1, "area-name-change", "inferred",
              "Lower Crossing", "Devil's Crossing",
              "Areas traversed on the sampled frames were " + AREAS + ". The Lower Crossing -> "
              "Devil's Crossing transition therefore occurred, but no frame located it and no "
              "notes.md was delivered (protocol sec 2.4 asks for area + play_time at every "
              "transition). Location UNRESOLVED - both bounds NULL rather than guessed.", None))
    # 5d. one unallocated-clock-loss break per map segment
    for i in range(len(ANCHORS) - 1):
        p0, t0 = ANCHORS[i][0], ANCHORS[i][1]
        p1, t1 = ANCHORS[i + 1][0], ANCHORS[i + 1][1]
        loss_ms = int(round(((t0 - p0) - (t1 - p1)) * 1000))
        if loss_ms <= 0:
            continue
        B.append((f"{S}/break-clockloss-{i:02d}", "unknown",
                  int(t0 * 1000), int(t1 * 1000), int(p0 * 1000), int(p1 * 1000), loss_ms,
                  0, 1, 0, 0, "panel-counter-delta", "hypothesis", None, None,
                  f"{loss_ms} ms of wallclock that play_time did not count, somewhere in "
                  f"pts [{p0}, {p1}]. DERIVED from the anchor-pair divergence, not observed. "
                  f"break_kind='unknown' because the MECHANISM is only attested for "
                  f"break-zone-observed-1; zone transition is the leading hypothesis. "
                  f"breaks_combat_continuity=0 because that is unknown, not established - "
                  f"do not exclude fits on this row until the mechanism is confirmed.", None))
    # 5e. epoch-boundary candidates from the mtime burst structure
    nb = 0
    for bi, b in enumerate(bursts):
        dur = mt[b[-1][1]] - mt[b[0][1]]
        if len(b) < EPOCH_MIN_N or dur < EPOCH_MIN_DUR:
            continue
        nb += 1
        p0 = mt[b[0][1]] - VSTART
        p1 = mt[b[-1][1]] - VSTART
        B.append((f"{S}/break-epoch-cand-{bi:02d}", "epoch-boundary",
                  playtime_at(p0, A), playtime_at(p1, A), int(p0 * 1000), int(p1 * 1000), None,
                  0, 0, 1, 1, "mtime-burst-inference", "hypothesis", None, None,
                  f"EPOCH-BOUNDARY CANDIDATE. {len(b)} screenshots (shots {b[0][0]}-{b[-1][0]}) "
                  f"taken within {dur:.1f} s of each other. Protocol sec 2.3 says a boundary "
                  f"costs ~60-90 s of overlapping character-sheet scroll crops, which is exactly "
                  f"this signature. INFERRED FROM FILE MTIMES ALONE - no pixel has been read. "
                  f"Rule: burst gap <= {BURST_GAP_S} s, n >= {EPOCH_MIN_N}, duration >= "
                  f"{EPOCH_MIN_DUR} s. Falsified if the shots turn out not to be a character "
                  f"sheet. galadriel's pass confirms or drops each one.", None))
    cx.executemany("""INSERT INTO session_break
      (break_id,session_id,break_kind,play_time_ms_lo,play_time_ms_hi,pts_ms_lo,pts_ms_hi,
       clock_step_ms,breaks_combat_continuity,breaks_clock_affine,breaks_character_state,
       exclude_from_fit,detection_method,confidence,area_from,area_to,evidence,capture_id)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                   [(r[0], S) + r[1:] for r in B])

    # --- 6. the observed ledger -------------------------------------------
    for lbl, pts, pt, mk, sub, num, vb, rm, cc, ccf, occ, note in ledger_rows():
        cid = f"{S}/video-session"
        if lbl:
            r = cx.execute("SELECT capture_id FROM capture WHERE session_id=? AND label=?",
                           (S, lbl)).fetchone()
            cid = r[0] if r else None
        unit = UNITS.get(mk)
        cx.execute("""INSERT INTO session_ledger
          (session_id,play_time_ms,play_time_method,play_time_uncertainty_ms,pts_ms,
           measure_key,measure_subkey,value_num,unit,verbatim,read_method,read_confidence,
           uncertainty_abs,capture_id,cross_check_status,cross_check_fields,occluded,
           validity_flag,validity_note)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                   (S, int(pt * 1000), rm, 1000, int(pts * 1000), mk, sub, num, unit, vb,
                    rm, None, 0.0, cid, cc, ccf, occ, "valid", note))

    cx.commit()
    print("foreign_key_check:", cx.execute("PRAGMA foreign_key_check").fetchall() or "CLEAN")
    for t in ("capture", "session_ledger", "session_break", "session_control",
              "clock_anchor", "clock_map"):
        print(f"  {t}: {cx.execute(f'SELECT COUNT(*) FROM {t} WHERE 1').fetchone()[0]} total, "
              f"{cx.execute(f'SELECT COUNT(*) FROM {t}' + (' WHERE session_id=?' if t!='x' else ''), (S,)).fetchone()[0]} this session")
    print(f"  epoch-boundary candidates: {nb}")
    print("  captures with play_time_ms:",
          cx.execute("SELECT COUNT(*) FROM capture WHERE session_id=? AND play_time_ms IS NOT NULL",
                     (S,)).fetchone()[0], "/ 315")
    cx.close()


if __name__ == "__main__":
    main()
