-- catalogue.db — v1.2 data migration (no schema change)
-- Applied: 2026-05-16
-- Owner: elrond
-- Pixogen vendor row insert — HOLD-to-APPROVED state transition
--
-- Context:
--   Per Pattern A dispatch 2026-05-16 (close Pixogen catalogue loop), Pixogen vendor
--   record is being inserted into catalogue.db following:
--     1. Matt downloaded Pixogen Lite (free; AFGameAssets / Antoine Fauville license)
--     2. License file verified clean (commercial use OK; modification OK; Pixi.js
--        runtime tinting permitted per § 2.A.4; attribution required per § 3.A.1)
--     3. Drax v0.19 wired Void Shield into demo + added attribution credit
--   License is VERIFIED CLEAN; consumption is APPROVED-WITH-ATTRIBUTION.
--
--   Prior state: Pixogen had ZERO presence in catalogue.db. legolas Mode B raw
--   extraction at `agentic_orchestration/research/catalogue/pixogen/full-2026-05-16.jsonl`
--   carried `license_unverified: true` + `consumption_hold: HOLD`. Per Pixogen
--   exclusion adjudication 2026-05-16 (pivot-insurance-ledger.md line 136 + cross-
--   vendor substrate inventory), Pixogen rows were excluded from cipher-width
--   analysis pending license verification.
--
--   This migration creates the vendor attestation row reflecting the cleared HOLD.
--   No catalogue_packs or catalogue_assets rows are added (NO Pixogen pack curation
--   per dispatch scope — Full pack not acquired; Lite curation is a separate
--   follow-on dispatch).
--
-- Cross-seam ADR compliance:
--   - ADR-002 (cross-seam schema = Matt approval): no schema change in this migration
--     (pure data insert into elrond-owned catalogue.db). Dispatch acceptance by Matt
--     via knight-rider Pattern A routing.
--   - ADR-004 (MIGRATION.md for cross-seam handoff): companion entry MIGRATION.md v1.5.
--   - ADR-006 (external system writes require authorization): write confined to
--     elrond-owned catalogue.db; license verification + consumption approval are
--     upstream Matt+drax events.
--
-- Companion documents:
--   `agentic_orchestration/research/curated/MIGRATION.md` (v1.5 entry)
--   `agentic_orchestration/research/catalogue/pixogen/findings-summary-2026-05-16.md`
--     (legolas's vendor findings-summary; license-unverified state captured pre-clearance)
--   `agentic_orchestration/research/catalogue/pixogen/full-2026-05-16.jsonl`
--     (legolas's raw extraction; still carries the original HOLD flags — that's a raw
--     extraction artifact, untouched per ownership-boundary discipline)
--   `agentic_orchestration/research/curated/pixogen-catalogue-curated-2026-05-16.jsonl`
--     (THIS dispatch's curated parallel; carries flag-flipped state)
--
-- Reversibility: pure INSERT into catalogue_sources. Reversible via
--   `DELETE FROM catalogue_sources WHERE source='itch-pixogen';`
-- (no downstream catalogue_packs / catalogue_assets rows exist yet, so the delete
-- is safe; FK constraints would block deletion if/when downstream rows land.)

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- =============================================================================
-- 1. catalogue_sources: insert Pixogen vendor row
-- =============================================================================
--
-- source = 'itch-pixogen': namespace-prefixed key matches the convention established by
--   itch-pimen (vendor + platform), distinguishing from any future non-itch Pixogen
--   storefront (none currently known).
-- display_name = 'Pixogen (itch.io / AFGameAssets)': brand + legal entity (Antoine
--   Fauville trading as AFGameAssets; Pixogen is the itch.io store handle).
-- url = 'https://pixogenassets.itch.io/': vendor itch.io page (root for both Full and Lite SKUs).
-- vendor_type = 'individual-creator': single-creator (Antoine Fauville), not a multi-
--   creator aggregator. Matches itch-pimen pattern.
-- primary_register_hint = 'hand-drawn-pixel': vendor's branded register from the
--   legolas extraction ("Pixel Art RPG VFX"; 64x64 uniform canvas with hand-pixeled
--   frames). Aligns with derived_register classification expected at pack curation.
-- default_license = 'commercial-royalty-free': license file (downloaded + verified by
--   Matt 2026-05-16) permits commercial use, modification, Pixi.js runtime tinting
--   (§ 2.A.4), requires attribution (§ 3.A.1). Maps cleanly to the
--   commercial-royalty-free enum; attribution requirement carried in the notes field
--   and at per-asset level via license_url + per-asset metadata.
-- register_mixed = 0: vendor ships exclusively pixel-art-raster (PNG spritesheets,
--   Unity Package). No vector/painterly/3d shipping in current inventory. Future
--   cross-register surfacing would flip to 1.
-- notes = comprehensive state capture: license verification path + AFGameAssets
--   reference + Pixi.js tinting clause + attribution requirement + pricing reality
--   (Full €19.99 paid not-yet-acquired; Lite €0 acquired) + Drax v0.19 demo wiring
--   attestation.

INSERT INTO catalogue_sources (
    source,
    display_name,
    url,
    vendor_type,
    primary_register_hint,
    default_license,
    notes,
    added_at,
    register_mixed
) VALUES (
    'itch-pixogen',
    'Pixogen (itch.io / AFGameAssets)',
    'https://pixogenassets.itch.io/',
    'individual-creator',
    'hand-drawn-pixel',
    'commercial-royalty-free',
    'Single-creator vendor (Antoine Fauville trading as AFGameAssets). Itch.io storefront '
        || 'ships Pixel Art RPG VFX in two SKUs: Full (€19.99, 108 animations / 11 categories, '
        || '636 sprites at 64x64px) and Lite (free, 8 animations / 8 categories, 48 sprites). '
        || 'Also packaged inside Pixel Art RPG Mega Pack (€59.99). '
        || 'LICENSE: AFGameAssets license file (18kB, distributed with each pack). '
        || 'Verified clean 2026-05-16 by Matt via Lite-pack download. Terms permit: '
        || 'commercial use, modification, Pixi.js runtime tinting (§ 2.A.4). '
        || 'REQUIRES ATTRIBUTION (§ 3.A.1) — downstream consumers must include credit. '
        || 'Drax v0.19 wired Void Shield into demo with attribution credit (canonical first '
        || 'consumption instance). '
        || 'PRICING (corrected 2026-05-16): Full €19.99 is the only purchasable SKU (Mega Pack '
        || 'is the other paid route); Lite is a SEPARATE free download (not a free version of '
        || 'Full — distinct pack with reduced category set). Lite acquired by project 2026-05-16; '
        || 'Full not yet acquired. Curated catalogue rows for Lite tracked separately via '
        || 'curated jsonl + future pack-curation dispatch. '
        || 'CONSUMPTION STATE: APPROVED-WITH-ATTRIBUTION (transitioned from HOLD 2026-05-16). '
        || 'License verification date: 2026-05-16. '
        || 'No generative AI used in asset creation (vendor-attested). '
        || 'Contact: afgameassets@gmail.com. '
        || 'Substrate-novelty per Tier-1 sweep: ships Void (spatial-absence; canonical first '
        || 'instance) and Technology (sci-fi VFX; fully novel — single-vendor Tier-1 substrate).',
    '2026-05-16T22:10:00Z',
    0
);

-- =============================================================================
-- 2. schema_meta — record v1.2 data-migration application
-- =============================================================================
--
-- v1.2 is a DATA migration, not a SCHEMA migration. Recording in schema_meta keeps
-- the migration audit trail single-threaded (per audit § 7 recommendation that all
-- catalogue.db mutations route through a numbered migration script for replay
-- safety). Description discriminates data vs schema for downstream readers.

INSERT INTO schema_meta (version, applied_at, description, migration_script) VALUES (
    '1.2',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'DATA MIGRATION (no schema change): Pixogen vendor row insert. HOLD-to-APPROVED-WITH-ATTRIBUTION transition following Matt license verification + Drax v0.19 demo consumption 2026-05-16. AFGameAssets license clean for commercial use + modification + Pixi.js tinting; attribution required.',
    'catalogue_migrations/v1_2_pixogen_vendor_insert.sql'
);

COMMIT;

-- =============================================================================
-- Verification queries (run interactively post-migration)
-- =============================================================================
--
-- Vendor row inserted:
--   sqlite3 catalogue.db "SELECT source, display_name, vendor_type, primary_register_hint, default_license, register_mixed FROM catalogue_sources WHERE source='itch-pixogen';"
--   Expected: itch-pixogen|Pixogen (itch.io / AFGameAssets)|individual-creator|hand-drawn-pixel|commercial-royalty-free|0
--
-- Schema-meta row recorded:
--   sqlite3 catalogue.db "SELECT version, description FROM schema_meta WHERE version='1.2';"
--   Expected: 1.2|DATA MIGRATION (no schema change)...
--
-- Vendor count check:
--   sqlite3 catalogue.db "SELECT COUNT(*) FROM catalogue_sources;"
--   Expected: 3 (itch-pimen + craftpix + itch-pixogen)
--
-- Downstream rows confirmation (none yet — by design):
--   sqlite3 catalogue.db "SELECT COUNT(*) FROM catalogue_packs WHERE source='itch-pixogen';"
--   Expected: 0
--   sqlite3 catalogue.db "SELECT COUNT(*) FROM catalogue_assets WHERE source='itch-pixogen';"
--   Expected: 0
