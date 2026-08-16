# KC2-PM4 · MICRO-LAP AD — THE T LEG · FINDINGS

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-16 · **Side:** REFERENT-ONLY
**Authority:** `R-PM4-75 part 4(ii)` — the second licensed referent-functional carve-out.
**Fires:** `UNREACHED-I28-1` (the lane gamora named by name and declined by name).
**Prereg:** `prereg.md`, sha256 `93ffe4b9927eb94f100f5c5ba826bfeeafc6f447c52f4d712bf38c00381d7505`,
committed **ALONE** at `052008ee` before a single number of this lap existed.
**HALTs:** 0 · **Determinism:** ×2 byte-identical · **Predictions:** 9 PASS / 1 FAIL,
wording unchanged.

---

## 1 — HEADLINE

**`T_ref` is emitted for waves 151–160, `F-AD-1` PASSES at the primary rung, and the T leg turns
out to be the 9-cut segmentation itself wearing different arithmetic.**

Three sentences the conductor should carry forward:

1. **The gate closes.** `L_agg(293.6) = 3.352406` against the pinned bracket `3.3519` —
   `rel_dev = +1.510e-04`, inside `TOL = 5.0e-3` and inside the **a-priori worst-case rounding
   budget of 9.2e-4** that the prereg fixed before the number existed. The interval machinery, the
   per-wave partition and `T_ref` together reproduce the run's own pinned occupancy figure. Both
   secondary rungs close too (`+1.094e-04` at 285.7, `+1.503e-04` at 300.0). `T_ref` is licensed.

2. **The aggregation rule was byte-cited, and the byte-citation was load-bearing.** The pinned
   bracket is an **observed-instant-weighted** mean — *neither* of the two options the commission
   offered. The two rules it is **not** miss by roughly two orders of magnitude more than
   tolerance: the unweighted per-wave mean by `−8.91e-2`, the wall-clock time-weighted mean by
   `−5.92e-2`. Had I guessed, I would have guessed wrong, and the gate would have failed for a
   reason that had nothing to do with `T_ref`.

3. ⚑ **The T leg is not a new measurement, and the findings say so first rather than last.**
   `observed_fraction` is *constructed* at `pm4ac_residence_2026_08_16.py:388` as
   `len(wobs)/((WAVE_END[w]−WAVE_START[w])/DT)`, so `n_obs/obs_frac/60` is an **algebraic inverse**
   that recovers `WAVE_END[w] − WAVE_START[w]` to 4-dp rounding. `T_ref` therefore carries
   **`OBS-H2-6`'s ±0.25 s per cut**, not the ±1 frame its six decimal places suggest. This was
   written into the prereg (§ 2.2) before computing, precisely so that it could not later be
   discovered as good news.

**What this lap did not do:** it touched no sim quantity, opened no sim artifact, and placed nothing
beside a sim number. `T_ref` leaves here as a pinned artifact for the conductor to route into I-29.
The comparison is not mine to make and I did not make it.

---

## 2 — `F-AD-1` — GATE VERDICT, WITH THE BYTE-CITED AGGREGATION RULE

### 2.1 Verdict

| rung `R_gpx` | status | `L_pinned` (I2) | `L_agg` (this lap) | `rel_dev` | `TOL` | verdict |
|---:|---|---:|---:|---:|---:|:--|
| **293.6** | **PRIMARY** | 3.3519 | **3.352406** | **+1.510e-04** | 5.0e-3 | **PASS** |
| 285.7 | secondary | 3.2423 | 3.242655 | +1.094e-04 | 5.0e-3 | PASS |
| 300.0 | secondary | 3.4251 | 3.425615 | +1.503e-04 | 5.0e-3 | PASS |

The verdict of record is the primary rung's. The secondaries are corroboration, and the three
together are **a bracket that stays a bracket** (`R-PM4-70`) — they are not a sensitivity to be
collapsed to a mean. `R = 150.0` is **absent from this table by design** (`Lap AC DO-NOT 7`).

⚑ **The deviation is rounding, and it was predicted to be rounding before it was seen.** The prereg
§ 4.2 budget, fixed a priori:

| source | a-priori bound |
|---|---:|
| per-interval `body_time_s = round(n·DT, 4)` (`pm4ac_residence:295`) over 10,205 intervals | 9.0e-4 |
| per-wave `total_body_time_s = round(…, 3)` (`pm4ac_residence:393`) over 10 waves | 8.8e-6 |
| pinned `mean_occupancy = round(…, 4)` (`pm4r_contact:266`) | 1.5e-5 |
| `observed_fraction` 4-dp rounding | **0 — cancels identically** (§ 2.2) |
| **worst-case total** | **9.2e-4** |

Observed `1.51e-4` is **6.1× inside** that bound. The sign is positive on all three rungs, which is
the expected signature of `round(n/60, 4)` biasing single-frame intervals upward
(`round(1/60,4) = 0.0167`, `+3.33e-5 s` each). Nothing here needed explaining after the fact.

### 2.2 The aggregation rule — read from the pinned artifact's own construction, byte-cited

The commission required the rule be established by byte-citation, not guessed, and asked whether it
is time-weighted or a per-wave mean. **It is neither.**

`pm4r_contact_2026_08_14.py` (sha256 `8994b96a8da280e031fd6d795e8db7b5894910c4b8a233b4b064e1010068f2a7`):

- **`:58`** — `times = sorted(t for t in P if FIGHT_T0 <= t <= FIGHT_T1)`, with `P` the player-plate
  map built at **`:50-52`**. The unit of aggregation is **an instant at which a player plate was
  detected**.
- **`:248-252`** — `cc` is built as *one integer per element of `times`*: the in-ring monster-plate
  count at that instant.
- **`:266`** — `mean_occupancy = round(float(cc.mean()), 4)`. An **unweighted mean over `times`**.
- **`:59-61`**, echoed in the CSV's own `basis` column — *"instants without a player plate are
  **EXCLUDED, not imputed**"*, over *"10216 instants with a detected player plate"*.

The waves never appear in that computation, so it is **not a per-wave mean**. Un-covered instants
are dropped rather than carried, and coverage is **not uniform across waves** (0.8993–0.9765), so it
is **not a wall-clock time-weighted mean**. It is an **observed-time-weighted** mean: each wave
contributes in proportion to its *covered* duration.

Stated exactly, with `B_A(w) = total_body_time_s(w)` at rung A and `N_obs = Σ_w n_obs(w)`:

```
L_pinned  =  Σ_intervals n_frames / N_obs                     (pm4ac_residence:328,339 — F_AC_1)
          =  Σ_w B_A(w) / ( DT · Σ_w n_obs(w) )
          =  Σ_w B_A(w) / Σ_w [ observed_fraction(w) · T_ref(w) ]      ← T enters, exactly
```

the last step by the `:388` identity `observed_fraction(w)·T_ref(w) ≡ n_obs(w)·DT`, **in which the
4-dp rounding of `observed_fraction` cancels identically** — which is why the gate's residual is a
body-time rounding artefact and not a `T_ref` artefact. Equivalently:

```
L_agg = Σ_w L_recon(w)·ω(w) / Σ_w ω(w),   L_recon(w) = B_A(w)/T_ref(w),   ω(w) = obs_frac(w)·T_ref(w)
```

`Σ B_A = 570.803 s` · `Σ ω = 170.266667 s` · `Σ T_ref = 181.000477 s`.

### 2.3 The two rules it is not — published so the citation can be seen to matter

| candidate aggregation | value | `rel_dev` vs pinned | inside `TOL`? |
|---|---:|---:|:--|
| **`L_agg` — observed-time-weighted (byte-cited)** | **3.352406** | **+1.510e-04** | **YES** |
| `Σ B_A / (DT·N_obs)` — the same identity, computed directly | 3.352406 | +1.510e-04 | YES (agrees with `L_agg` to 1e-15) |
| `L_naive_mean` — unweighted per-wave mean | 3.053190 | −8.912e-02 | no, **18× over** |
| `L_walltime` — wall-clock duration-weighted | 3.153599 | −5.916e-02 | no, **12× over** |

`P-7` and `P-8` were blind and both PASS. The independent computation of the same identity two ways
(rows 1 and 2) agreeing to `1e-15` is the internal check that the algebra in § 2.2 is arithmetic and
not narrative.

### 2.4 Evaluability and the partition — verified, not assumed

Pre-declared floors, all cleared: 10/10 waves present · `N_obs = 10216 ≥ 10000` · every
`obs_frac(w) > 0` and `T_ref(w) > 0`.

Partition assembled in `R-PM4-75 part 3`'s **operational form** — from the artifact's own
construction, three levels of **explicit** key assignment, **zero unassigned keys**, an unassigned
key configured to HALT rather than default:

| level | keys present | USED | DECLARED-UNUSED | unassigned |
|---|---:|---:|---:|---:|
| `pm4ac_residence.json` top level | 22 | 2 | 20 | **0** |
| `residence["293.6"]` | 12 | 3 | 9 | **0** |
| `residence["293.6"].per_wave[*]` | 8 | 5 | 3 | **0** |

Exhaustiveness **verified**, not assumed: `Σ_w n_obs(w) = 10216 == 10216` (top-level
`n_observed_instants`) and `Σ_w n_intervals(w) = 10205 == 10205` (rung `n_intervals`). Both exact.
`D-I27-1 / D-E7-1 / D-I28-1` was three-in-three; this lap does not make it four.

---

## 3 — PER-WAVE `T_ref`, AND THE Σ-vs-WINDOW DECLARATION

### 3.1 The table

All columns below are in the committed artifact `pm4ad_t_ref.csv`
(sha256 `128074ad69e162b09446d5a1fd0be54fe75cd6ccadd92e978bcf6b01fff72fde`).

| wave | **`T_ref` (s)** | `T_direct` (s) | dev (s) | `n_obs` | `obs_frac` | `ω` = observed time (s) | `B_A` (s, **rung A = LOWER bound**) | `L_recon` = `B_A/T_ref` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 151 | **15.599785** | 15.600 | +0.000215 | 870 | 0.9295 | 14.500000 | 40.207 | 2.577407 |
| 152 | **16.299710** | 16.300 | +0.000290 | 955 | 0.9765 | 15.916667 | 44.307 | 2.718269 |
| 153 | **14.900367** | 14.900 | −0.000367 | 836 | 0.9351 | 13.933333 | 25.385 | 1.703649 |
| 154 | **14.199979** | 14.200 | +0.000021 | 795 | 0.9331 | 13.250000 | 58.294 | 4.105217 |
| 155 | **16.200807** | 16.200 | −0.000807 | 932 | 0.9588 | 15.533333 | 36.954 | 2.280998 |
| 156 | **20.200422** | 20.200 | −0.000422 | 1149 | 0.9480 | 19.150000 | 57.393 | 2.841178 |
| 157 | **19.299577** | 19.300 | +0.000423 | 1068 | 0.9223 | 17.800000 | 81.024 | 4.198227 |
| 158 | **12.999692** | 13.000 | +0.000308 | 759 | 0.9731 | 12.650000 | 33.638 | 2.587600 |
| 159 | **26.299213** | 26.300 | +0.000787 | 1503 | 0.9525 | 25.050000 | 113.646 | 4.321270 |
| 160 | **25.000927** | 25.000 | −0.000927 | 1349 | 0.8993 | 22.483333 | 79.955 | 3.198081 |
| **Σ** | **181.000477** | 181.000 | — | **10216** | — | **170.266667** | **570.803** | — |

**Range 12.9997 s (w158) – 26.2992 s (w159), ratio 2.023.** ⚑ Every value carries **±0.25 s** from
`OBS-H2-6`, so the honest read of, say, wave 159 is *"26.3 ± 0.25 s"* — the six decimals are the
arithmetic's, not the measurement's.

`T_direct` is the **transcription** cross-check: the same spans parsed from bytes out of
`pm4r_contact_occupancy.csv`'s `basis` column (`"wave span 683.0-698.6 s (Lap H-2 OBS-H2-6, +-0.25
s)"`, rows 17–26). Max deviation **0.000927 s**, `P-1` PASS. ⚑ **This is not an independent
measurement.** Both descend from `WAVE_START` at `pm4r_lib_2026_08_14.py:52-55`. Agreement proves
the segmentation survived transit through two laps intact; it proves **nothing** about whether the
segmentation is right.

`T_ref` is **rung-invariant** across all four rungs in the source (`P-2` PASS), as its construction
requires — `obs_times` at `pm4ac_residence:384` carries no ring radius. Rung `150.0` was read for
**this check only**; no body-time, occupancy or residence quantity at `R = 150.0` was read, pooled
or published (`Lap AC DO-NOT 7`).

### 3.2 ⚑ Σ `T_ref` vs the fight window — a TAUTOLOGY, declared as one

`Σ T_ref = 181.000477 s` · fight window `[683.0, 864.0]` = `181.0 s` · **gap = −0.000477 s**.

The gap is **zero to rounding, and that confirms nothing about the referent.**
`pm4r_lib_2026_08_14.py:58` sets `WAVE_END[w] = WAVE_START[w+1]` for `w < 160` and
`WAVE_END[160] = FIGHT_T1`. The ten windows therefore **telescope** across the fight window **by
construction**: exhaustive, non-overlapping, and admitting **no inter-wave dead time by
definition**. The 9 cuts are *partition boundaries*, not *events with duration*. A zero gap
demonstrates that this lap read line 58 correctly. That is its entire content, and the prereg said
so before the number was computed.

⚑ **`UNREACHED-AD-1` — whether inter-wave dead time exists in the referent at all.** A wave-N clear
and a wave-N+1 spawn may well be separated by real seconds of nothing. This segmentation **cannot
see them**, because `OBS-H2-6` cuts at the wave-counter *digit change* and assigns every intervening
second to one wave or the other. **Obstacle named:** the wave counter is the only pinned clock in
this footage and it *partitions* rather than *brackets*. Closable only by a second, independent
end-of-wave signal (last-monster-death, or spawn-burst onset) — neither exists as a pinned artifact
in this run.

### 3.3 ⚑ THE COVERAGE HAZARD — the most consequential thing this lap found for I-29

`L_recon(w) = B_A(w)/T_ref(w)` is the functional the commission named, and it is emitted as named.
But `B_A(w)` can only accrue **at instants where a player plate was detected**, while `T_ref(w)` is
the **whole wall-clock window**. `L_recon(w)` is therefore a **coverage-deflated** occupancy, and
the deflation is exactly `obs_frac(w)` — which **varies wave to wave from 0.8993 to 0.9765**, i.e. a
**2.4 %–11.2 % wave-varying downward bias**.

The coverage-corrected form is `B_A(w)/ω(w) = L_recon(w)/obs_frac(w)`, computable directly from two
committed columns of `pm4ad_t_ref.csv`:

| wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `L_recon` | 2.5774 | 2.7183 | 1.7036 | 4.1052 | 2.2810 | 2.8412 | 4.1982 | 2.5876 | 4.3213 | 3.1981 |
| `B_A/ω` (coverage-corrected) | 2.7729 | 2.7837 | 1.8219 | 4.3995 | 2.3790 | 2.9970 | 4.5519 | 2.6591 | 4.5368 | 3.5562 |

⚑ **The choice between these two is not cosmetic and it is not mine to make.** It reorders the
waves: `L_recon` peaks at **wave 159**; coverage-corrected it peaks at **wave 157**. It is the
reason `P-10` reads FAIL below and would read PASS under the other functional — and I have left the
FAIL standing rather than switching functionals to collect a PASS. **I-29 must declare which of the
two it uses, and if it uses `L_recon` it inherits a wave-varying 2.4–11.2 % downward bias that no
sim quantity shares.** This is `DO-NOT AD-2` and it is the single most useful sentence this
micro-lap produces.

---

## 4 — DEFECT TABLE (self-caught, pre-claim)

| id | class | what | when caught | disposition |
|---|---|---|---|---|
| — | — | **No computational defect was found in this lap.** | — | Reported as the absence it is, not as a claim of virtue. The lap is small, its arithmetic is four lines, and both determinism runs and the two-way identity check in § 2.3 agree; that is the extent of the assurance and I do not inflate it. |
| `PD-AD-1` | **declared process deviation, NOT a defect** | One **POST-HOC verification** was added to the instrument *after* the first numbers were seen: Lap R's per-wave instant counts in its `basis` text vs Lap AC's `n_observed_instants`. | self, at self-audit before any claim | Added, and **labelled `POST-HOC` in the emitted JSON's own key and value**. It **grades nothing**, is **not** a criterion, and **cannot change any verdict**. Proof it changed nothing: `pm4ad_t_ref.csv` is **byte-identical** (`128074ad…72fde`) to the pre-addition run. Result: exact on all ten waves and on `N_obs = 10216`. Declared here rather than quietly absorbed, because the prereg's authority comes from being complete and this is the one place it was extended. |

**Near-misses worth naming, since a defect table with nothing in it is usually a table that was not
looked at hard enough:**

- The prereg's `TOL = 5.0e-3` was budget-derived a priori at 9.2e-4 worst case. Observed `1.51e-4`.
  Had I set `TOL` at the budget rather than 5.4× it, the gate would still have passed — but the
  margin was **not** knowable in advance and the headroom was the right call, not a lucky one.
- `pm4r_contact:58` brackets the fight window **inclusively at both ends** while the per-wave
  windows are **half-open** with `WAVE_END[160] = 864.0` **exclusive**. An instant at exactly
  `t = 864.0` would sit in `times` and in **no** wave, silently breaking the § 2.2 identity. The
  pre-registered exhaustiveness check (§ 2.4) is what covers this; it came back exact
  (`10216 == 10216`), so no such instant exists. **This was covered by pre-registration rather than
  by luck** — but it is exactly the class of off-by-one that a "looks right" reading would have
  walked past, and it is named so the next lap keeps the check.

---

## 5 — PREDICTIONS (graded wording-unchanged from `prereg.md` § 6)

| id | prediction *(verbatim)* | grade | evidence |
|---|---|:--|---|
| `P-1` | `T_ref` agrees with `T_direct` to within **0.01 s** on all 10 waves | **PASS** | max abs dev 0.000927 s (w160); all 10 parsed |
| `P-2` | `T_ref` identical to 4 dp across all four rungs | **PASS** | 150.0 / 285.7 / 293.6 / 300.0 all agree |
| `P-3` | `Σ T_ref = 181.00 s ± 0.05 s` and equals `FIGHT_T1 − FIGHT_T0` | **PASS** | 181.000477 s, gap −0.000477 s |
| `P-4` | `F-AD-1` PASSES at rung 293.6 within `TOL = 5.0e-3` | **PASS** | rel_dev +1.510e-04 |
| `P-5` | `F-AD-1` also passes at 285.7 and 300.0 | **PASS** | +1.094e-04 / +1.503e-04 |
| `P-6` | partition exhaustive on both instants and intervals, exactly | **PASS** | 10216 == 10216 · 10205 == 10205 |
| `P-7` ⚑blind | `L_naive_mean` misses the pinned bracket by more than `TOL` | **PASS** | −8.912e-02, 18× over |
| `P-8` ⚑blind | `L_walltime` misses the pinned bracket by more than `TOL` | **PASS** | −5.916e-02, 12× over |
| `P-9` ⚑blind | `max_w T_ref / min_w T_ref ≥ 2.0` | **PASS** | 26.299213 / 12.999692 = **2.0231** |
| `P-10` ⚑blind | the longest-window wave is **not** the highest-`L_recon` wave | **FAIL** | both are **wave 159** |

**9 PASS / 1 FAIL. Nothing was retro-edited, softened, or dropped.**

⚑ **`P-9` passed by 1.5 %.** The window-length spread is `2.0231×`, against a threshold of `2.0`
declared blind. That is a hair, and it is reported as a hair: had the threshold been `2.05` it would
read FAIL, and the prediction is therefore weak evidence for anything beyond "the windows are not
uniform." **What the numbers do support without a threshold:** the windows lengthen materially over
the run (151–158 sit in 13.0–20.2 s; 159 and 160 are 26.3 and 25.0 s). **No mechanism is attributed
to that.** Whether it reflects more monsters, tougher monsters, longer travel, or the counter
lagging is **`UNREACHED-AD-3`** and this lap has no instrument that could tell them apart.

⚑ **`P-10`'s FAIL is informative and is deliberately left standing.** Wave 159 is simultaneously the
longest window (26.3 s) and the highest `L_recon` (4.321) — so the prediction that length and
occupancy would not coincide is wrong on this data. **Under the coverage-corrected functional
(§ 3.3) the peak moves to wave 157 and `P-10` would read PASS.** I did not switch functionals to
collect the PASS; the prereg named `L_recon` and `L_recon` is what was graded. The rule-dependence
is itself the finding, and it is the same finding as § 3.3. ⚑ **This is not evidence that longer
waves are busier** — wave 154 is one of the *shortest* windows (14.2 s) and carries the third
*highest* occupancy (4.105), so the relationship is not monotone and no trend is claimed.

---

## 6 — DETERMINISM

The instrument was run twice into separate output directories and every emitted artifact compared
by sha256:

| artifact | run 1 | run 2 | verdict |
|---|---|---|---|
| `pm4ad_t_ref.csv` | `128074ad…72fde` | `128074ad…72fde` | **IDENTICAL** |
| `pm4ad_t_ref.json` | `d7b18d3f…3d4e` | `d7b18d3f…3d4e` | **IDENTICAL** |

*(Truncations above are **LOCATORS**. The full-64 values, re-hashed from bytes, are in § 9.)*

A third pair of runs was executed after the `PD-AD-1` post-hoc block was added; the CSV came back
byte-identical to the pre-addition run, which is the proof that the addition changed no number.
No timestamps, no absolute paths of the run, and no dict-ordering non-determinism enter the emitted
artifacts (`sort_keys=True`).

---

## 7 — UNREACHED CENSUS (obstacle named on every one)

| id | what is unreached | obstacle, named |
|---|---|---|
| **`UNREACHED-AD-1`** | whether **inter-wave dead time exists in the referent** | `OBS-H2-6` cuts at the wave-counter digit change and **partitions** rather than **brackets**; every intervening second is assigned to one wave or the other by construction (`pm4r_lib:58`). Closable only by a second independent end-of-wave signal (last-monster-death or spawn-burst onset); no such pinned artifact exists in this run. |
| **`UNREACHED-AD-2`** | whether `T_ref`'s **±0.25 s** can be tightened | the wave counter is read at 4 fps by frame-difference on a 52×26 digit crop (`pm4r_lib:50-51`). Tightening means re-reading the counter at 60 fps — a new referent measurement, outside this micro-lap's licensed scope, and it would re-open a pinned segmentation that nine prior laps have built on. |
| **`UNREACHED-AD-3`** | **why** the later wave windows are longer | this lap has no instrument that can distinguish monster count, monster toughness, travel distance and counter lag. The correlation is reported; no mechanism is attributed. |
| **`UNREACHED-AD-4`** | which of `L_recon` and `B_A/ω` is the **right** per-wave occupancy for a cross-seam comparison | it depends on what the sim's own `T` counts, which is **sim-side** and this lap is forbidden to look. It is a **conductor ruling**, not a measurement. § 3.3 supplies both columns so the ruling can be made on numbers. |
| *carried* | `UNREACHED-AC-1..6`, `NAMED-AC-1`, `UNREACHED-I28-3/4/5` | unchanged by this lap; none was touched, closed, or narrowed. `UNREACHED-I28-1` **is closed by this lap** — the T leg is emitted and gated. |

---

## 8 — DO-NOT BLOCK

**New this lap:**

1. **DO NOT** treat `T_ref`'s decimals as its precision. Every value carries **±0.25 s** from
   `OBS-H2-6`. Quote wave 159 as **26.3 ± 0.25 s**, never as 26.299213 s. The six decimals exist
   because the arithmetic is an algebraic inverse (§ 1.3), not because the clock is that good.
2. ⚑ **DO NOT** use `L_recon(w) = B_A(w)/T_ref(w)` in any cross-seam comparison **without declaring
   the coverage convention**. It is **coverage-deflated by `obs_frac(w)`, which varies 0.8993–0.9765
   across waves** — a 2.4–11.2 % wave-varying downward bias that no sim quantity shares. Either use
   `B_A(w)/ω(w)` or state the bias. Both columns are committed; there is no excuse for silence
   (§ 3.3, `UNREACHED-AD-4`).
3. **DO NOT** read `Σ T_ref = 181.0` as evidence that referent waves run back-to-back with no dead
   time. The windows telescope **by construction** (`pm4r_lib:58`); the sum is a tautology and the
   dead-time question is `UNREACHED-AD-1` (§ 3.2).
4. **DO NOT** cite `T_direct`'s agreement as independent corroboration of the segmentation. It is a
   **transcription** check between two artifacts descending from the same `WAVE_START` dictionary
   (§ 3.1).
5. **DO NOT** aggregate per-wave occupancies by an unweighted mean or by wall-clock duration when
   comparing to the pinned bracket. Both are wrong against the pinned construction by 18× and 12×
   the gate tolerance respectively (§ 2.3). The rule is **observed-instant weighting**.
6. **DO NOT** read `F-AD-1`'s PASS as a re-derivation or a confirmation of the occupancy bracket.
   It is a **fidelity gate on `T_ref`**. The bracket is pinned and stays pinned; this lap produces
   no competing occupancy figure (Lap AC § 4.7, carried).
7. **DO NOT** compare any number in this lap to any sim quantity. `T_ref` is emitted **as a pinned
   artifact for the conductor's I-29 commission**; this lap placed nothing side by side and no
   licence to do so is created by its existence.

**All prior DO-NOT blocks carried unchanged and cumulative:** Lap V § 7.2 · Lap V-2 § 11.2 ·
Lap W § 7.2 · Lap X § 12.2 · Lap Y § 11.6 · Lap Z § 5 · Lap AA § 6 · **Lap AB § 9 (all ten)** ·
**Lap AC § 9 (all nine)** · **I-28's eight**. Specifically exercised here:

- **Lap AB DO-NOT 9** — `pm4u_arrivals.csv` was **not opened**, cited, or derived from. It is not an
  input and appears in the prereg's explicit NOT-AN-INPUT list.
- **Lap AC DO-NOT 3** — **no referent residence scalar is quoted.** `B_A(w)` appears only as the
  numerator of a ratio, labelled **"rung A = LOWER bound"** in the CSV, in the § 3.1 header and in
  the emitted JSON's `bound_direction` field, every time it appears.
- **Lap AC DO-NOT 4** — no quantity here is compared to any sim quantity.
- **Lap AC DO-NOT 6** — every count is a LOWER bound; plate absence never proves body absence.
- **Lap AC DO-NOT 7** — `R = 150.0` was read **only** for the rung-free `T_ref` invariance check and
  is absent from every table of body-time, occupancy and bracket in this note.
- **Lap AC DO-NOT 8** — nothing was converted to metres. This lap deals in seconds.
- **Lap AC DO-NOT 9** — no track count was used as a body count. This lap uses **no body count at
  all**; `N` is I-29's leg.
- **`R-PM4-72 part 4`** — `share_player` was not touched, quoted, or reasoned about.
- **`R-PM4-75 part 2` / `I-28 DO-NOT 8`** — every full-64 in § 9 is re-hashed from bytes; no
  truncated pin anywhere was expanded from memory.

---

## 9 — FULL-64 DIGEST TABLE (re-hashed from bytes at the moment of writing)

⚑ **`R-PM4-75 part 2`:** a truncated pin is a **LOCATOR**, not a digest. Every value below was
produced by hashing the file on disk while writing this table. No prefix-plus-suffix from the
charter, from a prior lap's prose, or from memory was expanded to 64 characters
(`D-I28-3`'s hazard, not repeated).

**Emitted by this lap:**

| artifact | sha256 |
|---|---|
| `prereg.md` (committed **ALONE** at `052008ee`) | `93ffe4b9927eb94f100f5c5ba826bfeeafc6f447c52f4d712bf38c00381d7505` |
| `pm4ad_t_ref.csv` | `128074ad69e162b09446d5a1fd0be54fe75cd6ccadd92e978bcf6b01fff72fde` |
| `pm4ad_t_ref.json` | `d7b18d3fc2f992d6a5f46746f635f703ac09caaf17fa8c720d66f2ebce293d4e` |
| `pm4ad_findings.md` (this file) | published in `pm4ad_digests.json`, hashed after this file's final write; the conductor re-hashes from its own seat |

**Instruments:**

| script | sha256 |
|---|---|
| `pm4ad_t_leg_2026_08_16.py` | `34d77f15302f71ae34faa5250304a6cd483f87c9f82f24e6dd997e301210704c` |
| `pm4ad_digests_2026_08_16.py` | `a4bd2dd96c9ff01d26177edfe9cac21b4d85379dc89b667132beabb300dca8d7` |

**Inputs (each asserted at instrument start; nine EXACT, zero mismatches, zero HALTs):**

| input | sha256 |
|---|---|
| `pm4ac_residence.json` *(verified twice — pin **and** Lap AC's own manifest)* | `bdf02b2278d2f62d23d590b6a196efd0e4ef181dff8e9992b75f1c805f037f14` |
| `pm4ac_digests.json` | `17f10603ecc45faf0002ee4978d198a741484f23f4be17f77ccc69ca2dc6a1e3` |
| `pm4ac_findings.md` *(read for method, never quoted for a number)* | `28cd24aaf05116ea5c363f1ecaf1b02cd51486564b933be7f02cd137b856d4bd` |
| `pm4r_contact_occupancy.csv` *(the pinned bracket)* | `913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6` |
| `pm4ac_residence_2026_08_16.py` | `58b7a87c94791f83b497ee9ba23d0defdafd731825c28f7b35f9d12f426c1c07` |
| `pm4ac_lib_2026_08_16.py` | `4cd928bf265fb15972d1bd7a0a4aed5ab0b6209d1c96d8e4c3de0687b5e26b74` |
| `pm4r_contact_2026_08_14.py` *(aggregation rule read from here)* | `8994b96a8da280e031fd6d795e8db7b5894910c4b8a233b4b064e1010068f2a7` |
| `pm4r_lib_2026_08_14.py` | `630bede0bbc10389dca79d04601d319d37a02f266d406c0aad837480b110762b` |

**Commits (meta-repo, this lap):** `052008ee` prereg **ALONE** → `f776f01b` instrument + emitted
artifacts → *(this findings commit)*.

---

## 10 — FIREWALL — WHAT THIS LAP DID NOT DO

1. **No sim artifact, cell, ledger, output directory or code path was opened.** Referent side only,
   start to finish.
2. **No comparison of any quantity to any sim quantity**, in prose, in a table, or by adjacency.
   `T_ref` is emitted as a pinned artifact **for** I-29; making the comparison is the conductor's
   commission and this lap did not pre-empt a line of it.
3. **The occupancy bracket was not re-derived.** `F-AD-1` is a fidelity gate. `3.3519` is pinned and
   stays pinned; `3.352406` is a reconstruction *of* it, never a competitor *to* it.
4. **The segmentation was not re-measured.** The 9 cuts are `OBS-H2-6`'s. This lap re-expresses them
   in a different arithmetic and does not adjudicate their ±0.25 s.
5. **Nothing was tuned.** No config, no frozen ensemble (`E-s09-cp150` untouched), no pinned
   instrument modified. Lap AC's and Lap R's scripts were opened read-only and their digests are
   unchanged after this lap as before it.
6. **No designation by grade.** Nothing here is called good, bad, better, worse, high or low.
   `T_ref` is 12.9997–26.2992 s; that is a length, not a verdict.
7. **No metre conversion, no body count, no arrival rate, no residence scalar quoted.**
8. **`UNREACHED-AD-4` was not decided.** Which per-wave functional I-29 should use depends on
   sim-side facts this lap is forbidden to look at. Both columns are supplied; the ruling is not
   mine and I did not make it by implication.

---

*Micro-lap AD ends. `T_ref` is pinned, gated, and on the conductor's desk. Zero HALTs.*
