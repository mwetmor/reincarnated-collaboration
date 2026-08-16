# KC2-PM4 · MICRO-LAP AD — THE T LEG · PRE-REGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-16 · **Side:** REFERENT-ONLY
**Authority:** `R-PM4-75 part 4(ii)` — the SECOND licensed referent-functional carve-out:
*per-wave referent wave-window duration in referent-clock seconds, waves 151–160, from Lap AC's own
9-cut segmentation arithmetic* (`n_observed_instants / observed_fraction / 60`, Lap AC § 4.6).
Fires `UNREACHED-I28-1`, which gamora's I-28 named by lane and declined by name.

**This file is committed ALONE, before any number of this lap is computed.** Nothing below is
adjusted after the fact. Every criterion, tolerance, prediction, HALT condition and gate-failure
landing site is fixed here in the wording that will be graded.

---

## 0 — WHAT THIS LAP IS, IN ONE PARAGRAPH

The run carries a standing ~17× occupancy residual whose arithmetic decomposition is
`L = Q · N / T`. I-28 (gamora, `L-65`) closed the `Q` leg — body-time per decoded body — and found
the sim BELOW the referent bracket on 10/10 evaluable pairs. The `T` leg — how long a referent wave
*window* lasts in referent-clock seconds — has never been emitted as a pinned artifact. It is the
last arithmetic term I-29 needs. This lap emits it, gates it against the run's own pinned occupancy
bracket, and **stops there**. It computes no sim quantity, opens no sim artifact, and places nothing
side by side with a sim number. `T_ref` leaves this lap as a pinned artifact for the conductor to
route; the comparison is I-29's, not mine.

---

## 1 — INPUT PINS (asserted at instrument start; MISMATCH ⇒ HALT)

Every number entering this lap enters through one of these files, **never through prose**
(`R-PM4-67 part 2` / `D-CON-6`). The instrument asserts each digest before reading any content and
aborts the process on the first mismatch.

| # | path (repo-relative) | sha256 (full 64, re-hashed from bytes at prereg time) | role |
|---|---|---|---|
| I1 | `agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/pm4ac_residence.json` | `bdf02b2278d2f62d23d590b6a196efd0e4ef181dff8e9992b75f1c805f037f14` | **the T source** — `residence[RC].per_wave[*]` `n_observed_instants`, `observed_fraction`; **and** `total_body_time_s` = `B_A(w)` for the gate |
| I2 | `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-r-locomotion-contact/pm4r_contact_occupancy.csv` | `913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6` | **the pinned bracket** (`scope=at_sim_D_ENGAGE_M_2.400`) **and** the independently-transcribed wave spans in the `basis` column |
| I3 | `agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/pm4ac_digests.json` | `17f10603ecc45faf0002ee4978d198a741484f23f4be17f77ccc69ca2dc6a1e3` | Lap AC's own digest manifest — I1's pin is re-checked against **its** recorded value, so I1 is verified twice |
| I4 | `agentic_orchestration/research/scripts/pm4ac_residence_2026_08_16.py` | `58b7a87c94791f83b497ee9ba23d0defdafd731825c28f7b35f9d12f426c1c07` | construction-of-record for `observed_fraction`, `body_time_s`, the per-wave partition |
| I5 | `agentic_orchestration/research/scripts/pm4ac_lib_2026_08_16.py` | `4cd928bf265fb15972d1bd7a0a4aed5ab0b6209d1c96d8e4c3de0687b5e26b74` | `DT`, `FPS`, `RING_PRIMARY` |
| I6 | `agentic_orchestration/research/scripts/pm4r_contact_2026_08_14.py` | `8994b96a8da280e031fd6d795e8db7b5894910c4b8a233b4b064e1010068f2a7` | construction-of-record for `mean_occupancy` — **the aggregation rule is read from here** |
| I7 | `agentic_orchestration/research/scripts/pm4r_lib_2026_08_14.py` | `630bede0bbc10389dca79d04601d319d37a02f266d406c0aad837480b110762b` | `WAVE_START`, `WAVE_END`, `FIGHT_T0`, `FIGHT_T1` |
| I8 | `agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/pm4ac_findings.md` | `28cd24aaf05116ea5c363f1ecaf1b02cd51486564b933be7f02cd137b856d4bd` | Lap AC findings — pinned for provenance; **read for method, never quoted for a number** |
| I9 | *this file* | computed after write, published in the findings digest table | prereg |

⚑ **NOT AN INPUT, DELIBERATELY:** `pm4u_arrivals.csv` (Lap AB DO-NOT 9 — this lap does not open,
cite or derive from it) · every sim artifact, cell, ledger and code path without exception ·
`pm4ac_ring_intervals.csv` (7.2 MB; the per-wave aggregates in I1 are the pinned form of it and the
raw file is not needed — if the gate requires it, that is a HALT, see § 8).

---

## 2 — THE FUNCTIONAL: `T_ref(w)`

### 2.1 Definition (the licensed lane, verbatim from the ruling)

For each wave `w ∈ {151 … 160}`, at rung `RC`:

```
T_ref(w)  =  n_observed_instants(w)  /  observed_fraction(w)  /  60      [referent-clock seconds]
```

with both operands taken **by identity** from
`I1 :: residence[str(RC)].per_wave[i]` where `per_wave[i]["wave"] == w`.

The divisor 60 is `FPS`, pinned at `I5:83` (`FPS = 60.0`), `DT = 1.0 / FPS` at `I5:84`.

### 2.2 What this arithmetic actually is — declared in advance, not discovered after

`observed_fraction` is constructed at **`I4:388`**:

```python
observed_fraction=round(len(wobs) / max((WAVE_END[w] - WAVE_START[w]) / DT, 1), 4),
```

with `wobs` defined one line earlier at **`I4:384`** as
`[t for t in obs_times if WAVE_START[w] <= t < WAVE_END[w]]`, and
`n_observed_instants = len(wobs)` at **`I4:387`**.

⚑ **Therefore `T_ref(w)` as licensed is an algebraic INVERSE of the wave-window span itself**, not an
independent measurement of it:

```
n_obs(w) / obs_frac(w) · DT  ≡  n_obs(w) / [ n_obs(w) · DT / (WAVE_END[w] − WAVE_START[w]) ] · DT
                             ≡  WAVE_END[w] − WAVE_START[w]                (exact but for the 4-dp round)
```

This is stated **here, before computing**, because it is the single most important honest thing this
lap can say about its own product: the T leg is **the 9-cut segmentation recovered to rounding
precision**, and its uncertainty is the segmentation's uncertainty (`Lap H-2 OBS-H2-6`, **±0.25 s**
per cut, from a 4 fps frame-difference read of the wave-counter digit crop — `I7:50-51`), **not**
the ±1-frame resolution the arithmetic superficially suggests. Any downstream consumer that treats
`T_ref` as a 4-decimal-place quantity is over-reading it. § 6.3 carries this as a DO-NOT.

### 2.3 The independent-transcription cross-check (`T_direct`)

`I2`'s `basis` column, rows `scope=per_wave`, carries the same spans as free text, e.g.
`"wave span 683.0-698.6 s (Lap H-2 OBS-H2-6, +-0.25 s), 870 instants"` (`I2:17`). The instrument
parses these **from bytes** with a strict regex and emits `T_direct(w)`.

⚑ **This is a TRANSCRIPTION check, not an independent measurement.** Both `T_ref` and `T_direct`
descend from the same `WAVE_START` dictionary (`I7:52-55`); agreement demonstrates that no lap
mangled the segmentation in transit, and demonstrates **nothing whatever** about whether the
segmentation is correct. Pre-declared as such so that a PASS cannot later be over-read.

### 2.4 Rung-dependence: pre-declared as NONE

`n_observed_instants` and `observed_fraction` are built from `obs_times` (`I4:384`), which is the
player-plate instant set and carries **no** ring radius. `T_ref` must therefore be **bit-identical
across all four rungs** present in I1 (`150.0`, `285.7`, `293.6`, `300.0`). This is checked (`P-2`)
and a failure is a **HALT**, not a finding — it would mean the artifact is not what its own
construction says it is.

⚑ **DO-NOT 7 compliance (Lap AC § 9.7):** rung `150.0` is touched in this lap for **exactly one
purpose** — the `T_ref` rung-invariance check, on quantities that are rung-free by construction. No
body-time, occupancy, residence or bracket quantity at `R = 150.0` is read, pooled, averaged or
published anywhere in this lap.

---

## 3 — THE AGGREGATION RULE, READ FROM THE PINNED ARTIFACT'S OWN CONSTRUCTION

The commission requires the aggregation rule be **byte-cited from the pinned bracket's own
construction, not guessed**. It is.

### 3.1 What the pinned bracket is

`I2:28` — `at_sim_D_ENGAGE_M_2.400 , , 293.6 , 0.201938 , 3.3519 , , 352 , 2.75 ,
"2.400 m converted at 122.32 ground px/m (anchor bracket, NOT ruled)"`.

Its `mean_occupancy` is produced at **`I6:266`**:

```python
mean_occupancy=round(float(cc.mean()), 4),
```

where `cc` is built at **`I6:248-252`** as one integer per element of `times`, and `times` is defined
at **`I6:58`**:

```python
times = sorted(t for t in P if FIGHT_T0 <= t <= FIGHT_T1)
```

`P` being the player-plate map (`I6:50-52`). `I6:59-61` prints, and the CSV `basis` column for the
whole-fight rows records, `"10216 instants with a detected player plate"`, and states in the same
breath that *"instants without a player plate are EXCLUDED, not imputed"*.

### 3.2 ⚑ THE RULE, STATED — and it is NEITHER of the two options the commission offered

The pinned bracket is an **unweighted mean over OBSERVED PLAYER-PLATE INSTANTS**, over the whole
fight window `[683.0, 864.0]`. It is:

- **not** a per-wave mean (the waves never appear in `I6:248-266`);
- **not** a wall-clock time-weighted mean (instants without a player plate are dropped, `I6:58`,
  and coverage is not uniform across waves — Lap AC § 4.5 limit 5 records 0.8993–0.9765);
- it **is** an **observed-time-weighted** mean: each wave contributes in proportion to
  `n_obs(w)`, i.e. to its *covered* duration, not its wall duration.

Expressed exactly, with `N_obs = Σ_w n_obs(w)` and `B_A(w) = total_body_time_s(w)` at rung `RC`:

```
L_pinned(RC)  =  Σ_intervals n_frames / N_obs                          (I1 :: F_AC_1.functional)
              =  [ Σ_w B_A(w) / DT ] / N_obs
              =  Σ_w B_A(w)  /  ( DT · Σ_w n_obs(w) )
              =  Σ_w B_A(w)  /  Σ_w [ obs_frac(w) · T_ref(w) ]          ← T enters here, exactly
```

the last step by § 2.2's identity `obs_frac(w) · T_ref(w) ≡ n_obs(w) · DT`, in which **the 4-dp
rounding of `obs_frac` cancels identically**. Equivalently, as a weighted mean of the per-wave
reconstructions:

```
L_agg(RC)  =  Σ_w  L_recon(w) · ω(w)  /  Σ_w ω(w) ,
   with     L_recon(w) = B_A(w) / T_ref(w)          (the commission's per-wave functional)
   and      ω(w)       = obs_frac(w) · T_ref(w)     (OBSERVED time in wave w — the byte-cited weight)
```

**`L_agg` is the gate statistic.** The weight `ω` is not chosen; it is what `I6:58`'s exclusion of
un-covered instants forces.

### 3.3 The two rules that will be reported and are pre-declared to be WRONG

Both are computed and published beside `L_agg`, so the reader can see that the byte-citation was
load-bearing rather than decorative:

- `L_naive_mean = (1/10) · Σ_w L_recon(w)` — the unweighted per-wave mean;
- `L_walltime  = Σ_w B_A(w) / Σ_w T_ref(w)` — the wall-clock time-weighted mean (drops `obs_frac`).

`P-7` and `P-8` predict both MISS the pinned value by more than the gate tolerance. If either
matches within tolerance the finding is that the byte-citation was **not** discriminating here, and
it will be reported in exactly those words.

---

## 4 — GATE `F-AD-1` (pre-registered in full, before any number)

### 4.1 Statement

> At the **primary rung `RC = 293.6`**, the reconstruction
> `L_agg(293.6) = Σ_w B_A(w) / Σ_w [obs_frac(w) · T_ref(w)]`,
> assembled over `w = 151…160` from I1 by identity, using the § 3.2 aggregation rule read from I6,
> must reproduce the pinned `mean_occupancy` at `R_gpx = 293.6, scope = at_sim_D_ENGAGE_M_2.400` in
> I2, with **relative deviation `|L_agg / L_pinned − 1| ≤ TOL`**.

### 4.2 `TOL = 5.0e-3`, and the budget that justifies it — fixed here

Derived a priori from the published precision of the operands, **before seeing any deviation**:

| source of deviation | bound |
|---|---|
| per-interval `body_time_s = round(n·DT, 4)` (`I4:295`), worst case over 10,205 intervals summed into ~5.7e2 s | ≤ 5e-5 × 10205 / 570 ≈ **9.0e-4** |
| per-wave `total_body_time_s = round(…, 3)` (`I4:393`), 10 waves | ≤ 5e-4 × 10 / 570 ≈ **8.8e-6** |
| pinned `mean_occupancy = round(…, 4)` (`I6:266`) at 3.3519 | ≤ 5e-5 / 3.3519 ≈ **1.5e-5** |
| `obs_frac` 4-dp rounding | **0** — cancels identically in `ω`, § 3.2 |
| **worst-case total** | **≈ 9.2e-4** |

`TOL = 5.0e-3` is ~5.4× the worst-case rounding budget — enough headroom that a PASS is not luck,
tight enough that a genuine aggregation-rule error cannot hide inside it. It is **10× tighter** than
Lap AC's `F_AC_1_TOL = 0.05`. It is not adjustable after the number is seen; § 8 fixes what happens
instead.

### 4.3 Evaluability floor (pre-declared; failure ⇒ UNREACHED, not PASS)

The gate is evaluable only if **all** hold:
- all 10 waves 151–160 present in `I1 :: residence["293.6"].per_wave` — **10/10 required**;
- `Σ_w n_obs(w) ≥ 10000`;
- every `obs_frac(w) > 0` and every `T_ref(w) > 0`;
- the partition check of § 4.4 passes.

If any fails, `F-AD-1` is **UNREACHED** with the failing clause named. It is never a PASS by
default and never a FAIL by default.

### 4.4 Partition check (`R-PM4-75 part 3` operational form — binding)

The partition over I1 is assembled **from the artifact's own construction**, never from memory:

1. Enumerate every element of `residence["293.6"]["per_wave"]`. Each is assigned to exactly one of
   `{151, …, 160}` by its own `"wave"` key. **An element whose `wave` is not in that set, or that
   duplicates a wave already assigned, HALTs.**
2. Enumerate every **top-level key** of `residence["293.6"]` and assign each explicitly to one of:
   `USED-BY-THIS-LAP` / `DECLARED-UNUSED`. **Any key not explicitly assigned HALTs** — no default,
   no allow-list one-worder (`D-I28-1`'s class, three-in-three; this lap does not make it four).
3. Exhaustiveness is **verified, not assumed**: `Σ_w n_intervals(w)` must equal
   `residence["293.6"]["n_intervals"]`, and `Σ_w n_obs(w)` must equal `I1 :: n_observed_instants`.
   A shortfall means intervals or instants fall outside the 10 windows and the aggregation rule of
   § 3.2 loses its last equality; that is a **HALT** (§ 8(c)), not a tolerance question.

### 4.5 Secondary rungs — reported, never pooled

`F-AD-1` is **declared at `293.6`**. It is additionally computed at `285.7` and `300.0` (I2:27,
I2:29) and reported as the **bracket that it is** (`R-PM4-70`: brackets stay brackets). The verdict
of record is the primary rung's; the secondaries are corroboration and are labelled so. `R = 150.0`
is **not** in this set (§ 2.4).

---

## 5 — `Σ T_ref` vs THE FIGHT WINDOW (pre-declared as a TAUTOLOGY, not a confirmation)

The commission asks for a sanity declaration of `Σ_w T_ref(w)` against the fight window
`[683.0, 864.0]`, duration `181.0 s`, with any gap **declared, not smoothed**.

⚑ **Pre-declared before computing:** the gap will be **zero to rounding, and this is a tautology,
not evidence.** `I7:58` constructs `WAVE_END[w] = WAVE_START[w+1]` for `w < 160` and
`WAVE_END[160] = FIGHT_T1`, so the ten windows **telescope** across `[FIGHT_T0, FIGHT_T1]` by
construction: they are exhaustive, non-overlapping, and admit **no inter-wave dead time by
definition**. The 9 internal cuts are *partition boundaries*, not *events with duration*.

Therefore:
- A zero gap **confirms nothing about the referent** — it confirms that this lap read `I7:58`
  correctly. It is graded (`P-3`) as an arithmetic self-check only.
- A **non-zero** gap would mean an operand was mis-read or an artifact is inconsistent with its own
  construction — that is a **HALT**, not a finding about the game.
- ⚑ **What the run must NOT conclude:** that referent waves have no gap *in the world*. A wave-N
  clear and a wave-N+1 spawn may well be separated by real dead time; this segmentation cannot see
  it, because `OBS-H2-6` cuts at the **wave-counter digit change** and assigns every intervening
  second to one wave or the other. **Whether inter-wave dead time exists in the referent is
  `UNREACHED-AD-1`, pre-declared here**, with its obstacle named: the counter is the only pinned
  clock and it partitions rather than brackets. This matters to I-29 precisely because a sim `T`
  that *does* contain dead time would not be like-for-like with a referent `T` that structurally
  cannot.

---

## 6 — PREDICTIONS (graded wording-unchanged; blind ones marked ⚑)

| id | prediction | grading rule |
|---|---|---|
| `P-1` | `T_ref(w)` agrees with `T_direct(w)` (I2 `basis` transcription) to within **0.01 s** on all 10 waves. | PASS iff max abs difference ≤ 0.01 s |
| `P-2` | `T_ref(w)` is **identical to 4 dp across all four rungs** in I1 (150.0 / 285.7 / 293.6 / 300.0). | PASS iff all four rung vectors agree to 4 dp; FAIL ⇒ **HALT** per § 2.4 |
| `P-3` | `Σ_w T_ref(w) = 181.00 s ± 0.05 s`, and equals `FIGHT_T1 − FIGHT_T0` from I7. | PASS iff within band |
| `P-4` | `F-AD-1` **PASSES** at rung 293.6 within `TOL = 5.0e-3`. | PASS iff gate verdict is PASS |
| `P-5` | `F-AD-1` also passes at 285.7 and 300.0. | PASS iff both within `TOL` |
| `P-6` | The per-wave partition is **exhaustive**: `Σ_w n_intervals(w) == n_intervals` and `Σ_w n_obs(w) == n_observed_instants`, both exactly. | PASS iff both exact |
| `P-7` ⚑ | `L_naive_mean` (unweighted per-wave mean) **MISSES** the pinned bracket by more than `TOL`. | blind |
| `P-8` ⚑ | `L_walltime` (wall-duration weighted) **MISSES** the pinned bracket by more than `TOL`. | blind |
| `P-9` ⚑ | `max_w T_ref / min_w T_ref ≥ 2.0` — the wave windows are not near-uniform in length. | blind |
| `P-10` ⚑ | The wave with the **longest** window is **not** the wave with the highest `L_recon(w)`. | blind |

Predictions are graded in the findings with **wording unchanged from this file**. A FAIL is
reported as a FAIL and is informative; no prediction is retro-edited, softened, or dropped.

---

## 7 — DETERMINISM, DIGESTS, ORDER OF WORK

- **Determinism ×2:** the instrument runs twice into two separate output directories; **every**
  emitted artifact must be **byte-identical**, compared by sha256. A single mismatch is a defect
  and is reported as one.
- **`D-AA-5`:** all full-64 digests are computed **after** the final write of every artifact.
- ⚑ **`R-PM4-75 part 2` / `I-28 DO-NOT 8` — binding on this document too:** a truncated pin is a
  **LOCATOR**, not a digest. Every full-64 hex string published in this lap's findings is **re-hashed
  from the bytes on disk at the moment of writing**. No truncated pin appearing anywhere — in the
  charter, in a prior lap's prose, in my own memory of Lap AC — is ever expanded to 64 characters.
  If a value cannot be hashed, the truncation actually held is published as a truncation and
  labelled one. (`D-I28-3` is three days old; it is not repeated here.)
- **Order:** this prereg is committed **ALONE** → instrument + emitted artifacts committed →
  findings committed. Any self-caught defect gets an **addendum committed ALONE before its repair**.
- **No pinned instrument is modified.** Lap AC's and Lap R's scripts are read-only inputs; this lap
  writes a new script under `agentic_orchestration/research/scripts/`.

---

## 8 — HALT CONDITIONS AND PRE-WRITTEN LANDING SITES

Written **before** any number, so that no outcome is improvised.

**(a) Gate deviation in `(TOL, 5e-2]` — landing site `ROUNDING-DOMINATED NEAR-MISS`.**
Report the deviation, the § 4.2 budget, and the observation that the deviation exceeds the budget.
Verdict is **FAIL**. `TOL` is **not** widened. `T_ref` is published but flagged
`GATE-FAIL — NOT LICENSED FOR I-29 WITHOUT A CONDUCTOR RULING`, and `UNREACHED-AD-2` is opened:
*"exact closure blocked by published-precision loss; closable only by re-running Lap AC's residence
instrument at higher precision, which would modify a pinned lap and is refused."*

**(b) Gate deviation `> 5e-2` — landing site `AGGREGATION-RULE MISMATCH`.**
The § 3.2 rule then does not describe the pinned construction. Publish all four candidate
aggregations (`L_agg`, `L_naive_mean`, `L_walltime`, and `Σ B_A / (DT · N_obs)` computed directly)
with their deviations; verdict **FAIL**; **HALT to the conductor**; `T_ref` emitted marked
`UNGATED — DO NOT USE`. Under no circumstances is a fifth aggregation invented to make the number
land.

**(c) Partition non-exhaustive (§ 4.4.3) — HALT.** No repair attempted inside this lap; the
condition is unmodeled and belongs to the conductor.

**(d) Rung-invariance of `T_ref` fails (`P-2`) — HALT.** The artifact would not match its own
construction; nothing downstream of it is safe.

**(e) Any input digest mismatch — HALT** before a single byte of content is read.

**(f) `T_direct` unparseable from I2's `basis` column — NOT a HALT.** `P-1` is graded UNREACHED
with the obstacle named; the gate does not depend on `T_direct`.

**(g) Any condition not modeled above — HALT and report.** This lap improvises nothing.

---

## 9 — DO-NOT BLOCK CARRIED IN ADVANCE (all prior blocks, unchanged and cumulative)

Carried in force for this lap: **Lap V § 7.2 · Lap V-2 § 11.2 · Lap W § 7.2 · Lap X § 12.2 ·
Lap Y § 11.6 · Lap Z § 5 · Lap AA § 6 · Lap AB § 9 (all ten) · Lap AC § 9 (all nine) · I-28's
eight.** Named explicitly because they bind this lap's hands in specific places:

- **Lap AB DO-NOT 9** — `pm4u_arrivals.csv` is not opened, cited or derived from. It is not an input.
- **Lap AC DO-NOT 3** — no referent residence scalar is quoted. `B_A(w)` enters this lap **only** as
  the numerator of a ratio whose denominator is `T_ref(w)`, i.e. as the rung-A leg of a bracket, and
  the findings will say "rung A, LOWER bound" every time it appears.
- **Lap AC DO-NOT 4** — **no quantity in this lap is compared to any sim quantity.** `T_ref` is
  emitted as a pinned artifact for the conductor's I-29 commission. I place nothing side by side.
- **Lap AC DO-NOT 6** — every count here is a LOWER bound; plate absence never proves body absence.
- **Lap AC DO-NOT 7** — `R = 150.0` is never pooled (§ 2.4 states its single rung-free use).
- **Lap AC DO-NOT 8** — no ground-pixel quantity is converted to metres on a single anchor. The
  three-rung bracket governs. (This lap converts nothing; it deals in seconds.)
- **Lap AC DO-NOT 9** — no track count is used as a body count. This lap uses **no** body count at
  all; `N` is I-29's leg, not mine.
- **`R-PM4-72 part 4`** — `share_player` is not touched, quoted or reasoned about here.

New DO-NOTs this lap expects to add are **not** pre-written as findings; § 2.2's over-reading
hazard and § 5's dead-time hazard are flagged in advance so that the findings can state them as
carried, not discovered.

---

## 10 — FIREWALL (what this lap will not do, fixed in advance)

1. **No sim artifact, cell, ledger, output directory or code path is opened.** Referent side only.
2. **No comparison of any kind to any sim quantity**, in prose, in a table, or by adjacency.
3. **No re-derivation of the occupancy bracket.** The bracket is pinned and stays pinned; `F-AD-1`
   is a fidelity gate on `T_ref`, never a competing occupancy figure. (Lap AC § 4.7's clause,
   carried verbatim in intent.)
4. **No new segmentation.** The 9 cuts are `OBS-H2-6`'s; this lap re-expresses them, it does not
   re-measure them, and it does not adjudicate their ±0.25 s.
5. **No tuning of anything, whatever the arithmetic says.** No config, no frozen ensemble, no
   pinned instrument is touched.
6. **No designation by grade** — nothing here is called good, bad, better or worse.
7. **No metre conversion, no body count, no arrival rate, no residence scalar.**

---

*Prereg ends. Committed ALONE. The instrument may now be written.*
