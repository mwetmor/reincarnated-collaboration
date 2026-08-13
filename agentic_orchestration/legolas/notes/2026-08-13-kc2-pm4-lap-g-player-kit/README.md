# KC2-PM4 Lap G — the player's own kit: dashes, potions, circuit-breakers, and the channel

**Seat:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`, ledger **L-6**
**Serves:** charter items **I-2** (kit / dash) and **I-3** (potion / circuit-breaker) — the only
queue items that can reach **T4b**, which has now MISSED twice and is unreachable by any
board-side fold.
**Date:** 2026-08-13 · **Status:** LANDED. **31/31 verification checks PASS, 0 FAIL.**
Read-only throughout. No tuning. No estimate anywhere — every number is a decoded field or an
explicitly DECLARED gap (GL-12).

---

## 0 — The one-paragraph answer

**The sim's player is missing a counterplay layer that is not small, and it is not one mechanism —
it is six.** Matt's actually-played save (which existed on the share and had never been read; Lap A
read the *pristine download*) carries **three independent movement skills** (Vire's Might 3.6 s /
12 m, Rune of Violent Delights 2.5 s / 16 m, and — new in patch 1.3.0.0 and absent from the 2022
build entirely — **Evade, 3.0 s / 10 m, free to every character**), a **12-second 800 + 25 % + 25 %-over-time
health potion**, an **automatic 6,100-point damage shield that fires at 50 % health with 100 %
certainty** (Turtle Shell), a second **2,900-point shield on a 3-second cooldown** that fires on
30 % of hits taken (Arcane Barrier), an **automatic 35 %-of-health heal at 33 % health** (Menhir's
Will), and a **24-second, 10-second-duration +38 % damage / 30-absorb panic button** (Ascension).
Against the sim's wave-160 intake of **20,861 damage over 6.69 s**, the *decoded, measured*
recovery available in that window is **≥ 9,000 absorbed + 7,002 healed** — i.e. **the reference
player had, on the record, roughly 77 % of that intake in pure counterplay he was never given in
the sim.** That is what T4b has been failing on, and it is now substrate rather than testimony.

**Q5 answered flatly and MEASURED:** `eyeofreckoning1.dbr` carries **`canUseWhileMoving = 1`** —
against a template default of `0`, and against a whole-corpus census in which only **4 of 15**
records that declare the field set it TRUE, of which only two are real player skills. **The EoR
channel permits movement by deliberate authoring.** The sim's player, pinned for 3,732 ticks
(GL-12 / R-CPB-4 lineage), is modelling the *opposite* of what the data says.

---

## 1 — ⚑ THE SOURCE MOVED, and this is the lap's first finding

Lap A (2026-08-12) parsed `gdc/_EoRWarlGuts/player.gdc`, sha256 `c8738da3…` — the **2022 forum
download**, extracted from the pristine zip **before first load**. That was correct for Lap A's
charter (establish the build-of-record's sheet). It is the wrong file for *"the kit as PLAYED."*

**Matt's played save is on the share, in two byte-identical copies, and had never been read:**

| file | sha256 | bytes | seed | `expansion_status` |
|---|---|---|---|---|
| `/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/player.gdc` | `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5` | 98,101 | `0x5298565B` | **7** = AoM ǀ FG ǀ **FoA** |
| `/Volumes/reincarnated/GD-matt-test/eor-test-2/save/_EoRWarlGuts/player.gdc` | *(identical)* | 98,101 | — | — |
| `…/lap-a-player-sheet/gdc/_EoRWarlGuts/player.gdc` (pristine, Lap A) | `c8738da3…` | 87,820 | `0x55555555` | 3 = AoM ǀ FG |

**Source of record for this lap: the PLAYED save. The pristine is retained as the cross-check**, and
both are parsed by the same code and diffed field by field (hook (b)).

---

## 2 — ⚑ LAP A's CLIFF C-3 BIT, AND IS NOW CLOSED — the real `.gdc` stream cipher

Lap A's parser handled only the **plaintext** case and said so: the pristine file's seed *is*
`0x55555555`, so `seed ^ 0x55555555 == 0`, the key table is all zeros, and the XOR stream is the
identity. Lap A filed cliff **C-3**: *"Any other GD save would need the real CRC-style key schedule…
it was simply not needed."* **The played save's seed is `0x5298565B`. The cliff bit.**

The schedule, established here **from the bytes**, never spelled from memory:

```
seed = uint32 @0  XOR  0x55555555 ;  key = seed
for i in 0..255:  k = rotate_right_1(k) ;  k = (k * 39916801) mod 2^32 ;  table[i] = k
read_u8 :  v = raw   ^ (key & 0xFF) ;  key ^= table[raw]
read_u32:  v = raw32 ^  key         ;  key ^= table[b]  for each of the 4 RAW bytes
```

Three things were **measured, not assumed**, and each has a falsifier:

* **The round count.** Four candidate schedules (1/2/3/4 rotate-multiply rounds per table entry)
  were run. **All four decode the magic** — the first int uses the initial key, so the table is
  irrelevant there, and a magic check would have passed a wrong schedule. Only **rounds = 1**
  decodes `header_version = 2` *and* the wide-string name `EoRWarlGuts`; the other three desync
  inside the name length. **This is why the magic was not treated as the verification.**
* **Three byte-windows consume without advancing the key**, found by *solving*, not guessing. The
  key error `D = true_key XOR my_key` is **constant** once introduced (both sides update by the
  same `^= table[raw]`), so a run of known plaintext pins `D` exactly. A 16-byte run of zeros at
  file offset 78..93 decoded to a constant `0xd8`, which pins `D`; searching every 1/4/5/8-byte
  window in 64..78 for `XOR table[b] == D` returned **exactly one candidate: bytes 70..73** — the
  post-header int. The same rule then holds for **block lengths** and **block end-markers**.
* **The verification is total, and it is cross-file.** With these rules the played save walks
  **15/15 blocks, every end-marker decodes to 0, terminating at byte 98,101 of 98,101** — and the
  *same code* walks the pristine plaintext save to **87,820/87,820, 15/15 zero markers.** A reader
  tuned to one file does not do that.
* **Two blocks need a resync, and they name themselves.** Blocks 3 (inventory) and 4 (stash) carry
  *nested* length ints, so a blanket key advance over the payload over-bumps. Because the
  end-marker's plaintext is 0, the true key at the marker is exactly the raw marker bytes — the
  walker resyncs there and reports per block whether the blanket skip was `clean`. **On the played
  save 13/15 are clean; the two that are not are 3 and 4, and neither is read by this lap.**
  **Blocks 8 (skills) and 14 (UI settings) — the only two this lap reads — are both `clean`, i.e.
  each independently reproduced its own zero end-marker.**

---

## 3 — Q1 · THE ACTIVE KIT AS PLAYED

**Deliverable: `pm4g_played_kit.csv`** (324 rows; every allocated skill, every devotion node with a
level, every autocast binding, every bar slot). The bar itself is 10 slots:

| ordinal | skill | display name | mastery | rank alloc → **effective** | note |
|---:|---|---|---|---:|---|
| 0 | `playerclass09/viremight1` | **Vire's Might** | Oathkeeper | 1 → **2** | dash · devotion proc **Maul** bound |
| 1 | `playerclass01/warcry1` | **War Cry** | Soldier | 12 → **16** | −29 % enemy damage, 7.5 s cd · **Ulzaad's Decree** bound |
| 2 | `playerclass09/ascension1` | **Ascension** | Oathkeeper | 1 → **2** | 10 s / 24 s cd panic button |
| 3 | `itemskillsgdx2/runes/rush_d203` | **Violent Delights** | *rune, medal slot 14* | — | **second dash**, 2.5 s cd |
| 4 | `playerclass01/blitz1` | **Blitz** | Soldier | 1 → **5** | charge |
| 5 | `default/defaultweaponattack` | default attack | — | 1 | |
| **6** | `playerclass09/eyeofreckoning1` | **Eye of Reckoning** | Oathkeeper | 15 → **16** | **the channel** |
| **7** | `playerclass09/eyeofreckoning1` | **Eye of Reckoning** | Oathkeeper | 15 → **16** | **bound a SECOND time** |
| 8 | `playerclass09/summon_celestialguardian1` | Summon Guardian of Empyrion | Oathkeeper | 1 → **2** | petLimit 2, 20 s cd |
| 9 | `itemskillsgdx1/relics/summondeathstalker` | Summon Deathstalker | *relic, slot 11* | — | petLimit 1, 15 s cd |

Plus **`default/defaultevade`, rank 1, present in the played save's block 8 and ABSENT from the
pristine's** — patch 1.3.0.0's universal dodge. It is not on the numbered bar because in 1.3 it has
its own dedicated input.

**Rank algebra.** `rank_allocated` is MEASURED from block 8. `rank_effective` is DERIVED and its
basis is written into every row: Lap A's camera-measured sheet (frame 512) gives **+1 all skills,
+3 Soldier, +0 Oathkeeper**, so Soldier skills take **+4** and Oathkeeper skills **+1**.
Item-granted, devotion and default skills take **no** rank bonus in GD and are returned unchanged
with that said out loud rather than silently applied.

> **⚑ IS-G1 — a correction against Lap A's own prose.** Lap A's README § 4 states *"Gutsmasher
> grants +4 ranks"* to Eye of Reckoning. **Its own CSV does not support that**: the measured rows
> are `weapon_plus_soldier_all = 2`, `weapon_plus_occultist_all = 2`, `bonus_oathkeeper_skills = 0`,
> `bonus_all_skills = 1`. **EoR's effective rank is 16 (15 + 1), not 19.** This lap uses the CSV
> (measured) and not the prose. Flagged for the conductor because the damage limb rides it.

---

## 4 — Q2 · MOVEMENT — three dashes, and the range field says "Maximum range" in the game's own words

**Deliverable: `pm4g_movement_skills.csv`.** All lengths are metres and all times seconds under the
Lap-F display-contract ruling (`SkillDistanceFormat={%.1f0 {^E}Meter %s1}` — the game prints raw DB
lengths followed by the literal word "Meter"). Nothing is rescaled. Sim tick = 0.08163 s.

| skill | class | **cooldown** | **range** | run-speed mod | impact radius | end radius | mana | ticks (cd) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Vire's Might** (rank 2) | `Skill_AttackPathCharge` | **3.600 s** | **12.0 m** | +250 % | 2.20 m | 3.30 m | 26 | 44.1 |
| **Violent Delights** (rune, medal) | `Skill_AttackPathCharge` | **2.500 s** | **16.0 m** | +300 % | 2.00 m | 3.00 m | 66 | 30.6 |
| **Evade** (1.3.0.0, universal) | `Skill_Evade` | **3.000 s** | **10.0 m** | +250 % | — | — | 0 | 36.8 |
| **Blitz** (rank 5) | `Skill_AttackWeaponCharge` | **3.500 s** | **DECLARED-GAP** | +300 % | — | — | 42 | 42.9 |

**Evidence chain for the range field (hook (c)).** `skill_attackpathcharge.tpl` and
`skill_evade.tpl` both declare

```
waveDistance   real   defaultValue "1.0"   description "Maximum range"
maxMoveRatio   real   defaultValue "1.0"   description "Ratio between absolute and walkable distances"
endRadiusMultiplier real                   description "Multiplier for final radius attack at destination point"
```

and `templatebase/skill_activated.tpl` declares `skillCooldownTime  real  description "Seconds"`.
So the four numbers above are field-for-field, description-for-description measured. `maxMoveRatio`
is **2.0** on both charges and **1.1** on Evade — the walkable-path allowance, which matters if the
sim ever models obstruction.

**⚑ Blitz's range is a DECLARED GAP and the dead end is named.** `Skill_AttackWeaponCharge` declares
**no range field at all** — only `maxDistanceBuffer`, whose description is explicitly about
*monsters*. Blitz carries `distanceProfile = 'Melee'`, and the picklist's six values
(`Melee;Short;Moderate;Long;Maximum;Boss`) match six `gameengine.dbr` scalars **6/6 by name**:

```
meleeRange 1.25 · shortRange 4.75 · moderateRange 9.0 · longRange 15.0 · maximumRange 18.0 · bossRange 32.0
(alongside meleeTargetDistance 2.4000000954 = the sim's own D_ENGAGE_M, and meleeAutoTargetDistance 4.0)
```

A 6/6 name match is strong, but **the engine's use of that join is not decodable from the corpus**,
and it cannot be Blitz's charge distance anyway (Vire's Might is `Long` = 15.0 while its explicit
`waveDistance` is 12.0; the rune is `Long` while its `waveDistance` is 16.0 — the two do not agree
in either direction). **Declared, not estimated.** If a fold needs Blitz's reach, the named
escalation is a camera measure off Matt's video.

**Riders** (all per-rank, indexed at the effective rank, in the CSV): Vire's Might carries
`offensivePhysicalMin 73`, a 2 s physical DoT `40`, `offensiveTauntMin 25`, plus the two allocated
modifiers (fire 27, fire-DoT 29 over 3 s, −10 % total speed for 2 s from `viremight2`; bleed 51 over
3 s from `viremight3`). The rune carries **350 bleed over 2 s** and −20 % attack speed. Blitz
carries `offensivePhysicalMin 190`, knockdown, and via `blitz2` a 3 s 120 physical DoT and −130 DA.
**Every dash in this kit is also a damage and a debuff event** — which is the part the sim's
"no movement skill" simplification silently deletes twice over.

---

## 5 — Q3 · POTIONS — ⚑ the whole system changed under the save, and the numbers still agree

**Deliverable: `pm4g_consumables.csv` (56 rows).** This is the finding I did not expect.

**The 2022 save's own potion records do not exist in the patch Matt played.** The pristine save's
inventory names `records/items/misc/potions/potion_healtha01.dbr` and `…/potion_energya01.dbr`.
**Neither is present in any of the eight Edition-III archives.** The only `OneShot_PotionHealth`
records in the entire corpus are four `_old`-prefixed, deprecated ones.

**In patch 1.3.0.0 (Fangs of Asterkarn) potions became SKILLS, not items** — and the played save
proves the character has them:

| record | class | flat | instant % | over-time % | cooldown | charges | cast |
|---|---|---:|---:|---:|---:|---:|---|
| `skills/default/defaulthealthpotion` | `Skill_ChargePotion` | **800** | **25 %** | — | **12.0 s** | 1 | `instantCast` |
| `skills/default/defaultmanapotion` | `Skill_ChargePotion` | 120 | 15 % | — | 12.0 s | 1 | `instantCast` |
| `…/potionmodifiers/healthpotion_healovertime` **← ALLOCATED, rank 1** | `Skill_PotionModifier` | — | — | **25 %** | — | — | `ignoreDisruption` |

**Hook (d) — the cross-check across two independent record paths — PASSES, and then a third
surface corroborates it:**

* `defaulthealthpotion` (gdx3 **skill**) vs `_oldpotion_healtha01` (base **item**, deprecated):
  `skillLifeBonus 800 == bonusLifePoints 800` · `skillLifePercent 25 == bonusLifePercent 25` ·
  `skillCooldownTime 12.0 == useDelayTime 12.0`. **EXACT on all three.**
* Add the one allocated modifier and the reconstruction is term-for-term complete:
  **800 flat + 25 % instant + 25 % over-time on a 12 s cooldown** — which is *exactly* the 2022 item
  potion, `bonusLifePercentSlow` included. Crate ported the health potion, did not rebalance it,
  and made heal-over-time the default-unlocked modifier.
* **The ENERGY potion DIFFERS and is reported, not averaged** (charter law): skill `120 / 15 % /
  12 s` vs item `250 / 35 % / 25 s`. The energy potion *was* rebalanced — weaker per use, cooldown
  halved.

> **⚑ A by-product decode that closes G3's ambiguity from the other side.** The 1.3-era block-8
> entry gained exactly one byte over the 2022 layout (27 → 28 after the record path). All 10
> insertion points were tried; two parse (the new byte is adjacent to `enabled`). Its **meaning**
> is now measured anyway: `b2 == 1` on **exactly 38 of the 40** potion-modifier records and on
> **zero** of the other 327 rows in the block; the two exceptions are the health+energy
> heal-over-time pair. **`b2` is the FoA potion-modifier LOCK flag**, and the one modifier this
> character has *selected* is `healthpotion_healovertime`.

**What is NOT decodable, and is declared:** the potion **stack / charge count at the moment of
death** lives in block 3 (inventory), which this lap does not parse (cliff C-G6, inherited from Lap
A's C-4). For I-3 the sim needs the *rate* (one use per 12 s, one charge) and the *magnitude*
(800 + 25 % instant + 25 % over-time = **800 + 0.25 × 20,005 + 0.25 × 20,005 ≈ 10,802 hp per use**
against the measured 20,005 HP bar), not the stack depth — Crucible resupplies and Matt was not
observed running dry.

---

## 6 — Q4 · DEFENSIVE ACTIVES AND CIRCUIT-BREAKERS — six of them, two fully automatic

**Deliverable: `pm4g_defensive_actives.csv` (21 rows).** Ranks are the measured effective ranks;
devotion-proc ranks are the MEASURED `devotion_level` straight out of block 8.

| what | record | trigger | chance | magnitude | duration | **cooldown** |
|---|---|---|---:|---|---:|---:|
| **Turtle Shell** | `devotion/tier1_29e_skill` @ dev **25** | **LowHealth ≤ 50 %** | **100 %** | **6,100 damage absorbed** | — | **8.0 s** |
| **Arcane Barrier** | `devotion/tier2_17c_skill` @ dev **20** | **HitByEnemy** | 30 % | **2,900 absorbed** (elemental/aether/chaos/vitality/poison qualifiers) | — | **3.0 s** |
| **Menhir's Will** | `playerclass01/willtolive1` rank **5** | **LowHealth ≤ 33 %** | auto | **35 % of health healed** + **120 hp/s regen** | 10.0 s | **21.0 s** |
| **Ascension** | `playerclass09/ascension1` rank **2** | manual | — | **30 absorb**, **+38 % all damage**, +39 % retaliation | 10.0 s | **24.0 s** |
| **War Cry** | `playerclass01/warcry1` rank **16** | manual | — | **−29 % enemy damage** for 5 s, 33 % current-life dmg, 18 m radius, −45 phys res | 5.0 s | **7.5 s** |
| **Ulzaad's Decree** | `devotion/tier2_37d_skill` @ dev **20** | AttackEnemy | 20 % | +200 % phys/pierce, 190 flat protection | 10.0 s | **22.0 s** |
| **Fighting Spirit** | `playerclass01/fightingspirit1` rank **5** | on-hit | **30 %** | +95 % total damage, +108 OA | 6.2 s | 5.0 s |
| **Tip the Scales** | `devotion/tier2_02f_skill` @ dev **20** | HitByEnemy | 33 % | **132 life leech**, 310 vitality, −20 all res on target | — | **1.0 s** |
| **Maul** | `devotion/tier2_05f_skill` @ dev **20** (on Vire's Might) | AttackEnemy | 20 % | −35 % target protection, **45 life leech** | 5.0 s | — |
| **Assassin's Mark** | `devotion/tier1_08e_skill` @ dev **25** (on **EoR**) | **AttackEnemyCrit** | **100 %** | debuff | 18.0 s | — |
| **Shifting Sands** | `devotion/tier3_20e_skill` @ dev **15** | AttackEnemy | 20 % | 5 projectiles, fumble + −140 OA | 1.0 s | 0.5 s |

Trigger semantics are decoded from the bound controller records, not inferred —
`skillautocastcontroller.tpl` declares `triggerType` (picklist:
`OnEquip;OnKill;LowHealth;LowMana;AttackEnemy;CastBuff;CastDebuf;HitByEnemy;HitByMelee;HitByProjectile;HitByCrit;AttackEnemyCrit;Block`),
`triggerParam`, `chanceToRun`, `targetType`, `autoTargetRadius`. E.g. Turtle Shell's controller is
`cast_@selfat50%health_100%.dbr` = `{triggerType: LowHealth, triggerParam: 50.0, chanceToRun: 100,
targetType: Self}`.

Also carried (passive, always-on, in the CSV): **Field Command** rank 14 (+100 OA/+100 DA, +22 %
armour absorption, 12 m aura), **Presence of Virtue** rank 13, **Divine Mandate** rank 13,
**Presence of Might** (Seal of Might component).

### ⚑ 6.1 — What this means for the wave-160 residual, arithmetically

The sim's terminal wave: **20,861 damage over 6.69 s / 82 ticks**, player HP bar **20,005**, zero
player damage rows. Against that window, the *measured* counterplay the reference player carried:

| layer | availability in a 6.69 s window | absorbed / restored |
|---|---|---:|
| Turtle Shell (auto @50 % HP, 8 s cd) | fires **once**, guaranteed | **6,100** |
| Arcane Barrier (30 % of hits, 3 s cd) | fires **≥ 2×** at this hit density | **≥ 5,800** |
| Menhir's Will (auto @33 % HP, 21 s cd) | fires once | **7,002** (35 % of 20,005) |
| Health potion (12 s cd, 1 charge) | fires once | **≈ 10,802** (800 + 25 % + 25 % over-time) |
| Ascension (manual, 24 s cd) | available | 30 absorb + damage window |
| War Cry (manual, 7.5 s cd) | available | **−29 % on all enemy damage for 5 s** |

**Σ of the automatic layers alone ≈ 18,900 against a 20,861 intake — and that is before the potion,
before War Cry's −29 %, and before three dashes at 10–16 m simply removing the player from the
pack.** T4b did not fail because the board was wrong. It failed because the player had no answer,
and the reference player had six.

---

## 7 — Q5 · CHANNEL-MOVEMENT — **MEASURED, and the corpus discriminates it**

**`records/skills/playerclass09/eyeofreckoning1.dbr`:**

| field | value | template declaration |
|---|---|---|
| `Class` | `Skill_AttackRadiusSpin` | `skill_attackradiusspin.tpl` → includes `skillchanneled.tpl` |
| **`canUseWhileMoving`** | **`1` (true)** | `skillchanneled.tpl`, `bool`, **default `0`**, description empty |
| `delayMovement` | `1` (true) | `skill_attackradiusspin.tpl`, `bool`, default `0`, **description EMPTY** |
| `rotationSpeedMultiplier` | **0.35** | `skill_attackradiusspin.tpl`, *"Multiplier applied to player rotation speed while skill is active"* |
| `duration` | 0.25 s | `skillchanneled.tpl`, default 0.2 |
| `useResetsDuration` | true | `skillchanneled.tpl`, default 1 |
| `timeBetweenAttacks` | 200 (ms) | *"Time between hits to enemies along the path"* |
| `skillTargetRadius` | 3.0 m | = the sim's `EOR_RADIUS_M`, unconverted |
| `characterRunSpeedModifier` | **absent / 0** | — |
| `skillCooldownTime` · `instantCast` · `forceMovement` | **all absent** | — |

**Verdict, in three clauses, each with its grade:**

1. **MEASURED — the channel permits movement.** `canUseWhileMoving = 1` against a template default
   of `0`. **Deliverable `pm4g_channel_census.csv`:** across the entire corpus only **15** skill
   records declare the field at all; **11 set it FALSE and 4 set it TRUE** — and two of the four
   are developer base-templates. The only two *real* records that set it are
   **`playerclass09/eyeofreckoning1`** and `itemskillsgdx2/relics/hungeringreach`. Movement while
   channelling EoR is a deliberate, rare authoring decision, not a default.
2. **MEASURED-ABSENT — there is no movement-speed penalty on the skill.** EoR declares no
   `characterRunSpeed*` field. Whatever the engine does to speed while channelling, **it is not in
   this record**, and the sim must not invent one.
3. **What *is* penalised is TURNING, by a factor of 0.35** — `rotationSpeedMultiplier`, with an
   explicit template description. That is the measured cost of channelling: you may move, but you
   re-aim at roughly a third speed. (This is the same family of fact the R-CPB-4 engine routing was
   asking for.)

**DECLARED-GAP C-G3:** `delayMovement`'s template description is **empty**, and whether *casting
another skill* (a dash, a potion) **breaks** the channel is engine-internal — no field in the
corpus expresses it. None of the four movement skills declares any exclusion field
(`exclusiveSkill`, `skillDependancy`, `canUseWhileMoving` all absent/false on all four), so the
data offers no evidence of mutual exclusion; **absence of a field is not evidence of independence,
and it is reported as a gap rather than resolved.**

---

## 8 — The four pre-named verification hooks

All four were named in the commission **before** the decode ran. **31/31 checks PASS.**
Full machine output: `pm4g_verify_summary.json`.

**(a) Kit coverage — every quickbar slot accounted.** Block-8 declared 367 == parsed 367. Binding
ordinals contiguous `[0..9]`. 10/10 bound slots resolve to a corpus record. Both item-skill slots
carry their item record and equip location (`rush_d203 ← d203_rune @14` = medal;
`summondeathstalker ← d114_relic @11` = relic — **both agree with Lap A's independently-recovered
equipment array**). 324/324 kit rows carry an engine `Class`.
**Plus (a+):** the 1.3 extra block-8 byte decoded as the potion-modifier lock flag, 38/40 exact.

**(b) Cross-check vs the build guide — followed / deviated per slot.** The governing ruling is
**R-V3-2** (playtest directions v3 § 2): *savefile-primary*, and the forum post states the pristine
zip **is** the `b28gD0KN` character. grimtools is robots-blocked, so the decidable cross-check is
played-save vs build-of-record-savefile:

* **88 allocated skills, ZERO rank deltas.** Matt did not respec.
* **285 devotion nodes, ZERO deltas.**
* **7/7 devotion-proc bindings identical.** The playtest directions flagged a real risk — patch
  v1.2.1.5 ran a one-time reset that unassigned Celestial Powers from two-handed-weapon-granted
  skills, and Gutsmasher is a two-hander. **It did not materialise** (or Matt re-bound exactly):
  `viremight1 ← Maul`, `warcry1 ← Ulzaad's Decree`, `divinemandate1 ← Arcane Barrier`,
  `presenceofvirtue1 ← Tip the Scales`, `summon_celestialguardian1 ← Shifting Sands`,
  `fieldcommand1 ← Turtle Shell`, `eyeofreckoning1 ← Assassin's Mark`.
* **The bar changed, and the change is coherent:** 13 slots → 10. **Dropped:** Field Command,
  Divine Mandate, Presence of Virtue, Presence of Might — and the check proves *all four are
  `Skill_BuffRadiusToggled` / `Skill_BuffSelfToggled`*, i.e. passive/toggled auras that need no
  activation. **Added: none. Eye of Reckoning went from 1 slot to 2.** Matt kept every active and
  cleared the passives off the bar. **Verdict: FOLLOWED, with a bar-layout deviation that removes
  no capability.**

**(c) The dash's cooldown and range with `.dbr` field evidence.** Three PASS rows, each quoting the
field, its type, its template and its description verbatim (§ 4). Blitz's gap PASSES as a *declared*
gap with its dead end named.

**(d) Potion heal magnitude across two independent record paths.** PASS (§ 5), with the third-surface
corroboration and the energy-potion divergence reported rather than averaged.

---

## 9 — Defects, cliffs and self-corrections (Discipline #11)

| id | what |
|---|---|
| **IS-G1** | **Against Lap A's own prose:** "Gutsmasher grants +4 ranks" to EoR is unsupported by Lap A's measured CSV. EoR effective rank is **16**, not 19. The damage limb rides this. |
| **IS-G2** | **Against the run, not one lap:** Matt's played save has been on the share since 2026-08-05 and no lap read it. Every player-side claim in PM-2/PM-3/PM-4 to date was made against the *pristine* file. The two agree on skills and devotions (hook (b)) — but the pristine has **no `defaultevade`, no potion skills, and a different bar**, so the played file was load-bearing all along. |
| **IS-G3** | Lap A reported `item_skill_desync_at_index: 0` on block 8's item-skill sub-list. **This lap reproduces the desync on BOTH saves** and declares that sub-record layout unresolved. The *count* (2) reads fine; the entries do not. Not load-bearing — the item skills the kit uses arrive via block 14 with their item records attached. |
| **C-G1** | **Block-14 slot → physical key/mouse-button mapping: DECLARED-GAP.** The per-slot trailer is not fixed-width (13 bytes on most, 17 or 21 on `ascension1` / `eyeofreckoning1` / the rune, with variable-length `0xFFFFFFFF` runs). Four fixed-grammar hypotheses were built and **all four falsified**. What is emitted — record, ordinal, item-skill byte, item record, equip location — is directly read. Escalation if ever needed: a camera read of the bar from Matt's video. |
| **C-G2** | The 1.3 block-8 extra byte's *position* is ambiguous between two adjacent slots (§ 2 / G3). Its *meaning* is nonetheless measured (§ 5 by-product). Nothing load-bearing depends on the position. |
| **C-G3** | **Whether casting a skill breaks the EoR channel is engine-internal** — no corpus field expresses it. Declared. |
| **C-G4** | Whether Matt had *unlocked* additional potion containers/modifiers beyond the default is answered for the modifiers (block 8: only `healthpotion_healovertime` allocated) but the three **containers** all sit at rank 0, so the base cooldown/charges apply — i.e. **12 s / 1 charge**, no flask or tincture discount. |
| **C-G5** | Blitz's charge range (§ 4). |
| **C-G6** | **Block 3 (inventory) is not parsed** — inherited from Lap A's C-4 — so potion *stack depth at death* is unread. The rate and magnitude, which are what I-3 needs, are unaffected. |
| **C-G7** | `defaultevade` is **not** on the numbered bar in block 14. Whether it was *used* is a video question, not a save question; Matt's testimony (*"ALOT of dashing"*) is the only evidence of use and it is testimony, not measurement. |

**Two things I went looking for and did not find**, reported so nobody re-runs them: (i) a
`skillTargetRadius`-style range field anywhere on `Skill_AttackWeaponCharge`'s include closure —
there is none; (ii) any corpus field expressing channel-interrupt-on-cast — there is none.

---

## 10 — What the sim can take from this, and what it must not

**Directly consumable, MEASURED, unit-compatible with the sim's own space:** every cooldown in
seconds, every range in metres, every magnitude either flat or as a fraction of the measured 20,005
HP bar, every trigger as a `(triggerType, triggerParam, chanceToRun)` triple. All four CSVs are
per-record with an explicit `grade` column.

**What must NOT be taken:** any binding-to-physical-key inference (C-G1), Blitz's range (C-G5),
channel-interrupt semantics (C-G3), potion stack depth (C-G6). This lap rules **none** of the
model questions — whether the sim's player *should* dash, *when* he potions, whether the shields
stack — those are gamora's fold and the conductor's ruling, exactly as Lap D/E/F left their limbs.

**The limb legolas explicitly refuses to rule** (the C-F1 precedent): **the counterplay POLICY.**
The data says the player had three dashes, a potion, two automatic shields, an automatic heal and
two manual buttons. It does not say how a human used them, and a *policy* is a model choice, not a
decode. If the conductor wants a bound rather than a policy, the honest one is the arithmetic in
§ 6.1 — an upper bound on recoverable damage in the terminal window, computed only from cooldowns
and magnitudes that are on the record.

---

## 11 — Files and digests

| file | sha256 | rows |
|---|---|---:|
| `pm4g_played_kit.csv` | `2fd5a34792b96125bd55a40891dfd65cdeb43c385c6ef06607486342d53ce0b3` | 324 |
| `pm4g_movement_skills.csv` | `9db4c9b1bbf0c5a0813a7afbe6724709df4a58f21f8c499d7f6169b76a6e3d2e` | 4 |
| `pm4g_consumables.csv` | `6956bfcbf0b02020d4404633cb11c71f0744dee2e902130648199119ac0c1797` | 76 |
| `pm4g_defensive_actives.csv` | `0cdfd3af9a22e2d6d7de59ca0b8238f0e2c04c64192a16dee894ef71ae0be306` | 21 |
| `pm4g_field_evidence.csv` | `11ec85bb968e861bc01f7286f358988aa9e4fc9b3dfe18bdd920eff43d79c169` | 44 |
| `pm4g_channel_census.csv` | `fda0f72b00e61021082fef88c584e96fd72ba8cfc6415bdf5520356acdf5e977` | 15 |
| `pm4g_emit_summary.json` | — | provenance, save diff, digests |
| `pm4g_verify_summary.json` | — | 31 checks, 31 PASS / 0 FAIL |

The authoritative digest for every file is `pm4g_emit_summary.json → digests`, which the verifier
re-computes and compares byte-for-byte; the table above is a convenience copy.

**Instruments** (in `agentic_orchestration/research/scripts/`):
`pm4g_lib_2026_08_13.py` (the `.gdc` cipher + block walker + rank algebra + tag reader) ·
`pm4g_emit_2026_08_13.py` · `pm4g_verify_2026_08_13.py`.
They import Lap D's ruled `.arz` reader (`E3.winner`, whole-record replacement) and Lap F's
`templates.arc` reader unchanged — **no chain is re-implemented.**

**Sources, all read-only:** the two `player.gdc` files above ·
`/Users/admin/Games/vendor/grim-dawn-edition-III-20260808` (8 archives) ·
`/Volumes/reincarnated/agent-prompts/2026-08-01-eor-warlord-playtest-directions-v3.md` (the
build-guide doc of record; its § 2 R-V3-2 ruling is what makes hook (b) decidable) ·
Lap A's `measured-player-sheet.csv` (skill-rank bonuses only).

---

*Filed by legolas (UNKNOWN-RESEARCHER), 2026-08-13, under the KC2-PM4 charter, Lap G. Read-only on
`/Volumes/reincarnated/`, on the vendor corpus and on every prior emission. No engine-repo writes.
No constant fitted toward any band.*
