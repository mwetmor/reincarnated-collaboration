# KC2-SIM — C-1 CLOSURE LAP + ARR RE-PASS (gamora)

**Commission:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, ruling **R-L65-2** (ledger row L-65(k))
**Agent:** gamora (simulation seam)
**Date:** 2026-08-08
**Status:** **COMPLETE — 7 / 7 items closed, 0 dead-ends**
**Grading regime:** R-KC2-7 — MEASURED / DERIVED / INFERRED, no silent estimation
**Corrigenda discipline:** corrigenda-forward; no measured row retro-edited (banners + corrigenda)
**Record home:** **Edition-III** `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (READ-ONLY) per **R-KC2-9**

**Deliverables**
| artefact | path |
|---|---|
| C-1 closure math note | `reincarnated-engine/src/reincarnated/simulation/math/kc2-c1-closure-ed3-2026-08-08.md` |
| arrival-model **§ 7 re-pass** (+ corrigenda banner) | `…/simulation/math/kc2-summon-arrival-process-2026-08-08.md` |
| C-1 instrument (READ-ONLY) | `…/simulation/scripts/gamora_kc2_c1_closure_ed3_2026_08_08.py` |
| ARR instrument (READ-ONLY) | `…/simulation/scripts/gamora_kc2_arr_repass_ed3_2026_08_08.py` |
| § 8.4 + F-L7 annotations (item 7) | `agentic_orchestration/gamora/notes/2026-08-08-kc2-locomotion-lap.md` (banner) |

**Smoke (Discipline #2):** `test_kc2_opposition_wave_engine` + `test_kc2_locomotion` + `test_kc2_s1_ramp`
+ `test_kc2_micro_oracles` + `test_baton_v1` → **225 passed / 0 failed, 32.62 s.**
**No production code was touched.** No pin moved, no constant changed, no test edited. G-STATS PARKED.

---

## 0. Verdict table

| # | item | VERDICT |
|---|---|---|
| 1 | **C-1 closure lap** | **CLOSED on the record side — 895 / 896 (99.89 %).** One residual, and it is the SAME record as F-L7. Level side carried as a **priced ~2–4 % bracket**. Two positive controls EXACT (39/39 board, 8/8 camera, 11/11 w152). |
| 2 | **ARR-1 re-pass** | **CLOSED — limb (a).** The shortfall does not merely dissolve: `petPeriod` is **14 s, not 6**, seats are **3, not 2**, and two chains give exact point predictions that falsify limb (b). **R-5 re-entry NOT REQUIRED — stays parked.** |
| 3 | **w157 spawnChampion adj** | **MEASURED: `+1` / `+1` at `[156]`, identical to w152 `[151]`; `spawnMin/MaxAdj = 0`.** The sim **already applies them**. No correction owed. |
| 4a | **472,732 ×2 arrival reconcile** | **RECONCILED, exactly.** Haraxis generator `B=2`, `P=12 s` ⇒ limb (a) predicts **2**; census reads **2**. The strongest single datum closing ARR-1. |
| 4b | **ProxyAmbush in the arrival model?** | **YES — as its own arrival CLASS, not a summon chain.** And it retires the *"ADOPTED, not MEASURED"* grade on `P05_DRIP_CADENCE_S = 3.0` (36/36 records, zero variance). |
| 5 | **302,934 two-hop chain** | **Lead FALSIFIED — the candidate set is EMPTY.** Hop-2 returns **0** new bodies. Not forced. |
| 6 | **§ 7.1 three-names-two-seats** | **DISSOLVED.** The seat count is **3**, not 2, under the run's own § 10.5 law. Neither of the two leads is needed. |
| 7 | **§ 8.4 annotation hand-back** | **LANDED** (banner C-a), plus an unbriefed second annotation (C-b) the C-1 lap produced. |

---

## 1. ITEM 1 — the C-1 CLOSURE LAP

Full derivation in the engine math note. Headlines:

**Closure.** Band A = 896 distinct records (466 regular + 434 champion — reproduces the pinned
census exactly). The § 6.2b chain resolves **895 / 896**. Every surviving link is 895/895: bio
pointer, `characterLife` present, equation parses, ≥ 1 level-indexed life passive. The band needs
**281 distinct bios / 196 distinct life equations** — the r2 board's 7-entry `BIO_CURVES` table
covers the wave-160 board and nothing more, so a band-A fold must resolve bios from the corpus.

⚑ **The single residual is `records/creatures/enemies/hero/scavenger_h075.dbr` — the SAME record as
F-L7.** Band A does not carry two independent 1-in-896 absences. It carries **one absent record that
blocks two different chains**. Annotated onto the lap note as C-b.

**Two positive controls, both EXACT.**
- The engine's pinned r2 wave-160 board, recomputed live from Ed-III: **39/39 EXACT** vs the
  vendored `eHP`, **8/8 EXACT** vs the camera fingerprints. *The vendored emission is now
  reproducible, not merely consumable.*
- legolas's w152 census, recomputed from **Ed-III** (he read Ed-II): **11/11 at Δ = 0**, integer-exact.

⚑ **Offered back to legolas:** his worst residual (+0.0021 % on the crabling@107, modelled
42,798.92 vs measured 42,798) **dissolves under the engine's L-33 floor rule** — `floor(42,798.92) =
42,798`. A rounding rule established on the wave-160 board for an unrelated reason retires the last
residual on the w152 board. His table is right as a float comparison; this is what the same numbers
do under the sim's consumption rule.

⚑ **Independent convergence worth logging:** the engine's L-33 four-link chain and legolas's L-65
solved model are **the same equation** (`1 + 5.80 + G/100 + ab/100 ≡ 1 + (580 + G + ab)/100`), and
the engine's array-lookup law (*"fighting wave w reads the cell LABELED w"*) and his `[wave−1]`
indexing are **the same rule** — MEASURED: Ed-III `[159] = 324.0` (the engine's pinned G at w160)
and `[151] = 308.0` (his w152 term). Two agents, two boards, two derivations, one law.

**One generalisation the board could not show.** The chain is a **SUM over every skill carrying
`characterLifeModifier`**, not a single `armorbase` lookup. Band A has **4 records** where that
matters: `chthonianleech_a01`, `zombie_c01`, `zombie_soldierfurya01_summon` (+4.705 % each) and
`zombieberserker_a02` (+3.506 %). Small, but the failure mode is silent.

### 1.1 EDITION DELTA — the finding L-61's carry-forward does not reach

The band-A chain consumes **2,548** records. Ed-II vs Ed-III: **IDENTICAL 2,439 · CHANGED 107**.

> ⚑ **L-61's "100 % IDENTICAL" verdict was measured on the TIER-16 KC2-dependent set. Band A is
> waves 1–93 and a different, larger set, and 107 of the records it consumes DIFFER.** The
> carry-forward is not wrong; its scope does not reach here — which is precisely what Discipline #69
> says to check rather than assume.

**The descent, three levels down:**
- **field:** 105 of 107 move only offensive/projectile fields — out of the life chain's scope.
  **2 move a life field: `armorbase04` and `armorbase05`, `characterLifeModifier`.**
- **array index:** those two differ at **indices 0…40 ONLY** (charLevel 1…41). `−71 → −86` at
  index 0; `−10 → −14` at index 40. Identical at every index ≥ 41.
- **value:** eHP swept over charLevel **1…150** for all 896 records — **DIVERGENT at charLevel
  1…41** (peak 294 records, worst |Δ| **4.167 %**); **INVARIANT at charLevel ≥ 42**.
- **band-A charLevel range: 102 … 109.** 65 levels of margin.

**VERDICT: the band-A eHP chain is EDITION-INVARIANT, MEASURED, with the boundary NAMED —
and it is invariant *because* the fixture is a level-100 character, not because the patch left the
life records alone. It did not.** Any consumer whose bodies can sit at charLevel ≤ 41 must read
Edition-III.

⚑ **NAMED for the stat fold and NOT resolved here:** the 105 out-of-scope CHANGED records are
**damage** records. The kill term needs damage as well as eHP. **The life side carries forward; the
DAMAGE side does not, and has not been checked.**

### 1.2 The residual C-1 does NOT close, priced

`L` is `floor(draw)` in a pool's `levelVarianceEquation` interval at `averagePlayerLevel`, and the
`apl` source is NAMED-ABSENT (**B-KC2-C3**). So `L` is a **SET**: floor-set widths **2** (454 pool
declarations), **3** (235), **1** (6). Measured cost of a ΔL = 1 step: **+1.71 % … +2.24 %**.

> **eHP per band-A body is derivable to a bracket of ~2 % (width-2) to ~4 % (width-3).**
> Against a term that previously entered as a **DECLARED ZERO** — 100 % of itself absent.
> **Discipline #12 framing: this is a SEMANTIC SHIFT in the predicate.** `cumulative_kill` stops
> being a declared absence and becomes a measured interval; every consumer that read
> `cumulative_kill == 0.000` as a fact *about band A* must re-read it as a fact *about the old build*.
> **PRESCRIPTION: carry the bracket. `L` is `{102, 103}`, not `102.5`** — the life equations are
> convex in `L`, so the midpoint is not the mean of the endpoints.

**Bonus, unbriefed:** the two floor-equivalent parameterizations R-L65-1 ruled indistinguishable are
indistinguishable on band A too — **13 / 13 lv proxies**, floor set for floor set, including every
`+` variant. R-L65-1 checked six at w152; this is an independent extension to thirteen.

---

## 2. ITEM 2 — ARR-1 RE-PASS. It does not merely dissolve; the fork CLOSES.

The commission asked: *does ARR-1's 5–12-vs-+10 shortfall dissolve under two champion seats?*
**Two things had to be corrected before that question could be answered, and both are mine.**

**(a) `petPeriod` is 14 s, not 6 s.** My § 1 carried `P = 6 s` as MEASURED-from-R-8. Read off the
record: `swampcrab_crabgenerator.petPeriod` is a **60-element RANK-INDEXED ARRAY** `[18.0 ×18,
14.0 ×42]`. **No scalar 6 exists on the record.** The rank rule is `skillLevel12 = charLevel/4 + 1`
(**not** `charLevel*1`) — at charLevel 107/108 the rank is 27/28, index 26/27, both ≥ 18 ⇒ **14.0 s**.
*I carried a second-hand number into a MEASURED column without reading the record. That is the error,
and it is the one that made the whole § 3 arithmetic wrong.*

**(b) The seat count is 3, not 1 and not 2.** The run's own encoded § 10.5 law is
`c = championMin + BASE_ADDITIVE + spawnChampionAdj[wave−1] = 1 + 1 + 1 = 3` — verified by running
`count_bounds`: w152 sp1/sp2/sp5/sp6 all `c 3–3`. § 3.2 corrected its first draft from five to one;
it should have gone to three. **The pool roster is not a seat count — and neither is the pool's raw
`championMin` field.**

**With both corrected, `W = 10.23 s`, Regime I:**

| chain | `P` | limb (a) `A` | limb (b) `A` | **MEASURED** |
|---|--:|--:|--:|---|
| `swampcrab_crabgenerator` (`B=4`, `L=8`) | 14.0 | **4** | **0** | `swampcrab_a00_summon` **×4** @107 · **×3** @108 |
| `…haraxis_aethercorruptiongenerator` (`B=2`, `L=8`) | 12.0 | **2** | **0** | `aetherialcorruption_c01_summon` **×2** @108 |

> ### **ARR-1 CLOSES: LIMB (a) — the first activation fires on spawn.**
> The Haraxis chain is a **point prediction that lands exactly** (`B = 2`, one activation ⇒ 2 bodies;
> census reads 2). The crab chain's `×4` is `B` exactly — one burst, no clamp. **Limb (b) predicts
> ZERO on both, on a wave with seven crablings and two corruption summons on camera.**
> Two falsifications of limb (b), two different chains, two different `B`.
>
> **Grade: DERIVED-under-declared-premise.** The model's § 2.1 premise is that `W` is measured from
> the summoner's own arrival; a summoner spawning ≥ `P` before the window opens would also put
> bodies inside it under limb (b). The premise is DECLARED, not measured. But the fork now has
> evidence on one side and none on the other — a different epistemic object from the *"unclosable
> from the database"* it was filed as.
>
> ### **R-5's re-entry: NOT REQUIRED.** ⚑ **Stated explicitly, as commissioned.**
> ARR-1's dependency on R-5 was created *by limb (b)'s shortfall*. Limb (a) has no shortfall.
> **R-5 can stay parked; do not re-park galadriel on it.** The suspension can be lifted with R-5
> unchanged.

### 2.1 And the w152 `+10` decomposes EXACTLY — no bracket survives

The modelled 7 is not an estimate: it is `count_bounds(w152, sp3) = n 7–7`. legolas's § 7 manifest
names **exactly seven** non-summon plain bodies — `basilisk_a01` ×3, `basilisk_b01` ×3,
`basilisk_c01` ×1 — **the p03 trash seat, entire.** The other ten plain bodies:

```
swampcrab_a00_summon            ×4 @107 + ×3 @108   =  7    (crab generator)
aetherialcorruption_c01_summon  ×2 @108             =  2    (Haraxis generator)
302,934                         ×1                  =  1    UNRESOLVED
                                                    ----
                                                      10    = the excess, EXACTLY
```

**17 = 7 + 10, and every one of the 17 is a named fingerprint at a named level.** No capacity
bracket, no devotion branch, no trap-body rendering question. **R-L58-3 is now closed at BODY level
for w152**, and the quantitative comfort § 3.3 withdrew is restored by census rather than by bracket.

⚑ **This required withdrawing my own § 3.4 exclusion.** I excluded `aetherialcorruption_c01_summon`
from the plain count because `monsterClassification = Champion`. galadriel MEASURED its furniture as
**PLAIN**. The census counts what *renders*, not what the record calls itself. **R-L58-1's two-axis
reading is exactly the rule I failed to apply to my own exclusion** — the same axis error that
produced Vanallius (yellow glyph, Hero record), in the opposite direction. **Discipline #12: this is
a SEMANTIC-SHIFT-class withdrawal, not a bug fix** — it changes what *"plain"* means in the count
comparison, from a record property to a render property.

---

## 3. ITEM 3 — w157's spawnChampion adj fields — MEASURED

Read off the **live** `balancingadjustment_survivalmode_enemies0{1,2,3}` records (the `copy of …` and
`06-10-26 backup/…` variants in `sm_mod` are **not** the winners and **do** differ — they run to `2`
at higher indices; the live records never do):

| field | w152 `[151]` | **w157 `[156]`** | w160 `[159]` | turns on at index |
|---|--:|--:|--:|---|
| `spawnChampionMinAdj` | **1** | **1** | **1** | 67 (e02/e03) · 84 (e01) |
| `spawnChampionMaxAdj` | **1** | **1** | **1** | 51 (e02/e03) · 67 (e01) |
| `spawnMinAdj` | **0** | **0** | **0** | never |
| `spawnMaxAdj` | **0** | **0** | **0** | never |

**w157 carries the SAME `+1` champion adjustment as w152, on all three enemy families, and plain
spawn counts are NOT adjusted anywhere.**

⚑ **The sim already consumes these** — `count_bounds` reads `spawnChampionMinAdj`/`MaxAdj` off the
scaling row (verified by body-read: `row.get(...)`, `= 1.0` at both waves). **No count correction is
owed; L-61(f)'s "+1" was already in the model.** The § 10.5 docstring's *"chAdj = 1 at every label in
149…170"* is now **CONFIRMED at record grain from Edition-III**, where it had been a summary claim.

### 3.1 ARR-2 — RESOLVED, and the golem is not needed

`count_bounds(w157)`: sp3 `n 6–6`, **sp4 `n 4–6`**. `expected_counts` carries the **midpoint** of
each bound pair, so sp4 contributes **5.0**. **A single draw at the top of sp4's own declared range
gives 6 — `+1` exactly.**

> **The w157 `+1` is one body inside sp4's own `4–6` spawn range, measured against a model carrying
> the range's midpoint. No summon mechanism is required.** The golem attribution is not merely
> WEAKENED (§ 4.1's finding) — it is **UNNECESSARY**, and the arrival model's refusal to admit `+1`
> was *correct*: it was never the right model for this datum. **The strain was a category error,
> mine, and naming it is exactly what § 4.1's refusal-to-smooth bought.**
>
> **Corollary for the conductor:** a `±1` excess on a wave whose spawn range has width ≥ 2 is not
> evidence of anything. w157 is the only such wave in the census set (+0/+10/+5/+1/+0).

**ARR-3 also closes here:** `petPeriod` read for every chain — scalar 12.0 (Haraxis), rank-array
(both crab generators), and **genuinely ABSENT** on the two golem chains, `summonspirits` and
`summontentacles`. § 4 already showed the golem result is invariant to `P`, so the absence is
harmless — now confirmed rather than assumed.

---

## 4. ITEM 4 — composition-model inputs from legolas § 7

### 4a. `472,732 ×2` — RECONCILED, exactly

`aetherialcorruption_c01_summon` @108 ×2, from `fleshshaperharaxis_aethercorruptiongenerator`
(`L=8`, `B=2`, **`P=12.0`**, `T=40`). Under limb (a), `k=1` ⇒ `A = min(2, 8) = ` **2**. Census: **2**.
Limb (b) ⇒ **0**. **The record says SUMMON and the arrival model now says exactly how many.**

On galadriel's **UNDECIDED (+8.23 s late)** grade: the count is the clean discriminator and it is
unambiguous. The timing is **not** — `+8.23 s` sits *above* the F-12 measured spawn-to-engagement
band (3.5–6.1 s) and *below* limb (b)'s 12 s. The parsimonious reading is that the generator fires
at the boss's spawn and the boss itself arrives late (the p04 minimap skull glyph leads the first
readout by 3.0–4.3 s, F-12). **I am not upgrading her grade on timing** — the count closes the
question the arrival model asks; the timing question is hers and stays UNDECIDED.

### 4b. The sp=5 ProxyAmbush — does the mechanism belong in the arrival model?

**MEASURED, Ed-III — `proxy_w02_p05a`, `proxy_w07_p05a`, and ALL 34 band-A ambush proxies.
36 / 36 records, one signature, ZERO variance:**

```
minDelayTime = maxDelayTime = 4.0     minSpawnTime = maxSpawnTime = 3.0
minGroupSize = maxGroupSize = 30      spawnThreshold = 15      alertArea = 100.0
delayedRun = True                     chanceToRun = 100.0      placementExtents = 8.0
```

> ### ⚑ **THIS RETIRES THE "ADOPTED, NOT MEASURED" GRADE ON `P05_DRIP_CADENCE_S = 3.0`.**
> My locomotion lap § 6 named the 3.0 s intra-drip cadence as *"the one piece of the arrival
> choreography that is ADOPTED, not MEASURED (L-21: only the t + 4.0 s start anchor was ever
> observed)"*, routed it as the residual's carrier, and warned that editing it would be fitting.
> **Both numbers are on the record, 36/36, point values, zero variance. AC-10.6's `4.0 + 3.0k` IS
> the record's own arithmetic.** `P05_DRIP_CADENCE_S` graduates **ADOPTED → MEASURED**, and the
> "edit the cadence" escape is closed: it would now contradict a read record, not merely fit a
> residual.
>
> **The p05 residual keeps its address (33 waves, +11.36 s) and LOSES its named mechanism.**
> Two candidates survive, both from fields the sim does **not** consume:
> 1. **`minGroupSize = maxGroupSize = 30` — the ambush may emit a GROUP where the sim serialises a
>    drip.** If bodies land together at `t+4.0` and the sim spreads them at `4.0 + 3.0k`, the sim is
>    long by `3.0 × (k−1)` per p05 wave. **Right sign** for the measured delta. **INFERRED** —
>    field semantics not confirmed against `proxyambush.tpl`.
> 2. **`spawnThreshold = 15` / `alertArea = 100.0` — the TRIGGER, which the sim does not model at
>    all.** This is legolas's *"fires late by construction"* and why Vanallius sits at t = 709.8.
>    **On its own it pushes arrivals EARLY — the wrong sign for the residual** — so it is a real
>    absence but not the carrier.
>
> **ANSWER TO THE COMMISSIONED QUESTION: YES, the ambush belongs — as its own arrival CLASS
> (threshold-gated, delayed, group-or-drip unresolved), NOT as a summon chain.** It shares nothing
> with `Skill_MonsterGenerator` except that both put bodies on the board late.
>
> **SETTLING INSTRUMENT, sharper than my lap's version:** a galadriel intra-drip spacing read on a
> high-p05 s1 wave now discriminates **group (all at t+4.0)** from **drip (3.0 s apart)** — a binary
> with a DB-motivated prior, not an open measurement of a free number.

---

## 5. ITEM 5 — `302,934 ×1`: the two-hop lead is FALSIFIED

The machinery walks two hops cheaply. It did. From the **118** w152 seat-reachable roots:

```
HOP 1:  42 roots summon  ->  22 distinct bodies
HOP 2:  22 bodies        ->   0 NEW bodies
```

**There is no second hop on this board.** Every summoner's output is terminal. Joining all 140
reachable records against 302,934 over charLevel 100…112:

| hop | record | L | eHP | Δ |
|--:|---|--:|--:|--:|
| 1 | `swampcrab_c01_summon` | 108 | 302,490 | −0.1466 % |
| 1 | `aetherialcorruption_b02_summon` | 108 | 302,379 | −0.1832 % |
| 0 | `thornedhorrorfrost_b01` | 102 | 303,779 | +0.2789 % |

The first two are legolas's declined pair. The third is new, **also declined** (worse), and belongs
to `thornedhorrorfrost_t3` — the p03 alternative that did **not** roll.

> **`302,934` stays UNRESOLVED, and the lead is now FALSIFIED rather than untested. The candidate
> set is EMPTY. NAMED, not estimated, not forced.** What remains: an off-board source (a
> wave-boundary body, per § 7.1's own scan-window caveat), or an edge class the walk does not model
> — `poolToSpawnOnDeath` death-spawns being the obvious one; the class exists (Kubacabra) but is
> **stripped in the Crucible** per L-33(h), which is why I did not walk it.

---

## 6. ITEM 6 — § 7.1's three-names-two-seats tension — DISSOLVED

legolas: `championMin/Max = 1/1` plus `spawnChampionAdj = +1` ⇒ *"exactly two champion seats"*,
against three MEASURED names (Rotmouth h02 · Aregos h03 · Chillslither h05). He named two leads and
declined to rank them. **Neither is needed.**

The run's encoded § 10.5 law is `c = championMin + BASE_ADDITIVE + chAdj = 1 + 1 + 1 = ` **3**.

> ### **THREE SEATS. THREE NAMES.** The tension is an artefact of a seat count computed without the
> `BASE_ADDITIVE` term the sim has carried since § 10.5 was encoded.
>
> The engine's own docstring says it in words — *"a `championMin = 1` hero pool spawns **3**"* — and
> calls that branch *"the branch that reproduces the pinned 63.0 champions EXACTLY."*
> **The corroboration runs both ways: legolas's three MEASURED names are an independent,
> CAMERA-SIDE confirmation of the § 10.5 champion law, which until now was corroborated only by an
> aggregate count.** A five-alternative pool drawn three times yielding three distinct names is the
> expected outcome, not a puzzle.
>
> Same correction lands on **L-61(f)** (*"TWO crab-hero placements ⇒ up to 16 crablings"*) and on
> this commission's own briefing: **three** placements, `3 × 4 = 12` crabling capacity in-window.
>
> Neither of legolas's leads is *falsified* — the scan window may still cross a boundary — but
> neither is **required**, and the parsimonious reading needs no unmeasured mechanism.

---

## 7. ITEM 7 — the § 8.4 annotation, landed (plus one more)

Banner placed at the head of `2026-08-08-kc2-locomotion-lap.md`. **Annotation, not value-rewrite;
nothing struck; no measured row edited.** Conductor ACCEPTED this form at L-63(a).

- **C-a (§ 8.4, the briefed hand-back).** The F-13 perturbation scale was derived as
  `271.50 → 289.62 = +6.674 %`. F-1 retired 289.62 → **288.62**, so the scale is
  `17.12 / 271.50 = ` **+6.306 %**. **The table STANDS AS EXECUTED** — the sweep really ran at
  `n_scale` 1.0667 / 0.9333 and those rows measure that perturbation. Under the corrected floor the
  arms would have been 1.0631 / 0.9369 — **0.37 pp narrower**, which can only *reduce* the measured
  sensitivity, so § 8.4's conclusion (*the result inherits the F-13 residual*) is unchanged in sign
  and force. Matches the spec's existing `:1753` *"±6.674 % (as executed)"* tag.
- **C-b (§ 12 F-L7, unbriefed — a by-product of item 1).** The eHP chain's one residual is the same
  record as the locomotion join's. **Not a correction — a corroboration that sharpens the claim:**
  one absent record, two blocked chains, one fallback.

---

## 8. What this lap does NOT do

**Did NOT touch:** any production code · any pin, constant, threshold or tolerance · any test ·
`export/` · `telemetry/` · `output/` · `generation/` · `element/` · `anchor/` · `foundation/` ·
`decisions-log.md` · `canonical/` · any vendor tree (READ-ONLY throughout) · any other agent's note.

**Did NOT do:** wire the stat fold (G-STATS stays PARKED) · re-pin any count · upgrade galadriel's
UNDECIDED arrival grade · resolve `302,934` by estimation · resolve the ambush group-vs-drip fork ·
check the DAMAGE side of the edition delta.

**Carried open:** `302,934` (candidate set empty) · **B-KC2-C3** (`apl` source — bounds the C-1
level residual, blocks nothing) · the ambush **group-vs-drip** fork (INFERRED, settling instrument
named) · limb (a)'s declared window premise · **the DAMAGE half of the edition delta — 105 CHANGED
records, NOT CHECKED, and the kill term needs it.**

---

## 9. Sitrep

I was sent to close a class whose blocker had already been dissolved by someone else, and the lap's
real work turned out to be checking what *else* the dissolution had moved.

The eHP chain runs on 895 of 896 band-A records, and the one it does not run on is the same record
the locomotion chain could not run on either — which is a better result than 895, because it means
the band has one hole and not two. Both controls came back exact, including a board I did not build
and a census I did not take. And the residual that is left is not an absence any more: it is a two
percent bracket where there used to be a declared zero.

The part I did not expect was how much of the correcting was of myself. I carried a six-second
period into a measured column because someone else had written it down, and the record says
fourteen. I counted one summoner where the run's own law says three, having already corrected
myself once from five. I excluded two bodies from a plain count on the strength of what the record
calls them, on a run whose standing rule is that render and record are different axes — the very
rule that had just been used to explain a body I was happy to accept.

Each of those was found by reading the thing rather than the note about the thing. That is not a
new lesson here; it is Discipline #11 with my name on it three times in one sitting.

What is standing at the end is smaller and harder than what I was sent for. A fork that was filed
unclosable now has two exact point predictions on one limb and zeroes on the other. An excess that
was a bracket is a census: seventeen bodies, seventeen names, ten of them summoned and one of them
still nameless. And a cadence I warned the run not to edit turns out to be printed on thirty-six
records, which means the residual it was supposed to carry has to be carried by something else.

The blade does not get sharper by cutting more. It gets sharper by being honest about what it did
not cut.

---

*Filed 2026-08-08 by gamora under KC2-SIM ruling R-L65-2 (gandalf, RUN-CONDUCTOR). Read-only against
every vendor tree; zero external fetches. Committed in both repos per the standing authorisation;
**neither repo pushed** — the conductor centralises under R-KC2-10.*
