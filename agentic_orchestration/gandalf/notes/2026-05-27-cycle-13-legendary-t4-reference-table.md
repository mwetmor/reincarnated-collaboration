# Cycle 13 — Legendary T1 + T4 Node Reference Table

> **Purpose:** comprehensive per-character per-slot reference for design conversation. Shows every worn legendary T1 item + every T4 node across all 16 characters. Use this to imagine gameplay scenarios and design improvements.

**Source:** `reincarnated-engine/output/cycle-13-mechanical-season-001/characters/`
**Generated:** 2026-05-27
**Author:** gandalf

---

## Summary statistics

- **16 characters** at endgame node (L45-50+); all class_chain_count=3
- **16 T4 candidates** (1 per character; 1 active per `one-T4-unlocked-at-a-time` lock 2026-05-27)
- **176 worn T1 legendary items** (16 chars × 11 slots: main_weapon + secondary_item + head + chest + hands + feet + legs + amulet + ring_1 + ring_2 + belt)
- **176 capability modifiers** (1 per legendary slot)
- Triggered_passives: not every slot has one; varies per character (typical 8-11 per character)

---

## dex_01_dagger_assassin

**Element:** wind · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=melee / tempo=high / amplitude=flat / attribute=DEX / proxy_density=none
**Resource model:** mana

### T4 Node (active)

- **candidate_id:** `wind_t4_chain_1_RESOURCE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `RESOURCE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 81.0 / 62.0 / 19.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 40.30 | 31.00 | 0.30 |
| chain_wide_own | 26.60 | 19.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 40.30 | 31.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `on_kill_explosion` (p=1.00): Triggers an explosion in a 3m radius for 40% weapon damage on kill |
| 2 | **secondary_item** | axis_adjusting | `cap_axis_damage_type_convert` | `chain_lightning_on_hit` (p=1.00): Chains lightning to the nearest enemy for 25% weapon damage on hit |
| 3 | **head** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 4 | **chest** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 5 | **hands** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | — |
| 6 | **feet** | axis_adjusting | `cap_axis_damage_type_convert` | `shield_on_low_hp` (p=0.90): Activates a damage-absorbing shield (10% max HP) below 25% HP |
| 7 | **legs** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `shield_on_low_hp` (p=0.90): Activates a damage-absorbing shield (10% max HP) below 25% HP |
| 8 | **amulet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | — |
| 9 | **ring_1** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |
| 10 | **ring_2** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |
| 11 | **belt** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |

---

## dex_02_archer

**Element:** wind · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=ranged / tempo=high / amplitude=flat / attribute=DEX / proxy_density=none
**Resource model:** mana

### T4 Node (active)

- **candidate_id:** `wind_t4_chain_1_TRADE_OFF_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `TRADE_OFF`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 72.0 / 62.0 / 10.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 28.60 | 22.00 | 0.30 |
| chain_wide_own | 14.00 | 10.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 28.60 | 22.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `thorny_on_hit` (p=1.00): Returns 15% of weapon damage to attacker as thorns damage on hit |
| 2 | **secondary_item** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `element_projectile_on_crit` (p=1.00): Fires an element-typed projectile on critical strike for 30% weapon dmg |
| 3 | **head** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 4 | **chest** | axis_adjusting | `cap_axis_damage_type_convert` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 5 | **hands** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 6 | **feet** | axis_adjusting | `cap_axis_damage_type_convert` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 7 | **legs** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 8 | **amulet** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | — |
| 9 | **ring_1** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_element_affinity` (p=0.75): Passive: +8% damage bonus to gear-element skill damage |
| 10 | **ring_2** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |
| 11 | **belt** | axis_adjusting | `cap_axis_damage_type_convert` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |

---

## dex_03_crossbow_sniper

**Element:** wind · **Cohort:** dps_min_maxer · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=ranged / tempo=low / amplitude=spiky / attribute=DEX / proxy_density=none
**Resource model:** cooldown

### T4 Node (active)

- **candidate_id:** `wind_t4_chain_1_DEFENSIVE_CONVERSION_ELEMENT_CONVERSION_character_wide`
- **Category A (character-wide):** `DEFENSIVE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `character_wide` · **parallel_chain_mode:** `own_chain` · **target_chain_id:** `None`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 72.0 / 62.0 / 10.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide ⬅ SELECTED | 31.50 | 21.00 | 0.50 |
| chain_wide_own | 11.70 | 9.00 | 0.30 |
| chain_wide_parallel | 25.20 | 21.00 | 0.20 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `geometric_aoe_on_hit` (p=1.00): Spawns a geometric AoE burst on successful hit for 20% weapon damage |
| 2 | **secondary_item** | axis_adjusting | `cap_axis_damage_type_convert` | **[TRUE-ACTIVE]** `true_active_secondary_skill` (p=1.00): Grants a secondary active skill slot not found in the skill tree |
| 3 | **head** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 4 | **chest** | axis_adjusting | `cap_axis_damage_type_convert` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 5 | **hands** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 6 | **feet** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | — |
| 7 | **legs** | axis_adjusting | `cap_axis_damage_type_convert` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 8 | **amulet** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | — |
| 9 | **ring_1** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_element_affinity` (p=0.75): Passive: +8% damage bonus to gear-element skill damage |
| 10 | **ring_2** | triggered_passive | `cap_triggered_passive_on_kill_burst` | — |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |

---

## dex_04_twin_blade_fencer

**Element:** wind · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=mid / tempo=high / amplitude=flat / attribute=DEX / proxy_density=none
**Resource model:** mana

### T4 Node (active)

- **candidate_id:** `wind_t4_chain_2_RESOURCE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `RESOURCE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_1`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 81.0 / 62.0 / 19.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 40.30 | 31.00 | 0.30 |
| chain_wide_own | 26.60 | 19.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 40.30 | 31.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `chain_lightning_on_hit` (p=1.00): Chains lightning to the nearest enemy for 25% weapon damage on hit |
| 2 | **secondary_item** | axis_adjusting | `cap_axis_damage_type_convert` | **[TRUE-ACTIVE]** `true_active_secondary_skill` (p=1.00): Grants a secondary active skill slot not found in the skill tree |
| 3 | **head** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 4 | **chest** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 5 | **hands** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 6 | **feet** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 7 | **legs** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 8 | **amulet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 9 | **ring_1** | axis_adjusting | `cap_axis_damage_type_convert` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 10 | **ring_2** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |
| 11 | **belt** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_element_affinity` (p=0.75): Passive: +8% damage bonus to gear-element skill damage |

---

## int_01_standard_wizard

**Element:** fire · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=ranged / tempo=medium / amplitude=variable / attribute=INT / proxy_density=none
**Resource model:** energy

### T4 Node (active)

- **candidate_id:** `fire_t4_chain_1_DEFENSIVE_TRADEOFF_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `DEFENSIVE_TRADEOFF`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 74.0 / 62.0 / 12.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 31.20 | 24.00 | 0.30 |
| chain_wide_own | 16.80 | 12.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 31.20 | 24.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `on_kill_explosion` (p=1.00): Triggers an explosion in a 3m radius for 40% weapon damage on kill |
| 2 | **secondary_item** | triggered_passive | `cap_triggered_passive_on_hit_regen` | **[TRUE-ACTIVE]** `true_active_secondary_skill` (p=1.00): Grants a secondary active skill slot not found in the skill tree |
| 3 | **head** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 4 | **chest** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 5 | **hands** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 6 | **feet** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 7 | **legs** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `shield_on_low_hp` (p=0.90): Activates a damage-absorbing shield (10% max HP) below 25% HP |
| 8 | **amulet** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 9 | **ring_1** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 10 | **ring_2** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_on_kill_regen` (p=0.75): Passive: regenerates 3% resource on kill |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `general_passive_cooldown_reduce` (p=0.75): Passive: -5% cooldown on all skills while equipped |

---

## int_03_pyromantic_caster

**Element:** fire · **Cohort:** dps_min_maxer · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=mid / tempo=low / amplitude=spiky / attribute=INT / proxy_density=none
**Resource model:** cooldown

### T4 Node (active)

- **candidate_id:** `fire_t4_chain_1_RESOURCE_CONVERSION_ELEMENT_CONVERSION_character_wide`
- **Category A (character-wide):** `RESOURCE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `character_wide` · **parallel_chain_mode:** `own_chain` · **target_chain_id:** `None`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 86.0 / 62.0 / 24.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide ⬅ SELECTED | 54.00 | 36.00 | 0.50 |
| chain_wide_own | 31.20 | 24.00 | 0.30 |
| chain_wide_parallel | 43.20 | 36.00 | 0.20 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `freeze_on_crit` (p=1.00): Applies freeze debuff (0.5s) to target on critical strike |
| 2 | **secondary_item** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `on_kill_explosion` (p=1.00): Triggers an explosion in a 3m radius for 40% weapon damage on kill |
| 3 | **head** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 4 | **chest** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `thorns_on_being_hit` (p=0.90): Returns thorns damage equal to 20% of attack damage on being hit |
| 5 | **hands** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 6 | **feet** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 7 | **legs** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 8 | **amulet** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | — |
| 9 | **ring_1** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `general_passive_element_affinity` (p=0.75): Passive: +8% damage bonus to gear-element skill damage |
| 10 | **ring_2** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `general_passive_move_speed` (p=0.75): Passive: +6% movement speed while equipped |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_hit_regen` | — |

---

## int_04_red_mage_spellsword

**Element:** fire · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=melee / tempo=high / amplitude=flat / attribute=INT / proxy_density=none
**Resource model:** mana

### T4 Node (active)

- **candidate_id:** `fire_t4_chain_1_RESOURCE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `RESOURCE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 86.0 / 62.0 / 24.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | -2.92 | -2.25 | 0.30 |
| chain_wide_own | -19.95 | -14.25 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | -2.92 | -2.25 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `freeze_on_crit` (p=1.00): Applies freeze debuff (0.5s) to target on critical strike |
| 2 | **secondary_item** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `thorny_on_hit` (p=1.00): Returns 15% of weapon damage to attacker as thorns damage on hit |
| 3 | **head** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 4 | **chest** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | — |
| 5 | **hands** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 6 | **feet** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 7 | **legs** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 8 | **amulet** | triggered_passive | `cap_triggered_passive_on_hit_regen` | — |
| 9 | **ring_1** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |
| 10 | **ring_2** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_move_speed` (p=0.75): Passive: +6% movement speed while equipped |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |

---

## int_05_arcane_familiar_mage

**Element:** fire · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=ranged / tempo=medium / amplitude=variable / attribute=INT / proxy_density=light
**Resource model:** energy

### T4 Node (active)

- **candidate_id:** `fire_t4_chain_2_DEFENSIVE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `DEFENSIVE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_1`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 74.0 / 62.0 / 12.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 31.20 | 24.00 | 0.30 |
| chain_wide_own | 16.80 | 12.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 31.20 | 24.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `geometric_aoe_on_hit` (p=1.00): Spawns a geometric AoE burst on successful hit for 20% weapon damage |
| 2 | **secondary_item** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `thorny_on_hit` (p=1.00): Returns 15% of weapon damage to attacker as thorns damage on hit |
| 3 | **head** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 4 | **chest** | axis_adjusting | `cap_axis_damage_type_convert` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 5 | **hands** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 6 | **feet** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 7 | **legs** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `shield_on_low_hp` (p=0.90): Activates a damage-absorbing shield (10% max HP) below 25% HP |
| 8 | **amulet** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |
| 9 | **ring_1** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | — |
| 10 | **ring_2** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_on_kill_regen` (p=0.75): Passive: regenerates 3% resource on kill |
| 11 | **belt** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | — |

---

## str_01_heavy_barbarian

**Element:** earth · **Cohort:** dps_min_maxer · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=melee / tempo=low / amplitude=spiky / attribute=STR / proxy_density=none
**Resource model:** cooldown

### T4 Node (active)

- **candidate_id:** `earth_t4_chain_1_DEFENSIVE_CONVERSION_ELEMENT_CONVERSION_character_wide`
- **Category A (character-wide):** `DEFENSIVE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `character_wide` · **parallel_chain_mode:** `own_chain` · **target_chain_id:** `None`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 72.0 / 62.0 / 10.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide ⬅ SELECTED | 33.00 | 22.00 | 0.50 |
| chain_wide_own | 13.00 | 10.00 | 0.30 |
| chain_wide_parallel | 26.40 | 22.00 | 0.20 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `thorny_on_hit` (p=1.00): Returns 15% of weapon damage to attacker as thorns damage on hit |
| 2 | **secondary_item** | spatial_adjusting | `cap_spatial_adjust_range_extend` | **[TRUE-ACTIVE]** `true_active_secondary_skill` (p=1.00): Grants a secondary active skill slot not found in the skill tree |
| 3 | **head** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 4 | **chest** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 5 | **hands** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 6 | **feet** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `thorns_on_being_hit` (p=0.90): Returns thorns damage equal to 20% of attack damage on being hit |
| 7 | **legs** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 8 | **amulet** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_on_kill_regen` (p=0.75): Passive: regenerates 3% resource on kill |
| 9 | **ring_1** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 10 | **ring_2** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_element_affinity` (p=0.75): Passive: +8% damage bonus to gear-element skill damage |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_hit_regen` | — |

---

## str_02_light_fighter

**Element:** earth · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=melee / tempo=high / amplitude=flat / attribute=STR / proxy_density=none
**Resource model:** mana

### T4 Node (active)

- **candidate_id:** `earth_t4_chain_1_TRADE_OFF_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `TRADE_OFF`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 72.0 / 62.0 / 10.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 28.60 | 22.00 | 0.30 |
| chain_wide_own | 14.00 | 10.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 28.60 | 22.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `freeze_on_crit` (p=1.00): Applies freeze debuff (0.5s) to target on critical strike |
| 2 | **secondary_item** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `on_kill_explosion` (p=1.00): Triggers an explosion in a 3m radius for 40% weapon damage on kill |
| 3 | **head** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 4 | **chest** | axis_adjusting | `cap_axis_damage_type_convert` | — |
| 5 | **hands** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 6 | **feet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 7 | **legs** | axis_adjusting | `cap_axis_damage_type_convert` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 8 | **amulet** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |
| 9 | **ring_1** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 10 | **ring_2** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |

---

## str_03_polearm_soldier

**Element:** earth · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=melee / tempo=medium / amplitude=variable / attribute=STR / proxy_density=none
**Resource model:** energy

### T4 Node (active)

- **candidate_id:** `earth_t4_chain_1_DEFENSIVE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `DEFENSIVE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 74.0 / 62.0 / 12.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 31.20 | 24.00 | 0.30 |
| chain_wide_own | 16.80 | 12.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 31.20 | 24.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `thorny_on_hit` (p=1.00): Returns 15% of weapon damage to attacker as thorns damage on hit |
| 2 | **secondary_item** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `chain_lightning_on_hit` (p=1.00): Chains lightning to the nearest enemy for 25% weapon damage on hit |
| 3 | **head** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 4 | **chest** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `shield_on_low_hp` (p=0.90): Activates a damage-absorbing shield (10% max HP) below 25% HP |
| 5 | **hands** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `shield_on_low_hp` (p=0.90): Activates a damage-absorbing shield (10% max HP) below 25% HP |
| 6 | **feet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 7 | **legs** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 8 | **amulet** | axis_adjusting | `cap_axis_damage_type_convert` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |
| 9 | **ring_1** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `general_passive_element_affinity` (p=0.75): Passive: +8% damage bonus to gear-element skill damage |
| 10 | **ring_2** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `general_passive_move_speed` (p=0.75): Passive: +6% movement speed while equipped |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |

---

## wis_01_channeling_cleric

**Element:** water · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=mid / tempo=medium / amplitude=variable / attribute=WIS / proxy_density=none
**Resource model:** energy

### T4 Node (active)

- **candidate_id:** `water_t4_chain_1_RESOURCE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `RESOURCE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 78.0 / 62.0 / 16.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 24.70 | 19.00 | 0.30 |
| chain_wide_own | 9.80 | 7.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 24.70 | 19.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `freeze_on_crit` (p=1.00): Applies freeze debuff (0.5s) to target on critical strike |
| 2 | **secondary_item** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `life_steal_on_hit` (p=1.00): Restores 2% max HP per hit (stacks up to 3x per second) |
| 3 | **head** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 4 | **chest** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 5 | **hands** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `shield_on_low_hp` (p=0.90): Activates a damage-absorbing shield (10% max HP) below 25% HP |
| 6 | **feet** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 7 | **legs** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 8 | **amulet** | axis_adjusting | `cap_axis_damage_type_convert` | `general_passive_defense_aura` (p=0.75): Passive: +5% all damage reduction while equipped |
| 9 | **ring_1** | spatial_adjusting | `cap_spatial_adjust_range_extend` | — |
| 10 | **ring_2** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_cooldown_reduce` (p=0.75): Passive: -5% cooldown on all skills while equipped |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |

---

## wis_02_holy_knight

**Element:** water · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=melee / tempo=medium / amplitude=variable / attribute=WIS / proxy_density=none
**Resource model:** energy

### T4 Node (active)

- **candidate_id:** `water_t4_chain_1_DEFENSIVE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `DEFENSIVE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 74.0 / 62.0 / 12.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 31.20 | 24.00 | 0.30 |
| chain_wide_own | 16.80 | 12.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 31.20 | 24.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `chain_lightning_on_hit` (p=1.00): Chains lightning to the nearest enemy for 25% weapon damage on hit |
| 2 | **secondary_item** | axis_adjusting | `cap_axis_damage_type_convert` | `on_kill_explosion` (p=1.00): Triggers an explosion in a 3m radius for 40% weapon damage on kill |
| 3 | **head** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 4 | **chest** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 5 | **hands** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `thorns_on_being_hit` (p=0.90): Returns thorns damage equal to 20% of attack damage on being hit |
| 6 | **feet** | axis_adjusting | `cap_axis_damage_type_convert` | — |
| 7 | **legs** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `thorns_on_being_hit` (p=0.90): Returns thorns damage equal to 20% of attack damage on being hit |
| 8 | **amulet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |
| 9 | **ring_1** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | — |
| 10 | **ring_2** | triggered_passive | `cap_triggered_passive_on_kill_burst` | — |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_cooldown_reduce` (p=0.75): Passive: -5% cooldown on all skills while equipped |

---

## wis_03_ritual_mage

**Element:** water · **Cohort:** dps_min_maxer · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=ranged / tempo=low / amplitude=spiky / attribute=WIS / proxy_density=none
**Resource model:** cooldown

### T4 Node (active)

- **candidate_id:** `water_t4_chain_1_RESOURCE_CONVERSION_ELEMENT_CONVERSION_character_wide`
- **Category A (character-wide):** `RESOURCE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `character_wide` · **parallel_chain_mode:** `own_chain` · **target_chain_id:** `None`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 86.0 / 62.0 / 24.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide ⬅ SELECTED | 54.00 | 36.00 | 0.50 |
| chain_wide_own | 31.20 | 24.00 | 0.30 |
| chain_wide_parallel | 43.20 | 36.00 | 0.20 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `life_steal_on_hit` (p=1.00): Restores 2% max HP per hit (stacks up to 3x per second) |
| 2 | **secondary_item** | axis_adjusting | `cap_axis_damage_type_convert` | `curse_on_hit` (p=1.00): Applies curse debuff reducing target defenses by 10% for 3s on hit |
| 3 | **head** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `thorns_on_being_hit` (p=0.90): Returns thorns damage equal to 20% of attack damage on being hit |
| 4 | **chest** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `cleanse_on_cc` (p=0.90): Cleanses one CC effect and grants 1s CC-immunity on being CCed |
| 5 | **hands** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 6 | **feet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 7 | **legs** | axis_adjusting | `cap_axis_damage_type_convert` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 8 | **amulet** | axis_adjusting | `cap_axis_damage_type_convert` | — |
| 9 | **ring_1** | triggered_passive | `cap_triggered_passive_on_kill_burst` | — |
| 10 | **ring_2** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |
| 11 | **belt** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `general_passive_move_speed` (p=0.75): Passive: +6% movement speed while equipped |

---

## wis_04_storm_caller

**Element:** water · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=ranged / tempo=medium / amplitude=variable / attribute=WIS / proxy_density=none
**Resource model:** energy

### T4 Node (active)

- **candidate_id:** `water_t4_chain_1_DEFENSIVE_CONVERSION_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `DEFENSIVE_CONVERSION`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 74.0 / 62.0 / 12.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 31.20 | 24.00 | 0.30 |
| chain_wide_own | 16.80 | 12.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 31.20 | 24.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `element_projectile_on_crit` (p=1.00): Fires an element-typed projectile on critical strike for 30% weapon dmg |
| 2 | **secondary_item** | spatial_adjusting | `cap_spatial_adjust_range_extend` | **[TRUE-ACTIVE]** `true_active_secondary_skill` (p=1.00): Grants a secondary active skill slot not found in the skill tree |
| 3 | **head** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 4 | **chest** | mechanic_adjusting | `cap_mechanic_adjust_aoe_persist` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 5 | **hands** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `element_resist_on_hit` (p=0.90): Grants +15% elemental resistance for 2s after being hit |
| 6 | **feet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 7 | **legs** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 8 | **amulet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `general_passive_move_speed` (p=0.75): Passive: +6% movement speed while equipped |
| 9 | **ring_1** | spatial_adjusting | `cap_spatial_adjust_aoe_radius` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |
| 10 | **ring_2** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `general_passive_cooldown_reduce` (p=0.75): Passive: -5% cooldown on all skills while equipped |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `general_passive_move_speed` (p=0.75): Passive: +6% movement speed while equipped |

---

## wis_05_monk

**Element:** water · **Cohort:** balanced · **Chain count:** 3 (2 T4-chain + 1 supporting)
**BC tuple:** range=melee / tempo=high / amplitude=variable / attribute=WIS / proxy_density=none
**Resource model:** mana

### T4 Node (active)

- **candidate_id:** `water_t4_chain_1_TRADE_OFF_ELEMENT_CONVERSION_chain_wide_parallel`
- **Category A (character-wide):** `TRADE_OFF`
- **Category B/C (chain-specific):** `C: ELEMENT_CONVERSION`
- **T4 scope:** `chain_wide_parallel` · **parallel_chain_mode:** `parallel` · **target_chain_id:** `t4_chain_2`
- **Magnitude tier:** `null` · **Magnitude midpoint:** `null`
- **Resolve / Create / Net synergy:** 79.0 / 62.0 / 17.0
- **Separability pass:** True · **Pattern 9/10 WARN:** False/False

**Scope projection (algorithm weighed all 3 scopes; selected the highest weighted_score):**

| Scope option | weighted_score | net_synergy | prior_weight |
|---|---|---|---|
| character_wide | 37.70 | 29.00 | 0.30 |
| chain_wide_own | 23.80 | 17.00 | 0.40 |
| chain_wide_parallel ⬅ SELECTED | 37.70 | 29.00 | 0.30 |

### Worn Legendary T1 Items (11 slots)

| # | Slot | Capability category | Capability modifier | Triggered passive (pattern + description) |
|---|---|---|---|---|
| 1 | **main_weapon** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | `element_projectile_on_crit` (p=1.00): Fires an element-typed projectile on critical strike for 30% weapon dmg |
| 2 | **secondary_item** | triggered_passive | `cap_triggered_passive_on_crit_chain` (restriction: weapon_only) | `on_kill_explosion` (p=1.00): Triggers an explosion in a 3m radius for 40% weapon damage on kill |
| 3 | **head** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `stun_on_being_hit` (p=0.90): 10% chance to stun attacker for 0.3s on being hit |
| 4 | **chest** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 5 | **hands** | triggered_passive | `cap_triggered_passive_on_kill_burst` | `speed_boost_on_dodge` (p=0.90): Grants +20% movement speed for 2s on successful dodge |
| 6 | **feet** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `counter_on_block` (p=0.90): Counter-attacks for 25% weapon damage on successful block |
| 7 | **legs** | spatial_adjusting | `cap_spatial_adjust_range_extend` | `reflect_on_being_hit` (p=0.90): Reflects 15% of incoming physical damage back to attacker |
| 8 | **amulet** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | — |
| 9 | **ring_1** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_crit_boost` (p=0.75): Passive: +5% critical hit chance while equipped |
| 10 | **ring_2** | mechanic_adjusting | `cap_mechanic_adjust_proj_bounce` | — |
| 11 | **belt** | triggered_passive | `cap_triggered_passive_on_hit_regen` | `general_passive_resource_regen` (p=0.75): Passive: +8% resource regeneration rate while equipped |

---

## Cross-character observations (after producing the table above)

### T4 Category B/C distribution

**100% of characters: Category C = ELEMENT_CONVERSION.** Zero Category B (multiplicative). Zero DUAL_ELEMENT_ADDITION. The 3-category taxonomy + new DUAL_ELEMENT_ADDITION strategy we locked in our 2026-05-27 Pattern-B session is operationally collapsed to a single B/C strategy.

### True-active discipline drift

Per D55 lock: true-actives are WEAPONS-ONLY. The data shows `true_active_secondary_skill` appearing on `secondary_item` (off-hand) slot for 4 of 16 characters — violating D55.

Affected characters:
- dex_03_crossbow_sniper (secondary_item)
- dex_04_twin_blade_fencer (secondary_item)
- int_01_standard_wizard (secondary_item)
- str_01_heavy_barbarian (secondary_item)
- wis_04_storm_caller (secondary_item)

### Capability category 0-count

Across 176 legendary slots:
- **multiplicative**: 0 (doc 40 D54 lock — should appear on Tier 1+2; not firing)
- **added_skill_true_active** (in capability_modifiers): 0 (true-actives appear only in triggered_passive field, not capability)

### Triggered_passive deduplication needed

Per-character pattern_id duplicate detection (same pattern_id appearing on 2+ slots):
- **dex_01_dagger_assassin**: `cleanse_on_cc` ×2, `shield_on_low_hp` ×2, `general_passive_resource_regen` ×2
- **dex_02_archer**: `cleanse_on_cc` ×2, `general_passive_crit_boost` ×2
- **dex_03_crossbow_sniper**: `cleanse_on_cc` ×2
- **dex_04_twin_blade_fencer**: `speed_boost_on_dodge` ×2, `cleanse_on_cc` ×2, `general_passive_defense_aura` ×2
- **int_01_standard_wizard**: `general_passive_defense_aura` ×2
- **int_03_pyromantic_caster**: `cleanse_on_cc` ×2
- **int_04_red_mage_spellsword**: `general_passive_crit_boost` ×2
- **str_01_heavy_barbarian**: `reflect_on_being_hit` ×2
- **str_02_light_fighter**: `speed_boost_on_dodge` ×2, `general_passive_resource_regen` ×2, `general_passive_defense_aura` ×2
- **str_03_polearm_soldier**: `stun_on_being_hit` ×2, `shield_on_low_hp` ×2
- **wis_01_channeling_cleric**: `element_resist_on_hit` ×2
- **wis_02_holy_knight**: `thorns_on_being_hit` ×2
- **wis_04_storm_caller**: `counter_on_block` ×2, `reflect_on_being_hit` ×2, `general_passive_move_speed` ×2
- **wis_05_monk**: `speed_boost_on_dodge` ×2

### Same-trigger-window stacking (the heavy_barbarian pattern)

Per-character count of effects on overlapping trigger windows. Multiple effects on the same trigger window stack chaotically:

| Character | on_being_hit-family effects | on_block-family effects | on_crit-family effects |
|---|---|---|---|
| dex_01_dagger_assassin | 3 | 2 | 0 |
| dex_02_archer | 5 | 1 | 1 |
| dex_03_crossbow_sniper | 5 | 0 | 0 |
| dex_04_twin_blade_fencer | 3 | 1 | 0 |
| int_01_standard_wizard | 2 | 2 | 0 |
| int_03_pyromantic_caster | 4 | 1 | 1 |
| int_04_red_mage_spellsword | 4 | 1 | 1 |
| int_05_arcane_familiar_mage | 6 | 1 | 0 |
| str_01_heavy_barbarian | 5 | 1 | 0 |
| str_02_light_fighter | 1 | 1 | 1 |
| str_03_polearm_soldier | 4 | 3 | 0 |
| wis_01_channeling_cleric | 3 | 2 | 1 |
| wis_02_holy_knight | 4 | 1 | 0 |
| wis_03_ritual_mage | 6 | 0 | 0 |
| wis_04_storm_caller | 3 | 2 | 1 |
| wis_05_monk | 2 | 1 | 1 |

---

## Reading guide — for the design conversation

Imagine each character at endgame engagement (L50, fully geared). Walk through the loadout slot-by-slot and ask:

1. **Core identity check** — without any of the 11 legendary items, just chain composition + T4: what kind of character is this?
2. **Thematic seed check** — looking at the 11 legendary items, can the cohesion-judge LLM synthesize a richer thematic identity ("explosive frost-fire")? Or is it template redundancy?
3. **Mechanical chaos check** — what fires when the player is hit? When they crit? When they kill? Are there 2+ effects competing for the same trigger window?
4. **D55 weapons-only check** — is true-active appearing where it shouldn't (off-hand instead of weapon)?
5. **Element coherence check** — fire mage with freeze_on_crit is thematic SEED (good); thorny + reflect ×4 is REDUNDANCY (bad).

---

**Signed:** gandalf · 2026-05-27 · for the wider-angle design conversation on capability density + cohesion-judge architecture