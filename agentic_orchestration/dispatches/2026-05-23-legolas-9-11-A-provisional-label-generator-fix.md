# Dispatch — 2026-05-23 — legolas — 9.11-A provisional-label-generator bug fix (sequencing-load-bearing before Phase E-1.5)

**From:** knight-rider
**To:** legolas (Pattern-A-light; code investigation + fix + verification; you own `phase_e1_pipeline.py write_clusters_subsample`)
**Approved by:** Matt 2026-05-23 ~13:15 EDT (per gandalf design-side spot-check relay escalating 9.11-A priority)
**Estimated effort:** ~45-90 minutes (locate bug in `write_clusters_subsample` + fix + verify by re-running subsample mode + comparison check on a handful of clusters)
**Sequencing:** **LOAD-BEARING.** This dispatch must complete BEFORE Phase E-1.5 sensitivity sweep fires. Per gandalf spot-check: if E-1.5 re-fires with the broken labeler, all new clusters need ~37.6%+ human-override pass — wastes the labeling work.
**Gate-1:** SKIPPED. Code bug fix in your own seam; no methodology choices.
**Acceptance:** New provisional descriptions emitted by `write_clusters_subsample` correctly reflect cluster rep evidence on a sample of the 47 originally-overridden clusters (≥90% alignment with gandalf's overrides); pipeline test re-fire of subsample mode produces clean output; tag cut.

---

## Why this dispatch exists

Gandalf Phase E-2 cluster labeling work uncovered that the provisional-label-generator in `phase_e1_pipeline.py write_clusters_subsample` (legolas-authored function from your Phase E-1 frame-revision pipeline addition) generates token-pairs ungrounded in actual rep content. **47 of 125 clusters required human-override** during Phase E-2 — far above the 5-15 the dispatch predicted.

Per gandalf spot-check relay (`gate-2-findings-record` § 4.2):

> The bug isn't 5-15 edge cases — it's systemic random token-pair generation. Examples from spot-check:
> - Cluster 0: provisional "staff/axe"; reps are revolver/kukri/wakizashi
> - Cluster 9: provisional "dagger/wand"; reps are all javelins
> - Cluster 23: provisional "lance/rifle"; reps are SPH + MANPADS systems
> - Cluster 53: provisional "bow/hammer"; reps are bow + glaive + halberd
>
> The generator appears to produce token-pairs ungrounded in actual rep content.

Without this fix, Phase E-1.5 sensitivity sweep (which re-fires the subsample pipeline at multiple `min_cluster_size` values) would produce new clusters with the same broken provisional descriptions, requiring gandalf to do another labor-intensive human-override pass on each sweep variant. Fixing the labeler now preserves the value of Phase E-1.5.

## Required reading before starting

1. **`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-output-gate-2-findings-record.md`** § 4.2 — gandalf's spot-check finding + sequencing escalation
2. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-completion-summary.md`** § Override Count + Listing — gandalf's 47-override category breakdown
3. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`** — the 47 clusters with `provisional_description_overridden: true` field; `override_reason` field shows what gandalf observed for each
4. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/scripts/phase_e1_pipeline.py`** `write_clusters_subsample` function — the bug locus

## Math-before-code (for the fix design)

### § 1. Diagnose the bug

Per gandalf's evidence, the generator emits token-pairs like `staff/axe`, `dagger/wand`, `lance/rifle`, `bow/hammer` that are NOT supported by rep content. Hypothesis: the function picks top-K weapon_type tokens from a sparse/partial weapon_type column, possibly with insufficient grounding in actual rep canonical_name evidence.

**Before fixing, document in math-note what the bug actually is.** Read `write_clusters_subsample` end-to-end; trace how it derives the weapon-type portion of the provisional description; identify the exact line(s) that produce ungrounded token-pairs. Math-note at `phase-E-pattern-6-2026-05-23/9-11-A-labeler-bug-math-note.md` documents:

1. **What the function does (verbatim):** quote the relevant code lines with line numbers
2. **What goes wrong:** trace one or two of gandalf's example clusters (Cluster 0, 9, 23, or 53) through the function logic; show why the ungrounded token-pair emerges
3. **Root cause classification:** is it (a) the wrong data source (e.g., the function reads `structured_properties.weapon_type` field which is sparse/noisy), (b) the wrong aggregation (e.g., picks two random tokens rather than the dominant), (c) ungrounded token-pair concatenation (combines tokens that don't co-occur in reps), or (d) something else?
4. **Fix approach:** state the fix in math-note form before writing code. Two viable approaches:
   - **Approach A — rep-canonical-name-grounded:** derive the weapon-form description from regex matches against rep canonical_names (matching the existing 30-weapon-type pattern from features.md), then take the highest-frequency match across the top-K hdbscan_native reps
   - **Approach B — structural-only:** strip weapon-form claims entirely; emit provisional descriptions as `PROVISIONAL: <lineage> <period> <register>; <kind>; N=<count>` without a weapon-form guess. Downstream labelers know to derive weapon-form from rep evidence themselves.
   - Recommend **Approach A** if the rep-canonical-name evidence is reliable (lower-friction for downstream readers); **Approach B** if rep-canonical-name evidence is itself sparse or unreliable. Pick one with reasoning.

### § 2. Verification plan

Before firing the fix, name the cheapest refuting test per Discipline #19 (forensic-conclusion-discipline):

> **Cheapest refuting test for the bug fix:** re-fire the subsample pipeline in `--mode subsample-k3` with the fix applied; compare new provisional descriptions for the 47 originally-overridden clusters against gandalf's `override_reason` field in the JSON. If ≥90% of the new provisional descriptions match the form gandalf overrode TO (within rep-evidence semantic equivalence), the fix works. If <90%, the fix is incomplete; iterate.

### § 3. Idempotency check

Confirm that running the fixed `write_clusters_subsample` produces deterministic output (no random component that would make verification flaky). HDBSCAN itself is reproducible via `random_state=42`; the provisional-description generator should be similarly deterministic. If you find randomness in the generator that contributes to the bug, document it.

## Scope

- [ ] Read gandalf's 47-override JSON entries (focus on `original_provisional` + `override_reason` fields)
- [ ] Locate `write_clusters_subsample` in `phase_e1_pipeline.py`; trace the provisional-description-generation path
- [ ] Author math-note at `phase-E-pattern-6-2026-05-23/9-11-A-labeler-bug-math-note.md` per § 1-§ 3 above
- [ ] Apply the fix to `phase_e1_pipeline.py write_clusters_subsample`
- [ ] **Verification re-fire:** `python scripts/phase_e1_pipeline.py --mode subsample-k3 --k_final 3 --min_cluster_size 10 --subsample_n 10000 2>&1 | tee scripts/full-run-log-2026-05-23-9-11-A-fix-verify.txt`
- [ ] **DO NOT commit the verification re-fire's DB writes as overrides.** Either (a) run verification against a temporary DB copy, OR (b) revert DB UPDATEs after verification (the existing `clusters.label` content from elrond Phase E-2-DB dispatch — when it lands — should not be clobbered by your verification fire). If elrond's Phase E-2-DB has NOT yet fired by the time you run, the verification re-fire's DB writes will just overwrite the legolas-Phase-E-1 provisional labels (acceptable; those are replaced anyway by elrond's UPDATE). Coordinate with knight-rider if unsure of fire sequence.
- [ ] Comparison check: for each of the 47 overridden clusters, compare new provisional description to gandalf's `override_reason`. Document alignment percentage in completion record.
- [ ] If alignment ≥ 90%: write completion summary + tag
- [ ] If alignment < 90%: iterate on fix; document iteration in math-note; re-verify
- [ ] Write `phase-E-pattern-6-2026-05-23/9-11-A-completion-summary.md` with:
  - Bug diagnosis (root cause + fix approach)
  - Sample-cluster verification (before/after on Clusters 0, 9, 23, 50, 53 at minimum)
  - Alignment percentage
  - Phase E-1.5 readiness declaration
- [ ] Tag: `legolas/9-11-A-provisional-label-generator-fix-2026-05-23` (seam-prefix per ADR-001; local only)
- [ ] Append completion record to this dispatch per `dispatches/README.md`

## Acceptance criteria

- [ ] **Bug diagnosis documented** in math-note with root cause classification + fix approach justification
- [ ] **Fix applied** to `phase_e1_pipeline.py write_clusters_subsample`
- [ ] **Verification re-fire executed** at `--mode subsample-k3` defaults
- [ ] **Comparison check ≥ 90% alignment** on the 47 overridden clusters (new provisional descriptions match gandalf's override-reason semantics)
- [ ] **No regression on non-overridden clusters** (the 78 clusters where gandalf accepted provisional as-is should still receive correct provisional descriptions under the fix)
- [ ] **DB state preserved or coordinated:** verification re-fire does not clobber elrond's Phase E-2-DB UPDATE (if that has fired) OR no clobber concern (if elrond's dispatch has not yet fired)
- [ ] **Phase E-1.5 readiness declared.** Completion summary says: "9.11-A fixed; Phase E-1.5 sensitivity sweep dispatch may now be authored + fired without re-introducing the labeler bug."

## Out of scope

- **Sub-carries 9.11-C / 9.11-D / 9.11-E / 9.11-G.** Substrate-tagging-artifact / curation-gap / marginal-lineage recognition work — separate dispatches.
- **Phase E-1.5 sensitivity sweep.** Knight-rider authors that AFTER your acceptance lands.
- **Cluster re-labeling.** Gandalf's Phase E-2 labels stand; you do NOT re-derive canonical labels in this dispatch.
- **DB-side schema changes.** Elrond Phase E-2-DB handles any DB structure changes; you do NOT touch schema.
- **The substrate itself.** Locked.
- **Phase E-3 / E-4 work.** Hand-off notes only if you surface anything relevant during diagnosis.

## What knight-rider does after your return

1. Read completion summary + math-note
2. Verify alignment percentage + Phase E-1.5 readiness declaration
3. **If ≥ 90% alignment:** author Phase E-1.5 sensitivity sweep dispatch (legolas Pattern-A-light or Pattern-B per scope) with 9.10-G.1 psutil-install preflight folded in
4. **If < 90% alignment AND fix is incomplete:** route back to you for iteration; do not author Phase E-1.5
5. Update sub-carry tracking; mark 9.11-A as CLOSED

## References

- **Gate-2 findings record:** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-output-gate-2-findings-record.md` § 4.2
- Gandalf JSON with override evidence: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`
- Gandalf completion summary § Override Count: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-completion-summary.md`
- Discipline #19 (forensic-conclusion-discipline) candidate: `agentic_orchestration/knight-rider/notes/2026-05-23-discipline-observations-for-jack-ryan.md` Observation 6
- ADRs: ADR-001 (tag protocol), ADR-006 (read-only external state default — DB writes in this dispatch are confined to verification scope; coordinate with elrond Phase E-2-DB if both dispatches fire close in time)

---

## Tag at completion

```
legolas/9-11-A-provisional-label-generator-fix-2026-05-23
```

Seam-prefix per ADR-001. Local-only.

---

**Signed:** knight-rider, 2026-05-23 ~13:20 EDT post-gandalf-spot-check-relay. 9.11-A escalated to load-bearing sequencing constraint (must land before Phase E-1.5). Code fix in your own seam; math-before-code discipline applied per Discipline #1; cheapest-refuting-test named per Discipline #19.
