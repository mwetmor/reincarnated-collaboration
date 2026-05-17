# Environment Tileset Vendor Scout — 2026-05-17

**Mode:** B (systematic catalogue crawl)
**Commissioner:** knight-rider (per Matt direct authorization 2026-05-17; gandalf commission `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-legolas-mode-b-environment-tileset-catalogue-sweep-vs2a.md`
**Crawl date:** 2026-05-17
**Time spent:** ~4h
**Time cap:** 8h (honored)

---

## Section 1 — Methodology + Scope

### Style register target

Hand-drawn pixel-art (HD-2D-shaped), Candidate B per `canonical/story/style-register.md`. NOT retro Stardew-class (16-bit minimal, SNES-era). NOT vector. NOT anime hand-drawn. The target register is the Octopath Traveler / Sea of Stars / Eastward aesthetic: pixel-resolution art with hand-drawn illustration sensibility, higher fidelity than retro but within the pixel-art medium.

**Critical finding on register availability:** The top-down dungeon tileset landscape is overwhelmingly retro-pixel-art (16x16, 32x32, 16-bit aesthetic). Genuine HD-2D-quality tilesets (matching the register of chierit Elementals at their aesthetic intent) are scarce in the top-down dungeon interior category. Most Tier-1 vendors (Elthen, Foozle Lucifer, Seliel the Shaper, Pipoya) explicitly self-describe as SNES-era retro or 16-bit style. The best-fit candidates lean toward "higher-fidelity retro" rather than pure HD-2D. Gandalf will need to assess borderline packs via sample images.

### Three sourcing categories (per Amendment 1)

- **MAP** — full room-sized image shipped as single asset (e.g., 1440×1440 px painted scene)
- **BACKGROUND_PIECE** — large background panel filling significant room portion (e.g., 1920×1080 scene usable as room fill)
- **TILESET** — small repeating units (16×16 / 32×32 / 48×48 / 64×64) tiled across floor + wall surface
- **MIXED** — pack ships tileset + complementary larger pieces together

### Room dimension fit annotation rules (per Amendment 2)

Target room dimensions: 720×720 px (15m small), 1440×1440 px (30m default), 2160×2160 px (45m large) at 48 px/m.

For TILESET category:
- EXACT_FIT_SMALL: ≥4 floor + ≥4 wall variants
- EXACT_FIT_DEFAULT: ≥8 floor + ≥6 wall variants
- EXACT_FIT_LARGE: ≥12 floor + ≥8 wall variants + prop variety
- MULTI_BAND: cleanly covers ≥2 size bands
- UNDER_VARIETY: too few variants for default-room credible fill

For MAP/BACKGROUND_PIECE category: ships at or scalable to target dimensions.

**Tile scale compatibility note:** At 48 px/m (the project's rendering anchor), a 32×32 px tile = 0.667m rendered per tile side. A 48×48 px tile = exactly 1m per tile side. A 64×64 px tile = 1.333m. All three are compatible — 32×32 tiles produce slightly denser grid, 48×48 is exact-meter match, 64×64 is coarser grid. A 720×720 px room needs 22.5×22.5 tiles at 32px, 15×15 at 48px, or 11.25×11.25 at 64px.

### License criteria

Preferred: CC0, CC-BY, or commercial-royalty-free (pay-once, use commercially). Flagged: subscription gating (CraftPix premium), unclear Patreon-linked terms, AI-Assisted disclosure.

### "Each room is independent" framing (per Amendment 3)

Pack selection does not require multi-room coherence. A pack covering one great thematic room type is valid. Did not hunt for packs requiring wall-to-wall tile coherence across room boundaries.

---

## Section 2 — Vendor-by-Vendor Scout

### Vendor 1 — Pimen (pimen.itch.io)

**Environment coverage: ZERO**

Pimen produces exclusively VFX and spell effect packs (elemental, buff/debuff, explosion, smoke). No tilesets, no room backgrounds, no environment assets of any kind in the catalogue. Confirmed across full catalogue sweep.

**Environment verdict: SKIP. No relevant environment assets.**

---

### Vendor 2 — CreativeKind (creativekind.itch.io)

**Environment coverage: MINIMAL (individual structures only)**

CreativeKind focuses on character animations and VFX. No comprehensive environment tileset packs. However, they do offer individual structure/prop assets (Dark Tower $2, Demon Gate $3, Crystal Tower $2, Totem, Altar, Statue variants) under their "Pixel Structures" collection. These could supplement prop layers if a tileset's prop coverage is thin.

**Individual structure assets:** ~10–15 items, priced $2–$3 each, pixel art register consistent with their character packs (hand-drawn pixel, higher fidelity).

**Environment verdict: NO tileset packs. WATCH as prop-layer supplement source. Pixel register is likely higher-fidelity than retro vendors.**

---

### Vendor 3 — Ansimuz (ansimuz.itch.io)

**Environment coverage: MODERATE but register mismatch**

Ansimuz has extensive environment assets across multiple themed collections (Gothicvania, Warped, SunnyLand, etc.) but ALL are sidescrolling platformer assets — not top-down. Confirmed: Legend of Faune (top-down Zelda-like) uses 16×16 tiles, retro register, beach/outdoor theme, CC0. "Tiny RPG Dungeon" is described as top-down but is also retro register.

**Style register assessment:** Retro pixel-art across the board. The Gothicvania series (castles, swamps, churches) is visually strong for the dark-fantasy genre but is explicitly a side-scroller / Castlevania-style register. NOT compatible with the project's top-down room/hallway topology.

Top-down packs found:
- **Tiny RPG Dungeon** — top-down, 16×16, retro. CC0-adjacent (name-your-price). Stone dungeon interior.
- **Legend of Faune** — top-down, 16×16, CC0, beach tileset. Theme mismatch.

**Environment verdict: UNDER VARIETY / REGISTER MISMATCH. Tiny RPG Dungeon is the only top-down interior option; retro register, minimal variants. Not a primary candidate.**

---

### Vendor 4 — Pipoya (pipoya.itch.io)

**Environment coverage: BASIC free tilesets, retro register**

Pipoya produces RPG-style free tilesets:
- **FREE RPG Tileset 16×16** — CC0, retro
- **FREE RPG Tileset 32×32** — CC0, retro
- **PIPOYA FREE RPG World Tileset 32×32 / 40×40 / 48×48** — CC0, overworld/exterior focus

48×48 format is noted (exactly 1m/tile at 48 px/m scale). However, Pipoya's tilesets are exterior/overworld themed, not dungeon interior. Style register is retro 16-bit RPG Maker-adjacent.

**Environment verdict: FREE and CC0 but EXTERIOR focus, RETRO register. UNDER VARIETY for dungeon interior. Not a primary candidate.**

---

### Vendor 5 — Foozle (foozlecc.itch.io)

**Environment coverage: MODERATE — top-down dungeon tilesets, free, CC0, retro register**

Foozle's Lucifer Collection is the most complete top-down dungeon ecosystem on itch.io at the free/CC0 tier:

**Lucifer — Dungeon Tileset**
- URL: https://foozlecc.itch.io/lucifer-dungeon-tileset
- Tile dimensions: 32×32 px
- Perspective: Top-down confirmed
- License: CC0 1.0 — free for all projects including commercial, attribution not required
- Price: Name-your-own (free)
- Coverage: Floor tiles, wall tiles, dungeon environmental elements. Includes .ase (Aseprite) source files. Retro aesthetic, stone-gray dungeon.
- File size: 149 kB zip
- Style register: Retro pixel-art (classic dungeon crawler aesthetic, not HD-2D)

**Lucifer — Lava Dungeon Tileset**
- URL: https://foozlecc.itch.io/lucifer-lava-dungeon-tileset
- Tile dimensions: 32×32 px
- License: CC0 1.0
- Price: Free
- Coverage: Floor tiles, wall tiles, props, animated lava streams/bubbles/effects. PNG + .ase source files.
- Theme: Lava dungeon — fire/volcanic season fit

**Lucifer — Desert Tileset**
- URL: https://foozlecc.itch.io/lucifer-desert-tileset
- License: CC0 1.0 / Free
- Theme: Desert exterior (less dungeon-interior fit)

**Lucifer — Exterior Tileset**
- URL: https://foozlecc.itch.io/lucifer-exterior-tileset
- Theme: Exterior (out of scope for interior room system)

**Foozle ecosystem note:** The Lucifer Collection also ships characters (Warrior, Necromancer, Sorceress), enemies (Skeleton King, Goblin Rider, Cultist, Possessed, etc.), and a Diablo-style RPG UI — notable for its genre alignment with Reincarnated's ARPG framing. The Lucifer aesthetic consistently evokes Diablo-I/II era dungeon crawlers.

**Style register assessment:** Retro pixel-art but tonally appropriate (dark dungeon aesthetic, Diablo-genre adjacent). Tile variant counts not explicitly stated in documentation; pack sizes suggest moderate variant counts (149 kB = limited spritesheet).

**Foozle environment verdict: CANDIDATE (secondary). CC0 license is optimal. Theme and genre fit are good (Diablo-era). Register is retro not HD-2D — flagged for gandalf assessment. Best path: acquisition is free, use as placeholder-upgrade or VS2b-expansion while sourcing HD-2D-register primary.**

---

### Vendor 6 — Elthen (elthen.itch.io) — LIKELY-HIGH-FIT per gandalf commission

**Environment coverage: VERY HIGH — 29+ thematic tileset packs, all top-down, all $10**

Elthen is the deepest tileset catalogue among the Tier-1 vendors. 29+ packs confirmed, each $10 (or $160 for a 31-pack bundle), all top-down, all 32×32 tiles.

**License terms:** Commercial and personal use permitted. No blockchain/crypto. No AI training. Attribution: credit appreciated but appears optional (confirmed via community post: "Feel free to use the sprites in commercial/non-commercial projects"). "No generative AI was used" on all packs.

**Style register assessment:** Elthen's tilesets are labeled "Pixel Art / Retro / Fantasy" across all packs. However, community commentary describes the aesthetic as having "really fkin appealing stylization" — suggesting quality above baseline retro. The Lizardfolk Temple pack was assessed as "hand-drawn pixel art at moderate-to-high fidelity; consistent with creator's fantasy asset portfolio using carefully crafted sprite work rather than retro 16-bit minimalism." This is the closest Tier-1 vendor to HD-2D-adjacent. Tile dimensions (32×32) are smaller than ideal for HD-2D register but the artistic intent is higher-fidelity.

**Register judgment:** Borderline. Elthen is above Foozle/Ansimuz/Seliel in artistic intent but below true HD-2D (Octopath Traveler environmental quality). Flag for gandalf visual inspection — some packs may qualify, some may not.

**Key packs for ARPG dungeon theming:**

1. **2D Pixel Art Arcane Dungeons Tileset** — https://elthen.itch.io/2d-pixel-art-arcane-dungeons-tileset — $10 — Arcane/magical dungeon, animated energy pipes/barriers/torches/crystals, 32×32, top-down, 125 kB zip. Multiple animated elements.

2. **2D Pixel Art Lava Dungeons Tileset** — https://elthen.itch.io/2d-pixel-art-lava-dungeons-tileset — $10 — Lava dungeon with animated lava bubbles/streams/waterfall, 32×32, top-down, PNG + JSON. Fire/volcanic theme.

3. **2D Pixel Art Cultist Dungeons Tileset** — https://elthen.itch.io/2d-pixel-art-cultist-dungeons-tileset — $10 — Occult dungeon, rotating puzzle pillars with 8 occult symbols, stone gates, 3 portal variants, spike/spear traps. 10 files. Cult/dark-magic theme.

4. **2D Pixel Art Volcanic - Lava Tileset** — https://elthen.itch.io/2d-pixel-art-volcanic-lava-tileset — $10 — Volcanic, animated lava/fire/smoke, 32×32, PNG + JSON. Overlaps with lava dungeons but different set.

5. **2D Pixel Art Dwarven Caves Tileset** — https://elthen.itch.io/2d-pixel-art-dwarven-caves-tileset — $10 — Dwarven cave, 32×32, top-down. Two files (Brazier-sheet.png + Dwarven Caves Tileset.png). Cave/underground theme.

6. **2D Pixel Art Haunted Mansion Tileset** — https://elthen.itch.io/2d-pixel-art-haunted-mansion-tileset — $10 — Haunted interior, fireplace, floating furniture variants, plants, vases. 81 kB main tileset. Gothic/mansion theme.

7. **2D Pixel Art Hell Tileset** — https://elthen.itch.io/2d-pixel-art-hell-tileset — $10 — Infernal, animated lava waterfalls/bubbles/fire, 32×32. 42 kB.

8. **2D Pixel Art Pyramid Interior Tileset** — https://elthen.itch.io/2d-pixel-art-pyramid-interior-tileset — $10 — Egyptian pyramid interior, animated door-drop/brazier/sandfall. 23 kB main tileset + 3 animated elements.

9. **2D Pixel Art Lizardfolk Temple Tileset** — https://elthen.itch.io/2d-pixel-art-lizardfolk-temple-tileset — $10 — Temple/reptilian, animated water, 32×32, top-down. 15 kB spritesheet (small pack).

10. **2D Pixel Art Dungeon Tileset** — https://elthen.itch.io/2d-pixel-art-dungeon-tileset — Name-your-price (free option) — Generic stone dungeon, 32×32, top-down, commercial use confirmed, attribution required. 47 kB.

11. **2D Pixel Art Medieval House Interior Tileset** — https://elthen.itch.io/2d-pixel-art-medieval-house-interior-tileset — $10 — Medieval interior, animated fireplace (two variants: with/without pot). 3 PNG files. Interior/domestic theme.

12. **2D Pixel Art Nightmarescape Tileset** — https://elthen.itch.io/2d-pixel-art-nightmarescape-tileset — $10 — Dark horror/nightmare, compatible with Forest Tileset, 105 kB. Horror/surreal theme.

13. **2D Pixel Art Magic Wasteland Tileset** — https://elthen.itch.io/2d-pixel-art-magic-wasteland-tileset — $10 — Corrupted wasteland, animated fissures/corrupted trees/toxic bubbles, 13 files total. Corrupted-nature theme.

14. **2D Pixel Art Arctic Tileset** — https://elthen.itch.io/2d-pixel-art-arctic-tileset — $10 — Arctic/ice, 32×32.

**Bundle:** 31 tilesets for $160 (avg $5.16/each) — cost-effective if acquiring multiple.

**Elthen environment verdict: PRIMARY CANDIDATE POOL. 10–14 packs have ARPG-dungeon-theming relevance. License is clean for commercial use. Tile variant counts are not explicitly documented (requires download to verify); pack file sizes suggest moderate variant depth. Register is borderline HD-2D — flagged for gandalf visual inspection. The bundle at $160 provides comprehensive seasonal theme coverage across many seasons.**

---

### Vendor 7 — CraftPix (craftpix.net) — Drift-13 filter applied

**Environment coverage: MIXED register — filtered per Drift-13 lesson**

CraftPix ships both pixel-art and vector environment packs. Filter applied: pixel-art only.

**Confirmed VECTOR (eliminated per Drift-13):**
- 2D Top Down Dungeon Tileset — $5.50 — 256×256 px tiles, AI/EPS/PNG vector format, explicitly vector
- Multiple other dungeon packs in vector register

**Pixel-art packs identified:**
- **Free 2D Top-Down Pixel Dungeon Asset Pack** — FREE — Royalty-free commercial use. Animated torches, chests, traps, water. PNG + PSD. Created March 2025. Tile dimensions not stated. Retro-pixel register.
- **Top-Down Dungeon Pixel Tileset (RPG/Roguelike)** — Premium membership gated — 16×16 tiles, "hundreds of handcrafted pieces," traps/props/animated elements. Retro pixel.
- **Medieval Interior Top Down Pixel Art Tileset** — Premium membership gated — Available in 16×16, 32×32, 48×48, and 64×64 px variants. Medieval interior: walls, stairs, windows, doors, drawers, shelves, bed. Retro pixel but 48×48 option is dimensional-fit compatible.
- **Cave Tileset Top Down Pixel Art** — Premium membership gated — Cave labyrinth, crystals/stalagmites/lava vents/mushrooms/altars. PNG + PSD.

**License/cost model flag:** CraftPix premium packs require subscription membership (described as "$4,850+ value for 98% savings"). Some individual packs have standalone prices ($5.50). The free pack is download-available without membership. The subscription model is non-standard relative to itch.io one-time purchase convention.

**CraftPix environment verdict: FREE PACK is a viable secondary candidate (retro register, no cost, commercial-use). Premium packs require subscription evaluation — the Medieval Interior at 48×48 is the most dimensionally compatible. Register across all pixel packs is retro, not HD-2D. NOT a primary candidate for VS2a given register mismatch and cost model complexity.**

---

### Additional Vendors Discovered During Crawl

The crawl surfaced several non-Tier-1 vendors with relevant environment packs:

#### Seliel the Shaper (seliel-the-shaper.itch.io) — Mana Seed ecosystem

Seliel has the deepest single-creator tileset ecosystem on itch.io — 25+ tileset packs all compatible with each other (Mana Seed system). All are 16×16 tiles, explicitly SNES-era retro ("16-bit-style," "100% HUMAN-MADE / NO AI"). Paper doll character system and extensive tileset ecosystem. Top-down.

Key dungeon packs:
- **Eternal Dungeon** — $14.99 — 16×16, SNES-retro, 2 floor types + 2 wall types with 7 layer styles, columns/archways/pillars/obelisks/altars, 4-frame brazier animation. Floor variants: 2. Wall variants: 2 with layerable styles. UNDER_VARIETY for default room fill at 16×16.
- **Castle Dungeon** — $17.99 — 16×16, SNES-retro, stone walls with variable heights, doors, stairs, columns, prison cells, spike traps, rugs, animated secrets. 3 palette variants.
- **Fortified Keep** — $19.99 — 16×16, castle interior/exterior, walls/doors/windows/banners/stairs. Explicitly "retro SNES-style."

**License:** "Mana Seed User License" — commercial use permitted, Web3 explicitly blocked.

**Seliel verdict:** UNDER VARIETY + RETRO REGISTER. 16×16 tiles at retro scale. Does not meet HD-2D register. Good ecosystem compatibility for future open-world or exterior work but not the ARPG interior dungeon target. NOT a primary candidate for VS2a.

#### Kokoro Reflections (kokororeflections.itch.io) — "KR Legendary Palaces" series

Kokoro Reflections ships a series of thematic "Legendary Palace" interior tilesets at 48×48 AND 32×32 (both included). Commercial use explicitly included. Price range $8.99–$15.99. "No generative AI was used."

**Tile dimensions: 48×48 px primary (32×32 also included) — EXACT meter-match at 48 px/m scale.**

The 48×48 tile size is the exact match for the project's PIXELS_PER_METER=48 anchor. One tile = one meter at native scale.

Key packs:
1. **KR Legendary Palaces ~ Reaper Tileset** — $9.99 — 48×48 and 32×32. Top-down. Theme: death/undead palace with fog effects. Ground: foggy gray surfaces, dismal purple water, fancy floor tiles, spike traps, fog overlays. Walls: fog-wrapped. Props: stairs, pillars, arches, raised platforms, throne, windows, treasure chest, push block, bridge rails, statues, magic rings, chains, lanterns, diagonal stairs, ladders, gravestones. Animated: treasure chest, fire animations (black/white/purple). Overlays: fog layers (black+white), parallax background. 8.5 MB zip. URL: https://kokororeflections.itch.io/kr-legendary-palaces-reaper-tileset-for-rpgs

2. **KR Legendary Palaces ~ Phoenix Tileset** — $9.99 — 48×48 and 32×32. Top-down. Theme: fire/lava palace. Ground: lava variants, dark ground, fiery orange-edged tiles, purple contrast, glittery fire paths, spike traps, fiery weeds. Walls: dark and light stone with orange tones. Props: accent pillars, arches, raised platforms, throne, fire-windows (small/large), treasure box, push block, bridge rails, statues, magic rings, glowing lanterns. Animated: treasure chest, fire torches. 7.4 MB zip. URL: https://kokororeflections.itch.io/kr-legendary-palaces-phoenix-tileset-for-rpgs

3. **KR Legendary Palaces ~ Naga Tileset** — $8.99 — 48×48 and 32×32. Top-down. Theme: serpentine palace ("lair of the queen of snakes"). Ground: water, marble (black/teal/purple/gold), scale floors, scale gold-edged, decorative edges, spikes, pits, gold edging. Walls: matching per floor type with coordinated roofs. Props: stairs, pillars, arches, raised platforms, throne, windows (small/large), animated treasure chest, push blocks, bridge rails, statues, magic rings, diagonal stairs, ladders (3 designs), snake-themed wall decor, jewels. 13 MB zip. URL: https://kokororeflections.itch.io/kr-legendary-palaces-naga-tileset-for-rpgs

4. **KR Wizard's Hideout** — $8.99 — 48×48 and 32×32. Top-down. Theme: wizard cavern. Contents: cavern walls/details, colorful crystals, magical implements, potion bottles, shelving with books, crystal balls. URL: https://kokororeflections.itch.io/kr-wizards-hideout-for-rpgs

5. **KR Snow Castle Tileset** — $15.99 — 48×48 and 32×32. Theme: ice/snow castle interior. URL: https://kokororeflections.itch.io/kr-snow-castle-tileset-for-rpgs

**Style register assessment:** Kokoro Reflections is described by reviewers as high-quality (5.0/5 stars across packs). The 48×48 tile dimension, rich prop coverage, and thematic variety suggest higher fidelity than typical 16-bit retro. The Reaper/Phoenix/Naga packs especially have extensive prop lists consistent with HD-2D-quality environmental detail. **Flagged as possible HD-2D-adjacent — requires gandalf visual inspection of sample images.** These are the strongest dimensional-fit candidates (48×48 = exact 1m/tile at project scale).

**License:** "Yes! You can use these tilesets in your game, even if you intend to sell it...and even if the games contain mature themes." Explicit commercial rights included. No NFT.

**Kokoro Reflections verdict: HIGH PRIORITY CANDIDATE. 48×48 tiles are dimensionally perfect. Extensive prop coverage. Commercial license clean. Thematic range (death/fire/ice/serpent/wizard) maps well to season anchors. Register requires gandalf visual inspection — may be HD-2D-adjacent. Cost: $9–$16/pack, highly reasonable.**

#### PIXELHUNT (pixelhunt.itch.io) — MAP category

- **135 Dungeon Topdown Backgrounds** — $4.99 — 135 individual top-down dungeon background images at 1920×1080 px each. PNG format. 116 MB zip. Themes: different colors, locations, lighting, angles, stylizations. Recommended for "Visual Novels, Character Backgrounds, Themed Backgrounds, RPG Games, Adventure Games." Tags include "Top-Down" and "Isometric."

**Room dimension fit assessment:** Each background is 1920×1080 px. Target rooms are square (720×720 / 1440×1440 / 2160×2160). The 1920×1080 aspect ratio is widescreen, not square. For a 1440×1440 room: the 1080 height is close but would need 360 px of additional height OR the image would need to be cropped/padded to square. For a 720×720 small room: the 1920×1080 is ~2.67× oversized in width — significant crop required. **The aspect ratio mismatch with the project's square room dimensions is a structural issue.**

**License clarification needed:** The page does not explicitly state commercial use terms. "Use with any engines you like" implies broad compatibility but falls short of explicit commercial authorization.

**Style register:** Pixel art described as "high quality" at 1920×1080 — likely higher fidelity than 32×32 tile packs but aspect-ratio incompatible with square room dimensions.

**PIXELHUNT verdict: FLAGGED FOR ASPECT RATIO MISMATCH AND LICENSE UNCERTAINTY. Surface as follow-on acquisition candidate if aspect ratio mismatch can be confirmed as manageable by drax (crop + extend, or use as parallax layer). License must be clarified before acquisition. If confirmed commercial-OK and usable at 1080 height in a 1440 tall room, this becomes a strong MAP-category candidate.**

#### Val Sama 66 (valsama66.itch.io)

- **Spring Ruins Interior** — Name-your-price (free option) — 48×48 tiles, top-down, underground temple with spring-inspired aesthetics. Floor tiles: 13 ground textures + 5 special = 18 floor variants. Wall tiles: 2 wall textures. Props: 30+ decorative tiles. Animated: chests, doors, chalices, levers. 497 kB zip. Published 10 days ago (May 2026). Commercial use permitted; credit appreciated not required; redistribution of raw assets prohibited.

**Style register:** Described as "Retro hand-drawn pixel art" — borderline position. The 48×48 tile dimension and "hand-drawn" descriptor suggest higher fidelity than baseline retro. Spring/overgrown temple theme.

**Room dimension fit:** 18 floor variants at 48×48 far exceeds the EXACT_FIT_DEFAULT threshold (≥8). 2 wall textures falls below the ≥6 threshold for default room — UNDER_VARIETY on walls.

**Val Sama 66 verdict: PARTIAL CANDIDATE. Floor variety is excellent (18 variants). Wall variety insufficient for default-room credible fill (2 variants). Spring/ruin theme is distinctive and seasonal-anchor-mappable (spring rebirth / overgrown ruin). Free option makes acquisition cost-zero. Register needs gandalf visual inspection.**

#### Miguelsgp

- **Pixelart Tileset Dungeon 64×64 — 4 versions** — €1 — 64×64 tiles, top-down, 23 tiles per set in 4 color/lighting variants (Oriental/Sand Castle / Dark Dungeon variants). Commercial use permitted. PNG format, 123 kB. 4.8/5 stars.

**Room dimension fit:** 64×64 tiles, 23 tiles per set. If 23 tiles = ~5 floor + ~5 wall + corners/transitions (rough estimate), this may be UNDER_VARIETY for default room fill. However, 4 color variants provide thematic flexibility.

**Style register:** Retro pixel at 64×64 — larger tiles but still retro aesthetic.

**Miguelsgp verdict: LOW COST SECONDARY CANDIDATE. Good for testing 64×64 scale compatibility with drax's renderer. €1 cost makes it risk-free acquisition.**

#### SakPix (sakpix.itch.io) — AI-Assisted flag

SakPix has multiple dark fantasy dungeon tilesets (Dungeon Asset Pack, Crimson Gothic Castle, Volcanic Inferno Dungeon) at $4 each (60% off) with 32×32 tiles. HOWEVER: SakPix carries an **"AI Assisted" disclosure tag** under Graphics. Per project practice on register and attribution integrity, this is a material flag. Eliminated from primary candidacy.

**SakPix verdict: ELIMINATED — AI-Assisted disclosure conflicts with project's "No generative AI" preference across all catalogue sourcing to date.**

---

## Section 3 — Top 5–10 Candidate Packs (Cross-Vendor)

Summary table. Rows annotated per Amendment 4. All packs are top-down perspective. Tile variant counts are hand-curated estimates based on pack documentation and file sizes; gandalf should verify via visual inspection and/or pack download.

---

### CANDIDATE 1 — Kokoro Reflections: KR Legendary Palaces ~ Reaper Tileset

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Legendary Palaces ~ Reaper Tileset |
| URL | https://kokororeflections.itch.io/kr-legendary-palaces-reaper-tileset-for-rpgs |
| Price | $9.99 |
| License | Commercial use included. No NFT. No AI stated. |
| Sourcing category | TILESET |
| Sourcing category rationale | Small repeating tiles (48×48 and 32×32) with companion props/overlays |
| Room dimension fit | MULTI_BAND (estimated: floor/wall variants likely sufficient for small and default; large may need repeat)|
| Tile variant counts | Floor: estimated 8–12 variants (foggy gray, purple water, fancy tiles, spike traps, fog ground variants); Wall: estimated 4–6 variants (fog-wrapped wall types). **Requires download to confirm exact counts.** |
| Native asset dimensions | N/A (TILESET) |
| Tile dimensions | 48×48 px (32×32 version also included) |
| File format | ZIP, PNG, RPG Maker + universal sheets |
| Coverage | floor, wall, stairs, props (pillars/arches/throne/windows/statues/chests/lanterns/gravestones/chains), animated (torches in 3 colors, animated chest), fog overlays, parallax background |
| Primary fit seasons | death / undead palace / necromancer lair / dark cathedral / underworld domain / shadow realm — maps to seasons with death/shadow/underworld anchors |
| Style register | hand-drawn pixel art; requires gandalf visual inspection for HD-2D register confirmation |
| Sample images | https://img.itch.zone/ (multiple previews accessible from product page https://kokororeflections.itch.io/kr-legendary-palaces-reaper-tileset-for-rpgs) |
| AI disclosure | None stated |

**Why this pack:** 48×48 tiles are the exact 1m/tile match for the project's 48 px/m scale. Death/undead theme is strongly season-anchor-mappable. Rich prop coverage (throne, statues, chains, gravestones). Animated torch variants in multiple colors. Fog overlays provide atmosphere layering. Explicit commercial license. Part of a coherent series — purchasing Phoenix + Naga + Reaper gives three visually distinct season environments from one creator.

---

### CANDIDATE 2 — Kokoro Reflections: KR Legendary Palaces ~ Phoenix Tileset

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Legendary Palaces ~ Phoenix Tileset |
| URL | https://kokororeflections.itch.io/kr-legendary-palaces-phoenix-tileset-for-rpgs |
| Price | $9.99 |
| License | Commercial use included. No NFT. No AI stated. |
| Sourcing category | TILESET |
| Room dimension fit | MULTI_BAND (estimated: sufficient floor/wall variants for small+default) |
| Tile variant counts | Floor: ~10+ variants (lava, dark ground, fiery orange, purple contrast, glittery fire, spike traps, fiery weeds); Wall: ~3–4 types (dark, light, stone/brick variants). **Requires download.** |
| Tile dimensions | 48×48 px (32×32 included) |
| File format | ZIP, PNG, RPG Maker + universal |
| Coverage | floor, wall, stairs, props (pillars/arches/throne/fire-windows/treasure box/push blocks/bridge rails/statues/magic rings/lanterns), animated (chest, fire torches) |
| Primary fit seasons | fire / volcanic peak / phoenix rebirth / flame palace / lava domain — maps to fire-element seasons |
| Style register | hand-drawn pixel art; gandalf visual inspection needed |
| Sample images | Accessible from product page https://kokororeflections.itch.io/kr-legendary-palaces-phoenix-tileset-for-rpgs |
| AI disclosure | None stated |

**Why this pack:** Thematically the strongest fire-element season pack in the catalogue. Same 48×48 dimensional fit as Reaper. Good prop list including fire-windows and magic rings. Series coherence — if Reaper is acquired for a death-season, Phoenix for a fire-season, Naga for a water/serpent season, the project has three visually distinct environments for ~$30 total.

---

### CANDIDATE 3 — Elthen: 2D Pixel Art Cultist Dungeons Tileset

| Field | Value |
|---|---|
| Vendor | Elthen's Pixel Art Shop |
| Pack name | 2D Pixel Art Cultist Dungeons Tileset |
| URL | https://elthen.itch.io/2d-pixel-art-cultist-dungeons-tileset |
| Price | $10 |
| License | Commercial use permitted, no blockchain/AI. Attribution unclear (Patreon-linked; appears optional per community post). |
| Sourcing category | TILESET |
| Room dimension fit | UNDER_VARIETY to EXACT_FIT_SMALL (estimated: moderate floor/wall variants at 32×32; 10 files total including animated elements). **Requires download for exact tile variant count.** |
| Tile variant counts | Unknown from documentation. Pack contains 10 files (17–100 kB each). Animated elements: rotating pillars (8 symbols), stone gates, 3 portal variants, spike traps, spear traps. Suggests moderate base tile count + rich animated prop set. |
| Tile dimensions | 32×32 px |
| File format | PNG sprite sheets |
| Coverage | floor, wall, props (braziers, statues for orbs/swords), animated objects (occult rotating pillars, gates, portals, traps), light sources |
| Primary fit seasons | occult ritual / dark magic lair / forbidden temple / void ceremony / cultist shrine — maps to dark/void/corruption seasons |
| Style register | retro-to-borderline pixel art; strongly thematic; gandalf visual inspection needed |
| Sample images | Accessible from https://elthen.itch.io/2d-pixel-art-cultist-dungeons-tileset (img.itch.zone previews) |
| AI disclosure | "No generative AI was used" |

**Why this pack:** The occult thematic is highly distinctive and maps well to Reincarnated's ceremonial/dark-magic season concepts. The rotating puzzle pillars with 8 occult symbols and 3 portal variants are unusual prop assets that add visual interest. Price is reasonable at $10. The 10-file pack structure suggests meaningful content depth.

---

### CANDIDATE 4 — Elthen: 2D Pixel Art Arcane Dungeons Tileset

| Field | Value |
|---|---|
| Vendor | Elthen's Pixel Art Shop |
| Pack name | 2D Pixel Art Arcane Dungeons Tileset |
| URL | https://elthen.itch.io/2d-pixel-art-arcane-dungeons-tileset |
| Price | $10 |
| License | Commercial use permitted, no blockchain/AI. Attribution: Patreon-linked, appears optional. |
| Sourcing category | TILESET |
| Room dimension fit | UNDER_VARIETY to EXACT_FIT_SMALL (estimated; pack is 125 kB including animated elements) |
| Tile variant counts | Not stated; pack contains main tileset + animated energy pipes, magical barriers, torches, crystals, levers. File size (125 kB) suggests moderate base tile set. |
| Tile dimensions | 32×32 px |
| File format | ZIP (125 kB) |
| Coverage | floor, wall, props, animated (energy pipes, magical barriers, torches, crystals), puzzle mechanics (levers) |
| Primary fit seasons | arcane tower / mage sanctum / magical laboratory / ley-line nexus / enchanted ruins — maps to magic/arcane seasons |
| Style register | retro-to-borderline pixel art; gandalf inspection needed |
| Sample images | img.itch.zone previews accessible from product page |
| AI disclosure | "No generative AI was used" |

**Why this pack:** Strong arcane/magical theming distinct from the cultist pack. Animated energy pipes and magical barriers are unusual environmental elements. Complements the Cultist pack as a "lighter magic" vs "dark cult" distinction. Same $10 price point.

---

### CANDIDATE 5 — Kokoro Reflections: KR Legendary Palaces ~ Naga Tileset

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Legendary Palaces ~ Naga Tileset |
| URL | https://kokororeflections.itch.io/kr-legendary-palaces-naga-tileset-for-rpgs |
| Price | $8.99 |
| License | Commercial use included. No NFT. No AI stated. |
| Sourcing category | TILESET |
| Room dimension fit | MULTI_BAND (estimated: richest coverage in the series at 13 MB; floor types include water + multiple marble variants + scale floors) |
| Tile variant counts | Floor: estimated 10–15 variants (water, marble black/teal/purple/gold, scale floors, scale gold-edged, decorative edges, spikes, pits, gold edging); Wall: estimated 4–6 matching types. **Requires download.** |
| Tile dimensions | 48×48 px (32×32 included) |
| File format | ZIP (13 MB), PNG, RPG Maker + universal |
| Coverage | floor, wall, stairs (diagonal), props (pillars/arches/throne/windows/treasure chest animated/push blocks/bridge rails/statues/magic rings/ladders ×3/snake wall decor/jewels), animated (chest) |
| Primary fit seasons | serpentine domain / water palace / jade sanctum / naga lair / underground river palace — maps to water/earth/jade seasons |
| Style register | hand-drawn pixel art; gandalf visual inspection needed |
| Sample images | Accessible from product page https://kokororeflections.itch.io/kr-legendary-palaces-naga-tileset-for-rpgs |
| AI disclosure | None stated |

**Why this pack:** Largest file in the Kokoro series (13 MB) suggesting greatest content depth. Rich floor variety (water + multiple marble types + scale floors). The water/serpentine theme distinguishes it from fire (Phoenix) and death (Reaper). Three Kokoro packs together = fire + death + water/serpent themes for ~$30.

---

### CANDIDATE 6 — Elthen: 2D Pixel Art Lava Dungeons Tileset

| Field | Value |
|---|---|
| Vendor | Elthen's Pixel Art Shop |
| Pack name | 2D Pixel Art Lava Dungeons Tileset |
| URL | https://elthen.itch.io/2d-pixel-art-lava-dungeons-tileset |
| Price | $10 |
| License | Commercial use permitted, no blockchain/AI. Attribution: Patreon-linked. |
| Sourcing category | TILESET |
| Room dimension fit | UNDER_VARIETY (pack contains animated elements; floor variant count unknown from documentation) |
| Tile variant counts | Not stated. Animated: lava bubbles, lines, streams. File: PNG + JSON animation data. |
| Tile dimensions | 32×32 px |
| Coverage | floor, wall, props (braziers, light sources), animated lava (bubbles/lines/streams) |
| Primary fit seasons | volcanic eruption / lava flow / fire dungeon / molten earth — maps to fire/earth/volcanic seasons |
| Style register | retro-to-borderline pixel art |
| AI disclosure | "No generative AI was used" |

---

### CANDIDATE 7 — Foozle Lucifer: Dungeon Tileset (free CC0 baseline)

| Field | Value |
|---|---|
| Vendor | Foozle (foozlecc.itch.io) |
| Pack name | Lucifer — Dungeon Tileset |
| URL | https://foozlecc.itch.io/lucifer-dungeon-tileset |
| Price | Free (name-your-own) |
| License | CC0 1.0 — no restrictions, commercial use, no attribution required |
| Sourcing category | TILESET |
| Room dimension fit | UNDER_VARIETY (estimated; 149 kB zip at 32×32 suggests limited tile set for default room) |
| Tile variant counts | Unknown; small file size suggests ~10–20 tiles total. Aseprite source files included. |
| Tile dimensions | 32×32 px |
| File format | ZIP (149 kB), PNG + .ase Aseprite source |
| Coverage | floor, wall, dungeon environmental elements |
| Primary fit seasons | stone dungeon / dark basement / crypt / generic dungeon — maps to death/shadow/dungeon seasons |
| Style register | retro pixel art (Diablo-era dungeon aesthetic) |
| AI disclosure | "No generative AI was used" |

**Why this pack:** CC0 license makes acquisition cost-zero and attribution-free. Genre alignment is strong (Diablo-era dungeon aesthetic). Aseprite source files enable custom modification. Best use: immediate acquisition as placeholder-upgrade while HD-2D-register packs are evaluated. Could also serve as VS2b expansion for a "generic dungeon" room type distinct from season-themed rooms.

---

### CANDIDATE 8 — Val Sama 66: Spring Ruins Interior (partial — wall variety gap)

| Field | Value |
|---|---|
| Vendor | Val Sama 66 (valsama66.itch.io) |
| Pack name | Spring Ruins Interior - Asset Pack |
| URL | https://valsama66.itch.io/spring-ruins-interior-asset-pack |
| Price | Name-your-own (free option) |
| License | Commercial use permitted; credit appreciated not required; no redistribution of raw assets. |
| Sourcing category | TILESET |
| Room dimension fit | UNDER_VARIETY (18 floor variants far exceeds thresholds; 2 wall variants far below ≥6 threshold) |
| Tile variant counts | Floor: 13 ground textures + 5 special = 18 variants (confirmed). Wall: 2 variants (confirmed). Props: 30+ decorative tiles. |
| Tile dimensions | 48×48 px |
| File format | ZIP (497 kB) |
| Coverage | floor ×18, wall ×2, props ×30+, animated (chests, doors, chalices, levers) |
| Primary fit seasons | spring ruin / overgrown temple / nature-reclaimed shrine / verdant ruins / goddess temple — maps to spring/life/nature seasons |
| Style register | retro hand-drawn pixel art (48×48; recent release May 2026) |
| AI disclosure | Not stated |

**Why this pack despite wall gap:** Floor variety (18 variants) is exceptional and exceeds all thresholds. The overgrown temple / spring-goddess theme is highly distinctive and maps to seasonal anchors not covered by other candidates. Free option. 48×48 tile dimension. Wall gap means room fill requires pairing with a complementary wall source OR accepting 2-variant wall repetition for VS2a (small room = 15 wall tiles, 2 variants may be acceptable for VS2a ship gate). Flag for drax: can repeated 2-variant wall be visually acceptable in a 720×720 or 1440×1440 room?

---

### CANDIDATE 9 — Elthen: 2D Pixel Art Dungeon Tileset (free baseline)

| Field | Value |
|---|---|
| Vendor | Elthen's Pixel Art Shop |
| Pack name | 2D Pixel Art Dungeon Tileset |
| URL | https://elthen.itch.io/2d-pixel-art-dungeon-tileset |
| Price | Name-your-own (free option) |
| License | Commercial use confirmed ("commercial/non-commercial projects"); attribution required per Patreon terms |
| Sourcing category | TILESET |
| Room dimension fit | UNDER_VARIETY (47 kB zip; small file implies limited tile set) |
| Tile variant counts | Unknown. Community rates it as "vibrant color palette" and "aesthetic cohesion." |
| Tile dimensions | 32×32 px |
| File format | PNG (Dungeon_Tileset.png, 47 kB) |
| Coverage | floor, wall, dungeon environmental (details unknown without download) |
| Primary fit seasons | stone dungeon / crypt / classic fantasy dungeon — generic dungeon anchor |
| Style register | retro pixel art |
| AI disclosure | "No generative AI was used" |

---

### CANDIDATE 10 — PIXELHUNT: 135 Dungeon Topdown Backgrounds (conditional)

| Field | Value |
|---|---|
| Vendor | PIXELHUNT (pixelhunt.itch.io) |
| Pack name | 135 Dungeon Topdown Backgrounds |
| URL | https://pixelhunt.itch.io/135-dungeon-topdown-backgrounds |
| Price | $4.99 |
| License | UNCLEAR — "use with any engines you like" stated; explicit commercial authorization not confirmed. Requires license clarification before acquisition. |
| Sourcing category | BACKGROUND_PIECE |
| Room dimension fit | ASPECT_RATIO_MISMATCH — 1920×1080 px (widescreen) vs target square rooms (720×720 / 1440×1440 / 2160×2160). 1080 height is usable as floor of a 1440×1440 room with padding/extension. **drax assessment needed.** |
| Native asset dimensions | 1920×1080 px per background |
| Tile variant counts | N/A (MAP/BACKGROUND_PIECE) |
| File format | PNG (116 MB zip) |
| Coverage | 135 unique top-down dungeon room scenes; different themes/colors/lighting/angles |
| Primary fit seasons | varied — 135 backgrounds likely cover multiple dungeon themes |
| Style register | pixel art at 1920×1080 — likely higher fidelity than 32×32 tile packs; visual inspection needed |
| AI disclosure | Not stated |

**Conditional candidacy:** If commercial license is confirmed and drax can accommodate 1920×1080 widescreen backgrounds into square room rendering (crop, or use as floor panel leaving walls separate), this pack at $4.99 for 135 scenes is extraordinary value. Flag for follow-on investigation.

---

## Section 4 — Findings-Blockers

### Blocker 1 — Register gap: HD-2D-quality top-down interior tilesets are scarce

The core finding: the top-down dungeon interior tileset landscape does not have a widely available pack that clearly meets the HD-2D-shaped pixel-art register as cleanly as chierit Elementals meet the character register. The retro pixel-art register dominates at 16×16 and 32×32. The Kokoro Reflections packs at 48×48 are the strongest candidates for HD-2D adjacency, but visual inspection by gandalf is required to confirm register fit.

**Recommended resolution:** Gandalf visual inspection of sample images for Candidates 1–5 before VS2a selection. If none clear the HD-2D bar, the project has two paths:
- Path A: Accept best-available higher-fidelity retro pixel (Kokoro Reflections) as VS2a ship — "above-geometric-placeholders" bar is met even if not full HD-2D register match
- Path B: Commission/generate environment art in HD-2D register via LLM (star-lord) — higher cost, out of scope for VS2a tight timeline

### Blocker 2 — Elthen tile variant counts unconfirmed

Elthen's pack documentation does not itemize floor/wall tile variant counts. Room-dimension-fit annotations for Elthen packs are estimates only. **Download + manual count required before gandalf can make a VS2a selection from Elthen packs.** The small file sizes (47–125 kB) suggest limited tile sets that may fall below the EXACT_FIT_DEFAULT threshold.

**Recommended resolution:** Acquire the free Elthen Dungeon Tileset ($0) and 1–2 paid packs at $10 each for count verification during Track B. Total cost ≤$30 for verification pass.

### Blocker 3 — Kokoro Reflections tile variant counts unconfirmed

Same issue as Elthen but with larger file sizes (7–13 MB) suggesting more content. The documentation itemizes prop types extensively but does not give precise floor/wall tile variant counts.

**Recommended resolution:** Same as Blocker 2 — small paid acquisition ($9–$10) for Track B verification. Kokoro Reaper/Phoenix are the highest-priority downloads given 48×48 dimensional fit.

### Blocker 4 — PIXELHUNT license ambiguous

The 135-background pack has no explicit commercial license statement. "Use with any engines" is insufficient for project's commercial standards.

**Recommended resolution:** Contact PIXELHUNT via itch.io message to confirm commercial terms before acquisition. If confirmed, this is a VS2b-expansion candidate given its breadth (135 backgrounds × varying themes).

### Blocker 5 — CraftPix subscription gating on best pixel-art packs

The CraftPix Medieval Interior (available at 48×48) and Cave Tileset are premium-membership-gated. Individual pricing is not easily accessible. Subscription model is non-standard.

**Recommended resolution:** If Kokoro Reflections packs satisfy register + variant-count requirements, CraftPix acquisition is not needed for VS2a. Defer to VS2b+ if Tier-1 proves insufficient.

---

## Section 5 — Hand-off for Gandalf Track B Framework

### Top candidate shortlist for VS2a `primary_fit_seasons` annotation (in priority order)

1. **Kokoro Reaper** → death / underworld / shadow / necromancer palace seasons
2. **Kokoro Phoenix** → fire / volcanic / rebirth / phoenix ascension seasons
3. **Elthen Cultist Dungeons** → dark occult / void ceremony / forbidden temple seasons
4. **Elthen Arcane Dungeons** → arcane / mage sanctum / ley-line nexus seasons
5. **Kokoro Naga** → water / serpentine / jade palace / underground river seasons
6. **Val Sama 66 Spring Ruins** → spring / nature reclamation / goddess temple / verdant ruin seasons
7. **Kokoro Wizard's Hideout** → wizard / hermit / scholar / mystic cavern seasons
8. **Foozle Lucifer Dungeon (free)** → generic dark dungeon / baseline dungeon placeholder seasons

### Coverage-completeness summary

| Pack | Floor | Wall | Props | Overlays | Animated | Notes |
|---|---|---|---|---|---|---|
| Kokoro Reaper | ✓ | ✓ | ✓ rich | ✓ fog | ✓ chest + torches | Most complete coverage |
| Kokoro Phoenix | ✓ | ✓ | ✓ rich | - | ✓ chest + torches | Strong floor/prop |
| Kokoro Naga | ✓ rich | ✓ | ✓ rich | - | ✓ chest | Richest content (13 MB) |
| Elthen Cultist | ? | ? | ✓ (orbs, portals) | - | ✓ pillars, gates | Animated props are standout |
| Elthen Arcane | ? | ? | ✓ | - | ✓ energy pipes, crystals | Animated features standout |
| Val Sama 66 Spring | ✓ ×18 | ✓ ×2 only | ✓ ×30+ | - | ✓ chests, doors | Floor-strong, wall-weak |
| Foozle Lucifer | ? | ? | ? | - | - | Small pack, retro |

Floor/wall counts marked ? require download verification.

### Per-substrate room-band coverage assessment

**Small room (720×720) — 15×15 tiles at 48px:**
- Kokoro Reaper / Phoenix / Naga: estimated EXACT_FIT_SMALL or better
- Val Sama 66 Spring: EXACT_FIT_DEFAULT on floors; may reach EXACT_FIT_SMALL on walls (2 variants may be tolerable at small room scale)
- Foozle Lucifer: likely UNDER_VARIETY but free CC0

**Default room (1440×1440) — 30×30 tiles at 48px:**
- Kokoro Naga: potentially EXACT_FIT_DEFAULT or MULTI_BAND (richest content)
- Kokoro Reaper/Phoenix: potentially EXACT_FIT_DEFAULT (variant counts need verification)
- Val Sama 66 Spring: UNDER_VARIETY on walls; floor exceeds threshold

**Large room (2160×2160) — 45×45 tiles at 48px:**
- All candidates likely UNDER_VARIETY for large room fill; large room is out of VS2a scope anyway (VS2a ships default + small rooms per dispatch scope)

### Cross-reference to prior catalogue work

- **VFX vendors (Pimen, CreativeKind):** No environment assets found in either. No cross-reference needed.
- **Elthen:** New discovery for environment work; not in prior character/monster catalogues.
- **Foozle:** Not in prior catalogues; Lucifer Collection has an entire ecosystem (characters + environment + UI) that may be worth cataloguing more broadly in VS2b.
- **Kokoro Reflections:** New discovery; no prior catalogue entry. High priority for Elrond schema addition.

### Tier-2 vendor sweep — follow-on commission recommendations

Tier-2 vendors already partially crawled (CodeManu, FrostWindz, BraCKEYs, Pixogen) were NOT re-evaluated in this dispatch (per time-cap and scope constraint). Recommended follow-on vendors for environment packs specifically:

1. **Seliel the Shaper** — Has 25+ tileset packs at 16×16 retro; primarily out of scope for VS2a register but worth a systematic catalogue pass for VS2b open-world/exterior environments
2. **Kenney.nl** — Free CC0 assets in bulk; known to have top-down dungeon tiles; unverified for HD-2D register
3. **Szadi Art** — itch.io vendor with RPG tileset packs; not evaluated in this dispatch
4. **Raou** — TDRPG Interior pack (16×16, 400+ tiles, 5 wall types, commercial-OK at $18) — worth evaluating if Tier-1 variant counts prove insufficient
5. **Phantom Cooper** — 24×24 Dungeon Interiors and Exteriors at $4.25 — mid-range tile size worth visual inspection

---

## Source List

All URLs accessed 2026-05-17.

- Pimen catalogue: https://pimen.itch.io/
- Elthen catalogue: https://elthen.itch.io/
- Ansimuz catalogue: https://ansimuz.itch.io/
- Foozle catalogue: https://foozlecc.itch.io/
- Pipoya catalogue: https://pipoya.itch.io/
- CreativeKind catalogue: https://creativekind.itch.io/
- CraftPix pixel tilesets: https://craftpix.net/categorys/pixel-art-tilesets/
- CraftPix top-down dungeon: https://craftpix.net/product/top-down-dungeon-pixel-tileset-for-rpg-and-roguelike-game/
- CraftPix free dungeon pack: https://craftpix.net/freebies/free-2d-top-down-pixel-dungeon-asset-pack/
- CraftPix Medieval Interior: https://craftpix.net/product/medieval-interior-top-down-pixel-art-tileset/
- Foozle Lucifer Dungeon: https://foozlecc.itch.io/lucifer-dungeon-tileset
- Foozle Lucifer Lava Dungeon: https://foozlecc.itch.io/lucifer-lava-dungeon-tileset
- Seliel the Shaper catalogue: https://seliel-the-shaper.itch.io/
- Seliel Eternal Dungeon: https://seliel-the-shaper.itch.io/eternal-dungeon
- Seliel Castle Dungeon: https://seliel-the-shaper.itch.io/castle-dungeon
- Seliel Fortified Keep: https://seliel-the-shaper.itch.io/fortified-keep
- Seliel Muddy Cave: https://seliel-the-shaper.itch.io/muddy-cave
- Kokoro Reaper: https://kokororeflections.itch.io/kr-legendary-palaces-reaper-tileset-for-rpgs
- Kokoro Phoenix: https://kokororeflections.itch.io/kr-legendary-palaces-phoenix-tileset-for-rpgs
- Kokoro Naga: https://kokororeflections.itch.io/kr-legendary-palaces-naga-tileset-for-rpgs
- Kokoro Wizard's Hideout: https://kokororeflections.itch.io/kr-wizards-hideout-for-rpgs
- Kokoro Snow Castle: https://kokororeflections.itch.io/kr-snow-castle-tileset-for-rpgs
- PIXELHUNT 135 Backgrounds: https://pixelhunt.itch.io/135-dungeon-topdown-backgrounds
- Val Sama 66 Spring Ruins: https://valsama66.itch.io/spring-ruins-interior-asset-pack
- Miguelsgp 64x64 Dungeon: https://miguelsgp.itch.io/free-tileset-dungeon
- Anokolisa Dungeon Crawler: https://anokolisa.itch.io/dungeon-crawler-pixel-art-asset-pack
- Raou TDRPG Dungeon: https://raou.itch.io/dungeon-tileset-top-down-rpg
- Raou TDRPG Interior: https://raou.itch.io/top-down-interior-tileset
- Sscary The Dungeon: https://sscary.itch.io/the-dungeon
- SakPix Dungeon (eliminated): https://sakpix.itch.io/dungeon-asset-pack-32x32-pixel-art
- Goblin Portal Dungeon: https://goblinportal.itch.io/top-down-fantasy-dungeon-game-kit
- Itch.io tag pages consulted: dungeon+top-down, dungeon+tileset, dark-fantasy+top-down, backgrounds+dungeon, 64x64+tileset

---

*Filed by legolas, 2026-05-17. All data is read-only from public sources. No assets acquired.*
