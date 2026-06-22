# Research — D2 + PoE Endgame Elemental Resistance and Monster Modifier Mechanics — 2026-06-22

**Mode:** A (analytical)
**Commissioner:** gandalf (design steward)
**Scope:** Mechanics-level grounding on resist architecture, opportunity cost of capping, systems that keep resists live, rare/unique monster modifier taxonomy, and monster resist scaling across tiers — in Diablo 2 (LoD, post-1.10) and Path of Exile (PoE 1, pre-PoE 2).

---

## Comparison Table — Resist Cap Model

| Dimension | Diablo 2 LoD (post-1.10) | Path of Exile 1 |
|---|---|---|
| Base player resist cap | 75% | 75% |
| Absolute max resist cap | 95% (via items/skills) | 90% (via items/tree nodes) |
| Difficulty penalty to base resist | Normal 0 / Nightmare −40 / Hell −100 | −10% per act completion stamp (6 acts × −10% = −60% total at endgame) |
| Gear needed to reach cap vs penalty | ~+175 raw resist across gear in Hell | ~+135 raw resist across gear for maps |
| Overcapping purpose | Raises max resist (requires specific items) | Buffers against curse/exposure/map-mod reduction before cap is broken |
| Universal "all resist" affixes | Yes ("All Resistances" suffix) | Yes (both prefix "to all Elemental Resistances" and suffix; crafted variants) |
| Active mechanisms that break the cap | Conviction aura (monsters), Lower Resist curse | Elemental Weakness (curse), Exposure, penetration gems, map mods, "-max resist" mods |
| Immunity system | Yes — monsters at ≥100% resist become immune; breakable at 1/5 efficiency | No true immunity; penetration and curse drive resist negative (extra damage taken) |
| Endgame mandatory? | Yes — uncapped in Hell = near-instant death from elemental spikes | Yes — at 0% resist a T16 map boss kills orders of magnitude faster |

---

## Q1 — Endgame Resist Architecture

### Diablo 2 (LoD, post-1.10)

**Cap and max-cap mechanics.** The player's default resistance cap is 75% per element (fire, cold, lightning, poison). The theoretical absolute ceiling is 95%, reachable only by raising *maximum* resistance, which requires specific gear:
- Paladin's Resist Aura tree skill synergies can push max to 82–90% passively for the Paladin only.
- Items with "+X% to Maximum [Element] Resistance" exist but are rare (e.g., Stormshield unique shield: +8–10% max resist to all, Thundergod's Vigor: +10–15% to max lightning resist, Skullder's Ire: +1 to all max resists, Andariel's Visage: +1 all max resists). Stacking multiple such items across gear slots can reach 80–85% max resist for non-Paladins.
- Max all-resist 95% is theoretically achievable (Paladin with Redemption or Salvation at high slvl) but not a standard endgame configuration.

**Difficulty penalty.** Hell difficulty applies a flat −100 to all elemental resistances. Nightmare applies −40. Normal: no penalty. These are character-level offsets applied before the cap clamp:
- A character with no resistance gear in Hell starts at −100% to all elements (taking 200% of elemental damage — the extra 100% amplifies incoming hits above baseline).
- To hit 75% cap in Hell, a character needs +175 total raw resistance per element from gear, charms, skills, and quest rewards.

**Quest rewards.** Completing Anya's quest (Act 5, "Rescue on Mount Arreat") across all three difficulties grants +10 all resists per completion = +30 total across Normal/NM/Hell. This is a meaningful free 30 points toward the 175 needed.

**Gear sourcing — per-element vs all-resist.** D2 distinguishes:
- Per-element affixes (e.g., "of the Glacier" = +25–30 cold resist on jewelry) — higher per-element ceiling on rare items.
- "All Resistances" suffix — applies a single bonus to all four elemental resistances simultaneously. This is the more gear-efficient source and appears on rare/magic items and set/runeword items.
- Key runewords providing all-resist: Smoke (Nef+Lum, body armor) = +50 All Resistances; Rhyme (Shael+Eth, shield) = +25 All Resistances; Spirit (Tal+Thul+Ort+Amn, shield) = +35 cold/lightning/poison resist (not all); Ancient's Pledge (Ral+Ort+Tal, shield) = +43 fire, +48 cold, +43 lightning, +48 poison (per-element, totaling ~182 across four, covering most of the deficit for one gear slot).
- Smoke alone (+50 all resist) plus Ancient's Pledge shield (+43–48 per element) provides enough for most characters to cap in Hell without further optimization — but locks two major gear slots.
- Tal Rasha's Wrappings full set: +105 fire, +105 cold, +138 lightning, +65 poison resist (with full-set bonus +50 all) — extreme case; still needs two gear pieces.

**Failure mode of being under-capped.** At 0% resist, incoming elemental damage is unmitigated. At −100% (no gear in Hell), you take 200% of the listed damage (the extra is additive amplification). One-shot potential is extreme: in Hell, elite packs with fire/cold/lightning enchanted and spells like Hydras, Blizzard, or Charged Bolts deal damage calibrated to opponents AT cap. A character 40% under cap against a Burning Dead pack in Act 5 Hell (Chaos Sanctuary level) can die in 1–2 hits from Diablo's lightning hose or a Charged Bolt barrage. Under-capping is not viable at endgame Hell content — it is not an accepted trade-off for offense in the way PoE builds sometimes tolerate it on specific elements.

---

### Path of Exile 1

**Cap mechanics.** Default maximum resistance is 75% per element (fire, cold, lightning, chaos). The absolute cap is 90%, achievable by raising *maximum* resistance through passive tree nodes (e.g., "Elemental Adaptation" cluster = +4% max fire/cold/lightning resist; several such nodes scattered across the tree), gear affixes ("+1% to maximum [element] resistance," rare on high-ilvl gear), and certain unique items (Loreweave unique belt: base max resist set to a fixed 78–80% all, limited from stacking higher; Kaom's Heart: no resist slots at all — tradeoff).

**The campaign penalty.** Each of the 6 acts completed stamps a permanent −10% to all elemental resistances on the character, accumulating to −60% total by act 10. Chaos resistance has no such stamp but has no base gear contribution from the passive tree either — it must be sourced entirely from gear.

**Gear sourcing — all-resist vs per-element.** PoE gear affixes:
- "to all Elemental Resistances" — prefix or suffix depending on slot. Rings, belts, boots, gloves, body armor, helmets, amulets all carry this. Typical endgame values: boots/gloves suffix = +25–40%; rings suffix = +20–38%; belt suffix = +20–35%; body armor prefix = +12–24%. Two-Stone Ring base item has +12–16% built-in before affixes.
- Per-element suffixes ("to Fire Resistance") — appear on the same slots; rolls 1–10 points higher than all-resist rolls but only cover one element.
- Crafting: bench can add +(5–8)% or +(9–12)% to all Elemental Resistances as a crafted mod. A key gap-filling tool.
- In practice, a fully kitted endgame character gets resist from 5–7 gear slots simultaneously to hit 75% across all three (four with chaos). The crafting/trading meta is well-developed precisely because the gap is 135 points and each piece contributes 20–40.

**Failure mode of being under-capped.** At 75% fire resist, you take 25% of incoming fire damage. At 0% fire resist, you take 100% — a 4× multiplier relative to cap. At −75% (feasible via Elemental Weakness + Exposure on a bare character), you take 175%. T16 map pinnacle bosses — Sirus, Uber Elder, Shaper — have attacks dealing several thousand fire/cold/lightning damage per hit at full resist. A character 30% under cap against Sirus's Die Beam takes ~40% more damage per hit than a capped character; that converts from survivable to one-shot at most endgame HP totals. Under-capping is fatal against elemental-heavy bosses and punishes sustained map-running via attrition against DoT mechanics (ignite, shock). Some high-life/high-ES builds deliberately run uncapped chaos resist since chaos mitigation gear eats affix budget and chaos sources are rarer; this is a build-specific risk calculus, not a general practice.

---

## Q2 — Opportunity Cost of Capping

### Diablo 2

**Budget framing.** In Hell, reaching 75% on all four elements from −100 baseline requires ~175 raw resist per element. Achievable combination: Smoke body (+50 all) + Ancient's Pledge shield (+43–48 per element) + Anya quest reward (+30 all across Normal/NM/Hell) + three small charms with "All Resistances +5–11" each + two rare rings/amulets. The body armor and shield slots are both major optimization slots — a Chains of Honor or Enigma runeword body armor and a Stormshield or Spirit shield are endgame BiS offensive/utility choices. Smoke is budget/ladder-start; Ancient's Pledge is early-cycle placeholder.

**Trade-off sharpness.** Yes — capping requires locking either the body armor slot or the shield slot (or both) to resist-primary items at early-to-mid Hell. A non-capped but offense-invested character (e.g., holding Grief phase blade + high-offense body armor) will do more damage but die easily to elemental damage types. Most experienced players cap resists first, then optimize offense. Charms (small charms with all-resist, large charms like Hellfire Torch +10–20 all resist, Annihilus unique charm +10–20 all resist) allow capping without locking armor/shield slots — but those charms are high-value trade items costing real in-game currency.

**Endgame expectation.** Capping all four elements in Hell is the assumed baseline for any viable character. Running uncapped on any element is considered a beginner error or a temporary ladder-start concession. "Cap resists" is step one of every D2 build guide.

---

### Path of Exile

**Budget framing.** With a −60% penalty, a character needs +135 raw resist per element from gear plus passive tree. Passive tree alone can contribute ~50–80 all-resist (from resist clusters, +max nodes, elemental adaptation nodes). That still requires 55–85 additional points from gear per element. A 6-slot gear configuration spending ~25–35 each covers the gap but consumes: one suffix on each ring, one suffix on belt, one suffix on boots. That is 4 out of 6 available suffixes on major accessory slots — significant. Helm, body armor, and gloves must cover the remaining gap or compensate.

**The chaos resist problem.** Chaos resist has no passive tree contribution base and no campaign reward. Every point of chaos resist must come from gear. Chaos-resist-capping requires a whole extra affix budget axis. Many builds deliberately do NOT cap chaos resist (run at 10–40%) and compensate with high life. This is the most common explicit trade-off in PoE gearing.

**"Cap everything" as default?** For fire/cold/lightning: yes, hard expectation. For chaos: build-dependent — a life/evasion character with 5000+ HP often skips chaos cap; a low-life or CI character ignores chaos entirely. The opportunity cost is real but the meta around Two-Stone Rings and resist-heavy crafting has made reaching 75% fire/cold/lightning achievable without sacrificing all offensive affixes, particularly for melee builds that use life/strength gear bases with resist sub-affixes. Caster builds suffer more because their amulets and rings are under more pressure from damage affixes.

---

## Q3 — Keeping Capped Resists Meaningful

### Diablo 2

**Conviction Aura (Paladin skill / Aura Enchanted monsters).**
- Applied by: high-level Paladins (Hammerdin, Smiter), Aura Enchanted unique monsters using Conviction, Uber Mephisto (slvl 20 Conviction), Infinity runeword (slvl 12 Conviction).
- Effect: reduces enemy Fire, Cold, and Lightning resistances by a flat percentage. Does NOT affect Magic or Poison resistance.
- Level table (selected): slvl 1 = −30%; slvl 5 = −50%; slvl 10 = −75%; slvl 12 = −85% (Infinity runeword); slvl 15 = −100%; slvl 20 = −125% (Uber Mephisto); slvl 25 = −150% (hard cap).
- Maximum the aura can reduce resist: −150%, also the cap on what the aura applies.
- Against non-immune monsters: full value applies. A player at 75% fire resist with a slvl 12 Conviction on an enemy (−85%) sees the enemy's fire resist go from (e.g.) 50% → −35%. That enemy now takes fire damage as if it had negative resist — taking MORE than 100% of raw fire damage.
- Against immune monsters: the 1/5 rule. A monster with 110% fire resist (immune) against slvl 12 Conviction: −85% × 0.2 = −17% effective. 110 − 17 = 93% — no longer immune, but still 93% fire resistant. Still highly resistant; not killable efficiently with fire.
- Aura Enchanted monster Conviction level: max(mLVL / 8, 1). A Hell Act 5 monster at area level 85 → mLVL 85 → slvl 10 Conviction (−75% resist reduction). Against a player with 75% capped fire resist: player's fire resist is now 0% (75 − 75 = 0). Maximum Resistance does NOT protect against Conviction; it only caps how high your resist can go, not how far it can be reduced. A 75% cap + 75% Conviction = 0% effective — you're taking full fire damage. This is the primary mechanism making capped resist a live concern against Aura Enchanted packs.

**Lower Resist (Necromancer curse).**
- Applies to: Fire, Cold, Lightning, and Poison resistances. Does NOT affect physical or magic.
- Level values: slvl 1 ≈ −30%; slvl 10 ≈ −50%; slvl 20 ≈ −62%; slvl 40 ≈ −80% (with +skills).
- Against non-immune monsters: full value. At slvl 20, a monster at 0% resist drops to −62% (taking 162% elemental damage).
- Against immune monsters: 1/5 effectiveness. Can break immunities up to ~113% base resist (113 × 0.2 = 22.6 reduction; 113 − 22.6 = 90.4; below 100, immune broken). Monsters with 115%+ resist cannot be broken by Lower Resist alone (even with cold mastery or conviction stacking, max breakable in-game is ~110%).
- Conviction + Lower Resist stacking: when both are applied to an immune monster, both are reduced to 1/5 before combining.

**Sunder Charms (D2R Patch 2.5, Ladder Season 1, 2022 — version-dependent).**
- A PoE-expansion-era addition (not in original 1.10 LoD). Six grand charms, one per element.
- Mechanic: when held by the player, the Sunder Charm sets an immune monster of that element to exactly 95% resistance (from whatever higher value). Immunity is broken, converting a "cannot damage at all" situation to "95% resistant."
- Player penalty: the matching element's resistance is reduced on the player by −70 to −90% (rolls a range). Example: Flame Rift (fire) reduces player's fire resist by −70 to −90%. This is a substantial self-debuff — a player at 75% fire cap now runs at −15% fire resist (taking 115% fire damage) if they hold Flame Rift.
- Post-sunder immunity interaction: Conviction and Lower Resist still apply at 1/5 effectiveness to sundered monsters. Example: monster sundered to 95% fire resist + slvl 12 Conviction (−85% at 1/5 = −17%) → 95 − 17 = 78% fire resist. That is now a damageble number for fire builds.
- Trade-off: holding one Sunder Charm occupies a grand charm inventory slot (also takes up a charm slot costing item-find potential) AND permanently penalizes your own resist for that element. High-resist gear is mandatory before using Sunder Charms viably.
- Version note: Sunder Charms exist only in D2R Patch 2.5+ (Ladder Season 1 forward). Not present in original LoD 1.10. The original game had NO mechanism to break immunities reliably — Conviction and Lower Resist could reduce immune monster resist but at 1/5 efficiency only.

**Monster Immunities and the area-difficulty curve.**
- Normal difficulty: few monsters have any immunity.
- Nightmare: some monsters in later acts have one immunity; players generally encounter their first "cannot damage" moment here.
- Hell: nearly every monster type has at least one immunity. Zone-specific immunity distribution varies: Act 4 Chaos Sanctuary monsters (Oblivion Knights, Venom Lords, Doom Knights) are heavily fire- and cold-immune requiring lightning or poison solutions; Act 5 (Nihlathak area, Worldstone) has heavy fire and lightning immunity density.
- Unique monsters in Hell can spawn with an additional immunity on top of their base immunity (Magic Resistant or Fire/Cold/Lightning Enchanted affixes can push a borderline immune to confirmed immune), potentially creating dual immunity situations requiring multiple damage types.
- Unbreakable immunity thresholds (post-1.10): 144% for fire/cold/lightning, 124% for physical, 114% for poison. Monsters above these thresholds cannot be reduced below 100% even by full-strength Conviction + Lower Resist — true hardwall.

**"-Max Resist" effects.** Unlike PoE, D2 does not have map mods reducing player maximum resistances. The player maximum resist floor is stable at 75% unless raised. The primary live mechanic is monster-side (Conviction, immunities), not player-max-resist reduction.

---

### Path of Exile

**Elemental Weakness (Hex curse).**
- Applied by: player enemies (map bosses, special monster types that cast curses), Hexer Archnemesis modifier, maps with Elemental Weakness mod.
- Effect (version-dependent): Pre-3.20 = −20% all elemental resists at slvl 1, scaling to −39% at slvl 20. Post-3.20 patch: −15% at slvl 1, −30% at slvl 20 (reduced in a resist-rebalance pass).
- Map mod version: fixed at slvl 1 (−15% post-3.20 on maps; was −20% pre-3.20). Rolling Elemental Weakness on a map is considered a dangerous map mod — the most impactful curse players avoid or compensate for.
- Overcapping interaction: if a player has 100% fire resist (25% overcapped) and takes a slvl 1 Elemental Weakness curse (−15%), their fire resist drops to 85% uncapped — still capped at 75%, no damage effect. The overcap acts as a buffer. If Exposure (−20%) also applies: 85 − 20 = 65% — now they're 10% under cap and taking noticeably more fire damage. Overcapping by 30–40% is standard for players who run maps with curse mods.

**Exposure.**
- A separate debuff stack from curses; both can apply simultaneously.
- Default Exposure effect: −10% to the relevant resistance. Can be improved by "increased Effect of Exposure" modifiers on gear/tree (to approximately −15% or more).
- Applied by: some skill supports (Frost Bomb, Shattering Steel supports), certain passive tree keystones, monster skills (some bosses apply Exposure natively).
- Map mods do NOT typically apply raw Exposure, but monster skills in maps can.

**Penetration (spell/attack gems).**
- Operates after all other resistance calculations. Unlike curses/exposure (which lower the uncapped resistance), penetration is applied as effective resist reduction at the moment of damage calculation, not to the underlying resistance value.
- Does NOT affect the player's character sheet resistance; it's a damage calculation modifier.
- Values by gem (at max level): Fire Penetration Support = 34% fire resist penetrated; Cold Penetration Support = 34%; Lightning Penetration Support = 34%; Elemental Penetration Support = 28% (all three elements simultaneously, lower than per-element gems). Plus "Call to Arms" notable and various item modifiers can add 5–15% additional penetration.
- Effect at cap: a monster at 75% fire resist struck by a skill linked to Fire Penetration Support (34%) takes damage as if the monster had 41% fire resist. Since PoE monsters aren't typically at 75% resist (unlike players), penetration is primarily used against high-resist rare/unique monsters and bosses.
- Penetration does NOT apply below 0% — if resist is already negative, penetration provides no additional benefit.

**"-Max Resistance" map mods.**
- High-tier map suffix "of Exposure" (red map tier): "Players have −(9–12)% to all maximum Resistances." This is the most dangerous defensive map mod in PoE. At the high roll (−12%), a player's maximum fire/cold/lightning resist drops from 75% to 63%. They now take 37% of fire damage instead of 25% — a 48% relative damage increase.
- Stacked with Elemental Weakness map mod: −12% max resist + −15% curse = even uncapped resist isn't sufficient to maintain cap. Players building for high-quantity map-running sometimes refuse to run both simultaneously.
- Sirus fight (Awakener pinnacle boss): has a native mechanic that reduces player maximum resistances periodically during certain phases (via the Die Beam and rotating arena decay), making overcapping and sustaining the max resist value during the encounter a live concern.

**"Monsters deal extra damage as [element]" map mods.**
- A distinct axis from player resist reduction. Monsters can roll a map suffix like "Monsters deal X% of Physical Damage as [Fire/Cold/Lightning/Chaos] Damage." At high values (20–30% extra elemental), the practical effect is that a player who is capped on fire is still taking 20% more effective elemental damage than expected relative to the monster's base damage profile. This interacts with player resists but doesn't reduce them — it inflates the denominator of damage that matters.

**Reflect (legacy mechanic, pre-3.0 era, largely removed).**
- In earlier PoE leagues, rare monsters could have an Elemental Reflect modifier returning a percentage of elemental damage to the attacker. High-burst elemental builds would one-shot themselves. Reflect was removed from the game as a monster mod for rare/unique monsters in 3.0 campaign changes; map-level Reflect mods still existed on specific old maps. By 3.15 onward, Reflect mods were heavily revised or removed from most content.

---

## Q4 — Rare/Unique/Champion Monster Modifier Systems

### Diablo 2

**Three monster tiers above Normal:**
1. Champions — preset types (5 types) with fixed stat bonuses, spawn in packs of 3–5.
2. Unique (Boss) — single named monster with random affixes, spawns with a pack of minions.
3. Superunique — specific named monsters at fixed locations (Andariel, Diablo, Bishibosh) with fixed preset modifiers ± difficulty-scaling additions.

**Champion Types (stat bonuses).**

| Type | HP bonus | Damage | Speed | Special |
|---|---|---|---|---|
| Base Champion | ×3 Normal / ×2.5 NM / ×2 Hell | +90%/+75%/+66% | +20% run | +2 mLVL |
| Berserker | ×4.5 Normal (×3.75 NM / ×3 Hell, cumulative) | +270%/+225%/+198% | standard | +3 mLVL; ×5 exp |
| Fanatic | ×3 / ×2.5 / ×2 | +90% | +100% run | −70% defense |
| Ghostly | ×3 / ×2.5 / ×2 | +90% | −50% run | 80% physical resist (replaces all other values); cold damage on hit |
| Possessed | ×6 Normal / ×5 NM / ×4 Hell | +90% | standard | Immune to curses |

Note: Ghostly's 80% physical resist is categorically different from Stone Skin (50% phys resist on a boss affix) — Ghostly is a champion type, not an affix, and sets physical resist to 80 flat.

**Unique/Boss Affixes (1 in Normal / 2 in Nightmare / 3 in Hell).**

| Affix | Mechanical Effect | Key Numbers |
|---|---|---|
| Extra Strong | +damage and +AR on boss and minions | Boss: +135%/+112%/+99% dmg by difficulty |
| Extra Fast | +100% Faster Run/Walk for boss and minions | — |
| Cursed | 75% chance per melee/missile hit to apply Amplify Damage curse | Skill level = (mLVL/5)+1 |
| Magic Resistant | +40% Cold, then +40% Fire, then +40% Lightning resist (sequential, up to 2 immunities) | Capped at creating no more than 2 immunities |
| Fire Enchanted | Adds fire damage mLVL×0.66 to mLVL; death explosion dealing 3.5–5.8% (NM) or 0.4–0.6% (Hell) of base max life; +75% fire resist | Death explosion scales DOWN by difficulty |
| Cold Enchanted | Adds cold damage mLVL×0.66 to mLVL; cold nova on death at slvl = mLVL/2; +75% cold resist; cold length (mLVL×0.2)+4 seconds | — |
| Lightning Enchanted | Adds lightning damage mLVL×0.66 to mLVL; releases 8 charged bolt missiles on hit; +75% lightning resist | Bolts deal (2×(mLVL/2))−1 per bolt |
| Mana Burn | Mana damage (same formula as above); drained mana converted to life for boss; +20% magic resist | Devastating for mana-dependent builds |
| Stone Skin | +50% physical damage resistance; +200% base defense | Hell: effectively 100% physical resist per community note — may be mechanic rounding |
| Aura Enchanted | Grants one of: Might, Holy Fire, Holy Freeze, Holy Shock, Blessed Aim, Conviction, or Fanaticism | Level = max(mLVL/8, 1); Conviction at this level can fully drain player resist cap |
| Spectral Hit | Adds random elemental damage type (Magic/Fire/Lightning/Cold/Poison) per hit; +20% resist to that element | Elemental: mLVL×0.66 to mLVL |
| Teleportation | Boss teleports when below 30% HP (melee) or within melee range (ranged); restores up to 30% life | — |
| Multiple Shots | Boss fires 3 missiles per attack | Ranged types only |

**Aura Enchanted — Conviction detail.** When a unique monster spawns with Conviction aura in Hell at area level 85: Conviction slvl = 85/8 ≈ 10 (rounded down). At slvl 10, Conviction applies −75% to all nearby player fire/cold/lightning resistances. A player with 75% capped resist is now at 0% effective resist. A player with 85% capped resist (via Paladin passive tree) drops to 10% effective. This is the single most threatening affix for elemental builds — a normal affix roll that can completely neutralize capped resists.

---

### Path of Exile

**Monster rarity tiers:** Normal, Magic (1–2 affixes), Rare (prefix + suffixes, one may be an aura), Unique (fixed preset; pinned to specific encounters or map bosses).

**Rare monster affix count:** 3 total (typically 1 prefix + 2 suffixes, or variations). One of the three may be an aura mod applying effects to nearby allies.

**Archnemesis system (PoE 3.17–3.19) — now partially integrated into core rare mods (3.20+).** In 3.20+, the complex named Archnemesis recipes were dissolved back into the normal rare-mod pool, but many of the mechanical effects survived as named modifiers. Key modifiers with resist/damage relevance (as of 3.17–3.24 era, including post-integration):

| Modifier | Key Mechanical Effects |
|---|---|
| Flameweaver | +50% fire resist; converts 25% phys → fire; 50% phys as extra fire; fire ailment immunity |
| Stormweaver | +50% lightning resist; converts 25% phys → lightning; 50% phys as extra lightning; lightning ailment immunity |
| Frostweaver | +50% cold resist; converts 25% phys → cold; 50% phys as extra cold; cold ailment immunity |
| Chaosweaver | +50% chaos resist; converts 25% phys → chaos; 15% non-chaos as extra chaos |
| Crystal-skinned | +40% all elemental resistances; fires crystals; cold explosion on death |
| Empowered Elements | Cycles through elemental affinity every 4 sec; 90% resist to non-affinity elements; +50% damage taken from current affinity type | 
| Storm Herald | +40% lightning resist; 30% increased lightning damage; 25% phys as extra lightning; 50% phys converted to lightning; 50% reduced lightning ailment effect |
| Incendiary | +75% fire resist; guaranteed ignite on hit; 300% increased ignite damage |
| Dynamo | Lightning ailment immunity; guaranteed shock on hit; 25% increased shock effect |
| Permafrost | Cold ailment immunity; 25% freeze chance; 25% increased freeze duration |
| Consecrator | Spawns consecrated ground; 2% life regen/sec to allies; 30% reduced elemental damage taken by monster |
| Hexer | Casts Elemental Weakness or Temporal Chains or Enfeeble on nearby players (the debuff that hits players is active in real-time) |
| Hasted | +40% movement speed; +100% evasion; nearby allies +30% attack/cast speed |
| Crystal-skinned | +40% all elemental resistances |
| Juggernaut | Cannot be slowed; +2 maximum endurance charges; auto-charges when hit |
| Sentinel | Blocks 50% of attack and spell damage; +10% block per type |

**How map mods layer on top.** Map modifiers apply to the whole map instance independent of individual monster mods. Relevant map mod categories:
- "Monsters deal X% of Physical Damage as [Fire/Cold/Lightning/Chaos] Damage" — effectively a damage type shift/addition applied to ALL monsters in the map.
- "Players have −(9–12)% to all maximum Resistances" (red tier suffix "of Exposure") — reduces every player's max resist cap.
- "Area is inhabited by [element] monsters" — biases the monster pool toward fire/cold/lightning-typed monsters, creating elemental damage type concentration.
- Elemental Weakness curse on maps (slvl 1) — see Q3 above.
- "Monsters' skills chain X additional times," "Monsters have X% increased Area of Effect," "Monsters gain an additional Endurance/Frenzy/Power Charge on Kill" — these compound with elemental mods to create danger.

**Version note.** The Archnemesis system as a player-facing mechanic existed from 3.17 to 3.19. From 3.20 onward, GGG reworked rare monster mods back to a simpler list; many Archnemesis effects were preserved as core rare mods but some were culled. The Flameweaver/Stormweaver/Frostweaver/Chaosweaver pattern (elemental conversion + resist) is stable through 3.25.

---

## Q5 — Monster Resist + Damage Development Across Tiers

### Diablo 2

**Difficulty scaling architecture.** D2 uses three static difficulty tiers (Normal / Nightmare / Hell) rather than continuous scaling. Monster resist and HP are baked into static tables per-monster-per-difficulty, not dynamically scaled to map tier.

**How monster resistances are set:**
- Base monster resistances are defined per monster type per difficulty in the game data (monstats.txt in modding terms). Hell difficulty versions of monsters have their resistances elevated manually in the static tables — this is not a formula but a per-monster editorial decision.
- Example: Bishibosh (a Superunique Fallen Shaman) has 140% fire resistance in Normal — unbreakable fire immunity even at Normal. Other monsters may have 50% fire in Normal, 75% in Nightmare, 95%+ in Hell.
- The general pattern: Normal monsters rarely have >75% in any element (so no immunities with rare exceptions). Nightmare monsters often have 75–95% in one element (borderline immune). Hell monsters routinely have 100–125% in one or more elements (confirmed immune, with the higher values requiring extraordinary resistance reduction to break).

**"/players X" command.** D2 allows a command that simulates multiplayer (more players) without additional humans. At /players 8: monster life is multiplied by 4.5× (formula: Life × (N+1)/2, N=8 → ×4.5). Resistances and immunities are NOT changed by /players X. It is solely an HP and item-drop scaler.

**Area level (alvl) and its effect on monster stats.** Each zone has a fixed area level. Monster level (mLVL) is the higher of alvl or the minimum monster level for that type. Higher mLVL increases: raw damage (via per-level scaling formulas), experience, and the effectiveness of mLVL-scaled affix effects (Extra Strong damage scales with mLVL, Enchanted damage scales with mLVL). But resist values themselves are fixed in the data tables — mLVL does not raise base resist.

**Hell Act distribution of immunities.** All five acts in Hell have immunity-heavy monster populations:
- Act 1 Hell: Cold Plains (cold, lightning, poison, physical immunities distributed across the zone's monster population), Blood Moor (cold, fire), Caves (fire, cold, lightning by monster type). Immunities present from the first zone.
- Act 3 Hell: Jungle areas have spider/tentacle monsters with multiple immunities; Council members (Kurast) are fire or cold immune by subtype.
- Act 4 Hell (Chaos Sanctuary): Oblivion Knights = cold/fire immune; Doom Knights = cold immune; Venom Lords = fire immune; Pit Lords = fire immune. Lightning builds are strongly preferred here.
- Act 5 Hell (Arreat): Frenzytaurs = lightning/cold immune; Enslaved = fire immune; Nihlathak's temple (Halls of Pain) has heavy lightning immunity in monsters. Worldstone Keep acts as a gauntlet requiring multiple damage types or consistent immunity-breaking.

**Overall damage type distribution.** The game does not weight zone monster populations toward any one element for resistance purposes — it distributes so that any single-element build will encounter 25–40% of monsters in Hell that it either cannot damage or damages very poorly. This forces either: (a) a secondary damage type, (b) Conviction/Lower Resist support, (c) physical damage as the base (physical immunities are rarer and concentrated mostly in undead-type areas).

---

### Path of Exile

**Monster resist architecture.** PoE monsters do NOT have the same kind of per-monster manually tuned resistance tables as D2. Instead:
- Normal-rarity monsters have low base resistances; most enemy types in the campaign have 0% elemental resistance or very low values unless they are explicitly "fire-themed" (e.g., fire golems, ash priests) with higher base fire resist.
- Map tier (T1–T16) primarily affects monster level (mLvl 68–84+) which scales HP, damage, and accuracy. Monster level itself does not raise base resist — monster BASE resist stays close to 0% for most normal-tier enemies throughout.
- No immunity system exists for players in standard PoE. "Immunity" as a concept exists for monsters only in specific cases: some unique monsters have 0% of a damage type (functionally blocking it), and some minion-type monsters have immunity phases as a boss mechanic.

**How map mods create elemental variance:**
- A map with "Monsters deal 25% of Physical Damage as Fire Damage" effectively gives all monsters in the instance a fire damage component layered onto their physical attacks — changing the damage type mix the player faces.
- "Area is inhabited by [Monsters] with Elemental Damage" biases the monster-type pool toward high-elemental-output monster families.
- "Monsters are Hexproof" on a map makes curse-based defense (like Temporal Chains as crowd control, Elemental Weakness as a damage boost) nonfunctional — a significant modifier for curse-dependent builds.

**Pinnacle boss design.** PoE's primary endgame resistance stress comes from boss fight design rather than from monster-pool immunities:
- Shaper (T16 Shaped Maps): heavy cold and physical attack patterns; cold/lightning Bullet Hell phase. Capped cold resist is essential.
- Sirus (Awakener): fire/lightning die-beam; rotating storm rings; some phases reduce player max resist as a mechanic.
- Uber Elder (combination): fire (Elder) + cold (Shaper tentacles + icestorm). Running both fire and cold capped is mandatory.
- Uber Atziri: reflects damage in one phase — old reflect mechanics still active in this specific fight (a legacy exception). Elemental builds must manually turn off damage during the reflect phase.
- Maven (T16 Maven Invitation): orchestrates all pinnacle bosses simultaneously + memory game mechanics; broad elemental coverage required against combined boss pools.

**Post-campaign resist penalty as the core tension.** PoE's primary mechanism for keeping resist a live problem is the act-completion stamp. Unlike D2 where the penalty is a one-time hit at entering Hell, PoE applies the penalty incrementally as the player progresses through Acts 1–10. The result is that resist re-capping is an ongoing process throughout the campaign, and newly equipped items must constantly re-evaluate resist coverage. Every time a player swaps a piece of gear, they re-check their resist totals because the penalty has made the system not self-correcting.

---

## Knowledge Gaps Not Resolved

1. **D2 per-zone monster resistance tables.** Full monstats.txt data (which lists every monster's exact resistance by difficulty) requires direct game file access or fan-database crawl; could not retrieve specific percentages for all Hell zones. The Arreat Summit and Diablo Wiki have partial data; a full immunity database exists at maxroll.gg/d2 but was not crawled at asset level.
2. **PoE post-3.20 rare monster mod complete table.** The full list of current rare monster prefix/suffix mods in PoE 1 (post-Archnemesis 3.20 rework) is on poewiki.net's "List of monster prefix mods" and "List of monster suffix mods" pages — both returned 403 on direct fetch. The Archnemesis era mods are well-documented above; the exact current reduced pool is not fully enumerated here.
3. **PoE map mod resist-reduction exact value ranges.** The specific value range for "Players have −X% to elemental resistances" (non-maximum; affecting uncapped resist directly) on maps is unclear — search results conflated it with the maximum-resist reduction mod. It may exist only as the maximum-resist variant in current PoE. Needs direct wiki page fetch.
4. **D2 LR + Conviction combined threshold tables.** Exact combined breakpoints for which Hell monster resist values are breakable via Conviction at various levels + Lower Resist at various levels are calculable from the 1/5 rule and the data above, but no authoritative table was found verifying the full matrix.
5. **PoE monster base resist values by type.** PoE monsters' base resist values per type (especially fire golems, ice witch types, etc.) are not enumerated — only the general "near 0% for normal rarity" pattern is established. Specific monster types with elevated base resists would require poewiki.net monster data pages.

---

## Source List

- classic.battle.net/diablo2exp/basics/resistances.shtml (Blizzard official, Arreat Summit)
- maxroll.gg/d2/resources/elite-monster (D2R elite monster mechanics, fetched 2026-06-22)
- maxroll.gg/d2/resources/immunities (D2R immunity mechanics, fetched 2026-06-22)
- maxroll.gg/d2/resources/sundered-charms (Sunder Charm mechanics, fetched 2026-06-22)
- diablo2.io/skills/conviction-t4034.html (Conviction skill data, fetched 2026-06-22)
- diablo.fandom.com/wiki/Conviction (Conviction wiki, search result data)
- diablo-archive.fandom.com/wiki/Resistances_(Diablo_II) (D2 resistance wiki, search result data)
- purediablo.com strategy/monster-resistances-immunities-guide (search result data)
- www.pathofexile.com/forum/view-thread/3267228 (GGG official Archnemesis modifier list, fetched 2026-06-22)
- vhpg.com/poe-nemesis-modifiers/storm-herald/ (PoE Nemesis modifier data, fetched 2026-06-22)
- mobalytics.gg/poe-2/guides/resistances (PoE 2 resistance guide, consulted for mechanics cross-reference)
- mobalytics.gg/poe-2/guides/penetration (PoE penetration mechanics cross-reference)
- pathofexile.fandom.com/wiki/Elemental_Weakness (Elemental Weakness wiki, search result data)
- poewiki.net/wiki/Elemental_Penetration_Support + Fire/Cold/Lightning Penetration Support (penetration gem values, search result data)
- vhpg.com/all-elemental-resistances/ and vhpg.com/poe-archnemesis-mods/ (PoE resist crafting + mod data, search result reference)
- gamefaqs.gamespot.com/boards/605432-path-of-exile/78436476 (overcap community discussion)
- pathofexile.com forum threads (3265213, 3705932, 3727782) — community mechanics discussion
- d2runes.io/runewords/ and diablo2.io/runewords/ — runeword resist values
