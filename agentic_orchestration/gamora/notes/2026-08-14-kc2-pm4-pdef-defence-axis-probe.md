# KC2-PM4 · **P-DEF** — THE DEFENCE-AXIS PROBE

**Author:** gamora · **Conductor:** gandalf (RUN-CONDUCTOR) · **Commission:** R-PM4-49 part 5
**Date:** 2026-08-14 · **Frames:** `D-I19-8` (decode) · `D-I19-7` (frame)
**Class:** PROBE — no fold, no new mechanic, no tuning (Law 3). **Zero production lines edited.**

---

## 0 — THE HEADLINE, IN FOUR LINES

1. **`D-I19-8` is `A′ · INERT BY REACH`** — neither A nor B as chartered. The wire is **LIVE**, the
   term **FIRES**, and it **reaches no body**. The banner's ×2 is produced 6 times per ladder and
   consumed 0 times.
2. **No banked verdict moves.** I-18 and I-19 measured the axis correctly. It measured zero
   because it **is** zero on these boards — and I-18 is closed by **re-measurement**, not by
   inheritance.
3. **`D-I19-7` is `(i) a genuine model excursion`** — but **not a NEAR-arm fact**, and the
   tripwire's own message misattributes it. The **board** leaves the arena first; the player is
   dragged after it; and what carries him past his own reachable set is the **measured dash
   layers**, not the seek policy.
4. **One sub-defect found and not repaired:** `simulate_wave(defenses_enabled=…)` is a **dead
   parameter**. It deceived no measurement, because it is not the live control.

---

## 1 — WHY THE NEGATIVE ALONE COULD NEVER HAVE ANSWERED THIS

The charter names two hypotheses. **Both of them predict the same observation.** "Identical output"
is what an inert term looks like *and* what an unwired flag looks like. Reading the null harder
does not separate them; it just produces a longer null.

The discriminator is a **positive control**: put the player where the term *does* engage and see
whether the output moves. Two were built, and both were written into the script **before any number
existed** — the design is in the module docstring, above the code, with the reasoning stated.

This is the same shape as the I-19 `D-I19-6` catch: the instrument has to be able to fail before
its pass means anything.

---

## 2 — `D-I19-8`: THE EVIDENCE CHAIN

### 2.1 — Static wiring census (AST, not grep)

`ast.Name` **LOADS** inside the declaring function body — a grep counts docstrings and comments, a
LOAD count cannot.

| site | loads | verdict |
|---|---:|---|
| `run.py::simulate_wave(defenses_enabled)` | **0** | ⚑ **DEAD PARAMETER — declared, never read** |
| `run.py::simulate_wave(defence_field)` | **4** (L1896, L1897, L2954, L2955) | live |

So `defenses_enabled` is vestigial. **It is not the live control and it never was.** Every driver
call site moves `defences=` and `defence_field=fld(defences)` **together**, so no measurement was
ever deceived by it. Reported, **not repaired** (NOTE-9).

The live chain, end to end, is intact:

```
defence_field.player_damage_multiplier((px,py), k)          run.py:1896   (every tick)
  -> dmg_mult
  -> PlayerOffense.damage_against(record, dmg_mult)         run.py:2007   (per body HIT)
       -> raw * banner_factor(dmg_mult)                     player_offense.py:435
  -> PlayerSustainFold.heal_basis_against(…, dmg_mult)      run.py:2016
```

Nothing is shadowed. Nothing is scoped wrong. **Hypothesis B is dead at the AST.**

### 2.2 — Geometry receipt

| purchase | name | xy | aura r | player dmg % | note |
|---:|---|---|---:|---:|---|
| 1 | Deathchill Beacon | (+10.5934, +8.4446) | 0.0 | 0.0 | skipped by `if r <= 0.0: continue` |
| 2 | Stormcaller Beacon | (−14.8583, −11.3641) | 0.0 | 0.0 | skipped |
| 3 | Inferno Beacon | (+1.6831, −19.8278) | 0.0 | 0.0 | skipped |
| **4** | **Vanguard Banner** | **(−5.1529, −3.0014)** | **8.0** | **+100.0** | **the only object that can return ≠ 1.0** |

Player camp is `(0.0, 0.0)`. **Distance camp → banner = 5.9633 m < 8.0 m.** The camp is *inside*
the tether. That single fact is what makes control 3b possible with zero invented constants.

### 2.3 — ⚑ THE NEGATIVE IS **NOT** WHAT I EXPECTED, AND THAT IS THE FINDING

The lazy version of hypothesis A — *"the player is never in the tether"* — is **FALSE**, and the
probe's first pass killed it:

```
banner_tether_ticks = 6          occupancy 0.002513
min player→banner  = 6.2718 m    (< the 8.0 m aura)
```

The field **fires**. The multiplier **is 2.0** on six ticks. And the scorecard is still identical
to the digit. So the null lives one layer deeper, and the probe went and got it — a census of the
multiplier at **both ends** of the chain:

| | value |
|---|---|
| ticks evaluated | **2388** |
| multiplier histogram | **`{2.0: 6, 1.0: 2382}`** |
| hot ticks (within-wave index) | **`[1, 2, 3, 4, 5, 6]`** — wave 151 only |
| `damage_against` calls | **3852**, multipliers **`{1.0: 3852}`** |
| `heal_basis_against` calls | **3852**, multipliers **`{1.0: 3852}`** |
| **non-unit multiplier reaching a body** | ⚑ **0 calls** |

**The mechanism, exactly.** The player spawns at camp, 5.963 m from the banner, inside the 8.0 m
aura. The seek policy immediately walks him *away* from it:

```
k=1  mult=2.0  d_banner=6.2718   k=5  mult=2.0  d_banner=7.5164
k=2  mult=2.0  d_banner=6.5816   k=6  mult=2.0  d_banner=7.8293
k=3  mult=2.0  d_banner=6.8924   k=7  mult=1.0  d_banner=8.1428   <- exit
k=4  mult=2.0  d_banner=7.2040
```

**The tether dwell is 6 ticks = 0.4898 s, once, at the start of wave 151.** And in that window the
board is empty of anything the disc can hit — the sim's own measured arrival ramp (I-19 § 8) puts
t→50 % at **5.80–16.73 s**, and even the *referent's* is **3.27 s**. The dwell is an order of
magnitude shorter than the fastest arrival **on both clocks**, which is why this null is robust and
not a coincidence of one seed.

> ⚑ **The ×2 is real, it is live, and it lands on an empty board.**

### 2.4 — Re-derivation, because a counter is not a measurement (Discipline #11)

The occupancy was recomputed from `tracks.player_path_*` — a different object, computed a different
way — and made to agree or disagree in public:

| | field counter | re-derived from tracks | agree |
|---|---:|---:|---|
| ticks total | 2388 | 2388 | ✓ |
| tether ticks | 6 | 6 | ✓ |

### 2.5 — ⚑ THE POSITIVE CONTROLS. THIS IS THE LEG THAT DECIDES IT

**3a · SYNTHETIC (wire test).** Banner aura 8.0 → 1000 m, one in-process shim, nothing else moved.
Multiplier becomes 2.0 on every tick (occupancy **1.000**).

| | defoff | banner ×2 everywhere |
|---|---|---|
| terminal | `player_death@156` | **`arena_tier_exhausted@154`** |
| l4l 151–160 | 194.9388 s | **90.0408 s** |
| waves | 6 | **3** |

**3b · REAL GEOMETRY (zero invented constants).** `CAMP_THEN_COLLECT` + `defences=True`. The camp
sits inside the true 8.0 m aura, so occupancy is **1.000** on the *measured* radius. Event counts
diverge wave by wave (w151 **896** vs **1025**; w152 2327 vs 2301; w153 1801 vs 1825; w154 3612 vs
3672) — fewer damage rows under ×2, because bodies die in fewer ticks.

**Both positives fire. `wire_is_live = True`.** The wire is not merely present in the AST; it moves
the run when the geometry lets it. **Therefore the null on the cluster cells is a fact about the
board, not about the code.**

### 2.6 — Matrix-wide, because the claim is matrix-wide

A null measured on one arm and generalised by argument is exactly the move this run refuses. All
**eight** `defon` arms of the I-19 matrix:

| arm | terminal | ticks | hot | hot idx | **reach** |
|---|---|---:|---:|---|---:|
| COUPLED · PX-LO · NEAR | `player_death@152` | 633 | 6 | 1–6 | **0** |
| COUPLED · PX-LO · RING | `player_death@155` | 1714 | 6 | 1–6 | **0** |
| COUPLED · PX-HI · NEAR | `player_death@152` | 431 | 6 | 1–6 | **0** |
| COUPLED · PX-HI · RING | `player_death@152` | 563 | 6 | 1–6 | **0** |
| DECOUPLED · PX-LO · NEAR | `player_death@156` | 2388 | 6 | 1–6 | **0** |
| DECOUPLED · PX-LO · RING | `player_death@156` | 2077 | 6 | 1–6 | **0** |
| DECOUPLED · PX-HI · NEAR | `arena_tier_exhausted@154` | 1305 | 6 | 1–6 | **0** |
| DECOUPLED · PX-HI · RING | `player_death@155` | 2037 | 6 | 1–6 | **0** |

`ALL_ARMS_ZERO_REACH = True`. **All eight terminals reproduce the banked I-19 matrix exactly** — a
free determinism cross-check the probe did not set out to buy.

### 2.7 — ⚑ I-18 CLOSED BY MEASUREMENT, NOT BY INHERITANCE

*"The wiring is unchanged, therefore the I-18 null carries"* is an **argument**. The probe re-ran
the **I-18 configuration** (`advance=False`, `NEAREST_NODE`) and required it to reproduce I-18's
banked cell values **before** reporting a census:

| arm | l4l banked I-18 | l4l recomputed | reproduces | hot | reach |
|---|---:|---:|---|---:|---:|
| COUPLED · PX-LO | 50.04081632653062 | 50.04081632653062 | ✓ | 6 | **0** |
| COUPLED · PX-HI | 155.34693877551024 | 155.34693877551024 | ✓ | 6 | **0** |
| DECOUPLED · PX-LO | 165.3061224489796 | 165.3061224489796 | ✓ | 6 | **0** |
| DECOUPLED · PX-HI | 155.51020408163268 | 155.51020408163268 | ✓ | 6 | **0** |

`ALL_FOUR_REPRODUCE_I18 = True` · `ALL_FOUR_ZERO_REACH = True`.

### 2.8 — ⚑ WHAT THE LEDGER SAYS ABOUT THE BANKED VERDICTS

**NOTHING CHANGES.** No I-18 or I-19 verdict is touched, softened, or withdrawn.

Both laps ran the defence axis correctly and reported what it measured. The axis measured zero
because it **is** zero on these boards. The honest correction is not to the verdicts — it is to
what the matrix *thought it was buying*: four cells of every matrix were duplicates, and the run
paid compute for a column that could not carry information given where the player stands. That is
a **design** cost, banked at I-19 by my own reading of my own output, and it is now priced.

---

## 3 — THE I-20 MATRIX CONSEQUENCE

**The defence axis MAY be pruned at I-20, and the justification is decode-grade** — with one
condition that must ride with it in the ledger, because it is the difference between a true
statement and a convenient one:

> **It is INERT BY REACH, not inert by truth.** The banner is not a dead object. It is a live ×2
> whose 0.49 s of player-occupancy does not overlap any arrival on this ladder.

Consequences that follow from that phrasing and not from the loose one:

1. **The prune is CONDITIONAL ON THE BOARD.** Any I-20+ change that (a) slows the player out of
   camp, (b) speeds arrivals up — **which is precisely what Lap T's arrival decode is chartered to
   do (R-PM4-49 part 4)** — or (c) moves the camp or the banner, can make the axis live again.
   ⚑ **Lap T is the single most likely thing in this run to un-prune this axis.** If Lap T lands a
   beacon speed magnitude or a faster march, the first six ticks of wave 151 stop being empty.
2. **The prune must be re-verified, not assumed, after Lap T lands.** The check is cheap: the
   reach census is one number (`n_calls_with_non_unit_multiplier`) and it is now a committed
   instrument.
3. **`camp_defoff` is untouched by this.** The camp control never had a `defon` twin, and control
   3b shows exactly why it would not have been a duplicate: a camping player is inside the tether
   **the whole time**. The pruned axis is redundant *for the cluster geometry only*.
4. **Recommended I-20 shape:** drop the `defon`/`defoff` split from the cluster column, keep the
   `defence_field` **wired and ON** in the surviving cell (so the telemetry key and the instrument
   both stay live), and carry the reach census as a standing assertion.

---

## 4 — `D-I19-7`: THE FRAME

**VERDICT: `(i)` a GENUINE MODEL EXCURSION. Not an instrument artifact. NOT a NEAR-arm fact.**
And the tripwire's own message — *"The seek policy ran away"* — **misattributes it.**

### 4.1 — The arithmetic, pre-registered before the run

A seek step is `p' = p + (b−p)/|b−p| · moved` with `0 ≤ moved ≤ |b−p|`, so `p'` lies on the segment
`[p, b]`. The Euclidean ball is convex, therefore

```
|p'| <= max(|p|, |b|)                                    (CONVEXITY BOUND)
```

Every spawn is inside 45.06 m. So **if** bodies stay inside 45.06 m, the player's offset is
non-increasing above 45.06 m and 80 m is unreachable by seeking. The trip **requires** a body
outside — which makes the branch decidable by one number.

### 4.2 — What the trace says

**ZERO convexity violations in ~13,000 traced steps across all eight arms.**
`zero_convexity_violations_on_every_arm = True`. **The seek law is exact.** It is not the culprit.

**The BOARD leaves the arena first.** Drift census, all eight arms:

| arm | terminal | max player | max body | roster >45.06 | roster PLACED | pet >45.06 | pet PLACED |
|---|---|---:|---:|---:|---:|---:|---:|
| COU·PX-LO·NEAR | death@152 | 60.38 | 55.97 | 14 | **0** | 32 | 12 |
| COU·PX-LO·RING | death@155 | 77.27 | 68.90 | 34 | **0** | 58 | 16 |
| COU·PX-HI·NEAR | death@152 | 29.33 | 43.21 | 0 | 0 | 0 | 0 |
| COU·PX-HI·RING | death@152 | 47.37 | 43.20 | 0 | 0 | 0 | 0 |
| DEC·PX-LO·NEAR | death@156 | **80.00** | 79.72 | 71 | **0** | 180 | 83 |
| DEC·PX-LO·RING | death@156 | **79.71** | 78.16 | 38 | **0** | 66 | 23 |
| **DEC·PX-HI·NEAR** | **trip@154** | **79.70** | 78.40 | 14 | **0** | 60 | 25 |
| DEC·PX-HI·RING | death@155 | **80.00** | **80.89** | 66 | **0** | 155 | 71 |

Four facts fall straight out:

1. **Six of eight arms have boards outside the spawn envelope.** ⚑ **ZERO roster bodies are ever
   PLACED beyond 45.06 m — 14 to 71 per arm WALK there.** The monster pursuit law has no
   containment term. Pets *are* placed beyond (12–83/arm), because their summoners already are.
2. ⚑ **The player OVERSHOOTS HIS OWN REACHABLE SET.** On the defect cell his max offset is
   **79.704 m** against a seek-reachable bound of **78.396 m** — **1.308 m he cannot have walked.**
3. ⚑ **And here is what put him there.** The seek step is not the only writer of the player's
   position: `move_policy.apply()` (the I-4 cadence + three **MEASURED** dash layers) and the I-3
   geometry clip both run after it in the same tick. Measured on the defect cell:

   | | value |
   |---|---:|
   | ticks where something other than the seek step moved the player | **121 / 1306** |
   | net **outward** displacement not written by the seek law | **+205.42 m** |
   | inward (the I-3 clip shortening a blocked step) | −15.34 m |
   | **largest single gap** | **15.995 m** |

   `15.995 m` is **`Violent Delights`**, `records/skills/itemskillsgdx2/runes/rush_d203.dbr`,
   MEASURED `range_m = 16.0`, cooldown 2.5 s (Lap G). The other two layers are `Vire's Might`
   (12.0 m) and `Evade` (10.0 m). **The dashes carry him past the body cloud; the seek law never
   could.**
4. ⚑ **The tripwire watches the WRONG ACTOR.** `PLAYER_SANE_BOUND_M` is player-only. On
   **DEC·PX-HI·RING the BOARD reaches 80.89 m — past the sane bound — while the player sits at
   80.00 m and does not trip.** The instrument fires on the *second* actor to leave the arena.

**And it is not a NEAR-arm fact.** Four arms are parked at **79.70–80.00 m**, i.e. three of them
sit within 0.30 m of a hard terminal without tripping (the bound is a strict `>`). NEAR and RING
both appear at the top of that list. **Which arm trips is a coin-flip of the drift, not a property
of the NEAR geometry.** The charter's phrasing — *"the NEAR-arm geometry legitimately walks the
player past 80 m"* — is measured **FALSE**; the correct statement is that *the board* walks out and
the player follows on any arm that lives long enough. The two arms with no drift at all
(COU·PX-HI·NEAR/RING) simply die at wave 152 before it can develop.

### 4.3 — Diagnostic widening (NOT ADOPTED)

`run.PLAYER_SANE_BOUND_M` 80.0 → 1e9, in-process, one call, never adopted, never scored:
the player reaches **100.39 m**, the board **93.42 m**, non-seek outward displacement **+519.61 m**
over 271/2676 ticks — and the ladder then ends **normally** at `player_death@156`. So the bound
trip is not a terminal state of the model; it is a tripwire crossing a *drifting but otherwise
healthy* run. **This says the DEC·PX-HI·NEAR cell's `arena_tier_exhausted@154` is an INSTRUMENT
terminal sitting on top of a run that had four more waves in it** — which is worth knowing before
anyone reads that cell's short ladder as a difficulty signal.

**NOT REPAIRED (NOTE-9).** Framed, evidenced, routed. Repairing either half — the containment or
the bound — mid-run would make I-18 and I-19 unreachable, and the drift is not this probe's
mechanism to fold.

### 4.4 — What I am NOT claiming

I have not decoded *why* the mutual pursuit drifts outward rather than settling, and I have not
measured whether the referent's own board does the same. Both are real questions and neither is
answered here. What is measured is: the board leaves, the player follows, the dashes overshoot,
and the bound watches only him.

---

## 5 — LAW 3 / NOTE-9 COMPLIANCE

| | |
|---|---|
| production lines edited | **0** |
| constants moved | **0** |
| folds adopted | **0** |
| defects repaired | **0** (three named: `defenses_enabled` dead param, board drift, player-only bound) |
| in-process widenings | 2 — banner aura 8.0→1000 (wire test), `PLAYER_SANE_BOUND_M` 80→1e9 (diagnostic). Both named at their patch site in code, both reversed in a `finally`, **neither adopted** |
| frozen substrate `E-s09-cp150` | **untouched** |
| banked I-18/I-19 artifacts | **unmodified** (re-hashed before use, read-only) |
| `export/` | **untouched** |

**Smoke (Discipline #2):** kc2 suite **296 passed, 1 failed** — the **same one pre-existing
failure** recorded at I-18R and I-19
(`test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface`, `secondary_streams.py:136`).
Zero production drift.

---

## 6 — ARTIFACTS (GL-6, full digests)

| artifact | sha256 |
|---|---|
| `src/reincarnated/simulation/scripts/gamora_kc2_pm4_pdef_defence_axis_2026_08_14.py` | see commit `975eaa72` |
| `src/reincarnated/simulation/output/kc2-pm4-pdef-findings-20260814_165633.json` | `2e5c56429e99acdacf23ea3d2b17ac37e71ba624e158d68243ce8c70d9fcf776` |

**Inputs re-hashed before use:**

| input | sha256 |
|---|---|
| `kc2-pm4-i18-findings-20260814_105832.json` | `8cb394607bb2d492a99ba9987a08918902001ff946a0e326d5e3342b874175bd` |
| `kc2-pm4-i19-findings-20260814_162041.json` | `59c6c85befdb4294e9b51e2353ffa6786e40bb4dfb61b33a2eb5fde8702d13e9` |

Four intermediate findings files were emitted while the instrument was being built (the reach leg,
the matrix sweep, the I-18 leg and the non-seek displacement leg were each added after the previous
run's result demanded them) and were **deleted** in favour of the final artifact, which contains
every leg. Stating it rather than leaving five near-duplicate files with no account of their
relationship. All of them are reproducible from the committed script.

Probe wall time **83.5 s** (20 ladders + 2 traced ladders). No full regen. No re-run of the I-19
matrix.

---

## 7 — CARRIED / ROUTED

| id | state |
|---|---|
| `D-I19-8` | **CLOSED — A′ INERT BY REACH.** Wire live, term fires, reach zero, matrix-wide, I-18 and I-19 both re-measured. No banked verdict moves. |
| `D-I19-7` | **FRAMED — (i) genuine excursion, board-caused, dash-carried, player-only tripwire.** Not repaired. |
| **NEW · `D-PDEF-1`** | `simulate_wave(defenses_enabled=…)` is a **dead parameter** (0 AST loads). Vestigial; deceived no measurement. Not repaired. |
| **NEW · `D-PDEF-2`** | **No containment on monster pursuit.** Roster bodies walk to 78–93 m from a 45.06 m spawn envelope on 6/8 arms; pets are then *placed* out there. Not repaired. |
| **NEW · `D-PDEF-3`** | **`PLAYER_SANE_BOUND_M` is a player-only tripwire** and fires on the second actor to leave the arena. On DEC·PX-HI·RING the board is at 80.89 m and nothing complains. Not repaired. |
| **NEW · `U-PDEF-1`** | Why the mutual pursuit drifts **outward** rather than settling is **undecoded**, and whether the referent's board does the same is **unmeasured**. Named, not guessed. |
| **I-20 gate** | Defence axis **MAY** be pruned — **conditionally**, and Lap T's arrival decode is the most likely thing to un-prune it. Re-verify with the committed reach census after Lap T lands. |
