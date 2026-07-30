# WR2-ENCGEO / F-WR2-5 pursuit diagnostic — the speed half and the AI half, measured

**Run:** WR2-ENCGEO-2026-07-29. **Finding:** F-WR2-5 (Matt, owner-watch): *"The boss movement speed
is too fast… the boss is pinned to wherever the character moves… Unless it's not movement speed but
the AI that pins the boss to the player. It could be a combination of both."*
**Cell type:** READ-ONLY diagnostic. No `src/` change, no simulation executed. **Author:** gamora.
**Date:** 2026-07-30. **Class:** evidentiary note. **Findings only** — the design fork is the
conductor's and Matt's.

**Instrument:** `agentic_orchestration/gamora/notes/2026-07-30-wr2-f5-support/wr2_f5_pursuit.py`
plus the supplement `…/wr2_f5_kite_onsets.py`. Both live outside `src/` executed paths, per the
`2026-07-29-wr1-envelope-spec-support/` precedent.
**Bank:** `2026-07-30-wr2-f5-pursuit-diagnostic.json` (per-fight rows for all 180 boss fights +
per-leg + pooled + the watch-seed exhibit). Supplement output:
`…-support/wr2_f5_kite_onsets_output.json`.
**Population:** all 450 banked AFTER traces at
`reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after/`; the pursuit
measures run on the **180 boss-tier fights** (3 legs × 30 seeds × arms A/B).

---

## §1. Instrument validation — 4 banked facts reproduced before any new number was read

Discipline #11/#12. The instrument aborts unless all four gates pass. They all passed.

| gate | banked fact | reproduced |
|---|---|---|
| **V1** | watch-seed footer, `pre` / boss/B / seed 74000802 → `elapsed_s` 37.0 | **37.000000000000256** ✅ |
| **V2** | battery-of-record §4.2 `pre`-leg AFTER elapsed means: boss/A 32.04, boss/B 48.92 | **32.043333** / **48.923333** (n=30 each) ✅ |
| **V3** | S-1: 450 traces, **292,305** pair samples, **0** violations, worst slack **−0.000989 m** | **450 / 292,305 / 0 / −0.0009889945962079372** ✅ |
| **V4** | **132** nova firings, 44 per leg, 44 distinct trace basenames per leg | **132**, 44/44/44, 44 traces/leg ✅ |

V3 is a full independent reimplementation of the Cell-B S-1 predicate
(`slack = d − (rᵃ+rᵇ)`, `tol 0.01`) from the raw traces, and it lands on the same worst-slack pair
(`trash/seed74000800`, tick 43, werewolf ↔ `zombie_a01_1`, d = 0.99901 vs contact 1.0) — consistent
with the 2026-07-30 erratum that the residual is a contact-solver ε during melee engagement, not a
spawn artefact.

**Fixture geometry (header join, constant across all 180 boss fights):** player radius 0.5 m, boss
radius 1.5 m → body floor **C_body = 2.0 m**. Boss melee skill `point`, `range_m` 2.0; under
`body_separation_v2` (the `bsep` flag, ON in all three leg names) the live range gate is
`nearest_dist <= range_m + target.entity_radius` → **C_reach = 2.5 m**. Spawn separation
**17.051 m**, identical in all 180. Tick size 0.1 s, no reduced-tick ticks observed.

---

## §2. THE SPEED HALF — the ratio is 0.70, not 1.0. The boss is 30 % SLOWER than the player.

| quantity | value | distinct values over 180 fights |
|---|---|---|
| boss `movement_speed_ms` | **4.025** | 1 |
| player `movement_speed_ms` | **5.75** | 1 |
| **boss / player** | **0.70** | 1 |
| escort `movement_speed_ms` | 4.0825 (ratio 0.71) | — |

**Provenance — the two sides of the ratio do NOT have the same provenance.** Recovered by read-only
source inspection, not inferred from traces:

- **Player 5.75** — `spatial_engine.py:7311`, `float(class_dict.get("movement_speed", 5.75))`. The
  kitcal werewolf kit declares no `movement_speed`, so the player takes the **ungraded engine
  default**. This is exactly the case `kitcal_g5_harness.py:941` labels
  `movement_speed_provenance = "engine-default-ungraded"` (INFO-1's subject).
- **Boss 4.025** — `kitcal_g5_scenarios.py:620`, `"movement_speed": 5.75 * float(row.run_speed)`.
  **Graded** from the GD record: sim base pace × the pak-adjusted `run_speed` multiplier. 4.025 /
  5.75 = 0.70 exactly, so the boss record's `run_speed` is 0.70. Consumed at
  `combatant.py:1342`.

So the boss's speed is a *graded* number sitting over an *ungraded* one. The fixture's ratio is 0.70
and the denominator is a default, not a measurement of the werewolf.

---

## §3. Boss speed utilization — the boss moves on **100 %** of ticks, at ~**95.8 %** of cap

Per step k: `s_k = |b_{k+1} − b_k|`, `cap_k = v_boss·dt_k`, `u_k = s_k / cap_k`.

| quantity | pooled (180 fights) |
|---|---|
| **fraction of steps with any displacement** | **1.000** (min 1.000, max 1.000 — every fight) |
| mean `u` (mean of per-fight means) | **0.9577** (range over fights 0.9448 – 0.9734) |
| fraction of steps at `u ≥ 0.999` | 0.0511 (median 0.0390) |
| min `u` seen anywhere | 0.0932 |
| max `u` seen anywhere | 0.99999999999999 |
| mean per-tick boss displacement | 0.3862 m (= 0.960 × 0.4025 m cap) |

There is not one tick in 180 boss fights on which the boss stands still. `u` sits just under 1
rather than at 1 because of the contact solver, not because of any AI hesitation: the boss steps its
full `v·dt` toward the player, overlaps, and the area-weighted separation split
(`_body_separation_split`) then shoves it back by its 0.10 share of the correction, shortening the
net displacement. `u` is the *realized* fraction; the *commanded* fraction is 1.0 by construction of
`factor = min(speed/d, 1.0)`.

---

## §4. Pursuit heading purity — frame-perfect, against the player's PRE-step position

Angle between the boss's realized displacement and the boss→player unit vector, computed against
**both** intra-tick phases because the read order is not assumable:

| reference | pooled mean | max over fights | fraction of steps ≤ 1° |
|---|---|---|---|
| **θ_pre** — player position at step start | **1.90°** | 122.8° | **0.912** |
| θ_post — player position at step end | 9.50° | 126.0° | 0.077 |

θ_pre is the concentrated one → **the navigator reads the player's position BEFORE the player moves
in that tick**, and steers exactly at it. 91.2 % of all moving steps are within 1° of the pursuit
ray; the pooled mean error is under two degrees. There is no turn-rate limit, no acceleration ramp,
no lead, and no lag beyond the one-tick read.

**The residual angle is the contact solver, not the AI.** Of the 2,824 steps with θ_pre > 5°,
**2,692 (95.3 %)** are steps that END within 1 cm of the body floor — i.e. the shove, not a steering
error. This matches the law read at `spatial_engine.py:2129-2156`: `heading_rad` is set to
`atan2(dy,dx)` of the commanded vector every tick, and the only thing that perturbs the landing
point is the separation solver and the arena clamp.

---

## §5. Separation — the median separation is **exactly 2.000 m in every one of 180 fights**

| quantity | pooled |
|---|---|
| min separation over all fights | **1.99936 m** (the S-1 ε residual) |
| **median separation, per fight** | **2.000 m — min 2.000, max 2.000 across all 180 fights** |
| mean separation (mean of per-fight means) | 2.367 m (range 2.190 – 2.866) |
| max separation over all fights | 17.051 m (= spawn) |
| **fraction of ticks within C_body + 1 cm** | **0.921** (median 0.931; leg range 0.889 – 0.952) |
| fraction of ticks within C_body + 5 cm | 0.944 |
| fraction of ticks within C_body + 25 cm | 0.949 |
| **fraction of ticks inside the melee gate (≤ 2.5 m)** | **0.953** (median 0.960; leg range 0.933 – 0.972) |

Timeline, identical in all 180 fights: bodies start 17.051 m apart, the boss enters its melee gate at
**t = 1.5 s** and reaches the body floor at **t = 1.8 s**, and from there the pair is glued.

The pinned claim quantified: **the boss is inside its melee gate for 95.3 % of the fight and in body
contact for 92.1 % of it.** The single most common separation value is the floor itself.

---

## §6. Attack-commit — the boss has **no commit state at all**. It move-and-hits, always.

`commit_state` on the boss entity is **`"idle"` on 76,714 of 76,714 boss-alive ticks** — the only
value ever observed. Cross-tab: `idle → frac_moving = 1.000`. There is no wind-up freeze, no
recovery freeze, no attack-committed stationary tick.

Confirmed against the source: `_navigate_entity(mob, …)` is called for every alive mob every tick
inside the mob-movement phase (`spatial_engine.py:5384`), with early returns only for hard-CC, leash,
and fear-flee. No branch consults an attack or cast state.

Inside the boss's **own** nova wind-up windows (§7) the boss moves on **100 %** of the 23 ticks at
mean `u = 0.9889`, covering 9.155 m. The boss does not stop to cast its own ring.

### 6.1 Kite windows the AI concedes

A kite window = a maximal run of ticks with separation > C_reach (2.5 m), i.e. the boss cannot reach.

| quantity | pooled |
|---|---|
| windows per fight | mean **1.267**, median **1**, max **2** |
| fights with zero windows | 0 |
| window duration (n = 228) | min 0.6 s, median 1.5 s, **max 1.5 s** |
| total daylight per fight | mean **1.66 s** (min 1.5 s, max 2.1 s) |
| **kite fraction of fight** | mean **0.047** (median 0.040) |

**Every fight's first window opens at t = 0.0 and closes at t = 1.4 s — the opening approach, in all
180 fights, identically.** Its 1.5 s length is not an AI concession: it is the mutual charge
(17.051 − 2.5) / (5.75 + 4.025) = 1.48 s.

**48 of 180 fights (26.7 %) have a second window; it opens at t = 5.0 s and lasts 0.6 s in all 48**,
reaching a peak separation of 2.996 m. Those 48 are **exactly** the 48 boss fights with no nova
firing (180 − 132), split 16 per leg, 24 arm-A / 24 arm-B. Inspecting one: the window is opened by
the **player**, not conceded by the boss — the player's per-tick `decision.intent` is `reposition`
onto an **escort** (`slitha_melee_b01_1`), so the player walks ~1 m off the boss and the boss closes
it back within 6 ticks. Correlation measured; mechanism inspected on one exemplar only.

**So: after t = 1.4 s the boss concedes no daylight at all in 132 of 180 fights, and 0.6 s of
player-initiated daylight in the other 48.**

---

## §7. The 132 nova telegraph escapes — the boss closes 8.2 m and the player never leaves the ring

All 132 firings are geometrically identical (consistent with battery-of-record §3's "one geometry
verified 132 times"): onset tick 7 (t = 0.7 s), declared `fire_tick` 30, `wind_up_s` 2.3188,
`radius_m` 12.0.

| quantity | all 132 firings (single value unless noted) |
|---|---|
| declared window | 2.30 s |
| separation at onset | **10.209 m** |
| **separation at declared fire** | **2.000 m** |
| **separation at realized delivery** | **2.000 m** |
| max separation inside the window | 10.209 m (the onset value — it only decreases) |
| **net closure** | **8.209 m** at **3.569 m/s** |
| boss path length in window | 9.155 m; boss moving on 100 % of ticks; mean `u` 0.9889 |
| player path length in window | 12.002 m (= 5.218 m/s = 0.907 × 5.75) |
| player distance to ring origin at onset | 10.209 m (origin = the boss's position at onset) |
| **player max distance to ring origin in window** | **10.209 m** |
| player distance to origin at declared fire | 5.707 m |
| player distance to origin at realized delivery | 4.480 m |
| **firings where the player ever left the 12 m ring** | **0 of 132** (132 assessed, 0 unassessable) |
| boss distance to its own ring origin at fire | 6.174 m (inside its own ring) |

**What the boss does during the telegraph:** it never stops, and it closes the entire 8.2 m gap,
arriving at the body floor at t = 1.8 s — *twelve ticks before its own ring fires* — and holding
2.000 m from there through the delivery tick and beyond.

**What the player does:** it does not run an escape. Watch-seed tick-by-tick (`pre`, boss/A and
boss/B, seed 74000802, identical): the player's `decision.intent` is **`advance`** for ticks 7–15
(closing at 0.978 m/tick = the exact sum 5.75 + 4.025 of both speeds), then **`reposition`** from
tick 16 on. Its distance to the ring origin runs 10.209 → 5.609 (t = 1.5 s) → wanders 5.6–6.96 →
5.707 at fire → 4.480 at delivery. It is inside the 12 m footprint for **100 %** of every window.
The player's intent vocabulary across the `pre` leg's 60 boss fights is
`{reposition: 22,758, advance: 960, hold: 572}` — there is no `evade`/`escape` intent in the
realized stream at all. S-7 clause 1 certifies the ring is *analytically* escapable at
`worst ratio_to_bound 0.149`; the realized policy never attempts it, and the two facts do not
contradict — one is a bound, the other a behaviour.

### 7.1 Two incidental measured facts (no interpretation offered)

1. **The ring delivers 3 ticks after its declared `fire_tick`, in 132/132 firings.** The realized
   boss-sourced `circle`-geometry damage event lands at tick 33 where the telegraph declares
   `fire_tick` 30 (lag distinct value: exactly 3 ticks, 0.3 s). The escape window's true closing
   edge is therefore 2.6 s, not the declared 2.3 s. I did not find this offset banked in the Cell-D
   or WARN-discharge notes; flagged for the conductor as an INFO, not asserted as a defect.
2. **Declared vs realized ring payload.** `telegraph.damage_amount` is 218.076 (median; max 247.517)
   while realized `delivered` is 207.4 / 414.8 / 470.8 (median 414.8). 414.8 = 2 × 207.40, matching
   the battery-of-record's S-2 `worst_drop_abs` 414.80 and anchor-grain 207.40. Consistent with the
   already-banked "`nova_unit_payload_hp` ≠ `telegraph.damage_amount`" trap (WARN-discharge §3).

---

## §8. The decomposition, stated flat

F-WR2-5 asked whether PINNING is speed, AI, or both. Measured:

- **The speed half is not the mechanism.** The boss is **0.70×** the player's speed, not 1.0× and not
  faster. The player can out-run the boss at every instant, at 1.725 m/s of surplus. Caveat on the
  ratio's own footing: its denominator (5.75) is the ungraded engine default, its numerator (4.025)
  is graded from the GD record.
- **The AI half is the mechanism, and it has three separable components:**
  1. **Zero-latency pursuit.** Target = the player's current position, re-read every tick; heading
     re-solved every tick (θ_pre mean 1.90°, 91.2 % of steps ≤ 1°); no turn-rate limit, no
     acceleration, no lead, no lag beyond one tick.
  2. **Zero-downtime pursuit.** No commit state exists on the boss — `idle` on 76,714/76,714 ticks,
     moving on 100 % of them, including 100 % of its own nova wind-up ticks. The navigator is not
     gated on attacking.
  3. **Zero-daylight steady state.** Median separation is exactly the 2.0 m body floor in every one
     of 180 fights; 95.3 % of ticks inside the 2.5 m melee gate; the only conceded window is the
     1.4 s opening charge (and, in the 48 non-nova fights, one 0.6 s player-initiated gap at
     t = 5.0 s).
- **Which means the player-side policy is the other load-bearing half of the observed pinning.** The
  realized player stream is `reposition`-dominated (22,758 / 24,290 intents) and closes into the boss
  during the boss's own 12 m ring telegraph in 132/132 firings. A boss 30 % slower than the player
  stays glued because nothing in the realized player behaviour ever tries to use the 1.725 m/s
  surplus to open distance. Perceived "boss too fast" and "boss pinned to me" are both consistent
  with a *slower* boss that never pauses, never turns wide, and never has to — because the target
  keeps closing.

---

## §9. Reproduction

```
python3 ~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/\
2026-07-30-wr2-f5-support/wr2_f5_pursuit.py        # gates V1-V4 then writes the JSON bank
python3 ~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/\
2026-07-30-wr2-f5-support/wr2_f5_kite_onsets.py    # kite-window onsets + theta-outlier attribution
```

Exit code 0 iff all four validation gates pass; 2 otherwise. Runtime ~2 s and ~2 s. Read-only:
neither script opens anything for write outside `agentic_orchestration/gamora/notes/`.
