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

---
---

# AMENDMENT — 2026-07-28 — THE TERMINAL SIGNATURE VERDICT, on the fully-repaired stack

**Lap:** amendment lap (terminal), run `KC1-2026-07-27` · commissioned by the conductor under **R-KC1-23**
**Author:** gandalf (named sub-agent, gandalf seam) · role-tag **`DRIFT-CRITIC`**
**Engine:** `67e7ccb` · tag `gamora/v-dot-delivery-2` · harness `harness-v1` · 30 seeds × 3 arms × 150 fights = 450 fights
**Evidence — THE TERMINAL STACK:**
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5_fix3/{g5, g5_r3arm, g5_s1control}`
(all three reports stamp `engine_git_hash: 67e7ccb`, verified this lap; 450 traces `g5-replay-trace/v1`)
**Certification this lap rests on:** `qa/findings/2026-07-28-gate2-gamora-dot-delivery-2-rereview.md` — **CONDITIONAL PASS, BLOCK LIFTED**
**Quarantines honoured (read as evidence NOWHERE above):** `output/kitcal_g5/g5_r3arm/` (pre-DoT-fix, permanently quarantined per Gate-2 **SS-1**) · `output/kitcal_g5/smoke/traces/` (5 stray post-fix files, Gate-2 **WARN-1** — untouched) · `kitcal_g5_fix/` + `kitcal_g5_fix2/` (superseded generations; cited for lineage only)
**Charter:** §14.27 (R-KC1-23) · §14.28 · §14.29 (R-KC1-24) · §14.30 · §14.31 (R-KC1-25) · §14.32 · §14.33 · §14.36

> ⚠ **SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** Same declared conflict as the T-5 lap, and it bites
> harder here: two of the three structural predicates I am about to grade turn out to be **defective
> instruments of my own authorship**. I grade them as defective and I do not let the defect purchase
> a better verdict in either direction.

> **R-KC1-23 compliance.** Everything above this rule STANDS UNEDITED. No T-5 grade is re-litigated
> on an unchanged series. Where `_fix3` moves a series, the delta is reported at **§A-6** and the
> T-5 grade is re-tested against the pre-registered band — not re-argued.

---

## THE TERMINAL VERDICT

> ## HONORABLE FAIL — **CONFIRMED on a complete signature set, and RE-DECOMPOSED.**
> **The letter of the T-5 verdict stands. Its reason is entirely retired and replaced.**
>
> T-5 failed on **coverage**: 5 of 6 signature legs were never run, because the conductor's fire
> command took two harness defaults. That failure is now **closed** — four repair laps later, the
> execution census reads **6 of 6 legs run**, on a stack whose DoT lever is connected, whose kernel
> delivery ledger is exact to 1 µs, and whose provenance stamp resolves to the kernel that produced it.
>
> The run now fails on **substance**, and §6.0 sentence 2 decides it without argument:
>
> | §6.2 signature | T-5 status | **Terminal grade** |
> |---|---|---|
> | **S-1** A-step exists | HALF-EXECUTED | **REPRODUCED** — cleanly isolated by the control, with a negative control inside it |
> | **S-2** DoT-tail lift confined to B | NOT EXECUTED | **INSTRUMENT-VOID** — predicate unsatisfiable AND unfalsifiable by construction; lever confirmed live on post-registered instruments |
> | **S-3** gear step inverts hazard SHAPE | NOT EXECUTED | **NOT REPRODUCED — band-letter HIT, signature ABSENT** |
>
> **Kit spec v2 §6.0 sentence 1** — *"A band miss with all three structural signatures reproduced is a
> PASS with a tuning note"* — **cannot fire**: the three are not reproduced.
> **§6.0 sentence 2** — *"A band hit with a signature absent is a FAIL"* — **fires verbatim on S-3**,
> which is the textbook instance the sentence was written for and the first time in this run it has
> had a complete enough battery to fire at all.
>
> **The verdict is therefore FAIL, and it is HONORABLE**: every residual carries a named mechanism, a
> named owner, and a number to beat. **Not PASS-with-tuning-notes** (a signature is measurably absent).
> **Not CONDITIONAL** — see §A-7.3 for why inventing that grade at grading time would be the softest
> and most dangerous form of goalpost movement available to this role.
>
> **What the run bought with four repair laps:** it moved from *"we did not run the test"* to
> *"we ran the test, and here is exactly which mechanism the sim does not have."* That is the
> entire difference between an unaccountable sim and an accountable one, and it is the run's return.

| Band grading (§3) — **UNCHANGED by `_fix3`** | Count |
|---|---|
| **PASS, weighting-robust** | **1** — N-2 |
| **MISS, weighting-robust** | **7** — N-5, N-7, N-8, N-9, N-10, N-11, N-12 |
| **CUT-DEPENDENT** | **3** — N-1, N-3, N-4 |
| **NOT SCORED** | **1** — N-6 |
| **Band verdicts CHANGED by the repaired stack** | **ZERO** (§A-6) |

---

## §A-1 — EXECUTION CENSUS: 6 of 6 legs, against T-5's 1 of 6

Coverage before accuracy, again, first (pattern §6.1). This is the gate T-5 failed.

| Signature leg | T-5 | Terminal | Evidence |
|---|---|---|---|
| S-1 arc leg | ✓ ran | ✓ ran | `_fix3/g5` — A = 4.000 / 2.000 / 1.500 at trash / champion / mixed_pack |
| S-1 single-target control leg | ✗ unrun | ✓ ran | `_fix3/g5_s1control`, 150 fights, `s1_control: true` |
| S-2 like-for-like W-c → R3 | ✗ unrun | ✓ ran | `_fix3/g5_r3arm`, matched seeds, `r3_arm: true`, pool 1607 |
| S-2 DoT lever connected | ✗ (null instrument ×2) | ✓ | 3,182 player DoT rows / 80,492 HP in R3 against 0 pre-fix |
| S-3 gear step instantiated | ✗ unrun | ✓ ran | pool 759 → 1607 = **×2.1173** against the fixture's ×2.11 |
| S-3 itemised mitigation | ✗ unrun | **✗ STILL ABSENT** | `worst_drop_abs` **identical on 143/150 matched fights**; per-tier median ratio **×1.0000** |

**The last row is the verdict.** Five legs closed across four repair laps. The sixth did not close and
**could not have** — it is not a flag that was left off, it is a mechanism the build class does not have.

---

## §A-2 — S-1: **REPRODUCED.** The band-letter miss is a defect in my own instrument, and the control proves it.

### A-2.1 The control's literal result, stated first and without softening

`s1_control_a_summary`, `_fix3/g5_s1control`, band **A ∈ [0.98, 1.05]** as pre-registered at P-2:

| Tier | control **A** (mean = min = max, all 30 seeds) | in band? | control **hits/press** |
|---|---|---|---|
| trash (8) | **2.6667** | ✗ | **1.0000** (max over all 150 fights: **1.0**) |
| champion (4) | **1.3333** | ✗ | **1.0000** |
| mixed_pack (6) | **1.2000** | ✗ | **1.0000** |
| boss (3) | **1.0000** | ✓ | **1.0000** |

**The control misses its pre-registered band at every pack tier.** I record that before anything else,
because what follows is an argument that the band was wrong, and an argument of that shape must begin
by conceding the number it is about to reinterpret.

### A-2.2 Why the miss is instrument, not sim — and why that is a finding, not a rescue

Three facts, none of them discovered after the fact:

1. **The pre-registered second instrument adjudicates geometry, and it is unambiguous.** Kit spec §6.2's
   note offers `hits/press` (§1.1p) as an independent AoE-breadth check — **written before any sim
   result existed.** The control reads **exactly 1.0000, every tier, every seed, max 1.0 across 150
   fights.** No press ever touched two bodies. The multi-target geometry is **provably neutralized**.
   Whatever A is measuring in the control, it is not breadth.
2. **A has a coincidence floor above 1, and the floor is a property of the pinned kit.** Claws compile
   at `cooldown_seconds = 0.0` and the sim has **no player attack-speed model**, so sequential
   single-target kills land inside one 0.5 s `kill_event_bin_s`. Gate-2 reproduced this at event level
   (`…-gate2-gamora-g5-s1control.md`): one kill per 0.1 s tick, eight kills into three bins; `compute_abc`
   is not buggy; no alternative explanation survives. **My predicate assumed A's floor is 1.0. In this
   battery it is 2.667 / 1.333 / 1.200.**
3. **The control is the HARDER control, not the weaker one.** Gamora neutralized *both* geometries
   (claws cone → single_target AND charge line → single_target). A weaker control drives A → 1 by
   spacing kills out, which would have made the band **easier** to hit and A ≈ 1 stop meaning "the arc
   was the mechanism." The control that failed the band is the one designed to make passing it hardest.

### A-2.3 The A-step, read against the floor instead of against 1.0 — and the negative control inside it

This is the comparison the signature actually claims. Canonical and control differ in **exactly 7 leaves,
all geometry** (Gate-2, independent leaf diff); damage, cooldown, energy, range and the charge bleed are
held at canonical values. Per-tier, at matched seeds:

| Tier | canonical **A** | control **A** (floor) | **A-lift** | canonical hits/press |
|---|---|---|---|---|
| trash (8 mobs) | 4.0000 | 2.6667 | **×1.5000** | 2.5714 |
| champion (4) | 2.0000 | 1.3333 | **×1.5000** | 1.5855 |
| mixed_pack (6) | 1.5000 | 1.2000 | **×1.2500** | 1.1770 |
| **boss (3, spread)** | **1.0000** | **1.0000** | **×1.0000** | 1.0447 |

**The boss row is a negative control that nobody designed and that the signature could not have faked.**
Where the arc has nothing to catch — three spread mobs, 1.04 hits/press — the lift is *exactly* ×1.0000.
If the excess control-A were an artifact that also inflated canonical A spuriously, the boss tier would
still show a lift. It shows none. The A-step appears where breadth appears and vanishes where breadth
vanishes, monotonically in density: **×1.50 → ×1.50 → ×1.25 → ×1.00**.

**Confound checked, not assumed:** the control is *not* outcome-identical to canonical (716 kills vs 720;
boss 56/60 vs 60/60; 270 DoT rows vs 90). **Every one of those divergences is boss-tier.** At the three
pack tiers where the A-lift is measured, the two arms deliver **identical** DoT (mixed_pack 90 rows /
16,767.0 HP in both; zero rows in trash and champion in both) and identical win rates (30/30 each).
The pack-tier lift comparison is clean.

### A-2.4 Grade

> **S-1: REPRODUCED.** The arc leg passes its band as written (A > 1.25 at all three G-5a pack sizes,
> without density outside those pools). The control leg **misses its band letter** and the miss is
> **assigned to a defect in the predicate I authored** — A was banded as though its floor were 1.0 in a
> battery where the floor is measurably 2.667. The geometry-neutralization the leg exists to establish
> is established by the **pre-registered** second instrument at 1.0000 hits/press, and the A-step it
> exists to isolate is isolated at ×1.50 / ×1.50 / ×1.25 with a ×1.00 negative control.
>
> **This is a signature reproduced on better evidence than its own predicate could have delivered.**
> **Owed to the spec:** §6.2's S-1 control predicate must gain a coincidence-floor clause — *"the
> control leg is graded against the control's own measured A, not against 1.0, whenever
> `cooldown_seconds = 0.0` or no attack-speed model is compiled"* — plus `hits/press = 1.0` promoted
> from diagnostic to **co-equal predicate**. Filed at §A-8.3.

---

## §A-3 — S-2: **INSTRUMENT-VOID.** Both legs of my predicate are degenerate; the lever is live.

### A-3.1 The predicate is not merely unsatisfiable — it is also unfalsifiable, and the second half is worse

§6.2's S-2 predicate has two legs: **(a)** *"lifts B by ≥ 1.10×"* and **(b)** *"with A and C each within
their bootstrap CI of the no-DoT arm."*

Leg (a) was proven **UNSATISFIABLE BY CONSTRUCTION** by Gate-2's magnitude sweep (§14.31): B flat at
1.0000 on three of four tiers across **six orders of magnitude** of DoT magnitude — including a magnitude
that cuts boss kill-time 4.2× — and moving *against* the lever on the fourth. `A·B·C ≡ kills/encounter`,
and kills are pinned by design in a battery where every tier always clears.

**Leg (b) is the one nobody has yet named, and it is the more instructive failure.** Measured this lap
across all 150 matched fights per arm:

| arm | kills | **A** | **B** | **C** | A·B·C | kills/enc |
|---|---|---|---|---|---|---|
| W-c (`_fix3/g5`) | 720 | 1.7143 | 1.0769 | 2.6000 | 4.8000 | 4.8000 |
| R3 (`_fix3/g5_r3arm`) | 720 | **1.7143** | **1.0769** | **2.6000** | 4.8000 | 4.8000 |

**A and C do not move. They are bit-identical — and so is B.** Leg (b) therefore reads a *perfect pass*,
and it reads it for **exactly the reason leg (a) reads a null**: in a designed battery the whole A/B/C
frame is pinned, so all three components are constants and none of them can carry information about the
DoT. A predicate one of whose legs cannot fail and the other of which cannot succeed is not a hard test;
**it is not a test.**

**This is a defect in my own §6.2, and its root is nameable.** B was a live quantity in the *fixture's*
telemetry because encounter composition varied there. In a **composition-designed** battery it degenerates
into a residual of A and C. I banded a fixture-side quantity onto a sim-side battery of a different
epistemic kind, and did not check the arithmetic held under the change. **Same family as §2.3's defect —
a fixture instrument carried across a join that changes its meaning — and it is the second instance in
one spec.**

### A-3.2 The lever IS live — measured this lap, on post-registered instruments

Both reviewers converged on the same two re-expressions. Recomputed from `_fix3` traces this lap
(independent of gamora's and jack-ryan's extractors; my numbers reproduce jack-ryan's §5 table exactly):

| Instrument | W-c | R3 | Delta |
|---|---|---|---|
| **Boss mean kill-time** | **28.4500 s** | **26.0600 s** | ratio **0.91599**; paired **−2.3900 s**, sd 0.4693 |
| **Player DoT damage share** | **1.295 %** | **6.215 %** | **×4.80** |
| Player DoT rows | 90 | 3,182 | ×35.4 |
| Player DoT damage | 16,767.0 | 80,492.3 | +63,725.3 (the poison alone) |

**And a paired sign test I ran because a ratio of means is not a signal:** on the 60 seed-matched boss
fights, **R3 is faster on 60 / 60. Zero slower, zero tied.** Under a null of no effect that is
p = 2⁻⁶⁰ ≈ 8.7 × 10⁻¹⁹. The DoT lever is not marginally live; it is unanimously live where it can act.

**Where it *can* act is itself the finding — the DoT is overkill-gated, and I can now put a number on it:**

| arm | trash | champion | mixed_pack | boss |
|---|---|---|---|---|
| W-c DoT rows / share of player damage | 0 / 0.000 % | 0 / 0.000 % | **90 / 7.826 %** | 0 / 0.000 % |
| R3 DoT rows / share | 0 / 0.000 % | 0 / 0.000 % | 90 / 7.826 % | **3,092 / 6.542 %** |
| S-1c DoT rows / share | 0 / 0.000 % | 0 / 0.000 % | 90 / 7.826 % | 180 / 3.446 % |

**The canonical kit's own bleed reaches exactly one of four tiers.** Everywhere else the charge one-shots
its target and the G-4 liveness gate correctly refuses corpse-DoT. Paired per-tier kill-time deltas
confirm the confinement: trash **+0.0033 s** (29/30 tied), champion **+0.0067 s** (28/30 tied),
mixed_pack **+0.0133 s** (20/30 tied) — *nothing moves at the pack tiers*; the entire S-2 signal is
poison-on-boss. And the control's 180 boss rows against canonical's 0 measure the gating directly:
remove the line geometry, the charge stops over-killing, the bleed sticks.

### A-3.3 Grade — and the honesty the post-registration requires

The conductor asked me to find the true framing rather than a lenient-looking pass. Here it is.

> **S-2: INSTRUMENT-VOID — NOT counted as a reproduced signature; NOT counted as an absent one.**
>
> **Why not PASS.** The instruments above were **selected after** the registered one was found null.
> Their thresholds were never pre-registered. A ×4.80 DoT share and an 8.40 % kill-time cut *look* like
> a comfortable pass — but against **what band?** I could write "≥ ×1.10 in DoT share" now and clear it
> by a factor of four; that number would be chosen in full knowledge of the result it must admit. **A
> threshold authored after the measurement is not a threshold, it is a description wearing a predicate's
> costume,** and §6.0's arithmetic is over pre-registered predicates or it is over nothing. Counting S-2
> as reproduced would let a spec defect of mine buy the run a better verdict.
>
> **Why not FAIL.** §6.0 sentence 2's "signature absent" means *the sim was asked and could not*. The sim
> was never validly asked. The lever is connected, delivers unanimously at the only tier where a 5 s DoT
> can act before its target dies, and its confinement pattern is mechanically explained. Grading that a
> sim inadequacy would convert **my** instrument defect into **gamora's** calibration verdict — the same
> error R-KC1-23 refused to make with the fire-command omission, and it must be refused again here.
>
> **The honest grade is the third state: the DoT-tail effect is DIRECTIONALLY CONFIRMED and
> QUANTIFIED — kill-time ×0.9160, 60/60 paired, DoT share 1.295 % → 6.215 %, confinement mechanically
> explained — and the pre-registered claim it was supposed to test ("confined to B") remains
> UNTESTED, because the instrument that was supposed to test it does not exist in this class of
> battery.** For §6.0's purposes S-2 is not-reproduced, and it therefore cannot rescue the verdict —
> which is the *only* direction in which the ambiguity is allowed to resolve when the ambiguity is the
> grader's own fault.
>
> **Owed to the spec** (§A-8.3): S-2 must be re-registered on the kill-time-delta instrument with a band
> set from **fixture** data, before KIT-CAL-2 runs, and §6.2 must carry the general rule this lap
> learned: *a ratio-decomposition statistic whose product is pinned by battery design carries zero
> information about any intervention that does not change the product.*

---

## §A-4 — S-3: **NOT REPRODUCED.** Band-letter hit, signature absent. This is what decides the run.

### A-4.1 The letter passes. Both legs.

§6.2's S-3 predicate: *"A ×2.11 EHP step **plus** the itemised mitigation (§1.7) drives the ≥10 %-EHP
drop count to zero or near-zero **and** the p99 worst-drop below 12 % EHP — i.e. a fall in **normalized**
worst-hit, not merely in raw HP."*

| Leg | Sim, `_fix3` W-c → R3 | Reads |
|---|---|---|
| EHP step is ×2.11 | 759 → 1607 = **×2.1173** | ✓ |
| ≥10 %-EHP drop count → zero/near-zero | **0 → 0** (all cuts, all 300 fights) | ✓ |
| p99 worst-drop < 12 % EHP | **7.583 % → 3.581 %** (CUT-1); 7.898 % → 3.731 % (CUT-2) | ✓ |

**On the letter, S-3 is a clean sweep.** And that is precisely the situation §6.0 sentence 2 exists to
handle, because two of those three ticks are worthless.

### A-4.2 Both acceptance legs are VACUOUS — they were satisfied before the step

- The ≥10 %-EHP drop count is **0 on the pre-step side too.** A predicate asking the step to *drive* a
  count to zero cannot be evidenced by a count that starts at zero. Nothing was driven anywhere.
- The p99 worst-drop is **7.583 % pre-step** — already inside the "< 12 % post-step" target. The sim's
  hazard was inside S-3's finish line before S-3's race began.

T-5 already recorded the underlying fact (§4.1: the sim's hazard is *"a narrow band of constant chip"*).
What is new is that this collapse **makes S-3's acceptance test unable to discriminate**: any step at all,
including no step, would have passed both legs.

### A-4.3 And the claim the legs encode is measurably FALSE: the sim's step is pure SCALE

S-3's actual claim is in its title — *inverts hazard **SHAPE**, not just scale.* Measured this lap:

| Tier | median worst-drop **% EHP** | ratio | median worst-drop **absolute HP** | ratio |
|---|---|---|---|---|
| trash | 6.0458 → 2.8555 | **×2.1173** | 45.887 → 45.887 | **×1.0000** |
| champion | 7.0889 → 3.3481 | **×2.1173** | 53.805 → 53.805 | **×1.0000** |
| mixed_pack | 7.0863 → 3.3469 | **×2.1173** | 53.785 → 53.785 | **×1.0000** |
| boss | 7.8023 → 3.6946 | ×2.1118 | 59.219 → 59.372 | ×0.9974 |
| | | **EHP pool ratio = ×2.1173** | `worst_drop_abs` **identical on 143 / 150 matched fights** | |

**The normalized fall equals the pool ratio to five significant figures, at every pack tier, exactly.**
The sim's gear step changes the denominator and *nothing else*. There is no mitigation on the step —
`mitigation_delta` was never pinned (BQ-3; the galadriel armour re-crop residual). The 7 fights whose
absolute drop differs are boss fights, and they differ by 0.26 % — the poison shifting which incoming
hit happens to be the worst, not any change in what a hit costs.

**Against the fixture, quoted verbatim from §6.2 and NOT recomputed:**

| | fixture | sim |
|---|---|---|
| EHP step | ×2.11 | ×2.1173 |
| p99 worst-drop, normalized | 33.02 % → 7.38 % = **×4.474 fall** | 7.583 % → 3.581 % = **×2.117 fall** |
| **normalized fall ÷ EHP ratio** | **2.12** | **1.000** |
| max single drop | 72.42 % → 8.50 % = ×8.52 | 7.587 % → 3.583 % = ×2.117 |
| drops ≥ 10 % EHP | **27 of 332 → 0 of 109** | 0 → 0 |

**Half of the fixture's fall came from somewhere other than the pool.** That "somewhere" is the itemised
mitigation the predicate names in its own text — the ≥125 Armor, the amatok aura's +16, the 18 %
Physical→Acid conversion (§1.7). The sim's fall came **entirely** from the pool. The fixture inverted a
distribution that carried 8.1 % of its drops above the 10 %-EHP line into one carrying 0 %. The sim
rescaled a distribution that had no drops above that line either side.

> **S-3: NOT REPRODUCED. The band letter reads HIT; the signature is ABSENT.**
> **Category (iv) mechanism-class absence** — itemised mitigation is not modelled on the gear step
> (BQ-3, known and named in the predicate's own honorable-fallback column: *"(iv) if it survives because
> player defence cannot be pinned"*). The predicate **pre-committed this attribution before results**,
> which is why it can be applied now without any appearance of convenience.
>
> **This single row decides the run.** It is the only signature on the table that was fully executed,
> fully instrumented, and still measurably failed to reproduce — and the failure is not a tuning
> distance. The sim cannot express a shape inversion because it has no shape to invert and no
> mitigation to invert it with.

---

## §A-5 — KEEPER (2) RE-READ, and a correction to keeper (3)'s stated evidence

### A-5.1 Keeper (2) — "the A/B multi-kill statistics invert" — **TRANSFORMS. Survives descriptively, dies interventionally, and REROUTES.**

The keeper as banked: sim A 2.25 vs fixture 1.76; sim B 1.12 vs fixture 2.41 — *"the one genuine
category-(ii) sim-mechanics delta on the table."* Against the residual-B degeneracy of §A-3.1, three
rulings, in increasing order of consequence:

1. **The DESCRIPTIVE half SURVIVES intact.** B's degeneracy is a statement about B's **response to an
   intervention**, not about B's **level**. The sim's kills genuinely do bunch into single kill-events
   where the fixture's chained across a burst, and the fixture's B = 2.4141 was measured on a
   composition-*sampled* window where nothing was pinned. The comparison of levels is legitimate. *(It
   remains cut-contingent per §2.3: sim B reads 1.1429 / 1.1000 / 1.0769 on CUT-1 / CUT-2 / all-150
   against the fixture's 2.4141 — the direction and rough magnitude are robust to the cut; the exact
   ratio is not.)*
2. **The INTERVENTIONAL half DIES.** T-5's §7.2 item 1 called this *"the highest-value item on this
   list… all present, all tunable. Route to gamora."* **That routing was wrong and I am retracting it.**
   In a designed battery B cannot be moved by anything that does not move kills-per-encounter. There is
   no B knob. Any future lap that tries to "tune B toward 2.41" will be tuning a residual.
3. **And the control tells us what A and B actually are — one fact, seen twice.** Removing the arc
   geometry moves the sim **A 1.7143 → 1.4150** and **B 1.0769 → 1.2714** at constant kills (720 → 716).
   A falls and B rises *together*, because both are readings of the same thing: **how many kills land
   inside one 0.5 s bin.** They are not two deltas; they are one. And its root cause is now named —
   claws at `cooldown_seconds = 0.0`, **no player attack-speed model** — which is the identical mechanism
   that produced S-1's coincidence floor.

> **Keeper (2) disposition: TRANSFORMED, and REROUTED from calibration to wave-inheritance.**
> It is no longer *"the highest-value calibration delta"* and it is no longer gamora's to tune. It is
> **one mechanism-class absence — the attack-speed model — presenting as two statistics.** It moves from
> T-5 §7.2 (closable by the current build class) to **Q-KC1-1 wave inheritance**, alongside frigidring
> and dodge-on-tell. **This is the single largest change the amendment makes to the join-forward.**
> *(Its category also shifts: T-5 filed the N-5 miss as category (ii) sim-mechanics divergence. With
> `cooldown_seconds = 0.0` and no attack-speed model measured at source, it is category **(iv)**.)*

### A-5.2 Keeper (3) — "the arc is narrower" — **CONCLUSION SURVIVES; its T-5 EVIDENCE is SUPERSEDED.**

Gate-2 resolved the 1.36-vs-2.58 contradiction as **aggregation scope, no computational error on either
side**: T-5's §4.3 pooled three tiers ex-boss (1374/1009 = 1.3617); gamora quoted trash alone
(253/98 = 2.5816); **neither is a valid §1.1p comparator** — the pool is 75 % mixed_pack, and adding the
boss's 2,082 presses swings it to 1.1485. The `_fix3` canonical breadth, per tier:

| Tier (mobs) | hits/press | vs fixture 2.362 |
|---|---|---|
| trash (8) | **2.5714** | +8.9 % — **the arc is RIGHT at fixture-comparable density** |
| champion (4) | 1.5855 | −33 % |
| mixed_pack (6) | 1.1770 | −50 % |
| boss (3) | 1.0447 | −56 % |

**The conclusion — "do not tighten the target cap" — SURVIVES on strictly better evidence than it was
born with:** `max_targets` is read **nowhere** in the engine (the cap never binds; max observed hits/press
anywhere = 4 against a cap of 5), and `CONE_HALF_ANGLE_RAD = π/4` puts the A2 premise at source. **The
stated evidence in T-5 §4.3 — "the sim's arc hits 1.36 targets per press… breadth is under-delivered" —
is superseded**: 1.3617 is a composition artifact of a 75 %-mixed_pack pool, not a breadth measurement.
**Restated density-conditional:** *the cone delivers fixture-comparable breadth at 8-mob density and
under-catches monotonically as spacing opens.* T-5's actual backlog instruction (re-scope BQ-1/BQ-2 from
"is the cap too generous" to "why does the cone under-catch at mixed-pack spacing") was **right, and is
now right for the correct reason.**

*(Keeper (1) — the hazard distribution collapsed to its middle — is untouched by this lap: N-7 through
N-12 are unmoved to 4 dp in `_fix3`, §A-6.)*

---

## §A-6 — BAND DELTAS: six series move, **ZERO verdicts change**

Recomputed from `_fix3/g5` by the identical §2.2 script against T-5's pre-fix values (`kitcal_g5/g5`
@ `bef1f55`). Per R-KC1-23, unchanged series are **not re-litigated**.

| # | Band (§6.3, pre-registered) | CUT-1 pre → **`_fix3`** | CUT-2 pre → **`_fix3`** | T-5 grade | **Terminal grade** |
|---|---|---|---|---|---|
| N-1 | 3.0 – 7.0 s | 4.4000 → **4.4000** | 7.3000 → **7.1000** ⟵ moved | CUT-DEPENDENT | **CUT-DEPENDENT** *(unchanged; ⚠ see below)* |
| N-2 | 1.10 – 1.80 | 1.4503 → **1.4237** ⟵ | 1.6316 → **1.6635** ⟵ | PASS | **PASS** (robust) |
| N-3 | ≥ 18 s present | 11.500 → **10.400** ⟵ | 30.300 → **29.800** ⟵ | CUT-DEPENDENT | **CUT-DEPENDENT** |
| N-4 | 1.45 – 2.10 | 2.2500 → 2.2500 | 1.9091 → 1.9091 | CUT-DEPENDENT | **CUT-DEPENDENT** |
| N-5 | 1.95 – 3.00 | 1.1163 → **1.1429** ⟵ | 1.0820 → **1.1000** ⟵ | MISS (low) | **MISS** (low, robust) |
| N-6 | *non-target* | 2.3889 → **2.3333** ⟵ | 2.5417 → **2.5000** ⟵ | NOT SCORED | **NOT SCORED** |
| N-7 | 0.228 – 0.528 | 0.0000 → 0.0000 | 0.0000 → 0.0000 | MISS | **MISS** |
| N-8 | 0.5 % – 5.0 % | 51.1655 → 51.1655 | 63.2854 → **63.8445** ⟵ | MISS (high) | **MISS** (high) |
| N-9 | 0.8 % – 5.0 % | 6.8745 → 6.8745 | 7.0889 → 7.0889 | MISS (high) | **MISS** (high) |
| N-10 | 8 % – 30 % | 7.3374 → 7.3374 | 7.8297 → 7.8297 | MISS (low) | **MISS** (low) |
| N-11 | ≥ 40 % present | 7.5874 → 7.5874 | 7.9036 → 7.9036 | MISS | **MISS** — *see below* |
| N-12 | 30 % – 65 % | 0.0000 → 0.0000 | 0.0000 → 0.0000 | MISS | **MISS** — *NOT-RECUT carried* |

**Six series moved; no grade did.** The woken charge bleed contributes 16,767 HP — **1.295 %** of player
damage, and *all of it at mixed_pack* — which is why the deltas concentrate in the duration bands
(mixed_pack mean elapsed 10.500 → 10.160 s) and why N-4, N-7, N-9, N-10, N-11, N-12 are unmoved to 4 dp.
Kills 720/720 and wins 150/150 both sides. **The DoT repair was indispensable for instrument integrity
and immaterial to the band table** — which is itself the cleanest possible statement of how small the
canonical kit's DoT channel is, and worth one line in the wave brief.

> ⚠ **N-1 is now fragile and was not before.** CUT-2 moved 7.300 → **7.100** against a band ceiling of
> **7.0 s**. It remains a miss on CUT-2 and the grade is unchanged, but it now sits **0.1 s** outside a
> band it was 0.3 s outside. Any further tempo movement flips N-1 from CUT-DEPENDENT to weighting-robust
> PASS. **Do not quote N-1 as a stable miss.** *(And per §7.3 it is not citable either way until §6.3
> gains its tier-weighting rule.)*

**N-11 and N-12, restated as instructed and not re-argued.** N-11 stays **MISS**, attributed **wholly**
to category (iv) mechanism-class absence (frigidring / HALT-2 / H-1). It is **not** evidence of a
calibration error in any pinned operand and **must never be quoted as one**. N-12 stays MISS and carries
P-4's **NOT-RECUT** non-stationarity caveat, which remains non-binding on a numerator of zero. The §5
competing NOT-EVALUABLE reading remains respectable and remains carried to Matt veto-open; the terminal
verdict is FAIL either way, since §6.0 sentence 2 is now decided by S-3 rather than by N-11.

**§6.4's qualifier, carried as required** (*"this qualifier travels with every §6.3 row, always"*): the
fixture's W-c distribution has a three-point mass at its end carrying **50.9 %** of measured intake.
N-10 and N-11 read *"the fixture is capable of this,"* not *"the fixture does this routinely."*

---

## §A-7 — §6.0 APPLIED, AND WHY THE THIRD GRADE WAS REFUSED

### A-7.1 The arithmetic

- **Sentence 1** — *"A band miss with all three structural signatures reproduced is a PASS with a tuning
  note."* Precondition: **all three**. We have one reproduced (S-1), one instrument-void (S-2), one
  absent (S-3). **Does not fire.**
- **Sentence 2** — *"A band hit with a signature absent is a FAIL."* S-3's band-letter legs both read
  **hit** (§A-4.1) and S-3's signature is **absent** (§A-4.3). **Fires verbatim.** This is the first lap
  of the run with a battery complete enough for sentence 2 to fire on substance rather than on coverage.
- **Sentence 3** — *"G-5 runs the coverage gate FIRST."* Run at §A-1: **6 of 6 legs**, against T-5's 1 of 6.

### A-7.2 What changed between the two verdicts, said plainly

| | **T-5** | **Terminal** |
|---|---|---|
| Cause of failure | **Coverage** — 5 of 6 legs unrun (conductor fire-command omission) | **Substance** — S-3's mechanism is absent |
| Signature census | 0.5 reproduced / 2.5 unrun | 1 reproduced / 1 instrument-void / 1 absent |
| Band verdicts | 1 PASS / 7 MISS / 3 cut-dep / 1 unscored | **identical** |
| Owner of the dominant miss | the conductor | **the build class** (BQ-3, mitigation modelling) |
| Highest-value "closable" delta | N-5 / A–B inversion → gamora | **retracted** — it is the attack-speed model → wave |

**The letter of the verdict did not move across four repair laps and roughly a dozen instrument
failures.** Everything underneath it did. A verdict that survives the repair of every instrument that
produced it is a verdict one can act on.

### A-7.3 Why NOT `CONDITIONAL` — the grade I was explicitly offered and am declining

The conductor's charge named CONDITIONAL as an available re-grade. I decline it, and the reason matters
more than the decline.

CONDITIONAL means *"pass, pending X."* Here X would be **itemised mitigation on the gear step** — a
mechanism that **does not exist**, was **named absent before the run** (BQ-3), and is **already
represented** in the grading vocabulary by honorable-fallback **category (iv)**, which expresses it as a
**FAIL with a named owner and an acceptance target**. Category (iv) is not a softer FAIL; it is a FAIL
that tells you who owns it. Introducing CONDITIONAL would add nothing except a milder word — and it
would add it **at grading time, after seeing the result, on a rubric that pre-registered exactly two
outcomes.** That is goalpost movement in its softest and most defensible-sounding form, which is the
form this role exists to refuse. §5 refused the same move on N-11 when the softer reading favoured the
sim; refusing it again when the softer reading favours the **run** is the same discipline, pointed the
harder direction.

**The verdict is FAIL. It is honorable, fully decomposed, and every residual has an owner.**

---

## §A-8 — JOIN-FORWARD: the split HQ-3 hands the wave charter

### A-8.1 The table

**Column key.** *Wave* = Q-KC1-1 inheritance — a mechanism the current build class **does not have**;
un-closable by calibration; needs a named acceptance target in the wave charter. *Calibration* = closable
now, by the current build class, in-seam. *Spec* = a defect in kit spec v2 that this seam owns.

| # | Residual | Evidence it owns | **Class** | Owner / route |
|---|---|---|---|---|
| 1 | **frigidring / telegraph-burst modeling** | **N-11** (7.90 % vs ≥ 40 %), **N-12** (0 % vs 30–65 %), most of **N-10** | **WAVE** (iv) | wave charter; acceptance = death-2 trajectory (R-KC1-22); target: single hit ≥ 40 % of pool becomes *possible*; ≥10 %-EHP drop share reaches 30–65 % |
| 2 | **evasion / dodge-on-tell** | **N-7** (0.000 vs 0.378), **N-8** (51 % vs 1.79 %), **N-9** (6.87 % vs 1.79 %) | **WAVE** (iv) | wave charter; acceptance = Matt's winning attempt (§14.24); target: zero-intake fraction into 0.228–0.528 |
| 3 | **player attack-speed model** *(NEW — promoted from calibration this lap)* | **N-5** (1.14 vs 2.41), **N-4**'s CUT-1 high side, S-1's coincidence floor, **keeper (2) in full** | **WAVE** (iv) | wave charter. Root: claws compile `cooldown_seconds = 0.0`; A and B are one bin-occupancy fact seen twice (§A-5.1) |
| 4 | **itemised mitigation on the gear step (`mitigation_delta`, BQ-3)** *(NEW — S-3's cause)* | **S-3** — the signature that decides the run | **WAVE** (iv) | wave charter; acceptance = normalized-fall ÷ EHP-ratio must exceed 1.0 (fixture reads **2.12**; sim reads **1.000**). **Carries the galadriel armour re-crop residual** |
| 5 | **hero-slot semantics** | boss-tier only; no band directly | **WAVE** | carried as-is (`A-HP-3` hero slot = MEASURED 4702) |
| 6 | **crit labelling (HALT-3)** | blocks crit-decomposition of N-4 / N-5 | **WAVE** (trace call site, not a mechanism) | wave charter |
| 7 | **freeze-CC (H-1-adjacent)** | no band surface | **WAVE** | joins the ledger beside evasion |
| 8 | **BQ-4 / `battle_surge`** | no band; §14.26 no-flip | **WAVE, re-open** | **the no-flip verdict is scoped to the chip regime.** Re-test *after* burst + dodge land; must NOT be inherited as settled |
| 9 | **no-`else` silent fall-through** (`resolve_skill`, 26 handled names) | the defect that voided S-2's lever for a whole lap | **WAVE** (Discipline #8) | Gate-2 §14.31 recommended shape: derived frozenset + strict-raise behind a flag |
| 10 | **Battery composition coverage** | **N-1, N-3** cut-dependence; part of N-4's | **CALIBRATION** | gamora — G-5a declares Act-1 pools 1–8 / 2–9 / 3–10 / **8–16**; the battery ran three fixed points (8/4/6) and never the large pool. **Sweep density; do not fix it** |
| 11 | **Chained-encounter attrition scenario** | no band — *the band table cannot see it* | **CALIBRATION** | gamora — sim takes a median **51 %** of pool per pack encounter and wins 30/30 because encounters are isolated. The fixture's player chained **49**. Nothing in the battery tests the chain |
| 12 | **Arc breadth at open spacing** (BQ-1/BQ-2 re-scope) | keeper (3), density-conditional | **CALIBRATION** | rocket (cone geometry) + gamora (spacing/formation) — *not* a cap change; `max_targets` is read nowhere |
| 13 | **`arm_a_jitter = false`** | named deviation; immaterial to every verdict | **CALIBRATION** | gamora — cheap to close; leaving it open leaves a named deviation standing in the record |
| 14 | **§6.3 tier-weighting + boss-tier window membership** | **N-1, N-3, N-4** not citable either way until closed | **SPEC** | this seam (§7.3, unchanged) |
| 15 | **§6.2 S-2 predicate re-registration** | S-2's instrument void | **SPEC** | this seam — re-register on kill-time delta with a **fixture-set** band, before KIT-CAL-2 |
| 16 | **§6.2 S-1 coincidence-floor clause** | S-1's band-letter miss | **SPEC** | this seam — grade the control against its own measured A; promote `hits/press` to co-equal predicate |

### A-8.2 The split, counted

| Class | Count | Bands it owns |
|---|---|---|
| **Q-KC1-1 WAVE INHERITANCE** (mechanics not yet built) | **9** (#1–9) | **8 of the 10 non-passing bands** — N-4*, N-5, N-7, N-8, N-9, N-10, N-11, N-12 · **plus S-3** |
| **CURRENT-CLASS CALIBRATION** (closable now) | **4** (#10–13) | **2** — N-1, N-3 (both via battery composition; both also blocked on the §6.3 spec fix) |
| **SPEC — this seam's own** | **3** (#14–16) | N-1/N-3/N-4 not citable until #14; S-1 and S-2 predicates defective |

\* N-4 is **double-attributed**: primary WAVE (attack-tempo compression, #3), secondary SPEC (#14,
join-construction — it is cut-dependent).

**The headline for the wave charter:** *eight of the ten non-passing bands, and the one signature that
decides the verdict, are owned by four mechanisms that do not exist yet — burst, evasion, attack-speed,
and mitigation. Two bands are owned by a battery that never swept its declared density range. Zero are
owned by a mis-pinned operand.* **Every G-5 dataset in `_fix3` is the before-baseline** for all of it:
450 fights, 30 seeds, `67e7ccb`, deterministic traces, coverage 1.0. Every row above has a number to
beat, which it did not have before this run.

### A-8.3 Owed to the spec, consolidated

Kit spec v2 cannot be quoted again until three amendments land: **§6.3** gains a tier-weighting rule and
an explicit boss-tier window-membership clause (§7.3, unchanged); **§6.2 S-2** is re-registered on an
instrument that is not a pinned residual; **§6.2 S-1** gains its coincidence-floor clause. All three are
**spec amendments, not re-grades** — every band and every predicate in this run stays exactly as
pre-registered.

**The general rule this run taught the spec, worth carrying to KIT-CAL-2 above all the specifics:**
*a fixture-side statistic does not keep its meaning when carried onto a designed battery. The fixture's
window was composition-**sampled**; the sim's is composition-**designed**. Every statistic whose value
depends on what varied — B, and every tier-weighted aggregate — degenerates across that join.* Two of
this spec's twelve bands and one of its three signatures were defective for that single reason, and it
was foreseeable.

---

## §A-9 — CARRIED CAVEATS — restated, NOT resolved

Every one of these stands open and travels with any quotation of this verdict:

1. **`arm_a_jitter = false`** — named deviation from R-KC1-18 as written: flat 5.0 % against the
   measured 3.25–6.75 % range. Immaterial to every grade in this document (the flip rule resolved with a
   281–345 HP inter-arm gap; intra-arm jitter cannot reach it). **Recorded, not smoothed.**
2. **The 1.61-vs-1.10 regen-floor discrepancy — UNRESOLVED.** Carried from the charter; not touched by
   any repair lap; not load-bearing on any grade above, and it must not be cited as though it were settled.
3. **The galadriel armour re-crop residual (`mitigation_delta` pin)** — the operand whose absence is
   S-3's proximate cause (§A-4.3). Named absent before the run (BQ-3); still absent; now with a
   measured consequence (normalized-fall ÷ EHP-ratio = **1.000** against the fixture's **2.12**).
4. **N-12 NOT-RECUT (P-4)** — the fixture value is at R2-whole grain and cannot be re-cut to W-c from
   the store. Non-binding here only because the sim numerator is zero on every cut.
5. **Leech `capacity` / `healed` are NON-POOLABLE across fix generations** (Gate-2 **SS-1** extension,
   C-6): `delivered` is HP-pinned, so DoT gain is exactly offset by direct-hit loss and
   `leech_capacity_total` falls by `Δ_DoT × door_pct`. `_fix`, `_fix2` and `_fix3` leech totals must
   never be pooled with each other or with `kitcal_g5/`.
6. **Gate-2 residuals open at CONDITIONAL PASS** — **WARN-1** (the overwrite guard sits at the
   report-write site, not the trace layer; 5 traces can land in a protected directory before the refusal
   fires — and 5 such files sit in `kitcal_g5/smoke/traces/` today) · **WARN-2** (SS-6 wording:
   5 Δ=1.0 cells coalesce rather than shift; zero exposure at shipped Δ ∈ {0.1, 0.5}) · INFO-1…INFO-4.
   All in-seam, none blocking; gamora's to close at her discretion.
7. **§5's N-11 competing NOT-EVALUABLE reading** remains respectable and remains carried to Matt
   **veto-open**. It changes the MISS count (10 vs 9 on the conservative binary) and changes nothing else.
8. **`_fix2` is final in substance; `_fix3` supersedes in provenance only** — 33 headline cells, 0 moved;
   450 traces byte-identical with the header hash stripped. `_fix3` is read here because it is the
   generation whose stamp (`67e7ccb`) resolves to the kernel that produced it.

---

## AMENDMENT PROVENANCE

- **Sim side, all MEASURED this lap** from `output/kitcal_g5_fix3/{g5, g5_r3arm, g5_s1control}`
  @ `67e7ccb`, tag `gamora/v-dot-delivery-2`, run `KC1-2026-07-27`, harness `harness-v1`, seed base
  74000800, 30 seeds × 5 cells × 3 arms = 450 fights. Band arithmetic by the **identical §2.2 script**;
  breadth, DoT-share and paired kill-time deltas recomputed from the 450 traces by an extractor written
  this lap. My DoT-share figures (1.295 % / 6.215 % / 3.887 %; totals 1,295,220.00 and 16,767.00) and my
  boss kill-time ratio (0.91599) **reproduce jack-ryan's §5 table exactly** on an independent extractor
  — cross-check, not citation.
- **Fixture side:** every value quoted verbatim from kit spec v2 §6.2 / §6.3 / §6.4. **No fixture value
  was recomputed in this lap or the last** — recomputing the goalposts at grading time is the failure
  mode this discipline exists to prevent.
- **Pre-fix comparison values** for §A-6 read from `output/kitcal_g5/g5/` @ `bef1f55` — the T-5
  canonical battery, which is *not* quarantined (only `kitcal_g5/g5_r3arm/` and `kitcal_g5/smoke/` are).
  The quarantined artifacts were opened by nothing in this lap.
- **Certification chain:** `…-gate2-gamora-g5-s1control.md` (control CONDITIONAL PASS; coincidence floor
  verified at event level; 1.36-vs-2.58 resolved) → `…-gate2-gamora-g5-dotfix-addendum.md` (BLOCK lifted;
  census verified 5.7× broader; B proven unsatisfiable by construction) →
  `…-gate2-gamora-dot-tick-delivery-r-kc1-25.md` (BLOCK, with appended §3.2 correction) →
  `…-gate2-gamora-dot-delivery-2-rereview.md` (**CONDITIONAL PASS — the certification this lap rests on**).
- **Grading status:** every grade in this amendment is **veto-open** per the run's ledger convention.
  The conductor carries §A-4 (S-3 as the deciding row), §A-5.1 (keeper (2)'s reroute out of gamora's
  lane) and §A-7.3 (the CONDITIONAL refusal) to Matt explicitly.

**Signed:** gandalf (`DRIFT-CRITIC`), **amendment lap**, 2026-07-28.
