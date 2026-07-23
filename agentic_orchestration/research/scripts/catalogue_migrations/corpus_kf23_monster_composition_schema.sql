-- corpus_kf23_monster_composition_schema.sql
-- KF-2/3 additive schema — KIT-FIDELITY run (charter KFL-8(d)).
-- Author: elrond | 2026-07-23 | DB: agentic_orchestration/research/curated/corpus.db
-- ADDITIVE-ONLY: two new tables, zero existing-table change. Rebuildable (idempotent-safe via IF NOT EXISTS).
-- Companion MIGRATION doc: agentic_orchestration/research/curated/MIGRATION-kf23-monster-composition-2026-07-23.md
--
-- Dual-column law (charter): source_value IMMUTABLE + verbatim anchor; rdr_value stays NULL until the
-- gamora/star-lord normalization-rule lane derives it. elrond authors neither rules nor rdr_values.

CREATE TABLE IF NOT EXISTS monster_numeric (
    monster_id       TEXT NOT NULL,                 -- e.g. 'd2-fallen', 'poe1-goatman-leapslam-l68'
    game             TEXT NOT NULL,                 -- 'd2' | 'poe1' | 'poe2' | 'gd'
    monster_name     TEXT NOT NULL,                 -- display name
    numeric_key      TEXT NOT NULL,                 -- e.g. 'hp_min','defense','ar_attack1','fire_resist_pct'
    source_value     REAL NOT NULL,                 -- IMMUTABLE, anchored
    source_scale     TEXT NOT NULL,                 -- e.g. 'd2_flat_hp','d2_defense_rating','poe1_armour_rating','pct'
    rdr_value        REAL,                          -- DERIVED by rule; NULL until a rule runs; sim reads THIS only
    rule_id          TEXT REFERENCES normalization_rule(rule_id),
    rule_version_applied INTEGER,
    source_anchor    TEXT NOT NULL,                 -- verbatim quote for source_value
    source_url       TEXT NOT NULL,
    source_date      TEXT NOT NULL,
    starter_set      TEXT NOT NULL,                 -- e.g. 'd2-act1-normal','poe1-zone68','poe2-levelscale'
    gap_flag         TEXT
                       CHECK (gap_flag IS NULL OR gap_flag IN ('normal_resist_inferred','formula_level_anchor','one_source','range_estimate')),
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (monster_id, numeric_key)
);
CREATE INDEX IF NOT EXISTS idx_mnum_game    ON monster_numeric(game);
CREATE INDEX IF NOT EXISTS idx_mnum_starter ON monster_numeric(starter_set);
CREATE INDEX IF NOT EXISTS idx_mnum_rule    ON monster_numeric(rule_id);

CREATE TABLE IF NOT EXISTS kit_composition (
    comp_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    direction        TEXT NOT NULL CHECK (direction IN ('dealt','received')),
    factor_key       TEXT NOT NULL,                 -- e.g. 'base_damage','fire_mastery_mult','hit_chance','crit_ev','target_mitigation'
    factor_role      TEXT NOT NULL,                 -- 'base'|'modifier'|'hit_chance'|'crit_ev'|'mitigation'
    status           TEXT NOT NULL CHECK (status IN ('anchored','pinned','gap_excluded')),
    factor_value     TEXT,                          -- value/expression when anchored/pinned; NULL when gap_excluded
    ref              TEXT NOT NULL,                 -- anchor citation OR PIN id OR GAP id
    notes            TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX IF NOT EXISTS idx_kcomp_kit ON kit_composition(kit_id);
CREATE INDEX IF NOT EXISTS idx_kcomp_dir ON kit_composition(kit_id, direction);
