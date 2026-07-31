# WR3-KITE-COMMIT — STAGE-2b BUILD REPORT (the load-bearing pair, the stage map, and the fix that un-fixed the fight)

**Date:** 2026-07-30 · **Author:** gamora (simulation seam) · **Class:** verdict note
**Commission:** gandalf (RUN-CONDUCTOR), **R-WR3-23** (§10 rulings) + **R-WR3-24** (measured
payloads, the boss-level correction, the damage-stage adjudication mandate)
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/wr3-kite-commit-stage2b-2026-07-30.md`
**Engine commit:** `97d51798` (branch `main`, **NOT pushed** — the conductor pushes)
**Computing cell:** `simulation/wr3_cell_s2b_2026_07_30.py` · artifacts
`simulation/output/kitcal_g5/wr3_cell_s2b_statistics.json`,
`…/wr3_s2b_f2_ablation.json` · battery root `…/wr3_battery_s2b/` · stage sweep
`…/wr3_stagesweep_s2b/` (all banked in git with the commit)

---

## §0 — HEADLINE, BEFORE ANY DETAIL

| | value |
|---|---|
| **A-1 STAGE MAP verdict** | **COINCIDENCE**, and the map is a **PARTITION, not a scalar**. **⚑ HALT RAISED** (both corrections move the nova's delivered regime by 25.0 % / 73.5 %, far past the 15 % predicate). **NOT actioned** — three pre-registered arms, `S0_NONE` default. |
| **A-2 RE-RANK verdict** | **The loss mechanism is NOT wave-first.** Blizzard demoted (centre is fixed), icearmor promoted, wave holds rank 1 on a **different warrant**. My own stage-2 "r ≈ 9.5 m crossover" is **CORRECTED**. |
| **H1 — boss-encounter win rate** | **0.983 / 1.000 / 0.950** vs Matt-signed **[0.40, 0.60]** → **FAIL, above band** |
| **H2 — full-mix win rate** | **0.993 / 1.000 / 0.980** vs > 0.50 → **PASS** (R-WR3-2's acceptance sentence) |
| **G-T′ — mean boss fight duration** | **36.0 / 35.0 / 35.7 s** vs [59, 118] → **FAIL, below band** |
| **G-I1 — icearmor uptime** | **0.342 / 0.347 / 0.344** vs [0.30, 0.42] → **PASS** |
| **Schema fields landed** | `spoke_offset_rad` · `t_launch_s` · `projectile_velocity_ms` on the telegraph record; `shape` gains `"rect"`. `replica-frame/v1` stays **v1**. MIGRATION written. |
| **Every OTHER gate** | **PASS** — G-W1, G-B1, G-B2, G-F2, G-S′, G-U′. None vacuous. |
| **Flag-OFF byte-identity** | **PROVEN**, not asserted: digest `a0c6b5c8f6c8795f` identical to `92381a23` |

**⚑ THE FINDING THAT MATTERS MOST IS NOT IN THAT TABLE.** §5's seed-matched ablation:

| arm (leech 0, boss tier, 30 seeds) | H1 (player win) | verdict | damage taken |
|---|---|---|---|
| stage 2 (no kit, no F-2) | **0.567** | **IN BAND** | 785.6 (103.5 % of pool) |
| **kit only** (F-2 + icearmor OFF) | **0.433** | **IN BAND** | 656.2 (86.5 %) |
| kit + **F-2** + icearmor | 0.933 | out, above | **301.0 (39.7 %)** |

**R-WR3-23(7)'s in-flight steering — commissioned as a fidelity fix — is a large PLAYER BUFF, and
it is the single mechanism that takes this fight out of the Matt-signed band.** Nova crossings go
**2.20–2.33 → 0.133 (−94 %)**. The band is *reachable*. F-2 is what leaves it.

---

## §1 — PHASE A-1: THE STAGE MAP (R-WR3-24(3), BLOCKING)

Full derivation: math note §1–§2. The map, one row per GD stage:

| # | GD stage (grade) | fixture stage | status |
|---|---|---|---|
| 1 | rank-5 damage array (M) | `phys/cold_per_projectile` 148/247 | **MODELLED** |
| 2 | per-element pool rider ×1.06 phys (M) | — | **MISSING** (worth 1.2 %; now built) |
| 3 | pool `offensiveTotalDamageModifier` −65 ⇒ ×0.35 (M) | operand of `tdm_additive_multiplier`, **not applied under Arm P** | **MISSING (graded arm)** |
| 4 | pak `offensiveTotalDamageModifier` −25 ⇒ ×0.75 (M) | same operand, same non-application | **MISSING (graded arm)** |
| 5 | distance bands 50/100/140 % (M) | `band_scale_at` | **MODELLED** |
| 6 | per-prong multiplicity (M) | `n_realized(r, φ, offset)` | **MODELLED** |
| 7 | defender armour (M) | `gd_taken_physical`, M-1 replica | **MODELLED** |
| 8 | defender resists (M) | `gd_taken_elemental` × Matt's gear vector | **MODELLED** |

**NO DOUBLE-COUNT BETWEEN 3/4 AND 7/8.** Stages 3–4 are attacker-side outgoing; 7–8 are
defender-side incoming. They share no operand — `delivered_by_channel` reads only `armour` and
`resists`, neither of which contains `offensiveTotalDamageModifier`.

### 1.1 Convergence or coincidence — **COINCIDENCE**

| outgoing stage | nova mid-band 1 prong | far-band 1 prong | A-NOVA-2 ceiling |
|---|---|---|---|
| **×1.0 — Arm P, SHIPPED** | **256.82** | **359.55** | 1274.11 |
| ×0.75 — `S1_PAK` | 192.62 | 269.66 | 895.67 |
| ×0.2625 — `S2_FULL` | 68.11 | 94.38 | 283.14 |

256.82 is a **pre-damper** number being compared against a **post-damper** measurement (260.498).
They are not the same quantity and their 1.4 % agreement carries no information. The decisive
evidence is §1.2, not this pair.

### 1.2 THE DOUBLE-COUNT, AND WHERE IT ACTUALLY IS

`BOSS_DMG_SWEEP`'s HELD **50.0** is the dead centre of the referent's **post-damper 43.1–60.8**
band (legolas §5, corroborated independently against the envelope's measured 35–85 cross-tier
band). At the delivered layer: fixture `0.30 × 50 = 15.00`; referent `0.30 × (43.1…60.8) =
12.93…18.24`.

**⇒ THE FIXTURE'S TWO BOSS DAMAGE CHANNELS SIT AT OPPOSITE ENDS OF GD'S CHAIN, 3.81× APART.**

```
STAGE MAP, FINAL — A PARTITION, NOT A SCALAR (SS-S2B-3):
  skill-row channels (nova, wave, blizzard)  ->  enter RAW  ->  the stage APPLIES
  default-attack channel (melee)             ->  enters COMPOSED  ->  it DOES NOT
```

A build that took "the ×0.2625 mandate" literally across all four channels would have shipped a
boss whose melee delivers **3.9 HP a swing**. The commissioned reconciliation's answer is a
partition, and this is it.

### 1.3 ⚑ THE HALT, RAISED AND NOT ACTIONED

Both corrections move the nova's delivered regime by **−25.0 %** (`S1_PAK`) and **−73.5 %**
(`S2_FULL`) — far past the commission's 15 % predicate. **I did not re-point the graded regime.**
Instead, following R-M2-1's own pattern, three pre-registered arms ship with `S0_NONE` — today's
behaviour, and the regime every banked WR1/WR2/WR3 figure was measured under — as the default and
the regime of record. Selecting anything else re-bases the entire evidence chain, which is exactly
why it is the conductor's ruling and not this build's.

**The evidence, in BOTH directions, including against the arm I believe is correct:**

- **FOR `S2_FULL`:** §1.2's melee corroboration, from a different record set. The standard GD
  semantics of a character-level `offensiveTotalDamageModifier`. `armorbase0N` is carried by
  **93.4 %** of 1,307 Monster records and cannot be dropped without dropping it game-wide.
- **AGAINST `S2_FULL`:** under it the **entire** Primordian kit's single-event ceiling is 283.14
  and no single prong exceeds 107 — yet the referent's `greatestDamageReceived` is **260.498** and
  `lastHitBy` **273.704** (U-5, open). Under `S1_PAK` the far-band prong is **269.66** and the
  measured worst-taken sits **3.5 % below it**, precisely where R-WR3-23(2)'s "an absence produced
  by competence is a LOWER bound" predicts a dodged far band should sit. *That is a real argument
  and I am not going to pretend it is not.*
- **THE DISCRIMINATOR IS NOT OURS TO SETTLE:** whether 260.498 was a Primordian event at all. The
  run also contains Warden Krieg. That is a legolas question.

### 1.4 A THIRD INSTANCE OF THE SAME BINDING ERROR — in OUR seam

`NovaParams.tdm_additive_multiplier = 0.05` composes from `armorbase05 = **−78**`.
`armorbase05.offensiveTotalDamageModifier = −91 + rank`, so **−78 ⇒ rank 13 — the PLAYER's level.**
Correct binding is the monster's own charLevel **18** ⇒ **−73**.

**This is the identical defect legolas diagnosed in the carried-ext 122/210 and 58/111 arrays, in a
third independent place, found by reading our own constant against his corrected chain.** It
corroborates his diagnosis by a route he did not have. The constant is **not mutated** — it is the
record of what Arm C ran (SS-S2B-4); the corrected operands live on the new stage object.

### 1.5 A-NOVA-2 RE-DERIVED PER ARM, and TWO NEW PINS

| leg / regime | S0 (record) | S1_PAK | S2_FULL |
|---|---|---|---|
| `pre` / R2_proxy | **359.55** | 269.66 | 94.38 |
| `post` / R3 | **359.55** | 269.66 | 94.38 |
| `pre_endpoint` / R2_low | **407.96** | 305.97 | 107.09 |

**⚑ A-DMG-1 FIRED, TRUTHFULLY, ON THE NEW WAVE CHANNEL — and it is the stage map's sharpest
independent datum.** On the first battery attempt, unprompted:

> `A-DMG-1 (HELD channels): a single NON-NOVA received event of **279.82** exceeds the measured
> post-mitigation ceiling **260.5**.`

At `S0_NONE` the wave over-delivers against the referent's worst-taken. At `S1_PAK` it is 209.87
and at `S2_FULL` 74.18 — both comfortably under. **A falsification device that knows nothing about
the stage-map argument pointed at the same conclusion §1.2 reached from the melee channel.**
Reported to the conductor; **not used here to pick an arm.**

Discharged **by re-derivation, not silencing**, in exactly the shape R-WR3-23(2) ratified:

- **A-WAVE-1** and **A-BLIZ-1 (NEW)** — computed per-regime, per-stage single-event ceilings for
  the two M-graded channels (wave 345.32 / 258.99 / 91.37; blizzard 173.61 / 130.21 / 45.93 at
  R2_proxy, each including icearmor's +28 % cold so the ceiling bounds the *worst reachable* event).
- **A-DMG-1 STANDS** at the unchanged 260.50 on the **HELD melee** limb, where its argument is
  sound and where it can still fire.

### 1.6 The boss-level correction (R-WR3-24(2))

charLevel **18** adopted (proxy chain + the envelope's measured `lifeAndMana` anchor at 0.4 %).
**Rank 5 is invariant over 16–19, so no payload array moves.** The corrected level and its
derivation live as a named constant (`PRIMORDIAN_CHAR_LEVEL`) beside the stage map. The fixture's
`OppositionRow.char_level = 13` is a fixture-wide key (HP derivation, escort levels) and is
deliberately **not** re-pointed here.

### 1.7 MELEE GRADUATION — **PROPOSED, NOT ENACTED** (commission item 6)

`BOSS_DMG_SWEEP = (33, 50, 67)` was chosen when no referent existed. **Proposal:** re-centre on the
band's own endpoints and midpoint, **`(43.1, 52.0, 60.8)`**, and move `dmg_grade` from
`HELD-SWEPT` → `M-BAND`; A-DMG-1's HELD melee scope then discharges on the melee limb exactly as it
discharged on the nova limb. **Not enacted** — it moves a HALT-1 charter parameter, and every
banked `D-HELD` escort row invites the same question. Conductor's ruling.

---

## §2 — PHASE A-2: THE RE-RANKING UNDER TRUE MECHANICS

### 2.1 My stage-2 rank-2 premise is DEAD

Stage 2 ranked the blizzard #2 as *"the ONLY threat position cannot answer: 24 drops over 8 s,
**re-aimed every 2 s**."* **Falsified.** `targetingMode = 'Point'` + `groundOnly = True` (M, clean
64-record crosstab): `skillTargetInterval 2.0` is a **volley cadence at the same centre**. Position
CAN answer it by leaving the circle.

Measured landing rate against a *stationary* player at the centre, 400 seeds: **0.6775 drops/cast**
— the math note predicted 0.65–0.82 before the code ran. Against our *moving* policy the battery
measured **0.31–0.33**.

### 2.2 My stage-2 "r ≈ 9.5 m crossover" is WRONG, and I am correcting it

Stage 2 scored the wave dodge against the **0.552 s actionable window alone**, omitting the wave's
**travel time**. The front is visible for `r/11.429` s after release and a competent pilot keeps
moving (legolas computes the same ~1.7 s at the cast range). With travel counted:

```
escape ⟺ v_p (t_release + r/v_front − t_lat) ≥ w(r) + r_p
       ⟺ 2.888 + 0.4578 r ≥ 2.0 + 0.09375 r   ⟺  0.888 + 0.364 r ≥ 0   TRUE FOR ALL r
```

**There is no crossover.** The widening-RECTANGLE resolver is still the right build — an arc
misprices the lane at every radius but the fit points — but the warrant is **faithfulness, not a
crossover**. Under the blizzard's slow the margin collapses to `0.022 + 0.226 r`: still positive,
and **2 cm of it at point-blank**. That is the interaction, and it is why the loss mechanism is
compound.

### 2.3 The loss mechanism is COMPOUND, and it is the freeze

```
nova prong lands → action_lock 1.3 s (OUTLASTS the boss's own 1.369 s melee lock)
a frozen player has v_p = 0 → the escapable wave becomes unescapable
→ the wave's own 30 %/3 s damage-reduction debuff cuts player DPS → the fight lengthens
blizzard's 30 %/5 s slow shortens every escape budget in the loop
icearmor's +35 % aspd and +28 % cold multiply the whole thing for 37.5 % of the fight
```

**Predicted wave hit rate ≈ 0.10. Measured: 0.098 / 0.100 / 0.099.** The pre-registered number
survived contact to two figures.

### 2.4 THE RE-RANKING (amends R-WR3-23(1)'s ratification, on measurement)

| rank | skill | stage-2 rank | why it moved |
|---|---|---|---|
| **1** | `primordian_wave` | 1 | **HOLDS, on a different warrant.** Not "inescapable" — the **largest single payload in the kit** (358.1 delivered incl. DoT at S0, vs the nova's 256.82) and **the only channel the freeze can convert**. Plus the 30 %/3 s damage-reduction debuff, in neither carried-ext nor stage 2. |
| **2** | `primordian_icearmor` | **3 → 2** | **PROMOTED.** "Zero lethality of its own" is falsified: it is a MULTIPLIER ON RANKS 1 AND 3 — +35 % aspd (lock 1.369 → 1.014 s), +28 % cold on a payload row that is 62–64 % cold — up 37.5 % of the fight for a ~1.81 s commit. |
| **3** | `chillbane_blizzard` | **2 → 3** | **DEMOTED as damage** (fixed centre, 0.31 landed drops/cast measured), **retained for the 30 %/5 s slow**, which is the term that makes §2.3's chain fire more often. |

### 2.5 IS THE BAND REACHABLE? — **YES, and §5 names what leaves it**

The math note pre-registered that the stage arm would bracket the band. **That prediction was
WRONG, and usefully so.** Measured on the 30-seed stage sweep (pre leg):

| stage arm | boss-fight player win | duration | boss intake |
|---|---|---|---|
| **S0_NONE** (record) | 0.983 | 36.0 s | 37.5 % maxHP |
| S1_PAK | 1.000 | 36.2 s | 30.5 % |
| S2_FULL | 1.000 | 36.2 s | 16.2 % |

The stage arm moves *intake* by 2.3× and the win rate **not at all** — because under the full kit
**the player never comes close to dying at any arm**. The dial is not the stage. It is §5.

---

## §3 — PHASE B: GATE RE-REGISTRATION (before the battery; every column NAMES its cell)

Math note §9, written before a line of code. Stage 2's gates were registered against a two-skill
boss; **G-M″ is the only one that MOVED** (0.955 → 0.90 floor), and the note says why in advance:
icearmor's +35 % attack speed is the first mechanism in the run that could lower a whiff rate.

| gate | column | band / predicate | AFTER (`pre` / `post` / `pre_endpoint`) | BEFORE (stage 2) | verdict | cell |
|---|---|---|---|---|---|---|
| **H1** | boss-encounter win rate | **[0.40, 0.60]** (R-WR3-17(a), MATT-SIGNED) | **0.983 / 1.000 / 0.950** | 1.00 / 1.00 / 1.00 | **FAIL — above** | Cell S2B |
| **H2** | full-mix win rate | > 0.50 (R-WR3-2) | **0.993 / 1.000 / 0.980** | 1.00 | **PASS** | Cell S2B |
| **G-T′** | mean boss fight duration | [59, 118] s | **36.0 / 35.0 / 35.7** | 39.0 / 36.4 / 39.0 | **FAIL — below** | Cell S2B |
| **G-W1** | wave hit rate | **[0.05, 0.45]** two-sided | **0.098 / 0.100 / 0.099** | n/a | **PASS** | Cell S2B |
| **G-B1** | blizzard drops landed / cast | **[0.0, 0.9]** | **0.321 / 0.328 / 0.311** | n/a | **PASS** | Cell S2B |
| **G-B2** | blizzard slow applications | **> 0** | **43 / 42 / 41** | n/a | **PASS** | Cell S2B |
| **G-I1** | icearmor uptime | **[0.30, 0.42]** | **0.342 / 0.347 / 0.344** | n/a | **PASS** | Cell S2B / engine |
| **G-I2** | boss effective-HP multiplier | ≈ 1.103 REPORTED | 1.1034 (arithmetic) | — | **REPORTED** | math note §6 |
| **G-F2** | in-flight steering events | **> 0** | **667 / 672 / 662** | 0 | **PASS** | Cell S2B |
| **G-N1″** | nova crossings / boss fight | REPORTED, direction ↓ | **0.133** on all three | 2.33 / 2.20 / 2.33 | **REPORTED — direction HELD** | Cell S2B |
| **G-N3″** | worst single event | ≤ A-NOVA-2 / A-WAVE-1 / A-BLIZ-1 per leg per arm | 279.82 / 279.82 / 317.90 | 256.82 / 256.82 / 291.40 | **PASS** (after §1.5's re-derivation) | harness |
| **G-S′** | S-1 collision residual | 0 violations | **0 / 0 / 0** | 0 | **PASS** | harness |
| **G-U′** | player speed row | exactly 1.30× | `[5.2325]` on every fight | [5.2325] | **PASS** | harness S-7 |
| **G-SCH** | telegraph schema | 3 keys present on novas, `null` elsewhere; v1 unchanged | as built | — | **PASS** | `test_wr3_…stage2b` |
| **G-BYTE** | flag-OFF byte identity | digest reproduces | `a0c6b5c8f6c8795f` = HEAD | — | **PASS** | smoke |

**Vacuity declared, not hidden:** **S-7 clause 1 remains VACUOUS** (Mechanism D disarmed,
SS-S2-2). Reported as vacuous, not as a pass — unchanged from stage 2.

**Pre-registered directions recorded before the battery:** H1 ↓, G-T′ ↑, wave hit rate ≈ 0.10,
blizzard ≤ 0.9, icearmor ≈ 0.375, nova crossings ↓. **Five of six held.** The one that did not is
**G-T′ — duration FELL again** — and §5 explains it: F-2 cut the player's damage intake by 62 %, so
nothing slowed the fight down.

---

## §4 — WHAT WAS BUILT

### 4.1 `primordian_wave` — the widening RECTANGLE (not the arc primitive)

Geometry 3.0 → 6.0 u over 16.0 u, depth 1.0, `waveTime` 1.4 s (front 11.4286 m/s), release
0.852 s (band 0.852–0.947 carried in-source as U-WAVE-T, mirroring U-3's treatment), **hits ONCE**
(`skill_attackwave.tpl` declares no tick field — M-negative on the full 281-field dump), 100 % on a
5.0 s cadence, MediumRange ⇒ 9.0 u.

**The dwell is 0.0875 s — SUB-TICK — so the resolver solves band membership as an INTERVAL over the
tick, not at its endpoints.** Same defect class, same fix, as `RingEvent.crossing_time`.

Payload rank 5: **153 phys / 272 cold** (point values; both Max fields are scalar 0.0 — no roll) +
**91 cold DoT over 3.0 s** + **the 30 %/3.0 s damage-reduction debuff**.

**⚑ SS-S2B-5: THE PLAYER GAINS AN OUTGOING-DAMAGE DEBUFF CHANNEL.** No prior mechanism in this
engine reduced player damage output. U-A1's sign is a lean (`offensiveSlow<X>` family convention:
*the target deals 30 % less*), and it is the **conservative** lean — the alternative reading
(*takes 30 % more*) is worth roughly twice as much to the boss.

**Named and NOT modelled:** the sunder clip's root bone swings the cone's ORIGIN up to ~1.4 u
mid-animation (net displacement 0.0). Second-order against a 2.84 m clearance requirement.

### 4.2 `chillbane_blizzard` — the drop scheduler

Centre **FIXED at cast**; 4 volleys × 6 drops over 8.0 s; scatter 8.0 u (adjudicated against
`dropRadius` 15.0) + `dropVariation` 3.0 positional jitter (U-B3 lean); **1.32 u splash** hit test
(`projectileExplosionRadius` + the **referent's** 0.32 body — U-BODY-1 applied consistently with
the nova per R-WR3-23(3)); 0.833 s falling-orb warning (U-B2: there is no cast animation at all —
M-negative — so the descent is the whole tell); 76/137 per drop (U-B1 lean: whole block per drop);
**30 %/5.0 s total-speed slow.**

**Its own RNG sub-stream** (`GD_BLIZZARD_STREAM_SALT`, disjoint from the nova's), all 24 drop
positions drawn at cast in a fixed `(volley, index)` order, area-correct inverse transform
(`r = R√U`, not `r = R·U`, which would pile drops at the centre and silently double the landing
rate). Deterministic draw count, so no other mechanism's arming can shift a blizzard draw.

**Named as a BIAS, not sold as conservatism (C-7):** `offensiveSlowTotalSpeed` is movement **and**
attack **and** cast speed. Only the **movement** leg is wired — the other two would reach into the
player's cadence composition at a site shared with production. The omission makes the blizzard
**weaker** than the referent.

### 4.3 `primordian_icearmor` — twice the described ability

25 % absorb / 12 s / 32 s (**uptime 37.5 %**, measured 0.342–0.347), `instantCast` (the absorb and
the +35 % are live at frame 0, not at the f25 callback), **+35 % attack speed**, **+28 % cold**,
**total slow immunity**, cold retaliation. Cast is a **COMMIT** (U-C1's lean): the `BuffQuick` clip
is ~1.81 s with **zero root motion**, so the boss buys 12 s of buff for ~1.81 s of standing still.

**⚑ THE SLOW IMMUNITY IS CARRIED, DECLARED, AND INERT — and saying so is the point** (the
commission's explicit ask). It is inert **twice over, both measured**: (a) `primordian_passive`
rank 5 carries the same `defensiveTotalSpeedResistance 500.0` **permanently**, so the boss is
slow-immune all fight regardless; (b) the player's compiled kit emits no slow, chill or root at
all. It ships as a field with its provenance, and a test asserts no engine path reads it as a
behaviour — so the day a player-side slow lands it is already there, **inert by measurement rather
than absent by oversight**.

**Cold retaliation ≈ 3.5 over 2 s composed (13.3 at S0).** ≤ 1.8 % of a 759 pool, below the tick
quantum of every other channel. **Reported and NOT wired** — a retaliation channel needs a
player-side melee-contact event this ranged-claw kit does not generate per hit.

### 4.4 F-2's in-flight steering (SS-S2B-1)

The pending set gains rings **in flight but not yet resolved against this target**, with the budget
running to `t_launch + r/v` — the front's own kinematics — and selection over the union by
**earliest deadline**. **Keyed to `threat_half_width_m is not None`** (the star hit test being
live), *not* to a flag: under a uniform ring the old behaviour is correct and the decision window
really does close at launch. Same construction as SS-S2-1's phase gate, for the same reason.

**No new information is granted.** The policy already receives `spoke_offset_rad` for pending
rings; an in-flight fan is *visible* (beat 3 of the measured tell), so the in-flight case needs a
strictly **weaker** fidelity argument than the pending case that already shipped. Reaction latency
and the actionable-window ceiling both still apply. Same scorer, same candidates, same
strict-improvement rule — R-M3-1 intact.

### 4.5 Schema (R-WR3-23(6), ADOPTED)

`spoke_offset_rad` + `t_launch_s` + `projectile_velocity_ms` ride the **telegraph** record;
`null` on every non-projectile telegraph; `replica-frame/v1` **stays v1**. Drax reconstructs the
fan procedurally: `prong_k(t) = origin + v·(t − t_launch)·(cos, sin)(offset + k·2π/N)`. **Per-frame
per-prong positions REFUSED.** `shape` gains a fifth value **`"rect"`**.

**⚠ DRAX: this is your D-F4 discipline candidate firing again — fourth value-set growth in four
runs.** An exhaustive `match` over `shape` without a default arm will now silently draw nothing for
every wave in every stage-2b trace. MIGRATION.md carries the full consumer note.

**One thing a consumer must still know out-of-band:** the prong COUNT (16) is not emitted. Flagged
as the candidate for the next amendment if drax wants it in-record.

---

## §5 — THE FINDING: F-2 IS A PLAYER BUFF, AND IT IS WHAT LEAVES THE BAND

The battery's own numbers say the kit landed and still the boss cannot win. The ablation says why.
Seed-matched, 30 seeds, boss tier, single arm, `pre` regime:

| arm | leech 0.00 | leech 0.05 | leech 0.08 | damage taken (leech 0) |
|---|---|---|---|---|
| **A** stage 2 (no kit, no F-2) | **0.567 IN BAND** | 1.000 | 1.000 | 785.6 (103.5 %) |
| **B** kit only (F-2 + icearmor OFF) | **0.433 IN BAND** | 0.667 | 0.767 | 656.2 (86.5 %) |
| **C** kit + F-2 + icearmor | 0.933 | 0.967 | 1.000 | **301.0 (39.7 %)** |

Three things fall out of that table, and each is decision-grade:

1. **F-2 CUTS PLAYER DAMAGE INTAKE BY 54 % (656 → 301) AND MOVES THE WIN RATE 0.433 → 0.933.**
   Nova crossings collapse **2.20–2.33 → 0.133 (−94 %)**. It was commissioned as a fidelity fix for
   a measured defect (the policy walked back across corridors after launch) and it *is* that — but
   it is also the largest single balance intervention in this run, and it points the wrong way for
   the band. **It should be its own flag, separable from the kit.** Today one flag arms both.
2. **THE KIT WORKS.** Arm B — the kit with F-2 and icearmor disarmed — sits at **0.433, inside the
   Matt-signed band**, and takes the fight from 103.5 % to 86.5 % of pool. R-WR3-23(1)'s
   load-bearing ruling is vindicated in direction, though **stage 2 was ALREADY in band at leech 0
   (0.567)** — which reframes the whole calibration distance.
3. **THE BATTERY'S H1 IS DOMINATED BY LIFESTEAL, WHICH IS A BQ-3 CALIBRATION-DOOR PARAMETER, NOT A
   MECHANISM.** At leech 0.05 the stage-2 arm goes 0.567 → **1.000**. Both battery arms carry leech
   (0.05 / 0.08) because the fixture's A/B compares two leech depths. **So H1 as measured on the
   battery of record is answering a question about the leech door as much as about the boss.** That
   is not a defect in the battery — it is what the A/B was built for — but it is load-bearing for
   any ruling that reads H1 as a boss-difficulty number. **Routed, not resolved.**

---

## §6 — THE TWO DEFECTS THE SMOKE FOUND (Discipline #11, and both are semantic shifts)

Neither was in the math note. Both were found by looking at counters rather than at outcomes, and
both were pre-existing conflations that only became load-bearing at four specials.

### SS-S2B-8 — RE-USE TIMER vs ACTION-SLOT OCCUPANCY

`cooldown_seconds` was doing double duty: the skill's own re-use eligibility (`skill_cooldowns[idx]`
— correct) **and** the mob's whole action budget (`action_available_at` — wrong). With ONE special
that was benign. With four it was catastrophic: **`chillbane_blizzard`'s `Delay 10.0 s` locked the
boss out of EVERY action for ten seconds, and nova crossings went 3 → 0 on the same seed. The kit
starved itself.** The referent separates them — `specialAttackNDelay` is a per-slot eligibility
timer (5.0 / 6.0 / 10.0 independently) while the action is occupied for the **cast animation**.
`action_occupancy_s` is absent on every pre-stage-2b packet, so the expression is untouched off the
arm.

### SS-S2B-9 — THE MULTI-SPECIAL TIEBREAK

`ready_indices[0]` is a lowest-index tiebreak. With one special that is not a policy; with four it
is a strict priority order. Measured: the boss selected melee 9× / nova 5× / wave 4× and
**`chillbane_blizzard` ZERO TIMES in a whole fight** — the wave sits one index above it on a 5.0 s
clock against the blizzard's 10.0 s and starved it permanently. The referent has no such order.
The fix is the minimum that removes starvation without inventing an AI: **among eligible SPECIALS,
the least recently used**; identical to `ready_indices[0]` whenever at most one special is eligible
(every pre-stage-2b fixture in the tree); the **default attack keeps strict priority**, so the
melee cadence, the C2 lock and every duty-cycle number are untouched; deterministic, zero RNG.

**A third, smaller one:** `IceArmorState.cooldown_left_s` initialised to 32.0 made the buff
unavailable for 32 s of a ~36 s fight — `icearmor_casts = 0`, a mechanism measuring nothing with
every counter a clean zero. **That is the R-WR3-15 `is_boss`-on-the-wrong-object shape, second
occurrence in this run.** And a fourth: `range_m: 0.0` on the self-buff hit the *documented dead*
`range_m == 0.0` carve-out (`float(0.0 or 2.0) == 2.0`), gating a self-cast on the player standing
inside 2.0 m. Repaired at the packet (40.0 = `leash_distance_m`), **not** at the dead branch — that
remains a named follow-on, and fixing it would move every fight containing a zero-range skill.

---

## §7 — SEMANTIC SHIFTS (Discipline #12) — all declared in the math note BEFORE implementation

| id | shift |
|---|---|
| **SS-S2B-1** | The nova policy's decision window **extends past launch** while prongs fly. True of a star, false of a ring; keyed to the hit test, not a flag. |
| **SS-S2B-2** | **The outgoing damage stage becomes an explicit, named, three-armed object.** Today's ×1.0 stops being an unnamed absence and becomes `S0_NONE`, a POSITION. Nothing moves; a silent omission becomes an inspectable choice. |
| **SS-S2B-3** | **The stage map is a PARTITION, not a scalar.** Anyone applying "×0.2625" to `BOSS_DMG_SWEEP` double-counts. |
| **SS-S2B-4** | `tdm_additive_multiplier = 0.05` is **superseded as an operand** (built at charLevel 13). The constant is not mutated — it is the record of what Arm C ran. |
| **SS-S2B-5** | **The player gains an outgoing-damage debuff channel.** Every instrument reading player DPS off a stage-2b trace sees a term that did not exist. |
| **SS-S2B-6** | **Boss attack cadence becomes time-varying** (icearmor's +35 %). R-WR3-13's F5 on-grid check re-registers as **two grids** — `{1.7, 1.8}` unbuffed, `{1.2, 1.3}` buffed. |
| **SS-S2B-7** | The telegraph record gains three keys and a fifth `shape`. Additive; v1 stays v1; MIGRATION written. |
| **SS-S2B-8** | Re-use timer and action-slot occupancy are **separated**. §6. |
| **SS-S2B-9** | **A least-recently-used tiebreak among specials.** The melee keeps strict priority. §6. |

---

## §8 — UNMEASURED-SURFACE LEANS (R-WR3-20(d)'s standing rule)

| id | surface | lean | veto |
|---|---|---|---|
| **STAGE-1** | which outgoing stage is real | **`S0_NONE` is the regime of record** by continuity and by §1.3's HALT. `S2_FULL` is what I believe is mechanically correct. **Conductor's ruling.** | **HALT** |
| **U-A1** | sign of `offensiveSlowDamageMult` | **target deals 30 % less** (family convention). The CONSERVATIVE lean — the alternative is worth ~2× more to the boss. | open |
| **U-B1** | blizzard block whole-per-drop vs ÷6 | **whole** (÷6 lands below the game's own measured trash floor) | open |
| **U-B2** | blizzard pre-impact ground telegraph | **none — the 0.833 s falling orb IS the warning** | open |
| **U-B3** | `dropVariation` positional vs height | **positional**; ≤ 0.125 s of stagger either way | open |
| **U-C1** | can the boss act out of `instantCast` | **committed** (~1.81 s); root motion 0 under either reading | open |
| **U-WAVE-T** | which pak modifier hits the sunder anim | **0.852 s** anim-table figure; band 0.852–0.947 carried in-source | open |
| **U-3** | `'MediumRange'` / `'LongRange'` → metres | **9.0 / 15.0**, carried from the star note | open |
| **U-BODY-1** | our 0.5 m body vs the referent's 0.32 | **payload** hit tests compose from the REFERENT's bodies; the **policy's clearance planning** uses our own `entity_radius` (it has to — that is the body it must move). Both conventions named, difference 0.18 m. | open |

---

## §9 — TESTS AND SUITE STATE (stated honestly, per the commission)

| item | value |
|---|---|
| New unit tests | **38** in `tests/test_wr3_kite_commit_stage2b.py`, all passing |
| WR1 + WR2 + WR3 suites re-run together | **3,907 passing** |
| **Full `tests/` verdict from the STAGE-2 run — the answer that was owed** | **61 failed, 9,749 passed, 21 errors in 1,278 s** = **82 failing names against the 81-name baseline.** |
| **The 82nd name, identified and FIXED** | `tests/test_wr2_d_nova_telegraph.py::test_the_selector_transcription_above_matches_the_LIVE_selector_source`. **Cause: the W-1 amendment (`2a33881e`), not stage 2.** W-1 extracted the range predicate verbatim out of `_select_skill_for_entity` into `_skill_range_covers` (decision AI-D1), and this guard-the-guard inspected the old site — behaving exactly as designed on a refactor it could not distinguish from an edit. **Re-pointed at the extraction site**, with an added assertion that the selector delegates rather than keeping a second copy. **Baseline is back to 81.** |
| AST assertion: no RL imports in `env_contract` | **still green** |
| Flag-OFF byte identity | **`a0c6b5c8f6c8795f`, PROVEN identical to `92381a23`** across 4 tiers × 3 seeds × 2 arms (15 fights) by stashing the tree and re-running |

Written to catch the failure modes this build could actually have: three tests exist **because the
smoke found the defect first** (`test_icearmor_is_ready_at_engagement`,
`test_blizzard_is_not_starved_by_index_order`, `test_action_occupancy_is_not_the_reuse_cooldown`).
The corridor and splash radii are pinned as **compositions** so a re-derivation from the wrong
bodies breaks the sum; the stage arms are pinned to their measured operands; the HALT's own >15 %
predicate is pinned so the report's HALT cannot silently stop being justified.

---

## §10 — REPRODUCTION

```bash
cd ~/Games/reincarnated-engine && export PYTHONPATH=src
python3 -m pytest tests/test_wr3_kite_commit_stage2b.py -q -p no:randomly          # 38 pass
# battery of record — SEQUENTIAL, one leg at a time (Discipline #3)
bash /tmp/gamora_s2b_bat3.sh          # R2_proxy · R3 (--r3-arm) · R2_proxy_resists_low
python3 -c "from reincarnated.simulation import wr3_cell_s2b_2026_07_30 as C; C.main()"
python3 /tmp/abl2.py                  # the §5 F-2 ablation
```

Nothing wrote to `wr2_battery_after/`, `wr3_battery_s2/`, or any `wr3_battery_after*` root.

---

## §11 — WHAT THE CONDUCTOR OWES A RULING ON

1. **⚑ THE STAGE MAP (§1.3) — the HALT.** Which of `S0_NONE` / `S1_PAK` / `S2_FULL` is the regime
   of record. Evidence in both directions is in §1.1–§1.5. **The discriminator we cannot settle:
   whether the referent's 260.498 was a Primordian event at all** — that is a legolas question and
   it decides the ruling.
2. **⚑ F-2 SHOULD BE ITS OWN FLAG (§5).** It is the largest balance intervention in this run and it
   is currently welded to the kit. Separating it is a one-line change and it is the conductor's to
   scope, because the stage-2b arm's H1 is not attributable while they share a flag.
3. **THE LEECH FINDING (§5.3).** H1 on the battery of record is dominated by a BQ-3 door parameter.
   Any ruling that reads H1 as a boss-difficulty number needs this stated.
4. **THE RE-RANKING (§2.4)** — blizzard demoted to a tempo channel, icearmor promoted to rank 2.
   Amends R-WR3-23(1)'s ratification on measurement.
5. **MY OWN STAGE-2 CORRECTIONS (§2.1, §2.2)** — the blizzard re-aim premise and the r ≈ 9.5 m
   crossover were both wrong, and R-WR3-23(1) ratified a ranking that rested partly on them.
6. **MELEE GRADUATION (§1.7)** — proposed `(43.1, 52.0, 60.8)` + `M-BAND`, not enacted.
7. **SS-S2B-8 / SS-S2B-9 (§6)** — two pre-existing conflations repaired under a flag. Both are
   arguably fixture-wide truths that should not stay flag-scoped.
8. **A-WAVE-1 / A-BLIZ-1 (§1.5)** — the pin set grows by two; the shape of the widening is mine and
   is veto-open.
9. **THE PRONG COUNT IS NOT EMITTED (§4.5)** — the one out-of-band fact a renderer still needs.

---

*WR3-KITE-COMMIT stage-2b build report — gamora, simulation seam, 2026-07-30. Engine committed at
`97d51798`; neither repo pushed.*
