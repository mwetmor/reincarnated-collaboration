# Gate-2 (DEV-MODE) — KC2-SIM Phase D — 2026-08-08

**Reviewer:** jack-ryan (BLOCK authority)
**Commission:** gandalf `RUN-CONDUCTOR`, KC2-SIM Phase-D fold (ledger **L-38**); Limb 2 fires under
**desirable-run-pattern standing safety #2** (independent Gate-2 on in-run reclassifications — the
conductor may not self-clear).
**Predecessor:** `jack-ryan/notes/2026-08-08-kc2-gate2-phase-c.md` §§ 1–8 (re-read before this pass).
**Targets:** engine `~/Games/reincarnated-engine` @ `0474ca1d` + `2b562474` atop `bae60ce6`,
branch `main`, **UNPUSHED** · spec § 14 F-10 block + ledger L-38(g) · six conductor spec annotations.
**Commit state:** this note only, in the meta-repo. **No engine write. No push anywhere.**

---

## VERDICTS

| Limb | Verdict |
|---|---|
| **1 — gamora G-D wiring re-lap** (engine code) | **PASS-with-findings** — 0 BLOCK · 1 WARN · 1 INFO |
| **2 — F-10 reclassification** | **MODIFIED** — disposition **UPHELD**; empirical leg **RE-GRADED**; one documentary sentence corrected |
| **3 — small items** | census answered (**635 is the operative denominator**); drift check **4 clean / 1 mischaracterized / 2 missed siblings** |

**No BLOCK is open.** The F-10 disposition stands and I would not reverse it — but its published
text over-claims one of its three legs, and a Gate-B-class finding is exactly where an over-claimed
leg does the most damage later.

---

# LIMB 1 — gamora's G-D wiring re-lap

**Verdict: PASS-with-findings.** Every load-bearing evidentiary claim in her §§ 8.4 / 12.1 / 16.3 /
17 / 18 reproduced on my own instruments, most of them off the CSVs rather than through her code.

## § 1.1 — Independently measured, not accepted

| # | Claim | My method | Result |
|---|---|---|---|
| 1 | Law-flip moves exactly 2 of 25 array fields at fighting-160 | swept all 25 fields, label 159 vs 160, `halt9_survival_wave_scaling_full.csv` | **2/25** — `characterLifeModifier` 322→324 (**+0.621 %**) · `characterDefensiveAbility` 66→67 (**+1.515 %**) ✓ |
| 2 | Counts BIT-IDENTICAL under both laws | distinct `(spawnChampionMinAdj, spawnChampionMaxAdj)` over labels 149–170 | **one pair, `('1','1')`** → count model provably flip-invariant ✓ |
| 3 | FoA wall binds fighting 171; law total on [1,200] | labels 170/171/172 = 344/420/430; label 1 = 95; label 200 = 990 / +130 | ✓ all |
| 4 | Chain 8/8 EXACT @ G=324 | **my own four-link implementation** off `t21…r2.csv` (`base_life`, `armorbase_pct`), floor | **8/8 EXACT, residual 0** ✓ |
| 5 | Inverted guards score as declared | same instrument | **G=322 → 0/8** (−0.177 / −0.179 / −0.181 %) · **round → 3/8** · **multiplicative → 0/8** ✓ |
| 6 | § 6.2b phase-row predicate agreement | record-name predicate vs `spawn_source` | **3 rows, SET-EQUAL** ✓ |
| 7 | Exclusion hazard 2,967,411 eHP = 21.2 % | summed the 3 excluded rows | **2,967,411** = **21.2 %** of 13,981,477 ✓ |
| 8 | Registry 635 / DB-CITED 511 / TPL-DEFAULT 124 / 74 exempt | `exemption_registry()` census | ✓ exact; sole non-boss exempt = `celestialmonstrosity_t3.dbr` ✓ |
| 9 | `gdx1` path defect now raises | called both paths | `gdx1` → **KeyError** ✓; `gdx2` → `Cited(False, TPL-DEFAULT)` ✓; retired `IGNORE_GAME_BALANCE` **absent** ✓ |
| 10 | Three SHA pins match on-disk | `shasum -a 256` ×3 + `BOARD_CSV_SHA256` | ✓ `ddfc81ca…` / `40182de2…` / `bbdc81f1…` |
| 11 | Vendored sidecars byte-true to legolas scratch | `cmp` ×2 | **IDENTICAL** ✓ |
| 12 | F-9 parameter + `<unrostered>` guard | `roll_wave(160, …, empty_roster_plus_one=True)` sweep | `<unrostered>` **reachable at seed 0** ✓; default disposition `NO_OP_ON_EMPTY` ✓ |
| 13 | 117 distinct pools / 621 alternative rows | independent count off v2 | **117** distinct empty-regular-roster pools of 635 ✓ |
| 14 | `VALID_GRADES` growth + same-commit AST census | diff vs `bae60ce6` | **7 → 8**, the addition is exactly `TPL-DEFAULT`; census file ships in `0474ca1d`, 4 cells, green ✓ |
| 15 | Blast radius 291 P / 0 F | ran her declared 12 files | **291 passed / 0 failed** ✓ |
| 16 | `kubacabra_phase_chain` REMOVED not edited | `hasattr` | **absent**; `kubacabra_crucible_phases()` → `(2955796,)` ✓ |

**Suite adjudication is not mine** (her § 16.3; conductor's at G-D close). Not blocked on.

## § 1.2 — WARN

### **D-W1 — the shipped p06 provenance asserts a ruling the run has superseded**

**Severity: WARN.** **Traces to:** L-37(b) · F-10 disposition · Discipline #12 (declare semantic
shifts) · my own Phase-C **G-W2**, of which this is a recurrence.

```
count_model_provenance()["p06_state"]
  → "DEMOTED-OPEN (L-33(g)) — both limbs carried; parameter, not a default"

tests/test_kc2_opposition_wave_engine.py:840
  def test_p06_fixture_state_is_DEMOTED_OPEN_and_both_limbs_are_carried(...)
```

L-37(b) **RULED p06 OFF** for the specified run (MEASURED-NULL, positive-controlled), and F-10's
own disposition names **p06-OFF as operative**. The engine ships `DEMOTED-OPEN` and pins it in a
test whose name asserts it.

**Cause is benign** — her lap and L-37 were concurrent, and her § 14 declares the state honestly as
of her write. The finding is that the surface which **rides into baton provenance** now carries a
superseded ruling, so its failure mode is silent at the gate that consumes it. That is the same
property that made G-W1 my one Phase-C carry-forward.

**Action — developer:** re-scope the constant and the test to *"RULED OFF for the specified run
(L-37(b), veto-open); ON limb carried informative"*, keeping both limbs and the parameter. Two
strings and a test name.

## § 1.3 — INFO

**D-I1 — the KC2 test count is 101, not 102.** Collected, per file, at `2b562474`:

```
test_kc2_opposition_wave_engine   43   (report says 44)      test_kc2_run_surfaces      14  ✓
test_kc2_energy_devotion          19   ✓                     test_kc2_channel_disc      21  ✓
test_kc2_grade_vocabulary_census   4   ✓                     test_telegraph_value_set    3  ✓
                                       KC2 five files = 101   (+ telegraph census = 104)
```

Her **104 total is right**; the component `44` and the derived `102` are each one high, and her
`2b562474` commit message's own component list sums to **105 ≠ its stated 104**. Baseline at
`bae60ce6` is 78, so the growth is **78 → 101 (+23)**. Propagated into **ledger L-38(a)**
("KC2 tests 78→102"). Non-material; same class as the Phase-C "15 vs 19 assertions" corrigendum,
which was mine.

## § 1.4 — The positive record

- **The G-B1 lesson was applied prospectively, unprompted** — blast radius derived by **grep on
  every touched name**, not by file list (her § 16). This is the exact remedy § 2 of my Phase-C
  note prescribed, generalised by her without being told to.
- **The L-36 census discipline was honoured on the enum SHE grew** — `VALID_GRADES` +`TPL-DEFAULT`
  ships with its census **in the same commit**, and the completeness cell is **AST, not grep**,
  because the grep form went red on a prose cross-reference. That is the `test_adr_006` pattern
  correctly transferred.
- **She made a passing AC fail by citation and pinned it as a miss.** AC-10.4's p06-OFF limb was
  *inside* the band as built (286.83) and is *outside* it under citation (271.50). The seam that
  gains nothing from this reported it, tested it under a name that says so, and **declined the
  branch that lands** (§ 12.1). On charter § 4.2 — the run's hardest rule — this is the strongest
  single act in the unit.
- **Two self-caught defects reported up rather than quietly fixed:** the `poolsbossgdx1→gdx2` path
  defect (inert on counts, **live on provenance** — precisely the failure mode G-W4 named), and the
  117-vs-621 provenance-count ambiguity.
- **All six of my Phase-C findings are discharged** (G-W1 ×3 SHA pins · G-W2 · G-W3 as tests ·
  G-W4 as a graded registry · S-W1 split · G-I3 · G-I5..G-I8).

---

# LIMB 2 — F-10 reclassification review (standing safety #2)

> ## **VERDICT: MODIFIED.**
> **The disposition is UPHELD and I would not reverse it.** The DOCUMENTARY and ARITHMETIC legs
> hold under independent re-derivation. **The EMPIRICAL leg does not: the wave-160 camera
> observation is VACUOUS for F-9 under the operative p06-OFF limb**, and must be re-graded from
> *CONFIRMED-ON-CAMERA* to *not discriminated*. One sentence of the documentary leg is
> arithmetically false — correcting it **strengthens** the ruling but exposes a pre-existing spec
> inconsistency that a future re-pin will regenerate.

## § 2.1 — DOCUMENTARY leg — **UPHELD on its core; one sentence CORRECTED; stronger support found**

**(a) Core claim VERIFIED.** Spec § 10.5 line 980 draws, verbatim:

```
regulars  = randint(n_min, n_max)
champions = randint(c_min, c_max) if rand() < pool.championChance/100 else 0
```

No roster term anywhere in the branch. ✓

**(b) I found a stronger documentary item than the ruling cites, and it is in the pin's OWN
source.** U-9 § 4.3 — the note that published 292.0 — states its method verbatim:

> *"Applying A/floor with clamp across all **558 non-exempt pools**"*  (558 = 632 − 74)

A **pool-level sweep with no roster join**, from the computation itself rather than from a
restatement of the model. **Recommend the conductor cite it**; it is the best documentary evidence
available for reading (i) and it was not used.

**(c) CORRECTION — the sentence *"the only roster-awareness at pin time was the U9-8 hero-pool
edge"* is arithmetically false as applied to the pins.**

The U9-8 edge (§ 10.4: hero pools carry no regular roster ⇒ zero regulars) covers **95 of the 117**
empty-roster pools. The other 22 are **DEVOTION (15) and BOUNTY (7)**. In the band 151–170 the
split is **HERO 26 / DEVOTION 15 / BOUNTY 6 = 47**. Measured on my own instrument:

```
cited  ×  U9-8 hero-only carve-out   →   280.50 / 301.17     vs pins 292.0 / 316.5   (−11.50 / −15.33)
cited  ×  fully roster-blind (+1)    →   292.50 / 317.17                             (+0.50 / +0.67)
```

**If the U9-8 edge had been applied to the pinned totals, the pins would read 280.50 / 301.17.**
They do not. So the edge was **declared in § 10.4 prose and never carried into the pinned numbers**
— the pin-era model was roster-blind *full stop*, not roster-blind-except-heroes.

This **strengthens** the ruling: fully-roster-blind is exactly the config that lands. But it
records a **pre-existing § 10.4 ↔ § 10.5 internal inconsistency at pin time**, independent of the
117-pool discovery. **This must be carried**, because F-10's re-open clause permits re-derived pins
at a future pre-registration point, and unless § 10.4's U9-8 edge is reconciled with whatever model
produces the new pins, the same inconsistency regenerates.

**(d) The "would confront" argument is the weakest sub-claim.** It infers pin-era intent from F-9's
authorial framing, not from a trace of the computation. Grade it **CORROBORATIVE** and let (a)+(b)
carry the leg — they are sufficient without it.

**(e) Positive, and it belongs on the record.** gamora's implementation makes U9-8 a **special
case** of F-9's no-op (`roster_n == 0` ⇒ zero regulars, hero pools included), so § 10.4's edge is
honoured **in code for the first time**. Her `count_bounds` docstring already says so.

## § 2.2 — ARITHMETIC leg — **UPHELD; "unique fit" needs one qualifier; the fit is near-exact, not exact**

Re-run on an instrument that reads the CSVs only and **imports nothing from `reincarnated`**
(`/tmp/jr-kc2/lattice.py`). Every cell reproduces:

| exemption | empty-disposition | reg OFF | reg ON | ch OFF | ch ON | Δ(292.0) | Δ(316.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| none | no-op | 290.83 | 310.83 | 63.00 | 81.00 | −1.17 | −5.67 |
| none | +1 | 311.83 | 337.83 | 63.00 | 81.00 | +19.83 | +21.33 |
| 6-override | no-op | 286.83 | 306.83 | 63.00 | 81.00 | −5.17 | −9.67 |
| 6-override | +1 | 307.83 | 333.83 | 63.00 | 81.00 | +15.83 | +17.33 |
| **cited** | **no-op** | **271.50** | **290.17** | **63.00** | **81.00** | **−20.50** | **−26.33** |
| **cited** | **+1** | **292.50** | **317.17** | **63.00** | **81.00** | **+0.50** | **+0.67** |

- Champions **63.00 / 81.00 invariant across all six cells** ✓ (structural, as claimed).
- Exemption band effect **−19.33 / −20.67** → reproduces L-35(c)'s "≈ 20.7" ✓.
- Empty-disposition band effect **+21.00 / +27.00** → **reproduces F-9's registered ≈ 27.0 exactly** ✓.
- Per-limb tracking (OFF +21.00 vs miss 20.50; ON +27.00 vs 26.33) ✓.

**QUALIFIER — "only cited/+1 lands" is true on the 6-cell lattice as drawn.** Extend the
empty-disposition axis to the U9-8 carve-out **the documentary leg itself names**, and **2 of 12
cells land inside T-2 on both limbs**: `cited/+1` (+0.50/+0.67) and **`6-override/hero-only`
(+3.83/+1.33)**. The second is not a live rival — the 6-entry override is a Phase-C *sim* artifact
postdating the pins, and it fails the per-limb-tracking test (+9.00/+11.00 against misses of
5.17/9.67). **So the discrimination survives — but it is carried by per-limb tracking plus
historical availability of the exemption config, not by "landing" alone.** Landing alone is a
2-of-12 criterion and the ruling should say which sub-criterion is load-bearing.

**RESIDUAL — structured, not noise, and not explained.** +0.50 (OFF) and +0.67 (ON) are exact
weighted-mixture quanta (½; ½ + ⅙), not rounding. I ruled out the obvious cause: the POP-A/POP-B
population delta **does not reach the band** — none of the 7 differing pools appears in 151–170,
and `legendary_override` is `False` on all **265** band rows. So one or two alternative rows still
differ by one body between U-9's sweep and the v2 emission. **Not verdict-moving** (the nearest
rival is 40× further away), but *"unique fit"* should not be read as an exact reconstruction.
**Recommend the residual be named rather than absorbed into "sub-0.25 %".**

## § 2.3 — EMPIRICAL leg — **REJECTED AS GRADED. The wave-160 observation is vacuous for F-9.**

Measured on the v2 emission:

```
wave 160, ALL alternatives                                   6 rows
  non-exempt with EMPTY regular roster                       1 row   ← spawn point 6
  non-exempt with EMPTY regular roster on points 1-5         0 rows
```

**p06 is RULED OFF (L-37(b)) and F-10 names p06-OFF as operative.** Therefore, under the model of
record, **wave 160 contains no empty-roster pool for the `+1` to land on.** `NO_OP_ON_EMPTY`,
`CONJURE_FROM_TEMPLATE` and `PROMOTE_TO_CHAMPION_DRAW` all predict **the same wave-160 cohort**.
The observation has **zero likelihood ratio**; it cannot confirm no-op.

Read the other way it is **circular**: the same "zero stars / zero hero-band readouts" frame is the
evidence that ruled p06 OFF in the first place (L-37(b)). One observation cannot both establish
p06-OFF *and*, conditional on p06-ON, discriminate F-9's branches.

**The discriminating test exists, is deterministic, and was not run.** Ten of the twenty band waves
carry non-exempt empty-roster alternatives on points 1–5. Expected extra un-rostered bodies under
`CONJURE` vs `NO_OP`, p06-OFF — **integer, weight-1 picks, not probabilistic**:

```
w151  2.00  |  w152  3.00  |  w153  2.00  |  w157  2.00  |  w158  2.00     <- ALL IN FOOTAGE
w161  2.00  |  w162  2.00  |  w163  2.00  |  w167  2.00  |  w168  2.00
                                                    band total  21.00  (closes against the lattice)
```

**Wave 152 predicts exactly three extra un-rostered trash bodies under CONJURE and zero under
NO_OP, deterministically, inside the extracted s2 window.** That is the footage limb F-9's own
resolution path named, and it is cheap.

**Re-grades required:**
- F-9 status: *"No-op-on-empty **CONFIRMED-ON-CAMERA**"* → *"**NOT DISCRIMINATED ON CAMERA** — the
  wave read carries no empty-roster pool under the operative p06-OFF limb; the discriminating waves
  (151 / 152 / 153 / 157 / 158) are in-footage and unread."*
- F-10 empirical leg → **CORROBORATION NOT AVAILABLE** (not *contradicted* — simply silent).
- F-10 re-open condition currently reads *"the `proxypool` template fine-print contradicting the
  camera."* Since the camera does not speak to this, widen it to: *"the template fine-print **or** a
  galadriel count pass on any of waves 151/152/153/157/158."*

## § 2.4 — Why the disposition survives on two legs

| F-10 claim | Rests on | Survives? |
|---|---|---|
| Pins 292.0 / 316.5 → **SUPERSEDED-PROVENANCE** | documentary + arithmetic | **YES** |
| Count model of record = **CITED + no-op**, p06-OFF 271.50 / 63.00 | **F-9's pre-registration** (charter § 4.2) | **YES** — and more cleanly |
| Misses stay pinned AS named misses | § 4.2 + L-32(b) fallback posture | **YES**, untouched |
| `+1` stays an un-adopted parameter | § 4.2 | **YES**, untouched |

The second row is the important one. **Pre-registration governs regardless of the camera** — you do
not switch branches because one lands, and you do not need the camera to say so. The current text
lets *"confirmed on camera"* do work that pre-registration is already doing; removing the
over-claim leaves the finding standing on **more durable** ground, not less. That is why this is
MODIFIED and not REJECTED.

**Charter § 4.2 read adversarially, as at Phase C: HELD.** Nothing was fitted. The seam that would
have benefited from adopting the `+1` refused it, and the conductor's ruling *reclassifies the pins
rather than moving the model toward them* — which is the correct direction and the whole point of
the Gate-B event class.

---

# LIMB 3 — small items

## § 3.1 (a) — The 632 vs 635 census delta: **635 is the operative denominator**

**The axis is the DIFFICULTY SLOT, not row-count vs distinct-pool-count.** And the reconciliation
was **already published in the adopted E-2 probe note** (`legolas/notes/2026-08-08-kc2-e2-exemption-probe.md`
§ 2.1, adopted at L-35) — this was a citation-lookup miss, not an open question:

| population | definition | n | IGB = 1 |
|---|---|---:|---:|
| **POP-A** | pools reachable via base `pool{i}` (U-9's `q5` sweep) | **632** | **74** |
| **POP-B** | **Gladiator view** — `poolLegendary{i}` where declared, else `pool{i}` | **635** | **74** |
| POP-C | union of `pool` ∪ `poolEpic` ∪ `poolLegendary` | 637 | 74 |

`B \ A` = 5 pools, `A \ B` = 2 pools, `A ⊂ C`. **The numerator is 74 in all three**, so no
arithmetic anywhere moves on the choice.

Independently confirmed: the v2 emission and the sidecar each carry **exactly 635 distinct
`pool_record` values**, casefold collisions **0**. And the choice is **immaterial to the band** —
none of the 7 differing pools appears in waves 151–170.

**Disposition.** § 10.5 fact 3 cites POP-A (`74/632`) inside a **Gladiator** count model whose own
binding (§ 10.4) is *"`poolLegendary` = Gladiator"*. **The operative denominator is 635.** One-line
fix, and it should be applied to all three sibling addresses together:

- § 10.5 fact 3 — `74/632` → `74/635 (Gladiator view; 74/632 on the base-pool population — POP-A/POP-B, E-2 probe § 2.1; numerator 74 in all three)`
- § 10.4 — *"925 spawn proxies → 632 pools"* (POP-A, correct as a proxy-graph statement — scope it)
- § 10.5 — *"All 632 Crucible pools reference the identity `proxypoolequation_01.dbr`"* (same)

## § 3.2 (b) — Drift check on the six conductor annotations

Method: `git diff HEAD` on the spec (tracked; dirty since the G-C close at `135dfa8a`). Diff is
**+104 / −12**; I read every deletion.

| # | Annotation | Class | Verdict |
|---|---|---|---|
| 1 | § 6.2b level-law **DISCRIMINATED** | old reading `~~struck~~`, new law + L-37(a) lineage appended | **CLEAN** |
| 2 | § 10.5 **U9-6 RULED-OFF** | full lineage chain `~~RESOLVED: p06 is ON (L-21)~~ → DEMOTED-OPEN → RULED OFF`; superseded 5th-body identification struck with superseding parenthetical | **CLEAN — exemplary** |
| 3 | AC-10.4 **F-10 annotation** | appended parenthetical; prior text intact | **CLEAN** |
| 4 | § 12 **T-2 denominator** | appended parenthetical; original *"1.9 % (5.5 monsters on 292…)"* retained verbatim | **CLEAN** |
| 5 | § 14 **F-9 status + F-10 blocks** | pure addition | **CLEAN** |
| 6 | AC-6.5 **×5.746 restatement** | lineage preserved by verbatim quotation + diagnosis — **not** a silent rewrite — but the **guard's stated predicate changed** | ⚑ **WARN — mischaracterized** |

### **D-W2 — AC-6.5's guard predicate was restated, and L-38(e) says it was not**

**Severity: WARN.** Pre-fold, the additive-M guard's published predicate was the **ratio**:

```
tests/…  spec line 588 @ 135dfa8a:
  - **Additive-M guard** — a multiplicative composition overshoots ×2.9 (M 28.83 vs 10.02);
```

`0/8` was published **only for the G-index guard** (pre-fold line 591). Post-fold the additive-M
guard reads *"every multiplicative composition scores **0/8**"*. That is a **predicate promotion
from ratio-form to score-form**, and L-38(e)'s *"the BINDING predicate (multiplicative scores 0/8)
untouched and unambiguous throughout"* is not true of the spec text.

It is the **right** predicate — a ratio is not a falsification criterion — and gamora's test pins
all three ratios plus the spec's own `28.832` literal, so nothing is silently pickable. **Action:**
one clause, annotating that the guard's predicate was *also* restated at this fold, not only its
descriptive figure.

### **D-W3 — two missed siblings: the fold annotated the named address and left the same claim elsewhere**

**Severity: WARN.** **Traces to:** Discipline #2 (blast radius) · my Phase-C **§ 2** finding, transposed.

**(i) § 12 T-3 is STALE and contradicts this fold** — spec line 2016, unchanged:

```
| **T-3** | count model — **U9-6 bonus spawn** | **RESOLVED: p06 = ON, measured** (L-21 census)
  | branch RETIRED — counts run the p06-on table | **closed**, no tolerance carried |
```

Its own table-neighbour **T-2 was annotated at this fold**; T-3 — the row that *carries* the p06
ruling and instructs consumers to *"run the p06-on table"* — was not. It directly contradicts
§ 10.5 line 1022 and AC-10.4's OFF-MEASURED, **both edited this same fold**. This is a live
instruction to a consumer that is now wrong.

**(ii) § 6.2b line 534 carries the un-annotated ×2.9** — *"Multiplicative composition still
overshoots ×2.9 (structural guard retained)"* — **three lines below** the same bullet's freshly
corrected `G = 324` text, and 66 lines above the C-1 restatement that rules that very figure a
mixed-chain artifact.

*(Lines 2216 / 2239 also carry `×2.9` and *"reads label-159's 322"*, but sit inside an explicitly
superseded record blockquote — 2239 says so in terms. **Clean.**)*

**The pattern is worth naming.** Both misses are the **G-B1 failure mode transposed onto the spec**:
blast radius derived as an **address list** rather than by **grep on the moved claim**. gamora
applied the grep-derived radius prospectively to code this lap (her § 16) — the spec fold did not.
`grep -n "×2\.9\|p06 = ON"` closes both in one pass.

**(iii) Cosmetic, INFO:** in annotation 1 the bold markers were dropped inside the struck text, so
the strike is not byte-identical to the text it supersedes. No predicate moves. Recorded only
because strike-with-lineage is worth the strictest reading available.

---

## § 4 — Action list

| # | Sev | Owner | Action |
|---|---|---|---|
| **D-W1** | WARN | gamora | Re-scope `count_model_provenance()["p06_state"]` + `test_p06_fixture_state_…` to **RULED OFF for the specified run (L-37(b))**; keep both limbs and the parameter. |
| **F-10-E** | WARN | conductor | Re-grade F-9's status *CONFIRMED-ON-CAMERA* → **not discriminated**; F-10's empirical leg → **corroboration not available**; widen the re-open condition to include a galadriel count pass on w151/152/153/157/158. |
| **F-10-D** | WARN | conductor | Correct *"the only roster-awareness at pin time was the U9-8 hero-pool edge"* (applying it gives 280.50/301.17, not the pins); cite **U-9 § 4.3's "all 558 non-exempt pools"**; record the § 10.4 ↔ § 10.5 pin-time inconsistency against the re-pin clause. |
| **F-10-A** | INFO | conductor | Qualify *"unique fit"* — 2 of 12 cells land once the U9-8 axis is drawn; the load is carried by **per-limb tracking + historical availability**. Name the **+0.50 / +0.67** residual as structured and unexplained rather than absorbing it into "sub-0.25 %". |
| **D-W2** | WARN | conductor | One clause on AC-6.5: the **guard's predicate** was restated (ratio-form → score-form), not only its descriptive figure. |
| **D-W3** | WARN | conductor | Annotate **§ 12 T-3** (still "p06 = ON … counts run the p06-on table") and **§ 6.2b line 534** (un-annotated ×2.9). Derive the next fold's spec radius by grep, not address list. |
| **L3a** | INFO | conductor | § 10.5 fact 3 `74/632` → `74/635` (POP-B, Gladiator) with the POP-A scope named; apply to the § 10.4 and § 10.5 sibling addresses together. Answer was already in the adopted E-2 probe § 2.1. |
| **D-I1** | INFO | conductor | KC2 count of record is **101** (78 → 101, +23); `opposition_wave_engine` is **43**, not 44. L-38(a)'s "78→102" and gamora's § 14/§ 16 carry the +1. |

**ADR-002 tiering.** Limb 1 is within-seam engine work with no cross-seam schema change — my tier,
**no Matt escalation required**. **Limb 2 is not mine to close.** F-10 re-grades a
pre-registered acceptance criterion on a Gate-B-class event; the ledger already lists it as a
**Matt surface, veto-open**, and my MODIFIED verdict adds two text corrections to that same
surface. It rides the G-D close to Matt as planned — I am not blocking it, and no BLOCK is open.

**Re-review scope on resubmission:** none required. D-W1 is a two-string fix inside gamora's tier;
the F-10 re-grades are the conductor's text, not code, and I do not need to see them again unless
the empirical leg is defended rather than re-graded — in which case I would want the wave-152 count.

---

**Signed:** jack-ryan, Gate-2 DEV-MODE, KC2-SIM Phase D, 2026-08-08.

*The build is the cleanest of the run: she generalised her own BLOCK into a prospective discipline,
grew an enum and fenced it in the same commit, and refused a branch that would have closed two
failing gates. The reclassification reaches the right answer on two good legs and one that does not
hold — and the leg that does not hold is the one the ruling did not need. Take the camera out of
F-10 and it stands on pre-registration, which is where it was always strongest.*
