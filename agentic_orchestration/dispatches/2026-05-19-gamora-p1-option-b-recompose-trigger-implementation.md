# Dispatch — 2026-05-19 — gamora — Option B recompose-trigger re-conditioning IMPLEMENTATION (P1)

**Status:** ACTIVE — fires immediately to gamora on knight-rider routing.
**Authority on activation:** AUTONOMOUS L1 within engine-sim seam per engine-rebuild protocol § 4.0 + recompose-validation hive § 4.1.
**Author:** knight-rider, folding gandalf design brief + jack-ryan Gate-1 amendments
**Date:** 2026-05-19

**Predecessor / dependency:**
- `agentic_orchestration/dispatches/2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` (P0, landed in `recompose-hive/v0.1-option-a-floor-widened` — Option A floor widening)
- `agentic_orchestration/dispatches/2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md` (P1 design brief — gandalf's authored brief; primary design source for this implementation)
- `agentic_orchestration/qa/pending/2026-05-19-p1-option-b-recompose-trigger-gate1.md` (jack-ryan Gate-1 critique — APPROVE-WITH-AMEND; six amendments folded into this dispatch)

---

## § 1 — TL;DR

Implement Option B: re-condition the recompose trigger in `_primary_recompose_loop` so it detects floor-lock-post-Option-A (`_quick_modifier_estimate` exited with `last_wr > RECOMPOSE_SIGNAL_HI`), overrides the lever working modifier to a sub-floor probe value (`LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005`), and lets levers find DPS-sensitivity signal. This is the architectural completion of Option A: P0 unblocked the binary search range; P1 unblocks the lever evaluation signal range.

**Scope: single touch site (`_primary_recompose_loop`) + two new named constants + one ClassBalanceResult field + three new per-attempt telemetry fields + MIGRATION.md v1.22 + four unit tests + smoke gate B1 cold-start on class_0001.**

All four jack-ryan Gate-1 REQUIRED amendments + one RECOMMENDED + one OPTIONAL are folded in below. The optional one (Amendment 5: naming) is gamora's discretion.

---

## § 2 — Required reading (gamora)

1. `agentic_orchestration/dispatches/2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md` — **the primary design source.** Read in full. § 2 (math), § 3 (implementation scope), § 4 (smoke B1), § 5 (cross-seam), § 6 (Discipline #12 framing), § 8 (out-of-scope), § 9 (reversibility).
2. `agentic_orchestration/qa/pending/2026-05-19-p1-option-b-recompose-trigger-gate1.md` — **jack-ryan Gate-1 critique with amendments enumerated.** Read § 5 (Amendments) in full.
3. `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` — verify current state post-Option-A. Key landmarks per jack-ryan § 1: constants block near line 70; `ClassBalanceResult` at line 324; `balance_class()` primary recompose call at line 699; secondary loop recompose call at line 764; `_quick_modifier_estimate` at line 1288 (`_SIGNAL_LO, _SIGNAL_HI = 0.30, 0.70` local at line 1308); `_primary_recompose_loop` at line 1323 (direction check at line 1351-1365; lever loop at line 1374-1401).
4. `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md` § 4-5 — Options A/B math foundation.
5. `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.21 — template for v1.22 entry.
6. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1, #2, #11, #12, #13a, #15, #18, R11(b), Pattern P7 (the anchors this dispatch invokes).

---

## § 3 — Implementation scope

### § 3.1 — Code changes in `balance_loop.py`

**Single touch site for the implementation proper:** `_primary_recompose_loop` (line 1323).

**Per gandalf brief § 3.1 + jack-ryan Amendments 1, 2:**

#### (a) Module-level named constants (Discipline #18; Amendment 1 REQUIRED)

Add at the module-level constants block near line 70 (alongside `RECOMPOSE_QUICK_ITERS`, `MODIFIER_LOW_THRESHOLD`, etc.):

```python
# ── B14.5 recompose signal-range bounds (same pair used by both
# _quick_modifier_estimate and the Option-B floor-lock detection in
# _primary_recompose_loop). Single source of truth per Discipline #18.
#
# RECOMPOSE_SIGNAL_LO: float = 0.30   — lower bound; below → kit too weak; lever
#                                       evaluation signal range is unreachable
# RECOMPOSE_SIGNAL_HI: float = 0.70   — upper bound; above → kit saturates the
#                                       gauntlet; lever deltas → 0
#
# Promoted from two local literals (one in _quick_modifier_estimate, one
# proposed in _primary_recompose_loop's Option-B branch) to a single named
# pair 2026-05-19 (Option B implementation; jack-ryan Gate-1 Amendment 1).
#
# Semantic shift (Discipline #12): the recompose direction-trigger's
# effective signal range is the same range _quick_modifier_estimate uses
# for early-exit. Making this explicit prevents future drift if the
# range is empirically tuned (jack-ryan critique § 2 Discipline #13a).
RECOMPOSE_SIGNAL_LO: float = 0.30
RECOMPOSE_SIGNAL_HI: float = 0.70
```

Then refactor `_quick_modifier_estimate` (line 1308) to use these constants instead of the local `_SIGNAL_LO, _SIGNAL_HI = 0.30, 0.70`. Same behavior; correct single-source.

#### (b) New named constant `LEVER_FLOOR_LOCK_WORKING_MODIFIER` (Discipline #18)

Add at module-level constants block near `MODIFIER_LOW_THRESHOLD` (full docstring per gandalf brief § 3.2; ~25 LOC including doc):

```python
# ── Option B floor-lock recovery (2026-05-19) — Discipline #18 named constant ─────
# Sub-floor working modifier used by recompose levers when _quick_modifier_estimate
# could not reach signal range (last_wr > RECOMPOSE_SIGNAL_HI) at the search floor.
# [... full docstring per gandalf brief § 3.2; carry verbatim ...]
LEVER_FLOOR_LOCK_WORKING_MODIFIER: float = 0.005
```

#### (c) Floor-lock detection branch in `_primary_recompose_loop` (gandalf brief § 3.1; ~30 LOC + Amendment 2 logging)

After `_quick_modifier_estimate` returns (line 1351), before the direction check (line 1356):

```python
eval_modifier, current_wr = self._quick_modifier_estimate(
    player_class, gauntlet, fights_per_matchup, target_winrate
)

# ── Option B (2026-05-19): floor-lock-post-Option-A detection ─────────
# If _quick_modifier_estimate could not reach signal range at the search
# floor, lever evaluation needs a sub-floor working modifier to find
# DPS-sensitivity. Otherwise levers run at a saturated WR ceiling and
# all deltas are 0.0 (the trap diagnosed pre-Option-A; persists post-A
# for kits whose true m* < MODIFIER_SEARCH_FLOOR). See MIGRATION.md v1.22
# and gandalf brief § 2.
floor_lock_detected = current_wr > RECOMPOSE_SIGNAL_HI
working_modifier = eval_modifier
if floor_lock_detected:
    working_modifier = LEVER_FLOOR_LOCK_WORKING_MODIFIER
    # Re-evaluate WR at the sub-floor working modifier so levers see the
    # real baseline they will be measured against.
    current_wr, _, _, _ = self._evaluate_class(
        player_class, gauntlet, fights_per_matchup, working_modifier
    )
    # Pattern P7 silent-default watch (Amendment 2): fail-loud on the
    # two distinguishable failure modes at the probe value so kit-redesign
    # candidates can be triaged from run-log without per-class telemetry inspection.
    if current_wr > RECOMPOSE_SIGNAL_HI:
        log.debug(
            "Class %s: floor_lock_detected but still saturated at working_modifier=%.4f "
            "(WR=%.4f > SIGNAL_HI=%.2f). Levers will find no signal; "
            "kit-redesign-queue candidate.",
            player_class.id, working_modifier, current_wr, RECOMPOSE_SIGNAL_HI,
        )
    elif current_wr < RECOMPOSE_SIGNAL_LO / 2:
        log.debug(
            "Class %s: floor_lock_detected but over-suppressed at working_modifier=%.4f "
            "(WR=%.4f < 0.15). Levers will reject reduce_dps direction; "
            "kit-redesign-queue candidate.",
            player_class.id, working_modifier, current_wr,
        )

# Determine recompose direction from modifier magnitude (UNCHANGED).
# Direction uses eval_modifier (search-space value), not working_modifier
# (probe value). This preserves the semantic that direction reflects
# where the binary search wants to go.
if eval_modifier < MODIFIER_LOW_THRESHOLD:
    reduce_dps = True
    # ... rest unchanged
```

Lever loop (line 1374): replace `eval_modifier` with `working_modifier` in the lever-call positional arg.

Per-attempt telemetry record (line 1382 area): add two fields per gandalf brief § 3.3 + Amendment 1 (uses module-level constant):

```python
"eval_modifier": round(eval_modifier, 4),           # unchanged semantics
"working_modifier": round(working_modifier, 4),      # NEW — equal to eval_modifier unless floor_lock_detected
"floor_lock_detected": floor_lock_detected,          # NEW — bool
```

#### (d) `ClassBalanceResult` new field (gandalf brief § 3.3; Amendment 5 OPTIONAL naming)

```python
floor_lock_recompose: bool | None = None   # True if Option-B floor-lock-recovery fired (default None for pre-Option-B back-compat)
```

**Amendment 5 (OPTIONAL — gamora's discretion):** consider renaming `floor_lock_recompose` → `recompose_floor_lock` for consistency with `modifier_extreme_low` convention (modifier/condition before qualifier). Default to gamora's judgment. If renamed, update all references in the dispatch + brief consistently.

### § 3.2 — Test additions (Amendment 3 REQUIRED — raised from "≥ 3" to "exactly 4 specific cases")

Add to `tests/test_balance_loop.py`. Minimum four test cases, ~30-50 LOC total:

1. **`test_floor_lock_detected_fires_when_saturated`** — mock `_quick_modifier_estimate` to return `(0.011, 0.98)` (floor-proximity + saturated WR); run `_primary_recompose_loop`; assert at least one attempt has `floor_lock_detected=True` AND `working_modifier == LEVER_FLOOR_LOCK_WORKING_MODIFIER`.

2. **`test_floor_lock_not_detected_when_signal_reached`** — mock `_quick_modifier_estimate` to return `(0.012, 0.55)` (floor-proximity but signal-range WR); run `_primary_recompose_loop`; assert all attempts have `floor_lock_detected=False` AND `working_modifier == eval_modifier`.

3. **`test_floor_lock_recompose_field_in_classbalanceresult`** — integration-style (full `balance_class()` call on a constructed/mocked floor-locked class); assert `result.floor_lock_recompose` is a `bool` (not `None`).

4. **`test_floor_lock_telemetry_records_working_modifier`** — verify that when `floor_lock_detected=True`, recompose_attempts records both `working_modifier=0.005` AND `floor_lock_detected=True` correctly; verify that `eval_modifier` is still the original `_quick_modifier_estimate` output (not the probe value).

Tests 1 and 2 require mocking `_evaluate_class` (monkeypatch pattern; existing patterns in `tests/test_balance_loop.py` apply).

### § 3.3 — MIGRATION.md v1.22 entry (Amendment 6 REQUIRED additions folded in)

File at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`. Use gandalf brief § 5.4 template; add Amendment 6 clauses verbatim:

#### Star-lord obligation section (template + R11(b) clause):

> **Star-lord action required:** YES (schema v2.13)
>
> Add nullable columns to `class_balance_results` (or equivalent target table):
> - `floor_lock_recompose` (bool, nullable)
> - per-attempt records in `recompose_attempts_json`: new keys `working_modifier` (float), `floor_lock_detected` (bool) — nullable / absent in pre-Option-B rows
>
> Update query patterns:
> - `WHERE floor_lock_recompose = TRUE` → Option B served population
> - `WHERE floor_lock_recompose = TRUE AND status = 'converged' AND final_balance_modifier >= 0.05` → Option B success population
> - `WHERE floor_lock_recompose = TRUE AND status = 'converged' AND final_balance_modifier < 0.05` → Option B partial-success (design-review flag)
> - `WHERE floor_lock_recompose = TRUE AND status = 'failed'` → Option B did not save the kit (kit-redesign queue candidate)
>
> Sub-bucketing:
> - `recompose_fire_count_total` — sum of all firings (existing)
> - `recompose_fire_count_floor_lock` — NEW; subset where `floor_lock_detected=True` for at least one attempt
>
> **Round-trip (R11(b) obligation):** additive-nullable; existing consumer code paths tolerate absent keys. Isolation verified by `test_floor_lock_recompose_field_in_classbalanceresult` (confirms `ClassBalanceResult.floor_lock_recompose` is a bool at `balance_class()` exit, exercising the production path through `convergence_report → ClassBalanceResult` construction).

#### Rocket obligation section (explicit, not implicit):

> **Rocket watchpoint (informational):** Post-Option-B, floor-lock-recovery kits' composition signatures may differ materially from rocket's intended generation output (recompose lever reshapes the kit). This is by design. Rocket's seed-promotion logic should be aware that `modifier_extreme_low=False, floor_lock_recompose=True` is a PASS condition — the kit was recoverable via Option B and should be treated as converged for promotion purposes. If rocket's seed-promotion logic currently treats any `modifier_extreme_low=True` record as non-promotable, it should NOT be updated to treat `floor_lock_recompose=True` records similarly.

### § 3.4 — Documentation discipline

- Module-level docstring on `LEVER_FLOOR_LOCK_WORKING_MODIFIER` per gandalf brief § 3.2 (Discipline #18; ~25 LOC docstring covering rationale, semantic-shift framing, reversibility, cross-refs).
- Module-level docstring pair on `RECOMPOSE_SIGNAL_LO`/`RECOMPOSE_SIGNAL_HI` covering single-source-of-truth + Discipline #13a drift watch motivation (~15 LOC).
- Inline comments in `_primary_recompose_loop` floor-lock branch citing MIGRATION.md v1.22 + gandalf brief.

### § 3.5 — Secondary loop interaction (jack-ryan § 6 informational)

The secondary loop at lines 717-775 in `balance_class()` calls `_primary_recompose_loop` a second time (line 764) when a better element variant is found. Under Option B, this second call will also execute the floor-lock-detection branch if the element-variant class is still floor-locked. **This is intentional and correct** — the secondary loop's second pass should also benefit from Option B.

**Gamora obligation:** verify the double-invocation works as expected via the existing integration test surface (the existing `test_balance_loop.py` tests that exercise secondary-loop paths should continue to pass; the floor-lock detection should fire correctly in both first-pass and second-pass invocations). Document the interaction in AGENT_STATE.md completion record. No additional test required beyond Amendment 3 test #3.

---

## § 4 — Smoke gate B1 (gandalf brief § 4 + Amendment 4 RECOMMENDED)

### § 4.1 — BLOCKING (gandalf brief § 4.2; ALL FOUR must hold)

Cold-start single-class convergence on **class_0001 from season_100002** (the canonical floor-locked test class; continuity with P0 A1 smoke). Cold-start: `initial_modifier=1.0` (NOT warm-started from prior `final_modifier=0.0509`).

Verify via `recompose_attempts` telemetry on the result:

| # | Condition | Verification |
|---|---|---|
| 1 | `floor_lock_detected=True` recorded in at least one recompose_attempt | Direct field check on serialized telemetry |
| 2 | At least one recompose_attempt has `working_modifier=LEVER_FLOOR_LOCK_WORKING_MODIFIER (0.005)` | Direct field check |
| 3 | At least one recompose_attempt has `before_winrate < 0.95` AND `accepted=True` AND `\|delta\| ≥ RECOMPOSE_DELTA_FLOOR (0.02)` | Lever found traction (signal reached) AND was accepted AND delta is meaningful |
| 4 | Post-recompose binary search converges with `final_modifier > MODIFIER_SEARCH_FLOOR (0.01)` AND `modifier_extreme_low=False` (i.e., `final_modifier ≥ 0.05`) | Recompose reduced DPS density enough that class no longer needs sub-0.05 modifier |

**All four BLOCKING. Any one fails → P1 rolls back per § 6 reversibility.**

### § 4.2 — WARN-level secondary checks (gandalf brief § 4.3 + Amendment 4 RECOMMENDED)

WARN-level secondary on **class_0003 (earth_controller) + class_0006 (fire_controller) from season_100002**:

| Condition | Action |
|---|---|
| At least one lever produces non-zero delta at working_modifier=0.005 | Direct field check |
| Recompose succeeds AND binary search converges with `final_modifier > 0.01` | Count toward "Option B effective" population |
| Recompose succeeds but boss-tier WR still fails post-convergence | Flag class as "kit-redesign candidate (boss-tier orthogonal)" |
| Recompose fails (no lever accepted at working_modifier=0.005) | Flag class as "Pattern-A confirmed (lever-irrecoverable)" |

**Amendment 4 RECOMMENDED addition:** for class_0001, if post-recompose `final_modifier ∈ [0.05, 0.10)`, log WARNING: *"Option B marginal recovery — modifier above 0.05 but below 0.10; partial-effectiveness flag for P2 inspection."* This is not BLOCKING; it augments the existing WARN section for early-signal on partial-effectiveness.

### § 4.3 — Test suite regression check

`pytest tests/test_balance_loop.py tests/test_range_profile.py` — verify no existing test fails. The new test cases from Amendment 3 (§ 3.2 four cases) should all PASS.

### § 4.4 — Total smoke effort

- BLOCKING (Mode-1): class_0001 cold-start single-class convergence — ~5 min wall time
- WARN-level (Mode-2): class_0003 + class_0006 cold-start single-class — ~10 min wall time
- Test suite (Mode-3): pytest — ~2 min wall time

**Total: ~20 minutes.** No diagnostic-season-stop-gap regen at P1; P2 is the dedicated venue for season-level diagnostic regen under both Options A and B.

### § 4.5 — Falsifying condition (when P1 rolls back, gandalf brief § 4.4)

P1 rolls back if any of:

1. Smoke gate B1 BLOCKING fails on class_0001 (any of the four BLOCKING conditions misses) — implementation diagnosis is wrong; the working-modifier-at-0.005 mechanism does not unlock lever signal.
2. B1 passes on class_0001 but `floor_lock_detected=True` fires for > 50% of classes across class_0001, class_0003, class_0006 — re-condition threshold is too aggressive (false-positive on legitimately-converging-at-floor classes); revisit `RECOMPOSE_SIGNAL_HI` value or signal logic.
3. Existing test suite regression (any test in `tests/test_balance_loop.py` or `tests/test_range_profile.py` that previously passed now fails) — implementation correctness regression.

If rollback fires: revert per § 6 (full git revert OR parameter-level soft-disable). Surface to knight-rider via hive log FRICTION entry IMMEDIATELY.

---

## § 5 — Acceptance criteria

- [ ] Module-level named constants `RECOMPOSE_SIGNAL_LO=0.30` + `RECOMPOSE_SIGNAL_HI=0.70` added with docstring (Amendment 1)
- [ ] `_quick_modifier_estimate` refactored to use the named constants (Amendment 1)
- [ ] Module-level named constant `LEVER_FLOOR_LOCK_WORKING_MODIFIER=0.005` added with full docstring per gandalf brief § 3.2 (Discipline #18)
- [ ] `_primary_recompose_loop` floor-lock detection branch added per § 3.1(c) — `last_wr > RECOMPOSE_SIGNAL_HI` signal; `working_modifier=LEVER_FLOOR_LOCK_WORKING_MODIFIER` override; `current_wr` re-evaluation
- [ ] Fail-loud log entries for `current_wr > RECOMPOSE_SIGNAL_HI` AND `current_wr < RECOMPOSE_SIGNAL_LO / 2` cases (Amendment 2)
- [ ] Lever loop uses `working_modifier` (not `eval_modifier`) when calling lever functions
- [ ] `recompose_attempts` records gain `working_modifier` + `floor_lock_detected` fields per attempt
- [ ] `ClassBalanceResult.floor_lock_recompose: bool | None = None` field added (Amendment 5 OPTIONAL: consider renaming to `recompose_floor_lock`; gamora's call)
- [ ] Four unit tests added per Amendment 3 § 3.2 (test cases 1-4 specific)
- [ ] Smoke gate B1 BLOCKING (§ 4.1) — all four conditions PASS on class_0001 cold-start
- [ ] Smoke gate B1 WARN-level (§ 4.2) — class_0003 + class_0006 cold-start single-class executed; outcomes documented
- [ ] Smoke gate B1 Amendment 4 WARN-level near-floor secondary (`final_modifier ∈ [0.05, 0.10)` log warning) implemented in smoke script
- [ ] Test suite regression check: `pytest tests/test_balance_loop.py tests/test_range_profile.py` — all PASS (§ 4.3)
- [ ] MIGRATION.md v1.22 entry per § 3.3 — gandalf brief § 5.4 template + Amendment 6 R11(b) round-trip clause + explicit rocket watchpoint section
- [ ] AGENT_STATE.md updated with completion record + secondary loop interaction documentation (§ 3.5)
- [ ] Hive log STATE entry at completion (fetch-before-commit discipline)
- [ ] Knight-rider notified — knight-rider verifies smoke B1 BLOCKING all-PASS; fires `gamora/v1.14-balance-loop-option-b-recompose-conditioned` seam tag + `recompose-hive/v0.2-option-b-recompose-conditioned` hive milestone tag (engine + collab)

---

## § 6 — Reversibility (gandalf brief § 9)

**Option 1 (full revert):** remove the floor-lock-detection branch + named constants + telemetry fields + ClassBalanceResult field via single git revert. Telemetry-table schema additions stay as nullable columns indefinitely. No persistent data depends on Option B behavior.

**Option 2 (parameter-level soft-disable):** set `LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR` (0.01). Floor-lock branch fires (and the diagnostic telemetry still records `floor_lock_detected=True` for instrumented classes), but `working_modifier` equals `eval_modifier` so lever evaluation reverts to pre-Option-B behavior. This is the soft-disable path — preserves diagnostic telemetry while disabling the behavioral change.

**Revert triggers:**
- Smoke gate B1 BLOCKING fails per § 4.5 → immediate full revert
- P2 fresh diagnostic regen surfaces a defect where Option B produces unbalanced kits in a different failure mode → surface to gandalf for re-disposition; soft-disable via option 2 until disposition
- P3 validation verdict CANNOT REJECT NULL → surface to Matt with Option B sub-population's behavior analyzed (wind-down trigger #3)

---

## § 7 — Out-of-scope (HARD; per gandalf brief § 8)

1. Bidirectional levers / DPS-increase forced working modifier for ceiling-locked classes — B-prime scope; deferred
2. Changes to `MODIFIER_SEARCH_FLOOR` or `MODIFIER_SEARCH_CEILING` — Option A is settled
3. Changes to `_quick_modifier_estimate` internal logic — only adding shared named-constant usage (Amendment 1); internal algorithm unchanged
4. Full-season regen at P1 — P2 is the dedicated venue
5. New lever types beyond `skill_swap` / `geometry_mix` / `cooldown_energy`
6. Changes to rocket b6_kit_builder / b6_archetype_templates / skill generation
7. Changes to per-tier WR targets / floors / ceilings — R1 disposition settled
8. Changes to `RECOMPOSE_DELTA_FLOOR = 0.02` — lever delta meaningfulness threshold unchanged
9. Doppelganger / experimental classes — `DOPPELGANGER_MODIFIER_FLOOR = 0.30` unchanged; experimental classes still skip recompose
10. New `recompose_outcome` enum values — `"primary_loop_converged"` covers Option-B-success case

---

## § 8 — Cross-seam impact

- **Star-lord:** schema v2.13 obligations per § 3.3 MIGRATION.md v1.22 entry (additive nullable). Picked up at P2 telemetry work; no immediate blocker.
- **Rocket:** informational watchpoint per § 3.3 (composition signatures of floor-lock-recovery kits may differ from generation output; `modifier_extreme_low=False, floor_lock_recompose=True` is a PASS for seed-promotion).
- **Drax:** no impact. Modifier values are engine-internal; no loadout UI consumes them.
- **Knight-rider:** verifies smoke B1 BLOCKING all-PASS on completion; fires both tags; routes P2 phase authoring (gandalf picks substrate; knight-rider authors rocket + star-lord + gamora dispatch).

---

## § 9 — Tag plan

`gamora/v1.14-balance-loop-option-b-recompose-conditioned` — intermediate seam tag at completion.
`recompose-hive/v0.2-option-b-recompose-conditioned` — P1 hive milestone tag, fired by knight-rider on smoke B1 BLOCKING all-PASS pass (engine + collab).

---

## § 10 — References

**Predecessors:**
- `agentic_orchestration/dispatches/2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md` (gandalf design brief — primary design source)
- `agentic_orchestration/qa/pending/2026-05-19-p1-option-b-recompose-trigger-gate1.md` (jack-ryan Gate-1 — amendments folded into this dispatch)
- `agentic_orchestration/dispatches/2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` (P0)

**Investigation:**
- `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md` § 4-5

**Hive:**
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` § 3 P1 + § 6 P1
- `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md` § 2 P1 acceptance gate
- `agentic_orchestration/hive-mind/recompose-validation-log.md`

**Code:**
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py`
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- `tests/test_balance_loop.py`
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`

**Engineering disciplines anchored:**
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #1 (math-before-code; gandalf § 2), #2 (smoke-test; § 4 + Amendment 3), #11 (empirical inspection; § 5.1 telemetry sub-bucketing), #12 (semantic shift; § 6 framing), #13a (implicit-pillar drift; Amendment 1), #15 (drift-detection; implicit-precondition framing § 2.2 + § 6.2), #18 (named constants; Amendments 1 + § 3.1(b)), R11(b) (cross-seam round-trip; Amendment 6), Pattern P7 (silent-default; Amendment 2)

---

*Authored 2026-05-19 by knight-rider, folding gandalf design brief (`a400436`) + jack-ryan Gate-1 amendments (`93c2a29`). All 4 REQUIRED amendments folded as acceptance criteria; 1 RECOMMENDED added as smoke-script feature; 1 OPTIONAL left to gamora's discretion. The lever sharpens; the road continues. Gamora: execute under AUTONOMOUS L1 within engine-sim seam.*
