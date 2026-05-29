-- ARPG Community Research Sprint — SQLite Schema
-- Authored 2026-05-29 evening late per gandalf authorization
-- Path: agentic_orchestration/research/arpg-community-axes-2026-05-29/research.db

CREATE TABLE IF NOT EXISTS builds (
  build_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_site TEXT NOT NULL,
  source_url TEXT NOT NULL,
  game TEXT NOT NULL,
  class_or_ascendancy TEXT,
  primary_skill TEXT,
  season_or_league TEXT,
  build_name TEXT,
  tagline TEXT,
  author TEXT,
  last_updated TEXT,
  archived_status BOOLEAN DEFAULT 0,
  acquired_at TEXT DEFAULT (datetime('now')),
  UNIQUE (source_site, source_url)
);

CREATE TABLE IF NOT EXISTS build_ratings_structured (
  build_id INTEGER REFERENCES builds(build_id),
  axis_name TEXT NOT NULL,
  rating_value TEXT,
  rating_normalized REAL,
  PRIMARY KEY (build_id, axis_name)
);

CREATE TABLE IF NOT EXISTS build_pros_cons (
  pc_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  polarity TEXT NOT NULL,
  text_tag TEXT NOT NULL,
  normalized_concept TEXT
);

CREATE TABLE IF NOT EXISTS build_activities (
  act_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  activity_name TEXT NOT NULL,
  content_tier_claim TEXT,
  activity_layer TEXT
);

CREATE TABLE IF NOT EXISTS build_variants (
  var_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  variant_name TEXT,
  progression_stage TEXT,
  activity_focus TEXT,
  mechanic_focus TEXT
);

CREATE TABLE IF NOT EXISTS build_skills (
  skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  skill_name TEXT NOT NULL,
  skill_role TEXT,
  order_position INTEGER,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS build_gear (
  gear_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  gear_slot TEXT,
  item_name TEXT NOT NULL,
  item_type TEXT,
  is_required BOOLEAN,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS build_stat_targets (
  stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  stat_name TEXT NOT NULL,
  target_value REAL,
  target_unit TEXT,
  priority_tier INTEGER,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS build_performance_claims (
  claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  claim_type TEXT,
  claim_value TEXT,
  content_context TEXT
);

CREATE TABLE IF NOT EXISTS build_summary (
  build_id INTEGER PRIMARY KEY REFERENCES builds(build_id),
  summary_text TEXT,
  descriptors_extracted TEXT
);

CREATE TABLE IF NOT EXISTS loot_substrate_vocabulary (
  vocab_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_site TEXT,
  game TEXT,
  layer TEXT,
  term TEXT NOT NULL,
  layer_role TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS vocabulary_convergence (
  conv_id INTEGER PRIMARY KEY AUTOINCREMENT,
  concept TEXT NOT NULL,
  layer TEXT,
  sites_observed_count INTEGER,
  sites_list TEXT,
  convergence_strength TEXT,
  vocabulary_variants TEXT,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_builds_site ON builds(source_site, game);
CREATE INDEX IF NOT EXISTS idx_builds_class ON builds(class_or_ascendancy);
CREATE INDEX IF NOT EXISTS idx_activities_name ON build_activities(activity_name);
CREATE INDEX IF NOT EXISTS idx_ratings_axis ON build_ratings_structured(axis_name);
CREATE INDEX IF NOT EXISTS idx_stat_targets_name ON build_stat_targets(stat_name);
CREATE INDEX IF NOT EXISTS idx_vocab_concept ON vocabulary_convergence(concept);
