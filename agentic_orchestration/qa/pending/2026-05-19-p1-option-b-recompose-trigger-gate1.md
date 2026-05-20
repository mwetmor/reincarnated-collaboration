# Gate-1 Critique — 2026-05-19 — P1 Option B Recompose-Trigger Re-conditioning

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1, pre-implementation peer critique)
**Date:** 2026-05-19
**Brief author:** gandalf
**Brief path:** `agentic_orchestration/dispatches/2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md`
**Protocol:** `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` § 3 P1 + § 6 P1
**Scope-of-work acceptance gate:** `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md` § 2 (P1)
**Critique patterns applied:** Pattern A (discipline audit) + Pattern B (technical correctness) + Pattern C (scope discipline)

---

## § 0 — TL;DR + Disposition

**DISPOSITION: APPROVE-WITH-AMEND**

The brief is technically sound and well-reasoned. The core design decisions — `last_wr > _SIGNAL_HI` as the re-condition signal, `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005`, the four-condition smoke B1 gate, and the cross-seam schema v2.13 additions — are all defensible. The departure from gamora § 5.2 is the right call: the `status=failed AND eval_modifier ≤ floor + ε` framing does not match code-architecture reality (recompose runs pre-binary-search) and carries ambiguity the `last_wr` signal avoids cleanly.

**Six amendments required** before knight-rider authors the gamora implementation dispatch. All are correctness or clarity improvements; none are architectural objections. Two are mandatory-code-level (Amendment 1: `_QUICK_SIGNAL_HI` single-source-of-truth; Amendment 2: `_evaluate_class` NaN/error fail-loud guard); three are test-specification improvements (Amendments 3, 4, 5); one is a MIGRATION.md template completion (Amendment 6).

None of the amendments change the core design direction. Gamora can implement from this brief + amendments without back-routing to gandalf.

---

## § 1 — Required Reading Absorbed

All seven required documents read in full:

1. Hive log (all entries through routing to jack-ryan)
2. Gandalf brief in full (10 sections, ~720 LOC)
3. Scope-of-work § 2 (P1 acceptance gate)
4. Protocol §§ 3 + 6 (P1 per-phase requirements)
5. Investigation §§ 4-5 (mechanism + Options math)
6. `balance_loop.py` lines 60-139 (constants), 324-403 (ClassBalanceResult), 680-775 (primary recompose context), 1288-1407 (_quick_modifier_estimate + _primary_recompose_loop in full), 1547-1900 (all three lever functions), 2139-2160 (_evaluate_class signature)
7. MIGRATION.md v1.21 (Option A consumer template, for v1.22 conformance check)
8. Engineering disciplines #1, #2, #11, #12, #13a, #15, #17, #18, R11(b), Pattern P7

**Code-state confirmation:** `balance_loop.py` post-Option-A has `MODIFIER_SEARCH_FLOOR = 0.01`, `MODIFIER_SEARCH_CEILING = 4.0` at lines 123-124. `ClassBalanceResult` has `modifier_extreme_low: bool | None = None` at line 389. `_primary_recompose_loop` at line 1323 calls `_quick_modifier_estimate` and passes `eval_modifier` directly into lever calls at line 1378. `_SIGNAL_HI = 0.70` is a local variable inside `_quick_modifier_estimate` at line 1308. No module-level `_QUICK_SIGNAL_HI` constant exists.

---

## § 2 — Pattern A: Discipline Audit

### Discipline #1 — Math-before-code

**CONFIRMED.** The brief's § 2 is a complete mathematical derivation: the floor-lock mechanism is traced from `_quick_modifier_estimate` exit conditions through lever delta failure, with the signal-range trap articulated precisely. The 0.005 working modifier choice is justified via three explicit reasons (domain separation, signal range, determinism). The predicted-outcome table in § 2.5 is empirically grounded in Phase B.2 Pattern A/B carve. No hand-waving observed.

**One note (INFO, not WARN):** § 2.5 estimates 3-8 floor-lock-recovery classes per season. This is a reasonable conservative bound given the 22 Pattern-B population, but the empirical basis is not cited (it appears to be gandalf's architectural judgment rather than data from the stop-gap regen). P2 will produce the empirical number; the estimate's precision doesn't block P1.

### Discipline #2 — Smoke-test discipline

**CONFIRMED.** Smoke gate B1 is scoped tightly: single-class cold-start (~5 min) + two secondary classes (~10 min) + pytest (~2 min). No full-season regen at P1. Smoke conditions are well-separated: conditions 1-3 test mechanism-fires-correctly; condition 4 tests mechanism-is-effective. The WARN/BLOCK distinction (class_0001 BLOCKING; class_0003, class_0006 WARN-level) is appropriate and matches the diagnostic intent.

**One note (WARN — see Amendment 3):** The brief specifies "≥ 3 test cases" in `tests/test_balance_loop.py` for the new branch. Three test cases is thin for a branch with four distinct observable states. See Amendment 3 for recommended minimum test surface.

### Discipline #11 — Empirical inspection

**CONFIRMED.** The `floor_lock_recompose` sub-bucketing (§ 5.1) and the per-attempt `working_modifier` / `floor_lock_detected` telemetry fields are correct. These let P2/P3 reconstruct the exact chain of events for each floor-lock-recovery class. The sub-bucketing question (recompose_fire_count_total vs _floor_lock) is addressed explicitly and correctly.

### Discipline #12 — Semantic-shift framing

**CONFIRMED.** § 6 is explicit and accurate:

- Before: `eval_modifier` always equals `working_modifier` in the lever loop. Levers evaluate at the binary-search signal.
- After: for floor-lock-detected classes, `working_modifier` diverges from `eval_modifier`. This IS a semantic widening of the recompose trigger's effective domain.
- Class-identity shift: kits that pre-Option-B exited as `recompose_outcome="failed_regenerate"` may now exit as `recompose_outcome="primary_loop_converged"` with a materially different composition.

**One tightening needed (WARN — see Amendment 6):** The MIGRATION.md v1.22 template in § 5.4 is correct in content but missing a clause for the R11(b) cross-seam round-trip obligation. See Amendment 6.

### Discipline #15 — Drift-detection (implicit-precondition framing)

**CONFIRMED.** § 2.2 + § 6.2 together make the implicit precondition explicit: the recompose architecture previously assumed `_quick_modifier_estimate` reaches signal range before returning. Option B makes this assumption visible and adds a detection branch when it fails. The `floor_lock_detected` boolean is the explicit guard. This is the correct application of Discipline #15.

### Discipline #18 — Implicit-pillar named constant

**CONFIRMED** for `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005`. The brief's proposed docstring (§ 3.2) is thorough — rationale, semantic-shift framing, reversibility, cross-references all present.

**WARN — see Amendment 1:** `_QUICK_SIGNAL_HI = 0.70` in the brief's pseudocode (§ 3.1, line 183) is a second Discipline #18 implicit-pillar candidate that the brief handles incorrectly. See Amendment 1.

---

## § 3 — Pattern B: Technical Correctness

### (a) § 2.3 departure defensibility — `last_wr > _SIGNAL_HI` vs `eval_modifier ≤ floor + ε`

**DISPOSITION: DEPARTURE IS DEFENSIBLE. Substitution is clean.**

Code-architecture trace confirms both of gandalf's rejection reasons:

**(1) `status=failed` not available at recompose time.** Correct. The call sequence in `balance_class()` (line 699) is: `_primary_recompose_loop()` runs first, returns `(any_lever_accepted, baseline_eval_modifier)`. Binary search runs after. The `recompose_outcome` variable (initialized at line 698 as `"modifier_fallback"`) is updated to `"failed_regenerate"` at line 1099 — AFTER the binary search converges. At `_primary_recompose_loop` call time, `status=failed` does not yet exist. The `status=failed AND eval_modifier ≤ floor + ε` framing is definitionally impossible as a pre-recompose signal.

**(2) `eval_modifier ≤ floor + ε` is false-positive ambiguous.** Correct. A class whose true `m*` is 0.013 will have `eval_modifier ≈ 0.012` with `last_wr ≈ 0.45` — that's a legitimate signal-range-reached case. The `eval_modifier ≤ floor + ε` test would catch this class incorrectly. The `last_wr > _SIGNAL_HI` test would correctly bypass it (WR=0.45 < 0.70 → no floor-lock).

**Does any consumer depend on the rejected semantic?** No. Search of `balance_loop.py` finds no code path that uses `eval_modifier ≤ floor + ε` as a detection condition. The `modifier_extreme_low` flag (Option A, line 1043) checks `modifier < 0.05` (final convergence modifier, post-binary-search) — a completely different variable. No existing star-lord query logic references a pre-recompose `eval_modifier ≤ floor + ε` semantic; that semantic only appears in gamora's investigation § 5.2 as a proposed (but not yet implemented) design. The substitution is architecturally clean.

**One implementation nuance gamora must note:** the direction check in `_primary_recompose_loop` at line 1356 uses `eval_modifier` to set `reduce_dps / increase_dps`. At floor-lock, `eval_modifier ≈ 0.01` (floor), so `eval_modifier < MODIFIER_LOW_THRESHOLD (0.30)` is True → `reduce_dps = True`. This is the correct direction even under Option B: a floor-locked kit IS too DPS-heavy; levers should reduce DPS. The brief's pseudocode correctly preserves this direction check on `eval_modifier` (not `working_modifier`). Confirmed correct.

### (b) § 4.2 smoke B1 BLOCKING condition #4 tightness

**DISPOSITION: CONDITION #4 AS WRITTEN IS MINIMALLY ACCEPTABLE. RECOMMEND TIGHTENING TO WARN-SECONDARY. See Amendment 4.**

Condition #4 as written: `final_modifier > MODIFIER_SEARCH_FLOOR (0.01) AND modifier_extreme_low=False (i.e., final_modifier ≥ 0.05)`.

**The tightness question:** Is `final_modifier ≥ 0.05` the right proof-of-effectiveness threshold?

Analysis of the three candidates:

- **`> 0.01` (bare floor crossing):** too weak. A class moving from `eval_modifier ≈ 0.01` to `final_modifier ≈ 0.014` would pass BLOCKING, but this is a 40% improvement from the floor — the lever barely moved the kit. Not proof of effectiveness.

- **`≥ 0.05` (= `modifier_extreme_low=False`):** the brief's current choice. This is a meaningful threshold — it means the post-recompose binary search converges above the prior floor, i.e., the kit no longer needs extreme modifier suppression. This IS a proof of effectiveness for the primary population. However, it encodes the prior floor (0.05) as a proxy for "healthy," which is coincidental rather than principled.

- **`> 0.10` or band `∈ [0.10, 0.50]`:** more aggressive; tests whether recompose moved the kit into a "comfortably healthy" range rather than barely above the old floor. This would reject partial success cases where recompose ran but the kit still needs extreme suppression (just not quite as extreme as before).

**My disposition:** condition #4 as written (`modifier_extreme_low=False`) is acceptable as a BLOCKING condition because it tests the meaningful semantic — does the class no longer require sub-0.05 modifier suppression? A class at final_modifier=0.06 has been genuinely moved out of the extreme range. The 0.0501 edge case (barely passes) is theoretically possible but unlikely: the binary search converges to `TOLERANCE * 2` precision, and for a floor-locked kit that has been recomposed by even a moderate lever delta, the resulting modifier should be materially above 0.05.

**However:** the brief should add a WARN-level secondary check for the `0.05 ≤ final_modifier < 0.10` range (near-floor convergence — recompose ran but kit is still heavily suppressed). This catches the "technically PASS but barely" case without blocking P1 acceptance. See Amendment 4.

**The false-negative on partial-effectiveness** (recompose helps but kit still needs sub-0.10 modifier) is real but should be scored at P3 validation, not smoke B1. Smoke B1 is proof-of-mechanism; P3 is proof-of-effectiveness-at-season-scale.

### (c) § 3.2 `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005` magnitude

**DISPOSITION: MAGNITUDE IS CORRECT. "KIT-REDESIGN FLAG" IS THE RIGHT OUTCOME FOR THE 0.005-STILL-SATURATED CASE.**

Three-reason argument in § 2.4 (domain separation, sufficient signal range, determinism) is sound. Stress-testing the edge case:

**If a kit wins 100% at modifier=0.005:** This means the kit's true `m*` is below 0.005. At that level, the kit's base DPS is so extreme that 0.5% of baseline DPS still saturates the gauntlet. The lever library (skill_swap, geometry_mix, cooldown_energy) can only reshape the composition within the existing kit's ability set — it cannot redesign the fundamental damage scaling. These are the 27 Pattern-A cases gandalf describes: kits where the damage-density pathology is structural, not compositional.

**Is "kit-redesign flag" the correct outcome?** Yes. The lever library's job is to reshape compositional ratios (damage/non-damage role balance; geometry efficiency; cooldown rotation). If the kit saturates at 0.005, no compositional reshaping will fix it — the issue is the raw damage magnitudes of individual skills, which only rocket's b6_kit_builder can address. Routing these to the kit-redesign queue is architecturally correct.

**Should there be a fallback (0.001 if 0.005 fails)?** The brief's implicit answer is no, and I concur for three reasons: (1) at 0.001 modifier, fight dynamics become extremely noisy — modifier affects damage linearly, but fight outcomes at 0.1% damage baseline are dominated by timeout mechanics rather than genuine combat resolution; (2) a kit that fails at 0.005 will have WR ≈ 1.00 at 0.001 too (the ceiling saturates for the same reason); (3) adding a fallback introduces an escalating probe that has no natural termination condition. Half-floor is the principled single probe; anything lower is speculation.

**One minor note:** the brief states "for ~all observed floor-locked R8 inverted kits, this drops WR into measurable range" but does not cite specific measurements. The investigation data (§ 3.2) shows swarm WR at floor=0.0509 is 0.82-1.00. At modifier=0.005 (50% below the new floor), even a kit with swarm WR=0.99 at floor should see WR drop meaningfully — the damage-reduction is multiplicative and substantial. This is inference from the mechanism, not empirical measurement at 0.005; the smoke gate B1 condition #3 (`before_winrate < 0.95` at working_modifier=0.005) will empirically validate this claim.

### Discipline #13a implicit-pillar drift watch — `_QUICK_SIGNAL_HI`

**WARN → Amendment 1 (REQUIRED).**

The brief's pseudocode at § 3.1 introduces:

```python
_QUICK_SIGNAL_HI = 0.70  # mirror of _SIGNAL_HI in _quick_modifier_estimate
```

This is declared as a local variable inside `_primary_recompose_loop`. Meanwhile, `_SIGNAL_HI = 0.70` is a local variable inside `_quick_modifier_estimate` (line 1308). These are two local literals encoding the same semantic threshold — "signal range upper bound for lever delta meaningfulness."

**The risk:** if `_SIGNAL_HI` in `_quick_modifier_estimate` is ever updated (e.g., tuned from 0.70 to 0.65 based on empirical lever delta analysis), the `_QUICK_SIGNAL_HI` check in `_primary_recompose_loop` would be stale. The floor-lock detection would remain calibrated to 0.70 even when the signal range has moved. This is a silent drift instance — exactly the shape Discipline #13a and #18 are designed to catch.

**The fix:** the two local literals should share a single module-level named constant. See Amendment 1 for the recommendation.

### Pattern P7 silent-default watch — `_evaluate_class` error behavior

**WARN → Amendment 2 (REQUIRED).**

The brief's § 3.1 pseudocode includes:

```python
current_wr, _, _, _ = self._evaluate_class(
    player_class, gauntlet, fights_per_matchup, working_modifier
)
```

`_evaluate_class` signature (line 2139) returns `(overall_winrate, per_opponent_winrates, batches, loadouts_by_opponent)`. The `overall_winrate` position is `float`. However, the function does not have an explicit error path guard — if the gauntlet is empty or `fights_per_matchup=0`, the inner loop over `gauntlet` produces `win_rates = {}` and `batches = {}`, and the function would return based on whatever the downstream aggregation does with empty dicts. Looking at `balance_class()` upstream, `fights_per_matchup` is always a positive integer from the caller, and `gauntlet` is always non-empty (validated at `_build_gauntlet`). So under normal operation, this is safe.

**However:** at `working_modifier=0.005`, the fight evaluation is running at extreme suppression. The concern is not NaN/ZeroDivision in Python sense (DPS scaling is multiplicative, not division) but rather that at modifier=0.005, every fight may time out, producing WR=0.0 if timeouts are counted as losses. This is not a bug — it's the expected behavior for a Pattern-A kit that can't win even at 0.5% DPS. But the `current_wr = 0.0` case should be handled explicitly in the floor-lock branch logic: if `current_wr` after re-evaluation is still near 1.00 (kit dominates at 0.005) or is 0.0 (kit collapses entirely at 0.005), the lever loop will behave differently.

**The specific risk:** if `current_wr ≈ 0.0` at `working_modifier=0.005` (kit is so weak at 0.005 that all fights time out → loss), then `reduce_dps=True` direction tries to reduce DPS further, but the kit is already losing all fights. Lever delta would be near 0.0 (WR can't go lower than 0.0). All levers rejected. `floor_lock_detected=True` but no lever accepted — correct outcome (kit-redesign queue) but reached for the wrong reason. This case needs a comment at minimum, and ideally a fail-loud log entry so gamora can distinguish "kit saturates at 0.005 (classic floor-lock-recovery failure)" from "kit collapses at 0.005 (working_modifier is too low for this archetype type)."

See Amendment 2 for the prescription. This is a code-comment + logging obligation, not a design change.

### Test coverage adequacy

**WARN → Amendment 3 (REQUIRED).**

The brief specifies "≥ 3 test cases" and "≥ 30 LOC" in `tests/test_balance_loop.py`. Three test cases for a branch with the following observable states is thin:

- State A: floor-lock-detected=True, lever accepted, final_modifier moves above floor (the happy path)
- State B: floor-lock-not-detected=False (normal kit; Option B branch doesn't fire)
- State C: floor-lock-detected=True, no lever accepted (kit-redesign-queue case)
- State D: floor-lock-detected=True, lever accepted, but final_modifier stays near floor (partial-effectiveness)

The brief's minimum of 3 tests would naturally cover states A, B, and C. State D (partial effectiveness) is less critical for the unit test but useful for regression. More critically, three behavioral cases need to be covered at the unit level:

- `floor_lock_detected=True` fires when `last_wr > 0.70` at exit
- `floor_lock_detected=False` when `last_wr ≤ 0.70` at exit (signal-range-reached case)
- The `recompose_attempts` telemetry records `working_modifier` and `floor_lock_detected` per-attempt

These require mocked `_quick_modifier_estimate` + `_evaluate_class` to be deterministic. The existing test patterns in `test_balance_loop.py` (e.g., `test_strong_class_gets_nerfed` at line 376, `test_weak_class_gets_buffed` at line 389) use full `BalanceLoop.balance_class()` runs — these are integration-style, not unit-level. For the new branch, mock-based unit tests would be more robust and faster.

**Minimum required test additions (Amendment 3):**
1. `test_floor_lock_detected_fires_when_quick_estimate_saturated` — mock `_quick_modifier_estimate` to return `(0.011, 0.98)` (floor-proximity + saturated WR); assert `floor_lock_detected=True` in recompose_attempts + `working_modifier=0.005`.
2. `test_floor_lock_not_detected_when_signal_reached` — mock `_quick_modifier_estimate` to return `(0.012, 0.55)` (floor-proximity but signal-range WR); assert `floor_lock_detected=False` in recompose_attempts + `working_modifier` equals `eval_modifier`.
3. `test_floor_lock_recompose_field_in_classbalanceresult` — run `balance_class()` on a mock floor-locked class; assert `result.floor_lock_recompose` is a bool (not None).
4. `test_floor_lock_detected_no_lever_accepted_kit_redesign` — mock `_quick_modifier_estimate` returning saturated WR + mock all levers returning `accepted=False`; assert `recompose_outcome` is `"failed_regenerate"` (not `"primary_loop_converged"`); assert `floor_lock_recompose=True` in result.

These four test cases cover all four observable states cleanly. Brief minimum of 3 should be raised to 4.

### Back-compat assertion — `recompose_outcome` enum and `recompose_attempts` schema

**CONFIRMED. No new enum values introduced.**

Inspection of `balance_loop.py` confirms `recompose_outcome` takes values: `"skipped_experimental"`, `"modifier_fallback"`, `"primary_loop_converged"`, `"primary_loop_reverted"`, `"failed_regenerate"`, `"secondary_converged"`. The brief's § 8 item 10 explicitly rules out new enum values. `"primary_loop_converged"` covers Option B success (recompose fired via sub-floor probe and was accepted). This is correct — the outcome from the binary search's perspective IS a primary loop convergence.

`recompose_attempts` is a list of dicts appended to `player_class.balance_metadata["recompose_attempts"]`. The new fields (`working_modifier`, `floor_lock_detected`) are additions to existing dict keys — additive, not replacement. Pre-Option-B records (lacking these keys) will not be broken by the addition because existing consumers iterate over attempt dicts and read specific named keys; new keys are simply absent in legacy records. The `None` default pattern is consistent with v1.21 precedent.

**One nuance:** existing star-lord queries that read `recompose_attempts[*].eval_modifier` will continue to work correctly — `eval_modifier` semantics are unchanged (it remains the `_quick_modifier_estimate` output, not the probe value). The new `working_modifier` field is the divergent value; `eval_modifier` is stable. Confirmed.

### Cross-seam coordination — star-lord schema v2.13 alignment

**MOSTLY CONFIRMED with one naming ambiguity (Amendment 5).**

The schema v2.13 additions in § 5.1 are:
- `floor_lock_recompose` (bool, nullable) on `class_balance_results` table
- `floor_lock_detected` (bool, per-attempt, nullable) on recompose_attempts telemetry
- `working_modifier` (float, per-attempt, nullable) on recompose_attempts telemetry

All three are additive-nullable per the v1.21 pattern. The recommended query-filter patterns in § 5.1 are correct and complete. The sub-bucketing fields (`recompose_fire_count_total` + `recompose_fire_count_floor_lock`) are appropriately scoped as derived aggregations, not primary schema fields.

**Naming check against v2.12 conventions:** v2.12 used `modifier_extreme_low` (snake_case bool, simple name). The new v2.13 fields follow the same convention. `floor_lock_recompose` is slightly ambiguous — it could read as "lock on floor due to recompose" rather than "recompose triggered by floor-lock." `recompose_floor_lock` would be more consistent with the existing `modifier_extreme_low` naming (modifier comes first in compound names). However, this is a style observation, not a blocker. See Amendment 5 for a recommended rename, but mark it OPTIONAL (gamora decides at implementation time).

**R11(b) check:** The brief provides recommended query-filter usage at § 5.1, which partially satisfies R11(b). However, the round-trip smoke clause (R11(b) form (i) or (ii)) is not explicit in the implementation acceptance criteria (§ 7.2). See Amendment 6.

### MIGRATION.md v1.22 template completeness

**MOSTLY COMPLETE with one gap (Amendment 6).**

The template in § 5.4 follows v1.21 structure correctly. It covers:
- Discipline #12 semantic shift framing
- Discipline #18 named constant
- Star-lord consumer obligation ("YES, schema v2.13")

**Missing:** an explicit R11(b) round-trip smoke clause. The v1.21 entry does not include this explicitly either (v1.21 was authored before R11(b) was codified as a named prescription). But v1.22 should set the right precedent. The clause needed is: "Round-trip: additive-nullable; existing consumer code paths tolerate absent keys. Isolation verified by [test_floor_lock_recompose_field_in_classbalanceresult]." See Amendment 6.

**Also missing from v1.22 template:** A note on the rocket informational watchpoint (§ 5.2 — composition signatures of floor-lock-recovery kits may differ from rocket's intended generation output). The v1.21 entry had an explicit rocket informational section. The v1.22 template's "rest of entry follows v1.21 template" language implies gamora should carry this over, but it should be named explicitly given that v1.22 is more behaviorally significant for rocket than v1.21 was.

---

## § 4 — Pattern C: Scope Discipline

**CONFIRMED. No scope creep observed.**

The brief's § 8 hard out-of-scope list is thorough and all ten items correctly exclude B-prime (bidirectional levers), floor changes (Option A settled), `_quick_modifier_estimate` internals, full-season regen at P1, new lever types, rocket b6_kit_builder, per-tier WR targets, `RECOMPOSE_DELTA_FLOOR`, doppelganger/experimental classes, and new `recompose_outcome` enum values.

**Verifying the implementation scope (§ 3) against the out-of-scope list:**

- The `working_modifier` variable in the lever loop (§ 3.1) is a local variable inside `_primary_recompose_loop` — it does not become a new parameter to lever functions. Lever function signatures (`_lever_skill_swap`, `_lever_geometry_mix`, `_lever_cooldown_energy`) all take `eval_modifier: float` as a positional parameter. The brief's pseudocode passes `working_modifier` in the position currently called `eval_modifier`. **This is a parameter-name-only change at the call site** — the lever functions don't need to be renamed. This is correct and within-scope.

- The `_quick_modifier_estimate` function's internal logic is NOT modified (consistent with § 8 item 3). Only its output (`last_wr`) is consumed by the new detection branch.

- No new seams are touched. `balance_loop.py` is the single touch file for the implementation proper; `ClassBalanceResult` adds one field; `tests/test_balance_loop.py` adds tests; `MIGRATION.md` adds v1.22 entry. Scope is tight.

**Secondary loop interaction — one confirmation needed:**

The secondary loop in `balance_class()` at lines 717-775 calls `self._primary_recompose_loop()` a second time (line 764) when a better element variant is found. Under Option B, this second call to `_primary_recompose_loop` will also execute the floor-lock detection branch if the element-variant class is still floor-locked after redistribution. This is **correct behavior** — the secondary loop's second pass should also benefit from Option B. The `floor_lock_detected` flag in the attempt records from the secondary pass will correctly be `True` if the redistributed class is still floor-locked. Gamora should verify this interaction is intentional and document it in AGENT_STATE.md completion record.

---

## § 5 — Amendments (APPROVE-WITH-AMEND)

### Amendment 1 — REQUIRED: `_QUICK_SIGNAL_HI` must be a module-level named constant, not a local

**Rationale:** Discipline #18 (implicit-pillar named-constant). Two local literals (0.70 in `_quick_modifier_estimate` and 0.70 in `_primary_recompose_loop`) encode the same semantic threshold. If one changes, the other silently diverges. This is the exact implicit-pillar drift shape Discipline #18 was authored to prevent.

**Recommended implementation:**

At the module-level constants block near line 70 (alongside `RECOMPOSE_QUICK_ITERS`, `MODIFIER_LOW_THRESHOLD`, etc.):

```python
# ── B14.5 recompose signal-range bounds (same pair used by both _quick_modifier_estimate
#    and the Option-B floor-lock detection in _primary_recompose_loop) ──────────────────
RECOMPOSE_SIGNAL_LO: float = 0.30   # lower bound of lever-signal range (below = kit too weak)
RECOMPOSE_SIGNAL_HI: float = 0.70   # upper bound of lever-signal range (above = kit saturated)
```

Then `_quick_modifier_estimate` replaces its local `_SIGNAL_LO, _SIGNAL_HI = 0.30, 0.70` with these constants. And `_primary_recompose_loop`'s Option B detection uses `RECOMPOSE_SIGNAL_HI` instead of `_QUICK_SIGNAL_HI = 0.70`.

**This is a small, clean change.** The module-level naming also makes the `_QUICK_SIGNAL_HI` in the brief's pseudocode obsolete — the brief's comment `# mirror of _SIGNAL_HI in _quick_modifier_estimate` confirms the shared-constant intent; the fix is to make sharing explicit. No behavior change; only single-source-of-truth.

**Impact on brief:** gamora replaces the brief's local `_QUICK_SIGNAL_HI = 0.70` in pseudocode with `RECOMPOSE_SIGNAL_HI`. Same behavior; correct single-source.

### Amendment 2 — REQUIRED: Fail-loud logging for `current_wr ≈ 0.0` at `working_modifier=0.005`

**Rationale:** Pattern P7 silent-default watch. At `working_modifier=0.005`, a heavily nerfed kit may produce `current_wr ≈ 0.0` (all timeouts, counted as losses). The lever loop in `reduce_dps=True` direction will then try to reduce DPS on a kit that is already losing all fights — all lever deltas will be 0.0 from below, and all levers will be rejected. This is the correct outcome (kit-redesign queue) but the failure mode is indistinguishable from "kit saturates at 0.005" in the telemetry without an explicit log entry.

**Recommended implementation:** After the re-evaluation `current_wr` assignment in the floor-lock branch:

```python
if floor_lock_detected:
    working_modifier = LEVER_FLOOR_LOCK_WORKING_MODIFIER
    current_wr, _, _, _ = self._evaluate_class(
        player_class, gauntlet, fights_per_matchup, working_modifier
    )
    if current_wr > RECOMPOSE_SIGNAL_HI:
        log.debug(
            "Class %s: floor_lock_detected but still saturated at working_modifier=%.4f "
            "(WR=%.4f > SIGNAL_HI=%.2f). Levers will find no signal; kit-redesign-queue candidate.",
            player_class.id, working_modifier, current_wr, RECOMPOSE_SIGNAL_HI,
        )
    elif current_wr < RECOMPOSE_SIGNAL_LO / 2:   # < 0.15 suggests over-suppression at 0.005
        log.debug(
            "Class %s: floor_lock_detected but over-suppressed at working_modifier=%.4f "
            "(WR=%.4f < 0.15). Levers will reject reduce_dps direction; kit-redesign-queue candidate.",
            player_class.id, working_modifier, current_wr,
        )
```

This is logging only — no behavior change. Adds ~10 LOC. Converts the silent-no-op into an observable-from-run-log event.

### Amendment 3 — REQUIRED: Minimum test count raised to 4; specific test cases enumerated

**Rationale:** Discipline #2 (smoke-test discipline) + the four observable Option-B branch states.

**Required minimum test surface (replaces brief's "≥ 3 test cases"):**

1. `test_floor_lock_detected_fires_when_saturated` — mock `_quick_modifier_estimate` → `(0.011, 0.98)`; run `_primary_recompose_loop`; assert at least one attempt has `floor_lock_detected=True` and `working_modifier=LEVER_FLOOR_LOCK_WORKING_MODIFIER`.

2. `test_floor_lock_not_detected_when_signal_reached` — mock `_quick_modifier_estimate` → `(0.012, 0.55)`; run `_primary_recompose_loop`; assert all attempts have `floor_lock_detected=False` and `working_modifier == eval_modifier`.

3. `test_floor_lock_recompose_field_in_classbalanceresult` — integration-style (full `balance_class()` call on a constructed floor-locked class or mocked path); assert `result.floor_lock_recompose` is a `bool` (not `None`).

4. `test_floor_lock_telemetry_records_working_modifier` — assert that when `floor_lock_detected=True`, recompose_attempts records both `working_modifier` and `floor_lock_detected` fields correctly (and that `eval_modifier` is still the original estimate, not the probe value).

Tests 1 and 2 require mocking `_evaluate_class` to return a controlled WR at `working_modifier=0.005`. The monkeypatch pattern used elsewhere in the test file applies here.

### Amendment 4 — RECOMMENDED: Smoke B1 condition #4 — add WARN-level near-floor secondary check

**Rationale:** Brief § 4.2 condition #4 as written (`modifier_extreme_low=False`, i.e., `≥ 0.05`) is the right BLOCKING floor. But the "barely passes" case (final_modifier ∈ [0.05, 0.10]) is worth flagging as a WARN to give early signal on partial-effectiveness before P2 season-scale analysis.

**Recommended addition to § 4.3 WARN-level conditions:**

```
| If post-recompose final_modifier ∈ [0.05, 0.10) for class_0001, 
  log as WARNING: "Option B marginal recovery — modifier above 0.05 
  but below 0.10; partial-effectiveness flag for P2 inspection." |
```

This is not a BLOCKING change; it augments the existing WARN-level section. Gamora adds this as a log.warning in the smoke script alongside the existing WARN condition reporting for class_0003 / class_0006.

### Amendment 5 — OPTIONAL: Consider renaming `floor_lock_recompose` → `recompose_floor_lock`

**Rationale:** Naming consistency with `modifier_extreme_low` (modifier comes before qualifier). `recompose_floor_lock` reads as "recompose triggered by floor-lock" which better describes the boolean's semantics. `floor_lock_recompose` reads ambiguously (could mean "a floor-lock condition caused by recompose").

**This is optional** — gamora decides at implementation time. If the name is already in use in star-lord v2.12 schema planning work (I cannot verify this), the existing name takes precedence. The constraint is internal consistency only.

### Amendment 6 — REQUIRED: MIGRATION.md v1.22 template must include R11(b) round-trip clause and rocket watchpoint

**Rationale:** R11(b) cross-seam round-trip discipline. MIGRATION.md v1.22 introduces a cross-seam contract change (new nullable fields on `ClassBalanceResult` + new recompose_attempts telemetry fields). R11(b) requires either a round-trip smoke clause or an explicit justification clause.

**Required additions to § 5.4 template:**

Under "Star-lord action required":

```
**Round-trip (R11(b) obligation):** additive-nullable; existing consumer code paths tolerate 
absent keys. Isolation verified by `test_floor_lock_recompose_field_in_classbalanceresult` 
(confirms ClassBalanceResult.floor_lock_recompose is a bool at balance_class() exit, 
exercising the production path through convergence_report → ClassBalanceResult construction).
```

Under "Rocket — INFORMATIONAL" (currently implicit in "rest of entry follows v1.21 template"):

```
**Rocket watchpoint (informational):** Post-Option-B, floor-lock-recovery kits' 
composition signatures may differ materially from rocket's intended generation output 
(recompose lever reshapes the kit). This is by design. Rocket's seed-promotion logic 
should be aware that `modifier_extreme_low=False, floor_lock_recompose=True` is a 
PASS condition — the kit was recoverable via Option B and should be treated as converged 
for promotion purposes. If rocket's seed-promotion logic currently treats any 
`modifier_extreme_low=True` record as non-promotable, it should not be updated to treat 
`floor_lock_recompose=True` records similarly.
```

---

## § 6 — Open Questions for Knight-rider

**None blocking.** One informational:

The secondary loop calls `_primary_recompose_loop` a second time if a better element variant is found (line 764). Under Option B, the floor-lock detection branch will also fire on this second call if the redistributed class is still floor-locked. Gamora should confirm this double-invocation behavior is intentional and document it. Knight-rider should note this as an expected interaction in the implementation dispatch so gamora is alert to it.

---

## § 7 — Disposition + Sign-off

**APPROVE-WITH-AMEND.**

Amendments:
- **1 (REQUIRED):** Module-level `RECOMPOSE_SIGNAL_HI / RECOMPOSE_SIGNAL_LO` to replace two local literals encoding the same threshold.
- **2 (REQUIRED):** Fail-loud log entries for `current_wr ≈ 0.0` and `current_wr > RECOMPOSE_SIGNAL_HI` at `working_modifier=0.005` in the floor-lock branch.
- **3 (REQUIRED):** Minimum test count raised to 4; specific test cases enumerated above.
- **4 (RECOMMENDED):** WARN-level near-floor secondary condition (#4b) in smoke B1 script.
- **5 (OPTIONAL):** Naming consideration for `floor_lock_recompose` vs `recompose_floor_lock`.
- **6 (REQUIRED):** MIGRATION.md v1.22 template additions (R11(b) round-trip clause + rocket watchpoint).

Required amendments: 1, 2, 3, 6 (four required).
Recommended: 4 (one recommended).
Optional: 5 (one optional).

The design is sound. Gamora can implement from this brief + these amendments. No back-routing to gandalf required.

**Routing recommendation:** knight-rider folds amendments 1-4 + 6 into the gamora implementation dispatch as REQUIRED acceptance criteria; amendment 5 as gamora's discretion. Dispatch gamora for P1 implementation.

**Reviewing disciplines confirmed:** #1 ✓, #2 ✓ (with Amendment 3 caveat), #11 ✓, #12 ✓ (with Amendment 6 caveat), #13a ✓ (Amendment 1), #15 ✓, #18 ✓ (with Amendment 1), R11(b) ✓ (with Amendment 6), Pattern P7 ✓ (Amendment 2).

---

*Gate-1 critique authored 2026-05-19 by jack-ryan under DESIGN-MODE (peer collaborator at Gate-1). BLOCK authority retained but not exercised — all issues are correctness/clarity improvements that fold into the implementation dispatch without requiring gandalf re-disposition. Cite: ADR-002 (QA Gate-1 authority); REVIEW_PROCESS.md Principles 1-5; Engineering Disciplines #1, #2, #11, #12, #13a, #15, #18, R11(b); Pattern P7.*
