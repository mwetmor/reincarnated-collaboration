# KC2-SIM — gamora sitting (corrections + annotations + one modeling note)

**Agent:** gamora (simulation seam)
**Date:** 2026-08-08
**Commission:** gandalf (RUN-CONDUCTOR), at the G-D gate close — standing next-touch queue
**Status:** **CLOSED** — all 5 items discharged. Engine `f06e2981` + `d79950e3`; meta `f77d12a1`.
**UNPUSHED** (conductor pushes at the next fold beat).
**Scope:** BLOCKING PRE-STEP of the C-1 closure lap. Corrections + annotations + one modeling
note. NO new sim behavior, NO s1/s2 re-runs, NO C-1 work.

## Item roster (5)

| # | Item | Severity | Status |
|---|---|---|---|
| 1 | F-1 — superseded floor constant `F13_MEASURED_FLOOR_REGULARS` 289.62 → 288.62 (+ derived pct) | WARN (blocking) | **DONE — 8 hits, not 5** |
| 2 | L-54(d) corrigendum pins — `sm_mod/a` → LOADABLE `sm1/a`, F-L6-FORCED | standing | **DONE — both discharged** |
| 3 | F-3 — bank the 13-file roster as a resident artifact | WARN | **DONE** |
| 4 | F-2 — `+77` test-count decomposition is short by 2 (→ `+75`) | INFO | **FALSIFIED — `+77` decomposes exactly** |
| 5 | R-8 / R-L58-4 — arrival-process model as math-note section (NO sim code) | modeling | **DONE — ARR-1/2/3 raised** |

**Headline for the conductor:** the blocking item is cleared and the C-1 lap is unblocked. Three
things went differently from the brief: **F-1's priced hit list was short by three** (one of them a
second live test pin that would have gone RED on a partial fix), **F-2 is falsified rather than
annotated**, and the **arrival model reversed its own first conclusion** on w152 once the seat law
was read correctly.

## Constraints acknowledged

- Engine-repo edits are mine (seam discipline). Commits AUTO-FIRE (this task = authorization).
- Meta-repo: only this sitting note + the roster artifact.
- NO push from me — conductor pushes at the next fold beat.
- Do NOT touch the sim spec (conductor's file). Spec deltas → proposed edits w/ line refs here.
- Do NOT read/wait on the in-flight legolas Edition-III note.

---

## Running log

### 00:00 — note filed (recovery surface established)

---

# ITEM 1 — F-1: the superseded floor constant

## 1.1 The arithmetic, recomputed independently (NOT taken from the Gate-2 note)

**Floor reconstruction from the w153 strike (L-52(e) E-form):**

```
271.50 (M1 model of record)
+ 10.00  (w152)
+  4.50  (w153: 22 − 17.50)      ← the strike: 22, not 23
+  2.62  (w157)
= 288.62
```

`22 − 17.50 = 4.50` ✓ · `271.50 + 10.00 + 4.50 + 2.62 = 288.62` ✓ — the corrected floor
reproduces exactly.

**Derived percentage — my own computation, before comparing to jack-ryan's:**

| quantity | superseded | corrected |
|---|---:|---:|
| floor | 289.62 | **288.62** |
| excess over record | +18.12 | **+17.12** |
| `(floor − 271.50)/271.50` | 6.674033149 % | **6.305709024 %** |
| rounded 3 d.p. | **+6.674 %** | **+6.306 %** |
| `F13_N_PERTURBATION` = floor/271.50 | 1.066740331 | **1.063057090** |
| mirror scale `2 − p` | 0.933259669 | **0.936942910** |
| code f-string `{100·(p−1):.2f} %` | `6.67 %` | **`6.31 %`** |

**Match check:** my `+6.306 %` **MATCHES** jack-ryan's recomputed `+6.30571 %` to every reported
digit. Independent arithmetic confirms; I did not inherit the value.

## 1.2 ⚑ The hit list is LONGER than the Gate-2 note's five. It is EIGHT engine line-hits.

The value-set sweep (OP § 4.11 / desirable-run-pattern § 6.5) — run whole-file, case-insensitive,
across all four repos, on **both** `289.62` and the `6.674` family (`6.674` · `6.67x` · `6.68x` ·
`1.0667` · `0.9333` — prior-state-names-as-values included) — turns up **three engine line-hits
beyond jack-ryan's five**. One of them is a **second live test pin that would have gone RED on the
correction** and was not in the priced list.

### HIT TABLE — EDITED (8 engine lines, all gamora seam)

| # | surface | line | kind | on JR's list? |
|---|---|---:|---|---|
| 1 | `src/reincarnated/simulation/kc2/calibration.py` | 935–937 | comment — `289.62` + `+6.68 %` | yes (hit 1) |
| 2 | `src/reincarnated/simulation/kc2/calibration.py` | **938** | **LIVE CONSTANT** `F13_MEASURED_FLOOR_REGULARS` | yes (hit 2) |
| 3 | `tests/test_kc2_locomotion.py` | 563 | docstring — `289.62 = +6.67 %` | yes (hit 3) |
| 4 | `tests/test_kc2_locomotion.py` | **565** | **TEST PIN** `== 289.62` | yes (hit 4) |
| 5 | `src/reincarnated/simulation/math/kc2-locomotion-lap-2026-08-08.md` | 369 | `289.62` + `+6.68 %` | yes (hit 5) |
| **6** | `tests/test_kc2_locomotion.py` | **567** | ⚑ **SECOND TEST PIN — `F13_N_PERTURBATION == approx(1.0667, abs=1e-3)`** | **NO — MISSED** |
| **7** | `src/reincarnated/simulation/math/kc2-locomotion-lap-2026-08-08.md` | 370 | `±6.68 %` (the perturb-limb restatement) | **NO — MISSED** |
| **8** | `src/reincarnated/simulation/AGENT_STATE.md` | 25 | `±6.674 %` + `289.62` — the L-52(j) hand-back, never discharged | named at L-52/L-54(f), not in F-1's five |

**Hit 6 is the load-bearing addition.** `|1.0667 − 1.063057090| = 0.003643 > 1e-3`, so correcting
only jack-ryan's hits 1–5 would have left `test_..._is_READ_from_F_13_not_chosen` **RED on its
third assertion** with the first two green — a correction that half-lands and fails noisily. It is
the same tripwire class as hit 4, one line down, and the enumeration stopped one line early. That
is itself an instance of the very failure class this correction remediates (a sweep enumerated by
eye rather than by grep), and it is worth naming as such rather than folding in silently.

### HIT TABLE — BENIGN (not edited; one clause each)

**Engine:**

| surface | line(s) | one-clause reason |
|---|---|---|
| `data/kc2/kc2_crucible_emitter_geometry.csv` | 5, 229 | `46.674` is an emitter x-coordinate — digit-string collision |
| `data/kc2/kc2_crucible_emitter_geometry.csv` | 209 | `326.67` is a bearing in degrees — collision |
| `data/kc2/kc2_crucible_patrolpoints.csv` | 90 | `16.6742` is a patrol-point coordinate — collision |
| `data/kc2/pe6_crucible_waves.csv` | 175, 185 | `16.67` are wave body-count means — collision |
| `src/reincarnated/generation/AGENT_STATE.md` | 1093, 1178, 3318 | `96.67 %` / `66.67 %` caster-coherence + LC-011 figures — rocket seam, unrelated quantity |
| `src/reincarnated/simulation/AGENT_STATE.md` | 2605 | `2026-06-15 SESSION 18` date string — collision |
| `src/reincarnated/simulation/math/dot-tick-delivery-2026-07-28.md` | 29, 66 | `66.67 %` DoT sub-tick delivery fractions — unrelated quantity |
| `src/reincarnated/simulation/math/wr2-d-nova-telegraph-2026-07-29.md` | 231, 238 | `16.67 %` S-7 telegraph margin — unrelated quantity |
| `src/reincarnated/simulation/math/wr3-anchor-refit-2026-07-30.md` | 261 | `36.67` cold-anchor event mean — collision |
| `src/reincarnated/simulation/output/**/*.jsonl` (kitcal traces) | many | `289.627…` leech floats / `…6.67…` tick timestamps — numeric collision (already discharged at L-52(i)) |
| `src/reincarnated/export/*`, `telemetry/*` | — | **ZERO hits.** `count_model_provenance()` carries the model by *citation + SHA*, never the floor value → **no star-lord coupling, no cross-seam hand-back fires** (verified, not assumed) |

**Meta-repo — conductor surfaces, BENIGN BY GOVERNANCE (the correction is already resident):**

| surface | line(s) | one-clause reason |
|---|---|---|
| `gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` | 199, 202, 204, 206, 208, 209, 323 | append-only ledger; L-52(e) states `288.62`, L-52(i)+L-54(f)+L-56(b) state the supersession — tail-append governs (the ledger's own declared rule) |
| `gandalf/notes/2026-08-08-kc2-f13-count-model-discrimination.md` | 403, 416, 423 | derivation record governed by its own appended § 9 addendum, which at :584 names `289.62 → 288.62` explicitly |
| `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` | 1753, 1756 | already annotated in place — :1756–1758 names L-52's corrected `288.62 / ±6.30 %` and grades the swept scale conservative |
| `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` | 3261, 3276, 3494 | each sits in a block carrying a trailing L-52 annotation naming `288.62` (:3280-block at +9 lines; :3498–3500 verbatim E-form) |
| `jack-ryan/notes/2026-08-08-kc2-gate2-locomotion-lap.md` | 49, 196–220, 240 | this *is* the finding that names the correction — stating both values is its function |
| drax / galadriel / legolas / canonical / CHANGELOG | many | `66.67 %` · `16.67` · `216.67` · `−56.68°` · `0.9333 s` · `96.67 %` — unrelated quantities in unrelated seams, digit-string collisions only |

### HIT TABLE — HANDED BACK `(surface, owner)`

| surface | line(s) | owner | why handed back |
|---|---|---|---|
| `agentic_orchestration/gamora/notes/2026-08-08-kc2-locomotion-lap.md` | 41, 429–430, 435–436 | **gamora seam, conductor-folded artifact** | mine by seam, but (a) commission scopes my meta-repo writes to this note + the roster artifact, and (b) it is a **Gate-2-reviewed folded evidentiary record** — §8.4's rows are true measurements *executed at* scale 1.0667/0.9333. Rewriting those values in place would falsify the record of what ran. Correct treatment = **corrigendum annotation, not value rewrite**. Exact proposal in § 1.4 below. |

**Nothing lands in a surface I don't own that isn't already governed.** No `(surface, owner)` pair
routes outside the run's existing hand-back machinery.

### Cross-seam check, run rather than assumed

`export/` · `telemetry/` · `output/` carry **zero** hits on either value.
`wave_engine.count_model_provenance()` — the one declared gamora↔star-lord coupling on the count
model (`export/AGENT_STATE.md:140`, *"NONE beyond a read-only constant compare"*) — carries the
model by **citation + SHA**, never by floor value. **No MIGRATION.md entry is owed and no star-lord
hand-back fires.** Verified by reading the function body, not by trusting the AGENT_STATE claim.

## 1.3 What landed

- `calibration.py` :935–959 — comment corrected; **live constant 288.62**; retired value carried as
  `F13_MEASURED_FLOOR_REGULARS_SUPERSEDED_AT_L52`; the semantic shift stated in-comment.
- `tests/test_kc2_locomotion.py` :561–579 — both pins moved (`288.62`, `approx(1.0631)`); retired
  value **asserted as retired**; the E-form recomputed in-test rather than transcribed.
- `math/kc2-locomotion-lap-2026-08-08.md` :368–371 + a dated corrigendum block — values corrected,
  § F.4's table deliberately **not** restated, with the reason given.
- `simulation/AGENT_STATE.md` :25 — corrigendum appended (the L-52(j) hand-back, discharged).

`n_sensitivity()`'s `perturbation_basis` string is computed from the constants, so it self-corrects
to *"271.5 (record) → 288.62 (measured floor) = 6.31 %"* with no edit needed. Confirmed by reading
the f-string, not assumed.

## 1.4 Proposed corrigendum for the conductor — lap note (NOT executed by me)

`agentic_orchestration/gamora/notes/2026-08-08-kc2-locomotion-lap.md`. Proposed as an
**annotation**, not a value rewrite — the § 8.4 rows are true measurements at the scale they ran
under, and overwriting them would destroy the record of what executed:

| line | current | proposed |
|---:|---|---|
| 41 | `±6.67 % (F-13 floor)` | `±6.674 % as executed (F-13 floor 289.62 → corrected 288.62 = ±6.306 %; envelope conservative)` |
| 429–430 | `271.50 → 289.62 … +6.674 %` | leave as the executed record; append the L-52 corrigendum line beneath |
| 434–436 | table `1.0000 / 1.0667 / 0.9333` | **leave** — these are the scales that ran. Add a footnote: *corrected scales 1.0631 / 0.9369 lie inside the swept pair; re-run rides C-1.* |

---

# ITEM 2 — L-54(d) corrigendum pins: `sm_mod/a` → LOADABLE `sm1/a`, F-L6-FORCED

## 2.1 Executed truth, verified at source

| surface | reads | grade |
|---|---|---|
| `locomotion.py` :177 | `("survivalworld_a.map", "sm1")` | **executed truth** |
| `calibration.py` `ARENA_SELECTION["s2"]` | `("survivalworld_a.map", "sm1", "…⚑ FORCED BY GEOMETRY AVAILABILITY…")` | already correct |
| `calibration.py` :1236 runtime `second_geometry_value` | `"sm1/survivalworld_a vs sm_mod/survivalworld_f"` | already correct |
| `locomotion.py` :181 | `sm_mod/survivalworld_a` | **correct in context** — the clause explaining why that archive *cannot* express tier 16 |
| `calibration.py` :342 docstring | `s2 → sm_mod/survivalworld_a` | ⚑ **STALE — corrected** |
| math note § B.3 :107 + JC-G2 ¶ | `sm_mod/survivalworld_a.map`, *"the archive limb is `sm_mod` for both"* | ⚑ **STALE — corrected** |

Hand-back verified **COMPLETE at exactly two surfaces**, matching Gate-2's affirmative counterpart.
My own independent sweep of `survivalworld_a` across engine `.py`/`.md` found no third.

## 2.2 Treatment

**Corrigenda-forward, and the two surfaces get different treatment because they are different
kinds of document.**

- `calibration.py:342` is **live docstring** — the stale clause is corrected in place and a dated
  `⚑ CORRIGENDUM 2026-08-08 (L-54(d))` paragraph states the mechanism (`sm_mod` carries p01 tiers
  1–15; s2 is tier 16; the limb is forced by geometry availability, not chosen by fit — JC-G8) and
  names the surfaces that were already right.
- math note **§ B.3 is a derivation record**, so the superseded declaration is left **legible**
  with `⚑ SUPERSEDED` inline and a dated corrigendum block beneath carrying the executed-truth
  table, the mechanism, the scope (declaration only — no s2 number moves, because no s2 number was
  ever produced under `sm_mod`), and the lineage L-46 → build → L-54(d) → Gate-2 → discharged.

**One thing worth naming beyond bookkeeping.** JC-G2's *"the archive limb is `sm_mod` for both"*
was load-bearing as an argument for cross-sitting comparability. It is **false for s2**, and the
true statement is **stronger** for the lap's purpose: s1 and s2 differ in **archive as well as
arena**, which *widens* the second-geometry diagnostic's generalisation claim. It is also
independent corroboration of the R-L53-1 loading law — the tier ceiling was derived from archive
contents and then met, unprompted, by the loader.

---

# ITEM 4 — F-2: ⚑ FALSIFIED. The `+77` decomposes EXACTLY.

**Commissioned as:** *"the `+77` decomposition is short by 2 (decomposes to `+75`) — annotate with
the corrected decomposition."* **Measured result: there is nothing to correct.** The lap's `+77`
is right; Gate-2's reconstruction is the thing that was two short.

## 4.1 Method — collection, not parsing

My first attempt reconstructed counts by parsing `@pytest.mark.parametrize` blocks out of
`git show` output and landed at `+79`. **A parser that has to be trusted is not evidence**
(Discipline #11), so I discarded it and measured instead: two throwaway `git worktree`s at
`13451fdf` and `a5382e65`, real `pytest --collect-only -q` per file, worktrees removed after.

| file | @`13451fdf` collected | @`a5382e65` collected | Δ |
|---|---:|---:|---:|
| `tests/test_baton_v1.py` | **51** | **86** | **+35** |
| `tests/test_kc2_locomotion.py` | *absent* | 41 | +41 |
| `tests/test_kc2_micro_oracles.py` | 27 | 28 | +1 |
| `tests/test_kc2_s1_ramp.py` | 26 | 26 | 0 |
| `tests/test_kc2_opposition_wave_engine.py` | 44 | 44 | 0 |
| | | | **+77** |

`git diff --stat 13451fdf a5382e65 -- tests/` lists these five files and no others, so the set is
closed.

## 4.2 Where Gate-2's `+75` came from — the same mechanism it correctly diagnosed elsewhere

Gate-2's F-2 states *"parametrize count is 0 → 0 in all four non-locomotion files, so there is no
hidden expansion there."* **That is measured wrong.** `test_baton_v1.py` carries parametrize at
**both** SHAs:

| SHA | `def test` | `@parametrize` | collected | expansion |
|---|---:|---:|---:|---:|
| `13451fdf` | 49 | 1 (`test_every_json_style…` over `JSON_STYLES`, n=3) | **51** | +2 |
| `a5382e65` | 82 | 2 (`…JSON_STYLES` n=3 · `test_r_loco_1_arena_ref_guard_has_teeth` n=3) | **86** | +4 |

`JSON_STYLES = ('rows-compact', 'indent', 'compact')` at **both** SHAs, so the growth is not there.
The `def test` delta is `82 − 49 = +33`; the **net expansion delta is +2** (`+4 − +2`); total
**+35**. And `+75 + 2 = +77`.

⚑ **The two "missing" tests are the R-LOCO-1 arena-ref guard's own parametrize expansion.**
star-lord's `test_r_loco_1_arena_ref_guard_has_teeth` expands 1 definition into 3 node IDs —
`[patch0-member outside the cited enumeration]`, `[patch1-null selection claiming DECLARED]`,
`[patch2-truncated enumeration]` — i.e. the residual is exactly the cross-seam item **this lap
routed**. The parametrize-expansion mechanism was diagnosed correctly for
`test_kc2_locomotion.py` (39 − 1 + 3 = 41) and then not applied to `test_baton_v1.py`.

## 4.3 ⚑ Independent corroboration — star-lord measured the same +35, from the other side

I found this **after** completing the worktree measurement, which is why it is corroboration rather
than a source. `star-lord/notes/2026-08-08-kc2-baton-waypoints-bundle.md` § 5.2, from his own
census attribution probe:

> *"Collection arithmetic closes exactly: 76 + 10,299 + 21 = 10,396 = jack-ryan's 10,361 at
> `cbb29e68` **+ 35**, and +35 is precisely my baton test additions (**51 → 86**)."*

**`51 → 86` is exactly my measured pair**, arrived at by a different method (his: collection
arithmetic closing against a third party's baseline; mine: `--collect-only` in worktrees at two
SHAs). Two independent measurements, same number, neither derived from the other. The `+33` in
Gate-2's F-2 is the `def test` count; **`+35` is the collected count**, and the seam that owns the
file had already published it.

**Disposition:** F-2's finding is **retired**, not annotated. No edit is owed to the lap note.
The reconstruction and its evidence live here and in the census artifact so the retirement is
auditable rather than asserted. Routed to jack-ryan (his finding, his seam) via the conductor.

---

# ITEM 5 — R-8 / R-L58-4: the arrival-process model

**Deliverable:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-summon-arrival-process-2026-08-08.md`
(new file, 303 lines). **MATH NOTE ONLY — no simulation code wired, no count re-pinned.**

## 5.1 The model

Named constants `L = petLimit` · `B = petBurstSpawn` · `P = petPeriod` · `T = spawnObjectsTimeToLive`
· `M = limit1` · `W` = measured cohort window.

```
k_a(W,P) = floor(W/P) + 1     limb (a) fires on spawn
k_b(W,P) = floor(W/P)         limb (b) re-arms first  — ALSO the approach-delay proxy

Regime I   (T >= W, nothing expires):   A(W) = min( k*B , L )
Regime II  (T <  W, slots recycle):     A(W) <= min( k*B , L*ceil(W/T) )

A_pool(W) = SUM_r  n_r * A_r(W),   n_r <= limit1(r)
```

Both waves sit in **Regime I** (`T` = 30 s and `∞` vs `W` = 10.23 s and 8.63 s).
Windows are galadriel's measured values (fourth extraction § 2.2/§ 2.4) — R-8's *"10.2 s"* is
**10.23 s**, and w157's **8.63 s** was not quoted in R-8 at all.

## 5.2 Results

**w152 crab** (`L8 / B4 / P6 / T30`, `W = 10.23`): limb (a) activates at `t = 0, 6.0` → raw 8,
clamp 8 → **A = 8**. Limb (b) activates at `t = 6.0` only → **A = 4**. Per summoner **`{4, 8}`**.
The limb-(a) answer sits on a flat shelf for `W ∈ [6, 30)` — insensitive to ±4 s of window error.
The limb-(b) answer has only **1.77 s** of headroom to its next step and is window-fragile.

### 5.2a ⚑ AN ERROR THIS NOTE MADE, CAUGHT, AND CORRECTED IN PLACE

My first draft wrote *"5 of 5 members carry the generator → n up to 5"* and concluded the fork was
harmless (2 vs 3 summoners against 5 available). **That read a pool ROSTER as a SEAT COUNT.**
legolas § 2.1's spawn table gives w152 sp1 as `0–0` plain with champion `1–1` — **one crab hero
seats, not five.** *"5 of 5"* is a **reliability** statement (whichever member seats **is** a
producer) and carries no multiplicity at all.

Re-derived under the seat law, with Haraxis (MEASURED) contributing **zero plain** bodies because
both its chains produce Champions:

```
limb (a):  sp1 crab 8  +  sp6 devotion [1..8]  =   9 … 16    >= +10 on most devotion branches
limb (b):  sp1 crab 4  +  sp6 devotion [1..8]  =   5 … 12    >= +10 only on the TOP branch
```

and only **3 of 6** `devotion_heroes` pools are producers at all — if the roll lands on one of the
other three, **neither limb reaches +10 on plain bodies** (sp1 alone tops out at 8).

⚑ **This reverses the draft's conclusion. ARR-1 IS load-bearing for w152.** On limb (b), and on any
non-producing devotion roll, the account does not close on plain bodies alone and pulls **R-5** in
as a dependency (do trap / ground-object bodies render census-visible bars?), or Regime-II
recycling on `chthonianabomination_summontentacles` (`L12`/`B12`/**`T = 5 s`** — the wave's only
`T < W` chain, bound `A ≤ min(12k, 36)`).
**R-L58-3's `SOLE-MECHANISM, CLOSED AT CLASS LEVEL` survives** — every candidate is a generator
chain, so the *class* is untouched — but the *quantitative comfort* of the capacity reading does
not. That is a stronger reason to resolve ARR-1 than the draft gave, and I would rather publish the
reversal than the tidier first answer.

**w157 golem** (`L4 / B4 / no TTL`, `W = 8.63`): `B = L` collapses Regime I to
`A = min(4k, 4) ∈ {0, 4}` — **invariant to `P`, to `k`, and to `W`.** One activation saturates,
nothing ever expires to free a slot, every later activation is fully blocked. The NAMED-ABSENT
`petPeriod` is therefore **harmless** for this chain. Pool ceiling **8** under `limit1 = 2`
(R-L58-4's rule, now with an arrival count attached).

## 5.3 ⚑ ARR-2 — the finding the fold has to see

**The observed w157 `+1` is outside the model's admissible set `{0, 4, 8}`.** The join note's
*"ONE in-window spawn = +1 exactly"* is not what `petBurstSpawn = 4` predicts — the first
activation puts **four** bodies on the board. Four candidate resolutions named, **none adopted**:
partial burst on spawn-point availability · staged emission caught mid-frame · three died before
the census frame (**= C-1**, unavailable in-sim under the declared-zero kill term) · three render
without bars (**= R-5**, galadriel, parked). Or the chain did not fire and `+1` has another source.

**Direction is worth naming:** R-8 was raised expecting capacity to *over*-state arrivals. For
w152 it does, on one limb. **For w157 the arrival model is TIGHTER than the capacity reading and
does not admit the observed value at all.** A model that only ever loosens constraints is not
being used as a model.

## 5.4 Two prescriptions for the G-STATS kill-term fold

1. ⚑ **Do not average a discrete arrival set into a fractional `N`.** w157's answer is `{0, 4, 8}`;
   its mean 4 is not an expectation the process can produce over a single wave — it is a step
   function of one unclosed fork, not a Bernoulli mixture. Carry the **set**, or a **bracket with
   each end's limb named**. Same discipline the run already applied to the F-13 band and the
   `v_ref` K-region.
2. ⚑ **Cap per summoner, never per wave.** `petLimit` at pool level under-counts by `limit1`.

**Forks routed:** ARR-1 (t=0 vs t=P — closable by galadriel frame timing) · ARR-2 (above) ·
ARR-3 (`petPeriod` missing from the join tables for every chain but the crab — legolas rider).

---

# ITEM 3 — F-3: bank the 13-file roster

## 3.1 ⚑ CONFOUND, NAMED BEFORE THE RESULT

The census was launched post-commit at `f06e2981`. **I then edited two files while it was
running** — `calibration.py:350` and the math note § B.3 corrigendum, both to fix an attribution
error I caught by inspection (`ARENA_SELECTION` lives in `locomotion.py:173`, not
`calibration.py`; I had cited the wrong module in my own corrigendum). Both edits are
**docstring/prose only, zero behavioural impact** — but they make the tracked tree dirty, and
`test_kitcal_g5_harness.py::test_G5_W1_untracked_loaded_source_is_invisible_until_it_is_imported`
forces `git status` clean by construction.

**This is the F-11 mechanism again, self-inflicted, and it is recorded before the census returns
rather than explained after.** If that test appears in the roster, the attribution is this edit and
it is settled by re-running the pair against a clean tree — a 13-second check, not an argument.
Star-lord documented exactly this hazard against me during the locomotion lap (*"gamora edited
three modules during and after my census run"*); I reproduced it on myself, which is worth stating
plainly.

**MEASURED RESOLUTION: the tripwire did not fire, and it could not have.**
`test_kitcal_g5_harness.py:624–631` **monkeypatches `git status` to return empty for the whole
test**, precisely so the tracked-modification branch cannot make it pass or fail vacuously. The
lap's pre-commit failure came from the **other** branch — `locomotion.py` was **untracked** and
imported. My edits touched only **tracked** files and planted no untracked importable module, so
that branch was never armed. `test_kitcal_g5_harness.py` is absent from the roster. Named before
the result, closed by mechanism rather than by absence from a list.

## 3.2 The artifact

**→ `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-08-08-kc2-census-roster.md`**

Bare `pytest --tb=no -q` at `f06e2981`, **21 m 29 s**:

```
63 failed, 10354 passed, 3 warnings, 21 errors in 1289.35s
```

⚑ **EXACT on all three scalars vs the lap's binding census at `a5382e65`** (63 / 10,354 / 21) — a
clean smoke gate on the F-1 correction, and consistent with the fact that I added assertions inside
an existing test rather than new test functions, so the collected count should not move. It did not.

**Roster: 12 failure files (63) + 1 error file (21).** Per-file against star-lord's L-39 baseline:
**12/12 EXACT, zero novel failure files, zero novel error files, zero count movement in any file.**

## 3.3 ⚑ The "13" resolved

The lap's § 11.1 column headed **"failure files"** reads `13 / 14 / 13`. The measured set is
**12 failure files + 1 error file = 13 files carrying any problem**. **The count was right; the
column header was imprecise.** Banked so nobody hunts for a thirteenth failing file that does not
exist.

## 3.4 Standing practice adopted

Per Gate-2's *"Action — gamora: emit the failure-file roster alongside the scalars on the next
census, **and as standing practice**"* — adopted. The roster ships with the scalars from here.

---

# PROPOSED SPEC DELTAS (NOT executed — conductor's file)

`agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md`. All four are
**status flips or pointers**, none is a value change; every value in the spec is already current.

| # | line | current | proposed |
|---:|---:|---|---|
| 1 | **1758** | *"gamora hand-back queued for `simulation/AGENT_STATE.md:25`. No count re-pinned."* | → *"gamora hand-back **DISCHARGED** at engine `f06e2981`. The enumeration was **8 engine line-hits**, not the 2 queued nor F-1's 5 — the 3 additions incl. a second live test pin (`F13_N_PERTURBATION`) that would have gone RED on a partial correction. `F13_MEASURED_FLOOR_REGULARS` = 288.62 in code; retired value carried as `…_SUPERSEDED_AT_L52` and asserted-as-retired by test. § F.4 table NOT restated — re-run rides C-1."* |
| 2 | **1871–1872** | *"the math note § B.3 and `calibration.py:342` docstring still carry the superseded 's2 → sm_mod/a' pre-build declaration — gamora hand-backs"* | → *"…**both DISCHARGED** at engine `f06e2981`, corrigenda-forward (superseded declaration left legible with a dated correction beside it). No s2 number moves: `locomotion.ARENA_SELECTION['s2']` always carried `sm1`. **JC-G2's *'the archive limb is `sm_mod` for both'* is now false for s2** — s1/s2 differ in archive as well as arena, which *widens* the second-geometry generalisation claim."* |
| 3 | **3266** (`summoned_bodies` in the un-adopted-mechanism list) | named, no model behind it | → append a pointer: *"arrival process now modelled — `simulation/math/kc2-summon-arrival-process-2026-08-08.md` (R-8 / R-L58-4). Capacity ≠ arrivals: w152 crab `A ∈ {4,8}` per summoner (class closure undisturbed); w157 golem `A ∈ {0,4}`, pool ceiling 8. **⚑ ARR-2: the observed w157 `+1` is OUTSIDE the admissible `{0,4,8}`.** Still UN-ADOPTED — the note is a model, not a pin."* |
| 4 | **1753** | *"(L-54: MEASURED — ±6.674 % moves the mean Δ +0.496/−1.462 s…"* | no change to the value (it records what executed); optional clarity edit *"±6.674 % **as executed**"* to match the corrected AGENT_STATE phrasing |

**Also for the conductor, not a spec delta:** Gate-2 **F-2 is FALSIFIED** (§ item 4 above) — the
ledger's L-56(d) row states *"`+77` decomposes to `+75` (short by 2) — gamora annotates at next
touch."* Measured result is that `+77` decomposes exactly; the correction is owed to the **finding**,
not to the lap. Routes to jack-ryan.

---

# SCOPE HELD — what I did NOT do

- **No calibration executed.** `n_sensitivity()` was not re-swept; § 8.4's table is not restated.
  The corrected scale is declared, the re-run is routed to the C-1 lap.
- **No s1 / s2 re-runs.** No simulation was run at all beyond what the test suite itself drives.
- **No C-1 work**, and I did not read or wait on the in-flight legolas Edition-III note.
- **No sim code for R-8.** The arrival model is a math note. `wave_engine` count paths are
  untouched; **no pin moved**.
- **No spec edits.** Four deltas proposed above with line refs; none executed.
- **No lap-note edits.** The § 8.4 rows are the record of what executed; a corrigendum-annotation
  is proposed at § 1.4 instead of a value rewrite.
- **No push**, either repo. The conductor pushes at the next fold beat.
- **No decisions-log entry.** Nothing here is an architectural commitment — F-1 and L-54(d) are
  corrections, ARR-1/2/3 are forks routed, not rulings.

# SEMANTIC SHIFTS DECLARED (Discipline #12)

1. **`F13_MEASURED_FLOOR_REGULARS` 289.62 → 288.62.** Changes what the constant *means* relative to
   every § 10.9a F.4 table published against it — the code no longer reproduces the executed rows.
   Framed in-code, in the math note, in AGENT_STATE, and in the commit message. Retired value
   carried as a named sibling and asserted-as-retired by test.
2. **JC-G2's *"the archive limb is `sm_mod` for both"* is now FALSE for s2.** Not a typo fix: it was
   a load-bearing comparability argument, and the corrected statement is *stronger* (s1/s2 differ
   in archive as well as arena).

Neither changes a result. Both change how an existing statement should be read, which is why they
are declared rather than folded in.
