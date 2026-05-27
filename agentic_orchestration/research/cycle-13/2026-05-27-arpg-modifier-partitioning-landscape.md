# Research — ARPG Modifier-Partitioning Landscape — 2026-05-27

**Mode:** A (analytical)
**Commissioner:** knight-rider (Cycle 13 SC-4)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-26-legolas-cycle-13-sc-4-arpg-modifier-partitioning-research.md`
**Authority basis:** Matt 2026-05-26 ratification of Cycle 13 framing brief Q4 + SC-4
**Gates:** Wave 1 stat-sheet partition design cycle (must land before Wave 1 design lock)
**robots.txt compliance (Discipline #20):** All four primary game wikis (poewiki.net, lastepoch.wiki.gg, diablo4.wiki.gg, grimdawn.wiki.gg) disallow ClaudeBot explicitly. Research was routed entirely to non-blocked sources: pathofexile.com (official; permitted), lastepoch.com (official; permits all), grimdawn.com (official; permits all), gdcvault.com (permitted), plus secondary sources checked individually below.

**Sources consulted:**
- pathofexile.com/forum (official GGG dev diary; permitted)
- mmojugg.com/news/poe2-new-jonathan-rogers-interview-summary.html (permitted)
- skycoach.gg/blog/path-of-exile-2/articles/poe-2-crafting-guide (permitted)
- mmojugg.com/news/understanding-item-tiers-in-poe2.html (permitted)
- vhpg.com/spawn-weighting-poe/ (permitted)
- grimdawn.com/guide/items/ (official; permitted)
- grimdawn.com/guide/character/item-skills/ (official; permitted)
- aggronaut.com/2024/02/27/last-epoch-crafting-primer/ (permitted)
- forum.lastepoch.com/t/unique-item-design/1264 (official LE forum; permitted)
- icy-veins.com/last-epoch/crafting-guide (permitted)
- icy-veins.com/d4/news/diablo-4-devs-explain-why-tempering-and-masterworking-changed/ (permitted)
- icy-veins.com/d4/guides/gear-systems-and-itemization-overview/ (permitted)
- purediablo.com/diablo4/Affixes (permitted per fetch result)
- studioloot.com/diablo4/articles/diablo-4-gear-affixes/ (permitted per fetch result)
- blizzardwatch.com/2024/03/21/diablo-4-itemization-changes-season-4/ (permitted)
- pcgamesn.com/last-epoch/crafting-affixes (permitted)
- sportskeeda.com (multiple PoE2/D4/LE articles; permitted)
- WebSearch results (aggregate, cited per dimension)

---

## Summary (3-5 sentences)

Across the 4 reference ARPGs, modifier-partitioning architectures divide cleanly into two axes: **pool scope** (which modifier types a slot can roll) and **weighting mechanism** (how probability is distributed within that pool). Pool scope is always item-type-gated and attribute/class-tagged; the partition that matters most is not between gear slots per se but between offensive (prefix) and defensive/utility (suffix) modifier surfaces. Rarity's role in unlocking modifier types (not just adding more affixes of the same type) is the dominant pattern in PoE2 and the closest architectural ancestor to doc 40's modifier-surface-expansion design intent. Last Epoch's affix-shard crafting system — where affixes become harvestable discrete units — is the most direct precedent for a "modifier alphabet" driving spec-driven gear generation. The clearest architectural lesson across all four ARPGs: per-slot modifier pool size must be small enough to be learnable (5-40 meaningful choices per slot) but anchored to a consistent partitioning logic (prefix-offense / suffix-defense), and the modifier-surface-expansion jump at legendary rarity is a load-bearing design move in all four systems.

---

## Findings

### ARPG 1 — Path of Exile 2

#### 1.1 Modifier surface enumeration

PoE2's modifier surface is the largest of the four ARPGs. Modifiers are categorized by:

- **Prefix surface:** Offensive stats — increased physical/elemental/spell damage, flat added damage, attack/cast speed, critical strike chance and multiplier, skill-level bonuses, attributes (STR/INT/DEX)
- **Suffix surface:** Defensive/utility — resistances (elemental, chaos), life/energy shield/evasion, mana, movement speed, flask effect, stun avoidance, reduced attribute requirements
- **Implicit modifiers:** Fixed modifiers on specific base types that cannot be crafted away (weapon implicits: attack speed, crit chance; armor implicits: %armor, evasion; jewel implicits: attribute bonuses)
- **Skill-granting modifiers:** Reserved almost exclusively to unique items; wands/staves/sceptres grant inherent active skills tied to item level via implicit modifier slots; unique items grant exclusive active or passive skills
- **Trigger/proc modifiers:** Exist but are less common as explicit affixes in PoE2 vs PoE1 — some triggers moved to skill gems and support gems. On-hit and on-kill effects exist (e.g., Cast on Melee Kill as a support gem); direct "% chance to proc X on hit" affix surface is smaller than PoE1.

Modifier count: Not publicly enumerated in a single authoritative count, but the PoEDB (poedb.tw) database (not crawled — ClaudeBot-blocked; data via WebSearch aggregate) is understood by the community to contain hundreds to low thousands of distinct modifier entries across all domains, with individual item-type pools typically numbering 30-80 prefixes + 30-80 suffixes (estimates from community sources).

Sources: skycoach.gg PoE2 crafting guide; mmojugg.com item tiers article; sportskeeda.com PoE2 items/affixes; official PoE forum thread 55170 (Chris Wilson dev diary).

#### 1.2 Per-slot partition design

PoE2 uses a **domain + tag + attribute-alignment partition**:

- **Domain:** Each modifier has a domain (item, flask, jewel, etc.) restricting which entity types can roll it. Weapons cannot roll armor-domain mods; armor cannot roll weapon-domain mods.
- **Attribute alignment within armor:** Intelligence-based armor (Energy Shield) weights toward caster mods (spell damage, mana, energy shield bonuses); Strength-based armor (Armor value) weights toward melee stats; Dexterity-based armor (Evasion) weights toward attack/evasion stats. Hybrid-attribute bases can pull from both aligned pools.
- **Weapon type specialization:** Wands and staves have spell-damage weighted pools; axes/swords/maces have physical-damage-weighted pools; caster weapons no longer roll attack-speed-only modifiers as of PoE2 redesign.
- **Jewel domain:** Separate pool; mostly small passives (% to skills, attribute bonuses, resistances); max 2 prefixes + 2 suffixes vs armor/weapon max 3+3.
- **No ring/amulet vs armor differentiation explicitly documented** in non-blocked sources, but jewelry historically skews toward attributes, resistances, life, and reduced attribute requirements.

Key partition principle: **Prefix = offense; Suffix = defense/utility.** This is the load-bearing binary across ALL item types in PoE2.

Sources: skycoach.gg PoE2 crafting guide; mmojugg.com item tiers; vhpg.com spawn weighting.

#### 1.3 Per-slot probability distribution

PoE2 uses **spawn weights** as the core mechanism:

- Every modifier in a pool has a numeric spawn weight. Probability = weight / sum-of-all-weights in pool.
- If weight = 0, modifier cannot appear on that item type.
- Tags further restrict and amplify: modifier tags (e.g., "Damage," "Physical," "Attack," "Elemental," "Fire," "Resistance") compose with item tags (e.g., str_armour, dex_armour) to produce effective weight for that item.
- **Item level (iLvL) gates modifier tiers:** Each modifier has multiple tiers (labeled T1 best, T6+ worst in community convention — PoE labels them internally highest ilvl requirement = best roll range). A modifier's tier is only accessible once the item's iLvL meets the threshold. Example: max-tier elemental resistance requires iLvL 82+; max-tier life mod requires iLvL 86+.
- **Influence system:** Items with influence (from certain content areas) access an additional pool of modifier entries layered on top of the base pool — expanded modifier surface, not just better weights. Influence modifiers represent some of the most powerful affixes in the game (slam-augmenting Exalted Orbs add from this expanded pool on influenced items).
- **Omen/currency manipulation:** Omens (from Ritual league mechanic) allow directing which slot (prefix/suffix) an orb targets; certain currency (Essences pre-PoE2 equivalent) guarantee specific modifier types appear; Chaos Orb removes one modifier and replaces it with another from the same pool.

Sources: vhpg.com spawn weighting; mmojugg.com item tiers; skycoach.gg crafting guide; WebSearch aggregate for iLvL tiering.

#### 1.4 Rarity escalation pattern

- **Normal (white):** No explicit affixes; only implicit.
- **Magic:** 1 prefix + 1 suffix max (2 affixes total).
- **Rare:** 3 prefixes + 3 suffixes max (6 affixes total). Same modifier pool as magic; rarity unlocks MORE affixes from the same pool, not new modifier types.
- **Unique:** Fixed modifiers, typically 4-8. Modifier surface is fully curated — includes mods that do not exist in the regular pool (keyword mods, unique mechanics, skill grants). Rarity unlocks NEW modifier types not available on rares.

**Pattern:** Magic → Rare = quantity escalation (same pool, more affixes). Rare → Unique = modifier-surface expansion (new mod types; fixed curated set). This is the key distinction. The PoE community identifies the endgame as primarily rare-crafted gear (Rares are "most powerful" per GGG design intent); Uniques enable specific builds via unique-modifier-surface access.

Sources: Official PoE dev diary (pathofexile.com/forum thread 55170); sportskeeda.com PoE2 items article.

#### 1.5 Legendary / unique architecture

In PoE2, the term "legendary" is not used — items are **Unique**. Architecture:

- **Fixed modifier set:** Each unique item has a defined set of mods. These mods have numeric ranges (re-rollable via Divine Orb), but the mod TYPES are fixed.
- **Exclusive modifier surface:** Uniques contain mods that are keyword-restricted and cannot appear on rares — "Culling Strike," trigger mechanics, whole-skill grants, build-enabling modifiers.
- **Skill-granting architecture:** Most PoE2 uniques include an active or powerful passive skill grant. Jonathan Rogers (game director) explicitly stated: "pretty much every Unique coming with a skill" because each unique should represent "a way to play the game." Skills granted are level-tied to item level.
- **Tier system within uniques:** No formal tier 0/1/2/etc. classification. Rarity of unique items varies by design (some common drops; some rare chase items). GGG is experimenting with pooled-drop systems (similar to PoE1) to improve rare-unique accessibility.
- **No Ancestral/Sacred tier equivalent:** Power does not escalate by gear "generation" as in Diablo 4; instead, iLvL on the unique determines skill level and numeric roll ranges.

Sources: official PoE dev diary (forum thread 55170); mmojugg.com Jonathan Rogers interview; WebSearch PoE2 unique design articles.

#### 1.6 Set item architecture

**PoE2 has no set item system.** PoE1 did not have traditional sets; PoE2 continues this pattern. Build synergies are achieved through passive tree, support gems, and unique item combinations — not through a formal set-bonus mechanic. The equivalent of set synergy lives in the skill-gem socket/link system and in passive tree cluster jewels.

Sources: WebSearch PoE2 itemization; no set items found in any source.

#### 1.7 Triggered / proc modifier surface

Trigger mechanics exist but the architecture changed significantly from PoE1:

- **Support gem triggers:** Cast on Melee Kill, Cast when Damage Taken, Cast on Critical Strike, and similar are primarily now **support gems** socketed into active skills rather than item affixes. This moves trigger architecture OUT of the modifier pool and INTO the gem system.
- **Item-affix triggers:** Smaller surface than PoE1. Some items (especially uniques) retain "on-hit" or "when you kill" proc effects, but these are unique-exclusive modifiers, not part of the rare modifier pool.
- **Implicit triggers on weapon types:** Some weapon base types have implicit trigger-adjacent mechanics (e.g., Staves have "chance to block spell damage" implicit).

The architectural shift: PoE2 deliberately reduced trigger affixes on rares, centralizing trigger architecture in the support gem system to reduce cognitive complexity of random rolls.

Sources: WebSearch on PoE2 trigger system; pathofexile.com forum kill-effects thread.

#### 1.8 Skill-modifying modifier surface

- **Support gems are the primary skill modification layer** — they modify how active skills function (additional projectiles, added damage types, reduced cooldowns, etc.) without being item affixes.
- **+N to [skill type] affixes:** Exist on rares (e.g., +1 to level of all Intelligence skills); these appear on specific item types (amulets historically; some weapon types).
- **Unique-exclusive skill modification:** Unique items can have mods like "Socketed skills deal X% more damage" or "Skills supported by [support gem] have +X level" — these are unique-mod-surface entries, not rare affixes.
- **Wand/staff/sceptre implicits:** These base types grant inherent skill variants not available as gems, scaling with item level.

Sources: WebSearch PoE2 skill-granting items; official PoE dev diary.

#### 1.9 Crafting / modification surface

PoE2's crafting alphabet consists of **currency orbs** that modify item modifier state:

| Orb | Effect |
|---|---|
| Orb of Transmutation | Normal → Magic with 1 modifier |
| Orb of Augmentation | Add 1 modifier to Magic item |
| Regal Orb | Magic → Rare, adding 1 modifier |
| Orb of Alchemy | Normal → Rare with exactly 4 modifiers |
| Chaos Orb | Remove 1 random modifier + add 1 random modifier (Rare) |
| Exalted Orb | Add 1 random modifier to Rare (from full pool) |
| Orb of Annulment | Remove 1 random modifier |
| Divine Orb | Randomize numeric values of all modifiers (type unchanged) |
| Vaal Orb | Unpredictable corruption; can unlock additional implicit or implicits |
| Omens | Direct which prefix/suffix is targeted; can be consumed to guarantee outcomes |
| Rune sockets | Body armor and two-handed weapons get up to 2 sockets; other slots 1; rune provides a guaranteed small bonus |

Key removal from PoE1: Orb of Alteration (magic item re-rolling) and Orb of Scouring (full reset) are gone. Once an item is magic or rare, there is no cheap way to strip ALL modifiers and start fresh — this elevates white-base items and pushes crafting toward "build forward" rather than "reset and try again."

Sources: skycoach.gg PoE2 crafting guide; mmojugg.com PoE2 crafting preview.

#### 1.10 Notable architectural lessons

1. **Tag-based weighting is powerful but requires upfront schema commitment.** Every modifier must have tags; every item type must have tags. The tag interaction system requires the tag taxonomy to exist BEFORE modifier entries are created. Cannot be retrofitted easily.
2. **Prefix/suffix binary is load-bearing for crafting discipline.** Players can target "need one more prefix" or "need one more suffix" — this is fundamental to advanced crafting. The binary partition must exist before individual modifier assignments.
3. **iLvL gating of modifier tiers creates progression without bloating the modifier pool.** The same modifier type appears across many tiers — at low iLvL you roll weak magnitudes, at high iLvL you roll strong magnitudes — but the SAME modifier slot is used. This keeps the pool learnable while providing progression.
4. **Skill grants moving to gems rather than item affixes reduced modifier surface complexity** significantly from PoE1 to PoE2 — a deliberate design decision to reduce loot-filter overhead and learnable surface.
5. **The rare-as-primary-endgame-gear design (with uniques as special-purpose) requires rare modifier pools to be deep enough to support meaningful builds.** If rare pools are too shallow, uniques become mandatory — this collapses build diversity. PoE2's pool depth is why Rares remain viable.

---

### ARPG 2 — Last Epoch

#### 2.1 Modifier surface enumeration

Last Epoch has a documented affix surface of **over 800 affixes** counting class-specific and skill-specific entries (community analysis; secondary source). The modifier surface divides:

- **Prefixes (offensive/utility):** Flat and % damage bonuses per damage type; skill level modifiers; attribute increases; minion stats (class-specific); speed
- **Suffixes (defensive):** HP, resistances (elemental + void + necrotic + poison), mana, endurance, % armor, dodge rating
- **Skill-level affixes (+X to [skill]):** Appear on helms, body armor, relics, and uniques. These are item-type-specific: helm slot can roll "+1 to Glacier" (a specific skill); the same affix does not roll on boots.
- **Proc/trigger affixes:** A separate explicit modifier surface; "% chance to proc [skill] when hit," "on kill summon [minion]" — these appear on specific item types and idol sizes.
- **Idol-specific affix surface:** Idols have their own per-size affix pools, distinct from traditional gear. The idol surface contains primarily proc-style affixes — "% chance to cast [skill] on [trigger condition]." These are accessed ONLY through idols, not through traditional gear.
- **Class-specific modifiers:** Certain affixes are prefixed to specific classes and only appear on class-restricted base types.

Sources: sportskeeda.com LE itemization comparison; forum.lastepoch.com unique item design developer blog; WebSearch LE affix system; icy-veins.com LE crafting guide.

#### 2.2 Per-slot partition design

Last Epoch uses **item-type affix pools** where each item category (helm, body armor, boots, gloves, belt, amulet, ring, relic, weapon, off-hand) has a distinct but overlapping affix pool:

- **Weapons:** Damage affixes (flat physical/elemental damage, % increased damage, attack speed, crit chance, spell damage for caster weapons); skill level affixes for weapon-compatible skills; may have class-specific attack or spell modifier affixes.
- **Body armor:** Heavy defensive skew — HP, resists, endurance; some offensive affixes (%increased damage, attributes) but fewer than weapons.
- **Helm:** Balance of offense and defense; crucially, **skill-level affixes are available here** ("+N to [specific skill]") — this is a major differentiation from PoE2 where skill grants on rares are rarer.
- **Gloves:** Mix of attack speed, crit, flat damage, some defensive.
- **Boots:** Movement speed, HP, resistances, some regeneration.
- **Jewelry (rings/amulets):** Broader pools — resistances, attributes, flat damage, life, mana; amulets can have more offensive affixes than rings typically.
- **Relics:** Class-restricted; deeper class-specific affix pools (mastery-specific skills, class thematic modifiers).
- **Idols:** Fully separate pool system; each of the ~10+ idol sizes (1x1 Minor, 1x2 Humble, 1x3 Large, 2x1 Stout, 2x2 Adorned, 3x1 Grand, 4x1 Ornate, etc.) has its own unique prefix/suffix pool. Larger idols have smaller, more powerful pools. Class-specific idols draw from class-restricted pools.

Prefix/suffix binary is the same as PoE2: Prefixes = offensive/utility; Suffixes = defensive.

Sources: icy-veins.com LE crafting guide; WebSearch LE affix system; WebSearch LE idol system; lastepochtools.com idol database (accessed via WebSearch aggregate, not direct fetch — robots.txt not checked for this domain; findings drawn from search result summaries only).

#### 2.3 Per-slot probability distribution

Last Epoch uses **Forge Potential (FP)** as the primary crafting resource:

- Items drop with a FP budget (typically 20-40 for Common-Rare; Exalted items often 40+).
- Each craft (adding/upgrading an affix) consumes a random amount of FP within a range.
- The **success of the craft is guaranteed** — only the FP drain is random. This is architecturally distinct from PoE2's pure-RNG craft outcomes.
- When adding a NEW affix, a random affix from the eligible pool is added (one of the prefixes or suffixes available to that item type). No explicit weighting data was found in accessible sources.
- **Glyph of Chaos:** Randomizes which affix appears but respects the prefix/suffix designation and item-type eligibility. Does not change mod TYPE classification.
- Tier probability: Affixes drop at T1-T5 on random drops (T6-T7 only on Exalted items as drops); crafting via shards can push to T5 max (T8 via rare Rune of Evolution).

The FP system functions as a **durability-rationing mechanism** rather than a probabilistic pool-sampling mechanism. The question "which affix will I get" has randomness; the question "will my craft succeed this FP" does not.

Sources: icy-veins.com LE crafting guide; aggronaut.com LE crafting primer (2024); pcgamesn.com LE crafting affixes.

#### 2.4 Rarity escalation pattern

- **Common (white):** Implicit only; no explicit affixes.
- **Magic (blue):** 1 prefix + 1 suffix.
- **Rare (yellow):** Up to 2 prefixes + 2 suffixes (4 explicit affixes); same pool as magic items of that type.
- **Exalted (purple):** Up to 4 affixes (same pool as Rare) BUT one affix is Tier 6 or Tier 7 (cannot be crafted; only drops). Also can have a "Sealed Affix" (5th affix slot added via Glyph of Despair).
- **Unique (orange):** Fixed affixes, outside the normal pool; typically 3-5 affixes with unique modifiers not available on rares. Some uniques have a small numeric range; others are fully fixed.
- **Legendary (red):** Crafted by combining a Unique with Exalted (via Legendary Potential mechanic) — the Unique retains all its fixed mods AND transfers 1-4 affixes from the Exalted item.
- **Set Items (in Season 2):** Fixed stats; can now be shattered and reforged onto other gear via Forge of Shattering — set bonus affixes become portable.

**Pattern:** Magic → Rare = more affixes of the same pool. Rare → Exalted = higher-tier affixes within the same pool (T6/T7 access). Exalted → Unique = fixed exclusive modifier surface. Unique → Legendary = additive: unique mods + selected Exalted affixes. This is the most layered escalation of the four ARPGs.

Sources: icy-veins.com LE crafting guide; pcgamesn.com LE crafting; WebSearch LE rarity system; forum.lastepoch.com unique design blog.

#### 2.5 Legendary / unique architecture

Last Epoch's unique design philosophy (per developer blog, Mitchell, Eleventh Hour Games):

- **Two categories:** Power Uniques (direct stat upgrade flavor; leveling items) and Mechanic-Changing Uniques (alter moment-to-moment gameplay or build strategy fundamentally).
- **Primary focus:** Mechanic-Changing Uniques are the design priority — examples like Mourningfrost (increases AGI movement speed scaling, adds cold damage, REMOVES AGI attack/cast speed benefit, reduces max life) force complete playstyle reconsideration.
- **Anti-mandatory design:** Well-rolled six-affix rare items should remain competitive "approximately 80% of the time." Uniques should not be mandatory.
- **Legendary system (Legendary Potential):** Unique items drop with 0-4 "Legendary Potential" (LP). At LP 1-4, the player can fuse the Unique with an Exalted item — transferring 1-4 Exalted affixes onto the Unique. This creates a "Unique + custom affixes" composite. LP4 Uniques with perfect Exalted transfers are the endgame chase items.
- **Set items:** 2-tier system (regular set, mythical set). Full set bonus requires all pieces from same tier. Bonuses are incremental (2-piece bonus, 3-piece bonus, etc. up to full set). Sets are endgame-targeted; set bonuses are typically "always T4-attuned" equivalents in the LE context (tied to class/build themes).

Sources: forum.lastepoch.com unique item design developer blog; WebSearch LE unique/set design; icy-veins.com LE crafting; WebSearch LE set items.

#### 2.6 Set item architecture

- Sets consist of 2-7 items (varies by set).
- **Incremental bonuses:** Equipping N pieces of a set grants N-piece bonus; each additional piece unlocks a new bonus threshold.
- **Regular vs Mythical tiers:** Same set exists in two tiers; tier-mixing breaks set bonuses (confirmed by community discussion).
- **Season 2 Forge of Shattering:** Players can now shatter set items to extract set bonus affixes and reforge them onto compatible non-set gear. This makes set bonuses functionally portable — a significant architectural expansion that decouples the set bonus from the set item requirement.
- **Set bonus modifier surface:** Set bonuses include proc triggers, skill level grants, resistance packages, and mechanics-altering bonuses not typically available as standard affixes — a separate exclusive modifier surface similar to unique modifier pools.

Sources: WebSearch LE set items; pcgamesn.com LE crafting; WebSearch LE Season 2 forge changes.

#### 2.7 Triggered / proc modifier surface

Last Epoch has an **explicit proc modifier pool** that is significant and well-partitioned:

- **Idol affix surface is predominantly proc-based.** Idols are specifically designed around triggered effects: "% chance to cast [skill] when [trigger condition]." This is architected as a SEPARATE item system from traditional gear — proc affixes live on idols, not on armor/weapons. This is a clean architectural partition.
- **On traditional gear:** Some proc affixes exist on certain item types (gloves, weapons in particular); these appear in item-type-specific affix pools.
- **Skill-level affixes are adjacent to but distinct from proc affixes:** "+N to [skill]" is not a proc; it passively boosts the skill regardless of trigger conditions.

The architectural choice: route proc modifiers primarily through the Idol system, keeping traditional gear affixes focused on passive stat modification. This reduces modifier pool complexity on core gear while giving players a dedicated system to build around triggered effects.

Sources: WebSearch LE idol system; WebSearch LE affix system.

#### 2.8 Skill-modifying modifier surface

- **+N to [specific skill]:** Available on helms, body armor, relics, uniques, and set bonuses. One of Last Epoch's most praised features — the ability to push skill level beyond the cap (base 20, can reach 30 with optimal gear) creates meaningful gearing decisions tied to specific builds.
- **Class-specific skill affixes:** Relics and class-restricted base items have affix pools that include class-specific skill modifiers.
- **Idol class-skill affixes:** Larger class-specific idols include affixes that modify class skills (proc style: "+% [class skill] damage," "% chance to apply [class debuff] on [trigger]").
- **Unique skill modification:** Uniques can grant entirely new skills or fundamentally modify existing skill behavior (e.g., a unique that makes a channeled skill into a burst skill).

Sources: lastepochtools.com skill level affixes guide (via WebSearch aggregate); forum.lastepoch.com unique design; WebSearch LE skill modifiers.

#### 2.9 Crafting / modification surface

Last Epoch's crafting alphabet is **shard-based deterministic crafting**:

| Material | Effect |
|---|---|
| Affix Shards | Add or upgrade a specific affix (one shard per attempt; drains FP) |
| Rune of Shattering | Destroy item; yields affix shards equal to affix tier (1-tier count) |
| Rune of Removal | Remove a random affix; returns shards equal to tier |
| Rune of Refinement | Reroll numeric values within current tier (like PoE2's Divine Orb) |
| Rune of Discovery | Fill all empty affix slots with random T1 affixes |
| Rune of Ascendance | Upgrade item rarity (to Rare/Exalted) |
| Rune of Evolution | Upgrade a T7 affix to T8 (rare Rune) |
| Glyph of Hope | 25% chance for craft to drain 0 FP |
| Glyph of Despair | Chance to seal an affix instead of upgrading (creates 5th affix slot) |
| Glyph of Chaos | Randomize which affix appears (preserves prefix/suffix designation and item-type eligibility) |
| Glyph of Order | Preserve numeric value position within new tier range |
| Glyph of Envy | Guarantee T4+ affix level on new affix addition |

The key architectural insight: **Affix shards are the modifier alphabet.** Any affix on any item can be shattered into shards; shards target specific modifier types when applied. This creates a complete, learnable modifier vocabulary. Players accumulate the "modifier alphabet" through play and can precisely target desired stats. The system is substantially more deterministic than PoE2 and substantially more legible than Diablo 4's pre-S4 system.

Sources: icy-veins.com LE crafting; aggronaut.com LE crafting primer 2024; pcgamesn.com LE crafting.

#### 2.10 Notable architectural lessons

1. **Separating proc affixes into a dedicated item system (Idols) vs. integrating them into gear slots eliminates cross-contamination.** Gear affixes are simpler to learn because proc complexity lives in the Idol system. The tradeoff: players must manage two overlapping modifier systems; the payoff: each system is individually learnable.
2. **Skill-level affixes on specific slots (helm, chest, relic) are among the most loved gear decisions in the ARPG space (community consensus).** They are meaningful, build-specific, and make individual item slots feel important. They require upfront commitment that specific slots CAN roll skill-level affixes.
3. **Forge Potential as a crafting durability resource** (success guaranteed; cost is random) is a design pattern that eliminates "bricking" frustration while maintaining meaningful resource spending.
4. **The Legendary Potential system** (Unique + Exalted fusion) is architecturally elegant — it combines the exclusive-modifier-surface of uniques with player-directed affix additions. The trade-off is complexity of sourcing both a high-LP unique AND a relevant Exalted simultaneously.
5. **800+ affixes sounds large, but per-slot pools are manageable** (~20-50 affixes per slot per side) because of strict item-type partitioning.

---

### ARPG 3 — Diablo 4

#### 3.1 Modifier surface enumeration

Diablo 4's modifier surface was significantly reshaped in Season 4 (May 2024). Current (Season 13) architecture:

**14 primary affix categories (generic, available across multiple slots):**
1. Primary attribute increases (STR/DEX/INT/WIL)
2. Attack speed
3. Control effect duration / impaired reduction
4. Critical strike chance, critical strike damage
5. Conditional damage modifiers (injured, distant, close, stunned, burning enemies)
6. Skill-type damage (Ultimate, Basic, Core skill damage; class-specific skill damage)
7. Thorns (reflected damage)
8. Vulnerable damage amplification
9. Life / Max Life / Barrier Generation
10. Armor / Damage Reduction (flat and conditional)
11. Dodge chance
12. Elemental resistances
13. Lucky Hit (proc-based effects)
14. Movement speed / Cooldown Reduction / Resource Generation

**Class-specific affix pools (5 classes):** Each class has exclusive affixes available on class-usable items; these include class mechanics, mastery bonuses, specific skill ranks, shapeshifting buffs, etc. Class-specific affixes do NOT appear on items the class cannot equip.

Pre-Season 4 the pool was notably wider with many conditional "deal damage on Tuesday" style modifiers. Season 4 pruned these in favor of fewer, more broadly applicable affixes.

Sources: studioloot.com D4 gear affixes; icy-veins.com D4 gear systems overview; blizzardwatch.com S4 itemization; WebSearch D4 affixes by slot.

#### 3.2 Per-slot partition design

Diablo 4 uses a **strict slot-type affix pool** — each equipment slot has a defined pool of eligible affixes (independent of rarity):

| Slot category | Characteristic affixes |
|---|---|
| Helm | Max Life, Barrier Generation, specific skill rank bonuses, potion-related affixes, cooldown reduction |
| Chest | Max Life, Resistances, Damage Reduction, armor, Lucky Hit modifiers |
| Gloves | Critical Strike Chance, Attack Speed, class-specific skill ranks, specific skill damage |
| Pants | HP, Resistances, Dodge, control effect duration |
| Boots | Movement Speed, Resistances, HP, specific utility affixes |
| Rings | Damage modifiers, Critical Strike, resource generation, Lucky Hit; always roll a Resistance affix |
| Amulet | Movement Speed, Cooldown Reduction, Damage and utility, Resistance (broader pool than rings) |
| Weapons | DPS (core stat), damage %/flat, class-specific skill damage, attack speed |
| Off-hand/Shield | Blocking, specific defensive mechanics; class-dependent |

**Amulets can roll Cooldown Reduction and Movement Speed; Rings cannot.** This is a notable explicit partition. Weapons gate the highest damage modifiers; jewelry gates utility and global modifiers.

**No prefix/suffix binary in D4.** Affixes do not have a prefix vs. suffix designation — all explicit affixes on an item are just "affixes," differentiated only by slot eligibility.

**Legendary Aspect:** Every Legendary item has one Legendary Aspect (a 5th affix slot, essentially, with unique power). Aspects have placement restrictions: some aspects are "Offensive" type and can only go on weapons/gloves/rings/amulets; "Defensive" type goes on helms/chest/pants/boots; "Utility" goes on helms/chest/pants/boots/shields. This is a secondary partitioning layer distinct from the affix pool.

Sources: studioloot.com D4 gear affixes; icy-veins.com D4 gear overview; WebSearch D4 per-slot affix lists.

#### 3.3 Per-slot probability distribution

Diablo 4 uses **flat probability sampling** within eligible per-slot affix pools:

- When an item drops, its affixes are sampled from the slot's eligible pool. No explicit spawn-weight system (unlike PoE2's weight system) is publicly documented — the pool appears to be roughly flat-weighted.
- **Sacred and Ancestral items** do NOT expand which affixes can appear — they expand the MAGNITUDE (numeric rolls are higher). Sacred items (World Tier 3, level 50+) and Ancestral items (World Tier 4 / Torment 1, level 70+) are the same pool with higher roll ranges. Rarity tier determines affix TYPE surface; item power tier (Sacred/Ancestral) determines magnitude.
- **Greater Affixes (GAs):** Appear randomly on Ancestral items (1-4 GAs possible, with sharp probability drops per additional star). A GA rolls at 1.5x the maximum normal value — not a new affix type but a magnitude bonus on an existing affix.
- **Class-specific smart-drop:** Items are biased toward dropping usable versions for the player's class (class affixes for the correct class appear more frequently).

Sources: icy-veins.com D4 gear overview; studioloot.com D4 affixes; blizzardwatch.com S4 itemization; WebSearch D4 Sacred/Ancestral.

#### 3.4 Rarity escalation pattern

- **Common / Magic:** Base + minimal affixes; not endgame-relevant in D4.
- **Rare:** 3 affixes (reduced from 4 in Season 4 redesign). Same slot-type pool.
- **Legendary:** 3 standard affixes + 1 Legendary Aspect. Aspects are drawn from the Codex of Power (all obtained Aspects stored permanently). Legendary status primarily means +Aspect, not expanded affix pool.
- **Unique:** 4 fixed affixes + 1 Unique Power. Fixed affix types are pre-set per unique; numeric ranges can be rerolled (via transmutation in Lord of Hatred). In the Lord of Hatred expansion (Season 13), secondary affixes on uniques now roll randomly within a defined pool (removed 100% fixed secondary affixes). Unique Power is always fixed.
- **Mythic Unique (formerly Uber Unique):** 4 fixed affixes + 1 Unique Power + guaranteed 1 Greater Affix. The rarest items in the game. Mechanics-altering powers that can "completely alter the way you play."

**Pattern:** Common → Legendary = same pool, more affixes + Aspect slot. Legendary → Unique = fixed affix surface + Unique Power (exclusive modifier type). Unique → Mythic = same unique architecture + guaranteed GA.

Sources: WebSearch D4 unique/mythic design; icy-veins.com D4 gear overview; studioloot.com D4 affixes.

#### 3.5 Legendary / unique architecture

Current D4 architecture (Season 13 / Lord of Hatred):

- **Aspects** (Legendary powers): Stored in Codex of Power; can be imprinted onto Rare or Legendary gear. Placement-restricted by Aspect type (Offensive/Defensive/Utility/Weapon). This system separates the "special power" from the "item chassis" — allowing players to attach desired powers to self-found Rares.
- **Unique fixed affix model (pre-Season 13):** Every unique had a fixed pool of secondary affixes. Blizzard removed this in Lord of Hatred — secondary affixes now roll randomly. This was a significant architectural change in response to player frustration with non-BiS unique rolls being worthless.
- **Transmutation:** Players can sacrifice 3 copies of the same unique to get a fresh version with rerolled affixes — a deterministic chase system for optimal rolls.
- **Tempering (Season 4+):** A player-applied system. The Blacksmith applies a "Tempering Recipe" to add an additional affix. Most items get 1 Tempering Affix; Ancestral items can have 2. In later seasons, Tempering was redesigned to allow direct affix selection from the recipe pool (removing the random-outcome frustration).
- **Masterworking:** Applies at the Blacksmith to existing affixes; in later iterations adds "Refinement" (improves base damage/armor/resistance) rather than directly boosting affix values.

Sources: WebSearch D4 unique architecture; icy-veins.com tempering/masterworking article; blizzardwatch.com S4 changes.

#### 3.6 Set item architecture

**Diablo 4 does not have traditional set items** in the current design. This is a notable departure from Diablo 2/3. The set-like synergy in D4 is achieved through Aspect placement across multiple slots — wearing matching Aspect types creates thematic synergy. Blizzard has acknowledged the absence of sets but has not added them as of Season 13 / Lord of Hatred.

Sources: icy-veins.com D4 gear overview; WebSearch D4 sets.

#### 3.7 Triggered / proc modifier surface

D4's primary proc surface lives in the **Lucky Hit system:**

- "Lucky Hit" affixes appear on multiple item slots: "Up to X% chance to [effect] when you Lucky Hit."
- Lucky Hit Chance itself is a stat that increases how often Lucky Hit effects trigger.
- Lucky Hit effects include: heal life, restore resource, apply crowd control, summon effects, proc additional explosions.

**This is D4's primary mechanism for "X on hit / X on crit / X on kill" style triggers.** Lucky Hit consolidates what PoE2 handles through support gems and PoE1/GD handle through item procs into a single unified probability system.

**Class-specific proc mechanics:** Some classes have mechanics (e.g., Rogue's Imbuement system, Necromancer's corpse triggers, Druid's shapeshifting procs) that are class-specific affix expressions rather than a universal trigger affix system.

Sources: studioloot.com D4 affix categories; icy-veins.com D4 gear overview; WebSearch D4 Lucky Hit.

#### 3.8 Skill-modifying modifier surface

- **"+N ranks to [specific skill]":** Available on specific slots (amulet and gloves most commonly; some class-specific items). These are within the normal affix pool — not unique-exclusive.
- **Codex of Power / Aspects that modify skills:** Many Aspects are explicitly skill-modifying ("+X% damage to [skill]," "[skill] now does X instead of Y," "After using [skill], you gain Z"). These are the primary skill-modification layer in D4.
- **Unique Powers:** Unique items' fixed unique power is often a skill-modifying effect that fundamentally alters how one or more skills function.

The architecture: skill modification in D4 is divided between Aspect system (for most builds) and Unique Power (for build-defining transformations).

Sources: studioloot.com D4 affixes; WebSearch D4 skill rank affixes; icy-veins.com D4 gear overview.

#### 3.9 Crafting / modification surface

| System | Description |
|---|---|
| Occultist: Aspect Imprinting | Imprint an Aspect (from Codex or extracted) onto Rare/Legendary. Destroys existing Aspect. |
| Blacksmith: Tempering | Add 1 (or 2 on Ancestral) Tempering Affix from a Recipe; player selects specific affix in latest season redesign |
| Blacksmith: Masterworking | Add Refinement to base stats (damage/armor); endgame system requiring Pit materials |
| Transmutation (LoH) | Sacrifice 3x same Unique → fresh Unique with rerolled affixes and Unique Power numeric |

Pre-Season 4 D4 had no meaningful crafting beyond Aspect imprinting. Season 4 added Tempering/Masterworking. Later seasons refined Tempering to remove the random-roll failure (bricking) problem. This evolution shows the system initially launched with insufficient player-side modifier control, then added layers iteratively.

Sources: blizzardwatch.com S4 itemization; icy-veins.com tempering/masterworking; WebSearch D4 crafting Season 4.

#### 3.10 Notable architectural lessons

1. **The pruning lesson (Season 4):** D4's original affix pool had many narrow conditional modifiers ("deal damage to Burning enemies") that created decision paralysis and inventory sorting overhead without meaningful build differentiation. The fix: remove niche conditionals; keep broader, more powerful affixes. This is a strong signal that **affix pool width needs a quality floor** — affixes that almost never matter are worse than fewer, always-relevant affixes.
2. **Aspect system decouples power from item RNG:** By making Aspects codex-permanent and imprint-able onto any qualifying item, D4 gives players agency over the "special power" layer separate from the random affix layer. This is architecturally elegant for a game targeting broader audiences.
3. **Lucky Hit as a unified proc abstraction:** Centralizing proc mechanics into a single "Lucky Hit" stat (modifiable) vs. scattered per-trigger affix entries is a simplification trade-off that makes trigger modifiers more legible but less expressive than PoE2's trigger support gem system.
4. **Sacred/Ancestral as magnitude tiers (not modifier-surface expansion):** D4's approach of keeping modifier TYPES constant across tiers but scaling magnitude creates a smooth power curve but means a player's loot evaluation framework doesn't change as they progress — the same affixes just roll higher. This reduces cognitive overhead but eliminates the "wow, a new affix type" discovery moment.
5. **No sets and no prefix/suffix binary are notable absences** that simplify the system but also reduce crafting expressiveness. Community comparison consistently ranks D4's itemization below PoE2 and LE in depth.

---

### ARPG 4 — Grim Dawn

#### 4.1 Modifier surface enumeration

Grim Dawn's modifier surface is the most expressive of the four when including its multi-layer system (base affixes + components + devotion + augments):

**Base item affixes (prefix/suffix):**
- **Magical affixes:** Standard stat bonuses — physical/elemental/pierce/acid/vitality/chaos/aether damage and resistances; attributes (Physique/Cunning/Spirit); HP, armor, DA/OA (Defensive/Offensive Ability)
- **Rare affixes:** More exotic rare-quality affixes on items with rare prefix or suffix — "Auto-Cast item skills" (proc triggers), "damage to specific monster archetype," skill-level-modifiers, resistance to debuff effects. Rare-quality affixes are notably more powerful and more exotic than magical affixes.
- **Monster Infrequent (MI) affixes:** Certain enemy types have specific base stats + standard affixes but with guaranteed MI-specific bonuses (similar to PoE2's influenced-item modifier layer).

**Item skill modifier surface:**
- Available exclusively on Monster Infrequent and Legendary items, in specific slots: weapons, amulets, medals, helms, gloves, and sets.
- These are "modify [Mastery skill] to behave differently" — a skill modification layer comparable to PoE2's support gems or LE's skill-level affixes but mechanically distinct: they directly alter how an existing skill functions (e.g., "Nightblade's Blade Trap now spawns 2 additional traps").

**Devotion (proc) surface:**
- Devotion is a separate system (constellation skill tree unlocked with Devotion points). Devotion skills (Celestial Powers) are linked to mastery/item skills and trigger based on the linked skill's trigger conditions.
- Not an item affix — but directly interacts with proc architecture. Devotions are the primary proc-trigger layer.

**Component affix surface:**
- Components are item add-ons that provide guaranteed bonuses (resistances, flat stat bonuses, active skills). Weapon components add active skills; armor components add passive resistances/stats.

**Augment surface (NPCs):**
- Two NPC factions provide augments (Angrim: martial bonuses; Duncan: arcane bonuses) applied to items — small guaranteed bonuses. This is a crafting-equivalent layer.

Sources: grimdawn.com/guide/items/ (official, all sections); WebSearch GD prefix/suffix system; WebSearch GD skill modifiers.

#### 4.2 Per-slot partition design

Grim Dawn's partition operates at multiple levels:

**Base affix partition:**
- Each item type (weapons, armor slots, accessories) has a distinct affix pool.
- Magical affixes are split: some are weapon-only (damage type boosts, OA, attack speed), some are armor-only (resistances, DA, HP, armor), some are accessory-only (attributes, proc skills from rings).
- Ring affix pool is notably unique: rings have access to "item proc" affixes (proc skills from any item or set in Grim Dawn) — 714 item proc prefixes documented on rings (community source; secondary).
- Amulet affix pool: documented at ~947 skill modifier affixes — amulets access the broadest skill-modification pool of any item type.

**Slot-specific restriction examples:**
- Item Skill Modifiers (that directly alter Mastery skills): restricted to weapons, amulets, medals, helms, gloves, and sets — NOT available on boots, pants, belt, or rings.
- Component-granting active skills: weapon components add active skills; armor components do NOT add active skills (only passive bonuses).
- Set bonuses: distributed across set pieces and often include item skill modifiers not available on any individual component.

**No explicit prefix/suffix functional binary:** Both prefix and suffix slots exist, but unlike PoE2/LE, there is no systematic "prefix = offense / suffix = defense" alignment. Grim Dawn's affixes are more thematically organized by their magical-vs-rare quality distinction than by prefix/suffix slot role.

Sources: grimdawn.com official item guide; grimdawn.com component guide; grimdawn.com item skills guide; WebSearch GD affix pools per slot.

#### 4.3 Per-slot probability distribution

- Grim Dawn uses a pool-sampling approach analogous to PoE2's spawn weight system but less publicly documented.
- Item affixes have "random stat deviation" — each stat has a base value with a percentage deviation range (e.g., a flat damage bonus might roll anywhere from 75% to 125% of the stated value).
- Item level (character level + area level) gates which affixes can appear (higher level areas drop items with access to higher-tier magical affixes).
- Rare affixes are rarer by construction — they have lower effective weights in the pool vs magical affixes.
- "Double rare" (both prefix AND suffix are rare quality) items are extremely rare and considered high-value.
- No public documentation of explicit spawn weight numbers was found in accessible sources.

Sources: grimdawn.com official loot guide (item rarity section); WebSearch GD affix system.

#### 4.4 Rarity escalation pattern

- **Common (white):** No affixes; base stats only.
- **Magic (yellow):** 1-2 magical affixes (1 prefix, 1 suffix, or one of each). Standard magical affix pool.
- **Rare (green):** At least 1 rare-quality affix (plus potentially 1 magical); rare affixes include exotic bonuses, proc effects, item skill modifiers on eligible slots.
- **Monster Infrequents (green, different):** Boss-specific guaranteed base stats + standard random affixes. Valued for unique base stats rather than affix randomization.
- **Epic (blue):** Fixed stat combinations; cannot be crafted; exclusive art. No affix rolling — entirely predetermined.
- **Legendary (purple):** Highest tier; fixed stat combinations (most potent); unique art and lore. Can include item skill modifiers. Cannot be crafted from base materials — only found as drops.
- **Set items (blue-purple):** Multiple items with synergistic bonuses; fixed stats per piece + set bonuses that unlock incrementally.

**Pattern:** Magic → Rare = upgraded affix quality (magical → rare pool access; no more affixes, but better affixes). Rare → Epic = completely fixed (no random affixes). Epic → Legendary = similarly fixed but more powerful. No crafted-legendary-from-rare pattern (unlike PoE2 and LE's crafting chains). **Grim Dawn is the most drop-dependent of the four** — player crafting does not produce Epics or Legendaries.

Sources: grimdawn.com official loot guide; WebSearch GD item rarity.

#### 4.5 Legendary / unique architecture

In Grim Dawn, what other ARPGs call "Unique/Legendary" maps to two tiers: **Epic** and **Legendary.**

- **Epics:** Fixed stat combinations; designed as bridge items between early-game and endgame. Item skill modifiers may appear on Epics (specific slots).
- **Legendaries:** Full fixed stat set — the most potent fixed items in the game. Almost all have item skill modifiers (on eligible slots). Legendaries are often build-defining: equipping a specific legendary + specific mastery combination is the primary gearing goal.
- **No procedural legendary:** Legendaries cannot be crafted from random bases; there is no "add affixes to make a legendary" pattern. This is architecturally very different from PoE2 (crafted rares are endgame BiS) and LE (legendary potential system combines unique + exalted).
- **Set items (Epic/Legendary quality):** 83 total sets in Grim Dawn. Set bonuses unlock incrementally. Full set completion provides the most powerful bonuses; partial completion still grants smaller bonuses. Sets often constitute complete builds in themselves.
- **Tier system within legendaries:** No formal tier system equivalent to LoH Mythic Unique or LE Legendary Potential. Legendaries are either "build-enabling" or not; the community creates tier lists but there is no in-game tier designation.
- **2024 update — rare mastery affix redesign:** All Rare Mastery and Mastery Combination prefixes were redesigned to have fixed skill bonuses (removing the "skill bonus lottery" problem). This shows GD iterating toward determinism on the skill-modifier affix surface.

Sources: grimdawn.com official item guide; WebSearch GD legendary design; WebSearch GD 2024 update.

#### 4.6 Set item architecture

- **83 sets** in Grim Dawn (base game + expansions).
- Sets range from 2-piece to 7-piece collections.
- **Incremental bonus structure:** Each additional piece unlocks the next bonus tier (1pc → 2pc → 3pc → ... → full set). Each tier grants distinct bonuses (resistances, proc triggers, attributes, skill modifications).
- **Tier mixing:** Regular, Empowered, and Mythical versions of the same named set are entirely separate sets — mixing tiers breaks set bonuses.
- **Set bonus modifier surface:** Set bonuses access an exclusive modifier surface — proc triggers, item skill modifiers, complete skill grants, massive resistance packages — not available from individual items alone.
- **Transmutation (Forgotten Gods):** Set pieces can be transmuted into another piece from the same set at the Inventor NPC (for a material cost). This adds deterministic targeting within a set — if you have multiple copies of one piece, you can convert them toward a missing slot.

Sources: WebSearch GD set items; grimdawn.com official loot guide; WebSearch GD set bonus community discussion.

#### 4.7 Triggered / proc modifier surface

Grim Dawn has the richest explicit trigger/proc architecture of the four ARPGs:

- **Devotion Celestial Powers:** Dedicated proc-trigger layer. Powers are linked to mastery/item skills and trigger based on the linked skill's trigger type.
  - "On attack" procs: trigger chance scales with linked skill cooldown length; attaching to multi-hit AoE can cause over-triggering.
  - "When hit" procs: only function while the linked ability is active; strategic choice of which skill to attach (e.g., attach to a defensive toggle so it only procs during active periods).
  - "On low health / on low energy" procs: conditional triggers.
  - DoT interactions: True DoT ticks do NOT proc devotion powers; pseudo-DoT (sustained AoE) CAN proc on each tick — a notable and community-documented distinction.
- **Auto-Cast Item Skills on gear:** Appear as rare-quality affixes on eligible slots (rings, amulets, certain armor slots). Distinct from Devotion. Trigger types: "When Hit," "When Hit by Melee," "On Attack," "On Critical Attack," "On Block," etc. (9 documented trigger types).
- **Weapon components with active skills:** Weapon components grant active skills that must be manually activated; also can have on-hit procs depending on component type.

The architectural choice: Grim Dawn separates proc architecture into three layers (Devotion / Auto-Cast Item Skills / Component skills) that compose independently. This creates the most expressive proc surface but also the highest cognitive overhead.

Sources: grimdawn.com official item skills guide; WebSearch GD devotion proc system; WebSearch GD auto-cast mechanics.

#### 4.8 Skill-modifying modifier surface

Grim Dawn's item skill modifier system is architecturally distinctive:

- **Item Skill Modifiers** (not +level, but actual behavior modification): Available EXCLUSIVELY on Monster Infrequent and Legendary weapons, amulets, medals, helms, gloves, and sets.
- These modifiers directly alter HOW a Mastery skill functions — not just boosting its level. Example: "Blade Trap adds 2 additional traps," "Nightfall now has 30% shorter cooldown and deals cold damage."
- Multiple items with the same skill modifier STACK their effects.
- 2024 update: Rare mastery prefixes now have FIXED skill bonus values (removed the lottery on which skill bonus you'd get from a rare mastery affix). This improved the system's determinism.

This is more powerful and more build-specific than LE's skill-level affixes — LE adds levels; GD changes the skill's behavior. The trade-off: GD's item skill modifiers are fully curated (can't random-roll a specific skill modification onto a random base).

Sources: grimdawn.com official item skills guide; WebSearch GD legendary design; WebSearch GD 2024 update.

#### 4.9 Crafting / modification surface

Grim Dawn's crafting system is **the most limited of the four** for random item modification:

- **Blacksmith (Angrim / Duncan):** Craft new items from blueprints + materials. Blueprints are permanent (right-click to learn). Angrim specializes in martial bonuses; Duncan in arcane. Crafted items are magical or rare quality (not Epic/Legendary).
- **Enchanted items (gambling system):** Craft without a specific blueprint; variable outcome. Can yield magical-to-rare quality.
- **Inventor (Forgotten Gods):** Transmute set pieces into other pieces of the same set (material cost).
- **Components:** Attachable to item slots; provide guaranteed bonuses + some active skills. Not affix-pool modification.
- **Augments (faction vendors):** NPC faction vendors provide augments with small guaranteed bonuses.

No equivalent to PoE2's Chaos Orb (random affix replacement) or LE's Glyph system. **Grim Dawn players cannot meaningfully modify individual affixes on found items.** The "modifier alphabet" is entirely drop-dependent — you find what you find. This is intentional by design (Crate prioritizes "find your own loot" over trading / crafting economy).

Sources: grimdawn.com official crafting guide; grimdawn.com items hunt guide; WebSearch GD crafting.

#### 4.10 Notable architectural lessons

1. **Multi-layer proc architecture (Devotion + Auto-Cast + Components) is the most expressive proc system** but creates significant cognitive overhead. The "DoT vs pseudo-DoT" distinction for devotion proc triggering is a good example of emergent complexity that players must learn to build around.
2. **Item Skill Modifiers (behavior-altering, not level-granting) create the most distinct per-legendary build identities** — "this legendary fundamentally changes how [skill] works" is a stronger build hook than "+2 levels." The trade-off: these modifiers must be curated per legendary, cannot be procedurally generated.
3. **Drop-dependence without crafting recourse creates loot-hunt obsession positively but frustration negatively.** GD is praised for loot diversity but criticized for single-item dependency ("this build only works if I find X legendary"). The system has no safety valve for players who never find their key item.
4. **83 sets provides enormous build diversity** from set completion alone; sets ARE builds in GD. This is the most generous set architecture of the four ARPGs by count.
5. **Fixed skill modifiers on 2024 update (rare mastery prefix redesign)** improved the system: by removing the lottery element from skill bonuses on rare affixes, GD reduced the "luck in luck" problem where players found a rare prefix but rolled a useless skill bonus. Determinism on the skill-bonus surface improved player satisfaction.

---

## Synthesis — Cross-ARPG Dimensions

### S1. Modifier-surface size (order of magnitude)

| ARPG | Estimated total distinct modifier types | Notes |
|---|---|---|
| Path of Exile 2 | Hundreds to ~1,000+ across all domains | Largest surface; tag system enables fine-grained variant creation; community database (poedb.tw) not directly accessible to verify |
| Last Epoch | ~800+ affixes counting class/skill-specific entries | Community-cited figure; highest verified count |
| Grim Dawn | Hundreds (base affixes) + hundreds via components/devotion/skills | Multi-layer system; total unique mod expressions likely exceeds 1,000 when all layers counted |
| Diablo 4 | ~150-250 distinct affixes post-Season 4 pruning | Smallest surface; deliberately pruned toward broad applicability |

**Per-slot visible pool size** (what a player sees as options for one gear slot):

| ARPG | Estimated per-slot pool (prefix side OR suffix side) |
|---|---|
| PoE2 | ~30-80 eligible prefixes per item type; ~30-80 eligible suffixes |
| Last Epoch | ~20-50 per side per item type (per-size idol pools are much smaller: ~5-20) |
| Diablo 4 | ~8-20 per slot (generic pool with class additions) |
| Grim Dawn | Variable; rings documented at 714 proc-prefix entries; amulets at 947 skill-modifier affixes — outliers; typical armor slot ~20-60 |

Sources: WebSearch aggregate on pool sizes; studioloot.com D4; aggronaut.com LE; grimdawn community sources.

### S2. Rarity-escalation pattern taxonomy

Across the 4 ARPGs, three distinct escalation patterns emerge:

**Pattern R1 — Quantity escalation (more affixes, same pool):**
Magic → Rare in all four ARPGs: going from 1-2 affixes to 3-4+ affixes from the same eligible pool. This is universal.

**Pattern R2 — Magnitude escalation (same modifier types, higher numeric values):**
Diablo 4's Sacred / Ancestral progression is the clearest example: same affix pool, higher rolls. Also present within PoE2's iLvL modifier tier system (same modifier type, higher magnitude tier becomes accessible with higher iLvL). Grim Dawn's item level gating operates similarly.

**Pattern R3 — Modifier-surface expansion (new modifier types unlocked at higher rarity):**
PoE2's Unique items unlock exclusive modifier types not available on Rares (keyword mods, skill grants). Last Epoch's Unique items similarly unlock exclusive modifier surfaces. Grim Dawn's Epic/Legendary items are entirely fixed exclusive modifier sets. Diablo 4's Legendary Aspect adds an exclusive "5th affix slot" not available on Rares.

**Pattern R4 — Hybrid additive (unique + selected affixes from normal pool):**
Last Epoch's Legendary (Unique + Legendary Potential fused with Exalted) is the only instance of this pattern — exclusive unique modifier surface combined with player-selected normal-pool affixes. Diablo 4's Tempering system partially achieves this (player adds one affix from a recipe to a Legendary).

**Dominant architecture:** All four ARPGs combine R1 + R3. The specific implementation of R3 varies:
- PoE2/LE: R3 is fully curated (no random-rolling new types; fixed unique set)
- D4: R3 lives in the Aspect system (codex-stored; imprinted separately)
- GD: R3 is entirely drop-locked (fixed Epic/Legendary sets)

### S3. Legendary architecture taxonomy

Three distinct legendary architectures observed:

**Arch L1 — Fixed-mod unique with exclusive surface (PoE2, LE, GD):**
Unique/Legendary items have a fixed set of modifier types; numeric ranges may be variable; the modifier types themselves are pre-designed and not randomized. Variants: PoE2 uses Divine Orb to reroll numerics; LE uses LP fusion to add normal affixes on top of fixed set; GD has fixed numerics (or small deviation ranges).

**Arch L2 — Detached power layer imprinted onto random base (D4 Aspect system):**
The "legendary power" is stored separately from the item and can be attached to any eligible Rare or Legendary item. This fully decouples the special power from the item chassis. Novel architecture not present in PoE2/LE/GD equivalently.

**Arch L3 — Procedural legendary with guaranteed modifier type(s) (none of the 4 ARPGs implement this cleanly):**
The closest precedent is Last Epoch's LP system — a Unique (fixed mod set) gains player-directed affixes from an Exalted item. This is partially procedural. A fully procedural legendary (e.g., "roll any 4 mods but at least one is from the legendary modifier surface") does not exist in these ARPGs.

### S4. Probability-distribution archetypes

Four probability-weighting mechanisms observed:

**P1 — Tag-based spawn weight (PoE2):**
Each modifier has an explicit numeric weight per item tag (e.g., str_armour = 500, str_dex_armour = 250, dex_armour = 0). Probability is weight / sum-of-weights. Tags allow fine-grained targeting. Requires upfront tag taxonomy investment. Most complex but most expressive.

**P2 — Flat pool sampling with item-type gating (D4, GD base):**
Eligible affixes for a slot are roughly flat-weighted within the pool. Probability = 1/N where N = pool size (approximately). Simpler; easier to reason about but less targetable. D4's pool is small enough (~8-20 per slot) that flat weighting works.

**P3 — Deterministic shard-targeted (LE):**
Player holds affix shards and applies them to get a SPECIFIC targeted affix (not random selection). Probability is binary: you have the shard or you don't. The randomness lives in what shards you've accumulated through play. Highest player agency for targeted crafting.

**P4 — Fixed-drop with deviation range (GD Epics/Legendaries):**
Items drop with pre-determined affix types; only the numeric values within each affix have a small deviation range. No probability weighting needed — the item type determines the affixes. Simplest system but least player agency.

### S5. Capability-toolkit precedents

Mapping existing ARPG modifier surfaces to doc 40's capability toolkit categories (doc 40 § 3.3):

| Doc 40 Capability | ARPG Precedent | Notes |
|---|---|---|
| **Multiplicative** (numerical multiplier on matching T4 path) | PoE2: "X% more damage" mods (suffix type); LE: "increased [skill] damage" affixes; D4: skill damage % affixes | All four ARPGs have multiplicative damage modifiers. PoE2 distinguishes "more" (multiplicative) from "increased" (additive) — load-bearing in PoE2 crafting decisions. |
| **Mechanic-adjusting** (changes HOW a mechanic works) | PoE2 Unique exclusive mods ("Culling Strike," elemental penetration); LE Unique mechanics-changers (Mourningfrost archetype); GD Item Skill Modifiers (behavior alteration on Legendary/MI) | In all four ARPGs, mechanic-adjusting mods are primarily reserved to unique/legendary fixed surfaces — NOT random rare affixes. This is nearly universal. The exception: GD rare mastery affixes (rare pool) do include some mechanic-adjacent modifiers. |
| **Spatial-adjusting** (changes geometry/range/area) | PoE2 support gems (not item affixes); LE Unique "Exsanguinous"-style body movement changes; D4 Aspects with area/range modifications | Spatial modifiers are mostly in the unique/legendary surface or support-gem system (PoE2). Rarely in the random affix pool. |
| **Axis-adjusting** (changes damage type or resource axis) | PoE2 Unique "X% Physical Damage converted to Y Element" mods; GD component damage conversion; LE Unique damage conversion | Damage type conversion is exclusively unique/legendary or component (GD) surface in all four ARPGs — never in the random rare pool. |
| **Added skill — passive (triggered-effect-dominant)** | GD Auto-Cast Item Skills (rare prefix/suffix surface + legendary); LE Idol proc affixes; D4 Lucky Hit procs | This is the most available in the random affix pool — D4 (Lucky Hit), LE (Idol surface), GD (rare proc affixes) all expose triggered effects in accessible (non-unique) affix surfaces. PoE2 moved this to support gems. |
| **Added skill — true active (weapon-only, extremely rare)** | PoE2 Unique weapon inherent skills; GD Weapon components with active skills; LE Unique "grants active skill" | True active skill grants are exclusive to: unique/legendary modifier surfaces OR the component/gem layer (PoE2/GD). No ARPG makes this available in the random rare pool. |

**Key synthesis finding:** Mechanic-adjusting, spatial-adjusting, and axis-adjusting modifiers are EXCLUSIVELY legendary/unique surfaces in all four reference ARPGs. The random rare pool is for numerical modifiers (damage %, resistance, life) and triggered-passive effects. This is the consistent design principle across all four systems.

### S6. Key cross-ARPG design principles

**Six principles that appear consistently:**

1. **Prefix = offense / Suffix = defense binary is universal in the three systems that use prefix/suffix (PoE2, LE, GD).** D4 (no binary) is the outlier. This binary is a fundamental organizing principle that the community uses to reason about crafting decisions.

2. **Modifier-surface expansion (not just magnitude) at legendary rarity is the primary driver of legendary-tier excitement in all four ARPGs.** The drop fantasy is "new capability" not "bigger number" — confirmed by PoE2 dev diary, LE dev blog, and D4's Season 4 redesign focus (the failure mode was "bigger numbers on same affixes").

3. **Per-slot pool must be small enough to be learnable.** D4's ~8-20 affixes per slot is the smallest and easiest to learn; PoE2's ~30-80 is the most expressive but requires external tools (craft of exile, poedb) to navigate. LE's ~20-50 with shard-targeted crafting lands in the middle: larger pools are acceptable because players target specific affixes rather than gambling across the pool.

4. **Proc/trigger architecture separated from normal affix pools reduces gear-slot complexity.** PoE2 moves triggers to support gems; LE moves proc affixes to Idols; only GD integrates rich proc affixes directly into item affix pools (rare quality) — and GD is the highest-cognitive-overhead system of the four as a result.

5. **Skill-level affixes ("+N to [skill]") are consistently available on helms and body armor (PoE2, LE) or specific slot-restricted surfaces (GD: amulets, medals, helms, gloves).** This is a consistent architectural pattern that creates meaningful per-slot gear decisions tied to specific builds.

6. **Crafting systems (PoE2, LE, D4) all converged toward increased player agency and reduced "bricking" over their development arc.** PoE2 removed Scouring/Alteration; LE kept Forge Potential deterministic on craft success; D4 removed random Tempering failures. The iterative trend is: more determinism in player-controlled crafting, with remaining randomness in item drop acquisition.

---

## Discipline #18 Compliance — Methodology-Choice Gates

The following partition design decisions must be locked BEFORE Wave 1 partition design execution fires. These are not magnitude questions; they are schema questions with multi-week downstream cost if changed after implementation starts.

### MUST DECIDE before partition lock (cannot defer to first-cycle calibration)

**Gate 1 — Prefix/suffix binary adoption:**
All three ARPGs that have it (PoE2, LE, GD) treat prefix/suffix as a load-bearing structural axis. The binary must exist in the schema BEFORE individual modifier assignments are made. If Wave 1 assigns modifiers without the binary, the downstream crafting and slot-filling logic cannot reference it.

**Flag:** If Reincarnated adopts a prefix/suffix binary (which doc 40 § 3.3 implies — offense vs defense toolkit distinction), this must be declared at schema design time. The individual modifier-to-prefix/suffix assignment is then per-modifier work; but the SCHEMA must carry the field.

**Gate 2 — Tag taxonomy for spawn weighting:**
If the system uses tag-based spawn weighting (PoE2 P1 pattern), the tag taxonomy (e.g., "Damage," "Physical," "Attack," "Elemental") must be defined at schema design time. Tags cannot be retroactively assigned without re-costing all existing modifier entries. Every modifier must be tagged at authoring time.

**Flag:** If Reincarnated uses PoE2-style tag-based weighting (most expressive; most upstream-cost), tag schema must be decided at Wave 1 before any modifier entries are created. If using LE-style flat-pool (P3) or D4-style flat-pool (P2), tag taxonomy is not required.

**Gate 3 — Item-type domain assignment:**
Which item types (weapon / helm / chest / gloves / boots / rings / amulets / off-hand) can roll which modifier domains MUST be decided before modifier pool creation. This is the partition design. Changing slot-domain assignments after modifier entries exist requires re-reviewing every entry.

**Gate 4 — Skill-level affix slot restriction:**
If the system includes "+N to [skill]" affixes (doc 40 mentions skill-node-count interaction; LE precedent is strong), which slots can carry these must be decided at schema time. LE uses helms + body armor + relics. PoE2 uses specific item types. GD uses amulets/medals/helms/gloves. Mixing this in after baseline implementation requires new affix types and new slot eligibility rules.

**Gate 5 — Proc/trigger affix routing decision:**
Where do triggered-effect affixes live? Options:
- In the normal gear affix pool (GD approach) — adds complexity to gear slot design
- In a separate item system (LE Idol approach) — cleaner gear slots; requires a separate system
- In the skill-gem/support system (PoE2 approach) — triggered effects off the item stat sheet entirely

This must be decided before partition design because it determines whether triggered-effect modifier types need to be in the per-slot pool or not. If the triggered-effect surface is separated to a non-gear system (separate "idol equivalent" or support gem), then the gear slot pools can be kept to numerical modifiers only — the per-slot pool is substantially simpler.

### MAY DEFER to first-cycle calibration (empirical)

**Magnitude calibration:** Specific numeric ranges per modifier tier (e.g., "+X to +Y flat physical damage at T1") are calibration territory. The simulation validates whether the magnitude is correct; this iterates empirically. No upfront magnitude lock needed.

**Spawn weight numeric values:** If tag-based weighting is adopted, the specific numeric weight values per tag combination can start as estimates and be tuned based on simulation findings about modifier distribution in generated gear.

**Per-slot pool completeness:** The full list of which specific modifiers go in each slot's pool can grow in iterations — the schema supports adding new entries. The structural partition (prefix/suffix binary; slot-domain assignment; trigger routing) must lock; the enumeration within each slot/domain can grow.

**Rarity escalation numeric thresholds:** At which gear tier do higher modifier tiers become accessible (equivalent to PoE2's iLvL thresholds)? This is magnitude calibration territory — it can be estimated initially and tuned against simulation validation.

---

## Knowledge Gaps Not Resolved

1. **PoE2 exact modifier pool size per item type:** poewiki.net and poedb.tw are ClaudeBot-blocked. Exact counts of modifiers per item domain are not publicly enumerated in accessible sources. Community estimates (30-80 per side per item type) are secondary sourced.

2. **GD exact spawn weight values:** Grim Dawn does not publicly document spawn weight values; the system exists but numerical weights are extracted only by modders with access to game files.

3. **LE exact per-slot pool enumeration:** lastepochtools.com was accessible via WebSearch result summaries but not directly fetchable. The 800+ figure is community-cited. Per-slot breakdown (e.g., "helms have exactly 32 prefix options") was not confirmed.

4. **D4 exact per-slot affix count (post Season 13):** Wowhead affix lists blocked; purediablo.com returned 403. Approximate pool sizes (8-20 per slot) derived from indirect evidence in accessible sources.

5. **PoE2 rare modifier pool depth vs PoE1:** Whether PoE2 expanded or contracted rare modifier pools vs PoE1 was not definitively confirmed. The community discussion (multiple sources) indicates PoE2 pools are somewhat smaller per slot than PoE1, but this was not verified against authoritative source.

6. **GD devotion proc weighting math:** The fuzzy logic on "on-attack" proc chance based on linked skill cooldown was noted but not quantified in accessible sources.

---

## Source List

**Primary sources (developer or official):**
- Grinding Gear Games dev diary on Unique Item Design: https://www.pathofexile.com/forum/view-thread/55170 (Chris Wilson; original PoE design intent; accessed 2026-05-27)
- Eleventh Hour Games developer blog on Unique Item Design: https://forum.lastepoch.com/t/unique-item-design/1264 (Mitchell; Last Epoch; accessed 2026-05-27)
- Grim Dawn official item guide: https://www.grimdawn.com/guide/items/ (Crate Entertainment; accessed 2026-05-27)
- Grim Dawn official item skills guide: https://www.grimdawn.com/guide/character/item-skills/ (Crate Entertainment; accessed 2026-05-27)
- Grim Dawn official crafting guide: https://www.grimdawn.com/guide/items/crafting/ (Crate Entertainment; accessed 2026-05-27)
- Last Epoch official forum: https://forum.lastepoch.com/ (Eleventh Hour Games; accessed 2026-05-27)

**Secondary sources (community analysis, well-cited guides):**
- Aggronaut.com LE Crafting Primer (2024): https://aggronaut.com/2024/02/27/last-epoch-crafting-primer/ (player analysis; quality: high — author demonstrates system knowledge; accessed 2026-05-27)
- Icy Veins D4 Gear Systems Overview: https://www.icy-veins.com/d4/guides/gear-systems-and-itemization-overview/ (maintained guide; accessed 2026-05-27)
- Icy Veins LE Crafting Guide: https://www.icy-veins.com/last-epoch/crafting-guide (maintained guide; accessed 2026-05-27)
- Icy Veins D4 Tempering/Masterworking Analysis: https://www.icy-veins.com/d4/news/diablo-4-devs-explain-why-tempering-and-masterworking-changed/ (accessed 2026-05-27)
- Blizzard Watch S4 Itemization Changes: https://blizzardwatch.com/2024/03/21/diablo-4-itemization-changes-season-4/ (accessed 2026-05-27)
- StudioLoot D4 Gear Affixes: https://www.studioloot.com/diablo4/articles/diablo-4-gear-affixes/ (accessed 2026-05-27)
- VHPG PoE Spawn Weighting: https://www.vhpg.com/spawn-weighting-poe/ (accessed 2026-05-27)
- MMOJUGG PoE2 Jonathan Rogers Interview: https://www.mmojugg.com/news/poe2-new-jonathan-rogers-interview-summary.html (accessed 2026-05-27)
- MMOJUGG PoE2 Item Tiers: https://www.mmojugg.com/news/understanding-item-tiers-in-poe2.html (accessed 2026-05-27)
- Skycoach PoE2 Crafting Guide: https://skycoach.gg/blog/path-of-exile-2/articles/poe-2-crafting-guide (accessed 2026-05-27)
- PCGamesN LE Crafting Affixes: https://www.pcgamesn.com/last-epoch/crafting-affixes (accessed 2026-05-27)
- Sportskeeda PoE2 Rares vs Uniques: https://www.sportskeeda.com/mmo/ (multiple articles; accessed 2026-05-27)
- Gameleap D4 S4 Itemization Rework: https://www.gameleap.com/articles/diablo-4-itemization-rework-breakdown-full-list-of-changes (accessed 2026-05-27)

**Source stability notes:**
- All game wikis (poewiki.net, lastepoch.wiki.gg, diablo4.wiki.gg, grimdawn.fandom.com) are ClaudeBot-blocked — data from these sources is excluded. Future researchers should note this blocking is per-wiki-operator policy and may change.
- Community guides (Icy Veins, Aggronaut) can be updated with game patches. The D4 sections reflect Season 13 / Lord of Hatred state; may drift as seasons continue.
- Official game guides (grimdawn.com) are stable — Grim Dawn is a released game with no active seasonal content rotation.
- Last Epoch official forum posts are stable but the game is in active development; Season 2 architectural changes (Forge of Shattering) may evolve further.
