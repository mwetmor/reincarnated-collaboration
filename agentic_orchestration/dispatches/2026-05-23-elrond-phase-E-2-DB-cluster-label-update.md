# Dispatch — 2026-05-23 — elrond — Phase E-2-DB cluster-label UPDATE from gandalf JSON

**From:** knight-rider
**To:** elrond (Pattern-A-light; data steward DB UPDATE pass; explicit Matt-approved DB-write authorization)
**Approved by:** Matt 2026-05-23 ~13:15 EDT (post Gate-2 PASS + gandalf spot-check relay)
**Estimated effort:** ~30-45 minutes (read JSON + author UPDATE script + execute + round-trip smoke + MIGRATION.md amendment + tag)
**Gate-1:** SKIPPED. No new methodology choices; mechanical UPDATE pass from gandalf's reviewed JSON. Jack-ryan Gate-2 PASS on gandalf output (`5b8754e`); gandalf design-side spot-check ratified labels as substrate-descriptive lock-compliant.
**Acceptance:** All 125 rows in `clusters` table have `label` populated from gandalf JSON's `canonical_label` field; zero rows remain with `label LIKE 'PROVISIONAL:%'`; round-trip smoke PASS; MIGRATION.md amended; tag cut.

---

## Why this dispatch exists

Gandalf Phase E-2 cluster labeling (commit `5b8754e`, tag `gandalf/phase-E-2-cluster-labeling-2026-05-23`) produced canonical labels for all 125 clusters in machine-readable JSON at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`. The DB `clusters.label` column currently holds provisional auto-generated descriptions from legolas's Phase E-1 fire. This dispatch UPDATEs `clusters.label` from gandalf's canonical labels.

Per dispatch boundary discipline (ADR-006 read-only-default + seam ownership): gandalf authors canonical content; elrond owns DB curation. This sub-dispatch is the explicit DB-write authorization for the canonical labels.

## Required reading before starting

1. **`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-output-gate-2-findings-record.md`** — Gate-2 findings synthesis + gandalf spot-check relay
2. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`** — your UPDATE input (machine-readable; 125 cluster entries)
3. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-completion-summary.md`** § Hand-off Notes — suggested SQL pattern + schema gap notes
4. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md`** § Schema changes — idempotent `ALTER TABLE ADD COLUMN` pattern precedent

## Locked decisions (not re-litigated)

- **Source of truth:** gandalf JSON `canonical_label` field per cluster — authoritative
- **UPDATE key:** `db_cluster_id` field on each JSON cluster entry maps to `clusters.id` (1-125 in SQLite)
- **NOT the `id` field:** the `id` field (0-124) is the legolas cluster_id for cross-doc reference and is NOT the DB primary key. **Use `db_cluster_id` for the UPDATE WHERE clause.**
- **Substrate-descriptive-only lock** (gandalf spot-check 13:15 EDT): canonical labels are substrate-descriptive; no cultural-tradition descriptors. Operational lock confirmed.

## Open design question — your call to make at fire time

**Should you ALTER TABLE clusters ADD COLUMN cluster_type TEXT in this dispatch?**

Jack-ryan Gate-2 Finding 4 surfaced this as a sub-dispatch design question, not a BLOCK. Tradeoffs:

| Option | Pros | Cons |
|---|---|---|
| ALTER TABLE now (in this dispatch) | Schema captures all gandalf-authored cluster metadata in one place; downstream Phase E-3/E-4 reads from DB consistently | Adds schema scope to a mechanical UPDATE pass; ADR-002 architectural-tier check arguable |
| Defer to Phase E-3 (or later) | Mechanical UPDATE-only scope preserved; cluster_type lives in JSON artifact (durable) | Phase E-3/E-4 consumers must read both DB + JSON for full picture |

**Recommendation (knight-rider):** ALTER TABLE in this dispatch IF the change is fully idempotent (catch error if column exists) AND populated from the JSON `cluster_type` field in the same transaction as the `label` UPDATE. Single-transaction DB state. The schema change is genuinely additive (no existing column modified); ADR-002 architectural-tier is not triggered (additive metadata column at sub-dispatch tier).

If you prefer to defer, document the deferral in MIGRATION.md + carry forward as sub-carry **9.11-H** for a future schema-extension dispatch.

## Scope

- [ ] Read gandalf JSON; verify 125 entries; verify all have non-null `canonical_label` + valid `db_cluster_id` (1-125; no gaps)
- [ ] Pre-UPDATE state capture: `SELECT id, label FROM clusters ORDER BY id` — log existing provisional labels (or null) for audit trail
- [ ] (Optional per design question above) `ALTER TABLE clusters ADD COLUMN cluster_type TEXT;` — idempotent; catch error if column exists
- [ ] Execute UPDATE in a transaction:
  ```sql
  BEGIN;
  UPDATE clusters SET label = ? WHERE id = ?;
  -- (optional) UPDATE clusters SET cluster_type = ? WHERE id = ?;
  -- one row per cluster from JSON; parameterized
  COMMIT;
  ```
- [ ] Verification queries:
  ```sql
  -- 1. All 125 clusters have non-PROVISIONAL labels
  SELECT COUNT(*) FROM clusters WHERE label LIKE 'PROVISIONAL:%';
  -- expected: 0
  
  -- 2. Total cluster count unchanged
  SELECT COUNT(*) FROM clusters;
  -- expected: 125
  
  -- 3. Label content sample (manual check)
  SELECT id, label FROM clusters WHERE id IN (1, 50, 90, 62, 86) ORDER BY id;
  -- 90 should show "East Asian Uncurated-Period Metadata Pool" or similar metadata-bucket framing
  -- 62 should show "Abyssal Bane Mega-Family" or similar prefix-bundled framing
  -- 86 should show S. American Indigenous Contemporary Shotgun framing
  ```
- [ ] Round-trip smoke test (50-100 row sample): for each sampled row, verify `weapon_knowledge_entries.cluster_id` joins cleanly to `clusters.id` and gets the new canonical label (no orphans; no NULL labels)
- [ ] Write MIGRATION.md amendment (append to existing `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md` OR new sibling at `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/MIGRATION.md` per your preference):
  - UPDATE pass executed (125 rows)
  - Pre-state captured (audit trail)
  - Optional ALTER TABLE outcome (did you add cluster_type column or defer?)
  - Cross-seam impact: `weapon_knowledge_entries.cluster_id` references `clusters.id` which now carries canonical labels — Phase E-3/E-4 + engine/loadout consumers see canonical labels in next read
  - ADR-004 + Discipline #8 compliance: round-trip smoke result; provenance to gandalf JSON
- [ ] Tag: `elrond/phase-E-2-DB-2026-05-23` (seam-prefix per ADR-001; local only)
- [ ] Append completion record to this dispatch per `dispatches/README.md`

## Acceptance criteria

- [ ] **All 125 labels updated.** Zero rows in `clusters` have `label LIKE 'PROVISIONAL:%'`
- [ ] **No row count change.** `SELECT COUNT(*) FROM clusters` = 125 before and after
- [ ] **Round-trip smoke PASS.** 50-100 row sample joined cleanly from `weapon_knowledge_entries` to `clusters` with canonical labels
- [ ] **MIGRATION.md amended** with UPDATE provenance + optional ALTER TABLE outcome + cross-seam declarations
- [ ] **Tag cut.** `elrond/phase-E-2-DB-2026-05-23` local
- [ ] **No DB push.** Local-only per ADR-006

## Out of scope

- **`cluster_membership` table changes.** Only `clusters.label` (and optionally `clusters.cluster_type`) UPDATE in this dispatch. The `cluster_membership.assignment_method` column added by legolas Phase E-1 is unchanged.
- **`weapon_knowledge_entries.cluster_id` changes.** Read-only join target.
- **Cluster algorithm re-fire.** This is a label-content UPDATE only; no clustering changes.
- **Sub-carries 9.11-C / 9.11-D / 9.11-E** (curation gap; substrate-tagging artifacts; cultural-vs-geographic discipline). These are separate elrond dispatches; do NOT touch substrate cleaning in this dispatch.
- **Sub-carry 9.11-A** (labeler bug fix). Separate legolas dispatch; you do not investigate `write_clusters_subsample` code in this dispatch.
- **Phase E-1.5 sensitivity sweep.** Deferred until 9.11-A lands.
- **DB push to origin.** Local-only per ADR-006.

## What knight-rider does after your return

1. Read completion record + MIGRATION.md amendment
2. Verify acceptance gates
3. **No additional Gate-2 needed** unless schema change (ALTER TABLE) introduced — in which case knight-rider invokes jack-ryan Pattern-A-light schema-validation check
4. Update CHANGELOG; mark sub-carry 9.10-A (Phase E-1) AND Phase E-2 cycle as CLOSED with the DB write complete
5. Phase E-2-DB completion paves the way for: Phase E-3/E-4 work (when defined); engine/loadout downstream consumers seeing canonical labels

## References

- **Gate-2 findings record:** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-output-gate-2-findings-record.md`
- Gandalf Phase E-2 JSON output: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`
- Gandalf Phase E-2 completion summary: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-completion-summary.md`
- Legolas Phase E-1 MIGRATION.md: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md`
- ADRs: ADR-001 (tag protocol), ADR-002 (tiered approval — additive schema column at sub-dispatch tier), ADR-004 (cross-seam MIGRATION.md), ADR-006 (DB-write requires explicit approval — this dispatch IS the approval)

---

## Tag at completion

```
elrond/phase-E-2-DB-2026-05-23
```

Seam-prefix per ADR-001. Local-only.

---

**Signed:** knight-rider, 2026-05-23 ~13:20 EDT post-Gate-2-PASS + gandalf spot-check relay. Pattern-A-light scope; mechanical UPDATE from reviewed JSON. Sub-dispatch authorization covers DB-write under ADR-006. Open design question on ALTER TABLE for cluster_type is yours; either decision is acceptable.

---

## Completion record

**Completed:** 2026-05-23 (elrond fire)
**Tag shipped:** `elrond/phase-E-2-DB-2026-05-23` (local; not pushed per ADR-006)
**MIGRATION.md written:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/MIGRATION.md` (new sibling; cross-references parent legolas Phase E-1 MIGRATION.md)
**Curation script:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/scripts/phase_e2_db_update.py`
**Run log:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/scripts/run-log-2026-05-23.txt`
**Pre-state audit trail:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/pre-update-state-clusters.tsv`
**Post-state audit trail:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/post-update-state-clusters.tsv`

### Acceptance gates

| Gate                                                                | Result |
|---|---|
| All 125 `clusters.label` updated; zero `PROVISIONAL:` remain         | PASS (count=0) |
| `SELECT COUNT(*) FROM clusters` = 125 unchanged                      | PASS |
| Spot-checks on dispatch-named clusters                              | PASS (db_ids 1/51/63/87/91 — note dispatch text used legolas `id` values 0/50/62/86/90; DB-side keys are `id + 1`) |
| Round-trip smoke 100-row sample (`weapon_knowledge_entries` JOIN `clusters`) | PASS (0 orphans, 0 NULL labels, 0 PROVISIONAL via join, 0 NULL cluster_type) |
| MIGRATION.md amended                                                 | PASS (new sibling) |
| Tag cut local                                                        | PASS |
| No DB push                                                           | PASS (local-only) |

### Design decision exercised: ALTER TABLE clusters ADD COLUMN cluster_type TEXT

**Decision:** YES — applied in this dispatch, single-transaction with the `label` UPDATE.

**Rationale:**
1. JSON carried `cluster_type` for all 125 rows already; deferring forces downstream consumers into dual-read (DB + sidecar JSON).
2. Additive-only schema change; ADR-002 sub-dispatch tier (no architectural-tier trigger).
3. Idempotent (catches `OperationalError: duplicate column name`).
4. Precedent: legolas Phase E-1 added `cluster_membership.assignment_method` under identical logic.
5. No `CHECK` constraint on the column — gandalf is authoritative on the open vocabulary (Discipline #14 spirit; future sensitivity-sweep labels can extend without schema migration).

**Domain populated:** 7 distinct `cluster_type` values across 125 rows:

| Value                            | N |
|---|---|
| weapon_family                    | 50 |
| named_template_family            | 41 |
| mixed_cross_cultural             | 18 |
| mixed_form_pool                  | 9 |
| modern_military_hardware_pool    | 4 |
| rare_lineage_isolate             | 2 |
| metadata_bucket                  | 1 |

### Anomaly surfaced (NOT a Phase E-2-DB defect — logged for downstream visibility)

Round-trip smoke included `weapon_knowledge_entries.id=3` "PMD series mines" assigned to `cluster_id=116` ("European Uncurated-Period Spear Family") — these are Soviet anti-personnel landmines, not spears. Substrate clustering artifact (`assignment_method=nearest_centroid`; distance-based, not density-based). Candidate diagnostic for the existing 9.11-C/D/E elrond curation-gap sub-carries or Phase E-1.5 sensitivity sweep. **No action taken in this dispatch.** Recorded in MIGRATION.md § 7 for knight-rider routing.

### Notes for knight-rider

- Schema change introduced (additive column `cluster_type`). Per dispatch § "What knight-rider does after your return" point 3: this MAY invoke jack-ryan Pattern-A-light schema-validation check. Schema is fully additive, idempotent, single-transaction, no CHECK constraint, no FK — minimum-surface change.
- Dispatch's spot-check expectations (cluster 50/62/86/90 → metadata/Abyssal Bane/Shotgun/East Asian Uncurated) **all match the actual labels at db_cluster_id+1** (legolas-id indexing in the dispatch text). I have flagged the off-by-one indexing in MIGRATION.md § 6 for clarity, but the labels themselves are exact matches.
- Parallel-fire deconfliction: I touched only `clusters.label` and `clusters.cluster_type` (new column). Legolas 9.11-A used a temp DB copy (no overlap). Gandalf 9.11-G was read-only (no overlap).
- Sub-carry **9.11-H** NOT needed — cluster_type column added in this pass, not deferred.
