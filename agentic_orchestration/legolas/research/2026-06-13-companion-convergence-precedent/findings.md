# Research — Companion Convergence: Genre Precedent for Q8 — 2026-06-13

**Mode:** A (analytical)
**Commissioner:** gandalf
**Provenance note:** Authored by Legolas (Mode A pull, agent `a0d94702be0cf755d`); captured to disk by gandalf because the sub-agent environment blocked the direct Write (findings would otherwise have been lost, as the 2026-06-12 proxy-summoner pull was). Content reproduced faithfully from Legolas's return.
**Sources:** Maxroll.gg D2 + D4, Icy Veins D3, Inven Global D3, TheGamer D4 VoH, PureDiablo D4, Last Epoch forums, PoE Wiki, PoE Vault, Enter the Gungeon Wiki, TV Tropes, GameRant, CBR, DiabloBytes, Steam Community Grim Dawn threads, Torchlight Wiki, D2R Blizzard forums.

---

## Synthesis: 9 Load-Bearing Takeaways

**1. The gap-fill principle is the genre's universal answer.**
Across D2 mercs, D3 followers, D4 VoH mercs, Last Epoch Beastmaster, and Grim Dawn Briarthorn, every companion system that *feels good* gives the player something they structurally cannot have in their own kit. The companion does not add more of what the player already does — it adds what the player sacrificed to become what they are.

**2. The most durable pairings are asymmetric by primary dimension.**
The genre's canonically great combos (glass-cannon player + Holy Freeze merc, DoT player + burst finisher, pure-damage player + CC controller) share one structural property: player and companion are not competing for the same kill. The companion either enables the kill (setup), extends the window (CC), or recovers from the player's failure mode (survival/sustain). Pairings where both player and companion are in the damage dimension are the canonical failure state — named identically in D2, D3, and D4.

**3. The bond item must carry a "third thing."**
D3's Emanate mechanic (patch 2.7) is the clearest genre proof: Nemesis Bracers + Flavor of Time + Oculus Ring on the follower create a compound effect neither player nor follower produces alone. Oculus Ring specifically creates a positional damage area that *requires the companion to exist* but *plays through the player's movement.* This is the convergence item design target: a mechanic only present when both kits are bound together.

**4. Act 2 Holy Freeze is the single most validated ARPG companion pairing.**
D2 codified this so thoroughly it became genre law: a caster who cannot survive being surrounded chooses Holy Freeze not for damage but for a permanent slow aura that creates a safe-fire zone. The merc deals zero meaningful damage; it does all the survival that matters. This glass-cannon + CC-bodyguard pairing has been validated by community analysis for 23 years and is still the dominant choice in D2 Resurrected.

**5. The mandatory-tax anti-pattern has a specific mechanism: one companion solves a universal bottleneck.**
D2's Insight merc (Meditation aura, solves mana for every caster build) became mandatory not because it was overpowered but because mana is a problem *every build has*, making the companion choice class-agnostic. The Q8 matrix should have no companion strategy that is a valid fill for all player strategies. Each valid pairing should hinge on something *specific to that player-strategy combination.*

**6. D3 pre-2.7 follower irrelevance is the "stat-stick" failure case; the Emanate fix is instructive.**
Before patch 2.7, followers did not scale into endgame and were ignored. The fix was not to scale the follower's own damage — it was to give followers 13 gear slots with the Emanate mechanic, making their value the items they *carry*, not the actions they *take.* For Q8: companion validity should not depend on the companion's autonomous performance at endgame difficulty. It should depend on the convergence item mechanic, which is not subject to the same scaling constraint.

**7. D4 VoH Reinforcement trigger conditions are a direct model for convergence item activation logic.**
The second mercenary in D4 fires under these exact conditions: (a) when player casts a specific skill, (b) when player casts any skill in combat, (c) when player becomes CC'd, (d) when player loses 30%+ HP from a single hit. These are player-state conditions, not always-on buffs. The compound (player does X → companion fires Y) is legible, reactive, and creates emergent moments. The convergence item's activation should follow this pattern — fire on a condition from the player's strategy, produce a response from the companion's strategy.

**8. Isekai 2-slot party logic maps exactly to Q8's structure.**
The classic isekai 4-slot (vanguard, healer, mage/burst, support/buffer) has a canonical 2-slot contraction: protagonist fills one role, companion fills the complementary opposite. Confirmed examples: Rudeus (mage/burst) + Eris (vanguard/tank) in *Mushoku Tensei;* Naofumi (tank) + Raphtalia (damage) in *Shield Hero.* The 2-slot pairing is always a complementary-opposite, never a matching-same. The Q8 matrix is, structurally, a 25×25 version of this.

**9. Companion-as-identity (not stats) produces disproportionate player attachment.**
Baby Good Mimic in Enter the Gungeon is the genre's cleanest proof: a reformed enemy creature, mechanically modest, that generates strong attachment because its *nature* (a redeemed mimic, using mimicry to protect rather than deceive) reads as a meaningful character arc. For Reincarnated's "ascended spirits from the form-library" framing: the companion's spirit identity, origin, and bond-name are the primary attachment vehicle. The convergence item should carry bond-flavor — what these two spirits share — not just stat-flavor.

---

## Q1 — The Mercenary/Follower-as-Complement Canon

### Diablo 2 Mercenaries

The Act 2 Desert Mercenary is the genre's foundational companion-as-gap-filler. The system works through permanent auras addressing specific player deficiencies:

**Holy Freeze aura:** Permanently slows and chills all nearby enemies, creating a safe-fire zone for casters. Chosen when the player has no CC and needs positional safety. The merc's damage output is irrelevant — the aura IS the value. Most commonly paired with glass-cannon builds (Sorceress, fire Necromancer, Lightning Amazon).

**Might aura:** Amplifies physical damage. Chosen by non-physical builds to break monster physical-immune variants, or by summoner builds to amplify minion physical output. Note: Might on a physical-damage Barbarian is the canonical D2 "doubling down" mistake — the genre's first named example of redundant companion + player strategy.

**Insight runeword (gear-carried Meditation aura):** The single most impactful merc contribution in the game — mana recovery from Meditation. However, Insight became a mandatory cross-build choice (see Q4). Critically, the Meditation aura is delivered not through the merc's intrinsic design but through a player-crafted item the merc wears. The item (runeword) is the value carrier. The merc is the item platform.

**Infinity runeword (gear-carried Conviction aura):** Reduces enemy elemental resistances by 85%, breaking immunities the player cannot break otherwise. The highest-value gap-fill in the game — available only via the merc weapon slot — because the player cannot wear Infinity themselves.

Design note on the D2 merc system: the merc's intrinsic aura (chosen at hire) provides one function; the item it wears provides a second, often more impactful function. The best D2 merc configurations layer both: an intrinsic aura (Holy Freeze for CC) plus a gear-carried aura (Infinity for immunity-breaking) on the same character. This two-layer structure is worth noting for the convergence item: the companion's intrinsic strategy + the convergence item's bonus = two distinct contributions.

### Diablo 3 Followers

Three role-tagged followers with distinct function niches:

**Templar (tank/heal):** Life regeneration, defensive buffs, stun/freeze on enemies. Best paired with fragile/glass-cannon/hardcore builds. Chosen when the player cannot survive being hit. The Templar's post-2.7 strength: paired with Thunderfury (a chained lightning proc that slows enemies) it can function as a CC platform with utility items.

**Enchantress (buff/utility):** Attack speed buffs, cooldown reduction, CC via slow/freeze. Best paired with cooldown-dependent builds and builds needing sustained DPS uptime. The Enchantress's value is enabling more of the player's own output through CDR, not contributing her own damage.

**Scoundrel (damage-amplification):** Crit chance buffs, area CC. "Usually left unpicked" per community guides. The failure case: crit buffs for a damage-primary player add more of what the player already does. Pre-patch 2.7 the Scoundrel was effectively unmandatory except in specific builds that needed crit chance caps they couldn't reach themselves.

**Patch 2.7 Emanate rework (Season 23, 2021):** Followers gained 13 gear slots with legendary powers that Emanate (apply to player). Key items:
- Oculus Ring: Spawns a damage circle on enemy death (85% increased damage for player standing in it). The circle requires the follower to kill something (or be present at death), but the value is the player stepping into it. A positional "third thing."
- Nemesis Bracers: Spawns elite pack at each pylon. Follower wears this so player can use the bracers slot for other gear.
- Flavor of Time: Doubles pylon buff duration. Stacks with Nemesis Bracers for a compound effect.

The Enchantress is the dominant Greater Rift companion post-2.7, not because of her own actions, but because she can equip all eight of the best Emanate items due to her "access to all skills" passive.

### Diablo 4: Vessel of Hatred Mercenaries (2024)

Four distinct archetypes:

**Raheir (tank/bodyguard/defensive):** Shield-bearer, blocks incoming attacks, protects player. Barter specialty: Defensive Aspects. Reinforcement trigger: fires when player loses 30%+ HP from a single hit — a direct response to player failure state. Dominates adoption because survival is near-universal.

**Subo (utility/resource-gen/detection):** CDR, resource generation, "maphack" enemy/material reveal. Barter specialty: Utility Aspects. Pairs naturally with resource-starved builds. His Seeker skill pre-reveals enemies, enabling burst-setup builds to position before entering rooms.

**Varyana (melee sustained/overpower):** Close-range with a Massacre Meter that strengthens on kill streaks. Barter specialty: Mobility Aspects. The problematic case: her damage-output identity reads as redundant for damage-primary players. Her best complement is survivability-primary builds (tank/retaliation) that need burst output they can't generate themselves — but her stat identity mismatches that role.

**Aldkin (caster/CC/resource drain):** Shapeshifting, vulnerability debuffs, CC. Barter specialty: Resource Aspects. Mixed mechanics (guide notes they're "mixed badly") — simultaneously useful for casters who need vulnerability uptime and potentially penalizing for resource-hungry builds due to the drain component.

**Hire vs. Reinforcement:** Hired merc is a constant party member with full skills. Reinforcement fires once per condition met, then leaves. Reinforcement trigger conditions: (a) player casts a specific skill, (b) player casts any skill in combat, (c) player becomes CC'd, (d) player loses 30%+ HP. This condition-reactive design makes the Reinforcement feel like an answer to player state, not just a constant companion.

### Path of Exile — Animate Guardian

The AG is the genre's clearest "companion as pure gear carrier, no damage role" example. The AG wears unique items whose effects apply to nearby allies:

- **Leer Cast:** "You and nearby allies gain 50% increased damage." The AG does nothing but wear the helmet. The helmet IS the value.
- **Victario's Influence:** Grants aura effects to nearby minions. AG is a mobile aura platform.
- **Kingmaker:** Grants allies Fortify and Culling Strike. AG has near-zero damage but grants the player permanent Fortify uptime and a culling threshold.
- **Dying Breath:** Nearby enemies have 18% increased effect of curses on them. AG debuffs enemy curse-resistance, amplifying the player's curse effectiveness.

The AG has survived years of PoE meta cycles precisely because its value is independent of its own damage output — it does not scale with game difficulty, and neither does its contribution (the aura/buff effect is fixed). This makes it resistant to the stat-stick problem.

AG failure mode: AG death destroys the carried uniques permanently. This creates a meta where AG-carrying builds must invest heavily in AG survivability OR avoid the system in dangerous map mods.

### Last Epoch — Beastmaster Companions

Per-companion role breakdown (from community forum analysis):

- **Wolf:** Tank/buffer. "Makeshift tank, poor endgame damage scaling." Roar skill grants +25% melee damage + increased attack speed to nearby companions — specifically buffing the Scorpion. The Wolf+Scorpion cross-synergy creates a "third thing" (Roar+Scorpion together exceeds either alone).
- **Sabertooth:** Damage/bleed builds. Stacks bleeds quickly with attack speed nodes. Damage-primary companion, works when the player explicitly builds around companion output.
- **Raptor:** "Strongest pet by far" for raw damage. Best when player has become a companion-empowerment build (summoner-style), not when player is the primary damage source.
- **Bear:** Tank + damage. Taunt node at level 17/12 makes it the best aggro-drawer. Pairs with fragile builds needing a durable frontliner.
- **Scorpion:** DoT builds. Works with the Wolf's Roar. Lacks as a standalone companion.
- **Spriggan:** Healing aura — pure survival gap-fill. Chosen when the build has no self-heal.

Community design note: "It's best to think of your minion as a helpful ally, not your main source of damage." The Last Epoch design explicitly frames companions as supplements, not co-equal damage sources.

### Grim Dawn — Conjurer Companion Design

Conjurer (Shaman + Occultist mastery combo) uses two primary companions with differentiated roles:

**Briarthorn:** High health, high armor, aggro-draw via Taunt at level 17/12, reflects damage back to enemies. The "tank" companion — explicitly designed to soak hits and hold aggro for the player. Also applies damage-reflect CC, making it a dual tank/control gap-fill.

**Hellhound:** Offensive-primary, but not a traditional tank. Its Ember Claw skill generates threat focused on itself, functioning as a targeted aggro-drawer for specific contexts. Lower durability than Briarthorn; sometimes used as a "bomb" (resummoned at low HP to deal burst damage on resurrection).

Community note: "Conjurer has far stronger and tankier individual pets whereas Cabalist's are very frail." The design choice to make Conjurer pets durable (vs. frail-and-numerous Cabalist) reflects the one-companion-as-complement philosophy vs. the summoner-army philosophy. For Q8: Conjurer is the right analog, not Cabalist.

### Torchlight — Pet System

Torchlight's pet design is the clearest example of "companion as pure logistics, no combat role." The pet's primary function: carry surplus loot, teleport to town to sell items and buy potions while the player continues exploring. The pet can also cast scrolls (Town Portal, Identify).

Community note: "One of the distinguishing aspects of Torchlight is that pets can go to town and sell your stuff." This is a companion whose value is entirely in the dimension the player can't act in while fighting. It fills the "economy/logistics" gap without contributing any combat mechanics. Torchlight 3 extended pets with skill trees and auras, but the foundational design is logistics-first.

Design implication: the "economy/logistics" companion role is valid — it fills a real gap (inventory pressure, consumable supply). It maps to the "resource-gen" companion strategy in Q8 (the companion that keeps the player resourced vs. the companion that does things).

---

## Q2 — The Archetype-Pairing Map

### Canonical valid pairings (genre-validated)

| Player strategy | Companion role | Canonical game example | Why it works |
|---|---|---|---|
| Glass cannon / burst caster | CC / bodyguard (Holy Freeze) | D2: Blizzard Sorceress + Holy Freeze Act 2 merc | Merc creates safe-fire zone; player kills safely inside the slow field; no damage competition |
| Glass cannon / burst caster | Tank / aggro-draw | D4: any caster + Raheir; Last Epoch: fragile build + Bear | Companion absorbs hits player cannot survive; player kills without interruption |
| Pure damage / no CC | CC / controller companion | D3: damage build + Enchantress slow/freeze | Player creates burst windows; companion extends or creates those windows with CC |
| DoT / sustained damage | Burst finisher companion | Last Epoch: DoT Beastmaster + Sabertooth (crit burst) | Player applies persistent damage; companion fires burst payoff when target is weakened |
| Resource-starved (mana/energy) | Resource-generation companion | D2: any caster + Insight merc (Meditation aura) | Player's structural constraint solved; companion does exactly one job: keep player functional |
| Summoner / minion-master | Aura / buff companion | D2: Skeletal Necromancer + Might merc (amplifies minion physical) | Player's damage is distributed across minions; companion amplifies that distributed output |
| Tank / retaliation | Burst finisher companion | D4: tanky class + Varyana (Massacre burst) | Player sustains and holds enemies; companion delivers burst the tank's playstyle couldn't generate |
| AoE / clear build | Single-target finisher | Generic ARPG; PoE AG with Culling Strike (Kingmaker) | Player clears packs but struggles with single-target bosses; companion executes low-HP targets |
| Sustain / survival primary | Damage amplification | D3: Templar heals + Oculus Ring (damage amp for player standing in circle) | Player lives; companion creates conditions for more damage |
| Any build without detection/setup | Utility / detection | D4: any build + Subo (enemy reveal, resource gen) | Subo's maphack function pre-positions the player for burst; the setup is what the player's kit rewards |

### Canonical anti-fits (genre-validated failures)

| Player strategy | Companion role | Why it fails | Game example |
|---|---|---|---|
| Physical damage melee | Physical damage amp (Might aura) | Amplifies what player already does; no gap filled | D2: physical Barbarian + Might merc |
| Burst damage dealer | Burst damage companion | Two co-equal damage sources; additive not multiplicative | D3: Scoundrel on a Monk — both dealing same value type |
| Damage-primary caster | Another damage dealer | Redundant; companion damage fails to scale endgame | D3 pre-2.7: all followers used as damage dealers |
| Summoner (army) | More summoned units from companion | Scaling chaos; no control; no role complement | D2: skeletal necro + skeleton-producing companion |
| Any player vs. universal bottleneck | Universal bottleneck solver | Companion fills a problem every build has → mandatory for all → no expressive choice | D2: Insight merc for mana; D3 pre-2.7 Enchantress for CDR |
| CC-primary controller | CC companion | Two sources of CC; diminishing returns; target overcrowded | Generic; any "double CC" configuration |
| Survival-primary tank | Survival/heal companion | Player doesn't need help surviving; companion's healing goes to waste | D3: Templar with a tanky Crusader |

---

## Q3 — The Bond/Convergence-Item Mechanism

Three properties that make a bond mechanic feel emergent rather than additive (derived from genre analysis):

**Property 1: The mechanic only exists when both kit-halves are present.**
D3 Oculus Ring Emanate: the circle spawns because the follower exists, wearing the ring. The player steps into it. The follower's existence + the player's positioning + the freed gear slot = a three-part compound. If either half is absent, the mechanic does not exist.

**Property 2: The bond item is action-conditional, not always-on.**
D4 Reinforcement trigger design: the second mercenary fires exactly when the player's condition is met (loses 30% HP, casts specific skill, becomes CC'd). The compound (player state X → companion action Y) is legible and reactive. Compare to always-on flat buffs (+5% damage), which register as number soup and produce no moment of felt synergy.

**Property 3: The bond item carries semantic identity, not just a number.**
PoE AG items are named, identity-bearing uniques. Leer Cast is a helmet with a leering face; wearing it on the AG means your companion walks around emitting a laughing aura that buffs everyone. The item's identity is part of why it reads as synergy — you gear the companion as a character, and the character's outfit produces the effect.

### Specific bond-mechanism precedents

- **D3 Emanate (patch 2.7):** Item on follower → effect for player. The convergence item IS the binding mechanism. Value is carried by the item, not by the companion's actions.
- **D2 runeword-on-merc:** Items crafted specifically to be worn by the companion (Insight, Infinity). The item's value only expresses through the merc relationship — an Insight polearm in the player's stash does nothing.
- **D4 Rapport system:** Bond deepens over time, unlocking new passive options. Progression of the relationship unlocks mechanical depth (new skill points, loot caches, Pale Marks). The bond is a progression axis, not a binary switch.
- **Last Epoch Wolf + Scorpion cross-synergy:** The Wolf's Roar buffs the Scorpion specifically. Neither companion alone produces the Roar+Scorpion compound — taking both and investing in Roar is the "bond item" equivalent, a mechanical investment that only pays off when both halves exist.

**Design implication for Q8:** The convergence item should be action-conditional. It fires when the player's strategy condition is met, and produces the companion-strategy's response. It should have a name and semantic identity referencing the bond between the two spirit-types. The mechanic it creates must require both the player's kit-action AND the companion's presence — if it would work without the companion, it is not emergent.

---

## Q4 — Anti-Patterns: Where Companion Systems Failed

### 1. The mandatory-tax anti-pattern (D2 Insight merc, patch 1.10+, 2003—present)

Insight runeword on an Act 2 merc solves mana regeneration so universally that it is correct for every caster build. Community forums as late as 2021 (D2 Resurrected) confirm Insight is essentially mandatory for budget builds. The mechanism: Insight solved a universal bottleneck (mana), not a build-specific gap. Every build has a mana problem; every build takes the same answer; the merc's aura-variety (the intended choice axis) is overridden by gear. No design fix was applied in D2; the homogenization persists. D4 addressed it by making mercenary passives conditional on player-specific states.

### 2. The stat-stick failure (D3 followers, all patches before 2.7, 2012—2021)

Followers were ignored by endgame players for 9 years. The mechanism: follower damage was tied to the follower's own stats, which did not scale to match player power growth or enemy HP at high difficulty. Followers had roles (CC, heal, buff) but the contributions were too small to be noticed at endgame. The fix (patch 2.7) shifted value from "what the follower does" to "what items the follower carries." The follower became a gear platform, and its Emanate items create effects that don't degrade at endgame because they're flat mechanics (spawn elite, double pylon duration) not percentage-of-follower-damage contributions.

### 3. The companion-as-pure-aura-bot problem (D2 Act 2 Infinity merc)

Some D2 builds took an Act 2 merc purely for the Conviction aura from Infinity. The merc existed solely to walk behind the player emitting the aura, died constantly, and required rune-expensive resurrection. It had no identity, no role-drama, no moment — it was a mobile aura tower with bad survivability. Players invested in merc gear specifically to keep the aura-tower alive, not to make the merc a meaningful companion. The lesson: an aura-carrier companion must either have strong survivability (so it doesn't die and interrupt the buff) or its death must not matter (the buff comes from an item, and the item survives). D3's post-2.7 unkillable follower solves this perfectly.

### 4. Content trivialization via companion power creep (D2 Skeletal Necromancer, patch 1.09+)

At certain gear thresholds, a D2 Necromancer's army could clear content without the player actively participating. The player's role reduced to "walk into room, wait." This is a summoner-army pattern (not a single-companion pattern), but it surfaces the role-inversion risk: if companion contribution becomes so powerful that the player becomes a buff-taxi, the designed relationship inverts. For Q8: the ≤15% damage amp cap on companion buffs is not just a balance number — it is a role-inversion prevention mechanism.

### 5. The dual-damage redundancy failure (D3 Scoundrel; D4 Varyana-on-damage-builds)

The D3 Scoundrel's primary identity was damage amplification (crit buffs) for damage-primary players. Damage-primary players already have damage — the Scoundrel was adding more of what the player already does. The result: "usually left unpicked" per community guides. D4's Varyana has a structurally identical problem: her burst-damage identity reads as redundant for damage-primary builds; she pairs better with tank/survival builds who need burst output, but her stats and thematics misread as a damage companion. When both player strategy and companion strategy are in the same primary dimension, the compound is addition, not multiplication. This is the design rule for which Q8 cells are INVALID.

---

## Q5 — Isekai/Anime Party-Composition Resonance

### The canonical isekai 4-slot party

Confirmed across multiple series:

- *Grimgar of Fantasy and Ash:* Haruhiro (rogue/control), Yume (archer/ranged damage), Shihoru (mage/burst), Merry (healer/sustain), Ranta (aggressive fighter/tank-pressure).
- *Dungeon Meshi:* Laios (vanguard tank), Marcille (mage/burst), Falin (healer), Chilchuck (utility/trap-disarm).
- *Mushoku Tensei:* Rudeus (mage/burst), Sylphiette (utility/CC support), Eris (vanguard/melee tank). The 3-slot contraction of the canonical 4-slot.

The 4 roles: vanguard/tank (frontline, absorbs hits), healer/sustain (restoration, buffs), mage/burst (high output, low survivability), utility/buffer (CC, stat amplification). Every isekai party with 4+ members fills these roles, sometimes across a single character (role-compressed archetypes like the "battle mage" or the "paladin" who tank-and-heal simultaneously).

### The 2-slot contraction (the Q8 scenario)

When stripped to protagonist + one companion, the canonical pairings are:

- **Glass mage protagonist + tank companion.** Rudeus + Eris in *Mushoku Tensei* (early arcs). The mage does damage at range; the tank holds enemies and absorbs hits. The pairing is complementary-opposite: the thing the mage cannot do (survive a hit) is exactly what the tank provides.
- **Tank protagonist + damage companion.** Naofumi + Raphtalia in *Rising of the Shield Hero* (early arcs). The shield hero cannot deal offensive damage (his kit is purely defensive); Raphtalia deals all the damage. The player's inability to kill is the structural gap the companion fills.
- **Offense protagonist + healer/sustain companion.** The most common 2-slot configuration in the isekai genre. The hero does damage; the companion keeps them alive. This is the functional equivalent of the D2 glass-cannon + Templar configuration.
- **Overpowered protagonist + information/utility companion.** Rimuru Tempest + Great Sage (Raphael) in *That Time I Got Reincarnated as a Slime.* The "companion" is an intelligence that provides tactical analysis, identification of skills, and strategic advice — not combat contribution. This maps to the "utility/detection" companion role (Subo in D4 terms).

The 2-slot isekai party is *always* a complementary-opposite pairing. The genre has no popular examples of a protagonist + one companion where both fill the same role. A "glass mage + glass mage" 2-slot isekai party does not exist in the genre canon — it would not survive. This is the isekai genre's accumulated wisdom on the Q8 question, stated as narrative survival law.

### Companion-as-identity (not stats) — the draw is WHO they are

**Bond Creatures (TV Tropes):** A documented trope where a permanent empathic link between two characters allows them to share abilities. Established through narrative (a chosen relationship, a rescue, a resonance event), not through stat optimization. Mechanical benefits (shared abilities, improved stats) are framed as *expressions of the relationship's depth.* The bond deepens → the compound grows. This is the Rapport system in D4 as narrative — the relationship progression IS the mechanic progression.

**Seirei Gensouki: Spirit Chronicles:** A spirit-contract isekai where the bonded spirit has an independent identity and history. Bond established through elemental resonance, not stat optimization. The spirit's identity — what kind of spirit, what their past was — is the primary draw. The spirit provides both mechanical benefit (expanded magic, information, protection) and narrative role (companion identity, emotional anchor).

**Baby Good Mimic (Enter the Gungeon):** Reformed hostile creature, modest mechanical contribution, strong player attachment because its *nature* is meaningful. The "Baby Good" EtG naming convention (Baby Good Mimic, Baby Good Shelleton) is an entire companion archetype: former enemies made companions, each carrying the identity of what they were before they were "good." For Reincarnated: the player's form-library IS a library of past enemy-type forms. An ascended spirit companion that was "a form the player previously inhabited" is structurally Baby Good Mimic — a former adversary-type, now bonded, using its nature to protect rather than threaten.

**Design implication for Q8:** The companion's spirit identity should reference its archetype in the flavor layer of the convergence item and its entry in the form-library. The bond-narrative (what these two spirits share, what event the convergence represents) is the primary player-attachment vehicle. A companion labeled "Briarthorn tank spirit" is less compelling than a companion labeled "the iron-barked warrior from the forest-form you wore in your second reincarnation, now traveling forward with you." The convergence item's name should carry the resonance — not "Defense Talisman +15%" but something like "Bark-and-Flame Pact" or "The Weight of a Shared Season."

---

## Knowledge Gaps Not Resolved

1. **Torchlight 3 companion skill trees and aura specifics.** Sources confirmed the expanded pet system exists in TL3 but did not yield detail on how companion aura roles pair with build types.
2. **D4 VoH mercenary class-specific pairing data.** Confirmed the four archetypes; did not surface community consensus on which D4 class pairs best with which mercenary. This data likely exists in community tier lists.
3. **PoE Secrets of the Atlas mercenary system.** PoE introduced a distinct mercenary system separate from minion summoning. Sources confirmed the system exists but did not yield sufficient role-complementarity detail for this commission.
4. **Isekai JRPG game-mechanical companion design.** The isekai angle was sourced from anime series. *Ni no Kuni,* *Tales of,* and isekai-themed JRPGs may have more translatable mechanical companion design. This pass did not cover those.

---

**Author:** Legolas (Mode A), 2026-06-13. Captured by gandalf. Downstream consumer: gandalf Q8 companion-convergence matrix (`gandalf/notes/2026-06-13-q8-companion-convergence-matrix-scaffold.md`).
