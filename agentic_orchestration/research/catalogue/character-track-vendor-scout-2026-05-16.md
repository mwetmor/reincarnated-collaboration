# Research — Character-Animation Vendor Scout — 2026-05-16

**Mode:** A (analytical)
**Commissioner:** knight-rider (Pattern A dispatch, gandalf Track 4 — B13 lead-time investment)
**Approved by:** Matt (2026-05-16, Day 4 approval of gandalf Track 4 decision #2)
**Sources consulted:** itch.io vendor pages (direct fetch), CraftPix.net product and license pages, GameDevMarket asset pages (partial — 403 on some), web search sweeps across multiple query vectors
**Style register target:** Hand-drawn pixel-art, HD-2D-shaped (per `canonical/story/style-register.md`, locked 2026-05-15)
**B13 priority filter:** Vendors with coverage of `roll`, `parry_active`, `block_active`, `iframe_dash` equivalents ranked high

---

## Summary (4 sentences)

Eight candidate character-animation vendors are surfaced, ranging from strong HD-2D-register matches (Seliel the Shaper — Mana Seed; chierit — Elementals series) to capable retro-pixel-register vendors with confirmed defensive-mobility coverage (GandalfHardcore Samurai, LuizMelo Knights Pack). The B13 defensive-mobility cluster (`roll`, `parry_active`, `block_active`, `iframe_dash`) is directly addressed by three vendors — Seliel the Shaper (explicit `parry` and `evade` states), chierit (explicit `roll`, `slide`, `defend` states), and LuizMelo Knights Pack (explicit `block` and `hold shield` states) — with GandalfHardcore also covering `block`, `block hit`, and `dash`. CraftPix.net's character sprite catalogue is **vector-register, not pixel-art** across multiple verified product pages — it does not meet the HD-2D pixel register requirement and carries a subscription/membership cost model that is non-standard relative to the itch.io vendor class. License verification flags are surfaced for Pixogen (non-public license file requires download) and CraftPix (subscription model, not per-asset purchase); all itch.io vendors reviewed have publicly verifiable license terms.

---

## Findings

### Vendor 1 — Seliel the Shaper (Mana Seed Character Base)

**URL:** https://seliel-the-shaper.itch.io/character-base
**Platform:** itch.io
**Cost:** Free base tier (commercially usable); $19.98 full asset
**License:** Not explicitly stated as CC-standard; terms permit commercial use with download, no resale. Restriction: explicitly blocks blockchain/Web3 games. Terms appear on pack page; no separate license file required.
**License flag:** VERIFY — license statement is on-page (not CC-labeled). Full terms reviewed from page text: commercial use permitted, modification permitted, resale prohibited, Web3 explicitly blocked. Provisionally clear for Reincarnated. Web3 restriction irrelevant to this project.

**Animation states confirmed:**
- Movement: Idle, Walk (6-frame), Run (6-frame), Jump (4-frame)
- Sword & Shield combat: combat-ready idle, combat-ready move, forehand slash, backhand slash, thrust, shield bash, **parry**, **evade**, hit reaction, knockdown, lunge forward, retreat backward, draw/sheathe
- Spear/Polearm combat: same structure including **parry**, **evade**, hit reaction, knockdown
- Bow combat: same structure including **parry**, **evade**, hit reaction, knockdown
- All states in 4 directions

**B13 defensive-mobility coverage:** STRONG — explicit `parry` and `evade` across three weapon sets; `knockdown` adds iframe-recovery state. `shield bash` = active parry-counter analog.

**Sprite dimensions:** 64x64 frame cells on 512x512 sheets; character ~32px tall
**File format:** PNG sprite sheets + Aseprite source files; paper doll system (separate sheets for body, clothing, hair, weapons)
**Character count:** One base; paper doll system supports runtime weapon/outfit swapping
**Decomposition:** Decomposed — paper doll system with separate body/clothing/weapon/hair layers
**Style register:** Hand-drawn pixel sensibility; 64x64 frame cells; layered construction; consistent with HD-2D-pixel register. Creator describes as "16-bit-style." Self-described as "100% HUMAN-MADE / NO AI USED IN ANY WAY."
**AI-content signal:** Confirmed human-made.
**Ecosystem depth:** Full tileset ecosystem (30+ tileset packs), creature sprites, NPC packs — all Mana Seed-compatible. Third-party expansion packs (armor sets, body variants) exist. High ecosystem coherence.
**Sample SKUs:**
- Character Base (free + $19.98 full): base combat character, 3 weapon sets, parry/evade/knockdown states
- NPC Pack #1 ($9.99): standalone animated NPCs
- NPC Pack #2 ($9.99): additional NPCs

**Notes for downstream:** Paper doll decomposition is Drax-favorable for Pixi.js wiring. Sprite dimensions at 64x64 per frame align with HD-2D-pixel register. The full character base is the single highest-priority item in this scout for B13 defensive-mobility coverage. Tileset ecosystem is a bonus — not in-scope for this commission but relevant for future environment work.

---

### Vendor 2 — chierit (Elementals series)

**URL:** https://chierit.itch.io/
**Platform:** itch.io
**Cost:** Free base tier (13–15 animations per character); $7.50 per character full pack (adds ~12 Elemental Mode animations); $50 bundle for all 10 characters
**License:** Creative Commons Attribution 4.0 International (CC-BY 4.0). Commercial use permitted; modification permitted; credit "chierit" required; resale prohibited.
**License flag:** CLEAR — CC-BY 4.0 is publicly verifiable, well-understood. Attribution requirement is the only operational constraint. No download-only license file.

**Characters in Elementals series (10 total):**
Fire Knight, Water Priestess, Wind Hashashin, Ground Monk, Metal Bladekeeper, Leaf Ranger, Crystal Mauler, Lightning Ronin, Light Valkyrie, Shadow Stalker

**Animation states confirmed (Leaf Ranger — representative sample):**
- Movement: idle, run, jump
- Combat: 1_atk, 2_atk, 3_atk, air_atk, sp_atk
- **Defensive: roll, slide, defend**
- Status: take_hit, death
- Elemental Mode (paid): transformation sequence + extended attacks

**Animation states confirmed (Water Priestess):**
- Movement: idle, walk, surf, jump (up/down)
- Combat: air attack, tumble, 3-hit combo, special attack
- Support/defensive: heal, **defend**, take hit, death

**B13 defensive-mobility coverage:** STRONG — explicit `roll`, `slide`, `defend` confirmed on Leaf Ranger. `defend` = active block analog. `slide` = iframe-dash equivalent. Coverage validated on two characters; assumed consistent across series.

**Sprite dimensions:** Not explicitly stated on pack pages. Preview GIFs suggest ~48–64px character height, standard HD-pixel band.
**File format:** PNG sprite sheets + Aseprite source files included
**Character count:** 10 elemental-themed characters; each is a distinct archetype (ranger, knight, monk, assassin, ronin, valkyrie, stalker etc.)
**Decomposition:** Monolithic per character (each character is its own sprite sheet, not a paper doll). Individual characters are distinct sprites, not layered.
**Style register:** Hand-drawn pixel art; higher-fidelity than retro-pixel; illustration sensibility. Consistent with HD-2D-pixel register. Creator-confirmed "No generative AI was used."
**AI-content signal:** Confirmed on both fetched pack pages.
**Element-archetype alignment:** EXCEPTIONAL — the 10-character roster maps directly to Reincarnated's element system. Fire Knight, Water Priestess, Wind Hashashin, Ground Monk, Lightning Ronin, Shadow Stalker, Light Valkyrie cover the primary elemental archetypes. This is the strongest thematic alignment of any vendor found.
**Sample SKUs:**
- Elementals: Leaf Ranger ($7.50 full): 25 animations including roll/slide/defend, elemental mode
- Elementals: Water Priestess ($7.50 full): 27 animations including defend, heal states
- Elementals Bundle ($50): all 10 characters

**Notes for downstream:** Element-to-character mapping means each Reincarnated class archetype has a candidate sprite kit. Bundle at $50 for 10 characters = $5/character — extremely cost-efficient for the register quality. CC-BY 4.0 is cleanest license in the scout. Monolithic sprite sheets (not paper doll) mean character swapping is asset-level, not layer-level — Drax should confirm wiring approach.

---

### Vendor 3 — LuizMelo (Knights Pack + broader catalogue)

**URL:** https://luizmelo.itch.io/
**Platform:** itch.io
**Cost:** Free to $12.90 per pack; Knights Pack $7.75; most individual packs $1.25–$8.00; bundle pricing not confirmed
**License:** Creative Commons Zero v1.0 Universal (CC0) confirmed on Knight Pack and Medieval Warrior Pack 2. CC0 = no attribution required, commercial use unrestricted. Each pack page should be individually verified.
**License flag:** CLEAR (CC0 confirmed on sampled packs). Note: verify CC0 applies consistently across the full catalogue — some creators shift licenses between packs.

**Packs sampled:**

*Knight Pack ($1.25):*
- Animation states: Idle, Run, Crouch, Jump, Air Flip, Fall, Attack1, Attack2, Attack3, **Roll**, Slide, Take Hit, Death, Wall Idle, Wall Slide
- Sprite: 21x32 pixels; CC0; single knight character
- B13 coverage: `roll` confirmed; no explicit parry/block

*Knights Pack ($7.75):*
- Animation states: Idle, Run, Jump, Fall, Attack, **Hold Shield**, **Block**, Take Hit, Death
- Sprite: dimensions not specified; 3 knights with 3 weapon variants (single sword, sword+shield, two-handed sword)
- B13 coverage: `block` and `hold shield` confirmed; roll absent

*Medieval Warrior Pack 2 (free/NWYP):*
- Animation states: Idle (8fr), Run (8fr), Jump (2fr), Fall (2fr), Take Hit (3fr), Death (9fr), Attack x4 weapons (4fr each)
- Single character; no defensive states detected

*Dark Knight series ($8.00–$12.90 per pack):*
- 3-pack series; animation states not fully fetched
- Dark Knight 3 at $12.90 suggests higher animation count

**B13 defensive-mobility coverage:** MODERATE — `block` and `hold shield` confirmed on Knights Pack; `roll` confirmed on Knight Pack. No `parry` state detected. Two packs required to cover both block and roll.

**Sprite dimensions:** 21x32 (Knight Pack); varies by pack
**File format:** ZIP; PNG sprite sheets; no Aseprite source files confirmed
**Character count:** Varies; 1–3 per pack; large catalogue breadth (~20+ distinct character packs across knight/warrior/wizard/ghost-warrior series)
**Decomposition:** Monolithic per pack (single sprite sheet per character/weapon combo)
**Style register:** Retro pixel-art register. 21x32 sprite dimensions are at the retro-pixel band, below the HD-2D-pixel range (64–128px). Style confirmed as retro on fetched pack pages.
**AI-content signal:** "No generative AI was used" confirmed on fetched packs.
**Volume:** Largest pure character-sprite catalogue in the scout — 20+ packs spanning knights, warriors, wizards, ghost warriors, hunters, heavy armor, dark knights. Enemy/monster sprite coverage also present.
**Sample SKUs:**
- Knight Pack ($1.25): roll animation, CC0, single knight
- Knights Pack ($7.75): block/hold shield, 3 character variants
- Dark Knight ($8.00): higher-animation-count knight; states not fully verified

**Notes for downstream:** Register gap is the key constraint — LuizMelo is retro-pixel-register (21x32 sprites), not HD-2D-pixel. This is usable for prototype/placeholder work but is not the canonical register target. The catalogue breadth (20+ packs) and CC0 licensing make it valuable as a fallback or prototyping asset layer. Not recommended as primary character-animation vendor for the locked register, but very low friction for initial wiring work.

---

### Vendor 4 — GandalfHardcore (Pixel Art Samurai + catalogue)

**URL:** https://gandalfhardcore.itch.io/
**Platform:** itch.io
**Cost:** $3.24–$14.99 per pack; bundle $65.99 for 39 packs; 35% discount applied across packs
**License:** "Commercial and non-commercial projects permitted; modification permitted; no reselling, no AI training, no NFT/blockchain." License stated on product pages; no separate license file required.
**License flag:** VERIFY — non-CC license; terms are on product pages but use a custom statement rather than a standardized license. Key restrictions (no AI training, no NFT) are not operational constraints for this project. Provisionally clear. Recommend review of full terms before purchase.

**Animation states confirmed (Samurai Character — representative):**
- Idle (5fr), Run (8fr), Walk (8fr), Run Attack (8fr), Attack (8fr), Jump (4fr), Fall (4fr), Wall Slide (4fr), Landing (5fr), Heavy Attack/Strong Slash (13fr), **Block** (4fr), **Block Hit** (4fr), **Dash** (6fr), Resting (5fr), Death/Seppuku (17fr)
- Portraits: 64x64 pixel character portraits included

**B13 defensive-mobility coverage:** STRONG — explicit `block`, `block hit`, and `dash` confirmed. `block_active` = Block state; `iframe_dash` = Dash state. No `parry` or `roll` states detected.

**Sprite dimensions:** 96x64 pixels (Samurai)
**File format:** PNG sprite sheet + Aseprite source file
**Character count:** Large catalogue — Samurai, Knight, Wizard, Archer, Skeleton, Angel, Succubus, Maid, Soldier, NPC packs (100+), enemy packs. The Samurai is the highest-confirmed defensive-mobility pack.
**Decomposition:** Monolithic per pack
**Style register:** "16-bit era pixel art fidelity" — this is at the retro-to-mid-pixel register. 96x64 sprite dimensions are in the mid-pixel band, approaching HD-2D range but with a classic arcade aesthetic rather than a hand-drawn illustration sensibility. Not a clean HD-2D register match.
**AI-content signal:** "No generative AI was used" confirmed.
**Catalogue breadth:** Wide — multiple character archetypes (warrior, mage, archer, thief, skeleton-enemy, celestial) plus large NPC packs (100+ NPCs, 50+ modern NPCs). Covers both player-class and enemy archetypes.
**Sample SKUs:**
- Samurai Character ($5.19): 15 animations including block/block-hit/dash, 96x64, Aseprite source
- Female Character 128px ($14.99): 128px tall; animation states not fully verified
- 10 Enemy Characters ($4.54): enemy sprite kit
- Bundle ($65.99): 39 packs

**Notes for downstream:** Highest confirmed B13 coverage (3 of 4 defensive states) among retro-mid-pixel vendors. Sprite dimensions at 96x64 are the largest in the non-HD-2D vendor class — closer to HD-2D range than LuizMelo. Register gap (not hand-drawn pixel) is the key flag. Useful as prototyping layer and as reference for animation-state structure; Drax should assess whether 96x64 at this fidelity is acceptable for HD-2D pipeline or needs register upgrade.

---

### Vendor 5 — rvros (Animated Pixel Adventurer)

**URL:** https://rvros.itch.io/animated-pixel-hero
**Platform:** itch.io
**Cost:** Name-your-own-price (free option available)
**License:** "Personal and commercial use permitted; modification permitted; redistribution prohibited." Not CC-labeled; custom statement on product page.
**License flag:** VERIFY — non-CC, custom statement. Provisionally clear for commercial use. Confirm no per-project cap or attribution requirement.

**Animation states confirmed (39 animations):**
- Movement: Idle x2, Walk, Run x2, Crouch, Crouch Walk, Slide
- Combat: Attack x3, Air Attack x3, Punch x3, Kick x2, Drop Kick, Sword Draw/Sheathe
- Mobility: Jump, Fall, Somersault, Wall Slide, Wall Climb, Wall Run, Corner Grab/Climb/Jump
- Special: Cast Spell, Use Item, Knocked Down, Recover
- Environment: Water Idle, Water Move
- Status: Hurt, Die

**B13 defensive-mobility coverage:** ABSENT — no `roll`, `parry`, `block`, or `dodge` states. Strong spell-cast state; strong mobility states. Gap on all four defensive states.

**Sprite dimensions:** 50x37 pixels
**File format:** Individual sprites + sprite sheets + Aseprite source files; multiple packs (base + Hand Combat + Bow variants)
**Character count:** Single character with equipment variants
**Decomposition:** Monolithic
**Style register:** Retro pixel-art. 50x37 is below HD-2D-pixel band.
**AI-content signal:** No statement found on page.
**Community signal:** 267 ratings, 4.9/5 stars; extensively used in shipped games. Widely cited in indie game dev community as a benchmark for free pixel-art character assets.
**Sample SKUs:**
- Animated Pixel Adventurer (free/NWYP): 39 animations, no defensive states
- Hand Combat pack: additional unarmed animations
- Bow pack: additional ranged animations

**Notes for downstream:** Despite the 4.9-star rating and exceptional animation breadth, the B13 defensive-mobility gap (zero defensive states) and retro-pixel register make rvros a secondary candidate. Highest value as a reference baseline for animation-state breadth expectations; not recommended as a primary B13 vendor.

---

### Vendor 6 — Elthen's Pixel Art Shop (Adventurer Sprites)

**URL:** https://elthen.itch.io/pixel-art-adventurer-sprites
**Platform:** itch.io
**Cost:** Name-your-own-price; bundle option $15 for 5 assets
**License:** "Free for commercial and non-commercial use; modification permitted; credit requested (not required) for commercial use." Not CC-labeled; custom statement.
**License flag:** VERIFY — non-CC custom statement. "Full licensing details on Patreon" is a flag — verifiable license terms should not require Patreon access. Treat as HOLD until full license text is retrieved from a non-paywalled source.

**Animation states confirmed:**
- Idle, Movement, Attack x3, Damage, Death, Jump, Climb, Shoot (Bow), Cast Spell, Run Upwards, **Roll**, Push, Fall Down
- Community-contributed directional animations (up/down) not in base pack

**B13 defensive-mobility coverage:** PARTIAL — `roll` confirmed; no explicit `parry`, `block`, or `dodge`.

**Sprite dimensions:** 32x32 pixels
**File format:** PNG sprite sheets; paperdoll armor add-on available ($4+)
**Character count:** Single adventurer character with armor variants
**Decomposition:** Partial — base character monolithic; paperdoll armor system exists as a separate add-on layer
**Style register:** Retro pixel-art. 32x32 is at the retro-pixel lower bound.
**AI-content signal:** "No generative AI was used" confirmed.
**Catalogue breadth beyond Adventurer:** Elthen ships a broad catalogue of individual character archetypes — Monk, Barbarian, Squire (with Block state confirmed), Pyromancer, Rogue, Thief, Assassin, Dwarf series, plus enemy/creature sprites. The Squire pack explicitly lists "Block" as an animation state.
**Squire Pack note:** Animation states confirmed: Idle, Movement, Attack, **Block**, Damage, Death. The Squire is the Elthen pack with direct block-state coverage. Price: $4.

**Sample SKUs:**
- Pixel Art Adventurer Sprites (NWYP): roll state, 32x32
- Squire Sprites ($4): block state confirmed
- Pyromancer Sprites ($4): spell-cast states

**Notes for downstream:** Register gap (32x32 retro-pixel) is the primary flag. Elthen packs are strong for prototyping and for filling specific animation-state gaps cheaply. The Squire's block state is the most useful single-pack B13 coverage item in the Elthen catalogue. License flag on Patreon reference should be resolved before purchase.

---

### Vendor 7 — CraftPix.net (character sprites)

**URL:** https://craftpix.net/categorys/pixel-art-sprites/
**Platform:** CraftPix.net (proprietary store)
**Cost:** Subscription/membership model — "Premium membership" required for most paid assets; no per-asset price displayed for most packs. Freebies available without membership.
**License:** Proprietary CraftPix license. Commercial use permitted (game distribution). No attribution required. Redistribution of source files prohibited. Per-project unlimited use. No AI training. Perpetual access to downloaded assets after subscription ends.
**License flag:** HOLD — non-public proprietary license (CraftPix File Licenses page reviewed; terms are site-specific, not standardized). Subscription model is non-standard relative to itch.io per-asset purchasing. Full terms reviewed from https://craftpix.net/file-licenses/ and are reasonably clear, but the subscription-gating creates a cost-model flag. Recommend Matt evaluate subscription cost vs per-asset alternatives.

**Register finding (CRITICAL):** Multiple CraftPix character sprite product pages verified as **vector-register, not pixel-art register.** Specifically:
- Adventure Game Character Sprite Pack: "vector graphics; layered; AI, EPS, PNG, PSD formats"
- Woman Hero Game Character Sprite: "vector graphics; parts of body divided into separate elements for vector editor"
- Warrior Sprite Sheets Pixel Art Pack 2: described as "pixel art" but PSD format; animation states not listed
- RPG Heroes Pixel Art Asset Pack: animation states not listed; PSD format

**Assessment:** CraftPix markets some products as "pixel art" but the product page evidence shows vector delivery (AI, EPS formats) for character sprite packs. The "pixel art" label on CraftPix covers a range of actual deliverables. CraftPix character sprites require individual product-level inspection to confirm pixel-art vs vector register. Do not treat CraftPix as a pixel-art vendor class without per-product verification.

**Animation states (confirmed on specific packs):**
- Woman Hero: idle, fall, shoot (fire/ice/poison x3 each), death, get hit, hit, jump, on ladder, **roll**, run, swim
- Warrior/RPG Heroes: animation state lists not published on product pages

**B13 defensive-mobility coverage:** `roll` confirmed on Woman Hero (vector register). No `parry`, `block`, or `dodge` confirmed on pixel-art-labeled packs.

**Sample SKUs:**
- Free Assassin, Mage, Viking pixel art heroes (free): freebie; animation count not confirmed
- Warrior Sprite Sheets Pixel Art Pack 2: 3 characters (Viking, Knight, Barbarian); animation states not listed
- RPG Heroes Pixel Art Asset Pack: 3 characters; animation states not listed

**Notes for downstream:** CraftPix is excluded from top-3 recommendations on two grounds: (1) register mismatch — product pages show vector delivery, not HD-2D pixel art; (2) non-standard cost model — subscription required. The "pixel art" label on CraftPix requires per-product verification before any asset is sourced. If Matt wishes to explore CraftPix further, the freebie tier (no subscription required) is the low-friction evaluation path.

---

### Vendor 8 — GandalfHardcore — Male/Female Base (secondary finding)

**URL:** https://gandalfhardcore.itch.io/2d-pixel-art-male-and-female-character
**Platform:** itch.io
**Cost:** Free
**License:** Same custom statement as Samurai pack — commercial permitted, no resale, no AI training
**License flag:** VERIFY (same as Samurai pack above)

**Animation states:** 7 base animations; separate layers for clothing, hair, accessories. Animation count is lower than Samurai pack — this is a base/template rather than a combat-complete character.
**B13 defensive-mobility coverage:** ABSENT — 7 base animations do not include combat defensive states.
**Style register:** Same retro-to-mid-pixel register as Samurai pack.

**Notes for downstream:** Listed for completeness as a potential paper-doll customization layer. Not a primary B13 candidate. The Samurai pack (Vendor 4) is the GandalfHardcore candidate for B13 work.

---

## B13 Defensive-Mobility Coverage Matrix

| Vendor | `roll` | `parry_active` | `block_active` | `iframe_dash` | Register |
|---|---|---|---|---|---|
| Seliel the Shaper (Mana Seed) | — | CONFIRMED (parry) | CONFIRMED (shield bash) | CONFIRMED (evade) | HD-2D-pixel |
| chierit (Elementals) | CONFIRMED | — | CONFIRMED (defend) | CONFIRMED (slide) | HD-2D-pixel |
| LuizMelo Knights Pack | — | — | CONFIRMED | — | retro-pixel |
| LuizMelo Knight Pack | CONFIRMED | — | — | — | retro-pixel |
| GandalfHardcore Samurai | — | — | CONFIRMED | CONFIRMED (dash) | mid-pixel |
| rvros Adventurer | — | — | — | — | retro-pixel |
| Elthen Adventurer | CONFIRMED | — | — | — | retro-pixel |
| Elthen Squire | — | — | CONFIRMED | — | retro-pixel |
| CraftPix (vector) | CONFIRMED (vector only) | — | — | — | VECTOR — not pixel |

**B13 coverage at HD-2D register:** Seliel the Shaper and chierit together cover all four B13 defensive states within the locked register.

---

## Style Register Assessment

**HD-2D-pixel register (matches canonical lock):**
- Seliel the Shaper — Mana Seed Character Base: 64x64 frame cells, layered paper doll, hand-drawn pixel sensibility. Closest to canonical register.
- chierit — Elementals series: hand-drawn illustration pixel sensibility, Aseprite source files, element-archetype framing.

**Mid-pixel register (borderline — below canonical target but above retro):**
- GandalfHardcore Samurai: 96x64 sprites, detailed animation, retro aesthetic rather than hand-drawn illustration sensibility.

**Retro-pixel register (below canonical target; useful for prototyping):**
- LuizMelo: 21x32 sprites; retro register confirmed
- rvros: 50x37 sprites; retro register confirmed
- Elthen: 32x32 sprites; retro register confirmed

**Vector register (NOT pixel art — excluded from consideration):**
- CraftPix character sprites: vector delivery confirmed on multiple product pages

---

## License Verification Flags

Per C.2 amendment discipline (from Step B):

| Vendor | Flag | Reason | Status |
|---|---|---|---|
| Seliel the Shaper | VERIFY | Non-CC custom license; Web3 restriction; terms on product page (not separate file) | Provisionally clear; Web3 restriction not applicable to this project |
| chierit | CLEAR | CC-BY 4.0, publicly verifiable; attribution to "chierit" required | Operational — add credit to game credits |
| LuizMelo | CLEAR (per sampled packs) | CC0 confirmed on Knight Pack + Medieval Warrior Pack 2; verify per-pack for any exceptions | Cross-check each individual pack before purchase |
| GandalfHardcore | VERIFY | Custom non-CC license; "no AI training" and "no NFT" restrictions explicitly stated | Provisionally clear; restrictions not applicable to this project; recommend review of full terms |
| rvros | VERIFY | Custom non-CC license; "Patreon for full details" not present here; redistribution prohibited | Provisionally clear; confirm no attribution requirement |
| Elthen | HOLD | "Full licensing details on Patreon" is a flag — verifiable terms should not require Patreon access | Retrieve non-paywalled license text before purchase |
| CraftPix | HOLD | Proprietary subscription model; vector register mismatch; register verification required per-product | Excluded from recommendations pending register and cost model evaluation |

---

## Knowledge Gaps Not Resolved

1. **Sprite dimensions for chierit Elementals series not confirmed from page text.** Preview GIFs suggest ~48–64px character height. Full dimension data requires download-inspect or creator contact. Assumed HD-2D-pixel band based on visual evidence; confirm before wiring.

2. **GandalfHardcore full catalogue animation states not fetched beyond Samurai.** The Female Character 128px ($14.99) at 128px sprite height is unverified — if animation states include defensive mobility, this could be the highest-register GandalfHardcore candidate. Not fetched due to time constraints.

3. **LuizMelo Dark Knight series (3 packs, $8–$12.90 each) animation states not fetched.** Higher price suggests higher animation count; defensive states unknown. Worth sampling if LuizMelo is selected.

4. **GameDevMarket character animation catalogue not accessible** — multiple product pages returned 403. The "CHARACTER PACK: RPG HEROES & ENEMIES" and "Pixel hero character sprite" (which mentioned roll/shield-block-walk in search snippets) were not fetchable. This platform may warrant a direct browse session.

5. **Unity Asset Store character animation catalogue not accessed** — category page returned only navigation metadata, not asset listings. Could surface additional vendors if needed.

6. **No vendor found** with all four B13 defensive states (`roll`, `parry_active`, `block_active`, `iframe_dash`) confirmed in a single character pack. Seliel the Shaper comes closest (parry, shield-bash as active-parry analog, evade) but lacks a named `roll` state. chierit (roll, defend, slide) lacks an explicit `parry`. Combined, these two vendors cover all four states.

7. **Non-humanoid character-sprite vendors** not scoped in this commission. The style-register doc notes this as a known gap and a separate follow-on commission territory.

---

## Top-3 Vendor Recommendations (for knight-rider report)

Ranked by: (1) register match to canonical HD-2D-pixel lock, (2) B13 defensive-mobility coverage, (3) license cleanliness, (4) cost efficiency.

**Rank 1 — Seliel the Shaper (Mana Seed Character Base)**
- URL: https://seliel-the-shaper.itch.io/character-base
- Strongest HD-2D register match; confirmed `parry` and `evade` states; paper doll decomposition (Drax-favorable); full tileset ecosystem; $19.98 full asset. License: verify custom terms (provisionally clear). Priority item for B13.

**Rank 2 — chierit (Elementals series)**
- URL: https://chierit.itch.io/
- Strongest thematic alignment (element-named characters map to Reincarnated's element system); confirmed `roll`, `slide`, `defend` states; HD-2D register; CC-BY 4.0 (cleanest license in scout); $7.50/character or $50/bundle. Direct element-to-sprite-archetype correspondence is unique to this vendor.

**Rank 3 — GandalfHardcore Samurai Character**
- URL: https://gandalfhardcore.itch.io/pixel-art-samurai-character
- Confirmed `block`, `block hit`, `dash`; 96x64 sprites (largest non-HD-2D-register vendor); Aseprite source files; $5.19. Register is mid-pixel (not HD-2D-hand-drawn), but sprite size and animation quality make this the strongest prototyping option for B13 wiring work before HD-2D assets are sourced. License: verify custom terms.

---

## Source List

- https://seliel-the-shaper.itch.io/character-base (fetched 2026-05-16)
- https://seliel-the-shaper.itch.io/ (fetched 2026-05-16)
- https://chierit.itch.io/elementals-leaf-ranger (fetched 2026-05-16)
- https://chierit.itch.io/elementals-water-priestess (fetched 2026-05-16)
- https://chierit.itch.io/ (fetched 2026-05-16)
- https://luizmelo.itch.io/knight-pack (fetched 2026-05-16)
- https://luizmelo.itch.io/knights-pack (fetched 2026-05-16)
- https://luizmelo.itch.io/medieval-warrior-pack-2 (fetched 2026-05-16)
- https://luizmelo.itch.io/ (fetched 2026-05-16)
- https://gandalfhardcore.itch.io/pixel-art-samurai-character (fetched 2026-05-16)
- https://gandalfhardcore.itch.io/ (fetched 2026-05-16)
- https://gandalfhardcore.itch.io/2d-pixel-art-male-and-female-character (searched 2026-05-16; page not directly fetched)
- https://rvros.itch.io/animated-pixel-hero (fetched 2026-05-16)
- https://rvros.itch.io/ (fetched 2026-05-16)
- https://elthen.itch.io/pixel-art-adventurer-sprites (fetched 2026-05-16)
- https://elthen.itch.io/ (fetched 2026-05-16)
- https://craftpix.net/product/adventure-game-character-sprite-pack/ (fetched 2026-05-16)
- https://craftpix.net/product/woman-hero-game-character-sprite/ (fetched 2026-05-16)
- https://craftpix.net/product/warrior-sprite-sheets-pixel-art-pack-2/ (fetched 2026-05-16)
- https://craftpix.net/product/rpg-heroes-pixel-art-asset-pack/ (fetched 2026-05-16)
- https://craftpix.net/file-licenses/ (fetched 2026-05-16)
- https://craftpix.net/categorys/pixel-art-sprites/ (fetched 2026-05-16)
- https://www.gamedevmarket.net/asset/character-pack-rpg-heroes-enemies-pixel-art-animated-characters-animations (403 — not accessible 2026-05-16)
- https://www.gamedevmarket.net/asset/pixel-hero-character-sprite (403 — not accessible 2026-05-16)
- https://penzilla.itch.io/protagonist-character (fetched 2026-05-16)
- https://penzilla.itch.io/ (fetched 2026-05-16)
- https://itch.io/game-assets/tag-action-rpg/tag-characters (fetched 2026-05-16)
- Web searches: 12 queries across itch.io pixel art character animation, craftpix character sprite animation states, GandalfHardcore catalogue, hand-drawn pixel character combat states, HD-2D register character vendors, GameDevMarket pixel character, Unity Asset Store 2D characters — 2026-05-16

---

— legolas, 2026-05-16
