-- =====================================================================
-- VDM-2 DDL v1 — REVIEWABLE ARTIFACT — *** NOT APPLIED ***
-- =====================================================================
-- Author:      elrond (data steward)
-- Wave:        W3a (VDM-2 -> Edition-next lap, gandalf RUN-CONDUCTOR)
-- Charter:     agentic_orchestration/gandalf/notes/2026-07-22-vdm2-edition-next-lap-charter.md
-- Run state:   agentic_orchestration/gandalf/notes/2026-07-22-vdm2-edition-next-lap-run-state.md
-- Package:     2026-07-22-vdm2-w3a-migration-package.md  (the reviewable report this file belongs to)
-- Predecessor: 2026-07-22-vdm2-ddl-v0.sql  (this file = v0 + A-1..A-7 folded)
-- Pilot src:   2026-07-22-vdm2-pilot-4kit.md  (§6 amendment list A-1..A-7)
-- Target:      agentic_orchestration/research/curated/corpus.db  @ v1.1-verified (md5 50df15b776ad5b0da93fe90cdee1163d)
-- Governs:     spec = matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md
--
-- STATUS: THIS FILE IS A REVIEWABLE DRAFT FOR jack-ryan Gate-2. IT HAS NOT
--         BEEN RUN AGAINST corpus.db. Application is Wave W3b (Gate-2 PASS
--         first, backup+md5 first, MIGRATION.md per ADR-004, v2.0 stamp LAST).
--         Syntax-validated on a THROWAWAY COPY only; the live db is untouched.
--
-- WHAT CHANGED v0 -> v1 (the 7 pilot amendments, ALL ADDITIVE, G5-clean):
--   A-1  add 'self' to skill_geometry_band.range_band CHECK enum
--   A-2  declare trigger-door args (parallel_triggers/trigger_condition/
--        cadence_scale) as door_arg_schema DATA rows (BLOCK P0-A.4 below)
--   A-3  add 'fan_spread' to motion_signature_registry as a DATA row (BLOCK P1-A.2)
--   A-4  add 'real' to door_arg_schema.arg_type CHECK enum
--   A-5  origin vocab 'at_target'/'self_and_proxies' -> DOC-ONLY (origin is
--        free TEXT; documented in the column comment; ZERO DDL change)
--   A-6  corpus_class system tally = 19 (not 11) -> DOC-ONLY census (the enum
--        already admits 'system' at v0; only the rider row-count shifts; see
--        the package report A-6 census + the corpus_class rider header)
--   A-7  preserve NULL t4_doors -> RIDER-BEHAVIOR (baked into the door-strip
--        rider in the rider SQL, NOT a DDL coercion; see package §rider)
--
-- CHECK-SAFETY HEADER (jack-ryan Gate-2 pre-registered check):
--   The ONLY two amendments that touch a CHECK constraint are A-1
--   (skill_geometry_band.range_band) and A-4 (door_arg_schema.arg_type).
--   BOTH CHECKs live on tables INTRODUCED BY v0/v1 ITSELF — these tables do
--   NOT yet exist in corpus.db. Therefore:
--     * NO SQLite table-rebuild is incurred (CHECK is authored at CREATE time,
--       not ALTERed on an existing table).
--     * ZERO VDM-1 data is touched by A-1/A-4 (the tables are empty at CREATE).
--     * The two EXISTING-table CHECKs the spec could have forced a rebuild on
--       (verify_ledger.claim_family / .verdict) are NOT touched — v0/v1 add
--       only nullable columns there (BLOCK P3), and need NO new family/verdict
--       value. The CHECK-rebuild trap is avoided by design.
--   Net: A-1 and A-4 hit ONLY v0-NEW tables. No rebuild. No VDM-1 data touched.
--
-- DESIGN LAW (unchanged from v0; read the schema-diff report before applying):
--   * ADDITIVE-FIRST. Zero DROP / zero ALTER-of-existing-column / zero
--     CHECK-modification-on-an-existing-table. Every VDM-1 row stays valid;
--     kit_master (574) recomputes unchanged; frozen cell_keys stay byte-identical.
--   * Six flat VDM-2 blocks re-home as kit_id-keyed SIDE-CAR TABLES (the store
--     is normalized-relational, not flat JSON — W0's largest correction).
--   * source-anchored + reversible + tagged-not-encoded + versioned.
--   * Gate G5: no breaking change forced by non-D3 pilot kits (W2 confirmed
--     zero breaking; the 7 amendments here are the additive fallout).
-- =====================================================================


-- =====================================================================
-- BLOCK 0 -- STAMP GUARD (informational; the real stamp is written by the
--            W3b apply script AFTER a verified backup+md5, not here)
-- =====================================================================
-- Precondition the W3b script MUST assert before any statement below:
--   SELECT version FROM corpus_schema_meta ORDER BY rowid DESC LIMIT 1;
--   -- MUST equal 'v1.1-verified' / 'v1.1-deprecation-source_urls'
-- The FINAL line of the W3b migration (NOT here) will be:
--   INSERT INTO corpus_schema_meta(version, applied_utc, note)
--   VALUES ('v2.0', '<utc>', 'VDM-2 schema landing ... <full note>');


-- #####################################################################
-- ## P0-A -- TYPED DOOR-ARGS REGISTRY  (spec s2)
-- #####################################################################
-- (Unchanged from v0 except A-4 arg_type enum + A-2 seed data rows below.)

-- 0.1 The door catalogue: one row per distinct door token in the registry.
CREATE TABLE IF NOT EXISTS door_registry (
    door_name        TEXT PRIMARY KEY,          -- e.g. 'DUAL_PROXY'; matches t4_doors tokens
    door_status      TEXT NOT NULL DEFAULT 'active'
                       CHECK (door_status IN ('active','deprecated','proposed')),
    rfc_ref          TEXT,                       -- new doors require full RFC (spec s2); pointer to it
    description      TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);

-- 0.2 Per-door arg schema: one row per (door, arg). Declares type, the legal-
--     value enum (JSON array; tagged-not-encoded), and the DEFAULT bare usage
--     implies.
-- >>> A-4 AMENDMENT: arg_type CHECK enum gains 'real' <<<
--     v0 enum was {enum,int,ref,bool,list,duration_s,pct}. CoC Ice Nova's
--     cadence_scale=0.75 is a raw fraction (0..1), NOT a percent -> 'real'
--     added. This CHECK is on a v1-NEW table (door_arg_schema does not exist
--     in corpus.db yet) => no rebuild, no VDM-1 touch (see CHECK-SAFETY header).
CREATE TABLE IF NOT EXISTS door_arg_schema (
    door_name        TEXT NOT NULL REFERENCES door_registry(door_name),
    arg_name         TEXT NOT NULL,              -- e.g. 'sync_mode'
    arg_type         TEXT NOT NULL
                       CHECK (arg_type IN ('enum','int','real','ref','bool','list','duration_s','pct')),
    enum_values      TEXT,                       -- JSON array of legal values when arg_type='enum'
    default_value    TEXT,                       -- the value bare usage assumes (spec: "all args default")
    arg_rfc_ref      TEXT,                        -- new ARG VALUE = cheap mini-RFC (spec s2); pointer
    notes            TEXT,
    PRIMARY KEY (door_name, arg_name)
);

-- 0.3 Per-kit door binding: the ACTUAL args a given kit sets on a door it uses,
--     PLUS the mutation_surface flag (spec s8 folds into this exact row). One
--     row per (kit, door, arg) actually bound. A door left bare => no rows here
--     => the door_arg_schema default applies.
CREATE TABLE IF NOT EXISTS kit_door_arg (
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    door_name        TEXT NOT NULL REFERENCES door_registry(door_name),
    arg_name         TEXT NOT NULL,
    arg_value        TEXT,                        -- the bound value (validated against door_arg_schema in-app)
    mutation_surface TEXT NOT NULL DEFAULT 'locked'
                       CHECK (mutation_surface IN ('locked','mutable')),  -- spec s8 season lever
    derivation       TEXT NOT NULL DEFAULT 'dossier-prose'
                       CHECK (derivation IN ('dossier-prose','datamine','player_attested','authored','default')),
    source_anchor    TEXT,                        -- verbatim prose/quote the value was derived from (elrond law)
    bound_date       TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (kit_id, door_name, arg_name),
    -- FK to the arg schema keeps bindings honest: no binding an arg the door
    -- does not declare.
    FOREIGN KEY (door_name, arg_name) REFERENCES door_arg_schema(door_name, arg_name)
);
CREATE INDEX IF NOT EXISTS idx_kda_kit  ON kit_door_arg(kit_id);
CREATE INDEX IF NOT EXISTS idx_kda_door ON kit_door_arg(door_name);
CREATE INDEX IF NOT EXISTS idx_kda_mut  ON kit_door_arg(mutation_surface);

-- >>> A-2 AMENDMENT: trigger-door arg DECLARATIONS (DATA rows, not DDL) <<<
--     CoC Ice Nova (D-2 refutation surface) proved the trigger-family doors
--     carry three args the v0 registry had not yet declared. Declaring them
--     as door_arg_schema rows is the intended growth path (a data row, not a
--     schema change). These rows presuppose the door_registry rows for the
--     trigger-family doors exist; the W3b/W4 door-catalogue seed (built from
--     the 28 on-record door tokens) inserts those door_registry rows first.
--     GUARD: these INSERTs are here for REVIEW COMPLETENESS. In the W3b apply
--     they run only AFTER the door_registry seed (else the FK to door_registry
--     fails loud under PRAGMA foreign_keys=ON — which is the correct behavior).
--     They are re-run-safe via 'INSERT OR IGNORE' (idempotent).
--
--     Type choices (A-4-consistent):
--       parallel_triggers : int    (count of parallel on-crit triggers; Cospri = 2)
--       trigger_condition : enum    (on_crit | on_hit | on_kill | on_cast; default on_crit)
--       cadence_scale     : real    (0..1 raw fraction; A-4 'real' — NOT pct)
--     Applied to the trigger-family door(s) attested in the pilot: ELEMENTAL_ECHO.
--     The pattern generalizes to other trigger doors at W4 as their arg
--     surfaces are attested; this is the seed, not the closure.
--
-- INSERT OR IGNORE INTO door_registry(door_name, door_status, description) VALUES
--   ('ELEMENTAL_ECHO','active','trigger-family door: a host action triggers a payload skill (e.g. Cast-on-Crit).');
-- INSERT OR IGNORE INTO door_arg_schema(door_name, arg_name, arg_type, enum_values, default_value, notes) VALUES
--   ('ELEMENTAL_ECHO','trigger_condition','enum','["on_crit","on_hit","on_kill","on_cast"]','on_crit','A-2: the event that fires the triggered payload'),
--   ('ELEMENTAL_ECHO','parallel_triggers','int',NULL,'1','A-2: number of parallel trigger sources (Cosps Malice = 2nd on-crit trigger => 2)'),
--   ('ELEMENTAL_ECHO','cadence_scale','real',NULL,'1.0','A-2/A-4: raw 0..1 fraction (CoC 14%-CDR breakpoint => 0.75); a real, not a pct');
--   -- (left as commented seed in this REVIEW file; the live seed lives in the rider SQL, ordered after the door_registry catalogue.)


-- #####################################################################
-- ## P0-B -- STRUCTURED DEVIATIONS + AUTO-DOCKET WIRING  (spec s3)
-- #####################################################################
-- (Unchanged from v0. The pilot G4 gate exercised this route end-to-end with
--  no amendment. deviation_class enum {engine_inexpressible,param_gap,
--  accepted_downgrade} is complete for the pilot set.)

CREATE TABLE IF NOT EXISTS kit_deviation (
    deviation_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    missing_expression TEXT NOT NULL,             -- what has no native expression (from prose)
    deviation_class  TEXT NOT NULL
                       CHECK (deviation_class IN ('engine_inexpressible','param_gap','accepted_downgrade')),
    hook_refs        TEXT,                         -- JSON array of recognition_hook ids (P2), e.g. ["H1"]
    proposed_fix_type TEXT
                       CHECK (proposed_fix_type IN ('door_param','new_door_rfc','none') OR proposed_fix_type IS NULL),
    proposed_fix_target TEXT,                      -- e.g. 'DUAL_PROXY.sync_mode+origin_model'
    downgrade_owner  TEXT,                          -- sign-off handle; mandatory when class=accepted_downgrade
    downgrade_signoff_date TEXT,
    docket_id        INTEGER REFERENCES mechanic_gap_docket(docket_id),  -- set by auto-wire when class in (EI,PG)
    source_anchor    TEXT,                           -- verbatim deviation prose the row derived from
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    -- WIRING RULE 1 (spec s3): accepted_downgrade => owner sign-off present.
    CHECK (deviation_class <> 'accepted_downgrade' OR downgrade_owner IS NOT NULL),
    -- WIRING RULE 2 (spec s3): accepted_downgrade must NOT open a docket
    -- (absorbed by sign-off). Soft-enforced (docket_id nullable at insert; the
    -- W4 emitter opens the docket then back-fills docket_id).
    CHECK (deviation_class = 'accepted_downgrade' OR docket_id IS NULL OR docket_id > 0)
);
CREATE INDEX IF NOT EXISTS idx_kdev_kit    ON kit_deviation(kit_id);
CREATE INDEX IF NOT EXISTS idx_kdev_class  ON kit_deviation(deviation_class);
CREATE INDEX IF NOT EXISTS idx_kdev_docket ON kit_deviation(docket_id);

-- ADDITIVE extension to the EXISTING docket so an auto-opened VDM-2 docket is
-- distinguishable from the 19 VDM-1 matt-ratified rows and traces to its source.
-- (No existing docket column is touched. New rows take status='open', the table
--  default, which distinguishes them from the 19 status='matt-ratified' rows.)
ALTER TABLE mechanic_gap_docket ADD COLUMN source_deviation_id INTEGER REFERENCES kit_deviation(deviation_id);
ALTER TABLE mechanic_gap_docket ADD COLUMN source_kit_id       TEXT;   -- single kit that auto-opened it (vs evidence_kits array)
ALTER TABLE mechanic_gap_docket ADD COLUMN intake_lane         TEXT;   -- 'mint' (source-side, existing) | 'deviation' (engine-side, NEW second intake)


-- #####################################################################
-- ## P1-A -- GEOMETRY BANDS  (spec s4)  [per-skill grain: D-2 HYPOTHESIS HELD]
-- #####################################################################
-- Grain is (kit_id, skill_ordinal) -- the pilot's D-2 refutation surface
-- (CoC support-gem + GD transmuter) confirmed the per-skill grain HOLDS and
-- the spec's flat single-geometry{}-per-kit block is refuted. Support gems
-- model as a door + trigger-primitive on the PAYLOAD skill's row (via
-- count_multiplier_source), not as a phantom skill row.
--
-- >>> A-1 AMENDMENT: range_band CHECK enum gains 'self' <<<
--     Masquerade Simulacrum + several summon/self-buff skills have
--     range_band='self'. v0 enum {melee,short,medium,long,screen} lacked it.
--     This CHECK is on a v1-NEW table => no rebuild, no VDM-1 touch (header).

CREATE TABLE IF NOT EXISTS skill_geometry_band (
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    skill_ordinal    INTEGER NOT NULL,            -- 0-based index into mapping_json.skills[]
    source_skill     TEXT,                         -- echoes mapping_json.skills[].source_skill for legibility
    delivery_class   TEXT
                       CHECK (delivery_class IN ('projectile','beam','zone','motion','aura','summon_delegate','melee_arc') OR delivery_class IS NULL),
    origin           TEXT,                         -- free TEXT (A-5 documented vocab): 'self' | 'self_and_proxies' | 'at_target' | ...
                                                   --   A-5: controlled origin vocabulary is DOCUMENTED here (no CHECK; origin stays free TEXT).
                                                   --   Attested values so far: 'self', 'self_and_proxies' (Masquerade), 'at_target' (Trapsin).
                                                   --   The W4 emitter SHOULD draw from this controlled set; new values are additive prose.
    width_band       TEXT CHECK (width_band IN ('narrow','medium','wide') OR width_band IS NULL),
    range_band       TEXT CHECK (range_band IN ('self','melee','short','medium','long','screen') OR range_band IS NULL),  -- A-1: 'self' added
    speed_band       TEXT CHECK (speed_band IN ('slow','medium','fast','instant') OR speed_band IS NULL),
    pierce           TEXT,                          -- '0' | '<n>' | 'all' (kept TEXT: 'all' is legal)
    chain            INTEGER,
    fork             INTEGER,
    count_per_cast   INTEGER,
    count_multiplier_x INTEGER,                     -- the 'x' of count_multiplier
    count_multiplier_source TEXT,                   -- causal source, e.g. 'door:DUAL_PROXY' (spec: capture the cause)
    cadence_class    TEXT CHECK (cadence_class IN ('spam','builder_spender','cooldown','channel') OR cadence_class IS NULL),
    motion_signature TEXT,                          -- named-path enum; open-ended registry (see motion_signature_registry)
    band_conf        REAL,                          -- carries the 0.82-style confidence forward
    derivation       TEXT NOT NULL DEFAULT 'dossier-prose'
                       CHECK (derivation IN ('dossier-prose','datamine','player_attested','authored')),
    source_anchor    TEXT,                          -- verbatim guide text the bands were read from (elrond law)
    -- optional exact{} overlay: datamine lanes ONLY (spec s4). STAYS NULL at
    -- apply (G-FIND-1 / V-19): the .txt datamine lane is NOT on record; genuine
    -- population is a downstream legolas Mode-B datamine dependency. Never
    -- blocks a kit (the band lands on prose alone).
    exact_json       TEXT,                          -- {value, units, ...} from D2 txt / GD DBR / PoB-RePoE / TQ dbr -- NULL at apply
    exact_source_type TEXT,                         -- 'd2_missiles_txt' | 'gd_dbr' | 'poe_repoe' | 'tq_dbr' | NULL -- NULL at apply
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (kit_id, skill_ordinal)
);
CREATE INDEX IF NOT EXISTS idx_sgb_kit      ON skill_geometry_band(kit_id);
CREATE INDEX IF NOT EXISTS idx_sgb_delivery ON skill_geometry_band(delivery_class);
CREATE INDEX IF NOT EXISTS idx_sgb_cadence  ON skill_geometry_band(cadence_class);

-- motion_signature is a CLASSIFICATION against a growable named-path registry.
CREATE TABLE IF NOT EXISTS motion_signature_registry (
    signature_name   TEXT PRIMARY KEY,             -- 'straight_line','spiral_out','orbit_fixed','sine','mortar_arc','wall_sweep','fan_spread',...
    engine_impl_ref  TEXT,                          -- pointer to the canonical engine implementation
    description      TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);

-- >>> A-3 AMENDMENT: seed the motion registry, incl. 'fan_spread' (DATA rows) <<<
--     GD Stun Jacks' 180-degree radial sector is 'fan_spread' -- NOT one of the
--     v0 seed paths. Because motion_signature_registry is growable BY DESIGN,
--     this is a registry-row addition, not a schema change. The seed below
--     lands the v0 seed paths + fan_spread. Idempotent (INSERT OR IGNORE).
--     (Left as commented seed in this REVIEW file; the live seed lives in the
--      rider SQL, alongside the door catalogue seed.)
-- INSERT OR IGNORE INTO motion_signature_registry(signature_name, description) VALUES
--   ('straight_line','projectile travels a straight vector from origin'),
--   ('spiral_out','projectile spirals outward from origin'),
--   ('orbit_fixed','effect orbits a fixed point (player or anchor)'),
--   ('sine','projectile follows a sinusoidal path'),
--   ('mortar_arc','projectile lobs on a ballistic arc to a target point'),
--   ('wall_sweep','effect sweeps as a wall/line across an area'),
--   ('fan_spread','A-3: radial fan / sector spray (e.g. GD Stun Jacks 180-degree point-blank spread)');


-- #####################################################################
-- ## P1-B -- DUAL-COLUMN NUMERICS + NORMALIZATION-RULE REGISTRY  (spec s5)
-- #####################################################################
-- (Unchanged from v0. V-13: normalization_rule ships EMPTY; rdr_value honest-
--  NULL until battle-sim populates rules (gamora/star-lord semantics, ADR-004
--  when populated). The run authors ZERO balance transforms.)

CREATE TABLE IF NOT EXISTS normalization_rule (
    rule_id          TEXT PRIMARY KEY,             -- e.g. 'N-D3-SET-01'
    rule_version     INTEGER NOT NULL DEFAULT 1,   -- VERSIONED: bump re-derives dependents corpus-wide
    source_scale     TEXT NOT NULL,                -- the scale this rule consumes, e.g. 'd3_set_pct_bonus'
    description      TEXT NOT NULL,
    rule_owner       TEXT,                          -- battle-sim team sign-off (spec s5) -- gamora/star-lord seam
    formula_ref      TEXT,                          -- pointer to the transform (script/spec), not inline math
    status           TEXT NOT NULL DEFAULT 'proposed'
                       CHECK (status IN ('proposed','active','superseded')),
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS kit_numeric (
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    numeric_key      TEXT NOT NULL,                -- e.g. 'dr_masq','set_mult'
    source_value     REAL NOT NULL,                -- IMMUTABLE, anchored (VERIFY territory) -- spec s5
    source_scale     TEXT NOT NULL,                -- e.g. 'd3_pct_dr'
    rdr_value        REAL,                          -- DERIVED by rule; NULL until rule runs; sim reads THIS only
    rule_id          TEXT REFERENCES normalization_rule(rule_id),
    rule_version_applied INTEGER,                   -- which rule version produced the current rdr_value (staleness check)
    source_anchor    TEXT,                          -- verbatim quote for source_value (VERIFY anchor; elrond law)
    verify_ledger_id INTEGER REFERENCES verify_ledger(id),  -- link to the mechanics verdict on this source_value (spec s7)
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (kit_id, numeric_key)
);
CREATE INDEX IF NOT EXISTS idx_knum_kit  ON kit_numeric(kit_id);
CREATE INDEX IF NOT EXISTS idx_knum_rule ON kit_numeric(rule_id);


-- #####################################################################
-- ## P2-A -- RECOGNITION HOOKS  (spec s6)
-- #####################################################################
-- (Unchanged from v0.)
CREATE TABLE IF NOT EXISTS recognition_hook (
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    hook_id          TEXT NOT NULL,                -- kit-local id, e.g. 'H1'
    rank             INTEGER NOT NULL,             -- 1 = most identity-defining
    hook_type        TEXT
                       CHECK (hook_type IN ('geometry','defense_identity','cadence','threshold_moment','register','resource','control','other') OR hook_type IS NULL),
    hook_text        TEXT NOT NULL,                -- the recognizable-experience sentence
    expressed_by     TEXT,                          -- 'door:DUAL_PROXY{sync_mode,origin_model}' | 'geometry.cadence_class' | 'assert:delta_t4' | 'element:shadow'
    provenance       TEXT NOT NULL DEFAULT 'crawled'
                       CHECK (provenance IN ('crawled','player_attested','authored')),  -- spec s6: H4 is player_attested
    coverage_status  TEXT NOT NULL DEFAULT 'unresolved'
                       CHECK (coverage_status IN ('expressed','accepted_downgrade','unresolved')),  -- machine-checkable (spec s6)
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (kit_id, hook_id)
);
CREATE INDEX IF NOT EXISTS idx_rh_kit      ON recognition_hook(kit_id);
CREATE INDEX IF NOT EXISTS idx_rh_coverage ON recognition_hook(coverage_status);


-- #####################################################################
-- ## P2-B -- SIM ACCEPTANCE BLOCK  (spec s6)
-- #####################################################################
-- (Unchanged from v0. Trapsin confirmed shape='ramp' absorbs the stacked-
--  synergy gradient; CoC/Stun Jacks confirm shape='step'. 2-value enum holds.)
CREATE TABLE IF NOT EXISTS kit_acceptance_assert (
    assert_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    assert_text      TEXT NOT NULL,                -- e.g. 'projectiles_per_cast == 3'
    hook_id          TEXT,                          -- links to recognition_hook.hook_id (coverage back-ref)
    expected_state   TEXT,                          -- e.g. 'RED until DUAL_PROXY.origin_model ships' (spec s6)
    last_result      TEXT
                       CHECK (last_result IN ('green','red','untested') OR last_result IS NULL),
    routed_docket_id INTEGER REFERENCES mechanic_gap_docket(docket_id),  -- red-test doctrine: red assert -> docket
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX IF NOT EXISTS idx_kaa_kit  ON kit_acceptance_assert(kit_id);
CREATE INDEX IF NOT EXISTS idx_kaa_hook ON kit_acceptance_assert(hook_id);

CREATE TABLE IF NOT EXISTS kit_delta_t4 (
    kit_id           TEXT PRIMARY KEY REFERENCES canon_corpus(kit_id),
    shape            TEXT NOT NULL
                       CHECK (shape IN ('step','ramp')),   -- spec s6: 'step' = threshold-crossing experience target
    asserts_json     TEXT,                          -- JSON array of the T4 transition asserts
    shape_signoff    TEXT NOT NULL DEFAULT 'unvalidated'
                       CHECK (shape_signoff IN ('unvalidated','human-validated')),  -- 'step' human-validated in review book, never self-certified
    shape_signoff_by TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);


-- #####################################################################
-- ## P3 -- VERIFY EXTENSION  (spec s7)
-- #####################################################################
-- (Unchanged from v0. mechanics verdicts ALREADY EXIST -- this is a granularity
--  extension, NOT a new family. Deliberately does NOT touch the
--  claim_family/verdict CHECKs => no rebuild. Only nullable columns added.)
ALTER TABLE verify_ledger ADD COLUMN claim_subject TEXT;   -- fine-grained target: 'geometry.range_band' | 'numeric.dr_masq' | 'skill_loop' | NULL(=coarse VDM-1 row)
ALTER TABLE verify_ledger ADD COLUMN anchor_lint   TEXT
                       CHECK (anchor_lint IN ('OK','ANCHOR_WEAK') OR anchor_lint IS NULL);  -- spec s7 lint; hygiene only, never auto-escalates
ALTER TABLE verify_ledger ADD COLUMN source_lane   TEXT
                       CHECK (source_lane IN ('crawled','player_attested','dataset','official') OR source_lane IS NULL);  -- spec s7 new 'player_attested' lane
-- NOTE: these two ADD-COLUMN CHECKs are the ONE subtle case -- adding a NEW
-- column WITH a CHECK is legal in SQLite ADD COLUMN *provided* the CHECK
-- references only the new column and the column is nullable (both true here);
-- it does NOT rebuild the table and cannot invalidate existing rows (they get
-- NULL, which every CHECK admits via 'OR ... IS NULL'). Verified on throwaway
-- copy. run_tag already exists (default 'vdm1'); VDM-2 mechanics rows set 'vdm2'.


-- #####################################################################
-- ## HOUSEKEEPING  (spec s8 + charter W0 housekeeping list)
-- #####################################################################
-- All ADDITIVE columns on canon_corpus. DATA population is the rider SQL
-- (co-located in the package), NOT here. Column definitions unchanged from v0.

-- H1. corpus_class -- record|annex|system.
--     >>> A-6: the 'system' value covers ALL 19 is_system=1 rows (NOT 11).
--     The enum was already 3-value at v0; A-6 is a DOC/census correction, not
--     a DDL change. NULL means 'unclassified' only (V-14), never 'system'.
--     The rider (package) writes: system = every is_system=1 (19);
--     record = is_system=0 AND corpus_bucket IN (poe1,d2,gd,poe2,le) (267);
--     annex = is_system=0 AND other games (299). 267+299+19 = 585.
ALTER TABLE canon_corpus ADD COLUMN corpus_class TEXT
                       CHECK (corpus_class IN ('record','annex','system') OR corpus_class IS NULL);

-- H2. eras_normalized -- V-16 option (c): per-game canonical era-token set
--     (fixed lowercase vocabulary PER GAME, documented in MIGRATION.md). NO
--     cross-game ordinal in the column (shelves derive at the Leg-B beat per
--     Q38 eras=shelves). Raw 'eras' preserved (reversible). The rider writes
--     the normalized token list per row from its raw semicolon-shorthand.
ALTER TABLE canon_corpus ADD COLUMN eras_normalized TEXT;

-- H3. original_element -- PROMOTION of elem_raw (100% non-NULL on record-270,
--     verified 270/270). elem_raw stays as the raw source (never dropped).
ALTER TABLE canon_corpus ADD COLUMN original_element TEXT;

-- H4. court -- Q38 k=5 {fire,cold,lightning,physical,chaos-poison}, DERIVED
--     from elem_raw per V-15 (see package court rider + coverage report).
--     Coverage 257/270 courted, 13 honest-NULL. court is MUTABLE data (V-18:
--     W5 elem_raw corrections re-derive affected rows).
ALTER TABLE canon_corpus ADD COLUMN court TEXT
                       CHECK (court IN ('fire','cold','lightning','physical','chaos-poison') OR court IS NULL);

-- H5. atlas_coords -- PROMOTION/DENORMALIZATION of canon_engine_key.cell_key
--     (268/270 on-record; 2 honest NULL: poe1-blood-magic-kit, d2-teleport-
--     sorc). Reversible (cell_key is the source of truth).
ALTER TABLE canon_corpus ADD COLUMN atlas_coords TEXT;

-- H6. capstone_source_acquisition -- spec s8 enum; drives T4 reveal
--     presentation. Currently NONE (implicit in mapping prose) -> this is a
--     per-kit PROSE derivation (W4 re-emission tranche work), NOT a census-
--     cheap rider. The COLUMN lands here (v1); population defers to W4 (honest:
--     reading capstone provenance from 267 kits' prose is the re-emission job,
--     not a bulk census map). Column stays NULL at W3b apply.
ALTER TABLE canon_corpus ADD COLUMN capstone_source_acquisition TEXT
                       CHECK (capstone_source_acquisition IN
                         ('set_threshold','rune','support_gem','ascendancy','transmuter','unique_item','synergy_stack','skill_native')
                         OR capstone_source_acquisition IS NULL);

-- NOTE ON mutation_surface (spec s8): NOT a canon_corpus column. Folds into
-- kit_door_arg.mutation_surface (P0-A) per spec s8. Already defined above.

-- NOTE ON expected-section checklists (spec s8): per-game CONFIG, not per-kit
-- data. Modeled as a small reference table (W4/W5 checklist lane is queryable).
CREATE TABLE IF NOT EXISTS expected_section_checklist (
    game             TEXT NOT NULL,               -- 'd3','poe1','gd',... (matches canon_corpus.game grain)
    required_section TEXT NOT NULL,               -- 'kanai_cube','legendary_gems','gem_links','passive_tree','devotions','transmuters',...
    rationale        TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (game, required_section)
);


-- =====================================================================
-- END VDM-2 DDL v1 DRAFT.  *** NOT APPLIED ***
-- Applied only in Wave W3b, after: (1) jack-ryan Gate-2 PASS on this package,
-- (2) verified backup corpus.db.pre-vdm2-schema-2026-07-22-backup + md5,
-- (3) a MIGRATION.md entry per ADR-004, (4) PRAGMA foreign_keys=ON, (5) the
-- data riders, (6) the v2.0 stamp as the FINAL statement, (7) compendium regen.
--
-- SUMMARY vs v0: identical structure + 2 CHECK-enum additions (A-1 range_band
-- 'self', A-4 arg_type 'real'), both on v1-NEW tables (no rebuild, no VDM-1
-- touch); A-2/A-3 are DATA-row seeds (live in the rider SQL); A-5/A-6 are
-- doc-only; A-7 is rider behavior. 12 new tables + 9 additive columns across
-- 2 existing tables. ZERO breaking. G5 clean.
-- =====================================================================
