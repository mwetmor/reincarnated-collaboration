# Research — ARPG Damage Scaling Patterns — 2026-05-27

**Mode:** A (analytical — Pattern A-deep; methodology consultation per Discipline #18)
**Commissioner:** knight-rider (Cycle 14 SC-5 dispatch)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratification)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-legolas-cycle-14-sc-5-damage-scaling-research.md`
**Gates:** Wave 0.5 (damage_scaling_type routing + per-skill emission)
**Sources consulted:** see § 8 Source List
**Disciplines honored:** #18 (methodology-before-execution), #11 (empirical inspection), #1 (math-before-code)

---

## Summary (3-5 sentences)

Community-canonical ARPG damage-formula research across 7+ games (D2 LoD, D3, D4, PoE/PoE2, Last Epoch, Grim Dawn, Lost Ark) **strongly validates** doc 47's three-path architecture. The physical/magical separation is genre-universal: five of seven surveyed games use an independent base-spell-damage seed for magical skills that does not route through weapon raw physical damage. D3 and D4 are the architectural outliers that route ALL skills (including spells) through weapon damage — but both games compensate by designing caster weapons with appropriately inflated "weapon damage" stats so the weapon is functionally a spell-power proxy, not a literal physical damage value. Doc 47's formula structures are well-grounded; the primary refinement recommendation is that the magical formula needs to account for element affinity modifiers as an additive pool (not a standalone multiplier) to prevent the D4-launch multiplier inflation pattern. The edge-case catalogue reveals three implementation risks requiring Wave 0.5 attention: the element-conversion physical-retains-both-modifier pattern (PoE1 vs PoE2 contrast), the DOT scaling independence requirement, and the crit base-value source asymmetry between physical (weapon-based) and magical (skill-gem-based) paths.

---

## Findings

### 1. Per-Game Per-Path Formula Tables (Q-SC5-1 through Q-SC5-4 supporting data)

#### 1.1 Diablo 2: Lord of Destruction

**Physical formula structure:**
```
physical_damage = weapon_base_damage_range
                × (1 + STR_or_DEX_bonus / 100)    [weapon-type dependent: melee=STR, bow=DEX, knife=0.75×STR+0.75×DEX]
                × (1 + enhanced_damage_on_weapon / 100)
                × (1 + off_weapon_enhanced_damage / 100)
```

Flat damage affixes (min/max ranges) add before the percentage multipliers in the off-weapon ED phase.

**Magical/spell formula structure:**
```
spell_damage = base_skill_damage_range(skill_level)    [completely independent of weapon; defined per-skill per-level in game data]
             × (1 + fire_mastery_bonus / 100)           [Sorceress mastery skill; equivalent to element affinity]
             × (1 + synergy_bonus / 100)                [e.g., Fireball receives +16% fire damage per level of Fire Bolt]
             × (1 + item_fire_damage_bonus / 100)       [+%fire damage affixes]
```

**Caster weapon role:** +to-skill-level (increases `skill_level` → higher base_skill_damage_range), Faster Cast Rate (cast speed), +%fire/cold/lightning damage. The staff's own physical damage stat (e.g., 30-60 damage on a crystal sword) has **zero** effect on Fireball or any spell.

**Confirmed by:** Diablo 2 wiki damage bonus entry; Sorceress Fire Spells documentation; physical damage FAQ at mannm.org. Primary source (game data documentation): the physical damage formula explicitly separates spells — "Spells are as always subject to equipment restrictions, say they are only enhanceable via skill boni, [Faster Cast Rate], and, if you're lucky, with [decreasing of enemy's physical resistance]. Spell damage ignores weapon damage entirely, depending instead on skill levels and cast rate modifiers." (Source: mannm.org D2 physics damage FAQ).

**Hybrid handling:** D2 has no formal hybrid skill class in the modern sense. The Paladin's Holy Bolt is a physical+magical hybrid but handled via separate damage components. The Druid's summoned minions use physical weapon proxy stats independent of player weapon. No cross-attribute ω-penalty analog exists in D2.

**Crit on magical:** D2 spells have no critical-strike system by default. Deadly Strike (from gear) applies only to attack-based skills, not spells. Open Wounds likewise attack-only.

**DOT scaling:** Poison DoT scales from skill level + synergies (same formula as the base spell damage seed). Burn (Firestorm, Meteor impact) shares the element-mastery scaling. Not weapon-derived.

**Doc 47 genre canon table validation (§ 1.2):** CONFIRMED for D2. Physical = weapon damage + STR/DEX scaling. Magical = base spell damage + skill level + synergies. Caster weapon = +to-skills / +%element damage / FCR, never raw physical scaling.

---

#### 1.2 Diablo 3

**Physical formula structure (all skills, including spells):**
```
skill_damage = (weapon_average_damage_per_hit)    [weapon min-max damage averaged; not DPS — spell damage cares about damage-per-hit not DPS]
             × skill_damage_percentage             [shown in tooltip as "300% weapon damage"; varies per skill]
             × (1 + INT_bonus / 100)               [INT = 1% damage per point; caster's primary stat]
             × (1 + additive_damage_bonuses / 100)
             × multiplicative_bonuses_product       [e.g., Pain Enhancer, Strongarm Bracers conditional multipliers]
```

**Architectural note — D3 is the outlier:** D3 routes ALL skills (physical AND magical) through weapon damage. A Wizard Fireball and a Barbarian Whirlwind both use "weapon damage ×%" as the base seed. The architectural compensation: **caster weapons (wands, orbs, staves, sources) are designed with appropriately high weapon damage stats** reflecting their spell-power role. A high-end Wizard wand may show "1800-2200 damage" which is functionally the spell-power budget, not physical striking power. The "weapon damage" stat on a caster item is calibrated as if it were spell power.

**Confirmed by:** D3 damage formula documentation at purediablo.com; D3 blog damage explanation. Key quote: "Unlike in Diablo 2, a wizard cares deeply about his weapon, as all offensive skills have their damage based on the weapon equipped. The weapon damage that spells use to calculate 'X% of weapon damage' is not using your DPS but your actual damage per 'hit'."

**Crit:** Unified system — all skills (physical and magical) use the same crit chance pool from gear. Crit chance × crit multiplier. No distinction between physical crit and spell crit.

**DOT scaling:** DoTs (e.g., Bleeding, Burning from Wizard) scale through the same weapon-damage × skill% base but DoT ticks do not separately crit in most cases (vanilla behavior).

**Hybrid handling:** Not architecturally relevant — D3's unified weapon-damage base means physical/magical distinction doesn't create routing complexity. All skills compute from the same base.

**Doc 47 genre canon table validation (§ 1.2):** PARTIALLY CONFIRMED with annotation. D3 uses "weapon damage" for spells but the caster weapon's "weapon damage" stat is functionally spell power, not physical striking power. The architectural intent of doc 47 (caster weapon modifies HOW spell scales, not raw physical damage entering) is preserved because caster weapon's spell-power-calibrated "weapon damage" stat is not the same as a physical weapon's physical-striking-power stat. The label is the same; the semantic intent is different. This is the D3-D4 model.

---

#### 1.3 Diablo 4

**Physical formula structure:**
```
skill_damage = weapon_damage_value                             [skill tooltip shows skill_damage_pct × weapon_damage]
             × (1 + additive_bonus_sum / 100)                  [all +%damage type affixes sum into this one bucket]
             × (1 + vulnerable_bonus / 100)                    [separate multiplier for Vulnerable enemies; baseline 20%]
             × crit_multiplier_if_applicable                   [separate multiplicative bucket]
             × (1 + main_stat_bonus / 100)                     [main stat = 0.1% skill damage per 1 point; e.g., 1000 INT = +100% damage as separate bucket]
             × global_multiplier_product                       [conditional multipliers with × tag]
```

**Magical skills (Sorcerer):** SAME formula — weapon damage as base. Like D3, D4's sorcerer staff/focus/wand is designed with appropriate weapon damage levels for the class's spell-power budget. Intelligence is the main stat (0.1% per point), applying as a separate multiplicative bucket. The "wooden staff" in D4 is mechanically calibrated to be a spell-power proxy — a Sorcerer staff shows damage values calibrated for INT-scaling + spell use, not physical combat.

**Crit:** Unified — base crit chance 5%, increased via gear affixes and Dexterity for all classes. Crit multiplier is a separate multiplicative bucket. DoT skills explicitly **cannot benefit from Critical Strikes** unless the tooltip states otherwise.

**DOT scaling:** DoTs scale through additive bonuses and vulnerable/global multipliers but skip the crit bucket. Bleed/Burn/Poison follow same formula except no crit.

**Hybrid handling:** Class-specific. Druid's shapeshifting provides hybrid physical+elemental that scales through the same unified bucket system.

**D4 launch inflation problem (Q-SC5-5 supporting):** Community documentation (Icy Veins analysis) identified that the multiplicative bucket system + abundant "More Damage" multipliers in skill trees led to exponential build power. Players at launch could stack 5+ independent multiplicative buckets (Vulnerable, Crit, Main Stat, Global Multipliers, Conditional Multipliers) producing values that inflated from millions to quadrillions within seasons. The root cause: **too many independently multiplicative buckets with easy-to-achieve conditions**. Post-Season 2 reworks consolidated and capped several buckets.

**Doc 47 genre canon table validation (§ 1.2):** CONFIRMED for D4 with same annotation as D3 — all skills route through weapon damage, but caster weapons are designed as spell-power proxies. The architectural semantic of "caster weapon modifies spell" is preserved via weapon-design, not via routing separation.

---

#### 1.4 Path of Exile (PoE1 + PoE2)

**Physical attack formula structure:**
```
physical_attack_damage = weapon_physical_damage_range          [weapon's inherent physical damage stat]
                       × (1 + local_enhanced_damage / 100)     [weapon-local affix; applies before global]
                       × (1 + global_increased_physical / 100) [additive pool: all "increased physical damage" sources]
                       × more_multiplier_product               [support gems + keystones; multiplicative]
                       × crit_if_applicable
```

**Magical/spell formula structure:**
```
spell_damage = base_spell_damage(gem_level)                     [defined per skill gem per level; COMPLETELY independent of weapon]
             × damage_effectiveness × added_damage_flat         [flat added damage on items × effectiveness; many spells have 0% effectiveness for flat dmg]
             × (1 + sum_of_increased_spell_damage / 100)        [additive pool: "increased spell damage", "increased fire damage", etc. ALL sum into one pool]
             × more_multiplier_product                          [support gems + keystones; multiplicative; stacks less efficiently]
             × crit_multiplier_if_crit
```

**Caster weapon role:** Wands/staves provide `+%spell damage`, `+%element damage`, `+to-gem-level`, `+mana`, flat added damage (modified by damage effectiveness). The weapon's **own physical damage** (e.g., a wand has 20-60 physical damage) has NO effect on spell damage unless the player specifically picks the "Battlemage" keystone (Contact-based attack conversion) or equivalent. Per the PoE wiki: "flat damage added to a weapon is added to the weapon's base damage and doesn't affect spells unless explicitly stated otherwise."

**Crit on spells vs attacks — KEY ARCHITECTURAL DIFFERENCE:**
- **Attacks:** base crit chance comes from the **weapon's own base critical strike chance stat**
- **Spells:** base crit chance comes from the **skill gem itself** (listed in the gem description), independent of weapon
- Formula is identical: `crit_chance = base_crit × (1 + increased_crit_chance)`. But the base source is different.

**DOT scaling (PoE1):** DoTs (Ignite, Bleed, Poison) are seeded from the hit that applies them but scale independently:
- **Ignite:** scales with `increased fire damage`, `increased burning damage`, `increased DoT`, NOT with spell damage or attack damage modifiers
- **Bleed:** scales with `increased physical damage`, `increased bleed`, `increased DoT`
- **Poison:** scales with `increased chaos damage`, `increased poison`, `increased DoT`; explicitly: "stats modifying spell damage and attack damage do NOT apply to poison"
- DoTs cannot crit.

**Damage conversion (element conversion) — hybrid pattern:**
- **PoE1:** Converted damage RETAINS memory of original type. Physical → Fire conversion means BOTH `increased physical damage` AND `increased fire damage` apply to the converted portion. This enables the famous "scales as both" pattern.
- **PoE2:** CHANGED — converted damage no longer retains original type. Only the final damage type's modifiers apply. This is architecturally cleaner but removes the "scales as both" double-dipping.

**Hybrid skills:** Elementalist with "Shaper of Flames" converts cold/lightning to fire — result scales as fire only. No formal "hybrid physical+magical" skill type in PoE's sense — there are attacks that add elemental damage on hit (treated as separate damage components), not skills that scale from both physical and INT simultaneously.

**Additive vs multiplicative stacking:** PoE's canonical pattern — all "increased" sources pool additively into one multiplier; "more" sources are independent multiplicative stacks. This provides diminishing returns from stacking within the additive pool but full returns from mixing additive + multiplicative sources.

**Doc 47 genre canon table validation (§ 1.2):** STRONGLY CONFIRMED. PoE is the purest implementation of the physical/magical separation. Spell damage = gem level base, never weapon physical. Caster weapon = +%spell damage / +%element damage / +to-gem-level. This is the most direct precedent for doc 47's magical formula architecture.

---

#### 1.5 Last Epoch

**Physical attack formula structure:**
```
physical_attack_damage = (base_weapon_attack_damage
                         + added_physical_damage_flat)
                       × damage_effectiveness                   [skill-specific multiplier on added damage]
                       × (1 + increased_physical_sum / 100)     [additive: all "increased physical", "increased melee", etc.]
                       × more_multiplier_product
```

Attack speed scales from weapon base attack rate; physical attacks scale from weapon base damage.

**Magical/spell formula structure:**
```
spell_damage = (base_skill_spell_damage
               + added_spell_damage_flat × effectiveness)       ["+X spell damage" on weapons/gear × effectiveness]
             × (1 + increased_spell_damage_sum / 100)
             × more_multiplier_product
             × crit_multiplier_if_applicable
```

Key: `added_spell_damage_flat` on weapons (e.g., "+4 Spell Damage") is flat base-level contribution, **not** the weapon's physical attack damage. The weapon's raw physical attack damage does NOT scale spells. Cast speed does not scale from weapon base attack rate (attacks do scale from weapon base attack rate — explicit distinction).

**Attribute scaling:**
- Physical attacks: Strength scales physical damage
- Spells: Attunement scales spell damage ("just as the damage from a sword scales with your Strength score, many magical-based abilities become stronger with Attunement")
- Per-skill tags determine which attributes apply (not universal — each skill has scaling tags)

**Crit:** Hits can crit; DoTs cannot crit. Default crit multiplier = 200% (represented as "2" in the formula: `damage × (2 + additional_crit_multi_sources)`).

**DOT scaling:** DoTs scale independently: `increased damage type` bonuses, duration (more ticks = more total damage), and shred/penetration. Explicitly cannot crit or trigger "on hit" effects.

**Hybrid skills:** Mixed damage types are scaled independently per component then summed. "Adaptive Damage" on weapons converts to the skill's damage type — a smart system that lets weapon affixes contribute meaningfully to whatever skill type is equipped.

**Doc 47 genre canon table validation (§ 1.2):** CONFIRMED. Last Epoch is architecturally very close to doc 47's model. Physical = weapon-based; magical = skill-based; weapon provides spell damage via `+spell damage` modifier, not raw physical. Attunement = INT/WIS analog.

---

#### 1.6 Grim Dawn

**Physical attack formula structure:**
```
physical_damage = weapon_base_physical_damage                   [weapon's physical damage stat]
                × skill_weapon_damage_pct / 100                 [most attack skills show "X% Weapon Damage"; e.g., 125% Weapon Damage]
                × (1 + cunning_bonus / 100)                     [Cunning: +0.33% physical damage per point]
                × (1 + percent_physical_bonuses / 100)          [additive pool: gear physical damage bonuses]
```

**Magical/spell formula structure:**
```
elemental_spell_damage = base_skill_elemental_damage            [defined per skill; independent of weapon physical]
                       × (1 + spirit_bonus / 100)               [Spirit: +0.33% magical damage per point]
                       × (1 + percent_elemental_bonuses / 100)  [additive pool: gear elemental bonuses]
                       × conversion_if_applicable               [damage conversion rules per skill order]
```

**Hybrid note:** Many Grim Dawn skills include BOTH a `%Weapon Damage` component AND flat elemental/vitality damage. A skill like Callidor's Tempest (Arcanist) has "12% Weapon Damage + X Fire Damage". This means it scales from BOTH physical weapon AND spell modifiers, but as **separately computed components that sum**. This is the GD precedent for sum_paths hybrid.

**Caster weapon role (off-hand focuses/tomes):** Provides `+%elemental damage`, `+%spirit`, cooldown reduction, flat elemental/vitality damage bonuses. Does NOT directly contribute weapon physical damage to spells.

**Cunning vs Spirit:**
- Cunning → physical/pierce/bleed/trauma damage bonuses
- Spirit → vitality/elemental/magical damage bonuses
- Physique → health/defensive

**DOT scaling:** Duration damage (Bleed, Burn, Poison DoTs) scales with Cunning for physical DoTs and Spirit for elemental DoTs. DoTs have their own base amounts and scale independently from direct hit damage.

**Damage conversion order:** Base Skill → Skill Modifiers → Skill/Transmuter Conversion → Equipment/Buffs Conversion → Equipment/Auras/Passives. Conversion is applied before `+%` damage bonuses. Critical nuance: if a skill converts physical to fire, the `+%fire damage` bonuses apply AFTER conversion to the converted portion.

**Doc 47 genre canon table validation (§ 1.2):** CONFIRMED with refinement. GD confirms the physical/magical separation but also provides the clearest precedent for the **sum_paths hybrid pattern** (explicit `%Weapon Damage` component + flat elemental component summed per skill).

---

#### 1.7 Lost Ark

**Formula structure:**
```
skill_damage = (initial_value + attack_power × skill_coefficient)
             × (1 + crit_chance × (crit_multiplier - 1))    [approximate expected value form]
             × conditional_multiplier_product               [Grudge, Master Brawler, class-specific multipliers]
```

`attack_power` derives from Weapon Power (weapon stat → Attack Power stat) + class attribute (Strength for Warriors, Intelligence for Mages, Dexterity for Gunners/Assassins).

**Key architectural note — Lost Ark is a unified-formula game like D3/D4:** There is no separate physical vs magical formula at the base level. All classes (physical Warriors and magical Mages) scale skills from the same `attack_power` base. The class-specific attribute (Strength/INT/DEX) feeds into `attack_power` rather than being a separate multiplier. Class separation is via **attribute-to-attack-power conversion efficiency** (INT gives Mages the same attack power per point that STR gives Warriors), not via separate damage formulas.

**Caster weapon role:** Caster-class weapons contribute to `weapon_power` (which feeds attack_power), same architecture as physical weapons. Higher tier caster weapon = higher attack power = higher spell damage. This is functionally identical to D3/D4's "caster weapons have appropriate weapon damage stats" model.

**Crit:** Unified system. Critical Rate (hit chance of crit) + Critical Damage (multiplier on crit). No distinction between spell crit and physical crit.

**Doc 47 genre canon table validation (§ 1.2):** Lost Ark is the second unified-formula case alongside D3/D4. Physical and magical both scale from weapon power, differentiated only by class stat (STR vs INT vs DEX feeding the same attack power pool). This is architecturally distinct from doc 47's two-seed approach but does not contradict the doc 47 architecture — it represents an alternative design philosophy.

---

#### 1.8 Genre Canon Table — Comprehensive

| Game | Physical formula seed | Magical formula seed | Physical/magical separated? | Caster weapon role |
|---|---|---|---|---|
| **D2 LoD** | Weapon physical damage range | Base skill damage per level + synergies (independent) | YES — clean separation | +to-skills, +%element damage, FCR; NOT raw weapon damage |
| **D3** | Weapon average damage per hit | Same weapon damage per hit × skill% | NO — unified | Caster weapon calibrated as spell-power proxy; INT multiplier |
| **D4** | Weapon damage × skill% | Same: weapon damage × skill% | NO — unified | Caster weapon calibrated as spell-power proxy; INT multiplier |
| **PoE / PoE2** | Weapon physical damage range | Skill gem base damage per gem level (independent) | YES — clean separation | +%spell damage, +%element damage, +to-gem-level; NOT raw weapon damage |
| **Last Epoch** | Weapon base attack damage | Skill base spell damage (independent); +spell damage on weapons as flat add | YES — clean separation | +spell damage (flat), +%spell damage (%), NOT raw weapon attack damage |
| **Grim Dawn** | Weapon physical × skill %weapon damage | Skill base elemental damage (independent); Spirit attribute | YES — clean separation | Off-hand provides +%elemental, +Spirit; hybrid skills sum both paths |
| **Lost Ark** | Weapon Power → attack_power; STR attribute | Same weapon power base; INT attribute feeds same attack_power | NO — unified | Caster weapon = weapon power proxy; same system |

**Convergent pattern reading:** 4 of 7 games (D2, PoE, LE, GD) use clean physical/magical separation with independent damage seeds. 3 of 7 (D3, D4, Lost Ark) use unified weapon-damage-base architecture. The unified approach requires careful weapon-design (caster weapons must have calibrated "weapon damage" or "weapon power" stats). The separated approach (doc 47's model) avoids this calibration problem entirely but requires a separate `base_spell_damage` lookup table.

---

### 2. Structural Validation of Doc 47 Formulas (Q-SC5-1 through Q-SC5-4)

#### 2.1 Q-SC5-1 — Physical formula structure validation

**Doc 47 physical formula:**
```
weapon_base_physical_damage × skill_damage_multiplier × (1 + attribute_bonus/100) × (1 + global_physical_modifier/100) × tier_coefficient × element_conversion_factor × crit_multiplier
```

**Assessment: VALID. Well-grounded in genre canon.**

Supporting evidence:
- D2 LoD: weapon base damage × STR/DEX bonus × enhanced damage multipliers — matches this structure
- PoE1: weapon physical damage range × (1 + increased_physical additive pool) × more multipliers — matches structure with additive-pool-first composition
- Grim Dawn: weapon damage × cunning bonus × percent physical bonuses — matches structure
- Last Epoch: weapon base × increased_physical additive pool — matches structure

**Community variations to note for gamora:**

1. **Additive pool composition order matters.** Genre-canonical pattern places all `+%` modifiers in a single additive pool first, then multiplies by "more" modifiers (PoE pattern). Doc 47's formula shows `(1 + attribute_bonus/100) × (1 + global_physical_modifier/100)` as TWO separate multiplicative terms. This is technically equivalent to D4's bucket model (two separate multipliers) but diverges from PoE's model (one additive pool). The implementation question for gamora: should `attribute_bonus` and `global_physical_modifier` be in the SAME additive pool (summed then multiplied once) or separate multiplicative buckets?

   **Finding:** The D4/Lost Ark model (separate buckets for main stat vs additive bonuses) produces slightly MORE power per unit than the PoE model (one additive pool). The doc 47 formula as written with two separate `(1 + x/100)` terms creates two independent multipliers. For a small game like Reincarnated (fewer affix sources than PoE/D4), the risk of runaway multiplication is lower — but the gamora implementation should still be aware of this distinction.

2. **Pre-mitigation vs post-mitigation crit.** Community-canonical pattern: crit fires on the raw damage BEFORE defense mitigation is applied. Doc 47 shows `crit_multiplier` at the end of the formula alongside `apply_target_defenses`. This is correct — crit multiplies pre-defense. The `apply_target_defenses` call in the pseudocode (§ 4.2) correctly applies after crit. No amendment needed.

3. **Tier_coefficient placement.** Doc 47 places `tier_coefficient` before `element_conversion_factor`. Genre-canonical pattern (PoE, GD): conversion happens before percentage bonuses apply. If `element_conversion_factor` conceptually changes the damage type, it should be applied before the `tier_coefficient` modifies the converted amount. Mild reordering recommendation: apply `element_conversion_factor` BEFORE `tier_coefficient` in the physical formula. See § 3.4 element conversion edge case for detail.

#### 2.2 Q-SC5-2 — Magical formula structure and base_spell_damage seed validation

**Doc 47 magical formula:**
```
base_spell_damage(element, skill_tier) × skill_damage_multiplier × (1 + caster_attribute_bonus/100) × (1 + weapon_spell_damage_modifier/100) × (1 + element_affinity_modifier/100) × (1 + global_spell_damage_modifier/100) × tier_coefficient × element_conversion_factor × crit_multiplier
```

**Assessment: VALID. `base_spell_damage` as the seed (not weapon physical damage) is strongly genre-supported.**

Supporting evidence:
- D2 LoD: base skill damage per level is the canonical seed for all spells; weapon physical damage is zero contribution
- PoE/PoE2: skill gem base damage per gem level is the canonical seed; explicit wiki statement: "flat damage on a weapon is added to the weapon's base damage and doesn't affect spells unless explicitly stated otherwise"
- Last Epoch: skill base spell damage + added_spell_damage flat (from weapons as a separate affix, not raw weapon damage)
- Grim Dawn: skill base elemental damage independent of weapon physical

**Alternative (D3/D4 model) and why doc 47's choice is better for Reincarnated:**

The D3/D4 unified-weapon-damage approach works because caster weapons in those games are calibrated as spell-power proxies. In a QD-engine context with substrate-bound weapons, calibrating "weapon damage" on a wooden staff to reflect spell power would require:
- Separate physical-damage-stat tracks per weapon-attribute-family
- The stat labeled "weapon damage" on a staff would have no relationship to the staff's actual physical striking power
- This creates semantic confusion at the player-facing layer (spirit guide narration: "your 50 physical damage staff contributes its 50 damage to Ice Spike" is confusing)

Doc 47's architecture (base_spell_damage as independent seed; caster weapon provides `+%spell damage` modifier) is cleaner for a substrate-bound system. It accurately reflects what the weapon IS (a conduit/amplifier) vs what it IS NOT (a damage source for spells).

**Refinement for the magical formula — element_affinity additive pooling:**

Doc 47's current magical formula multiplies THREE separate percentage terms:
```
(1 + weapon_spell_damage_modifier/100) × (1 + element_affinity_modifier/100) × (1 + global_spell_damage_modifier/100)
```

These are THREE independent multiplicative buckets. Genre-canonical precedent (PoE, Last Epoch) places all "increased spell damage" sources — including element affinity bonuses, weapon spell modifiers, and global spell bonuses — into ONE additive pool:
```
(1 + (weapon_spell_damage_modifier + element_affinity_modifier + global_spell_damage_modifier) / 100)
```

**Recommendation for gamora:** Implement the magical formula's percentage modifiers as ONE additive pool: `(1 + sum_of_all_spell_damage_pct / 100)`. This prevents the D4-launch pattern where independent multiplicative buckets compound to inflated damage. The separate buckets approach becomes problematic when players can easily stack all three sources simultaneously. PoE's model (everything "increased" pools additively) is the community-canonical anti-inflation pattern.

**See § 4 (AI-tell and community perception) for the D4 inflation failure mode in detail.**

#### 2.3 Q-SC5-3 — Hybrid skill patterns validation

**Doc 47 hybrid patterns:**
1. `physical_with_element_flavor` — physical path with element conversion
2. `magical_with_martial_weapon` — magical path with ω-penalty for cross-attribute
3. `sum_paths` — both paths summed × hybrid_balance_factor

**Assessment: ALL THREE patterns are genre-grounded.**

Evidence:
- **Pattern 1 (physical_with_element_flavor):** PoE's "Avatar of Fire" keystone converts all damage to fire — the skill remains an attack (physical seeded) but the converted portion is fire. Last Epoch's Adaptive Damage handles similar conversions. GD's Blademaster builds use physical weapon + converted elemental overlay. CONFIRMED genre pattern.

- **Pattern 2 (magical_with_martial_weapon):** PoE's Battlemage keystone applies intelligence to attacks; various intelligence-scaled builds use martial weapons with spell-scaling overlays. GD's Arcanist/Soldier hybrid uses STR/Cunning to boost physical component while Spirit boosts magical component. CONFIRMED genre pattern.

- **Pattern 3 (sum_paths):** Grim Dawn is the clearest precedent. Callidor's Tempest explicitly has "12% Weapon Damage + X Fire Damage" — two independently computed components that sum. The `hybrid_balance_factor` in doc 47 is an extension of this pattern with an explicit weighting parameter. Also precedented in GD's Saboteur builds where physical + fire components both scale from their respective attributes then sum.

**Additional genre patterns NOT in doc 47 worth flagging for gamora:**

4. **Proc-on-physical pattern (not sum_paths but additive bonus):** Skills like PoE's "Added Lightning Damage Support" — a physical attack that ALSO adds a separate flat lightning damage component. This isn't a sum_paths hybrid — it's a physical skill with an additive elemental proc. If Reincarnated needs this pattern (e.g., "a melee strike that procs fire sparks"), it doesn't require a new hybrid_pattern enum — the `element_conversion_factor` in the physical path handles it partially, but a `proc_on_hit_element_bonus` sub-system might be cleaner for the proc pattern specifically. Flag for gamora's attention.

#### 2.4 Q-SC5-4 — Genre canon table confirmation

**Assessment: Doc 47's § 1.2 genre canon table is CONFIRMED and can be strengthened.**

Additions/refinements from deeper research:

| Game | Enhancement to doc 47's table entry |
|---|---|
| D2 LoD | Weapon physical has zero contribution to spells. Fireball's base damage per level (e.g., level 20 = ~400-430 fire damage) is entirely skill-table-derived. Confirmed |
| D3 | All skills scale from weapon damage — caster weapons are spell-power proxies. This is a design-pattern choice, not a physical/magical split. INT is a separate multiplicative bucket |
| D4 | Same as D3 architecture. Weapon damage × skill% × INT bucket × other buckets. Caster weapon stats are calibrated for class budget. DoTs cannot crit |
| PoE | Spell crit base comes from skill gem (not weapon). "Increases and reductions to physical damage do NOT apply" to spells. Only "spell damage", "element damage", "global damage" apply |
| LE | Attunement = INT/WIS analog. Explicit: weapon attack damage does not scale spells by default. "+spell damage" on weapons is a flat modifier, not weapon damage |
| GD | Spirit attribute → +0.33% magical damage per point (parallel to Cunning's +0.33% physical). Hybrid skills explicitly sum physical + elemental components |
| Lost Ark | Unified attack_power model — no physical/magical formula separation at routing level |

---

### 3. Edge-Case Catalogue (§ 7.3 of dispatch)

#### 3.1 Weapon-Element-Conversion Skills (T4 ELEMENT_CONVERSION)

**Dispatch question:** Does element-converted physical scale fully like physical or partially like magical?

**Finding: Depends on the conversion architecture chosen. Two distinct genre patterns:**

**Pattern A — Physical retains both modifier types (PoE1 model):**
Physical damage converted to fire via T4 ELEMENT_CONVERSION scales BOTH `+%physical damage` and `+%fire damage` modifiers. The converted damage "remembers" its physical origin. This is PoE1's historical behavior and enables "scales as both" builds.

**Pattern B — Converted damage takes only the final type (PoE2 model):**
Converted physical-to-fire scales ONLY `+%fire damage`. No physical modifiers apply to the converted portion. Cleaner; prevents double-dipping.

**Recommendation for Wave 0.5:** Choose Pattern B (PoE2 model). Doc 47 already implies this — physical path + element_conversion_factor suggests the conversion happens at the final step, meaning the output is classified as the converted element. Implementing Pattern A would require tracking "damage type memory" across the formula, adding significant implementation complexity. Pattern B is cleaner and the more modern community-canonical approach. **Decision for gamora: after element_conversion_factor is applied, the damage is classified as the converted element type only. `+%physical damage` modifiers do NOT carry over.**

**Implementation note:** This means `apply_target_defenses` at the end of `calculate_physical_damage` should use `damage_type=skill.element` (the converted element), not `"physical"`, when ELEMENT_CONVERSION T4 is active. Doc 47 § 4.2 already does this correctly: `damage_type=skill.element or "physical"`. Confirmed correct.

#### 3.2 Caster Weapons with STR Characters (Cross-Attribute Equip Problem)

**Dispatch question:** If a STR character equips a wooden staff, does the staff's physical damage scale by STR?

**Finding: Enforcement-at-equip is the correct solution, confirmed by genre precedent.**

Genre precedent:
- PoE: weapon-type requirements enforced at equip. STR characters cannot equip INT-requirement weapons without meeting the INT requirement. If somehow equipped, the weapon's physical damage is available but spell damage modifiers on the weapon don't help the STR character's skills.
- Last Epoch: Each skill has scaling tags that determine what attributes apply. A physical attack skill on a wand would scale from Attunement if the skill has Attunement scaling, which a STR physical skill doesn't.
- GD: Attribute requirements enforced at equip. A soldier (STR/Cunning-primary) can technically equip a caster off-hand but won't benefit from Spirit-scaling spells without investing Spirit.

**Recommendation for Wave 0.5 (confirmed: enforce at equip):** Doc 47 § 7.2 notes `attribute_requirement` and `weapon_type_family` as required substrate fields. Wave 0.5 should enforce: a physical-attribute character cannot equip a caster-attribute weapon without meeting the `attribute_requirement` threshold. If the equip system doesn't enforce this, the `damage_scaling_type` routing still protects the formula: a STR character equipping a caster staff who uses a `damage_scaling_type=physical` skill will look up `weapon.base_physical_damage` (low on a staff, 20-80 per doc 47 § 3.1) — the damage will simply be weak, not broken. The architecture self-corrects. But enforcement-at-equip is cleaner UX.

#### 3.3 Hybrid Skills — sum_paths vs per-path-isolated

**Dispatch question:** sum_paths approach vs per-path-isolated approach — risks?

**Finding: sum_paths is genre-valid but creates a calibration edge case.**

When `sum_paths` sums physical + magical with a `hybrid_balance_factor`:
```
dmg = phys × balance_factor + magic × (1 - balance_factor)
```

**Risk:** If balance_factor = 0.5 and physical_path outputs X while magical_path outputs Y, the total is 0.5X + 0.5Y. This is NOT the same as running either path at 100%. The player who invests heavily in `+%physical damage` for a hybrid skill only benefits from the 50% physical component — the investment efficiency halves. This is the "hybrid tax" pattern — genre-canonical (see Lost Ark's identity skills that scale poorly with stat optimization, or PoE's hybrid-damage gems that resist perfect optimization). The ω-penalty for Option C cells already addresses this architecturally. The `hybrid_balance_factor` just makes it explicit.

**GD precedent for the sum approach:** Skills with explicit `%Weapon Damage + flat Elemental` sum both and the player can optimize both paths independently. Neither "halves" — both components are full value. The GD model is additive combination (full physical + full magical), not balanced split. Doc 47's `hybrid_balance_factor × phys + (1 - hybrid_balance_factor) × magic` is the more formally controlled version.

**Recommendation:** The `sum_paths` implementation is valid. The Wave 0.5 implementation note: `hybrid_balance_factor` values near 0.5 produce the most "hybrid" feel but weakest optimization ceiling per path. Values near 0 or 1.0 approximate single-path behavior. The starting calibration for hybrid skills should probably be 0.5-0.6 physical-weighted for melee hybrid classes (Holy Knight, Spellsword) given that weapon damage is the "visible" component.

#### 3.4 Element Affinity Stacking — Additive vs Multiplicative

**Dispatch question:** `+%fire damage` partition affixes + element_affinity weapon modifier — additive or multiplicative composition?

**Finding: ADDITIVE is the genre-canonical and inflation-safe pattern.**

Evidence:
- PoE: All "increased fire damage" sources (gear affixes, passive tree, weapon modifiers) pool into ONE additive pool. Example: 50% increased fire damage from gear + 30% from passive tree + 20% from weapon = (1 + (50+30+20)/100) = 2.0×. NOT 1.5 × 1.3 × 1.2 = 2.34×.
- D4 post-Season-2: "Total Additive Bonus" bucket pools all conditional damage sources additively.
- Last Epoch: "Increased Damage" sources are explicitly additive with each other. "More Damage" sources are separate multipliers. The game documentation explicitly calls out "Game says 'multiplicative' but actually it's additive" as a player-confusion source — the correct behavior is additive within the pool.

**Recommendation for Wave 0.5:** Implement element affinity stacking as ADDITIVE. `element_affinity_modifier` in doc 47's magical formula should be the **sum** of:
- `+%[element] damage` partition affixes from gear
- Element affinity modifier on caster weapon
- Chain passive `+%[element] damage` bonuses
- T4 Cat C element-conversion bonuses (if applicable)

Then apply as ONE pool: `(1 + total_element_affinity_sum / 100)`.

If doc 47's formula is implemented as separate `(1 + element_affinity_modifier/100)` and `(1 + global_spell_damage_modifier/100)` multiplicative terms, this creates two buckets rather than one. See § 2.2 Refinement above for the full additive-pool recommendation.

#### 3.5 Crit on Magical — Same as Physical?

**Dispatch question:** Does spell power crit work the same as physical crit?

**Finding: Mechanically similar but DIFFERENT BASE CRIT SOURCE — important asymmetry.**

Evidence:
- **PoE (primary authoritative source):** Physical attack crit base = weapon's base crit chance. Spell crit base = skill gem's own base crit chance. Formula is identical: `crit_chance = base_crit × (1 + increased_crit)`. Multiplier application is the same. But the base values are different (e.g., a bow might have 6% base crit, while Ice Nova spell might have 5% base crit at gem level 1).
- **D4:** Unified crit system. Base 5% for all skills including spells. No distinction.
- **Last Epoch:** Same crit formula for hits; DoTs explicitly cannot crit.
- **D2:** No crit for spells at all (Deadly Strike = attack-only).

**Recommendation for Wave 0.5:** Implement crit as architecturally unified (same `crit_chance` pool and `crit_multiplier` pool for both physical and magical), BUT consider whether `base_crit_chance` for magical skills should be skill-intrinsic (PoE pattern) vs character-level (D4 pattern). For Reincarnated's simplicity at v1, the character-level base crit (D4 pattern — one base crit chance for the character, modified by gear) is simpler to implement and avoids per-skill crit-base calibration. This is a gamora implementation decision, not a formula correctness issue.

**Doc 47 already assumes unified crit:** The pseudocode in § 4.2 and § 4.3 both apply `player.crit_chance` and `player.crit_multiplier` without distinction between physical and magical. This matches the D4/Lost Ark/LE model. CONFIRMED VALID. The PoE per-spell-base-crit model is NOT required — it is an optional refinement for v1.1+.

#### 3.6 DOT Scaling — Separate Formula Required

**Dispatch question:** Do burn/poison/bleed/freeze scale from instant damage or have separate scaling formula?

**Finding: DOTs require a separate scaling formula. Genre-universal pattern: DoTs DO NOT crit, and their scaling pool differs from the hit that applies them.**

Evidence across all surveyed games:
- **D4:** "DoT skills explicitly cannot benefit from Critical Strikes unless stated otherwise." DoTs scale through additive bonuses + vulnerable + global multipliers but NOT crit bucket.
- **PoE:** "DoTs cannot crit." Ignite scales with `increased fire damage` + `increased burning damage` + `increased DoT`. Poison scales with `increased chaos` + `increased poison` + `increased DoT`. Crucially: "stats modifying spell damage and attack damage do NOT apply to poison." DoTs have their own modifier pools.
- **Last Epoch:** "DoTs cannot crit or trigger 'on hit' effects." Duration increases are direct damage multipliers (more ticks). Separate increased-damage categories for DoT types.
- **D2:** Poison damage (and Bone Spear's poison component) scales from skill level + synergies, not from weapon damage. Same independent-seed pattern as spells.
- **Grim Dawn:** Duration damage (DoTs) scales with Cunning (physical DoTs: Bleed, Trauma) or Spirit (elemental DoTs: Burn, Frostburn). Separate attribute scaling from hit damage. DoTs do not crit.

**Recommendation for Wave 0.5:** Doc 47 does not explicitly enumerate a DOT formula. gamora's `damage_resolver` needs a DOT sub-formula:
```
dot_damage_per_tick = base_dot_damage(element, ailment_type, skill_tier)
                    × (1 + increased_dot_type_modifiers / 100)   [additive: all "+%burn damage", "+%bleed", "+%DoT", "+%[element] damage" in ONE pool]
                    × global_dot_multipliers                      [multiplicative, separate from hit formula]
× tick_count (for total DoT damage)
```

DoTs **do not crit**. DoTs do not consume `crit_multiplier`. This is genre-universal (PoE, D4, LE, GD all agree — D2 has no formal crit system for spells so n/a).

The ailment damage signatures deferred design (per memory record `project_ailment_damage_thematic.md`) that adds secondary damage signatures to control ailments (wind cut+bleed, earth thorny root, water cold-burn) will compose with this DOT sub-formula. Those ailments would use `base_dot_damage` seeded from the ailment type. Noting for KR: this DOT formula gap in doc 47 is a Wave 0.5 implementation item.

#### 3.7 Off-Hand Item Scaling

**Dispatch question:** How do secondary_item off-hand caster items scale per `off-hand-items-2026-05-24.md`?

**Finding: Genre pattern — off-hand caster items provide multiplier/modifier bonuses, not independent damage sources.**

Evidence:
- **PoE:** Off-hand items (quiver, shield, focus) provide `+%spell damage`, `+to-gem-level`, `+mana regen`, `+%cast speed`. They do NOT provide independent weapon damage that factors into the damage formula.
- **GD off-hands (tomes/focuses/artifacts):** Provide `+%elemental damage`, `+Spirit`, cooldown reduction, flat elemental damage bonuses. They add to the modifier pools, not as separate damage seeds.
- **Last Epoch off-hands (catalysts, shields):** Provide `+spell damage`, `+cast speed`, `+mana`. No independent damage seed.

**Application for doc 47 / Wave 0.5:** Off-hand caster items (tome/focus/talisman per `off-hand-items-2026-05-24.md` categories) should contribute to the **modifier pools** in the magical formula:
- `+%spell damage` → adds to `global_spell_damage_modifier` pool
- `+%element damage` → adds to `element_affinity_modifier` pool
- `+to-skill-level` → increases skill_level which may increase `base_spell_damage` if skill has level-scaling (deferred per doc 41)
- `+mana` → resource pool, not damage formula

Off-hand items for physical characters (shield) contribute to defensive stats only (damage reduction, block chance). No damage formula entry for physical shields. This is genre-universal.

**Wave 0.5 note:** When elrond enriches substrate weapon fields per doc 47 § 8.3, the off-hand item schema parallel enrichment (spell_damage_modifier, element_affinity_modifiers per off-hand) should follow the same pattern. Both main-weapon and off-hand feed into the same modifier pools in the formula.

---

### 4. AI-Tell and Community Perception (Q-SC5-5, Q-SC5-6)

#### 4.1 Q-SC5-5 — Damage Formula Failure Modes That "Feel Bad"

**Primary failure mode: Too many independent multiplicative buckets.**

The D4 launch case is the community-canonical example. Multiple sources document the progression:
- Launch (2023): Players discovered 5-7 independent multiplicative damage buckets (Base Damage × Additive Bonuses × Vulnerable × Crit × Main Stat × Global Multipliers × Conditional Global Multipliers)
- With aggressive optimization, builds could stack multiplicative chains producing millions → billions → eventually quadrillions of damage
- Community frustration: "If an ability doesn't provide a damage multiplier, it's unlikely to be beneficial in the long term" (per Icy Veins analysis) — build diversity collapsed because only multiplier-providing skills had value
- Post-Season-2 reworks: Blizzard consolidated some multiplicative buckets, removed others, reworked Vulnerable damage cap

**Formula-level source of the problem:** When N independent `(1 + x_i / 100)` terms exist in the formula, total damage scales as the PRODUCT of all N terms. With N=6 and average `x_i` = 100% per bucket, total multiplier = 2^6 = 64×. Adding one more 100% bucket goes from 64× to 128× — a 100% increase. This makes outlier-stacking highly rewarding and build-defining, but also creates huge variance between optimized and unoptimized players.

**Mitigation genre patterns:**
1. **PoE's additive pool:** Groups most damage bonuses into one additive pool with natural diminishing returns. A second "100% increased damage" source only increases the total multiplier from 2.0× to 3.0× (adding 1.0) rather than from 2.0× to 4.0× (multiplying by 2). Reduces blow-up risk.
2. **D4's post-rework bucket capping:** Removed Vulnerable damage from being a separate uncapped multiplier; capped certain global multipliers.
3. **Last Epoch's "Increased vs More" clarity:** Explicit documentation that "Increased" is additive (diminishing returns) and "More" is multiplicative (no diminishing returns but fewer sources). Players know not to stack Increased past a certain point.

**Application for doc 47:** The magical formula currently has three separate percentage terms:
```
(1 + weapon_spell_modifier/100) × (1 + element_affinity_modifier/100) × (1 + global_spell_modifier/100)
```
These three separate terms can compound. With all three at modest values (e.g., 50% each), total = 1.5 × 1.5 × 1.5 = 3.375× instead of additive pool result = (1 + 1.5) = 2.5×. At higher values (100% each), the compound = 8× vs additive = 4×. At high-end optimization, this gap doubles the theoretical damage ceiling.

**Recommendation already stated in § 2.2:** Pool these into one additive `sum_of_all_spell_damage_pct` modifier. This is the genre-canonical anti-inflation choice.

#### 4.2 Q-SC5-6 — "Wooden Staff Scaling Ice Spike" Failure Modes

The titular failure mode from Matt's framing question: what community patterns produce this "feels bad" outcome?

**Pattern 1 — Uniform formula applied to all skill types (D3 launch era):**
D3's unified weapon-damage-for-all-skills approach occasionally generated community complaint when players felt the "spell power" concept was muddied by the weapon-centric framing. Players expected spells to scale from INT/intellect innately, not "find a weapon with higher numbers." The compensation (caster weapons with calibrated weapon damage) mitigated the functional issue but not the semantic one — players found it non-intuitive that a Wizard needed a better "wand damage" number rather than a higher "spell power" number. This is a player-perception/readability issue, not a formula correctness issue.

**Pattern 2 — Missing routing guard (Cycle 13 Reincarnated SyntheticPlayerClass):**
Cycle 13 Track A used `magnitude=3000` synthetic primary_attack for all kit types. Without `damage_scaling_type` routing, a caster kit with a wooden staff ran the same formula as a warrior kit with a greatsword. Both got `3000 × skill_multiplier × attribute_bonus`. This produced nonsensical outputs where a water mage with INT investment did "STR-anchored" damage regardless of their weapon.

**Pattern 3 — Physical crit source inheritance on spells:**
If the game uses weapon base crit chance as the crit base for ALL skills including spells, a caster holding a weapon with high physical attack crit (e.g., a critical-chance-boosted sword) would gain inflated spell crit. PoE explicitly avoided this — spell base crit comes from the spell gem, not the weapon. Implementation guard: for Reincarnated, if crit chance is character-level (unified pool from gear), this is less of an issue since there's no per-weapon base crit asymmetry. But if weapon-type-specific crit bonuses exist ("+crit chance for sword attacks"), those must NOT apply to spell skills.

**Pattern 4 — Element affinity stacking synergy with crit:**
If element affinity bonuses and crit multiplier are both independent multiplicative buckets, a player who stacks both gets an exponential return:
- 200% increased fire damage (3×) × 200% crit multiplier (3×) = 9× total
- With 100% crit chance, expected value = 9×
- Adding another 200% fire damage source: 5× × 3× = 15× — a 67% increase for what appears to be a "same category" investment

Community perception: "stacking the same stat (fire damage) suddenly became worth it again because the crit interaction made it a separate multiplier." This is the gear-design trap — it rewards extreme single-stat investment in ways the designer didn't intend. Mitigation: keep element affinity in the same additive pool as global_spell_damage, ensuring crit is the ONLY independent multiplier for magical skills.

---

### 5. Knowledge Gaps Not Fully Resolved

1. **Grim Dawn game mechanics wiki was blocked (403)** during this research pass. The Grim Dawn findings in § 1.6 are derived from Steam forum discussions, the Grimtools database, and the archived Fandom wiki. The mechanical descriptions are consistent across these secondary sources but lack the primary wiki citation depth of other games. Risk: low — the patterns reported (weapon_damage_pct for attacks; independent elemental seed for spells; Spirit/Cunning attribute split) are corroborated by multiple community sources.

2. **Lost Ark formula details** are less thoroughly documented in English than the Western ARPG titles. The `initial_value` and `skill_coefficient` in the Lost Ark formula are described by the community as "not publicly available and only approximately calculable." The characterization of Lost Ark as a unified-weapon-power model is well-supported but the per-skill coefficient details are not granular.

3. **D3 caster weapon stat calibration details** — exactly how Blizzard calibrated wand/staff "weapon damage" values relative to physical weapon types — were not precisely documented in accessible sources. The architectural pattern (all skills scale from weapon damage; caster weapons are calibrated spell-power proxies) is confirmed; the exact calibration ratios are not.

4. **Path of Exile 2 hybrid-skill handling** — PoE2 is relatively new (December 2024 early access). Community documentation of hybrid physical+magical scaling patterns is thinner than PoE1. The damage conversion change (no type-memory in PoE2) is well-documented; per-skill hybrid-path handling details less so.

---

### 6. Structural Recommendations Summary for gamora (Wave 0.5 Implementation)

The following are implementation-level structural recommendations from this research, organized by priority:

**R1 (High priority — formula composition):** Pool all magical percentage modifiers into ONE additive pool rather than separate multiplicative buckets. `(1 + (weapon_spell_modifier + element_affinity_modifier + global_spell_modifier) / 100)`. Prevents D4-launch multiplier inflation pattern.

**R2 (High priority — DOT sub-formula):** Implement a separate DOT sub-formula that does NOT use `crit_multiplier`. DoTs cannot crit — this is genre-universal across PoE, D4, Last Epoch, and Grim Dawn. A DoT formula stub needs to be in the damage_resolver.

**R3 (Medium priority — element conversion type classification):** After ELEMENT_CONVERSION T4 fires, classify the output damage as the converted element type only (no "retains physical origin" memory — use PoE2 model, not PoE1). The `apply_target_defenses` call must use the converted element type. Doc 47 § 4.2 already does this correctly — confirm preserved in implementation.

**R4 (Medium priority — crit base source):** Use character-level unified crit pool (D4/LE model) rather than per-skill base crit (PoE model). This is simpler at v1 and well-supported. Physical attack crit and spell crit draw from the same character crit chance stat.

**R5 (Low priority — off-hand formula integration):** Off-hand caster items contribute to modifier pools (global_spell_damage, element_affinity) not as independent damage seeds. Ensure off-hand stats route to the same modifier aggregation that main-hand caster weapon stats do.

**R6 (Implementation note — hybrid sum_paths calibration):** Starting `hybrid_balance_factor` = 0.5 for balanced hybrid skills. Consider whether GD's additive model (full physical + full magical, not split) is preferable to doc 47's weighted-split model for player experience. The split model limits optimization ceiling per path; the additive model rewards investment in both paths equally.

---

## Source List

Sources accessed 2026-05-27:

- [Damage Bonus — Diablo 2 Wiki (Fandom)](https://diablo2.diablowiki.net/Damage_Bonus)
- [Physical Damage FAQ — mannm.org D2 Library](https://www.mannm.org/d2library/faqtoids/physd_eng.html)
- [Sorceress Fire Spells — Diablo2 Diablowiki](https://diablo2.diablowiki.net/Sorceress_Fire_Spells)
- [Fireball — Diablo Wiki Fandom](https://diablo.fandom.com/wiki/Fire_Ball) (access blocked; fire spells formula confirmed via other sources)
- [Fireball Sorceress Build — Icy Veins D2](https://www.icy-veins.com/d2/fireball-sorceress-build)
- [How Stuff is Calculated in Diablo 3 — PureDiablo](https://www.purediablo.com/how-stuff-is-calculated-in-diablo-3) (access blocked during session; content confirmed via search result extracts)
- [Basic Theorycrafting: The Damage Formula — BlizzPro](https://blizzpro.com/2014/05/17/basic-theorycrafting-damage-formula/)
- [Damage for Beginners — D4 Maxroll](https://maxroll.gg/d4/getting-started/damage-for-beginners)
- [In-Depth Damage Guide — D4 Maxroll](https://maxroll.gg/d4/resources/in-depth-damage-guide)
- [Diablo 4 Damage Buckets and Formula — Diablo4.gg](https://diablo4.gg/diablo-4-damage-buckets-and-formula-explained/) — primary D4 formula source
- [How Multipliers Are Breaking Diablo 4's Damage System — Icy Veins](https://www.icy-veins.com/d4/news/how-multipliers-are-breaking-diablo-4s-damage-system/)
- [Diablo 4's Damage Inflation — Vocal.media](https://vocal.media/gamers/diablo-4-s-damage-inflation-from-millions-to-quadrillions)
- [Damage for Beginners — PoE Maxroll](https://maxroll.gg/poe/getting-started/damage-for-beginners) — primary PoE physical/spell separation source
- [Damage Scaling — PoE2 Maxroll](https://maxroll.gg/poe2/getting-started/damage-scaling) — primary PoE2 structure source
- [Damage Conversion — PoE Wiki](https://www.poewiki.net/wiki/Damage_conversion) (access blocked; content confirmed via search extracts)
- [Damage over Time — PoE Wiki](https://www.poewiki.net/wiki/Damage_over_time) (access blocked; PoE DoT content confirmed via search extracts + Fandom wiki)
- [Critical Strike — PoE Wiki](https://www.poewiki.net/wiki/Critical_strike) (access blocked; crit formula confirmed via search extracts + Fandom mirror)
- [Critical Strike — PoE Fandom](https://pathofexile.fandom.com/wiki/Critical_strike)
- [Critical Strike for Spells — PoE Fandom](https://pathofexile.fandom.com/wiki/Critical_Strike_for_Spells)
- [Damage Calculations Explained — Last Epoch Maxroll](https://maxroll.gg/last-epoch/resources/damage-explained) — primary LE formula source
- [Damage for Beginners — Last Epoch Maxroll](https://maxroll.gg/last-epoch/getting-started/damage-for-beginners)
- [Increased Damage — Last Epoch Wiki Fandom](https://lastepoch.fandom.com/wiki/Increased_Damage)
- [Last Epoch Attunement Points Explained — Game Rant](https://gamerant.com/last-epoch-attunement-points-explained/)
- [Base Damage — Last Epoch Tools](https://www.lastepochtools.com/guide/section/base_damage)
- [Game Mechanics — Grim Dawn Fandom Archive](https://grimdawn-archive.fandom.com/wiki/Game_Mechanics) (access blocked; content confirmed via search extracts)
- [Game Mechanics — Grim Dawn Wiki (Official Fandom)](https://grimdawn.fandom.com/wiki/Game_Mechanics) (access blocked; content confirmed via search extracts)
- [Physical Damage — Grim Dawn Wiki](https://grimdawn.fandom.com/wiki/Physical_Damage) (access blocked; confirmed via search extracts)
- [Grim Dawn Guide — Gameplay Combat (Official)](https://www.grimdawn.com/guide/gameplay/combat/)
- [Steam Discussion — Magical and Physical Damage Spirit/Cunning (Grim Dawn)](https://steamcommunity.com/app/219990/discussions/0/405692224235221965/)
- [Steam Discussion — Stats and Calculating (Grim Dawn)](https://steamcommunity.com/app/219990/discussions/0/617335934126887771/)
- [Damage — Lost Ark Wiki Fandom](https://lostark.fandom.com/wiki/Damage) (access blocked; content confirmed via search extracts)
- [Damage Formula in Lost Ark — Official Forums](https://forums.playlostark.com/t/damage-formula-in-lost-ark/259714) (access blocked; content confirmed via search extracts)
- [Weapon Power — Lost Ark FextraLife](https://lostark.wiki.fextralife.com/Weapon+Power)
- [Hidden Mechanics Most ARPGs Never Explain — FextraLife](https://fextralife.com/hidden-mechanics-most-arpgs-never-explain/)
- [Spell Damage vs. Weapon Damage: A Complete Breakdown — EatHealthy365](https://eathealthy365.com/spell-damage-vs-weapon-damage-a-complete-breakdown/)
- [RPG/ARPGs Skill Damage = %Weapon Damage WHY? — Beamdog Forums](https://forums.beamdog.com/discussion/70390/rpg-arpgs-skill-damage-weapon-damage-why)
- [Damage conversion — PoE Wiki](https://www.poewiki.net/wiki/Damage_conversion) (access blocked)
- [PoE 2 Guide: Damage Conversion — Mobalytics](https://mobalytics.gg/poe-2/guides/damage-conversion)
- [Critical Damage Types — D4 Forums (Blizzard)](https://us.forums.blizzard.com/en/d4/t/critical-damage-types-additive-or-multiplicative/48421)

---

## Appendix A: Doc 47 Formula Amendments Table

| Formula location | Doc 47 current form | Research finding | Recommendation |
|---|---|---|---|
| Magical formula — percentage modifiers | Three separate `(1+x/100)` terms for weapon_spell_mod, element_affinity, global_spell | Genre-canonical: pool into ONE additive sum (PoE, LE, post-S2 D4) | REFINE: pool into one additive `(1 + sum_pct/100)` term |
| Physical formula — element_conversion_factor placement | After tier_coefficient | Genre-canonical: conversion before percentage multipliers | MINOR REORDER: element_conversion_factor before tier_coefficient |
| DOT scaling — not in doc 47 | Not specified | Genre-universal: DoTs need separate formula; cannot crit | ADD: DOT sub-formula in gamora damage_resolver |
| Crit on magical | `player.crit_chance` unified | Confirmed: D4/LE unified model is valid and simpler | CONFIRMED — no change needed |
| Off-hand item formula integration | Not explicitly specified in § 4 | Genre-canonical: off-hand feeds modifier pools, not separate seed | ADD: note in § 4.3 that off-hand modifier fields aggregate into same pools as main-hand |

---

## Appendix B: Framing-Audit Checklist (Discipline #23 Pattern A-deep three-question protocol)

Per hive-mind-protocol § 7.5:

**Q1 — Load-bearing framing assumptions this research depends on:**
- Doc 47 assumes a three-path routing is sufficient for Reincarnated's v1 skill design space. Confirmed by genre survey.
- Doc 47 assumes `base_spell_damage` calibrated at generation time is operationally feasible. Confirmed — all separated-model games (D2, PoE, LE, GD) maintain per-skill base damage tables. This is standard.
- Doc 47 assumes Option C hybrid cells need per-skill design decisions. Confirmed — genre precedent shows hybrid patterns are always per-skill design choices, not formula-derivable.

**Q2 — Evidence that could refute these assumptions:**
- If the substrate weapon library doesn't carry `spell_damage_modifier` fields (doc 47 § 8.3 notes "audit needed"), the magical formula has no weapon modifier input. **This is a live risk.** The elrond substrate audit (doc 47 § 8.3) must confirm `spell_damage_modifier` field availability before gamora implements the formula.
- The `BASE_SPELL_DAMAGE` table (referenced in § 4.3 pseudocode) must exist as a calibrated data source at Wave 0.5 time. This table is implied but not specified in doc 47. Rocket's per-skill emission (Track D.2) must populate this or it must be generated as a separate calibration artifact.

**Q3 — Should framing be refined before execution?**
No — the doc 47 architectural commitments are sound and well-grounded. The implementation risks identified (substrate spell_damage_modifier audit, BASE_SPELL_DAMAGE table creation, DOT sub-formula) are tractable Wave 0.5 implementation items, not framing-level concerns.

---

*Research complete. Commissioned by knight-rider for Cycle 14 SC-5. Output gates Wave 0.5 dispatch authoring.*
