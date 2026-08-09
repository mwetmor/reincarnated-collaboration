# KC2-SIM — GATE-2 REPAIR BUNDLE on the stat fold — gamora

**Commission:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, ledger **L-71(g)** — fired against
jack-ryan's Gate-2 verdict **L-70** (PASS-WITH-FINDINGS, 3 WARN / 4 INFO / 0 BLOCK, all within-seam,
approved directly per ADR-002).
**Agent:** gamora (simulation seam) · **Date:** 2026-08-08
**Findings note under repair:** `agentic_orchestration/jack-ryan/notes/2026-08-08-kc2-stat-fold-gate2.md` (613 lines, read in full)
**Target of the findings:** engine `08b87085` + `f573f171`, atop `c17f0791`
**Grading regime:** R-KC2-7 — MEASURED requires a cited reproduction chain
**Push discipline:** **COMMIT-ONLY, NOT PUSHED** (R-KC2-10 — the conductor pushes; my commits ride as passengers)

**Commits (engine, atop `97fb8f65`):**

| SHA | slice |
|---|---|
| `489a74ba` | Gate-2 repair bundle — F-1 / F-2 / F-5 / F-6 / F-7 |
| `81d16e6d` | HB-5 BANKING — the relocated F-3 boss-scale sweep |

**Smoke (Discipline #2, six-file KC2 set, no `-x` per #65):** **258 passed / 0 failed, 36.18 s.**

> ⚑ **ATTRIBUTION (#10) — only +2 of the +14 against the 244 baseline is mine.** `test_baton_v1.py`
> grew **86 → 98** collected in the same working tree under **star-lord's** concurrent HB-2 baton
> commission (`export/baton_v1_{schema,emitter,validator}.py`, uncommitted at run time and **not**
> staged by me). Mine is `test_kc2_monster_stats.py` **19 → 21** (both F-7). The arithmetic closes
> exactly: **244 + 12 (star-lord) + 2 (gamora) = 258.** A smoke number measured on a shared working
> tree is a number about the TREE, and saying "258, +14 mine" would have been a free claim.

---

## 0. Status table

| item | grade | verdict |
|---|---|---|
| **F-1** WARN — vacuous ADDITIVE-NULLABLE test | **MEASURED** | **CLOSED.** Board supplied; pair now discriminating (252.163 → 11.347 reproduced). ONE MIGRATION claim kept, the other struck. |
| **F-2** WARN — 4.736 % does not reproduce | **MEASURED** | **CLOSED — and the leak was LARGER than the sample.** Six magnitudes moved, not one. Corrigenda at **6** in-seam sites; guard tightened; #72 sweep executed — **37 hits / 19 files, 100 % dispositioned, ONE hand-back** (ledger L-69). |
| **F-3** WARN — hit tables are curated subsets | **MEASURED** | **CLOSED — and the un-rowed population is ELEVEN, not the six the finding named.** ⚑ **My first draft of the repair said TEN and was itself wrong**; the programmatic diff caught it. Full reconciliation + population statement below. |
| **F-5** INFO — `:322` cites a token it does not pin | **MEASURED** | **CLOSED.** Corrected in MIGRATION + § 4 here. |
| **F-6** INFO — damage law's unstated sub-rule | **MEASURED** | **CLOSED.** Landed in math note § C; **verified against the implementation**, not asserted. |
| **F-7** INFO — fallback wave/limb-invariant | **MEASURED** | **CLOSED — and it is a SEMANTIC SHIFT (#12), framed as one.** `_g_band` now RAISES. Fallback priced on **both** limbs; **the sign flips**. |
| **HB-5** BANKING | **MEASURED** | **CLOSED.** SHA re-verified immediately before staging, identical. |
| **HB-8** NAMING | **MEASURED** | **CLOSED — naming only, nothing fixed.** Full node-ID list at § 8. |

**F-4 (INFO)** is not in this bundle: its action is *"jack-ryan / gandalf: consider whether …"* and it
is explicitly *"filed as an observation, not a required change."* Nothing is owed by me. Named here
so its absence is a decision rather than an omission.

---

## 1. F-1 — the ADDITIVE-NULLABLE guarantee now has an instrument behind it

### 1.1 Reproduced before repaired (#11)

jack-ryan's probe reproduces exactly on my side. **With the board supplied**, at wave 10 / seed 1:

```
default (run.py's own else branch)        t_end_s = 252.163265
explicit ms.player_damage_per_tick()      t_end_s = 252.163265   same_as_default = True
probe SHEET limb        (51,726.0/tick)   t_end_s =  11.346939   same_as_default = False
probe 1.0                                 t_end_s = 326.530612   same_as_default = False
probe 0.0                                 t_end_s = 326.530612   same_as_default = False
```

The three discriminating values match jack-ryan's 252.163 / 11.347 / 326.531 to the digit.

### 1.2 What the repaired test now carries

`tests/test_kc2_monster_stats.py::test_simulate_wave_accepts_the_limb_additively_without_moving_its_default`
now supplies `hp_lookup=ms.ehp_lookup(10, ms.LevelLimb.LO)` to both calls and adds a third,
probing call. **Two limbs with two different jobs, which the single old assertion conflated:**

- **limb (i) — the default is PINNED.** `a` (no parameter ⇒ `run.py:313–314`'s own `else` branch)
  must equal `b` (parameter supplied from `monster_stats`). If `run.py`'s expression ever drifts from
  `player_damage_per_tick(DB_COMPONENT)`, this breaks. **Chained with `test:171`** — which pins
  `player_damage_per_tick(DB_COMPONENT)` to `(flat_physical_min + flat_physical_max) / 2` — the loop
  closes from the emitted branch back to the composed basis. jack-ryan's objection to `:171` was that
  it *"never imports `run.py`"*; correct, and it no longer has to, because limb (i) does.
- **limb (ii) — the comparison CAN fail.** The SHEET probe must move `t_end_s`. Without it, limb (i)
  is an equality between two things that were never able to differ, which is what the old test was.

### 1.3 The MIGRATION cell — ONE claim, and the other struck

F-1's action was *"either add a test that reads `run.py`'s default branch, or soften the MIGRATION
cell to 'verified by inspection of the diff' — **not both claims, one of them**."*

**Kept: the test claim.** The cell still reads `**NONE** — asserted by
test_kc2_monster_stats.py::test_simulate_wave_accepts_the_limb_additively_without_moving_its_default`,
and it is now true. **Struck: the by-inspection claim** — the addendum states explicitly that the
entry does *not* also rest on inspection of the diff. The probe numbers are pasted into the MIGRATION
entry so a consumer can re-run the discrimination rather than trust it.

> **Why the strong option and not the soft one.** Softening to "verified by inspection" would have
> been honest and cheap, and would have left the cross-seam contract permanently unguarded — a
> boundary in prose only. That sentence is mine, from the fold's own § 1.2; it should cost me the
> same thing it costs the instrument.

---

## 2. F-2 — the level bracket. THE SAMPLE WAS ONE MAGNITUDE; THE POPULATION IS SIX

### 2.1 Reproduction from the shipped board (R-KC2-7 cited chain)

Read `data/kc2/t22_band_a_monster_stats.csv` (`0d6992e8…`, 968 rows), take rows where `ehp_w93_lo`
is non-empty (**967** — the population the note itself names), sum each limb.

```
 wave     population     n    median_lo          sum_lo          sum_hi  bracket_%
   w1        all_ehp   967      291,018     330,176,187     341,401,376     3.3998
   w1       rostered   895      357,588     321,253,931     331,992,357     3.3427
   w1   dmg_measured   953      307,825     329,464,418     340,665,628     3.3998
  w47        all_ehp   967      295,707     335,442,657     346,770,512     3.3770
  w47       rostered   895      363,238     326,376,084     337,212,635     3.3203
  w47   dmg_measured   953      312,784     334,718,695     346,022,272     3.3770
  w93        all_ehp   967      311,447     353,123,210     364,796,031     3.3056
  w93       rostered   895      382,207     343,572,162     354,738,425     3.2500
  w93   dmg_measured   953      329,433     352,358,320     364,005,866     3.3056
```

**All nine combinations land in 3.25 – 3.40 %.** jack-ryan's exhaustive ruling-out reproduces
exactly. Per-record distribution at w93: mean 3.037 %, median 2.477 %, max 10.376 %, 6 zero-width
rows. **No reading of the artefact reaches 4.736 %.**

⚑ **One thing the retired single figure never said: the bracket is mildly WAVE-DEPENDENT** —
3.3998 % (w1) → 3.3770 % (w47) → 3.3056 % (w93). A one-number summary of a wave-indexed quantity is
its own small #63 hazard, and the corrigendum states all three.

### 2.2 ⚑ #72 CLAUSE 7 APPLIED TO THE FINDING ITSELF — the leak is six magnitudes, not one

*"A defect found in a sample is a hypothesis about the population."* jack-ryan found the bracket. If
the mechanism is *"the board was re-emitted under the per-slot correction and the derived magnitudes
were not re-stated,"* then **every** magnitude in that block is suspect. I swept the block:

| quantity | RETIRED (per-pool snapshot) | **SHIPPED BOARD** | moved? |
|---|---|---|---|
| n (rows carrying eHP) | 967 | **967** | no |
| median (lo limb), w93 | 298,651 | **311,447** | **YES** |
| Σ lo, w93 | 349,743,635 | **353,123,210** | **YES** |
| Σ hi, w93 | 366,306,626 | **364,796,031** | **YES** |
| **bracket, w93** | **4.736 %** | **3.3056 %** | **YES — jack-ryan's finding** |
| TTK, limb DB | 72.99 s | **76.12 s** | **YES — not in the finding** |
| TTK, limb SHEET | 0.4080 … 0.5580 s | **0.4254 … 0.5819 s** | **YES — not in the finding** |
| ratio DB : SHEET | ×130.8 … ×178.9 | ×130.8 … ×178.9 | **no — INVARIANT** |
| per-RECORD floor-set widths | "1–3" | **1…6** | **YES — not in the finding** |

**The ratio is the control.** It is a ratio of DPS, so the median cancels — and it is the one figure
in the block that did **not** move. That is not luck; it is the mechanism's own signature, and its
invariance is what confirms the diagnosis rather than merely being consistent with it.

**Direction, and why nothing downstream broke.** The per-pool union WIDENED the level sets ⇒ lower
Σ lo, higher Σ hi, wider bracket, lower median ⇒ shorter TTK. Every retired figure **overstated** the
residual or **understated** the kill cost. The error was conservative in every limb, which is why a
1.4 pp drift could ride in production for a day without a gate noticing.

### 2.3 ⚑ AND ONE FIGURE THAT SURVIVES — the widths were RIGHT, and being read wrong

Math note § 2.1 reads *"floor-set widths across pool slot declarations   width 2: 454 · width 3: 235
· width 1: 6."* Sum **695** — the same population as the `(a)/(b′) IDENTICAL 695 / 695` line beneath
it. I traced it to the instrument (`gamora_kc2_stat_fold_ed3_2026_08_08.py:426–450`): it counts
**(pool × lv-formula) declarations**, not records. **The figure is correct for its own object.**

A record's level set is the **union over every slot that can roll it**, so it can exceed any single
declaration's width. The board's own sets prove the union mechanism without needing the vendor tree:

```
distinct level sets on the board, width >= 4:
    (102,103,104,105)   (103,104,105,106)   (104,105,106,107)   (105,106,107,108)
    (103,104,107,108)   <- NON-CONTIGUOUS   (103,104,105,107,108)   (103,104,106,107,108)
    (102,103,104,105,106)   (104,105,106,107,108)   (103,104,105,106,107,108)
per-record width distribution, all 968 rows:  {1: 5, 2: 688, 3: 226, 4: 32, 5: 14, 6: 3}
```

**`(103,104,107,108)` cannot be produced by any single ≤3-wide declaration.** All 49 width-≥4 rows
decompose this way. So: **§ 2.1's number is not corrected, it is DISAMBIGUATED**; and `calibration.py`'s
*"widths 1–3"* and § 5.1's *"floor sets of width 1–3"* — which took the per-declaration number for
the per-record one — **are** corrected. Two objects, one phrase. Calling all four a leak would have
been as wrong as calling none of them one.

### 2.4 The guard, and why its absence is the actual finding

`test_the_level_bracket_is_NON_TRIVIAL_which_is_why_it_is_carried` asserted `0.03 < x < 0.07`.
**3.3056 % sits inside that band, so the suite stayed green while the test's own docstring was false
against the artefact it reads.** Repaired into two assertions with two jobs:

```python
assert bracket == pytest.approx(0.033056, abs=5e-6)   # (i) DRIFT GUARD, against the SHA-pinned board
assert 0.01 < bracket < 0.05                          # (ii) DESIGN CLAIM — non-degenerate
```

Limb (i) means a board re-emit that moves the bracket now **fails**, which forces the #64 re-statement
that did not happen last time. `test_L_is_a_SET…`'s `widths <= {1..6}` is tightened to `==` for the
same reason — a subset assertion could not tell the per-pool snapshot from the per-slot truth.

### 2.5 Corrigenda landed (in-seam)

| site | change |
|---|---|
| `kc2/calibration.py:893–901` (`s1_kill_term_fold` docstring — the fold's consuming surface) | bracket, widths, both TTK figures corrected; corrigendum banner naming #64 + the retired values in place |
| `math/kc2-stat-fold-ed3-2026-08-08.md` § 5.1 | full corrigendum block: retired→shipped table, reproduction chain, wave-dependence, the guard added |
| `math/…` § 5.2 | `0.41–0.56` → `0.43–0.58`; `72.99 s` → `76.12 s`, both struck in place |
| `math/…` § 2.1 | disambiguation block (§ 2.3 above) |
| `tests/test_kc2_monster_stats.py` | band tightened; widths equality; docstrings re-stated |
| `simulation/AGENT_STATE.md` | SESSION 109's `0.41–0.56 s` and `~73 s/body` **struck in place** (not forward-pointed) — see § 7 for why this surface is the exception; SESSION 110 block added |

**Six sites, and the list is the population, not a selection** — it is the in-seam subset of the
§ 2.6 sweep table, which is where the completeness is established.

⚑ **One correction the fold's own text needed and the finding did not ask for.** The `0.43–0.58 s`
is **arithmetic on the median body**, and § 5.2 read it as though it were a measurement. Measured
per-body kill time from `s1_kill_term_fold` (waves {10,30,50,70,90} × both level limbs, SHEET limb,
8 seeds):

```
 wave limb  bodies  cum_kill_s  per_body_s  cleared          binding
   10   lo   12.88       5.561      0.4319        8     last_arrival
   30   lo   20.00       7.806      0.3903        8     last_arrival
   50   lo   16.00      10.224      0.6390        8     last_arrival
   70   lo   26.50      10.439      0.3939        8     last_arrival
   90   lo    2.00       9.796      4.8980        8  cumulative_kill
```

The arithmetic sits **inside** the empirical spread (0.390 … 0.669 s on the four low waves). The w90
figure is 4.898 s because only **2 bodies** spawn there — a body-mix fact, not a disagreement — and
it is the wave where the binding term flips, which is the fold's own headline. **Both are now
labelled for what they are.**

### 2.6 #72 OBLIGATION — the value sweep on the old spelling

**A value change owes the sweep.** Executed mechanically; output pasted; every hit rowed.

**DECLARED SET.** Roots: **the ENTIRE tree of both repos** — `/Users/admin/Games/reincarnated-engine`
and `/Users/admin/Games/reincarnated-collaboration` — deliberately WIDER than the stat fold's
`{src,tests,design}` + `{agentic_orchestration,canonical}`, because a stale value does not respect a
folder boundary. Types: all text files (`grep -I` skips binaries). Surfaces: **tracked** (`git grep`)
**and untracked-not-ignored** (`git ls-files --others --exclude-standard`). EXCLUDES: `.git`,
`__pycache__`, `node_modules`, `.venv`, `galadriel/**/captures` image trees. **PATTERN:**
`(^|[^0-9,.])4\.736([^0-9]|$)|(^|[^0-9,.])4\.74([^0-9]|$)|(^|[^0-9,.])4\.7 ?%|~ ?4\.7([^0-9]|$)` —
i.e. the exact value plus its 2-d.p., 1-d.p.-with-percent and approximation spellings, left-guarded
so timestamps (`21:13:24,736`) and longer decimals (`4.733727…`) cannot match. **A first attempt with
an unguarded `4.736` returned 13 MB of timestamp noise; the guard is why this table is 37 lines and
not 40,000, and the guard is stated so it can be challenged.**

**RESULT: 37 hit lines across 19 files. Rowed: 19 / 19 files, 37 / 37 lines.**

| # | file | hits | owner | disposition |
|---|---|---|---|---|
| 1 | `engine/src/reincarnated/simulation/kc2/calibration.py:895` | 1 | **gamora** | **CORRECTED** → 3.3056 %, with the retired value struck in place. The shipped-code instance. |
| 2 | `engine/src/…/math/kc2-stat-fold-ed3-2026-08-08.md:274,277` | 2 | **gamora** | **CORRECTED** — § 5.1 corrigendum block. |
| 3 | `engine/tests/test_kc2_monster_stats.py:90` | 1 | **gamora** | **CORRECTED** — docstring re-stated; band tightened in the same edit. |
| 4 | `meta/…/gamora/notes/2026-08-08-kc2-stat-fold.md:36,138,409` | 3 | **gamora** | **AS-EXECUTED RECORD — STANDS, corrigenda-forward.** Forward-pointer to this note added at § 6; the return note is not retro-edited (run convention). |
| 5 | `meta/…/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` L-68(c) | 1 | **gandalf** | **DISCHARGED UPSTREAM — no action owed.** The conductor's own corrigendum lands at **L-70(d)** (*"the level bracket is NOT 4.736 % — the shipped board gives 3.3056 %"*). Cited as discharged per the commission. |
| 6 | `meta/…/2026-08-07-kc2-sim-run-ledger.md` L-69 | 1 | **gandalf** | ⚑ **HAND-BACK — not named in the finding.** L-69 carries *"the 4.736 % bracket = NAMED, PRICED residuals carried on the baton."* Same corrigenda-forward logic as L-68(c) and covered in substance by L-70(d), but **not explicitly named there**. Conductor's row, conductor's call. |
| 7 | `meta/…/2026-08-07-kc2-sim-run-ledger.md` L-70, L-71 | 2 | **gandalf** | **BENIGN — these ARE the corrigendum** (L-70(d) states the correction; L-71(g) states this commission). Correct as written. |
| 8 | `meta/…/2026-08-07-kc2-sim-run-ledger.md` L-67(c) | 1 | **gandalf** | **BENIGN — different referent.** Matched on `"+3.5…+4.7 %"`, the C-1 armorbase silent-failure class, not the bracket. ⚑ **I opened this row intending a hand-back and closed it as benign on inspection**, which is worth stating: the same row carries *"`L` is a floor-SET (**widths 2/454 pools** · 3/235 · 1/6)"* and *"per-body eHP is a ~2–4 % bracket"*. The word **"pools"** is doing exactly the disambiguating work § 2.3 says my own note failed to do, and the ~2–4 % is correct against the shipped board (per-record mean 3.037 %, median 2.477 %). **The conductor's row is right where mine was ambiguous.** No action owed. |
| 9 | `meta/…/jack-ryan/notes/2026-08-08-kc2-stat-fold-gate2.md` ×8 | 8 | **jack-ryan** | **BENIGN — this is the finding itself.** Every instance quotes the retired value in order to retire it. Correct as written. |
| 10 | `engine/src/…/math/kc2-c1-closure-ed3-2026-08-08.md:145` | 1 | **gamora** | **BENIGN — different referent.** *"a missing 4.7 % on a body that looks fine"* is the C-1 armorbase class (`zombie_c01` +4.705 %), not the level bracket. |
| 11 | `engine/src/reincarnated/simulation/AGENT_STATE.md:6908` | 1 | **gamora** | **BENIGN — different referent.** `0.63–4.74×` is the RESOLVE convergence ratio. |
| 12 | `engine/src/…/math/kpm-band-spatial-recalibration-…-STAGE2B-….md:79,122,129` | 3 | **gamora** | **BENIGN — different referent.** `4.74×` KPM convergence ratios. |
| 13 | `engine/output/S1-first-batch-2026-05-19/cohesion-judging-2026-05-19.md:133` | 1 | **star-lord** | **BENIGN — different referent.** `(~4.7)` cohesion score. |
| 14 | `meta/…/dispatches/2026-06-16-gamora-kpm-band-spatial-recalibration.md:115` | 1 | **knight-rider** | **BENIGN — different referent.** `0.63–4.74×`, same object as row 12. |
| 15 | `meta/…/skill_handoff_2026-06-16.md:116` | 1 | **knight-rider** | **BENIGN — different referent.** KPM band `4.74`. |
| 16 | `meta/…/drax/notes/2026-08-01-beam-slits.md:13,80,86` | 3 | **drax** | **BENIGN — different referent AND different unit.** `4.74 m` slit lengths. |
| 17 | `meta/…/drax/notes/2026-08-01-lap-2c-restage.md:656` | 1 | **drax** | **BENIGN — different referent.** Beam-slit restage, same object as row 16. |
| 18 | `meta/…/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md:769` · `2026-07-30-ambient-refit-fold-in.md:2492` | 2 | **gandalf** | **BENIGN — different referents.** `4.7 %` of fight time; `4.74 m` slit length. |
| 19 | `meta/…/galadriel/{pipeline/lifecycle-scores.json, captures/…/bind-w157.json, captures/…/p0-player-action-state-4012-raw.json}` | 3 | **galadriel** | **BENIGN — machine artefacts.** Bare `4.736,` / `4.74,` array elements in emitted JSON; no claim, no prose, no grade word. |

**POPULATION STATEMENT.** The stated pattern over the stated set returns **37 hit lines across 19
files**. The table above has **19 rows covering all 19 files and all 37 lines** — the row/file
counts coinciding at 19 is arithmetic coincidence, not a check (the ledger is 1 file across 4 rows;
galadriel is 3 files in 1 row; gandalf's charter + fold-in are 2 files in 1 row). **The check that
matters is the one stated: 37/37 lines and 19/19 files, reconciled against the tool's output rather
than against my memory of it.** *"Every hit is dispositioned"* is now true of the **SWEEP**, not
merely of the table — which is the sentence F-3 says I did not earn last time.

**HAND-BACKS: ONE.** Row 6 (**ledger L-69**, gandalf) is the only row I cannot close myself. Row 5
(L-68(c)) is **discharged upstream** at L-70(d) and cited as such per the commission. Row 8 I opened
as a second hand-back and **closed as benign on inspection** — the conductor's phrasing is correct;
see the row. Rows 9–19 are other seams' surfaces with different referents and no action owed.

**A companion sweep on the other five leaked magnitudes** (`298,651` / `349,743,635` / `366,306,626`
/ `72.99` / `0.4080` / `0.5580` / `0.41–0.56` / `widths 1–3` / `width 2: 454`) over the same set
returned **21 hit lines across 8 files**: math note ×8 **CORRECTED**; `calibration.py:893,901` ×2
**CORRECTED**; `AGENT_STATE.md:11` ×1 ⚑ **OWED — see § 7**; gamora return note ×2 **as-executed,
stands**; jack-ryan gate2 note ×4 and ledger L-68 ×1 **benign, these are the finding**; drax
`2026-08-01-vfx-truth-1.md` ×2 and gandalf `2026-08-01-br2-true-shape-run-charter.md` ×1 **BENIGN —
different referent** (`0.4080 m` corridor half-width, a length in metres).

---

## 3. F-3 — the hit tables. THE UN-ROWED POPULATION IS TEN, AND SIX WAS THE SAMPLE

### 3.1 The reconciliation, mechanical

Both declared sweeps re-run over the fold's own declared set (roots
`engine/{src,tests,design}` + `meta/{agentic_orchestration,canonical}`; types `*.py`, `*.md`;
excludes vendor / `captures` / `__pycache__` / `.git`; `grep -rniE`), and the **file sets diffed
programmatically against the files my published tables name** — not eyeballed.

```
=== SWEEP A ===  mechanical files 24   hit lines 181   rowed files 19   UN-ROWED 5
=== SWEEP B ===  mechanical files 16   hit lines  76   rowed files  8   UN-ROWED 8
```

Of those 13, **two post-date the fold** — jack-ryan's own Gate-2 note, which matches in **both**
sweeps — and are outside the fold-time population. **Fold-time un-rowed: ELEVEN.** jack-ryan required
rows for **six** and bracketed three SWEEP-A this-commit artefacts as *"defensibly trivial."*
**Two are in neither account** — rows **B-3** and **B-7** below.

> ⚑ **AND I NEARLY SHIPPED THIS SECTION WITH THE DEFECT IT REPAIRS IN IT.** My first draft of the
> two tables below listed **ten** and reconciled by eye. The programmatic diff says **eleven**: I had
> rowed the fold's return note under SWEEP A and **not** under SWEEP B, where it also matches (row
> **B-7**). One document, two sweeps, one row. **This is F-3 at one level deeper, found by the same
> tool that found F-3 and not by re-reading**, which is the entire content of #72 clause 5 —
> a hand-curated list is a labelled expectation, and mine was wrong twice in a row about the same
> file. The count in this note is the diff's, not mine.

### 3.2 The missing rows (SWEEP A)

| surface | hits | owner | disposition |
|---|---|---|---|
| **A-1** `meta/…/gandalf/notes/2026-08-08-kc2-locomotion-spec-amendment.md:23` | 1 | **gandalf** | **BENIGN — and VINDICATED, not merely unaffected.** It states the composition is *"closer to `max(last_arrival, cumulative_kill) + tail`"*; the fold makes `max` and `+` separate for the first time, which is the condition under which that sentence becomes discriminating rather than vacuous. Created 11:17:14, ~7 h before the fold — **it existed at sweep time and I did not row it.** |
| **A-2** `engine/src/…/math/kc2-stat-fold-ed3-2026-08-08.md` | 8 | gamora | **BENIGN — this-commit artefact.** The fold's own math note; the hits are the fold describing itself. |
| **A-3** `engine/tests/test_kc2_monster_stats.py` | 9 | gamora | **BENIGN — this-commit artefact.** The new tests; the hits are the assertions that make the shift falsifiable. |
| **A-4** `meta/…/gamora/notes/2026-08-08-kc2-stat-fold.md` | 10 | gamora | **BENIGN — this-commit artefact.** The return note carrying the table. ⚑ **A table that omits the document it lives in is the most defensible omission and the least defensible principle** — clause 5 says the sweep's output is the sweep's output. |

### 3.3 The missing rows (SWEEP B)

| surface | hits | owner | disposition |
|---|---|---|---|
| **B-1** `engine/src/reincarnated/simulation/kc2/run.py:219,283` | 2 | **gamora** | **BENIGN — parameter plumbing, no grade word.** `p05_drip_cadence_s: Optional[float] = None` and its pass-through. Carries no claim about the cadence's grade. ⚑ **This is production code in MY OWN seam that I edited in the same commit, and it had no row** — the least excusable of the ten. |
| **B-2** `engine/src/reincarnated/simulation/MIGRATION.md:68,71` | 2 | **gamora** | **BENIGN — this IS the graduation entry.** Item 4 states the ADOPTED → MEASURED move and the deliberate non-rename. Correct as written; it should have been rowed as such. |
| **B-3** `meta/…/gamora/notes/2026-08-08-kc2-locomotion-lap.md:29,336,354,358,626,628` | 6 | **gamora** | ⚑ **THE TENTH — absent from jack-ryan's account as well as mine.** As-executed record of the locomotion lap, carrying *"ADOPTED, not measured (L-21)"* at `:626`. **Stands** — it describes a lap that ran under the retired grade. Confusable with the ENGINE file `math/kc2-locomotion-lap-2026-08-08.md`, which **is** rowed; two files, similar names, one row between them. |
| **B-4** `engine/src/…/math/kc2-summon-arrival-process-2026-08-08.md:592,599,620,629` | 4 | **gamora** | **BENIGN — this IS the graduating artefact.** § 592–629 is where `P05_DRIP_CADENCE_S` graduates. Correct as written. |
| **B-5** `meta/…/gamora/notes/2026-08-08-kc2-c1-closure-arr-repass.md` (5 hits) | 5 | **gamora** | **BENIGN — this IS the graduation's home record** (§ 4b / `:267` *"THIS RETIRES THE 'ADOPTED, NOT MEASURED' GRADE"*). The document Gate-2's V-1 timeline rests on. |
| **B-6** `meta/…/galadriel/notes/2026-08-08-eor-followup-extraction.md:231,252` | 2 | **galadriel** | **BENIGN — dispositioned upstream at L-67(j) and not restated by me.** The extraction that supplies the *"3 s drip cadence starting t+4 s"* reading. Other seam; no action owed. |
| **B-7** `meta/…/gamora/notes/2026-08-08-kc2-stat-fold.md` (6 hits) | 6 | **gamora** | ⚑ **THE ELEVENTH — in neither jack-ryan's account nor my own first draft of this table.** The fold's return note matches **both** patterns; I rowed it under SWEEP A (row A-4) and not under SWEEP B. **BENIGN — this-commit artefact**, the note carrying the tables. **One document, two sweeps, one row is one row short**, and the only thing that caught it was diffing the tool's file set against mine in code. |

### 3.4 ⚑ One published row that is WRONG, found by executing F-3 properly

§ 6.2 row 9 reads: *"`math/kc2-locomotion-lap-2026-08-08.md:559–560` | **STANDS — as-executed
record**, already banner-annotated at the C-1 lap."*

**Checked: that file carries no cadence-graduation banner.** Its only `SUPERSEDED` banners (`:107`,
`:416`, `:440`) are about the bar_hue census and the F13 floor — different objects. The graduation
banner lives in `gamora/notes/2026-08-08-kc2-c1-closure-arr-repass.md:267` and in the ledger.

**Corrected disposition:** *"STANDS — as-executed record. The graduation is recorded at the C-1 lap
note (`…-c1-closure-arr-repass.md:267`) and at ledger L-67(g), **not in this file.**"* The old
sentence read as *"this file was annotated"* and only the other reading was true. A row with a
reason is worth having only if the reason is checkable, and this one was not — **which is F-3's own
thesis arriving one level deeper than the finding placed it.**

### 3.5 Population statement

**"UNRESOLVED rows: none. Every hit is dispositioned"** (return note § 6) was **true of the tables
and false of the sweeps.** Restated, with the population named:

> *Across **SWEEP A** (24 files / 181 hit lines) and **SWEEP B** (16 files / 76 hit lines) over the
> declared set, **every file returned by the tool is now rowed** — 19 previously + 4 new for A,
> 8 previously + 7 new for B. **One file is declared OUT of the fold-time population by date**
> (jack-ryan's Gate-2 note, which matches in both sweeps and did not exist when they were run);
> that is an exclusion by **date**, not by judgement, and it is stated rather than assumed.*

**Table row-count == mechanical file-count, in both sweeps, checked by diffing the tool's file set
against the table's in code rather than by reading.** The check is the point: reading is what
produced both the original omission and my first draft's.

---

## 4. F-5 — the citation

`test_kc2_s1_ramp.py:322` reads
`assert s.kill_time_grade == cal.KILL_TIME_GRADE == "NAMED-ABSENT-DECLARED-ZERO"`. That is
`calibration.py:318` — a **module constant** on the s1-cycle sample. It is **not**
`composition.kill_term_grade`, the per-run field `run.py:524` emits. **Two unrelated surfaces
spelling the same token**, which is precisely the confusion #67 exists to catch, and I walked into it
while citing #67.

**Corrected protection statement: ONE pin, PREFIX-ONLY.** The only test reading `run.py`'s emitted
token is `test_kc2_locomotion.py:530`, `.startswith("NAMED-ABSENT")`.

**Consequence I owe the consumers, which the finding stops short of:** a consumer keying on the
**whole string** is protected by nothing on this side. MIGRATION now says so and tells them to key on
the prefix. **The keep-decision is unaffected** — the token is still accurate for a call with no
board, and renaming would still move a live contract. What was wrong was the evidence, and a
cross-seam contract citing a pin that is not there advertises one guarantee more than it has.

---

## 5. F-6 — the damage law's sub-rule

Landed in `math/kc2-stat-fold-ed3-2026-08-08.md` § 3.1, in the law statement itself.

> **RULE: a flat entry with no resolvable `Max` is a POINT value ⇒ `Max := Min` FOR THAT SKILL,
> before the per-skill sums are taken.**

**Verified against the implementation rather than asserted** (`gamora_kc2_stat_fold_ed3_2026_08_08.py:307–322`,
`_at()` at `:285–291`). Three reachable cases, all the same rule: key **absent** from the `.dbr`; key
present as an array but **`rank_i − 1` outside it**; key resolves to **zero** at the required rank.
⚑ **And the rule is SYMMETRIC** — `if not mn: mn = mx` — a limb neither the finding nor my own § 3.2
parenthetical mentions. If neither resolves the type is **skipped**, not zeroed.

**Priced:** `passiveproperties_boar.dbr` declares `offensivePhysicalMin` with no `offensivePhysicalMax`
key at all; a reproducer working from the stated law alone missed `boar_a03` by **15.12 %** on the
max limb. Under the rule it reproduces to 6 s.f. (1.178191 vs board 1.178191, against 0.742021 for
the alternative), and the sample goes 43/43.

**Why `Max := Min` and not `Min := 0`:** both make the row internally ordered, but only one is a
measurement. A missing `Max` read as zero gives the inverted interval `[Min, 0]` — the same symptom
the `Skill_Passive` discriminator was minted for.

**On "unstated."** § 3.2 already carried *"`Max` defaults to `Min` when absent or zero, inside the
skill."* It is true. It is also (a) inside a paragraph about a **different** correction, (b) missing
the array-index case, (c) missing the symmetric limb, and (d) **not in the law statement a reproducer
reads.** R-KC2-7 asks for a chain a careful reproducer can execute from its stated form; a true
sentence three sub-sections away does not make the stated form executable. **The finding is right and
the "it was already there" defence is not available.**

---

## 6. F-7 — the fallback and the clamp. ⚑ THIS IS A SEMANTIC SHIFT (#12), FRAMED AS ONE

### 6.1 The fallback, priced on BOTH limbs

`ehp_lookup`'s docstring now declares the invariance and prices it. **I measured the HI limb, which
the finding does not:**

```
limb LO :  w1  +6.88 %   w47  +5.22 %   w93   0.00 %   (the cell it was taken from)
limb HI :  w1  +4.23 %   w47  +2.62 %   w93  -2.42 %   ⚑ SIGN FLIPS — it UNDER-states here
share of the roster                              1 / 968  =  0.103 %
```

jack-ryan's LO figures reproduce exactly. **The sign flip matters more than the magnitude:** a
consumer told only *"the fallback overstates by up to 6.9 %"* would conclude it is conservative and
could safely be ignored in one direction. **On the HI limb at w93 it is not.**

**Not repaired by making it move.** A two-anchor reconstruction of a record that has no record would
be an invented number — the exact thing the INFERRED grade exists to refuse. **Declared, priced,
left alone;** it closes when the record does (F-L7 / C-1).

### 6.2 `_g_band` — RAISES now, and this is a behaviour change

**OLD:** `return G_BAND_A[max(0, min(len(G_BAND_A) - 1, int(wave) - 1))]` — silent saturation, under
a docstring promising it would *"say so by construction."*
**NEW:** `ValueError` outside 1…93, with the band named in the message.

> ⚑ **I am calling this a SEMANTIC SHIFT and not a docstring fix, because it changes what a call
> outside 1…93 MEANS.** Before, `_g_band(150)` returned a number; after, it raises. Any caller
> relying on the saturation — none exists today — changes behaviour. Framed per **#12** rather than
> buried as a fix, per the standing rule that when I am unsure which it is I assume the shift.

**Why raising rather than annotating.** Band B (s2, waves 151–160) is a **different board**, excluded
by name from this fold. `G[92] = 156.0` against band B's own term (`survivalmode_enemies03[151] = 308.0`
at w152) is **understated ~2×** — not a rounding, a different object. A wave-150 lookup that returns
a number is a wrong answer wearing a right answer's clothes, which is #63's whole subject.

**Blast radius: ZERO, and enumerated rather than assumed.** Every call site of `_g_band` was walked:
`MonsterStat.ehp` (`monster_stats.py:167`) is the only one, reached from `ehp_lookup` ← `s1_kill_term_fold`
/ tests, all in-band. **The raise is unreachable from the shipped call graph and exists to keep it
that way.** Pinned by `test_g_band_RAISES_outside_band_A_instead_of_saturating_silently`, which
asserts the in-band values are byte-unchanged *first*.

---

## 7. ⚑ THE ONE PLACE WHERE CORRIGENDA-FORWARD AND THE CHECKPOINT CONVENTION CONFLICT

`src/reincarnated/simulation/AGENT_STATE.md` carried the retired *"0.41–0.56 s per median body"* and
*"~73 s/body"* in its SESSION 109 block. This is the one site where the run's two conventions point
opposite ways, so I am stating the reasoning rather than just the outcome.

- **Corrigenda-forward** says an as-executed record stands and the correction lands forward. That is
  why the return note (§ 2.6 row 4) and the ledger rows are **not** retro-edited.
- **But `AGENT_STATE.md` is not a record of what happened — it is a statement of where things
  ARE**, read at the top of every session I start. A stale figure there is not history; it is a
  **wrong current claim**, which is the same object F-2 is about.

**Resolved: corrected IN PLACE, with the retired value struck and visible** — the identical treatment
`calibration.py`'s docstring got, and for the identical reason (both are live-read surfaces, not
archives). A **SESSION 110** block is prepended carrying the bundle; the SESSION 109 block keeps its
as-executed shape everywhere the figure is not load-bearing on a reader's next action.

**What I did NOT retro-edit, and the line between them:** the return note, the math note's §§ outside
the corrigendum blocks, and every ledger row. Those are archives. The distinguishing test I used is
*"would a reader take this sentence as a statement about the world today?"* — if yes it is corrected
in place, if no it gets a forward pointer.

---

## 8. HB-8 — NAMING ONLY. NOTHING FIXED.

**The commission: *"mechanically enumerate ALL failure + error node IDs … naming only, fix nothing.
The conductor surfaces the red-tree fact to Matt; his call needs names, not a count."*** Below is the
complete list. **I changed nothing in response to it and diagnosed nothing** — every module named
here is outside my seam.

### 8.1 The exact state it was measured on

```
command   python3 -m pytest tests/ --tb=no -q -p no:cacheprovider -rfE
tree      engine 81d16e6d  (= 97fb8f65 + 489a74ba repair bundle + 81d16e6d HB-5 banking)
          PLUS star-lord's HB-2 work, uncommitted in the shared working tree at run time:
            M src/reincarnated/export/baton_v1_emitter.py
            M src/reincarnated/export/baton_v1_schema.py
            M src/reincarnated/export/baton_v1_validator.py
            M tests/test_baton_v1.py
          (he committed them mid-run as 7e192537 + 3cb3bc2f; the run read the working tree)
result    63 failed, 10387 passed, 3 warnings, 21 errors in 1283.34s (0:21:23)
```

> ⚑ **A FIRST ATTEMPT WAS DISCARDED RATHER THAN REPORTED.** I started a full-tree run before making
> the repairs and edited source while it was mid-flight. Its numbers would have straddled two trees
> and been un-nameable, so I killed it and re-ran clean on a state I can write down. **A count from a
> tree I cannot name is not a measurement**, and HB-8's whole purpose is to produce names.

### 8.2 ⚑ THE A/B CONTROL — MY REPAIRS MOVED NOTHING

| | conductor's pre-repair run (L-71(i)) | this run, post-repair |
|---|---|---|
| failed | **63** | **63** |
| errors | **21** | **21** |
| passed | 10,373 | **10,387** |

**The failure and error counts are IDENTICAL, and `passed` moves by exactly +14 — the same +14 the
six-file smoke moves by, and for the same two reasons (+12 star-lord's baton tests, +2 my F-7 pair).
Both measurements close on the same arithmetic independently.** Corroborating structurally: **none
of the 13 failing modules contains a single reference to `kc2` or `monster_stats`** (checked
mechanically, 0/13). The red tree pre-dates this bundle and is untouched by it.

### 8.3 Where it is concentrated

```
  33  tests/test_cycle12_layer4_convergence.py          [F]
  21  tests/test_cycle13_wave5_season_generation.py     [E]  <- all 21 ERRORS are this one module
  12  tests/test_cycle12_layer6_t4_wireup.py            [F]
   4  tests/test_kit_space_emitter.py                   [F]
   4  tests/test_foundation.py                          [F]
   2  tests/test_wr2_d_nova_telegraph.py                [F]
   2  tests/test_substrate_identity_loader.py           [F]
   1  tests/test_wr1_m12_gd_mitigation_nova.py          [F]
   1  tests/test_wave5_swift_closure_path_x_phase4_feeds_phase5.py   [F]
   1  tests/test_no_canonical_four_in_llm_prompts.py    [F]
   1  tests/test_kit_space_skill_naming.py              [F]
   1  tests/test_dispatch_3b_phase5_seam1_pm1_gb.py     [F]
   1  tests/test_cycle13_normal_season_export.py        [F]
                                                        --
                                                        84  = 63 F + 21 E
```

**Three modules carry 66 of 84 (78.6 %), and all 21 errors are a single module** — which is a shape
fact worth putting in front of Matt beside the count, because "63 failures" and "three broken
modules" are very different decisions. ⚑ **`test_cycle12_layer4_convergence.py` is the CONVERGENCE
LOOP and its name will read as mine.** It is not: it is the cycle-12 layer-4 kit convergence gate
(rocket/generation lineage), it references neither `kc2` nor `monster_stats`, and its 33 failures
sit at 33 both before and after this bundle. **I am naming the near-miss because a conductor
scanning this list would be right to stop on that filename.**

### 8.4 The complete list — 84 node IDs, `F` = failed, `E` = error

```
F tests/test_cycle12_layer4_convergence.py::TestGate1ConvergenceResultShape::test_dataclass_fields_exist
F tests/test_cycle12_layer4_convergence.py::TestGate1ConvergenceResultShape::test_converged_bool
F tests/test_cycle12_layer4_convergence.py::TestGate1ConvergenceResultShape::test_iteration_count_int
F tests/test_cycle12_layer4_convergence.py::TestGate1ConvergenceResultShape::test_final_modifier_float
F tests/test_cycle12_layer4_convergence.py::TestGate1ConvergenceResultShape::test_per_dim_adjustments_dict
F tests/test_cycle12_layer4_convergence.py::TestGate1ConvergenceResultShape::test_to_dict_json_serializable
F tests/test_cycle12_layer4_convergence.py::TestGate1ConvergenceResultShape::test_from_dict_round_trip
F tests/test_cycle12_layer4_convergence.py::TestGate2PhaseFunctions::test_phase1_sp_voting_conserves_budget
F tests/test_cycle12_layer4_convergence.py::TestGate2PhaseFunctions::test_phase1_sp_per_node_within_cap
F tests/test_cycle12_layer4_convergence.py::TestGate2PhaseFunctions::test_phase1_returns_adjustment_dict
F tests/test_cycle12_layer4_convergence.py::TestGate2PhaseFunctions::test_phase2_t4_selection_returns_dict_and_changes
F tests/test_cycle12_layer4_convergence.py::TestGate2PhaseFunctions::test_phase3_trigger_selection_returns_dict_and_changes
F tests/test_cycle12_layer4_convergence.py::TestGate2PhaseFunctions::test_random_restart_sp_budget_conserved
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_converge_kit_returns_convergence_result
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_iteration_count_le_max_iterations
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_final_modifier_is_positive
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_converged_is_bool
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_per_dim_adjustments_has_required_keys
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_iterations_are_list_of_dicts
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_converged_kit_is_not_none
F tests/test_cycle12_layer4_convergence.py::TestGate3ConvergeKitShape::test_all_archetypes_converge_kit_runs
F tests/test_cycle12_layer4_convergence.py::TestGate4Determinism::test_determinism_5_reruns
F tests/test_cycle12_layer4_convergence.py::TestGate4Determinism::test_different_seeds_produce_different_results
F tests/test_cycle12_layer4_convergence.py::TestGate5ThirtyKitSmoke::test_30_kit_smoke_convergence_rate
F tests/test_cycle12_layer4_convergence.py::TestGate5ThirtyKitSmoke::test_30_kit_smoke_per_kit_wr_for_converged
F tests/test_cycle12_layer4_convergence.py::TestGate5ThirtyKitSmoke::test_mage_controller_regression
F tests/test_cycle12_layer4_convergence.py::TestGate6ResumeConvergence::test_resume_from_non_converged_result
F tests/test_cycle12_layer4_convergence.py::TestGate6ResumeConvergence::test_resume_from_converged_result_returns_as_is
F tests/test_cycle12_layer4_convergence.py::TestGate6ResumeConvergence::test_resume_merges_iteration_logs
F tests/test_cycle12_layer4_convergence.py::TestGate6ResumeConvergence::test_resume_total_iteration_count_is_cumulative
F tests/test_cycle12_layer4_convergence.py::TestGate7RoundTrip::test_converged_kit_round_trip
F tests/test_cycle12_layer4_convergence.py::TestGate7RoundTrip::test_cap_hit_round_trip
F tests/test_cycle12_layer4_convergence.py::TestGate7RoundTrip::test_round_trip_from_converge_kit_output
F tests/test_cycle12_layer6_t4_wireup.py::TestGate3SignatureChainElection::test_election_is_deterministic
F tests/test_cycle12_layer6_t4_wireup.py::TestGate3SignatureChainElection::test_election_returns_valid_chain_id
F tests/test_cycle12_layer6_t4_wireup.py::TestGate3SignatureChainElection::test_election_tie_break_favors_first_chain
F tests/test_cycle12_layer6_t4_wireup.py::TestGate3SignatureChainElection::test_election_sets_signature_chain_id_on_wire_up
F tests/test_cycle12_layer6_t4_wireup.py::TestGate3SignatureChainElection::test_election_validates_skill_tree_invariants
F tests/test_cycle12_layer6_t4_wireup.py::TestGate3SignatureChainElection::test_validate_invariants_catches_invalid_node_type
F tests/test_cycle12_layer6_t4_wireup.py::TestGate5IntegrationSmoke::test_wire_up_produces_no_exceptions_for_22_kits
F tests/test_cycle12_layer6_t4_wireup.py::TestGate5IntegrationSmoke::test_t4_alteration_output_is_dict_or_none
F tests/test_cycle12_layer6_t4_wireup.py::TestGate5IntegrationSmoke::test_signature_chain_id_is_set_after_wire_up
F tests/test_cycle12_layer6_t4_wireup.py::TestGate5IntegrationSmoke::test_altered_ctx_json_serializable
F tests/test_cycle12_layer6_t4_wireup.py::TestGate5IntegrationSmoke::test_no_regression_on_layer3_invariants
F tests/test_cycle12_layer6_t4_wireup.py::TestGate5IntegrationSmoke::test_round_trip_full_kit_json
F tests/test_cycle13_normal_season_export.py::TestRoundTrip::test_manifest_has_elements_block
F tests/test_dispatch_3b_phase5_seam1_pm1_gb.py::TestSmokeTest10Seasons::test_10_season_tiebreak_rate_under_20pct
F tests/test_foundation.py::TestConfigLoading::test_has_five_elements
F tests/test_foundation.py::TestConfigLoading::test_rotating_elements_are_canonical_substrates
F tests/test_foundation.py::TestConfigLoading::test_element_color_ranges_non_overlapping
F tests/test_foundation.py::TestFoundationValidation::test_validator_accepts_7_substrate_elements
F tests/test_kit_space_emitter.py::TestMultiKitEmit::test_all_kits_written
F tests/test_kit_space_emitter.py::TestMultiKitEmit::test_chronicle_event_kit_ids_match_files
F tests/test_kit_space_emitter.py::TestMultiKitEmit::test_kits_index_has_all_kit_ids
F tests/test_kit_space_emitter.py::TestMultiKitEmit::test_per_kit_json_files_exist
F tests/test_kit_space_skill_naming.py::TestOutputSchemaValidity::test_flavor_false_implies_flavor_word_null
F tests/test_no_canonical_four_in_llm_prompts.py::TestMonsterNamingNoCanonicaFour::test_all_elements_monsters
F tests/test_substrate_identity_loader.py::TestFoundationIntegration::test_rotating_elements_count_is_four
F tests/test_substrate_identity_loader.py::TestFoundationIntegration::test_load_foundation_still_passes_element_count
F tests/test_wave5_swift_closure_path_x_phase4_feeds_phase5.py::TestBackwardCompatPhase5EntryPoints::test_run_phase5_cohesion_judge_accepts_path_x_pm1_result_in_smoke
F tests/test_wr1_m12_gd_mitigation_nova.py::test_INTEGRATION_the_nova_fires_telegraphs_and_lands_a_death2_class_blow
F tests/test_wr2_d_nova_telegraph.py::test_the_minted_telegraph_carries_the_DERIVED_duration_under_the_arm
F tests/test_wr2_d_nova_telegraph.py::test_the_minted_telegraph_carries_the_MEASURED_0_750_off_the_arm_H_M2_f
E tests/test_cycle13_wave5_season_generation.py::TestW5R2GauntletSimIntegration::test_all_kits_receive_wr_bracket_result
E tests/test_cycle13_wave5_season_generation.py::TestW5R2GauntletSimIntegration::test_passing_kits_is_subset_of_all
E tests/test_cycle13_wave5_season_generation.py::TestW5R2GauntletSimIntegration::test_q10_substrate_led_emission
E tests/test_cycle13_wave5_season_generation.py::TestW5R2GauntletSimIntegration::test_gauntlet_result_returned
E tests/test_cycle13_wave5_season_generation.py::TestW5R2GauntletSimIntegration::test_smoke_mode_produces_passing_kits
E tests/test_cycle13_wave5_season_generation.py::TestW5R2GauntletSimIntegration::test_gauntlet_result_counts_consistent
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_season_metadata_written
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_season_metadata_fields
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_season_metadata_kit_count
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_characters_directory_created
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_gear_sets_directory_created
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_character_files_written
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_gear_set_files_written
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_principle_6_round_trip_pass
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_character_json_required_fields
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_character_json_wr_bracket_pass_true
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_character_json_bc_tuple_complete
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_sim_cycling_quality_report_written
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_wr_bracket_pass_rate_consistent
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_pass_plus_fail_equals_total
E tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring::test_authoring_summary_matches_metadata
```

### 8.5 What I am NOT saying

**No diagnosis, no triage, no severity.** `--tb=no` was used deliberately — the commission asked for
names, and a traceback-carrying run would have invited me to start fixing things in three other
agents' seams. **The one substantive observation I will offer**, because it is free from the names
alone: `test_foundation.py::test_has_five_elements` /
`test_rotating_elements_count_is_four` /
`test_validator_accepts_7_substrate_elements` are asserting **five**, **four** and **seven** element
counts in the same tree. That is a shape a conductor can route on without anyone reading a
traceback. **Routing is the conductor's, not mine.**

---

## 9. Sitrep

The finding I was sent to fix said one number was wrong. The number was wrong, and so were five
others sitting beside it, for the same reason and in the same direction — and the only reason I
found them is that jack-ryan's own note told me the mechanism, and a mechanism is a hypothesis about
a population. I have written that sentence into other people's work often enough that it was
uncomfortable to be on the receiving end of it, which is probably the correct amount of discomfort.

Two things this lap taught me that the findings did not contain.

The first is that a value can be right and still be wrong to read. The floor-set widths — 454 and
235 and 6 — are correct, and I have spent this lap correcting things that quote them, because I wrote
them down for one population and then used them for another two sections later. Nobody's arithmetic
failed. A phrase covered two objects and I never noticed I had stopped meaning the first one.

The second is that my own sweep table omitted the file it was printed in, and production code in my
own seam that I had edited that same hour. Not because I curated — because I looked at the output
and saw the interesting rows. That is what curation is when you do it without deciding to. Clause 5
does not say "do not curate"; it says paste the output, and the reason is that the sweep does not
know which rows I find interesting.

And then I did it again. My first draft of the repair for that finding counted ten un-rowed surfaces
and there are eleven — I had rowed the fold's return note under one sweep and not the other, which
is the same file and the same blindness one level down. It was caught by diffing the tool's file set
against my table in code, thirty seconds of work I only did because I had just finished writing a
paragraph about why reading is not checking. I do not think I would have caught it by reading it a
third time. That is the part worth keeping: the discipline is not "be more careful," it is "make the
check mechanical," and I needed to be told that twice in one lap by two different instruments.

The bracket was overstated, so the residual looked worse than it is and nothing downstream broke.
That is luck presented as a mitigation. What actually protected the run was that the board — the
thing anybody could re-derive — was correct, and the only casualties were sentences about it. The
board was checked by an instrument. The sentences were checked by me.

---

*Filed 2026-08-08 by gamora under KC2-SIM ledger L-71(g) (gandalf, RUN-CONDUCTOR), repairing Gate-2
verdict L-70 (jack-ryan). Read-only against every vendor tree; zero external fetches; no writes to
telemetry or `export/`. Committed in both repos; **NEITHER REPO PUSHED** — the conductor centralises
under R-KC2-10.*
