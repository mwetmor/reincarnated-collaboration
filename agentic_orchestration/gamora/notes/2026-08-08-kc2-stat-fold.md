# KC2-SIM — THE STAT FOLD (G-STATS discharge lap) — gamora

**Commission:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, ruling **R-L67-1** (ledger L-67(k))
**Agent:** gamora (simulation seam) · **Date:** 2026-08-08
**Status:** **COMPLETE — 8 / 8 items closed. G-STATS PASSABLE on the eHP limb; ONE gate-reading question handed back.**
**Gate:** **G-STATS** — spec § 11, the 33rd baton-emit check (Matt ruling **R-KC2-8**)
**Record home:** **Edition-III** `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (READ-ONLY, **R-KC2-9**)
**Grading regime:** R-KC2-7 — MEASURED / DERIVED / INFERRED, no silent estimation
**Corrigenda discipline:** corrigenda-forward; no measured row retro-edited

**Deliverables**

| artefact | path |
|---|---|
| math note (BEFORE code, #1) | `reincarnated-engine/src/reincarnated/simulation/math/kc2-stat-fold-ed3-2026-08-08.md` |
| measurement instrument (READ-ONLY) | `…/simulation/scripts/gamora_kc2_stat_fold_ed3_2026_08_08.py` |
| **NEW** consuming module | `…/simulation/kc2/monster_stats.py` |
| **NEW** vendored stat board (SHA-pinned) | `reincarnated-engine/data/kc2/t22_band_a_monster_stats.csv` (`0d6992e8…`, 968 rows) |
| **NEW** tests | `reincarnated-engine/tests/test_kc2_monster_stats.py` (19) |
| MIGRATION entry (R11(b) clause included) | `…/simulation/MIGRATION.md` |

**Commits (NEITHER REPO PUSHED — conductor centralises under R-KC2-10):**
engine `08b87085` (math note + instrument) · engine `f573f171` (production fold) · meta `bededb20` + this note.

**Smoke (Discipline #2, no `-x` per #65):** `test_kc2_opposition_wave_engine` + `test_kc2_locomotion`
+ `test_kc2_s1_ramp` + `test_kc2_micro_oracles` + `test_baton_v1` + `test_kc2_monster_stats`
→ **244 passed / 0 failed, 33.84 s** (was 225; **+19 new, ZERO regressions**).

---

## 0. Verdict table

| # | item | VERDICT |
|---|---|---|
| 1 | **DAMAGE-side Ed-III read** | **CLOSED — 953/968 MEASURED**, field set declared + excluded set declared AND enforced. ⚑ **A ledger inference INVERTS** (§ 1.3). |
| 2 | **eHP fold with bracket semantics** | **CLOSED — wired.** `L` is a SET (`LevelLimb`), band bracket **4.736 %**, no midpoint offered anywhere. |
| 3 | **Bios from the corpus** | **CLOSED — 299 bios / 212 life equations** resolved per record (the summon closure adds 18/16 over the band-A-only figure). |
| 4 | **#70 coverage declaration** | **CLOSED** — 968 encoded (896 + 72 summon), eHP 967, damage 953, BOTH 953; 8 exclusions named, the largest **PRICED**. |
| 5 | **`scavenger_h075` modal fallback** | **CLOSED — declared at all three consumption sites.** One record, **three** blocked chains, not three absences. |
| 6 | **#72 sweep on `cumulative_kill`** | **CLOSED — mechanical, two sweeps, hit tables in § 6.** |
| 7 | **Grade-word hand-back repair** | **CLOSED — and it was MISPRICED (#72 clause 8).** A test pin on the retired grade was outside the hand-back's scope. |
| 8 | **Beat-5 re-entry** | **RECOMMENDATION GIVEN, not decided** (§ 8). Short form: the stated blocker discharges; a **different** one takes its place. |

---

## 1. ITEM 1 — the DAMAGE half, read at last

### 1.1 The chain is the life chain's structural twin

```
life   :  eHP   = floor( characterLife(L) × (1 + Σ characterLifeModifier / 100) )
damage :  swing = Σ_i offensive<T>Min/Max[rank_i − 1] × (1 + Σ offensive<T>Modifier / 100)
```

Same sum-over-every-attached-passive (the C-1 generalisation), same rank rule
`rank_i = int(skillLevel_i(L))`, same `[wave − 1]` array-lookup law, same two adjuster records
(`mp+difficulty_enemies01[8]`, `survivalmode_enemies03[wave−1]`). **One structural law, two
attribute families** — which is itself corroboration: a damage chain that needed a *different* law
would have been a reason to distrust one of them.

```
DAMAGE chain resolves      953 / 968   (98.45 %)
  residual  14   MEASURED-ZERO-SWING-INCOMPLETE   (skill-emission-only bodies)
  residual   1   RECORD-ABSENT                    (hero/scavenger_h075.dbr — the SAME record)
types carried  Physical 947 · Pierce 177 · Aether 133 · Life 112 · Chaos 96 · Poison 82 ·
               Cold 80 · Lightning 53 · Fire 39 · Elemental 18
```

### 1.2 The field set, DECLARED and — this is the part that mattered — ENFORCED

**CONSUMED:** `offensive<T>Min/Max` for T ∈ {Physical, Pierce, Fire, Cold, Lightning, Poison,
Aether, Chaos, Life, Bleeding, Elemental}, plus `offensiveTotalDamageModifier` +
`offensive<T>Modifier` from difficulty[8] + survivalmode_enemies03[wave−1] + attached passives.

**EXCLUDED (8 classes, each with a sign):** DoT/`*Duration*` · `offensivePercentCurrentLife*` ·
leech/mana-burn · control channels · body-record modifiers (**zero on 896/896 — measured, not
assumed**) · `poolToSpawnOnDeath` summon edges (Crucible-stripped, L-33(h)) · **every skill whose
`Class` is not `Skill_Passive`** · band B.

> ⚑ **MY FIRST DRAFT WROTE THE EMISSION EXCLUSION AND DID NOT IMPLEMENT IT — and its own emitted
> table is what caught that.** Four `trollhalf` rows came out with `swing_min > swing_max`, because
> `trollhalf_lightningbolt.dbr` carries `offensiveLightningMin = 1088 > Max = 870` at rank 29.
> **A bolt is not a swing.** The ordering violation was the symptom; consuming an emission channel
> into a swing total was the mechanism. Discriminator: the skill record's `Class`. With it enforced
> the invariant **HOLDS 953/953**. *(#11 — the table said so before any test did. A declared
> boundary that the instrument does not enforce is a boundary in prose only.)*

**The exclusion is PRICED, not merely named:** 818/953 bodies carry a non-passive damage channel, at
**median ×2.87 / mean ×3.37 / max ×25.15** of the consumed swing. **This is a flat-magnitude ratio,
not a DPS ratio** — emission channels carry cooldowns the sim does not model. Sign **POSITIVE**.

### 1.3 ⚑ CORRIGENDUM TO L-67(b) — the inference inverts

L-67(b) recorded: *"R-KC2-9 is now confirmed load-bearing BY MEASUREMENT: an Ed-II damage read
would have shipped 105 stale records."* Reasonable from the field histogram. **It is not what the
measurement says.**

```
surface REACHED by the damage fold        2,378 records
  IDENTICAL 2,266 · CHANGED 110 · ONLY-II 0 · ONLY-III 0 · ABSENT-BOTH 2

CHANGED, split by skill `Class`:
  AttackProjectileRing 22 · AttackProjectileBurst 21 · ProjectileAreaEffect 13 ·
  AttackProjectile 11 · AttackWave 11 · AttackWeapon 6 · …
  ⚑ CHANGED whose Class IS CONSUMED (Skill_Passive):  2
        records/skills/nonplayerskills/passive/armorbase04.dbr
        records/skills/nonplayerskills/passive/armorbase05.dbr   ← THE SAME PAIR AS THE LIFE SIDE

value descent, CONSUMED channel (953 records × waves {1,47,93}):   0 MOVE   ⇒ EDITION-INVARIANT
value descent, EXCLUDED channel (828 records):                    74 MOVE
        rifthound_eastswamp_cliffs   5,593.0 -> 4,369.0   −21.884 %
        ghost_oligarch_02            4,095.0 -> 3,316.0   −19.023 %
        ghost_h07                    7,900.0 -> 6,478.0   −18.000 %
        banditminiboss_mine01        4,836.0 -> 3,973.0   −17.845 %
```

> **CORRECTED STATEMENT.** The band-A **swing** channel is **EDITION-INVARIANT**, and the reason is
> named: the only two consumed records that changed are `armorbase04/05`, and they differ only at
> charLevel ≤ 41 where band A sits at 102…109. **R-KC2-9 is load-bearing on the damage side for
> exactly the channel this fold declares OUT-OF-MODEL** — 74 of 828 emission totals move, worst
> **−21.9 %**. A future lap that folds emissions in inherits an edition dependency this one does
> not, and off Ed-II would ship **74** stale records, not 105.
>
> **Nothing retro-edited.** L-67(b) stands as record; this row carries the sharper frame.
> *(The pin remains correct and the discipline that produced it worked — what moved is the size and
> the address of what it protects.)*

---

## 2. ITEM 2 — the eHP fold, with the bracket carried

`kc2/monster_stats.py` exposes `LevelLimb.{LO,HI}` and `ehp_lookup(wave, limb)`. **No midpoint is
offered anywhere in the API** — the life equations are convex in `L`, so writing one down has to be
a decision, and the enum makes it one.

```
band-A eHP at wave 93 over 967 records with a level set
    median (lo)  298,651      Σ lo 349,743,635 … Σ hi 366,306,626      bracket 4.736 %
floor-set widths       width 2: 454 · width 3: 235 · width 1: 6
(a)/(b′) equivalence   IDENTICAL 695 / 695   (R-L65-1 checked 6, C-1 checked 13)
```

**Intermediate waves are RECONSTRUCTED, and the reconstruction is CHECKED not asserted.** `eHP` is
affine in `G[w−1]`, the only wave-dependent term, so two anchors plus the exact array determine
every wave. The emission carries `ehp_w47_*` as a **control column** and a test asserts the
reconstruction against it: **1934 / 1934 comparisons within 1 HP** (worst 0.869).

> ⚑ **A CORRECTION I OWE MYSELF: the first draft of the module linearised `G` itself.** Measured
> against the record, `max |G − linear| = 17.49 percentage points` ≈ **2.5 % on eHP** — the same
> order as the entire level bracket the fold exists to carry. The array is now carried verbatim
> (93 cells), and a test pins the non-linearity so nobody re-derives the shortcut.

### 2.1 ⚑ A THIRD POSITIVE CONTROL, on a board I did not build — and a hand-back

`data/kc2/kc2_s1_banda_record_inputs.csv` is legolas's 895-row band-A board, SHA-pinned, built under
the **other** parameterization. Naive set-equality: **IDENTICAL 3 / DIFFER 892.**

Rather than adjudicate another agent's board, a mechanism was **tested**:

> **Hypothesis H.** The board's `charLevel_min/max` is not an achievable floor set; it is the range,
> over the record's SLOTS, of `floor(minVarianceEquation at apl = 100) + 3` — the per-slot
> **minimum** draw level.
>
> **H reproduces the board on 895 / 895 rows (100.00 %).**

**The two objects are RECONCILED, not in conflict** — they answer different questions. And the exact
reproduction independently confirms three things at once: the index-paired slot law, the
`apl = 100 + 3` parameterization, and the floor rule.

⚑ **HAND-BACK TO LEGOLAS (his seam, his board), sign NAMED.** A consumer reading `charLevel_max` as
*"the highest level this body spawns at"* reads **systematically LOW** (for `lv3_strong` the board
says `103,103` where the equation reaches `104`). **No live consumer exists today** —
`locomotion.py:52` reads only `characterRunSpeed*` from that emission, verified by grep. Registered
before a consumer appears, not filed as a defect.

⚑ **And the slot law caught MY error first.** My draft unioned every `levelVarianceEquation*` field
on the pool record; `aetherialhorror_t1` declares `lv3_strong` at slots 1/3 and `lv2_normal` at slot
2, widening `aetherhorrora_a01` from `{103,104}` to `{102,103,104}`. **That is legolas's L-65(e)
per-slot finding, and my draft was precisely the error it predicts.**

---

## 3. ITEM 3 — bios from the corpus

**CLOSED by construction.** The chain resolves `characterAttributeEquations → characterLife` per
record: **299 distinct bios / 212 distinct life equations** over the encoded roster (band-A-only was
281/196; the 72 summon bodies add **18 bios / 16 equations** the earlier figure did not carry).
The r2 board's 7-entry `BIO_CURVES` remains a wave-160 object and is untouched.

---

## 4. ITEM 4 — the #70 coverage declaration

```
ENCODED RECORDS                                    968     [896 rostered + 72 summon]
  eHP chain MEASURED                   967   (99.90 %)
  DAMAGE chain MEASURED                953   (98.45 %)
  BOTH — the G-STATS predicate         953   (98.45 %)
  carrying a level SET                 968   (100.00 %)  [896 MEASURED-SET · 72 DERIVED-INHERITED]
  summon bodies with BOTH chains        58 / 72
  ordering invariant swing_min ≤ swing_max          HOLDS 953 / 953
```

**Summon closure runs to FIXPOINT, not to a fixed hop depth** — layer 1 adds 72 bodies, layer 2 adds
**0**. Hop-2 was empty on the w152 board too; this is the independent extension to 896 roots and it
is a **measured output**, not a carry-forward (#69).

**The 14 MEASURED-ZERO-SWING bodies get their own token (#63 / #72 clause 6(b)).** Aether crystals,
two traps, two wind devils, the Dreeg eye, three cluster-summons. The record was read; every
attached skill was read; the swing total is zero **and that is the measurement**. But their entire
damage surface sits in the declared exclusion — **the footnote for 953 bodies is the whole story for
these 14** — so they are graded `MEASURED-ZERO-SWING-INCOMPLETE` and are **not** counted as MEASURED
coverage.

**What the declaration excludes** is listed in § 1.2 and carried in code as `DECLARED_EXCLUSIONS`,
each with a reason and a sign. Band B (s2, waves 151–160) is excluded **by name**: this fold is band
A only.

---

## 5. ITEM 5 — `scavenger_h075`: one record, three chains, one fallback

```
present in Ed-III  False        present in Ed-II  False
sibling family `hero/scavenger_h*` in the encoded roster:  6
    eHP@w93    n=6   min 236,981   median 382,207   max 491,198
    swing@w93  n=6   min     918   median     918   max   1,397
```

**Absent from every archive in both editions.** It blocks the locomotion `characterRunSpeed` join
(F-L7), the C-1 life chain, and now the damage chain — **one hole, three chains.** *(C-1 recorded
"two"; the damage read makes it three. Corrigenda-forward.)*

**FALLBACK: the modal value over its own sibling family** — a measured population, not an invented
number. **GRADE: INFERRED.** It does **not** satisfy G-STATS for this record. Declared where
consumed: `ABSENT_RECORD_FALLBACK_GRADE` in the module, the `ehp_lookup` docstring, the emitted
board row, and § 8 of the math note. Supplied at the fallback rather than at **zero**, because a
zero here would silently mean *"dies on first coverage"* — a claim, not an absence (**#63**).

---

> ## ⚑ CORRIGENDA-FORWARD BANNER — added 2026-08-08 after Gate-2 (verdict **L-70**, PASS-WITH-FINDINGS)
>
> **This note STANDS as the as-executed record of the fold. Three of its claims have been corrected
> or completed since, and the corrections live at
> `agentic_orchestration/gamora/notes/2026-08-08-kc2-gate2-repair-bundle.md`. Nothing below is
> retro-edited.**
>
> 1. **§ 2 / § 9's `4.736 %` level bracket is RETIRED → `3.3056 %`** (Gate-2 **F-2**, #64 BASIS
>    FORM). The figure was a pre-correction (per-POOL) snapshot; the board was re-emitted under the
>    per-SLOT correction and the magnitudes derived from it were not re-stated. **Five further
>    magnitudes in the same block moved** and are re-stated in the repair bundle § 2.2: median lo
>    298,651 → 311,447; Σ lo 349,743,635 → 353,123,210; Σ hi 366,306,626 → 364,796,031; TTK DB
>    72.99 s → 76.12 s; TTK SHEET 0.4080…0.5580 s → 0.4254…0.5819 s. The **×130.8…×178.9 ratio is
>    INVARIANT** and stands. **The BOARD was never in question** — Gate-2 reproduced it
>    independently (102/102 eHP cells, 1934/1934 comparisons). The errors were **conservative** in
>    every limb.
> 2. **§ 6.1's citation of `test_kc2_s1_ramp.py:322` is CORRECTED** (Gate-2 **F-5**). It pins
>    `KILL_TIME_GRADE` (`calibration.py:318`, a module constant), **not** `run.py:524`'s composition
>    token. **ONE pin protects that token — `test_kc2_locomotion.py:530` — and it is `.startswith`
>    prefix-only.** The decision not to rename stands; the evidence for it was half wrong.
> 3. **§ 6's *"UNRESOLVED rows: none. Every hit is dispositioned"* was TRUE OF THE TABLES AND FALSE
>    OF THE SWEEPS** (Gate-2 **F-3**, #72 clauses 4+5). **Ten fold-time surfaces were un-rowed**,
>    including production code in my own seam (`run.py:219,283`) and this note itself. All ten are
>    rowed with reasons in the repair bundle § 3, along with a population statement and **one
>    published row of § 6.2 that was wrong** (the `banner-annotated at the C-1 lap` claim).

## 6. ITEM 6 — the #72 sweeps. MECHANICAL, output pasted, sets declared

**Declared set (both sweeps).** Roots: `reincarnated-engine/{src,tests,design}` +
`reincarnated-collaboration/{agentic_orchestration,canonical}`. Types: `*.py`, `*.md`.
**EXCLUDES:** vendor trees (READ-ONLY, not consumers) · `galadriel/captures/**` (image artifacts) ·
`__pycache__` · `.git`. Case-insensitive. Tool: `grep -rniE`.

### 6.1 SWEEP A — the `cumulative_kill` semantic shift

Pattern: `cumulative_kill|declared[ _-]zero|kill_term_grade|s1_ehp_coverage|KILL_TIME_GRADE|kill_time_grade`

| surface | owner | disposition |
|---|---|---|
| `kc2/run.py:304, 522–524` | **gamora** | **REPAIRED.** Token `NAMED-ABSENT-DECLARED-ZERO` kept (accurate for a call with no board, and pinned by two tests); the false trailing clause *"band A carries no per-record eHP"* replaced. |
| `kc2/calibration.py:204–205, 318, 337, 376, 827–830, 848–853, 1225, 1305` | **gamora** | **ANNOTATED, values unchanged.** `composition_report` + `simulate_s1_cycle` are the **declared-zero limb** by construction (they supply no board); their rows stand as executed. A `stat_fold_annotation` key names which build the zero belongs to. |
| `kc2/locomotion.py:396, 731, 742, 757, 768` | **gamora** | **BENIGN — carrier, not claimant.** `kill_term_grade` is a passthrough field; `s1_ehp_coverage()` is cited as a *pattern* (counted-not-declared), which is unaffected. |
| `kc2/monster_stats.py` (new) | gamora | current, this commit. |
| `tests/test_kc2_locomotion.py:198, 506–507, 530, 605` · `test_kc2_s1_ramp.py:246, 298, 317, 322, 364` | **gamora** | **UNCHANGED, and deliberately.** These pin the **unfolded** path, which still is a declared zero. `:530` (`startswith("NAMED-ABSENT")`) and `:322` (`== "NAMED-ABSENT-DECLARED-ZERO"`) are why the token was not renamed. |
| `math/kc2-locomotion-lap-2026-08-08.md`, `…-s1-ramp…`, `…-c1-closure…`, `…-summon-arrival…` | gamora | **AS-EXECUTED RECORDS — stand.** Each describes a lap that ran under the declared zero. |
| `simulation/MIGRATION.md` | **gamora** | **NEW ENTRY** — the value move + the timeout hazard + the R11(b) clause. |
| `simulation/AGENT_STATE.md` | gamora | current, this commit. |
| spec `2026-08-08-kc2-sim-battle-spec.md` (5 hits) | **gandalf** | already annotated by the conductor at L-67(j). **No action owed.** |
| ledger `2026-08-07-kc2-sim-run-ledger.md` (4 hits) | **gandalf** | run record. **Corrigendum to L-67(b) offered in § 1.3; not edited by me.** |
| `jack-ryan/notes/…gate2-locomotion-lap.md` (2 hits) | **jack-ryan** | as-executed Gate-2 record — stands. |
| gamora notes ×4 (locomotion lap, c1-closure, s1-beat3, sitting) | gamora | as-executed records — stand. |

**UNRESOLVED rows:** none. Every hit is dispositioned.

### 6.2 SWEEP B — the cadence grade graduation (item 7's discharge)

Pattern: `P05_DRIP_CADENCE|intra-drip|drip cadence|adopted_cadence|is_the_adopted_spec_value|not_adopted`

| surface | disposition |
|---|---|
| `wave_engine.py:492` | **REPAIRED** — comment `"model adopted"` → `"MEASURED — 36/36 ProxyAmbush records, zero variance"`. Value 3.0 untouched. |
| `wave_engine.py:586–592` (docstring) | **REPAIRED** — the *"adopted, not observed"* paragraph replaced; the camera claim is preserved as historically correct about the camera. |
| `calibration.py:1156–1161` (docstring) | **REPAIRED** — and it costs the function its explanation, which is stated rather than glossed. |
| `calibration.py:1195` `grades` **emitted value** | **REPAIRED** — now names the record basis and the graduation; `cadence_grade_history` added to the **same local dict** (not a baton field). |
| `calibration.py:1240` `finding` string | **REPAIRED** — the false clause quoted and struck in place; the localisation restated as unchanged. |
| `calibration.py:1193` `adopted_cadence_s` · `:1175` `is_the_adopted_spec_value` | **NOT RENAMED — reasoned.** See § 7. |
| `calibration.py:795, 1246` `not_adopted` / `candidate_gamora_named_not_adopted` · `test:362` | **BENIGN — different referent.** These name the JC-G7 consequence candidate and the diagnostic-not-a-calibration claim. Nothing to do with the cadence's grade. |
| `tests/test_kc2_locomotion.py:682–688` (docstring), **`:716` (assertion)** | **REPAIRED — and this is the mispricing, § 7.** |
| `tests/test_kc2_locomotion.py:699, 710–711` | **UNCHANGED** — they pin the **value** 3.0 and the adopted-flag structure, neither of which moved. |
| `math/kc2-locomotion-lap-2026-08-08.md:559–560` | **STANDS — as-executed record**, already banner-annotated at the C-1 lap. |
| `AGENT_STATE.md:19` (graduation) / `:29` (pre-graduation lap text) | `:19` current; `:29` is the SESSION-107 as-executed entry and stands. |
| jack-ryan Gate-2 note · ledger L-54/L-67 · spec | other seams / run records — **stand**. |

---

## 7. ITEM 7 — the hand-back, and why it cost more than it was priced at

L-67(j) scoped this as *"grade-words in comments/docstrings/EMITTED metadata … value 3.0 UNCHANGED
and record-confirmed, so zero behavioral drift."* Comments and docstrings, yes. **But the sweep
found a TEST PIN on the retired grade:**

```
tests/test_kc2_locomotion.py:716      assert "NOT measured" in d["grades"]
```

That assertion pinned the cadence's **ADOPTED** grade — the grade that graduated to **MEASURED** at
L-67(g) on 36/36 records with zero variance. **Leaving it would have left the suite asserting a
claim the run has falsified by measurement.**

> ⚑ **THIS IS #72 CLAUSE 8 FIRING ON THE VERY HAND-BACK THAT CARRIES IT.** *"A hand-back scoped as
> 'a note edit' that is actually a live-constant edit plus a test-assertion edit plus a re-run is
> mispriced."* Scoped as comments + metadata; executed as comments + a live emitted string + a test
> assertion + a re-run. **Naming it is the point — the discipline predicted its own next instance.**

**What I changed and what I did not, stated so it can be audited rather than trusted:**
- The assertion now reads the **same field** carrying the corrected grade, plus the graduation
  history — so the *graduation* is pinned, not merely the new word.
- **No numeric assertion, tolerance, threshold or constant moved anywhere in that file.**
  `P05_DRIP_CADENCE_S == 3.0` is still asserted, two lines up, and I added it again beside the
  repaired assertion.
- **This is not a test edited to make a change pass.** The change *is* the grade move, ruled at
  L-67(g); the test's subject moves with the ruling. I am flagging it as **the highest-scrutiny
  item of this lap** for Gate-2, because "I repaired a test that was failing my change" and "I
  repaired a test that pinned a retired fact" look identical from outside and only one is legitimate.

### 7.1 The key-name call: ANNOTATE, DO NOT RENAME

`adopted_cadence_s` and `is_the_adopted_spec_value` say that **3.0 is the value the spec adopted** —
and the graduation did not change that. It *added a basis*; it did not un-adopt the constant. So the
names are not false, a name is a pin (**#67**), and `is_the_adopted_spec_value` is read downstream
at `test_kc2_locomotion.py:710`. **Renaming would move a contract in order to relabel a fact that
has not moved.** What *was* false is the `grades` **value**, and that is what the repair changed.

---

## 8. ITEM 8 — beat-5 re-entry: RECOMMENDATION, not a decision

**Beat 5's pause condition** (L-54(g)): *"volume without a kill term adds no discrimination;
C-1 gates."* **C-1 has landed. The stated condition is discharged.**

**But the fold reveals the discrimination is now gated on a different open item, and the honest
answer is that the blocker MOVED rather than cleared.**

**Measured, this lap** — cycle time with the board OFF vs ON (SHEET limb), 10 waves × 8 seeds:

```
mean sim OFF 18.587 s   ->   ON 19.887 s      mean shift  +1.300 s
per-wave shift, ONE-SIGNED:  +0.000 … +4.875 s   (0.000 at w4/w30; 4.875 at w90)
```

**Three things follow.**

1. **On the DB player-damage limb the ladder TIMES OUT** (measured: 0/4 cleared at waves 50 and 90).
   Volume there buys *less* discrimination than before, not more. On the SHEET limb it runs.
   **Which limb the ladder uses is E-6 / HALT-4's disposition, and this fold explicitly declined to
   make it.** A full ladder fired before that disposition would book the selection by default.
2. **The fold moves T-1 in the failing direction.** T-1's residual is on record at **+4.207 s**
   (sim slower than fixture, L-54(e)); the fold adds a one-signed **+1.30 s**. Volume would buy a
   *sharper measurement of a worse fit*. That is still information — but it is not the information
   beat 5 was paused for.
3. **Volume now buys one genuinely new observable it could not before:** the composition law is
   discriminating. `max()` and `+` separate (6.10–10.51 s at waves 10/50/90), and at **wave 90 the
   modal binding term FLIPS to `cumulative_kill`** — the first time in this run that the law's
   second term has bound anything. **A full ladder would census how many of the 92 waves are
   kill-bound vs arrival-bound**, which is a new shape fact and one the § 4.5 wall-shape metric
   consumes.

> ### RECOMMENDATION
> **RE-ENTER — but AFTER the player-damage limb is dispositioned, and RE-SCOPED to the new
> observable.** Fire beat 5 as a **binding-term census across all 92 band-A waves**, not as another
> T-1 fit attempt. If the conductor wants it sooner, it can run SHEET-limb-only with the limb
> labelled a **DECLARED SELECTION** — cheap and honest, but it books a selection this fold declined
> to make, and that should be a conductor's ruling with its own row, not a side effect of a batch.
>
> **Second-order note the conductor asked for at L-67(j):** the **§ 4.5 wall-shape rank consumes
> clear-time, and clear-time has now MOVED** (+1.30 s mean, one-signed, concentrated on the
> high-body waves). The seeded batch's HOLD is discharged on its *"stat fold lands"* condition —
> **but it must be re-run against the moved clear-times, not the pre-fold ones.** A batch computed
> on both would be comparing two different sims.

---

## 9. G-STATS readiness — can the 33rd check PASS now?

| predicate | state |
|---|---|
| eHP inputs MEASURED, every encoded body incl. summons | **967 / 968 (99.90 %)** — 1 INFERRED fallback, named |
| damage MEASURED | **953 / 968 (98.45 %)** — 14 MEASURED-ZERO-INCOMPLETE + 1 ABSENT, all named |
| folded into the sim's kill term | **eHP YES** (wired, tested). **Monster damage: NO SURFACE EXISTS** |
| truth-boundary tags read MEASURED | **YES** on every row; non-MEASURED rows carry their own token |

> ### VERDICT: **PASSABLE ON THE eHP LIMB. ONE COMMITMENT-LEVEL QUESTION BLOCKS A CLEAN PASS.**
>
> G-STATS says *"MEASURED … and folded into the sim's kill term."* **Monster damage can be MEASURED
> and cannot be folded into a kill term, because a kill term is not where it goes** — the kill
> term's two inputs are monster eHP and *player* damage; monster damage feeds the player's
> incoming-damage term, which the sim declares out of model (`player_hp` FLAT by construction;
> `monster_attack_model = abstract-schedule`). Building that surface needs an attack cadence, a hit
> model and a mitigation model — **three free parameters the charter forbids inventing.**
>
> **Reading (i)** — the clause's intent is Matt's R-KC2-8 words, *"I do not want to ship the baton
> without the actual monster stat tables"* ⇒ **a MEASURED damage table shipped on the baton
> satisfies it, and G-STATS PASSES today.**
> **Reading (ii)** — literal ⇒ **G-STATS cannot pass** until an incoming-damage model exists, which
> this run has not chartered. **Handed back. Not decided here.**

**Residuals, priced:**

| residual | price |
|---|---|
| `scavenger_h075` — 1 body, INFERRED fallback | **1 / 968 = 0.10 %** of the roster; the fallback is a measured sibling median |
| 14 MEASURED-ZERO-SWING-INCOMPLETE bodies | **1.45 %** of the roster; all are traps/crystals/turrets whose damage is wholly in the declared exclusion |
| emission-channel damage excluded | **median ×2.87** of consumed swing (flat magnitude, not DPS), sign POSITIVE, 818/953 bodies |
| level bracket | **4.736 %** band-wide; irreducible until B-KC2-C3 (`apl` source) closes |
| player-damage limb | **×130.8 … ×178.9** — E-6/HALT-4, **player-side, not a stat-table residual** |
| band B (s2) stats | **NOT MEASURED.** Out of this fold's declared scope |

---

## 10. What this lap did NOT do

**Did NOT:** change any default · move any pin, constant, threshold or tolerance · edit any
pre-existing test **assertion** except the one grade-word pin in § 7 (declared, reasoned,
flagged for Gate-2) · touch `export/` · `telemetry/` · `output/` · `generation/` · `element/` ·
`anchor/` · `foundation/` · `decisions-log.md` · `canonical/` · any vendor tree (READ-ONLY
throughout) · any other agent's note · pick the player-damage limb · measure band B · fold the
emission channels · resolve the G-STATS gate reading · decide beat-5.

---

## 11. Sitrep

I was sent to fold the monster stats into the kill term, and the fold worked; what I did not expect
was how much of the lap would be spent finding out that my own instrument was lying to me in two
different ways, both times in the direction of looking finished.

The first was that I wrote down a list of damage channels the table would not consume, and then
consumed them anyway. The table caught it, not a test — four rows came out with a minimum larger
than their maximum, which happens when you add a lightning bolt to a sword swing. The second was
that I took a level proxy from the pool when the game takes it from the slot, and I only found that
because a board somebody else built refused to agree with mine. Both errors are the same shape: I
had the right rule written down and the wrong rule running.

The result I most wanted to be able to report is one I can't take credit for. The declared zero,
which the run refused to estimate for months and carried as a named absence with a sign, turns out
to have been within half a second of the truth. Nobody could have known that. The absence was named
correctly, signed correctly, and refused correctly, and the reward for all that discipline is the
discovery that the honest answer and the easy answer were nearly the same number. That is worth
saying plainly, because the temptation next time will be to conclude that the estimate would have
been fine.

It would not have been. On the other player-damage limb the same board gives seventy-three seconds
a body and every wave times out. The two answers are a factor of a hundred and thirty apart, and the
only reason we know which one is near the truth is that both were carried as cited quantities
instead of one being averaged into a plausible middle.

The blade does not get sharper by cutting more. It gets sharper by noticing which edge was doing
the cutting.

---

*Filed 2026-08-08 by gamora under KC2-SIM ruling R-L67-1 (gandalf, RUN-CONDUCTOR). Read-only against
every vendor tree; zero external fetches. Committed in both repos per the standing authorisation;
**neither repo pushed** — the conductor centralises under R-KC2-10.*
