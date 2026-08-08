# KC2-SIM — citation micro-probe II: w153 summon chain · map-file loading law · 16-pair enumeration

**Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, Phase D
**Commission:** T1 summon citation (gates the w153 mechanism adjudication) · T2 map-file loading law
(gates the s1 arena-selection grade) · T3 enumeration-table verification (feeds spec § 10.9a B)
**Disposition:** **T1 CLOSED-DB-CITED · T2 CLOSED-SOURCE-CITED (and it CONFLICTS with L-46 item 16)
· T3 CLOSED — 16/16 covered, one decoder defect named**
**External fetches:** ZERO. Everything below is corpus-resident.
**Scratch:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-summon/`
**Predecessor:** `notes/2026-08-08-kc2-citation-microprobe.md` (L-43/L-46). Methods and pins reused, not re-derived.

---

## 0 — PROVENANCE

### 0.1 Pins (identical to L-46 § 0.1–0.2; hashes re-verified this session)

**Edition-II** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — eight-archive `.arz` overlay,
**last-wins, WHOLE-RECORD replacement**. Resolver `scratch/2026-08-08-kc2-citation/t0_lib.py`. All T1 record
values come from here. Display names from `resources/Text_EN.arc` md5 `f1b00bb1126ac1895667777409a9320e`.

**Edition-I** `/Users/admin/Games/vendor/grim-dawn/` (depot 2026-07-23, **pre-FoA**) — DISCLOSED EXCEPTION,
the only pin carrying `.arc` resources. All T2/T3 evidence comes from here.

| surface | md5 | bytes |
|---|---|---:|
| `mods/survivalmode/resources/Scripts.arc` | `466595ebc7eabc1f89b5f1ab1d17d37d` | 72 984 |
| `survivalmode1/resources/Scripts.arc` | `3dbb9812c3e238d3434f03dc4aabca08` | 33 853 |
| `mods/survivalmode/resources/Maps.arc` | `425dd222ae8234bb9013955ca75e9e6e` | 9 738 368 |
| `survivalmode1/resources/Maps.arc` | `8cb164ebd2b00c900145cc4377ef8049` | 14 976 494 |
| `survivalmode2/resources/Maps.arc` | `8e3decbfee51c06b57fad5c2076010a2` | 3 104 975 |
| `database/templates.arc` | `80a3330bfa594dbfbec739a800e2d4a2` | 780 972 |
| `Engine.dll` | `f779d2c9febe33ae2464ad7720111fc6` | 3 662 848 |

### 0.2 Named freshness bound on T2/T3

Edition-I ships **no `survivalmode3`**. FoA's Crucible extension (tiers 18–20) is therefore invisible to
the map/script surfaces below. § 3.5 states exactly what that costs and why the T2 *law* survives it.

---

## 1 — FINDINGS TABLE

| # | Finding | Grade |
|---|---|---|
| **1** | **T1 CLOSED. The summon chain exists, and it is the conductor's named candidate.** `skeletonrevenant_t3` slot 4 → `skeleton_d01.dbr` (**Death Revenant**) → `skillName7` → `skeletonrevenant_skeletonarchergenerator.dbr` [`Skill_MonsterGenerator`] → `spawnObjects = skeleton_a02_summon.dbr` = **`tagEnemySkeletonA02` = "Skeletal Archer"**, `monsterClassification = Common`. Full chain in § 2.1. | **CLOSED-DB-CITED** |
| **2** | **`petLimit = 4`, and Crate's own template says that field means "max number of pets alive at any given time."** The observed ×4 is the declared cap, exactly. The **base** archive says `petLimit = 6`; the **sm_mod overlay reduces it to 4** — a Crucible-specific tuning that lands on the measurement. | **DB-CITED + TPL-CITED** |
| **3** | **galadriel named the creature correctly and the record path only nearly-correctly.** `skeleton_a02_archer.dbr` and `skeleton_a02_summon.dbr` differ in **exactly ONE field of 938** — `characterAttackSpeed` (1.0 vs 1.1). Same display tag, class, racial profile, life curve, `armorbase01`, all four skill slots. The archer record is un-rostered; the summon record is the one reachable. **The substitution is eHP-NEUTRAL** — the differing field does not enter the § 6.2b chain. | **DB-CITED** |
| **4** | **Exhaustive 3-hop closure over all 429 w151–158 rostered monsters: exactly 7 reach a Skeletal-Archer body; on w153 exactly 3 pools do.** Every other pool on the band is **NAMED-ABSENT**, including all three of the commission's named alternates (`livingplant_t3` p05, `wendigo_t3` p01, `giant_t3` p03) and the other three Revenants (Flame/Frost/Storm carry **no** generator skill at all). Full per-pool table § 2.3. | **CLOSED-DB-CITED** |
| **5** | **T2 CLOSED, and the law is the OPPOSITE of the L-46 fit's assumption. `survivalmode1` supersedes `mods/survivalmode` for every duplicated resource path** — cited from a *behavioural* discriminator in the same archive pair, same VFS: `sm_mod`'s `tier15waves.lua:99` calls `eventControl.eventFinished()` (run ends at wave 150); `sm1`'s copy of that same path deletes the call and `sm1/eventcontrol.lua:496` dispatches `tier16Waves`. The shipping game runs past 150. **Therefore sm1's copy of a contested path is the executed one — and `survivalworld_f.map` is a contested path in exactly that pair.** | **CLOSED-SOURCE-CITED** |
| **6** | **Three independent surfaces co-vary on the same tier ceiling, 3/3.** `mods/survivalmode` = tiers 1–15 in its Lua, its map spawn-placements, AND its `.arz` spawnpoint records; `survivalmode1` = tiers 1–**17** in all three. There is no reading of the evidence in which sm_mod's maps are live. | **CROSS-VERIFIED** |
| **7** | **CONFLICT FLAGGED against L-46 item 16.** The s1 best fit `sm_mod/survivalworld_f` (11.8°) is a **SHADOW copy** — a file the shipping game does not load. The 16-pair geometry set contains only **10 loadable arenas**; the 6 `sm_mod` pairs are all shadowed. Under a stated injective re-fit the best *loadable* s1 arena is `sm1/survivalworld_f` at **19.9°, outside galadriel's ±15°**. **The s1 arena selection must NOT be upgraded to CITED. It should stay DECLARED, over a 10-member loadable enumeration.** | **CONFLICT** |
| **8** | **The same shadowing changes the geometry numbers materially.** For the *same* arena letter, sm_mod→sm1 emitter radii move up to **−30.2 %** (`b/p01`) and **−26.3 %** (`f/p06`, the conductor's 40.35→29.73). Nine of 33 comparable emitters move >10 %. Any parameter read off an sm_mod row is read off a dead file. | **MEASURED** |
| **9** | **T3: 16/16 (archive, map) pairs present in the CSV. No absent pair.** L-46 item 13's enumeration (sm_mod 6, sm1 8, sm2 2) is confirmed against the archives themselves. Per-pair p01/p05/p06 table § 4.2. | **VERIFIED** |
| **10** | **One decoder defect, named: 1 placement of 7 473 (0.013 %) was dropped.** `sm1/survivalworld_j.map` `tier12spawnpoint01` — string-table index 162 exists, placement #340 is missing from my emission (sequence jumps 339→341). **Tier 12 = waves 111–120, arena j only — outside band A and outside s1/s2. Zero calibration impact.** | **BLOCKED-DECODE (1 row)** |
| **11** | **Bonus, unasked: the DB overlay law is now ENGINE-CITED, not merely empirical.** `Engine.dll` `.text` RVA 0x66db9–0x67114 references the database roots in the literal sequence `database` → `gdx1` → `gdx2` → `gdx3` → `/mods/database.arz` → `survivalmode1` → `survivalmode2` → `survivalmode3` — the exact order L-33/L-46 derived from record behaviour. | **BINARY-CITED (corroborative)** |

---

## 2 — TASK 1 · SUMMON CITATION — **CLOSED-DB-CITED**

### 2.1 The chain, every link with its archive (overlay last-wins)

```
pinned CSV row : global_wave 153 | tier 16 | tier_wave 3 | spawn_point 3
                 proxy   records/proxies/tier16waves/proxy_w03_p03a.dbr
                 pool    records/proxies/poolsbasic/skeletonrevenant_t3.dbr   [sm_mod]

POOL   records/proxies/poolsbasic/skeletonrevenant_t3.dbr        owners=[sm_mod]      winner=sm_mod
         spawnMin = spawnMax = 6      championChance = 0.0
         name1 = .../skeleton_c01.dbr  weight1=100  minPlayerLevel1=25  lv4_champion+
         name2 = .../skeleton_c02.dbr  weight2=100  minPlayerLevel2=25  limit2=3  lv4_champion+
         name3 = .../skeleton_c03.dbr  weight3=100  minPlayerLevel3=25  lv4_champion+
         name4 = .../skeleton_d01.dbr  weight4= 75  minPlayerLevel4=45  limit4=2  lv5_elitechampion
                                                                        ^^^^^^^^  <-- THE SOURCE

MONSTER records/creatures/enemies/skeleton_d01.dbr     owners=[gdx2, sm_mod, sm2]   winner=sm2
         description            = tagEnemySkeletonC04  -> "Death Revenant"
         monsterClassification  = Champion
         charLevel              = charLevel*1+2
         characterRacialProfile = Race001
         skillName7             = records/skills/nonplayerskills/summoning/
                                  skeletonrevenant_skeletonarchergenerator.dbr
         skillLevel7            = charLevel/4+1
         (all three owning archives carry skillName7 identically — robust to the overlay law)

SKILL  records/skills/nonplayerskills/summoning/
       skeletonrevenant_skeletonarchergenerator.dbr    owners=[base, sm_mod]        winner=sm_mod
         Class                  = Skill_MonsterGenerator
         templateName           = database/templates/skill_monstergenerator.tpl
         spawnObjects           = records/creatures/enemies/skeleton_a02_summon.dbr
         petLimit               = 4          <-- sm_mod overlay.  BASE SAYS 6.
         petBurstSpawn          = 2
         petPeriod[0..21]       = 6.0 s      (5.0 s from index 22 up; skillMaxLevel 60)
         skillCooldownTime[0]   = 6.0 s
         spawnObjectsTimeToLive = 30.0 s
         distanceProfile        = Maximum

PET    records/creatures/enemies/skeleton_a02_summon.dbr  owners=[base, sm_mod]     winner=sm_mod
         description            = tagEnemySkeletonA02  -> "Skeletal Archer"
         monsterClassification  = Common
         charLevel              = charLevel*1     minLevel 8   maxLevel 250
         characterRacialProfile = Race001
         skillName3             = .../passive/armorbase01.dbr      (the § 6.2b armour link)
```

`tagEnemySkeletonA02 = "Skeletal Archer"` — `resources/Text_EN.arc :: tags_creatures.txt`.
Same file: `tagEnemySkeletonC01/02/03/04` = **Flame / Frost / Storm / Death Revenant** — which
identifies the pool's four slots as precisely "the four Revenants" the commission named.

### 2.2 The count, and what the engine says the count MEANS

Crate documents the two fields in `database/templates.arc :: skill_spawnpet.tpl`, verbatim:

| Variable | Crate's description |
|---|---|
| `petBurstSpawn` | *"number of pets spawned when skill is activated"* |
| `petLimit` | *"max number of pets alive at any given time"* |

`skill_monstergenerator.tpl` declares the same two Variables by name (with empty descriptions), so the
semantics carry. **`petLimit = 4` is therefore a declared ceiling of four concurrent Skeletal Archers per
Death Revenant** — the observed ×4 is the cap, not a coincidence of timing. Mechanism: 2 per cast, one
cast per 6 s, cap 4, each body living 30 s → the cap is reached at t ≈ 6 s and held.

**Upper bound worth carrying:** `limit4 = 2` permits up to **two** Death Revenants in one w153 p03 spawn,
so the ceiling on that spawn point is **8** archers, not 4. Four observed = one Revenant at cap (or two
below cap). The sim should model the cap per-summoner, not per-wave.

**Pet LEVEL is NAMED-ABSENT.** No `petLevel`-class Variable exists on `Skill_MonsterGenerator` or its
`Skill_Spawning` base; a corpus-wide template sweep for pet/spawn/summon *level* Variables returns only
`controllermonster.tpl :: petTargetLevelRange`, `itemset.tpl :: petBonusLevel`, and
`monsterspawner.tpl :: min/maxSpawnLevel` — none of which governs this path. Two **corroborations**, not
citations: (a) `lv5_elitechampion` gives min `(apl+2)`, max `(apl+1)+(apl/50)` = 102–103 at apl 100, and
`skeleton_d01`'s own `charLevel*1+2` lifts that to **104–105** — galadriel's **L105** reading sits exactly
at the top of the summoner's own band; (b) L-33's camera closure resolved a **Skeletal Archer at L109**
with eHP 41 237 EXACT at wave 160. Both readings say the archers arrive at wave level, not at
`skillLevel7 = charLevel/4+1 ≈ 27`. **The rule itself remains undeclared in the corpus.**

### 2.3 Per-candidate verdicts — the exhaustive negative

Method: from each of the **429** distinct monster records rostered anywhere on w151–158 (roster + champ
columns of the pinned CSV), BFS the **full `.dbr` reference graph** — *every field of every record*, not
just `spawnObjects` — to depth 3, flagging any path that lands on a `Class = Monster` record whose
`description` is `tagEnemySkeletonA02`. This catches `Skill_OnDeathSpawnActor` (317 slots on the band),
`Skill_SpawnPetMonster`, `Skill_TargetedSpawnPet` and nested pet-summons-pet, not only the obvious class.

**7 of 429 monsters reach a Skeletal Archer.** On **wave 153**, three pools:

| sp | pool | member | skill slot | skill | petLimit | burst |
|---:|---|---|---|---|---:|---:|
| **3** | `poolsbasic/skeletonrevenant_t3` (trash) | `skeleton_d01` **Death Revenant** | `skillName7` | `skeletonrevenant_skeletonarchergenerator` | **4** | 2 |
| 2, 4 | `poolsbounty/bounty_heroes02` (BOUNTY) | `kc_bounty07` | `skillName6` | `factionskills/necro_skeletongenerator` | 8 | 2 |
| 2, 4 | `poolsbounty/bounty_heroes02` (BOUNTY) | `kc_bounty08` | `skillName10` | `factionskills/necro_summonskeletonarchers02` | 6 | 3 |
| 2, 4 | `poolsbounty/bounty_heroes03` (BOUNTY) | `odv_bounty13` (also `tagEnemySkeletonC04`) | `skillName7` | `skeletonrevenant_skeletonarchergenerator` | **4** | 2 |

Elsewhere on the band: `devotion_heroes03 → ghost_h07` and `devotion_heroes04 → skeleton_h07`
(w152 p06 / w158 p02, `skillName12`, same skill, petLimit 4), and `skeletalgolem_t3 → skeletalgolem_b01`
(w157 p04, `skillName9`, `skeletalgolem_summonskeletons01`, petLimit 4, burst 4).

**Discrimination.** Only two w153 sources carry `petLimit = 4`, and both are Death Revenants. The named
candidate `skeletonrevenant_t3` is on **spawn point 3** — the conductor's stated p03. The bounty pair sit
on p02/p04 and carry petLimit 8 and 6. If galadriel's census localised the four bodies to p03, the
adjudication is unambiguous: **`skeleton_d01`, one Revenant, at its declared cap.**

**NAMED-ABSENT, explicitly** (the commission's priority list, in order):

| candidate | verdict |
|---|---|
| `skeleton_c01` **Flame Revenant** | **NAMED-ABSENT** — carries no summon/generator skill of any class |
| `skeleton_c02` **Frost Revenant** | **NAMED-ABSENT** — same |
| `skeleton_c03` **Storm Revenant** | **NAMED-ABSENT** — same |
| `skeleton_d01` **Death Revenant** | **PRESENT** — three generators (archer / warrior / knight) |
| `poolsbasicgdx1/livingplant_t3` p05 (w151, w153) | **NAMED-ABSENT** (2 members) |
| `poolsbasicgdx1/wendigo_t3` p01 (w153) | **NAMED-ABSENT** (6 members) |
| `poolsbasicgdx3/giant_t3` p03 (w153) | **NAMED-ABSENT** (6 members) |
| `poolshero/chthoniandreadguard_hero` p06 (w153) | **NAMED-ABSENT** (11 members) |
| `poolsherogdx3/giant_hero` p06 (w153) | **NAMED-ABSENT** (4 members) |
| `bounty_heroes01`, `poolsbountygdx1/*`, `poolsbountygdx3/*` (w153) | **NAMED-ABSENT** |
| all remaining w151–158 pools (95 of 101 pool×sp entries) | **NAMED-ABSENT** |

### 2.4 The adjudication-relevant structural point

`skeleton_a02_summon.dbr` is **rostered in no pool anywhere on the band** — it is a pet record, it only
ever enters the world through a generator. A body-count model driven by pool rosters cannot emit it *by
construction*. That is why the four were unexplained: they are a **second body source**, orthogonal to the
roster, gated by `petLimit` per summoner rather than by `spawnMin/Max` per pool.

The Death Revenant additionally carries `skillName8` → `skeletonrevenant_skeletongenerator01`
(`skeleton_a01_summon` = **Skeletal Warrior**, petLimit 4) and `skillName9` →
`skeletonrevenant_summonknight01` (`skeleton_b02_knight_summon` = **Skeletal Knight**, Champion,
petLimit 4, burst 1). **One Death Revenant is licensed to add up to 12 bodies** the roster never named.

---

## 3 — TASK 2 · MAP-FILE LOADING LAW — **CLOSED-SOURCE-CITED**

### 3.1 The contest, stated precisely

Exactly two archives ship `survivalworld_a…f.map`, and they are the same two archives that contest the
Crucible's Lua:

| resource root | Maps.arc | Scripts.arc |
|---|---|---|
| `mods/survivalmode/resources/` | `survivalworld_a…f` (6) | 24 files incl. `game/survival.lua`, `tier01…15waves.lua`, `game/events/survivalevent.lua` |
| `survivalmode1/resources/` | `survivalworld_a…g, j` (8) | 11 files incl. `game/survival.lua`, **`tier15…17waves.lua`** |
| `survivalmode2/resources/` | `survivalworld_h, i` (2) | *(Edition-I ships a 2 048-byte empty container)* |

`resources/Scripts.arc`, `gdx1/`, `gdx2/` carry **no** `survival*` path — no third contender exists for
either surface. **8 of sm1's 11 script paths are duplicates of sm_mod paths.** So the resource VFS must
resolve per-path collisions in this exact pair, for scripts and maps alike.

### 3.2 The citation — a behavioural discriminator inside the contested pair

`scripts/game/survival.lua` exists in **both** archives with different contents:

| line | `mods/survivalmode/resources/Scripts.arc :: game/survival.lua` | `survivalmode1/resources/Scripts.arc :: game/survival.lua` |
|---:|---|---|
| 29 | `Script.Load("scripts/game/survival/tier15Waves.lua")` | `Script.Load("scripts/game/survival/tier15Waves.lua")` |
| **30** | `Script.Load("scripts/game/questevents.lua")`  *(file ends)* | **`Script.Load("scripts/game/survival/tier16Waves.lua")`** |
| **31** | — | **`Script.Load("scripts/game/survival/tier17Waves.lua")`** |
| 32 | — | `Script.Load("scripts/game/questevents.lua")` |

And `scripts/game/survival/tier15waves.lua`, also in both, diverges at the run terminator:

```lua
-- mods/survivalmode/resources/Scripts.arc :: game/survival/tier15waves.lua
-- 91: -- Grant credit Token for defeating 15 waves
-- 92: function gd.survival.tier15Waves.endsurvivalModeEvent(objectId)
-- 97:   if not eventFailed then
-- 98:     LuaGlobalEvent("completeProgressToken")
-- 99:     gd.survival.eventControl.eventFinished()      <-- RUN TERMINATES AT WAVE 150

-- survivalmode1/resources/Scripts.arc :: game/survival/tier15waves.lua
-- 91: -- Grant credit Token for defeating 150 waves
-- 98:     LuaGlobalEvent("completeProgressToken")
-- 99:     (blank -- the eventFinished() call is DELETED)
```

and `survivalmode1/resources/Scripts.arc :: game/survival/eventcontrol.lua` adds the continuation:

```lua
-- 495:  elseif rewardTier == 15 then
-- 496:      gd.survival.tier16Waves.startSurvivalModeEvent()
-- 497:  elseif rewardTier == 16 then
-- 498:      gd.survival.tier17Waves.startSurvivalModeEvent()
-- 543:  function gd.survival.eventControl.startTier15Event()
-- 546:      Game.SetSurvivalWaveTier(151)
-- 554:      gd.survival.tier16Waves.startSurvivalModeEvent()
```

`mods/survivalmode/…/eventcontrol.lua` stops at `rewardTier == 14` (line 486) and declares no
`startTier15Event`, no `tier16Waves`, no `tier17Waves`.

**The discriminator.** If `mods/survivalmode`'s copies won the contested paths, the Crucible would call
`eventFinished()` at wave 150 and could not proceed. The shipping game demonstrably proceeds — galadriel's
own s2 footage is waves **150–160**, and the pinned wave-pool CSV enumerates to global wave **200**
(tiers 1–20). Therefore **`survivalmode1`'s copy of a contested path is the one the engine executes**, and
`mods/survivalmode`'s copy of that path is dead.

`Maps.arc` sits in the *same resource root pair*, resolved by the *same* VFS. Hence:

> **T2 ANSWER — CITED. For `survivalworld_f.map` (and a, b, c, d, e), the shipping Crucible loads the
> `survivalmode1/resources/Maps.arc` copy. The `mods/survivalmode/resources/Maps.arc` copy is shadowed.**

### 3.3 Independent cross-verification — three surfaces, one tier ceiling

The two archives were cut to the same content ceiling on every surface. This is not one observation:

| surface | `mods/survivalmode` | `survivalmode1` |
|---|---|---|
| Lua `survival.lua` loads | tier01…**tier15** | tier01…**tier17** |
| `Maps.arc` — `tierNNspawnpoint01` placements in every `survivalworld_*.map` (raw-byte census, 16/16 files) | **t01…t15**, n=15 | **t01…t17**, n=17 |
| `.arz` — which archive declares `records/scriptentities/tierNNspawnpoint01.dbr` | t01…t15 = `sm_mod` | **t16, t17 = `sm1`** (t18–20 = `sm3`) |

`tier16spawnpoint01.dbr` is declared **only** in `SurvivalMode1.arz` and placed **only** in sm1's and
sm2's map copies. Waves 151–160 (= tier 16) use spawn points **1–6** per the pinned CSV. An sm_mod map
copy has no tier-16 p01 placement at all: under that copy, wave 153's spawn point 1 has nowhere to emit.
**There is no reading in which the sm_mod maps are live.**

### 3.4 The Engine.dll lane — reported, and deliberately NOT used as the citation

`Engine.dll` (PE32, imagebase `0x10000000`) references the roots from `.text`:

* **database mount**, RVA `0x00066db9`–`0x00067114`, literal sequence:
  `/database/database.arz` → `/gdx1/…` → `/gdx2/…` → `/gdx3/…` → `/mods/database.arz` →
  `/survivalmode1/…` → `/survivalmode2/…` → `/survivalmode3/…`
  — **exactly the empirically-derived DB overlay order.** A genuine corroboration of L-33/L-46's law.
* **mod mount**, RVA `0x00069f47`: `mods/survivalmode/database/survivalmode.arz`.
* **resource mount**, RVA `0x0006bb9f`–`0x0006bf51`: `mods/` · `/resources` · `mods/` · `/database` ·
  `survivalmode` · `survivalmode3/resources` · `survivalmode2/resources` · `survivalmode1/resources` ·
  `.arz` · `survivalmode`.

I looked for a `const char*` **array** (whose order would be a citation) and found none — the strings are
referenced inline by individual instructions. **Literal order in x86 `.text` is compiler-determined and is
NOT evidence of call order** (note the resource block lists sm3, sm2, sm1 — descending — while the
database block ascends). I therefore report this lane as corroborative context and rest the verdict on
§ 3.2, which is behavioural. *Enumerated but not decisive: no disassembler on this host; a capstone pass
over RVA 0x6b900–0x6c100 would settle call order and is a cheap follow-up if the conductor wants it.*

### 3.5 What the T2 answer does to the s1 arena-selection grade — **CONFLICT**

L-46 item 16 ranked `sm_mod/survivalworld_f` best for s1 (11.8°) with `survivalworld_a` runner-up. **Both
are shadow copies.** The 16-pair geometry set collapses to **10 loadable arenas** — `sm1` a, b, c, d, e,
f, g, j + `sm2` h, i — which is exactly the ten `tagSurvivalArena_01…_10` names. The six `sm_mod` pairs
contribute **zero** distinct arenas; they are older revisions of six of the ten.

The shadowing is not cosmetic. Same arena letter, sm_mod → sm1:

| map | emitter | sm_mod r | sm1 r | Δ |
|---|---|---:|---:|---:|
| b | p01_tier01 | 40.39 | 28.20 | **−30.2 %** |
| b | p04 | 38.45 | 28.81 | **−25.1 %** |
| d | p04 | 44.50 | 31.86 | **−28.4 %** |
| c | p03 | 34.96 | 45.06 | **+28.9 %** |
| c | p06 | 27.29 | 34.80 | **+27.5 %** |
| f | p06 | **40.35** | **29.73** | **−26.3 %** (the conductor's figure) |
| f | p05 | 10.96 | 13.82 | +26.1 % |
| a | p05 | 11.60 | 7.16 | −38.3 % |

9 of 33 comparable emitters move more than 10 %. **Every geometry row keyed `sm_mod` in
`kc2_crucible_emitter_geometry.csv` describes a file the game does not load.**

Re-fit, restricted to loadable copies. *Method stated because it is not byte-identical to L-46's:* each
observed arrival is assigned to a **distinct** emitter (brute-force injective assignment over all
emitters present); score = mean |Δbearing|; p01 taken at the band's own tier.

| footage set | L-46 best (shadow) | best **LOADABLE** | verdict |
|---|---|---|---|
| s1, 4 arrivals | `sm_mod/f` 11.9° · `sm_mod/a` 11.6° | `sm1/f` **19.9°** | **OUTSIDE ±15°** |
| s2 w160, 4 arrivals | `sm_mod/f` 14.9° | `sm1/f` **18.2°** | OUTSIDE ±15° |
| s2 w151, 2 arrivals | — | `sm1/a` **10.2°** | inside ±15° (2 obs only) |

> **Ruling input: T2 does NOT upgrade the s1 arena selection to CITED. It flags a conflict.** The evidence
> that produced the 11.8° fit was drawn from a superseded file. `arena_id` should remain **DECLARED**, now
> over a **10-member loadable enumeration**, and § 10.9a should say so. Discriminating it still needs a
> save-file level id or a footage landmark (L-46 O-6, unchanged).

**Freshness bound, named.** Edition-I predates FoA. The `.arz` declares `tier18/19/20spawnpoint01.dbr` in
`sm3`, and spawn points are only ever placed in arena maps — so **FoA must re-ship the arena maps again**,
and by the same law `survivalmode3`'s copies would supersede `sm1`'s. Those files are
**NAMED-ABSENT-CONFIRMED in every pin I hold** (Edition-II ships no `.arc` at all; Edition-I has no
`survivalmode3` directory). The geometry in § 4 is therefore the **survivalmode1-era** geometry: correct
for a pre-FoA 170-wave Crucible, and of unknown currency for the 200-wave build the pinned wave-pool CSV
describes. This is L-46 O-4 again, now load-bearing rather than hygienic.

### 3.6 Lanes exhausted for T2

| lane | result |
|---|---|
| Mod descriptor / manifest file | **NAMED-ABSENT-CONFIRMED.** Full-tree enumeration of `mods/`, `survivalmode1/`, `survivalmode2/`: 22 files, all `.arz`/`.arc`. No `.txt`, `.cfg`, `.ini`, no descriptor of any kind. |
| Lua naming a map path or level root | **NAMED-ABSENT-CONFIRMED.** 304 extracted Lua files: zero occurrences of `survivalworld`, `.map`, `levelName`, `worldName`, `LoadLevel`, `SetLevel`. Coordinates are read at runtime (`survivalevent.lua:398 entity[id]:GetCoords()`); the Lua consumes level geometry and never names it. |
| Lua declaring loading order | **NAMED-ABSENT** as a *declaration* — but the **consequence** is cited (§ 3.2), which is stronger. |
| Explicit path-resolution declaration in the DB / templates | **NAMED-ABSENT.** No VFS/mount fields in `gameengine.dbr` (366 fields, re-checked) or `templates.arc`. |
| Engine binary | **PARTIAL** — root strings located and code windows identified (§ 3.4); no pointer array; disassembly not available on this host. |
| **Behavioural discriminator in the contested archive pair** | **CITED — this is the answer.** |

---

## 4 — TASK 3 · ENUMERATION TABLE — **VERIFIED, 16/16**

### 4.1 Coverage

`/Users/admin/Games/reincarnated-engine/data/kc2/kc2_crucible_emitter_geometry.csv` — **333 lines = 1
header + 332 data rows** (L-46 quotes the row count, the commission the line count; both are right).

Expected pairs from the archives themselves: `sm_mod` a–f (6) + `sm1` a–g, j (8) + `sm2` h, i (2) = **16**.
Present in CSV: **16**. **ABSENT: NONE. EXTRA: NONE.** L-46 item 13 confirmed.

### 4.2 Per-pair summary — p01 (tier01 row) · p05 · p06

Radius in metres from the `PatrolPoint_Attack` centroid; bearing as clock position.
**`LOAD` = the copy the shipping game resolves (§ 3.2); `shadow` = superseded.**

| | archive | map | p01 (tier01) | p05 (ambush) | p06 | p01 tiers | patrol r̄ |
|---|---|---|---|---|---|---:|---:|
| shadow | `sm_mod` | a | 36.06 m @ 9.5h | 11.60 m @ 7.8h | 27.75 m @ 1.6h | 15 | 18.20 |
| shadow | `sm_mod` | b | 40.39 m @ 9.1h | 9.38 m @ 9.4h | 39.89 m @ 1.4h | 15 | 12.83 |
| shadow | `sm_mod` | c | 32.69 m @ 9.3h | — absent — | 27.29 m @ 2.9h | 15 | 18.70 |
| shadow | `sm_mod` | d | 41.39 m @ 5.9h | — absent — | 38.48 m @ 2.8h | 15 | 18.52 |
| shadow | `sm_mod` | e | 39.07 m @ 9.8h | — absent — | 31.17 m @ 1.4h | 15 | 15.48 |
| shadow | `sm_mod` | f | 39.00 m @ 9.3h | 10.96 m @ 7.5h | **40.35 m @ 1.4h** | 15 | 20.89 |
| **LOAD** | `sm1` | **a** | 35.96 m @ 9.5h | 7.16 m @ 9.6h | 31.95 m @ 2.6h | 17 | 18.20 |
| **LOAD** | `sm1` | **b** | 28.20 m @ 9.6h | 8.98 m @ 11.8h | 40.14 m @ 2.6h | 17 | 12.83 |
| **LOAD** | `sm1` | **c** | 32.61 m @ 9.3h | — absent — | 34.80 m @ 4.1h | 17 | 18.70 |
| **LOAD** | `sm1` | **d** | 41.23 m @ 5.9h | — absent — | 40.12 m @ 2.8h | 17 | 18.52 |
| **LOAD** | `sm1` | **e** | 39.07 m @ 9.8h | — absent — | 28.22 m @ 0.8h | 17 | 15.48 |
| **LOAD** | `sm1` | **f** | 43.80 m @ 9.4h | 13.82 m @ 8.3h | **29.73 m @ 1.9h** | 17 | 20.89 |
| **LOAD** | `sm1` | **g** | 39.16 m @ 10.8h | 2.56 m @ 2.2h | 32.25 m @ 0.2h | 17 | 14.31 |
| **LOAD** | `sm1` | **j** | 42.79 m @ 11.0h | 13.16 m @ 3.0h | 46.97 m @ 2.1h | **16** ⚑ | 20.32 |
| **LOAD** | `sm2` | **h** | 30.34 m @ 0.2h | 17.15 m @ 0.4h | 38.17 m @ 2.4h | 17 | 16.57 |
| **LOAD** | `sm2` | **i** | 33.23 m @ 10.5h | 1.70 m @ 2.9h | 36.12 m @ 2.2h | 17 | 16.03 |

**p05 is genuinely absent from arenas c, d and e** — in both archives, consistently. Six absences across
16 pairs, leaving the n=10 that L-46 § 4.3 reports. Those three arenas have **no ambush point**; a sim that
assumes six emitters everywhere is wrong on 3 of 10 loadable arenas.

**⚑ The one defect.** `sm1/survivalworld_j.map` should carry 17 p01 tier placements; the CSV has 16.
Missing: **tier12**. The string `records/scriptentities/tier12spawnpoint01.dbr` is present exactly once in
the map's string table (offset 1 848 329), and my placement emission skips both placement #340 and
string-table index 162 (the sequence runs 339 → 341, indices 161 → 163) — so this is a **variable-length
record my decoder mis-sized, not a content gap**. **1 of 7 473 placements = 0.013 %.** Tier 12 = waves
111–120 in arena j only: outside band A (waves 1–93), outside s1, outside s2. **Zero calibration impact.**
Named rather than silently carried.

### 4.3 Restatement for spec § 10.9a B

> The Crucible arena enumeration is **10 arenas** (`tagSurvivalArena_01…_10`), realised as **16
> (archive, map) file pairs** across three resource roots. Six of the sixteen — every
> `mods/survivalmode` pair — are **superseded revisions** of `survivalmode1` pairs of the same path and
> are not loaded by the shipping game (§ 3.2). The loadable set is `survivalmode1` × {a, b, c, d, e, f,
> g, j} and `survivalmode2` × {h, i}. Arenas **c, d, e carry no p05 ambush emitter**. Geometry is
> **survivalmode1-era (pre-FoA)**; FoA's 200-wave build almost certainly re-ships these maps and those
> files are absent from every pin.

---

## 5 — WHAT I DID NOT DO

- **No fitting.** § 3.5's re-fit is a re-scoring of galadriel's already-recorded bearings against already-
  measured geometry, with the method stated inline. No parameter was solved against a clear time.
- **No re-grading of the mechanism itself.** I report that the summon exists, what it declares, and what
  it cannot be. Whether the sim models summoned bodies is a conductor ruling.
- **No claim that L-46's 11.8° was arithmetically wrong.** My injective re-fit is a *different* method and
  does not reproduce L-46's numbers exactly. The conflict I raise is about **which files are live**, which
  is method-independent.
- **No disassembly.** § 3.4's binary lane is reported as corroborative and explicitly not rested on.
- **No spec or build edits**, no CSV edits. The § 4.2 defect is named for the conductor, not patched.

---

## 6 — OPEN ITEMS HANDED BACK

| # | Item | Owner |
|---|---|---|
| **P-1** | **Summoned bodies are a second, un-rostered body source.** One Death Revenant licenses up to 12 (4 archers + 4 warriors + 4 knights); `limit4 = 2` allows two Revenants on w153 p03. The sim's pool-driven body count cannot produce them. Model, or declare out-of-model. | conductor → gamora |
| **P-2** | **`Skill_MonsterGenerator` pet LEVEL is NAMED-ABSENT.** Two independent corroborations put the archers at summoner level (§ 2.2), but the rule is undeclared. If the sim gives summoned bodies eHP, the level input is DECLARED, not cited. | conductor → gamora |
| **P-3** | **Every `sm_mod` row in `kc2_crucible_emitter_geometry.csv` describes a shadowed file.** Recommend a `loaded` boolean column, or restricting the emission to the 10 loadable pairs, before anything downstream reads a radius from it. | conductor → gamora / elrond |
| **P-4** | **§ 10.9a B and L-46 item 16 both need the § 4.3 restatement**, and `arena_id` must stay DECLARED. | conductor (SPEC-AUTHOR) |
| **P-5** | **L-46 O-4 is now load-bearing, not hygienic.** Without `survivalmode3/resources/Maps.arc` the current-build arena geometry is unobtainable, and by § 3.2's law it supersedes what I measured. Escalate the pull. | conductor → matt_to_do |
| **P-6** | **Decoder defect:** 1 placement of 7 473 dropped (`sm1/survivalworld_j` tier12, § 4.2 ⚑). Out of band; fix on next map-decode pass. | legolas |
| **P-7** | **Optional cheap follow-up:** a capstone disassembly of `Engine.dll` RVA 0x6b900–0x6c100 would convert § 3.4's resource-mount corroboration into an independent second citation for T2. Not needed for the verdict. | conductor (discretionary) |

---

**Filed:** legolas (UNKNOWN-RESEARCHER), 2026-08-08, KC2-SIM Phase D. Every row DB-, TPL-, SOURCE-,
LEVEL- or BINARY-CITED, or explicitly graded NAMED-ABSENT / CONFLICT / BLOCKED-DECODE. Zero external
fetches. Zero fitted parameters. Note UNCOMMITTED per commission.
