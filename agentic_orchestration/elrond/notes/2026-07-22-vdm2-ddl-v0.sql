-- =====================================================================
-- VDM-2 DDL v0 — DRAFT — *** NOT APPLIED ***
-- =====================================================================
-- Author:      elrond (data steward)
-- Wave:        W0 (VDM-2 -> Edition-next lap, gandalf RUN-CONDUCTOR)
-- Charter:     agentic_orchestration/gandalf/notes/2026-07-22-vdm2-edition-next-lap-charter.md
-- Companion:   2026-07-22-vdm2-schema-diff-and-ddl-v0.md  (diff report + migration plan)
-- Target:      agentic_orchestration/research/curated/corpus.db  @ v1.1-verified
-- Governs:     spec = matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md
--
-- STATUS: THIS FILE IS A DRAFT. IT HAS NOT BEEN RUN AGAINST corpus.db.
--         Application is Wave W3 (jack-ryan Gate-2 first, backup first,
--         MIGRATION.md entry per ADR-004). This wave = analysis + draft ONLY.
--
-- DESIGN LAW (from the diff report; read it before applying):
--   * ADDITIVE-FIRST. Zero DROP/ALTER-of-existing-column. Every VDM-1 row
--     stays valid; kit_master (574) recomputes unchanged; the 469+ frozen
--     cell_keys stay byte-identical.
--   * The spec was INFERRED from a rendered D3 viewer (its own s0.2). The
--     actual store is NORMALIZED RELATIONAL, not a flat JSON record. The
--     spec's flat blocks (door args, geometry{}, numerics{}, deviations[],
--     recognition_hooks[], acceptance{}) are re-homed here as SIDE-CAR
--     TABLES keyed to kit_id, NOT as JSON columns on canon_corpus. This is
--     the single largest correction the diff produced.
--   * source-anchored + reversible + tagged-not-encoded + versioned
--     (elrond schema principles). Every new fact traces to its origin.
--   * Gate G5: no breaking change forced by non-D3 pilot kits. Nothing
--     below is breaking; the pilot (W2) is the refutation surface.
--
-- PRIORITY ORDER matches spec s1: P0 door-args + P0 deviations first,
-- then P1 geometry + P1 dual-numerics, then P2 hooks + acceptance, then
-- housekeeping. Each block is independently applyable.
-- =====================================================================


-- =====================================================================
-- BLOCK 0 -- STAMP GUARD (informational; the real stamp is written by the
--            W3 migration script AFTER a verified backup, not here)
-- =====================================================================
-- Precondition assert the W3 script MUST run before any statement below:
--   SELECT version FROM corpus_schema_meta ORDER BY rowid DESC LIMIT 1;
--   -- MUST equal 'v1.1-deprecation-source_urls' / 'v1.1-verified'
-- The final line of the W3 migration (NOT here) will be:
--   INSERT INTO corpus_schema_meta(version, applied_utc, note)
--   VALUES ('v2.0', '<utc>', 'VDM-2 schema landing ... <full note>');


-- #####################################################################
-- ## P0-A -- TYPED DOOR-ARGS REGISTRY  (spec s2)
-- #####################################################################
-- Spec model: each door in the T4 registry gets a typed arg schema; bare
--   usage stays legal (all args default). Season mutation_surface (s8)
--   reduces to per-arg locked|mutable.
-- Ground truth: doors live TODAY as a bare JSON array kit_mapping.mapping_json
--   ->'$.t4_doors' (e.g. ["DUAL_PROXY","PERSISTENCE_ENGINE_uptime"]). ~28
--   distinct doors on record-270. NO arg schema anywhere. Bare usage IS the
--   current universal state, so "bare stays legal" is automatically satisfied
--   -- these tables are the OPTIONAL typed overlay.
-- Re-home decision: TWO registry tables (door def + per-arg def) + ONE
--   per-kit binding table. NOT a JSON blob: doors are a closed shared
--   vocabulary (registry), and per-arg locked|mutable is a queryable QA
--   surface (machine-checkable coverage), so relational wins.

-- 0.1 The door catalogue: one row per distinct door token in the registry.
CREATE TABLE IF NOT EXISTS door_registry (
    door_name        TEXT PRIMARY KEY,          -- e.g. 'DUAL_PROXY'; matches t4_doors tokens
    door_status      TEXT NOT NULL DEFAULT 'active'
                       CHECK (door_status IN ('active','deprecated','proposed')),
    rfc_ref          TEXT,                       -- new doors require full RFC (spec s2); pointer to it
    description      TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);

-- 0.2 Per-door arg schema: one row per (door, arg). Declares type, the
--     legal-value enum (as JSON array, tagged-not-encoded), and the DEFAULT
--     that "bare usage" implies. This is the registry-wide typed schema.
CREATE TABLE IF NOT EXISTS door_arg_schema (
    door_name        TEXT NOT NULL REFERENCES door_registry(door_name),
    arg_name         TEXT NOT NULL,              -- e.g. 'sync_mode'
    arg_type         TEXT NOT NULL
                       CHECK (arg_type IN ('enum','int','ref','bool','list','duration_s','pct')),
    enum_values      TEXT,                       -- JSON array of legal values when arg_type='enum'
    default_value    TEXT,                       -- the value bare usage assumes (spec: "all args default")
    arg_rfc_ref      TEXT,                        -- new ARG VALUE = cheap mini-RFC (spec s2); pointer
    notes            TEXT,
    PRIMARY KEY (door_name, arg_name)
);

-- 0.3 Per-kit door binding: the ACTUAL args a given kit sets on a door it
--     uses, PLUS the mutation_surface flag (spec s8 folds into this exact
--     row -- no separate mechanism). One row per (kit, door, arg) actually
--     bound. Kits that leave a door bare simply have no rows here for that
--     arg -> the default from door_arg_schema applies. Migration (spec s2):
--     derive args from dossier/mapping prose where derivable; else leave
--     unbound and open a deviation (P0-B) with class='param_gap'.
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
    -- does not declare. (door_name,arg_name) is the PK of door_arg_schema.
    FOREIGN KEY (door_name, arg_name) REFERENCES door_arg_schema(door_name, arg_name)
);
CREATE INDEX IF NOT EXISTS idx_kda_kit  ON kit_door_arg(kit_id);
CREATE INDEX IF NOT EXISTS idx_kda_door ON kit_door_arg(door_name);
CREATE INDEX IF NOT EXISTS idx_kda_mut  ON kit_door_arg(mutation_surface);


-- #####################################################################
-- ## P0-B -- STRUCTURED DEVIATIONS + AUTO-DOCKET WIRING  (spec s3)
-- #####################################################################
-- Spec model: deviation prose -> structured deviations[] with
--   class in {engine_inexpressible, param_gap, accepted_downgrade}; classes
--   {engine_inexpressible,param_gap} AUTO-open a mechanic_gap_docket;
--   accepted_downgrade REQUIRES an owner sign-off field.
-- Ground truth: deviation prose lives TODAY as the unstructured column
--   kit_mapping.deviation_notes (free text, per kit). mechanic_gap_docket
--   EXISTS (19 rows, all matt-ratified from VDM-1) but has NO deviation_class,
--   NO per-kit FK, NO hook_refs, NO structured proposed_fix. So: one NEW
--   side-car table for the structured deviation, and a light ADDITIVE
--   extension to the existing docket for the wiring link.
-- Re-home decision: kit_deviation is a NEW table (1-to-many per kit).
--   deviation_notes stays as the reversible raw prose source (never dropped).

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
    -- accepted_downgrade REQUIRES owner sign-off (spec s3: "silent downgrades
    -- are the failure mode this section exists to kill"). Enforced by CHECK:
    downgrade_owner  TEXT,                          -- sign-off handle; mandatory when class=accepted_downgrade
    downgrade_signoff_date TEXT,
    docket_id        INTEGER REFERENCES mechanic_gap_docket(docket_id),  -- set by auto-wire when class in (EI,PG)
    source_anchor    TEXT,                           -- verbatim deviation prose the row derived from
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    -- WIRING RULE 1 (spec s3): accepted_downgrade => owner sign-off present.
    CHECK (deviation_class <> 'accepted_downgrade' OR downgrade_owner IS NOT NULL),
    -- WIRING RULE 2 (spec s3): the two auto-docket classes SHOULD carry a
    -- docket_id once the auto-wire has run; accepted_downgrade must NOT open
    -- a docket (it is absorbed by sign-off). Soft-enforced (docket_id nullable
    -- at insert; the W4 emitter opens the docket then back-fills docket_id).
    CHECK (deviation_class = 'accepted_downgrade' OR docket_id IS NULL OR docket_id > 0)
);
CREATE INDEX IF NOT EXISTS idx_kdev_kit    ON kit_deviation(kit_id);
CREATE INDEX IF NOT EXISTS idx_kdev_class  ON kit_deviation(deviation_class);
CREATE INDEX IF NOT EXISTS idx_kdev_docket ON kit_deviation(docket_id);

-- ADDITIVE extension to the EXISTING docket so an auto-opened VDM-2 docket
-- is distinguishable from the 19 VDM-1 matt-ratified rows and traces back to
-- its source deviation + kit. (No existing docket column is touched.)
ALTER TABLE mechanic_gap_docket ADD COLUMN source_deviation_id INTEGER REFERENCES kit_deviation(deviation_id);
ALTER TABLE mechanic_gap_docket ADD COLUMN source_kit_id       TEXT;   -- single kit that auto-opened it (vs evidence_kits array)
ALTER TABLE mechanic_gap_docket ADD COLUMN intake_lane         TEXT;   -- 'mint' (source-side, existing) | 'deviation' (engine-side, NEW second intake)
-- NOTE: new auto-opened dockets take status='open' (the table default),
-- which cleanly distinguishes them from the 19 'matt-ratified' VDM-1 rows.
-- Triage happens at RESOLUTION, not at open (spec s3).


-- #####################################################################
-- ## P1-A -- GEOMETRY BANDS  (spec s4)
-- #####################################################################
-- Spec model: enumerated, sim-executable bands (delivery_class, width/range/
--   speed bands, pierce/chain/fork, count_per_cast, count_multiplier{x,source},
--   cadence_class, motion_signature enum) + optional exact{} overlay from
--   datamine lanes. Bands required on T1/T2; adjectival prose demoted to notes.
-- Ground truth: geometry lives TODAY split across
--   (a) kit_mapping.mapping_json->'$.skills[].geometry_value' (single coarse
--       enum: line|self_buff|melee_arc|beam|zone|...),
--   (b) mapping_json->'$.skills[].delivery_notes' (adjectival prose: "narrow
--       pierce projectile", "tripling projectile delivery" <- count_multiplier
--       stranded here),
--   (c) kit_dossier family='skill_geometry' payload_json (delivery/range/etc.
--       as prose: "medium-long range" @ conf 0.82 -- exactly the adjectives),
--   (d) canon_engine_key.geometry_value + delivery_value + cell_key slots.
--   NO band structure. count_multiplier prose-only. So the bands are a NEW
--   structured re-emission of data already present in (a)-(d).
-- Re-home decision: a NEW per-skill geometry-band table. A kit can have
--   multiple skills (Masquerade has 3), and geometry is PER SKILL, so the
--   grain is (kit_id, skill_ordinal). This is a critical divergence from the
--   spec's flat single-geometry{} block, which assumes one geometry per kit
--   (D3 single-skill bias). MULTI-SKILL kits (PoE support-gem stacks, GD
--   multi-skill loops) would MISFIT a flat block -> per-skill grain required.

CREATE TABLE IF NOT EXISTS skill_geometry_band (
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    skill_ordinal    INTEGER NOT NULL,            -- 0-based index into mapping_json.skills[]
    source_skill     TEXT,                         -- echoes mapping_json.skills[].source_skill for legibility
    delivery_class   TEXT
                       CHECK (delivery_class IN ('projectile','beam','zone','motion','aura','summon_delegate','melee_arc') OR delivery_class IS NULL),
    origin           TEXT,                         -- free text: 'self' | 'self_and_proxies' | ...
    width_band       TEXT CHECK (width_band IN ('narrow','medium','wide') OR width_band IS NULL),
    range_band       TEXT CHECK (range_band IN ('melee','short','medium','long','screen') OR range_band IS NULL),
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
    -- optional exact{} overlay: datamine lanes ONLY (spec s4). Reserved. Kept
    -- as a small typed set of columns + a source_type; never blocks a kit.
    exact_json       TEXT,                          -- {value, units, ...} from D2 txt / GD DBR / PoB-RePoE / TQ dbr
    exact_source_type TEXT,                         -- 'd2_missiles_txt' | 'gd_dbr' | 'poe_repoe' | 'tq_dbr' | NULL
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (kit_id, skill_ordinal)
);
CREATE INDEX IF NOT EXISTS idx_sgb_kit      ON skill_geometry_band(kit_id);
CREATE INDEX IF NOT EXISTS idx_sgb_delivery ON skill_geometry_band(delivery_class);
CREATE INDEX IF NOT EXISTS idx_sgb_cadence  ON skill_geometry_band(cadence_class);

-- motion_signature is a CLASSIFICATION task against a canonical, growable
-- named-path registry (spec s4: pick a named path, don't derive spiral math).
-- Registry table keeps the enum open + documents each path's engine impl.
CREATE TABLE IF NOT EXISTS motion_signature_registry (
    signature_name   TEXT PRIMARY KEY,             -- 'straight_line','spiral_out','orbit_fixed','sine','mortar_arc','wall_sweep',...
    engine_impl_ref  TEXT,                          -- pointer to the canonical engine implementation
    description      TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);


-- #####################################################################
-- ## P1-B -- DUAL-COLUMN NUMERICS + NORMALIZATION-RULE REGISTRY  (spec s5)
-- #####################################################################
-- Spec model: numerics{} = {source_value (immutable, anchored, VERIFY
--   territory), source_scale, rdr_value (derived by a registered rule),
--   rule}. rdr_value derived by a VERSIONED normalization rule (registry
--   owned by battle-sim team). Sim reads rdr_value ONLY. Re-running a rule
--   re-derives every dependent rdr_value corpus-wide.
-- Ground truth: source-scale numerics (83% DR, 5500% set-mult) live TODAY
--   ONLY as prose inside mapping_json delivery_notes / fidelity_notes and
--   dossier payloads. NO structured numeric anywhere; NO normalization-rule
--   registry; NO rdr_value. Wholly new.
-- Re-home decision: a NEW per-numeric table (a kit has many numerics), keyed
--   (kit_id, numeric_key), + a NEW versioned rule registry. The rule
--   registry is engine-adjacent (spec: "owned by the battle-sim team") --
--   see the diff report's cross-seam note: the REGISTRY of rules may need a
--   star-lord/gamora sign-off on rule SEMANTICS even though the TABLE lives
--   in corpus.db (elrond seam). ADR-004 escalation flagged, not resolved here.

CREATE TABLE IF NOT EXISTS normalization_rule (
    rule_id          TEXT PRIMARY KEY,             -- e.g. 'N-D3-SET-01'
    rule_version     INTEGER NOT NULL DEFAULT 1,   -- VERSIONED: bump re-derives dependents corpus-wide
    source_scale     TEXT NOT NULL,                -- the scale this rule consumes, e.g. 'd3_set_pct_bonus'
    description      TEXT NOT NULL,                -- e.g. 'D3 set multipliers map into the RDR T4 multiplier band'
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
-- Spec model: recognition_hooks[] = ranked {id, rank, type, hook, expressed_by,
--   provenance?}. QA rule: mapping status cannot be CLOSE while any hook is
--   neither expressed_by-resolved NOR covered by an accepted_downgrade
--   deviation. Coverage is machine-checkable.
-- Ground truth: NONE. The concept is "operative but implicit" in the current
--   deviation prose (spec s6). Wholly new. H4 exists ONLY via player
--   attestation -> provenance lane needed.
-- Re-home decision: NEW per-kit hook table (1-to-many). hook_refs in
--   kit_deviation (P0-B) point at these ids. The coverage QA is a VIEW /
--   app-level check, not a trigger (kept flexible).

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
-- Spec model: acceptance{signature:[{assert,hook,expected?}], delta_t4:{shape,
--   asserts[]}}. Red-test doctrine: asserts allowed to fail; a failing assert
--   routes to a docket (never a silent pass). delta_t4.shape encodes the
--   attested experience target (step vs ramp); step claims are human-validated
--   (review book), never self-certified.
-- Ground truth: NONE. Wholly new.
-- Re-home decision: TWO tables -- signature asserts (many per kit) and a
--   per-kit delta_t4 header (1 per kit, carries the shape field) + its asserts.

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
    asserts_json     TEXT,                          -- JSON array of the T4 transition asserts (e.g. 'projectiles_per_cast: 1 -> 3')
    -- 'step' claims are human-validated in the review book, NEVER self-certified
    -- (charter red-test doctrine). This flag records the sign-off state.
    shape_signoff    TEXT NOT NULL DEFAULT 'unvalidated'
                       CHECK (shape_signoff IN ('unvalidated','human-validated')),
    shape_signoff_by TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);


-- #####################################################################
-- ## P3 -- VERIFY EXTENSION  (spec s7)
-- #####################################################################
-- Spec model: verdict coverage extends to the mechanics dossier (geometry
--   bands, numerics.source_value, skill loop) for T1/T2; anchor-entailment
--   lint (ANCHOR_WEAK, hygiene queue, never auto-CONTRADICTED); NEW verdict
--   source 'player_attested'; rubber-stamp detector applies.
-- Ground truth: verify_ledger EXISTS with claim_family already INCLUDING
--   'mechanics' (530 CONFIRMED / 25 CONTRADICTED / 42 UNSUPPORTED). So the
--   FAMILY exists; what the spec wants is FINER-GRAINED mechanics verdicts
--   (per geometry band, per numeric) + a lint flag + a source lane. This is
--   an ADDITIVE column extension to the EXISTING table, NOT a new family and
--   NOT a new table. This is a correction vs the spec's assumption that
--   mechanics verdicts don't yet exist.
-- CHECK-safety note: verify_ledger.claim_family and .verdict already carry
--   CHECK constraints. Adding a value to a CHECK requires a table rebuild in
--   SQLite (CHECKs can't be ALTERed). We DO NOT touch those CHECKs (no new
--   family/verdict value needed). We only ADD nullable columns, which is safe.

ALTER TABLE verify_ledger ADD COLUMN claim_subject TEXT;   -- fine-grained target: 'geometry.range_band' | 'numeric.dr_masq' | 'skill_loop' | NULL(=coarse VDM-1 row)
ALTER TABLE verify_ledger ADD COLUMN anchor_lint   TEXT
                       CHECK (anchor_lint IN ('OK','ANCHOR_WEAK') OR anchor_lint IS NULL);  -- spec s7 lint; hygiene only, never auto-escalates
ALTER TABLE verify_ledger ADD COLUMN source_lane   TEXT
                       CHECK (source_lane IN ('crawled','player_attested','dataset','official') OR source_lane IS NULL);  -- spec s7 new 'player_attested' lane
-- run_tag already exists (default 'vdm1'); VDM-2 mechanics rows set run_tag='vdm2'.
-- rubber-stamp detector is a QUERY over (run_tag='vdm2', claim_family='mechanics')
-- contradiction rate, not a schema object.


-- #####################################################################
-- ## HOUSEKEEPING  (spec s8 + charter W0 housekeeping list)
-- #####################################################################
-- All ADDITIVE columns on canon_corpus. Data population is W3/W4, NOT here.
-- Each is a DERIVATION whose rule the diff report pins (some are trivial,
-- several are NOT -- see the diff report's "housekeeping is not free" section).

-- H1. corpus_class -- record|annex per Q34 (poe1+d2+gd+poe2+le = 270 record;
--     other games = annex). DERIVED FROM the existing corpus_bucket (100%
--     non-NULL, verified). NOTE THE FORK (diff report): 11 rows are
--     is_system=1 system-records with NO kit_mapping; the charter says
--     "corpus_class 574/574" but there are 585 rows. Enum here admits a
--     third value 'system' so all 585 get a class; the record|annex count
--     stays 270|304 over the 574 kit_master rows. Conductor confirms.
ALTER TABLE canon_corpus ADD COLUMN corpus_class TEXT
                       CHECK (corpus_class IN ('record','annex','system') OR corpus_class IS NULL);

-- H2. eras_normalized -- NOT a trivial copy. eras TODAY is per-game,
--     semicolon-delimited shorthand ('3.0-3.6;3.7-3.13','lod;d2r','aom-2017;
--     patch-1.1-1.2'). Normalization needs a per-game era map (diff report
--     flags this as a real derivation task). Column reserved; the map is a
--     W3 rider input. Raw 'eras' preserved (reversible).
ALTER TABLE canon_corpus ADD COLUMN eras_normalized TEXT;

-- H3. original_element -- PROMOTION of existing elem_raw. VERIFIED: elem_raw
--     is 100% non-NULL on record-270 (270/270, zero blanks), so promotion is
--     total on-record (charter precondition MET). elem_raw stays as the raw
--     source (never dropped; tagged-not-encoded).
ALTER TABLE canon_corpus ADD COLUMN original_element TEXT;

-- H4. court -- element-courts k=5 {fire,cold,lightning,physical,chaos-poison}
--     per Q38, DERIVED from elem_raw. NOT a trivial map: elem_raw has ~21
--     distinct values on-record incl. 'physical?','void','aether','acid',
--     'necrotic','vitality','magic','n/a','mixed(...)'. The k=5 court
--     assignment for the non-canonical tokens is an OPEN DERIVATION QUESTION
--     (diff report open-Q). Column + CHECK reserved; the elem_raw->court map
--     is a W3 rider input requiring conductor/Q38 confirmation for the tail.
ALTER TABLE canon_corpus ADD COLUMN court TEXT
                       CHECK (court IN ('fire','cold','lightning','physical','chaos-poison') OR court IS NULL);

-- H5. atlas_coords on-record -- the 13-dim mechanical tuple, local to the kit
--     (spec s8). ALREADY PRESENT as canon_engine_key.cell_key (strict-13
--     pipe-serialization, 268/270 on-record) + the compact lattice_coord.
--     This column is a PROMOTION/DENORMALIZATION so pinnacle synthesis +
--     season mutation read coords without an atlas join (spec s8 rationale).
--     2 record kits lack cell_key (poe1-blood-magic-kit, d2-teleport-sorc) ->
--     stay NULL honestly. Reversible (cell_key is the source of truth).
ALTER TABLE canon_corpus ADD COLUMN atlas_coords TEXT;

-- H6. capstone_source_acquisition -- spec s8 enum; drives T4 reveal
--     presentation (a set_threshold kit stages T4 as an equip moment). Maps
--     to the spec's capstone.source_acquisition. Currently: NONE (implicit in
--     mapping prose). New.
ALTER TABLE canon_corpus ADD COLUMN capstone_source_acquisition TEXT
                       CHECK (capstone_source_acquisition IN
                         ('set_threshold','rune','support_gem','ascendancy','transmuter','unique_item','synergy_stack','skill_native')
                         OR capstone_source_acquisition IS NULL);

-- NOTE ON mutation_surface (spec s8): it is NOT a canon_corpus column. It
-- folds into kit_door_arg.mutation_surface (P0-A) per spec s8 ("per door-arg
-- locked|mutable ... no separate mechanism required"). Already defined above.

-- NOTE ON expected-section checklists (spec s8): per-source-game required-
-- section list that reclassifies a null as 'extraction_gap'. This is a
-- CONFIGURATION artifact (per-game), not per-kit data. Modeled as a small
-- reference table so the W4/W5 checklist lane is queryable.
CREATE TABLE IF NOT EXISTS expected_section_checklist (
    game             TEXT NOT NULL,               -- 'd3','poe1','gd',... (matches canon_corpus.game grain)
    required_section TEXT NOT NULL,               -- 'kanai_cube','legendary_gems','gem_links','passive_tree','devotions','transmuters',...
    rationale        TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (game, required_section)
);


-- =====================================================================
-- END VDM-2 DDL v0 DRAFT.  *** NOT APPLIED ***
-- Applied only in Wave W3, after: (1) jack-ryan Gate-2, (2) verified
-- backup (corpus.db.pre-vdm2-schema-<date>-backup), (3) a MIGRATION.md
-- entry per ADR-004, (4) the v2.0 stamp as the FINAL statement.
-- Gate G5 pin: if a non-D3 pilot kit (W2) forces any statement above to
-- become breaking, that is a GATE-FAIL FINDING, not a forced march.
-- =====================================================================
