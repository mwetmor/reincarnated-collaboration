# MIGRATION — 2026-05-24 — Cycle 10 Stage 1.5 schema delta (8 additive columns)

**Author:** elrond (data steward)
**Authority:** knight-rider Cycle 10 dispatch (Matt 2026-05-23 parent authorization; ADR-006 heuristic-execution scope)
**Status:** v1 — cross-seam impact declaration per ADR-004 + REVIEW_PROCESS Principle 6
**Target DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (gitignored; loadout-repo-owned data dir; elrond-owned schema per AGENTS.md)

---

## §1 What changed (one line)

`weapon_knowledge_entries` gains 8 new columns (`extracted_*`) populated from regex + structured-properties + seed-list extraction; no rows DELETEd; no columns dropped/renamed; same additive-column pattern as Phase D + Stage 1 (parallel).

## §2 Why (one line)

Cycle 10 Stage 1.5 mines the rich-structured-field sources for named-bearer attribution + materials + provenance + dimensions + historical-use, producing Track M1 mining dividend + Stage 2 cross-tab input.

## §3 Who's affected

### §3.1 Cross-seam consumer check

`weapon_knowledge_entries` consumer search results (same query as Phase D MIGRATION.md §3.1):

| Repo | Production-code consumers | Notes |
|---|---|---|
| `reincarnated-loadout` | 0 | engine season JSON exports consumed; not this table |
| `reincarnated-engine` | 0 | engine's own telemetry.db is separate file |
| `reincarnated-demo` | 0 | reads engine season JSON only |
| `reincarnated-collaboration` | legolas crawl scripts (write-only INSERTs with explicit columns) | unaffected by additive schema |

### §3.2 Within-domain (elrond's seam) impact

- 8 new columns ALTER-added; all NULL-defaulted (no CHECK constraints)
- ~89,841 rows updated with extracted_* values (NULL where source-schema has no signal)
- Stage 1 parallel dispatch operates on disjoint `proxy_*` columns — no conflict

## §4 What downstream consumers need to do

**Nothing** — schema delta is purely additive, all new columns NULL-defaulted, no existing columns dropped/renamed/retyped. Backward-compatible.

### §4.1 Future consumers (informational)

- **Stage 2 cross-tab refinement (elrond, future Wave 3)** — reads `extracted_*` columns to compose v1_scope quality scores
- **Stage 2.5 quality composite scoring (elrond, future Wave 3)** — reads `extracted_provenance_richness` as composite-score input
- **Phase 5 cohesion-judge alignment scoring (gamora / star-lord, future)** — may read `extracted_named_bearer` to feed bearer-alignment soft-bias scoring per skill-system § 12.3
- **Track M1 substrate-spine bearer mining (legolas, deferred)** — consumes `named-bearer-matches.json` as already-mined attribution baseline; reduces M1 crawl scope ~50-65% per `track-m1-mining-dividend.md` § 2.2

## §5 Schema diff (additive only)

```sql
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_length_value REAL;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_length_unit TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_weight_value REAL;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_weight_unit TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_materials TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_named_bearer TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_provenance_richness REAL;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_historical_use TEXT;
```

No views added. No CHECK constraints (extraction values free-text + REAL).

| Item | Status |
|---|---|
| Columns dropped | 0 |
| Columns renamed | 0 |
| Columns retyped | 0 |
| Enum values changed | 0 |
| Tables dropped | 0 |
| Tables renamed | 0 |
| Indexes dropped | 0 |
| Rows DELETEd | 0 |

## §6 Row-level mutations

| Mutation | Rows | Reversible? |
|---|---:|---|
| UPDATE `extracted_length_value/unit` | 6,247 populated; remainder NULL | Yes — reverse via pre-step backup at `backups/telemetry.db.pre-stage-1-5-2026-05-24` |
| UPDATE `extracted_weight_value/unit` | 10,063 populated | Yes |
| UPDATE `extracted_materials` | 8,895 populated | Yes |
| UPDATE `extracted_named_bearer` | 1,051 populated | Yes |
| UPDATE `extracted_provenance_richness` | 87,623 non-zero (full substrate; even thin sources get small score) | Yes |
| UPDATE `extracted_historical_use` | 13,613 populated | Yes |

## §7 Backward-compatibility checklist

| Check | Status |
|---|---|
| Existing INSERT statements (legolas crawl scripts) continue to work | ✓ — all 8 new columns are NULL-defaulted |
| Existing SELECT statements continue to work | ✓ — no columns dropped/renamed |
| Existing PRAGMA introspection | ✓ — total columns: 25 → 33 (8 added) |
| Existing UNIQUE constraint preserved | ✓ |
| Existing indexes preserved | ✓ |
| Stage 1 parallel `proxy_*` columns | ✓ — disjoint column namespace; no write conflict |
| Phase D MIGRATION.md columns | ✓ — disjoint; Phase D added 9 different column names |

## §8 Migration execution order

1. Backup: `cp telemetry.db backups/telemetry.db.pre-stage-1-5-2026-05-24` ✓ (155 MB)
2. `scripts/01_schema_migration.py` — ALTER × 8 (idempotent PRAGMA-guarded) ✓
3. `scripts/02_extract_structured_fields.py` — full population (~1 sec; 89,841 rows; 7 columns updated) ✓
4. `scripts/03_extract_named_bearer.py` — bearer extraction (~6 min; 89,841 rows scanned; 1,051 bearer-populated; rep-audit overlay applied) ✓
5. Post-execution verification: per-source coverage table + match log ✓ (see `per-source-coverage.md`)
6. Spot-check artifact landed for gandalf review ✓ (see `spot-check-gandalf-request.md`)
7. Track M1 dividend memo authored ✓ (see `track-m1-mining-dividend.md`)
8. Tag `elrond/v0.0-cycle-10-stage-1-5-structured-field-extraction` pending gandalf 30-row spot-check pass

## §9 Verification statement

Per ADR-004: grep verified `weapon_knowledge_entries` has zero production-code consumers (same as Phase D MIGRATION.md §3.1; substrate environment unchanged in 2 days).

Per REVIEW_PROCESS Principle 6 (cross-seam round-trip discipline): Stage 1 elrond sub-agent operates on `proxy_*` columns in parallel; disjoint column namespace verified via dispatch §3 column list comparison (`proxy_range_class`, `proxy_geometry_class`, `proxy_tempo_class`, `proxy_attribute_class`, `proxy_fingerprint_confidence` vs `extracted_*`). No write conflict.

## §10 Authority + sign-off

**Approved by:** Matt 2026-05-23 (Cycle 10 parent dispatch authorization; ADR-006 heuristic-execution scope per dispatch § 5)
**Executed by:** elrond
**Cross-seam coordination:** none (zero consumers)
**Next:** gandalf 30-row spot-check verdict → tag intent fires.

---

**Signed:** elrond (data steward; Cycle 10 Stage 1.5 executor)
