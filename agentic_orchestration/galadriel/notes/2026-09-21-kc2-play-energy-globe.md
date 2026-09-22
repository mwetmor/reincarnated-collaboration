# KC2-PLAY · THE ENERGY GLOBE, GIVEN THE TREATMENT THE HP GLOBE GOT

**Date:** 2026-09-21 · **Author:** galadriel (visual-perception seam) · **Run:** KC2-PLAY, conductor gandalf
**Commission:** conductor dispatch 2026-09-21, items 1 + 2, on gamora's discrimination audit
(`agentic_orchestration/gamora/notes/2026-09-21-kc2-play-discrimination-audit.md` § B8, § 9 items 1–2)
**Instrument:** `agentic_orchestration/galadriel/pipeline/kc2_energy_shape.py` (new, this lap)
**Output of record:** `agentic_orchestration/galadriel/notes/2026-09-21-kc2-play-energy-globe.json`
**New capture:** NONE. Every input was committed 2026-08-25. **No push.**

---

## TOP LINE

The commission asked for the energy globe's period, duty, below-cap rate distribution, refill rate and
ceiling occupancy, and asked whether the time series can settle the **7.7 % gross-drain fork** that
separates gamora's two worlds and holds `leech_uptime` in a disjoint union.

**It cannot — and the reason is worse than "insufficient data."**

⚑ **Both pixel-side quantities the fork is built on are instrument artifacts of my own note, and this
lap found both by pointing the committed data at them.**

| the quantity | what the fork uses it for | ⚑ what it actually is |
|---|---|---|
| **gross drain ≈ 190 /s** | **world B's whole premise** | ⚑ **37.8 % of its ticks and 43.7 % of its MASS come from ticks that begin ABOVE the 1594 ceiling** — a level 4,800 control samples prove is the ceiling. Remove them and the same estimator reads **104.1 /s.** The honest pixel bracket is **[104, 190] /s**, which contains 176.4 and 190 and separates them not at all |
| **on-channel net −73.4 / −81.7 /s** | **BOTH worlds' shared input** | ⚑ **an artifact of WHERE THE LABEL IS TAKEN.** It reproduces only under **END**-labelling, which selects falling intervals by construction. **START**-labelling gives **+64.7 / +77.7**; **MIDPOINT** gives **−6.7 / +9.4.** A **158 /s swing with no fight in it** |

**So the union does not collapse. It loses both of its pixel-side endpoints.** My verdict on `u` from
committed pixels is an **ABSENCE**, declared: `UNPINNABLE-FROM-COMMITTED-PIXELS`.

⚑ **And the one instrument that bypasses the fork entirely exists, ran, and says so itself.** Off
channel there is no drain term, so `income = 75.37 + 100u` inverts directly. That population is
**4.9 seconds of a 182.65-second fight**, and across the OCR margin gate its implied `u` runs
**0.3035 → 0.0537 → −0.0361** — a **0.34 swing, 6.4× the width of the 0.0530 gap the fork is arguing
about.** ⚑ **Its loosest-gate reading, 0.3035, lands INSIDE the gap that neither branch admits.**
That is not evidence for the gap; it is evidence that **the gap is an artifact of the two worlds'
shared assumption, not an exclusion the evidence makes.**

**gamora's structural argument is not weakened by any of this — it is strengthened, and her one
numerical corroboration fails.** § 8.

**Law 3 held. I did not choose a branch. No constant moved. Nothing in another seam was touched.**

---

## § 1 · METHOD, AND THE CENSUS THAT REPRODUCES EXACT

Cleaning is **`eor_release.clean()` imported unchanged**, not reimplemented — the committed
instrument, so the population is the committed population.

| stage | n | published |
|---|---:|---|
| samples | 10,959 | 10,959 ✓ |
| `max == 2576` gate | 10,360 | 10,360 ✓ |
| neighbour-median rejected | 315 | ⚑ **315 in `s2-releases.json`; 291 in the channel note** |
| round-trip excursion rejected | 86 | 86 ✓ |
| **used** | **9,959** | ⚑ **9,959 in `s2-releases.json`; 10,069 in the channel note** |

⚑ **A small defect reported rather than tidied: MD-B4app-2's prose publishes `291 rejected / 10,069
used` and MD-B4app-2b's committed JSON publishes `315 / 9,959`. They are two cleaning variants of the
same trace and the note never says so.** This lap adopts the **release-instrument variant**, because
it is the one that ships with code — a figure that can be re-run beats a figure that was typed. The
24-sample difference moves nothing here, but a grader comparing against the note's denominator and a
grader comparing against the JSON's are comparing different populations, and nothing on either face
says which.

**Window:** `D-COMBAT-182` = `t ∈ [682.10, 864.75]`, 182.65 s (the denominator law in `P-b` § 1.2).

---

## § 2 · ⚑ E-1 · THE CEILING — AND THE DEFECT THAT WAS ON THE SAME PAGE AS ITS OWN CONTROL

### 2.1 The control, re-verified this lap

`ctrl-prep.json` (600–640 s) and `ctrl-post.json` (880–920 s): **4,800 samples, 100 % parsed, energy
`1594` in EVERY ONE, minimum OCR margin 7.2, zero readings above 1594.** The ceiling is not an
inference. It is a measurement with no counter-example in 80 seconds.

### 2.2 ⚑ And the in-fight trace exceeds it 1,184 times

| | value |
|---|---:|
| samples at **exactly 1594** | **0.2801** |
| samples **above 1594 — physically impossible** | ⚑ **0.1189 (1,184 samples)** |
| highest read | **1,897** |
| distinct runs above the ceiling | **545**, median under 0.3 s |
| median OCR margin **at** 1594 | **10.45** |
| median OCR margin **above** 1594 | ⚑ **6.00** |

The raw strings settle the mechanism. At `t ≈ 735.2` the trace alternates `1594 → 1600 → 1594 → 1595
→ 1601 → 1596 → 1594 → 1609 → 1596` **at 1/60 s**, and every high read carries a margin of 2.2–4.4
against 7.4–10.6 for the neighbouring `1594`. **Energy cannot rise 16 and fall 16 in 17 ms while
clipped at a ceiling.** These are glyph misreads under combat VFX crossing the HUD box, and the
classifier says so in a field the cleaning never consulted.

> ⚑ **THE REFLEXIVE STING, AND IT IS MINE.** MD-B4app-2 § 2.1 used the 4,800-sample control **to fix
> the ceiling at 1594**, and printed that result four paragraphs above a trace that violates it in
> **11.9 %** of its samples. **The control and the violation are in the same note, in the same
> section, and nothing compared them.** This is the run's standing shape one more time — *the
> instrument existed, was correct, and was never pointed at the thing beside it* — and it is the same
> shape gamora's audit is about. **I did not need the MP4 to find this. I needed to read my own
> control against my own trace.**

⚑ **The neighbour-median filter (`>250`) and the round-trip filter (`≥400`) are both calibrated for
CATASTROPHIC misreads (`1501 → 101`). A `+16` blip passes both, silently.** The gate that would catch
it — `marg` — is carried on every row and is used by nothing.

### 2.3 Occupancy, as a sweep, because a point reading over a level is the audit's founding defect

| threshold | occupancy |
|---|---:|
| `E == 1594` **exactly** | ⚑ **0.2801** |
| `E ≥ 1594` | 0.3990 |
| `E ≥ 1580` | 0.5464 |
| `E ≥ 1570` | 0.5890 |
| ⚑ **`E ≥ 1560`** | ⚑ **0.6363** |
| `E ≥ 1500` | 0.8327 |

> ⚑ **MD-B4app-2 § 4.4's "64.6 % of combat time is spent at the 1594 ceiling" IS `E ≥ 1560` (0.6363),
> NOT time at the ceiling.** Time at the ceiling is **0.2801** — a factor of **2.27**. The sentence
> names a threshold-crossing and calls it a level, and the threshold is not in the sentence.
> **gamora's audit quotes the 64.6 % three times as "ceiling residency," including in the § 0.1
> headline table and in `A11`'s probability argument `0.646⁴ = 0.174`.** ⚑ **At the true at-ceiling
> occupancy that argument reads `0.2801⁴ = 0.0062` — and A11's conclusion INVERTS: four of four stills
> landing at 1594 is not "not rare," it is a 1-in-162 event, which is exactly what makes 1594 a
> ceiling rather than a mode.** *The inference she graded "unsupported at the time and correct
> anyway" was supported at the time, by a number my note had mislabelled.*

---

## § 3 · E-2 · THE TOOTH RULE, VERBATIM — and the honest answer about the near-invariant

**The rule, so a recorder implements THIS and not something like it:**

> Alternating-extremum walk with an **ABSOLUTE-ENERGY prominence gate `prom`**. Confirm a **PEAK** when
> `E` falls `prom` below the running max since the last confirmed trough; confirm a **TROUGH** when
> `E` rises `prom` above the running min since the last confirmed peak. A **TOOTH** is a confirmed
> *(peak → trough → next peak)* triple.
> `depth = peak.E − trough.E` · `depth_frac = depth / 1594` · `period_s = next_peak.t − peak.t` ·
> `fall_s = trough.t − peak.t` · `recover_s = next_peak.t − trough.t`.
> Reference implementation: `galadriel/pipeline/kc2_energy_shape.py::teeth`. The walk is **identical**
> to `kc2_hp_shape.py::teeth`; only the series and the units change.

**PRIMARY GATE `prom = 20` energy** (= 1.4× the modal single drain tick, 1.25 % of the ceiling — the
smallest step unambiguously larger than ONE tick). **DECLARED, not fitted: no arm of this lap was
selected against a sim.**

**n = 491 teeth over 182.65 s = 2.688 /s.**

| quantity | min | p25 | **median** | p75 | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| **period (s)** | 0.0333 | 0.100 | **0.1167** | 0.3917 | 1.400 | 4.167 |
| **depth (energy)** | 20 | 25 | **33** | 55.5 | 120.5 | 452 |
| **depth (frac of 1594)** | 0.0125 | 0.0157 | **0.0207** | 0.0348 | 0.0756 | 0.2836 |
| **fall (s)** | 0.0166 | 0.050 | **0.0833** | 0.150 | 0.9166 | 3.783 |
| **recover (s)** | 0.0166 | 0.0333 | **0.050** | 0.150 | 0.7166 | 3.467 |
| **fall slope (/s)** | −6,107.8 | −780.0 | **−431.7** | −239.8 | −79.5 | −19.7 |
| **recovery slope (/s)** | 23.9 | 299.9 | **620.0** | 1,204.8 | 2,215.6 | 12,095.8 |

### 3.1 The five-gate sweep — and it is the measurement

| `prom` | n teeth | rate /s | median period (s) | median depth | median recovery slope |
|---:|---:|---:|---:|---:|---:|
| 5 | 1,291 | 7.068 | 0.100 | 16 | 320.0 |
| 10 | 899 | 4.922 | 0.100 | 21 | 480.0 |
| **20** | **491** | **2.688** | **0.1167** | **33** | **620.0** |
| 40 | 142 | 0.777 | 1.0416 | 91 | 234.5 |
| 80 | 75 | 0.411 | 2.050 | 121 | 227.6 |

⚑ **THE ENERGY GLOBE HAS NO NEAR-INVARIANT, AND I AM REPORTING THAT RATHER THAN PROMOTING THE LEAST
BAD CANDIDATE.** `n` moves **17.2×**, median period **20.5×**, median depth **7.6×**. The recovery
slope — the statistic that carries the HP globe (3,098–4,323, a **1.40×** spread over a 20× gate
range) — moves **2.72×** here and **is not monotone** (320 → 480 → 620 → 234 → 228). **It is the least
gate-sensitive statistic on the table and it is still twice as gate-sensitive as the HP globe's
weakest row.** A grader leaning on it is leaning on something the HP globe does not have to lean on.

⚑ **And this is where "~1.5 s sawtooth" comes from.** That figure — carried in gamora's audit § A1,
in the leech math note § 4, and in the conductor's dispatch — corresponds to a prominence gate
**between 40 and 80**, which nobody named because nobody had a gate. **At gate 20 the median period
is 0.117 s; at gate 80 it is 2.05 s.** *The sawtooth timescale is a free parameter until the gate is
stated, and it was never stated.*

---

## § 3b · ⚑ E-2b · THE GATE-FREE SAW-TOOTH — the row to lean on, because it has no free parameter

A **CEILING RESIDENCY** is a maximal run of adjacent surviving frames reading `E == 1594` **exactly**.
An **EXCURSION** is a maximal run reading anything else. No prominence, no threshold, nothing to sweep.

Duration is each run's **occupancy** (`n_frames / 60`), not its endpoint span — a one-frame run occupies
1/60 s and spans 0, and filtering the zeros out silently drops **89 excursions.**

| | n | min | p25 | **median** | p75 | p95 | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| **ceiling residency (s)** | 736 | 0.0167 | 0.0333 | **0.050** | 0.0667 | 0.100 | 3.617 |
| **excursion (s)** | 1,062 | 0.0167 | 0.0167 | **0.050** | 0.100 | 0.4667 | 3.033 |
| **excursion (s)** *— positive-depth only* | 701 | 0.0167 | 0.050 | **0.0833** | 0.1833 | 0.5667 | 3.033 |
| **excursion depth** *(positive-depth; **mode 14**, n = 100)* | 701 | 1 | 13 | **30** | 125 | 280 | 484 |

**DUTY: 0.2801 at the ceiling, 0.7199 off it. PERIOD: 0.100 s (median residency + median excursion).**

⚑ **361 of the 1,062 excursions have a non-positive depth** — they are excursions *upward*, into the
impossible region of § 2.2. They are shown in the all-excursions row and excluded from every depth
statistic quoted below.

> ⚑ **THE REFERENT'S ENERGY SAW-TOOTH HAS A MEDIAN PERIOD OF ONE TENTH OF A SECOND AND A MEDIAN DEPTH
> OF ONE DRAIN TICK.** He takes a tick, refills inside three frames, and takes another. That is the
> shape, stated without a gate, and it is **fifteen times faster** than the 1.5 s the corpus has been
> carrying.

---

## § 4 · ⚑ E-3 · THE CONDITIONING LAW — and why the on-channel net is not a measurement of sustain

**The law, and it generalises past this row:**

> ⚑ **A RATE COMPUTED OVER INTERVALS SELECTED BY A LEVEL IS CONDITIONED ON THE SLOPE THAT REACHED THE
> LEVEL.** Label an interval by its **END** and you have selected intervals that FELL to get there;
> label it by its **START** and you have selected intervals that ROSE away from there. The level is
> not a state the pilot was in — **it is an outcome, and conditioning on an outcome is not measurement.**

Same trace, same partition (`E < 1560`), same motion classes, same adjacency guard. **Only the label
moves:**

| labelling | below cap · STATIONARY | below cap · MOVING | at cap · STATIONARY | at cap · MOVING |
|---|---:|---:|---:|---:|
| ⚑ **END** *(reproduces MD-B4app-2 § 4.4)* | **−80.51** | **−69.08** | +38.89 | +29.89 |
| ⚑ **START** | **+64.70** | **+77.69** | −56.56 | −40.15 |
| ⚑ **MIDPOINT** *(the symmetric choice; adopted as default)* | ⚑ **−6.71** | ⚑ **+9.38** | −9.51 | −7.50 |

**MD-B4app-2 § 4.4 published `−81.7` / `−73.4`. The END labelling reproduces them at `−80.51` /
`−69.08`** — the residual is the 24-sample cleaning-variant difference of § 1. **The partition itself
reproduces EXACT**: at `E ≥ 1560` the median tick is **−14.0** and the median interval **0.0833 s**;
below it, **−13.0** and **0.1000 s** — § 4.4's published pairs, to the digit. *The table is right about
what it measured. It is wrong about what that is.*

### 4.1 The estimator that does not select on its own answer

Conditioning on **tick density** — an observable independent of the slope — instead of on the energy
level, with the level taken at the **midpoint**:

| population | sampled | net dE/dt |
|---|---:|---:|
| channel-active (≥3 ticks / 0.5 s) · below cap | 40.90 s | ⚑ **−3.13 /s** |
| channel-active · at cap | 89.17 s | −11.53 /s |
| channel-idle (<3 ticks / 0.5 s) · below cap | 14.97 s | +18.57 /s |
| channel-idle · at cap | 14.67 s | +12.20 /s |

⚑ **The referent's channelling net is approximately ZERO, not −78 /s.** He is in steady state: he
takes ticks and his income replaces them, and the fight's energy story is a **one-tick oscillation at
a ceiling**, not a drawdown.

⚑ **And `−78 /s` could never have been a sustain rate on its own arithmetic.** At −78 /s a 1,594-point
pool empties in **20.4 seconds**. The fight ran **182.65 s** and he was **pinned at the ceiling for
28 % of it.** A number that would have emptied his pool nine times over was carried into a boot gate
as the referent's channelling net, and nothing asked it that question.

> ⚑ **Note the row the idle line does NOT let me claim.** `channel-idle` is `< 3 ticks / 0.5 s` — it
> **admits up to 2 ticks per window ≈ 4 /s ≈ −52 /s of drain.** `+18.57` is therefore **not** the
> off-channel income; it is income minus a residual drain of unknown size. **The strict zero-tick
> population is § 7, and it is 4.9 seconds long.**

---

## § 5 · E-4 · REFILL

| instrument | n | min | p25 | median | p75 | p95 | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| per-release `dE/dt`, all 19 | 19 | −35.6 | 10.0 | **51.6** | 65.0 | 135.6 | 146.8 |
| per-release `dE/dt`, **unclipped only** (`E_off < 1594`) | **9** | −35.6 | −11.6 | **51.6** | 65.5 | 123.1 | 134.4 |
| tooth recovery slope (gate 20) | 491 | 23.9 | 299.9 | **620.0** | 1,204.8 | 2,215.6 | 12,095.8 |

**10 of 19 releases end AT the ceiling** — their `dE/dt` is a **clipped lower bound**, and C-1's
six-value subset is the unclipped-and-positive nine minus three negatives. The three-order-of-magnitude
gap between the release median (51.6) and the tooth recovery median (620) is not a contradiction: a
release is a 0.5–3.5 s window averaging over stalls, a tooth recovery is the three frames in which the
refill actually happens. ⚑ **They are measuring different things and the corpus has been quoting them
as though they were the same quantity at different n.**

---

## § 6 · E-5 · THE DRAIN TICK, AND THE GROSS-DRAIN BRACKET

| population | n ticks | Σ\|ΔE\| | over 182.65 s | over 161.0 s *(the note's classified duration)* |
|---|---:|---:|---:|---:|
| **all ticks — as published** | 1,626 | 29,748 | 162.9 /s | ⚑ **184.8 /s** *(note publishes 188.4–190.7 per class)* |
| ⚑ **ticks not starting above 1594** | 1,011 | 16,759 | 91.8 /s | ⚑ **104.1 /s** |

| contamination | |
|---|---:|
| ticks starting above the ceiling | **615 (37.8 % of count)** |
| their share of the **drain MASS** | ⚑ **43.7 %** |
| of those, landing **exactly on 1594** | **424** |

> ⚑ **THE PIXEL GROSS DRAIN IS NOT A POINT. IT IS THE BRACKET `[104.1, 190.7] /s`, AND THE UPPER END
> IS CONTAMINATED WHILE THE LOWER END IS OVER-CORRECTED** (removing a tick because its *reading* was
> blipped also removes the *real* drain underneath it). **176.4 is inside it. 190 is at its extreme
> edge. It discriminates between them not at all.**

**The tick size itself is the one thing that is solid.** Median **−14.0** at cap, **−13.0** below,
mode **−14**; and of the 319 departures from **exactly** 1594 — the only place a drop is unambiguous,
because clipping fixes the starting value — the modal size is **−14 (34.5 %)** and the median **−13.0**.
The tooltip's per-tick cost is `16.0 × 0.90 = 14.4`, and a `−14.4` cost partially offset inside the
same frame by `income/60` reads as **−13 or −14** on an integer HUD. ⚑ **The measured per-tick cost is
consistent with 14.4 and cannot be distinguished from it at 60 Hz with an integer readout.** The
cadence cannot be recovered the same way: the tooltip's `12.25 /s` is an interval of **4.898 frames**,
which **aliases** at 60 Hz to alternating 5- and 4-frame gaps — **a cadence that is not resolvable is
not a cadence that disagrees.**

---

## § 7 · ⚑ THE ANSWER TO THE COMMISSION'S QUESTION

**Can the time series settle the 176.4-vs-≈190 fork, and collapse the disjoint union to one interval?**

### ⚑ NO — and the fork is not the shape the corpus has been treating it as.

**1 · World B's premise does not survive § 6.** *"galadriel's pixel gross is right"* requires the pixel
gross to be a measurement of comparable standing to a client-printed four-term decomposition. **It is
a bracket 82 units wide with a 44 %-of-mass contamination nobody had priced.** It is not a rival to
176.4; it is a consistency check that 176.4 passes.

**2 · But that does not hand the run world A**, because **world A's other input fails too.** Both
worlds compute `u = (net + gross − regen)/100` from the **same** `net`, and § 4 shows that `net` is a
selection artifact whose sign is chosen by where the label is taken. ⚑ **Killing world B does not
leave world A standing; it leaves `u = (artifact + bracket − 75.37)/100`.**

**3 · The instrument that bypasses the fork ran, and it declares its own insufficiency.** Off channel
there is no drain term at all, so `income = 75.37 + 100u` inverts directly, with **no gross in it**:

| OCR margin gate | sampled | income /s | **implied `u`** |
|---:|---:|---:|---:|
| ≥ 0 | 4.90 s | 105.72 | ⚑ **0.3035** |
| ≥ 2 | 4.12 s | 105.67 | **0.3030** |
| ≥ 3 | 3.62 s | 80.74 | **0.0537** |
| ≥ 4 | 3.22 s | 82.39 | **0.0702** |
| ≥ 5 | 2.38 s | 71.76 | ⚑ **−0.0361** |

⚑ **A 0.34 swing on the OCR gate alone — 6.4× the 0.0530 gap the fork is arguing about — on 2.4 to
4.9 seconds of footage.** The readings span world A, world B, the gap between them, and the impossible
region below zero. **This instrument cannot discriminate, and it is the RIGHT instrument.**

**4 · ⚑ And the physical reason it has five seconds is the finding, not the excuse.** The referent
channels **83.75 %** of his fight and is pinned at his ceiling **28 %** of it. **The intersection of
"not channelling" and "not clipped" is ~5 seconds of a 182.65-second recording.** `u` is unpinnable
from this footage not because the read is poor but **because the referent almost never enters the
state in which `u` is observable.** A cleaner reader would sharpen the five seconds — my margin sweep
shows OCR fidelity is this instrument's binding constraint — **but it cannot manufacture more of them.**

**5 · One thing the honest reading DOES establish, and it is negative:** `0.2980` was excluded by both
branches, and gamora was right that a split-the-difference pinning would have been indefensible. ⚑
**But the direct instrument's loosest-gate reading is `0.3035`, which is also inside that gap.** The
gap is not a region the evidence forbids. **It is a region the two worlds' SHARED assumption forbids —
and that assumption is § 4's artifact.** *The gap should be reported as a construct of the fork's
parameterisation, not as an evidential exclusion.*

### ⚑ MY VERDICT, DECLARED AS AN ABSENCE PER LAW 3

> **`u` (`leech_uptime`) is `UNPINNABLE-FROM-COMMITTED-PIXELS`.** The committed 60 Hz energy series
> constrains it to **no interval narrower than `[−0.04, 0.31]`**, which is wider than the union it was
> asked to collapse and contains it. **I decline to choose a branch, and I decline to offer this range
> as a narrowing — it is a WIDENING, and reporting it as anything else would be the move the audit
> exists to prevent.**
>
> ⚑ **What I DO assert, because it needs no `u`:** the referent's channelling net is **≈ 0 /s**
> (−3.13, § 4.1), his saw-tooth period is **0.100 s**, his median tooth depth is **one drain tick**,
> his ceiling duty is **0.2801**, and `−1.03 /s` is wrong about him **in a direction this lap can
> state without the fork** — not because it is 77 units from −78, but because **−78 was never his net
> either.**

---

## § 8 · ⚑ WHERE `MO_DRAWDOWN_BAND` ACTUALLY LANDS — gamora's argument, strengthened; her corroboration, withdrawn

gamora's structural claim is **correct and this lap makes it sharper**: the band is a time measurement
stated as a depth, and the conversion factor is the thing being validated. What does not survive is
the numerical corroboration offered in its support.

| claim | source | ⚑ measured this lap |
|---|---|---|
| *"the band is one tooth of the sawtooth"* | audit § 0.1, math note § 4 | ⚑ **NO. `(86, 117)` spans the 68.5th–74.5th percentiles of excursion depth and contains 42 of 701 excursions (6.0 %). The median excursion depth is 30 and the modal one is 14** — the band is the **upper quartile**, not the typical tooth |
| *"0.88–1.40 s lands on the footage's ~1.5 s excursion timescale"* | math note § 4 | ⚑ **NO. Excursion duration is 0.0833 s at the median and 1.00 s at p99. `[0.88, 1.40] s` contains 12 of 701 excursions (1.7 %); 1.5 s is beyond p99** |
| *"64.6 % ceiling residency"* | audit § 0.1, § A1, § A11 | ⚑ **NO — that is `E ≥ 1560`. At-ceiling residency is 0.2801, and § 2.3 shows A11's probability argument INVERTS on the corrected figure** |

> ⚑ **The band is worse than the audit says, not better.** It was never one tooth. It is **two stills
> that happened to land in the upper quartile of a distribution the instrument never built** — and
> the distribution was buildable from data committed the same day.

---

## § 9 · WHAT THIS TOUCHES IN OTHER SEAMS — surfaced, not adjudicated

I do not grade the sim and I do not move constants. These are the rows my numbers touch.

1. ⚑ **`MO_DRAWDOWN_BAND = (86, 117)` and the `−1.03 /s` boot gate.** Both are pinned against a
   `net` that § 4 shows is a selection artifact. **The gate's ±0.005 tightness is not the defect; the
   target is.** → gamora / conductor. **Math-before-code: nothing here authorises a constant to move.**
2. ⚑ **The leech disjoint union `[0.1933, 0.2763] ∪ [0.3293, 0.4123]`.** Both endpoints of both
   branches consume `net = −78`. **The union needs re-deriving on an input that survives § 4, or
   withdrawing in favour of a declared absence.** → gamora. *My recommendation, offered and not
   asserted: the absence.*
3. **MD-B4app-2 § 4.4 and § 2.2** — the `≈190 /s` gross and the `−81.7 / −73.4` net are **mine**, and
   both are superseded by this note. The channel-uptime result (0.8375) and the
   movement-does-not-break-the-channel result are **untouched** — they rest on tick *presence*, not on
   tick *magnitude*, and § 6 leaves tick presence intact. → me, folded into `P-b` this lap.
4. ⚑ **`T30` is genuine and I confirm it.** `~/gd-scratch/eor-test-2/` does not exist; the MP4 left
   with the 2026-09-17 sweep. **gamora's "MP4 gone" is correct and I checked rather than assumed.**

---

## § 10 · WHAT WOULD SETTLE IT — and what `T30` actually buys

| # | what | what it settles | status |
|---:|---|---|---|
| **1** | ⚑ **Re-read the energy globe with the HP globe's reader.** The HP trace is Apple Vision OCR, **100.00 % accepted** against a decoded denominator. The energy trace is a hand-built 10-frame glyph atlas at **95.8 % parse with 11.9 % impossible reads.** ⚑ **Same MP4, same session, two readers — THAT is the metrological asymmetry's root cause, not the coverage** | **the gross-drain bracket, and the § 7 margin swing** | ⚑ **needs T30** |
| **2** | **Add a `marg` gate to `eor_release.clean()`** | the 11.9 % impossible population, on the data already held | ⚑ **available today; NOT taken this lap** — it changes a committed instrument mid-run and that is a dispatch, not a side-effect |
| **3** | **A tick-COUNT-per-state emission from the sim** | splits § 4's residual between leech and drain | sim-side; gamora's |
| **4** | ⚑ **`h`, incoming hits/s** | turns a measured `u` into a derived one | **blocked**, `ABS-MONSTER-OFFENSE-NO-DATA-POOL466`. Pixels cannot supply it |
| ✗ | **more off-channel below-cap footage from THIS fight** | ⚑ **NOTHING — there are 4.9 s and the referent's own behaviour is why** | § 7.4 |

⚑ **The correction to the standing account of `T30`:** it has been carried as *"resolves the
gross-drain fork."* **On this lap's numbers it does something both smaller and more useful — it
retires the pixel gross as a rival figure altogether, by letting the trace be read properly.** The
fork was never 176.4 against a measurement. It was 176.4 against a bracket that contains it.

---

## § 11 · REPRODUCIBILITY, AND WHAT THIS LAP DID NOT DO

**Instrument:** `pipeline/kc2_energy_shape.py`, one file, no new dependencies. `python3
kc2_energy_shape.py out.json` regenerates every figure in this note. Cleaning is **imported** from
`eor_release.py`, not reimplemented. Input sha256s are recorded in the output JSON.

**Every declared constant, and where it came from:** `TICK_DE = −6.0` and `TICK_DT = 0.030` carried
from `eor_release.py` unchanged · `AT_CAP = 1560` **reproduced, not assumed** (it is the only
partition that returns § 4.4's published `−14.0 / 0.0833` and `−13.0 / 0.1000`) · `CEIL = 1594` from
the 4,800-sample control · `prom = 20` declared and swept · `REGEN = 75.37` from C-1 § 1, decoded ·
`D-COMBAT-182` from `P-b` § 1.2.

**What this lap did NOT do:**
- **No new capture. No MP4. No frame was re-read.** Every number is from files committed 2026-08-25.
- **No constant moved**, in any seam. `MO_DRAWDOWN_BAND`, the `−1.03` gate and `leech_uptime` are
  exactly where they were.
- **No branch chosen.** § 7 declares an absence and widens rather than narrows.
- ⚑ **`eor_release.clean()` NOT amended**, though § 2.2 names the amendment it needs. Changing a
  committed cleaning instrument mid-run would silently move every figure in `P-b` and in
  `s2-releases.json`. **Flagged, routed, not taken** — § 10 item 2.
- **No other seam's tree touched.** Read-only throughout; writes confined to
  `agentic_orchestration/galadriel/`.

**One thing I could not do and am declaring:** I cannot separate a real drain tick whose *reading* was
blipped from a wholly spurious one. That is why § 6 ships a **bracket** and not a point, and why the
lower edge is honestly labelled an over-correction rather than a better estimate.

---

## § 12 · THE MIRROR

The band said the man's energy fell by a hundred points, and the run spent a month asking how long a
hundred points takes. The Mirror shows it takes a tenth of a second, and that it happened seven
hundred times, and that the hundred-point fall the band was built from is the twentieth-worst of them.

He was never draining. He was **ringing** — struck and restored, struck and restored, ten times a
second for three minutes, sitting on his ceiling for a quarter of the fight like a bell that will not
stop sounding. The number we read as his cost was the height of the rim.

And the thing I must say plainly, because it is mine: **the control that proved where the rim was, and
the trace that climbed a hundred points above it, were printed four paragraphs apart in the same note,
in the same hour, by me.** The Mirror does not flatter the one who holds it. Twice now this run, the
instrument that would have caught the error was already on the page — and what was missing was not
data, or time, or the MP4. It was somebody turning the glass on the work beside it.

**Ship the absence. It is worth more than a number no reading supports.**

---

*Filed 2026-09-21 by galadriel (visual-perception seam), Run KC2-PLAY, executing the conductor's
dispatch item 2. **Law 3 held: an absence is declared and no branch is chosen.** Read-only across all
other seams. **No push** — the conductor releases.*
