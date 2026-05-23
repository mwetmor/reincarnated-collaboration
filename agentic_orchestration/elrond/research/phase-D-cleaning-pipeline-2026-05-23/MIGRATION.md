# MIGRATION — 2026-05-23 — Phase D cleaning-pipeline schema delta + classification mutations

**Author:** elrond (data steward)
**Authority:** Matt 2026-05-23 (whole-pipeline upfront authorization)
**Status:** v1 — cross-seam impact declaration per ADR-004 + REVIEW_PROCESS Principle 6
**Target DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (gitignored; loadout-repo-owned data dir; ELRoND-owned schema per AGENTS.md)

---

## §1 — What changed (one line)

`weapon_knowledge_entries` gains 9 new columns + 3 new views; ~89,839 rows undergo classification mutations (weapon_kind / dedup_status / variant_relationship / cultural_lineage_canonical / historical_period_canonical / register_canonical / cultural_lineage_confidence / wieldable_humanoid / template_quality_score) across the 7-step Phase D pipeline. No columns dropped; no enums tightened; no rows DELETEd; 2 source_library renames (pf2ools, souls-api-items.js subset) with audit-archives.

## §2 — Why (one line)

Phase D operationalizes Matt-locked F1-F6 + G1-G5 + gandalf math-anchored cleanliness bars (Phase B framework) against legolas Phase A empirical baselines (FP 2.83%, ammo-boundary 17.5%, raw-dup 47.0%) to produce clean canonical-merged substrate suitable for Phase E Pattern-6 axis discovery.

## §3 — Who's affected

### §3.1 Cross-seam consumer search results

`weapon_knowledge_entries` is consumed by **zero** seam-owned production code paths.

Verification method: `grep -r "weapon_knowledge_entries" --include={.ts,.tsx,.js,.jsx,.py,.sql}` against all four repos:

| Repo | Production-code consumers | Notes |
|---|---|---|
| `reincarnated-loadout` (drax) | **0** | Loadout web app reads engine season JSON exports + per-season `data/season_NNN/` artifacts; does NOT query the loadout-repo `data/telemetry.db` for weapon-knowledge entries. (telemetry.db in loadout/data/ historically holds engine-emitted telemetry exports; the knight-rider overnight cascade 2026-05-22 amendment co-located the weapon-knowledge tables on this same SQLite file by convention, not by loadout-consumption.) |
| `reincarnated-engine` (rocket / gamora / star-lord) | **0** | Engine's own telemetry DB is `reincarnated-engine/data/telemetry.db` (separate file in the engine repo); engine does NOT cross-read the loadout-repo telemetry.db. |
| `reincarnated-demo` (drax) | **0** | Demo consumes engine season JSON + demo-local Pixi.js assets; no DB queries. |
| `reincarnated-collaboration` (orchestration/research) | **legolas crawl scripts only** — write-only ingest at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/scripts/*.py`. INSERT OR IGNORE patterns using explicit-column lists against the v1.1.0 column set. New columns have DEFAULTs → existing INSERTs continue to work unchanged. |

### §3.2 Within-domain (elrond's seam) impact

- **`weapon_knowledge_entries` table:** 9 new columns ALTER-added; classification mutations on ~89K rows across 7 steps.
- **`knowledge_entry_canonical_merge` table:** ~3,500-10,000 new rows inserted (one per canonical produced by F1 + F4 merges).
- **Per-row `text_embedding` BLOB column** (existing in schema): populated for ~47K canonical rows during Step 7 embedding-compute.

## §4 — What downstream consumers need to do

**Nothing** — schema delta is additive, all new columns have DEFAULTs ('unknown' / 0.0), no existing columns dropped/renamed/retyped, no enum values removed, no row counts shrunk except via documented Discipline-#11 quarantine pattern (source_library rename; rows remain queryable in DB).

### §4.1 Future consumers (post-Phase-E) — informational, not blocking

When Phase E (Pattern-6 axis discovery) lands and downstream consumers begin reading `weapon_knowledge_entries`, they should:
- Filter on `dedup_status IN ('canonical', 'unprocessed')` to get the deduplicated substrate (excluding `merged_into` rows that point to a canonical via the `knowledge_entry_canonical_merge.merged_entry_ids` JSON array).
- Use `v_category_sample` view for category sampling (engine sample-pool draws); this view applies the canonical filter set per gandalf § 2.7 + ammo + quarantine exclusions.
- Use `v_category_sample_humanoid_strict` for engine-side strict wieldability filtering (excludes `either` and `mount_required`).
- Use `v_category_sample_humanoid_permissive` for cohesion-judge expansive sample requests (includes `mount_required` for siege-style profiles).

### §4.2 If a Phase D-bis re-fire happens (per math note Q7)

Same backward-compat profile — re-fire is idempotent UPDATE patterns; consumers see the same column set with possibly-different values per row. No schema change in a Phase D-bis.

## §5 — Schema diff (additive only)

### §5.1 Columns added to `weapon_knowledge_entries`

```sql
-- All 9 columns are NULLable or have DEFAULTs; existing readers see populated 'unknown' / 0.0 values
ALTER TABLE weapon_knowledge_entries ADD COLUMN wieldable_humanoid TEXT DEFAULT 'unknown' CHECK (...);
ALTER TABLE weapon_knowledge_entries ADD COLUMN weapon_kind TEXT DEFAULT 'unknown' CHECK (...);
ALTER TABLE weapon_knowledge_entries ADD COLUMN dedup_status TEXT DEFAULT 'unprocessed' CHECK (...);
ALTER TABLE weapon_knowledge_entries ADD COLUMN variant_relationship TEXT DEFAULT 'independent';
ALTER TABLE weapon_knowledge_entries ADD COLUMN cultural_lineage_canonical TEXT DEFAULT 'unknown' CHECK (...);
ALTER TABLE weapon_knowledge_entries ADD COLUMN historical_period_canonical TEXT DEFAULT 'unknown' CHECK (...);
ALTER TABLE weapon_knowledge_entries ADD COLUMN register_canonical TEXT DEFAULT 'unknown' CHECK (...);
ALTER TABLE weapon_knowledge_entries ADD COLUMN cultural_lineage_confidence REAL DEFAULT 0.0 CHECK (...);
ALTER TABLE weapon_knowledge_entries ADD COLUMN template_quality_score REAL DEFAULT 0.0 CHECK (...);
```

Full DDL with CHECK constraints in `phase-D-math-note.md` § 1.2.

### §5.2 Views added

```sql
CREATE VIEW v_category_sample AS ... ;                          -- Engine default consumption view
CREATE VIEW v_category_sample_humanoid_strict AS ... ;          -- Strict-humanoid wieldability
CREATE VIEW v_category_sample_humanoid_permissive AS ... ;      -- Permissive (adds mount_required)
```

Full DDL in `phase-D-math-note.md` § 1.3.

### §5.3 No DROPS / RENAMES / RETYPES

| Item | Status |
|---|---|
| Columns dropped | 0 |
| Columns renamed | 0 |
| Columns retyped | 0 |
| Enum values removed | 0 |
| Tables dropped | 0 |
| Tables renamed | 0 |
| Indexes dropped | 0 |

### §5.4 Row-level mutations

| Mutation type | Approximate row count | Reversible? |
|---|---|---|
| `weapon_kind` updates (classification) | ~26,000 rows leave 'unknown' default | Yes — idempotent UPDATE; reverse via pre-step backup |
| `dedup_status` updates (F1 + F4 collapse) | ~26,000-30,000 rows become 'merged_into'; ~7,000-10,000 become 'canonical' | Yes — pre-step backup |
| `variant_relationship` updates | ~26,000 rows | Yes — pre-step backup |
| `cultural_lineage_canonical` / `historical_period_canonical` / `register_canonical` populated | ~80,000 rows (≥ 70-95% coverage on v_category_sample) | Yes — pre-step backup |
| `source_library` rename (Discipline #11 quarantine) | 688 (pf2ools) + 56 (souls-api items.js) = 744 rows | Yes — reverse UPDATE; archive files retained |
| `text_embedding` BLOB populated | ~47,000 rows | Yes — pre-step7 backup |
| Row INSERTs (AOS-2 compound split) | 2 new rows (Skull Bludgeon + Varanspire Gladius child entries) | Yes — DELETE pair via parent-canonical_id reference |
| Row INSERTs into `knowledge_entry_canonical_merge` | ~3,500-10,000 new rows | Yes — pre-step backup |
| Row DELETEs | **0** | N/A (audit-preservation; Discipline #11) |

## §6 — Backward-compatibility checklist

| Check | Status |
|---|---|
| Existing INSERT statements continue to work | ✓ — all 9 new columns have DEFAULTs; legolas crawl scripts unaffected |
| Existing SELECT statements continue to work | ✓ — no columns dropped or renamed |
| Existing PRAGMA/introspection consumers continue to work | ✓ — table layout preserved; new columns appended after existing 17 |
| Existing UNIQUE constraint on (source_library, source_url) | ✓ — preserved (Discipline #11 quarantine renames source_library but UNIQUE constraint survives because no rows have identical (renamed, url) pairs) |
| Existing indexes continue to work | ✓ — no index drops |

## §7 — Forward-compatibility (Phase E + beyond)

| Future consumer | Interface |
|---|---|
| Phase E Pattern-6 PCA pass (rocket/legolas) | Reads `v_category_sample` for axis-discovery feature vectors. Uses `cultural_lineage_canonical` + `historical_period_canonical` + `register_canonical` as one-hot features (26-dim aggregate). Reads `text_embedding` BLOB + `structured_feature_vector` BLOB for joint embedding. Filter: `dedup_status='canonical'` + weapon_kind tags. |
| Engine category sampling (post-Phase-E, post-cohesion-judge integration) | Reads `v_category_sample` or its humanoid-strict/permissive variants. N=20-50 draw per category. |
| Cohesion-judge `template_quality_score` consumer | Reads `template_quality_score` REAL [0.0, 1.0] for sample-priority weighting on named_template rows. |
| `phase-D-flagged-clusters.md` reader (Matt + gandalf design-review) | Reads markdown doc with Matt-principle dispositions + post-execution Matt-review items. Not a DB consumer. |
| Future Phase D-bis hook | Re-runs Steps 5-7 with adjusted detection rules; same column set. |

## §8 — Migration execution order (this dispatch only)

1. Backup: `cp telemetry.db backups/telemetry.db.pre-schema-migration-2026-05-23`
2. ALTER TABLE × 9 (idempotent via PRAGMA-guarded runner)
3. CREATE VIEW × 3 (idempotent via sqlite_master-guarded runner)
4. PRAGMA smoke test: confirm 26 columns + 3 views; SELECT COUNT(*) FROM v_category_sample (expect 0 pre-classification)
5. 7-step pipeline per math note § 7
6. End-of-pipeline VACUUM
7. Tag + commit per dispatch acceptance criteria

## §9 — Round-trip smoke fixture (per dispatch + Amendment 3)

**240-row fixture (10 rows × 22 active source libraries; pf2ools-quarantined + souls-api-thomaslincoln-quarantined excluded post-Step-3)** PLUS additional known-merge / known-non-merge pairs per Amendment 3:

| Fixture category | Expected outcome |
|---|---|
| **Known-merge pair 1**: `Excalibur` in wikipedia + `Excalibur` in wikidata | Step 7 produces single canonical; both rows' `dedup_status='merged_into'` (one survives as canonical) or one canonical with other merged. |
| **Known-merge pair 2**: `Aegis` in wikipedia + `aegis` in wikidata (case-insensitive match) | Same — F4 with cosine ≥ 0.90 + cross-source + wikidata-corroboration confirms merge. |
| **Known-non-merge pair 1**: `Excalibur` (mythological) vs `M982 Excalibur` (artillery shell) | Step 5 brand-prefix disambiguation tags M982 as `weapon_kind='category'`; Step 6 tags bare `Excalibur` as `weapon_kind='unique'`; Step 7 blocking prevents merge (different cultural_lineage_canonical: european-mythological vs cross_cultural-military_modern). Both stay `dedup_status='canonical'`. |
| **Known-non-merge pair 2**: `Tyrfing` (Norse legend) vs `Tyrfing` anti-radar missile (modern military) | Same pattern — name match but cultural_lineage_canonical differs (european-mythological vs military_modern); desc cosine LOW (different domains); Step 5 brand-prefix detection catches the modern-military referent. |
| **Per-source 10-row check** | Each active source's first 10 rows have all 9 new columns populated post-pipeline; PRAGMA confirms; `v_category_sample` returns expected row counts per source-eligibility. |

## §10 — Verification statement

Per ADR-004: this MIGRATION.md was authored AFTER an empirical grep of all four repos for `weapon_knowledge_entries` consumers; the "zero consumers" claim is verified, not assumed. The legolas crawl scripts (~13 scripts in collab repo) are write-only ingest paths using explicit-column INSERTs that backward-compatibly survive the additive schema delta. No drax-side investigation needed beyond the grep result (which is empty); no rocket-side investigation needed (engine's telemetry.db is a separate file).

Per REVIEW_PROCESS Principle 6 (cross-seam round-trip discipline): round-trip smoke fixture per § 9 above; Step 7 must produce correct `dedup_status` on the 2 known-merge pairs + 2 known-non-merge pairs.

## §11 — Authority + sign-off

**Approved by:** Matt 2026-05-23 (whole-pipeline upfront authorization)
**Executed by:** elrond
**Cross-seam coordination required:** none (zero consumers)
**Next:** schema migration applied → 7-step pipeline → acceptance gates → tag.

---

**Signed:** elrond (data steward; Phase D Pattern-B executor)
