# WR3-KITE-COMMIT — R-WR3-12(8.6) BOSS DUTY-CYCLE PRE-BUILD MEASUREMENT

**Date:** 2026-07-30
**Author:** gamora (simulation seam)
**Commissioned by:** gandalf (RUN-CONDUCTOR), run WR3-KITE-COMMIT, ruling R-WR3-12, spec flag §8.6
**Mode:** READ-ONLY. No engine edits. No simulation runs. Frozen traces only.
**Substrate:** `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after/` — 180 boss fights (3 legs × 2 cells × 30 seeds)
**Instrument:** `agentic_orchestration/gamora/notes/2026-07-30-wr3-dutycycle-support/wr3_duty_cycle.py`
**Data sidecar:** `agentic_orchestration/gamora/notes/2026-07-30-wr3-duty-cycle-prebuild.json`

---

## VERDICT

**CAL-C1 = 0.35 / CAL-C2 = 0.25 (T_lock 0.60 s) STAND AS GROUNDED. Hold them.** The realized boss inter-swing interval is a metronome at **median 1.500 s** (P25 = P75 = 1.500; min 1.500, max 1.600; n = 4,252 intervals), so T_lock 0.60 lands at **duty 28.6 %** (spec-literal) / **40.0 %** (cooldown-absorbing) with the boss movement-locked for a **median 34.8 % of the whole fight** — comfortably clear of both failure directions §8.6 named, and 1.55× above the §3.4 arithmetic floor exactly as the spec claimed. **Do not move to 0.40** (its usable window is *one tick*) and **do not move to 0.90** (it crosses the degeneracy line on two independent measures). Three build-time flags below (F1 tick realization, F2 strike-tick accounting, F3 the telegraph's pre-existing 0.5 s wind-up) need a conductor ruling before the build, but **none of them changes the verdict on the values.**

---

## 0 — Identity assertion of the frozen root

Asserted before a single number was read, per the wr2 cell precedent. All gates PASS; the instrument aborts on any failure and emits nothing.

| Gate | Predicate | Result |
|---|---|---|
| **I0** | leg-dir name set == the three banked WR2-AFTER legs; 150 traces each (450); 60 boss traces each (180) | **PASS** — exact |
| **I1** | SHA-256 rolled digest over the sorted `(basename, sha256)` pairs of all 180 boss traces | `b5ce25e68d4361f91070911d6c3e7e5548b424cea04972f35943a4f654345e3e` |
| **V1** | watch-seed footer: `pre` / `boss/B` / seed 74000802 → `elapsed_s == 37.0` | **PASS** — 37.000000000000256 |
| **V2** | `pre`-leg `elapsed_s` means: `boss/A == 32.04`, `boss/B == 48.92` | **PASS** — 32.043333, 48.923333 |
| **V4** | nova firings: 132 total, 44 per leg, `":nova:"` in `attack_id` | **PASS** — 44 / 44 / 44 |
| **V5** | recovered `C_drawn` inside the closed-form band `[1.411111, 1.511111]` | **PASS** — 0 / 4,432 violations |
| **V6** | swing-resolution count == `skill_cooldowns[0]` rising-edge count, per fight | **PASS** — 0 / 180 mismatched |

Per-leg boss-trace digests: `pre` `e8dc6336…`, `post` `b4a6766d…`, `pre_endpoint` `935adfc3…` (full values in the sidecar's `I1_identity_manifest`).

V3 (the S-1 separation predicate) is **not** re-run here. It is a geometry gate, not a cadence gate, and F-WR2-5 already banked it clean over these same traces — re-running it would be ceremony, not evidence.

**Completeness:** a boss-tier roster entity appears in **zero** non-`boss__` traces (`boss_entity_outside_boss_cells: []`). C2's boss-tier scope (§3.6) therefore has no leakage into the trash / champion / mixed_pack legs, and those legs are correctly excluded.

---

## 1 — What counts as a boss swing, and why the count is trustworthy

The fixture boss (`boss&quest/slith_wightmirecave01`, "Primordian, the Forgotten One") carries exactly two skills:

| idx | id | geometry | range |
|---|---|---|---|
| 0 | `slith_wightmirecave01_attack` | `point` | 2.0 m — **the basic swing** |
| 1 | `primordian_frigidring_r4` | `circle` | 10.0 m — the M-2 nova |

- **BASIC SWING RESOLUTION** := `damage` event with `source_id == boss_id` and `geometry == "point"`. `skill_idx == 0` is *asserted*, not assumed — a point-damage event with any other index aborts the run.
- **NOVA RESOLUTION** := `geometry == "circle"`. The nova resolves at an analytic ring crossing with `skill_idx == -1`, so the two are separable on **both** fields independently. **They are fully distinguishable.**

**The whiff question, settled.** In the BEFORE build there is no whiff channel. `_select_skill_for_entity` gates the melee on `nearest_dist <= range_m + target.entity_radius` (`spatial_engine:2645`, under `body_separation_v2` — the `bsep` flag is ON in every leg name), so an out-of-range boss does not select the skill and pays no cooldown; a selected point-geometry melee always produces exactly one hit. **Damage-resolution count == swing count.** This is not asserted from the code alone — V6 checks it mechanically against the rising edges of `skill_cooldowns[0]`, which is written *only* at the attack site (`spatial_engine:6293`), and gets **0 mismatches across all 180 fights**. If a swing-without-damage channel existed anywhere in the battery, V6 would have found it.

---

## 2 — Realized boss attack events per fight

**4,432 basic-swing resolutions and 132 nova resolutions across 180 boss fights. Zero fights with zero swings.**

| | n | min | P25 | median | P75 | max | mean | sd |
|---|---|---|---|---|---|---|---|---|
| swings / fight, **pooled** | 180 | 6 | 12.0 | **25.5** | 35.0 | 42 | 24.62 | 11.22 |
| swings / fight, `pre` | 60 | 10 | 12.0 | 21.0 | 30.25 | 42 | 23.17 | 10.15 |
| swings / fight, `post` | 60 | 34 | 34.0 | 35.0 | 36.0 | 36 | 34.90 | 0.79 |
| swings / fight, `pre_endpoint` | 60 | 6 | 7.75 | 12.0 | 22.0 | 37 | 15.80 | 9.42 |
| swings / fight, `boss/A` | 90 | 6 | 11.0 | 21.5 | 34.0 | 36 | 21.62 | 11.30 |
| swings / fight, `boss/B` | 90 | 9 | 20.0 | 34.0 | 35.75 | 42 | 27.62 | 10.30 |

The spread across legs is **fight-length spread, not cadence spread** — `elapsed_s` runs median 43.9 s (P25 23.6, P75 58.8, min 14.4, max 68.9), and the swing count tracks it almost exactly. The `post` leg's near-degenerate σ = 0.79 is the R3-armed leg reaching its duration ceiling in nearly every seed.

---

## 3 — Inter-swing interval distribution

### 3.1 The realized (wall-clock) interval — the headline number

n = 4,252 strike-to-strike intervals.

| | min | P25 | **median** | P75 | max | mean | sd |
|---|---|---|---|---|---|---|---|
| **pooled, all** | 1.500 | 1.500 | **1.500** | 1.500 | 1.600 | 1.5103 | 0.0304 |
| `pre` (n=1330) | 1.500 | 1.500 | 1.500 | 1.500 | 1.600 | 1.5109 | 0.0312 |
| `post` (n=2034) | 1.500 | 1.500 | 1.500 | 1.500 | 1.600 | 1.5096 | 0.0295 |
| `pre_endpoint` (n=888) | 1.500 | 1.500 | 1.500 | 1.500 | 1.600 | 1.5110 | 0.0313 |
| `boss/A` (n=1856) | 1.500 | 1.500 | 1.500 | 1.500 | 1.600 | 1.5104 | 0.0305 |
| `boss/B` (n=2396) | 1.500 | 1.500 | 1.500 | 1.500 | 1.600 | 1.5103 | 0.0304 |

**The distribution has exactly two values.** 1.5 s (3,813 — 89.675 %) and 1.6 s (439 — 10.325 %). Nothing else. Per-fight medians: **178 of 180 fights have median exactly 1.500**; the two outliers are 1.550 (an even interval count straddling the two mass points).

**Zero pursuit-gapped intervals. Zero nova-spanning intervals. All 4,252 intervals classify `clean`.** Once the swing train starts, the boss is never out of reach when its cooldown expires — F-WR2-5's *"the boss is pinned"* finding, restated at the cadence layer: **the boss's realized attack cadence is a metronome, and this fixture has no pursuit-induced cadence noise at all.**

### 3.2 The governed cadence — `cooldown_seconds + gd_swing_pause`

Spec §3.4 says C2 changes no attack cadence and that the free time "remains governed by the existing `cooldown_seconds` + the seeded `gd_swing_pause` draw." That quantity is recoverable *exactly* from the trace rather than modelled: at the swing tick the emitted `skill_cooldowns[0]` is the drawn value less one decay, so `C_drawn = skill_cooldowns[0](swing tick) + tick_size`.

n = 4,432 recovered draws:

| | min | P25 | median | P75 | max | mean | sd |
|---|---|---|---|---|---|---|---|
| `C_drawn` | 1.4112 | 1.4356 | **1.4595** | 1.4850 | 1.5110 | 1.4604 | 0.0288 |

Closed form the fixture composes: `T_base(1.0) / rate 90 % = 1.111111 s` + `U(0.30, 0.40)` = **`[1.411111, 1.511111]`, mean 1.461111**. Observed mean 1.460439 — **0.00067 s below the closed-form mean over 4,432 draws. 0 band violations.** The recovery arithmetic is correct and the M-4 cadence composer is delivering exactly what it advertises.

**Realized minus governed = 1.5103 − 1.4604 = 0.0499 s ≈ dt/2.** That is the tick grid, and nothing else: each drawn interval is rounded *up* to the next 0.1 s boundary, which adds a mean half-tick and collapses a continuous `U(1.411, 1.511)` into the two-point mass at {1.5, 1.6}. The 1.6 share should be `P(C_drawn > 1.5) = 0.11111`; observed 0.10325, z = −1.63. Consistent.

**This 0.05 s quantization tax is load-bearing for the build**: the post-C2 machine will pay it again on every phase boundary. See F1.

### 3.3 Nova, separated

**Distinguishable, and structurally irrelevant to the interval distribution.**

| | value |
|---|---|
| fights where the nova skill was selected (action gate consumed) | **180 / 180** |
| nova cast time | **t = 0.700 s in every fight** (σ = 0) |
| rings actually minted → resolutions | **132 / 180 (73.3 %)** — 48 refused by the range gate or the 80 % `Chance` gate; the refused cast still pays the 6.0 s cooldown |
| nova telegraph events emitted | 132 — equals *resolutions*, not *casts* |
| nova re-casts | **0** — the boss never selects skill 1 again |
| first basic swing | **t = 6.800 s in every fight** (σ = 0) |
| intervals spanning a nova | **0** |

The nova shares the mob action gate with the melee (`spatial_engine:5965` gate, `:6294` tail), so its 6.0 s cooldown blackholes the swing train — but **that blackhole lands entirely before the first swing** (cast 0.7 → gate opens 6.7 → first swing 6.8), which is why it never appears inside the inter-swing distribution. This is what makes the reported interval statistics clean measurements of the melee cadence and nothing else.

> **WARN-N1 (reported, not graded — outside this commission's scope, routed to the conductor).** The nova telegraph event stream counts **resolved** novas (132), not **cast** novas (180). A cast refused by the range gate or the 80 % `Chance` branch consumes the boss's entire 6.0 s action budget and emits *no telegraph record at all*. Any consumer reading nova cast frequency off the telegraph stream under-counts by 26.7 % on this fixture. The Cell-BAT S-7 "132 firings" figure is a count of **rings minted**, which is the right denominator for S-7's escapability law and the wrong one for "how often did the boss spend its action on the nova."

---

## 4 — The implied duty cycle

### 4.1 Definitions, stated precisely

The frozen traces have **no lock**: a swing resolves on the tick it fires and the mob navigation phase consults no attack state. So the *entire* measured interval is FREE (unlocked) time. Mapping that onto the post-C2 cycle requires one choice the spec does not make — **where the cooldown clock is set relative to windup entry** — so both readings are carried, named, and reported.

> **M-ADD (spec-literal; PRIMARY).** §3.4: *"C2 changes no attack cadence: the free time between swings remains governed by the existing `cooldown_seconds` + the seeded `gd_swing_pause` draw."* Free time preserved; the lock is inserted **on top** of it.
> `cycle_after = I_free + T_lock` → **`duty_ADD = T_lock / (I_free + T_lock)`** — the commission's formula, verbatim.

> **M-ABS (cooldown-absorbing; ALTERNATIVE, and the upper bound on duty).** The existing engine sets the cooldown **at** the attack site (`spatial_engine:6293-6294`). If windup entry *is* that site, the lock runs concurrently with the cooldown and the cycle does not lengthen.
> `cycle_after = max(I_free, T_lock) = I_free` (I_free ≫ T_lock throughout) → **`duty_ABS = T_lock / I_free`**.

> **L_fight — the fight-level locked fraction**, which is the number that actually answers *"what fraction of the fight is the boss movement-locked."*
> `L_fight(T_lock) = n_swings × T_lock / elapsed_s`
> This is **not** duty. Duty is measured over the attack cycle; L_fight over the whole fight. They differ by exactly the **attack-active fraction**, measured here at median **0.871** (P25 0.766, P75 0.893) — the shortfall being the opening approach (median 15.5 % of the fight) plus the one-shot 6.0 s nova blackhole.

**Named assumptions — all four are load-bearing and none is hidden:**

- **A1 — FROZEN-CADENCE.** The projection holds the measured cadence *and* the measured fight length fixed. Post-build, with K armed and C2-L1 whiffing live, both move. **This is a pre-build sanity envelope, not a prediction of the post-build state.** Direction of the error is knowable and stated in §4.4.
- **A2 — IN-RANGE-ONLY LOCK.** The boss enters windup only when the target is already in reach (§3.2 enter condition). Pursuit time is unlocked. L_fight is therefore built from *realized* swing counts, never from extrapolated cycle counts.
- **A3 — NOVA SHARES THE ACTION GATE.** Confirmed by read and by measurement (§3.3), not assumed. The spec scopes C2's packet to the boss melee skill and is silent on the nova; every statistic here is reported both pooled and nova-free, and they are identical because zero intervals span a nova.
- **A4 — TICK QUANTIZATION.** dt = 0.1 s. T_lock realizes at tick granularity: 0.40 = 4 ticks, 0.60 = 6, 0.90 = 9. The spec's §3.4 floor `T_lock ≥ 0.387` therefore realizes as `≥ 0.4`, and 0.40 clears it by **one eighth of a tick**.

### 4.2 The numbers

Anchors: `I_free` = realized median **1.500 s** (primary), and the governed `C_drawn` median **1.4595 s** (secondary, shown for sensitivity — it moves duty by < 0.7 pp).

| T_lock | ticks | floor margin vs 0.387 | daylight `5.75×(T−0.30)` | **duty_ADD** | **duty_ABS** | **L_fight** median (P25–P75) |
|---|---|---|---|---|---|---|
| **0.40** | 4 | +0.013 s | 0.575 m (min 0.5) | **0.2105** | **0.2667** | **0.2322** (0.2043–0.2381) |
| **0.60** | 6 | +0.213 s | 1.725 m | **0.2857** | **0.4000** | **0.3483** (0.3064–0.3571) |
| **0.90** | 9 | +0.513 s | 3.450 m | **0.3750** | **0.6000** | **0.5225** (0.4596–0.5357) |

On the `C_drawn` anchor: 0.40 → 0.2151 / 0.2741; 0.60 → **0.2913 / 0.4111**; 0.90 → 0.3814 / 0.6166. Per-cell L_fight medians at 0.60: `boss/A` 0.3404, `boss/B` 0.3536 — the cells agree.

### 4.3 The full pre-registered fallback bracket, on the realized median

| WINDUP × RECOVERY | T_lock | clears floor | daylight | duty_ADD | duty_ABS | L_fight mean |
|---|---|---|---|---|---|---|
| 0.25 × 0.15 | 0.40 | yes (+0.013) | 0.575 | 0.2105 | 0.2667 | 0.2219 |
| 0.25 × 0.25 | 0.50 | yes | 1.150 | 0.2500 | 0.3333 | 0.2774 |
| 0.35 × 0.15 | 0.50 | yes | 1.150 | 0.2500 | 0.3333 | 0.2774 |
| **0.35 × 0.25** | **0.60** | **yes (+0.213)** | **1.725** | **0.2857** | **0.4000** | **0.3329** |
| 0.25 × 0.40 | 0.65 | yes | 2.013 | 0.3023 | 0.4333 | 0.3606 |
| 0.50 × 0.15 | 0.65 | yes | 2.013 | 0.3023 | 0.4333 | 0.3606 |
| 0.35 × 0.40 | 0.75 | yes | 2.587 | 0.3333 | **0.5000** | 0.4161 |
| 0.50 × 0.25 | 0.75 | yes | 2.587 | 0.3333 | **0.5000** | 0.4161 |
| 0.50 × 0.40 | 0.90 | yes | 3.450 | 0.3750 | **0.6000** | **0.4993** |

**Degeneracy thresholds on this fixture, derived from the measured median:**

- `duty_ABS = 0.50` at **T_lock = 0.750 s**
- `L_fight` median `= 0.50` at **T_lock = 0.861 s**
- `duty_ADD = 0.50` at **T_lock = 1.500 s** — unreachable inside the bracket

> **The mechanism's safe ceiling on this fixture is T_lock ≲ 0.75 s.** The bracket's top two rungs sit **on** (0.75) and **past** (0.90) the boundary. Every rung ≤ 0.65 is comfortably safe. **T_lock 0.60 sits in the middle of the safe band — not at either edge.**

### 4.4 Which values land in a degenerate regime

- **T_lock 0.90 (W 0.50 × R 0.40) — DEGENERATE. Flagged on two independent measures.** `duty_ABS = 0.600` and `L_fight` median `= 0.5225` both cross 50 %. This is precisely the failure §8.6 called *"the one that does not announce itself"* — a boss locked for more than half its own attack cycle and more than half the fight, producing a broken-easy fixture that stage 2 would then calibrate against.
  **One honest qualification:** `L_fight` is an **upper bound** under A1. Post-build, a kiting player both (a) leaves range when the cooldown expires, suppressing windup entry entirely, and (b) causes C2-L1 whiffs. Both reduce realized swings, so the true post-build `L_fight` will be *lower* than tabulated. `duty_ABS`, however, is **cycle-relative and does not depend on the swing count** — the 0.600 at T_lock 0.90 is robust to A1. The degeneracy call on 0.90 therefore stands on the measure that survives the assumption.
- **T_lock 0.40 (W 0.25 × R 0.15) — NOT degenerate, but ARITHMETICALLY FRAGILE. Do not choose it.** It clears the §3.4 floor by 0.013 s — **one eighth of a tick**. Its usable window is `T_lock − REACTION_LATENCY_S = 0.40 − 0.30 = 0.10 s`, which on the 0.1 s grid is **exactly one tick**, yielding 0.575 m of daylight against the 0.5 m minimum: 0.075 m of margin, or 13 ms of player travel. **Any single tick of policy latency beyond the modelled 0.30 s zeroes the window**, and G1/G2 then fail for the arithmetic reason §8.6 warned about rather than for a behavioural one. On a 0.1 s tick grid a one-tick window is not a mechanism; it is a rounding artifact.
- **T_lock 0.60 — CLEAN.** Usable window 0.30 s = **three ticks**; daylight 1.725 m against a 0.5 m floor (3.45× margin); duty 28.6 / 40.0 %; L_fight 34.8 %. Robust to ±1 tick of realization error in either direction (see F1/F2: even at a realized 0.70 s the numbers are duty_ADD 0.318 / duty_ABS 0.467 / L_fight ≈ 0.406 — still non-degenerate). **This is the value with margin on both sides, which is what a stage-1 "prove the geometry exists" value is supposed to have.**

---

## 5 — Verdict, and the build flags that come with it

**CAL-C1 = 0.35 and CAL-C2 = 0.25 (T_lock = 0.60 s) STAND AS GROUNDED INITIAL VALUES.** No move inside the fallback bracket is recommended. The spec's §3.4 derivation survives contact with the measurement in every particular it asserted: the boss's realized cadence is 1.500 s median, T_lock 0.60 is 40 % of it under the strictest reading, the value sits 1.55× above the arithmetic floor exactly as claimed, and both the value below it and the value above it in the pre-registered bracket have concrete disqualifying properties. The number that §8.6 said was missing is now measured, and it does not move the choice.

Five flags follow. **None changes the verdict; three want a conductor ruling before a line of code is written.**

> **F1 — TICK REALIZATION. 0.35 and 0.25 are 3.5 and 2.5 ticks. The sum is integral; the phases are not. (RULING WANTED.)**
> The engine runs dt = 0.1 s and §3.3's `Commitment` durations will be compared against `elapsed` on tick boundaries — the same grid that already converts a `U(1.411, 1.511)` cadence draw into a two-point mass at {1.5, 1.6} (§3.2). A naive `elapsed >= deadline` machine realizes windup 0.35 → 4 ticks and recovery 0.25 → 3 ticks, giving a realized **T_lock = 0.70 s, not 0.60**.
> **Recommendation: hold T_lock as SIX TICKS and split it 3/3 — windup 0.30 s (the lower bound of the same measured 0.30–0.40 dead-time quantum CAL-C1 was drawn from, so it stays M-anchored), strike on tick 4, recovery 0.30 s.** This preserves §3.4's window arithmetic *exactly* (T_lock 0.60 unmoved, daylight 1.725 m unmoved) and *improves* the heavy-vs-basic hierarchy the spec's derivation-1 cares about: 0.750 / 0.30 = **2.5×** versus the spec's stated 2.14×. The alternative 4/2 split (windup 0.40, recovery 0.20) also holds T_lock at 0.60 but drops the hierarchy ratio to 1.875×, below the 2× the spec's own reasoning leans on. **Prefer 3/3.**
> **Note for the [CAL] register:** the *only* fully tick-aligned point in the pre-registered `{0.25, 0.35, 0.50} × {0.15, 0.25, 0.40}` bracket is `0.50 × 0.40 = 0.90` — the degenerate corner. There is no tick-aligned escape inside the bracket, which is why the fix belongs in the realization rule rather than in the values.

> **F2 — STRIKE-TICK ACCOUNTING. Is the strike tick inside T_lock or additional? (RULING WANTED.)**
> §3.2 gives `strike` a duration of "exactly one tick" and §3.4 computes `T_lock = WINDUP_S + RECOVERY_S = 0.60` with no term for it. If the strike tick is *additional*, realized T_lock = 0.70 s (7 ticks). Both readings are non-degenerate (0.70 → duty_ADD 0.318, duty_ABS 0.467, L_fight ≈ 0.406), so **this does not threaten the verdict** — but G2's window arithmetic is stated to a precision that the ambiguity exceeds, and the gate should not be evaluated against an under-specified denominator. Pick one before the build.

> **F3 — THE TELEGRAPH ALREADY ADVERTISES A 0.5 s WIND-UP FOR THIS EXACT SWING. (RULING WANTED.)**
> `TELEGRAPH_WIND_UP_DEFAULTS_S["point"] = 0.5` (`spatial_engine:223-228`, commented *"degenerate nearest-1 marker: reaction-margin floor tell"*), and the frozen traces confirm it: every boss basic-swing telegraph in the battery carries `wind_up_s: 0.5` — **while applying no delay at all.** It is cosmetic today. Once C2 lands, `WINDUP_S = 0.35` (or a 0.30 realization per F1) makes the *advertised* lead and the *real* strike disagree by 0.15–0.20 s. That is exactly the failure mode the nova cast seam was written to prevent (`spatial_engine:6255`, verbatim: *"and Godot would render a lie"*), arriving on the melee side.
> **Recommendation: the C2 fixture packet writes `wind_up_s = WINDUP_S` onto the boss melee skill alongside `commitment_bin` and `cast_time`, so the mint's per-skill override (`_mint_telegraph_spec`: `skill_dict.get("wind_up_s")` before the default table) carries the real number.** One key on the same packet §3.3 is already authoring; no new mechanism.
> Note the tempting alternative and why I am not recommending it: 0.50 *is* in the fallback bracket, so adopting `WINDUP_S = 0.50` would make the mechanism inherit the telegraph's own existing constant for free. But it forces T_lock to 0.65 (with R 0.15) or 0.75 (with R 0.25 — on the `duty_ABS = 0.50` line) or 0.90 (the degenerate corner). **Writing the packet is cheaper than moving the value.**

> **F4 — C2's SCOPE vs THE SHARED ACTION GATE. (Recommend the build state it explicitly.)**
> The nova consumes the same `mob.action_available_at` as the melee and is selected in **180/180 fights at t = 0.7 s**, holding the gate for 6.0 s. The spec scopes C2's packet to the boss *melee* skill and is silent on the nova. If C2 were to also commit the nova cast, the first 6.8 s of every boss fight becomes lock-relevant and every number in §4 moves. **Recommend stage 1 state in one line that C2 arms on the boss melee packet only and the nova cast remains uncommitted** — which is what §3.3 already implies but does not say.

> **F5 — THE PROJECTION'S DIRECTION OF ERROR, for G2's benefit.**
> Under C2, the cooldown is armed at the attack site — so a whiffed swing (C2-L1) *still pays its cadence*. A player kiting out of reach when the gate opens, however, suppresses windup entry entirely and the boss pays nothing. The two effects run opposite ways on the swing *count* and the same way on the *resolution* count. **Prediction, offered as a falsifiable check the build can run for free:** post-build the boss's realized **swing** cadence should stay pinned at 1.5/1.6 s whenever it is engaged, while the **resolution** rate falls. If the post-build swing cadence itself moves off {1.5, 1.6} in engaged windows, C2 changed the attack cadence — which §3.4 says it must not — and that is a build defect, not a balance outcome.

---

## 6 — Two mechanism facts found while measuring (evidentiary, reported)

**(1) The dead-on-the-swing-tick cooldown emission.** The decay loop (`spatial_engine:6467-6471`) skips any entity with `not e.is_alive`, and the tick order is player phase → mob attack phase → ally-proxy realized-fight phase → decay → frame emit. On the ticks where an ally-proxy kills the boss *after* the boss has already swung that tick, the decay never runs and the emitted `skill_cooldowns[0]` is the drawn value with **no** decay offset. 6 of 4,432 recovered swings take this branch; all 6 are the fight's final swing on a player win, all in the `post` leg, and all land inside the closed-form band once the offset is dropped. The instrument reads the boss's own `alive` flag in that tick record and branches mechanically rather than heuristically. **This split is itself the confirmation that the one-decay offset rule is right for the other 4,426** — two different branches, one band, zero violations.

**(2) Where the fight's determinism actually lives.** Nova cast at t = 0.700 s and first basic swing at t = 6.800 s, both with **σ = 0 across all 180 fights**. The opening 6.8 s of every boss fight in the battery is identical: approach, one nova selection consuming the full 6.0 s action budget, then the metronome starts. All 180-fight variance enters *after* t = 6.8 s. Anything the WR3 build measures in that opening window is measuring a constant.

---

## 7 — Reproduction

```
python3 ~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/\
2026-07-30-wr3-dutycycle-support/wr3_duty_cycle.py \
  > ~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/\
2026-07-30-wr3-duty-cycle-prebuild.json
```

Read-only; no arguments; aborts with a non-zero exit and an empty payload if any of I0 / V1 / V2 / V4 / V5 fails. Runtime ≈ 90 s over 450 traces. The instrument lives in the gamora notes support dir per the F-WR2-5 / `wr1_envelope_spec_support` precedent — **instruments in notes are instruments, not production code**, and nothing under `src/` was read for anything but reference or written at all.

---

*R-WR3-12(8.6) pre-build measurement gate — gamora, simulation seam, 2026-07-30. Read-only over the frozen WR2 battery of record. No engine edits, no simulation runs, no telemetry writes.*
