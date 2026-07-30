# Finding — 2026-07-29 — Gate-2 on WR2-ENCGEO Cell D (nova cast-gate parity + Mechanism D)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** **CLEAR-with-notes** — 5 WARN, 5 INFO, no BLOCK. **Cell BAT RELEASES on this gate.**
**Target:** engine `28386b26` + `b35695c0` + `796a6f6d` reviewed as ONE landing atop `ecea69f`
**Developer:** gamora
**Governing:** charter §8.21 (Mechanism D + S-7) · §8.22 (diagnostic verdict + the range-semantics
checklist law, **first enforcement**) · §8.23 (R-WR2-20 flag topology + WARN riders) · §8.24
(conductor rulings) · spec §D / §E / §G · R-WR2-19 (MATT-SIGNED)
**Principles applied:** #1 math-before-code · #2 smoke-gate/evidence · #3 cross-seam impact ·
#4 decisions-log/ruling-ledger as truth · #5 severity matters
**Disciplines cited:** #1, #8, #10, #11, #12

---

## 0. Verdict in one paragraph

Every pre-registered obligation this landing owes is **independently reproduced, not accepted**. I
re-enumerated the range-consuming predicates myself and reached gamora's substantive conclusion by a
*stronger* route than the sweep took; I re-derived the escape law and got 2.318840579710145 s with an
exact IEEE-754 round-trip; I wrote my own S-7 grader against my own emitted traces and got **5/5 HOLD,
worst ratio-to-bound 0.14928412301085175** — matching gamora's last printed digit; I re-emitted the
flag-OFF slice from a scratch `ecea69f` tree and got **SHA-256 identity on all 6 traces with `diff -r`
returning zero lines**; I ran the full regression alone and got **60 / 6197 / 21** with the name-diff
**EMPTY both directions, 81/81**; I re-measured the residual counters on all four tiers in both D arms
myself. The onset-tick correction is right, its falsifier is sound, and I verified its *premise* in
source rather than in prose. Nothing in the landing is undeclared: the non-comment diff in
`spatial_engine.py` is exactly eight edits and the cell note names all eight. **No BLOCK.** The five
WARNs are all of one family — statements that are *true where they were measured* and *incomplete or
wrong where they were generalized* — and one of them is a correction to **my own Cell C finding**,
which gamora propagated verbatim and the conductor then ratified into charter §8.24.

---

## 1. Obligation 1 — the range-semantics checklist law, FIRST ENFORCEMENT — **PASS on the class, WARN on the method**

Charter §8.22 (ii): *"a range-semantics change must be verified at EVERY predicate that consumes
range, enumerated by grep, not at the shared entry point."* This law exists because of a gate-escape
at **my** Cell B gate. I therefore ran my own enumeration and did not read gamora's table until after.

**My grep families** (over `spatial_gauntlet/` + `gd_nova.py` + every module reachable from the two
attack phases): `distance_to` / `distance_to_point` / `_dist_point_to_segment` / `math.hypot` /
`math.sqrt`, then `(<=|>=|<|>)` intersected with `radius|range|reach|dist|leash|proximity|band_`,
then — the check that actually settles it — **every consumer of `entity_radius` / `target_radius` in
the entire `simulation/` tree.**

### 1.1 The decisive check, and it is stronger than a table of 19 rows

A radius-semantics law can only be violated at a site that *consumes a target radius*. There are
exactly **three** such sites in the whole tree, and all three are surface-aware under the flag:

| site | predicate | flag-aware? |
|---|---|---|
| `spatial_engine.py:2645` shared selector | `nearest_dist <= range_m + nearest_target.entity_radius` | ✅ under `body_separation_v2` (SS-B-1) |
| `spatial_engine.py:4530` nova cast gate | `p.fire_range_m + (target.entity_radius if self._body_separation_v2 else 0.0)` | ✅ **this cell's fix** |
| `policy/reposition.py:107` band reach | `min_attack_range + target_radius if surface_to_surface` | ✅ under `body_separation_v2` (Cell C) |

Every other range comparison in the tree is radius-blind by construction, so **no fourth site can be
"still centre-to-centre under the flag" — there is no fourth site that could be.** gamora's claim
*"the nova's private reach gate was the only per-skill REACH predicate downstream of the shared
selector; the class is closed, not just the instance"* is **CONFIRMED**, and confirmed by a route that
does not depend on the classification argument being right.

I also independently reproduced the negative finding. In the mob/boss attack phase the branch at
`spatial_engine.py:6003` is `if skill.get(_GD_NOVA_KEY) is not None:` → `elif geo in ("self","none")`
→ `else _compute_aoe_hits`. The nova gate was the only distance comparison in that chain. In the
player attack phase there is no distance comparison between `_select_skill_for_entity` and
`_compute_aoe_hits`. Both re-read end to end.

### 1.2 The method gap → WARN-1

gamora's 18 of 19 line citations resolve **correctly against `ecea69f`** (I checked them one by one),
so the table is honest about what it points at. But it is **not grep-complete**, and the law's own
words are "enumerated by grep." Sites carrying a distance/radius comparison that the table does not
list:

| site | predicate | class (mine) |
|---|---|---|
| `spatial_engine.py:407` `_aura_beneficiaries_in_radius` | `hypot(b − origin) <= r` | FOOTPRINT (aura extent); solo ⇒ beneficiary set is `[player]`, `d = 0` |
| `spatial_engine.py:3686` `aura_effective_benefit` radius gate | `hypot(beneficiary − origin) > float(R)` | FOOTPRINT, same pair |
| `spatial_engine.py:712` `_f8_leash_latch_under_lock` | `sqrt(Δspawn) > entity.leash_distance_m` | AI-STATE — a **SECOND** leash site; the table lists only `:1990` |
| `spatial_engine.py:5463` | `player.distance_to_point(m) <= M1_GATHER_RADIUS_M` | SELECTION/movement (gather centroid) |
| `spatial_engine.py:2028` | `_d < _WAVED_EPS_FLEE_MIN` | degenerate-direction guard |
| `spatial_engine.py:2300` legacy push-apart | `d < ENTITY_RADIUS_BOSS and d > 0.0001` | FOOTPRINT/collision |
| `spatial_engine.py:5721` + `:7856` | `_bs_resid_m > self._collision_residual_max_m` | INSTRUMENT (Cell B's own counter) |
| `commitment_state_machine.py:158` / `:165` / `:170` | `pdist` vs `preferred_range_m` | AI-STATE — a **SECOND COPY** of the kite/standoff predicates the table lists only at engine `:2081/:2104/:2114` |
| `gd_nova.py:292` (pre-landing) | `r <= p.explosion_radius_m` | FOOTPRINT (per-projectile blast) |
| `gd_nova.py:490` (pre-landing) | `hypot(target − spoke) <= blast` | FOOTPRINT (spoke coverage) |

**None is REACH, so the verdict does not move.** The two that matter for the law's future use are the
duplicated pairs: `commitment_state_machine.py` carries a second copy of a predicate family the table
treats as single-sited, and `:712` is a second leash. A range law that ever needs to reach an
AI-STATE or MOVEMENT predicate would have to be applied at **two** sites, and a reader auditing "19
sites" against their own grep gets a different number and cannot tell which of us is wrong.

---

## 2. Obligation 2 — cast-gate parity + flag isolation (R-WR2-20) — **PASS**

Read at source (`spatial_engine.py:4507–4581`):

```python
_eff_fire_range = p.fire_range_m + (
    target.entity_radius if self._body_separation_v2 else 0.0
)
if mob.distance_to(target) > _eff_fire_range:
    return False
...
_tg_wind_up_s = (
    _gd_telegraph_escape_duration_s(target.movement_speed, p)
    if self._nova_telegraph_v2
    else float(p.wind_up_s)
)
```

* The gate conditions on `_body_separation_v2` **only**; the law conditions on `_nova_telegraph_v2`
  **only**. No cross-contamination. `test_item_1_did_NOT_get_its_own_flag_R_WR2_20` pins this by
  *partitioning the function source at `"MECHANISM D"`* and asserting each half sees only its own
  flag — the right shape, because it fails on a future edit rather than on a future value.
* **Both flag states agree with the selector.** Flag OFF: gate `10.0`, selector `range_m` = `10.0`.
  Flag ON: gate `10.0 + 0.5 = 10.5`, selector `10.0 + 0.5 = 10.5`. Same term, same attribute, same
  flag. `test_the_nova_cast_gate_AGREES_WITH_THE_SELECTOR_at_every_distance` drives 13 distances × 2
  flag states, and `test_the_selector_transcription_above_matches_the_LIVE_selector_source` guards
  against the parity pins passing against a stale transcription — the correct generalization of Cell
  B's HALT (Discipline #10).
* **Byte-identity by construction, verified:** flag OFF the added term is literally `0.0` and
  `_tg_wind_up_s` is `float(p.wind_up_s)`. Pre-landing `cast()` read `t_launch=float(t_cast) +
  float(params.wind_up_s)`; post-landing it reads `_wind_up = float(params.wind_up_s)` when the
  override is `None`. Identical expression.
* **Nothing undeclared.** The full non-comment diff of `spatial_engine.py` across the three commits is
  **eight edits** (import, ctor param, ctor assignment, docstring clause, the gate, the duration
  derivation, the `cast()` kwarg, the `TelegraphSpec` field) plus two `run_spatial_fight` threads and
  one conditional result key. Every one appears in cell note §2. **Discipline #12 satisfied.**

---

## 3. Obligation 3 — escape-law arithmetic + determinism — **PASS**

Reproduced from scratch:

```
FRAC·v      = 0.90 × 5.75 = 5.175
T           = 12.0 / 5.175 = 2.318840579710145      (== gamora's value, exact)
R / T       = 5.175 EXACTLY in IEEE-754 double      → no tolerance needed even at d = 0
T / 0.750   = 3.0917874396135265                    (the 3.09× claim, exact)
ticks       = 23.18840579710145
v_req(0)    = 5.175   ratio 1.0        (exact, no epsilon)
v_req(2.0)  = 4.3125  ratio 0.8333333333333334      (B's floor — worst REACHABLE, ≥16.67 % margin)
```

* **`NOVA_ESCAPE_FRAC = 0.90`, untuned.** `gd_nova.py:276`. The harness reads it **from the module**
  (`from reincarnated.simulation.gd_nova import NOVA_ESCAPE_FRAC as _NOVA_ESCAPE_FRAC`) and
  `test_the_report_declares_the_arm_AND_the_dial_read_from_the_module` asserts identity, not equality
  — a stamp that cannot disagree with the law that ran (the C-4 lesson, correctly applied).
* **Zero RNG, and I measured it rather than reading it.** The law is one division on two floats; no
  draw added, none moved, `fire_chance` and `_spoke_offset` keep their order. **S-4 class re-fired by
  me on the D-ARMED arm:** three boss seeds emitted twice → **SHA-256 identical both replicates.**
* **Derived at cast, per-fight-constant.** `target.movement_speed` is the KIT stat, not the per-tick
  `_e4_move_speed`/F8 product. Verified in source and in the traces: `wind_up_s` is
  `2.318840579710145` on every armed firing across five seeds.
* **`v <= 0` fallback declared and asserted** (`return float(p.wind_up_s)`), unreachable on this
  fixture. Spec §E-D authored in math note §2.7 — see WARN-5.

---

## 4. Obligation 4 — the onset-tick correction — **PASS, and the premise verified in source**

The correction is right, the direction argument is right, and it is the item in this landing I most
wanted to be right, because **Cell BAT's gate-of-record script inherits it.**

**My own measurement, five armed firings, from traces I emitted:**

| read | `d` | ≤ 10.5 (the fixed gate's own ceiling)? | `v_req` | ratio to bound |
|---|---|---|---|---|
| `tick − 1` | **10.78359052386978** | **NO** | 0.524577 | 0.101367 |
| **`tick`** | **10.208590523869779** | **YES** | **0.7725453365811579** | **0.14928412301085175** |
| `tick + 1` | 9.633590523869776 | yes | 1.020514 | 0.197201 |

Identical on all five seeds (the approach carries no RNG). **The falsifier holds:** at `tick − 1` the
distance exceeds the ceiling the cast gate itself applies, so the telegraph could not exist at that
position — a convention that contradicts the predicate which produced the record cannot be that
record's convention.

**I also verified the premise, not just the conclusion.** The argument rests on "no player position
mutation between the mob action phase and the tick record." Confirmed in source: the only player
position writes in the tick loop are `spatial_engine.py:5683` / `:5702` (movement) and
`_apply_soft_collision` at `:5716`; nova crossing resolve is `:5739`; the M-3 evade decision is
consumed inside the movement phase (`:5592` / `:5613`), **not** after the mob action. The mob action
phase runs at `:5949+` and the tick record is written at `:6691` with nothing between them that moves
the player. So the tick-*k* record holds exactly the position the caster measured — which is why
`d@tick` reproduces the F-WR2-3 diagnostic's independently measured cast distance to **10 decimal
places.**

`MIGRATION.md` §6 and math note §3.1 both state `tick` with the full falsifier table. **Recorded, not
silently edited** — the right call (Discipline #11). But see **WARN-4**: the contract as written is
not codeable.

---

## 5. Obligation 5 — S-7 spot-check reproduction — **PASS, to the last printed digit**

I did not grade gamora's JSON. I emitted the armed slice myself (boss + trash + champion +
mixed_pack × 6 seeds × 2 D arms), wrote my own grader, and applied my own predicate.

| quantity | my value | gamora's |
|---|---|---|
| firings assessed / hold / fail | **5 / 5 / 0** | 5 / 5 / 0 |
| unassessable (no speed field) | **0** | 0 |
| `d_onset` (all five) | **10.208590523869779** | 10.208590523869779 |
| `wind_up_s` (all five) | **2.318840579710145** | 2.318840579710145 |
| worst `v_req` | **0.7725453365811579** | 0.7725453365811579 |
| bound | **5.175** | 5.175 |
| **worst ratio to bound** | **0.14928412301085175** | 0.14928412301085175 |

The a-priori math-note value is `0.14928412301085192`; the measured is `0.14928412301085175`. They
agree through **15 significant figures** and diverge at the 16th. The charter's "15 s.f." is correct
and conservative. **A derivation written before the code and a measurement taken after it meeting at
the 15th digit is what makes P-2 a prediction rather than a restatement** (Discipline #1 + #11).

**The vacuity argument (§4.1) is correct and load-bearing.** Without an independent
`movement_speed_ms` the only route to `FRAC·v` from a trace is `radius_m / wind_up_s`, which *is* the
law, and S-7 collapses to `d ≥ 0`. I confirmed the conditional field at artifact level: **present
(`5.75`) on every armed trace, absent on every one of the six unarmed traces.** Both halves measured.

---

## 6. Obligation 6 — flag-OFF byte-identity vs `ecea69f` — **PASS, independently reproduced**

Method: `git archive ecea69f | tar -x` to `/tmp/jr_d_base` (read-only plumbing — no worktree, no
`.git` write), then the SAME unarmed slice emitted from each tree with `git_hash` pinned to one
literal so the header field is comparable. Slice: boss + trash × seeds 74000800/-01/-02 = **6 traces**,
all three v2 flags OFF.

* `diff -r base head` → **zero differing lines.** Not "modulo `engine_git_hash`" — literally zero.
* **SHA-256 identical on all 6**, and identical to the digests emitted from the baseline tree.
* The unarmed nova telegraph still carries the WR1 banked MEASURED values, verified by me from the
  trace: `tick 8`, `t_s 0.7999999999999999`, `wind_up_s 0.75`, `radius_m 12.0`,
  `fire_t_s 1.5499999999999998`, `fire_tick 15`, `range_m null` — and **seed 74000800 still has no
  ring.** SS-D-1's flag-OFF half is verified against the fixture's own numbers, as gamora claims.
* `range_m: null` on the telegraph event independently confirms the **ring-reconciliation** verdict:
  a ring has no forward extent, so the WR1 `range_m 10.0` / `radius_m 12.0` flag is a naming
  collision across two record blocks, not a lying telegraph. `radius_m` = `projectile_distance_m` =
  12.0 is one constant with four readers. **Name-and-pin ratification CONFIRMED.**

---

## 7. Obligation 7 — full regression name-diff — **PASS, EMPTY both directions, 81/81**

Run **ALONE** (charter §8.11 / the WR2 wave-tail law): sequential, single process, nothing else held
the editable install for the duration.

```
python3 -m pytest tests/ -q -p no:randomly --tb=no -rfE
60 failed, 6197 passed, 3 warnings, 21 errors in 1215.39s (0:20:15)
```

My totals match the cell's report (`60 / 6197 / 21` in 1205.00 s) **exactly on all three counts.**

| | count |
|---|---|
| observed FAILED+ERROR names | **81** |
| baseline names | **81** |
| **added** (mine, not baseline) | **0** |
| **removed** (baseline, not mine) | **0** |

**New-test delta judged.** `passed` rises by exactly **69** over Cell C's 6,128 (which I measured
myself at that gate) — precisely the 69 tests in `tests/test_wr2_d_nova_telegraph.py`, with no other
test-count movement anywhere in the suite. **Cell D's own suite 69/69** and **B + C + D + the two nova
suites (`test_wr1_m12_gd_mitigation_nova.py`, `test_wr1_m12b_m3_realized_count_telegraph_response.py`)
223/223**, both re-run by me.

**Process catch, self-ledgered by gamora and correct:** a comment-only source edit landed mid-run and
the regression was killed and restarted against the final tree rather than reasoned about (the Cell
B-FIX `inspect.getsource` hazard). ~7 min for a regression of record against a tree that still exists.
That is the lesson applied unprompted, and it is worth naming as the right instinct.

---

## 8. Obligation 8 — riding obligations, ZERO behaviour change — **ALL SIX DISCHARGED**

| item | discharge | my check |
|---|---|---|
| **WARN-1** flip clock | named in code (`:5654-5675`) + math note §5.1 + **pinned** by `test_the_flip_clock_is_a_REPOSITION_tick_clock_not_a_sim_tick_clock` | ✅ **and the pin CANNOT pass vacuously** — it asserts `n_repos > 0 and n_other > 0` *before* comparing, so a fight exercising one branch FAILS rather than proving nothing. It also pins the SOURCE: `src.count("self._orbit_ticks_since_flip = (") == 1` and that the single site sits inside the REPOSITION limb, so moving it to the tick loop fails the test and forces the §E periods to be re-read as seconds. This is exactly the declaration-vs-transcription gap I filed, closed the strong way. |
| **WARN-2** clearance | 0.80 → **0.30 m** at cell-note erratum + math note §5.2 + `test_WARN_2_...` | ✅ arithmetic re-derived: `min(AOE_RADIUS_DEFAULTS.values()) = 3.0`, `band_outer(boss) = 2.70`, clearance **0.30**. The two-different-0.80s trap is named at the Cell C note. |
| **WARN-3** MIGRATION §5 | restated by field name `total_abs_turn_rad` (path-derived, **not** `heading_rad`) with the measured counter-table | ✅ and the counter-table numbers (3.84/4.07/150.80 vs 4.9651/1.7081/129.1411) are the ones I measured at Cell C, unchanged. Cell B moving them in OPPOSITE directions is stated. |
| **WARN-5** annulus | named beside SS-C-3 in the Cell C math note **and** D math note §5.4, with the `BAND_WIDTH` coupling; `test_WARN_5_...` | ✅ band arithmetic re-derived live: boss `(2.10, 2.70)`, mob `(1.10, 1.7000000000000002)`. The annulus `d ∈ (1.70, 2.00]` and the "closes at `BAND_WIDTH ≥ 0.90`" coupling both hold. **Name-and-pin, not repair** — as ratified. |
| **INFO-1 / INFO-4** | stall convention (3.84 vs 7.43) + `azimuth_reversals` deadband (1/3/21 vs 9/23/22) in `trajectory()`'s docstring; `test_INFO_1_and_INFO_4_...` | ✅ present and pinned so a later edit cannot quietly drop them. |

WARN-5's discharge is materially *more* than the "one fact" I asked for — a full measured block on
both sides of the annulus with the tuning-lap trigger stated. Good.

---

## 9. Obligation 9 — residual counters (§B-6) — **PASS, re-measured by me on all four tiers, both arms**

I re-emitted all four tiers × 6 seeds × both D arms and read the counters myself:

| tier | fights | ticks D-OFF | ticks D-ON | per fight | worst gap |
|---|---|---|---|---|---|
| **trash** | 6 | **12** | **12** | **2.000** | **0.0013506294675260655 m** (1.3506 mm) |
| champion | 6 | 0 | 0 | 0.000 | 0.0 |
| mixed_pack | 6 | 0 | 0 | 0.000 | 0.0 |
| boss | 6 | 0 | 0 | 0.000 | 0.0 |

**Identical under D on every tier** — the required answer, since D changes timing and not geometry.
The trash figure reproduces Cell C's `180 = 2 × 90` signature exactly, and the 1.3506 mm matches
gamora's printed digits. **Not repaired** (charter instruction). The two-quantities warning is
correct: 1.3506 mm is the counter's deliberate PRE-correction over-report; the 0.98 mm Cell C and I
both measured is the POST-solver overlap in emitted frames. **WARN-2's evidence boundary is still not
reached.**

Corroborating S-6, also re-measured: boss `elapsed_s` moves **both** directions
(801 `17.6→40.2`, 802 `35.5→20.4`, 803 `37.3→20.8`, 804 `17.5→37.0`, 805 `37.1→22.0`) and is
**exactly unchanged on 74000800** — the one seed with no ring. `winner` is `monster` 6/6 in both arms.
Crossing COUNT is 5/5 in both arms; what moved is WHEN. gamora's "the cleanest available
demonstration that the arm acts through the nova and nowhere else" is a fair reading and I reproduce
every figure.

**F-WR2-3 CLOSED, confirmed:** `n_nova_crossings` per seed under `_bsep` = 0, 1, 1, 1, 1, 1 where
Cell C measured 0 on all six. The 74000800 miss is the 80 % `Chance` draw and **not** the gate — I
confirmed that independently: the same seed also mints no ring at **flags-OFF**, where the gate is
not in question.

---

## 10. Conductor-ruling check (§8.24) — standing safeties §6.2

| ruling | my check |
|---|---|
| cast gate 6/6 at `d = 10.2086 ≤ 10.5`; `n_nova_crossings` 0 → 1 on five seeds | **CONFIRMED** (see §9). The "6/6" for the gate itself is inferred rather than banked — see INFO-2. |
| 19-site sweep, exactly ONE out of law, **class closed not just instance** | **class conclusion CONFIRMED by a stronger check** (§1.1). The *completeness* claim is **WARN-1**. |
| `T = 2.319 s` vs measured 0.750 (3.09×), zero RNG, per-fight-constant | **CONFIRMED** exactly (§3) |
| S-7 5/5, worst 0.149, matching a-priori to 15 s.f. | **CONFIRMED** to the last digit (§5) |
| flag-OFF byte-identity exact; name-diff EMPTY 81/81; 69/69; 223/223 | **ALL CONFIRMED** by independent re-run (§6, §7) |
| **onset tick is `tick`, not `tick − 1`**; Cell BAT's script MUST use `tick` | **CONFIRMED**, falsifier sound, premise verified in source (§4) |
| report baseline pins at `796a6f6d`; trace identity at `ecea69f` | **CONFIRMED** — two `wave_regime` keys are unconditional; trace content unaffected and byte-verified. The standing rule *"report-baseline pins at the latest landing; trace-identity pins at the mechanism baseline"* is the right generalization of a class now on its third occurrence. |
| ring reconciliation RATIFIED name-and-pin | **CONFIRMED** — telegraph `range_m` is `null`; `radius_m` 12.0 is one constant, four readers (§6) |
| R-WR2-21 premise: M-3 dark on the battery of record | **CONFIRMED** — `piloted_competence_m3` is hard-coded `None` at `kitcal_g5_harness.py:1922`. Refusing to drop the clause is the same law as R-WR2-16 R3 and the paired M-3 arm is the right instrument. |
| **FOOTPRINT classification RATIFIED; "harmless on this fixture (no circle skill in the boss kit)"** | classification **CONFIRMED**; the parenthetical is **FALSE** → **WARN-2** |
| **"D reaches the clause through telegraph tick count (8 → 24), not through budget"** | direction right, arithmetic incomplete → **WARN-3** |

---

## 11. WARN items

### WARN-1 — the sweep is conclusive on REACH but is not grep-complete, and this is the law's first enforcement

**Descriptive.** gamora's table lists 19 sites with correct `ecea69f` line citations. My own
enumeration finds **at least ten further distance/radius comparison sites** absent from it (§1.2),
including two *duplicated* predicate families the table treats as single-sited: a second leash
(`spatial_engine.py:712` beside the listed `:1990`) and a second copy of the kite/standoff family
(`commitment_state_machine.py:158/165/170` beside the listed engine `:2081/:2104/:2114`).

**Rationale.** Charter §8.22 (ii) is worded "enumerated by grep." None of the omissions is REACH, so
the *verdict* is unaffected and the class **is** closed — but the law's value is that a second party
can reproduce the enumeration and get the same set. I could not. The duplicated families are the
substantive part: a future range law that legitimately reaches an AI-STATE or MOVEMENT predicate would
have to be applied at two sites, and the table would send the builder to one.

**Recommendation.** gamora: extend math note §1.3 with the missing sites and their classes (no code
change, no re-run). gandalf: consider sharpening §8.22 (ii) to require the **grep invocations** be
recorded alongside the table, so "complete" is checkable rather than assertable — the same reason
INFO-1/-4 now live in a docstring beside their numbers.

### WARN-2 — "this kit carries no circle skill at all" is FALSE, it is MY error, and it changes the ledger item's trigger

**Descriptive.** Five documents plus a conductor ruling state that the circle-AoE whiff window is
harmless because the fixture has no circle skill. **The boss kit does carry one.** From the header of
a trace I emitted:

```
mob boss&quest_slith_wightmirecave01_0 | radius 1.5
       0 slith_wightmirecave01_attack     point   range_m 2.0
       1 primordian_frigidring_r4         circle  range_m 10.0
```

The nova IS the circle skill. `_aoe_radius_for_skill` on it returns **3.5** (its
`effect_category` is `None`, so the default applies). What actually keeps the window shut is the
branch at `spatial_engine.py:6003` — `if skill.get(_GD_NOVA_KEY) is not None:` intercepts **before**
the generic-AOE `else`, so the ring goes to `gd_nova`'s analytic resolver and never reaches
`_compute_circle_hits`. I verified `_gd_nova` is present on that skill and absent on the other three
mob skills in the tier.

**Provenance: mine.** My Cell C finding wrote *"this kit carries no circle skill at all
(`feral_claws_r16` cone / `rip_and_tear_r16` line, per the trace headers)"*. I read the **player's**
entity block and generalized to the fixture. gamora propagated it verbatim into the Cell C note
erratum, math note §1.4 and §5.2, and cell note §3.2 / §7.10; the conductor then ratified it into
charter §8.24 as *"harmless on this fixture (no circle skill in the boss kit)"* — the exact inversion.
**This is the same failure shape as F-WR2-3 and as the gate-escape §8.22 (ii) exists to prevent: I
checked one consumer instead of every consumer.**

**Why it matters beyond tidiness.** The ledger item's true trigger is *"a circle-geometry skill without
a `_gd_nova` block"*, not *"a kit gains a circle skill."* And for a skill of the nova's shape the
window is not the 0.5 m-wide `(3.0, 3.5]` on record: it is `(aoe_radius, range_m + r_target]` =
`(3.5, 10.5]` — a **7.0 m** window. So both the trigger condition and the magnitude on the ledger are
understated.

**Recommendation.** gamora: correct all four engine/meta sites, restate the guard as the `_gd_nova`
intercept by file:line, and record the `(3.5, 10.5]` magnitude for the without-`_gd_nova` case.
gandalf: correct the §8.24 parenthetical in the ruling ledger — the *disposition* (FOOTPRINT ≠ REACH,
reported-not-repaired) is unaffected and I re-affirm it, but a ruling should not rest on a false
ground. **I own the origin of this and am filing it against my own prior finding.**

### WARN-3 — the M-3 evade arithmetic is right at cast and incomplete across the window; R-WR2-21 pre-names its FIRST SUSPECT on the incomplete form

**Descriptive.** Cell note §7.9, MIGRATION §8 and charter R-WR2-21 all state that
`min(t_remaining, ACTIONABLE_WINDOW_S)` binds in **both** arms, so *"D changes the per-tick evade
budget by exactly nothing"* and reaches R-WR2-19's second clause *"through telegraph TICK COUNT
(8 → 24), not through budget."* But `t_remaining_s` is `ring.t_launch − elapsed`, evaluated **per
tick** and decreasing (`telegraph_response.py:215`), so the cap binds in the D-OFF arm only on the
**first** tick. My recomputation:

| arm | telegraph ticks | **ACTING ticks** (`t_eff > 0`) | first-tick budget | executed-reach ceiling |
|---|---|---|---|---|
| D OFF (0.750 s) | 8 | **5** | 2.3000 m | ≈ **2.59 m** |
| D ON (2.3188 s) | 24 | **21** | 2.3000 m | ≈ **11.61 m** |

`t_eff = min(t_rem, 0.70) − 0.30 ≤ 0` whenever `t_rem ≤ 0.30`, so the last **three** ticks of *any*
window are HOLD. The figures on record (8 → 24 ticks, ≈4.3 → ≈13.3 m) count telegraph ticks, not
actionable ones.

**Rationale.** The direction is unchanged and D reaches the second clause **more** strongly than
reported, so R-WR2-21's disposition survives untouched. The risk is diagnostic, not directional:
R-WR2-21 pre-names `ACTIONABLE_WINDOW_S` as **FIRST SUSPECT** if the crossing rate does not drop, and
grounds that on "the budget is identical in both arms." A Cell BAT grader holding that sentence would
mis-diagnose a measured non-drop, because the budget is *not* identical across the window — the
mechanism's reach into the clause is ~4.5× larger than the "budget is identical" framing implies.
`ACTIONABLE_WINDOW_S` remains M-graded and outside spec §E; **nothing should be tuned** — this is a
correction to the *arithmetic on record*, not a request to move a constant.

**Recommendation.** gamora: restate §7.9 and MIGRATION §8 in ACTING ticks (5 → 21) with the
`t_eff ≤ 0` floor named. gandalf: carry the corrected form into R-WR2-21 / the Cell BAT brief so the
FIRST SUSPECT designation rests on the right arithmetic.

### WARN-4 — the S-7 field contract is not codeable as written, and it feeds the gate of record

**Descriptive.** Math note §3, cell note §4 and MIGRATION §6 all give the predicate as
`player.x_m@[onset_tick]`, with the source named as
`<tick record where tick == onset_tick>.entities[is_player].x_m`. **Tick-record entity blocks carry no
`is_player` key.** They carry `entity_id`, `alive`, `x_m`, `y_m`, `heading_rad`, `hp`, `commit_state`,
`commit_skill_idx`, `is_leashing`, `is_activated`, `energy`, `skill_cooldowns`, `ailments`. A grader
must resolve the player's `entity_id` from the **header** block where `is_player == true`, then join on
`entity_id`. Separately, the telegraph record is `{"record_type": "event", "event": "telegraph", ...}`
— not `record_type: "telegraph"`.

**Rationale.** I hit both while writing my own grader; the first raised `IndexError` on an empty list.
This is the **same class** as the onset-tick error the cell corrected: a contract statement a
downstream script inherits verbatim. Discipline #8 (schema validation at boundaries) — a field
contract whose join key is unstated is a contract with a hole in it.

**Recommendation.** gamora: add the two join facts to MIGRATION §6 and math note §3 (one line each,
documentation-only — **I approve this directly under ADR-002**). gandalf: Cell BAT's grading script
should be written against the corrected contract, not the current text.

### WARN-5 — spec §E carries no Mechanism-D rows, and spec §G has no Cell-D obligation class

**Descriptive.** The tunable/frozen wall for D (`NOVA_ESCAPE_FRAC` YES; the law, the `R` source, the
`v` source, the `v ≤ 0` fallback, the ring identity, the flag default all NO) exists **only** in
gamora's math note §2.7 as "§E-D — spec §E's table, extended." Spec §E itself still lists only B and C
rows. Spec §G likewise scopes Gate-2 obligations to Cell B and Cell C; Cell D's obligation class came
from the charter and this brief.

**Rationale.** Charter §8.23 ruled, on WARN-4/-5 at Cell C, that **"spec §C-1 is the operative text"** —
i.e. the spec is the operative frozen wall and a cell note is not. D's wall therefore sits outside the
document the run has declared operative. The content is Matt-signed and correct; the *home* is wrong,
and a tuning lap reading §E to find out what it may move will not find D there.

**Recommendation.** gandalf (SPEC-AUTHOR): fold the §E-D rows into spec §E and add a Cell-D row to
§G, so the wall and the obligation classes each have one home. No behaviour, no re-run.

---

## 12. INFO items

- **INFO-1 — the escape law's one free input is UNGRADED.** `v = 5.75 m/s` comes from
  `movement_speed=float(class_dict.get("movement_speed", 5.75))` (`spatial_engine.py:7182` at
  `ecea69f`, exactly as the math note cites — citation correct). That is an **engine default filling
  an absent kit field**, neither M nor D. Math note §2.2 calls it *"measured, not assumed"*; the
  accurate statement is *read from the engine, not transcribed.* This matters because SS-D-1's whole
  frame is grading discipline: the cell carefully grades the constant it **replaces** (0.750 = M, 45
  frames @ 60.000 fps CFR, bracket 0.717–0.750) and leaves the constant it **reads** ungraded — which
  is the shape H-M2-f exists to name. Consumer consequence for drax: the `3.09×` / `1.57 s` figures in
  MIGRATION §2 are **default-specific**, and any kit that declares `movement_speed` shifts `T`.
  Recommendation: name the grade in math note §2.2 and add a `v` row to §E-D.
- **INFO-2 — only the boss-tier S-7 slice is banked.** `2026-07-30-wr2-cell-d-s7-spotcheck.json` is
  the sole raw artifact (2 arms × 6 boss fights × 5 firings). The §7.6 four-tier residual table, the
  §7.4 SHA-256 list, the §7.5 regression name list, and the §7.1 "gate 6/6" figure are **asserted, not
  banked** — the `s7` array holds 5 entries, and 74000800's gate pass is an inference from the
  flag-OFF `Chance` miss. **I independently re-measured every one of them and they all hold**, so this
  is a bankability note, not a correctness one. Cell C's precedent (statistics + S-4 JSON committed)
  was slightly wider. Recommendation: bank the four-tier counter table and the regression name list
  with Cell BAT, since Cell BAT re-reports both.
- **INFO-3 — the CORRECT 0.80 m was not labelled at its own site.** Cell note §6.2 says "Both are now
  labelled at both sites," but the Cell C math note's §2.2 line still reads *"the reach term is slack
  by 0.80 m (boss) and 0.80 m (mob)"* with no disambiguating label. Only the D math note §5.2 names
  the collision. One clause at `wr2-c-movement-policy-2026-07-29.md:92` closes it.
- **INFO-4 — two line-number conventions in one note, neither stated.** The sweep table (§1.3) cites
  **pre-landing** (`ecea69f`) lines — I verified 18 of them resolve exactly — while cell note §2.1
  cites **post-landing** lines. Both are internally correct; a reader diffing one against their own
  tree will be off by 3–130 lines depending on which table they are in. One header line each.
- **INFO-5 — the ADR-004 cross-seam round-trip is satisfied but not yet acknowledged.** MIGRATION
  names star-lord (two unconditional `wave_regime` keys, a moved report baseline) and drax (the
  conditional `movement_speed_ms` and a 3.09× telegraph-duration change, with the explicit warning
  that a tell animation hard-coded to 0.750 s will be wrong by 1.57 s). The field is v1-ADDITIVE and
  CONDITIONAL so nothing breaks, and `replica-frame/v1` correctly does not bump. Routing the two
  acknowledgements is the outstanding half.

---

## 13. Action

- [x] **jack-ryan:** verdict **CLEAR-with-notes**. **Cell BAT RELEASES on this gate.** No BLOCK, no
      Matt escalation, no commitment boundary reached. The S-3 tuning lap remains **UNSPENT**; every
      §E parameter and `NOVA_ESCAPE_FRAC` sit at their declared defaults.
- [x] **jack-ryan (ADR-002 direct approval):** the 69 new tests approved as test additions; the six
      riding-obligation discharges approved as documentation-only; WARN-4's two contract lines
      pre-approved as documentation-only.
- [x] **jack-ryan (self-correction):** WARN-2 filed **against my own Cell C finding**. The
      no-circle-skill claim originated with me and I checked one entity block instead of the roster.
- [ ] **gamora:** **WARN-1** — extend math note §1.3 with the ten missing sites and their classes,
      including the two duplicated families (`:712` leash, `commitment_state_machine.py:158/165/170`).
      Doc only, no re-run.
- [ ] **gamora:** **WARN-2** — correct all four engine/meta sites; restate the guard as the
      `_GD_NOVA_KEY` intercept at `spatial_engine.py:6003` by file:line; record the `(3.5, 10.5]`
      magnitude for a circle skill without a `_gd_nova` block. Doc only.
- [ ] **gamora:** **WARN-3** — restate §7.9 and MIGRATION §8 in ACTING ticks (**5 → 21**, not 8 → 24)
      with the `t_eff = min(t_rem, 0.70) − 0.30 ≤ 0` floor named. **Do not touch
      `ACTIONABLE_WINDOW_S`** — it is M-graded and outside §E.
- [ ] **gamora:** **WARN-4** — add the two join facts to MIGRATION §6 + math note §3: the player's
      `entity_id` comes from the header's `is_player` block and joins on `entity_id` in tick records;
      the telegraph record is `record_type: "event"` with `"event": "telegraph"`.
- [ ] **gamora:** **INFO-1** — name `v = 5.75`'s grade (engine default, not M) in math note §2.2 and
      add a `v` row to §E-D. **INFO-3 / INFO-4** — one clause each.
- [ ] **gandalf (RUN-CONDUCTOR):** **WARN-2** — correct §8.24's *"no circle skill in the boss kit"*
      parenthetical in the ruling ledger. The FOOTPRINT disposition stands and I re-affirm it; the
      stated ground is false and the ledger item's trigger + magnitude both change.
- [ ] **gandalf (RUN-CONDUCTOR):** **WARN-3** — carry the corrected evade arithmetic into R-WR2-21 and
      the Cell BAT brief, so the pre-named FIRST SUSPECT rests on the right numbers.
- [ ] **gandalf (SPEC-AUTHOR):** **WARN-5** — fold §E-D into spec §E and add a Cell-D row to §G.
- [ ] **gandalf:** **WARN-1** — consider requiring the grep invocations be recorded alongside any
      §8.22 (ii) sweep table, so completeness is checkable rather than assertable.
- [ ] **gandalf:** **INFO-2** — have Cell BAT bank the four-tier residual table and the regression
      name list it re-reports. **INFO-5** — route the star-lord and drax MIGRATION acknowledgements.
- [ ] **Matt:** nothing. Mechanism D is Matt-signed (R-WR2-19) and shipped inside its signature;
      `NOVA_ESCAPE_FRAC` is untuned at 0.90; no M-graded constant was moved; SS-D-1 is named, not
      laundered, and `NovaParams` is not mutated.

---

## 14. References

**Reviewed (engine, `796a6f6d`):**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gd_nova.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/telegraph_response.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/reposition.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/commitment_state_machine.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wr2_cell_c_move_2026_07_29.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wr2-d-nova-telegraph-2026-07-29.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wr2-c-movement-policy-2026-07-29.md`
- `~/Games/reincarnated-engine/tests/test_wr2_d_nova_telegraph.py`

**Reviewed (meta):**
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr2-cell-d-nova-telegraph.md`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr2-f3-nova-diagnostic.md`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-30-wr2-cell-d-s7-spotcheck.json`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt` (81-name baseline)
- `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr2-cell-c.md` (my prior; corrected by WARN-2)

**Governing:**
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` §6, §8.21–8.25
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-29-wr2-mechanism-spec.md` §D, §E, §G

**My own evidence (scratch, regenerable, not banked):**
`/tmp/jr_d_base/` (`git archive ecea69f` scratch tree) · `/tmp/jr_d_bytecheck.py` ·
`/tmp/jr_d_tr_base/` + `/tmp/jr_d_tr_head/` (byte-identity, 6 traces each, SHA-256 identical) ·
`/tmp/jr_d_s7.py` (my S-7 grader + four-tier residual re-report) · `/tmp/jr_d_arm_bsep/` +
`/tmp/jr_d_arm_ntv2/` (armed slices, 4 tiers × 6 seeds) · `/tmp/jr_d_s4_rep2/` (S-4 replicate on the
D-armed arm) · `/tmp/jr_d_regression.txt` (full regression, 1215.39 s) · `/tmp/jr_d_names.txt` +
`/tmp/jr_d_baseline.txt` (name-diff, EMPTY both directions)
