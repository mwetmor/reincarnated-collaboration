# Dispatch — 2026-05-19 — gamora — Stage A2 A4 B14 multi-band convergence sim

**From:** knight-rider
**To:** gamora (sim seam — B14 multi-band convergence OWNER; extends B14.5 V1)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires at Stage A2 kickoff
**Estimated effort:** ~2–3 weeks gamora
**Acceptance:** Per § Acceptance. Tag fires: `stage-a2/v0.4-b14-multi-band-convergence`.
**Hive context:** Stage A2 closeout hive — A4 is the **riskiest Stage A2 piece** per roadmap "Refactor vs rewrite" note. B14.5 V1 architecture is the canonical balance-loop pattern; B14 EXTENDS multi-band without replacing.

---

## Context

Per `canonical/28-engine-arpg-rebalance-design.md` B14 + `canonical/16-project-roadmap.md` § "Track A landing rhythm":

> **B14 is the riskiest piece but operates on existing primitives.** 5 production seasons + demo1 v1.2 prove the architecture; throwing it away discards validated knowledge.

B14.5 V1 shipped 2026-05-12 as `v1.3-b14-5-primary-loop` — the CANONICAL BALANCE-LOOP ARCHITECTURE. B14 multi-band extends this V1 pattern with multi-band convergence (e.g., 0/16/32/50 tier-band convergence in single sim run).

**Risk mitigation per roadmap:**
- B14.5 V1 architecture preserved as canonical pattern
- `v1.3-b14-5-primary-loop` tag is restore point
- Per-stage tagged releases enable incremental rollback

---

## Required reading

In order:
1. `canonical/28-engine-arpg-rebalance-design.md` B14 (full spec)
2. `canonical/16-project-roadmap.md` § "Track A landing rhythm" (refactor-vs-rewrite + B14 risk note)
3. B14.5 V1 architecture: `v1.3-b14-5-primary-loop` commit + completion record (canonical balance-loop pattern)
4. B14.5 V1 design discipline lessons: `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (engineering disciplines authored from B14.5 work — particularly Discipline #1 math-before-code + #2 smoke-test + canonical-balance-loop pattern)
5. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
6. `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` + related code paths (current single-band V1)
7. `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.4 (A4)
8. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Math-before-code (Discipline #1)

**Math-load-bearing per B14 spec.** Authoring required before implementation:

### Multi-band convergence design draft

**Path:** `reincarnated-engine/design/working-agreement/A4-b14-multi-band-convergence-2026-05-19.md`

Captures:

1. **Band definitions** — tier-bands (e.g., 0 / 16 / 32 / 50; specific tier-band selection per B14 spec)
2. **Convergence math** — how multi-band convergence extends V1's recompose-first + hybrid rejection gate + adaptive quick-estimate pattern
3. **Smoke-test mode** for fast iteration (per V1 canonical pattern)
4. **Per-band telemetry** captured + analyzed
5. **Cross-band variance budget** — what's the acceptable variance across bands for "converged"?
6. **Hypothesis tests** — what does B14 multi-band PASS mean per spec?
7. **Rollback path** — `v1.3-b14-5-primary-loop` is restore point; explicit fail-safe

Jack-ryan reviews math before commit.

---

## Cross-seam contract change? (Principle 6 gate)

**Sim seam only; telemetry surface extends.**

**MIGRATION.md** at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (telemetry surface extension + multi-band convergence pattern).

**Round-trip smoke**: per-band convergence telemetry → class_balance_results extension → export packet.

---

## Scope

- [ ] Math-before-code design draft authored
- [ ] Multi-band convergence operational (extends V1 architecture; does NOT replace)
- [ ] B14 hypothesis tests executed per spec
- [ ] Per-band telemetry captured + cross-band variance budget honored
- [ ] Smoke-test mode operational for fast iteration
- [ ] Rollback path documented + tested (verify V1 baseline still achievable if multi-band regresses)
- [ ] MIGRATION.md appended at sim seam
- [ ] Round-trip smoke per Principle 6
- [ ] Smoke-test GREEN throughout
- [ ] AGENT_STATE.md updated
- [ ] Tag fire request: `stage-a2/v0.4-b14-multi-band-convergence`

---

## Acceptance criteria

- [ ] Design draft authored + jack-ryan math review BEFORE production code change
- [ ] Multi-band convergence operational (extends V1)
- [ ] B14 hypothesis tests PASS per spec
- [ ] Per-band telemetry captured
- [ ] Cross-band variance budget validated
- [ ] Rollback path operational
- [ ] MIGRATION.md
- [ ] Smoke-test GREEN
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on math-before-code phase start + STATE on impl phase + STATE on hypothesis-test pass + completion
- [ ] Tag: `stage-a2/v0.4-b14-multi-band-convergence`

---

## Out of scope

- B7 gear-variance gate (A1; sibling sim work)
- B12 gear-slot expansion (A2; catalogue work)
- B13 mobility geometries (A3; catalogue + AI work)
- B14.5 V1 architecture replacement (V1 is canonical pattern; B14 extends)
- New balance metric introductions beyond multi-band (out)
- Convergence reshape (Stage A6 territory)
- Cross-season meta-progression validation (separate playtest exception; not A4)

---

## Open questions for gamora

- **Band selection** — L1 gamora per B14 spec. Recommendation: 4 bands matching ARPG progression milestones (e.g., 0/16/32/50). Document choice.
- **Hypothesis-test threshold** — L1 gamora + gandalf consult if threshold philosophy requires design judgment (e.g., is "multi-band convergent" measured by absolute variance or relative shape?)
- **Smoke-test mode trade-offs** — L1 gamora per V1 canonical pattern; document smoke vs full-regen discipline (Discipline #2)
- **Rollback trigger** — L1 gamora. If B14 multi-band fails hypothesis test, rollback to V1; document failure-mode detection criteria
- **Substrate-identity continuity** — B14 must preserve substrate-identity invariance per R8 disposition § 9.5; document validation
- **B14.5 V2 secondary-loop interaction** — if V2 secondary-loop work surfaces during B14, surface to gandalf for re-disposition (V2 was forward-flagged; not in A4 scope)

---

## References

- `canonical/28-engine-arpg-rebalance-design.md` B14
- `canonical/16-project-roadmap.md` § "Track A landing rhythm"
- B14.5 V1 architecture: `v1.3-b14-5-primary-loop` (2026-05-12; canonical balance-loop pattern)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Disciplines from B14.5)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` + `balance_loop.py`
- `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.4
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** Stage A2 kickoff (VS2b V6 ships). Engine-only; no design watch-item gate.

**Post-activation:** gamora L1 within seam; jack-ryan reviews math; gandalf L2 consult only if threshold philosophy or substrate-identity surfaces. No Matt-wait. **Highest-risk dispatch in Stage A2 — pre-approval includes the rollback authority.**

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. A4 extends the canonical balance-loop pattern; multi-band convergence is the riskiest piece but operates on V1's proven primitives; the rollback tag stays available if hypothesis fails.*
