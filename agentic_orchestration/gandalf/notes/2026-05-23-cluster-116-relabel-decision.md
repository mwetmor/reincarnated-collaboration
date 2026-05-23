# Cluster 116 Relabel Decision — Path 1 (Targeted Relabel Now)

> **STATUS:** RESOLVED 2026-05-23 — gandalf Pattern A-light decision on open-thread `gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md`. Routes to knight-rider for elrond Phase-E-2-relabel sub-dispatch.

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct instruction to handle cluster-116 surface in current session
**Status:** Decision artifact. Closes the 9.13-D open-thread.

---

## 1. Decision: Path 1 — Targeted relabel now

Per open-thread `gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md`, two paths surfaced:

- **Path 1 — Targeted relabel now (lower-cost):** author corrected canonical label; knight-rider sub-dispatches elrond UPDATE single row; ~30 min total cost
- **Path 2 — Defer to 9.11-D (status-quo):** zero cost now; production DB continues to carry inaccurate label during 9.11-D wait (days-to-weeks per open-thread)

**Decision: Path 1.**

## 2. Reasoning

**Four reasons favor Path 1 over Path 2:**

1. **The label is empirically inaccurate NOW.** Cluster 116 carries PMD landmines + Round shield + M111 grenade + GYATA-64 mine as members; the current label "European Uncurated-Period Spear Family" does not reflect content. Per Discipline #11 (empirical-inspection over assumption), honest documentation is a baseline discipline value. Letting an inaccurate label sit in production DB violates this without compensating benefit.

2. **The "sunk investment" risk is small.** Path 1's investment IS the relabel work itself. If 9.11-D substrate-tagging-discipline work later triggers a re-cluster pass and Cluster 116 dissolves or reforms, the relabel work isn't "sunk" — it gets superseded by a NEW relabel pass against the new cluster taxonomy. That's normal substrate-led cluster-labeling work, not duplicated effort.

3. **Semantic-layer rep-audit discipline (per gandalf OP § 4.4 + hive-mind protocol § 7.4) wants downstream consumers to rep-audit, but the FIRST line of defense is label accuracy at the source.** If the label is wrong at the source, every downstream consumer must apply rep-audit to catch it; if the label is honest, downstream consumers can use the label as starting context without re-deriving. Path 1 reduces downstream rep-audit load proportionally.

4. **The 9.11-D timeline is "days-to-weeks" per open-thread.** During that interim window, downstream consumers (cohesion-judge calibration at P5; T4-B catalogue authoring scaffolding consumers; any LLM-consumer of cluster labels) would see "Spear Family" for a cluster containing landmines. Path 1 closes the misinformation window proactively.

## 3. Proposed corrected label

**Current label (inaccurate):** "European Uncurated-Period Spear Family"

**Proposed corrected label:** `"European Uncurated-Period Mixed Military Hardware Pool"`

**Reasoning for label choice:**

- **"European"** — preserved from original; lineage_canonical tag holds at substrate level
- **"Uncurated-Period"** — preserved from original; period_canonical = uncurated; Phase E-1.5 sensitivity sweep confirms this tag is structural at all mcs variants. Per § 4.3 flag enum, `lineage_uncurated` applies; per period flag, `period_tag_likely_metadata_artifact` applies
- **"Mixed Military Hardware"** — substrate-honest content interpretation; reps span mines + shield + grenade + APC + similar mid-modern military equipment categories. Replaces "Spear Family" which was the labeling-pipeline-bug artifact
- **"Pool"** — signals heterogeneity per `mixed_form_within_cluster` flag; consistent with naming convention for cross-form clusters in Phase E-2 label set (e.g., Cluster 0 "Cross-Cultural Contemporary Mixed-Form Pool", Cluster 63 "European Industrial Decorative/Mixed-Form Pool")

**Special-case flags to update:**

| Flag | Status |
|---|---|
| `provisional_description_overridden` | YES — was already set during Phase E-2 spot-check; remains set |
| `mixed_form_within_cluster` | YES — was set during Phase E-2; remains set |
| `modern_military_hardware` | ADD — wasn't in original; reps confirm |
| `lineage_uncurated` | YES — was already set; remains |
| `period_tag_likely_metadata_artifact` | YES — was set; remains |
| `labeling_pipeline_bug_surfaced` | ADD — surfaces the bug case for documentation |
| `phase_d_bis_curation_gap` | YES — was set; remains |

(Cluster 116's original Phase E-2 flag set per `phase-E-2-cluster-labels.md` line ~1455: `provisional_description_overridden`. Additional flags above derive from Cluster 116's current empirical content + § 4.3 enum.)

## 4. Routing for execution

**Knight-rider sub-dispatch scope:**

```
Phase E-2-relabel sub-dispatch — Cluster 116 label correction (gandalf 9.13-D resolved)

Target seam: elrond
Scope: UPDATE single row in clusters table where id=116
  - SET clusters.label = 'European Uncurated-Period Mixed Military Hardware Pool'
  - SET clusters.special_case_flags = [add 'modern_military_hardware' + 
    'labeling_pipeline_bug_surfaced' to existing flag set]
  - Update Phase-E-2-DB MIGRATION.md provenance note
  - Smoke: SELECT label, special_case_flags FROM clusters WHERE id=116
  - Commit + push

Cross-references:
  - Decision artifact: gandalf/notes/2026-05-23-cluster-116-relabel-decision.md
  - Open-thread (now closed): gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md
  - Original Phase E-2 entry: phase-E-2-cluster-labels.md Cluster 116
  - Phase E-2-DB elrond commit c08ceee (provenance)
```

**Estimated effort:** ~15 min elrond UPDATE + smoke + provenance update + commit. Single-transaction atomic operation.

## 5. Post-relabel state

After the relabel UPDATE lands:

- `clusters` table row id=116 carries correct label
- `phase-E-2-cluster-labels.md` source-of-truth file remains UNCHANGED (it captured Phase E-2 state at that moment; the DB-side correction is a post-Phase-E-2 amendment per Phase-E-2-DB elrond UPDATE pattern)
- Open-thread `gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md` can be moved to closed status (or stays as historical record)
- 9.13-D sub-carry CLOSED
- 9.13-A PMD landmines anomaly: SUBSUMED by this relabel (label-fix path chosen per the open-thread's "9.13-A → either subsumed by 9.13-D (label-fix) OR persists to 9.11-D (substrate-fix)" framing). 9.13-A no longer requires separate action — though 9.11-D substrate-tagging-discipline work remains separately scoped per its own cross-cutting application

## 6. What this decision does NOT do

- Does NOT change Cluster 116's substrate placement (which is empirically correct per Phase E-1.5 mcs-invariance)
- Does NOT address the underlying substrate-tagging-discipline issue at scale (9.11-D / 9.11-E remain scoped separately)
- Does NOT modify the source-of-truth Phase-E-2 cluster-labels.md file (that file captures Phase E-2 state at authoring; DB-side amendments are tracked via Phase-E-2-DB MIGRATION.md)
- Does NOT pre-commit to label staying at this value if 9.11-D re-cluster pass triggers cluster dissolution

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct instruction to handle in current session (Pattern A-light decision)
**Path chosen:** Path 1 — targeted relabel now
**Routing:** Via Matt to knight-rider for elrond Phase-E-2-relabel sub-dispatch authoring
**Companion artifact:** `gandalf/open-threads/2026-05-23-cluster-116-relabel-or-defer-surface.md` (now CLOSED via this decision)

---

**Signed:** gandalf
**For:** closing the 9.13-D open-thread with Path 1 decision + proposed corrected label + routing scope for knight-rider sub-dispatch authoring.
