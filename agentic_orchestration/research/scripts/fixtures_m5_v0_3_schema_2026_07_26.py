#!/usr/bin/env python3
"""
fixtures.db - MILESTONE 5: schema fixtures-v0.3
================================================
Commissioned by gandalf, `2026-07-26-gd-general-play-run-protocol.md` sec 5 (data contract),
against the first real general-play run (313 stills + 1:53:36 of 1080p60 video).

Agent: elrond (store owner). Run AFTER m1-m4 + the gd_bridge chain. Idempotent.

THE CENTRAL CHANGE
------------------
v0.1/v0.2 assume the unit of observation is a TRIAL: every number lands in
`trial_measurement` under a (trial, phase) key. That holds for L0, where Matt hand-brackets
each fight with a before/after screenshot pair.

It does NOT hold for a general-play run. There the unit of observation is a SESSION-CONTINUOUS
LEDGER sampled ~2 fps off the PlayStats panel, which exists PRIOR TO and INDEPENDENT OF any
segmentation into engagements. Trials are DERIVED from that ledger, by a rule (S1/S2/S3), and
sec 4.5 asks for three competing rules simultaneously. Forcing the ledger through
`trial_measurement` would store the same readings three times, once per segmentation, and let
the three copies drift.

So v0.3 splits the two layers:
  * `session_ledger`  - the observed series. Keyed on play_time_ms. One copy. No segmentation.
  * `fixture_trial`   - a WINDOW over that series, carrying which rule cut it.
`trial_measurement` survives unchanged for hand-bracketed L0 rows and for attributed values.

SECOND CHANGE: play_time_ms is the join key, pts_ms is not.
`play_time` is the game-state clock; video offset is the camera clock. They diverge by a banked
prefix (+356 s here) and by ~73 s of frozen loading time accumulated in discrete steps at zone
transitions. Both are stored on every row; every cross-artifact join goes through play_time_ms.
The map between them is a first-class object (`clock_map` + `clock_anchor`), fitted per session,
never assumed - gandalf verification sec 3.

THIRD CHANGE: the derived layer is separable from the observed layer, and enforceable.
`measure_dict.layer` + `measure_dict.ingest_block` + two triggers. `attacks_per_kill` is
registered and BLOCKED at the database level pending the sec 6b skill_use_count verdict, so the
block survives the memory of the person who wrote it down.

Backup taken before this runs: fixtures.db.pre-v0.3-*-backup
"""

import hashlib
import os
import sqlite3
import sys

REPO = "/Users/admin/Games/reincarnated-collaboration"
DB = os.path.join(REPO, "agentic_orchestration/research/curated/fixtures.db")
VERSION = "fixtures-v0.3"

# ---------------------------------------------------------------------------
# read-method vocabulary of record (v0.1 had it duplicated as a CHECK on two
# tables; v0.3 makes the dict authoritative and FKs the new tables to it)
# ---------------------------------------------------------------------------
READ_METHODS = [
    # key, family, is_ocr, needs_confidence, note
    ("screenshot-fullres",      "still",  0, 0,
     "Human read of a full-resolution crop of a native PNG. M3 method law."),
    ("screenshot-downscaled",   "still",  0, 0,
     "Read off a downscaled frame. Region location only - never bank a digit from this."),
    ("screenshot-illegible",    "still",  0, 0, "Region located, digits not resolvable."),
    ("video-frame-human",       "video",  0, 0,
     "Human read of a full-resolution crop of a frame extracted from the session MP4. "
     "DISTINCT from video-frame-ocr: the sec 4.6 G-c OCR error-rate audit is a claim about "
     "the OCR class only, and a human read must not hide inside that class."),
    ("video-frame-ocr",         "video",  1, 1,
     "CV read of an extracted frame. Requires read_confidence AND a cross_check_status other "
     "than 'unchecked' before it is trustworthy - gandalf D-1: legibility is not accuracy."),
    ("video-frame-ocr-rejected","video",  1, 1,
     "CV read that failed its confidence gate or its cross-field check. Banked, not used."),
    ("hand-noted-point",        "hand",   0, 0, "Matt's notes, point value."),
    ("hand-noted-band",         "hand",   0, 0, "Matt's notes, banded value."),
    ("inferred-adjacent-trial", "derive", 0, 0, "Carried from a neighbouring trial. Circular; excluded from continuity gates."),
    ("sim-emitted",             "sim",    0, 0, "Emitted by the simulation lane."),
    ("derived",                 "derive", 0, 0, "Computed from other banked readings."),
    ("mtime-arithmetic",        "meta",   0, 0,
     "Derived from filesystem mtime against a banked video_start_epoch. Metadata, not a pixel read."),
    ("container-origin",        "meta",   0, 0,
     "The container's own origin: pts=0 for the session recording. Definitional, not measured."),
    ("derived-from-anchor",     "meta",   0, 0,
     "Extrapolated along a clock_map segment from the nearest clock_anchor. NEVER a join key - "
     "up to ~19 s of unallocated frozen loading time sits inside a segment and an engagement "
     "lasts ~5 s."),
    ("absent",                  "meta",   0, 0,
     "The field was looked for and is NOT AVAILABLE. Honest missing. Never an inference."),
]

DDL_NEW = r"""
-- =====================================================================
-- v0.3 NEW TABLES
-- =====================================================================

CREATE TABLE IF NOT EXISTS read_method_dict (
  read_method   TEXT PRIMARY KEY,
  family        TEXT NOT NULL,      -- still|video|hand|sim|derive|meta
  is_ocr        INTEGER NOT NULL,
  needs_confidence INTEGER NOT NULL,
  note          TEXT
);

-- The observed session-continuous ledger. THE unit of observation for a
-- general-play run. Exists prior to, and independent of, any segmentation.
CREATE TABLE IF NOT EXISTS session_ledger (
  ledger_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  play_time_ms    INTEGER,               -- GAME-STATE clock. THE JOIN KEY. NULL = unresolved.
  play_time_method TEXT REFERENCES read_method_dict(read_method),
  play_time_uncertainty_ms INTEGER,
  pts_ms          INTEGER,               -- CAMERA clock. Frame retrieval only. Never a join key.
  measure_key     TEXT NOT NULL REFERENCES measure_dict(measure_key),
  measure_subkey  TEXT NOT NULL DEFAULT '',
  value_num       REAL,
  value_num_hi    REAL,
  value_text      TEXT,
  unit            TEXT,
  verbatim        TEXT,
  read_method     TEXT NOT NULL REFERENCES read_method_dict(read_method),
  read_confidence REAL,                  -- CV confidence 0-1; NULL for human reads
  uncertainty_abs REAL,
  capture_id      TEXT REFERENCES capture(capture_id),
  -- gandalf D-1: a confidently-rendered wrong digit does not announce itself.
  -- An OCR read is NOT trusted until it co-agrees with a second field on the same frame.
  cross_check_status TEXT NOT NULL DEFAULT 'unchecked'
      CHECK (cross_check_status IN ('unchecked','co-agree','co-disagree','single-field-only','not-applicable')),
  cross_check_fields TEXT,               -- e.g. 'kills,deaths,max_level_achieved'
  occluded        INTEGER NOT NULL DEFAULT 0,   -- gandalf D-2 quest-tracker overlay
  validity_flag   TEXT NOT NULL DEFAULT 'valid'
      CHECK (validity_flag IN ('valid','window-expired','superseded','suspect')),
  validity_note   TEXT,
  UNIQUE (session_id, measure_key, measure_subkey, capture_id, play_time_ms)
);
CREATE INDEX IF NOT EXISTS ix_session_ledger_join
  ON session_ledger (session_id, measure_key, measure_subkey, play_time_ms);
CREATE INDEX IF NOT EXISTS ix_session_ledger_pts
  ON session_ledger (session_id, pts_ms);

-- Segmentation breaks, first-class. Deaths, zone transitions, epoch boundaries.
-- Three DIFFERENT kinds of break, distinguished by three independent flags rather
-- than collapsed into one 'is a break' boolean:
--   a death           breaks combat continuity, NOT the clock, NOT character state
--   a zone transition breaks combat continuity AND the clock (frozen loading time)
--   an epoch boundary breaks character-state carry-over only
CREATE TABLE IF NOT EXISTS session_break (
  break_id        TEXT PRIMARY KEY,
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  break_kind      TEXT NOT NULL CHECK (break_kind IN
                    ('death','zone-transition','epoch-boundary','menu-return',
                     'console-command','capture-pause','stutter','unknown')),
  -- LOCATION IS A BAND, NOT A POINT. A death known only to lie between two panel
  -- samples is located to that bracket and says so.
  play_time_ms_lo INTEGER,
  play_time_ms_hi INTEGER,
  pts_ms_lo       INTEGER,
  pts_ms_hi       INTEGER,
  clock_step_ms   INTEGER,               -- wallclock that play_time did NOT count across this break
  breaks_combat_continuity INTEGER NOT NULL DEFAULT 1,
  breaks_clock_affine      INTEGER NOT NULL DEFAULT 0,
  breaks_character_state   INTEGER NOT NULL DEFAULT 0,
  exclude_from_fit         INTEGER NOT NULL DEFAULT 1,
  detection_method TEXT NOT NULL CHECK (detection_method IN
                    ('panel-counter-delta','mtime-burst-inference','video-observed',
                     'audio-cue','hand-noted','area-name-change','unresolved')),
  confidence      TEXT NOT NULL CHECK (confidence IN ('attested','inferred','hypothesis')),
  area_from       TEXT,
  area_to         TEXT,
  evidence        TEXT,
  capture_id      TEXT REFERENCES capture(capture_id),
  superseded_by   TEXT REFERENCES session_break(break_id)
);
CREATE INDEX IF NOT EXISTS ix_session_break_pt
  ON session_break (session_id, play_time_ms_lo);

-- Session-level controls. A run property that changes what a MEASURE MEANS.
-- The no-potion decision makes life_healed entirely endogenous; a future run WITH
-- potions produces a life_healed that is the sum of two unrelated processes and is
-- worth nothing. Nothing in the v0.2 schema distinguished those two numbers.
CREATE TABLE IF NOT EXISTS session_control (
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  control_key     TEXT NOT NULL,
  held            TEXT NOT NULL CHECK (held IN ('held','violated','partial','unknown','not-attempted')),
  intent          TEXT NOT NULL CHECK (intent IN
                    ('deliberate-control','protocol-requirement','incidental','unknown')),
  affects_measure_key TEXT NOT NULL DEFAULT '',   -- '' = session-wide, no single measure
  effect_on_measure   TEXT NOT NULL DEFAULT 'none'
      CHECK (effect_on_measure IN
        ('none','confound-retired','confound-introduced','measure-invalidated','measure-enabled')),
  effect_note     TEXT,
  evidence        TEXT,
  ruled_by        TEXT,
  ruled_date      TEXT,
  PRIMARY KEY (session_id, control_key, affects_measure_key)
);

-- The play_time <-> pts map. gandalf verification sec 3 ruling: piecewise, slope-1
-- segments, knots at zone transitions, FITTED per session, never assumed.
CREATE TABLE IF NOT EXISTS clock_anchor (
  anchor_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  pts_ms          INTEGER NOT NULL,
  play_time_ms    INTEGER NOT NULL,
  source          TEXT NOT NULL CHECK (source IN ('screenshot-panel','video-frame-panel','hand-noted')),
  capture_id      TEXT REFERENCES capture(capture_id),
  read_method     TEXT NOT NULL REFERENCES read_method_dict(read_method),
  co_agreeing_fields TEXT,            -- the D-1 cross-check that makes this anchor trustworthy
  uncertainty_ms  INTEGER,
  evidence        TEXT
);

CREATE TABLE IF NOT EXISTS clock_map (
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  segment_ordinal INTEGER NOT NULL,
  pts_ms_from     INTEGER,
  pts_ms_to       INTEGER,
  offset_ms       INTEGER,            -- play_time_ms = round(slope * pts_ms) + offset_ms
  slope           REAL NOT NULL DEFAULT 1.0,
  fit_method      TEXT NOT NULL CHECK (fit_method IN ('anchor-pair-slope1','ols','assumed','unfitted')),
  n_anchors       INTEGER,
  residual_max_ms INTEGER,
  opening_break_id TEXT REFERENCES session_break(break_id),
  status          TEXT NOT NULL CHECK (status IN ('provisional','fitted','superseded')),
  notes           TEXT,
  PRIMARY KEY (session_id, segment_ordinal)
);

-- Per-slot equipment provenance. The v0.2 store had gear as one JSON blob on
-- fixture_character, which cannot express the difference between
--   'this slot is empty', 'this slot has gear we did not read', and 'we have no doll shot'.
-- gandalf sec 7: if an early affix proves unreadable, DROP THE SLOT, never infer it.
-- 'occupied-unread' is what that drop looks like, and it is not a validation error.
CREATE TABLE IF NOT EXISTS character_gear_slot (
  character_id    TEXT NOT NULL REFERENCES fixture_character(character_id),
  slot            TEXT NOT NULL,
  slot_state      TEXT NOT NULL CHECK (slot_state IN
                    ('read','empty','occupied-unread','not-captured','unknown')),
  item_name       TEXT,
  item_rarity     TEXT,
  item_record     TEXT,
  affixes_json    TEXT,
  affix_completeness TEXT NOT NULL DEFAULT 'unknown'
      CHECK (affix_completeness IN ('complete','partial','none-read','not-applicable','unknown')),
  read_method     TEXT NOT NULL REFERENCES read_method_dict(read_method),
  capture_id      TEXT REFERENCES capture(capture_id),
  notes           TEXT,
  PRIMARY KEY (character_id, slot)
);
"""

# ---------------------------------------------------------------------------
# rebuilds: three tables whose CHECK / UNIQUE constraints are wrong for this run
# ---------------------------------------------------------------------------

CAPTURE_NEW = r"""
CREATE TABLE capture_new (
  capture_id   TEXT PRIMARY KEY,
  session_id   TEXT NOT NULL REFERENCES fixture_session(session_id),
  path         TEXT NOT NULL,
  -- v0.3: path was documented 'repo-relative'. A 13 GB session MP4 will never be in
  -- the repo. storage_root names the anchor so path stays relative to SOMETHING stated.
  storage_root TEXT NOT NULL DEFAULT 'repo',
  -- v0.3: kind was carrying two axes at once (content role AND media type).
  -- media_kind is now the media axis; kind stays the content-role axis.
  media_kind   TEXT NOT NULL DEFAULT 'still'
                 CHECK (media_kind IN ('still','video','video-frame','text-log','other')),
  kind         TEXT NOT NULL CHECK (kind IN
                 ('playstats-panel','console-log','world-view','character-sheet',
                  'trial-frame','video-session','equipment-doll','skill-tree',
                  'nameplate-tooltip','other')),
  label        TEXT,
  sha256       TEXT NOT NULL,
  mtime_utc    TEXT,
  -- v0.3: v0.1 documented mtime as TRANSFER time. For the GP run it is demonstrably
  -- CAPTURE time (it aligns to the video timeline at four independent points). Same
  -- column, two meanings; this column says which.
  mtime_semantics TEXT NOT NULL DEFAULT 'unknown'
                 CHECK (mtime_semantics IN ('capture-time-attested','transfer-time','unknown')),
  mtime_epoch  REAL,
  pts_ms       INTEGER,
  pts_method   TEXT,
  pts_uncertainty_ms INTEGER,
  play_time_ms INTEGER,
  play_time_method TEXT,
  play_time_uncertainty_ms INTEGER,
  burst_id     TEXT,
  burst_ordinal INTEGER,
  duration_s   REAL,
  parent_capture_id TEXT REFERENCES capture(capture_id),
  pixel_w INTEGER, pixel_h INTEGER,
  notes        TEXT
);
"""
CAPTURE_COPY = """
INSERT INTO capture_new (capture_id,session_id,path,kind,label,sha256,mtime_utc,pixel_w,pixel_h,notes,
                         storage_root,media_kind,mtime_semantics)
SELECT capture_id,session_id,path,kind,label,sha256,mtime_utc,pixel_w,pixel_h,notes,
       'repo','still','transfer-time' FROM capture;
"""

TRIAL_NEW = r"""
CREATE TABLE fixture_trial_new (
  trial_id       TEXT PRIMARY KEY,
  fixture_set_id TEXT NOT NULL REFERENCES fixture_set(fixture_set_id),
  trial_ordinal  INTEGER NOT NULL,
  lane           TEXT NOT NULL CHECK (lane IN ('gd-live','sim')),
  -- v0.3: THREE segmentations coexist over ONE ledger (protocol sec 4.5). They are
  -- three WINDOWINGS, not three datasets. segmentation therefore joins the unique key -
  -- without it, S1 trial 7 and S2 trial 7 of the same set collide.
  -- 'S0-explicit' is the L0 rows: hand-bracketed by Matt's before/after screenshots.
  -- Calling those S1 would be a lie; no kill-to-kill rule produced them.
  segmentation   TEXT NOT NULL DEFAULT 'S0-explicit'
                   CHECK (segmentation IN ('S0-explicit','S1-kill-to-kill',
                                           'S2-combat-window','S3-per-entity')),
  segmentation_params TEXT,            -- JSON, e.g. {"idle_gap_s": 3.0}; NOT a constant
  outcome        TEXT CHECK (outcome IN
                   ('monster-killed','player-died','monster-fled','aborted','timeout',
                    'no-fight-baseline')),
  t_start_playtime_s INTEGER,
  t_end_playtime_s   INTEGER,
  t_start_playtime_ms INTEGER,
  t_end_playtime_ms   INTEGER,
  t_start_pts_ms INTEGER,
  t_end_pts_ms   INTEGER,
  before_capture_id  TEXT REFERENCES capture(capture_id),
  after_capture_id   TEXT REFERENCES capture(capture_id),
  monster_entity_id  TEXT,
  contaminated       INTEGER NOT NULL DEFAULT 0,
  contamination_reason TEXT,
  -- a trial that straddles a death / zone transition / epoch boundary must be
  -- excluded from any continuous-series fit. Naming the break makes that a JOIN.
  spans_break_id TEXT REFERENCES session_break(break_id),
  derived_from_ledger INTEGER NOT NULL DEFAULT 0,
  notes TEXT,
  UNIQUE (fixture_set_id, segmentation, trial_ordinal)
);
"""
TRIAL_COPY = """
INSERT INTO fixture_trial_new (trial_id,fixture_set_id,trial_ordinal,lane,outcome,
  t_start_playtime_s,t_end_playtime_s,before_capture_id,after_capture_id,
  monster_entity_id,contaminated,contamination_reason,notes,segmentation,derived_from_ledger)
SELECT trial_id,fixture_set_id,trial_ordinal,lane,outcome,
  t_start_playtime_s,t_end_playtime_s,before_capture_id,after_capture_id,
  monster_entity_id,contaminated,contamination_reason,notes,'S0-explicit',0
FROM fixture_trial;
"""

SET_NEW = r"""
CREATE TABLE fixture_set_new (
  fixture_set_id     TEXT PRIMARY KEY,
  session_id         TEXT NOT NULL REFERENCES fixture_session(session_id),
  character_id       TEXT NOT NULL REFERENCES fixture_character(character_id),
  -- v0.3: 'GP' added. See evidence_class below - the two are NOT the same axis.
  ladder_rung        TEXT NOT NULL CHECK (ladder_rung IN ('L0','L1','L2','L3','L4','L5','GP')),
  -- v0.3: a general-play set is not a rung on the L0-L5 constraint ladder; it holds
  -- none of L0's constraints by construction. It is a different GRADE of evidence.
  evidence_class     TEXT NOT NULL DEFAULT 'ladder-calibration'
                       CHECK (evidence_class IN ('ladder-calibration','distribution-sample')),
  monster_record     TEXT,
  monster_display_name TEXT,
  monster_identity_method TEXT NOT NULL CHECK (monster_identity_method IN
                       ('spawn-command-verbatim','screenshot-nameplate','video-frame-nameplate',
                        'area-roster-inference','assumed-unverified')),
  monster_identity_evidence TEXT,
  monster_level      INTEGER,
  monster_level_method TEXT,
  monster_source     TEXT CHECK (monster_source IN ('spawned','world','unknown')),
  pack_size          INTEGER,
  engagement_mode    TEXT CHECK (engagement_mode IN ('pre-aggroed','from-idle','unknown')),
  area_name          TEXT,
  intended_n INTEGER, actual_n INTEGER,
  purpose TEXT,
  monster_record_candidates TEXT,
  monster_bio_record TEXT,
  -- RECORD-derived rank: GD monsterClassification, from the corpus bridge (M4).
  monster_rank TEXT,
  -- v0.3: OBSERVED rank, from nameplate colour (protocol sec 4.3). A DIFFERENT column,
  -- because it has a different provenance and because disagreement between the two is
  -- evidence (an affixed spawn), not an error to be reconciled away. O-7.
  monster_rank_observed TEXT CHECK (monster_rank_observed IN
                       ('normal','champion','hero','boss','unknown') OR monster_rank_observed IS NULL),
  monster_rank_observed_method TEXT,
  monster_rank_observed_evidence TEXT,
  monster_race TEXT,
  monster_record_method TEXT,
  monster_record_evidence TEXT
);
"""
SET_COPY = """
INSERT INTO fixture_set_new (fixture_set_id,session_id,character_id,ladder_rung,monster_record,
  monster_display_name,monster_identity_method,monster_identity_evidence,monster_level,
  monster_level_method,monster_source,pack_size,engagement_mode,area_name,intended_n,actual_n,
  purpose,monster_record_candidates,monster_bio_record,monster_rank,monster_race,
  monster_record_method,monster_record_evidence,evidence_class)
SELECT fixture_set_id,session_id,character_id,ladder_rung,monster_record,
  monster_display_name,monster_identity_method,monster_identity_evidence,monster_level,
  monster_level_method,monster_source,pack_size,engagement_mode,area_name,intended_n,actual_n,
  purpose,monster_record_candidates,monster_bio_record,monster_rank,monster_race,
  monster_record_method,monster_record_evidence,'ladder-calibration'
FROM fixture_set;
"""

# ---------------------------------------------------------------------------
# additive ALTERs
# ---------------------------------------------------------------------------
ALTERS = [
    ("fixture_session", "video_start_epoch", "REAL"),
    ("fixture_session", "video_start_epoch_method", "TEXT"),
    ("fixture_session", "video_start_epoch_uncertainty_s", "REAL"),
    ("fixture_session", "playtime_banked_prefix_s", "REAL"),
    ("fixture_session", "wallclock_seconds", "REAL"),
    ("fixture_session", "playtime_seconds", "REAL"),
    ("fixture_character", "completeness_detail", "TEXT"),
    ("fixture_character", "provenance_gap", "TEXT"),
    ("fixture_character", "epoch_trigger", "TEXT"),
    ("measure_dict", "layer", "TEXT NOT NULL DEFAULT 'observed' "
                              "CHECK (layer IN ('observed','derived'))"),
    ("measure_dict", "derivation", "TEXT"),
    ("measure_dict", "depends_on", "TEXT"),
    ("measure_dict", "ingest_block", "TEXT"),
    ("measure_dict", "block_ref", "TEXT"),
    ("measure_dict", "semantics_status", "TEXT NOT NULL DEFAULT 'settled' "
                                         "CHECK (semantics_status IN ('settled','contested','unknown'))"),
    ("measure_dict", "semantics_note", "TEXT"),
]

# ---------------------------------------------------------------------------
# triggers: the sec 6b block, enforced by the store rather than remembered
# ---------------------------------------------------------------------------
TRIGGERS = r"""
DROP TRIGGER IF EXISTS trg_block_derived_trial_measurement;
CREATE TRIGGER trg_block_derived_trial_measurement
BEFORE INSERT ON trial_measurement
WHEN (SELECT ingest_block FROM measure_dict WHERE measure_key = NEW.measure_key) IS NOT NULL
BEGIN
  SELECT RAISE(ABORT, 'measure_key is INGEST-BLOCKED in measure_dict; see measure_dict.ingest_block');
END;

DROP TRIGGER IF EXISTS trg_block_derived_session_ledger;
CREATE TRIGGER trg_block_derived_session_ledger
BEFORE INSERT ON session_ledger
WHEN (SELECT ingest_block FROM measure_dict WHERE measure_key = NEW.measure_key) IS NOT NULL
BEGIN
  SELECT RAISE(ABORT, 'measure_key is INGEST-BLOCKED in measure_dict; see measure_dict.ingest_block');
END;
"""

# ---------------------------------------------------------------------------
# views: rebuilt so segmentation cannot silently triple-count
# ---------------------------------------------------------------------------
VIEWS = r"""
DROP VIEW IF EXISTS v_trial_wide;
DROP VIEW IF EXISTS v_trial_delta;
DROP VIEW IF EXISTS v_set_spread;
DROP VIEW IF EXISTS v_ledger_continuity;
DROP VIEW IF EXISTS v_differential;
DROP VIEW IF EXISTS v_fixture_bank_certified;
DROP VIEW IF EXISTS v_fixture_bank_certified_clean;
DROP VIEW IF EXISTS v_session_ledger_wide;
DROP VIEW IF EXISTS v_measure_interpretability;
DROP VIEW IF EXISTS v_character_provenance;

CREATE VIEW v_trial_wide AS
SELECT
  t.trial_id, t.fixture_set_id, t.trial_ordinal, t.segmentation, t.lane, t.outcome,
  t.t_start_playtime_s, t.t_end_playtime_s,
  t.t_start_playtime_ms, t.t_end_playtime_ms, t.contaminated, t.spans_break_id,
  MAX(CASE WHEN m.measure_key='play_time'          AND m.phase='before' THEN m.value_num END) AS play_time_before,
  MAX(CASE WHEN m.measure_key='play_time'          AND m.phase='after'  THEN m.value_num END) AS play_time_after,
  MAX(CASE WHEN m.measure_key='kills'              AND m.phase='before' THEN m.value_num END) AS kills_before,
  MAX(CASE WHEN m.measure_key='kills'              AND m.phase='after'  THEN m.value_num END) AS kills_after,
  MAX(CASE WHEN m.measure_key='life_healed'        AND m.phase='before' THEN m.value_num END) AS life_healed_before,
  MAX(CASE WHEN m.measure_key='life_healed'        AND m.phase='after'  THEN m.value_num END) AS life_healed_after,
  MAX(CASE WHEN m.measure_key='max_level_achieved' AND m.phase='before' THEN m.value_num END) AS max_level_before,
  MAX(CASE WHEN m.measure_key='max_level_achieved' AND m.phase='after'  THEN m.value_num END) AS max_level_after,
  MAX(CASE WHEN m.measure_key='hp_current'         AND m.phase='after'  THEN m.value_num END) AS hp_after,
  MAX(CASE WHEN m.measure_key='fight_seconds'      AND m.phase='during' THEN m.value_num END) AS fight_seconds_lo,
  MAX(CASE WHEN m.measure_key='fight_seconds'      AND m.phase='during' THEN COALESCE(m.value_num_hi,m.value_num) END) AS fight_seconds_hi,
  MAX(CASE WHEN m.measure_key='hp_cost_abs'        AND m.phase='during' THEN m.value_num END) AS hp_cost_lo,
  MAX(CASE WHEN m.measure_key='hp_cost_abs'        AND m.phase='during' THEN COALESCE(m.value_num_hi,m.value_num) END) AS hp_cost_hi,
  MAX(CASE WHEN m.measure_key='skill_use_count' AND m.measure_subkey LIKE '%defaultweaponattack%' AND m.phase='before' THEN m.value_num END) AS weaponattack_before,
  MAX(CASE WHEN m.measure_key='skill_use_count' AND m.measure_subkey LIKE '%defaultweaponattack%' AND m.phase='after'  THEN m.value_num END) AS weaponattack_after
FROM fixture_trial t LEFT JOIN trial_measurement m USING (trial_id)
GROUP BY t.trial_id;

CREATE VIEW v_trial_delta AS
SELECT
  b.trial_id, t.segmentation, b.measure_key, b.measure_subkey,
  a.value_num - b.value_num AS delta,
  b.value_num AS before_value, a.value_num AS after_value,
  CASE WHEN b.read_method = a.read_method THEN b.read_method
       ELSE b.read_method || '|' || a.read_method END AS read_method_pair,
  CASE WHEN b.validity_flag='valid' AND a.validity_flag='valid' THEN 'valid'
       ELSE b.validity_flag || '|' || a.validity_flag END AS validity_pair
FROM trial_measurement b
JOIN trial_measurement a
  ON a.trial_id = b.trial_id AND a.measure_key = b.measure_key
 AND a.measure_subkey = b.measure_subkey AND a.phase='after'
JOIN fixture_trial t ON t.trial_id = b.trial_id
WHERE b.phase='before';

-- v0.3: segmentation joins the GROUP BY. Without it, once S1/S2/S3 coexist over one
-- ledger this view averages three windowings of the same kills into one 'spread'.
CREATE VIEW v_set_spread AS
SELECT
  t.fixture_set_id, t.segmentation, d.measure_key, d.measure_subkey,
  COUNT(*) AS n,
  MIN(d.delta) AS min_delta, MAX(d.delta) AS max_delta,
  AVG(d.delta) AS mean_delta,
  MAX(d.delta) - MIN(d.delta) AS range_delta,
  CASE WHEN COUNT(*) > 1
       THEN SQRT( (SUM(d.delta*d.delta) - COUNT(*)*AVG(d.delta)*AVG(d.delta))
                  / (COUNT(*)-1.0) ) END AS stdev_delta
FROM v_trial_delta d JOIN fixture_trial t USING (trial_id)
GROUP BY t.fixture_set_id, t.segmentation, d.measure_key, d.measure_subkey;

CREATE VIEW v_ledger_continuity AS
SELECT
  s.fixture_set_id, prev.segmentation,
  prev.trial_ordinal AS prev_ordinal, nxt.trial_ordinal AS next_ordinal,
  ma.measure_key, ma.measure_subkey,
  ma.value_num AS after_prev, mb.value_num AS before_next,
  mb.value_num - ma.value_num AS gap_delta,
  md.off_trial_semantics,
  CASE WHEN mb.value_num - ma.value_num = 0 THEN 'continuous'
       WHEN md.off_trial_semantics = 'may-advance' THEN 'expected-advance'
       ELSE 'DISCONTINUOUS' END AS verdict
FROM fixture_trial prev
JOIN fixture_trial nxt
  ON nxt.fixture_set_id = prev.fixture_set_id
 AND nxt.segmentation   = prev.segmentation
 AND nxt.trial_ordinal  = prev.trial_ordinal + 1
JOIN fixture_set s ON s.fixture_set_id = prev.fixture_set_id
JOIN trial_measurement ma ON ma.trial_id = prev.trial_id AND ma.phase='after'
JOIN trial_measurement mb ON mb.trial_id = nxt.trial_id  AND mb.phase='before'
 AND mb.measure_key = ma.measure_key AND mb.measure_subkey = ma.measure_subkey
JOIN measure_dict md ON md.measure_key = ma.measure_key AND md.value_kind='counter'
WHERE ma.read_method <> 'inferred-adjacent-trial'
  AND mb.read_method <> 'inferred-adjacent-trial'
  AND ma.measure_key <> 'play_time';

CREATE VIEW v_differential AS
SELECT
  o.fixture_set_id, o.segmentation, o.measure_key, o.measure_subkey,
  o.n AS oracle_n, o.mean_delta AS oracle_mean, o.min_delta AS oracle_min, o.max_delta AS oracle_max,
  s.n AS sim_n,    s.mean_delta AS sim_mean,    s.min_delta AS sim_min,    s.max_delta AS sim_max,
  s.mean_delta - o.mean_delta AS mean_gap
FROM (SELECT sp.* FROM v_set_spread sp JOIN fixture_set fs USING (fixture_set_id)
      JOIN fixture_session ss USING (session_id) WHERE ss.lane='gd-live') o
JOIN (SELECT sp.* FROM v_set_spread sp JOIN fixture_set fs USING (fixture_set_id)
      JOIN fixture_session ss USING (session_id) WHERE ss.lane='sim') s
  ON s.fixture_set_id = o.fixture_set_id AND s.measure_key = o.measure_key
 AND s.measure_subkey = o.measure_subkey AND s.segmentation = o.segmentation;

CREATE VIEW v_fixture_bank_certified AS
SELECT t.*, s.fixture_set_id AS set_id, s.monster_display_name, s.monster_record,
       s.monster_level, s.evidence_class, s.monster_rank_observed,
       c.character_id AS char_id, c.char_level
FROM fixture_trial t
JOIN fixture_set s        ON s.fixture_set_id = t.fixture_set_id
JOIN fixture_character c  ON c.character_id   = s.character_id
WHERE s.monster_identity_method IN
        ('spawn-command-verbatim','screenshot-nameplate','video-frame-nameplate')
  AND s.monster_level IS NOT NULL
  AND s.monster_level_method IS NOT NULL
  AND c.completeness = 'full-sheet'
  AND t.outcome <> 'no-fight-baseline'
  AND t.spans_break_id IS NULL
  AND NOT EXISTS (
        SELECT 1 FROM trial_measurement m1
        JOIN fixture_trial t2 ON t2.trial_id = m1.trial_id
        JOIN trial_measurement m2 ON m2.trial_id = t2.trial_id
        WHERE t2.fixture_set_id = s.fixture_set_id
          AND m1.measure_key='max_level_achieved' AND m2.measure_key='max_level_achieved'
          AND m1.value_num <> m2.value_num);

CREATE VIEW v_fixture_bank_certified_clean AS
SELECT * FROM v_fixture_bank_certified WHERE contaminated = 0;

-- v0.3 NEW: the observed ledger as a wide time series, keyed on the GAME-STATE clock.
CREATE VIEW v_session_ledger_wide AS
SELECT
  session_id, play_time_ms, pts_ms,
  MAX(CASE WHEN measure_key='kills'              THEN value_num END) AS kills,
  MAX(CASE WHEN measure_key='deaths'             THEN value_num END) AS deaths,
  MAX(CASE WHEN measure_key='max_level_achieved' THEN value_num END) AS max_level,
  MAX(CASE WHEN measure_key='life_healed'        THEN value_num END) AS life_healed,
  MAX(CASE WHEN measure_key='hp_current'         THEN value_num END) AS hp_current,
  MAX(CASE WHEN measure_key='health_potions_used' THEN value_num END) AS health_potions,
  MIN(cross_check_status) AS weakest_cross_check,
  MIN(COALESCE(read_confidence, 1.0)) AS weakest_confidence,
  COUNT(*) AS n_fields
FROM session_ledger
WHERE validity_flag='valid'
GROUP BY session_id, play_time_ms;

-- v0.3 NEW: what does a measure MEAN in a given session, given that session's controls.
CREATE VIEW v_measure_interpretability AS
SELECT
  s.session_id, md.measure_key, md.layer, md.semantics_status, md.ingest_block,
  md.confounds,
  GROUP_CONCAT(sc.control_key || '=' || sc.held || ' [' || sc.effect_on_measure || ']', '; ')
    AS session_controls
FROM fixture_session s
CROSS JOIN measure_dict md
LEFT JOIN session_control sc
  ON sc.session_id = s.session_id AND sc.affects_measure_key = md.measure_key
GROUP BY s.session_id, md.measure_key;

-- v0.3 NEW: honest inventory of what a character epoch actually has behind it.
CREATE VIEW v_character_provenance AS
SELECT
  c.character_id, c.session_id, c.snapshot_ordinal, c.char_level,
  c.completeness, c.completeness_detail, c.provenance_gap, c.epoch_trigger,
  (SELECT COUNT(*) FROM character_stat cs WHERE cs.character_id=c.character_id) AS n_stats,
  (SELECT COUNT(*) FROM character_stat cs WHERE cs.character_id=c.character_id
     AND cs.read_method='absent') AS n_stats_absent,
  (SELECT COUNT(*) FROM character_gear_slot g WHERE g.character_id=c.character_id) AS n_slots,
  (SELECT COUNT(*) FROM character_gear_slot g WHERE g.character_id=c.character_id
     AND g.slot_state='occupied-unread') AS n_slots_unread,
  (SELECT COUNT(*) FROM character_gear_slot g WHERE g.character_id=c.character_id
     AND g.slot_state='not-captured') AS n_slots_uncaptured
FROM fixture_character c;
"""


def cols(cx, table):
    return {r[1] for r in cx.execute(f"PRAGMA table_info({table})")}


def main():
    if not os.path.exists(DB):
        sys.exit(f"missing {DB}")
    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys=OFF")
    cx.execute("PRAGMA legacy_alter_table=ON")

    # ---- 1. drop views (rebuilds below would break them) -------------------
    for v in ("v_trial_wide", "v_trial_delta", "v_set_spread", "v_ledger_continuity",
              "v_differential", "v_fixture_bank_certified", "v_fixture_bank_certified_clean",
              "v_session_ledger_wide", "v_measure_interpretability", "v_character_provenance"):
        cx.execute(f"DROP VIEW IF EXISTS {v}")

    # ---- 2. new tables -----------------------------------------------------
    cx.executescript(DDL_NEW)
    cx.executemany(
        "INSERT OR REPLACE INTO read_method_dict (read_method,family,is_ocr,needs_confidence,note) "
        "VALUES (?,?,?,?,?)", READ_METHODS)

    # ---- 3. additive ALTERs ------------------------------------------------
    for tbl, col, decl in ALTERS:
        if col not in cols(cx, tbl):
            cx.execute(f"ALTER TABLE {tbl} ADD COLUMN {col} {decl}")

    # ---- 4. three rebuilds -------------------------------------------------
    for new_ddl, copy_sql, name in (
            (CAPTURE_NEW, CAPTURE_COPY, "capture"),
            (TRIAL_NEW,   TRIAL_COPY,   "fixture_trial"),
            (SET_NEW,     SET_COPY,     "fixture_set")):
        if "segmentation" in cols(cx, name) or "storage_root" in cols(cx, name) \
                or "evidence_class" in cols(cx, name):
            continue  # already rebuilt (idempotent)
        n_before = cx.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        cx.execute(f"DROP TABLE IF EXISTS {name}_new")
        cx.executescript(new_ddl)
        cx.executescript(copy_sql)
        cx.execute(f"DROP TABLE {name}")
        cx.execute(f"ALTER TABLE {name}_new RENAME TO {name}")
        n_after = cx.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        assert n_before == n_after, f"{name}: {n_before} -> {n_after}"
        print(f"  rebuilt {name}: {n_after} rows preserved")

    # ---- 5. derived-layer registry + the sec 6b block ----------------------
    cx.execute("""UPDATE measure_dict SET
        semantics_status='contested',
        semantics_note='gandalf verification sec 6b: 692 skill uses against 882 kills '
          || '(0.78/kill). Unresolved whether the panel counts SWINGS or ACTIVATIONS. '
          || 'werewolf1_skill01_claws at 358 uses over 113 min is ~3.2/min - implausibly low '
          || 'for a primary attack. RAW per-skill counts remain ingestable as OBSERVED values; '
          || 'any derived attack-rate is blocked. galadriel settling empirically.'
        WHERE measure_key='skill_use_count'""")
    cx.execute("""UPDATE measure_dict SET
        semantics_status='unknown',
        semantics_note='Reads 0.00 for the entire GP run. gandalf D-3: dead field, do not model.'
        WHERE measure_key='dps_field'""")
    cx.execute("""UPDATE measure_dict SET
        semantics_status='unknown',
        semantics_note='Reads 0 for the entire GP run. gandalf D-3: dead field, do not model.'
        WHERE measure_key='total_score'""")
    cx.executemany("""INSERT OR REPLACE INTO measure_dict
        (measure_key,label,unit,value_kind,panel_field,lane_availability,
         ladder_rung_introduced,definition,confounds,off_trial_semantics,
         layer,derivation,depends_on,ingest_block,block_ref,semantics_status,semantics_note)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", [
        ("attacks_per_kill", "Attacks per kill", "count/kill", "gauge", None, "both", "GP",
         "skill_use_count delta over a segmentation window, divided by the kills delta over "
         "the same window.",
         "AoE multi-kill inflates the denominator; pet/DoT/retaliation kills increment kills "
         "with no player activation; the counter may register activations rather than swings.",
         "trial-scoped", "derived",
         "delta(skill_use_count, window) / delta(kills, window)",
         '["skill_use_count","kills"]',
         "BLOCKED. Do not ingest. skill_use_count semantics are unresolved (gandalf "
         "verification sec 6b); an attack-rate derived from a contested numerator would be "
         "wrong by an unknown multiplicative factor and would not announce itself. Unblock "
         "by clearing this column once galadriel's swings-vs-activations verdict lands.",
         "gandalf/notes/2026-07-26-gd-playtest-v1-artifact-verification.md sec 6b",
         "contested", "Blocked at the store, not in a document."),
        ("kills_per_minute", "Kills per minute", "count/min", "gauge", None, "both", "GP",
         "kills delta divided by PLAY_TIME delta - never by video-offset delta.",
         "Video-offset denominators absorb ~73 s of frozen loading time across this run and "
         "bias every rate computed over 882 kills.",
         "trial-scoped", "derived",
         "delta(kills, window) / (delta(play_time_ms, window)/60000)",
         '["kills","play_time"]', None, None, "settled", None),
        ("hp_fraction", "HP globe fraction", "frac", "gauge", "hp globe", "oracle-only", "GP",
         "hp_current / hp_max as read from the orb numerals.",
         "Fill-fraction pixel reading is REJECTED (galadriel calibration 2026-07-26, 4.6 pp "
         "signal vs a 90.5 pp null band). Numerals only.",
         "may-advance", "derived", "hp_current / hp_max", '["hp_current","hp_max"]',
         None, None, "settled", None),
        ("area_name", "Current area", None, "categorical", "world/map", "oracle-only", "GP",
         "The named zone the player is in. A covariate on monster level and pack composition.",
         "Unlabelled area transitions make a level drift look like a variance.",
         "may-advance", "observed", None, None, None, None, "settled", None),
        ("monster_count_visible", "Visible hostiles", "count", "gauge", None, "oracle-only", "GP",
         "Hostiles on screen at a sample. The target-count term sec 6b explanation 1 needs.",
         "Occlusion, off-screen pack members.",
         "may-advance", "observed", None, None, None, None, "unknown",
         "Not yet extracted by any pipeline. Registered so the AoE multi-kill hypothesis has "
         "a place to land."),
    ])

    # ---- 6. triggers + views ----------------------------------------------
    cx.executescript(TRIGGERS)
    cx.executescript(VIEWS)

    # M4 applied its seven ALTERs but never wrote its schema_meta row, so the version
    # ledger skipped v0.2. Backfilled here, flagged as second-hand.
    if not cx.execute("SELECT 1 FROM schema_meta WHERE version='fixtures-v0.2'").fetchone():
        cx.execute("INSERT INTO schema_meta (version,applied_utc,note) VALUES (?,?,?)", (
            "fixtures-v0.2", "2026-07-26T14:41:28+00:00",
            "M4 tag-bridge. BACKFILLED BY M5 (elrond, 2026-07-26): "
            "gd_bridge_m3_bridge_and_fixtures_2026_07_26.py applied the seven ALTERs and the "
            "monster_record UPDATE but never wrote its schema_meta row, so the version ledger "
            "skipped v0.2. applied_utc is taken from the backup filename "
            "fixtures.db.pre-v0.2-20260726T144128Z-backup and is therefore the PRE-migration "
            "instant, not an independent timestamp. Recorded so the ledger is contiguous; "
            "flagged so it is not mistaken for a first-hand record."))

    cx.execute("INSERT INTO schema_meta (version,applied_utc,note) VALUES (?,?,?)", (
        VERSION,
        __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "M5. Session-ledger layer split from the trial layer; play_time_ms as join key; "
        "clock_map/clock_anchor; session_break; session_control; character_gear_slot; "
        "read_method_dict; observed/derived split with attacks_per_kill INGEST-BLOCKED "
        "pending gandalf sec 6b. Rebuilt capture / fixture_trial / fixture_set. "
        "Applied by fixtures_m5_v0_3_schema_2026_07_26.py."))
    cx.commit()

    cx.execute("PRAGMA foreign_keys=ON")
    bad = cx.execute("PRAGMA foreign_key_check").fetchall()
    print("foreign_key_check:", "CLEAN" if not bad else bad[:5])
    print("integrity_check:", cx.execute("PRAGMA integrity_check").fetchone()[0])
    for v in cx.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name"):
        n = cx.execute(f"SELECT COUNT(*) FROM {v[0]}").fetchone()[0]
        print(f"  view {v[0]}: {n} rows")
    print("certified view:", cx.execute(
        "SELECT COUNT(*) FROM v_fixture_bank_certified").fetchone()[0], "(expect 3)")
    cx.close()


if __name__ == "__main__":
    main()
