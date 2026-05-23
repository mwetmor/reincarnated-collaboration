# MIGRATION — 2026-05-23 — Phase E-2-DB cluster-label UPDATE + cluster_type column add

**Author:** elrond
**Date:** 2026-05-23
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-elrond-phase-E-2-DB-cluster-label-update.md`
**DB path:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Tag:** `elrond/phase-E-2-DB-2026-05-23`
**Authorization:** explicit Matt approval 2026-05-23 ~13:15 EDT (per ADR-006) covering this DB write
**Parent migration:** `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md` (Phase E-1 cluster writes)

---

## What changed (one line)

Replaced all 125 `clusters.label` PROVISIONAL strings with gandalf-canonical labels and added `clusters.cluster_type TEXT` populated per-row, single transaction.

## Why (one line)

Phase E-2 gandalf labeling commit `5b8754e` ratified by jack-ryan Gate-2 + gandalf design-side spot-check; this is the DB write that lifts canonical labels into the catalogue store consumed by Phase E-3/E-4 + downstream engine/loadout consumers.

## Who's affected

- **Gandalf (Phase E-3 and beyond):** Canonical labels and `cluster_type` now live in DB; future work reads from one store (DB) rather than DB + JSON sidecar.
- **Star-lord:** Read-only telemetry queries on `weapon_knowledge_entries.cluster_id` JOIN `clusters` now return substrate-descriptive canonical labels instead of `PROVISIONAL:` placeholders.
- **Drax:** Loadout app (`reincarnated-loadout`) — DB lives in this repo's `data/telemetry.db`; any cluster-label surfacing in UI will now show canonical labels.
- **Rocket:** Engine canonical library unaffected (no engine-internal schema touched).
- **Legolas:** Phase E-1.5 sensitivity sweep (if/when fired) inherits the new column; will need to populate `cluster_type` on any newly written cluster rows.

## Schema changes

### Table: `clusters`

**New column added (idempotent):**

```sql
ALTER TABLE clusters ADD COLUMN cluster_type TEXT;
```

Catches `OperationalError: duplicate column name` (safe to re-run; if column exists, error is caught and execution continues).

**Domain (7 distinct values populated; gandalf-authored substrate-honest meta-typology):**

| `cluster_type` value           | N clusters | Semantic |
|---|---|---|
| `weapon_family`                  | 50 | Substrate-coherent weapon-form group within a lineage/period |
| `named_template_family`          | 41 | Magic-item / D&D-style named-template family (e.g., "Abyssal Bane") |
| `mixed_cross_cultural`           | 18 | Cross-cultural pool that is axis-coherent but weapon-form-heterogeneous |
| `mixed_form_pool`                | 9  | Form-heterogeneous pool within a single lineage/period |
| `modern_military_hardware_pool`  | 4  | Contemporary military hardware groupings |
| `rare_lineage_isolate`           | 2  | Small clusters dominated by a rare/non-canonical lineage |
| `metadata_bucket`                | 1  | Uncurated-period metadata-token cluster (substrate is uncurated) |

**No type-CHECK constraint added on the column.** Rationale: Phase E-1.5 sensitivity sweep may introduce new `cluster_type` values (gandalf authorship), and the column is gandalf-authoritative — a CHECK constraint would force a schema migration on every new type. Discipline #14 spirit (per-instance vocabulary stays explicit; mechanical labels stay internal).

**`clusters.label` column:** No schema change; row content updated. 125 rows transitioned from `PROVISIONAL: …` to substrate-descriptive canonical labels (e.g., `Fantasy-Generic "Abyssal Bane" Named-Template Mega-Family`, `East Asian Uncurated-Period Metadata Pool`).

### Tables NOT touched

- `cluster_membership` — unchanged (legolas Phase E-1 ownership; out of scope per dispatch).
- `weapon_knowledge_entries` — unchanged (read-only join target; `cluster_id` references untouched).

---

## § 4. Provenance + idempotency

**Input artifact:** `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`

- `cluster_algorithm_version` (in JSON): `phase-E-1-subsample-k3-2026-05-23` (matches legolas Phase E-1 algorithm-version tag in DB)
- `labeled_by` (in JSON): `gandalf`
- `label_authority`: `coarse_spine_canonical` (Phase E-2; weapon-form-resolution deferred to Phase E-1.5)
- 125 entries verified pre-write: `db_cluster_id` densely covers `[1, 125]`; all `canonical_label` + `cluster_type` non-null.

**Indexing note (LOAD-BEARING):**
- JSON `id` field (0-124) = legolas cluster_id used in `clusters.md` + axis-discovery + dispatch text.
- JSON `db_cluster_id` field (1-125) = SQLite `clusters.id` primary key.
- This UPDATE used `db_cluster_id` in the WHERE clause (per dispatch locked decision).

**Idempotency:** Re-running the curation script will:
1. Catch the `duplicate column name` error on ALTER TABLE (no-op skip).
2. Re-write the same 125 (label, cluster_type) pairs by db_cluster_id — net no-change.

**Pre-state captured for audit:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/pre-update-state-clusters.tsv` (125 rows, all PROVISIONAL).

**Post-state captured:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/post-update-state-clusters.tsv` (125 rows, canonical labels + cluster_type column).

---

## § 5. Decision record — ALTER TABLE clusters ADD COLUMN cluster_type

Per dispatch § "Open design question," I (elrond) had discretion to ALTER TABLE in this pass or defer.

**Decision: ALTER TABLE in this pass.**

Reasoning:
1. JSON carries `cluster_type` per row for all 125 clusters; deferring forces every downstream consumer to read both DB + sidecar JSON. Single-store reads beat dual-store reads.
2. Schema change is additive only (no existing column modified). ADR-002 sub-dispatch tier (additive metadata column does not trigger architectural-tier approval requirement).
3. Operation is idempotent — catches `duplicate column name` error if re-run.
4. Single-transaction with the `label` UPDATE keeps DB state consistent (either everything lands together or nothing does).
5. Precedent: Legolas Phase E-1 added `cluster_membership.assignment_method` under identical idempotent-additive-column logic.
6. No `CHECK` constraint added — gandalf is authoritative on `cluster_type` domain; sensitivity sweep + future labeling passes may add types without forcing a schema migration each time.

**Downstream notification (ADR-004 compliance):**
Star-lord and Drax: when you read `clusters` and want to filter or label by typology, query the new `cluster_type` column. The 7 current values are listed in § Schema changes above. Treat as gandalf-authored open vocabulary (no CHECK).

---

## § 6. Discipline #8 compliance — schema validation at boundaries

**Round-trip smoke test executed (100-row sample):**

```sql
SELECT wke.id, wke.canonical_name, wke.cluster_id, c.label, c.cluster_type
FROM weapon_knowledge_entries wke
JOIN clusters c ON c.id = wke.cluster_id
WHERE wke.cluster_id IS NOT NULL
ORDER BY wke.id
LIMIT 100;
```

Result: 100 rows returned; **0 orphans, 0 NULL labels, 0 PROVISIONAL labels, 0 NULL cluster_type values.** PASS.

Sample joined rows (first 3 + last 3) recorded in
`agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/scripts/run-log-2026-05-23.txt`.

**Verification gate counts:**

| Check                                                              | Expected | Observed |
|---|---|---|
| `SELECT COUNT(*) FROM clusters`                                    | 125 | 125 |
| `SELECT COUNT(*) FROM clusters WHERE label LIKE 'PROVISIONAL:%'`   | 0 | 0 |
| `SELECT COUNT(*) FROM clusters WHERE label IS NULL OR label = ''`  | 0 | 0 |
| `SELECT COUNT(*) FROM clusters WHERE cluster_type IS NULL OR ...`  | 0 | 0 |

**Spot-checks (dispatch-named clusters, indexed by `db_cluster_id`):**

| db_cluster_id | cluster_type           | canonical_label |
|---|---|---|
| 1   | mixed_cross_cultural     | Cross-Cultural Contemporary Mixed-Form Pool |
| 51  | mixed_form_pool          | European Contemporary Two-Hand Mixed Pool (Mil-Modern + Reproduction Blade) |
| 63  | named_template_family    | Fantasy-Generic "Abyssal Bane" Named-Template Mega-Family |
| 87  | rare_lineage_isolate     | S. American Indigenous Contemporary Shotgun Cluster |
| 91  | metadata_bucket          | East Asian Uncurated-Period Metadata Pool |

(Dispatch text mentioned "Cluster 50/62/86/90" — these are legolas-side `id` values from the JSON. The DB side uses `db_cluster_id`, which is `id + 1`. Spot-checks pass; labels match dispatch's expected framing exactly.)

---

## § 7. Observation surfaced for sub-carry follow-up (NOT a Phase E-2-DB defect)

During the round-trip smoke I observed an unrelated artifact worth flagging for the appropriate downstream owner:

- `weapon_knowledge_entries.id=3` "PMD series mines" is assigned to `cluster_id=116` ("European Uncurated-Period Spear Family"). PMD-series mines are landmines (Soviet anti-personnel) — not spears, and probably not European-period-coherent.
- This is a **substrate clustering artifact** (the row is `assignment_method=nearest_centroid` for that cluster — distance-based, not density-based), **not a labeling defect**.
- It surfaces as a candidate diagnostic for **9.11-C/D/E curation gap / substrate-tagging artifacts** (the existing elrond sub-carry suite), or for Phase E-1.5 sensitivity sweep.
- **Out of scope for this dispatch.** No action taken; logged here for knight-rider visibility.

---

## § 8. Forward-compat declaration for Phase E-3 / E-4 + engine/loadout consumers

1. **Phase E-3 / E-4 (gandalf-authored if/when defined):** `clusters.label` carries substrate-descriptive canonical labels; `clusters.cluster_type` carries gandalf meta-typology. Both populated for all 125 rows. Schema is append-compatible (additive only) with potential Phase E-1.5 re-clustering — if that pass re-populates `clusters`, ensure `cluster_type` is included in the write.
2. **Engine consumers (rocket/star-lord):** Catalogue-aware features (asset-pool selection, scaling-by-cluster, etc.) can now key off `clusters.label` and `clusters.cluster_type` as stable read-only signals.
3. **Loadout consumers (drax):** Any UI surfacing of `cluster_id` for a weapon entry can now display a canonical human-readable label + typology.
4. **ADR-004 compliance:** This MIGRATION.md is the cross-seam coordination artifact. Star-lord + Drax + Gandalf read this before any new code that depends on canonical labels.
5. **No DB push.** All writes local-only per ADR-006.

---

## DB verification at completion

```
clusters: 125 rows
  label LIKE 'PROVISIONAL:%' : 0
  label IS NULL              : 0
  cluster_type IS NULL       : 0
  cluster_type distribution  :
    weapon_family                50
    named_template_family        41
    mixed_cross_cultural         18
    mixed_form_pool               9
    modern_military_hardware_pool 4
    rare_lineage_isolate          2
    metadata_bucket               1
Round-trip smoke (100-row JOIN sample): PASS
```

Tag: `elrond/phase-E-2-DB-2026-05-23` (local; no push).
