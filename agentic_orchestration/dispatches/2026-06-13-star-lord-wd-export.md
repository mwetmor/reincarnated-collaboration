# Dispatch — 2026-06-13 — star-lord — W-D export-side: consume the commit-grade BC emit

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-06-13 (D1–D6 dispositions — "author the W-D-export dispatch per your plan").
**Status:** GATE-1 PENDING (jack-ryan DESIGN-MODE). **GATED — do NOT start** until gamora's `simulation/MIGRATION.md` v1.31 emit-contract section is on disk AND you have read the D1-decompose caveat below.
**Estimated effort:** ~hours (consume-side wiring + one schema-migration check).

## Context

This is the export-side half of W-D, following the **W-B split pattern** (your `star-lord/v-wb-typewall-export-1` precedent). gamora's W-D build (engine `5ec33bb`) now MINTS a production `CommitGradeVerdict` from spatial telemetry — the artifact your W-B `ExportCommitGradeVerdictDocument` + `admit_bc_for_identity` were typed for. The emit contract (8 axis fields + 4 provenance markers, field-for-field) is in `simulation/MIGRATION.md` **v1.31**. You wire the export side to consume it.

## CAVEAT — the bins are wired-not-yet-fully-discriminating (load-bearing)

cond.4 PASSED as a **gate-read** (wired-not-default + mint), but **per Matt's D1 hard constraint, that does NOT mean "the archive measures the kit."** §6.4 ("measures the current kit = measured fact") stays OPEN and closes only at W-F. Several axes are wired-but-not-discriminating pending the D1 per-axis decompose (Axis-2A deferred to the proxy-port; Resource/Control wired-but-reference-set-undifferentiated; Defensive discriminates only in the W-F boss room; mobility lock-edge re-calibration pending). **Therefore: the W-D export must NOT stamp or advertise the consumed BC as "measures the kit" / behavioral-identity-certified.** It is a commit-grade *provenance* artifact (fidelity=commit, engine=spatial) whose **discrimination is not yet certified.** Keep the admission semantics as provenance-grade, not identity-truth, until §6.4 closes at W-F.

## Required reading before starting

- `simulation/MIGRATION.md` v1.31 (gamora's emit contract — reconcile field-for-field; if not on disk when you start, HALT and tell KR)
- Your own W-B export types: `ExportCommitGradeVerdictDocument`, `admit_bc_for_identity` (`star-lord/v-wb-typewall-export-1`, engine `a89f21a`)
- `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md` (D1 hard constraint, §6.4 open)
- gamora W-D math note: `reincarnated-engine/src/reincarnated/simulation/math/wd-six-axis-measure-build-2026-06-13.md` (§10 — what discriminates vs what's deferred)

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring)

**YES.** consume the gamora→star-lord commit-grade BC emit (the v1.31 contract). Round-trip smoke required (Principle 6): take a real spatial-emitted `CommitGradeVerdict` through your export consume boundary and assert (a) it is admitted as commit-grade provenance, AND (b) it is NOT advertised as identity-certified/measures-the-kit (the §6.4-open semantics).

## Scope

- [ ] Consume gamora's v1.31 commit-grade BC emit field-for-field into the export path (reconcile provenance markers + 8 axis fields to your `ExportCommitGradeVerdictDocument`)
- [ ] Preserve the §6.4-open semantics — provenance-grade admission, NOT identity-truth advertisement (CAVEAT above)
- [ ] **INFO (jack-ryan Gate-2 flag):** `spatial_fight_results.total_displacement` additive column (float, default 0.0) needs a **non-breaking** schema migration IF the export DB persists spatial results — enumerate, document, apply the additive migration (additive-only; no destructive change)
- [ ] MIGRATION.md consume-side section reconciling to gamora's v1.31 emit contract
- [ ] Round-trip smoke per Principle 6 (above)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `star-lord/v-wd-export-1`

## Out of scope

- **The 1D `bc_measured_bins.json` search-grade path** — already done in W-B; untouched here.
- **Stamping the BC as "measures the kit"** — forbidden until §6.4 closes at W-F (CAVEAT).
- **Production telemetry.db apply** — Matt's ADR-006 gate (telemetry v2.17 still pending); do not apply.
- **Pushing to remote** — Matt's wave-close gate; accumulate commits.

## References

- W-D close + D1 hard constraint: `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md`
- W-B split precedent: `dispatches/2026-06-13-star-lord-wb-typewall-export.md`
- Gate-2: jack-ryan gates the consume boundary + round-trip + the additive migration.

---

**Author:** knight-rider, 2026-06-13. Export-side consume of the W-D commit-grade mint, with the §6.4-open discrimination caveat enforced so provenance-grade is not mistaken for identity-truth.
