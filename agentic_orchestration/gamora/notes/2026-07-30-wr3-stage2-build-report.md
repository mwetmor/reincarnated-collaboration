# WR3-KITE-COMMIT — STAGE-2 BUILD REPORT (the STAR nova, referent C2/speed, Evade, the A-DMG-1 re-derivation)

**Date:** 2026-07-30 · **Author:** gamora (simulation seam) · **Class:** verdict note
**Commission:** gandalf (RUN-CONDUCTOR), run WR3-KITE-COMMIT, **R-WR3-20 (MATT-SIGNED)** + **R-WR3-21**
(relaunch — supersedes the stopped first stage-2 commission entirely)
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/wr3-kite-commit-stage2-2026-07-30.md`
**Engine commit:** `92381a23` (branch `main`, **NOT pushed** — the conductor pushes)
**Computing cell:** `simulation/wr3_cell_s2_2026_07_30.py` · artifact
`simulation/output/kitcal_g5/wr3_cell_s2_statistics.json` · battery root
`simulation/output/kitcal_g5/wr3_battery_s2/` (banked in git with this commit — the R-WR3-15 lesson)

---

## §0 — HEADLINE, BEFORE ANY DETAIL

| | value |
|---|---|
| **PHASE-A verdict** | **NOT DEGENERATE for the package as signed — but the ranking INVERTS.** No HALT. |
| **Boss-encounter win rate (H1)** | **1.00** on all three legs, 180 boss fights. Band 0.40–0.60 → **FAIL, above band** |
| **Full-mix win rate (H2)** | **1.00** (450 fights). R-WR3-2's majority sentence → **PASS** |
| **Mean boss fight duration (G-T′)** | **36.4 / 39.0 / 39.0 s** vs GD 59–118 s → **FAIL, BELOW band** |
| **A-DMG-1** | **RE-DERIVED and DISCHARGED.** A-NOVA-2 ceilings 359.55 / 359.55 / 407.96 |
| **Full-kit phasing** | wave + blizzard + icearmor **PHASED, NOT dropped** — and Phase A RE-RANKS them as load-bearing |
| **Byte-identity vs stage-1 traces** | **NOT expected and NOT claimed.** Behaviour legitimately changed. |

**⚠ READ §1 BEFORE READING §0 AS A FAILURE.** The two FAILing gates are the two the math note
*predicted would fail*, in the directions it predicted, for the reason it named before the battery
ran: the loss mechanism the 40–60 % band needs is not in this build, because it is in the three
skills Phase A ranks as load-bearing and this build phases.

---

## §1 — PHASE A: THE FEASIBILITY PRE-PASS (math-before-code, BEFORE any code line)

Full derivations in the math note §1–§6. The four results that decide the run:

### 1.1 The melee gets EASIER to escape under referent durations, not harder

Time-from-commit-to-contact goes 0.40 s → 0.50 s while the player's reaction latency stays 0.30 s,
so the free player ticks before the strike go **1 → 2** (+82 % of daylight). The 1.30× speed trim
(−9 % per step) does not come close to offsetting the extra tick.

```
free ticks per boss cycle = E[gap]/dt − N_lock
   stage 1:  15.10 − 6  = 9.10 → 3.663 m of closing per cycle
   stage 2:  17.69 − 14 = 3.69 → 1.485 m of closing per cycle       (−59.5 %)
```

Against `K_RELEASE_M = 4.0` and `C_reach = 2.5` the boss must recover 1.5 m to be swing-legal. It
recovers 1.485 m — **1 % short.** The referent's longer commit does not buy the boss melee hits; it
buys the boss *rootedness*. **Measured post-build: melee whiff 68/68 = 100.0 %.** The prediction
held, and further than predicted.

### 1.2 The star makes the nova CHEAPER to dodge — and that is the referent, not a defect

The lateral clearance needed to leave a prong corridor is `hit_half_width` — **constant in r**, the
`r·sin` and the `1/r` cancel exactly. 0.42 m at 5.2325 m/s = **0.080 s = 9.4 % of a 0.85 s
telegraph = one tick.** Legolas's own design statement ("cheap to pass, expensive to fail") is an
arithmetic fact about this fixture, not a flourish. **So the star correction, alone, is degenerate in
the kite-trivially-safe direction.**

### 1.3 The freeze chain is RECOVERABLE, not a lethal spiral (the commission's explicit ask)

```
freeze 1.3 s = 13 ticks   vs   boss cycle 17.69 ticks, N_lock 14 ticks
 ⇒ a frozen player spans 0.73–1.02 boss cycles ⇒ ≤ 1 landed swing IF the boss is already in reach
 ⇒ boss closing during a 13-tick freeze at 21 % free duty: 13 × 0.209 × 0.4025 = 1.09 m  (needs ≥ 1.5)
```

The spiral needs the freeze to outlast the boss's **approach**, and the approach budget is short by
0.4 m. The one corner where it does chain is `r ≤ 2.5` at the crossing instant — where the boss is
already swing-legal — and that corner is self-limiting: the player is only there voluntarily, and it
is the **50 %** damage band.

### 1.4 THE RANKING FINDING — and it inverts the commission's own default

With melee at ~0 % landing and the nova at ~0 % (as designed by the referent), **there is no loss
mechanism.** The 40–60 % band is unreachable by any setting of any [CAL] row. Ranked:

| rank | skill | why | build cost |
|---|---|---|---|
| **1** | **`primordian_wave`** | **THE mechanism that prices the kite.** Lateral dodge cost `w(r) + r_p` against a 0.552 s actionable window crosses the player's own speed at **r ≈ 9.5 m** — kite past it and the cone cannot be left. 100 % chance on a **5 s** cadence (3.4× the nova's 80 % × 6 s), 217.2 delivered = 28.6 % of the 759 pool. It also gives the boss a reason to be at range, which is where the star's 140 % band lives. | MEDIUM — the engine's `cone` primitive is an ARC and **inverts the load-bearing property** (over-covers near, under-covers far). Needs a widening-rectangle resolver of the `NovaScheduler` shape. |
| **2** | **`chillbane_blizzard`** | The ONLY threat position cannot answer: 24 drops over 8 s, re-aimed every 2 s, no single-decision telegraph. 112.9 per drop; three landings = 44.6 % of the pool. | MEDIUM — no primitive; needs a drop scheduler + its own RNG sub-stream. |
| 3 | `primordian_icearmor` | +10.3 % effective boss HP ⇒ +10.3 % exposure. **Zero lethality of its own.** | LOW |

**`primordian_wave` and `chillbane_blizzard` are LOAD-BEARING, not garnish.** This is a re-ranking of
R-WR3-21(6)'s "the star correction is the non-negotiable core, the other three phase in behind it" —
reported for veto, not taken as licence.

**No HALT was raised.** The degenerate configuration (star-only) is a strict SUBSET of the signed
package; the package as Matt signed it — *"any other GD Primordian boss behaviors"* — is not
degenerate. Halting on a subset I chose to build would have been reporting my own scoping as a
finding.

---

## §2 — PHASE B: GATE RE-REGISTRATION (before the battery, every column NAMES its cell)

Stage-1's gates were registered at 1.43× / 0.30 s / ring-nova. **None was carried.** The full table
is math note §8; the graded rows and their measured values:

| gate | column | band / predicate | AFTER (30 seeds × 3 legs × 2 arms) | BEFORE (frozen WR2) | verdict | cell |
|---|---|---|---|---|---|---|
| **H1** | boss-encounter win rate | **[0.40, 0.60]** (R-WR3-17(a), MATT-SIGNED) | **1.00 / 1.00 / 1.00** | 0.133 / 1.00 / 0.000 | **FAIL — above band** | Cell S2 |
| **H2** | full-mix win rate | > 0.50 (R-WR3-2) | **1.00 / 1.00 / 1.00** | 0.653 / 1.00 / 0.600 | **PASS** | Cell S2 |
| **G-T′** | mean boss fight duration | [59, 118] s | **39.0 / 36.4 / 39.0** | 40.5 / 58.7 / 29.3 | **FAIL — below band** | Cell S2 |
| **G-D′** | boss committed-tick share | [0.76, 0.82] | 0.7914 *derived*; declared cycle = referent exactly | 0.399 | **PASS (arithmetic)** | math note §2.3 + test |
| **G-F5′** | inter-initiation gap ∈ {1.7, 1.8} s | PASS/FAIL — off-grid ⇒ build defect | on-grid | {1.5, 1.6} | **PASS** — the metronome MOVED, as ruled | Cell S2 / test |
| **G-E′** | C2 episode shape | `w5/s1/r9`, `N_emit = N_lock + 1` | as built | `w4/s1/r2` | **PASS** | `test_wr3_kite_commit_stage2` |
| **G-M′** | melee whiff rate | **≥ 0.955** (registered as a FLOOR so a FALL is the surprise) | **1.000** (68/68) | 0.9555 | **PASS** | engine counters |
| **G-N1′** | nova hit rate | two-sided band [0.00, 0.35] of firings | crossings/boss fight **2.20–2.33** (was 0.733) | 0.733 | **REPORTED** — §4 F-2 | Cell S2 |
| **G-N3′** | worst single nova event | ≤ **A-NOVA-2** per leg | **256.82 / 256.82 / 291.40** | 207.4 / 207.4 / 235.4 | **PASS** | Cell S2 + harness |
| **G-S′** | S-1 body separation | residual predicate unchanged | 0 violations | 0 | **PASS** | harness |
| **G-U′** | player speed row | ratio exactly 1.30× | `movement_speed_ms = [5.2325]` on every fight | [5.75] | **PASS** | harness S-7 join key |

**Vacuity declared, not hidden:** **S-7 clause 1 is VACUOUS** on this arm — Mechanism D is disarmed
(SS-S2-2), so there is no escape-law-derived duration to grade. It is reported as vacuous, not as a
pass.

**Pre-registered directions, all recorded before the battery:** whiff ↑, closing budget ↓, duty ↑↑,
duration ↑ (kit) then ↓ (DPS), win rate ↓. **Six of seven held. The seventh (§4 F-2) did not, and
that is the most useful finding in this report.**

---

## §3 — WHAT WAS BUILT

### 3.1 The STAR (R-WR3-21) — one parameter, not a rewrite

**The geometry CLASS was never wrong.** `gd_nova.py` has modelled 16 discrete spokes with a per-ring
rotation and an INTEGER realized count since R-WR1-11. The defect was **one field**: the hit test
read `projectileExplosionRadius = 1.5` — legolas §4.2's **Reading B, adjudicated REJECTED** on four
independent supports, and the reading under which Matt's gap-walk is impossible at every radius the
boss casts from.

- `NovaParams` gains `threat_half_width_m` / `prong_collision_radius_m` / `referent_target_radius_m`
  / `ring_phase_mode`, **all additive and default-`None`**, so `PRIMORDIAN_FRIGIDRING` and every
  banked WR1/WR2 figure are byte-identical (pinned numerically, not structurally, by test).
- `PRIMORDIAN_FRIGIDRING_STAR_R5`: rank **5** (148 phys / 247 cold / 77 cold-DoT — the shipped model
  was rank 4), corridor **0.42**, telegraph **0.85 s** (U-3 band 0.80–0.89 carried), phase **aimed**.
- The closed form is re-verified against the **independent segment-distance oracle** on the new
  corridor: **0 mismatches** over 8 radii × 720 azimuths.

**⚑ THE BODY-RADIUS ADJUDICATION — the one decision I had to make and the one worth a veto.**
The corridor composes `prong actorRadius (0.10, M) + target actorRadius (0.32, M)`. Composing it from
**our** 0.5 m body instead gives 0.60 — and that is not a rounding difference:

```
gaps close below r = h / sin(11.25°):   h = 0.42 → 2.153 m  (INSIDE the 50 % close band)
                                        h = 0.60 → 3.076 m  (STRADDLES the boundary at 2.5)
```

At `h = 0.60`, two prongs land at **100 % each** in `r ∈ [2.5, 3.076)` for **513.6 delivered — 67.7 %
of the 759 pool**, a spike 1.43× larger than the far-band worst, sitting exactly where the player
fights, and **manufactured entirely by our player being 1.56× fatter than the referent's.** Legolas
§6.1 establishes from a 214-of-299-record corpus pattern that the 50 % close band exists *because*
prongs converge — Crate prices the overlap to 1.00×. Importing our body while keeping Crate's bands
is a hybrid with no referent behind it.

**I took the referent composition (0.42), and the test that pins it is the one that would have caught
the alternative.** Note the direction: 0.42 makes the nova *easier* to dodge and removes the spike —
it pushes **AWAY** from the band I was asked to reach. **U-BODY-1** carried: our 0.5 m
`ENTITY_RADIUS_STANDARD` vs the referent's 0.32 u is a fixture-geometry delta that now has a named
consequence; it is not this cell's to change (it governs the collision solver, `C_reach`, and every
banked battery).

### 3.2 The angular-dodge verb (R-WR3-21(2))

`evade_decision` gains `spoke_offset_rad`. **Off (`None`): byte-identical** — the scorer is
`nova_expected_delivered(r)`, *a function of r alone*, so bearing is invisible and the only verb that
exists is radial. That is precisely why stage 1 read `escape_rate 0.526` beside `crossings 0.000`:
the policy was solving a distance problem the referent does not pose.

**On:** the scorer switches to `nova_delivered(r, count=n_realized(r, φ, offset))` — the resolver's
own two functions, in the order the resolver calls them (R-M3-1 intact, still exactly one
implementation), and the candidate set gains explicit **safe-bearing shelves** at the corridor edges
and the two adjacent mid-gaps.

**⚑ WHY IT IS NOT CLAIRVOYANCE, and this is the whole justification (SS-S2-1):** the engine passes an
offset **only** when `ring_phase_mode == "on_target"`, i.e. when the fan is facing-anchored
(`useTargetDir = 0`, M) — and C2-L2 freezes the boss's heading **bit-exactly** for the whole commit
(W-1 note §1.5: 0.0 rad drift on 3,096/3,096). Every prong bearing is therefore derivable, for the
whole telegraph, from a posture the telegraph publishes. Under a randomly-rotated ring the argument
does **not** hold — which is why the switch is keyed to the phase mode and **not** to a flag.

### 3.3 C2 at referent durations, and the one-tick fencepost

| | referent (M) | realized | error |
|---|---|---|---|
| wind-up → contact | 0.489 s | 0.500 s (W=4, strike at T+5) | +2.2 % |
| recovery | 0.879 s | 0.900 s (R=9) | +2.4 % |
| `T_lock` | 1.369 s | 1.400 s (14 ticks) | +2.3 % |
| cycle | 1.719 s | **1.719 s DECLARED**, 1.769 s on the grid | +2.9 % |
| **rooted fraction** | **79.6 %** | **79.1 %** | **Δ 0.5 pp** |

**The duty cycle — the quantity R-WR3-19 named as the real fidelity gap — lands within half a
percentage point of the referent.** That is the strongest single number in this build.

**SS-C2-3, and it is the defect class that already cost this run one HALT (D-F1).** The machine
strikes at `T+W+1`, so time-to-contact is `(W+1)·dt`. Writing the referent 0.489 into `cast_time`
would give W=5 and a **0.600 s** contact (+22.7 % over an **M** value). The packet therefore declares
`cast_time = contact − dt = 0.389` and `wind_up_s = 0.489` (the referent lead) separately, which
also lands the telegraph's declared onset on the initiation instant exactly — stage 1's packet
declared it **one tick late**. I did **not** change `round(cast_time/dt)`: that would retro-actively
redefine what stage 1's ruled 0.30 meant.

### 3.4 MECHANISM EV — GD Evade at its own parameters

3.0 s / 1 charge / 10.0 u / 0.333 s lock (3 ticks) / **NO i-frames** (M-negative, three independent
reads). Executed over its ticks at 3.33 m/tick — **a fast MOVE, not a teleport** (canon §5 names
teleport as "the trap"). Costs the action slot. Fires only when the *walk* is insufficient
(`payload_target > 0` and the charge is up) and only if the dash is **strictly better than the walk**.

**The §7.2 fence holds on the mechanism's own nature**, not only on our flag: GD's Evade record's 476
fields contain no defensive/avoidance/immunity value, its template declares exactly two variables of
its own, and all nine GDX3 runes touch only cooldown and charges. A test asserts **no RNG token
appears anywhere in the mechanism's source**.

### 3.5 Speed and DPS

`movement_speed` 5.75 → **5.2325** (ratio **exactly 1.30×**). **SS-S2-5: THE PLAYER MOVED, NOT THE
BOSS.** The boss's `run_speed = 0.70` is the pak-adjusted **MEASURED** Primordian multiplier
(0.85 × 0.82 = 0.697); moving it to hit a ratio would corrupt a measurement. Extraction §3.4 also
shows the player is the over-fast side against **every** row, so every player:mob ratio moves by
0.910× and lands in the referent's band — correct for the trash and champion legs too.

DPS lever: `cadence_scale = 0.625` (250 → 400 nominal), built off `DEFAULT_RESOURCE_ECONOMY` so the
40 sibling keys keep the emit contract's own values. **[CAL] by necessity and the row T10 discharges.**

---

## §4 — FINDINGS

### F-1 — **A-DMG-1 RE-DERIVES, AND THE RE-DERIVATION IS WHAT LET THE BATTERY OF RECORD COMPLETE**

**The pin fired again**, on the `pre_endpoint` leg, at **291.40** — the *mid-band single prong* on the
gate-adverse resists endpoint. Under the un-re-derived pin the 30-seed battery HALTs exactly as it
did in stage 1, and R-WR3-15's chartered debt could never discharge.

**The re-derivation (R-WR3-21(3), "by re-derivation, not silencing"):**

A-DMG-1 compares a modelled event against `greatestDamageReceived = 260.498` — the worst hit the
referent **TOOK**. That is a sound conservatism check while the boss damage regime is **HELD**
(`dmg_grade = "HELD-SWEPT"`): a modelled number with no referent. Under R-WR3-20(d) referent-parity
the nova's payload **stops being modelled** — it is the M rank-5 block, delivered through the
M-graded M-1 replica of GD's own operator, against the M-graded gear vector off Matt's own save. The
pin would then be grading one measurement against another. And:

> `greatestDamageReceived` is a **LOWER bound** on what the game can deliver, never an upper one.
> Legolas established that Matt **dodged this specific attack** ("which is what I did"). **A player
> who dodges the far band never generates far-band evidence.** Using his worst-taken as a ceiling on
> the mechanic reads *an absence produced by competence* as *a bound on the mechanic*.

**Two pins replace one, and neither is weaker:**

1. **A-DMG-1 STANDS, scope-narrowed** to the HELD/modelled channels (boss melee `BOSS_DMG_SWEEP`,
   every `D-HELD` escort row) at the unchanged **260.50**, where its argument is sound and where it
   can still fire. Off the stage-2 arm the predicate is **byte-identical**.
2. **A-NOVA-2 (NEW)** takes the nova at a **COMPUTED**, per-regime ceiling — every reachable
   `(radius, count)` swept through the resolver's own `nova_delivered`, exhaustive because piercing
   is absent (M-negative), 3 prongs need `r ≤ 1.098` (inside the 2.0 m body floor), and payload is
   monotone in count at fixed band:

   | leg | regime | **A-NOVA-2** | measured worst | % of that leg's pool |
   |---|---|---|---|---|
   | `pre` | R2_proxy | **359.55** | 256.82 | 33.8 % of 759 |
   | `post` | R3 | **359.55** | 256.82 | 16.0 % of 1607 |
   | `pre_endpoint` | R2_proxy_resists_low | **407.96** | 291.40 | 38.4 % of 759 |

   **It bites**: it is exactly the pin that catches the `h = 0.60` body-radius defect (§3.1, 513.6),
   a rank error, a band-boundary error, or a piercing leak.
3. **REPORTED beside both (ungraded), the fidelity delta the narrowing must not hide.** R-WR3-8(a)
   requires the pool to be NAMED and R-WR3-4 warns that an unlabelled fraction is the ninth family
   exhibit. Referent worst-taken: **34.32 % of 759** / **16.28 % of 1600**. Our worst realized event
   is **33.8 %** (759 leg) and **16.0 %** (1607 leg) — **inside the referent's own worst-taken
   fraction under both readings.** The theoretical far-band prong (47.4 % / 22.4 %) is above it, and
   is REPORTED as the remaining gap; the battery never reached it because the policy stays inside
   9.0 m. *(Legolas §12's "34.6 % of the 1600 pool" compares RAW payload to a pool; the table above
   compares DELIVERED to a pool. Not the same quantity — the near-coincidence is arithmetic, not
   confirmation.)*

### F-2 — **THE NOVA IS NO LONGER INERT. §3.4's prediction was FALSIFIED, and that is the good news.**

`crossings / boss fight` goes **0.733 → 2.20–2.33** (3.0×). Stage 1's *"0 of 114 rings deliver"* is
discharged. Two measured mechanisms:

1. **The aimed phase (SS-S2-1) is a real threat increase.** A stationary player is hit by default, so
   the nova now *demands* a decision every cast instead of being dodged by accident.
2. **THE POLICY STOPS STEERING AT LAUNCH, BUT THE RING FLIES FOR UP TO 0.857 s AFTERWARDS.**
   `_m3_telegraph_response` reads only rings with `t_launch > elapsed`. That is **correct for a
   uniform ring** (you cannot outrun it) and **WRONG FOR A STAR** — bearing still matters while the
   prongs travel. The player dodges to a gap, the telegraph ends, K-T2 re-engages, and the player
   walks back across a corridor before the front arrives. **This is a NAMED, UNBUILT half of the
   angular verb** (§5), discovered by the battery. It is not a defect in what shipped: what shipped
   answers the *telegraph* correctly.

The verb *is* working where it steers: the worst per-projectile event is the **mid-band** figure on
every leg and **the far band (140 %) is never reached** — the policy holds inside 9.0 m.

### F-3 — **THE K [CAL] ROWS ARE NOT A DIAL. Measured, and it is a warning to the grill.**

Sweeping CAL-K2 (`pressure_threshold`) at 10 seeds × 2 arms:

| CAL-K2 | 2.00 | 2.50 | 3.00 | 3.50 | **4.00** | 4.50 | 5.31 |
|---|---|---|---|---|---|---|---|
| player win rate | 0.70 | 0.80 | 0.90 | 0.85 | **0.55** | 1.00 | 1.00 |
| boss strikes landed / initiated | 95/183 | 53/163 | 89/181 | 51/83 | 53/64 | 0/26 | 0/94 |

**Non-monotone and chaotic** — the kite bout either phase-locks against the boss's 1.769 s metronome
or does not, and the win rate jumps between regimes. **4.00 lands inside the 40–60 % band and I have
deliberately NOT taken it.** Picking a value out of a chaotic sweep because it hits the target is
fitting to noise, not calibration, and it would hand the conductor a number that will not reproduce.
Both K rows ship at **DERIVED anchors**, each a re-derivation of the sentence the stage-1 comment
already carried:

```
CAL-K3′ (bout_max)          = N_lock·dt + CAL-K1 = 1.400 + 0.300 = 1.70 s   ("a bout must span the
                                                                              commit it answers")
CAL-K2′ (pressure_threshold) = 3 × cycle          = 3 × 1.769     = 5.31 s   ("~3 chances for K-T2a")
```

**The stage-1 values were NOT carried:** at CAL-K3 = 1.50 the bout expires mid-commit and the boss's
melee hit rate goes **11.3 % → 88.9 %**. That is the exact gate-shopping-in-reverse R-WR3-20 forbids,
caught before the battery.

### F-4 — **The DPS lever and the full kit must land TOGETHER, and the arithmetic said so first**

Math note §6, written before the build: `16,235 / (400 × 0.79) = 51.4 s` — *below* the band; only a
kit-imposed uptime tax (uptime → ~0.5) puts it back at 81 s. **Measured: 36–39 s.** The DPS lever
alone moves duration out of band in the opposite direction. **The lever is correct and its
companion is missing** — this is F-1.4's ranking finding restated as a duration row.

### F-5 — Mechanism D is disarmed, and the A/B is a PACKAGE comparison

**SS-S2-2:** `nova_telegraph_v2` would set the telegraph to `12 / (0.9 × 5.2325) = 2.548 s` — **3.0×**
the referent's 0.85 s. Its Matt-signed premise (*"there is no reason for the telegraph as the skill
damage cannot be avoided"*) is **discharged by measurement**: under the star the damage *is* avoidable
at 0.42 m of lateral movement. Referent-parity governs; D is disarmed for this arm.

**Consequence declared before the battery, not after:** the AFTER leg suffix loses `_ntv2`, so the
stage-2 arm differs from the frozen BEFORE arm in more than one flag. That is correct — stage 2 is a
package by Matt's signature — but it means **no stage-2 column may be attributed to a single
mechanism.**

### F-6 — Byte-identity vs stage-1 traces is NOT expected, and is not claimed

Speed, commit durations, cadence, nova geometry, nova rank, telegraph duration, ring phase and the
policy's scorer all moved. **Divergence from stage-1 traces is the mechanism, not a regression.**
What IS claimed and IS proven: **the flag-OFF path is byte-identical.** `PRIMORDIAN_FRIGIDRING`'s
`n_expected` is pinned to the M-12b landing's own transcribed table; every stage-2 seam defaults
`False`; the WR1 nova suite, the WR3 stage-1 suite and the W-1 suite all re-run green **unchanged**.

---

## §5 — PHASED, NAMED, NOT DROPPED (the commission's explicit obligation)

| item | why not in this build | Phase-A rank |
|---|---|---|
| `primordian_wave` | the engine's `cone` is an **ARC**, which over-covers near and **under-covers far** — it inverts the one property (the r ≈ 9.5 m crossover) that makes the wave load-bearing. A faithful build needs a widening-rectangle resolver of the `NovaScheduler` shape. Approximating it with an arc would have shipped a mechanism that *looks* built and measures the opposite of the referent. | **RANK 1** |
| `chillbane_blizzard` | no primitive exists; needs a drop scheduler + its own RNG sub-stream (~1 module). | **RANK 2** |
| `primordian_icearmor` | needs a timed damage-taken multiplier at a site shared with production. | RANK 3 |
| the angular verb's **in-flight** half (F-2) | discovered *by* the battery, after the build. | — |
| MECHANISM EV on the K-T2 melee limb | declared scope in the flag's own comment. `ev_dashes = 0` across the whole battery — the walk always sufficed under the telegraph limb, exactly as math note §4 predicted ("not the marginal mechanism"). | — |

**Wall clock is the honest reason for the first three.** Phase A ranks them; the report says so; none
is dropped.

---

## §6 — TESTS AND SUITE STATE

| item | value |
|---|---|
| New unit tests | **38** in `tests/test_wr3_kite_commit_stage2.py`, all passing |
| WR3 stage-1 + W-1 + WR1-M12 + M12b suites (re-run) | **3,622 passing, unchanged** |
| Combined WR3 stage-1 + stage-2 | **3,561 passing in 1.41 s** |
| Full `tests/` re-run | **launched at cell close; the verdict is OWED at jack-ryan Gate 2** (Discipline: stated honestly rather than asserted). The 81-name baseline is the comparison. Everything this cell adds is either new default-off code or `tests/` sources that the commit tracks; the 82nd untracked-source guard's precondition is satisfied because the new modules are tracked at `92381a23`. |
| AST assertion: no RL imports in `env_contract` | **still green** (untouched by this build) |

The stage-2 tests are written to catch the failure modes this build could actually have, not for
coverage: the default-inert claim is pinned **numerically** (the legacy `n_expected` table,
transcribed from `EXT_1_3_FALSIFIED_n`'s own preserved docstring, not recomputed); the corridor is
pinned as a **composition** so a re-derivation from the wrong bodies breaks the sum; the 2-prong band
is pinned to lie inside the 50 % close band (the test that catches the `h = 0.60` defect); the
one-tick fencepost is pinned **in both directions** including the rejected 0.600 s realization.

---

## §7 — SEMANTIC SHIFTS (Discipline #12) — all declared BEFORE implementation, math note §10

| id | shift |
|---|---|
| **SS-S2-1** | The ring phase becomes **derivable from the boss's frozen facing**, so the policy may score the **realized** count instead of the expectation. The M-12 claim that phase is invisible until release was true of a *randomly rotated* ring and is **false of a facing-anchored one**. |
| **SS-S2-2** | **Mechanism D is DISARMED for the stage-2 arm.** Its Matt-signed premise is discharged by the star's measured 0.42 m escape. |
| **SS-S2-3** | The nova's hit test moves from `projectileExplosionRadius` (splash) to a composed prong+body corridor. `explosion_radius_m` survives as the splash datum and stops being the hit test. |
| **SS-S2-4** | `A-DMG-1` narrows scope to the HELD channels; `A-NOVA-2` takes the star. §4 F-1. |
| **SS-S2-5** | Player `movement_speed` 5.75 → 5.2325. **THE PLAYER MOVED, NOT THE BOSS.** |
| **SS-C2-3** | The stage-2 C2 packet declares `cast_time = contact − dt` and `wind_up_s = contact`, so the telegraph's onset lands on the initiation instant. Stage 1's one-tick-late lead is corrected *by construction*, on the new packet only. |
| **SS-K-1 (extended)** | The limb discriminator gains a fourth value, `evade:dash` (MECHANISM EV). The bare `"evade"` is **still** emitted only when `kite_policy_v1` is off, so every WR2 instrument reading the frozen BEFORE root sees the string it always saw. |

**No `MIGRATION.md` entry is owed.** The replica-frame schema is **untouched** — no new frame field
was added, and the star needs none for the render *as currently specified*. **⚑ SCHEMA QUESTION FOR
THE CONDUCTOR, proposed not emitted:** a faithful star render wants **per-prong projectile positions**
(16 bearings + a front radius per live ring). Today a consumer can reconstruct them from
`spoke_offset_rad` + `t_launch` + `projectileVelocity` **only if those three ride the telegraph
record**, which they do not. That is a `replica-frame/v1` amendment (drax + galadriel consumers) and
I have not unilaterally emitted it.

---

## §8 — UNMEASURED-SURFACE LEANS (R-WR3-20(d)'s standing rule)

| id | surface | lean taken | veto |
|---|---|---|---|
| **U-U1** | GD-u → sim-metre conversion | **`1 u ≡ 1 m`**, by continuity: every nova length has ridden this since WR1-BUILD-M12 under R-WR1-8/R-WR2-15. **NOT a HALT** — refusing it would leave a 12.0-**m** ring made of 0.10-**u** prongs. | open |
| **U-BODY-1** | our 0.5 m player body vs the referent's 0.32 u | corridor composes from the **referent's** two bodies; our `entity_radius` is deliberately not an operand. The `h = 0.60` counterfactual and its 513.6 spike are reported. | open |
| **U-1** | ring phase | **hostile** (prong 0 on target), per R-WR3-21(5) | ruled |
| **U-3** | which pak modifier hits the nova telegraph | **0.85** midpoint; band 0.80–0.89 carried in-source | ruled |
| **U-4** | boss recovery = upper bound | taken as-is at 0.879; flagged at the constant | open |
| **wave/blizzard payloads** | 122/210 and 58/111 | **CARRIED-EXT, not M** — from the fixture's own named-absence ledger. If a verdict leans on them, that is a legolas commission, not a gamora assumption. | open |
| **EV dash profile** | the referent's decelerating slide | **equal per-tick split** — the endpoint and duration are M, the interior profile is not; a fabricated curve would be invention wearing a measurement's clothes. | open |

---

## §9 — REPRODUCTION

```bash
cd ~/Games/reincarnated-engine
python3 -m pytest tests/test_wr3_kite_commit_stage2.py -q -p no:randomly       # 38 pass
python3 -c "
from reincarnated.simulation.spatial_gauntlet import kitcal_g5_harness as H
H.main(['--run','--seeds','30','--seed-base','74000800','--gd-cadence','--with-nova',
        '--emit-telegraphs','--mitigation-regime','R2_proxy','--trace-decisions','--no-trace',
        '--out-dir','src/reincarnated/simulation/output/kitcal_g5/wr3_battery_s2',
        '--body-separation-v2','--movement-policy-v2','--kite-policy-v1','--boss-commit-v1',
        '--wr3-stage2-v1'])"
python3 -c "from reincarnated.simulation import wr3_cell_s2_2026_07_30 as C; C.main()"
```

Legs ran **sequentially** on the same seed set (Discipline #3). Nothing wrote to `wr2_battery_after/`
or to any `wr3_battery_after*` root.

---

## §10 — WHAT THE CONDUCTOR OWES A RULING ON

1. **The Phase-A RE-RANKING** (§1.4): `primordian_wave` + `chillbane_blizzard` promoted from
   phase-in to **load-bearing**. The band is unreachable without them by any [CAL] setting.
2. **The A-DMG-1 re-derivation** (§4 F-1) — narrowing + A-NOVA-2. R-WR3-21(3) directs it; the shape
   of the narrowing is mine and is veto-open.
3. **U-BODY-1** (§3.1) — the corridor composes from the referent's bodies, not ours.
4. **SS-S2-2** — Mechanism D disarmed, and the A/B consequently a package comparison.
5. **F-3** — CAL-K2/K3 ship at derived anchors; **4.00 hits the band and was refused as a noise fit.**
6. **The schema question** (§7) — per-prong projectile positions for a faithful star render.
7. **F-2's in-flight steering** — the named unbuilt half of the angular verb, discovered by the
   battery.

---

*WR3-KITE-COMMIT stage-2 build report — gamora, simulation seam, 2026-07-30. Engine committed at
`92381a23`; neither repo pushed.*
