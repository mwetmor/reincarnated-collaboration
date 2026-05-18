# Dungeon Objects Quality Audit — VS2a — 2026-05-18

**Authority:** Matt L3 playtest 2026-05-18: *"the stairs sprite is a really bad choice. Generally all of the dungeon objects are poor."*
**Dispatch:** `agentic_orchestration/dispatches/2026-05-18-elrond-dungeon-objects-quality-audit.md`
**Author:** elrond
**Type:** Pattern A — quality audit + swap-candidate scout; no spend; no sprite swaps (drax v1.17 follow-on)
**Scope:** all dungeon objects wired in demo as of drax v1.13 + v1.16.x
**Register reference:** HYBRID a3 — hand-drawn pixel-art HD-2D-shaped per `canonical/story/style-register.md` (NOT retro-pixel; dispatch language "Cluster A retro-pixel" is sonic-register nomenclature mapped imprecisely; visual register lock is HD-2D-shaped HYBRID a3)
**Predecessor:** drax v1.13 completion record + drax v1.16.x audio/holy hotfixes (see `2026-05-17-drax-vs2a-final-sprint-comprehensive-wiring.md`)

---

## Executive summary

**Root-cause finding.** The "bad stairs sprite" and "generally poor dungeon objects" verdict traces to **one structural defect** in drax v1.13 Area 1 wiring: the `walls_floor.png` composite sheets from the three WIRE-NOW CraftPix dungeon tilesets (net-298079, net-125640, net-169442) are **NOT auto-tilable 16px grids** — they are **architecture-piece atlases** containing complete wall sections, stair frames, doorway compositions, columns, and alcoves arranged in irregular non-tile-aligned patterns. Drax's slicer treats every cell of rows 4-8 as a "floor tile candidate" and tiles them deterministically across the floor, producing **stair-fragments and wall-bar-fragments scattered across every room's floor**. Matt is seeing stair geometry where floor tiles should be — because the slicer is shredding a doorway-with-stairs composite into 16px tiles and using those slices as repeated floor coverage.

**Secondary findings.**
- The dedicated **clean floor tile sheets exist** in 298079 (`plates.png`, 208×128, a proper 13×8 grid of 16px stone-plate floor tiles) and were NOT used. Drax's tile slicer reaches the wrong sheet.
- Drax frame-count estimates for animated props (candles, torches, fountain) are wrong by 1.5-4× — actual sheet dimensions (224×288 torches, 432×224 candles, 288×64 fountain) do not match the assumed (192×64 / 256×64 / 384×64) layouts. Drax inferred without inspection; this is acknowledged in drax's TODO(drax) markers.
- The 169442 `Objects.png` (384×96) contains the **highest-quality dungeon object library currently on disk**: clean cut-out stone stairs, wooden ladders, crates, barrels, sacks, vases, treasure boxes — none of which are wired. This is the lead swap candidate for stairs + general dungeon prop variety.
- The 298079 `stairs.png` (192×240) is a dedicated stair-piece sheet (wooden trap-doors + alcove-with-stair frames) — also not wired. Mid-quality (3/5); functional but reads more as "cellar trapdoor" than "dungeon descent."
- The Seliel chests + pots (drax v1.12 wiring) are high quality (4/5) and register-fit. They were NOT flagged by Matt; the "generally poor" verdict is **specifically about CraftPix-tileset-derived wiring**, not the Seliel-wired ambient props.

**Recommended path for drax v1.17.** Three priority swaps + one frame-count correction batch + one decommission:
1. **PRIORITY 1 — Stop tiling walls_floor.png rows 4-8 as floor tiles.** Switch to 298079 `plates.png` as the proper floor-tile source (13×8 clean grid). Quality jump: 1/5 → 4/5.
2. **PRIORITY 2 — Wire stairs explicitly.** Use 169442 `Objects.png` top-left stair piece for season_001003 (cathedral). Use 298079 `stairs.png` for the others as fallback. Render at the exit-door threshold position (or as ambient decoration in corner positions). Quality jump: 1/5 → 4/5 (169442) or 3/5 (298079).
3. **PRIORITY 3 — Add high-quality dungeon prop variety from 169442 `Objects.png`** (crates, barrels, sacks, vases — at 16-24px source size × 1.5-2× scale). Eliminates Matt's "generally poor" verdict.
4. **Frame-count correction batch.** Drax-side TODO already noted in code: candles (432×224 not 256×64), torches (224×288 not 192×64), fountain (288×64 not 384×64). Visually-inspectable fix.
5. **Decommission row-shredded "wall tiles" on perimeter.** Drax already has a thin 8px Graphics perimeter overlay as a backup; promote that to the primary wall rendering until a proper auto-tile path lands (deferred to VS2b).

**Acquisition flag list.** **EMPTY.** All identified swap candidates are already on disk in the CraftPix mega catalogue acquisitions. No Matt spend recommended for VS2a. Future VS2b commission candidates flagged at end (Mucho Pixels for coffin/weapon-stand/pot states; Anokolisa free 500-sprite dungeon pack for general variety) but not VS2a-blocking.

---

## 1. Current-state audit

### 1.1 Object inventory (every dungeon object class wired in demo)

| # | Object class | Source pack | Source file | Wiring module | Quality (1-5) | Register fit (1-5) | Matt-flag |
|---|---|---|---|---|---|---|---|
| 1 | **Floor tiles** | CraftPix net-298079 / 125640 / 169442 | `walls_floor.png` rows 4-8 | `dungeonTileset.ts::drawTilesetFloor` | **1** | 2 | YES — root cause |
| 2 | **Hallway floor tiles** | same | same rows | `dungeonTileset.ts::drawTilesetHallwayFloor` | **1** | 2 | YES — same as #1 |
| 3 | **Wall tiles (sprite-based)** | same | `walls_floor.png` rows 0-3 | `dungeonTileset.ts::drawTilesetWalls` | **1** | 2 | YES — fragmented wall slices |
| 4 | **Wall perimeter (Graphics)** | n/a — procedural | `roomRenderer.ts` 8px stroke | `roomRenderer.ts` | 3 | 4 | OK (backup path) |
| 5 | **"Stairs" sprite (apparent)** | walls_floor.png composite — UNINTENDED | walls_floor rows 4-8 cells | tiled as floor (#1) | **1** | 1 | YES — Matt's explicit call-out |
| 6 | **Doors / gates (Graphics)** | n/a — procedural | `roomRenderer.ts::_drawDoorThreshold` | `roomRenderer.ts` | 3 | 4 | OK |
| 7 | **Chests** | Seliel Treasure Chests | `19.07c/treasure chests.png` | `ambientProps.ts::ChestProp` | **4** | 4 | OK — Matt did NOT flag |
| 8 | **Pots (breakable)** | Seliel Breakable Pots | `20.05b/breakable pots (*).png` | `ambientProps.ts::PotProp` | **4** | 4 | OK — Matt did NOT flag |
| 9 | **Coffins** | CraftPix net-298079 | `coffins.png` | `ambientPropsExtension.ts::CoffinProp` | **4** | 4 | OK — closes G-COFFIN |
| 10 | **Candles** | CraftPix net-298079 | `candles.png` (432×224) | `ambientPropsExtension.ts::createDungeonLoopProp('candles')` | **2** | 3 | YES — frame count wrong (drax assumed 4@64; actual layout differs) |
| 11 | **Torches** | CraftPix net-298079 | `torches.png` (224×288) | `ambientPropsExtension.ts::createDungeonLoopProp('torches')` | **2** | 3 | YES — frame count wrong (drax assumed 3@64; actual is larger grid) |
| 12 | **Fountain** | CraftPix net-125640 | `fountain_animation.png` (288×64) | `ambientPropsExtension.ts::createDungeonLoopProp('fountain')` | **2** | 3 | YES — frame count wrong (drax assumed 6@64; actual 6@48 likely) |
| 13 | **Magic book (animated)** | CraftPix net-809047 | `Open_book.png` (1088×816) | `ambientPropsExtension.ts::createMagicBookProp` | **4** | 4 | OK |
| 14 | **Magic book (static)** | CraftPix net-809047 | `Open_book_bookmarks1.png` | same | **4** | 4 | OK |
| 15 | **Hazard: ghost trap** | CraftPix net-298079 | `ghost_trap.png` | `dungeonTileset.ts::spawnDungeonHazardProp('ghost_trap')` | 3 | 3 | OK (not Matt-flagged but unconfirmed in playtest) |
| 16 | **Hazard: statue fire** | CraftPix net-298079 | `Statue_fire.png` | `spawnDungeonHazardProp('statue_fire')` | 3 | 3 | OK |
| 17 | **Hazard: dragon trap** | CraftPix net-298079 | `dragon_trap.png` | `spawnDungeonHazardProp('dragon_trap')` | 3 | 3 | OK (frame-count estimate may be off) |
| 18 | **Hazard: fire trap** | CraftPix net-125640 | `fire_trap.png` | `spawnDungeonHazardProp('fire_trap')` | 3 | 3 | OK |
| 19 | **Hazard: spike trap** | CraftPix net-125640 | `spike_trap.png` | `spawnDungeonHazardProp('spike_trap')` | 3 | 3 | OK |
| 20 | **Floor loot (DireDungeon)** | DireDungeon Items | `DireDungeonItemsTileset_by_DerNachbar` | `direDungeonLoot.ts` | 4 | 4 | OK (separate seam — gear pipeline) |
| 21 | **Gear drops (visual)** | same | same | `gearDrop.ts` | 4 | 4 | OK |

### 1.2 Quality-rating rubric (1-5)

- **5:** High-quality pixel-art HD-2D shape; register-coherent with combat sprites; reads clean at rendered scale; per-pack craftsmanship visible.
- **4:** Strong pixel art; register-fit; minor concerns (e.g., source register is SNES-era softer than combat — drax v1.12 flag) but does not break read.
- **3:** Functional; quality-adequate but not standout; minor frame-count/scale issues; would benefit from polish.
- **2:** Wired but with clear defects (wrong frame count, mis-sized, partial render); needs correction but salvageable.
- **1:** Structurally broken — wrong source, wrong slicing, wrong layout interpretation; produces visible artifacts. Matt-visible.

### 1.3 Register-fit rubric (1-5)

- **5:** HD-2D hand-drawn pixel-art register per style-register.md Candidate B lock; matches combat sprite register exactly.
- **4:** Compatible register; minor softness or palette divergence acceptable.
- **3:** Same-family pixel-art but discernibly different sub-register (e.g., SNES-leaning where combat is darker fantasy).
- **2:** Pixel-art but mis-fit (e.g., colored stone fragments scattered as floor; pieces don't tile clean).
- **1:** Register break — clearly wrong (e.g., trapdoor read as stair; doorframe read as floor tile).

### 1.4 The structural defect — diagnostic detail

The three CraftPix dungeon `walls_floor.png` sheets are composition reference atlases, NOT clean tilesets:

**net-298079 walls_floor.png (224×352 = 14 cols × 22 rows at 16px).** Visual inspection:
- Rows 0-3 (drax "wall tiles"): dark stone wall sections with mixed elements — column capitals, arched windows, alcoves cut into walls. Slicing into 16px cells produces broken fragments of column tops and window frames.
- Rows 4-8 (drax "floor tile candidates"): contains **stair-frame compositions** — square doorway frames with stone stair pieces inside. When sliced and tiled across a room floor, the player sees stair-fragments repeated across the floor.
- Rows 9-21: more composite architecture (coffin reliefs, water-coast pieces, large stone slabs).

**The clean floor tile sheet exists separately: `plates.png` (208×128 = 13 cols × 8 rows at 16px).** Pure repeatable stone-plate floor tiles, color-coded variants, with light-gray "outdoor" and dark "indoor" stone plates. This is the sheet that should be tiled across floors.

**net-125640 walls_floor.png (192×336 = 12 cols × 21 rows at 16px).** Even worse mismatch:
- Top portion: wooden-plank trap doors with iron banding (NOT walls and NOT floor — these are dungeon doors/hatches).
- Middle portion: doorway frames with stone stairs descending (proper stair-piece composition).
- Bottom portion: square stone-slab door-blocks.

When drax's slicer renders rows 4-8 of this sheet as "floor tile candidates," every tile-position in the room shows a fragment of a stair-step or doorframe stone. **This is precisely the "stairs sprite is bad" Matt observed.**

**net-169442 walls_floor.png (208×368 = 13 cols × 23 rows at 16px).** Similar architecture-atlas pattern: blue-stone walls with carved cut-outs, columns, doorways, and one clear stair-descent composition. Same slicer-shredding defect.

The bottom-right corner of all three sheets typically contains a small set of clean floor tiles (the "plate" tiles), but drax's slicer doesn't reach them — it's sampling from the architecture rows.

---

## 2. Swap-candidate scout

Priority order: **stairs** (Matt-explicit call-out) → **floor tiles** (root cause; affects every encounter) → **animated props** (frame-count corrections) → **prop variety** (general improvement).

### 2.1 Stairs — three swap candidates ranked

| Rank | Source pack | Source file | Source coords | License | Register fit | Drop-in or preprocess | Note |
|---|---|---|---|---|---|---|---|
| **A (LEAD)** | CraftPix net-169442 | `Objects.png` (384×96) | top-left ~32×64px region (visual: clean stone descending-stairs piece with stair-step shading + fish-bone detail above) | CraftPix-Free-Terms (commercial; one credit line covers all 298079/125640/169442 packs) | **5** — clean HD-2D pixel-art, distinct stair geometry, blue-gray stone consistent with 169442 wall palette | **Drop-in** — single 32×64 sprite extraction; render at 2-2.5× scale → 64-80px rendered; place at exit-door threshold or room corner | Already on disk |
| **B** | CraftPix net-298079 | `stairs.png` (192×240) | full sheet — 3 cols × 5 rows of dedicated stair pieces (wood trapdoors top rows; stone alcove-with-stairs bottom rows; 64×48 cell-size approximate) | same license | **3** — wood trapdoor pieces read more as cellar-hatches than dungeon stairs; alcove-stair pieces (bottom 2 rows) are functional | **Drop-in for bottom 2 rows** (alcove-stairs); upper rows (wooden trapdoors) should not be used as descent-stairs | Already on disk; bottom-rows usable, top-rows reject |
| **C** | CraftPix net-169442 | `decorative_cracks_floor.png` (128×240) | top region — iron-bar pit-grate + horizontal-descent stair pieces | same | **3** — pit-grate read is more "trapped pit" than "stairs"; usable for hazard rather than stair | **Conditional use** — frame as hazard, not as descent-stair; preprocess to isolate pit-grate cells | Already on disk; better matched for trap-element than stair |

**Recommendation:** Candidate A (169442 `Objects.png` top-left stair piece) as primary. Candidate B (298079 `stairs.png` bottom-rows alcove-stairs) as per-season fallback when 169442 palette doesn't fit. Candidate C as a hazard, not a stair.

### 2.2 Floor tiles — single high-confidence swap

| Source pack | Source file | Layout | License | Register fit | Drop-in or preprocess |
|---|---|---|---|---|---|
| CraftPix net-298079 | `plates.png` (208×128) | **13 cols × 8 rows of 16px clean stone-plate floor tiles** — light gray + dark gray variants in clear grid layout | CraftPix-Free-Terms | **5** — purpose-built floor tile sheet; pure repeatable grid | **Drop-in** — replace `walls_floor.png` row 4-8 sampling with `plates.png` full-sheet sampling; render at 2× scale (32px tiles); same alpha + variant logic as current |

**Recommendation:** Drax v1.17 replaces the floor-tile source from `walls_floor.png` rows 4-8 to `plates.png` entirely for net-298079. For 125640 and 169442, the same fix applies — they each likely have a similar dedicated floor-plate sheet hidden in their composite (drax visual inspection during swap-implementation will confirm; if not, use 298079 `plates.png` for all three seasons as a safe default — the palette is appropriately neutral).

### 2.3 Walls (perimeter) — keep procedural path; defer sprite-walls to VS2b

The `walls_floor.png` rows 0-3 sprite-wall rendering is **structurally broken in the same way as floor**: composite atlas sliced into 16px cells produces fragmented column-capitals and window-frame pieces tiling around the perimeter.

**Recommendation:** Drax v1.17 disables `drawTilesetWalls()` (or routes it through a no-op) and falls back to the existing 8px Graphics perimeter overlay (which drax retained as backup). This is the same procedural perimeter that shipped pre-tileset; it works. Proper sprite-wall auto-tiling (4-corner + 4-edge auto-tile system using the actual wall pieces from `walls_floor.png` rows 0-3 with manual cell-coordinate inspection) is **VS2b scope** — too much craft for VS2a.

### 2.4 Animated props — frame-count corrections (per existing TODO(drax) markers)

| Prop | Current assumption | Actual sheet dimensions | Recommended layout interpretation | Note |
|---|---|---|---|---|
| Candles (298079) | 4 frames × 64×64 | 432×224 | likely **9 cols × 4 rows = 36 frames at 48×56**, or **6 cols × 4 rows = 24 frames at 72×56** — visual inspection needed at swap time | Visual: 5-row grid of green-flame candles; each row is one candle variant × 6-8 frames horizontally; pick 1 row as the animation strip |
| Torches (298079) | 3 frames × 64×64 | 224×288 | likely **5 cols × 6 rows = 30 frames at ~44×48**, or **7 cols × 9 rows at 32×32** — visual inspection needed | Visual: teal-flame torches in multi-variant grid; pick the most-visible variant row |
| Fountain (125640) | 6 frames × 64×64 | 288×64 | **6 cols × 1 row × 48px wide**, or **9 cols × 1 row × 32px wide** | Likely a single horizontal animation strip; recompute frame width = 288 / N where N is frame-count from visual inspection |
| Dragon trap (298079) | 4 cols × 6 rows × 80px = 24 frames | 320×496 | actual ratio 320/80=4 cols × 496/80=6.2 rows → likely **4 cols × 6 rows × 80×82px** — drax estimate close but rows may be 82-83px not 80px | Minor adjustment; existing estimate is workable |

**Recommendation:** Drax v1.17 inspects each PNG visually (or via PIL) before re-deriving frame-counts; replaces the TODO(drax) comments with verified values. This is a 20-minute correction batch.

### 2.5 Additional dungeon prop variety — high-value low-cost expansion

The 169442 `Objects.png` (384×96) contains 10-12 distinct high-quality dungeon objects not currently wired. Recommended additions to `ambientPropsExtension.ts`:

| Object | Source coords (approximate) | Recommended use | Quality | Register fit |
|---|---|---|---|---|
| Wooden ladder | mid-top region, ~16×64 | ambient decoration (corner positions, near walls); alternative descent-marker | 4 | 5 |
| Rubble piles (orange/tan stone) | mid region, ~24×16 each, multiple variants | floor decoration scattered in 2-3 spots per room | 4 | 5 |
| Wooden crates / boxes | mid region, ~24×24 each | ambient decoration; could be loot-stand variant | 4 | 5 |
| Barrels (wood-banded) | right region, ~24×32 each | ambient decoration; alternative to current breakable pot variants | 4 | 5 |
| Burlap sacks (gray/orange) | right region, ~24×24 each | ambient decoration; great for loot-anchor visual | 4 | 5 |
| Ceramic vases (blue) | far-right region, ~16×24 each | ambient decoration; alternative breakable-pot variant | 4 | 5 |
| Treasure boxes | mid region, ~24×24 | secondary chest variant (alongside Seliel) | 4 | 5 |

The 298079 `other_objects.png` (160×352) similarly contains:
- Stone pillars / columns (gray + teal variants) — excellent for room-corner placement
- Chests with stone surrounds
- Hanging metal cages (chained from ceiling — great atmospheric prop)
- Bone piles + skulls (shadow/undead-element rooms)
- Gem piles + jugs (treasure-room flavor)

**Recommendation:** Drax v1.17 wires 3-4 of these as a "dungeon prop variety pack" placed 1-2 per room as ambient decoration. License is the same CraftPix-Free-Terms; one credit line covers all of these. Quality jump from current "candles+torches+fountain" minimal variety to "full dungeon room read."

### 2.6 Free-characters-and-vfx pack — no dungeon-object content

Audit confirmed: the `free_characters_and_vfx/` directory (Frostwindz + Alenia + character VFX) contains **no dungeon-object content** (verified via 169442/inventory paths and free-characters-and-vfx-inventory.jsonl). It is character + VFX only. No swap candidates from there for this audit.

### 2.7 Icons-and-props catalogue (legolas-1 + elrond curation, 79 rows)

Audit confirmed: zero stair entries (`grep -i stair` returned 0 rows). The curated icon/prop catalogue covers floor-loot (gear/gold/potions) + UI icons + chest/coffin/pot props. No additional stair candidates beyond what's already on disk in CraftPix dungeon tilesets.

---

## 3. Acquisition flag list

**EMPTY for VS2a.** All identified swap candidates are already on disk under `reincarnated-demo/public/assets/craftpix_catalogue_large/`. The license is CraftPix-Free-Terms (one credit line covers all three primary packs + the additional 5 WIRE-LATER packs in the dungeon-tileset subset manifest).

### 3.1 Future VS2b commission candidates (informational only — NOT VS2a-blocking)

| Pack | Cost | What it adds | When to revisit |
|---|---|---|---|
| **Mucho Pixels Dungeon Tileset** | $4.95 | Best-coverage single pack for chest + coffin + weapon-stand + pots with locked/unlocked/opened states; would be alternative chest source if Seliel softness becomes a Matt concern at Earth-Self surfaces | VS2b — only if Matt flags Seliel register-softness explicitly |
| **Anokolisa free dungeon crawler pack 500+ sprites 16x16** | FREE | Half-price acquisition (zero cost); rich 500-sprite library extends prop variety | VS2b — when prop-variety expansion warrants a second source pack |
| **Indie-Vova Dungeons & Pixels RPG 32x32** | $5.99 | 32px-native props (chests, barrels, crates, shields); better Path A-prime alignment (less upscale needed) | VS2b — only if 16px Seliel + CraftPix upscale-to-ARPG-band creates visible quality concern |

**No Matt acquisition decision needed for VS2a.** Minimizing per dispatch directive.

---

## 4. Recommendation summary for drax v1.17 swap dispatch

### 4.1 Priority-ordered swap targets

| Priority | Object class | Current source (BAD) | Target source (GOOD) | Effort | Quality jump |
|---|---|---|---|---|---|
| **P1** | Floor tiles (rooms + hallways) | `walls_floor.png` rows 4-8 (all 3 packs) | `plates.png` (208×128) from net-298079 — full sheet as variant pool | 30 min | 1/5 → 4/5 |
| **P2** | Stairs (room corners / exit threshold) | nothing wired explicitly; player sees stair-fragments in shredded floor (#1) | `Objects.png` top-left stair piece from net-169442 (primary) + `stairs.png` bottom-rows from net-298079 (fallback) | 30-45 min (load + slice + place) | 1/5 → 4-5/5 |
| **P3** | Wall perimeter | `walls_floor.png` rows 0-3 sliced as wall tiles | revert to procedural 8px Graphics perimeter (existing backup path) | 10 min (disable `drawTilesetWalls`) | 1/5 → 3/5 |
| **P4** | Animated props (candles, torches, fountain) | wrong frame-count estimates | visual inspection + frame-count correction | 20 min | 2/5 → 4/5 |
| **P5** | Dungeon prop variety (NEW) | not currently wired | 3-4 props from 169442 `Objects.png` + 298079 `other_objects.png` (ladder, crates, barrels, sacks, columns, rubble) | 60-90 min | adds new visible variety; closes Matt "generally poor" concern |

**Total drax v1.17 estimate: ~3-4 hours** for full audit-recommendation implementation.

### 4.2 What NOT to touch (preserve existing quality)

- **Seliel Treasure Chests** (`ambientProps.ts::ChestProp`) — rated 4/5; Matt did NOT flag. Keep as-is.
- **Seliel Breakable Pots** (`ambientProps.ts::PotProp`) — rated 4/5. Keep as-is.
- **Coffins** (`ambientPropsExtension.ts::CoffinProp`) — rated 4/5; closes G-COFFIN cleanly. Keep as-is.
- **Magic book** (`ambientPropsExtension.ts::createMagicBookProp`) — rated 4/5. Keep as-is.
- **Hazard props** (ghost_trap, statue_fire, dragon_trap, fire_trap, spike_trap) — rated 3/5; Matt did NOT specifically flag. Frame-count corrections noted but not P1.
- **DireDungeon floor loot + gear drops** — separate seam; rated 4/5. Out of scope.

### 4.3 Visual register check (HYBRID a3 — HD-2D hand-drawn pixel-art)

All recommended swap targets are within the locked register per `style-register.md` Candidate B:
- 169442 `Objects.png`: blue-stone pixel art with hand-drawn shading sensibility — **HD-2D-coded, register-fit 5/5**
- 298079 `plates.png`: clean stone-plate pixel art, neutral gray — register-fit 5/5
- 298079 `stairs.png` (bottom rows): stone alcove pixel art — register-fit 4/5 (slightly less hand-drawn-coded than 169442; still in-register)
- 298079 `other_objects.png` columns + cages + bones: dark-fantasy pixel art with column-capital detail — register-fit 5/5

No swap candidate introduces a register break. All preserve the HYBRID a3 lock.

---

## 5. Drax v1.17 handoff brief

**Audience:** drax (demo seam). **Trigger:** post-elrond-audit + post-drax-v1.16.2 completion (same-repo serialization per dispatch directive). **Estimated scope:** ~3-4 hours total.

### 5.1 Files to modify

| File | What to change |
|---|---|
| `/Users/admin/Games/reincarnated-demo/src/visuals/dungeonTileset.ts` | **P1:** Replace `_ensureTileTextures()` floor-tile source from `walls_floor.png` rows 4-8 to `plates.png` (208×128 = 13 cols × 8 rows at 16px). Add `_ensurePlatesTextures()` (or extend the existing function). Update `drawTilesetFloor()` + `drawTilesetHallwayFloor()` to consume the plates texture array. **P3:** Disable `drawTilesetWalls()` (return `false` immediately) so caller falls back to procedural perimeter; preserve the function shell for VS2b re-enablement. |
| `/Users/admin/Games/reincarnated-demo/src/visuals/dungeonTileset.ts` (continued) OR new `src/visuals/dungeonStairs.ts` | **P2:** New stair-prop module. Load 169442 `Objects.png` top-left stair piece (~32×64 source; render at 2-2.5× scale → 64-80px rendered). Expose `spawnStairProp(parent, x, y, seasonId)`. Per-season variant: season_001003 → 169442 stair; others → 298079 `stairs.png` bottom-rows. Place at exit-door threshold position (consume `exitDoor(room, dungeon)` from `world/topology.ts`). |
| `/Users/admin/Games/reincarnated-demo/src/visuals/ambientPropsExtension.ts` | **P4:** Visual-inspect actual frame layout for `candles.png` (432×224), `torches.png` (224×288), `fountain_animation.png` (288×64). Replace `DUNGEON_LOOP_DESCS` entries with corrected `frameW`, `frameH`, `cols`, `rows`, `frameCount` values. |
| `/Users/admin/Games/reincarnated-demo/src/visuals/ambientPropsExtension.ts` (continued) | **P5:** New prop descriptors for 169442 `Objects.png` extracted props (ladder, crate, barrel, sack, vase) + 298079 `other_objects.png` props (column, hanging-cage, rubble). Add `createDungeonStaticProp(parent, label, x, y)` factory + per-room placement helper (`dungeonPropsForRoom`) that returns 2-4 positions for ambient props. |
| `/Users/admin/Games/reincarnated-demo/src/main.ts` | Call `spawnStairProp()` at exit-door threshold per room init. Call new `dungeonPropsForRoom()` placement helper to scatter 2-4 props per room. |

### 5.2 Preprocessing required

**No alpha-channel preprocessing needed.** All CraftPix PNGs ship with alpha channels. All Seliel PNGs ship with alpha. PIL not required.

**No rescaling preprocessing needed at file level.** All scale handling is in-engine via `sprite.scale.set(N)` per the Path A-prime per-slug discipline. Source files stay at native pixel resolution.

**Visual inspection IS required for §5.1 P4 (frame-count corrections).** Drax should open each PNG (in a viewer or via PIL `Image.open(path); img.show()`) before re-deriving the frame-grid layout.

### 5.3 Test plan

| Test | Verify |
|---|---|
| Boot demo, season_001001 (water/lightning dark) | Floor tiles are clean stone-plate (light-gray + dark-gray repeating pattern); NO stair-fragments scattered; wall perimeter is procedural 8px stroke; chest + pot ambient props unchanged |
| Boot demo, season_001003 (holy/cathedral) | Floor tiles same as above; stair-prop visible at exit-door threshold from 169442 Objects.png — clean blue-stone stair piece, ~64-80px rendered, recognizable as descending-stairs |
| Boot demo, season_001005 (earth/fire) | Floor tiles consistent; stair-prop from 298079 stairs.png bottom-rows (alcove style) visible |
| Combat for >30s in any season | Animated candles + torches + fountain visible at proper frame rate (not frame-count-broken); coffin animation preserved; magic book preserved |
| Visual register check | All swapped sprites read as HD-2D hand-drawn pixel-art register; no visible style break against combat sprites + monster sprites |
| Manual placement spot-check | Each room has 2-4 ambient props (ladder OR crate OR barrel OR sack OR vase OR column OR cage) — NOT all the same — placed away from player spawn and aggro zones |

### 5.4 Failure-mode flags

- **If 169442 `Objects.png` top-left stair piece is not at exact (0, 0, 32, 64) cell:** drax visually re-inspects and adjusts source-coords. The image is 384×96; the stair piece is clearly visible as the leftmost shape in the top row — pixel-precise extraction may need ±4px tuning.
- **If 298079 `plates.png` floor tiles produce a visible "edge seam" between adjacent room tiles:** drax may need to add a sub-pixel positioning fix (currently the slicer renders with integer x/y — should be fine, but flag if seams appear).
- **If `drawTilesetWalls()` disable causes a visible regression** (e.g., the procedural perimeter is now visible but jarring): drax should NOT re-enable the broken sprite walls; instead, refine the procedural perimeter stroke (color, thickness, alpha) to match the new floor-tile palette.
- **If frame-count corrections produce visibly broken animations** (e.g., a torch frame shows half of two torches): drax falls back to the smallest-feasible frame count (1 frame = static sprite) until visual inspection confirms the correct grid.

### 5.5 Out-of-scope for drax v1.17 (defer to v1.18 or VS2b)

- Auto-tile system for sprite walls (proper 4-corner + 4-edge auto-tile from `walls_floor.png` rows 0-3 with manual cell-coord inspection) — VS2b
- Mucho Pixels acquisition for richer coffin/weapon-stand/pot states — VS2b, gated on Matt approval if Seliel softness becomes a concern
- Anokolisa free 500-sprite pack acquisition + curation — VS2b prop-variety expansion
- Animated stair-prop (descending animation when player approaches) — out of scope; static stair sprite is sufficient
- Per-season palette tinting of swap-in floor tiles — out of scope; native palette is acceptable across all 5 VS2a seasons

### 5.6 Acceptance criteria (drax v1.17)

- [ ] `npm run build` clean (TS errors zero)
- [ ] Boot demo per `npm run dev`; floor tiles read as clean stone-plate, NO stair-fragments visible
- [ ] Stair-prop visible at exit-door threshold in all 5 VS2a seasons
- [ ] Animated candles/torches/fountain visibly animating at correct frame rate (no broken-frame artifacts)
- [ ] At least 2 new ambient-prop classes wired (3 recommended: e.g., ladder + crate + barrel)
- [ ] All swapped sprites preserve HYBRID a3 register fit (no style break flagged)
- [ ] Attribution updated: existing "CraftPix dungeon tileset assets" line covers all new wirings (no new credit needed)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.17-dungeon-objects-quality-swaps-1` (local; no push per ADR-006)

---

## 6. Schema + curation notes (elrond domain)

### 6.1 Catalogue-side observation

The CraftPix dungeon-tileset subset manifest (`dungeon-tileset-subset-vs2a-2026-05-17.jsonl`) **correctly identifies** the rich object inventory in net-298079 (lists `stairs`, `coffins`, `arches/columns`, `other_objects` explicitly in the `room_tile_coverage` field). The defect is downstream — drax's wiring interpreted `walls_floor.png` as the sole tile-source and bypassed `plates.png` + `stairs.png` + `Objects.png` + `other_objects.png`.

**Curation lesson:** for VS2b commissions, surface a **per-file usage-recommendation field** in the subset manifest (e.g., `usage_recommendation: "floor_tile_pool"` for `plates.png`; `usage_recommendation: "ambient_prop_pool"` for `Objects.png`; `usage_recommendation: "composite_reference_DO_NOT_TILE"` for `walls_floor.png` until auto-tile authoring lands). This would prevent the slicer-shredding defect class entirely.

### 6.2 Schema migration recommendation

Append to `agentic_orchestration/research/curated/MIGRATION.md` (data-layer migration log): add a v1.x bullet noting the `usage_recommendation` field convention as a forward schema convention for dungeon-tileset subset manifests. Non-blocking; advisory for VS2b crawl scope.

### 6.3 Drift audit

Cross-reference `canonical/story/drift-audit.md` for any prior flag on tileset-vs-composite-atlas ambiguity. None found in current scan; this audit surfaces the distinction newly. Recommend Gandalf or jack-ryan note in decisions-log: **"composite reference atlases are NOT auto-tilable tilesets; sprite-tile rendering must consume purpose-built tile-grid sheets only."** — distillable as a discipline (mechanical-vs-composite distinction).

---

## 7. Audit completion record

**Authored:** 2026-05-18 by elrond
**Dispatch:** `2026-05-18-elrond-dungeon-objects-quality-audit.md`
**Scope completed:**
- [x] Current-state audit (Section 1; 21 dungeon object classes inventoried; ratings 1-5 per quality + register)
- [x] Swap-candidate scout (Section 2; stairs with 3 candidates ranked; floor tiles single high-confidence swap; animated props correction batch; prop variety expansion)
- [x] Acquisition flag list (Section 3; EMPTY for VS2a; informational VS2b candidates listed)
- [x] Output doc authored at `agentic_orchestration/research/curated/dungeon-objects-quality-audit-2026-05-18.md`
- [x] Drax v1.17 handoff brief (Section 5; files + preprocessing + test plan + failure-modes + acceptance criteria)
- [x] Visual register check: all swap candidates preserve HYBRID a3 lock
- [x] License verified for every swap candidate (CraftPix-Free-Terms; one credit line covers all)

**Out of scope (honored):**
- Did NOT swap any sprites (drax v1.17 seam)
- Did NOT authorize spend (acquisition flag list empty)
- Did NOT modify drax v1.13 code (audit-only)
- Did NOT touch hybrid_mage retire chain
- Will NOT push tag

**Tag:** `elrond/v1.8-dungeon-objects-quality-audit-1` (local; no push per ADR-006; per dispatch directive)

**Coordination ready:** Drax v1.17 dispatch can fire post-drax-v1.16.2-completion (same-repo serialization per dispatch directive) consuming Section 5 brief.
