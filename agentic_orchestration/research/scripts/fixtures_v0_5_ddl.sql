-- fixtures-v0.5 — the MEASURED-FIXTURE layer
-- M8, elrond, 2026-07-28. KIT-CAL-1 run KC1-2026-07-27 phase P-1 (G-3).
--
-- What this schema is for, said plainly:
--   A play session was recorded. Two independent OCR readers walked the footage:
--   one reading the stats PANEL (T-A, counters at 0.5 s), one reading the health
--   GLOBE (T-B, HP numerals at 15 fps inside engagement windows). Those two series
--   are the measurement. Everything above them -- engagements, regimes, the fixture,
--   the rollup -- is a PARTITION of those series, and every partition is named, dated,
--   and replaceable without touching the series underneath it.
--
-- Four things this schema refuses to let a consumer do:
--   1. Pool the regimes. There is no 'ALL' regime. regime_stat is keyed on a
--      session_regime row and session_regime holds only real build-stable spans.
--   2. Read a coverage-bearing figure without its coverage. measure_dict.requires_coverage
--      + two ABORT triggers make a NULL coverage on such a figure unrepresentable.
--   3. Overwrite a segmentation. A re-cut is a NEW segmentation_run; the old rows stay
--      readable and every engagement names the run it belongs to.
--   4. Take a figure without its declared conditions. fixture_condition is scoped and
--      the consumer views join it in.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- 1. session_regime -- a contiguous span of a session over which build identity holds
-- ---------------------------------------------------------------------------
-- A regime is NOT a convenience bucket. It is the assertion "across this play_time
-- span the thing being measured did not change." Verdict sec 3: a pooled fit across
-- three regimes describes a run that never happened.

CREATE TABLE IF NOT EXISTS session_regime (
  regime_id        TEXT PRIMARY KEY,               -- '<session_id>/R2'
  session_id       TEXT NOT NULL REFERENCES fixture_session(session_id),
  regime_key       TEXT NOT NULL,                  -- 'R1' | 'R2' | 'R3'
  regime_ordinal   INTEGER NOT NULL,
  -- half-open [lo, hi) on the GAME-STATE clock. play_time is the join key, always.
  play_time_s_lo   INTEGER NOT NULL,
  play_time_s_hi   INTEGER NOT NULL,
  build_label      TEXT NOT NULL,                  -- 'four-skill pre-transform' etc.
  build_break_evidence TEXT,                       -- how the boundary was located
  boundary_grade   TEXT NOT NULL CHECK (boundary_grade IN
                     ('MEASURED','DERIVED','INFERRED','ATTESTED','UNVERIFIED')),
  -- headline counts as banked by the segmentation of record; recomputed at verify time
  kills            INTEGER,
  engagements      INTEGER,
  char_level_lo    INTEGER,
  char_level_hi    INTEGER,
  -- 'fixture' | 'secondary' | 'report-only'. Verdict sec 3 + ruling R-KC1-2.
  distribution_role TEXT NOT NULL CHECK (distribution_role IN
                     ('fixture','secondary','report-only')),
  distribution_role_rationale TEXT,
  source_ref       TEXT,
  notes            TEXT,
  UNIQUE (session_id, regime_key)
);

-- ---------------------------------------------------------------------------
-- 2. segmentation_run -- a NAMED cut of a session into engagements
-- ---------------------------------------------------------------------------
-- The re-ingestion tolerance lives here. G-2b may rule a different grain (HALT H-1).
-- When it does, that is a new row with status='current' and this one flips to
-- 'superseded' + superseded_by. No engagement row is ever edited in place, and any
-- consumer that pinned a segmentation_id keeps reading exactly what it read before.

CREATE TABLE IF NOT EXISTS segmentation_run (
  segmentation_id  TEXT PRIMARY KEY,               -- '<session_id>/S1-gap5s-v1'
  session_id       TEXT NOT NULL REFERENCES fixture_session(session_id),
  segmentation     TEXT NOT NULL CHECK (segmentation IN
                     ('S0-explicit','S1-kill-to-kill','S2-combat-window','S3-per-entity')),
  rule_text        TEXT NOT NULL,
  params_json      TEXT NOT NULL,                  -- {"gap_threshold_s":5.0,"pad_s":3.0}
  derived_from     TEXT NOT NULL,                  -- the series this cut was made on
  n_engagements    INTEGER,
  n_kills          INTEGER,
  dur_median_s     REAL, dur_mean_s REAL, dur_max_s REAL,
  authored_by      TEXT NOT NULL,
  authored_date    TEXT NOT NULL,
  ruling_ref       TEXT,                           -- e.g. 'verdict sec 4 / HALT H-1'
  status           TEXT NOT NULL CHECK (status IN ('current','superseded','candidate')),
  superseded_by    TEXT REFERENCES segmentation_run(segmentation_id),
  reproduction_note TEXT,
  source_ref       TEXT
);

-- ---------------------------------------------------------------------------
-- 3. fixture_trial extensions -- the engagement grain
-- ---------------------------------------------------------------------------
-- M7 already made fixture_trial able to hold a pack engagement (fixture_set_id
-- NULLABLE, session_id the real parent). v0.5 adds only the two pointers an
-- engagement needs: which cut produced it, and which regime it fell in.

ALTER TABLE fixture_trial ADD COLUMN segmentation_id TEXT
  REFERENCES segmentation_run(segmentation_id);
ALTER TABLE fixture_trial ADD COLUMN regime_id TEXT
  REFERENCES session_regime(regime_id);

DROP INDEX IF EXISTS ux_trial_ledger_scoped;
-- Re-keyed on segmentation_id: two cuts of the same session can both hold an 'e007'.
CREATE UNIQUE INDEX ux_trial_ledger_scoped
  ON fixture_trial (session_id, COALESCE(segmentation_id, segmentation), trial_ordinal)
  WHERE fixture_set_id IS NULL;
CREATE INDEX IF NOT EXISTS ix_trial_regime ON fixture_trial (regime_id, segmentation_id);

-- ---------------------------------------------------------------------------
-- 4. coverage becomes structurally non-optional
-- ---------------------------------------------------------------------------
ALTER TABLE measure_dict ADD COLUMN requires_coverage INTEGER NOT NULL DEFAULT 0;

-- trial_measurement is REBUILT rather than ALTERed, to close a live drift defect:
-- its inline read_method CHECK froze the v0.1 nine-value list, while read_method_dict
-- has since grown to fifteen (video-frame-ocr, video-frame-human, mtime-arithmetic,
-- derived-from-anchor, container-origin, video-frame-ocr-rejected). A CHECK that
-- disagrees with the dictionary it shadows will silently force honest provenance into
-- a wrong bucket -- exactly the transformation this store forbids. The CHECK becomes
-- an FK to the dictionary, so the two cannot drift again.
DROP TRIGGER IF EXISTS trg_block_derived_trial_measurement;
ALTER TABLE trial_measurement RENAME TO trial_measurement_pre_v0_5;
CREATE TABLE trial_measurement (
  trial_id      TEXT NOT NULL REFERENCES fixture_trial(trial_id),
  measure_key   TEXT NOT NULL REFERENCES measure_dict(measure_key),
  measure_subkey TEXT NOT NULL DEFAULT '',
  phase         TEXT NOT NULL CHECK (phase IN ('before','after','during','derived')),
  value_num     REAL,
  value_num_hi  REAL,
  value_text    TEXT,
  unit          TEXT,
  read_method   TEXT NOT NULL REFERENCES read_method_dict(read_method),
  uncertainty_abs REAL,
  capture_id    TEXT REFERENCES capture(capture_id),
  verbatim      TEXT,
  validity_flag TEXT NOT NULL DEFAULT 'valid'
                  CHECK (validity_flag IN ('valid','window-expired','superseded','suspect')),
  validity_note TEXT,
  coverage      REAL,
  coverage_basis TEXT,
  evidence_grade TEXT CHECK (evidence_grade IN
                  ('MEASURED','DERIVED','INFERRED','ATTESTED','UNVERIFIED') OR evidence_grade IS NULL),
  PRIMARY KEY (trial_id, measure_key, measure_subkey, phase)
);
INSERT INTO trial_measurement
  (trial_id, measure_key, measure_subkey, phase, value_num, value_num_hi, value_text,
   unit, read_method, uncertainty_abs, capture_id, verbatim, validity_flag, validity_note)
SELECT trial_id, measure_key, measure_subkey, phase, value_num, value_num_hi, value_text,
       unit, read_method, uncertainty_abs, capture_id, verbatim, validity_flag, validity_note
FROM trial_measurement_pre_v0_5;
DROP TABLE trial_measurement_pre_v0_5;
CREATE TRIGGER trg_block_derived_trial_measurement
BEFORE INSERT ON trial_measurement
WHEN (SELECT ingest_block FROM measure_dict WHERE measure_key = NEW.measure_key) IS NOT NULL
BEGIN
  SELECT RAISE(ABORT, 'measure_key is INGEST-BLOCKED in measure_dict; see measure_dict.ingest_block');
END;

CREATE TRIGGER trg_require_coverage_trial_measurement
BEFORE INSERT ON trial_measurement
WHEN (SELECT requires_coverage FROM measure_dict WHERE measure_key = NEW.measure_key) = 1
 AND NEW.coverage IS NULL
BEGIN
  SELECT RAISE(ABORT,
    'measure_key requires_coverage=1: a coverage-bearing figure may not be stored without its coverage');
END;

-- ---------------------------------------------------------------------------
-- 5. panel_series_sample / panel_series_reading -- the T-A series (0.5 s, stats panel)
-- ---------------------------------------------------------------------------
-- Kept OUT of session_ledger deliberately. session_ledger is the sparse, capture-anchored
-- hand/screenshot layer (49 rows keyed on capture_id). This is a dense video-OCR series
-- keyed on pts with per-field refusal semantics. Same measures, different provenance,
-- different density, different failure modes. v_session_reading_all unions them and
-- labels the layer, so a cross-layer query is one view away and the two never silently mix.

CREATE TABLE IF NOT EXISTS panel_series_sample (
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  series          TEXT NOT NULL,                  -- 'T-A-panel'
  sample_ordinal  INTEGER NOT NULL,               -- the reader's frame index i
  pts_ms          INTEGER NOT NULL,               -- CAMERA clock. Retrieval only.
  play_time_ms    INTEGER,                        -- GAME clock. THE JOIN KEY. NULL = refusal.
  play_time_read_status TEXT NOT NULL CHECK (play_time_read_status IN
                    ('accepted','rejected-nonmonotonic','missing')),
  play_time_raw   REAL,                           -- the reader's raw read, kept when rejected
  play_time_confidence REAL,
  frame_status    TEXT,                         -- the reader's own frame verdict ('OK', ...)
  panel_luma      INTEGER,                        -- reader gate signal, banked verbatim
  regime_id       TEXT REFERENCES session_regime(regime_id),
  PRIMARY KEY (session_id, series, sample_ordinal)
);
CREATE INDEX IF NOT EXISTS ix_panel_sample_pt
  ON panel_series_sample (session_id, play_time_ms);
CREATE INDEX IF NOT EXISTS ix_panel_sample_pts
  ON panel_series_sample (session_id, pts_ms);

CREATE TABLE IF NOT EXISTS panel_series_reading (
  session_id      TEXT NOT NULL,
  series          TEXT NOT NULL,
  sample_ordinal  INTEGER NOT NULL,
  measure_key     TEXT NOT NULL REFERENCES measure_dict(measure_key),
  measure_subkey  TEXT NOT NULL DEFAULT '',       -- skill .dbr leaf for skill_use_count
  -- read_status is the whole point of this table. 'accepted' = passed the monotonic
  -- gate. 'rejected-nonmonotonic' = the reader SAW a value and the gate refused it;
  -- value_raw preserves it. A field ABSENT for a sample_ordinal is a REFUSAL (the
  -- reader returned nothing) -- never interpolated, and counted in series_field_quality.
  read_status     TEXT NOT NULL CHECK (read_status IN ('accepted','rejected-nonmonotonic')),
  value_num       REAL,                           -- NULL when rejected
  value_raw       REAL NOT NULL,                  -- ALWAYS the reader's raw read. Reversibility.
  read_confidence REAL,
  path_corr       REAL,                           -- skill-icon path correlation, where emitted
  PRIMARY KEY (session_id, series, sample_ordinal, measure_key, measure_subkey)
);
CREATE INDEX IF NOT EXISTS ix_panel_reading_measure
  ON panel_series_reading (session_id, measure_key, measure_subkey, sample_ordinal);

-- ---------------------------------------------------------------------------
-- 6. globe_series_frame -- the T-B series (15 fps, health-globe numerals)
-- ---------------------------------------------------------------------------
-- One row per DECODED frame including refusals, because the refusal code is the
-- coverage. 19,348 rows; 2,165 of them carry hp IS NULL and a named refusal code.

CREATE TABLE IF NOT EXISTS globe_series_frame (
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  series          TEXT NOT NULL,                  -- 'T-B-globe'
  pts_ms          INTEGER NOT NULL,
  hp_current      REAL,                           -- NULL = refusal
  hp_raw          REAL,
  read_confidence REAL,
  refusal_code    TEXT NOT NULL,                  -- 'OK'|'NODIG'|'FLASH'|'LOWCONF'|'TRUNC'|...
  reader_path     TEXT NOT NULL CHECK (reader_path IN ('validated','greedy-fallback')),
  eng_id          INTEGER NOT NULL,               -- window this frame was decoded FOR
  trial_id        TEXT REFERENCES fixture_trial(trial_id),
  -- eng_id is IN the key on purpose. 48 frames sit inside two adjacent padded windows
  -- and were decoded twice, once per window. Keying on pts alone would silently drop
  -- one copy and quietly change a window's coverage denominator.
  PRIMARY KEY (session_id, series, eng_id, pts_ms)
);
CREATE INDEX IF NOT EXISTS ix_globe_pts ON globe_series_frame (session_id, pts_ms);
CREATE INDEX IF NOT EXISTS ix_globe_trial ON globe_series_frame (trial_id);
CREATE INDEX IF NOT EXISTS ix_globe_code  ON globe_series_frame (session_id, refusal_code);

-- ---------------------------------------------------------------------------
-- 7. series_field_quality -- ONE quality ledger, three grains
-- ---------------------------------------------------------------------------
-- Same columns whether you ask about the run, a regime, or a single engagement.
-- This is where life_healed's non-monotonic rejection rate lives, as counts rather
-- than as a rate, so no consumer inherits somebody else's choice of denominator.

CREATE TABLE IF NOT EXISTS series_field_quality (
  scope_kind      TEXT NOT NULL CHECK (scope_kind IN ('session','regime','engagement')),
  scope_ref       TEXT NOT NULL,                  -- session_id | regime_id | trial_id
  series          TEXT NOT NULL,                  -- 'T-A-panel' | 'T-B-globe'
  measure_key     TEXT NOT NULL,
  measure_subkey  TEXT NOT NULL DEFAULT '',
  n_samples       INTEGER NOT NULL,               -- frames the reader was asked to read
  n_present       INTEGER NOT NULL,               -- reader returned a value
  n_accepted      INTEGER NOT NULL,               -- value survived the gate
  n_rejected_nonmonotonic INTEGER NOT NULL DEFAULT 0,
  n_missing       INTEGER NOT NULL DEFAULT 0,     -- refusals
  n_greedy_path   INTEGER,
  refusal_hist_json TEXT,
  unreadable_break_s REAL,
  -- The DELTA family has its own numerator and denominator, and they are NOT the frame
  -- counts above. Frame coverage = frames returning an accepted read / frames decoded,
  -- and it is what the totals gate (>= 0.80) is defined on. Delta coverage =
  -- covered_s / wallclock_s = admissible PAIR-time, and it is what a rate is per. The
  -- two differ (R2 62 vs 63 engagements pass at 0.80). Storing one and calling it
  -- 'coverage' would silently change which engagements are in a total.
  covered_s       REAL,
  wallclock_s     REAL,
  source_ref      TEXT,
  PRIMARY KEY (scope_kind, scope_ref, series, measure_key, measure_subkey)
);

-- ---------------------------------------------------------------------------
-- 8. regime_stat -- the rollup grain gamora's harness reads
-- ---------------------------------------------------------------------------
-- Keyed on regime_id: a pooled row is UNREPRESENTABLE, because there is no pooled
-- regime to point at. stat_family separates 'totals' (coverage-gated engagements,
-- a fragment is not a total) from 'rates' (per COVERED second, wider inclusion).
-- galadriel sec 6: the two families are reported side by side and never mixed.

CREATE TABLE IF NOT EXISTS regime_stat (
  segmentation_id TEXT NOT NULL REFERENCES segmentation_run(segmentation_id),
  regime_id       TEXT NOT NULL REFERENCES session_regime(regime_id),
  stat_family     TEXT NOT NULL CHECK (stat_family IN
                    ('totals','rates','drops','damage','frames','counts')),
  measure_key     TEXT NOT NULL REFERENCES measure_dict(measure_key),
  statistic       TEXT NOT NULL CHECK (statistic IN
                    ('n','mean','median','p10','p50','p90','p99','min','max','sd','total','frac')),
  value_num       REAL,
  unit            TEXT,
  n_included      INTEGER,                        -- engagements the figure was computed over
  n_total         INTEGER,                        -- engagements in the regime
  inclusion_rule  TEXT,                           -- verbatim; e.g. 'coverage >= 0.80'
  coverage        REAL,                           -- regime frame/delta coverage behind it
  coverage_basis  TEXT,
  evidence_grade  TEXT NOT NULL CHECK (evidence_grade IN
                    ('MEASURED','DERIVED','INFERRED','ATTESTED','UNVERIFIED')),
  source_ref      TEXT NOT NULL,
  PRIMARY KEY (segmentation_id, regime_id, stat_family, measure_key, statistic)
);

CREATE TRIGGER trg_require_coverage_regime_stat
BEFORE INSERT ON regime_stat
WHEN (SELECT requires_coverage FROM measure_dict WHERE measure_key = NEW.measure_key) = 1
 AND NEW.coverage IS NULL
BEGIN
  SELECT RAISE(ABORT,
    'measure_key requires_coverage=1: a regime figure may not be stored without its coverage');
END;

-- ---------------------------------------------------------------------------
-- 9. measured_fixture / fixture_target -- what the sim is held accountable TO
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS measured_fixture (
  fixture_id      TEXT PRIMARY KEY,               -- 'GD-R2-werewolf'
  session_id      TEXT NOT NULL REFERENCES fixture_session(session_id),
  regime_id       TEXT NOT NULL REFERENCES session_regime(regime_id),
  segmentation_id TEXT NOT NULL REFERENCES segmentation_run(segmentation_id),
  kit_id          TEXT,                           -- 'gd-werewolf-kitcal-1'
  run_id          TEXT NOT NULL,                  -- 'GP-gd-2026-07-26-s1'
  calibration_run TEXT,                           -- 'KC1-2026-07-27'
  fixture_role    TEXT NOT NULL CHECK (fixture_role IN
                    ('primary','secondary','report-only')),
  naming_status   TEXT NOT NULL CHECK (naming_status IN
                    ('matt-ratified','elrond-provisional','proposed')),
  ruling_ref      TEXT,
  charter_ref     TEXT,
  verdict_ref     TEXT,
  evidence_grade  TEXT NOT NULL,
  notes           TEXT
);

CREATE TABLE IF NOT EXISTS fixture_target (
  fixture_id      TEXT NOT NULL REFERENCES measured_fixture(fixture_id),
  target_key      TEXT NOT NULL,                  -- 'ttk_shape','damage_intake', ...
  -- tier is the ruling, made queryable. 'provisional' is NOT a softer 'primary';
  -- it means the run may not band this quantity until the named gate clears.
  tier            TEXT NOT NULL CHECK (tier IN ('primary','provisional','report-only')),
  measure_key     TEXT REFERENCES measure_dict(measure_key),
  stat_family     TEXT,
  rationale       TEXT,
  gate_ref        TEXT,                           -- what must land before tier can change
  ruling_ref      TEXT,
  band_status     TEXT NOT NULL DEFAULT 'unratified'
                    CHECK (band_status IN ('unratified','ratified','waived')),
  band_lo         REAL, band_hi REAL, band_ref TEXT,
  PRIMARY KEY (fixture_id, target_key)
);

-- ---------------------------------------------------------------------------
-- 10. fixture_condition -- the declared holes that travel WITH the figures
-- ---------------------------------------------------------------------------
-- Constraint 3 of the G-3 charge: R3's coverage hole must be a queryable fact,
-- not a footnote. Everything a reader would otherwise have to remember from a
-- prose document is a row here, scoped to what it conditions.

CREATE TABLE IF NOT EXISTS fixture_condition (
  condition_id    TEXT PRIMARY KEY,
  scope_kind      TEXT NOT NULL CHECK (scope_kind IN
                    ('session','regime','engagement','measure','fixture')),
  scope_ref       TEXT NOT NULL,
  condition_kind  TEXT NOT NULL CHECK (condition_kind IN
                    ('coverage-hole','confound','anomaly','control-violation',
                     'resolution-limit','instrument-dead','normalisation-caveat',
                     'sample-size','provisional-ruling')),
  severity        TEXT NOT NULL CHECK (severity IN ('blocking','high','moderate','low','note')),
  headline        TEXT NOT NULL,
  detail          TEXT,
  affects_measure_keys TEXT,                      -- comma-separated; '' = all
  affected_engagement_ids TEXT,
  affected_kills  INTEGER,
  cause           TEXT,
  cause_grade     TEXT CHECK (cause_grade IN
                    ('MEASURED','DERIVED','INFERRED','ATTESTED','UNVERIFIED')),
  recoverable_from_this_footage INTEGER NOT NULL DEFAULT 0,
  remedy          TEXT,
  evidence_ref    TEXT,
  status          TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open','resolved','superseded','accepted')),
  raised_by       TEXT, raised_date TEXT
);
CREATE INDEX IF NOT EXISTS ix_condition_scope ON fixture_condition (scope_kind, scope_ref);

-- ---------------------------------------------------------------------------
-- 11. evidence_claim -- grade as a first-class row, with its upgrade criterion
-- ---------------------------------------------------------------------------
-- MEASURED / ATTESTED / DERIVED / INFERRED / UNVERIFIED are not adjectives here.
-- Each claim names WHO said it, WHEN, and the SPECIFIC empirical criterion that
-- would move it up a grade. A grade with no upgrade criterion is a dead end and
-- says so by leaving the column NULL.

CREATE TABLE IF NOT EXISTS evidence_claim (
  claim_id        TEXT PRIMARY KEY,
  session_id      TEXT REFERENCES fixture_session(session_id),
  subject_kind    TEXT NOT NULL CHECK (subject_kind IN
                    ('control','series','build-identity','measurement','boundary',
                     'anomaly','fixture','instrument')),
  subject_ref     TEXT NOT NULL,
  claim_text      TEXT NOT NULL,
  grade           TEXT NOT NULL CHECK (grade IN
                    ('MEASURED','DERIVED','INFERRED','ATTESTED','UNVERIFIED','REFUTED')),
  method          TEXT,                           -- how it was established
  source          TEXT NOT NULL,
  source_date     TEXT NOT NULL,
  upgrade_criterion TEXT,                         -- EMPIRICAL, never time-passage
  upgrade_gate_ref TEXT,
  upgraded_from   TEXT,
  supersedes      TEXT REFERENCES evidence_claim(claim_id),
  status          TEXT NOT NULL DEFAULT 'current'
                    CHECK (status IN ('current','superseded','withdrawn'))
);

-- ---------------------------------------------------------------------------
-- 12. session_control extensions -- controls carry a grade too
-- ---------------------------------------------------------------------------
ALTER TABLE session_control ADD COLUMN evidence_grade TEXT;
ALTER TABLE session_control ADD COLUMN upgrade_criterion TEXT;
ALTER TABLE session_control ADD COLUMN claim_id TEXT REFERENCES evidence_claim(claim_id);

-- ---------------------------------------------------------------------------
-- 13. Consumer views -- the shapes gamora's harness reads
-- ---------------------------------------------------------------------------

-- 13.1 Engagement grain, regime-stamped, conditions counted.
DROP VIEW IF EXISTS v_engagement_wide;
CREATE VIEW v_engagement_wide AS
SELECT
  t.trial_id, t.session_id, t.segmentation_id, t.regime_id,
  r.regime_key, r.distribution_role, t.trial_ordinal AS eng_id,
  t.t_start_playtime_s, t.t_end_playtime_s, t.outcome, t.contaminated,
  MAX(CASE WHEN m.measure_key='engagement_seconds' THEN m.value_num END) AS dur_s,
  MAX(CASE WHEN m.measure_key='kills' AND m.phase='during' THEN m.value_num END) AS kills,
  MAX(CASE WHEN m.measure_key='intake_hp'   THEN m.value_num END) AS intake_hp,
  MAX(CASE WHEN m.measure_key='intake_hp'   THEN m.coverage  END) AS intake_coverage,
  MAX(CASE WHEN m.measure_key='healed_hp'   THEN m.value_num END) AS healed_hp,
  MAX(CASE WHEN m.measure_key='hp_drop_count' THEN m.value_num END) AS n_drops,
  MAX(CASE WHEN m.measure_key='hp_drop_max' THEN m.value_num END) AS drop_max,
  MAX(CASE WHEN m.measure_key='hp_drop_p50' THEN m.value_num END) AS drop_p50,
  MAX(CASE WHEN m.measure_key='hp_max_observed' THEN m.value_num END) AS hp_max_observed,
  MAX(CASE WHEN m.measure_key='hp_min_observed' THEN m.value_num END) AS hp_min_observed,
  MAX(CASE WHEN m.measure_key='damage_spent' THEN m.value_num END) AS damage_spent,
  MAX(CASE WHEN m.measure_key='damage_spent' THEN m.coverage  END) AS damage_dps_coverage,
  q.n_accepted  AS life_healed_accepted,
  q.n_rejected_nonmonotonic AS life_healed_rejected,
  CASE WHEN q.n_present > 0
       THEN ROUND(1.0*q.n_rejected_nonmonotonic/q.n_present, 5) END AS life_healed_reject_rate_of_present,
  (SELECT COUNT(*) FROM fixture_condition c
    WHERE c.status='open'
      AND ((c.scope_kind='engagement' AND c.scope_ref = t.trial_id)
        OR (c.scope_kind='regime'     AND c.scope_ref = t.regime_id))) AS n_open_conditions
FROM fixture_trial t
JOIN session_regime r ON r.regime_id = t.regime_id
LEFT JOIN trial_measurement m ON m.trial_id = t.trial_id
LEFT JOIN series_field_quality q
       ON q.scope_kind='engagement' AND q.scope_ref = t.trial_id
      AND q.series='T-A-panel' AND q.measure_key='life_healed'
WHERE t.derived_from_ledger = 1
GROUP BY t.trial_id;

-- 13.2 THE fixture surface. Pinned to the ratified fixture row; nothing pooled can
--      reach it, because it is keyed through measured_fixture -> one regime_id.
DROP VIEW IF EXISTS v_fixture_engagements;
CREATE VIEW v_fixture_engagements AS
SELECT f.fixture_id, f.fixture_role, f.kit_id, e.*
FROM measured_fixture f
JOIN v_engagement_wide e
  ON e.regime_id = f.regime_id AND e.segmentation_id = f.segmentation_id;

-- 13.3 A regime figure NEVER leaves this DB without its conditions attached.
DROP VIEW IF EXISTS v_regime_stat_conditioned;
CREATE VIEW v_regime_stat_conditioned AS
SELECT
  s.*, r.regime_key, r.distribution_role,
  (SELECT COUNT(*) FROM fixture_condition c
    WHERE c.status='open' AND c.scope_kind='regime' AND c.scope_ref = s.regime_id
      AND (c.affects_measure_keys = ''
           OR (',' || c.affects_measure_keys || ',') LIKE ('%,' || s.measure_key || ',%'))
  ) AS n_conditions,
  (SELECT GROUP_CONCAT(c.condition_id, ' | ') FROM fixture_condition c
    WHERE c.status='open' AND c.scope_kind='regime' AND c.scope_ref = s.regime_id
      AND (c.affects_measure_keys = ''
           OR (',' || c.affects_measure_keys || ',') LIKE ('%,' || s.measure_key || ',%'))
  ) AS condition_ids,
  (SELECT GROUP_CONCAT(c.headline, ' | ') FROM fixture_condition c
    WHERE c.status='open' AND c.scope_kind='regime' AND c.scope_ref = s.regime_id
      AND (c.affects_measure_keys = ''
           OR (',' || c.affects_measure_keys || ',') LIKE ('%,' || s.measure_key || ',%'))
  ) AS conditions
FROM regime_stat s
JOIN session_regime r ON r.regime_id = s.regime_id;

-- 13.4 The accountability contract, one row per target, tier and band visible.
DROP VIEW IF EXISTS v_fixture_accountability;
CREATE VIEW v_fixture_accountability AS
SELECT f.fixture_id, f.fixture_role, f.kit_id, f.calibration_run,
       t.target_key, t.tier, t.measure_key, t.stat_family,
       t.band_status, t.band_lo, t.band_hi, t.gate_ref, t.ruling_ref, t.rationale
FROM measured_fixture f JOIN fixture_target t USING (fixture_id);

-- 13.5 Two rejection rates, both denominators shown, neither chosen for the reader.
DROP VIEW IF EXISTS v_series_rejection;
CREATE VIEW v_series_rejection AS
SELECT scope_kind, scope_ref, series, measure_key, measure_subkey,
       n_samples, n_present, n_accepted, n_rejected_nonmonotonic, n_missing,
       CASE WHEN n_present > 0
            THEN ROUND(100.0*n_rejected_nonmonotonic/n_present, 3) END AS reject_pct_of_present,
       CASE WHEN n_samples > 0
            THEN ROUND(100.0*n_rejected_nonmonotonic/n_samples, 3) END AS reject_pct_of_samples,
       CASE WHEN n_samples > 0
            THEN ROUND(100.0*n_accepted/n_samples, 3) END AS accepted_pct_of_samples
FROM series_field_quality;

-- 13.6 The two reading layers, unioned and LABELLED. They never silently mix.
DROP VIEW IF EXISTS v_session_reading_all;
CREATE VIEW v_session_reading_all AS
SELECT 'sparse-anchor' AS source_layer, session_id, NULL AS sample_ordinal,
       play_time_ms, pts_ms, measure_key, measure_subkey, value_num,
       read_method, read_confidence, validity_flag AS read_status, capture_id
FROM session_ledger
UNION ALL
SELECT 'T-A-panel-series', p.session_id, p.sample_ordinal,
       s.play_time_ms, s.pts_ms, p.measure_key, p.measure_subkey, p.value_num,
       'screenshot-downscaled', p.read_confidence, p.read_status, NULL
FROM panel_series_reading p
JOIN panel_series_sample s
  ON s.session_id=p.session_id AND s.series=p.series AND s.sample_ordinal=p.sample_ordinal;

-- 13.7 The grade ledger, with what would move each claim.
DROP VIEW IF EXISTS v_evidence_ledger;
CREATE VIEW v_evidence_ledger AS
SELECT claim_id, session_id, subject_kind, subject_ref, grade, claim_text,
       source, source_date, upgrade_criterion, upgrade_gate_ref, status
FROM evidence_claim WHERE status='current'
ORDER BY CASE grade WHEN 'MEASURED' THEN 1 WHEN 'DERIVED' THEN 2 WHEN 'ATTESTED' THEN 3
                    WHEN 'INFERRED' THEN 4 WHEN 'UNVERIFIED' THEN 5 ELSE 6 END, subject_ref;
