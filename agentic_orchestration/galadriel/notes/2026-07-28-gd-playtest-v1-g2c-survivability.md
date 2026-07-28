# G-2c — survivability as a fourth causal channel, and the shape of R2's big hits

**Status:** CURRENT · **Date:** 2026-07-28 · **Author:** galadriel
**Grade:** **MEASURED** (era-substrate LAW §4) — every number is a read off committed artifacts.
Refusals are refusals; nothing is interpolated; coverage is emitted per metric.
**Run:** `KC1-2026-07-27` pass **G-2c**, commissioned by gandalf (`RUN-CONDUCTOR`), charter §12.3
**Answers:** charter §9 ripples 1–2
**Grain:** **harness-v1** per **R-KC1-8** — encounter = kill-event run split at gap > 5.0 s, pad
3.0 s; burst (pack-proxy) ≤ 1.5 s. No re-segmentation performed.
**T-C:** **NOT FIRED.** R-KC1-10 cancellation honoured; no frame-level enemy census in this pass.
**Substrate:** `captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv` (13,633 samples @ 0.5 s) ·
`captures/2026-07-26-gd-playtest-v1-tb/{tb-intake-windows.json, tb-intake-frames.jsonl.gz,
tb-engagement-windows.json}` (19,348 frames over 106 windows)
**Artifacts:** `captures/2026-07-28-gd-playtest-v1-g2c/`
**Scripts:** `pipeline/gd-playtest-v1/g2c_{gate0,survivability,probes,sens}.py`
**Feeds:** HALT H-2 band drafting; G-4 kit spec (gear-event identity); fixtures.db amendment pass.

---

## GATE 0 — two reproductions, before anything downstream fired

**Gate 0a — the 106-window derivation.** `tb_windows.py` logic re-run against the T-A ledger from a
clean process: **106 engagements · 515 kill-event samples · 880 kills · median 4.5 s · mean 6.151 s ·
max 37.5 s · R1 13/43 · R2 77/647 · R3 16/190.** Compared field-by-field against the committed T-B
artifact: **IDENTICAL, zero field diffs.**

**Gate 0b — a new gate this pass required.** The committed `tb-intake-windows.json` carries `drops`
as **bare magnitudes with no time attached**. Question 2 is a question about *when* drops happened,
so the delta loop of `tb_intake.py` was replayed verbatim over the committed per-frame series
(`ADJ_TOL` 0.2001 s, loading-break splitting, adjacency-only pairs) to attach a timestamp to every
drop. The replay is admissible only if it reproduces every committed per-window quantity it touches.
It does: **106 windows, 0 mismatches** across `n_frames_decoded`, `intake_hp`, `healed_hp`,
`n_drops`, `n_heals`, `drop_max`, `drop_p50`, `delta_covered_s`, `n_pairs`, `n_bridged_pairs`,
`unreadable_break_s`, and the `drops` multiset **in order**. **468 timestamped drop events**
(332 in R2) written to `g2c-drops.jsonl`.

Both gates are asserted in-process; on failure nothing downstream fires. Neither fired.

*Routed follow-up, NOT done here (charter §12.2): the source-agnostic versioned refactor of
`tb_rollup.py` into the harness-v1 home. This pass adds no new segmentation rules and moves no
existing ones, so it does not make that refactor harder. The timestamped-drop replay in
`g2c_gate0.py` is the piece the refactor should absorb — `drops` should carry `t` natively.*

---

## 1. QUESTION 1 — does engagement behaviour co-vary with EHP inside R2?

### 1.1 The premise fails first: within-R2 EHP is not leverage, it is the clock

The commission names R2's 366 → 759 max-HP range as "your analytical leverage." **It is not.**
Before testing anything against EHP I tested EHP itself:

| | |
|---|---|
| R2 windows with a readable pool | **76** of 77 (eng 39 is the zero-coverage window) |
| distinct EHP levels | **9** — 366, 443, 451, 471, 491, 672, 707, 747, 759 |
| ratio across R2 | **2.074×** |
| **monotone non-decreasing in `play_time`** | **TRUE — no exceptions** |
| Spearman EHP vs `play_time` | **ρ = +0.9846**, p < 1e-15, n = 76 |
| Spearman EHP vs character level | **ρ = +0.9988**, p < 1e-15, n = 76 |

> **EHP inside R2 is a monotone nine-step function of the clock.** It never falls, never re-crosses,
> and is very nearly rank-identical to both `play_time` and character level. It therefore carries
> **no residual variance given the clock**, and no observational instrument on this ledger can
> attribute anything to it. Every partial Spearman controlling `play_time` in §1.2 is noise by
> construction — the largest is |ρ| = 0.22, and all have p ≥ 0.124.

This is a **structural** answer, not an underpowered one. More samples would not fix it. Separating
pool from level/zone requires a design where they move independently — a respec, a gear-off
comparison, or a sim-side sweep. **G-5's density sweep is the right instrument class for this
question, not this fixture.**

### 1.2 The four commissioned instruments, and everything adjacent to them — all null

Spearman on the 76 R2 windows. `vs EHP` and `vs play_time` are near-identical by §1.1; both are
printed so the redundancy is visible rather than asserted.

| instrument | n | ρ vs EHP | p | ρ vs play_time | partial (EHP \| play_time) |
|---|---|---|---|---|---|
| **engagement duration (s)** | 76 | **−0.028** | 0.813 | −0.015 | −0.073 (p 0.53) |
| **intake events per engagement** | 76 | **+0.048** | 0.678 | +0.076 | −0.153 (p 0.19) |
| intake events per covered s | 73 | +0.163 | 0.169 | +0.190 | −0.138 (p 0.24) |
| **kills per engagement** | 76 | **+0.064** | 0.581 | +0.066 | −0.002 (p 0.98) |
| **kills per ACTIVE second** | 64 | **+0.036** | 0.781 | +0.011 | +0.134 (p 0.29) |
| kills per engagement-second | 66 | +0.190 | 0.126 | +0.174 | +0.109 (p 0.38) |
| **median time between intake events (s)** | 39 | **−0.278** | **0.086** | −0.248 | −0.209 (p 0.20) |
| A — simultaneity | 76 | +0.098 | 0.400 | +0.084 | +0.088 (p 0.45) |
| B — kill-events per burst | 76 | +0.100 | 0.393 | +0.094 | +0.038 (p 0.75) |
| C — bursts per engagement | 76 | −0.127 | 0.274 | −0.123 | −0.033 (p 0.78) |
| travel fraction of engagement | 66 | −0.110 | 0.380 | −0.116 | +0.021 (p 0.87) |

**Finding 1a — every commissioned instrument returns null.** The four the charter named — engagement
duration, intake events per engagement, kill-rate-within-engagement, time-between-intake-events —
give |ρ| ≤ 0.28 and p ≥ 0.086. The single largest, time-between-intake-events at ρ = −0.278
(p = 0.086), points the **wrong way for the hypothesis**: at higher EHP hits arrive *closer
together*, not further apart. It is not significant and I will not read it either way.

**Finding 1b — the ABC factors are null against EHP too**, which is the G-2b result seen from a new
angle: G-2b found kills/engagement flat within R2 vs `play_time` (ρ = 0.075, p = 0.52); since EHP is
rank-equivalent to `play_time`, it is necessarily flat vs EHP as well (ρ = 0.064, p = 0.58). The two
passes agree because they are, at this grain, the same measurement.

**Finding 1c — the within-plateau control agrees.** Inside an EHP plateau the pool is *constant*.
Pooling rank-residuals across the nine plateaus (`g2c-probes.json` P-2): kills r = −0.039 (p 0.74),
duration r = +0.061 (p 0.61), A r = −0.120 (p 0.31), B r = −0.036 (p 0.76), C r = +0.015 (p 0.90).
**Behaviour is flat against the clock at constant pool, and flat against the pool across the clock.**
There is no behavioural signal here to attribute to anything.

### 1.3 What DOES move: raw hazard — and the EHP denominator eats most of it

| instrument | n | ρ vs EHP | p |
|---|---|---|---|
| **intake HP per covered second (RAW)** | 73 | **+0.246** | **0.036** |
| intake %EHP per covered second | 73 | +0.170 | 0.152 |
| **largest drop in the engagement (RAW HP)** | 50 | **+0.390** | **0.0051** |
| largest drop in the engagement (%EHP) | 50 | +0.198 | 0.167 |
| mean drop (RAW HP) | 50 | +0.207 | 0.149 |
| mean drop (%EHP) | 50 | +0.018 | 0.901 |

**Finding 1d — the world scaled with the pool.** Raw intake rate and raw biggest-hit rise with EHP at
ρ = +0.25 / +0.39. Express the *same quantities* in EHP units and both fall out of significance
(+0.170, p 0.15; +0.198, p 0.17), and mean drop size goes to exactly zero (+0.018, p 0.90). Over R2,
**a 2.07× pool bought approximately no net EHP-denominated safety.** That is a description of the
joint progression — pool, level and zone advanced together — and explicitly **not** a causal claim
about EHP, which §1.1 forbids.

### 1.4 The cross-regime signature test — the one place the channel is still discriminable

Within R2 the channel is invisible. Across the R2/R3 boundary the two competing hypotheses make
**different predictions about which ABC factor moves**, and that is testable:

- *Survivability ("tankier, holds pack centres")* → **C up** (more bursts held per engagement) and/or
  **duration up**; A may rise if he can stand inside larger clumps.
- *DoT tail* → **B up alone**; A and C unchanged.

R2's last 16 engagements (`play_time` 4604–5808) vs R3 (6475–6847), Mann–Whitney on the
per-engagement distribution, n = 16 each:

| factor | R2-last-16 | R3 | ratio | MW p |
|---|---|---|---|---|
| A — simultaneity | 1.763 | 1.984 | ×1.125 | 0.533 |
| **B — kill-events per burst** | 2.510 | 3.495 | **×1.392** | **0.096** |
| C — bursts per engagement | 1.875 | 2.125 | ×1.133 | 0.311 |
| engagement duration (s) | 4.906 | 7.688 | ×1.567 | 0.734 |
| kills per engagement | 8.062 | 11.875 | ×1.473 | 0.199 |

*(Estimator reconciliation, `g2c-sensitivity.json` S-3: G-2b §5d reports the **ratio-of-means**
regime aggregate — A 1.897 / B 2.267 / C 1.875 for R2-last-16 and 1.900 / 2.941 / 2.125 for R3. This
pass's Mann–Whitney needs the per-engagement distribution, hence **mean-of-ratios**. Both forms are
banked. They are two estimators of the same quantity, not a discrepancy.)*

**Finding 1e — the observed signature fits the DoT tail better than survivability.** B is the only
factor under p = 0.1 and the only one with a ratio outside the noise band the others sit in. C moves
×1.13 at p = 0.31; A moves ×1.13 at p = 0.53. Duration's means differ by ×1.57 but its
Mann–Whitney is p = 0.73 — the mean is carried by two long right-tail engagements, not by a shifted
distribution. **Survivability is neither supported nor excluded here; it is underpowered at n = 16**,
and it predicts movement in C and duration that the ranks do not show.

### 1.5 VERDICT ON QUESTION 1

> **The survivability channel leaves no measurable trace inside R2, and inside R2 it is in principle
> unmeasurable.** All four commissioned instruments are null (|ρ| ≤ 0.28, p ≥ 0.086). The EHP
> instrument itself is rank-degenerate with the clock (ρ = +0.985) and with character level
> (ρ = +0.999), so **"confounded, undecidable" is the correct answer on causal attribution** — and it
> is a *structural* undecidability, not a sample-size one. What is decidable and non-null: **raw
> hazard rose with the pool and EHP-normalised hazard did not** (ρ +0.246 → +0.170; ρ +0.390 →
> +0.198), i.e. the progression was roughly safety-neutral in EHP terms. Cross-regime, the R3 lift
> sits in **B alone**, which is the DoT signature; the survivability signature (C and/or duration)
> is absent at the rank level. **The fourth channel does not earn a place in the causal ledger on
> this evidence — and it cannot be given one from this fixture at all.**

---

## 2. QUESTION 2 — the 27 ≥10%-EHP hits in R2: early-clustered or late?

### 2.1 Answer: LATE, decisively

| | |
|---|---|
| R2 drop events (total) | **332** |
| ≥ 10% EHP | **27** (8.13% of drops) |
| median `play_time` of the 27 | **5453** — against **3838** for all R2 drops |
| Mann–Whitney (big-hit times vs all-drop times) | **p = 9.5e-5** |
| median position within R2's span (1134–6052) | **0.878** |
| split at R2's **covered-time** median (`play_time` 3800) | **4 early / 23 late** |
| in the final 377 s of kill activity (`play_time` ≥ 5431) | **18 of 27 (66.7%)** |

**By EHP plateau, against admissible covered intake time as the exposure denominator:**

| EHP | `play_time` span | covered s | frac of R2 covered time | drops | **≥10% EHP** | expected if uniform |
|---|---|---|---|---|---|---|
| 366 | 1470–1563 | 75.5 | 9.1% | 15 | **0** | 2.46 |
| 443 | 1824–1903 | 74.1 | 8.9% | 16 | **0** | 2.41 |
| 451 | 2068–2153 | 85.0 | 10.2% | 25 | 2 | 2.76 |
| 471 | 2637–2815 | 34.2 | 4.1% | 13 | **0** | 1.11 |
| 491 | 2939–3045 | 61.1 | 7.4% | 50 | 2 | 1.99 |
| 672 | 3689–3919 | 205.3 | 24.7% | 67 | 2 | 6.68 |
| 707 | 4256–4604 | 195.1 | 23.5% | 47 | 3 | 6.35 |
| **747** | 4987–5648 | 82.1 | 9.9% | 66 | **9** | 2.67 |
| **759** | 5791–5808 | 17.9 | 2.2% | 33 | **9** | 0.58 |

> **The two highest plateaus are 12.0% of R2's covered intake time and carry 18 of the 27 big hits
> against 3.25 expected — a 5.5× enrichment.** The three lowest-denominator plateaus (366, 443, 471),
> together 22.1% of covered time, carry **zero**. The low-denominator-artifact hypothesis predicts
> exactly the opposite pattern.

### 2.2 The same hits in raw HP — denominator removed entirely

The decisive test uses **no denominator at all**: count drops above a fixed **raw HP** threshold, per
covered second, split at R2's covered-time median (`play_time` 3800). Exposure is near-identical on
the two sides — **413.1 s early vs 417.1 s late** — so the rates are directly comparable.

| raw threshold | early n | late n | early /100 s | late /100 s | **rate ratio** | binomial p vs exposure |
|---|---|---|---|---|---|---|
| ≥ 10 HP | 63 | 74 | 15.25 | 17.74 | ×1.16 | 0.394 |
| ≥ 20 HP | 32 | 48 | 7.75 | 11.51 | ×1.49 | 0.093 |
| **≥ 40 HP** | 8 | 38 | 1.94 | 9.11 | **×4.70** | **9.3e-6** |
| **≥ 75 HP** | 2 | 21 | 0.48 | 5.03 | **×10.4** | **6.6e-5** |
| ≥ 100 HP | 2 | 11 | 0.48 | 2.64 | ×5.45 | 0.022 |
| ≥ 150 HP | 0 | 4 | 0.00 | 0.96 | — | 0.125 |

**Finding 2a — small hits are flat, big hits are late, and the denominator moves the WRONG way for
the artifact hypothesis.** At ≥ 10 HP the rate ratio is 1.16 (p = 0.39) — indistinguishable. The
separation appears only above ~40 HP. And the denominator *grew* 2.07× across R2, which **suppresses**
late percentages; the late clustering survives that suppression rather than being manufactured by it.

**Finding 2b — the 27 are large in absolute terms, not just relative ones.**

| | n | mean | median | p25 | p75 | max |
|---|---|---|---|---|---|---|
| the 27 (raw HP) | 27 | **125.7** | **84** | 77 | 121 | **541** |
| all R2 drops (raw HP) | 332 | 20.2 | 5.0 | 1 | 18 | 541 |

### 2.3 Robustness — and the one qualification

`g2c-sensitivity.json` S-1:

| variant | ≥ 40 HP | ≥ 75 HP |
|---|---|---|
| full | ×4.70, p = 9.3e-6 | ×10.4, p = 6.6e-5 |
| **drop the death engagement (eng 82)** | ×4.15, **p = 6.6e-5** | ×8.55, **p = 3.9e-4** |
| **worst leave-one-engagement-out** (drops eng 88, 7 of the 23 ≥75 HP hits) | ×3.82, **p = 2.6e-4** | ×7.14, **p = 0.0022** |
| **engagement unit** (distinct engagements carrying such a hit) | 4/35 vs 16/42, **Fisher p = 0.0094** | 2/35 vs 9/42, Fisher p = 0.058 |
| **excise the whole post-death tail (eng 82–89)** | ×2.38, p = 0.045 | **×2.24, p = 0.43 — NOT established** |

**Finding 2c — the result survives every single-engagement deletion and holds on the conservative
engagement unit, but at the highest thresholds it is CARRIED BY R2's TERMINAL EIGHT ENGAGEMENTS.**
Excise `play_time` 5447–5808 and the ≥75 HP contrast collapses to p = 0.43. The honest statement is
two-part: **R2's body is comparatively homogeneous in big-hit rate; R2's tail is a different regime.**

### 2.4 The R2 tail is a distinct hazard sub-regime

| | body (eng 13–81, `play_time` 1470–5431) | **tail (eng 82–89, 5447–5808)** | ratio |
|---|---|---|---|
| engagements | 69 | 8 | |
| covered intake seconds | 782.2 (94.2%) | **48.1 (5.8%)** | |
| kills | 604 | 43 | |
| total measured intake (HP) | 3,811 (56.8%) | **2,901 (43.2%)** | |
| intake HP per covered second | 4.87 | **60.36** | **×12.4** |
| drop events per 100 covered s | 32.7 | 158.1 | ×4.8 |
| drops ≥ 40 raw HP | 25 (54%) | **21 (46%)** | ×13.7 by rate |
| deaths | 0 | **1** | |

**5.8% of R2's covered intake time carries 43% of its measured damage and 46% of its ≥40-HP hits.**

### 2.5 Denominator sensitivity — the count is robust, two magnitudes are not

`hp_max_seen` (max *current* HP observed) is the denominator `tb_rollup.py` used and therefore the
one that produced the charter's "27". It is a **lower bound** on the true pool, so it **overstates**
percentages. Re-scored against `max_hp_modal` (the modal right operand of the full "cur/max" read),
with one guard: **a modal read below the window's own current-HP high is rejected** — eng 31 returns
modal 45 against a current-HP high of 451, a truncated right operand.

| | |
|---|---|
| ≥10% on `hp_max_seen` (charter figure) | **27** |
| ≥10% on modal-where-valid | **27 — unchanged** |
| windows whose denominator was understated | eng **84** (430 vs 747), **85** (434 vs 747), **88** (726 vs 759) |
| windows with a rejected modal read | eng **31** (45 vs 451) |
| windows with no modal read at all | 8 (eng 25, 27, 30, 32, 33, 34, 37, 39) |

**Finding 2d — the count survives the correction; two individual magnitudes do not.** Eng 84's two
hits re-score from **33.0% / 43.0% → 19.0% / 24.8%**. Both still clear 10%, so the census is
unchanged — but neither figure should travel as a 43%-of-pool hit.

### 2.6 VERDICT ON QUESTION 2

> **LATE, and not a low-denominator artifact.** 18 of 27 sit in R2's final 377 seconds of kill
> activity; the three lowest-denominator plateaus carry **zero**; the effect is reproduced with the
> denominator removed entirely (≥40 raw HP: ×4.70, p = 9.3e-6; ≥75 raw HP: ×10.4, p = 6.6e-5, on
> near-equal exposure), and it is invisible at ≥10 raw HP, which is where a denominator artifact
> would have shown first. It survives removing the death engagement (p = 6.6e-5) and any single
> engagement (worst case p = 2.6e-4). **Qualification:** above ~75 HP the effect is carried by the
> terminal eight engagements — R2's body is homogeneous, R2's tail is a separate hazard regime.
> **R2 carried genuine large hits near max pool.** The charter's ripple-2 reading is upheld, with the
> anchor it used re-graded in §3.1.

---

## 3. CONTRADICTIONS — named loudly, per the commission

### 3.1 ⚠ C-1 — the 72.4% anchor hit IS the death, and it is floor-censored

Charter §9 ripple 2: *"The 72.4% hit sits at EHP 747 — late-regime, near-max pool — so at least the
extreme is a genuine huge hit."*

| | |
|---|---|
| the drop | `pts_s` **5151.4333**, eng 82, **hp 541 → 0**, dt 0.133 s |
| death-counter increment | `pts_s` **5151.5**, i = 10303, deaths **1 → 2** |
| separation | **0.067 seconds** |
| `play_time` | **5453** |

**It is the killing blow of the run's second and final death.** Three consequences:

1. **541 is a LOWER BOUND, not a measurement.** The globe floors at 0; whatever the blow's nominal
   damage was above 541, the instrument cannot see it. The hit is at least as large as claimed —
   possibly much larger — but it is censored, and censored values must not enter a distribution fit.
2. **Every statistic carrying it must carry "this is a death event."** The charter's headline
   R2-vs-R3 max-drop contrast (**541 → 136**, cited in §9 as surviving in raw HP) is partly a
   comparison of *a death* against *a regime containing no death at all*. R3 has zero deaths. The
   hazard-shape finding still stands — §2.2's threshold sweep re-establishes it without this event,
   and §2.3 shows the late clustering survives eng 82's deletion at p = 6.6e-5 — but **the specific
   541-vs-136 framing is not a like-for-like comparison** and should not anchor a band.
3. It is also the *only* fixture event where the intake instrument and the death counter can be
   cross-validated against each other. They agree to 0.067 s. That is a free calibration datum for
   the R-KC1-11 degradation model, and I recommend it be banked as one.

### 3.2 ⚠ C-2 — R2 is NOT "the longest stretch without a compound step"

Charter §9 ripple 4: *"**R2 remains the fixture** precisely because it is the longest stretch without
a compound step."* **The max-HP series contradicts this.** Bracketing each EHP step against the
level-up series and the `shield_block_chance` series (`g2c-probes.json` P-4):

| EHP step | Δ HP | % | bracket (`play_time`) | level-ups in bracket | HP per level-up | block change in bracket |
|---|---|---|---|---|---|---|
| 366 → 443 | **+77** | +21.0% | 1563–1824 | **NONE** | — | — |
| 443 → 451 | +8 | +1.8% | 1903–2068 | L5 | 8 | — |
| 451 → 471 | +20 | +4.4% | 2153–2637 | L6 | 20 | — |
| 471 → 491 | +20 | +4.3% | 2815–2939 | L7 | 20 | — |
| **491 → 672** | **+181** | **+36.9%** | 3045–3689 | L8 | **181** | **15.0 → 18.0 @ `play_time` 3256** |
| 672 → 707 | +35 | +5.2% | 3919–4256 | L9 | 35 | — |
| 707 → 747 | +40 | +5.7% | 4604–4987 | L10 | 40 | — |
| 747 → 759 | **+12** | +1.6% | 5648–5791 | **NONE** | — | — |

**R2 contains at least three gear events, and one of them is compound:**

- **`play_time` 3045–3689 — COMPOUND.** +181 HP is **4.5× the largest level-attributable gain** in
  the regime (40 HP at L10), and its bracket contains **the run's only `shield_block_chance` change,
  15.0 → 18.0 at `play_time` 3256**. **Pool and mitigation moved together, inside the fixture.** By
  the charter's own §9 definition of the R2/R3 event, that is a compound gear step.
- **`play_time` 1563–1824 — pure gear.** +77 HP (+21.0%) with **zero level-ups in the bracket**
  (L4 landed at 1563, L5 at 1907).
- **`play_time` 5648–5791 — minor, pure gear.** +12 HP, zero level-ups.

This also **refines §11.2**. That correction was right — block is not the R2/R3 boundary mechanism,
and Matt was wearing a shield long before level 12. But in falsifying block as the *boundary*
mechanism, §11.2 walked past what the single block change actually is: **the timestamp of an
intra-R2 gear event**, coincident with the largest pool step in the regime.

**What this does and does not change.** R2 remains the right fixture — it is the longest span, the
largest sample, one build, one skill set. But it is **not** justified by the stated reason, and the
practical consequence is real: R2's own EHP normalisation is not measuring one character. Anything
fit across the `play_time` 3256 step is fit across a gear change.

### 3.3 ⚠ C-3 — unit collision inside ratified ruling R-KC1-8

R-KC1-8 records: *"death-counter increments at **pt 2837** (outside windows AND dps spans …) and
**pt 5152** (inside both)."* Those are **`pts_s`** (video clock) values. Their `play_time` values are:

| event | `pts_s` | **`play_time`** |
|---|---|---|
| deaths 0 → 1 | 2837.0 | **3156** |
| deaths 1 → 2 | 5151.5 | **5453** |

Everywhere else in the charter, "pt" abbreviates `play_time` (`pt 1145`, `play_time 3256`,
`play_time 6052`). A reader applying that convention places the second death ~300 s early, in a gap
between engagements 76 and 77, and would then read "inside both" as false. **The ruling's substance
is correct on the video clock; only its clock label is ambiguous.** It matters concretely: the
correct `play_time` 5453 is where the fixture's largest hit lives (§3.1), and `play_time` 3156 sits
100 s from the C-2 block change at 3256. Recommend R-KC1-8 be amended to carry both clocks
explicitly.

### 3.4 ⚠ C-4 — the instrument degrades exactly where question 2 lands

Globe coverage falls as EHP rises: **ρ = −0.432, p = 9.9e-5** across R2 windows, and **−0.250,
p = 0.043** even *within* EHP plateaus. The high-EHP end of R2 — the region carrying the answer to
question 2 — is the worst-measured part of the fixture.

Concretely: R2's last EHP quartile has 19 engagements but only **7** clear the 0.80 coverage gate,
and those 7 include the three most violent windows (eng 84, 88, 89). The quartile's
coverage-gated mean intake reads **260.7 HP** against 35–48 HP in the first three quartiles — a
figure that is simultaneously **true of its sample** and **not a regime estimate**.

> **Recommendation, in-lane:** for R2's late region, per-covered-second **rates** are the defensible
> instrument and per-engagement **totals** are not. §2.2's threshold sweep is built entirely on rates
> for this reason. This does not weaken the question-2 answer — it is why that answer was constructed
> denominator-free.

**A related honesty note.** The pooled within-plateau hazard-vs-clock correlation is +0.383
(p = 0.00098), which looks like "hazard rises with the clock even at constant pool." Split per
plateau it is **not uniform**: 747 gives ρ = +0.685 (p = 0.029, n = 10) and 672 gives ρ = +0.499
(p = 0.058, n = 15), but **707 — the largest plateau at n = 19 — is exactly null (ρ = −0.047,
p = 0.85), with a median engagement intake of 0.0 HP/s.** The pooled figure is carried by the same
tail as everything else in §2.3. I report it as **weak and tail-driven**, not as a finding.

---

## 4. Consequences I am routing, not ruling

1. **HALT H-2 band drafting (gandalf).** R2's intake distribution is **not stationary** (§2.4:
   ×12.4 in rate between body and tail, 5.8% of covered time holding 43% of intake). A band fit on
   pooled R2 intake is a band fit on a bimodal mixture. Either declare the tail as a named
   sub-partition or carry the non-stationarity explicitly in the band's error bars. Bands on
   **rates**, not totals (§3.4).
2. **G-4 kit spec.** The gear-identity task grows: **`play_time` ~3256 is a second gear event**
   requiring identification (+36.9% pool, +3 pp block), and `play_time` 1563–1824 is a third
   (+21.0% pool, no level-up). The `.gdc` probe already returned "a depot fetch contains no save,"
   so these are `.arz`-side or testimony-side questions.
3. **fixtures.db (elrond).** Three columns worth carrying: `is_death_event` on drop rows (§3.1),
   a `denominator = hp_max_seen | max_hp_modal` flag on every %EHP figure (§2.5), and the
   `pts_s` / `play_time` pair on every event row (§3.3).
4. **R-KC1-11 degradation model (star-lord/gamora).** The 0.067 s agreement between the intake
   instrument and the death counter (§3.1) is the only independent cross-validation of the globe
   reader in the fixture. Bank it as a calibration datum.
5. **The EHP-vs-progression question is not answerable from any observational fixture** (§1.1). It
   is answerable by **G-5's sweep**, holding pool fixed while density/level vary. Routed there.

---

## 5. Coverage register

| Metric | Coverage | Basis |
|---|---|---|
| 106-window reproduction | 100% | field-identical to committed T-B |
| timestamped drop replay | **100%, 0/106 mismatches** | every committed per-window quantity |
| R2 windows with a readable pool | 76 / 77 (98.7%) | eng 39 is zero-coverage |
| R2 windows with a modal `cur/max` read | 68 / 77 (88.3%) | 8 with none, 1 rejected (eng 31) |
| R2 globe frame coverage | **92.1%** body (eng 13–81) / **66.4%** tail (eng 82–89); per-window low 0.21 | §3.4 |
| `deaths` series | 100%, 0 non-monotone | terminal value 2 |
| `shield_block_chance` series | 1 change in the whole run | §3.2 |
| `max_level` series | 100%, 0 non-monotone | 11 level-ups located on both clocks |
| **causal separation of pool from level/zone within R2** | **0% — structurally impossible** | ρ = +0.985 / +0.999 (§1.1) |
| pack size | **0% — no instrument exists** | T-C cancelled per R-KC1-10; routed to G-4/G-5 |

---

## 6. What this note does NOT claim

- It does **not** claim survivability had no effect. It claims the effect is **unmeasurable inside
  R2 in principle** (§1.1), leaves **no behavioural trace** in any instrument tried (§1.2–1.3), and
  fits the R2→R3 signature **worse than the DoT-tail hypothesis** does at n = 16 (§1.4). Absence of
  a measurable trace is not absence.
- It does **not** claim R2's late hazard rise is *caused* by anything. Pool, level, zone, and act
  progression all advance together; §1.1 forbids attribution among them.
- It does **not** re-open the R2/R3 boundary. §11.3's DERIVED-NONIDENTIFYING grade is untouched;
  this pass adds only that the boundary's dead interval also brackets the 759 → 1600 step.
- It does **not** claim the R2 tail is anomalous *play*. Eight engagements around a death, in a
  poorly-covered stretch, is what the ledger shows; why it is violent is not a question this
  instrument can answer.
- It does **not** fire, propose, or depend on any T-C enemy census. R-KC1-10 is honoured in full.

---

**The Mirror, briefly.** He got twice as hard to kill and it changed nothing that can be seen. Nine
times the pool stepped up beneath him, and across seventy-two minutes not one thing he did with it
moved: the fights are the same length, the hits arrive at the same spacing, he kills at the same
rate. What the extra health bought was not safety — the world took it back at the same pace it was
given, so that the *fraction* of him a blow removed never changed at all. And then, at the very end
of the stretch, in the last six minutes of a regime that had been placid for an hour, the numbers
turn: the big hits arrive thirteen times as fast, forty-three percent of everything he ever suffered
in R2 lands inside five percent of its measured time, and the largest reading in the whole fixture is
not a hit at all. It is the last five hundred and forty-one points of him, going to zero, sixty-seven
milliseconds before the counter admits it.

**Signed:** galadriel, 2026-07-28.
