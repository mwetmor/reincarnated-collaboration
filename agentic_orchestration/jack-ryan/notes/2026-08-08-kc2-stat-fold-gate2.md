# Gate-2 Finding — 2026-08-08 — KC2 G-STATS stat fold

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Commissioned by:** gandalf (RUN-CONDUCTOR, KC2-SIM autonomous run), ledger row L-68
**Target:** `reincarnated-engine` commits `08b87085` (math note + instrument) and `f573f171` (production fold), atop `c17f0791`
**Developer:** gamora
**Claim surface under audit:** `agentic_orchestration/gamora/notes/2026-08-08-kc2-stat-fold.md`
**Verdict:** **PASS-WITH-FINDINGS** — 3 WARN, 4 INFO, 0 BLOCK. All within-seam; **jack-ryan approves
directly per ADR-002**; nothing routed to Matt.
**Principles applied:** 1 (math-before-code / smoke-gate), 3 (cross-seam impact), 4 (decisions-log
as truth), 5 (severity matters)
**Disciplines cited:** #11, #63, #64, #67, #70, #72 (clauses 4, 5, 6, 7, 8)

## Scope

IN: (1) the `tests/test_kc2_locomotion.py:716` pin repair [FIRST-scrutiny]; (2) the #72 sweeps (note § 6);
(3) the coverage declaration + CSV spot-check vs vendor tables; (4) the ADDITIVE-NULLABLE claim on
`run.simulate_wave(player_damage_per_tick=...)`; (5) grade vocabulary per R-KC2-7.

OUT: the G-STATS gate reading fork (R-KC2-8 sentence vs spec § 11 "folded into the kill term") — Matt
commitment-boundary, filed Q52.

---

## Running log

### V-0 — SMOKE, INDEPENDENTLY REPRODUCED ✅

Re-ran the claimed suite myself, same six files, no `-x`:

```
244 passed in 33.05s
```

Claim was 244 passed / 0 failed / 33.84 s. **REPRODUCED.** Baseline 225 at `c17f0791` + 19 new
= 244; the arithmetic closes and zero regressions is consistent with the count.

### V-1 — THE test:716 PIN REPAIR — the FIRST-scrutiny item ✅ LEGITIMATE

Three sub-claims, all checked independently of the note.

**(1) The graduation is real and PRE-DATES the repair.** Timeline, from git:

| artefact | commit | timestamp |
|---|---|---|
| gamora C-1/ARR note carrying the graduation (§ 4b) | meta `0ccdc19e` | 2026-08-08 **17:23:29** |
| ledger L-67 fold recording it (`P05 cadence ADOPTED→MEASURED 36/36`) | meta `8a1ec8be` | 2026-08-08 **17:31:18** |
| stat fold — math note + instrument | engine `08b87085` | 2026-08-08 **17:56:18** |
| stat fold — production (the repair) | engine `f573f171` | 2026-08-08 **18:10:08** |

Graduation lands **33–47 minutes before** the repair, in a lap (`c17f0791`) that touched
**zero production code**. The basis — `minSpawnTime = maxSpawnTime = 3.0` on 36/36 band-A
ProxyAmbush proxies — is a **vendor-record read**, i.e. an input this fold did not produce and
could not have moved. The graduation is causally upstream and substrate-independent of the fold.
Additionally: the repair was **externally commissioned**, not self-initiated — ledger L-67(j)
carries the conductor's hand-back verbatim (*"HAND-BACK (may-not-edit, gamora's seam) … grade-words
in comments/docstrings/EMITTED metadata … grade-word repair rides the stat-fold commission"*).

**(2) NO numeric assertion, tolerance, or constant moved — byte-verified.** I did not sample; I
enumerated. `git diff c17f0791 f573f171 -- '*.py'` removes exactly **30 lines**. 26 are docstring
or comment prose. The remaining **four** are:

```
-    per_tick_damage = (basis.flat_physical_min + basis.flat_physical_max) / 2.0
-        kill_term_grade=("MEASURED — hp_lookup supplied" if hp_lookup
-P05_DRIP_CADENCE_S: float = 3.0           # below the minimap instrument's resolution; model adopted
-    assert "NOT measured" in d["grades"]
```

- `P05_DRIP_CADENCE_S: float = 3.0` — **value byte-identical**; only the trailing comment moved.
- `per_tick_damage = …` — the ADDITIVE-NULLABLE change; the removed expression is preserved
  character-for-character in the new `else` branch (see V-4).
- `kill_term_grade=(…` — a string continuation; the `NAMED-ABSENT-DECLARED-ZERO` token is
  preserved as a **prefix**, which is what `test_kc2_locomotion.py:530` (`.startswith`) reads.
- `assert "NOT measured" in d["grades"]` — **the ONE removed assertion in the entire commit, and
  it contains no numeral.**

`grep -i assert` over every removed line returns that single line. `P05_DRIP_CADENCE_S == 3.0` is
still asserted at `tests/test_kc2_locomotion.py:705` (untouched, in the *neighbouring* test) and
is **additionally** asserted at the new `:738`. Assertions `:697–:706` and `:717–:721` are
unchanged. **Claim (2) VERIFIED.**

**(3) The kept key names are correctly kept.** `adopted_cadence_s` (calibration.py:1200) and
`is_the_adopted_spec_value` (:1184) assert that **3.0 is the value the spec adopted**. The
graduation moved the *basis* (camera-unresolvable → record-measured), not the *value* and not the
*fact of adoption*. `is_the_adopted_spec_value` is read downstream at `test_kc2_locomotion.py:716`
and gates `:717`'s `drip_cadence_s == 3.0`; renaming would have moved a live contract to relabel a
fact that did not move. **Correct call, and correctly reasoned in place** (#67).

**Net on the FIRST-scrutiny question.** The repair is the legitimate kind. It is externally ruled,
causally upstream, value-preserving, assertion-preserving, and **strictly strengthening** — the
old line pinned one substring; the new block pins the corrected grade, the 36/36 basis, the
`value 3.0 UNCHANGED` clause, a `cadence_grade_history` field, and the constant. It is not a test
edited to make a change pass.

⚑ **One structural observation the note does not make, filed for the record.** Gamora edited the
source string (`calibration.py:1195`) and its assertion (`test:716`) *in the same commit*. That is
mechanically indistinguishable from the illegitimate pattern, and the only thing separating them is
the external ruling — which lives in a **different repo** (`meta`) from the code (`engine`). The
audit trail held here because the ledger row and the note timestamps were reachable. **See F-4.**

### V-2 — THE ADDITIVE-NULLABLE CLAIM ⚑ THE CLAIM IS TRUE; THE TEST DOES NOT CARRY IT

Claim as written in the commit message and relayed in the commission: *"`run.simulate_wave` gains
`player_damage_per_tick`, ADDITIVE-NULLABLE, default expression **byte-identical** — asserted by
test, so zero drift by construction."*

**The byte-identity itself: TRUE, verified by diff.** `run.py:313–314` reads

```python
per_tick_damage = (float(player_damage_per_tick) if player_damage_per_tick is not None
                   else (basis.flat_physical_min + basis.flat_physical_max) / 2.0)
```

The `else` limb is character-for-character the removed line. Signature change is a keyword-only
`Optional[float] = None` appended last. **Additive and nullable: confirmed.**

**The test that is said to assert it does not.** `test_simulate_wave_accepts_the_limb_additively_without_moving_its_default`
(tests/test_kc2_monster_stats.py:190–197) calls `simulate_wave` twice **with no `hp_lookup`** and
compares `t_end_s`. On that path `run.py:334` gives every body `hp = 0.0`, so `run.py:455`'s
`applied = min(per_tick_damage, a["hp"])` is `0.0` for **any non-negative** `per_tick_damage`.
`t_end_s` cannot depend on the parameter. I probed it rather than reasoning about it:

```
test-as-written  a t_end 9.795918367346939   b t_end 9.795918367346939
  probe=       0.0  t_end=9.795918367346939  same_as_default=True
  probe=       1.0  t_end=9.795918367346939  same_as_default=True
  probe=1000000000.0  t_end=9.795918367346939  same_as_default=True
  probe=      -5.0  t_end=326.530612244898   same_as_default=False
```

**The test passes if the default branch computes `0.0`, or `1.0`, or `1e9`.** It is vacuous for
the whole non-negative domain — which is the entire domain the claim is about. The same call pair
*with a board supplied* is sharply discriminating:

```
WITH board (ehp_lookup(10, LO)), default            t_end 252.163265
  probe=        334.00 (DB limb)      t_end=252.163265   same=True
  probe=      51726.00 (SHEET limb)   t_end= 11.346939   same=False
  probe=          1.00                t_end=326.530612   same=False
```

Its companion, `test_the_DB_limb_is_byte_identical_to_what_run_py_always_computed` (:171–178),
**never imports or touches `run.py`** — it pins `monster_stats.player_damage_per_tick` against a
copy of the expression re-typed inside the test. If `run.py`'s default branch drifted tomorrow,
both tests stay green.

So the load is carried by my reading of the diff, **not** by the suite. The claim "zero drift by
construction" is sound as a statement about *this* commit and unsound as a statement about the
*guard*. This is gamora's own § 1.2 sentence turned on his own test: *"a declared boundary that the
instrument does not enforce is a boundary in prose only."* → **F-1, WARN.**

### V-3 — THE COVERAGE DECLARATION ✅ RECOMPUTED FROM THE ARTEFACT, EXACT

I did not read the note's numbers; I recomputed them from the CSV.

```
rows 968
in_roster              {'1': 896, '0': 72}          → 968 = 896 rostered + 72 summon ✅
life_grade             {'MEASURED': 967, 'ABSENT:RECORD-ABSENT': 1}                  ✅
damage_grade           {'MEASURED': 953, 'ABSENT:MEASURED-ZERO-SWING': 14,
                        'ABSENT:RECORD-ABSENT': 1}                                   ✅
BOTH MEASURED          953  →  98.4504 %   (note claims 98.45 %)                     ✅
level_grade            {'MEASURED-SET': 896, 'DERIVED-INHERITED': 72}                ✅
rows carrying a level set                968 / 968                                   ✅
ordering invariant swing_min ≤ swing_max HOLDS 953 / 953, zero violations             ✅
```

**SHA pin verified:** `shasum -a 256 data/kc2/t22_band_a_monster_stats.csv` → `0d6992e8…`, matching
`STATS_CSV_SHA256` at `monster_stats.py:38` and the note's claim. 969 file lines = 968 rows + header.

**Residual arithmetic closes:** 967 eHP + 1 absent = 968; 953 damage + 14 zero-swing + 1 absent =
968. `BOTH = 953` is forced (the 14 and the 1 are disjoint on the damage side, and the 1 is the
same record on both sides) — the note's "BOTH 953" is not a coincidence of two counts, it is the
damage count, and the note says so.

**No grade inflation at the emission.** The `scavenger_h075` row (CSV:608) carries
`ABSENT:RECORD-ABSENT` in **both** grade columns and leaves every numeric field empty. The
INFERRED modal fallback is supplied at the **consumption** site (`monster_stats.ehp_lookup`), where
`ABSENT_RECORD_FALLBACK_GRADE` names it. Board and consumer are correctly separated; the board does
not claim what it does not have. Per R-KC2-7 this is the right shape.

**The hop-1 FIXPOINT claim, independently re-walked.** I re-ran the summon closure from the 72
summon bodies with my own edge-walker (`spawnObjects*`, `skillName{i}` → `spawnObjects*` /
`petBonusName*` / `summonRecord*`, and one hop through `buffSkillName*` / `petSkillName*`,
`/creatures/`-filtered):

```
summon bodies on board:                              72
hop-2 targets reached from them:                      9
  ... of which NOT already on the encoded board:      0
```

**Fixpoint at hop 1 CONFIRMED**, and confirmed as a *measured* output rather than a carry-forward
from the w152 board — which is what #69 asks for.

### V-4 — THE BOARD ITSELF, REPRODUCED FROM THE VENDOR TABLES ✅

I did not sample the note's chains; I re-implemented them and ran them against Edition-III raw.
Instrument: `/tmp/jr_verify_stat_fold.py` + `/tmp/jr_verify_damage.py`, built on the shared
low-level `gd_arz_adapter_2026_07_24.ArzArchive` + the L-33/C-9 overlay law only — **gamora's
`Chain` / `resolve` / stat-fold instrument deliberately NOT imported.** Read-only throughout.

**(a) The constants.**

```
difficulty  characterLifeModifier[8]        = 580.0     ✅ (the chain's 580)
survivalmode_enemies03 array length         = 200
  [0]=95.0   [92]=156.0   [151]=308.0   [159]=324.0
```

`[151] = 308.0` is legolas's w152 term and `[159] = 324.0` is the engine's pinned wave-160 `G`.
**Both cross-lap corroboration points verified from raw.**

**(b) `G_BAND_A` is carried verbatim.**

```
G_BAND_A (93 cells) vs raw survivalmode_enemies03[0:93]:  IDENTICAL   (mismatches = 0)
```

The self-correction gamora declared (his first draft linearised `G`; max |G − linear| = 17.49 pp)
is genuinely repaired — the array is the record, not a shape.

**(c) The eHP chain — 102 independent comparisons, 0 mismatches.** 17 records (random seed
20260808 over the MEASURED set, plus forced inclusion of a `trollhalf`, a `_summon`, and a
`scavenger_h*`), each at waves 1 / 47 / 93 × both level limbs:

```
eHP spot-check: 17 records x 6 cells = 102 comparisons, 0 mismatches
```

Sample spans trash (`skeleton_a02_archer`, 30,517), mid (`gazer_d01`, 225,243), heroes
(`troll_h03`, 491,482), summon bodies (`livingplant_a01_summon`, `aetheranomaly_01_summon`),
bounty records (`dc_bounty06`), and the largest body on the board
(`trollhalf_dermapterandeeps_01`, 1,281,895). **The board reproduces exactly.**

**(d) The intermediate-wave reconstruction — the note's headline claim, checked over the WHOLE
board rather than a sample.**

```
ms.MonsterStat.ehp(47) vs the ehp_w47 control column:
   comparisons = 1934    worst |delta| = 0.868852 HP    over-1-HP = 0
```

The note claims *"1934 / 1934 comparisons within 1 HP (worst 0.869)"*. **Exact match, to the
digit.** And I checked the control column is not itself circular: my raw w47 chain reproduces
`ehp_w47_*` on the same 17 records, 0 mismatches. The affine argument is sound — `G[w−1]` is the
only wave-dependent term and enters linearly.

**(e) The damage chain — 43 records, 0 differ.** Implemented from the note's stated law and run at
`level_lo`, wave 93, against `swing_w93_min/max`:

```
43 reproduced / 0 differ  (of 43)
trollhalf rows on the board: 35; ordering violations: 0
```

This is the half nobody had checked, and it reproduces. The `Class == Skill_Passive` discriminator
is genuinely enforced (not prose): I confirmed the ordering invariant holds on every `trollhalf`
row, which is the exact class whose violation caught the unenforced exclusion.

⚑ **One sub-rule is load-bearing and is NOT in the stated law — see F-6.** My first pass missed
`boar_a03` by 15.12 % on the max limb. Cause: `passiveproperties_boar.dbr` declares
`offensivePhysicalMin` with **no `offensivePhysicalMax` key at all**. The board is right and my
reading of the law was wrong — the operative rule is *a flat entry with no resolvable Max is a
POINT value, so Max := Min for that skill*, which reproduces `boar_a03` to 6 significant figures
(ratio 1.178191 vs board 1.178191, against 0.742021 for the alternative). With that rule applied
the sample goes 43/43.

**(f) The level bracket — DOES NOT REPRODUCE. See F-2.**

### V-5 — THE #72 SWEEPS, RE-RUN MECHANICALLY ⚑ SEE F-3

I re-ran both sweeps with gamora's declared patterns over his declared set
(`reincarnated-engine/{src,tests,design}` + `reincarnated-collaboration/{agentic_orchestration,canonical}`,
`*.py` + `*.md`, `grep -rniE`, excluding `__pycache__` / `galadriel/captures` / vendor).

**Clauses correctly discharged:**

- **Clause 6(a)** — the set is declared *before* the tables and names what it excludes. ✅
- **Clause 6(b)** — declined rows emitted as their own token, never folded into a substantive
  verdict. The 14 `MEASURED-ZERO-SWING-INCOMPLETE` bodies are **excluded from MEASURED coverage**
  and carry their own grade; the absent record is `ABSENT:RECORD-ABSENT` on the board and
  `INFERRED` at the consumption site. ✅ **Textbook.**
- **Clause 7** — *a defect found in a sample is a hypothesis about the population.* The
  `swing_min > swing_max` defect was found on four `trollhalf` rows and then swept over the
  **whole** board (953/953 holds). I re-verified: 0 violations. ✅
- **Clause 8** — the work-class mispricing is **self-named**, in the note, the commit message, the
  MIGRATION entry, and in a comment beside the repaired assertion. The discipline predicted its own
  next instance and the developer said so rather than being told. ✅ **Credit where due.**

**Clauses 4 + 5 — the hit tables are curated subsets of their own mechanical output. → F-3.**

### V-6 — GRADE VOCABULARY (R-KC2-7) ✅ IN THE ARTEFACTS; ⚑ IN THE PROSE

**Emitted artefacts: clean.** No grade inflation anywhere I can find in the CSV or the emitted
metadata. Grade tokens on the board are `MEASURED` / `ABSENT:RECORD-ABSENT` /
`ABSENT:MEASURED-ZERO-SWING` / `MEASURED-SET` / `DERIVED-INHERITED` — each earned, each with the
non-MEASURED rows excluded from the MEASURED counts. `stat_coverage()` **counts from the board**
rather than restating a constant (`monster_stats.py:275–298`), which is the right construction and
means the numbers move on their own at a re-emit.

`STATS_CSV_GRADE` and `ABSENT_RECORD_FALLBACK_GRADE` both state their basis inline. `PlayerDamageLimb`
carries `Cited(..., "MEASURED")` provenance on the SHEET limb and `E-6 / HALT-4 PARTIAL` on the DB
limb — neither is silently preferred, and `s1_kill_term_fold` refuses to pick (asserted at
`test_kc2_monster_stats.py:235`). **The fold does not resolve an open finding by default.** ✅

**Prose: one MEASURED-graded figure does not reproduce (F-2), and one reproduction chain is
incomplete as stated (F-6).**

---

## Findings

### F-1 — WARN — the ADDITIVE-NULLABLE guarantee is published as test-backed; the test is vacuous

**What.** The claim *"default expression byte-identical — **asserted by test**, so zero drift by
construction"* appears in the commit message, in the conductor's L-68 ledger row, and — the part
that matters — in `src/reincarnated/simulation/MIGRATION.md`'s "New surfaces" table, where the
consumer-impact cell reads `**NONE** — asserted by test_kc2_monster_stats.py::test_simulate_wave_accepts_the_limb_additively_without_moving_its_default`.
That is a **cross-seam contract statement** aimed at star-lord and drax.

The byte-identity is **true** — I verified it from the diff. The named test does not establish it.
It exercises `simulate_wave` with **no `hp_lookup`**, where `run.py:334` zeroes every body's HP and
`run.py:455`'s `applied = min(per_tick_damage, a["hp"])` makes `t_end_s` independent of the
parameter for the entire non-negative domain. Probed: `t_end_s` is bit-identical at
`player_damage_per_tick ∈ {default, 0.0, 1.0, 1e9}`. Its companion at `:171` — named
`..._byte_identical_to_what_run_py_always_computed` — never imports `run.py`.

**Rationale.** Discipline **#11** (empirical inspection over assumption) as gamora himself states it
in § 1.2 of his own note: *"a declared boundary that the instrument does not enforce is a boundary
in prose only."* Also Review Principle 1 (smoke-gate) and Principle 3 (cross-seam impact) —
MIGRATION.md is the cross-seam contract and it currently over-promises.

**Action.**
- [ ] gamora: supply a board to both calls in
      `test_simulate_wave_accepts_the_limb_additively_without_moving_its_default` (e.g.
      `hp_lookup=ms.ehp_lookup(10, ms.LevelLimb.LO)`), which makes the pair discriminating —
      verified: `t_end_s` moves 252.163 → 11.347 → 326.531 across probes with a board supplied.
      One line, no new fixture.
- [ ] gamora: either add a test that reads `run.py`'s default branch, or soften the MIGRATION cell
      to *"verified by inspection of the diff"* — **not both claims, one of them.**

### F-2 — WARN — the level bracket 4.736 % does not reproduce from the shipped board, and it is in shipped code

**What.** `src/reincarnated/simulation/kc2/calibration.py:895`, inside `s1_kill_term_fold`'s
docstring — the fold's headline consuming surface — states *"Measured span across band A:
**4.736 %**."* The math note § 5.1 (`kc2-stat-fold-ed3-2026-08-08.md:272–277`) carries the same
figure with its components. Recomputed from the shipped CSV over the population the note itself
names ("the 967 records with a level set"):

| quantity | math note § 5.1 | shipped `t22_band_a_monster_stats.csv` |
|---|---|---|
| median (lo limb) | 298,651 | **311,447** |
| Σ lo | 349,743,635 | **353,123,210** |
| Σ hi | 366,306,626 | **364,796,031** |
| **bracket** | **4.736 %** | **3.3056 %** |

I ruled out a column or population mismatch exhaustively — all nine combinations of
{w1, w47, w93} × {all 967, rostered 895, damage-MEASURED 953} give brackets in **3.25–3.40 %**.
No alternative definition reaches 4.736 % either (per-record mean 3.037 %, median 2.477 %,
max 10.376 %). **The figure is not reachable from the shipped artefact under any reading.**

The four figures are mutually consistent as a set, so this is a single **pre-correction snapshot**,
and the direction is exactly what gamora's own declared self-correction #2 predicts: his draft
unioned `levelVarianceEquation*` **per pool** instead of **per slot**, which widens the level sets,
which lowers Σ lo, raises Σ hi, and widens the bracket. **The board was re-emitted under the
correction; the magnitudes derived from it were not re-stated.**

The figure propagates: note § 2, note § 9's *residual pricing table*, and ledger **L-68(c)**
(*"level bracket 4.736 % (until B-KC2-C3)"*). The residual pricing table is a decision input for
**Q52**, the Matt commitment-boundary this fold hands back.

⚑ **The test does not catch it.** `test_the_level_bracket_is_NON_TRIVIAL_which_is_why_it_is_carried`
asserts `0.03 < (hi-lo)/lo < 0.07`; 3.3056 % sits inside the band, so the suite is green while its
own docstring (*"the band-wide span is ~4.7 %"*) is false against the artefact it reads.

**Rationale.** Discipline **#64** BASIS FORM propagation, verbatim: *"when a correction retires an
operand or a factor, every magnitude derived from it is re-stated in the same landing."* The
per-slot correction retired the per-pool operand in the same landing; Σ lo, Σ hi, median and the
bracket are magnitudes derived from it and were not re-stated. This is #64's **fourth** instance
and the first in the DERIVED-SUMMARY class (the prior three were derived *constants*). Secondarily
**R-KC2-7** — MEASURED wants a cited reproduction chain, and this chain's output is falsified by
the artefact it claims to summarise.

**Not a BLOCK, and the reason is stated:** the board is correct (V-4), no computed sim value
depends on the figure, and the error is **conservative** — it overstates the residual, so it cannot
cause a gate to be passed that should not be. But it is a MEASURED-graded number in production code
and in the run ledger that its own artefact contradicts.

**Action.**
- [ ] gamora: re-run § 5.1 against the shipped board and land a corrigendum-forward correction at
      `calibration.py:895` + math note § 5.1. Note § 2's identical block inherits it.
- [ ] gamora: while there, tighten `test_the_level_bracket_is_NON_TRIVIAL...` — a band of
      [0.03, 0.07] on a figure whose true value is 0.0331 leaves 2 pp of drift headroom on the
      quantity the test exists to protect.
- [ ] gandalf (conductor): L-68(c) carries `4.736 %`; corrigenda-forward row owed. **Q52's
      residual table should not be handed to Matt carrying it.**
- [ ] jack-ryan (me): **#64 gains a fourth founding instance, DERIVED-SUMMARY class.** Filed as a
      follow-on; not written in this note.

### F-3 — WARN — both #72 hit tables are curated subsets of their own mechanical output

**What.** The note § 6 closes with *"**UNRESOLVED rows:** none. Every hit is dispositioned."* Re-run
mechanically over gamora's own declared set and patterns, that is not true of the sweep output —
only of the table.

**SWEEP A** — one pre-existing, other-seam surface is in the declared set, matched the declared
pattern, and has **no row**:

```
agentic_orchestration/gandalf/notes/2026-08-08-kc2-locomotion-spec-amendment.md:23
  "...composition is closer to `max(last_arrival, cumulative_kill) + tail`..."
```

The file was created 2026-08-08 **11:17:14**, ~7 hours before the fold — it existed at sweep time.
(Three further un-rowed SWEEP-A files are this-commit artefacts — his own math note, his return
note, and `test_kc2_monster_stats.py` — defensibly trivial.)

**SWEEP B** — five files un-rowed: `kc2/run.py:219,283` (**his own seam, production code he edited
this commit**), `MIGRATION.md:52,55`, `math/kc2-summon-arrival-process-2026-08-08.md:592,599,620,629`,
`gamora/notes/…c1-closure-arr-repass.md` (5 hits), `galadriel/notes/2026-08-08-eor-followup-extraction.md`
(2 hits, dispositioned upstream by the conductor at L-67(j) but not restated).

**I checked every missed row. All are benign** — the spec-amendment's `max(la, ck) + tail` statement
is not merely unaffected but *vindicated* by the semantic shift; `run.py`'s hits are parameter
plumbing carrying no grade word; the rest are as-executed or this-commit. **No stale value hides
behind any of them.** The finding is completeness, not content.

**Rationale.** **#72** clause 4 (*"discharge by hit table … every benign hit gets a one-clause
reason"* — a row with no reason is a row with no row) and clause 5 (*"the output of the sweep is the
tool's output, pasted; a hand-curated list is a labelled expectation and is checked against the
sweep, never substituted for it"*). The gap between the mechanical output and the table is precisely
the object clause 5 was minted to close, and #72's own founding instances 5–7 were all committed by
people who knew the law — the failure mode is structural, which is the sentence #71 and #72 both
carry.

**Action.**
- [ ] gamora: add the six missing rows with one-clause benign reasons; correct *"every hit is
      dispositioned"* to name the population it is true of.

### F-4 — INFO — the co-edit's legitimating ruling lives in a different repository

**What.** The source string (`calibration.py:1195`) and its assertion (`test_kc2_locomotion.py:716`)
were changed in the **same commit**. That is mechanically indistinguishable from
test-edited-to-pass; the only thing separating them is the external ruling, which lives in
`reincarnated-collaboration` (ledger L-67(g)/(j)) while the code lives in `reincarnated-engine`.
The audit held here only because both repos were reachable and both timestamps survived.

Gamora mitigated this correctly and deliberately — the commit message names L-67(g), the code
comment names it, the MIGRATION entry names it, and the note routes it to Gate-2 as the
first-scrutiny item. **This finding is a note about the system, not about him.**

**Rationale.** **ADR-004** (cross-seam handoff via MIGRATION.md) and Review Principle 4
(decisions-log as truth). A grade graduation that authorises a test-assertion edit in another repo
is a cross-repo contract with no artefact in the code repo other than prose.

**Action.**
- [ ] jack-ryan / gandalf: consider whether in-run grade graduations that authorise test-pin edits
      should leave a machine-checkable trace on the engine side. **Filed as an observation, not a
      required change.**

### F-5 — INFO — `test_kc2_s1_ramp.py:322` is cited as pinning a token it does not pin

**What.** The note § 6.1 and `MIGRATION.md` both cite `test_kc2_s1_ramp.py:322`
(`== "NAMED-ABSENT-DECLARED-ZERO"`) as one of two pins protecting `run.py`'s
`composition.kill_term_grade` token. It pins a **different object**:

```
tests/test_kc2_s1_ramp.py:322
    assert s.kill_time_grade == cal.KILL_TIME_GRADE == "NAMED-ABSENT-DECLARED-ZERO"
```

`kill_time_grade` / `calibration.KILL_TIME_GRADE` (calibration.py:318, untouched) is a module
constant on the s1-cycle sample, not the per-run composition field `run.py:524` emits. The **only**
test protecting `run.py`'s token is `test_kc2_locomotion.py:530`'s `.startswith("NAMED-ABSENT")` —
one pin, not two, and a prefix match rather than an equality. The **decision** (do not rename) is
still correct; the cited evidence is half wrong.

**Rationale.** **#67** (a name is a pin) — the reasoning is right and the citation is loose.

**Action.**
- [ ] gamora: correct the citation in the note and MIGRATION; consider whether a prefix-only pin is
      the protection the token deserves.

### F-6 — INFO — the damage chain has an unstated sub-rule that a reproducer needs

**What.** The note § 1.1 states the damage law as
`swing = Σ_i offensive<T>Min/Max[rank_i − 1] × (1 + Σ offensive<T>Modifier / 100)`. A record whose
attached passive declares `offensive<T>Min` with **no `offensive<T>Max` key** — e.g.
`passiveproperties_boar.dbr` (`offensivePhysicalMin` present, `offensivePhysicalMax` absent
entirely) — is not covered by that sentence, and the choice of rule moves the answer by 15 % on the
max limb. The operative rule is *Max := Min for that skill when Max does not resolve*; the board
implements it and is right (verified to 6 s.f.).

**Rationale.** **R-KC2-7** — MEASURED is warranted by a *cited reproduction chain*. A chain that a
careful reproducer cannot execute from its stated form is under-specified. Also **#70**: the
consumed field set is declared, but this is a resolution rule inside it, not a boundary.

**Action.**
- [ ] gamora: add the one-clause sub-rule to the math note's § C law statement. The board needs no
      change.

### F-7 — INFO — the absent-record fallback is wave-invariant and limb-invariant, undeclared at the consumption site

**What.** `monster_stats.ehp_lookup(wave, limb)` returns `ABSENT_RECORD_FALLBACK_EHP_W93`
(382,207.0) for `scavenger_h075` at **every wave and both limbs**. The docstring says the record is
*"supplied at its INFERRED fallback rather than at zero"* — correct and well-reasoned (#63) — but
does not say the fallback is a wave-93 constant. Priced:

```
scavenger_h* sibling median eHP:   w1 = 357,588   w47 = 363,238   w93 = 382,207
fallback supplied at EVERY wave                        = 382,207
  overstatement at w1  = 6.88 %      at w47 = 5.22 %      share of roster = 0.103 %
```

Worst case ≈ 6.9 % on 1 body in 968. **Immaterial in magnitude; the point is that it is a claim the
consumption site does not make.** The `_g_band()` clamp has the same shape — it saturates silently
outside waves 1…93 while its docstring says it will *"say so by construction."*

**Rationale.** **#63** (a value that reads as a fact should be one) — applied here at a finer grain
than the fold applied it, and this fold applied #63 well elsewhere (the timeout-zero guard is
exemplary).

**Action.**
- [ ] gamora: one clause in `ehp_lookup`'s docstring naming the fallback as wave- and
      limb-invariant, with the ≈ 6.9 % worst-case price. No code change needed.

---

## Verdict

**PASS-WITH-FINDINGS.**

The fold is sound where it matters. I reproduced the board from the vendor tables with an
independently written chain — 102/102 eHP cells, 1934/1934 reconstruction comparisons within 1 HP
(worst 0.869, matching the claim to the digit), 43/43 damage records, `G_BAND_A` identical to the
raw array, the hop-1 fixpoint re-walked to 0 new bodies, the SHA pin verified, the coverage
declaration recomputed exact at 968 = 896 + 72 / 967 / 953 / 953 = 98.4504 %, the ordering invariant
953/953, and the smoke reproduced at 244/0. **Nothing in the emitted artefacts is graded above what
it earned.**

**The FIRST-scrutiny item clears.** The test:716 repair is the legitimate kind, and it clears on all
three sub-tests: the graduation pre-dates the repair by 33–47 minutes on a vendor-record basis this
fold could not have moved; the repair was externally commissioned at L-67(j); no numeric assertion,
tolerance, or constant moved anywhere in the commit (30 removed Python lines enumerated — exactly
one is an assertion and it carries no numeral); and the kept key names are correctly kept for a
correctly stated reason. The new block is strictly stronger than the line it replaced.

**Three WARNs, none blocking.** Two of them share a shape worth naming: **F-1** and **F-2** are both
cases where the *claim is true or the artefact is correct*, and what has drifted is the **guard or
the summary** — a test that cannot fail, and a derived magnitude that outlived its operand. That is
the same failure mode #72 clause 5 and #64 exist for, at two different joints, and it is the failure
mode this fold otherwise caught in itself twice.

**F-2 is the one with a downstream consequence.** The 4.736 % bracket rides in production code and
in ledger L-68(c)'s residual pricing, and that pricing is a decision input for **Q52**. It errs
conservative and blocks nothing, but the corrigendum is owed before the residual table is put in
front of Matt.

**What I could not verify** is listed in the section below.

**Approval routing (ADR-002).** All seven findings are within-seam corrections to gamora's own
surfaces (docstrings, one test call, one hit table, one citation) — no schema change, no API change
to consumers, no new ADR. **I approve them directly**; none needs Matt. The one item that touches
another seam is the L-68(c) corrigendum, which is the conductor's own row.

---

## What I could not verify

1. **The Ed-II edition-delta figures** (`0/953 consumed swing values move II→III`; `74/828 emission
   totals move, worst −21.9 %`; `2,266 IDENTICAL / 110 CHANGED`). Checking these needs a full
   two-edition sweep over ~2,378 records; I verified the *shipped* Ed-III board instead, which is
   what the fold consumes. The corrigendum's **direction** is corroborated indirectly — the two
   consumed records that changed (`armorbase04/05`) are the same pair the C-1 lap found on the life
   side, and band A sits at 102…109 while those records differ only at charLevel ≤ 41.
2. **The kill-term timing figures** (0.41–0.56 s/body on the SHEET limb; ~73 s/body on the DB limb;
   separation 6.10–10.51 s at w10/50/90; the w90 binding-term flip). These come from
   `s1_kill_term_fold()`, which the new tests exercise and which passed in my re-run; I did not
   re-derive the magnitudes independently.
3. **The 818/953 emission-channel pricing** (median ×2.87 / mean ×3.37 / max ×25.15). This is the
   *excluded* channel — by construction it is not on the board, so there is nothing emitted to check
   it against. It is a declared exclusion with a declared sign, which is what #70 asks for.
4. **The clear-time shift** (OFF 18.587 s → ON 19.887 s, +1.300 mean, one-signed, +4.875 at w90) and
   the beat-5 / T-1 consequences in note § 8. Out of this Gate's scope and routed to R-L68-2/3.
5. **`299 bios / 212 life equations`** (note § 3). Not recomputed; the per-record `bio_record` and
   `life_equation` columns I did consume reproduced exactly on all 17 sampled records.
6. **The G-STATS gate reading fork** — explicitly out of scope; Matt commitment-boundary, Q52.

---

## References

- `/Users/admin/Games/reincarnated-engine` commits `08b87085`, `f573f171` (baseline `c17f0791`)
- `/Users/admin/Games/reincarnated-engine/data/kc2/t22_band_a_monster_stats.csv`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/monster_stats.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/calibration.py` (`:895`, `:1184`, `:1195`, `:1200`, `:1240`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/run.py` (`:313`, `:334`, `:455`, `:524`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/wave_engine.py` (`:498`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-stat-fold-ed3-2026-08-08.md` (`:272–277`)
- `/Users/admin/Games/reincarnated-engine/tests/test_kc2_monster_stats.py` (`:88`, `:171`, `:190`)
- `/Users/admin/Games/reincarnated-engine/tests/test_kc2_locomotion.py` (`:705`, `:716`, `:719–738`)
- `/Users/admin/Games/reincarnated-engine/tests/test_kc2_s1_ramp.py` (`:322`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-08-08-kc2-stat-fold.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-08-08-kc2-c1-closure-arr-repass.md` (§ 4b, the graduation basis)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` (L-67, L-68)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#11, #63, #64, #67, #70, #72)
- My verifiers: `/tmp/jr_verify_stat_fold.py`, `/tmp/jr_verify_damage.py` (read-only against
  `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/`)


