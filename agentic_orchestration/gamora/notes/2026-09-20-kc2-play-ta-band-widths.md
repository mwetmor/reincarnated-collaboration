# KC2-PLAY · T-A BAND **WIDTHS** — the variance half of the prereg

> **STATUS:** CURRENT — W1 return. **Author:** gamora (simulation seam), 2026-09-20.
> **Run:** KC2-PLAY Wave 1 (charter § 4.4, § 5; ledger **KP-4**). **Conductor:** gandalf `RUN-CONDUCTOR`.
> **Companion, cross-pinned by sha at the W1 seal:** `gandalf/notes/2026-09-20-kc2-play-ta-prereg.md`
> (decision rules, decisiveness classes, FAIL taxonomy, denominator law, divergence-register v0 —
> authored in parallel by a gandalf sub-agent). ⚑ **I do not edit that file and it does not edit
> this one** (KP-4's reasoning-boundary ruling: two seats, two files, one seal).
> **Companion math note:** `reincarnated-engine/src/reincarnated/simulation/math/kc2-play-v3p2-lift-prereg-2026-09-20.md` (`dfc0c4a3`).
> **Authority:** widths only. **No simulation executed. No sealed cell re-run or re-graded (K-7)** —
> the M-POL-2 seal was opened READ-ONLY after `shasum` verification and every figure below is
> **derived from its own per-salt cells**, never retyped from a summary.
> ⚑ **Widths are pinned BEFORE any GDScript result exists. This file is IMMUTABLE once committed**
> (charter WARN-16): a change is a new dated version with its reason, never an edit, and a change
> made after a graded run exists is a HALT.

---

## § 0 — Substrate, verified before it was read

| cell | derived sha256 | pinned | state |
|---|---|---|---|
| `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | `ad61ad2a8c799d6e…` | `ad61ad2a8c799d6e…` | **UNCHANGED** |
| `…-mech-20260816_124031.json` | `20b05cb4ef3bd888…` | `20b05cb4ef3bd888…` | **UNCHANGED** |
| `…-w1walls-20260825_220058.json` | `7a992c81ca6e56e5…` | `7a992c81ca6e56e5…` | **UNCHANGED** |

Every band below is computed from `ensemble["M-POL-2"]["0".."4"]` — the **per-salt cells** — and not
from the seal's `⚑ pooled` block. Why that distinction is load-bearing is § 3, and it is the single
most likely way for T-A to fail for a non-reason.

---

## § 1 — THE EXACT ROWS I CERTIFY (no tolerance; pass/fail)

These are structural. They do not get a width, and asking for one would be a category error.

### E-1 · Inertness relations — **certified, by digest**

| arm | `digest_stripped` salt 0 | `digest_full` salt 0 | terminals |
|---|---|---|---|
| `M0` (control) | `226cbf132c46a711…` | `a0c715ee5dffd4f2…` | `[155, 152, 155, 151, 152]` |
| **`M-POL-2-NULL`** (disarmed) | **`226cbf132c46a711…`** | **`a0c715ee5dffd4f2…`** | **`[155, 152, 155, 151, 152]`** |
| `M-POL-2` (the build) | `80ce0ae30b4e95be…` | `6de10192f6ee2261…` | `[156, 152, 151, 151, 156]` |
| `M-POL` (G5) | `a282e799b3f805d7…` | `1047ef65020b8ae8…` | `[151, 151, 151, 151, 151]` |

**`M-POL-2-NULL ≡ M0` byte-exactly on both digests and on all five terminals.** That is the
strongest instrument T-A has: **a port that reproduces the arm's inertness relations proves
STRUCTURE without needing a tape.** The relation is what is graded, not the digest value — a
GDScript runtime will not produce a Python object digest, so the `EXACT` claim is:

> **E-1:** the port's disarmed arm reproduces the port's own control arm **byte-for-byte on the
> port's own digest**, and the port's armed arm **does not**. Three relations: `NULL == M0`,
> `M-POL-2 != M0`, `G5 != M0`.

⚑ **The trap this row exists to catch, named because the run has already been bitten by it:** a
fold that is *supposed* to be off but permutes the RNG stream produces a digest that differs for a
reason that is not the fold. That is `D-I22-1`, and it was found by exactly this relation.

### E-2 · Conservation identity → 0 — **certified, and it has SEVEN terms**

```
offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed
residual → 0   (module tolerance 1e-6)
```

⚑ **Grade on all seven.** A live driver-side assert-wall in this repo recomputes the residual with
**six**, omitting `counterplay_absorbed` — the I-16 `C-I15-4` repair landed in the module and not in
that driver's local copy. Two instruments answer different questions under one name. **A port that
emits six terms and passes a six-term check has passed something that is not the identity.** The
math note § V5 carries the citations; this row carries the consequence.

**E-2 is `STRUCTURAL`:** a non-zero residual means damage is being created or destroyed, which is
not a fidelity difference — it is a broken port.

### E-3 · Coverage — ~~**72 / 72**~~ → ⚑ **89 / 89, gate before grade**

> ⚑ **SUPERSEDED IN PLACE (WARN-6):** the denominator is ~~72~~ → **89**, the ENUMERATED census
> row ids (M 23 · D 19 · P 7 · K 26 · W 14) — ledger **`KP-9`**, jack-ryan W1 pre-read `9e02f5b2`.
> **See ADDENDUM 3 at the foot of this file** for why the 72 does not enumerate. Every band in
> this file is reported as `value @ coverage k/89`. *Annotation in place; the original text
> below is untouched.*

Charter § 4.3. Not mine to compute, but it is `EXACT` and it **gates every band below**: a band
reported without `@ coverage k/`~~`72`~~`89` beside it is not a T-A result. I will not certify a band whose
coverage line is absent.

### E-4 · The constructed denominator — **an identity, checkable**

```
D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE      (PRE_FIGHT and DEAD excluded)
```
Verified on the seal: pooled `287 + 2211 + 166 + 119 = 2783 = D_constructed`. ✓
The per-salt sum equals the pooled sum (2,783), so the partition is exact at both grains.

⚑ **No sealed artifact carries `D`. It is CONSTRUCTED and the seal says so in its own basis
string.** The census's warning stands and is repeated here because it is the cheapest possible
T-A failure: *using a different denominator is the single easiest way to fail T-A for a non-reason.*

---

## § 2 — THE BAND ROWS: how the width is derived

### 2.1 · What the band is a band *of* — declared before any number

The graded object is **the mean of a NEW 5-salt run**, compared against the mean of the sealed
5-salt run. Not an individual salt; not the pooled figure.

The interval is therefore a **prediction interval for a new 5-salt mean**, not a confidence
interval on the sealed mean. Those differ by a factor of √2 and the difference is not cosmetic: a
confidence interval asks *"where is the true mean?"*, and T-A asks *"will a faithful port land
here?"* — which must carry **both** runs' sampling error.

```
half-width = t(0.975, df=4) · s · √(1/5 + 1/5) = 2.776445 · s · 0.632456 = 1.755978 · s
```

with `s` the **sample** standard deviation of the five sealed per-salt values.

### 2.2 · ⚑ `ddof` is a width decision, and I am making it explicitly

Charter § 4.4 quotes the terminal 5-vector *"at σ 2.32."* **That is the POPULATION standard
deviation** (`ddof = 0`). The **sample** standard deviation is **2.588436**.

| estimator | σ | resulting half-width |
|---|---:|---:|
| population (`ddof=0`) — the charter's 2.32 | 2.315167 | 4.065 |
| **sample (`ddof=1`) — what I use** | **2.588436** | **4.545** |

**I use `ddof = 1`, and the band is 10.6 % wider for it.** The five salts are a *sample* from the
seed ensemble, not the population of all possible runs; `ddof = 0` would treat five draws as the
whole world and would make the band **too narrow**, which fails a faithful port. Widening against
my own interest is the only direction in which this choice is safe.

**This is not a correction to the charter.** 2.32 is a true description of the sealed five numbers.
It is the wrong estimator for *predicting a sixth through tenth*, which is what T-A does.

### 2.3 · ⚑ Why the raw per-salt spread is NOT the width — the decomposition

The five salts do not carry equal weight. `D_constructed` per salt is
**[1084, 305, 106, 185, 1103]** — a **10.4× span**. Salt 2 is **106 ticks ≈ 8.7 seconds of fight**.

Every rate statistic (uptime, the state shares, release duty) is a proportion on that denominator,
so each salt carries its own binomial sampling error:

| salt | `D` | uptime | binomial SE |
|---:|---:|---:|---:|
| 0 | 1084 | 0.904059 | 0.00895 |
| 1 | 305 | 0.895082 | 0.01755 |
| **2** | **106** | **0.783019** | **0.04004** |
| 3 | 185 | 0.913514 | 0.02067 |
| 4 | 1103 | 0.900272 | 0.00902 |

Decomposing the observed variance:

| component | variance | sd | share |
|---|---:|---:|---:|
| observed TOTAL (across salts) | 0.00234849 | 0.04846 | 100 % |
| mean WITHIN-salt (sampling) | 0.00049984 | 0.02236 | **21.3 %** |
| implied BETWEEN-salt (model) | 0.00184865 | 0.04300 | 78.7 % |

**Release duty decomposes almost identically: 21.5 % sampling.**

⚑ **So roughly a fifth of the "model variance" the observed spread displays is the salts having
different amounts of fight in them, not the model behaving differently.** And the extremes are
exactly where it bites: the observed uptime minimum (0.783) and the observed release-duty maximum
(0.215) are **the same salt** — salt 2, the 106-tick one, whose own sampling SE is ±0.040.

**What I do with that, and what I refuse to do with it.** I **keep** the sampling noise inside the
band rather than subtracting it out. A new 5-salt run will have its own short salts and its own
binomial noise; a band that removed the sampling component would be a band the oracle itself would
fail about a fifth of the time. **The decomposition is reported so the band's width is understood,
not so it can be narrowed.** Narrowing a band using a variance component that will recur in the
graded run is re-banding with the sign reversed — the defect my own `W1` prereg recorded at `G-6`.

### 2.4 · THE BANDS

All from the five sealed per-salt values of `M-POL-2`. `half-width = 1.755978 · s(ddof=1)`.

| # | row | sealed per-salt values | mean | s | **half-width** | **BAND** |
|---|---|---|---:|---:|---:|---|
| **B-1** | **terminal wave** (5-vector mean) | 156, 152, 151, 151, 156 | 153.200000 | 2.588436 | **4.545** | **[148.65, 157.75]**, clipped below at the ladder floor **151** ⇒ effective **[151, 157.75]** |
| **B-2** | uptime | .904059 .895082 .783019 .913514 .900272 | 0.879189 | 0.054181 | **0.0951** | **[0.7840, 0.9743]**, clipped above at 1.0 ⇒ **[0.7840, 1.0]** |
| **B-3** | `frac_moving` | .857934 .852459 .849057 .881081 .846782 | 0.857462 | 0.013855 | **0.0243** | **[0.8331, 0.8818]** |
| **B-4** | `P(channel \| moving)` | .932258 .923077 .811111 .926380 .942184 | 0.907002 | 0.054094 | **0.0950** | **[0.8120, 1.0020]** ⇒ clipped **[0.8120, 1.0]** |
| **B-5** | `P(channel \| stationary)` | .733766 .733333 .625000 .818182 .668639 | 0.715784 | 0.073452 | **0.1290** | **[0.5868, 0.8448]** |
| **B-6** | plant ratio (window 5.0 s) | 1.442410 1.222222 1.194672 1.102832 1.462250 | 1.284877 | 0.159280 | **0.2797** | **[1.0052, 1.5646]** |
| **B-7** | release duty | .095413 .104235 .214953 .086022 .099188 | 0.119962 | 0.053518 | **0.0940** | **[0.0260, 0.2139]**, clipped below at 0 ⇒ **[0.0, 0.2139]** |

**Per-wave durations (charter § 4.4's second band row):** ⚑ **NOT BANDED HERE — HONEST-FAIL, with
its reason.** The M-POL-2 seal's per-salt cells carry `terminal_wave`, `terminal_reason`, `n_waves`
and the shape/plant/census blocks; they do **not** carry per-wave `duration_s`. The nine
`acceptance.json` rows that *do* carry per-wave durations grade against the **footage** — they are
**T-B rows**, as the census § 3a established, and banding a port against them would measure
port-plus-model-plus-pilot at once, which is precisely what T-A exists to separate. **A per-wave
duration band for T-A requires a sealed emission that does not exist**, and manufacturing one would
mean re-running a cell (K-7). Routed to the conductor: either accept per-wave durations as a T-B
row only, or fire a sibling that emits them. **I do not invent a width for a statistic the oracle
never published.**

**Five-state census (charter's "five-state census stats on the CONSTRUCTED denominator"):** the
four alive states are graded as **shares of `D`**, each with its own band by the same rule. The
pooled shares are `CHANNELLING 0.103126 · CHANNELLING_AND_MOVING 0.794466 · MOVING 0.059648 ·
IDLE 0.042760` and they sum to 1 exactly. ⚑ **Grade the shares, and grade them per-salt-then-mean
(§ 3) — not the raw counts**, which scale with how long the salt survived and would grade fight
length under the name of channel behaviour.

---

## § 3 — ⚑ THE POOLED-vs-PER-SALT HAZARD, AND WHY IT IS THE LIKELIEST NON-REASON FAILURE

The seal publishes **two different statistics under one name**, and the charter's § 4.4 band list
draws from both without saying which:

| statistic | seal's **pooled** | **mean-of-salts** | Δ |
|---|---:|---:|---:|
| uptime | 0.897593 | 0.879189 | **+0.0184** |
| `frac_moving` | 0.854114 | 0.857462 | −0.0033 |
| `P(chan \| moving)` | 0.930164 | 0.907002 | **+0.0232** |
| `P(chan \| stationary)` | 0.706897 | 0.715784 | −0.0089 |
| **plant ratio** | **1.390601** | **1.284877** | **+0.1057** |

Pooling weights each salt by its `D`, so the two 1,000-tick salts dominate and the 106-tick salt
nearly vanishes. **The mean-of-salts weights every salt equally.** Neither is wrong; they are
answers to different questions.

⚑ **On the plant ratio the gap is 0.1057 against a half-width of 0.2797 — 38 % of the whole
tolerance consumed by choosing the wrong one of two numbers that share a name.**

**The rule, registered here:** every band in § 2.4 is a band on the **mean-of-salts**, because the
graded object is a 5-vector and the arms are compared salt-for-salt. **A port's pooled figure must
never be compared against these bands.** The census's own § 3c quotes *pooled* uptime 0.897593 and
*pooled* plant ratio 1.390601; the charter's § 4.4 quotes *per-salt* uptime 0.783–0.914 and
*per-salt* release duty 0.086–0.215. **Both sources are correct and they are not the same
quantity.** A grader that mixes them is running the exact defect my `W1` prereg self-caught at
`G-4` — *"graded a POOLED band against a SINGLE-SALT number"* — and at `G-6`, one wave ago, in
this same seam.

**Requirement on the runtime (for drax, via the conductor):** emit **per-salt** shape statistics
and their denominators, so the grader can form either statistic and is forced to say which.

---

## § 4 — ⚑ WHAT THESE BANDS CAN AND CANNOT DECIDE

Charter § 4.4 declares BAND rows *"individually NON-decisive."* Here is **how** non-decisive,
quantified, because a decisiveness class asserted without a number is a hope.

**B-1, the terminal-wave band, separates NOTHING at n = 5.** Every arm in the seal — including
`M-POL`, the deliberately-different G5 arm — falls inside it:

| arm | mean terminal | inside [148.65, 157.75]? |
|---|---:|---|
| `M0` (control) | 153.00 | **YES** |
| `M-POL-2` (the build) | 153.20 | **YES** |
| `M-POL-2-NULL` | 153.00 | **YES** |
| `M-POL` (G5 — a different policy) | 151.00 | **YES** |

**A band that admits the arm the run built specifically to be different cannot certify a port.** At
σ ≈ 2.6 with n = 5, the terminal wave is a **reporting row, not a gate** — and the seal itself
already says so: its terminal block is labelled `⚑ T1_reported_never_gated`. **This band is
registered as `BAND / NON-DECISIVE / REPORT-ONLY`, and the T-A report must print that sentence
beside the number** so nobody reads "terminal wave in band" as evidence of fidelity.

⚑ **And there is a sharper reason not to gate on it, already measured in this seam.** My `W1`
prereg recorded `Q.10`: **one suppressed motion tick moved a terminal by five waves** (salt 4,
156 → 151), and the fold was exonerated by its own inertness digests. A statistic that moves five
waves on one tick is not a fidelity instrument. It is a fact about this fixture.

**What the bands CAN do, in decreasing order of power:**

| row | discriminating power | why |
|---|---|---|
| **B-3 `frac_moving`** | **strongest band row** | s = 0.0139 — the tightest of the seven, a ±2.4 pp window on a 0.857 mean. The pilot's motion policy is the most reproducible thing in the fight. |
| **B-7 release duty** | usable | ±0.094 on 0.120, but the width is inflated by salt 2 (§ 2.3) |
| B-2 uptime · B-4 `P(chan\|moving)` | weak — both clip at 1.0 | a one-sided band is half a test |
| B-5 `P(chan\|stationary)` | weak | s = 0.073 on a mean of 0.716, and the stationary population is small |
| B-6 plant ratio | weak, and § 3-fragile | widest relative width; the pooled/per-salt gap eats 38 % of it |
| **B-1 terminal wave** | **none** | § 4 above |

**Therefore the T-A verdict's weight sits on the `EXACT` rows — E-1 inertness, E-2 conservation,
E-3 coverage, E-4 the denominator identity — and on B-3.** That is an honest statement of what a
5-salt fidelity grade is worth, and it belongs in the report rather than in a footnote.

**Declared ceiling, carried per charter WARN-14:** without sibling **S5** no sealed cell emits a
per-site draw count, so a stream divergence in the port can be **seen but not located**. With the
math note's finding that there are **29 live draw sites, not 13**, that ceiling is lower than the
charter assumed when it was written.

---

## § 5 — HONEST-FAILS AND WHAT THE CONDUCTOR MUST DISPOSE OF

| # | item | disposition asked |
|---|---|---|
| **W-1** | **Per-wave durations have no T-A band** (§ 2.4). The sealed cells do not carry per-wave `duration_s`; the only per-wave durations in the substrate are the **footage's**, i.e. T-B. | Accept as **T-B-only**, or fire a sibling that emits them. **I will not manufacture a width for an unpublished statistic.** |
| **W-2** | **B-1 is report-only** (§ 4). It admits every arm including G5. | Accept `BAND / NON-DECISIVE / REPORT-ONLY` and require the sentence printed beside the figure. |
| **W-3** | **`ddof` is 1, not 0** (§ 2.2); bands are 10.6 % wider than the charter's σ 2.32 implies. | Noted, not a ruling — but the charter's figure should not be read as a width. |
| **W-4** | **Pooled vs per-salt** (§ 3). Two statistics share five names and the charter's band list draws from both. | Ratify the **mean-of-salts** rule and require the runtime to emit per-salt statistics **with their denominators**. |
| **W-5** | **E-2 has seven terms and a live instrument checks six.** | Grade on seven. (The stale driver is reported, not repaired — repairing it would touch a sealed configuration, K-7.) |

**Cross-pin:** this file and `gandalf/notes/2026-09-20-kc2-play-ta-prereg.md` are pinned to each
other **by sha at the W1 seal**. jack-ryan pre-reads **both** before any graded run exists
(charter § 5, WARN-16). If the decision-rules file assigns a decisiveness class that contradicts
§ 4 above, **the contradiction is a seal item, not something either author resolves alone.**

---

*Widths derived from the sealed per-salt cells, never retyped from a summary. Sealed cells
hash-verified and never re-run (K-7). No simulation executed. Pinned before any GDScript result
exists; immutable once committed. — gamora (simulation seam), 2026-09-20.*

---

# ⚑ ADDENDUM 1 — 2026-09-20, answering the conductor's four W1 reads

> **This is an APPEND, not an edit.** The body above is unchanged and stays the record of what was
> pinned first (corrigenda-forward; WARN-16 — no graded run exists, so an amendment is legal, and
> it is dated and reasoned rather than silent). Occasioned by the conductor's four READ-ONLY items
> against the T-A prereg `gandalf/notes/2026-09-20-kc2-play-ta-prereg.md` (`5f2c27cf`), which I do
> not edit. All four are reads of sealed JSON by key. **K-7 untouched; nothing executed.**

## A1 · (1) THE COMPLEMENT CHECK — **they ARE complements, and the published duty is on a DIFFERENT DENOMINATOR**

The conductor's arithmetic was exactly right, and it found a real defect.

| salt | `D_constructed` | `n_player_ticks_observed` | `PRE_FIGHT` | `n_chan` | `n_released` | uptime | **duty (published)** | u + duty | **released / D** | **u + released/D** |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1084 | 1090 | 6 | 980 | 104 | 0.904059 | 0.095413 | 0.999472 | 0.095941 | **1.000000** |
| 1 | 305 | 307 | 2 | 273 | 32 | 0.895082 | 0.104235 | 0.999316 | 0.104918 | **1.000000** |
| 2 | 106 | 107 | 1 | 83 | 23 | 0.783019 | 0.214953 | 0.997972 | **0.216981** | **1.000000** |
| 3 | 185 | 186 | 1 | 169 | 16 | 0.913514 | 0.086022 | 0.999535 | 0.086486 | **1.000000** |
| 4 | 1103 | 1109 | 6 | 993 | 110 | 0.900272 | 0.099188 | 0.999460 | 0.099728 | **1.000000** |

**Two identities, both asserted over all five salts and both holding exactly:**

```
n_player_ticks_observed  =  D_constructed + PRE_FIGHT          (5/5, asserted)
n_channelling + n_released  =  D_constructed                   (5/5, asserted)
∴  uptime + (n_released / D_constructed)  =  1.000000          (5/5, exact)
```

**The answer:** `uptime` and release duty **are complements — on the CONSTRUCTED denominator**. But
the seal publishes `release_duty` under the key `⚑ release_duty_on_observed_ticks`, i.e. on
`n_player_ticks_observed = D + PRE_FIGHT`. **Two denominators, one salt, one pair of statistics.**

⚑ **The conductor's tell was exact and worth recording**: *"if they were complements the max duty
would round to 0.216–0.217, never 0.215."* On `D` the max duty is **0.216981**. On `observed` it is
**0.214953**. The published 0.215 is the observed-denominator figure. **A third-decimal
disagreement was the visible end of a denominator mismatch** — which is the same class of defect
this note's § 3 was written about, found a second time, in my own band table.

### The restatement, and it changes B-7

**All six denominator-sharing rows are restated to the CONSTRUCTED denominator `D`**, and B-7 moves:

| row | construction, restated | mean | s (ddof=1) | half-width | **BAND** |
|---|---|---:|---:|---:|---|
| B-3 | `frac_moving` = `(CH_AND_MOVING + MOVING) / D` | 0.857462 | 0.013855 | 0.0243 | [0.8331, 0.8818] (unchanged) |
| B-4 | uptime = `(CHANNELLING + CH_AND_MOVING) / D` | 0.879189 | 0.054181 | 0.0951 | [0.7840, 1.0] (unchanged) |
| B-5a | `P(chan\|moving)` = `CH_AND_MOVING / (CH_AND_MOVING + MOVING)` | 0.907002 | 0.054094 | 0.0950 | [0.8120, 1.0] (unchanged) |
| B-5b | `P(chan\|stationary)` = `CHANNELLING / (CHANNELLING + IDLE)` | 0.715784 | 0.073452 | 0.1290 | [0.5868, 0.8448] (unchanged) |
| B-6 | plant ratio (window 5.0 s / fight-wide) | 1.284877 | 0.159280 | 0.2797 | [1.0052, 1.5646] (unchanged) |
| **B-7** | **release duty ON `D`** = `n_released / D` — ⚑ **RESTATED** | **0.120811** | **0.054181** | **0.095141** | **[0.025670, 0.215952]** ⇒ clipped **[0.0, 0.215952]** |

⚑ **B-7's old figures (mean 0.119962, s 0.053518, band [0.0, 0.2139]) were on the observed
denominator and are superseded, named in place.** The width barely moves — but the *construction*
is now the same one the other five rows use, and **the port is told which denominator to divide
by.** That is the whole value: the width was never the risk, the denominator was.

⚑ **A consistency check falls out of the restatement, and it is worth stating because it is free.**
B-7's restated `s` is **0.054181 — byte-identical to B-4's (uptime's)**. It must be: `released/D ≡
1 − uptime` exactly (§ A1's identity), and a constant minus a variable has the same variance. **The
two rows are now provably one row with a sign flip**, which means B-4 and B-7 are **not independent
evidence** and a T-A report must not count them twice. On the *observed* denominator that identity
was broken and the two rows looked independent when they were not — a second, quieter cost of the
denominator mismatch, and the one that would have inflated a fidelity verdict rather than failed it.

*(Transcription note: I first published this row's `s` as 0.054061 and its band as [0.0259,
0.2157]. Both were wrong — a transposed digit — and were caught by re-deriving the figures from the
seal rather than trusting the line I had just written. Recorded rather than silently corrected,
because this file's whole claim is that its numbers come from the cells.)*

**B-3, B-4, B-5a, B-5b, B-6, B-7 are therefore GRADEABLE, not UNGRADEABLE** — the prereg's
conditional is discharged in the affirmative. The construction is restated above and each row now
carries its denominator explicitly.

**Requirement on the runtime (drax), sharpened:** emit `D_constructed` **and** `PRE_FIGHT` **and**
`n_ticks_released` **per salt**, so every rate can be reconstructed on either denominator and the
grader cannot pick one by accident.

## A2 · (2) E-7b — **EXACT**. The class is fixed, before any graded run exists.

Read from the W1 walls seal (`7a992c81…`), `⚑ pools / per_arm`:

| arm | `n_wall_clamps_player` | `n_wall_clamps_body` | `max_body_radius_m` | `n_avoidance_vetoes` | `n_pool_occupancy_ticks` |
|---|---:|---:|---:|---:|---:|
| `W1` | **0** | **0** | 43.404802385345796 | 2 | 0 |
| `W1-NULL` | **0** | **0** | 43.404994665356945 | 0 | 0 |
| `W1-PROBE` | **0** | **0** | 43.404994665356945 | 0 | 2 |
| `W1-SENS` | **0** | **0** | 43.404802385345796 | 2 | 0 |

> **E-7b is `EXACT`.** Both counters are **zero on every arm**. No reclassification to BAND; no
> width is owed.

**Why it is zero, which matters more than the zero:** `max_body_radius_m = 43.4048…` against
`R_wall = 43.758085029822276` — a margin of **0.353 m (0.81 %)**. **The wall never binds.** So
E-7b is not "the port clamped correctly"; it is *"the port never needed to clamp"*.

⚑ **And that makes E-7b a pure falsifier in exactly one direction, extending the prereg's own E-7a
reasoning.** Under the pack's **superseded box** `DS-SPAWN-SCATTER` the reachable radius is
`35.758085 + 8.0·√2 = 47.072` m — **3.31 m ABOVE the wall, with certainty.** A port that implements
the pack's emphatic *"NOT A DISC"* note **cannot** produce zero clamps. **Zero is therefore the
signature of the correct spawn law**, and a non-zero clamp count on the port is a spawn-law defect
reported as a wall statistic. The 0.81 % margin is what makes the test sharp: there is almost no
room between "correct law, never clamps" and "wrong law, clamps constantly".

⚑ **Carried caveat:** because the oracle's counters are structural zeros, **E-7b cannot certify
that the port's wall WORKS** — only that the port does not exceed the wall. A port with no wall at
all also scores zero. The wall's *existence* is checked by R2D geometry probes, not here, and the
T-A report must say so rather than let a green E-7b read as a working wall.

## A3 · (3) B-2 / B-10 / B-12 — **no key path exists. All three are UNGRADEABLE, declared.**

| row | statistic | key path in `[M-POL2]` / `[W1W]` for the arm of record | class |
|---|---|---|---|
| **B-2** | per-wave `duration_s` | ⚑ **NONE.** The only `duration_s` keys in `[M-POL2]` are `ensemble/<arm>/<salt>/⚑ fold/parameters/typeA_duration_s_MEAN` and `typeB_duration_s_MEAN` — **channel-release parameters, not wave durations.** `[W1W]`'s `per_wave` keys sit under `⚑ arena` / `⚑ arena_per_salt` and carry **arena occupancy**, not durations. Per-salt cells carry `terminal_wave`, `terminal_reason`, `n_waves` — and no per-wave duration. | **UNGRADEABLE** |
| **B-10** | arrival latency histogram, co-arrival census, `n_deferred / n_arrived / n_dropped_at_wave_end` | ⚑ **NONE.** `arrival`, `latency` and `n_deferred` are **absent from both seals**. They exist only in `[MECH]`, **a different arm.** Per the conductor's ruling, cross-arm grading measures a configuration difference — the one failure V0 exists to prevent. | **UNGRADEABLE** |
| **B-12** | intake by wave and by damage family; leech healed per tick | ⚑ **NONE.** `intake`, `damage_family` and `leech` are absent from both seals. | **UNGRADEABLE** |

**This confirms and generalises this note's own `W-1`**, which reached the same verdict for B-2
independently, before the conductor's rule was written. ⚑ **B-10's internal half survives
regardless**, exactly as the prereg says: the **seven-term** conservation identity (**E-2**) is
run-internal and needs no oracle side. So the arrival machinery is still gated — on conservation,
not on latency.

**I do not manufacture widths for these three.** A width for an unpublished statistic is a fitted
constant with a confidence interval drawn around it.

## A4 · (4) ARM SET — V0 now configures all five arms

Accepted and implemented. `V0` carries **five `V0-ARM-*` rows** — `M0`, `M-POL-2`,
`M-POL-2-NULL`, `W1`, `W1-NULL` — each stated as a **DELTA against the base row set, never as a
second full copy** (two full copies are two things that can disagree). Each carries its sealed
terminal 5-vector. Landed in
`src/reincarnated/simulation/output/kc2-lifted-rows-KC2PLAY-W1-v3p2-tier1-*.json`.

⚑ **One correction the arm set forces on E-1 as written in § 1 above.** The W1 seal shows
`W1-NULL` terminals `[156, 152, 151, 151, 156]` — **the `M-POL-2` vector, not `M0`'s
`[155, 152, 155, 151, 152]`.** The two NULL arms are inert against **different parents**:
`M-POL-2-NULL ≡ M0` (the channel fold disarmed) and `W1-NULL ≡ M-POL-2` (the arena fold disarmed).
**E-1's three relations become four, and each names its own parent:**

```
E-1a   M-POL-2-NULL  ==  M0          (channel fold disarmed → the control)
E-1b   W1-NULL       ==  M-POL-2     (arena fold disarmed → the build)   ⚑ NOT M0
E-1c   M-POL-2       !=  M0
E-1d   W1            !=  M-POL-2     (terminals [156,152,151,151,151] — salt 4 moves 156 → 151)
```

⚑ **E-1d is the one to watch, and it is this seam's carried miss `Q.10`:** `W1` differs from
`M-POL-2` on **one salt only**, by **five waves**, on **two suppressed ticks** — and the fold is
**exonerated**, because `W1-NULL` and `W1-PROBE` both reproduce the seal byte-exactly. A port that
fails E-1d has not necessarily got the wall wrong; it may have got one tick wrong. **E-1d is
`EXACT` on the RELATION (`!=`) and must never be graded on the magnitude of the difference.**

## A5 · ⚑ A CONDUCTOR PREMISE I MUST CONTRADICT, WITH THE MEASUREMENT

The routing message states: *"the register found THREE known-bad oracle limbs, not two (War Cry
I8_LEGACY, Potion I4_EXCURSION_MAX, LifeMonitor POLL_AT_SLOT)"*, and *"ORACLE keeps auto-fire at
θ 0.49."*

**Two of those three are not in the cell of record, and θ is not 0.49.** V0's trace of the M-POL-2
driver (math note `dfc0c4a3` § 1.2, committed before this message arrived):

| limb | the premise | **the cell of record** | status |
|---|---|---|---|
| War Cry | `I8_LEGACY`, duration 5.0 (the retired invented literal) | **`WarCryLimb.COOLDOWN`, duration 7.5 s** | **NOT-IN-CELL-OF-RECORD** |
| Potion | `I4_EXCURSION_MAX`, θ = 0.49 (measured-falsified 5/9) | **`PotionLimb.TRACE_CONSISTENT`, θ = 0.22972972972972974** | **NOT-IN-CELL-OF-RECORD** |
| LifeMonitor | `POLL_AT_SLOT` | `sustain_procs_fold` **not passed** ⇒ repair limb not installed | ⚑ **LIVE — the one survivor** |

`I8_LEGACY` and `I4_EXCURSION_MAX` are `load_kit()`'s **defaults**, and the driver **overrides
both**. The premise traces to census (c-4), which read the module defaults; V0 is the row-set whose
entire purpose is that `MODULE-DEFAULT` and `DRIVER-OF-RECORD` are different claims about the same
value. **All three are carried in `V0` as `V0-KB-*` rows with their status**, so the register is
complete and correct rather than merely three-long.

**Consequence for V13 (Tier 2) — the instruction is accepted, with its number corrected.** V13 will
carry the potion's **parameters** (800 flat + 25 % instant + 25 % HoT, cd 12.0 s, 1 charge)
**cleanly separable from its θ policy**, exactly as asked, so PLAY can bind it to a manual key with
auto-fire OFF. But the ORACLE arm's auto-fire θ is **0.2297**, not 0.49; θ = 0.49 is the falsified
limb that the sealed cell does not run. **A PLAY-vs-ORACLE divergence row written against 0.49
would describe a divergence from a configuration nobody graded.**

**Routed to the conductor as a correction, not adjudicated here.** It changes a divergence-register
row and the L4 "what this build does not do" page; both are the conductor's.

---

# ⚑ ADDENDUM 2 — 2026-09-20, the three pre-seal reads (prereg v1.1 `30111ac8`, § D concordance)

> **APPEND ONLY.** Nothing above is rewritten; this file is cross-pinned in prereg v1.1 at
> `a7984b79…`. All three are reads — sealed JSON by key, source by grep. **K-7 untouched; nothing
> executed.**

## B1 · (1) BOARD ROLL — **NO. `TA-X-23` is declared OUTSIDE T-A's REACH.**

Swept both seals for roster/class keys (`roster`, `n_bodies`, `n_regular`, `hero`, `nemesis`,
`champion`, `composition`, `n_spawn`):

| seal | per-wave roster counts by class |
|---|---|
| `[M-POL2]` `ad61ad2a…` | ⚑ **ZERO matching keys.** Nothing. |
| `[W1W]` `7a992c81…` | only `n_spawn_placements` / `n_spawn_outside_wall` / `n_spawn_within_half_m_of_wall` under `⚑ arena[_per_salt]` — **a placement TOTAL, not a class breakdown** |

**There is no oracle side to grade against.** `TA-X-23` does not become EXACT; the board roll is
**outside T-A's reach** and the report must say so. ⚑ And the conductor's own reason for refusing
to invent the row is the right one and I second it: **`L-49` — the recorded composition VALIDATES,
IT DOES NOT SPAWN.** Asserting the port's roll against `waves.json` `roster_counts` would assert
against something **the sim does not reproduce either**, so a red would indict the port for the
oracle's own behaviour.

⚑ **What this leaves uncaught, stated plainly:** **12 of the 29 live draw sites are the board roll**
(`wave_engine.py`, V9). It is the mechanism most likely to be rewritten from scratch in GDScript,
its divergence shows up as **a different set of monsters** rather than a different number, and
**T-A cannot see it at all.** `n_spawn_placements` is the nearest available proxy — a per-salt
placement total, which would catch a gross count error and nothing about composition. Closing this
properly is a **sibling that emits per-wave class counts**, not a T-A row.

## B2 · (2) THE TWO OWED WIDTHS

### `TA-B-09` — channel split — **GRADEABLE. It is the TIGHTEST band in the set.**

`CHANNELLING / (CHANNELLING + CHANNELLING_AND_MOVING)`, from the per-salt `census` blocks (both
components are published per salt, so the split exists):

| salt | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| split | 0.115306 | 0.120879 | 0.120482 | 0.106509 | 0.113797 |

> **mean 0.115395 · s 0.005863 · half-width 0.010295 · BAND [0.105100, 0.125689]**

⚑ **`s = 0.005863` is less than half of `TA-B-03`'s 0.013855 — this is now the most discriminating
BAND row T-A has**, and it is the one degree of freedom the four alive-state shares had left. § 4's
power table is superseded on this point: **`TA-B-09` displaces `TA-B-03` at the top.** It survives
the § 2.3 critique too — the split is a ratio *within* the channelling population, so the short-salt
denominator problem bites it far less than it bites `TA-B-02`.

### `TA-B-13` — `max_body_radius_m` — ⚑ **UNGRADEABLE AS A BAND. Declared now, before any graded run.**

W1 per salt: `[43.404802385345796, 41.97652009526441, 41.97652009526441, 41.97652009526441,
41.97652009526441]` — **two distinct values over five salts; four identical.**

| | |
|---|---|
| mean / s / half-width | 42.262177 / 0.638747 / 1.121626 |
| t-based band | [41.140550, 43.383803] |
| ⚑ **the oracle's OWN observed maximum, 43.404802** | ⚑ **OUTSIDE IT** |

**A band that rejects the oracle cannot grade a port.** Two reasons, and either alone is
sufficient:

1. **It is an EXTREME over hundreds of bodies, not a mean.** Maxima do not have symmetric
   sampling distributions, and `t · s · √(2/5)` assumes one. The whole § 2.1 construction is the
   wrong instrument for this statistic.
2. **The per-salt sample is DEGENERATE** — 4 of 5 salts return the identical `41.97652009526441`,
   which is a *structural* value (one particular body's spawn placement plus its own radius), not a
   sampled draw. `s` here measures "did salt 0 happen to roll the one big body", not model variance.

⚑ **And it is already covered, one-sidedly and exactly.** `TA-X-11` / `E-7a` assert
`max_body_radius_m ≤ R_wall = 43.758085029822276` — which **holds on the oracle (43.404802, margin
0.353 m / 0.81 %)** and which **the superseded box scatter cannot satisfy** (47.072 m, 3.31 m over).
**So `TA-B-13` is dropped as a BAND and the one-sided EXACT bound carries its whole falsifying
power.** Nothing is lost; a wrong instrument is removed.

## B3 · (3) ROUNDING — ⚑ **PYTHON BUILT-IN `round` = BANKER'S. GDScript DOES NOT MATCH.**

| | |
|---|---|
| the cadence law | `threat.py:1402` — `max(1, int(round(per / mult * self.ticks_per_s)))` |
| which `round` | ⚑ **the Python BUILT-IN** — no `import numpy` anywhere on the threat / cadence / arrival modules, no `decimal`, no `math.floor(x+0.5)`. Built-in `round` on a float is **ROUND-HALF-TO-EVEN**. |
| corroboration in the seal itself | the M-POL-2 fold's `⚑ quantisation_error` block states the rule in its own words: *"round-half-to-**EVEN** to the nearest whole tick (Python's `round`)"* |
| ⚑ the hazard | **GDScript's `round()` rounds half AWAY FROM ZERO.** `round(2.5)` is **2** in Python and **3** in GDScript. An EXACT row asserting the wrong rule reds a correct port — and worse, a port that uses GDScript's `round()` desynchronises the **threat RNG stream** (V4-LAW-1: the period sets `is_opportunity`, which sets how many `choose_slot` calls draw). |

**Every other half-sensitive site on these paths, so the port can be audited once rather than
debugged five times:**

| site | expression | half-case risk |
|---|---|---|
| `threat.py:1402` | swing period → ticks | ⚑ **LIVE — the cadence law** |
| `threat.py:1522` | `max(1, int(round(s.delay_s × ticks_per_s)))` — first-cast gate | ⚑ LIVE |
| `threat.py:1555` | `max(1, int(round(cd × ticks_per_s)))` — slot cooldown | ⚑ LIVE |
| `threat.py:1867` | `tick + max(1, int(round(r.dot_duration_s × ticks_per_s)))` — DoT expiry | ⚑ LIVE |
| `deferred_arrival.py:330` | `int(math.ceil(raw))` — **arrival tick** | **SAFE** — `CEIL` is the limb of record and is half-insensitive. (`:329`'s `round` is reachable only under `QuantLimb.ROUND`, **not of record**.) |
| `dot_timeline.py:380` | `int(exact) if TRUNCATE_NTICKS else int(round(exact))` | guarded — **`TRUNCATE` is the decoded rule (`R-DOT-2` truncates, never rounds)** |
| `control_application.py:591` | `max(0, int(exact) if TRUNCATE_BUCKETS else int(round(exact)))` | guarded, same shape |
| `counterplay.py:212` | `int(round(x × BAR_PX))` | presentation quantisation only — not on a damage path |
| `threat.py:1424` | `int(sha256(actor_id)[:8], 16) % period_ticks` | **not of record** — the `HASH` phase model; `ENGAGE` is of record (V0) |

> **Recommendation to the conductor, one line:** the port must implement **round-half-to-even
> explicitly** at the four LIVE sites — never GDScript's bare `round()` — and the prereg's EXACT
> rows must assert **banker's**, not "round". This is cheap to state now and expensive to find
> after a red.

---

# ⚑ ADDENDUM 3 — 2026-09-20, the coverage denominator is **89**, not 72

> **APPEND ONLY.** § E-3 above is not rewritten; this supersedes its figure in place.
> Occasioned by jack-ryan's W1 pre-read **NO-SEAL** (`qa/findings/2026-09-20-run-KC2-PLAY-w1-preread.md`, `9e02f5b2`).

**§ E-3's `72 / 72` is superseded: the coverage denominator is `89 / 89`, the ENUMERATED census row
ids, per ledger `KP-9`.** Re-counted from my own census tables this session: **89 ids — M 23 · D 19
· P 7 · K 26 · W 14** — against the headline table's 72.

⚑ **The 72 is mine and it does not enumerate.** It is the headline count *after* collapsing the
~dozen genuinely split rows (`M3`, `M4b`, `D7`, `D11`, `K6`, `K8`, `K15`, `K16`, `K17`, `K25`, `W9`,
`D13/D14`) to their primary class — **and the note never records which id collapses into which.**
So no rule reproduces 17/41/14 = 72 from the tables, and a coverage gate keyed to 72 asks the
runtime to map to a denominator that cannot be reconstructed from the document that defines it.
**The 89 ids govern; the 72 stays as a class-share headline and is not a gate.**

Consequence for this file, stated so no line has to be edited: **every band above is reported as
`value @ coverage k/89`**, and § E-3's refusal stands unchanged in substance — *I will not certify
a band whose coverage line is absent.* Only the denominator moves.

---

# ⚑ ADDENDUM 4 — 2026-09-21 · THE WARRANTS

> **APPEND ONLY. Nothing above is rewritten.** The body and Addenda 1–3 stay the record of what was
> pinned, in the words they were pinned in. Precedent: this file's own Addenda 1, 2 and 3.
> **Author:** gamora (simulation seam). **Occasioned by:** conductor gandalf's dispatch executing
> `gamora/notes/2026-09-21-kc2-play-discrimination-audit.md`, ratified in full.
> **Read-only throughout except this file.** No sealed cell re-run (**K-7 held** — `[M-POL2]`
> re-opened READ-ONLY after `shasum` verification, as the body was). No code, no pack row, no prereg
> row, no oracle value changed. No sub-agent wrote anything.

## ⚑ A4.0 · WHAT THIS IS, AND THE RULE IT HAS TO ANSWER FIRST

**This file's own header says: *"a change made after a graded run exists is a HALT."* A graded run
exists** — run #1, v1.4, `STRUCTURAL @ coverage 89/89`, 2026-09-21. **So I have to say what this is
before I say anything else.**

**A WARRANT IS NOT A WIDTH.** Every sentence below states what an instrument *can and cannot
decide*. **Not one adds an admissible region, removes one, moves a value, a width, a class, a
verdict or a grade.** § 4 of the body — *"WHAT THESE BANDS CAN AND CANNOT DECIDE … a decisiveness
class asserted without a number is a hope"* — **is the same kind of writing, for seven rows. This
addendum extends it to the rest.**

⚑ **AND I DO NOT GET TO RULE MY OWN CHANGE EXEMPT. That is precisely the move the immutability rule
exists to prevent, and a seat that declares itself outside a rule it is subject to has repealed it.**
So, stated as an obligation on the conductor rather than a conclusion of mine:

1. **The disposition is gandalf's, not mine.** If he judges this HALT-class, it reverts as **one
   commit** — the addendum is contiguous and touches nothing above it. *"An escalation overtaken by
   events still requires a disposition; 'resolved by supersession' is a legitimate disposition and
   takes one line; silence is not."*
2. ⚑ **THE PIN MOVES, AND HERE IS ITS BEFORE-STATE, DERIVED THIS SESSION, NOT CARRIED.**
   Prereg v1.5 pins `P-a = 7a5d4aa3305ed14748a903b60ebfe48ac1a186fdb951fb6b8608abba92406750`, and
   `shasum -a 256` on this file **immediately before this append returned exactly that.** After the
   append it is a different file and **v1.5's `P-a` pin is STALE — a `C1` cap condition if a graded
   run were to meet it.**
3. ⚑ **NO GRADED RUN CAN MEET IT, AND THAT IS DERIVED FROM THE PREREG, NOT ASSUMED.** Matt **F3**:
   the last graded run is spent **after** the decode lap and drax's repairs. **F2**: re-base. v1.5
   § H.4 cl. 2: *"the successor prereg (v2.0) is COMMITTED — alone, with every pin re-derived —
   BEFORE the re-based cells are graded."* **The next graded run is post-decode, post-re-base, and
   therefore post-v2.0, and v2.0 re-derives every pin it carries.** The movement is **harmless in
   fact and declared anyway**, because a pin whose staleness is discovered by a cap trip is a pin
   nobody declared.
4. **The same movement is already owed.** `OQ-4` has me minting `TA-B-16…19`'s widths as *"a new P-a
   addendum."* **That addendum will move this pin too.** This one does not pre-empt it: ⚑ **NO WIDTH
   IS MINTED HERE. `TA-B-16…19`'s slots stay NAMED AND EMPTY**, and § A4.4 below says exactly what a
   width for `TA-B-16` would have to be a width *of* before one can honestly exist.

**What this addendum does NOT do, enumerated so nothing has to be inferred:** it mints no width ·
regrades nothing · reclassifies nothing · **does not touch `TA-X-06`'s class, because `OQ-1` is with
Matt and a document that moved it would moot the question instead of answering it** · does not read
drax's seam, so **`TA-X-24` stays bounded exactly as the audit bounded it** · takes **no** upgrade it
discovered (those are § A4.6, flagged and not taken).

## ⚑ A4.1 · THE 17 T-A WARRANTS

**One sentence per row, on the row, in the form the audit's own three model rows already carry
(`TA-X-18` · `TA-X-16` · `TA-X-27`(b)): what the statistic throws away, and a materially different
behaviour that produces the same number.** A **MIS-READ** row also states **what it DOES pin**,
because those rows are misfiled, not worthless, and striking them would discard real evidence.

⚑ **Law 3 held: every alternative named below is already measured somewhere in this corpus, or is
the immediate neighbour of a failure this run has already had. I named none I could not point at.**

### Group 1 — the rows this file itself certifies (§ 1 `E-1`…`E-4`, Addendum 1 `A2`)

| row | ⚑ what the statistic THROWS AWAY | ⚑ a MATERIALLY DIFFERENT behaviour that satisfies it | verdict |
|---|---|---|---|
| **`TA-X-02`** coverage 89/89, zero unmapped *(this file's `E-3`)* | ⚑ **TRUTH.** It counts mappings; it checks none of them | ⚑ **census `M4`, mapped `IMPLEMENTED` with a note describing an implementation that did not exist.** 89/89 was green while one of the 89 was false. ⚑ **DOES PIN: COMPLETENESS** — that no census id is unclassified. Real, and a precondition. It is read as coverage of BEHAVIOUR and it is coverage of PAPERWORK | **MIS-READ** |
| **`TA-X-03`** inertness A — `M-POL-2-NULL ≡ M0` *(`E-1a`)* | ⚑ **the possibility that BOTH arms are identically broken** | ⚑ **a port that never implements the channel fold at all** produces identical digests on both arms and passes perfectly. **Non-discriminating ALONE; discriminating IN COMPANY with `TA-X-05` — and the company is present** | **NON-DISC**, undeclared |
| **`TA-X-04`** inertness B — `W1-NULL ≡ M-POL-2` *(`E-1b`)* | same | same — **and its partner is `TA-X-06`.** ⚑ **If `OQ-1` retires `TA-X-06`, this row is ORPHANED and a port with NO ARENA FOLD AT ALL passes every remaining `W1` EXACT row.** Not an argument to keep `TA-X-06`; **a price tag to read before ruling.** `OQ-1` is Matt's and this row's warrant is not a vote | **NON-DISC**, undeclared |
| **`TA-X-05`** distinctness C — `M-POL-2 ≢ M0` *(`E-1c`)* | ⚑ **magnitude and direction ENTIRELY. It is ONE BIT** | ⚑ **a port whose fold is wrong in every particular still differs from `M0`.** It proves the fold EXISTS. It never says it is right | **NON-DISC**, undeclared |
| **`TA-X-06`** distinctness D — `W1 ≢ M-POL-2` *(`E-1d`)* | ⚑ **everything, in the honest direction** — the row is unfalsifiable except by invention | ⚑ **the only route to green is inventing a veto rule nobody wrote**, and then the row is green about a fiction. ⚑ **DOES PIN: nothing `TA-X-04` does not.** Its entire mechanism is `n_avoidance_vetoes`, which the prereg classed **report-only, no width, no trigger rule**, seven lines away. ⚑ **`OQ-1` IS WITH MATT. NOT ACTED ON IN EITHER DIRECTION** | **MIS-READ** *(prereg-declared § F.2e)* |
| **`TA-X-07`** conservation, 7 terms *(this file's `E-2`)* | ⚑ **THE ALLOCATION AMONG THE TERMS** | ⚑ **a port that drops 30 % of damage and books it as `voided` satisfies conservation exactly**, and the consequence is LIVE: ceiling `C-e` — the port is unkillable and this row was graded on a green identity. ⚑ **Second, sharper, and it is THIS FILE'S OWN `W-5`, still open:** the live assert-wall checks **SIX** of the seven, omitting `counterplay_absorbed`. **A term omitted from a conservation check is a free variable.** ⚑ **And v1.5 § F.2d repaired the TOLERANCE of a row whose defect is ALLOCATION** | **NON-DISC**, undeclared |
| **`TA-X-08`** denominator partition identity *(this file's `E-4`)* | ⚑ **the partition's CONTENT** | ⚑ **a port that classifies every tick `IDLE`** satisfies both sub-identities exactly. ⚑ **DOES PIN: the denominator law** — and it is what resolved the `0.215`-vs-`0.217` tell, which was a real find | **NON-DISC**, undeclared |
| **`TA-X-10`** containment supremum `max_body_radius_m ≤ 43.758085` *(`E-7a`)* | ⚑ **the whole admissible half** | ⚑ **a port that spawns every body at the anchor (`ρ = 0`) passes on every instance**, as does one whose bodies barely move. ⚑ **Its two-sided partner was `TA-B-13`, and THIS FILE RETIRED IT — Addendum 2 § B2, *"a band that rejects the oracle cannot grade a port."* The supremum has stood alone since, and this is the file where it was left alone.** ⚑ **Its falsifying power is REAL and ONE-SIDED, exactly as Addendum 1 § A2 derived:** the superseded box scatter reaches **47.072 m, 3.31 m over the wall**, so zero clamps is the **signature of the correct spawn law**. **It falsifies ONE NAMED WRONG LAW. It certifies no right one** | **NON-DISC**, undeclared |

### Group 2 — the prereg's own EXACT rows

| row | ⚑ what the statistic THROWS AWAY | ⚑ a MATERIALLY DIFFERENT behaviour that satisfies it | verdict |
|---|---|---|---|
| **`TA-X-13`** no player crit `== 0` | presence-vs-absence | ⚑ **a port with NO crit implementation scores zero identically to a correct crit limb at `LO`.** ⚑ **STRUCTURAL ZERO — § A4.2** | **NON-DISC**, undeclared |
| **`TA-X-14`** the two DO-NOTs, both `== 0` | presence-vs-absence | ⚑ **a port with NO release mechanism satisfies both clauses**, and it is **ACTIVELY VACUOUS RIGHT NOW** — the port's Type-A limb is entirely absent, which § A4.4 below measures on the seal. ⚑ **STRUCTURAL ZERO** | **NON-DISC**, undeclared |
| **`TA-X-17`** spawn offset `≤ 8.0` m, every body | the whole admissible half | ⚑ **a port that spawns every body AT the anchor (`ρ = 0`) passes on every instance.** **Non-discriminating ALONE; `TA-X-18` closes it and `TA-X-18` is present** | **NON-DISC**, undeclared |
| **`TA-X-22`** flag-off release cause `== 0` | presence-vs-absence | ⚑ **a port with no interrupts limb scores zero.** ⚑ **STRUCTURAL ZERO** | **NON-DISC**, undeclared |
| **`TA-X-24`** phase model `ENGAGE` — `sha256(actor_id) mod n` **never evaluated** | presence-vs-absence | ⚑ **as stated the assertion is a NEGATIVE, and a port with NO phase model also never evaluates the hash.** ⚑ **STRUCTURAL ZERO.** ⚑ **BOUNDED, DELIBERATELY: if the row carries an unstated POSITIVE limb in the runtime the verdict moves to DISCRIMINATING. I did not read drax's seam and the conductor routes that check** | **NON-DISC**, undeclared |
| **`TA-X-25`** the NO-DATA path, 3 clauses | ⚑ **COMPOSITION** | ⚑ *"proves MEMBERSHIP, never COMPOSITION"* — the run traded a **per-salt discriminator** for a **per-arm one-bit presence test**, the trade was correct, **and the report must not print it as though the discriminator survived.** ⚑ **DOES PIN: per-arm presence, and clause (c)'s structural non-zero.** ⚑ Clause **(a)** `refused == 0` is separately a **STRUCTURAL ZERO** — a port with no refusal limb scores 0 — **declared, at ceiling `C-a`** | **MIS-READ** *(self-declared at `C-a`)* |
| **`TA-X-26`** declared-JOIN conformance, 5 clauses | ⚑ **THE JOIN KEY** | ⚑ **a port that loads the CSV correctly and joins on `display_name` instead of `record` produces a PERMUTATION of multipliers across records — the right multiset, the wrong per-record assignment — and passes all five.** (a)–(d) never look at assignment; **(e) is a MEAN, and a mean is invariant under permutation.** ⚑ **Not invented: 210 of the 7,900 rows carry a comma inside `display_name`**, which already shifted the parse once and landed `0.0` = LEECH-IMMUNE at the multiplier's index. ⚑ **DOES PIN: load, sha, parse SHAPE, single call site, and the armed-set magnitude — all real, none of them assignment.** ⚑ **CLOSED AT § A4.3 with three spanning spot-checks.** ⚑ **And it gains a NINTH structural zero at § A4.2: clause (a)'s identity is satisfied by a port declaring ZERO joins** | **MIS-READ** |

### Group 3 — the diagnostic side

| row | ⚑ what the statistic THROWS AWAY | ⚑ a MATERIALLY DIFFERENT behaviour that satisfies it | verdict |
|---|---|---|---|
| **`TA-B-06`** plant ratio | ⚑ **nothing about the RATIO — the defect is that the two sides computed DIFFERENT STATISTICS** | ⚑ **the oracle's `n_window` is a TICK COUNT (61 per wave); the port's `n_windows` is a WINDOW COUNT (`D/61`). One name, two dimensions.** ⚑ **DOES PIN, on the oracle side: the ratio of two stationary rates, exactly, reproducing all five published values** — the width `[1.0052, 1.5646]` stands as the ORACLE-SIDE reference and a port value cannot be compared to it until the port emits the corrected construction. ⚑ **THE UNDER-SPECIFICATION IS MINE AND THIS FILE IS WHERE IT WAS AUTHORED — see § A4.5, where I ran the neighbour check on my own table** | **MIS-READ** *(prereg-declared § F.3a)* |
| **`TA-B-16`** released ticks per wave | ⚑ **the COMPOSITION of its own numerator** | ⚑ **§ A4.4 — its numerator has TWO GRAINS, and the port's mixture is 100 % of the one that is NOT scale-free** | **NON-DISC**, undeclared |

## ⚑ A4.2 · THE STRUCTURAL-ZERO CLASS, RUN AS A SET OPERATION OVER ALL 27 EXACT CLAUSE-ROWS

**The prereg's § F.5 cl. 6 rule is right and needs no change.** Its remedy sentence — *"Stop
re-discovering the class; make the report print it"* — is also right. **The membership list was
short, and running the question ONCE over the whole set says by how much and, more usefully, WHY.**

### ⚑ A4.2a · THE MEMBERSHIP TEST AND THE RULE DO NOT HAVE THE SAME EXTENSION — that is why the list kept coming up short

| | |
|---|---|
| **the RULE** (§ F.5 cl. 6) | *"every EXACT row satisfied by an **ABSENCE** prints the absence"* — a **SEMANTIC** property |
| **the membership TEST** as the corpus states it | *"for every EXACT row whose assertion is a **ZERO or a NEGATIVE**…"* — a **SYNTACTIC** property |

⚑ **A ZERO IS ONE SHAPE OF SATISFIED-BY-ABSENCE. IT IS NOT THE ONLY ONE.** An **inertness equality**
(`≡`) carries no zero anywhere and is satisfied perfectly by a port that implements nothing. A
**one-sided bound** (`≤`) carries no zero and is satisfied by a port that produces nothing to bound.
**Screening on the syntax finds the zeros and walks past the rest** — which is exactly the history:
four found by syntax, four more found one at a time by reading, and the remainder never found at all.

> ⚑ **THE MEMBERSHIP TEST, RESTATED TO MATCH ITS OWN RULE — and this is the only change the class
> needs:**
> **FOR EVERY EXACT ROW, ASK: DOES A PORT THAT LACKS THE MECHANISM THE ROW IS ABOUT SCORE THE SAME?**
> **Not "is the assertion a zero." That question is about the sentence; this one is about the port.**

### ⚑ A4.2b · THE FULL MEMBERSHIP — one pass, all 27 clause-rows, nothing sampled

| # | clause-row | a port LACKING the mechanism scores… | member? | named where |
|---:|---|---|:--:|---|
| 1 | `TA-X-01` self-determinism | a port with no determinism produces **different** digests | ✗ | — |
| 2 | `TA-X-02` coverage 89/89 + 0 unmapped | 0 mapped ≠ 89 — ⚑ **the zero is BOUND TO A POSITIVE** | ✗ | — |
| 3 | ⚑ `TA-X-03` inertness A | **identical digests on both arms. PASSES** | ⚑ **✓** | ⚑ **NEW** |
| 4 | ⚑ `TA-X-04` inertness B | **identical digests. PASSES** | ⚑ **✓** | ⚑ **NEW** |
| 5 | `TA-X-05` distinctness C | no fold ⇒ no difference ⇒ **fails** | ✗ | — |
| 6 | `TA-X-06` distinctness D | **fails** | ✗ | — |
| 7 | ⚑ `TA-X-07` conservation → 0 | applies no damage ⇒ every term 0 ⇒ **residual 0. PASSES** — and v1.5's relative form and 4,500-term budget both pass at depth 0 too | ⚑ **✓** | ⚑ **NEW** |
| 8 | ⚑ `TA-X-08` denominator identity | runs no ticks ⇒ `0 = 0 + 0` and `0 + 0 = 0`. **PASSES** | ⚑ **✓** | ⚑ **NEW** |
| 9 | `TA-X-09` nine test vectors | **fails** without `math_rules` | ✗ | — |
| 10 | ⚑ `TA-X-10` containment supremum `≤` | spawns at `ρ = 0` ⇒ **inside the bound. PASSES** | ⚑ **✓** | ⚑ **NEW** |
| 11 | `TA-X-11` wall-clamp zeros | no wall ⇒ 0 | ✓ | prereg |
| 12 | `TA-X-12` pool inertness `== 0.0` | aprons absent ⇒ 0 | ✓ | prereg |
| 13 | ⚑ `TA-X-13` no player crit | no crit limb ⇒ 0 | ✓ | ⚑ audit |
| 14 | ⚑ `TA-X-14` the two DO-NOTs | no release limb ⇒ 0, **and it is vacuous TODAY** | ✓ | ⚑ audit |
| 15 | `TA-X-15(a)` p05 at tick 49 | **fails** — a measured positive | ✗ | — |
| 16 | `TA-X-15(b)` no intra-point stagger | unrepresentable ⇒ satisfied | ✓ | prereg |
| 17 | `TA-X-16` p06 OFF | ⚑ **zero BOUND TO a positive (47) AND to a COUNTER. The anti-structural-zero device** | ✗ | — |
| 18 | ⚑ `TA-X-17` spawn offset `≤ 8.0` | no scatter ⇒ every body at the anchor ⇒ **PASSES** | ⚑ **✓** | ⚑ **NEW** |
| 19 | `TA-X-18` scatter-law discriminator | **fails** — three alternatives, input chosen where they separate | ✗ | — |
| 20 | `TA-X-19` arrival unconditionality | no arrival limb ⇒ vacuous | ✓ | prereg |
| 21 | ⚑ `TA-X-21` quantisation + **zero bare `round(`** | no threat path ⇒ **zero bare `round(`. PASSES.** *(Its `CEIL` half's vacuity IS declared; the `zero bare round(` half is not)* | ⚑ **✓ PARTIAL** | ⚑ **NEW** |
| 22 | ⚑ `TA-X-22` flag-off release cause | no interrupts limb ⇒ 0 | ✓ | ⚑ audit |
| 23 | ⚑ `TA-X-24` phase model, as stated | no phase model ⇒ hash never evaluated | ✓ | ⚑ audit |
| 24 | ⚑ `TA-X-25(a)` `refused == 0` | no refusal limb ⇒ 0 | ✓ | ⚑ **NEW as a member; the FACT is declared at `C-a`** |
| 25 | ⚑ `TA-X-26(a)` join-audit identity | ⚑ **declares ZERO joins ⇒ `0 == 0 + 0`. PASSES** | ⚑ **✓** | ⚑ **NEW** |
| 26 | `TA-X-27(a)` zero short-circuits | ⚑ **CLOSED IN COMPANY** — the scan *"censuses every draw-site call and refuses any it cannot classify"*, bound to clause (c)'s **29-site registry**. A port with no sites is caught by (c) | ✗ | — |
| 27 | `TA-X-20` hit-test 2.99 / 3.01 | ⚑ **the negative is BOUND TO a positive on the same row.** No hit test ⇒ fails the hit limb | ✗ | — |

> ⚑ **MEMBERSHIP: 17 of 27 clause-rows. The prereg's § F.5 cl. 6 names 4; the audit added 4; this
> pass adds 9.** *(`TA-X-25(a)` is new as a class member and its underlying fact was already
> declared at `C-a`, so the count of genuinely unannounced members is 8.)*

### ⚑ A4.2c · THE REPAIR IS ONE SENTENCE AND THE CORPUS HAS INVENTED IT FOUR TIMES ALREADY

**Every one of the 10 NON-members fails the test for one of exactly two reasons**, and the second is
a device:

| reason | rows |
|---|---|
| asserts a **POSITIVE** an absent mechanism cannot produce | `TA-X-01` · `TA-X-05` · `TA-X-06` · `TA-X-09` · `TA-X-15(a)` · `TA-X-18` |
| ⚑ **BINDS ITS ZERO TO A POSITIVE ON THE SAME ROW** | `TA-X-02` (0 unmapped **+ 89 mapped**) · `TA-X-16` (0 p06 keys **+ 47 picks + a counter**) · `TA-X-20` (3.01 miss **+ 2.99 hit**) · `TA-X-27(a)` (0 short-circuits **+ a 29-site census that refuses what it cannot classify**) |

> ⚑ **BIND EVERY ZERO TO A POSITIVE ON THE SAME ROW.** A zero says *the mechanism did not fire.* A
> positive beside it says *the mechanism exists.* ⚑ **`TA-X-02`'s 89, `TA-X-16`'s counter,
> `TA-X-20`'s hit limb and `TA-X-27(a)`'s registry census are FOUR INDEPENDENT INVENTIONS OF ONE
> DEVICE, by different authors, at different times, and no document names them as the same thing.**
> **The prereg's own remedy — *make the report print it* — makes the class VISIBLE. This makes it
> SMALLER.** The two compose; neither replaces the other.

⚑ **AND THE STRUCTURAL FINDING ABOUT THE `W1` ARM, WHICH IS WHY `OQ-1`'S PRICE IS WHAT IT IS.**
`TA-X-04` (member), `TA-X-11` (member), `TA-X-12` (member) and `TA-X-24` (member) are four of the
`W1`-facing EXACT rows, and the arm's only non-member is **`TA-X-06`** — the row `OQ-1` proposes to
retire. **The `W1` arm's entire falsifying power currently rests on the one row most likely to be
struck.** *(Reported. `OQ-1` is Matt's and nothing here rules it.)*

## ⚑ A4.3 · `TA-X-26`'s JOIN KEY — three spanning spot-checks, derived against `P-i`

**Derived this session** from `~/Games/reincarnated-engine/data/kc2/pm4p_leech_resistance.csv`
(3,312,159 B; `P-i` = `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e`), parsed with
an RFC-4180 reader. **Every clause-(c) figure reproduces exactly, with no exceptions:** 7,900 data
rows · 790 distinct `record` · **8** distinct `total_leech_resist_pct` `{65, 75, 83, 88, 105, 115,
565, 588}` · **5** distinct `adcth_mult_COUPLED` `{0.0, 0.12, 0.17, 0.25, 0.35}` · all 790 records
wave-invariant (0 violators) · **mean over all 790 = `0.252215`**, median `0.25`, max `0.35`, min
`0.0`, **48** records at exactly `0.0`. ⚑ *Which independently reproduces the prereg's own § F.2a
figures — a third derivation of them, by a third route.*

### Why a MEAN cannot carry this row, stated as arithmetic rather than as an opinion

**A permutation of the multiplier column across records preserves the MULTISET exactly. A mean is a
function of the multiset alone. Therefore the mean is INVARIANT under every permutation** — and so
are clause (c)'s counts, and so are (a), (b) and (d), which never look at assignment at all.
⚑ **Five clauses, and the quantity they all commute with is the one the row exists to check.**

### The three spot-checks — chosen to SPAN the tiers, because that is where a permutation shows

| tier | `record` | `display_name` | `total_leech_resist_pct` | `adcth_mult_COUPLED` |
|---|---|---|---:|---:|
| **MAX** | `records/creatures/enemies/aetherialbloater_a01.dbr` | Aetherial Bloater | `65.0` | **`0.35`** |
| **MEDIAN** | `records/creatures/enemies/devotion/aetherialphantom_h01.dbr` | **`Athraz, the Watcher`** | `75.0` | **`0.25`** |
| **ZERO** *(leech-immune)* | `records/creatures/anomalies/aetheranomaly_01_summon.dbr` | Whirlwind | `565.0` | **`0.0`** |

**Three named records, three different multipliers: any permutation that moves one of them off its
value is caught.** Their per-tier populations are **255 / 367 / 48** of 790, so the three together
also witness that the three largest tiers are populated at all — which a shifted parse disturbs.

### ⚑ AND A FINDING THAT CHANGES WHAT THE SPOT-CHECKS ARE FOR

**The 21 comma-bearing records live in only THREE of the five tiers — `0.12` (9), `0.17` (9), `0.25`
(3) — and NONE at `0.35` or at `0.0`.** The reason is semantic and structural, not accidental:
*"Name, the Title"* is the boss/nemesis naming convention, named bosses carry **higher** leech
resistance, and higher resistance means **lower** coupled multiplier. The `0.35` and `0.0` tiers are
unnamed trash and anomaly/summon entities. **They have no titles, so they have no commas.**

> ⚑ **A TIER-SPANNING SPOT-CHECK AND AN RFC-4180 COMMA SPOT-CHECK ARE NOT THE SAME TEST AND CANNOT
> BE SATISFIED BY THE SAME THREE RECORDS.** Two of the three above **cannot** be comma-bearing; that
> is a property of the data. **A fourth, dedicated parse check is owed** — and `Galakros, the
> Mountain` (`records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr`, resist `83.0`,
> multiplier **`0.17`**) is the natural one: **it is the record the tier gate already caught once,
> it carries the quoted comma, and it covers the fifth tier the three spanning picks do not reach.**
> *(`Galakros` sits at `0.17` and therefore cannot BE one of the three spanning picks — which is
> itself the point: one record cannot serve two independent tests.)*

**Routed as an observation, exactly as the audit routed it. The prereg is immutable and the clause is
gandalf's to author.** The derivation is here so that authoring it costs a paste.

## ⚑ A4.4 · `TA-B-16`'s TWO GRAINS — the numerator PARTITIONED, before any immunity claim

**The prereg marks `TA-B-16` IMMUNE by construction: per-wave over per-wave. § C.6's mechanical test
assumes the numerator has ONE grain.** ⚑ **The seal publishes the partition and it has two.**

**Derived from `[M-POL2]` (`ad61ad2a…`, hash-verified, opened READ-ONLY, K-7 held), keys
`⚑ fold/n_ticks_released_typeA` / `…_typeB` and `⚑ fold/⚑ typeA_wave_census`:**

| salt | `n_waves` | released | **Type-A** | **Type-B** | A / wave | B / wave |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 6 | 104 | **96** | 8 | **16.000** | 1.333 |
| 1 | 2 | 32 | **32** | 0 | **16.000** | 0.000 |
| 2 | 1 | 23 | **16** | 7 | **16.000** | 7.000 |
| 3 | 1 | 16 | **16** | 0 | **16.000** | 0.000 |
| 4 | 6 | 110 | **96** | 14 | **16.000** | 2.333 |
| **mean-of-salts** | | | | | ⚑ **16.0000** | ⚑ **2.1333** |

**`16.0000 + 2.1333 = 18.1333` — which reproduces the published `TA-B-16` figure EXACTLY**, and is
the check that the partition is the right one and not a decomposition chosen to be convenient.

### The two grains, named separately as § C.6 requires

| limb | mechanism | measured | grain | scale-free in `T`? |
|---|---|---|---|---|
| ⚑ **Type-A** | one release per wave transition; `typeA_duration_ticks = 16`, `n_typeA_fired == n_waves` on **5/5**, **zero skipped, zero lost to wave end** | ⚑ **`16 × n_waves`, EXACTLY, on every salt. `s = 0`, `CV = 0`** | ⚑ **per-WAVE** | ⚑ **YES — and not by measurement: by construction, and the construction is visible in the census** |
| ⚑ **Type-B** | cast-triggered, Poisson-ish at `λ_B` per tick | `[1.333, 0, 7.000, 0, 2.333]`, mean **2.1333**, `s = 2.8925`, ⚑ **`CV = 1.356`** | ⚑ **per-TIME** | ⚑ **NO — its per-wave count scales with wave DURATION** |

> ⚑ **A GRAIN IS A PROPERTY OF AN EVENT CLASS, NOT OF A COUNTER.** `TA-B-16`'s numerator is a
> **MIXTURE**, and a mixture is scale-free only where the **composition** is held fixed.
> ⚑ **`TA-B-19` measures ticks-per-wave. It cannot see a composition difference, and § C.6 names it
> as the row that can falsify the immunity claim.** The row that could is a **per-wave release count
> SPLIT BY TYPE** — ⚑ **and the ORACLE side of it has existed, per salt, in the sealed cell, since
> August. The PORT side is what is missing, and its absence is the finding.**

### ⚑ AND THE PART THAT WOULD HAVE READ AS PROGRESS FOREVER IF NOBODY WROTE IT DOWN

**The port has NO Type-A limb** (§ F.3b). Its releases are **100 % Type-B**, over waves **2.985×
longer**. So:

| comparison | oracle | port | miss |
|---|---:|---:|---|
| released ticks **per tick** *(the original)* | `0.120811` | `0.024430` | **4.945×** |
| released ticks **per wave** *(`TA-B-16`, as constructed)* | `18.1333` | `11.76` | **1.542×** |
| ⚑ **like-for-like: a faithful port's expectation at `T = 482`** — Type-A `16.000` (immune) **+** Type-B `2.1333 × 2.985 = 6.368` (dilutes) | ⚑ **22.368** | `11.76` | ⚑ **1.902×** |

> ⚑ **THE 5× → 1.5× IMPROVEMENT IS PARTLY THE NEW CONFOUND CANCELLING THE OLD, AND THE TRUE MISS IS
> LARGER THAN EITHER HEADLINE.** The per-tick form **over-charged** the port (a per-wave numerator
> over a per-tick denominator, inflated by 2.985× longer waves). The per-wave form removes that —
> **and leaves a per-TIME component in the numerator which now scales UP on the port side**, where
> the port's Type-B runs at `11.76 / 6.368 = 1.847×` the faithful expectation. **That inflation
> pushes the port's total toward the oracle's and makes the miss look SMALLER.**
> ⚑ **`1.542×` is neither the artefact nor the truth. It sits between two live errors of opposite
> sign.** The prereg's own § C.6 warned that *"swapping one un-audited invariance claim for another
> is how this defect would survive its own repair."* **It did.**

⚑ **AND THIS IS WHY NO WIDTH IS MINTED FOR `TA-B-16` HERE.** `OQ-4` asks for one. **A width over a
mixture whose composition differs between the two sides would be a width over an undefined
quantity** — and the honest construction is **two rows, `TA-B-16a` (Type-A per wave) and `TA-B-16b`
(Type-B per wave)**, of which the first has `s = 0` on the oracle and **needs no band at all** (it is
an EXACT structural constant, `16 × n_waves`), and the second needs the port to emit a split it
currently cannot. **Stating that is within a warrant's scope. Minting either is not, and authoring
the row is gandalf's.**

## ⚑ A4.5 · THE NEIGHBOUR CHECK, RUN ON MY OWN TABLE — and it returns exactly one row

The conductor's standing instruction: *"when you write a warrant, check whether the row beside it
needs the same one."* **Run against § 2.4 / Addendum 1's seven band rows, asking only: does the row
state its statistic as a FORMULA, or as a LABEL?**

| row | how the construction is written |
|---|---|
| `B-3` `frac_moving` | `(CH_AND_MOVING + MOVING) / D` — **formula** |
| `B-4` uptime | `(CHANNELLING + CH_AND_MOVING) / D` — **formula** |
| `B-5a` `P(chan\|moving)` | `CH_AND_MOVING / (CH_AND_MOVING + MOVING)` — **formula** |
| `B-5b` `P(chan\|stationary)` | `CHANNELLING / (CHANNELLING + IDLE)` — **formula** |
| ⚑ **`B-6` plant ratio** | ⚑ **`(window 5.0 s / fight-wide)` — A LABEL** |
| `B-7` release duty | `n_released / D` — **formula** |
| `B-1` terminal wave | a raw 5-vector; needs none |

> ⚑ **SIX OF SEVEN CARRY A FORMULA. THE ONE THAT CARRIES A LABEL IS THE ONE THAT FAILED — and the
> tell was visible in the shape of my own table, months before the port and the oracle computed two
> different statistics under one name.** The under-specification was mine; I declared it at the
> grade; **what I had not done was ask the same question of the six rows beside it.** The check costs
> one pass over a table I wrote, and it is the only known remedy for this shape.

## ⚑ A4.6 · FLAGGED SEPARATELY — upgrades found while writing warrants, and NOT TAKEN

**A warrant that quietly repairs its row is not a warrant; it is a change with no review.** Each of
these is cheap, none is in this addendum, and each is routed:

| # | the upgrade | why it is not here |
|---:|---|---|
| **1** | ⚑ **`TA-X-26` clause (c) should assert the PER-TIER RECORD COUNTS — `0.0`→48, `0.12`→43, `0.17`→77, `0.25`→367, `0.35`→255** (derived, § A4.3). Far stronger than *"5 distinct values"*: a permutation preserves the vector, **but a SHIFTED PARSE does not** | a new assertion on an immutable row. **gandalf's** |
| **2** | ⚑ **`TA-X-26` clause (a) needs a STRUCTURAL NON-ZERO** — `n_declared ≥ 1`, or better the declared join set's own cardinality. **As written, a port declaring no joins passes the identity `0 == 0 + 0`** (§ A4.2b row 25) | same |
| **3** | ⚑ **`TA-X-04` needs a positive limb before `OQ-1` retires `TA-X-06`** — any observable the arena fold changes, or the `n_avoidance_vetoes` counter `TA-B-14` already reports | **Matt's**, via `OQ-1`. **Not acted on in either direction** |
| **4** | **MO-4's observation window widens from wave 1 / 40 ticks to the declared 10-wave scope** — one argument | engine-side; a separate change, flagged in its own warrant |
| **5** | ⚑ **`TA-B-16` splits into `16a` / `16b`** (§ A4.4) | authoring a row is the prereg's. **gandalf's** |

## ⚑ A4.7 · THE SEVEN T-B WARRANTS — AUTHORED HERE, OWED TO `P-b`, AND I CANNOT FILE THEM MYSELF

⚑ **A BOUNDARY I AM DECLARING RATHER THAN CROSSING.** The dispatch asks for the warrant **on the
row**. For these seven the row lives in **`galadriel/notes/…-w1-tb-expected-values-and-u-rider.md`
and its JSON** — **another seat's instrument, pinned into the prereg as `P-b` / `P-c` / `P-d`.**
Writing into it would be a cross-seam edit of a sha-pinned artifact belonging to a seat live in this
run, and **no dispatch authorized that.** So the sentences are written, and **the fold into `P-b` is
galadriel's, routed through the conductor.** *(This is drax's `TA-X-06` handling, one seam over:
declare the absence, name the consequence, route it, do not fill it.)*

⚑ **A framing that must travel with all seven, because galadriel's own note usually ships it and
nothing on the individual rows says so:** these are **non-discriminating ALONE and discriminating IN
COMPANY**, and the company — `TB-HP-10`'s six order statistics and five-gate sweep, `TB-HP-11`'s
localisation, `TB-HP-12`'s per-wave table — **is present in the same note.** *The rows are right; the
READING is what fails.* galadriel says it herself: *"A twin that spreads its danger evenly across ten
waves has the right aggregate and the wrong story."*

| row | value | ⚑ THROWS AWAY | ⚑ a MATERIALLY DIFFERENT behaviour that satisfies it |
|---|---:|---|---|
| **`TB-HP-01`** time at full | `0.428414` | ⚑ **all time-structure** | a twin at full for the first 77.5 s and never again. ⚑ **And the row's dominant uncertainty is its own DENOMINATOR, not its read: `0.4284` (LIVE-MAX) vs `0.3976` (NOMINAL), a 3.08 pp gap with no fight in it** — galadriel states this; the row's warrant is that a comparison quoting one figure has not said which |
| **`TB-HP-02` / `-03`** below 90 % / 75 % | `0.212319` / `0.090231` | same, **and both are denominator-SENSITIVE** | same. Rescued in company by `TB-HP-12`'s per-wave table |
| **`TB-HP-04` / `-05`** below 50 % / 33 % | `0.034619` / `0.010036` | time-structure *(denominator-INSENSITIVE — a real strength, and it is stated)* | ⚑ **galadriel names the alternative herself.** ⚑ **And `TB-HP-11` FALSIFIES it on the referent: all 8 sub-half excursions are in waves 159–160; waves 151–158 never go below half at all** |
| ⚑ **`TB-HP-06`** below 25 % | **`0` frames** | ⚑ **a ONE-SIDED BOUND — the whole admissible half** | ⚑ **THE PORT ALREADY SATISFIES IT AND IT IS THE RUN'S LARGEST KNOWN DIVERGENCE.** `terminal_reason = cleared` 25/25, HP never below **79.44 %** (ceiling `C-e`). ⚑ **AN UNKILLABLE TWIN PASSES THIS ROW.** Its two-sided partner exists — `TB-HP-08`'s floor at 26.79 % — **and is not bound to it** |
| **`TB-HP-07`** frames decreasing | `0.137293` | **magnitude and clustering** | one huge hit/s vs many tiny hits/s at matched cadence. Rescued in company by `TB-HP-10`'s depth distribution. *(Its `n` vs `n−1` ambiguity is declared and both print 13.73 %; the row says to use `n−1`)* |
| **`TB-HP-08`** HP minimum | `5,360` (26.79 %) | ⚑ **an EXTREME over n draws — the body of the distribution; and it scales with n** | any distribution whose worst single frame lands at 26.79 %. ⚑ **THE SAME CLASS AS `TA-B-13`, WHICH THIS FILE RETIRED AS UNGRADEABLE AT ADDENDUM 2 § B2 FOR EXACTLY THIS REASON — and nothing on `TB-HP-08`'s face says so.** *(It is not proposed for retirement: as an absolute floor beside `TB-HP-06`'s zero it is the two-sided partner that row lacks. It is proposed for LABELLING)* |
| **`TB-HP-14`** leech cadence | `11.408 /s` in `[11.387, 12.250]` | bracket-membership throws away **where in the bracket** | ⚑ **the measured value lands `0.021` above the bracket's LOW EDGE on a `0.863`-wide bracket — a 2.4 % margin.** Inside-a-bracket reads as corroboration; **at the edge it is one small bias from being outside**, and nothing on the row's face says which. *(Its per-body heal limb is already declared an UPPER bound — correctly handled, and the contrast is the point)* |

---

*Addendum 4 filed 2026-09-21 by gamora (simulation seam), Run KC2-PLAY, executing the conductor's
dispatch on the ratified discrimination audit. **APPEND ONLY; nothing above rewritten.** **NO WIDTH
MINTED — `TA-B-16…19`'s slots stay named and empty, and § A4.4 states what a `TA-B-16` width would
have to be a width OF before one can honestly exist.** **Nothing regraded, reclassified or widened;
`TA-X-06` untouched because `OQ-1` is Matt's; `TA-X-24` left bounded because I did not read drax's
seam.** **K-7 held** — `[M-POL2]` hash-verified and opened read-only, never re-run. **Law 3 held.**
⚑ **THIS FILE'S SHA HAS MOVED: prereg v1.5's `P-a` pin `7a5d4aa3…` was verified current immediately
before this append and is now STALE. v2.0 must re-derive it (§ A4.0 cl. 2–3).** No push.*
