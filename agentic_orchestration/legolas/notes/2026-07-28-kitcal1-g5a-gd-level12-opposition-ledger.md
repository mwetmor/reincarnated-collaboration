# KIT-CAL-1 G-5a — GD level-12 opposition ledger (Act 1, Normal, 1 player)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-28 · **Work-package:** G-5a
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` (conductor: gandalf)
**Class:** evidentiary — measured extraction from primary source
**Mode:** read-only. No writes outside `legolas/notes/` + `legolas/scratch/2026-07-28-kitcal1-g5a/`.

## Provenance

| Archive | SHA-256 | records |
|---|---|---|
| `database/database.arz` | `8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f` | 34,114 |
| `gdx1/database/GDX1.arz` | `e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539` | 18,447 |
| `gdx2/database/GDX2.arz` | `f6d5bd67602ce5af2de394507c36f198a9388be26350517434e7ff5e4ee1e985` | 16,451 |
| `gdx3/database/GDX3.arz` | `1661be5ef6db1f0805cba4929d7d50bf13cbdc983c1b4413f6016a5ef330dcf0` | 24,178 |

Corpus root `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`. Display names bridged from
`*/resources/Text_EN.arc` (20,394 tags loaded) per the 2026-07-26 displayname-bridge lane.

Tooling: `legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py` — imports gandalf's G-4 wrapper,
which imports legolas's `research/scripts/gd_arz_adapter_2026_07_24.py` `ArzArchive`. Nothing rebuilt.

**Grading key:** **M** = MEASURED (field read verbatim from `.arz`) · **D** = DERIVED (computed by
evaluating source equations/arrays; composition operator stated) · **U** = UNRESOLVED.

---

## 1. The level-scaling mechanism (all M unless noted)

GD monsters carry **no concrete HP or damage numbers**. Every stat is resolved at spawn time from
five chained records. The chain, exactly:

```
proxy (records/proxies/area001/*.dbr)
  → pool (records/proxies/pools/p_*.dbr)          spawnMin/Max, championChance, nameN/weightN
      → levelVarianceEquationN (records/proxies/lvN_*.dbr)   spawnLevel = f(averagePlayerLevel)
  → monster (records/creatures/enemies/**.dbr)
      .charLevel                     "charLevel*1"  → effective charLevel = f(spawnLevel)
      .characterAttributeEquations   → records/creatures/enemies/bios/bio_*.dbr
      .skillNameN + .skillLevelN     → records/skills/nonplayerskills/passive/*.dbr (rank-indexed arrays)
  → records/game/gameengine.dbr .monsterAttributePak
      → records/game/balancingadjustment_mp+difficulty_enemies01.dbr   [difficulty x players]
  → records/game/combatformulas.dbr   OA/DA/damage equations
```

### 1a. Spawn level from player level (M)

`records/proxies/lvN_*.dbr`, field `minVarianceEquationNormal` / `maxVarianceEquationNormal`.
Resolved at **averagePlayerLevel = 12**:

| Record | min eq | max eq | spawn level @ pL12 |
|---|---|---|---|
| `lv1_weak.dbr`, `lv1_weak+.dbr` | `(averagePlayerLevel-1)` | `(averagePlayerLevel-1)` | 11 |
| `lv2_normal.dbr`, `lv2_normal+.dbr` | `(averagePlayerLevel-1)` | `(averagePlayerLevel)` | 11–12 |
| `lv3_strong.dbr` | `(averagePlayerLevel)` | `(aPL)+(aPL/75)` | 12 |
| `lv3_strong+.dbr` | `(averagePlayerLevel)` | `(aPL+1)+(aPL/90)` | 12–13 |
| `lv4_champion.dbr` | `(averagePlayerLevel+1)` | `(aPL+1)+(aPL/75)` | 13 |
| `lv5_elitechampion.dbr` | `(aPL+2)` | `(aPL+1)+(aPL/50)` | 14 (**min>max — source quirk**) |
| `lv6_hero.dbr` | `(aPL+2)+(aPL/50)` | `(aPL+3)+(aPL/50)` | 14–15 |
| `lv7_uber hero.dbr` | `(aPL+3)` | `(aPL+3)+(aPL/50)` | 15 |
| `lv8_boss.dbr` | `(aPL+3)+(aPL/50)` | `(aPL+4)+(aPL/50)` | 15–16 |

Area cap: `records/proxies/limit_area001.dbr` → `minPlayerLevelEquationNormal=1`,
`maxPlayerLevelEquationNormal=200`. **Act 1 is uncapped on Normal** — monster level tracks the
player 1:1 with the offsets above. (`limit_area002` starts at 8, `limit_area003` at 12 — Act
gating is by *minimum* player level only.)

### 1b. Spawn level → creature charLevel (M)

The monster record's own `charLevel` field is a second remap. It is **not** always identity:

| record | `charLevel` | @ spawn 12 / 15 |
|---|---|---|
| `zombie_a01`, `boar_a01`, `boar_h01`, `humanoutlaw_melee_a01` | `charLevel*1` | 12 / 15 |
| `zombiemutated_a01` (champion) | `charLevel*1+1` | 13 |
| `zombie_soldiera01` | (+1) | 13 |
| `hero/zombie_h01`, `hero/rifthound_h01` | `charLevel*1+5` | 20 |
| `boss&quest/warden01`, `warden02` | `(charLevel*1.1)+2` | 18 (from spawn 15) |

This is the single easiest thing to get wrong: **Warden Krieg's stat block is resolved at charLevel
18, not 15, when the player is level 12.**

### 1c. Base attributes (M for equations, D for values)

`records/creatures/enemies/bios/bio_*.dbr`, e.g. `bio_zombie_01.dbr`:

```
characterLife             = ((charLevel*4)^1.33)+24
characterMana             = ((charLevel*8)^1.22)+100
characterStrength         = (charLevel*4.5)+10
characterDexterity        = (charLevel*6.5)+10
characterIntelligence     = (charLevel*6)+15
characterOffensiveAbility = (charLevel*6)+5
characterDefensiveAbility = (charLevel*3)+25
```

336 bio records exist (one per creature family/tier). At charLevel 12:
`characterLife = (48^1.33)+24 = 172.21+24 = **196.21**`.

### 1d. Rank-indexed passive tables (M)

`skillNameN` + `skillLevelN` on the monster; the skill level equation is evaluated in `charLevel`
and **truncated to int** (D — truncation vs round is not stated in source; at the ranks involved
the difference is ≤1 rank). Only records with `Class = Skill_Passive` modify the creature's own
stat block; `Skill_Attack*` / `Skill_Buff*` are separately-triggered abilities (see §3).

Two families carry essentially all of it:

**`records/skills/nonplayerskills/passive/damagebase_physical0N.dbr`** — base unarmed attack
(`unarmedOnly = True` on 01). `FileDescription` states the tier explicitly. Rank-12 slice of the
200-element `offensivePhysicalMin`/`Max` arrays:

| record | FileDescription | @rank 12 | @rank 50 |
|---|---|---|---|
| `damagebase_physical01` | Default Phys Dmg for Normal Enemies | 65 – 80 | 285 – 315 |
| `damagebase_physical02` | …Strong Enemies and Champions | 70 – 82 | 290 – 358 |
| `damagebase_physical03` | …Champions and Heroes | 76 – 88 | 299 – 396 |
| `damagebase_physical04` | …Heroes and Bosses | 96 – 121 | 416 – 538 |
| `damagebase_physical05` | …Elite Heroes and Bosses | 109 – 141 | 486 – 631 |
| `damagebase_physical06` | …Uber Bosses | 110 – 147 | 509 – 675 |
| `damagebonus_physical01` | Phys Dmg **Bonus** for Weapon-Wielding Enemies | 52 – 64 | 228 – 252 |
| `damagebonus_physical03` | …Weapon-Wielding Heroes | 59 – 74 | 269 – 343 |

All also carry `offensivePhysicalModifier = 35` (20 on tier 03+) with
`offensivePhysicalModifierChance = 8` — an 8 %-of-hits +35 % physical spike, **not** folded into the
figures below.

**`records/skills/nonplayerskills/passive/armorbase0N.dbr`** — armor tier **and** the low-level
damper. Critically, 01/02 and 03–06 share *identical* `offensiveTotalDamageModifier` and
`characterLifeModifier` curves within their group; only `defensiveProtection` differs:

| record | FileDescription | TDM r1→r12→r15→r50→r100 | lifeMod r1→r19→r50 | armor r12 |
|---|---|---|---|---|
| `armorbase01` | Damage Reduced Levels 8-18 | −55 → −44 → −41 → −6 → +30 | −58 → −58 → −4 | 4 |
| `armorbase02` | Damage Reduced Levels 8-18 | (identical to 01) | (identical) | 9 |
| `armorbase03` | Damage Reduced Levels 1-20 | −90 → −79 → −76 → −41 → +25 | −71 → −71 → −4 | 21 |
| `armorbase04` | Damage Reduced Levels 1-20 | (identical to 03) | (identical) | 39 |
| `armorbase05` | **For Bosses** — Dmg Reduced Lv 1-20 | (identical to 03) | (identical) | 65 |
| `armorbase06` | **For Bosses** — Dmg Reduced Lv 1-20 | (identical to 03) | (identical) | 98 |

**`records/skills/nonplayerskills/passive/damage_totaladjuster.dbr`** — 25-element
`offensiveTotalDamageModifier` = +4/rank. Ranked by e.g. `charLevel/30`, so it is **rank 0 (inert)
for most level-12 trash** and rank 1–2 for champions/bosses.

### 1e. Global difficulty × multiplayer pak (M)

`records/game/gameengine.dbr` → `monsterAttributePak = records/game/balancingadjustment_mp+difficulty_enemies01.dbr`.
Its arrays are 12 elements = **3 difficulties × 4 player counts**; index = `difficulty*4 + (players−1)`.
Proven by `characterLifeMultModifier = [0,90,180,270, 0,90,180,270, 0,90,180,270]` (players cycling
inside each difficulty block) against `characterLifeModifier = [50×4, 320×4, 580×4]`
(Normal / Elite / Ultimate). **Normal, 1 player = index 0:**

| field | Normal/1P | Elite/1P | Ultimate/1P |
|---|---|---|---|
| `characterLifeModifier` | **+50 %** | +320 % | +580 % |
| `characterLifeMultModifier` | **0 %** | 0 % | 0 % |
| `offensiveTotalDamageModifier` | **−25 %** | +25 % | +40 % |
| `characterOffensiveAbility` / `…Modifier` | **0 / −12 %** | +40 / −8 % | +50 / −8 % |
| `characterDefensiveAbility` / `…Modifier` | **+35 / −15 %** | +60 / −8 % | +75 / −8 % |
| `characterAttackSpeedModifier` | **−10 %** | 0 % | 0 % |
| `characterRunSpeedModifier` | **−18 %** | −18 % | −18 % |
| `characterStr/Dex/IntModifier` | **−5 %** | +4…+5 % | +5…+10 % |
| `defensiveAbsorptionModifier` | **−20 %** | −20 % | −20 % |
| all elemental `defensive*` | **0** | +2…+13 | +5…+19 |
| `retaliationTotalDamageModifier` | **−66 %** | −30 % | −15 % |

Also `gameengine.monsterLevelGapFixer = [0, 5, 7]` — a per-difficulty level bump; **0 on Normal**.
`gameengine.armorDefensiveAbsorption = 70.0`; `monsterDefenseCap = [100,100,100]`.

### 1f. Composition — and one falsified hypothesis (D, load-bearing)

HP: `hp = (bioLife + flatLife) × (1 + Σ skillLifeMod/100) × (1 + pakLifeMult/100)`, with the pak's
`characterLifeModifier` summed into the skill pool. For `zombie_a01` @ charLevel 12:

```
196.21 × (1 + (−58 + 50)/100) × (1 + 0/100) = 196.21 × 0.92 = 180.5 HP
```

Damage: **the naive "sum all `offensiveTotalDamageModifier` sources" reading is FALSIFIED by the
source itself.** `zombiemutated_a01` at its own spawn level uses `armorbase03` (rank 14 → −78) with
no positive offset; additive composition with the pak's −25 gives **−103 %, i.e. negative damage**,
which is impossible. `warden01` gives −97 % (≈0 damage for the Act-1 boss). Therefore the pak's TDM
must be a **separate multiplicative stage**:

```
tdmMult = (1 + Σ_skillPassive TDM / 100) × (1 + pakTDM / 100)
dmg     = Σ offensivePhysicalMin/Max × tdmMult × ((dexterity/245) + 1)
```

The trailing dexterity term is `combatformulas.dbr .physicalDamageEquation =
physicalDamageDV*((dexterityDV/245)+1)`, applied with the pak's −5 % Dex.
**Graded D. The operator is inferred by contradiction, not stated in source** — see §6.

OA/DA use `combatformulas.dbr` verbatim:
```
offensiveAbilityEquation = (OA + (charLevel*12) + ((dex+bonus)*0.5)) * (1 + OAmod/100) + 53
defensiveAbilityEquation = (DA + (charLevel*12) + ((str+bonus)*0.5)) * (1 + DAmod/100) + 53
```

Worked example, `zombie_a01` @ charLevel 12, Normal/1P:

| step | value |
|---|---|
| `damagebase_physical01` rank 12 | 65 – 80 |
| `armorbase01` rank 12 TDM | −44 % |
| `damage_totaladjuster` rank `12/30`→0 | inert |
| pak TDM | −25 % |
| `tdmMult` | 0.56 × 0.75 = **0.42** |
| dex = (12×6.5+10) × 0.95 | 83.6 → ×(83.6/245+1) = **1.341** |
| **damage per hit** | 65×0.42×1.341 – 80×0.42×1.341 = **36.6 – 45.1** |

---

## 2. Level-12 opposition ledger — Act 1, Normal, 1 player

Player level 12. `spawn` = proxy-pool level; `charL` = post-remap creature level. HP, dmg, armor,
OA, DA all **D** (computed from the M records above). `aspd`/`run` are the record's
`characterAttackSpeed`/`characterRunSpeed` after the pak's −10 %/−18 % (D).
Flags: **W** = wields a randomly-rolled weapon (see §6-b) · **C** = damage max clamped to min
(a passive adds flat `offensivePhysicalMin` with no `Max`).

### Trash (Common)

| name | record | spawn | charL | HP | dmg/hit | armor | OA | DA | aspd | run | non-phys | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Walking Dead | `zombie_a01` | 11 | 11 | 163 | 33–41 | 3 | 255 | 268 | 1.06 | 0.82 | — | |
| Walking Dead | `zombie_a01` | 12 | 12 | 181 | 37–45 | 4 | 274 | 283 | 1.06 | 0.82 | — | |
| Wretcher | `zombie_b02h` | 12 | 12 | 181 | 42–52 | 9 | 274 | 283 | 0.94 | 0.90 | — | |
| Plague Walker | `zombie_g01` | 12 | 12 | 181 | 37–45 | 9 | 274 | 283 | 0.94 | 0.82 | — | |
| Rotting Soldier | `zombie_soldiera01` | 12 | 13 | 702 | 38–48 | 10 | 354 | 329 | 1.03 | 0.74 | — | W |
| Tainted Hound | `zombiehound_a01` | 12 | 12 | 493 | 40–49 | 9 | 292 | 299 | 1.12 | 1.07 | Aether 8.8–10.1, Pierce 2.1 | |
| Corruption (gazer) | `gazer_a01` | 12 | 12 | 222 | 36–45 | 4 | 281 | 266 | 1.08 | 1.07 | — | |
| Ghoul | `ghoul_a01` | 12 | 14 | 599 | 42–56 | 5 | 323 | 308 | 0.90 | 0.82 | — | |
| Stonetusk (boar) | `boar_a01` | 12 | 12 | 352 | 63 flat | 9 | 296 | 285 | 0.90 | 0.74 | — | C |
| Gargantuan Stonetusk | `boar_a02` | 12 | 12 | 821 | 33 flat | 21 | 315 | 313 | 0.90 | 0.70 | — | C |
| Scavenger | `scavenger_a01` | 12 | 12 | 430 | 41–48 | 9 | 289 | 271 | 0.90 | 0.90 | Pierce 4.6 | |
| Rifthound | `rifthound_swamp_a01` | 12 | 12 | 226 | 39–49 | 4 | 292 | 277 | 0.99 | 0.94 | — | |
| Cronley's Lackey | `humanoutlaw_melee_a01` | 12 | 12 | 447 | 29–36 + wpn | 4 | 293 | 272 | 0.77 | 0.54 | — | W |
| Cronley's Gunman | `humanoutlaw_ranged_a01` | 12 | 12 | 447 | 15–18 + wpn | 4 | 293 | 272 | 0.77 | 0.54 | Pierce 17.6 | W |
| Bloodsworn Adulant | `humanchthonic_cultist_a01` | 12 | 12 | 617 | 31–39 + wpn | 9 | 321 | 285 | 0.68 | 0.54 | — | W |
| Scrapheap Rift Scourge | `prawn_a01` | 12 | 12 | 200 | 37–46 | 9 | 286 | 269 | 0.90 | 0.82 | Pierce 4.2 | |
| Dreadweave Arachnid | `spidergianta_a01` | 12 | 12 | 232 | 37–46 | 9 | 284 | 268 | 1.03 | **1.64** | Poison 12.2 | |
| Boneback Gnasher | `bonerat_meleea01` | 12 | 12 | 232 | 42–52 | 9 | 289 | 274 | 0.99 | 1.03 | — | |
| Skeletal Warrior | `skeleton_a01` | 12 | 12 | 223 | 33–40 + wpn | 4 | 310 | 292 | 1.08 | 0.98 | — | W |

### Champion / Hero / Boss

| name | record | spawn | charL | HP | dmg/hit | armor | OA | DA | aspd | run | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Fleshwarped Butcher | `zombiemutated_a01` | 13 | 14 | 923 | 23–24 | 25 | 406 | 346 | 1.17 | 1.03 | |
| Fury | `zombie_c01` | 13 | 14 | 676 | 58–76 | 11 | 367 | 337 | 1.35 | 0.82 | Life 25.5 |
| Ironhide Stonetusk | `boar_b01` | 13 | 13 | 1,326 | 34 flat | 43 | 366 | 350 | 0.90 | 0.61 | C |
| **Dreadtusk, the Hunter's Bane** (hero) | `hero/boar_h01` | 15 | 15 | 4,097 | 42 flat | 52 | 444 | 386 | 0.90 | 0.53 | C |
| **Abner, the Forsaken One** (hero) | `hero/zombie_h01` | 15 | **20** | 6,712 | 34–45 | 40 | 545 | 479 | 1.26 | 1.31 | |
| **Charrus** (hero) | `hero/rifthound_h01` | 15 | **20** | 5,721 | 39–49 | 40 | 541 | 479 | 1.08 | 0.98 | Fire 8.7 |
| **Warden Krieg** ph.1 | `boss&quest/warden01` | 15 | **18** | 26,155 | 35–44 + wpn | 106 | 523 | 472 | 0.94 | 0.94 | W |
| **Warden Krieg** ph.2 | `boss&quest/warden02` | 15 | **18** | 35,198 | 37–47 + wpn | 106 | 535 | 476 | 1.08 | 1.15 | W |

Warden Krieg is the Act-1 boss (Hidden Laboratory), spawned by
`records/proxies/boss&quest/questproxy_wardena01.dbr` → `qp_wardena01.dbr`
(`spawnMin=spawnMax=1`, `alwaysSpawn1=True`, `levelVarianceEquation1 = lv7_uber hero`).
`warden01` carries `chanceToSpawnOnDeath = 100.0` and
`poolToSpawnOnDeath = records/proxies/poolsdeathspawn/dp_wardenphase2.dbr` — the two-phase fight is
source-visible, not lore. `weaponScale = 1.3` on both phases.

### Resistances (M — read directly off the monster record)

| monster | resistances (%) |
|---|---|
| Walking Dead / Wretcher / Plague Walker | *(none)* |
| Rotting Soldier | Pierce 10, Fire 10, Stun 20 |
| Tainted Hound | Aether 50 |
| Corruption (gazer) | Lightning 50, Aether 33, Life 30 |
| Ghoul | **Fire −20**, Life 30, Stun 33, Freeze 33, Trap 33 |
| Stonetusk / Gargantuan | Physical 10/15, Cold 15, Stun 30/50 |
| Dreadweave Arachnid | **Fire −15**, Poison 30 |
| Skeletal Warrior | Pierce 20, Cold 50 |
| Fleshwarped Butcher | Fire 15, Stun 50 |
| Fury | Physical 8, Pierce 15, Fire 10, Lightning 18, Poison 12, Stun 25 |
| Ironhide Stonetusk / Dreadtusk | Physical 25, Pierce 20, Cold 25 |
| Abner | Physical 40, Pierce 26, Poison 15 |
| Charrus | Lightning 30 |
| Warden Krieg ph.1 | Pierce 12, Fire 15, Poison 8, Aether 25, Stun 30, Freeze 30, Trap 30 |
| Warden Krieg ph.2 | Pierce 15, Fire 20, Cold 10, Lightning 8, Poison 15, Aether 33, Stun 30, Freeze 30, Trap 30 |

The Normal/1P pak adds **0** elemental resistance — every value above is the monster's own.

### Burst abilities (the real hero/boss threat)

Base-attack damage is nearly tier-invariant (§4). Tier threat lives in `Skill_Attack*` records.
Flat damage components, at the creature's own charLevel, after `tdmMult`:

| monster | ability | class | flat damage |
|---|---|---|---|
| Rotting Soldier | `zombie_charge` | AttackWeaponCharge | 72.6 phys (+300 % atk spd, +120 % run) |
| Stonetusk | `genericphysical_charge` | AttackWeaponCharge | +30 % TDM, +120 % run |
| Dreadtusk | `boar_charge` | AttackWeaponCharge | 28.6 phys (+300 % atk spd, +120 % run) |
| Dreadtusk | `dreadtusk_headbutt` | AttackWeapon | 25.8 phys |
| Warden ph.1 | `aetherwave_warden` | AttackWave | 38.1 phys + 56.0 aether |
| Warden ph.1 | `aetherzap_warden` | AttackSpellChaos | 48.1 aether |
| Warden ph.1 | `aetherarc_warden` | AttackWave | 43.9 phys + 32.8 aether |
| Warden ph.1 | `warden_charge` | AttackWeaponCharge | 46.0 phys + 16.3 aether (+120 % run) |
| Warden ph.1 | `aetherring_warden` | AttackProjectileAreaEffect | 31.9 aether |
| Warden ph.2 | `aethersmash_warden` | AttackRadius | **80.4 phys + 80.4 aether** |
| Warden ph.2 | `aetherstreak_warden2` | AttackWave | 23.3 phys + 73.2 aether |
| Warden ph.2 | `wardenspikes1` | AttackProjectileBurst | 26.7 phys + 22.1 pierce |

Both Warden phases carry `warden_rally1` / `warden2_rally2`
(`Skill_PassiveOnLifeBuffSelf`, +20–30 % total speed, ph.2 also +150 OA) — a below-threshold enrage.

---

## 3. Pack composition priors (M)

`records/proxies/pools/p_*.dbr`. `spawnMin/Max` are gated by
`proxyPoolEquation = proxypoolequation_01.dbr`, whose four equations are all `poolValue * 1` —
**an identity pass-through on Normal**, so the pool numbers are the literal pack sizes.
Champion count is `championChance` % per pack, capped by `championMax`; champions draw from a
*separate* `nameChampionN` roster (tougher DBRs), not from a multiplier on the trash proto.

| pool | spawn | championChance | championMax | trash entries | champion entries |
|---|---|---|---|---|---|
| `p_zombie_n` | **1–8** | 25 % | 2 | 9 | 7 |
| `p_zombie_n_hounds` | 3–7 | 20 % | 1 | 4 | 7 |
| `p_zombie_n_burning` | 3–7 | 20 % | 1 | 6 | 6 |
| `p_beasts_boar_n` | **2–9** | 15 % | 2 | 4 | 8 |
| `p_beasts_boar_t` | 4–7 | 25 % | 2 | 4 | 8 |
| `p_beasts_boarvulture_n` | 3–10 | 20 % | 2 | 5 | 9 |
| `p_beasts_prawn_n` | 3–9 | 20 % | 2 | 6 | 9 |
| `p_beastsswamp_rifthound_n` | **1–6** | 0 % | 1 | 4 | 0 |
| `p_spidergiant_n` | 6–9 | 10 % | 1 | 5 | 8 |
| `p_spidergiant_amb_n` (ambush) | 5–7 | 0 % | 0 | 5 | 0 |
| `p_undead_skeletons_n` | 3–10 | **50 %** | 2 | 2 | 9 |
| `p_undead_skeletons_amb_n` | **8–16** | 50 % | 2 | 2 | 9 |
| `p_undead_ghosts_amb_n` | 5–12 | 40 % | 2 | 4 | 9 |
| `p_undead_ghouls_n` | 3–8 | 50 % | 2 | 4 | 9 |
| `p_undead_skeletongolem_n` | 6–11 | 40 % | 1 | 4 | 9 |
| `p_undead_ghosts+skeletons_n` | 3–10 | 50 % | 2 | 6 | 9 |

Level-12-relevant roster gating inside `p_zombie_n` (M): `minPlayerLevel3 = 12` (Plague Walker
enters exactly at pL12), `minPlayerLevelChampion3 = 11`, `minPlayerLevelChampion4 = 12`,
`maxPlayerLevel9 = 7` / `maxPlayerLevelChampion7 = 13` (starter variants aging out). **The roster
itself churns at level 12** — this is not a static pool.

Area-001 proxies compose pools by weight, e.g. `bonerats-zombies_n.dbr`:
`pool1 p_beasts_prawn_n` w55 / `pool2 p_zombie_n` w20 / `pool3 p_zombie_n_hounds` w25,
`placementExtents = 6.0`; `beasts_boar_n.dbr`: `pool1 p_beasts_boar_n` w100, `placementExtents = 12.0`.
`placementExtents` is the pack's spatial spread radius.

**Not re-extracted (already banked from the Edition-II cut):** controller spatial fields —
`ViewDistance`, `SightAngerRate`, `MaxPursuitDistance`, `fleeDistance`. Cross-reference by the
`controller` field on each monster record, e.g. `zombie_a01 → records/controllers/enemy/controller_zombiea01.dbr`,
`warden01 → records/controllers/enemy/controller_boss_warden.dbr`. 175 records under
`records/controllers/enemy/`.

Adjacent M fields on the monster record that bear on pack behaviour and are *not* in the
controller: `distressCall = True`, `distressCallGroup = Aetherial`, `distressCallRange = 16.0`,
`distressCallTime = 2000` ms, `maxDistressCalls = 1`, `numAttackSlots = 4`, `numDefenseSlots = 4`
(zombie_a01). `numAttackSlots` caps how many pack members can engage simultaneously — a hard
concurrency prior for the sim.

---

## 4. The ratios that matter

Player level 12 measured (Matt play-test 2026-07-26): **759 HP pre-gear-step, 1600 HP post-gear-step.**

| tier | dmg/hit (mid) | % of 759 | % of 1600 | hits to kill player (759 / 1600) |
|---|---|---|---|---|
| trash (Common), 20-proto span | 33 – 49 | 4.3 – 6.5 % | 2.0 – 3.1 % | 15–23 / 33–48 |
| trash median | **41** | **5.4 %** | **2.6 %** | 19 / 39 |
| champion | 24 – 67 | 3.1 – 8.8 % | 1.5 – 4.2 % | 11–32 / 24–68 |
| hero | 40 – 44 | 5.2 – 5.8 % | 2.5 – 2.8 % | 17–19 / 36–40 |
| boss (Warden, base attack) | 39 – 42 | 5.2 – 5.5 % | 2.5 – 2.6 % | 19 / 39 |
| boss (Warden ph.2 `aethersmash`) | 161 burst | 21.2 % | 10.1 % | 5 / 10 |

| tier | HP | HP / 759 | HP / 1600 |
|---|---|---|---|
| trash light (`zombie_a01`, `prawn_a01`, `skeleton_a01`) | 181 – 226 | 0.24 – 0.30 | 0.11 – 0.14 |
| trash heavy (`ghoul_a01`, `zombie_soldiera01`, `boar_a02`) | 599 – 821 | 0.79 – 1.08 | 0.37 – 0.51 |
| champion | 676 – 1,326 | 0.89 – 1.75 | 0.42 – 0.83 |
| hero | 4,097 – 6,712 | 5.4 – 8.8 | 2.6 – 4.2 |
| boss ph.1 + ph.2 combined | 61,353 | 80.8 | 38.3 |

### The headline

**Act-1 Normal opposition is differentiated almost entirely on the HP axis, not the damage axis.**
Across a 200× HP span (181 → 35,198), base-attack damage-per-hit stays inside a **33–67** band —
a 2× spread. Every tier lands at **≈ 2.5 % of the post-gear player pool per hit** and **≈ 5 % of
the pre-gear pool**. This is not an artefact of my composition rule: it falls straight out of the
source, because `armorbase03–06` (used by champion/hero/boss) apply a −76 % damper at rank ~15
against `armorbase01/02`'s −41 %, almost exactly cancelling the richer `damagebase_physical03–06`
tables. The designers deliberately flattened early-game monster hit size and expressed tier
entirely through HP, armor, resistances, pack size, and burst abilities.

Corollaries for sim pinning:

1. **Player pool / trash hit ≈ 39** at the post-gear step, **≈ 19** pre-gear. The gear step Matt
   measured (759 → 1600) is a clean 2.1× survivability doubling with the opposition held fixed.
2. **Pack DPS, not single-hit DPS, is the pressure term.** `numAttackSlots = 4` caps simultaneous
   melee engagement at 4, so a 8-zombie pack applies ≈ 4 × 41 = **164 damage per engagement round**
   ≈ 10.3 % of the post-gear pool.
3. **Time-to-kill is the tier signal.** Player-side: trash needs 181–821 damage, champions
   676–1,326, heroes 4.1–6.7 k, the boss 61.4 k across two phases — a **339× TTK span** from
   lightest trash (181) to the full Warden fight, and **~75×** from heaviest trash (821).
4. **Armor matters at the boss, not at trash.** Warden armor 106 vs trash 3–9;
   `gameengine.armorDefensiveAbsorption = 70 %`.
5. Monster **run speed on Normal is uniformly reduced 18 %** by the pak. Effective values cluster
   0.54–1.07 with two outliers: Dreadweave Arachnid **1.64** (fastest Act-1 trash) and
   Abner **1.31**. Charge abilities add **+120 % run** for their duration.

---

## 5. Records used (exact paths)

**Scaling machinery**
- `records/game/gameengine.dbr` — `monsterAttributePak`, `playerAttributePak`, `monsterLevelGapFixer`, `armorDefensiveAbsorption`, `monsterDefenseCap`, `monsterRunSpeedCapMin/Max`, `bossRange`, `alertDistance`, `challengeAdjustment`, `endBossRecord`
- `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` — the 3×4 difficulty/player pak
- `records/game/balancingadjustment_mp+difficulty_players01.dbr` — player-side counterpart (Normal = all zero)
- `records/game/balancingadjustment_challengemode_enemies01.dbr` — Crucible/challenge deltas (incl. `spawnMaxAdj=1`, `spawnChampionMaxAdj=2`)
- `records/game/combatformulas.dbr` — `offensiveAbilityEquation`, `defensiveAbilityEquation`, `physicalDamageEquation`, `probabilityToHitEquation`, `pthThreshold1-6` / `pthDamageModifier1-6`, `pthMinimum`
- `records/game/experienceformulas.dbr` — `experienceEquation` in `monsterLevel` / `averagePartyLevel` (kill-cadence cross-check)

**Level resolution**
- `records/proxies/lv1_weak.dbr` … `records/proxies/lv8_boss.dbr` (+ `…+` variants) — 18 records
- `records/proxies/limit_area000.dbr` … `limit_area008.dbr`, `limit_unlimited.dbr`
- `records/proxies/proxypoolequation_01.dbr`

**Attribute equations** — `records/creatures/enemies/bios/bio_*.dbr` (336 records; `bio_zombie_01.dbr` quoted)

**Passive scaling tables** — `records/skills/nonplayerskills/passive/`:
`damage_totaladjuster.dbr`, `damagebase_physical00–06.dbr`, `damagebonus_physical01–05.dbr`,
`damagebonusranged_physical01–02.dbr`, `armorbase01–06.dbr`, `resists_heroboss.dbr`,
`resists_aetherial.dbr`, `passiveproperties_boar.dbr`, `passiveproperties_zombiemutated.dbr`,
`shieldblock.dbr` (192 passive records in base archive)

**Monsters** — all rows in §2, under `records/creatures/enemies/`

**Pools / proxies** — all rows in §3, under `records/proxies/pools/` (326 records) and
`records/proxies/area001/` (486 records); `records/proxies/boss&quest/questproxy_wardena01.dbr`,
`records/proxies/boss&quest/boss&questpools/qp_wardena01.dbr`,
`records/proxies/poolsdeathspawn/dp_wardenphase2.dbr`

**Display names** — `*/resources/Text_EN.arc`

---

## 6. Confidence + gaps

### High confidence (MEASURED, no inference)
- The five-record resolution chain and every field name and array in §1.
- All spawn-level equations, `charLevel` remaps, pool sizes, champion chances, roster gating.
- All resistances in §2 (read verbatim off the monster record).
- The pak index semantics (Normal/1P = index 0) — proven internally by the
  `characterLifeMultModifier` 4-cycle against the `characterLifeModifier` 3-block.

### Medium confidence (DERIVED; arithmetic shown, assumption named)
- **HP figures.** Composition (single additive life-modifier pool, then the multiplayer scalar) is
  the standard TQ/GD engine behaviour and produces a self-consistent 181 → 35,198 ladder. Not
  independently validated against a running client.
- **Damage figures.** The multiplicative pak stage (§1f) is **inferred by contradiction**, not
  stated in source. Under the alternative additive reading, `zombiemutated_a01` and both Warden
  phases deal **negative or zero damage** — impossible — so additive is falsified; but "multiplicative"
  is not thereby *proven*, only left standing. A third possibility (engine floors the summed
  modifier at some value > −100 %) would give different numbers. **If G-5 sim pinning is sensitive
  to monster hit size, this is the number to validate against a live client first.**
- **Skill-level truncation.** `int()` on equations like `(charLevel/25)+2`. Round-half-up would
  shift some ranks by 1; the effect on any figure here is ≤ 4 %.
- **`C`-flagged damage (min-clamped).** `passiveproperties_boar` and kin add flat
  `offensivePhysicalMin` with no `Max`, producing min > max after summation. I report
  `max ← max(min, max)`. The engine's actual clamp direction is not in the source.

### UNRESOLVED — flagged, not guessed
1. **Weapon-wielder base damage (W flag).** `zombie_soldiera01`, `humanoutlaw_*`,
   `humanchthonic_cultist_*`, `skeleton_a01`, `warden01/02` roll a weapon at spawn from
   `lootRightHandItem1-3` master tables (e.g. `mt_gearweaponsmelee1h.dbr`,
   `tdynx_enemy_sword1h_broken.dbr`). Their listed damage is **only the
   `damagebonus_physical0N` bonus** — real damage is that **plus** a per-instance random weapon.
   Resolving it requires walking the loot tables with the level-gated affix machinery; out of scope
   for G-5a. Warden also has `weaponScale = 1.3` and a fixed `records/items/enemygear/gear_warden_mace.dbr`
   in the corpus, which *could* be resolved exactly in a follow-up.
2. **Attack cadence in seconds.** `characterAttackSpeed` (e.g. 1.18) is a multiplier on an
   animation-driven base; `characterBaseAttackSpeedTag = CharacterAttackSpeedAverage`. The source
   does not carry a base attack interval in seconds — it lives in the `.anm` animation tables, which
   this lane does not parse. **The `aspd` column is a relative multiplier only.** Any DPS figure
   downstream must supply its own base interval and say so.
3. **Cross-check against grimtools failed.** `grimtools.com/monsterdb/276` (Warden Krieg) renders
   client-side; the underlying 8 MB `monsterdb.js` bundle carries the *same* `.arz` payload I parsed
   (record `m275` = `warden01`, `sk1256` = `armorbase01` with the identical `−55…+30` TDM array,
   and the same 12-element difficulty pak), confirming **my parse is faithful** — but the bundle's
   composition code is minified and I did not reverse it. So the composition operator in §1f
   remains adjudicated by contradiction, not by a second source. Accessed 2026-07-28.
4. **`lv5_elitechampion.dbr` has min > max** (`aPL+2` vs `(aPL+1)+(aPL/50)`). A source defect or an
   engine-side clamp I cannot see. No monster in §2 uses it; noted so it is not rediscovered.
5. **`characterLifeMultModifier` vs `characterLifeModifier`.** Both exist in the pak; I applied the
   first multiplicatively and folded the second into the additive pool. At Normal/1P the former is
   0, so no level-12 figure depends on the choice — but it will matter for any multiplayer or
   higher-difficulty extension.
6. **Veteran mode not modelled.** Matt's play-test was Normal. GD's "Veteran" is a Normal-difficulty
   toggle; I did not locate its adjustment record and did not guess one. If the fixture was played
   on Veteran rather than plain Normal, every damage and HP figure here is a floor.

---

*Downstream: gandalf (G-5 conductor) for sim-vs-fixture comparison; elrond if any of this is to be
curated into the catalogue. No canonical doc amended by this note.*
