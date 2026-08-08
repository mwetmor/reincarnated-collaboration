# KC2-SIM Phase D beat 1 — the G-D wiring re-lap (gamora seam)

**Run:** KC2-SIM (autonomous, desirable-run pattern). **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Author:** gamora (simulation seam). **Phase:** D — calibrate, beat 1 (pre-registered FIRST).
**Base:** engine `main` @ `bae60ce6`. **Commits:** **`0474ca1d`** (the lap) + **`2b562474`**
(a self-caught provenance-count split, § 12.2) — engine `main`, **both UNPUSHED**.
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/kc2-gd-wiring-relap-2026-08-08.md`.
**Companion note corrected IN PLACE** (§ D.3a precedent, at section scale):
`…/math/kc2-mechanism-stack-2026-08-08.md` §§ D.3b · E-header · F.1 · F.2a · F.4a · F.5 · E.5.
**This report is UNCOMMITTED** per charter § 4.7 — the conductor commits at gate close.

**Status: COMPLETE.** All 13 register items executed. **Two ACs that passed at `bae60ce6` now MISS
and are pinned AS MISSES** (AC-10.4 both regular limbs) — reported, not tuned. Three items are
raised under **CONFLICTS** for conductor adjudication; none blocked the lap.

> ### The one-paragraph version
> The array-lookup law inverted, which re-interprets every array read in the `enemies0{1,2,3}`
> family and moves opposition HP +0.62 %. The eHP chain now closes **8/8 camera-named bodies at
> residual 0**. The exemption citation landed and moved the AC-10.4 band totals by ~20 bodies on
> each limb — **both now miss**, and the branch that would close them (F-9's `+1`-on-empty) lands
> at Δ +0.50 / +0.67 against the pins, which is exactly why I did not take it.

---

## § 0 — Register execution table (jack-ryan: this is the Gate-2 index)

| # | Register item | State | Evidence § |
|---|---|---|---|
| 1 | `ArrayLookupLaw` label-flip; re-derive every array consumption | **DONE** | § 1, § 2 |
| 2 | AC-10.5 322 → 324 + inverted guards | **DONE** | § 3 |
| 3 | Re-print every balancingadjustment-derived value (before/after) | **DONE** | § 2 |
| 4 | Consume r2 with the § 6.2b phase-row exclusion | **DONE** | § 4 |
| 5 | **G-W1** t20-values loader grade + vendored-SHA pin | **DONE** | § 5 |
| 6 | **G-W2** kubacabra single-phase re-scope | **DONE** | § 6 |
| 7 | **G-W3** AC-6.x tests-or-regrade | **DONE (tests)** | § 7 |
| 8 | **G-W4** Cited-graded exemption entries; consume the SHA-pinned sidecars | **DONE** | § 8 |
| 9 | **S-W1** § 9.5 one-line split (my side only) | **DONE** | § 9 |
| 10 | **G-I3** math-note § D.3 currency | **DONE** | § 10 |
| 11 | **F-8** corrected drain row consumed; grade DB-CITED | **DONE** | § 11 |
| 12 | **F-9** no-op-on-empty declared explicitly in the wiring | **DONE** | § 12 |
| 13 | **G-I5..G-I8** census-file cosmetics | **DONE** | § 13 |
| — | AC-10.4 re-evaluation BY CITATION (standing rule) | **DONE — both limbs MISS** | § 8.4 |
| — | p06 NOT resolved (DEMOTED-OPEN, galadriel probe in flight) | **HELD OPEN** | § 14 |

---

## § 1 — Register 1: the label-flip, and the one line that carries it

**L-33(c) / spec § 10.7:** *fighting wave `w` reads 0-based index `w − 1` = the cell LABELED `w`*.

The emissions are keyed by **label** (`wave` ∈ [1, 200]; U-8's `wave = index + 1`), so in
label-space the corrected law is the **identity**:

```
                  pre-flip (L-29, at bae60ce6)      post-flip (L-33, at 0474ca1d)
label_for(w)  =   max(1, w − 1)               →     w                    domain [1, 200], total
```

`src/reincarnated/simulation/kc2/opposition.py` — `ArrayLookupLaw` now also exposes
`zero_based_index_for(w) = w − 1`, so the law can be stated in the engine's own coordinates without
a second convention.

**The clamp is REMOVED, not retained.** Under the corrected law fighting wave 1 reads index 0 = the
cell labeled 1; the boundary the old law declared has no referent. Value-neutral (both laws return
95 at `w = 1`) and semantics-bearing: **a retained clamp is a claim that a boundary exists.** A law
that needs no edge case where its rival needed one is itself corroborating (L-33(c)).

Domain violations now raise with the reason in the message:

```python
raise ValueError(
    f"wave_fought must be in [1, 200], got {wave_fought} — "
    f"the law is TOTAL on that interval and has no clamp")
```

**Falsification hook retained, unchanged:** `WaveScaling` still has no scalar path, so the
pre-registered G-D diagnostic (a damage-side misfit at exactly-one-cell granularity re-opens the
law) is still a one-line change and nothing else.

---

## § 2 — Register 3: EVERY balancingadjustment-derived value, before and after

Source: `data/kc2/halt9_survival_wave_scaling_full.csv` (600 × 28, all 25 array fields × 3
difficulties) and `data/kc2/u8_survival_wave_scaling.csv`. Gladiator. Computed read-only, pre-code.

**Cross-check first:** the U-8 nine and the halt9 full grain agree on **0 disagreements over
200 waves × 9 fields** under the new law — the two emissions are consistent, so the table below is
not an artifact of one file.

### 2.1 The full before/after table

`OLD` = what the code returned at `bae60ce6`; `NEW` = at `0474ca1d`. **Bold = moved.**

| field | w1 | w2 | w93 | w150 | w151 | w155 | **w160** | w161 | w170 | **w171** | w172 | w180 | w200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `characterLifeModifier` OLD | 95 | 95 | 154 | 300 | 304 | 312 | 322 | 324 | 342 | 344 | 420 | 500 | 965 |
| `characterLifeModifier` NEW | 95 | 95 | **156** | **304** | **306** | **314** | **324** | **326** | **344** | **420** | **430** | **510** | **990** |
| `offensiveTotalDamageModifier` OLD | 5 | 5 | 19 | 41 | 42 | 42 | 43 | 43 | 45 | 45 | 56 | 74 | 125 |
| `offensiveTotalDamageModifier` NEW | 5 | 5 | 19 | **42** | 42 | 42 | 43 | **44** | 45 | **56** | **57** | **75** | **130** |
| `offensivePhysicalModifier` OLD | 0 | 0 | −15 | −18 | −18 | −19 | −21 | −21 | −24 | −24 | −25 | −28 | −44 |
| `offensivePhysicalModifier` NEW | 0 | 0 | −15 | −18 | −18 | −19 | −21 | −21 | −24 | **−25** | −25 | −28 | **−50** |
| `characterOffensiveAbility` OLD | 0 | 0 | 23 | 47 | 48 | 49 | 50 | 50 | 53 | 53 | 54 | 62 | 82 |
| `characterOffensiveAbility` NEW | 0 | 0 | 23 | **48** | 48 | 49 | 50 | 50 | 53 | **54** | **55** | **63** | **83** |
| `characterDefensiveAbility` OLD | 0 | 0 | 29 | 59 | 60 | 63 | 66 | 67 | 73 | 74 | 75 | 80 | 94 |
| `characterDefensiveAbility` NEW | 0 | 0 | 29 | **60** | **61** | 63 | **67** | 67 | **74** | **75** | 75 | **81** | **95** |
| `characterAttackSpeedModifier` OLD | 0 | 0 | 7 | 11 | 11 | 11 | 11 | 11 | 11 | 11 | 12 | 12 | 13 |
| `characterAttackSpeedModifier` NEW | 0 | 0 | 7 | 11 | 11 | 11 | 11 | 11 | 11 | **12** | 12 | 12 | 13 |
| `spawnChampionMinAdj` OLD / NEW | 0/0 | 0/0 | 1/1 | 1/1 | 1/1 | 1/1 | **1/1** | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| `spawnChampionMaxAdj` OLD / NEW | 0/0 | 0/0 | 1/1 | 1/1 | 1/1 | 1/1 | **1/1** | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |

*(`spawnMinAdj` / `spawnMaxAdj` are absent from the emission — 0 by declaration for all w, both
laws.)*

### 2.2 Three structural facts, each load-bearing

**(a) At fighting-160 exactly TWO of the 25 array fields move.** Swept, not assumed:

| field | OLD | NEW | Δ |
|---|---:|---:|---:|
| `characterLifeModifier` | 322 | **324** | **+0.621 %** |
| `characterDefensiveAbility` | 66 | **67** | +1.515 % |

Everything else is plateau-identical across labels 159/160 and therefore **flip-robust** — including
`offensiveTotalDamageModifier` (+43) and `offensivePhysicalModifier` (−21). This is the arithmetic
behind L-29(c)'s strike of the "+43 → +41" claim **STANDING**: 41 exists in no cell of the family
under either law. Test: `test_exactly_two_fields_move_at_fighting_160_under_the_flip`.

**(b) The count model is INVARIANT under the flip.** `spawnChampionMinAdj = spawnChampionMaxAdj =
1.0` at **every** label in 149–170. Measured end-to-end: expected regulars/champions over 151–170
are bit-identical under both laws (271.50 / 63.00 p06-OFF; 290.17 / 81.00 p06-ON).
**Consequence, and I state it because it is the available error: no AC-10.4 movement may be
attributed to L-33.** The counts moved for a different reason (§ 8). Test:
`test_the_count_model_is_INVARIANT_under_the_law_flip`.

**(c) The decade wall moves one wave earlier; the boundary case dissolves.**

```
fighting 170 → label 170 = 344
fighting 171 → label 171 = 420     ← the +76 pp FoA wall binds HERE (was: fighting 172)
fighting 172 → label 172 = 430
fighting   1 → label   1 =  95     ← no clamp; the law is total on [1, 200]
```

---

## § 3 — Register 2: AC-10.5 322 → 324, guards inverted

`tests/test_kc2_opposition_wave_engine.py::test_AC_10_5_life_scaling_while_fighting_160_is_324_NOT_322_and_NOT_168`

```
was:  assert life(160) == 322.0 ;  assert != 324.0  (lookup-law guard) ;  assert != 168.0  (F-2)
is :  assert life(160) == 324.0 ;  assert != 322.0  (index-inversion guard) ; assert != 168.0  (F-2)
      assert ArrayLookupLaw.label_for(160)            == 160
      assert ArrayLookupLaw.zero_based_index_for(160) == 159
```

**Both wrong answers stay named in one place; only which one is wrong changed.** The 322 value is
retained as the regression guard it now is, per BR-2's INVERT-DON'T-DELETE rule.

Other inverted guards in the same file, each with its reason in the diff:

| test | was | is |
|---|---|---|
| `…lookup_law_applies_to_EVERY_array_in_the_family` | 200 → 965 / +125 | **990 / +130**, and `!= 965` / `!= 125` retained as guards |
| `…decade_wall_binds_AT_its_label_not_one_wave_later` | 420 binds fighting **172** | 420 binds fighting **171**; `!= 344` at 171 retained |
| `…N_equals_1_BOUNDARY_DISSOLVES_and_the_clamp_is_retired` | clamp declared at `w = 1` | **no clamp**; `label_for(w) == w` for all 200; `label_for(0)` and `label_for(201)` both raise `match="TOTAL"` |
| `…two_off_by_ones_are_distinct_facts` | `label_for(151) == 150` | `label_for(151) == 151`; the contrast is now `label + 1` vs `label` |
| `test_the_wave_record_carries_324_while_fighting_160` (run-surfaces) | asserted **322** + carried E-7 open | asserts **324**; **E-7 RESOLVED in § 11.4's favour** |

**E-7 disposition, explicitly:** at Phase C I recorded a spec-internal conflict — § 11.4's inline
comment said "324 at wave 160" while § 10.7 + AC-10.5 said 322, and I emitted 322 per the law.
**The comment was right and the law was wrong.** The two seams now agree on 324 without star-lord
changing a line (his field is a pass-through; verified at `68e2e372` that his only literal 324 was a
synthetic wave-43 fixture).

---

## § 4 — Register 4: r2 consumed under the § 6.2b phase-row exclusion

**Source of record vendored byte-identical** (`diff -q` silent ×3):

| file | SHA-256 | rows |
|---|---|---|
| `data/kc2/t21_wave160_board_ehp_r2.csv` | `ddfc81ca15279449046ca026f807912a0686d48a43533a7302bbcaa009ae72f3` | 39 × 33 |

### 4.1 The exclusion rule, applied and MEASURED

```
39 rows  −  3 `nemesis_beast_01_p{2,3}*` rows  =  36 board rows
```

`load_wave160_board()` applies it **by default**; `include_phase_rows=True` exists only so a test can
measure the hazard.

- **Predicate agreement, asserted:** the record-name predicate (the spec's own wording) selects
  exactly the same 3 rows as `spawn_source == "phase-UNWIRED-in-crucible"` — set-for-set. The rule
  is enforced on the **record name**; the `spawn_source` agreement is carried as corroboration until
  legolas's r3 promotes the verdict class.
- **Hazard, quantified:** summing the 3 excluded rows inflates a board total by **2,967,411 eHP =
  21.2 %** of the 13,981,477 engaged-window total. That is what the rule is worth, and it is now a
  number in a test rather than a warning in a note.

### 4.2 The four-link chain, re-derived and closed EXACT

```
L          = levelVarianceEquation(apl) + 3            DECLARED sim input (+3 MEASURED, DB source NAMED-ABSENT)
base_life  = ((L × coefficient) ^ exponent) + constant  winner-only bio, PARSED off the row
M          = 1 + 5.80 + G/100 + armorbase_pct/100       ADDITIVE
eHP        = floor(base_life × M)                       floor, NOT round
```

`own_characterLifeModifier` is **NOT applied** — every r2 row carries
`own_applied = "NO (falsified: Bileeater +50 -> +4.41%)"`, and a test asserts the chain does not read
it.

| body | L | armorbase | M | base_life | floor @ **G=324** | measured | Δ | floor @ G=322 | Δ % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Zantarin, the Immortal | 109 | 125 | 11.29 | 329,751.6885 | **3,722,896** | 3,722,896 | **0** | 3,716,301 | −0.177 % |
| Archmage Aleksander | 109 | 125 | 11.29 | 329,751.6885 | **3,722,896** | 3,722,896 | **0** | 3,716,301 | −0.177 % |
| Kubacabra P1 | 109 | 125 | 11.29 | 261,806.5764 | **2,955,796** | 2,955,796 | **0** | 2,950,560 | −0.177 % |
| Galakros, the Mountain | 106 | 103 | 11.07 | 207,385.3354 | **2,295,755** | 2,295,755 | **0** | 2,291,607 | −0.181 % |
| Aetherial Bileeater | 112 | 129 | 11.33 | 42,726.8744 | **484,095** | 484,095 | **0** | 483,240 | −0.177 % |
| Death Revenant | 109 | 125 | 11.29 | 41,497.2687 | **468,504** | 468,504 | **0** | 467,674 | −0.177 % |
| Aleksander's Shard | 109 | 125 | 11.29 | 9,203.9473 | **103,912** | 103,912 | **0** | 103,728 | −0.177 % |
| Skeletal Archer | 109 | 110 | 11.14 | 3,701.7872 | **41,237** | 41,237 | **0** | 41,163 | −0.179 % |

**The three structural guards, each scored:**

```
G = 324 (cell LABELED 160) + floor  →  8/8 EXACT, residual 0, zero free parameters
G = 322 (index-inverted read)       →  0/8, every body ≈ −0.177 %   ← G-index guard
G = 324 + round instead of floor    →  3/8 (round misses 5)          ← floor guard
multiplicative M (either reading)   →  0/8                           ← additive-M guard
```

Board total: engaged window = **13,981,477** with camera multiplicities — asserted equal to
`ENGAGED_WINDOW_EHP_TOTAL`, and its docstring carries the L-33(f) warning the TTK surface must
consume: **this is a FLOW, not a stock** (summons respawn; `petLimit` 3/6/12, TTL 30–75 s).

**Retired with it:** `board_ehp_floor()` (it was never a floor — the ≈ 9.4 M figure missed both the
summon layer and the armorbase term) and `TOL_NEMESIS_CLASS` / `TOL_P04_BAND` (T-8 RETIRED, L-33(e)
— a tolerance band on an exact closure is meaningless).

---

## § 5 — Register 5 (G-W1): loader grade + vendored-SHA pins

jack-ryan's exact action was *"(a) carry the grade on the loader … so it can ride into provenance;
(b) **pin the vendored SHA in a test** with the comment 'bump when the F-7 revision lands' — that
converts a silent staleness at G-D into a loud failure."*

The F-7 revision **has** landed, so (a) is discharged by carrying the *resolved* grade, not a
pending one:

```python
BOARD_CSV_GRADE = "F-7-RESOLVED (L-33) — chain closes 8/8 EXACT, residual 0, zero free parameters"
```

and by putting the grades **on the rows**: `BoardEntry` now carries `charlevel_grade` (r2's per-row
provenance) and `verdict` (`EXACT` vs `PREDICTION-uncorroborated`), so a prediction row cannot ride
into baton provenance dressed as a measurement.

(b) is discharged **three times**, not once — the same failure mode existed on the count side:

| pinned constant | file | asserted by |
|---|---|---|
| `opposition.BOARD_CSV_SHA256` | `t21_wave160_board_ehp_r2.csv` | `test_G_W1_the_board_source_is_GRADED_and_its_vendored_SHA_is_PINNED` |
| `wave_engine.POOLS_CSV_SHA256` | `pe6_crucible_wave_pools_v2.csv` | `test_G_W4_every_exemption_is_a_GRADED_cited_value_and_the_SHAs_are_PINNED` |
| `wave_engine.EXEMPTION_CSV_SHA256` | `pe6_pool_ignoregamebalance.csv` | same |

The same test also asserts the **superseded emissions are gone** — see § 15.

---

## § 6 — Register 6 (G-W2): kubacabra single-phase re-scope

| was | is |
|---|---|
| `kubacabra_phase_chain()` → 3 values; docstring *"KUBACABRA IS THREE-PHASE AND THE SIM NEEDS ALL THREE (L-29)"* | **`kubacabra_crucible_phases()` → `(2_955_796,)`** — one value |
| test `test_kubacabra_is_three_phase_and_the_sim_carries_all_three` | **`test_kubacabra_is_SINGLE_PHASE_in_the_crucible_and_no_P2_P3_body_can_be_rolled`** |
| — | `kubacabra_campaign_phase_chain_DB_ONLY()` keeps the DB fact inspectable, named so it cannot be mistaken for a Crucible enumeration |

**The old name is REMOVED, not edited**, and a test asserts `not hasattr(op, "kubacabra_phase_chain")`
— so a caller who wanted the old behaviour collides with the ruling rather than with a
differently-shaped tuple.

**The claim now pinned is the one jack-ryan asked for** (*"add the assertion that no P2/P3 body
enters a roll, which is the fact worth pinning"*): 300 rolls of wave 160, every body's record checked
against both phase markers. Zero.

Grade upgraded per L-33(h): L-30(c)'s *declared-unmanifested* → **MEASURED-ABSENT-WITH-MECHANISM**.
The mechanism is in the docstring: the phase chain is a campaign death-spawn and the `[sm1]` overlay
**deletes its wiring** (994 fields vs gdx1's 995); the Crucible strips campaign-only mechanics. The
C-9 overlay law (**whole-record replacement, never field-merge**) is stated beside it, because a
field-merge is precisely how this chain would have haunted the model.

---

## § 7 — Register 7 (G-W3): AC-6.1 / 6.2 / 6.3 are tests, not prose

Re-graded from PASS-on-prose to **executable**, which is the arm jack-ryan preferred.

| AC | test | what it actually checks |
|---|---|---|
| **AC-6.1** | `test_AC_6_1_spawned_records_are_a_SUBSET_of_the_emitted_roster_weighted_as_emitted` | 5 waves × 60 rolls: every spawned record ∈ that wave+point's emitted roster (champion rows against the champion roster, regulars against the regular one) — this catches a roster index running off the end of `roster_records`, which a code-structure statement cannot. Plus the weighting limb on wave 160's genuine 50/50 p04 choice, 2,000 rolls, \|p − 0.5\| < 0.05. |
| **AC-6.2** | `test_AC_6_2_body_count_reproduces_the_10_5_model_TO_THE_INTEGER_on_every_one_of_20_waves` | **Per-wave, all 20 waves of 151–170, both p06 limbs = 40 comparisons**, against an **independent re-implementation** of § 10.5 read straight off the CSV, sharing no code with `wave_engine` beyond the csv reader. jack-ryan's objection was exact: *"an aggregate can be right while a per-wave count is wrong — and E-3 is precisely a per-wave discrepancy, so this is not hypothetical."* |
| **AC-6.3** | `test_AC_6_3_concurrent_bosses_are_NOT_capped` | Two limbs, as suggested: **(i)** no concurrency-cap constant exists in the module (source scan for `BOSS_CONCURRENCY_CAP`, `MAX_CONCURRENT_BOSSES`, `boss_limit`, `max_bosses`); **(ii)** a roll DOES place ≥ 3 boss-pool bodies simultaneously. An absence this seam can produce a presence for. |

The module header's coverage claim now matches what it delivers.

---

## § 8 — Register 8 (G-W4) + the AC-10.4 re-evaluation BY CITATION

### 8.1 What replaced what

The six-entry declared-override `dict[str, bool]` is **retired**. Exemption resolves through a
**635-pool citation registry** built from the SHA-pinned sidecar, every value a graded `Cited`:

```
exemption_registry() → Dict[str, PoolExemption]      635 pools, 74 exempt
PoolExemption.exempt : Cited[bool]                   grade ∈ {DB-CITED (511), TPL-DEFAULT (124)}
ignore_game_balance(pool_record) → Cited[bool]       an UNKNOWN pool RAISES; there is no default
```

`DB-CITED` (the record carries the field) and `TPL-DEFAULT` (it does not, and the template's
declared default governs) are **different epistemic states**, which is exactly G-W4's point —
*"the grade is not on the value, so a reader cannot tell a DB-CITED entry from a spec-declared
one."* **E-3 turned on two `TPL-DEFAULT` rows.**

`VALID_GRADES` grows by `TPL-DEFAULT` (the "one addition" jack-ryan anticipated); its census ships
in the same commit — § 13.

### 8.2 The class heuristic is FALSE BY ONE, in code

L-35's fact-3 correction, verified independently on the sidecar: filtering the 74 exempt pools by
`pool_kind != "boss"` returns **exactly one row** —
`records/proxies/poolsbasicgdx3/celestialmonstrosity_t3.dbr`, kind `trash`, `True`, `DB-CITED`. It is
named as a module constant (`SOLE_NON_BOSS_EXEMPT_POOL`) and asserted by name, so a future reader
who re-derives "exempt ⟺ boss" from the other 73 collides with the counter-example first.
`PoolExemption.is_boss_pool` exists but its docstring says *"Descriptive only. **Never** a substitute
for reading `exempt`."*

### 8.3 ⚑ A defect in my own Phase-C table, found by the citation pass and owned

| declared entry (`wave_engine.py:89–96` @ `bae60ce6`) | declared | cited | verdict |
|---|---|---|---|
| `poolsboss/nemesis_all.dbr` | True | True (PRESENT/DB-CITED) | AGREE |
| `poolsbossgdx1/nemesis_all_noaetherialvanguard.dbr` | True | True (PRESENT/DB-CITED) | AGREE |
| `poolsbossgdx1/nemesis_wendigooraetherialvanguard.dbr` | True | True (PRESENT/DB-CITED) | AGREE |
| `poolsbossgdx1/aetherialcolossus_galakros.dbr` | False | False (ABSENT/TPL-DEFAULT) | AGREE |
| `poolsbossgdx1/korvaaktombguardian.dbr` | False | **NO SUCH RECORD** | ⚑ **PATH DEFECT** |
| `poolsherogdx1/wendigocannibal_hero.dbr` | False | False (PRESENT/DB-CITED) | AGREE |

The Steward's pool is `poolsbossgdx**2**/korvaaktombguardian.dbr`. My key matched **nothing** and
fell through to the declared default — which happens to equal the intended `False`, so the defect is
**behaviourally inert on counts** and **live on provenance**: that pool was reported by
`pools_on_default_exemption` as running on the default while I believed it declared. This is
precisely the failure mode G-W4 named, and it was invisible until the value carried a citation.
`test_the_retired_declared_override_table_is_GONE_and_its_path_defect_cannot_return` asserts the
`gdx1` path now **raises** rather than defaulting.

Renamed with it: `on_default_exemption` → **`on_template_default`**. The old name meant *"absent from
my table"* — a property of the code. The new one is a property of the DB and is the one worth
counting.

### 8.4 ⚑ AC-10.4 RE-EVALUATED BY CITATION — both regular limbs now MISS

Waves 151–170. T-2 = 1.9 % of the wave-total count.

| model | regulars p06 OFF | regulars p06 ON | champions OFF / ON |
|---|---:|---:|---:|
| no exemptions at all (math-note F.4 pre-code row) | 290.83 | 310.83 | 63.00 / 81.00 |
| **as built** (`bae60ce6`, declared override + default) | 286.83 | 306.83 | 63.00 / 81.00 |
| **CITED** (sidecar flags, no-op-on-empty) — **shipped** | **271.50** | **290.17** | **63.00 / 81.00** |

| limb | target | CITED | Δ | Δ % | T-2 band | verdict |
|---|---:|---:|---:|---:|---:|---|
| p06 OFF | 292.0 | **271.50** | −20.50 | 7.02 % | ±5.55 | **MISS** *(was INSIDE as built)* |
| p06 ON | 316.5 | **290.17** | −26.33 | 8.32 % | ±6.01 | **MISS** *(was a miss; wider)* |
| champions, OFF-limb pin | 63.0 | **63.00** | 0.00 | 0.00 % | — | **EXACT** |
| champions, ON limb (pin-less) | 81.0 | **81.00** | 0.00 | 0.00 % | — | consistent |

**Reconciliation with L-35(c), exact.** The exemption set's band effect against the no-exemption
baseline is **310.83 − 290.17 = 20.67 ≈ the ledger's "≈ 20.7"** on the p06-ON limb (19.33 on OFF),
against the **4.00** the as-built totals accounted. The ledger figure is **re-derived, not assumed**.

**Why the champion pin could not move — structural, not luck.** 28 distinct pools in the band flip
`False → True` under citation. Measured: **all 28 carry `championChance = 0.0`**. A zero chance gates
the champion draw entirely, so the champion expectation is *provably* invariant under the exemption
correction. 63.00 EXACT is the term the correction cannot reach.

**Both misses are pinned AS MISSES**, in the shape jack-ryan called *"the single best piece of § 4.2
evidence in the unit"*:

- `test_AC_10_4_RE_EVALUATED_BY_CITATION_and_the_p06_OFF_limb_now_MISSES_292`
- `test_AC_10_4b_p06_ON_also_MISSES_316_5_and_BOTH_misses_are_FINDINGS_not_tuning_targets`

Each asserts the value, asserts `|Δ| > 0.019 × target` ("the miss is real and must stay visible"),
and carries the superseded as-built figure so the movement is attributable. **Neither can be
silently closed without deleting a test that says so in its own name.**

⚑ **The sensitivity limb is recomputed WITHOUT mutating the registry.** The old test mutated
`we.IGNORE_GAME_BALANCE` in a `try/finally`; the new one re-implements § 10.5 with every pool forced
non-exempt in a private helper. A test that edits a citation to make a point is a test that can edit
a citation.

### 8.5 E-3, confirmed closed-against-bound by citation

```
3 exempt nemeses (p01/p02/p03, one each — DB-CITED True)
+ 2 at p04            (both pools ABSENT/TPL-DEFAULT → additives → floor((1+1)×1.2) = 2)
+ 3 p06 hero champions (1 + 1 + chAdj 1 = 3, § 10.5 fact 5)
= 8
```

`test_E_3_CLOSED_AGAINST_BOUND_wave_160_carries_EIGHT_modified_bodies` asserts the two p04 flags by
citation and then the arithmetic. The spec's `≤ 7` was the spec's error; the sim's 8 was right.

---

## § 9 — Register 9 (S-W1): the § 9.5 one-line split, my side only

```
was:  devotion.ENVELOPE_DISCLOSURE = "devotion_envelope_disclosure:\n  ruling: …"
is :  devotion.ENVELOPE_DISCLOSURE_KEY = "devotion_envelope_disclosure:"      ← the wire key
      devotion.ENVELOPE_DISCLOSURE     = "  ruling: …"                        ← the value
      devotion.envelope_disclosure_block() → key + "\n" + value               ← for humans
```

`run.out_of_model_manifest()["devotion_envelope_disclosure"]` is now **byte-identical** to
`export.baton_v1_schema.DEVOTION_ENVELOPE_DISCLOSURE`, matching CD-5's ruling that the leading
register-key line IS the wire key.

`test_S_W1_the_register_key_line_is_the_WIRE_KEY_and_not_part_of_the_value` asserts the key is not
inside its own value, and checks byte-equality against star-lord's constant **by reading the literal
out of his module source rather than importing his runtime** — his file is his; my test only reads
it. **I did not touch `export/`.** His Phase-D join assert is his lap.

---

## § 10 — Register 10 (G-I3): math-note currency

`math/kc2-mechanism-stack-2026-08-08.md` amended **in place**, per the § D.3a precedent — the note
records that it was wrong rather than quietly acquiring the right answer.

| § | correction |
|---|---|
| **D.3b** (new) | E-1's *"the spec does not adjudicate"* **struck**; **RULED NON-STACKING** (L-32(a)) with its three legs restated, and the record that the stacking reading's rescue of the naive Soulfire cost was **named and refused as a reason**. Notes that E-5 then dissolved from the other direction (F-8's premise withdrawn) — so the tension stacking would have "explained" never existed. |
| **E-header** (new block) | Six-row table of what moved from five links to four; plus the two ledger rules the section's error produced: *a residual that survives on one body but not on others is a term, not a mystery*, and *exact-closure evidence outranks statistical-shape evidence*. |
| **F.1** | `scaling_row(w) = row LABELED w`; the clamp sentence struck — **no boundary exists**. |
| **F.2a** (new) | The "why 322, not 324" table struck with its degeneracy named (curve ratio spans 0.018 % over L ∈ [106,150]); the reverse/robust consequence map; and L-33(c)'s rule that **verification against a ruled-but-wrong convention propagates the convention's error**. |
| **F.4a** (new) | The cited band table, the 20.67 reconciliation, the championChance-0 explanation, and F-9's un-adopted branch stated with a pointer to why it is not taken. |
| **F.5** | E-3 **CLOSED-AGAINST-BOUND**; E-4 **RULED** (fact 5 governs; the § 10.4 phrase struck as a total-cap misstatement). |
| **E.5** | source is r2 under the exclusion rule; "last wins" sharpened to **whole-record replacement, never field-merge**. |

---

## § 11 — Register 11 (F-8): the corrected drain row, graded DB-CITED

**Wiring verified to consume the corrected row.** `fixture.SKILL_MANA_COST_R26` = 16.0, and its
citation now names the record:

```python
SKILL_MANA_COST_R26 = Cited(16.0, "eyeofreckoning1.dbr skillManaCost[26] (array [4..16]) — "
                                  "spec §3.1 as corrected by L-35(d) / F-8", "DB-CITED")
```

`16.0 × 12.25 × 0.90 = 176.4/s` — asserted by `test_F_8_the_drain_constant_names_its_OWN_record_now`,
which also asserts the cite does **not** name `eyeofreckoning2` or `aetherray2`. **The value does not
move; the citation does**, which is the entire point of a provenance-on-the-value discipline.

`SoulfireCostTerm` grade **UNADJUDICATED → DB-CITED** (⚑ semantic shift, declared: the value 0.0 does
not move, what it *means* does). The record's silence is the citation —
`eyeofreckoning2.dbr` declares no `skillManaCost` at all, and 474/476 `SkillSecondary_*` records omit
it, so **omission is the NORM, not an anomaly**. `superseded_grade` is retained on the dataclass so
the graduation is inspectable. The admissibility bound survives as a derived consistency check that
S = 0 trivially satisfies — **kept, because a bound that only exists while it is embarrassing is not
an instrument.**

---

## § 12 — Register 12 (F-9): no-op-on-empty, declared explicitly

Spec § 14 F-9's wording is *"the sim implements **no-op on empty roster** … and DECLARES it in the
baton count-model provenance. The alternative branches … are NAMED, never fitted."* All three parts:

```python
EMPTY_ROSTER_DISPOSITION = "NO_OP_ON_EMPTY"
EMPTY_ROSTER_BRANCHES_NAMED = (
    "NO_OP_ON_EMPTY (adopted, spec § 14 F-9)",
    "CONJURE_FROM_TEMPLATE (named, not fitted — costs +21.0/+27.0 bodies over 151–170)",
    "PROMOTE_TO_CHAMPION_DRAW (named, not fitted)",
)
```

`count_model_provenance()` is the declarable surface (composition + exemption sources with SHAs,
exemption grade census, the sole non-boss exempt pool, the branch taken, the branches named, the
array-lookup law, and p06's DEMOTED-OPEN state). `CountBounds` and `WaveRoll` carry
`empty_regular_roster` / `pools_with_empty_regular_roster` / `empty_roster_disposition` per roll.
Census asserted: **117 of 635** pools carry an empty regular roster.

### 12.1 ⚑ THE ARITHMETIC I DID NOT ACT ON — and it is the strongest number in the lap

The alternative branch is exposed as a **parameter** (`empty_roster_plus_one=True`) threaded through
`count_bounds` / `expected_counts` / `expected_counts_over` / `roll_wave`. Running it end-to-end:

```
p06 OFF :  271.50 → 292.50    vs target 292.0    Δ = +0.50  (0.17 %)   INSIDE ±5.55
p06 ON  :  290.17 → 317.17    vs target 316.5    Δ = +0.67  (0.21 %)   INSIDE ±6.01
band effect: +21.00 (OFF) / +27.00 (ON) — the ON figure reproduces F-9's declared ≈ 27.0 EXACTLY
```

**The adopted branch is outside T-2 on both limbs; the un-adopted branch is inside on both.** Two
readings exist and only the conductor may choose:

- **(i) reconstruction** — the U-9 count model behind the spec's 292.0 / 316.5 pins was itself
  computed with the `+1` landing on empty rosters, in which case the pins and the branch are the
  same claim; or
- **(ii) coincidence** — two ≈ 20-body corrections cancelling, in which case adopting it is textbook
  fitting, and L-33(e)'s own rule is the warning (*the celebrated ±0.004 % closure was two ~12 %
  errors cancelling*).

**I cannot discriminate (i) from (ii) from inside this seam.** It needs the `proxypool` template
fine-print or galadriel's boss-only-wave count pass — **both already named as F-9's resolution
path**. So: the sim ships the pre-registered disposition, the miss is pinned as a miss, and the
sensitivity is a function rather than a constant. **A branch reachable only by editing a constant is
a branch that gets edited.**

`test_F_9_the_UN_ADOPTED_branch_is_a_PARAMETER_and_it_lands_INSIDE_the_band` pins all six numbers
and re-asserts that the default is still `NO_OP_ON_EMPTY`.

**One additional guard:** even under the un-adopted branch, an empty roster has no name to draw, so
the body is emitted `<unrostered>` rather than invented. A conjured body with a fabricated identity
would be a worse error than the count it fixes.

### 12.2 ⚑ Self-caught while printing the provenance surface for this report (commit `2b562474`)

`count_model_provenance()["empty_roster_pools"]` returned **621** where spec § 14 F-9 says **117**.
Both are true and they count different things: **117 distinct POOLS of 635** carry an empty regular
roster, and those same pools recur across waves and spawn points, so the **alternative-ROW** count
over the 200-wave ladder is **621**.

Shipping one number under the word "pools" would have put a baton provenance block **5× away from
the spec section it cites** — the exact class of ambiguity D-2 was declared to prevent (*"two named
tick counts, precision over ambiguity"*). Split into `empty_roster_distinct_pools` (117) and
`empty_roster_alternative_rows` (621), both asserted, **plus an assertion that they DIFFER** so a
future refactor cannot quietly alias them.

Caught only because the report asked for the surface to be printed rather than described.

---

## § 13 — Register 13 (G-I5..G-I8) + the VALID_GRADES census

### 13.1 The four cosmetics

| # | finding | disposition |
|---|---|---|
| **G-I5** | census docstring's line-list was **stale at birth** (`:357` became a comment in the same commit) | **Line numbers DELETED, not refreshed.** The list now names each file's *fencing style* and cell count. A courtesy that is wrong on the file you just edited is not a courtesy; the grep is the only address the file gives. |
| **G-I6** | dangling *"(membership, not equality — see note below)"* with no note below | **The note is written.** A paragraph explains that membership cells are monotone under growth, cannot redden on an addition, fail only on removal — which is why they needed no amendment — and that cell 3 backstops their removal-guard intent. |
| **G-I7** | `ever_admitted_*` vs `EXPECTED_*` drift vector; protocol step 1 named only one | **Step 1 now names BOTH**, and cell 3's docstring states *why* they are separate literals: `EXPECTED_*` is an exact pin that moves both ways, `ever_admitted_*` is a monotone floor. "They are identical today and that is a fact about today, not an invariant." |
| **G-I8** | dedicated wave-neutral file was the right call | Recorded, and **followed again** — the new grade census is its own file for the same reason. |

Also corrected in place: **"19 assertions across 5 files"** (jack-ryan § 8.3's AST-precise count),
with the note that "15" was the 4-file equality subtotal — fixed here rather than by re-touching a
committed message, per his own disposition.

### 13.2 The `VALID_GRADES` census — G-B1's lesson applied *prospectively*

`VALID_GRADES` grew by `TPL-DEFAULT` this lap. Rather than wait for the next Gate-2 to find a stale
fence, the census ships **in the same commit as the growth**:
`tests/test_kc2_grade_vocabulary_census.py` — exact membership · never-REMOVED monotone floor ·
**the step-2 completeness claim, executable** · non-vacuity (the validator actually rejects an
unlisted grade).

⚑ **The completeness cell is AST, not grep, and it earned that on its first run.** The grep version
went red immediately — because the *sibling* census names `VALID_GRADES` in its docstring as a
cross-reference, which is a prose mention and not an enumerating consumer. The cell now walks the
AST for `Name`/`Attribute` nodes, the same reason `test_adr_006_no_external_db_write` walks the AST
rather than grepping strings: **so a module can document a vocabulary without tripping the guard that
protects it.** Today the answer is exactly two files, and a third makes it red.

---

## § 14 — What this lap deliberately did NOT do

- **p06 is NOT resolved.** `u9_bonus_spawn_state` stays **DEMOTED-OPEN** (L-33(g)); the galadriel
  probe is in flight. `pools_for()`'s docstring had the struck L-21 census leg in it and now says so
  explicitly. Both limbs are carried through AC-10.4, and `count_model_provenance()["p06_state"]`
  reads `DEMOTED-OPEN`. Test: `test_p06_fixture_state_is_DEMOTED_OPEN_and_both_limbs_are_carried`.
- **The AC-10.4 champion pin 63.0 stays scoped to the p06-OFF limb** (spec annotation, G-I1). The
  81.0 ON-limb figure is asserted as measured-consistent with **no pin claimed**.
- **F-9's alternative branch is not adopted**, however well it lands (§ 12.1).
- **E-6 is not closed.** `compose_damage_basis()` still declares it does not target the sheet band;
  the residual enumeration remains an unfired contingency.
- **No star-lord seam edit.** S-W1 is a one-line split on my side; his join assert is his lap.

**Seam boundary, verified file-for-file.** `git diff --name-only bae60ce6 0474ca1d` over
`export/ telemetry/ llm/ generation/ element/ anchor/ foundation/` returns **0 files**. The whole
diff is 19 paths, all inside `simulation/` + `tests/` + `data/kc2/`.

**Test counts, file-exact:** `test_kc2_channel_disc` 21 · `test_kc2_energy_devotion` 19 ·
`test_kc2_opposition_wave_engine` 44 · `test_kc2_run_surfaces` 14 ·
`test_kc2_grade_vocabulary_census` 4 = **102** (was 78).

---

## § 15 — Data retired, and why retirement rather than co-existence

| file | state | git records it as | reason |
|---|---|---|---|
| `data/kc2/t20_wave160_board_ehp.csv` | **GONE** | `D` (delete) | superseded — `glad_cell = 322` scores 0/8 |
| `data/kc2/pe6_crucible_wave_pools.csv` | **GONE** | `R091` → `…_v2.csv` | superseded by v2 (git detected the 91 %-similar rename; the old path no longer exists either way) |

**v2 was verified a strict superset before v1 was removed** — row-order-aligned, 1,998 = 1,998,
23/23 shared columns, **zero cell mismatches**, plus three flag columns. This is D-7's rule applied
to data: *carrying both is how a closed HALT re-opens by accident.* A test asserts both files are
absent, so a well-meaning re-vendor of t20 goes red.

The two SHA-pinned emissions are also **cross-checked against each other**: v2's per-row flag agrees
with the registry's per-pool flag on all 1,998 rows, and the provenance columns agree too. One
resolution path, two independently emitted files, and the agreement asserted rather than assumed.

---

## § 16 — Test declaration against the 7-item baseline

**Blast radius derived by GREP on every touched name** — the G-B1 lesson, applied
(*"a grep on the value-set names rather than a file-list selection would have caught it"*):

```
grep -rln "VALID_SHAPES|VALID_FAMILIES|VALID_GRADES|ENVELOPE_DISCLOSURE|load_wave160_board|
           ArrayLookupLaw|life_modifier|ignore_game_balance|IGNORE_GAME_BALANCE|kubacabra|
           SoulfireCostTerm|SKILL_MANA_COST|WaveScaling|expected_counts|roll_wave|count_bounds" tests src
```

→ 12 test files. **Result: 291 passed / 0 failed** (includes star-lord's `test_baton_v1.py`, which
is green — his seam is unaffected in code by my split).

| file | result |
|---|---|
| `test_kc2_opposition_wave_engine.py` | **44 passed** (was 26 tests; +18) |
| `test_kc2_energy_devotion.py` | **19 passed** (+2) |
| `test_kc2_run_surfaces.py` | 14 passed |
| `test_kc2_channel_disc.py` | 21 passed |
| `test_kc2_grade_vocabulary_census.py` | **4 passed** (new file) |
| `test_telegraph_value_set_census.py` | 3 passed |
| `test_baton_v1.py` · `test_br2_resolve_truth_1.py` · `test_br2_trace_stage_1.py` · `test_wr1_m5_hp_provenance.py` · `test_wr3_kite_commit_stage2b.py` · `test_wr3_stage2c.py` | all green |
| **total @ `0474ca1d`** | **291 passed / 0 failed** |
| **KC2 + census re-run @ `2b562474`** | **104 passed / 0 failed** |

**KC2 test count: 78 → 102** across five files (21 · 19 · 44 · 14 · 4).

### 16.1 The 7-item pre-existing baseline (jack-ryan § 8.3 / G-I4 — the corrected count is 7)

Re-run at this HEAD, **test-ID for test-ID**:

```
tests/test_wr2_d_nova_telegraph.py::test_the_minted_telegraph_carries_the_DERIVED_duration_under_the_arm
tests/test_wr2_d_nova_telegraph.py::test_the_minted_telegraph_carries_the_MEASURED_0_750_off_the_arm_H_M2_f
tests/test_wr1_m12_gd_mitigation_nova.py::test_INTEGRATION_the_nova_fires_telegraphs_and_lands_a_death2_class_blow
tests/test_kit_space_emitter.py::TestMultiKitEmit::test_all_kits_written
tests/test_kit_space_emitter.py::TestMultiKitEmit::test_chronicle_event_kit_ids_match_files
tests/test_kit_space_emitter.py::TestMultiKitEmit::test_kits_index_has_all_kit_ids
tests/test_kit_space_emitter.py::TestMultiKitEmit::test_per_kit_json_files_exist
                                                            → 7 failed, 134 passed
```

**2 nova-telegraph + 1 wr1_m12 + 4 kit_space_emitter = 7. Exactly the baseline, unchanged, zero
run-caused additions.** The 56 pre-existing tree failures and 21 pre-existing-env errors were not
chased, per the commission.

### 16.2 Worktree hazard — not applicable, and stated so

**No git worktree was used for any measurement in this lap.** All runs were in-tree at HEAD, so the
`.pth` editable-install leak (L-34(c)) had no opportunity to fire. Import provenance was printed
in-run anyway and reads
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/opposition.py` — the working
tree, not site-packages.

### 16.3 Full suite — launched, NOT RETURNED at report time. Stated, not omitted.

`python3 -m pytest tests/ -q` was launched at the `0474ca1d` tree and **had not returned when this
report was written** (it was ~55 % through; the 21 pre-existing-env errors had already appeared in
their expected block). It is not reported as green and it is not reported as failing — a suite that
has not returned is not evidence either way. *(Same posture as the Phase-C report § 8; the conductor
re-ran it then and adjudicated it at L-34(b).)*

**Per Discipline #2 the blast radius above is the correct grade for a build lap, and it is what this
report stands on.** The full suite is milestone validation and is the conductor's at gate close.

**The arithmetic it must decompose to, pre-registered here so it can be checked rather than
narrated:**

```
failures = 0 run-caused  +  7 pre-existing baseline (§ 16.1, re-run and confirmed test-ID for test-ID)
                         + 56 pre-existing tree (untouched seams: cycle12_layer4 ×33 · cycle12_layer6 ×12
                           · foundation ×4 · substrate_identity_loader ×2 · 5 singles)
errors   = 21 PRE-EXISTING-ENV (TestW5R3SeasonContentAuthoring, LLM-key-dependent;
                                key removed by design 2026-06-12)
```

**Any failure outside those three buckets is run-caused and is mine.** The most likely candidate, if
one appears, is a consumer of the retired data files or of a renamed `opposition`/`wave_engine`
surface — but the grep-derived radius (§ 16) returned **zero** such consumers outside the 12 files
already run, and the two retired CSVs are asserted absent by a test.

`2b562474` (the § 12.2 split) is **test + provenance-dict only** — no mechanism, no constant, no
data — and the KC2 + census suites were re-run green at it (104 passed / 0 failed), so it does not
change what the in-flight suite would say about the mechanisms.

---

## § 17 — CONFLICTS

*Recorded precisely, not resolved. None blocked the lap; each is the conductor's to adjudicate at
fold.*

### C-1 — AC-6.5's descriptive overshoot ratio is stale (arithmetic, not predicate)

Spec § 6.2b / AC-6.5 describes the additive-M guard as *"a multiplicative composition overshoots
**×2.9 (M 28.83 vs 10.02)**"*. Those two numbers come from **different chains**:
`28.83 = (1+5.80)(1+3.24)` is the multiplicative composition **without** the armorbase term, and
`10.02 = 1+5.80+3.22` is the additive M at the **superseded** G = 322 **without** armorbase.

Under the corrected four-link chain, on the nemesis row (`armorbase = 125`):

```
additive                                  M = 11.29
multiplicative, all three terms           M = 64.87   → ×5.746
multiplicative, two-term (armorbase added) M = 30.08   → ×2.664
```

**The BINDING predicate is unaffected — every multiplicative reading scores 0/8**, which is what
AC-6.5 asks the guard to prove, and the test asserts that. Only the spec's *prose* ratio is stale.
The test pins **all three ratios plus the spec's own 28.832**, so neither reading of the prose is
silently picked. **Conductor call:** whether to restate AC-6.5's descriptive figure (my
recommendation: restate to ×5.746 with the two-term reading noted, since the four-link chain is now
the chain of record).

### C-2 — The § 12 T-2 tolerance is expressed against a superseded denominator

T-2 reads *"1.9 % (5.5 monsters on **292**, waves 151–170)"*. The 292 is the AC-10.4 p06-OFF
**target**, and the cited model now returns 271.50 on that limb. Applying T-2 as a percentage of the
target (what I did: ±5.55 on 292.0, ±6.01 on 316.5) is the reading that keeps the goalpost fixed
where it was pinned at G-B close, and it is the reading the Phase-C tests already used — so I kept it
and did not re-derive the band from the new model. **But a reader could equally take 1.9 % of the
model's own output** (±5.16 / ±5.51), which does not change either verdict (both still MISS) but does
change the reported margin. **Conductor call:** which denominator T-2's percentage takes. Flagged
because a tolerance whose denominator is ambiguous is the kind of thing that quietly turns into a fit
two laps later.

### C-3 — F-9's disposition and AC-10.4's targets are pre-registered against each other

Two pre-registrations meet here and cannot both be satisfied:

- **spec § 14 F-9** pre-registers the sim's disposition as **no-op-on-empty**;
- **AC-10.4** pins 292.0 / 316.5, and § 10.5 fact 5's own arithmetic was published with them.

Executing the first makes the second miss by ~20 / ~26 bodies; the un-adopted branch closes both to
Δ +0.50 / +0.67 (§ 12.1). I implemented the pre-registered disposition and pinned the misses, per
charter § 4.2 and the standing rule (L-32(j)/L-35(c)) — **I did not improvise a resolution.** But the
near-exact landing of the alternative is, on its face, evidence about **how the spec's own pins were
computed**, which is a provenance question I have no instrument for. **Conductor call:** whether
F-9's resolution path (template fine-print / galadriel boss-only-wave counts) fires now, and whether
AC-10.4's pins are re-derived rather than re-tested. **Do not read § 12.1 as a recommendation to
adopt the branch** — it is a recommendation to go and find out.

---

## § 18 — What the next beat inherits

**Beat 2 (MO-1..MO-5 micro-oracles) is unblocked.** Nothing in the micro-oracle set touches the
flipped law or the exemption citation: MO-1 (1594/2576) and MO-2 (982) are energy-side and green;
MO-4 (20,005) is a pinned constant; MO-5's ~7.0 s floor still emerges from geometry.

**Beat 3 (s1 ramp 1→93, BINDING)** now runs under a law with **no boundary case** — the old clamp at
`w = 1` is gone, so the N = 1 edge that was "declared" is simply the law.

**Beat 4 (s2 inequality, INFORMATIVE)** starts from the corrected board: **13,981,477 eHP over the
fight window, and it is a FLOW** — summons respawn on 30–75 s TTLs, so eHP destroyed over the wave is
strictly greater than the instantaneous board. The TTK surface must consume this as a rate, not a
stock, and `board_ehp_engaged_window()`'s docstring says so where a caller will read it.

**Carried open, unchanged by this lap:** E-6 (sheet-band residual, contingency) · HALT-7 (boss skill
rank binding) · p06 DEMOTED-OPEN (galadriel) · F-9's branch (§ 12.1 / C-3) · legolas's r3
verdict-class (my loader's `spawn_source` cross-check will keep agreeing when it lands; the SHA pin
will go red, which is the intended loud failure).

---

**Filed:** gamora, 2026-08-08, KC2-SIM Phase D beat 1. Engine commit **`0474ca1d`** on `main`,
**UNPUSHED** — push fires only on Matt's word. Gate-2 REQUIRED and NOT self-cleared.
