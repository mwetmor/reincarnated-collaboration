# Dispatch — 2026-05-27 — Phase 7 2-Layer Joint-Gate Evaluation (gandalf composition spec + jack-ryan Discipline #18 canonical-write)

**From:** knight-rider
**To:** gandalf (composition spec authoring) + jack-ryan (Discipline #18 math-hotspot canonical-write at joint-gate threshold)
**Approved by:** Matt 2026-05-27 pre-ratification #1 (Phase 7 2-layer joint-gate thresholds; LOCKED Cycle 14 v1)
**Estimated effort:** ~1 week (gandalf composition spec ~3-4 days + jack-ryan canonical-write ~2-3 days post composition spec landing)
**Acceptance:** Phase 7 2-layer joint-gate spec authored; canonical thresholds at engine/canonical anchored; mechanical pass + cohesion pass + HELD verdict semantics; consumes Cycle 14 Phase 4 archive output + Phase 5 cohesion-judge output; mutability STATIC at Cycle 14 v1

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** lock the per-season acceptance gate combining mechanical archive ACCEPTED (Phase 4) with LLM cohesion validation (Phase 5). Without Phase 7 joint-gate, kits would pass to player surface without coherent identity validation. Composes "Engine first. Game second. Phase third." — engine-layer mechanical integrity (Phase 4) + game-layer thematic coherence (Phase 5) jointly evaluated at phase boundary (Phase 7).

**Refutation conditions:**
- Mechanical pass threshold (gauntlet PASS rate >70% within ±25% of cohort midpoint per cohort) produces too-restrictive OR too-permissive seasons empirically
- Cohesion pass threshold (ai_tell_compliance ≥0.7 + cohesion-judge confidence ≥0.65) saturates (all PASS) or starves (all FAIL)
- HELD verdict semantics (return-to-phase for cohesion-fail; discard for mechanical-fail) creates infinite loop OR loses kits that should be salvageable
- STATIC mutability prevents legitimate Cycle 15+ auto-tuning

## Context

**Matt pre-ratification #1 (LOCKED Cycle 14 v1):**

- **Mechanical pass:** gauntlet PASS rate >70% within ±25% of cohort midpoint per cohort (5 cohorts: Damage / Defensive / Control / Support / Hybrid; midpoints empirically calibrated per cohort) + Phase 4 archive ACCEPTED
- **Cohesion pass:** ai_tell_compliance_score ≥0.7 + cohesion-judge confidence ≥0.65
- **HELD verdict:**
  - cohesion-fail-only → return-to-phase (kit returns to Phase 5 for re-LLM with new prompt seed)
  - mechanical-fail → discard (no salvage; Phase 4 archive rejected it)
  - NO silent re-roll loops; logged for design-quality audit per Discipline #43
- **Mutability:** STATIC at Cycle 14 v1; Cycle 15+ may auto-tune from production-season evidence

**Authority anchors:**
- Phase 4 archive ACCEPTED signal from gamora Dispatch 3A (`749d5aa`) MG-1..MG-5 emit kit_archive entries
- Phase 5 cohesion-judge output from Dispatch 3B Seam 3 (star-lord `bf7f659`) ExportFactionCluster schema includes cohesion_judge_confidence + ai_tell_compliance_score fields
- Discipline #43 design-quality audit at HELD verdict logging

## Required reading

- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 7 (canonical spec)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.10 (Phase 7 placeholder handling)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` ExportFactionCluster (cohesion_judge_confidence + ai_tell_compliance_score)
- Gamora Dispatch 3A completion record (kit_archive ACCEPTED signal semantics)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #18 (math-hotspot ratification; canonical-write authority for Phase 7 thresholds) + § #43 (design-quality audit)

## Discipline #46 compliance

- ExportFactionCluster + kit_archive DB queries follow per-cell bounding (Phase 4 archive scope) + Phase 5 export schema query patterns
- EXPLAIN QUERY PLAN at impl time

## Discipline #42 framing-audit

- **Q1:** (1) Cohort midpoints empirically calibrated per cohort (Damage/Defensive/Control/Support/Hybrid) requires Phase 4 production-season baseline data; (2) HELD verdict "return-to-phase" produces convergent re-LLM behavior (no infinite loop); (3) STATIC mutability is the right ratchet for v1
- **Q2:** verify cohort midpoint calibration data source; verify return-to-phase semantics terminate
- **Q3:** if cohort midpoints can't be empirically calibrated pre-impl, invoke #44 + route back; if return-to-phase fails to terminate, redesign HELD verdict

## Scope (two seams; sequential gandalf → jack-ryan)

### Seam 1 — gandalf composition spec authoring (~3-4 days)

- [ ] Author Phase 7 composition spec at `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` (gandalf judgment on canonical path)
- [ ] Mechanical pass spec (gauntlet PASS rate threshold; cohort midpoint calibration procedure; ±25% band semantics)
- [ ] Cohesion pass spec (ai_tell_compliance + cohesion-judge confidence thresholds; failure-mode analysis)
- [ ] HELD verdict state machine (cohesion-fail → return-to-phase; mechanical-fail → discard; logging schema)
- [ ] Design-quality audit hooks (Discipline #43 composition; what gets logged at HELD verdict)
- [ ] Mutability lock semantics (STATIC at v1; Cycle 15+ auto-tune trigger criteria)
- [ ] D-Sharpened composition (Phase 7 evaluates ALL kits uniformly regardless of substrate-anchored vs synthesized)
- [ ] Risks + Watch Items per failure-modes register § 5 (F-5 joint-gate threshold drift; F-1 math methodology drift)

### Seam 2 — jack-ryan Discipline #18 canonical-write (~2-3 days)

- [ ] Canonicalize Phase 7 thresholds at engine canonical path (math note at `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` OR equivalent jack-ryan judgment)
- [ ] Discipline #18 math-hotspot compliance (algorithm spec + methodology ratification + empirical-evidence-gated mutability ratchet)
- [ ] Discipline #43 composition (HELD verdict logging structure for design-quality audit)
- [ ] Gate-1 PASS verdict on gandalf composition spec
- [ ] Cross-reference Phase 4 archive ACCEPTED + Phase 5 cohesion-judge output schemas

### Cross-cutting

- [ ] Composes with gamora `749d5aa` Phase 4 archive output (kit_archive table + ACCEPTED signal)
- [ ] Composes with star-lord `bf7f659` Phase 5 ExportFactionCluster output (cohesion fields)
- [ ] STATIC mutability ratchet at Cycle 14 v1; Cycle 15+ revisit trigger documented

### Closure

- [ ] Phase 7 spec at canonical path (gandalf seam) + canonical math note (jack-ryan seam)
- [ ] Append completion records (both seams; cross-reference each other)
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern
- [ ] Signal Phase 7 dispatch ready for downstream Wave 5 production-season consumption

## Acceptance criteria

- [ ] Phase 7 composition spec landed (gandalf seam)
- [ ] Phase 7 thresholds canonicalized (jack-ryan seam)
- [ ] Mechanical + cohesion pass thresholds + HELD verdict state machine specified
- [ ] STATIC mutability ratchet locked
- [ ] Discipline #18 + #43 + #46 § 7 compliance verified
- [ ] D-Sharpened invariance verified
- [ ] Risks + Watch Items embedded
- [ ] Completion records + commit + push

## Out of scope

- Do NOT execute Phase 7 impl (separate dispatch at Wave 4/5 boundary)
- Do NOT touch Phase 4 impl (gamora Dispatch 3A already complete)
- Do NOT touch Phase 5 impl (Dispatch 3B in progress)
- Do NOT auto-tune thresholds (STATIC at Cycle 14 v1)
- Do NOT enter Wave 5 production-season scope (separate dispatch)

## Open questions

- **Q-P7-1 (gandalf):** Cohort midpoint calibration data source — Phase 4 production season required OR can it use historical telemetry (D11 + D12 era)?
- **Q-P7-2 (gandalf):** Return-to-phase max retry count? If unbounded, what prevents infinite loop semantically? Recommend 2-retry cap with discard-on-3rd-fail
- **Q-P7-3 (jack-ryan):** Discipline #18 canonical-write venue — engine math/ folder vs canonical/ folder? Your judgment

## References

- Matt 2026-05-27 pre-ratification #1 verbatim (Phase 7 thresholds LOCKED)
- Doc 39 § Phase 7 canonical spec
- Gamora Dispatch 3A completion `749d5aa` (Phase 4 ACCEPTED signal)
- Star-lord Dispatch 3B Seam 3 completion `bf7f659` (Phase 5 cohesion fields)
- Engineering-disciplines.md § Discipline #18 + #43 + #46

---

## Completion record (two seams; append per seam)

### Seam 1 — gandalf
(pending)

### Seam 2 — jack-ryan
(pending)
