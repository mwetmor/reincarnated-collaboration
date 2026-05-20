# Option B Design Brief — Recompose-Trigger Re-conditioning (P1)

**Version:** v1.1 (amended 2026-05-19 by gandalf post smoke-B1-FRICTION re-disposition; see § 4.1 retrospective, § 4.4 BLOCKING-semantics tightening, § 9 soft-disable elevation, and v1.1 amendment note at § 0)
**Author:** gandalf (story-and-design steward)
**Authority:** AUTONOMOUS L2-equivalent per engine-rebuild protocol § 4.0 + recompose-validation hive (Architectural / load-bearing cross-cutting decisions — gandalf decides; no escalation).
**Date:** 2026-05-19 (same evening as P0 acceptance; amended same day)
**Hive:** Recompose-Validation (third activation; P1)
**Predecessor:** `agentic_orchestration/dispatches/2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` (P0, landed in `recompose-hive/v0.1-option-a-floor-widened`)
**Triggering hive handoff:** `agentic_orchestration/hive-mind/recompose-validation-log.md` entry `2026-05-19 23:00 EDT — knight-rider HANDOFF — P1 design brief AUTHORING ROUTED TO GANDALF`
**Re-disposition handoff:** `agentic_orchestration/hive-mind/recompose-validation-log.md` entry `2026-05-19 EDT — knight-rider HANDOFF — P1 smoke-B1-FRICTION RE-DISPOSITION ROUTED TO GANDALF` (gamora cold-start exposed class_0001's true `m* ≈ 0.072`; smoke B1 conditions 1+2 BLOCKING-failed; mechanism mechanically verified by unit tests; this is a test-class-selection issue, not a mechanism defect)
**Next routing:** jack-ryan Gate-1 critique → knight-rider authors gamora implementation dispatch from this brief + jack-ryan amendments.

---

## v1.1 amendment note (2026-05-19, post smoke-B1-FRICTION)

The v1.0 brief routed through jack-ryan Gate-1 (APPROVE-WITH-AMEND; 4 required + 1 recommended + 1 optional amendments folded) and gamora implementation (179/179 tests PASS; mechanism mechanically verified). Smoke gate B1 BLOCKING failed on class_0001 cold-start because the test class's true equilibrium `m* ≈ 0.072` is *above* `MODIFIER_SEARCH_FLOOR=0.01` — class_0001 is NOT in the masked-Pattern-B-extreme population the smoke was designed to test. The v1.0 brief's § 4.1 rationale for selecting class_0001 leaned on its warm-start signature (`modifier=0.0509` + saturated WR); that signature is a TOLERANCE-satisfied-at-old-floor artifact, not a true `m* < 0.01` equilibrium.

**v1.1 amendments (substance):**
- **§ 4.1:** explicit retrospective on the warm-start-signature error; correction that cold-start dry-run is mandatory before any future canonical smoke test class is locked in.
- **§ 4.4:** BLOCKING semantics tightened — "BLOCKING fails when smoke conditions fail AND post-hoc analysis confirms the test class actually has the property the smoke was designed to detect." When post-hoc analysis shows the test class doesn't have the property, disposition is *test-design failure*, not *mechanism failure*; proper response is soft-disable + re-route empirical question to natural venue (P2 full-season regen).
- **§ 9:** Reversibility option 2 (soft-disable via `LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR`) elevated from "alternative" to "preferred path when smoke fails due to test-class-selection issues." The full-revert path (option 1) is reserved for cases where the mechanism itself is independently invalidated, not for test-class-selection misses.

**v1.1 disposition:** Option B is MECHANICALLY COMPLETE / BEHAVIORALLY SOFT-DISABLED. Hive milestone tag `recompose-hive/v0.2-option-b-recompose-conditioned` HELD pending P2 empirical verification. Intermediate seam tag `gamora/v1.14-balance-loop-option-b-recompose-conditioned-soft-disable` fires under autonomous L1 once gamora applies the one-line constant change. Full STATE entry: hive log `2026-05-19 EDT — gandalf STATE — P1 smoke-B1-FRICTION RE-DISPOSITION: OPTION 2 (SOFT-DISABLE)`.

---

## § 0 — TL;DR

The recompose trigger fires correctly post-Option-A. What does *not* fire for the most extreme kits is the *lever signal*: `_quick_modifier_estimate` can exit at modifier near the new floor (0.01) but with `last_wr` still pinned at the WR ceiling (~0.95-1.00) — because the kit's true equilibrium modifier is below the binary-search floor altogether. At that exit state, lever deltas are 0.0 by the same mechanism gamora diagnosed pre-Option-A: any DPS perturbation gets absorbed by the WR ceiling.

**Option B's job:** detect "floor-lock-post-Option-A" (the binary search bottomed out *and* signal range was never reached) and force lever evaluation at a *sub-floor working modifier* where the kit is actually sensitive to DPS changes. The signal is **`last_wr > _SIGNAL_HI`** (i.e., the quick estimate exited still saturated), NOT `eval_modifier < floor + epsilon` (which is post-hoc-ambiguous; a class can land at-floor with WR=0.5 perfectly legitimately).

**Working modifier under floor-lock-detected:** fixed `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005` (half the new floor). This is a single-shot, simple, predictable widening of the lever-evaluation domain *only* — the binary search retains MODIFIER_SEARCH_FLOOR=0.01 as its bound. No discontinuity in convergence semantics; only an internal probe value the levers use to find traction.

**Smoke gate B1:** on class_0001 from season_100002 (the canonical floor-locked test class), post-Option-B run must show (a) `floor_lock_detected=True` in recompose_attempts telemetry, (b) lever evaluations executing at `working_modifier=0.005` with `before_winrate < 0.95` (signal reachable), (c) at least one lever produces `|delta| ≥ RECOMPOSE_DELTA_FLOOR=0.02`, (d) post-recompose binary search converges with `final_modifier > 0.01` (kit DPS density reduced — class no longer pinned at floor).

**Departure from gamora § 5.2:** the proposed re-condition signal `eval_modifier ≤ floor + epsilon` is replaced with `last_wr > _SIGNAL_HI`. Rationale in § 2.3. The departure is principled, not adversarial — gamora's framing conflated "binary search bottomed out" with "lever evaluation has no signal," which are different states.

**Scope discipline:** no bidirectional levers (B-prime). No new architectural surface. Surgical sharpening of the existing composition lever; the recompose-hive's central premise.

---

## § 1 — Required reading (for downstream agents)

**jack-ryan (Gate-1 critique):**

1. This brief in full.
2. `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md` § 4 (mechanism + signal-range trap) and § 5.2 (gamora's Option B framing — the proposal this brief departs from in one named place).
3. `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` lines 1288-1407 (`_quick_modifier_estimate` + `_primary_recompose_loop`).
4. `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.21 (the named-constant + semantic-shift conventions established by Option A; v1.22 follows the same template).
5. `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 11.6 (sign-off conditions; specifically condition 5 — "B's design brief addresses kits that even Option A cannot converge" — which this brief operationalizes).

**gamora (implementation, after Gate-1):**

1-4 above, plus:
5. `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md` § 2 (P1 acceptance gate definition).
6. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` Disciplines #1, #2, #11, #12, #18.

**star-lord (telemetry consumer):**

1. § 5 of this brief (cross-seam impact).
2. MIGRATION.md v1.22 once authored.

---

## § 2 — The math: recompose-trigger signal-range analysis

### § 2.1 — State of the world post-Option-A

`MODIFIER_SEARCH_FLOOR = 0.01` (was 0.05). Binary search bounds `[0.01, 4.0]` at four sites in `balance_loop.py` (verified MIGRATION.md v1.21).

`_quick_modifier_estimate` (line 1288) uses the same bounds and exits when *either* (a) RECOMPOSE_QUICK_ITERS=10 iterations exhausted, *or* (b) `_SIGNAL_LO=0.30 <= last_wr <= _SIGNAL_HI=0.70` (early-exit at signal range).

For a kit whose true WR=0.5 equilibrium modifier `m*` is *within* the new bounds (i.e., `0.01 ≤ m* ≤ 4.0`), the adaptive estimate converges into the signal range on average within 3-5 iterations. Levers evaluate at `eval_modifier ≈ m*` where `WR ∈ [0.30, 0.70]`. DPS-perturbation levers produce meaningful deltas (typical ~0.03-0.10). Recompose works as designed. **This is the unblocked case Option A unlocks for the 22 Pattern-B classes (44.9% of catalogue per Phase B.2).**

For a kit whose true WR=0.5 equilibrium modifier `m* < 0.01` (below the new floor), the adaptive estimate cannot reach `m*`. The search narrows toward the floor, `high` keeps decreasing, but `last_wr` stays at the ceiling (~0.95-1.00) because the kit dominates the gauntlet at every modifier ≥ 0.01. The estimate exits via RECOMPOSE_QUICK_ITERS exhaustion (not early-exit) with `eval_modifier ≈ 0.01 + ε` and `last_wr ≈ 0.95-1.00`. **This is the floor-lock-post-Option-A case. Some unknown subset of the 22 Pattern-B classes — and potentially some of the 27 Pattern-A classes if their boss-WR-zero pattern is in fact masked by lower-tier saturation — fall here.**

### § 2.2 — Why the trigger fires but the levers fail

The recompose direction trigger at line 1356:

```python
if eval_modifier < MODIFIER_LOW_THRESHOLD:   # 0.0101 < 0.30 → True
    reduce_dps = True
```

— fires correctly. `reduce_dps=True` is set. Levers loop.

Inside each lever (e.g., `_lever_skill_swap` lines 1664-1675), the swap is evaluated with the *same* `eval_modifier` value the recompose loop received:

```python
new_wr, _, _, _ = self._evaluate_class(player_class, gauntlet, fights_per_matchup, eval_modifier)
delta = new_wr - current_wr
if reduce_dps:
    accepted = delta < -RECOMPOSE_DELTA_FLOOR
```

At `eval_modifier ≈ 0.0101`, `current_wr ≈ 0.99`. Any DPS-reducing swap produces `new_wr ≈ 0.99` as well — the kit still saturates the gauntlet. `delta ≈ 0.0`. Lever rejected. All three levers fail for the same reason. `total_accepted = 0`. `_primary_recompose_loop` returns `(False, eval_modifier)`. The class proceeds to the rejection-gate-and-binary-search path (line 916) which converges at the floor — `status=converged` (Option A's gift) but with no kit composition change. **The kit is the same broken kit; the floor is just wider.**

This is the *same* signal-range trap gamora's § 4.3 diagnosed pre-Option-A — only now with the floor at 0.01 instead of 0.05. **Option A is necessary but not sufficient.** Option B closes the architectural gap.

### § 2.3 — The re-condition signal: `last_wr > _SIGNAL_HI`, not `eval_modifier ≤ floor + ε`

Gamora's investigation § 5.2 proposed:

> When `_quick_modifier_estimate` returns `eval_modifier <= low + epsilon` (i.e., the estimate bottomed out at the floor), the primary recompose loop should attempt levers at a *lower working modifier*…

The activation prompt to me reified this as `status=failed AND eval_modifier ≤ MODIFIER_SEARCH_FLOOR + epsilon`. I depart from this framing in one named place, and the departure matters.

**Two reasons:**

**(1) Code-architecture mismatch.** `_primary_recompose_loop` runs *before* binary search. At lever-evaluation time, `status=failed` is not yet observable — that's a post-binary-search state. The activation prompt's framing conflates a pre-recompose signal with a post-binary-search outcome. The correct pre-recompose signal must be derivable from `_quick_modifier_estimate`'s direct output.

**(2) `eval_modifier ≤ floor + ε` is post-hoc-ambiguous.** A class can land at `eval_modifier=0.012` *with `last_wr=0.45`* — meaning the quick estimate found signal-range right at the new floor. This is a *legitimate convergence* (a kit whose true `m*` is just barely above the floor); we do NOT want to re-invoke levers at sub-floor working modifier for this class. The `eval_modifier ≤ ε` test would false-positive here.

The unambiguous signal is **`last_wr` at exit from `_quick_modifier_estimate`**. The quick estimate has early-exit at `[_SIGNAL_LO, _SIGNAL_HI] = [0.30, 0.70]`. When the estimate exits via this early-exit, `last_wr` is in `[0.30, 0.70]` and levers will have signal at `eval_modifier`. When the estimate exits via iteration exhaustion (the "couldn't find signal" case), `last_wr` is either `> _SIGNAL_HI` (kit too strong at floor) or `< _SIGNAL_LO` (kit too weak at ceiling).

**Re-condition signal: `last_wr > _SIGNAL_HI`.** This is the precise floor-lock-post-Option-A failure mode. It has no epsilon. It does not depend on the specific floor value. It is symmetric: a future B-prime extension for ceiling-locked classes (kits too weak even at modifier=4.0) would use `last_wr < _SIGNAL_LO` — same code template, opposite sign.

**Diabolic-design-history sidebar.** This is the same lesson Path of Exile internalized over its first decade. GGG's damage system uses internal multipliers that route through several layers; when one layer's range constraint clipped the input to a downstream layer, the bug was diagnosed as "the multiplier doesn't update" — but the truer framing was "the *signal* the multiplier needs to consume is being clipped." The fix was always to widen the signal range, not to add epsilon to a value check. Same shape here.

### § 2.4 — Working-modifier choice under floor-lock-detected

The investigation suggested `working_modifier = 0.025` (literally below the prior floor of 0.05 but above the new floor of 0.01). With Option A landed, that value sits *within* the binary search range, which creates a semantic discontinuity: levers would evaluate at a modifier the binary search itself can also reach, but with different intent.

**Cleaner design: `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005` — fixed, below the search floor, named constant per Discipline #18.**

Three reasons:

**(1) Domain separation.** 0.005 is below `MODIFIER_SEARCH_FLOOR = 0.01`, so the lever-evaluation working modifier is unambiguously *not* a value the binary search will ever converge to. The lever is using it as a *probe* — "at what DPS level does this kit start losing fights?" — not as a candidate equilibrium. This is semantically clean and matches the Pattern of Exile / Diablo II "internal scaling vs displayed value" distinction (gandalf disposition § 11.4 Read 2): the working modifier is plumbing; the user-facing modifier remains constrained to `[0.01, 4.0]`.

**(2) Sufficient signal range.** At `working_modifier = 0.005`, even an extreme over-powered kit's effective DPS is 0.5% of baseline. For ~all observed floor-locked R8 inverted kits, this drops WR into measurable range (typically WR < 0.95). The signal range is `_SIGNAL_LO ≤ wr ≤ _SIGNAL_HI` for clean lever evaluation, but levers only need `wr` below the WR ceiling for delta to be non-zero — meaning *any* working modifier where the kit is sensitive to DPS will do.

**(3) Deterministic, no extra fight evaluations.** A fixed value adds zero runtime cost beyond the lever evaluations themselves (which already run). Alternative designs (adaptive probe; double-bisection; widened signal range) add 5-10 extra fight evaluations per floor-locked class — meaningful at scale.

**Risk: what if `working_modifier=0.005` is *still* not low enough for some kit?** If a kit wins 100% at modifier=0.005, the kit is not floor-locked — the kit is *fundamentally* over-armed; no DPS reduction available to the lever library can balance it. This is no longer a balance-loop problem; it is a kit-redesign-queue problem. Smoke gate B1 will detect this case (all levers rejected even at working_modifier=0.005); the disposition is "kit-redesign flag" and the class is excluded from the floor-lock-recovery population. This is the architectural floor of what levers can do; no further recourse exists short of regenerating the kit from scratch.

### § 2.5 — Predicted-outcome math (Phase B.2 Pattern A/B carve)

From CHANGELOG Phase B.2 finding:
- **22 classes / 44.9%** are Pattern-B (latent boss-kill capability gated by floor). Post-Option-A, these classes should converge naturally if their `m*` is `≥ 0.01`. *Most* of the 22 should be served by Option A alone — they are not floor-lock-detected post-Option-A (`last_wr` lands in signal range).
- **27 classes / 55.1%** are Pattern-A (kit-composition pathology; boss WR = 0 at all modifiers ≤ 2.0). These classes are the open empirical question. The brief's central prediction: an unknown fraction of these are *not* truly Pattern-A but are *masked* Pattern-B-extreme cases — their boss-WR-zero pattern is downstream of lower-tier saturation that pins the binary search at floor. Option B addresses this masked subset.

**Predicted disposition per population:**

| Population | Pre-Option-A | Post-Option-A | Post-Option-B (this brief) |
|---|---|---|---|
| Pattern-B (22 classes, `m* ∈ [0.01, 2.0]`) | status=failed at floor | status=converged | Same — levers had signal at `eval_modifier` already |
| Pattern-B-extreme (subset, `m* < 0.01`) | status=failed at floor | status=converged at floor, kit unchanged | floor_lock_detected=True; levers run at 0.005; recompose actually fires |
| Pattern-A (27 classes, boss-zero structural) | status=failed at floor / mixed | status=converged at floor with boss=0 | Lever attempts at 0.005; most still fail → flagged kit-redesign |

The "masked Pattern-B-extreme" subset is the population this brief specifically serves. Its size is the empirical question P2 will answer. Conservatively: expect 3-8 classes from across both Pattern-A and Pattern-B populations to be in this floor-lock-recovery population for a typical season.

---

## § 3 — Implementation scope

### § 3.1 — Where the re-condition lives in `balance_loop.py`

**Single touch site: `_primary_recompose_loop` at line 1323.**

The current logic at lines 1351-1365:

```python
eval_modifier, current_wr = self._quick_modifier_estimate(
    player_class, gauntlet, fights_per_matchup, target_winrate
)

# Determine recompose direction from modifier magnitude
if eval_modifier < MODIFIER_LOW_THRESHOLD:
    reduce_dps = True
    increase_dps = False
elif eval_modifier > MODIFIER_HIGH_THRESHOLD:
    reduce_dps = False
    increase_dps = True
else:
    reduce_dps = False
    increase_dps = False
```

The proposed addition: after `_quick_modifier_estimate` returns, check `current_wr > _SIGNAL_HI`. If True, the estimate failed to reach signal range — we are in floor-lock-post-Option-A. Set a `floor_lock_detected` flag, override `working_modifier` for the lever loop, and re-evaluate `current_wr` at the new working modifier.

**Pseudocode for the proposed addition:**

```python
eval_modifier, current_wr = self._quick_modifier_estimate(
    player_class, gauntlet, fights_per_matchup, target_winrate
)

# ── Option B (2026-05-19): floor-lock-post-Option-A detection ─────────
# If _quick_modifier_estimate could not reach signal range at the search
# floor, lever evaluation needs a sub-floor working modifier to find
# DPS-sensitivity. Otherwise levers run at a saturated WR ceiling and
# all deltas are 0.0 (the trap diagnosed pre-Option-A; persists post-A
# for kits whose true m* < MODIFIER_SEARCH_FLOOR). See Discipline #12
# semantic-shift framing in MIGRATION.md v1.22.
_QUICK_SIGNAL_HI = 0.70  # mirror of _SIGNAL_HI in _quick_modifier_estimate
floor_lock_detected = current_wr > _QUICK_SIGNAL_HI
working_modifier = eval_modifier
if floor_lock_detected:
    working_modifier = LEVER_FLOOR_LOCK_WORKING_MODIFIER  # 0.005
    # Re-evaluate WR at the sub-floor working modifier so levers see the
    # real baseline they will be measured against.
    current_wr, _, _, _ = self._evaluate_class(
        player_class, gauntlet, fights_per_matchup, working_modifier
    )

# Determine recompose direction from modifier magnitude (UNCHANGED).
# Direction logic uses eval_modifier (the search-space value), not
# working_modifier (the probe value). This preserves the semantic that
# direction reflects where the binary search wants to go.
if eval_modifier < MODIFIER_LOW_THRESHOLD:
    reduce_dps = True
    increase_dps = False
elif eval_modifier > MODIFIER_HIGH_THRESHOLD:
    reduce_dps = False
    increase_dps = True
else:
    reduce_dps = False
    increase_dps = False
```

Then the lever loop at line 1374 uses `working_modifier` (not `eval_modifier`) when calling each lever:

```python
for lever_name, lever_fn in levers:
    for attempt in range(1, RECOMPOSE_MAX_ATTEMPTS + 1):
        accepted, new_wr, specifics = lever_fn(
            player_class, gauntlet, fights_per_matchup,
            working_modifier, current_wr, reduce_dps, increase_dps,
        )
        # ... record attempt; specifics now includes working_modifier separately from eval_modifier
```

And `recompose_attempts.append({...})` (line 1382) gains two fields:

```python
"eval_modifier": round(eval_modifier, 4),           # unchanged
"working_modifier": round(working_modifier, 4),      # NEW — equal to eval_modifier unless floor_lock_detected
"floor_lock_detected": floor_lock_detected,          # NEW — bool
```

### § 3.2 — Named constant (Discipline #18)

A new module-level constant near line 73 (next to `MODIFIER_LOW_THRESHOLD`):

```python
# ── Option B floor-lock recovery (2026-05-19) — Discipline #18 named constant ─────
# Sub-floor working modifier used by recompose levers when _quick_modifier_estimate
# could not reach signal range (last_wr > _SIGNAL_HI=0.70) at the search floor.
#
# Rationale: Option A widened MODIFIER_SEARCH_FLOOR to 0.01, but for kits whose
# true WR=0.5 equilibrium modifier is below the floor, the lever evaluation at
# eval_modifier ≈ 0.01 still sees WR at the ceiling (1.00) → all lever deltas
# are 0.0 → all levers rejected → recompose fails despite trigger firing
# correctly. This is the same signal-range trap from pre-Option-A, persisting
# for the sub-floor-m* sub-population.
#
# Design: levers evaluate at a fixed sub-floor probe value (0.005, half the
# search floor) only when floor_lock_detected. The binary search bounds are
# unchanged; this constant only affects what working modifier the LEVERS use
# when measuring DPS-sensitivity. The class's final_modifier remains constrained
# to [MODIFIER_SEARCH_FLOOR, MODIFIER_SEARCH_CEILING].
#
# Semantic shift (Discipline #12): the recompose trigger's effective signal
# range expands. Previously: "eval_modifier < MODIFIER_LOW_THRESHOLD" was the
# only direction signal. Now: floor-lock-detection adds a second branch where
# the working modifier diverges from eval_modifier to enable lever traction.
# This is documented in MIGRATION.md v1.22.
#
# Reversibility: revert by either (a) setting LEVER_FLOOR_LOCK_WORKING_MODIFIER
# = MODIFIER_SEARCH_FLOOR (which disables the divergence — working modifier always
# equals eval_modifier) or (b) removing the floor_lock_detected branch entirely.
# No persistent data depends on this value. Reversion produces convergence
# outcomes identical to Option-A-only (status=converged at floor with unchanged
# kit composition for floor-locked-post-A classes).
#
# See: decisions-log 2026-05-19 entry (Option B); MIGRATION.md v1.22;
# balance-loop-floor-investigation-2026-05-19.md § 4.3 + § 5.2;
# 2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md § 2.4.
LEVER_FLOOR_LOCK_WORKING_MODIFIER: float = 0.005
```

### § 3.3 — Telemetry surface

`recompose_attempts` (the list appended to `player_class.balance_metadata["recompose_attempts"]` and surfaced in `convergence_report`) gains two per-attempt fields documented above (`working_modifier`, `floor_lock_detected`). Existing field `eval_modifier` is **unchanged in semantics** — it remains the value `_quick_modifier_estimate` returned. The new field `working_modifier` is what the lever actually used. When `floor_lock_detected=False`, the two are equal.

`ClassBalanceResult` gains a new top-level boolean:

```python
floor_lock_recompose: bool | None = None   # True if Option-B floor-lock-recovery fired
```

Default `None` for backward-compat with pre-Option-B results.

### § 3.4 — LOC + scope estimate

- `balance_loop.py` recompose loop: ~30 LOC (the proposed addition + telemetry threading)
- `balance_loop.py` named constant + docstring: ~25 LOC
- `ClassBalanceResult` dataclass field: 1 LOC
- Test additions (unit-level: floor-lock detection branch coverage): ~30 LOC in `tests/test_balance_loop.py`
- MIGRATION.md v1.22 entry: ~80 LOC

**Total: ~165 LOC.** Within gamora's § 5.2 estimate of 25-50 LOC for the implementation proper; total scope (including telemetry + tests + MIGRATION) lands at the higher end of the original estimate.

**HARD scope-bounds (per knight-rider handoff and recompose-hive scope-of-work § 4):**

- No bidirectional levers (DPS-increase forced working modifier for ceiling-lock cases). B-prime scope; not P1.
- No new lever types beyond skill_swap / geometry_mix / cooldown_energy.
- No changes to b6_kit_builder (rocket's seam).
- No changes to `_quick_modifier_estimate` internal logic — only its callsite consumption changes.
- No changes to binary search bounds — Option A is settled.

---

## § 4 — Smoke gate B1 design (the falsifying experiment)

### § 4.1 — Test class selection

> **v1.1 RETROSPECTIVE (2026-05-19):** the v1.0 rationale below was partially wrong. Class_0001's warm-start signature (`modifier=0.0509` + saturated WR) was interpreted as evidence of true equilibrium `m* < MODIFIER_SEARCH_FLOOR`. Cold-start under Option B exposes class_0001's true `m* ≈ 0.072`, well *above* floor. The warm-start signature was a TOLERANCE-satisfied-at-old-floor artifact: warm-starting from `modifier=0.0509` satisfied convergence TOLERANCE immediately at the pre-Option-A floor without the binary search descending into the signal range. Symptom-driven test selection conflated "binary search bottomed out at floor with WR-saturation" (the symptom) with "true equilibrium below floor" (the cause). The symptom appears for both Pattern-B-extreme classes AND for any-`m*` classes warm-started from prior-floor convergence; the v1.0 smoke design did not distinguish these.
>
> **Discipline #11 (empirical inspection over assumption) applies retroactively.** A cold-start dry-run on class_0001 *before* locking it in as the canonical B1 subject would have surfaced `m* ≈ 0.072` and disqualified it. This is now mandatory smoke-design discipline: **for any future smoke designed to test a population-membership property, the candidate test class must be confirmed (via dedicated empirical dry-run) to have the property the smoke is designed to detect, before the smoke is locked in as BLOCKING.** The discipline goes into the engineering-disciplines record as an extension to Discipline #11.
>
> The remainder of this section preserves the v1.0 rationale as the historical record + correction context.

**Primary B1 test class (v1.0; superseded by v1.1 retrospective): class_0001 (fire_mage) from season_100002 (ember).** Rationale:

- Pre-Option-A: status=failed at modifier=0.0509 with all per-tier WR at ceiling (per gamora investigation § 3.2).
- Post-Option-A stop-gap regen: `modifier_extreme_low=0` warm-started in (per gamora P0 STATE 2026-05-19) — the cold-start case is the binding test, but class_0001's profile suggests it is in the "true m* < 0.01" population. *[v1.1: this inference was wrong — cold-start reveals `m* ≈ 0.072`.]*
- Already canonical test class for P0 A1 smoke gate (FAILED→CONVERGED demonstrated). Continuity of test surface. *[v1.1: continuity was the wrong selection criterion; population-membership confirmation is the right one.]*
- fire_mage is the modal R8 inverted archetype: high damage density, wide skill pool. Behavior on this class is broadly representative. *[v1.1: representativeness for general behavior is not the same as representativeness for the *specific* property the smoke tests. class_0001 is broadly representative AND not in the masked-Pattern-B-extreme population.]*

**Secondary B1 test classes (WARN-level, not BLOCKING; v1.0):**

- class_0003 (earth_controller) from season_100002: the *partial-over-power* case per gamora § 3.3 (modifier=0.0500 exact, boss WR=0.00). Tests Option B's behavior on a class where lower-tier saturation drives the floor-lock but boss-tier failure is from a different mechanism (energy-cycle on tanky boss). Expected outcome: lever evaluation runs at working_modifier=0.005; lower-tier WR drops into signal range; lever picks reduce_dps direction; some lever accepts on a swarm/magic-tier kit; binary search re-converges at modifier above floor. Boss-tier failure may persist (genuinely orthogonal); flag as kit-redesign candidate. *[v1.1 empirical: class_0003 cold-start `final_modifier=0.2575`, `floor_lock_recompose=False` — class_0003 is also above-floor, not floor-lock-recovery population. Same warm-start artifact pattern as class_0001.]*
- class_0006 (fire_controller) from season_100002: similar to class_0003 but different element. Robustness check. *[v1.1 empirical: `final_modifier=0.1338`, same above-floor pattern.]*

**v1.1 forward-looking smoke-design discipline (the lesson):**

Any future smoke gate that tests a population-membership claim (e.g., "this class is in the masked-Pattern-B-extreme population") must include a **pre-lock empirical confirmation step**: a dedicated cold-start dry-run on the candidate test class, in the post-fix configuration, to confirm the candidate has the property the smoke is designed to detect. The cost is small (~5 min per candidate) and the cost-of-not-doing-it is the FRICTION we are now resolving. The discipline extends Discipline #11 (empirical inspection over assumption) into smoke-design specifically: empirical confirmation of the *test subject* is itself a pre-condition for empirical validity of the *test*.

### § 4.2 — B1 BLOCKING acceptance condition (class_0001)

All four of the following must hold (verified via `recompose_attempts` telemetry on class_0001 cold-start convergence with Option B active):

| # | Condition | Verification |
|---|---|---|
| 1 | `floor_lock_detected=True` recorded in at least one recompose_attempt | Direct field check on serialized telemetry |
| 2 | At least one recompose_attempt has `working_modifier=0.005` (i.e., LEVER_FLOOR_LOCK_WORKING_MODIFIER) | Direct field check |
| 3 | At least one recompose_attempt has `before_winrate < 0.95` AND `accepted=True` AND `\|delta\| ≥ RECOMPOSE_DELTA_FLOOR=0.02` | The lever found traction (signal reached) AND was accepted (kit shaped) AND delta exceeds the meaningfulness floor |
| 4 | post-recompose binary search final convergence: `final_modifier > MODIFIER_SEARCH_FLOOR` AND `modifier_extreme_low=False` (i.e., `final_modifier ≥ 0.05`) | Recompose reduced the kit's DPS density enough that the class no longer needs sub-0.05 modifier |

**All four BLOCKING. Any one fails → P1 rolls back.**

Condition 4 is the *hardest* and the most important. Conditions 1-3 verify the mechanism fires; condition 4 verifies the mechanism *works* — that the recompose actually moved the kit into a healthier modifier range.

### § 4.3 — WARN-level conditions (class_0003, class_0006)

WARN-level conditions (do not block P1 acceptance but inform P2 substrate choice and Pattern-A/B disposition):

| Condition | Verification |
|---|---|
| At least one lever produces non-zero delta at working_modifier=0.005 | direct |
| If recompose succeeds and binary search converges with `final_modifier > 0.01`, count toward "Option B effective" population | direct |
| If recompose succeeds but boss-tier WR still fails post-convergence, flag as "kit-redesign candidate (boss-tier orthogonal)" | per-tier WR check |
| If recompose fails (no lever accepted at working_modifier=0.005), flag class as "Pattern-A confirmed (lever-irrecoverable)" | direct |

### § 4.4 — Falsifying condition (the P1 rollback trigger)

> **v1.1 BLOCKING-SEMANTICS TIGHTENING (2026-05-19):** the v1.0 falsifying conditions below are partially superseded. The literal reading "smoke B1 BLOCKING fails → P1 rolls back" is too coarse: it treats *mechanism failure* and *test-design failure* as the same disposition. They are not. The v1.1 reading distinguishes:
>
> | Failure mode | Diagnosis | Disposition |
> |---|---|---|
> | Smoke fails AND test class is empirically confirmed (via independent cold-start analysis) to have the property the smoke is designed to detect AND mechanism cannot be verified by unit tests | Mechanism is wrong | Full revert (option 1) |
> | Smoke fails AND test class is empirically confirmed NOT to have the property the smoke is designed to detect | Test-design failure | Soft-disable (option 2) + re-route empirical question to natural venue (P2) + brief amendment + new smoke-design discipline |
> | Smoke fails AND mechanism IS verified by unit tests AND test-class population membership is ambiguous | Underspecified disposition; surface to gandalf for re-disposition | Hold tags; re-disposition |
>
> The P1 smoke-B1-FRICTION (2026-05-19) falls in the second row. Disposition: soft-disable, this brief amendment (v1.1), and re-route empirical question to P2. **The v1.0 "literal BLOCKING → full revert" reading is retired as overly literal.** Gandalf's authority to re-dispose on the *meaning* of a BLOCKING failure is explicit per the autonomous-operation framework (engine-rebuild protocol § 4.0).
>
> v1.0 conditions retained below as historical record + base contract for future smoke gates that *do* have empirically-confirmed test classes.

**P1 rolls back if any of the following (v1.0; superseded by v1.1 distinction above for the test-class-selection failure mode):**

1. **Smoke gate B1 BLOCKING fails on class_0001** (any of the four BLOCKING conditions above misses). Implication: the design diagnosis is wrong; the working-modifier-at-0.005 mechanism does not unlock lever signal. *[v1.1: this implication only holds when class_0001 is empirically confirmed to be in the masked-Pattern-B-extreme population. The 2026-05-19 cold-start finding disconfirms class_0001's membership; the implication does not apply; disposition is test-design failure, not mechanism failure.]*
2. **B1 passes on class_0001 but `floor_lock_detected=True` fires for >50% of classes across class_0001, class_0003, class_0006** — implication: the re-condition threshold is too aggressive (false-positive on legitimately-converging-at-floor classes); revisit `_SIGNAL_HI` value or the signal logic. *[v1.1 empirical: 0/3 = 0% false-positive rate observed; condition 2 not triggered; signal is not over-aggressive.]*
3. **Existing test suite regression** (any test in `tests/test_balance_loop.py` or `tests/test_range_profile.py` that previously passed now fails) — implementation correctness regression. *[v1.1 empirical: 179/179 PASS; condition 3 not triggered.]*

### § 4.5 — Smoke gate B1 minimal-regen scope

B1 does NOT require a full season regen. The test surface is:

- **Mode-1 (BLOCKING):** single-class cold-start convergence on class_0001 from season_100002. Cold-start: `initial_modifier=1.0` (not warm-started from prior season's `final_modifier=0.0509`). Single class. ~5 min wall time.
- **Mode-2 (WARN):** repeat for class_0003 and class_0006. ~10 min additional wall time.
- **Mode-3 (test suite):** `pytest tests/test_balance_loop.py tests/test_range_profile.py` — verify no regression. ~2 min.

**Total smoke effort: ~20 minutes.** No diagnostic-season-stop-gap regen at P1 (P2 is the dedicated venue for season-level diagnostic regen under both Options A and B).

---

## § 5 — Cross-seam impact

### § 5.1 — Star-lord (telemetry consumer)

**Required additions (schema v2.13, additive):**

1. Optional nullable boolean column on `class_balance_results`: `floor_lock_recompose` (True if Option-B floor-lock-recovery fired; False if Option-B branch did not fire; NULL for pre-Option-B rows).
2. Optional nullable column on `recompose_attempts` telemetry table (if such a table exists; otherwise the field lives inside `class_balance_results.recompose_attempts_json`): `floor_lock_detected` (bool, per-attempt) and `working_modifier` (float, per-attempt). NULL for pre-Option-B rows.

**Recommended query-filter usage:**

- `WHERE floor_lock_recompose = TRUE` → the floor-lock-recovery population (kits where Option B's sub-floor working modifier was the unlock).
- `WHERE floor_lock_recompose = TRUE AND status = 'converged' AND final_balance_modifier >= 0.05` → Option B success population (recompose actually moved the kit out of the extreme-low range).
- `WHERE floor_lock_recompose = TRUE AND status = 'converged' AND final_balance_modifier < 0.05` → Option B partial success (recompose ran but kit still needs extreme modifier suppression; design-review flag).
- `WHERE floor_lock_recompose = TRUE AND status = 'failed'` → Option B did not save the kit (lever library exhausted at sub-floor working modifier; kit-redesign queue candidate).

**Sub-bucketing the recompose-fire-count question (from knight-rider handoff):**

YES — recompose-fire-count should be sub-bucketed. Specifically:

- `recompose_fire_count_total` — sum of all recompose firings (existing field; unchanged).
- `recompose_fire_count_floor_lock` — NEW; sub-count where `floor_lock_detected=True` for at least one recompose attempt in the class.

This separation lets us, post-hoc, ask "of all recompose firings in a season, what fraction were floor-lock-recovery firings vs regular recompose firings?" The answer to that question carves the population into Pattern-B-easy (regular recompose) vs Pattern-B-extreme (floor-lock-recovery), and informs the P2-to-P3 verdict synthesis.

### § 5.2 — Rocket (generation seam)

**No required changes.** Option B is contained inside `balance_loop.py`. Rocket's b6_kit_builder is *not* touched.

**Informational:** Post-Option-B, the population of classes that exit `status=converged, modifier_extreme_low=True, recompose_outcome="primary_loop_converged"` should *shrink* compared to Option-A-only baseline — those classes are now recomposed to higher-modifier convergence. If rocket's seed-promotion logic uses `modifier_extreme_low=True` as a "kit too extreme for promotion" signal, that filter still applies; the population is just smaller.

**Informational watchpoint:** if Option B's recompose successfully shapes a kit (e.g., swaps in lower-DPS skills), the resulting kit's element distribution, skill composition, or geometry mix may differ materially from rocket's intended generation output. This is *by design* — the recompose lever's job is to shape the kit. But it means R8-inverted-pipeline kits that go through floor-lock recovery may end up with composition signatures the rocket-side QA doesn't currently anticipate. No action required; documented for awareness.

### § 5.3 — Drax (loadout seam)

**No impact.** Modifier values are engine-internal; no loadout UI consumes them. Loadout publishes final post-convergence modifier as a single value; the floor-lock-recovery branch is invisible at the UI layer (as it should be — modifier is plumbing, not a player-facing concept per gandalf disposition § 11.4 Read 2).

### § 5.4 — MIGRATION.md v1.22 — what it records

Suggested entry (gamora authors at implementation time; this is the template):

> **## v1.22 — Option B recompose-trigger floor-lock recovery + LEVER_FLOOR_LOCK_WORKING_MODIFIER (2026-05-19)**
>
> **Author:** gamora
> **Dispatch:** `agentic_orchestration/dispatches/2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md` (gandalf) + the knight-rider-authored implementation dispatch
> **Investigation:** `balance-loop-floor-investigation-2026-05-19.md` § 5.2; gandalf brief § 2 (math) + § 3 (implementation)
> **Authority:** recompose-validation hive P1, AUTONOMOUS L2-equivalent (gandalf design) + L1 (gamora implementation)
>
> **Discipline #12 — SEMANTIC SHIFT:** the recompose direction-trigger's effective signal range expands. Previously, the direction check `eval_modifier < MODIFIER_LOW_THRESHOLD` was the sole trigger gate. Now, when `_quick_modifier_estimate` exits with `last_wr > _SIGNAL_HI=0.70`, a `floor_lock_detected` branch fires, overriding the lever-evaluation working modifier to `LEVER_FLOOR_LOCK_WORKING_MODIFIER=0.005`. This is a widening of the recompose trigger's effective domain. Classes whose true WR=0.5 equilibrium modifier is below `MODIFIER_SEARCH_FLOOR=0.01` now experience successful recompose firings (sub-floor probe finds lever signal), whereas pre-Option-B these classes exited with `recompose_outcome="failed_regenerate"` and `modifier_extreme_low=True`.
>
> **Discipline #18:** new module-level named constant `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005` with full docstring covering rationale, semantic-shift framing, reversibility, cross-references.
>
> **Star-lord action required:** YES (schema v2.13) — see consumer obligations below.
>
> (… rest of entry follows v1.21 template; gamora fills in implementation specifics.)

### § 5.5 — AGENT_STATE.md notes

Two AGENT_STATE.md files updated at implementation:

- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (gamora) — Option B landing record; smoke gate B1 results; MIGRATION.md v1.22 reference.
- `reincarnated-engine/src/reincarnated/telemetry/AGENT_STATE.md` (star-lord, when star-lord picks up schema v2.13 work) — Option B telemetry schema additions.

---

## § 6 — Discipline #12 semantic-shift framing (explicit)

### § 6.1 — What changes semantically

**Before Option B:** the recompose trigger fires on `eval_modifier < MODIFIER_LOW_THRESHOLD (0.30)`. The lever loop evaluates each lever at `working_modifier = eval_modifier`. When `eval_modifier` is at the search floor and `current_wr > 0.95`, lever deltas are 0.0; recompose loop returns with no lever accepted.

**After Option B:** the recompose trigger still fires on `eval_modifier < MODIFIER_LOW_THRESHOLD`. *Additionally,* when `current_wr > _SIGNAL_HI (0.70)` at exit from `_quick_modifier_estimate`, a `floor_lock_detected` branch overrides `working_modifier` to `LEVER_FLOOR_LOCK_WORKING_MODIFIER (0.005)` for the lever loop. Levers evaluate at the sub-floor probe value; recompose can fire successfully for kits whose true m* < MODIFIER_SEARCH_FLOOR.

**Class identity shift:** kits that pre-Option-B exited as `status=converged, modifier_extreme_low=True, recompose_outcome="failed_regenerate"` may now exit as `status=converged, modifier_extreme_low=False, recompose_outcome="primary_loop_converged"` — *with a materially different kit composition*. The same class name carries a different skill mix. This is the deliberate intent of recompose (it is a *composition* lever), but it must be called out: the same class id pre-Option-B and post-Option-B will differ in composition for the floor-lock-recovery population.

**This is NOT a bug fix.** It is a deliberate, named widening of the recompose trigger's effective signal range with explicit rationale (signal-range trap at floor + need for sub-floor lever probe). The recompose architecture's implicit precondition ("`_quick_modifier_estimate` reaches signal range") is being made explicit and protected via `floor_lock_detected` detection.

### § 6.2 — Why this is the right shift (design judgment)

The alternative would be: leave Option B unimplemented, accept that Option A alone serves the 22 Pattern-B classes (those with `m* ≥ 0.01`), and route the sub-floor-m* population to kit-redesign. That choice would be cleaner architecturally but would burn ~3-8 classes per season into the kit-redesign queue when they are mathematically recoverable.

The recompose-hive's central premise (per scope-of-work § 0) is that *the composition lever is the bridge between the old aggregate-mean contract and the new per-tier contract*. Letting that lever fail on the sub-floor-m* population — when the fix is a 30-LOC sub-floor probe — would undercut the premise. **Option B is the natural completion of Option A.** The semantic widening it introduces is precisely the widening Option A's diagnosis demanded.

This is the Diablo II Necromancer summon-density lesson restated (gandalf disposition § 11.7): the previous architecture's implicit assumption about resource regen broke when costs shifted; the post-Inferno fix made the assumption explicit. Same pattern here: the recompose architecture's implicit assumption that `_quick_modifier_estimate` reaches signal is being made explicit via `floor_lock_detected` and protected via `LEVER_FLOOR_LOCK_WORKING_MODIFIER`.

---

## § 7 — Acceptance criteria (for jack-ryan Gate-1 + gamora implementation)

### § 7.1 — Gate-1 acceptance (jack-ryan critique)

The brief is Gate-1-ready when:

- [x] Design questions from knight-rider handoff (six bullets) are addressed in named sections.
- [x] Math is shown (not waved): § 2 derives the signal-range trap mechanism + the working-modifier choice.
- [x] Departure from gamora § 5.2 is named and defended (§ 2.3).
- [x] Discipline #12 semantic shift is framed explicitly (§ 6).
- [x] Smoke gate B1 has a falsifying condition (§ 4.4).
- [x] Cross-seam impact (star-lord, rocket, drax) is enumerated (§ 5).
- [x] Reversibility path is named (§ 9).
- [x] Out-of-scope is stated HARD (§ 8).

Jack-ryan reviews under standard Gate-1 critique (Pattern A: discipline audit; Pattern B: technical correctness; Pattern C: scope discipline). Amendments fold into the brief before knight-rider authors the gamora implementation dispatch.

### § 7.2 — Implementation acceptance (gamora)

The implementation is ready for P1 tag fire when:

- [ ] `balance_loop.py` `_primary_recompose_loop` gains floor-lock-detection branch per § 3.1 pseudocode.
- [ ] `balance_loop.py` named constant `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005` introduced with full docstring per § 3.2.
- [ ] `ClassBalanceResult` gains `floor_lock_recompose: bool | None` field.
- [ ] `recompose_attempts` records gain `working_modifier` + `floor_lock_detected` fields per § 3.3.
- [ ] Test additions in `tests/test_balance_loop.py` covering floor-lock-detection branch (mock or fixture-based; ≥ 30 LOC, ≥ 3 test cases).
- [ ] Smoke gate B1 BLOCKING conditions verified per § 4.2 (class_0001 cold-start single-class run; four BLOCKING conditions all hold).
- [ ] WARN-level smoke conditions per § 4.3 documented in implementation completion record (class_0003 + class_0006); no rollback gate.
- [ ] Full test suite (`pytest tests/test_balance_loop.py tests/test_range_profile.py`) PASS — no regression per § 4.4 condition 3.
- [ ] MIGRATION.md v1.22 entry filed per § 5.4 template.
- [ ] AGENT_STATE.md updates per § 5.5.

P1 tag: `recompose-hive/v0.2-option-b-recompose-conditioned` (per scope-of-work § 2).

---

## § 8 — Out-of-scope (HARD)

The following are explicitly NOT in P1's scope:

1. **Bidirectional levers / DPS-increase forced working modifier for ceiling-locked classes.** B-prime scope; deferred. The `last_wr < _SIGNAL_LO` symmetric case (kits too weak even at modifier=4.0) is *interesting* but is not the recompose-hive's central premise — P1 stays surgical on the floor-lock case Phase B.2 empirically identified.
2. **Changes to `MODIFIER_SEARCH_FLOOR` or `MODIFIER_SEARCH_CEILING`.** Option A is settled (v0.1 tag landed). No further floor widening this hive.
3. **Changes to `_quick_modifier_estimate` internal logic.** The function's signal-range early-exit logic is correct; this brief consumes its output, does not modify it.
4. **Full-season regen at P1.** Smoke is single-class; full diagnostic regen is P2.
5. **New lever types.** The existing three (`skill_swap`, `geometry_mix`, `cooldown_energy`) are the lever library. No new levers in P1.
6. **Changes to rocket b6_kit_builder / b6_archetype_templates / skill generation.** Rocket's seam is not touched.
7. **Changes to per-tier WR targets / floors / ceilings.** R1 disposition is settled.
8. **Changes to `RECOMPOSE_DELTA_FLOOR = 0.02`.** The lever delta meaningfulness threshold is unchanged. If at `working_modifier=0.005` levers consistently produce small deltas (e.g., 0.01-0.015) below this threshold, the disposition is to investigate the working_modifier value, not to lower the delta floor — lowering the meaningfulness threshold would let noise be mistaken for signal.
9. **Doppelganger / experimental classes.** `DOPPELGANGER_MODIFIER_FLOOR = 0.30` is unchanged; experimental classes still skip recompose entirely (line 697-708).
10. **`recompose_outcome` enum values.** No new values; the existing `"primary_loop_converged"` covers the Option-B-success case (it does converge via primary loop, just with a sub-floor working modifier during evaluation).

---

## § 9 — Reversibility

> **v1.1 ELEVATION (2026-05-19):** Reversion option 2 (parameter-level soft-disable) is now the **preferred path** when smoke fails due to test-class-selection issues (the situation we are in). The v1.0 framing treated option 1 (full revert) as the default and option 2 as an alternative; v1.1 inverts that framing. Full revert is reserved for cases where the mechanism itself is independently invalidated (e.g., unit tests fail; production path through `ClassBalanceResult.floor_lock_recompose` is broken; the branch produces incoherent behavior under mock conditions). When the mechanism is verified by unit tests and the failure is a test-class-selection issue, soft-disable preserves the verified infrastructure for cheap re-enable on the natural empirical venue (P2 full-season regen).

Option B's revert path is clean and minimal.

**Reversion option 1 (full revert):** remove the floor-lock-detection branch in `_primary_recompose_loop` (lines added per § 3.1). Restore `working_modifier = eval_modifier` unconditionally. Remove `LEVER_FLOOR_LOCK_WORKING_MODIFIER` constant. Remove `floor_lock_recompose` field from `ClassBalanceResult`. Remove `working_modifier` / `floor_lock_detected` fields from `recompose_attempts` records.

Single git revert reverses everything except telemetry-table schema additions (those can stay as nullable columns indefinitely). No persistent data depends on Option B's behavior.

*v1.1 use criterion:* full revert applies when mechanism is independently invalidated. Not the current situation.

**Reversion option 2 (parameter-level disable; v1.1 preferred path for test-class-selection failures):** set `LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR` (i.e., 0.01). This makes the floor-lock branch a no-op semantically: `working_modifier` becomes equal to `eval_modifier` for floor-locked cases (since `eval_modifier ≈ 0.01` at floor-lock). The `floor_lock_detected` flag still fires, but the lever evaluation reverts to pre-Option-B behavior. This is the "soft disable" path — preserves the diagnostic telemetry while disabling the behavioral change.

*v1.1 use criterion:* soft-disable applies when (a) the mechanism is verified by unit tests + production-path inspection, AND (b) the smoke gate failed due to test-class-selection issues (test class doesn't have the population-membership property the smoke was designed to detect). Under soft-disable, infrastructure + telemetry are preserved; one-line re-enable (`LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005`) is available when a confirmed floor-lock-recovery subject surfaces (P2 venue).

*v1.1 soft-disable tag convention:* the seam tag fires with an explicit qualifier — `gamora/v1.14-balance-loop-option-b-recompose-conditioned-soft-disable` — to make the soft-disable state visible to future archaeologists. The hive milestone tag (`recompose-hive/v0.2-option-b-recompose-conditioned`) is HELD; it does not fire until the behavioral change is empirically demonstrated (P2 surfaces a real subject + re-enable + smoke passes).

**Reversion conditions (when to revert; v1.1):**

- Smoke gate B1 BLOCKING fails AND mechanism independently invalidated → full revert (option 1).
- Smoke gate B1 BLOCKING fails AND mechanism verified by unit tests AND test class confirmed NOT in target population → soft-disable (option 2); brief amendment; route empirical question to P2.
- P2 fresh diagnostic regen surfaces a defect where Option B produces unbalanced kits in a different failure mode (e.g., recompose pushes a class to modifier=0.50 but with a kit composition that fails per-tier WR checks). Surface to gandalf for re-disposition; soft-disable via option 2 until disposition.
- P3 validation verdict is CANNOT REJECT NULL (per scope-of-work § 1). H_RC refutation may implicate Option B specifically — surface to Matt with the Option B sub-population's behavior analyzed.
- P2 returns zero `floor_lock_detected=TRUE` rows across full-season regen → wind-down trigger #3 candidate (masked-Pattern-B-extreme population may not exist at the scale § 2.5 predicted); soft-disable becomes the right end state; surface to Matt at P3 with the empirical verdict.

**What survives revert:** the design diagnosis (this brief), the empirical Pattern-A/B carve from Phase B.2, the named-constant precedent for `MODIFIER_SEARCH_FLOOR` (Option A's gift), and the floor-lock-detected telemetry schema. None of these depend on Option B's behavior; all remain valuable independent of whether Option B's implementation ships.

**What survives soft-disable:** in addition to the items that survive full revert, soft-disable also preserves (a) the full Option B branch logic (verified by unit tests), (b) `LEVER_FLOOR_LOCK_WORKING_MODIFIER` as a named constant (value changed from 0.005 → MODIFIER_SEARCH_FLOOR=0.01; docstring updated to reflect soft-disable state + re-enable path), (c) all telemetry fields and their per-attempt round-trip, (d) the smoke gate B1 script (preserved for re-use when a real subject is identified at P2). Re-enable cost: one-line constant change.

---

## § 10 — References

**Predecessor brief (P0):**
- `agentic_orchestration/dispatches/2026-05-19-gamora-balance-loop-floor-option-A-implementation.md`

**Investigation (the math):**
- `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md` §§ 4-5 (mechanism + options)

**Concurrence framing:**
- `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 11 (gandalf staged-approval concurrence on Options A + B)

**Hive context:**
- `agentic_orchestration/hive-mind/recompose-validation-log.md` (this hive's log)
- `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md` (mission scope)
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` (protocol § 3 P1 + § 6 P1)

**Pattern-A/B empirical foundation:**
- `agentic_orchestration/CHANGELOG.md` lines 28, 38-42, 75-76 (Phase B.2 Pattern-A/B carve)

**Autonomous-operation authority:**
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.1 (gandalf decides cross-cutting design; no L3-to-Matt during operation)

**Engineering disciplines anchored:**
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #1 (math-before-code — § 2), #2 (smoke-test — § 4), #11 (empirical inspection / attribution — § 5.1), #12 (semantic shift — § 6), #15 (drift-detection — § 2.2 + § 6.2 implicit-precondition framing), #18 (implicit-pillar named constant — § 3.2)

**Code (verified locations as of post-Option-A landing):**
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py`:
  - line 73: `MODIFIER_LOW_THRESHOLD = 0.30` (existing direction threshold; unchanged)
  - line 123: `MODIFIER_SEARCH_FLOOR = 0.01` (Option A named constant; reference)
  - line 1288: `_quick_modifier_estimate` (existing; output consumed by Option B re-condition check)
  - line 1323: `_primary_recompose_loop` (single touch site for Option B)
  - line 1351-1365: existing direction-trigger block (Option B adds floor-lock detection above this)
  - line 1374-1401: existing lever loop (Option B threads `working_modifier` through to lever calls)
  - new constant location: near line 73, paired with `MODIFIER_LOW_THRESHOLD`

---

*Authored 2026-05-19 by gandalf under AUTONOMOUS L2-equivalent authority (recompose-validation hive; architectural / load-bearing cross-cutting design). Brief routes to jack-ryan for Gate-1 critique. The recompose lever sharpens; the road continues. Mithrandir signs.*
