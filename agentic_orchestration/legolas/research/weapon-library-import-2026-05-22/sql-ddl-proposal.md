# SQL DDL Proposal — Weapon Library DB Schema
# Priority 3

**Date:** 2026-05-22
**Mode:** A (analytical design)
**Commissioner:** gandalf, authorized by Matt 2026-05-22 evening
**Target DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (SQLite; confirmed 0 bytes / greenfield)
**DDL file:** `schema.sql` (this directory — ready to run once approved)
**Depends on:** `metadata-normalization.md` (canonical tag schema), `library-enumeration.md` (library inventory)

---

## Summary

The proposed schema is 9-table SQLite design built around a central `weapons` entity, with
specialized satellite tables for sim-properties, aesthetic metadata, source provenance, and
import-pipeline state. The design makes two key trade-offs: (1) the most performance-critical
query predicates (gear_catalogue_id, range_class, tech_level, cultural_lineage, readiness_state)
are direct columns on the `weapons` table rather than normalized to tag relationships — this
enables fast compound index scans without joins for the selection hotpath; (2) a controlled
vocabulary (`tag_taxonomy`) provides extensible many-to-many tagging for secondary attributes
without polluting the structural columns. A `substrate_density` table supports density-routing
decisions (empty → Meshy gap-fill; sparse → priority Meshy; adequate/dense → DB selection)
without requiring aggregate queries at generation time.

---

## 1. Entity-Relationship Diagram

```
libraries (library registry)
    |
    +--< weapon_sources >--+ weapons (core entity)
                           |   |
                    licenses   |---< weapon_tags >--- tag_taxonomy
                               |
                               +--- weapon_sim_props (1:1 optional)
                               |
                               +--- weapon_aesthetic (1:1 optional)
                               |
                               +--- weapon_readiness (1:1 optional)

substrate_density (aggregate density map; references gear_catalogue_id enum)
```

**Cardinalities:**
- `libraries` 1 --- M `weapon_sources`
- `licenses` 1 --- M `weapon_sources`
- `weapons` 1 --- M `weapon_sources` (one weapon can exist in multiple libraries)
- `weapons` 1 --- M `weapon_tags`
- `tag_taxonomy` 1 --- M `weapon_tags`
- `weapons` 1 --- 0..1 `weapon_sim_props` (populated after sim-verification)
- `weapons` 1 --- 0..1 `weapon_aesthetic` (populated during import)
- `weapons` 1 --- 0..1 `weapon_readiness` (tracks pipeline state)

---

## 2. Table-by-Table Justification

### 2.1 `weapons` — Core entity

The central table intentionally denormalizes several fields that would otherwise belong in
satellite tables. Specifically: `range_class`, `geometry_class`, `tempo_class`, `tech_level`,
`cultural_lineage`, `tone`, `style_register`, `gear_catalogue_id`, and `readiness_state` are all
direct columns on `weapons` rather than tag relationships.

**Justification:** These are the PRIMARY QUERY PREDICATES for weapon selection at generation time
(selection pattern P1-P5). Putting them as direct columns allows compound indexes and avoids
joins on the selection hotpath. With 10–100K weapons at peak import scale, a join-free query
on a compound index is 10–50x faster than an equivalent JOIN through weapon_tags.

**Trade-off acknowledged:** This creates some denormalization. If the controlled vocabulary
for any of these enums needs to change, an ALTER TABLE + data migration is required. The
`tag_taxonomy` table provides the semantic vocabulary definition; the `weapons` table stores
the assigned values as TEXT with CHECK constraints. The tag_taxonomy seed data defines the
valid values; the CHECK constraints enforce them.

**gear_catalogue_id field:** This is the load-bearing link to the 15-gear catalogue. Values
1–15 map directly to the gear rule-table entries. NULL means "pending review" or "no clear
match." This integer is indexed directly on `weapons` for fast filtering.

**dominant_element_affinities field:** Stored as a comma-separated string (e.g., "fire,water")
rather than a normalized table. Justification: (1) this is a derived field computed from the
BDI ω-table and element pairings, not a source field; (2) it is read-only at query time (no
update joins needed); (3) JSON_EACH() or simple LIKE queries on a small set suffice for
7-element space; full normalization would add a join with negligible selectivity benefit.

---

### 2.2 `weapon_sources` — Source provenance

One weapon can exist in multiple libraries (e.g., a weapon uploaded to both Sketchfab and
Meshy). The `is_primary` flag designates which source is the authoritative download path.
This table handles all license-compliance data (attribution, license URL, attribution text).

**UNIQUE constraint on (library_id, source_asset_id):** Prevents duplicate imports from the
same library. If a crawl re-encounters an already-imported model, the existing row is
updated (not duplicated) via INSERT OR REPLACE logic in the import pipeline.

**license_id FK:** References the `licenses` table's `game_approved` flag. The import pipeline
should set `readiness_state = 'rejected'` on weapons where the primary source has
`game_approved = 0`. The `v_weapons_ready` view enforces this automatically.

---

### 2.3 `weapon_tags` — Many-to-many secondary tags

For metadata attributes that are: (1) secondary to the main selection query predicates, or
(2) multi-valued per weapon (e.g., a weapon tagged with both "dragon-slayer" and "holy"), or
(3) lower-confidence inferences (confidence < 1.0 column).

**confidence column:** Distinguishes explicit tags (1.0, from source metadata) from inferred
tags (0.5–0.9, from NLP/keyword analysis) from defaults (0.1–0.3, from pack-level inference).
The selection patterns can optionally filter by confidence threshold.

---

### 2.4 `weapon_sim_props` — Detailed simulation properties

Optional 1:1 satellite for quantified sim properties. Separated from `weapons` for two reasons:
(1) these fields are populated AFTER import by the sim-verification pass (rocket territory),
not at crawl time; (2) queries that don't need sim-property details avoid loading these columns.

**sim_viable field:** This is the rocket verification gate. A weapon with `sim_viable = 0`
should not be served as a canonical selection output until verified. The `v_weapons_ready`
view does not filter on this — that filtering is left to the selection patterns which can
optionally add `AND sim_viable = 1` for strict mode.

---

### 2.5 `weapon_aesthetic` — Detailed aesthetic metadata

Optional 1:1 satellite for aesthetic fields beyond the main `weapons` table columns. Contains
confidence scores per aesthetic field, secondary cultural lineages for cross-cultural weapons,
source attribution (Smithsonian structured field vs. tag inference), and raw source data
preserved for re-normalization.

**culture_source_field and era_source_field:** Track provenance of the aesthetic inference.
"smithsonian_culture_field" means the value came from a structured museum metadata field
(high confidence). "tag_inference" means it was inferred from free-text tags (medium
confidence). This traceability is valuable if aesthetic normalization rules change.

---

### 2.6 `weapon_readiness` — Import pipeline state machine

Tracks each weapon through the import pipeline. State machine:

```
needs_format_conversion
    → (format conversion complete) → needs_scale_normalization
    → (scale verified) → needs_texture_bake (if textures present)
    → (textures OK or absent) → sim_viability_unverified
    → (rocket passes) → ready_to_import
    → (readiness confirmed) stays ready_to_import

Alternates:
    Any state → rejected (license rejected or quality gate failure)
    Any state → needs_meshy_regenerate (model failed quality gate; Meshy generates replacement)
```

**import_batch field:** Tracks which import batch (e.g., "phase-a-kenney-2026-05-25") a weapon
was imported in. Useful for batch-level rollback if an import has errors, and for audit logs.

---

### 2.7 `substrate_density` — Precomputed density map

This table powers the density-routing decision at generation time without requiring an
aggregate COUNT query over the full weapons table on every class generation.

**Population strategy:** After each import batch, a maintenance job runs:
```sql
INSERT OR REPLACE INTO substrate_density
    (dominant_element, range_class, gear_catalogue_id,
     weapon_count_total, weapon_count_ready, weapon_count_cc0, weapon_count_cc_ok,
     density_tier, last_computed)
SELECT
    -- dominant_element derived from affinities; see selection-patterns.md for approach
    -- ... aggregate query ...
```

**density_tier mapping:**
- `empty` (0 ready weapons) → route to Meshy gap-fill
- `sparse` (1–2 ready weapons) → serve available + queue Meshy gap-fill for this vector
- `adequate` (3–10 ready weapons) → serve from DB selection
- `dense` (>10 ready weapons) → serve from ranked DB selection

---

### 2.8 `tag_taxonomy` — Controlled vocabulary

Central vocabulary registry. Seeded in schema.sql with all canonical values for all
namespaces. New namespaces can be added without schema changes. Wikidata QIDs are stored
as optional reference for ontology-linked queries.

**Parent_tag_id for hierarchy:** Supports tree-structured tags (e.g., "katana" is-a "sword"
is-a "edged weapon"). In practice, the hierarchy depth for the weapon DB is shallow (2–3
levels maximum), so recursive CTE queries are feasible in SQLite.

---

### 2.9 `libraries` and `licenses` — Registry tables

Static reference tables. `libraries` tracks all import sources with their API endpoints,
import tier assignment, and license class. `licenses` is seeded with the complete
license-tier policy (game_approved flag is the authoritative gate for selection pattern
filtering). Both tables support future additions without schema migration.

---

## 3. Index Rationale

### Primary selection index (most important)
```sql
CREATE INDEX idx_weapons_selection_core ON weapons
    (gear_catalogue_id, range_class, tech_level, cultural_lineage, readiness_state);
```
**Rationale:** The canonical selection query (selection-patterns.md § P1) filters on all five
of these columns. A compound index on them in this order (high-selectivity predicates first)
allows SQLite to do a single range scan without full table scan. Expected cardinality at
100K weapons: gear_catalogue_id (15 values → ~6,667/value), range_class (4 values → ~1,667/value
after gear filter), tech_level (8 values → ~208/value after prior filters). Final result set
for a specific (gear, range, tech, culture) tuple: typically 10–100 rows — scannable without
further index.

### Density routing index
```sql
CREATE INDEX idx_weapons_density_vec ON weapons (gear_catalogue_id, range_class);
```
**Rationale:** Density queries aggregate over (gear_catalogue_id, range_class) pairs. This
covers the COUNT queries in the density maintenance job.

### Source provenance index for license filtering
```sql
CREATE INDEX idx_sources_primary ON weapon_sources (weapon_id, is_primary) WHERE is_primary = 1;
```
**Rationale:** The selection views join `weapon_sources` with `is_primary = 1`. A partial
index on is_primary=1 rows only reduces index size proportionally.

---

## 4. Migration Considerations

Since this is a greenfield DB, no migration concerns exist for v1. For future re-population:

**v1 → v2 migration patterns (anticipated):**

1. **Adding new gear catalogue entries (>15):** The `gear_catalogue_id` column is an unconstrained
   INTEGER (not a FK to a separate table by design). Adding gear 16+ requires no schema change —
   just update the tag_taxonomy seed data and import new weapons with the new ID.

2. **Adding new tag namespaces:** `tag_taxonomy` accommodates new namespaces without schema change.
   New namespaces can be added via INSERT into tag_taxonomy.

3. **Refining aesthetic enums (e.g., splitting 'medieval' into sub-eras):** Requires an UPDATE
   pass on the `weapons` table plus CHECK constraint revision via ALTER TABLE. Feasible in SQLite
   3.35+ (ALTER TABLE supports dropping constraints). Recommend: version the check constraints
   by storing them in a migration script outside the main schema.sql.

4. **Adding vector embedding column for similarity search (post-v2):** The `weapons` table can
   be extended with a BLOB column for embedding vectors. SQLite's built-in vector similarity
   (available via sqlite-vec extension) would require one additional extension installation.

5. **Moving DB to a server-side Postgres (post-demo2):** The schema is PostgreSQL-compatible
   with minor changes: INTEGER PRIMARY KEY AUTOINCREMENT → SERIAL, TEXT types are identical,
   CHECK constraints are identical, indexes are identical in syntax. Migration path is clean.

---

## 5. Full Table List

| Table | Rows (at 100K import) | Primary access pattern |
|---|---|---|
| `weapons` | 100K (target) | range scan via idx_weapons_selection_core |
| `weapon_sources` | ~120K (some weapons in 2 sources) | JOIN via idx_sources_primary |
| `weapon_tags` | ~500K (avg 5 tags/weapon) | JOIN via idx_weapon_tags_weapon |
| `tag_taxonomy` | ~100 (controlled vocab) | lookup by namespace+value |
| `weapon_sim_props` | ~30K (only verified weapons) | PK lookup |
| `weapon_aesthetic` | ~100K (populated at import) | PK lookup |
| `weapon_readiness` | ~100K (all weapons) | PK lookup |
| `substrate_density` | 7 × 3 × 15 = 315 (max) | full table scan acceptable at this size |
| `libraries` | ~15 | full table scan acceptable |
| `licenses` | ~12 | full table scan acceptable |

**Total DB size estimate at 100K weapons:**
- weapons: ~100K × 500 bytes avg = ~50 MB
- weapon_tags: ~500K × 50 bytes = ~25 MB
- weapon_sources: ~120K × 300 bytes = ~36 MB
- Other tables: ~10 MB
- Total estimated: ~120 MB — well within SQLite's operational range

---

## 6. Open Questions for Matt/Gandalf Review

1. **Should `gear_catalogue_id` be a strict FK to a `gear_catalogue` table, or stay as an integer
   with tag_taxonomy lookup?** Current design: tag_taxonomy lookup. If the gear catalogue
   is expected to grow substantially (>30 entries), a dedicated gear_catalogue table is cleaner.

2. **Should `dominant_element_affinities` be a normalized table or comma-separated string?** Current
   design: comma-separated TEXT for simplicity. At 7 elements, JSON_EACH() queries are adequate.
   If multi-element queries become performance-sensitive, normalization to a dedicated table is warranted.

3. **Should `weapon_readiness` be a separate table or columns on `weapons`?** Current design: separate
   table to avoid bloating the selection hotpath with pipeline state columns. If rocket/drax
   prefer fewer joins, these can be folded back into `weapons` table.

4. **BDI ω calibration field placement:** `best_omega_score` is currently a column on `weapons`.
   After H3 hypothesis test (W1.21), per-element ω scores may be needed (7 scores per weapon).
   This would require a `weapon_element_omega` junction table. Deferred to v1.1.

---

**Signed (research):** legolas (research scout; Mode A analytical design)
**For:** Matt approval of schema before import pipeline execution dispatch;
rocket (W1.15) and drax (loadout app) consume schema for implementation.
