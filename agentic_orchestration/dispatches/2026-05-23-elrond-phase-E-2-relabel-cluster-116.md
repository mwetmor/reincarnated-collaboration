# Dispatch — 2026-05-23 — elrond — Phase-E-2-relabel cluster_id=116 (follows gandalf 9.13-D Path 1 decision)

**From:** knight-rider
**To:** elrond (Pattern-A-light; single-row DB UPDATE under explicit DB-write authorization)
**Approved by:** Matt 2026-05-23 (per gandalf 9.13-D Path 1 decision commit `b5e13de`)
**Estimated effort:** ~15-30 minutes (read decision + execute UPDATE + smoke + MIGRATION.md amendment + tag)
**Gate-1:** SKIPPED. Single-row UPDATE per gandalf design-side decision; no methodology choices.
**Acceptance:** `clusters.id=116` has `label = 'European Uncurated-Period Mixed Military Hardware Pool'` (replaces incorrect "European Uncurated-Period Spear Family"); row count unchanged at 125; round-trip smoke PASS; MIGRATION.md amendment; tag cut.

---

## Why this dispatch exists

Gandalf resolved sub-carry 9.13-D (cluster-116 relabel-or-defer open-thread) at commit `b5e13de` by choosing **Path 1 (targeted relabel now)**. The current label in production DB is "European Uncurated-Period Spear Family" but the cluster contains PMD landmines + Round shield + M111 grenade + GYATA-64 mines — a mixed military hardware pool, NOT a spear family. The label was identified as a labeling-pipeline artifact (not a clustering error) by jack-ryan Gate-2 Finding 7 on Phase E-1.5 + reframed in Cycle 9.13 closeout.

Per gandalf 9.13-D decision: targeted relabel of the single cluster fixes the documentation accuracy issue without waiting for 9.11-D substrate-tagging-discipline work.

## Required reading before starting

1. **`agentic_orchestration/gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md`** — original surface from knight-rider; two-path framing
2. **Gandalf 9.13-D decision commit** `b5e13de` (collaboration repo) — Path 1 chosen; proposed canonical label "European Uncurated-Period Mixed Military Hardware Pool"
3. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`** — cluster_id=116 entry (legolas `id=115`; `db_cluster_id=116`); original gandalf canonical label + reps
4. **`agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/MIGRATION.md`** — Phase E-2-DB UPDATE provenance (cycle reference)
5. **Engineering disciplines updates (jack-ryan canonical write `1fae3fa`):** specifically Discipline #20 (density-based row-duplication prohibition; not directly relevant here but newly canonical); Discipline #1.1 (resource-bounds projection; not relevant for single-row UPDATE); Discipline #19.1 (cheapest-refuting-test per claim type — for the round-trip smoke verification)

## Locked decisions (not re-litigated)

- **New canonical label:** `'European Uncurated-Period Mixed Military Hardware Pool'` (gandalf-authored; do NOT alter)
- **Target row:** `clusters.id=116` (DB primary key; matches gandalf JSON `db_cluster_id=116` / legolas `id=115`)
- **Source DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
- **No cluster_type change** unless you observe the existing `cluster_type` on this row is `metadata_bucket` (Cluster 90 framing) when it should not be — verify before changing; gandalf 9.13-D decision did not specify cluster_type change

## Scope

- [ ] Read the gandalf 9.13-D decision file + open-thread surface + Phase E-2-DB MIGRATION.md
- [ ] Pre-UPDATE state capture (audit trail): `SELECT id, label, cluster_type FROM clusters WHERE id = 116;`
- [ ] Execute UPDATE:
  ```sql
  BEGIN;
  UPDATE clusters
    SET label = 'European Uncurated-Period Mixed Military Hardware Pool'
    WHERE id = 116;
  COMMIT;
  ```
- [ ] Verification queries:
  ```sql
  -- 1. Row exists with new label
  SELECT id, label, cluster_type FROM clusters WHERE id = 116;
  -- expected: label = 'European Uncurated-Period Mixed Military Hardware Pool'
  
  -- 2. Row count unchanged at 125
  SELECT COUNT(*) FROM clusters;
  -- expected: 125
  
  -- 3. No PROVISIONAL labels (Phase E-2-DB acceptance preserved)
  SELECT COUNT(*) FROM clusters WHERE label LIKE 'PROVISIONAL:%';
  -- expected: 0
  
  -- 4. Cluster membership join still clean for cluster 116
  SELECT COUNT(*) FROM cluster_membership WHERE cluster_id = 116;
  -- expected: ~10,087 (same as Phase E-2-DB; mcs-invariant per Phase E-1.5)
  
  -- 5. Sample row check: PMD landmines weapon_knowledge_entries.id=3
  SELECT wke.id, wke.canonical_name, c.label
    FROM weapon_knowledge_entries wke
    JOIN cluster_membership cm ON wke.id = cm.weapon_knowledge_entry_id
    JOIN clusters c ON cm.cluster_id = c.id
    WHERE wke.id = 3;
  -- expected: c.label = 'European Uncurated-Period Mixed Military Hardware Pool'
  ```
- [ ] Round-trip smoke: 10-row sample from `cluster_membership WHERE cluster_id = 116`; join to `weapon_knowledge_entries`; verify all 10 see the new label via join
- [ ] Write MIGRATION.md amendment (append to `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/MIGRATION.md` OR new sibling at `agentic_orchestration/elrond/research/phase-E-2-relabel-cluster-116-2026-05-23/MIGRATION.md` per your preference):
  - UPDATE pass executed (1 row)
  - Pre-state captured (audit trail)
  - Cross-seam impact: Phase E-3/E-4 + engine/loadout consumers see corrected label on next read
  - ADR-004 + Discipline #8 compliance: round-trip smoke result; provenance to gandalf 9.13-D decision commit `b5e13de`
  - Cross-reference to gandalf open-thread + 9.13-D decision
- [ ] Tag: `elrond/phase-E-2-relabel-cluster-116-2026-05-23` (seam-prefix per ADR-001; local only)
- [ ] Append completion record to this dispatch per `dispatches/README.md`
- [ ] Commit your work to git

## Acceptance criteria

- [ ] **Single row updated** — `clusters.id=116` has new canonical label
- [ ] **Original label superseded** — "European Uncurated-Period Spear Family" no longer present in production DB
- [ ] **Row count unchanged** — `SELECT COUNT(*) FROM clusters` = 125 before and after
- [ ] **Phase E-2-DB acceptance preserved** — zero PROVISIONAL labels (Phase E-2-DB Cycle 9.12 invariant holds)
- [ ] **Round-trip smoke PASS** — 10-row sample joined cleanly with new label
- [ ] **MIGRATION.md amended** with audit trail + cross-references
- [ ] **Tag cut** — local only

## Out of scope

- **Other cluster relabels** — only cluster_id=116 in this dispatch
- **Substrate cleaning / re-tagging** — 9.11-D + 9.11-E + 9.11-C are separate elrond dispatches; do NOT touch substrate in this dispatch
- **Cluster_type column change** unless current value is verified inconsistent — gandalf 9.13-D did not specify
- **Re-clustering** — Phase E-2 labels stand; this is a single label correction
- **DB push to origin** — local-only per ADR-006

## What knight-rider does after your return

1. Read completion record + MIGRATION.md amendment
2. Verify acceptance gates
3. Update CHANGELOG entry — note 9.14-B CLOSED + 9.13-D fully resolved (decision + execution both landed)
4. **No Gate-2 invocation needed** — single-row UPDATE per gandalf design-side decision; mechanical execution

## References

- **Gandalf 9.13-D decision commit:** `b5e13de` (collaboration repo)
- **Original open-thread:** `agentic_orchestration/gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md`
- **Phase E-2-DB UPDATE provenance:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/MIGRATION.md`
- **Phase E-1.5 Gate-2 Finding 7 (anomaly surfacing):** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-5-output-gate-2-findings-record.md`
- **Engineering disciplines canonical (jack-ryan commit `1fae3fa`):** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- ADRs: ADR-001 (tag protocol), ADR-004 (cross-seam MIGRATION.md), ADR-006 (DB write requires explicit approval — this dispatch IS the approval; sub-dispatch tier)

---

## Tag at completion

```
elrond/phase-E-2-relabel-cluster-116-2026-05-23
```

Seam-prefix per ADR-001. Local-only.

---

**Signed:** knight-rider, 2026-05-23 post-gandalf-9.13-D-Path-1-decision. Pattern-A-light scope; mechanical single-row UPDATE per design-side ruling.

---

## Completion record — elrond — 2026-05-23

**Status:** CLOSED — all acceptance criteria PASS.

**What landed:**
- Single-row UPDATE on `clusters.id=116` executed in transaction at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
- Pre-state captured: `'European Uncurated-Period Spear Family'` / `weapon_family`
- Post-state confirmed: `'European Uncurated-Period Mixed Military Hardware Pool'` / `weapon_family`
- All 5 verification queries PASS (V1 label updated; V2 row count=125 unchanged; V3 PROVISIONAL labels=0; V4 cluster_membership join clean=1335 rows for cluster 116; V5 PMD landmines see new label via join)
- Round-trip smoke 10/10 PASS (10-row sample from `cluster_membership WHERE cluster_id=116` joined to `weapon_knowledge_entries` and `clusters` all see new label)
- `cluster_type` deliberately unchanged (gandalf 9.13-D did not specify; current value `weapon_family` consistent pending 9.11-D substrate-tagging work)
- MIGRATION.md written at `agentic_orchestration/elrond/research/phase-E-2-relabel-cluster-116-2026-05-23/MIGRATION.md` (new sibling per dispatch preference; cleaner provenance scope than appending to E-2-DB MIGRATION.md)
- Pre/post state TSV files captured at `pre-update-state-cluster-116.tsv` + `post-update-state-cluster-116.tsv`
- Tag cut local: `elrond/phase-E-2-relabel-cluster-116-2026-05-23`
- Local commit landed

**Anomaly:** Dispatch § Scope V4 estimated cluster_membership count "~10,087" — observed count is 1335 for cluster 116. The dispatch estimate appears to have been the wrong scope (total cluster_membership across all 125 clusters is 48,430, not 10,087 either). Cluster 116 membership row count is invariant pre/post relabel; smoke gate PASS regardless of the estimate-vs-actual mismatch. Surfacing for knight-rider records.

**Cross-seam impact summary:** Gandalf 9.11-D + 9.11-E + 9.11-C, star-lord telemetry joins, drax loadout UI, legolas Phase E-1.5 (when fired) — all consume corrected label on next DB read. Open-thread `agentic_orchestration/gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md` may be archived (gandalf's call).

**Signed:** elrond, 2026-05-23 post-9.14-B-execution.
