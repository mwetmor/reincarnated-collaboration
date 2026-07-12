-- corpus_v1_0_canon_corpus.sql
-- Canon-corpus DB v1.0 — the mobile ARPG canon corpus under the ENGINE-FRAME schema of record.
-- Authority: corpus-rekey-spec-v1.md §2 fate table (gandalf, Matt inversion ruling 2026-07-12).
-- Owner: elrond.  Provenance tag: mobile-harvest-v3.
--
-- STATUS: PROPOSED / PAPER-WORK. This DDL is NOT executed until Matt's corpus-housing
--         D-ruling lands + standard ADR-006 authorization. See corpus-db-schema-proposal-2026-07-12.md.
--
-- Housing (OPEN — Matt D-ruling): default proposal is a NEW store
--   agentic_orchestration/research/curated/corpus.db  (parallel to catalogue.db, distinct domain:
--   catalogue.db = art assets; corpus.db = genre kits). Alternative under review: a namespaced
--   table-set inside an existing curated DB. Housing does not change this DDL — only the file it lands in.
--
-- SCHEMA LAWS baked here (spec §2, §1):
--   1. PREFIX KEPT: attr/range/tempo/amp/proxy/commit are typed engine-lattice coordinates (1:1 with
--      the engine lattice), each carried as {value, confidence}.  This 6-slot prefix IS lattice_coord.
--   2. SUFFIX RETIRED-TO-RAW: mob/geo/ctrl/def/econ/elem are RAW descriptor columns flagged
--      'awaiting-rekey'.  NO mappings are invented here.  The six design sessions supply mapping tables
--      later; the rekey_* tables + v_canon_corpus_rekeyed view let those join in WITHOUT rewriting rows.
--   3. MEASURED-VS-PROJECTED LAW: corpus rows can NEVER carry measured/fingerprint values.  There is
--      deliberately NO measured column on canon_corpus.  Measured axes = gauntlet fingerprints only,
--      which live in a separate engine-side store, not here.
--   4. REVERSIBLE / SOURCE-ANCHORED: every row traces to atlas_key_orig (verbatim) + provenance_tag +
--      source_date.  A clean rebuild from the v3 CSV lands at this exact curated state.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- version / lineage tracking (parallels catalogue.db schema_meta pattern)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS corpus_schema_meta (
    version        TEXT NOT NULL,          -- '1.0'
    applied_utc    TEXT NOT NULL,
    note           TEXT
);
INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES
 ('1.0', '2026-07-12T00:00:00Z',
  'Canon corpus initial lock: engine-frame prefix KEEP, suffix RETIRE-TO-RAW, measured-law hardened. Source: rdr-kit-atlas-v3.csv (563 rows).');

-- ---------------------------------------------------------------------------
-- main table
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS canon_corpus (
    -- ---- identity (spec §2 identity columns) ----
    kit_id                TEXT PRIMARY KEY,           -- e.g. 'poe1-tornado-shot'
    folk_name             TEXT,                       -- 'Tornado Shot'
    game                  TEXT NOT NULL,              -- game OF RECORD (v3 CSV `game` col); HoT is its OWN game ('hot')
    corpus_bucket         TEXT,                       -- harvest BUCKET (v3 CSV `corpus` col). NOT game-of-record:
                                                      --   bucket 'hades' -> games hades1/hades2; 'tl' -> tl1/tl2/tli.
                                                      --   kept as harvest provenance only.
    tier                  TEXT,                       -- engine-assigned lean: T1/T2/T2b/T3/RDR
    tier_confirm_pending  INTEGER NOT NULL DEFAULT 0, -- 1 = tier lean flagged for Matt confirm (all HoT rows)
    canon_tier            TEXT,                       -- era-depth: deep/moderate/shallow/negative/roster/bench
    eras                  TEXT,                       -- semicolon-joined era strings
    negative              INTEGER NOT NULL DEFAULT 0, -- 0/1 negative-space flag
    lineage               TEXT,                       -- lineage string (may be empty)
    gx                    TEXT,                       -- gap-refs, space-joined (e.g. 'GX-10 GX-14')

    -- ---- provenance (spec §2: original key preserved verbatim) ----
    source                TEXT NOT NULL,              -- 'canon' | 'roster' | 'bench'
    roster_provenance_only INTEGER NOT NULL DEFAULT 0,-- 1 for roster/bench (Matt throw-out ruling: lineage-only)
    is_system             INTEGER NOT NULL DEFAULT 0, -- 1 for SYS-annex evidence records (not kits)
    unresolved            INTEGER NOT NULL DEFAULT 0, -- 1 when key_completeness < 4 (sub-threshold key)
    atlas_key_orig        TEXT,                       -- ORIGINAL mobile atlas_key, verbatim provenance
    key_completeness      INTEGER,                    -- 1..12 slots filled (mobile-harvest metric)
    provenance_tag        TEXT NOT NULL DEFAULT 'mobile-harvest-v3',
    source_date           TEXT NOT NULL DEFAULT '2026-07-12',

    -- ---- PREFIX: typed engine-lattice coordinates, {value, confidence} per slot (spec §2 KEEP) ----
    lattice_coord         TEXT,                       -- 6-char prefix code = engine-lattice coord 1:1
    attr_val              TEXT CHECK (attr_val   IN ('STR','DEX','INT','WIS') OR attr_val   IS NULL),
    attr_conf             REAL,
    range_val             TEXT CHECK (range_val  IN ('melee','mid','ranged') OR range_val  IS NULL),
    range_conf            REAL,
    tempo_val             TEXT CHECK (tempo_val  IN ('low','med','high')     OR tempo_val  IS NULL),
    tempo_conf            REAL,
    amp_val               TEXT CHECK (amp_val    IN ('flat','spiky','var')   OR amp_val    IS NULL),
    amp_conf              REAL,
    proxy_val             TEXT CHECK (proxy_val  IN ('solo','light','heavy') OR proxy_val  IS NULL),
    proxy_conf            REAL,
    -- commitment enum OF RECORD: instant / wind-up / channel (code constant still spells 'snap'/'wind'/'chan'
    -- upstream — a trivial engine-hygiene rename flag, NOT a design question; spec §2)
    commit_val            TEXT CHECK (commit_val IN ('instant','wind-up','channel') OR commit_val IS NULL),
    commit_conf           REAL,
    -- how prefix confidence was sourced:
    --   'per-slot'      = true per-axis {v,c} from source jsonl (roster/bench, and canon IF jsonl recovered)
    --   'avg-collapsed' = only avg_conf available (canon rows from v3 CSV alone) — see open Q1
    prefix_conf_provenance TEXT NOT NULL DEFAULT 'avg-collapsed',
    avg_conf              REAL,                       -- mobile avg of proxy/geo/commit conf (lossy)

    -- ---- SUFFIX: RAW descriptor columns, awaiting-rekey (spec §2 RETIRE-TO-RAW). NO mappings invented. ----
    mob_raw               TEXT,                       -- raw movement descriptor (e.g. 'very-high')
    geo_raw               TEXT,                       -- raw geometry descriptor (e.g. 'multi-spawn')
    ctrl_raw              TEXT,                       -- control descriptor (see ctrl_def_from_code)
    def_raw               TEXT,                       -- defensive descriptor (see ctrl_def_from_code)
    econ_raw              TEXT,                       -- raw economy descriptor (e.g. 'mana-light')
    elem_raw              TEXT,                       -- raw element descriptor (e.g. 'physical')
    ctrl_def_from_code    INTEGER NOT NULL DEFAULT 0, -- 1 = ctrl_raw/def_raw are atlas_key-decoded coarse codes,
                                                      --     NOT source-raw strings (v3 CSV drops the raw ctrl/def);
                                                      --     honesty flag so re-key never mistakes them for source truth
    suffix_rekey_status   TEXT NOT NULL DEFAULT 'awaiting-rekey',

    -- ---- ADD: engine-native columns authored at RE-KEY time (spec §2 ADD; NULL at ingest) ----
    motion_frame              TEXT,                   -- 'orbiter_spiral' etc. — authored from engine sources
    t4_doors                  TEXT,                   -- T4 door refs
    option_c_substrate_flags  TEXT,                   -- Option-C substrate flags
    commit_provenance         TEXT,                   -- commitment pin-vs-roll provenance

    -- ---- mobile-pass DRAFT provenance (kept, flagged mobile-derived; NOT authority) ----
    mobile_cell_id            TEXT,                   -- mobile atlas cell browse id
    mobile_key_group          TEXT,                   -- mobile grouping key (KEYED/UNRESOLVED/SYS|..)
    mobile_rank_in_cell       INTEGER,
    mobile_representative      INTEGER,
    mobile_mechanics_status   TEXT,                   -- DRAFT mac-pass classification
    mobile_blocking_mechanics TEXT,
    mech_note                 TEXT,
    flags                     TEXT,
    prov                      TEXT
);

CREATE INDEX IF NOT EXISTS idx_cc_game        ON canon_corpus(game);
CREATE INDEX IF NOT EXISTS idx_cc_source      ON canon_corpus(source);
CREATE INDEX IF NOT EXISTS idx_cc_lattice     ON canon_corpus(lattice_coord);
CREATE INDEX IF NOT EXISTS idx_cc_tier        ON canon_corpus(tier);

-- ---------------------------------------------------------------------------
-- RE-KEY mapping tables (EMPTY at v1.0 — populated by the six design sessions).
-- Join-ready: keyed on the raw descriptor so a mapping row lights up every corpus row carrying
-- that raw value, WITHOUT any UPDATE to canon_corpus.  This is the "mapping tables join in without
-- rewriting rows" discipline (spec §2, elrond dispatch).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS rekey_geo  (raw TEXT PRIMARY KEY, engine_value TEXT, confidence REAL, session_ref TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS rekey_ctrl (raw TEXT PRIMARY KEY, engine_value TEXT, confidence REAL, session_ref TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS rekey_mob  (raw TEXT PRIMARY KEY, engine_value TEXT, confidence REAL, session_ref TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS rekey_def  (raw TEXT PRIMARY KEY, engine_value TEXT, confidence REAL, session_ref TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS rekey_econ (raw TEXT PRIMARY KEY, engine_value TEXT, confidence REAL, session_ref TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS rekey_elem (raw TEXT PRIMARY KEY, engine_value TEXT, confidence REAL, session_ref TEXT, note TEXT);

-- ---------------------------------------------------------------------------
-- consumption view: engine-frame prefix (authoritative) + re-keyed suffix (via LEFT JOIN).
-- Suffix engine columns are NULL until the relevant design session populates its rekey_* table.
-- Rows are never rewritten; the view derives the re-keyed value at read time.
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_canon_corpus_rekeyed AS
SELECT
    c.kit_id, c.folk_name, c.game, c.tier, c.canon_tier, c.negative, c.lineage, c.gx, c.source,
    c.lattice_coord,
    c.attr_val,  c.attr_conf,
    c.range_val, c.range_conf,
    c.tempo_val, c.tempo_conf,
    c.amp_val,   c.amp_conf,
    c.proxy_val, c.proxy_conf,
    c.commit_val,c.commit_conf,
    -- raw preserved + engine-mapped (NULL until session fires):
    c.geo_raw,  g.engine_value  AS geo_engine,  g.confidence  AS geo_map_conf,
    c.ctrl_raw, ct.engine_value AS ctrl_engine, ct.confidence AS ctrl_map_conf,
    c.mob_raw,  m.engine_value  AS mob_engine,  m.confidence  AS mob_map_conf,
    c.def_raw,  d.engine_value  AS def_engine,  d.confidence  AS def_map_conf,
    c.econ_raw, e.engine_value  AS econ_engine, e.confidence  AS econ_map_conf,
    c.elem_raw, el.engine_value AS elem_engine, el.confidence AS elem_map_conf,
    c.suffix_rekey_status, c.roster_provenance_only, c.is_system, c.unresolved
FROM canon_corpus c
LEFT JOIN rekey_geo  g  ON c.geo_raw  = g.raw
LEFT JOIN rekey_ctrl ct ON c.ctrl_raw = ct.raw
LEFT JOIN rekey_mob  m  ON c.mob_raw  = m.raw
LEFT JOIN rekey_def  d  ON c.def_raw  = d.raw
LEFT JOIN rekey_econ e  ON c.econ_raw = e.raw
LEFT JOIN rekey_elem el ON c.elem_raw = el.raw;

-- ---------------------------------------------------------------------------
-- convenience view: the substrate of record (canon only, kits only, keyed).
-- Roster/bench (provenance-only) and SYS-annex and sub-threshold rows are excluded.
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_corpus_substrate AS
SELECT * FROM canon_corpus
WHERE source = 'canon' AND is_system = 0 AND unresolved = 0;
