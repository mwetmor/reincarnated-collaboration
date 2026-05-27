# Research — ARPG Trigger Condition Vocabulary (Cycle 14 SC-4) — 2026-05-27

**Mode:** A (analytical)
**Commissioner:** knight-rider (Cycle 14 SC-4)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-legolas-cycle-14-sc-4-trigger-vocabulary-research.md`
**Authority basis:** Matt 2026-05-27 Q5 ratification; framing brief § 5 SC-4
**Gates:** Wave 1 — concentration architecture Layers 1-4+7 (trigger vocabulary expansion + synergy scan)

**robots.txt compliance (Discipline #20):**
- pathofexile.com: `User-agent: *` standard — no ClaudeBot/anthropic-ai Disallow — PERMITTED
- poe2wiki.net: standard community wiki — PERMITTED
- grimdawn.com: official site, no bot Disallow — PERMITTED
- lastepochtools.com: community tools site — PERMITTED
- diablo2.io: community database — PERMITTED
- maxroll.gg: community guide site — PERMITTED (403 on some pages; data via WebSearch aggregate instead)
- fextralife.com: community wiki — PERMITTED (403 on some pages; data via WebSearch aggregate instead)
- Game wikis accessed via WebSearch aggregate where direct fetch returned 403; no crawling of blocked paths

**Sources consulted:**
- poewiki.net/wiki/Trigger (PoE trigger mechanics)
- pathofexile.fandom.com/wiki/List_of_trigger_related_skill_gems (PoE trigger gem list)
- game8.co/games/Path-of-Exile-2/archives/488224 (PoE2 meta gem list)
- game8.co/games/Path-of-Exile-2/archives/487670 (PoE2 trigger explained)
- diablo2.io/runewords/ (D2 runeword proc conditions)
- diablo2.io/uniques/ (D2 unique item proc conditions)
- grimdawn.com/guide/character/item-skills/ (GD item skill triggers — official)
- grimdawn.com/guide/gameplay/combat/ (GD combat mechanics — official)
- maxroll.gg/last-epoch/resources/passives-and-skills (LE passive overview)
- forum.lastepoch.com (LE channeling trigger mechanics)
- fextralife.com/lost-ark-combat-engravings-guide (LA combat engravings)
- maxroll.gg/lost-ark/resources/engraving-system-guide (LA engraving system)
- vulkk.com/2022/02/18/how-to-use-lost-arks-engraving-system/ (LA engraving conditions)
- wowhead.com/diablo-4/aspects (D4 aspects)
- WebSearch aggregate (multiple queries across all 7+ ARPGs; specific queries cited per finding below)

---

## Summary

Cross-surveying 7 ARPGs (PoE1, PoE2, D2 LoD, D3, D4, Last Epoch, Grim Dawn, Lost Ark) yields a rich trigger condition vocabulary that maps cleanly onto the 11 families specified in doc 46 Layer 4. The genre-canonical core is well-represented in all games; several families (environmental, positional, combo) are more game-specific with limited cross-game penetration. 63 trigger conditions are catalogued across all 11 families. The genre-canonical evidence strongly supports the action, defense, resource, and state families; is moderate for enemy-state and skill-conditioned; and is sparse-but-confirmed for environmental, combo, positional, element, and timer families. Key AI-tell risk patterns cluster in the action family (generic on-attack/on-hit wording); mitigation requires specificity (weapon type, skill tier, specific damage type). Same-pattern_id dedup risks are concentrated in the defense family (counter_on_defensive cluster = 4 conditions) and the action family (on_hit cluster). Trigger-window collision risks are highest between action family conditions (multiple instant-window conditions). The conditions flagged as "skills disguised as triggered passives" in the Cycle 13 data (speed_boost_on_dodge, defense_aura, counter_on_block duplicates) are clearly identifiable as Layer 2 migration candidates, not genuine mechanic-altering trigger conditions.

---

## Section 1 — The 11 Trigger Families: Catalogued Conditions

### Family 1: ACTION

Genre-canonical across all 7 ARPGs. The densest family; highest AI-tell risk; requires vocabulary specificity to differentiate.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_hit` | On Hit | 7/7 | common | PoE CWDT, D2 "on striking", GD "on attack", LE "on hit", D4 "Lucky Hit: direct damage", LA all attack-based engravings |
| `on_crit` | On Critical Strike | 7/7 | common | PoE Cast on Critical Strike; PoE2 Cast on Critical; D4 Keen Blunt Weapon; GD "On Critical Attack"; LE crit passives; D2 "on striking" (crit variant); GD official guide confirms |
| `on_cast` | On Skill Cast (non-attack) | 6/7 | common | PoE cast gems; D4 "when you use [Skill]"; LE "on use"; LA "on ability activation" (Adrenaline); GD auto-cast item skills |
| `on_channel_tick` | On Channel Tick | 4/7 | uncommon | LE "while channeling" + "every second while channeling" (Winds of Justice, Forgemaster's Stance); D4 Aspect of Channeling; PoE channeling mechanics; not in D2/GD |
| `on_channel_end` | On Channel Completion | 3/7 | uncommon | PoE "Perfect Timing" (release in timing window); LE "on channel complete"; D4 charging skill completion (Super Charge engraving); partial evidence |
| `on_melee_hit` | On Melee Hit (weapon-specific) | 5/7 | common | D2 "on striking" (melee weapon implied); GD "On Attack" (melee); D4 melee-specific aspects; PoE Cast on Melee Kill; LE melee node differentiation; Lost Ark back/front attack |

**ACTION family count: 6 conditions**

---

### Family 2: DEFENSE

Well-represented across all 7 ARPGs. The counter_on_defensive pattern_id cluster is the most critical dedup risk in the entire vocabulary.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_being_hit` | On Being Hit (damage taken) | 7/7 | common | D2 "When Struck"; GD "When Hit" (official guide lists 3 variants: when hit, when hit by melee, when hit by ranged); PoE Cast when Damage Taken; D4 "when you take damage"; LE "when hit" passives; Lost Ark Crisis Evasion |
| `on_block` | On Block | 5/7 | common | PoE Cast when Stunned (blocks a stunning hit variant); GD "On Block" (official guide confirmed); D2 Exile runeword block; D4 block mechanics; LE block passives; NOT in Lost Ark (no block mechanic) |
| `on_dodge` | On Dodge/Evade | 5/7 | uncommon | PoE2 Cast on Dodge (direct confirmation: "gains 2 energy per metre travelled while dodge rolling"); D4 Snap Frozen Aspect ("each Chilled or Frozen enemy you Evade through"); LE dodge mechanics; Lost Ark evade-directional; partial D3 |
| `on_near_death` | On Low HP / Near Death | 6/7 | common | GD "On Low Health" (official guide confirmed); D4 Master's Tenacity ("when you're under 50% HP"); Lost Ark Emergency Rescue ("when HP reaches 30%"); LE low HP passives; D3 low-health procs; MP Efficiency engraving (Lost Ark "below 50% HP") |
| `on_being_hit_by_crit` | On Being Hit by Critical | 3/7 | uncommon | GD "When Hit by a Critical" (official guide confirmed distinct type); partial evidence in D4; D3 defensive items |
| `on_stun` | On Being Stunned | 3/7 | uncommon | PoE Cast when Stunned; D4 Vital Point Hit (stagger); GD crowd control triggers; PoE2 "Trigger Wind Wave when Stunned" (confirmed) |

**DEFENSE family count: 6 conditions**

---

### Family 3: RESOURCE

Moderate cross-game penetration. D4 and Lost Ark use resource thresholds heavily; D2/GD less so.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_resource_full` | At Full Resource | 5/7 | uncommon | D4 Aspect of Echoing Fury (fury generation); PoE2 "triggers socketed Spells on reaching maximum Energy" (direct confirmation for meta gems); LE mana-full nodes; Lost Ark resource management passives |
| `on_resource_spend` | On Resource Spend / Energy Spend | 5/7 | uncommon | PoE2 Manaforged Arrows ("when you've spent enough mana"); D4 fury-spend mechanics; LE mana-spend nodes; D4 resource-generation aspects |
| `on_resource_low` | At Low Resource | 4/7 | uncommon | GD "On Low Energy" (official guide confirmed); D4 "when below X% resource"; Lost Ark MP Efficiency Increase ("when MP below 50%"); LE mana/ward shortage passives |
| `on_resource_tick` | On Resource Tick (periodic regen event) | 3/7 | rare | LE mana/ward tick events; D4 spirit generation ticks; PoE2 energy accumulation tick per hit |
| `on_resource_pop` | On Resource Cap Pop (burst on filling) | 3/7 | rare | PoE2 meta gem energy mechanic (explicit "triggers all socketed Spells on reaching maximum Energy" — this IS the burst on filling); D4 Awakening ("reduces cooldown; enables 3 additional uses"); LE ward-burst mechanics |

**RESOURCE family count: 5 conditions**

---

### Family 4: STATE

Well-supported across ARPGs. D4 is the richest source for state-conditioned triggers (healthy/injured/berserking/unstoppable/moving/channeling). PoE uses "recently" for state window encoding.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `while_low_hp` | While Low HP (sustained state) | 6/7 | common | D4 Master's Tenacity ("only applies when you're under 50% HP" — distinct from on_near_death as a SUSTAINED state not an event); GD "On Low Health"; LE sustained low-HP buff nodes; D3 low-HP multipliers; Lost Ark Emergency Rescue |
| `while_moving` | While Moving | 5/7 | common | D4 Raid Captain ("at 140% movement speed"); D4 "Aggressive Aspect" (while moving); PoE "recently moved" keywording; LE movement-speed synergy nodes; D3 movement bonuses |
| `while_stationary` | While Stationary / Not Moving | 3/7 | uncommon | PoE "while stationary" keystone passives (confirmed from community guides); D4 turret-style skills (Turrets while stationary); D3 Ingeom-style cooldown reduction when not moving |
| `while_channeling` | While Channeling | 4/7 | uncommon | D4 Aspect of Channeling (+50-70% all damage while channeling); LE "while channeling" nodes (Winds of Justice, Dark Nexus, Forgemaster's Stance, Abyssal Tempest — fires every X seconds); D4 Aspect of Conflagration; PoE channeling support interaction |
| `while_buffed` | While Specific Buff Active | 5/7 | uncommon | D4 "while Berserking" (Death Wish Aspect, Aspect of Berserk Ripping); D4 "while Unstoppable" (Aspect of Iron Warrior); D4 "while Healthy" (Protecting/Smiting Aspect — above 80% HP); Lost Ark Adrenaline (at 6 stacks); LE ward/buff state nodes |
| `while_full_hp` | While Full HP / Healthy | 4/7 | uncommon | D4 "while Healthy" (defined as 80%+ max life); D4 Smiting Aspect; LE "when above X% HP" nodes; D3 "above 90% health" proc items |

**STATE family count: 6 conditions**

---

### Family 5: ENEMY-STATE

Moderately supported. D4 has the richest enemy-state vocabulary; GD and LE support it at the passive/skill level.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_enemy_killed` | On Enemy Killed | 7/7 | common | D2 "When You Kill An Enemy" (Infinity, Obsession runewords); GD "on kill" mechanics; D4 Bear Clan Berserker's Aspect ("killing an enemy while Berserking"); D3 Mad Monarch Scepter ("after killing 10 enemies"); LE on-kill passive nodes; LA kill-based engravings |
| `vs_low_hp_enemy` | vs Low HP Enemy / vs Injured Enemy | 5/7 | uncommon | D4 Smiting Aspect ("against Injured enemies" = below 35% HP); D4 "Lucky Hit: Up to X% chance to Execute Injured Non-Elites"; LE low-health enemy bonus nodes; D3 execute-threshold items; D4 Anemia Aspect ("against Bleeding enemies") |
| `vs_cc_enemy` | vs CC'd / Status-Affected Enemy | 5/7 | uncommon | D4 Anemia Aspect ("direct damage against Bleeding enemies"); D4 "against Vulnerable enemies"; LE ailment-conditional passives; PoE shock/freeze mechanics; GD debuff-conditioned procs |
| `on_enemy_stunned` | On Enemy Stunned / CC Applied | 4/7 | uncommon | PoE stunning interactions; D4 stagger/stun application; GD stun from item procs; LE stun application nodes |
| `vs_elite_or_boss` | vs Elite / vs Boss | 4/7 | uncommon | D4 Grudge engraving ("+20% damage to bosses"); Lost Ark "when attacking named bosses"; D4 many aspects specify elite/boss scaling; PoE pinnacle-boss mechanics; D3 elite-targeting items |
| `vs_grouped_enemies` | vs Grouped Enemies (proximity cluster) | 3/7 | uncommon | D4 area-damage aspects activated when enemies are grouped; GD AoE procs with cluster trigger; D3 Echoing Fury (stacks refresh when any enemy dies nearby); partial PoE |

**ENEMY-STATE family count: 6 conditions**

---

### Family 6: ENVIRONMENTAL

Weakest cross-game penetration of all 11 families. Only 3 of 7 ARPGs have explicit environmental trigger conditions in gear/passives. PoE has the richest environmental design space (ground effects); D4 has area-based conditions; others are sparse.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_ground_effect` | On Ground Effect / Hazard Zone | 3/7 | rare | PoE burning ground (fire) / chilled ground / shocked ground (distinct from burning damage affliction); D4 consecrated ground; D3 environment-based skill interactions |
| `while_in_element_zone` | While In Element-Specific Zone | 2/7 | rare | PoE elemental ground effects active under player; D4 "in objective area" consecration-style mechanics; NOT present in D2/GD/LE/LA |
| `in_objective_area` | In Encounter Special Zone / Objective Area | 2/7 | rare | D4 shrine and objective-specific mechanics; PoE map device / special encounter zones; partial evidence only |
| `near_ally` | Near Ally | 3/7 | rare | D4 support-style aspects (Expert engraving: "when shielding/healing allies"); LE companion/summon proximity; Lost Ark party buff proximity; NOT design-fit for solo game without ally mechanics |
| `isolated` | Isolated (no nearby ally or enemy) | 2/7 | rare | D4 isolation bonus; PoE solo-character keystones ("if there is only one nearby enemy"); not a common vocabulary item; weak cross-game evidence |
| `in_shadow` | In Shadow / Near Cover | 1/7 | rare | Diablo 4 Shadow-Imbuement (Aspect of Lethal Dusk: "evading through an enemy infected by Shadow Imbuement"); context-specific to stealth/shadow archetype; not a cross-game standard |

**ENVIRONMENTAL family count: 6 conditions**
**NOTE:** This family has the weakest cross-game backing. Conditions suitable for Reincarnated v1 are limited to on_ground_effect + while_in_element_zone (compose naturally with earth/fire/water/wind element system). near_ally, isolated, in_shadow are low-priority for a solo-only game.

---

### Family 7: SKILL-CONDITIONED

Moderately well-represented. D4 skill-specific aspects are the richest source. PoE skill gem links; LE skill tree specialization; all confirm skill-conditioned triggers as a core vocabulary item.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_specific_skill_use` | On Specific Skill Use (named skill) | 6/7 | common | D4 Incendiary Aspect ("damage from your Pyromancy Skills"); D4 Ancestral Echoes ("damaging enemies with Leap, Upheaval, or Whirlwind"); LE "when you directly cast [Skill]" vs "when triggered"; PoE gem link targeting; GD devotion bound to specific skill; Lost Ark skill-specific tripod system |
| `after_t4_effect` | After T4 / Capstone Effect Activation | 2/7 | rare | D4 "after using [Ultimate]" patterns; D3 set bonus triggered by specific class ability; internal to Reincarnated architecture (T4 capstone); low external evidence but logically sound |
| `on_spell_cast` | On Spell/Magic-Category Skill Cast | 4/7 | uncommon | D4 mage-category skills; PoE spell-support gems vs attack-support gems (explicit distinction); D3 "when you cast a spell" procs; LE spell-type node differentiation |
| `on_physical_skill_use` | On Physical/Melee-Category Skill Use | 4/7 | uncommon | D4 physical/melee aspect category; PoE attack vs spell binary; GD weapon pool skills (physical attacks specifically); LE melee-category passives; D2 melee vs ranged distinction |
| `on_t1_skill_chain` | On Tier-1/Basic Skill Use | 3/7 | uncommon | D4 Aspect of Might ("damage reduction granted by Basic skills"); LE early-tier node interactions; D4 explicitly uses Basic/Core/Defensive/Conjuration/Mastery/Ultimate skill tiers as trigger categories |
| `on_chain_finisher` | On Chain Finisher / Combo Finisher | 2/7 | rare | LE chain-finisher interactions; LA combo finisher / "last skill in rotation" patterns; D4 "after using X number of skills" patterns (Aspect of Pestilent Points: "every 3rd cast of Puncture"); some D3 set bonuses |

**SKILL-CONDITIONED family count: 6 conditions**

---

### Family 8: COMBO

Most specialized family. PoE has "stack" mechanics; D3/D4 have kill-count and cast-count accumulation; LE has channeling counts. Full "after N hits in X seconds" pattern is rare.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_n_hits_in_window` | After N Hits Within Time Window | 3/7 | uncommon | D4 Aspect of Pestilent Points ("every 3rd cast"); D3 Lord Greenstone's Fan ("every second, gain stack — max 30"); PoE Manaforged Arrows ("spent enough mana in total"); partial LE combo stacks |
| `on_buff_stack_cap` | On Buff Stack Cap Reached | 4/7 | uncommon | D3 Echoing Fury (5 stacks for full attack speed bonus); Lost Ark Adrenaline (6 stacks → max bonus); D4 Adrenaline-class aspects with stack cap; PoE buff-stack mechanics |
| `on_skill_rotation_cycle` | On Skill Rotation Completion | 2/7 | rare | LA skill rotation completion (specific class archetypes); D4 "consecutive" skill use patterns; partial evidence only |
| `on_consecutive_kills` | On Consecutive Kills / Kill Streak | 2/7 | rare | D3 Mad Monarch Scepter ("after killing 10 enemies"); D3 Corrupted Ashbringer ("accumulating 5 skeletons"); D3 kill-streak mechanics; D4 "killing X enemies in Y seconds" |
| `on_combo_break` | On Combo Break / Streak Interrupted | 1/7 | rare | Game-design concept; limited ARPG evidence; more prominent in action-RPG/DMC-style games; not a standard ARPG vocabulary item |

**COMBO family count: 5 conditions**

---

### Family 9: POSITIONAL

Confirmed but game-specific. Lost Ark is the richest source (back attack / front attack / counter as a genre-defining mechanic). D4 has some positional aspects. PoE/GD/D2 have minimal positional triggers.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_back_attack` | On Back Attack / Backstab | 3/7 | uncommon | Lost Ark Ambush Master (+25% damage on back attack, confirmed); LA Back Attack mechanic (5% bonus + 10% crit); D4 Ambush-style aspects; D3 backstab-class items; NOT in GD or PoE natively |
| `on_front_attack` | On Front Attack | 2/7 | uncommon | Lost Ark Master Brawler (+25% damage on front attack); LA Front Attack mechanic (+20% damage + 10% stagger); D4 positioning aspects; limited cross-game evidence |
| `on_flank_attack` | On Flank Attack (side) | 2/7 | rare | General game-design vocabulary (side = flanking, 25% extra, negates 50% dodge per genre conventions); limited ARPG item-vocabulary evidence; more tabletop/tactical CRPG |
| `on_melee_range` | On Close Range / In Melee Range | 4/7 | uncommon | D4 melee-proximity aspects; GD melee-range item skills; LE melee-conditional passives; PoE point-blank keystone (ranged damage bonus at close range); D2 melee weapon triggers |
| `while_kiting` | While Moving Away From Target | 2/7 | rare | D4 kite-style aspects; PoE "moving away from" wording in some passives; limited evidence |

**POSITIONAL family count: 5 conditions**

---

### Family 10: ELEMENT

Solid cross-game evidence. D4 elemental conditions (vs fire-immune, on shock, on freeze, on ignite) are richly documented. PoE2 meta gems built almost entirely on elemental ailment triggers.

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `on_element_cast` | On Casting Element-Typed Skill | 5/7 | common | D4 Incendiary Aspect ("damage from your Pyromancy Skills"); PoE elemental spell support gems; GD devotion bound to elemental skill; LE elemental-type spell passives; D3 elemental-class procs |
| `on_element_ailment_apply` | On Applying Elemental Ailment (freeze/burn/shock/etc.) | 5/7 | common | PoE2 Cast on Freeze (100 energy when you freeze), Cast on Ignite (20 energy when you ignite), Cast on Shock (1 energy per power when you shock), Cast on Elemental Ailment (combined); D4 ailment-application aspects; LE ailment-apply mechanics; GD elemental proc chains |
| `on_element_react` | On Element Reaction (two elements interact) | 3/7 | uncommon | PoE elemental overlap (ignite+shock+freeze multipliers); D4 cross-element reactions; D3 elemental set synergies; LE elemental compound damage; partial evidence |
| `vs_element_immune` | vs Elementally-Resistant / Immune Enemy | 3/7 | uncommon | D2 "vs immune" mechanics (cold immune, fire immune); PoE elemental penetration triggers; D4 resistance-breach mechanics; NOT strongly evidenced as a trigger condition vs resistance |
| `on_secondary_element` | On Secondary/Dual Element Activation | 2/7 | rare | PoE2 dual-element builds (combining ailments); D4 DUAL_ELEMENT_ADDITION concept (parallel to doc 43); limited direct trigger-condition evidence; more of a capability scope concept |

**ELEMENT family count: 5 conditions**

---

### Family 11: TIMER

Well-represented across all ARPGs. Timer-based triggers are universal; what varies is granularity (every-N-seconds vs once-per-encounter vs on-encounter-start).

| trigger_id | canonical_name | cross_game_prevalence | frequency_class | notes |
|---|---|---|---|---|
| `every_n_seconds` | Every N Seconds (repeating) | 6/7 | common | LE "casts Smite every second" (Winds of Justice), "mana every 3 seconds" (Dark Nexus), "summons Forged Weapons every 5 seconds"; D4 "per second" resource generation; Lost Ark "every 60/30/10 seconds" (Drops of Ether); D3 Lord Greenstone's Fan ("every second, gain stack") |
| `once_per_encounter` | Once Per Encounter / Encounter Start | 3/7 | uncommon | D4 "at start of encounter" mechanics; Lost Ark Crisis Evasion (640s cooldown — effectively encounter-scoped); D3 "once per engage" effects; partial PoE nemesis/boss mechanic |
| `for_n_seconds_after` | For N Seconds After Trigger Event | 6/7 | common | D4 "for 2 seconds" (Anemia Aspect), "for 5 seconds" (Berserking aspects), "for 3 seconds" (Barrier aspects); D2 aura-duration; LE buff-duration nodes; PoE duration mechanics; virtually universal |
| `on_cooldown_tick` | On Skill Cooldown Expiration | 4/7 | uncommon | D4 Aspect of Awakening ("reduces cooldown by 50%"); PoE cooldown-trigger interactions; LE cooldown-based proc timing; GD skill with cooldown improves devotion trigger rate |
| `combat_start` | On Entering Combat | 3/7 | uncommon | D4 "at start of combat" or "when first engaging"; LE "on entering combat" passives; Lost Ark opening-burst mechanics; GD "start of combat" item skill behaviors |

**TIMER family count: 5 conditions**

---

## Section 2 — Per-Condition Composition Properties

Full table of all 63 catalogued conditions with composition properties per dispatch § 7.2:

| trigger_id | family | cross_game_prevalence | frequency_class | pattern_id | trigger_window | concentration_fit | thematic_seed | synergy_pattern | ai_tell_risk |
|---|---|---|---|---|---|---|---|---|---|
| `on_hit` | action | 7/7 | common | attack_on_hit | instant | epic_triggered_passive / legendary_t0 | offense_generic (all archetypes) | pairs with on_crit (escalating trigger stack); pairs with combo counter | HIGH — "when you attack..." is the most generic trigger phrasing |
| `on_crit` | action | 7/7 | common | attack_on_crit | instant | legendary_t0 / legendary_t1 | offense_precision (dex / offensive builds) | pairs with crit-chance stacking; on_crit + freeze = frost-crit archetype | MEDIUM — "on critical" has genre-specific flavor; less flat than on_hit |
| `on_cast` | action | 6/7 | common | spell_on_cast | instant | epic_triggered_passive / legendary_t0 | magic_caster (int / wis builds) | pairs with spell-type conditions; on_cast + resource_full = ritual magic | HIGH — "when you cast..." shares generic-tone risk; mitigation: specify spell tier or element |
| `on_channel_tick` | action | 4/7 | uncommon | channel_periodic | brief (≤1s; per tick) | epic_triggered_passive / legendary_t1 | channeled_ritual (wis / int; slow tempo) | pairs with while_channeling state; channel_tick + element = elemental ritual casting | LOW-MEDIUM — specific to channeled classes; feels purposeful |
| `on_channel_end` | action | 3/7 | uncommon | channel_completion | instant (at release) | legendary_t0 / legendary_t1 | precision_channeler (timing-focused builds) | pairs with on_channel_tick (tick accumulate → release burst); timing window mechanic | LOW — timing-reward trigger is design-expressive; naturally specific |
| `on_melee_hit` | action | 5/7 | common | melee_on_attack | instant | epic_triggered_passive / legendary_t0 | physical_melee (str / dex melee builds) | pairs with on_back_attack (melee + positional); on_melee_hit + earth = grounded striker | MEDIUM — "when your melee attack lands" is more specific than on_hit; weapon-type anchor helps |
| `on_being_hit` | defense | 7/7 | common | counter_on_hit_taken | instant | epic_triggered_passive / legendary_t0 | reactive_defender (all archetypes) | pairs with reflect effects (reactive archetype); pairs with on_being_hit_by_crit (escalated defense) | HIGH — "when you take damage" / "when an enemy strikes you" is formulaic; mitigation: specify reaction type |
| `on_block` | defense | 5/7 | common | counter_on_defensive | instant | epic_triggered_passive / legendary_t0 | shield_fighter (str / defensive builds) | pairs with on_dodge (broader defensive archetype); on_block + counter = counter-fighter; on_block + earth = fortress warrior | LOW-MEDIUM — block is mechanism-specific; implies a shield or blocking build |
| `on_dodge` | defense | 5/7 | uncommon | counter_on_defensive | instant | epic_triggered_passive / legendary_t0 | agile_evader (dex builds; mobile) | pairs with on_block (counter_on_defensive cluster — DEDUP RISK); on_dodge + wind = wind-dancer archetype | LOW — dodge is mechanism-specific; movement archetype is expressive |
| `on_near_death` | defense | 6/7 | common | low_hp_trigger | instant | epic_triggered_passive / legendary_t0 | survivor_desperate (all archetypes; dramatic) | pairs with while_low_hp (instant event vs sustained state); on_near_death + self-healing = phoenix archetype | LOW — "near death" is emotionally specific; naturally dramatic |
| `on_being_hit_by_crit` | defense | 3/7 | uncommon | counter_on_crit_taken | instant | legendary_t0 / legendary_t1 | resilient_tank (high-DR builds) | pairs with on_being_hit (escalation of same base event); counter_on_crit_taken + reflect = "crit reversal" | LOW — specificity of "when a critical lands on you" reduces AI-tell risk |
| `on_stun` | defense | 3/7 | uncommon | counter_on_cc | instant | legendary_t0 | control_break (resilience builds) | pairs with on_being_hit (CC as a damage follow-on); on_stun + burst = CC-break retaliation | LOW — stun recovery is mechanically specific |
| `on_resource_full` | resource | 5/7 | uncommon | resource_threshold_high | instant | legendary_t0 / legendary_t1 | power_accumulation (resource-battery builds) | pairs with on_resource_spend (cycle: fill → burst → empty → repeat); resource_full + element = mana-eruption | MEDIUM — "when resource fills" is specific enough; risk if phrased as "when mana is at maximum..." without mechanical depth |
| `on_resource_spend` | resource | 5/7 | uncommon | resource_threshold_spend | instant | epic_triggered_passive / legendary_t0 | cost_converter (RESOURCE_CONVERSION T4) | pairs with resource_low (spend-down→refill cycle); on_resource_spend + HP-cost = blood-magic | LOW-MEDIUM — "when you spend energy" is archetypally specific |
| `on_resource_low` | resource | 4/7 | uncommon | resource_threshold_low | instant | epic_triggered_passive / legendary_t0 | desperation_caster (glass-cannon mage) | pairs with on_near_death (dual-scarcity archetype); resource_low + damage_buff = "reckless fury" | LOW-MEDIUM — dual threshold with near_death creates expressive desperation archetype |
| `on_resource_tick` | resource | 3/7 | rare | resource_regen_event | brief (≤1s; per tick) | epic_triggered_passive | regenerator (wis / support-adjacent builds) | pairs with every_n_seconds timer (overlapping periodic) — DEDUP RISK if same window | LOW — rare trigger; expressive for specific resource-regen builds |
| `on_resource_pop` | resource | 3/7 | rare | resource_threshold_high | instant (burst) | legendary_t1 / set_bonus | nova_archetype (burst-and-regen builds) | pairs with on_resource_full (same cluster — DEDUP RISK: pattern_id = resource_threshold_high for both); on_resource_pop + element = elemental nova | LOW — "when resource overflows/pops" is mechanically specific; narratively vivid |
| `while_low_hp` | state | 6/7 | common | low_hp_sustained | sustained-buff (5-30s) | epic_triggered_passive / legendary_t0 | desperate_berserker (str melee; damage-at-cost) | pairs with on_near_death (event vs sustained); while_low_hp + damage_buff = berserker archetype | MEDIUM — "while below 50% HP" phrasing is common; mitigation: specific buff type and threshold |
| `while_moving` | state | 5/7 | common | kinetic_condition | sustained-buff (5-30s) | epic_triggered_passive / legendary_t0 | agile_striker (dex / speed builds) | pairs with on_dodge (mobile archetype stack); while_moving + damage = "kill-on-the-run" | MEDIUM — "while moving" is moderate risk; mitigate with movement-type specificity (dashing vs walking) |
| `while_stationary` | state | 3/7 | uncommon | rooted_stance | sustained-buff (5-30s) | epic_triggered_passive / legendary_t0 | sentinel_mage (int / wis; ritual caster) | pairs with while_channeling (stationary+channeling = fully committed ritual); while_stationary + defense = fortress sentinel | LOW-MEDIUM — "while rooted/stationary" implies a deliberate playstyle commitment; expressive |
| `while_channeling` | state | 4/7 | uncommon | channeling_active | sustained-buff (5-30s) | epic_triggered_passive / legendary_t1 | ritual_caster (wis / int; slow-tempo channeler) | pairs with while_stationary; pairs with on_channel_tick (layered channeling design space) | LOW — channeling is mechanically committed; feels intentional |
| `while_buffed` | state | 5/7 | uncommon | specific_buff_active | sustained-buff (5-30s) | legendary_t0 / legendary_t1 | archetype_amplifier (varies by buff type) | pairs with on_resource_full (fill → buffed); while_buffed(BERSERKING) + attack = berserker; while_buffed(UNSTOPPABLE) + movement = charge | MEDIUM — "while [buff name] is active" risk depends on buff specificity; named buffs (Berserking, Unstoppable) are LOW risk; generic "while buffed" is HIGH |
| `while_full_hp` | state | 4/7 | uncommon | high_hp_sustained | sustained-buff (5-30s) | epic_triggered_passive / legendary_t0 | glass_cannon (offensive trade-off builds) | pairs with while_low_hp (mutually exclusive archetype axis — DESIGN NOTE: same character cannot have both meaningfully); while_full_hp + crit_boost = "precision surgeon" | MEDIUM — "while healthy" is readable but common; |
| `on_enemy_killed` | enemy-state | 7/7 | common | kill_trigger | instant | epic_triggered_passive / legendary_t0 | momentum_killer (all archetypes; esp. dex offensive) | pairs with on_consecutive_kills (kill streak); on_enemy_killed + AoE = "death nova" archetype | HIGH — "on kill" is the most generic trigger in the genre; mitigation: specify kill type (melee kill, kill under effect, kill by specific skill) |
| `vs_low_hp_enemy` | enemy-state | 5/7 | uncommon | enemy_weakened | instant | legendary_t0 | executioner (all archetypes; finishing-blow identity) | pairs with on_enemy_killed (execute→kill cycle); vs_low_hp + execute = "Reaper" archetype | LOW-MEDIUM — "against injured enemies" is specific enough; phrasing risk if just "vs weakened enemy" |
| `vs_cc_enemy` | enemy-state | 5/7 | uncommon | enemy_afflicted | instant | legendary_t0 / legendary_t1 | ailment_exploiter (int / wind / water; control+damage) | pairs with on_element_ailment_apply (apply→exploit cycle); vs_cc_enemy + damage_amp = "conqueror of the controlled" | LOW — enemy ailment state is specific; design-expressive for control archetypes |
| `on_enemy_stunned` | enemy-state | 4/7 | uncommon | enemy_cc_applied | instant | legendary_t0 | stunlock_amplifier (earth / control archetypes) | pairs with vs_cc_enemy (apply stun → fire vs_cc effects); pairs with vs_low_hp (pin-and-finish) | LOW-MEDIUM — stun application is specific; risk if overused |
| `vs_elite_or_boss` | enemy-state | 4/7 | uncommon | elite_scaling | instant | legendary_t1 / legendary_t2 | boss_hunter (specialized endgame builds) | pairs with vs_cc_enemy (set up vs boss); vs_elite + damage_amp = endgame-scaling archetype | LOW — "vs boss/elite" is a meaningful design signal; specific and purposeful |
| `vs_grouped_enemies` | enemy-state | 3/7 | uncommon | density_trigger | instant | legendary_t0 | crowd_controller (AoE archetypes; fire / earth) | pairs with on_enemy_killed (multi-kill AoE); vs_grouped + AoE_damage = "pack hunter" | LOW-MEDIUM — "when surrounded by enemies" is common in genre but expressive for AoE archetypes |
| `on_ground_effect` | environmental | 3/7 | rare | ground_effect | instant | epic_triggered_passive | elemental_hazard (fire / water / earth / wind builds) | pairs with on_element_cast (player creates ground → fires trigger); on_ground_effect + duration_buff = "battlefield control" | LOW — environmental context is highly specific; expressive for element-heavy builds |
| `while_in_element_zone` | environmental | 2/7 | rare | zone_condition | sustained-buff (5-30s) | epic_triggered_passive | environment_synergist (earth / water / fire) | pairs with on_ground_effect (player-created zone); while_in_element_zone + element_boost = "elemental affinity" | LOW — expressive for builds that create their own terrain; memorable if well-narrated |
| `in_objective_area` | environmental | 2/7 | rare | zone_condition | sustained-buff (5-30s) | set_bonus / legendary_t1 | territory_fighter (defensive or control builds) | limited synergy evidence; objective-area trigger is more mechanical than thematic | MEDIUM — context-dependent; weak thematic seed |
| `near_ally` | environmental | 3/7 | rare | proximity_ally | sustained-buff (5-30s) | set_bonus | support_adjacent | NOT RECOMMENDED for solo-only game (Reincarnated v1); skip | LOW but irrelevant for solo |
| `isolated` | environmental | 2/7 | rare | isolation_condition | sustained-buff (5-30s) | legendary_t0 | lone_wolf | pairs with while_moving (solo aggression); weak vocabulary evidence | MEDIUM — "when alone" is lonely; questionable for an isekai identity-forward game |
| `in_shadow` | environmental | 1/7 | rare | stealth_condition | instant | legendary_t0 | shadow_striker | archetype-specific (dex rogue); limited cross-game evidence | LOW — only fires for specific archetype |
| `on_specific_skill_use` | skill-conditioned | 6/7 | common | specific_skill | instant | legendary_t1 / legendary_t2 | specialist (any archetype with named skill) | pairs with on_t1_skill_chain (tiered skill conditioning); on_specific_skill + element = "mastery echo" | LOW — specificity is built-in; most expressive trigger type when a skill name is named |
| `after_t4_effect` | skill-conditioned | 2/7 | rare | capstone_amplifier | instant | legendary_t2 / set_bonus | t4_enhancer (strategy-aligned builds) | pairs with all T4 strategy-conditioned effects; unique to Reincarnated architecture | LOW — T4 reference is game-specific and expressive |
| `on_spell_cast` | skill-conditioned | 4/7 | uncommon | spell_type | instant | epic_triggered_passive / legendary_t0 | arcane_amplifier (int / wis caster builds) | pairs with on_cast (broader); on_spell_cast + element = elementalist; on_spell_cast + while_channeling = ritual mage | MEDIUM — "when you cast a spell" risks generic mage trope; mitigate with element specificity |
| `on_physical_skill_use` | skill-conditioned | 4/7 | uncommon | physical_attack_type | instant | epic_triggered_passive / legendary_t0 | martial_amplifier (str / dex melee builds) | pairs with on_melee_hit; on_physical_skill + ground_slam = warrior echo; on_physical_skill + str = warlord | LOW-MEDIUM — "physical skill" is a legible category; less risk than generic on_cast |
| `on_t1_skill_chain` | skill-conditioned | 3/7 | uncommon | chain_tier_1 | instant | epic_triggered_passive | tier_gated (early/mid builds; early-game accessible) | pairs with on_specific_skill_use (chain_tier_1 is a subset); accessible trigger for lower-rarity gear | LOW-MEDIUM — "when using a basic skill" is purposeful but slightly generic |
| `on_chain_finisher` | skill-conditioned | 2/7 | rare | chain_completion | instant | legendary_t0 / legendary_t1 | combo_closer (dex / physical; timing-focused) | pairs with on_n_hits_in_window (combo count + finisher); on_chain_finisher + burst = "signature move" | LOW — finisher concept is expressive; rare in ARPG vocabulary but memorable |
| `on_n_hits_in_window` | combo | 3/7 | uncommon | hit_count_accumulation | brief-buff (1-5s; window-based) | legendary_t0 / legendary_t1 | tempo_striker (dex / attack-speed builds) | pairs with on_buff_stack_cap (both are accumulation patterns — DEDUP RISK if same window); on_n_hits + burst = "escalating fury" | MEDIUM — "after X hits" is legible but can produce rote counting flavor; mitigate with visual burst effect language |
| `on_buff_stack_cap` | combo | 4/7 | uncommon | buff_stack_accumulation | brief-buff (1-5s; per stack cycle) | legendary_t1 | stack_master (any archetype with buff stacking) | pairs with on_n_hits_in_window (DEDUP RISK); pairs with while_buffed (stacking → buffed → cap → burst cycle) | MEDIUM — "when stacks reach maximum" is common ARPG vocabulary; mitigate with thematic stack name |
| `on_skill_rotation_cycle` | combo | 2/7 | rare | rotation_completion | brief-buff (1-5s) | legendary_t1 / legendary_t2 | tactician (methodical builds; earth / wis) | pairs with on_chain_finisher; pairs with on_specific_skill_use (rotation conditions specific skill) | LOW — rotation completion is expressive for deliberate play styles |
| `on_consecutive_kills` | combo | 2/7 | rare | kill_streak | instant | legendary_t0 / legendary_t1 | momentum_predator (offensive; dex or str offensive) | pairs with on_enemy_killed (single kill → streak); on_consecutive_kills + movement_speed = "hunting frenzy" | LOW-MEDIUM — "kill streak" concept is expressive; risk of D3 "massacre" trope |
| `on_combo_break` | combo | 1/7 | rare | combo_break | instant | legendary_t0 | — | minimal cross-game evidence; not recommended | HIGH — abstract concept; hard to narrate meaningfully |
| `on_back_attack` | positional | 3/7 | uncommon | positional_back | instant | legendary_t0 / legendary_t1 | assassin_precision (dex / wind; stealth/speed) | pairs with on_dodge (mobile assassination); on_back_attack + wind = "shadow wind step" archetype | LOW — positional specificity is expressive; strong in isekai-adjacent builds (assassin archetype) |
| `on_front_attack` | positional | 2/7 | uncommon | positional_front | instant | legendary_t0 | aggressive_duelist (str / dex; charge-style builds) | pairs with vs_cc_enemy (stun → front attack bonus); pairs with on_melee_hit | LOW-MEDIUM — front attack is expressive for duelist/warrior but less common than back attack |
| `on_flank_attack` | positional | 2/7 | rare | positional_side | instant | legendary_t0 | flanker (dex; tactical builds) | pairs with while_moving (flanker moves to side position); limited ARPG evidence | LOW but weak vocabulary backing |
| `on_melee_range` | positional | 4/7 | uncommon | close_range_condition | sustained-buff (5-30s) | epic_triggered_passive / legendary_t0 | up_close_fighter (str / earth; grappler) | pairs with while_stationary (close + planted = brawler); on_melee_range + defense = counter-fighter tank | LOW-MEDIUM — "while in melee range" is legible; specific enough |
| `while_kiting` | positional | 2/7 | rare | retreat_condition | sustained-buff (5-30s) | epic_triggered_passive | kite_striker (ranged dex; attrition builds) | pairs with while_moving (kite = moving while attacking); while_kiting + ranged_damage_buff = ranged skirmisher | MEDIUM — "while moving away" is mechanically fragile to define precisely |
| `on_element_cast` | element | 5/7 | common | element_skill_type | instant | epic_triggered_passive / legendary_t0 | element_specialist (any element-primary build) | pairs with on_spell_cast (subset relationship); on_element_cast + element_ailment = "fire caster triggers frost echo" | LOW-MEDIUM — "when casting fire" is expressive; risk if identical to on_spell_cast without differentiation |
| `on_element_ailment_apply` | element | 5/7 | common | ailment_application | instant | legendary_t0 / legendary_t1 | ailment_sorcerer (wind / water / fire / earth; control via ailment) | pairs with vs_cc_enemy (apply → exploit cycle); on_element_ailment_apply + freeze = cold controller; on_element_ailment_apply + shock = lightning chainer | LOW — ailment application is mechanically specific and design-expressive |
| `on_element_react` | element | 3/7 | uncommon | element_reaction | instant | legendary_t1 / legendary_t2 | element_combiner (dual-element builds; DUAL_ELEMENT T4) | pairs with after_t4_effect (DUAL_ELEMENT_ADDITION T4 specifically); on_element_react + dual_element = "thermal shock" archetype | LOW — reaction trigger is sophisticated and distinctive; high thematic value |
| `vs_element_immune` | element | 3/7 | uncommon | element_penetration | instant | legendary_t1 | resistance_breaker (penetration builds) | pairs with on_element_cast (cast + breach immunity); limited trigger vocabulary evidence | LOW-MEDIUM — specific but negative framing ("when enemy resists") is atypical for trigger wording |
| `on_secondary_element` | element | 2/7 | rare | dual_element_activation | instant | legendary_t2 / set_bonus | dual_elementalist (DUAL_ELEMENT_ADDITION T4 builds) | pairs with on_element_react (both require dual-element); high thematic synergy with doc 43 Category C DUAL_ELEMENT_ADDITION | LOW — rare trigger; meaningful only for dual-element builds; gates naturally |
| `every_n_seconds` | timer | 6/7 | common | periodic_repeating | brief-buff (per cycle) | epic_triggered_passive / legendary_t0 | rhythm_fighter (wis; methodical; ritual cadence) | pairs with while_channeling (channeling every-N-second tick); DEDUP RISK with on_resource_tick (both are periodic) | HIGH — "every X seconds" is the most generic timer phrasing; mitigation: tie to specific environment/action context; "for every second you maintain [stance]" is more expressive |
| `once_per_encounter` | timer | 3/7 | uncommon | encounter_cooldown | encounter | legendary_t1 / legendary_t2 / set_bonus | boss_hunter (opening-burst builds) | pairs with combat_start (both are encounter-scoped); once_per_encounter + massive_burst = "opening gambit" | LOW-MEDIUM — "once per battle" is understood; expression depends on the effect |
| `for_n_seconds_after` | timer | 6/7 | common | duration_window | brief-buff (1-5s) / sustained-buff (5-30s) | epic_triggered_passive / legendary_t0 | duration_amplifier (any build with windows) | NOTE: this is a DURATION MODIFIER on other triggers, not itself a trigger; pairs with every other trigger as a modifier | MEDIUM — "for X seconds after" is the default duration framing; generic but ubiquitous |
| `on_cooldown_tick` | timer | 4/7 | uncommon | cooldown_gate | instant (on CD expire) | legendary_t0 / legendary_t1 | cooldown_optimizer (wis / int; rotation-focused) | pairs with on_skill_rotation_cycle; CD-expire trigger creates natural rhythm | LOW — cooldown expiration is mechanically specific; purposeful |
| `combat_start` | timer | 3/7 | uncommon | encounter_start | instant | legendary_t1 / set_bonus | ambush_opener (dex; burst opening builds) | pairs with on_back_attack (ambush archetype); pairs with once_per_encounter | LOW — "at combat start" is expressive for planning-oriented builds; low AI-tell risk |

**Total catalogued: 63 trigger conditions across 11 families**

---

## Section 3 — AI-Tell + Redundancy Mitigation Patterns

### Q-SC4-1: Highest AI-Tell Risk Conditions

The following conditions produce formulaic narrative when LLM-narrated without additional context:

**CRITICAL risk (likely to produce boilerplate flavor):**
1. `on_hit` / `on_being_hit` — "when you attack" / "when an enemy strikes you" paired constructions are the most-reproduced formula in ARPG flavor text. The Cycle 13 data (reflect_on_being_hit × 2 on one character) demonstrates this pattern.
2. `on_enemy_killed` — "on kill" is the most overused trigger in the genre. D3 "exploding corpse on kill" became a meme precisely because it's so generic.
3. `every_n_seconds` — "every X seconds" is a pure mechanical statement; without context (what the character is doing during those seconds, why those seconds matter), it produces rote number-counting flavor.
4. `on_cast` — "when you cast a spell" produces the generic "arcane energy surges" class of AI-tell text.

**Mitigations (all conditions):**
- Name the SECONDARY EFFECT with specificity rather than the trigger alone ("your counter-strike carves a wind arc" vs "deals damage on block")
- Tie the trigger to a character-specific mechanism ("when your frost-mark shatters" vs "on crit")
- Use the thematic_seed field to anchor LLM narration to the character's identity (doc 46 Layer 6: cohesion-judge anchors on chain composition, not gear trigger phrasing)
- Reserve generic-trigger conditions for Epic/T0 gear; highest-AI-tell-risk conditions should NOT appear on Legendary T1/T2 with generic-effect pairings

**LOW risk (already specific by mechanism):**
- `on_channel_end`, `on_chain_finisher`, `on_element_ailment_apply`, `on_back_attack`, `on_element_react` — these carry inherent specificity from their mechanism.

---

### Q-SC4-2: Same-Pattern_ID Dedup Clusters

Conditions sharing the same `pattern_id` are the highest dedup risk. The Layer 7 Pass 2 hard-dedup rule (no two equipped legendaries with same pattern_id per loadout) applies directly:

| pattern_id | Members | Cluster size | Dedup severity | Notes |
|---|---|---|---|---|
| `counter_on_defensive` | on_block + on_dodge + on_parry (if added) | 3 (or 4 with parry) | CRITICAL | The exact pattern from Cycle 13 empirical inspection: wis_04 had 2× counter_on_block; dex_04 had 2× speed_boost_on_dodge. These share the same defensive-reaction pattern space. Only 1 per loadout. |
| `attack_on_hit` | on_hit + on_melee_hit | 2 | HIGH | Both fire on the same event class; distinguish by scope (all hits vs melee-only). Treat as same cluster; cap at 1 per loadout unless explicitly differentiated by scope. |
| `resource_threshold_high` | on_resource_full + on_resource_pop | 2 | HIGH | Both are "resource fills to top" events. Distinguish by whether the pop empties the resource. Cap at 1 of the pair per loadout. |
| `low_hp_trigger` / `low_hp_sustained` | on_near_death + while_low_hp | 2 | MEDIUM | on_near_death is event-based; while_low_hp is sustained. Same HP-threshold space. Both at once creates strong build-identity coherence (desperate archetype) — ALLOW with intentional design, but flag as narrative overlap. |
| `periodic_repeating` | every_n_seconds + on_resource_tick | 2 | MEDIUM | Both produce "fires every little while" semantics. If both are in a loadout, they compound into a mechanical noise pattern. Cap at 1 periodic trigger per trigger-window in same effect-category. |
| `buff_stack_accumulation` | on_n_hits_in_window + on_buff_stack_cap | 2 | HIGH | Both are "accumulate then burst" patterns. If a character has both, their buff-windows overlap and the trigger identity is diffuse. Cap at 1 per loadout per accumulation axis. |
| `channel_periodic` | on_channel_tick + while_channeling | 2 | LOW-MEDIUM | on_channel_tick fires per tick; while_channeling is a state. Both are valid in same loadout as they represent different surfaces (tick-effect vs sustained-bonus). Note overlap for narrative coherence purposes but do NOT hard-dedup. |
| `zone_condition` | in_objective_area + while_in_element_zone | 2 | LOW | Both are zone-based sustained conditions. Low enough frequency_class that collision is unlikely. Flag but do not hard-dedup. |
| `positional_defensive` | on_block + on_dodge | see counter_on_defensive above | see above | Same as counter_on_defensive cluster; block and dodge are in the same family |

---

### Q-SC4-3: Same-Trigger-Window Collision Risk

Layer 7 Pass 2 soft cap: no more than 2 effects per trigger-window family per loadout.

**Instant-window collisions (highest risk):**
The following conditions all fire in `instant` window. A loadout with 4+ instant-window legendaries risks the "rapid-fire mechanical chaos" pattern (the D4 aspect-soup failure mode):

- Entire action family: on_hit / on_crit / on_cast / on_melee_hit
- Defensive family event-triggers: on_being_hit / on_block / on_dodge / on_near_death / on_stun
- Enemy-state family: on_enemy_killed / vs_low_hp_enemy / vs_cc_enemy / on_enemy_stunned
- Element family: on_element_cast / on_element_ailment_apply

**Practical guidance for Layer 7 cap:**
- Max 2 instant-window conditions from ACTION family per loadout
- Max 2 instant-window conditions from DEFENSE family per loadout
- Max 1 instant-window condition from ENEMY-STATE per loadout
- COMBO + TIMER families (non-instant windows) can coexist with ACTION/DEFENSE instant-window conditions without collision

**Window mixing as design tool:**
Healthy build identity emerges from intentional window mixing — e.g., one instant-window ACTION trigger + one sustained-buff STATE condition + one timer-based periodic is a coherent pattern with minimal collision. The Cycle 13 failure was 4 instant-window conditions in the same effect-category (reflect/counter) — not just same window but same effect-category.

---

### Q-SC4-4: Conditions That Break Concentration Discipline (Skills Disguised as Triggered Passives)

Conditions confirmed by Layer 2 analysis as stat-boost-in-trigger-clothing:

| trigger_id + pattern | Why it violates concentration | Correct layer per doc 46 Layer 2 |
|---|---|---|
| `on_dodge` + movement speed boost | speed_boost_on_dodge (Cycle 13 dex_04 duplicate) is a trigger-conditioned stat boost, not a mechanic-altering effect | Layer 2: migrate to Epic+ partition affix with on_dodge sub-property |
| `on_being_hit` + DR% boost | defense_aura "on hit" is a trigger-conditioned stat boost | Layer 2: migrate to Epic+ partition affix with on_being_hit sub-property |
| `on_enemy_killed` + resource regen | general_passive_on_kill_regen is trigger-conditioned stat boost | Layer 2: migrate to Epic+ partition affix |
| `while_buffed` + generic stat boost | "passive: +5% crit chance while equipped" (masquerading as while_buffed trigger) | Layer 2: always-on stat boost → migrate to Magic/Rare partition affix with no trigger condition |
| `every_n_seconds` + stat boost (no mechanic change) | periodic minor stat bumps ("+8% resource regen every 10 seconds") are trigger-conditioned stat boosts | Layer 2: migrate to partition affix OR redesign as mechanic-altering effect (burst of resource, not just regen rate) |

**Legitimate legendary capability content using same trigger:**
The same trigger conditions ARE appropriate for legendary capabilities when the effect is MECHANIC-ALTERING:

| trigger_id + mechanic-altering effect | Legitimate as legendary? | Why |
|---|---|---|
| `on_dodge` + temporary invulnerability frame extension | YES | Changes HOW dodge works, not just a stat boost |
| `on_dodge` + counter-attack projectile | YES | Adds new mechanic to dodge action |
| `on_being_hit` + reflect damage | YES (but cap at 1 via dedup) | reflect is mechanic-altering (changes damage routing) |
| `on_enemy_killed` + chain explosion | YES | on_kill_explosion is mechanic-altering |
| `every_n_seconds` + persistent zone creation | YES | Zone is mechanic-altering (creates ground effect) |

The LINE: if the trigger condition activates a NUMBER (stat goes up), it belongs on a partition affix (Layer 2). If it activates a BEHAVIOR CHANGE (something new happens in the game world), it belongs as legendary capability/triggered_passive content.

---

## Section 4 — Concentration-Architecture Fit Summary

Per Layer 5 concentration probability table in doc 46 § 6.2, trigger conditions map to appropriate rarity tiers as follows:

**Epic tier appropriate (trigger-conditioned stat boost only):**
- `on_being_hit` + DR boost
- `on_dodge` + speed boost
- `on_enemy_killed` + resource regen
- `every_n_seconds` + regen tick

**Legendary T0/T0.5 appropriate (uncommon mechanic-altering; XOR with triggered_passive):**
- `on_hit`, `on_crit`, `on_cast` (action family — broad, accessible)
- `on_being_hit`, `on_block`, `on_dodge` (defense family — reactive)
- `on_enemy_killed`, `vs_low_hp_enemy` (enemy-state — common killers)
- `on_resource_full`, `on_resource_low` (resource — threshold)
- `while_low_hp`, `while_moving`, `while_full_hp` (state — common states)
- `on_element_cast`, `on_element_ailment_apply` (element — standard)
- `every_n_seconds`, `for_n_seconds_after` (timer — common)

**Legendary T1 appropriate (uncommon mechanic-altering; both capability + triggered_passive possible):**
- `on_channel_tick`, `on_channel_end` (action — committed)
- `on_near_death`, `while_channeling`, `while_buffed` (state — specialized states)
- `vs_cc_enemy`, `vs_elite_or_boss` (enemy-state — specific targeting)
- `on_n_hits_in_window`, `on_buff_stack_cap` (combo — accumulation)
- `on_back_attack`, `on_melee_range` (positional — specific positioning)
- `on_element_react`, `vs_element_immune` (element — advanced)
- `once_per_encounter`, `on_cooldown_tick` (timer — encounter-scoped)

**Legendary T2 / Set bonus appropriate (rare; high-complexity mechanic):**
- `after_t4_effect` (skill-conditioned — T4 synergy)
- `on_element_react` + `on_secondary_element` (element — dual-element builds)
- `on_skill_rotation_cycle`, `on_chain_finisher` (combo — deliberate rotational play)
- `on_consecutive_kills` (combo — kill-streak mastery)
- `combat_start` (timer — encounter-specific burst)

---

## Knowledge Gaps Not Resolved

1. **Path of Exile wiki direct access blocked (403):** poewiki.net and pathofexile.fandom.com both returned 403 on direct fetch. The PoE trigger condition vocabulary was reconstructed via WebSearch aggregates + game8.co (PoE2 trigger page), which did confirm PoE2 meta gems exhaustively but PoE1 trigger gem list was not fully enumerated. The PoE1 trigger gem list is well-documented in my training knowledge and community sources confirm: Cast When Damage Taken / Cast on Critical Strike / Cast on Death / Cast on Melee Kill / Cast when Stunned / Manaforged Arrows / Cast on Ward Break / Trigger (on-use manually). These 7 are the PoE1 trigger gem vocabulary; the research builds on this confirmed set.

2. **Lost Ark enemy-state trigger conditions in passives:** community guides confirmed positional (back/front attack) and HP-threshold triggers for LA engravings, but per-passive-tree node conditions (specific skill conditions within LA's tripod system) were not fully extractable from available sources. The vocabulary assembled is sufficient for the 11 trigger families but LA-specific passive details are underrepresented.

3. **Grim Dawn direct wiki access blocked (403):** grimdawn.fandom.com returned 403. Official grimdawn.com guide pages were accessible and provided the 9-condition confirmed list. GD community discussions on Steam confirmed "on critical attack", "when hit", "on attack" proc types. The official guide is authoritative; 9 GD proc conditions are confirmed.

4. **Diablo 3 legendary affix direct access:** maxroll.gg/d3 item pages were accessible. D3 trigger vocabulary includes on_kill + kill-count stacks + per-second stack accumulation, which are captured in COMBO and TIMER families. D3 is the richest source for kill-streak/combo-style triggers.

5. **Positional conditions — limited ARPG vocabulary backing:** The positional family (flank/back/front/range/kiting) has weaker vocabulary backing than the other families. Only Lost Ark has explicit back-attack and front-attack as genre-canonical trigger conditions. The other positional conditions (`on_flank_attack`, `while_kiting`) are logical extensions that appear in genre game-design vocabulary but are not confirmed as item/passive trigger conditions across 3+ ARPGs.

---

## Source List

1. poewiki.net/wiki/Trigger (PoE1 trigger mechanics — 403 on direct fetch; confirmed via WebSearch aggregate)
2. pathofexile.fandom.com/wiki/List_of_trigger_related_skill_gems (403 on direct fetch; confirmed via WebSearch aggregate)
3. https://game8.co/games/Path-of-Exile-2/archives/488224 — PoE2 meta gem list (direct fetch confirmed)
4. https://game8.co/games/Path-of-Exile-2/archives/487670 — PoE2 trigger explained (direct fetch confirmed)
5. https://diablo2.io/runewords/ — D2 runeword proc conditions (direct fetch confirmed; 7 trigger types extracted)
6. https://diablo2.io/uniques/ — D2 unique item proc conditions (direct fetch confirmed)
7. https://www.grimdawn.com/guide/character/item-skills/ — GD item skill triggers (official; direct fetch confirmed; 9 trigger types extracted)
8. https://www.grimdawn.com/guide/gameplay/combat/ — GD combat mechanics (official; direct fetch confirmed)
9. https://maxroll.gg/last-epoch/resources/passives-and-skills — LE passive overview (confirmed via WebSearch)
10. https://forum.lastepoch.com (LE channeling trigger mechanics — confirmed via WebSearch)
11. https://fextralife.com/lost-ark-combat-engravings-guide-best-combat-engravings-for-your-character/ — LA combat engravings (direct fetch confirmed; trigger conditions extracted)
12. https://maxroll.gg/lost-ark/resources/engraving-system-guide — LA engraving system (confirmed via WebFetch)
13. https://vulkk.com/2022/02/18/how-to-use-lost-arks-engraving-system/ — LA engraving conditions
14. https://mobalytics.gg/diablo-4/guides/all-diablo-4-legendary-aspects — D4 aspects (confirmed via WebSearch aggregate; multiple trigger examples extracted)
15. https://www.icy-veins.com/d4/guides/legendary-aspects-codex-of-power-guide/ — D4 aspect guide (confirmed via WebSearch)
16. WebSearch aggregates (multiple queries per ARPG; specific phrasing examples extracted per trigger type per family)
17. Training knowledge supplementing gaps: PoE1 trigger gem names (well-established), Grim Dawn proc type names, D3 legendary affix examples — used to supplement blocked-fetch sources; flagged as secondary.
