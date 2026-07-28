# QA PENDING — 2026-07-28 — gamora — BQ-3: the calibration-override door (Gate 2, DEV-MODE)

**Submitted by:** gamora (simulation seam)
**Reviewer requested:** jack-ryan, **DEV-MODE Gate 2, BLOCK authority — NON-WAIVABLE**
**Scope class:** WITHIN-SEAM (ADR-002) — **jack-ryan can approve directly.** All production code
changes are inside `simulation/`. One cross-seam MIGRATION entry is owed to star-lord (§6).
**Tag:** `gamora/v-bq3-calibration-door-1` @ `c067bbd`
**Repo:** `reincarnated-engine`, branch `main`. **COMMIT-NEVER-PUSH** — no push performed on either repo.
**Gate 2 is REQUIRED and I have NOT self-cleared it.**

---

## What was built, and why the shape is unusual

**Run:** KIT-CAL-1 (`KC1-2026-07-27`), build item **BQ-3**. Charter
`gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.6/§14.8.

Matt RATIFIED the two player-side carve-out closures my own G-5b census specified
(`gamora/notes/2026-07-28-kitcal1-g5b-sim-opposition-census.md` §5.3) — **with a hard amendment
(verbatim):**

> *"I agree, but ultra-think and implement whatever is needed to ensure these lines/values are
> NEVER used in the sim/pipeline. We need to build out real mechanisms and fit them to the kits in
> the future."*

The feature itself is ~9 lines: an optional `max_hp` on `entity_from_class_dict` and an optional
defence block on `combatant_projection_from_class_dict`, so a KIT-CAL-1 harness can express the GD
play-test-v1 R2 fixture's measured **759→1600** HP pool and gear defence — values the engine cannot
otherwise reach (player `max_hp` is derived with a 10,000 floor; projection-path defence is
hardcoded to zeros).

**The containment is the deliverable, not the wiring.** The failure mode the amendment defends
against is not a wrong number — it is a *correct* number arriving through the wrong door, and
thereby becoming a permanent, silent, cheap substitute for the player-defence and player-HP
mechanisms the engine still owes. Please review §3 hardest.

**Math note (Discipline #1, landed BEFORE any code):**
`reincarnated-engine/src/reincarnated/simulation/math/bq3-calibration-override-door-2026-07-28.md`

---

## Commits in review (4, in order — all engine repo)

| Commit | Milestone |
|---|---|
| `9605fd8` | math note (containment design, `max_hp`-floor argument, pre-registered digest, LOUD-FLAGs) |
| `9e78649` | implementation — new `calibration_overrides.py` + 5 wiring sites |
| `0fd8a8e` | test suite (39) + `simulation/MIGRATION.md` cross-seam entry |
| `c067bbd` | AGENT_STATE SESSION 77 |

Files touched (production): `simulation/spatial_gauntlet/calibration_overrides.py` (**new**),
`spatial_resolver_adapter.py`, `spatial_engine.py`, `spatial_telemetry.py`, `gauntlet_modes.py`,
`simulation/t4_sim_cycling.py`.

---

## 1. The judgement call I most want reviewed: I OVERRULED MY OWN CENSUS

Census §5.3 proposed soft-reading the **existing** `class_dict["defense"]` block, on the argument
that *"the `defense` key already exists in the kit compiler's output, so no new contract is
invented."*

**I now believe that argument is inverted, and I did not implement it.** The kit compiler emits
`"defense": {"riders": []}` on **every** compiled kit (`kit_compiler.py:630`). Hanging override
semantics on a live, production-emitted key means that the day rocket or the compiler starts
emitting a real `defense.armor` — **which is precisely the "real mechanism" Matt's amendment says
is still owed** — that mechanism *silently activates the calibration door in production*, and every
symptom of it looks like the mechanism working correctly.

Implemented instead: one namespaced key `class_dict["_calibration_overrides"]`, emitted by nothing,
colliding with nothing, underscore-prefixed (this codebase's own "not resolver-consumed" convention,
`kit_compiler.py:601-604`). `T-3d` asserts a `defense` block carrying `armor: 9999` is **inert**.

**Please rule on whether overruling the census here was correct.** It is the only design decision in
this build that departs from what was ratified as described, and it is deliberate rather than
incidental.

## 2. Empirical claims — all self-reported, please verify first-hand (Discipline #11)

| Claim | Evidence | How to re-run |
|---|---|---|
| Byte-identity on production paths | digest `25c212eb584a65fcca5ebbdd217b8206b841aa0dd4e829aa4c78ea35c67dcebc` unchanged | `pytest tests/test_bq3_calibration_override_door.py::TestByteIdentity -q` |
| The digest is genuinely **pre-registered** | captured on `c96323b` with **zero files touched**, then written into the test as a constant | `git stash` the four commits and recompute (the fingerprint rig is reproduced inside the test file) |
| Flag alone is inert (door open, no block) | `T-9`, same digest | same |
| Zero regression | sim-adjacent selection: 1,578 passed; **55 FAILED/ERROR entries diff-EMPTY** vs a `git stash` baseline on the identical selection | `pytest tests/ -q -k "spatial or gauntlet or convergence or kit_compiler or telemetry or balance or resolver or combatant or wave"`, before/after |
| Smoke gate (Discipline #2) | KF-4 kit-compiler smoke **36 GREEN / 0 RED / 1 known GAP — SMOKE PASS** | `python3 -m reincarnated.simulation.kit_compiler.smoke_kf4_compiler` |
| New suite | **39/39 pass** | `pytest tests/test_bq3_calibration_override_door.py -q` |

The smoke gate is worth noting for a specific reason: it drives the **real** kit compiler, whose
`class_dict` carries the production `defense` key — so L1's non-wiring is proven against the actual
production emitter, not only against a hand-built fixture.

## 3. Containment — six layers. Please attack these.

| Layer | Mechanism | Test |
|---|---|---|
| L1 | ONE namespaced key `_calibration_overrides`; `defense` NOT wired | `T-3d`, `T-8c` |
| L2 | keyword-only `allow_calibration_overrides=False` at all three player-building entries | `T-9` |
| **L3** | **present-but-not-allowed is a CRASH** (`CalibrationOverrideLeak`) — a dict carrying the block **cannot be simulated at all** by a non-opted-in path. Unknown sub-keys + out-of-domain values also raise. Refuses to half-apply on the full-object path. | `T-3a/b/c/e`, `T-4` (15 cases) |
| L4 | **unconditional** negative asserts (no opt-in parameter exists) at `ConvergenceUsageMode.run_slot`, `.run_slot_smoke`, `_run_kit_slot_worker`, `t4_sim_cycling._w4g_run_fight_batch` | `T-7a/b/c/d` |
| L5 | static **AST** sweep (not grep — docstrings necessarily quote the flag name) for `allow_calibration_overrides=True`; allow-list **EMPTY at landing** | `T-8`, non-vacuity proved by `T-8b` |
| L6 | output stamping on `SpatialFightResult` | `T-2`, `T-6`, `T-6b` |

**L3 is the layer I consider load-bearing** and the one I would most like challenged: it is what
converts the door from *conventional* (production must remember not to pass the flag) to
*structural* (production **cannot** run a block-bearing dict at all, flag or no flag).

**Deliberately NOT built:** environment variable, global module flag, runtime registry. Each is
process state a production run could inherit accidentally. The opt-in is a call-site argument and
nothing else. If you think one of those would be stronger, say so.

## 4. Semantic shift, declared (Discipline #12)

**Inside the door, player `max_hp` stops being a pure function of `(vitality, strength)`.** That
invariant has held on every path since the spatial engine existed. Outside the door it holds
bit-for-bit (§2).

The override is applied **VERBATIM — deliberately NOT `max(floor, override)`.** Reasoning (math note
§1.2): `HP_BASE = 10,000` is a *balance anchor* (calibrated against `CLASS_HP_REFERENCE = 20,000`
and per-hit magnitudes 625/1500/2500), not a numerical-stability floor — nothing divides by it, and
the only hard requirement is `max_hp > 0` (`hp_pct = hp / max_hp`, `spatial_engine.py:5296`, which
the validator enforces). A `max()` would silently return 10,000 for the fixture's 759→1600 pool and
the harness would report a fixture comparison **it never actually ran**. Verbatim-or-nothing is the
honest semantics; `T-5` asserts no floor is applied.

## 5. What I deliberately did NOT fix — please confirm this was the right call

**LOUD-FLAG-1 (math note §5).** The projection player's **kernel** `CombatantState.max_hp` is
scratch `1.0`, and the engine re-syncs only `hp` (`spatial_engine.py:5140` — MEASURED). So every
resolver path reading `defender.max_hp` for the player — execute threshold
(`damage_resolver.py:977`), freeze-shatter (`effect_resolver.py:140`), leech/heal caps
(`:1203,1259`) — computes `hp_frac ≫ 1` and those mechanics never fire on the player. **This
pre-exists BQ-3 by a year of commits.**

I did not extend the override there. Two reasons: (a) outside census scope and outside Matt's
ratification; (b) the real one — it would make a `max_hp` override silently **enable mechanics that
the no-override path leaves dormant**, which is exactly the "override quietly becomes the mechanism"
hazard the amendment forbids. A harness needing player-side execute/shatter fidelity must raise it
as its own item.

## 6. Cross-seam (Principle 6) — star-lord ACTION OWED; rocket owes NOTHING

Two additive fields on `SpatialFightResult` (the carrier every `export/schemas.py` builder is
constructed from — named explicitly because the 2026-07-26 entry got this wrong and it cost a
BLOCK):

- `calibration_overrides_used: bool = False`
- `calibration_override_fields: str = ""`

Plus `"calibration_overrides_used": bool` on the `run_spatial_fight` aggregate dict.

**MIGRATION §2 carries the part that is not optional:** any analysis, export, band-fit or aggregate
that mixes `calibration_overrides_used = True` rows into a production population is **INVALID**;
star-lord's read path should filter `= 0` by default and surface the field list wherever provenance
is displayed.

**Rehydration is SAFE here, unlike `liveness_gate_version`** — and I checked rather than assumed,
because you found that hazard at SESSION 76. `SpatialFightResult(**archived_pre_BQ3_row)` yields
`False`/`""`, which is **true** for every such row: there is no era in which a row could have been
calibration-stamped and then lost the field, so absence is unambiguous. No pre-splat normalisation
idiom is owed for these two fields. Asserted by `T-2b`, which states the property so a future "fix"
to the default has to argue against a test rather than silently win.

## 7. Decisions-log — one entry proposed (jack-ryan to draft; capture, not gate)

**Calibration-override door is a debt marker with a scheduled deletion.** The door exists only until
real player-defence and player-HP mechanisms land; at that point `_calibration_overrides` should be
**deleted, not migrated**, and L5's allow-list is the inventory of everything needing re-pointing
(math note §5 LOUD-FLAG-3). Recording this now is what keeps the door from quietly becoming the
mechanism.

## 8. Seed hygiene (Discipline #3)

BQ-3 band **74M**; new fights `74_000_100+`. `730_010_001` is a deliberately frozen pre-change
baseline seed and must not move. **Next-free: `74_000_200+`.**

## References

- Math note: `reincarnated-engine/src/reincarnated/simulation/math/bq3-calibration-override-door-2026-07-28.md`
- Containment module: `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/calibration_overrides.py`
- Tests: `reincarnated-engine/tests/test_bq3_calibration_override_door.py`
- MIGRATION: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-28 entry)
- Census (the thing I partly overruled): `agentic_orchestration/gamora/notes/2026-07-28-kitcal1-g5b-sim-opposition-census.md` §5.2/§5.3
- Charter: `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.6/§14.8
- Completion record: `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` SESSION 77 @ `c067bbd`
