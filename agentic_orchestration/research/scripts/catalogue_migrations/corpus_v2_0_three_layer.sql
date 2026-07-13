-- corpus_v2_0_three_layer.sql
-- Canon-corpus DB v2.0 — three-layer schema per gandalf DELTA v2 (2026-07-12).
-- Owner: elrond.  Authority: 2026-07-12-elrond-corpus-ingest-brief.md DELTA v2.
-- Matt authorization: Q24(a)/(b)/(c) rulings 2026-07-12.
--
-- SCHEMA LAWS:
--   LAYER 1 — canon_corpus: identity + prefix (engine-lattice) + suffix (raw provenance)
--             [stands from v1.0 with targeted amendments per DELTA v2]
--   LAYER 2 — canon_probe_facts: one row per kit × family (probe output verbatim)
--   LAYER 3 — canon_engine_key: mapping-pass output verbatim, keyed on kit_id
--   ROSTER  — roster_atlas + roster_lineage_enrichment (Q24(b) replacement for 48 mobile rows)
--
-- RETIRED from v1.0:
--   rekey_geo / rekey_ctrl / rekey_mob / rekey_def / rekey_econ / rekey_elem
--   (re-key is per-kit via probe+judgment, not per-raw-value; no rekey_elem or rekey_mob
--    may EVER exist — element=free axis, mobility=emergent; both permanent by omission)
--
-- LAWS (permanent):
--   NO rekey_elem / rekey_mob table — ever (law by omission, same as measured-vs-projected)
--   suffix_rekey_status: geo/ctrl/def/econ = 'keyed-v1'; mob/elem = 'descriptor-final' (permanent)
--   ctrl.treatment: 'damage'|'control'|'hybrid' only — 'support' is NEVER legal (Q22 ruling)
--   def.bin: 'tank'|'mitigate'|'evade'|'absorb'|'glass'|'post-cutoff-deferred'|'FLAGGED'
--   geometry null: legal ONLY with resolved:placed-lane / gx-candidate:orbit / post-cutoff-deferred

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- schema version / lineage tracking
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS corpus_schema_meta (
    version        TEXT NOT NULL,
    applied_utc    TEXT NOT NULL,
    note           TEXT
);

-- ---------------------------------------------------------------------------
-- LAYER 1: canon_corpus
-- Identity + prefix engine-lattice + suffix raw provenance.
-- Amendments from v1.0:
--   - suffix_rekey_status default changed from 'awaiting-rekey' to slot-specific (geo/ctrl/def/econ='keyed-v1', mob/elem='descriptor-final')
--     NOTE: ingested as single value per row; updated post-ingest per slot logic
--   - is_system set from CSV key_group SYS detection (18 rows)
--   - rekey_* tables removed entirely
--   - view updated to LEFT-JOIN Layer 3 instead of rekey_* tables
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS canon_corpus (
    -- ---- identity ----
    kit_id                TEXT PRIMARY KEY,
    folk_name             TEXT,
    game                  TEXT NOT NULL,
    corpus_bucket         TEXT,
    tier                  TEXT,
    tier_confirm_pending  INTEGER NOT NULL DEFAULT 0,
    canon_tier            TEXT,
    eras                  TEXT,
    negative              INTEGER NOT NULL DEFAULT 0,
    lineage               TEXT,
    gx                    TEXT,

    -- ---- provenance ----
    source                TEXT NOT NULL,
    is_system             INTEGER NOT NULL DEFAULT 0,
    unresolved            INTEGER NOT NULL DEFAULT 0,
    mint                  INTEGER NOT NULL DEFAULT 0,
    dossier_owed          INTEGER NOT NULL DEFAULT 0,
    atlas_key_orig        TEXT,
    key_completeness      INTEGER,
    provenance_tag        TEXT NOT NULL DEFAULT 'mobile-harvest-v3',
    source_date           TEXT NOT NULL DEFAULT '2026-07-12',

    -- ---- PREFIX: typed engine-lattice coordinates {value, confidence} ----
    lattice_coord         TEXT,
    attr_val              TEXT CHECK (attr_val   IN ('STR','DEX','INT','WIS') OR attr_val   IS NULL),
    attr_conf             REAL,
    range_val             TEXT CHECK (range_val  IN ('melee','mid','ranged','dual') OR range_val IS NULL),
    range_conf            REAL,
    tempo_val             TEXT CHECK (tempo_val  IN ('low','med','high')     OR tempo_val  IS NULL),
    tempo_conf            REAL,
    amp_val               TEXT CHECK (amp_val    IN ('flat','spiky','var')   OR amp_val    IS NULL),
    amp_conf              REAL,
    proxy_val             TEXT CHECK (proxy_val  IN ('solo','light','heavy') OR proxy_val  IS NULL),
    proxy_conf            REAL,
    commit_val            TEXT CHECK (commit_val IN ('instant','wind-up','channel') OR commit_val IS NULL),
    commit_conf           REAL,
    prefix_conf_provenance TEXT NOT NULL DEFAULT 'avg-collapsed',
    avg_conf              REAL,

    -- ---- SUFFIX: raw descriptor columns (provenance-only) ----
    mob_raw               TEXT,
    geo_raw               TEXT,
    ctrl_raw              TEXT,
    def_raw               TEXT,
    econ_raw              TEXT,
    elem_raw              TEXT,
    ctrl_def_from_code    INTEGER NOT NULL DEFAULT 0,
    -- suffix_rekey_status: geo/ctrl/def/econ rows will be updated to 'keyed-v1'
    --   after Layer 3 ingest; mob/elem are permanent 'descriptor-final'
    suffix_rekey_status   TEXT NOT NULL DEFAULT 'awaiting-rekey',

    -- ---- ADD: engine-native (authored at re-key time; NULL at ingest) ----
    motion_frame              TEXT,
    t4_doors                  TEXT,
    option_c_substrate_flags  TEXT,
    commit_provenance         TEXT,

    -- ---- mobile-pass provenance (kept, flagged; NOT authority) ----
    mobile_cell_id            TEXT,
    mobile_key_group          TEXT,
    mobile_rank_in_cell       INTEGER,
    mobile_representative     INTEGER,
    mobile_mechanics_status   TEXT,
    mobile_blocking_mechanics TEXT,
    mech_note                 TEXT,
    flags                     TEXT,
    prov                      TEXT
);

CREATE INDEX IF NOT EXISTS idx_cc_game        ON canon_corpus(game);
CREATE INDEX IF NOT EXISTS idx_cc_source      ON canon_corpus(source);
CREATE INDEX IF NOT EXISTS idx_cc_lattice     ON canon_corpus(lattice_coord);
CREATE INDEX IF NOT EXISTS idx_cc_tier        ON canon_corpus(tier);
CREATE INDEX IF NOT EXISTS idx_cc_negative    ON canon_corpus(negative);
CREATE INDEX IF NOT EXISTS idx_cc_is_system   ON canon_corpus(is_system);
CREATE INDEX IF NOT EXISTS idx_cc_mint        ON canon_corpus(mint);

-- ---------------------------------------------------------------------------
-- LAYER 2: canon_probe_facts
-- One row per kit × family. Probe output stored as-is (facts_json = full family object).
-- Families: delivery | footprint | control | defense | economy | element |
--           movement | geo_text | rank1_upgrade | sources_used
-- post_cutoff_cap: 1 if this kit is post-cutoff (conf cap ≤0.5 applies)
-- dossier_owed: 1 for post-cutoff kits + mint kits
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS canon_probe_facts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id          TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    family          TEXT NOT NULL CHECK (family IN (
                        'delivery','footprint','control','defense','economy',
                        'element','movement','geo_text','rank1_upgrade','sources_used'
                    )),
    facts_json      TEXT NOT NULL,   -- full family object serialized as JSON
    conf            REAL,            -- family-level confidence (NULL for non-numeric families)
    prov            TEXT,            -- provenance string if present in family object
    post_cutoff_cap INTEGER NOT NULL DEFAULT 0,  -- 1 = post-cutoff kit; conf cap ≤0.5
    dossier_owed    INTEGER NOT NULL DEFAULT 0,  -- 1 = deeper dossier needed
    UNIQUE (kit_id, family)
);

CREATE INDEX IF NOT EXISTS idx_cpf_kit_id ON canon_probe_facts(kit_id);
CREATE INDEX IF NOT EXISTS idx_cpf_family  ON canon_probe_facts(family);

-- ---------------------------------------------------------------------------
-- LAYER 3: canon_engine_key
-- Mapping-pass output verbatim (ingested from corpus-engine-key-v1.jsonl).
-- Do NOT re-derive any values. Left-joined into v_canon_corpus_rekeyed.
-- row_class governs combat denominators: 'combat-kit'=463 / 'system-record'=15
-- ctrl.treatment CHECK: 'support' is NEVER legal (Q22 ruling).
-- geometry null: legal with flags containing 'resolved:placed-lane' / 'gx-candidate:orbit' /
--               'post-cutoff-deferred' only.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS canon_engine_key (
    kit_id                TEXT PRIMARY KEY REFERENCES canon_corpus(kit_id),

    -- geometry
    geometry_value        TEXT,
    geometry_rule_fired   TEXT,
    geometry_conf         REAL,

    -- ctrl
    ctrl_treatment        TEXT CHECK (ctrl_treatment IN ('damage','control','hybrid') OR ctrl_treatment IS NULL),
    ctrl_ailments_mapped  TEXT,      -- JSON array serialized
    ctrl_ailment_gaps     TEXT,      -- JSON array serialized

    -- def
    def_bin               TEXT CHECK (def_bin IN ('tank','mitigate','evade','absorb','glass',
                                                   'post-cutoff-deferred','FLAGGED') OR def_bin IS NULL),
    def_riders            TEXT,      -- JSON array serialized
    def_conf              REAL,

    -- econ
    econ_status           TEXT,
    econ_gaps             TEXT,      -- JSON array serialized
    econ_meter_type       TEXT,

    -- mob (descriptors only — no engine mapping; mobility=emergent)
    mob_skill_is_movement INTEGER,
    mob_policy_while_casting TEXT,
    mob_verbs             TEXT,      -- JSON array serialized

    -- row classification (governs combat denominator)
    row_class             TEXT NOT NULL CHECK (row_class IN ('combat-kit','system-record')),
    route                 TEXT,      -- system-record route (loot-economy/progression/etc.)
    flags                 TEXT,      -- JSON array serialized
    provenance_json       TEXT,      -- full provenance object

    -- full raw row (for fidelity — the JSONL row verbatim)
    raw_json              TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cek_row_class ON canon_engine_key(row_class);
CREATE INDEX IF NOT EXISTS idx_cek_def_bin   ON canon_engine_key(def_bin);
CREATE INDEX IF NOT EXISTS idx_cek_ctrl_trt  ON canon_engine_key(ctrl_treatment);

-- ---------------------------------------------------------------------------
-- ROSTER LAYER: roster_atlas
-- 45 rows from gandalf/views/roster-atlas-rebuilt-v1.csv (engine-sourced).
-- Q24(b): replaces the 48 mobile CSV roster/bench rows entirely.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roster_atlas (
    kit_id           TEXT PRIMARY KEY,
    name             TEXT,
    attr             TEXT,
    range_slot       TEXT,   -- 'range' is not reserved but 'commit' is; renamed for clarity
    tempo            TEXT,
    amp              TEXT,
    proxy            TEXT,
    commit_slot      TEXT,   -- 'commit' is SQLite reserved word; stored as commit_slot
    econ             TEXT,
    elem             TEXT,
    provenance       TEXT,
    lineage_targets  TEXT,   -- raw CSV string
    note             TEXT,
    class_v4r2       TEXT,
    source_date      TEXT NOT NULL DEFAULT '2026-07-12'
);

-- ---------------------------------------------------------------------------
-- ROSTER LAYER: roster_lineage_enrichment
-- 45 rows from megaprobe-2026-07-12/roster-lineage-enrichment.jsonl.
-- bc6 coordinates + lineage resolved to corpus kit_ids + neighbor analysis.
-- FK: lineage_targets_json references resolved corpus_kit_ids — dangling refs reported.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roster_lineage_enrichment (
    kit_id                       TEXT PRIMARY KEY REFERENCES roster_atlas(kit_id),
    folk_name                    TEXT,
    class_v4r2                   TEXT,
    bc6_attr                     TEXT,
    bc6_range                    TEXT,
    bc6_tempo                    TEXT,
    bc6_amp                      TEXT,
    bc6_proxy                    TEXT,
    bc6_commit                   TEXT,
    bc6_raw                      TEXT,
    provenance                   TEXT,
    note                         TEXT,
    lineage_targets_json         TEXT,   -- full array serialized
    target_count                 INTEGER,
    targets_resolved             INTEGER,
    targets_gap                  INTEGER,
    min_lineage_target_distance  INTEGER,
    nearest_corpus_neighbors_json TEXT,  -- full array serialized
    neighbor_count_d0            INTEGER,
    neighbor_count_d1            INTEGER,
    neighbor_count_d2            INTEGER,
    genre_density                INTEGER,
    whitespace_flag              INTEGER NOT NULL DEFAULT 0,
    source_date                  TEXT NOT NULL DEFAULT '2026-07-12'
);

CREATE INDEX IF NOT EXISTS idx_rle_whitespace ON roster_lineage_enrichment(whitespace_flag);
CREATE INDEX IF NOT EXISTS idx_rle_class      ON roster_lineage_enrichment(class_v4r2);

-- ---------------------------------------------------------------------------
-- VIEW: v_corpus_substrate
-- Canon kits only; excludes negatives, system, unresolved, mint.
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_corpus_substrate AS
SELECT * FROM canon_corpus
WHERE source = 'canon'
  AND is_system = 0
  AND unresolved = 0
  AND negative = 0;

-- ---------------------------------------------------------------------------
-- VIEW: v_canon_corpus_rekeyed
-- Layer-1 + Layer-3 left-join. Layer-3 governs where present.
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_canon_corpus_rekeyed AS
SELECT
    c.kit_id, c.folk_name, c.game, c.tier, c.canon_tier, c.negative,
    c.lineage, c.gx, c.source, c.is_system, c.mint, c.dossier_owed,
    c.lattice_coord,
    c.attr_val,  c.attr_conf,
    c.range_val, c.range_conf,
    c.tempo_val, c.tempo_conf,
    c.amp_val,   c.amp_conf,
    c.proxy_val, c.proxy_conf,
    c.commit_val,c.commit_conf,
    c.geo_raw,   c.ctrl_raw,  c.mob_raw,
    c.def_raw,   c.econ_raw,  c.elem_raw,
    c.suffix_rekey_status,
    -- Layer 3 engine-keyed values:
    k.geometry_value,    k.geometry_conf,
    k.ctrl_treatment,    k.ctrl_ailments_mapped, k.ctrl_ailment_gaps,
    k.def_bin,           k.def_riders,           k.def_conf,
    k.econ_status,       k.econ_gaps,            k.econ_meter_type,
    k.mob_policy_while_casting, k.mob_verbs,
    k.row_class,         k.route,                k.flags AS ek_flags
FROM canon_corpus c
LEFT JOIN canon_engine_key k ON c.kit_id = k.kit_id;

-- ---------------------------------------------------------------------------
-- VIEW: v_combat_kits
-- Combat kits only (row_class='combat-kit'). Denominator for Board 2 counts.
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_combat_kits AS
SELECT c.*, k.geometry_value, k.geometry_conf, k.ctrl_treatment,
       k.ctrl_ailments_mapped, k.ctrl_ailment_gaps,
       k.def_bin, k.def_riders, k.econ_status, k.econ_gaps,
       k.row_class, k.route, k.flags AS ek_flags
FROM canon_corpus c
JOIN canon_engine_key k ON c.kit_id = k.kit_id
WHERE k.row_class = 'combat-kit';
