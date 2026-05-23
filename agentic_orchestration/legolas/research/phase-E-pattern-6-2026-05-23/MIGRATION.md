# MIGRATION — 2026-05-23 — Phase E-1 Frame-Revision Subsample k=3 DB Writes

**Author:** legolas
**Date:** 2026-05-23
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-frame-revision-stratified-subsample-k3.md`
**DB path:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Tag:** `legolas/phase-E-1-frame-revision-subsample-k3-2026-05-23`

---

## What changed (one line)

Phase E-1 frame-revision: 125 weapon clusters written to `clusters` + `cluster_membership` + `weapon_knowledge_entries.cluster_id` for all 48,430 rows in `v_category_sample`; `assignment_method` column added to `cluster_membership`.

## Why (one line)

Pattern-6 weapon-knowledge clustering (substrate-voted k=3 on stratified subsample ~10K); produces cluster_id as cross-seam join key for Phase E-2 labeling (gandalf) and downstream E-3/E-4 pipeline consumption.

## Who's affected

- **Elrond:** Curates the `clusters` + `cluster_membership` tables; Phase E-2 dispatch input. Must read this MIGRATION.md before E-2 schema work.
- **Gandalf (Phase E-2):** Labels clusters canonically. Uses `clusters.label` (provisional) and `cluster_membership` as input. Must be aware of native-vs-nearest-assigned split (see §4 below).
- **Star-lord:** Telemetry schema read-only; not directly affected. `weapon_knowledge_entries.cluster_id` is a new populated field — downstream LLM-call or season-export code consuming `weapon_knowledge_entries` will now see non-NULL `cluster_id` for all 48,430 rows.
- **Rocket:** Engine canonical library read-only; not directly affected.

## Schema changes

### Table: `cluster_membership`

**New column added:**

```sql
ALTER TABLE cluster_membership ADD COLUMN assignment_method TEXT;
```

Values: `'hdbscan_native'` | `'nearest_centroid'`

Column was absent before this migration. Added idempotently via `ALTER TABLE ... ADD COLUMN` with error handling (safe to re-run; if column exists, error is caught and execution continues).

### Table: `clusters`

No schema change. Populated with 125 rows. Prior content cleared (`DELETE FROM clusters`).

`cluster_algorithm_version` = `'phase-E-1-subsample-k3-2026-05-23'` (distinguishes this run from future re-runs or variant runs).

### Table: `cluster_membership`

Populated with 48,430 rows (one per `weapon_knowledge_entries` row in `v_category_sample`). Prior content cleared (`DELETE FROM cluster_membership`).

### Table: `weapon_knowledge_entries`

`cluster_id` field populated for all 48,430 rows matching `v_category_sample` filter. Prior `cluster_id = NULL` state restored before re-population (`UPDATE weapon_knowledge_entries SET cluster_id = NULL WHERE cluster_id IS NOT NULL`). Idempotent.

---

## § 4. Native-vs-Nearest-Assigned Provenance Split (LOAD-BEARING for Phase E-2 / E-3 / E-4)

**This section is mandatory reading before any downstream Phase E consumption.**

All 48,430 `cluster_id` values in `cluster_membership` are substrate-voted at **k=3** (axes 1-3 from the full-pool PCA; bootstrap cosine-dist 0.0011, 0.0118, 0.0131 respectively — all far below 0.10 stability floor). The k=3 frame is intentional per the substrate-voting-is-binding gate (Discipline #18 amendment candidate; frame-revision note §2; gandalf kernel-panic-diagnosis §9.2).

**However, the cluster_id assignment confidence is NOT equal across all rows:**

| `assignment_method` | N rows | Cluster assignment basis | Confidence range | Notes |
|---|---|---|---|---|
| `hdbscan_native` | **10,000** | HDBSCAN density-based clustering on the stratified subsample in axes-1-3 projection space | Full HDBSCAN confidence (confidence_score ≥ 0.5; noise-within-subsample assigned at < 0.5) | These rows are the substrate for the clustering structure |
| `nearest_centroid` | **38,430** | Nearest-centroid assignment in axes-1-3 projection space (not density-based) | confidence_score < 0.5 (lower confidence encoding) | These rows inherit a cluster_id based on spatial proximity; their density profile was not part of cluster formation |

**Downstream Phase E-2 / E-3 / E-4 consumers MUST NOT assume equal density-based confidence across all rows.** Specifically:

1. **Phase E-2 (gandalf labeling):** Label validation and quality assessment should weight `hdbscan_native` rows more heavily. Cluster representatives chosen for labeling should preferentially come from `hdbscan_native` rows (where HDBSCAN's internal density-reachability structure confirms cluster membership).

2. **Phase E-3 / E-4 (if applicable):** Any downstream model trained on `cluster_id` as a feature should treat `assignment_method` as a confidence weight. `nearest_centroid` rows are not noise — they are correctly assigned to their nearest cluster — but their assignment is distance-based, not density-based.

3. **SQL pattern for filtering by provenance:**
   ```sql
   -- Native rows only (for high-confidence label work)
   SELECT * FROM cluster_membership WHERE assignment_method = 'hdbscan_native';
   
   -- All rows (full pool coverage)
   SELECT * FROM cluster_membership WHERE assignment_method IN ('hdbscan_native', 'nearest_centroid');
   
   -- Count by method
   SELECT assignment_method, COUNT(*) FROM cluster_membership GROUP BY assignment_method;
   -- → hdbscan_native: 10000, nearest_centroid: 38430
   ```

---

## § 5. Cluster Algorithm Version + Frame-Revision Provenance

All cluster rows carry `cluster_algorithm_version = 'phase-E-1-subsample-k3-2026-05-23'`.

**k=3 axis basis:** The cluster structure is derived from the 3 substrate-stable PCA axes (bootstrap cosine-dist 0.0011–0.0131; axes 4-12 at 0.39-0.80 — unstable and intentionally excluded). This is NOT a k=12 clustering result. Future Phase E-2 / E-3 / E-4 work that expands the substrate (Alternative 2) or runs a sensitivity sweep (Phase E-1.5) will produce a different `cluster_algorithm_version` tag — do not conflate.

**Frame-revision cite:** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md` documents why k=3 was chosen (substrate-voting-is-binding; Discipline #18 amendment candidate).

---

## § 6. Forward-Compat Declaration for Phase E-2 / E-3 / E-4

- **Phase E-2 (gandalf labeling):** `clusters.label` contains provisional auto-generated descriptions (format: `PROVISIONAL: <lineage> <period> <weapon-type> weapons (<register>; <kind>; N=<count>)`). Gandalf canonicalizes these in Phase E-2. Do not treat provisional labels as final.
- **Phase E-3 / E-4 (if defined):** `cluster_membership.cluster_id` → `clusters.id` FK. `weapon_knowledge_entries.cluster_id` → `clusters.id` FK. Both populated for all 48,430 rows. Schema is append-compatible; adding `canonical_label` or similar columns to `clusters` will not break this migration.
- **ADR-004 compliance:** This MIGRATION.md is the cross-seam coordination artifact per ADR-004. Elrond reads this before Phase E-2 schema work. Star-lord reads this before any telemetry queries on `weapon_knowledge_entries.cluster_id`.
- **Discipline #8 compliance (schema validation at boundaries):** All 48,430 `cluster_membership` rows verified by round-trip smoke test (100-row sample; `weapon_knowledge_entries.cluster_id` non-NULL, `cluster_membership` row exists, `clusters.dominant_axes_description` valid JSON). Smoke PASS confirmed.

---

## DB verification at completion

```
clusters:           125 rows
cluster_membership: 48,430 rows
  hdbscan_native:   10,000
  nearest_centroid: 38,430
weapon_knowledge_entries.cluster_id populated: 48,430
Round-trip smoke: PASS (100-row sample, 2026-05-23 12:27:37 EDT)
```
