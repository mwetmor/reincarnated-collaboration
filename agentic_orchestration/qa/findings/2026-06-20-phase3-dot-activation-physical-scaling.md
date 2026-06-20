# Finding — 2026-06-20 — Phase 3 DoT activation + physical-DoT scaling (F3-DEFECT fix)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO
**Target:** `gamora/v-dot-activation-phase3-1` (engine `9e1d25d`, collab `573a3e1`)
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 4 (decisions-log/recompose-first), 6 (cross-seam round-trip); Disciplines #1, #3, #11, #12; instrument-validity KR brief §3 GATE G4
**Mode:** DEV-MODE Gate-2 (boundary 3 of 4: resource → rotation → DoT → mitigation)

## What I found

Phase 3 is a clean, well-scoped, recompose-first commit. Verified first-hand: HEAD == tag (no drift). The Phase-3 commit `9e1d25d` touches only `damage_resolver.py` (the `_add_or_refresh` F3-DEFECT fix, 27 lines), `spatial_engine.py` (the DoT-channel accumulator, 22 lines), the harness, and the two docs. F1 (DoT ticking, `spatial_engine.py:2003-2022`) and F2 (physical-DoT scaling via source attribute, `damage_resolver.py:1002-1018`) were committed at `e537b29` and are LIVE + correct on the current tree — NOT re-implemented here. The `0.003` coefficient is UNCHANGED (`:1017`) — no magnitude re-tune, faithful to recompose-first. The G4 smoke artifact is on disk (`dot-activation-phase3-G4-smoke-20260620_162359.json`) and corroborates every number in the math-note. 141 targeted refresh/dot/ailment/tick tests PASS. The 60 full-suite failures are causally disjoint from Phase 3 (Phase 3 touched no test files and none of the failing-test source areas).

### F3-DEFECT ruling (the headline item — scrutinized hardest): SOUND.

(a) **Faithful ARPG behavior, not invented.** The fix at `damage_resolver.py:1043-1051` makes DoT refresh keep `max(_old_tick, _new_tick)` for tick_damage while always refreshing duration. "A weaker re-apply must not weaken a live DoT" is a standard ARPG DoT-refresh rule — recompose-first, not a new mechanic. The diagnosis is correct and two-seam (Discipline #11): rocket's zero-tick T1 seed (`round(1²·0.3)=0`) × this seam's prior unconditional `existing.params = new_effect.params` last-writer-wins. The selector fires T1 ~22× per T4 (firing-count), so the live T4 bleed (tick=5) was being clobbered to 0 most of the time.

(b) **Correctly SCOPED to DoT refresh.** The max-preserving branch is gated `if new_effect.name in _DOT_AILMENT_NAMES:` (`:1044`); the `else` at `:1050` retains `existing.params = new_effect.params` (last-writer-wins) for non-DoT effects. No regression to debuff/buff/control refresh semantics. `_DOT_AILMENT_NAMES` is registry-derived (introduced `7ec1ff5`, predates this fix), so drain auto-included — not a hand-rolled set.

(c) **Actually resolves the zeroing.** G4 artifact (first-hand): the STR-bleed kit (`endgame_bc_melee_low_spiky_str_none_t4_chain_2`) fires bleed T4 (`tier_firing {"1":672,"4":36}`) and produces `sum_player_dot=182.28` on boss_with_adds → `str_bleed_boss_dot_dps=0.1008 > 0`. Pre-fix this measured exactly 0. Necessary and sufficient.

### Throttle-vs-magnitude framing: CORRECTLY framed (verified first-hand).

The STR/caster realized-DPS gap (0.10 vs 0.32, ratio 0.312) is throttle-driven, NOT a per-tick magnitude weakness and NOT caster over-performance. Evidence: per-tick magnitudes ARE symmetric (F2: tick_scale STR 1.24 vs INT 1.27, a 2.4% gap). The realized gap tracks the T4-firing-rate gap: STR fires bleed-carrying T4 at 5.2% of casts vs INT 12.8% (`str_t4_pct_boss`/`int_t4_pct_boss` in the artifact). 5.2/12.8 = 0.41, same direction as the 0.31 DoT-DPS ratio. This is the Phase-2 mana-default pool-starve re-expressed as DoT under-funding — the G4 "throttled-low (NOT zero)" condition. STR's real rage economy (Phase 6) is what funds spend-on-anchor bleed; the mana-default population borrows the wrong economy. Correctly framed as a mana-default instrument artifact.

### Finding-3 doc correction: CORRECT, and exposed-not-folded confirmed.

The `dps-measurement-instrumentation-2026-06-19.md` §1.1/§2/§3.1 "DoT folds into the per-hit float" error is corrected: original text retained for the historical record (marked PRE-F1, superseded), correction box added. Crucially, the no-double-count guarantee HOLDS by a new mechanism (two disjoint channels each summed once). The accumulator is EXPOSED, not folded: `dot_damage_dealt`/`dot_damage_received` are NEW separate `SpatialEntity` fields (`:544-552`); the `delivered_*` accumulators capture direct hits only and never see the DoT channel. Therefore NO existing delivered-DPS consumer's value shifts — confirmed.

### Semantic-shift continuity (Discipline #12): DECLARED and coherent.

Declared in the math-note §6, the `_add_or_refresh` docstring, the accumulator comment, the commit, and AGENT_STATE. This is the third of four boundaries (resource → rotation → DoT). The Phase-2→Phase-3 interaction is correctly identified as load-bearing: DoT non-zero is CONDITIONAL on Phase 2 firing T4 (zero-tick T1-only would still measure ~0). Composes coherently with Phases 1-2. Fourth boundary (Phase 4 mitigation) noted.

### Measure-isolated / no production-gate regression: CONFIRMED.

`bands_untouched: true` in the artifact; Phase 3 touched no band/gate source. Fresh disjoint seed base 16,000,000 (Discipline #3, clears all known-used bases). MIGRATION: harness-local accumulation, no `SpatialFightResult` schema change → no MIGRATION required (Principle 6 round-trip not applicable; correctly stated).

## Rationale

Recompose-first held (Principle 4 / brief §3): mechanism faithfully ported, `0.003` coefficient and `round(tier²·0.3)` seed both held, no magnitude tune. Math-before-code held (Principle 1 / Discipline #1): a thorough math-note precedes all code with sanity-bounded per-tick and full-fight estimates. Smoke-gate held (Principle 2): G4 smoke artifact on disk. F3-DEFECT diagnosis and fix exemplify Discipline #11 (empirical inspection, two-seam interaction) and #12 (semantic-shift framed not buried). G4 auto-resolves per the brief's pre-registered table (STR bleed > 0; symmetry is per-tick and holds; the realized gap is throttle, the named "throttled-low not zero" branch — not an escalate fork).

## INFO items (non-blocking; carried forward)

1. **[Phase-5 Gate-6] DoT-only-on-long-lived-targets property.** DoT-DPS ≈ 0 on fast-clear shells (open_arena/magic_pack/elite_pack) because low-HP adds die before the first 1.0s `DOT_TICK_INTERVAL` tick; non-zero only on boss_with_adds/mini_boss/chokepoint_corridor. Real tick-interval × kill-speed interaction (not a defect) — makes bleed a single-target-only tool by construction, which matches STR's substrate-assigned bleed intent. The Phase-5 magnitude decision should weigh this.

2. **[Phase-6 Gate-7] STR throttle = population artifact.** The STR DoT under-funding is the mana-default population borrowing the wrong economy, not a real STR weakness. Phase 6 (STR's native rage build-on-swarm/spend-on-anchor) is the honest read. Boss-FOCUS DoT ≈ 0 (player-AI bleeds the nearest swarm, not the anchor) is the STR anchor-gap itself — Phase 6 territory.

3. **[Cosmetic — INFO only] Stale population scope in two code comments.** The F1 comment (`spatial_engine.py:1997-1998`) and the F2 comment (`damage_resolver.py:1000`) say "0/66 carry tick_damage (season-001 population)". The math-note §1 says the HARNESS `build_population()` carries 25/66 with non-zero tick. These are two DIFFERENT populations (shipping season-001 legendaries fed to the production gate = 0/66; the BC-archetype sim population the harness builds = 25/66) — not a contradiction, and the harness measurements are valid. Suggest a one-line clarification in those comments at a future touch so a future reader doesn't mistake "0/66" for the harness population. Not blocking.

4. **[Out-of-scope — confirmed not Phase 3] 60 pre-existing test failures.** Confirmed out-of-seam: `test_foundation.py`/`test_substrate_identity_loader.py` (5-element vs 7-substrate config drift, rocket seam), `test_wave5...cohesion_judge` (LLM auth, star-lord/env), `test_cycle12_layer4_convergence.py` (convergence dataclass shape). Phase 3 touched NO test files and NONE of these source areas (verified by `git diff --name-only e2f3929 9e1d25d`). NOT introduced by Phase 3; NOT a Phase-3 BLOCK. Rocket-seam standing item.

## Action

- [x] jack-ryan: Gate-2 PASS-WITH-INFO — F3-DEFECT max-preserving change ruled SOUND (faithful, scoped, effective).
- [ ] gamora (optional, future touch): clarify the "0/66" population scope in the F1/F2 code comments (INFO #3).
- [ ] gandalf: carry INFO #1 + #2 to the Phase-6 STR-lever disposition and Phase-5 magnitude decision.
- [ ] Matt: no decision needed at this gate (measure-isolated, bands untouched). Band approval is Phase-5 (GATE G6).

## References

- `reincarnated-engine` `9e1d25d` (tag `gamora/v-dot-activation-phase3-1`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:1002-1018` (F2), `:1024-1052` (`_add_or_refresh` F3-DEFECT fix), `:60-62` (`_DOT_AILMENT_NAMES`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:544-552` (accumulator fields), `:2003-2022` (F1 tick + accumulator)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/dot-activation-physical-scaling-phase3-2026-06-20.md` (math-note)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/dps-measurement-instrumentation-2026-06-19.md` (F3 doc correction)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/dot_activation_phase3_harness_2026_06_20.py` (G4 harness)
- `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/dot-activation-phase3-G4-smoke-20260620_162359.json` (G4 artifact)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` §3 GATE G4
