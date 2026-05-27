# Dispatch — 2026-05-27 — gamora — Cycle 13 SC-6 GAP 2 Reference Encounter Audit

**From:** knight-rider
**To:** gamora (audit lead)
**Approved by:** Matt 2026-05-27 — Cycle 13 handoff doc § 4.1.3 (SC-6 GAP 2 audit dispatch) + framing brief § 4.1 KR autonomous (sidecar dispatching) + Matt verbatim "Resume Wave 0 → Wave 1 dispatch sequencing"
**Estimated effort:** 4-6 hrs audit (Pattern A subagent-sized)
**Acceptance:** audit memo at `agentic_orchestration/gamora/notes/2026-05-27-sc-6-reference-encounter-audit.md` covering current reference encounter content vs ~22 BC-target cells + gap identification + recommended additions; feeds Cycle 13 Wave 5 gauntlet sim execution preparation

## Context

Closeout doc § 5.1 GAP 2 LOCKED architectural intent:
- Endgame-reference-encounter catalog covering ~22 BC-target cells (per `v1-bc-target-intent-2026-05-24.md`)
- Minimum 8-12 / optimal 15-22 / maximum ~30 reference encounters
- Each encounter exercises full playability criterion (D61 / now Discipline #26)
- Wave 0 audit dispatch fires — gamora (sim-side audit lead) + rocket (encounter content audit) + jack-ryan (Gate-1 critique)

This dispatch is the gamora-led multi-seam audit. Gamora is audit lead per simulation seam ownership of gauntlet sim + reference encounter consumption; rocket is encounter content seam owner; jack-ryan is Gate-1 critique on audit findings + recommended-additions list.

**Per Cycle 13 v1 scope (closeout § 4 + doc 41):** calibrate against endgame-reference-encounter (L45-50+ progression node only); multi-node calibration is post-scaling-formulas work (Cycle 14+). Audit focus is endgame-encounter-only for v1; pre-endgame encounter content is deferred.

**Per Discipline #26 (Playability) + #30 (Sim methodology naming):** each encounter should exercise playability criterion (6 sub-gates: KPM-in-band + rotation-coherence + resource-flow + defensive-uptime + non-degenerate + cognitive-load-manageable) per cohort × cell.

## Required reading before starting

1. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 5.1 (GAP 2 substantive lock + audit framing)
2. `canonical/41-progression-framework-2026-05-27.md` § 3 (node-identity mapping — endgame node L45-50+)
3. `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` (P_node + C_archetype + W function — sim consumes reference encounters per scaffolds)
4. `canonical/story/v1-bc-target-intent-2026-05-24.md` (Sketch F + ~22 BC-target cells; sim coverage targets)
5. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes operational truth)
6. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 4 + § 6 + § 8 (multi-T4 architecture + multi-node calibration + D27 progression nodes; endgame focus)
7. `agentic_orchestration/operating-procedures/gamora.md` (your operating procedure — fight-engine + balance-loop + gauntlet sim)
8. `agentic_orchestration/dispatches/2026-05-26-gamora-cycle-13-wave-0-methodology-consultation-prep.md` (your prior dispatch this cycle; methodology framework draft is companion context)
9. Existing reference encounter content paths (review your own seam): `reincarnated-engine/src/reincarnated/simulation/` for gauntlet sim test fixtures + reference encounter definitions; locate per file + line number for audit citations (Discipline #1.2)
10. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1.2 code-citation + #11 empirical inspection + #18 + #26 playability + #30 sim methodology naming)

## Math-before-code (audit; no code)

NOT applicable — audit + reporting only. No engine modifications. No sim runs.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Audit memo is design-input artifact; no schema / fixture / boundary mutation.

## Scope

### Audit dimensions

- [ ] **Current reference encounter inventory** — enumerate every existing reference encounter in current engine codebase (sim fixtures + test encounter definitions + balance loop reference encounters); file path + line number per encounter per Discipline #1.2
- [ ] **BC-target-cell coverage map** — for each existing encounter, identify which BC-target cell(s) it exercises per the 5-tuple BC partition (engagement profile / damage geometry / proxy density / control density / damage tempo / damage amplitude variance / defensive profile / resource economy); map encounter → cell(s)
- [ ] **Coverage gap analysis** — per the ~22 v1 BC-target cells per `v1-bc-target-intent-2026-05-24.md`, identify which cells have:
  - **WELL-COVERED:** ≥1 high-quality encounter directly exercising the cell
  - **THIN-COVERAGE:** 1 encounter but quality concerns OR encounter only partially exercises the cell
  - **NO-COVERAGE:** 0 encounters; cell is a gap
- [ ] **Encounter quality assessment** — for each existing encounter, evaluate against playability criterion (#26) 6 sub-gates:
  - Does encounter sustain KPM measurement? (long enough to measure; varied enough to not trivialize)
  - Does encounter exercise rotation coherence? (forces meaningful skill choice)
  - Does encounter exercise resource flow? (resource economy management challenge)
  - Does encounter exercise defensive uptime? (incoming damage; defense decisions)
  - Does encounter risk degenerate states? (any of the 8 patterns per closeout § 5.2)
  - Does encounter respect cognitive load? (manageable scope; not trivializing or overwhelming)
- [ ] **Cycle 13 v1 scope filter** — focus audit on ENDGAME-reference-encounter category only (L45-50+ per doc 41); flag any encounters that are pre-endgame as "deferred Cycle 14+ scope" (not Cycle 13 v1 work)
- [ ] **Recommendation — encounter additions per gap closure** — for each NO-COVERAGE cell + THIN-COVERAGE cell, propose specific additions:
  - Minimum target (per closeout § 5.1): 8-12 encounters total
  - Optimal target: 15-22 encounters
  - Maximum: ~30 encounters
  - Per recommended addition: cell targeted + encounter intent + expected playability-criterion coverage + difficulty calibration intent (anchored to endgame per Block C scaffolding § 1.4 anchored intent)

### Multi-seam coordination

- [ ] **Rocket consultation flag** — if encounter content additions require new mob types / new encounter templates / new test fixtures, flag specific work-unit specifications for rocket Wave 0/1 implementation; do NOT author rocket implementation work in this dispatch
- [ ] **Jack-ryan Gate-1 critique handoff** — audit memo concludes with Gate-1 critique fire intent (KR will dispatch jack-ryan critique on this audit's recommendations post-completion)

### Discipline application

- [ ] **#1.2 code-citation discipline** — every encounter inventoried with file path + line number
- [ ] **#11 empirical inspection over assumption** — citations VERIFIED before reporting (don't trust grep summaries; spot-check actual file content)
- [ ] **#26 playability** — each encounter quality assessed against 6 sub-gates per closeout LOCK
- [ ] **WARN-pattern reminder per skill_handoff_2026-05-26 § 1 Priority 2 (carried into Cycle 13 per scope-doc context):** post-script empirical count assertions per audit dimension — "I cite N encounters; verified by grep <pattern> at <paths> returning N entries"

## Acceptance criteria

- [ ] Audit memo authored at `agentic_orchestration/gamora/notes/2026-05-27-sc-6-reference-encounter-audit.md`
- [ ] All 5 audit dimensions covered with empirical data
- [ ] File path + line number citations per Discipline #1.2
- [ ] Coverage map exhaustive over ~22 v1 BC-target cells
- [ ] Quality assessment per encounter against #26 6 sub-gates
- [ ] Recommendation explicit + actionable (specific encounter additions; not "needs more research")
- [ ] Post-script empirical count assertions per dimension
- [ ] Memo length proportional to actual gap surface (~5-12 pages typical)
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Authoring new reference encounters (audit only; rocket implementation in subsequent dispatch IF recommendation accepted)
- Modifying simulation code
- Running simulation against encounters
- Pre-endgame encounter content audit (deferred Cycle 14+ per doc 41 § 4 #4)
- Cross-cycle scope expansion proposals
- Authoring jack-ryan Gate-1 critique on audit findings (separate dispatch)

## Open questions for the agent to resolve

- Encounter granularity — does an "encounter" mean a single fight, a sequence (e.g., gauntlet wave), or a calibrated set? Apply gauntlet sim's own definition consistently
- Quality threshold — if an encounter exercises 5 of 6 playability sub-gates but fails 1, classify as "THIN-COVERAGE" or "WELL-COVERED with caveat"? Your call as seam-owner per substrate-led discipline
- Minimum-to-optimal trade-off — if recommending additions, prioritize NO-COVERAGE cells first; THIN-COVERAGE improvements as secondary

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 5.1 (GAP 2 source)
- `canonical/41-progression-framework-2026-05-27.md` § 3 (endgame node identity)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` (sim consumes encounters per scaffolds)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (~22 BC-target cells)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1.2 + #11 + #18 + #26 + #30)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-handoff-to-knight-rider.md` § 4.1.3 (this dispatch's authority basis)

---

**Cycle:** 13
**Wave:** 0 / Sidecar SC-6 (multi-seam: gamora lead + rocket consultation flagged + jack-ryan Gate-1 post-audit)
**Gates:** feeds Wave 5 gauntlet sim execution preparation
**Priority:** P2 — fire parallel with Wave 1 + SC-4 expansion + SC-2 expansion
