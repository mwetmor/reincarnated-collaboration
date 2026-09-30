# C-11a — the SCOPE of the global-magnitude attribute limb, and what a hero "aura" actually is

**Date:** 2026-09-29 · **Author:** legolas (UNKNOWN-RESEARCHER) · **Commission:** C-11a, issued by
the KC2-PLAY conductor (gandalf) from gamora's C-11 decomposition (engine `14d97484`).
**Boundary:** the oracle's sealed stack takes **×3.58** the referent's landed intake on w151–159.
The single largest term is the **global-magnitude ATTRIBUTE limb** (ρ 0.177, share 1.36 of 3.58).
Its equation and the body attributes are SOURCED; **its SKILL SCOPE was not.**
**Mode:** read-only. No sealed cell opened, re-run or moved. Nothing fitted, nothing tuned (Law 3).
**Surfaces:** Crate authoring templates (`…/2026-08-08-kc2-halt-bundle/tpl/`, 808 files) · Mac
Edition-II depot `.arz` (`~/depots/…/24346246/`, CRUCIBLE precedence KP-79) · **Edition-IV binary**
`~/Games/vendor/grim-dawn-edition-IV-20260929/x64/Game.dll` (build 24825149, sha256
`07775a29…`, post-referent — **every byte-level row below is labelled Edition-IV**).

---

## 0 · VERDICT IN ONE PARAGRAPH

The attribute limb's scope is **not decided by the skill kind at all.** In the engine it is decided
by a **single boolean stored at offset `+0x10` of each runtime damage attribute**, set by whichever
`AddDamageToAccumulator` producer minted that damage row, and read by exactly six
`CombatAttribute…::Process` functions which are the only places in `Game.dll` where
`combatformulas`' damage equations are ever applied. **Every `DamageAttribute*` producer sets it to
1. Every `RetaliationAttribute*` damage producer sets it to 0.** So: **aura-granted damage, procs,
attacks, casts, leech, mana-burn and DoTs are ALL attribute-scaled; RETALIATION IS NOT.** The
oracle applies the limb to retaliation and should not. Separately — and this is the larger finding
— ⚑ **the three hero "aura" records the oracle fires as damage sources are not damage sources.**
`arcane_elementalaura_buff`, `vampiric_vampireaura_buff` and `eldritcharmor_enchantedaura_buff` are
`SkillBuff_Passive` records reached through `Skill_BuffRadiusToggled`: toggled radius **BUFFS** that
grant flat damage, leech and *resistances* to bodies inside 12 m / 10 m. **They have no pulse, no
tick rate and deal no damage of their own.** M_inst does **not** double-count against the attribute
limb — but the per-element own-modifier probably does, in a way nobody has priced.

| question | answer | grade |
|---|---|---|
| **L-C11-1 (a) aura pulses** | scaled **if** the row is a `DamageAttribute*` row — but see L-C11-4: the Crucible hero auras have no damage rows | **BYTE-DECODED (A)**, Edition-IV |
| **L-C11-1 (b) procs / on-hit** | **SCALED.** No proc-specific producer exists; procs mint ordinary `DamageAttributeAbs*` rows (flag 1) | **BYTE-DECODED (A)**, Edition-IV |
| **L-C11-1 (c) retaliation** | ⚑ **NOT SCALED.** Three `RetaliationAttribute*` producers store flag **0** | **BYTE-DECODED-EXACT (A)**, Edition-IV |
| **L-C11-1 (d) attacks / casts** | **SCALED** (flag 1) | **BYTE-DECODED (A)**, Edition-IV |
| **L-C11-1 per damage family?** | **YES — five families, five divisors**, and two of the oracle's are wrong | **DB-SOURCED-VERBATIM (A)**, Edition-II |
| **L-C11-3 M_inst double-count** | **NO.** `CombatAttributeTotalDamageMod`'s per-attribute `Execute` is the folded no-op; M_inst never touches a damage row's value. Both apply, at different layers | **BYTE-DECODED (A−)**, Edition-IV |
| **L-C11-4 hero aura pulse semantics** | ⚑ **THERE IS NO PULSE.** Toggled radius buff; `Skill_BuffRadiusToggled` → `SkillBuff_Passive`; grants, not damage | **DB-SOURCED-EXACT (A)**, Edition-II |
| **L-C11-2 body dex/int lineage** | **NOT PURSUED** — not cheap; commission made it conditional |

---

## 1 · THE EQUATIONS, VERBATIM (Edition-II, `records/game/combatformulas.dbr`)

```
physicalDamageEquation          = (physicalDamageDV*((dexterityDV/245)+1))
pierceDamageEquation            = pierceDamageDV*((dexterityDV/245)+1)
physicalDurationDamageEquation  = (physicalDamageDV*((dexterityDV/215)+1))
magicalDamageEquation           = magicalDamageDV*((intelligenceDV/215)+1)
magicalDurationDamageEquation   = magicalDamageDV*((intelligenceDV/200)+1)
physicalDamagePercentage        = (physicalDamageDV*((dexterityDV/245)+1))
physicalDamageBonus             = 0
```

Template `combatequations.tpl` carries Crate's own descriptions:
`physicalDurationDamageEquation` — *"Internal trauma and bleed damage adjustment"*;
`physicalDamagePercentage` / `physicalDamageBonus` — *"Only for char sheet cunning dmg"*.

**Two consequences the oracle does not have.**
1. **The families are keyed on the DAMAGE TYPE, never on the skill.** There is no retaliation
   equation, no aura equation, no proc equation. The scope question therefore cannot be answered
   from the records at all — it lives in the application site, which is § 2.
2. ⚑ **The oracle's duration divisors are wrong.** Bleed / internal trauma is **dex/215**, not
   dex/245; burn / frostburn / electrocute / poison / vitality-decay is **int/200**, not int/215.
   Priced in § 5 (P3). It is worth nothing, and that is a result.

Crate's own client strings corroborate the family split (Edition-II `tags_ui.txt`):
`tagCharAttributeDescription01` — Cunning *"increasing physical, pierce, bleed and internal trauma
damage"*; `tagCharAttributeDescription03` — Spirit *"magnifies the damage of magical attacks."*
**Note the tag says "attacks" and the DB says bleed and internal trauma — the client string is
loose and must not be read as a scope statement.** That is why this lap went to the binary.

---

## 2 · THE APPLICATION SITE — the scope is one boolean (Edition-IV, `x64/Game.dll`)

`x64/Game.dll` exports **25,100 decorated C++ symbols**. That is what made this decode possible and
it is the durable lane finding of this commission (§ 7).

**Every damage equation is applied in exactly six functions**, found by scanning `.text` for the
`Character`-relative displacements of the equation slots (`Character+0x530` is the embedded
`CombatManager`; `+0x1f0/0x208/0x210/0x218/0x220` are its equation objects, stored by
`CombatManager::LoadRecord` at `0x180109080`):

| function | equation read | `Character` disp |
|---|---|---|
| `CombatAttributeDamage_BasePhysical::Process` `0x180103930` | physical **and** pierce | `+0x720`, `+0x740` |
| `CombatAttributeDamage_BonusPhysical::Process` `0x1801046d0` | physical | `+0x720` |
| `CombatAttributeAbsDamage::Process` `0x180100390` | pierce | `+0x740` |
| `CombatAttributeAbsDamageElemental::Process` `0x180100a50` | magical | `+0x748` |
| `CombatAttributeDurDamage::Process` `0x180100e70` | physical-duration | `+0x738` |
| `CombatAttributeDurDamageElemental::Process` `0x1801015e0` | magical-duration | `+0x750` |

**All six open with the identical gate:** `cmp byte ptr [rcx + 0x10], 0` → `je` past the whole
equation block. The byte at `+0x10` is set by the constructor
(`??0CombatAttributeDamage_BasePhysical@GAME@@QEAA@W4CombatAttributeType@1@MMMM_NM@Z`, `0x1801036c0`:
`movzx eax, byte ptr [rsp+0x38]` → `mov byte ptr [rcx+0x10], al`) — i.e. it is the ctor's `_N`
(bool) parameter. **The attribute limb is opt-in per damage row.**

### 2.1 · Who sets it — the scope table

Producers enumerated by disassembling every export matching `AddDamageToAccumulator` and reading
its store to `[reg+0x10]`:

| producer | flag | meaning |
|---|---|---|
| `DamageAttributeAbs::AddDamageToAccumulator` `0x18017a670` | **1** | **all flat skill/item damage** — this is the aura-granted, proc, attack and cast path |
| `DamageAttributeAbsBaseElemental` / `…BonusElemental` `0x18017c140` | **1** | elemental base + bonus |
| `DamageAttribute_BasePhysical` `0x18018cf80` · `DamageAttribute_Physical` `0x18018ef40` · `DamageAttributeAbs_BonusPhysical` `0x18018f610` | **1** | physical legs |
| `DamageAttributeDur` `0x18017d170` · `DamageAttributeDurBaseElemental`/`…Bonus` `0x18017f2c0` | **1** | **DoTs** |
| `DamageAttributeAbs_LifeLeech` `0x180187420` · `…_ManaBurn` `0x18018fc50` · `…_PercentCurrentLife` `0x180186930` · `…_Disruption` · `…_Convert` · `…_Confusion` · `…_Fear` · `…_Taunt` | **1** | leech, burn, %-life, control |
| `DamageAttributeReflex` `0x1801810a0` | **1** | reflex |
| ⚑ `RetaliationAttributeAbs::AddDamageToAccumulator` `0x18041a3d0` | **0** *(`xor ecx,ecx` → `mov byte ptr [rbx+0x10], cl`)* | **retaliation, all elemental** |
| ⚑ `RetaliationAttributeAbs_Physical` `0x18041a650` | **0** | **retaliation physical** |
| ⚑ `RetaliationAttributeDurBonus` `0x18041b210` | **0** | **retaliation DoTs** |

*(`RetaliationAttributeAbs_Confusion/_Convert/_Fear/_PercentCurrentLife` share an address with their
`DamageAttributeAbs_*` twins — identical-COMDAT folding of control-effect code that carries no
damage value. They are not counter-evidence.)*

**There is no aura producer and no proc producer.** A skill's `Parameters_Offensive` rows — whether
the skill is `Skill_Attack*`, `Skill_Buff*`, `Skill_OnHit*` or a secondary — become
`DamageAttribute*` objects and carry flag 1. **Retaliation is the single exception in the engine.**

### 2.2 · Corroborating structure

`CombatManager::TakeAttack` (`0x18010a650`) emits all of
`combatType = Melee Attack / Ranged Attack / Retaliation Attack / Debuff Attack / Reflection Attack
/ Direct Attack` from **one** routine — so retaliation is not on a separate damage pipeline; it is
the same pipeline carrying rows minted with the flag off. `SkillManager` keeps the two collection
paths separate by name: `CollectAvailableOffensiveDamageAttributes` vs
`CollectAvailableRetaliationAttributes`.

### 2.3 · ⚑ A composition finding nobody asked for, and it may be the bigger one

Inside `CombatAttributeDamage_BasePhysical::Process` the per-element percent modifier (damage-attr
`+0x48`) is applied to the **UNSCALED** base and then **ADDED** to the equation's output:

```
xmm8 = |base| * [attr+0x48] * 0.01          ; computed BEFORE the equation   (0x180103a1c–0x180103a34)
… if flag: [attr+0x20] = physicalDamageEquation(base)                        (0x180103a45–0x180103a77)
xmm8 += [attr+0x20]  →  [attr+0x20]                                          (0x180103afe, 0x180103b22)
```

i.e. **`total = base·a + base·own/100`, not `base·a·(1 + own/100)`.** (`0.01` and the `0x7fffffff`
abs-mask and the `100.0` pierce-ratio clamp were read from `.rdata` and confirmed.) The same block
also shows the physical row being split by `offensivePierceRatio` (damage-attr `+0x2c`, clamped
0–100) into a physical part taking the dex/245 physical equation and a pierce part taking the
dex/245 pierce equation — which is why one `Process` reads two equations.

**Grade B on the mapping of `+0x48` to `offensivePhysicalModifier` by name** — `+0x48` is set after
construction, by the modifier pass, and I did not pin which modifier class writes it. **Grade A on
the FORM** (additive against an unscaled base): that is plain in the instruction order. Priced at
P4 in § 5, and it is the second-largest number in this note.

---

## 3 · L-C11-3 — M_inst vs the attribute limb: no double-count

`CombatAttributeAccumulator::ModifyDamage` (`0x1801061c0`) walks the modifier list and calls
`modifier->vtbl[+0x40](damageAttribute, region)` on every damage row. **`CombatAttributeTotalDamageMod`'s
slot `+0x40` is `0x180015880`** — the identical-COMDAT-folded empty stub shared by hundreds of
no-op virtuals. **So the `offensiveTotalDamageModifier` class never modifies a damage row's value.**
It is consumed at the total layer (`CombatAttributeAccumulator::GetTotalDamageModifierType`,
`CombatManager::ContributeDamageMultiplier`, `CombatManager::CalculateDamageModifier`).

**Answer: GD applies BOTH to the same packet, at two different layers, and they are not the same
term. The oracle's composition of M_inst against the attribute limb is not a double-count.**
Grade A−: I proved TotalDamageMod's *absence* from the per-attribute path; I did not trace its
positive application site to the arithmetic form. That is the one loose end in this answer.

---

## 4 · L-C11-4 — ⚑ the hero "auras" are not pulses. They are buffs.

All three records the oracle names (gamora C-11 § 4, killing-burst mass) were pulled from the
Edition-II depot with expansion precedence:

| record | class | template | payload |
|---|---|---|---|
| `…/heroskills/archetypes/arcane_elementalaura.dbr` | `Skill_BuffRadiusToggled` | `skill_buffradiustoggled.tpl` | `buffSkillName` → the buff below; `instantCast 1` |
| `…/arcane_elementalaura_buff.dbr` | **`SkillBuff_Passive`** | `skillbuff_passive.tpl` | `offensiveElementalMin` **60-rank array 4 → 426**; `offensiveElementalModifier 35`; `offensiveCritDamageModifier 8`; `skillTargetRadius 12`; **no `…Max`, no duration, no interval, no pulse field of any kind** |
| `…/vampiric_vampireaura_buff.dbr` | `SkillBuff_Passive` | same | **`offensiveLifeLeechMin 500`** and nothing else offensive; `skillTargetRadius 12` |
| `…gdx2/buff/eldritcharmor_enchantedaura_buff.dbr` | `SkillBuff_Passive` | same | ⚑ **`defensiveElementalResistance 20`, `defensivePhysical 20`**, `offensiveElementalMin` 5 → 428; `skillTargetRadius 10` |

**`defensivePhysical = 20` settles it.** A damage pulse does not carry armour. These records are
the full `Parameters_Offensive + Defensive + Character + Retaliation + Conversion + Skill` grant
block that `skill_buff.tpl` includes — a **stat buff applied to bodies within the radius**, whose
`offensive*` rows are flat damage added to *those bodies' own attacks*, and whose `defensive*` rows
are defences granted to them.

The class discriminator is explicit in Crate's own template corpus: an enemy-targeted radius effect
is authored as **`skillbuff_debufradius.tpl` / `SkillBuff_Debuf*`**. These three are
`skillbuff_passive.tpl`. The Edition-IV symbol table agrees — `SkillBuff_Passive` exports
`DispelBuff(Character&)`, `CollectPassiveCharAttributes`, `GetTargetRadiusTag`, and carries a
`CombatFilter` vtable; **it exports no damage-application method at all.** The FX names say the same
(`…_selfloop_chfxpak01` on self, `…_otherloop_fx01` on others).

**So: there is no tick rate, because there is no tick. There is no per-pulse damage, because there
is no pulse. The pulse's "damage" is a grant to the pack.** The `arcane` aura's rank-60 value
(426 flat elemental) is added to the attack of every body it covers — where it then *does* take the
attribute limb (flag 1, § 2.1) and M_inst.

---

## 5 · THE PRICE — arithmetic on gamora's committed numbers, nothing fitted

All inputs are from her C-11 FINDINGS § 1 (pooled 151–159, landed, Leg B): oracle by class —
trash 2,692 · hero 1,363 · boss 715 · champion-bounty 461 · champion 307 · summon 202 · nemesis 5
(**Σ 5,745**); referent **1,606**; **S = ×3.577**. Limb-removal divisors by class: hero 33 ·
champion-bounty 40 · champion 9.6 · trash 7.0 · boss 2.25 · summon/nemesis ≈ 1.

| # | restriction | resulting landed ratio | basis |
|---|---|---|---|
| **P1** | limb OFF for **retaliation rows only** (L-C11-1c) | ⚑ **bracket ×2.14 – ×3.58** | retaliation's share of intake is **not in the committed summary**. Upper bound assumes ALL trash intake is retaliation (2,692 → 385; the named source `aetherorbitalretaliation` is trash); lower bound assumes it is negligible |
| **P2** | hero auras contribute **no direct damage** (L-C11-4) | **≥ ×2.73** before offset | removes at most all hero intake (1,363 → 0). **Offset not quantifiable here**: the grant re-enters as flat damage on every covered body's attack |
| **P1+P2** | both, at their maxima | **×1.29** | 385 + 0 + 715 + 461 + 307 + 202 + 5 = 2,075 |
| **P3** | duration divisors corrected to /215 and /200 (§ 1) | **×3.58 → ×3.58** | her `NO-MDOT` arm is ρ 1.016, so DoT is ≈1.6 % of intake; a +6.3 % lift on it is ≤ +0.1 % of total. ⚑ **negative result** |
| **P4** | own-modifier additive on the **unscaled** base (§ 2.3) | **×2.91** | her `NO-GMAG-OWN` ρ 0.777 → own contributes ×1.287. Under GD's form it contributes 1 + 0.287/a; at a = 6.44 (int 1,170) that is 1.045. 3.577 × 1.045/1.287 |
| — | P1+P2+P4 at their maxima | **×1.05** | a **maximal bound**, not an estimate. Stated so nobody reads it as a target |

**What would turn P1 and P2 from brackets into numbers, from data gamora already has:** a per-skill
landed-HP/s census of her BASE grid, split by (i) rows whose source record name matches
`*retaliation*` and (ii) rows sourced from `*_aura_buff`. She produced exactly that column for the
four killing-burst skills; it needs pooling over all skills, waves 151–159.

---

## 6 · WHAT GAMORA WOULD CHANGE — stated, not made

Each of the following alters the oracle's reference. **That is Matt's HALT. Nothing is proposed as
an action here.**

1. **Gate the attribute limb off for retaliation rows.** Sourced, exact, mechanism-identified.
2. ⚑ **Re-model `*_aura_buff` records as radius buffs on the bodies in range, not as damage
   sources.** This is the largest single item in the note and it is a *content* re-model, not a
   coefficient change — it moves the oracle's #2 killer class.
3. **Reconsider the own-modifier composition** to `base·a + base·own/100` (§ 2.3). Grade-B field
   identity; would want the `+0x48` writer pinned first.
4. **Correct the duration divisors** to dex/215 and int/200. Worth ≈ nothing (P3); correct anyway.
5. **Do not add `physicalDamagePercentage` as a second limb** — Crate's own template says
   *"Only for char sheet cunning dmg."*

---

## 7 · LANE NOTE — the Edition-IV binary carries a full C++ symbol table

`x64/Game.dll` (build 24825149) exports **25,100 decorated MSVC C++ names**, including every
`GAME::Character`, `GAME::CombatManager`, `GAME::CombatAttribute*`, `GAME::Skill_*` and
`GAME::DamageAttribute*` method and vtable. Combined with `.pdata` function bounds this turns the
binary from an opaque blob into a **named, navigable decode surface**. The tooling built this lap
lives beside this note and is reusable:
`…/legolas/scratch/2026-09-29-c11a-attrscope/` — `pe.py` (PE sections, string→VA, RIP-relative LEA
xrefs), `exports.py` (export-table dump), `gddis.py` (capstone disassembly with string
annotation), `rawcall.py` (byte-level `E8/E9` call scan — **linear-sweep disassembly misses call
sites and must not be trusted for reference counts**), `flags.py`, `eqsites.py`.

⚑ **Caveat that must travel with every byte-level row above:** Edition-IV is **post-referent**
(the referent MP4 predates build 24825149). The equation *values* in § 1 are Edition-II; the
*mechanism* in §§ 2–3 is Edition-IV. Nothing here checks that the mechanism was identical in the
referent build. The `.arz` records in § 4 are Edition-II, CRUCIBLE precedence, and stand on their
own.

**Knowledge gaps not resolved.**
- **L-C11-2** (Crucible body dex/int lineage) — not pursued; the commission made it conditional on
  being cheap, and it is not.
- Which modifier class writes damage-attribute `+0x48` (§ 2.3, grade B).
- `CombatAttributeTotalDamageMod`'s positive application arithmetic (§ 3, grade A−).
- Whether `CombatAttribute…::Process`'s `Character&` is the attacker or the defender was inferred
  from semantics and from gamora's Lap M/O chain reproduction, **not** re-derived here.
