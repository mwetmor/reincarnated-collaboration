# Dispatch — 2026-05-19 — gamora — Stage A2 A1 B7 gear-percentile variance gate

**From:** knight-rider
**To:** gamora (sim seam — engine-only; B7 OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19 "approved, proceed all the way through Stage A2"); fires at Stage A2 kickoff
**Estimated effort:** ~2–3 days gamora
**Acceptance:** Per § Acceptance. Tag fires: `stage-a2/v0.1-b7-gear-variance-gate`.
**Hive context:** Stage A2 closeout hive — A1 is engine-only; can fire at Stage A2 kickoff (no A6 framework gate; engine-only sim work).

---

## Context

Per `canonical/28-engine-arpg-rebalance-design.md` B7 + co-design with B10 (gauntlet structure already shipped):

> Per-class gear-percentile variance check: balance loop must produce stable convergence across multiple gear rolls per class.

The variance gate is a sim-time validation that catalogue gear rolls don't destabilize convergence per class. Co-designed with B10 (which sets the gauntlet density baseline against which gear-variance is measured).

A1 closes the variance check that VS2a's S1 kit-redesign sprint shipped against. Now the catalogue is stable; B7 gates whether gear rolls preserve that stability.

---

## Required reading

In order:
1. `canonical/28-engine-arpg-rebalance-design.md` B7 + B10 co-design
2. VS2a S1 dispatch + completion record (`agentic_orchestration/dispatches/2026-05-19-rocket-plus-gandalf-vs2a-S1-kit-redesign-sprint.md`) — catalogue baseline
3. B14.5 V1 canonical balance-loop architecture (`v1.3-b14-5-primary-loop` 2026-05-12)
4. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
5. `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.1 (A1)
6. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

- [ ] Per-class gear-variance simulation: multiple roll percentiles (e.g., 25/50/75/90/99) across each class's gear loadout
- [ ] Variance metric: convergence stability across roll percentiles
- [ ] Gate threshold per B7 spec (gamora L1 selects; document choice)
- [ ] Telemetry surface: per-class gear-variance distribution captured (extends `class_balance_results` if needed)
- [ ] Run on VS2a-regen catalogue + VS2b-regen catalogue (both seasons available post-VS2b ship)
- [ ] MIGRATION.md if telemetry surface extends
- [ ] Smoke-test GREEN
- [ ] AGENT_STATE.md updated
- [ ] Tag fire request: `stage-a2/v0.1-b7-gear-variance-gate`

---

## Cross-seam contract change? (Principle 6 gate)

**Sim seam only; telemetry surface may extend** (additive per ADR-004).

**MIGRATION.md** at sim seam if telemetry extends. Star-lord consumer notified via hive log if class_balance_results table extends.

**Round-trip smoke**: per-fight gear-variance telemetry → class_balance_results → export packet (if extended). Field-presence check.

---

## Acceptance criteria

- [ ] Gear-variance simulation operational across roll percentiles
- [ ] Per-class variance gate threshold applied; all classes pass OR documented exceptions surface
- [ ] Telemetry captured + (if extended) MIGRATION.md appended
- [ ] Smoke-test GREEN
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on start + STATE on completion
- [ ] Tag: `stage-a2/v0.1-b7-gear-variance-gate`

---

## Out of scope

- New gear catalogue additions (rocket A2 scope)
- B12 affix work (A2)
- B14 multi-band convergence (A4)
- Loadout UI changes (drax; not in B7 scope)

---

## Open questions for gamora

- **Variance gate threshold** — L1 gamora per B7 spec; document choice. If catalogue surfaces class-specific instabilities, surface to gandalf for re-disposition (may indicate kit-redesign or gear-tuning gap)
- **Roll percentile granularity** — L1 gamora. Recommendation: 5-point sample (25/50/75/90/99) covers reasonable variance space; document choice
- **Telemetry surface extension** — L1 gamora + star-lord consult if class_balance_results table needs new fields

---

## References

- `canonical/28-engine-arpg-rebalance-design.md` B7 + B10
- VS2a S1 dispatch + completion record (catalogue baseline)
- B14.5 V1 architecture (canonical balance-loop pattern)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.1
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** Stage A2 kickoff (VS2b V6 ships).

**Post-activation:** gamora L1 within seam; no Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. A1 validates that gear rolls preserve catalogue stability; the variance gate is the canary on the convergence.*
