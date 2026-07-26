-- fixtures.db — schema fixtures-v0.1
-- Author: elrond (data steward). Commissioner: gandalf (GD program, gap 5).
-- Governing artifacts:
--   elrond/notes/2026-07-25-l0-fixture-schema-draft.md      (v0.1 draft)
--   gandalf/notes/2026-07-25-l0-fixture-schema-review.md    (ACCEPT + rulings O-1..O-10)
-- O-1 ruling: SEPARATE store, not additive tables in corpus.db. Cross-DB joins via ATTACH.
--
-- Landing extensions beyond the reviewed sketch (all additive, all documented in
-- research/curated/MIGRATION-fixtures.md § "Landing extensions"):
--   E1  character_stat            long-form exhaustive character-sheet readings (G-5 per-field)
--   E2  fixture_trial.outcome    += 'no-fight-baseline'  (carries O-10's round-1 panel reading)
--   E3  capture.kind             += 'trial-frame'        (one frame = panel + world + overlay)
--   E4  fixture_set.monster_display_name    (nameplate text; the .dbr is a separate join)
--   E5  fixture_trial.monster_entity_id     (overlay instance id; start=end proves one fight)
--   E6  fixture_character.notes
-- NOT taken: a merged 'anger-overlay+logdata' trace channel. The two channels stay two
-- rows per entity per observation — draft § 6.3 is exactly why.

PRAGMA foreign_keys = ON;

CREATE TABLE schema_meta (
  version     TEXT NOT NULL,
  applied_utc TEXT NOT NULL,
  note        TEXT
);

CREATE TABLE fixture_session (
  session_id        TEXT PRIMARY KEY,
  lane              TEXT NOT NULL CHECK (lane IN ('gd-live','sim')),
  session_date      TEXT NOT NULL,
  operator          TEXT,
  game_edition_pin  TEXT,          -- composite pin, gd-edition-pin-2026-07-24 convention
  game_build_string TEXT,
  difficulty        TEXT CHECK (difficulty IN ('normal','veteran','elite','ultimate') OR difficulty IS NULL),
  container         TEXT,
  save_identity     TEXT,
  console_flags     TEXT,          -- JSON
  rig_version       TEXT,
  raw_notes_path    TEXT,
  capture_dir       TEXT,
  capture_clock_source TEXT NOT NULL DEFAULT 'in-game-playtime',
  sim_config_ref    TEXT,
  notes             TEXT,
  adapter           TEXT NOT NULL,
  schema_version    TEXT NOT NULL,
  created_date      TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE capture (                      -- ORACLE-ONLY
  capture_id   TEXT PRIMARY KEY,
  session_id   TEXT NOT NULL REFERENCES fixture_session(session_id),
  path         TEXT NOT NULL,               -- repo-relative
  kind         TEXT NOT NULL CHECK (kind IN
                 ('playstats-panel','console-log','world-view','character-sheet',
                  'trial-frame','other')),                                   -- E3
  label        TEXT,                        -- 'Screenshot (13)'
  sha256       TEXT NOT NULL,
  mtime_utc    TEXT,                        -- TRANSFER time, not capture time (draft § 8.5)
  pixel_w INTEGER, pixel_h INTEGER,
  notes        TEXT
);

CREATE TABLE fixture_character (
  character_id      TEXT PRIMARY KEY,
  session_id        TEXT NOT NULL REFERENCES fixture_session(session_id),
  snapshot_ordinal  INTEGER NOT NULL,
  valid_from_playtime_s INTEGER,
  char_level        INTEGER,
  mastery_1 TEXT, mastery_2 TEXT,
  hp_max REAL, energy_max REAL, oa REAL, da REAL, armor_avg REAL,
  weapon_record TEXT, weapon_dmg_min REAL, weapon_dmg_max REAL, attack_speed_pct REAL,
  resist_json TEXT, devotion_json TEXT, skill_bar_json TEXT, gear_json TEXT,
  completeness      TEXT NOT NULL CHECK (completeness IN
                      ('full-sheet','partial','level-and-hp-only','level-only','unknown')),
  capture_id        TEXT REFERENCES capture(capture_id),
  notes             TEXT,
  UNIQUE (session_id, snapshot_ordinal)
);

-- E1 -------------------------------------------------------------------------
-- Long-form exhaustive character-sheet readings. Same rationale as
-- trial_measurement (draft § 5): per-field provenance is the requirement, the
-- GD sheet has ~130 named fields, and the field set grows per rung/patch.
-- fixture_character keeps the typed columns the joins need; character_stat
-- keeps everything the sheet actually said.
CREATE TABLE character_stat (
  character_id  TEXT NOT NULL REFERENCES fixture_character(character_id),
  stat_key      TEXT NOT NULL,      -- snake_case of the verbatim sheet label
  stat_group    TEXT,               -- 'header'|'attributes'|'combat'|'resistances'|
                                    -- 'damage-per-hit'|'character'|'skill-bonuses'|
                                    -- 'physical'|'magical'|'pet-bonuses'|'defense'|
                                    -- 'retaliation'|'stats'
  value_num     REAL,
  value_num_hi  REAL,               -- for ranges like 'Weapon Attack 31-83'
  value_text    TEXT,
  unit          TEXT,               -- 'pct' | 'hp' | 'dmg' | 's' | NULL
  panel_label   TEXT NOT NULL,      -- VERBATIM label as rendered
  verbatim      TEXT NOT NULL,      -- VERBATIM value as rendered
  read_method   TEXT NOT NULL CHECK (read_method IN
                  ('screenshot-fullres','screenshot-downscaled','screenshot-illegible',
                   'hand-noted-point','hand-noted-band','inferred-adjacent-trial',
                   'sim-emitted','derived','absent')),
  uncertainty_abs REAL,
  capture_id    TEXT REFERENCES capture(capture_id),
  validity_flag TEXT NOT NULL DEFAULT 'valid'
                  CHECK (validity_flag IN ('valid','window-expired','superseded','suspect')),
  validity_note TEXT,
  PRIMARY KEY (character_id, stat_key)
);

CREATE TABLE fixture_set (
  fixture_set_id     TEXT PRIMARY KEY,
  session_id         TEXT NOT NULL REFERENCES fixture_session(session_id),
  character_id       TEXT NOT NULL REFERENCES fixture_character(character_id),
  ladder_rung        TEXT NOT NULL CHECK (ladder_rung IN ('L0','L1','L2','L3','L4','L5')),
  monster_record     TEXT,                  -- .dbr path; NULL admitted, O-8
  monster_display_name TEXT,                -- nameplate text, when attested
  monster_identity_method TEXT NOT NULL CHECK (monster_identity_method IN
                       ('spawn-command-verbatim','screenshot-nameplate',
                        'area-roster-inference','assumed-unverified')),
  monster_identity_evidence TEXT,
  monster_level      INTEGER,               -- the bio-formula charLevel; NEVER the player's level
  monster_level_method TEXT,
  monster_source     TEXT CHECK (monster_source IN ('spawned','world','unknown')),
  pack_size          INTEGER,
  engagement_mode    TEXT CHECK (engagement_mode IN ('pre-aggroed','from-idle','unknown')),
  area_name          TEXT,
  intended_n INTEGER, actual_n INTEGER,
  purpose TEXT
);

CREATE TABLE fixture_set_constraint (
  fixture_set_id TEXT NOT NULL REFERENCES fixture_set(fixture_set_id),
  constraint_key TEXT NOT NULL,
  held           TEXT NOT NULL CHECK (held IN ('held','violated','unknown','expired')),
  evidence       TEXT,
  PRIMARY KEY (fixture_set_id, constraint_key)
);

CREATE TABLE fixture_trial (
  trial_id       TEXT PRIMARY KEY,
  fixture_set_id TEXT NOT NULL REFERENCES fixture_set(fixture_set_id),
  trial_ordinal  INTEGER NOT NULL,
  lane           TEXT NOT NULL CHECK (lane IN ('gd-live','sim')),
  outcome        TEXT CHECK (outcome IN
                   ('monster-killed','player-died','monster-fled','aborted','timeout',
                    'no-fight-baseline')),                                   -- E2
  t_start_playtime_s INTEGER,
  t_end_playtime_s   INTEGER,
  before_capture_id  TEXT REFERENCES capture(capture_id),
  after_capture_id   TEXT REFERENCES capture(capture_id),
  monster_entity_id  TEXT,     -- ShowAngerLevels/LogData instance id, when overlay is on
  contaminated       INTEGER NOT NULL DEFAULT 0,
  contamination_reason TEXT,
  notes TEXT,
  UNIQUE (fixture_set_id, trial_ordinal)
);

CREATE TABLE measure_dict (
  measure_key   TEXT PRIMARY KEY,
  label         TEXT NOT NULL,
  unit          TEXT,
  value_kind    TEXT NOT NULL CHECK (value_kind IN ('counter','gauge','band','categorical')),
  panel_field   TEXT,
  lane_availability TEXT NOT NULL CHECK (lane_availability IN ('both','oracle-only','sim-only')),
  ladder_rung_introduced TEXT,
  definition    TEXT,
  confounds     TEXT
);

CREATE TABLE trial_measurement (
  trial_id      TEXT NOT NULL REFERENCES fixture_trial(trial_id),
  measure_key   TEXT NOT NULL REFERENCES measure_dict(measure_key),
  measure_subkey TEXT NOT NULL DEFAULT '',   -- the skill .dbr path etc. (O-2)
  phase         TEXT NOT NULL CHECK (phase IN ('before','after','during','derived')),
  value_num     REAL,
  value_num_hi  REAL,
  value_text    TEXT,
  unit          TEXT,
  read_method   TEXT NOT NULL CHECK (read_method IN
                  ('screenshot-fullres','screenshot-downscaled','screenshot-illegible',
                   'hand-noted-point','hand-noted-band','inferred-adjacent-trial',
                   'sim-emitted','derived','absent')),
  uncertainty_abs REAL,
  capture_id    TEXT REFERENCES capture(capture_id),
  verbatim      TEXT,
  validity_flag TEXT NOT NULL DEFAULT 'valid'
                  CHECK (validity_flag IN ('valid','window-expired','superseded','suspect')),
  validity_note TEXT,
  PRIMARY KEY (trial_id, measure_key, measure_subkey, phase)
);

CREATE TABLE trial_trace (
  trace_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id   TEXT NOT NULL REFERENCES fixture_session(session_id),
  trial_id     TEXT REFERENCES fixture_trial(trial_id),   -- NULL = session-scoped observation
  seq          INTEGER,
  channel      TEXT NOT NULL CHECK (channel IN
                 ('anger-overlay','logdata-console','sim-controller-emit','sim-anim-emit')),
  entity_ref   TEXT,
  trace_token  TEXT NOT NULL,          -- VERBATIM
  controller_state TEXT,               -- mapped 33-IN roster name; NULLABLE
  mapping_status TEXT NOT NULL CHECK (mapping_status IN
                   ('identity','case-normalized','inferred-mapping','unmapped')),
  vocab_status TEXT NOT NULL CHECK (vocab_status IN
                 ('in-roster-33','out-by-attestation-5','needs-join-2','not-in-40-state-table')),
  t_offset_s   REAL, duration_s REAL, duration_s_hi REAL,
  duration_method TEXT,
  capture_id   TEXT REFERENCES capture(capture_id),
  verbatim_line TEXT
);

-- ---------------------------------------------------------------------------
-- VIEWS (draft § 5). Spread is DERIVED; never stored.
-- ---------------------------------------------------------------------------

-- readings pivoted for ergonomics; the long table remains the truth
CREATE VIEW v_trial_wide AS
SELECT
  t.trial_id, t.fixture_set_id, t.trial_ordinal, t.lane, t.outcome,
  t.t_start_playtime_s, t.t_end_playtime_s, t.contaminated,
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

-- after - before per cumulative measure, carrying the WORST read_method of the pair
CREATE VIEW v_trial_delta AS
SELECT
  b.trial_id, b.measure_key, b.measure_subkey,
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
WHERE b.phase='before';

-- N-trial spread per (set, measure). Q47's instrument.
CREATE VIEW v_set_spread AS
SELECT
  t.fixture_set_id, d.measure_key, d.measure_subkey,
  COUNT(*) AS n,
  MIN(d.delta) AS min_delta, MAX(d.delta) AS max_delta,
  AVG(d.delta) AS mean_delta,
  MAX(d.delta) - MIN(d.delta) AS range_delta,
  CASE WHEN COUNT(*) > 1
       THEN SQRT( (SUM(d.delta*d.delta) - COUNT(*)*AVG(d.delta)*AVG(d.delta))
                  / (COUNT(*)-1.0) ) END AS stdev_delta
FROM v_trial_delta d JOIN fixture_trial t USING (trial_id)
GROUP BY t.fixture_set_id, d.measure_key, d.measure_subkey;

-- before(n+1) vs after(n) on cumulative counters: the off-trial-activity detector (draft § 8.1)
CREATE VIEW v_ledger_continuity AS
SELECT
  s.fixture_set_id,
  prev.trial_ordinal AS prev_ordinal, nxt.trial_ordinal AS next_ordinal,
  ma.measure_key, ma.measure_subkey,
  ma.value_num AS after_prev, mb.value_num AS before_next,
  mb.value_num - ma.value_num AS gap_delta,
  CASE WHEN mb.value_num - ma.value_num = 0 THEN 'continuous' ELSE 'DISCONTINUOUS' END AS verdict
FROM fixture_trial prev
JOIN fixture_trial nxt
  ON nxt.fixture_set_id = prev.fixture_set_id AND nxt.trial_ordinal = prev.trial_ordinal + 1
JOIN fixture_set s ON s.fixture_set_id = prev.fixture_set_id
JOIN trial_measurement ma ON ma.trial_id = prev.trial_id AND ma.phase='after'
JOIN trial_measurement mb ON mb.trial_id = nxt.trial_id  AND mb.phase='before'
 AND mb.measure_key = ma.measure_key AND mb.measure_subkey = ma.measure_subkey
JOIN measure_dict md ON md.measure_key = ma.measure_key AND md.value_kind='counter'
WHERE ma.read_method <> 'inferred-adjacent-trial'   -- draft § 4.6 rule: no circular evidence
  AND mb.read_method <> 'inferred-adjacent-trial'
  AND ma.measure_key <> 'play_time';                -- play_time always advances

-- G3-B: oracle lane joined to sim lane on the same fixture set + measure
CREATE VIEW v_differential AS
SELECT
  o.fixture_set_id, o.measure_key, o.measure_subkey,
  o.n AS oracle_n, o.mean_delta AS oracle_mean, o.min_delta AS oracle_min, o.max_delta AS oracle_max,
  s.n AS sim_n,    s.mean_delta AS sim_mean,    s.min_delta AS sim_min,    s.max_delta AS sim_max,
  s.mean_delta - o.mean_delta AS mean_gap
FROM (SELECT sp.* FROM v_set_spread sp JOIN fixture_set fs USING (fixture_set_id)
      JOIN fixture_session ss USING (session_id) WHERE ss.lane='gd-live') o
JOIN (SELECT sp.* FROM v_set_spread sp JOIN fixture_set fs USING (fixture_set_id)
      JOIN fixture_session ss USING (session_id) WHERE ss.lane='sim') s
  ON s.fixture_set_id = o.fixture_set_id AND s.measure_key = o.measure_key
 AND s.measure_subkey = o.measure_subkey;

-- O-8: the CERTIFIED bank. Q47 rules against THIS view only.
-- Certification predicate (three criteria, all structural):
--   1. monster identity attested by spawn command or nameplate  (not 'assumed-unverified',
--      not 'area-roster-inference'), AND the monster's own level is attested;
--   2. the character in force is a full-sheet snapshot;
--   3. no mid-set level-up — every trial in the set reads the same max_level_achieved,
--      which is guaranteed structurally by fixture_set.character_id pinning one snapshot,
--      and re-asserted here against the readings.
CREATE VIEW v_fixture_bank_certified AS
SELECT t.*, s.fixture_set_id AS set_id, s.monster_display_name, s.monster_record,
       s.monster_level, c.character_id AS char_id, c.char_level
FROM fixture_trial t
JOIN fixture_set s        ON s.fixture_set_id = t.fixture_set_id
JOIN fixture_character c  ON c.character_id   = s.character_id
WHERE s.monster_identity_method IN ('spawn-command-verbatim','screenshot-nameplate')
  AND s.monster_level IS NOT NULL
  AND s.monster_level_method IS NOT NULL
  AND c.completeness = 'full-sheet'
  AND t.outcome <> 'no-fight-baseline'
  AND NOT EXISTS (
        SELECT 1 FROM trial_measurement m1
        JOIN fixture_trial t2 ON t2.trial_id = m1.trial_id
        JOIN trial_measurement m2 ON m2.trial_id = t2.trial_id
        WHERE t2.fixture_set_id = s.fixture_set_id
          AND m1.measure_key='max_level_achieved' AND m2.measure_key='max_level_achieved'
          AND m1.value_num <> m2.value_num);

-- the certified bank with inter-trial ledger contamination additionally excluded
CREATE VIEW v_fixture_bank_certified_clean AS
SELECT * FROM v_fixture_bank_certified WHERE contaminated = 0;
