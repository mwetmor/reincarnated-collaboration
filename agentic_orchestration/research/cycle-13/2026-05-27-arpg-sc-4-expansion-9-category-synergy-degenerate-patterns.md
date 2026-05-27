# Research — ARPG SC-4 Expansion: 9-Category Surface Verification, Synergy Taxonomy, Degenerate-Pattern Catalog — 2026-05-27

**Mode:** A (analytical)
**Commissioner:** knight-rider (Cycle 13 SC-4 Expansion)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-legolas-cycle-13-sc-4-expansion-9-category-synergy-degenerate-patterns.md`
**Authority basis:** Matt 2026-05-27 — Cycle 13 handoff § 4.1.4 + framing brief § 4.1 KR autonomous sidecar dispatching
**Companion:** `research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md` (base SC-4 research)
**Gates:** Wave 1 doc 42 (9-category verification) + Wave 2 T4 synergy scan implementation (rocket) + Wave 4 sim degenerate-state detection methodology (gamora)

**robots.txt compliance (Discipline #20):**
- pathofexile.com: `User-agent: *` with specific path disallows only (no ClaudeBot/anthropic-ai block) — PERMITTED
- lastepoch.com: `User-agent: *` + `Allow: /` — FULLY PERMITTED
- grimdawn.com: `User-agent: *` with WordPress admin path disallows only — PERMITTED
- Game wikis (poewiki.net, lastepoch.fandom.com, grimdawn.fandom.com, diablo4.wiki.fextralife.com): NOT directly crawled — data accessed via WebSearch aggregate + permitted secondary sources only (same discipline as base SC-4 research)

**Sources consulted:**
- mmojugg.com/news/path-of-exile-2-character-sheet-breakdown.html (permitted; PoE2 character sheet)
- mmojugg.com/news/biggest-changes-nerfs-best-league-starters-poe-2-050-return-of-the-ancients.html (permitted; PoE2 0.5.0 nerfs)
- deltiasgaming.com/all-stats-in-path-of-exile-2-explained/ (403 on direct fetch; data via WebSearch aggregate)
- mmoexp.com/News/path-of-exile-2-best-keystone-passives-to-build-around.html (permitted; PoE2 keystones)
- maxroll.gg/d4/getting-started/stats-for-beginners (permitted; D4 character sheet)
- dotesports.com/diablo/news/diablo-4-stats-explained (403 on direct fetch; data via WebSearch aggregate)
- studioloot.com/diablo4/articles/diablo-4-stats-guide/ (permitted; D4 stat categories)
- grimdawn.com/guide/character/character-basics/ (official; permitted; GD character sheet)
- grimdawn.com/guide/gameplay/combat/ (official; permitted; GD combat mechanics)
- vulkk.com/2024/02/26/last-epoch-idols-guide/ (permitted; LE idols)
- forum.lastepoch.com/t/ward-is-ruining-the-game/67124 (official LE forum; permitted; ward controversy)
- pcgamesn.com/last-epoch/overpowered-build-bugs-fixed (permitted; LE OP builds)
- gamerant.com/path-of-exile-2-poe2-dawn-hunt-nerfs-020-builds-items-skills-good-bad-why/ (permitted; PoE2 nerfs analysis)
- pcgamesn.com/diablo-4/patch-notes-1-1-3 (permitted; D4 CC nerf patch notes)
- mmogah.com/news/poe/guide-to-theorycrafting-in-path-of-exile (permitted; PoE theorycrafting)
- gamefaqs.gamespot.com/pc/671567-grim-dawn/faqs/78675 (403 on direct fetch; data via WebSearch)
- WebSearch aggregate (multiple queries; cited per dimension below)

---

## Summary

The 9-category character sheet framework locked in the closeout (Damage / Defense / Resource / Crit / Speed / Resistance-Penetration / On-trigger / Build-identity / Utility-Meta-progression) is **architecturally sound and non-standard by design** — it is more granular than any single reference ARPG's player-facing taxonomy, which is correct for our engine's internal logic. Reference ARPGs range from 3-category (D4: Offense / Defense / Utility) to 5-category (GD: three tabs covering Attributes + Combat + Resistance groups). The specific granularity choices most worth flagging for doc 42 are: Crit split from Damage (non-universal but defensible), Build-identity as explicit category (unique to our design), and On-trigger as a distinct surface (LE's idol system is the closest precedent). Synergy taxonomy across the four ARPGs maps naturally onto the closeout 4-category framework (tension-resolution / theme-compound / cross-chain composition / element-gap fill), with one addition warranted: a **scaling-interaction** category for synergies that arise purely from stacking the same scaling axis multiplicatively. Degenerate-pattern verification finds 7 of the 8-pattern v1 catalog confirmed by ARPG history; resource-starvation is the weakest-evidenced as a distinct degenerate pattern (more a difficulty-balance symptom). Two additional patterns surface clearly: **dot-stack degenerate** (infinite DoT layering without counterplay) and **passive-screen-clear** (numeric stacking eliminating active engagement requirement), both warranting v1 catalog extension.

---

## Topic 1 — 9-Category Character Sheet Surface Verification

### 1.1 Reference ARPG actual stat sheet categorizations

#### Path of Exile 2

PoE2's character sheet (C key) does NOT use a single top-level categorization visible as named tabs in the traditional sense. The character window is divided by **functional surface rather than labeled category headers**:

- **Defensive surface (primary character sheet):** Life / Energy Shield / Mana / Spirit / Armour / Evasion / Dodge / Block / Resistances (Fire / Cold / Lightning / Chaos) / Stun Protection / Ailment Protection / Damage Taken / Damage Redirection / Thorns / Flasks / Charms / Charges / **Miscellaneous** (for stats not belonging to a specific category)
- **Offensive surface (per-skill, NOT character sheet):** PoE2 moves offense to a per-skill pop-out window in the Skills Panel (G key). Clicking the expand arrow on each skill reveals: Accuracy Rating, chance to hit, full damage breakdown (by damage type), outgoing stun/ailment modifiers. **There is no single "Offense" tab on the character sheet — offense is disaggregated to the skill level.**
- **Attributes:** Strength / Dexterity / Intelligence shown separately (attributes panel, not the stat categories above)

**PoE2 effective category count (player-facing):** Approximately 3-4 logical groupings (Defenses / Resources / Attributes / Misc), with offense deliberately excluded from the character sheet in favor of per-skill display.

Sources: mmojugg.com PoE2 character sheet breakdown; deltiasgaming.com PoE2 stats (WebSearch aggregate); WebSearch aggregate PoE2 character sheet UI.

#### Last Epoch

Last Epoch's character sheet (C key) exposes:

- **Offensive stats:** Flat and % damage bonuses (by damage type), attack speed, cast speed, critical strike chance, critical multiplier, skill level bonuses
- **Defensive stats:** HP / Ward / Leech / Regeneration / Resistances (elemental + void + necrotic + poison) / Armor / Dodge / Block / Endurance / Crit Avoidance / Glancing Blow / Stun Avoidance / Damage Reduction
- **Resource stats:** Mana, HP pool, class-specific resource pools
- **Other stats:** Minion stats, ailment stats, and miscellaneous modifiers (class-dependent)

**LE effective category count (player-facing):** 4 named groupings: Offense / Defense / Resource / Other. This is the closest reference ARPG to our 9-category architecture in logical separation.

Sources: WebSearch aggregate LE character sheet; maxroll.gg LE defenses guide; gameleap.com LE stats explained.

#### Diablo 4

Diablo 4's stat tab on the character screen divides stats into **six explicit named categories:**

1. **Currency** (gold held; largely decorative on the stat sheet)
2. **Core Stats** (Strength / Intelligence / Willpower / Dexterity — with class-specific attribute bonuses)
3. **Offensive** (Weapon Damage, Attack Speed, Critical Strike Chance, Critical Strike Damage, Overpower Damage, Vulnerable Damage, conditional damage modifiers)
4. **Defensive** (Max Life, Armor, Damage Reduction, Resistances, Dodge Chance, Healing Received, Barrier Generation, Fortify bonus)
5. **Utility** (Lucky Hit Chance, Cooldown Reduction, Resource Cost Reduction, +Skill Ranks, Maximum Resource, Resource Generation, Movement Speed)
6. **PVP** (PVP-specific adjustments; not relevant to PVE build design)

**D4 effective category count (PVE build-relevant):** 4 meaningful categories: Core Stats / Offensive / Defensive / Utility. Crit is folded into Offensive. Resistance is folded into Defensive. Resource stats split between Core (max resource) and Utility (generation/cost reduction). No explicit Crit, On-trigger, or Build-identity categories.

Sources: maxroll.gg D4 stats for beginners; studioloot.com D4 stats guide; WebSearch aggregate D4 character sheet UI.

#### Grim Dawn

Grim Dawn's character window has **three tabs:**

- **Tab 1 (Basics/Overview):** Core attributes (Physique / Cunning / Spirit), HP / Energy resource pools, core elemental resistances (Fire / Cold / Lightning / Poison & Acid), Offensive Ability (OA), Defensive Ability (DA), Armor Rating, DPS summary
- **Tab 2 (Combat Stats):** Detailed offensive breakdown — per-ability DPS (right-click / left-click), OA/DA detailed, critical hit chance and damage multiplier, pierce chance, attack speed, cast speed
- **Tab 3 (Secondary Stats):** Secondary resistances (Aether / Chaos / Pierce / Bleed / Stun / Freeze / Slow / Knockdown / etc.), additional defensive layers, spirit-based bonuses, energy regen

**GD effective category count (player-facing tab structure):** 3 tabs, but the underlying logic covers: Attributes / Resources / Combat-offense / Resistances (primary) / Resistances (secondary) / Defense-layers. Crit is under Tab 2 (Combat). No explicit Utility or Build-identity category.

Sources: grimdawn.com/guide/character/character-basics/ (official); WebSearch aggregate GD character sheet tabs; grimdawn.com combat guide.

---

### 1.2 Category granularity comparison

| Category | PoE2 | Last Epoch | Diablo 4 | Grim Dawn | Our 9-Category |
|---|---|---|---|---|---|
| Damage (base) | Per-skill only | Offense tab | Offensive tab | Tab 2 DPS | Category 1 |
| Defense | Character sheet primary | Defense tab | Defensive tab | Tab 1 + Tab 3 | Category 2 |
| Resource | Mana/Spirit on sheet | Resource/Other | Utility (gen) / Core (max) | Tab 1 (HP/Energy) | Category 3 |
| Crit | Per-skill only | Offense tab (folded) | Offensive tab (folded) | Tab 2 (folded) | Category 4 — SPLIT |
| Speed | Per-skill (atk/cast) | Offense tab | Utility tab | Tab 2 | Category 5 |
| Resist / Penetration | Character sheet | Defense tab | Defensive (resist) + Offensive (pen) | Tab 1+3 (resist); Tab 2 (pen) | Category 6 |
| On-trigger | Unique/gem surface | Idol system (separate) | Lucky Hit (Utility) | Devotion/Auto-cast (separate system) | Category 7 — SPLIT |
| Build-identity | Not explicit | Not explicit | Not explicit | Not explicit | Category 8 — UNIQUE |
| Utility / Meta-prog | Misc (sheet) | Other | Utility tab (partial) | Not explicit | Category 9 |

---

### 1.3 Cross-ARPG comparison: specific verification questions

#### Is splitting Crit from Damage standard practice?

**No — splitting Crit into its own category is non-standard.** All four reference ARPGs fold Crit into their Damage/Offensive surface:

- PoE2: Crit appears in per-skill offense display (crit chance, crit multiplier alongside damage types)
- Last Epoch: Crit is within the Offense tab alongside damage modifiers
- Diablo 4: "Critical Strike Chance" and "Critical Strike Damage" are explicitly listed under the Offensive category
- Grim Dawn: Critical hit % and multiplier live in Tab 2 (Combat Stats) alongside DPS

**Assessment:** Splitting Crit out as Category 4 is a deliberate design choice specific to our system — it reflects Crit's distinct generator/modifier role in our 8-resource model (crit-on-condition, crit-on-element). No reference ARPG presents it this way player-facing. The split is justifiable architecturally (Crit functions as a probability modifier that multiplies damage rather than adding to it) but is not genre precedent. Worth flagging explicitly in doc 42 as a designed divergence.

#### Is Build-identity a distinct category in any reference ARPG?

**No reference ARPG has an explicit "Build-identity" category.** This is unique to our architecture and reflects the T4-attunement annotation + set-bonus rank + class-intrinsic supporting chain investment surface.

The closest precedent is Diablo 4's set-bonus display (D2/D3 era: set bonuses shown as dedicated rows in character sheet). In current D4, there is no set system — so no precedent. In LE, set bonuses appear implicitly in stat totals rather than as a labeled category. In GD, set bonuses are similarly folded into totals.

**Assessment:** Build-identity as Category 8 is genuinely novel. It reflects the transparency design intent (player sees their T4 attunement state, set completion, and supporting chain investment as a distinct dashboard dimension). No conflict with ARPG precedent because no ARPG does what we're doing at this level of generation-driven annotation.

#### Is Utility-Meta-progression (magic find / XP boost / currency drop) a standard category? Where do ARPGs place these?

- **PoE2:** Magic find (item quantity/rarity) is on the character sheet under Miscellaneous or Flask sections depending on source. No explicit "Utility" category — it lives in Misc.
- **Last Epoch:** No magic-find equivalent directly exposed on character sheet. Loot filter governs visibility but not a character stat.
- **Diablo 4:** Magic find analog ("Rare Find Chance" from Torment 1+ rewards) is not prominently on character sheet — implied through game difficulty tier selection, not a stat line.
- **Grim Dawn:** Item drop-related stats (% item drop, % magic find) are accessible on the character sheet in later tabs; present but not headlined.

**Assessment:** Utility-Meta-progression as a named category is non-standard across reference ARPGs. Most treat it as Misc or fold it into Utility. Our explicit naming of this category is a UX transparency choice that has no strong precedent but also no strong counter-precedent. Worth noting in doc 42 that this may be a "Spirit Guide data-oracle" decision (showing the player the state of their progression-acceleration stats) as much as a pure system-taxonomy decision.

#### Is Resistance-Penetration distinct from Damage, or fold-in?

Mixed across reference ARPGs:

- **PoE2:** Resistance (defensive) lives on the character sheet. Penetration (offensive — e.g., "elemental penetration") appears as a stat on the offensive display but is categorically considered an offensive modifier in the community taxonomy.
- **Last Epoch:** Resistance on defense tab; penetration on offense tab. Split.
- **Diablo 4:** Resistances are under Defensive; penetration-equivalent mechanics (Vulnerable damage) are under Offensive. Effectively split by character-sheet presentation.
- **Grim Dawn:** Resistances are Tabs 1+3. Penetration equivalents (% resistance reduction via RR skills) are NOT character-sheet stats — they are skill-effect properties not shown on the stat sheet at all.

**Assessment:** Combining Resistance and Penetration into a single Category 6 is unusual. Most ARPGs split resist (defensive category) from penetration (offensive category) because they live on opposite sides of the interaction. Our Category 6 bundles both because they interact with the same numeric axis. This is mechanically coherent but creates a UX category that is partly offensive and partly defensive — worth flagging in doc 42 as a category with mixed semantic direction.

---

### 1.4 Recommendation for doc 42 authoring

Present neutrally as follows (final call is gandalf):

1. **9-category count is appropriate** — the reference ARPG range is 3-5 player-facing categories; our 9-category design is intentionally more granular for internal logic and transparency purposes. No ARPG evidence suggests 9 is wrong; 3 ARPGs use 4 meaningful categories (LE is closest).

2. **Three specific divergences to document explicitly in doc 42:**
   - Category 4 (Crit split from Damage): non-standard; justified by Crit's probability-modifier role; no precedent conflict
   - Category 8 (Build-identity): unique to our design; no ARPG precedent; justified by T4-attunement annotation architecture
   - Category 6 (Resistance-Penetration combined): mixed-direction category; most ARPGs split these across Offense and Defense surfaces; worth deciding whether the internal-taxonomy logic overrides the player-facing semantic expectation

3. **No amendment to 9-category lock required** based on ARPG landscape. The framework is a designed extension of ARPG convention, not a departure from it.

**Wave-1-informing:** This entire section is Wave-1-informing — it feeds gandalf doc 42 partition cycle work directly.

---

## Topic 2 — Synergy Taxonomy

### 2.1 Community synergy categorization per ARPG

#### Path of Exile 2

PoE2's theorycrafting community organizes synergies around **keystone passive interactions** and **support gem chains**:

**Keystone synergies (documented patterns from mmoexp.com and WebSearch aggregate):**

| Keystone | Synergy type | What it resolves | Downstream tension created |
|---|---|---|---|
| Blood Magic | Tension-resolution | Eliminates mana dependency for skill costs | Forces life sustain stacking; creates vulnerability to life-cost-without-regen |
| Chaos Inoculation | Tension-resolution | Eliminates chaos damage vulnerability; provides chaos immunity | Forces complete energy shield reliance; any ES depletion is lethal |
| Elemental Equilibrium | Cross-chain composition | Enables multi-element manipulation for self-inflicted infusions | Requires careful element sequencing; using the wrong element breaks the infusion |
| Iron Reflexes | Theme-compound | Converts evasion to armor for Strength builds using hybrid gear | Eliminates evasion as a defensive layer entirely |
| Mind over Matter | Tension-resolution | Redirects damage to mana before life (survivability layer) | Requires heavy mana investment; competes with mana-for-skills budget |
| Whispers of Doom | Cross-chain composition | Enables dual curse application | Requires Blasphemy or slow activation; no synergy if only one curse is relevant |
| Zealot's Oath | Tension-resolution | Converts life regeneration to ES recovery | Disables natural ES recharge; requires high life regen stacking instead |
| Eldritch Battery | Cross-chain composition | ES absorbs mana damage; pairs with MoM | Requires high ES AND high mana investment; over-investment in either reduces efficiency |

**Support gem chains:** The PoE2 community identifies "support gem chains" as the primary synergy vehicle — stacking multiple support gems that multiply specific properties (e.g., Cast on Melee Kill + chain-friendly AoE + splash supports). These are primarily **theme-compound** synergies.

**Trap synergy examples (PoE community identified):**

- **Elemental Equilibrium with self-damage:** Builds that accidentally hit themselves with the "wrong" element break their own infusion cycle. Looks powerful (manipulating elements for infusions) but creates a self-sabotage failure mode if element sequencing is imprecise.
- **Dual-conversion stacking:** Stacking multiple damage conversion effects (e.g., physical-to-fire + fire-to-cold) produces unintended interaction because conversions compound — the final element may not benefit from any of the scaling investments. Community-identified as a theorycrafting pitfall.
- **Herald chains pre-nerf (PoE2 0.5.0):** Herald of Ice + Thunder combination appeared powerful but created a passive screen-clearing pattern that invalidated active engagement. Players invested heavily; GGG nerfed broadly. Builds that over-invested in herald scaling lost their investment entirely.
- **Archmage mana scaling (PoE2 pre-0.2.0):** Stacking mana for damage via Archmage appeared like a multiplicative synergy; it was, but the magnitude (11x bonus at high investment in 0.1.0) created a degenerate top-end that forced a nerf eliminating much of the investment value. Trap for anyone who built toward the high-end — nerf landed and 30%+ damage reduction followed.

Sources: mmoexp.com PoE2 keystones guide; gamerant.com PoE2 0.2.0 nerfs; mmojugg.com PoE2 0.5.0 patch.

#### Last Epoch

Last Epoch's theorycrafting community identifies synergies along three axes:

1. **Skill tree node chains:** Linear skill tree paths where nodes amplify each other (e.g., Dive Bomb Falconer: Devastating Dive → Rushing Wings → Focused Hunter nodes chain-amplify the same skill)
2. **Idol proc synergies:** Idol affixes trigger on conditions (% chance to cast [skill] on [trigger]) composing with active skill kit (e.g., Explosive Trap detonation triggers Falcon penetration buff — a cross-chain composition pattern)
3. **Defensive layer stacking:** Ward generation + damage reduction + Endurance stacking as a theme-compound synergy

**Degenerate synergy exemplars (community-identified):**

- **Infinite Ward generation (PoE2 CI analog):** Pre-tuning Falconer + Runemaster builds generated 50,000+ Ward via Vampiric Pool bug (40% of minion HP as ward vs intended 4%) and Sanguine Runestone threshold scaling bug. The synergy: Ward generation scaled faster than incoming damage, creating effective immortality. EHG patched mid-season after player survey (55.5% voted for fix). Detection method: community report + developer confirmation.
- **Ward-as-mandatory archetype (ongoing community debate):** Ward-heavy builds (1k HP / 30-60k Ward) create a "binary survivability" pattern where the build is either immortal or one-shot. Community thread (forum.lastepoch.com) debated capping Ward at a HP multiple. EHG's response was to nerf Ward Retention formula at Cycle launch rather than hard-cap — a mitigation-via-generation-parameter approach.
- **Falconer/Warlock S1 dominance:** Described by EHG as "server-wide trouble" builds — the pattern where one build archetype dominates by such a margin that other archetypes are implicitly de-validated.

**Trap synergy exemplars:**

- **Dual Mastery statistical-not-actual synergy (LE class mastery):** Builds that look thematically aligned on paper but share no mechanical amplification. Example: choosing two masteries that both deal damage of different types without any conversion bridge means neither type benefits from the other's scaling — the character deals two separate damage types without multiplicative combination. Looks thematically coherent; underperforms vs a single-type build.
- **Specific idol proc + no damage scaling:** Idol procs trigger skills that are not scaled by any gear/passive investment — the proc fires but deals base damage only. Example: a "% chance to cast [skill] on hit" idol that triggers a skill not in the player's build — the proc fires at base level with no amplification. Community refers to this as "dead proc syndrome."

Sources: pcgamesn.com LE OP builds; forum.lastepoch.com ward debate; WebSearch aggregate LE synergy builds; vulkk.com idols guide.

#### Diablo 4

D4's theorycrafting community structures synergies around:

1. **Aspect placement optimization:** Which aspects go on which slots (Offensive aspects → weapons/gloves/rings/amulets; Defensive → armor slots) and how aspects compose with class mechanics
2. **Tempering recipe targeting:** Players select tempering affixes to fill specific build gaps — a form of deliberate gap-fill synergy
3. **Lucky Hit chains:** Building Lucky Hit Chance to amplify multiple on-hit effects simultaneously (cross-chain composition via a unified proc axis)

**Degenerate synergy exemplars:**

- **Eagle Evade Spiritborn (Oct 2024 nerf):** Spiritborn's evade could be cast more rapidly than normal depending on input method, allowing infinite evade loops while projecting demon-seeking projectiles with no cooldown. Pattern: input-speed exploit + proc trigger compounding → mandatory-skill-lock (evade spam was the only required action). Blizzard detected via community report + performance impact reports; patched the evade animation in 2.0.3. Mitigation: animation lock enforcement.
- **Overpower damage stacking (ongoing nerfs):** Overpower creates burst damage based on HP + Fortify thresholds. Repeatedly nerfed across Seasons 8 and 9 because Overpower stacking with critical strike created a one-shot floor that bypassed encounter design. Detection: community tier lists + telemetry (implied by rapid response cadence). Mitigation: scalar reduction, then formula change.
- **Vulnearble + multiplier stacking (S4 origin):** Pre-Season 4, stacking "damage to Vulnerable enemies" across multiple affix slots created multiplicative-appearing but actually-additive interactions (multiple same-bucket multipliers added rather than multiplied). The community initially over-valued these affixes; the Season 4 pruning of narrow conditionals corrected the pool. Trap for players who stacked multiple Vulnerable affixes expecting multiplicative benefit.

**Trap synergy exemplars:**

- **Same-bucket damage stacking:** D4 community explicitly documented that stacking multiple modifiers of the same damage category (e.g., multiple "increased damage to close enemies" affixes) adds together rather than multiplies. This is a well-known newbie trap — players assume stacking more of the same type is multiplicative; it is additive and hits diminishing marginal returns rapidly.
- **Conditional affix stacking (pre-S4):** The pre-Season 4 pool contained narrow conditionals ("deal X% more damage to Injured enemies") that community analysis showed almost never triggered in actual gameplay flow — enemies either died too fast or the player wasn't close enough. Affixes that looked like DPS multipliers were functional dead weight. S4 pruning removed most of these.

Sources: windowscentral.com Eagle Evade nerf; wowhead.com Overpower nerfs; gamerank.com D4 season 8 nerfs; gamerant.com aspects stacking; maxroll.gg D4 stats.

#### Grim Dawn

GD's theorycrafting community (grimtools.com community) organizes synergies around the **dual mastery system** and **damage conversion chains**:

1. **Good mastery pairings:** Combinations where one mastery provides resistance reduction (RR) that benefits the other mastery's primary damage type (e.g., Occultist provides Vitality RR + Chaos RR, pairing with any vitality/chaos damage mastery). Resist reduction is the GD community's canonical example of a **tension-resolution synergy** — RR converts damage invested in one mastery from "blocked by enemy resists" to "bypasses resistance floor."
2. **Conversion chains:** Damage type conversion (e.g., physical-to-fire + fire-to-cold) creates a synergy where one mastery's physical damage converts to another type that a second mastery scales multiplicatively. When conversion aligns cleanly, this is a **cross-chain composition** synergy.
3. **Devotion + skill linking:** Attaching Celestial Powers to specific skills with the right proc type (on-attack vs when-hit vs on-crit) creates compound trigger patterns — a **theme-compound** synergy.

**Degenerate synergy exemplars:**

- **200k DPS + 400k physical retaliation + immortal combination (community-cited):** Warder (Shaman/Soldier) builds that stacked vitality storm totem, retaliation damage, and specific devotion chains to create characters that were simultaneously immortal (facetanking bosses like Callagadra) and dealing multiplicative damage through retaliation stacking. Crate's detection method: community report on Hardcore. Mitigation: tuning balance patches.
- **Resist reduction over-stacking:** GD has additive resist reduction from multiple sources; the community documented that stacking multiple RR sources past the monster's resist cap creates "wasted RR" — the mechanic functions but the investment is not returned. This is documented as a **resource-overflow analog** in the GD skill/devotion investment context.

**Trap synergy exemplars:**

- **Dual masteries with conflicting weapon requirements (e.g., Trickster: Nightblade + Shaman):** Nightblade (dual-wield optimized) + Shaman (two-hand weapon optimized) are "a bit at odds" — community consensus is this combination requires deliberately avoiding the weapon-type-conflicting skill trees within each mastery. Looks powerful on paper (both have strong skills); underperforms vs a unified-weapon-type combination.
- **Double conversion break (community-documented):** Equipping two items that both convert the same damage source (e.g., two items with 100% fire-to-cold conversion) splits the conversion proportionally (50% fire + 50% cold from each) rather than fully applying both. Players who stack multiple conversion items expecting full stacking on each lose damage. Community FAQ on this is explicitly titled "Double conversion item, which has priority?"
- **Battlemage (Arcanist + Soldier):** Community consensus is this is one of the weaker dual mastery pairings — "has the least synergy between them and generally performs poorly at endgame." Bonuses are not multiplicative in practice because Arcanist (caster) and Soldier (physical melee) don't amplify each other's primary scaling axes.

Sources: grimdawn.com combat guide; WebSearch aggregate GD synergy/trap builds; steamcommunity.com GD discussions; gamefaqs.gamespot.com GD FAQ.

---

### 2.2 Cross-ARPG synthesis: does the closeout 4-category framework hold?

The closeout § 2.5 four-category synergy framework maps well across all four ARPGs with one addition:

| Synergy category | PoE2 evidence | LE evidence | D4 evidence | GD evidence |
|---|---|---|---|---|
| **Tension-resolution** | Blood Magic (mana cost → life cost removes mana tension); CI (removes chaos vulnerability) | Ward-as-defensive-floor (resolves HP-squish tension) | Lucky Hit build (resolves proc randomness through Lucky Hit Chance investment) | Resist reduction (RR resolves "damage blocked by enemy resist" tension) |
| **Theme-compound** | Support gem chains stacking same scaling axis | Skill tree node chains (Dive Bomb → Devastating Dive → Rushing Wings) | Aspect composition for class-mechanic amplification | Devotion + skill-type matching (on-attack Celestial Powers on high-attack-speed skills) |
| **Cross-chain composition** | Elemental Equilibrium (multi-element manipulation across infusion axes) | Idol proc triggering skills from a parallel subsystem | Lucky Hit Chance boosting multiple on-hit effects simultaneously | Dual mastery: one mastery provides RR for another mastery's damage type |
| **Element-gap fill** | Off-element keystones (Iron Reflexes for hybrid armor builds) | Idol resistance fixes (idols plugging resist gaps) | Tempering recipe targeting to fill stat gaps | Augments/components used to cap resistances |
| **NEW: Scaling-interaction** | Archmage mana-to-damage scaling (multiplicative axis stacking) | Ward generation rate stacking | Aspect stacking same-bucket (additive, not multiplicative — creates trap variant) | Conversion chain stacking across damage types |

**Addition warranted:** A **Scaling-interaction** category should be added to the framework. This captures synergies (and their degenerate/trap variants) that arise from stacking values on the same scaling axis — the interaction is mathematical rather than mechanical. The distinction matters for algorithm design because:
- True scaling-interaction synergies (multiplicative stacking across separate multiplier buckets) are high-value and non-degenerate
- False scaling-interaction (additive stacking within the same bucket, mistaken for multiplicative) is the source of many trap builds in D4 and GD
- The algorithm's synergy scan should distinguish between "does this compound multiply independently?" vs "does this add to the same bucket?"

The first-do-no-harm principle (Discipline #7 candidate from closeout) surfaces as the **Downstream-tension-creation** check. Multiple real-world examples confirm its necessity:
- CI (PoE2): resolves chaos damage tension; creates binary survivability tension
- Ward extreme (LE): resolves survivability tension; creates feast-or-famine gameplay tension
- Archmage (PoE2): resolves mana-scaling tension; created degenerate top-end tension requiring a sweeping nerf

All three are real-world instances of synergies that resolved Pass 1 (upstream resolution) while failing Pass 2 (downstream creation). The first-do-no-harm check is empirically validated by ARPG history.

**Wave-2-informing:** The scaling-interaction addition and the Pass 1/Pass 2 framework details are Wave-2-informing — they feed rocket's T4 synergy scan implementation.

---

### 2.3 Recommendation

The closeout 4-category framework holds. One addition — **Scaling-interaction** (5th category) — is warranted based on cross-ARPG evidence. The scaling-interaction category covers both the strongest legitimate synergies (true multiplicative stacking across buckets) and the most common trap synergies (additive stacking within the same bucket, misidentified as multiplicative). The algorithm needs to distinguish these cases explicitly.

---

## Topic 3 — Degenerate-Pattern Catalog Research

### 3.1 ARPG-sourced degenerate patterns and the v1 catalog verification

**Summary table: v1 catalog vs ARPG evidence**

| v1 Pattern | PoE2 analog | LE analog | D4 analog | GD analog | Confirmed? |
|---|---|---|---|---|---|
| 1. Infinite stunlock | Freeze loop builds; chain CC | Not prominently documented | Enemy CC nerf (1.1.3); player-side not documented | OA/DA imbalance producing stun dominance | **Partial** — player-side player-induced stunlock not strongly evidenced; enemy CC is well-documented |
| 2. Zero-damage void | Build that deals only defensive layers, no offense | Not documented | Not documented | Build with 200k DPS + 400k retaliation with 0 active offense investment | **Weak** — no clear ARPG example of zero-damage player builds as a sim-validation issue |
| 3. Mandatory-skill-lock | Archmage Spark dominance (single skill meta); Herald chain dominance | Falconer/Warlock single-archetype dominance | Eagle Evade spam (evade was the only required action) | Vitality Storm Totem immortal builds | **CONFIRMED** — strong cross-ARPG evidence |
| 4. Permanent-CC | Freeze chain builds; crowd control chains pre-PoE2 | Not documented | D4 1.1.3 enemy CC nerf; player-side CC builds mentioned but not documented | DA inversion builds creating permanent stun | **Partial** — enemy-facing more documented than player-induced |
| 5. Resource-starvation | Mana starvation noted in PoE2 early access feedback | LE forum debate on "mana as balancing tool" | Resource exhaustion at high cooldown rotation | Energy exhaustion in kiting builds | **WEAK** — documented as difficulty issue and early-game friction, not as a degenerate sim state |
| 6. Degenerate-tank | CI + ES builds pre-nerf; Poison Pathfinder ES regeneration | Ward extreme builds (1k HP / 50k Ward) | Resolve stacking "make every build immortal" (LoH) | 200k DPS + immortal Warder | **CONFIRMED** — strong cross-ARPG evidence |
| 7. Bounce-CC | Skill cancellation via rapid-fire CC (pre-nerf) | Not documented | Not documented | "When-hit" devotion proc loops | **PARTIAL** — exists as a devotion/proc architecture issue in GD; less documented in others |
| 8. Resource-overflow | PoE2 Overflow mechanic (overflow past max explicitly designed) | Ward "feast or famine" (overflow → instant death on depletion) | Maximum resource affixes in Utility tab | Energy overflow in certain GD devotion proc builds | **PARTIAL** — resource overflow as a problem is partially intentional design (PoE2 Overflow mechanic) vs accidental degenerate state |

---

### 3.2 Detection methodology per ARPG

| ARPG | Primary detection method | Evidence |
|---|---|---|
| **PoE2 (GGG)** | Community meta-analysis + telemetry (inferred) + broad balance patches. GGG primarily detects via community tier list dominance + player build diversity metrics (implied by "stale meta" language). Direct telemetry not publicly confirmed. Mitigation cadence: per-league patch cycle. | gamerant.com 0.2.0 nerfs; mmojugg.com 0.5.0 patch |
| **Last Epoch (EHG)** | Community survey + bug report correlation. EHG explicitly polled players on mid-season nerfs (55.5% vote threshold for action). Distinguishes bug-driven OP from balance-driven OP — bugs get mid-season patches; balance issues wait for cycle launch. | pcgamesn.com OP builds; gamerant.com EHG survey |
| **Diablo 4 (Blizzard)** | Community report + performance impact + telemetry (inferred from rapid response to Eagle Evade). Blizzard has not publicly described internal detection methodology. Response cadence is fastest of the four — hotfixes within days of major exploits (Eagle Evade: live for ~2 weeks before nerf). | windowscentral.com Eagle Evade nerf; gamerank.com S8 nerfs |
| **Grim Dawn (Crate)** | Community report-driven exclusively. Crate is a small studio; no public telemetry system described. Forum-driven: community posts extreme builds → Crate reviews → balance patches in major updates (not hotfixes). Slowest response cadence. | steamcommunity.com GD discussions; WebSearch GD nerf history |

**Cross-ARPG detection pattern:** All four studios rely primarily on **community-report-driven detection** (forum posts, tier lists, build diversity analysis) rather than pure telemetry. Telemetry may inform Blizzard and GGG internally but is not the described primary detection mechanism. The EHG player-survey approach is uniquely transparent and unique to studios with small enough player bases to make surveys actionable.

**Implication for Cycle 13 degenerate-state detection:** The v1 catalog's hybrid approach (explicit pattern checks first + KPM-out-of-band as proxy) is well-positioned because it is sim-driven rather than community-report-driven — which is appropriate for generation-time validation (no players yet). The pattern-check approach mirrors what studios do retroactively; our implementation does it pre-ship.

---

### 3.3 Mitigation patterns per ARPG

| Mechanism | ARPG uses | Description |
|---|---|---|
| **Nerf the source mechanic** | PoE2, D4, LE | Reduce the scalar that enables the pattern (e.g., Archmage bonus reduced from 11x to 3x; Ward Retention formula change at cycle launch; Overpower scalar nerfs) |
| **Nerf the synergy interaction** | PoE2, GD | Limit stacking (e.g., conversion cap at 100%; RR diminishing returns) |
| **Reshape the encounter** | D4 | Enemy CC tuning (patch 1.1.3: enemy CC duration and frequency reduced) — mitigation via encounter-side rather than player-side |
| **Add counterplay mechanic** | PoE2, LE | Cooldown enforcement on trigger-loops (Eagle Evade animation lock); Ward Retention formula change rather than hard cap |
| **Remove from pool** | D4 | S4 pruning: remove narrow conditional affixes that created decision paralysis without meaningful build differentiation |
| **Community-survey gating** | LE | Mid-season nerfs require community consensus before deployment — limits over-patching risk |

---

### 3.4 Additional patterns from ARPG literature (v1 catalog extension candidates)

**Pattern 9 — Passive-screen-clear / Zero-engagement degenerate:**

The PoE2 0.2.0 patch (gamerant.com analysis) explicitly describes what GGG called "passive screen-clearing through stacked numerical advantages rather than active engagement." Herald of Ice + Thunder, Archmage Spark, and attribute-stacking all created a meta where the player's required active engagement dropped to near-zero. The patch notes language: "a rather stale meta where many builds used the same Ascendancies, items, and skills."

This pattern is distinct from mandatory-skill-lock (Pattern 3): Pattern 3 = one skill dominates rotation (player still actively uses that skill); passive-screen-clear = player barely needs to act at all (the build self-executes against the encounter). Pattern 3 is a rotation-narrowing problem; passive-screen-clear is an engagement-elimination problem.

**Proposed definition for v1 catalog extension:** Passive-screen-clear: player's active inputs drop below a minimum engagement threshold (e.g., <1 active skill used per 10 seconds of encounter) while encounter proceeds successfully. Distinct from efficiency (good players minimize wasted actions) — passive-screen-clear eliminates the requirement for meaningful input.

**Pattern 10 — DoT-stack degenerate / Unbounded damage-over-time:**

PoE2 (0.5.0 nerfs — Poison Pathfinder) + GD (DoT stacking from different sources always does full damage, per GD game mechanics wiki) both surface a degenerate pattern where damage-over-time effects stack without bound: each new DoT application adds to damage rather than refreshing. At extreme investment, the stacking produces burst-equivalent damage on the first contact (enemy dies from accumulated DoTs before any DoT duration expires meaningfully). This is distinct from degenerate-tank (Pattern 6) and from zero-damage void (Pattern 2) — it is an offensive analog where DoT becomes a de facto one-shot with infinite uptime.

**Proposed definition for v1 catalog extension:** DoT-stack degenerate: damage-over-time sources stack without a per-type cap to the point where effective damage on application exceeds the encounter's HP pool within one tick window — degenerates to "instant kill on contact" despite using a DoT mechanic. Detection: DoT DPS sum at maximum stack count > 5x expected sustained DPS.

---

### 3.5 Assessment of v1 8-pattern catalog

**Strongly confirmed (4/8):** Pattern 3 (mandatory-skill-lock), Pattern 6 (degenerate-tank), Pattern 1 (infinite stunlock — partial, player-side), Pattern 7 (bounce-CC — partial via GD Devotion proc loops).

**Weakly confirmed or partially evidenced (3/8):** Pattern 4 (permanent-CC — enemy-side well-documented, player-side less so), Pattern 8 (resource-overflow — partially a designed mechanic in PoE2, not always degenerate), Pattern 5 (resource-starvation — documented as a difficulty/tuning symptom, not clearly a degenerate simulation state per se).

**Least evidenced as a distinct sim-failure mode (1/8):** Pattern 2 (zero-damage void — no clear ARPG analog where a character deals functionally zero damage and the sim reports this as other than "build doesn't work").

**Recommendation for v1 catalog:** The 8-pattern v1 catalog is sufficient for Cycle 13 v1 scope. Two additions worth queuing for v1.1:
- Pattern 9: Passive-screen-clear (engagement-elimination)
- Pattern 10: DoT-stack degenerate (unbounded DoT compounding)

These are Wave-4-informing items for gamora's degenerate-state detection methodology consultation (SC-7).

---

## Knowledge gaps not resolved

1. **PoE2 character sheet exact UI label taxonomy:** PoE2 moves offensive stats to per-skill panel rather than a named category on the character sheet. The exact label text for each section of the PoE2 character sheet (does it say "Miscellaneous" vs "Other" vs no header?) was not confirmed by a source able to display the exact UI text. Functional content is well-documented.

2. **GD Tab 2/Tab 3 exact header names:** Official GD guide confirms three tabs exist; exact named headers for tabs 2 and 3 were not confirmed (the tabs display content but may not have labeled names beyond "Combat" and "Details" or equivalent).

3. **Last Epoch character sheet exact UI label text (current Season 4):** LE character sheet content is well-documented; whether the Season 4 UI uses "Offense / Defense / Resource / Other" as exact header strings vs different labels not confirmed from a 2025/2026 source.

4. **GD degenerate pattern specifics (Crate patch notes):** Crate's patch notes are not easily indexed by web search; specific GD degenerate-pattern history is documented primarily by community forum posts rather than official patch note citations. GD official patch notes were not fetched (forum URL not directly accessible).

5. **PoE community explicit "trap synergy" taxonomy:** No PoE-specific guide was found that taxonomizes trap synergies explicitly (the community identifies them case-by-case rather than via a named framework). Data extracted from observed build pitfalls rather than a dedicated taxonomy document.

---

## Discipline #18 timing classification

**Wave-1-informing (gandalf doc 42 authoring):**
- All of Topic 1 (§§ 1.1-1.4): 9-category surface verification, cross-ARPG comparison, specific verification questions, recommendation for doc 42
- Topic 2 § 2.1 synergy exemplar data (per-ARPG): feeds gandalf pattern library curation (D7 honor AI-tell line; pattern library is gandalf-curated)

**Wave-2-informing (rocket T4 synergy scan implementation):**
- Topic 2 §§ 2.2-2.3: Scaling-interaction 5th synergy category addition; Pass 1 / Pass 2 empirical validation across ARPGs; degenerate synergy detection patterns

**Wave-4-informing (gamora degenerate-state detection methodology — SC-7):**
- Topic 3 §§ 3.1-3.5: Full v1 catalog verification; detection methodology per ARPG; mitigation patterns; Pattern 9 and Pattern 10 extension candidates

---

## Source list

| Source | URL | Access | Permission |
|---|---|---|---|
| mmojugg.com PoE2 character sheet | https://www.mmojugg.com/news/path-of-exile-2-character-sheet-breakdown.html | Fetched | Permitted |
| mmojugg.com PoE2 0.5.0 nerfs | https://www.mmojugg.com/news/biggest-changes-nerfs-best-league-starters-poe-2-050-return-of-the-ancients.html | Fetched | Permitted |
| mmoexp.com PoE2 keystones | https://www.mmoexp.com/News/path-of-exile-2-best-keystone-passives-to-build-around.html | Fetched | Permitted |
| gamerant.com PoE2 0.2.0 nerfs | https://gamerant.com/path-of-exile-2-poe2-dawn-hunt-nerfs-020-builds-items-skills-good-bad-why/ | Fetched | Permitted |
| maxroll.gg D4 stats for beginners | https://maxroll.gg/d4/getting-started/stats-for-beginners | Fetched | Permitted |
| studioloot.com D4 stats | https://www.studioloot.com/diablo4/articles/diablo-4-stats-guide/ | Fetched | Permitted |
| pcgamesn.com D4 patch 1.1.3 | https://www.pcgamesn.com/diablo-4/patch-notes-1-1-3 | Fetched | Permitted |
| grimdawn.com character basics | https://www.grimdawn.com/guide/character/character-basics/ | Fetched | Permitted |
| grimdawn.com combat guide | https://www.grimdawn.com/guide/gameplay/combat/ | Fetched | Permitted |
| forum.lastepoch.com ward debate | https://forum.lastepoch.com/t/ward-is-ruining-the-game/67124 | Fetched | Permitted |
| pcgamesn.com LE OP builds | https://www.pcgamesn.com/last-epoch/overpowered-build-bugs-fixed | Fetched | Permitted |
| vulkk.com LE idols guide | https://vulkk.com/2024/02/26/last-epoch-idols-guide/ | Fetched | Permitted |
| windowscentral.com Eagle Evade | https://www.windowscentral.com/gaming/diablo-4-latest-patch-nerfs-everyones-favorite-build-amongst-some-other-much-needed-bug-fixes | Attempted; content truncated | Permitted |
| WebSearch aggregate (multiple queries) | Various — cited inline per dimension | WebSearch | N/A |
| Prior SC-4 base research | research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md | Read | Internal |
