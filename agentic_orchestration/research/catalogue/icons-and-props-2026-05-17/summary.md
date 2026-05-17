# Icon + Prop Catalogue Crawl — Summary — 2026-05-17

**Mode:** B (systematic catalogue crawl)
**Commissioner:** knight-rider (Matt L3, 2026-05-17 ~21:30 EDT)
**Sizing reference:** `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (gandalf v1.7)
**Output schema reference:** `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md` (elrond)
**Crawl date:** 2026-05-17

---

## 1. Vendors Crawled

| Vendor | URL | Notes |
|---|---|---|
| CraftPix | https://craftpix.net | Primary premium/free vendor. Rich icon + props catalogue. Most findings here. |
| Pimen | https://pimen.itch.io | CONFIRMED: Zero icon/prop/loot content — VFX-only. Existing 2026-05-16 crawl definitive. |
| Seliel the Shaper | https://seliel-the-shaper.itch.io | Mana Seed. High-quality 16x16 SNES-style. Treasure chests (free), breakable pots (free), alchemy gear (potions). |
| Franuka | https://franuka.itch.io | RPG Icon Pack 500+ at 16x16/32x32/48x48. Strong multi-type coverage. |
| Akari21 | https://akari21.itch.io | RPG Icon Pack 200+ native 16x16+32x32. Star-rarity system. |
| Vennril | https://vennril.itch.io | 250+ item sprites at 16x16/32x32/48x48/64x64. Strong weapon + armor coverage. |
| DerNachbar (Dire Dungeon Items) | https://dernachbar.itch.io | Best single comprehensive pack: 259 items, CC BY 4.0. |
| Shikashipx | https://shikashipx.itch.io | 284 icons, CC BY 4.0. Free with attribution. |
| GandalfHardcore | https://gandalfhardcore.itch.io | 20+ pixel art chests 32x32 (side-scroller focus; not top-down primary). |
| Pixel Serial | https://pixelserial.itch.io | Free RPG top-down chests, 9 types, 18x16 animated. |
| PixelExplosive | https://pixelexplosive.itch.io | 12 chest opening animations, 32x32 grid. |
| Mucho Pixels | https://muchopixels.itch.io | Dungeon Tileset Pack — best combined chest+coffin+weapon-stand+pots in one pack. |
| Elthen | https://elthen.itch.io | Destructible objects (crate/barrel/pot/chest) with damage+destroy animation. Free. |
| Indie-Vova | https://indie-vova.itch.io | Dungeons & Pixels RPG 32x32 — chests, barrels, crates, shields. |
| Anokolisa | https://anokolisa.itch.io | Free dungeon crawler pack 500+ sprites, 16x16. |
| BigWander | https://bigwander.itch.io | Weapon rack 128 sprites (free); armor rack chest pieces. |
| Pixel-1992 | https://pixel-1992.itch.io | Gold piles + coin piles + chests. AI-assisted flag. |
| AquaSenshi | https://aquasenshi.itch.io | Free 25-icon potion pack — health/mana/poison/energy/speed confirmed. |
| SODA | https://soda-1.itch.io | 150+ stylized potion icons 32x32. Health+mana confirmed. |
| Bis | https://bis1994.itch.io | 270 potion icons 32x32, 18 designs x 12 colors, empty variants. |
| OpenGameArt | https://opengameart.org | CC0 + OGA-BY sources; gold icons, potion pack, dungeon objects. |
| Kenney | https://kenney.nl | CC0. Roguelike/RPG 1700 assets, Caves+Dungeons 520, Tiny Dungeon 130. 16x16. |

**Not re-crawled (VFX-only confirmed):** Pixogen, Frostwindz, CodeManu, CreativeKind, Fellor, Pipoya — all 2026-05-16 full crawls show zero icon/prop/loot content.
**Partial/error:** GameDev Market — 403 errors on product pages. Pixel Dungeon Set + RPG Pixel Icons Pack surfaced from search but not fetchable.

---

## 2. Coverage Matrix

| Subcategory | Status | Best Sources |
|---|---|---|
| Potion icons — health/mana | WELL COVERED | AquaSenshi (free, health+mana confirmed), SODA (150+, health+mana confirmed), CraftPix 100-potion pack |
| Potion icons — fill levels | PARTIAL | Bis (empty variants = proxy), SODA (small/medium/large sizes = proxy). No dedicated 3/3-2/3-1/3 fill states found anywhere. |
| Gold piles — floor drop | COVERED | Pixel-1992 (17 models x 3 sizes, AI-assisted), OGA CC0 16x16 (10 icons), Dire Dungeon Items (45 coin variants) |
| Gold piles — stack-size variation | WELL COVERED | OGA Clint Bellanger (bit-stack 1/2/4/8/16), Pixel-1992 small/medium/large, Dire Dungeon 45 variants |
| Gear weapons — floor drop | WELL COVERED | Dire Dungeon Items (54 melee + 19 ranged, CC BY), Vennril 250+ (dagger/sword/axe/wand/bow/spear/hammer), CraftPix 100 Weapon Icons |
| Gear armor — floor drop | WELL COVERED | Dire Dungeon Items (36 pieces + 12 amulets + 12 rings), CraftPix 100 Armor Icons, Vennril 250+ |
| Gear rarity tiers | SPARSE | No pack with pre-built ARPG white/magic/rare/unique colored borders. Closest: Dire Dungeon 10 colored outline variants. Rarity-border overlay would need custom authoring. |
| Chests — small/medium/large | COVERED | Seliel (free, 5 types, top-down), Pixel Serial (free, 9 types), Mucho Pixels (gold+silver, locked/unlocked/opened) |
| Chests — open+closed states | COVERED | Seliel (open+closed confirmed), Mucho Pixels (locked/unlocked/opened), Pixel Serial (4-frame animated) |
| Chests — animated | COVERED | Pixel Serial (4-frame), PixelExplosive (12 opening-animation designs), GandalfHardcore (7+6 frame, side-scroller) |
| Coffin — open+closed | PARTIAL | Mucho Pixels (stone coffin with open state — best find). CraftPix topdown tileset (coffin present, open state not confirmed). SPARSE overall. |
| Weapon stand | COVERED | Mucho Pixels (resizable stand + 7 weapons + broken variant), CraftPix free dungeon objects (weapon racks), CraftPix guild hall (weapon rack + mannequin) |
| Armor stand | PARTIAL | CraftPix guild hall (mannequin confirmed). Standalone armor stand with helmless/full variants not confirmed anywhere. Coverage is implied from context. |
| Urns/vases/barrels — intact | WELL COVERED | CraftPix free dungeon objects, Mucho Pixels (4 pot types + 2 barrel types), Elthen (pot/barrel/crate), Seliel breakable pots |
| Urns/vases/barrels — destroyed frames | COVERED | Mucho Pixels (broken states for pots+barrels, BEST), Elthen (damage+destroy animation), Seliel (3-frame breaking + shard particles) |
| UI gear icons comprehensive | WELL COVERED | Dire Dungeon Items (259 items CC BY), CraftPix 1000+ pack, CraftPix 100 weapon + 100 armor, Akari21 200+ |
| UI potion icons health+mana | COVERED | AquaSenshi (free, confirmed), SODA (confirmed), Dire Dungeon (16 potions), CraftPix packs |
| UI gold icon | COVERED | Dire Dungeon (45 coin variants), CraftPix treasure packs, OGA Clint Bellanger |
| UI rarity frames/borders | NOT FOUND | No vendor supplies pre-built ARPG rarity-tier UI border system in pixel-art. Custom authoring or CraftPix Basic UI pack as frame substrate. |

---

## 3. Sizing-Mismatch Flags

**Targets per gandalf v1.7 canon:**
- Floor loot potions/gold: ~35px mobile
- Floor loot gear drops: ~50px mobile
- Chests: ~110-130px mobile
- Destructibles (vases/urns): ~65-85px mobile
- UI icons: 110-125px mobile

| Pack | Native Size | Issue |
|---|---|---|
| CraftPix Free Game Coins Sprite Sheets | 512x512 | FAR OVERSIZED for floor drop. Heavy downscale required (~14x). Quality risk. |
| Pixel-1992 RPG Loot Pack 1200 | 128x128, 64x64 | OVERSIZED for ~35px floor-loot target. 64x64 = ~1.8x; downscale may be acceptable for ~40px floor target. |
| Pixel Serial chests | 18x16 (closed) | UNDERSIZED for 110-130px chest target. ~6-7x upscale needed. Intended for 16px-grid games. |
| Kenney, Seliel Alchemy Gear, most OGA | 16x16 | UNDERSIZED: 7x upscale for UI icons. 2x acceptable for floor-loot. Pixel-art upscaling acceptable if intentional register. |
| CraftPix Topdown Dungeon Tileset, Mucho Pixels | 16x16 | Tileset grid logic: chest spans ~3-4 tiles = 48-64px effective. Reasonable for prop sizing. |
| Most 32x32 UI icon packs | 32x32 | Below 110-125px UI target. Standard: slot-frame system at 3-4x = 96-128px brackets target. Not a blocking issue. |

**Key note:** No pack delivers assets natively at gandalf's 110-125px UI target. This is standard 2D pixel-art practice. The gap is bridged by drax's frame/slot rendering pipeline. CraftPix Basic UI pack (free) supplies slot frame infrastructure.

---

## 4. License-Status Flags

### CC-0 (no restriction)
- OGA Bonsaiheldin gold 16x16
- Kenney all packs

### CC-BY (attribution required, commercial OK)
- Dire Dungeon Items — CC BY 4.0. Best single pack. Attribution text in credits.
- Shikashi's Fantasy Icons — CC BY 4.0. Credit: Matt Firth (shikashipx) + game-icons.net.
- OGA 48 magic potions — OGA-BY 3.0. Attribution required.

### CC-BY-SA (attribution + share-alike — FLAGGED)
- OGA Clint Bellanger gold 32x32 — CC-BY-SA 3.0. Share-alike clause may conflict with proprietary commercial release. Recommend deferring in favor of Dire Dungeon Items CC BY 4.0 gold coverage.

### CC-BY-ND (attribution, no derivatives — commercial OK)
- Bis Potions 270 — CC BY-ND 4.0. Commercial OK, modification prohibited.

### Commercial license (royalty-free, no attribution)
CraftPix (all packs), Akari21, Vennril, AquaSenshi, SODA, GandalfHardcore, Pixel Serial, Mucho Pixels, Elthen, Seliel (Mana Seed), PixelExplosive, Indie-Vova, BigWander, Franuka (custom license — attribution required; verify current terms).

### AI-Generated Content Flag
- Pixel-1992 packs — "AI Assisted" with manual Aseprite refinement. Flagged for elrond curation per team AI-asset policy.

---

## 5. Cost Rollup

| Pack | Cost | Key Coverage |
|---|---|---|
| Dire Dungeon Items | $10.00 | 259 items comprehensive; CC BY 4.0 |
| SODA 150+ Stylized Potions | $3.25 | 150+ potions, health+mana, size variants |
| Bis Potions 270 | $7.00 | 270 variants, empty included |
| Akari21 RPG Icons 200+ | $3.00 | 200+ icons, star-rarity system |
| Franuka RPG Icon Pack 500+ | $4.99 | 500-600+, 3 sizes |
| Vennril 250+ Items | $4.99 | 250+, 4 size variants |
| PixelExplosive 12 Chest Animations | $2.00 | 12 chest opening animations |
| GandalfHardcore 20+ Chests | $2.59 | 20+ variants, animated (side-scroller) |
| Indie-Vova Dungeons & Pixels 32x32 | $5.99 | Full tileset + chests+barrels+crates |
| Mucho Pixels Dungeon Tileset | $4.95 | Chest+coffin+weapon-stand+pots with states |
| Seliel Alchemy Gear | $12.99 | 416 potion variants, 16x16 |
| Pixel-1992 Coin Piles + Chests | $1.99 | 17 pile models x 3 sizes + chests (AI-assisted) |
| CraftPix premium packs | membership or ~$5.50+ per pack | 1000+ icons, 100-weapon, 100-armor, 100-potion, treasure packs |
| **All free packs** | FREE | CraftPix freebies x7, OGA CC0 + OGA-BY, Seliel chests+pots, AquaSenshi, Elthen, Pixel Serial, Shikashi, BigWander, Anokolisa, Kenney |

**Minimum cost for comprehensive coverage without free-tier gaps:**
Dire Dungeon Items ($10) + SODA potions ($3.25) + Mucho Pixels ($4.95) = **$18.20** covers UI icons + floor loot + chest+coffin+weapon-stand+pots comprehensively. CraftPix free tier fills background gaps at $0.

---

## 6. Vendor Breadth Map (for broader 2D sprite survey)

For `2026-05-17-legolas-broader-2d-sprite-catalogue-genre-survey-queued.md` — avoid duplicate icon/prop work:

- **CraftPix**: icon/prop well-covered here. Broader survey: check character/monster/tileset coverage.
- **Pimen**: VFX-only. No duplicate risk; out of scope for icon/prop.
- **Seliel the Shaper**: icon/prop/object focused. No character/enemy sprites. Broader survey: LOW PRIORITY (scope mismatch).
- **Kenney**: CC0 mega-library. Broader survey SHOULD hit roguelike character packs (`kenney.nl/assets/roguelike-characters`) and roguelike cave tileset — not covered here.
- **Elthen**: destructibles done here. Also has character sheets — broader survey candidate.
- **OpenGameArt**: partial icon crawl only. Broader survey should target OGA character + monster + tileset content.
- **GameDev Market**: 403 errors here. Broader survey should retry.
- **Franuka, Akari21, Vennril, DerNachbar**: icon-focused vendors. Likely no character sprite coverage. Broader survey: LOW PRIORITY.
- **Anokolisa, Indie-Vova**: partial dungeon prop + tileset coverage. Have character sprites too. Broader survey candidates.

---

*Filed 2026-05-17 by legolas. Output: floor-loot.jsonl (29 rows), ambient-props.jsonl (23 rows), ui-icons.jsonl (25 rows), this summary. Downstream: elrond curation dispatch.*
