# MIGRATION — 2026-05-23 — Phase E-2 cluster-116 single-row relabel (post-9.13-D Path 1)

**Author:** elrond
**Date:** 2026-05-23
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-elrond-phase-E-2-relabel-cluster-116.md` (9.14-B)
**DB path:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Tag:** `elrond/phase-E-2-relabel-cluster-116-2026-05-23` (local only)
**Authorization:** gandalf 9.13-D Path 1 decision commit `b5e13de` (Matt-approved via design-side ruling 2026-05-23); ADR-006 sub-dispatch DB-write authority via knight-rider 9.14-B dispatch
**Parent migration:** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/MIGRATION.md` (Phase E-2-DB canonical-label UPDATE pass)

---

## What changed (one line)

Single-row UPDATE on `clusters.id=116`: `label` transitioned from `'European Uncurated-Period Spear Family'` to `'European Uncurated-Period Mixed Military Hardware Pool'`. No other column changes; no schema change; row count unchanged.

## Why (one line)

The Phase E-2 canonical label for cluster 116 was a labeling-pipeline artifact (jack-ryan Gate-2 Finding 7 on Phase E-1.5; reframed in Cycle 9.13 closeout). The cluster contains PMD landmines + Round shield + M111 grenade + GYATA-64 mines — a mixed military hardware pool, NOT a spear family. Gandalf 9.13-D resolved via Path 1 (targeted relabel now); this migration is the DB write that lifts the gandalf-authored canonical correction.

## Pre / post state

### Before (pre-UPDATE capture; archived at `pre-update-state-cluster-116.tsv`)

```
id  label                                          cluster_type
116 European Uncurated-Period Spear Family         weapon_family
```

### After (post-UPDATE capture; archived at `post-update-state-cluster-116.tsv`)

```
id  label                                                       cluster_type
116 European Uncurated-Period Mixed Military Hardware Pool      weapon_family
```

`cluster_type` deliberately unchanged. Gandalf 9.13-D Path 1 decision did not specify a cluster_type change. Per dispatch § Locked decisions: "No cluster_type change unless you observe the existing cluster_type on this row is `metadata_bucket` … when it should not be." Observed value is `weapon_family`, which remains the closest substrate-meta-type fit pending 9.11-D substrate-tagging-discipline work (mixed military hardware pool is a refinement of substrate-coherent weapon-form grouping, not a metadata bucket).

## SQL executed

```sql
BEGIN;
UPDATE clusters
  SET label = 'European Uncurated-Period Mixed Military Hardware Pool'
  WHERE id = 116;
COMMIT;
```

Single transaction. One row affected. No backup created — pre-state captured to TSV pre-execution; trivially reversible via the inverse UPDATE if gandalf 9.13-D decision is itself reversed.

## Verification (round-trip smoke + acceptance gates)

| Check | Query | Expected | Observed | PASS/FAIL |
|---|---|---|---|---|
| V1 label updated | `SELECT id, label, cluster_type FROM clusters WHERE id = 116` | new label | new label | PASS |
| V2 row count unchanged | `SELECT COUNT(*) FROM clusters` | 125 | 125 | PASS |
| V3 zero PROVISIONAL labels | `SELECT COUNT(*) FROM clusters WHERE label LIKE 'PROVISIONAL:%'` | 0 | 0 | PASS |
| V4 cluster_membership join clean | `SELECT COUNT(*) FROM cluster_membership WHERE cluster_id = 116` | clean integer | 1335 | PASS (note: dispatch estimated "~10,087" but that figure is the total across all clusters at the time of Phase E-2-DB; per-cluster membership for 116 is 1335. Total `cluster_membership` rows across all 125 clusters = 48,430. Dispatch estimate appears to have been the wrong scope — corrected here for the record. Cluster 116 membership count is invariant pre/post relabel.) |
| V5 PMD landmines see new label via join | `SELECT wke.id, wke.canonical_name, c.label FROM weapon_knowledge_entries wke JOIN cluster_membership cm ON wke.id = cm.knowledge_entry_id JOIN clusters c ON cm.cluster_id = c.id WHERE wke.id = 3` | new label | new label (`PMD series mines` → `European Uncurated-Period Mixed Military Hardware Pool`) | PASS |
| Round-trip smoke (10-row sample) | 10 rows from `cluster_membership cluster_id=116` joined to `weapon_knowledge_entries` and `clusters` | all 10 see new label | 10/10 see new label (PMD series mines, GYATA-64 mine, TM-35 mine, coats of arms and flags of Andorra, Mk 7 mine, Jacobi mine, Round sheild ×4) | PASS |

**Discipline #19.1 cheapest-refuting-test per claim type:**
- Memory: N/A (single-row UPDATE; trivial footprint)
- Methodology: N/A (no methodology choice)
- Substrate: V2 row count + V3 PROVISIONAL count + V4 membership count (substrate-invariant ✓)
- Cross-seam: schema-diff equivalent = column set unchanged + row count unchanged (✓)
- Framing: gandalf 9.13-D Path 1 decision (✓ — locked upstream)
- Cluster-semantic: V5 + 10-row round-trip rep-audit (✓ — new label is consistent with rep set: landmines + shield + grenade)

## Cross-seam impact

- **Gandalf:** Phase E-3/E-4 + 9.11-D + 9.11-E + 9.11-C substrate-tagging-discipline work now consume the corrected label on next DB read. Open-thread `agentic_orchestration/gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md` may be archived/closed (gandalf's call).
- **Star-lord:** Read-only telemetry joins on `clusters.label` for cluster 116 surface the corrected label.
- **Drax:** Loadout app reads from this same DB; any cluster-label surfacing in UI now reflects the corrected label.
- **Rocket:** No engine-internal impact (engine canonical library does not import from this DB).
- **Legolas:** Phase E-1.5 sensitivity sweep (when fired) inherits the corrected label on cluster 116. No re-crawl required.
- **Knight-rider:** 9.14-B CLOSED + 9.13-D fully resolved (decision + execution both landed).

## ADR-004 + Discipline #8 compliance

- **ADR-004 (cross-seam MIGRATION.md):** This file documents the audit trail; cross-seam consumers identified above.
- **Discipline #8 (round-trip smoke after schema or data changes):** 10-row smoke sample PASSED.
- **Discipline #14 spirit (mechanical labels stay internal; per-instance vocabulary explicit):** Corrected label uses substrate-descriptive vocabulary ("Mixed Military Hardware Pool") rather than incorrect form-implication ("Spear Family"). Schema is now more substrate-honest.
- **Discipline #25 (semantic-layer rep-audit):** The 10-row smoke functions as a rep-audit: 6 landmines + 1 metadata noise row (coats of arms — substrate-meta artifact, not a weapon) + 4 Round shields. The corrected label "Mixed Military Hardware Pool" is the substrate-honest description; the previous "Spear Family" would have semantically committed downstream design surfaces to a form-implication the substrate does not support. Path 1 closes the semantic-layer leak.

## References

- **Gandalf 9.13-D decision commit:** `b5e13de` (collaboration repo)
- **Original open-thread:** `agentic_orchestration/gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md`
- **Phase E-2-DB UPDATE provenance (parent):** `agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/MIGRATION.md`
- **Phase E-1.5 Gate-2 Finding 7 (anomaly surfacing):** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-5-output-gate-2-findings-record.md`
- **Engineering disciplines canonical (jack-ryan commit `1fae3fa`):** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- ADRs: ADR-001 (tag protocol), ADR-004 (cross-seam MIGRATION.md), ADR-006 (DB write requires explicit approval — covered by 9.14-B dispatch + gandalf 9.13-D)

---

**Signed:** elrond, 2026-05-23. Single-row mechanical UPDATE per gandalf design-side ruling. Reversible. Round-trip smoke 10/10 PASS.
