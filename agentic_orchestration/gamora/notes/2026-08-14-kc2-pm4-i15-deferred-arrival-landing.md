# KC2-PM4 · I-15 — **THE DEFERRED-ARRIVAL TICK-ORDER FOLD** — landing note

> **Run:** KC2-PM4 · **Iteration:** I-15 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** **R-PM4-37 part 5** (ledger **L-28**). **Discharges `C-I13-2`.**
> **Math note (FIRST, its own commit):**
> `simulation/math/kc2-pm4-i15-deferred-arrival-2026-08-14.md` — engine `18ab867e`
> **Engine commits:** `18ab867e` (math note ONLY) → `3a00afcc` → `e446d731` → `0103ceb9`
> → `8b6431d8` → `05cc5eb3`
> **Record cell:** `cluster_defon__critlo`, **DESIGNATED BY MEASUREMENT** (R-PM4-36 part 2).
> **Not pushed** — the conductor verifies from his own seat and pushes.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**The referent's 1.6166 s full-health dwell is projectile flight time, and this lap measured it
from two columns nobody tuned.** Wave 160 — the wave T1, T2 and the whole T4b family sit on — is
**100 % projectile-borne**: one actor (`w160_a002`, Archmage Aleksander) firing
`aetherialvanguard_arcanemissilenova` at a measured velocity of 14.0 from 23–26 m, and nothing
else touches the player. Under deferred arrival the player enters that wave at full health and
**nothing reaches him for 22 ticks = 1.795918367346939 s**, against the referent's MEASURED
**1.6166 s** — ratio **1.1109**. The math note pinned the arithmetic **1.7959183673469388** and the
interval **[1.71, 1.88]** before the first tick, and the run landed on the arithmetic *exactly*.
⚑ **And the commission's own premise is FALSIFIED by its own measurement, as pre-registered:
co-arrival is REAL (50 arrival ticks gather 111 casts fired on different ticks) and
SUB-DOMINANT — the deepest single-tick concentration FALLS from 15,012.31 to 14,587.96 (×0.9717),
so T4b(c) does not fire.** On a board whose casts are already cooldown-synchronised, a
*heterogeneous* latency scatters faster than it gathers. **S-1, the pre-named STRUCTURAL candidate,
is correct for the THIRD consecutive application of R-PM4-31 part 5.**

---

## 1 — THE SCORECARD, THREE CELLS

**Record cell `cluster_defon/critLO`** (designated by measurement per R-PM4-36 part 2; critHI
RETIRED per R-PM4-37 part 2 — **W-6 narrowing with reason**, stated in the math note § 7 before the
driver existed).

| | camp/critLO | cluster-defoff/critLO | ⚑ **cluster-defon/critLO (RECORD)** | I-14 record |
|---|---:|---:|---:|---:|
| **T1** terminal | death @154 ✗ | death @160 **MET** | ⚑ **death @160 — MET** | @160 MET |
| death t into wave | — | — | ⚑ **4.6531 s** (⚑ **RETARD +1.1429**) | 3.5102 |
| **T2** `l4l` | 83.0204 ✗ | 179.7551 **MET** | ⚑ **187.7551 — MET** | 186.6122 |
| ratio to 182.7167 | 0.4544 | 0.9838 | ⚑ **1.0276** | 1.0213 |
| **T3** MAE (s) | 6.9220 | 5.6484 | **6.2170** | 6.3313 |
| **T4a** mean `hp_frac` | 0.8832 | 0.9290 | ⚑ **0.9173** (video 0.932) | 0.8989 |
| **T4b(b)** dwell | 0.0 | 0.0 | **0.0** (target 1.6166) | 0.0 |
| ⚑ **T4b(b) ENTRY dwell** | 7.2653 | 1.3061 | ⚑⚑ **1.795918367346939** | — |
| ⚑ ratio to 1.6166 | 4.494 | 0.808 | ⚑⚑ **1.1109** | — |
| **T4b(c)** instant kill | ✗ | ✗ | **✗** | ✗ |
| deepest tick cluster | 5,499.07 | 11,450.59 | ⚑ **14,587.96** (×0.9717) | 15,012.31 |
| deferred applications | 44 | 334 | **329** | — |
| median latency | 6 t | 8 t | **8 t** (min 1, max 84) | — |
| co-arrival ticks | 1 | 58 | **50** | — |

**T1 · T2 · T4a all MET on the record cell. T3 NEAR and slightly IMPROVED (6.3313 → 6.2170).
T4b(b) and T4b(c) remain the run's unmet family, and § 3 says why in mechanism terms.**

---

## 2 — THE COMMISSION'S TWO QUESTIONS, ANSWERED

### 2.1 ⚑ T4b(b) — **the dwell, and it is a CORRESPONDENCE, not a score**

The commission asked for T4b(b) *explicitly on every cell*. Here it is, honestly, in two parts.

**Part one — the instrument does NOT move, and I predicted that (P.6, CONFIRMED).**
`t4b_instrument`'s `b_full_health_dwell_before_death_s` counts back from the death tick while
`hp ≥ 0.999`. It reads **0.0 on all three cells**, because this sim kills the player at the bottom
of a grind, not from full. **It will keep reading 0.0 until one volley can delete the pool** — and
that is a magnitude question, not a timing one.

**Part two — and this is the lap's find.** The referent has its dwell *because it is killed FROM
FULL*: in the video T4b(b) and T4b(c) are the **same event**. What the deferral makes measurable is
the **mechanism**:

| wave | wave opens | first damage lands | ⚑ full-health dwell |
|---:|---:|---:|---:|
| 159 | run-tick 1880 | 1912 | 2.6122 s |
| ⚑ **160** | run-tick **2243** | **2265** | ⚑⚑ **1.795918367346939 s** |

Against the referent's **1.6166 s** that is **ratio 1.1109**, from `t = d/v` with both terms
measured and no free parameter anywhere in the chain. ⚑ **It is reported as a correspondence and
the code says so where the number is computed** (`entry_dwell()`'s docstring and the scorecard's
`⚑ NOT_A_SCORE` field), not only in this note.

### 2.2 ⚑ T4b(c) — **the commissioned hypothesis is FALSIFIED, and it was pre-registered as such**

The commission's reasoning was exact: *"concentration-in-time is exactly what ≥ max HP within ≤ 1
tick needs; staggered casts with differing flight times can CO-ARRIVE."* **Both halves of that
were measured before the code existed, and they point opposite ways.**

- **Co-arrival is REAL and counted.** 50 arrival ticks gather applications cast on ≥ 2 *different*
  ticks, involving 111 cast ticks of 244 arrival ticks. The deepest gathers casts from ticks 181
  and 183 at wave 159 and is worth 9,051.35.
- ⚑ **And the board's deepest single-tick concentration nevertheless FALLS**: 15,012.31 →
  **14,587.96**, ×0.9717, against a pool of 20,005 (0.729). **T4b(c) does not fire.**

**The mechanism, stated as S-1:** the sim's casts are already synchronised by a shared cooldown
lattice while the flight times are *heterogeneous* — 1 to 84 ticks, median 8. A per-cast latency
therefore **scatters what was simultaneous faster than it gathers what was staggered**. The deepest
cluster (w159, run-tick 1979, 35 rows, `hp_frac_before` 1.0000) is a tick that already existed and
that deferral *thinned*.

⚑ **The consequence, and it is the lap's most load-bearing sentence: the T4b family is not
reachable by tick order at all.** It needs ONE body delivering ≥ 20,005 in ONE volley — a
magnitude/multiplicity question the run has already **HALTED** on. **`C-I14-1`'s 193 un-decoded
actors carrying 56.02 % of the player's intake are now the only remaining route, and no iteration
can close it — only a decode lap can (Lap O, in flight).**

---

## 3 — CASTER-DEATH SEMANTICS, PRE-DECLARED AND MEASURED

Both limbs emitted, the record pre-declared in the math note § 2.2 **before the run** — this is not
outcome-selected, it is the referent game's own semantics.

| | RECORD `persist` | `S-VOID-ON-DEATH` | Δ |
|---|---:|---:|---:|
| T1 | death @160 | death @160 | — |
| `l4l` | **187.7551** | **187.7551** | ⚑ **0.0000** |
| mean `hp_frac` | 0.9172747 | 0.9172747 | ⚑ **0.0000000** |
| T4b(c) | ✗ | ✗ | — |
| arrivals past a caster death | **12 persisted** | **12 voided** | 12 |

⚑ **The bracket is REAL (12 arrivals actually change hands) and VERDICT-IDENTICAL to the seventh
decimal.** P.14 predicted exactly this. **§ 8.2's pre-registered new-bracket test therefore returns
0 divergent keys, and the record-cell designation stands without deferral** — asserted by wall
check 21, not merely obeyed.

⚑ **Note the direction, because it is the uncomfortable one:** `persist` is the damage-**RAISING**
end. It was taken on its semantics (a fired projectile is an independent actor in the referent
engine; nothing in the 48-file corpus carries a despawn-on-owner-death rule), not on its direction.
And it does **not** contradict this run's "no swinging from beyond the grave" rule — that rule
governs whether a dead body may *initiate* an action; this one governs whether an action a living
body already initiated *completes*. Two different predicates, named rather than conflated.

---

## 4 — THE PRE-REGISTERED PREDICTIONS, GRADED — **16 / 17**

| # | claim | got | |
|---|---|---|---|
| P.1 | waves 151–158 reproduce I-14 EXACTLY | 8 waves, **max delta 0.0 s**, Σ 153.46938775510205; w159 span 29.63265306122449 = I-14's | ✅ |
| P.2 | T1 MET, death on wave 160 | `player_death @160` | ✅ |
| P.3 | ⚑ deferral RETARDS the death, t ∈ [4.30, 6.60] s | **4.653061224489797** (+1.1429 vs I-14) | ✅ |
| P.4 | ⚑ deferral RETARDS `l4l` ∈ [187.40, 189.70], T2 still MET | **187.75510204081633**, ratio 1.0276 | ✅ |
| P.5 | T4a ∈ [0.899, 0.930], at or ABOVE I-14 | **0.9172747354117985** | ✅ |
| P.6 | ⚑ T4b(b) as INSTRUMENTED stays 0.0 | **0.0** | ✅ |
| P.7 | ⚑⚑ entry dwell ∈ [1.71, 1.88] s (arithmetic 1.7959183673469388) | **1.795918367346939** | ✅ |
| P.8 | T4b(c) does NOT fire; cluster < 16,000 | `False`; 14,587.96 | ✅ |
| P.9 | ⚑⚑ **deferral DISPERSES** — cluster ∈ [12,000, 15,000], below I-14's 15,012.31 | **14,587.96** (×0.9717) | ✅ |
| **P.10** | co-arrival ≥ **60** arrival ticks | ⚑ **50** | ❌ |
| P.11 | threat RNG draws over w151–158 identical to fold-OFF | **3,230 = 3,230** | ✅ |
| P.12 | fold-OFF byte-identity ×3, key ABSENT | 3/3 EXACT, 0 of 30 waves carry the key | ✅ |
| P.13 | 0 dropped at a wave boundary over w151–159 | **0** on all nine (2 at w160, whose "end" is the death) | ✅ |
| P.14 | `S-VOID-ON-DEATH` verdict-IDENTICAL | 0 divergent keys | ✅ |
| P.15 | camp still dies @154, `l4l` ∈ [83.0, 86.5] | @154, **83.0204081632653** | ✅ |
| P.16 | reach counted, median latency ∈ [4, 9] ticks | 329 deferred / 577 identity, median **8** (1–84) | ✅ |
| P.17 | `S-QUANT-ROUND` verdict-identical on T1 | @160, `l4l` 187.75510204081633 — identical | ✅ |

### 4.1 ⚑ P.10 — THE FALSIFICATION, AND ITS ROOT CAUSE IS MINE (`D-I15-3`)

I predicted ≥ 60 co-arrival ticks from a static estimator over the I-14 baton and got **50**.
**The prediction and the instrument were not measuring the same quantity, and that is my defect,
not the model's.** My estimator counted an arrival tick as co-arrival if ≥ 2 *any* player-incoming
rows from different cast ticks landed there — **including identity-path rows** — and keyed on
run-wide ticks across the whole ladder. The shipped instrument counts **only deferred applications**
and is **per wave** (the fold is constructed per wave). It is strictly narrower on two axes and it
is the better definition. **The number was graded against a definition it was not made under, and
the honest verdict is FALSE.** The claim it carried — *co-arrival is real* — holds on the stricter
instrument too.

### 4.2 ⚑ THE STRUCTURAL PRE-NAMING, THIRD APPLICATION — **S-1 CORRECT AGAIN**

| candidate | verdict |
|---|---|
| ⚑ **S-1 (STRUCTURAL)** — *deferral is a DISPERSAL operator; the T4b family is unreachable by tick order and only `C-I14-1`'s decode gap remains* | ⚑ **CORRECT.** Cluster ×0.9717, T4b(c) unfired, co-arrival real and sub-dominant. |
| **S-2 (STRUCTURAL)** — *the effect on the death wave is a one-time TRANSIENT of exactly one flight time* | ⚑ **CORRECT.** The retard is **+1.1429 s** against a w160 flight time of 1.7959 s — the same order, and less than one flight time because the counterplay re-actuates into the reprieve. |
| **S-3 (STRUCTURAL)** — *the fold is one-sided; no span can move* | ⚑ **CORRECT.** All eight spans 151–158 delta **0.0**, w159 identical. |
| **T-1 (throughput)** — *the tick-walk prices the death EARLY* | ⚑ **CORRECT, again.** It said 4.8163 s; the truth is 4.6531 s. ⚑ **Honest note: this time it priced LATE by 0.16 s**, because it could not see the counterplay re-actuating into the reprieve either. The bracket was set above it and the answer came in below it — the flaw was real, its sign was not the one I named. |

**R-PM4-31 part 5 is now 3-for-3 on structural pre-naming.**

---

## 5 — THE FOLD, AS BUILT

| # | limb | direction | measured |
|---|---|---|---|
| **A1** | arrival at `cast + ceil((d/v)/period)` | NEUTRAL in total, LATER in time | 329 deferred / 577 identity on the record cell |
| **A2** | caster death = **PERSIST** (record) | RAISES vs VOID | 12 arrivals; verdict-identical |
| **A3** | in-flight at wave end → DROPPED + counted | ⚑ REDUCES | **0 rows** on w151–159 |
| **A4** | R-PM2-5 re-clamp of the PCL component at ARRIVAL | ⚑ REDUCES | 0.0 reclaimed (no PCL row deferred this run) |

**GL-12 at the gate:** 69 corpus rows carry `velocity ≤ 0` (61 zero, 8 negative −5.0). **Not
deferred, not invented, COUNTED** — 44 identity-path applications on the record cell.

**The fold's one clean invariant, and it held:** `resolve_attack` is still called at the cast tick
with every RNG draw in its original position; only the *application* is queued. **Threat draws over
waves 151–158: 3,230 record = 3,230 fold-OFF.** Zero lines of `threat.py` were changed — the queue
is fed from `resolve_attack`'s own detail dict, which is what makes *"every magnitude is I-14's,
byte for byte"* structural rather than asserted.

---

## 6 — ⚑ FIVE DEFECTS, ALL FRAMED

| id | what | disposition |
|---|---|---|
| ⚑ **`D-I15-1`** | **SELF-CAUGHT, PRE-RUN.** I-13 § 3.4 quoted **49 ticks/s** where `channel.ticks_per_s` gives `AS%/16 = 12.25` — a divide-by-4 slip. The ring residual it named is 4 ticks, not 13; the BOARD-WIDE residual is far larger anyway (median 8 ticks, max 84). ⚑ **Repaired structurally: `simulate_wave` now ASSIGNS the sim's own rate onto the fold, so a spec cannot hand it a clock the sim does not run at.** | corrected in the math note before either number was used |
| ⚑ **`D-I15-2`** | **Discipline #12 SEMANTIC SHIFT, FRAMED.** *"damage is applied when it is RESOLVED"* → *"damage is applied when it ARRIVES"*. Every projectile-borne monster application has landed at its cast tick since PM-2. | framed; **decisions-log entry PROPOSED** (§ 9) |
| ⚑ **`D-I15-3`** | **SELF-CAUGHT AT GRADING.** P.10's prediction basis (all rows, run-wide keys) and the shipped instrument (deferred rows, per wave) are different quantities. Graded **FALSE** rather than re-scoped. | § 4.1 |
| ⚑ **`D-I15-4`** | the arrival row's provenance printed a **wave-local** cast tick beside a **run-wide** `run_tick`. Internally consistent (schedule and due both key the wave-local clock) and no number depended on it — but it is the "wrong frame" class this run has banked before. ⚑ **Repaired in the dataclass (`cast_run_tick`), not in the f-string.** | repaired; lap re-run from scratch pre-banking |
| ⚑⚑ **`D-I15-5`** | **CAUGHT BY star-lord's VALIDATOR, NOT BY ME.** `AC-11.7b` keys damage rows on `(run_tick, source, target, skill, tag)` to assert *"damage is never AGGREGATED"* — and **co-arrival collided it for the first time in this run's history**: two projectiles from ONE caster with ONE skill on DIFFERENT ticks arriving on the SAME tick. ⚑ **The mechanism the lap was commissioned to measure surfaced as a schema violation.** The repair is **provenance, not aggregation**: the arrival row's `damage_source_tag` now names its volley (`chain_initial@cast2292`). **Zero validator predicates touched — the gate is star-lord's and it was right.** | repaired; **MIGRATION § 1b** carries consumer guidance |

---

## 7 — THE ASSERT WALL: **20 / 21**, AND THE ONE RED IS MINE AND FAILED CLOSED

Spec written in the math note § 8 (**W-5**), 22 checks / 21 scored, form rules W-1/2/3/6.
⚑ **R-PM4-37 part 6 honoured on every check**: a single `have()` helper **raises** on a missing
input key rather than returning falsy, and every check's `detail` carries `keys_asserted`. **A
check that cannot find its own inputs is a RED, not a silent `None`** — the repair applied to all
21, not just to the one D-I14-4 found.

**⚑ RED — check 8 (conservation).** Predicate:
`offered == applied + dropped + voided + pool_truncated + pcl_reclaimed`, to 1e-6.
Measured: offered 661,362.73 · applied 386,746.49 · dropped 15,814.02 · voided 0.0 ·
pool-truncated 4,696.35 · pcl-reclaimed 0.0 → **residual 254,105.87**.

**Diagnosed, not merely reported: the identity omitted the COUNTERPLAY sink** — and the math note's
own § 2.1 pseudocode shows it (`dmg = counterplay.absorb(dmg)` sits between offer and apply).
**The fold conserves.** The counterplay layer keeps its own books and they close exactly:
`raw 5,089,467.36 = applied 2,668,128.04 + absorbed 945,393.79 + warcry_reduced 1,475,945.54`,
**residual −0.0**. Nothing is lost; my predicate was under-specified.

⚑ **It was NOT edited to pass.** jack-ryan's no-mid-lap-repair precedent (AFFIRMED at R-PM4-33
part 3) applies to the wall. The repair — adding the absorb sink to the identity — lands in I-16.
**W-6 note also carried in the check names:** check 4 narrowed from 6 cells to 3 because critHI is
retired **by measurement**; check 11's scope (waves 151–158) is in its NAME because the death tick
legitimately diverges.

---

## 8 — ARTIFACTS AND DIGESTS (FULL 64 hex, GL-6)

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i15-findings-20260814_103837.json`
`6295ff743ad8698baa243b8d7bd88a1a1681202f4525ad6e691af918c6542347`

**Knot artifacts:**

| cell | sha256 |
|---|---|
| ⚑ `cluster-defon-critlo` **(RECORD)** | `0a84b4a6540d7e756742358fe7df72a4a0cd4c540398917ce5323370f1813cc0` |
| `cluster-defoff-critlo` | `b4eca2da9a57c3bb43d37289df05e79f4c26ac44acec297e232473dcf5b8bd26` |
| `camp-defoff-critlo` | `54cf12cbf5be5343914786380e656e90b541925968d98b959f0814774e579485` |

**⚑ BATONS — three, 67/67 GREEN each** (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33):

| column | sha256 |
|---|---|
| ⚑ `pm4-i15-cluster-defon-critlo` **(RECORD)** | `d24599724895a4de22c21aad2cf176ec2fe0257cca6686d58ecbd449fd296e00` |
| `pm4-i15-cluster-defoff-critlo` | `82aec861e154b713da5fd043295dbb0cff6ed12065838f2393e04dc2692c598d` |
| `pm4-i15-camp-defoff-critlo` | `de3e2a99340771e27d36bded50553dee6e7413d405a163046bf5ea3ebdc8ed78` |

**The adapter's independent replay reproduces the driver to the digit on all three** —
187.7551 / 179.7551 / 83.0204, `end_reason player_death` on every one, `final_wave` 160/160/154.

**Determinism ×2 — ZERO differences on all three cells:**
`e64e0cb881b6fa194bbe834be708774706bcf8c38bb754e1245ed3bd02accf9f` (record) ·
`e28081fd76358c19897a3e7293280b7f0693d698de9514648fa66ca0eb7191cf` ·
`653e294b492b6d1dcc50b0682346b5915511ac77ef4ae1d44c31b2d3331dc51c`

**Fold-OFF byte-identity ×3 — EXACT vs I-14's critLO surfaces**, `monster_deferred_arrival`
**ABSENT-not-None** on 30/30 waves (the ninth use in this run):
`c035f057…1881` · `752b772a…d368` · `eb3831aa…8276`

**Substrate pin (1, measured):** `pm2_tg2_attack_damage.csv`
`e250089e7db3ef90f8a02dc2459c27b5bcc159a559769630aefb0167577bbf3c`
**Frozen substrate `E-s09-cp150`: 20 artifacts verified, UNTOUCHED.**

**Law 3:** `law_3.moved == {}` **TOP-LEVEL** (D-6b), 11 witnesses read from the witness set.
**Zero new free constants.**

**MIGRATION.md:** written **from the emitted bytes** — `set(i15.waves[0]) − set(i14.waves[0])` is
`set()` in **both** directions, top-level key diff `set()`, `events.columns` identical,
`_schema_version` 1 → 1. **Zero telemetry schema changes.** The one field whose *value shape*
changed (`damage_source_tag` on arrival rows) is declared with consumer guidance in § 1b.

---

## 9 — TO THE CONDUCTOR

| id | what | disposition |
|---|---|---|
| ⚑ **`C-I13-2`** | deferred projectile arrival | ⚑ **DISCHARGED.** Both terms measured, folded, verdict-affecting, and the semantics bracket closed verdict-identically. |
| ⚑ **`C-I14-1`** | 193 un-decoded actors, **56.02 %** of intake | ⚑ **PROMOTED by S-1 to the ONLY remaining route to T4b.** Lap O is now the run's critical path, not a parallel nicety. |
| ⚑ **`C-I15-1`** | DoT seeding still starts at CAST | ROUTED — measured **0.22 %** of intake board-wide, **0.00 %** at w160 |
| ⚑ **`C-I15-2`** | the co-landing count is evaluated at the CAST separation | ROUTED — folding it needs deferred RESOLUTION, which would move the threat RNG stream and destroy the fold's one clean invariant; emitted as a read-only counterfactual |
| ⚑ **`C-I15-3`** | cross-wave flight | ROUTED — **0 rows** on every completed wave; carrying them needs a new ladder channel |
| ⚑ **`C-I15-4`** | **check 8's conservation identity omits the counterplay sink** | ROUTED — repair in I-16; NOT edited mid-lap |
| ⚑ **DECISIONS-LOG PROPOSED** | **`D-I15-2`** — the arrival-time semantics. This changes how every projectile-borne monster application in the model is interpreted, and per Discipline #12 it belongs in the log rather than in a commit message. Proposed to jack-ryan via knight-rider. | awaiting |
| carried | `D-N-1` · explosion-centre UNDECIDED · `D-I12-5` (w154 TTL, **unmoved a sixth time** — floor 0.1786 @w154) · Q57 (Matt, non-blocking) | carried |

⚑ **On the convergence gate (R-PM4-37 part 7):** the record cell now meets **T1 · T2 · T4a**, is
NEAR on **T3** (6.2170 s MAE, and its surface is still targeting/locomotion), and **T4b(b)/(c)
remain unmet with a named mechanism**. S-1 says no further *iteration* can move T4b. **If the
conductor is weighing a convergence HALT, the honest reading is that the run's remaining gap is a
DECODE gap and the gate's precondition (b) — every carried debt dispositioned — now turns on Lap O.**

---

**Author:** gamora (simulation seam) · 2026-08-14 · **math note first, code second, and the git
order is the proof.**
