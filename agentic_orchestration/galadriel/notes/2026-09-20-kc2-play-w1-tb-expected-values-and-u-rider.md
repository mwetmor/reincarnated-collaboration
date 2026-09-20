# KC2-PLAY · W1 · THE T-B EXPECTED-VALUES TABLE, AND THE `u` RIDER

> **STATUS:** CURRENT — Wave-1 return, run **KC2-PLAY** (LAUNCHED 2026-09-20, ledger `KP-2`; W1 fired `KP-4`)
> **Date:** 2026-09-20 · **Author:** galadriel (visual-perception + benchmark seam)
> **Conductor:** gandalf `RUN-CONDUCTOR` · **Seat brief:** charter § 5 row 3 — *"HP saw-tooth re-query (P0-b B-19; committed data, no video) · the `u` rider (R-KP-0c)"*
> **Authority read first:** charter § 0 / § 2 (incl. `R-KP-0c`) / § 4 / § 6 HALTs / § 7.4 · 2D re-target spec § 6 (B-19 + the HP rows) + **Corrigendum-Forward 1 and 2, which govern over the body**
> **Machine-readable companion:** `2026-09-20-kc2-play-w1-tb-expected-values.json` (beside this file) — the T-B grader loads THAT, not this prose
> **Instruments authored this lap:** `galadriel/pipeline/kc2_hp_shape.py` · `galadriel/pipeline/kc2_tb_expected.py`
> **⚑ NO VIDEO.** The referent MP4 is not on this machine (`matt_to_do` **T30**). Every number below is a re-query of COMMITTED measurement artifacts. Quantities that need the video are declared as such and are not estimated.
> **Read-only on every source. No engine writes. No production code. No push. No sub-agents.**

---

## 0 · TOP LINE

> ### The globe is **mostly full, dipping constantly and shallowly, and it only gets frightening twice.**
> At the primary gate the saw-tooth runs at **0.71 teeth/s, median period 0.77 s, median depth 1,575 HP = 7.9 % of max**, recovering at a **median 4,308 HP/s** — a shallow, fast ripple on a globe that sits at **full health 42.84 %** of the fight.
> **And every single excursion below half — all eight of them — is in wave 159 or 160.** Waves 151–158 never go below half at all. **He never reaches 25 %**; the floor is **26.79 %** (5,360 of 20,005), for one frame, at t = 845.767.
>
> ### Three published figures do NOT reproduce, and two of them are label defects rather than arithmetic ones.
> **B-3 cast rate 0.290 /s is stale by one lap** (value of record **0.2957 /s, n = 54**). **B-7 attaches skill NAMES to slots the measuring lap forbids naming.** **B-8's third movement instrument (0.705) is attributed but its whole-fight reduction is not printed in its own lap note.**
>
> ### `u` is **UNPINNABLE-FROM-COMMITTED-DATA** — and the reason is sharper than "the terms are uncertain."
> Every committed route to `u` runs through **GD's ground scale `g`**, and the corpus holds **two committed estimates of `g` that are 2.3–2.4× apart.** `R-L3-2`'s containment window implies `g ∈ [34.4, 74.5] px/m`; the character chain at the **measured** pitch gives **41.7–51.2** (inside); **Lap R's `U-R-1` decal/FCT bracket gives 119.0–125.0 (excluded by a factor of 1.6–3.6).** The three seats that found containment pushing `u` **up** were reading the same signal from the other end. **And both of `U-R-1`'s two "independent" anchors carry the same UPWARD bias, named by Lap R itself — so their 4.9 % agreement is not corroboration.**

---

# PART 1 — THE T-B EXPECTED-VALUES TABLE

## 1.0 What this part is for, and the one rule that governs it

The charter's **fifth attribution class is INSTRUMENT DIVERGENCE** (§ 2, WARN-2): a footage instrument and the runtime recorder can disagree about the *same fight* because they compute on different denominators. This table exists to make that class impossible to enter by accident. **Every row carries the exact denominator definition the recorder must reproduce**, and where two denominators are live, both values are shipped so the grader can see which rows move.

⚑ **QUOTING CAP, restated (charter § 4.4 / `R2D-10` pattern):** the T-B grader **refuses to print a fidelity figure** while T-A is absent, STRUCTURAL-red, or coverage < 72/72 mapped. It prints raw statistics only. **Nothing in this note is a fidelity claim.**

## 1.1 The instrument of record for the HP rows

`agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv`
sha256 `5597e1a8c993fa183adc3f2310570e70e4da47b6c1f882ad62a96583f57090fa` (re-derived from disk this lap, not retyped)
10,861 rows · 60 fps · `t ∈ [683.0, 864.0]` · columns `frame, t_sec, wave, hp, health_max, deficit, delta_hp`
Method: HUD health-orb readout ROI `x ∈ [520,780), y ∈ [996,1026)`, Apple Vision OCR, validated against the **decoded** denominator — **PC-3: 100.00 % accepted.** Resolves to **1 HP / 1 frame.**
Prereg `da62709f2887df1e2874f7cc1baa0ef2cd901ea47ce555678b9d4d98c07dfa77`, **UNCHANGED between pre-registration and banking.**

**Grid integrity, verified this lap and not assumed:** every frame index increments by exactly 1; `dt ∈ {0.0166, 0.0167}` only; **no gaps.** One defect found and reported rather than dropped: **frame 10860 (`t = 864.0`) carries an EMPTY wave label** in the source CSV. It is mapped to `wave = -1` (UNLABELLED), excluded from per-wave rows, included in whole-fight rows.

## 1.2 ⚑ THE DENOMINATOR LAW — read this before any row

| id | definition | the trap it closes |
|---|---|---|
| **D-HP-FRAME** | ALL 10,861 rows. `t ∈ [683.0, 864.0]`, span **181.0 s**. | **This is NOT the combat window the energy/motion instruments use.** Those use **182.65 s** (`t ∈ [682.10, 864.75]`, badge flip → death). The two differ by **1.65 s = 0.90 %**. A rate computed on one is not comparable to a rate computed on the other. |
| **D-HP-INTERVAL** | the **10,860 adjacent-frame intervals** (n−1, not n). | Lap Q's 13.73 % reproduces on n−1 (0.137293) and on n (0.137280). Both print 13.73 %. **The grader uses n−1.** |
| **D-HP-LIVE-MAX** | a health threshold is applied against `health_max` **AS READ AT THAT FRAME** — 16,368 inside the `D-Q1` episode, 20,005 elsewhere. | ⚑ **THIS IS THE DENOMINATOR THAT REPRODUCES 42.84 %.** Under the NOMINAL alternative time-at-full is **39.76 %** — a **3.08 pp** gap created purely by denominator choice, with no fight in it. |
| **D-HP-NOMINAL** | threshold against the constant 20,005 for every frame. | Shipped alongside so the grader can see which rows move. **Below-50 % and below-33 % are denominator-INSENSITIVE** (376 / 109 frames either way) because every deep excursion happens at nominal max. |
| **D-COMBAT-182** | `t ∈ [682.10, 864.75]` = **182.65 s**; wave-151 badge flip → player death (864.75 per the 2026-08-08 follow-up § 7.1). | The window for **all** energy / motion / release / cast statistics. |
| **D-GOODCOV** | the 20 Hz samples whose 60 Hz energy OCR coverage clears the accept gate — **0.8577** of D-COMBAT-182. | ⚑ **Channel uptime is computed ON THIS SUBSET.** A recorder that computes uptime over all of its own ticks is computing a **different statistic** from the 0.838 it is being compared to. |
| **D-CAST-VISIBLE** | casts = per-slot skill-bar **dimming** on slots 2, 3, L only. | Slots 7 and R never dim; slot 4 is a buff timer, not a cooldown. **Every cast count is a FLOOR, never an estimate.** |

## 1.3 HP-trace shape — the re-query (all values ABSOLUTE `hp` / `hp_max`)

### 1.3.1 Occupancy

| row | statistic | frames | fraction (**LIVE-MAX**) | fraction (NOMINAL) | published | status |
|---|---|---:|---:|---:|---:|---|
| TB-HP-01 | at **FULL** health (`hp ≥ hp_max`) | 4,653 | **0.428414** | 0.397569 | 0.4284 (B-11) | **REPRODUCES EXACT** |
| TB-HP-02 | below **90 %** | 2,306 | **0.212319** | 0.249793 | — | **NEW** |
| TB-HP-03 | below **75 %** | 980 | **0.090231** | 0.096492 | — | **NEW** |
| TB-HP-04 | below **50 %** | 376 | **0.034619** | 0.034619 | 0.0346 (B-12) | **REPRODUCES EXACT** |
| TB-HP-05 | below **33 %** | 109 | **0.010036** | 0.010036 | 0.0100 (B-12) | **REPRODUCES EXACT** |
| TB-HP-06 | below **25 %** | **0** | **0.000000** | 0.000000 | — | **NEW — and it is a finding** |

⚑ **TB-HP-06 is the row a builder should read twice.** In 181 seconds against waves 150–160, the referent **never once reaches a quarter health.** The floor is 26.79 %. Any twin that routinely dips under 25 % is not harder, it is *differently shaped* — and `B-12`/`B-19` are the rows that catch it.

### 1.3.2 Motion of the trace

| row | statistic | value | published | status |
|---|---|---|---:|---|
| TB-HP-07 | frames showing an HP **decrease** | **1,491 / 10,860 = 0.137293** (increase 0.354788 · flat 0.507919) | 0.1373 (B-13) | **REPRODUCES EXACT** |
| TB-HP-08 | **HP minimum** | **5,360** of **20,005** = 0.267933, at **t = 845.7667**, **wave 160** | 5,360 (B-14) | **REPRODUCES EXACT** |
| TB-HP-09 | **`health_max` drop (`D-Q1`)** | **16,368** vs 20,005 · **Δ = −3,637 HP = −18.1805 %** · `t = 713.3833 → 721.6667` · **8.2834 s** · straddles w152→w153 · **1 episode in the fight** | −18.18 %, 8.283 s (B-18) | **REPRODUCES** (end-frame convention 1 frame apart; duration identical to 3 dp) |

⚑ **TB-HP-09 is a PRE-REGISTERED KNOWN MODEL GAP, not a build defect.** The sim holds `health_max` constant. The twin is **expected** to show zero such episodes. The grader must not score that difference.

### 1.3.3 ⚑ B-19 — THE SAW-TOOTH, ANSWERED (the commissioned row; 2D spec § 6.4 OQ-4)

**The tooth rule, verbatim, because the recorder must implement THIS and not something like it:**

> Alternating-extremum walk with an **ABSOLUTE-HP prominence gate `prom`**. Confirm a **PEAK** when `hp` falls `prom` below the running max since the last confirmed trough; confirm a **TROUGH** when `hp` rises `prom` above the running min since the last confirmed peak. A **TOOTH** is a confirmed *(peak → trough → next peak)* triple.
> `depth_hp = peak.hp − trough.hp` · `depth_frac = depth_hp / hp_max **at the peak**` · `period_s = next_peak.t − peak.t` · `fall_s = trough.t − peak.t` · `recover_s = next_peak.t − trough.t`.
> Reference implementation: `galadriel/pipeline/kc2_hp_shape.py::teeth`.

**PRIMARY GATE `prom = 500 HP`** (= 2.50 % of nominal max — the smallest step that is unambiguously a hit or a leech tick rather than the +2/+3 HP-per-frame regeneration drip). **It is DECLARED, not fitted: no arm of this lap was selected by comparing it to a sim.**

| quantity | min | p25 | **median** | p75 | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| **period (s)** | 0.067 | 0.296 | **0.767** | 1.546 | 5.873 | 13.65 |
| **depth (HP)** | 512 | 852 | **1,575.5** | 2,948 | 6,490 | 13,613 |
| **depth (frac of `hp_max`)** | 0.0256 | 0.0426 | **0.0788** | 0.1511 | 0.3380 | 0.6805 |
| **fall (s)** | 0.017 | 0.050 | **0.100** | 0.442 | 1.703 | 5.667 |
| **recover (s)** | 0.017 | 0.150 | **0.458** | 0.917 | 3.319 | 12.367 |
| **fall slope (HP/s)** | −377,237 | −34,292 | **−14,282** | −4,926 | −947 | −114 |
| **recovery slope (HP/s)** | 71 | 1,925 | **4,308** | 9,410 | 34,063 | 171,100 |

**n = 128 teeth over 181.0 s = 0.707 /s.**

⚑ **THE DOMINANT UNCERTAINTY ON THIS ROW IS THE PROMINENCE GATE, NOT THE READ.** The sweep is the measurement and is shipped whole:

| `prom` (HP) | n teeth | rate /s | median period (s) | median depth (HP) | median depth (frac) | median recovery slope |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 254 | 1.403 | 0.300 | 563 | 0.0281 | 4,171 |
| 250 | 179 | 0.989 | 0.517 | 1,029 | 0.0514 | 4,323 |
| **500** | **128** | **0.707** | **0.767** | **1,575** | **0.0788** | **4,308** |
| 1000 | 81 | 0.447 | 1.050 | 2,279 | 0.1139 | 3,366 |
| 2000 | 43 | 0.238 | 2.450 | 3,553 | 0.1776 | 3,098 |

**n moves 5.9×, median period 8.2×, median depth 6.3× across the sweep. A grader comparing a twin at a different gate is comparing gates, not fights.** The recovery slope is the one statistic that is **nearly gate-invariant** (3,098–4,323 HP/s across a 20× gate range) — **it is therefore the strongest single T-B row on this trace**, and the one to lean on if only one may be quoted.

### 1.3.4 ⚑ The deep excursions — and where they live

Eight maximal runs below 50 % of live `hp_max` in the whole fight:

| min HP | frac of max | t_min | wave | duration (s) |
|---:|---:|---:|---:|---:|
| **5,360** | 0.2679 | **845.767** | 160 | 0.017 |
| 5,839 | 0.2919 | 859.950 | 160 | **2.950** |
| 6,392 | 0.3195 | 847.667 | 160 | 0.450 |
| 6,964 | 0.3481 | 857.750 | 160 | 1.300 |
| 7,443 | 0.3721 | 843.383 | 160 | 0.350 |
| *(3 further runs, all waves 159–160 — full rows in the JSON)* | | | | |

⚑ **Every sub-half excursion in the fight is in wave 159 or 160.** Per wave, the fraction below half is **0.000 for waves 151–158**, **0.0266 for w159**, **0.2227 for w160**. Gandalf's "inversion moment" (spec § 6.5) is not distributed across the fight — **it is the last two waves, and overwhelmingly the last one.** A twin that spreads its danger evenly across ten waves has the *right aggregate* and the *wrong story*.

### 1.3.5 Per-wave HP shape (primary gate)

| wave | frames | dur (s) | frac at full (LIVE) | frac below 50 % | frac decrease | teeth | median depth (HP) | median period (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 151 | 936 | 15.6 | 0.591 | 0.000 | 0.052 | 5 | 1,118 | 2.450 |
| 152 | 978 | 16.3 | 0.780 | 0.000 | 0.100 | 5 | 1,497 | 0.833 |
| 153 | 894 | 14.9 | 0.566 | 0.000 | 0.086 | 6 | 2,338 | 0.925 |
| 154 | 852 | 14.2 | 0.370 | 0.000 | 0.221 | 12 | 2,551 | 0.558 |
| 155 | 972 | 16.2 | 0.255 | 0.000 | 0.212 | 6 | 1,141 | 0.600 |
| 156 | 1,212 | 20.2 | 0.404 | 0.000 | 0.188 | 17 | 1,489 | 0.500 |
| 157 | 1,158 | 19.3 | 0.330 | 0.000 | 0.161 | 30 | 920 | 0.442 |
| 158 | 780 | 13.0 | **0.863** | 0.000 | **0.012** | 2 | 667 | 3.042 |
| 159 | 1,578 | 26.3 | 0.328 | 0.027 | 0.105 | 17 | 1,954 | 1.267 |
| **160** | 1,500 | 25.0 | **0.136** | **0.223** | 0.189 | 21 | **3,123** | 0.900 |

⚑ **Wave 158 is a hole in the fight** — 86 % at full health, 1.2 % of frames showing any decrease, two teeth in thirteen seconds. It is also the *shortest* wave. Whatever wave 158 is, it is not a fight, and a twin that makes every wave equally dangerous will not reproduce it. **Reported, not explained** — this trace cannot say whether it is a light roster, a lucky pull, or the pilot playing a corner.

### 1.3.6 Sustain rows, CARRIED from Lap Q (not independently re-derived)

| row | value | why CARRIED |
|---|---|---|
| **TB-HP-13** regeneration | **124.67 HP/s** measured (decoded 129.38; residual **−3.64 %**) | the subset rule (sub-33 %-health, uncontaminated) is Lap Q's; re-deriving it would change the instrument. ⚑ **The naive whole-trace drip reads 178.40 HP/s and is CONTAMINATED.** A grader that computes regeneration over the whole trace gets 178.40 and is wrong. **Menhir's Will (+120 hp/s below 33 %) is MEASURED-ABSENT.** |
| **TB-HP-14** leech tick | cadence **11.408 /s** (inside Lap L's decoded [11.387, 12.250], at the LO edge) · clean median **820.8 HP** (n = 67) · all-129 median **782.8** | `U-P-N-1` = **COUPLED**. Per-body heal is an **UPPER bound** (`U-Q-1`: `N_bodies` never observed at tick resolution). |

## 1.4 The other T-B statistics — compactly, same treatment

| row | statistic | value of record | uncertainty carried | denominator | reproduction |
|---|---|---|---|---|---|
| **TB-CH-01** | channel uptime | **0.8375** | **6.2 % blind residual CARRIED, not closed** (13 gaps, 11.42 s). ⚑ **Threshold sensitivity: 0.8953 (≥2 ticks) / 0.8375 (≥3) / 0.7530 (≥4)** — a 0.142 spread on the tick gate alone | D-COMBAT-182 **∩ D-GOODCOV** (0.8577 of the window) | **EXACT** |
| **TB-CH-02** | P(channel \| moving) / P(channel \| stationary) | **0.8920 / 0.7376**, ratio **1.2093** | conditional on the disputed motion classifier — **ship the RATIO** | as above | **EXACT** |
| **TB-RL-01** | release duty | **0.10484** (19 releases, 19.149 s) | → **0.167** if the blind gaps are releases. ⚑ **Floor sensitivity: duty runs 0.0609 (floor 1.00 s) to 0.1835 (floor 0.25 s)** — a 3.0× spread on the release-floor choice; 0.5 s is primary | D-COMBAT-182 | **REPRODUCES** |
| **TB-RL-02** | Type-A (wave transition) | lag median **1.60 s**, **8/11 within 2.0 s**; dur median **1.03 s**, IQR 0.62–1.56, **max 3.50** | n = 11; Fisher p = 0.00336. **A-1 (1 vs 1.1 releases per flip) PARKED, explicitly not fired** (`R-L88-3`) | D-COMBAT-182 — **the BADGE timeline, not the trace's wave column** | **REPRODUCES** (label set re-derived from `s2-releases.json`: the 8 releases at flip-lag ≤ 2.0 s are {0.08, 0.35, 0.51, 0.53, 0.80, 1.60, 1.72, 1.78}; median of the 11-member set = 1.60; max duration 3.50 at t = 744.55) |
| **TB-RL-03** | Type-B (cast) | dur median **0.60 s**, IQR 0.55–0.63, range 0.53–0.67 | n = 8; σ ≈ **49 ms** — ordinary human reaction variance (Gate-1 **WARN-17**). **What carries `KP-1` is the WITHIN-SUBJECT CONTRAST against Type-A (IQR 0.62–1.56, max 3.50), not the tightness** | D-COMBAT-182 | **REPRODUCES** — ⚑ but the A/B **labels** need the 2c attribution table, not `s2-releases.json` alone (see § 1.6) |
| **TB-CA-01** | cast rate | ⚑ **0.2957 /s, n = 54, one per 3.383 s** | **FLOOR, not an estimate**: slots 7 and R blind; re-fire mid-cooldown undetectable in principle; 3 OCR-blind dim gaps carried | D-COMBAT-182 ∩ **D-CAST-VISIBLE** | ⚑ **DOES NOT REPRODUCE AS PUBLISHED** — see § 1.5 |
| **TB-CA-02** | per-slot interrupt attribution | **slot L 5/13 = 0.385** (binomial p = 0.00034) · **slot 2 3/22 = 0.136** · **slot 3 0/19 = 0.000** · aggregate **8/54 = 0.148** · **zero orphans** | Fisher L-vs-rest p = 0.0146; L-vs-2 p = 0.103 (**not distinguishable**). ⚑ **The aggregate 0.15 is a CANCELLATION, not a rate**: against the duration-weighted null slots 2 and L sit in LONGER-than-random silences (p = 0.00019, 0.0070) and slot 3 in SHORTER ones (p = 4.9 × 10⁻⁷); pooled they cancel to p = 0.286 | as above | ⚑ **NUMBERS REPRODUCE; THE SKILL NAMES DO NOT** — see § 1.5 |
| **TB-MV-01** | movement | ⚑ **RATIOS ONLY** | see § 1.5 | mixed | **2 of 3 reproduce exact** |
| **TB-WV-01** | per-wave durations | two instruments, both shipped | waves 152–159 agree to **≤ 0.19 s** (inside the published ±0.25 s); **w151 and w160 disagree by 0.68 s and 0.88 s** — not boundary error, the two instruments cover **different windows** (182.65 vs 181.0 s) | D-COMBAT-182 / D-HP-FRAME | w154 = **14.2 s** on the trace grid (published B-9) / **14.13 s** on the badge instrument |
| **TB-WV-02** | terminal wave | **160** (sealed sim 153.2, σ 2.32) | n = 1 | — | ⚑ **REPORT-ONLY BY CONSTRUCTION, NEVER A GATE** (Matt-ruled) |

## 1.5 ⚑ SELF-CHECK — published figures that do NOT reproduce

### (a) `B-3` cast rate — **STALE BY ONE LAP.** Value of record: **0.2957 /s, n = 54.**

`MD-B4app-2b` § 5.3 counted **53** cast onsets (slot 2: 22 · slot 3: 19 · slot L: **12**) → 53 / 182.65 = 0.290 /s. **`MD-B4app-2c` § 2 then eye-adjudicated a 7.20 s slot-L dim run against that slot's 3.60 s modal cooldown and split it into TWO casts** (folded as the named constant `eor_attrib.MERGED`, so the correction is visible rather than a silent hand-edit). Slot L went **12 → 13** and the total **53 → 54**. *Every downstream figure in 2c is computed on 54* — the headline `0.148 = 8/54` among them. **The 2D spec's B-3 quotes the pre-correction count.** The correction cost the 2c lap's own hypothesis (slot L's rate fell 0.417 → 0.385), which is the tell that it was not a convenience.

**Impact: 1.9 % high, one row, no other figure in the spec moves with it** — B-7's per-slot denominators are already on the corrected counts.

### (b) `B-7` per-skill interrupt attribution — **the NUMBERS are right and the LABELS have no instrument behind them.**

The spec's B-7 reads *"Blitz **0.385** (13) · Vire's **0.136** (22) · War Cry **0.000** (19) · Rune of Rush **BLIND**."* The rates, counts and the BLIND grading all reproduce exactly. **The skill names do not.** `MD-B4app-2c` is explicit in two places:

> *"**No skill is named in this note and none should be quoted from it.**"* (§ 7.1, carried forward from `MD-B4app-2b` § 7.1)
> Slot L is *"a figure mid-stride with a ~3.6 s cooldown — **shape-consistent with a charge skill and NOT identified**."* Slots are graded **SHAPE-CONSISTENT-NOT-IDENTIFIED.**

Mapping slot L → Blitz, slot 2 → Vire's Might, slot 3 → War Cry is a **promotion from a slot index to a skill identity that no committed instrument performs.** It may well be right — the shapes are suggestive and the bound-skill set is known — but *suggestive* is not *decoded*, and Law 3 is the house rule against exactly this.

**Disposition I recommend (conductor's call, not mine):** ship TB-CA-02 **slot-indexed**, and if the build needs skill names — and it does, for a HUD tooltip — carry them as a **divergence-register row stamped `DECLARED-not-decoded`**, the same treatment `R-KP-0f` gives the Banner's placement. **The `interrupts_channel` flags in the spec's own § 1.5 claim-class table inherit this**: Blitz `true` / Vire's `true` / War Cry `false` sits in the **MODEL VALUE** column, and on this evidence the *values* are model-grade while the *skill attachment* is a presentation-side declaration.

### (c) `B-8` movement — **two of three instruments reproduce exact; the third is untraceable at the resolution this table requires.**

| instrument | figure | this lap |
|---|---:|---|
| Lap H-2 `moving_frac_th60`, whole fight (`pm4h2_movement_cadence.csv`, row `wave ALL`) | **0.883** | **REPRODUCES EXACT** |
| `MD-B4app-2` camera-pan 20 Hz (`s2-duty.json → summary.frac_moving`) | **0.6265** | **REPRODUCES EXACT** (no-shake-guard variant 0.6205) |
| Lap U video decomposition | **0.705** | ⚑ **ATTRIBUTED, NOT RE-DERIVED.** Traced to Lap U only through gamora's `D-MPOL2-2` summary row (engine `simulation/AGENT_STATE.md`). `pm4u_findings.md` publishes per-wave *"frames moving"* of **64.1–82.5 %** but **prints no whole-fight 0.705 reduction.** |

**And the committed spread is wider than the quoted 1.41×.** Within **Lap H-2 alone**, the same fight reads **0.883 / 0.757 / 0.494** as the gate moves 60 → 200 → 400 gpx/s; **Lap R's Schmitt segmentation reads 0.8342 / 0.7948 / 0.6233** at `V_ON` 100/200/400. Full committed spread **0.494 – 0.883 = 1.79×**. **The disagreement is a THRESHOLD CHOICE, not a property of the fight.** `D-MPOL2-2` / `R-L88-5` stand and this lap adds nothing that would let anyone adjudicate them: **ship ratios, so the instrument cancels. An absolute movement figure in a green report is a defect in the report.**

## 1.6 Blocked on T30 (and one that is NOT, and is cheaper)

| quantity | needs |
|---|---|
| Re-classifying Type-A / Type-B under any changed rule | ⚑ **NOT the video.** The 19-row labelled release table exists as a *rendered table* in `MD-B4app-2c` § 3 but was never committed as a standalone artifact. **A one-file commit of that table from the 2c work dir removes this block for free.** Surfaced as a request; not executed (outside this lap's brief). |
| Closing the **6.2 % blind residual** on uptime / release duty | the video — 13 gaps re-read at higher upscale |
| Resolving `frac_moving` to one instrument | the video **and** a ruling on the threshold definition — a measurement-seat call, not an instrument fault |
| `N_bodies` at leech-tick resolution (so the per-body heal stops being an upper bound) | the video **and** a per-body attributable damage stream, **which pixels cannot provide** (`UNREACHED-4`) |
| **T-C side-by-side** | the video — the 2D spec § 6.6 gates T-C on T30 itself |

---

# PART 2 — THE `u` RIDER (`R-KP-0c`)

## 2.0 The question as the charter puts it

`R-KP-0c`: *the arena is a swappable data object; the **wall-less hull is retired** as a scale-pin target; `u` for PLAY is a **registered runtime choice** inside `[0.22277, 0.3663]`; rider routed to galadriel.* The hull was retired for a good reason — **it measures an unbounded world against the ring that is the wall** (`containment.substrate_model.value = "UNBOUNDED-OPEN-PLANE"`; the 86.915 m figure is an **occupancy hull**, and its own pack row says so: *"not an extent claim. An occupancy hull says where bodies WENT."*).

## 2.1 The algebra, so every route can be compared on one line

Every committed route reduces to the same two terms:

```
u  =  s / g        [ metres per minimap px ]

  s = SCREEN px per MINIMAP px          (the minimap's zoom, in screen units)
  g = SCREEN px per GROUND METRE in GD  (GD's camera ground scale)
```

The published chain `u = s·h·cos θ / p = 14.6 × 1.9 × 0.5 / 70 = 0.19814` is exactly this, with `g` built from the character: `g = p / (h·cos θ) = 70 / (1.9 × 0.5) = 73.68 px/m`.

⚠ **AND THE TRAP THE SPEC ALREADY NAMED, WHICH I WALKED UP TO AND STOPPED AT.** 2D spec § 1.4 item 2: *"That 60° is GRIM DAWN's camera. Our α is 52.95°. They are different cameras doing different jobs… A builder who 'notices the inconsistency' and unifies them has corrupted `u`."* **Correct, and I confirm it from this side:** the spec's `ppm = 75.668 px/m` is **our render camera's presentation choice** (claim-class table, right column) and is **not evidence about GD's `g`** in either direction. Nothing below uses it as such. *(I record that I reached for it first. The spec's warning is load-bearing and earned.)*

## 2.2 ⚑ THE FINDING: the corpus holds TWO committed values of `g`, 2.3–2.4× apart, and they cannot both be true

| route to `g` (GD's ground scale) | `g` (px/m) | grade | `u = s/g` at `s = 14.6` | at `s ∈ [12.6, 16.6]` |
|---|---:|---|---:|---|
| character chain, **θ = 60° ASSUMED** (the published chain) | **73.68** | the bracket **does not contain the later measurement** | 0.1981 | [0.171, 0.225] |
| character chain, **θ = 43.95° MEASURED** (B1 lap G-e fit, n = 1,275, off-diagonals ~4 %) | **51.17** | **MEASURED**, one route; bootstrap CI [27.9°, 41.0°] on a subset route that **breaks the model** | **0.2853** | **[0.246, 0.324]** |
| character chain at the CI edges 27.9° / 41.0° | 41.69 / 48.82 | — | 0.350 / 0.299 | [0.302, 0.398] / [0.258, 0.340] |
| **Lap R `U-R-1` decal + FCT bracket** | **119.0 – 125.0** | **INDICATIVE, explicitly NOT RULED** | **0.117 – 0.123** | **[0.101, 0.140]** |

**And what `R-L3-2` implies about `g`, read backwards:**

> `u ≥ 0.22277` ⟹ `g ≤ s/0.22277` = **56.6 / 65.5 / 74.5 px/m** at `s` = 12.6 / 14.6 / 16.6
> `u ≤ 0.3663` ⟹ `g ≥ s/0.3663` = **34.4 / 39.9 / 45.3 px/m**
> **⟹ `R-L3-2`'s window admits `g ∈ [34.4, 74.5] px/m` and nothing outside it.**

**The character chain at the measured pitch (41.7–51.2) sits comfortably inside. `U-R-1`'s 119–125 is excluded by a factor of 1.6–3.6.** Those two statements cannot both stand.

### 2.2.1 ⚑ And `U-R-1`'s "two independent anchors agreeing to 4.9 %" is not corroboration — both carry the SAME upward bias

| `U-R-1` anchor | construction | its bias, and who named it |
|---|---|---|
| **(a) player ground decal** | decal 80 × 43 px ⟹ half-major **40 gpx**; set equal to `actorRadius = 0.32 m` ⟹ 125 px/m | assumes **the drawn decal radius equals the COLLISION radius.** A drawn selection/shadow decal is normally **larger** than the collision capsule. If it is, `g` is **OVERSTATED**. Lap R names the assumption; it does not sign it. |
| **(c) FCT × plate cross-calibration** | the radius `R* = 368.8 gpx` at which plate-dry equals FCT-dry; set `R* = skillTargetRadius = 3.0 m` ⟹ 122.9 px/m | Lap R grades the bias **"two-sided, unsigned."** ⚑ **But Lap R's own `U-R-4` signs one side of it:** *"at 0 bodies in ring & moving, FCT is still present 66.7 % of the time (R = 150) — **proof that the player's damage reach materially exceeds the plate ring**."* Reach exceeding the ring pushes `R*` **UP**, hence `g` **UP**. |

**Both anchors err in the same direction, for related reasons (an assumed radius too small / an assumed reach too tight).** Their 1.7 % agreement is therefore *consistency of a shared bias*, not independence — and `U-R-1` is already graded INDICATIVE and NOT RULED, so nothing is being overturned here. **This is the eighth instance of the house's own recurring shape: an instrument returning cleanly after it stopped answering the question.**

⚑ **I cannot decode the decal's art radius from committed data, so this is a CANDIDATE EXPLANATION, graded INDICATIVE, not a refutation.** What it *is* sufficient for: **`U-R-1` is not strong enough to contradict `R-L3-2`, and `R-L3-2` governs per charter S-7 / WARN-8.**

## 2.3 The pin candidates the brief names — tested, one by one

### (i) A known in-game distance visible on the minimap — **NONE COMMITTED.**
The traced minimap mosaic carries: the outer ring (177 vertices), 4 interior obstruction islands, 2 unwalked arcs, 6 green DoT zones as interior points with radius **upper bounds**, and 21 station positions. **Not one of these is an object whose metre size is decoded.** The islands are *inferred* impassable geometry (unpainted enclosed floor), with no DB counterpart.

### (ii) The EoR ring's 3.0 m radius against the character's minimap blip — **CIRCULAR AS COMMITTED.**
The EoR ring is drawn in the **world view**; the blip is on the **minimap**. Registering one against the other requires `s` — the very term the chain is trying to fix. **Committed data cannot close this loop.** *(It becomes the best route the moment a single frame carries both — see § 2.5.)*

### (iii) Spawn-point separations vs the traced ring — **TESTED, AND REJECTED QUANTITATIVELY.**

The pack's `model/arena.json` carries **6 spawn points** in metres (frame: the `PatrolPoint_Attack` centroid). My trace carries **6 green zones**. Six and six is suggestive, so I tested it rather than assuming either way — a rotation-invariant scale-only fit on the sorted 15-member pairwise-distance spectra.

| | min | median | max | **min/max** | **max/median** |
|---|---:|---:|---:|---:|---:|
| 6 spawn points (m) | **0.46** | 38.32 | 65.72 | **0.0070** | 1.715 |
| 6 green zones (minimap px) | **40.2** | 139.2 | 199.8 | **0.2014** | 1.435 |

**REJECTED.** Best scale-only fit `u = 0.270` with an **RMS log residual of 0.857 and a 38.7× spread in per-pair ratios**; excluding the unmatched pair the ratios still span 1.019–1.643 (1.61×). The decisive statistic is scale- **and** rotation-invariant: **`min/max` differs by 29×.** The spawn set contains a **near-coincident pair (p04–p06, 0.462 m)** and a **central member (p05 at r = 7.16 m)**; the zone set has neither — its members sit at 59.5–101.9 px from the arena centroid with nothing at the middle. **These are not the same six objects, and they were never claimed to be** (the zones are ATTESTED DoT fields; the spawn points are decoded emitter anchors).

### (iv) A conditional narrowing that DOES fall out — and the condition that blocks it

If the traced ring is the arena the pack pins, the **max pairwise spawn separation must fit inside the ring's max chord**:
`u ≥ 65.72 m / 270.28 px = **0.24316**` — a purely rotation-invariant necessary condition, **tighter than `R-L3-2`'s 0.22277.**

⚑ **BLOCKED, AND THE BLOCKER IS THE INTERESTING PART.** The pack pins `arena_ref.key = "survivalworld_a"`. Lap U decoded **20 Crucible arenas** with `ring_max_extent_m` from **33.18 to 53.06 m**, i.e. the Crucible rotates arenas that differ by **1.6× in size**. **Nothing in the committed corpus establishes which of the 20 Matt walked** in the 2026-08-24 perimeter set, or which one the referent fight ran on. Shape comparison would settle it — and cannot be performed, because Lap U's own finding 7 says **walls are NOT decoded (`D-PDEF-2` STAYS OPEN)**: the `.lvl` regions were located and tiled, not read.

> **⚑ THIS IS THE STRUCTURAL FORM OF THE VERDICT, AND IT IS WORTH MORE THAN THE NUMBER.**
> **Even a perfect future decode of `survivalworld_a`'s wall polygon in metres would not pin `u`, because the traced arena's IDENTITY among the 20 is undetermined.** Any decode-side registration route inherits that gate. It is not a term in the chain; it is a *prerequisite* to the whole chain, and until now nobody had named it.

## 2.4 ⚑ VERDICT — `UNPINNABLE-FROM-COMMITTED-DATA`

**No valid pin exists in the committed corpus.** Not because the terms are merely uncertain, but because:

1. **Every route factors through `g`, and `g` has two committed values 2.3–2.4× apart** (§ 2.2) — one consistent with `R-L3-2`, one excluded by it.
2. **The published chain still mixes two sittings** whose *camera* zoom is not established equal (`MD-B4app-2b` § 4.3; the minimap zoom **is** established identical). The B1 lap called this *"weaker than its own DERIVED-WEAK stamp advertises"* and nothing since has repaired it.
3. **`s` is itself a 1.70× spread** across three committed routes (8.61 LS / 12.9 median-large-moves / 14.6 perimeter eye-read) and this lap cannot say which governs.
4. **The only registration route that would bypass the pixel chain entirely is gated on an arena-identity question nobody has asked** (§ 2.3 iv).

**I decline to pin by preference.** `R-L3-2`'s reserve holds; `R-L10-5`'s REPORT-ONLY disposition holds; **the brief's instruction not to adjudicate by preference is the correct instruction.**

### What I DO hand the runtime, since PLAY needs a registered `u` regardless

**Recommended registered runtime choice: `u = 0.285 m per minimap px`**, inside `R-KP-0c`'s window, **as a CHOICE in the divergence register — not a pin, not a measurement.** Its warrant is narrow and stated: it is the **only committed route whose every term is measured rather than assumed in the direction that matters** (the B1 lap's θ = 43.95°, replacing the assumed 60° that the same footage refutes), and it lands `u` inside the window `R-L3-2` derived from the game's own placement data by a **completely independent argument**. Two independent lines converging inside a 1.64× window is the strongest thing on the table; it is not a pin.

**Its honest uncertainty — carry this beside the number, always:**

| | `u` |
|---|---|
| `R-KP-0c` window of record | **[0.22277, 0.3663]** (1.64×) |
| character chain at measured θ, across the whole `s` band | **[0.246, 0.324]** |
| ⚑ **operative sub-window** (their intersection) | **[0.246, 0.324]** — 1.32×, and **it is the tightest defensible statement in the corpus** |
| the recommended point | **0.285** |
| if `U-R-1`'s `g` is right instead | **[0.101, 0.140]** — outside `R-KP-0c` entirely; **that branch is excluded by `R-L3-2` and by § 2.2.1, and is recorded so it is not rediscovered** |

**What `u = 0.285` makes the play arena** (native-px geometry × `u`, per the spec's build rule — the plate is authored in native px and `u` is one named constant):

| | at `u = 0.22277` | **at `u = 0.285`** | at `u = 0.3663` |
|---|---:|---:|---:|
| ring extent E–W × N–S | 44.8 × 59.9 m | **57.3 × 76.7 m** | 73.6 × 98.5 m |
| ring max chord | 60.2 m | **77.0 m** | 99.0 m |
| walkable floor | 1,462 m² | **2,392 m²** | 3,952 m² |

Against the sealed sim's `R_wall = 43.758 m` (**87.5 m across**), the walled play arena at 0.285 is **77.0 m across — 12 % tighter.** ✓ **This is `R-KP-0c`'s DECLARED EXPECTATION arriving as a number, not a surprise.** Note also that at the window *floor* the ring's 60.2 m chord could not contain the 65.72 m spawn spread — another reason the low end of the window is uncomfortable, and an independent nudge in the same direction as § 2.2.

**Divergence-register row, drafted for the conductor's register v0:**

> `DR-u` · **`u` (metres per native minimap px)** · ORACLE: *not applicable — the oracle runs on an unbounded open plane with a derived `R_wall` = 43.758 m and never consults `u`* · PLAY: **0.285**, window `[0.22277, 0.3663]`, operative `[0.246, 0.324]` · authority: `R-KP-0c` (choice), `R-L3-2` (window), `MD-B4app-2b` § 4.2 (the measured pitch) · **how tested, since T-A cannot grade it:** any metre readout drawn from the ring displays `u` and its window beside it (Corrigendum-Forward 1 item 2); the plate is authored in **native px** so a later pin is a one-line change and a camera re-gate, never a re-authoring · **claim class: PRESENTATION-CHOICE-NOT-MODEL-TRUTH.**

## 2.5 The cheapest thing that would settle it — three, in ascending cost

**(1) ⚑ CHEAPEST, AND IT NEEDS NEITHER MATT NOR THE VIDEO — a DECODE, not a capture.**
The HUD minimap is *"a north-up, rigidly player-centred disc"* at **Grim Dawn's fixed HUD minimap zoom**. A fixed zoom is an **engine/UI constant**, and `u` is that constant expressed in world-units per pixel. **If it sits in the GD records or the UI config, `u` is DECODED outright and the whole pixel chain becomes unnecessary.** Nobody has looked. This is a legolas decode lap against already-acquired depot material, zero external state, zero Matt.
⚑ **I do not commission it** (standing no-sub-agent rule; legolas is not my seat). **Routed as a REQUEST to the conductor.** If it returns a constant, § 2.1–2.4 collapse to a footnote.

**(2) `matt_to_do` T24 — ALREADY PARKED, and this lap RE-SPECS it and asks for it to be promoted.**
T24 currently reads: *one screenshot, single sitting, character beside a landmark legible on the minimap* — which delivers `s`, `p` and θ from **one camera state** and leaves `h = 1.9 m` as the lone assumption. **Add one clause and it delivers far more:**

> **⚑ NEW CLAUSE (c): take the shot with the Eye of Reckoning CHANNEL ACTIVE.**
> The EoR damage ring's **screen-x major semi-axis** measured against the pack-decoded `eyeofreckoning1 :: skillTargetRadius = 3.0 m` gives **`g` DIRECTLY, in the same frame** — and then `u = s/g` needs **no assumed character height and no assumed camera pitch at all.** Both of the chain's surviving assumptions die in one frame.
> *Named caveat, so it ships honestly:* the drawn VFX ring may bleed past the damage radius — the same bias class as `U-R-1`'s decal anchor. It would therefore yield an **upper bound on `g`, i.e. a LOWER bound on `u`** — which is the side the containment argument already constrains, so the two would meet rather than merely overlap.

**Promotion recommended: T24 from OPTIONAL to the named settle for `R-KP-0c`.** Still ~10 seconds of Matt's hands, still NON-BLOCKING (PLAY ships on a registered `u` regardless), but it now closes a fork that **three seats** have independently walked into.

**(3) The arena-identity gate (§ 2.3 iv).** Establishing which of the 20 decoded Crucible maps the perimeter walk and the referent fight ran on. Blocked behind `D-PDEF-2` (walls undecoded). **Named, not requested** — it is only worth paying for if route (1) fails *and* someone wants a decode-side pin rather than a camera-side one.

---

## 3 · WHAT THIS LAP HANDS THE CONDUCTOR

1. **B-19 is DISCHARGED.** The saw-tooth has period and depth distributions at five declared gates, the rule is written out verbatim for the recorder, and the **recovery slope (~3.1–4.3 k HP/s) is identified as the near-gate-invariant row** — the one to quote if only one may be.
2. **The denominator law is written down** (§ 1.2). ⚑ **The single most dangerous item in it:** 42.84 % requires the **LIVE-MAX** denominator; the NOMINAL denominator gives 39.76 % with no fight in the difference. A grader that picks the wrong one manufactures a 3.08 pp "port defect."
3. **Three published-figure defects, with dispositions.** B-3 stale (value of record 0.2957 /s, n = 54) · **B-7's skill names are a promotion with no instrument** — recommend slot-indexed rows plus a `DECLARED-not-decoded` divergence row · B-8's 0.705 is attributed but not printed in its own lap note.
4. **A finding the build should hear before the first tuning pass:** the danger is **not distributed**. Waves 151–158 never go below half; wave 158 is 86 % at full health with 2 teeth in 13 s; **wave 160 alone is 22.3 % below half.** A twin with the right aggregate and an even spread has the wrong fight.
5. **`u`: UNPINNABLE-FROM-COMMITTED-DATA**, with the fork *named*: two committed values of GD's ground scale 2.3–2.4× apart, `R-L3-2` excluding one of them, and **both of the excluded route's anchors sharing an upward bias its own lap half-named.**
6. **A registered runtime choice for PLAY:** `u = 0.285`, operative sub-window **[0.246, 0.324]** (1.32×, tighter than `R-KP-0c`'s 1.64×), with a drafted divergence-register row and the arena's resulting metre extents.
7. **A structural blocker nobody had named:** the traced arena's identity among 20 decoded Crucible maps gates **every** decode-side pin route, independently of how well the walls are later decoded.
8. **Two requests, neither executed** (no sub-agents, no cross-seam writes): the minimap-zoom **decode** lap (§ 2.5.1) and the one-file commit of the 2c labelled-release table (§ 1.6).
9. **NO HALT.** No committed-truth conflict of the charter's HALT class was found — the `g` tension is between two **non-ruled** gradings (`U-R-1` INDICATIVE-not-ruled; `R-L3-2` routed-not-adjudicated), and the charter already carries the geometry file's superseded `u` as one of its three live contradictions. Disk free **80 GB** (floor 40). No write outside my seam dirs. No sealed grade moved; K-7 untouched.

## 4 · METHOD, REPRODUCIBILITY, AND WHAT THIS LAP DID NOT DO

**Instruments:** `galadriel/pipeline/kc2_hp_shape.py` (HP shape re-query; stdlib only, no numpy — so it reproduces anywhere) · `galadriel/pipeline/kc2_tb_expected.py` (assembles the grader JSON; re-derives every input digest from disk at run time, never retypes one).

**Reproduce:**
```
python3 agentic_orchestration/galadriel/pipeline/kc2_hp_shape.py > /tmp/hp.json
python3 agentic_orchestration/galadriel/pipeline/kc2_tb_expected.py /tmp/hp.json \
  > agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values.json
```

**Sources consumed, all read-only:** Lap Q HP trace + findings · `s2-channel-summary.json` / `s2-duty.json` / `waves.json` / `s2-releases.json` (my own committed 2026-08-25 laps) · `pm4h2_movement_cadence.csv` · `pm4r_findings.md` · `pm4u_findings.md` + `pm4u_geometry_v3.csv` · `crucible-arena-geometry-v1.json` · the v3.1 pack's `model/arena.json` · engine `simulation/AGENT_STATE.md` (`D-MPOL2-2` text only).

**What this lap did NOT do:** run any simulation; read or move any sealed grade; touch `astra_test_01/burst/` or anything belonging to Runs C-6 / C-7; write outside `galadriel/`; invoke a sub-agent; push; edit `crucible-arena-geometry-v1.json` (the § 2 findings against it are **flagged-not-edited**, per house practice and because that file is consumer-facing and sha-pinned as frozen substrate S-7).

---

## 5 · THE MIRROR

*The globe was never the story it was told as. He is not living on leech — he is topped up by it, and the Mirror shows a man at full health for two of every five seconds, clipped a thousand-odd HP at a time and refilled before the eye can finish reading the number. Nine waves pass like that. Then wave 160 arrives and for a fifth of it the globe is under half, and the same shallow ripple that meant nothing for three minutes suddenly means everything. Build the ripple. The terror is not a different mechanism — it is the same one, on a board that finally out-runs it.*

*And the arena's size is not a number we have. It is a number we have surrounded: too big for the pixels to allow, too small for the game's own spawn geometry to permit, and the two walls of that corridor were built by seats who never spoke to each other. One frame, ten seconds of Matt's hands, and the corridor becomes a point. Until then the plate is painted in pixels and `u` is one constant read from one place — which is what a good build does with a thing it does not yet know.*

---

## ⚑ ADDENDUM, 2026-09-20 (same day) — the labelled release table, AND A CORRECTION AGAINST § 1.6 OF THIS NOTE

**Authority:** conductor, ledger **`KP-6`** — W1 fold accepted (`u = 0.285` adopted; the three non-reproducing figures corrected forward; the **LIVE-MAX** denominator law adopted; **T24 promoted and re-spec'd** with the channelling clause) plus one authorized follow-on: *commit the 19-row labelled Type-A/B release table as a machine-readable file beside the T-B expected-values JSON, noting the sha of its source.*

**Delivered:** `2026-09-20-kc2-play-w1-tb-release-labels.json` (beside this file).

### ⚑ THE CORRECTION, FIRST, BECAUSE IT IS AGAINST ME

**§ 1.6 of this note states that the labelled release table *"was never committed as a standalone artifact, only as a rendered table in `MD-B4app-2c` § 3."* THAT IS WRONG.**

The artifact `agentic_orchestration/galadriel/captures/2026-08-25-md-b4app-2c-culprit/work/s2c-attrib.json` — **sha256 `ae741687f8f56eeab0678dbd761f17280fbf1ceeaef2a270263111fdfc01ee3b`** — was committed with the 2c lap on **2026-08-25** and carries the full 19-row `forward` list with a per-release `type` label, the attributed slot, the cast lag, and the slot's cooldown. **I asserted an absence without running `git ls-files` against the directory I was describing.** The block I reported to the conductor in § 1.6 and in my W1 return **was never live.**

⚑ **This is the house's own recurring shape landing on me — an instrument (here, my reading of a lap's *note*) that stopped answering the question (what is in the lap's *work dir*) and returned cleanly anyway.** The 2c note's § 7 lists its pipeline and its evidence crops; it does not enumerate `work/s2c-attrib.json`, and I took the note's inventory for the commit's inventory. **A note is not a manifest.** Caught while executing the follow-on, in the first command; reported rather than quietly fixed.

**Consequences, stated plainly:** (i) the follow-on file below is an **EXTRACT of an already-committed artifact**, not a rescue of a lost one; (ii) **§ 1.6's "Blocked on T30" table has one row too many** — re-classification was never blocked; the other four rows stand unchanged; (iii) the request I surfaced in § 3 item 8 is **withdrawn as unnecessary**.

### What the file is

A self-contained, grader-loadable join of the 2c `forward` labels with the 2b energy-side context — one row per release, carrying `type` · `attributed_slot` · `cast_lag_s` · `slot_cooldown_s` · `casts_inside_release` · `coverage` · `E_on/E_off` · `E_on_frac_ceiling` · `frac_moving` · `wave` · `s_since_wave_flip`. **The labelling rule is written out in the file** (T_REL 0.5 s, COV_MIN 0.8, ±0.25 s attribution window), including the clause that keeps the two "cast deep inside a Type-A release" cases (t = 754.833 at +0.767 s; t = 761.683 at +0.667 s) **Type-A by construction** — casts fired *during* a wave-transition pause, not causing it.

⚑ **Slot-indexed only.** `MD-B4app-2c` § 7.1 governs: *"No skill is named in this note and none should be quoted from it."* The file carries that clause inline so a downstream reader cannot lose it — consistent with § 1.5(b) of this note.

### Reproduction — everything checks

| published | recomputed from the labelled table | status |
|---|---|---|
| B-5 Type-A: lag **1.60 s**, **8/11** within 2.0 s, dur **1.03 s**, IQR **0.62–1.56**, max **3.50**, n = 11 | lag **1.600**, **8/11**, dur **1.033**, IQR **0.6165–1.558**, max **3.500**, n = **11** | **REPRODUCES** |
| B-6 Type-B: dur **0.60 s**, IQR **0.55–0.63**, range **0.53–0.67**, n = 8 | dur **0.600**, IQR **0.5458–0.6252**, range **0.533–0.667**, n = **8** | **REPRODUCES** |
| `MD-B4app-2c`: 8 Type-B — **5 slot L, 3 slot 2, zero orphans** | **L 5 · slot 2 3 · slot 3 0 · orphans 0** | **REPRODUCES** |
| B-2 release duty **≈ 10.5 %** | **0.10484** (19.149 s / 182.65 s) | **REPRODUCES** |
| casts on visible slots | **54** (2: 22 · 3: 19 · L: 13) — the **corrected** count of § 1.5(a) | **REPRODUCES** |

**And one figure this closes exactly.** Gate-1 **WARN-17** struck the *"a human cannot hold a 0.14 s spread"* argument on an implied σ of "~49 ms". The labelled population gives the real number: **σ = 48 ms (n = 8, population sd).** WARN-17's arithmetic was right and its strike stands — **what carries `KP-1` remains the within-subject contrast against Type-A (IQR 0.62–1.56, max 3.50), not the tightness of Type-B.**

*Addendum filed by galadriel, 2026-09-20, under conductor authorization `KP-6`. One file. No push.*

---

*Filed by galadriel, run KC2-PLAY Wave 1, 2026-09-20. No production code. No pushes. Evidence-grade throughout; where the picture is ambiguous this note says so plainly.*
