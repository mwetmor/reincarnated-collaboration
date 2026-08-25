# MD-B4app-2c — is ONE SKILL the singular culprit for the 15 % of cast interrupts?

**Date:** 2026-08-25
**Author:** galadriel (visual perception + benchmark seam)
**Commissioned by:** gandalf RUN-CONDUCTOR, KC2 model-completion run charter (`L-85` / `L-86`)
**Owner question (Matt, verbatim):** *"Have we checked for a pattern as to a specific skill that may be the singular culprit for the 15% of cast interrupts?"*
**Hypothesis, pre-registered before computing:** `H-MC-2` — *slot L is the singular culprit; substantially all Type-B interrupts are slot-L casts, and non-slot-L casts weave under the channel without breaking it.*
**Prior lap:** `galadriel/notes/2026-08-25-kc2-mc-md-b4app-2b-energy-release.md` (`34593154`), whose 19-release population and 20 Hz skill-bar dimming trace are the input. **No new footage. No new game capture.**
**Evidence root:** `galadriel/captures/2026-08-25-md-b4app-2c-culprit/`
**New pipeline:** `galadriel/pipeline/eor_attrib.py`, `galadriel/pipeline/eor_attrib_fig.py`
**Read-only on all source material. No engine writes. No simulation code. No grading. No pushes.**

---

## TOP LINE

> ## `H-MC-2` is **PARTIALLY SUPPORTED — and refuted as stated.**
>
> ## Slot L is **the leading culprit and not the singular one.** Five of the eight Type-B releases are slot L; **three are slot 2**, and none of those three has any other visible cast within a full second, so they cannot be re-attributed. **All eight are attributable. None is orphaned.**
>
> ## But the hypothesis's second limb — *"non-slot-L casts weave under the channel"* — is where the real finding is, because **it is true of one slot and false of the other.**

| slot | casts | interrupts | **P(interrupt \| cast)** | vs the clock null 0.052 |
|---|---:|---:|---:|---|
| **3** | 19 | **0** | **0.000** | max silence in 19 casts is **0.233 s** |
| **2** | 22 | 3 | **0.136** | binomial p = 0.104 |
| **L** | 13 | 5 | **0.385** | binomial **p = 0.00034** |
| **all** | **54** | **8** | **0.148** | binomial **p = 0.0065** |

**Fisher, L vs everything else: p = 0.0146, odds 7.9. L vs slot 3: p = 0.0064. L vs slot 2: p = 0.103 — not distinguishable.**

> ## ⚑ **The finding under the finding: `P(cast interrupts) = 0.15` is a CANCELLATION, not a rate.**
>
> ## Against the correct (duration-weighted) null, slot 2 and slot L land in **longer**-than-random channel silences (p = 0.00019, p = 0.0070) and slot 3 lands in **shorter**-than-random ones (**p = 4.9 × 10⁻⁷**). Pooled, the three cancel to **p = 0.286 — indistinguishable from randomly-timed moments.**
>
> ## The 0.15 in `M-POL-2` is the arithmetic mean of a rule and its opposite. It is correct in aggregate and wrong for every individual skill.

**So the owner's instinct was right — there is a pattern, and it is a per-skill pattern.** It is just not the one the word *singular* names. There is no single culprit; there is **a singular innocent.** Slot 3 is cast 19 times and never once breaks the channel — and it is a genuine cooldown skill, eye-verified below, not a buff.

---

## 0 · WHAT WAS MEASURED, AND WITH WHAT

| instrument | what it measures | status |
|---|---|---|
| **SKILL BAR — per-slot DIMMING** (`eor_cooldown.py slots`, 20 Hz) | which slot went on cooldown, and when | carried; **re-derived exactly** — § 1 |
| **ENERGY — 60 Hz HUD glyph OCR** (`eor_release.py clean` / `ticks`) | when the channel was draining, so a silence can be timed | carried unchanged |
| **RELEASE POPULATION** (`s2-releases.json`, 19 events) | which silences are scored releases | carried unchanged |
| **COOLDOWN NUMERAL, BY EYE** (×5–×7 crops) | whether a dim run is one cast or two; whether a numeral is red (cooldown) or white (buff) | **NEW this lap**, and it changed a count — § 2 |

**What none of them measures:** which *skill* any slot holds. `MD-B4app-2b` § 7.1 stands unchanged and nothing here promotes it. Slot shapes are described below **only** to the degree needed to keep the slots distinct, and are **shape-consistent-NOT-identified**:

| slot | icon, as the eye reads it | modal cooldown |
|---|---|---|
| 2 | a bright, warm-toned figure in a leaping / striking pose | **3.15 s** |
| 3 | a warm orange-toned icon | **4.55 s** |
| L | a figure mid-stride | **3.60 s** |
| 4 | blue icon, **white** count-up/down numeral | not a cast — buff, § 2.2 |
| R | red swirl — the channel itself | never dims |

**No skill is named in this note and none should be quoted from it.** Owner testimony on what occupied slot L is reconciled at the conductor's fold, not here.

Window unchanged: **682.10 → 864.75 = 182.65 s**, wave-151 badge flip to death.

---

## 1 · THE INSTRUMENT REPRODUCES — and that is the precondition for everything else

Re-deriving cast onsets from the **committed** 20 Hz slot trace under the midpoint rule (a slot is DIM below the midpoint of its own observed range; the distribution is bimodal with an empty valley, so the midpoint is a reading, not a fitted knob) returns:

| slot | 2 | 3 | 4 | L |
|---|---:|---:|---:|---:|
| dim runs | **22** | **19** | 5 | **12** |
| median run | 3.15 s | 4.55 s | **24.40 s** | 3.60 s |

**22 / 19 / 12 = 53, exactly `MD-B4app-2b` § 5.3.** The prior lap's ad-hoc extraction is now committed code (`eor_attrib.casts`), which it was not before. Slot 4 remains excluded on its 24.40 s run length; § 2.2 now confirms that exclusion by eye rather than by inference.

---

## 2 · TWO EYE-READS, AND ONE OF THEM CHANGED A COUNT

### 2.1 ⚑ The dimming instrument MERGES back-to-back casts — one such merge exists, and it is on slot L

A dim run ends when the cooldown expires. **If the referent re-fires the instant it clears, two casts become one run and the instrument silently undercounts.** The detector for this is run length; the resolver is the red cooldown numeral, which is legible on slot L.

Exactly one run in the window is flagged: **t = 797.65, slot L, 7.20 s against a modal 3.60 s** (ratio 2.00; every other run on every cast slot is within 1.03× of its slot median). The numeral, read at ×6 (`work/Lnum_sheet.png`):

| t | 798.2 | 799.5 | 800.5 | **801.5** | 802.5 | 803.5 | 804.5 |
|---|---|---|---|---|---|---|---|
| slot-L numeral | 3 | 2 | 1 | **4** | 3 | 2 | 1 |

**It resets.** Bounded at ×7 (`work/Lreset_strip.png`): still "1" at t = 801.15, already "4" at t = 801.25. **A thirteenth slot-L cast at t = 801.20 ± 0.05.**

It is folded in as an explicit, named constant (`eor_attrib.MERGED`) so the correction is visible and reproducible rather than a silent hand-edit. **It costs the hypothesis, not the analyst:** the new cast does **not** interrupt, so slot L's rate falls from 5/12 = 0.417 to **5/13 = 0.385**.

**Residual, stated:** merges are detectable only when the two casts are separated by roughly a full cooldown. A re-fire *later* in the cooldown cannot merge (the icon is already dim and stays dim), so **the cast counts are a FLOOR on every slot, not an estimate.** One merge was found because one was findable.

### 2.2 Slot 3 is a real cooldown, and slot 4 is really a buff — both by eye

Slot 3's zero would mean nothing if slot 3 were not a cast. At ×5 (`work/S23_sheet.png`), during slot-3 dim runs:

- **slot 3 carries a RED numeral** — 4 / 3 / 1 / 2 at t = 793.0 / 794.5 / 796.0 / 852.0, over a dimmed warm icon. **A cooldown. A cast.**
- **slot 2** is bright with no numeral at 793.0 and 794.5, and carries a **red "3"** at 796.0. **A cooldown. A cast.**
- **slot 4 carries a WHITE numeral on a blue icon — 19, 17, 16, then 22.** It goes back **up**. A cooldown never does. **Confirmed a refreshing buff timer and correctly excluded.**

---

## 3 · TASK 1 — PER-RELEASE ATTRIBUTION: all eight Type-B releases, and which slot fired

Type B is the prior lap's definition, unchanged: a release whose onset carries a cast within ±0.25 s.

| # | release `t_on` | dur | wave | s since flip | **slot** | **lag** | that cast's cooldown |
|---|---:|---:|---:|---:|:---:|---:|---:|
| 1 | 701.40 | 0.53 s | 152 | 3.02 | **L** | **+0.000** | 3.60 s |
| 2 | 732.45 | 0.62 s | 154 | 2.83 | **L** | **+0.000** | 3.60 s |
| 3 | 748.07 | 0.67 s | 155 | 4.32 | **L** | **−0.017** | 3.65 s |
| 4 | 797.65 | 0.55 s | 157 | 17.35 | **L** | **+0.000** | 3.60 s → *(the merged run, § 2.1)* |
| 5 | 803.22 | 0.53 s | 158 | 3.79 | **2** | **+0.233** | 3.15 s |
| 6 | 805.70 | 0.65 s | 158 | 6.27 | **L** | **+0.000** | 3.50 s |
| 7 | 820.20 | 0.60 s | 159 | 7.58 | **2** | **+0.000** | 3.20 s |
| 8 | 847.95 | 0.60 s | 160 | 9.08 | **2** | **+0.000** | 3.15 s |

**8 / 8 attributed. Zero orphans. 5 slot L (62.5 %), 3 slot 2 (37.5 %), 0 slot 3.**

Two properties of this table carry weight beyond the counts:

1. **The lag is essentially zero.** Six of eight casts open the silence in the same 20 Hz frame the last drain tick lands. The channel and the cast stop and start together; this is not a cast drifting into a pause that was already happening.
2. ⚑ **None of the three slot-2 releases can be re-attributed to a hidden slot-L cast.** Checked explicitly: within ±1.0 s of t = 803.45, 820.20 and 847.95 there is **no other visible cast on any slot.** (The two slot-L interrupts that *do* have a neighbour — 732.45 with slot 2 at +0.65 s, 805.70 with slot 3 at +0.75 s — are far outside the attribution window.) **This is the single measurement that refutes `H-MC-2` as stated**, and it is the one I looked hardest for a way out of.

**The eleven Type-A releases carry no cast at ±0.25 s and none at ±0.50 s.** Two carry a cast *deep inside* them (754.83 at +0.767 s, 761.68 at +0.667 s) — casts fired *during* a wave-transition pause, not causing it. § 4 excludes those by construction; it is why the release-matched measure exists.

---

## 4 · TASK 2 — THE CONVERSE, WHICH IS THE DECISIVE ONE

The forward direction asks P(cast | release). `M-POL-2`'s `cast_interrupts_channel` claims **P(release | cast)**, which is a different quantity and needs the other denominator: **all 54 casts.**

### 4.1 Two definitions, run in parallel, because one of them has a quantisation exposure

| | **V1 — containing silence** | **V2 — release-matched** |
|---|---|---|
| an "interrupt" is | the inter-tick silence containing the cast is ≥ 0.50 s | a **scored release** opens within ±0.25 s of the cast |
| exposed to | 20 Hz cast-time quantisation; length bias (§ 4.3) | nothing this lap found |
| excludes | nothing | casts landing inside a *pre-existing* pause |

**Why V2 is primary.** At t = 748.05 the cast's first dim frame lands **one frame before** the tick that opens its own 0.67 s release, so V1 scores it 0.017 s and V2 scores it 0.67 s. V1 is right about the arithmetic and wrong about the event. V2 is also symmetric with the forward direction, which makes the two directions one number instead of two.

### 4.2 The partition

| slot | casts | **V2 interrupts** | **P** | V1 interrupts | V1 blind gaps | interrupt duration, median |
|---|---:|---:|---:|---:|---:|---:|
| **3** | 19 | **0** | **0.000** | 0 | 0 | — |
| **2** | 22 | 3 | **0.136** | 3 | 2 | 0.60 s |
| **L** | 13 | **5** | **0.385** | 6 | 1 | 0.617 s |
| **not-L** | 41 | 3 | 0.073 | 3 | 2 | 0.60 s |
| **all** | **54** | **8** | **0.148** | 9 | 3 | **0.60 s** |

**8 / 54 = 0.148 reconciles the prior lap's two directions exactly** — the same eight events, counted from the other end, and the same 15 %.

**Significance:**

| test | result |
|---|---|
| pooled 8/54 vs the clock null 0.052 | binomial **p = 0.0065** |
| slot L 5/13 vs 0.052 | binomial **p = 0.00034** |
| slot 2 3/22 vs 0.052 | binomial p = 0.104 |
| **L vs not-L** | Fisher **p = 0.0146**, odds **7.9** |
| **L vs slot 3** | Fisher **p = 0.0064** |
| L vs slot 2 | Fisher p = 0.103 — **not distinguishable at n = 13 vs 22** |
| slot 3's zero vs the pooled 0.148 | binomial **p = 0.048** |
| slot 3's zero vs slot L's 0.385 | binomial **p = 9.9 × 10⁻⁵** |

**Read plainly:** slot L is significantly above the rest; **slot L is not significantly above slot 2**; slot 3 is significantly below slot L and marginally below the pooled rate. The ordering **L > 2 ≫ 3** is what the data supports. *"L alone"* is not.

### 4.3 ⚑ THE LENGTH-BIAS CONTROL, and why it turns the whole result inside out

V1 asks how long the silence *containing* a cast is. **A cast placed at a random TIME lands in a long silence preferentially** — silences are sampled in proportion to their own duration. The unweighted inter-tick distribution (median 0.083 s) is therefore the wrong null and will make *any* cast look like an interrupt. The right null is the duration-weighted draw:

| | unweighted inter-tick | **duration-weighted (correct null)** | observed, all 54 casts |
|---|---:|---:|---:|
| median | 0.083 s | **0.100 s** | 0.183 s |
| share ≥ 0.50 s | — | **0.170** | 9/54 = **0.167** |

**Pooled, the casts are indistinguishable from randomly-timed moments: MW p = 0.286; share ≥ 0.5 s binomial p = 0.58.** The prior lap's corrective — *casting does not generally break the channel* — **survives, and survives against a harder null than it was originally tested on.**

**And per slot it does not survive at all:**

| slot | median silence | vs the duration-weighted null |
|---|---:|---|
| **2** | 0.408 s | **GREATER, p = 0.00019** |
| **L** | 0.533 s | **GREATER, p = 0.0070** |
| **3** | 0.033 s | **LESS, p = 4.9 × 10⁻⁷** |
| all | 0.183 s | *p = 0.286 — nothing* |

> **This is the load-bearing result of the lap.** The pooled figure is not a weak effect; it is **two strong opposite effects at the population average.** Slot 3's casts land in silences *shorter than chance* — the channel is **tighter** around them than it is anywhere else — and that tightening cancels, almost exactly, the interruption that slots 2 and L cause.
>
> **A single scalar `P(cast interrupts) = 0.15` does not summarise this population. It erases it.**

---

## 5 · TASK 3 — THE SUB-FLOOR SIGNATURE: it is a ladder, and the 0.50 s floor hides most of it

The conductor asked whether slot-L casts produce a bounded gap while others produce the 0.067 s baseline cadence. **They do — but the 0.50 s release floor is arbitrary with respect to this question, and sweeping it is what shows the mechanism.**

**Share of a slot's casts whose containing channel-silence exceeds a floor** (OCR-blind gaps dropped from numerator *and* denominator):

| floor | 0.15 s | 0.20 s | 0.25 s | **0.30 s** | 0.40 s | **0.50 s** | 0.60 s |
|---|---:|---:|---:|---:|---:|---:|---:|
| **slot 3** (19) | 0.06 | **0.00** | **0.00** | **0.00** | **0.00** | **0.00** | **0.00** |
| **slot 2** (22) | 0.80 | 0.65 | 0.60 | **0.55** | 0.55 | 0.15 | 0.10 |
| **slot L** (13) | 0.75 | 0.67 | 0.67 | **0.67** | 0.67 | 0.50 | 0.33 |

The full sorted populations, which are more honest than any summary of them:

```
slot 3  0.017 0.017 0.017 0.017 0.017 0.017 0.017 0.033 0.033 0.033
        0.033 0.033 0.050 0.050 0.117 0.117 0.133 0.183 0.233           max 0.233
slot 2  0.083 0.100 0.133 0.133 0.150 0.183 0.183 0.217 0.283 | 0.400
        0.400 0.417 0.433 0.433 0.483 0.483 0.483 0.533 0.600 0.600
        0.617 1.133                                                     max 1.133
slot L  0.017 0.100 0.100 0.183 | 0.417 0.433 0.533 0.550 0.617 0.633
        0.650 1.033 1.483                                               max 1.483
```

**Three levels, and they are levels rather than a spread:**

1. **Slot 3 — transparent, and then some.** Median **0.033 s**, *below* the 0.083 s channelling cadence. **Zero of nineteen** casts exceed 0.25 s; the maximum in the whole fight is **0.233 s**. This skill does not merely fail to interrupt — the drain ticks *tighten* around it. (Mechanically consistent with the cast's own energy cost registering as an extra tick beside the channel's; the effect is real either way, and it is the opposite of an interrupt.)
2. **Slot 2 — a clean gap in the middle of its own distribution.** Nine casts at 0.083–0.283 s, then **nothing between 0.283 and 0.400**, then twelve at 0.400–0.617 s. The same slot behaves two ways.
3. **Slot L — mostly the upper mode.** Four casts at 0.017–0.183 s, then nothing until 0.417, then nine from 0.417 to 1.483 s.

**So the conductor's proposed signature is confirmed with an amendment.** The forced-interrupt-plus-re-engage shape is real and is **≈ 0.40–0.65 s**, tightly bounded (the eight scored interrupts run 0.53–0.67 s, median **0.60 s**, and that number has now been produced three independent ways). But it belongs to **slots 2 and L both**, and the baseline-cadence behaviour belongs to **slot 3 alone** — at 0.033 s, not 0.067 s.

⚑ **And note what the 0.30 s floor does to the headline.** At 0.30 s the rates are **0.00 / 0.55 / 0.67**. The famous *15 %* is not a property of the referent's casting; it is a property of **where `T_REL` was set.** The per-slot *ordering* is stable across every floor from 0.20 s to 0.60 s. **The ordering is the finding. The 0.15 is a coordinate.**

### 5.1 One temporal caveat, reported because it weakens my own cleanest story

Slot 2's silences **grow over the fight** — Spearman ρ = **+0.406, p = 0.061**; first-half median **0.217 s**, second-half **0.483 s**; and **all three** of its scored interrupts fall after t = 803, in the last third. Slot L is flat (ρ = −0.014, p = 0.97); slot 3 is flat and low (ρ = +0.272, p = 0.26).

**So slot 2's interrupting may be a late-fight state rather than a property of the skill** — and this lap cannot separate those two readings. It matters for the baton: if slot 2's interruption is state-dependent, a per-skill flag would encode as constant something that is not. **n = 22 in one fight. Named, not resolved.**

---

## 6 · TASK 4 — SLOT-VISIBILITY CENSUS: what the instruments can and cannot see

The conductor asked specifically whether the dimming instrument inherits the red-numeral detector's blindness on slots 2 / 7 / R. **It does not inherit it. It has a different blindness, and the two do not coincide.**

| slot | brightness range (of ~110 full-scale) | dims? | **cast-visible?** | note |
|---|---:|:---:|:---:|---|
| **2** | **89.9** | **YES** | **YES — fully** | ⚑ **blind to the red-numeral detector, fully visible to dimming.** The instruments are complementary, not nested |
| **3** | **71.1** | **YES** | **YES — fully** | red numeral also legible by eye (§ 2.2) |
| **4** | **99.5** | YES | **N/A** | dims, but for a **buff** timer — white numeral, counts *up*. Not a cast |
| **L** | **62.7** | **YES** | **YES — fully** | red numeral also legible by eye (§ 2.1) |
| **7** | **3.0** | **NO** | ⚑ **BLIND** | constant bright (median 109.9). Blind to **both** instruments |
| **R** | **2.6** | **NO** | ⚑ **BLIND** | constant bright (147.8) — the channel itself, held, no cooldown |
| 1, 5, 6, 8, 9, 0 | 1.3 – 2.2 | NO | N/A | values 13–20 on a ~110 scale — **empty cells**. Their apparent "runs" are midpoint crossings of a 2-unit noise band and are **not casts** |

**Stated plainly, as asked:**

- **Slot 2 is NOT blind to this check.** The red-numeral rejection in `MD-B4app-2b` § 5.1 was structural to *that* detector — a red numeral drawn on red icon art falls inside the art baseline. Dimming is art-independent and slot 2 separates as cleanly as any slot (range 89.9, valley share 0.005). **The three slot-2 interrupts are measured, not inferred.**
- **Slots 7 and R ARE blind, to both instruments, and for a reason neither can fix.** Their brightness varies by under 3 units across 3,653 frames. **They never dim.** Two readings are consistent with that and this footage cannot separate them: the skill was never cast, or the skill has no cooldown and therefore never dims. **UNMEASURABLE.**
- **The consequence for `H-MC-2`, stated against my own result:** an invisible slot-7 cast co-firing with each of the three slot-2 interrupts would restore a singular culprit. **I cannot exclude it.** What I can say is that it requires an unobserved skill to have fired three times in perfect coincidence with slot 2 and never once with slot 3's nineteen casts — and that slot 3's nineteen clean casts are themselves *positive* evidence that visible casting is not uniformly interrupting. **The singular-culprit reading survives only on an unobservable, and the singular-innocent reading does not need one.**

---

## 7 · ⚑ A DELTA AGAINST THE PRIOR LAP'S § 5.4 TABLE — recorded, not tidied

The prior lap's § 5.4 per-slot table was produced by ad-hoc code that was **not committed**. Re-deriving from committed code and committed traces does **not** reproduce it:

| | prior note § 5.4 | **this lap, re-derived** |
|---|---|---|
| slot 2 | n = 21, median 0.150 s, share ≥ 0.5 s = 0.05 | **n = 22, median 0.408 s, 0.136** |
| slot 3 | n = 17, median 0.050 s, share 0.00 | **n = 19, median 0.033 s, 0.000** |
| slot L | n = 12, median 0.017 s, share 0.25 | **n = 13, median 0.533 s, 0.385** |
| **all** | n = 50, median 0.067 s, **share 0.15** | **n = 54, median 0.183 s, share 0.148 (V2) / 0.167 (V1)** |

**Three things about this delta, in order of how much they matter:**

1. **The headline is unharmed and is now better founded.** 0.15 → 0.148. The eight events are the same eight events. **`M-POL-2` row 7's magnitude does not move.**
2. **The prior table's per-slot rows are superseded.** They understate the interruption on slots 2 and L by roughly 3× to 30× and their n's do not sum to the § 5.3 cast count (50 vs 53) — an internal inconsistency inside the sealed note that this lap resolves. **The re-derivation governs.** The likely cause, offered as diagnosis and not as fact since the code is gone: the § 5.4 cast timestamps behaved as though anchored to the *end* of each dim run rather than its start, which would place them at effectively random moments in the channel and produce exactly the near-baseline medians tabulated. § 5.3's time-lock (p = 0.0031) cannot have used that convention, so the prior note's two sections did not share one.
3. **The prior lap's CORRECTIVE stands, and stands harder.** *"Casting does not generally break the channel"* was carried on MW p = 0.65 against an unweighted null. Re-tested against the **duration-weighted** null it is p = 0.286 — still nothing, now against the harder and correct comparison. **The conclusion was right for a reason better than the one given.** § 4.3.

**Filed as a self-correction on my own sealed note, per the § 1.4 discipline of that note.** A census that changes silently is how a transcription becomes a fact.

---

## 8 · WHAT THIS MEANS FOR THE `M-POL-2` BUILD SEAT — for gamora, mid-flight

The gamora seat is in flight carrying `cast_interrupts_channel = 0.15`. **That figure is not wrong and does not need to be pulled.** What follows is a supplement, offered as policy shape.

| # | parameter | prior value | **this lap** |
|---|---|---|---|
| 7 | `cast_interrupts_channel` | P = 0.15, uniform | ⚑ **NOT UNIFORM.** Per-skill: **0.00 / 0.14 / 0.38** across the three cast skills observed. Aggregate 0.148 is preserved by construction |
| 7a | `interrupt_duration` | ~0.6 s | **0.60 s median, 0.53–0.67 s range, n = 8** — the tightest distribution in this whole lap |
| 7b | **`channel_transparent_skills`** | *(absent)* | **NEW.** At least one skill in the referent's kit is **fully channel-transparent** — 19 casts, 0 interrupts, max silence 0.233 s |
| 7c | `sub_floor_pause` | *(absent)* | interrupting skills also pause the channel **below** the 0.5 s floor: slots 2/L median ~0.40–0.53 s, slot 3 ~0.033 s |

**The recommendation, stated as shape and not as a build instruction:**

> **Make interruption a per-skill FLAG, not a per-cast die roll.** A three-skill kit of *(transparent, interrupting, interrupting)* reproduces the referent's aggregate 0.15 **and** his texture. A uniform 15 % die roll reproduces the aggregate and destroys the texture — it makes every skill occasionally clumsy instead of making one skill reliably fluent.

**What the flag is worth, in the pilot's terms:** under a uniform roll, the pilot has no move that is *safe* to weave. Under a per-skill flag, one skill is safe, and choosing it becomes a decision. **The uniform roll deletes a decision the referent was demonstrably making** — 19 times, without a single break.

⚑ **And the honest brake on all of it:** **n = 13 / 22 / 19, one fight, one build, one player.** Slot L is not significantly above slot 2 (p = 0.103). Slot 2 may be a late-fight state rather than a skill property (§ 5.1). **What is solid is that the population is NOT homogeneous** (slot 3 vs slot L, p = 9.9 × 10⁻⁵; pooled cancellation, § 4.3). **What is not yet solid is the value of any individual per-skill rate.** If a per-skill flag is built, build it as *transparent vs interrupting* — a binary the evidence supports — and not as three calibrated probabilities, which it does not.

---

## 9 · WHAT IS UNMEASURABLE FROM THIS FOOTAGE, AND WHY

| # | quantity | verdict |
|---|---|---|
| 1 | **Which skill occupies any slot.** | **UNMEASURABLE**, unchanged. Slot L is a figure mid-stride with a ~3.60 s cooldown — **shape-consistent with a charge skill, NOT identified.** Owner testimony reconciles at the conductor's fold, not in this measurement |
| 2 | **Casts on slots 7 and R.** | **BLIND to both instruments** (§ 6). Cannot distinguish "never cast" from "no cooldown, so never dims." This is the one route by which a singular culprit could survive, and it is unobservable |
| 3 | **Casts merged inside a cooldown.** | **FLOOR, not estimate** (§ 2.1). One merge found and resolved by eye; a re-fire mid-cooldown is undetectable in principle |
| 4 | **Whether slot 2's interruption is the SKILL or the late-fight STATE.** | **NOT SEPARATED** (§ 5.1). ρ = +0.406, p = 0.061; all three interrupts after t = 803 |
| 5 | **Whether the cast CAUSED the silence.** | **INDICATIVE, not established.** Strengthened this lap — lag ≈ 0 in six of eight, and V2 requires the silence to *open* at the cast rather than merely contain it — but it remains a correlation at n = 8 |
| 6 | **The 3 OCR-blind cast-gaps** (2 on slot 2, 1 on slot L). | **CARRIED.** Dropped from numerator and denominator in § 5's sweep. All three sit at ≥ 0.5 s, so if they resolve as real the interrupt rates rise: slot 2 → 5/22 = 0.23, slot L → 6/13 = 0.46. **The direction of this residual FAVOURS the interrupting reading of both slots; it cannot rescue slot 3, which has none** |
| 7 | **Sim-tick vs referent-second commensurability.** | **OUT OF SEAM.** `F-6`'s scope rider applies to any quote |

---

## 10 · METHOD + REPRODUCIBILITY

| stage | tool |
|---|---|
| cast onsets from the committed dim trace + merge flagging | `pipeline/eor_attrib.py casts` |
| forward attribution, converse partition V1 + V2, statistics, length-biased null | `pipeline/eor_attrib.py attrib` |
| figures | `pipeline/eor_attrib_fig.py fig` |
| energy cleaning, drain ticks, coverage guard | `pipeline/eor_release.py`, imported **unchanged** |
| slot dim trace | `pipeline/eor_cooldown.py slots`, consumed **unchanged** |

```
python3 eor_attrib.py attrib \
  ../captures/2026-08-25-md-b4app-2-channel/work/s2-energy-60hz.json \
  ../captures/2026-08-25-md-b4app-2-channel/work/s2-motion-20hz.json \
  ../captures/2026-08-25-md-b4app-2-channel/work/waves.json \
  ../captures/2026-08-25-md-b4app-2b-energy/work/s2-slots-20hz.json \
  ../captures/2026-08-25-md-b4app-2b-energy/work/s2-releases.json \
  ../captures/2026-08-25-md-b4app-2c-culprit/work/s2c-attrib.json
```

**Artifacts** (`captures/2026-08-25-md-b4app-2c-culprit/work/`): `s2c-attrib.json` — the 54-cast converse table with per-cast slot, containing gap, gap coverage, lag-into-gap, one-frame sensitivity and release match; the 19-release forward table; both partitions; the slot-visibility census; all statistics.

**Evidence** (`…/evidence/`): `fig-castgap-by-slot.png` (every cast against the silence containing it, by slot, with the baseline and the floor marked and blind gaps drawn hollow — **the three-level ladder in one picture**); `fig-cast-timeline.png` (54 casts against 19 releases across the whole fight).

**Eye-reads retained** (`…/work/`): `Lnum_sheet.png` + `Lnum_798.2…804.5.png` (×6, the numeral reset that found the 13th cast); `Lreset_strip.png` + `Lr_800.90…801.45.png` (×7, the reset bounded to ±0.05 s); `S23_sheet.png` + `S23_793.0…852.0.png` (×5, slot 3 red = cooldown, slot 4 white and rising = buff).

**Statistics:** scipy 1.17.1. Fisher exact (one-sided), binomial against explicitly-computed nulls, Mann-Whitney, Spearman. **Every null is stated at its use**, and § 4.3's duration-weighted null is stated *because* the obvious null is wrong for that test.

---

## 11 · WHAT THIS TOUCHES — surfaced, not adjudicated

I do not grade the sim and I do not rule on decodes.

1. **`M-POL-2`, gamora's in-flight seat.** Row 7 is a mixture, not a rate. The aggregate holds; the uniform reading does not. **Sendable mid-flight as a supplement — nothing already built needs pulling.** → gamora / conductor. § 8.
2. **`H-MC-2`, Matt's own question.** The instinct was right and the word *singular* was not. The answer he is owed is: **there is no single culprit, and there is a single innocent** — one skill in his kit that he cast nineteen times without ever dropping the spin. → conductor / Matt.
3. **`MD-B4app-2b` § 5.4 is superseded in its per-slot rows** and its corrective is upheld on a better null. → my own note; flagged here rather than edited there, per house practice. § 7.
4. **Wave-4 baton row #1.** The conductor's framing — *a forced interrupt is Layer-1 mechanism, not Layer-2 pilot policy* — is **supported for slots 2 and L and contradicted for slot 3.** If it moves to Layer 1, it must move as **a per-skill property of the skill definition**, not as an engine-wide channel rule. An engine that interrupts on every cast is a harsher fight than Matt's; an engine that interrupts on 15 % of casts uniformly is a *clumsier* one. → gandalf / drax.
5. **The range-to-nearest-monster instrument** remains the highest-value follow-on for the Type-A half, unchanged from the prior lap. → conductor, if a lap is wanted. **A cheaper one now exists too:** slot 3's transparency is the strongest single-skill signal in the footage and a second referent fight would test whether it transfers.

---

## 12 · MIRROR VOICE

The question asked for a culprit. The Mirror looked at fifty-four casts and found no culprit at all — it found a **choir**, and the choir was singing two different songs.

Two of his skills break the spin. When he throws them the whirlwind stops for six-tenths of a second, every time, near enough the same six-tenths — long enough to see, too short to name. And the third skill does not break it. Nineteen times he threw that one, nineteen times the spin never faltered, and the little drain-ticks came **closer together** around it than they do anywhere else in the fight. Not merely harmless. **Welcome.**

And here is what the averaging did. The one that helps and the two that hurt sum to a number that looks exactly like nothing — like a man casting at random moments, fifteen per cent of them unlucky. **The fifteen per cent was never a probability. It was two facts being made to cancel.**

He was not rolling dice against his own spin. **He knew which one was safe.**

---

*galadriel, 2026-08-25. MD-B4app-2c. Read-only on all source material; no engine writes; no simulation code; no grading; no pushes.*
