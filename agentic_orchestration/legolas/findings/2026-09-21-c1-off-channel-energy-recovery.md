# Research — C-1: off-channel energy recovery, Grim Dawn EoR Warlord referent — 2026-09-21

**Mode:** A (analytical / primary-source probe)
**Commission:** **C-1**, the first issued under *The Commission Rule* (`gandalf/notes/2026-09-21-the-commission-rule.md`)
**Commissioner / conductor:** gandalf (RUN-CONDUCTOR, Run KC2-PLAY)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Access:** read-only throughout. No game file, save, pack, oracle or vendor tree was modified. robots.txt verified per-domain before any fetch; see § 8.

---

## HEADLINE

**The MECHANISM question is ANSWERED, decisively, from four independent surfaces. The DECOMPOSITION of the rate lands `searched-SOURCE-UNLOCATED` with a named partial formula and a 28.75 /s residual.**

Three sentences, in the order a reader needs them:

1. ⚑ **`regen_per_s = 75.37` is BOTH the on-channel and the off-channel rate. It is unconditional.** Grim Dawn contains no channel-conditional stat machinery of any kind, and every enumerated contributor to it is an always-on character stat, aura or gear line.
2. **Off-channel drain is not reduced — it is structurally absent.** Eye of Reckoning's cost is a **per-attack-tick charge** (`skillManaCost`), not a per-second upkeep (`skillActiveManaCost`, which exists in the engine and which EoR does not carry). No tick, no charge. `off_channel_drain = 0.0`, exactly.
3. ⚑ **`tip_the_scales` CAN contribute off-channel.** It is not channel-gated at all — it is gated on **being hit** (`triggerType = HitByEnemy`, 33 %). Channelling and being-hit are **orthogonal axes**, and neither the oracle nor the port models the real one.

**What this convicts:** the port's `+175.37 /s` off-channel law is wrong, but **not in the half that was suspected.** Its regen term is correct and unconditional. The unprovenanced part is crediting **Tip the Scales at its full 100 /s bound** — and that same over-credit sits in the **channelling** branch too, where it produces the `−1.03 /s` the runtime boot-checks to ±0.005. ⚑ **The footage contradicts `−1.03 /s` outright: galadriel measured the below-cap channelling net at −73.4 to −81.7 /s.** See § 6. That tension is reported, not reconciled.

**What did NOT close:** `75.37` itself is already graded `MEASURED` and C-1 does not depend on decomposing it. I attempted the decomposition anyway, enumerated nine contributors, found the Crate-official spirit formula, and **still fall 28.75 /s short.** That residual is a *bonus* investigation's honest end state, not a failure of C-1. ⚑ **I did not tune Spirit to close it.** See § 5.3.

---

## 0 · Surface status — what was searched, what was reachable, what was not

| Surface | Status | Detail |
|---|---|---|
| **Build guide** (Matt's #1) | ✅ searched, **with a named gap** | Crate forum `/t/`, `grimdawn.com/guide/`, Steam, Miraheze fetched. **GrimTools, Reddit, Fandom NOT fetched — robots.txt.** § 8 |
| **Game on disk — DBRs / ARZ** | ✅ **LIVE** | `/Users/admin/depots/` — 7 archives parsed: 34,114 (base) + 18,447 (GDX1) + 16,451 (GDX2) + 24,178 (GDX3) + 1,004 + 811 + 1,431 (SurvivalMode 1–3) records |
| **Game on disk — binary** | ❌ **UNAVAILABLE** | `/Users/admin/Games/vendor/grim-dawn/Game.dll` gone; `/Volumes/reincarnated` not mounted. **No PE binary anywhere on this host.** This is where the base-regen formula lives. |
| **Localization** | ✅ | 8 × `Text_EN.arc`, **20,394 tags** extracted |
| **Save** | ✅ | `player.gdc`, sha256 `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5` — byte-identical to the 2026-08-23 decode fixture. Level 100, 55 devotion, 367 skill entries, 92 allocated. |
| **Footage** | ✅ derived artifacts | galadriel `MD-B4app-2` / `-2b`. ❌ **source MP4 gone** (`/Users/admin/gd-scratch/eor-test-2/`) — no re-measure possible this session. |

**Reproduction tooling** (scratch, read-only, reusable): `arz.py` (TQIT `.arz` reader, all 7 archives), `scan.py` (full-database field scan), `arcread.py` (copied unmodified from `research/scripts/gd_arc_reader_2026_07_26.py`), `gdcg7.py` (copied unmodified from `legolas/scratch/2026-07-28-gdc-parse-g7/gdc_parse.py`). Parser validated against the 2026-07-23 probe's own record counts (34,114 base — exact match).

---

## 1 · Q1 — THE MECHANISM: why off-channel drain is exactly zero

### 1.1 The engine has two cost fields; EoR uses only the per-activation one

| field | semantics | present on `eyeofreckoning1.dbr`? |
|---|---|---|
| `skillManaCost` | charged **per activation / per attack** | ✅ `[4.0, 4.0, 5.0, … 15.0, 16.0]`, 26 ranks |
| `skillActiveManaCost` | charged **per second while active** | ❌ **ABSENT** |

`skillActiveManaCost` occurs on exactly **75 records across all four archives.** Every single one is a toggle, aura, shapeshift or NPC aura buff — `Skill_BuffSelfToggled`, `Skill_BuffAttackRadiusToggled`, `SkillBuff_Passive`, `SkillBuff_Debuf`, `Skill_Shapeshift`, `Skill_BuffSelfColossus`, `Skill_BuffSelfDuration`. **Eye of Reckoning is not among them.**

### 1.2 The client says it in plain English

`tagGDX2Class09SkillDescription07A` (`tagsgdx2_skills.txt`, GDX2 `Text_EN.arc`):

> *"…for as long as the Oathkeeper channels their focus into the attack. ^oRequires a melee weapon. **At 100% Attack Speed, Eye of Reckoning deals damage and drains Energy every 0.16s.**"*

This closes byte-exact against the DBRs:

```
eyeofreckoning1.dbr :: timeBetweenAttacks = 200 (ms)
malepc01.dbr        :: characterAttackSpeed = 1.25
200 ms / 1.25 = 0.1600 s      <-- the client's own figure, exactly
```

⚑ **The drain is an EVENT BOUND TO THE ATTACK TICK.** Not a rate, not an upkeep. Therefore:

> **`off_channel_drain = 0.0`, grade `DB-CITED` + `CLIENT-VERBATIM`. Derived from record text and client text, not inferred.**

### 1.3 The full decomposition reproduces the client tooltip

```
per-tick charge  = skillManaCost[rank 26] x cost_factor = 16.0 x 0.90 = 14.40
drain per second = 14.40 x 12.25 ticks/s                              = 176.40 /s
client tooltip (in-video, s2 t~193-240)                               = 176.4    ✓
```

Cross-check on the tick rate: `0.16 s x 12.25 /s = 1.96`, i.e. the pack's `ticks_per_second = 12.25` implies **196 % total attack speed**. I have **not** independently verified the character's attack speed; this is a testable consequence handed to gamora, not a finding asserted here.

---

## 2 · Q2 — THE RATE, one row per contributor, with per-term provenance

Only **two** stat fields in the entire shipped database carry energy regeneration. Verified by exhaustive field-name scan across all four archives: `characterManaRegen` (flat, energy/s) and `characterManaRegenModifier` (percent). **No ranged / min-max form of either exists on any record.**

### 2.1 Contributors to off-channel energy INCOME

| # | Contributor | Term | Value | Source record | Grade |
|---|---|---|---|---|---|
| 1 | base PC record | `characterManaRegen` | **1.0** (level-1 seed) | `database.arz :: records/creatures/pc/malepc01.dbr` | `DB-CITED` |
| 2 | ⚑ **Presence of Virtue** (aura buff) @ total rank 18 | `characterManaRegen[17]` | **10.4** | `GDX2.arz :: records/skills/playerclass09/presenceofvirtue1_buff.dbr` | `DB-CITED` + save-rank |
| 3 | **Scales of Ulcama** (devotion) | `characterManaRegen` | **2.5** | `database.arz :: records/skills/devotion/tier2_02c.dbr` | `DB-CITED` + save + **dev patch note** (§ 9.1) |
| 4 | Arcanum Dust augment (necklace) | `characterManaRegen` | **2.5** | `GDX1.arz :: records/items/enchants/b130a_enchant.dbr` | `DB-CITED` + save |
| 5 | Arcanum Dust augment (Gargabol's Ring) | `characterManaRegen` | **2.5** | same record | `DB-CITED` + save |
| 6 | Combustion Band (ring base) | `characterManaRegen` | **1.8** | `GDX1.arz :: records/items/gearaccessories/rings/d110_ring.dbr` | `DB-CITED` + save |
| | | **gear + skill flat subtotal** | **19.7** | | |
| 7 | **Arcane Spark** component (medal) | `characterManaRegenModifier` | **20.0 %** | `database.arz :: records/items/materia/compb_arcanespark.dbr` | `DB-CITED` + save |
| 8 | Scales of Ulcama | `characterManaRegenModifier` | **33.0 %** | `tier2_02c.dbr` | `DB-CITED` + save |
| 9 | Jackal (devotion) | `characterManaRegenModifier` | **10.0 %** | `database.arz :: records/skills/devotion/tier1_38a.dbr` | `DB-CITED` + save |
| | | **percent subtotal** | **63.0 %** | | |
| — | ⚑ **base regeneration from Spirit** | — | **NOT RECOVERED** | formula lives in `Game.dll`; **binary not mounted** | ⚑ **`searched-SOURCE-UNLOCATED`** |
| 10 | **Tip the Scales** (devotion proc) | leech | **200.0 over 2.0 s**, *conditional* — see § 4 | `GDX3.arz :: records/skills/devotion/tier2_02f_skill.dbr` | `DB-CITED` + save-confirmed |

**Correctly EXCLUDED** — these carry regen fields but are **`level = 0`** in the save (not taken): Panther (+15 %), Raven (+1.5), Dryad (+1.0), Lotus (+1.0/+15 %), Bard's Harp (+3.0/+25 %), Eye of the Guardian (+1.0). Also excluded because they carry no regen at all: the Warborn Armor set (3 pieces equipped), the Deathstalker relic, all 12 equipped items' prefixes/suffixes/modifiers, and every one of the 92 allocated skills' buff chains other than Presence of Virtue. `itemSkills` in the save: **0**.

⚑ **Row 2 is a pack row we do not have.** The pack already reads `presenceofvirtue1_buff.dbr` at index 17 for its **reservation** (`V15-12 = 220.0`). It has never lifted the **regeneration** off the same record at the same index.

### 2.2 The composition rule — the client states it

`tagCharStatsEnergyRegenInfo` (`tags_ui.txt`), verbatim:

> *"The rate at which your energy replenishes. **Percent bonuses only affect regeneration from gear and skills; not base regeneration, which is based on spirit.**"*

Units confirmed by `tagCharManaRegen` = `"{%+.1f0} {^E}Energy Regenerated per second"`.

```
total = base(spirit)  +  gear_and_skill_flat x (1 + percent)
```

### 2.3 The equipped loadout (resolved, for the record)

Warborn Visor · **Kaisan's Burning Eye** (+ **Seal of Annihilation** + Arcanum Dust) · Warborn Chestguard · Solael-Sect Legguards · Windshear Greaves · Sandreaver Bracers · **Combustion Band** · **Gargabol's Ring** (+ Arcanum Dust) · Gladiator's Distinction · Warborn Pauldrons · **Mark of Harvoul** (+ **Arcane Spark**) · Deathstalker (relic) · **Gutsmasher** (2H blunt).

---

## 3 · Q3 — ⚑ THE CRUX, answered in one sentence

> ## **`regen_per_s = 75.37` is BOTH the off-channel rate and the on-channel rate. It is a continuous, unconditional character stat, and nothing in Grim Dawn suppresses, reduces or otherwise alters it while a skill is being channelled.**

Five independent legs. No channel condition survives any of them.

**Leg 1 — exhaustive field scan, all four archives.** Every field whose *name* contains `channel` is an **animation-speed** field: `dHandedChannelAnimSpeed`, `…ChannelStartAnimSpeed`, `…ChannelEndAnimSpeed` across the five weapon stances — **15 fields, all animation, 4,594 records each.** ⚑ **There is no field anywhere in the shipped database that conditions any stat on channelling state.**

**Leg 2 — the stat is a per-second character stat**, not a skill state (`tagCharManaRegen`, above).

**Leg 3 — ⚑ the minimally-different tooltip pair.** The health and energy stat tooltips are word-for-word parallel — same template, same author, same sentence shape:

| | |
|---|---|
| `tagCharStatsLifeRegenInfo` | *"The rate at which your health replenishes **while in combat**. Percent bonuses only affect regeneration from gear and skills; not base regeneration, which is based on physique."* |
| `tagCharStatsEnergyRegenInfo` | *"The rate at which your energy replenishes. Percent bonuses only affect regeneration from gear and skills; not base regeneration, which is based on spirit."* |

**The health one carries a state qualifier. The energy one omits it.** The game knows how to say "conditional on state" and chose not to, for energy. This is about as strong as a negative gets from client text.

**Leg 4 — every contributor is unconditional.** A base character stat; one *toggled* aura paid for by a permanent **220-energy reservation** and carrying **no `skillActiveManaCost`** (i.e. no upkeep — see § 9.1 for the developer statement confirming this); one passive devotion; three gear lines. **None has an activation condition of any kind.**

**Leg 5 — GD's one out-of-combat recovery mechanism is health-only.** `tagQuickTip45` / `tagQuickTip46` / `tagTutorialTip45TextD`: Constitution converts to health out of combat. ⚑ **There is no energy analogue.** Clean negative on "energy recovers by a special out-of-combat rule."

**⚑ And the footage agrees, which is the strongest leg of all.** galadriel's derived off-channel income (**≈ +112 /s**) is the *same number* as the income implied by her channelling measurement (gross drain ≈ 190 /s + net ≈ −78 /s = **+112 /s**). **The income term is identical on both sides of the channel.** The only thing that changes between the two states is whether the drain is being charged. See § 6.

---

## 4 · Q4 — can `tip_the_scales` contribute off-channel?

### 4.1 ⚑ YES — because it is not channel-gated at all. It is HIT-gated.

`records/skills/devotion/tier2_02f_skill.dbr` — `FileDescription = "Scales of Ulcama - Tip the Scales"`.

| term | value | source | grade |
|---|---|---|---|
| trigger | **`triggerType = HitByEnemy`** | `records/controllers/itemskills/cast_@enemyonanyhit_33%.dbr` | `DB-CITED` |
| chance | **`chanceToRun = 33`** | same | `DB-CITED` |
| target / radius | `targetType = Enemy`, `autoTargetRadius = 22.0` | same | `DB-CITED` |
| cooldown | `skillCooldownTime = 1.0` | proc DBR | `DB-CITED` |
| energy leech | `offensiveSlowManaLeachMin[19] = 200.0` over `offensiveSlowManaLeachDurationMin = 2.0 s` | proc DBR | `DB-CITED` |
| tier | ⚑ **`devotionLevel = 20`, `experience = 24207639` — exactly `skillExperienceLevels[19]`, the top tier** | **the save** | `SAVE-CONFIRMED` |
| host | `presenceofvirtue1.dbr` — a **permanent toggled aura** | **the save** (`autoCastSkill` / `autoCastController`) | `SAVE-CONFIRMED` |
| stacking | same-source ⇒ **refresh, not stack** | our L-32/E-1 ruling; our own `Game.dll` DoT decode (same-source MAX) | `DECODED` |

**The spec's "HitByEnemy, 33 %" is verbatim correct.**

### 4.2 ⚑ A near-miss worth recording: the filename is not the field

I nearly filed a false contradiction here. The controller filename reads `cast_@enemyonanyhit_33%`, which *looks* offensive ("on any hit **I** land"). It is not. I mapped all 250 controller records and **the two axes are orthogonal**:

- `targetType` ∈ {`Self`, `Ally`, `Enemy`, `EnemyLocation`} — **where the triggered skill is aimed**
- `triggerType` ∈ {`AttackEnemy`, `AttackEnemyCrit`, **`HitByEnemy`**, `HitByMelee`, `HitByProjectile`, `HitByCrit`, `Block`, `LowHealth`, `LowMana`, `OnKill`, `CastBuff`, `OnEquip`} — **what event fires it**

`base_atself_onanyhit`, `base_atally_onanyhit` and `base_atenemy_onanyhit` **all** carry `triggerType = HitByEnemy`. `AttackEnemy` is the separate, distinct token for "when you attack." **`HitByEnemy` unambiguously means taking a hit.** The `@enemy` prefix is the TARGET.

**Consequence for the model:** a player who stops channelling but remains in the pack still procs it. A player who has disengaged does not. **Channelling and being-hit are different axes and the model conflates them.**

### 4.3 The realized rate is neither 100 /s nor `0.33 × 100`

From the decoded mechanism alone, with `h` = **incoming enemy hits per second on the player**:

```
realized_per_s = 100.0 x U(h),   U(h) = 1 - (1 - 0.33)^(2h)
```
(`U` = probability a cast landed inside the 2.0 s leech window; the 1.0 s cooldown caps applications, and refresh-not-stack caps the delivered rate at one window's worth.)

| h (hits/s) | 0 | 0.25 | 0.5 | 1 | 2 | 3 | 5 | 8 | 12 |
|---|---|---|---|---|---|---|---|---|---|
| **realized /s** | **0.0** | 18.1 | 33.0 | 55.1 | 79.8 | 91.0 | 98.2 | 99.8 | 100.0 |

⚑ **`h` is the missing input — and it is ALREADY a registered absence** (`ABS-MONSTER-OFFENSE-NO-DATA-POOL466`, the opposition model). The envelope row's *"up to 100 energy/s"* is the `h → ∞` limit. **`TIP_THE_SCALES_TRIGGER_CHANCE = 0.33` is dead in the code because the function that would consume it was never written** — the bound was shipped where the realized rate belonged.

⚑ **Note explicitly: the naive `0.33 × 100 = 33.0` is NOT what this mechanism yields at any `h`.** `U` crosses 0.33 near `h ≈ 0.5` hits/s and saturates well above it. Anyone folding this must fold `U(h)`, not the bare chance.

### 4.4 Unreconciled: a duration conflation in `devotion.py`

`kc2/devotion.py:59` carries `duration_s=3.0` for `tip_the_scales`. The DBR has **two** durations and both are real:

- `offensiveSlowManaLeachDurationMin = 2.0` — the **energy leech**
- `offensiveTotalResistanceReductionAbsoluteDurationMin = 3.0` — the **resist shred**

Which one that field is meant to carry is not stated in the code. Reported; not resolved.

---

## 5 · The decomposition attempt — and the residual

### 5.1 The arithmetic, shown

With the Crate-official Spirit formula (§ 9.2) and total Spirit = 237 (base 50 + save-bio 74 + gear `characterIntelligence` 113):

```
gear + skill flat                     = 19.7
gear + devotion percent               = 63.0 %
spirit flat      = 0.01   x 237       =  2.37
spirit percent   = 0.26 % x 237       = 61.62 %

total = base_L100 + 2.37 + 19.7 x (1 + 0.63 + 0.6162)
      = base_L100 + 2.37 + 44.25
      = base_L100 + 46.62

MEASURED total (ceremony §D #511)      = 75.37 /s
RESIDUAL, NOT ATTRIBUTED               = 28.75 /s
```

Without the Spirit formula the residual was **42.26 /s**; the formula narrows it to **28.75 /s** and does not close it. The remaining unknown is the **level-scaling of base regeneration** — its formula is in `Game.dll`, and the binary is not mounted.

### 5.2 ⚑ I DID NOT TUNE SPIRIT TO MAKE IT CLOSE

Closure is available. Solving for the Spirit value that would make the ledger balance:

```
75.37 = 1.0 + 0.01 S + 19.7 x (1.63 + 0.0026 S)   ->   S = 690.3
```

**I am not doing that, and this is the reason:** ~690 Spirit is not a number a physical two-hander Warlord carries. His base is 50, his gear contributes 113, and his build dumps attribute points into Physique, not Spirit. To make 690 true I would have to assume an attribute allocation the save contradicts, in service of a number I wanted to reach. **That is precisely the fitted constant Law 3 forbids, and it is more dangerous here than usual because it would close cleanly and look like a derivation.**

**A near-closing number is the only condition under which Law 3 is ever actually tested.** The honest end state is a residual with a name on it.

### 5.3 The same hole appears in a second, independent ledger

Max energy, as a self-test of the gear-resolution method:

```
base:  characterMana 250 + manaIncrement 16 x 99 levels = 1834
gear:  characterMana (compa_restlessremains)            = + 220
                                                          ------
                                                           2054
MEASURED (energy globe, four timestamps / 830 s)        =   2576
residual                                                =    522
```

⚑ **The same shape.** One unenumerated Spirit-scaled term appears in both the regen ledger and the pool ledger, which is exactly what the client's own tooltip predicts ("base regeneration, which is based on spirit") and exactly what the Crate guide's *"energy by 2 and energy regeneration by 0.01 + 0.26%"* describes. **This is consistency evidence for the shape of the missing term. It is not a derivation of it, and I am not fitting one.**

### 5.4 ⚑ C-1 does not depend on this

`75.37` is already graded `MEASURED` and the commission did not ask me to decompose it. § 3 answers the crux by **mechanism** — whether the rate is conditional — and that answer does not move whatever the decomposition turns out to be. **The residual is a bonus investigation's honest end state, not a failure of C-1.**

---

## 6 · ⚑ THE CONTRADICTION. I am not reconciling it.

The commission was explicit: *"Do not reconcile a disagreement for me… That tension is information; a smoothed answer destroys it."*

| quantity | value | provenance |
|---|---|---|
| pack / port channelling net | **−1.03 /s** | derived `176.4 − 75.37 − 100.0`; boot-gated at ±0.005 (`kc2rt_fight.gd:409`) |
| ⚑ **footage, below-cap channelling net** | **−81.7 /s** (stationary) · **−73.4 /s** (moving) | `MD-B4app-2` § 4.4, measured |
| footage, gross drain | **≈ −190 /s** | ibid. — galadriel flags this **NOT DERIVED** against the published 176.4 |
| footage, derived off-channel income | **≈ +112 /s** | `MD-B4app-2b` § 1.3 (derived by galadriel from her own two measurements, not directly measured) |
| footage, direct per-release `dE/dt`, 6 unclipped positives | 36.4 · 51.6 · 65.5 · 65.5 · 106.2 · 134.4 — **median 65.5** | `s2-releases.json`, my extraction |
| **port's off-channel law** | **+175.37 /s** | ⚑ **exceeds every one of the 19 measured releases** (max observed 134.4 /s over 0.867 s) |

**Three things follow. None is a reconciliation.**

**(a) The port's `+175.37 /s` is refuted by footage.** No measured release reaches it.

**(b) The over-credit is in the Tip-the-Scales term, and it sits on BOTH branches.** `112 − 75.37 = 36.6`, and `190 − 78 − 75.37 ≈ 36.6`. The proc appears to realize roughly **a third** of its 100 /s bound in both states. That is the right *order* for a 33 % trigger. ⚑ **I am flagging this as a numerical coincidence, not a derivation** — see § 4.3: the mechanism does not yield `0.33 × 100` at any `h`.

**(c) ⚑ The band `(86, 117)` never constrained the RATE — only the DEPTH.** The oracle reproduces the `1477` crossing as a *slow transit* at −1.03 /s arriving at t = 99.6 s. The footage shows **64.6 % of combat spent pinned at the 1594 ceiling**, with fast sawtooth excursions 86–117 deep on a **~1.5 s** timescale, refilled by 0.6–3.5 s releases (19 of them, 10.5 % of combat, one every 9.6 s; 12 of 19 reach the ceiling *before they end*). **Both reproduce the numbers. Only one reproduces the dynamics.** A depth measurement cannot pin a rate, and it was read as though it could.

**A caveat that must ride with (a)–(c):** galadriel's own note carries *"a second combat-only per-second energy sink cannot be excluded from pixels"* and grades the per-tick-vs-tooltip reconciliation **NOT DERIVED**. The −190 /s gross drain is hers and she does not assert it against the published 176.4.

---

## 7 · ⚑ BY-CATCH: C-3 is solved

`energy.cost_factor = 0.90`, currently graded `MEASURED-EXACT-SOURCE-UNLOCATED` — **the one back-solved value in the energy stack**. The source is in the save:

> **`GDX1.arz :: records/items/materia/compb_sealannihilation.dbr`** — **Seal of Annihilation** (`Class = ItemRelic`, `itemClassification = Rare`, `levelRequirement = 75`), socketed in **Kaisan's Burning Eye** (necklace, equipment slot 1) per `player.gdc`.
>
> **`skillManaCostReduction = 10.0`**

Units confirmed from the client's own strings: `SkillManaCostReduction = "-{%.0f0}% {^E}Skill Energy Cost"`; `tagCharStatsManaCostReductionInfo = "The percent by which the energy cost of your skills is reduced."`

**−10 % ⇒ ×0.90.** It is the **only** cost-reduction source on the build: zero across all other equipped items, affixes, components, augments and relic bonuses, and zero across all 92 allocated skills and their buff chains.

→ **Proposed regrade: `MEASURED-EXACT-SOURCE-UNLOCATED` → `DB-CITED` + `SAVE-CONFIRMED`.**

### 7.1 Independent validation: 11 of 11 pack rows reproduced from primary source

I rebuilt the pack's rank model from the save (`allocated + all-skills 1 + mastery bonus + per-skill bonus`, all read out of equipped gear) and hit **six total ranks exactly** — including **EoR rank 26** (15 allocated + 1 all + 10 skill) — then checked every reachable energy row:

| pack row | pack | primary source | verdict |
|---|---|---|---|
| `V15-6` skill_mana_cost_rank26 | 16.0 | `eyeofreckoning1.dbr skillManaCost[25]` | ✅ |
| `V15-7` cost_factor | 0.90 | `compb_sealannihilation.dbr` −10 % | ✅ |
| `V15-8` soulfire_period_s | 0.2 | `eyeofreckoning2.dbr projectilePeriod` | ✅ |
| `V15-10` leech_total / duration / cooldown | 200.0 / 2.0 / 1.0 | `tier2_02f_skill.dbr`, save `devotionLevel = 20` | ✅✅✅ |
| `V15-12` presenceofvirtue1 / 2 / 3 | 220 / 100 / 107 | `[17]` / `[9]` / `[10]` at ranks 18 / 10 / 11 | ✅✅✅ |
| `V15-12` fieldcommand1 / 2 | 205 / 50 | `[13]` / `[11]` at ranks 14 / 12 | ✅✅ |

**Eleven for eleven.** `V15-10`'s grade can move from `DECODED` (a code pointer, `kc2/energy.py:204-217`) to `DB-CITED` + `SAVE-CONFIRMED` with a named record and index.

---

## 8 · ⚑ THE NAMED GAP — what robots.txt put out of reach

**This is a gap, not a silence, and a reader must not read the § 9 negatives as broader than they are.**

| Domain | robots.txt verdict | Action |
|---|---|---|
| ⚑ **`www.grimtools.com`** | `User-agent: ClaudeBot → Disallow: /` (also `Content-Signal: ai-train=no`) | **NOT FETCHED. Zero pages.** |
| ⚑ **`www.reddit.com` / `old.reddit.com`** | `User-agent: * → Disallow: /` | **NOT FETCHED.** r/Grimdawn entirely out of scope. |
| ⚑ **`grimdawn.fandom.com`** | robots.txt **unretrievable** (403 / Cloudflare JS challenge); articles 402/403 | **NOT FETCHED.** Appears only as search-result titles, flagged as such. |
| `forums.crateentertainment.com` | `/t/` topic pages **allowed**; `/search` **disallowed** | Topic pages fetched. ⚑ **The forum's own search was NOT used** — all discovery routed through external search, which will have cost some threads. |
| `www.grimdawn.com` | `/guide/` allowed | Fetched. **Primary.** |
| `steamcommunity.com` | discussions allowed | Fetched. |
| `grimdawn.miraheze.org` | `/wiki/<Article>` allowed | Fetched — used as the datasheet substitute for the two blocked wikis. |
| `grimdawn.wiki.fextralife.com` | NXDOMAIN | Does not exist. |

⚑ **GrimTools is the canonical item / skill / devotion database and the planner every guide links to.** It is the single largest hole in the build-guide leg. Every `grimtools.com/calc/…` or `/db/…` reference encountered is an **unvisited** reference. Any negative in § 9 should be read as *"not found in the sources reachable under robots.txt,"* never as *"does not exist."*

---

## 9 · BUILD-GUIDE ADDENDUM — the community and developer record

### 9.1 ⚑ Two PRIMARY developer statements that corroborate the structural findings

**Zantai (Crate Entertainment)**, v1.2.0.0 patch notes, 11 Nov 2023
`https://forums.crateentertainment.com/t/grim-dawn-version-v1-2-0-0-v1-2-0-1-v1-2-0-2-v1-2-0-3-hotfixes/132117` — TIER: **primary**

> *"Toggled buffs are now automatically toggled on and no longer need to be on the skill bar"*
> ⚑ *"**Toggled buffs no longer have an energy upkeep.** Some Energy Regeneration Constellations have had their Energy Regeneration reduced"*

**This is a developer statement confirming the mechanism I derived from field presence in § 1.1 and § 3 leg 4.** `skillActiveManaCost` is the upkeep field; `presenceofvirtue1_buff.dbr` does not carry it, and carries `characterManaLimitReserve = 220.0` instead. In the current version toggles are paid by **reservation**, not upkeep. Depot verified: `skillActiveManaCost present: False`.

> ⚑ *"**Scales of Ulcama: reduced Energy Regeneration to 2.5** and incrased Health Regeneration to 30"*

Depot: `tier2_02c.dbr :: characterManaRegen = [2.5]`. **Byte-exact.** Contributor #3 now carries a primary dev citation.

Also from the same patch, load-bearing for reading older guides: *"Energy Regeneration Magic Suffixes no longer drop."*

**v1.2.1.0** (13 Jun 2024) and **v1.3.0.0** (22 Jul 2026) contain **no EoR energy-cost change**. v1.3.0.0's EoR line is damage-only: *"increased % Weapon damage scaling with rank to 39%, 50% by max ultimate rank. Added % Crowd Control and % Max Crowd Control resist for the caster while channeling the skill."*

### 9.2 ⚑ The Spirit formula — PRIMARY, and it is the missing term's name

**Crate Entertainment**, official guide, *Character Basics*
`https://www.grimdawn.com/guide/character/character-basics/` — TIER: **primary**

> Spirit *"increases your health by 1.5, magical damage by 0.47%, magical duration damage by 0.5%, **energy by 2 and energy regeneration by 0.01 + 0.26%**"*

Applied in § 5.1. ⚑ **The official guide contains no mention of channelled skills at all, and no statement that regeneration is conditional on anything.**

Corroborating the flat/percent split I used (community explainer, **Gs11**, 3 Jun 2016, `/t/energy-regen-math-for-poor-student/32771`, TIER: tertiary):

> *"[Percent] bonuses boost only your Flat Bonuses by the listed amount. **They have no effect on your Base Energy Regen.**"*
> *"Spirit percent bonus: This is a Percent Bonus equal to spirit/400."*

(spirit/400 = 0.25 %/pt vs Crate's 0.26 %/pt — a rounding or version drift; both recorded, neither preferred.)

*Unreconciled:* a search snippet asserted *"base energy regeneration is 3 for new characters"*; **Ceno** (2 Jun 2016, same thread) states *"Base energy regen at level 1 6.50."* No retrievable source for the former. Both are 2016-era. Neither is used above.

### 9.3 ⚑ THE 2016 TRAP — stated as a trap, because the next person will re-derive it

The only full Tip-the-Scales stat block reachable under robots.txt is Miraheze's, and **the page is stamped v1.0.0.6 / 11 Oct 2016** — two expansions stale. It reads: *"Tip the Scales (**20 %** Chance when Hit)"*, *"**1.5 Second** Skill recharge"*, 15 ranks, rank 15/15 *"**200** Vitality Damage"* and *"**320** Energy Leech over 2 Seconds"*.

**The depot, across all four archives:**

| archive | ranks | chance | trigger | cooldown | **energy leech** max | **vitality** max | ADCtH max |
|---|---|---|---|---|---|---|---|
| `database.arz` | 15 | **33 %** | `HitByEnemy` | **1.0** | 160.0 / 2.0 s | 250.0 | 120 % |
| `GDX1.arz` | **20** | **33 %** | `HitByEnemy` | **1.0** | **200.0 / 2.0 s** | **310.0** | 132 % |
| `GDX2.arz` | **20** | **33 %** | `HitByEnemy` | **1.0** | **200.0 / 2.0 s** | **310.0** | 132 % |
| `GDX3.arz` | **20** | **33 %** | `HitByEnemy` | **1.0** | **200.0 / 2.0 s** | **310.0** | 132 % |

**Unanimous on 33 % / 1.0 s / `HitByEnemy`.** The wiki's 20 % and 1.5 s are pre-expansion values. **Our spec's 33 % and 1.0 s stand.**

⚑ **THE TRAP, and it is a good one.** The research leg correctly warned that *"the wiki's rank-15 figure is 320 Energy Leech; **200 is the rank-15 Vitality Damage**"* — i.e. that our `leech_total = 200.0` might be the wrong stat entirely.

**In the CURRENT game the roles are: energy leech = 200.0, vitality = 310.0. Our 200.0 is correct.**
**Against the 2016 table, `200` genuinely IS the vitality line.**

⚑ **The numbers effectively swapped roles across versions.** A researcher working from that wiki — the only full block a robots-respecting crawl can reach — would have imported **vitality damage as an energy rate**, and it would have looked entirely plausible, because the value they were looking for was sitting one row away wearing the number they expected. **Our figure is right for a reason that has to be written down, or the next commission re-derives the error.** The catch cost nothing and prevented a real one.

**Adjudicating a snippet the research leg correctly refused to assert** (*"33% chance when hit… 310 Vitality Damage and absorbs 400 energy for 2 seconds"*, no fetchable source): **`33 %` ✓ and `310 Vitality` ✓ match the current depot exactly; `400 energy` does NOT** (depot: 200.0 at every rank of every archive). Two of three confirmed, one unmatched.

### 9.4 ⚑ Independent community confirmation that Tip the Scales is HIT-gated

**tqFan**, *"[1.1.9.7] SSF Physical Eye of Reckoning Warlord"*, 4 Jan 2023
`https://forums.crateentertainment.com/t/1-1-9-7-ssf-physical-eye-of-reckoning-warlord-leveling-and-beginner-build-hc-friendly/124405` — TIER: secondary

> *"on the very rare times you don't have Energy and pot's on cooldown — **stand in some DoT for the bar to quickly feel up by proccing Scales**"*

A guide author's documented recovery procedure **while not attacking** is **to get hit**. § 4.1 arrived at from a completely independent direction. It is also evidence that base regen alone is *too slow to be a tactic* — which is a statement about its magnitude, **not** about it being off.

Also from tqFan, a consequence a model should carry: *"when you run out of energy, you lose Beronath conversion aura and need to recast it."*

⚑ **A conflation trap to carry forward:** guides saying *"Scales for energy"* (**fordprefect**, twice, `/t/…/113547`: *"You need Scale for energy regen"*) refer to the **constellation's passive +2.5 /s node**, **not** the proc. fordprefect never binds or discusses Tip the Scales. Reading those as proc endorsements overstates the proc and understates the passive.

### 9.5 Per-tick charging — community-confirmed

**Duck**, Steam, 8 Apr 2019 (`https://steamcommunity.com/app/219990/discussions/0/1812044473326273999/`) — TIER: tertiary:

> *"**It costs X energy per tick**… The total energy per second it costs is divided between the ticks, which is a much more precise answer!"*

**RodHull**, same thread, 7 Apr 2019:

> *"EoR lists its cost as XX per second, but the text states about it draining every 0.2 seconds (or somesuch) at 100% att speed."*

⚑ **The tooltip's "per second" is a DERIVED DISPLAY of a per-tick charge.** Exactly the § 1 structural finding, independently held by the community.

### 9.6 C-3 — a second −10 % source exists; ours is the one in the save

The research leg found **Focusing Prism** (amulet component, `-10% Skill Energy Cost`, Miraheze, rev. 3 Mar 2020) — available to any build, **named by zero EoR Warlord guides**, and actively deprecated for the slot by arivus's 2021 component review. **Our referent used a different −10 % component: Seal of Annihilation** (§ 7), which is in his save.

⚑ **A named FALSE POSITIVE to record.** Oathkeeper's **Reprisal** carries *"-10% Energy Cost"* at rank 1 (→ −27 % at rank 14). **It is a modifier local to Aegis of Menhir**, which is *not allocated on this build at all*. Anyone back-solving `0.90` from an Oathkeeper sheet will find Reprisal first and it will look exactly right. It cannot be the source here.

**Negative confirmed on the candidates the commission named:** Divine Mandate, the Ultos/Ulzaad items and both mastery bars carry **no** energy-cost reduction.

*(Caveat carried from the research leg: no source states the local-vs-global rule for `-% Energy Cost` in words. The local reading follows from Reprisal sitting inside the Aegis of Menhir node chain and from v1.3.0.0's *"Endless Flame: increased base % Energy Cost Reduction by 5%"* being written per-skill. Flagged as inference.)*

### 9.7 The Q3-crux community negative, stated at its true strength

> *"No source claims suppression, the unit conventions and the entire remedy set presuppose continuous regen, and **nobody has ever written it down**."*

**Zero developer statements on channel-state vs regen.** Threads read in full and found silent on it: `/t/channeling-skills-are-underperforming/44664`, `/t/…/35376` (Mechanics 101), `/t/…/99567` (Local and Global Modifiers), `/t/…/32771` (Energy Regen Math), `/t/…/48275` (Sudden Energy problems), `/t/…/136606`, plus five Steam threads.

⚑ **This is the weakest of the four legs, and it does not need to carry weight.** The community's silence is an **unrebutted default**, not a sourced fact. What converts it into a finding is the DBR field scan, the client's minimally-different tooltip pair, and the footage income identity — §§ 3 and 6. **The community assumes it; the data shows it.**

### 9.8 ⚑ THE v1.2.0.0 HARD BREAK — a standing hazard for every future commission on this referent

**v1.2.0.0 (11 Nov 2023) is a discontinuity in the energy record.** It removed toggle upkeep, cut several constellations' energy regeneration, and stopped Energy Regeneration magic suffixes from dropping.

⚑ **Every EoR Warlord guide with a worked energy section is 1.1.9.x (2019–2023) and predates it.** The post-1.2 guides (callie `/t/…/134634`, Feb 2024; Roipu `/t/…/149529`, 2025–26) are near-silent on energy — Roipu's entire treatment is *"Also it costs too much energy to keep spinning!"* plus a potion line.

> **There is no post-1.2 EoR Warlord guide with a worked energy section. That is a hole in the community record, not a hole in the search.**

**Therefore, standing for this referent: primary sources (depot DBRs, client strings, the save, the footage) GOVERN. Build guides are a corroborating layer only, and any guide-sourced number must carry its patch version.** A 1.1.9.x energy figure is not evidence about a 1.3.x referent. Our depot is post-1.2 and the save is post-1.2.

---

## 10 · Knowledge gaps not resolved

| Gap | Status | What was searched |
|---|---|---|
| ⚑ **Base energy regen as a function of level** (the 28.75 /s residual) | **`searched-SOURCE-UNLOCATED`**, with the Spirit half of the formula now named | All 7 ARZ archives (field-name scan, 2 regen fields exist); `gameengine.dbr`; `combatformulas.dbr`; `playerlevels.dbr`; `malepc01`/`femalepc01.dbr`; all 20,394 localization tags; Crate official guide; forum mechanics threads. **The formula is in `Game.dll` and the binary is not mounted.** |
| Any channel-conditional stat rule | ⚑ **CLEAN NEGATIVE** | All four archives by field name; all 20,394 strings by value. None exists. |
| Any energy analogue to Constitution | ⚑ **CLEAN NEGATIVE** | Localization sweep. Health-only. |
| Re-measure of off-channel rate from video | **searched-UNAVAILABLE** | Source MP4 deleted (`/Users/admin/gd-scratch/`). |
| `Game.dll` (binary surface) | **UNAVAILABLE this session** | `/Users/admin/Games/vendor/grim-dawn/` gone; `/Volumes/reincarnated` unmounted; no PE binary on host. |
| GrimTools / Reddit / Fandom | ⚑ **BLOCKED BY robots.txt — NOT a negative** | § 8. |
| Owl constellation's `-% Energy Cost` value | unlocated | Named as existing by one Steam source; value lives on GrimTools (blocked). |
| Save bio field mapping (`physique` / `cunning` / `spirit`) at v8 | ⚑ **UNVERIFIED — flagged, and § 5.1 depends on it** | Our prior art solved v8 drift for the *skills* block, not the *bio* block. Reads physique 74 / cunning 858 / spirit 74, which is an odd allocation for a physical Warlord. **If this mapping is wrong, the 28.75 residual moves.** |
| `tip_the_scales` duration conflation in `devotion.py:59` | reported, unresolved | § 4.4. |

---

## 11 · Advisory to the conductor (routing is gandalf's; nothing folds on this finding alone)

1. **New pack row owed** — Presence of Virtue `characterManaRegen[17] = 10.4 /s`, same record and index the pack already reads for `V15-12`'s reservation.
2. **C-3 closes** on `compb_sealannihilation.dbr :: skillManaCostReduction = 10.0`. Proposed regrade in § 7.
3. **`V15-10` can be regraded** `DECODED` → `DB-CITED` + `SAVE-CONFIRMED` (§ 7.1).
4. **If an off-channel branch is built:** income = the *same* income term as on-channel; drain = **0** (structural). ⚑ **The open parameter is `h` (incoming hits/s), not a channel flag** — and `h` is already registered as `ABS-MONSTER-OFFENSE-NO-DATA-POOL466`.
5. ⚑ **The `−1.03 /s` boot check needs adjudicating against the footage's −73/−82.** That is a design call above my seam.
6. **C-4 is substantially answered as a by-catch** (§ 4): the trigger is verified `HitByEnemy` / 33 %, and the realized-rate function `U(h)` is given. What remains open is `h`.

---

## 12 · Source list

**Primary — shipped game data (read-only, local depots, accessed 2026-09-21):**

- `/Users/admin/depots/219991/24346246/database/database.arz` (34,114 records)
- `/Users/admin/depots/642280/24346246/gdx1/database/GDX1.arz` (18,447)
- `/Users/admin/depots/897670/24346246/gdx2/database/GDX2.arz` (16,451)
- `/Users/admin/depots/2699230/24346246/gdx3/database/GDX3.arz` (24,178)
- `/Users/admin/depots/{642281,897671,2699231}/…/SurvivalMode{1,2,3}.arz` (1,004 / 811 / 1,431)
- 8 × `Text_EN.arc` across the same depots — 20,394 localization tags

**Primary — the save:**

- `agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/player.gdc`, sha256 `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5`

**Primary — developer statements (accessed 2026-09-21):**

- Zantai / Crate Entertainment, v1.2.0.0 patch notes, 11 Nov 2023 — `forums.crateentertainment.com/t/…/132117`
- Crate Entertainment, official guide *Character Basics* — `www.grimdawn.com/guide/character/character-basics/`

**Primary — measured footage (project artifacts):**

- `galadriel/notes/2026-08-25-kc2-mc-md-b4app-2-channel-uptime.md` § 4.4
- `galadriel/notes/2026-08-25-kc2-mc-md-b4app-2b-energy-release.md`
- `galadriel/captures/2026-08-25-md-b4app-2b-energy/work/s2-releases.json`

**Secondary — community guides (tier and version stamped inline in § 9):**

- fordprefect, v1.1.9.4 Gutsmasher Warlord — `/t/…/113547`
- tqFan, v1.1.9.7 SSF Physical EoR Warlord — `/t/…/124405`
- tqFan, energy-leech mechanics — `/t/…/108637`
- sir_spanksalot, v1.1.4.2 DW EoR Warborn Warlord — `/t/…/50454`
- ChthonicSonic, FG Oathkeeper datamine, 8 Dec 2018 — `/t/…/47953`
- arivus, component review, 10 Mar 2021 — `/t/…/108114`
- Ceno / Gs11, energy-regen math, Jun 2016 — `/t/…/32771`

**Tertiary — Steam discussions and Miraheze datasheets:** cited inline. ⚑ **Miraheze pages carry 2016–2021 version stamps; see § 9.3 for why that matters.**

**Project prior art reused unmodified:**

- `research/scripts/gd_arz_adapter_2026_07_24.py` (format truth)
- `research/scripts/gd_arc_reader_2026_07_26.py`
- `legolas/scratch/2026-07-28-gdc-parse-g7/gdc_parse.py`

---

**Filed by:** legolas (UNKNOWN-RESEARCHER), 2026-09-21.
**Routing:** gandalf (conductor). Nothing folds into the oracle or the pack on this finding alone.
