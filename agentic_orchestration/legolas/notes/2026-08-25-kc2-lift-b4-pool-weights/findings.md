# KC2 LIFT RUN · Lap **B4** — within-pool member roll weights, waves 150–160

> **CONDUCTOR CAPTURE NOTE (gandalf RUN-CONDUCTOR, 2026-08-25):** the harness blocks seat-authored `findings.md` writes (third instance this run; md-b4app-2d precedent); the seat returned the complete findings text in its lap result and the conductor captured it here VERBATIM (transport HTML-entities de-escaped: `&lt;`→`<`, `&gt;`→`>`, `&amp;`→`&`). Authorship is the legolas seat's. Seat commit: `a2c0dd91` (7 lap artifacts, verified). Fold: LIFT ledger L-9.

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-25 · **Conductor:** gandalf (RUN-CONDUCTOR)
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-25-kc2-lift-run-charter.md` · **Authorizing ruling:** R-L2-3
**Commissioned by:** elrond's curation finding **A-B4-1**, `agentic_orchestration/elrond/notes/2026-08-25-kc2-lift-b2-b8-curation.md`
**Substrate:** Edition III of record, `~/Games/vendor/grim-dawn-edition-III-20260808/` — **READ-ONLY, nothing sealed touched (K-7)**
**Artifacts:** `b4_pool_members_w150_160.csv` (576 rows) · `b4_extract.py` · `b4_controls.py` · `b4_diagnostics.json` · `tpl_proxypool.txt` · `tpl_proxypoolequation.txt` · `pins.json` (16 inputs+outputs, full sha256)

---

## § 0 — Headline

**The hole A-B4-1 named is closed, and it was not a hole of the shape the commission assumed.**

- **576 / 576 slots carry an explicit integer weight. ZERO NULLs.** The pre-named honest-fail fallback (R-L2-3) was **not needed for weights** — it fired on nothing. The weights were never missing from the *corpus*; they were dropped by the *flattening* that produced `pe6…_v2.csv`.
- **The per-slot surface is 14 fields, not 3.** `database/templates/proxypool.tpl` declares **7 per-slot fields × 2 independently-indexed families** (normal, champion), i = 1..15. The commission named three; censusing first was load-bearing.
- **The absences are real, they are in the OPTIONAL fields, and they are now countable**: 66 slots with no `limit`, 468 with no `minPlayerLevel`, 554 with no `maxPlayerLevel`, 572 with no `alwaysSpawn`. Every one carries an explicit `<field>_state = ABSENT` cell. Nothing defaulted, nothing inferred.
- **Four positive controls pass 4/4**, each against an independently-produced lineage artifact.

---

## § 1 — Method, and what it deliberately did not do

**The reader is IMPORTED, not re-implemented.** `Ed.winner()` from `gamora_kc2_c1_closure_ed3_2026_08_08` — the same reader that produced band-A/band-B monster life — applies the **L-33 / C-9 overlay law: `.arz` overlay is WHOLE-RECORD REPLACEMENT, never a field merge.** A second reader is a second thing that can drift, and a field-merge reader would resurrect deliberately-deleted slots. The eight archives are searched in the canonical order `base · gdx1 · gdx2 · gdx3 · sm_mod · sm1 · sm2 · sm3`; the last carrier wins outright.

**The index-pairing law (L-65(e)) is obeyed and was never relaxed.** `name<i>` pairs with `weight<i>` / `limit<i>` / `minPlayerLevel<i>` / `maxPlayerLevel<i>` / `alwaysSpawn<i>` / `levelVarianceEquation<i>` **at the same index**. A stem is never unioned across indices. The champion family is a **parallel array**, not a continuation of the normal one — the two are indexed from 1 independently, and merging them would be the exact error gamora's `pool_slot_proxies` docstring records having made and caught.

**Scan overshoot is detected, not silently truncated.** The template declares i = 1..15; the extractor scans to **40** so that a record exceeding its own template's ceiling would be *reported*. **None does** (`overshoot: []`). Slot indices are also checked for contiguity — **no holes** (`holes: []`) in any of the 117 pools, either family.

---

## § 2 — Coverage

### 2.1 Pools and slots

| | count |
|---|---|
| Pool references in `pe6…_v2.csv` at waves 150–160 | **156** rows |
| Distinct pool records | **117** |
| Pools **resolved** in Edition III | **117 / 117 (100 %)** |
| Pools unresolved | **0** |
| Normal-family slots | **262** |
| Champion-family slots | **314** |
| **Rows emitted** | **576** |
| Rows carrying `POOL_UNRESOLVED` (honest-fail) | **0** |

**Archive winners:** `sm3` 62 · `sm_mod` 26 · `sm1` 22 · `sm2` 7. **Winner agrees with the pinned CSV's `pool_archive` on 117/117** — no archive-attribution disagreement.
**Template:** `database/templates/proxypool.tpl` on **117/117**. No template mismatch.

> ⚑ **Row count differs from elrond's forecast, and the basis is why, not an error.** A-B4-1 projected *"518 rows for the 150–160 slice"*, counted over the CSV's **156 pool-reference rows** (a pool referenced at three waves was counted three times, and only regular rosters were summed). This lap emits **576 rows at the (pool × family × slot) grain — 117 distinct pools, deduplicated, both families.** The wave context is preserved as a `waves_referencing` column rather than by row multiplication. Neither number is wrong; they count different things, and the difference is recorded so a Wave-3 census does not read it as a shortfall.

### 2.2 Per-slot field coverage — every absence named

| field | family | PRESENT | ABSENT | template default |
|---|---|---|---|---|
| `name<i>` | normal | **262** | 0 | *(none declared)* |
| `weight<i>` | normal | **262** | **0** | *(none declared)* |
| `levelVarianceEquation<i>` | normal | **262** | 0 | *(none declared)* |
| `limit<i>` | normal | 196 | **66** | ⚑ *(none declared)* |
| `minPlayerLevel<i>` | normal | 102 | **160** | ⚑ *(none declared)* |
| `maxPlayerLevel<i>` | normal | 17 | **245** | ⚑ *(none declared)* |
| `alwaysSpawn<i>` | normal | 4 | **258** | ⚑ *(none declared)* |
| `nameChampion<i>` | champion | **314** | 0 | *(none declared)* |
| `weightChampion<i>` | champion | **314** | **0** | *(none declared)* |
| `levelVarianceEquationChampion<i>` | champion | **314** | 0 | *(none declared)* |
| `limitChampion<i>` | champion | **314** | 0 | *(none declared)* |
| `minPlayerLevelChampion<i>` | champion | 6 | **308** | ⚑ *(none declared)* |
| `maxPlayerLevelChampion<i>` | champion | 5 | **309** | ⚑ *(none declared)* |
| `alwaysSpawnChampion<i>` | champion | 0 | **314** | ⚑ *(none declared)* |

**Slots with unrecoverable weights: 0.** The honest-fail path exists in the emitter and is exercised by no row.

---

## § 3 — Template-declared semantics, VERBATIM

Extracted from `database/templates.arc` → `proxypool.tpl` (sha256 pinned). Descriptions are authored **only on index 1**; indices 2..15 carry `description = ""`. Quoted exactly:

| variable | type | `description` (verbatim) | `defaultValue` (verbatim) |
|---|---|---|---|
| `name1` | `file_dbr` | `"spawn record"` | `""` |
| `weight1` | `int` | **`"pooled weight of selection"`** | `""` |
| `levelVarianceEquation1` | `file_dbr` | `"available if difficulty exceeds value"` | `""` |
| `limit1` | `int` | **`"number available to spawn"`** | `""` |
| `minPlayerLevel1` | `int` | `"minimum average player level for which to use the record"` | `""` |
| `maxPlayerLevel1` | `int` | `"maximum average player level for which to use the record"` | `""` |
| `alwaysSpawn1` | `bool` | **`"force spawn of object"`** | `""` |
| `nameChampion1` | `file_dbr` | `"spawn record"` | `""` |
| `weightChampion1` | `int` | `"pooled weight of selection"` | `""` |
| `levelVarianceEquationChampion1` | `file_dbr` | `"available if difficulty exceeds value"` | `""` |
| `limitChampion1` | `int` | `"number available to spawn"` | `""` |
| `minPlayerLevelChampion1` | `int` | `""` | `""` |
| `maxPlayerLevelChampion1` | `int` | `""` | `""` |
| `alwaysSpawnChampion1` | `bool` | `"force spawn of object"` | `""` |

Pool-grained scalars (all present on 117/117 except `ignoreGameBalance`, present on 92):

| variable | type | `description` | `defaultValue` |
|---|---|---|---|
| `spawnMin` / `spawnMax` | `int` | `""` | `"1"` |
| `championMin` / `championMax` | `int` | `""` | `"0"` |
| `championChance` | `real` | `""` | `"0"` |
| `proxyPoolEquation` | `file_dbr` | `"ProxyPoolEquation record"` | `""` |
| `ignoreGameBalance` | `bool` | `""` | `"0"` |

⚑ **Two things the template says that are worth reading twice.**

1. **`levelVarianceEquation<i>`'s description is mis-transplanted.** It reads *"available if difficulty exceeds value"* — the description of a numeric gate — on a `file_dbr` field that points at an `lv*` proxy record. The **observed values are the lv-proxy family** (`lv6_hero` ×315, `lv3_strong` ×61, `lv4_champion+` ×40, `lv7_uber hero` ×39, `lv8_boss+` ×38, `lv2_normal` ×36, `lv5_elitechampion` ×24, `lv4_champion` ×13, `lv3_strong+` ×10 — 576/576 present), which is what L-65(e) and `pool_slot_proxies` already treat it as. **The template's own prose is unreliable here; the values are not.** Recorded so nobody lifts the description as the semantics.
2. **NO per-slot field declares a `defaultValue`.** So for the 66 limit-absent slots, *the template cannot tell you what an absent `limit` means.* See § 5, O-1.

---

## § 4 — Findings

### **F-B4-1 · ⚑ FIRST-ORDER — this lap supplies exactly the two inputs the incumbent code named as its reason for refusing to weight.**

`simulation/kc2/wave_engine.py::_emit`, verbatim, in the shipped engine:

> *"⚑ The name draw is UNIFORM over the roster, which is the incumbent behaviour and is retained deliberately: the decoded picker is WEIGHTED and decrements per-entry `limitN`, but the sidecar publishes only the SUM of those limits (`UNREACHED-I22-1`). **Modelling the weighting without the per-entry limits would be an invention**; the capacity SUM is what was decoded, and capacity is what is applied."*

and `UNREACHED-I22-1` itself (`simulation/AGENT_STATE.md`, verbatim):

> *"per-entry `limitN` values are not in the sidecar, only their sum, so which roster NAME is exhausted first is unmodelled. **Count-inert, identity-live.**"*

**Both preconditions are now on the table**: `weight<i>` at 576/576 and `limit<i>` at 510/576 with the remaining 66 explicitly ABSENT rather than guessed. The refusal was correct when it was made and is **no longer forced** — the substrate it was waiting on is this CSV. It stays a refusal until someone rules on **O-1** below, because the 66 absent limits still stand between the parts and a faithful picker.

**This finding is the lap's reason to exist and it was not in the commission.** The commission described a curation gap; the gap turns out to be an *engine* carry with a named address.

### **F-B4-2 · The uniform fallback is wrong on 34 of 81 multi-slot normal pools, and the error is large.**

- **81** pools have a normal-family roster; **35** are single-slot (uniform is trivially exact).
- **34 pools carry more than one distinct weight** — uniform is *demonstrably* the wrong mix there.
- Total-variation distance between the true weighted mix and the uniform mix: **mean 0.0494 over all 81 pools; mean 0.1176 over the 34 that differ; max 0.2222.**
- Worst within-pool weight ratios: `chthonianvoid_ambush_t3` **6.67×** (15 vs 100) · `aetherialbloater_t3` **5.00×** · `giant_t3` **4.55×** (33 vs 150) · `cultistvitality_t3` **4.00×** · `yetidire_t3` / `gargoyle_t3` **3.03×**.
- Weight vocabulary is small and integer-valued: `100`×169, `75`×40, `50`×39, `25`×5, `33`×4, and one each of `15 · 20 · 34 · 40 · 150`.

⚑ **The champion family is the opposite case, and it is a genuine simplification, not an assumption.** **All 314 champion slots carry weight `100`** and **all 314 carry `limitChampion = 1`.** So for champions the uniform draw *is* the weighted draw, and capacity is exactly the roster size. A-B4-1's composition worry is **confined to the normal family**. Naming this halves the exposure.

### **F-B4-3 · ⚑ A player-level CEILING exists on 22 slots, and at this band it points the roster error in the OPPOSITE direction from the weights.**

`maxPlayerLevel<i>` — *"maximum average player level for which to use the record"* — is declared on **22 slots across 10 pools**, with values **15, 30, 35, 50, 70**:

| pool | family | slots | max |
|---|---|---|---|
| `poolshero/chthoniandreadguard_hero` | champion | 6,7,8,9,10 (`chthonianfiend_h01..h05`) | **15** |
| `poolsbasicgdx1/chthonianrylok_t3`, `chthonianservitor_t3`, `wendigo_t3` | normal | 5 slots | 30 |
| `poolsbasicgdx2/gargoyle_t3`, `statue_t3` | normal | 6 slots | 30 |
| `poolsbasic/chthonianvoid_ambush_t3` | normal | 9,10,11 (`chthoniandevourer_a01/b01/b02`) | 35 |
| `poolsbossgdx2/fatherkymon` | normal | 2 (`korvaak_lieutenant_01`) | 50 |
| `poolsbossgdx1/fleshweaverkrieg`, `poolsbossgdx2/korvaakmessenger` | normal | 1 each | 70 |

**If the ceiling is enforced at a Crucible band-B sitting, these 22 members are EXCLUDED from the roll while appearing in the pinned CSV's flattened roster list.** So the flattened roster is not merely un-weighted — for these ten pools it is **over-inclusive**, and `fleshweaverkrieg` / `korvaakmessenger` are **single-slot boss pools whose only member carries a ceiling of 70**.

⚑ **I am NOT ruling that the exclusion happens.** Three things are true and none of them is a verdict: (a) the field is declared with that description; (b) the values are these; (c) **nothing in `simulation/kc2/` references `minPlayerLevel`, `maxPlayerLevel` or `alwaysSpawn` at all** — grep returns zero hits across the seam and zero hits across `data/kc2/*.csv`. Whether the shipped picker consults the gate, and what *"average player level"* resolves to in Crucible, are **binary-decode questions** (O-2). The rows are emitted with the gate values present so the question is answerable rather than invisible.

`minPlayerLevel<i>` is the mirror field: **108 slots** (102 normal + 6 champion) across 17 distinct values `4,5,8,10,12,15,16,20,25,30,35,40,45,50,55,60,70`. At a band-B sitting every one of these *passes*, so the floor is the inert half and the ceiling is the live half — which is precisely backwards from the intuition that a level gate at wave 155 would be a floor.

### **F-B4-4 · `alwaysSpawn<i>` = *"force spawn of object"* is declared on 4 slots, and 3 of them are boss-pool slot 1.**

| pool | family | slot | member |
|---|---|---|---|
| `poolsboss/ghoul_nercropolis` | normal | 1 | `boss&quest/ghoul_necropolis_01` |
| `poolsboss/skeletalgolem_ilgorr` | normal | 1 | `boss&quest/skeletalgolem_stepsoftorment_01` |
| `poolsboss/witchgod_sentinel` | normal | 1 | `boss&quest/witchgod_finalboss` |
| `poolsbasic/skeletalgolem_t3` | normal | 2 | `skeletalgolem_c01` |

This is a **roll-order rule, not a weight**: a forced member bypasses the weighted draw. It is per-slot, it is in the template, it is unmodelled in `simulation/kc2/`, and it was not in A-B4-1's three-field list. Zero champion slots carry it.

### **F-B4-5 · A-B4-2's `proxyPoolEquation` is not an unknown — it is the IDENTITY map, and it is the same record for all 117 pools.**

Every pool in the band declares `proxyPoolEquation = records/proxies/proxypoolequation_01.dbr`. That record lives in **`base` only** (single carrier, no overlay), and reads in full:

```
templateName          = database/templates/proxypoolequation.tpl
spawnMinEquation      = "poolValue * 1"
spawnMaxEquation      = "poolValue * 1"
championMinEquation   = "poolValue * 1"
championMaxEquation   = "poolValue * 1"
```

**All four are `poolValue * 1`.** So the pool's declared `spawnMin/Max` and `championMin/Max` pass through unscaled at this band. This does not answer all of A-B4-2 (roll order, RNG stream, and per-spawn-point vs global weight normalisation remain open — see O-3), but it **removes one of its three unknowns from the "assume" column into the "cited" column**, and it does so for 117/117 pools rather than by sampling.

### **F-B4-6 · Six ORPHAN per-slot gate fields on two pools — authoring residue in the winning record itself.**

| pool | slot | field | value |
|---|---|---|---|
| `poolsbasic/chthonianleech_t3` | 4 | `maxPlayerLevel4` | 25 |
| `poolsbasic/chthonianleech_t3` | 5 | `minPlayerLevel5` / `maxPlayerLevel5` | 12 / 25 |
| `poolsbasic/chthonianleech_t3` | 6 | `minPlayerLevel6` / `maxPlayerLevel6` | 12 / 25 |
| `poolsbasic/skeletonrevenant_t3` | 5 | `maxPlayerLevel5` | 30 |

These are indices with a **player-level gate and no `name<i>`** — a gate on a slot that has no member. Both pools are **single-carrier (`sm_mod` only)**, so this is **not** an overlay artifact of whole-record replacement; it is residue left in the authored record when a roster was shortened.

**They are correctly excluded from the emitted rows** (`name<i>` is the slot existence key), and `holes: []` confirms the *populated* indices remain contiguous 1..n. Reported because a future extractor that keys on `weight<i>` or on "any indexed field" instead of on `name<i>` would manufacture six phantom slots — and the six values look plausible enough to survive review.

---

## § 5 — Open questions, each with what would close it

**O-1 · What does an ABSENT `limit<i>` mean to the shipped picker?** The decode says the picker **filters `limit != 0`** (`Game.dll+0x1035841a`) and **decrements the taken entry** (`0x103584fc`). If an absent int field reads as **0**, those 66 slots would be filtered out entirely — which cannot be right, since Lap V's own decode treated absent-limit pools as **`regular_capacity = inf`** and that reading reproduces the band's counts. So the two readings disagree and **the template declares no default to adjudicate between them** (§ 3). *Closes on:* a binary check of the DBR loader's absent-int behaviour, or an explicit ruling ratifying Lap V's `inf`. **Do not let this default silently**; 39 of 81 normal pools have at least one limit-absent slot, and 4 pools have *no* limit on *any* slot.

**O-2 · Is the player-level gate consulted, and what is "average player level" in Crucible?** See F-B4-3. *Closes on:* binary decode of the picker's gate test, plus the Crucible's definition of the average. 22 slots and two single-member boss pools hang on it.

**O-3 · A-B4-2's remainder is NOT closed by this lap.** Still open: (a) whether pool weights normalise **per spawn point** or globally — the incumbent `_weighted_pick` normalises per spawn point, which is a *code* fact, not a decoded one; (b) whether the within-pool member draw is weighted-**with** or **without** replacement — the `limit` decrement at `0x103584fc` reads as *without*, but that is one address, not a proof; (c) which RNG stream the member draw consumes. B2 § 6.2's two-idiom finding (`RandomUniformLocked::IGenerate` vs CRT `rand()%100`, *"except pet-ignore, which is `%101`"*) is exactly why *"assume uniform"* is not safe here. **`UNREACHED-V4` already refuses to fold draw ORDER; this lap does not disturb that refusal.**

**O-4 · Waves 150 vs 151.** Lap V's band is 151–170, so **8 of the 117 pools are referenced only at wave 150** and are outside C-2's cross-check. Their slot rows are emitted and pass C-1, C-3 and C-4; they simply have no independent capacity oracle. Named so a census does not read 109 ≠ 117 as a gap.

---

## § 6 — Positive controls (`b4_controls.py`, re-runnable, **4/4 PASS**)

| control | what it proves | result |
|---|---|---|
| **C-1** ordered `member_record` list per (pool, family) vs the pinned `pe6…_v2.csv` `roster_records` / `champ_records` | the **index pairing** and the **overlay winner choice** — a wrong archive or a mis-paired index reorders or repopulates the list | **117/117 pools, 0 mismatches, both families** |
| **C-2** per-slot `limit<i>` SUM vs Lap V's independently decoded `regular_capacity` / `champion_capacity` | **the lift's whole thesis**: the sum that was the only available grain decomposes into parts, and the parts add back exactly (ABSENT → `inf`, as Lap V read it) | **109 pools, 0 mismatches** |
| **C-3** the run ledger's own hand-quoted slot (L-53) | byte-level agreement with a claim written by a different agent from a different pass | `skeletonrevenant_t3` slot 4 = `skeleton_d01.dbr`, **weight 75, minPlayerLevel 45, limit 2** — **exact** |
| **C-4** every `member_record` resolves in some archive (the G-7 dangling class) | no phantom members carried into the lift | **576 slots, 0 dangling** |

> C-2 is the one that matters. It is not a self-consistency check — Lap V decoded those capacities from the binary and published only sums; this lap read the parts from the corpus. **Two independent paths, agreeing on 109 pools, both families.**

---

## § 7 — Emitted schema (`b4_pool_members_w150_160.csv`, 576 rows × 30 cols)

Grain: **(pool_record × family × slot_index)**. Rows-not-fields; every optional field ships with an explicit companion `_state` column so an absence is a *value*, never a blank to be interpreted.

```
pool_record · pool_archive_winner · pool_archive_csv · pool_template
family ∈ {normal, champion} · slot_index
member_record
weight              + weight_state                    ⚑ 576/576 PRESENT
limit               + limit_state                     ⚑ 510 PRESENT / 66 ABSENT
min_player_level    + min_player_level_state          ⚑ 108 PRESENT / 468 ABSENT
max_player_level    + max_player_level_state          ⚑  22 PRESENT / 554 ABSENT
always_spawn        + always_spawn_state              ⚑   4 PRESENT / 572 ABSENT
level_variance_equation + level_variance_equation_state   ⚑ 576/576 PRESENT
spawn_min · spawn_max · champion_min · champion_max · champion_chance
proxy_pool_equation · ignore_game_balance
slot_weight_share        ⚑ DERIVED: weight / Σ weight within (pool, family). Marked derived here
family_weight_total          so the baton lift never mistakes it for a corpus value.
waves_referencing · pool_kinds
```

**Baton-lift shape** (`(value, scope, provenance)`, per elrond's ROWSET sketch): the `pool_member` rowset A-B4-1 proposed lands **576 rows with `value(member_weight)` POPULATED, not NULL**, scope `per(pool_record, family)`, provenance `{archive_winner, pool_record, slot_index, sha256 of the winning .arz}`. The **NULL** cells that remain are the four optional gates, each with its own `_state` column, so a Wave-3 census can assert *"576 member rows, 576 weights, 0 fabricated, 66 declared-absent limits"* by counting rather than by trusting.

---

## § 8 — HALT check

**No HALT.** Every condition met was modelled or is reported as an open question with the evidence that would close it. Nothing was improvised: the two places where the corpus does not answer (O-1 absent-limit semantics, O-2 gate enforcement) are **named and left open** rather than defaulted, and the derived column that *is* an inference (`slot_weight_share`) is labelled as derived in the schema itself.
