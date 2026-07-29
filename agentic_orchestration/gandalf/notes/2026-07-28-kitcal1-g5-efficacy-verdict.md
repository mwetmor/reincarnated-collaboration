# VERDICT — 2026-07-28 — KIT-CAL-1 G-5: the N-band JOIN (run efficacy, finale lap)

**Run:** `KC1-2026-07-27` · exit predicate **T-5, second half**
**Author:** gandalf (named sub-agent, gandalf seam)
**Engine:** `bef1f55` · harness `harness-v1` · 150 fights / 30 seeds
**Evidence:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/g5/kitcal_g5_g5_report.json` (+ 150 `g5-replay-trace/v1` traces alongside)
**Spec under test:** `agentic_orchestration/gandalf/notes/2026-07-28-kitcal1-g4-kit-spec-v2.md` §6.2 (structural) + §6.3 (bands N-1…N-12)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §0 (rubric law) · §2 (T-5) · §14.9 · §14.13 (P-1…P-8) · §14.23 (H-1) · §14.25 · §14.26
**Grading vocabulary:** continuous with the fixture-side verdict (`…/2026-07-26-gd-playtest-v1-efficacy-verdict.md`)

> ⚠ **SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** The bands below were written by this seam (kit spec v2 §6.3,
> ratified as-drafted at P-3). I am now judging a build against them. The conflict is live and declared.
> **The bands were pre-registered before any sim result existed and are quoted here verbatim from §6.3.
> No band was moved. Two of them turn out to have been under-specified — that is a defect in MY spec and
> it is recorded as one below (§2.3), not used to rescue a number.**

---

## VERDICT

> ## HONORABLE FAIL — decomposed. Category (iv) mechanism-class absence dominates; category (ii) sim-mechanics divergence carries one real finding; one new category — **join-construction error, mine** — accounts for three.
>
> The verdict is **decided by the spec's own pre-registered decision rule**, not by band arithmetic.
> Kit spec v2 **§6.0 sentence 1**: *"A band miss with all three structural signatures reproduced is a
> PASS with a tuning note. A band hit with a signature absent is a FAIL."*
>
> **Two of the three PRIMARY structural signatures were never executed** (S-2 and S-3 — no R3 arm exists
> in the battery; `r3_arm: false`), and **S-1 ran only one of its two legs.** Under §6.0 the run cannot
> reach PASS regardless of what the band table says. The band table then misses anyway.
>
> **This is a good result for the run's stated purpose and a bad result for anyone hoping the sim
> already matches GD.** §0 asked whether the sim *can be held accountable* to a measured external
> fixture. It can: the join produced a specific, decomposable, mechanism-named miss profile, and the
> profile is legible enough to write the next wave's backlog from it directly (§7).

| §6.2 structural signature (PRIMARY — outranks every band) | Execution status |
|---|---|
| **S-1** A-step exists | **HALF-EXECUTED** — arc leg ✓ (A > 1.25 on both cuts); single-target control leg **NOT RUN** |
| **S-2** DoT-tail lift confined to B | **NOT EXECUTED** — no DoT arm in the battery |
| **S-3** gear step inverts hazard SHAPE | **NOT EXECUTED** — one player pool (759) across all 150 fights; no gear-step arm |

| Band grading (§3) | Count |
|---|---|
| **PASS, weighting-robust** (passes on every legitimate cut) | **1** — N-2 |
| **MISS, weighting-robust** (misses on every legitimate cut) | **7** — N-5, N-7, N-8, N-9, N-10, N-11, N-12 |
| **CUT-DEPENDENT** (grade flips with an unpinned weighting choice — §2.3) | **3** — N-1, N-3, N-4 |
| **NOT SCORED** (declared non-target, R-KC1-9) | **1** — N-6 |
| *Conservative binary, if forced (cut-dependent → MISS):* | *1 PASS / 10 MISS / 1 not-scored* |

---

## §1 — COVERAGE GATE, FIRST

Per charter T-5 and desirable-run-pattern §6.1 (pattern-observation 1: **coverage before accuracy** —
KIT-FIDELITY failed by certifying a sliver). Nothing below is a band grade. This section asks only:
**which fixture series does the sim reproduce AT ALL?**

### 1.1 The structural census — 2.5 of 3 primary signatures unrun

The report's own header settles this before any statistic is computed: **`r3_arm: false`**, and
`player_pool` is **759.0 on all 150 fights** — including the boss tier. The battery is entirely
inside the W-c-side kit at one gear state.

- **S-1 (A-step).** The predicate has two legs: *single-target arm returns A ∈ [0.98, 1.05]* AND
  *arc arm returns A > 1.25 at G-5a pack sizes without needing density outside those pools.*
  **The arc leg is satisfied** — A = 2.2500 (packs-only) / 1.9091 (packs + boss Arm A), at pack sizes
  8 / 4 / 6, all inside G-5a's declared Act-1 pools. **The control leg was not run**: no single-target
  arm exists in the battery. The boss tier's A = 1.0000 is *not* a substitute — it reads 1.0 because a
  3-mob boss trio dies sequentially over ~28 s, not because a single-target kit was compiled.
  **Grade: HALF-EXECUTED.** The half that ran, passed.
- **S-2 (DoT-tail confined to B).** Requires a like-for-like W-c → R3 comparison with the poison DoT
  added. **No DoT arm exists.** The A/B arms in this battery are **leech** arms (R-KC1-18), a different
  question entirely. **Grade: NOT EXECUTED.**
- **S-3 (gear step inverts hazard shape).** Requires the ×2.11 EHP step plus itemised mitigation and a
  re-read of the ≥10 %-EHP drop count across the step. **One pool, no step. Grade: NOT EXECUTED.**
  (Note: `A-HP-1` asserts the pool ∈ {759, 1607} and passed — but 1607 was asserted *available*, never
  *instantiated*. An assertion over a set is not evidence that both members were exercised.)

**This is the finding of the lap.** The three signatures were declared PRIMARY and declared to outrank
every number in §6.3. The battery executed one of six legs. Any verdict that had led with the band
table would have certified a sliver — precisely the failure mode the coverage-first rule exists to
catch, and precisely what §6.1 of the pattern warns about.

### 1.2 The named-absent ledger — what is structurally invisible

Carried verbatim from the report's `named_absent` array + charter §14.24 / §14.26, with the join
consequence stated for each:

| # | Absent mechanism | Ruling that removed it | Consequence for the join |
|---|---|---|---|
| 1 | **`battle_surge`** — on-crit 3 s self-HoT + 6 s ICD (~1,500 HP of in-fight healing) | P-6 NOT-EXPRESSIBLE → **BQ-4** | The A/B arms exist *because* of this. Resolved: no flip (§14.26) |
| 2 | **`primordian_frigidring`** — 16-projectile 360° hard-freeze nova | **HALT-2** + §14.23 **H-1** (compiling `freeze` forbidden, §14.22(3)); magnitude inside the HELD boss clamp | **Kills N-11 and N-12 outright and most of N-10.** Bias direction named: sim boss is *less* bursty than fixture boss |
| 3 | **crit labelling in the trace** | **HALT-3** — resolver crits, no call site logs it; P-6 declined to glue | No crit-conditioned statistic is computable; N-4/N-5 cannot be decomposed by crit |
| 4 | **dodge-on-tell / evasion** | **R-KC1-22** — build-class inexpressible (no tell modeling, no dodge policy) | **Kills N-7 outright and most of N-8/N-9.** The sim player stands in contact for 100 % of every encounter |
| 5 | **freeze-CC (GD semantics)** | H-1-adjacent; RDR shatter is an RDR mechanic, GD freeze is pure CC | Un-modeled crowd-control; no join surface |
| 6 | **amatok flat cold rider** | only the aura's +16 armor folded (into the door) | Small magnitude bias, honest direction |
| 7 | **passive regen 1.10 HP/s** | charter §14.16 — declared negligible (~66 HP/min) | Slightly overstates sim attrition; ~4 HP over a 4 s encounter |
| 8 | **`arm_a_jitter = false`** | named deviation, §14.26 — flat 5.0 % vs measured 3.25–6.75 % | Immaterial to the flip; **is** a deviation from R-KC1-18 as written, recorded not smoothed |

### 1.3 How much of the watched surface can the band table actually see?

**The table computes 11 of its 12 numbers** (N-6 is declared non-target). Computability is not
visibility. Sorting the twelve by *what they interrogate*:

- **N-1 … N-5 (5 of 12) — tempo and kill-decomposition.** These interrogate mechanics the build
  **can** express: encounter duration, skew, arc breadth, multi-kill structure. **These are the real
  join.** They are where a miss teaches something the current build-class could act on.
- **N-7 … N-12 (6 of 12) — the entire hazard half.** Every one of these is measured against a hazard
  model that is **declared-absent in both directions**: no avoidance (ledger item 4) and no burst
  (ledger item 2). Their misses were *predictable from the ledger before the battery ran* — and they
  are the six misses that arrive. Their diagnostic value is confirmatory, not informative.
- **N-6 (1 of 12)** — reported, never scored.

> **The honest headline of the coverage gate:** *the band table interrogates the sim's tempo with five
> instruments and its hazard with none, because both halves of the hazard mechanism — the avoiding and
> the bursting — are outside the build class. Of the three signatures that were supposed to outrank the
> table, five of six legs did not run.* **The fraction of the fixture's watched surface this join can
> see is roughly one part in four, and the seen part is entirely the tempo side.**

---

## §2 — METHOD (so Gate-2 can re-derive byte-for-byte)

### 2.1 Rules applied

1. **Source:** `kitcal_g5_g5_report.json`, key `fights` (150 records). No trace parsing for N-1…N-12;
   traces are used only for the S-1 second instrument (§4.3).
2. **Encounter = one fight record.** Verified: `abc.encounters == 1` on all 150.
3. **Ratio statistics are ratios-of-sums, not means-of-ratios** — A = Σkills / Σkill_events,
   B = Σkill_events / Σbursts, C = Σbursts / Σencounters. This matches the fixture-side ledger
   construction (421 kills / 49 engagements ⇒ A·B·C = 8.5916 ≈ 421/49 = 8.5918, identity holds to 2e-4).
   *(Mean-of-fight would give A = 2.5000 on the packs cut instead of 2.2500 — recorded so the choice
   is inspectable, not silent.)*
4. **Quantiles:** linear interpolation on the sorted sample, `h = (n−1)p`; verified identical to
   `numpy.percentile(x, 90)` default (7.3374 both ways on the packs cut).
5. **Normalization (O-8):** intake read from the pre-computed `intake.total_intake_pct_maxhp` and
   `intake.worst_drop_pct_maxhp` — already % of max HP against the 759 canonical pool.
6. **Coverage gate (P-5):** `intake.coverage == 1.0` on **all 150 fights**. The ≥0.80 gate for
   N-7…N-10 admits every fight; the gate-off rule for N-11 is therefore moot on the sim side. Per the
   report's own `coverage_note`, P-5's gate is a **fixture-side instrument** carried for like-for-like,
   not applied to the sim. **No fight was excluded by any gate.**
7. **N-12** uses `intake.drops_ge_10pct_count`, which is **0 on all 150 fights** ⇒ numerator 0 ⇒
   share 0.0000 % on every cut. The statistic is defined (0 / positive total), not undefined.

### 2.2 Re-derivation script (exact)

```python
import json, statistics as st
d = json.load(open('kitcal_g5_g5_report.json')); F = d['fights']
def q(xs, p):
    xs = sorted(xs); h = (len(xs)-1)*p; lo = int(h); fr = h-lo
    return xs[lo] if lo+1 >= len(xs) else xs[lo] + fr*(xs[lo+1]-xs[lo])
PACK = [f for f in F if f['tier'] in ('trash','champion','mixed_pack')]        # CUT-1, n=90
BA   = [f for f in F if f['tier']=='boss' and f['arm']=='A']                   # +30 -> CUT-2, n=120
S = PACK                     # or PACK+BA
dur = [f['elapsed_s'] for f in S]; ti = [f['intake']['total_intake_pct_maxhp'] for f in S]
wd  = [f['intake']['worst_drop_pct_maxhp'] for f in S]
N1 = st.median(dur); N2 = st.mean(dur)/st.median(dur); N3 = max(dur)
N4 = sum(f['abc']['kills'] for f in S)/sum(f['abc']['kill_events'] for f in S)
N5 = sum(f['abc']['kill_events'] for f in S)/sum(f['abc']['bursts'] for f in S)
N6 = sum(f['abc']['bursts'] for f in S)/sum(f['abc']['encounters'] for f in S)
N7 = sum(1 for f in S if f['intake']['zero_intake'])/len(S)
N8 = st.median(ti); N9 = st.median(wd); N10 = q(wd, 0.90); N11 = max(wd)
N12 = 0.0 if sum(f['intake']['drops_ge_10pct_count'] for f in S) == 0 else None
```

### 2.3 ⚠ A DEFECT IN MY OWN SPEC — the window's membership for the boss tier was never pinned

**Stated before the numbers, because it changes three grades and I will not present it as a footnote
afterwards.**

§6.3 binds eleven of twelve bands to "W-c". On the **fixture** side W-c is unambiguous: `play_time ≥
3619` inside R2 — a natural 49-engagement sequence that **demonstrably contains the Primordian boss
encounter**, because §6.3's own N-11 row quotes the 72.42 % event as *"it is death 2"* with window
**W-c**, and §6.4's terminal-3 mass (50.9 % of W-c intake, median worst-drop 41.9 %) *is* that
encounter.

On the **sim** side there is no natural sequence — there is a designed 4-tier battery with equal seed
counts. Nothing in §6.3 says which tiers constitute W-c. The report labels the whole run
`window_id: "W-c"` with `r3_arm: false` and pool 759 throughout, which reads the boss tier **into**
W-c. The conductor's dispatch framing reads it **out** ("boss fights are the R3 arm").
**Both readings are defensible and the spec does not adjudicate. That is my defect, not gamora's and
not the conductor's.** Deeper: the sim's battery is **composition-designed** where the fixture's is
**composition-sampled**, so *every* aggregate band is a function of a tier-weighting rule that was
never pre-registered.

**How I handle it, chosen so that no choice can flatter the result:**

- **CUT-1 (packs only, n = 90)** — trash + champion + mixed_pack. The conductor's framing.
- **CUT-2 (packs + boss Arm A, n = 120)** — the like-for-like-with-fixture-W-c reading. Arm A only,
  because Arm A is canonical (§14.26) and Arms A/B are *the same encounter under two door values*.
- **CUT-3 (all 150) is reported but REJECTED as illegitimate** — it double-counts the boss to 40 % of
  the sample. **It is also the cut that most flatters N-4** (1.7143 against a fixture 1.7615 — a near
  bullseye). Naming that explicitly is the point: the most flattering cut is the least legitimate one,
  and it is not used.
- **Grading rule:** PASS only where **both** legitimate cuts pass; MISS where **both** miss;
  **CUT-DEPENDENT** where they disagree — and the disagreements split **one each way** (N-1 passes on
  CUT-1 and misses on CUT-2; N-3 and N-4 miss on CUT-1 and pass on CUT-2), so the third state is not a
  device for absorbing misses. A conservative binary (cut-dependent → MISS) is given in the verdict box
  for anyone who wants one; **the verdict is the same under either presentation.**

**Boss-tier weighting caveat, carried with every tail band:** the boss is ~25 % of CUT-2's encounters
against roughly 2–6 % of the fixture's W-c engagements. CUT-2 therefore **over**-weights the sim's
heaviest tier — and the tail bands (N-10, N-11, N-12) still miss **low** under that over-weighting.
The miss is robust to the distortion that would most help it.

---

## §3 — THE BAND TABLE

Fixture values and bands quoted verbatim from kit spec v2 §6.3 (pre-registered; ratified as-drafted,
P-3). Sim values computed per §2.

| # | Quantity | Fixture (MEASURED) | Pre-registered band | **CUT-1** (n=90) | **CUT-2** (n=120) | **Grade** |
|---|---|---|---|---|---|---|
| **N-1** | Median encounter duration | 4.5 s | 3.0 – 7.0 s | **4.400 s** ✅ | **7.300 s** ❌ | **CUT-DEPENDENT** |
| **N-2** | Mean / median duration ratio | 1.311 | 1.10 – 1.80 | **1.4503** ✅ | **1.6316** ✅ | **PASS** (robust) |
| **N-3** | Max encounter duration | 27.5 s | **≥ 18 s present** | **11.500 s** ❌ | **30.300 s** ✅ | **CUT-DEPENDENT** |
| **N-4** | **A** — kills per kill-event | 1.7615 | 1.45 – 2.10 | **2.2500** ❌ | **1.9091** ✅ | **CUT-DEPENDENT** |
| **N-5** | **B** — kill-events per burst | 2.4141 | 1.95 – 3.00 | **1.1163** ❌ | **1.0820** ❌ | **MISS** (robust, low) |
| **N-6** | **C** — bursts per encounter | 2.0204 | *declared non-target* | 2.3889 | 2.5417 | **NOT SCORED** |
| **N-7** | Fraction of encounters with **zero** intake | 0.378 | ±0.15 abs → 0.228 – 0.528 | **0.0000** ❌ | **0.0000** ❌ | **MISS** (robust, low) |
| **N-8** | Median encounter intake, % max HP | 1.79 % | 0.5 % – 5.0 % | **51.17 %** ❌ | **63.29 %** ❌ | **MISS** (robust, high ~29–35×) |
| **N-9** | Median worst single drop, % max HP | 1.79 % | 0.8 % – 5.0 % | **6.874 %** ❌ | **7.089 %** ❌ | **MISS** (robust, high) |
| **N-10** | p90 worst single drop, % max HP | 16.82 % | 8 % – 30 % | **7.337 %** ❌ | **7.830 %** ❌ | **MISS** (robust, low — *just* under the floor) |
| **N-11** | Largest single intake event, % max HP | 72.42 % (floor-censored; death 2) | **≥ 40 % present** | **7.587 %** (57.59 HP) ❌ | **7.904 %** (59.99 HP) ❌ | **MISS** (robust — argued at §5) |
| **N-12** | Share of intake carried by drops ≥ 10 % EHP | 46.82 % | 30 % – 65 % *(NOT-RECUT)* | **0.0000 %** ❌ | **0.0000 %** ❌ | **MISS** (robust — see caveat) |

**N-12's carried caveat (P-4).** The fixture value is at **R2-whole** grain and cannot be re-cut to
W-c from the store; P-4 accepted it there with the **non-stationarity caveat** attached. The sim value
is grain-immune in this instance: **zero drops ≥ 10 % EHP exist anywhere in 150 fights, on any cut,
including the boss.** No re-cut of the fixture side and no re-weighting of the sim side moves a
numerator of zero. The caveat is carried and, for once, does not bind.

**§6.4's qualifier, carried as required ("this qualifier travels with every §6.3 row, always"):** the
fixture's W-c distribution has a **three-point mass at its end carrying 50.9 % of measured intake**.
N-10 and N-11 read *"the fixture is capable of this"*, not *"the fixture does this routinely."* A sim
that reproduces the median and misses the tail has missed the more important half. **This sim missed
both**: its median worst-drop is ~3.8× too high and its tail is 9.2× too low. It did not reproduce a
tail-less version of the fixture — it reproduced a different distribution shape entirely (§4.2).

### 3.1 Per-tier values (weighting-free — immune to §2.3's defect)

Given that every aggregate is weighting-contingent, the per-tier reads are the more durable evidence:

| Tier | mobs | med dur | **A** | **B** | **C** | med intake %HP | med / max worst-drop %HP | zero-intake |
|---|---|---|---|---|---|---|---|---|
| trash | 8 | 4.20 s | **4.000** | 1.000 | 2.000 | 51.17 % | 6.03 / 6.22 % | 0/30 |
| champion | 4 | 4.40 s | **2.000** | 1.000 | 2.000 | 35.18 % | 7.09 / 7.58 % | 0/30 |
| mixed_pack | 6 | 10.45 s | **1.500** | 1.263 | 3.167 | 73.24 % | 7.09 / 7.59 % | 0/30 |
| boss (Arm A + B) | 3 | 28.80 s | 1.000 | 1.000 | 3.000 | 157.12 % | 7.80 / 7.90 % | 0/60 |

Player wins **150 / 150**. Kills per encounter: **6.00** (CUT-1) / 5.25 (CUT-2) against the fixture's
**8.59**.

---

## §4 — THE THREE READINGS THE NUMBERS CARRY

These are the findings, as distinct from the grades.

### 4.1 The hazard distribution is not tail-light — it is *collapsed to its middle*

Read N-7, N-9, N-10 together against the fixture:

| | fixture | sim (CUT-1) | direction |
|---|---|---|---|
| encounters with **zero** intake | 37.8 % | **0.0 %** | the quiet is gone |
| **median** worst drop | 1.79 % | **6.87 %** | the floor is ~3.8× too **high** |
| **p90** worst drop | 16.82 % | **7.34 %** | the tail is ~2.3× too **low** |
| **max** single drop | 72.42 % | **7.59 %** | the violence is ~9.5× too **low** |

The fixture's hazard is **bimodal and zero-inflated**: most engagements cost nothing, a few nearly kill
you. The sim's hazard is a **narrow band of constant chip** — every encounter, every seed, 5–8 % per
hit, 878 received hits across 90 pack encounters (~9.8 per encounter), never zero and never large.

**The sim reproduces neither the fixture's quiet nor its violence.** And the two halves have the two
named absences as their causes, one each: the quiet is gone because there is **no avoidance**
(R-KC1-22 — the sim player stands in contact 100 % of the time); the violence is gone because there is
**no burst** (HALT-2 — frigidring). This is the same symmetry §14.26 found at the boss tier, now
measured across the whole W-c surface: *both tails of the real fight live in mechanics the sim cannot
express.*

### 4.2 The kill-decomposition is **redistributed**, not merely mis-scaled — and this is a real (ii)

A·B·C is an identity over kills-per-encounter. Both sides decompose it, and the decomposition inverts:

| | **A** (kills/kill-event) | **B** (kill-events/burst) | **C** (bursts/enc) | **kills/enc** |
|---|---|---|---|---|
| fixture (W-c) | 1.7615 | **2.4141** | 2.0204 | **8.59** |
| sim (CUT-1) | **2.2500** | 1.1163 | 2.3889 | **6.00** |

The sim delivers **70 % of the fixture's kill throughput** but routes it through a different structure:
kills **concentrate inside a single 0.5 s kill-event** (A high) instead of **chaining across kill-events
within a burst** (B ≈ 1, meaning almost every burst produces exactly one kill-event). The fixture's
werewolf grinds a pack down over a sustained burst; the sim's werewolf deletes a slice of it at once and
then starts a new burst.

**This is category (ii) sim-mechanics divergence and it is the one band miss that is genuinely about
the sim's combat model rather than about an absence.** Grain is not the explanation — the report's
`grain` block (`encounter_gap_s: 5.0`, `kill_event_bin_s: 0.5`, `burst_gap_s: 1.5`) is the
instrument-canonical grain, identical to the fixture's `S1-gap5s-v1`. It is like-for-like.

### 4.3 S-1's second instrument reverses the naive reading of N-4 — the arc is **narrower**, not wider

The spec offered a fully independent AoE-breadth diagnostic (§6.2, explicitly *"a diagnostic, not a
band"*): fixture **1,606 hits / 680 presses = 2.362 hits per press**. Computed from the 90 W-c replay
traces — grouping player-sourced `damage` events by `(tick, skill_idx)`, one group = one press:

| Tier | presses | mean hits/press |
|---|---|---|
| trash (8 mobs) | 98 | **2.582** |
| champion (4) | 155 | 1.581 |
| mixed_pack (6) | 756 | 1.159 |
| **W-c pooled** | **1,009** | **1.3617** |
| *(boss, 3)* | *2,082* | *1.045* |

**The sim's arc hits 1.36 targets per press against the fixture's 2.36.** So the sim's high A is **not**
caused by an over-broad cone or a missing target cap — breadth is *under*-delivered. A is high because
**attack tempo compresses multiple presses into one 0.5 s kill-event bin**, not because any press is
wide. Only the densest tier (trash, 8 mobs packed) approaches the fixture's breadth; at mixed-pack
spacing the 150° cone catches essentially one target.

**Consequence for the backlog:** a reflexive reading of "N-4 misses high ⇒ tighten the target cap"
would have been **exactly backwards**. BQ-1 (target-count cap) and BQ-2 (per-skill / rank-scaling cone)
should be re-scoped toward **geometry-vs-spacing**, i.e. why the cone under-catches at realistic mob
spacing, and toward attack-tempo calibration — not toward capping breadth. *(Grade caveat: the
fixture's `hitsInflicted` semantics are UNCERTAIN — whether DoT ticks are excluded is unknown — which
is why this is a diagnostic and why it is not being converted into a band now.)*

---

## §5 — N-11: MISS, not NOT-EVALUABLE — the argument

Sim: **max single drop 7.90 % of max HP (59.99 HP)**, on every cut, across 150 fights. Band: **≥ 40 %
present**. Fixture: **72.42 %** (floor-censored — it is death 2).

**The case FOR NOT-EVALUABLE** is real and must be stated at full strength: the fixture's 72.42 % event
*is* the frigidring nova. Compiling a `freeze` emitter is **forbidden** by charter §14.22(3) and by the
§14.23 **H-1** fidelity-law ruling (GD freeze is pure CC; RDR's shatter is an RDR mechanic and must not
be smuggled in), and the nova's damage magnitude sits inside the **HELD** boss clamp. §14.26 further
records that at the declared sweep ceiling (67 DPH) the worst drop scales only to ~10 % — **no value
inside the swept range produces a near-lethal single hit.** On that reading the band's subject was
removed from the build by a ruling, and grading its absence as a MISS scores the sim for obeying a law
this seam wrote.

**Two arguments defeat it.**

1. **R-KC1-22 pre-committed the run to this exact comparison, before results.** Matt ratified that
   boss-tier interpretation anchors to the **death-2 no-evasion trajectory** — the very engagement whose
   killing blow N-11 quotes. To now rule that engagement's defining event NOT-EVALUABLE is to unwind a
   pre-registered anchor after seeing that the sim missed it. **That is goalpost movement, and it is the
   one thing this role may not do.**
2. **N-11 does not name frigidring.** It is an unconditional existence test over the *whole configured
   build*: *"the sim must be capable of a near-lethal single hit."* The configured build — every damage
   row, every tier, both arms, the full declared 33/50/67 sweep — produced a maximum of 7.90 %. The
   build failed the test it was set. That a *sufficient* explanation exists for the failure does not
   convert the failure into a non-event; it converts it into a **decomposed** failure, which is exactly
   what §0's honorable-fail clause asks for.

**RULING: N-11 = MISS**, attributed **wholly to honorable-fallback category (iv), mechanism-class
absence** (frigidring / HALT-2 / H-1). It is a MISS the current build-class **cannot** close and that
the Q-KC1-1 wave inherits with a named acceptance target. It is **not** evidence of a calibration error
in any pinned operand, and it must never be quoted as one.

**Conductor: carry this grading to Matt veto-open.** The competing NOT-EVALUABLE reading is respectable
and the two rulings differ in exactly one visible way — the run's MISS count (10 vs 9 on the
conservative binary). The verdict is HONORABLE FAIL either way, since §6.0's structural rule already
decided it.

**N-12 grades the same way and for the same reason** (zero drops ≥ 10 % EHP anywhere), with P-4's
non-stationarity caveat carried and non-binding per §3.

---

## §6 — VERDICT AGAINST §0's RUBRIC (rubric law: name the rubric, diff it against the intent)

**§0's intent sentence:**
> *Prove the RDR battle sim can be held accountable to a measured external fixture: map the play-test-v1
> werewolf build into a sim-abstract kit from GD source data, run it in gamora's harness, and land
> inside pre-registered acceptance bands against the R2 fixture — **or fail honorably with the miss
> decomposed** into source-mapping error vs sim-mechanics error vs fixture-measurement error.*

**The rubric I actually applied:** *Did the G-5 battery reproduce the fixture's structural signatures at
all (coverage), and where it produced comparable numbers, did they land inside bands pre-registered at
P-3 — and is every miss attributable to a named category?*

**The diff — what fell out, said out loud:**

1. **"Land inside acceptance bands" was answerable only on the tempo half.** Six of twelve bands
   measure a hazard model whose two governing mechanisms are declared-absent. Those bands were
   *computed* but they did not *test* anything the build could have passed. **The intent sentence
   assumed a build with a hazard model; the build under test has a chip model.**
2. **"Against the R2 fixture" collapsed to "against W-c minus most of its own tail."** The fixture's
   W-c carries 50.9 % of its intake in three terminal engagements; the sim's battery has no analogue
   of a terminal engagement, and §2.3's unpinned weighting means the sim's aggregate is a design
   choice rather than a sample. **The join is narrower than "R2" by a wide margin.**
3. **The three-way decomposition in §0 was incomplete.** §0 names source-mapping / sim-mechanics /
   fixture-measurement. The dominant category here is a fourth the spec named elsewhere —
   **(iv) mechanism-class absence** — and a fifth this lap discovered: **join-construction error**
   (§2.3), which is neither the source's fault nor the sim's nor the fixture's, but **the spec
   author's**. Three grades hang on it. *Recorded as an amendment candidate to §0's decomposition
   vocabulary for the next charter of this class.*
4. **What the run DID prove, and it is the thing §0 actually asked first:** *the sim can be held
   accountable.* The battery ran clean (exit 0, 8/8 static assertions, coverage 1.0 on all 150 fights,
   150/150 deterministic traces), the pre-registered rule decided the verdict without argument, and
   every miss carries a named mechanism. **An accountable sim that fails a band is worth more than an
   unaccountable one that passes.** That is the run's return.

### Full miss decomposition

| Band | Miss direction | Category | Owner |
|---|---|---|---|
| N-1, N-3 | cut-dependent | **join-construction** (§2.3) + battery ran 3 fixed compositions, never G-5a's 8–16 large pool | spec (mine) + harness scenario design |
| N-4 | cut-dependent (high on CUT-1) | **join-construction** + **(ii)** attack-tempo compression (not breadth — §4.3) | spec (mine) + sim |
| N-5 | low, 2.16× | **(ii) sim-mechanics divergence** — kill-decomposition inverted (§4.2) | sim — **the real calibration delta** |
| N-7 | low (0.00 vs 0.378) | **(iv)** no dodge/kite/evasion policy — R-KC1-22 | build class |
| N-8, N-9 | high (~29–35×, ~3.8×) | **(iv)** same root — continuous contact, no disengagement | build class |
| N-10, N-11, N-12 | low (2.3×, 9.5×, ∞) | **(iv)** no burst mechanic — frigidring, HALT-2 + H-1 | build class |

---

## §7 — THE JOIN-FORWARD NOTE

### 7.1 Q-KC1-1 wave inheritance (NOT closable by the current build-class)

| Item | Band evidence it now owns | Acceptance fixture |
|---|---|---|
| **frigidring / telegraph-burst modeling** | **N-11** (7.90 % vs ≥40 %), **N-12** (0 % vs 30–65 %), most of **N-10** | The death-2 trajectory (R-KC1-22). Target: a single hit ≥ 40 % of pool must become *possible*, and the ≥10 %-EHP drop share must reach 30–65 % |
| **evasion / dodge-on-tell** | **N-7** (0.000 vs 0.378), **N-8** (51 % vs 1.79 %), **N-9** (6.87 % vs 1.79 %) | **Matt's winning attempt** — banked at §14.24 as the measured proof that dodge-on-tell converts this exact loss into a win. Target: zero-intake fraction into 0.228–0.528 |
| **BQ-4 (crit-trigger consequence / `battle_surge`)** | no band; resolved as non-load-bearing *within the sim's current behavior space* (§14.26 no-flip) | Re-test the flip **after** burst + dodge land — a sustain proc that is inert against chip may be decisive against burst. **The no-flip verdict is scoped to the chip regime and must be re-opened, not inherited as settled** |
| **HALT-3 crit labelling** | blocks decomposition of **N-4/N-5** by crit | A trace call site, not a mechanism change |
| **freeze-CC (H-1-adjacent)** | no band surface | joins the ledger beside evasion |
| **leech carriers F-1…F-7, hero scaling** | none directly (boss-tier only) | carried as-is |

**This G-5 dataset is the before-baseline for all of the above** (150 fights, 30 seeds, `bef1f55`,
deterministic traces, coverage 1.0). Every row above has a *number to beat* now, which it did not have
before this lap.

### 7.2 Genuine calibration deltas the current build-class COULD close

1. **N-5 / the A–B inversion (§4.2) — the highest-value item on this list.** No absent mechanism is
   implicated. The sim's bursts terminate after one kill-event where the fixture's chain 2.4. This is
   attack-tempo, kill-event binning behavior, and target re-acquisition — all present, all tunable.
   **Route to gamora.**
2. **Arc breadth at realistic spacing (§4.3) — 1.36 hits/press vs 2.36.** Re-scope **BQ-1/BQ-2** from
   "is the cap too generous" to **"why does the 150° cone under-catch at mixed-pack spacing"**. The
   diagnostic reverses the naive backlog reading and would have sent the next wave the wrong way.
   **Route to rocket (geometry) + gamora (spacing/formation).**
3. **The battery's composition coverage.** G-5a declared Act-1 pools of 1–8 / 2–9 / 3–10 / **8–16**;
   the battery ran three fixed points (8 / 4 / 6) and never the large pool. **Sweep density rather than
   fixing it** — this alone would make N-1/N-3/N-4 weighting-robust instead of cut-dependent.
4. **Per-encounter attrition sanity.** The sim werewolf takes a **median 51 % of its pool per pack
   encounter** and still wins 30/30, because encounters are evaluated in isolation. **Chained
   encounters at this attrition rate are unsurvivable** — the fixture's player chained 49 of them.
   Nothing in the battery tests the chain. **Candidate for the next lap's scenario spec.**
5. **`arm_a_jitter = false`.** Cheap to close; immaterial to this verdict; leaving it open leaves a
   named deviation standing in the record.

### 7.3 Owed to the spec (this seam's own follow-up)

**Kit spec v2 §6.3 must gain a tier-weighting rule and an explicit boss-tier window-membership clause
before any band from it is quoted again** (§2.3). Until then, N-1 / N-3 / N-4 are not citable as either
pass or fail. This is a **spec amendment**, not a re-grade of this run — the bands themselves stay
exactly as pre-registered.

---

## PROVENANCE

- **Sim side:** `kitcal_g5_g5_report.json` @ engine `bef1f55`, run `KC1-2026-07-27`, harness
  `harness-v1`, seed base 74000800, 30 seeds × {trash, champion, mixed_pack, boss×2 arms} = 150 fights;
  all 8 static assertions passed in-run; `intake.coverage == 1.0` on all 150. Traces:
  `…/kitcal_g5/g5/traces/*.jsonl`, schema `g5-replay-trace/v1` over base `replica-frame/v1`.
- **Fixture side:** every value quoted verbatim from kit spec v2 §6.3 / §6.2 / §6.4, themselves
  MEASURED from `fixtures.db` (`regime_stat` / `v_engagement_wide`, session `GP-gd-2026-07-26-s1`,
  segmentation `S1-gap5s-v1`). **No fixture value was recomputed in this lap** — recomputing the
  goalposts at grading time is the failure mode this discipline exists to prevent.
- **Grade of all sim-side statistics:** MEASURED (computed from the banked report; §2.2 reproduces
  them exactly).
- **Ruling status:** every grade in §3 and the §5 N-11 ruling are **veto-open** per the run's ledger
  convention. The conductor carries §5 to Matt explicitly.

**Signed:** gandalf (`DRIFT-CRITIC`, judging this seam's own spec), 2026-07-28.
