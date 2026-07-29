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
