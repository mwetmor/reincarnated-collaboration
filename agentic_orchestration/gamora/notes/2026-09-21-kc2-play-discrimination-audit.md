# KC2-PLAY · THE DISCRIMINATION AUDIT OF THE REFERENT VALIDATION SET

> **STATUS:** CURRENT — Run KC2-PLAY, commissioned by conductor gandalf 2026-09-21 following C-1
> (`legolas/findings/2026-09-21-c1-off-channel-energy-recovery.md` § 6).
> **Author:** gamora (simulation + spirit-guide seam). **ANALYSIS ONLY.**
> **Read-only held throughout.** No code, no constant, no pack row, no prereg row, no oracle value
> was changed. No sealed cell was opened or re-run (K-7 held). No push. No sub-agents.
>
> **Sources read** (all read-only): prereg v1.5 in full · C-1 in full · galadriel's T-B
> expected-values note in full · `simulation/kc2/micro_oracles.py` · `…/energy.py` ·
> `…/fixture.py` · `…/calibration.py` · `…/channel.py` (the `ticks_per_s` route) ·
> `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` §§ 3.2–3.4 · `legolas/notes/2026-08-07-pe1-eor-spin-parameters.md` § 4.4.
>
> ⚑ **Law 3 held.** Every alternative behaviour named below is either (a) already measured somewhere
> in the corpus, or (b) the immediate neighbour of a failure the run has already had. **I named no
> alternative I could not point at.** Where I could not settle a row I say so and say why.

---

## § 0 · THE COUNT, AND THE ONE NUMBER THAT MATTERS

**86 rows audited.**

| verdict | n |
|---|---:|
| **DISCRIMINATING** | **20** |
| **NON-DISCRIMINATING** | **45** |
| **MIS-READ** | **10** |
| **COULD NOT SETTLE** | **4** |
| ⚑ **NO INSTRUMENT** *(declared extension — see § 0.2)* | **7** |

⚑ **45 NON-DISCRIMINATING is not the number that matters, and quoting it alone would be the same
defect this audit is about.** The set partitions:

| | n | meaning |
|---|---:|---|
| **NON-DISCRIMINATING · DECLARED** | **22** | the corpus already says the row cannot discriminate, on the row's own face. **These are correctly handled rows.** MO-5's one-sidedness, the prereg's CLASS V, its four named structural zeros, galadriel's *"ship ratios"*, `TB-CA-01`'s declared floor |
| ⚑ **NON-DISCRIMINATING · UNDECLARED** | ⚑ **23** | the row is read as confirming a property it cannot reach, and nothing on its face says so |

**23 + 10 MIS-READ = 33 rows carry weight they cannot bear.** That is the audit's result.

### 0.1 · THE HEADLINE, IN ONE LINE OF ARITHMETIC

The oracle's own depth equation is `depth(t) = charge_per_tick + |net|·t = 14.4 + |net|·t`
(`micro_oracles.observe_s2_transit`). Run it twice — once at the oracle's pinned net, once at the
footage's measured net:

| | net /s | **t at depth 86** | **t at depth 117** | the band's information content |
|---|---:|---:|---:|---|
| **oracle**, `leech_uptime = 1.0` | **−1.03** | **69.5 s** | **99.6 s** | a slow monotone transit |
| **footage**, galadriel `MD-B4app-2` § 4.4 | **−73.4 … −81.7** | **0.88 … 0.98 s** | **1.26 … 1.40 s** | ⚑ **one tooth of a sawtooth** |

> ⚑ **THE SAME BAND, ON THE SAME EQUATION, IS ONE SECOND OF CHANNELLING OR A HUNDRED.** A band over
> depth cannot separate a 1-second tooth from a 100-second transit, because the separation lives
> entirely in `|net|`, and `|net|` is the quantity `depth` was divided by to reach the band.
> **The band is a TIME measurement stated as a DEPTH, and the conversion factor is the thing being
> validated.**

C-1 said *"a depth measurement cannot pin a rate."* The arithmetic says the stronger thing: **the
band's own construction consumed the rate**, and 1.26–1.40 s is the footage's measured ~1.5 s
excursion timescale reproduced by the oracle's equation the moment the pinned `leech_uptime = 1.0`
is replaced by the footage's own number.

### 0.2 · WHY I ADDED A FIFTH VERDICT, AND WHY I AM NOT HIDING THAT I DID

Seven rows have **no oracle side and no port side to compare** — `TA-B-10` / `-11` / `-12`, and four
`MEASURED` fixture constants with **zero consumers anywhere in the tree**. Grading those
NON-DISCRIMINATING would credit the corpus with a check it does not have. **A row that cannot be
evaluated is not a weak instrument; it is no instrument**, and conflating the two is the same class
of error as conflating *"this check is weak"* with *"this value is wrong"* — which the commission
expressly forbade. **NO INSTRUMENT is a declared extension of the taxonomy, not a silent one.**

### 0.3 · THE CLASS, STATED — because the commission asked for the third instance and there are more

The commission named two instances (the energy band; the T-A band half). **The audit found the class
has five distinguishable shapes, and each destroys a different thing:**

| shape | what it destroys | instances found |
|---|---|---|
| ⚑ **A BAND / POINT READING OVER A LEVEL** | **time-structure and rate** | the energy band · `TB-HP-01…08` occupancy rows · the four `1594` stills read as a ceiling |
| **A ONE-SIDED BOUND** | **the entire admissible half** | `MO-5` · `TA-X-10` · `TA-X-17` · `TB-CA-01` · `TB-HP-14`'s per-body heal |
| ⚑ **A STRUCTURAL ZERO** | **the difference between "ran and produced zero" and "absent"** | `TA-X-11 / 12 / 19 / 15(b)` **(named by the prereg)** + ⚑ **`TA-X-13` · `TA-X-14` · `TA-X-22` · `TA-X-24` (NOT named — § 4.4)** |
| **A CONSERVED SUM / PARTITION IDENTITY** | **the allocation among the terms** | `TA-X-07` · `TA-X-08` |
| ⚑ **A RELATION WITHOUT A MAGNITUDE** | **everything but one bit** | `TA-X-03 / 04 / 05` · `TA-X-26`'s five clauses against a permuted join |

---

## § 1 · METHOD

For each row, three questions in order:

1. **What does this statistic throw away?** (band → time-structure · mean → distribution · total →
   rate and ordering · extreme → the body of the distribution · digest → nothing between the two
   objects and everything about whether either is right · zero → presence-vs-absence.)
2. **Does the property being claimed live in the part thrown away?**
3. **Name a materially different behaviour that satisfies the check.** If I can name one from the
   corpus or from the immediate neighbourhood of a failure the run has already had, the row is
   NON-DISCRIMINATING. If I genuinely cannot after trying, it is DISCRIMINATING and I say what makes
   it so.

⚑ **One framing that governs all of GROUP C and D and that I want on the record before the table:**
**the T-A rows do not validate the oracle against the referent. They validate the PORT against the
ORACLE.** Their discrimination question is therefore *"can this separate a faithful port from an
unfaithful one"*, and **every green T-A row is silently conditional on the oracle being right.** The
prereg puts that sentence on the report face **once**, for one row (§ F.5 cl. 7, the unkillable-player
sentence). ⚑ **It is true of all 26.**

---

## § 2 · GROUP A — THE ENERGY / MICRO-ORACLE SET (the oracle validated against the referent)

**12 rows. 4 DISCRIMINATING · 4 NON-DISCRIMINATING · 4 MIS-READ.**

| # | row | statistic's shape | what it throws away | verdict | the alternative that satisfies it |
|---|---|---|---|---|---|
| **A1** | ⚑ **`MO_DRAWDOWN_BAND = (86, 117)`** | **two point readings** — `1594−1508` (w158) and `1594−1477` (w~156). **n = 2 stills.** | **rate · frequency · dwell · refill mechanism · the entire trajectory between the two samples** | ⚑ **MIS-READ** | **the footage itself** — 64.6 % of combat pinned at the ceiling, ~1.5 s sawtooth, 19 discrete refills. **And the oracle** — a monotone −1.03 /s transit. Neither shares a single dynamical property with the other |
| **A2** | ⚑ **MO-3 scalar limb — `ceiling − band_max = 1477`** | **an algebraic identity in three readings, two of which are the same reading** | **everything** | ⚑ **MIS-READ** | ⚑ **any sustain model whatsoever.** § 2.1 |
| **A3** | **MO-3 transit limb — the trajectory crosses 1477 at t ≈ 99.6 s** | an **internal** cross-check of the integrator against the closed form | **whether 99.6 s is right about the referent** | ⚑ **MIS-READ** | ⚑ **the referent fails this check.** § 2.2 |
| **A4** | **MO-1 usable ceiling `1594 = 2576 − 982`** | exact-integer, two independently-sourced terms | nothing arithmetic; it pins a **level**, never a dynamic | **DISCRIMINATING** | — (a wrong reservation, a wrong aura set, or a decremented-rather-than-recomputed ledger all move it off an integer) |
| **A5** | **MO-2 reservation `982`, 7 DB rows, never reading the pin** | exact-integer sum | — | ⚑ **DISCRIMINATING — SINCE 2026-09-21, NOT SINCE PIN TIME.** § 2.3 | at pin time: **any of the 81 `(O, S)` offset cells** that lands 982 |
| **A6** | **MO-4 player HP max `20005`, "consumed UNMODIFIED"** | a single-value read back from **wave 1, 40 ticks** | **waves 2–10** | **NON-DISCRIMINATING** ⚑ *undeclared* | a model that applies a T-7 envelope from wave 2 onward. The check's window is smaller than the claim's scope; widening it to the whole run costs nothing |
| **A7** | **MO-4's `hp_max_basis == "POST-SCALING"` limb** | a **string equality against a declared constant** | **the model's actual basis** | **NON-DISCRIMINATING** ⚑ *undeclared* | a PRE-scaling model whose declared constant says POST. ⚑ **This is `TA-X-26` / trap 8 on the oracle side — *the header is where the claim is made* — and nobody has instrumented it here** |
| **A8** | **MO-5 cycle floor `7.0 s`, `observed ≥ target`** | **one-sided; no upper limb** | **the entire overshoot half** | **NON-DISCRIMINATING** *(declared)* | **any `v_ref < 4.0`.** `v_ref` is a DECLARED-FREE-PARAMETER sitting in the numerator of the dominant term — ⚑ **the check gets greener the slower the pilot is.** The module knows and says so |
| **A9** | ⚑ **the drain decomposition `16.0 × 12.25 × 0.90 = 176.4` vs the client-printed 176.4** | a **four-way closure**, three terms independently sourced (DBR rank-26 cost · sheet attack speed · Seal of Annihilation −10 %, now `DB-CITED + SAVE-CONFIRMED` per C-1 § 7) landing on a fourth the game printed | — | **DISCRIMINATING** | — none. ⚑ **With one live disagreement carried, not closed: galadriel's pixel-measured gross drain is ≈ 190 /s against this 176.4, a 7.7 % gap graded NOT DERIVED** |
| **A10** | ⚑ **the `−1.03 /s` boot gate, ±0.005** (`kc2rt_fight.gd:409`) | a **port↔oracle identity on a derived constant**, at 0.5 % of its own magnitude | **whether −1.03 is right** | ⚑ **MIS-READ** | ⚑ **the tightest gate in the energy stack, pinned to a number the footage refutes by ~70–80 /s.** Flagged separately at § 7 as an *actually-wrong* row |
| **A11** | **`ENERGY_MAX = 2576`, and the inference "1594 recurs at 4 timestamps ⇒ it is a CEILING"** | **four point samples at unknown phase** | **the residence-time distribution** | **NON-DISCRIMINATING** ⚑ *undeclared* | ⚑ **a MODAL level rather than a hard ceiling.** At the footage's measured **64.6 % ceiling residency**, four of four samples landing at 1594 has probability **0.646⁴ = 0.174** — not rare. **The inference was unsupported at the time and is CORRECT ANYWAY**, because MO-2's DB derivation independently produced the 982 |
| **A12** | ⚑ **the T-1 s1 clear-time gate** — 92 measured waves, per-wave ± 1.0 s, two-class rollup, sign argument | **per-wave, two-sided, distributional, with the pooled form made to RAISE** | very little | ⚑ **DISCRIMINATING — THE BEST INSTRUMENT IN THE CORPUS.** § 2.4 | — |

### 2.1 · A2 — `MO-3`'s scalar limb is `MO-1` wearing a second badge

`micro_oracles.observe_s2_in_combat_energy` computes `usable_ceiling() − band_max` and its docstring
says:

> *"The band is its own MEASURED row — it is **NOT derived from 1477 anywhere** — so this is a
> consistency check between instruments rather than an algebraic tautology."*

⚑ **That sentence is false, and the corpus shows it in two places.** `P-E1` § 4.4's globe table lists
the readings `1594 ×4`, `1508`, **`1477`**, and concludes *"sustained channelling draws the bar down
only **86–117** below that ceiling."* The battle spec § 3.2 writes the same arithmetic under
`usable_ceiling ≈ 1594`. **`band_max = 1594 − 1477` by construction.** So

```
observe_s2_in_combat_energy()  =  ceiling − band_max  =  ceiling − (1594 − 1477)
```

which equals 1477 **iff `ceiling == 1594`** — i.e. **iff MO-1 passes.** The limb has no content beyond
MO-1. ⚑ **A model with zero drain, zero regen and zero leech passes it.**

⚑ **And the guard that was supposed to catch exactly this could not see it.** The module's own rule 2
— *"a derivation may not read its own target"* — is enforced by **scanning `energy.py`'s source for
the string `MO_ENERGY_RESERVATION`.** `MO-3` reads its own target through a *second constant computed
from it*. **The guard is source-scan-shaped; the defect is arithmetic-shaped.** The module's opening
paragraph names the hazard precisely — *"a pin the model CONSUMES and the test RE-READS is a
tautology — it passes on any model, including a wrong one"* — and then ships an instance of it one
oracle later.

### 2.2 · A3 — the transit limb is a check the referent would fail

The limb asserts the trajectory reaches ≤ 1477 within 200 s and that the crossing time matches
`t* = (117 − 14.4)/1.03 = 99.61 s`. Both sides of that comparison are the model's own. It is an
honest integrator-vs-algebra cross-check and the docstring says so.

⚑ **It is being read as the dynamic half of MO-3 — the part that goes beyond the scalar identity.**
It cannot be, for a reason sharper than "it is internal": **`EnergyModel.run_channel` integrates an
UNINTERRUPTED channel and has no release mechanism at all.** The referent channels at **83.75 %
uptime with 19 interruptions**, and each interruption is what refills the globe. So the transit limb
is evaluated on a trajectory the referent **never occupies**, and a hypothetical recorder replaying
the referent's own energy trace would **fail** it — no monotone crossing exists.

> ⚑ **`TA-B-13`'s retired form is the same shape one seam over:** *"a band that rejects the oracle
> cannot grade a port."* Here: **a check the referent fails cannot corroborate a model of the
> referent.**

### 2.3 · A5 — MO-2 became discriminating three months after it was pinned

Spec § 3.2's derivation of 982 is *"the unique solve (mastery-wide offsets **O = +1, S = +4, one cell
of 81**; cross-validated by EoR total = 26)."* ⚑ **Two free parameters, an 81-cell search, and the
accepted cell is the one that lands on the target.** At pin time the constraints were: total = 982
(the target) and EoR = 26. **Two parameters, two constraints, zero residual degrees of freedom —
zero falsifiability.** Any cell reaching 982 was admissible; the instrument could not separate a
correct rank model from a fitted one.

⚑ **C-1 § 7.1 is what made it discriminating, and it did so on 2026-09-21.** Rebuilding the rank
model from the save alone (`allocated + all-skills 1 + mastery bonus + per-skill bonus`) reproduced
**11 of 11 pack rows** — `220 / 100 / 107` at ranks 18/10/11 and `205 / 50` at 14/12 among them.
**Nine additional independent constraints, all satisfied.** The fit is retroactively a derivation.

**This belongs in the audit and not in a footnote:** MO-2 is one of only four DISCRIMINATING rows in
the energy group, and its discrimination is **three months younger than its `MEASURED` badge.**

### 2.4 · A12 — the corpus already built the instrument this audit is asking for

`calibration.py` T-1, pinned at G-B close:

* **92 per-wave comparisons**, two-sided, tick-quantised — not an aggregate.
* ⚑ **`t1_pooled_mean` RAISES** with the message *"Use `t1_two_class_rollup()`; the classes are
  declared before the numbers are seen."* **§ 12 T-1 forbids a pooled mean over the bimodal mix.**
* `MEASURED_S1_AGGREGATE` is *"reported only — **never a comparison target** (that is the pooled mean
  T-1 bans)."*
* `t1_verdict` ships **three Pearson correlations** and a **mechanism** diagnosis: *"the sim's clear
  time is a function of BODY COUNT; the fixture's is not. The residual is a mechanism, not a
  magnitude."*
* ⚑ **`t1_sign_argument` — the strongest single instrument in the corpus.** It uses the **known SIGN**
  of an absent term (`engagement_kill_time ≥ 0`) to split the waves into those falsified *independently
  of the missing measurement* and those the absence could still explain. **It discriminates DESPITE a
  missing term.**

> ⚑ **THE ASYMMETRY IS THE STRUCTURAL FINDING OF THIS AUDIT.** The discipline the commission is
> asking me to invent **was built in this repo in August, for clear times, and is enforced by code
> that raises.** It was not applied to the energy band, not to the T-A bands, and not to the T-B
> occupancy rows. **The house rule exists. Its application is not uniform.**

---

## § 3 · GROUP B — THE T-B EXPECTED-VALUE TABLE (footage-derived; the twin is checked against these)

**22 rows. 8 DISCRIMINATING · 14 NON-DISCRIMINATING (7 declared, 7 undeclared).**

⚑ **A pattern worth naming before the rows:** several of these are **non-discriminating alone and
discriminating in company**, and galadriel's note usually ships the company. Where it does, I say so;
where it does not, the row is exposed.

| # | row | shape | throws away | verdict | alternative |
|---|---|---|---|---|---|
| **B1** | `TB-HP-01` full-health occupancy **0.428414** | occupancy fraction | ⚑ **all time-structure** | **NON-DISC** *undeclared* | a twin at full for the first 77.5 s then never again. **Rescued in company** by § 1.3.5's per-wave table and § 1.3.3's teeth |
| **B2** | `TB-HP-02 / -03` below 90 % / 75 % | same | same | **NON-DISC** *undeclared* | same |
| **B3** | `TB-HP-04 / -05` below 50 % / 33 % | same (denominator-insensitive — a real strength) | same | **NON-DISC** *undeclared* | ⚑ **galadriel names it herself**: *"A twin that spreads its danger evenly across ten waves has the right aggregate and the wrong story."* **The row is right; the reading is what fails** |
| **B4** | ⚑ `TB-HP-06` **below 25 % = 0 frames** | a **one-sided bound** | the whole admissible half | **NON-DISC** *undeclared* | ⚑ **THE PORT ALREADY SATISFIES IT AND IS THE RUN'S LARGEST KNOWN DIVERGENCE** — `terminal_reason = cleared` 25/25, HP never below **79.44 %** (ceiling `C-e`). **An unkillable twin passes.** Two-sided partner exists (`TB-HP-08`'s floor at 26.79 %) and is not bound to it |
| **B5** | `TB-HP-07` frames decreasing **0.137293** | an interval rate | **magnitude and clustering** | **NON-DISC** *undeclared* | one huge hit/s vs many tiny hits/s at matched cadence. Rescued in company by B-19's depth distribution |
| **B6** | `TB-HP-08` HP minimum **5,360** | ⚑ **an extreme over n draws** | **the body of the distribution**; scales with n | **NON-DISC** *undeclared* | any distribution whose worst single frame lands at 26.79 %. ⚑ **Same class as the retired `TA-B-13`** — and it is not labelled that way here |
| **B7** | `TB-HP-09` `health_max` drop episode | a declared **model gap** | — | **DISCRIMINATING** | — ⚑ **and correctly EXCLUDED from grading.** *"The grader must not score that difference."* A clean row |
| **B8** | ⚑ **B-19 saw-tooth — six order statistics × five prominence gates** | a **distribution with a declared sensitivity sweep** | very little | ⚑ **DISCRIMINATING** | — none nameable at the same gate. ⚑ **This is what the energy band should have been.** § 3.1 |
| **B9** | ⚑ B-19's **gate-invariant recovery slope** (3,098–4,323 HP/s across a 20× gate range) | an invariant **identified by sweeping the free parameter** | — | ⚑ **DISCRIMINATING** | — **the free parameter was swept until one statistic stopped moving. That is the method** |
| **B10** | § 1.3.4 **deep-excursion localisation** — all 8 sub-half runs in w159/160 | a **localisation**, not an aggregate | — | **DISCRIMINATING** | — it is precisely the statistic that falsifies B3's alternative |
| **B11** | § 1.3.5 **per-wave HP shape** (10 waves × 9 columns) | per-wave, unpooled | — | **DISCRIMINATING** | — and it surfaces w158 as *"a hole in the fight"*, which no aggregate could |
| **B12** | `TB-CH-01` channel uptime **0.8375** | duty fraction, **with a free tick gate** | time-structure; ⚑ **and the gate spans 0.7530 – 0.8953, a 0.142 range** | **NON-DISC** *(declared — the sensitivity is printed)* | a twin channelling in one 153 s block. ⚑ **And note: the oracle's own `0.879189` sits INSIDE the footage's gate-induced range — the comparison can be made to pass or fail by choosing the gate** |
| **B13** | `TB-CH-02` `P(chan\|moving)/P(chan\|stationary)` ratio **1.2093** | a ratio, **deliberately**, to cancel the classifier | the absolute levels (intended) | **NON-DISC** *(declared)* | ⚑ **the ratio REDUCES the confound, it does not remove it** — raising the motion threshold moves the *slow* frames across the partition, biasing the two conditionals unequally. Magnitude unmeasured; `frac_moving` spans **1.79×** across committed instruments |
| **B14** | `TB-RL-01` release duty **0.10484** | a duty fraction with a **free floor** | time-structure; ⚑ **floor choice spans 0.0609–0.1835, 3.0×** | **NON-DISC** *(declared)* | **the parameter spread dwarfs any plausible fidelity signal.** It is a choice with a number attached |
| **B15** | `TB-RL-02 / -03` — the **Type-A vs Type-B within-subject contrast** | a **contrast**, with IQRs and a Fisher p | — | **DISCRIMINATING** | — ⚑ **and galadriel identifies the load-bearing half correctly**: *"What carries KP-1 is the WITHIN-SUBJECT CONTRAST, not the tightness."* *(The medians alone, at n = 11 and n = 8, are not.)* |
| **B16** | `TB-CA-01` cast rate **0.2957 /s** | ⚑ **a declared FLOOR** | the whole upper half | **NON-DISC** *(declared)* | any twin casting ≥ 0.2957 /s, including one casting 3 /s |
| **B17** | `TB-CA-02` aggregate interrupt rate **0.148** | ⚑ **a mean over opposite-signed subpopulations** | the sign structure | **NON-DISC** *(declared)* | ⚑ **galadriel's own words**: *"The aggregate 0.15 is a CANCELLATION, not a rate"* — slots 2/L in longer-than-random silences, slot 3 in shorter, **pooled p = 0.286.** The per-slot rows carry the signal. *(Separate class: the SKILL NAMES are a promotion with no instrument — a labelling defect, correctly routed to `DECLARED-not-decoded`.)* |
| **B18** | `TB-MV-01` movement — **ratios only** | a ratio, because the absolute is unrecoverable | — | **NON-DISC** *(declared, exemplarily)* | ⚑ **committed spread 0.494–0.883 = 1.79×, and *"The disagreement is a THRESHOLD CHOICE, not a property of the fight."*** The declaration to beat: *"An absolute movement figure in a green report is a defect in the report"* |
| **B19** | `TB-WV-01` per-wave durations, **two instruments** | agreement of **two independent instruments** to ≤ 0.19 s on w152–159 | — | **DISCRIMINATING** | — ⚑ and the w151/w160 disagreement (0.68 / 0.88 s) is **explained mechanically** (182.65 vs 181.0 s windows) rather than absorbed |
| **B20** | `TB-WV-02` terminal wave **160**, n = 1 | one draw | everything | **NON-DISC** *(declared at both ends)* | ⚑ `TA-B-01`'s band *"admits every arm in the seal, including the G5 control the run built to be different"* |
| **B21** | `TB-HP-13` regeneration **124.67** measured vs **129.38** decoded, residual −3.64 % | **two routes, one measured one decoded, agreeing** | — | **DISCRIMINATING** | — ⚑ **with a live hazard carried in prose, not in code**: *"The naive whole-trace drip reads 178.40 HP/s and is CONTAMINATED."* **The discrimination lives entirely in the subset rule (sub-33 %, uncontaminated); a grader who does not read the prose gets a 43 % overestimate** |
| **B22** | `TB-HP-14` leech cadence **11.408 /s** in decoded `[11.387, 12.250]`; per-body heal an **UPPER bound** | a bracket-membership + a one-sided bound | the upper half of the heal | **NON-DISC** *undeclared for the cadence* | ⚑ **the cadence lands 0.021 above the bracket's LOW edge on a 0.863-wide bracket — a 2.4 % margin.** Inside-a-bracket is corroboration; **at the edge it is one small bias from being outside**, and nothing on the row's face says so |

### 3.1 · B8 — the metrological asymmetry, stated plainly

Two HUD orbs, one fight, one session:

| | HP globe | ⚑ **energy globe** |
|---|---|---|
| instrument | **10,861-row 60 fps OCR CSV**, sha-pinned, grid-integrity verified, 100 % accept | ⚑ **five eye-read stills** |
| statistic | tooth rule written verbatim · **6 order statistics** · **5-gate sweep** · gate-invariant identified | ⚑ **a two-point band** |
| what a twin is checked against | period, depth, fall, recovery, slopes, per-wave localisation | ⚑ **depth, once** |

**The cause is legitimate** — the energy OCR clears its accept gate on only **0.8577** of the window
and the source MP4 is gone (`matt_to_do` **T30**). **The consequence stands anyway:** the oracle's
entire sustain model is validated by an instrument two orders of magnitude weaker than the one beside
it, and **nothing on the band's face said so.**

⚑ **AND THE PART THAT IS NOT A COMMISSION.** A 20 Hz energy series **exists and is committed** —
`D-GOODCOV` covers **85.77 %** of combat; `galadriel/captures/2026-08-25-md-b4app-2b-energy/work/s2-releases.json`
carries **19 releases with per-release `dE/dt`**; `MD-B4app-2` § 4.4 carries the **below-cap
channelling net**. C-1 extracted the ceiling residency (64.6 %), the excursion timescale (~1.5 s) and
six unclipped positive `dE/dt` values **from artifacts committed on 2026-08-25**. ⚑ **The band was
minted in August from five stills and was never re-derived against the time series that landed
beside it.** The discriminating instrument is not missing. **It is on disk and older than the grade.**

---

## § 4 · GROUP C — THE T-A PREREG EXACT ROWS

**27 clause-rows over 26 row-ids** (`TA-X-15` split into (a)/(b) per the prereg's own construction).
**6 DISCRIMINATING · 16 NON-DISCRIMINATING (5 declared, 11 undeclared) · 4 MIS-READ · 1 COULD NOT SETTLE.**

| id | shape | throws away | verdict | alternative that satisfies it |
|---|---|---|---|---|
| `TA-X-01` | byte-exact repeat | — | **DISC** | — the claim (determinism) is narrow and the row matches it. ⚑ v1.5's *"names an arm/salt that MUST DIFFER from `P-2`'s"* is the audit's question answered at authoring time |
| `TA-X-02` | **coverage 89/89, zero unmapped** | ⚑ **TRUTH** | ⚑ **MIS-READ** | ⚑ **census `M4` was mapped `IMPLEMENTED` with a note describing an implementation that did not exist.** The prereg caught it and added cl. 1a. **Discriminating for completeness of the mapping; read — as a precondition and cap condition `C3` — as coverage** |
| `TA-X-03` | inertness A, byte-exact | ⚑ **the possibility that BOTH arms are identically broken** | **NON-DISC** *undeclared* | **a port that never implements the fold at all** produces identical digests on both arms and passes perfectly. *(Partner `TA-X-05` closes it — see below)* |
| `TA-X-04` | inertness B, byte-exact | same | **NON-DISC** *undeclared* | ⚑ **§ 4.1 — `TA-X-04`'s partner is `TA-X-06`, and OQ-1 proposes retiring `TA-X-06`.** Read § 4.1 before ruling OQ-1 |
| `TA-X-05` | distinctness C — **`≢`, one-sided** | ⚑ **magnitude and direction entirely — it is ONE BIT** | **NON-DISC** *undeclared* | **a port whose fold is wrong in every particular** still differs from `M0`. It proves the fold EXISTS, never that it is right |
| `TA-X-06` | distinctness D | — | ⚑ **MIS-READ** *(prereg-declared, § F.2e)* | ⚑ **unfalsifiable in the honest direction** — the only route to green is inventing a veto rule nobody wrote. Classed EXACT while its only mechanism was classed report-only **seven lines away in the same file.** I confirm the prereg's finding and add § 4.1 |
| `TA-X-07` | **conservation, 7 terms** | ⚑ **THE ALLOCATION AMONG THE TERMS** | **NON-DISC** *undeclared* | ⚑ **a port that drops 30 % of damage and books it as `voided` satisfies conservation exactly.** The identity is blind to what a damage model is *for* — and `C-e` shows the consequence is live: **the port is unkillable and `TA-X-07` was graded on a green identity.** ⚑ **Second, sharper:** the runtime's own assert-wall checks **SIX** of the seven (omits `counterplay_absorbed`) — **a term omitted from a conservation check is a free variable** |
| `TA-X-08` | denominator partition identity | ⚑ **the partition's CONTENT** | **NON-DISC** *undeclared* | **a port that classifies every tick `IDLE`** satisfies both sub-identities. *(Its own claim — the denominator law — it does pin, and it resolved the 0.215-vs-0.217 tell)* |
| `TA-X-09` | **9 `math_rules` test vectors** | **coverage of the rule space** | ⚑ **COULD NOT SETTLE** | nine points pin a closed form and do not pin a piecewise rule. ⚑ **The row's power is the vectors' BRANCH COVERAGE of `math_rules.json`, which no document states and which I would have to open the pack to determine.** § 6 |
| `TA-X-10` | containment supremum **≤** | the whole admissible half | **NON-DISC** *undeclared* | **a port whose bodies barely move** passes. ⚑ **The two-sided partner was `TA-B-13`, retired because *"its own t-band rejects the oracle's observed maximum."*** The supremum now stands alone |
| `TA-X-11` | wall-clamp **zeros** | presence-vs-absence | **NON-DISC** *(declared)* | *"a port with no wall at all also scores zero"* — the prereg's own words |
| `TA-X-12` | pool damage **== 0.0** | presence-vs-absence | **NON-DISC** *(declared)* | *"the aprons are ABSENT, not present-at-zero"* |
| `TA-X-13` | ⚑ **no player crit — `== 0`** | presence-vs-absence | **NON-DISC** ⚑ *undeclared* | ⚑ **a port with NO crit implementation scores zero identically to a correct crit limb at `LO`.** **FIFTH structural zero; the prereg enumerated four** |
| `TA-X-14` | ⚑ **the two DO-NOTs — both `== 0`** | presence-vs-absence | **NON-DISC** ⚑ *undeclared* | ⚑ **a port with NO release mechanism satisfies both clauses.** **SIXTH structural zero — and ACTIVELY vacuous right now**, because the port's Type-A limb is entirely absent (prereg § F.3b) |
| `TA-X-15(a)` | release schedule — p05 at **tick 49**, measured | — | **DISC** | — an exact integer tick against a declared schedule |
| `TA-X-15(b)` | no intra-point stagger | presence-vs-absence | **NON-DISC** *(declared)* | *"unrepresentable rather than absent"* — the fourth structural zero, and the first caught before a grader had to name it |
| `TA-X-16` | **p06 OFF — value AND enforcement**, `n_pool_picks == 47` + a **filtered-key COUNTER** | — | ⚑ **DISC (at v1.5; NON-DISC at v1.4)** | ⚑ **the prereg's own sentence IS this audit's question**: *"a filter with no counter is indistinguishable from a filter that never fired."* Two independent routes agree on 54/47 |
| `TA-X-17` | spawn offset **≤ 8.0 m**, every body | the whole admissible half | **NON-DISC** *undeclared* | ⚑ **a port that spawns every body AT the anchor (`ρ = 0`) passes on every instance.** *(Partner `TA-X-18` closes it — and it is present)* |
| `TA-X-18` | ⚑ **scatter-law three-law discriminator** — feed `u₁ = u₂ = 0.5`, assert `(−4.0, 0.0)` against `(−5.656854, 0)` and `(0.0, 0.0)` | — | ⚑ **DISCRIMINATING — THE TEMPLATE** | — none. ⚑ **The alternatives were NAMED FIRST and the input was CHOSEN at the point where they separate. This is what the commission's question looks like when it is answered at authoring time instead of at audit time** |
| `TA-X-19` | arrival unconditionality | presence-vs-absence | **NON-DISC** *(declared)* | *"no arrival limb at all"* — satisfied vacuously; OQ-8 routes it |
| `TA-X-20` | hit-test at **2.99 m hit / 3.01 m miss** + two negatives | — | **DISCRIMINATING** | — a boundary probe at ± 0.01 m. Same family as `TA-X-18` |
| `TA-X-21` | quantisation per site + **zero bare `round(`** | unregistered sites; ⚑ **unexercised branches** | **NON-DISC in part** *(declared)* | ⚑ **its `CEIL` assertion is *"asserted in a vector table and never exercised"*** because no arrival limb exists |
| `TA-X-22` | ⚑ **flag-off release cause `== 0`** | presence-vs-absence | **NON-DISC** ⚑ *undeclared* | ⚑ **a port with no interrupts limb scores zero.** **SEVENTH structural zero** |
| `TA-X-24` | ⚑ **phase model `ENGAGE` — `sha256(actor_id) mod n` NEVER EVALUATED** | presence-vs-absence | **NON-DISC** ⚑ *undeclared* | ⚑ **as stated the assertion is a NEGATIVE, and a port with NO phase model also never evaluates the hash.** **EIGHTH structural zero — carried with the caveat that the row may hold an unstated positive limb; if it does not, a positive (the realised phase vector) closes it** |
| `TA-X-25` | NO-DATA path, 3 clauses | ⚑ **composition** | **MIS-READ** *(self-declared at `C-a`)* | ⚑ *"proves MEMBERSHIP, never COMPOSITION"*; *"the run traded a per-salt discriminator for a per-arm one-bit presence test… the report must not print it as though the discriminator survived"* |
| `TA-X-26` | ⚑ **declared-JOIN conformance, 5 clauses** | ⚑ **THE JOIN KEY** | ⚑ **MIS-READ** | ⚑ **§ 4.2 — a PERMUTED join passes all five clauses** |
| `TA-X-27` | degenerate-draw consumption, 4 clauses | *(its own limit is printed: says nothing about WHICH monsters)* | ⚑ **DISCRIMINATING — second-best-constructed row in the set** | — ⚑ **clause (b) asserts PER-SEED consumption counts and says *"never the mean"*, because the distribution is geometric. That refusal is the discrimination** |

### 4.1 · ⚑ A CONSEQUENCE OF OQ-1 NOBODY HAS PRICED — `TA-X-04` IS ABOUT TO BE ORPHANED

The inertness/distinctness family works **only in pairs.** An inertness row (`≡`) is satisfied by a
port that implements nothing; its distinctness partner (`≢`) is what proves something was
implemented.

| pair | inertness | distinctness | state |
|---|---|---|---|
| `M-POL-2` / `M0` | `TA-X-03` | **`TA-X-05`** | ✅ intact |
| **`W1` / `M-POL-2`** | **`TA-X-04`** | ⚑ **`TA-X-06`** | ⚑ **the distinctness half is the row OQ-1 asks Matt to retire** |

⚑ **If `TA-X-06` is reclassed `UNGRADEABLE-DECLARED` — which is OQ-1's lean, and which I think is
right on its own merits — then `TA-X-04` has no partner, and a port with NO ARENA FOLD AT ALL passes
every remaining `W1` EXACT row.** The prereg's § F.2e cl. 8 says *"striking `TA-X-06` does not make
anything PASS"*, which is true of the **verdict**; it is not true of the **coverage**. ⚑ **Not a
reason to keep `TA-X-06`. A reason to know what its removal costs before removing it** — and the
replacement is cheap: `TA-X-04` gains a positive limb (any observable the arena fold changes), or the
W1 arm's distinctness moves onto the `n_avoidance_vetoes` counter that `TA-B-14` already reports.

### 4.2 · ⚑ `TA-X-26` — five clauses, and not one of them checks the join KEY

| clause | what it pins |
|---|---|
| (a) | that every declared join is **consumed or declared-unconsumed** |
| (b) | that the CSV is **loaded**, sha-verified, with **≥ 1 named call site** |
| (c) | the **parse's SHAPE** — 7,900 rows · 790 records · 8 resist tiers · 5 multiplier values · wave-invariance |
| (d) | that the law is **READ, not recomputed** |
| (e) | the **MEAN** over the armed set — `0.266406 ± 5e-7` |

⚑ **A port that loads the CSV correctly and joins on `display_name` instead of `record` produces a
PERMUTATION of multipliers across records — the right multiset, the wrong per-record assignment —
and passes all five.** (a)–(d) never look at assignment; **(e) is a mean, and a mean is invariant
under permutation.**

**This alternative is not invented.** Clause (c)'s own text establishes that **210 of the 7,900 rows
carry a comma inside `display_name`**, which already shifted the parse once and landed `0.0` =
LEECH-IMMUNE at the multiplier's index. **A join on `display_name` is the immediate neighbour of the
failure the clause was written to catch.**

⚑ **And clause (e) is the shape gandalf's § J table already indexes as instance 5** — *same file,
same column, two populations, two answers* (`0.266406` over 128 armed, `0.252215` over all 790). The
prereg fixed the **population** defect by putting the population in the clause's own sentence. **The
PERMUTATION defect is a different axis and is untouched.**

**What would close it, and it is three lines:** assert **three named records** with their expected
`adcth_mult_COUPLED`, chosen to span tiers (one at `0.35`, one at `0.25`, one of the 48 at `0.0`).
A permutation cannot survive three spanning spot-checks. **Routed as an observation, not a repair —
the prereg is immutable and this is gandalf's to author.**

### 4.3 · The row that discriminated by accident, and the mechanism is generalisable

`TA-B-09` (channel split) sits at **+32.5 half-widths with the WRONG SIGN**, against a confound that
predicts **−6.45**. The prereg reads it correctly: *"a genuine defect sits underneath."*

⚑ **The mechanism deserves a name, because it is the one way a confounded statistic still works:**
**a confounded statistic discriminates when the residual exceeds the confound's SIGNED prediction.**
That requires the confound's magnitude **and sign** to be derived first — which is exactly what
§ A.1's perfect-port table did. **`TA-B-09` is not a lucky row; it is the row that benefited from the
confound being quantified.** Quantifying a confound does not only excuse rows — **it rescues one.**

### 4.4 · ⚑ THE STRUCTURAL-ZERO CLASS HAS EIGHT MEMBERS AND § F.5 cl. 6 KNOWS ABOUT FOUR

| # | row | named by the prereg? |
|---:|---|---|
| 1 | `TA-X-11` wall-clamp zeros | ✅ |
| 2 | `TA-X-12` pool inertness | ✅ |
| 3 | `TA-X-19` arrival unconditionality | ✅ |
| 4 | `TA-X-15(b)` intra-point stagger | ✅ |
| ⚑ 5 | **`TA-X-13` no player crit** | ❌ |
| ⚑ 6 | **`TA-X-14` the two DO-NOTs** | ❌ *(and actively vacuous — the Type-A limb is absent)* |
| ⚑ 7 | **`TA-X-22` flag-off release cause** | ❌ |
| ⚑ 8 | **`TA-X-24` phase model, as stated** | ❌ *(caveated — see the row)* |

⚑ **The RULE is already right.** § F.5 cl. 6 — *every EXACT row satisfied by an ABSENCE prints the
absence* — needs no change. **The MEMBERSHIP LIST is short by four**, and it is short by four because
the class was discovered row-by-row, four separate times, rather than by asking the membership
question of the whole set at once. **The prereg's own remedy sentence is *"Stop re-discovering the
class; make the report print it."* The complementary half is: enumerate the members.**

The membership test is mechanical and takes one pass: **for every EXACT row whose assertion is a zero
or a negative, ask whether a port lacking the mechanism entirely scores the same.** Eight of 27
clause-rows do.

---

## § 5 · GROUP D — THE T-A DIAGNOSTIC ROWS

**19 ids. 2 DISCRIMINATING · 10 NON-DISCRIMINATING (9 declared) · 1 MIS-READ · 3 COULD NOT SETTLE · 3 NO INSTRUMENT.**

⚑ **The prereg already ran this audit on six of these and got zero out of six** (§ A.1). I confirm it
and report only what is new.

| id | verdict | note |
|---|---|---|
| `TA-B-01` terminal wave | **NON-DISC** *(declared)* | ⚑ the declaration to beat: *"its band admits every arm in the seal, including the G5 control the run built to be different."* **A band that admits your negative control is not a band** |
| `TA-B-02` uptime | **NON-DISC** *(declared)* | CANNOT FAIL at `T = 482` |
| `TA-B-03` `frac_moving` | **NON-DISC** *(declared)* | CANNOT PASS |
| `TA-B-04` `P(chan\|moving)` | **NON-DISC** *(declared)* | CANNOT FAIL — the confound pushes it at the clip |
| `TA-B-05` `P(chan\|stationary)` | ⚑ **COULD NOT SETTLE** | the dilution largely cancels and the residual's sign is not derivable from anything published. **The prereg declines to name a direction and I decline with it** |
| `TA-B-06` plant ratio | ⚑ **MIS-READ** *(declared, § F.3a)* | ⚑ **the sharpest instance in the corpus: the two sides computed DIFFERENT STATISTICS, and the symbol carried the ambiguity — the oracle's `n_window` is a TICK COUNT, the port's `n_windows` is a WINDOW COUNT. One name, two dimensions** |
| `TA-B-07` release duty | **NON-DISC** *(declared)* | ⚑ *"ONE ROW WITH A SIGN FLIP"* with `TA-B-02`. **Not independent evidence** |
| `TA-B-08` | **NON-DISC** *(declared)* | *"its sign may survive, its margin 0.0048 does not"* |
| `TA-B-09` channel split | ⚑ **DISCRIMINATING — IN THE EVENT** | § 4.3. Discriminating **because the residual exceeded the confound's signed prediction**, not because the band was well built |
| `TA-B-10` per-wave durations | ⚑ **NO INSTRUMENT** | authored at a grain the seal does not publish |
| `TA-B-11` arrival latency | ⚑ **NO INSTRUMENT** | absent from both seals and now from the port |
| `TA-B-12` intake / leech | ⚑ **NO INSTRUMENT** | ⚑ **and the run's largest divergence lives inside it (`C-e`)** |
| `TA-B-13` `max_body_radius_m` | **NON-DISC** *(declared)* | *"a band that rejects the oracle cannot grade a port"* |
| `TA-B-14` vetoes / occupancy | **NON-DISC** *(declared)* | raw counts 0–2, no denominator — and it carries `TA-X-06`'s entire mechanism |
| `TA-B-15` NO-DATA fraction | **NON-DISC for the port** *(declared)* | measures the substrate; promotion permanently barred |
| ⚑ `TA-B-16` **released ticks per wave** | ⚑ **NON-DISCRIMINATING — undeclared. § 5.1** | ⚑ **its NUMERATOR HAS TWO GRAINS** |
| `TA-B-17` stationary ticks / wave | ⚑ **COULD NOT SETTLE** | no width exists; the immunity claim is by mechanism and the calibration range cannot test it |
| `TA-B-18` motion-suppressed ticks / wave | ⚑ **COULD NOT SETTLE** | same |
| `TA-B-19` **ticks per wave** | ⚑ **DISCRIMINATING** | ⚑ **it IS the dilution factor. It measures the confound directly instead of correcting for it — the only row in the diagnostic set that can falsify the others' calibration assumption** |

### 5.1 · ⚑ `TA-B-16`'s IMMUNITY CLAIM HAS A HOLE THE GRAIN LAW DOES NOT COVER

§ C.6's mechanical test is *"a fraction is confounded iff its numerator and its denominator scale
with **different** quantities."* `TA-B-16` is `released ticks / n_waves` — **per-wave over per-wave**,
and the prereg marks it **IMMUNE by construction.**

⚑ **The test assumes the numerator has ONE grain. It has two.**

| release type | trigger | grain |
|---|---|---|
| **Type-A** | wave transition | ⚑ **per-WAVE** — count per wave is invariant in wave length |
| **Type-B** | cast | ⚑ **per-TIME** — count per wave scales with wave DURATION |

So `released ticks per wave` is a **mixture**, and the mixture is scale-free **only if the Type-A :
Type-B composition matches on both sides.** ⚑ **It is known not to: the port has no Type-A limb at
all** (§ F.3b's own words, and `TB-RL-02`'s 11 Type-A vs `TB-RL-03`'s 8 Type-B in the footage). The
port's releases are 100 % per-time, over waves **2.985× longer**.

**So `TA-B-16` is confounded in the opposite direction from `TA-B-07`** — it under-charges the port —
and the 5× → 1.5× improvement the prereg quotes is real but is **partly the new confound cancelling
the old one**, not purely the removal of a distortion.

⚑ **This is not a correction to § C.6. It is an EXTENSION of it**, and it is the clause the Grain Law
is missing:

> ⚑ **A GRAIN IS A PROPERTY OF AN EVENT CLASS, NOT OF A COUNTER. Before declaring a rate scale-free,
> PARTITION ITS NUMERATOR BY TRIGGER and confirm every part shares the grain — and if the parts
> differ, the rate is scale-free only where the MIXTURE is held fixed.**

The prereg's § C.6 closing clause anticipated the general hazard — *"swapping one un-audited
invariance claim for another is how this defect would survive its own repair"* — and named
`TA-B-19` as the row that can falsify it. ⚑ **`TA-B-19` measures ticks-per-wave. It cannot see a
composition difference.** The row that would is a **per-wave release count split by type**, which the
port cannot emit because the Type-A limb is absent — ⚑ **and that absence is itself the answer.**

---

## § 6 · THE FOUR ROWS I COULD NOT SETTLE, AND WHY

| row | why I could not settle it | what would settle it |
|---|---|---|
| `TA-X-09` **nine `math_rules` test vectors** | ⚑ **Nine points pin a closed form and do not pin a piecewise rule, and no document states which shape `math_rules.json`'s nine rules have or which branches the vectors exercise.** Settling it means opening `P-h`'s pack and reading the rules — in scope for a sibling, **not** for a read-only audit that would then be asserting a pack fact without a derivation | **a per-rule branch-coverage statement beside each vector** — the same discipline `TA-X-18` already applies to the scatter law |
| `TA-B-05` `P(chan\|stationary)` | the dilution **largely cancels** and the residual's sign is not derivable from any published figure. ⚑ **The prereg declines to name a direction it cannot derive; naming one here would be exactly the invention Law 3 forbids** | the per-wave restatement, once `TA-B-17`'s width exists |
| `TA-B-17` stationary ticks / wave | ⚑ **no width exists — the slot is NAMED AND EMPTY.** There is no instrument to audit yet. Its immunity is claimed **by mechanism**, and the oracle's calibration range (ticks-per-wave ∈ [106, 185], 1.75×) **cannot test the claim** — the prereg says so itself | a width **plus** a calibration range that spans the realised 482.4. Only the F2 re-base can supply the second |
| `TA-B-18` motion-suppressed ticks / wave | same | same |

⚑ **I am also declaring a boundary on one row I DID settle.** `TA-X-24` is graded NON-DISCRIMINATING
**on the assertion as the prereg states it** (a negative: the hash is never evaluated). If the row
carries an unstated positive limb in the runtime, the verdict moves to DISCRIMINATING. **I could not
verify the runtime side without reading drax's seam, and I did not.**

---

## § 7 · ⚑ FLAGGED SEPARATELY, PER THE COMMISSION — WHERE THE ORACLE IS *ACTUALLY WRONG*, NOT MERELY UNVALIDATED

**This is a different class from the one commissioned and it is reported apart from the table.**

### 7.1 · `leech_uptime = 1.0` is pinned, and the footage says 0.23 – 0.37

`EnergyModel.net_per_s(leech_uptime=1.0)` credits Tip the Scales at its **full 100 /s bound**, and the
`−1.03 /s` boot gate holds it there to ± 0.005. The footage's two independent routes give:

| route | arithmetic | implied `leech_uptime` |
|---|---|---|
| on-channel net, published gross 176.4 | `−78 = −176.4 + 75.37 + 100u` | **0.230** |
| on-channel net, galadriel's gross ≈ 190 | `−78 = −190 + 75.37 + 100u` | **0.366** |
| off-channel income ≈ +112 /s | `112 = 75.37 + 100u` | **0.366** |

⚑ **A 2.7× to 4.3× over-credit on the leech term** — and C-1 reached the same place by a different
road (*"the unprovenanced part is crediting Tip the Scales at its full 100 /s bound"*).

⚑ **AND THE COINCIDENCE C-1 DECLINED TO CLAIM IS NOT ONE.** C-1 § 6(b) notes that the on-channel and
off-channel routes both land near a third of the bound and flags it *"as a numerical coincidence, not
a derivation."* ⚑ **C-1's OWN § 3 crux finding is why they agree:** the proc is gated on
`triggerType = HitByEnemy`, **channelling and being-hit are orthogonal axes**, so `U(h)` does not
depend on channel state. **Two routes landing on the same `U` is the mechanism's signature, not an
accident.** Under C-1's own `U(h) = 1 − 0.67^(2h)`, `U = 0.366` ⟹ **`h ≈ 0.57` incoming hits/s** —
an entirely ordinary rate for a Crucible pack at waves 151–160.

**Consequences, stated and not repaired:**
* **`h` is the free parameter, not a channel flag** — C-1 advisory 4, and `h` is already registered as
  `ABS-MONSTER-OFFENSE-NO-DATA-POOL466`.
* ⚑ **The oracle's model is wrong in its PINNING, not in its FORM.** With `leech_uptime` taken from
  the footage instead of pinned at 1, the *same* equation reproduces the *same* band in **0.88–1.40 s
  — the footage's measured excursion timescale** (§ 0.1). **The model was one free parameter away from
  reproducing the dynamics, and the instrument that would have found it was a band.**
* **`TIP_THE_SCALES_TRIGGER_CHANCE = 0.33` is dead in the code** because the function that would
  consume it was never written (C-1 § 4.3) — the bound shipped where the realized rate belonged.
* ⚑ **Routing:** this is a **design call above my seam** (C-1 advisory 5 says so) and it touches a
  boot-gated constant. **I changed nothing. Math-before-code applies: the re-derivation of
  `MO_DRAWDOWN_BAND` and the sustain net against the committed 20 Hz series is a math note owed
  before any constant moves.**

### 7.2 · Three smaller items in the same class

| item | what is wrong |
|---|---|
| ⚑ **`T1_TOLERANCE_S = 1.0` is graded `"MEASURED"`** | it is *"the semantic floor, pinned at G-B close"* — **a declared decision, not a measurement**, and the comment above it says so (*"NOT the instrument precision"*). ⚑ **`VALID_GRADES` already carries `DECLARED-FREE-PARAMETER` and it is used correctly two lines below for `SPAWN_RESOLUTION_S`.** A decision wearing a MEASURED badge. *(Counted as MIS-READ in the table)* |
| ⚑ **`T1_TOLERANCE_S` is a FIXED ABSOLUTE on a 12×-spanning quantity** | the measured clears run **7.03 – 82.13 s**. ± 1.0 s is **± 14 %** at wave 47 and **± 1.2 %** at wave 80. **A fixed absolute tolerance across a 12× range is a relative tolerance that varies 12×**, and nobody chose that profile — it fell out. *(It happens to be strictest on the ×10 waves, which is arguably the right direction; it is not a derived direction)* |
| ⚑ **`SHEET_EOR_DAMAGE_PER_HIT` vs the DB-component limb differ ×130.8 – 178.9** | `calibration.py` carries both player-damage limbs and the gap is E-6's magnitude. **Which limb runs is a live free choice with a 179× lever on outcome**, and no referent instrument adjudicates it |
| ⚑ **`FIXTURE_RUN_SPEED_PCT = 135.0`, cited *"AT the cap"*** | ⚑ **a measurement taken at a cap is CENSORED.** A character whose uncapped speed is 150 % reads 135. **The cite names the hazard and does not draw the consequence.** *(Counted as NO INSTRUMENT — it has zero consumers)* |

---

## § 8 · GROUP E — `MEASURED` GRADES THAT NOTHING IS CHECKED AGAINST

**6 rows. 4 NO INSTRUMENT · 1 MIS-READ · 1 NON-DISCRIMINATING.**

⚑ **Four `Cited(..., "MEASURED")` constants have ZERO consumers anywhere in
`src/reincarnated/simulation/kc2/` — verified by grep across the tree, not assumed:**

| constant | value | consumers |
|---|---|---:|
| `ENERGY_ABSORPTION_PCT` | 20.0 | **0** |
| `FIXTURE_BLOCK_CHANCE` | 0.0 | **0** |
| `FIXTURE_RUN_SPEED_PCT` | 135.0 | **0** *(and censored — § 7.2)* |
| `FIXTURE_IDENTITY_ENVELOPE_PCT` | (−0.5, +3.9) | **0** |

`fixture.py`'s own docstring says *"A reader who prints a constant sees where it came from."* ⚑ **A
reader who prints `FIXTURE_BLOCK_CHANCE = 0.0 [MEASURED]` reasonably concludes the model honours a
zero block chance. The model never reads it.** The claim may well be structurally true (no block limb
exists) — **but that is a structural zero, and § F.5 cl. 6's rule says an absence must be printed as
an absence.** The rule exists on the port side and has no oracle-side counterpart.

**Not a defect in the values. A gap between what the `Cited` wrapper looks like it asserts and what
it asserts** — which is the same shape as `TA-X-26`/trap 8: *the place where the claim is made cannot
check the claim.*

---

## § 9 · WHAT WOULD DISCRIMINATE — AND WHAT IS ALREADY ON DISK

| # | what | cost | status |
|---:|---|---|---|
| **1** | ⚑ **RE-DERIVE `MO_DRAWDOWN_BAND` AND THE SUSTAIN NET FROM THE COMMITTED 20 Hz ENERGY SERIES.** `D-GOODCOV` covers 85.77 % of combat; `s2-releases.json` carries 19 releases with per-release `dE/dt`; `MD-B4app-2` § 4.4 carries the below-cap net | ⚑ **NOT A COMMISSION — the data is committed and older than the grade** | **available today** |
| **2** | ⚑ **Report the energy globe the way B-19 reports the HP globe** — a tooth rule, order statistics, a threshold sweep, a named near-invariant. **The template exists one section away in the same note** | one lap, no new capture | **available today** |
| **3** | ⚑ **Enumerate the structural-zero class instead of discovering it.** One mechanical pass: *for every EXACT row asserting a zero or a negative, does a port lacking the mechanism score the same?* Eight of 27 do | one pass | **available today** |
| **4** | **Three spanning spot-checks on `TA-X-26`** — three named records × their expected `adcth_mult_COUPLED`, across tiers. Closes the permuted-join hole | three lines | gandalf's to author (prereg is immutable) |
| **5** | **A positive limb for `TA-X-04`** before OQ-1 retires `TA-X-06` (§ 4.1) | one row | **price it before ruling OQ-1** |
| **6** | **Widen MO-4's window** from wave 1 / 40 ticks to the declared 10-wave scope | free | — |
| **7** | ⚑ **`h` — incoming hits/s.** The one genuinely absent measurement in the energy stack | ⚑ **A COMMISSION** — registered as `ABS-MONSTER-OFFENSE-NO-DATA-POOL466`; pixels cannot supply it (`UNREACHED-4`) | **blocked; F2's decode is the first thing that could move it** |
| **8** | **Reconcile gross drain 176.4 (client) vs ≈ 190 (pixels)** — a 7.7 % fork carried NOT DERIVED and load-bearing on § 7.1's `U` | needs the MP4 (`matt_to_do` **T30**) | **blocked** |

⚑ **Six of eight need no new measurement.** The commission asked me to be honest when the answer is
*"a measurement we do not have."* **For the row that occasioned this audit, it is not. The
discriminating instrument was committed on 2026-08-25 and was never pointed at the band.**

---

## § 10 · THE DISCIPLINE THIS PRODUCES — one clause, and it is not a new rule

The Grain Law (§ C.6 / § J) already says: *before banding a rate, name the grain of its numerator and
its denominator separately.* This audit adds the question that has to be asked **one step earlier**,
and that would have caught the energy band, the T-A band half, `TA-B-06`, and the four unnamed
structural zeros **with a single sentence each**:

> ⚑ **BEFORE A STATISTIC IS ACCEPTED AS VALIDATING A PROPERTY, NAME ONE MATERIALLY DIFFERENT
> BEHAVIOUR THAT WOULD PRODUCE THE SAME NUMBER. IF YOU CAN NAME ONE, THE STATISTIC IS EVIDENCE ABOUT
> SOMETHING ELSE. IF YOU CANNOT, WRITE DOWN WHY YOU CANNOT — THAT SENTENCE IS THE INSTRUMENT'S
> WARRANT, AND A STATISTIC WITHOUT IT HAS NONE.**

**Three rows in the corpus already carry that sentence, written at authoring time**, and they are
three of the twenty DISCRIMINATING rows:

* ⚑ **`TA-X-18`** — *"polar → (−4.0, 0) · uniform-in-area → (−5.656854, 0) · box → (0.0, 0.0)."* **The
  alternatives are named on the row's face and the input was chosen where they separate.**
* ⚑ **`TA-X-16`** — *"a filter with no counter is indistinguishable from a filter that never fired."*
* ⚑ **`TA-X-27(b)`** — *"asserts the per-seed consumption counts, **never the mean**"*, because the
  distribution is geometric.

**The house can already do this. It does it when someone thinks to.** The gap is that nothing asks.

⚑ **And the answer to the commission's framing question.** Matt is about to declare the referent
battle system a line in the sand. **20 of 86 rows are load-bearing; 22 more are honestly declared as
not load-bearing, which is almost as good.** The 33 that carry weight they cannot bear are not
33 wrong values — ⚑ **I found exactly one row where the oracle is materially wrong (§ 7.1), and it is
one pinned parameter, not a broken model.** **A line in the sand does not require every instrument to
discriminate. It requires every instrument to SAY whether it does.** That is 33 sentences, most of
them one line, and § 9's items 1–3, 6 are the only ones that need work rather than words.

---

*Filed 2026-09-21 by gamora (simulation + spirit-guide seam), Run KC2-PLAY, under conductor
gandalf's discrimination-audit commission. **Analysis only — no code, no constant, no pack row, no
prereg row, no oracle value changed. K-7 held: no sealed cell opened or re-run.** Law 3 held: every
alternative behaviour named is drawn from the committed corpus or from the immediate neighbourhood of
a failure the run has already had, and the four rows I could not settle are named with their reasons
at § 6. **Every arithmetic result in § 0.1, § 2.1, § 2.3, § 7.1 and § 5.1 was derived here from the
cited documents, not transcribed.** No production code, no dispatch, no push.*
