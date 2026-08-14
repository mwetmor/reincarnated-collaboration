# KC2-PM4 · I-10 — landing note: **the arrivals were already discrete. I moved their PHASE, the bursts arrived — and the fight did not move by one tick.**

> **Run:** KC2-PM4 · **Iteration:** I-10, THE DAMAGE-ARRIVAL VARIANCE FOLD · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** ruling **R-PM4-23** (charter ledger **L-19**), pre-authorized at **R-PM4-22** (L-18) on my own gating request.
> **Math note (Discipline #1, written and committed BEFORE the code — commit `533b97c8`, its own commit, so the git order is the proof):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i10-arrival-variance-2026-08-14.md`
> **Judged against:** I-9's pinned batons and the **L-19 RE-DERIVED BANDS**.
> **Status:** COMPLETE. **No HALT.**

> ### ⚑ NOTE-9 — THE BASIS FOR EVERY NUMBER IN THIS NOTE
> | class | source | sha256 (FULL, GL-6) |
> |---|---|---|
> | every **I-10** quantity | `simulation/output/kc2-pm4-i10-findings-20260814_035800.json` | **`44bdeeac5d81fd3618bdbd6fe1b9186c42612bed6b197b810ad8bba1df4a6b6d`** |
> | every **I-9** quantity | `simulation/output/kc2-pm4-i9-findings-20260814_022801.json` | `a45b81548478387fe2bae5954b1c0f718416e8eef1add0a83f3c1996a53adf28` |
> | the **measured death** | `data/kc2/pm4k_death_anchor.csv` (legolas Lap K, imported unmodified) | `999347db3e1b5caa69809abf8d56d1c7212d67321ae8c80e87abd2e71d584a6e` |
> | the **burst target** | `data/kc2/pm4k_deep_bursts.csv` | `044742102ffa845ea05c8c2bade32e8d8ca29d36983f0f6a99b897e3f591a93f` |
> | the **wave spans** | `data/kc2/pm4k_segments.csv` | `a1b03c319db32d81cbcbae6efe5b584f01a8069b4af3514b8a886d1ac0b80785` |
>
> All three Lap-K digests are **verified from bytes at run time by the driver** and match the
> conductor's own L-19 values; the I-9 findings digest likewise. A wrong digest HALTs the lap.
> **There is no unsourced number below.**

---

## 0 — The one-paragraph answer

**The fold worked mechanically and changed nothing structurally.** Moving φ — the origin of a
monster's swing clock — from a hash of its NAME to the tick it ARRIVED produced exactly the
correlation the math note predicted: coincident arrivals rose from **21 to 28** rows on one tick
(and to **30** on the corner), the deepest single tick rose **9,270 → 11,290** applied, the sim
crossed the video's **−0.30-of-the-bar** depth class **for the first time in the run**, the floor
fell **0.4238 → 0.3512**, and intake rose **+19.7 %**. ⚑ **And the terminal wave did not move, no
wave's duration moved by one tick, the like-for-like is 223.265306122449 s — IDENTICAL to I-9 to
the tenth of a millisecond — and the instant-kill clause did not fire on any of the eight cells.**
T1, T2, T3 and T4b all MISSED. **That is four consecutive iterations in which a perturbation of a
different subsystem has been completely absorbed by this model** (§ 11.1), and it is the finding.
The pre-registered candidate error in math note § 9.1 **fires**: I priced the CORRELATION and not
the DWELL (§ 9.1).

---

## 1 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 16 predictions, 20-check wall, the false premise declared pre-run) | `simulation/math/kc2-pm4-i10-arrival-variance-2026-08-14.md` | **`533b97c8`** |
| 2 | `kc2/threat.py` — `PhaseModel`, `ThreatEngine.phase_model`, `note_position`, `max_reach_m`, `is_opportunity` (φ only), `phase_of` docstring CORRECTED | modified (ADDITIVE; the default IS I-9) | `a9ac9483` |
| 3 | `kc2/arrival.py` — **NEW**: Lap-K pinned substrate + the L-19 bands, **built from the CSVs, never from a literal** | new module | `a9ac9483` |
| 4 | `kc2/run.py` — `phase_model` keyword; `dist` hoisted above the opportunity test; `run.engage_log` | modified | `a9ac9483` |
| 5 | `data/kc2/pm4k_*.csv` ×3 — Lap K's emissions, imported UNMODIFIED | new substrate | `a9ac9483` |
| 6 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `a9ac9483` |
| 7 | `export/kc2_run_adapter.py` — `phase_model` spec field + 3 I-10 specs | modified | `a9ac9483` |
| 8 | **driver + 20-check wall + determinism + 5 sensitivity cells** | `simulation/scripts/gamora_kc2_pm4_i10_arrival_variance_2026_08_14.py` | `a9ac9483` |
| 9 | **3 knot supplies + findings** | `simulation/output/` | `062a8a73` |
| 10 | **⚑ 3 BATONS** | `src/reincarnated/output/` | (this note's commit) |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6)

| what | sha256 |
|---|---|
| **findings** | `44bdeeac5d81fd3618bdbd6fe1b9186c42612bed6b197b810ad8bba1df4a6b6d` |
| knots CAMP/DEF-OFF | `a387269beee97f40bbd639f015378ffa951a2901bf2135993522ae7df99115f4` |
| knots CLUSTER/DEF-OFF | `fe1260a8b933cbe8baa7f6907fcdddc28999464ba4fcf04051a1cd5eb6cf5a81` |
| **knots CLUSTER/DEF-ON** ← reference | `6b562287f331ea077b3c0488e8b23cb92388ccad0ec1ce0780ea40b432f2b219` |
| **baton** CAMP/DEF-OFF | `0489f5924eff1b92c63503ab976bb2e4d88ed53f5ef9bd61d1122f6b2b21ed97` |
| **baton** CLUSTER/DEF-OFF | `759d4881ce02c2d57afa38fc2854c9cc83a75fc32994dec7ff905b8bf9682a63` |
| **baton** CLUSTER/DEF-ON ← reference | `5a9a183d590444b306da4e67e6415a2f1ccf82ac05134f71620bfd5d6c325f46` |
| determinism surface CAMP/DEF-OFF | `7d05fc815794bc1cc7bd5826ab4e7623b94cfefc3b78f747f9c5d50bd8e03351` |
| determinism surface CLUSTER/DEF-OFF | `faaf70e5ce44291863ee741cad844928d765453f517557ee02c80a438f2a9516` |
| determinism surface CLUSTER/DEF-ON | `8255e8d8bd92b542d3022a4df0473b0258c7331e13f0f24c8c911c418fa0e91a` |

All three batons emitted **FULL, 67/67 green** (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33) on a
clean tree. **The I-9 batons these SUPERSEDE:**
`3b2c5a3e8b59967c0dbad0a81d7104ef8b287e31bd120bd06d08cd6f9b790762` /
`d0953482b22ad9c74a3360327ec6d381ba1d031a757a97d340111e8a7dd9c7c0` /
`aaea3e2ef2850c016d32dcc6efb588581509ca44b6c1a1a6e3ede973d0f5d1e4`.

### 1.1 — ⚑ THE FOLD-OFF ARM IS BYTE-EXACT, AT THREE DEPTHS

| layer | arm | declared (math note § 7) | measured |
|---|---|---|---|
| **1a** | I-9 config at I-10 HEAD with `PhaseModel.HASH` (**the DEFAULT**) | byte-EXACT vs I-9 ×3 | **EXACT ×3** — `8210322b…7689` / `fd112bb1…3274f` / `83701c4f…bb06` |
| **1b** | pre-I-6 arm (jacobi4, offense off, band-C off, I-8 kit limbs) | byte-EXACT vs I-5, **five folds back** | **EXACT ×3** — `5f616040…7fa7` / `0ad5b297…2605` / `95a34b2e…c7a4` |
| **1c** | ABSENT-not-None: the legacy arm never passes `phase_model` at all | registry EMPTY on every wave | **EMPTY ×3** |
| **1d** | the three I-10 cells | divergent BY CONSTRUCTION (§ 6, RNG) | divergent, as declared |

---

## 2 — ⚑ THE FIRST FINDING IS THAT THE COMMISSION'S PREMISE WAS FALSE, AND THE MATH NOTE SAID SO BEFORE THE CODE

R-PM4-23 asked me to *"replace smoothed per-tick damage delivery with … per-attack discrete
arrivals at the decoded attack periods … per-hit magnitudes from the tables … the existing to-hit
model (23.50 % miss)."*

**All four were already in the model and had been since I-7.** Measured, not argued:

| commissioned property | measured at I-9 |
|---|---|
| per-attack **discrete** arrivals | **1,150** `damage_dealt` rows on 6,321 ticks; **71 %** of ticks carry no incoming at all |
| decoded periods | 169 profiles, swing periods **0.4222–1.9765 s** |
| **+11 % AS at w160** | `attack_speed_mult = 1.11` |
| **23.50 % miss** | `472 / (1532+472) = 0.23553` |

**The sim never delivered smoothed per-tick throughput.** I banked this in the math note § 1
*before* writing a line of code precisely so it could not be read afterwards as an excuse. The
question the lap actually had to answer was narrower: the arrivals are discrete — **why is their
SUM never large?**

---

## 3 — ⚑ THE ANSWER, AND IT WAS A FUNCTION OF THE MONSTER'S NAME

`ThreatEngine.phase_of(actor_id, n) = int(sha256(actor_id)[:8], 16) % n`.

A body's swing phase was a **hash of its name**: uniform, independent, maximally de-correlating.
Math note § 2 priced it — at the roster's median 10-tick period, with 541 ticks carrying ≥ 5
bodies in the engage ring, `E[5-body coincidences across the whole 20-wave fight] = 541 × (1/10)⁴
= 0.054`. **The sim had never produced a full-to-zero tick because five independent uniform phases
coincide 0.054 times in a fight this long — not because its magnitudes were small.**

The fold replaces φ and **nothing else**. The opportunity law `(t − φ) mod n == 0` is untouched
(assert-wall check 7: **36,000 (id, period) pairs, 0 mismatches** — the HASH branch is the legacy
law bit-for-bit; checks 8 and 9: **0 early swings, 0 law violations on 1,405 emitted rows**).

> ### ⚑ THE LAW-3 POSITION, AND IT IS A SUBTRACTION
> **This fold DELETES an invented quantity; it adds none.** The hash was a pseudo-random
> de-correlator with nothing behind it in any decoded table, whose own docstring admitted its
> purpose was a modelling assertion (*"a board that swings in lockstep is an artifact of the
> harness"*). φ = the engagement tick is a **state variable produced by the measured locomotion**.
> There is no constant to fit and none was fitted. **I corrected that docstring rather than
> deleting it**, because a wrong sentence removed is a lesson lost.

### 3.1 — What the registry measured

| quantity (reference cell) | measured |
|---|---:|
| bodies registered | **911** |
| distinct origin ticks | **207** |
| **mean bodies sharing an origin tick** | **4.401** |
| max bodies sharing an origin tick | **36** |
| cohorts ≥ 5 bodies | **68** |

⚑ **The correlation is real and it is EMERGENT.** Nothing chose 4.401; it is what the arrival
process produces when the player walks into a pack.

### 3.2 — ⚑ AND THE MECHANISM SHOWS UP IN THE TELEMETRY AS A COLLAPSE OF WASTE

| reference cell | I-9 | **I-10** | Δ |
|---|---:|---:|---:|
| `n_attack_opportunities` | 6,876 | **3,374** | **−50.9 %** |
| `n_out_of_reach` | 4,371 | **379** | ⚑ **−91.3 %** |
| `n_hits` | 1,532 | **1,860** | **+21.4 %** |
| `n_misses` | 472 | 570 | — |
| miss rate | 0.23553 | **0.23457** | the to-hit law is intact |
| `damage_total` applied | 1,866,957 | **2,235,594** | **+19.7 %** |
| `n_damage_taken_rows` | 1,150 | **1,447** | +25.8 % |

**Under the hash, two of every three swing opportunities were spent on a body that could not
reach the player.** Under engagement anchoring a body's clock does not start until it can act, so
the opportunity count halves while landed hits rise by a fifth. **That is the fold's content,
visible as a single pair of numbers.**

---

## 4 — ⚑ THE ARRIVAL STRUCTURE MOVED, AND IT MOVED A LOT

Reference cell, both instruments reported because they disagree and the disagreement matters.

| statistic | I-9 | **I-10** | video (Lap K) |
|---|---:|---:|---:|
| ticks carrying incoming | 1,839 (29.1 %) | **2,095 (33.1 %)** | — |
| **max simultaneous incoming rows on one tick** | 21 | **28** | — |
| max simultaneous **distinct bodies** on one tick | 20 | **27** | — |
| **deepest single tick, applied** | 9,270.4 (0.4634 bar) | **11,290.4 (0.5644 bar)** | **20,005 (1.0000)** |
| bodies in that tick | 2 | **13** | ring 1 / max 4, 13 nameplates |
| ticks ≥ 0.30 bar **applied** | 5 | **10** | — |
| ticks ≥ 0.50 bar applied | 0 | **1** | — |
| **worst END-OF-TICK HP fall** ⚑ like-for-like | **−0.18559** | ⚑ **−0.31289** | **−1.0000** |
| **EOT falls ≤ −0.30** ⚑ like-for-like | **0** | ⚑ **1** | **4** (of the 35 deepest windows) |

> ### ⚑ THE SIM ENTERS THE VIDEO'S DEPTH CLASS FOR THE FIRST TIME IN TEN ITERATIONS.
> I-9's § 9.1 measured the sim's worst end-of-tick fall at **−0.18559 of the bar** and its count of
> falls at or beyond −0.30 at **zero**. I-10's reference cell falls **−0.31289** in a single tick
> and does it once. The video, on Lap K's own instrument, does it four times. **The residual on
> this axis is now a factor of ~3 on depth and ~4 on count, not a categorical absence.**

### 4.1 — ⚑ AN INSTRUMENT DISAGREEMENT I HAVE TO NAME RATHER THAN PICK A SIDE OF

I-9 § 9.1 reported *"the video's top 35 bursts (≥ 0.30 of the bar in 0.0816 s)"* — i.e. **all 35**
of its windows at ≤ −0.30. **Lap K's own 35-deepest emission has only 4 at ≤ −0.30.** The two
numbers come from two instruments: I-9's was a rolling MAX over ±0.10 s on the Lap H-2 bar-pixel
trace; Lap K's is 60 fps orb-OCR, and **L-19 banked the H-2 instrument as wrong in KIND near
death**. I am not adjudicating this — **the Lap-K figure is the one this lap scores against,
because it is the newer instrument on the same referent, and both counts ride the findings
artifact so the conductor can overrule me with one line.**

---

## 5 — THE THREE CELLS OF RECORD, AGAINST I-9

| | camp/DEF-OFF | cluster/DEF-OFF | **cluster/DEF-ON** ← reference |
|---|---|---|---|
| terminal | `arena_tier_exhausted`@171 | @171 | **@171** |
| t_s | 1940.489795918368 | 512.8163265306123 | **516.0** |
| ⚑ **all three IDENTICAL to I-9** | ✓ | ✓ | ✓ |
| mean HP EOT (I-9) | 0.993694 (0.993694) | 0.973585 (0.973585→) | **0.984048** (0.988315) |
| min HP EOT (I-9) | 0.161918 | 0.239956 | **0.351201** (0.423841) |
| min HP intra (I-9) | 0.1592 | 0.1731 | **0.3507** (0.4233) |
| excursions < 0.70 EOT / intra (I-9) | 10 / 21 | 15 / 22 | **8 / 20** (8 / 14) |
| max simultaneous rows | 39 | 35 | **28** |
| deepest tick applied | 9,498 (0.475) | 10,258 (0.513) | **11,290 (0.564)** |
| ticks ≥ 0.30 bar applied | 11 | 6 | **10** |
| ⚑ instant-kill clause | **NO** | **NO** | **NO** |

⚑ **Note the shape:** mean HP for camp/DEF-OFF is *unchanged from I-9 to six figures* while its
floor is the deepest of the three (0.1619). The fold redistributes intake in TIME without moving
its total on that cell — which is precisely what an arrival-structure fold is supposed to do.

---

## 6 — ⚑ THE BRACKET, AND **NEITHER END BOUNDS THE LIMB OF RECORD**

Declared in the math note § 4 as LO = HASH, RECORD = ENGAGE, HI = SPAWN, with S-WINDUP beside it.
**Measured, ordered by lethality:**

| limb | mean HP | min HP EOT / intra | excursions EOT / intra | deepest tick | terminal | l4l 151–160 |
|---|---:|---:|---:|---:|---|---:|
| **S-WINDUP** (engage + n) | **0.990963** | 0.4486 / 0.4334 | 3 / 9 | 6,904 | @171 | 223.265306122449 |
| **S-PHASE-LO** (HASH) ← *declared LO* | 0.988315 | 0.4238 / 0.4233 | 8 / 14 | 9,270 | @171 | 223.265306122449 |
| **S-PHASE-HI** (SPAWN) ← *declared HI* | 0.987015 | 0.3662 / 0.3657 | 6 / 27 | 10,877 | @171 | 223.265306122449 |
| **RECORD** (ENGAGE) | **0.984048** | **0.3512 / 0.3507** | 8 / 20 | **11,290** | @171 | 223.265306122449 |
| S-PHASE-HI-CLUSTER-OFF (SPAWN, DEF-OFF) | 0.976402 | 0.3407 / **0.2623** | 13 / 42 | **14,334** | @171 | 225.2245 |
| S-PCL (declared exclusion, priced) | 0.981461 | 0.3346 / 0.3341 | 10 / 47 | 12,103 | @171 | 223.265306122449 |

> ### ⚑ THE BRACKET IS MIS-DECLARED, AND I DECLARED IT BEFORE THE RUN, SO IT IS A FINDING AND NOT A CORRECTION.
> **`SPAWN` is not an upper bound and `HASH` is not a lower one.** The record limb (ENGAGE) is
> MORE lethal than both declared ends on every depth statistic, and S-WINDUP sits OUTSIDE the
> bracket on the shallow side. **P.14 is falsified, and the reason is mechanical:** a spawn-anchored
> body burns swing opportunities while it is still walking in (§ 3.2's `n_out_of_reach` is the same
> waste the hash suffered), whereas an engagement-anchored one spends every opportunity in reach.
> **Arrival phase is not a one-dimensional dial, and R-PM4-2's LO/HI shape does not fit it.** That
> is routed to the conductor as § 12.1.
>
> ⚑ **And the thing the bracket was FOR — spanning the outcome bands — it does not do, for the
> second lap running.** Every limb terminates `arena_tier_exhausted`@171, and every limb but the
> DEF-OFF corner has the **identical** like-for-like to the tenth of a millisecond.

**S-PHASE-HI-CLUSTER-OFF is the one number worth staring at:** intra-tick floor **0.2623**, which
is **below the video's measured 0.291877**, with a deepest tick of **14,334 (0.717 of the bar)**.
**A cell in this lap goes deeper than the referent's collapse floor — and still does not die.**

---

## 7 — TARGET STATE vs THE L-19 RE-DERIVED BANDS (reference cell)

| band | L-19 target | measured | verdict |
|---|---|---|---|
| **T1** | death on wave **160**, acceptance {159–161} | **no death; `arena_tier_exhausted`@171** — and **no death at ANY of the 8 cells** | **MISSED** |
| **T2** | ToD like-for-like **182.7167 s**, band **[155.31, 210.12]** | **223.265306122449 s** (+22.2 %) — ⚑ **IDENTICAL to I-9 to the tenth of a millisecond** | **MISSED**, unchanged |
| **T3** | the ten measured spans | **10/10 scored**, median ratio **1.1152**, MAE **7.0756 s** | **NEAR/MISSED** |
| **T4a** | alive while clearing, mean → 0.932 | mean HP **0.984048** (I-9 0.988315) | **MET**, moved toward |
| **T4b (a)** | SURVIVED excursion, floor ≈0.29, ~7.4 s, full recovery | deepest survived: floor **0.3512**, **3.51 s**, wave 166, recovered — **0 matches of the measured shape** | **MISSED** |
| **T4b (b)** | full-health dwell ~1.6 s | no death → **not evaluable** | **UNEVALUABLE** |
| **T4b (c)** | ⚑ instant kill hp≥0.95 → 0 in ≤1 tick on w160 | ⚑ **DID NOT FIRE. 0 of 8 cells.** | **MISSED** |

### 7.1 — ⚑ T3's SHAPE IS THE INTERESTING MISS, AND IT IS THE OPPOSITE OF THE MEASUREMENT

| | w159 | w160 |
|---|---:|---:|
| **measured slowdown** (× the 16.267 s mid-median) | **1.617** | **1.595** |
| **sim slowdown** | 1.307 | ⚑ **0.787** |

The referent's final two waves are its **slowest** — 26.30 s and 25.95 s against a 16.27 s
mid-median. The sim's wave 160 is its **fastest recent wave**, 16.33 s = 0.63× the measured span.
**The player is clearing wave 160 in less time than the man who died on it took to die.** No
arrival-structure fold can reach that: wave duration is set by the PLAYER's damage output, and
this fold does not touch it (§ 11.1).

Per-wave, sim vs measured (s): 151 18.37/16.27 · 152 23.10/16.25 · 153 16.24/14.75 · **154 40.73/14.12
(2.886×)** · 155 13.31/16.32 · 156 24.08/20.20 · 157 33.06/18.85 · 158 10.94/13.10 · 159 27.10/26.30
· **160 16.33/25.95 (0.629×)**.

---

## 8 — MATCH GATES (INTERMEDIATE observables, judged SEPARATELY from T1–T4)

| gate | I-9 | **I-10** | video target | verdict |
|---|---:|---:|---:|---|
| **MG-1** ring median | 0 | **0** | 1 | MISSED |
| **MG-2** ring p90 | 4 | **4** | 3 | MISSED |
| **MG-3** ring **max** | 17 | **17** | **10** | MISSED |
| **MG-4** moving fraction | 0.8411363275670528 | **0.8411363275670528** | 0.883 | MISSED |
| **MG-6** longest stationary | MET | **MET** | ≤ 1.40 s | **MET** |
| **MG-7** dash rate | MET | **MET** | 5.3235 s | **MET** |

⚑ **The entire gate block is byte-identical to I-9** (`match_gates == i9['match_gates']` is
`True` in the findings artifact). The gates measure geometry and movement; a phase fold touches
neither. **Reported in full because "identical" is a measurement.**

**Burst-composition gate:** target 35 windows, deepest −1.0000, **4 at ≤ −0.30**, 13 nameplates and
ring-max 4 at the deepest. Sim reference: **1** at ≤ −0.30 on the like-for-like EOT basis (from
**0**), **13 bodies** in its own deepest tick. ⚑ **The body count at the deepest instant now
MATCHES the referent's nameplate count exactly (13); the magnitude does not (0.564 vs 1.000).**

---

## 9 — PRE-REGISTERED PREDICTIONS vs OUTCOME

Falsified predictions keep their original wording (the run's standing practice).

**Four confirmed · three split · nine falsified.** ⚑ **This is the worst prediction record of the
run, and it is reported as such.**

| # | prediction | outcome |
|---|---|---|
| **P.1** | layers 1a/1b/1c byte-EXACT; 1d divergent; `S-PHASE-LO` reproduces I-9's baton exactly | **SPLIT.** 1a **EXACT ×3** ✓ · 1b **EXACT ×3** ✓ · 1c registry **EMPTY ×3** ✓ · 1d divergent ✓ · **the baton limb required MASKING** (§ 10.1, D-I10-1) ✗ |
| **P.2** | max simultaneous rows **5 → [8, 25]** | **⚑ FALSIFIED, AND THE BASELINE WAS MINE AND WRONG.** "5" was a wave-160-only `damage_dealt` count; the instrument's actual I-9 baseline is **21**. Measured **28** — outside my band, on a band built from the wrong number |
| **P.3** | deepest tick **≥ 15,000**; on a wave in {158…170} | **⚑ FALSIFIED on the magnitude — 11,290 (14,334 on the corner, still short).** The wave limb CONFIRMED (162) |
| **P.4** | intake rises **25–90 %** (point 2.9 M) | **⚑ FALSIFIED — +19.7 % (2,235,594)**, just below my band's floor |
| **P.5** | ⚑ **THE REFERENCE CELL DIES** (~65 %) | **⚑ FALSIFIED. Nothing dies, on any of eight cells** |
| **P.6** | ⚑ **T1 MISSED LOW — death before 159, point wave 154 ± 3** | **⚑ FALSIFIED. There is no death to be early or late.** I predicted an overshoot and got total inertness |
| **P.7** | T2 **falls** into [150, 215]; *"if the cell survives to 160, l4l stays within ±3 % of I-9's"* | **SPLIT — main limb FALSIFIED, escape limb CONFIRMED AT ZERO.** l4l is **223.265306122449**, identical to I-9 to the tenth of a millisecond: **0.000 %** |
| **P.8** | T3 UNEVALUABLE on missing waves if he dies early | **CONFIRMED-VACUOUSLY — 10/10 scored, 0 unevaluable.** The protection was not needed |
| **P.9** | the instant-kill clause **FIRES** somewhere in the surface (~55 %) | **⚑ FALSIFIED. 0 of 8 cells.** The deepest single tick anywhere is **0.717** of the bar |
| **P.10** | mean HP → [0.93, 0.975]; min intra ≤ 0.25; excursions EOT into [10, 40] | **⚑ FALSIFIED, ALL THREE LIMBS — 0.984048 / 0.3507 / 8.** All three moved the RIGHT WAY and none reached my bands; excursions did not move at all |
| **P.11** | deep-window count **0 → ≥ 5** | **CONFIRMED on the applied-damage instrument (10).** ⚑ On the like-for-like EOT instrument it is **1**, which is still the first non-zero in the run. Both reported (§ 4.1) |
| **P.12** | ⚑ **the bracket SPANS**: HASH → SPAWN differ on terminal wave by ≥ 3 waves | **⚑ FALSIFIED. They differ by ZERO.** Second lap running that a bracket has failed to span |
| **P.13** | ring gates + moving fraction unchanged if nobody dies | **CONFIRMED — every gate byte-identical to I-9** |
| **P.14** | S-WINDUP sits **strictly between** HASH and ENGAGE | **⚑ FALSIFIED — it sits OUTSIDE, on the shallow side** (§ 6), and so does SPAWN on the other axis |
| **P.15** | determinism ×2 EXACT ×3; batons FULL 67/67 ×3; Law 3 `moved: {}`; wall **20/20** | **SPLIT.** determinism **0 differences ×3** ✓ · batons **FULL 67/67 ×3** ✓ · Law 3 `moved: {}` ✓ · **wall 18/20** ✗ (§ 10) |
| **P.16** | D-I8-3 (`ManaBurnDrain`) not reached by a cell of record | **CONFIRMED** |

### 9.1 — ⚑ THE UNIFYING ERROR, AND I NAMED THIS ONE BEFORE THE RUN TOO

I-1 priced sustain not exposure · I-2 eHP not co-residence · I-3 throughput not reach · I-4 the
size of the counterplay not its shape · I-5 the repair not its convergence · I-6 the mean not the
variance · I-7 the numerator of a saturated ratio · I-8 the solver not the board it produces ·
I-9 the actuation not the arrival process it responds to.

**I-10: I priced the CORRELATION and not the DWELL** — and math note § 9.1 says exactly that, in
those words, before the run:

> *"A phase fold makes bodies swing together; it does not make them stay. If the referent's death
> required four bodies to be in the ring for several consecutive seconds — a pack that surrounds
> and holds — then correlating their clocks buys one big tick and the player walks out of it, and
> the 7.4 s survived excursion at 0.29 will still be unreachable because it is a DWELL phenomenon,
> not a BURST phenomenon. I will report the excursion-duration statistic whether or not it
> embarrasses this iteration."*

### ⚑ AND IT DOES EMBARRASS THIS ITERATION, SO HERE IS THE NUMBER.

| | **video (Lap K)** | **sim I-10, reference cell** |
|---|---:|---:|
| deepest SURVIVED excursion — floor | **0.291877** | 0.351201 |
| deepest SURVIVED excursion — **duration** | ⚑ **7.4167 s** | ⚑ **3.5102 s** |
| recovers to full | yes | yes (wave 166) |
| excursions matching the measured shape (floor ≤0.35 ∧ ≥5 s ∧ full recovery) | 1 | **0** |

**The sim's deepest excursion is 47 % as long as the referent's.** The fold bought the burst and
did not buy the hold. **Exactly as written, before the run.**

---

## 10 — ⚑ TWO RED CHECKS, BOTH DEFECTS IN MY OWN PREDICATES, NEITHER REPAIRED TO GREEN

Wall reads **18/20**. I-8 § 4.3 and I-9 § 10.1's precedent applies verbatim: leave the measured RED
standing and put the correctly-specified quantity beside it.

### 10.1 — ⚑ D-I10-1: CHECK 2 ASSERTS ON AN INPUT THE DRIVER NEVER PRODUCED

**Check 2 RED — "fold-OFF batons reproduce I-9's three baton digests byte-exactly"; measured
`got=None`.** I wrote a check whose input the driver never builds: the fold-off arms compute a
surface digest and are then discarded; their knots are never written, so no baton can be emitted
from them. **The check could not have passed no matter what the model did.**

**Executed OUT OF BAND, and it passes:** re-emitting the I-9 spec (`pm4-i9-cluster-defon`) at I-10
HEAD produces a baton in which `events`, `tracks`, `actors`, `waves`, `config` and `config_hash`
are all **EQUAL** to I-9's baton of record, and the masked digest is **EXACT**:
`d8965c26cceab7a70bcbe8bb2cf29db016f35c90ccc984d159f8ca324f00687d` on both.

⚑ **And the FULL-hash form of check 2 was never satisfiable in principle**, which is the part
worth banking: a baton's `sim_pin` carries `engine_version_full`, the engine git SHA. **Two batons
emitted at two different commits cannot hash-match, by construction.** Every future "baton
byte-identity" check in this run must be a MASKED-identity check over
`{_emitted_at, baton_run_id, sim_pin}` or it is asserting that git does not advance.

### 10.2 — CHECK 12 RED — MY OWN INVENTED THRESHOLD, ON THE THIRD ATTEMPT TO SPECIFY THIS PREDICATE

**Check 12 RED — "worst post-solve penetration < 1e-6 m on every cell"; measured
`8.96e-6 / 4.25e-6 / 7.48e-7`.** The math note rejected two wrong predicates for this check in
writing (== 0, and equality-to-I-9's-counts) and then I wrote a third: **a 1e-6 m bound I invented
in the check itself.** I-9 measured **8.959519020246276e-06** on `camp_defoff` — the identical
number. **The check is wrong about the world's scale, not about the world.**

**The correctly-specified quantity, and it is EXACT:** every convergence observable is IDENTICAL to
I-9 on all three cells — `pairs_above_tolerance_postsolve_total` **182 / 8 / 2**, worst penetration
**8.959519020246276e-06 / 4.253369068063506e-06 / 7.477930188404258e-07**, `t_s`, `n_ticks`.
**The I-8 invariant is untouched by this fold, digit for digit. I did not move the band after
seeing the number.**

### 10.3 — The eighteen that passed

layer 1a EXACT ×3 (1) · layer 1b EXACT ×3 (3) · ABSENT-not-None, registry empty ×3 (4) · three
Lap-K digests from bytes at FULL 64 hex (5) · the I-9 findings digest from bytes (6) · **the phase
law equivalence, 36,000 pairs, 0 mismatches (7)** · **0 early swings (8)** · **0 law violations on
1,405 emitted rows (9)** · the offense fold unchanged over shared waves (10) · the counterplay kit
unchanged limb-for-limb (11) · the intra-tick invariant, 0 violations (13) · 0 structural
violations (14) · determinism ×2 EXACT ×3 (15) · Law 3 `moved: {}` (16) · the hit test untouched
on a 12-point law grid (17) · the non-health exclusion counted (18) · **the T4b clause proved
READ-ONLY by grepping the package's own source (19)** · **the L-19 T3 vector reconstructed from
`pm4k_segments.csv` and matching the ledger to the hundredth (20)**.

### 10.4 — Discipline #3

**One process, one seed, start to finish.** Verified from the process table mid-run after I-9's
D-I9-2: a single `gamora_kc2_pm4_i10…` Python process (pid 51361) for the whole 369.9 s of wall.
The other matches in `pgrep` were my own monitor shells, whose command strings contain the
pattern — **named because a pgrep that matches its own watcher is exactly how a second process
hides.**

---

## 11 — ⚑ WHAT GOES TO THE CONDUCTOR

### 11.1 — ⚑ THE STRUCTURAL FINDING: FOUR SUBSYSTEMS, FOUR ABSORPTIONS, AND THE SAME NUMBER EVERY TIME

| lap | perturbation | terminal wave | like-for-like |
|---|---|---|---|
| **I-7** | +4,158 monster damage | unmoved | unmoved |
| **I-8** | +129,150 damage; every body's position re-solved to float32 precision | unmoved | 233.551 → 223.265 |
| **I-9** | **−486,590** damage-prevention withdrawn (0 %→29 % of every point taken) | unmoved | **223.265306122449** |
| **I-10** | arrival phase re-anchored; intake **+368,637 (+19.7 %)**; coincidence 21→28; depth −0.186→−0.313 | **unmoved** | ⚑ **223.265306122449** |

> ### ⚑ THE LIKE-FOR-LIKE HAS NOT MOVED BY ONE FLOATING-POINT BIT IN THREE ITERATIONS, ACROSS PERTURBATIONS OF THE PLAYER'S DEFENCE, THE MONSTERS' MAGNITUDES AND THE MONSTERS' TIMING.
> **And the reason is now provable rather than suspected:** wave duration is set by **the player's
> damage output**, which is a constant `player_damage_per_tick` against a board whose eHP is fixed
> by the wave tables. Nothing on the monster side — not their damage, not their positions, not
> their timing — can move it while the player survives. **T2 and T3 are, in this model,
> FUNCTIONS OF THE PLAYER'S OFFENCE ALONE.** Every iteration since I-7 has been perturbing
> variables that provably cannot reach two of the four target bands.
>
> ⚑ **That is a claim about the model's structure, not about this fold, and it is the thing I most
> want the conductor to rule on.** If T2/T3 are to move, the next iteration has to be on the
> **player's damage output** — the one term this run has never folded, and the one that sets
> both. `player_damage_per_tick` is `PLAYER_DAMAGE_LIMB`, a limb selected at I-1 and unexamined
> since.

### 11.2 — ⚑ THE BRACKET SHAPE R-PM4-2 PRESCRIBES DOES NOT FIT A PHASE

§ 6 measured it: **the record limb is more lethal than both declared bracket ends**, and the
fourth limb sits outside on the other side. LO/HI bracketing assumes the under-determined quantity
is a scalar with a monotone effect. **φ is a point on a circle, and "more correlated" is not
"further along the dial"** — SPAWN correlates bodies that are still out of reach, so its
correlation is *wasted*. **The R-PM4-2 machinery is sound for magnitudes and mis-shaped for
timings; that is a conductor-level question about the run's own method, not mine to settle.**

### 11.3 — ⚑ THE DEEPEST CELL IN THE LAP GOES BELOW THE REFERENT'S FLOOR AND STILL DOES NOT DIE

`S-PHASE-HI-CLUSTER-OFF` takes an intra-tick floor of **0.2623** — below the video's measured
**0.291877** — with a deepest tick of **0.717 of the bar**, and survives to the arena wall. **The
model can now produce the referent's DEPTH and cannot produce its DEATH.** The gap between those
two facts is § 9.1's dwell, and § 11.1's untouched player-offence term.

### 11.4 — The instrument disagreement of § 4.1, and the defects

**§ 4.1** — I-9's "35 windows ≤ −0.30" and Lap K's "4 of 35" are two instruments on one referent
and they differ by ~9×. Flagged for the conductor because **I-9's number is in the ledger at L-18
and I-10 is scoring against a different one.**

**D-I10-1** (check 2 asserts on an input the driver never produced; and its FULL-hash form is
unsatisfiable across commits by construction) is **banked and closed by the out-of-band execution**
in § 10.1. **Check 12's third mis-specification** is banked in § 10.2. **D-I8-3** (`ManaBurnDrain`,
no measured resistance row) is **carried unchanged** — no cell of record reached it.

---

## 12 — WHAT I DID **NOT** TOUCH

Mitigation (85.28 % measured) · the R-PM2-5 percent-current-life cap (30.19 % of intake, and the
structural anti-tail named in math note § 5) · every slot magnitude, the to-hit model, crit,
attack speed · the converging solver, τ, the non-overlap invariant · the tick order · movement,
cadence, dash · K-1…K-6 entire · the seed (conductor seed 9) · **the BOARD-ROLL RNG**, so the 344
bodies, their records and their scatter are byte-identical to I-9's · Law 3 (`moved: {}`).

---

**Author:** gamora (simulation seam) · 2026-08-14 · math note first, code second, and the git
order (`533b97c8` → `a9ac9483` → …) is the proof.
