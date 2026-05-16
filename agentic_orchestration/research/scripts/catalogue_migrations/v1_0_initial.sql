-- catalogue.db — v1.0 initial schema
-- Applied: 2026-05-16
-- Owner: elrond
-- Companion documents:
--   agentic_orchestration/research/curated/catalogue-schema.md (full schema doc)
--   agentic_orchestration/research/curated/catalogue-rubric-schema.md (six-axis rubric)
--   agentic_orchestration/research/curated/MIGRATION.md (this migration entry)
-- See catalogue-schema.md § 3 for the full rationale on each column and CHECK constraint.

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- =============================================================================
-- schema_meta — migration tracking
-- =============================================================================

CREATE TABLE schema_meta (
    version          TEXT PRIMARY KEY,
    applied_at       TEXT NOT NULL,        -- ISO-8601 timestamp
    description      TEXT NOT NULL,
    migration_script TEXT
) STRICT;

INSERT INTO schema_meta (version, applied_at, description, migration_script) VALUES (
    '1.0',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'Initial catalogue schema; six-axis style rubric v1.0; embodiment tag aligned to embodiment-narrative-layer.md v1.0',
    'catalogue_migrations/v1_0_initial.sql'
);

-- =============================================================================
-- catalogue_sources — vendor / source metadata
-- =============================================================================

CREATE TABLE catalogue_sources (
    source                  TEXT PRIMARY KEY,
    display_name            TEXT NOT NULL,
    url                     TEXT NOT NULL,
    vendor_type             TEXT NOT NULL CHECK (vendor_type IN (
        'individual-creator', 'studio-creator', 'aggregator-marketplace',
        'commons-repository', 'unknown'
    )),
    primary_register_hint   TEXT CHECK (primary_register_hint IN (
        'retro-16bit', 'hand-drawn-pixel', 'clean-vector', 'painterly-raster',
        'anime-cel', 'mixed', 'unknown'
    )),
    default_license         TEXT CHECK (default_license IN (
        'CC0', 'CC-BY', 'CC-BY-NC', 'CC-BY-SA', 'CC-BY-ND',
        'commercial-royalty-free', 'commercial-per-project', 'commercial-royalty-bearing',
        'commercial-license', 'unity-asset-store', 'proprietary', 'mixed', 'unknown'
    )),
    notes                   TEXT,
    added_at                TEXT NOT NULL
) STRICT;

-- =============================================================================
-- crawl_sessions — Legolas crawl provenance
-- =============================================================================

CREATE TABLE crawl_sessions (
    session_id              TEXT PRIMARY KEY,
    source                  TEXT NOT NULL REFERENCES catalogue_sources(source),
    legolas_version         TEXT,
    mode                    TEXT NOT NULL CHECK (mode IN (
        'mode-b-sample', 'mode-b-full-crawl', 'mode-a-supplement'
    )),
    started_at              TEXT NOT NULL,
    completed_at            TEXT,
    asset_count             INTEGER,
    raw_output_path         TEXT NOT NULL,
    curated_at              TEXT,
    notes                   TEXT
) STRICT;

-- =============================================================================
-- catalogue_packs — pack-level grouping (with pack_register_consistency advisory)
-- =============================================================================

CREATE TABLE catalogue_packs (
    pack_id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    source                      TEXT NOT NULL REFERENCES catalogue_sources(source),
    source_pack_id              TEXT,
    pack_name                   TEXT NOT NULL,
    pack_url                    TEXT,
    pack_license                TEXT CHECK (pack_license IN (
        'CC0', 'CC-BY', 'CC-BY-NC', 'CC-BY-SA', 'CC-BY-ND',
        'commercial-royalty-free', 'commercial-per-project', 'commercial-royalty-bearing',
        'commercial-license', 'unity-asset-store', 'proprietary', 'mixed', 'unknown'
    )),
    pack_cost_usd               REAL,
    asset_count                 INTEGER,
    -- Per gandalf dialogue Topic 2 addition: post-curation quality signal
    pack_register_consistency   TEXT NOT NULL DEFAULT 'unknown'
        CHECK (pack_register_consistency IN ('consistent', 'mixed', 'unknown')),
    added_at                    TEXT NOT NULL,
    UNIQUE (source, source_pack_id)
) STRICT;

-- =============================================================================
-- catalogue_assets — the primary table
-- =============================================================================

CREATE TABLE catalogue_assets (
    -- Identity + source provenance
    asset_uid                              INTEGER PRIMARY KEY AUTOINCREMENT,
    source                                 TEXT NOT NULL REFERENCES catalogue_sources(source),
    source_asset_id                        TEXT NOT NULL,
    crawl_session_id                       TEXT NOT NULL REFERENCES crawl_sessions(session_id),
    source_url                             TEXT NOT NULL,
    source_date                            TEXT NOT NULL,        -- ISO-8601 date
    source_metadata_raw                    TEXT NOT NULL,        -- JSON string preserving Legolas raw

    -- Display fields
    name                                   TEXT NOT NULL,
    description                            TEXT,

    -- Pack grouping
    pack_id                                INTEGER REFERENCES catalogue_packs(pack_id),

    -- Content classification (separate dimension from style register)
    category                               TEXT NOT NULL CHECK (category IN (
        'character', 'enemy', 'vfx', 'environment', 'ui', 'audio',
        'tile', 'icon', 'portrait', 'other'
    )),
    dimensionality                         TEXT NOT NULL DEFAULT '2d'
        CHECK (dimensionality IN ('2d', '3d')),

    -- Six-axis style rubric (see catalogue-rubric-schema.md)
    rubric_version                         TEXT NOT NULL DEFAULT '1.0',
    resolution_band                        TEXT NOT NULL CHECK (resolution_band IN (
        'tiny', 'retro', 'hd2d-pixel', 'narrative-pixel', 'cinematic-pixel',
        'raster', 'vector', 'unknown'
    )),
    palette_size                           TEXT NOT NULL CHECK (palette_size IN (
        '16-color', 'restricted', 'expansive', 'truecolor', 'unknown'
    )),
    shading_technique                      TEXT NOT NULL CHECK (shading_technique IN (
        'flat-fill', 'single-step', 'dithered', 'gradient-ramp', 'painterly',
        'vector-flat', 'unknown'
    )),
    linework_style                         TEXT NOT NULL CHECK (linework_style IN (
        'hard-1px-outline', 'soft-outline', 'variable-width', 'no-outline',
        'vector-clean', 'unknown'
    )),
    animation_frame_density                TEXT NOT NULL CHECK (animation_frame_density IN (
        'static', 'low', 'mid', 'high', 'cinematic', 'unknown'
    )),
    derived_register                       TEXT NOT NULL CHECK (derived_register IN (
        'retro-16bit', 'hand-drawn-pixel', 'clean-vector', 'painterly-raster',
        'anime-cel', 'manual-review'
    )),
    derived_register_source                TEXT NOT NULL DEFAULT 'rule'
        CHECK (derived_register_source IN (
            'rule', 'override', 'manual-review-resolved', 'gandalf-call'
        )),
    derived_register_override_rationale    TEXT,

    -- Embodiment tag (character/enemy assets only) — v1.0 starter set + structural placeholders
    -- New embodiments enter via embodiment-narrative-layer.md amendment, NOT by catalogue convenience.
    embodiment_tag                         TEXT CHECK (embodiment_tag IN (
        'humanoid', 'slime', 'beast', 'dragonling', 'swarm', 'construct', 'spirit', 'plant',
        'pending-amendment', 'not-applicable', 'unknown'
    )),
    pending_amendment_hint                 TEXT,

    -- Wiring viability (Legolas Mode B decomposition signal)
    decomposition                          TEXT NOT NULL CHECK (decomposition IN (
        'monolithic', 'decomposed', 'partial', 'not-applicable', 'unknown'
    )),

    -- Closed enum per drax wiring-track Flag 1 (2026-05-16); prevents curator divergence
    -- on format strings (e.g., 'spritesheet' vs 'png-spritesheet' vs 'sprite_sheet').
    file_format                            TEXT NOT NULL CHECK (file_format IN (
        'png', 'png-spritesheet', 'aseprite', 'svg', 'gif', 'jpg', 'mp4', 'webm',
        'json-atlas', 'tmx', 'wav', 'mp3', 'ogg', 'ttf', 'otf', 'other', 'unknown'
    )),

    -- License + cost
    license                                TEXT NOT NULL CHECK (license IN (
        'CC0', 'CC-BY', 'CC-BY-NC', 'CC-BY-SA', 'CC-BY-ND',
        'commercial-royalty-free', 'commercial-per-project', 'commercial-royalty-bearing',
        'commercial-license', 'unity-asset-store', 'proprietary', 'unknown'
    )),
    license_url                            TEXT,
    cost_usd                               REAL NOT NULL DEFAULT 0.0,
    cost_model                             TEXT NOT NULL DEFAULT 'free' CHECK (cost_model IN (
        'free', 'one-time', 'per-seat', 'per-project', 'royalty',
        'subscription', 'non-standard', 'unknown'
    )),

    -- Quality / curator review
    quality_flag                           TEXT NOT NULL DEFAULT 'unreviewed'
        CHECK (quality_flag IN (
            'unreviewed', 'pass', 'borderline', 'fail', 'deferred'
        )),
    quality_rationale                      TEXT,
    manual_review_queued                   INTEGER NOT NULL DEFAULT 0
        CHECK (manual_review_queued IN (0, 1)),

    -- Audit-trail
    curated_at                             TEXT NOT NULL,
    curated_by                             TEXT NOT NULL,
    superseded_at                          TEXT,
    superseded_by_uid                      INTEGER REFERENCES catalogue_assets(asset_uid),

    UNIQUE (source, source_asset_id, crawl_session_id)
) STRICT;

CREATE INDEX idx_catalogue_assets_source             ON catalogue_assets(source);
CREATE INDEX idx_catalogue_assets_category           ON catalogue_assets(category);
CREATE INDEX idx_catalogue_assets_derived_register   ON catalogue_assets(derived_register);
CREATE INDEX idx_catalogue_assets_embodiment_tag     ON catalogue_assets(embodiment_tag) WHERE embodiment_tag IS NOT NULL;
CREATE INDEX idx_catalogue_assets_pending_amendment  ON catalogue_assets(pending_amendment_hint) WHERE embodiment_tag = 'pending-amendment';
CREATE INDEX idx_catalogue_assets_decomposition      ON catalogue_assets(decomposition);
CREATE INDEX idx_catalogue_assets_license            ON catalogue_assets(license);
CREATE INDEX idx_catalogue_assets_current            ON catalogue_assets(superseded_at) WHERE superseded_at IS NULL;
CREATE INDEX idx_catalogue_assets_pack               ON catalogue_assets(pack_id) WHERE pack_id IS NOT NULL;

-- =============================================================================
-- asset_style_tags — secondary style tags (many-to-many)
-- =============================================================================

CREATE TABLE asset_style_tags (
    asset_uid       INTEGER NOT NULL REFERENCES catalogue_assets(asset_uid) ON DELETE CASCADE,
    tag             TEXT NOT NULL,
    confidence      REAL NOT NULL DEFAULT 1.0 CHECK (confidence BETWEEN 0.0 AND 1.0),
    source          TEXT NOT NULL CHECK (source IN (
        'vendor-metadata', 'legolas-inferred', 'elrond-curated'
    )),
    added_at        TEXT NOT NULL,
    PRIMARY KEY (asset_uid, tag)
) STRICT;

CREATE INDEX idx_asset_style_tags_tag ON asset_style_tags(tag);

-- =============================================================================
-- catalogue_rejections — viability-gate failure record
-- =============================================================================

CREATE TABLE catalogue_rejections (
    rejection_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    source              TEXT NOT NULL,
    pack_name           TEXT,
    rejection_date      TEXT NOT NULL,
    failure_track       TEXT NOT NULL CHECK (failure_track IN (
        'structural', 'wiring', 'design', 'multi-track'
    )),
    failure_rationale   TEXT NOT NULL,
    reviewer            TEXT NOT NULL,
    re_sampleable       INTEGER NOT NULL DEFAULT 0 CHECK (re_sampleable IN (0, 1)),
    notes               TEXT
) STRICT;

-- =============================================================================
-- abstraction_groupings + asset_grouping_membership — emergent-grouping analyses
-- =============================================================================

CREATE TABLE abstraction_groupings (
    grouping_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name                 TEXT NOT NULL,
    dimension            TEXT NOT NULL,
    created_by_analysis  TEXT NOT NULL,
    created_at           TEXT NOT NULL,
    member_count         INTEGER,
    description          TEXT
) STRICT;

CREATE TABLE asset_grouping_membership (
    asset_uid       INTEGER NOT NULL REFERENCES catalogue_assets(asset_uid) ON DELETE CASCADE,
    grouping_id     INTEGER NOT NULL REFERENCES abstraction_groupings(grouping_id) ON DELETE CASCADE,
    confidence      REAL NOT NULL DEFAULT 1.0 CHECK (confidence BETWEEN 0.0 AND 1.0),
    PRIMARY KEY (asset_uid, grouping_id)
) STRICT;
