# Dispatch — 2026-05-21 — gamora — W0.10: Boss AI leash-reset bug fix (Late-P0 workstream)

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** **gandalf W0.9 cumulative Gate-2 architectural close-out 2026-05-21 — OPTION A disposition** ("P0 should not close half-validated; W0.10 closes P0 on both architectural AND empirical commitments"). Per Matt's autonomous-operation directive 2026-05-21.
**Status:** PENDING — ACTIVE (gamora may execute when launched)
**Estimated effort:** ~1-2 weeks (substantial; math-before-code → critique-pair → implementation → re-test Track C § 2.3 prediction)
**Acceptance:** Player AI boss-focus mode implemented + add leash semantics calibrated; W0.9.6-equivalent calibration re-sweep verifies boss/mini-boss tier WR enters per-tier contract bounds (or surfaces residual gap requiring P2/P3 multi-dim convergence per math note §5.3); tag `qd-rebuild/v0.10-boss-ai-leash-reset-fixed`.

---

## Context — what surfaced

Per W0.9 Phase 2.5 calibration sweep (engine tag `qd-rebuild/v0.9-phase-2-5-calibration-sweep-complete`; commit `0837c7b`), the new spatial gauntlet reveals a structural arena-AI bug that universally blocks boss-tier engagement:

**Boss AI leash-reset bug** (gamora's empirical diagnosis per Discipline #11 inspection):
1. Player AI targets nearest alive mob — elite add at ~12m, NOT boss at ~17m
2. Player damages add → add chases player beyond `leash_distance_m=12.0` from spawn
3. Add leashes back → `entity.hp = entity.max_hp` (FULL HP RESET)
4. Repeat for 240s. Boss (stationary_caster, HP=53k at 0.40×) NEVER ENGAGED.
5. Empirical evidence: physical_grappler dealt 215,238 damage total (145 casts × 1,485 base damage); elite add HP dropped only 4,453 (consistent with ~3 hits landing between leash cycles).

**Math validates boss IS killable if reached:** TTK ~54s at modifier=0.742 within 240s timeout. NOT a scaling issue. STRUCTURAL ARENA-AI BUG.

**This is the recompose-hive "fix the arena, not the synergy" principle catching the NEXT arena bug** after PackProxy ×8 retirement. Per gandalf cumulative close-out: PackProxy and boss-AI-leash-reset are structurally identical — arena-side implementation defects that strip legitimate synergies of the ability to demonstrate themselves. Both are the same category of falsification.

**Per ARPG canon:** boss IS the focal point per D2/D3/D4/PoE/Last Epoch/Grim Dawn convention. Nearest-mob targeting is the BUG; boss-focus targeting is the GENRE-CORRECT default. The fix RESTORES canon, not deviates from it.

## Scope per gandalf Option A disposition + jack-ryan amendments

**Sub-task W0.10.1 — Math-before-code (Discipline #1; REQUIRED):**

Author math note at `reincarnated-engine/src/reincarnated/simulation/math/w0-10-boss-ai-leash-reset-fix.md`. Cover:

1. **Bug mechanism formalization:** leash-reset state machine + targeting priority math (current nearest-mob; replacement boss-focus when win_condition == "boss_killed")
2. **Add spawn position calibration:** current spawn at (3,26) creates the chase-out-of-leash dynamic; alternative spawn positions analyzed (e.g., adjacent to boss rather than arena edge); spatial-geometry math
3. **Boss-focus AI targeting logic:** when `win_condition in {"boss_killed", "mini_boss_killed"}`, player AI prioritizes boss/mini-boss over adds. Pseudocode + activation gate.
4. **Predicted re-sweep outcomes:** for each tier and 10-kit roster, predict per-tier WR under fix. Cross-reference Track C § 2.3 prediction + W0.9 math note §5.3 joint-resolution call.
5. **Joint-resolution empirical verification design:** after fix lands, re-run W0.9.6-equivalent calibration sweep. Verify whether high-modifier kits exit boss-zero floor (predicted via W0.9 + W0.1); low-modifier mage kits route to P2/P3 multi-dim convergence per math note §5.3.
6. **#13a-partition compliance:** boss-focus AI logic must partition on `win_condition` (mechanical encounter property), NEVER on substrate identity. Verify in implementation spec.

**Sub-task W0.10.2 — jack-ryan Gate-1 review of math note:**

Per recompose-hive P1 + W0.1/W0.2/W0.9 critique-pair precedent. Math note routes through jack-ryan Gate-1 BEFORE implementation. Standard amendment fold-in pattern.

**Sub-task W0.10.3 — gandalf architectural review of math note:**

Parallel to jack-ryan Gate-1. Architectural alignment review: "fix the arena, not the synergy" continuation + ARPG-canon thematic preservation + substrate-as-cohesion preservation (boss-focus is mechanical, not substrate-keyed).

**Sub-task W0.10.4 — Implementation (Phase 2):**

Files affected:
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (player AI targeting; player action phase)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (add spawn positions if calibration recommends)
- New tests in `tests/test_w010_boss_ai_focus.py`
- MIGRATION.md v1.29 entry per ADR-004 + Discipline #12 semantic shift

**Sub-task W0.10.5 — Re-run W0.9.6-equivalent calibration sweep:**

Verify per-tier WR outcomes match prediction. Per gandalf: P0 closes on architectural AND empirical commitments. Empirical verification is W0.10's load-bearing acceptance criterion.

**Sub-task W0.10.6 — jack-ryan Amendment 1 fold-in (caller-side wiring):**

Per jack-ryan W0.9 cumulative Gate-2 Amendment 1: `balance_loop.py` callers of `_run_spatial_slot()` in `_evaluate_class()` / `_evaluate_room_class()` / `_evaluate_variance_check()` don't yet pass a real `SqliteSpatialTelemetryWriter` or `GauntletArchive`. **Fold this into W0.10 scope** (since W0.10 re-sweep needs real DB emission anyway). Document the caller-side wiring; instantiate writer at call sites in calibration sweep script + production season runs.

**Sub-task W0.10.7 — Cumulative Gate-2:**

Standard critique-pair after implementation (gandalf architectural + jack-ryan DEV-MODE BLOCK-authority). When approved, fires `qd-rebuild/v0.10-boss-ai-leash-reset-fixed` final tag.

## Required reading before starting

- `reincarnated-engine/src/reincarnated/simulation/math/gauntlet-migration-arena-equivalence.md` (W0.9 math note; §5.3 joint-resolution call; §6 calibration sweep design)
- `agentic_orchestration/CHANGELOG.md` 2026-05-21 W0.9 Phase 2.5 entry — boss AI leash-reset bug empirical diagnosis
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` § 11.5 — "fix the arena, not the synergy" governance principle
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 2.3 — Track C joint-resolution prediction (currently BLOCKED by bug; will be re-tested post-fix)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — player AI targeting current state
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` — add spawn positions current state
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11.1 (state-space conditioning — applies to your re-sweep verification) + § 13a-partition (no substrate-keying)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — prior W0.9 Phase 2.5 record
- `scripts/w096_calibration_sweep.py` — your prior calibration sweep script (template for re-sweep)

## Math-before-code (Discipline #1; REQUIRED)

See Sub-task W0.10.1. Math note FIRST. jack-ryan + gandalf review BEFORE implementation. This pattern has held cleanly through W0.1 + W0.2 + W0.9 — repeat it for W0.10.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable for the bug fix itself** (player AI behavior change in spatial_engine.py is internal to simulation seam). Re-sweep will exercise existing v2.15 telemetry round-trip per W0.9 Phase 2.5 pattern.

**However, caller-side wiring (W0.10.6) DOES touch cross-seam:** balance_loop.py production callers need SqliteSpatialTelemetryWriter + GauntletArchive wiring. Document at MIGRATION.md v1.29 + verify production-path round-trip via re-sweep (which IS the smoke).

## Scope

- [ ] Math note authored (W0.10.1)
- [ ] jack-ryan Gate-1 + gandalf review (W0.10.2 + W0.10.3)
- [ ] Phase 2 implementation (W0.10.4)
- [ ] Re-run calibration sweep (W0.10.5)
- [ ] Caller-side wiring fold-in (W0.10.6; jack-ryan W0.9 cumulative Amendment 1)
- [ ] Cumulative Gate-2 (W0.10.7)
- [ ] MIGRATION.md v1.29 per ADR-004
- [ ] AGENT_STATE.md updated
- [ ] Tag: `qd-rebuild/v0.10-boss-ai-leash-reset-fixed`

## Acceptance criteria

- [ ] Boss AI boss-focus mode LIVE (player AI prioritizes boss when win_condition == "boss_killed" or "mini_boss_killed")
- [ ] Add leash semantics calibrated (no full HP reset cascading; OR add spawn positions tuned to prevent the chase-out-of-leash dynamic)
- [ ] Re-sweep verifies: high-modifier kits (≥0.30) exit boss-zero floor; low-modifier mage kits route to P2/P3 multi-dim convergence per math note §5.3
- [ ] Discipline #17 anomaly count: <10/50 (vs current 50/50)
- [ ] No regressions on prior tests (W0.9 sub-phases tests preserved)
- [ ] #13a-partition compliance: boss-focus AI logic partitions on win_condition (mechanical), NOT on substrate
- [ ] Cumulative Gate-2 critique-pair approved
- [ ] Tag fired

## Out of scope

- Multi-dim convergence implementation (P2/P3 territory; low-modifier mage path)
- B6+W0.1 verification re-sweep (requires B6 generation which is rocket territory; W0.1 Concern 1 carries to post-B6)
- Multi-tier archive insertion (jack-ryan W0.9 cumulative Amendment 2; routed to P1/P2)
- W0.7 ablations (separate workstream)
- Cohesion-judge integration (P5)

## Open questions for math note resolution

- **Boss-focus activation gate:** when `win_condition` is `"boss_killed"` only, OR also `"mini_boss_killed"`? Document choice + reasoning.
- **Add behavior under boss-focus:** do adds continue to threaten player (incidental damage) but player ignores them, OR do adds despawn / become non-aggressive? Per ARPG canon, adds typically threaten throughout; player focuses boss but takes incidental damage. Document.
- **Add spawn position calibration:** scope to all 3 new scenarios (MAGIC_PACK + ELITE_PACK + MINI_BOSS) OR only MINI_BOSS? Math note evaluates.
- **Leash semantics:** is the HP-reset-on-leash semantically correct for ANY tier, or does this surface a deeper convention question? D2 monsters don't HP-reset when leashed; D3 elites do; PoE varies. Math note resolves.

## Critique-pair structure

- **gandalf** reviews architectural alignment (math note Step 0 + Phase 2 close-out): "fix the arena" continuation; ARPG-canon preservation; substrate-as-cohesion preservation; #13a-partition compliance (win_condition partition, not substrate)
- **jack-ryan** reviews math correctness (Step 0) + implementation correctness (Phase 2 close-out): Discipline #11.1 cold-start verification; Discipline #17 calibration anomaly threshold; Discipline #12 semantic shift framing; #13a-partition implementation
- **knight-rider** folds verdicts into state-of-hive + decisions-log + CHANGELOG; fires final tag at acceptance

## Authorization

Per Matt's 2026-05-21 autonomous-operation directive: "You do not need my approval. The hive must move forward... Continue towards completion unless I intervene." gandalf Option A disposition (W0.10 as late-P0 workstream) IS the operative authorization. Knight-rider proceeds.

## References

- `agentic_orchestration/CHANGELOG.md` 2026-05-21 W0.9 Phase 2.5 + W0.9 cumulative Gate-2 entries
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11.1 (state-space conditioning; W0.9 Phase 2.5 is canonical example) + § 13a-partition
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` § 11.5 (governance principle)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 2.3 (joint-resolution prediction; BLOCKED until W0.10 ships)
- W0.9 math note + 5 sub-phase tags
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.9 (gauntlet architecture commitment; W0.10 framing addition recorded per gandalf Amendment 3)
