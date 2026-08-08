# KC2-SIM Phase D — the LOCOMOTION LAP (§ 10.9a). gamora seam.

**Run:** KC2-SIM (autonomous, desirable-run pattern). **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Author:** gamora (simulation seam). **Phase:** D — the F-12 locomotion amendment lap (L-46 / L-47).
**Base:** engine `main` @ `13451fdf` (beat 3) — **moved to `265069b1` mid-lap** when star-lord's
`28b578fe` + drax's counter-sign landed underneath me (see F-L10).
**Commit:** **`a5382e65`** — engine `main`, **UNPUSHED**.
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/kc2-locomotion-lap-2026-08-08.md`.
**MIGRATION:** `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — new top entry.

> ### The one-paragraph version
> The board moves. T-1 **still fails**, and it is not re-pinned — but the residual collapsed from
> **+23.16 s to +4.21 s**, the body-count coupling fell from **+0.737 to +0.515** against a fixture
> at **+0.154**, and the per-seed variance halved. Then the part that matters more than any of
> those: **the residual is no longer distributed, it has an ADDRESS.** Split on whether a wave rolls
> the ambush point, the **59 waves without p05 match the fixture's mean to +0.20 s** and the entire
> delta sits on the **33 waves with p05** (+11.36 s). The term carrying it is the **3.0 s intra-drip
> cadence** — the one piece of the arrival choreography that is **ADOPTED, not MEASURED** (L-21: only
> the t + 4.0 s start anchor was ever observed), and which was **INERT under the static board**
> because every p05 body read slot 0. The lap **ships 3.0 s unchanged**. And `v_ref` was **not
> calibrated**: the K-1…K-3 region is **EMPTY under every reading**, which halts calibration by rule.

---

## § 0 — Headline (the conductor's index)

| # | Quantity | Result |
|---|---|---|
| **T-1 per-wave** | 92 clears, ± 1.0 s, tick-quantised, **UNCHANGED** | **8 IN-BAND / 65 OVER / 19 UNDER — FAIL** (beat 3: 0/89/3) |
| delta | mean / median / range | **+4.207** / +4.422 / [−67.32, +29.99] s (beat 3: +23.16) |
| **r(clear, N)** — DIAGNOSTIC | sim vs fixture +0.154 | **+0.515** (beat 3: **+0.737**, the falsified comparator) |
| **residual localisation** | split on p05 presence | **non-p05 (n=59) +0.20 s · p05 (n=33) +11.36 s** |
| two-class ratio | ×10 : non-×10 | measured **2.00×** · sim **0.905×** — still INVERTED, **re-attributed** |
| seed sd | mean / max | **1.72** / 4.63 s (beat 3: 3.22 / 5.10) |
| **K region** | K-1 ∧ K-3 at declared A = 0.5 s | **EMPTY under every reading** — calibration **HALTED** |
| **JC-7 consequence** | A ≳ 2.81 s required | **VIOLATED by 2.31 s** — a FINDING with 4 named candidates + 1 of mine |
| **v_ref** | | **NOT calibrated.** Standing 4.0 m/s carries forward with its grade |
| micro-oracles | MO-1…MO-5 | **5/5 PASS**; MO-5 re-demonstrated under **CITED** radii, 7.75 → **9.797 s** |
| **L-A vs L-B** | sensitivity delta | **+0.44 s mean**, max 2.63 s, 61/92 waves differ; `r` identical to 0.005 |
| **N-sensitivity** | ±6.67 % (F-13 floor) | **+0.50 / −1.46 s** — the result **INHERITS** the F-13 residual |
| **D2-2** | negative control, **n = 32** | mean closes ≈ **6.9 m/s**; structure **flat** across a 2× sweep |
| **s2 second geometry** | waves 151–159, INFORMATIVE | tripwire fires on 5/9 — **and cannot discriminate**, attribution given |
| tests | bare `pytest` post-commit, per-file vs L-39 | **63 F / 10,354 P / 21 E — EXACT match on 63/21, ZERO novel failure files** |
| commit | engine `main`, **UNPUSHED** | **`a5382e65`** |

---

## § 1 — What was built (§ 10.9a A–C, amendment brief § 3)

**Per-actor motion**, `x_a(t+dt) = x_a(t) + characterRunSpeed(a)·v_ref·dt·unit(target − x_a)`, planar,
open-plane. The disc hit-tests **current** positions; `disc.resolve_tick` no longer sees a spawn
coordinate anywhere.

**Six cited radii per selected arena**, p01 keyed **per content tier**, in the `PatrolPoint_Attack`
centroid frame. `Arena.emitter_radius_m` **DELETED, not re-valued**.

**The gate**, per record: `ViewDistance` / `MaxPursuitDistance` / `PursuitTime`, with the p05 ambush
exclusion read from the **pool's own `is_ambush` flag** rather than inferred from the point index.

**Two limbs** — L-A zone-first (ruled default) and L-B gate-first (sensitivity); the run records which.
**Arrival and kill instrumented separately** — `contact_t_s` / `engage_t_s` / `death_t_s` per actor.

**SHA-256 verified before consumption**, all three, in both the `legolas/notes/…-microprobe/` and
`legolas/scratch/2026-08-08-kc2-citation/` copies (identical), then vendored byte-identical into
`reincarnated-engine/data/kc2/` with the digests asserted by test:

```
kc2_crucible_emitter_geometry.csv  ece0c345f14e2da1af63bd2e388b7dc0be32a1e0c703636b192924f84649cff9  332 rows
kc2_crucible_patrolpoints.csv      106facbaac3cb7b44991b569b1b2934738a3eee83145fb8e095071ae93693747  173 rows
kc2_s1_banda_record_inputs.csv     ac50ef778555ec26e76559eb5932f2dd0b478f8f4f37038464c09a8d777f657e  895 rows
```

**Every figure § 10.9a B quotes was RECOMPUTED from the bytes, not transcribed** (Discipline #11).
All agree: `characterRunSpeed` n = 895 / median 1.000 / mean 1.0358 / 0.60–2.00 / 191 exactly 1.0 /
311 below / 393 above; `ViewDistance` 80.0 on 868; `MaxPursuitDistance` 125.0 on 868; `PursuitTime`
10 000 ms on 890 (12 000 on 5); `disableMovement` absent 895/895; jitter n = 810 median 15.0;
`walkDistance` n = 677 median 4.5.

---

## § 2 — The player-movement policy, stated ONCE (§ 10.9a A/C/D)

**`CAMP_THEN_COLLECT`, at the `PatrolPoint_Attack` centroid.** Closure attribution is
`closing = v_ref × characterRunSpeed(a)` — **the player contributes ZERO closing term** — and the
conversion happens in one function, `locomotion.closing_to_v_ref`, asserted round-trip by test.

The starting declaration was **pure CAMP**, which is what § 10.9a A/C imply: § 2.2's discriminability
caveat and § 10.9a A's limb analysis are both written for *"a centrally-camped player"*, and § 10.9a
E channel (i) states the premise as *"the player stops touring."* It is also the conservative limb.

**Pure CAMP was then MEASURED to be non-terminating, and that is a finding about the spec's model
rather than a defect in the build** — see F-L1 below. `CAMP_THEN_COLLECT` is the minimal completion:
the player holds while **any** actor is inbound and closes on the residual only when **none** is. The
measured cost of the completion is **0.95 m of mean player path per run, firing on 32 of 368 runs**,
against beat-3 tours of **88–199 m**. Channel (i) survives: the player has stopped touring.

`KITE` and `TOUR` are named and **not implemented**; `TOUR` is the retired static-board behaviour and
`simulate_wave` raises on it.

---

## § 3 — The `v_ref` bracket: A declared first, then the consequence checked (JC-7)

### 3.1 `A` declared, BEFORE the check

```
A := spawn_resolution (0.0 — AC-10.6 puts p01-p04 at t = 0) + advance_tick_latency (0.5) = 0.5 s
grade: DECLARED-FREE-PARAMETER, **NO CORPUS SOURCE**
```

`calibration.ADVANCE_TICK_LATENCY_S` carries the citation string *"spec § 10.9 — cycle decomposition
term; no corpus source"*. In JC-7's sense `A` is therefore **DECLARED-UNKNOWN-FROM-EVIDENCE with a
build placeholder of 0.5 s**. Nothing in the read set raises it. Declared at this value, with this
grade, **before** the inequality below was evaluated. `k_bracket()` takes `A` as an **input**; there
is no code path that solves for it.

### 3.2 The three constraints, recomputed

| # | class | arithmetic | bound on **closing** |
|---|---|---|---|
| **K-1** | ring (p04) | (38.45 − 4.0)/4.3 = 34.45/4.3 | **≥ 8.0116 m/s** (LOWER) |
| **K-2** | ambush (p05) | (10.17 − 4.0)/6.1 = 6.17/6.1 | **≥ 1.0115 m/s** (LOWER, weak) |
| **K-3** | ring median, MO-5 floor | 33.53/(7.0 − 0.5) = 33.53/6.5 | **≤ 5.1585 m/s** (UPPER) |

**R-L48-1 honoured.** K-2 is an **ambush-class** measurement at a 10.17 m radius and binds p05 and
nothing else; the ring constraints use ring radii. Asserted by test that the two arithmetics carry
different radii and that the ratio exceeds 3.5×.

### 3.3 The region: **EMPTY**, robustly

```
K-1 ∧ K-3  requires  8.0116 <= closing <= 5.1585      ->  EMPTY
```

Not an artifact of the `d_engage` declaration. Under the **most permissive mixed reading**
(`d_engage = 4.0` in K-1, minimising the lower bound; `2.4` in K-3, maximising the upper) it is
`[8.0116, 5.4046]` — still empty. Under the lap's own declared `d_engage = 2.4` on both limbs,
`[8.3837, 5.4046]` — emptier. **Empty under every reading in the DB range.**

**Per § 10.9a D this HALTS calibration.** `v_ref` was **not selected**; the standing declared value
**4.0 m/s (HALT-2)** carries forward unchanged with its grade. It was never solved against T-1
residuals, and there is no code path that could.

### 3.4 The pre-registered consequence — **VIOLATED**, and carried as a finding

`K-1 ∧ K-3` simultaneously satisfiable only if `33.53/(7.0 − A) ≥ 8.0116`, i.e. **`A ≥ 2.8148 s`**.
(Matched `d_engage = 2.4`: 2.8097 s. Most-permissive mixed: 2.6151 s. The spec's pre-registered
**≳ 2.81 s** is confirmed to four figures.)

**Declared A = 0.5 s. Required A ≳ 2.81 s. VIOLATED by 2.3148 s.**

Carried with the four candidates the spec names and **does not choose among**:
1. the minimap glyph is not the spawn instant;
2. the readout is not first-contact;
3. the boss carries a sub-1.0 `characterRunSpeed` — note this **relocates** the term rather than
   dissolving it, because the bound is on *closing*, not on `v_ref`;
4. the player was closing and the attribution differs (i.e. CAMP is wrong for the K-1 observation).

**JC-G7 — a fifth candidate, named as mine and NOT adopted.** The § 10.9a C omissions are, by their
own stated sign, a **latency reservoir**: patrol-idle 1–5 s, `EmoteBeforePursuingChance`, swing
pauses, the `walkDistance` terminal correction. A ~2.3 s shortfall is exactly their order of
magnitude. **I do not fold them in** — constructing `A` to close the inequality is fitting by another
route. It is named so a later lap that models the controller surface knows what it will be testing.

### 3.5 Where the standing `v_ref` sits

Under CAMP at `characterRunSpeed = 1.0`, closing = 4.0 m/s: **VIOLATES K-1** (short by 4.01),
**SATISFIES K-3** (margin 1.16).

**The named prediction was NOT earned, and I say so.** Under mutual closure K-1 reads
`v_ref ≥ 3.4092 m/s`. This lap declares CAMP, so the player contributes no closing term and that
reading does not apply to this run. It is reported as the **policy-conditional** value it is;
claiming it would be importing a closure term the run did not model.

---

## § 4 — Micro-oracles re-run, and MO-5 under CITED radii

| oracle | target | observed | verdict | margin |
|---|---|---|---|---|
| MO-1 energy usable ceiling | 1594 | **1594** | PASS | 0.0 % |
| MO-2 energy reservation | 982 | **982** | PASS | 0.0 % |
| MO-3 s2 in-combat energy | 1477 | **1477** | PASS | 0.0 % |
| MO-4 HP orb / max health | 20 005 | **20 005** | PASS | 0.0 % |
| **MO-5 cycle floor** | 7.0 (one-sided) | **9.7971** | **PASS** | **+39.96 %** (was +10.71 %) |

### 4.1 A second defect found in MO-5's own wiring, and corrected

**MO-5's pin is an s1 measurement, and the observer was running the s2 arena.** The pinned values
7.03 / 7.05 / 7.07 s are **s1 waves 47 / 8 / 81** — they appear verbatim in `MEASURED_S1_CLEAR_S`.
The pre-L-46 observer read `ARENA_S2.emitter_radius_m`, which was harmless only because every arena
carried the same uncited float. **Under cited per-arena geometry the sitting matters**, and running
an s1 pin on s2 geometry is the L-21 pooling violation wearing a different hat. Corrected: MO-5 runs
the **s1** arena's cited **active** ring (p06 OFF, the operative limb) at **tier 5** — the content
tier of w47, the fastest observed floor. Declared, not chosen for its number.

### 4.2 The two effects, reported SEPARATELY (§ 10.6 instruction)

**Effect 1 — geometry**, isolated in the closed form (same formula, same `v_ref`, radius swapped):

```
retired uncited 30.0 m   ->  7.7500 s
cited ring min   29.818  ->  7.7045 s
cited ring MEDIAN 38.1885 -> 9.7971 s      delta vs retired  +2.0471 s
cited ring max   44.231  -> 11.3078 s
```

The cited s1 ring is larger than the retired float, so the traversal leg lengthens and **the floor is
pushed UP**. Cited s1 tier-5 active ring: `[29.818, 34.196, 42.181, 44.231]` m.

**Effect 2 — player-touring removal.** Not visible in the closed form at all; MO-5's expression never
carried a touring term. It lives in the RAMP, where the retired build's clear time carried a
**2.5×–5.1×** tour inflation that CAMP removes by construction. **Quoted from beat 3, not re-run** —
the retired build no longer exists to run, which is itself the honest statement.

**The two are not pooled.** The *provisional-on-geometry* flag from L-43 / F-12-C-4 clears on this
demonstration.

### 4.3 The overshoot is a FINDING, not a better pass

MO-5 is one-sided and 9.797 ≥ 7.0 PASSES. But the number says something the verdict does not:
**the sim's minimum achievable cycle (9.797 s closed-form; 8.0 s empirical over band A at 32 seeds)
EXCEEDS the fixture's fastest observed clear (7.03 s)**. At `v_ref = 4.0` the model cannot reach the
fixture's fast waves at all. That is K-1's message arriving from a second direction — and it is
**not** a licence to re-pin MO-5 or to move `v_ref`.

---

## § 5 — The s1 ramp, waves 1 → 93, against **UNCHANGED** T-1

`t1_table()` over the 92 clears at **32 seeds each** (band `310_000 + wave×1000 + k`, one sequential
pass, Discipline #3 — **deliberately the same band as beat 3**, because `roll_wave` consumes the rng
first and identically, so the same seed yields the **same board and the same scatter**. That makes
the comparison **paired**: every difference below is the motion model, not a different draw).

Arena **`sm_mod/survivalworld_f.map`** — DECLARED over the cited 10-member enumeration, evidence
named (microprobe § 4.5 best fit to galadriel's four s1 arrival bearings, mean |Δ| **11.8°**;
runner-up `survivalworld_a` 13.1°). p06 OFF. Scaling `WaveScaling(gladiator, full grain)`.

### 5.1 The verdict

```
in-band   8 / 92        beat 3:   0 / 92
over     65 / 92        beat 3:  89 / 92
under    19 / 92        beat 3:   3 / 92
delta    mean +4.207 s  median +4.422 s   range [-67.32, +29.99]      beat 3: mean +23.16
seed sd  mean 1.723 s   max 4.628 s                                   beat 3: 3.22 / 5.10
r(sim, N)      +0.5151      r(measured, N) +0.1537      r(sim, measured) +0.0170
x10 (n=9)  measured 28.57  sim 18.17          non-x10 (n=83)  measured 14.29  sim 20.08
ratio      measured 2.00x   sim 0.905x                                beat 3 sim: 0.86x
```

**T-1 FAILS. It is not re-pinned, not widened, not averaged.** `t1_pooled_mean()` still raises.

In-band waves: **5, 9, 15, 18, 42, 60, 79, 84**. Under waves (19): 10, 33, 35, 38, 40, 44, 50, 51,
55, 57, 59, 63, 65, 70, 74, **80**, 89, **90**, **92** — beat-3's three survivors are all still in it.

### 5.2 Selected per-wave rows (the record the report cites)

`lb` = the § 5.3 re-derived lower-bound verdict. `ringL` / `ambL` = last ring / last ambush arrival.

| w | cls | meas | sim | sd | min | Δ | T-1 | lb | E[N] | ringL | ambN | ambL |
|---:|:--:|---:|---:|---:|---:|---:|:--|:--|---:|---:|---:|---:|
| 1 | — | 9.08 | 11.44 | 1.17 | 10.00 | +2.36 | over | consist | 12.00 | 10.04 | 0 | — |
| 5 | — | 12.08 | 12.66 | 2.66 | 10.00 | **+0.58** | **in-band** | consist | 13.00 | 11.26 | 0 | — |
| 8 | — | 7.05 | 11.47 | 0.66 | 10.00 | +4.42 | over | FALS | 12.25 | 9.95 | 0 | — |
| 9 | — | 10.07 | 10.97 | 2.05 | 8.00 | **+0.90** | **in-band** | consist | 17.75 | 9.52 | 0 | — |
| 10 | x10 | 28.42 | 12.03 | 1.10 | 10.00 | −16.39 | under | consist | 12.50 | 10.49 | 0 | — |
| 15 | — | 14.17 | 13.97 | 0.73 | 13.00 | **−0.20** | **in-band** | consist | 18.00 | 12.48 | 0 | — |
| 18 | — | 16.13 | 15.91 | 4.35 | 11.00 | **−0.22** | **in-band** | consist | 13.67 | 14.40 | 0 | — |
| 20 | x10 | 16.73 | 19.44 | 1.32 | 16.00 | +2.71 | over | consist | 10.50 | 18.06 | 0 | — |
| **30** | x10 | 15.53 | **40.25** | 1.03 | 39.00 | **+24.72** | over | FALS | 20.00 | 13.58 | **12.00** | **38.74** |
| 42 | — | 16.25 | 17.03 | 1.91 | 12.00 | **+0.78** | **in-band** | consist | 10.00 | 15.54 | 0 | — |
| 47 | — | 7.03 | 13.53 | 0.75 | 12.00 | +6.50 | over | FALS | 16.00 | 12.01 | 0 | — |
| 50 | x10 | 22.27 | 16.19 | 2.39 | 12.00 | −6.08 | under | consist | 16.17 | 14.73 | 0 | — |
| 60 | x10 | 19.85 | 19.78 | 1.63 | 16.00 | **−0.07** | **in-band** | consist | 6.50 | 18.28 | 0 | — |
| 70 | x10 | 24.02 | 15.56 | 1.25 | 13.00 | −8.46 | under | consist | 26.33 | 14.09 | 0 | — |
| 79 | — | 17.22 | 17.62 | 2.04 | 13.00 | **+0.41** | **in-band** | consist | 15.00 | 16.10 | 0 | — |
| 80† | x10 | 82.13 | 14.81 | 1.70 | 11.00 | −67.32 | under | consist | 25.00 | 13.33 | 0 | — |
| 84 | — | 12.17 | 12.31 | 0.58 | 11.00 | **+0.14** | **in-band** | consist | 25.00 | 10.78 | 0 | — |
| 89 | — | 16.10 | 12.50 | 0.97 | 10.00 | −3.60 | under | consist | 6.00 | 10.98 | 0 | — |
| 90 | x10 | 26.43 | 9.81 | 0.95 | 8.00 | −16.62 | under | consist | 2.00 | 8.26 | 0 | — |
| **91** | — | 13.17 | **29.12** | 4.39 | 24.00 | **+15.96** | over | FALS | 39.50 | 12.33 | **8.22** | **27.57** |
| 92† | — | 78.45 | 28.41 | 2.83 | 24.00 | −50.04 | under | consist | 27.33 | 16.17 | 8.00 | 26.88 |

Note w30 and w91: their `ringL` (13.58, 12.33 s) sits with the rest of the band; their `ambL`
(38.74, 27.57 s) is what carries the delta. That is § 6.

### 5.3 The sign argument — **RE-DERIVED**, never inherited (§ 10.9a E.2)

F-12's 89/92 is a **record**, not a premise. The arithmetic, re-derived under the amended model:

> With the kill term at a declared zero a body dies on its **first** disc tick, so the wave ends at
> its **last arrival**. Arrival times are a function of geometry and speed **only** — they do not
> read actor HP at any point. Therefore `t_end ≥ last_arrival` holds for **any** HP assignment, and
> the measured cycle is a lower bound on every completion of the amended model.

Confirmed empirically: `cumulative_kill = 0.000` and `tail = 0.000` on every band-A wave.

**Result: 46 falsified / 46 consistent** (beat 3: 89 / 3). The falsified set **halved**, because the
touring inflation left — which is the term the amendment removed.

---

## § 6 — ⚑ WHERE THE RESIDUAL LIVES. The sharpest finding of the lap.

The band-A residual is **not distributed**. Split on whether a wave rolls the ambush point:

| class | n | sim mean | measured mean | **delta** | r(sim,N) | r(meas,N) | mean p05 bodies |
|---|---:|---:|---:|---:|---:|---:|---:|
| **without p05** | **59** | 15.659 | 15.455 | **+0.204** | +0.3855 | +0.1060 | — |
| **with p05** | **33** | 27.471 | 16.108 | **+11.363** | +0.0041 | +0.2346 | **7.249** |

**On 59 of 92 waves the amended model reproduces the fixture's mean clear time to a fifth of a
second.** The entire delta sits on the 33 ambush waves.

The arithmetic says why. AC-10.6's choreography emits p05 body *k* at `4.0 + 3.0k`, so a 7.249-body
pool injects `3.0 × (7.249 − 1) = **18.747 s of pure SCHEDULE**` before any traversal at all. The
instrument disagrees: the **fixture's own p05 waves are 0.653 s slower** than its non-p05 waves. The
model predicts ~19 s of ambush penalty; the fixture shows under one second.

**And the term that carries it is the one piece of the arrival choreography that is NOT MEASURED.**
Per § 10.6 / L-21, galadriel confirmed the **t + 4.0 s start anchor ×3** (s1 waves 4/6/13, wave 13
clean) — but *"the 3 s intra-drip cadence sits below the minimap instrument's resolution"* and is an
**adopted model**. Under the retired static board it was **inert**: `simulate_wave` read `sched[sp][0]`
for every body on a point, so all p05 bodies shared the first slot. **This lap is the first time the
cadence has been load-bearing, and the first time it could be falsified.**

Sensitivity (`p05_drip_sensitivity()`, 32 seeds) — **a DIAGNOSTIC that gives the residual an address,
not a calibration**:

| cadence | adopted? | in-band | delta mean | r(sim,N) | delta on p05 waves | delta on non-p05 waves |
|---:|:--:|---:|---:|---:|---:|---:|
| **3.0 s** | **YES (shipped)** | 8/92 | **+4.207** | +0.5151 | **+11.363** | +0.204 |
| 1.5 s | no | 10/92 | +1.168 | +0.4720 | +2.890 | +0.204 |
| 0.0 s | no | 13/92 | **+0.199** | +0.3734 | **+0.189** | +0.204 |

**The non-p05 delta is invariant to three decimal places across the whole sweep.** That invariance is
what makes the localisation a measurement rather than a coincidence of means: the term moves the
residual it explains and nothing else.

**THE RUN SHIPS 3.0 s.** `P05_DRIP_CADENCE_S == 3.0` is asserted by test. Editing a spec constant to
close a residual is fitting — and worse than the usual kind, because it would be fitting a
**MEASURED** gate (T-1) with an **UNMEASURED** term. **Routed to the conductor as a finding**, with
the observation that the cadence is now falsifiable in a way it was not before: a galadriel re-read
targeted at intra-drip spacing on a high-p05 s1 wave would decide it.

---

## § 7 — The composition law: measured, and the degeneracy stated

```
law                 clear_time  ~=  MAX(last_arrival, cumulative_kill) + tail
last_arrival_mean         18.381 s
cumulative_kill_mean       0.000 s          <- DECLARED ZERO, band A carries no per-record eHP
tail_mean                  0.000 s
static_additive_mean     175.434 s          <- the RETIRED composition, computed beside it
static / amended ratio     9.544x
binding term            last_arrival on 92 / 92 waves
```

**SEPARABILITY IS NOT MEASURABLE THIS LAP, AND THAT IS THE FINDING RATHER THAN A GAP TO PAPER OVER.**
A composition law cannot be measured on a model one of whose two terms is a declared zero: with
`cumulative_kill = 0` the `max()` and the sum coincide and the law cannot discriminate.

**Band A** lacks the kill term (beat 3 § C.1: 7 of 896 records carry eHP — 99.2 % absent, C-1).
**s2 was supposed to be where it became measurable** — and it is not, for a *different* reason: the
r2 board is a **wave-160** board, so its coverage over waves 151–159 is **0.315 %**, and on the
handful of instances that ARE covered the bodies carry real eHP (10⁵–10⁶) against a
`compose_damage_basis()` understated by **×130.8…×178.9** (E-6 / HALT-4 PARTIAL). They do not die
inside the tick cap: the kill-ON limb **times out** (9 of 16 seeds on w154) instead of measuring a
kill term. **Band A lacks eHP; s2's covered subset lacks damage. The law is unmeasurable on both.**

The `static_additive` figure is the one thing this section does establish: **9.54×** the amended
arrival term. That is how much of the retired sim's clear time was pure sequencing.

**F-12's 89/92 lower-bound argument is RETIRED as a live argument** and is not re-used anywhere.

---

## § 8 — Arrival profile, gate telemetry, limbs, N-sensitivity

### 8.1 Arrival profile by emitter class

| class | n waves | spawn | first arrival | last arrival | note |
|---|---:|---:|---:|---:|---|
| **ring** (p01–p04) | 92 | t = 0 | **6.267 s** | **14.501 s** | pure traversal |
| **ambush** (p05) | 33 | 4.0 + 3.0k | **6.141 s** | **25.293 s** | 7.249 bodies mean |

The ring's *first* arrival (6.27 s) and the ambush's *first* arrival (6.14 s) nearly coincide — the
p05 body starts 4 s late but only has ~11 m to cross. The divergence is entirely in the *last*
arrival, and § 6 names the term.

### 8.2 Gate telemetry — **pre-registration held**

```
gate re-closures after opening : 0
PursuitTime firings            : 0
```

As pre-registered: `ViewDistance` 80 m > every measured emitter radius (max 47.89 m) and
`MaxPursuitDistance` 125 m > every arena diagonal, so for the 868/895 modal records the gate is open
at t = 0 and stays open. **The 27/895 records at `ViewDistance = 15.0 m` are the exception, and they
are F-L1.**

### 8.3 L-A vs L-B — the sensitivity delta (AC-10.12.4)

```
delta mean +0.440 s   median +0.375 s   range [0.000, +2.625]   61 / 92 waves show any delta
L-A mean 19.908 s     L-B mean 19.467 s
r(sim, N)   L-A +0.4969      L-B +0.5021
```

**A small delta is a reportable finding and it was not forced.** § 2.2 / JC-3 predict near-
indistinguishability for a centrally-camped player because the gate is open at t = 0; forcing
separation would mean choosing a player position to make a difference appear, which is fitting a
policy to a diagnostic. The limbs are *distinguishable* (61 waves differ, max 2.63 s) but small.

**JC-2's caution is CONFIRMED and L-46(a)'s stated reason is not supported by the measurement.**
The ruling adopted L-A as *"the less body-count-coupled shape."* Measured, the two `r(sim, N)` values
differ by **0.005** — L-A is very slightly the *more* coupled of the two. What removes the coupling
is that the monsters travel at all; the choice of limb does not measurably contribute. **The ruled
default stands** (nothing here argues for L-B), but its stated justification should not be carried
forward as if it had been demonstrated.

### 8.4 N-sensitivity (§ 10.9a F.4) — **the result INHERITS the F-13 residual**

Perturbation scale **read from F-13, not chosen**: the band re-grade 271.50 (record) → 289.62
(measured floor) = **+6.674 %**. 32 seeds.

| n_scale | in-band | delta mean | vs base | r(sim,N) |
|---:|---:|---:|---:|---:|
| 1.0000 | 8/92 | +4.207 | — | +0.5151 |
| 1.0667 | 7/92 | +4.703 | **+0.496** | +0.5071 |
| 0.9333 | 9/92 | +2.745 | **−1.462** | +0.3777 |

**The result is SENSITIVE to N at roughly half to one and a half seconds on a ± 1.0 s tolerance, so
it inherits the F-13 residual and says so.** Band A contains no censused wave, so no band-A count is
falsified *or* corroborated; it draws from the same trash limb F-13 graded INCOMPLETE. The asymmetry
(−1.46 vs +0.50) is itself informative: shrinking N removes p05 bodies, and § 6 explains why that
buys more than adding them costs. **No count was re-pinned; the count model is untouched.**

---

## § 9 — The s2 second-geometry diagnostic (§ 10.9a F.5, INFORMATIVE)

Arena **`sm1/survivalworld_a.map`** — a genuinely different cited geometry from s1's
`sm_mod/survivalworld_f.map`, which is what makes this the generalisation test band A cannot provide.
Six cited radii at tier 16: p01 35.758 · p02 32.820 · p03 33.372 · p04 31.720 · **p05 7.160** ·
p06 31.948. Waves 151–159; **wave 160 excluded by construction** (death-in-progress, 104.73 s, *"not
a clear"* — the same exclusion band A applies to wave 93). 16 seeds, band `330_000 + wave×1000 + k`.

**The inequality's direction, corrected.** § 12 pins it as *"sim kit-alone must clear ≤
fixture-with-defenses; **faster ⇒ anomaly tripwire**"*, and those two clauses only compose one way:
the sim is kit-alone while the fixture had **+offense AND −enemy-threat** (L-12a), so the sim should
be **no better** than the fixture — `sim_clear_time ≥ fixture_clear_time`. That reading is also the
only one consistent with *"cannot false-trip under a slow bias."*

| w | measured | sim mean | min | max | N | last arrival | sim faster by | no better? | kill-ON | TO | excluded |
|---:|---:|---:|---:|---:|---:|---:|---:|:--|---:|---:|:--|
| 151 | 16.28 | 18.75 | 15 | 21 | 26.6 | 17.22 | −2.47 | **yes** | 18.8 | 0 | — |
| **152** | 16.45 | 12.94 | 12 | 15 | 17.8 | 11.34 | **+3.51** | no | 12.9 | 0 | **F-13** |
| **153** | 14.78 | 17.69 | 15 | 20 | 23.6 | 16.29 | −2.91 | **yes** | 17.7 | 0 | **F-13** |
| 154 | 14.13 | 12.31 | 10 | 17 | 11.9 | 10.68 | **+1.82** | no | 189.8 | **9** | — |
| 155 | 16.33 | 11.50 | 10 | 13 | 18.4 | 10.04 | **+4.83** | no | 11.5 | 0 | — |
| 156 | 20.22 | 25.25 | 24 | 26 | 17.8 | 23.77 | −5.03 | **yes** | 25.2 | 0 | — |
| **157** | 19.13 | 13.19 | 12 | 15 | 20.3 | 11.60 | **+5.94** | no | 13.2 | 0 | **F-13** |
| 158 | 13.18 | 13.62 | 12 | 17 | 33.1 | 12.17 | −0.45 | **yes** | 13.6 | 0 | — |
| 159 | 26.25 | 11.69 | 10 | 13 | 9.3 | 10.13 | **+14.56** | no | 11.7 | 0 | — |

**Tripwire fires on 5 of 9 — AND IT CANNOT DISCRIMINATE, which is stated rather than glossed.** The
sim's kill term is a declared zero on this band (eHP coverage 0.315 %), so its clear time is **pure
arrival** while the fixture's contains kill. A sim with no kill term beating a fixture with one is
arithmetic, not an anomaly about locomotion. Reporting the firing as a locomotion finding would be
an attribution error.

What the band **does** establish: the movement rules run against a **second cited geometry** and
produce clear times in the same 10–26 s envelope as the fixture (all-9 sim mean 15.22 s vs measured
17.42 s; unexcluded-6 sim 15.52 vs measured 17.73). Under a model with no kill term at all, on an
arena it has never seen, that is the generalisation result.

**w152 / w153 / w157 are simulated, reported, and absent from parameter selection** (F-13 / L-47).
Since the K region is EMPTY and no parameter was selected at all this lap, **the exclusion binds
vacuously** — stated rather than left as an implication.

---

## § 10 — D2-2: the negative control, re-run at 32 seeds

**The embargo, discharged — and the digit is a DIFFERENT QUANTITY, which is the honest statement.**
Beat 3's sweep ran at **n = 8** against a T-1 table at **n = 32**: a control at a different depth
from the thing it controls. Its headline digit (~10.5 m/s) was embargoed. It **cannot be reproduced**,
because the static board it was measured on no longer exists to run. So the restatement is not a
confirmation; it is a replacement.

**Restated, amended model, n = 32:**

| v_ref | ×declared | in-band | delta mean | r(sim,N) | sim ×10 ratio (measured 1.999) |
|---:|---:|---:|---:|---:|---:|
| 2.00 | 0.50 | 0/92 | +15.706 | +0.4292 | 0.977 |
| 3.00 | 0.75 | 5/92 | +7.744 | +0.4911 | 0.951 |
| **4.00** | **1.00** | **8/92** | **+4.207** | **+0.5151** | **0.905** |
| 5.00 | 1.25 | 12/92 | +2.129 | +0.5201 | 0.870 |
| 6.00 | 1.50 | 12/92 | +0.753 | +0.5214 | 0.838 |
| 8.00 | 2.00 | 6/92 | −0.938 | +0.5217 | 0.790 |
| 10.50 | 2.62 | 2/92 | −2.145 | +0.5188 | 0.753 |

**The mean crosses zero at ≈ 6.9 m/s** (linear between 6.0 → +0.753 and 8.0 → −0.938).

**And the control's point survives intact.** Across a **5.25× sweep** of the free scalar,
`r(sim, N)` moves within **+0.429 … +0.522** — flat — and the class ratio moves **away** from the
measured 2.00× (0.977 → 0.753), not toward it. In-band peaks at 12/92. **Fitting the scale parameter
buys the mean and nothing structural.** A scale parameter cannot repair a structure error; that was
true of the static board and it is still true.

Note where K-1 would put it: `v_ref ≥ 8.01` under CAMP, where the mean delta is already **−0.94 s**
and in-band has **fallen** to 6/92. The K-region and T-1 do not point at the same value, which is
another face of § 3.4's violated consequence.

---

## § 11 — Tests, census, commit

**New file:** `tests/test_kc2_locomotion.py` — **41 tests**, covering AC-10.7 … AC-10.12, the three
SHA pins, the record join, every judgment call **paired with its alternative's measured cost**, the
K-region, the composition law, the residual localisation, and the one-way import rule extended to
`locomotion`.

**Beat-3 tests rewritten, not deleted.** Twelve tests asserted the static board's numbers. Each now
asserts the amended measurement **and keeps the beat-3 figure as a named constant** (`BEAT3_SPLIT`,
`BEAT3_DELTA_MEAN_S`, `BEAT3_R_SIM_VS_N`, `BEAT3_CLASS_RATIO`, `BEAT3_SEED_SD_MEAN_S`,
`BEAT3_UNDER_WAVES`, `BEAT3_SIGN_ARGUMENT`) with a header stating that both generations live in the
file on purpose. **A corrected number whose predecessor has been deleted is a correction nobody can
audit.** The T-1 92/92 FAIL verdict **stands as the pinned baseline**; it is not superseded as a
record and it was not re-run.

### 11.1 The census — run TWICE, and the difference between the runs is itself the finding

Bare `pytest`, full census, **no `-k` narrowing**, compared **per file** against the L-39 baseline.

| run | failed | passed | errors | failure files |
|---|---:|---:|---:|---:|
| **L-39 baseline** (re-reproduced this session, 21 m 31 s) | **63** | 10,277 | **21** | 13 |
| pre-commit (my tree, 22 m 15 s) | 64 | 10,353 | 21 | **14** |
| **post-commit — BINDING** (21 m 46 s) | **63** | **10,354** | **21** | **13** |

**Post-commit: EXACT match on failures (63 = 63) and errors (21 = 21). ZERO NOVEL FAILURE FILES.**
`+77` passing (41 new locomotion tests, the rewritten beat-3 tests, and star-lord's baton additions
that landed underneath me).

**⚑ THE PRE-COMMIT RUN HAD EXACTLY ONE NOVEL FAILURE FILE, AND I AM REPORTING IT RATHER THAN ONLY
THE CLEAN RUN, BECAUSE THE MECHANISM IS INSTRUCTIVE.**
`tests/test_kitcal_g5_harness.py::test_G5_W1_untracked_loaded_source_is_invisible_until_it_is_imported`
— **F-11's exact mechanism** (*"`code-surface-v1` grades this repo dirty by construction"*, star-lord
Phase-D, folded L-42). The test forces `git status` clean so that any `-dirty` can only come from the
**untracked-loaded-source** branch, then asserts a bare hash with nothing planted. My own
**untracked-but-imported `locomotion.py`** was the planted source: by the time the census reached that
test, an earlier test had imported it.

It was **reproduced deterministically** (`pytest tests/test_kc2_locomotion.py tests/test_kitcal_g5_harness.py`
→ 1 failed, and the same pair passes 72/72 after the commit), so the attribution is a measurement
rather than an inference. **The detector was working correctly**; the failure was a tree-state
artifact whose sole cause was that the commit had not happened yet, and it is **resolved BY the
commit**. I did not treat that as licence to skip the gate: the post-commit census above is the
binding one, run on the state that actually ships.

**Concurrency note, because it affects attribution.** star-lord and drax were editing `export/` in the
same working tree during this lap; their work landed as `28b578fe` + `265069b1` mid-run and my base
moved `13451fdf` → `265069b1`. I staged **only my own files, by name** — nothing under `export/`,
nothing in `tests/test_baton_v1.py`. The 286/286 blast radius (which includes his `test_baton_v1`) was
green against the combined tree.

**Commit:** `a5382e65` on engine `main` — **UNPUSHED**. Sixteen files: 4,922 insertions / 174
deletions. **NOTHING PUSHED, either repo.** The meta-repo lap note is **UNCOMMITTED** — the conductor
folds it.

---

## § 12 — Findings for the conductor

Every item is a judgment call I made under commission, named, with what I did and why, so a veto is
cheap.

**F-L1 — ⚑ PURE CAMP IS NON-TERMINATING UNDER § 10.9a A's OWN CITED CONSTANTS. A finding about the
spec's model, not a defect in the build.**
**27 of band A's 895 DB-cited records carry `ViewDistance = 15.0 m`** (the other 868 carry 80.0).
Under L-A they path to their assigned patrol node — median 18.85 m, **max 30.07 m** from the centroid
— and the gate's first term `|x_a − player| ≤ ViewDistance` then **never opens**. They park at the
node forever; the wave never clears; the run terminates on the tick cap. Measured: **8.7 % of band-A
runs unable to clear, 2.19 % of bodies parked** (368 runs, 4 seeds/wave).
**The mechanism the model omits which would resolve it in-game is `distressCall`**, which § 10.9a C
declares OUT-OF-MODEL and grades *"unsigned — couples, could go either way."* **This lap measures its
absence as SIGNED**: without it, low-`ViewDistance` actors beside dying neighbours never acquire.
**What I did (JC-G9):** completed the policy minimally — `CAMP_THEN_COLLECT`, hold while any actor is
inbound, close on the residual only when none is. Cost measured at **0.95 m mean player path, firing
on 32 of 368 runs**, against beat-3 tours of 88–199 m. Pure `CAMP` stays runnable and both limbs are
reported. **Veto-open**; a conductor who prefers the pure limb gets a 30 %-timeout T-1 table and I
would rather that choice be made on the number than by default.

**F-L2 — ⚑ `PursuitTime`'s SEMANTICS ARE NAMED-ABSENT AND THE TWO READINGS ARE NOT CLOSE.**
§ 10.9a A writes `time_in_pursuit(a) ≤ PursuitTime(a)` and says nothing about what starts, stops or
resets that clock. **(i) LIFETIME BUDGET** — runs from first acquisition, never resets: any actor
whose approach exceeds 10 s parks permanently, and it left **30.4 % of band-A runs unable to clear**
(mean cycle 111 s). **(ii) MEMORY TIMER** — runs only while an *acquired* target is out of
`ViewDistance`, resets on re-acquisition.
**What I did (JC-G10):** declared **(ii)**. It is the reading the field's own neighbourhood supports
(it sits beside `ViewDistance` / `InnerViewDistance` / `MaxYViewDistance`, and `MaxPursuitDistance`
125 m already supplies the spatial leash (i) would duplicate in time), and (i) is **contradicted by
the instrument** — the fixture cleared all 92 waves in 7.03–82.13 s. **(i) remains runnable**
(`pursuit_time_is_lifetime_budget=True`) and its cost is asserted by test, so the declaration is
falsifiable rather than convenient. **Conductor's call.**

**F-L3 — ⚑ THE RESIDUAL IS LOCALISED IN AN UNMEASURED SPEC CONSTANT (§ 6).** The 3.0 s p05
intra-drip cadence carries the entire band-A delta; it is ADOPTED, not measured (L-21), and it was
inert under the static board. **I did not touch it.** Routed as a finding, with the note that it is
now falsifiable: a galadriel re-read targeted at intra-drip spacing on a high-p05 s1 wave decides it.

**F-L4 — the K region is EMPTY and the JC-7 consequence is VIOLATED by 2.31 s** (§ 3). Calibration
halted; `v_ref` unchanged; four spec candidates carried, one of mine named-not-adopted.

**F-L5 — MO-5's observer was running the WRONG SITTING** (§ 4.1). Its pin is s1 (waves 47/8/81) and
the observer read the s2 arena — a latent L-21 pooling that only became visible when the geometry
stopped being one shared float. Corrected in-seam; reported because it is a **grade** correction to
a § 12 row's *derivation*, not to its pin.

**F-L6 — `sm_mod` CARRIES NO p01 GEOMETRY ABOVE TIER 15** (JC-G8). `sm_mod` has p01 tiers 1–15;
`sm1` and `sm2` have 1–17. The s2 band is tier 16, so **`sm_mod/survivalworld_a` cannot express the
s2 band at all** and the archive limb is **forced by geometry availability, not chosen by fit**. It
is also the microprobe's own runner-up (8.7° vs 6.0°). Any future lap needing tier 16–17 geometry is
confined to the `sm1` / `sm2` limbs. Recorded because a silent archive switch mid-band would be
undetectable.

**F-L7 — the band-A locomotion join is 895 of 896** (JC-G0). `records/creatures/enemies/hero/
scavenger_h075.dbr` is absent from the emission and takes a DECLARED modal fallback
(`characterRunSpeed` 1.000 — the band's median AND mode; gate at the 868/895 modal values). Counted
at runtime and reported; never silent.

**F-L8 — L-46(a)'s STATED REASON is not supported by the measurement** (§ 8.3). The ruling adopted
L-A as *"the less body-count-coupled shape"*; measured, the two limbs' `r(sim, N)` differ by 0.005
and L-A is marginally the *more* coupled. JC-2 predicted exactly this. **The ruled default stands**;
its justification should not be carried forward as demonstrated.

**F-L9 — the ×10 inversion SURVIVED and RE-ATTRIBUTED.** Beat 3 attributed it to the body-count
model. Under motion the body-count coupling fell 30 % and the inversion barely moved (0.86× →
0.905×). Its remaining cause is the **other** named absence: ×10 waves carry fewer bodies with more
HP each, and band-A eHP is a declared zero (C-1). With no kill term a wave of few tough bodies
**must** be cheaper — arithmetic, not locomotion. **C-1 is now the load-bearing open item for T-1.**

**F-L10 — R-LOCO-1 / R-LOCO-2 CLOSED IN PARALLEL BY star-lord, COUNTER-SIGNED BY drax. I touched no
`export/`, and the two seams converged independently — which is the part worth recording.**
While this lap ran, `28b578fe` (star-lord) + `265069b1` (drax counter-sign) landed **Option-1
waypoints** (`actors[].path[]` + `path_model: "PIECEWISE-LINEAR"`), `arena_ref` over the cited
enumeration with `arena_archive` **required**, `positions_provenance` retyped to the two-layer object,
and `D-ARENA-DECLARED` → `D-ARENA-CITED`. My base moved from `13451fdf` to `265069b1` mid-lap.

**Two independent convergences, neither coordinated:**
1. **The `spawn_t_s` rename.** His `baton_v1_emitter` derives `ac.spawn_t_s` from `spawn_tick`; my
   `actors[]` renamed `arrive_t_s` → `spawn_t_s` for the same reason, in the same lap, without
   contact. The semantic shift § 12/1 names was reached from both sides.
2. **`arena_archive` is load-bearing.** He measured the map name under-determining the geometry by
   **36 %** on the very arena declared for s1; I hit the same edge from the other direction —
   `sm_mod` carries **no p01 geometry above tier 15**, so the s2 band cannot be expressed on that
   limb at all (F-L6). Two different measurements, one conclusion: **the archive is not optional.**

**What I can offer his `actors[].path[]` supplier, stated as an offer and not a claim:**
`KC2Run.movers[]` carries the full per-tick trajectory and, more usefully, the three points a
piecewise-linear reduction actually needs — `spawn_xy`, `node_xy` (or `None` for an ambush spawn),
and the position at `contact_t_s` / `engage_t_s`. His waypoint cost measurement (357 B/actor against
a routed premise of "tens") is against his own fixture; a sim-sourced path would carry **3–4 nodes
per actor** under the L-A motion law, because that is how many segments the law has. **His seam, his
call** — I am naming the supplier, not proposing the schema.

**Still open on his side, re-flagged so it does not age out:** nothing from beat 3 that I can see —
`28b578fe` also landed R-4's p06 rider on both sides, which closes the `fixture_p06_state` flag I
filed at beat 3.

---

## § 13 — § 10.9a C omissions, restated as omissions

| input | extent | sign |
|---|---|---|
| `characterRunSpeedJitter` | n = 810, median 15.0, mean 12.21, max 50.0 | unsigned (dispersion) — **arrival is a distribution, not a time**; the lap ran point-speed and folded nothing into `v_ref` |
| the `ControllerMonster` surface | 126 records × 27 fields: roam, patrol-idle 1–5 s, `EmoteBeforePursuingChance`, swing pauses | **+ LATER** |
| `walkDistance` | n = 677, median 4.5 m; `walkSpeed` median 1.000 | **+ LATER** |
| `distressCall` / range / time | per record | unsigned as declared — **measured SIGNED this lap** (F-L1) |
| patrol-node assignment | 173 nodes; rule in no pin | DECLARED nearest-node (JC-G4); the run records which ran |
| collision / occlusion | none in the read set | OPEN-PLANE, DECLARED (M-10) |
| F-13 residual on N | trash limb INCOMPLETE | reported as N-sensitivity (§ 8.4); the result **inherits** it |

---

## § 14 — Scope held

**Did NOT touch:** `export/` · `telemetry/` · `output/` · `generation/` · `element/` · `anchor/` ·
`foundation/` · the GD corpus · the count model · `ArrayLookupLaw` · F-9 · F-10 · AC-10.4 · the
exemption sidecar · `decisions-log.md` · `canonical/`.

**Did NOT do:** calibrate `v_ref` (region EMPTY — halted; swept only as a declared negative control) ·
re-pin T-1, MO-5, or any § 12 row · widen or average any tolerance · edit the p05 cadence to close a
residual · fold the C-row latency terms into `A` · adopt a `distressCall` model · resolve R-LOCO-1 ·
run the full ladder (beat 5 stays paused).

**Carried open, unchanged:** C-1 (band-A eHP — now the load-bearing item) · E-6 / HALT-4 (PARTIAL) ·
HALT-7 · C-5 (T-1's tolerance vs the process's own variance — **softened**, sd 3.22 → 1.72 s, but
still 1.7× the two-sided band against a single measured draw) · F-13's `+1` branch · legolas's r3.

---

**Filed:** gamora, 2026-08-08, KC2-SIM Phase D — the locomotion lap. **This note is UNCOMMITTED —
the conductor folds it.** Engine-side commit + census: § 11.1. **NOTHING PUSHED, either repo.**
Gate-2 REQUIRED and NOT self-cleared.
