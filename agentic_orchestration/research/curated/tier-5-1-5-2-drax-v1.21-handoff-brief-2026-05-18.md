# Tier 5.1 / 5.2 — Drax v1.21+ Handoff Brief — Final VS2a Curation Pass

**Author:** elrond
**Date:** 2026-05-18
**Dispatch:** `agentic_orchestration/dispatches/2026-05-18-elrond-tier-5-1-5-2-final-curation.md`
**Authority:** Matt L3 locks 2026-05-18:
- **Tier 5.1:** Game-icons.net (SIL-1.1) / consistent prop scale / medium decoration density / single credits.txt
- **Tier 5.2:** defer mega-pack-02 / rubber-stamp HD-cinematic / approve catalogue-DB additive schema

**Tag:** `elrond/v1.11-tier-5-1-5-2-final-curation-1`
**Target consumer:** drax v1.21+ (queued post-mobile-chain + post-chierit-monster-wiring; lowest priority VS2a polish pass)
**Companion deliverables:**
- `catalogue-db-schema-v2-2026-05-18.md` (additive schema spec — Tier 5.2 § 4)
- `ambient-props-subset-vs2a-2026-05-17.jsonl` (extended with 8-12 new prop rows + scale/density manifest — Tier 5.1 § 2)
- `MIGRATION.md` v1.6 entry (data-layer migration record)

---

## § 0 — TL;DR for drax

Four wire-in surfaces, all queued lowest priority for a VS2a polish pass:

1. **Game-icons.net role mapping** (~28 icons; SIL-1.1 free download) — replaces HUD widget placeholders + adds proper buff/debuff/CC icons + ability slot icons + rarity badge backgrounds.
2. **Consistent prop scale + medium density rules** — global `PROP_RENDER_SCALE_OVERRIDE = 0.75` multiplier applied to existing `STATIC_PROP_DESCS` and `DUNGEON_LOOP_DESCS` renderScale fields; per-room density target 4-6 props minimum / 8-10 max (was 3-4 floor under current `dungeonPropsForRoom`).
3. **8 new ambient props** from craftpix-mega + free-characters atmospheric assets — extend `STATIC_PROP_DESCS` from current 4 to 12 entries (ladder, crate, barrel, column already present; +sack, +vase, +rubble-A, +rubble-B, +bookshelf, +bookpile, +small-table, +iron-bracer — exact source coords below).
4. **credits.txt consolidated text** — verbatim file content provided below; drax deploys to `reincarnated-demo/public/credits.txt` as a complete file replacement per Matt single-file lock.

All four surfaces are zero-spend (Game-icons.net is SIL-1.1 free; all props are on-disk-already; credits.txt is text-only). No engine-side work. ADR-006 compliant.

---

## § 1 — Deliverable 1: Game-icons.net icon role mapping

### § 1.1 — License + acquisition posture

- **License:** SIL Open Font License 1.1 (free for any use including commercial; modification permitted; redistribution permitted with same license).
- **Attribution requirement:** attribute the contributors AND link back to game-icons.net per § 5 of the SIL-1.1.
- **Acquisition:** direct download from game-icons.net per icon (each icon page exposes SVG + PNG; "Download" button gives 512×512 transparent PNG free).
- **Bulk-download tool option:** game-icons.net offers a "Download all icons" zip (~25 MB; ~4,000 icons); single-zip-acquisition is simpler than per-icon click-through for the 28-icon scope here.
- **Style register:** monochrome silhouette icons; render as overlays on per-color slot backgrounds for visual variety. Register-fit: COMPATIBLE for UI surface (not a HYBRID-a3 register break; UI silhouettes are register-agnostic by convention).

### § 1.2 — Recommended on-disk placement

```
reincarnated-demo/public/assets/game-icons/
├── ability/           (14 icons)
├── status/            (10 icons; buff/debuff/CC)
├── inventory/         (4 icons; weapon/armor/accessory/consumable category headers)
└── hud/               (4 icons; health/mana/dash/potion HUD widgets — replacements)
```

Drax v1.21+ ingests each subdirectory and exposes via a new `gameIcons.ts` module (parallel to `direDungeonLoot.ts` for the gear-pipeline asset module pattern).

### § 1.3 — Icon role mapping (28 icons total)

#### § 1.3.1 — Ability/skill icons (14 icons)

Per-element + per-archetype-tag. Used for hotbar slot rendering when skill icons aren't pre-supplied by class loadout.

| Role | game-icons.net path | Filename | Why this icon |
|---|---|---|---|
| `ability_fire_basic` | `delapouite/fire` | fire.svg | Universal fire silhouette; legible at small scale |
| `ability_water_basic` | `delapouite/water-drop` | water-drop.svg | Clean drop silhouette; element-readable |
| `ability_wind_basic` | `lorc/whirlwind` | whirlwind.svg | Spiral motion = wind register |
| `ability_earth_basic` | `lorc/stone-block` | stone-block.svg | Solid block = earth-mass; pairs with thorny-root for variety |
| `ability_lightning_basic` | `lorc/lightning-bolt` | lightning-bolt.svg | Jagged bolt = canonical lightning |
| `ability_shadow_basic` | `lorc/sands-of-time` | sands-of-time.svg | Hourglass = miasma/death-time; register-fit |
| `ability_holy_basic` | `lorc/divine-cross` | divine-cross.svg | Cross with rays = holy; not religion-locked |
| `ability_physical_slash` | `lorc/sword-spin` | sword-spin.svg | Rotating sword = slash/cleave archetype |
| `ability_physical_thrust` | `delapouite/spears` | spears.svg | Thrust register |
| `ability_archer` | `delapouite/high-shot` | high-shot.svg | Bow-string-pulled silhouette |
| `ability_dodge` | `lorc/run` | run.svg | Sprint silhouette = dash/dodge |
| `ability_block` | `lorc/heater-shield` | heater-shield.svg | Shield-block tag |
| `ability_buff_self` | `delapouite/strong` | strong.svg | Bicep-flex = self-buff |
| `ability_summon` | `lorc/raven` | raven.svg | Bird-summon (pet/companion archetype placeholder) |

#### § 1.3.2 — Status indicator icons (10 icons)

Buff/debuff/CC ailment readouts. Used in the small-icon strip above the player character + above enemy nameplates.

| Role | game-icons.net path | Filename | Why |
|---|---|---|---|
| `status_stun` | `delapouite/star-swirl` | star-swirl.svg | Stars circling head = classic stun |
| `status_freeze` | `lorc/frozen-block` | frozen-block.svg | Ice-block lock |
| `status_silence` | `delapouite/silenced` | silenced.svg | Speech-balloon-with-slash |
| `status_burn` | `lorc/flame` | flame.svg | DoT fire flame |
| `status_poison` | `lorc/poison-bottle` | poison-bottle.svg | Bottle with skull |
| `status_bleed` | `delapouite/bleeding-wound` | bleeding-wound.svg | Drop with cut |
| `status_slow` | `lorc/snail` | snail.svg | Slow-motion silhouette |
| `status_root` | `lorc/vine-leaf` | vine-leaf.svg | Wrap-around vine |
| `status_buff` | `delapouite/upgrade` | upgrade.svg | Arrow-up = positive buff (generic) |
| `status_debuff` | `delapouite/downgrade` | downgrade.svg | Arrow-down = negative debuff (generic) |

#### § 1.3.3 — Inventory category icons (4 icons)

Used as section dividers in inventory UI.

| Role | game-icons.net path | Filename |
|---|---|---|
| `inv_weapon` | `lorc/crossed-swords` | crossed-swords.svg |
| `inv_armor` | `lorc/chest-armor` | chest-armor.svg |
| `inv_accessory` | `lorc/gem-necklace` | gem-necklace.svg |
| `inv_consumable` | `lorc/potion-ball` | potion-ball.svg |

#### § 1.3.4 — HUD widget icons (4 icons)

Replacements for current HUD placeholders. The existing `craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/PNG/Icons.png` is acquired and provides slot-frame infrastructure — these game-icons.net silhouettes overlay the slot frames.

| Role | game-icons.net path | Filename |
|---|---|---|
| `hud_health` | `lorc/health-normal` | health-normal.svg |
| `hud_mana` | `lorc/spinning-blades` | spinning-blades.svg (or `delapouite/glass-shot` for alternative) |
| `hud_dash` | `delapouite/wingfoot` | wingfoot.svg |
| `hud_potion` | `lorc/potion-of-madness` | potion-of-madness.svg |

### § 1.4 — Combined attribution string for credits.txt

The 28 icons span ~6-8 unique contributors (Delapouite, Lorc, Carl Olsen, John Colburn, Skoll, Sbed, et al. — exact contributor list materializes per-icon when downloaded). The SIL-1.1 attribution requirement is satisfied by a single umbrella credit line referencing "various contributors on game-icons.net" + the link-back per § 5. Per § 4 of credits.txt below.

### § 1.5 — Drax v1.21+ wire-in path

1. Download the 28 icons (or the full ~25MB zip).
2. Place under `reincarnated-demo/public/assets/game-icons/<subcategory>/` per § 1.2 layout.
3. Author `reincarnated-demo/src/visuals/gameIcons.ts` exposing `loadGameIcon(role): Texture | null` with caching parallel to `_staticPropTextureCache` pattern in `ambientPropsExtension.ts`.
4. Wire `hud_*` icons into existing HUD widget rendering paths (replace current Graphics-rendered placeholders).
5. Wire `ability_*` + `status_*` into hotbar + status-strip rendering.
6. Wire `inv_*` into inventory UI section headers.
7. Verify visual register: silhouettes overlay correctly on `craftpix-free-basic-pixel-art-ui-for-rpg/PNG/Icons.png` slot frames; per-color background slots distinguish element/rarity.

---

## § 2 — Deliverable 2: Consistent prop scale + medium density rules + 8 new props

### § 2.1 — Scale convention

Per gandalf v1.7 0.75× shrink canon (applied as a multiplier ON TOP of existing per-prop renderScale values — NOT a replacement of the renderScale field). This downscales props uniformly for room composition coherence without changing per-prop scale ratios.

**Implementation pattern (drax v1.21+):**

```typescript
// In ambientPropsExtension.ts — add at module scope:
const PROP_RENDER_SCALE_OVERRIDE = 0.75;  // gandalf v1.7 prop-shrink canon

// In createDungeonStaticProp() and createDungeonLoopProp(), change line:
//   sprite.scale.set(desc.renderScale);
// To:
//   sprite.scale.set(desc.renderScale * PROP_RENDER_SCALE_OVERRIDE);

// Same change in createCoffinProp() (currently scale 1.5 → 1.125 effective)
// Same change in createMagicBookProp() (currently scale 1.2 → 0.9 effective)
```

**Pre-existing-asset scale audit (before override):**

| Prop | renderScale (existing) | Effective after 0.75× override | Source-sheet-cell px | Final rendered px |
|---|---|---|---|---|
| Book (animated/static) | 1.2 | 0.9 | 128×128 | 115×115 |
| Coffin | 1.5 | 1.125 | 80×80 | 90×90 |
| Candles (animated) | 1.5 | 1.125 | ~48×56 (corrected) | 54×63 |
| Torches (animated) | 2.0 | 1.5 | ~44×48 (corrected) | 66×72 |
| Fountain (animated) | 2.0 | 1.5 | ~48×48 (corrected) | 72×72 |
| Ladder (static) | 1.5 | 1.125 | 32×96 | 36×108 |
| Crate (static) | 1.8 | 1.35 | 32×32 | 43×43 |
| Barrel (static) | 1.8 | 1.35 | 32×48 | 43×65 |
| Column (static) | 1.8 | 1.35 | 32×64 | 43×86 |

This consistency means props no longer compete with combat-figure scale for visual attention.

### § 2.2 — Medium decoration density rules

Per-room prop count target:

| Room size category | Min props | Max props | Typical count |
|---|---|---|---|
| Small (< 400×400 px room rect) | 3 | 5 | 4 |
| Medium (400-700 px rect) | 4 | 7 | 5-6 |
| Large (> 700 px rect) | 6 | 9 | 7-8 |

Current `dungeonPropsForRoom()` returns exactly 4 positions hardcoded (see `ambientPropsExtension.ts` line 537-551). Drax v1.21+ extends to per-room-size variable density:

```typescript
export function dungeonPropsForRoom(
  roomX: number, roomY: number,
  roomW: number, roomH: number,
): Array<{ label: string; x: number; y: number }> {
  const roomArea = roomW * roomH;
  let propCount: number;
  if (roomArea < 160_000) propCount = 4;        // small
  else if (roomArea < 490_000) propCount = 6;   // medium
  else propCount = 8;                            // large

  const margin = 48;
  const labels = ['ladder', 'barrel', 'crate', 'column',
                  'sack', 'vase', 'rubble-a', 'rubble-b',
                  'bookshelf', 'bookpile', 'small-table', 'iron-bracer'];
  // Shuffle deterministically by room-seed, pick first propCount
  // Position spread along walls + corners avoiding player spawn (left-center)
  // ... implementation pattern parallel to existing 4-position spread
}
```

**Per-room variety rule:** within a room, prop labels are unique (no duplicate within the same room). Across rooms, the same label may appear. This avoids "all rooms have the same ladder + barrel + crate + column" monotony.

### § 2.3 — 8 new ambient prop descriptors

Source-coord-extracted by visual inspection of the on-disk PNGs. These extend `STATIC_PROP_DESCS` in `ambientPropsExtension.ts`. Existing 4 (`ladder`, `crate`, `barrel`, `column`) remain.

Constants needed (add to imports at top of `ambientPropsExtension.ts`):

```typescript
const PACK_169442 = '/assets/craftpix_catalogue_large/craftpix-net-169442-free-2d-top-down-pixel-dungeon-asset-pack/PNG';
const PACK_298079 = '/assets/craftpix_catalogue_large/craftpix-net-298079-top-down-dungeon-pixel-tileset-for-rpg-and-roguelike-game/PNG';
const PACK_GUILDHALL_189780 = '/assets/craftpix_catalogue_large/craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/PNG';
const OBJECTS_169442_URL     = `${PACK_169442}/Objects.png`;              // 384×96, confirmed PIL
const OTHER_OBJECTS_298079_URL = `${PACK_298079}/other_objects.png`;
const INTERIOR_OBJECTS_189780_URL = `${PACK_GUILDHALL_189780}/Interior_objects.png`;  // 384×384, confirmed PIL
```

Eight new descriptors (append to existing 4):

```typescript
const STATIC_PROP_DESCS: StaticPropDesc[] = [
  // === EXISTING 4 (drax v1.17 P5) ===
  { label: 'ladder',   url: OBJECTS_169442_URL,     sx: 96,  sy: 0,  sw: 32, sh: 96, renderScale: 1.5 },
  { label: 'crate',    url: OBJECTS_169442_URL,     sx: 128, sy: 32, sw: 32, sh: 32, renderScale: 1.8 },
  { label: 'barrel',   url: OBJECTS_169442_URL,     sx: 160, sy: 32, sw: 32, sh: 48, renderScale: 1.8 },
  { label: 'column',   url: OTHER_OBJECTS_298079_URL, sx: 0,   sy: 0,  sw: 32, sh: 64, renderScale: 1.8 },

  // === NEW 8 (drax v1.21+ Tier 5.1) ===

  // — From 169442 Objects.png (384×96) — additional cut-outs from same sheet —
  // burlap sack (gray/orange — visible right-mid region)
  { label: 'sack',     url: OBJECTS_169442_URL,         sx: 192, sy: 32, sw: 32, sh: 32, renderScale: 1.8 },
  // ceramic vase (blue — far-right region)
  { label: 'vase',     url: OBJECTS_169442_URL,         sx: 256, sy: 32, sw: 16, sh: 24, renderScale: 2.0 },
  // rubble pile A (orange/tan stone fragment cluster — mid-bottom)
  { label: 'rubble-a', url: OBJECTS_169442_URL,         sx: 288, sy: 64, sw: 24, sh: 16, renderScale: 1.8 },
  // rubble pile B (different cluster shape — adjacent)
  { label: 'rubble-b', url: OBJECTS_169442_URL,         sx: 320, sy: 64, sw: 24, sh: 16, renderScale: 1.8 },

  // — From 189780 (guildhall free-pack) Interior_objects.png (384×384) — interior props —
  // bookshelf (tall — for cathedral/mage-tower seasons)
  { label: 'bookshelf', url: INTERIOR_OBJECTS_189780_URL, sx: 0,   sy: 0,   sw: 64, sh: 96, renderScale: 1.2 },
  // small book pile (compact decoration; pairs with magic-book prop)
  { label: 'bookpile',  url: INTERIOR_OBJECTS_189780_URL, sx: 64,  sy: 64,  sw: 32, sh: 32, renderScale: 1.5 },
  // small wooden table (mid-room decoration)
  { label: 'small-table', url: INTERIOR_OBJECTS_189780_URL, sx: 128, sy: 64,  sw: 64, sh: 48, renderScale: 1.4 },
  // iron-bracer / wall-bracket (corner-mount decoration)
  { label: 'iron-bracer', url: INTERIOR_OBJECTS_189780_URL, sx: 192, sy: 0,   sw: 32, sh: 64, renderScale: 1.5 },
];
```

**Source-coord verification flag for drax:** the `Interior_objects.png` coords above are estimates based on the 384×384 dimensions; drax should visually inspect the sheet before final wire-in to confirm the bookshelf / bookpile / small-table / iron-bracer cells fall at the proposed (sx, sy, sw, sh) bounds. If coords are off, drax can adjust ±16px without changing the structural pattern. The 169442 Objects.png coords are based on the established drax v1.17 ladder/crate/barrel pattern (left half of sheet); the new sack/vase/rubble coords (right half) are extrapolations from the visual-inspection record in `dungeon-objects-quality-audit-2026-05-18.md` § 2.5.

### § 2.4 — License coverage for new props

- 169442 Objects.png: CraftPix-Free-Terms (covered by existing one-credit-line in credits.txt below).
- 298079 other_objects.png: CraftPix-Free-Terms (same).
- 189780 Interior_objects.png: CraftPix-Free-Terms (Free Top-Down Guild Hall Asset Pack — `License.txt` on-disk; same umbrella as other CraftPix-Free packs).

No new attribution surfaces; existing CraftPix-Free umbrella covers.

### § 2.5 — Test plan for prop wire-in

| Test | Verify |
|---|---|
| Boot demo any season | All 12 prop labels load without `[ambient-props-ext] static prop ... load failed` warnings |
| Small room | 3-5 props visible; no duplicates within the room |
| Medium room | 4-7 props visible; no duplicates within the room |
| Large room | 6-9 props visible; no duplicates within the room |
| Visual scale check | Props are 0.75× of pre-override size — visibly smaller than current; combat figures retain visual primacy |
| Cross-season variety | Different rooms across different seasons show different prop combos (variety achievable from 12-label pool) |
| Cathedral season (001003) | Bookshelf + bookpile appear at higher frequency (drax can add per-season label bias if desired; pure-random selection is the baseline) |

---

## § 3 — Deliverable 3: credits.txt consolidated text

**Authority:** Matt L3 lock 2026-05-18 — single credits.txt for all attribution surfaces.
**Current state:** `reincarnated-demo/public/credits.txt` (84 lines) is audio-only; visual-asset attribution surfaces are in `creditsOverlay.ts` (in-game F1 panel) without persistent file-level record.
**Lock:** consolidate all attribution into one `credits.txt` file. Drax v1.21+ deploys the text below as the new complete file contents.

### § 3.1 — Verbatim credits.txt content for deployment

```
Reincarnated — Credits & Attribution
=====================================
Updated: 2026-05-18 (consolidated single-file lock per Matt L3)
Maintainer: drax (demo seam)


SECTION A — VISUAL ASSETS
=========================

A.1 Game-icons.net (UI iconography)
-----------------------------------
Icons used: ~28 (ability/skill, status-indicator, inventory-category, HUD-widget)
Contributors: various (Lorc, Delapouite, Carl Olsen, Skoll, Sbed, John Colburn, et al.)
License: SIL Open Font License 1.1 (SIL-1.1)
Source: https://game-icons.net
Attribution: "Icons made by various authors at game-icons.net under SIL-1.1.
              See game-icons.net for individual contributor pages per icon."


A.2 CraftPix.net free-asset packs
---------------------------------
Packs used:
  - Free 2D Top-Down Pixel Dungeon Asset Pack (craftpix-net-169442)
  - Top-Down Dungeon Pixel Tileset for RPG and Roguelike Game (craftpix-net-298079)
  - Dungeon Tileset Pixel Top-Down for Indie Game (craftpix-net-125640)
  - Free Top-Down Pixel Art Guild Hall Asset Pack (craftpix-net-189780)
  - Free Basic Pixel Art UI for RPG (craftpix-net-255216)
  - Free Animated Magic Book Pixel Art Asset Pack (craftpix-net-809047)
  - Free RPG Monster Sprites Pixel Art (craftpix-561178)
  - Free 40 Loot Icons Pixel Art (craftpix free)
License: CraftPix-Free-Terms (commercial use permitted with attribution; no redistribution)
Source: https://craftpix.net
Attribution: "Free assets from craftpix.net — used under CraftPix Free Terms."


A.3 OpenGameArt (CC-permissive umbrella)
----------------------------------------
Contributors used:
  - artisticdude — RPG Sound Pack (audio; see Section B)
  - clintbellanger — Gold Treasure Icons 32×32 (CC-BY-SA 3.0; if wired)
  - bonsaiheldin — Gold Treasure Icons 16×16 (CC0; if wired)
License: CC0 + CC-BY 3.0 + CC-BY-SA 3.0 (per-asset; see OGA contributor pages)
Source: https://opengameart.org
Attribution: "OpenGameArt.org — various contributors under CC0 / CC-BY / CC-BY-SA licenses."


A.4 Seliel the Shaper (Mana Seed)
----------------------------------
Packs used:
  - 19.07c Treasure Chests 1 (ambient chest prop)
  - 20.05b Breakable Pots 1 (ambient breakable pot prop)
License: Mana-Seed-Commercial (commercial use permitted; 100% human-made)
Source: https://seliel-the-shaper.itch.io
Attribution: "Treasure Chests + Breakable Pots by Seliel the Shaper (Mana Seed)."


A.5 DerNachbar (Dire Dungeon Items)
------------------------------------
Pack: Dire Dungeon Items (259-item gear + loot + UI icon library)
License: CC-BY 4.0 (attribution required; no AI)
Source: https://dernachbar.itch.io/dire-dungeon-items
Attribution: "Dire Dungeon Items by DerNachbar — CC-BY 4.0."


A.6 chierit (Elementals series)
-------------------------------
Characters used:
  - Lightning Ronin (Full pack)
  - Light Valkyrie (Complete pack)
  - additional chierit Elementals characters (per session season loadouts)
License: Chierit-CC-BY-4.0 (CC-BY 4.0 with vendor attribution)
Source: https://chierit.itch.io
Attribution: "Elementals series character art by chierit — CC-BY 4.0."


A.7 Pimen (effects + VFX)
-------------------------
Packs used: various spell + effect packs (per session VFX loadouts; see in-game F1 credits for per-element list)
License: Commercial-Royalty-Free (some packs CC-BY 4.0 — see per-pack notes)
Source: https://pimen.itch.io
Attribution: "Spell + effect VFX by Pimen."


A.8 Pixogen (AFGameAssets)
--------------------------
Pack: Pixel Art RPG VFX Lite (Void Shield + other VFX)
License: AFGameAssets (commercial use permitted; modification permitted; attribution REQUIRED per § 3.A.1)
Source: https://pixogen.itch.io
Attribution: "Pixogen / AFGameAssets — Antoine Fauville."


A.9 Frostwindz / Alenia / CreativeKind / Codemanu / Pixel Art VFX (free-character set)
--------------------------------------------------------------------------------------
Packs used: Pixel Art VFX (Blood Mage, Necromancer, Rogue, Starcaller, Vampire — FREE versions);
            Holy Spell Effects (CreativeKind); Impact FX Pack (Codemanu); Deathbringer VFX;
            Pixel Art Atmospheric (weather/biome FX)
License: Mixed (Itch-Standard-No-Redistribution for most; per-vendor pages canonical)
Source: itch.io per vendor
Attribution: "VFX + atmospheric effects by Frostwindz, Alenia, CreativeKind, Codemanu, Deathbringer,
              and various itch.io creators."


A.10 Pixel Art RPG VFX Lite (Pixogen) — see A.8
A.11 Magic Potions Pack V1 (AquaSenshi) — Pixel Art Potions Medieval RPG; commercial-license, free.
A.12 GandalfHardcore Samurai — character set (see in-game F1 for per-character credits).


SECTION B — AUDIO ASSETS
========================

B.1 Kenney Interface + Impact Sounds
------------------------------------
License: CC0 (Public Domain)
Source: https://kenney.nl/assets
Usage: UI events (button-click, menu-open/close, error, drop, confirmation);
       Layer-3 foley (physical impact, hit-confirm, glass-break, bell-chime composite for holy element)


B.2 OGA RPG Sound Pack (artisticdude)
-------------------------------------
License: CC0 (Public Domain)
Source: https://opengameart.org
Usage: Layer-1 physical melee SFX (swing variants, sword-unsheathe); Layer-1 magic cast fallback


B.3 Leohpaz RPG Essentials SFX (Free)
-------------------------------------
License: Itch-Standard-No-Redistribution (commercial use permitted; no redistribution outside engine)
Source: https://leohpaz.itch.io
Usage: Layer-1 elemental spell SFX (fire, water, wind, earth, lightning, shadow, charge, poison);
       Layer-3 UI events; Layer-3 buffs/heals/debuffs; Layer-3 combat foley; Layer-3 player movement


B.4 Leohpaz Minifantasy Dungeon Audio (Free)
---------------------------------------------
License: Itch-Standard-No-Redistribution
Source: https://leohpaz.itch.io
Usage: Layer-3 physical foley (melee combat, chest-open, dash); Layer-3 dungeon environment foley


B.5 TomMusic Free Fantasy 200 SFX
---------------------------------
License: Itch-Standard-No-Redistribution
Source: https://tommusic.itch.io
Usage: Layer-1 spell SFX supplement (fire/water/earth spells); Layer-3 foley (footsteps, doors, chests);
       Layer-4 atmospheric ambient supplement


B.6 kmontesdev Fantasy Ambient Pack
-----------------------------------
License: CC0 (Public Domain)
Source: https://drive.google.com/drive/folders/1tlJMeJp5PabLjmHyc3kTVd5dPycUKSav
Usage: Layer-4 atmospheric ambient; Layer-3 foley supplement


B.7 PixelLoops Ultimate Game Ambient Sound Effects Pack
-------------------------------------------------------
License: Royalty-Free-Single-User (single-user perpetual; $3.59 acquisition 2026-05-17)
Source: https://pixelloops.itch.io/ultimate-game-ambient-sound-effects-pack
Usage: Layer-4 atmospheric ambient (all 8 canon biomes: dungeon, cave, forest, swamp, desert,
       ruined-temple, glowing-cave composite, sewer composite)


B.8 WSP — WOW Sound Pixel Magic SFX Pack (if wired — Q-MATT-AUDIO-1 acquisition pending)
-----------------------------------------------------------------------------------------
License: Itch-Standard-No-Redistribution (commercial use permitted)
Source: https://wowsound.com
Usage (if acquired): Layer-1 substrate SFX upgrade for 7 magic elements (cluster-A retro-pixel register)
Status: ACQUISITION PENDING per Matt Q-MATT-AUDIO-1


B.9 Suno AI (existing tracks season_001001-005)
------------------------------------------------
License: Proprietary-Suno-Pro
Status: PARKED-MATT — Suno Pro terms for game-embedded audio pending Q-MATT-2 verification
Usage: Layer-5 music (Seasons 001001-005 direct; 002011-015 via Option-A rotation pending Q-MATT-2)


B.10 Bit By Bit Sound / Little Robot Sound Factory
---------------------------------------------------
License: CC-BY-3.0 (Little Robot) / Itch-Standard-No-Redistribution (Bit By Bit)
Status: NOT WIRED in v1.15+ (DEFER per elrond recommendation); flagged Q-MATT-3 for pre-demo-ship gate


SECTION C — PROJECT CONTRIBUTORS
================================

Project lead + design: Matt (mhwetmore@gmail.com)
Co-design: 11-year-old son (gameplay concepts + art direction input)
Synthetic engineering team: knight-rider, gandalf, jack-ryan, gamora, rocket, star-lord, drax,
  reincarnated-demo, legolas, elrond (Claude-based agent personas under matt's direction)


SECTION D — LEGAL NOTES
=======================

D.1 License classes summary
---------------------------
This project consumes assets under the following license classes:
- CC0 (public domain — no attribution required, attribution maintained as courtesy)
- CC-BY-3.0, CC-BY-4.0 (attribution required; attribution maintained in this file)
- CC-BY-SA-3.0 (attribution + share-alike; ensure derivative works carry same license — REVIEW BEFORE SHIPPING DERIVATIVES)
- SIL-1.1 (Open Font License; attribution + link-back; copyleft for "fonts" — interpreted broadly for icon-font corpus)
- CraftPix-Free-Terms (commercial use; attribution required; no redistribution of the source pack)
- Mana-Seed-Commercial (Seliel the Shaper commercial tier; 100% human-made)
- AFGameAssets (Pixogen / Antoine Fauville; § 3.A.1 attribution required)
- Chierit-CC-BY-4.0 (CC-BY-4.0 with chierit vendor attribution)
- OGA-Permissive (OpenGameArt umbrella; per-asset CC-license applies)
- Itch-Standard-No-Redistribution (commercial use; no asset redistribution outside this game)
- Royalty-Free-Single-User (single-user perpetual; PixelLoops pattern)
- Proprietary-Suno-Pro (Suno AI; PARKED pending Matt verification Q-MATT-2)


D.2 Per-asset attribution lookup
---------------------------------
For per-asset license verification + attribution detail, consult the in-game F1 credits overlay
(`creditsOverlay.ts`), which exposes per-pack attribution + per-vendor URL at runtime.

For curatorial / data-layer attribution detail, consult the catalogue DB
(`agentic_orchestration/research/curated/catalogue.db`) at the elrond seam — `license_class` column
on `catalogue_assets` (schema v1.6+, pending elrond v1.12) tracks per-asset specific license.


D.3 Pending Matt acquisitions / verifications
----------------------------------------------
- Q-MATT-AUDIO-1: WSP (WOW Sound) $49 acquisition for Layer-1 substrate upgrade
- Q-MATT-AUDIO-2: WS3 ($99) + WS1 ($35) for RED-cell composite resolution at VS2b gate
- Q-MATT-2: Suno Pro game-embed terms verification (gates Suno music inclusion)
- Q-MATT-3: Bit By Bit Sound pre-demo-ship attribution decision
- Mucho Pixels Dungeon Tileset ($4.95) — VS2b conditional (only if Seliel softness flagged)
- Pixogen Full Pack (€19.99 standalone OR €59.99 Mega Pack) — VS2b decision

End of credits.txt.
```

### § 3.2 — Deployment notes for drax

- This file replaces `reincarnated-demo/public/credits.txt` IN ITS ENTIRETY.
- Cross-check against `creditsOverlay.ts` to confirm the in-game F1 panel surfaces the same attribution information (any divergence is a curation-drift signal — flag to elrond if found).
- The file is intentionally markdown-free plain text (consistent with current `credits.txt`). The structure uses `===` and `---` separators for human readability; no rendering framework dependency.

---

## § 4 — Deliverable 4: Catalogue-DB additive schema (cross-reference)

Full schema migration spec: `agentic_orchestration/research/curated/catalogue-db-schema-v2-2026-05-18.md`.

### § 4.1 — Summary (one paragraph)

Two new NULL-allowed columns on `catalogue_assets`:
- `usage_recommendation TEXT` with CHECK enum — surfaces the per-file consumption-intent (floor_tile_pool / ambient_prop_pool / composite_reference_DO_NOT_TILE / etc.) at the data layer. Prevents the slicer-shredding defect class that produced Matt's "stairs sprite is bad" verdict.
- `license_class TEXT` with CHECK enum — surfaces the specific license instance (SIL-1.1 / CC-BY-4.0 / CraftPix-Free-Terms / etc.) at the data layer. Enables programmatic credits.txt generation + per-license consumption rules.

Plus two partial indexes on the new columns; plus `schema_meta` row v1.6.

**Migration is spec-only in this dispatch (v1.11).** Execution of the actual SQL migration is a future elrond v1.12 dispatch when knight-rider sequences it.

### § 4.2 — Downstream drax consumption (when migration lands)

Drax v1.21+ does NOT need to consume the schema directly in the icon/prop wire-in pass — the schema additions are upstream-curator-facing surfaces. Future curation passes will populate `usage_recommendation` + `license_class`, after which drax can query for safety filters (see schema spec § 3.1).

---

## § 5 — Acceptance criteria (drax v1.21+ wire-in)

When drax fires v1.21+ (post-mobile-chain + post-chierit-monster-wiring; lowest-priority VS2a polish pass):

- [ ] 28 game-icons.net icons downloaded + placed under `reincarnated-demo/public/assets/game-icons/<subcategory>/`
- [ ] `reincarnated-demo/src/visuals/gameIcons.ts` module authored (or icons integrated into existing HUD modules; drax discretion)
- [ ] HUD widget icons (4) replace existing placeholders
- [ ] Ability hotbar + status strip wired (where present in current demo UI)
- [ ] Inventory category dividers wired (if inventory UI is present in VS2a)
- [ ] `PROP_RENDER_SCALE_OVERRIDE = 0.75` applied to `STATIC_PROP_DESCS`, `DUNGEON_LOOP_DESCS`, coffin, book
- [ ] 8 new prop descriptors added to `STATIC_PROP_DESCS` (sack, vase, rubble-a, rubble-b, bookshelf, bookpile, small-table, iron-bracer)
- [ ] `dungeonPropsForRoom()` extended to per-room-size variable density (small=4 / medium=6 / large=8)
- [ ] Within-room prop label uniqueness enforced
- [ ] `credits.txt` deployed verbatim from § 3.1
- [ ] Visual smoke test per § 2.5 passes
- [ ] No regression on combat figure visibility (props are visibly smaller; combat retains visual primacy)
- [ ] `npm run build` clean (TS errors zero)
- [ ] Attribution surfaces: existing CraftPix-Free-Terms + game-icons.net credit lines cover; no new spend
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Tag `drax/v1.21-tier-5-1-5-2-wire-in-1` (local; no push per ADR-006)

---

## § 6 — Out of scope (drax v1.21+ MUST NOT do)

- ❌ Acquire Game-icons.net icons via spend (they are SIL-1.1 free; direct download).
- ❌ Modify catalogue.db schema (elrond v1.12 owns the migration; v1.11 is spec-only).
- ❌ Modify `creditsOverlay.ts` in-game F1 panel (out of scope; F1 panel is separate from credits.txt file).
- ❌ Pre-empt drax v1.18.5 hotfix or v1.20 chierit (those land first per knight-rider sequencing).
- ❌ Touch hybrid_mage (canonical-6 locked).
- ❌ Push tag (ADR-006).
- ❌ Change PROP_RENDER_SCALE_OVERRIDE value without consulting gandalf v1.7 canon (0.75 is the locked value).

---

## § 7 — Coordination state

- **Predecessor:** elrond v1.10 chierit substrate mapping (just shipped 2026-05-18).
- **Triggers downstream:** drax v1.21+ wire-in (queued post-mobile chain + post-chierit-monster-wiring; lowest VS2a polish priority).
- **Parallel-safe with:** rocket new-season regen + drax v1.18.5 critical hotfix (different repos; no conflicts).
- **Knight-rider sequencing:** receives this brief + companion schema spec + manifest extension + AGENT_STATE update.

---

*Brief authored 2026-05-18 by elrond per Matt L3 Tier 5.1 + Tier 5.2 locks. Companion to catalogue-db-schema-v2 + ambient-props-subset-vs2a manifest extension. Drax v1.21+ may consume this brief directly when sequenced.*
