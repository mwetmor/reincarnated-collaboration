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

### E-3 · Coverage — **72 / 72, gate before grade**

Charter § 4.3. Not mine to compute, but it is `EXACT` and it **gates every band below**: a band
reported without `@ coverage k/72` beside it is not a T-A result. I will not certify a band whose
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
