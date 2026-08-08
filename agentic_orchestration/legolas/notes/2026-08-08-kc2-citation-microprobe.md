# KC2-SIM — citation micro-probe: band-A eHP inputs · movement citations · arena geometry (F-12a)

**Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, Phase D — commissioned at ledger **L-43**
**Commission:** three citation surfaces for the **F-12 locomotion amendment** — C-1 (band-A per-record eHP
emission) · C-3 (movement-speed citations + engine m/s hunt) · F-12a (arena geometry)
**Disposition:** **Task 1 CLOSED-DB-CITED · Task 2a CLOSED-DB-CITED · Task 2b PARTIAL (unit CLOSED,
rate NAMED-ABSENT-CONFIRMED) · Task 3 CLOSED-LEVEL-CITED (first-of-kind)**
**External fetches:** ZERO. Everything below is corpus-resident.
**Scratch:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-citation/`
**Artifacts:** `notes/2026-08-08-kc2-citation-microprobe/` (6 CSVs, hashes § 0.3)

---

## 0 — PROVENANCE (mandatory, per ledger L-2)

### 0.1 Edition-II pin — every numeric value in Task 1 and Task 2a

`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`, eight-archive overlay stack, **last-wins,
WHOLE-RECORD replacement** (never field-merge — L-33 C-9). Resolver `scratch/…/t0_lib.py`.

| # | archive | md5 | bytes |
|---|---|---|---:|
| 1 | `database/database.arz` | `20d47784be5f93124636992f9e5562e2` | 58 338 379 |
| 2 | `gdx1/database/GDX1.arz` | `6e09ba92fed5f200d5cd1858cb1ddf31` | 42 398 951 |
| 3 | `gdx2/database/GDX2.arz` | `45160bf9c535b207134f006663a0e6a2` | 33 106 854 |
| 4 | `gdx3/database/GDX3.arz` | `08365db74863744fea2cfc7254666f55` | 47 334 429 |
| 5 | `mods/survivalmode/database/SurvivalMode.arz` | `ac4ad3539196ccf26b6f8be6ab7d3a8b` | 7 052 806 |
| 6 | `survivalmode1/database/SurvivalMode1.arz` | `3fd5a20f084ec9c4fbca326e0d1a1fb4` | 2 459 167 |
| 7 | `survivalmode2/database/SurvivalMode2.arz` | `a15a93ec279ea064be95ae4421756e2c` | 2 351 568 |
| 8 | `survivalmode3/database/SurvivalMode3.arz` | `e3ce424133993d2483c2daa57d1017ab` | 3 919 713 |

### 0.2 Edition-I pin — DISCLOSED EXCEPTION for Tasks 2b and 3

**The Edition-II pin ships NO `.arc` at all.** Its entire contents are 8 `.arz` + 8 `Text_EN.arc`
(verified by full-tree enumeration: 18 files, no `Scripts.arc`, no `templates.arc`, no `Maps.arc`,
no `Levels.arc`). The Lua, template and level surfaces the commission asked me to search therefore
came from the Edition-I full install, **pre-FoA** (`/Users/admin/Games/vendor/grim-dawn/`, depot
2026-07-23; no `gdx3`, no `survivalmode3`) — the same lane opened at U-8/L-9 and graded there.

| surface | md5 | bytes | grade |
|---|---|---:|---|
| `database/templates.arc` | `80a3330bfa594dbfbec739a800e2d4a2` | 780 972 | TPL-CITED (Edition-I, freshness-probed) |
| `resources/Scripts.arc` | `2662cf369622c7be0c8292d077a610e4` | 287 114 | SOURCE-CITED (Edition-I) |
| `gdx1/resources/Scripts.arc` | `78b80140de527d57e3c5960c1b51246a` | 231 213 | SOURCE-CITED |
| `gdx2/resources/Scripts.arc` | `314af0ea68d94e678a4f42295edc696c` | 178 004 | SOURCE-CITED |
| `mods/survivalmode/resources/Scripts.arc` | `466595ebc7eabc1f89b5f1ab1d17d37d` | 72 984 | SOURCE-CITED |
| `survivalmode1/resources/Scripts.arc` | `3dbb9812c3e238d3434f03dc4aabca08` | 33 853 | SOURCE-CITED |
| `resources/System.arc` | `33aef29015e31fc28289a1b9e6f1ebb2` | 816 021 | searched, NOT a config surface (43 files: 8 `.msh`, 35 `.tex`) |
| `mods/survivalmode/resources/Maps.arc` | `425dd222ae8234bb9013955ca75e9e6e` | 9 738 368 | LEVEL-CITED (Edition-I) |
| `survivalmode1/resources/Maps.arc` | `8cb164ebd2b00c900145cc4377ef8049` | 14 976 494 | LEVEL-CITED |
| `survivalmode2/resources/Maps.arc` | `8e3decbfee51c06b57fad5c2076010a2` | 3 104 975 | LEVEL-CITED |

**Named freshness gap (bounded, class = U-8's G1).** Edition-I carries no `survivalmode3` resources,
so any FoA-added arena or arena edit is invisible to Task 3. **Bound:** Edition-II declares
`tier18/19/20spawnpoint01.dbr` — three tier-1 emitter placements my Edition-I maps cannot show. They
sit **entirely outside band A** (waves 1–93 = tiers 1–10) and outside s2 (waves 150–160 = tiers 15–16),
so the gap does not touch either calibration band. It does mean the ten-arena roster below is a
**pre-FoA** roster.

### 0.3 Artifacts (beside this note)

| file | rows × cols | sha256 |
|---|---|---|
| `kc2_s1_banda_record_inputs.csv` | 895 × 86 | `ac50ef778555ec26e76559eb5932f2dd0b478f8f4f37038464c09a8d777f657e` |
| `kc2_s1_banda_placement_inputs.csv` | 1 589 × 36 | `1f1b9ee533f10c38df381175c915bd5bbf2d3c0063f2a38874335c4713209a74` |
| `kc2_s1_banda_wave_cells.csv` | 93 × 6 | `eb58cf0d62375001346553fa8f2e71e5fd6e87819af183170004b5fedcd36d3d` |
| `kc2_crucible_emitter_geometry.csv` | 332 × 15 | `ece0c345f14e2da1af63bd2e388b7dc0be32a1e0c703636b192924f84649cff9` |
| `kc2_crucible_patrolpoints.csv` | 173 × 11 | `106facbaac3cb7b44991b569b1b2934738a3eee83145fb8e095071ae93693747` |
| `kc2_crucible_arena_placements.csv` | 895 × 7 | `f05c66f1fcec57d28e937601225901e1bfab5c4f6a5a36e41bec274d7f7df66d` |

---

## 1 — FINDINGS TABLE (one read for the conductor)

| # | Finding | Grade |
|---|---|---|
| **1** | **Band-A eHP coverage 7/896 → 895/896 (0.8 % → 99.9 %).** Per-record INPUTS emitted (bio curve + value at level, armorbase record + array cell, own modifier, Ultimate term, § 10.7 cell), never a summary total. **100 % of resolved records carry BOTH a bio `characterLife` curve and an `armorbaseNN` passive** — the § 6.2b four-link chain runs on every one, no gaps. | **CLOSED-DB-CITED** |
| **2** | **The emitter's chain code reproduces the L-33 closure 8/8 EXACT, residual 0.** Same code path, run at wave-160 parameters, lands Zantarin/Aleksander 3 722 896 · Kubacabra 2 955 796 · Galakros 2 295 755 · Bileeater 484 095 · Revenant 468 504 · Shard 103 912 · Archer 41 237. The band-A emission is not a new model; it is the ratified one, extended. | **VERIFIED** |
| **3** | **The +3-offset vs apl-103 ambiguity is IMMATERIAL for band A.** L-33 left two non-discriminable readings of the level rule. Run across all **13 level-variance proxies** used in band A, both readings return the **identical integer band on 13/13** — so the open question cannot move a single band-A eHP. The ledger's "non-discriminable from one wave" is now "non-discriminable AND consequence-free on this band." | **DB-CITED (closes a live ambiguity for band A)** |
| **4** | **`levelVarianceEquation` is PER-ROSTER-SLOT, not per-pool.** A pool carries `levelVarianceEquationN` alongside `nameN`/`weightN`/`minPlayerLevelN`/`limitN`, so *the same monster record spawns at different levels from different slots*. 1 589 (pool × slot) placements across 309 band-A pools bind 13 distinct level proxies, charLevel **102 – 109**. A per-record eHP scalar would have been wrong by construction; the placement CSV carries the grain. | **DB-CITED** |
| **5** | **ONE band-A roster entry points at a record that does not exist:** `records/creatures/enemies/hero/scavenger_h075.dbr` — referenced by a band-A pool, absent from all eight archives. 895 of 896 resolve. | **BLOCKED-SUBSTRATE (1 record)** |
| **6** | **`characterRunSpeed` census, band A: n=895, median 1.0, mean 1.0358, range 0.60 – 2.00.** 191 records exactly 1.0; **311 below 1.0; 393 above.** Emitted per-record. Confirms and refines HALT-2's corpus-wide census on exactly the population the sim needs. | **CLOSED-DB-CITED** |
| **7** | **A SECOND, uncited locomotion term exists: `characterRunSpeedJitter`** — n=810, median **15.0**, mean 12.2, max 50.0 (85 records carry none). Nothing in the spec, the build, or HALT-2 mentions it. If it is a ± % dispersion on run speed, arrival is a *distribution*, not a time. | **DB-CITED — NEW, unmodelled** |
| **8** | **THE MECHANISM IS SOURCE-CITED, AND IT IS NOT "PATH TO THE PLAYER."** `sm_mod/game/events/survivalevent.lua:552` — every non-ambush Crucible spawn is linked to a **named patrol-point group** and told to *"follow the set path"*; **17/17 tier modules set `patrolPoint = "PatrolPoint_Attack"`** (all 200 waves). Ambush spawns are excluded by `IsAmbush()`. Monsters converge on an arena-resident **destination**, not on a pursuit vector. | **SOURCE-CITED (Crate's own comments)** |
| **9** | **The engine's world LENGTH unit is the METRE, by Crate's own annotation** — four template fields declare m/s: `travelSpeed` / `tailTravelSpeed` *("beam velocity in meters per second")*, `particleSpeed` *("meters/second")*, `textureSpeed` *("meters/second")*. **The `(radius, v_ref)` degeneracy therefore half-collapses: radius is no longer free — it is measurable in metres, and § 3 measures it.** | **CLOSED-DB-CITED (unit)** |
| **10** | **The character locomotion RATE in m/s is NAMED-ABSENT-CONFIRMED.** Enumerated surface: 260 Lua files / 97 907 lines (complete engine-API census — **zero** speed/velocity/rate call), `templates.arc` 18 999 Variables (`characterRunSpeed` carries **no description**; no `baseRunSpeed`/`defaultRunSpeed` exists anywhere), `gameengine.dbr` 366 fields (caps are **percentages**, not rates), `System.arc` (meshes/textures only). `v_ref` stays DECLARED. | **NAMED-ABSENT-CONFIRMED** |
| **11** | **`gameengine.dbr` asymmetry, load-bearing for C-3: `playerRunSpeedCapMax = 135` but `monsterRunSpeedCapMax = 500`.** The fixture is AT its cap; monsters have 3.7× the headroom. Also `alertDistance = 6.0`, `meleeTargetDistance = 2.4`, `meleeAutoTargetDistance = 4.0`, `monsterRunSpeedCapMin = [20, 25, 30]` by difficulty. | **DB-CITED** |
| **12** | **A whole per-record AI-locomotion surface was never opened: `controller`.** Every band-A record points at a `ControllerMonster` DBR (**126 distinct**, 0 missing). It declares `MaxPursuitDistance` (**125.0** on 868/895), `ViewDistance` (**80.0** on 868), `PursuitTime` (**10 000 ms**), `RoamBehavior`/`RoamDistance`, patrol-idle timings, `EmoteBeforePursuingChance`, and swing pauses. Emitted per-record (27 columns). `character.tpl` adds **`walkDistance`** — *"Distance below which to walk when pursuing"* (n=677, median 4.5 m). | **DB-CITED — NEW, unmodelled** |
| **13** | **F-12a CLOSED: arena geometry IS level-resident, and is now extracted.** § 10.6's "arena geometry is mostly NOT DB-resident, and the sim must not go looking for it" was true **of the Edition-II fetch**; Edition-I ships `Maps.arc`. **10 Crucible arenas** (`survivalworld_a…j`, tagged `tagSurvivalArena_01…10`), `.map` container format decoded first-of-kind, **7 473 placements** parsed across 16 map files. | **CLOSED-LEVEL-CITED (first-of-kind)** |
| **14** | **The build's uncited `Arena.emitter_radius_m = 30.0` is wrong in BOTH directions, and the error is structural.** Measured against the `PatrolPoint_Attack` centroid: **ring emitters (p01–p04, p06) median 37.53 m** (n=322, 15.5–47.9) — 30.0 sits at the **9.3rd percentile**; **p05, the ambush point, median 10.17 m** (n=10, 1.7–17.2). **The ring is 3.7× the ambush radius.** One radius for six emitters is the defect, not the value. | **MEASURED** |
| **15** | **Spawn point 1 is placed PER TIER** — up to **17.4 m** of spread across a single arena's 15–17 tier placements. p01 is not one site; the emission keys it `p01_tierNN`. | **MEASURED** |
| **16** | **Bearing-match against galadriel's footage is SUGGESTIVE, NOT DISCRIMINATING.** Best s1 fit `survivalworld_f` (mean |Δ| 11.8°), runner-up `survivalworld_a` (13.1°) — both inside her ±15°. `arena_id` stays a DECLARED parameter; it is now declared **over a cited 10-member enumeration** rather than over nothing. | **PARTIAL** |

---

## 2 — TASK 1 + 2a · BAND-A PER-RECORD INPUTS — **CLOSED-DB-CITED**

### 2.1 The band is reproduced EXACTLY before anything is emitted

Band A := distinct monster records reachable in Crucible waves **1…93**, **p06 EXCLUDED**
(`S1_BONUS_SPAWNS_ENABLED = False`, `calibration.py:224`). From `pe6_crucible_wave_pools.csv`:

| quantity | this probe | gamora (`calibration.py:513-515`, beat-3 § 5) |
|---|---:|---:|
| distinct **regular** records | **466** | 466 |
| distinct **champion** records | **434** | 434 |
| **union** | **896** | 896 |
| overlap (both roles) | 4 | (implied by 466+434−896) |

Exact on all four. The p06 exclusion is load-bearing — including spawn point 6 gives 469/446/911, and
the wave bound is not (1…93 and 2…93 are identical: wave 1 introduces no record wave 2 lacks).

### 2.2 What is emitted, and why it is INPUTS

The commission's instruction — *"emit the per-record INPUTS … NOT just a computed total"* — is
structurally necessary here, not stylistic. The § 6.2b chain is

```
L    = floor( proxy levelVarianceEquation(apl=100) ) + 3        # +3 MEASURED, DB-source NAMED-ABSENT
base = characterLife(bio, L)                                     # winner-only overlay
M    = 1 + 5.80 + G(wave)/100 + armorbaseNN[L-1]/100             # ADDITIVE
eHP  = floor( base × M )
```

and **two of its four links vary with placement, not with the record**: `L` comes from the pool's
per-slot `levelVarianceEquation`, and `G` comes from the wave. A per-record eHP number would have
silently averaged over both. So:

- **`kc2_s1_banda_record_inputs.csv`** (895 × 86) — record-intrinsic terms. `bio_record` +
  `bio_archive` + `life_equation`; `armorbase_record` + `armorbase_archive` + `skillLevel` equation +
  the array cells at the record's own charLevel min/max; `own_characterLifeModifier` **with
  `own_applied = NO`** carried explicitly (L-33 C-5 falsified it — Bileeater's +50 breaks its own
  exact closure by +4.41 %); `ultimate_pct = 580` with its record and archive; the § 10.7 record,
  archive and **lookup law as a string**; `base_life_at_charLevel_min/max`. Plus all of § 2.4's
  locomotion columns.
- **`kc2_s1_banda_placement_inputs.csv`** (1 589 × 36) — the **(pool × slot × record)** grain: slot
  weight, `minPlayerLevel`, `limit`, the bound `levelVarianceEquation` record and its two equations
  **verbatim**, charLevel under **both** readings, `armorbase_index` and `armorbase_pct` at the used
  level, `base_life_at_charLevel`, and the pool's band-A wave span.
- **`kc2_s1_banda_wave_cells.csv`** (93 × 6) — wave → `gladiator_array_index` → `characterLifeModifier`
  cell, each row restating the corrected law. Band A spans **G = 95.0 (wave 1) … 156.0 (wave 93)**.

Column names follow the r2 CSV where they overlap (`record`, `winner_archive`, `bio_record`,
`bio_archive`, `life_equation`, `armorbase_record`, `armorbase_skill_level_eq`, `armorbase_index`,
`armorbase_pct`, `ultimate_pct`, `own_characterLifeModifier`, `own_applied`, `charLevel`,
`charLevel_grade`, `monster_class`).

### 2.3 Self-check — the chain code IS the L-33 chain

Run at wave-160 parameters against the eight camera-measured bodies:

| body | L | armorbase | `M` | base_life | eHP | measured | residual |
|---|---:|---|---:|---:|---:|---:|---:|
| Zantarin · Aleksander | 109 | 05[108]=125 | 11.29 | 329 751.6885 | 3 722 896 | 3 722 896 | **0** |
| Kubacabra P1 | 109 | 05[108]=125 | 11.29 | 261 806.5764 | 2 955 796 | 2 955 796 | **0** |
| Galakros | 106 | 05[105]=103 | 11.07 | 207 385.3354 | 2 295 755 | 2 295 755 | **0** |
| Aetherial Bileeater | 112 | 04[111]=129 | 11.33 | 42 726.8744 | 484 095 | 484 095 | **0** |
| Death Revenant | 109 | 05[108]=125 | 11.29 | 41 497.2687 | 468 504 | 468 504 | **0** |
| Aleksander's Shard | 109 | 04[108]=125 | 11.29 | 9 203.9473 | 103 912 | 103 912 | **0** |
| Skeletal Archer | 109 | 01[108]=110 | 11.14 | 3 701.7872 | 41 237 | 41 237 | **0** |

**8/8 EXACT** under `G = GLAD[159] = 324` (the cell LABELED 160). This is the ratified chain, extended
— not a second model needing its own gate.

### 2.4 The band-A eHP scale, for the conductor's intuition

| wave | G | n | min | median | mean | max |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 95 | 895 | 17 371 | 357 588 | 358 736 | 2 967 765 |
| 50 | 110 | 895 | 17 683 | 363 642 | 364 868 | 3 017 227 |
| 93 | 156 | 895 | 18 639 | 382 207 | 383 673 | 3 168 913 |

By class at wave 93 — Boss 3 168 913 (n=1) · Quest median 1 285 651 (n=64) · Hero 382 207 (n=445) ·
Champion 173 945 (n=241) · Common 78 499 (n=144).

**⚑ Consumer warning.** The **G term moves only +64 % across the whole of band A** (95 → 156) while
the class spread is **×40** (Common 78 k → Boss 3.17 M). The dominant term in band-A opposition eHP is
**which record is drawn**, not which wave it is drawn in. A model that scales a class average by the
wave cell will be wrong in exactly the way T-1's per-wave predicate punishes.

### 2.5 Locomotion columns (Task 2a, shared file per the commission)

Per-record, in `kc2_s1_banda_record_inputs.csv`:

| field | n | min | median | mean | max |
|---|---:|---:|---:|---:|---:|
| `characterRunSpeed` | 895 | 0.600 | **1.000** | 1.0358 | 2.000 |
| `characterRunSpeedJitter` | 810 | 0.0 | **15.0** | 12.21 | 50.0 |
| `walkSpeed` | 887 | 0.450 | 1.000 | 0.9173 | 1.500 |
| `walkDistance` | 677 | 0.0 | 4.500 | 4.843 | 10.0 |
| `ctrl_MaxPursuitDistance` | 895 | 75.0 | **125.0** | 123.49 | 125.0 |
| `ctrl_ViewDistance` | 895 | 15.0 | **80.0** | 78.04 | 80.0 |
| `ctrl_PursuitTime` (ms) | 895 | 10 000 | 10 000 | 10 011 | 12 000 |

Also emitted: `characterRunSpeedModifier`, `min/maxRotationSpeed`, `characterAttackSpeed`,
`walkUsesRun`, `disableMovement` (**absent on 895/895** — nothing in band A is exempt from the movement
manager), `distressCall`/`distressCallRange`/`distressCallTime`, and 27 `ctrl_*` columns.

---

## 3 — TASK 2b · THE m/s HUNT — **PARTIAL: unit CLOSED, rate NAMED-ABSENT-CONFIRMED**

### 3.1 The searched surface, enumerated

| surface | extent | result |
|---|---|---|
| **Lua source** (6 `Scripts.arc`, base + gdx1 + gdx2 + sm_mod + sm1 + sm2) | **260 files, 97 907 lines** extracted | **ZERO** occurrences of `speed`, `velocity`, `m/s`, `per second`, `world unit`, `distance` |
| Lua **engine API**, complete census | 19 namespaces, **83** distinct `Namespace.Method`, **49** distinct object `:Method` | **no speed / velocity / rate / unit-conversion call exists**. Movement surface is exactly: `LinkPatrolPointGroup(string)` · `Run()` · `MoveAction(id, coords, bool)` · `SetCoords` · `Teleport*`. None takes or returns a rate. |
| `base/libs/vector.lua` | 83 lines, complete | pure vector math (`Length`, `LengthXZ`, `Unit`, dot, cross) — **unit-agnostic, no constant** |
| `templates.arc` | **18 999 distinct Variables** | `characterRunSpeed` has **no description**; **no** `baseRunSpeed`/`defaultRunSpeed`/`movementSpeed` Variable exists anywhere |
| `gameengine.dbr` | 366 fields | every `*RunSpeedCap*` is `"Index by difficulty 0 to 2"` — **percentages**, not rates |
| `System.arc` (base + gdx2) | 44 files | 8 `.msh` + 36 `.tex` — **not an engine-config surface** |

### 3.2 What DID close — the world unit is the metre

Four template Variables carry Crate's own unit annotation, verbatim:

| Variable | template | description |
|---|---|---|
| `travelSpeed` | `skill_attackspelldrain.tpl` | *"Head of the beam velocity in **meters per second**"* |
| `tailTravelSpeed` | `skill_attackspelldrain.tpl` | *"Tail of the beam velocity in **meters per second**"* |
| `particleSpeed` | `weathersystem.tpl` | *"Particle speed (**meters/second**, particle based systems only)"* — default `16.0` |
| `textureSpeed` | `lineeffect2.tpl` | *"Speed at which the texture moves along the beam in **meters/second**"* — default `1.0` |

This is the HALT-8 precedent exactly (Crate's *"Delay between projectile launches (seconds)"* pinned
`projectilePeriod`). A field whose value is denominated in m/s fixes the engine's length unit as the
**metre** — so `placementExtents = 8.0`, `alertArea = 100.0`, `alertDistance = 6.0`,
`meleeTargetDistance = 2.4`, `MaxPursuitDistance = 125.0`, `ViewDistance = 80.0` and **every arena
coordinate in § 4 are metres**.

**Consequence for L-43's C-3 degeneracy.** The ledger states *time ∝ radius / v_ref ⇒ (radius, v_ref)
collapse to ONE free timescale.* That degeneracy **half-collapses**: the radius half is no longer free.
It is a measured quantity in a cited unit (§ 4.3). One free scalar remains, and it is `v_ref` alone.

### 3.3 What did NOT close, and why it is a real negative

No corpus artefact converts the dimensionless `characterRunSpeed` multiplier into m/s. The multiplier's
referent (100 % = X m/s) lives in the executable or in root-motion animation data, neither of which is
in any pin. **HALT-2's CLOSED-BY-TYPE verdict stands, now with an enumerated search surface behind it.**

Two flanking facts the amendment should carry anyway:

1. **The cap asymmetry.** `playerRunSpeedCapMax = 135` vs `monsterRunSpeedCapMax = 500`
   (`bossRunSpeedCapMax = 500`, `absoluteRunSpeedCapMax = 350`). The fixture is *at* its ceiling
   (`FIXTURE_RUN_SPEED_PCT = 135`); monsters are not near theirs. Any model asserting the player
   out-runs the board must survive that.
2. **`characterRunSpeedJitter`** (median 15.0 over 810 band-A records). If it disperses run speed,
   the arrival term is a distribution and a single `v_mob` under-describes it. **Named, not modelled.**

### 3.4 The bonus — the mechanism itself is source-cited, and the spec's phrasing is off

`sm_mod/game/events/survivalevent.lua`, verbatim, Crate's comments intact:

```lua
--     'patrolPoint'    - patrol point group the spawns should head to upon spawning, set as a String [optional]
...
waveEvent.proxy[id] = Proxy.Create(waveEvent.waves[id][waveEvent.waveIndex][randomizer], waveEvent.coords[id].origin, true)
waveEvent.proxy[id]:SetCoords(waveEvent.coords[id])

-- set the spawns to patrol if a patrol point group was provided
if waveEvent.proxy[id]:IsAmbush() == false && waveEvent.patrolPoint != nil then
    waveEvent.proxy[id]:LinkPatrolPointGroup(waveEvent.patrolPoint)
end

-- Execute the proxy to dispense monsters and follow the set path
waveEvent.proxy[id]:Run()
```

**17/17 Crucible tier modules** (`tier01waves.lua` … `tier17waves.lua`, sm_mod + sm1) set
`survivalModeEventParameters.patrolPoint = "PatrolPoint_Attack"`. All 200 waves.

Three consequences the locomotion lap should absorb:

1. **F-12's diagnosis is confirmed at the source level.** The board is not static in the fixture —
   monsters are explicitly told to move on spawn. "Spec-described, build-omitted" is right.
2. **But "monsters path to the player" is NOT what the engine does.** They path to an
   **arena-resident patrol-point group** — a fixed convergence zone. Pursuit of the player is a
   *separate* controller behaviour, gated by `ViewDistance = 80 m`, bounded by
   `MaxPursuitDistance = 125 m` and `PursuitTime = 10 s`. The correct model is *travel to the
   convergence zone, then engage under controller rules*, which is **less** body-count-dependent than
   a pursuit model and therefore a better fit to the fixture's r = +0.154.
3. **p05 is excluded by construction.** `IsAmbush() == false` gates the link, and § 10.6 already
   names p05 the ambush point — the mechanism and the geometry (§ 4.3: p05 median radius **10.17 m**
   vs ring **37.53 m**) agree independently.

---

## 4 — TASK 3 · F-12a ARENA GEOMETRY — **CLOSED-LEVEL-CITED (first-of-kind)**

### 4.1 The four surfaces the commission named, answered

| surface | result |
|---|---|
| **the spawnpoint `.dbr` records** | **NO geometry.** `tier01spawnpoint01.dbr` is 7 fields: `Class=ScriptEntity`, `editorMesh`, `editorScale`, `onAddToWorld`, `onRemoveFromWorld`, `pathing=False`, `templateName`. § 10.6 correct. Edition-II carries 28 such records (incl. FoA's tier18/19/20). |
| **`proxypool` fine-print** | **NO geometry.** The 79-field pool record carries roster, weights, `minPlayerLevel`, `limit`, **`levelVarianceEquationN`**, `spawnMin/Max`, `champion*`, `proxyPoolEquation`, `ignoreGameBalance`. Zero positional fields. |
| **Lua arena scripts** | **NO literals — but the mechanism.** Coordinates are read at runtime: `waveEvent.coords[id] = entity[id]:GetCoords()` (`survivalevent.lua:398`). The Lua *consumes* level-resident geometry; it never declares it. |
| **level / map records** | **YES — and this is the finding.** Edition-I ships `Maps.arc`; Edition-II does not. |

### 4.2 The `.map` container, decoded

`survivalworld_a…j.map` — **10 distinct Crucible arenas** across three archives (sm_mod 6, sm1 8,
sm2 2; 16 files total, sm_mod/sm1 overlapping a–f), tagged **`tagSurvivalArena_01` … `_10`** with
level names (`SurvivalMode_Tomb`, `_Desert`, `_Forest`, `_Legion`, `_Udenbog`, `_DarkForest`,
`_Eldritch`, `_Basalt`, `_Void`, `_PerpetualNight`).

Format, solved empirically (magic `MAP\x09`; all offsets little-endian):

```
header   : [pstr "PatrolPoint_Attack"][pstr "Patrol Points"][u32 n]
           n x { [16B uid][u32 len][path][16B uid][f32 x][f32 y][f32 z] }
...
strings  : maximal contiguous run of [u32 len][records/….dbr]      (106-183 entries per map)
placements: [u32 count] then count x VARIABLE-length records:
              +0   9 x f32   orientation basis
              +36  3 x f32   world position (x, y, z)  -- METRES (§ 3.2)
              +48  u32       kind
              kind == 0 -> +52 u32 index into the string table          (56 B total)
              kind == 1 -> +52 20B control-object uid                   (72 B total)
```

**Decode verification, two independent legs.** (a) The layout was *solved*, not assumed — accepted only
where **every** index in the section is a valid table index, for **16/16** map files (7 473 placements).
(b) The header patrol group and the placement section are separately encoded and must agree: control-object
**counts match 16/16 EXACT**, and **155/173 positions (89.6 %)** coincide to 3 dp — the residual being
non-`PatrolPoint_Attack` control objects that the header group does not enumerate.

### 4.3 The measured geometry — F-12a's parameter, cited

Reference frame is the **`PatrolPoint_Attack` centroid** (the convergence zone of § 3.4), **not**
`playerspawnpoint` — the player spawn is the level ENTRY, tens of metres outside the arena
(arena b: player spawn Z = 26.2 vs patrol centroid Z = 64.7).

| emitter | n | min | median | mean | max |
|---|---:|---:|---:|---:|---:|
| **ring (p01–p04, p06)** | 322 | 15.52 | **37.53** | 37.39 | 47.89 |
| p01, band-A tiers 1–10 | 160 | 28.17 | 38.51 | 37.53 | 47.89 |
| p02 | 15 | 31.15 | 37.71 | — | 47.67 |
| p03 | 16 | 33.37 | 39.42 | — | 46.34 |
| p04 | 16 | 28.81 | 38.45 | — | 47.34 |
| p06 | 16 | 27.29 | 36.12 | — | 46.97 |
| **p05 — the ambush point** | 10 | **1.70** | **10.17** | 9.65 | **17.15** |
| patrol ring itself | 173 | — | 18.85 | — | 30.07 |

**The build's `Arena.emitter_radius_m = 30.0` sits at the 9.3rd percentile of all 332 measured emitter
radii.** It understates the ring by ~25 % and overstates the ambush point by ~3×. **The defect F-12a
named is confirmed and localised: it is not that 30.0 is the wrong number, it is that ONE radius cannot
describe six emitters whose ring : ambush ratio is 3.7×.** Under-declaring the freedom hid the
structure, exactly as F-12a says.

Also measured, and not previously modelled: **spawn point 1 is placed per tier**, spread up to
**17.36 m** within one arena across its 15–17 tier placements (`survivalworld_b`). The emission keys it
`p01_tierNN`; band-A (tiers 1–10) spread runs 0.31 – 16.39 m by arena.

### 4.4 What this bounds without fitting anything

- `ViewDistance = 80 m` (868/895 band-A records) **exceeds every measured emitter radius** (max 47.89 m).
  Every ring spawn is inside monster sight of the arena centre at t = 0.
- `MaxPursuitDistance = 125 m` (868/895) exceeds every arena's full diagonal.
- p05's `alertArea = 100.0` (§ 10.6, byte-identical at 107/107 sites) likewise covers the whole arena.

**Nothing here is a fitted parameter.** Each is a DB or level constant that *bounds* the geometry the
sim declares, which is the provenance-ladder upgrade F-12a asked for.

### 4.5 `arena_id` — PARTIAL, honestly

Matching galadriel's ESTIMATED-FOOTAGE ±15° bearings against the decoded emitter bearings:

| footage set | best fit | mean \|Δ\| | runner-up |
|---|---|---:|---|
| s1, 4 arrivals (3.0 / 5.2 / 6.9 / 9.6 o'clock) | `sm_mod/survivalworld_f` | 11.8° | `survivalworld_a` 13.1° |
| s2 wave 160, 4 arrivals (1.8 / 10.5 / 4.5 / 7.5) | `sm_mod/survivalworld_a` | 12.7° | `survivalworld_f` 14.9° |
| s2 wave 151, 2 arrivals (9.9 / 2.2) | `sm_mod/survivalworld_a` | **6.0°** | `sm1/survivalworld_a` 8.7° |

Both s2 sets favour `survivalworld_a`, which is mildly corroborating. But with six emitters, a ±15°
instrument and four observations, several arenas fit inside tolerance — **this does not identify the
fixture's arena and I decline to claim it does.** `arena_id` stays **DECLARED**; what changed is that it
is now declared over a **cited 10-member enumeration with per-arena geometry attached**, so the baton can
pin a real arena rather than a bare label. Discriminating it needs either a save-file level id or a
landmark match in the footage — a galadriel/save lane, not a datamine one.

---

## 5 — WHAT I DID NOT DO

- **No fitting, anywhere.** No parameter was solved against a measured clear time. § 4.3's radii are
  read out of level data; § 2's eHP inputs are read out of the DB.
- **No re-grading of T-1**, and no opinion offered on the tolerance form (C-5). Out of scope.
- **No spec or build edits.** Findings only; the conductor rules, gamora implements.
- **I did not model the patrol/pursuit mechanism.** § 3.4 reports what the source says. Whether the sim
  adopts *travel-to-convergence-zone* over *pursue-the-player* is a conductor ruling — but the two make
  different predictions about body-count dependence, which is the exact fingerprint F-12 turns on.

---

## 6 — OPEN ITEMS I AM HANDING BACK

| # | Item | Owner |
|---|---|---|
| **O-1** | `characterRunSpeedJitter` (median 15.0, n=810) is a DB-cited dispersion term with no place in the spec. Model, or declare out-of-model. | conductor → gamora |
| **O-2** | The `controller` surface (126 records, 27 emitted fields) is entirely unmodelled. `MaxPursuitDistance` 125 m · `ViewDistance` 80 m · `PursuitTime` 10 s · patrol-idle 1–5 s · `walkDistance` 4.5 m are all live locomotion parameters. | conductor → gamora |
| **O-3** | § 10.6's "arena geometry is NOT DB-resident, and the sim must not go looking for it" is now **false as written** — it was true of the Edition-II fetch only. Spec text needs the correction; the DECLARED-parameter ruling itself may or may not survive it. | conductor (SPEC-AUTHOR) |
| **O-4** | The Edition-II pin ships **no `.arc` at all**. The run-end hygiene row already asks for `templates.arc`; it should ask for **`Scripts.arc` + `Maps.arc` + `Levels.arc`** too, and for the FoA `survivalmode3` resources (closes U-8's G1 and this note's § 0.2 gap in one pull). | conductor → matt_to_do |
| **O-5** | `records/creatures/enemies/hero/scavenger_h075.dbr` is referenced by a band-A pool roster and exists in no archive. 1 of 896. Engine behaviour on a dangling roster entry is NAMED-ABSENT (same class as F-9's empty rosters). | conductor |
| **O-6** | `arena_id` discrimination needs a save-file level id or a footage landmark match. Datamine cannot settle it. | conductor → galadriel / save lane |

---

**Filed:** legolas (UNKNOWN-RESEARCHER), 2026-08-08, KC2-SIM Phase D. Every row DB-, TPL-, SOURCE- or
LEVEL-CITED, or explicitly graded NAMED-ABSENT / PARTIAL / BLOCKED-SUBSTRATE. Zero external fetches.
Zero fitted parameters.
