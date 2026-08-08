# Gate-2 — KC2-SIM locomotion lap (§ 10.9a A–C) — 2026-08-08

**Reviewer:** jack-ryan (DEV-MODE, Gate 2, standing safety #2 of the KC2-SIM autonomous run)
**Conductor:** gandalf (RUN-CONDUCTOR)
**Developer:** gamora (simulation seam)
**Target:** engine `a5382e65` on `main` (UNPUSHED — left unpushed); meta `f98faa80`
**Lap deliverable:** `agentic_orchestration/gamora/notes/2026-08-08-kc2-locomotion-lap.md` (713 lines)
**Spec contract:** `agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` § 10.9a blocks A–G
**Mode:** read-only on engine repo. No code changes, no test changes, no commits, no push.

> ## ⚑ CORRIGENDA — 2026-08-08, later fold (jack-ryan; KC2-SIM ledger L-63, commission R-L65-3)
>
> **The verdict is UNCHANGED: PASS-with-findings.** Two findings moved after the developer's sitting
> returned. **Nothing below is rewritten** — corrigenda-forward, no silent self-healing, the same rule
> this review applied to others.
>
> - **F-1 — UPHELD AND EXTENDED. My hit table was short by three.** I priced 5 engine line-hits; the
>   correction closed at **8** (L-63(a)). The load-bearing omission is `tests/test_kc2_locomotion.py:567`,
>   a **second live pin** whose repair-omission would have left the test **RED on its third assertion
>   with the first two green**. The finding was right; my own sweep of it was not. See the annotation
>   at F-1.
> - **F-2 — WITHDRAWN BY EVIDENCE.** The `+77` decomposes exactly; my reconstruction was wrong, and it
>   was wrong by the method error I was auditing for. See the annotation at F-2. Severity was INFO, so
>   no verdict limb rests on it.
> - **F-3, F-4, N-1 — unchanged.** F-3's set claim got its roster on disk at the same sitting (full
>   census at `f06e2981`: 63 F / 10,354 P / 21 E, exact on all three; 12/12 failure files exact vs
>   L-39; zero novel).
> - **Consequence beyond this record:** F-1 was the **fifth recurrence** of the value-set-sweep class
>   and fired `desirable-run-pattern.md` § 6.5's pre-registered graduation trigger. With L-63(a) and
>   L-65(j) as sixth and seventh, the law landed as **Discipline #72** on 2026-08-08; the
>   derived-value half of my own miss landed as **#64**'s third basis instance.

## VERDICT: **PASS-with-findings**

**Four findings: 2 × WARN, 2 × INFO. Zero BLOCK.** The lap's binding claims — T-1's 8/65/19 FAIL
un-re-pinned, the p05 residual localisation, the empty K-region and the violated JC-7 consequence,
MO-5 at 9.7971 s under cited radii, the D2-2 replacement, and the three SHA pins — are **verified
against evidence, not summaries**, and every one of them reproduces. Several reproduce to the last
digit, and the MO-5 geometry sweep reproduces as a *single closed form* rather than four
transcriptions, which is the kind of internal consistency that cannot be faked by narration.

Nothing here blocks the fold. F-1 (the § 6.5 sweep hit table) is the one item the conductor should
price before folding, and it is a **work-class** correction, not a verdict correction.

**Approval authority (ADR-002):** this verdict is mine to issue — no cross-seam schema change, no new
ADR, no milestone tag, no conflict with a locked decisions-log entry. Nothing escalates to Matt.

> **Re-commission note.** A prior Gate-2 agent completed this review (~70 tool uses) and lost its
> entire verdict to a stream idle timeout, writing nothing. This file is written FILE-EARLY and
> APPENDED-AS-I-GO precisely so that failure mode cannot recur. Nothing of the prior run survived;
> this review starts from zero evidence.

---

## 0. Verification ledger (populated as checks complete)

| # | Check | Result |
|---|---|---|
| 1 | § 10.9a A–G contract coverage | **PASS** — A–F met, G 11/11 addressed, 10/11 head-on (**F-4 INFO**) |
| 2 | Headline numbers vs the lap's own tables | **PASS** — 22/22 reproduce; several exact to the last digit; § 0 / § 5 / § 6 / § 7 / § 8.1 mutually reconcile |
| 3 | Engine spot-checks (`P05_DRIP_CADENCE_S`, `t1_pooled_mean`, `emitter_radius_m`, KITE/TOUR, CAMP_THEN_COLLECT) | **PASS** — all five hold (**N-1** INFO note, no action) |
| 4 | Test count (41 claimed vs 39 raw `def test`) | **RESOLVED** — parametrize expansion, 39−1+3 = 41; collected 41, **41 passed in 13.34 s**. The lap's number is the true executed count |
| 5 | Census 63 FAIL / 10,354 PASS / 21 ERROR — zero novel failure files | **PASS-with-findings** — scalars + transient mechanism verified (72/72 re-run); roster not on disk (**F-3 WARN**); `+77` decomposition short by 2 (**F-2 INFO**) |
| 6 | SHA pins (3 CSVs) | **PASS** — 3/3 byte-exact, row counts exact, and pinned in-test |
| 7 | § 6.5 value-set sweep (`spawn_t_s`, `emitter_radius_m`, + hand-back completeness) | **PASS-with-findings** — renames CLEAN; s2 hand-back (a)+(b) **verified COMPLETE**; F-13 hand-back **INCOMPLETE by 5 line-hits** (**F-1 WARN**) |

### Findings index

| id | severity | one line |
|---|---|---|
| **F-1** | **WARN** | L-52 hand-back list incomplete — 5 further line-hits carry the superseded `289.62`, incl. a live constant and a test pin; the correction is code+test+re-run, not a note edit — **⚑ UPHELD; closed at 8, not 5 (L-63(a))** |
| **F-2** | INFO | `+77 passing` does not decompose; per-file reconstruction lands at `+75`. Binding claims unaffected — **⚑ WITHDRAWN BY EVIDENCE (L-63(c)): it decomposes exactly** |
| **F-3** | **WARN** | "zero novel failure files" is a set claim; the 13-file roster is on no disk. Remedy is near-free |
| **F-4** | INFO | § 10.9a G's *first-engagement times* answered with arrival times; immaterial under CAMP + declared-zero kill |
| N-1 | INFO | `emitter_radius_m` survives as a *method* on the cited-geometry object — spelling collision with the deleted scalar, not a live reference. No action |

---

## 1. Verified-clean checks (evidence)

### V-1 — SHA pins: 3/3 EXACT, row counts EXACT

Re-hashed the vendored copies under `reincarnated-engine/data/kc2/` myself. All three digests
reproduce the lap's § 1 pin block character-for-character, and `wc -l` confirms the row counts
(header + N data rows):

| file | lap-pinned SHA-256 | re-hashed | claimed rows | `wc -l` | data rows |
|---|---|---|---:|---:|---:|
| `kc2_crucible_emitter_geometry.csv` | `ece0c345…49cff9` | **MATCH** | 332 | 333 | **332** |
| `kc2_crucible_patrolpoints.csv` | `106facba…693747` | **MATCH** | 173 | 174 | **173** |
| `kc2_s1_banda_record_inputs.csv` | `ac50ef77…d777f657e` | **MATCH** | 895 | 896 | **895** |

The digests are additionally asserted **in-test** (`test_kc2_locomotion.py` :42–52, parametrized over
all three), so a silent re-vendor goes red. Discipline #8 (schema validation at boundaries) satisfied
at the strongest available grade — provenance rides on the value, not in a comment.

### V-2 — Test count: the 41/39 discrepancy is PARAMETRIZE EXPANSION, not an inflated claim

Raw `def test` count in `tests/test_kc2_locomotion.py` is **39** — the commission's number is right.
The gap resolves at line 42: one `@pytest.mark.parametrize("name,sha", [...])` carrying **three**
entries (the three cited CSVs) expands one definition into three node IDs. 39 − 1 + 3 = **41**.

Collected and executed, not inferred:

```
python3 -m pytest tests/test_kc2_locomotion.py --collect-only -q  →  41 tests collected
python3 -m pytest tests/test_kc2_locomotion.py -q                 →  41 passed in 13.34s
```

**The lap's "41 tests" is the true executed count.** No finding.

### V-3 — Engine spot-checks: 5/5 hold

| claim | evidence | verdict |
|---|---|---|
| `P05_DRIP_CADENCE_S` exists **and is consumed** | defined `wave_engine.py:492` (`= 3.0`); consumed `wave_engine.py:588` as the default of the overridable `cadence`; read by `calibration.py:1023/1032/1064` for the sensitivity/provenance blocks; pinned `test_kc2_locomotion.py:686` (`== 3.0`) | **HOLDS** — genuinely load-bearing, not a decorative constant |
| `t1_pooled_mean` **refuses** pooling | `calibration.py:509` — body is a bare `raise ValueError` naming § 12 T-1 and redirecting to `t1_two_class_rollup()`; negative-control test at `test_kc2_s1_ramp.py:179` | **HOLDS** — the prohibition is executable, not a comment |
| `Arena.emitter_radius_m` **deleted**, no live references | no attribute anywhere; regression guard `test_kc2_opposition_wave_engine.py:826` asserts `not hasattr(we.ARENA_S1, "emitter_radius_m")`. Surviving hits are all deliberate: MIGRATION/AGENT_STATE/math-note prose, and star-lord's `baton_v1_validator.py:49–52,700–702` which pins `30.0` as a **retired-value tripwire** | **HOLDS** — see N-1 below for the one nuance worth naming |
| `KITE` / `TOUR` **raise** | `locomotion.py:150/151` declare them NOT IMPLEMENTED; `closing_to_v_ref` raises `NotImplementedError` on KITE (`:565–566`) and on TOUR (`:567`); `run.py:268–271` rejects any policy outside `{CAMP, CAMP_THEN_COLLECT}` at the entry point | **HOLDS** — refused at both the conversion and the simulation entry |
| `CAMP_THEN_COLLECT` **implemented** | `locomotion.py:148` enum member; `run.py:216` is the **default**; the collect branch fires at `run.py:395` gated on `all(...)` actors off-board | **HOLDS** |

### V-4 — § 6.5 value-set sweep on the two renames: CLEAN

- `arrive_t_s` — every surviving hit is either MIGRATION/AGENT_STATE/math-note prose **declaring** the
  rename, or the deliberate one-lap deprecated alias at `run.py:335` plus its self-describing sibling
  `arrive_t_s_deprecated` at `:336`. That is the declared behaviour in MIGRATION.md :22–30, :57.
  **No stale consumer.**
- `player_spawn_xy` → `player_camp_xy` and `emitter_bearings_oclock` → `footage_bearings_oclock` —
  both swept; surviving hits are MIGRATION prose, the `wave_engine.py:556` rationale comment, and the
  `test_kc2_opposition_wave_engine.py:825` `not hasattr` regression guard. **No stale consumer.**

**N-1 (INFO, no action).** `emitter_radius_m` survives as a *method name* on the cited-geometry object
(`locomotion.py:269`, `CitedGeometry.emitter_radius_m(spawn_point, tier)`), delegated by
`wave_engine.py:549 Arena.emitter_radius_of(...)`. This is a different object with a different arity
and is not the deleted scalar — the deletion claim is about `Arena.emitter_radius_m` the attribute,
and that is genuinely gone. Recording it only because the spelling collision means a future
grep-based sweep for the retired float will hit a live symbol. Not a finding.

### V-5 — Headline arithmetic: EVERY figure reproduces, several to the last digit

Recomputed independently rather than read back. Nothing in the lap's § 0 headline disagrees with the
lap's own tables, and the tables agree with each other.

| claim | lap value | my recomputation | verdict |
|---|---|---|---|
| K-1 `(38.45−4.0)/4.3` | ≥ 8.0116 | 8.011627906… | **EXACT** |
| K-2 `(10.17−4.0)/6.1` | ≥ 1.0115 | 1.011475409… | **EXACT** |
| K-3 `33.53/(7.0−0.5)` | ≤ 5.1585 | 5.158461538… | **EXACT** |
| A required `7.0 − 33.53/8.0116` | ≳ 2.8148 | 2.814833091… | **EXACT** (spec's pre-registered "≳ 2.81" confirmed to 4 fig.) |
| consequence violated by | 2.3148 | 2.314833091… | **EXACT** |
| ring:ambush ratio `38.45/10.17` | > 3.5× ("3.7×") | 3.7807 | **HOLDS** (test asserts > 3.5×) |
| T-1 split sums to 92 | 8 + 65 + 19 | 92 | **EXACT** (beat 3: 0+89+3 = 92) |
| mean Δ from the localisation split | +4.207 | (59·0.204 + 33·11.363)/92 = **4.20668** | **RECONCILES** — § 0 and § 6 are the same measurement |
| non-p05 Δ `15.659 − 15.455` | +0.204 | 0.204 | **EXACT** |
| p05 Δ `27.471 − 16.108` | +11.363 | 11.363 | **EXACT** |
| fixture p05 slower `16.108 − 15.455` | 0.653 | 0.653 | **EXACT** |
| drip schedule `3.0 × (7.249 − 1)` | 18.747 | 18.747 | **EXACT** |
| ×10 ratio measured `28.57/14.29` | 2.00× | 1.99930 | **EXACT** |
| ×10 ratio sim `18.17/20.08` | 0.905× | 0.904880 | **EXACT** |
| MO-5 margin `(9.7971−7)/7` | +39.96 % | 39.9586 % | **EXACT** |
| MO-5 retired margin `(7.75−7)/7` | +10.71 % | 10.7143 % | **EXACT** |
| cited ring median of `[34.196, 42.181]` | 38.1885 | 38.1885 | **EXACT** |
| MO-5 geometry sweep internal law | 4 radii → 4 times | implied slope **0.24999695 s/m ⇒ v = 4.00005 m/s**; predicts 7.7045 and 11.30775 vs claimed 7.7045 / 11.3078 | **EXACT** — the four rows are one consistent closed form at `V_REF = 4.0`, not four transcriptions |
| D2-2 zero crossing (linear 6.0→8.0) | ≈ 6.9 m/s | 6.8906 | **EXACT** |
| composition ratio `175.434/18.381` | 9.544× | 9.54431 | **EXACT** |
| § 7 `last_arrival_mean` vs § 6/§ 8.1 | 18.381 | (59·14.5 + 33·25.293)/92 ≈ 18.37 | **RECONCILES to ~0.01 s** across three independently reported sections |
| census pass delta `10,354 − 10,277` | +77 | 77 | arithmetic **EXACT** (decomposition: see F-2) |
| D2-2 `r` range across the 5.25× sweep | +0.429 … +0.522 | table rows span +0.4292 … +0.5217 | **HOLDS** — flat, as claimed |
| cadence sweep: p05 Δ +11.36 → +0.19, non-p05 holds | 3.0/1.5/0.0 s | non-p05 column reads 0.204 / 0.204 / 0.204 | **HOLDS** — invariance to 3 d.p. is real, and it is what converts the localisation from a coincidence of means into an address |

### V-6 — § 10.9a B "recomputed from the bytes, never transcribed": INDEPENDENTLY REPRODUCED, 8/8

The lap's strongest single claim (Discipline #11) is that every § 10.9a B figure was recomputed from
the CSV rather than copied out of the spec. I recomputed all of them myself from
`data/kc2/kc2_s1_banda_record_inputs.csv`:

| figure | lap | my recomputation |
|---|---|---|
| `characterRunSpeed` n / median / mean / range | 895 / 1.000 / 1.0358 / 0.60–2.00 | 895 / 1.0000 / 1.0358 / 0.60–2.00 |
| `characterRunSpeed` = 1.0 / below / above | 191 / 311 / 393 | 191 / 311 / 393 |
| `ViewDistance` 80.0 | 868 | 868 |
| `MaxPursuitDistance` 125.0 | 868 | 868 |
| `PursuitTime` 10 000 ms / 12 000 ms | 890 / 5 | 890 / 5 |
| `disableMovement` absent | 895/895 | 895/895 |
| jitter n / median (and mean / max) | 810 / 15.0 (12.21 / 50.0) | 810 / 15.0 (12.2111 / 50.0) |
| `walkDistance` n / median | 677 / 4.5 | 677 / 4.5 |

**8/8 exact.** Additionally:

- **F-L1's 27/895 `ViewDistance = 15.0`** — reproduced: the counter is exactly `{80.0: 868, 15.0: 27}`,
  a clean two-valued column. **The finding's premise is measured, not asserted.**
- **F-L7's 895/896 join** — reproduced: 895 distinct `record` values, and
  `records/creatures/enemies/hero/scavenger_h075.dbr` is **genuinely absent** from the emission.
  The declared modal fallback (`characterRunSpeed` 1.000) is also the band's true median **and** mode
  per the row above, so the fallback is the least-assuming one available.

### V-7 — Census: the binding claim's *mechanism* is verified, the *set* is not on disk (see F-3)

- **Commit-message framing is honest.** `a5382e65`'s message reports the **pre-commit** census
  (64 / 10,353 / 21) and explicitly says *"post-commit census re-run reported in the lap note."* A
  commit message cannot carry its own post-commit census; the lap does not pretend otherwise, and the
  64-vs-63 difference between message and note is this ordering, not a contradiction. **No finding.**
- **The single transient is verified resolved, byte-for-byte.** The lap claims
  `pytest tests/test_kc2_locomotion.py tests/test_kitcal_g5_harness.py` → *"the same pair passes
  72/72 after the commit."* I ran exactly that pair: **72 passed in 13.32 s.** The claimed count is
  the observed count. The F-11 untracked-but-loaded-source attribution is therefore a measurement,
  not an inference — and reporting the dirty pre-commit run beside the clean binding one is
  Discipline #12 (framing, not burying) executed at cost to the author.

---

## 2. Findings

Three findings, all sub-BLOCK. Severity vocabulary per REVIEW_PROCESS.md.

---

### F-1 — **WARN** — § 6.5 value-set sweep: the L-52 hand-back list is **INCOMPLETE**. Five line-hits across three engine files carry the superseded `289.62` F-13 re-grade, and one is a **live constant** with a **test pin**.

**Description (what exists).** L-52(e) re-derived the F-13 measured floor: `271.50 + 10.00 (w152)
+ 4.50 (w153: 22 − 17.50) + 2.62 (w157)` = **288.62**, superseding 289.62 (the w153 strike of the
16 368 green readout removes one body). Perturbation scale therefore corrects
`+6.674 %` → `+6.306 %` — I recomputed both: `(289.62−271.50)/271.50 = 6.67403 %`,
`(288.62−271.50)/271.50 = 6.30571 %`.

The conductor's L-52(j) sweep discharged this as **"HAND-BACK ×2, gamora seam"**, naming exactly two
surfaces: `gamora/notes/2026-08-08-kc2-locomotion-lap.md:427` and engine
`src/reincarnated/simulation/AGENT_STATE.md:25`. Both confirmed present and stale. **Beyond those
two, the superseded value survives at five further line-hits in three files:**

| # | surface | line | kind | owner |
|---|---|---:|---|---|
| 1 | `reincarnated-engine/src/reincarnated/simulation/kc2/calibration.py` | 935–937 | comment — *"271.50 (record) → 289.62 (measured floor) … +6.68 %"* | gamora |
| 2 | `reincarnated-engine/src/reincarnated/simulation/kc2/calibration.py` | **938** | **LIVE CONSTANT** — `F13_MEASURED_FLOOR_REGULARS: float = 289.62` | gamora |
| 3 | `reincarnated-engine/tests/test_kc2_locomotion.py` | 563 | docstring — *"(271.50 → 289.62 = +6.67 %)"* | gamora |
| 4 | `reincarnated-engine/tests/test_kc2_locomotion.py` | **565** | **TEST PIN** — `assert cal.F13_MEASURED_FLOOR_REGULARS == 289.62` | gamora |
| 5 | `reincarnated-engine/src/reincarnated/simulation/math/kc2-locomotion-lap-2026-08-08.md` | 369 | *"271.50 (record) → 289.62 (measured floor) … +6.68 %"* | gamora |

Hit 2 is not decorative. `calibration.py:940` derives
`F13_N_PERTURBATION = F13_MEASURED_FLOOR_REGULARS / F13_MODEL_OF_RECORD_REGULARS` = **1.06674**, and
`n_sensitivity()` consumes it as `scales = [1.0, F13_N_PERTURBATION, 2.0 − F13_N_PERTURBATION]` —
i.e. the executed sweep ran at **1.0667 / 0.9333**, which is precisely the `n_scale` column the lap
tabulates at § 8.4. Under the corrected floor the sweep runs at **1.0631 / 0.9369**.

**Prescription (separate from the above).** The load-bearing part of this finding is not the stale
digit — the conductor already graded that *"direction favorable, magnitude small,"* and I agree: the
lap's binding results (T-1 8/65/19, the p05 localisation, the empty K-region, MO-5, D2-2) are all
**untouched** by the perturbation scale, and § 8.4's qualitative verdict (*"the result inherits the
F-13 residual"*) survives any plausible re-run. **The load-bearing part is the WORK CLASS.** The
hand-back's disposition — *"ADJUDICATE AT THE LAP FOLD (an in-flight seam note is not mine to
edit)"* — is scoped as a **note edit**. It is not. Correcting it requires (a) a live-constant edit,
(b) a test-assertion edit that will otherwise go **red on the correction**, (c) two docstring edits
and a math-note edit, and (d) **a re-run of `n_sensitivity()`** to restate § 8.4's three-row table.
That is a code + test + re-execute item, not prose.

The test pin at hit 4 is, to be clear, **good design** — it is the tripwire working exactly as
intended, refusing to let the constant move silently. It is named here because it converts the
correction from free to costed, and the conductor should price it before the fold.

- **Cite:** desirable-run-pattern § 6.5 / gandalf OP § 4.11 (value-set sweep on consuming surfaces);
  Discipline #8 (schema/boundary validation); Discipline #12 (semantic shifts framed, not buried).
- **Action — gamora:** correct `F13_MEASURED_FLOOR_REGULARS` 289.62 → 288.62 across hits 1–5,
  re-run `n_sensitivity()`, restate § 8.4's table with the corrected `+6.31 %` scale. **Or**
  explicitly DEFER with the stale value NAMED as stale *in code* (a `SUPERSEDED_AT_L52` sibling), so
  the next reader does not re-derive from it.
- **Action — conductor:** re-grade the L-52(j) hand-back disposition from *note-edit-at-fold* to
  *code + test + re-run*, or rule the deferral.
- **Not a BLOCK because:** no lap conclusion turns on it, the direction is favorable, and the
  conductor had already registered the class of the error before I arrived. This finding extends the
  hit list; it does not overturn the disposition.

> ### ⚑ ANNOTATION — F-1 COMPLETION, 2026-08-08 later fold (jack-ryan; ledger L-63(a), engine `f06e2981`)
>
> **The finding is UPHELD. The hit table above is INCOMPLETE — I priced 5; it closed at 8.** The three
> beyond my list, verified by me at this fold rather than taken from the developer's report:
>
> | # | surface | line | kind | why my sweep missed it |
> |---|---|---:|---|---|
> | 6 | `tests/test_kc2_locomotion.py` | **567** | **SECOND LIVE PIN** — `assert cal.F13_N_PERTURBATION == pytest.approx(1.0667, abs=1e-3)` | the value is **derived**, not a spelling of `289.62` |
> | 7 | `src/reincarnated/simulation/math/kc2-locomotion-lap-2026-08-08.md` | 370 | prose ±6.68 % | second line of a two-line pair; I tabulated :369 |
> | 8 | `src/reincarnated/simulation/AGENT_STATE.md` | 25 | queued at L-52(j)/L-54(f), never discharged | already on the conductor's hand-back list; I recorded it as *confirmed present and stale* and did not carry it into my own table |
>
> **Hit 6 is the load-bearing one, and it is the one that indicts my method.** In the pre-correction
> file (`git show a5382e65:tests/test_kc2_locomotion.py`) the pins sit in one three-assertion block:
> `:565` the floor constant — **which I tabulated as hit 4** — `:566` the unchanged operand `271.50`,
> benign, and `:567` the derived perturbation. `|1.0667 − 288.62/271.50| = |1.0667 − 1.063057| =
> **0.0036 > 1e-3**`, so **the five-site repair I prescribed would have left this test RED on its
> third assertion with the first two green.**
>
> **The mechanism is not ignorance — which is worse, and is why it graduated a law.** The F-1 body
> above *names the derived pair explicitly*: "*the executed sweep ran at 1.0667 / 0.9333 … under the
> corrected floor the sweep runs at 1.0631 / 0.9369.*" I traced the derivation, printed both values,
> and never added `1.0667` to the grep set. The sweep enumerated the changed value's **spellings**;
> a value **derived from** it is not a spelling of it. That half of the miss is governed by
> **Discipline #64**'s BASIS FORM propagation clause — *binding since 2026-07-31, eight days before
> this review* — and now lands there as its **third founding instance**. The other half — that the
> residual enumeration was **by eye** in a file I was already reading — became **Discipline #72**
> clause 5, founding instance 6.
>
> **The prescription's substance held, and the developer took both limbs of it, not either.** I
> offered *"correct across hits 1–5 … **or** explicitly DEFER with the stale value NAMED as stale in
> code (a `SUPERSEDED_AT_L52` sibling)."* The sitting did **both**: the constant now reads `288.62`,
> and `F13_MEASURED_FLOOR_REGULARS_SUPERSEDED_AT_L52 = 289.62` exists with a test asserting the
> retirement (`calibration.py:950`/`:969`, `test_kc2_locomotion.py:576`). Re-grepped by me at this
> fold: **four `289.62` sites survive in the engine tree and all four are corrigenda or
> retired-value assertions — zero live consumers.** The recomputation reproduces mine exactly
> (`(288.62 − 271.50)/271.50 = 6.30571 %`), and the § 8.4 rows were deliberately **not** restated —
> they are true measurements at the scale named beside them, and the corrected scale lies *inside*
> the executed one, so the published envelope is conservative. That is the right call and it is
> **#12** done properly.
>
> **The work-class limb of the finding is confirmed by outcome.** I argued the L-52(j) disposition
> was mispriced as *"a note edit."* It was a live-constant edit + two test-pin edits + two docstring
> edits + a math-note edit + a state-file edit, held back from a re-run on an explicit and reasoned
> deferral. That limb is now **#72** clause 8.

**Affirmative counterpart — the other two hand-back surfaces are COMPLETE.** I swept
`survivalworld_a` across all engine `.py`/`.md` independently. The stale
`sm_mod/survivalworld_a` declaration appears at exactly the two named places —
`calibration.py:342` and math note § B.3 (:107) — and nowhere else. Every other hit is correct:
`locomotion.py:177` carries the executed truth `("survivalworld_a.map", "sm1")`;
`locomotion.py:181` uses `sm_mod/survivalworld_a` **correctly**, in the clause explaining why that
archive *cannot* express tier 16; `calibration.py:1215` (runtime) and `:1113` are right; the lap
note's own § 9 says `sm1/survivalworld_a.map` — **correct**. Hand-back (a)+(b) verified COMPLETE;
no extension needed there.

---

### F-2 — **INFO** — the "+77 passing" parenthetical does not decompose; my reconstruction lands at **+75**.

**Description.** § 11.1 states *"+77 passing (41 new locomotion tests, the rewritten beat-3 tests,
and star-lord's baton additions that landed underneath me)"*. The arithmetic `10,354 − 10,277 = 77`
is exact. The attribution is not itemised, and my per-file reconstruction across
`13451fdf → a5382e65` is two short:

| file | at `13451fdf` | at `a5382e65` | Δ | attributable to |
|---|---:|---:|---:|---|
| `tests/test_baton_v1.py` | 49 | 82 | **+33** | star-lord `28b578fe` |
| `tests/test_kc2_locomotion.py` | 0 | 41 *(collected)* | **+41** | this commit |
| `tests/test_kc2_micro_oracles.py` | 27 | 28 | **+1** | this commit |
| `tests/test_kc2_s1_ramp.py` | 26 | 26 | 0 | rewritten in place |
| `tests/test_kc2_opposition_wave_engine.py` | 44 | 44 | 0 | rewritten in place |
| | | | **+75** | |

`git diff --stat 13451fdf a5382e65 -- tests/` shows these five files and no others; drax's
`265069b1` touched no test file; and `parametrize` count is 0 → 0 in all four non-locomotion files,
so there is no hidden expansion there. Residual: **2 tests**.

**Prescription.** No action required of the developer. The `+77` is a descriptive parenthetical, and
the **binding** census claims — 63 = 63 failures, 21 = 21 errors, zero novel failure files — are
separately verified and do not depend on it. Most likely causes are a baseline re-reproduction taken
at a marginally different tree state or dynamic collection; neither is worth a census re-run to
settle. Recorded so the `+77` is not carried forward as an established decomposition.

- **Cite:** Review Principle #2 (smoke-gate — the gate claim is the failure/error equality, not the
  pass delta); Discipline #9 (attribution clarity).

> ### ⚑ ANNOTATION — F-2 **WITHDRAWN BY EVIDENCE**, 2026-08-08 later fold (jack-ryan; ledger L-63(c))
>
> **F-2 is withdrawn. The `+77` decomposes EXACTLY, and my reconstruction was the thing that was
> wrong.** The finding text above stands unedited; this annotation is its disposition.
>
> | file | Δ | note |
> |---|---:|---|
> | `tests/test_baton_v1.py` | **+35** | **51 → 86 collected**, not the 49 → 82 `def test` count in my table |
> | `tests/test_kc2_locomotion.py` | +41 | as I had it |
> | `tests/test_kc2_micro_oracles.py` | +1 | as I had it |
> | | **+77** | **exact** |
>
> The residual-2 was mine: `test_r_loco_1_arena_ref_guard_has_teeth` expands **1 `def` → 3 node IDs**.
> star-lord had independently published 51 → 86 before this review ran.
>
> **The error is worth naming precisely, because it is the failure mode this very review was
> auditing.** My table applied **collected-node counting** to the locomotion file and **`def test`
> counting** to the baton file — two methods in one column, silently — and then asserted the gap
> closed: *"`parametrize` count is 0 → 0 in all four non-locomotion files, so there is no hidden
> expansion there."* **That assertion is false**, and it is a **discharge-by-assertion** — exactly
> what § 6.5's fourth clause exists to forbid, committed by the reviewer citing § 6.5 two findings
> earlier. A mechanical `--collect-only` on both trees would have closed it in one command; I
> reasoned about the counts instead of collecting them. **Discipline #65** already owns the
> prescription (*reconcile `+passed` against the collected count*, not against a `def` count), and
> **#72** clause 5 now owns the enumeration half.
>
> **Nothing in the verdict moves.** F-2 was INFO, the finding itself said *"no action required of the
> developer"*, and the binding census claims (63 = 63 failures, 21 = 21 errors, zero novel failure
> files) were separately verified and never depended on the pass delta. The prescription's last line
> — *"recorded so the `+77` is not carried forward as an established decomposition"* — is now
> discharged in the opposite direction: **it IS established, and this is the decomposition.**

---

### F-3 — **WARN** — "ZERO NOVEL FAILURE FILES" is a **set** claim, and the set is not on disk anywhere.

**Description.** § 11.1 reports failure-**file** counts — 13 (L-39 baseline) / 14 (pre-commit) /
13 (post-commit) — and states the comparison was made *"per file."* The roster of those 13 files is
not printed in the lap note, in `src/reincarnated/simulation/AGENT_STATE.md`, or in
`src/reincarnated/simulation/math/kc2-locomotion-lap-2026-08-08.md` — I grepped all three. The
supporting evidence that **is** on disk is strong and I verified the load-bearing piece of it: exact
equality on both scalars (63 = 63, 21 = 21), one novel file **named**, its mechanism attributed to
F-11, its resolution reproduced deterministically, and the 72/72 pair re-run confirmed by me at the
shipping tree.

**Prescription.** This is the single gate-bearing claim in the lap that a reviewer cannot re-check
from what is on disk without a ~21-minute full-census re-run — which is outside my commission and
which I did not perform. Count equality on 63/21 with a swap hidden inside it is unlikely, but
"unlikely" is not the Gate-2 standard; **evidence, not summaries** is. The remedy is nearly free and
should be a standing habit rather than a one-off correction: **print the 13-file roster** (a
`--tb=no -q | grep` tail is seconds of work, and it is the artifact that makes the per-file
comparison auditable by someone other than its author).

I am explicitly **not** blocking on this. The lap's census discipline is otherwise exemplary — three
runs, per-file comparison stated, the dirty run reported beside the clean one, the binding run named
as the one that ships.

- **Cite:** Review Principle #2 (smoke-gate); Discipline #2 (smoke-test vs full-regen discipline);
  Discipline #10 (empirical inspection over assumption).
- **Action — gamora:** emit the failure-file roster alongside the scalars on the next census, here
  and as standing practice.

---

### F-4 — **INFO** — § 10.9a G's *"first-engagement times"* is reported as **arrival**, not engagement.

**Description.** § 10.9a G's report list opens *"arrival times by emitter · first-engagement
times."* The lap's § 8.1 tabulates first/last **arrival** by emitter class (ring 6.267 / 14.501;
ambush 6.141 / 25.293). `engage_t_s` is genuinely instrumented and defined — `run.py:383–384` sets
it on the first tick with `‖x_a − player‖ ≤ d_engage (2.4 m)`, `locomotion.py:614` carries the
field, and the math note :317 states the DB definition — but no engagement-time **summary** is
tabulated in the deliverable.

**Prescription.** Immaterial to this lap's results: under the declared CAMP policy with a
declared-zero kill term, contact and engagement are separated only by the `d_engage` shell, so the
engagement table would be a near-constant offset from the arrival table. Naming it because § 10.9a G
is a checklist the conductor reads for completeness, and this is the one row of eleven that is
answered adjacently rather than directly. Ten of eleven are answered head-on (see § 3 below).

- **Cite:** spec § 10.9a G.

---

## 3. § 10.9a A–G contract coverage — 11/11 reporting items addressed, 10/11 head-on

Blocks A–C are what the lap **builds**; D–F are procedure it **executes**; G is the reporting
contract. Mapping the deliverable against the spec (`…-kc2-sim-battle-spec.md` :1481–1994):

| block | spec requires | lap | grade |
|---|---|---|---|
| **A** | the motion model, stated as rules | § 1 — carries the equation verbatim incl. `x_a(t+dt) = x_a(t) + v(a)·dt·unit(target − x_a)`, planar/open-plane, both limbs L-A/L-B, and the disc hit-testing **current** positions | **MET** |
| **B** | every term with its citation; free surface = ONE scalar | § 1 + the three SHA pins + the 8/8 byte-recomputation I reproduced at V-6 | **MET, at the strongest available grade** |
| **C** | declared unmodelled inputs, NAMED as lap inputs | § 13 — seven-row table with each omission's extent **and sign**; `distressCall` re-graded unsigned → **measured SIGNED** (F-L1) | **MET, and exceeded** — one row was upgraded from declaration to measurement |
| **D** | `v_ref` bracket K-1…K-3, and where the declared value sits | § 3.2/3.3/3.5 — region EMPTY under every `d_engage` reading; calibration HALTED by rule; JC-7 consequence pre-registered then **reported violated** | **MET** |
| **E** | composition law RE-ESTABLISHED, never inherited | § 5.3 (sign argument re-derived, F-12's 89/92 retired as a live argument) + § 7 (law measured, **and its degeneracy declared unmeasurable** rather than papered) | **MET** |
| **F** | calibration procedure incl. N-sensitivity, second geometry, exclusions | § 8.4 (F.4) · § 9 (F.5) · § 10 (D2-2 negative control) | **MET** — modulo F-1's perturbation scale |
| **G** | eleven report items | see below | **11/11 addressed** |

§ 10.9a G item-by-item: arrival times by emitter → § 8.1 ✓ · **first-engagement times → § 8.1
reports arrival (F-4)** · composition law measured → § 7 ✓ · clear time vs T-1 UNCHANGED → § 5 ✓ ·
`r(clear, N)` vs the fixture's +0.154 → § 5.1 (+0.5151 sim vs +0.1537 fixture) ✓ · K-region and where
`v_ref` sits → § 3.2–3.5 ✓ · L-A vs L-B delta → § 8.3 ✓ · N-sensitivity → § 8.4 ✓ · MO-5 under cited
radii → § 4 ✓ · the three excluded waves **by name with their simulated results** → § 9 (w152/w153/
w157, each with sim mean/min/max and the exclusion column) ✓ · every C-row omission restated as an
omission → § 13 ✓.

**R-LOCO-1 (§ 10.9a G's routed schema gap) was closed in parallel by star-lord `28b578fe` +
drax `265069b1`, not by this lap.** The lap's § 12 F-L10 records this correctly, including that it
touched no `export/`, which I confirmed: `git diff --stat 13451fdf 265069b1` shows the three
`export/` files and `test_baton_v1.py` as star-lord's, and `a5382e65`'s tests touch none of them.
The scope claim at § 14 holds.

---

## 4. What I did not do

- **Did not run the full census** (~21 min) — outside commission scope; F-3 grades the evidence
  rather than regenerating it.
- **Did not run any simulation** — all engine execution was the two fast test invocations named
  above (41 tests / 13.34 s; 72 tests / 13.32 s).
- **Did not modify the engine repo** — no code, no tests, no commits, in any repo. `a5382e65`
  remains **UNPUSHED**, untouched.
- **Did not re-litigate R-L54-1 / R-L54-2 / R-L54-3.** These are the conductor's, recorded
  veto-open. I found **no ruling-evidence mismatch** against them: CAMP_THEN_COLLECT is implemented
  as ruled and defaulted (`run.py:216`); the memory-timer `PursuitTime` reading is the one built,
  with the lifetime-budget limb kept runnable (`pursuit_time_is_lifetime_budget=True`) and its
  30.4 % cost asserted by test, exactly as F-L2 claims; and the F-L6-forced `sm1/survivalworld_a`
  s2 execution is what `locomotion.py:177` actually carries, with the two stale contrary
  declarations already on the conductor's hand-back list (verified complete — see F-1's affirmative
  counterpart).

---

## 5. Standing-safety observations for the conductor (not findings)

Recorded because standing safety #2 is asked to watch for re-pinning and for gates being softened to
pass. **Neither happened, and the places where they were available are worth naming:**

1. **T-1 was the obvious re-pin target and was not touched.** 8/92 in-band is still a FAIL. The lap
   states it, keeps `t1_pooled_mean()` raising, and preserves the beat-3 92/92 verdict as `BEAT3_*`
   constants **in the same file** as the amended figures. Keeping the superseded number beside the
   corrected one is the discipline that makes a correction auditable rather than merely asserted.
2. **The p05 cadence was the available fitting move and was refused.** § 6's sweep shows 0.0 s takes
   the mean delta to +0.199 s and in-band to 13/92 — a visibly "better" result one constant away.
   The lap ships 3.0 s, pins it by test, and routes it as a finding. That is a MEASURED gate not
   being closed with an UNMEASURED term, which is the correct call.
3. **`v_ref` calibration halted rather than solved.** The K-region is empty; the lap did not fall
   back to fitting against T-1 residuals, and I confirmed there is no code path that could
   (`k_bracket()` takes `A` as an input). The mutual-closure reading 3.4092 is reported as
   policy-conditional and explicitly **not earned**.
4. **A was declared before the consequence was checked, and the consequence came back violated and
   was published.** Pre-registration that survives an unfavourable result is the whole point of
   pre-registration.
5. **JC-G7 named a fifth candidate that would close the 2.31 s gap and declined to adopt it.**
   Folding the § 10.9a C latency reservoir into `A` would have dissolved the violation; the lap
   names it as fitting-by-another-route and leaves it. Correct.
6. **The unfavourable census run was published beside the clean one.** Reporting the 64/14 pre-commit
   state, attributing it, and reproducing it deterministically cost the author something and bought
   the reader an auditable mechanism.
7. **F-L8 argues against a ruling that favoured the lap's own default.** L-46(a)'s stated
   justification for L-A is measured unsupported (limbs differ by 0.005 in `r`), and the lap says so
   while leaving the ruled default standing. Reporting evidence against your own conductor's stated
   reasoning is the behaviour this gate exists to protect.

**One framing note, no action.** The lap's closing line reads *"This note is UNCOMMITTED — the
conductor folds it."* That was true at authorship; it is now folded at meta `f98faa80`. The line
describes the state at writing and is not a stale claim.

---

## 6. Disposition

- **PASS-with-findings.** Fold may proceed.
- **F-1** → conductor prices the correction (code + test + re-run) or rules the deferral, with the
  stale value named as stale in-code if deferred.
- **F-3** → gamora, standing practice: emit the failure-file roster with the census scalars.
- **F-2, F-4, N-1** → record only.
- **Nothing escalates to Matt.** No cross-seam schema change, no new ADR, no milestone tag, no
  decisions-log conflict (ADR-002 tiered approval).
- **Engine `a5382e65` left UNPUSHED and unmodified.** No commits made by this review in any repo.

**Reviewer:** jack-ryan · Gate 2 · 2026-08-08

---

> ### ⚑ DISPOSITION ANNOTATION — 2026-08-08, later fold (jack-ryan; commission R-L65-3)
>
> **Verdict UNCHANGED (PASS-with-findings). All four findings + N-1 now CLOSED.**
>
> | id | disposition |
> |---|---|
> | **F-1** | **UPHELD, closed in code at 8 lines** (I priced 5). engine `f06e2981`. Both prescribed limbs taken — value corrected *and* retired value asserted-as-retired. Re-verified by me: zero live `289.62` consumers remain. |
> | **F-2** | **WITHDRAWN BY EVIDENCE.** `+77` decomposes exactly (35 + 41 + 1); my reconstruction mixed two counting methods in one table. |
> | **F-3** | **CLOSED.** Full census at `f06e2981` — 63 F / 10,354 P / 21 E exact on all three; 12/12 failure files exact vs L-39; **zero novel**. The set claim now has its roster on disk. |
> | **F-4 / N-1** | unchanged (record only). |
>
> **What escalated after all.** The original disposition said *"Nothing escalates to Matt."* That was
> correct for this record's own contents and is now **overtaken by a mechanism outside it**: F-1
> proved to be the **fifth recurrence** of the value-set-sweep class, firing
> `desirable-run-pattern.md` § 6.5's own pre-registered graduation trigger — whose named surface is
> **Matt, via jack-ryan**. Two further recurrences (L-63(a), L-65(j)) landed before the graduation
> executed. The law is now **Discipline #72**, minted under ADR-002 process-tier with Matt-veto open
> and explicitly flagged to his surface. **My own F-1 sweep is founding instance 6 of the discipline
> my own F-1 graduated**, and its derived-value half is **#64**'s third basis instance — a clause
> binding eight days before this review ran.
>
> Graduation record: `agentic_orchestration/jack-ryan/notes/2026-08-08-kc2-sweeplaw-graduation-touch.md`;
> engine `design/working-agreement/engineering-disciplines.md` **#72**; decisions-log 2026-08-08.
