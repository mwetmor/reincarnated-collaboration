# WR1-2026-07-28 — GRADING RECORD (G-A · G-B · M-8a)

**Status:** CURRENT · **Date:** 2026-07-29 · **Author:** gandalf (RUN-CONDUCTOR)
**Run:** WR1-2026-07-28 (wave-relay autonomous run) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md`
**Authority:** conductor grades under R-WR1-17 (Matt, "1) Yes.") — grading, baton emission and the
R-WR1-6 hold execute from the charter session. Grades are RULED, not open: R-WR1-18 (Matt, verbatim
*"Ratify all three."*) pre-registered P-1 / P-2 / P-3 as gate law before any number was graded.
**Substrate:** `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/`
(450 traces + `wr1_battery2_statistics.json`), read-only.
**Gate-2 of record:** `agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr1-battery.md`
(landing review + independent second-pass addendum + re-check parts §R1–§R12, verdict **CLEAR**).

> **What this document is.** The graded verdict of record for WR1's three pre-registered gates. It
> also executes the WARN-4 correction (§A-4 below) — the correction of record, because one of the
> three erroneous sites sits inside an SS-1-frozen artifact that must never be edited.
>
> **This record supersedes, of-record, the string
> `H_B2_6_FINDING.boss_decomposition.warning_to_the_grader` in
> `wr1_battery2_statistics.json`.** That artifact stands unedited and flagged known-wrong.

---

## §0 — GRADES AT A GLANCE

| gate | grade | one-line basis |
|---|---|---|
| **G-A** — mitigation moves worst-case damage across the gear step | **MISS** | bracket `[1.0000, 2.2700]`; the endpoint's 2.2700 decomposes as `1.1350 × 2.0000` and the gear component is **1.1350 < 1.50** |
| **G-B** — acceptance symmetry (killable at the death band · win reachable) | **PASS** | killable ✓ (`P(D ≥ 543) = 1.000`, all three regimes, n = 16/16 at r ≤ 1.26 m); win reachable ✓ (14/30 pre-leg) — **with a reported attribution surprise** |
| **M-8a** — is Battle Surge's absence load-bearing? | **FLIP on both pre legs; no flip on post** | pre 0/30 → 14/30 · endpoint 0/30 → **2/30** · post 30/30 both. Legs disposed **separately** per P-3 / R-M8-1 |

**G-A closes at the MISS.** No mitigation-remediation lap fires inside WR1 (P-1). The measured
source-side reason *is* the finding and routes to the wave tail.

---

## §1 — G-A: **MISS**

### 1.1 The literal bracket, as the estimator emitted it

Estimator: **nearest-rank p99, 1-based, `k = ⌈0.99m⌉`**, fixed in math note §2.3 **before any
measurement** and unchanged by the halt, the ruling, or this grading lap. No estimator switch was
made at any point — including at the moment a switch to `max` would have produced 1.1350 cleanly.

| tier | pre → endpoint (`ratio_p99`) | `ratio_max` (endpoint) | m (pre / post / endpoint) | cadence grade |
|---|---|---|---|---|
| trash | 1.0000 → **1.0000** | 1.0000 | 264 / 263 / 264 | **C** |
| champion | 1.0000 → **1.0000** | 1.0000 | 180 / 179 / 180 | **C** |
| mixed_pack | 1.0000 → **1.0696** | 1.0682 | 519 / 480 / 519 | **C** |
| **boss** | 1.0000 → **2.2700** | **1.1350** | 1828 / 2206 / **1334** | **M** |

**Bracket of record: `[1.0000, 2.2700]`.** The low end is the gate-adverse R2 point reading
(cold 0.14); the high end is the pre-named `R2_proxy_resists_low` endpoint (cold 0.00). The two are
**two readings of one bracketed quantity and are never pooled** (R3J L-1). The predicate is quoted
verbatim and untouched:

> **R-WR1-7: PASS iff `W_pre / W_post ≥ 1.50`.**

**No goalpost moved. The predicate text is not amended.**

### 1.2 Both halves, stated explicitly — the rubric-law requirement

A future reader who re-runs the predicate against the banked artifact will compute `2.2700` and see
it clear `1.50`. That reader must find this record saying **both** of the following. Omitting either
channel is the WARN-A failure shape (a record dropping a channel it carries), inverted.

**(i) THE ARITHMETIC CONDITION WAS MET AT THE ENDPOINT BOSS FACE VALUE.**
`2.2700 ≥ 1.50` is TRUE. This is not disputed, hedged, or estimator-shopped away. At the bracket's
upper endpoint the pre-registered statistic, computed by the pre-registered estimator, clears the
pre-registered threshold.

**(ii) IT DOES NOT ANSWER THE OWNER'S QUESTION.** The owner's question — the one the gate exists to
answer — is *how much does the R2 → R3 **gear step** move worst-case incoming damage?* The endpoint
figure is not a measurement of that. It decomposes **exactly**, computed rather than narrated:

```
2.2700  =  1.1350          ×  2.0000
           gear step          realized-count p99 RANK step
```

- **1.1350** — `(35.40 + 172.00/0.86) / 207.40`, the mitigation operator's own response to
  cold `0.14 → 0.00`. **Identical at every realized count.** Pre-registered in closed form at math
  note §10.2 *before the endpoint leg existed as an object*.
- **2.0000** — **not a damage effect. A rank artifact.** The endpoint's larger per-projectile
  payload shortens the boss fight, the received-event pool falls `1828 → 1334`, and the 1 % cut
  therefore lands on a **2-projectile** crossing where the point leg's landed on a **1-projectile**
  crossing. Proven by the payload-quantum histogram, which Gate-2 computed rather than inferred:

  ```
  delivered ÷ unit payload, boss-tier nova crossings, all 44 per leg:
    point    (unit 207.40)  ->  {1.0: 30, 2.0: 14}
    post     (unit 207.40)  ->  {1.0: 30, 2.0: 14}
    endpoint (unit 235.40)  ->  {1.0: 30, 2.0: 14}
  ```

  Every crossing delivers exactly 1× or 2× the unit payload. **The factor is the integer projectile
  count and nothing else — geometry, not HP.** The 14 two-projectile crossings sit on the same seven
  seeds (`…802, 805, 807, 809, 810, 818, 825`) on **all three legs and both arms**: the mitigation
  regime moves the payload per projectile and moves nothing about multiplicity.

**Intent grades on the gear component: `1.1350` vs `≥ 1.50` → MISS.**

**And the direction of the error matters.** The endpoint's larger payload is *itself* what shrinks
the pool. Grading 2.2700 at face value would partially **double-count the payload increase through
the estimator** — it is not a neutral estimator quirk, it inflates in the gate's own favour.

### 1.3 Four corroborations that the gear step is 1.1350

1. **Independent Gate-2 re-derivation.** jack-ryan recomputed G-A from the 450 banked traces with a
   nearest-rank p99 written from the math note's *words*, touching neither builder nor conductor
   code. Every cell reproduces to the digit (`235.40/207.40 = 1.135005` × `470.80/235.40 = 2.000000`
   = `2.270010` = measured). Two independent passes; both reached *"report the literal bracket
   `[1.0000, 2.2700]`, grade intent on 1.1350, name the rubric, never switch estimators"* unprompted.
2. **The endpoint's own arm B reads `1.1350` raw.** Arm B's pool (794) is large enough that the 1 %
   cut never reaches the 2-projectile crossings; arm A (pool 540) reads 2.2700. **The same leg, the
   same gear step, reads the pure gear step under a slightly larger pool.** This is a *measured
   instance*, not an inference — and it arrived as the falsification of a conductor claim
   (Gate-2 WARN-2, "arms give the same ratio", corrected with an erratum banner). The falsification
   *is* the corroboration.
3. **The pre-registered disagreement instrument fired at this cell.** `p99_and_max_ratios_agree`
   exists in the artifact precisely so a p99 sitting on a different mechanism from the max is
   visible without anyone looking for it. At boss/endpoint it reads `false` with
   `p99_over_max_ratio: 2.0` — an exact integer — and `p99_equals_max: true`. **See §A-5 for a
   correction to the charter's "here and nowhere else" wording; the substance stands, the scope
   claim did not.**
4. **The flip point is computable and razor-thin.** With `rank_from_top(m) = m − ⌈0.99m⌉ + 1`:

   | m | rank from top | endpoint p99 |
   |---|---|---|
   | 1200 – 1299 | 13 | 470.80 |
   | **1300 – 1399** (banked: **1334**) | **14** | 470.80 |
   | **1400** | **15** | **235.40** |

   **A boss received-event pool ~4.95 % larger (1334 → 1400) collapses the endpoint p99 from 470.80
   to 235.40 and the headline ratio from 2.2700 to 1.1350.** One-sided — a smaller pool leaves it at
   470.80. A headline that a 5 % pool change deletes is not a measurement of a gear step.

### 1.4 The measured source-side reason — this IS the finding (P-1)

The MISS is **not a tuning miss**. It was **predicted in closed form in the math note §10.2 before
the run**, and the mechanism was then measured rather than inferred:

- **Armour is saturated in both regimes.** The nova's physical leg delivers **118.0 per projectile**,
  which is below **both** candidate armour values. The operator has no room to respond.
- **Cold reads 0.14 in both the R2 point vector and the R3 vector.** The only channel that could
  move does not differ across the gear step at the graded point.
- **62.9 % of the payload is immobile across the gear step.**
- The remaining move is available only at the bracket's cold-0.00 endpoint, and there it is
  **1.1350** — a 13.5 % move against a 50 % requirement.
- **Danger in this fixture was situational, not statistical.** The boss fight's lethality lives in
  the once-per-fight nova crossing (§B-4), not in a distribution the gear step reshapes.

**P-1 consequence, Matt-ratified:** the MISS **CLOSES G-A for this run**. No
mitigation-remediation lap fires off it inside WR1. **The finding routes to the wave tail.**

**P-2 statement, Matt-ratified — settled direction, not an open question:** the **2.12
danger-signature ambition is RETIRED from the mitigation ledger** and **RE-REGISTERED as an
encounter-composition target** — boss-encountered-before-the-gear-plateau scenario modeling, in
KIT-CAL / wave vocabulary, on a future lap. The mitigation operator was never the instrument that
could deliver 2.12 against a saturated-armour payload; encounter composition is.

### 1.5 Caveats carried with the G-A grade

- **INFO-7 — `a_dmg_1_grain` is a SINGLE-CONFIGURATION measurement.** All 44 nova crossings per leg
  resolve at **one** geometric configuration: measured from the telegraph origin, every boss
  crossing in every fight lands at `t* = 1.9512 s` at the same radius. The falsifier's 132
  pre-flight crossings are therefore **one configuration sampled 132 times, not a sample over
  geometry.** The pin is fully live against the thing it is aimed at (payload-model inflation — it
  fires at ~+26 %); it is **not** a distributional bound and must not be read as one. Not a defect —
  a scope statement.
- **INFO-4 — `headroom_pct` denominators, named at every quotation in this record.**
  `A_DMG_1_preflight.headroom_pct` and `a_dmg_1_grain.pin_headroom_pct` carry the
  **inflation-tolerance** convention: **`(260.50 − worst_per_projectile) / worst_per_projectile`**.
  Quoted values under that denominator: **25.6027 %** at both point regimes (worst 207.40) and
  **10.6627 %** at the endpoint (worst 235.40). The *complement* convention — "margin below 260.50",
  `(260.50 − worst) / 260.50` — reads **9.64 %** at the endpoint and appears in math note §9.2 and
  in the `gd_mitigation.py` comment. **Same word, two denominators.** Wherever this record quotes
  headroom it quotes the inflation-tolerance form and says so.
- **132-crossings-one-geometry.** Restated as its own caveat because it bounds every headroom claim
  above: headroom is a single-configuration measurement, **not** a distributional bound.
- **A-M4-3 — three of four tiers carry a grade-C class-band assumption.** Non-boss swing-pause
  cadence is a *class-band* assumption, not a per-record measurement. `cadence_grade` in the
  artifact reads **C** for trash, champion and mixed_pack; only **boss** reads **M** (measured).
  All three grade-C tiers returned `1.0000` on both bracket legs, so the assumption is not
  load-bearing on the MISS — but it is load-bearing on any future claim that those tiers were
  *unmoved* rather than *unmeasured*.

---

## §2 — G-B: **PASS** (graded on OUTCOMES, per P-3)

P-3 (Matt-ratified) fixes the rubric: **G-B grades on outcomes** — no-evasion player killable at the
death-2 band ✓ / win reachable ✓ — with the attribution surprise **reported in the grade**, not
graded on.

### 2.1 Leg 1 — killable at the death-2 band ✓

Instrument: the **resolver's own** functions (`nova_substream` / `draw_spoke_offset` / `n_realized` /
`nova_delivered`) — one source, three consumers (gd_nova §7.1). Probe radius **r = 1.26 m** pinned by
WR1-GAL-3; band edges `[0.96, 1.61]` @95 %.

| cell | realized count | delivered (max) | `P(D ≥ 543)` | support max ≥ floor |
|---|---|---|---|---|
| pre @ 0.96 / **1.26** | **16 / 16** (min = max = expected) | 2080.348 | **1.000** | ✓ |
| post @ 0.96 / **1.26** | **16 / 16** | 2069.148 | **1.000** | ✓ |
| endpoint @ 0.96 / **1.26** | **16 / 16** | **2304.348** | **1.000** | ✓ |
| pre / post / endpoint @ 1.61 (band edge) | 6–7 | 775.348 / 764.148 / 873.348 | **1.000** | ✓ |

- **n = 16/16 at r ≤ 1.26 m** — at the fixture's death radius the 16 rays sit 0.49 m apart and
  multi-hit is **geometrically forced**; the realized count is deterministic, the seed drops out.
- **`P(D ≥ 543) = 1.000` on all three regimes** and at all three probe radii including both band
  edges. The one-frame floor is 543 HP.
- **Endpoint delivered 2304.348 = 3.08× pool.** ⚑ **Denominator named (INFO-4 discipline):**
  **3.0848× against the GD fixture pool of 747 HP**; against the **sim** pool of 759 HP the same
  number reads **3.0360×**. Both are in the artifact under
  `as_fraction_of_pool.{fixture_747, sim_pool}`. The charter's unqualified "3.08" is the
  **fixture_747** basis. See §A-6.

**Leg 1: PASS.** The acceptance shape is a statement about the **support** of the distribution, and
the support clears the floor everywhere it was probed.

### 2.2 Leg 2 — win reachable ✓, and the attribution is a surprise

| leg | M-3 dark | M-3 armed |
|---|---|---|
| pre (R2_proxy) | 0/30 | **0/30** |
| endpoint (R2_proxy_resists_low) | 0/30 | **0/30** |
| post (R3) | 30/30 | **30/30** |

**The win IS reachable — 14/30 on the pre leg (M-8a arm B).** Leg 2: **PASS.**

**⚑ ATTRIBUTION SURPRISE — REPORTED IN THE GRADE, per P-3:**

- **Sustain carries the win.** The reachable pre-leg win comes from the leech arm (arm B, 0.08 vs
  0.05) at **14/30**, with mean leech healed rising `422 → 1069 HP` and mean fight length
  `37.2 s → 57.9 s`.
- **The dodge pilot moves win rate `0.000` on all three legs.** M-3 (`piloted_competence`) armed vs
  dark is **identical on every leg**. The dark-arm cross-check is clean on all nine
  (leg × seed) pairs: M-3 consumes no RNG and performs no teleport.
- **This is consistent with the corpus, not anomalous.** GD has **no scaling evasion**. The real WIN
  in the source fixture was **positional**. The evasion side of acceptance symmetry is carried by a
  **different mechanism** than the one modeled for it — a KIT-CAL-vocabulary finding.
- **Routed to the wave tail, beside the 5.62 m standoff finding.**
- **Instrument caveat carried:** these fights use the runner's `spatial_dm`
  (`SPATIAL_DAMAGE_SCALE = 0.6`). The M-3/M-12 integration tests omit it and run the player at
  **1.667×**; their magnitudes and outcomes are **not comparable** with these. Gate-2's §8.17
  verification clause found **nothing to retract** — no graded claim in any prior finding quoted a
  magnitude or outcome from the contaminated paths (m3-m12b figures are identical on both `dm`
  values). Repair routed to the wave tail, not performed in-run.

---

## §3 — M-8a: legs disposed SEPARATELY (P-3 / R-M8-1)

**Decision rule quoted, not re-written:** spec §17 — *outcome FLIPS between arms ⇒ Battle Surge is
load-bearing ⇒ M-8b builds behind the door and BQ-4 promotes. NO FLIP ⇒ the absence is proven
non-load-bearing across BOTH regimes and BQ-4 CLOSES.*

Arms: **A = 0.05 lifesteal · B = 0.08** (ratio 1.60). **A-ARM-3 respected** — the arms do **not**
share per-seed RNG streams, so no paired per-seed delta table is produced; what is reported is a
**count of verdict disagreements**, a different object, with its caveat attached.

| leg | arm A | arm B | verdict | seeds disagreeing |
|---|---|---|---|---|
| **pre** (R2_proxy) | **0/30** | **14/30** | **FLIP** | 14 |
| **endpoint** (R2_proxy_resists_low) | **0/30** | **2/30** | **FLIP** (0 → 2 is still a flip) | 2 |
| **post** (R3) | 30/30 | 30/30 | **no flip** | 0 |

**Killability side — the arms are identical to the HP at BOTH grains, on every leg:**

| leg | worst single received A / B | worst per-projectile A / B |
|---|---|---|
| pre | **414.8 / 414.8** | **207.4 / 207.4** |
| post | **414.8 / 414.8** | **207.4 / 207.4** |
| endpoint | **470.8 / 470.8** | **235.4 / 235.4** |

Sizing carried, not re-derived: 22.7–68.2 HP/proc = 3.0–9.1 % of the 747 pool against a ≥ 543 HP
one-frame deletion ⇒ **NOT AN OPERAND** (spec §16.2, R-M8-1). A 3 s drip cannot alter a one-frame
kill. On the winnability side: 45–205 HP over the fight = 6–27 % of the pool ⇒ **MATERIAL**.

**Disposition:** the two pre legs flip; the post leg does not. **The legs are never pooled**
(R-M8-1) — the pre legs are two readings of one bracketed quantity, and the post leg is a different
regime. Battle Surge's absence is **load-bearing under R2 and non-load-bearing under R3**. M-8b was
**not built** in this run (P-3 gates it on exactly this evidence, and this evidence is the cell's
output). The disposition routes forward with the bracket attached, not as a clean fidelity result.

---

## §4 — CONTEXT ROW: diff vs the G-5 baseline

Baselines: pre vs `bef1f55`, post vs `f54c547` (declared, per-leg, not pooled).

| tier | boss win rate before → after (pre) | worst received hit before → after |
|---|---|---|
| **boss** | **1.000 → 0.233** | **59.99 → 414.80** |
| mixed_pack | 1.000 → 1.000 | 57.59 → 23.88 |
| champion | 1.000 → 1.000 | 57.55 → 18.00 |
| trash | 1.000 → 1.000 | 47.19 → 14.76 |

On the **post** leg the boss win rate returns to **1.000** while the worst received hit stays
**414.80**. Mean boss fight length `28.5 s → 47.6 s` (pre) / `57.7 s` (post).

**Read it plainly:** the wave did not make the boss uniformly harder. It made the boss **survivable
on average and lethal in one instant** — the non-boss tiers got *safer* by a factor of ~2.5–3 on
worst-case intake while the boss's worst-case intake went up **7×**. That shape is the run's most
transferable design finding and it belongs to the wave tail beside P-2.

---

## §A — CORRECTIONS AND SCOPE NOTES EXECUTED IN THIS RECORD

### §A-4 — ⚑ WARN-4: THE CORRECTION OF RECORD

**The claim, as it stands in three places:**

> *"2.2700 clears R-WR1-7's ≥ 1.50 on its face and **55 %** of it is NOT the gear step."*

**The "55 %" DERIVES FROM NOTHING. It is withdrawn. It must not be quoted.** It is the conductor's
own arithmetic error, erratum-class (R-WR1-8), caught by jack-ryan's Gate-2 second-pass addendum
§A.2 and accepted without dispute.

**CORRECT FIGURE — multiplicative share, and the basis is named:**

| reading of *"share of 2.2700 that is not the gear step"* | denominator | value |
|---|---|---|
| **multiplicative share** — gear factor `1.1350 / 2.2700`, so the count factor `2.0000` is the rest | **the ratio itself, 2.2700** | **50.00 %** |
| log share of the count step — `log 2.0000 / log 2.2700` | `log 2.2700` | 84.6 % |
| share of the excess over 1 — `(1.2700 − 0.1350) / 1.2700` | `2.2700 − 1` | 89.4 % |

**The correct statement under the obvious reading:** `2.2700 = 1.1350 × 2.0000`, so **the gear step
is exactly HALF of it — 50.00 % — and the other 50.00 % is the count step.**

**Discipline attached:** the three readings span 50 %–89 % on the same two numbers. **A percentage
here is meaningless without its named denominator. Whichever is quoted, name the denominator with
it.** (This is the same failure class as INFO-4's `headroom_pct`, one artifact apart — which is why
both are corrected in one lap.)

**⚑ THE THIRD SITE IS INSIDE THE BANKED ARTIFACT AND IS NOT EDITED.**

| site | disposition |
|---|---|
| `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery.md` §9.2 (line 773) | **corrected in place** with an erratum banner, original string left standing with its lineage |
| `reincarnated-engine/src/reincarnated/simulation/math/wr1-battery-ga-gb-m8a-2026-07-29.md` §14.1 | **corrected in place**, bannered identically |
| **`…/wr1_battery_2/wr1_battery2_statistics.json` → `H_B2_6_FINDING.boss_decomposition.warning_to_the_grader`** | **NOT EDITED. SS-1 forbids it.** The banked artifact is left standing and **flagged known-wrong**; **this grading record supersedes it of-record.** |

**SS-1 is the reason, and it is the right reason.** The banked battery artifact is the run's
byte-frozen evidence object; jack-ryan's re-check §R5 filed this caveat *in advance* precisely so it
would not be discovered mid-correction. The disposition is identical to WARN-1's: erratum in prose
at the point the claim was made, corrected figure in the grading record, banked string untouched.
**An artifact that can be silently edited after banking is not evidence.**

**Nothing numeric moves.** `2.2700`, `1.1350` and `2.0000` are unchanged. The decomposition, the
estimator (§2.3 nearest-rank p99), the un-evaluated-predicate stance and the MISS are all unchanged.
What was wrong was one rhetorical fraction in a grader-facing sentence.

### §A-5 — ⚑ DISCREPANCY STOP: the "`p99_and_max_ratios_agree: false` here and nowhere else" claim

**Charter §8.18 and gamora's cell note §9.2 (line 771) both state the flag reads `false` "on this
cell and on no other." THE BANKED ARTIFACT CONTRADICTS THIS.** Measured, every cell:

| tier | leg | `p99_and_max_ratios_agree` | `p99_over_max_ratio` |
|---|---|---|---|
| trash | pre / endpoint | true / true | 1.0 / 1.0 |
| champion | pre / endpoint | true / true | 1.0 / 1.0 |
| **mixed_pack** | **pre** | **false** | **0.99732** |
| **mixed_pack** | **endpoint** | **false** | **1.00132** |
| boss | pre | true | 1.0 |
| **boss** | **endpoint** | **false** | **2.0** |

**The flag reads `false` at THREE cells, not one.** Reported, not harmonized (R-WR1-8 class; this is
the conductor's own text being corrected).

**The substance of corroboration (3) survives intact, in a sharper form.** What is unique to
boss/endpoint is not that the flag fired — it is *the magnitude and integrality of the
disagreement*:

- **boss/endpoint:** `p99_over_max_ratio = 2.0` — an **exact integer**, and uniquely
  `p99_equals_max: true`. A p99 sitting on a structurally different object from the max.
- **mixed_pack (both legs):** `0.99732` and `1.00132` — **sub-0.3 % float noise** around 1 on a
  continuous damage distribution. Ordinary estimator jitter, no mechanism behind it.

**The corrected claim of record:** *the instrument fired at three cells; at exactly one — boss,
endpoint — the disagreement carries a material integer factor, and that is the cell where the p99 is
reading a different mechanism from the max.* The instrument did its job. The scope sentence around
it overstated, and the overstatement is corrected here rather than repeated.

### §A-6 — Denominator note on the "3.08× pool" figure (INFO-4 class)

`2304.348 / 747 = 3.0848` (**GD fixture pool**) · `2304.348 / 759 = 3.0360` (**sim pool**). Both are
in the artifact. The charter's unqualified "3.08" is the **fixture_747** basis. Neither is wrong;
quoting either without its denominator is. Named at every use in §2.1.

### §A-7 — Engine-pin stamp state, carried forward honestly (WARN-1 lineage)

`wr1_battery2_statistics.json` stamps `7f77ea0` in **both** `banked_legs[*].engine_git_hash` **and**
`statistics_engine_git_hash`. The charter's "two production events, two hashes, deliberately" claim
is **false as stamped** — Gate-2 WARN-1, root cause `--untracked-files=no` in the stamp helper.
**The artifact was NOT rewritten** (SS-1); errata were filed where the claim was made, and the stamp
detector was fixed *forward* (`_untracked_loaded_source()` now dirties the stamp when an imported
module is in no commit). **True provenance:** legs produced at `7f77ea0`; the statistics driver
landed at `05a294f`; the repair commit is `7c16fec`, byte-non-touching on the banked artifact per the
Gate-2 SS-1 check. This is the record; the artifact's self-stamp is known-incomplete.

---

## §B — WHAT ROUTES TO THE WAVE TAIL

1. **G-A's source-side finding** (P-1): armour saturated in both regimes; 62.9 % of payload immobile
   across the gear step; danger situational, not statistical. *The finding, not a remediation lap.*
2. **P-2 re-registration:** the 2.12 danger-signature ambition as an **encounter-composition**
   target (boss-before-gear-plateau scenario modeling). **Settled direction.**
3. **G-B's attribution surprise:** sustain carries the win; the dodge pilot moves 0.000; GD has no
   scaling evasion and the real WIN was positional. Travels beside the **5.62 m standoff** finding.
4. **The boss-fight shape finding:** non-boss worst-case intake fell ~2.5–3×; boss worst-case intake
   rose 7×; boss win rate 1.000 → 0.233 on the pre leg. The wave made one instant lethal rather than
   the fight harder.
5. **Corner-drift, not orbit** (R-WR1-20 evidence): the boss fight is a straight-line drift to the
   SW corner, resolved there, 75.03 % of player-alive ticks wall-pinned.
6. **frigidring `range_m 10.0` vs telegraph `radius_m 12.0`** param/schema discrepancy.
7. **Nova footprint clipped 1.92 m east** by the arena wall in all 132 firings — fixture-fidelity
   question (did GD's arena clip?).
8. **M-3/M-12 test-instrument repair** (1.667× paths omitting `SPATIAL_DAMAGE_SCALE`).
9. **INFO-6:** the anchor's DoT-aggregation grain, resolvable by one L0 trial.
10. **WARN-C:** the hero-term AST guard is defeatable four ways; the rule it guards (R-M5-1) is
    behavioural law regardless. Hardening only.
11. **WARN-5:** the stamp detector's reach is `simulation/` only while all three declaration sites
    say `reincarnated/`.
12. **Disposition 3 (banked, not adopted):** per-projectile `on_hit` grain. Rejected for this run
    (Discipline #12 + baseline comparability); **the question it answers is real and belongs to
    G-D** — routed to the baton's consumer notes instead.

---

## §C — HOW THIS RECORD WAS ASSEMBLED

Every number above was extracted from the banked artifact or the 450 banked traces in this lap and
checked against the charter's banked figures. **Three items did not reconcile silently and are
reported rather than harmonized:** §A-5 (the "nowhere else" scope claim — **contradicted**), §A-6
(the "3.08× pool" denominator — **ambiguous, both bases named**), §A-7 (the dual-hash stamp — known
WARN-1 state, restated). Two further discrepancies surfaced against the **baton's** spot-parse brief
and are reported in `2026-07-29-wr1-baton.md` §4 (`decision` events and a per-trace `realized_count`
field are **both absent from all 450 traces**). No banked number moved.

**Companion documents:** `2026-07-29-wr1-baton.md` (G-C) ·
`2026-07-28-wr1-wave-relay-run-charter.md` (the run ledger) ·
`qa/findings/2026-07-29-gate2-gamora-wr1-battery.md` (Gate-2 of record) ·
`gamora/notes/2026-07-29-wr1-battery.md` (cell note) ·
`gamora/notes/2026-07-29-wr1-envelope-spec.md` (spatial envelopes, R-WR1-20).
