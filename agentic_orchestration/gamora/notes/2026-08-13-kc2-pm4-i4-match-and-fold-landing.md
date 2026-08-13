# KC2-PM4 · I-4 — landing note: **the counterplay stack works, and it works too well to measure.**

> **Run:** KC2-PM4 · **Iteration:** I-4, MATCH-AND-FOLD · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-13
> **Fired under:** Matt's **R-PM4-11** (*"review the fight video … and match what occurs there"*)
> and the conductor's **R-PM4-12** (Jacobi push-apart is run-of-record).
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
> (ledger **L-10**).
> **Math note (Discipline #1, written BEFORE the code; twelve pre-registered predictions, nine
> match gates, and a § I of post-hoc corrections that leaves every falsified claim standing):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i4-match-and-fold-2026-08-13.md`
> **Status:** COMPLETE with **one named HALT** (D-I4-5, § 8). Assert wall **15/15 PASS**,
> determinism ×2 **EXACT** on all three cells (**0 differences**), check 1 byte-exact against a
> clean worktree. **No constant was tuned; the Law-3 witness is now ELEVEN and `moved: {}`.**

---

## 0 — The one-paragraph answer

**Every measurable limb is now folded, and the run has stopped being able to fail.** With the
DECODED counterplay stack in place — Turtle Shell, Arcane Barrier, Menhir's Will, the potion,
War Cry, Ascension's absorb, four of them on triggers that need no policy at all — **the player
does not die anywhere inside the measured substrate.** All three cells run off the end of the
eHP band at **wave 171** with mean HP **99.2 %**, against a baseline that died on **wave 160 at
198.20 s**. That is not a near-miss on T1; it is T1 becoming **unmeasurable**, because the death
wave is now **unbounded above** and the substrate stops at 170 (C-D2). **And it is not an artefact
of a generous limb**: the same result holds under the strict zero-parameter LOWER bracket of the
one undecided term (absorb duration), and it holds under the **movement fold alone with no
counterplay at all**. Lap G § 6.1's arithmetic — *Σ automatic layers ≈ 18,900 against a 20,861
terminal intake* — is confirmed and then some: over the ladder the layer absorbs **253,867** and
War Cry removes a further **239,659** of **1,206,271** raw. **T4b's four-lap residual is closed and
it took T1 and T2 with it.** The match gates moved in the predicted directions and met two of
seven: ring-density max **22 → 19** (target 10), moving fraction **0.931 → 0.842** (target 0.883),
the measured stationarity cap **1.40 s** now an enforced invariant, and the dash rate **MET** at one
per 5.353 s against a measured 5.3235.

---

## 1 — ⚑ THE PRE-RUN MEASUREMENT THAT CORRECTED THE COMMISSION'S OWN PREMISE

The commission states *"The sim player currently sits pinned."* I measured it before writing
anything, because the fold's whole shape depends on it. **It is true of the CAMP control and false
of the reference cell.**

| quantity | sim baseline | video | direction |
|---|---:|---:|---|
| moving fraction | **0.931** | **0.883** | sim moves **MORE** |
| median tick speed | **5.400 m/s** = the cap | — | flat out |
| bouts | **31** / 198.20 s | **107** / 181.0 s | 3.5× less broken up |
| *mean* bout | **5.95 s** | **1.49 s** | ⚑ the real gap |
| longest stationary | **2.69 s** | **1.40 s** | sim **violates** the cap |
| CAMP control | **0.000** | — | the "pinned" premise lives HERE |

**The sim's player was never pinned — he was a constant-speed centroid-chaser**, running at the cap
in a few enormous unbroken legs. The divergence I-4 had to close was the *grain* of his motion and
where it points, not whether it exists. Had I taken the premise on trust I would have built a
movement model to solve a problem the reference cell did not have.

---

## 2 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 12 predictions, 9 match gates, § I corrections) | `simulation/math/kc2-pm4-i4-match-and-fold-2026-08-13.md` | `6b37843f` |
| 2 | **`kc2/movement.py`** — cadence loader, dash layers, M-1…M-4, the derived stationary predicate | new | `6b37843f` |
| 3 | **`kc2/counterplay.py`** — six layers, the HP-trace threshold decode, the conservation identity | new | `6b37843f` |
| 4 | `kc2/run.py` — the three folds, the ring-density instrument, kit-state threading | modified | `6b37843f` |
| 5 | `kc2/locomotion.py` — the D-I4-2 knot amendment | modified | `550264dc`, `b1a14a03` |
| 6 | `export/kc2_run_adapter.py` — 3 spec fields, 3 specs, `_player_fold_state` | modified | `6b37843f`, `3c8a74a3` |
| 7 | **driver + assert wall (15) + determinism + 5 diagnostics** | `simulation/scripts/gamora_kc2_pm4_i4_match_and_fold_2026_08_13.py` | `6b37843f` |
| 8 | **7 vendored substrate CSVs**, byte-identical, SHA-pinned | `data/kc2/pm4h2_*.csv`, `data/kc2/pm4g_*.csv` | `6b37843f` |
| 9 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `6b37843f` |
| 10 | **3 knot supplies + findings** | `simulation/output/…20260813_131435.json` | `b1a14a03` |

**Artifacts of record (stamp `20260813_131435`):**

| what | sha256 |
|---|---|
| findings | `5e3e38b7f980f98e18deb42d22b9722e4d5cd5af4c28850211bd9ad343b8ed18` |
| knots CAMP/DEF-OFF | `06dc0144ccdff3f98592f1d7b42b2e70a71ce8606f64d932ef07fa65e5be5237` |
| knots CLUSTER/DEF-OFF | `02cd81f6a81821c1cd01bfa297caf2c3171cb008ab676944082970cf794ad74a` |
| **knots CLUSTER/DEF-ON** ← reference | `4df84fc76b1ee6a815ec8fa3f6db4e2a328652dd597989bca29d72e9e5e6ce21` |

⚑ **No I-4 batons — see § 8 (D-I4-5).** Engine `7b5c31b9 → 1f23357d`, six commits, **PUSHED**.

---

## 3 — ⚑ CHECK 1: THE DELTA IS EXACTLY THREE THINGS, AND THE BASELINE WAS MEASURED, NOT REMEMBERED

R-PM4-12 promoted an arm that I-3 ran as a **diagnostic** and never emitted as a baton — so there
was no recorded digest to compare against. I built one: a **clean `git worktree` at pre-I-4 HEAD
`7b5c31b9`**, replaying all three cells under `contact_response="separate"`.

| cell | pre-I-4 worktree digest | I-4 fold-OFF replay | |
|---|---|---|---|
| CAMP/DEF-OFF | `07390573179fd6f8…` | `07390573179fd6f8…` | **EXACT** |
| CLUSTER/DEF-OFF | `1c7e45cf256e2120…` | `1c7e45cf256e2120…` | **EXACT** |
| CLUSTER/DEF-ON | `1a5f54ebbfec55b1…` | `1a5f54ebbfec55b1…` | **EXACT** |

It runs FIRST and HALTs the lap on mismatch — **and it fired.** My first build added
`contact_response` to `waves[].body_geometry`, a key that looks free and is not: it moves the
fold-OFF wave dict. Check 1 went RED on the first cell and the key came straight back out.

**Determinism ×2, SIM layer, every cell: 0 differences** (`8452a547…` / `62ce6972…` / `2644e4c0…`).

---

## 4 — ⚑ THE MATCH GATES (INTERMEDIATE observables, judged SEPARATELY from T1–T4)

| gate | baseline | **I-4** | video target | verdict |
|---|---:|---:|---:|---|
| **MG-1** ring density median (d_engage) | 0 | **0** | **1** | MISSED |
| **MG-2** ring density p90 | 4 | **4** | **3** | MISSED |
| **MG-3** ring density **max** | **22** | **19** | **10** (R150) · 12 (R180) | MISSED, ratio **1.9×** |
| MG-3b max, disc basis | 32 | **31** | 12 (R180) | reported |
| **MG-4** moving fraction | 0.931 | **0.842** | **0.883** | MISSED (sim now **under**) |
| **MG-5** bouts / median bout | 31 / 0.33 s | **331 / 1.469 s** | 107 / 1.033 s | reported (C-I4-6) |
| **MG-6** longest stationary | **2.69 s** | **1.3878 s** | **≤ 1.40 s** | **MET** — one tick under the cap |
| **MG-7** dash rate | — | **95 dashes, 5.353 s apart** | 5.3235 s | **MET** |
| **MG-8** D1 signature | see below | see below | see below | direction **MET**, magnitude MISSED |
| **MG-9** corpses ghost | — | **0 violations / 1,592 deaths** | CONFIRMED on camera | **MET** |

⚑ **NOTE-9 on every ring number, and it is load-bearing.** `ground px → metres` is a **DECLARED
GAP** (OBS-H2-9). The video's 150-ground-px ring and the sim's radii are **not equated numerically
anywhere in this fold**. The correspondence is **SEMANTIC**: the video calibrated *"bodies whose
sprites abut the player"*; `D_ENGAGE_M = 2.4` is the DB's own `meleeTargetDistance`. Declared
pairings: video R150 ↔ sim d_engage, video R180 ↔ sim disc. The video's counts are **lower bounds**.

### 4.1 — the D1 signature: the direction is right and the far field is structurally wrong

| range band | sim median \|v_t\|/\|v\| | | video band | video |
|---|---:|---|---|---:|
| 40–120 m | **0.014** | | 900–1400 gpx | **0.388** |
| 20–40 m | 0.015 | | 600–900 gpx | 0.529 |
| 10–20 m | 0.023 | | 400–600 gpx | 0.549 |
| 6–10 m | 0.046 | | 300–400 gpx | 0.569 |
| 4–6 m | 0.082 | | 220–300 gpx | 0.611 |
| 2.4–4 m | 0.168 | | 150–220 gpx | 0.660 |
| **0–2.4 m (the ring)** | **0.430** | | **100–150 gpx (the ring)** | **0.739** |

**The measured law is reproduced in sign and in monotonicity**: median radial speed collapses to
**exactly 0.000** at the ring while the tangential fraction rises monotonically across all seven
bands. It is under-produced in magnitude, and the mechanism is nameable rather than mysterious:
**the sim's pursuit is straight-line by declaration**, so its far-field tangential fraction is 0.014
where the game's is 0.388. **I did not close that.** Manufacturing far-field lateral wander to move
a measured ratio toward the reference is exactly the fitting the charter bars.

---

## 5 — ⚑ THE T-BAND SCORECARD, AND THE CAVEAT THAT DOMINATES IT

> **⚑ TERMINAL REASON: `ehp_band_exhausted` AT WAVE 171. THE PLAYER DID NOT DIE.**
> The ladder walked off the end of the MEASURED substrate (Lap D/E emit waves 151–170; C-D2 parks
> the G(171) = 420 discontinuity). **Every band that names a death is reported against that fact
> rather than scored against the last wave simulated.** The caveat is on the wire as
> `scorecard.⚑ terminal_reason`, so it cannot be dropped downstream.

| band | verdict | number |
|---|---|---|
| **T1** survival depth (160) | **MISSED — and UNMEASURABLE** | no death by wave 170; the death wave is **unbounded above** within the substrate. Baseline died on **160** |
| **T2** 186 s ±15 % | **MISSED** | 508.57 s over **20** waves; **`like_for_like: false`** — this is not a ten-wave fight's duration |
| **T3** pacing shape | **NEAR** | median ratio **1.189** (baseline 1.127); Pearson **r = +0.020** over 10 comparable waves |
| **T4a** sustain | **MET** | mean HP **99.19 %** (baseline 96.53) |
| **T4b** terminal mechanism | **MISSED — but for the first time it is missing because there is no terminal** | last wave **20.16 s** with **1,085** player damage rows; DoT share **0.05 %** |

**Waves 151–160 like-for-like** (the honest comparison basis, carried from I-3; measured from the
findings' own `per_wave_s`, not from memory): the sim spends **227.755 s** on the reference's ten
waves against the measured **186 s**, i.e. **+22.4 %** — far inside I-3's block-arm result
(+75.7 %), outside the ±15 % band, and above the push-apart baseline's **198.204 s / +6.6 %**.
CLUSTER/DEF-OFF on the same basis: **215.837 s / +16.0 %**. **That is the number T2 would report if
the ladder had stopped where the reference did**, and it is stated here so the 508.57 s figure
cannot be mistaken for a comparable quantity.

---

## 6 — ⚑ WHERE THE COUNTERPLAY WENT (the arithmetic Lap G predicted, measured)

| layer | firings | absorbed / healed | note |
|---|---:|---:|---|
| **K-2 Arcane Barrier** | **103** of 377 rolls | **253,357** | 30 % on-hit, 3.0 s cd — the workhorse |
| **K-5 War Cry** | **68** | **239,659** removed | greedy on-cooldown; −29 % on 9,133 events |
| **K-4 potion** | **1** | 5,801 instant + 5,035 over time | ⚑ the player almost never got low enough |
| **K-6 Ascension** | 22 | 510 | absorb clause only |
| **K-1 Turtle Shell** | **0** | 0 | ⚑ **HP never reached 50 %** |
| **K-3 Menhir's Will** | **0** | 0 | ⚑ **HP never reached 33 %** |
| | | **raw 1,206,271 → applied 712,744** | **41 % of all incoming damage removed** |

**Conservation identity holds** (`raw − warcry − absorbed = applied`, residual **−1.6e-10**, a float
summation residue at 1.3e-16 relative — reported as a bound, not claimed exact).
**Cooldown violations: 0**, re-derived from the emitted `heal_tick` timestamps rather than from the
layer's own clock.

⚑ **The two circuit-breakers Lap G called the headline never fired**, because Arcane Barrier and
War Cry between them stop the player's HP from ever reaching their triggers. That is a real,
falsifiable structural claim about the build, and it inverts P.10.

### 6.1 — decomposition, and both limbs overshoot independently

| diagnostic | terminal | ladder s | mean HP | reading |
|---|---|---:|---:|---|
| **baseline** (push-apart, no player fold) | **death @160** | 198.20 | 96.53 % | R-PM4-12's arm before I-4 |
| **movement only** (no counterplay at all) | band @171 | 508.57 | 97.31 % | ⚑ **dashing ALONE saves him** |
| **counterplay only** (no movement) | band @171 | 468.73 | 99.29 % | ⚑ **the kit ALONE saves him** |
| **absorb LOWER bracket** (C-I4-4, pools live one tick) | band @171 | 508.57 | 98.06 % | ⚑ **the overshoot is NOT the generous limb** |
| block-response sensitivity (retired arm) | band @171 | 765.31 | 99.10 % | reported, no second matrix |

**Two independent limbs each carry the player past the substrate, and the one undecided term does
not decide it.** This is the reading that matters for the run: the residual is not a knob, it is
two separately-sufficient measured mechanisms.

---

## 7 — ⚑ PRE-REGISTERED PREDICTIONS vs OUTCOME — **five confirmed, one split, six falsified**

| # | prediction | outcome |
|---|---|---|
| **P.1** | moving fraction 0.931 → **0.86–0.90**; bouts 31 → **90–130** | **SPLIT.** Fraction **0.842** — *below* my floor. Bouts **331**, 2.5× my ceiling. Both misses are the same error: I priced the cadence gate and never priced the *stationary predicate* it would need |
| **P.2** | ring median **0→1**, p90 **2–4**, max **12–20** | **CONFIRMED on two of three.** median **0** (missed the clause), p90 **4** ✓, max **19** ✓ |
| **P.3** | the cap BINDS: ≥ 40 firings, window ≤ 1.40 s | **SPLIT.** Window **1.3878 s** ✓ — exactly one tick under, which is what binding looks like. But only **5** firings: the cadence's own pauses break the runs long before 1.40 s, so the cap is a backstop, not a workhorse |
| **P.4** | ⚑ **THE HEADLINE — T1 misses LONG, death wave 162–172, centre 165** | **⚑ RIGHT ON DIRECTION, WRONG ON KIND.** There is no death wave. The player survives the whole measured band. I predicted a number where the answer is "the instrument ran out" |
| **P.5** | waves 151–160 like-for-like **230–300 s** | **FALSIFIED.** **221.7 s** — under my floor. I over-priced the dash's re-closure cost and under-priced how much faster a surviving player clears |
| **P.6** | T3 median ratio **1.30–1.90**, \|r\| ≤ 0.4 | **SPLIT.** r = **+0.020** ✓; median ratio **1.189**, below my floor — same error as P.5 |
| **P.7** | T4a MET, mean HP ≥ 97.0 % | **CONFIRMED. 99.19 %** |
| **P.8** | T4b's fought clause FLIPS (≥15 s, >0 rows); DoT clause still misses | **CONFIRMED on both clauses** (20.16 s, 1,085 rows, DoT 0.05 %) — **but the verdict is right for a reason I did not predict**: the last wave is not a terminal wave at all |
| **P.9** | ring tangential ratio **0.45–0.62**; far field ≤ 0.03 | **SPLIT.** Far field **0.014** ✓ exactly as declared; ring **0.430**, a hair under my floor of 0.45 |
| **P.10** | K-1 ≥20 · K-2 ≥100 · K-3 ≥5 · K-4 ≥15; total 60k–250k | **⚑ FALSIFIED, AND THE FALSIFICATION IS THE FINDING.** K-2 **103** ✓; K-1 **0**, K-3 **0**, K-4 **1**. The low-health breakers never fire because the on-hit layers stop HP ever getting low. Total absorbed + healed **264,703**, just over my ceiling |
| **P.11** | CAMP survives to wave 161–170 | **CONFIRMED at the edge.** CAMP reaches the band end at **171**, 1,940.65 s |
| **P.12** | DEF-ON/DEF-OFF spread grows to **2–10 %**, DEF-ON no longer faster | **FALSIFIED.** Spread **1.06 %** (508.57 vs 513.96) and DEF-ON is still the faster cell. The banner tether survives the dashing because the player returns to the pack between dashes |

**The unifying error, and it is a new shape.** I-1: priced sustain, not exposure. I-2: priced eHP,
not co-residence. I-3: priced throughput, not the monsters' reach. **Here I priced the SIZE of the
counterplay and never priced its SHAPE.** Every one of P.4/P.5/P.6/P.10 is wrong because I asked
"how much damage does the stack remove" and never asked **"what does removing it continuously do to
the triggers of the layers that only fire when it fails?"** The answer is that a build with enough
on-hit mitigation never reaches its own emergency buttons — and a player who never reaches them
does not die, so there is no death wave to predict.

---

## 8 — ⚑ DEFECTS. FIVE. **THREE WERE CAUGHT BY OTHER SEAMS' GATES OR BY MY OWN WALL.**

| # | what | how found | disposition |
|---|---|---|---|
| **D-I4-1** | **The stationarity cap used an EXACT-ZERO predicate where the measurement uses a THRESHOLD.** The CLUSTER policy's arrival homing produces ~1e-3 m steps, so the model believed the player was moving while the emitted path showed him parked: the cap fired **5×** and let a **1.469 s** window through a MEASURED **1.40 s** cap | **my own assert wall, check 4** | Fixed at the source with a DERIVED threshold — the ratio `60/397.6` (both ground-px/s, from the row of record, **dimensionless so it crosses the OBS-H2-9 gap legally**) × the frozen baseline mean tick speed = **0.74998 m/s**. Numerator read from the **column name**, not typed |
| **D-I4-2** | **Two knot vertices on one tick** — push-apart displaces a body after `step()`, so a marker knot and the next step's deferred `halt` land on one tick at two positions | **star-lord's F5-E loader** — *"knot ticks do not increase, and sorting them here would hide the defect"* | Knot-vocabulary amendment (Discipline #12), with **check 15 PROVING it INERT under the `block` response** by reproducing the pre-I-4 worktree's extracted-path digests byte-exactly |
| **D-I4-3** | **The adapter built FRESH per-wave kit objects** while the driver threaded one per ladder — ten free cooldown resets, a different cadence phase, different wave durations, and a replay forty ticks away from the pinned knot artifact | **the adapter's `_spawn_tick` F5-M/F5-E reconciliation** | ⚑ **MY FIRST DIAGNOSIS WAS WRONG AND IS RECORDED AS WRONG.** I read it as push-apart making stillness inexact and drafted a routing memo to star-lord. It was my own model error. Fixed at the source (`_player_fold_state`) |
| **D-I4-4** | **Two corpse audits that would have passed VACUOUSLY.** (a) the audit filtered on an event family that does not exist (`actor_death`; it is `death`) and returned a clean pass on a ladder with **1,592** deaths; (b) its repair's first predicate was too broad and counted **2,400** `dot_tick`-outlives-its-source rows as footprint violations | `n_deaths == 0`, which is not a number a real audit returns | Both fixed; the function now **REFUSES to report a pass when it found no deaths**. **Result: 0 violations of 1,592 deaths — OBS-H2-1 CONFIRMED by measurement.** *(Same shape as I-3's `damage_taken` basis error — twice in two laps)* |
| **⚑ D-I4-5** | **THE HALT. Push-apart is structurally incompatible with the one-vertex-per-tick path contract.** A body moves TWICE inside a tick: `step()` puts it at A, the disc resolves against A and every damage row carries A, then separation displaces it to B. A polyline in `run_tick` carries ONE position per tick and cannot represent both. Residual against the gate's 0.002 m tolerance: up to **0.09 m** | **star-lord's `G-LOCO-ONE-TRAJECTORY` + `R-LOCO-1-HITTEST`** — *"the baton is carrying TWO trajectories for one actor"* | **NO I-4 BATONS. § 8.1** |

### 8.1 — ⚑ D-I4-5, in full, because it is the item that goes to the conductor

I attempted two fixes and **both are in the source, including the wrong one**:

1. **Attempt 1** wrote the **POST**-separation position (`mark_knot("separate")`). **Wrong** — it
   moved the path *away* from the wire, because the damage rows carry the **PRE**-separation
   position. Reverted, reasoning left in place.
2. **Attempt 2** keeps the **FIRST** vertex of a tick (the position the hit test actually used) and
   merges the later kind onto it. **Better** — `damage-row-outside` falls **76 → 61** — and still
   RED, because the residual *is* the displacement.

**The real resolution is a TICK-ORDER CHANGE: `step → SEPARATE → resolve`,** so the non-overlap
invariant holds at the moment the world is observed and a body moves once per tick. It is also the
more defensible model — resolving the weapon against a configuration the invariant then repairs
means the damage was computed on an inadmissible board. **But it is a Discipline #12 causal-order
shift: it invalidates this lap's check-1 baseline and re-prices every number in the matrix.** That
is an ITERATION, not a tail-end patch, and it is the conductor's ruling. **The gate's halt text —
"nothing here is repaired by widening a tolerance" — was obeyed. Nothing was widened.**

The lap's record is therefore the **findings + knots artifacts**, both committed and digest-pinned
— the same standing I-3's push-apart arm had when it was a diagnostic. **It is now the arm of
record, and this is the first thing that promotion broke.**

---

## 9 — DECLARED ASSUMPTIONS + CLIFFS (all on the wire, all in the math note)

**New this lap:** **C-I4-1** EoR facing / `rotationSpeedMultiplier 0.35` has no referent — this EoR
is a radius spin with no facing; declared, skipped · **C-I4-2** Blitz OMITTED entirely (range is a
Lap-G declared gap; carrying it cooldown-only would consume a dash opportunity it cannot spend) ·
**C-I4-3** the potion threshold **0.49** is the max observed excursion minimum and is an UPPER BOUND
over ALL layers, not a point identification — it sits one point below Turtle Shell's own decoded
50 % trigger; the alternative reading (0.41) is registered and **NOT run** · **C-I4-4** absorb pools
persist until consumed — the **UPPER** limb, taken **against** this run's standing preference for
the lower reading **because the lower reading here requires inventing a duration and is therefore
fictional**; the strict lower bracket IS run as a sensitivity and does not change the outcome ·
**C-I4-5** the potion's over-time component is spread over the potion's own measured 12.0 s cooldown
(the LOWER limb) · **C-I4-6** the bout-duration DISTRIBUTION is reproduced only in its mean; the
skew is not decoded and is not invented · **C-I4-7** the movement fold is REFUSED on CAMP by
construction, which makes CAMP the counterplay-only isolation cell.

**⚑ DECLARED-NOT-FOLDED, and all three run AGAINST the direction that would help T2/T3:**
Ascension's `+38 %`, Fighting Spirit's `+95 %` and Tip the Scales' leech are all OUTGOING-damage
clauses against a player-damage limb that is a character-SHEET reading of undecidable buff
composition (`fixture.py`: *"HALT-4 leaves application order PARTIAL … never closes it with a
coefficient"*). Multiplying a buff onto a total of unknown composition is a coin flip between a fold
and a double-count. Ascension's absorb clause **is** folded.

**Carried unchanged:** C-I2-1 · C-E3 · C-D2/C-D3/R-PM4-6 · C-F1/C-F3/C-F4/C-F5 · C-I3-5 · C-G3 ·
C-G6 · **OBS-H2-9 (ground px → m) — no pixel scale is invented anywhere in this fold** · wave 154's
travel outlier, undiagnosed for a **fifth** lap.

**⚑ LAW 3 — check 11, `moved: {}`, over ELEVEN constants:** I-3's nine plus **`PLAYER_SANE_BOUND_M`**
and **`MOVE_SPEED_FRACTION`**, the two this fold could have been tempted to move (a longer dash, a
faster player). **There is no fitted number anywhere in this lap.** Every folded magnitude is read
**by explicit column** out of a vendored, FULL-hash-pinned CSV; the potion threshold is **parsed**
out of OBS-H2-5's own prose with a guard that refuses a wrong parse; the motion threshold's
numerator is read off a **column name**. Assert-wall check 14 exists to keep it that way.

---

## 10 — SEAM WORK

**star-lord** — ⚑ **three gate catches in one lap, and all three were right.** The F5-E loader
caught D-I4-2; `_spawn_tick` caught D-I4-3 (which I then mis-diagnosed as *theirs* before finding it
was mine); `G-LOCO-ONE-TRAJECTORY` + `R-LOCO-1-HITTEST` caught D-I4-5 and are the reason there are
no I-4 batons. **No schema change is requested and none is needed**: no baton field, no enum member,
no validator predicate, no gate-wall pin. The one item that belongs to them is **D-I4-5's
resolution**, and it is a conductor ruling before it is a schema question.

**drax / scene consumers** — ⚑ **the crowd shape I described at I-3 is SUPERSEDED.** I-3 told
renderers the crowd forms a **queue**; R-PM4-12 retired that response and under the arm of record it
forms a **ring that spreads laterally**. Also: corpses carry **no footprint** (measured, 0/1,592),
and the player **channels while traversing**, including through a 10–16 m dash. Both MIGRATION files
carry the detail.

**rocket** — nothing. **jack-ryan** — Disciplines #1, #2, #3, #11, #12 exercised and named.

---

## 11 — ⚑ SELF-ATTACK SURFACES

1. **The run has stopped being able to fail, and that is a worse instrument than one that misses.**
   Three cells, five diagnostics, two independent limbs, one bracketed undecided term — **all of
   them end at the same wave for the same reason**: the substrate ran out. A matrix whose cells all
   terminate on an external boundary has stopped discriminating, exactly as I said at I-2 about a
   different boundary. **The next iteration cannot measure T1 at all without substrate past wave
   170**, and C-D2 is the named blocker.
2. **I chose the UPPER limb on the one undecided term** (C-I4-4, absorb persistence) with an
   argument I still believe — the lower limb is fictional — and it is the term most directly
   responsible for the overshoot. **I ran the strict lower bracket precisely because I did not want
   that argument to be load-bearing**, and it is not: the bracket lands on the same wave. But if
   anything in this lap deserves a second look, it is that.
3. **MG-4 now misses on the OTHER side.** The sim's moving fraction went 0.931 → 0.842 against a
   target of 0.883. I overshot the correction, and the mechanism is P.1's error: I priced the gate
   and not the predicate underneath it.
4. **The potion fired ONCE in 508 seconds.** A fold justified by "Matt played with potions" ends up
   with a potion that is almost never used — because the layers in front of it are so effective.
   That is either a true property of the build or evidence that the on-hit layers are over-priced,
   and **this lap cannot tell those apart.**
5. **D-I4-5 means the reference cell of record has no baton.** Every number in this note is
   verifiable from the committed findings + knots artifacts, but the conductor's CL-10 has, for the
   first time in this run, no baton to read the reference cell off.
6. **I mis-diagnosed D-I4-3 as another seam's defect before finding it was mine**, and I had a
   routing memo drafted. It is in the git history.

---

## 12 — WHAT I WOULD PUT TO THE CONDUCTOR

**Two rulings, in this order.**

1. **D-I4-5 — the tick order.** `step → separate → resolve` is the model-correct order and it is
   the only thing that makes the ruled contact response emit a baton. It re-prices every number,
   so it is an iteration and a ruling, not a patch. **Nothing else in the run can be emitted as a
   baton until it is decided.**
2. **The substrate boundary.** With every measurable limb folded, **T1 is no longer measurable
   inside waves 151–170**. Either the eHP band extends past 170 (C-D2's G(171) = 420 discontinuity
   is the named blocker and it is a legolas decode, not a model choice), or **the run HALTs
   exhausted with this residual as the finding** — which is precisely the charter's own second
   HALT condition, and I think it is the honest one.

**The residual, stated as plainly as I can.** Four iterations of measured-decode substrate
completion gave the roster its life, the summons their life, every body its space, and the player
his hands. **The sim now reproduces the reference fight's contact law, its corpse behaviour, its
channel-while-moving, its stationarity cap and its dash cadence — and it does not reproduce its
death.** The player Matt actually played, given the kit Matt actually had, does not die on wave 160
in this model. That is either the model's remaining error or the measurement's, and **the run has no
instrument left that can tell those apart.**

**No constant was tuned. Nothing was aimed at a band. I predicted a death wave of 165 and the
model returned no death at all.**
