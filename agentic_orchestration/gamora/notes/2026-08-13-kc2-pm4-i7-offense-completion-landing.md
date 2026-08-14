# KC2-PM4 · I-7 — landing note: **the term the ruling named cancels itself, and the first player dies.**

> **Run:** KC2-PM4 · **Iteration:** I-7, OFFENSE COMPLETION · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-13
> **Fired under:** ruling **R-PM4-17** (charter ledger **L-14**). **R-PM4-15 still binding** —
> D-I5-1 stays SOFT; **the Jacobi solver and its pass count are UNTOUCHED.**
> **Math note (Discipline #1, written and committed BEFORE the code — commit `3dd1f1e9`, its own
> commit, so the git order is the proof):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i7-offense-completion-2026-08-13.md`
> **Status:** COMPLETE. **No HALT.** Assert wall **22/22 PASS**, determinism ×2 **EXACT (0
> differences)** on all three cells, **three batons FULL at 67/67**, Law-3 witness `moved: {}`.
> **Two defects self-caught and closed (§ 8), one routing request at § 13.**

> ### ⚑ NOTE-9 — THE BASIS FOR EVERY NUMBER IN THIS NOTE
> Unless a different source is named inline, every I-7 quantity is read by key path from
> `reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i7-findings-20260814_005919.json`
> · sha256 **`d4d0478c94316de53a0a174f31290bb4573938be7afccb9dcab81ad6d2c5ec75`**, and every I-6
> quantity from `…/kc2-pm4-i6-findings-20260813_231731.json` · sha256
> **`2acf01299a565271ee26eb4a200448bf4609983a631f3b4e45637983c10ed2d6`** (verified from bytes at
> run time by the driver — a wrong digest HALTs the lap). **There is no unsourced number below.**

---

## 0 — The one-paragraph answer

**The ruling's headline term does nothing, and I knew that before the run.** R-PM4-17 named "+50
flat OA against the sim's 23.7 % miss rate" as a measured term that raises hit frequency. It is one
— and the **same Ultimate pak cell** carries `characterOffensiveAbilityModifier = −8.0` beside it,
with the survival array adding `+50.0 / +3.5` at wave 160. Folded together, which Law 3 *requires*,
they **cancel**: median effective OA across 237 bodies moves **2167.0 → 2167.4**, the population
mean miss probability **0.2430 → 0.2420**, and the reference cell's miss rate **23.69 % → 23.50 %**.
The attack-speed limb (**+11 %**, law S1) is the entire measurable content of the iteration, and it
buys **+6.8 % attack opportunities for +2.4 % intake** and **−0.0004 mean HP**. **But CLUSTER/DEF-OFF
now dies — on wave 160, the reference wave, 7.918 s in.** The first death in seven iterations.
Three measurements changed what this lap could claim: the OA unit ambiguity was **decidable** (§ 2),
the reference **baton cannot supply the clause-2 joint** it was named as the source of (§ 5), and
the HP trace this run has published for seven iterations is a **post-heal end-of-tick sample whose
true floor is 0.11 deeper** (§ 6). **Clause 2 reads MET.** And the pre-registered § 7.1 error
hypothesis — *I am pricing the numerator of a ratio whose denominator is the runaway term* — is
**confirmed by a control cell that changed the intake by 4,158 damage and moved the end-of-tick HP
statistics by exactly nothing** (§ 9.1).

---

## 1 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 15 predictions, 22-check wall) | `simulation/math/kc2-pm4-i7-offense-completion-2026-08-13.md` | **`3dd1f1e9`** |
| 2 | `kc2/offense.py` — laws **O1** + **S1**, the pak cross-check, the limb-keyed wire form | modified | `b0aaecc1` |
| 3 | `kc2/threat.py` — `folded_oa` / `oa_pre_modifier` / `ThreatProfile.oa_for`, the swing clock, **D-I7-2**, **D-I7-3** | modified | `b0aaecc1` |
| 4 | `kc2/run.py` — the intra-tick HP floor + the clause-2 ring-joint census, both on **run attributes** | modified | `b0aaecc1` |
| 5 | `export/kc2_run_adapter.py` — `offense_to_hit` / `offense_attack_speed` + 3 I-7 specs | modified | `b0aaecc1` |
| 6 | **1 new pinned CSV** (Lap I ultimate paks, AUDIT source) | `data/kc2/pm4i_ultimate_offense_paks.csv` | `b0aaecc1` |
| 7 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `b0aaecc1` |
| 8 | **driver + 22-check wall + determinism + 5 sensitivity cells** | `simulation/scripts/gamora_kc2_pm4_i7_offense_completion_2026_08_13.py` | `b0aaecc1` |
| 9 | **3 knot supplies + findings** (stamp `20260814_005919`) | `simulation/output/` | `65324120` |
| 10 | **⚑ 3 BATONS, FULL, 67/67** | `src/reincarnated/output/` | `f6f9304a` |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6)

| what | sha256 |
|---|---|
| **findings** | `d4d0478c94316de53a0a174f31290bb4573938be7afccb9dcab81ad6d2c5ec75` |
| knots CAMP/DEF-OFF | `7adae207aeb5c9c05330c6810b3d8e2af0e5d23379f408eadc76a254bd3591cc` |
| knots CLUSTER/DEF-OFF | `74f5f886d0a2bb44f46cc096e5580dfc1f9b2ed5f026bd85e9c4b9b5f4212331` |
| **knots CLUSTER/DEF-ON** ← reference | `c8463a22d0116d64a9795ed84e058376a3f27d3fd267d6a50b6f8019bb8266b2` |
| **baton** CAMP/DEF-OFF | `ce4c38b12b7c2896a5b1ef0f5bbdeb2b909bd17b3f824d7a45faa6fbdec13c1a` |
| **baton** CLUSTER/DEF-OFF | `d28900866b79192c74f0b95109a275365767e1f5dd12b3812ac7d77817a4b2c3` |
| **baton** CLUSTER/DEF-ON ← reference | `8b12244fade048f038dfd1d5aa6b02081cdc89a0e8bb672910d8aaf2102b2c8a` |
| determinism surface CAMP/DEF-OFF | `d6d71a0a8f29601c8d18e8e7c77e23abc2e1be1101269c32fffeb60423e8487f` |
| determinism surface CLUSTER/DEF-OFF | `2ed7286ed7d0c6b73fe9d7b9e38c47d7425aca5e8cf37381fa9a8a301fca8afd` |
| determinism surface CLUSTER/DEF-ON | `5cb321b9fcb015c8b314f23de5e4615993ebff93f6d8656b6fde6cb94015fde8` |
| **new pinned substrate** `pm4i_ultimate_offense_paks.csv` | `b09341478b938a10379086a9deead12a690a950a3048f69d9a0337781b54fc5e` |

**Baseline digests reproduced byte-exactly at I-7 HEAD, at TWO depths** (checks 1 + 2):
I-6 `e96c8101…f82637` / `9bf4785b…bec9dbeea`… → all three **EXACT**; and the **pre-I-6** arm still
reproduces I-5's `5f616040…`, `0ad5b297…`, `95a34b2e…` — **two folds back**, a check I-6 did not
carry and which would have caught a regression I-6's own one-hop check could not see.

---

## 2 — ⚑ THE SEMANTIC DECISION I HAD TO MAKE BEFORE ANY CODE (C-I7-1)

Lap I's method § 1.3 tabulates the survival array's cell as **`characterOffensiveAbility | +50.0 %`**
and its § 2.2 grades the Ultimate pak's cell **"+50 flat"** — the *same field name*, two units,
differing by a factor of ~44 at the board's median OA of 2167. My own I-6 § 12.4 carried the
ambiguity forward. This is decidable-or-fork, not a footnote, and **it is decidable: FLAT.**

1. **The corpus's paired-field convention.** Both records carry `characterOffensiveAbility` **and**
   `characterOffensiveAbilityModifier`. A percent reading of the first makes the second redundant
   on both records simultaneously.
2. **`combatformulas.dbr@offensiveAbilityEquation`, character for character**
   (`data/kc2/pm2_hit_math_constants.json`): `(offensiveAbilityDV + (characterLevelDV*12) +
   ((dexterityDV+bonusDV)*0.5)) * (1 + (offensiveAbilityModifierDV/100)) + 53`. **Exactly two
   slots** — one absolute, one percent — and the two field names map onto them one-for-one.
3. **The sim already implements that split** (`effective_oa(oa_base, level, flat, modifier_pct)`,
   R-PM2-3, since PM-2). The fold drops into a correctly-shaped hole; no new equation is written.
4. **Lap I suffixes every emitted column `_pct` mechanically**, including ones its own prose calls
   flat. The suffix is a naming artifact, not a unit claim.

⚑ **And FLAT is also the LOWER reading** (+100 on 2167 is +4.6 %; +100 % would be +2167). The
convention-correct choice and the conservative choice agree, so no fork was opened. **Routed to the
conductor at § 13 as a Lap-I erratum, not a blocker.**

### 2.1 — ⚑ NO PTH FORK. The stop-and-route condition does not trigger, and I checked the record

R-PM4-17 item 1 instructs me to STOP if the to-hit **model** is missing a decodable piece.
`combatformulas.dbr` is dumped **COMPLETE** (`__n_fields__: 44`, all 44 present). It carries
`probabilityToHitEquation`, `normalPTHEquation`, `pthMinimum = 55.0`, `pthThreshold1..6` and
`pthDamageModifier1..6` — **all six of which the sim implements** — and **no `pthMaximum` and no
other PTH term**. The sim's curve **is** the corpus's curve. The single absent input is
`dexterityDV`, ABSENT from the substrate, contributing zero, already declared under R-PM2-3 and
already the lower-damage direction. **Nothing to fork; the ruling's condition is answered from the
record rather than from memory.**

---

## 3 — THE TWO LAWS, EVERY CONSTANT TRACED TO A NAMED CSV CELL (Law 3 tripwire)

Source: `pm4i_wave_damage_modifier.csv` (`f0852cec…`) with `pm4i_ultimate_offense_paks.csv`
(`b0934147…`) pinned as an **audit** source. Basis carried verbatim onto the wire:
`balancingadjustment_survivalmode_enemies03.dbr@sm_mod [index wave−1]` +
`balancingadjustment_mp+difficulty_enemies01.dbr@base [index 8 = Ultimate/1-player]`.

| law | form | w151 | **w160** | w170 |
|---|---|---:|---:|---:|
| **O1** flat | `D_characterOffensiveAbility + U_…` | 98.0 | **100.0** | 103.0 |
| **O1** percent | `D_…Modifier + U_…Modifier` | −4.5 | **−4.5** | −4.5 |
| **S1** | `S_atk = 1 + (D+U)/100`; period `/ S_atk` | 1.11 | **1.11** | 1.11 |

**Grade:** `MEASURED (components); sum = DERIVED-SUM-ADDITIVE-BY-PARALLEL` — ⚑ and Lap I emitted a
`sum_` column for the *damage* chain and **none for these two**, so the summation is **my extension**
of its cliff C-I3. Filed as **C-I7-2**, named rather than inherited silently; both components ride
beside every sum on the wire.

**⚑ The pak is not trusted, it is checked.** `ultimate_pak_crosscheck()` re-reads the pak's `[8]`
cells and compares them to the wave table's `U_` columns — **4 fields × 50 waves, EXACT, every run**
(check 3). A transcription error between two Lap-I tables now HALTs the lap instead of riding it.

---

## 4 — ⚑ THE RESULT THE RULING DID NOT EXPECT: **THE OA LIMB IS A MEASURED WASH**

Basis `⚑ oa_arithmetic`, computed at run time over all **237** loaded profiles, `PLAYER_DA = 2591.0`.

| | median OA | median PTH | max PTH | mean miss prob |
|---|---:|---:|---:|---:|
| **base (I-6)** | 2167.0 | 77.437 | 84.609 | **0.24304** |
| after O1 @ w151 | 2165.46 (**−1.54**) | 77.390 | 84.247 | 0.24236 |
| **after O1 @ w160** | **2167.37 (+0.37)** | 77.449 | 84.303 | **0.24198** |
| after O1 @ w170 | 2170.24 (**+3.24**) | 77.536 | 84.388 | 0.24148 |

> ### ⚑ `(2125 + 100) × 0.955 + 53 = 2177.9` AGAINST `2125 × 1.000 + 53 = 2178.0`.
> The +100 flat grant and the −4.5 % modifier cancel. **The ruling's framing of "+50 flat OA
> against a 23.7 % miss rate" reads the pak's to-hit grant as a term that raises hit frequency. It
> is — and the same pak cell takes it back.** Folding one and not the other would have moved the
> miss rate ~4.6 points in the direction that flatters T1–T4, which is exactly the shape Law 3
> bars. **Both fold. The wash is the finding, and it was pre-registered as P.1 before the run.**

**Priced, not asserted — sensitivity S-OA-FLAT-ONLY** runs the counterfactual (the +50 flat grant
*without* the pak's own percent term): misses **454 → 379** (−16.5 %), mean HP **0.9859 → 0.9837**
(−0.0022 *toward* the video), excursions 13 → 15. **That is the cell an optimiser would have
shipped. It is not the run of record, and its delta is the measure of what Law 3 bought.**

### 4.1 — Crit: unreachable **by construction**, now from a mechanism instead of a zero count

`resolve_hit` awards tier ≥ 2 only when `PTH ≥ pthThreshold2 = 90.0`. Measured: PTH spans
**66.27 … 84.609** across all 237 bodies; `n(PTH ≥ 90) = 0` at base and at every folded wave (max
84.388 @ w170). `offensiveCritDamageModifier` (+27 %) **provably cannot bind**. `n_crits = 0` on all
three cells. Also measured: `n(PTH < 55) = 0`, so `pthMinimum` never binds either, and 9 of 237 sit
in the sub-threshold `55 ≤ PTH < 70` band where the multiplier is `PTH/70 < 1`.

---

## 5 — ⚑ ITEM 2: CLAUSE 2 IS **MET** — AND THE BATON COULD NOT ANSWER IT

R-PM4-17 item 2 names the I-6 reference baton (`c2ad90da…5db6b`) as the source. **It cannot be.**
Read from the baton's own bytes at its pinned digest (check 21): its `tracks` are
`circle_sweep` / `player_energy` / `player_hp` / `player_path` — **there is no per-tick actor-position
track**. Monster positions appear only on `events`, at attack instants, for the attacking body
alone. **The ring-occupant SET at the max-ring ticks is not recoverable from it.** Said plainly
rather than quietly substituting an instrument and calling it the baton's.

**What I did instead, and why it is the same measurement.** The I-6 reference *trajectory* is
reproduced byte-exactly by the check-1 arm (digest `0a0c140d…dafb808`, EXACT). I took the joint on
that trajectory with an in-run census that reads the *same* `live` dict `_observation_census`
already reads, draws no RNG and feeds nothing back — and **proved it inert**: the census arm's
surface digest **equals** the plain arm's (check 15, `0a0c140d…` both).

**The rule was fixed at module scope BEFORE the measurement** (math note § 5.3): *clause 2 = MET iff
`median(ARC) > 1.0` **and** `mean(pairs within ring) > 0` at the max-ring ticks.* Geometry: a body of
radius `r` at distance `d` subtends `asin(r/d)`; `n` bodies all at `d` fit without overlap iff
`Σ 2·asin(r_i/d) ≤ 2π`. `ARC` is that sum normalised to 1, so **`ARC > 1` is impossible, not tight**.

| at the **max-ring** ticks (I-6 trajectory, identical on the I-7 cell) | value |
|---|---:|
| ring occupancy | **19** |
| ticks at that occupancy | **1** |
| `ARC` | **1.27391** |
| overlapping pairs **among ring occupants** | **26** |
| engulfing bodies (`r ≥ d`, counted not clipped) | 0 |
| occupant radii — median / max | 0.350 m / 0.750 m |

| across **all 2,247 occupied** ticks | value |
|---|---:|
| fraction with `ARC > 1.0` | **2.047 %** (46 ticks) |
| fraction with ≥ 1 overlapping ring pair | **23.32 %** |
| mean pairs / occupied tick | **0.9746** · max **28** |
| `ARC` max | **1.52293** · mean 0.2517 |

> ### ⚑ **CLAUSE 2 = MET.** And my own I-6 counter-argument is answered *by the data that raised it*.
> At I-6 I said: *"if the ring's peak occupancy is dominated by small summon bodies (r 0.360 m,
> capacity 20.86), overlap is implicated less than the median figure suggests — and I will not
> assert a joint I have not measured."* **The max ring IS small-body dominated** — median occupant
> radius **0.350 m**, below the pet mode. **And it is still impossible**: the mix (one 0.750 m body
> among them) carries `ARC` to 1.274, and **26 pairs are actually interpenetrating at that instant**.
> The refusal to assert was right; the measurement resolves it against my own hedge.

⚑ **HONESTY ON SAMPLE SIZE, unprompted: the max-ring condition holds at exactly ONE tick.** A
verdict resting on `n = 1` would be thin, which is why the all-occupied-ticks distribution is
reported beside it and points the same way (`ARC > 1` on 46 ticks, ≥1 ring pair on 524).

**Clause 1** is MET and unchanged: ring 0/4/**19** against the video's 1/3/**10**.

---

## 6 — ⚑ ITEM 3: THE INTRA-TICK FLOOR, AND IT CORRECTS MY OWN I-6 § 6.1

**Where the floor is, read off the tick order rather than assumed.** HP is monotone non-increasing
through attacks → auras → DoTs and monotone non-decreasing from the regen slot onward, so the
minimum the tick takes *anywhere* is its value at the **death check**. Asserted per tick, not
assumed: `H_floor ≤ H_pre_cp ≤ H_end` holds on **6,097 / 6,097** ticks, **0 violations** (check 13).

**⚑ D-I7-1 — I-6 § 6.1 named the wrong evaluation point, and I am saying so rather than letting it
stand.** I wrote that K-3 firing while the recorded minimum read 0.3915 proved the triggers evaluate
"inside the tick". The mechanism is right; the point I implied was wrong. K-3 and K-4 test
`H_pre_cp` (**post-regen**, pre-counterplay-heal) — measured min **0.27688**, comfortably under
K-3's 0.33 trigger. `H_floor` is deeper than both. **No number moved; the explanation did.**

### 6.1 — The I-6 trajectory restated like-for-like (the comparison the ruling asked for)

| basis | mean HP | min HP | exc < 0.90 | **exc < 0.70** | ticks < 0.70 | exc < 0.50 | exc < 0.33 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **end-of-tick** (what every I-1…I-6 number used) | 0.98628 | **0.39155** | 30 | **12** | 87 | 3 | 0 |
| **⚑ true intra-tick floor** | 0.97744 | **0.27636** | 131 | **16** | 103 | 5 | **1** |
| *pre-counterplay* (`H_pre_cp`) | 0.98611 | 0.27688 | — | — | — | — | — |
| **video (Lap H-2)** | **0.932** | 0.28 *(collapse floor)* | — | **7** | — | — | — |

> ### ⚑ **THE SIM'S TRUE FLOOR AT I-6 WAS 0.2764. THE VIDEO'S TERMINAL COLLAPSE FLOOR IS 0.28.**
> On the depth axis the sim was already there and the instrument was hiding it. On the *count* axis
> it goes the wrong way: 16 intra-tick excursions against the video's seven, worse than the 12 the
> end-of-tick basis showed. **The shape divergence is larger than I-6 reported, not smaller.**

⚑ **The caveat is stated rather than buried.** The video is **frame**-sampled — an instant that can
land anywhere inside a tick. `H_end` is always post-heal (an upper reading); `H_floor` is the
envelope minimum (a lower reading). **The video's true statistic lies between them.** Both bases are
reported on every quantity and **neither is presented as "the" answer**; a single-basis comparison
overstates its own precision. This is filed in `simulation/MIGRATION.md` § 1 as the one thing a
baton consumer must change its mind about — the schema did not change, the *reading* of it must.

---

## 7 — ⚑ THE THREE CELLS: THE FIRST DEATH IN THE RUN

| cell | terminal | t (s) | mean HP | min HP (EOT / **intra**) | exc<0.70 (EOT / **intra**) | opportunities | miss | intake |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| CAMP/DEF-OFF | `arena_tier_exhausted`@171 | 1,939.67 | 0.9941 | 0.2926 / **0.2305** | 18 / **32** | 7,591 | 478/2,139 = 22.35 % | 1,981,619 |
| **CLUSTER/DEF-OFF** | **⚑ `player_death`@160** | **218.20** | 0.9759 | **0.0000** / **0.0000** | 6 / **5** | 3,387 | 221/884 = 25.00 % | 663,140 |
| **CLUSTER/DEF-ON** ← reference | `arena_tier_exhausted`@171 | 497.71 | **0.9859** | 0.4516 / **0.3273** | 13 / **21** | 6,477 | 454/1,932 = **23.50 %** | 1,734,232 |

> ### ⚑ **CLUSTER/DEF-OFF DIES ON WAVE 160 — THE REFERENCE WAVE — 7.918 s IN, KILLED BY `w160_pet0012`.**
> It grazed **0.0521** at I-6 and P.7b called it at 60 % confidence for waves 158–170. It landed on
> **160 exactly**. That is the first player death in seven iterations of this run, and it is a
> **defences-OFF** cell — the one Matt did **not** play. Read plainly: **the measured monster
> offense is now lethal at the reference wave against a player without his defensive sheet, and the
> defensive sheet is worth the entire gap between dying at 160 and clearing to 170.**

### 7.1 — The reference cell against I-6, term by term

| observable | I-6 | **I-7** | ratio |
|---|---:|---:|---:|
| attack opportunities | 6,067 | **6,477** | **×1.0676** |
| resolutions (hit + miss) | 1,828 | 1,932 | ×1.0569 |
| **miss rate** | 23.69 % | **23.50 %** | −0.19 pp |
| out of reach | 3,811 | 4,062 | ×1.0659 |
| `damage_total` | 1,693,121.06 | **1,734,231.60** | **×1.0243** |
| `damage_dot` | 3,344.70 | 3,496.15 | ×1.0453 |
| `damage_percent_current_life` | 509,086.50 | 485,546.85 | ×0.9538 |
| `heal_landed` | 1,056,676.09 | 1,084,265.13 | ×1.0261 |
| **`heal_overheal`** | 124,258,077 | **124,230,488** | — |
| mean HP | 0.986275 | **0.985925** | −0.00035 |
| min HP (end-of-tick) | 0.391548 | **0.451635** | ⚑ **higher** |
| K-1 / K-2 / K-3 / K-4 / K-5 / K-6 | 2 / 110 / 1 / 2 / 67 / 21 | **2 / 111 / 1 / 2 / 67 / 21** | ⚑ unmoved |

**⚑ +6.8 % opportunities bought +2.4 % intake.** The gap is the cooldown gate: a denser opportunity
schedule finds `basic` available more often and the specials still on `delay_s`. P.3's mechanism,
confirmed. And `percent_current_life` **fell** 4.6 % — the negative feedback carried from I-6:
pcl damage is a fraction of *current* HP, and the reference cell's min HP went **up**.

---

## 8 — ⚑ TWO DEFECTS, BOTH MINE-ADJACENT, BOTH SURFACED BY THE FOLD, BOTH ROUTED THROUGH GL-12

**D-I7-2 — `SlowLifeLeach` had no resistance row, and the guard refused rather than guessed.**
S1 gave a body an attack opportunity it had never had in seven iterations; it fired a
`SlowLifeLeach` DoT; `mitigate()` raised *"has no measured resistance on the Lap-A sheet. GL-12:
name it in `RESIST_PCT` or in `NON_HEALTH_KINDS` — do not guess a resistance."* **CAMP/DEF-OFF
halted at wave 168 on that refusal. The guard was right; the map was incomplete** — every other DoT
family had its `Slow*` row and this one did not, because nothing had ever fired one.

⚑ **Closed with the module's OWN already-measured constant.** `PLAYER_LIFE_LEECH_RESIST_PCT =
−25.0` has been in `threat.py` since PM-2 (`pm2_measured_player_sheet.csv` row `life_leech_resist`,
screenshot 519) and already drives `LEECH_MULTIPLIER` for the sibling `leech` **kind**. The fix
joins that same value to the DoT **limb** of the same family. **No new constant; Law 3's `moved: {}`
is untouched.**

⚑ **And I name the direction, because it is the damage-raising one.** −25 % resist is ×1.25 damage
— *toward* the target the run is chasing, which is exactly when a change deserves more scrutiny.
Three discriminators against it being a tuning move: (1) it is a **measured cell on a pinned sheet
with a named screenshot**, not a fitted number; (2) there is **no lower reading available** — the
alternative is a crash, so "take the conservative value" is not on the table; (3) it is a **proven
no-op on both CLUSTER cells** (their I-6 and I-5 digests are unmoved — check 22), so it cannot have
been chosen to move the reference cell's outcome.

**D-I7-3 — `SlowManaLeach` is next in line, and I did NOT give it a resistance.** The distinction is
worth being explicit about: `SlowLifeLeach` had a measured **health** resistance sitting unjoined —
that is a decode. `SlowManaLeach` drains **energy**; its measured cell (`energy_leech_resist = 0`,
same screenshot) is a resistance to an *energy* drain, and `mitigate()` returns *health* damage.
Mapping 0 into `RESIST_PCT` would silently convert an energy drain into a full-magnitude health hit
— an invention wearing a measurement's clothes, again in the damage-raising direction. Routing it
into the sim's energy ledger is a **new mechanism**, i.e. not this iteration's to improvise.
**So it is a DECLARED health-path exclusion, by name, counted on the wire** (`n_non_health_rows`; 1
row on CAMP/DEF-OFF, 0 on both clusters) — the exact discipline `NON_HEALTH_KINDS` already carries,
one level down. **It is a declared UNDER-read of threat, not a measured zero:** the player really
was having energy drained, the sim really does model energy (`energy_dryout` ends a wave), and the
two are not connected here. Closure path named at § 13.

Applied **at resolve time, after the row's chance draw** — never at load time, because dropping rows
in the loader would change how many `uniform()` calls the threat RNG consumes and would move digests
that have nothing to do with the exclusion.

### 8.1 — ⚑ THE ASSERT WALL EARNED ITS KEEP TWICE, BOTH TIMES BEFORE PUBLICATION

Check 1 went **RED on `camp_defoff` twice**, and both times for the same underlying reason: **an
observation was moving the thing it observed.** `_surface()` digests `[r.waves[0] for r in runs]`, so

1. `OffenseFold.as_dict()` gaining unconditional `oa_flat_add` / `oa_modifier_add` /
   `attack_speed_mult` keys moved every I-6 baseline; and
2. `ThreatTelemetry.as_dict()` gaining `n_non_health_rows` moved them again.

**Both were fixed structurally, not by widening the check**: the fold's wire form is now
**limb-keyed** (a fold that does not carry a limb does not emit its key, and its
`declared_not_folded` text is the one that was true when it was built — verified key-for-key against
the committed I-6 knot artifact), and the counter moved to a **run attribute**. ⚑ That is also why
both I-7 instruments ride run attributes rather than `waves[]` or `tracks`: **R-PM4-17's "no baton
schema change" is honoured structurally rather than by promise.**

---

## 9 — PRE-REGISTERED PREDICTIONS vs OUTCOME — **nine confirmed, one split, five falsified**

Falsified predictions keep their original wording (the run's standing practice).

| # | prediction | outcome |
|---|---|---|
| **P.1** | OA fold moves median OA by \|Δ\| < 1.0 point; miss rate stays within 23.687 % ± 1.0 pp | **CONFIRMED. Δ +0.37 points; 23.69 % → 23.50 %.** The wash, called before the run |
| **P.2** | opportunities rise 10–13 %: 6,067 → **6,674–6,856**, point 6,752 | **⚑ FALSIFIED — BY MY OWN INPUT, NOT BY THE MODEL. 6,477 (×1.0676).** I computed the quantised ratio at **tps = 49**, inferred from a stationarity figure; the sim's actual `ticks_per_s` is **12.25**. At 12.25 the quantisation is coarser and **24 of 160 roster swingers and 5 of 35 pets get no speed-up at all** (mean ratio 1.0911 / 1.0866, not 1.113). ⚑ A pre-registered band computed from an unverified input is a band about my arithmetic, not about the sim — and reading the fixture instead of inferring it would have cost one line |
| **P.3** | intake rises by LESS than the opportunity count; `n_on_cooldown` grows faster than `n_attacks_fired` | **SPLIT. The headline CONFIRMED and strongly: ×1.0243 intake against ×1.0676 opportunities.** The `n_on_cooldown` clause is **VACUOUS** — it is 0 on every cell in both iterations, so the gate I named is `delay_s` handled inside `choose_slot`'s availability branch, not the counter I pointed at |
| **P.4** | mean HP in **0.980–0.9863**, point 0.9843 | **CONFIRMED, at the very top of the band. 0.98593.** My point estimate was 5× too pessimistic — see § 9.1 |
| **P.5** | **excursions go the WRONG way**: 12 → 12–20 (point 15), **not** toward 7 | **CONFIRMED. 13 end-of-tick, 21 intra-tick.** The offense completion does **not** close the shape gap |
| **P.6** | intra-tick min < 0.39155 (point 0.20–0.36); intra-tick excursions ≥ end-of-tick; `min(H_pre_cp) ≤ 0.33` | **CONFIRMED on all three limbs. 0.27636** (inside the band) **· 16 ≥ 12 · 0.27688 ≤ 0.33** |
| **P.7** | T1 — the reference cell's player does NOT die; `arena_tier_exhausted` @171 | **CONFIRMED** |
| **P.7b** | **CLUSTER/DEF-OFF dies, wave 158–170** (stated at ~60 % confidence) | **⚑ CONFIRMED — wave 160, the reference wave, 7.918 s in.** The one prediction this lap that I hedged, and the one that landed on the nose |
| **P.8** | T2/T3 unchanged; like-for-like 233.5510 s exactly; per-wave times identical to the tick | **CONFIRMED on every wave that ran to completion under both iterations** — reference cell 233.55102040816328 s and all 20 per-wave times identical; CAMP/DEF-OFF identical; CLUSTER/DEF-OFF identical on waves 151–159. See § 9.2 for the check-predicate repair |
| **P.9** | match gates unchanged to the last digit | **CONFIRMED** (§ 11) |
| **P.10** | counterplay fires more: K-1 2→3–6, K-4 2→2–5, K-3 1→1–3 | **⚑ FALSIFIED on the reference cell. K-1 2, K-3 1, K-4 2 — not one firing moved.** Confirmed on CAMP/DEF-OFF (K-3 1→3, K-4 6→7). The reference cell's breakers are where they were |
| **P.11** | `n_crits` = 0 on all cells and max PTH < 90 at every wave | **CONFIRMED. 0 / 0 / 0; max PTH 84.609 base, 84.388 folded** |
| **P.12** | `skillCooldownReduction` == 0.0 at every wave 151–179 | **CONFIRMED**; first non-zero at 180, and the ladder walls at 171 |
| **P.13** | fold-off reproduces I-6's digests **and** I-5's | **CONFIRMED at both depths, all three cells, byte-exactly** |
| **P.14** | clause 2 reads MET; `median(ARC)` 1.3–2.0; mean pairs 1–6 | **⚑ SPLIT→FALSIFIED ON THE NUMBERS, CONFIRMED ON THE VERDICT. MET.** `ARC` **1.2739** is *below* my 1.3–2.0 band and mean pairs **26** is 4× above my 1–6 band. I bracketed the wrong quantity: I estimated a *typical* ring, and the max-ring tick is an *extreme* one |
| **P.15** | three batons FULL 67/67; determinism ×2 masked-EXACT | **CONFIRMED.** VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33 ×3; 0 differences ×3 |

### 9.1 — ⚑ THE PRE-REGISTERED ERROR HYPOTHESIS IS CONFIRMED, BY A CONTROL CELL

Math note § 7.1 named, before the run, the error I expected to be making: *"I am pricing the
monsters' side of a ratio whose denominator is the runaway term — `heal_adcth_offered` 125,250,358
against `heal_landed` 1,056,676; a model whose healing is effectively unbounded snaps back to full
between bursts by construction."*

**The attribution cells settle it.**

| cell | opportunities | misses | `damage_total` | mean HP | min HP | exc < 0.70 |
|---|---:|---:|---:|---:|---:|---:|
| I-6 (baseline) | 6,067 | 433 | 1,693,121.06 | 0.9862750884271755 | 0.39154790354897784 | 12 |
| **S-OA-ONLY** (O1 alone) | 6,067 | **430** | **1,697,278.75** | **0.9862750884271755** | **0.39154790354897784** | **12** |
| **S-SPD-ONLY** (S1 alone) | 6,477 | 456 | — | 0.985925199797722 | 0.45163471987230935 | 13 |
| **reference (O1 + S1)** | 6,477 | 454 | 1,734,231.60 | 0.985925199797722 | 0.45163471987230935 | 13 |

> ### ⚑ **S-OA-ONLY LANDS 4,157.70 MORE DAMAGE AND THE END-OF-TICK HP STATISTICS DO NOT MOVE — NOT APPROXIMATELY, TO SIXTEEN DIGITS.**
> Mean HP, min HP, and the excursion count are **bit-identical to I-6's**. Every unit of that extra
> damage was healed inside the same tick it landed in. **The player's sustain offers 118× what the
> HP bar can absorb** (124.2 M overheal against 1.08 M landed), so a 0.25 % intake increase is
> *invisible* in the trace. And S-SPD-ONLY reproduces the full reference result to sixteen digits:
> **S1 is the iteration; O1 contributes nothing measurable at all.**

**The unifying error, self-named, and it is a new shape.** I-1 priced sustain not exposure · I-2 eHP
not co-residence · I-3 throughput not reach · I-4 the size of the counterplay not its shape · I-5
the repair not its convergence · I-6 the mean not the variance. **I-7: I priced the numerator of a
saturated ratio.** I wrote the mechanism down in § 7.1 *before the run* and then still set P.4's
point estimate five times too pessimistic, because I extrapolated the I-5→I-6 coefficient instead of
trusting the saturation argument I had just made. **The mechanism was in my own math note and I
forecast off the regression line anyway** — which is the same failure mode as I-6, one level up.

### 9.2 — ⚑ CHECK 10's PREDICATE WAS REPAIRED **AFTER** SEEING THE DATA — SAID PLAINLY

The first form of check 10 asked for whole-list equality of per-wave clear times against I-6. It
went RED on two cells — and **not one clear time had moved**. CLUSTER/DEF-OFF's player died at wave
160 and CAMP/DEF-OFF halted at 168 (D-I7-2), so their ladders were shorter. Whole-list equality
conflates *"a wave took longer"* with *"the ladder ended sooner"* — two entirely different findings.
The predicate now compares the **common completed prefix** and reports the length difference and the
death-wave duration separately. **This is a measurement-definition repair made with the result in
hand. No number moved, and it is stated in those words rather than shipped as a green check.**

---

## 10 — TARGET STATE T1–T4 (reference cell; the run's own scorecard)

| band | target | measured | verdict |
|---|---|---|---|
| **T1** survival depth | death on wave **160** ({159–161} near-miss) | **no death; terminal wave 170** (`arena_tier_exhausted` @171) | **MISSED** |
| **T2** duration | 186 s ± 15 % (158.1–213.9) | **like-for-like 151–160 = 233.551 s** (+25.6 %); whole ladder 497.71 s | **MISSED** — ⚑ and **unchanged to the digit from I-6**, because S1 cannot move the player's kill work |
| **T3** pacing | per-wave clears correlate with 14/17/29 s | median ratio 1.1646, pearson r 0.1425 | **NEAR/MISSED**, **identical to I-6** |
| **T4a** sustain-through-throughput | alive while clearing | mean HP 0.9859 over 6,097 ticks | **MET** |
| **T4b** fought terminal wave, ~6.55 s collapse | DoT-involved collapse | terminal wave 170 cleared in 15.59 s; DoT 0.20 % of intake | **MISSED** |

⚑ **T2 and T3 are reported with their I-6 verdicts intact and the reason stated: the I-7 fold moves
monster→player intake only.** Re-reporting them as if they were evidence about this fold would be
padding. **The one T-band that moved is T1, and it moved on a cell that is not the reference one.**

### 10.1 — HP observables against the video

| | sim I-6 | **sim I-7 (EOT)** | **sim I-7 (intra)** | video |
|---|---:|---:|---:|---:|
| mean HP | 0.9863 | **0.9859** | **0.9769** | **0.932** |
| excursions < 0.70 | 12 | **13** | **21** | **7** |
| min / floor | 0.3915 | 0.4516 | **0.3273** | 0.28 |

**The divergence is unchanged in character and larger in magnitude.** The sim's trace is near-full
with occasional deep spikes; the video's is *persistently depressed*. On the intra-tick basis the
sim has **three times** the video's excursion count while sitting **4.5 points** above its mean.
**Adding intake widens the tail without closing the mean** — measured twice now, at I-6 and I-7.

---

## 11 — MATCH GATES: UNMOVED, BY CONSTRUCTION, AND SAID SO IN ADVANCE

NOTE-9 caveat carried unchanged: `ground px → m` is a DECLARED GAP (OBS-H2-9); the video's ring and
the sim's radii are **not equated numerically** anywhere. No pixel scale is invented here either.

| gate | I-6 | **I-7** | video target | verdict |
|---|---:|---:|---:|---|
| **MG-1** ring median | 0 | **0** | 1 | MISSED |
| **MG-2** ring p90 | 4 | **4** | 3 | MISSED |
| **MG-3** ring **max** | 19 | **19** | **10** (R150) | MISSED, ratio **1.9×** |
| **MG-4** moving fraction | 0.8365970051012013 | **0.8365970051012013** | 0.883 | MISSED |
| **MG-6** longest stationary | 1.3877551020408165 s | **1.3877551020408165 s** | ≤ 1.40 s | **MET** |
| **MG-7** dash rate | 5.351766513056837 s / 93 | **5.351766513056837 s / 93** | 5.3235 s | **MET** |

**P.9 confirmed to the last digit.** Two of six MET, unchanged for a fourth iteration. Not a result
about the fold — the fold proving it stayed inside its own boundary.

---

## 12 — SENSITIVITY CELLS (diagnostics, NOT matrix cells)

| cell | what | mean HP | Δ vs reference | min HP (intra) | exc<0.70 (EOT/intra) | misses |
|---|---|---:|---:|---:|---:|---:|
| reference | run-of-record (O1 + S1) | 0.985925 | — | 0.32727 | 13 / 21 | 454 |
| **S-OA-ONLY** | **O1 alone** | 0.986275 | +0.000350 | 0.27636 | 12 / 16 | **430** |
| **S-SPD-ONLY** | **S1 alone** | 0.985925 | **+0.00000014** | 0.32727 | 13 / 21 | 456 |
| **⚑ S-OA-FLAT-ONLY** | **the Law-3 counterfactual** | 0.983682 | **−0.002243** | 0.32726 | 15 / 25 | **379** |
| S-CONV | HI DoT convention | 0.985856 | −0.000069 | 0.32727 | 13 / 21 | 454 |
| S-PCL | scale `percent_current_life` too | 0.984147 | −0.001778 | 0.31779 | 17 / **47** | 454 |

**⚑ Law-3 note, unchanged from I-6 and now with a second exhibit.** S-PCL and **S-OA-FLAT-ONLY** are
the two cells that move an observable meaningfully toward the video. **Neither is adopted.** S-PCL's
composition is UNDECODABLE-FROM-SUBSTRATE and not scaling is the lower reading; S-OA-FLAT-ONLY is
the *deliberate omission of a measured term that happens to point the wrong way for the target*.
**They are reported, priced, and left. Adopting either because it moves an observable toward a
target is precisely the shape Law 3 bars, and having two of them on the page at once is the clearest
statement of that I can make.**

---

## 13 — ⚑ WHAT GOES TO THE CONDUCTOR — three items, no HALT

1. **⚑ CLAUSE 2 READS MET, AND SO DOES CLAUSE 1 (§ 5).** R-PM4-15's trigger is therefore satisfied
   on **measurement**, which is what it was gated on. **I-8 = the converging solver
   (sequential-projection class) is the conductor's to charter**, and L-14 pre-authorised it on
   exactly this condition. My inputs are supplied with their sample size stated honestly (`n = 1`
   tick at max occupancy, backed by 46 `ARC > 1` ticks and 524 overlapping-ring ticks across 2,247
   occupied ticks).
2. **The reference baton cannot answer a question about the board (§ 5).** Its `tracks` are
   player-only. This is a *coverage* fact about the emission surface, and it is worth the
   conductor's attention because any future ruling of the form "measure it from the baton" hits the
   same wall. **Closure path if wanted: a per-tick actor-position track — a star-lord schema change
   (I do not touch that seam), and I would file the proposal rather than build it.**
3. **⚑ AND THE ONE I THINK MATTERS MOST: the residual is no longer on the monsters' side.**
   § 9.1 measures the player's sustain offering **118×** what the HP bar can absorb. A control cell
   added 4,157.70 damage and the end-of-tick HP statistics did not move **to sixteen digits**. Every
   remaining monster-offense term I could fold — C-I6-1's own-term, the per-type surface, cast speed
   — lands in the *numerator* of a ratio whose *denominator* is saturated, and the video's signature
   is a **persistently depressed** trace, which is a statement about **recovery**, not about intake.
   **My lean, offered as a lean and not a decision: I-9 should be the player's sustain limb**
   (ADCtH's 21 % against 1,595 kills, the regen rate, whether GD's leech is per-hit-capped) rather
   than a third offense fold. **I have not measured that and I am not asserting it** — but a fourth
   iteration spent adding intake to a model that heals it away inside one tick is priced, above, at
   zero.

**Also routed, minor:** **C-I7-1** — Lap I labels `characterOffensiveAbility` "%" on one table and
"flat" on the other (§ 2). Worth a Lap-I erratum so the next consumer does not have to re-derive it
from the equation. **C-I7-2** — the additive summation of the OA and speed chains is my extension of
Lap I's `DERIVED-SUM-ADDITIVE-BY-PARALLEL`; Lap I emitted no `sum_` column for either. **D-I7-3** —
`SlowManaLeach`'s closure path is an energy-ledger connection, i.e. a model addition, and I have
left it declared rather than improvised.

---

## 14 — REGRESSION

**480 / 480 PASS** on the full reverse-dependency closure of every module touched
(`kc2/offense.py`, `kc2/threat.py`, `kc2/run.py`, `export/kc2_run_adapter.py`, `data/kc2/`): the
twelve test files that reference `kc2`, `monster_stats`, `kc2_run_adapter` or `baton_v1`.
`kc2`-selected alone: 297/297. The 59 pre-existing reds in `test_cycle12_layer4_convergence.py` and
`test_cycle13_wave5_season_generation.py` are **rocket-seam** and were proven pre-existing at I-6 by
worktree replay on `e26f12b0`; nothing this lap touched can be imported by them.

---

## 15 — DECLARED ASSUMPTIONS + CLIFFS

**New this lap:** **C-I7-1** (`characterOffensiveAbility` unit ambiguity — decided FLAT on the
equation, § 2) · **C-I7-2** (additive summation of the OA/speed chains is a gamora extension of Lap
I's C-I3) · **D-I7-1** (I-6 § 6.1's evaluation point corrected; no number moved) · **D-I7-2**
(`SlowLifeLeach` map row closed with the module's own measured constant; proven no-op on both
cluster cells) · **D-I7-3** (`SlowManaLeach` DECLARED health-path exclusion, counted, closure path
named) · `characterSpellCastSpeedModifier` **+16 % NOT FOLDED** (one measured clock, and it is a
weapon swing; also the higher reading) · `skillCooldownReduction` **MEASURED ZERO** across the
reachable band, proven inert · `offensiveStunModifier` / `Freeze` / `Petrify` / `Trap` /
`offensiveSlowDamageMultModifier` **+40** / `retaliationTotalDamageModifier` — all named,
none folded, each with its reason.

**Carried unchanged:** C-I6-1 (**still very likely the largest single unfolded offense term** — the
creature's own granted modifier, MEASURED for band C only; folding it for C and not B manufactures
an instrument artifact at 171) · C-I6-2 (arena tier-18 wall) · C-I5-1…C-I5-4 (**the Jacobi pass
count UNTOUCHED per R-PM4-15**) · C-I4-1…C-I4-7 · C-I3-5 · C-I2-1 · C-E3 · C-D1/C-D3/R-PM4-6 ·
C-F1/C-F3/C-F4/C-F5 · C-G3 · C-G6 · **OBS-H2-9 (ground px → m)** · Lap I C-I1…C-I4 · P-STACK-A
(POLICY-NOT-MEASUREMENT, immaterial) · `percent_current_life` NOT scaled · wave 154's travel
outlier, undiagnosed for an **eighth** lap.

**⚑ LAW 3 — `moved: {}`.** No constant is added, removed or moved. Every number in § 3 traces to a
named cell of `pm4i_wave_damage_modifier.csv` / `pm4i_ultimate_offense_paks.csv`; D-I7-2 joins an
existing measured constant to the family it is named for. **Nothing in this lap was chosen because
it moves T1–T4 — and § 4 and § 12 are the proof, since the fold's own headline is that the term the
ruling advertised does nothing, and the two cells that WOULD have moved the numbers toward the
target are the two I refused to adopt.**
