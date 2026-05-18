# Catalogue DB — Additive Schema Extension v1.6 (Tier 5.2 rubber-stamp)

**Author:** elrond
**Date:** 2026-05-18
**Authority:** Matt L3 lock 2026-05-18 Tier 5.2 — "approve catalogue-DB additive schema"
**Dispatch:** `agentic_orchestration/dispatches/2026-05-18-elrond-tier-5-1-5-2-final-curation.md`
**Tag:** `elrond/v1.11-tier-5-1-5-2-final-curation-1`
**Predecessor schema state:** v1.1 (column schema; data migration v1.5 = Pixogen vendor)
**Migration kind:** ADDITIVE only — no breaking changes; no back-fill required; new columns NULL-allowed.
**Migration script (proposed; not yet executed):** `agentic_orchestration/research/scripts/catalogue_migrations/v1_6_usage_recommendation_license_class.sql`

---

## § 1 — Why this migration

Two empirical observations from the past three days of curation work motivate this:

1. **The dungeon-objects audit lesson** (`dungeon-objects-quality-audit-2026-05-18.md` § 6.1 — "curation lesson"). Drax's v1.13 tile slicer treated `walls_floor.png` as an auto-tile floor pool when in fact it is a composite reference atlas. The shred-defect produced Matt's "stairs sprite is bad" verdict. Root cause: **the catalogue had no per-file usage-recommendation field** to distinguish floor-tile-pool sheets from prop-pool sheets from composite-reference atlases. A consumer (drax) had to infer intent from filename + visual inspection. The cost of that inference falling short was the entire VS2a drax v1.17 swap dispatch.

2. **License-class coverage drift.** Three new attribution-class vocabulary terms have entered the operational corpus in the past 72 hours without being captured in the closed `license` enum on `catalogue_assets`:
   - `SIL-1.1` (Game-icons.net — Tier 5.1 lock 2026-05-18)
   - `CraftPix-Free-Terms` (CraftPix free assets one-credit-line convention; current `license_specifics` workaround)
   - `Seliel-personal` / `Seliel-Mana-Seed` (Mana Seed license variant; currently coerced to `commercial-royalty-free` with notes-field hint)
   - `OGA-permissive` (OGA umbrella — already partially captured as `CC0` / `CC-BY` but the OGA-vendor-level convention warrants explicit attribution)

The current schema reaches the same operational outcomes via `notes` + `license_specifics` text fields, but those are free-text — consumers can't filter on them at the SQL layer. A new `license_class` enum surfaces this at queryable granularity without disturbing the existing `license` column's role as the legal-classification axis.

---

## § 2 — Migration scope (additive only)

### § 2.1 — New column on `catalogue_assets`

```sql
ALTER TABLE catalogue_assets
  ADD COLUMN usage_recommendation TEXT NULL
  CHECK (usage_recommendation IS NULL OR usage_recommendation IN (
    'floor_tile_pool',                  -- clean repeating-grid tile sheet; drax tile slicer consumes directly
    'ambient_prop_pool',                -- cut-out individual prop assets; drax static-prop placer consumes
    'animated_prop_pool',               -- frame-strip animation sheets; drax DUNGEON_LOOP_DESCS consumes
    'composite_reference_DO_NOT_TILE',  -- architecture-atlas reference sheet; consumer MUST NOT auto-tile
    'character_spritesheet',            -- per-state character animation sheets (chierit etc.)
    'ui_icon_pool',                     -- UI icon library (gear/potion/status/HUD widgets)
    'ui_frame_pool',                    -- UI frame/window/slot infrastructure
    'vfx_overlay_pool',                 -- VFX overlay frame-strips (cast/projectile/impact)
    'audio_layer_pool',                 -- audio asset (referenced from data layer but typed for completeness)
    'reference_only',                   -- not for consumption; reference texture (palette swatches, preview composites)
    'unknown'                           -- curator hasn't determined yet
  ));
```

**Default at insert time:** NULL. Existing 48 rows are not back-filled in this migration; they remain NULL until next curation pass touches each row (deferred per `curation-pipeline.md` standing pattern).

### § 2.2 — New column on `catalogue_assets`

```sql
ALTER TABLE catalogue_assets
  ADD COLUMN license_class TEXT NULL
  CHECK (license_class IS NULL OR license_class IN (
    'CC0',                              -- public domain
    'CC-BY-4.0', 'CC-BY-3.0',           -- creative commons attribution
    'CC-BY-NC-4.0', 'CC-BY-NC-3.0',     -- CC with non-commercial restriction (red flag)
    'CC-BY-SA-4.0', 'CC-BY-SA-3.0',     -- CC with share-alike (Drax filter concern)
    'CC-BY-ND-4.0',                     -- CC with no-derivatives (modification restriction)
    'SIL-1.1',                          -- Game-icons.net pattern; copyleft-lite for icon fonts
    'OFL-1.1',                          -- Open Font License (anticipated future use)
    'CraftPix-Free-Terms',              -- CraftPix free-asset one-credit-line convention
    'CraftPix-Premium-Membership',      -- CraftPix paid pack license
    'AFGameAssets',                     -- Pixogen / Antoine Fauville custom license (per § 3.A.1 attribution)
    'Mana-Seed-Personal-Use',           -- Seliel Mana Seed personal-use tier
    'Mana-Seed-Commercial',             -- Seliel Mana Seed commercial tier
    'OGA-Permissive',                   -- OpenGameArt permissive umbrella (CC0/CC-BY/GPL-compat) — vendor-class
    'Itch-Standard-No-Redistribution',  -- common itch.io pattern: commercial OK, no redistribution
    'Itch-PWYW-Custom',                 -- pay-what-you-want with custom terms
    'Proprietary-Suno-Pro',             -- Suno Pro music license (currently PARKED — Q-MATT-2)
    'Royalty-Free-Single-User',         -- PixelLoops-style single-user perpetual
    'Chierit-CC-BY-4.0',                -- chierit umbrella (subset of CC-BY-4.0 with vendor attribution)
    'unknown',                          -- license not determined
    'pending-verification'              -- license under verification (legolas HOLD state)
  ));
```

**Rationale:** `license_class` is a finer-grained classification than `license`. The existing `license` column captures broad categories (CC0 / CC-BY / commercial-royalty-free / etc.) suitable for legal-tier filtering. `license_class` captures the **specific license instance** suitable for credits.txt attribution generation + per-license-class consumption rules (e.g., "no auto-redistribute on Itch-Standard-No-Redistribution" or "no derivative works on CC-BY-ND-4.0").

The two columns are correlated but not redundant — `license = 'CC-BY'` rows split across `license_class IN ('CC-BY-4.0', 'CC-BY-3.0', 'Chierit-CC-BY-4.0')`, each with different attribution-string conventions.

### § 2.3 — New indexes

```sql
CREATE INDEX IF NOT EXISTS idx_catalogue_assets_usage_recommendation
  ON catalogue_assets(usage_recommendation)
  WHERE usage_recommendation IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_catalogue_assets_license_class
  ON catalogue_assets(license_class)
  WHERE license_class IS NOT NULL;
```

Partial indexes (WHERE NOT NULL) — same pattern as `idx_catalogue_assets_deliverable_register` (v1.1). Existing rows with NULL values do not bloat the index; consumers querying NOT-NULL get sub-linear lookup.

### § 2.4 — schema_meta v1.6 row

```sql
INSERT INTO schema_meta (version, applied_at, description, migration_script) VALUES
  ('1.6', '2026-05-18T<applied_at>Z',
   'Additive: usage_recommendation enum (per-file consumption hint) + license_class enum (per-asset specific license); Tier 5.2 Matt L3 2026-05-18',
   'catalogue_migrations/v1_6_usage_recommendation_license_class.sql');
```

---

## § 3 — What this enables (downstream consumer benefit)

### § 3.1 — Drax: structural-defect prevention

Before this migration, drax's tile-slicer + prop-placer code had no way to disambiguate at the catalogue layer:
- "Is this PNG a tile pool I can auto-tile?"
- "Is this PNG a prop pool I should slice into discrete cells?"
- "Is this PNG an architecture-atlas reference I must NOT auto-tile?"

After this migration:

```sql
-- Query: get auto-tileable floor sheets for a given pack
SELECT asset_path, sw, sh
FROM catalogue_assets
WHERE pack_id = ?
  AND usage_recommendation = 'floor_tile_pool';

-- Query: get prop placements
SELECT asset_path, prop_metadata
FROM catalogue_assets
WHERE pack_id = ?
  AND usage_recommendation IN ('ambient_prop_pool', 'animated_prop_pool');

-- Safety check: REJECT this asset for auto-tile rendering
SELECT 1 FROM catalogue_assets
WHERE asset_uid = ?
  AND usage_recommendation = 'composite_reference_DO_NOT_TILE';
```

The dungeon-objects audit defect (drax shredding `walls_floor.png` as floor pool) becomes an SQL-preventable error class. The defect is no longer "drax inferred wrong" — it becomes "elrond didn't tag the row" with explicit catalogue-side ownership.

### § 3.2 — Drax: credits.txt automation path

Before: per-pack attribution strings were hand-crafted in `credits.txt` from notes-field hints + vendor URL pattern matching.

After:

```sql
-- Generate attribution-required asset list grouped by license_class
SELECT
  license_class,
  pack_id,
  pack_origin,
  count(*) AS asset_count,
  vendor_url
FROM catalogue_assets
JOIN catalogue_packs USING (pack_id)
WHERE license_class IS NOT NULL
  AND license_class IN ('CC-BY-4.0', 'CC-BY-3.0', 'SIL-1.1',
                        'CraftPix-Free-Terms', 'CraftPix-Premium-Membership',
                        'Mana-Seed-Personal-Use', 'Mana-Seed-Commercial',
                        'AFGameAssets', 'Chierit-CC-BY-4.0', 'OGA-Permissive',
                        'Itch-Standard-No-Redistribution', 'Royalty-Free-Single-User')
GROUP BY license_class, pack_id
ORDER BY license_class, pack_id;
```

This produces the data shape needed for `credits.txt` generation. Drax (or a future curation script) can render the attribution surface programmatically rather than hand-curate.

### § 3.3 — Gandalf / abstraction-analysis: per-class license-risk surfaces

Queries become expressible:

```sql
-- Distribution of share-alike (SA) license exposure across substrates
SELECT
  substrate_tag,
  count(*) AS asset_count
FROM catalogue_assets ca
JOIN asset_style_tags t USING (asset_uid)
WHERE ca.license_class LIKE '%-SA-%'
  AND t.tag LIKE 'substrate:%'
GROUP BY substrate_tag
ORDER BY asset_count DESC;
```

Surfaces "if we ship with these substrates and trigger CC-SA derivative obligations, which substrates are most exposed?" — useful for pre-ship license audit.

---

## § 4 — What is NOT in this migration

- **No data back-fill.** Existing 48 catalogue_assets rows are not touched. Their `usage_recommendation` and `license_class` columns are NULL until a future curation pass populates them.
- **No drax-side consumption.** This migration ships the schema; consumption is downstream drax v1.21+ work (or a future curation-pipeline pass).
- **No deletion of any existing column.** `license`, `notes`, `license_specifics`, `deliverable_register` all retain their roles. The new columns are additive context.
- **No engine-side change.** ADR-004 unaffected — engine telemetry schema untouched. Catalogue DB is elrond-owned.
- **No game-icons.net icon-asset rows.** Those land as a future curation pass (game-icons.net is on-demand-download; per-icon catalogue rows are commission-able if the corpus grows large enough to warrant per-icon tracking — likely not until 100+ icons in use).

---

## § 5 — Reversibility

```sql
-- Reverse this migration:
DROP INDEX IF EXISTS idx_catalogue_assets_usage_recommendation;
DROP INDEX IF EXISTS idx_catalogue_assets_license_class;
ALTER TABLE catalogue_assets DROP COLUMN usage_recommendation;
ALTER TABLE catalogue_assets DROP COLUMN license_class;
DELETE FROM schema_meta WHERE version='1.6';
```

SQLite 3.35+ supports `ALTER TABLE ... DROP COLUMN`. Pre-3.35 fallback: rebuild table from CREATE-INSERT-DROP-RENAME pattern.

Pre-migration backup recommended (parallel to v1.4 backup): `cp catalogue.db catalogue.db.pre-v1.6-backup` before applying. Retain 1-week soft.

---

## § 6 — Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** Matt L3 2026-05-18 explicitly approved "catalogue-DB additive schema." Authorization scope clear; this migration falls within it.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** entry forthcoming under `MIGRATION.md` v1.6. Engine-telemetry schema untouched; no star-lord-side MIGRATION required.
- **ADR-006 (external-system writes require authorization):** writes confined to elrond-owned paths. Pre-migration backup is additional safety (not required by ADR but elected for schema migrations per v1.1 precedent).
- **ADR-007 (survey-mode):** this doc reports what the migration is (§§ 1-5); recommendation language confined to "what this enables" (§ 3), not prescriptive of consumer behavior.

---

## § 7 — Execution plan (when elrond v1.12 fires)

1. Backup: `cp catalogue.db catalogue.db.pre-v1.6-backup`
2. Apply: `sqlite3 catalogue.db < research/scripts/catalogue_migrations/v1_6_usage_recommendation_license_class.sql`
3. Verify: `SELECT version FROM schema_meta ORDER BY applied_at;` returns rows for 1.0, 1.1, 1.2, 1.6
4. Verify CHECK enforcement: `INSERT ... usage_recommendation='BOGUS'` rejected; `INSERT ... license_class='BOGUS'` rejected.
5. Append MIGRATION.md v1.6 entry per the v1.4 / v1.5 template.

**This dispatch (v1.11) ships the spec only.** Execution of the migration script + actual DB mutation is a follow-on dispatch when knight-rider sequences it (likely paired with the next curation pass that wants to populate the new columns).

---

## § 8 — Author / verification

- **Author:** elrond, 2026-05-18.
- **Cross-checked against:** dungeon-objects audit § 6 (curation lesson), v1.1 schema column-add pattern (v1_1_register_mixed_flag.sql), v1.5 data-migration pattern (v1_2_pixogen_vendor_insert.sql).
- **Spec status:** locked v1.6 design, **pending Matt approval at execution time** (separate from the Tier 5.2 spec-authoring approval Matt already gave).
- **Companion JSON Lines manifest extension (this same dispatch):** `ambient-props-subset-vs2a-2026-05-17.jsonl` extension with 8-12 new prop rows + `usage_recommendation` field demonstrating the convention in flight.
- **Companion handoff brief:** `tier-5-1-5-2-drax-v1.21-handoff-brief-2026-05-18.md` (consolidates icons + props + credits + schema).
