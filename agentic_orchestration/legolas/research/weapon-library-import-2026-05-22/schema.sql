-- =============================================================================
-- Weapon Library DB Schema v1
-- Target: /Users/admin/Games/reincarnated-loadout/data/telemetry.db (SQLite)
-- Authored: 2026-05-22 (legolas, Mode A+B mixed commission)
-- Status: PROPOSED — pending Matt approval before execution
-- Greenfield: DB is 0 bytes / no schema / no React cross-references as of 2026-05-22
-- =============================================================================
-- Rationale doc: sql-ddl-proposal.md (this directory)
-- Canonical tag schema: metadata-normalization.md (this directory)
-- Selection patterns: selection-patterns.md (this directory)
-- =============================================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- =============================================================================
-- SECTION 1: REFERENCE / LOOKUP TABLES
-- =============================================================================

-- ---------------------------------------------------------------------------
-- libraries: registry of source libraries
-- One row per import source. Tracks API metadata + import status.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS libraries (
    library_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT    NOT NULL UNIQUE,  -- "sketchfab", "meshy", "smithsonian", etc.
    display_name  TEXT    NOT NULL,
    base_url      TEXT    NOT NULL,
    api_url       TEXT,                     -- NULL if no API
    import_tier   INTEGER NOT NULL,        -- 1/2/3 per import strategy
    license_class TEXT    NOT NULL,        -- "cc0_only" / "cc_mixed" / "royalty_free_commercial" / "mixed"
    notes         TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------------
-- licenses: license tier registry
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS licenses (
    license_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    slug               TEXT    NOT NULL UNIQUE, -- "CC0", "CC_BY", "CC_BY_SA", "royalty_free_commercial", etc.
    display_name       TEXT    NOT NULL,
    commercial_ok      INTEGER NOT NULL DEFAULT 0,  -- 1=yes, 0=no
    attribution_req    INTEGER NOT NULL DEFAULT 0,  -- 1=yes, 0=no
    share_alike        INTEGER NOT NULL DEFAULT 0,  -- 1=yes (CC-SA)
    nc_restriction     INTEGER NOT NULL DEFAULT 0,  -- 1=non-commercial only (REJECT for game)
    game_approved      INTEGER NOT NULL DEFAULT 0,  -- 1=approved for shipping game use
    notes              TEXT
);

-- Seed data for known license tiers
INSERT OR IGNORE INTO licenses
    (slug, display_name, commercial_ok, attribution_req, share_alike, nc_restriction, game_approved, notes)
VALUES
    ('CC0',                    'CC0 Public Domain',                1, 0, 0, 0, 1, 'No restrictions; ideal for shipping product'),
    ('CC_BY',                  'CC Attribution 4.0',              1, 1, 0, 0, 1, 'Attribution required; acceptable for indie release with credits'),
    ('CC_BY_SA',               'CC Attribution-ShareAlike 4.0',   1, 1, 1, 0, 0, 'Share-alike complicates derivative product; caution'),
    ('CC_BY_NC',               'CC Attribution-NonCommercial',     0, 1, 0, 1, 0, 'REJECT — non-commercial restriction'),
    ('CC_BY_NC_SA',            'CC Attribution-NonCommercial-SA',  0, 1, 1, 1, 0, 'REJECT — non-commercial restriction'),
    ('CC_BY_NC_ND',            'CC Attribution-NonCommercial-ND',  0, 1, 0, 1, 0, 'REJECT — non-commercial restriction'),
    ('royalty_free_commercial','Royalty-Free Commercial Perpetual',1, 0, 0, 0, 1, 'TurboSquid/CGTrader; perpetual, no resale of model files'),
    ('OGA_BY',                 'OGA-BY 3.0/4.0',                  1, 1, 0, 0, 1, 'Attribution to OGA required; functionally CC-BY'),
    ('editorial_only',         'Editorial License Only',           0, 0, 0, 0, 0, 'REJECT — news/academic use only'),
    ('unknown',                'License Unknown',                  0, 0, 0, 0, 0, 'REJECT until clarified'),
    ('GPL2',                   'GNU GPL v2',                       0, 1, 1, 0, 0, 'REJECT — incompatible with closed-source product'),
    ('GPL3',                   'GNU GPL v3',                       0, 1, 1, 0, 0, 'REJECT — incompatible with closed-source product');

-- ---------------------------------------------------------------------------
-- tag_taxonomy: canonical controlled vocabulary
-- Normalizes all tag types: weapon_class, cultural_lineage, tech_level, tone, etc.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tag_taxonomy (
    tag_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_namespace   TEXT    NOT NULL,  -- "weapon_class" / "cultural_lineage" / "tech_level" / "tone" / "style_register" / "range_class" / "geometry_class" / "tempo_class" / "misc"
    tag_value       TEXT    NOT NULL,
    wikidata_qid    TEXT,              -- e.g., "Q13442" for sword; NULL if no Wikidata equivalent
    display_label   TEXT    NOT NULL,
    parent_tag_id   INTEGER REFERENCES tag_taxonomy(tag_id), -- for hierarchical tags
    notes           TEXT,
    UNIQUE (tag_namespace, tag_value)
);

-- Seed data: weapon_class canonical values
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, wikidata_qid, display_label) VALUES
    ('weapon_class', 'sword',             'Q13442',  'Sword'),
    ('weapon_class', 'dagger',            'Q571',    'Dagger'),
    ('weapon_class', 'polearm',           'Q44448',  'Polearm / Spear'),
    ('weapon_class', 'bow',               'Q9134',   'Bow'),
    ('weapon_class', 'crossbow',          'Q20484',  'Crossbow'),
    ('weapon_class', 'firearm',           'Q841628', 'Firearm'),
    ('weapon_class', 'thrown',            'Q1148715','Thrown Weapon'),
    ('weapon_class', 'staff',             NULL,      'Staff / Longstaff'),
    ('weapon_class', 'wand',              NULL,      'Wand / Focus Rod'),
    ('weapon_class', 'orb',               NULL,      'Orb / Sphere'),
    ('weapon_class', 'tome',              'Q49848',  'Tome / Grimoire'),
    ('weapon_class', 'hammer_mace',       'Q41137',  'Hammer / Mace'),
    ('weapon_class', 'axe',               'Q42948',  'Axe'),
    ('weapon_class', 'shield',            'Q131529', 'Shield'),
    ('weapon_class', 'ritual_instrument', 'Q220659', 'Ritual Instrument'),
    ('weapon_class', 'other',             NULL,      'Other / Unknown');

-- Seed data: range_class
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('range_class', 'melee',    'Melee (≤3 units)'),
    ('range_class', 'medium',   'Medium (3–8 units)'),
    ('range_class', 'ranged',   'Ranged (≥8 units)'),
    ('range_class', 'indirect', 'Indirect (no direct range — summoner/ritual)');

-- Seed data: geometry_class (per BDI ω-field / canonical-09 geometry palette)
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('geometry_class', 'point',       'Point (single-target)'),
    ('geometry_class', 'line',        'Line / Projectile'),
    ('geometry_class', 'arc_sweep',   'Arc / Sweep'),
    ('geometry_class', 'scatter',     'Scatter / Spread'),
    ('geometry_class', 'area_aura',   'Area Aura'),
    ('geometry_class', 'cone_aoe',    'Cone AOE'),
    ('geometry_class', 'beam',        'Beam / Channel'),
    ('geometry_class', 'indirect',    'Indirect / Conjured');

-- Seed data: tempo_class
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('tempo_class', 'fast',      'Fast (daggers, chakram, wand)'),
    ('tempo_class', 'measured',  'Measured (bow, spear, wand)'),
    ('tempo_class', 'slow',      'Slow (greatsword, staff, blunderbuss)'),
    ('tempo_class', 'channeled', 'Channeled (orb, censer, horn charge)');

-- Seed data: tech_level
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('tech_level', 'primitive',    'Primitive / Stone Age'),
    ('tech_level', 'ancient',      'Ancient (pre-500 CE)'),
    ('tech_level', 'medieval',     'Medieval (500–1500 CE)'),
    ('tech_level', 'early_modern', 'Early Modern (1500–1800)'),
    ('tech_level', 'industrial',   'Industrial (1800–1950)'),
    ('tech_level', 'advanced',     'Advanced / Near Future'),
    ('tech_level', 'sci_fi',       'Sci-Fi / Far Future'),
    ('tech_level', 'fantasy',      'Fantasy (anachronistic tech)');

-- Seed data: cultural_lineage
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('cultural_lineage', 'european',       'European'),
    ('cultural_lineage', 'east_asian',     'East Asian'),
    ('cultural_lineage', 'south_asian',    'South Asian'),
    ('cultural_lineage', 'middle_eastern', 'Middle Eastern'),
    ('cultural_lineage', 'african',        'African'),
    ('cultural_lineage', 'mesoamerican',   'Mesoamerican'),
    ('cultural_lineage', 'native_american','Native American'),
    ('cultural_lineage', 'oceanic',        'Oceanic'),
    ('cultural_lineage', 'fictional',      'Fictional / Invented'),
    ('cultural_lineage', 'cross_cultural', 'Cross-Cultural / Hybrid'),
    ('cultural_lineage', 'unknown',        'Unknown');

-- Seed data: tone
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('tone', 'heroic',   'Heroic'),
    ('tone', 'grim',     'Grim / Dark'),
    ('tone', 'sacred',   'Sacred / Holy'),
    ('tone', 'profane',  'Profane / Cursed'),
    ('tone', 'arcane',   'Arcane / Mystical'),
    ('tone', 'brutal',   'Brutal / Savage'),
    ('tone', 'elegant',  'Elegant / Noble'),
    ('tone', 'utility',  'Utility / Functional');

-- Seed data: style_register
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('style_register', 'realistic',     'Realistic'),
    ('style_register', 'stylized',      'Stylized'),
    ('style_register', 'low_poly',      'Low Poly'),
    ('style_register', 'cartoon',       'Cartoon'),
    ('style_register', 'hand_painted',  'Hand Painted'),
    ('style_register', 'photorealistic','Photorealistic'),
    ('style_register', 'voxel',         'Voxel');

-- Seed data: gear catalogue IDs (maps to 15-gear catalogue)
INSERT OR IGNORE INTO tag_taxonomy (tag_namespace, tag_value, display_label) VALUES
    ('gear_catalogue', '1',  'Greatsword'),
    ('gear_catalogue', '2',  'Twin Daggers'),
    ('gear_catalogue', '3',  'Battle Spear / Longstaff'),
    ('gear_catalogue', '4',  'Mace / Warhammer'),
    ('gear_catalogue', '5',  'Longbow'),
    ('gear_catalogue', '6',  'Crossbow'),
    ('gear_catalogue', '7',  'Blunderbuss / Scattergun'),
    ('gear_catalogue', '8',  'Throwing Knives / Chakram'),
    ('gear_catalogue', '9',  'Wand / Focus Rod'),
    ('gear_catalogue', '10', 'Orb / Sphere'),
    ('gear_catalogue', '11', 'Caster Staff'),
    ('gear_catalogue', '12', 'Tome / Grimoire'),
    ('gear_catalogue', '13', 'Censer / Thurible'),
    ('gear_catalogue', '14', 'Holy Symbol / Icon'),
    ('gear_catalogue', '15', 'War-Trumpet / Horn');


-- =============================================================================
-- SECTION 2: CORE WEAPON ENTITY
-- =============================================================================

-- ---------------------------------------------------------------------------
-- weapons: one row per unique imported weapon model
-- The central entity. All other tables join to this.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapons (
    weapon_id          INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Identity
    display_name       TEXT    NOT NULL,
    weapon_subclass    TEXT,                -- Free-text: "greatsword", "katana", "flintlock", etc.
    description        TEXT,               -- Source description (may be truncated)

    -- Sim-property fields (mechanical substrate-vector matching predicates)
    range_class        TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (range_class IN ('melee','medium','ranged','indirect','unknown')),
    geometry_class     TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (geometry_class IN ('point','line','arc_sweep','scatter','area_aura','cone_aoe','beam','indirect','unknown')),
    tempo_class        TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (tempo_class IN ('fast','measured','slow','channeled','unknown')),
    charge_class       TEXT    NOT NULL DEFAULT 'instant'
                                CHECK (charge_class IN ('instant','short_charge','long_charge','channeled')),
    accuracy_class     TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (accuracy_class IN ('precision','spread','area','unknown')),
    rhythm_class       TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (rhythm_class IN ('single_hit','multi_hit','burst','sustained','unknown')),
    stat_affinity      TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (stat_affinity IN ('STR','INT','WIS','mixed','unknown')),

    -- Aesthetic tuple fields (cohesion-judge identity matching predicates)
    tech_level         TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (tech_level IN ('primitive','ancient','medieval','early_modern','industrial','advanced','sci_fi','fantasy','unknown')),
    tone               TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (tone IN ('heroic','grim','sacred','profane','arcane','brutal','elegant','utility','unknown')),
    cultural_lineage   TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (cultural_lineage IN ('european','east_asian','south_asian','middle_eastern','african','mesoamerican','native_american','oceanic','fictional','cross_cultural','unknown')),
    style_register     TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (style_register IN ('realistic','stylized','low_poly','cartoon','hand_painted','photorealistic','voxel','unknown')),

    -- Gear catalogue match (derived; maps to 15-gear catalogue IDs)
    gear_catalogue_id  INTEGER,           -- 1–15; NULL if no clear match or pending review
    -- NOTE: deliberately NOT a FK to tag_taxonomy to keep this fast for index scans

    -- Element affinities (derived from BDI ω-table; stored as comma-separated element list)
    dominant_element_affinities TEXT,     -- e.g., "fire,water,lightning"; NULL until ω-analysis pass
    best_omega_score            REAL,     -- Precomputed best-match ω score; updated after H3 calibration

    -- Asset-readiness state
    readiness_state    TEXT    NOT NULL DEFAULT 'needs_format_conversion'
                                CHECK (readiness_state IN (
                                    'ready_to_import',
                                    'needs_format_conversion',
                                    'needs_scale_normalization',
                                    'needs_texture_bake',
                                    'needs_meshy_regenerate',
                                    'sim_viability_unverified',
                                    'rejected'
                                )),
    verified_for_sim   INTEGER NOT NULL DEFAULT 0,  -- 1 after rocket sim-viability check
    scale_normalized   INTEGER NOT NULL DEFAULT 0,  -- 1 after scale normalization pass
    has_textures       INTEGER NOT NULL DEFAULT 0,
    has_rig            INTEGER NOT NULL DEFAULT 0,
    poly_class         TEXT    NOT NULL DEFAULT 'unknown'
                                CHECK (poly_class IN ('low','mid','high','unknown')),

    -- Timestamps
    created_at         TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at         TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------------
-- weapon_sources: per-weapon source provenance (one-to-many: one weapon may
-- appear in multiple libraries; primary source is earliest or highest-quality)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapon_sources (
    source_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    weapon_id          INTEGER NOT NULL REFERENCES weapons(weapon_id) ON DELETE CASCADE,
    library_id         INTEGER NOT NULL REFERENCES libraries(library_id),
    license_id         INTEGER NOT NULL REFERENCES licenses(license_id),
    is_primary         INTEGER NOT NULL DEFAULT 1,  -- 1 = primary source for this weapon

    -- Source-native identifiers
    source_asset_id    TEXT,             -- Library-native ID (Sketchfab UID, OGA node ID, etc.)
    source_url         TEXT    NOT NULL, -- Canonical URL to asset page
    preview_image_url  TEXT,             -- Thumbnail URL for UI
    download_url       TEXT,             -- Direct download URL (may be API-authenticated)

    -- License compliance
    attribution_required INTEGER NOT NULL DEFAULT 0,
    attribution_text   TEXT,             -- Required attribution string for CC-BY models
    license_url        TEXT,             -- URL to full license text

    -- Acquisition
    cost_usd           REAL    NOT NULL DEFAULT 0.0,
    file_format        TEXT    NOT NULL DEFAULT 'unknown',  -- Format of source file
    converted_format   TEXT,             -- Format after pipeline conversion

    -- Crawl metadata
    crawl_date         TEXT    NOT NULL DEFAULT (date('now')),
    extraction_error   TEXT,             -- Non-null if extraction had issues

    UNIQUE (library_id, source_asset_id)  -- Prevent duplicate imports from same source
);

-- ---------------------------------------------------------------------------
-- weapon_tags: many-to-many tag assignments
-- Flexible secondary tagging beyond the structured columns in weapons table
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapon_tags (
    weapon_id          INTEGER NOT NULL REFERENCES weapons(weapon_id) ON DELETE CASCADE,
    tag_id             INTEGER NOT NULL REFERENCES tag_taxonomy(tag_id),
    confidence         REAL    NOT NULL DEFAULT 1.0,  -- 1.0=explicit; <1.0=inferred
    source             TEXT    NOT NULL DEFAULT 'import',  -- "import"/"inferred"/"manual"/"api"
    PRIMARY KEY (weapon_id, tag_id)
);

-- ---------------------------------------------------------------------------
-- weapon_sim_props: detailed simulation properties
-- Separate table for sim-property details beyond the main weapons columns.
-- Allows per-property confidence scores and source tracking.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapon_sim_props (
    weapon_id          INTEGER PRIMARY KEY REFERENCES weapons(weapon_id) ON DELETE CASCADE,

    -- Range quantified
    range_min_units    REAL,             -- Minimum effective range (engine units)
    range_max_units    REAL,             -- Maximum effective range (engine units)

    -- Tempo quantified
    base_attack_speed  REAL,             -- Base attacks per second (canonical sim units)
    charge_time_s      REAL,             -- Charge time in seconds (0 for instant)

    -- Hit properties
    hits_per_attack    INTEGER,          -- Number of hits per attack action (1 for single; 2+ for multi)
    aoe_radius_units   REAL,             -- AOE radius in engine units (0 for single-target)

    -- Stat scaling
    primary_stat       TEXT    CHECK (primary_stat IN ('STR','INT','WIS')),
    secondary_stat     TEXT    CHECK (secondary_stat IN ('STR','INT','WIS','none')),

    -- Sim-viability flag (populated by rocket after verification)
    sim_viable         INTEGER NOT NULL DEFAULT 0,  -- 1=verified viable
    sim_viability_notes TEXT,
    sim_verified_date  TEXT
);

-- ---------------------------------------------------------------------------
-- weapon_aesthetic: detailed aesthetic tuple
-- Extends weapons table with multi-value aesthetic assignments
-- and confidence scores per field
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapon_aesthetic (
    weapon_id              INTEGER PRIMARY KEY REFERENCES weapons(weapon_id) ON DELETE CASCADE,

    -- Tech level + confidence
    tech_level_confidence  REAL    NOT NULL DEFAULT 0.5,  -- 1.0=structured source; 0.5=inferred; 0.3=default

    -- Cultural lineage + confidence
    cultural_lineage_confidence REAL NOT NULL DEFAULT 0.5,

    -- Secondary cultural lineages (for cross-cultural weapons)
    secondary_lineage_1    TEXT    CHECK (secondary_lineage_1 IN ('european','east_asian','south_asian','middle_eastern','african','mesoamerican','native_american','oceanic','fictional','unknown')),
    secondary_lineage_2    TEXT    CHECK (secondary_lineage_2 IN ('european','east_asian','south_asian','middle_eastern','african','mesoamerican','native_american','oceanic','fictional','unknown')),

    -- Source attribution for aesthetic values
    culture_source_field   TEXT,   -- e.g., "smithsonian_culture_field" vs "tag_inference"
    era_source_field       TEXT,   -- e.g., "smithsonian_date_field" vs "tag_inference"

    -- Aesthetic raw source data (preserved for re-normalization)
    raw_source_tags        TEXT,   -- JSON-serialized array of source tags before normalization
    raw_source_description TEXT    -- Truncated source description used for inference
);

-- ---------------------------------------------------------------------------
-- weapon_readiness: import pipeline state tracking
-- Tracks each weapon through the import pipeline stages
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapon_readiness (
    weapon_id              INTEGER PRIMARY KEY REFERENCES weapons(weapon_id) ON DELETE CASCADE,
    current_state          TEXT    NOT NULL DEFAULT 'needs_format_conversion',
    import_batch           TEXT,   -- Import batch ID (e.g., "phase-a-kenney-2026-05-25")
    format_converted       INTEGER NOT NULL DEFAULT 0,
    scale_verified         INTEGER NOT NULL DEFAULT 0,
    texture_verified       INTEGER NOT NULL DEFAULT 0,
    glb_exported           INTEGER NOT NULL DEFAULT 0,
    stored_at_path         TEXT,   -- Local path after successful import
    last_state_change      TEXT    NOT NULL DEFAULT (datetime('now')),
    state_change_notes     TEXT
);


-- =============================================================================
-- SECTION 3: DENSITY MAP TABLE
-- Tracks substrate-vector coverage for density-routing decisions.
-- Populated by aggregate queries over weapons table at import time.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- substrate_density: precomputed density map for substrate-vector → weapon count
-- Used by selection pattern P6 (density-routing to Meshy gap-fill)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS substrate_density (
    density_id         INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Substrate-vector components (matches weapons table columns)
    dominant_element   TEXT    NOT NULL,  -- fire/water/earth/wind/lightning/holy/shadow
    range_class        TEXT    NOT NULL,  -- melee/medium/ranged
    gear_catalogue_id  INTEGER NOT NULL,  -- 1–15

    -- Density metrics (updated by periodic aggregate query)
    weapon_count_total  INTEGER NOT NULL DEFAULT 0,  -- all readiness states
    weapon_count_ready  INTEGER NOT NULL DEFAULT 0,  -- readiness_state = 'ready_to_import' only
    weapon_count_cc0    INTEGER NOT NULL DEFAULT 0,  -- CC0 license only (highest preference)
    weapon_count_cc_ok  INTEGER NOT NULL DEFAULT 0,  -- CC0 + CC-BY (game_approved = 1)

    -- Routing decision (updated after each import batch)
    density_tier       TEXT    CHECK (density_tier IN ('empty','sparse','adequate','dense')),
    -- empty  = 0 ready weapons → route to Meshy gap-fill
    -- sparse = 1–2 ready weapons → flag for prioritized Meshy gap-fill
    -- adequate = 3–10 → use DB selection
    -- dense  = >10 → use ranking query

    meshy_gapfill_queued INTEGER NOT NULL DEFAULT 0,  -- 1 if Meshy gap-fill request has been queued
    last_computed      TEXT    NOT NULL DEFAULT (datetime('now')),

    UNIQUE (dominant_element, range_class, gear_catalogue_id)
);


-- =============================================================================
-- SECTION 4: INDEXES
-- Performance optimization for the most common query patterns.
-- All index rationale in sql-ddl-proposal.md.
-- =============================================================================

-- Primary selection query predicates: gear_catalogue_id + range_class + tech_level + cultural_lineage
CREATE INDEX IF NOT EXISTS idx_weapons_gear_catalogue ON weapons (gear_catalogue_id);
CREATE INDEX IF NOT EXISTS idx_weapons_range_class    ON weapons (range_class);
CREATE INDEX IF NOT EXISTS idx_weapons_tech_level     ON weapons (tech_level);
CREATE INDEX IF NOT EXISTS idx_weapons_cultural       ON weapons (cultural_lineage);
CREATE INDEX IF NOT EXISTS idx_weapons_tone           ON weapons (tone);
CREATE INDEX IF NOT EXISTS idx_weapons_style          ON weapons (style_register);
CREATE INDEX IF NOT EXISTS idx_weapons_readiness      ON weapons (readiness_state);
CREATE INDEX IF NOT EXISTS idx_weapons_verified       ON weapons (verified_for_sim);

-- Compound index for the canonical selection query (gear + range + tech + culture)
CREATE INDEX IF NOT EXISTS idx_weapons_selection_core ON weapons
    (gear_catalogue_id, range_class, tech_level, cultural_lineage, readiness_state);

-- Compound index for density-routing queries (gear + range, any element via join)
CREATE INDEX IF NOT EXISTS idx_weapons_density_vec ON weapons
    (gear_catalogue_id, range_class);

-- Source provenance: license filtering (most common secondary predicate)
CREATE INDEX IF NOT EXISTS idx_sources_license        ON weapon_sources (license_id);
CREATE INDEX IF NOT EXISTS idx_sources_library        ON weapon_sources (library_id);
CREATE INDEX IF NOT EXISTS idx_sources_weapon         ON weapon_sources (weapon_id);
CREATE INDEX IF NOT EXISTS idx_sources_primary        ON weapon_sources (weapon_id, is_primary)
    WHERE is_primary = 1;

-- Tag lookup: namespace + value
CREATE INDEX IF NOT EXISTS idx_taxonomy_namespace     ON tag_taxonomy (tag_namespace, tag_value);
CREATE INDEX IF NOT EXISTS idx_weapon_tags_weapon     ON weapon_tags (weapon_id);
CREATE INDEX IF NOT EXISTS idx_weapon_tags_tag        ON weapon_tags (tag_id);

-- Density map: all three vector components
CREATE INDEX IF NOT EXISTS idx_density_vector ON substrate_density
    (dominant_element, range_class, gear_catalogue_id);


-- =============================================================================
-- SECTION 5: VIEWS
-- Convenience views for common query patterns.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- v_weapons_ready: all weapons that are fully import-ready + license-approved
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_weapons_ready AS
SELECT
    w.*,
    ws.source_url,
    ws.preview_image_url,
    ws.license_id,
    l.slug              AS license_slug,
    l.attribution_required,
    ws.attribution_text,
    ws.cost_usd,
    lib.slug            AS library_slug
FROM weapons w
JOIN weapon_sources ws ON ws.weapon_id = w.weapon_id AND ws.is_primary = 1
JOIN licenses l        ON l.license_id = ws.license_id AND l.game_approved = 1
JOIN libraries lib     ON lib.library_id = ws.library_id
WHERE w.readiness_state = 'ready_to_import';

-- ---------------------------------------------------------------------------
-- v_weapons_cc0: CC0-licensed ready weapons only (highest license preference)
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_weapons_cc0 AS
SELECT *
FROM v_weapons_ready
WHERE license_slug = 'CC0';

-- ---------------------------------------------------------------------------
-- v_density_summary: readable density map with routing decision
-- ---------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_density_summary AS
SELECT
    sd.*,
    tt.display_label AS gear_display_name
FROM substrate_density sd
LEFT JOIN tag_taxonomy tt ON tt.tag_namespace = 'gear_catalogue'
                          AND CAST(tt.tag_value AS INTEGER) = sd.gear_catalogue_id;


-- =============================================================================
-- SECTION 6: LIBRARY SEED DATA
-- =============================================================================

INSERT OR IGNORE INTO libraries
    (slug, display_name, base_url, api_url, import_tier, license_class, notes)
VALUES
    ('sketchfab',    'Sketchfab',             'https://sketchfab.com',
     'https://api.sketchfab.com/v3',      1, 'cc_mixed',
     'CC0+CC-BY subset; Data API v3; OAuth2; weapons-military category slug'),
    ('meshy',        'Meshy.ai Library',      'https://www.meshy.ai',
     NULL,                                 1, 'cc0_only',
     'CC0 uniform; 60K+ weapons; per-asset download; FBX/GLB/OBJ'),
    ('kenney',       'Kenney.nl',             'https://kenney.nl',
     NULL,                                 1, 'cc0_only',
     'CC0 uniform; ZIP packs; GLB/OBJ/FBX; Phase A seed set'),
    ('oga',          'Open Game Art',         'https://opengameart.org',
     NULL,                                 2, 'cc_mixed',
     'CC0+CC-BY+OGA-BY subset; 389 3D weapon entries; GPL must be filtered'),
    ('smithsonian',  'Smithsonian Open Access','https://www.si.edu/openaccess',
     'https://api.si.edu/openaccess/api/v1.0', 2, 'cc0_only',
     'CC0 uniform; museum-grade metadata; api.data.gov key required; OBJ+glTF'),
    ('itchio',       'itch.io',               'https://itch.io',
     NULL,                                 2, 'mixed',
     'CC0 packs only; 986 packs (tag-3d + tag-weapons); per-pack license review required'),
    ('turbosquid',   'TurboSquid',            'https://www.turbosquid.com',
     NULL,                                 3, 'royalty_free_commercial',
     'Perpetual royalty-free; 42K+ weapons; no API; per-asset purchase'),
    ('cgtrader',     'CGTrader',              'https://www.cgtrader.com',
     NULL,                                 3, 'royalty_free_commercial',
     'Perpetual royalty-free; 127K+ weapons; no API; per-asset purchase'),
    ('renderhub',    'RenderHub',             'https://www.renderhub.com',
     NULL,                                 3, 'royalty_free_commercial',
     'Extended Use License; 100+ free weapons; OBJ/FBX/GLTF'),
    ('free3d',       'Free3D',               'https://free3d.com',
     NULL,                                 3, 'mixed',
     'Personal-use default; royalty-free tier available; 1,605 weapons; verify per model'),
    ('meshy_generated', 'Meshy Generated',   'https://www.meshy.ai',
     'https://api.meshy.ai',              1, 'cc0_only',
     'Meshy gap-fill generation output; CC0 per Meshy terms; GLB primary format'),
    ('blendswap',    'BlendSwap',            'https://www.blendswap.com',
     NULL,                                 3, 'cc0_only',
     'CC0; .blend format only; Blender conversion required; small weapon count'),
    ('fab',          'Fab (Epic Games)',      'https://www.fab.com',
     NULL,                                 3, 'royalty_free_commercial',
     'Fab Standard License; Unreal-focused; per-asset purchase');

-- =============================================================================
-- END OF SCHEMA
-- Version: 1.0.0
-- Next: run against /Users/admin/Games/reincarnated-loadout/data/telemetry.db
--       after Matt approval
-- =============================================================================
