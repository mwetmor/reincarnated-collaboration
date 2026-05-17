-- catalogue.db — v1.1 schema migration
-- Applied: 2026-05-16
-- Owner: elrond
-- Pattern P8 prevention (d) — per-vendor register-mixed convenience flag + per-product deliverable_register field
--
-- Context:
--   Per `canonical/story/drift-audit.md` Drift-13 + Pattern P8 prescription (d), the catalogue schema is
--   amended to expose register-mixedness at two layers:
--     1. Per-product (`catalogue_assets.deliverable_register`) — SOURCE-OF-TRUTH; populated per-product
--        by curators from per-product-page inspection. Optional/NULL allowed because not every vendor
--        requires the field (single-register vendors like pimen are unambiguous; `register_mixed=0`
--        at the vendor level signals deliverable_register may be omitted; cross-register vendors like
--        CraftPix require deliverable_register populated per row).
--     2. Per-vendor (`catalogue_sources.register_mixed`) — CONVENIENCE AGGREGATE; downstream consumers
--        can quickly answer "is this vendor cross-register?" without scanning all per-product rows.
--        Set to 1 when ANY of the vendor's products carry a different `deliverable_register` than
--        the vendor's `primary_register_hint`.
--
-- Both layers benefit:
--   - Per-product field catches at curation time (the locked rubric); aligns with legolas persona-rule
--     extension landed today (`legolas.md` line 34).
--   - Per-vendor flag catches at consumption time (downstream-consumption safety net per Drift-13
--     Cross-references: drax sources VFX + characters from same vendor; gandalf register-validation).
--
-- Cross-seam ADR compliance:
--   - ADR-002 (cross-seam schema = Matt approval): Matt authorized 2026-05-16 ("yes to all 7" — decisions #2 + #5).
--   - ADR-004 (MIGRATION.md for cross-seam handoff): companion entry in MIGRATION.md v1.4.
--   - ADR-006 (external system writes require authorization): schema mutation confined to elrond-owned catalogue.db.
--
-- Companion documents:
--   `agentic_orchestration/research/curated/catalogue-schema.md` (full schema doc; v1.1 amendment to follow)
--   `agentic_orchestration/research/curated/MIGRATION.md` (v1.4 entry)
--   `canonical/story/drift-audit.md` Drift-13 + Pattern P8 (the prescription driver)
--   `.claude/agents/legolas.md` (per-product `deliverable_register` field — persona-rule extension landed today)
--
-- Reversibility: schema additions are additive (new columns with NULL/DEFAULT). Existing v1.0 rows
-- remain valid (deliverable_register populated NULL by default; register_mixed populated 0 by default).
-- No back-fill of existing pimen rows required (pimen is single-register; register_mixed=0 holds).

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- =============================================================================
-- 1. catalogue_sources: per-vendor register_mixed convenience flag
-- =============================================================================
--
-- 0 = vendor's products are all in one register (the primary_register_hint).
-- 1 = vendor's products span >1 register (cross-register vendor; downstream consumers must
--     check per-product deliverable_register before aggregating).
--
-- Default 0 (single-register assumption). Curators flip to 1 when first cross-register product
-- is curated for the vendor.
--
-- Per ADR-002 STRICT-table-compatible ALTER: SQLite supports ADD COLUMN with DEFAULT on STRICT tables.

ALTER TABLE catalogue_sources
    ADD COLUMN register_mixed INTEGER NOT NULL DEFAULT 0
        CHECK (register_mixed IN (0, 1));

-- =============================================================================
-- 2. catalogue_assets: per-product deliverable_register source-of-truth field
-- =============================================================================
--
-- Value set parallels primary_register_hint enum on catalogue_sources, with the addition of
-- 'not-applicable' (for non-asset rows like UI / audio / font where register doesn't apply).
-- NULL allowed: optional field — populated when the vendor is register-mixed or when a curator
-- has explicitly inspected the per-product-page to determine deliverable_register.
--
-- Distinguished from `derived_register` (six-axis rubric output): deliverable_register is the
-- VENDOR'S SHIPPING REGISTER as advertised/delivered per product (`pixel-art-raster`, `vector-eps`,
-- `hand-drawn-pixel`, `vector-ai`, `3d-mesh`, etc.). derived_register is the CURATOR'S inferred
-- visual register from the six-axis rubric (output of the rule cascade). They overlap on the
-- happy path (vendor ships pixel-art-raster → curator's rubric yields hand-drawn-pixel or
-- retro-16bit) and DIVERGE when:
--   (a) vendor mislabels a product on their site (drift catch at curation)
--   (b) vendor ships a register that doesn't map to the curator's rubric (e.g., vector AI/EPS
--       — the rubric outputs 'clean-vector'; deliverable_register is 'vector-ai' or 'vector-eps')
--   (c) vendor ships mixed deliverables in one product (rare; surface as quality_flag=borderline)
--
-- The closed enum captures the observed vendor-shipping-register vocabulary. Add new values
-- via future migration as new shipping shapes surface (e.g., '3d-mesh', 'unity-prefab').

ALTER TABLE catalogue_assets
    ADD COLUMN deliverable_register TEXT
        CHECK (deliverable_register IN (
            'pixel-art-raster',      -- PNG/PSD pixel-art (CraftPix VFX, Pimen, most itch creators)
            'vector-ai',             -- Adobe Illustrator vector source (CraftPix character packs)
            'vector-eps',            -- EPS vector source (legacy vector vendors)
            'vector-svg',            -- SVG vector source
            'hand-drawn-pixel',      -- explicitly hand-painted pixel art (overlaps but distinct from generic 'pixel-art-raster' — vendor branding signal)
            'painterly-raster',      -- painted PSD / high-DPI raster (non-pixel)
            'photographic',          -- photo-derived assets (rare)
            'audio',                 -- audio shipping format (when audio assets are curated)
            'font',                  -- font shipping format (when font assets are curated)
            'mixed',                 -- product ships >1 register (rare; force borderline quality_flag)
            'not-applicable',        -- register doesn't apply (e.g., utility scripts)
            'unknown'                -- not determinable; queued for inspection
        ));

-- Partial index for cross-register-query (locked-register filtering with deliverable signal).
CREATE INDEX idx_catalogue_assets_deliverable_register
    ON catalogue_assets(deliverable_register)
    WHERE deliverable_register IS NOT NULL;

-- =============================================================================
-- 3. Canonical first instance — CraftPix vendor row (register_mixed=1)
-- =============================================================================
--
-- Per dispatch instruction: CraftPix is the canonical first cross-register vendor.
-- Inserted with register_mixed=1 reflecting empirical evidence from
-- `agentic_orchestration/research/catalogue/craftpix/full-2026-05-16.jsonl`
-- (5 pixel-art records + 2 vector records).
--
-- vendor_type='aggregator-marketplace': CraftPix.net is a multi-creator pack aggregator, not a
-- single-creator studio. (Pimen, by contrast, is `individual-creator`.)
-- primary_register_hint='mixed': vendor doesn't have a single primary register; per-product deliverable
-- is the only authoritative read. (Some downstream consumers may prefer 'pixel-art' since 5/7 of
-- existing inventory is pixel-art-raster; the 'mixed' value forces them to check deliverable_register.)
-- default_license='mixed': CraftPix license terms vary per pack (royalty-free is most common but
-- premium membership has different terms); force the read.
-- register_mixed=1: explicit per-product inspection required at consumption.

INSERT INTO catalogue_sources (
    source, display_name, url, vendor_type, primary_register_hint,
    default_license, notes, added_at, register_mixed
) VALUES (
    'craftpix',
    'CraftPix.net',
    'https://craftpix.net/',
    'aggregator-marketplace',
    'mixed',
    'mixed',
    'Cross-register vendor (Drift-13 / Pattern P8 canonical first instance). '
        || 'VFX product line ships pixel-art-raster (PNG/PSD, 64-256px frames); '
        || 'character sprite product line ships vector (AI/EPS, layered for vector editor). '
        || 'Both lines carry CraftPix''s site-wide "pixel art" marketing label. '
        || 'Curators MUST populate deliverable_register per product (do not aggregate by vendor). '
        || 'License terms vary per product (royalty-free is most common; premium membership has different terms). '
        || 'AI training of CraftPix assets is prohibited per license terms (relevant for any LLM-pipeline integration).',
    '2026-05-16T00:00:00Z',
    1
);

-- =============================================================================
-- 4. schema_meta — record v1.1 application
-- =============================================================================

INSERT INTO schema_meta (version, applied_at, description, migration_script) VALUES (
    '1.1',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'Per-vendor register_mixed convenience flag + per-product deliverable_register field; CraftPix canonical first cross-register vendor. Drift-13 / Pattern P8 prevention (d). Matt-authorized 2026-05-16.',
    'catalogue_migrations/v1_1_register_mixed_flag.sql'
);

COMMIT;

-- =============================================================================
-- Verification queries (run interactively post-migration; not part of the migration transaction)
-- =============================================================================
--
-- Schema confirmation:
--   sqlite3 catalogue.db ".schema catalogue_sources"  -- shows register_mixed column
--   sqlite3 catalogue.db ".schema catalogue_assets"   -- shows deliverable_register column
--
-- CraftPix row:
--   sqlite3 catalogue.db "SELECT source, vendor_type, primary_register_hint, register_mixed FROM catalogue_sources WHERE source='craftpix';"
--   Expected: craftpix|aggregator-marketplace|mixed|1
--
-- Cross-register query pattern (downstream consumer convenience):
--   SELECT a.source, a.name, a.deliverable_register
--   FROM catalogue_assets a
--   JOIN catalogue_sources s ON s.source = a.source
--   WHERE s.register_mixed = 1 AND a.superseded_at IS NULL;
--
-- Per-product enforcement (curator-side reminder):
--   SELECT a.source, a.name
--   FROM catalogue_assets a
--   JOIN catalogue_sources s ON s.source = a.source
--   WHERE s.register_mixed = 1 AND a.deliverable_register IS NULL AND a.superseded_at IS NULL;
--   (Should be empty post-curation for register-mixed vendors; surfaces unbackfilled cross-register rows.)
