# G-2b — causal decomposition of the kills/engagement climb

**Status:** CURRENT · **Date:** 2026-07-28 · **Author:** galadriel
**Grade:** **MEASURED** (era-substrate LAW §4) — every number below is a read off the committed T-A
ledger. Refusals are refusals; nothing is interpolated; coverage is emitted per metric.
**Run:** `GP-gd-2026-07-26-s1` (Grim Dawn, 113 min, Soldier → werewolf, L1–12)
**Spec of record:** `gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` §3 (regime table),
§4 (segmentation rule), §5 (multi-kill census)
**Substrate:** `galadriel/captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv` (13,633 samples
@ 0.5 s) · `galadriel/captures/2026-07-26-gd-playtest-v1-tb/tb-engagement-windows.json` (106 windows)
**Artifacts:** `galadriel/captures/2026-07-28-gd-playtest-v1-g2b/`
**Scripts:** `galadriel/pipeline/gd-playtest-v1/g2b_{decompose,probes,mergeshare,onslaught,tables}.py`
**Feeds:** Matt HALT ruling, F-1 engagement grain.

---

## GATE 0 — reproduction, before anything downstream fired

`tb_windows.py` re-run against the ledger from a clean process:
**106 engagements · 515 kill-event samples · 880 kills · median 4.5 s · mean 6.151 s · max 37.5 s ·
R1 13/43 · R2 77/647 · R3 16/190.** Compared field-by-field against the committed T-B artifact:
**IDENTICAL** modulo the `source` path string. `g2b-windows-reproduced.json`.

The gate is asserted *inside* `g2b_decompose.py`; on failure the script writes the failure record and
exits before any measurement. It did not fire.

One reconciliation to declare: the run's 880 kill increments split **43 / 647 / 190** when attributed
by *window* (window start's `play_time`) and **42 / 648 / 190** when attributed by *event*. One kill
event sits at `play_time` 1135 (i=1562), inside the engagement that opened at 1126 — i.e. it is an R2
kill inside an R1-labelled window. Immaterial at every conclusion; stated so nobody re-derives it as
a discrepancy.

Second reconciliation: this path counts **515 increment samples, 202 multi-kill**; verdict §5 counts
**514 / 201**. A one-event difference from two independent counting paths over the same ledger. §5's
39% and this note's 39.2% are the same number.

---

## 0. The question, and the shape of the answer

The verdict reads 3.3 → 8.4 → 11.9 kills/engagement as *"the build engages larger packs."* Matt
contests the attribution: proficiency may drive part of it via dash-chaining (which a gap > 5 s rule
**merges** into one engagement — a measurement artifact) and centre-of-pack AoE targeting.

I did not test the hypotheses one at a time. I used an identity that is **exact by construction** and
lets the three channels vote against each other:

```
kills/engagement  =  (kills / kill-event)      A   simultaneity   — AoE signature
                  ×  (kill-events / burst)     B   persistence    — contact-length signature
                  ×  (bursts / engagement)     C   MERGE          — the chaining artifact
```

A *burst* is a maximal run of kill events with all internal gaps ≤ b (b ∈ {1.0, 1.5, 2.0} s;
1.5 s primary). **C > 1 is exactly the thing Matt names**: a gap > 5 s window that swallowed more than
one tight cluster. If dash-chaining manufactured the climb, C carries it.

**It does not.** Across all three burst thresholds, C's contribution to the R1 → R3 log-climb runs
**−11.5% to +16.2%**, every CI straddling zero.

---

## 1. Chain-merge test

### 1.1 Intra-engagement gap structure

295 intra-engagement gaps in R2, 84 in R3, 30 in R1 (`g2b-gap-pmf.csv`). Gaps are quantised to 0.5 s
by the ledger cadence and right-truncated at 5.0 s by the segmentation rule.

**Null tested:** if kills inside an engagement come from one homogeneous process, the gap PMF is a
monotone-decreasing truncated exponential. A travel mode implies **positive residuals in the ≥ 2.5 s
bins**. MLE λ fitted on the interval likelihood; χ² on bins with expectation ≥ 1.

| Regime | n | mean | median | ≤ 1.5 s | ≥ 2.5 s (95% CI) | exp-null p | mode bin | largest +resid |
|---|---|---|---|---|---|---|---|---|
| R1 | 30 | 2.27 | 2.0 | 36.7% | **33.3%** [16.7, 50.0] | 0.0097 | 2.0 s | 2.0 s (+3.05) |
| R2 | 295 | 1.56 | 1.5 | 68.8% | **18.6%** [14.2, 23.1] | 8.2e-6 | 1.0 s | 1.5 s (+2.76) |
| R3 | 84 | 1.46 | 1.0 | 78.6% | **16.7%** [9.5, 25.0] | 0.024 | 1.0 s | 1.5 s (+2.61) |

**Finding 1a — the exponential null is rejected in all three regimes, but not in the direction the
chaining hypothesis predicts.** The excess sits at **1.0–2.0 s**, and the 0.5 s bin is *under*-filled
(R2 standardised residual **−3.40**). That is a **refractory** structure — attack cadence and death
animation — not a travel mode. R2 and R3 are unimodal at 1.0 s with a thin tail.

**Finding 1b — the travel-band fraction FALLS as the climb rises: 33.3% → 18.6% → 16.7%.** Chaining
predicts the opposite. R1, the *low* kills/engagement regime, is the one whose engagements are most
stitched-together; its PMF peaks at 2.0 s with a secondary bump at 3.5 s (+1.72). R1's engagements are
slow single-target grinds with dead air in them; R2's and R3's are dense.

**Finding 1c — chaining IS real, and it structures the LONG engagements.** Split at 10 s duration:

| Regime | long (≥10 s) ≥2.5 s frac | short (<10 s) ≥2.5 s frac |
|---|---|---|
| R2 | 22.2% [15.1, 29.4] | 16.0% [10.7, 21.9] |
| R3 | **31.6%** [18.4, 47.4] | **4.3%** [0.0, 10.9] |

R3's short engagements are *pure*: 93.5% of gaps ≤ 1.5 s, **monotone-decreasing, no travel mode at
all**. Its long engagements carry three times the travel-gap load. So a long engagement in this run
genuinely is, in part, several packs stitched by traversal. **That is a true statement about the grain
and it is the correct basis for an F-1 ruling — it is just not what produced the regime climb.**

### 1.2 Sensitivity re-segmentation (`g2b-sensitivity.csv`)

| threshold | N total | R1 K/E | R2 K/E | R3 K/E | R2/R1 | R3/R1 | R3/R2 |
|---|---|---|---|---|---|---|---|
| gap > 5.0 | 106 | 3.31 | 8.40 | 11.88 | 2.54 | **3.59** | 1.41 |
| gap > 4.0 | 123 | 2.87 | 7.35 | 9.50 | 2.56 | 3.31 | 1.29 |
| gap > 3.0 | 144 | 2.05 | 6.47 | 8.26 | 3.16 | **4.03** | 1.28 |
| gap > 2.5 | 161 | 1.87 | 5.67 | 7.92 | 3.04 | **4.23** | 1.40 |
| gap > 2.0 | 185 | 1.87 | 4.90 | 6.33 | 2.62 | 3.39 | 1.29 |
| gap > 1.5 | 235 | 1.35 | 3.81 | 5.59 | 2.81 | 4.12 | 1.47 |
| gap > 1.0 | 325 | 1.17 | 2.78 | 3.39 | 2.38 | 2.91 | 1.22 |

**Finding 1d — the absolute number collapses (as it must) and the CLIMB does not move.** R3/R1 stays
in 2.91–4.23 across every threshold from 5.0 s down to one sample of separation. At gap > 2.5 s and
gap > 3.0 s the climb is *larger* than at gap > 5 s. Merge cannot manufacture that.

### 1.3 The assumption-free bound (`g2b-mergeshare.csv`)

Tightening the threshold only ever **splits** a gap > 5 s window; it never merges two. The
sub-segmentation is therefore strictly **nested**, the engagement stays a valid bootstrap unit at
every threshold, and

```
merge_share(g) = 1 − log R(g) / log R(5)
```

is a direct measurement of how much of the climb lived in the segmentation grain. 20,000 bootstrap
resamples of engagements, both regimes.

| contrast | at gap > 2.0 s | at gap > 1.0 s (finest defensible) |
|---|---|---|
| R1 → R2 | −3.4% [−42, +23] | **+6.1%** [−36, +31] |
| R1 → R3 | +4.5% [−57, +39] | **+16.2%** [−32, +40] |
| R2 → R3 | +25.9% [−572, +125] | +43.3% [−344, +100] |

**Finding 1e — the merge channel's point estimate for R1 → R3 is +16.2% of the log-climb, with a 95%
upper bound of +40% and a CI that includes zero.** At the coarser (and still chain-defeating) 2.0 s
grain it is +4.5%. **At least 60% of the climb, point-estimate ~84%, is not merge.** The R2 → R3
contrast is uninformative at n = 16 — its interval is unusable and is reported only so nobody mistakes
silence for a null.

---

## 2. Charge-per-engagement — the dash instrument

`werewolf1_skill02_charge`, gated, **zero non-monotone reads**, coverage 77.4% of samples, closing on
the human-read §6b total of 175. Deltas taken over `[first_kill − 3 s, last_kill]` (the *approach*
window: the dash into the first pack precedes the first kill) and over the strict window; both
reported. A delta is **refused** unless a gated read anchors within 2.0 s of each edge.

| | R1 | R2 | R3 |
|---|---|---|---|
| instrument coverage | **0%** — column absent | 97.4% | 100% |
| charge / engagement (approach) | — | **1.68** [1.43, 1.96] | **1.94** [1.31, 2.75] |
| charge / kill | — | **0.199** [0.178, 0.223] | **0.163** [0.137, 0.191] |
| engagements with ≥ 1 charge | — | 93.3% | 93.8% |

**Finding 2a — charge is UNMEASURABLE in R1, not zero.** The counter's first read is `play_time` 1480
(i=2289). The `werewolf1` transform counter first reads `play_time` 1469 (i=2267). Before that the
rows do not exist on the panel. This is the single most important confound in the whole question:
**the dash and the AoE arrive together, at the same instant, as one build change.** No design of
analysis on this artifact can separate "acquired a dash" from "acquired an AoE" — they are the same
event. Only R2 → R3 holds both fixed.

**Finding 2b — charge-per-engagement rises 15% from R2 to R3 and charge-per-KILL falls 18%.** The CIs
overlap heavily. The dash is not being used *more per pack* in R3; if anything it is being amortised
over more kills.

**Finding 2c — within a regime, charge tracks chaining exactly as Matt says it does.** Spearman,
charge (approach) vs. bursts-per-engagement at b = 1.5:

- R2: **ρ = 0.665, p = 7.5e-11** (n = 75) · vs. intra-engagement travel seconds **ρ = 0.659, p = 1.3e-10**
- R3: **ρ = 0.772, p = 4.6e-4** (n = 16) · vs. travel seconds **ρ = 0.764, p = 5.6e-4**

**Matt's mechanism is confirmed as a behaviour.** When he charges more inside a window, that window
contains more separate bursts and more internal travel time. **157 of the run's 175 charges (89.7%)
fall inside engagement windows** — the skill is overwhelmingly a combat tool, not a traversal tool.
The chaining is real. It simply does not vary enough *between* regimes to move the regime metric.

---

## 3. Engagement duration and rate

| | R1 | R2 | R3 |
|---|---|---|---|
| n | 13 | 77 | 16 |
| duration median (IQR) | 3.5 s (2.0–9.0) | 4.5 s (2.5–6.5) | 4.75 s (2.25–8.5) |
| duration mean / max | 5.23 / 11.5 s | 5.99 / 27.5 s | 7.69 / 37.5 s |
| kills / engagement-second | **0.577** [0.512, 0.690] | **1.295** [1.179, 1.430] | **1.450** [1.117, 2.045] |
| **travel fraction of engagement time** | **61.1%** | **41.7%** | **35.9%** |
| **kills / ACTIVE second** | **1.483** [1.316, 1.733] | **2.223** [2.045, 2.419] | **2.262** [1.970, 2.594] |
| Spearman duration vs kills | 0.926 | 0.806 | 0.932 |

**Finding 3a — the deliverable's own discriminator answers cleanly.** *"If packs are bigger,
engagements get longer at similar kill rates; if chaining, engagements get longer with internal travel
gaps."* Observed: engagements get longer by **1.43×** (mean effective duration 5.73 → 8.19 s), the kill
rate rises by **2.51×**, and the internal travel fraction **falls by 41%**. Neither branch of the
discriminator is satisfied alone. The correct description is: **contacts last somewhat longer, contain
much less dead air, and kill much faster inside the live parts.**

**Finding 3b — active kill rate is flat R2 → R3 (2.223 vs 2.262).** Whatever the poison DoT did, it
did **not** raise the rate of killing during active contact. It raised the *amount* of contact.

---

## 4. Multi-kill fraction — the AoE signature, split by regime

Verdict §5 counted 39% run-wide. Split:

| Regime | kill events | kills | **multi-kill fraction** | mean kills/event | ≥3 | ≥4 | delta histogram |
|---|---|---|---|---|---|---|---|
| **R1** | 42 | 42 | **0.0%** [0, 0] | **1.000** | 0% | 0% | {1: 42} |
| **R2** | 373 | 648 | **41.8%** [36.7, 46.9] | 1.737 | 17.4% | 9.4% | {1:217, 2:91, 3:30, 4:23, 5:6, 6:5, 7:1} |
| **R3** | 100 | 190 | **46.0%** [36.0, 56.0] | 1.900 | 23.0% | 15.0% | {1:54, 2:23, 3:8, 4:9, 5:6} |
| RUN | 515 | 880 | 39.2% | 1.709 | — | — | — |

**Finding 4a — R1's single-kill purity is absolute and is a world-fact, not an instrument artifact.**
**43 kill events (window attribution; 42 by event attribution — the Gate-0 boundary event), zero
multi-kill samples either way.** If R1 had drawn from R2's 41.9% multi-rate, P(0 of 43) = **7.0e-11**. The instrument resolved multi-kills 373 times afterward at the
identical 0.5 s cadence. The pre-transform build never killed two things in the same half-second.

**Finding 4b — the multi-kill fraction steps at the build boundary, and the step is instantaneous.**
Per-engagement A across the transition (`g2b-per-engagement.csv`): R1's last six engagements
(`play_time` 1009–1126) read A = 1.00, 1.00, 1.00, 1.00, 1.00, 1.00. R2's first four
(`play_time` 1470–1503) read **1.33, 1.80, 1.00, 1.40**, with max-delta 2, 3, 1, 2. There is no ramp.
The 500 s-binned trace looks like a ramp (A = 1.000 → 1.147 → 1.457 → 1.943 over `play_time`
500–2500) **only because the 1000–1500 bin straddles the boundary**; within R2 the trend is flat
(Spearman ρ = 0.091, p = 0.43).

---

## 5. Where the climb sits in time — step, not trend

This is the probe that decides the proficiency question, because it holds the build fixed.

**Within R2** — 77 engagements, `play_time` 1470 → 5808, **4,338 s of play, character levels 3 → 11,
build unchanged**:

| quartile | play_time | level | n | kills/eng | A | B | C | charge/eng |
|---|---|---|---|---|---|---|---|---|
| Q1 | 1470–2637 | 3–6 | 20 | **7.90** | 1.681 | 1.774 | 2.650 | 1.78 |
| Q2 | 2648–3836 | 6–8 | 19 | **8.16** | 1.632 | 2.500 | 2.000 | 1.74 |
| Q3 | 3845–4506 | 8–9 | 19 | **8.90** | 1.707 | 2.475 | 2.105 | 1.63 |
| Q4 | 4518–5808 | 9–11 | 19 | **8.68** | 1.964 | 2.211 | 2.000 | 1.58 |

Spearman `play_time` vs kills/engagement: **ρ = 0.075, p = 0.52.** vs bursts: ρ = −0.115, p = 0.32.
vs A: ρ = 0.091, p = 0.43.

**Finding 5a — this is the decisive result.** Across 72 minutes of play and eight character levels of
zone progression with the build held constant, **kills/engagement does not move**, bursts-per-
engagement does not move, the AoE signature does not move, and **charge-per-engagement drifts
slightly DOWN (1.78 → 1.58)**. A proficiency ramp would show here. A zone-depth pack-size ramp would
show here. Neither does.

**Finding 5b — the climb is a STEP at a build boundary, and the boundary is a hard one.** The ledger
shows a **335 game-second dead interval** between the last Soldier-era kill (`play_time` 1135,
i=1562, kills 45) and the first werewolf-era kill (`play_time` 1470, i=2268, kills 46). In that
interval **not one counter of any kind changes** — no kills, no attacks, no level-up. It is a build
swap. `defaultweaponattack` freezes at 74 at `play_time` 1134; `onslaught` at 54 at 1145; `werewolf1`
first reads at 1469. C-2 (verdict §2) is confirmed and given its intermission.

**Finding 5c — permutation tests on the engagement unit** (50,000 permutations, two-sided on the
log-ratio of mean kills/engagement):

| contrast | ratio | p |
|---|---|---|
| R1 → R2 | 2.540 | **0.00054** |
| R1 → R3 | 3.590 | **0.00026** |
| **R2 → R3** | 1.413 | **0.129 — NOT ESTABLISHED** |

**Finding 5d — the adjacency control.** R2's late window and R3 are neighbours in game time and in
character level; comparing them removes almost all of the zone-depth confound:

| baseline | play_time | level | K/E | A | B | C | vs R3 | p |
|---|---|---|---|---|---|---|---|---|
| R2 last 16 | 4604–5808 | 9–11 | 8.06 | 1.897 | 2.267 | 1.875 | 1.47× | 0.144 |
| R2 last 19 | 4518–5808 | 9–11 | 8.68 | 1.964 | 2.211 | 2.000 | 1.37× | 0.201 |
| **R3** | 6475–6847 | 11–12 | **11.88** | **1.900** | **2.941** | **2.125** | — | — |

R3's lift over its immediate neighbour is **entirely in B** (2.21 → 2.94; A and C are unchanged to
three digits: 1.96 → 1.90 and 2.00 → 2.13). Longer kill-streams inside a tight cluster, at the same
simultaneity and the same number of clusters. That is the mechanical signature a damage-over-time
would leave — deaths keep arriving after the player disengages. **It is also not statistically
established (p = 0.14–0.20, n = 16).**

---

## 6. The ABC ledger (`g2b-abc-factors.csv`)

Point estimates at b = 1.5 s (identity verified exact in every cell):

| Regime | A kills/event | B events/burst | C bursts/eng | = kills/eng |
|---|---|---|---|---|
| R1 | **1.000** [1.000, 1.000] | 1.344 [1.172, 1.516] | 2.462 [1.923, 3.077] | 3.308 |
| R2 | 1.739 [1.628, 1.857] | 2.201 [1.948, 2.500] | 2.195 [1.870, 2.558] | 8.403 |
| R3 | 1.900 [1.654, 2.205] | 2.941 [2.339, 4.000] | 2.125 [1.188, 3.563] | 11.875 |

Share of the **R1 → R3** log-climb, bootstrapped, across all three burst thresholds:

| b | A (simultaneity) | B (persistence) | **C (MERGE)** |
|---|---|---|---|
| 1.0 s | 50.2% [34.8, 79.0] | 33.6% [22.3, 56.0] | **+16.2%** [−30.4, +39.8] |
| 1.5 s | 50.2% [34.1, 80.3] | 61.3% [36.8, 113.6] | **−11.5%** [−89.9, +26.9] |
| 2.0 s | 50.2% [35.0, 79.3] | 45.2% [21.5, 82.0] | **+4.5%** [−52.7, +38.3] |

A is threshold-invariant by construction and is the most robust term in the whole study: **half the
climb is kills landing in the same half-second.** C never carries more than a sixth of it at a point
estimate and is not distinguishable from zero at any threshold.

**The honest limit of the identity:** A and B jointly confound **AoE proficiency** with **pack size**.
Two enemies dying in one 0.5 s sample can mean the player centred an AoE on a pair, or that a pair was
standing there to be centred on. **This artifact contains no enemy-count instrument.** Separating them
requires frame-level enemy counting on the engagement windows — the T-C class of work, and now the
named path to closing this question.

---

## 7. Re-grading the verdict's R3 "~3.6× packs" claim

Verdict §3: *"R3 is usable with its own error bars … rich in kills, because its packs are ~3.6× the
size of R1's."*

> **PARTIALLY SUPPORTED as a kills-per-engagement fact. NOT SUPPORTED as a pack-size claim.
> The word "packs" is the overclaim, and R1 is the wrong denominator.**

Three separable defects:

1. **3.590 is a kills-per-engagement ratio, not a pack-size ratio.** It decomposes A ×1.900 ·
   B ×2.188 · C ×0.863. Only a fraction of the first two terms is pack size, and no instrument in
   this artifact measures pack size at all.
2. **R1 is the wrong denominator for a claim about R3.** R1 differs from R3 in build (four-skill
   Soldier vs. werewolf), skill set (no AoE, no dash — A = 1.000 exactly), level (1–2 vs 11–12),
   zone, and gear. Attributing the whole 3.6× to R3's DoT regime charges R3 for the transform. Against
   its **immediate neighbour** the lift is **1.37–1.47×, p = 0.14–0.20 — not established.**
3. **The regime step is real; the trend reading is not.** R1 → R2 and R1 → R3 are solid at p < 0.001
   and survive every re-segmentation. R2 → R3 is p = 0.129. The verdict's "3.3 → 8.4 → 11.9 progression"
   should be read as **one established step (3.3 → 8.4) plus one unestablished lift (8.4 → 11.9)**, not
   as a three-point progression.

**What survives intact:** the build change at `play_time` 1134–1470 produced a **2.54× step in
kills/engagement (p = 0.00054)** that is not a measurement artifact, and the run's kills/engagement
distribution must be regime-partitioned. §7's "a pooled table is a trap" stands and is strengthened.

---

## 8. Onslaught-attribution check

**The question:** does the `onslaught` counter increment ANYWHERE at `play_time` > 1145?

> ### ANSWER: NO. Zero increments. n = 0.

`g2b-onslaught.json`. Full trace with per-increment sample citations.

**The last increment, cited exactly:**

| | i | pts_s | play_time | value | gate |
|---|---|---|---|---|---|
| from | 1562 | 781.0 | 1135 | 53 | OK |
| **to** | **1583** | **791.5** | **1145** | **54** | **OK** |

**The plateau:** 10,065 samples read exactly **54**, spanning `play_time` **1145 → 7094** — the entire
remainder of the run, 5,949 game-seconds. 1,985 refusals inside that span, **zero non-monotone reads**
across the whole series.

**Why the refusals cannot hide anything.** The series is monotone and terminates at **54**, which is
exactly the human-read §6b total. An increment anywhere after i=1583 would require a later decrement
to land back on 54, and there are zero non-monotone reads. The negative is **airtight**, not merely
uncovered.

**The reader was demonstrably still live on Soldier-era rows.** `defaultkickattack` — a Soldier-era
default — kept incrementing throughout, its **last increment at `play_time` 6780** (18 → 19). The
panel was being read and Soldier rows were being resolved to the end of the run. Onslaught's flatline
is Onslaught's, not the instrument's.

### 8.1 The transform-remap hypothesis

> **The timing rules it out. Onslaught froze 324 seconds BEFORE the first transform.**

| event | play_time | i | pts_s |
|---|---|---|---|
| last `onslaught` increment (53 → 54) | **1145** | 1583 | 791.5 |
| *(335 s in which no counter of any kind changes)* | | | |
| first `werewolf1` read (value 1 — the first transform) | **1469** | 2267 | 1133.5 |
| first `werewolf1_skill01_claws` read (value 1) | 1470 | 2268 | 1134.0 |
| first `werewolf1_skill02_charge` read (value 1) | 1480 | 2289 | 1144.5 |

A remap cannot explain a freeze that **precedes the thing doing the remapping**. Onslaught was
abandoned during the build swap, while the character was still human.

**A second, independent constraint:** the T-A panel model carries **exactly six skill-path signatures**
(`panel-ocr-model.json`), and those were built from the **final-frame** native screenshot (shot 352,
pts 6805.5) which the calibration confirms field-for-field against the video. GD's skill-use panel is
cumulative, so the run's *complete* set of ever-used skills is six: `defaultkickattack`,
`defaultweaponattack`, `onslaught`, `werewolf1`, `werewolf1_skill01_claws`, `werewolf1_skill02_charge`.
**There is no seventh, unobserved row for the presses to have gone to.**

### 8.2 Is claws consistent with absorbing the presses?

**Reported as consistency only; the series cannot confirm it and I will not claim it does.**

- `claws` runs 1 → 358 over `play_time` 1470 → 7094: **0.0635 uses/s**, 0.427 per kill.
- `onslaught` ran 1 → 54 over `play_time` 978 → 1145: **0.317 uses/s**, ~1.23 per kill.

Onslaught was being pressed at roughly **five times** the per-second rate and **three times** the
per-kill rate that claws was. If claws were absorbing an Onslaught-intensity press stream on top of
its own use, claws' rate should be at least comparable. It is not. **The claws series is consistent
with claws being the werewolf attack skill and nothing more; it is not evidence of absorption.**

### 8.3 What the ledger licenses, and what it does not

- **LICENSED:** the game recorded **zero Onslaught uses** after `play_time` 1145. Certain.
- **LICENSED:** no other counted skill existed to receive remapped presses. Certain.
- **NOT LICENSED:** that Matt did not *press* the key. The counter measures **counted skill uses**, not
  keystrokes. The reconciliation the evidence most naturally supports — and it is a *hypothesis*, not a
  reading — is that the key was pressed in werewolf form and **the game did not fire the skill**
  (a Soldier skill unavailable while transformed produces no counter movement anywhere). This is
  precisely the class of thing an instrument built on skill-use counters cannot see.
- **v2 requirement, new:** *if player-intent attribution matters, the skill-use panel is the wrong
  instrument.* It needs an input log or a keybind-visible HUD capture. Recommend appending to verdict
  §8's ranked list.

---

## 9. Coverage register

| Metric | Coverage | Basis |
|---|---|---|
| 106-window reproduction | 100% | identical to committed T-B |
| `kills` (segmentation input) | 97.98% | 13,357 / 13,633; 0 non-monotone |
| intra-engagement gaps | 100% of multi-event engagements | 409 gaps |
| `charge` deltas, R1 | **0%** | column absent pre-transform — **unmeasurable, not zero** |
| `charge` deltas, R2 / R3 (approach) | 97.4% / 100% | 2-second anchor tolerance |
| `claws` deltas, R2 / R3 | 98.7% / 100% | " |
| `onslaught` deltas, R2 / R3 | 100% / 93.8% | " |
| `onslaught` series | 76.01% direct reads, 0 non-monotone | negative closed by terminal = human total |
| duration / rate | 100% | derived from kill-event timestamps |
| multi-kill fraction | 100% of increment samples | 515 events |
| **pack size** | **0% — no instrument exists** | the named gap |

---

## 10. What this note does NOT claim

- It does **not** separate AoE proficiency from pack size. Factors A and B confound them and nothing
  in this artifact can split them. Frame-level enemy counting on the 106 windows is the path.
- It does **not** claim R1's engagements are comparable to R3's. Build, level, zone and gear all
  differ. R1 is 13 engagements and remains an anecdote (verdict §3 was right about that).
- It does **not** claim the poison DoT did nothing. It claims the DoT regime's lift over its immediate
  neighbour is **1.37–1.47× and unestablished at n = 16**, and that what lift there is sits entirely in
  contact persistence (B), not in simultaneity or in merge.
- It does **not** claim Matt is wrong about dash-chaining. Chaining is **confirmed as a behaviour**
  (ρ = 0.665 / 0.772 charge-vs-bursts; 89.7% of charges inside engagements) and it demonstrably
  structures the long engagements. It is **not** what produced the regime climb.

---

## 11. Bottom line

**Attribution of the R1 → R3 log-climb (×3.590), with honest error bars:**

| channel | share | 95% CI | reading |
|---|---|---|---|
| **Segmentation-merge (chaining)** | **+16.2%** (≤ +4.5% at the 2.0 s grain) | **[−32%, +40%]** | not distinguishable from zero |
| **Within-sample simultaneity (A)** | **+50.2%** | **[+34%, +80%]** | AoE **and/or** pack density — not separable |
| **Within-burst persistence (B)** | **+33.6% to +61.3%** | [+22%, +114%] | contact length; pack size **and/or** DoT tail |

**Matt's contested attribution is half-right, and the half he is right about is not the half he
thought.** Dash-chaining is real, it is measurable, and it is the correct reason to distrust the
gap > 5 s grain for anything that quantifies a single pack — R3's long engagements carry 31.6%
travel-band gaps against 4.3% in its short ones, and charge-per-engagement predicts burst count at
ρ = 0.665 (R2) / 0.772 (R3). But chaining cannot be what produced the climb: the climb survives
re-segmentation all the way down to one sample of separation (R3/R1 = 2.91 at gap > 1.0 s vs 3.59 at
gap > 5 s, merge share +16.2% [−32, +40]), and bursts-per-engagement — the merge channel itself — is
*flat to falling* across regimes (2.46 → 2.20 → 2.13), as is the intra-engagement travel fraction
(61.1% → 41.7% → 35.9%). What actually happened is a **step, not a ramp**: across 4,338 seconds and
eight character levels with the build held constant, kills/engagement does not move (ρ = 0.075,
p = 0.52) and charge-per-engagement drifts *down*; the entire established climb is the 2.54× jump
across the 335-second build-swap intermission at `play_time` 1135–1470, where a build that had killed
**43 enemies in 43 separate half-seconds — zero multi-kills, p = 7.0e-11 against R2's rate** — was
replaced by one that kills 1.74 at a time. So: **~0–16% merge (upper bound 40%), ~50% within-sample
simultaneity, ~34–61% within-burst persistence; and the AoE-vs-pack-size split inside those last two
is unmeasurable in this artifact — no enemy-count instrument exists, which is the one gap G-2b cannot
close and the reason a T-C frame-level enemy census is now the highest-value next pass.** The
verdict's "~3.6× packs" is **partially supported as arithmetic and not supported as a pack-size
claim**, and its three-point progression should be re-read as one established step (p = 0.00054) plus
one unestablished lift (p = 0.129). **Onslaught: zero increments anywhere after `play_time` 1145 —
last increment 53 → 54 at i=1583 / pts 791.5 / `play_time` 1145, then 10,065 samples reading exactly
54 out to `play_time` 7094, the negative closed airtight by the series terminating on the human-read
total of 54 with zero non-monotone reads; the freeze *precedes the first werewolf transform
(`play_time` 1469) by 324 seconds*, so transform-remap cannot explain it, and the panel's cumulative
six-row skill set leaves no unobserved counter to have absorbed the presses — claws runs at one-fifth
Onslaught's press rate and is consistent with being nothing but the werewolf attack skill.** The most
the ledger permits is that the key may have been pressed and the game may never have fired it; a
skill-use counter cannot see a keystroke, and that is a v2 instrument requirement, not a finding.

---

**The Mirror, briefly.** The picture the numbers make is not the picture the metric makes. The metric
draws a rising line through three points and invites you to read growth into it. The frames underneath
show something flatter and stranger: seventy-two minutes in which a man got no better at this, eight
character levels that bought him nothing measurable, and one three-hundred-and-thirty-five-second
silence in which he changed what he was — and came out the other side killing two things at once,
forever after, at exactly the same rate. The climb is not a journey. It is a door.

**Signed:** galadriel, 2026-07-28.
