# Research — Monster/Enemy-Combatant Sprite Vendor Scout — 2026-05-16

**Mode:** A (analytical)
**Commissioner:** knight-rider (Pattern A dispatch, Matt-authorized 2026-05-16 — closes monster/enemy-combatant gap)
**Approved by:** Matt (2026-05-16)
**Sources consulted:** itch.io vendor pages (direct fetch), CraftPix.net product pages, Unity Asset Store, GameDevMarket (partial — 403 on direct product fetch), web search sweeps across multiple query vectors
**Style register target:** Hand-drawn pixel-art, HD-2D-shaped (per `canonical/story/style-register.md`, locked 2026-05-15)
**Architecture reference:** `canonical/story/enemy-visual-legibility.md` — six monster archetypes (brute / caster / controller / sniper / swarmer / tank) + six perceptual axes (tier, element, archetype, trial-encounter, mirror, pack-vs-individual)
**B11/B13 mechanic-pairing filter:** Knockback-recipient animations, cast/channel states, summoning states, leap attacks scored high

---

## Summary (4 sentences)

Eight candidate monster/enemy-sprite vendors are surfaced spanning the full ARPG monster taxonomy: Elthen's Pixel Art Shop is the single most important finding — a 200+ pack catalogue with confirmed hand-drawn pixel-art boss sprites at 96x96 to 320x128 pixel dimensions, covering undead, humanoid, beast, elemental, and boss archetypes across thematic bundles, with a license gate (Patreon-only terms) that requires resolution before purchase. CreativeKind (already a Tier-1 VFX vendor) extends naturally into the monster track with hand-drawn pixel enemies at 168-176px dimensions — Lich ($9) and Crystal Golem ($4.50) are immediate candidates that share the register already confirmed for this project. MonoPixelArt offers a tight multi-pack catalogue (six packs: skeletons, golems, forest monsters, dark fantasy enemies, flying monsters, free character) with confirmed 64-90x96 dimensions, CC-style custom license, and no-AI declarations across all packs. The most significant register and license findings: CraftPix monster sprites confirm as true pixel art (PSD/PNG formats, 128-256px) but carry the same subscription cost model flagged in the character-track scout; OcO Medieval Fantasy packs vary register by series (Pack 1 is 64x64 retro; Pack 3 is 128x128 HD); GandalfHardcore's enemy catalogue is retro 32px register and is excluded from HD-2D recommendations.

---

## Findings

### Vendor 1 — Elthen's Pixel Art Shop (monster catalogue)

**URL:** https://elthen.itch.io/
**Platform:** itch.io
**Cost:** $3–$10 per pack; thematic bundles $20–$25 for 5-7 packs; per-pack pricing reviewed on individual pages
**License:** Custom terms referenced via Patreon link (https://www.patreon.com/posts/27430241). Page-text standard: "You can read about licensing here!" — Patreon link is required for full terms. Patreon page returned 403 during this scout session.
**License flag:** HOLD — license terms are Patreon-gated. Patreon fetch returned 403 (authentication wall). Cannot confirm commercial-use terms from public sources. Individual pack pages reviewed confirm "No generative AI was used" and do confirm commercial use in item descriptions (e.g., Minotaur: "Feel free to use the sprites in commercial/non-commercial projects"), but full standardized terms not publicly accessible without Patreon auth. This is the same HOLD pattern flagged in the character-track scout for Elthen. Recommend: navigate to the Patreon post directly in a browser session and confirm terms before purchase. Historical context from character-track scout: other Elthen packs (Adventurer, Squire) confirmed "commercial/non-commercial use permitted, modification permitted" — terms appear consistent but per-pack verification is required.

**Monster catalogue scope:** 200+ individual packs organized into thematic bundles:

| Bundle / Category | Monster Types | Representative Packs | Price Range |
|---|---|---|---|
| Undead #1, #2, #3 | Combusted, Mummy Brute, Ghost Townsfolk, Rotting Soldier, Skeletal Trumpetist, Lich | Lich ($6), Rotting Soldier, Mummy Brute | $5–$7 |
| Demons | Hell Guard Demon, Demon Piglet, Succubus, Abyssal Chicken | Hell Guard Demon ($5) | $3–$5 |
| Dragons | Elder Dragon, Drake, Faerie Dragon, Phoenix, Dragon Hatchling | Elder Dragon ($10), Dragon Hatchling ($3) | $3–$10 |
| Goblins | Loot Goblin, Kamikaze Bomber, Gunner | Various | $2–$5 |
| Orcs | Kid, Brute, Kamikaze Bomber, Warlock | Various | $3–$4 |
| Bandits | King, Mage, Trapster, Necromancer, Slingshot | Bandit King ($5) | $3–$5 |
| Construct/Golems | Multiple golem types, Guardian Scroll | Various | $1–$6 |
| Elementals | Fire, Wind, Shadow elementals, Mudling | Wind Elemental ($5) | $1–$5 |
| Cultists | Multiple cultist variants with transformation | Shadow Host Cultist ($5) | $5–$6 |
| Insects/Arachnids | Beetles, Spiders, Ticks, Scarabs | Spider Queen ($7) | $1–$7 |
| Aberrations | Werewolf ($7), Hill Giant ($7), Bridge Guard Troll ($7) | Boss-tier | $7 |
| Fishfolk / Frogfolk / Lizardfolk | Warrior classes + king variants | Octopus King ($6) | $1–$7 |

**Confirmed boss-tier packs with dimensions:**

*Lich Sprites ($6):*
- Sprite dimensions: 192x160 pixels
- Animation states: Idle/Movement, Prepare Spell, Cast x2, Damage, Death
- Notes: Large boss-class undead caster; confirmed "Prepare Spell" + "Cast x2" = B11 vortex/AOE channel analog
- File format: PNG + JSON

*Minotaur Sprites (free/NWYP):*
- Sprite dimensions: 96x96 pixels
- Animation states: Idle, Move, Taunt, Attack1-4, Damage1-2, Death (10 total)
- Notes: 96x96 at 10 states — strong brute-archetype candidate
- File format: PNG (101 kB)

*Hill Giant Sprites ($7):*
- Sprite dimensions: 320x128 pixels
- Animation states: Idle, Movement, Attack, Damage, Death
- Notes: 320x128 is a massive boss-tier canvas; appropriate for Trial encounter / act-boss tier
- File format: PNG + JSON

*Werewolf Sprites ($7):*
- Sprite dimensions: 160x64 pixels (beast form); 32x32 (human form)
- Animation states: Idle, Movement, Attack, Damage, Howl, Death, Transform
- Notes: Transform animation = elemental-transformation analog; Howl = channel/taunt state
- File format: PNG + JSON

*Dragon Hatchling Sprites ($3):*
- Sprite dimensions: Not confirmed from fetch (small pack, ~34 kB)
- Animation states: Idle, Move, Attack, Damage, Death
- Notes: Entry-level dragon; lower price suggests smaller canvas

**B11/B13 mechanic-pairing:**
- Lich "Prepare Spell" + "Cast x2" = direct caster-archetype coverage; AOE-channel analog
- Hill Giant at 320x128 = AOE-tank candidate (massive footprint = area-control presence)
- Werewolf "Transform" = trigger-animation for elemental-shift or phase-change mechanics
- Minotaur 10 states including multiple attacks = brute-archetype scripted-sequence coverage

**Style register assessment:** STRONG HD-2D-pixel match. Confirmed dimensions range from 96x96 (Minotaur) to 320x128 (Hill Giant) to 192x160 (Lich). Character-track scout confirmed Elthen's Adventurer (32x32) as retro-register; the monster catalogue operates at a significantly higher dimension range per the fetched boss-packs. The monster catalogue's upper tier (Lich, Hill Giant, Hill Giant, Werewolf) is firmly in the HD-2D pixel register range. The lower-tier packs (Dragon Hatchling at ~34 kB, smaller enemy types) may be at smaller dimensions — verify per-pack before purchase.

**Decomposition:** Monolithic sprite sheets (PNG + JSON pairs). Not paper-doll. Each monster is a self-contained animated sheet.

**AI-content signal:** "No generative AI was used" confirmed on all fetched packs.

**Per-product-line deliverable_register field (Drift-13):**
- Boss-tier line (Lich, Hill Giant, Werewolf, Minotaur): HD-2D-pixel confirmed from dimensions
- Mid-tier line (Dragon Hatchling, Cultists, Bandit types): dimensions not confirmed; infer from pack size
- Lower-tier line (Demon Piglet, Abyssal Chicken, small insect variants): likely retro-pixel register; DO NOT assume HD-2D without per-pack dimension verification

**Sample SKUs:**
- Minotaur Sprites (free/NWYP): 96x96, 10 animations, brute archetype
- Lich Sprites ($6): 192x160, 5 animation groups, caster/boss archetype
- Hill Giant Sprites ($7): 320x128, 5 animations, boss/tank archetype
- Werewolf Sprites ($7): 160x64, 7 animations including Transform
- Dragon Hatchling ($3): dimensions unconfirmed, 5 animations
- Undead Bundle #3 ($20): includes Lich + 4 additional undead packs

**Notes for downstream:** Elthen is the single deepest monster-sprite catalogue at the HD-2D register available on itch.io. The boss-tier packs (Lich, Hill Giant, Werewolf) are the highest-value items. The thematic bundle structure makes targeted purchasing economical — Undead Bundle for undead archetype, Bandits/Orcs/Goblins bundles for humanoid archetype, Dragons Bundle for boss-class flying. License HOLD is the primary risk: Patreon-gated terms must be resolved before purchase. Elrond should flag this in the viability-gate structural review.

---

### Vendor 2 — CreativeKind (monster/enemy line)

**URL:** https://creativekind.itch.io/
**Platform:** itch.io
**Cost:** $2.70–$9.00 per pack; bundle $84.99 for 26+ packs; standard discount ~10% currently active
**License:** Commercial and non-commercial use permitted; customization allowed; redistribution/resale prohibited. License stated on product pages, not CC-labeled but clear custom statement. Not Patreon-gated.
**License flag:** VERIFY — custom non-CC statement (same pattern as other Tier-1 itch.io vendors). Terms confirm commercial use; no attribution requirement found. Provisionally clear.

**Context:** CreativeKind is already a confirmed Tier-1 VFX vendor in the 9-vendor Step B catalogue. The monster track extends the same vendor into the enemy-sprite domain. Style register is confirmed hand-drawn pixel style matching the VFX packs.

**Monster/enemy packs confirmed:**

*Lich ($9, on sale from $10):*
- Sprite dimensions: 176x128 pixels
- Animation states: Idle (16fr), Short Spin Attack (16fr), Short Spin + Symbols (16fr), Long Spin Attack (32fr), Long Spin + Ghosts (32fr), Long Spin + Symbols (32fr), Third Attack (16fr), Fourth Attack (16fr), Casting (29fr), Hurt (2fr), Death (12fr)
- Total animations: 10 sequences; Casting is explicit = caster-archetype coverage
- Notes: Boss-class undead caster at 176x128; 4 color variations; casting + extended combo attacks = Trial encounter tier
- File format: ZIP (4.2 MB)
- AI-content: "No generative AI was used"

*Crystal Golem ($4.50, on sale from $5):*
- Sprite dimensions: 168x141 pixels
- Animation states: Idle (8fr), Run (8fr), Attack 1 (12fr), Attack 2 (12fr), Death (12fr)
- Notes: Construct/tank archetype at 168x141; 4 color variations; no cast state
- File format: ZIP (347 kB)
- AI-content: "No generative AI was used"

*Additional enemy packs (not individually fetched; dimensions unconfirmed):*
- Fire Elemental ($7.20): magical elemental archetype
- God Of Lightning ($7.20): magical elemental / boss archetype
- Fire Lord ($9): humanoid elemental boss archetype
- Mutant Skeleton ($4.50): undead archetype
- Demon Mage ($4.50): humanoid caster/dark archetype
- Hellfire Rhino ($4.50): beast archetype
- Animated Boss Character ($4.50): generic boss archetype
- Skull Monster ($2.70): undead / beast archetype
- Dark Soul Character ($3.15): dark humanoid archetype

**Coverage vs monster archetype taxonomy:**
- Brute/Tank: Crystal Golem (confirmed), Hellfire Rhino (inferred)
- Caster/Controller: Lich (confirmed casting), Demon Mage, Fire Lord, God of Lightning
- Undead: Lich, Mutant Skeleton, Skull Monster
- Magical: Fire Elemental, God of Lightning, Crystal Wisp
- Boss: Lich, Fire Lord, God of Lightning, Animated Boss Character
- Humanoid: Fire Lord, NightBorne Warrior (free, confirmed in character-track)
- Beast: Hellfire Rhino (inferred); beast archetype is weakest category

**B11/B13 mechanic-pairing:**
- Lich "Casting" (29fr) = long AOE-channel animation at caster tier
- Crystal Golem "Attack 1" + "Attack 2" = two-attack-phase tank behavior
- God of Lightning (unverified states) = potential AOE / lightning-strike state candidate

**Style register assessment:** CONFIRMED hand-drawn pixel style. Lich at 176x128 and Crystal Golem at 168x141 are firmly in the HD-2D-pixel register. These dimensions are the highest in the current scout. The hand-drawn illustration sensibility was established in the Step B VFX research for CreativeKind. Cross-register coherence with VFX packs already confirmed for this project is a significant operational advantage — enemy sprites and VFX effects from the same vendor have matching style registers, eliminating within-frame mixing risk.

**Decomposition:** Monolithic ZIP per pack. No paper doll.

**Per-product-line deliverable_register field (Drift-13):**
- Boss-tier line (Lich, Fire Lord, God of Lightning): HD-2D-pixel confirmed on Lich; inferred on others from vendor register consistency
- Mid-tier line (Crystal Golem, Fire Elemental, Demon Mage): HD-2D-pixel inferred from vendor register and Golem confirmed dimension
- Low-cost line (Skull Monster $2.70, Dark Soul $3.15): dimensions unconfirmed; may be smaller canvas; verify before assuming register match

**Sample SKUs:**
- Lich ($9): 176x128, 10 animation sequences, caster/boss, 4 color variants
- Crystal Golem ($4.50): 168x141, 5 animations, tank/construct, 4 color variants
- Fire Elemental ($7.20): dimensions unconfirmed, elemental archetype
- Hellfire Rhino ($4.50): dimensions unconfirmed, beast archetype
- Bundle ($84.99): 26+ packs including both enemy and VFX packs

**Notes for downstream:** CreativeKind's cross-track coherence (VFX already Tier-1 + monster sprites confirmed matching register) is the strongest operational argument for this vendor. Purchasing monster sprites from CreativeKind alongside the VFX packs eliminates within-frame style-register mixing at zero additional pipeline cost. The beast-archetype gap (Hellfire Rhino is the only candidate; not individually fetched) is a known gap to verify. Drax should confirm Pixi.js wiring viability from the monolithic ZIP format — same question applies to all CreativeKind assets.

---

### Vendor 3 — MonoPixelArt (multi-pack monster catalogue)

**URL:** https://monopixelart.itch.io/
**Platform:** itch.io
**Cost:** Free base tier (mushroom, 1 skeleton, 1 golem, char); $3–$4 premium (3 skeletons, 3 golems, full monster set); Dark Fantasy pack $4 premium
**License:** Custom on-page statement: "Feel free to use this asset pack in any project, commercial or not, but refrain from reselling, redistributing, or modifying it." Confirmed across Forest Monsters, Dark Fantasy Enemies, Skeletons, and Golems packs.
**License flag:** VERIFY — custom non-CC statement consistent across packs. Commercial use permitted; modification restricted. No Patreon gate. Provisionally clear.

**Pack catalogue (confirmed via direct fetch):**

*Forest Monsters 2D Pixel Art (NWYP / $4 premium):*
- Monsters: Mushroom (80x64), Slime (64x64), Bush Monster (90x64)
- Animation states (Mushroom): Idle, Hurt, Die, Run, Attack, Attack with Stun, Stun (7 states)
- Animation states (Slime): Idle, Hurt, Die, Run, Idle Jump, Run Jump, AttackGround, Air Hurt, Air Die (9 states)
- Animation states (Bush Monster): Idle, Hurt, Die, Run, Attack, AttackTimeFrame (6 states)
- Notes: Beast + magical creature archetypes; Slime jump = mobility analog; AttackTimeFrame = timed AOE window
- AI-content: "No generative AI was used"

*Dark Fantasy Enemies 2D Pixel Art (NWYP / $4 premium):*
- Monsters: Bat (64x64), Ghost Warrior (100x64), Evil Creature (90x64)
- Animation states (Bat): Idle fly, Fly, Hurt, Die, Attack1, Attack2, Idle Sleep, Wake up (8 states)
- Animation states (Ghost Warrior): Idle, Fly/Run, Hurt, Die, Spawn, Attack1, Attack2 (7 states)
- Animation states (Evil Creature): Idle, Walk, Hurt, Die, Attack1, Attack2, Spawn-Teleport, Escape-Teleport (8 states)
- Notes: Undead/dark archetype; Ghost Warrior "Spawn" = summoning/emergence state; Evil Creature "Teleport" = displacement/iframe analog
- AI-content: "No generative AI was used"

*Pixel Art Skeletons Pack (NWYP / $3 premium):*
- Monsters: 3 skeleton types (sword, halberd, sword+shield) — premium
- Sprite dimensions: 64x96 pixels
- Animation states: Idle, Hurt, Die, Walk, Attack1, Attack2 (6 states)
- Notes: Classic undead archetype; 64x96 at 6 states matches enemy-visual-legibility trash/elite tier
- AI-content: "No generative AI was used"

*2D Pixel Art Golems Asset Pack (NWYP / $4 premium):*
- Monsters: 3 golems (premium) including crystal variants
- Animation states: Idle, Hurt, Die, Walk/Fly, Attack, Teleportation (flying golem)
- Notes: Construct archetype; flying golem has Teleportation state = displacement analog; created with Aseprite
- AI-content: "No generative AI was used"

*Flying Forest Monsters 2D Pixel Art (NWYP / ~$4):*
- Monsters: flying creature variants
- Dimensions: not confirmed (pack page returned 404)

**Coverage vs monster archetype taxonomy:**
- Brute: Bush Monster (inferred)
- Caster/Controller: Evil Creature (teleport), Ghost Warrior (spawn)
- Sniper: none confirmed
- Swarmer: Bat (multiple attack states; sleep/wake suggests pack behavior)
- Tank: Golem (confirmed)
- Undead: Skeletons (confirmed), Ghost Warrior (confirmed)
- Beast: Slime (confirmed), Mushroom (confirmed), Bush Monster (confirmed)
- Magical: Golems (confirmed), Evil Creature
- Boss: none confirmed boss-tier within this catalogue; Ghost Warrior is mid-tier

**B11/B13 mechanic-pairing:**
- Evil Creature "Spawn-Teleport" + "Escape-Teleport" = displacement/vortex analog; combatant can enter and exit engagement zones
- Slime jump states = mobility/leap analog
- Ghost Warrior "Spawn" = emergence animation for B11 wave-spawning mechanic
- Golem flying + Teleportation = spatial repositioning animation

**Style register assessment:** CONFIRMED hand-drawn pixel art. Dimensions 64x64 to 100x64 to 64x96 span the mid-to-HD pixel band. The visual preview GIFs confirm a hand-drawn illustration sensibility, not retro 16-bit flattened style. The Skeleton at 64x96 and Ghost Warrior at 100x64 are in the HD-2D-pixel register. This is the same creator register as confirmed in the character-track from MonoPixelArt free character pack (26 animations, confirmed style).

**Decomposition:** Monolithic PNG sprite sheets. Aseprite source confirmed on Golems pack.

**Per-product-line deliverable_register field (Drift-13):**
- All confirmed packs: hand-drawn pixel, 64-100x64-96 dimensions — single consistent register; no drift detected across product lines

**Sample SKUs:**
- Forest Monsters (NWYP / $4): Mushroom, Slime, Bush Monster; beast archetypes; up to 9 animation states
- Dark Fantasy Enemies (NWYP / $4): Bat, Ghost Warrior, Evil Creature; undead/dark; teleport + spawn states
- Skeletons Pack (NWYP / $3): 3 skeleton types, 64x96, 6 animations
- Golems Pack (NWYP / $4): 3 golems, teleportation state, Aseprite source

**Notes for downstream:** MonoPixelArt's total catalogue (6 packs at ~$3-4 each; $15-20 total for premium across all packs) covers 5-6 of the 6 enemy archetypes at low cost. The register is confirmed. The limitation is scale — 3 monsters per pack, 6 packs total = ~15-18 distinct enemy sprites at full premium, which may be insufficient for full archetype coverage without supplementing from Elthen or CreativeKind. Drax: Aseprite source files on Golems pack is favorable for Pixi.js integration. License modification restriction (cannot modify assets) may constrain palette-shift work for S2 element-palette-shift from enemy-visual-legibility.md — verify with drax whether runtime tint/filter is "modification" under this license or a rendering operation.

---

### Vendor 4 — CraftPix.net (monster sprite line)

**URL:** https://craftpix.net/categorys/monster-sprites/
**Platform:** CraftPix.net (proprietary store)
**Cost:** Subscription/membership model — "Premium membership" required for most; individual purchase option exists on some packs ($5.50 for Pixel Art Monster Enemy Game Sprites; Boss Monsters also purchasable individually). Free tier available (Free RPG Monster Sprites, Free Fantasy Enemies).
**License:** Proprietary CraftPix license. "Royalty free usage in unlimited projects." "You can sell and distribute games with our assets." No attribution required. Redistribution of source files prohibited. Perpetual access to downloaded assets after subscription ends.
**License flag:** HOLD — same proprietary subscription model flagged in character-track scout (CraftPix). Per-product license is reasonably clear but non-standard. Cost model is subscription; individual purchase is available on at least some monster packs at $5.50. Subscription model is not suitable for per-asset evaluation at this stage.

**CRITICAL register finding (from character-track scout):** CraftPix character sprites were flagged as vector-register in the character-track scout. **Monster sprite packs require per-product verification.** The following findings distinguish monster-track CraftPix from character-track CraftPix:

*Pixel Art Monster Enemy Game Sprites ($5.50):*
- Sprite dimensions: 128x128 pixels (most); 256x256 (Ent)
- Animation states: Idle, Walk, Hurt, Attack, Death (5 states)
- File formats: PNG Transparent + PSD Photoshop
- Layered: Yes
- Style: Pixel art confirmed (PSD/PNG, not AI/EPS/vector formats)
- Number of monsters: 6 fantasy characters
- AI-content: No statement found

*Free RPG Monster Sprites Pixel Art:*
- Sprite dimensions: 128x128 or 256x256 (depending on monster)
- Animation states: Idle, Walk, Hurt, Attack, Death (5 states)
- File formats: PNG Transparent + PSD
- Style: Pixel art confirmed (classical frame-by-frame animation)
- AI-content: No statement found

*Boss Monsters Pixel Art (individual purchase confirmed):*
- Sprite dimensions: Mage 64x64, Demon 96x96, Ooze 96x96
- Animation states: Walk, Run, Sneer, Attack1, Attack2, Attack3, Hurt, Death (8 states)
- File formats: PSD + PNG
- Style: Pixel art confirmed
- Monsters: 3 boss characters (Mage, Demon, Ooze)
- AI-content: No statement found

**Register finding:** CraftPix **monster** sprites are confirmed pixel art (PSD/PNG delivery, not AI/EPS). This is a different finding from the character-track CraftPix evaluation where vector delivery was confirmed. The monster catalogue is in a different product line from the character sprites. Per Drift-13 per-product-line deliverable_register discipline: monster line = pixel art; character line = vector (per character-track scout finding). These are distinct product lines within CraftPix.

**Coverage vs monster archetype taxonomy:**
- Brute: multiple packs (not individually fetched; inferred from catalogue page)
- Caster: Boss Mage (confirmed), Demon Mage (inferred)
- Undead: Skeletons pack (Top-Down Pixel Skeletons confirmed: hurt, death, run, idle, walk, attack)
- Beast: Slime pack (Top-Down Pixel Art Slime Monsters: multiple attacks, idle, hurt, dead, walk, run)
- Magical: Fire Monster Sprites (Fire-themed; idle, walk, hurt, attack, death confirmed)
- Boss: Boss Monsters pack (Mage, Demon, Ooze — confirmed at 64-96px)
- Dragon: Dragon Sprite Sheets (3 dragons: take off, landing, gliding, attack, hurt, dead) — subscription-gated

**B11/B13 mechanic-pairing:**
- Boss Mage "Sneer" = taunt/channel state before AOE
- 3-attack sequence on Boss Monsters (Attack1, Attack2, Attack3) = scripted multi-phase boss behavior
- Dragon "Gliding" = sustained aerial state analog for elemental-projectile patterns

**Style register assessment:** CONFIRMED pixel art on sampled packs. 128x128 base dimension places the $5.50 pack in the HD-2D-pixel register. Boss Monsters at 64-96px are borderline mid-pixel to HD-2D-pixel. Subscription-required Dragon pack dimensions not confirmed.

**Decomposition:** Monolithic PNG sprite sheets + PSD layered files.

**Per-product-line deliverable_register field (Drift-13):**
- Monster sprite line: pixel art confirmed (PSD/PNG) — distinct from character sprite line (vector, per character-track scout)
- Boss Monsters line: pixel art at 64-96px — mid-pixel to HD-2D border
- Dragon line: subscription-gated; pixel art inferred from "PSD, PNG" format listing; dimensions not confirmed
- Note: Always verify per-product on CraftPix — the brand spans both pixel art and vector product lines

**Sample SKUs:**
- Pixel Art Monster Enemy Game Sprites ($5.50): 6 monsters, 128-256px, 5 animations, pixel art
- Free RPG Monster Sprites: 128-256px, 5 animations, free
- Boss Monsters Pixel Art (individual purchase): 3 bosses, 64-96px, 8 animations
- Free Fantasy Enemies Pixel Art: free evaluation tier

**Notes for downstream:** CraftPix monster line is viable at the 128x128 tier — confirmed pixel art, not vector. The subscription model remains non-standard but individual purchase is available on at least $5.50 packs. No AI-content statement found on any CraftPix pack; flag this gap. The free tier (Free RPG Monster Sprites, Free Fantasy Enemies) provides a zero-cost evaluation path before any subscription commitment. CraftPix's monster catalogue is a useful supplement for specific archetype gaps, particularly if no itch.io vendor covers a needed monster type.

---

### Vendor 5 — OcO (Medieval Fantasy Character Pack series — higher-numbered packs)

**URL:** https://oco.itch.io/
**Platform:** itch.io
**Cost:** Free (Packs 1-4, 6-7); $2 (Pack 5); $5 (Pack 3 full tier); $3 minimum for most
**License:** "Feel free to use and modify the characters depending on your current project." Commercial use permitted; reselling individual assets prohibited. Attribution requested (not required). Not CC-labeled; custom on-page statement.
**License flag:** CLEAR — terms confirmed on Pack 1 page. Commercial use explicit. Modification permitted. Attribution optional. Provisionally the cleanest itch.io enemy-sprite license in this scout after LuizMelo CC0.

**CRITICAL register finding — series spans multiple registers:**

*Pack 1 (original):*
- Sprite dimensions: 64x64 pixels — retro-pixel register
- Characters: Knight + Wolf + Bat + Witch + Golem (5 enemies)
- Animation states (Golem): Idle, IdleAlternate, Walk, Attack, Death (5 states)
- Animation states (Knight — playable): Idle, Attack, Shield, JumpAndFall, Roll, Death, Run

*Pack 3 ($5 full):*
- Sprite dimensions: 128x128 pixels (standard); 160x128 (large poses) — HD-2D-pixel register
- Characters: King (boss), Pike-man, Jester, Drake, Priest (5 characters)
- Animation states (King): Idle (18fr), Walk (8fr), Combo (58fr), Teleport
- Frame counts are high (King: 58fr combo) — animation depth is strong for boss tier
- Notes: Boss-class King with Teleport = displacement animation; Combo = multi-phase boss behavior

*Pack 7 (free):*
- 5 enemy types
- Sprite dimensions: not confirmed

**Per-product-line deliverable_register finding (Drift-13 — CRITICAL):**
- Pack 1: 64x64 — retro-pixel register
- Pack 3: 128x128 — HD-2D-pixel register
- Pack 5: dimensions unconfirmed
- Pack 6-7: dimensions unconfirmed
- **OcO packs span registers across the series.** Do not assume a single register for "OcO." Per-pack dimension verification required before any pack is treated as HD-2D candidates.

**Coverage vs monster archetype taxonomy:**
- Brute: Drake (inferred beast/brute); Golem (confirmed, 64x64 = retro)
- Caster: Witch (64x64, confirmed), Priest (128px, unconfirmed states)
- Undead: None confirmed in fetched packs; Jester may be dark/fool archetype
- Beast: Wolf (64x64, retro), Bat (64x64, retro), Drake (128px)
- Boss: King (128x128, confirmed boss-tier)
- Humanoid: Pike-man, Jester, King, Knight

**B11/B13 mechanic-pairing:**
- King "Teleport" = displacement animation (B11 vortex/reposition analog)
- King "Combo" 58fr = extended scripted-sequence boss attack phase
- Witch "Throw" = projectile/sniper animation

**Style register assessment:**
- Pack 1 (64x64): retro-pixel — BELOW HD-2D canonical target
- Pack 3 (128x128): HD-2D-pixel — MATCHES canonical target
- Pack 3's King is the single strongest boss-archetype sprite in this scout at confirmed 128x128 with teleport + extended combo states

**Decomposition:** Monolithic PNG strips (sprite sheets). No Aseprite source.

**AI-content signal:** "No generative AI was used" confirmed on Pack 3 page.

**Sample SKUs:**
- Medieval Fantasy Character Pack (free / $3): 5 characters including Golem, Wolf; 64x64 retro-register
- Medieval Fantasy Character Pack 3 (NWYP / $5): 5 characters including King boss; 128x128 HD-register
- Medieval Fantasy Character Pack 7 (free): 5 enemy types; register unconfirmed

**Notes for downstream:** Pack 3 at 128x128 is the recommended OcO pack for the HD-2D-pixel register. The $5 full-tier includes all 5 characters (King boss + 4 supporting enemies). Pack 1 is retro-register — useful for prototyping only (same pattern as LuizMelo in the character-track scout). Packs 5, 6, 7 require dimension verification before register classification. The cross-pack register variance is a Drift-13 flag: do not treat OcO as a consistent-register vendor; evaluate pack by pack.

---

### Vendor 6 — Clembod (Cultist + Eldritch catalogue)

**URL:** https://clembod.itch.io/
**Platform:** itch.io
**Cost:** $5–$13 per pack; free packs for evaluation
**License:** Custom on-page statement: "You can use this asset for personal and commercial purpose, you can modify this object to your needs. You can NOT redistribute or resell it." Confirmed on Cultist Enemy Pack.
**License flag:** CLEAR — commercial use explicit; modification permitted; no Patreon gate. Cleanest custom license in the scout alongside OcO.

**Pack catalogue:**

*Cultist Enemy Pack ($7.50):*
- Monsters: 4 cultist types (Cultist 45x42, Twisted Cultist 45x42, Big Cultist 108x59, Assassin Cultist 106x76)
- Animation states (Cultist): Idle, Attack, Walk, Death, Hit, Jump/Fall, Fireball, Impact (8 states)
- Animation states (Twisted Cultist): Idle, Attack, Walk, Death, Hit, Jump/Fall, Twist (7 states)
- Animation states (Big Cultist): Idle, Combo Attack, Run, Death, Hit, Jump/Fall (6 states)
- Animation states (Assassin Cultist): Idle, Attack, Ambush, Run/Blink, Death, Hit, Jump/Fall, Vanish, Arise (9 states)
- File format: ZIP (808 kB)
- AI-content: "No generative AI was used"

*Eldritch/cosmic catalogue (dimensions unconfirmed):*
- Voidcaller ($5): cosmic entity archetype
- Shoggoth ($5): beast/cosmic archetype
- Voidborn Goddess ($5): boss/cosmic archetype
- Ancient God Pack ($13): large boss-tier pack

**B11/B13 mechanic-pairing:**
- Cultist "Fireball" + "Impact" = projectile-cast + AOE-hit animation pair (direct B11 caster coverage)
- Assassin Cultist "Vanish" + "Arise" = iframe-dash analog (stealth-enter / stealth-exit pattern)
- Assassin Cultist "Ambush" = leap/dash attack analog
- Big Cultist "Combo Attack" = multi-phase brute-attack

**Style register assessment:** MIXED across the pack. Cultist base character is 45x42 — borderline retro-pixel/mid-pixel. Big Cultist is 108x59 — mid-pixel approaching HD-2D-pixel band. Assassin Cultist is 106x76 — mid-pixel band. The vendor produces characters in an elongated proportion (wide-format sprites) rather than square-frame format. The hand-drawn pixel art quality is confirmed from preview GIFs. Dimensions are smaller than the HD-2D target (64-128px character height), but the style register (hand-drawn illustration) is correct.

**Per-product-line deliverable_register field (Drift-13):**
- Cultist line: 45-108x42-76 — mid-pixel band; hand-drawn style register; BELOW HD-2D canonical dimension target but consistent hand-drawn illustration sensibility
- Eldritch/cosmic line (Voidcaller, Shoggoth, Ancient God): dimensions unconfirmed; likely larger canvas for god-tier entities; verify before purchase
- Note: Clembod's Cultists are stylistically consistent but at the small end of the HD-2D-pixel target range

**Decomposition:** Monolithic ZIP per pack. No paper doll.

**Notes for downstream:** Clembod's value is the animation-state richness (Fireball + Impact pair, Vanish/Arise pair, Ambush) and the cultist/dark-humanoid archetype not well-covered by other vendors. The Cultist pack maps directly to "cultists" in the ARPG humanoid-enemy taxonomy. The register is a borderline flag — not retro 16-bit, but not firmly HD-2D-pixel either. The eldritch catalogue (Shoggoth, Voidborn Goddess, Ancient God Pack at $13) is the most distinct boss-tier coverage in the scout (cosmic horror aesthetic). Dimensions on eldritch packs must be verified before register classification.

---

### Vendor 7 — LuizMelo (Monsters Creatures Fantasy)

**URL:** https://luizmelo.itch.io/monsters-creatures-fantasy
**Platform:** itch.io
**Cost:** Name-your-own-price (CC0 — free download available)
**License:** Creative Commons Zero v1.0 Universal (CC0). No attribution required, commercial use unrestricted.
**License flag:** CLEAR (CC0 confirmed). Cleanest license in the entire scout.

**Pack contents:**
- Monsters: Skeleton (Idle, Walk, Attack, Shield, Take Hit, Death), Mushroom (Idle, Run, Attack, Take Hit, Death), Goblin (Idle, Run, Attack, Take Hit, Death), Flying Eye (Flight, Attack, Take Hit, Death)
- Animation states: 4-6 per character; Skeleton has "Shield" state = block-analog
- Sprite dimensions: not confirmed from page fetch; likely 16-32px based on LuizMelo's known character sprite register (character-track finding: LuizMelo Knight Pack at 21x32)
- File format: ZIP; PNG sprite sheets
- AI-content: "No generative AI was used"
- Rating: 4.8/5 stars, 118 ratings

**B11/B13 mechanic-pairing:**
- Skeleton "Shield" = block-active/parry analog at enemy tier

**Style register assessment:** LIKELY retro-pixel register. LuizMelo's character sprites are confirmed retro (21x32 in character-track scout). The monster pack dimensions are unconfirmed but the vendor's consistent register pattern strongly suggests retro-pixel. Treat as retro-register until dimension confirmed via download-inspect.

**Per-product-line deliverable_register field (Drift-13):**
- Monsters Creatures Fantasy: dimensions unconfirmed; infer retro-pixel from vendor pattern; VERIFY before HD-2D-register assignment

**Notes for downstream:** LuizMelo's monster pack is valuable specifically for its CC0 license and Skeleton's Shield state. For prototyping purposes and placeholder enemy sprites with no license friction, this is the lowest-barrier entry in the scout. Not recommended as a primary HD-2D-register vendor. The 4-character scope (skeleton, mushroom, goblin, flying eye) is narrow for a full enemy roster. Supplement with Elthen or CreativeKind for production use.

---

### Vendor 8 — MonoPixelArt (character-referenced in enemy-legibility.md cross-reference note)

See Vendor 3 above (MonoPixelArt) — this is the same vendor. Referenced here separately because enemy-visual-legibility.md § S1 names "itch.io vendors Elthen, LuizMelo, ansimuz, pimen monster extensions" as the expected monster-sprite registry sources. MonoPixelArt was not in that original list but surfaces as the strongest mid-tier candidate in this scout. The list in enemy-visual-legibility.md should be updated to include MonoPixelArt.

---

### Non-qualifying vendors (register or quality gap)

The following vendors were evaluated and disqualified from primary recommendations:

| Vendor | Reason | Register |
|---|---|---|
| GandalfHardcore (enemy packs) | Enemy packs are 32x32 retro-pixel (Hell Tiles pack, Desert pack); "10 Enemy Characters" pack at $4.54 is retro-register | retro-pixel |
| Admurin (Mega Pack) | Explicitly retro/8-bit aesthetic confirmed; 150+ enemies but at retro resolution | retro-pixel |
| rvros (Pixel Monster Pack) | 10 monsters at 16x16 tile grid size; platformer orientation; CC0 license but retro-register | retro-pixel |
| Iphigenia Pixels | 16x16 sprites — retro-register confirmed | retro-pixel |
| Cyangmou (50 Fantasy Monsters) | $199.99 for static sprites only (no animations) — immediately disqualified | static sprites |
| finalbossblues (Action RPG Monsters) | 16x16 tile grid base size; $50 per pack; retro-register | retro-pixel |
| Enhaira (2D Pixel Monster) | License terms absent; 16x16 / 64x64 / 128x128 multi-res (register mixed); zombie/horror only; animation states unlisted | unclear |
| OcO Packs 1, 4, 6, 7 | 64x64 retro-register (Pack 1 confirmed); other packs unconfirmed — apply register-drift caution | retro-pixel (Pack 1) |

---

## Monster Type Coverage Matrix

Coverage rated by this scout across HD-2D-register vendors:

| Monster Type | Elthen | CreativeKind | MonoPixelArt | CraftPix | OcO (Pack 3) | Clembod |
|---|---|---|---|---|---|---|
| **Humanoid — bandit/cultist** | Bandit King, Cultists | NightBorne Warrior | Evil Creature | inferred | Pike-man, Jester | Cultists (CONFIRMED) |
| **Humanoid — dark mage** | Bandit Necromancer | Demon Mage, Archimage | Ghost Warrior | Boss Mage | Priest, Witch | Twisted Cultist |
| **Humanoid — fallen warrior** | Orcs, Kobolds, Lizardfolk | NightBorne Warrior (free) | — | — | King, Drake | Assassin Cultist |
| **Undead — skeleton** | Skeletal Trumpetist | Mutant Skeleton | Skeletons (3 types) | Skeletons pack | — | — |
| **Undead — ghost/wraith** | Medieval Ghost Townsfolk | Dark Soul | Ghost Warrior | — | — | Voidcaller (eldritch) |
| **Undead — lich** | Lich (192x160) | Lich (176x128) | — | — | — | — |
| **Beast — wolf/canine** | — | — | — | — | Wolf (64x64 retro) | — |
| **Beast — spider** | Spider Queen ($7) | — | — | — | — | — |
| **Beast — slime** | — | — | Slime (confirmed) | Slime pack | — | — |
| **Magical — golem** | Guardian Scroll, Golems | Crystal Golem (168x141) | Golems (3 types) | Golem pack | Golem (64x64 retro) | — |
| **Magical — elemental** | Fire/Wind/Shadow Elementals | Fire Elemental, God of Lightning | — | Fire Monster | — | — |
| **Magical — dragon** | Elder Dragon ($10), Hatchling | — | — | Dragon ($5.50, subscription) | Drake | — |
| **Boss — large unique** | Hill Giant (320x128) | Lich (176x128), Fire Lord | — | Boss pack (96px) | King (128x128) | Ancient God ($13) |

**Gaps in HD-2D-register coverage:**
- Wolf/canine beast: No confirmed HD-2D vendor. LuizMelo has Goblin/Flying Eye at retro; beast wolf specifically absent above retro register.
- Snake: Not surfaced in any vendor in this scout.
- Bear: Not surfaced.
- Zombie (not skeleton): MonoPixelArt / CraftPix inferred; not confirmed at HD-2D pixel dimensions.

---

## B11/B13 Mechanic-Pairing Summary

| Mechanic | Relevant Animation State | Vendor(s) | Pack(s) |
|---|---|---|---|
| Vortex/displacement recipient | Spawn-Teleport, Escape-Teleport | MonoPixelArt | Dark Fantasy Enemies (Evil Creature) |
| Vortex/displacement recipient | King Teleport | OcO | Pack 3 (King) |
| AOE-tank (large area recipient) | 320x128 canvas footprint | Elthen | Hill Giant |
| Channel/cast state | Prepare Spell, Cast x2 | Elthen | Lich |
| Channel/cast state | Casting (29fr) | CreativeKind | Lich |
| Channel/cast state | Fireball + Impact | Clembod | Cultist Enemy Pack |
| Leap/dash attack | Assassin Cultist Ambush | Clembod | Cultist Enemy Pack |
| Iframe-dash analog | Vanish + Arise | Clembod | Cultist Enemy Pack |
| Elemental-shift / phase-change | Transform | Elthen | Werewolf |
| Pack/swarm emergence | Spawn (Ghost Warrior) | MonoPixelArt | Dark Fantasy Enemies |
| Multi-phase boss | Combo (58fr) + 4x Attack | Elthen (Minotaur) + OcO | Minotaur, Pack 3 King |
| Block-at-enemy-tier | Shield state | LuizMelo | Monsters Creatures Fantasy |

---

## Style Register Assessment

**HD-2D-pixel register (confirmed at canonical target):**
- Elthen boss-tier: Minotaur (96x96), Lich (192x160), Hill Giant (320x128), Werewolf (160x64) — CONFIRMED
- CreativeKind: Lich (176x128), Crystal Golem (168x141) — CONFIRMED
- OcO Pack 3: King (128x128) — CONFIRMED
- CraftPix monster line: 128-256px — CONFIRMED (distinct from CraftPix character line which is vector)

**Mid-pixel register (below HD-2D target but above retro; hand-drawn illustration style):**
- MonoPixelArt: 64-100x64-96 — hand-drawn illustration sensibility; below 128px threshold but not retro 16-bit aesthetic
- Clembod Cultists: 45-108x42-76 — hand-drawn illustration sensibility; borderline mid-pixel
- Elthen mid-tier (Dragon Hatchling, small enemy packs): dimensions unconfirmed; infer smaller canvas from file size

**Register-drift flag (per-pack variance detected):**
- OcO: Pack 1 is 64x64 (retro); Pack 3 is 128x128 (HD-2D) — do not treat as consistent
- Elthen: Boss-tier confirmed HD-2D; lower-tier packs may be smaller — verify per-pack
- CraftPix: Monster line is pixel art; character line is vector — always verify per product line

---

## License Verification Flags

Per C.2 amendment discipline:

| Vendor | Flag | Reason | Status |
|---|---|---|---|
| Elthen | HOLD | License terms behind Patreon-only link (403 returned); per-pack commercial use language found on product pages but full standardized terms not public | Navigate to Patreon post in browser before purchase; terms appear to permit commercial use from product-page language |
| CreativeKind | VERIFY | Custom non-CC license; terms confirm commercial use on product pages; not Patreon-gated; no attribution required found | Provisionally clear; same tier as Seliel the Shaper from character-track |
| MonoPixelArt | VERIFY | Custom non-CC license; "modify" restriction may affect runtime tint/palette-shift operations; consistent across packs; commercial use explicit | Confirm with drax whether runtime Pixi.js tint is "modification" under this license |
| CraftPix | HOLD | Proprietary subscription model; individual purchase available ($5.50) but subscription-gating for most packs; no AI-content statement | Free tier available for zero-risk evaluation; individual purchase path exists for $5.50 monster pack |
| OcO | CLEAR | Commercial use explicit; modification permitted; attribution optional; no Patreon gate | Cleanest custom license in scout |
| Clembod | CLEAR | Commercial use explicit; modification permitted; no Patreon gate | Operationally clear; verify Eldritch packs have same terms |
| LuizMelo (Monsters) | CLEAR (CC0) | CC0 confirmed; no restrictions | CC0 — cleanest possible license |

---

## Knowledge Gaps Not Resolved

1. **Beast archetype — wolf/snake/bear — not covered at HD-2D register.** No vendor in this scout offers a wolf, snake, or bear monster sprite at confirmed HD-2D-pixel dimensions. LuizMelo's Monsters pack has a wolf at retro dimensions (inferred). This gap requires a follow-on targeted crawl or supplementary search specifically for beast-archetype pixel art at HD-2D resolution.

2. **Elthen lower-tier pack dimensions not confirmed.** Dragon Hatchling, Cultist packs, and numerous $3-5 packs have unconfirmed dimensions. Boss-tier confirmed; mid-tier requires download-inspect or per-page fetch of each individual pack.

3. **CraftPix full monster catalogue scope not fetched.** The CraftPix monster category page returned a list of 16+ packs but individual pages not fetched for most. Specific packs (Imp Mobs, Cave Bosses, Basement Enemies, Land Monster 2D) have unconfirmed register and animation states.

4. **Clembod Eldritch catalogue dimensions not confirmed.** Voidcaller, Shoggoth, Voidborn Goddess, Ancient God Pack ($13) have no confirmed dimensions from this scout. These are the most unique boss-tier candidates (cosmic horror aesthetic); verify dimensions before assessment.

5. **GameDevMarket character + monster catalogue partially blocked.** RPG Heroes & Enemies pack and other GameDevMarket packs returned 403. This platform was inaccessible in the character-track scout as well. A direct-browse session (not API fetch) may be required.

6. **OcO packs 5, 6, 7 dimensions not confirmed.** Pack 3 at 128x128 is the confirmed HD-2D candidate; other packs are free and may be HD-2D or retro — verify before use.

7. **MonoPixelArt runtime tint/palette-shift compatibility with "no modification" license clause** not confirmed. This is a B13/S2 compatibility flag for enemy-visual-legibility.md's element-palette-shift requirement.

8. **Unity Asset Store monster sprite catalogue** not accessed. RPG Monster PixelArt Pack ($29.99) and similar Unity Asset Store entries lack usable metadata from public pages. Unity Asset Store packs generally require Unity engine integration (not native Pixi.js); may not be directly compatible without export.

---

## Top-3 Vendor Recommendations

Ranked by: (1) register match to canonical HD-2D-pixel lock, (2) archetype coverage breadth, (3) license cleanliness, (4) animation richness (B11/B13 bonus), (5) cost efficiency.

**Rank 1 — Elthen's Pixel Art Shop (monster catalogue)**
- URL: https://elthen.itch.io/
- Deepest HD-2D-pixel monster catalogue on itch.io. Confirmed boss-tier sprites at 96x96 to 320x128. Covers all six monster archetypes across thematic bundles. B11/B13 coverage: Lich "Prepare Spell + Cast", Hill Giant 320x128 AOE footprint, Werewolf "Transform". Cost: $3-10 per pack; thematic bundles $20-25. Primary risk: Patreon-gated license (HOLD — verify before purchase). Recommended first purchase: Minotaur (free/NWYP) as zero-risk evaluation; then Lich ($6) and Hill Giant ($7) for boss-tier coverage.

**Rank 2 — CreativeKind (monster line)**
- URL: https://creativekind.itch.io/
- Already a Tier-1 VFX vendor; extending to monster track preserves within-frame register coherence (no mixing risk). Confirmed HD-2D-pixel dimensions (Lich 176x128, Crystal Golem 168x141). Lich has casting + extended spin attacks (B11 caster coverage). Custom license confirmed commercial use without Patreon gate. Cost: $4.50-9 per pack; $84.99 bundle for 26+ packs. Primary gap: beast archetype coverage is weak (Hellfire Rhino unverified). Recommended first purchase: Lich ($9) for boss-caster coverage.

**Rank 3 — MonoPixelArt (multi-pack catalogue)**
- URL: https://monopixelart.itch.io/
- Six-pack catalogue at $3-4 premium each covering undead (skeletons 64x96), beast (forest monsters 64-90x64), magical (golems with teleport), and dark (ghost warrior, evil creature with teleport + spawn states). B11/B13: Evil Creature "Spawn-Teleport" + "Escape-Teleport" (displacement); Ghost Warrior "Spawn" (wave-emergence). CC-style custom license; commercial use confirmed; no Patreon gate; no-AI confirmed. Cost: $15-20 total for all 6 packs (premium). Primary risk: "no modification" clause may conflict with runtime palette-shift (verify with drax). Recommended first purchase: Dark Fantasy Enemies (NWYP/$4) for teleport + spawn states; Skeletons Pack (NWYP/$3) for undead archetype.

---

## Register Drift / Pattern P8 Vigilance Findings

Per Drift-13 discipline and Pattern P8 register-confusion vigilance:

1. **CraftPix monster line vs character line register split (CRITICAL):** Character-track scout confirmed CraftPix character sprites as vector register. Monster-track scout confirms CraftPix monster sprites as pixel art (PSD/PNG, 128-256px). These are distinct product lines with different registers. Any downstream consumption of CraftPix assets MUST be tagged per-product-line; do not apply "CraftPix = vector" globally.

2. **OcO series register variance (CRITICAL):** Pack 1 is retro-pixel (64x64); Pack 3 is HD-2D-pixel (128x128). Series number does not predict register. Tag each OcO pack individually with its confirmed dimension.

3. **Elthen boss vs lower-tier register variance:** Boss-tier packs (Lich, Hill Giant, Werewolf, Minotaur) confirmed HD-2D-pixel. Lower-tier packs (Dragon Hatchling, smaller enemies) are likely smaller but unconfirmed. Do not apply a single register tag to the entire Elthen catalogue; tag per-pack.

4. **MonoPixelArt "no modification" clause vs runtime palette-shift:** enemy-visual-legibility.md S2 requires element palette-shift at runtime via Pixi.js tint. If MonoPixelArt's "no modification" clause covers runtime rendering operations, this would be a B13 wiring incompatibility. Structural track viability-gate review (Elrond) and Wiring track review (Drax) should assess before any MonoPixelArt packs are purchased.

---

## Source List

- https://elthen.itch.io/ (fetched 2026-05-16)
- https://elthen.itch.io/monster-sprite-pack (fetched 2026-05-16)
- https://elthen.itch.io/2d-pixel-art-beast-monster-sprites (fetched 2026-05-16)
- https://elthen.itch.io/2d-pixel-art-minotaur-sprites (fetched 2026-05-16)
- https://elthen.itch.io/2d-pixel-art-lich-sprites (fetched 2026-05-16)
- https://elthen.itch.io/2d-pixel-art-hill-giant-sprites (fetched 2026-05-16)
- https://elthen.itch.io/2d-pixel-art-werewolf-sprites (fetched 2026-05-16)
- https://elthen.itch.io/2d-pixel-art-dragon-hatchling-sprites (fetched 2026-05-16)
- https://creativekind.itch.io/ (fetched 2026-05-16)
- https://creativekind.itch.io/lich (fetched 2026-05-16)
- https://creativekind.itch.io/crystal-golem (fetched 2026-05-16)
- https://monopixelart.itch.io/ (fetched 2026-05-16)
- https://monopixelart.itch.io/forest-monsters-pixel-art (fetched 2026-05-16)
- https://monopixelart.itch.io/dark-fantasy-enemies-asset-pack (fetched 2026-05-16)
- https://monopixelart.itch.io/skeletons-pack (fetched 2026-05-16)
- https://monopixelart.itch.io/golems-pack (fetched 2026-05-16)
- https://craftpix.net/categorys/monster-sprites/ (fetched 2026-05-16)
- https://craftpix.net/product/pixel-art-monster-enemy-game-sprites/ (fetched 2026-05-16)
- https://craftpix.net/product/boss-monsters-pixel-art/ (fetched 2026-05-16)
- https://craftpix.net/product/dragon-pixel-art-character-sprite-sheets-pack/ (fetched 2026-05-16)
- https://craftpix.net/freebies/free-rpg-monster-sprites-pixel-art/ (fetched 2026-05-16)
- https://oco.itch.io/ (fetched 2026-05-16)
- https://oco.itch.io/medieval-fantasy-character-pack (fetched 2026-05-16)
- https://oco.itch.io/medieval-fantasy-character-pack-3 (fetched 2026-05-16)
- https://clembod.itch.io/ (fetched 2026-05-16)
- https://clembod.itch.io/cultist-enemy-pack (fetched 2026-05-16)
- https://luizmelo.itch.io/monsters-creatures-fantasy (fetched 2026-05-16)
- https://rvros.itch.io/pixel-monsters (fetched 2026-05-16)
- https://gandalfhardcore.itch.io/ (fetched 2026-05-16)
- https://admurin.itch.io/ (fetched 2026-05-16)
- https://iphigeniapixels.itch.io/animated-pixel-monster-pack-level-2 (search-only; not directly fetched 2026-05-16)
- https://cyangmou.itch.io/pixel-rpg-monster (fetched 2026-05-16)
- https://finalbossblues.itch.io/action-rpg-monsters (fetched 2026-05-16)
- https://assetstore.unity.com/packages/2d/characters/rpg-monster-pixelart-pack-250420 (fetched 2026-05-16)
- https://www.gamedevmarket.net/asset/character-pack-rpg-heroes-enemies-pixel-art-animated-characters-animations (403 — not accessible 2026-05-16)
- https://enhaira.itch.io/2d-monster-asset-pack (fetched 2026-05-16)
- https://itch.io/game-assets/tag-monsters/tag-pixel-art (fetched 2026-05-16)
- https://itch.io/game-assets/tag-enemy/tag-pixel-art (fetched 2026-05-16)
- Web searches: 12 queries across itch.io pixel art monster sprite, craftpix monster sprite, oco medieval fantasy pack, clembod cultist, elthen monster, creativekind monster enemy, MonoPixelArt dimensions, pixel art ARPG enemy boss HD 64px 128px commercial — 2026-05-16

---

— legolas, 2026-05-16
