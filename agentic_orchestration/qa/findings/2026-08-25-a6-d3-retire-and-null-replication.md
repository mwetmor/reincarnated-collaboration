# Finding — 2026-08-25 — A-6 / D3 disposition, S2B tranche-2 close

**Reviewer:** jack-ryan
**Severity:** INFO (D3 disposition) + one new discipline minted
**Target:** no tag — tranche-2 close precondition, not a Gate-2
**Developer:** n/a (this is my own Gate-1 criterion being disposed of)
**Principles applied:** #1 math-before-code, #2 smoke-gate, #4 decisions-log as truth, #5 severity matters

---

## 1. D3 — **A-6 is RETIRED.** Not defaulted-to-retire; refuted.

The gate said: *answered via D3 (a pre-registered, spec-predicate-selected null
population), or RETIRED with its reason recorded.* **The reason is recorded here, and it
is that D3's unblocking criterion cannot be met on this corpus — not that it ran out of
time.**

### 1.1 Reproduction first

Operator read at source (`s2b_xrow_rows37.py`), not from description. Receipt reproduced
from `xrow.json`'s `arms` array before anything new was derived: `null_mean` 0.5088,
`null_max` 3.6678, and all five per-row means/maxes identical to `NULL_COMPOSITION`.
KR's § 9.2 two-deletion table also reproduces exactly (`single_target` 1.5987 → 1.0020
on eight descriptors; four rows unchanged to 4 dp). **§ 9.2 is confirmed. § 9.3 is not.**

### 1.2 ⚑ The decisive test: **the within-row null does not replicate across the two stage cohorts — on any row, including the spec-clean one.**

The corpus contains two independent cohorts (`cathedral`, `arena`) measuring the *same*
element pairs of the *same* rows. The operator correctly never pools them. **That makes
each element pair a two-fold replicate, and nobody had read it that way.** Median
|relative difference| between the two readings of the same element pair, 8-descriptor set:

| row | median px | median cross-stage |Δ| | null mean |
|---|---:|---:|---:|
| line | 11,475 | **19.2 %** | 0.4114 |
| circle | 127,746 | **25.7 %** | 0.2330 |
| single_target | 1,740 | **49.4 %** | 1.0020 |
| multi_projectile | 5,446 | **56.8 %** | 0.3447 |
| **melee_arc** | 22,117 | **76.4 %** | 0.2426 |

**`melee_arc` — the one row drax certified as element-holds-shape-constant, "the tightest
invariance in the whole gate" — replicates worst.** Its `fire`/`water` pair reads
**0.6011 at cathedral and 0.1610 at arena**: a 3.7× swing on the same element pair, same
descriptors, same instrument, on a row whose arms are supposed to be the same shape.

The raw table shows why: `melee_arc`'s **stage** shift dwarfs its element spread —
`fill_of_bbox` 0.335–0.365 (cathedral) vs 0.422–0.446 (arena), `authored_px` ~18k vs ~26k.
**The within-row null carries a stage-interaction term of the same magnitude as itself.**

### 1.3 Why that retires A-6 rather than repairing it

D3 asked for a **spec-predicate-selected** null population. The spec predicate ("element
varies tint only") selects exactly one row on this tranche: `melee_arc`. **The predicate
selects the population with the worst replication in the corpus.** A bar carrying ~76 %
relative uncertainty, estimated from one row, then transported to cross-row pairs on rows
of different payload and different stage response, is not a bar. And A-6's criterion
consumes `null_max` — a global **maximum** over 76 pairs — the statistic most inflated by
an unstable term.

**A criterion whose null leg has no valid population is not suspended pending better data.
It is mis-specified. I wrote it. I retire it.** Tranche 2 seals without a cross-row number.

**What is NOT retired:** the *questions* Q1–Q5 remain open and worth answering. What is
retired is the specific null-referenced criterion. The `ANTI_TUNING_CLAUSE` survives
retirement in full — retiring the criterion is not a licence to differentiate any effect.

---

## 2. ⚑ KR's payload hypothesis (§ 9.3) is **REFUTED**. Three directional predictions, all backwards.

Saying so is what was asked for. The hypothesis: descriptors are ratios of pixel counts,
computed on masks ~70× smaller on some rows, so quantisation wobble is amplified by the
z-score.

1. **Leave-one-arm-out points the wrong way.** The most influential arm on the no-sig row
   is `single_target/fire` — dropping it takes the row 1.0020 → **0.6206**. Fire is the
   **largest** payload in the row (2,699 / 2,548 px vs 1,446–1,813). Quantisation noise
   predicts the *smallest* arm dominates. It is the largest.
2. **The descriptors driving it are the quantisation-ROBUST ones.** Share of
   `single_target`'s within-row squared distance: `radial_mean` **0.2835** +
   `radial_std` **0.2291** = **51 %**. Both are moments averaged over all *n* pixels —
   the most stable statistics in the set. The extremum-normalised descriptors the
   hypothesis indicts (`fill_of_bbox` 0.166, `major_over_diag` 0.051, `outer_shell_frac`
   0.011) total 0.228.
3. **A second payload inversion, unnamed in § 9.3.** `melee_arc` (22,117 px) has *higher*
   within-row CV than `multi_projectile` (5,446 px) on four descriptors — `fill_of_bbox`
   0.1103 vs 0.0331, `major_over_diag` 0.0588 vs 0.0136, `inner_core_frac` 0.1696 vs
   0.0427, `outer_shell_frac` 0.1486 vs 0.0850. **4× the payload, 3–4× the variation.**
   KR named one inversion; there are at least two, and the second is on the row he treats
   as well-behaved.

**And the positive account:** `single_target/fire` is genuinely a different shape, and it
**replicates** — `radial_mean` 0.4855 (cath) / 0.4559 (arena) against 0.373–0.407 for the
other three elements at both stages; `fill_of_bbox` 0.67/0.64 against 0.52–0.58.
**Quantisation noise does not reproduce across two independent cohorts. Signal does.**
`single_target`'s elevated null is the element motif swap drax already declared by spec —
**his original account was right and did not need replacing.**

**Rank order of null means is still roughly payload-ordered. That correlation may be real.
The proposed mechanism is not the cause of it.**

---

## 3. Ruling on the sequencing question (KR routed; I decide)

**The test is not "is it structural?" — it is: could the outcome, if known, change which
criterion I would choose, in a direction that makes a particular verdict more likely?**

- **The `circle`-decimation variant is NOT purely structural.** It recomputes *the
  within-stage null* — one of the two terms in A-6's own criterion — in the units of the
  scored corpus. Knowing its answer tells me which null population makes A-6 evaluable.
  **That is criterion selection with knowledge of the result. It was correctly withheld
  until D3 was disposed.**
- **The synthetic-mask variant IS purely structural** and is **authorised at any time,
  before or after pre-registration.** It removes corpus data from the loop entirely and
  measures a property of the descriptor functions, not of the artifacts. **KR's instinct
  to offer it was right and it is the version that should exist.**
- **Precedent, stated generally so it binds beyond this instance:** *a diagnostic that
  touches the scored corpus may run before pre-registration only if it cannot change the
  criterion. A diagnostic that recomputes a TERM OF THE CRITERION never qualifies —
  synthesise the input instead, or run it after disposition.*
- **Practical note, non-binding:** the decimation test is now largely mooted.
  `radial_mean` / `radial_std` are scale-normalised by construction (`r / rmax`, averaged
  over all *n*) and are near-invariant to subsampling in expectation. They are 51 % of the
  residual. **The test would very likely return "circle's null does not rise" — the
  conclusion § 2 above already reaches, more cheaply.** galadriel may run it as an
  instrument finding; it is no longer on A-6's path.

---

## 4. Discipline — minting **ONE** from the whole set, per KR's request

Five candidates were queued. **They are one discipline, and #75 cl. 2 already holds its
mirror half.** #75 cl. 2: *a separation instrument never shown to return DISTINCT on a
known-distinct pair is not an instrument.* That is the **positive** control. Every one of
the five candidates is the **negative** control missing.

### ⚑ Discipline #80 — **A gate's green is not evidence until that gate has been shown to go red, on this population, in this configuration.**

**Clause 1 — region.** A gate that measures a region must publish what is *in* the region,
not what the region is *named*. Three instances this run, worst at 99.6 % sky in a region
labelled `enemies`. **A region that cannot contain the failure cannot report it.**

**Clause 2 — the bar.** A threshold whose difficulty is set by the quantity it measures,
or which has no reachable failing branch, is not a bar. Instances: A-6's own null leg
(this finding); the `5378300000.0x` zero-denominator ratio; the S-A3 self-referential bar
and register-2 bloom gate (**those two are gandalf's to rule on — named, not merged**).

**Clause 3 — prose.** *drax's candidate, adopted verbatim as the clause title:* **"a fix
ported in prose is a fix that reads as adopted."** Three of four `VERBATIM` instances on
one file carried a sentence asserting a parity the code did not have. **My sharpening,
which is the operative half: an unasserted parity gets checked; an asserted one does not.
The sentence is load-bearing in the wrong direction — it is a negative control that
prints green by construction.**

**Founding positive instance, and it is from this run:** drax's
`wwcr_2026-08-25-PROBE-noneutralise/` retained corpus returning `count: 1`, built on his
own reasoning — ***"'fixed' and 'blind' print the same zero."*** **#80 is that sentence
generalised.** The discipline is minted with a worked example of compliance, not only of
breach.

**Binding form:** #80 attaches to any instrument, gate or assertion admitted as evidence
at a Gate-2. It requires a **named, retained artifact that makes the gate fail** —
retained, not merely run, per #66.

**Canonical write to `engineering-disciplines.md`: OWED, not yet made.** Under ADR-002 I
hold approval authority for the documentation write; I am sequencing it with KR's #78
cl. 6 write (owed to drax) so both land in one edit rather than two.

---

## 5. Actions

- [x] **jack-ryan:** D3 disposed — **A-6 RETIRED**, reason recorded (§ 1). Tranche-2's
      A-6 precondition is **DISCHARGED**. Nothing blocks the seal on my side.
- [ ] **jack-ryan:** write #80 + #78 cl. 6 into `engineering-disciplines.md` (one edit).
- [ ] **knight-rider:** § 9.3's payload mechanism is refuted — amend the ruling; it is
      currently the mechanism of record. § 9.2 stands.
- [ ] **galadriel:** decimation test **downgraded to optional** and moved off A-6's path;
      **synthetic-mask variant authorised**, `circle`-mask variant now also unblocked
      (D3 disposed) but as an instrument finding only.
- [ ] **gandalf:** clause-2's two unfalsifiable-bar instances (S-A3, register-2 bloom)
      remain **his** to rule on. Named here, deliberately not merged.

## 6. Flags on my own finding

- **§ 1.2's replication read is new and is mine.** It appears in no return. It is derived
  from `xrow.json`'s `arms` array with the operator's own z-scoring and pairing rules
  reproduced from source. It should be re-derived rather than adopted — **the exact
  instruction KR gave me about § 9, applied to myself.**
- **My first reading of the leave-one-out table was wrong.** The cathedral/arena values
  matching to 4 dp looked like perfect cross-stage replication; it is an averaging
  artifact. I checked it directly and found the opposite. Recorded because the wrong
  version was briefly load-bearing in my own reasoning.
- **I am retiring my own criterion.** Discipline #80 clause 2 convicts A-6's null leg by
  name, and A-6 is mine. Recorded so the mint does not read as aimed outward.

## References

- `/Users/admin/Games/reincarnated-godot/scripts/s2b_xrow_rows37.py`
- `/Users/admin/Games/reincarnated-godot/harness_logs/s2b_rows37_2026-08-24/xrow.json`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/knight-rider/rulings/2026-08-25-a6-decline-ratified-contamination-is-one-arm-not-one-pair.md` §§ 7.4, 8.5, 9
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-08-24-drax-s2b-rows-redispatch.md` A-6 … A-10
