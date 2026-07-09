# Research — ARPG Monster-Modifier (Affix) Genre Canon — 2026-07-08

**Mode:** A (analytical)
**Commissioner:** gandalf (design steward), E10 Leg 1 — "mob rare/champion affix layer, full-spec first pass" (Matt-ruled 2026-07-08)
**Feeds:** gandalf + Matt Pattern-B design session (E10 Leg 2); findings return to gandalf
**Constraint:** Do NOT produce a recommended affix list — canon expressed as axes; prescription deferred to design session

---

## Summary (5 sentences)

Every major ARPG since Diablo II has independently converged on the same four-family design space: stat-inflation modifiers, terrain-denial (ground-AoE) modifiers, displacement/CC modifiers, and summon/spawn modifiers. The genre's clearest design lesson comes from the Path of Exile Archnemesis disaster (3.17–3.19): bundling multiple effects under a single opaque thematic label, coupling mod-stacking to lethal probability spikes, and tying loot conversion to specific mod identities all independently broke player agency at scale, and GGG was forced to dismantle the system entirely in 3.20 in favour of "one modifier, one effect, self-descriptive name." Grim Dawn's Nemesis system is the genre's strongest precedent for the Reincarnated RIVAL class — faction-reputation-driven named-hunter spawns that pursue the player across sessions using their own kit, drop from a dedicated chest, and are announced by flavor title rather than mechanical label. Loot coupling is consistently tight: D2 boss packs set the floor (modifier count drives pack composition and therefore item-drop volume), PoE rare rarity bonus scales with mod count, and Last Epoch's Champion tier makes the sealed affix directly correspond to the Champion's exclusive modifier. The cross-cutting design axis that unlocks all of this cleanly is "one mod, one readable thing, element-coded telegraph" — an axis Reincarnated can implement in substrate-native terms through its element vocabulary, threat tiers, and archetype pools.

---

## §1 — Per-Game Canon

### 1.1 Diablo II / D2R

**Sources:** Maxroll D2 Elite Monster guide; Wowhead D2R Boss Attributes guide; community wiki (diablo2.diablowiki.net); PureDiablo; D2R community database.

#### A. Rarity/Tier Structure

Three enemy elevation tiers above normal:

| Tier | Modifier Count (by difficulty) | HP Multiplier | Drop Guarantee |
|---|---|---|---|
| **Champion** (colored name, one of 5 champion types) | Type-defined — fixed stat package | x3 Normal / x2.5 NM / x2 Hell | 2 potions + 1 Magic item |
| **Unique** (boss with random mods) | Normal: 1 / NM: 2 / Hell: 3 | x4 Normal / x3 NM / x2 Hell | Higher drop rate; not directly mod-count gated |
| **Super Unique** (named fixed encounters, e.g. Andariel) | Fixed preset of 2–5 mods | Varies | Boss-specific tables |

**Champion types (D2/D2R) — five fixed archetypes, each a bundle of stats:**

- **Champion:** balanced boost; notably vibrant coloration
- **Berserker:** highest damage output; mLVL +3; lowest life (50% base in Hell)
- **Fanatic:** fastest movement (+100% run/walk); lowest defense (-70%); 200% life in Hell
- **Ghostly:** translucent appearance; applies cold on-hit; 80% damage resistance across ALL elements (physical included — the signature "immune to basically everything" type)
- **Possessed:** highest life multiplier (x6 Normal; x4 Hell); mid-range damage

Note: Champions spawn at area level +2 (Berserkers +3), affecting item-level of drops from their kill.

#### B. Unique/Boss Modifier Pool (the 13 canonical affixes)

These are rolled on unique monsters (not champion types — champions use the fixed-type system above):

| Modifier | Mechanical Effect | Minion Inheritance |
|---|---|---|
| **Extra Strong** | Boss: +75-150% damage (scales per diff); +AR bonus | Minions: +49% damage, +33% AR (Hell) |
| **Extra Fast** | +100% run/walk speed for boss | Full inheritance |
| **Cursed** | 75% chance to cast Amplify Damage debuff on hit (amplifies player damage taken by ~100%) | Minions inherit in NM/Hell |
| **Magic Resistant** | +40% resistances to cold/fire/lightning | NM/Hell only as a modifier |
| **Fire Enchanted** | Adds fire damage; triggers corpse explosion on death (75–100% max HP over 4-yard radius) | Melee minions: fire dmg in NM/Hell only; ranged: all difficulties |
| **Cold Enchanted** | Adds cold damage; triggers Frost Nova on death (slows player) | Same minion inheritance pattern as Fire |
| **Lightning Enchanted** | Adds lightning damage; releases charged bolts on death | Same pattern |
| **Spectral Hit** | Adds random elemental damage type on each hit; +20% all element resistances (unless already 75%+) | Minions: +33-50% damage to one random element in NM/Hell |
| **Stone Skin** | +50% physical damage resistance; +200% base defense | Not inherited |
| **Mana Burn** | Drains mana equal to 4× damage dealt (intended); bugged in original code to multiply by 256 — effectively one-shotted mana bars | Minions burn mana in NM/Hell |
| **Aura Enchanted** | Boss radiates one of: Might, Holy Fire, Blessed Aim, Holy Freeze, Holy Shock, Conviction, Fanaticism (all scaled to monlvl/6–8) | Aura affects minions too |
| **Multiple Shots** | Ranged bosses fire 3 missiles per attack instead of 1 | Not inherited |
| **Teleportation** | Boss can teleport; heals up to 30% max HP per teleport | Not inherited |

**Historical note — Thief:** Pre-LoD, certain unique modifiers could cause equipment to drop from player's belt or even inventory on hit. Nerfed to potion-belt-drop only. Removed entirely in LoD because it was "very game-crash inducing" and felt unfair. Documented failure case: resource-attack modifiers that target player's build resources are high-frustration when they operate on assets outside the combat loop (equipment/inventory).

#### C. Minion Inheritance Rules

Boss packs spawn with 3–5 minions. Minion inheritance is selective, not blanket:
- **Full inheritance:** Extra Fast, Aura Enchanted
- **Half-stat inheritance:** Extra Strong (minions get ~half the boss damage bonus)
- **Difficulty-gated inheritance:** Elemental Enchanted (melee minions only get it in NM/Hell; ranged minions always)
- **No inheritance:** Stone Skin, Teleportation, Multiple Shots, Spectral Hit (boss only)
- Minions always receive HP bonuses scaled to difficulty (separate from modifier inheritance)

#### D. Telegraph Conventions

D2's telegraph language is primarily **visual-on-model**:
- Champion types: distinctive coloration (Ghostly is translucent, Fanatic moves obviously faster, Berserker is saturated)
- Unique boss modifiers: **nameplate** shows modifier names in yellow/orange text above the monster
- Aura Enchanted: visible Paladin aura ring around the boss — visually unambiguous
- Elemental Enchanted: color tinting (fire = red glow, cold = blue glow, lightning = yellow arcs)
- No ground pre-telegraphing (ground effects are the attack, not a warning)

**Naming convention:** D2 uses plain English descriptors that directly state the mechanic: "Extra Strong," "Stone Skin," "Mana Burn." The name IS the mechanic description. This is the genre floor for readability.

#### E. Loot Coupling

- Champion types always drop: 2 potions + 1 Magic-quality item (regardless of type)
- Unique boss modifier count does NOT directly scale item quality — the quality tier is set by the boss's item level (area level +2 for champions, area level for uniques)
- Boss pack kills create area-based drop density: more minions = more rolls = more items from the pack as a whole. Player count (1–8) also scales minion HP and drop rates

#### F. Design Lessons

- The 13-modifier system is deliberately narrow. Every modifier does exactly one named thing. Players learn the set within a few hours of play and it remains legible for the game's lifetime.
- Mana Burn's bug (256× multiplier) is the genre's canonical "resource-attack modifier gone wrong" case — the intent was interesting (counter-magic builds) but implementation punished mana-dependent builds catastrophically. Retained for identity/meme reasons in D2R.
- Thief's removal establishes the precedent: modifiers that attack player's build-investment assets (gear, inventory) rather than their in-combat state are unfun and tend to break game state.
- The 5 champion types function differently from the 13 unique modifiers — champion types are fixed bundles (the "class" of the champion), while unique mods are random draws. This two-track structure reappears in every later ARPG.

---

### 1.2 Diablo III

**Sources:** Maxroll D3 Elite Affixes; Blizzardwatch D3 elite affix guide; DiabloWiki Boss Modifiers; PureDiablo Reflects Damage patch analysis.

#### A. Rarity/Tier Structure

| Level Range | Max Affixes |
|---|---|
| 1–29 | 1 |
| 30–49 | 2 |
| 50–59 | 3 |
| 60+ | 4 |

**Two elite sub-classes:**
- **Champion packs** (blue text, 3–4 members): same affix set shared across the pack
- **Rare monsters** (yellow, with minions): unique named mob + minion group; yellow mob holds 4 affixes at cap

**Affix category budget rule:** An elite pack always has at least 2, at most 3 offensive affixes; cannot exceed 1 defensive AND 1 crowd-control affix simultaneously.

**Champion-exclusive affixes:**
- **Avenger** (Defensive): when a pack member dies, surviving members gain stacking damage/speed buffs
- **Fire Chains** (Offensive, Fire): fire chains link between pack members — deals constant damage to anything caught in the chain; visual telegraph is the visible chain itself
- **Health Link** (Defensive): all damage is distributed evenly across all living pack members

**Rare-exclusive affixes:**
- **Horde** (Defensive): doubles minion count
- **Missile Dampening** (Defensive): creates a slow-projectile dome — projectiles entering the dome lose 90% speed
- **Juggernaut** (Defensive): complete CC immunity + 30% damage reduction; the "can't be slowed or stunned" elite
- **Frozen Pulse** (Offensive, Cold): icicle chases player and pulses cold damage at 15-yard radius when stationary

#### B. Complete Shared Affix List (23)

**Terrain-denial / "Don't Stand in Fire" category:**
| Affix | Effect | Spatial Behavior |
|---|---|---|
| **Arcane Enchanted** | Rotating arcane sentry beams radiate from center | Frogger-style rotation, player must time movement |
| **Desecrator** | Spawns molten pit beneath player | Persistent ground hazard under player position |
| **Molten** | Boss leaves burning trail; death explosion (massive radius, 3-sec delay) | Trail + death AoE; death explosion is the deadliest single hit |
| **Plagued** | Large green poison pools on/around player, persist until elite dies | Persistent ground hazard expanding over time |
| **Mortar** | Launches arcing explosive projectiles at player area | Projectile arc with landing zone indicator |
| **Thunderstorm** | Lightning strike zone around player | Random-position lightning in player zone |

**Displacement / movement-threat category:**
| Affix | Effect |
|---|---|
| **Vortex** | Pulls player to monster position |
| **Wormhole** | Spawns paired portals; player walking into one is teleported to the other (often into pack) |
| **Waller** | Spawns U-shaped or straight walls; traps player in corridor |
| **Frozen** | Icicle chunks land and freeze player (solid freeze, movement-preventing) |
| **Orbiter** | Central lightning ball with orbiting rings; rings track player |

**CC (crowd control) / behavioral category:**
| Affix | Effect | Banned Pairs |
|---|---|---|
| **Jailer** | Purple prison, immobilizes all targets within 60 yards for 1.5–2.5s | Mutually exclusive with Knockback, Nightmarish, Vortex |
| **Knockback** | Pushes player backward on melee hit | ME with Jailer, Nightmarish, Vortex |
| **Nightmarish** | Fear: player runs in random direction | ME with Jailer, Knockback, Vortex |
| **Teleporter** | Monster repositions instantly; deals damage on arrival | — |

**Stat / property category:**
| Affix | Effect | Notes |
|---|---|---|
| **Electrified** | Boss deals bonus lightning damage; directional lightning bolts on hit | — |
| **Fast** | Increased attack and movement speed | — |
| **Illusionist** | Creates 3–5 temporary decoy copies; copies can attack | Soft CC on player attention |
| **Reflects Damage** | Returns percentage of damage dealt back to attacker when orange glow active | REMOVED — see §Failure Appendix |
| **Shielding** | Temporary invulnerability globe (blue shield) | Only yellow/rare mobs |
| **Poison Enchanted** | Criss-crossing poison paths from boss position | — |

**Banned affix pairs (confirmed):** Jailer + Knockback + Nightmarish + Vortex are mutually exclusive with each other (the CC category budget cap ensures at most 1 of these per pack).

#### C. Telegraph Conventions

D3 established the modern **multi-channel telegraph grammar**:
1. **Nameplate:** Affix names listed below the health bar (text labels); iconic abbreviation visible at range
2. **Ground indicators:** Pre-telegraphed AoE zones (Desecrator, Plagued) appear as colored ground decals before damage activates
3. **VFX color coding:** Element-coded (fire = orange, cold = blue, poison = green, lightning = yellow, arcane = purple)
4. **Audio sting:** Distinct audio cue when affix ability activates (particularly Waller walls appearing)
5. **Physics behavior:** Vortex has distinctive pull-toward animation; Waller has wall-rise animation (cannot be missed)

**Key innovation over D2:** Terrain-denial affixes use a "WARNING → HAZARD" two-phase system — a ground indicator briefly appears before the damage is active, giving players a choreography window to react. This is the foundational "dance with the ground" design that the genre has replicated ever since.

#### D. Loot Coupling

- No direct mod-count scaling of drop quality at the affix level
- Rarity class (champion vs rare) determines drop table tier
- In Greater Rifts: more elite packs spawn proportional to GR level; affix pool does NOT narrow or widen by GR tier — the same pool is used throughout

#### E. Design Lessons

- **Spatial choreography vs stat inflation:** D3 clearly bifurcates the design space. The most memorable and replayable affixes are choreography (Arcane Enchanted's rotating beams, Frozen Pulse's tracking icicle) not stat inflations. Reflects Damage is the canonical counter-example — it was pure stat response that bypassed player movement skill entirely.
- **Category budget rule is load-bearing:** Banning more than 1 defensive AND 1 CC affix per pack prevents composition disasters. Without this gate, combinations like Jailer + Waller + Vortex would produce guaranteed-death compositions with no counterplay.
- **Illusionist is the "attention CC" outlier:** It doesn't control the player's body but their targeting attention — a design class that has no direct parallel in D2.
- **Affix legibility via nameplate:** The explicit text listing is critical for player vocabulary-building. After a few hundred hours, experienced players read the nameplate and immediately shift to the correct avoidance pattern. This "learned choreography vocabulary" is one of D3's biggest design successes.

---

### 1.3 Diablo IV

**Sources:** Fextralife D4 Elites wiki; diablo4.gg Elite Affixes guide; Wowhead D4 Elite Affix overview; VHPG D4 affix pages.

#### A. Rarity/Tier Structure

Elites can have 2–4 affixes. No level-gated scaling (the affix count is not documented as level-gated the way D3 was). Minions of rare elites spawn as normal mobs with increased HP pools only (no affix inheritance).

#### B. Complete Affix Pool (organized by element, ~21 affixes)

**Cold (4):**
| Affix | Mechanic |
|---|---|
| **Cold Enchanted** | Attacks deal cold damage and chill; leaves frost patch on ground |
| **Chilling Wind** | Wall of wind that chills players passing through it |
| **Frozen** | Summons 3 icy crystals that chill in AoE; detonate after 3s (8s CD) |
| **Tempest** | Icy spikes that pull player toward enemy (minor damage + displacement, 13s CD) |

**Fire (3):**
| Affix | Mechanic |
|---|---|
| **Fire Enchanted** | Periodic 3-fireball burst; explodes 6s post-death |
| **Explosive** | Spawns fire orbs that detonate in large AoE after 5s (15s CD) |
| **Mortar** | Launches 4 mortars raining around target (3s CD); overlapping indicators spike damage |

**Lightning (5):**
| Affix | Mechanic |
|---|---|
| **Lightning Enchanted** | Releases 3 lightning spheres that bounce terrain when boss is struck |
| **Electrified Obelisks** | 3 lightning pillars chain bolts between themselves and players (6s, 12s CD) |
| **Shock Lance** | Rotating lightning beam with orbiting projectile (15s duration, 5s CD) |
| **Teleporter** | Instant reposition with lightning damage; 0.33s cast telegraph + audio cue (8s CD) |
| **Crackling Soul** | On death: spawns lightning sphere that follows and explodes near players |

**Poison (3):**
| Affix | Mechanic |
|---|---|
| **Plaguebearer** | Creates toxic pools; explodes on death (replaces D3 Plagued) |
| **Poison Enchanted** | Drops poison pool under player on hit; bonus blob on death |
| **Swinging Axes** | Lobs poisonous projectiles |

**Shadow (4):**
| Affix | Mechanic |
|---|---|
| **Shadow Enchanted** | Spawns attacking shadow clone on hit (4s duration, single hit) |
| **Terrifying** | Pentagrams on ground inducing fear (2s fear, 2s activation delay, 7s CD) |
| **Debilitating Storm** | Zones applying blindness + slow |
| **Hellbound** | 3-headed statue binding players in chains within radius (6s, 15s CD) |

**Generic/Utility (21+ in total, notable ones):**
| Affix | Mechanic |
|---|---|
| **Waller** | U-shaped walls trapping player in corridor (12s CD) — carried from D3 |
| **Suppressor** | Bubble preventing all ranged attacks/spells from outside |
| **Summoner** | Summons up to 6 minions from surrounding mob type (20s CD) |
| **Berserker** | Activates below 50% HP threshold — enhanced damage/speed |
| **Shielded** | Temporary immunity globe — carried from D3 |
| **Reprisal** | 25% barrier granted on activation |
| **Multishot** | Boss's ranged attacks split to 3 projectiles — echoes D2 Multiple Shots |
| **Vampiric** | Health leech on attacks and abilities |
| **Teleporter** | Instant repositioning (also listed under lightning by source — lightning-damage variant) |
| **Physical Resistance** | Flat physical damage reduction |
| **Non-Physical Resistance** | Flat elemental damage reduction |
| **Unstoppable** | CC immunity (echoes D3 Juggernaut) |

#### C. Telegraph Conventions

D4 extends D3's grammar with tighter visual consistency:
- **Affix icons** below health bar (not just text) — each affix has a designated icon
- **Element color-coding** formalized: fire = orange ground indicators; lightning = yellow/white; cold = blue; poison = green; shadow = purple
- **Explicit cast animations:** even Teleporter has a 0.33s cast + audio cue before arrival
- **Ground-hazard indicators** visible before activation (pre-telegraph window carried from D3)
- **Nameplate listing** of all active affix names below the HP bar

#### D. What D4 Dropped from D3 (and why)

- **Reflects Damage** — permanently removed (see §Failure Appendix)
- **Wormhole** — removed (perceived as instant confusion/unfair displacement)
- **Health Link** (champion-exclusive pool sharing) — not present in D4's documented pool
- **Avenger** (kill-buff on pack death) — not present
- **Fire Chains** — replaced by Demonic Chains (now a pull/displacement, not a damage link between pack members)
- Overall philosophy: D4 reduced pure-displacement/unavoidable-teleport effects and increased pre-telegraphed-spatial affixes. The design direction is "more readable, more survivable with good positioning" vs D3's "always moving to avoid."

#### E. Design Lessons

- D4's smaller pool (~21 vs D3's 30+) reflects a deliberate readability investment. Players learn the full set faster.
- Element-indexing the affix pool (every affix belongs to a damage element) means the player can read an elite's nameplate and immediately prepare their elemental mitigation/avoidance.
- Suppressor is D4's novel addition: a bubble that punishes pure-ranged play and forces approach. A "proximity pressure" affix — the first systematic use of this design class in the Diablo franchise.
- Berserker's threshold trigger (below 50% HP) introduces **temporal state transitions** to affix design — the mob changes behavior phase mid-fight. This feeds into boss-phase design without requiring full boss architecture.

---

### 1.4 Path of Exile — with Archnemesis Case Study

**Sources:** PoE Wiki Monster Modifiers; PCGamesN Archnemesis coverage; GGG official forum "What's Next for Archnemesis Modifiers Part 3" (3.19); GGG 3.20 Balance Manifesto: Monster Mods and Archnemesis; devtrackers.gg GGG developer statements; Guided.news 3.20 Archnemesis removal account.

#### A. Pre-Archnemesis System (PoE 1.0 through 3.16)

PoE's pre-AN system was acknowledged by GGG as "very out of date" but functional:
- **Magic monsters:** 1–2 modifiers (one named prefix, one named suffix)
- **Rare monsters:** 3–4 modifiers (prefix + suffix pairs)
- 1 modifier could be an aura (passive emanation affecting nearby enemies)
- Modifier names functioned like item affixes: "Hasted Shaman of Haemorrhage" communicated two effects
- The pre-AN pool included ~40 modifiers covering: stat inflation, elemental damage conversion, aura buffs, life regen, damage reflection, mana drain, bleed application, curse application, etc.
- **Notable pre-AN modifier: Nemesis** (in Nemesis league, originally): spawned unique items on rare kill — the league mechanic that proved loot-coupled rare modifiers were extremely desirable
- **Bloodlines** (in Bloodlines league): magic packs with shared unique properties (linked packs, spawning-on-death, volatile, etc.) — proved that pack-as-unit modifiers with behavioral properties created distinctive encounters

#### B. Archnemesis League (3.17 — February 2022)

AN was introduced as a league mechanic: players could apply modifier tokens to rare monsters to build custom bosses, with the assembled monster dropping rewards corresponding to its modifier composition.

**Tier structure (3.17 league version):**
- **Tier 1 (base modifiers, ~30 total):** naturally-dropping modifier tokens. Examples: Toxic, Vampiric, Deadeye, Sentinel, Flame Strider, Treant Horde, Berserker, Chaosweaver, Necromancer, Bonebreaker, Hasted, Trickster, Mystic, Hexer, Frenzied, Empowered, Bloodletter
- **Tier 2 (2-ingredient recipes):** created by combining two T1 tokens. Examples: Arcane Buffer (Mystic + Sentinel), Juggernaut (Bonebreaker + Sentinel), Malediction (Hexer + Chaosweaver)
- **Tier 3 (1+ T2 recipes):** highest-tier combinations. Examples: Arakaali-touched, Abberath-touched, Tukohama-touched, Lunaris-touched, Solaris-touched, Brine King-touched, Shakari-touched, Kitava-touched, Innocence-touched

**Bundled effect design (the problem):** Each named modifier contained multiple effects bundled under a single thematic label. Example cited by GGG in 3.20 manifesto:

> "Magma Barrier" (3.17–3.19) bundled: magma barrier creation, physical-to-fire damage conversion, bonus fire damage, fire resistance, physical damage reduction, and spawning volatile flamebloods to follow the player.

Another GGG example: "Archer" hid five separate effects behind a one-word name with no in-game description accessible during combat.

**The "Touched" tier's loot-conversion mechanic (3.19):**
In 3.19, loot-conversion modifiers were formalized: high-tier modifiers converted all drops to a specific type. Examples:
- **Drought Bringer:** "dropped items are converted to utility flasks"
- **Innocence-touched:** items converted to scarabs by rarity tier
- **Solaris/Lunaris-touched:** items converted to currency by rarity
- **Tukohama-touched:** items converted to maps
- **Kitava-touched:** rarity upgraded one tier (magic → rare → unique)
- **Corrupter:** all drops become corrupted

The interaction of stacked loot-conversion mods produced some high-reward outcomes but the opacity of "what will I get" made players feel compelled to swap to magic-find characters before killing specific mod combinations — creating a gameplay interruption (see GGG's own analysis).

#### C. Core Integration and Community Revolt (3.18 Sentinel League — May 2022)

When AN modifiers were integrated into the base rare monster pool (all rare monsters in all areas gained 1–4 AN modifiers), the reward bonuses were NOT preserved. Players began encountering the most lethal mod combinations in normal gameplay with no escalating reward rationale.

**Failure axes (documented from community and GGG statements):**

1. **Opacity failure:** Multi-effect bundling under thematic names meant players could not identify what a modifier did during combat. "Archer" read as a ranged archetype hint but contained five unrelated effects.

2. **Stacking lethality spikes:** Because each modifier contained 3–6 effects, a 3-modifier rare might have 9–18 simultaneous effects, some of which interacted multiplicatively. Players reported "dying in one hit from white mobs with four mods" — a phrase that circulated widely.

3. **Loot-conversion reward opacity:** The predictable-reward system that worked in the league (you built the mob; you knew the reward) became actively frustrating in core (you encountered the mob; you got punished with flask-only drops). Community director Bex_GGG acknowledged: "there is a fair bit of team agreement around it feeling bad."

4. **Ele-reflect class problem:** Certain modifier combinations produced effective elemental reflect behavior — one of the most historically-hated mechanics in the ARPG genre (see D3 Reflects Damage below). When combined with the opacity failure (players couldn't read which modifiers caused this), encounters became build-invalidating rather than build-challenging.

5. **League-blocking behavior:** Players began actively avoiding high-difficulty league mechanics when AN rare encounters were present within them, because the added AN difficulty was uncoupled from the league's reward structure. GGG acknowledged this via devtrackers.

#### D. Dismantling Timeline

- **3.18.0 (Sentinel League, May 2022):** AN modifiers added to core rare pool (revolt begins)
- **3.18.0b hotfix 1:** First round of numerical reductions (damage values, spawn rates cut)
- **3.19.0 (Lake of Kalandra, Aug 2022):** Significant modifier list passes; loot-conversion system refined; many numerical reductions; some modifiers removed (e.g., Deadeye lost all its bonus stats entirely)
- **3.19.0f (Sept 2022):** Further reduction to defensive AN modifiers; GGG explicitly acknowledged "quite a large jump in difficulty from campaign to early maps" caused by AN
- **3.20.0 (Forbidden Sanctum, Dec 2022):** Complete replacement. AN system retired.

#### E. 3.20 Replacement System — Design Principles (GGG's Own Words)

From the 3.20 Balance Manifesto: Monster Mods and Archnemesis (official GGG forum thread):

> "The keyworded mod names were not fully descriptive of what they did. The mods often had multiple effects bundled which made them harder to understand. Due to how many effects were included in a single mod, it made too many encounters too complex."

Four principles of the replacement system:
1. Each modifier performs **one specific function**
2. Mod names are **self-descriptive** (e.g., "Additional Critical Hits" rather than "Deadeye")
3. Encounters are **simpler on average** while retaining interesting emergent combinations at the margins
4. Loot rewards are **hidden** (not associated with specific visible mods) — eliminating the "magic-find swap" compulsion

The Magma Barrier example above: the 3.20 replacement "just puts a magma barrier around the monster and does nothing else."

#### F. Rogue Exiles — Named Rival Precedent

Rogue Exiles (introduced in PoE 1; present and expanded in PoE 2): named hostile NPCs built on the same character-creation system as player characters.

- Each Rogue Exile has a **player-class archetype**: their skills, gear, and stat loadout mirror a player build type
- They carry **unique items** that determine their stats (unlike regular mobs with abstract affix bonuses)
- They use **player skills** including Dodge Roll in PoE 2
- They use **life flasks** mid-combat to heal
- They have **smart targeting/pathfinding** beyond normal mob AI
- **Announced only by name:** no special intro sequence; they appear as a named entity on the minimap/nameplate
- **Escape mechanic (PoE 2):** If a Rogue Exile kills you (solo) or wipes your party, they portal out and leave the map forever with their loot. This creates genuine narrative stakes.
- **Loot coupling:** Rogue Exiles can drop the unique items they carry

This is the genre's cleanest existing implementation of "a hostile that operates on player-kit grammar" — which maps directly to the Reincarnated RIVAL class concept.

#### G. Design Lessons

- "One mod, one thing, self-descriptive name" is not a simplicity concession — it is the design discipline that makes complexity emergent at the combination layer rather than baked into individual modifier opacity.
- Loot-conversion mods that convert drops to a specific type work in opt-in contexts (league content) but are punishing in ambient encounters where the player has no agency over encountering them.
- Recipe-based mod combination systems (player assembles the monster) are a valid design space for *player-initiated* encounters; they fail when applied to *ambient* random encounters where the player is the reactive party.
- The pre-AN PoE system had a key virtue: modifier names operated like item affix grammar (prefix + suffix pairs), which players of an item-affix-heavy game already understand. AN abandoned that grammar and paid for it.

---

### 1.5 Last Epoch

**Sources:** Last Epoch official wiki (Enemy Affixes, Champions, Enemies); Maxroll LE Champions guide; IGGM Season 2 Champion Affixes; Sportskeeda LE Champion Item Affixes; lastepochtools.com.

#### A. Rarity/Tier Structure

| Enemy Rarity | Modifier Count | Visual Telegraph |
|---|---|---|
| Normal | 0 | No special marking |
| Magic | 1 (prefix or suffix) | Single modifier label |
| Rare | 2 (1 prefix + 1 suffix) | Two modifier labels |
| Champion | Rare mods + 1 exclusive Champion modifier | Distinctive red glow; skull-eye icon on minimap; orange nameplate |

Champions are harder than Rare enemies specifically due to the exclusive Champion modifier, not just stat scaling.

#### B. Enemy Modifier System (Magic/Rare)

Every enemy has a random chance to spawn with prefix, suffix, or both. Higher-level enemies have higher chance of higher-rarity spawning.

**Suffix special behavior:** Optionally, a suffix can be element-associated, granting either:
- **"Shred":** +3% element shredding to hits (reduces player resistance)
- **"Boost":** +50% element damage to hits AND +50% element resistance

This creates a clean mechanical distinction between offensive (Shred) and defensive (Boost) suffix families based purely on element association — no additional naming required.

The broader modifier naming space for LE magic/rare enemies in the endgame (Monolith of Fate echoes) includes modifiers like Volatile, Frenzied, Armored, Hasted, Warded — these are stat-inflation modifiers that translate directly to combat stats. The LE wiki Enemy Affixes page exists but was not fetchable at time of research; the confirmed framework is the prefix/suffix dual-slot system with element-keyed suffix behavior.

#### C. Champion Modifiers (the 14 Sealed-Affix-Coupled Types)

The Champion modifier is the **exclusive mechanic** — it directly determines what Sealed Affix drops on the item the Champion guarantees. The 14 confirmed Champion modifier types (Season 2, 2026) are named by the affix they carry:

Abyssal, Carnage, Death Grip, Infernal, Meteor, Mirage, Portal, Profane, River (Primalist-restricted), Spark, Storm, Venomous, Volcano, Whirlpool.

Each Champion modifier produces a Sealed Affix on a restricted gear slot type. For example, Meteor Champions drop 1H Axes/Daggers/Wands with Meteor Champion's Sealed Affix. The Champion's combat behavior is also tuned to the affix theme (a Volcano Champion deals fire damage).

**Design principle at work:** Champion modifier = visual identity + combat archetype + loot identity as a unified bundle. The modifier name IS the loot name. Perfect information for the player once the vocabulary is learned.

#### D. Telegraph Conventions

- Red glow on the Champion monster model
- Skull-eye icon on minimap for Champion locations
- No ground-pre-telegraph noted as distinct from regular rare combat
- Sealed affix type is NOT revealed pre-kill — only on item drop

#### E. Loot Coupling

- Champions guarantee at least 1 item drop with a Sealed Affix
- The specific Sealed Affix is determined by the Champion's exclusive modifier (direct 1:1 coupling)
- Sealed Affixes cannot be crafted-over, replaced, or upgraded; they behave like near-unique affixes
- Champion loot tier is the game's primary explicit "kill this enemy type for this specific affix" loop
- Higher corruption levels in Monolith spawn more Champions, making corruption scaling = Champion density scaling

#### F. Design Lessons

- Last Epoch's minimalism is a conscious stance: the enemy modifier system does not try to generate encounter complexity through modifier combination. The ITEM system generates complexity; enemy modifiers drive item-farming motivation.
- Champion modifiers as the loot-coupling anchor point is a clean design: players hunt Champions not for a chance at a loot table but for a specific, named, guaranteed affix type. Eliminates RNG frustration at the "do I kill this" decision.
- The element-keyed suffix mechanic (Shred vs Boost) is the tightest encoding in the genre: one word captures element + role in a way that is teachable and memorable.

---

### 1.6 Grim Dawn (including Nemesis System)

**Sources:** Grim Dawn official monster guide; Grim Dawn Factions/Reputation guide; Steam community Nemesis spawn discussions; Massively Overpowered Grim Dawn Nemesis overhaul (2024); SlashingCreeps Nemesis guide; SteamAH Nemesis locations guide.

#### A. Hero Monster System

Hero Creatures (marked by a **gold star above their head**; appear in orange on-screen) are distinct from normal or champion-rarity monsters:
- Spawn randomly within standard monster packs at elevated rates (increasing to "Hated" reputation tier triggers significantly increased hero spawn rates for that faction)
- Are individually named (given a unique name — they feel like named sub-bosses, not generic elite-rarity mobs)
- Highly resistant to crowd control
- Take reduced damage from %-of-current-life attacks
- Carry **item-quality equipment** that affects their combat behavior:

> "If a boss spawns with a weapon that burns mana, you might suddenly find yourself low on precious energy."

This means hero creatures carry actual item-grammar affixes (GD's item system is a Prefix/Suffix grammar system identical to item crafting). A hero's dangerous modifiers are not a separate mechanic — they ARE items on the enemy. The enemy's loot table and combat capability are unified through the item system.

#### B. Hero Creature Archetypes (Combat-Relevant Modifier Bundles)

GD uses named **archetypes** for hero combat behavior (similar to D2's champion types):

| Archetype | Primary Combat Behavior |
|---|---|
| **Bruiser** | Reduced damage taken; increased damage dealt; chance to stun on attacks |
| **Burning** | Bonus fire damage; periodic ring-of-fire AoE |
| **Corrupted** | AoE aether explosion; aura empowering self + nearby allies with aether |
| **Swift** | Aura increasing attack + movement speed for self + allies |
| **Unstoppable** | Bonus chaos damage; CC immunity aura for self + nearby allies |
| **Voidtouched** | Chaos field; chaos chain lightning; some variants chaos-teleport to far targets |
| **Arcane** *(Ashes of Malmouth)* | Elemental bolt that purges player buffs; aura increasing elemental damage for allies |
| **Timewarped** *(Ashes of Malmouth)* | Projectiles + fields slowing/petrifying players; aura accelerating allies and slowing players |
| **Vampiric** *(Ashes of Malmouth)* | Wave of vitality-sapping energy (heals self for damage dealt); life leech aura for allies |

Key note: Each archetype functions as a **faction-aligned bundle** (Burning heroes appear in fire-aligned factions; Voidtouched in Cthonian/Void factions). The archetype communicates expected faction membership, element, and combat pressure type in one label.

#### C. Nemesis System — The Vengeance Faction Boss

**Trigger mechanic (the most directly relevant RIVAL precedent):**

Nemesis bosses are faction-specific ultra-rare bosses that spawn when the player has accumulated "Nemesis" reputation level (the deepest hostile tier, deeper than "Hated") with a given faction. Reputation is earned by killing that faction's monsters. The more you kill, the more the faction escalates its response.

**Spawn behavior:**
- Nemesis spawns are **random encounters** within areas where that faction is present
- They do not spawn at fixed locations (2024 overhaul changed some fixed spawn points to fully dynamic)
- Each Nemesis spawns **once per game session** (not infinitely renewable within a session)
- GD guide flavor text on Nemesis: *"Should you encounter one, do not try to flee; it is already too late."*

**The 11 Nemesis Bosses (base game + expansions):**
| Nemesis Name | Faction | Associated Threat |
|---|---|---|
| Valdaran, Storm Scourge | Aetherials | Lightning/Aether |
| Benn'Jhar, the Colossal | Cthonians | Physical/Chaos |
| Fabius "the Unseen" | Human Outlaws | Physical/Bleeding |
| Moosilauke, the Chillwind | Aetherials | Cold |
| Zantarin, the Eternal | Undead | Vitality/Undead |
| The Iron Maiden | Cronley Gang (Human) | Physical |
| Archmage Aleksander | Aetherials | Aether/Fire |
| Reaper of the Lost Beasts | Beasts | Physical/Chaos |
| Kubacabra, the Endless Menace | Beasts | Chaos |
| Grava'Thul, the Voiddrinker | Chthonians | Chaos/Void |
| Kaisan | Eldritch (Forgotten Gods DLC) | Eldritch |

**Announcement grammar:** Nemesis bosses are announced by a formatted title: **"[Evocative Epithet], [Name]"** or **"[Name], [Title]"** (e.g., "Moosilauke, the Chillwind"). No cutscene or pre-combat screen — the name appears on the nameplate. The epithet is thematic, not mechanically descriptive.

**Loot coupling:** Nemesis bosses drop from a dedicated **Nemesis chest** (not a body) after kill:
- Very high chance of Epic item
- Increased chance of Legendary item
- Increased chance of crafting Blueprints
- This chest-based loot delivery is a distinct design signal: the boss is a loot event, not just a hard fight

#### D. Telegraph Conventions

- **Visual:** Gold star above hero head (persistent); hero name appears as orange text
- **Nemesis:** Name on nameplate with title designation; no other unique visual above-and-beyond a very hard fight
- **Archetype behavior:** Player learns archetype effects through repetition (Burning heroes always use ring-of-fire; Unstoppable heroes are CC immune); no in-combat text list like D3

#### E. Design Lessons

- Hero creatures carrying actual item-quality affixes is a radical unification of the item and enemy systems. It makes every hero encounter a preview of the loot table.
- The Nemesis system's reputation-scaling is the first ARPG implementation of "the world pushes back as you get stronger" at the enemy-encounter level. It creates narrative emergence from mechanical action (killing lots of X faction enemies eventually causes X faction to send their champion after you).
- "Once per session" Nemesis spawn limit is a significant design choice: it makes Nemesis encounters feel like events rather than grind. It prevents the Nemesis from becoming just another HP-sponge to farm continuously.
- The title-epithet naming convention ("Moosilauke, the Chillwind") creates fictional identity without mechanical prescriptiveness. The player doesn't know what "the Chillwind" does mechanically from the name alone — they learn through encounter.

---

### 1.7 Torchlight II + Diablo Immortal

#### A. Torchlight II — Champion System

**Sources:** Torchlight wiki Champions (T2); Steam community champion discussions; Slashnblast TLTII reference.

Torchlight II's champion system is a close adaptation of the D2/D3 model, simplified for a smaller scope:

**Champion structure:**
- Champions spawn with a pack of lesser monsters (same structure as D2 boss packs)
- Pack members have more HP than normal and **inherit the champion's special property**
- Special properties are listed in **violet text** in the monster's description
- Visual identification: champions are ringed by a **red light circle** at their base; "Champion" label appears in the description

**Special property list (confirmed vanilla mechanics):**
Champions can have special properties including: teleporting, attacking extra fast, causing more damage per hit, and elemental damage types. Community documentation (modding wiki) suggests the vanilla set is narrower than D2/D3 and does not have a well-maintained complete wiki list — the champion system is acknowledged as lighter than contemporaries.

**Elemental attack mechanics (confirmed from combat documentation):**
- Burn (from Fire): applies DoT based on level
- Freeze (from Ice): slows attack speed, cast speed, movement speed by 33%
- Shock (from Electric): causes the struck enemy to emit Charged Bolts at nearby targets when hit

**Loot:** Champions drop good loot and are the primary source of named/rare item drops in TL2's dungeon content. The specific loot table coupling to modifier type is not documented precisely — TL2's approach is straightforwardly "champions = better drops."

**Design note:** TL2 is a deliberate simplification of the formula. It doesn't attempt to innovate the champion system; it adapts D2's structure for a lighter-touch experience. The narrower affix pool is a feature, not an oversight.

#### B. Diablo Immortal — Mobile Adaptation

**Sources:** Diablo Fandom Monster Traits (DI); Fextralife DI Affixes wiki; DiabloHub champion/elite trait descriptions; Blizzard mobile design Q&A.

**Rarity tier structure in DI:**
| Tier | Trait Count |
|---|---|
| Champion | 1 trait |
| Rare | 2 traits |
| Ancient | 1–3 traits |
| Unique | 1–3 random traits + 2 fixed traits |

**Mobile adaptation decisions (what changed vs D3):**
- The overall trait pool largely mirrors D3 (Jailer, Arcane Enchanted, etc. are present)
- **Jailer (DI version):** immobilizes for 1.5–2.5s; pack members have cooldown between uses (preventing instant re-application); some rapid-repositioning skills (like Teleport) can break the trap
- **Arcane Enchanted (DI version):** summons glowing orbs that form into rotating arcane sentry beams — same mechanic as D3, adapted for touch controls
- Session duration design: Blizzard explicitly designed Diablo Immortal activities in 1-minute, 3-minute, and 5-minute units. This directly compresses encounter duration and means that affix encounters must resolve (telegraph, react, fight) within much shorter time windows than PC-paced ARPGs.

**Mobile-specific affix adaptations:**
- Touch controls constrain avoidance choreography (no precise mouse movement for narrow-window spatial dodges)
- Trait pools are kept to 1–2 traits for most encounter types; the 4-affix elite from D3 is reserved for Ancient/Unique tiers only
- "New affixes added" noted in April 2026 update (Season 11) including Legendary Affixes and PvP-specific abilities — suggests ongoing expansion post-launch

**Creative traits unique to DI (community-cited):** ground becoming icy floors (movement physics shift); wind pushing players to one side (directional displacement). These are mobile-native designs that use simple binary physics (slippery vs normal) rather than precise spatial choreography.

**Design lessons from DI:**
- Mobile session grain forces affix telegraph to be faster (shorter warning windows) and affix duration to be shorter
- Reducing max trait count for ambient enemies (1 trait = Champion, 2 = Rare) keeps the cognitive load manageable in contexts where players are on a phone, distracted, and playing in 3-minute sessions
- Touch control constraints make some D3 affixes (Arcane Enchanted's precise beam-dodge; Wormhole's portal-exit positioning) mechanically harder to execute — DI adapted these rather than removing them

---

## §2 — Cross-Cutting Syntheses

### 2A — Affix Taxonomy: Functional Families

Collapsing the union of all games, the complete genre affix design space clusters into **8 functional families**:

| Family | Sub-types | Genre Examples |
|---|---|---|
| **1. Damage-Add** | Elemental conversion, bonus damage, damage type overlay | Extra Strong (D2), Electrified (D3), Fire/Lightning/Cold Enchanted (all games), Vampiric (PoE, D4) |
| **2. Defense / Stat-Inflate** | Physical resistance, elemental resistance, HP multiplier, shield | Stone Skin (D2), Juggernaut (D3), Shielded (D3/D4), Magic Resistant (D2), Physical/Non-Physical Resistance (D4) |
| **3. Terrain-Denial** | Ground AoE, persistent hazard, trail | Plagued/Molten/Desecrator/Arcane Enchanted (D3), Plaguebearer/Fire Enchanted (D4), Flame Strider trail (PoE-AN), Burning ring (GD) |
| **4. Displacement / Movement-CC** | Pull, push, immobilize, fear, wall, portal | Vortex/Wormhole/Waller/Jailer/Knockback/Nightmarish (D3), Tempest/Hellbound (D4), Extra Fast (D2) |
| **5. Summon / Spawn** | Minion generation, pack augmentation, spawn-on-death | Horde (D3), Summoner (D4), Treant Horde (PoE-AN), death-triggered spawns (various) |
| **6. Resource-Attack** | Mana burn, life leech from player, flask conversion | Mana Burn (D2), Drought Bringer/Vampiric (PoE-AN), Vampiric (D4) |
| **7. Player-Debuff** | Curse, slow, resistance shred, CC aura | Cursed (D2), Malediction (PoE-AN), element Shred (LE), Debilitating Storm (D4) |
| **8. On-Death / Threshold** | Death explosion, death spawn, below-HP threshold activation | Cold/Fire Enchanted death effects (D2), Molten explosion (D3), Berserker threshold (D4), Crackling Soul (D4) |

**Notes for design session:**
- Families 1 and 2 are **stat-layer** (passive; no choreography required; purely math)
- Families 3 and 4 are **spatial-layer** (active choreography; player movement = the counter)
- Family 5 is **encounter-composition-layer** (changes the fight's population mid-combat)
- Families 6 and 7 are **resource-layer** (attacks player's build resources, not HP directly)
- Family 8 is **temporal-layer** (changes fight state based on time or HP threshold transitions)

The genre consensus on readability: Families 1–2 are easiest to telegraph (stat text on nameplate), Family 3 is the most viscerally readable (visible ground), Family 4 is the most emotionally frustrating when opaque (displacement without warning), Families 6–7 are highest-risk for "unfun" if too punishing (Mana Burn bug; Drought Bringer converting loot to flasks).

### 2B — Telegraph Grammar: How Each Game Makes Mods READABLE

Aggregating per-game observations into a consistent grammar model:

**Five telegraph channels used across the genre:**

| Channel | How Used | When It Appears |
|---|---|---|
| **Nameplate text** | Affix/modifier names listed on enemy nameplate; player reads before or during combat | Pre-combat and during |
| **Model visual** | Color tint (elemental), glowing effect, aura ring, translucency (GD Ghostly), star marker | Pre-combat, continuous |
| **Ground indicator** | Pre-AoE decal or warning zone showing where hazard will land before activation | Pre-activation (warning phase) |
| **VFX particle** | Elemental particle system on the enemy model indicating active affix (fire embers, cold crystals, lightning arcs) | Continuous during combat |
| **Audio sting** | Distinct sound on affix ability activation (wall rise, portal spawn, death explosion) | On activation |

**D2 grammar:** Nameplate text + model tint only. No ground indicators. Player learns through death.
**D3 grammar:** Nameplate text + ground indicators + VFX particles + audio. First implementation of the warning-then-damage two-phase spatial telegraph.
**D4 grammar:** Nameplate text + icons + ground indicators + audio + defined cast animations. Adds explicit cast animation (Teleporter's 0.33s telegraph) and icon system.
**PoE AN grammar (the failure):** No in-combat readable tooltip for bundled modifier effects. Nameplate shows modifier name but modifier name did not accurately describe effects. The nameplate channel failed because the text was thematic, not mechanical.
**PoE 3.20 grammar:** Nameplate text returns to mechanical ("Additional Critical Hits") rather than thematic ("Deadeye"). Ground indicators present for spatial abilities. Restores the channel that AN broke.
**GD grammar:** Star above head + archetype name (no combat tooltip). No explicit in-combat modifier text — player reads the star and the name, then learns through experience. Works in a game with 20+ hours of play investment; would fail in a shorter-form game.
**LE grammar:** Red glow + skull-eye minimap icon for Champions (lighter signal for Magic/Rare enemies). Sealed affix coupling means that "reading" the Champion's modifier name gives you the drop prediction, not the combat mechanic prediction. The loot telegraph is the primary value of the name.

**Substrate-relevant implication:** Reincarnated's D7 AI-tell line generates flavor-name lines from substrate. The element vocabulary (fire/earth/water/wind/etc.) can anchor the MODEL VISUAL channel (element-coded glow/tint) and the VFX channel independently of the nameplate text. The nameplate text should express the **functional family** clearly in addition to substrate flavor — the genre shows that flavor-only naming (AN's "Archer") fails; the mechanical descriptor needs to come through even if wrapped in flavor.

### 2C — Roll Budgets: Mods Per Rarity + Lethality Guards

**Mods-per-rarity across games:**

| Game | Magic/Normal+ | Champion/Elite | Rare (Boss) | Unique/Named |
|---|---|---|---|---|
| **D2** | — | Fixed type (1 bundle) | 1 / 2 / 3 (by difficulty) | Fixed preset |
| **D3** | — | 1–4 (level-scaled) | 1–4 (level-scaled) | 2–4 fixed |
| **D4** | — | 2–4 | 2–4 | 2 fixed + random |
| **PoE** (current) | 1–2 | — | 2–4 | — |
| **PoE AN** (3.18) | 1–4 (ambient) | — | 1–4 | — |
| **LE** | 0–1 | 0–2 | 2 (prefix + suffix) | 2 fixed + 1 Champion |
| **GD Hero** | — | 1 archetype | — | — |
| **DI** | — | 1 | 2 | 1–3 |

**Key lethality-stacking guard approaches:**

1. **Category budget caps (D3):** At most 1 defensive AND 1 CC affix; at least 2–3 offensive affixes. Prevents "wall + jail + CC" triple-layer compositions.
2. **Mutually exclusive pairs (D3):** The four displacement/CC affixes (Jailer, Knockback, Nightmarish, Vortex) are mutually exclusive. Prevents double-displacement compositions.
3. **Hardcoded family restrictions (general):** Elemental Enchanted types (Fire/Cold/Lightning) typically cannot co-occur on the same monster in games that use them (prevents "takes fire and cold and lightning damage" monsters that bypass all resistance strategies).
4. **Difficulty gating (D3 / PoE):** Certain affixes only appear at higher difficulty tiers. D3 level-gates affix count (1 at low level → 4 at 60+). PoE uses map tier / area level to control pool availability. LE uses corruption level.
5. **Modifier count cap as lethality proxy:** AN's failure demonstrated that increasing modifier count without individual-modifier complexity reduction is the worst of both worlds. The 3.20 fix inverted this: many simple modifiers allowed, because simple modifier × simple modifier = readable emergent combination.

**The "four-modifier cap" appears near-universal** (D2 at Hell with 3, D3/D4 cap at 4, PoE 3.20 allows up to 4 in maps). This cap exists because:
- Player working memory can hold ~4 combat tasks simultaneously
- More than 4 modifiers statistically guarantee at least one CC-layer and one spatial-layer co-occurring, which exhausts player movement budget

### 2D — Affix↔Loot Coupling

| Game | Coupling Mechanism | Player Decision Point |
|---|---|---|
| **D2** | Boss packs: more minions = more drop rolls. Modifier count on boss is 1/2/3 per difficulty — difficulty itself is the coupling, not specific mods. | "Do I play Hell for better drops?" |
| **D3** | No per-mod loot coupling. Affix count scales with level (more affixes = higher level = better item-level rolls). | "Do I push higher GR for better gems/items?" |
| **D4** | No per-mod loot coupling documented. | — |
| **PoE** (3.20) | Rare monsters with more mods are MORE LIKELY to have hidden reward mods (but player cannot identify which). Loot hidden and revealed on kill. | "Kill everything, don't skip rare packs." |
| **PoE AN** (3.18–3.19) | Direct coupling — specific loot-conversion mods produced specific loot types. Recipe mods yielded specified reward categories. | "Do I have MF character? What do I want to farm?" — BROKE the game |
| **LE** | Champion modifier directly determines Sealed Affix type on drop. 1:1 coupling. | "Which Champion type drops the affix I need?" |
| **GD Nemesis** | Nemesis kill drops from dedicated chest with elevated Epic/Legendary/Blueprint rates. | "Do I want to trigger this faction's Nemesis for its chest?" |

**Design lesson from PoE AN's coupling failure:** When loot conversion is tied to visible, pre-kill-readable modifiers AND requires a different character build (MF) to extract maximum value, the game creates an opt-out incentive for players with non-MF builds. Players either avoid the encounter or feel punished. The 3.20 fix (hide rewards; reveal on kill; all players benefit equally from killing more mods) eliminated the opt-out. The design principle: **loot coupling should CREATE motivation to engage, not CREATE friction for engagement.**

### 2E — Difficulty Scaling: How Affix Pools Widen/Deepen

| Game | Scaling Mechanism | What Changes |
|---|---|---|
| **D2** | Difficulty (Normal/NM/Hell) gates modifier count on bosses (1→2→3) and activates minion inheritance | Modifier quantity + minion behavior |
| **D3** | Player level gates affix count (1 at low level → 4 at 60+); Torment/GR levels scale monster HP/damage but not affix pool width | Count scales; pool stays constant |
| **D4** | World tier gates elite tier availability; affix count fixed at 2–4 regardless of tier in documented sources | Tiers unlock harder encounter types |
| **PoE** | Map tier (1–16+) scales rare monster modifier count (1–2 in acts; 2–3 in early maps; 3–4 in endgame maps) and pool width (some mods only appear in high-tier maps) | Both count AND pool |
| **LE** | Corruption level in Monolith scales Champion density and increases overall elite spawn rates | Density, not pool width per Champion |
| **GD** | Reaching Nemesis reputation unlocks Nemesis spawns; Hated reputation increases hero spawn frequency | Encounter TYPE available changes |

**The "threat tier" axis implication for Reincarnated:** This is the axis that determines which affix pools are available at which encounter difficulty. Every game in the genre uses some form of "higher difficulty → broader/deeper affix pool." The key question for the design session is whether Reincarnated's threat tiers (already established) directly map to affix-pool-bracket gates.

---

## §3 — Substrate-Mappability Hooks

**Elements with clear existing substrate homes:**

| Canon Element | Existing Reincarnated Substrate Axis | Mapping Note |
|---|---|---|
| X-Enchanted modifier family (Fire/Cold/Lightning/Poison equivalents) | Element vocabulary (fire/earth/water/wind/etc.) | Direct 1:1: each element gets its own "Enchanted" modifier in the terrain-denial family. The element name IS the modifier's label anchor. |
| Modifier count by rarity tier (1/2/3 per difficulty) | Threat tiers | Higher threat tier = more mods per mob; the tier bracket determines the affix-count budget. |
| Archetype-locked mods (GD's faction-aligned archetypes) | Archetype pools (damage/support/control/hybrid) | Archetype pools can constrain which affix families roll on a given mob's archetype. A support-archetype mob should get summon/spawn and player-debuff families; damage-archetype mob gets damage-add and terrain-denial. |
| Flavor-name generation for mod names | Glyph/flavor substrate + D7 AI-tell line | Names are substrate-derived, not hand-authored. The element vocabulary + archetype pool + functional family become the three inputs to name generation. |
| Loot coupling (Champion = specific drop type) | Gear/element/archetype coupling already in engine | Champion modifier coupling to a specific gear affix type mirrors existing gear-affix architecture. |
| On-death / threshold modifiers | Combat state machine (fight outcome telemetry) | HP threshold detection and death-event hooks are already instrumented for combat logging; these same hooks support modifier triggers. |

**Elements with NO current substrate home (hard questions for the design session):**

| Canon Element | Gap | Design Session Question |
|---|---|---|
| Minion inheritance rules (which mods pass to pack members) | No current pack-composition / minion-inheritance schema | Does Reincarnated's content encounter system model monster packs as a unit, or as individual mobs? If individual, minion inheritance has no natural home. |
| Banned modifier pairs (Vortex ≠ Knockback) | No affix exclusion/ban-pair system | How are incompatible modifier combinations prevented? Code-level constraint table? Or handled by the archetype-pool filtering being restrictive enough to make the problem rare? |
| Loot-conversion modifiers (PoE AN lesson: avoid in ambient) | No loot-conversion-modifier concept in current design | Should any modifier affect drop TYPE (not quantity)? The genre lesson strongly suggests: only in opt-in contexts. |
| Displacement modifier spatial implementation (Waller, Vortex) | No terrain generation for spatial modifiers | Reincarnated's current room architecture: does it support dynamically-spawned blocking geometry (walls)? Does it support "pull player toward point" physics? |
| Temporal state transitions (Berserker < 50% HP trigger) | No multi-phase mob state machine documented | Is a combat-phase state machine in scope for E10, or is that reserved for boss-class encounters? |
| Session-persistent named rival tracking (GD Nemesis "once per session") | No rival-persistence system yet | How does the RIVAL class track whether a specific named rival has already spawned this session? Needs a session-scope persistence hook. |
| Named rival kit construction from certified-non-rostered kits (E9-C) | Kit-built encounter system not yet built | How does the RIVAL class select from the certified-non-rostered archetype pool? What is the selection grammar? |

---

## §4 — Failure-Mode Appendix

### F1 — Archnemesis: The Over-Complexification Failure (PoE 3.17–3.19)

**Timeline:** League mechanic (3.17, Feb 2022) → Core integration (3.18, May 2022) → Community revolt → Iterative patches → Full dismantling (3.20, Dec 2022)

**Failure Axis 1 — Modifier Opacity:**
Modifier names were thematic labels ("Archer," "Magma Barrier," "Deadeye") that each concealed 3–6 distinct mechanical effects. There was no in-combat accessible description. Players literally could not know what a modifier did from its name without consulting a third-party wiki. GGG's own acknowledgment (3.20 Manifesto): "The keyworded mod names were not fully descriptive of what they did."

**Failure Axis 2 — Bundled Effect Stacking:**
Because each modifier contained multiple effects, a 3-modifier rare monster might have 12–18 simultaneous effects. Some of these effects interacted multiplicatively (damage conversion + damage bonus + resistance grant all in one modifier). The emergent lethality spikes were not predictable from reading the nameplate. GGG: "Due to how many effects were included in a single mod, it made too many encounters too complex."

**Failure Axis 3 — Loot Conversion in Ambient Encounters:**
Loot-conversion modifiers (Drought Bringer → flask-only drops; Innocence-touched → scarabs) were designed for opt-in contexts where players built the monster intentionally. In ambient encounters, these modifiers produced punishing loot outcomes with no player agency over whether the encounter occurred. GGG's Bex: "there is a fair bit of team agreement around it feeling bad."

**Failure Axis 4 — Effective Ele-Reflect via Mod Interaction:**
Certain modifier combinations produced effective damage reflection. Elemental reflect has been independently identified as one of the ARPG genre's most hated mechanics across D3 (Reflects Damage), PoE (Ele Reflect map mod), and elsewhere — because high-DPS builds are punished most severely by the mechanic that rewards good play (dealing high damage). AN enabled this via opaque modifier combinations, making it unpredictable and build-invalidating.

**Failure Axis 5 — Recipe Compulsion in Opt-Out Design Space:**
The AN league mechanic worked because players CHOSE to combine modifiers. When the same modifier system was applied to all ambient rare monsters, the "recipe combination" mental model was no longer applicable — but the reward associations from the league persisted (certain mods "should" drop certain items). This created friction where players evaluated mobs for their reward before engaging and sometimes skipped encounters. GGG's fix in 3.20: hide rewards completely; remove the selection-rationalization loop.

**Resolution anatomy (3.20):** One modifier, one effect, self-descriptive name, hidden reward system. "Magma Barrier" becomes exclusively "magma barrier creation, nothing else." Rewards hidden until kill. This is the direct inversion of AN's five failure axes.

---

### F2 — Reflects Damage: The Unavoidable-Damage Failure (D3 original → patch 1.07 → eventual removal)

**Original mechanic:** When a D3 elite had Reflects Damage, a percentage of all damage the player dealt was reflected back as damage to the player. The reflect was triggered when the monster displayed an orange glow (active reflection window).

**Failure Axis 1 — Punishes Optimal Play:**
High-DPS builds received more reflected damage per second than low-DPS builds. The mechanic explicitly penalized optimal play: the better you were at dealing damage, the more damage you received from reflection. This is the opposite of what engaging ARPG design requires (skills should create rewards, not punishments).

**Failure Axis 2 — Pet/Summon Interaction:**
Pet and minion damage originally reflected to the PLAYER, not the minion. This meant summoner-class builds received reflected damage from all summon damage — an invisible source of incoming damage with no counterplay (you cannot "dodge" your own minions' damage).

**Failure Axis 3 — Unavoidable Window:**
Unlike terrain-denial affixes where the player moves, Reflects Damage offered no spatial counterplay. The only valid counter was to stop attacking (or die). In a game designed around non-stop combat action, stopping attacking voluntarily is a non-fun solution.

**Blizzard's fix (Patch 1.07):** Changed Reflects Damage to a periodic buff (orange glow = reflection window active; no glow = safe to attack). The orange-glow telegraph created a timing window. Pet damage no longer reflected to player. This was the "temporal telegraph" fix — adding a time-window to make the mechanic survivable.

**Post-fix fate:** Reflects Damage persisted but was reduced in intensity. It was eventually removed from D4's affix pool entirely. D4 does not contain any analogue affix.

**Design lesson:** Pure damage reflection is a structural anti-pattern in ARPGs because:
- It punishes the player's core action (dealing damage)
- It benefits builds that deal LESS damage (anti-optimization incentive)
- It produces unavoidable damage in the absence of strong temporal telegraphing
- The only valid spatial counter is standing still, which negates the game's movement design

Any mechanic in the Resource-Attack family that draws from the player's primary combat action (vs from a secondary resource like mana) must be carefully bounded.

---

### F3 — Mana Burn Bug (D2) — Resource-Attack Scaling Failure

**Mechanic:** Mana Burn drained player mana equal to 4× the damage dealt. At a programmatic level, a coding error multiplied the drain by 256 — effectively draining the entire mana bar on any hit from a Mana Burn boss in Hell difficulty.

**Failure axis:** Resource-attack modifiers that interact with the player's ability to cast skills create a "can't fight back" loop if too severe. If the resource being drained (mana) gates the player's ability to deal damage, and the drain outpaces recovery, the player is locked out of their primary ability loop.

**Why it was kept:** Despite the bug, Mana Burn became iconic identity for Hell difficulty in D2 — the moment players encounter Mana Burn bosses forces them to have mana potions, mana leech gear, or low-mana-cost builds. It became a build-check rather than a frustration (at high levels where players are prepared). It was never fixed in the original D2 because it was retained as "authentic D2 Hell difficulty."

**Design lesson:** Resource-attack modifiers can be interesting (they create resource-management counterplay loops) but MUST NOT scale into instant-drain territory. The drain rate needs a ceiling that keeps the fight winnable.

---

## §5 — Secondary Thread: Named-Monster / Rival Conventions

### 5A — Path of Exile — Rogue Exiles (Direct RIVAL Precedent)

The Rogue Exile system is the closest genre precedent to Reincarnated's E9-C RIVAL class concept:
- **Kit grammar:** Rogue Exiles are built on the player-character system. They use player skills, carry player-valid unique items, have player-equivalent stat distributions. The hostile encounter is mechanically indistinguishable from fighting a human player.
- **Announcement:** Name on nameplate. No pre-encounter cutscene. The threat is discovered through exploration, not scripted.
- **Naming convention:** Real-name-style names (not epithets): "Exile" is the category; individual names are human character names. In PoE 2, each Rogue Exile is a named character with backstory fragments.
- **Persistence mechanic (PoE 2):** If the Rogue Exile kills you, they portal out forever. This makes every encounter high-stakes — failure has a permanent consequence.
- **Loot coupling:** They carry the unique items they're built with; those items can drop.

**RIVAL class implication:** E9-C's "other reaped souls on the same descent" framing maps exactly to the Rogue Exile model. A rival is a certified-kit-built character from the same "game space" as the player, encountered as a hostile. The kit-build grammar is the same grammar; the opposition is the relationship.

### 5B — Grim Dawn Nemesis — Reputation-Triggered Named Pursuer

Already covered in §1.6C above. The key RIVAL-class feed from Nemesis:
- **Trigger grammar:** The player's actions (killing faction members) summon the named pursuer. The rival is caused by player behavior, not random encounter.
- **Naming convention:** "[Name], [Evocative Epithet]" — thematic, not mechanically prescriptive. "Moosilauke, the Chillwind" is memorable without being a mechanic spoiler.
- **Announcement:** Nameplate name appears when the boss spawns. No advance warning — discovery is encounter-in-progress.
- **Session scope:** Once per session per faction. Makes each encounter feel like an event.

### 5C — Diablo III — Keywardens (Named Fixed Elite Sub-Bosses)

Keywardens (Odeg, Sokahr, Xah'Rith, Nekarat) are Super Unique named elites in each act with:
- Fixed spawn zone (random within zone, not fixed room)
- Fixed preset of 2–3 affixes (e.g., Odeg has Jailer + Knockback + Molten; Sokahr has Vortex + Missile Dampening)
- Fixed-affix design means experienced players know what to expect before engaging (Odeg = jail-safe corner; Sokahr = melee-close immediately)
- **Loot coupling:** Keys of Destruction/Hate/Terror on Inferno, probability-scaled with Monster Power; 100% drop at MP10

**RIVAL-class implication:** Named encounters with fixed/semi-fixed affix loadouts are distinguishable from ambient elites by predictability. Players develop named-encounter-specific strategies. The naming + fixed-affix combination creates "boss personality."

### 5D — Isekai Conventions: Floor Boss + Named-Encounter Announcement Grammar

**Solo Leveling gate/rank system:**
- Gates are ranked E through S (S = rarest, most dangerous); the rank itself is the primary danger telegraph before the encounter
- Named within-gate bosses have title-epithets: "Blood-Red Commander Igris" — a title that describes both the threat color/element (Blood-Red → crimson/physical) and the class (Commander). Jinwoo re-names Igris after defeating and claiming him as a shadow — the act of naming confers identity shift.
- Boss rooms are preceded by a "boss room approach" beat (door, environmental change, buildup) rather than a sudden encounter

**Sword Art Online floor bosses:**
- 100-floor structure; each floor has a named raid boss
- Boss names are typically fantasy-compound with difficulty signaling in the naming tier (floor 1 boss is simpler to pronounce/shorter than floor 75 boss)
- Players must reconnaissance (scout) the boss before strategy is possible — the scouting encounter and the kill encounter are separated

**That Time I Got Reincarnated as a Slime — naming as identity:**
- Receiving a True Name triggers evolution — combat identity and power fundamentally shift around the name
- Names create faction allegiance (named → bound to namer)
- Naming is a player-action mechanic, not a system label

**Design implication for RIVAL class announcement grammar:**
The genre convention across both Western ARPG and isekai sources converges on: **title-epithet at first encounter → personal-name on defeat/claim**. The rival is announced by a descriptive title ("The Unbroken Flame-Herald" / "the Chillwind") that hints at combat archetype without mechanically spelling it out; upon defeat or repeated encounter, the name becomes familiar and identity-associated. This maps to a two-stage naming grammar for Reincarnated's RIVAL class encounters.

---

## Source List

### Primary Sources (developer posts, official documentation)
- GGG Official Forum: "What's Next for Archnemesis Modifiers - Part 3" (3.19, 2022) — https://www.pathofexile.com/forum/view-thread/3267228
- GGG Official Forum: "3.20 Balance Manifesto: Monster Mods and Archnemesis" — https://www.pathofexile.com/forum/view-thread/3322245 (also at https://steamcommunity.com/games/238960/announcements/detail/3444719198700219528)
- GGG Official Forum: "Nerfing Defensive Archnemesis Modifiers" (3.19.0f) — https://www.pathofexile.com/forum/view-thread/3299347
- Blizzard Official: Diablo 3 Patch Notes — https://us.diablo3.com/en/game/patch-notes/
- Arreat Summit (Blizzard official D2 documentation): Monster Bonuses — https://classic.battle.net/diablo2exp/monsters/bonus.shtml
- Grim Dawn Official Monsters Guide — https://www.grimdawn.com/guide/gameplay/monsters/
- Grim Dawn Official Factions Guide — https://www.grimdawn.com/guide/character/factions/
- Blizzard News: Diablo Immortal Technical Alpha — https://news.blizzard.com/en-us/diablo-immortal/23785115
- Blizzard D4 Elite Affix Overview — https://www.wowhead.com/diablo-4/news/elite-boss-affixes-overview-for-diablo-iv-now-live-hellbound-plaguebringer-332154

### Secondary Sources (community wikis, guides, analysis)
- Maxroll D2 Elite Monster Guide — https://maxroll.gg/d2/resources/elite-monster
- Wowhead D2R Boss Attributes Guide — https://www.wowhead.com/diablo-2/guide/unique-boss-attributes-abilities-immunities
- Maxroll D3 Elite Affixes — https://maxroll.gg/d3/resources/elite-affixes (via d3planner mirror)
- Blizzardwatch D3 Elite Affix Combat Guide — https://blizzardwatch.com/2015/07/11/combat-elite-monster-affixes-diablo-3/
- DiabloWiki Boss Modifiers — https://www.diablowiki.net/Boss_Modifiers
- Fextralife D4 Elites — https://diablo4.wiki.fextralife.com/Elites
- Diablo4.gg Elite Affixes — https://diablo4.gg/diablo-4-elites-affixes/
- VHPG PoE Archnemesis Changes 3.19 — http://www.vhpg.com/poe-archnemesis-changes/
- PCGamesN Archnemesis Frustration Coverage — https://www.pcgamesn.com/path-of-exile/archnemesis-system
- Guided.news Archnemesis Removed in 3.20 — https://guided.news/en/gaming/path-of-exile-archnemesis-removed-in-3-20/
- PoE Wiki Rogue Exile — https://www.poewiki.net/wiki/Rogue_exile
- Mobalytics PoE 2 Rogue Exiles — https://mobalytics.gg/poe-2/guides/rogue-exiles
- Last Epoch Maxroll Champions — https://maxroll.gg/last-epoch/resources/champions
- IGGM Season 2 Champion Affixes — https://www.iggm.com/news/last-epoch-season-2-what-benefits-do-all-champion-affixes-provide
- Grim Dawn Nemesis Guide (SlashingCreeps) — https://slashingcreeps.com/en/grim-dawn/nemesis/
- Grim Dawn Nemesis Locations (SteamAH) — https://steamah.com/grim-dawn-nemesis-locations-guide/
- Massively Overpowered: Grim Dawn Nemesis Overhaul 2024 — https://massivelyop.com/2024/06/24/grim-dawn-overhauls-nemesis-boss-spawns-tweaks-physical-resistance-and-rebalances-pets/
- DiabloHub D3 Monster Traits — https://www.diablohub.com/guides/monster-traits-description/
- Diablo Fandom Monster Traits DI — https://diablo.fandom.com/wiki/Monster_Traits_(Diablo_Immortal)
- Gamepur AN Modifier Recipes — https://www.gamepur.com/guides/all-archnemesis-modifier-recipes-in-path-of-exile
- PureDiablo Reflects Damage Patch — https://www.purediablo.com/diablo-3-patch-monster-changes-reflects-damage
- DiabloWiki Reflects Damage — https://www.diablowiki.net/Reflects_Damage
- Diablo Fandom Keywarden — https://diablo.fandom.com/wiki/Keywarden

### Tertiary Sources (community discussion, supplementary)
- Gamefaqs D2 Thief modifier thread — https://gamefaqs.gamespot.com/boards/605432-path-of-exile/80040199
- Diablo Fandom Thief modifier — https://diablo.fandom.com/wiki/Thief
- Devtrackers GGG Archnemesis statement — https://devtrackers.gg/pathofexile/p/c9e61148
- Solo Leveling Fandom Igris — https://solo-leveling.fandom.com/wiki/Blood-Red_Commander_Igris
- Tensei Slime wiki Names — https://tensura.fandom.com/wiki/Name

---

*Research complete: 2026-07-08. Findings return to gandalf (design steward) for E10 Leg 2 design session with Matt.*
