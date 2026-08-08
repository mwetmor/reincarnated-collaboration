# KC2-SIM — w152 / w157 generator-join (mechanism adjudication input)

**Date:** 2026-08-08
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (RUN-CONDUCTOR), KC2-SIM run
**Mode:** A (analytical / primary-source probe)
**Status:** COMPLETE — Part A CLOSED · Part B ANSWERED (forked, both branches given) ·
Part C **NAMED-BLOCKED-ON-T15**
**External fetches:** ZERO. Corpus-resident only, Edition-II pin only.
**Truth-boundary tags:** MEASURED (read from records/emissions) · INFERRED (ratio or structural argument) · DECLARED (carried from prior notes)

## 0. Commission

Two Crucible waves are falsified against the KC2 composition model:

- **w152** — measured 17 plain-tier hostile bodies vs model support 7 (**+10**)
- **w157** — measured 15 vs 14 (**+1**)

Three hypotheses for w152: (i) non-archer GENERATOR/summon records among the wave's pools spawning
adds not in placement tables — LEAD; (ii) p05 drip-emitter replenishment arriving inside the cohort
scoring window; (iii) census multiplicity artifact — DEMOTED. For w157 the standing candidate is
`skeletalgolem_b01` p04 generator petLimit 4.

Three parts in order of decidability: **(A) FIELD CHECK** (derivation-free, must close) ·
**(B) RATIO STRUCTURE** (derivation-light) · **(C) EXACT HP JOIN** (may be BLOCKED on T15).

## 1. Substrate located — MEASURED

### 1.1 Corpus pin (Edition-II only; corpus-provenance rule honoured)

`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — eight-archive `.arz` overlay,
last-wins whole-record replacement, order `base → gdx1 → gdx2 → gdx3 → sm_mod → sm1 → sm2 → sm3`
(the order is BINARY-CITED in L-47 § 3.4 and behaviour-cited in L-47 § 3.2). Resolver reused
verbatim: `agentic_orchestration/legolas/scratch/2026-08-08-kc2-citation/t0_lib.py`.
Localisation from `resources/Text_EN.arc` ×4 → **20,245 tags loaded**.

**ZERO Edition-I extraction in this note.** The `~/Games/vendor/grim-dawn/` pin was not opened.
Every record value below comes from the Edition-II overlay. No external fetches.

### 1.2 Composition source of record

`/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv`
(the committed v2 of the P-E6 emission; `roster_records` / `champ_records` columns carry the
resolved `.dbr` paths). w152 + w157 = **39 pool rows, 239 distinct monster records**.

### 1.3 Instruments (this probe, reproducible)

`agentic_orchestration/legolas/scratch/2026-08-08-kc2-w152w157/`
`a1_genfields.py` (broad sweep, superseded) · **`a3_strict.py` (the sweep of record)** ·
`a3_hits.json` · `a3_rows.csv` · `a3_out.txt` · `a3_gaps.json`.

**Method, stated because it corrects a1.** From each rostered monster the walk follows **only
`skillName{i}`**; from a skill record only skill-composition edges; a spawned body that is itself
`Class = Monster` re-enters the walk as a monster (catching pet-summons-pet). Depth ≤ 4.
The broad a1 sweep (580 hits) was **rejected**: it followed `factions → faction_*.dbr →
nemesisSpawn → nemesis_aetherialvanguard_01.dbr → skillName9 → aetherialvanguard_summonshard`,
which attached the Aetherial Vanguard's crystal summon to **every Aetherial-faction monster in
the band**. That is a faction-table edge, not a skill of the rostered creature. Strict sweep:
**286 producer hits, 105 distinct (wave, sp, pool, summoner, skill, body) rows, 3 gaps.**

## 2. Part A — field check hit table — **CLOSES. MEASURED.**

### 2.0 Pool inventory of the two waves (from the pinned CSV) — MEASURED

**w152** (tier16 w02) — six spawn points, **one plain-tier (trash) point**:

| sp | kind | pool alternatives (engine picks ONE) | spawn min–max | champ |
|---:|---|---|---|---|
| 1 | HERO | `poolsherogdx1/swampcrab_hero` · `poolsherogdx1/ghostcrab_hero` · `poolsherogdx3/springscrab_hero` | 0–0 | 100 %, 1–1 |
| 2 | HERO | `poolsherogdx1/basilisk_hero` · `poolsherogdx3/thornedhorrorfrost_hero` | 0–0 | 100 %, 1–1 |
| **3** | **trash** | **`poolsbasicgdx1/basilisk_t3` · `poolsbasicgdx3/thornedhorrorfrost_t3`** | **5–6** | 0 % |
| 4 | BOSS | `swampcrab_carraxus` · `aetherialfleshshaper_hinissius` · `aetherialfleshshaper_haraxis` · `fleshweaverkrieg` | 1–1 | 0 % |
| 5\* | HERO | `poolsherogdx1/aetherialcorruption_hero` (ProxyAmbush) | 0–0 | 100 %, 1–1 |
| 6 | DEVOTION | `poolsdevotion/devotion_heroes01…06` | 0–0 | 100 %, 1–1 |

**w157** (tier16 w07) — six spawn points, **two plain-tier (trash) points**:

| sp | kind | pool alternatives | spawn min–max | champ |
|---:|---|---|---|---|
| 1 | BOSS | `wendigocannibal_packla` · `ghoul_nercropolis` · `aetherialbloater_malmouthdocks` | 1–1 | 0 % |
| 2 | DEVOTION | `poolsdevotiongdx1/devotion_heroes01…03` · `poolsdevotiongdx3/devotion_heroes01…03` | 0–0 | 100 %, 1–1 |
| **3** | **trash** | **`chthonianrylok_t3` (4–5) · `chthonianservitor_t3` (4–5) · `chthonianleech_t3` (6–6) · `gargoyle_t3` (3–4)** | 3–6 | 0 % |
| **4** | **trash** | **`swampgolem_t3` (3–5) · `aetherialbloater_t3` (5–6) · `skeletalgolem_t3` (6–6) · `yetidire_t3` (5–6)** | 3–6 | 0 % |
| 5\* | HERO | `aetherialimp_hero` · `aetherialcorruption_hero` · `wight_hero` (ProxyAmbush) | 0–0 | 100 %, 1–1 |
| 6 | HERO | `aetherialcolossus_hero` | 0–0 | 100 %, 1–1 |

`fleshweaverkrieg` (w152 p04) is the band's only `ignoreGameBalance = True` pool. All other
w152/w157 pools carry `igb = False`. No `legendary_override` on either wave — **the Gladiator
composition equals the Aspirant composition on both waves** (P-E6 § 2.4 list: 152 and 157 are
not among the 24 override waves).

### 2.1 HIT TABLE — every body-producing field on w152 — MEASURED

Only rows whose `spawnObjects` resolves to a `Class = Monster` record are shown. **PLAIN =
`monsterClassification = Common`** (a plain-tier body in galadriel's census sense); **Champion**
would carry a star and is out of scope.

| sp | pool (kind) | summoner record | summoner cls | skill record | skill Class | petLimit | burst | TTL s | body record | body tier | body name |
|---:|---|---|---|---|---|---:|---:|---:|---|---|---|
| 1 | `poolsherogdx1/swampcrab_hero` (HERO) | `swampcrab_h01…h05` (5 of 5) | Hero | `swampcrab_crabgenerator` | `Skill_MonsterGenerator` | **8** | **4** | 30 | `swampcrab_a00_summon` | **PLAIN** | Ugdenbog Crabling |
| 1 | `poolsherogdx1/swampcrab_hero` | `swampcrab_h05` | Hero | `bramble_summonbrambletrap` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `trap_brambletrap_a01` | **PLAIN**† | Bramble Trap |
| 1 | `poolsherogdx3/springscrab_hero` (HERO) | `springscrab_h01…h04` (4 of 4) | Hero | `springscrab_crabgenerator` | `Skill_MonsterGenerator` | **8** | **4** | 30 | `springscrab_a00_summon` | **PLAIN** | Calcified Crabling |
| 1 | `poolsherogdx3/springscrab_hero` | `springscrab_h01` | Hero | `thundering_summonlightningspike` | `Skill_TargetedSpawnPet` | 6 | 1 | 24 | `trap_lightningspike_hero_a01` | **PLAIN**† | Storm Conduit |
| 1 | `poolsherogdx3/springscrab_hero` | `springscrab_h03` | Hero | `arctic_summonicespike` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `trap_icespike_hero_a01` | **PLAIN**† | Ice Spike |
| 1 | `poolsherogdx1/ghostcrab_hero` (HERO) | `ghostcrab_h01…h05` | Hero | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| 2 | `poolsherogdx1/basilisk_hero` (HERO) | `basilisk_h05` only | Hero | `arctic_summonicespike` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `trap_icespike_hero_a01` | **PLAIN**† | Ice Spike |
| 2 | `poolsherogdx3/thornedhorrorfrost_hero` | `thornedhorrorfrost_h02` | Hero | `thundering_summonlightningspike` | `Skill_TargetedSpawnPet` | 6 | 1 | 24 | `trap_lightningspike_hero_a01` | **PLAIN**† | Storm Conduit |
| 2 | `poolsherogdx3/thornedhorrorfrost_hero` | `thornedhorrorfrost_h04` | Hero | `bramble_summonbrambletrap` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `trap_brambletrap_a01` | **PLAIN**† | Bramble Trap |
| **3** | **`basilisk_t3` (trash)** | `basilisk_a01`, `basilisk_b01`, `basilisk_c01` | Common/Champion | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| **3** | **`thornedhorrorfrost_t3` (trash)** | `thornedhorrorfrost_a01/b01/c01` | Champion | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| 4 | `swampcrab_carraxus` (BOSS) | `swampcrab_ugdenbog_01` | Quest | `carraxus_summonswampcrabc` | `Skill_SpawnPet` | 4 | 1→2 | 25 | `swampcrab_b01_summon` | **PLAIN** | Ugdenbog Spikeshell |
| 4 | `swampcrab_carraxus` | `swampcrab_ugdenbog_01` | Quest | `carraxus_summonswampcrabc` | `Skill_SpawnPet` | 4 | 1→2 | 25 | `swampcrab_c01_summon` | Champion | Ugdenbog Stoneshell |
| 4 | `swampcrab_carraxus` | `swampcrab_ugdenbog_01` | Quest | `swampcrab_crabgenerator` | `Skill_MonsterGenerator` | **8** | **4** | 30 | `swampcrab_a00_summon` | **PLAIN** | Ugdenbog Crabling |
| 4 | `fleshweaverkrieg` (BOSS) | `aetherial_fleshweaverkrieg`, `…kriegb` | Quest | `krieg_summonaethertrap` | `Skill_SpawnPet` | 3 | — | 30 | `krieg_aethertrap` | **PLAIN**† | Aether Trap |
| 4 | `fleshweaverkrieg` | `aetherial_fleshweaverkrieg`, `…kriegb` | Quest | `krieg_summoncorruptionc_secondary` | `Skill_TargetedSpawnPet` | 4 | 1 | 30 | `aetherialcorruption_c01_summon` | Champion | Fleshwarped Aberration |
| 4 | `aetherialfleshshaper_haraxis` (BOSS) | `aetherialfleshshaper_haraxis` | Quest | `fleshshaperharaxis_aethercorruptiongenerator` | `Skill_MonsterGenerator` | 8 | 2 | 40 | `aetherialcorruption_c01_summon` | Champion | Fleshwarped Aberration |
| 4 | `aetherialfleshshaper_haraxis` | `aetherialfleshshaper_haraxis` | Quest | `fleshshaperharaxis_summonspirits` | `Skill_TargetedSpawnPet` | 6→12 | 3→6 | 30 | `fleshshaper_spirit_01` | Champion | Aetherial Wraith |
| 4 | `aetherialfleshshaper_hinissius` (BOSS) | `aetherialfleshshaper_hinissius` | Quest | `fleshshaperhinissius_stormcorruptiongenerator` | `Skill_MonsterGenerator` | 8 | 2 | 40 | `aetherialcorruption_b02_summon` | Champion | Fleshwarped Stormwalker |
| 4 | `aetherialfleshshaper_hinissius` | `aetherialfleshshaper_hinissius` | Quest | `fleshshaperhinissius_summonstormcolossus` | `Skill_SpawnPet` | 3 | 1 | 30 | `aetherialcolossus_c02_summon` | Champion | Aetherial Stormbearer |
| 5\* | `aetherialcorruption_hero` (HERO) | `aetherialcorruption_h05` only | Hero | `arctic_summonicespike` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `trap_icespike_hero_a01` | **PLAIN**† | Ice Spike |
| 6 | `devotion_heroes01` | `chthoniandevourer_h06` | Hero | `chthonianabomination_summondevourers_a01` | `Skill_SpawnPet` | **8** | **4** | 30 | `chthoniandevourer_a01_summon` | **PLAIN** | Chthonian Hungerer |
| 6 | `devotion_heroes02` | `chthonianminion_h01…h07` (7 of 13) | Hero | `chthonicminion_summonvoidfienda01` | `Skill_SpawnPet` | 4 | 1 | — | `chthonianfiend_a01_summon` | **PLAIN** | Voidfiend |
| 6 | `devotion_heroes02` | `chthonianminion_h01…h07` | Hero | `chthonicminion_summonvoidfiendc01` | `Skill_SpawnPet` | 1 | 1 | — | `chthonianfiend_c01_summon` | Champion | Voidfiend Hellion |
| 6 | `devotion_heroes02` | `chthonianmonstrosity_h01` | Hero | `chthonianabomination_summontentacles` | `Skill_SpawnPet` | **12** | **12** | 5 | `chthonianabomination_tentacles_a01` | **PLAIN**† | Writhing Tentacle |
| 6 | `devotion_heroes03` | `ghost_h03` | Hero | `skeletonrevenant_skeletongenerator01` | `Skill_MonsterGenerator` | 4 | 2 | 30 | `skeleton_a01_summon` | **PLAIN** | Skeletal Warrior |
| 6 | `devotion_heroes03` | `ghost_h04` | Hero | `skeletalgolem_summonghosts01` | `Skill_SpawnPetMonster` | 4 | 4 | — | `ghost_a01_summon` | **PLAIN** | Apparition |
| 6 | `devotion_heroes03` | `ghost_h07` | Hero | `skeletonrevenant_skeletonarchergenerator` | `Skill_MonsterGenerator` | 4 | 2 | 30 | `skeleton_a02_summon` | **PLAIN** | Skeletal Archer |
| 6 | `devotion_heroes03` | `ghost_h07` | Hero | `skeletonrevenant_skeletongenerator01` | `Skill_MonsterGenerator` | 4 | 2 | 30 | `skeleton_a01_summon` | **PLAIN** | Skeletal Warrior |
| 6 | `devotion_heroes04` | `skeletalgolem_h02…h05` | Hero | `skeletalgolem_summonghosts01` | `Skill_SpawnPetMonster` | 4 | 4 | — | `ghost_a01_summon` | **PLAIN** | Apparition |
| 6 | `devotion_heroes04` | `skeleton_h02` | Hero | `balrazar_summonhellhound` | `Skill_SpawnPet` | 4 | 1 | 20 | `hellhound_undeadfaction_a01` | **PLAIN** | Hellhound |
| 6 | `devotion_heroes04` | `skeleton_h07` | Hero | `skeletonrevenant_skeletonarchergenerator` | `Skill_MonsterGenerator` | 4 | 2 | 30 | `skeleton_a02_summon` | **PLAIN** | Skeletal Archer |
| 6 | `devotion_heroes04` | `skeleton_h07` | Hero | `ilgorr_summonrevenant01` | `Skill_SpawnPetMonster` | 8 | 4 | 60 | `skeleton_c01_summon` | Champion | Flame Revenant |
| 6 | `devotion_heroes04` | `skeleton_h09` | Hero | `skeletonrevenant_skeletongenerator01` | `Skill_MonsterGenerator` | 4 | 2 | 30 | `skeleton_a01_summon` | **PLAIN** | Skeletal Warrior |
| 6 | `devotion_heroes04` | `skeleton_h09` | Hero | `skeletonrevenant_summonknight01` | `Skill_SpawnPetMonster` | 4 | 1 | — | `skeleton_b02_knight_summon` | Champion | Skeletal Knight |
| 6 | `devotion_heroes05` | `spider_cave_h02`, `_h03` | Hero | `spidercave_spidergenerator` | `Skill_MonsterGenerator` | 4 | 4 | 30 | `spidergiantb_cave_a01_summon` | **PLAIN** | Terrorweave Spiderling |
| 6 | `devotion_heroes06` | `prawncave_h03` | Hero | `prawncave_summonprawns` | `Skill_SpawnPetMonster` | 4 | 3 | — | `prawncave_a01_summon` | **PLAIN** | Pale Cavern Crawler |
| 6 | `devotion_heroes06` | `skeletalgolem_h01` | Hero | `skeletalgolem_summonghosts01` | `Skill_SpawnPetMonster` | 4 | 4 | — | `ghost_a01_summon` | **PLAIN** | Apparition |
| 6 | `devotion_heroes06` | `skeleton_h10` | Hero | `skeletonrevenant_skeletongenerator01` | `Skill_MonsterGenerator` | 4 | 2 | 30 | `skeleton_a01_summon` | **PLAIN** | Skeletal Warrior |
| 6 | `devotion_heroes06` | `skeleton_h10` | Hero | `rolderathis_summon_icerevenant` | `Skill_SpawnPetMonster` | 2 | 1 | 60 | `skeleton_c02_summon` | Champion | Frost Revenant |

† **Trap/ground-object class flag.** `trap_brambletrap_a01`, `trap_icespike_hero_a01`,
`trap_lightningspike_hero_a01`, `krieg_aethertrap`, `chthonianabomination_tentacles_a01` are
`Class = Monster` with `monsterClassification = Common`, i.e. they are plain-tier bodies **by the
record**. Whether they present a health bar the census can fingerprint is a **rendering question
the database cannot answer** — flagged in § 6, not asserted either way.

### 2.2 HIT TABLE — every body-producing field on w157 — MEASURED

| sp | pool (kind) | summoner record | summoner cls | skill record | skill Class | petLimit | burst | TTL s | body record | body tier | body name |
|---:|---|---|---|---|---|---:|---:|---:|---|---|---|
| 1 | `aetherialbloater_malmouthdocks` (BOSS) | `aetherialbloater_malmouthdocks_01` | Quest | `aetherialbloater_wormgenerator` | `Skill_MonsterGenerator` | 4 | 2 | 30 | `aetherialworm_b01…b04_summon` | Champion ×4 | Aetherial Rot/Blaze/Ice/Storm-\* |
| 1 | `wendigocannibal_packla` (BOSS) | `wendigocannibal_packla` | Quest | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| 1 | `ghoul_nercropolis` (BOSS) | `ghoul_necropolis_01` | Quest | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| 2 | `gdx1/devotion_heroes01` | `swampcrab_h01`, `_h02` | Hero | `swampcrab_crabgenerator` | `Skill_MonsterGenerator` | **8** | **4** | 30 | `swampcrab_a00_summon` | **PLAIN** | Ugdenbog Crabling |
| 2 | `gdx1/devotion_heroes02` | `swampcrab_h03`, `_h04` | Hero | `swampcrab_crabgenerator` | `Skill_MonsterGenerator` | **8** | **4** | 30 | `swampcrab_a00_summon` | **PLAIN** | Ugdenbog Crabling |
| 2 | `gdx1/devotion_heroes02` | `swampgolem_h01…h04` | Hero | `swampgolem_spawnplants` | `Skill_SpawnPet` | 3 | 1 | 20 | `livingplant_a01_summon` | **PLAIN** | Carnivorous Plant |
| 2 | `gdx1/devotion_heroes02` | `aetherialfleshshaper_h01…h04` | Hero | `aetherialsentry_corruptiongeneratorb` · `corruptionburning_generator` · `aetherialfleshshaper_summonbloater` | Generator / SpawnPet | 3–8 | 1–2 | 30–40 | `aetherialcorruption_b01/b02/b03_summon`, `aetherialbloater_b01_summon` | Champion ×4 | — |
| 2 | `gdx3/devotion_heroes01` | `chthonianherald_h04`, `dranghoul_h02`, `rhino_h01`, `rhino_h04` | Hero | bramble / icespike / lightningspike | `Skill_TargetedSpawnPet` | 6 | 1 | 12–24 | trap records | **PLAIN**† | trap bodies |
| 2 | `gdx3/devotion_heroes03` | `dranghoul_h02`, `rhino_h01`, `rhino_h04` | Hero | bramble / icespike | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | trap records | **PLAIN**† | trap bodies |
| 2 | `gdx1/devotion_heroes03`, `gdx3/devotion_heroes02` | all members | Hero | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| **3** | **`gargoyle_t3` (trash)** | `gargoyle_c01` | Champion | `gargoyle_summoneldritchground` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `eldritchground` | **PLAIN**† | Entropic Void |
| **3** | **`chthonianrylok_t3` · `chthonianservitor_t3` · `chthonianleech_t3`** | all 13 members | Common/Champion | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| **4** | **`skeletalgolem_t3` (trash)** | **`skeletalgolem_b01`** | **Champion** | **`skeletalgolem_summonskeletons01`** | **`Skill_SpawnPetMonster`** | **4** | **4** | **none** | **`skeleton_a02_summon`** | **PLAIN** | **Skeletal Archer** |
| **4** | **`skeletalgolem_t3`** | `skeletalgolem_c01` | Champion | `skeletalgolem_summonghosts01` | `Skill_SpawnPetMonster` | 4 | 4 | none | `ghost_a01_summon` | **PLAIN** | Apparition |
| **4** | **`swampgolem_t3` (trash)** | `swampgolem_c01` | Champion | `swampgolem_spawnplants` | `Skill_SpawnPet` | 3 | 1 | 20 | `livingplant_a01_summon` | **PLAIN** | Carnivorous Plant |
| **4** | **`aetherialbloater_t3` · `yetidire_t3`** | all 9 members | Common/Champion | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| 5\* | `aetherialcorruption_hero` | `aetherialcorruption_h05` | Hero | `arctic_summonicespike` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `trap_icespike_hero_a01` | **PLAIN**† | Ice Spike |
| 5\* | `aetherialimp_hero` | `aetherialimp_h05` | Hero | `arctic_summonicespike` | `Skill_TargetedSpawnPet` | 6 | 1 | 12 | `trap_icespike_hero_a01` | **PLAIN**† | Ice Spike |
| 5\* | `wight_hero` | all 4 members | Hero | — | — | — | — | — | — | **NAMED-ABSENT** | — |
| 6 | `aetherialcolossus_hero` | all 5 members | Hero | — | — | — | — | — | — | **NAMED-ABSENT** | — |

### 2.3 The two commissioned questions, answered directly

**Q(A1) — does w152 carry non-archer generator records capable of producing ~7 plain adds?**
**YES, MEASURED, and with room to spare — but NOT from its plain-tier pool.**

- The single **largest** plain-body producer on w152 is `swampcrab_crabgenerator`
  (`Skill_MonsterGenerator`, **petLimit 8, petBurstSpawn 4, TTL 30 s**) → `swampcrab_a00_summon`
  = **Ugdenbog Crabling, `monsterClassification = Common`**. It sits on **all five members of
  `poolsherogdx1/swampcrab_hero` (p01)** *and* on the p04 boss `swampcrab_ugdenbog_01`
  (Carraxus). A **single** swampcrab hero is licensed for **8 concurrent plain bodies** —
  more than the +10 needs from two summoners.
- The parallel `springscrab_crabgenerator` (petLimit 8, burst 4 → `springscrab_a00_summon`,
  Calcified Crabling, Common) sits on all four members of the p01 alternative
  `poolsherogdx3/springscrab_hero`.
- p04 Carraxus additionally carries `carraxus_summonswampcrabc` (`Skill_SpawnPet`, petLimit 4)
  whose slot-1 body `swampcrab_b01_summon` (Ugdenbog Spikeshell) is **also Common**.
- **None of these is an archer generator.** The archer chain
  (`skeletonrevenant_skeletonarchergenerator`, petLimit 4) appears on w152 **only** via
  p06 `devotion_heroes03 → ghost_h07` and `devotion_heroes04 → skeleton_h07` — one devotion pool
  is picked per wave and only two of the six carry it.
- **The w152 plain-tier pool itself is NAMED-ABSENT.** All six members of `basilisk_t3` and
  `thornedhorrorfrost_t3` carry **no** summon, generator or spawn skill of any class. The +10
  cannot come from the placement pool that supplies the modelled 7.

**Q(A2) — does w157 carry exactly the golem p04 candidate and nothing larger?**
**Substantially yes — with two named qualifications.**

- `skeletalgolem_t3` (p04 alternative, `spawnMin = spawnMax = 6`, `sm_mod`) slot
  **`skeletalgolem_b01`** carries **`skillName9` → `skeletalgolem_summonskeletons01`
  [`Skill_SpawnPetMonster`] petLimit 4, petBurstSpawn 4, no TTL** → `skeleton_a02_summon`
  = **Skeletal Archer, Common**. **CONFIRMED-CAPABLE.** ONE in-window spawn = +1 exactly;
  the record permits up to 4.
- **Qualification 1 — a sibling in the same pool.** `skeletalgolem_c01` carries
  `skeletalgolem_summonghosts01` (same class, **petLimit 4, burst 4**) → `ghost_a01_summon`
  (Apparition, Common). If the p04 roll seats a `_c01` alongside a `_b01`, the pool's plain-add
  ceiling is **8**, not 4.
- **Qualification 2 — p04 and p03 are not otherwise clean.** `swampgolem_t3` (the other p04
  alternative) has `swampgolem_c01` → `swampgolem_spawnplants` petLimit **3**; `gargoyle_t3`
  (p03) has `gargoyle_c01` → `eldritchground` petLimit **6** (a ground-object body, see †).
  **Nothing on w157 exceeds petLimit 8, and nothing on p03/p04 exceeds petLimit 6.**
- **Largest producer anywhere on w157** is again `swampcrab_crabgenerator` (petLimit 8) — but it
  is reachable only through **p02 devotion pools** `gdx1/devotion_heroes01` and
  `gdx1/devotion_heroes02`, and only via their `swampcrab_h01…h04` members. **Not on a
  plain-tier pool.**

### 2.4 Structural point that discriminates the two waves — MEASURED

| | w152 | w157 |
|---|---|---|
| plain-tier (trash) spawn points | **1** (p03) | **2** (p03, p04) |
| producer members inside the plain-tier pools | **0 of 6** | **3 of 21** (`skeletalgolem_b01`, `skeletalgolem_c01`, `swampgolem_c01`; + `gargoyle_c01` ground-object) |
| max plain-body petLimit on a plain-tier pool | — (none) | **4** |
| max plain-body petLimit anywhere on the wave | **8** (`swampcrab_crabgenerator`, on p01 hero + p04 boss) | **8** (`swampcrab_crabgenerator`, on p02 devotion only) |
| archer generator present? | only on p06 devotion (2 of 6 pools) | **yes, on p04 trash** (`skeletalgolem_b01`) |

The +10 on w152 must cross a **pool-kind boundary** (hero/boss producer → plain body). The +1 on
w157 does not: it is generated **inside the plain-tier pool that already supplies the model's
count**.

## 3. Part B — ratio structure verdicts

### 3.1 The enabling measurement: the survival life scalar is per-WAVE, so it CANCELS — MEASURED

`records/game/balancingadjustment_survivalmode_enemies03.dbr` [`sm_mod`] carries
`characterLifeModifier` as a **200-element array**. Indexing it as `array[wave − 1]` reproduces
the committed `u8_survival_wave_scaling.csv` gladiator column on **200 / 200 waves**
(`arr[151] = 308` = w152 gladiator; `arr[156] = 318` = w157; `arr[159] = 324` = w160).
`survivalinfo.dbr` binds `…enemies01/02/03` to `survivalAdjustmentNormal / Elite / Ultimate`.

> **CORRIGENDUM to P-E6 § 2.8 (my own prior note).** That table labelled the array "values at
> array index 99 (**level 100**)". The array is **WAVE-indexed, not level-indexed**: index 99 is
> **wave 100**. The § 2.8 numbers (+53 / +120 / +168 %) are therefore the *wave-100* scalars, not
> the level-100 scalars. The Gladiator figure at the KC2 band is **+308 % (w152) / +318 % (w157)**,
> not +168 %. Everything § 2.8 says about the *shape* of the Gladiator regime stands; the
> magnitudes are understated ~2× at the band. Flagged for the conductor to propagate.

**Consequence that makes Part B possible:** for two bodies **in the same wave**, the survival
scalar is a shared constant and divides out. A within-wave HP ratio is therefore
`lifeEq_A(L_A) / lifeEq_B(L_B)` exactly — no unknown multipliers required.

### 3.2 What the corpus permits — MEASURED

Life equations live on the `characterAttributeEquations` proto (`records/creatures/enemies/bios/…`),
which **is present in the Edition-II pin** (695 enemy bio records). Form is always
`((charLevel × k)^p) + c`.

**Exponent census over all 695 enemy bio records:**
`p ∈ {1.2 (1), 1.25 (2), 1.27 (8), 1.28 (37), 1.29 (13), 1.3 (8), 1.33 (250), 1.35 (25),
1.5 (339), 1.53 (11), 1.54 (1)}`. **Corpus maximum p = 1.54.**

**`charLevel` multiplier census over all 2,974 enemy Monster records:**
`×1` on 2,787, `×1.1` on 187. **No other multiplier exists.**

**Level-draw intervals** (`records/proxies/lv*.dbr`, evaluated at `averagePlayerLevel = 100`):

| variance eq | min | max | width |
|---|---:|---:|---:|
| `lv2_normal` | 99.000 | 100.000 | 1.000 |
| `lv3_strong` | 100.000 | **101.333** | 1.333 |
| `lv4_champion` | 101.000 | **102.333** | 1.333 |
| `lv4_champion+` | 101.000 | 103.000 | 2.000 |
| `lv5_elitechampion` | 102.000 | 103.000 | 1.000 |
| `lv6_hero` | **104.000** | **105.000** | 1.000 |
| `lv7_uber hero` | **103.000** | **105.000** | 2.000 |
| `lv8_boss+` | 106.000 | 106.000 | 0.000 |

Two endpoints are **fractional** (`apl + apl/75 = 101.333`). Whether the engine draws an integer
or a real from the interval is **not declared anywhere in the corpus** — that fork is stated
below and both branches are answered.

### 3.3 Achievable same-record HP ratios, restricted to the records actually on each wave

141 life-bearing records on each wave; the (exponent, charLevel-mult) classes present are
w152 `{1.25/×1, 1.28/×1, 1.29/×1, 1.33/×1, 1.5/×1, 1.5/×1.1}` and w157 the same plus `1.33/×1.1`.

**Branch A — INTEGER level draw** (bands identical on both waves):

| level step | achievable HP-ratio band |
|---|---|
| ΔL = 1 | **1.181 % … 1.519 %** |
| ΔL = 2 | **2.364 % … 3.046 %** |
| ΔL = 3 | 3.550 % … 4.580 % |

**Branch B — CONTINUOUS level draw**, max ratio reachable *within one variance interval*:

| variance eq | p1.25 | p1.28 | p1.29 | p1.33 | p1.5 |
|---|---:|---:|---:|---:|---:|
| `lv2_normal` | 1.264 % | 1.295 % | 1.305 % | 1.346 % | 1.519 % |
| `lv3_strong` | 1.669 % | 1.710 % | 1.723 % | **1.777 %** | **2.007 %** |
| `lv4_champion` | 1.653 % | 1.693 % | 1.706 % | 1.760 % | 1.987 % |
| `lv4_champion+` | 2.481 % | 2.542 % | 2.562 % | 2.642 % | 2.985 % |
| `lv5_elitechampion` | 1.227 % | 1.257 % | 1.266 % | 1.306 % | 1.474 % |
| **`lv6_hero`** | 1.203 % | **1.232 %** | 1.242 % | 1.281 % | **1.446 %** |
| `lv7_uber hero` | 2.433 % | 2.492 % | 2.512 % | 2.591 % | **2.927 %** |
| `lv8_boss+` | 0 % | 0 % | 0 % | 0 % | 0 % |

### 3.4 VERDICTS per measured delta — INFERRED

| wave | adjacent classes | Δ | Branch A (integer draw) | Branch B (continuous draw) |
|---:|---|---:|---|---|
| **152** | **42,798 → 43,548 (the LOW PAIR, ×4 + ×3)** | **1.752 %** | **NOT one record.** Falls in the dead gap between ΔL=1 (≤1.519 %) and ΔL=2 (≥2.364 %) | **ONE record admissible, but only from `lv3_strong` at p ≥ 1.33 or `lv4_champion+` / `lv7_uber hero` at any p.** Explicitly **NOT** reachable from `lv6_hero` (max 1.446 %) or `lv5_elitechampion` (max 1.474 %) |
| 152 | 91,696 → 93,599 | 2.075 % | **NOT one record** (dead gap) | one record admissible only from `lv4_champion+` or `lv7_uber hero`, or `lv3_strong` at p=1.5 |
| 152 | 237,258 → 242,124 | 2.051 % | **NOT one record** (dead gap) | same as above |
| 157 | 233,250 → 238,068 | 2.066 % | **NOT one record** (dead gap) | same as above |
| 157 | 398,226 → 406,243 | 2.013 % | **NOT one record** (dead gap) | same as above |
| 157 | 411,440 → 414,837 | 0.826 % | **NOT one record** — *below* the ΔL=1 floor of 1.181 % | one record admissible from any variance eq |
| 157 | **414,837 → 419,839** | **1.206 %** | **CONSISTENT with ONE record at ΔL = 1** (inside 1.181–1.519 %) | one record admissible |

**Four of the six inter-class deltas cluster at 2.01–2.08 %** (two on each wave) — a systematic
signature, not noise. Under Branch A none of them is a same-record level step; under Branch B all
four are reachable **only** from the three widest variance intervals (`lv4_champion+`,
`lv7_uber hero`, or `lv3_strong` at p = 1.5).

### 3.5 The pet constraint — the sharpest structural result in Part B — INFERRED

**Pets carry no `levelVarianceEquation`.** They are not rostered in any pool (L-47 § 2.4 for the
archer; re-verified here for `swampcrab_a00_summon`, `springscrab_a00_summon`,
`chthoniandevourer_a01_summon`, `ghost_a01_summon`). Their level therefore comes from the
summoner, and the rule is **NAMED-ABSENT in the corpus** (L-47 P-2, unchanged — I re-checked and
found no `petLevel`-class Variable on `Skill_MonsterGenerator`, `Skill_SpawnPet`,
`Skill_SpawnPetMonster` or `Skill_TargetedSpawnPet`).

Under the standing corroborated reading *(pets arrive at summoner level)*, this constrains the
w152 low pair hard, because `swampcrab_a00_summon` has **p = 1.28** and `charLevel = charLevel*1`:

| summoner source | its variance eq | level interval | max crabling-HP spread |
|---|---|---|---:|
| p01 `swampcrab_hero` members (Hero) | `lv6_hero` | [104.000, 105.000] | **1.232 %** |
| p04 `swampcrab_carraxus` → `swampcrab_ugdenbog_01` (Quest) | `lv7_uber hero` | [103.000, 105.000] | **2.492 %** |
| **both together** | — | [103.000, 105.000] | **2.492 %** |

> **INFERRED — the discriminating consequence.** Two crablings summoned by **two p01 heroes alone
> cannot differ by 1.752 %** — the `lv6_hero` interval caps the spread at **1.232 %**, under either
> quantisation branch. A 1.752 % crabling pair **requires the p04 boss roll to be
> `swampcrab_carraxus`**, whose `lv7_uber hero` interval reaches down to level 103 and which
> carries **the same `swampcrab_crabgenerator`** (petLimit 8, burst 4). Solving
> `(L₂/L₁)^1.28 = 1.01752` gives `L₂/L₁ = 1.013661`, e.g. **103.0 and 104.41** — both inside the
> union interval, neither inside `lv6_hero` alone.

This yields a **falsifiable prediction for the conductor**: if the census's single w152 skull is
**not** Carraxus, the crabling reading of the low pair fails and hypothesis (i) must be re-seated
on a different producer. If it **is** Carraxus, the low pair's ×4 + ×3 multiplicity, its 1.752 %
split, and the +10 magnitude all resolve on one generator record.

### 3.6 A measured contradiction I am obliged to surface — MEASURED

`monsterClassification` on the **trash-pool rosters** of these two waves is overwhelmingly
`Champion`, not `Common`:

| wave | sp | pool | spawn | Common / roster |
|---:|---:|---|---|---|
| 152 | 3 | `basilisk_t3` | 5–6 | **1 / 3** |
| 152 | 3 | `thornedhorrorfrost_t3` | 5–6 | **0 / 3** |
| 157 | 3 | `chthonianrylok_t3` | 4–5 | 2 / 5 |
| 157 | 3 | `chthonianservitor_t3` | 4–5 | 1 / 5 |
| 157 | 3 | `chthonianleech_t3` | 6 | 1 / 3 |
| 157 | 3 | `gargoyle_t3` | 3–4 | 1 / 6 |
| 157 | 4 | `swampgolem_t3` | 3–5 | **0 / 3** |
| 157 | 4 | `aetherialbloater_t3` | 5–6 | 2 / 5 |
| 157 | 4 | **`skeletalgolem_t3`** | 6 | **0 / 6** |
| 157 | 4 | `yetidire_t3` | 5–6 | **0 / 4** |

All ten pools carry `championChance = 0`, so every one of those bodies enters through the
**regular** roster, not the champion roster. Yet galadriel measures only **6 stars on w152** and
**6 on w157** against 17 and 15 plain.

> **Therefore the census's star glyph does NOT key on the record's `monsterClassification` field.**
> It must key on the pool-level champion mechanic (`championChance` / `nameChampion{j}`), which is
> a different axis. **This is load-bearing for how any "plain-tier" claim maps back to records** —
> and it means my own PLAIN/Champion column in § 2.1–2.2 (which *is* keyed on
> `monsterClassification`) is a **record-taxonomy label, not a screen-tier prediction**.
> Two summoned bodies I marked "Champion" (e.g. `skeleton_b02_knight_summon`,
> `aetherialcorruption_c01_summon`) may well render plain. **This widens, never narrows, the
> add-capacity of both waves.** Handed back as R-1 in § 6.

## 4. Part C — exact HP join status — **NAMED-BLOCKED-ON-T15**

I stopped Part C rather than estimate. What I closed, and exactly what remains open:

**Closed this session (an accelerant for T15, not a substitute for it):**

| link | status | citation |
|---|---|---|
| base life proto (`characterAttributeEquations` → `bios/bio_*.dbr`) | **PRESENT in the Edition-II pin**, 695 enemy records, form `((charLevel·k)^p)+c` | MEASURED, § 3.2 |
| spawn level (`levelVarianceEquation` → `records/proxies/lv*.dbr`) | **PRESENT**, 8 equations, intervals tabulated | MEASURED, § 3.2 |
| survival/wave scalar | **PRESENT and wave-indexed**; w152 Gladiator **+308 %**, w157 **+318 %** | MEASURED, § 3.1 |
| base-difficulty scalar (`balancingadjustment_mp+difficulty_enemies01.dbr`, `base`) | **PRESENT**: `characterLifeModifier` = 12-array `[50×4, 320×4, 580×4]` (difficulty × player-count); `characterLifeMultModifier` = `[0, 90, 180, 270]×3`. **Ultimate solo → +580 %, mult +0 %** | MEASURED |

**Still open — and each one alone blocks an exact join:**

1. **The stacking rule is undeclared.** Two records both write `characterLifeModifier`
   (`+580 %` base-difficulty, `+308 %` survival-wave). Additive-within-field gives ×9.88;
   multiplicative-across-records gives ×27.74. **Nothing in the corpus states which.** The two
   readings differ by a factor of 2.8 — larger than any inference I would be willing to carry.
2. **The effective `averagePlayerLevel` inside a Crucible run is not established.** Every
   variance equation is expressed in it; I assumed 100 throughout § 3 **for ratio work only**,
   where it cancels to first order. An absolute join cannot assume it.
3. **The pet-level rule remains NAMED-ABSENT** (L-47 P-2). Every add in § 2 is a pet.
4. **The mutator layer is unquantified.** `survivalinfo.dbr` declares `mutatorFx` / `mutatorSound`;
   no enemy-side magnitude was located and I did not go looking, being out of commission scope.

**Arithmetic check I ran and am reporting rather than using:** under the *additive* stacking
reading at `apl = 100`, `swampcrab_a00_summon` at level 103 composes to ≈ 37.2 k against a measured
low pair of 42.8 k / 43.5 k — **same order, ~15 % short.** That is consistent with the chain being
*incomplete* rather than *wrong*, and it is **not** a derivation. I did not solve for the level
that would close it. **PART C IS BLOCKED. NO HP VALUE IN THIS NOTE IS DERIVED.**

## 5. Adjudication input

**Which w152 hypothesis the record evidence supports.** The record evidence supports
**hypothesis (i), non-archer generator adds, and it is now the only hypothesis with a
measured mechanism behind it — but the producer is on the hero/boss points, not on the plain-tier
pool.** The decisive measurements are three. First, w152's *only* plain-tier pool (p03) is
**NAMED-ABSENT for producers**: all six members of `basilisk_t3` and `thornedhorrorfrost_t3` carry
no summon, generator or spawn skill of any class, so the +10 cannot originate where the modelled
7 originate. Second, the wave nonetheless carries **abundant plain-body generator capacity** —
`swampcrab_crabgenerator` (`Skill_MonsterGenerator`, **petLimit 8, petBurstSpawn 4, TTL 30 s**) →
`swampcrab_a00_summon` "Ugdenbog Crabling", `Common` — sitting on **all five members of the p01
`swampcrab_hero` pool AND on the p04 boss Carraxus**, with the parallel `springscrab_crabgenerator`
(same 8/4/30) on the alternative p01 pool; one summoner alone is licensed for eight plain bodies,
so +10 needs only two. Third, the **multiplicity signature matches the record**: `petBurstSpawn = 4`
is exactly the ×4 class, and ×4 + ×3 = 7 sits under a per-summoner cap of 8. Hypothesis (ii),
p05 drip replenishment, is **NAMED-ABSENT as a plain-body source on w152**: p05 is
`poolsherogdx1/aetherialcorruption_hero`, `spawnMin = spawnMax = 0` with `championChance = 100 %`
— it emits heroes, and its only plain-body reach is one Ice Spike trap on one of five members.
Hypothesis (iii) stays demoted; the low pair is 13/13 eye-read RED and census-handled. The one
qualification I attach, and it is a real one, is § 3.5: the 1.752 % split **cannot** come from two
`lv6_hero` summoners (interval-capped at 1.232 % for a p=1.28 pet), so the crabling reading
**requires the p04 roll to have been `swampcrab_carraxus`** — a check the conductor can run against
the census's single w152 skull, and one that will either seat the mechanism cleanly or force the
producer to be re-identified among the p06 devotion generators (`chthonianabomination_summondevourers_a01`,
limit 8 / burst 4, is the only other limit-8 plain producer on the wave).

**w157 golem candidate: CONFIRMED-CAPABLE.** `poolsbasic/skeletalgolem_t3` [`sm_mod`,
`spawnMin = spawnMax = 6`], roster slot 1 → `skeletalgolem_b01` [`monsterClassification = Champion`,
`charLevel = (charLevel*1.1)+2`, `levelVarianceEquation1 = lv4_champion`, `limit1 = 2`,
`minPlayerLevel1 = 35`] → **`skillName9` → `skeletalgolem_summonskeletons01`
[`Skill_SpawnPetMonster`, `petLimit = 4`, `petBurstSpawn = 4`, no TTL] →
`skeleton_a02_summon` = "Skeletal Archer", `monsterClassification = Common`.** The fields exist to
produce exactly +1 (one in-window spawn), and the declared ceiling from one summoner is 4. Two
qualifications travel with the confirmation: (a) `limit1 = 2` permits **two** `skeletalgolem_b01`
in one p04 spawn, so the pool ceiling is **8**, not 4 — model the cap per-summoner, not per-wave
(identical structure to the w153 Death Revenant, L-47 § 2.2); (b) the same pool's
`skeletalgolem_c01` carries `skeletalgolem_summonghosts01` (also petLimit 4 / burst 4 →
`ghost_a01_summon`, Common), so a mixed p04 roll raises the plain-add ceiling further.
**Nothing on w157's p03 or p04 exceeds petLimit 6, and nothing anywhere on w157 exceeds
petLimit 8** (`swampcrab_crabgenerator`, reachable only through the p02 devotion pools). The
answer to "the golem candidate and nothing larger" is therefore **yes on the plain-tier points,
with a named larger producer off them.**

## 6. Named gaps

| # | Gap | Grade | Owner |
|---|---|---|---|
| **R-1** | **The census's star glyph does not key on `monsterClassification`** (§ 3.6): ten trash pools with `championChance = 0` carry majority-`Champion` rosters, yet only 6 stars are measured on each wave. My PLAIN/Champion column in § 2.1–2.2 is a **record-taxonomy label, not a screen-tier prediction**. Bodies I marked Champion may render plain — this can only **widen** add capacity. | **CONTRADICTION SURFACED** | conductor → galadriel |
| **R-2** | **P-E6 § 2.8 corrigendum**: `balancingadjustment_survivalmode_enemies03` is **wave-indexed**, not level-indexed. The band's Gladiator life scalar is **+308 % / +318 %**, not the +168 % that note reports. | **CORRECTION** | conductor (propagate) |
| **R-3** | **Part C blocked on four named unknowns** (§ 4): the `characterLifeModifier` stacking rule, the in-Crucible `averagePlayerLevel`, the pet-level rule (L-47 P-2, still open), and the mutator layer. The proto + variance + both scalar records are now located — T15 is narrower than the ledger records it. | **NAMED-BLOCKED-ON-T15** | conductor → matt_to_do / gamora |
| **R-4** | **The integer-vs-continuous level draw is undeclared** (§ 3.2). Two variance equations have fractional endpoints (`apl + apl/75`). Every Part-B verdict forks on it and both branches are given, but the fork is not closable from the database. A single in-game monster-level readout at known `apl` would settle it. | **NAMED-ABSENT (declaration)** | conductor → galadriel (footage lane) |
| **R-5** | **Trap / ground-object bodies are `Class = Monster`, `Common`, and I cannot tell whether they carry a fingerprintable health bar.** Five such bodies are reachable on w152 (`trap_brambletrap_a01` life = flat **15**; `trap_icespike_hero_a01`, `trap_lightningspike_hero_a01`, `chthonianabomination_tentacles_a01`, `eldritchground` all share life `((charLevel*10)^1.25)+60`; `krieg_aethertrap` life = flat **150**, `charLevel = 1`). If they render bars they are plain bodies the model never counts; if not, they are noise. **The database cannot answer this.** | **RENDERING QUESTION — DB-UNANSWERABLE** | conductor → galadriel |
| **R-6** | **Three `.dbr` references on w157 p02 devotion heroes do not resolve** in the Edition-II pin: `nonplayerskills/bossskills/angela_arcaneblast.dbr` (via `chthonianrylok_h04.skillName16`) and `nonplayerskillsgdx3/attackmelee/dranghoul_butcher.dbr` (via `dranghoul_h01/h02.skillName8`). Both are attack skills by name, so producer risk is low, but they are **unresolved and named rather than assumed**. | **MISSING-REF (3 of ~2,900 edges)** | legolas |
| **R-7** | `records/creatures/anomalies/eldritchground.dbr` sits under **`anomalies/`**, not `enemies/` — it is the only w157 plain-body candidate outside the enemy tree. Its `Class` is nonetheless `Monster`. Whether the engine treats `anomalies/` bodies as hostiles for census purposes is **not established**. | **FLAG** | conductor |
| **R-8** | The **census-window timing** of every add is out of scope here and unresolved. `petPeriod` 6 s / `spawnObjectsTimeToLive` 30 s (crablings) versus a 10.2 s w152 cohort window means the *record capacity* stated in § 2 is a **ceiling**, not a prediction of in-window arrivals. Nothing in this note claims an arrival count. | **OUT-OF-SCOPE, NAMED** | conductor → gamora |

---

**Filed:** legolas (UNKNOWN-RESEARCHER), 2026-08-08, KC2-SIM mechanism-adjudication join.
Every Part-A row DB-CITED or explicitly NAMED-ABSENT. Every Part-B conclusion tagged INFERRED and
forked where the corpus does not decide. Part C explicitly **NAMED-BLOCKED-ON-T15** with zero
values estimated. Edition-II corpus only; **zero external fetches; zero fitted parameters.**
Note UNCOMMITTED per commission — the conductor folds and commits.
