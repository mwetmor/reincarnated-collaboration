# Dispatch — 2026-05-19 — gamora — VS2a R2 H1 re-validation under explicit `geometry_type` field

**From:** knight-rider
**To:** gamora (simulation seam — R2 sub-gauntlet re-run OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when F1 lands per gating
**Estimated effort:** ~1–3 days (sub-gauntlet re-run + analysis + disposition surface)
**Acceptance:** R2 H1 re-test produces variance metric under original ≥ 0.10 threshold; result documented at `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/R2-test1.md`. Tag fires: `vs2a/v0.2-r2-h1-revalidated`.
**Hive context:** VS2a hive ACTIVE; F1 (rocket+star-lord geometry_type schema) is the upstream gate. This dispatch is the **R2 disposition § 3.2 forward-routed re-test**.

---

## Context

Per R2 H1 disposition (`canonical/story/r2-h1-disposition-2026-05-19.md`):
- v0.14 fired under revised 4-sub-claim category-of-completion; sub-claim 3 (geometric signal exists at 28pp delta) PROVEN
- Original variance ≥ 0.10 threshold PRESERVED as VS2a re-test target
- Instrument limitation: name-heuristic 43/3/4 class distribution drove variance to 0.017 below threshold
- VS2a `geometry_type` per-skill schema field (F1) is the architectural pre-condition

When F1 ships:
- Catalogue has explicit `geometry_type` per skill (43/3/4 distribution becomes whatever the true geometry distribution actually is)
- `spatial_engine._determine_geometry_type()` reads explicit field instead of name-heuristic
- This dispatch re-runs R2 sub-gauntlet on the re-converged (or backfilled) 5-season catalogue under explicit classification
- Applies ORIGINAL H1 variance ≥ 0.10 threshold

Two possible outcomes:
1. **H1 PASS under corrected instrument** — variance ≥ 0.10 confirms spatial signal load-bearing as predicted (R2 architectural shift fully validated)
2. **H1 still FAIL under corrected instrument** — variance < 0.10 under explicit field surfaces a DEEPER FINDING (catalogue diversity may be the binding constraint; spatial substrate may need post-kit-redesign re-evaluation; potentially a separate disposition by gandalf)

---

## Required reading

In order:
1. `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.2 + § 4 (4-sub-claim PASS criteria + re-test gate)
2. F1 dispatch + completion record once F1 lands: `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-vs2a-geometry-type-schema.md`
3. F1 schema design doc once authored: `reincarnated-engine/design/working-agreement/F1-geometry-type-schema-design-2026-05-19.md`
4. R2 production sprint outputs: `reincarnated-engine/output/R2-sprint-2026-05-19/` (test1.md / test2.md / test3.md / summary.md)
5. `reincarnated-engine/src/reincarnated/simulation/spatial_engine.py` post-F1 (`_determine_geometry_type()` updated to direct-field-read)
6. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (your last checkpoint; post-R2 production graduation at engine `bb013b7`)
7. `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.1 re-test plan
8. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

- [ ] Verify F1 completion: explicit `geometry_type` field present on 51-class catalogue skills (backfill validated; rocket + star-lord acceptance criteria satisfied)
- [ ] Re-run R2 sub-gauntlet (all 51 classes × 3 scenarios × 30 fights) using updated `_determine_geometry_type()` direct-field-read
- [ ] Compute H1 metric: per-geometry-type mean WR + variance across geometry-type means
- [ ] Apply ORIGINAL H1 variance ≥ 0.10 threshold (NOT the revised category-of-completion frame; that was for v0.14; this is the post-F1 re-test under original criterion)
- [ ] H2 + H3 also re-computed (sanity check — they PASSED under heuristic; should still PASS under explicit field; if either regresses, surface as anomaly in disposition)
- [ ] Document result at `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/`:
  - `R2-test1.md` — H1 re-test (the key result)
  - `R2-test2.md` — H2 sanity-check re-test
  - `R2-test3.md` — H3 sanity-check re-test
  - `summary.md` — full re-run metadata + comparison to v0.13/v0.14 baselines
- [ ] Per-class category audit: explicit geometry-type distribution across 51 classes (the "true" partition that the heuristic mis-rendered as 43/3/4)
- [ ] **If H1 PASS:** STATE + HANDOFF entries in hive log; tag `vs2a/v0.2-r2-h1-revalidated` fires; WP-R2-A-1 watchpoint CLOSES
- [ ] **If H1 FAIL under corrected instrument:** STATE entry in hive log + REQUEST entry routing to gandalf for re-disposition; gandalf authors disposition per R2/R8/R1 precedent pattern (deeper finding worth surfacing — catalogue diversity may be binding constraint vs instrument)
- [ ] AGENT_STATE.md updated

---

## Cross-seam contract change? (Principle 6 gate)

**Sim seam re-run only; no schema or contract change in this dispatch.** F1 carried the contract change; this dispatch CONSUMES that change.

**Round-trip: not applicable in this dispatch — F1 already smoke-tested the round-trip; this dispatch re-uses the consumer surface.**

---

## Acceptance criteria

- [ ] R2 sub-gauntlet re-run executed under explicit `geometry_type` field
- [ ] H1 + H2 + H3 metrics recomputed
- [ ] Per-class geometry-type distribution audited (true partition surfaced)
- [ ] Result docs filed at `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/`
- [ ] If H1 PASS: tag `vs2a/v0.2-r2-h1-revalidated` requested + WP-R2-A-1 closed
- [ ] If H1 FAIL: gandalf re-disposition surface via REQUEST entry; tag HELD
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on start + STATE on completion + REQUEST if FAIL routes to gandalf

---

## Out of scope

- F1 implementation (rocket + star-lord; upstream)
- Spatial boss recalibration (R2 H1 disposition § 3.4 forward-flagged; potentially VS2b; not in scope unless gandalf re-disposition routes it)
- Kit-redesign coupling (S1 sprint; separate dispatch with own R1 sprint re-run as validation gate)
- New R2 hypothesis tests beyond H1/H2/H3 (out of scope)

---

## Open questions for gamora

- **Re-run cohort size** — full 51-class × 3-scenario × 30-fight (matches v0.13 production sprint) or subset for confirmation? Recommendation: full re-run to match production sprint cardinality + apples-to-apples variance comparison. L1 gamora.
- **Seed parity vs new seeds** — match v0.13 production sprint seeds for direct comparison or fresh seeds? Recommendation: seed parity for direct H1 comparison. L1 gamora.
- **What constitutes "PASS" vs "PARTIAL" re-disposition** — if variance is e.g. 0.08 (close to but below threshold), is that PASS (signal exists; instrument limitation persists at smaller magnitude) or FAIL (threshold is threshold)? Recommendation: literal threshold; if 0.08–0.099, surface to gandalf as PARTIAL with explicit framing.
- **H2 + H3 regression handling** — if either regresses below their (already-PASSED) thresholds under explicit field, surface as anomaly; do NOT roll back v0.14 tag.
- **Per-class geometry-type true partition disclosure** — does it influence S1 kit-redesign sprint shape? If the true partition surfaces e.g., 30 line / 15 point / 6 circle (very different from 43/3/4), surface to rocket + gandalf for S1 first-batch class selection refinement.

---

## References

- `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.2 + § 4
- F1 dispatch: `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-vs2a-geometry-type-schema.md`
- R2 production: `reincarnated-engine/output/R2-sprint-2026-05-19/`
- `reincarnated-engine/src/reincarnated/simulation/spatial_engine.py` (post-F1)
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.1 (F1 re-test gate)
- `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (WP-R2-A-1)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** F1 acceptance complete (schema field operational + backfill validated + `_determine_geometry_type()` direct-field-read + Pattern-P7 fail-loud + telemetry round-trip GREEN).

**Post-activation:** autonomous L1 gamora execution. If H1 FAIL, gandalf re-disposition under L2-equivalent. No Matt-wait either path.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. The instrument is mended; the test runs under the original threshold; the spatial signal either confirms or surfaces a deeper catalogue finding. Either result is honest progress.*

---

## Completion record

**Completed by:** gamora
**Date:** 2026-05-19
**Execution session:** VS2a R2-RT + R1 sprint v3 batch session

### Status: COMPLETE — H1 FAIL (new finding)

**Result:** H1 FAIL under corrected instrument. This is NOT a catalogue diversity failure. It is a spatial calibration saturation event.

**Root cause:** VS2a F1 correctly reclassified 18 additional circle-dominant classes (was 3, now 21 of 51). Circle skills now deal proper AOE damage in simulation. The DPS correction is large enough to produce WR=1.000 for all 51 classes in open_arena and chokepoint under the existing spatial calibration constants. H1 variance = 0.000 because the WR measuring surface is degenerate.

**True geometry partition (post-F1 backfill):**

| Geometry | n_classes | pct | was (heuristic) |
|---|---|---|---|
| circle | 21 | 41.2% | 3 |
| line | 2 | 3.9% | 0 |
| point | 28 | 54.9% | 43 |

**H-test results:**
- H1: FAIL (variance=0.000; threshold >=0.10; calibration saturation not catalogue diversity)
- H2: PASS at 100% (sanity check; boss_with_adds still 0.000; degenerate delta — consistent)
- H3: FAIL (chokepoint also at 1.000 WR ceiling; gap=0.000; same root cause)

**WP-R2-A-1:** PARTIALLY CLOSED — heuristic_fallback=0% (backfill condition MET); H1 measurement blocked by calibration saturation.

**Tag `vs2a/v0.2-r2-h1-revalidated` HELD** pending gandalf spatial calibration disposition + follow-on re-test.

**Scope completed:**
- [x] F1 completion verified (spatial_geometry_type in all shipped seasons; 0 heuristic_fallback)
- [x] R2 sub-gauntlet re-run executed (51 × 3 × 30; same seeds as production sprint)
- [x] H1/H2/H3 recomputed under explicit field
- [x] Per-class geometry-type distribution audited (true partition surfaced)
- [x] Result docs filed at `output/R2-h1-revalidation-2026-05-19/`
- [x] Hive log STATE + REQUEST entries filed
- [x] AGENT_STATE.md updated
- [ ] Tag `vs2a/v0.2-r2-h1-revalidated` HELD (H1 FAIL; spatial calibration disposition needed)

**Routing:** REQUEST to gandalf (hive log REQUEST entry filed) — spatial sub-gauntlet calibration recalibration before H1 can be measured under corrected instrument. Gandalf disposition covers open_arena/chokepoint calibration constants (SPATIAL_DAMAGE_SCALE, mob HP/count, or combination).

**Output files:**
- `/Users/admin/Games/reincarnated-engine/output/R2-h1-revalidation-2026-05-19/R2-test1.md`
- `/Users/admin/Games/reincarnated-engine/output/R2-h1-revalidation-2026-05-19/R2-test2.md`
- `/Users/admin/Games/reincarnated-engine/output/R2-h1-revalidation-2026-05-19/R2-test3.md`
- `/Users/admin/Games/reincarnated-engine/output/R2-h1-revalidation-2026-05-19/summary.md`
- `/Users/admin/Games/reincarnated-engine/output/R2-h1-revalidation-2026-05-19/geometry_audit.md`
- `/Users/admin/Games/reincarnated-engine/scripts/r2_h1_revalidation.py` (new script)
