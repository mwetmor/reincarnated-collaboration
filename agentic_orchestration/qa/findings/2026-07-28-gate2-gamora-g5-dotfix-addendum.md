# Finding (ADDENDUM) — 2026-07-28 — G-5 DoT-vocabulary repair (KIT-CAL-1 / KC1-2026-07-27)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2 re-review)
**Severity:** **BLOCK LIFTED** on `g5_r3arm/` · **WARN** (new, tick-rate) · **INFO** ×2
**Target:** engine `9f6805a` (fix) + `7483a21` (re-run), tag `gamora/v-g5-dotfix-1`
**Developer:** gamora (simulation seam)
**Supersedes:** the ESCALATE and the first BLOCK bullet of `2026-07-28-gate2-gamora-g5-s1control.md` §4
**Principles applied:** #1 math-before-code · #2 smoke-gate · #3 cross-seam impact · #5 severity
**Disciplines cited:** #1, #8 (schema validation at boundaries), #10 (empirical inspection over assumption), #12 (semantic-shift naming)
**Verification stance:** every claim below re-derived independently. Where gamora's method and mine differ, mine is stated and the difference is named.

---

## §0 — CORRECTION TO MY OWN §1.4 (filed, not buried)

**My named root cause was WRONG. My observation was right.**

Prior finding §1.4 stated: *"The kernel writes the DoT into the defender's scratch `CombatantState.active_effects`; that scratch is discarded."* That mechanism is **falsified**.

I reproduced the falsifier by my own construction — a minimal 2-effect kit pushed 30× through `resolve_spatial_hit`, reading object identity and the `active_effects` list identity on the way out:

```
NEW 'poison': obj-identity=True list-identity=True n_effects=8  ['poison']
OLD 'dot'   : obj-identity=True list-identity=True n_effects=0  []
NEW 'bleed' : obj-identity=True list-identity=True n_effects=1  ['bleed']
```

The seam carries DoT. `defender_state=target.combatant_state` (`spatial_engine.py:2556`) is a plain attribute read — Python passes the reference, and `_tick_effects(e.combatant_state, ...)` at `:5299` reads the same object. Only **HP** is scratch (`defender_live_hp` re-sync); `active_effects` never was.

**Where I went wrong, named so the error class is legible:** I read `resolve_spatial_hit`'s docstring — which enumerates discarded kernel side effects (`heal`, `lifesteal`, `heal_over_time`, `reflect`) and does *not* name DoT — and treated the omission as the defect. Every effect in that list is **attacker-side**. Defender-side ailments were never in scope of that sentence. I inferred a mechanism from a docstring gap instead of measuring it, which is precisely the failure Discipline #10 exists to prevent. The BLOCK was still correct: the observation (zero DoT events across 300 fights) was measured and reproduced, and the artifact was a null instrument either way. But **the mechanism in §1.4 must not be cited.**

**The real site verified by my own read**, not by accepting hers. `resolve_skill`'s effect loop (`damage_resolver.py:832`) dispatches on:

| kind | count | names |
|---|---|---|
| literals | 10 | `damage`, `heal`, `shield`, `heal_over_time`, `buff_damage`, `buff_defense`, `buff_dodge`, `buff_mana_regen`, `silence`, `lifesteal` |
| registry | 16 | `AILMENT_NAMES` (loaded, counted at runtime: 16) |

**= 26, and the loop terminates at `:1263` with `return total_damage, events`. There is no `else`.** `"dot" in AILMENT_NAMES` → `False`. The riders fell through every `elif` and were silently discarded.

**Root-cause correction: ACCEPTED.**

---

## §1 — BLAST-RADIUS CENSUS (Matt's historical-scope ruling hangs on this)

I did not sample her method. I ran a **broader** census, by two independent routes.

**Route 1 — data corpus.** Recursive walk of every `.json` under `output/`, `seasons/`, `src/reincarnated/simulation/output/` (excluding the `kitcal_g5*` fixture batteries), collecting every dict in any `effects` list carrying a `name`, tested against the live `AILMENT_NAMES | {10 literals}` set read from the module:

```
JSON scanned: 5110  |  files w/ effects: 2850
TOTAL effect instances: 19642  |  distinct names: 18
UNHANDLED instances: 0
```

This is **5.7× the base gamora reported** (19,642 across 2,850 files vs. her 3,462 across 632). Same verdict. All 18 distinct names — `damage` 8164, `knockback` 1489, `shield` 1476, `chill` 1402, `buff_damage` 1307, `burn` 894, `root` 878, `buff_dodge` 747, `buff_defense` 581, `lifesteal` 563, `heal` 500, `silence` 465, `buff_mana_regen` 315, `heal_over_time` 278, `bleed` 275, `shock` 150, `drain` 81, `consecrate` 77 — are dispatched.

**Route 2 — source tree, AST.** Parsed every `.py` under `src/`, `tests/`, `scripts/`, extracting every dict literal carrying both `"name"` and `"params"` keys:

```
{damage:37, lifesteal:5, burn:4, bleed:1, poison:1, heal:1, heal_over_time:1,
 shield:1, buff_damage:1, freeze:1, dot:1}
UNHANDLED: [('tests/test_kitcal_g5_dot_wake.py', 97, 'dot')]
```

The **only** surviving unhandled literal in the entire tree is the deliberate non-vacuity injection in her own DW-1b test. The three remaining `"name": "dot"` strings in `src/` are comments.

**Route 3 — history.** `git log -S '"name": "dot"' --all` returns exactly two commits: `bef1f55` (introduced, today) and `9f6805a` (removed, today). Zero prior batteries.

**Census verdict: VERIFIED, on a broader base than gamora's. My escalation's scope claim — "voids `dot` on every kit the spatial engine has ever run" — is FALSIFIED.** The voided class is 2 sites, both in `kitcal_g5_scenarios.py`, both authored today. Production is clean at 19,642 instances. **Matt's reserved historical-scope ruling can be answered: there is no historical scope.** The escalation in my prior §4 is **withdrawn as a repair item** and survives only as the residual-hazard item at §3.

---

## §2 — FIX SHAPE AND NO-STACK

**Writer census (my own grep, not her test).** All `active_effects` mutation sites in `src/`:

| site | function | side |
|---|---|---|
| `damage_resolver.py:1794` | `_add_poison_stack` | defender — reached only from `_try_apply_ailment` |
| `damage_resolver.py:1857` | `_add_or_refresh` | defender — reached only from `_try_apply_ailment` |
| `damage_resolver.py:1210/1222/1231` | `resolve_skill` | **attacker** (HoT, buffs) |
| `spatial_engine.py:3118/3195/3199/4077` | aura statmod riders | **player** |
| `effect_resolver.py:167` | cull comprehension | reader/cull |

**Ticker census.** `tick_effects` has exactly **one** call site in the tree: `spatial_engine.py:5299`, once per tick per entity.

**One writer, one ticker on the mob-defender DoT path. Confirmed.** `spatial_resolver_adapter.py` is untouched by `9f6805a` — no carry-back was added. Her refusal to "carry the DoT back" is the correct call and avoids re-creating the O-d second-writer hazard.

**Her pins are non-vacuous — proved by accident.** When I injected `tick_damage = 0.0` for a magnitude sweep, `A-DOT-2` raised and refused the run. That pin does real work.

**Adversarial look, two INFO-level notes:**

- **INFO-1.** `apply_chance=1.0` is *not unconditionally* deterministic: `did_apply_ailment(chance, resist, roll) = roll < chance*(1-resist)` (`foundation/math_model.py:155`). It is deterministic here only because `combatant_projection_from_monster_dict` returns `status_resist = 0.0` (verified). Correct behavior; the math note should say "deterministic against a zero-resist defender," not "deterministic."
- **INFO-2.** The `apply_chance` byte-neutrality argument holds on my read: `rng.random()` is evaluated as a *call argument*, so the draw is consumed on both legs and the downstream stream cannot desync.

Tests: `tests/test_kitcal_g5_dot_wake.py` + `test_kitcal_g5_harness.py` = **39 passed, 0.37 s**. Smoke `--smoke --no-trace` green.

**Fix shape: APPROVED under ADR-002** (within-seam fixture correction + a door in the already-ratified BQ-3/O-d shape; tests added; no consumer API change).

---

## §3 — RESIDUAL HAZARD: the no-`else` silent fall-through

**Descriptive.** The defect *class* is unrepaired. `resolve_skill`'s effect loop still terminates without an `else`. Any hand-authored effect dict carrying a name outside the 26 is still dropped in silence, producing numbers, passing asserts, and reporting a null as a measurement. That is exactly what happened, and it cost a full three-battery regen.

**Prescriptive.** Discipline #8 (schema validation at boundaries) applies squarely. My disposition:

- **Not a BLOCK on this artifact.** The census (§1) shows zero live exposure. Blocking a clean repair on a latent class is the wrong severity.
- **WAVE-ROUTE it, do not condition it.** An `else: raise` at `damage_resolver.py:~1263` is a kernel-level behavior change touching every caller in the tree — it is not gamora's to land unilaterally mid-run, and landing it during an active calibration run violates the same "one change at a time" logic that governs Discipline #3.
- **Recommended shape** (for the wave that takes it): a module-level `_HANDLED_EFFECT_NAMES` frozenset built from `AILMENT_NAMES` plus the literals, with a *strict* `else: raise ValueError` behind a validation flag defaulted ON in tests/fixtures and a `warnings.warn` in production emission paths. The set must be **derived**, never transcribed — gamora already applied that rule to her A-DOT pins (`from ... import AILMENT_NAMES`) and it is the right one.
- **ESCALATE to Matt** as a scoped, non-urgent item: cross-seam (rocket owns generation-side effect emission, gamora owns the kernel dispatch), zero current exposure, real recurrence risk.

---

## §4 — THE SECOND NULL INSTRUMENT (S-2)

**Her claim is VERIFIED, and it is stronger than she stated.**

**The identity is algebraic, not empirical.** `compute_abc` (`kitcal_g5_harness.py:201-238`) reads `kill_times_s` and nothing else, and returns `A = kills/kill_events`, `B = kill_events/bursts`, `C = bursts/1`. The product telescopes: `A·B·C ≡ kills ≡ kills/encounter`, identically, for every input. Empirical confirmation across all 450 post-fix fights: **0 identity violations.**

**kills/encounter is pinned by battery design.** Measured per (arm, tier): trash 8, champion 4, mixed_pack 6, boss 3 — a single value in every cell, with the sole exception of S-1 control boss `{2,3}` (its 4 losses). **Therefore B is a residual of A and C against a constant, not a free measurement.**

**I ran the adversarial test she did not: a DoT-magnitude sweep across six orders of magnitude on the R3 arm (6 seeds/tier).**

| `tick_damage` × | trash B | champ B | mixed B | boss B | **boss elapsed** |
|---|---|---|---|---|---|
| 0.001 | 1.0000 | 1.0000 | 1.2222 | 1.0000 | 28.38 |
| 1.0 (shipped) | 1.0000 | 1.0000 | 1.3333 | 1.0000 | 26.47 |
| 10 | 1.0000 | 1.0000 | **1.0000** | 1.0000 | 17.47 |
| 100 | 1.0000 | 1.0000 | 1.3333 | 1.0000 | 8.30 |
| 1000 | 1.0000 | 1.0000 | 1.3333 | 1.0000 | **6.80** |

`kills` invariant at 8/4/6/3 throughout. **B is flat at 1.0000 on three of four tiers across a 10⁶ lever swing — including a magnitude that cuts boss kill-time by 4.2×. On the fourth tier B moves *non-monotonically and against* the lever** (drops at 10×, where C rises to 4.0, product invariant at 6). B is binning noise.

**Instrument defect, stated precisely — and it is worse than "B returns 1.000."** Kit-spec §6.2's S-2 predicate is *"DoT-tail lift confined to B."* Because `A·B·C ≡ kills` and `kills` is fixed, **"confined to B" is structurally impossible**: any B movement mathematically forces a compensating A or C movement. The predicate is not merely unmeasurable on this fixture — it is **unsatisfiable by construction** in any battery where every mob dies every fight. A DoT tail changes *when* things die, not *how many*.

**Recommendation to the amendment lap (gandalf/Matt make the grading call, not me).** Two instruments in the banked post-fix data already read the lever and carry real per-seed variance:

| candidate | W-c | R3 | lift | per-seed sd |
|---|---|---|---|---|
| **boss elapsed_s** | 28.45 | 26.48 | **0.9309** (−6.9 %) | 0.71 / 0.63 |
| **player DoT damage share** | 0.732 % | 4.062 % | **5.55×** | — |

Boss elapsed is monotone in DoT magnitude across the whole sweep above. Trash/champion/mixed read ≈1.000 not because the instrument fails but because those tiers die inside the same cast — which is the correct physical answer and is itself citable. My recommendation: **re-express S-2 as a kill-time-delta band on the boss tier plus a DoT-damage-share floor, and retire B as an S-2 read entirely.** Note the same identity retires B as an *independent* read for **any** target on this fixture, not just S-2 — that is worth carrying to the amendment.

---

## §5 — BOSS-LOSS DISCLOSURE (verified)

Re-derived from the post-fix reports:

| tier | W-c | R3 | S-1 control | elapsed W-c / R3 / S-1 |
|---|---|---|---|---|
| trash | 30/30 | 30/30 | 30/30 | 4.23 / 4.23 / 4.77 |
| champion | 30/30 | 30/30 | 30/30 | 4.41 / 4.41 / 4.73 |
| mixed_pack | 30/30 | 30/30 | 30/30 | 10.26 / 10.26 / 11.57 |
| **boss** | **60/60** | **60/60** | **56/60** | 28.45 / 26.48 / 30.26 |

Control boss deaths 10 → 4 (pre → post). **Narrowed, not closed — exactly as disclosed.** The elapsed-time divergence at every tier also persists. My prior §4 condition stands unchanged: **the S-1 boss PASS may be cited only alongside the 56/60 and the elapsed divergence.** Disclosure obligation: MET.

**DoT-wake numbers independently re-derived from the traces** (ticks carry `event:"damage"`, `geometry:"dot"`, `skill_idx:-1`):

| battery | pre-fix ticks | post-fix ticks | post-fix damage | magnitudes |
|---|---|---|---|---|
| canonical W-c | 0 | 60 | 11,178.0 | `{186.3: 60}` |
| S-1 control | 0 | 180 | 33,534.0 | `{186.3: 180}` |
| R3 arm | 0 | 3,150 | 61,893.0 | `{20.7: 2070, 6.9: 900, 13.8: 120, 186.3: 60}` |

Every figure matches her landing exactly. Magnitudes quantize cleanly. **The lever is awake.**

---

## §6 — TICK-RATE: the 90 % claim does NOT verify. The defect is real and WORSE.

This is the one place my measurement materially contradicts hers, and it changes what should go to Matt.

**(a) The cited float fact is wrong as written.** `sum([0.1]*10)` evaluates to **exactly `1.0`** (Python's `sum` seeds with `int 0`, a different rounding path). The accumulator's actual behavior — repeated `x += 0.1` from `0.0` — gives `0.9999999999999999`. Same conclusion, wrong citation; it appears verbatim in the commit message, the math note §6 R-5, and the `DW-5` docstring.

**(b) The 90 % figure is an artifact of her probe's shape.** `tick_effects` steps **two** float accumulators at the same rate: `duration_remaining -= tick_size` (cull on `> 0` failing) and `tick_accumulated += tick_size` (fire on `>= 1.0`). They drift **identically**, so whether the final tick lands is a *race* between the two, not a fixed 10 % loss.

| harness | ts 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|
| **fixed 10.0 s wall clock** (her `DW-5`; effect pinned at `duration_remaining=1000.0`) | 900.0 (**90 %**) | 1000.0 | 1000.0 | 1000.0 |
| **cull-driven** (what a fight actually runs; `duration_remaining=10.0`) | **1000.0 (100 %)** — 101 sub-ticks | 1000.0 | 1000.0 | 1000.0 |

The drift bought a 101st sub-tick and the 10th DoT tick landed. **"Every DoT the engine has ever ticked at full fidelity delivered 90 % of declared" does not hold on the engine's own path.**

**(c) At the durations the G-5 kit actually ships, the loss is far larger.** Cull-driven, `TICK_SIZE = 0.1`:

| rider | declared | delivered | |
|---|---|---|---|
| charge **bleed 270 × 3.0 s** | 810.0 | **540.0** | **66.7 %** |
| claws **poison 10 × 5.0 s** | 50.0 | 50.0 | 100 % |

**Confirmed in the shipped artifact, not just in a probe.** Grouping the 180 `186.3` bleed ticks in `kitcal_g5_fix/g5_s1control/` by target and application gap:

```
bleed applications by ticks delivered (declared 3): {2: 90}
delivered/declared = 180/270 = 66.7%     (90/90 applications, zero exceptions)
```

**Corrected characterization for Matt.** Not "a uniform 10 % shortfall." It is: *at `TICK_SIZE = 0.1` the final DoT tick is kept or lost by a float-drift race between two independently-accumulating counters; measured shortfall is duration-dependent and non-monotonic — 0 % at 5.0 s, **33 % at 3.0 s**, 0 % at 10.0 s cull-driven, 10 % at 10.0 s under a fixed-clock harness.* Short DoTs — the common case for ARPG riders — are hit hardest, which inverts the risk assessment "90 %" implies.

**Consequence for this artifact, and it is not a BLOCK:** the post-fix G-5 bleed is delivering 2/3 of declared in all three batteries. The wake is real and the S-2 conclusion (§4) is magnitude-independent, so nothing here reverses. But **the post-fix absolute bleed numbers are ~33 % light** and the amendment must not read them as calibrated. `effect_resolver.py` is untouched by `9f6805a` — **pre-existing and production-wide is confirmed.**

**Tick-rate 90 %: NOT VERIFIED. Underlying defect: VERIFIED and larger than reported.** WARN.

---

## §7 — Action

### BLOCK — LIFTED

- [x] **`g5_r3arm/` quarantine — RELEASED for the post-fix artifact only.** `output/kitcal_g5_fix/g5_r3arm/` is readable. The **pre-fix** `output/kitcal_g5/g5_r3arm/` remains quarantined permanently as evidence and must never be pooled with post-fix output (SS-1). The S-2 restriction is **replaced, not lifted** — see the WARN below.

### WARN — must be carried into the amendment lap

- [ ] **gandalf / amendment lap:** S-2 cannot be graded from **B** on any designed-composition battery. Not "the arm missed" and not "B returned 1.000" — the predicate *"DoT-tail lift confined to B"* is **unsatisfiable by construction** while `A·B·C ≡ kills` and `kills` is fixed. Re-express against boss kill-time delta (0.9309, sd 0.63–0.71) and/or DoT damage share (0.732 % → 4.062 %). Ruling is gandalf's + Matt's; the instrument analysis is mine.
- [ ] **gamora:** correct the tick-rate finding per §6 before it reaches Matt — fix the `sum([0.1]*10)` citation, and restate 90 % as the duration-dependent race it is. `DW-5`'s assertion is *correct for its harness*; its **docstring generalization is not**. The shipped bleed loses 33 %, not 10 %.
- [ ] **gamora:** name in the math note that the post-fix bleed numbers carry the §6 shortfall, so the amendment does not read them as calibrated.
- [ ] **gamora:** §3.3 — `apply_chance=1.0` is deterministic *against a zero-resist defender* (INFO-1). One clause.

### ESCALATE to Matt

- [ ] **Historical scope (RESOLVED — decision now trivial).** My prior escalation's premise is falsified. Voided class = 2 sites, both authored today at `bef1f55`; production clean at **19,642** effect instances (my census, 5.7× hers); `git log -S` bounds the spelling to today. **No historical G-5 or production battery is affected. No re-run of prior work is owed.**
- [ ] **No-`else` hazard (§3) — wave-route, do not condition.** Kernel-level, cross-seam (rocket + gamora), zero live exposure, real recurrence risk. Discipline #8. Recommended shape in §3.
- [ ] **Tick-rate shortfall — route as its own item** with the §6 correction, not the 90 % framing. Pre-existing, production-wide, and it silently under-delivers every short DoT in the engine.

### APPROVED under my ADR-002 authority

- The **fixture re-spell** (`dot` → `bleed`/`poison`, `tick_damage = magnitude/duration`) — within-seam, no consumer API change, 16 tests added, pins non-vacuous by my own accidental injection.
- The **`apply_chance` door** — byte-neutral on both legs, verified structurally and by regression.
- The **`--r3-arm` output labelling fix** — closes my prior §1.8 WARN.
- The **DoT-wake evidence** — every tick count and magnitude re-derived from the traces and matched exactly.

### Decisions-log

- [ ] I will file **"Spatial-engine effect dispatch has no unknown-name guard (KIT-CAL-1 G-5)"** once Matt rules on §3. The earlier candidate title — *"Spatial-engine DoT effects are inert at the projection seam"* — is **withdrawn: its premise is false.**

---

## §8 — References

**Engine (`/Users/admin/Games/reincarnated-engine/`):**
- `src/reincarnated/simulation/damage_resolver.py:832-1263` — the 26-name effect loop with no `else`
- `src/reincarnated/simulation/damage_resolver.py:1678-1700` — `_try_apply_ailment`, the `apply_chance` door
- `src/reincarnated/simulation/damage_resolver.py:1794 / 1857` — the two defender-side writers
- `src/reincarnated/simulation/effect_resolver.py:55-131` — `tick_effects`, the dual-accumulator race (§6)
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:2556` — `defender_state=target.combatant_state`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:5299` — the single ticker
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py:201-238` — `compute_abc`, the telescoping identity
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py:184-240` — the repaired riders
- `src/reincarnated/simulation/math/dot-projection-discard-2026-07-28.md` — the math note under review
- `tests/test_kitcal_g5_dot_wake.py` — 16 new tests; `DW-5` docstring flagged at §6
- `src/reincarnated/simulation/output/kitcal_g5_fix/{g5,g5_r3arm,g5_s1control}/` — post-fix batteries, **released**
- `src/reincarnated/simulation/output/kitcal_g5/g5_r3arm/` — pre-fix, **permanently quarantined as evidence**

**Meta-repo (`/Users/admin/Games/reincarnated-collaboration/`):**
- `agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-g5-s1control.md` — the finding this amends (§1.4 corrected, §4 ESCALATE withdrawn)
- `agentic_orchestration/gandalf/notes/2026-07-28-kitcal1-g4-kit-spec-v2.md` §6.2 — the S-2 predicate requiring amendment

**Signed:** jack-ryan, 2026-07-28. §0, §1, §2, §4, §5 and §6 re-derived independently by live instrumentation or by walking the banked artifacts. §6 contradicts the developer's reported figure; the contradiction is measured, not asserted.
