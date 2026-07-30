# WR2-ENCGEO Cell B — combatant body separation (Mechanism B) + surface-to-surface range

**Run:** WR2-ENCGEO-2026-07-29 · **Cell:** B · **Seam:** gamora · **Date:** 2026-07-29
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` §1 mechanism B
**Build contract:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-mechanism-spec.md` §B / §D / §E / §G
**Math note:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wr2-b-body-separation-2026-07-29.md`
**Rulings applied:** R-WR2-3, -7, -8, -11, -12, -14 · **Baseline pin:** `9bfbdda`+ (jack-ryan Gate-2 INFO-1)
**Engine commit (NOT PUSHED):** `6dca36a`
**Status:** build COMPLETE. **⚑ HALT ON S-1.** Nothing graded — the cell computes, the conductor grades.

---

## Verdict table

| # | Gate-2 deliverable | verdict |
|---|---|---|
| 1 | **S-1** — min pairwise LIVING separation ≥ rᵢ+rⱼ − 1 cm, every tick, 450 fights | **FAIL — 129/450 traces pass; worst slack −0.252 m. ⚑ HALT, §HALT** |
| 2 | **S-4** — battery byte-reproducible at fixed seed, twice | **PASS — 450/450, all three legs** |
| 3 | `collision_residual_ticks` / `_max_m` reported (expected 0, 0) | **REPORTED — 95,852 and 0.28018. NOT the expected value; same mechanism as (1)** |
| 4 | Flag-OFF full regression byte-identical, name-diff vs the 81-name baseline | **PASS — `removed=0 added=0`** (§4) |
| 5 | Shuffled-order test (§D-2) — results DIFFER | **PASS** |
| 6 | D-3 grep sweep — entity membership converted to identity | **DONE — 66 compares audited, 2 entity hits, both converted; re-sweep = 0** |
| 7 | Math note (D-2 invariant + named bias, D-3 results, convergence argument) | **DONE** |
| 8 | Unit tests (predicate / split / dead-exempt / coincident / clamp / defaults / shuffle / range) | **DONE — 40 tests, all pass** |

**SS-1 asserted mechanically, not promised.** The driver refuses at entry if its output root is
`wr1_battery_2/` or `wr1_battery_2_aim/` or a descendant. `git status --porcelain` on both banked
roots: **empty**.

---

## ⚑ HALT — S-1 fails, and the frozen parameter set cannot reach it

I am not improvising a ruling. Per the cell brief: *"If the build forces a genuine fork the spec
doesn't cover, HALT and report."* This is that fork, and it is one sentence long:

> **Spec §B-2's prose and spec §B-2's pseudocode are not the same mechanism, and the pseudocode is
> the row marked FROZEN.**

### The measurement (full armed battery, 450 fights, 3 legs, seeds 74000800×30)

| | value |
|---|---|
| traces passing S-1 (`slack ≥ −0.01 m`) | **129 / 450** |
| worst slack | **−0.25216185346109277 m** |
| violating pair-samples | 81,861 / 340,828 (24.0 %) |
| violating ticks | 81,756 / 133,848 |
| `collision_residual_ticks` | 95,852 |
| `collision_residual_max_m` | 0.28017983717899186 |

| leg | traces pass | worst slack | violating ticks |
|---|---|---|---|
| pre (`R2_proxy`) | 40 / 150 | −0.25216 | 29,035 / 46,675 |
| post (`R3`) | 49 / 150 | −0.25216 | 28,345 / 45,157 |
| pre_endpoint (`R2_proxy_resists_low`) | 40 / 150 | −0.25216 | 24,376 / 42,016 |

Per-tier `collision_residual_ticks`, identical in shape across all three legs:
**boss 60/60 fights** (max 0.2802) · **mixed_pack 30/30** (max 0.0445) · **trash 30/30** (max 0.0439)
· **champion 0/30, max 0.0**.

**The worst slack is bit-identical across every failing seed, leg and arm.** That is not noise — it
is a deterministic geometric attractor, and it is the first clue.

### The mechanism, read off the trace rather than theorised

`boss__A__seed74000700`, and the same shape on every boss seed:

```
tick  player(x,y)      boss(x,y)          d
  97  (0.5241, 0.5)    (2.2417, 1.5241)   1.9997
  98  (0.5,    0.5)    (2.0275, 1.5946)   1.8792    <- player pins to the SW corner
 101  (0.5,    0.5)    (1.7418, 1.7331)   1.7500
 102  (0.5,    0.5)    (1.7359, 1.7359)   1.7478    <- fixed point
 475  (0.5,    0.5)    (1.7359, 1.7359)   1.7478    <- held for 374 more ticks
```

The player is wall-clamped in **both** axes at (0.5, 0.5) — the corner pin WR1-ENV measured on 179
of 180 boss fights. It therefore absorbs **none** of its share. And R-WR2-7 gives the *small* body
the *large* share: `w_player = 0.90`. The free boss absorbs only `0.10` per sweep, so the surviving
gap decays as `0.90^m`, and at the frozen `ITER_MAX = 8`, **`0.90^8 = 0.43047` survives every tick**.

With `Δ` = the boss's per-tick closure and `q = 0.9^ITER_MAX`:

```
g_{k+1} = (g_k + Δ)·q                fixed point:   g* = Δ·q / (1 − q)
```

Solving from the measured `g* = 0.25216` at `q = 0.43047` gives **`Δ = 0.3335 m/tick` — a 3.335 m/s
boss, which is the scenario's actual speed.** The model reproduces the measurement to three
decimals, so the diagnosis is not a story about the numbers; it is the numbers.

Required `ITER_MAX` at this `Δ`: **≥ 34** for S-1's 1 cm; **≥ 56** for `ε_touch`'s 1 mm.

### Why this is a spec fork and not a build defect

Spec §B-2 says, of clamp-inside-the-sweep:

> "A wall-pinned body absorbs none of its share; the residual survives into the next sweep and the
> *free* body takes it. **Within two or three sweeps the free body has absorbed 100 %.**"

True when the pinned body holds the **small** share (pinned boss / free player: decay `0.10^m`,
done in one sweep — pinned by a test). **False** in the direction this run actually produces. The
prose describes a **redistribution** — the free body taking the pinned body's share — which **the
pseudocode does not implement**: nothing transfers a clamped body's unabsorbed share to its partner;
the free body only ever takes its own `w_free` of what remains.

Two corroborating facts, both measured:

* **Every S-1 violation involves a wall-clamped body.** Free-space pairs are exact to 1e-12 at every
  radius ratio, single sweep. Pinned by `test_free_space_pair_is_exact_in_one_sweep_...`.
* **`champion` is the only tier whose fight never reaches a wall, and it is the only tier with zero
  residual** — 0 ticks in 90 fights across three legs.

One mechanism, not two. The implementation matches the pseudocode line for line; the pseudocode does
not deliver the predicate.

### Candidate resolutions, costed — the conductor's ruling, not mine

| # | change | frozen row touched | effect |
|---|---|---|---|
| **R1** | **Clamp-aware shortfall transfer.** After clamping `i`, measure the realized displacement and add the shortfall `gap·wᵢ − ‖realized‖` to `j`'s correction, inside the same sweep. | solver type/order | Exactly what §B-2's prose already describes. Converges the pinned 2-body pair in **one** sweep: player realizes 0, boss takes the whole gap, `d' = rᵢ+rⱼ` exactly. Both-pinned pairs stay residual and are correctly reported. |
| **R2** | `ITER_MAX` 8 → 34 (S-1 green) or → 56 (residual counter green too) | `ITER_MAX` | Arithmetically derived rather than tuned — but §E explicitly names raising `ITER_MAX` to pass S-1 as **drift**, and the value is `Δ`-dependent, so it needs re-deriving whenever a mob's speed changes. |
| **R3** | Accept the FAIL; make S-1 a post-C gate beside S-2 | none | C's wall-repulsion stops the player being the pinned body, removing the failing configuration rather than fixing the solver. Leaves the solver wrong in a corner no policy visits. |

**My read, offered as a read:** **R1.** It is the mechanism §B-2 already states in prose, it is one
measurement and one addition inside the existing loop, it needs no constant re-derived per scenario,
and it makes `ITER_MAX = 8` *correct* rather than incidental. But it touches a FROZEN row, so it is
not mine to take.

**Nothing has been tuned, widened or worked around.** `ITER_MAX = 8`, `ε_touch = 0.001`, the split
law, the solver order and the predicate all sit at their spec values, and the failure is pinned by a
unit test (`test_wall_pinned_SMALL_body_does_NOT_reach_the_predicate_in_eight_sweeps`) so whichever
resolution lands is forced to *change* that test rather than quietly satisfy it.

---

## 1 — What was built

`spatial_engine.py`, all of it behind `body_separation_v2: bool = False` (R-WR2-14):

| piece | what |
|---|---|
| `_apply_soft_collision(entities, arena, *, body_separation_v2=False)` | **body replaced**; dispatches. Flag OFF = the legacy 80 %-of-contact spring + boss hard body, verbatim. Returns `(residual_delta, max_residual_m)`. |
| `_apply_body_separation_v2` | the §B-2 projected Gauss-Seidel solver — index-ordered over `all_entities`, dead skipped **in place**, clamp INSIDE the sweep, `break` on a clean sweep, `ITER_MAX = 8`, `ε_touch = 0.001`, arena clamp outermost and unconditional |
| `_body_separation_split` | R-WR2-7 area-weighted `wᵢ = rⱼ²/(rᵢ²+rⱼ²)`, one law everywhere (R-WR2-12), zero-denominator guard |
| `_body_separation_normal` | §B-5 degenerate handling — `normalize(spawnᵢ−spawnⱼ)` then `(1,0)` with the lower index taking `+`. **Today's `d > 0.0001` skip does not survive into v2** (and is pinned as *surviving on the legacy path*, so flag-OFF is provably unchanged rather than accidentally repaired) |
| `_select_skill_for_entity(..., body_separation_v2=False)` | **SS-B-1** — `effective_range = range_m + target.entity_radius` |
| engine + `run_spatial_fight` | the flag, plus per-fight `_collision_residual_ticks` / `_max_m` and their batch aggregates |
| boss hard-body block | **deleted from the v2 path** (its dead-boss asymmetry with it). Retained verbatim on the legacy path — deleting it there would break flag-OFF byte-identity, which spec §B-7 makes non-negotiable. |

**Radius source is `entity_radius` only.** `ENTITY_RADIUS_BOSS` / `_STANDARD` are never consulted by
the solver; a test asserts a 0.9 m elite separates at 0.9, not at a global.

**One call site, unmoved.** The flag selects the law *inside* the function.

`kitcal_g5_harness.py`: `--body-separation-v2` → `drive` → `_drive_armed` → `run_one_fight` →
`run_spatial_fight`, `_bsep` label suffix, banner, three `wave_regime` keys, two per-fight fields.
**The INS-1 probe IS armed** — unlike Cell A's deliberate non-threading of `--trace-decisions`.
Mechanism B is mechanical, so an unarmed probe against an armed canonical would make INS-1 measure
the collision law instead of the leech door.

---

## 2 — SS-B-1: surface-to-surface range applies to BOTH actors (interpretation, veto-open)

R-WR2-8 names the site (`:2336` vicinity) and the formula, without an actor qualifier. `:2336` is
the **shared** selector — player action phase and mob action phase both route through it — so
applying the change *at the site* governs both. I am flagging this rather than smuggling it:

* **The units bug is symmetric.** Under B the boss's centre is held at `d ≥ 2.0` from the player's
  by the same solver. A boss melee with `range_m = 2.0` falls out of range on the same
  floating-point margin, silently zeroing **boss** DPS and failing S-3 from the other direction by
  making the player unkillable — the mirror of the failure R-WR2-8 exists to prevent.
* **R-WR2-12 already ruled this class of question:** one law everywhere. An actor-conditional range
  law would need a special case *added* to create a second physics.
* The D2/GD/PoE convention is not player-specific either.

Measured on the smoke pair (seed 74000700, boss tier): the player's boss-fight length moves 37.3 s →
47.7 s (arm A) and 63.5 s → 65.3 s (arm B), with kills unchanged — the player is now reaching a body
it previously could not, and the boss is reaching back. **Outcomes move. That is expected and it is
S-6/S-3 material, not Cell B's to grade.**

A pre-existing quirk found while testing and pinned rather than silently inherited:
`range_m = float(skill.get("range_m") or 2.0)` makes a declared `0.0` **falsy**, so it coerces to
2.0 and the `if range_m == 0.0: return True` self-cast branch is unreachable through a dict value of
0.0. Same class as the documented `or 2.0` capstone-cd coercion (SESSION-31). SS-B-1 adds the radius
on top of the *coerced* value and changes nothing else about it.

---

## 3 — D-3 sweep: 66 membership tests audited, 2 entity hits, both converted

**Method: AST walk, not grep.** Every `ast.Compare` with an `In`/`NotIn` operator across the whole
`spatial_gauntlet/` package. A text grep cannot separate `x in y` from `for x in y` and produced
60+ false positives on the first attempt (Discipline #4 — right tool for the question).

**66 compares. Exactly two have a `SpatialEntity` on the left and a container of them on the right:**

| # | site | expression | disposition |
|---|---|---|---|
| 1 | `spatial_engine.py` legacy boss hard-body block | `e not in bosses` | → `not any(e is _b for _b in bosses)` |
| 2 | `spatial_gauntlet/policy/seam.py` `choose_target` | `boss_focus in alive_mobs` | → `any(_m is boss_focus for _m in alive_mobs)` |

The other 64 are string / tuple / constant-set membership (`entity_id in self._deaths_this_tick`,
`scenario_id in MOB_HP_DIFFICULTY_SCENARIOS`, …) and carry no entity-equality hazard.
**Post-conversion re-sweep: 64 compares, zero entity-container RHS.**

### ⚠ Spec correction — §D-3(3)'s NaN mechanism does not reproduce

Spec §D-3(3) predicts `e not in bosses` becomes `True` for a boss against **its own entry** once any
float field goes NaN. I ran the prediction rather than assuming it (Discipline #11). **It does not
fire:**

```
e = E(nan, "x")              e == e  -> True      e in [e]  -> True
d1, d2 = E(nan,"x"), E(nan,"x")   d1 == d2 -> False   d1 in [d2] -> False
d3, d4 = E(1.0,"x"), E(1.0,"x")   d3 == d4 -> True    d3 in [d4] -> True   (d3 is not d4)
```

`list.__contains__` routes through `PyObject_RichCompareBool`, which short-circuits on **identity**
before calling `__eq__`; the dataclass `__eq__`'s tuple comparison short-circuits per element the
same way. An entity is always found in a list that physically contains it, NaN or not.

**The live hazard is §D-3(1), not (3):** `in` is *value* equality, so a **distinct** entity with
matching fields tests `True`. The only thing preventing that here is `entity_id` uniqueness — an
invariant enforced nowhere and stated nowhere, resting on a CPython implementation detail for the
rest. Thin enough to be worth removing, which is what the conversion does.

**Consequence, and it is a strengthening:** SS-B-2 is byte-identical **unconditionally**, not merely
"absent NaN". It is a hygiene repair — it removes an O(n·fields) test masquerading as an identity
test — named as a semantic shift because the predicate's *meaning* changes even where its answer
does not. It lands **unflagged**; flagging a hygiene repair would preserve the value-equality form
on the default path.

---

## 4 — Flag-OFF full regression: **name-diff EMPTY both directions — on the SECOND run**

Baseline: `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`,
81 names, pinned at `9bfbdda`+ per jack-ryan Gate-2 INFO-1.

```
python3 -m pytest tests/ -q -p no:randomly --tb=no -rfE
60 failed, 6082 passed, 3 warnings, 21 errors in 1205.72s (0:20:05)   EXIT=1

baseline names: 81   mine: 81
removed (in baseline, not mine): 0
added (mine, not baseline): 0
```

**`removed=0  added=0`.** Run to completion in the foreground, not "adjacent suites" — and the
WR1 §8.19 lesson **earned its keep here**, because the adjacent suites were green while the
regression was not.

### ⚑ The first run FAILED with 4 added names, and that is the part worth keeping

```
64 failed, 6077 passed, 21 errors in 1204.85s      removed=0  added=4
   + test_bq3_calibration_override_door.py::TestByteIdentity::test_T1_production_path_matches_pre_registered_digest
   + test_bq3_calibration_override_door.py::TestByteIdentity::test_T9_opening_the_door_without_overrides_changes_nothing
   + test_od_leech_carryback.py::TestByteIdentity::test_OD1_door_closed_matches_the_pre_registered_digest
   + test_od_leech_carryback.py::TestByteIdentity::test_OD1b_door_open_with_no_block_is_still_the_same_digest
```

**Cause: mine, and it was a SHAPE leak, not a behaviour leak.** Both files digest
`{k: v for k, v in raw.items() if k not in _DIGEST_EXCLUDE_AGG}` — the whole `run_spatial_fight`
return dict — against a constant pre-registered before either feature existed. I had emitted the
three §B-6 keys **unconditionally**, following Cell A's `wave_regime` precedent. Three additive
keys, four broken digests.

**Every combat pin in those same tests still passed** (`len(fight_results)`,
`mean_mobs_killed == 28.333…`, `total_aoe_hits == 3119`, and the per-row digest over
`SpatialFightResult`, which I never touched). So the fight was never perturbed — only the shape of
the dict that reports it.

**The obvious fix was refused by the tree, and the tree was right.** Adding the keys to
`_DIGEST_EXCLUDE_AGG` is blocked by
`test_OD1c_the_digest_exclusion_set_can_hide_nothing_but_calibration_fields`, which asserts that
set holds nothing but `fight_id` / `created_at`, the three structural payload containers, and
`calibration_*` — with the reason stated in the test: *"a COMBAT field must never be excluded —
that would turn the digest from a proof into a formality."* I am not widening that guard to
accommodate my own key.

**Fix: emit the three keys only when armed.** Flag OFF → the keys are absent → the digest surface
is unchanged → byte-identical. And it is the **better** P-2 shape, not a compromise: *absent* means
"the solver did not run", *present* means "it ran", which is sharper than an unconditional `0` that
cannot distinguish the two. The harness report keeps declaring all three unconditionally in
`wave_regime`, because that block exists to be an arm declaration.

**Proven inert to the sim, not asserted:** the whole 450-fight armed battery was re-fired after the
fix and every trace is **byte-identical to the pre-fix battery, 450/450**, with S-1 and the residual
census reproducing to the digit (`129/450`, `−0.25216185346109277`, `95,852` / `0.28017983717899186`).
Pinned forward by `test_flag_off_does_not_perturb_the_run_spatial_fight_RETURN_SHAPE`, which asserts
the *surface* rather than duplicating a digest constant.

The two unflagged SS-B-2 conversions are inside this result — the regression is what turns
"byte-identical in principle" into "byte-identical in fact."

Adjacent-suite gate fired first as the cheap smoke (Discipline #2): `test_wr2_b_body_separation` +
`test_kitcal_g5_harness` + `test_aware_fighter_policy_seam` + `test_spatial_gauntlet_scenarios` +
`test_wr1_battery_arms` + `test_wr1_battery2_a_dmg1_grain` + `test_wr1_m12_gd_mitigation_nova` +
`test_wr1_m12b_m3_realized_count_telegraph_response` = **244 passed**.

**Armed-vs-unarmed harness smoke** (seed 74000700, 5 fights, `--gd-cadence --with-nova
--emit-telegraphs --mitigation-regime R2_proxy`): unarmed report carries
`body_separation_v2_wr2_b: false, collision_residual_ticks: 0, collision_residual_max_m: 0.0`;
armed carries `true / 1105 / 0.28018`. Both static-pin sets and both INS-1 probes PASS in each arm.

---

## 5 — S-4 determinism: **450 / 450 byte-identical, twice, all three legs**

Each leg fired **twice** into two scratch roots **by one process from one tree**, traces compared
**byte-for-byte, un-normalized** (a determinism check that normalizes is weaker than the one S-4
asks for). Reports excluded — they embed absolute scratch paths, which differ by construction and
are not a determinism fact.

| leg | regime | traces | matched | differed |
|---|---|---|---|---|
| pre | `R2_proxy` | 150 | 150 | 0 |
| post | `R3` | 150 | 150 | 0 |
| pre_endpoint | `R2_proxy_resists_low` | 150 | 150 | 0 |

Cell A's lesson inherited: a determinism check that straddles a tree change measures the tree, not
the RNG — hence both replicates from one process, one tree state. This closes jack-ryan's INFO-2
(S-4 as a *battery* predicate) for the armed arm; Cell BAT still owns the graded battery of record.

Scratch roots removed after comparison; the result lives in the statistics artifact.

---

## 6 — Shuffled-order test (spec §D-2)

`test_shuffled_order_differs_the_invariant_is_real` runs the solver on the same four-body pile in
index order and on a shuffled copy and asserts the results **differ**. They do.

A test asserting they *matched* would be asserting Jacobi, which is not what was built. The point is
not that order-dependence is desirable — it is that **the ordering invariant is load-bearing**, so
"never sort / never filter-and-reindex / never iterate a set of entities" is a requirement rather
than a comment. The same test also asserts that **both** orderings satisfy the separation predicate
on free-space pairs: order changes *where* bodies land, never *whether* they separate.

Companions: `test_solver_never_reorders_the_caller_list`,
`test_dead_entities_are_skipped_in_place_not_removed`,
`test_spatial_entity_is_unhashable_so_index_membership_is_mandatory`.

**The named bias is in the math note (§6.2), not discovered later:** the player is index 0 and
resolves against every mob before any mob↔mob pair, so in a pack it accumulates more correction per
sweep than any single mob. Deterministic, arguably correct, now on the record.

---

## 7 — Test evidence

`tests/test_wr2_b_body_separation.py` — **40 tests, all pass**, one per frozen property:

predicate (4) · split law (5) · dead-exempt (3) · coincident fallback (4, incl. *the legacy skip
still skips*) · clamp-outermost (3, incl. both pin directions) · residual tripwire (4) ·
determinism/ordering (5) · flag default-OFF byte-identity (4, incl. the return-SHAPE pin §4) ·
SS-B-1 range (6, incl. mob-side and the `or 2.0` coercion) · the HALT itself (1).

Two of these exist specifically to make claims falsifiable rather than assertable:

* `test_default_call_reproduces_the_legacy_one_sided_1600_flat` reproduces spec §0.1's mechanism —
  a wall-pinned player has its half annulled by the clamp, so only the boss moves and separation
  lands **exactly** on `0.8 × 2.0 = 1.600`, in one call, on the DEFAULT path.
* `test_default_call_reproduces_the_legacy_two_sided_overshoot` pins a legacy quirk found while
  testing: `SEPARATION_FORCE_CONSTANT × 0.5 == 1.0`, so each body moves the **full** overlap and an
  unpinned legacy pair *overshoots* the 1.600 threshold to `d + 2·overlap`. Reported, not repaired —
  the legacy path is frozen by the byte-identity requirement.

---

## 8 — Artifacts

| path | size | committed |
|---|---|---|
| `output/kitcal_g5/wr2_cell_b_s1/` (450 traces + 3 leg reports) | **141 MB** | **no** — per the cell brief; the graded battery of record comes at Cell BAT. Regenerable in **10.4 s** of wall time from one command. |
| `wr2_cell_b_s1/wr2_cell_b_statistics.json` | small | **yes** — S-1 per-leg/per-trace statistics + residual census |
| `wr2_cell_b_s1/wr2_cell_b_s4.json` | small | **yes** — S-4, all three legs |
| `wr2_cell_b_determinism{,_b}/` | — | removed after comparison |

Driver: `~/Games/reincarnated-engine/src/reincarnated/simulation/wr2_cell_b_sep_2026_07_29.py`
(`--battery` / `--s1` / `--s4` / `--scan-dir`). It reuses `wr1_battery2_2026_07_29.LEGS` **by import,
not by transcription**, so R-WR2-5 is a property of the code path rather than a promise in a comment.
Legs fire SEQUENTIALLY (Discipline #3).

**S-1 is measured from the emitted frames, never from the solver's own counters** — an instrument
that grades itself is not a gate. Soundness (math note §8): the frame is emitted at loop bottom and
nothing mutates a position between the collision phase and that emission (verified: zero
`.x =` / `.y =` / `clamp_entity` sites in the intervening range); deaths occur after the collision
phase, so every entity marked alive at frame time was alive at solve time and the measured pair set
is a **subset** of what the solver resolved. Radii come from the header's per-entity
`entity_radius_m`, so even the measurement never consults a global.

---

## 9 — For the conductor

* **⚑ ONE RULING NEEDED: the S-1 HALT.** R1 / R2 / R3 above, costed. It touches a spec-FROZEN row,
  so it is yours. Everything needed to rule is in §HALT — I do not need a dialogue, just the ruling.
* **⚑ ONE VETO WINDOW: SS-B-1 applies to mobs as well as the player** (§2). Reverting to
  player-only is a one-line special case; my reasoning for both-actors is stated.
* **⚑ ONE SPEC CORRECTION: §D-3(3)'s NaN mechanism does not reproduce** (§3). The sweep obligation
  is discharged as written; its *justification* is (1), not (3).
* **INFO for Cell C's baseline:** three unconditional `wave_regime` keys and two unconditional
  per-fight fields landed, so — exactly as with Cell A's `trace_decisions_wr2_a` (INFO-1) — **Cell
  C's flag-OFF byte-identity BEFORE-snapshot must pin at Cell B's landing commit**, not at
  `9bfbdda`. Behaviour and trace content unaffected; report artifact only. MIGRATION §1 says so too.
* **INFO for Cell C:** WARN-1 (`spatial_engine.py:4258`, the second ungated `frame_sink.decision`)
  is untouched here and remains Cell C's obligation.
* **R-WR2-11 honoured:** S-2 is not computed, not claimed, and not implied. B alone provably worsens
  the corner pin, and §HALT is the quantitative form of that same fact — the corner is where the
  solver fails, and it is C that removes the player from the corner.
* **Not pushed.** The engine commit is local; the conductor pushes.

---

*gamora, 2026-07-29. The cell computes; the conductor grades. Math before code; the HALT is arithmetic, not opinion.*

---
---

# ⚑ B-FIX — R-WR2-16 implemented, S-1 re-gated

**Run:** WR2-ENCGEO-2026-07-29 · **Cell:** B-FIX · **Seam:** gamora · **Date:** 2026-07-29
**Ruling implemented:** **R-WR2-16** (charter §8.9) — resolution **R1, clamp-aware shortfall
transfer**. R2 (`ITER_MAX` raising) REFUSED as drift; R3 (defer S-1 post-C) REFUSED as goalpost
motion. **R-WR2-17** ratified the all-attacker surface-to-surface build — nothing changed for it.
**Baseline:** engine `6dca36a` · **Math note:** `simulation/math/wr2-b-body-separation-2026-07-29.md`
**§12** (new) · **Status:** COMPLETE. **The HALT is cleared. No new HALT.**

## Verdict table

| # | Gate-2 deliverable | verdict |
|---|---|---|
| 1 | **S-1** — min pairwise LIVING separation ≥ rᵢ+rⱼ − 1 cm, every tick, 450 fights | **PASS — 450/450 traces; worst slack −0.000998 m** (was 129/450, −0.25216) |
| 2 | `collision_residual_ticks` / `_max_m` | **7 and 0.0012118** (was 95,852 and 0.28018) — §B-4 below locates all 7 and shows they are §B-6's deliberate over-report, not over-constraint |
| 3 | **S-4** — battery byte-reproducible at fixed seed, twice | **PASS — 450/450, all three legs, 0 differing** |
| 4 | **Flag-OFF full regression** — name-diff vs the 81-name baseline | **see §B-5** |
| 5 | **Flag-OFF path byte-identical vs `6dca36a`** | **PASS — 150/150 traces identical; the ONLY differing bytes in the whole battery are the header's `engine_git_hash`, which differs by construction** |
| 6 | Unit tests — wall-pinned exact in ≤2 sweeps; both-clamped residual COUNTED; shuffled-order still passes | **DONE — 42 tests, all pass** (was 40) |
| 7 | Math note updated — transfer law, one-sweep proof, corner residual | **DONE — §12, five subsections** |
| 8 | **SS-1** — `wr1_battery_2/` and `wr1_battery_2_aim/` untouched | **PASS — porcelain empty, 908 files, zero mtimes after session start** |

---

## B-1 — What changed, in one paragraph

Inside `_apply_body_separation_v2`'s pair resolution only. After the intended split move and the
clamp, each body's **realized post-clamp displacement along the separation normal** is measured; the
**annulled magnitude** (`intended share − realized`, clamped into `[0, share]`) **transfers to the
pair partner in the same pass**, and the partner re-clamps. Both shortfalls are measured *before*
either transfer is written, so the two transfers touch disjoint bodies from a common state and the
pair outcome does not depend on write order — the transfer adds **no new ordering dependency** on
top of the existing index-order invariant. Zero RNG, index tuples only, in-place float adds only.

**Nothing else moved.** `ITER_MAX = 8`, `ε_touch = 0.001`, the split law, dead-exempt,
clamp-outermost, the S-1 predicate, the §B-6 counter semantics, the two flags' `False` defaults —
all at their spec values. The `git diff 6dca36a` on `spatial_engine.py` is **two hunks, both inside
`_apply_body_separation_v2`**; the legacy branch is not touched by a single character.

## B-2 — Why one pass is exact (math note §12.3), and why that kills R2 rather than merely beating it

With `Δᵢ`, `Δⱼ` the total per-pass displacements and `j` unconstrained:

```
Δᵢ·n̂ = g·wᵢ − σᵢ          −Δⱼ·n̂ = g·wⱼ + σᵢ
normal component of the new separation = d + (g·wᵢ − σᵢ) + (g·wⱼ + σᵢ) = d + g = rᵢ + rⱼ   (exact)
```

**`σᵢ` cancels identically.** The split always decided who moves, never how much in total (§2's sum
check); the clamp was eating the total, and the transfer puts it back. Corner pin: pinned player
realizes 0, `σᵢ = 0.90g`, free boss absorbs `0.10g + 0.90g = g`. One pass, zero perpendicular error.

Consequently §10.2's per-tick recurrence `g_{k+1} = (g_k + Δ)·q` has `q = 0`, so `g* = 0` **and the
mob speed `Δ` disappears from the expression**. That is the decisive argument against R2 and it is
worth stating as arithmetic rather than as preference: under R2 the required `ITER_MAX` (34 for
S-1's 1 cm, 56 for `ε_touch`) is **a function of mob movement speed**, so the gate would need
re-deriving every time a scenario re-tunes a mob. Under R1 it is a function of geometry alone.
`ITER_MAX = 8` is now *correct* rather than *incidental*.

**Sweep accounting.** The `break` reads a **pre-correction** measurement (§4, frozen), so any tick
with real overlap costs **two** sweeps — sweep 0 corrects, sweep 1 finds `gap ≤ ε` and breaks — and
a clean tick still costs one. `2 ≤ 8` with a factor-of-four margin, which is the margin §3.1 spends
on multi-body chains.

## B-3 — S-1: 450/450, and the worst slack is the frozen ε, not a wall

| | `6dca36a` | **B-FIX** |
|---|---|---|
| traces passing S-1 | 129 / 450 | **450 / 450** |
| worst slack | −0.25216185 m | **−0.00099845 m** |
| violating pair-samples | 81,861 / 340,828 (24.0 %) | **0 / 323,780** |
| violating ticks | 81,756 / 133,848 | **0 / 134,460** |

Worst slack is **−0.000998 m — inside `ε_touch = 0.001`**, i.e. inside the solver's own target and
an **order of magnitude inside S-1's 1 cm**, exactly the margin math note §1 promised. It is
identical to 17 s.f. across all three legs and it occurs on the pair
`gd-werewolf-kitcal-1` ↔ `hero_boar_h07_0` (contact 1.0 m, `mixed_pack__none__seed74000806`
tick 80). It is the `gap ≤ ε_touch → continue` skip threshold showing up as its own value, which
is what a correctly-converged solver's worst case should look like.

> **⚠ ERRATUM (WR2 Cell C, 2026-07-29; charter §8.13 WARN-1, jack-ryan's Gate-2, ADR-002
> documentation-only).** This paragraph previously called that pair "**mob↔mob** … **not a wall
> pair at all**". Both halves are wrong. `gd-werewolf-kitcal-1` is the **PLAYER** — the trace
> header records `"is_player": true, "entity_radius_m": 0.5` — so the pair is **player↔mob**; and
> at that tick both bodies sit at `y = 0.5`, which is exactly the south-wall clamp for a 0.5 m
> radius on the 36×36 arena, so **both are wall-clamped**.
>
> The conclusion is unaffected and the correct statement is narrower: **the pair's separation
> NORMAL is unaffected by the clamp** (the normal is x-aligned, the binding clamp is on y, so
> nothing is annulled along the correction axis). Restated in that form rather than as "no wall is
> involved" — which is broader than the measurement supports, and is the sentence a grader reads.

S-1 is measured **from the emitted frames, never from the solver's counters** (math note §8) — an
instrument that grades itself is not a gate. Method unchanged from the HALT run.

## B-4 — The 7 residual ticks: located, diagnosed, and NOT the corner case

`collision_residual_ticks` went **95,852 → 7**; `_max_m` **0.28018 → 0.0012118**.

| tier | fights with residual, `6dca36a` | fights with residual, **B-FIX** | max_m |
|---|---|---|---|
| boss | 180 / 180 | **0 / 180** | **0.0** |
| trash | 90 / 90 | **0 / 90** | **0.0** |
| mixed_pack | 90 / 90 | **7 / 90** | 0.0012118 |
| champion | 0 / 90 | 0 / 90 | 0.0 |

**No wall-pinned pair anywhere in the battery is residual any more** — which is precisely the claim
§12.3 makes, and `boss` going 180/180 → 0 is the corner pin being solved rather than argued about.

All 7 are `mixed_pack`, seeds **74000801 / 74000816 / 74000824** (three fights in each of the two
R2-family legs, one in the R3 leg). **Registered prediction was 0, so the miss is reported, not
absorbed.** They are a *different* mechanism, and it is the one §4 pre-registered: `max_residual` is
a **pre-correction** measurement of the last executed sweep, so a tick counts non-convergent iff
sweep 8 *observed and corrected* a gap above `ε_touch` — even when a 9th sweep would have broken
clean. Verified rather than asserted (Discipline #11) — worst **post-solver** overlap on the three
flagged fights:

| seed | worst post-solver slack | pair | vs `ε_touch` |
|---|---|---|---|
| 74000801 | −0.00094849 m | `hero_boar_h07_0` ↔ `slitha_melee_b01_2` | inside |
| 74000816 | −0.00071342 m | same pair | inside |
| 74000824 | −0.00094849 m | same pair | inside |

All inside 1 mm; every flagged PAIR is mob↔mob in a **pack chain**. `mixed_pack` is the only tier
whose contact graph is a genuine chain rather than a union of pairs, so it is the only tier where
§3.1's per-sweep *constraint propagation* — not §12.3's per-pair exactness — is the binding cost.

> **⚠ ERRATUM (WR2 Cell C, 2026-07-29; charter §8.13 WARN-1/WARN-2, ADR-002 documentation-only).**
> (1) This block previously added "no wall involved". The flagged PAIRS are mob↔mob, but the
> residual CHAIN terminates on a **corner-pinned player** at `(35.5, 0.5)` with the boar
> south-wall pinned at `(34.5, 0.5)` and blocked in `+x` by it (jack-ryan's tick-93
> reconstruction of seed 74000801). Chain, not pair, is the level at which the wall participates.
> (2) `ITER_MAX = 8`'s margin on the observed worst case is **1×, not the factor-of-four** the
> math note claimed: the counter can only increment when all 8 sweeps ran AND the 8th still saw
> `gap > ε_touch`, so each residual tick spent the entire frozen budget. The frozen row stays
> frozen (R-WR2-16 refused raising it); the counters are the instrument, and Cell C and Cell BAT
> carry them as a WATCHED quantity.

**Reported, not repaired.** Raising `ITER_MAX` to silence it is the same drift R2 was refused for;
re-defining the counter as a post-state measurement would turn a tripwire that errs toward *firing*
into one that errs toward *silence*, which §4 rules is the wrong direction. The disposition is the
one §4 pre-registered: **counter non-zero + S-1 green = the tripwire fired on sweep 8 and the ninth
would have been clean** — now with a measurement behind it instead of a hypothesis.

## B-5 — Flag-OFF full regression: **name-diff EMPTY both directions — on the THIRD run**

```
python3 -m pytest tests/ -q -p no:randomly --tb=no -rfE
60 failed, 6084 passed, 3 warnings, 21 errors in 1201.47s (0:20:01)

baseline names: 81   mine: 81
removed (in baseline, not mine): 0
added (mine, not baseline): 0
```

**`removed=0  added=0`.** `60 failed / 21 errors` reproduces the baseline exactly; `6084 passed` is
the baseline's `6082` plus the **two tests B-FIX adds** — the arithmetic the name-diff cannot show
and the count can.

### ⚑ Runs 1 and 2 each came back with added names, and BOTH were my process, not my code

Recorded because Cell C will be standing in the same room. Neither cause was the solver; both were
**me perturbing the measurement while it ran**. Each was diagnosed to a mechanism before being
dismissed — an added name is never waved away here.

**Run 1 — `added=3`. Cause: I edited `spatial_engine.py` MID-RUN.** The three names were

```
+ test_od_leech_carryback.py::TestTwoPathReachability::test_TW5_the_projection_factory_is_reachable...
+ test_wr1_m12b_m3_realized_count_telegraph_response.py::test_T_M3_8_an_EVADE_tick_resolves_NO_attack
+ test_wr2_b_body_separation.py::test_flag_off_does_not_perturb_the_run_spatial_fight_RETURN_SHAPE
```

**All three call `inspect.getsource` on objects in `spatial_engine.py`.** I had appended four comment
lines at ~line 2420 while the suite ran; the module was already imported, so every `co_firstlineno`
downstream of the edit still pointed at pre-edit line numbers while `linecache` served the post-edit
file — misaligned source slices, failing string assertions on source text.
**The confirmation is the test that did NOT fail:** the same file's other source-inspecting test
targets `_mint_telegraph_spec` at **line 1666, UPSTREAM of the edit**, and it passed. Downstream
fails, upstream passes. That is a mechanism, not a coincidence.
*Lesson, stated as law: a full regression is a MEASUREMENT; the tree is frozen for its duration.*

**Run 2 — `added=1`. Cause: I ran a SECOND pytest suite concurrently, and the two shared a package.**
The name was
`test_kitcal_g5_harness.py::test_G5_W1_untracked_loaded_source_is_invisible_until_it_is_imported`,
and the failure was inside its own **teardown**:

```
os.remove(os.path.join(cached, f))
E FileNotFoundError: .../spatial_gauntlet/__pycache__/_wr1_warn1_probe_module.cpython-312.pyc
```

That test plants a probe module in the package directory and deletes it afterwards. I had a
`git worktree` at `6dca36a` running the full suite at the same time — and **`reincarnated` is
installed EDITABLE, pinned to the main tree's `src/`**
(`_editable_impl_reincarnated_engine.pth -> /Users/admin/Games/reincarnated-engine/src`). A bare
`cd <worktree> && pytest` therefore imports the **main tree's** package, so both suites planted and
removed the *same* probe file in the *same* `__pycache__`: a listdir/remove race.
**Discipline #3 in a form the discipline does not spell out — "no parallel regens of the same seed"
generalises to "no parallel suites sharing an editable install."**

**That same fact invalidated the worktree run as a baseline**, and it is worth saying rather than
quietly dropping: it reported `71 failed / 5944 passed / 127 skipped` with 11 extra names, because
it ran *my* engine against the *worktree's* fixtures with the main tree's untracked `output/`
artifacts absent. **It is not evidence of anything and it is cited as none.**

**⚑ §B-7's `6dca36a` comparison is NOT affected — checked, not assumed.** Those runs passed
`PYTHONPATH=src` from inside the worktree, which precedes the `.pth` in `sys.path`. The proof is in
the artifacts: the base battery's trace headers record `engine_git_hash = 6dca36a` (clean) while
HEAD's record `6dca36a-dirty`. Two different trees, as intended.

**Run 3 — fired ALONE, tree frozen, no worktree, nothing else touching the repo.** That is the run
reported above, and it is the one that counts.

## B-6 — S-4 determinism: 450/450, twice, all three legs

Each leg fired **twice** into two scratch roots **by one process from one tree**, traces compared
**byte-for-byte, un-normalized**. Reports excluded (they embed absolute scratch paths).

| leg | regime | traces | matched | differed |
|---|---|---|---|---|
| pre | `R2_proxy` | 150 | 150 | 0 |
| post | `R3` | 150 | 150 | 0 |
| pre_endpoint | `R2_proxy_resists_low` | 150 | 150 | 0 |

`S4_PASS_ALL = true`. The transfer introduces no RNG draw and no ordering dependency, and this is
the measurement of that rather than the assertion of it.

## B-7 — Flag-OFF byte-identity vs `6dca36a`, measured across two trees

Static: the diff is two hunks, both inside `_apply_body_separation_v2`, which is unreachable at
`body_separation_v2=False`. **Dynamic, because static is not evidence:** a `git worktree` was cut at
`6dca36a` and the **flag-OFF** 30-seed leg (`R2_proxy`, 150 traces) fired from *both* trees.

```
traces: 150 / 150, same names
identical modulo header provenance : 150 / 150
header fields that differed        : ['engine_git_hash']      <- differs BY CONSTRUCTION
report identical modulo provenance : True
```

The only differing bytes in the entire 150-trace battery are the header's `engine_git_hash`. That is
the honest form of the claim — a raw byte compare across two commits *cannot* match on a field that
records the commit.

## B-8 — Unit tests: 42, all pass

| test | what it pins |
|---|---|
| `test_wall_pinned_SMALL_body_NOW_reaches_the_predicate_R_WR2_16` | **rewritten, not deleted.** Same geometry as the HALT test. Runs with `ITER_MAX` monkeypatched to **2** and asserts exact contact (`d == 2.0` to 1e-12, boss at 2.5) with the player still pinned at 0.5 and counters `(0, 0.0)` — so "≤2 sweeps" is *mechanical*, not a docstring claim. Also asserts the superseded `gap·0.9⁸` value is **no longer produced**, so the old law's arithmetic survives in the test rather than only in git. |
| `test_both_bodies_clamped_leaves_a_residual_that_is_COUNTED_not_silent` | **new.** A 1.6 m corridor pins both 0.5 m bodies against **opposing** walls; every share and every transfer is annulled; neither body moves; the predicate is violated; `resid == 1` and `resid_m == 0.4` **fire**. The corner case is COUNTED, and the boundary still wins (R-WR2-3). |
| `test_shortfall_transfer_never_exceeds_the_gap_partial_clamp_slides_the_wall` | **new.** Partial clamp (body sliding a flat wall): one axis annulled, the other realized. Asserts the pair lands **at or beyond** contact and that the over-resolution is bounded by the perpendicular slide the wall forced — i.e. the `[0, share]` bound holds. |
| `test_wall_pinned_LARGE_body_yields_the_predicate_in_one_tick` | unchanged, still passes — the favourable direction did not regress. |
| `test_shuffled_order_differs_the_invariant_is_real` | **unchanged, still passes.** The ordering invariant is still load-bearing; the transfer did not accidentally make the solver order-independent. |
| `test_over_constrained_tick_reports_loud_rather_than_silently_violating` | unchanged, still fires — the tripwire is proven live, not merely unfired. |
| `test_free_space_pair_is_exact_in_one_sweep_...` | unchanged — free-space exactness to 1e-12 at every radius ratio. |
| `test_iter_max_and_eps_are_the_frozen_values` | unchanged — `8` / `0.001` / `1e-6`. **The frozen row is asserted, not promised.** |

## B-9 — Semantic shift SS-B-3 (Discipline #12), named not buried

**`ITER_MAX` stops meaning "how many decay passes we can afford" and starts meaning "how far a
constraint may propagate through a contact chain."** Before, a clamped body's share was *lost* each
pass, so sweeps were a convergence budget against a geometric decay whose rate depended on the split
and whose fixed point depended on mob speed. After, a clamped body's share is *relocated* within the
pass, so each pair is exact in one pass and sweeps buy only chain propagation — which is what §3.1
always claimed `ITER_MAX = 8` was for.

Stated plainly: **`_apply_body_separation_v2` produces different positions than `6dca36a` on every
tick where a clamp binds.** That is the ruled change of law, not a bug fix smuggled in, and it lands
behind the **same** `body_separation_v2` flag — flag-OFF is untouched (§B-7).

## B-10 — INFO for the conductor: what the ARMED arm's outcomes did

Not graded here (R-WR2-11; S-3/S-6 are not Cell B's), reported because B-FIX moves the armed arm and
the conductor should not discover it at Cell BAT:

| leg | fights differing in ≥1 report field | winners identical | total mobs killed | mean elapsed |
|---|---|---|---|---|
| `R2_proxy` | 120 / 150 | **yes, 150/150** | 690 → **690** | 31.117 → 31.237 s |
| `R2_proxy_resists_low` | 120 / 150 | **yes, 150/150** | 661 → **661** | 28.011 → 28.131 s |
| `R3` | 120 / 150 | **yes, 150/150** | 720 → **720** | 30.105 → 30.273 s |

Positions move on every clamp-binding tick, so 80 % of fights differ somewhere — but **every winner
and every per-leg kill total is unchanged**, and mean fight length moves by **+0.12 to +0.17 s
(+0.4 % to +0.6 %)**. Small, one-directional, and consistent with bodies now being held slightly
further apart.

## B-11 — Artifacts

| path | committed |
|---|---|
| `output/kitcal_g5/wr2_cell_b_s1_r2/` — the B-FIX battery, 450 traces + 3 leg reports, 142 MB | **no** (per the cell brief; regenerable from one command) |
| `wr2_cell_b_s1_r2/wr2_cell_b_statistics.json` — S-1 per-leg/per-trace + residual census | **yes** |
| `wr2_cell_b_s1_r2/wr2_cell_b_s4.json` — S-4, all three legs | **yes** |
| `output/kitcal_g5/wr2_cell_b_s1/` — the **pre-fix HALT battery**, left in place | unchanged; its two committed JSONs remain the HALT's evidence |

**I emitted to a SIBLING `wr2_cell_b_s1_r2/` rather than overwriting `wr2_cell_b_s1/`**, so the
HALT's measurement and its resolution's measurement can be diffed against each other — which is what
§B-10's table is, and it would not exist if I had overwritten. Determinism scratch roots removed
after comparison; the `6dca36a` worktree removed after §B-7's comparison.

## B-12 — For the conductor

* **The HALT is cleared, and no new HALT is raised.** S-1 450/450, S-4 450/450, flag-OFF identical,
  SS-1 intact.
* **One registered prediction missed and is reported as missed:** math note §12.5 predicted
  `collision_residual_ticks = 0`; measured **7**. The over-constrained half of the prediction held
  (zero wall residuals, boss 180/180 → 0); the 7 are §B-6's deliberate pre-correction over-report on
  pack chains, verified against the post-solver frames (§B-4). **Nothing was widened to absorb it.**
* **Cell C's flag-OFF baseline still pins at `6dca36a`** — B-FIX adds no key to any returned dict and
  changes no report surface, so §8.9's ruling on that is unaffected.
* **R-WR2-11 still honoured:** S-2 is not computed, not claimed, not implied. B alone still
  provably worsens the corner *pin* (the 90/10 bulldozer moves the centroid faster); what B-FIX
  repairs is the solver failing **its own predicate**, which is a different thing. The docstring
  now says both, so the two cannot be conflated later.
* **Not pushed.** The engine commit is local; the conductor pushes.
