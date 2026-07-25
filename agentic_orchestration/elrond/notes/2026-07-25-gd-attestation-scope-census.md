# GD attestation scope census — the two-sided "needed" filter

**Agent:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-elrond-gd-attestation-scope-census.md`
**Type:** ANALYSIS / DATA CENSUS — read-only. No schema changes, no writes to corpus.db, no production code.
**Date:** 2026-07-25
**Reproducibility script:** `agentic_orchestration/research/scripts/gd_attestation_census_2026_07_25.py`
(reuses the productionized TQIT `.arz` parser from `gd_arz_adapter_2026_07_24.py`)

**Read-only attestation:** `corpus.db` mtime is unchanged at `2026-07-24 21:29` after this run; the
script opens it `file:...?mode=ro`. All `.arz` access is read-only. `git status` on
`agentic_orchestration/research/` is clean apart from the new script.

---

## SUMMARY (≤12 lines)

```
40 ControllerMonster states, all classified against the two-sided filter:
    IN (both P and M)        11
    IN (M only)              22
    OUT-BY-ATTESTATION        5   (Panic; QuestWalk/QuestMove/QuestUseSkill/QuestPlayAnimation)
    NEEDS-JOIN                2   (WanderPause; Patrol)
  -> PROPOSED G1-B SCOPE ROSTER = 33 states

84 behavioural controller parameters (87-field union over combat-relevant monsters'
controllers, less 3 metadata fields Class/templateName/FileDescription):
    IN                       62   (>=1% non-inert attestation)
    OUT-BY-ATTESTATION       22   (<1%; eye*/synergy*/spirit*/pet-target/appearDistance/pursueBehavior)

HEADLINE REVERSAL vs the provisional triage: the parameter<->creature join is NOT inference.
Every combat-relevant monster record carries a direct `controller` field; 3,207/3,207 resolve.
D-b is retired FOR THE .arz LANE ONLY (grimtools carries no controller field at all).

HEADLINE FIND: `EmoteBeforePursuingChance` (93.0% attestation, mode 20) is the entry gate for
AlertBeforePursue — the binding the binary-inspection research doc listed as "cannot determine".
```

---

## 1. Substrate actually read

| Side | Source | What landed |
|---|---|---|
| Monster (TRUE SOURCE) | `~/Games/vendor/grim-dawn-edition-II-20260724/` — `database.arz` + `GDX1/2/3.arz` | 4,066 `Monster` records; 442 `Controller*` records; 15,422 skill/item/buff records scanned |
| Monster (corroborating) | `research/datamine-acquisition/gd/raw/all_monsters.js` | 2,636 entries (regex count) |
| Player (P) | `research/curated/corpus.db` — `canon_corpus`/`kit_master`/`kit_dossier`/`kit_numeric` | 41 GD-lane kits, 246 dossier rows, 26 KF-2 numeric anchors |
| Vocabulary | `research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md` + `gamora/notes/2026-07-25-gd-40-state-coverage-audit.md` | 40 states; F1–F9 + L1/L2 family structure |

**`gdx3` note:** the dispatch anticipated "41 + any gdx3 rows" in corpus.db. There are **no gdx3 rows** —
`SELECT DISTINCT game FROM canon_corpus WHERE game LIKE 'gd%'` returns `gd` only, and zero kit_ids or
lineage values contain `gdx`. The GD lane is exactly 41 kits. The gdx3 *content* is present on the
monster side (`GDX3.arz` contributes 958 Monster records, 52 controllers) but has no player-side kit.

---

## 2. Combat-relevance filter — the predicate, stated for audit

A `.arz` record **R** is a **COMBAT-RELEVANT MONSTER** iff ALL of:

| # | Clause | Excluded by this clause |
|---|---|---|
| F1 | `R`'s record-table type == `Monster` | `Npc` (672), `Pet` (1,412), `Proxy`, `ProxyAmbush`, `Decoration`, `ScriptEntity`, `Destructible` |
| F2 | NOT `R.path.startswith('records/sandbox/')` | 241 (dev scratch: `sandbox/ben`, `sandbox/adam`, `sandbox/eric`, …) |
| F3 | NOT `R.path.startswith('records/creatures/npcs/')` | 58 |
| F4 | NOT `R.path.startswith('records/creatures/ambient/')` | 15 |
| F5 | `'testdummy' not in R.path` | 10 |
| F6 | `R.hiddenFromCombat is not True` | 203 |
| F7 | `R.invincible is not True` | 70 |
| F8 | `R.targetable is not False` | 204 |
| F9 | `R.defaultTeamMajor != 'TeamMajor_Human'` | 50 (friendly town/faction guards) |

**Result: N = 3,207** of 4,066 `Monster` records (287 excluded after F2; F2 itself removed 241 from 4,066).
Clause counts overlap; the union is 287.

Composition of the kept set: Hero 1,255 / Champion 912 / Common 508 / Quest 428 / Boss 75 / SuperBoss 29.

**Three filter decisions worth flagging, because a different reviewer could reasonably differ:**

- **`monsterClassification == 'Quest'` (428) is KEPT.** Sampling shows these are quest *bosses*
  (`grundleplith` "Rat Hoarder", `skeleton_stepsoftorment_01` "Grand Priest Zarthuzellan",
  `dranghoul_jaggedwaste` "Bloodfeast - Quest Groble Tyrant"), not quest-givers. They fight.
  This is NOT the same population as the `Quest*` controller states — see §2.3.
- **`records/skills/nonplayerskills*/` creature records (133) are KEPT.** These are boss-summoned
  adds authored as Monster records under the summoning skill's directory. They are combat actors.
- **`records/endlessdungeon/creatures/` (287 records) are KEPT** where they pass F3–F9. Shattered
  Realm monsters are combat-relevant.

### 2.1 The `quest` field is not the Quest-state discriminator

`quest` is **`False` on 3,207/3,207 kept monsters**, **`False` on 0/287 excluded monsters** (i.e.
also all-False), and **`False` on 216/216 base-archive `Npc` records**. There is no record in the
monster or NPC population with `quest = True`. Quest scripting rides `questFile1` (293 monsters,
9.1%), `taskUID1..10`, `onDie` (382), and `onAddToWorld` (140) — **script callbacks, not controller
states.** This is the load-bearing evidence for the four `Quest*` OUT verdicts in §3.

### 2.2 "Non-default" — the operational definition

The `.tpl` template defaults live inside the `.arc` resource bundles, which are out of scope for
this pass (same boundary as the GD-SLICE run's `.arc` localization deferral). So "non-default"
is operationalized as **non-inert**, semantically per type — and this is the *stronger* test,
because it asks "does this parameter permit the state to fire at all", not "does it differ from
a sibling":

| Value kind | Non-inert iff |
|---|---|
| numeric | `!= 0` |
| bool | `is True` |
| string | not in `{NeverFlee, NeverRoam, NeverUseSkill, None, ''}` |
| list (rank array) | any element `!= 0` |
| absent | inert (template default inherited) |

Both `present` and `non-inert` counts are reported throughout so a reader can substitute a different
definition without re-running.

---

## 3. The census matrix — 40 ControllerMonster states

All monster-side counts are **combat-relevant monsters (of N = 3,207)**, monster-weighted through the
`controller` join where the attesting field lives on the controller.

| # | State | Monster-side class | n | % | Attesting field(s) | Player-side (P) | **Verdict** |
|---|---|---|---|---|---|---|---|
| 1 | `Idle` | DATA-ATTESTED + ENGINE-UNIVERSAL | 1,830 | 57.1% | `ChanceToIdleOnPatrol`, `MaxPatrolIdleTime` (1,831), `MinPatrolIdleTime` (1,180) | NO | **IN (M)** |
| 2 | `Startup` | DATA-ATTESTED | 1,359 | 42.4% | `initialSkillName` 1,359; `initial2SkillName` 71; `onAddToWorld` 140 | NO | **IN (M)** |
| 3 | `Attack` | ENGINE-UNIVERSAL + DATA | 3,202 | 99.8% | any resolved skill ref; `attackSkillName` 1,461; `specialAttackChance` 2,957 | YES — all 41 kits | **IN (both)** |
| 4 | `Pursue` | DATA-ATTESTED | 3,206 | 100.0% | `ViewDistance`, `InnerViewDistance` (3,206), `MaxPursuitDistance`/`PursuitTime` (3,205) | YES — 4 kite kits (`gd-bloody-pox-conjurer`, `gd-bwc-demolitionist`, `gd-flames-of-ignaffar-purifier`, `gd-pet-conjurer`) | **IN (both)** |
| 5 | `RepositionForAttack` | DATA-ATTESTED | 1,608 | 50.1% | `enemyTooClose` 1,608; `RepositionChance` 961; `randomRepositionChance` 680 | YES — `gd-flames-of-ignaffar-purifier` (dossier: "reposition") | **IN (both)** |
| 6 | `JumpAttack` | DATA-ATTESTED (skill-class join) | 191 | 6.0% | `Skill_AttackWeaponBlink` on 191 monsters (41 monster-lane skill records) | YES — `gd-shadow-strike-infiltrator` (`playerclass04/shadowstrike.dbr` **is** `Skill_AttackWeaponBlink`) | **IN (both)** |
| 7 | `Roam` | DATA-ATTESTED | 2,573 | 80.2% | `RoamBehavior=='Roam'` 2,573; `RoamDistance`/`MinRoamDistance` 2,966; `Min/MaxTimeBeforeRoam` 3,075 | NO | **IN (M)** |
| 8 | `Flee` | DATA-ATTESTED | 666 | 20.8% | `FleeBehavior != NeverFlee` — **`FleeOnLowHealth` 359 / `FleeOnDamage` 248 / `FleeWhenEnemyClose` 59**; `FleeChance` 952; `fleeDistance` 2,024 | NO | **IN (M)** |
| 9 | `WanderPause` | **NEEDS-JOIN** | — | — | No dedicated field. `Min/MaxPatrolIdleTime` is patrol dwell; `Min/MaxTimeBeforeRoam` is roam interval. Which (if either) drives `WanderPause` is not decidable from records. | NO | **NEEDS-JOIN** |
| 10 | `Wander` | DATA-ATTESTED | 768 | 23.9% | `WanderDistance > 0` 768; `MinWanderDistance` 3,073 | NO | **IN (M)** |
| 11 | `Dying` | DATA-ATTESTED | 1,577 | 49.2% | `Skill_OnDeathSpawnActor` on 1,577; `dyingSkillName` 700; `chanceToSpawnOnDeath` 1,308; `onDie` 382; `deathFromEnemyDelay` 141 | NO | **IN (M)** |
| 12 | `Return` | DATA-ATTESTED | 3,205 | 99.9% | `MaxPursuitDistance`, `PursuitTime`; `ResetOriginAfterFleeing` 639 | NO | **IN (M)** |
| 13 | `FollowLeader` | DATA-ATTESTED | 1,640 | 51.1% | `LeadChance` (rank array, non-zero any rank) 1,640; `TeleportToLeaderDistance` 3,207 (100%) | NO | **IN (M)** |
| 14 | `Dead` | ENGINE-UNIVERSAL | 3,207 | 100.0% | terminal state; every fight resolves here | YES — every kit | **IN (both)** |
| 15 | `NavigateObstacle` | DATA-ATTESTED | 3,207 | 100.0% | `pathMass`, `pathingSize`, `avoidForce` (3,180 non-inert) universal; `useBoundingBoxesForDynamicObstacles` 210; `pathingViewDistance` 148; `forceCollision` 783 | NO | **IN (M)** |
| 16 | `DefendLeader` | DATA-ATTESTED | 1,640 | 51.1% | `healLeaderHealthPercentage` 3,106; `LeadChance` 1,640; `BuffAllyBehavior != NeverUseSkill` 3,196 | NO | **IN (M)** |
| 17 | `Charge` | DATA-ATTESTED (skill-class join) | 385 | 12.0% | `Skill_AttackWeaponCharge` on 385 monsters (68 monster-lane skill records incl. `nonplayerskills/attackcharge/`) | YES — `gd-cadence-witchblade` + `gd-krieg-death-knight` (Blitz = `playerclass01/blitz1.dbr` **is** `Skill_AttackWeaponCharge`); `gd-vires-might-shieldbreaker` (dossier: "charge/dash through pack", "11-meter charge range") | **IN (both)** |
| 18 | `Move` | ENGINE-UNIVERSAL + DATA | 3,206 | 100.0% | `characterRunSpeed` 3,180; `walkSpeed` 3,143; `walkDistance` 1,860; `walkUsesRun` 1,138 | YES — all kits | **IN (both)** |
| 19 | `Panic` | **UNREACHED** | 0 | 0.0% | No controller field, no monster field, no offensive/defensive skill channel. Nearest neighbours are already bound: `FleeBehavior`→`Flee`, `RandomAngerChance`→aggro | NO | **OUT-BY-ATTESTATION** |
| 20 | `DodgeAttack` | DATA-ATTESTED | 1,448 | 45.2% | `DodgeDistance` 1,448; `MinDodgeDistance` 1,439; `DodgeDelay` 1,536; `DodgeChance` 1,133 | NO (`characterDodgePercent`, 24 monsters, is a hit-avoidance stat — a **different mechanism**, do not count) | **IN (M)** |
| 21 | `Confused` | DATA-ATTESTED (skill channel only) | 9+9 skills | — | `offensiveConfusion*` on 9 player-class + 9 monster skill records (`playerclass02/flashbang1`, `playerclass03/evileye3`; `loghorrean_roarofmadness`). `defensiveConfusion` on **0/3,207** monsters → schema-present, record-unconfigured → universal susceptibility | NO — no GD-lane kit carries a confusion skill | **IN (M)** |
| 22 | `Paralyze` | DATA-ATTESTED | 567 | 17.7% | `defensivePetrify` non-zero 567; `offensivePetrify*` on 15 monster skills, **0 player skills** | NO | **IN (M)** |
| 23 | `Trapped` | DATA-ATTESTED | 728 | 22.7% | `defensiveTrap` non-zero 728; `SkillBuff_DebufTrap` record class; `offensiveTrap*` on 2 player skills (`playerclass06/graspingvines2`) | **NO** — see §3.1 false-positive warning | **IN (M)** |
| 24 | `Immobile` | DATA-ATTESTED | 728 | 22.7% | `defensiveTrap` 728, `defensiveFreeze` 622, `disableMovement` 3; `offensiveFreeze` 7 player skills, `offensiveSlowRunSpeed` 4 player skills | YES — `gd-aar-spellbinder` (freeze), `gd-callidors-tempest-templar` + `gd-retaliation-warlord` (slow) | **IN (both)** |
| 25 | `KnockedDown` | DATA-ATTESTED | 1,810 | **56.4%** | `defensiveKnockdown` non-zero 1,810 — **the densest CC channel in the bestiary**; `offensiveKnockdown*` on 11 player skills (`playerclass05/razorwind1b`, `playerclass02/flamestrike3`) | **NEEDS-JOIN** — 11 player skills carry it, but the kit→`.arz`-skill-record join is not built, so I cannot say whether any of the 41 kits is among them | **IN (M); P = NEEDS-JOIN** |
| 26 | `Stunned` | DATA-ATTESTED | 906 | 28.3% | `defensiveStun` non-zero 906; `offensiveStun*` on 19 player + 165 monster skills | YES — `gd-stun-jacks`, `gd-stormbox-elementalist` | **IN (both)** |
| 27 | `Scared` | DATA-ATTESTED (thinnest in the register) | 1 skill | — | `offensiveFear*` on **1** player skill (`playerclass01/warcry1b`, Break Morale/Terrify), **0** monster skills; `defensiveFear` on 0/3,207 monsters | NO | **IN (M)** |
| 28 | `Sleeping` | DATA-ATTESTED — **two independent lanes** | 1,468 | 45.8% | (a) CC-sleep: `defensiveSleep` non-zero 894; `offensiveSleep` 1 player skill (`shadowstrike_mod2`). (b) dormant-until-proximity: `ignoreSleepingEnemies == True` on **1,468** monsters' controllers + 454 `ProxyAmbush` records (`alertArea` 6.0, `spawnThreshold`, `minSpawnTime`, `chanceToRun`) + `monsterSleepAggressionFalloffRate` engine constant | NO | **IN (M)** |
| 29 | `WaitToAttack` | DATA-ATTESTED | 3,207 | **100.0%** | `numAttackSlots` on **3,207/3,207** — values 4 (55.1%) / 8 (43.7%) / 12 / 16 / 20 / 30; `numDefenseSlots` likewise; `maxSwingPause` 3,081 / `minSwingPause` 2,905 | NO | **IN (M)** — highest attestation density of any non-universal state |
| 30 | `Patrol` | **NEEDS-JOIN** | 1,830 params / **4** path records | 57.1% / 0.1% | `ChanceToIdleOnPatrol` 1,830 + `Min/MaxPatrolIdleTime` 1,831 configured — but only **4 `PatrolPoint` records exist across all four archives**. Parameters are set; the level-design substrate they consume is effectively absent | NO | **NEEDS-JOIN → leans OUT** |
| 31 | `QuestWalk` | UNREACHED | 0 | 0.0% | `quest == False` on 3,207/3,207 kept, 0/287 excluded, 216/216 `Npc`. Quest logic is `questFile1`/`taskUID*`/`onDie` script callbacks | NO | **OUT-BY-ATTESTATION** |
| 32 | `QuestMove` | UNREACHED | 0 | 0.0% | as row 31 | NO | **OUT-BY-ATTESTATION** |
| 33 | `QuestUseSkill` | UNREACHED | 0 | 0.0% | as row 31 | NO | **OUT-BY-ATTESTATION** |
| 34 | `QuestPlayAnimation` | UNREACHED | 0 | 0.0% | as row 31 | NO | **OUT-BY-ATTESTATION** |
| 35 | `TakeHit` | DATA-ATTESTED | 3,177 | 99.1% | **`hitThreshold` on 3,206 (100%), 14 distinct values** (mode 100, then 20/25/30/33/50) — a real per-monster hit-reaction threshold; `AttackedAnger` 3,182; `ProjectileAnger` 3,192; `AllyAttackedAnger` 3,175; per-stance `TakeHitAnim` on 3,346 | YES — every kit deals damage | **IN (both)** |
| 36 | `GettingUp` | DATA-ATTESTED | 1,810 | 56.4% | `GetUpFaceDownAnimSpeed` / `GetUpFaceUpAnimSpeed` on 3,346 records across 6 stance families; reachability gated by `defensiveKnockdown` (1,810) | NO | **IN (M)** |
| 37 | `UseSkillOnPoint` | DATA-ATTESTED | 2,977 | 92.8% | `specialAttackRange` enum on 2,977 (`ShortRange` 1,505 / `MediumRange` 618 / `AnyRange` 462 / `LongRange` 392); ground-point delivery classes `Skill_AttackProjectileDrop` (37 monster records) + `Skill_TargetedSpawnPet` (69 monster records) | YES — `gd-wendigo-totem-ritualist` ("Totems placed at ground positions"), `gd-word-of-pain-tactician` ("ground field under player"), `gd-mortar-purifier` (`mortartrap1` **is** `Skill_TargetedSpawnPet`), `gd-trozan-druid` (`skyshard1` **is** `Skill_AttackProjectileDrop`) | **IN (both)** |
| 38 | `UseSkillOnAlly` | DATA-ATTESTED | 3,106 policy / 155 skill | 96.9% / 4.8% | `healAllyHealthPercentage` 3,106; `BuffAllyBehavior`/`BuffAllyTargeting` 3,196–3,198; monsters carrying `Skill_BuffOther` 155; `healSkillName` 77; `buffOtherSkillName` 139 | NO — solo-scope engine; cf. `mechanic_gap_docket` #2 (aurabot party-support scope boundary, Matt-ratified 2026-07-19) | **IN (M)** |
| 39 | `Emote` | DATA-ATTESTED | 2,309 | 72.0% | `randomEmoteChance > 0` 2,309; `randomEmoteMin/MaxTime` 2,777; `emoteSound` 29; per-stance `EmoteAnim` on 3,494 | NO | **IN (M)** — see §5(b), this reverses a PROPOSED-OUT |
| 40 | `AlertBeforePursue` | DATA-ATTESTED | 2,983 | **93.0%** | **`EmoteBeforePursuingChance > 0` on 2,983** (mode 20, distribution 20/15/0/10/25/30); `alertAnimChance` 3,195 (non-zero 3,081; mode 30, then 100); `alertSoundChance` 3,207; `alertSound` 3,152; anger stack `SightAngerRate`/`InnerSightAngerRate`/`AngerTolerance`/`ForgiveRate` | NO | **IN (M)** — see §5(a) |

### 3.1 One player-side FALSE POSITIVE, called out so it is not banked

A naive text search of the GD dossiers returns `trap` on three kits — `gd-blade-trap`,
`gd-mortar-purifier`, `gd-roh-infiltrator`. **None of these attests the `Trapped` state.** In all
three, "trap" names a *deployable* (Blade Trap, Mortar Trap, Rune of Hagarrad), not the entrapment
CC. `gd-blade-trap`'s own dossier is explicitly a *negative* on the adjacent question:
`"Must be cast directly on enemy (not ground placement)"`. The genuine `offensiveTrap` player skill
is Grasping Vines (`playerclass06/graspingvines2`), which no GD-lane kit carries. `Trapped` is
therefore **IN (M), P = NO**.

A second near-miss: `confus` matched `gd-dee-witch-hunter`, but the match is in `anchor_quote` prose,
not in a mechanics payload. Not counted.

---

## 4. Controller-parameter roster — 87 fields, monster-weighted

The union of fields over the controllers actually referenced by the 3,207 combat-relevant monsters is
**87 fields** (90 across all 442 controller records). Removing the 3 metadata fields
(`Class`, `templateName`, `FileDescription`) leaves **84 behavioural parameters**: 62 IN, 22 OUT.

### 4.1 IN — 62 parameters at ≥1% non-inert attestation

Grouped by family, `non-inert count (%)`:

**F1 aggro onset / perception (7):** `ViewDistance` 3,206 (100.0%) · `InnerViewDistance` 3,206 (100.0%) ·
`MaxYViewDistance` 3,197 (99.7%) · `MaxPursuitDistance` 3,205 (99.9%) · `PursuitTime` 3,205 (99.9%) ·
`pathingViewDistance` 148 (4.6%) · `ignoreSleepingEnemies` 1,468 (45.8%)

**F2 anger / pre-commitment (9):** `SightAngerRate` 3,194 (99.6%) · `InnerSightAngerRate` 3,192 (99.5%) ·
`ProjectileAnger` 3,192 (99.5%) · `AttackedAnger` 3,182 (99.2%) · `AllyAttackedAnger` 3,175 (99.0%) ·
`ForgiveRate` 2,647 (82.5%) · `AngerTolerance` 1,935 (60.3%) · `RandomAngerEvaluationTime` 1,112 (34.7%) ·
`RandomAngerChance` 773 (24.1%) — **plus `EmoteBeforePursuingChance` 2,983 (93.0%)**

**F3 leash + return (3):** `MaxPursuitDistance` · `PursuitTime` · `ResetOriginAfterFleeing` 639 (19.9%)

**F4 idle loop (8):** `Min/MaxTimeBeforeRoam` 3,075 (95.9%) · `MinWanderDistance` 3,073 (95.8%) ·
`Min/RoamDistance` 2,966 (92.5%) · `RoamBehavior` 2,573 (80.2%) · `MaxPatrolIdleTime` 1,831 (57.1%) ·
`ChanceToIdleOnPatrol` 1,830 (57.1%) · `MinPatrolIdleTime` 1,180 (36.8%) · `WanderDistance` 768 (23.9%)

**F5 distress + pack (8):** `TeleportToLeaderDistance` 3,207 (100.0%) · `DistressResponseBehavior`
3,123 (97.4%) · `healAllyHealthPercentage` / `healLeaderHealthPercentage` 3,106 (96.9%) ·
`ChanceToRespondToDistressCall` 3,044 (94.9%) · `DistressResponseGroup` 2,949 (92.0%) ·
`LeadChance` 1,640 (51.1%)

**F6 combat spacing (9):** `BuffAllyTargeting` 3,198 (99.7%) · `BuffAllyBehavior` / `BuffSelfBehavior` /
`DebuffEnemyBehavior` 3,196 (99.7%) · `maxSwingPause` 3,081 (96.1%) · `minSwingPause` 2,905 (90.6%) ·
`enemyTooClose` 1,608 (50.1%) · `DodgeDelay` 1,536 (47.9%) · `DodgeDistance` 1,448 (45.2%) ·
`MinDodgeDistance` 1,439 (44.9%) · `DodgeChance` 1,133 (35.3%) · `RepositionChance` 961 (30.0%) ·
`randomRepositionChance` 680 (21.2%)

**F7 fear granularity (6):** `fleeDistance` 2,024 (63.1%) · `FleeDelay` 1,804 (56.3%) ·
`FleeTime` 1,416 (44.2%) · `maxFleeCount` 1,191 (37.1%) · `FleeChance` 952 (29.7%) ·
`FleeBehavior` 666 (20.8%) · `FleeTarget` 2,593 (80.9%)

**Emote (3):** `randomEmoteMin/MaxTime` 2,777 (86.6%) · `randomEmoteChance` 2,309 (72.0%)

**Pet-lane (4, flagged):** `ignorePetsInterval` 3,178 (99.1%) · `petAngerTransference` 3,176 (99.0%) ·
`petTargetLevelRange` 3,170 (98.8%) · `ignorePetsChance` 1,330 (41.5%). These govern how a *monster*
treats *player pets* — in scope only once the engine has a pet actor. **Flagged, not ruled.**

### 4.2 OUT-BY-ATTESTATION — 22 behavioural parameters below the 1% threshold

(23 fields fall below 1%; `FileDescription` is metadata and was never in the behavioural 84.)

| Parameter cluster | Fields | Non-inert n | Why |
|---|---|---|---|
| `eye*` | `eyeDodgeChance`, `eyeLeadChance`, `eyeRandomRepositionChance`, `eyeTimeMax`, `eyeTimeMin`, `eyeFleeChance` | 9, 9, 9, 9, 9, **0** | One boss controller family (Dreeg's Eye). Bespoke. |
| `synergy*` | `synergyChaosBeam`, `synergyChargeTime`, `synergyNumBeams`, `synergyRadius`, `synergySearchIntervalMax`, `synergySearchIntervalMin`, `synergyTeamSize` | 3 each | `ControllerMonsterSynergy` — 2 records total in the whole database. |
| `spirit*` | `spiritTarget` | 1 | `ControllerSpirit`/`ControllerSpiritHost` — 2 records each. |
| pet-target policy | `petTargetGreatestHealth`, `petTargetLeastAttacked` | **0**, 1 | Present on 3,170 records, non-inert on ≤1. Uniformly disabled. |
| loot callbacks | `lootDropAttachPointName`, `lootDropCallbackPoint` | 3 | Not combat. |
| misc | `appearDistance` 5 · `pursueBehavior` 1 · `dyingSkillCallbackPoint` 1 · **`ClearAngerWhenFleeing` 1** | — | `ClearAngerWhenFleeing` is the sharpest case: **present on 3,207/3,207 (100%) and `True` on exactly 1.** A field the whole bestiary carries and nothing uses. |

**Re-entry condition for all 22** (annex precedent, never deleted): a future GD edition or a future
corpus kit raises the field's non-inert monster count to ≥1% of the combat-relevant population, OR
a GD-lane kit's resolution is shown to exercise it.

---

## 5. What the census overturns

**(a) `AlertBeforePursue` has a parameter binding, and it is dense.** The binary-inspection research
doc's open item #1 states that entry conditions for `AlertBeforePursue` "cannot be determined" without
disassembly, and gamora's audit §7 carries that forward as "F2's parameter binding cannot be specified
from what we have." The data answers half of it: **`EmoteBeforePursuingChance`** is present on
3,205/3,207 controllers and non-zero on **2,983 (93.0%)**, modal value 20, with a real spread
(20 / 15 / 0 / 10 / 25 / 30). The name is decisive — the RTTI class has a `HandleEvent` override, the
state sits at Table-3 index #40, and this is the only controller field whose name binds "emote" to
"before pursuing." Supporting: `alertAnimChance` (mode 30, then 100, zero on only 114 monsters),
`alertSoundChance` 100%, `alertSound` 3,152.
**Still not determined:** the *exit* condition and the anger threshold that terminates the state.
Entry probability ≠ transition rule. That half remains open and I do not infer it.

**(b) `Emote` should not be PROPOSED-OUT.** gamora's audit classes `Emote` as PROPOSED-OUT
("Cosmetic"). By attestation it is the **7th-densest** state in the table: `randomEmoteChance > 0`
on 2,309 (72.0%), with per-monster min/max timing on 2,777. More consequentially, it is not
separable from row 40 — the *same* GD vocabulary word ("Emote") appears in `EmoteBeforePursuingChance`,
which is the `AlertBeforePursue` gate. If `Emote` is ruled out, the telegraph parameter it shares a
name with becomes orphaned. **Recommend: `Emote` moves PROPOSED-OUT → IN, on the narrow ground that
its parameter is the pre-pursuit telegraph, with the cosmetic idle-emote half separable later.**

**(c) HP-threshold flee exists in GD data, named.** gamora F7's named delta is "an HP-threshold flee
trigger keyed on `fleeDistance`". The trigger is not keyed on `fleeDistance` — it is an enum value:
`FleeBehavior ∈ {NeverFlee, FleeOnLowHealth, FleeOnDamage, FleeWhenEnemyClose}`, with
**`FleeOnLowHealth` on 359 monsters (11.2%)**, `FleeOnDamage` 248 (7.7%), `FleeWhenEnemyClose` 59 (1.8%).
The HP *level* is monster-side: `lowHealthTriggerLevel` 316 (9.9%) + `lowHealthResetLevel` 306 (9.5%).
This is a 4-way behaviour enum plus a two-parameter hysteresis band, not a single threshold.

**(d) `WaitToAttack` is 100%-attested and has an exact numeric budget.** gamora row 29 records
"No attack-token, slot, or queue system" on the sim side and ABSENCE across five search terms. On the
GD side it is not merely present, it is **universal and quantized**: `numAttackSlots` on 3,207/3,207
with only 7 distinct values, bimodal at 4 (1,768) and 8 (1,401). `numDefenseSlots` mirrors it. This
is the single highest coverage-per-parameter item in the roster — one integer per monster.

**(e) `Dying` is a real interval state with a skill hook.** gamora row 11 correctly finds sim-side
death is one statement. GD-side, `Dying` carries `Skill_OnDeathSpawnActor` on **1,577 monsters
(49.2%)**, `dyingSkillName` on 700 (21.8%), `chanceToSpawnOnDeath` 1,308, `poolToSpawnOnDeath` 334,
plus `deathFromEnemyDelay` 141. Nearly half the bestiary *does something* during death. This is a
combat mechanism (on-death splits, corpse explosions, add-spawns), not an animation window.

**(f) `Confused` / `Scared` / `Taunt` are resistance-free by construction.** `defensiveConfusion`,
`defensiveFear`, `defensiveTaunt`, `defensiveConvert`, `defensiveDisruption` all appear in the
**schema vocabulary of all four archives' string tables** — and are carried by **0 of 3,207**
combat-relevant monsters. The offensive halves exist (`offensiveConfusion*` 9 player + 9 monster
skills; `offensiveFear*` 1 player skill; `offensiveTaunt*` 15 player + 2 monster skills). Reading:
these CCs land on every monster with **no resistance channel at all** — the opposite of Stun/Knockdown,
which have per-monster resist tuning on 28–56% of the bestiary. If this asymmetry is not modelled,
mental CC will be uniformly overpowered relative to physical CC.

**(g) `stunResistanceInc` is the cleanest OUT in the whole census.** Present on **3,207/3,207 (100%)**
and non-zero on **0**. A field every single monster carries and no monster uses. It is the exemplar
of why the filter is two-sided: presence-counting alone would have ranked it top-tier.

---

## 6. Per-family attestation density — build-queue prioritization input

Ordered by the density the dispatch asked for (a family carried by 60% of the bestiary outranks one
carried by 3 monsters). "Density" = the family's *representative* attestation, footnoted where the
family's members diverge.

| Rank | Family | Density | States covered | gamora status | Note |
|---|---|---|---|---|---|
| 1 | **F1 aggro onset / perception** | **100.0%** | `Pursue`, `AlertBeforePursue`, `Sleeping`, `Idle` | BLOCKED-MECHANISM | `ViewDistance`/`InnerViewDistance` on 100% of the bestiary. The single densest gap. |
| 2 | **F3 leash + return** | **99.9%** | `Return` | EXISTS + PARAMETER-FAITHFUL | Distance half done (+0.15%). The `PursuitTime` OR-branch is attested at 99.9% and unbuilt. |
| 3 | **F9 hit reaction** | **99.1%** | `TakeHit`, `GettingUp`, `Dying` | BLOCKED-MECHANISM (mob actor) | `hitThreshold` on 100% with 14 distinct values. Higher density than the audit's framing implies. |
| 4 | **F2 anger / pre-commitment** | **99.5%** (anger) / **93.0%** (`EmoteBeforePursuingChance`) | `AlertBeforePursue` | BLOCKED-MECHANISM — "cheapest of the nine" | Now has a named parameter. |
| 5 | **F5 distress + pack** | **94.9%** | `FollowLeader`, `DefendLeader` | BLOCKED-MECHANISM | `ChanceToRespondToDistressCall` 94.9%; `distressCallRange` 99.8% monster-side; `LeadChance` 51.1%. |
| 6 | **F6 combat spacing** | **100.0%** (`numAttackSlots`) / 50.1% (`enemyTooClose`) / 45.2% (dodge) / 12.0% (`Charge`) / 6.0% (`JumpAttack`) | `WaitToAttack`, `RepositionForAttack`, `DodgeAttack`, `Charge`, `JumpAttack` | BLOCKED-MECHANISM | **Widest internal spread of any family.** `WaitToAttack` is universal; `JumpAttack` is 6%. Should be split for sequencing. |
| 7 | **F4 idle loop** | **95.9%** (`MaxTimeBeforeRoam`) / 80.2% (`RoamBehavior`) / 23.9% (`WanderDistance`) | `Roam`, `Wander`, `WanderPause`, `Idle`, `Patrol` | BLOCKED-MECHANISM (downstream of F1) | Roam is dense; Wander is not; Patrol is NEEDS-JOIN. |
| 8 | **F8 hard-CC / status lock** | **56.4%** (`KnockedDown`) → 28.3% (`Stunned`) → 27.9% (`Sleeping`) → 22.7% (`Trapped`) → 19.4% (`Freeze`) → 17.7% (`Petrify`) → 0% resist (`Confused`) | 6 states | BLOCKED-CONSUMER — "highest coverage-per-line" | See §7 divergence: the sim's ailment registry and GD's CC channel set do not line up. |
| 9 | **L2 monster support** | **96.9%** policy / **4.8%** skill | `UseSkillOnAlly`, `UseSkillOnPoint` | BLOCKED-MECHANISM | `UseSkillOnPoint` is 92.8% and belongs several rungs higher than `UseSkillOnAlly` (4.8%, and solo-scope-blocked). **Split recommended.** |
| 10 | **F7 fear granularity** | **20.8%** | `Flee`, `Panic`, `Scared` | PARTIAL | Lowest-density behavioural family. `Panic` OUT; `Scared` rests on 1 skill. |
| 11 | **L1 pathing recovery** | **100.0%** substrate / **6.5%** obstacle-specific | `NavigateObstacle` | BLOCKED-MECHANISM — "lowest priority" | Confirmed lowest: `useBoundingBoxesForDynamicObstacles` 210 monsters, `pathingViewDistance` 148. |

**Metric families (monster stats), same axis:**

| Family | Density | Verdict |
|---|---|---|
| Physicality / collision (`actorHeight`, `actorRadius`, `pathMass`, `pathingSize`, `physicsMass`, `avoidForce`) | 99.2–100% | IN |
| Range bands (`short/medium/longRangeMin/Max`) | 100% (`Max`), 57.8–96.1% (`Min`) | IN — `shortRangeMin` non-inert on only 31 (1.0%), borderline |
| Speeds (`characterRunSpeed` 99.2%, `characterAttackSpeed` 99.6%, `characterSpellCastSpeed` 99.9%, `walkSpeed` 98.0%) | ~99% | IN |
| Threat / distress (`distressCall*`, `angerMultiplier`, `hitThreshold`, `numAttackSlots`) | 99.1–100% | IN |
| Special-attack slots | slot 1 86.7% → 2 70.2% → 3 50.9% → 4 29.7% → 5 13.6% → **6 0.5% → 7 0.1%** | **IN slots 1–5; slots 6–7 OUT-BY-ATTESTATION** (16 and 4 monsters) |
| Damage-resist channels | `Pierce` 50.0% · `Physical` 42.5% · `Life` 40.8% · `Cold` 34.6% · `Fire` 34.1% · `Lightning` 29.9% · `Aether` 26.2% · `Poison` 25.1% · `Chaos` 22.0% | IN (all 9) |
| Resist channels in schema but on 0 monsters | `defensiveBleeding`, `defensiveElementalResistance`, `defensiveAbsorption`, `defensiveBlockModifier`, `defensiveProtection` | **OUT-BY-ATTESTATION** |
| **OA / DA / Life** | present 97.8–99.5%, **non-inert 0.0–0.2%** | **NEEDS-JOIN — see §7.3** |
| Low-health trigger | `lowHealthTriggerLevel` 7.8%, `lowHealthResetLevel` 7.5%, `berserkSkillName` 1 monster | IN (first two); `berserkSkillName` OUT |
| Death / lifecycle | `gibThreshold` 92.9% · `deleteBehavior` 97.9% · `dyingSkillName` 21.8% · `onDie` 11.9% · `deathFromEnemyDelay` **0.2%** · `lifeTime` **0.1%** | IN except `deathFromEnemyDelay` / `lifeTime` / `deathFromEnemyRange` (0.2%) → **OUT** |

---

## 7. Divergence flags and NEEDS-JOIN list

### 7.1 `.arz` vs grimtools — the corroborating source cannot see the AI lane at all

| Check | `.arz` (governs) | grimtools (corroborates) | Verdict |
|---|---|---|---|
| Monster population | 4,066 records / 3,207 combat-relevant | 2,636 entries by regex count | **DIVERGENCE, unresolved.** Also an internal one: MANIFEST claims 2,716; my count is 2,636 (−80). I do not resolve either; both are flagged. |
| `controller` field | present on 3,825/3,825 non-sandbox | **ABSENT** | **STRUCTURAL.** grimtools has no controller reference. |
| `ViewDistance`, `MaxPursuitDistance`, `PursuitTime`, `SightAngerRate`, `FleeBehavior`, `RoamDistance`, `WanderDistance`, `DodgeChance`, `RepositionChance`, `ChanceToRespondToDistressCall`, `EmoteBeforePursuingChance` | all present | **ALL ABSENT** | **STRUCTURAL: the entire 40-state / TSF6-spatial lane is un-corroboratable from grimtools. `.arz` is sole source.** |
| `hitThreshold`, `walkSpeed`, `stunResistanceInc`, `lowHealthTriggerLevel`, `characterOffensiveAbility`, `characterDefensiveAbility` | present | ABSENT | grimtools drops them (derived at render time). |
| `defensiveKnockdown` | 1,810 non-zero of 3,207 (56.4%) | 1,419 of 2,636 (53.8%) | **CONSISTENT** |
| `defensiveStun` | 906 (28.3%) | 728 (27.6%) | **CONSISTENT** |
| `defensiveSleep` | 894 (27.9%) | 768 (29.1%) | **CONSISTENT** |
| `defensiveTrap` | 728 (22.7%) | 612 (23.2%) | **CONSISTENT** |
| `defensiveFreeze` | 622 (19.4%) | 542 (20.6%) | **CONSISTENT** |
| `defensivePetrify` | 567 (17.7%) | 500 (19.0%) | **CONSISTENT** |

**Reading:** on the six CC-resist channels the two sources agree in both rank-order and rate to
within ~1.3 percentage points across a 571-monster population difference. That is a genuine positive
corroboration of the CC census. On the behavioural/AI lane grimtools cannot corroborate anything —
which means **every controller-state finding in this document rests on a single source**, and the
usual two-source safety net does not exist there. Flagged, not worked around.

### 7.2 TSF6 cited values vs the population — four divergences

TSF6 Track-A calibrated against specific parameter values. Four of the eight are not the population
modal value; two of those are not even close.

| Parameter | TSF6 cited | Population mode | Share of monsters @ cited | Median | Verdict |
|---|---|---|---|---|---|
| `ViewDistance` | 15.0 | 15.0 | **76.5%** | 15.0 | ✅ representative |
| `InnerViewDistance` | 4.0 | 4.0 | **93.5%** | 4.0 | ✅ representative |
| `MaxPursuitDistance` | 75.0 | 75.0 | **87.1%** | 75.0 | ✅ representative |
| `PursuitTime` | 10000 | 10000 | **95.8%** | 10000 | ✅ representative |
| `SightAngerRate` | 3.0 | **5.0** | **6.7%** | 5.0 | ⚠️ **DIVERGENCE** |
| `InnerSightAngerRate` | 12.0 | **10.0** | **6.0%** | 10.0 | ⚠️ **DIVERGENCE** |
| `fleeDistance` | 16.0 | **0.0** | **7.0%** | 8.0 | ⚠️ **DIVERGENCE** |
| `WanderDistance` | 4.0 | **0.0** | **3.5%** | 0.0 | ⚠️ **DIVERGENCE** — 76.1% of the bestiary has `WanderDistance = 0` |
| `distressCallRange` (monster) | 16.0 | **18.0** | **5.9%** | 18.0 | ⚠️ **DIVERGENCE** |

**The 4× anger ratio claim.** gamora F2 records `SightAngerRate` 3.0 / `InnerSightAngerRate` 12.0 as
a "4× ratio" and builds the inner/outer zoning argument on it. The population ratio distribution:

| ratio | monsters |
|---|---|
| **2.0×** | **1,820 (56.7%)** |
| 2.5× | 321 |
| 0.89× | 312 |
| 1.6× | 311 |
| 1.67× | 114 |
| **4.0×** | **97 (3.0%)** |
| 3.0× | 60 |

The 4× ratio is real but rare (3.0%). The population ratio is **2×**. The *structure* of the claim
(inner zone angers faster) survives — 88% of monsters have ratio > 1 — but the *magnitude* does not.
**This is a calibration-target correction, not a mechanism finding.** Anyone pricing F2 off "4×"
should re-price off 2×.

### 7.3 NEEDS-JOIN list — six items I will not infer

| # | Item | What is missing | Cheapest refuting/resolving test |
|---|---|---|---|
| J1 | **`WanderPause` parameter binding** (state #9) | No field carries the name. `Min/MaxPatrolIdleTime` and `Min/MaxTimeBeforeRoam` are both candidates; nothing in the records discriminates | Disassemble `OnBegin@ControllerMonsterStateWanderPause`, or live measurement per the playtest-capture instrument |
| J2 | **`Patrol` reachability** (state #30) | Parameters configured on 1,830 monsters (57.1%) but only **4 `PatrolPoint` records exist in the entire database**. Either patrol paths are authored in level `.lvl`/`.map` data outside the `.arz`, or the parameters are vestigial | Grep the `.arc`/level resources for patrol-path attachment; count monsters actually bound to a patrol path |
| J3 | **`KnockedDown` player-side (P)** (state #25) | 11 player-class skill records carry `offensiveKnockdown*`. Whether any of the 41 GD-lane kits' skills is among those 11 requires a kit→`.arz`-record join that does not exist. `exact_skill`/`exact_skill_field` carry exactly one kit (`gd-flames-of-ignaffar-purifier`, the GD-SLICE width-one proof) | Extend the GD adapter from width 1 to the 41-kit roster; then the join is a SQL query, not an inference |
| J4 | **OA / DA / Life metric family** | `characterOffensiveAbility` / `characterDefensiveAbility` / `characterLife` are present on ~98–99.5% of monsters and **non-inert on 0.0–0.2%**. The real values live in **720 distinct `characterAttributeEquations` bio records as formula strings** keyed on `charLevel` — e.g. `bio_hero_standard_01` (618 monsters): `characterOffensiveAbility = '(charLevel*7)+92'`, `characterLife = '((charLevel*18)^1.50)-20'`. The monster-record fields are additive overrides, not values | Build a `charLevel` expression evaluator (MANIFEST gap #3 names the same need). Until then **no absolute OA/DA/HP number for any GD monster is derivable from holdings** |
| J5 | **Pet-lane parameters** (4 fields, 41–99% attestation) | `ignorePetsChance`, `ignorePetsInterval`, `petAngerTransference`, `petTargetLevelRange` govern monster↔player-pet interaction. In-scope only once the engine has a pet actor. `gd-pet-conjurer` exists as a kit but the engine-side pet lane is a separate question | Gandalf/Matt scope call, not a data question |
| J6 | **`.tpl` template defaults** | "Non-default" is operationalized as "non-inert" (§2.2) because the `.tpl` files live in `.arc` bundles not parsed by this pass. A field whose template default is non-zero would be under-counted by my rule | Parse `database/templates/controllermonster.tpl` + `monster.tpl` from the `.arc` resource bundles |

**The D-b caveat, resolved in one direction only.** The dispatch instructs that the
parameter↔creature join at width > 1 is inference and must be flagged rather than resolved. It is
not inference in the `.arz` lane: **every non-sandbox `Monster` record carries an explicit
`controller` string field, and all 3,207 combat-relevant monsters resolve to an indexed
`Controller*` record — 0 unresolved.** The join is a direct foreign key, verified by resolution, not
by pattern-matching. (312 of 3,494 pre-filter monsters pointed at `ControllerStationaryMonster` /
`ControllerMonsterHidden` rather than `ControllerMonster`; once those four sibling classes are in
the index, resolution is total.) **D-b is retired for the `.arz` lane. It remains fully in force for
grimtools, which carries no controller field** — so any claim sourced from grimtools about which
monster has which AI parameter is still inference and is not made here.

**Incidental confirmation:** the 6 `ControllerMonsterHidden` records in the database independently
corroborate the `ControllerMonsterStateHidden` RTTI class the binary inspection found *without* a
Table-3 string entry (research doc §"RTTI State Class Count vs String Table Count"). Data lane and
binary lane agree.

---

## 8. Proposed G1-B scope roster (IN-list) — for Matt's ratification

### 8.1 States: 33 IN

**IN (both P and M) — 11.** Attested on both sides; highest confidence.
`Attack` · `Pursue` · `RepositionForAttack` · `JumpAttack` · `Dead` · `Charge` · `Move` · `Immobile` ·
`Stunned` · `TakeHit` · `UseSkillOnPoint`

**IN (M only) — 22.** Monster-attested; no GD-lane kit exercises them (expected — the corpus is
player builds, and most of these are monster-behaviour states with no player analogue).
`Idle` · `Startup` · `Roam` · `Flee` · `Wander` · `Dying` · `Return` · `FollowLeader` ·
`NavigateObstacle` · `DefendLeader` · `DodgeAttack` · `Confused` · `Paralyze` · `Trapped` ·
`KnockedDown` · `Scared` · `Sleeping` · `WaitToAttack` · `GettingUp` · `UseSkillOnAlly` · `Emote` ·
`AlertBeforePursue`

### 8.2 States: 5 OUT-BY-ATTESTATION

| State | Re-entry condition |
|---|---|
| `Panic` | Any GD edition ships a controller or monster field, or an offensive/defensive skill channel, that names panic distinctly from `Flee`/`Scared` |
| `QuestWalk` | Any combat-relevant monster record ships `quest = True`, or a controller-state binding to `questFile*` is demonstrated |
| `QuestMove` | as above |
| `QuestUseSkill` | as above |
| `QuestPlayAnimation` | as above |

### 8.3 States: 2 NEEDS-JOIN — Matt ruling deferred pending J1/J2

`WanderPause` (no parameter binding discoverable from records) · `Patrol` (parameters on 57.1% of
monsters, 4 path records in the database — leans OUT but the evidence is contradictory, and I will
not resolve a contradiction by picking the side I prefer)

### 8.4 Parameters: 62 IN / 22 OUT (of 84 behavioural)

Per §4. The 22 OUT are `eye*` (6: `eyeDodgeChance`, `eyeLeadChance`, `eyeRandomRepositionChance`,
`eyeTimeMax`, `eyeTimeMin`, `eyeFleeChance`), `synergy*` (7), `spiritTarget`,
`petTargetGreatestHealth`, `petTargetLeastAttacked`, `lootDropAttachPointName`,
`lootDropCallbackPoint`, `appearDistance`, `pursueBehavior`, `dyingSkillCallbackPoint`,
`ClearAngerWhenFleeing`.
Re-entry condition: non-inert monster count reaches ≥1% of the combat-relevant population, or a
GD-lane kit's resolution exercises it.

### 8.5 Metric families: OUT list

`stunResistanceInc` · `defensiveBleeding` · `defensiveElementalResistance` · `defensiveAbsorption` ·
`defensiveBlockModifier` · `defensiveProtection` · `specialAttack6*` · `specialAttack7*` ·
`deathFromEnemyDelay` · `deathFromEnemyRange` · `lifeTime` · `berserkSkillName` ·
`characterAttackSpeedModifier` · `characterSpellCastSpeedModifier` · `characterRunSpeedModifier` ·
`physicsRestitution` · `dbIgnoreWhenPathing` · `useBoundingBoxesForDynamicObstacles`
(the last four are present on 100%/6.5% and non-inert on 0)

### 8.6 Two sequencing recommendations, offered not ruled

1. **Split F6.** `WaitToAttack` (100.0%) and `JumpAttack` (6.0%) are 94 points apart inside one
   family. Treating F6 as a unit prices the whole family off its weakest member.
2. **Split L2.** `UseSkillOnPoint` (92.8%, and P-attested by 4 kits) is a top-quartile item;
   `UseSkillOnAlly` (4.8% skill-side, and blocked by the solo-scope boundary already Matt-ratified
   at `mechanic_gap_docket` #2) is a bottom-quartile one.

---

## 9. Provenance ledger

**VERIFIED (read the data, counts reproducible via the §0 script):** every count in §§2–6 and §7.1–7.2.
All `.arz` counts are over Edition-II (`grim-dawn-edition-II-20260724`), four archives, merged with
later-archive-wins ordering. All corpus.db counts are read-only SELECTs.

**COUNTED BY REGEX, not by parse:** the grimtools entry count (2,636). `all_monsters.js` is a JS
object literal with unquoted keys and is not JSON-parseable; I counted `[{,](m\d+):\{` occurrences.
This is why the MANIFEST's 2,716 and my 2,636 are both reported rather than one being corrected.

**INFERENCE — three, labelled, none banked as verdict:**
1. §5(a): that `EmoteBeforePursuingChance` is the `AlertBeforePursue` *entry* gate. The binding is
   from field-name semantics + 93.0% density + Table-3 adjacency, **not** from disassembly. The
   research doc's own open item #1 remains open on the exit condition. If disassembly shows the field
   drives a cosmetic pre-pursuit emote rather than the state, row 40's evidence cell should be
   re-sourced onto the anger stack (`SightAngerRate`/`AngerTolerance`, both ≥99.5%) — the **verdict**
   (IN(M)) would not change, only the binding.
2. §3 row 21/27: that `defensiveConfusion == 0` on all monsters means "no resistance channel" rather
   than "resistance handled elsewhere". Falsifiable by finding a confusion-resist path in the
   `characterAttributeEquations` bio records or the racial-profile tables.
3. §6 family densities: the choice of *representative* field per family is a judgment. Where family
   members diverge (F6 spans 6.0%–100.0%, F4 spans 23.9%–95.9%) I have reported the spread rather
   than a single number, so the judgment is inspectable.

**Not established — carried forward, not silently closed:** J1–J6 in §7.3. In particular **no
absolute HP, OA, or DA figure for any GD monster is derivable from current holdings** (J4) — the
MANIFEST named this as gap #1 and this census confirms it at the record level: the fields exist,
are populated on ~98% of monsters, and are **zero**.

**Not done, by scope:** no schema was designed, no DDL authored, no `MIGRATION.md` entry written, no
row written to corpus.db. Per the dispatch this is analysis only.

---

**Signed:** elrond, 2026-07-25. Substrate votes; scope follows attestation. Findings only —
read-only across every source, no schema changes, no production code.
