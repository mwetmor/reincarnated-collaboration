# P-E5 — devotion proc templates for the EoR Warlord fixture — 2026-08-07

**Probe:** P-E5, Phase A of the KC2-SIM autonomous run
**Conductor:** gandalf (RUN-CONDUCTOR)
**Agent:** legolas (UNKNOWN-RESEARCHER) · **Mode:** A (analytical / primary-source datamine)
**Access:** READ-ONLY over the vendor corpus and over an already-banked save parse. Nothing written
outside `agentic_orchestration/legolas/`. **Not committed** — the conductor commits at gate close.
**Scratch / reproducibility:** `agentic_orchestration/legolas/scratch/2026-08-07-pe5-devotion/`
(`p1_dump.py`, `p2_ctrl.py`, `p3_bind.py`, `p4_filtered.py`, `p12_payload.py`, plus emitted
`powers_raw.json`, `payload_at_fixture_rank.json`)

**Grading key:** **DB-CITED** = read verbatim from a named record + field · **SAVE-MEASURED** = read
from the fixture's own `player.gdc` · **INFERRED** = derived, basis stated · **OPEN-SEMANTIC** =
not decidable from this substrate; candidate readings given, conductor rules.

---

## VERDICT BLOCK

**CLOSED-DB-CITED for questions 1–5. Question 6 is OPEN-SEMANTIC by construction, with the one
DB fact that decides most of it recovered.**

Three things this probe returns that the commission did not expect:

1. **Question 5 does not need an assumption.** The commission asked whether max rank is "the safe
   assumption for an endgame character." It is not an assumption — **the fixture's rank is written in
   the save, and all seven powers are at their DB maximum**, with `devotion-experience` byte-equal to
   the terminal entry of each power's own `skillExperienceLevels` array. 7/7 exact joins.
   Furthermore **no item in the entire 93,190-record corpus grants `+skill` to any devotion power**
   (0 hits on `augmentSkillName* → records/skills/devotion/`), so unlike Eye of Reckoning there is no
   allocated-vs-total rank ambiguity here. Devotion rank is XP-only, and this character's is maxed.

2. **The trigger and the proc chance are properties of the POWER, not of the player's binding.**
   Each power's own record carries `templateAutoCast → records/controllers/itemskills/cast_@<trigger>_<pct>%.dbr`,
   and the fixture's seven save-side `autocast-controller-name` strings are **identical to those seven
   `templateAutoCast` values, 7/7**. The player chooses only the *host skill*. This closes the whole
   trigger/chance half of the commission with a two-sided join (DB ⟷ save).

3. **Two powers carry no cooldown field at all, and one of them is Assassin's Mark.**
   `skillCooldownTime` is **absent — not zero, absent —** from Assassin's Mark's and Maul's records.
   Combined with Assassin's Mark's `chanceToRun = 100`, the only rate limiters on the fixture's
   headline debuff are the crit-event rate of the channel and the 18-second debuff duration. That is
   the single most load-bearing fact in this probe for the contribution envelope.

**One correction and one closure to prior art** (§ 6): the `tier2_17c` UI node's `FileDescription`
reads **"Golem"** where its constellation is **Crab** — a DB authoring artifact, do not use UI-node
descriptions as constellation names. And the save-parse's *"Maul — `tier2_05f_skill`, display tag
unresolved"* is now **resolved**: the tag lives on the *buff* record, `tagDevotionEffectB05 = "Maul"`.

**One structural finding the conductor will want before writing the envelope** (§ 5.3): Shifting Sands
is bound to **Summon Celestial Guardian**, a `Skill_TargetedSpawnPet`. An `AttackEnemy` trigger on a
summon host has no player attack event to fire from. The DB gives the pet's attack surface
(`characterAttackSpeed = 0.9`, `attackSkillName = petskill_celestialguardian_bladearc1.dbr`,
`skillTargetNumber = 5`) but **cannot decide** whether the power is delegated to the pet. Flagged
OPEN-SEMANTIC — it changes Shifting Sands' uptime driver entirely.

---

## § 0 — Substrate, path correction, and currency

### 0.1 Corpus — path correction against the commission

The commission names `~/Games/vendor/grim-dawn/`. **That directory is the Edition-I raw depot fetch
and holds only five archives — it has no `GDX3.arz` and no `SurvivalMode3.arz`.** The Edition-II
pinned corpus of record is `~/Games/vendor/grim-dawn-edition-II-20260724/` (8 archives), and that is
what this probe read.

| Archive | Records | Role in this probe |
|---|---:|---|
| `database/database.arz` | 34,114 | base devotion tree, **all 176 autocast controllers**, 5 of 7 powers' origin |
| `gdx1/database/GDX1.arz` (Ashes of Malmouth) | 18,447 | **sets the live payload values for the 5 base-game powers** |
| `gdx2/database/GDX2.arz` (Forgotten Gods) | 16,451 | origin + live values for Ulzaad's Decree, Shifting Sands; Oathkeeper skills |
| `gdx3/database/GDX3.arz` (Fangs of Asterkarn) | 24,178 | overrides all 7 records, **changes nothing substantive** |
| `resources/Text_EN.arc`, `gdx2/resources/Text_EN.arc` | — | display-name tag resolution |

**Would Edition-I have been sufficient?** Numerically yes, and this is measured, not assumed —
§ 0.3 shows GDX3 moves nothing but `skillTemplates`. But Edition-I could not have *proven* that, so
the Edition-II read is the correct one and the commission's path should be amended.

### 0.2 Overlay semantics — verified before use

GD `.arz` overlay is **whole-record replacement**, not field merge. Verified: `tier1_08e_skill_buff.dbr`
carries **617 fields in all four archives** with identical key sets and differing values. Every value
in this note is therefore read from the **last archive that carries the record** (`base → gdx1 → gdx2
→ gdx3`, later wins), which is `gdx3` for all seven powers.

### 0.3 Which archive actually sets each number

| Record | carriers | base→gdx1 | gdx1→gdx2 | gdx2→gdx3 |
|---|---|---|---|---|
| `tier1_08e_skill.dbr` | base·gdx1·gdx2·gdx3 | 0 | 0 | 0 |
| `tier1_08e_skill_buff.dbr` | all four | **4** (`defensivePhysical`, `defensivePierce`, `skillActiveDuration`, `skillExperienceLevels`) | 0 | 0 |
| `tier1_29e_skill.dbr` | all four | **3** (`damageAbsorption`, `skillCooldownTime`, `skillExperienceLevels`) | 0 | 0 |
| `tier2_02f_skill.dbr` | all four | **6** (all four payload arrays + `weaponDamagePct` + XP axis) | 0 | 0 |
| `tier2_05f_skill.dbr` | all four | 0 | 0 | 0 |
| `tier2_05f_skill_buff.dbr` | all four | **4** (`defensiveProtectionModifier`, `offensiveLifeLeechMin`, `offensivePhysicalMin`, XP axis) | 1 (`skillMasteryLevelRequired`) | 0 |
| `tier2_17c_skill.dbr` | all four | **3** (`damageAbsorption`, `endBuffSelfNames`, XP axis) | 0 | 0 |
| `tier2_37d_skill.dbr` | gdx2·gdx3 | — | — | 0 |
| `tier3_20e_skill.dbr` | gdx2·gdx3 | — | — | 0 |

(`skillTemplates` / `skillBlackList` excluded — engine scaffolding, drifts every expansion.)

**Reading: Ashes of Malmouth is the last expansion that re-tuned the five base-game powers, and it
also extended their rank axes.** Forgotten Gods and Fangs of Asterkarn left all seven alone.

### 0.4 Rank-axis extension — AoM lengthened every base-game celestial power

`len(skillExperienceLevels)` per archive:

| Power | base | gdx1 | gdx2 | gdx3 |
|---|---:|---:|---:|---:|
| Assassin's Mark | 20 | **25** | 25 | 25 |
| Turtle Shell | 20 | **25** | 25 | 25 |
| Tip the Scales | 15 | **20** | 20 | 20 |
| Maul | 15 | **20** | 20 | 20 |
| Arcane Barrier | 15 | **20** | 20 | 20 |
| Ulzaad's Decree | — | — | **20** | 20 |
| Shifting Sands | — | — | **15** | 15 |

**Anyone reading a devotion power out of a pre-AoM corpus gets a 20/15-rank ceiling and the wrong
terminal values.** Recorded because it is exactly the class of error the `.arz`-vs-grimtools
contradiction came from.

### 0.5 Patch currency

Client is **1.3.0.5**; the corpus is pinned at **1.3.0.0**. `legolas/notes/2026-08-04-gd-1305-patch-delta-probe.md`
§ 2.6 rules class 2 (*Devotions / procs*) **ZERO across all five hotfixes** — *"No devotion section in
any of the five. Maul / Ulzaad's Decree / Crab / Divine Mandate bindings unaffected."* § 3 V2's join
table lists *"Devotion records + proc bindings — **SAFE, zero deltas**"*. **Every number in this note is
join-safe against the live client.**

---

## § 1 — Question 5, answered first, because it decides the other four

### 1.1 The rank axis is XP, not points — and the save records the result

Every celestial power carries `skillMaxLevel = 1` and (where present) `skillUltimateLevel = 1`. Those
are the **allocation** caps: one devotion point, one node. The **rank** axis is `skillExperienceLevels`,
an XP table of 25 / 20 / 15 entries by constellation tier, and the character's position on it lives in
the save's `character_skills.skills[]` as `devotion-level` + `devotion-experience`.

### 1.2 The fixture, measured — 7/7 at maximum, 7/7 XP byte-exact

Read from `agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/p_gdc.json`
(the end-state parse, SHA `b8e6f510…4bfa5`):

| Power | `devotion-level` | axis len (DB) | `devotion-experience` (save) | terminal `skillExperienceLevels` (DB) | join |
|---|---:|---:|---:|---:|:--:|
| Assassin's Mark | **25** | 25 | 22,862,135 | 22,862,135 | **=** |
| Turtle Shell | **25** | 25 | 22,862,135 | 22,862,135 | **=** |
| Tip the Scales | **20** | 20 | 24,207,639 | 24,207,639 | **=** |
| Maul | **20** | 20 | 24,207,639 | 24,207,639 | **=** |
| Arcane Barrier | **20** | 20 | 24,207,639 | 24,207,639 | **=** |
| Ulzaad's Decree | **20** | 20 | 24,207,639 | 24,207,639 | **=** |
| Shifting Sands | **15** | 15 | 26,160,399 | 26,160,399 | **=** |

**7/7 at max rank. 7/7 XP exactly equal to the DB's terminal XP entry.** This is SAVE-MEASURED, not
inferred, and it is cross-verified against the archive it was read from.

### 1.3 No gear can move it — measured negative

An exhaustive scan of all four archives for `augmentSkillName<N>` values pointing anywhere under
`records/skills/devotion/` returns **0 hits**. **Devotion celestial powers take no `+skill` bonus from
gear.** Consequence: the save-parse § 2.5 rule (*"a `.gdc` skill rank is never directly comparable to a
grimtools rank"*) **does not apply to devotion powers** — allocated rank *is* total rank here. Only
mastery skills need the gear correction.

### 1.4 Ruling for the conductor

> **Every payload value in § 2 is read at the fixture's own measured rank. No max-rank assumption was
> made and none is needed. There is no rank-dependent uncertainty to carry in the error bars.**

---

## § 2 — The seven powers

Field → player-facing mapping used throughout, with grade:

| DB field | Player-facing meaning | Grade |
|---|---|---|
| `offensivePhysicalMin/Max` | Physical damage (flat) | DB-CITED field; standard GD naming |
| `offensivePierceMin` | Pierce damage | standard |
| `offensiveLifeMin` | **Vitality** damage (GD's "Life" damage type) | INFERRED-standard |
| `offensiveLifeLeechMin` | % of Attack Damage converted to Health (ADCtH) | INFERRED-standard, corroborated by the banked Twin Fangs anchor (`gd_devotion_bank_2026_07_25.py`: *"Life leech … does max at 40%"*) |
| `offensiveSlowManaLeachMin` + `…DurationMin` | Energy Leech over N seconds | INFERRED-standard |
| `offensiveTotalResistanceReductionAbsoluteMin` + Duration | flat "Reduces target's Resistances by X" (all types) | INFERRED-standard |
| `defensive<Type>` **negative on a `SkillBuff_Debuf`** | "Reduces target's `<Type>` Resistance by X%" | INFERRED-standard |
| `defensiveProtection` / `defensiveProtectionModifier` | Armor (flat) / % Armor | INFERRED-standard |
| `offensivePhysicalModifier` / `offensivePierceModifier` | +% Physical / +% Pierce damage | INFERRED-standard |
| `offensiveSlowPhysicalModifier` | +% **Internal Trauma** damage | INFERRED-standard |
| `retaliationPhysicalMin/Max` | Physical Retaliation | standard |
| `offensiveSlowOffensiveAbilityMin` + Duration | −X Offensive Ability for N sec | standard |
| `offensiveProjectileFumbleMin` + Duration | X% Impaired Aim for N sec | standard |
| `offensiveCritDamageModifier` | +% Crit Damage | see § 2.7 caveat |
| `damageAbsorption` | flat damage absorption (shield pool) | standard |
| `weaponDamagePct` | % Weapon Damage carried by the proc | standard |

---

### 2.1 Assassin's Mark — bound to **Eye of Reckoning**

| | |
|---|---|
| **Power record** | `records/skills/devotion/tier1_08e_skill.dbr` (`Class = Skill_AttackBuff`, 4 fields: `Class`, `FileDescription`, `buffSkillName`, `templateName`) |
| **Payload record** | `records/skills/devotion/tier1_08e_skill_buff.dbr` (`Class = SkillBuff_Debuf`, `debufSkill = True`) |
| **Constellation** | `records/ui/skills/devotion/constellations/constellation08.dbr` → `FileDescription = "Assassin's Blade"`, `constellationDisplayTag = tagDevotion_A08` → **"Assassin's Blade"** (`Text_EN.arc :: tags_skills.txt`) |
| **Display name** | `skillDisplayName = tagDevotionEffectA08` → **"Assassin's Mark"** |
| **Fixture rank** | **25 / 25** (SAVE-MEASURED) |

**Trigger** — `templateAutoCast = records/controllers/itemskills/cast_@enemyonattackcrit_100%.dbr`:

```
triggerType       AttackEnemyCrit
targetType        Enemy
chanceToRun       100
autoTargetRadius  22.0
```

**Cooldown** — `skillCooldownTime` is **ABSENT from both records** (verified: `'skillCooldownTime' in
rec == False`). Not zero. Absent. **No DB-resident internal cooldown.**

**Duration** — `skillActiveDuration[25] = 18.0` s.

**Payload at rank 25** (all from `tier1_08e_skill_buff.dbr`):

| Field | Rank 25 | Meaning |
|---|---:|---|
| `defensivePhysical` | **−32.0** | Reduces target's **Physical Resistance** by 32% |
| `defensivePierce` | **−36.0** | Reduces target's **Pierce Resistance** by 36% |
| `skillActiveDuration` | 18.0 s | debuff duration |

No damage component. No radius, no target-count field — `Skill_AttackBuff` on a devotion is uniformly
a one-field wrapper (`buffSkillName` only) across all 5 such records in the corpus, while the AoE
variant is `Skill_AttackBuffRadius` + `pointBlank` (see Maul). **Assassin's Mark is single-target by
structural discriminator.** `autoTargetRadius = 22.0` is the controller's *acquisition* range, not an
effect radius — note it exceeds Eye of Reckoning's own `skillTargetRadius = 3.0` by 7.3×.

**Envelope consequence (DERIVED):** with `chanceToRun = 100`, no cooldown, and an 18 s duration, the
uptime of the debuff on a given engaged target is bounded only by the crit-event rate. Any crit rate
above 1 per 18 s on that target saturates it. **The interesting number is therefore not uptime on the
primary target — it is how many *distinct* targets carry the mark**, which turns on the § 5.1
OPEN-SEMANTIC.

---

### 2.2 Turtle Shell — bound to **Field Command**

| | |
|---|---|
| **Power record** | `records/skills/devotion/tier1_29e_skill.dbr` (`Class = Skill_BuffSelfShield`, `instantCast = True`) |
| **Constellation** | `constellation29.dbr` → `FileDescription = "Turtle"`, `constellationDisplayTag = tagDevotion_A29` → **"Tortoise"** |
| **Display name** | `tagDevotionEffectA29` → **"Turtle Shell"** |
| **Fixture rank** | **25 / 25** |

**Trigger** — `cast_@selfat50%health_100%.dbr`:

```
triggerType   LowHealth
triggerParam  50.0        <- health % threshold
targetType    Self
chanceToRun   100
              (no autoTargetRadius — self-cast)
```

**Cooldown** — `skillCooldownTime` is a **rank array**: `[32.0 … 8.0]`, **8.0 s at rank 25**.
**Duration** — **NOT IN THE CORPUS.** See § 7 gap G-1: `skillActiveDuration` is absent from **all 15
`Skill_BuffSelfShield` records in the corpus**, player and monster alike. Shield lifetime is engine-
or template-side and the `.tpl` files are not in the depot fetch.

**Payload at rank 25:** `damageAbsorption = 6100.0` — a flat 6,100-point absorption pool.
**No damage-type qualifier flags are set** (`fireDamageQualifier`, `coldDamageQualifier`,
`elementalDamageQualifier`, `lifeDamageQualifier`, `poisonDamageQualifier`, `bleedingDamageQualifier`
all `False`) → **absorbs all damage types.** Contrast Arcane Barrier (§ 2.5), which is filtered.

**Envelope consequence (DERIVED):** proc-rate ceiling **1 per 8 s**, and the trigger is a state
predicate (health ≤ 50%) rather than an event, so realized rate is a function of incoming-damage
volatility, not of attack cadence.

---

### 2.3 Tip the Scales — bound to **Presence of Virtue**

| | |
|---|---|
| **Power record** | `records/skills/devotion/tier2_02f_skill.dbr` (`Class = Skill_AttackSpell`, `distanceProfile = Maximum`) |
| **Constellation** | `constellation37.dbr` → **"Scales of Ulcama"** (`tagDevotion_B02`) |
| **Display name** | `tagDevotionEffectB02` → **"Tip the Scales"** |
| **Fixture rank** | **20 / 20** |

**Trigger** — `cast_@enemyonanyhit_33%.dbr`:

```
triggerType       HitByEnemy        <- DEFENSIVE trigger: fires when the PLAYER is hit
targetType        Enemy
chanceToRun       33
autoTargetRadius  22.0
```

> **Flag for the conductor.** The controller basename reads `onanyhit`, which is easy to misread as
> "on any hit *you land*." The `triggerType` field says **`HitByEnemy`** — it fires **when the player
> takes a hit**. Same for Arcane Barrier (§ 2.5). Two of the seven powers are on incoming-damage
> triggers, not outgoing.

**Cooldown** — `skillCooldownTime = 1.0` s (scalar).
**Duration** — the effect is instantaneous; two riders carry their own durations (below).

**Payload at rank 20:**

| Field | Rank 20 | Meaning |
|---|---:|---|
| `offensiveLifeMin` | **310.0** | Vitality damage |
| `offensiveLifeLeechMin` | **132.0** | 132% of Attack Damage converted to Health |
| `weaponDamagePct` | **33.0** | 33% Weapon Damage |
| `offensiveTotalResistanceReductionAbsoluteMin` | **20.0** | **Reduces target's Resistances by 20** … |
| `offensiveTotalResistanceReductionAbsoluteDurationMin` | 3.0 s | … for 3 seconds |
| `offensiveSlowManaLeachMin` | **200.0** | 200 Energy Leech … |
| `offensiveSlowManaLeachDurationMin` | 2.0 s | … over 2 seconds |

Single target (`Skill_AttackSpell`, no radius field). **Envelope ceiling: 1 proc per 1.0 s.**

**Note for the envelope math:** this is the *second* resistance-reduction source in the kit, and it is
a **structurally different encoding** from Assassin's Mark's — a flat all-resist field on the attack
record versus negative per-type resistances on a debuff record. Whether they stack is an engine rule,
**not DB-decidable** (§ 7 gap G-4).

---

### 2.4 Maul — bound to **Vire's Might**

| | |
|---|---|
| **Power record** | `records/skills/devotion/tier2_05f_skill.dbr` (`Class = Skill_AttackBuffRadius`, `pointBlank = True`) |
| **Payload record** | `records/skills/devotion/tier2_05f_skill_buff.dbr` (`Class = SkillBuff_Debuf`, `debufSkill = True`) |
| **Constellation** | `constellation40.dbr` → **"Dire Bear"** (`tagDevotion_B05`) |
| **Display name** | `tagDevotionEffectB05` → **"Maul"** — *this closes the save-parse § 2.3 "display tag unresolved" item; the tag is on the buff record, not the parent* |
| **Fixture rank** | **20 / 20** |

**Trigger** — `cast_@selfonattack_20%.dbr`:

```
triggerType       AttackEnemy
targetType        Self
chanceToRun       20
autoTargetRadius  5.0
```

**Cooldown** — `skillCooldownTime` **ABSENT from both records.** No DB-resident internal cooldown.
**Duration** — `skillActiveDuration = 5.0` s (scalar).

**Payload at rank 20** (from the buff record):

| Field | Rank 20 | Meaning |
|---|---:|---|
| `offensivePhysicalMin` | **305.0** | Physical damage |
| `offensiveLifeLeechMin` | **45.0** | 45% of Attack Damage converted to Health |
| `defensiveProtectionModifier` | **−35.0** | Reduces target's **Armor** by 35% |
| `skillActiveDuration` | 5.0 s | debuff duration |
| `skillTargetRadius` | **4.5** | AoE radius |
| `expansionTime` | 0.01 s | radius expansion time (effectively instant) |

**Point-blank AoE, radius 4.5, unlimited targets in radius** (no `skillTargetNumber` field).

**Envelope consequence (DERIVED):** ceiling = 0.20 × (Vire's Might attack-event rate). Vire's Might is
`Skill_AttackPathCharge` with `skillCooldownTime = 3.5999999` s and `timeBetweenAttacks = 100`, so the
host is itself cooldown-gated at ~1 use / 3.6 s. **Maul's realized rate is host-limited, not
chance-limited** — it is by some distance the lowest-frequency offensive proc in the kit.

---

### 2.5 Arcane Barrier — bound to **Divine Mandate**

| | |
|---|---|
| **Power record** | `records/skills/devotion/tier2_17c_skill.dbr` (`Class = Skill_BuffSelfShield`, `instantCast = True`) |
| **Constellation** | `constellation52.dbr` → `FileDescription = "Crab"`, `constellationDisplayTag = tagDevotion_B17` → **"Crab"** |
| **Display name** | `tagDevotionEffectB17` → **"Arcane Barrier"** |
| **Fixture rank** | **20 / 20** |

**Trigger** — `cast_@selfonanyhit_30%.dbr`:

```
triggerType       HitByEnemy        <- DEFENSIVE, fires when the player is hit
targetType        Self
chanceToRun       30
autoTargetRadius  5.0
```

**Cooldown** — `skillCooldownTime = 3.0` s (scalar).
**Duration** — **NOT IN THE CORPUS** (same gap G-1 as Turtle Shell).

**Payload at rank 20:** `damageAbsorption = 2900.0`, and — unlike Turtle Shell — **filtered by damage
type**:

```
aetherDamageQualifier      True
chaosDamageQualifier       True
elementalDamageQualifier   True
lifeDamageQualifier        True
poisonDamageQualifier      True
```

**Physical, Pierce and Bleed are NOT in the qualifier set.** Against a physical-damage threat profile
this shield absorbs nothing. That is a materially different defensive contribution from Turtle
Shell's unfiltered 6,100, and the envelope should not pool them.

**Envelope ceiling:** 1 proc per 3.0 s.

---

### 2.6 Ulzaad's Decree — bound to **War Cry**

| | |
|---|---|
| **Power record** | `records/skills/devotion/tier2_37d_skill.dbr` (`Class = Skill_BuffSelfDuration`, `instantCast = True`) — **GDX2-origin**, `FileDescription = "Ulzaad - Ulzaad Decree"` |
| **Constellation** | `constellation106.dbr` → `FileDescription = "Ulzaad"`, `constellationDisplayTag = tagGDX2Devotion_B201` → **"Ulzaad, Herald of Korvaak"** |
| **Display name** | `tagGDX2DevotionEffectB201` → **"Ulzaad's Decree"** |
| **Fixture rank** | **20 / 20** |

**Trigger** — `cast_@selfonattack_20%.dbr` (the same controller record Maul uses):

```
triggerType       AttackEnemy
targetType        Self
chanceToRun       20
autoTargetRadius  5.0
```

**Cooldown** — `skillCooldownTime = 22.0` s (scalar).
**Duration** — `skillActiveDuration[20] = 10.0` s.

**Payload at rank 20 — this is the buff's full contents:**

| Field | Rank 20 | Meaning |
|---|---:|---|
| `offensivePhysicalModifier` | **200.0** | **+200% Physical Damage** |
| `offensivePierceModifier` | **200.0** | **+200% Pierce Damage** |
| `offensiveSlowPhysicalModifier` | **200.0** | **+200% Internal Trauma Damage** |
| `offensivePhysicalMin` / `Max` | **42.0 / 45.0** | +42–45 flat Physical Damage |
| `defensiveProtection` | **190.0** | +190 Armor |
| `retaliationPhysicalMin` / `Max` | **205.0 / 450.0** | +205–450 Physical Retaliation |
| `skillActiveDuration` | **10.0 s** | buff duration |

**Envelope consequence (DERIVED, and this is the cleanest analytic bound in the whole probe):**
duration 10.0 s against cooldown 22.0 s gives a **hard maximum duty cycle of 10 / 22 = 45.45%**, and
that ceiling is reached only if the 20%-chance trigger fires within the first instant of every
cooldown expiry. War Cry (`Skill_AttackRadius`, `skillCooldownTime = 7.5` s) can offer a trigger event
at most every 7.5 s, so the practical bound is lower still. **Ulzaad's Decree is the one proc in this
kit whose contribution envelope is genuinely uptime-shaped rather than rate-shaped, and its ceiling is
below one half.**

---

### 2.7 Shifting Sands — bound to **Summon Celestial Guardian**

| | |
|---|---|
| **Power record** | `records/skills/devotion/tier3_20e_skill.dbr` (`Class = Skill_AttackProjectile`, `distanceProfile = Long`) — **GDX2-origin** |
| **Constellation** | `constellation109.dbr` → `FileDescription = "Azrakaa"`, `constellationDisplayTag = tagGDX2Devotion_C202` → **"Azrakaa, the Eternal Sands"** |
| **Display name** | `tagGDX2DevotionEffectC202` → **"Shifting Sands"** |
| **Fixture rank** | **15 / 15** |

**Trigger** — `cast_@enemyonattack_20%.dbr`:

```
triggerType       AttackEnemy
targetType        Enemy
chanceToRun       20
autoTargetRadius  22.0
```

**Cooldown** — `skillCooldownTime = 0.5` s. **Duration** — `skillActiveDuration = 1.0` s (projectile
lifetime).

**Payload at rank 15:**

| Field | Rank 15 | Meaning |
|---|---:|---|
| `offensivePhysicalMin` | **205.0** | Physical damage |
| `offensivePierceMin` | **335.0** | Pierce damage |
| `weaponDamagePct` | **30.0** | 30% Weapon Damage |
| `offensiveCritDamageModifier` | **40.0** | +40% Crit Damage — see caveat |
| `offensiveSlowOffensiveAbilityMin` / `…DurationMin` | **140.0** / 3.0 s | −140 Offensive Ability for 3 s |
| `offensiveProjectileFumbleMin` / `…DurationMin` | **25.0** / 3.0 s | 25% Impaired Aim for 3 s |

**Geometry:** `skillProjectileNumber = 1`, `skillProjectileMaximumNumber = 5`,
`projectilePiercingChance = 100.0`, `projectileExplosionRadius = 2.0`. One projectile per proc,
pierces every target it crosses, 2.0-radius impact. `skillProjectileMaximumNumber = 5` caps
simultaneous instances (INFERRED from field name + the 0.5 s cooldown against 1.0 s lifetime, which
would otherwise allow only 2 concurrent).

**Caveat on `offensiveCritDamageModifier`** — 461 records in the corpus carry a non-zero value. On
`Skill_Passive` devotion nodes (e.g. `tier2_21e.dbr`, 15.0) it grants the *player* crit damage; here it
sits on an *attack* record, so the parsimonious reading is **this projectile's own crit damage**.
INFERRED, basis stated; a player-wide grant is the alternative and would be a materially different
contribution. Not DB-decidable.

**Envelope ceiling:** 1 proc per 0.5 s — the highest-frequency ceiling in the kit — **but see § 5.3:
the trigger source may be the pets, not the player.**

---

## § 3 — The trigger layer, characterised

### 3.1 Schema — first-of-kind for this substrate

All autocast controllers live at `records/controllers/itemskills/cast_@<trigger><pct>%.dbr` in
**`database.arz` only** (176 records; GDX1 re-issues one, GDX2 none, GDX3 carries two unrelated
sandbox records). Template `database/templates/skillautocastcontroller.tpl`. **Exactly seven fields
exist across all 176 records:**

| Field | present on | values observed |
|---|---:|---|
| `templateName` | 176 | (one) |
| `FileDescription` | 176 | the percentage as text |
| `chanceToRun` | 176 | integer percent |
| `targetType` | 176 | `Self` · `Enemy` · `Ally` · `EnemyLocation` |
| `triggerType` | 176 | **closed set of 9**, below |
| `autoTargetRadius` | 161 | `5.0` · `8.0` · `15.0` · `22.0` · `30.0` |
| `triggerParam` | 9 | `15 · 20 · 25 · 30 · 33 · 35 · 40 · 45 · 50` (health-% thresholds) |

**The complete GD proc-trigger vocabulary, measured:**

```
AttackEnemy · AttackEnemyCrit · Block · HitByCrit · HitByEnemy ·
HitByMelee · HitByProjectile · LowHealth · OnKill
```

**There is NO internal-cooldown field on any controller.** The only DB-resident rate limiter is the
power's own `skillCooldownTime` — which, for Assassin's Mark and Maul, does not exist. This is worth
stating flatly because a plausible-looking "global proc ICD" is exactly the kind of thing an envelope
model invents when it needs one: **the corpus does not contain one.**

### 3.2 The DB ⟷ save cross-verification

The save stores the binding on the **host** skill's entry (`autocast-skill-name` + `autocast-controller-name`);
the power's own entry carries empty strings. Comparing the seven save-side controller strings against
the seven DB-side `templateAutoCast` values:

| Host skill (save) | Power (save) | controller (save) | `templateAutoCast` (DB) | match |
|---|---|---|---|:--:|
| `playerclass09/eyeofreckoning1` | `tier1_08e_skill` | `cast_@enemyonattackcrit_100%` | same | **✓** |
| `playerclass01/fieldcommand1` | `tier1_29e_skill` | `cast_@selfat50%health_100%` | same | **✓** |
| `playerclass09/presenceofvirtue1` | `tier2_02f_skill` | `cast_@enemyonanyhit_33%` | same | **✓** |
| `playerclass09/viremight1` | `tier2_05f_skill` | `cast_@selfonattack_20%` | same | **✓** |
| `playerclass09/divinemandate1` | `tier2_17c_skill` | `cast_@selfonanyhit_30%` | same | **✓** |
| `playerclass01/warcry1` | `tier2_37d_skill` | `cast_@selfonattack_20%` | same | **✓** |
| `playerclass09/summon_celestialguardian1` | `tier3_20e_skill` | `cast_@enemyonattack_20%` | same | **✓** |

**7/7.** The trigger and chance are not player choices — the player picks only the host.

### 3.3 The design logic the bindings reveal

The fixture's seven bindings are not arbitrary; **defensive-trigger powers are on toggled/aura hosts
and offensive-trigger powers are on attack hosts**, without exception:

| Power | trigger class | host `Class` | coherent? |
|---|---|---|:--:|
| Turtle Shell | `LowHealth` | `Skill_BuffRadiusToggled` (Field Command) | ✓ |
| Arcane Barrier | `HitByEnemy` | `Skill_BuffSelfToggled` (Divine Mandate) | ✓ |
| Tip the Scales | `HitByEnemy` | `Skill_BuffRadiusToggled` (Presence of Virtue) | ✓ |
| Assassin's Mark | `AttackEnemyCrit` | `Skill_AttackRadiusSpin` (Eye of Reckoning) | ✓ |
| Maul | `AttackEnemy` | `Skill_AttackPathCharge` (Vire's Might) | ✓ |
| Ulzaad's Decree | `AttackEnemy` | `Skill_AttackRadius` (War Cry) | ✓ |
| Shifting Sands | `AttackEnemy` | **`Skill_TargetedSpawnPet`** (Summon Celestial Guardian) | **see § 5.3** |

Six of seven are structurally clean. The seventh is the finding.

---

## § 4 — Question 6: what counts as an "attack" for the channelled spin

### 4.1 The one DB fact that decides most of it

`records/skills/playerclass09/eyeofreckoning1.dbr` (winner: **GDX2**), `Class = Skill_AttackRadiusSpin`,
template `database/templates/skill_attackradiusspin.tpl`:

```
timeBetweenAttacks        200
duration                  0.25
useResetsDuration         True
rotationSpeedMultiplier   0.35
skillTargetRadius         3.0
targetingMode             Point
distanceProfile           Melee
canUseWhileMoving         True
delayMovement             True
skillMaxLevel             16          skillUltimateLevel  26
```

**`timeBetweenAttacks = 200` is the tick interval, and the field is named `…Attacks`, not `…Hits` or
`…Ticks`.** That naming is itself evidence: the engine's own vocabulary calls each channel tick an
**attack**.

**Unit — INFERRED, milliseconds.** Basis: 56 records in the corpus carry the field; the value
histogram is `{50:1, 100:29, 200:5, 300:11, 330:1, 500:3, 600:3, 800:3}` — integers, 50–800. A seconds
reading gives 50–800 s per tick, physically impossible for a channel. A millisecond reading gives
1.25–20 Hz, which is the plausible band. Comparable channels corroborate: Aether Ray
(`playerclass05/aetherray1`, `Skill_AttackSpellBeam`) 300; Flames of Ignaffar
(`playerclass07/purifyingflame1`, `Skill_AttackSpellCone`) 300; Life Tap 300; Winds of Asterkarn 200.

> **Eye of Reckoning's base tick rate is 200 ms — 5 attack events per second.** DERIVED from a
> DB-CITED value plus a stated unit inference.

### 4.2 What is *not* decidable, stated precisely

Three questions the DB cannot answer. All three are **OPEN-SEMANTIC**; the conductor rules, not me.

**OS-1 — Does one tick generate one trigger event, or one per target struck?**

| Candidate | Consequence for Assassin's Mark uptime |
|---|---|
| **(a) per tick** — one `AttackEnemyCrit` roll per 200 ms regardless of how many enemies are inside the 3.0 radius | trigger rate = 5 Hz × P(crit); marks accumulate one target at a time |
| **(b) per target struck** — one roll per enemy hit per tick | trigger rate = 5 Hz × N<sub>targets</sub> × P(crit); marks saturate a whole pack almost instantly |
| **(c) per tick, but the mark lands on the specific enemy that was crit** | 5 Hz × P(crit), and the mark follows the crit target rather than the controller's 22 m search |

DB evidence bearing on it, offered without a ruling: the controller has `targetType = Enemy` **and**
`autoTargetRadius = 22.0`, i.e. it performs its own target *selection* within 22 m — which is 7.3× Eye
of Reckoning's 3.0 damage radius. A trigger that already selects its own target argues against (b)
and for (a)/(c). But the controller schema carries no "targets per fire" field, so this is a lean, not
a proof.

**OS-2 — Does `timeBetweenAttacks` scale with Attack Speed?**
No DB field couples them. `eyeofreckoning1.dbr` carries no `characterAttackSpeed` entry.
Candidates: (a) fixed 5 Hz regardless of Attack Speed; (b) 5 Hz is the base and Attack Speed scales it
multiplicatively, so the fixture's actual tick rate is 5 × (1 + AS%). Under (b) the fixture's tick
rate — and therefore every `AttackEnemy`-class proc rate in the kit — moves with a stat the sim
already models. **This is the higher-leverage of the two unknowns and it is the one worth closing
empirically** (§ 8).

**OS-3 — Does the crit that satisfies `AttackEnemyCrit` include the orbital sub-skill?**
`records/skills/playerclass09/eyeofreckoning2.dbr` (`SkillSecondary_AttackProjectileOrbiting`,
`projectilePeriod = 0.2`, `projectilePiercingChance = 100`, `skillProjectileTargetGroundOnly = True`)
is a *second* damage source on the same skill, ticking on its own 200 ms period. If its hits can crit
and count as attacks, the effective trigger rate roughly doubles. The fixture holds
`eyeofreckoning2` at allocated rank 12, so the sub-skill is live. Not DB-decidable.

### 4.3 The fixture's Eye of Reckoning values, for the conductor's arithmetic

Total rank **26** per the ceremony lane (allocated 15 + gear; `skillUltimateLevel = 26` is the DB cap,
so 26 is the ceiling and the two lanes agree — save-parse § 2.5). Rank-26 row:

| Field | Rank 26 |
|---|---:|
| `weaponDamagePct` | 50.0 |
| `offensivePhysicalMin` / `Max` | 162.0 / 182.0 |
| `offensiveFireMin` | 138.0 |
| `skillManaCost` | 16.0 |
| `defensiveCrowdControl` | 25.0 |
| `skillTargetRadius` | 3.0 (scalar, rank-invariant) |
| `timeBetweenAttacks` | 200 (scalar, rank-invariant) |

---

## § 5 — Findings the commission did not ask for

### 5.1 Assassin's Mark is the only power in the kit with *no* rate limiter of its own

Of the seven, five carry a `skillCooldownTime` (8.0 / 1.0 / 3.0 / 22.0 / 0.5 s). **Assassin's Mark and
Maul carry none**, and Assassin's Mark is additionally at `chanceToRun = 100`. Its rate is *entirely*
determined by the channel's crit-event rate — i.e. by OS-1 and OS-2. **The two unknowns in § 4.2 are
not peripheral to the envelope; for the fixture's single largest damage multiplier they are the whole
of it.** Maul is the mirror case and is harmless, because its host is cooldown-gated at 3.6 s.

### 5.2 The kit carries two structurally different resistance-reduction sources

Assassin's Mark: **−32% Physical / −36% Pierce Resistance**, encoded as negative `defensive<Type>` on a
`SkillBuff_Debuf`, 18 s.
Tip the Scales: **−20 all Resistances**, encoded as `offensiveTotalResistanceReductionAbsoluteMin` on an
attack record, 3 s.

Different fields, different records, different durations, different trigger polarity (offensive vs
defensive). **Whether they compose additively is an engine rule and is not in the corpus** (G-4).
The conductor should not silently sum them.

### 5.3 Shifting Sands' host is a pet summon — and this changes its uptime driver

`records/skills/playerclass09/summon_celestialguardian1.dbr`:

```
Class              Skill_TargetedSpawnPet
skillCooldownTime  20.0
petLimit           [n=26] 2,2,…,2,3,3,3      <- 2 at the fixture's rank
spawnObjects       records/skills/playerclass09/pets/celestialguardian_01.dbr …
```

Guardian actor (`pets/celestialguardian_01.dbr`, `Class = PetPlayerScaling`):

```
characterAttackSpeed  0.9
attackSkillName       records/skills/playerclass09/pets/petskill_celestialguardian_bladearc1.dbr
buffSelfSkillName     records/skills/playerclass09/pets/petskill_celestialguardian_celestialwrath1.dbr
```

Guardian attack (`petskill_celestialguardian_bladearc1.dbr`): `Class = Skill_AttackWeapon`,
`skillTargetNumber = 5`, `skillTargetAngle = 180.0`, `distanceProfile = Melee`.

**The problem, stated plainly.** An `AttackEnemy` trigger needs an attack event. `Skill_TargetedSpawnPet`
generates one only when the summon is *cast*, which is cooldown-gated at 20 s. Two readings:

| Candidate | Uptime driver |
|---|---|
| **(a) delegated to the pets** — the power is granted to each summoned Guardian and procs off *their* attacks | 2 guardians × their own attack cadence (`characterAttackSpeed = 0.9`, 5-target 180° arc) × 20%, floored by the power's own 0.5 s cooldown |
| **(b) procs on the summon cast** | at most 1 roll per 20 s × 20% ⇒ ~1 proc per 100 s — negligible, effectively a dead binding |

The corpus does contain a dedicated devotion-pet lane (`records/skills/devotion/pets/`, **147 distinct
records**) which is consistent with (a) being a real mechanic in this engine, but that is
circumstantial and I am not ruling it. **The two candidates differ by roughly two orders of magnitude
in Shifting Sands' contribution.** OPEN-SEMANTIC — conductor rules.

### 5.4 Analytic ceilings, all seven — DERIVED, for the envelope's upper bound

| Power | own cooldown | duration | hard ceiling from DB alone |
|---|---:|---:|---|
| Assassin's Mark | **none** | 18.0 s | **unbounded by the power** — set by crit-event rate; debuff saturates the target above 1 crit / 18 s |
| Turtle Shell | 8.0 s | *unknown (G-1)* | ≤ 1 proc / 8 s |
| Tip the Scales | 1.0 s | instant (+3 s RR, +2 s leech) | ≤ 1 proc / 1 s |
| Maul | **none** | 5.0 s | ≤ 0.20 × host rate; host is cd-gated at 3.6 s ⇒ ≈ 1 proc / 18 s |
| Arcane Barrier | 3.0 s | *unknown (G-1)* | ≤ 1 proc / 3 s |
| Ulzaad's Decree | 22.0 s | 10.0 s | **duty cycle ≤ 10/22 = 45.45%**, and lower in practice (host cd 7.5 s, chance 20%) |
| Shifting Sands | 0.5 s | 1.0 s (projectile) | ≤ 1 proc / 0.5 s — but see § 5.3 |

---

## § 6 — Corrections and closures against prior art

1. **`records/ui/skills/devotion/tier2_17c.dbr` has `FileDescription = "Golem"`. Its constellation is
   Crab.** `constellation52.dbr` (which enumerates `tier2_17a…e` as its `devotionButton1…5`) reads
   `FileDescription = "Crab"` and `constellationDisplayTag = tagDevotion_B17` → **"Crab"**; the skill
   record's own `FileDescription` is `"Crab - Arcane Barrier"`. Three sources against one.
   **Do not derive constellation names from UI-node `FileDescription`** — derive them from the
   `constellationNN.dbr` that lists the node, and resolve the display tag. The save-parse § 2.3 got
   this right; recording it so a future lane does not "correct" it wrongly.

2. **CLOSED — save-parse § 2.3's *"(Maul) — `tier2_05f_skill`, display tag unresolved"*.** The parent
   `Skill_AttackBuff*` records carry **no** `skillDisplayName`; the tag is on the buff record.
   `tier2_05f_skill_buff.dbr` → `skillDisplayName = tagDevotionEffectB05` → **"Maul"**. General rule:
   for `Skill_AttackBuff` / `Skill_AttackBuffRadius` devotion powers, **everything** — display name,
   description, payload, duration, radius, XP axis, and `templateAutoCast` — lives on the buff record;
   the parent carries 1–2 fields.

3. **Constellation display names differ from internal `FileDescription` for two of the seven.**
   `tier1_29` internal "Turtle" vs display **"Tortoise"**; `tier2_37` internal "Ulzaad" vs display
   **"Ulzaad, Herald of Korvaak"**; `tier3_20` internal "Azrakaa" vs **"Azrakaa, the Eternal Sands"**.
   The save-parse used display names throughout and is consistent.

4. **The commission's corpus path is wrong.** `~/Games/vendor/grim-dawn/` is the Edition-I fetch
   (5 archives, no GDX3). Use `~/Games/vendor/grim-dawn-edition-II-20260724/`. § 0.1.

5. **Devotion powers are exempt from the save-parse § 2.5 allocated-vs-total rank rule.** That rule
   was written for mastery skills. Devotion ranks take no gear bonus (§ 1.3, measured 0 hits), so a
   `.gdc` `devotion-level` **is** directly comparable to a grimtools devotion rank.

---

## § 7 — Named gaps

| # | Gap | Why it is open | What closes it |
|---|---|---|---|
| **G-1** | **Shield duration for Turtle Shell and Arcane Barrier** | `skillActiveDuration` is absent from **all 15** `Skill_BuffSelfShield` records in the corpus (player and monster). Lifetime is template- or engine-side | the `.tpl` files — **not in the depot fetch** (`database/templates/` does not exist; 0 `.tpl` anywhere in 189 MB). One in-game tooltip screenshot, or a depot pull that includes templates |
| **G-2** | **`distanceProfile` → metres** | enum `Melee · Short · Moderate · Long · Maximum · Boss` (3,244 records), with **no data-side definition record** | engine-side; only measurable in play |
| **G-3** | **`timeBetweenAttacks` unit** | INFERRED milliseconds from magnitude + cross-skill comparison (§ 4.1). Not stated anywhere in data | frame-count a channel tick, or a template read |
| **G-4** | **Do the two RR sources stack?** | different fields on different records; composition is engine arithmetic | in-game stat-sheet observation with one, then both, applied |
| **G-5** | **OS-1 / OS-2 / OS-3** (§ 4.2) | trigger firing semantics for a channel are engine code | frame-level observation, or a controlled proc-count measurement |
| **G-6** | **Is Shifting Sands delegated to the pets?** (§ 5.3) | pet-binding is engine behaviour; the DB shows only that the host is a spawn skill | one observation of whether sand projectiles originate at a Guardian or at the player |
| **G-7** | **`offensiveCritDamageModifier` scope on an attack record** | own-crit-damage vs player-wide grant; the field is used both ways elsewhere in the corpus | tooltip read |

**G-1 and G-5/G-6 are the two that touch the envelope.** G-1 bounds the two shields' contribution;
G-5/G-6 set the rate for the two largest offensive procs. Everything else is cosmetic.

---

## § 8 — One cheap closure, recommended not ruled

**G-5 (OS-2, attack-speed scaling) and G-1 (shield duration) are both closable from a single 60-second
in-game observation on the fixture**, which the run is already going to have a client open for:
hover Eye of Reckoning and Turtle Shell in the character sheet and read the tooltips; then toggle a
known Attack Speed source and re-read. That converts the largest remaining uncertainty in the envelope
from a modelling assumption into a measurement. **Not commissioned, not performed, offered as the
cheapest available upgrade to the envelope's error bars.**

---

## § 9 — Sources

All local, read-only, primary. No network access was used in this probe.

| Source | Path | Role |
|---|---|---|
| GD base database | `~/Games/vendor/grim-dawn-edition-II-20260724/database/database.arz` | 34,114 records; devotion tree, all 176 autocast controllers |
| Ashes of Malmouth | `…/gdx1/database/GDX1.arz` | 18,447; live payload values for the 5 base powers |
| Forgotten Gods | `…/gdx2/database/GDX2.arz` | 16,451; Ulzaad + Azrakaa constellations, Oathkeeper skills |
| Fangs of Asterkarn | `…/gdx3/database/GDX3.arz` | 24,178; final overlay (no substantive change to any of the 7) |
| Localization | `…/resources/Text_EN.arc` (`tags_skills.txt`), `…/gdx2/resources/Text_EN.arc` (`tagsgdx2_skills.txt`) | all 14 display tags resolved |
| Fixture save parse | `agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/p_gdc.json` | `devotion-level`, `devotion-experience`, `autocast-*` for all 367 skill entries |
| `.arz` adapter | `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (`ArzArchive`) | TQIT/LZ4-block reader |
| `.arc` reader | `agentic_orchestration/research/scripts/gd_arc_reader_2026_07_26.py` (`ArcArchive`) | ARC v3 reader |
| Prior art — bindings, devotion 55/55, EoR rank reconciliation | `legolas/notes/2026-08-05-eorwarlguts-save-parse.md` | the 7 bindings |
| Prior art — build context | `legolas/notes/2026-08-01-eor-endgame-build-of-record.md` | fixture provenance |
| Prior art — patch currency | `legolas/notes/2026-08-04-gd-1305-patch-delta-probe.md` § 2.6, § 3 V2 | devotion join-safety at 1.3.0.5 |
| Prior art — extraction lineage | `legolas/notes/2026-08-01-gd-pack-density-ranking.md` | overlay convention, adapter usage |
| Prior art — devotion field policy + Twin Fangs anchor | `research/scripts/gd_devotion_bank_2026_07_25.py`, `gd_devotion_field_policy_2026_07_25.py` | field-semantic corroboration |

---

## CLOSURE VERDICT

> **CLOSED-DB-CITED** for commission questions **1, 2, 3, 4, 5** — all seven powers' record paths,
> constellations, trigger conditions, proc chances, cooldowns, durations, payloads and geometry are
> read verbatim from named records and fields, at the fixture's **save-measured** rank, and the
> trigger layer is additionally cross-verified DB ⟷ save at 7/7.
>
> **PARTIAL** on question **6** — the channel's tick interval is recovered (`timeBetweenAttacks = 200`
> on `records/skills/playerclass09/eyeofreckoning1.dbr`), but the three semantics that convert ticks
> into trigger events are **OPEN-SEMANTIC** and are handed to the conductor with candidate readings:
> **OS-1** per-tick vs per-target-struck · **OS-2** attack-speed scaling of the tick rate ·
> **OS-3** whether the orbital sub-skill's hits count.
>
> **Named gaps carried:** **G-1** shield duration for Turtle Shell / Arcane Barrier is not in the
> corpus (absent from all 15 `Skill_BuffSelfShield` records; templates not in the depot fetch) ·
> **G-2** `distanceProfile` metre mapping · **G-3** `timeBetweenAttacks` unit is INFERRED ms ·
> **G-4** RR stacking rule · **G-5** = OS-1/2/3 · **G-6** whether Shifting Sands is delegated to the
> Celestial Guardians · **G-7** `offensiveCritDamageModifier` scope.

### Seven-row summary

| Power | Trigger | Chance | Cooldown | Headline payload at the fixture's rank |
|---|---|---:|---:|---|
| **Assassin's Mark** (r25/25) | `AttackEnemyCrit` → Enemy, 22 m acq. | **100%** | **none (field absent)** | −32% Physical Res, −36% Pierce Res, **18 s**; single target |
| **Turtle Shell** (r25/25) | `LowHealth` ≤ 50% → Self | **100%** | **8.0 s** | **6,100** damage absorption, **all damage types**; duration unknown (G-1) |
| **Tip the Scales** (r20/20) | `HitByEnemy` → Enemy, 22 m | **33%** | **1.0 s** | 310 Vitality + 33% Weapon Dmg, **132% ADCtH**, **−20 all Res / 3 s**, 200 Energy Leech / 2 s; single target |
| **Maul** (r20/20) | `AttackEnemy` → Self, 5 m | **20%** | **none (field absent)** | 305 Physical, **−35% Armor**, 45% ADCtH, **5 s**, **PBAoE r 4.5** |
| **Arcane Barrier** (r20/20) | `HitByEnemy` → Self | **30%** | **3.0 s** | **2,900** absorption, **Aether/Chaos/Elemental/Vitality/Poison only** (no Physical/Pierce); duration unknown (G-1) |
| **Ulzaad's Decree** (r20/20) | `AttackEnemy` → Self | **20%** | **22.0 s** | **+200% Physical / +200% Pierce / +200% Internal Trauma**, +42–45 Phys, +190 Armor, 205–450 Phys Retaliation, **10 s ⇒ duty cycle ≤ 45.45%** |
| **Shifting Sands** (r15/15) | `AttackEnemy` → Enemy, 22 m | **20%** | **0.5 s** | 205 Physical + 335 Pierce + 30% Weapon Dmg, +40% Crit Dmg, −140 OA / 3 s, 25% Impaired Aim / 3 s; 1 piercing projectile, 2.0 blast — **trigger source contested (G-6)** |

---

**Signed:** legolas, 2026-08-07. The commission asked whether max rank was a safe assumption. It
turned out not to be an assumption at all — the save has the number, all seven are maxed, and the
experience totals match the database's own tables to the unit. What the probe found that nobody asked
for is where the uncertainty actually lives: not in the ranks, and not in the payloads, but in two
places the database is structurally silent about. Assassin's Mark has no cooldown field at all, so its
whole contribution rides on how a spinning channel turns 200-millisecond ticks into trigger events;
and Shifting Sands is bound to a summon, which either delegates it to two guardians or renders it
nearly inert. Both are one observation away from closed.
