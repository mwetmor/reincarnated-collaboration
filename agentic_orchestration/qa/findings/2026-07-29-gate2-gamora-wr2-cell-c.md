# Finding — 2026-07-29 — WR2-ENCGEO Cell C (movement policy v2, Mechanism C)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** CLEAR-with-notes
**Target:** `61a6be4` (build) + `ecea69f` (gates), as one landing, on base `4f09e35`
**Developer:** gamora (relaunched cell; the build originates in a dead predecessor's adopted fragment)
**Run:** WR2-ENCGEO-2026-07-29 · charter §8.14–8.20 · mechanism spec §C / §D / §E / §G
**Principles applied:** 1 (math-before-code), 2 (smoke/gate discipline), 3 (cross-seam impact), 4 (decisions-log / ruling ledger as truth), 5 (severity matters), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #3, #10, #11, #12

---

## Verdict

**CLEAR-with-notes. Cell BAT releases.**

Every pre-registered gate the charter owes this cell (S-2, S-3, S-4, flag-OFF regression name-diff,
flag-OFF byte-identity, the `boss__B__seed74000802` trajectory reconstruction) is independently
confirmed. The full regression name-diff is **EMPTY both directions**. The adoption of the dead
agent's fragment is **audited and earned** — I spot-verified eight measured claims from the battery
on disk with my own checkers, and every one reproduces, several to 17 significant figures. The one
number that did not reproduce under a naive estimator is fully explained by the committed
instrument's own stall convention, which I reproduced exactly.

Five WARN and six INFO below. **None blocks.** No re-run is owed. Every WARN is a prose,
attestation or unnamed-semantics item; nothing touches a frozen row, a gate arithmetic, or the
determinism contract.

---

## 1. Full regression, name-diff law (Obligation 1) — **PASS, EMPTY both directions**

Run **ALONE** per charter §8.11 (no parallel pytest against the shared editable install; nothing
else held the install for the duration — all of my own analysis below reads JSON and imports no
package):

```
python3 -m pytest tests/ -q -p no:randomly --tb=no -rfE
```

```
60 failed, 6128 passed, 3 warnings, 21 errors in 1217.11s (0:20:17)
```

My totals match the cell's report (`60 / 6128 / 21` in 1226.30 s) exactly on all three counts.

**Name-diff against the 81-name baseline** — `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`:

| | count |
|---|---|
| observed FAILED+ERROR names | **81** |
| baseline names | **81** |
| **added** (in mine, not baseline) | **0** |
| **removed** (in baseline, not mine) | **0** |

**EMPTY both directions.** The name-diff is the criterion, not "adjacent suites green" (WR1 §8.19,
charter §6) — and it is the count-plus-names form, so a swap that held the total constant could not
hide. Nothing regressed and nothing silently started passing.

**New-test delta judged.** The `passed` count rises by exactly 44 over Cell B's 6,084: the 43 tests
in `tests/test_wr2_c_movement_policy.py` plus one SS-C-2 test added to
`tests/test_wr1_m12b_m3_realized_count_telegraph_response.py`. I enumerated the 43 by name — every
one maps to a spec §C/§D/§E row or a riding obligation, and three are of the *right* class rather
than the convenient one:

- `test_engine_inline_predicate_matches_the_seam_on_a_grid` — pins the engine's **inlined**
  advance/reposition predicate against `policy/seam.movement_intent`. Cell B's HALT was a
  transcription defect of exactly this shape (charter §8.8); pinning the two rather than trusting
  them to agree is the correct generalization of that lesson.
- `test_a_ROOTED_player_does_not_orbit_and_the_HELPER_IS_NEVER_CALLED` — the strong form. A test
  asserting only "did not move" would also pass against an implementation that computed an orbit
  and multiplied it by zero.
- `test_arming_C_MOVES_the_fight_the_arm_is_not_inert` — P-2's converse, so no measurement in this
  cell rests on an arm that might be inert.

The M-12b cardinality pin moves 3 → 4 rather than being loosened to `>=`. That pin is the tripwire
that caught the enum growth; moving it is right, weakening it would not have been.

---

## 2. Adoption audit-of-the-audit (Obligation 2) — **the audit was REAL**

Charter §8.15 set a discard-default. The relaunched cell declined it, claiming a full line-audit
plus re-derivation of every measured number. That claim is the thing under review, and the hazard
the cell itself named is the right one: an audit can prove code conformance, but it cannot prove a
measurement, and `MIGRATION.md` §5/§7 carried specific numbers with **no `wr2_cell_c/` battery on
disk** at the time.

I picked the three inherited numbers the cell flagged as unverified prose, plus five more the
fragment's own code produces, and re-derived all eight myself from the battery — my own checkers,
my own predicates, no import of the cell's driver.

| # | Claim (origin: the dead agent's fragment) | My independent value | Verdict |
|---|---|---|---|
| 1 | trajectory `~150 rad` on `boss__B__seed74000802` | **150.7957626798417** rad, **23.99989** circles | **EXACT** |
| 2 | straightness `0.48 → 0.07` | WR1 **0.4836**, Cell B **0.4838**, Cell C **0.07321** | **EXACT, all 3 arms** |
| 3 | nova `44/60 → 0/60` | `n_nova_crossings` **44 → 0 → 0**; `circle` telegraph **1 → 0 → 0** | **EXACT, and the wording correction is VALIDATED** — see §2.1 |
| 4 | player-alive tick counts per tier | 5,292 / 6,223 / 22,550 / 99,699 | **EXACT** |
| 5 | S-2 wall shares per tier | 0.0000 / 0.0000 / 0.0000 / **1.0040 %** | **EXACT** |
| 6 | S-1 worst post-solver overlap | **0.0009889945962079372 m** | **EXACT to 17 s.f.** |
| 7 | residual-counter uniformity | all 90 trash fights carry **(2 ticks, 0.00135062946752607)** identically | **EXACT to 17 s.f.** |
| 8 | SS-C-3 advance delta | 4,989 total; boss 960 / champion 330 / trash 180 invariant on all 3 legs; mixed_pack {191,191,197} | **EXACT, delta −51** |

### 2.1 The wording correction the cell made is the right one, and I can ground it in the field's own location

The fragment's `MIGRATION.md` said *"boss-tier nova casts fell 44/60 → 0/60."* The cell corrected
this to `n_nova_crossings`, a per-leg aggregate, and restated by field name. That correction is
**independently confirmed by where the number lives**: it is at
`report["a_dmg_1_grain"]["per_tier"]["boss"]["n_nova_crossings"]` — a per-leg aggregate block — and
it is **44 identically on all three legs** of `wr1_battery_2` (with `worst_nova_crossing_hp`
414.8 / 470.8 / 414.8). A per-fight cast count over three legs with different mitigation regimes
could not be leg-invariant. The fragment's sentence was wrong; the cell's is right. This is exactly
the §8.13 WARN-1 class, caught by the cell on its own inherited work.

**Conclusion on the adoption.** The audit was not asserted, it was performed. The single real hazard
the cell identified (unbacked numbers in a consumer-facing document) was the correct one, it was
closed by re-derivation rather than by trust, and one inherited sentence *did* fail re-derivation
and was corrected rather than smoothed over. **The WIP-triage deviation is correct and I ratify it.**
Attribution is clean per Discipline #10 — the commit message names the fragment as the predecessor's
work and the audit/corrections as this cell's.

---

## 3. Frozen-row conformance (Obligation 3) — **every row holds, three of them structurally**

| Frozen row (spec §E / §C-5 / §C-6) | How I checked | Verdict |
|---|---|---|
| Precedence EVADE ▸ REPOSITION ▸ ADVANCE ▸ HOLD | `if _m3_handled: pass` → `elif` REPOSITION (`:5532`) → `elif` ADVANCE (`:5570`) → HOLD. The M-3 tick claim is preserved verbatim; the REPOSITION limb sits strictly below it | **PASS, structural** |
| **heading-faces-target (C-5)** — the silent S-3 killer | measured on the ARMED battery, not just by unit test — see §4.3 | **PASS, 0 / 133,764 ticks off-cone** |
| REPOSITION does not suppress the attack (C-6) | the limb touches neither `_m3_evaded_this_tick` nor `action_available_at`; `grep` over the limb confirms no attack-side write | **PASS** |
| flip trigger SET (wall / dwell / target-change) | the three triggers are the only disjuncts in `reposition.py:trigger`; no fourth, none removed | **PASS** (but see WARN-1 on the *clock*) |
| flag defaults OFF | `False` at both engine entry points (`spatial_engine.py:3161`, `:7455`) and all three harness entry points (`kitcal_g5_harness.py:773`, `:1628`, `:1724`) | **PASS** |
| §E tunable defaults | `reposition.py` constants are 0.60 / 3.0 m / 0.50 / 0.10 m / 0.60 m / 4.0 s / 0.8 s / 0.50 — the spec table exactly. Lap UNSPENT | **PASS** |
| player-only scope (R-WR2-13) | `_navigate_entity` body untouched — the 2 diff hits are both comments, and no hunk in the 236-line engine diff falls in that function. Stronger: `wall_repulsion` / `WALL_BAND_M` / `WALL_PUSH_FRAC` appear **nowhere** in `spatial_engine.py`, so no mob or boss path can reach wall-awareness even by accident | **PASS, structural** |
| standard multiplicative chain (C-0) | `v · self._tick_size · _e4_move_scale` → `arena.clamp_entity` → `total_displacement += hypot(realized)`. The limb is additionally gated on `_e4_move_scale > 0.0`, so a rooted/hard-CC'd player never reaches the helper | **PASS** |
| band re-derived vs R-WR2-17 reach | boss `0.5+1.5+0.10 = 2.10`, `min(2.70, 2.0+1.5=3.50) = 2.70`; mob `1.10`, `min(1.70, 2.50) = 1.70`. Width binds both rows; reach slack 0.80 m. Inversion guard `if band_outer < band_inner` present and tested | **PASS — C-1 degeneracy dissolved** |

**C-5 is enforced structurally, not by convention:** `reposition_vector` has no heading output at
all, so a tangent-writing bug is unavailable rather than merely avoided. Same for C-6 (no
attack-side output) and R-WR2-13 (the wall term is unreachable outside the player limb). This is the
right shape for the three rows whose violation would have been silent.

---

## 4. Independent falsification (Obligation 4) — four candidates, all fired

Everything below is my own instrument reading the battery on disk. Nothing imports the cell's driver.
Scratch: `/tmp/jr_c_s2.py`, `/tmp/jr_c_s1.py`, `/tmp/jr_c_traj.py`, `/tmp/jr_c_heading.py`.

### 4.1 S-2 recomputed per tier — **PASS, and I STATE the predicate, which is NOT load-bearing**

**The predicate, stated** (charter §3 asks for "wall-contact"; the cell's operative definition is
the WR1-ENV clamp probe's, math note §9.1): a player-alive tick is wall-contact **iff**

```
min( |x − r| , |x − (W − r)| , |y − r| , |y − (H − r)| )  <  CLAMP_EPS = 1e-6
```

with `r` the player's per-entity radius from the trace header and `W`/`H` from the header frame.
This is a **clamp detector**, not a proximity detector: it asks whether the arena clamp is binding,
not whether the player is near a wall. That choice is load-bearing *in principle*, so I falsified it
by sweeping the epsilon:

| tier | alive ticks | share @1e-6 | @1e-3 | @1e-2 | @1e-1 | final-10 s | corner |
|---|---|---|---|---|---|---|---|
| trash | 5,292 | 0.0000 % | 0.0000 | 0.0000 | 0.0000 | 0.0000 % | 0.0000 % |
| champion | 6,223 | 0.0000 % | 0.0000 | 0.0000 | 0.0000 | 0.0000 % | 0.0000 % |
| mixed_pack | 22,550 | 0.0000 % | 0.0000 | 0.0000 | 0.0000 | 0.0000 % | 0.0000 % |
| boss | 99,699 | **1.0040 %** | 1.0040 | 1.0040 | 1.3611 | **2.5796 %** | 0.0000 % |

**The definition is NOT load-bearing at this gate.** The boss share is *identical* across four
orders of magnitude of epsilon, and even under a **10 cm** band — 100,000× looser than the probe's —
it reaches only 1.3611 %, still clearing the 5 % gate by 3.7×. The S-2 PASS therefore does not rest
on a tolerance choice. (The insensitivity is itself informative: the distribution is bimodal —
either the clamp binds exactly, or the player is well clear. There is no population of
"nearly-pinned" ticks, which is what a residual pin would look like.)

Confirmed exactly against the cell's figures: **worst single trace 1.471 %**
(`pre/boss__B__seed74000810`), **worst single final window 6.000 %**
(`pre/boss__A__seed74000800`), and **corner share 0.0000 % on every tier** — the `(0.5, 0.5)` state
WR1-ENV measured at a median 70.8 % of boss ticks does not occur once in 450 fights, from a wall
term that contains no corner code. Both clauses PASS on every tier.

### 4.2 Trajectory recomputed on `boss__B__seed74000802` — **PASS, and I found the one estimator seam**

| quantity | WR1 (neither) | Cell B (B only) | Cell C (B+C) | cell's table | verdict |
|---|---|---|---|---|---|
| `total_abs_turn_rad` | **3.8361** / 7.4308 † | **4.0688** | **150.7958** | 3.84 / 4.07 / 150.80 | see † |
| full circles | 0.61 | 0.65 | **23.99989** | 24.00 | **EXACT** |
| `azimuth_sweep_rad` | **−0.14186** | **−0.25087** | **+6.32234** | −0.14 / −0.25 / +6.32 | **EXACT** |
| `azimuth_reversals` | **1** | **3** | **21** | 1 / 3 / 21 | **EXACT** |
| `straightness_ratio` | **0.4836** | **0.4838** | **0.07321** | 0.4836 / 0.4838 / 0.0732 | **EXACT** |
| path length (m) | 36.14 | 36.13 | **350.41** | — | (new) |

† **The one prose falsification, and it is an estimator seam, not an error.** My first estimator —
which links the movement bearing *across* stall ticks — returns **7.4308** rad for the WR1 baseline,
not 3.84. Root cause found and reproduced: the committed driver
(`wr2_cell_c_move_2026_07_29.py:540-547`) compares **adjacent step pairs** and `continue`s when
*either* step falls below 1e-9, so the turn *into* a stall and the turn *out of* it are both
dropped. Under that exact convention I reproduce **3.8361 → 3.84**. It matters only on stall-heavy
paths — WR1 stalls on 196 of 369 steps and Cell B on 538 of 652, while **Cell C stalls on 0 of 688**,
which is why the two conventions agree exactly on the AFTER arm and on Cell B. The convention is
applied identically to all three arms, so **attribution is preserved and the conclusion is robust
under either reading** (3.84 → 150.80, or 7.43 → 150.80). Recorded as **INFO-1**, not a WARN: no
number the run acts on moves.

**The mechanism attribution holds.** Cell B moves `total_abs_turn_rad` by ~6 % (3.84 → 4.07) and
leaves straightness flat (0.4836 → 0.4838). Cell C takes it to 150.80 and collapses straightness to
0.073. **C is the mechanism that turns the path**, and the B-only column is what proves it —
Discipline #10 satisfied with one changed thing between adjacent pairs.

### 4.3 S-3's three predicates, recomputed from the leg footers — **PASS, all three**

Computed from `footer.winner` per trace, independent of the cell's aggregation:

| leg / arm | my win rate | predicate |
|---|---|---|
| pre / A (no-evasion) | **0/30 = 0.000** | **S-3a PASS** — still killable |
| pre / B | **30/30 = 1.000** | **S-3b PASS** — win reachable |
| post / A | **30/30 = 1.000** | **S-3c PASS** |
| post / B | **30/30 = 1.000** | **S-3c PASS** |
| pre_endpoint / B | **0/30 = 0.000** | ⚑ F-WR2-2 confirmed; not a charter predicate |

All non-boss tiers are 30/30 on every leg. The ⚑ reproduces: `pre_endpoint`/B is 0.000. The cell's
refusal to claim a FAIL on a leg the predicate does not name, while surfacing it anyway, is the
correct disposition; conductor §8.19 has already routed it to S-6 and Cell BAT.

**And the silent S-3 killer, falsified properly — this is the check that mattered most.**

My first instrument was **wrong, and I record that**: comparing `heading_rad` against the bearing to
the **boss** returned 720 boss-tier ticks beyond the 75° cone half-angle. That is an artifact of the
wrong reference — `heading_rad` is written toward the **nav target** (`spatial_engine.py:5306`),
which in a boss cell may be an add. The per-tick `decision` event names that target, so it is the
right instrument. Against it:

| reference | worst \|heading − bearing\| | ticks beyond the 75° cone half-angle |
|---|---|---|
| same frame (post-move positions) | 0.7024 rad = **40.24°** | **0 / 133,764** |
| previous frame (pre-move proxy — the fair pair, since heading is written before the movement branch) | 5.168e-02 rad = **2.96°** | **0 / 133,764** |

**C-5 holds functionally on the whole armed battery, not merely by unit test.** Over 133,764 armed
player-alive ticks there is not one on which the cone's aim could have missed the nav target for a
heading reason, and the residual 2.96° is just the one-tick lag of the target's own motion. The
line/cone kernels still aim at the boss. This closes the failure mode spec §C-5 called "the single
easiest way to fail S-3 while believing the mechanism works."

### 4.4 S-1 carry-forward, recomputed from the emitted frames — **PASS 450/450**

Measured post-solver from the traces, never from the solver's own counters (§B-6's instrument would
otherwise grade itself):

- **312,956 pair-samples** — exact match.
- **0 violations** of `d ≥ rᵢ+rⱼ − 1 cm`.
- worst overlap **0.0009889945962079372 m** — **exact to 17 s.f.**, inside `ε_touch` = 1 mm and an
  order of magnitude inside S-1's 1 cm.
- worst locus: `pre/trash__none__seed74000800`, tick 43, pair `gd-werewolf-kitcal-1 ↔ zombie_a01_1`,
  **player↔mob**, and **neither body on any clamp bound on either axis** — I verified the wall status
  rather than asserting it, which is the §8.13 WARN-1 lesson, and the cell's claim survives it
  verbatim.
- worst overlap by tier: trash 9.890e-4, champion 9.719e-4, boss 9.526e-4, mixed_pack 8.911e-4 — all
  inside `ε_touch`.

Cell B's geometric invariant survives a configuration space it never visited.

### 4.5 Residual counters 7 → 180 (Obligation 5) — **verified, and the pattern is what the cell claims**

| | Cell B (`4f09e35`) | Cell C |
|---|---|---|
| `collision_residual_ticks` | **7** | **180** |
| `collision_residual_max_m` | **0.0012118003135626054** | **0.0013506294675260655** |
| locus | mixed_pack mob↔mob chains, 3 seeds | **trash, all 90 fights, exactly 2 ticks each** |
| mixed_pack | 7 | **0** |

Both counter values reproduce to 17 s.f. from the reports. The uniformity claim reproduces exactly:
**all 90 residual fights are `trash`/arm `none`, and all 90 carry the identical pair
`(2 ticks, 0.00135062946752607)`** — one distinct value across 90 fights, 3 legs and 30 seeds.
Per-tier residual ticks: trash 180, champion 0, mixed_pack 0, boss 0.

That seed- and leg-invariance is the substantive finding, and it is a *better-behaved* object than a
growing chain residual: it is a deterministic geometric consequence of the trash spawn layout plus
C's opening motion, exactly the spawn-adjacency signature charter §8.19 named. **Post-solver overlap
stays inside 1 mm** (0.98 mm, §4.4), so the geometry the traces carry is sound and the counter is
reporting its own deliberate pre-correction over-report. `ITER_MAX` correctly stays frozen —
raising it to pass a gate was refused at R-WR2-16 and no gate needs it. WARN-2's
evidence-boundary is knocked on but not crossed; that door is the conductor's.

### 4.6 Determinism (Obligation 4d / 5)

**Zero RNG in the new path, audited three ways.** `policy/reposition.py` imports **only `math`** —
no `random`, no `numpy`, no `rng`, no substream construction; spec §D-1's `ORBIT_STREAM_SALT` is
neither defined nor referenced. There is exactly **one call site** (`spatial_engine.py:5532`), gated
on `self._movement_policy_v2 and self.player.is_alive and _e4_move_scale > 0.0`. No draw site is
added, removed or reordered anywhere in the 236-line engine diff, so no downstream stream position
moves — which is what keeps the S-6 before/after diff uncontaminated.

**§D-6 rounding rule:** `flip_ticks(period_s, tick_size) = max(1, int(round(period_s / tick_size)))`
— one rule, stated once, seconds in, with a `tick_size <= 0` guard. Correct per spec. (But see
**WARN-1** on what increments the counter it feeds.)

**Orbit state cannot leak across fights:** `SpatialFightEngine` is constructed inside
`for fight_idx in range(n_fights)`, so `_orbit_sign` / `_orbit_ticks_since_flip` /
`_orbit_last_target_id` are fresh per fight. `_orbit_sign` initialises to the constant `+1`, not a
draw.

**No `NameError` path:** `_wr2b_residual_keys: dict = {}` is initialised at `:7794` ahead of both
conditional branches, so arming C without B is safe.

**A THIRD determinism replicate, fired by me, which also closes provenance.** After the regression
finished (so nothing shared the install), I re-fired the `pre` leg from the clean committed tree
using the **exact argv the cell's S-4 artifact declares**, into a scratch root, then ran a recursive
field diff against the banked leg with **no a-priori exclusion** — the exclusion set is *discovered*,
which is the form Cell A's Gate-2 asked for:

```
traces compared         : 150
DISCOVERED differing fields: header/engine_git_hash  ×150   (61a6be4 banked -> ecea69f re-fire)
                             ...and nothing else, over 150 pairs
```

Every other field of every record of all 150 traces is equal. This is worth more than a third
replicate, because **the gates commit `ecea69f` touches no engine source** — its four files are
`MIGRATION.md`, the math note, and the two JSON artifacts. So the banked battery (emitted at
`61a6be4`) and my re-fire (at `ecea69f`) execute byte-identical engine code, the sole differing field
differs *by construction*, and **the banked evidence is provably the output of the committed code.**
The cell's own S-4 (150/150, un-normalized, one process one tree — Cell A's lesson correctly applied)
stands confirmed and extended.

---

## 5. SS-1 (Obligation 6) — **INTACT, verified mechanically**

Zero files under `wr1_battery_2/`, `wr1_battery_2_aim/`, `wr2_cell_b_s1/` or `wr2_cell_b_s1_r2/`
carry an mtime after 22:00 on 2026-07-29 (the Cell C session's start; the landing commits are 22:47
and 23:17). Recursive `find -newermt` returns 0 of 454 / 454 / 455 / 455 files in the four roots.
The cell's `_assert_not_banked` guard was extended over Cell B's version to cover Cell B's *own* two
batteries — the right generalization of INFO-6, and it makes the preserved HALT battery evidence
rather than scratch. AFTER artifacts land beside, never over.

---

## 6. Riding obligations (Obligation 7) — **both discharged correctly, and the banked traces are untouched**

**(a) Charter §8.6 WARN-1 — the ungated evade-branch `frame_sink.decision`.** Now **unified** under
`_trace_decisions` rather than merely also gated, so the two emitters cannot drift apart again. The
review question is whether this changed any banked trace content. **It did not, and I verified it
two ways at artifact level:**

| battery | `--trace-decisions` | traces carrying ≥1 `decision` record |
|---|---|---|
| `wr1_battery_2` | OFF | **0 / 450** |
| `wr2_cell_b_s1_r2` | OFF | **0 / 450** |
| `wr1_battery_2_aim` | ON | 450 / 450 |
| `wr2_cell_c` | ON | 450 / 450 |

And on the armed battery the channel is **exactly one record per tick**: 133,854 `decision` records
against 133,854 `tick` records, with **zero** of 450 traces showing a mismatch. Two live emitters
would give two records per tick. The M-3 emitter therefore never fired anywhere — confirming
mechanically that M-3 is dark (`piloted_competence` is not passed by the harness at all) and that
SS-C-2's gating shift changed no banked content. The invariant "no `decision` records ⟹ the
instrument was off" now holds, which it did not before.

**(b) Charter §8.13 WARN-3 — the SS-B-2 in-code rationale.** Both sites (`_apply_soft_collision`
and `policy/seam.choose_target`) now cite **§D-3(1) value-equality between two DISTINCT entities**
and state plainly that the §D-3(3) NaN self-miss does not reproduce, with the CPython
`list.__contains__` short-circuit given as the reason. I confirmed the change is
**documentation-only**: the executable line `others = [e for e in entities if not any(e is _b for _b in bosses)]`
and the `choose_target` identity form are unchanged context in the diff, and the third hunk is a
docstring. The corrected rationale is genuinely stronger — the byte-identity claim becomes
unconditional rather than NaN-conditional. Approved directly under **ADR-002** (documentation-only).
Pinned by `test_WARN_3_...`.

---

## 7. WARN (5) — fix advisable, none blocking, no re-run owed

### WARN-1 — the flip clock counts REPOSITION ticks, not sim ticks. Unnamed, and it is the one dial-facing item.

`_orbit_ticks_since_flip` is incremented **only inside the REPOSITION limb**
(`spatial_engine.py:5553-5555`). On any tick the player advances, holds, or is claimed by M-3, the
clock **freezes**. So `ORBIT_FLIP_PERIOD_S = 4.0 s` and `ORBIT_FLIP_DEBOUNCE_S = 0.8 s` measure
*4.0 s of repositioning* and *0.8 s of repositioning*, not 4.0 s and 0.8 s **elapsed** — which is
the word spec §C-2 rule 2 uses.

- **Blast radius, measured:** 5,118 of 133,854 armed decision ticks are non-reposition
  (advance 4,989 + hold 129) = **3.8 %**. Fully deterministic either way; **no gate moves**, and
  S-4 is untouched because this is state, not a draw.
- **Why it is a WARN and not an INFO:** §E makes both periods **TUNABLE**, so the S-3 lap is
  licensed to move exactly these two numbers — and a lap that moves a period does so believing it
  is moving seconds. Discipline #12 requires the shift be *named*; math note §3.2 and §8 both
  describe the flip as a pure function of `ticks_since_flip` without ever saying what increments it,
  and the cell note does not name it either.
- **It is also unpinned.** All flip tests pass `ticks_since_flip` in as a parameter to the pure
  helper (`tests/test_wr2_c_movement_policy.py:278-334`); **no test pins the engine's clock source.**
  That is the same declaration-vs-transcription gap that produced Cell B's HALT — here with a
  trivial consequence rather than a gate-breaking one, but the same shape, and the cell pinned the
  *predicate* against the seam by grid-equivalence while leaving the *clock* untested.
- **Action:** name it in the math note (one sentence, §3.2 or §8) and pin it with one engine-level
  test. Or make it a sim-tick clock, which is what "elapsed" reads as. Either is fine; **leaving it
  unnamed with the periods marked TUNABLE is the part I object to.**

### WARN-2 — the AoE whiff-window clearance is quoted to the WRONG EDGE: 0.80 m in the notes, 0.30 m in the test.

Cell note §3 and §8 state that `band_outer` = 2.70 m "sits **0.80 m clear** of the `aoe_radius` 3.0 /
selection 3.5 whiff window." The window is `d ∈ (3.0, 3.5]` — SS-B-1 lets a circle AoE be
**selected** out to 3.5 while `_compute_circle_hits` still measures `aoe_radius` = 3.0
centre-to-centre. The **binding edge is 3.0**, so the clearance is `3.0 − 2.70 = ` **0.30 m**.
0.80 m is the distance to the window's *far* edge, which nothing has to cross to get in.

The **test is correct and asserts the right number** —
`test_band_outer_stays_clear_of_the_circle_AoE_whiff_window` asserts
`smallest_circle_aoe - outer == approx(0.30)` and its docstring names the window as `[3.0, 3.5)`. So
the guard is real; only the narrative is loose. But the narrative is what a tuning lap reads, and it
overstates available `BAND_WIDTH` headroom by **2.7×**: +0.30 m walks into the window, not +0.80 m.

Mitigating, and it should be stated because it makes this cheap: **this kit carries no circle skill
at all** (`feral_claws_r16` cone / `rip_and_tear_r16` line, per the trace headers), so the window is
unreachable on this battery regardless. The test's own docstring says so. **Action:** correct the
number to 0.30 m in cell note §3/§8. No re-run, no code change.

### WARN-3 — MIGRATION §5 calls a path-tortuosity metric "cumulative absolute heading change", and the schema has a field named `heading_rad` that behaves differently.

`MIGRATION.md` §5 tells drax that "the cumulative absolute **heading change** goes from 3.84 rad to
150.80 rad." The reported quantity is `total_abs_turn_rad` — the accumulated turn of the **movement
bearing**, derived from `x_m`/`y_m`. It is **not** the `heading_rad` field, and C-5's whole point is
that `heading_rad` does something else: it stays on the nav target.

Measured, so the gap is sized rather than asserted — cumulative `|Δ heading_rad|` on the same trace:

| arm | `total_abs_turn_rad` (reported) | actual cumulative `|Δ heading_rad|` |
|---|---|---|
| WR1 | 3.84 | **4.9651** |
| Cell B | 4.07 | **1.7081** |
| Cell C | 150.80 | **129.1411** |

Same order and the same conclusion, but they are different numbers from different fields, and Cell B
moves them in **opposite directions**. This is precisely the field-name discipline the cell itself
applied correctly to `n_nova_crossings` two sections later in the same document (§7, "stated by FIELD
NAME, because the two quantities below are different things"). It was not applied here. Charter
§8.18 inherits the same phrasing. **Action:** restate MIGRATION §5 by field name
(`total_abs_turn_rad`, path-derived, not `heading_rad`). Consumer-facing, so worth the sentence.

### WARN-4 — SS-C-3 is a real precedence change to a *previously ADVANCE* interval, and the spec text it departs from is §C-0.

The cell implemented §C-1's radial rule (`REPOSITION iff d ≤ band_outer`) rather than §C-0's prose
("REPOSITION where it would today return HOLD"). Post-R-WR2-17 these are **different sets**:
`band_outer` = 2.70 > `min_attack_range` = 2.00, so `d ∈ (2.00, 2.70]` was ADVANCE and is now
REPOSITION.

**I judge the fork correctly resolved.** The arithmetic decides it: under §C-0's literal reading the
player must be inside 2.00 m to reposition, which post-B is unreachable — the band would be measure
zero and C would remain the no-op it exists to fill. §C-1 is the operative text. And the cell named
it (SS-C-3), measured its exact consequence (`advance` −51, entirely `mixed_pack`; boss/champion/trash
invariant at their Cell-A banked values — **I reproduced all of this exactly**), and routed it up.

The WARN is narrower: **this is a departure from a sentence in the frozen spec, resolved by the
builder.** Spec §E freezes "flip trigger set" and the precedence *order*, but it does not
adjudicate which of §C-0 / §C-1 defines the REPOSITION *region* — and the two disagree by 0.70 m of
standoff, which is where the player now spends ~97 % of the fight. That is a conductor's ruling, not
a builder's, even when the builder's reading is the only one that works. **Action for gandalf:**
ratify §C-1 as the operative text with a short R-WR2-n entry (or errata §C-0), so the operative
definition of the REPOSITION region is in the ruling ledger rather than only in a cell note. Nothing
re-runs; the arithmetic is not in dispute.

### WARN-5 — a residual HOLD annulus survives against standard-radius targets. The no-op filling is ASYMMETRIC, and nobody named it.

This one I found by asking why an *armed* policy emits `hold` at all. It emits 129 of them, and
every single one is the legacy no-op still standing.

The two predicates do not tile the line. REPOSITION owns `d ≤ band_outer`; ADVANCE owns
`d > min_attack_range`. Whether there is a gap depends on the sign of
`min_attack_range − band_outer`, and **that sign flips with the target's radius**:

| target | `band_outer` | `min_attack_range` | unowned annulus | consequence |
|---|---|---|---|---|
| boss (r 1.5) | **2.70** | 2.00 | **none** — the two overlap by 0.70 m | C fully fills the no-op; SS-C-3 |
| standard mob (r 0.5) | **1.70** | 2.00 | **`d ∈ (1.70, 2.00]`, 0.30 m wide** | **legacy HOLD survives** |

**Measured, and it is exactly this:** all **129** `hold` decision ticks in the armed battery fall on
targets of radius **0.5** at `d ∈ [1.7311, 1.9102]` — **129 / 129 inside the predicted annulus**, on
`trash` (90) and `mixed_pack` (39). Not one is a root, a hard-CC or a death: the player is alive with
no ailments on every one of them. So this is not the E4/F8 chain working, it is the band arithmetic
leaving a hole.

**Impact on this landing: none, and I want to be precise about that.** 129 of 133,854 armed ticks =
**0.096 %**. S-2 is 0.000 % on both affected tiers, every trash and mixed_pack fight is won 30/30 on
every leg, and the player is well inside its 2.50 m effective reach at 1.9 m so it is attacking
throughout. No gate moves. **This is not a defect I am asking to be repaired.**

**Why it is still a WARN.** It is the *other half* of WARN-4, and it is the half nobody measured.
The cell named the §C-0 / §C-1 fork and measured the direction where REPOSITION **took** territory
from ADVANCE (`advance` −51, SS-C-3). It did not name the direction where **HOLD kept** territory
§C-0's prose would have eliminated — and §C-0's prose is precisely "REPOSITION where it would today
return HOLD," which is the clause this annulus violates. Three further reasons it belongs in the
ledger rather than in a footnote:

1. **It scales with a TUNABLE.** The annulus width is
   `min_attack_range − (r_contact + BAND_PAD_INNER + BAND_WIDTH)`. `BAND_WIDTH` is a §E **YES** row,
   so a lap that *reduces* it widens the hole; raising it to ≥ 0.90 m closes it for standard mobs.
   A lap tuning "feel" would move this without knowing it exists.
2. **It generalizes to any small target.** The hole opens whenever the target is small relative to
   the kit's minimum reach. This battery has exactly two radii; a scenario with 0.9 m elites would
   sit somewhere new on this curve.
3. **The grid-equivalence test cannot catch it.** `test_engine_inline_predicate_matches_the_seam_on_a_grid`
   pins the engine and the seam to *agree* — and they agree perfectly, including on leaving the gap.
   Agreement is not coverage. Nothing asserts the intents tile the domain.

**Action:** name it in the math note beside SS-C-3 (they are one fact seen from two sides), and add
one assertion that the three intents tile `d` for a given band — or, if gandalf rules §C-0's
coverage intent binding under WARN-4, close the annulus by letting REPOSITION own
`d ≤ max(band_outer, min_attack_range)`. **My recommendation is name-and-pin, not repair:** the
measured impact is 0.096 % and changing the region would move outcomes on tiers that currently pass
everything.

---

## 8. INFO (6) — ledgered, no action required

- **INFO-1 — the trajectory estimator's stall convention is undocumented.** §4.2 †. The driver drops
  the turn on *both* sides of a stall step; a bearing-linked estimator returns 7.43 rather than 3.84
  for the WR1 baseline. Both are defensible, the convention is applied uniformly across all three
  arms, and no verdict moves. Worth one line in the `trajectory()` docstring so a future grader
  re-deriving with the other convention does not read a contradiction.
- **INFO-2 — cell note §2's "per leg" figures are ALL-TIER, in a paragraph that is otherwise
  boss-tier.** The quoted pre 0.829 / post 0.897 / pre_endpoint 0.488 % reproduce exactly as
  all-tier per-leg shares (my values 0.8289 / 0.8965 / 0.4878). Boss-only per-leg is
  **1.105 / 1.169 / 0.682 %** — all still inside the 5 % gate. Correct numbers, ambiguous label.
- **INFO-3 — leg ordering in the `mixed_pack` advance triple.** The note writes
  "(210 → 191 / 197 / 191)". I measure pre 191, pre_endpoint 191, **post 197**. Multiset and the −51
  delta are exact; only the positional order differs.
- **INFO-4 — `azimuth_reversals` needs the deadband to be stated.** The driver's `abs(d) > 1e-9`
  deadband is load-bearing for this metric: without it I get 9 / 23 / 22 instead of 1 / 3 / 21. With
  it I reproduce 1 / 3 / 21 exactly. Unlike the S-2 epsilon (§4.1) this one *is* sensitive, so it
  belongs in the docstring beside the number.
- **INFO-5 — Cell BAT's flag-OFF byte-identity baseline must pin at `ecea69f`, not `4f09e35`.**
  `report["wave_regime"]["movement_policy_v2_wr2_c"]` is emitted **unconditionally**, so a flag-OFF
  report now carries one more key. Same class as Cell B's INFO-1 and gamora self-reported it
  (MIGRATION §1, cell note §6). **CONFIRMED and ADOPTED** — flagging this for the conductor's Cell
  BAT brief. Trace content and behaviour are unaffected; only the report artifact.
- **INFO-6 — F-WR2-3 (nova dark) observations, not duplicated.** I verified the *numbers* only,
  because the mechanism has its own parallel diagnostic cell. For that cell's record: the effect is
  present at `4f09e35` with B alone (`n_nova_crossings` 44 → 0 on all three legs; `circle` telegraph
  1 → 0 on `boss__B__seed74000802`, the WR1 ring being minted at tick 8 with `attack_id`
  `boss&quest_slith_wightmirecave01_0:nova:1` and `fire_tick` 15), and it is **0 under B-only and 0
  under B+C**, so **C is not the cause** — the cell's disposition is right. `worst_non_nova_event_hp`
  is essentially unchanged across the three arms (51.590 → 51.596 → 51.590), which is consistent
  with the nova being the only thing removed. No further comment; that investigation is not mine.

---

## 9. Action

- [x] **jack-ryan:** verdict CLEAR-with-notes; Cell BAT releases on this gate.
- [x] **jack-ryan (ADR-002 direct approval):** WARN-3 riding obligation (b) confirmed
      documentation-only; the 43 new tests + 1 amended test approved as test additions.
- [ ] **gamora:** WARN-1 — name the reposition-tick flip clock in the math note, and pin it with one
      engine-level test (or convert it to a sim-tick clock). No re-run.
- [ ] **gamora:** WARN-2 — correct the AoE whiff-window clearance from 0.80 m to **0.30 m** in cell
      note §3/§8. The test is already right.
- [ ] **gamora:** WARN-3 — restate MIGRATION §5 by field name (`total_abs_turn_rad`, path-derived,
      **not** `heading_rad`). Consumer-facing; drax reads this.
- [ ] **gamora:** WARN-5 — name the residual HOLD annulus in the math note beside SS-C-3 (one fact,
      two sides), and pin that the three intents tile `d`. **Name-and-pin, not repair.**
- [ ] **gamora:** INFO-1 / INFO-4 — one docstring line each in `trajectory()` for the stall
      convention and the reversal deadband.
- [ ] **gandalf (RUN-CONDUCTOR):** WARN-4 + WARN-5 together — ratify spec §C-1 as the operative
      definition of the REPOSITION region (errata §C-0, or a new R-WR2-n), and rule whether §C-0's
      *coverage* intent ("REPOSITION where it would today return HOLD") binds. The fork has
      consequences in **both** directions: REPOSITION took `(2.00, 2.70]` from ADVANCE against the
      boss (SS-C-3, measured), and HOLD kept `(1.70, 2.00]` against standard mobs (WARN-5, measured).
      The builder's reading is the only workable one; both halves belong in the ruling ledger, not
      only in a cell note.
- [ ] **gandalf:** INFO-5 — carry the flag-OFF byte-identity baseline pin (`ecea69f`) into Cell BAT's
      brief.
- [ ] **Matt:** nothing. No BLOCK, no escalation, no commitment-boundary reached. The S-3 tuning lap
      remains **UNSPENT** and every §E parameter still sits at its spec default.

---

## 10. References

**Reviewed:**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/reposition.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/seam.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wr2_cell_c_move_2026_07_29.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wr2-c-movement-policy-2026-07-29.md`
- `~/Games/reincarnated-engine/tests/test_wr2_c_movement_policy.py`
- `~/Games/reincarnated-engine/tests/test_wr1_m12b_m3_realized_count_telegraph_response.py`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr2-cell-c-movement.md`

**Evidence:**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_cell_c/` (450 traces + 3 leg reports, uncommitted; `wr2_cell_c_statistics.json` + `wr2_cell_c_s4.json` committed)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/`, `wr1_battery_2_aim/`, `wr2_cell_b_s1/`, `wr2_cell_b_s1_r2/` (SS-1 frozen; read-only)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt` (81-name baseline)

**Governing:**
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` §2, §3, §7, §8.13–8.20
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-29-wr2-mechanism-spec.md` §C, §D, §E, §G
- Prior gates: `qa/findings/2026-07-29-gate2-gamora-wr2-cell-a.md`, `...-cell-b.md`

**Scratch (not banked):** `/tmp/jr_c_s2.py`, `/tmp/jr_c_s1.py`, `/tmp/jr_c_traj.py`,
`/tmp/jr_c_heading.py`, `/tmp/jr_wr2_cellc_regression.txt`

---

*Gate 2 closes. — jack-ryan*
