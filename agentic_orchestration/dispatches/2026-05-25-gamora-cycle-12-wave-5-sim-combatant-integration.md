# Dispatch — 2026-05-25 — gamora — Cycle 12 Wave 5 sim combatant integration (AlteredFightEngineContext consumption)

**From:** knight-rider
**To:** gamora (engine simulation seam — simulation/spirit_guide; fight engine + balance loop + damage resolver owner)
**Approved by:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q1 Option γ includes cross-seam wiring per Gate-2-on-L3 INFO-D) + skip-confirmation re-auth 2026-05-25 + KR autonomously orchestrates per scope-doc § 1
**Estimated effort:** ~30-90 min gamora (synthetic-agent throughput)
**Acceptance:** Sim combatant integration consumes AlteredFightEngineContext from Layer 6 wire-up; gauntlet sim run_spatial_gauntlet correctly applies 6 v1 strategy alterations to combat arithmetic; integration smoke (kit with alteration → gauntlet sim → fight outcome reflects alteration) PASS for representative kits; no regression on existing gauntlet sim baselines

---

## Context

Cycle 12 Wave 5 cross-seam follow-on fan-out — **THIS IS THE CRITICAL CONSUMER for T4 post-mortem readiness**. Without gamora sim consumer integration, the AlteredFightEngineContext from Layer 6 wire-up doesn't actually affect fights (alterations remain effectively intent metadata at sim time — same gap that triggered Cycle 11 BC-shift FAIL diagnostic + Tier 2 ratification).

Rocket Layer 6 ✅ COMPLETE + Gate-2 ✅ PASS — emits AlteredFightEngineContext per `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py` `apply_t4_alteration_to_combat()` + `wire_up_kit_layer6()`. The 6 v1 strategies each have specific combat-arithmetic touch-points already encoded in the AlteredFightEngineContext shape. Gamora sim consumer integrates the context at sim time so the gauntlet actually reflects the alterations.

**Gate-2 on L6 verified sim_prerequisite=None for all 6 strategies** — no sim-seam boundary touch required beyond combat-arithmetic deltas. Sim consumer integration is straightforward consumption (no engine architectural changes).

---

## Required reading before starting

- **`~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`** § v1.4-layer-6 — **PRIMARY load-bearing** — documents AlteredFightEngineContext shape Layer 6 emits
- **`~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py`** — `apply_t4_alteration_to_combat()` + 6 strategy application functions; verify combat-arithmetic touch-points per strategy
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-6-section-8-wireup-and-l9-refactor.md` Bucket 1 (§ 8 wire-up per-strategy combat-arithmetic touch-points)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-4-rocket-layer-6.md` Bucket 1 (verified all 6 strategies wire correctly; sim_prerequisite=None CLEAR)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 (apply_t4_alteration_to_combat signature LOCKED) + § L10 (Tier 2 framing — Cycle 11 § 8 intent metadata + Cycle 12 L6 wire-up = full v1 closure — gamora consumer integration COMPLETES the closure)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/` (gamora seam state; spatial_gauntlet entry point; fight engine architecture)
- `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (Cycle 11 § 8 — 6 strategy definitions for context)
- `canonical/story/skill-system-2026-05-24.md` § 8 (Algorithm § 8 architecture — semantic intent gamora preserves at sim time)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #2 + #2.1 + #8 + #11 + ADR-004)

---

## Math-before-code (per Discipline #1)

Author math-note at `~/Games/reincarnated-engine/src/reincarnated/simulation/notes/cycle-12-wave-5-sim-combatant-integration-2026-05-25.md` (or gamora naming) BEFORE implementation. Per Discipline #1.2 (L4/L6 precedent): math-note code-line citations REQUIRED.

### Math 1 — AlteredFightEngineContext consumption interface

- Per MIGRATION.md § v1.4-layer-6: AlteredFightEngineContext shape rocket emits
- Per t4_wireup.py: 6 strategy modifications per kit (cost_resource_override, hit_modifier, crit_rate, damage_type, defensive remap deltas, aoe_radius × damage_multiplier, max_life_override + chaos_immune)
- Gamora consumer: read AlteredFightEngineContext at fight-start; apply modifications to combat-arithmetic primitives

### Math 2 — Per-strategy sim consumer integration

For each of 6 v1 strategies, define gamora-side consumption + verify sim engine actually reflects:
- RESOURCE_CONVERSION: gamora uses `cost_resource_override` when computing skill cost
- TRADE_OFF: gamora applies `hit_modifier=1.0` + `crit_rate=0.0` at fight start
- ELEMENT_CONVERSION: gamora uses `damage_type` per skill on outgoing damage
- DEFENSIVE_CONVERSION: gamora applies defensive layer remap at fight start
- GEOMETRY_COLLAPSE: gamora uses `aoe_radius × damage_multiplier` for AOE skill geometry
- DEFENSIVE_TRADEOFF: gamora applies `max_life_override=1` + `chaos_immune=True` at fight start

### Math 3 — Integration smoke design (Discipline #19.1)

- Per-strategy integration smoke: kit with strategy X → gauntlet sim → fight outcome reflects strategy X (per cheapest-refuting-test design)
- Spot-check: 6 representative kits (one per strategy) + 6 baseline kits (no alteration) — verify alteration kits behave differently from baseline kits in semantically-expected ways
- Pre-existing gauntlet sim baselines must not regress

---

## Cross-seam contract change? (Principle 6 gate)

**No** in the strict sense — gamora consumes existing AlteredFightEngineContext shape from rocket L6 (consumer side; doesn't emit new shape). But gamora may want to extend fight_log dict shape if it records that alteration was applied (for downstream telemetry/audit). If fight_log shape changes, that's a cross-seam contract change requiring MIGRATION.md update.

**Round-trip smoke**: not strictly required (consumer-only side); but per Principle 6 spirit, integration smoke verifies fight outcome reflects alteration end-to-end.

---

## Scope (gamora sim combatant integration)

### Per-strategy consumer integration

- [ ] RESOURCE_CONVERSION: integrate cost_resource_override into skill-cost computation
- [ ] TRADE_OFF: apply hit_modifier=1.0 + crit_rate=0.0 at fight start
- [ ] ELEMENT_CONVERSION: apply damage_type per skill on outgoing damage resolution
- [ ] DEFENSIVE_CONVERSION: apply defensive layer remap at fight start (per rocket L6 deltas)
- [ ] GEOMETRY_COLLAPSE: apply aoe_radius × damage_multiplier for AOE skill geometry
- [ ] DEFENSIVE_TRADEOFF: apply max_life_override=1 + chaos_immune=True at fight start

### Integration smoke + acceptance

- [ ] Per-strategy integration smoke (6 representative kits × 6 strategies)
- [ ] Baseline kits (no alteration) regression check — gauntlet outcomes unchanged
- [ ] Full L2+L3+L4+L6 + gamora consumer end-to-end pass for a representative season (e.g., 22 kits × N fights)
- [ ] No regression on existing gauntlet sim baselines (Cycle 11 + earlier seasons)
- [ ] MIGRATION.md authored if fight_log shape changed; otherwise gamora-seam-only

### Provenance

- [ ] Math note authored per Discipline #1 + #1.2 (code-line citations)
- [ ] AGENT_STATE.md updated with Cycle 12 Wave 5 sim integration checkpoint
- [ ] Tag: `gamora/cycle-12-wave-5-sim-combatant-integration-2026-05-25`
- [ ] Auto-commit + auto-push per gamora seam authorization (CLAUDE.md addendum + Cycle 12 push-per-wave LIVE)

---

## Out of scope

- Layer 6 emission contract changes (LOCKED; consume as-is)
- New § 8 strategies beyond 6 v1 (v1.1+ scope)
- Star-lord export schema changes (separate cross-seam dispatch)
- Drax loadout consumer code (separate cross-seam dispatch)
- Architectural amendments (escalate via KR per scope-doc § 5)
- Performance benchmarking beyond Discipline #2.1 resource-scaling rehearsal
- v1.1+ items

---

## Acceptance criteria

- [ ] Math note authored per Discipline #1 + #1.2
- [ ] All 6 v1 strategies integrated per Math 2
- [ ] Integration smoke PASS (6 strategy kits + 6 baselines + full season end-to-end)
- [ ] No regression on existing gauntlet sim baselines
- [ ] MIGRATION.md if cross-seam impact (fight_log shape change); otherwise gamora-internal
- [ ] AGENT_STATE.md updated
- [ ] Tag: `gamora/cycle-12-wave-5-sim-combatant-integration-2026-05-25`

---

## Open questions for the agent to resolve

- Whether fight_log shape should record "alteration_applied" provenance for downstream telemetry/audit (gamora judgment; recommend yes for Cycle 12 → Cycle 13+ BDI test framework needs)
- Whether per-strategy integration smoke uses synthetic test kits OR existing season kits (gamora judgment; recommend synthetic for cheapest-refuting-test + existing for regression baseline)
- Whether gauntlet sim baseline regression check requires N-fight statistical sampling OR single-fight smoke per kit (gamora judgment per existing testing patterns)

---

## Cross-seam impact

If fight_log shape changes per "alteration_applied" provenance recording: MIGRATION.md required per ADR-004 (downstream telemetry/star-lord export consumers + future Cycle 13+ BDI test framework consumers).

If gamora sim integration surfaces strategy that doesn't apply correctly via AlteredFightEngineContext (e.g., requires gamora-side change beyond consumption): flag to KR for cross-seam coordination per scope-doc § 5 — possibly route to rocket for L6 amendment if rocket L6 emission missed a touch-point.

---

## References

- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-6 (PRIMARY)
- `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py`
- `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py`
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-6-section-8-wireup-and-l9-refactor.md`
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-4-rocket-layer-6.md` (Gate-2 PASS verdict; sim_prerequisite=None CLEAR)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 + § L10
- `canonical/story/skill-system-2026-05-24.md` § 8
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification + skip-confirmation re-auth + KR autonomously orchestrates per scope-doc § 1
**Status:** FIRE — Wave 5 parallel-fire with star-lord + drax cross-seam consumers; **CRITICAL CONSUMER** for T4 post-mortem readiness (without gamora integration, AlteredFightEngineContext doesn't actually affect fights)

**Matt-touch sequence:** gamora completes → KR captures in state file → integration smoke + jack-ryan Gate-2 on full new engine fires when all 3 cross-seam consumers land
