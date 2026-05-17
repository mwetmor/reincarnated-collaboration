# ARPG Map Overlay — Research & Engineering Plan

**Authority:** Joint commission. Pattern B — two parallel streams. Matt L3 commissioned 2026-05-17.
**Commission:** `agentic_orchestration/dispatches/2026-05-17-gandalf-drax-arpg-map-overlay-research-commission.md`
**Authorship:** Sections 1-7 — gandalf (genre canon + design principles). Sections 8-14 — drax (engineering plan).
**Scope window:** VS2b territory or later — NOT VS2a-gating. Research now; execute when scheduled.
**Tag (drax stream):** `drax/v1.7-arpg-map-overlay-engineering-plan-1`
**Sibling docs consumed:**
- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — gandalf pixel sizing canon (shipped; live numbers used)
- `canonical/story/mobile-ux-execution-plan-2026-05-17.md` — drax mobile UX plan (shipped; referenced in B3 + B5)
**Reading order:** § 1 Executive summary → §§ 2-7 Genre canon (gandalf) → § 8 Engineering audit → § 9 Two-mode plan → § 10 Mobile constraints → § 11 Data flow → § 12 Phasing → § 13 Deferrals → § 14 Open questions.

---

## § 1 — Executive summary

*[Authored by gandalf — section pending gandalf stream completion. Drax sections 8-14 are complete.]*

---

## § 2 — Two-group hypothesis validation

*[Authored by gandalf — pending.]*

---

## § 3 — Map content + render decisions per platform

*[Authored by gandalf — pending.]*

---

## § 4 — Iconography & symbol vocabulary

*[Authored by gandalf — pending.]*

---

## § 5 — Interaction model

*[Authored by gandalf — pending.]*

---

## § 6 — Mobile-specific design

*[Authored by gandalf — pending.]*

---

## § 7 — Aesthetic guidance

*[Authored by gandalf — pending.]*

---

## § 8 — Engineering reality audit (drax B1)

### § 8.1 — What exists today

**No minimap exists.** A search across all `.ts` files in `reincarnated-demo/src/` for `minimap`, `mini-map`, `worldMap`, `roomLayout`, and `mapOverlay` returns zero results. This is a **full greenfield build**.

This is the starting fact. Nothing to unwire, no legacy rendering to replace, no prior layout debt to account for.

### § 8.2 — Data sources available for a minimap

The dungeon topology is already fully modeled. All data a minimap needs is present in the running game state.

**Room and hallway graph (`src/world/topology.ts`)**

The `Dungeon` interface (topology.ts) holds the complete floor plan:
- `rooms: Room[]` — each Room has `id`, `bounds: Bounds` (`{x, y, width, height}` in world-pixels), `variant: 'small' | 'default' | 'large'`, `aggroState: 'dormant' | 'active' | 'cleared'`, and `doors: Door[]`.
- `hallways: Hallway[]` — each Hallway has `id`, `bounds`, `connects: [string, string]` (room IDs), and `doors: Door[]`.
- `startingRoom: string` — entry room ID.

The VS2a 7-room linear plan (`buildVS2aDungeon()`) populates this at gauntlet start. The total world-space extent for the VS2a plan is approximately 13,392 px wide × 2,160 px tall (7 rooms 720-2160 px wide + 6 hallways 480-768 px wide; max room height 2160 px). The minimap's coordinate system is a scaled-down projection of this bounds box.

**Aggro state (`src/world/aggro.ts`)**

Each Room already carries `aggroState: 'dormant' | 'active' | 'cleared'`. The minimap can read this directly from `_dungeon.rooms[i].aggroState` to color-code rooms (unexplored / active / cleared).

**Player position (`main.ts` — `playerPos: Vec2`)**

`playerPos` is updated every frame by the movement loop (`tickPlayerMove`). It is a module-level mutable. The minimap reads it directly as a world-coordinate point for the player dot.

**Monster positions (`main.ts` — `pack: PackActor[]`)**

Each `PackActor` in the current wave's `pack` array carries `.pos: Vec2` and `.combatant.isAlive`. The minimap reads alive pack members for monster dots. Pack actors not yet spawned (`.spawned === false`) should not be shown (they haven't materialized).

**Gear drop positions (`main.ts` — `gearDropSprites: GearDropSprite[]`)**

`gearDropSprites` is a module-level array updated each frame. Each `GearDropSprite` has a `.container.x / .container.y` (world coordinates) and `.item.tier` (for rarity color-coding). Drops are in world space; minimap can project them the same way as monster dots.

**Potion drop positions (`vfxPools.potionDrops: PotionDrop[]`)**

Potion drops are ground-state collectibles. The minimap can optionally show them (lower priority than gear/monsters/player).

**Camera state (`_cameraX`, `_cameraY`)**

The minimap is a viewport-pinned UI element (in `_layers.ui`) that counter-offsets camera movement via `_syncUiToScreen()`. It does not scroll with the world camera. Player position on the minimap is derived from world-space `playerPos`, not screen-space position.

**What is NOT yet modeled (design layer gaps)**

- NPC positions — no NPC system exists yet in VS2a. Minimap section for NPCs would be empty until a vendor/Spirit Guide NPC is placed in world.
- Treasure chests — no chest system exists yet; out of scope for VS2a.
- Waypoints / altars — no waypoint system exists yet.
- These are Phase MM4 additions when the underlying systems land.

### § 8.3 — Recommended rendering pipeline

**Recommendation: Pixi.js `Graphics`-based procedural render inside a `Container` pinned to `_layers.ui`.**

Not a `RenderTexture`, not a DOM/Canvas hybrid, not SVG.

Rationale:
- The minimap draws simple geometric primitives (rectangles for rooms/hallways, circles for dots, lines for door thresholds). `Graphics` handles all of this natively without an off-screen render pass.
- `RenderTexture` adds complexity and memory overhead (off-screen framebuffer allocation) for content that can be drawn directly. `RenderTexture` is appropriate when you're capturing complex world-geometry (e.g., a full-scene snapshot). Minimap content is abstract — it does NOT sample the world scene, it draws a schematic.
- DOM/Canvas hybrid breaks Pixi's compositing model (z-ordering, camera counter-offset, mobile scaling). Never appropriate here.
- SVG is a poor fit for a game loop; no frame-tick integration, no shared Pixi stage.

The `Graphics.clear()` + redraw pattern is appropriate for per-frame updates of the minimap background (room outlines, which don't change each frame) — but this should be optimized: **static layer cached; dynamic layer redrawn per frame**.

Two sub-containers within the minimap Container:
1. **Static layer** — room/hallway outlines drawn once at gauntlet start; redrawn only on room-state change (aggro transition). `Graphics` object, cleared and redrawn on aggro-state change events.
2. **Dynamic layer** — player dot, monster dots, gear-drop indicators, redrawn every frame.

This two-layer split means the expensive polygon draw (up to 7 rooms + 6 hallways = 13 rectangles) runs only on state changes, not every frame. The per-frame draw is circles only.

### § 8.4 — Performance budget estimate

**Corner minimap (Mode 1) — per-frame cost:**
- Static layer: 0 ms/frame (cached; only redraws on aggro transition; ~4 ms when it does redraw)
- Dynamic layer: clear + redraw N circles where N = 1 (player) + alive pack members (max ~6 for VS2a) + gear drops (0-10). At 7-17 small circles: **~0.1-0.3 ms/frame** on a mid-range desktop GPU (WebGL path, batched by Pixi).
- On mobile (WebGL with tighter budget): same 7-17 circles = **~0.3-0.8 ms/frame**. Well within a 16 ms frame budget (60 fps). Mobile GPU constraint is VRAM fill rate, not draw call count; small circles are negligible.

**Full-screen overlay (Mode 2) — open cost:**
- If static snapshot at open + delta updates: one-time cost ~4-8 ms to build the snapshot; subsequent frames only update moving dots (~0.1-0.3 ms). This is the recommended approach for Mode 2.
- If re-drawn every frame at 70-85% viewport: same as corner minimap but larger Graphics canvas. Still negligible (<1 ms/frame) because it's still rectangles + circles.

**Budget verdict:** Minimap render cost is not a concern for this title's content density. VS2a has at most 7 rooms + 6 hallways + 7 enemies at once. Even a naive full-redraw-every-frame approach would cost < 1 ms at 60 fps. Build it correctly (static/dynamic split), but don't over-engineer.

---

## § 9 — Two-mode rendering plan (drax B2)

### § 9.1 — Mode 1: Corner minimap

**Behavior:** Always-visible, top-right corner of viewport, 8% of canvas width (≈144 px at 1800 px canvas). Updates per frame. Semi-opaque dark background.

**Viewport pinning pattern:**

The demo already uses this exact pattern for every HUD element. `_layers.ui` is counter-offset by `_syncUiToScreen()` each frame so it stays screen-anchored. The minimap Container goes into `_layers.ui` at a fixed screen-space position. This is the same mechanism as `diabloHud`, `combatHud`, `potionHud`, and `desktopHudIcons`.

**Position:** top-right corner. `x = CANVAS_WIDTH - MINIMAP_W - MARGIN`; `y = MARGIN`. Size: approximately 180×180 px on PC (subject to gandalf A2 sizing spec; cite `<sibling-pending: gandalf sections 3-6>` for final numbers).

For the corner minimap, the world-to-minimap coordinate transform is:

```
scale = MINIMAP_W / dungeonWorldWidth
minimapX = (worldX - dungeonBounds.x) * scale + containerLeft
minimapY = (worldY - dungeonBounds.y) * scale + containerTop
```

Where `dungeonWorldWidth` and `dungeonWorldHeight` are the bounding box of all rooms + hallways combined (computed once at dungeon build time). The minimap preserves aspect ratio of the dungeon layout.

**Color coding (placeholder; gandalf A2 overrides):**
- Cleared room: `0x1a2a1a` (dark green tint)
- Active room: `0x2a1a1a` (dark red tint)
- Dormant room: `0x0a0e18` (near-black)
- Hallway: `0x08080c` (darker than rooms)
- Room outline: `0x334455` (muted blue-grey)
- Player dot: `0xffffff` radius 4 px, with a subtle pulse (scale 1.0 → 1.2 → 1.0 over 1s)
- Monster dot: `0xff4444` radius 3 px; elite/boss tier uses larger radius (4-5 px) — per gandalf A3 iconography spec
- Gear drop: `0xffcc44` radius 2 px — rarity color matches `gearDrop.ts` TIER_LABEL_COLORS; legendary gets the same `0xffcc00` glow
- Current room indicator: slightly brighter room-fill for player's current room

**File list:**
- `src/ui/minimap.ts` — new file. Exports `Minimap` class.
- Integration site: `main.ts` — constructed after dungeon build in `startGauntlet()`; updated in the per-frame ticker alongside `diabloHud.update()`.

**`Minimap` class interface (sketch for MM1-MM2):**

```typescript
class Minimap {
  readonly container: Container;
  constructor(parent: Container, dungeon: Dungeon, opts: MinimapOptions);
  update(playerPos: Vec2, pack: PackActor[], gearDrops: GearDropSprite[]): void;
  setRoomAggro(roomId: string, state: AggroState): void; // triggers static layer redraw
  destroy(): void;
}
```

The `update()` call is cheap (dynamic layer only). `setRoomAggro()` triggers the static layer redraw (called from `activateRoom()` / `clearRoom()` dispatch points in `main.ts`).

### § 9.2 — Mode 2: Full-screen centered overlay

**Behavior:** Toggle on `M` key (or button on mobile — see B3). Centered on viewport. 80% viewport coverage. Semi-transparent dark background (60-70% opacity). Gameplay continues underneath (does NOT pause — per ARPG canon; `main.ts` loop keeps running). Closed by pressing `M` again or pressing `Escape`.

**Pixi approach:** A second Container inside `_layers.ui`, rendered above the corner minimap. Default `visible = false`. On M-key toggle: `visible = true`, redraw static layer fresh (full floor plan at larger scale), then per-frame dynamic-layer updates.

**Coordinate transform (same formula as Mode 1 but with larger `MINIMAP_W`):**

At 80% of CANVAS_WIDTH = 1440 px wide, the floor plan renders at much larger scale. The aspect ratio of VS2a's linear dungeon is approximately 6.2:1 (width >> height), so the overlay height would be approximately 1440 / 6.2 = ~232 px. The overlay is horizontally wide but vertically compact — this is appropriate for a horizontal linear dungeon. This will likely look unusual; gandalf A2 may recommend rotating or compressing the layout for the overlay. This is a planning note, not a constraint.

**Overlay layout within the container:**
- Background panel: `drawRect(0, 0, OVERLAY_W, OVERLAY_H)` at 70% black alpha
- Floor plan: same `Graphics`-based room/hallway rectangles at larger scale
- Dynamic layer: same dots as corner minimap but at proportionally larger radius (~1.5× corner)
- Optional: wave label (`Wave 3 / 7 — Elite`), room names (future), legend (future)

**Pause-or-not decision note:** Per ARPG canon (D2 ALT-overlay, D4 full map, PoE overlay), gameplay does NOT pause when the overlay is open. The player navigates while watching the map. This is the recommended default. Gandalf A4 may confirm or modify. The engineering plan accommodates both (toggle `visible` without touching the game loop; if pause is needed, set a `_mapOverlayOpen` flag in `main.ts` that the fight-state logic checks before processing input).

**Same file:** `src/ui/minimap.ts` handles both modes via a `mode: 'corner' | 'overlay'` parameter or a `setMode()` method. The static layer render path is shared; scale factor differs. The dynamic layer `update()` call is identical for both modes.

**M-key binding in `main.ts`:** During `gState === 'fighting'` and `gState === 'door_active'`, check `input.wasPressed('KeyM')` and call `minimap.toggleOverlay()`. This follows the existing pattern for `KeyI` (inventory), `KeyC` (character sheet), and `KeyH` (combat log).

---

## § 10 — Mobile constraints (drax B3)

### § 10.1 — Corner minimap on mobile

The mobile UX execution plan (`canonical/story/mobile-ux-execution-plan-2026-05-17.md`) defines the mobile viewport as 375-428 px wide (logical CSS px at 2-3× device pixel ratio). The corner minimap must not overlap:
- The virtual joystick zone (bottom-left, outer ring ~160 px diameter per `joystick.ts` R_OUTER=80 → 160 px diameter, positioned at bottom-left)
- The touch hotbar (bottom-center/right)
- The touch potion buttons
- The touch icon cluster (top-right strip)

**Top-right corner is occupied on mobile** by `touchIcons.ts` (the inventory/character/log icon cluster). The minimap's corner position must be chosen to avoid this cluster. Based on the existing mobile layout, the icon cluster sits at approximately `x = CANVAS_WIDTH - 80` and `y = 80-200`. The minimap needs to either:
1. Sit above the icon cluster (very tight on mobile)
2. Sit to the left of it (less conventional)
3. Move to top-left corner on mobile (left of the joystick when joystick is not active; joystick is bottom-left only)

**Recommendation (subject to gandalf A5):** On mobile, the corner minimap sits top-right but at reduced size (~100×100 px). The touch icon cluster (`touchIcons.ts`) shifts slightly left or down to make room. This is tracked in the mobile UX execution plan as a layout adjustment.

The minimap tap gesture on mobile opens/closes the full overlay (same as M key on desktop). This is the ARPG mobile canon: tap the minimap corner to expand.

**Mobile size:** ~100×100 px for the corner minimap, per the general principle that mobile shrinks non-touch-target UI by 0.75× from PC values (PC ~180 px → mobile ~135 px, rounded to 100 px for safe-area margin). Exact value deferred to gandalf A2/A5 sizing spec (`<sibling-pending: gandalf sections 3, 5>`).

### § 10.2 — Full-screen overlay on mobile

On mobile, the full-screen overlay IS full-screen (no partial coverage). It fills the safe-area-inset canvas, which is already handled by Pixi's autoDensity + devicePixelRatio setup. The overlay's background blocks the game view completely on mobile (unlike desktop where 70% opacity lets gameplay show through).

**Close gesture:** Tap anywhere outside the floor plan area, or tap the minimap icon again. Not a swipe (swipes are reserved for the joystick + hotbar interactions per the mobile UX plan). A clearly-labeled close button (×) is placed at top-right corner of the overlay for clarity.

**No pinch-zoom in MM2-MM3.** Pinch-zoom on the map (D-Immortal, PoE Mobile) is Phase MM6 polish. The overlay shows the full floor plan at fixed scale in MVP.

### § 10.3 — Render performance on mobile

Per § 8.4: minimap draw cost is ~0.3-0.8 ms/frame on mobile at VS2a content density. This is acceptable. The primary mobile GPU constraint is fill rate (large transparent overlays), not draw call count. The full-screen overlay's dark background (a single filled rect) is cheap at mobile fill rates. No mobile-specific rendering optimization is required in MM1-MM3.

### § 10.4 — Integration with mobile UX execution plan

The mobile UX execution plan (Phase MX3 — layout zones) must include the minimap corner position in its layout-zone definition. The minimap is a new HUD element that the layout-zone system must account for. When MX3 fires, `minimap.ts` integration is a sub-item.

---

## § 11 — Data flow architecture (drax B4)

### § 11.1 — Map data source

The minimap's data feed is entirely internal to `main.ts` runtime state. No new engine schema fields are needed. No new loader calls. The data is already present:

| Data | Source in main.ts | Update frequency | Minimap use |
|---|---|---|---|
| Room/hallway layout | `_dungeon: Dungeon` (built once in `startGauntlet`) | Static per gauntlet | Static layer render |
| Room aggro state | `room.aggroState` on `_dungeon.rooms[i]` | On aggro transition | Static layer re-render |
| Player world position | `playerPos: Vec2` | Per frame | Player dot |
| Monster world positions | `pack[i].pos: Vec2` (alive + spawned only) | Per frame | Monster dots |
| Gear drop positions | `gearDropSprites[i].container.{x,y}` | Per frame | Drop indicators |
| Monster tier | `pack[i].spec.tier` | Static per wave | Dot color/size |
| Gear tier | `gearDropSprites[i].item.tier` | Static per drop | Drop color |
| Current wave number | `gauntlet.waveNumber` | Per wave advance | Active room highlighting |

### § 11.2 — Update frequency model

**Static layer** (room/hallway outlines, door markers, room fill colors):
- Built once at `startGauntlet()` when `_dungeon` is first constructed.
- Rebuilt whenever `setRoomAggro()` is called (at most 7 times per gauntlet — once per room-clear event). Not per frame.

**Dynamic layer** (player dot, monster dots, drop indicators):
- Redrawn every frame in the game-loop ticker, alongside `diabloHud.update()` and `updateHpBar()`.
- `minimap.update(playerPos, pack, gearDropSprites)` is the single per-frame call.
- When the full-screen overlay is closed (`visible === false`), `update()` skips the dynamic redraw (no-op if not visible). This avoids wasting GPU time when the overlay isn't shown.
- The corner minimap always updates (it's always visible during combat).

### § 11.3 — Memory model

**Whole-dungeon cache:** The VS2a dungeon has 7 rooms + 6 hallways. The static layer Graphics for the full floor plan is approximately 200 triangles (rect decomposition by Pixi). Memory: ~8-16 KB in Pixi's geometry buffer. Negligible.

**No partial-cache needed:** Multi-floor dungeons (where only the current floor is cached) are a Phase 3 concern. VS2a is single-floor linear; cache the whole thing.

**GC discipline:** The minimap Container and its Graphics children are created once per gauntlet start and destroyed in the existing `clearVfx()` / gauntlet-teardown path. No per-frame allocations. `Graphics.clear()` reuses the same Graphics object; it does not allocate.

### § 11.4 — Relationship to mobile execution plan

The mobile UX execution plan defines layout zones for mobile. The minimap is an additional HUD element in that zone system. The data flow described here is platform-invariant — the same `update()` call, same data sources, same rendering path. What changes on mobile is: (a) container position (top-right, smaller), (b) tap gesture for overlay toggle, (c) overlay is full-screen modal. The data pipeline does not change.

### § 11.5 — Integration with future NPC + chest + waypoint systems

When the engine eventually emits NPC positions, chest positions, or waypoint positions as part of the floor plan data (these do not exist yet), they are added as additional data sources in the same pattern:
- NPC: a separate array of `{ id, pos, kind }` passed to `minimap.update()`.
- Chests: same pattern.
- Waypoints: likely static (positions set at dungeon build time); added to static layer, not dynamic layer.

No architectural change is needed to add these. The `Minimap` class interface is designed to accept additional per-frame arrays.

---

## § 12 — Phased drax-dispatch plan (drax B5)

Each phase is a standalone dispatch (~0.5-2 days). Phases are sequential: each phase's smoke test gates the next.

### Phase MM1 — Data layer extraction

**Scope:** Extract and test the dungeon-to-minimap coordinate transform in isolation. No visible minimap; unit-testable via console output.

**Goal:** Prove the math. Given `_dungeon` from `buildVS2aDungeon()`, compute the bounding box of the full floor plan, verify the scale factor, verify that all room/hallway bounds project into the minimap coordinate space without clipping.

**Files:**
- `src/ui/minimap.ts` — new file. Contains:
  - `computeDungeonBounds(dungeon: Dungeon): Bounds` — union of all room + hallway bounds
  - `worldToMinimap(worldX, worldY, dungeonBounds, minimapW, minimapH): {x, y}` — coordinate transform
  - `MinimapOptions` interface (position, size, opacity)
  - `Minimap` class (constructor, `update()` stub, `setRoomAggro()` stub, `destroy()`)
- No changes to `main.ts` yet (integration is Phase MM2).

**Smoke test:** `npm run build` succeeds. Console-log the projected position of `playerPos` (player spawn for room_0) through `worldToMinimap()` — verify it appears at the expected minimap-space location (left-center of minimap for VS2a's room_0 spawn position).

**Dependencies:** None. Can start immediately. Does not require gandalf A2/A3 sizing spec — uses placeholder values.

**Line-count estimate:** ~120 lines for `minimap.ts` at this phase.

---

### Phase MM2 — Corner minimap MVP

**Scope:** Visible corner minimap with static room/hallway outlines + player dot + monster dots. No styling polish.

**Goal:** "I can glance top-right and see where I am, where the rooms are, and where monsters are."

**Files:**
- `src/ui/minimap.ts` — extend MM1 foundation:
  - `_buildStaticLayer()` — draws room/hallway rectangles + door threshold lines at minimap scale; room fill color by aggroState
  - `_updateDynamicLayer()` — clears + redraws player dot (white) + monster dots (red, size by tier)
  - `update()` — calls `_updateDynamicLayer()`
  - `setRoomAggro()` — calls `_buildStaticLayer()` on state change
- `main.ts` — integration:
  - After `_dungeon = buildVS2aDungeon(...)` in `startGauntlet()`: `_minimap = new Minimap(_layers.ui, _dungeon, cornerMinimapOpts)`
  - In per-frame ticker (alongside `diabloHud?.update(player)`): `_minimap?.update(playerPos, pack, gearDropSprites)`
  - On aggro transitions (`activateRoom()` / `clearRoom()` call sites): `_minimap?.setRoomAggro(room.id, room.aggroState)`
  - On gauntlet teardown: `_minimap?.destroy(); _minimap = null`

**Smoke test:** Demo launches, renders one frame without console errors. Corner minimap is visible top-right. Player white dot moves with WASD. Red dots appear for monsters and move with them. Aggro transitions change room color. `npm run build` passes.

**Dependencies:** MM1 complete. No gandalf spec needed for MVP — placeholder sizing.

**Line-count estimate:** MM1 (~120) + ~200 new lines in `minimap.ts` + ~30 integration lines in `main.ts` = ~350 total lines added.

---

### Phase MM3 — Full-screen overlay MVP

**Scope:** M-key toggle for full-screen overlay. Same data, larger scale. Semi-transparent background.

**Goal:** Press M, see the whole floor plan at readable size. Press M again (or Escape), return to corner minimap only.

**Files:**
- `src/ui/minimap.ts` — extend MM2:
  - `toggleOverlay()` — toggles `_overlayVisible`; on open: rebuilds static layer at overlay scale; on close: rebuilds at corner scale
  - `_overlayVisible: boolean` — controls which Container is shown
  - Two Container children: `_cornerContainer` and `_overlayContainer`; `_buildStaticLayer()` targets the currently-active container
  - `_overlayContainer` positioned at center: `x = (CANVAS_WIDTH - OVERLAY_W) / 2`; `y = (CANVAS_HEIGHT - OVERLAY_H) / 2`
  - Background panel added to `_overlayContainer` (dark rect, 70% alpha)
- `main.ts`:
  - During `gState === 'fighting'` and `gState === 'door_active'`: `if (input.wasPressed('KeyM')) _minimap?.toggleOverlay()`
  - `_minimap?.update()` updates both layers regardless of overlay state (corner always current; overlay only when open)

**Smoke test:** Press M during combat — overlay appears centered. Player dot and monster dots visible at overlay scale. Press M again — overlay closes. `npm run build` passes.

**Dependencies:** MM2 complete.

**Line-count estimate:** MM2 total (~350) + ~150 new lines in `minimap.ts` (overlay mode) + ~15 integration lines in `main.ts` = ~515 total lines.

---

### Phase MM4 — Iconography pass

**Scope:** Apply gandalf A3 iconography spec. Gear-drop indicators (rarity-colored), proper monster tier dot sizing, boss indicator, door/exit markers on minimap, optional wave label in overlay.

**Goal:** Map is informative enough to navigate by, not just locating-by.

**Files:**
- `src/ui/minimap.ts` — extend MM3:
  - `_drawMonsterDot()` — per-tier radius + color per gandalf A3 spec (placeholder until spec lands; replace `<sibling-pending: gandalf A3>` when available)
  - `_drawGearDrop()` — rarity-colored small diamond/square; matches `TIER_LABEL_COLORS` from `gearDrop.ts`
  - `_drawDoorMarker()` — small gap or tick mark on room-outline edge at door position; uses `door.position` from topology
  - `_drawExitMarker()` — brighter color for the active exit door (`_activeDoorId` from `main.ts`)
  - Wave label in overlay: `Text` child of `_overlayContainer` showing `Wave N / 7 — <tierLabel>`

**Smoke test:** Gear drops appear on minimap at correct positions with rarity colors. Boss room has distinct marker. Exit door is highlighted. `npm run build` passes.

**Dependencies:** MM3 complete + gandalf A3 iconography spec available (`<sibling-pending: gandalf section 4>`). Can use placeholders and iterate.

**Line-count estimate:** ~515 + ~120 new lines in `minimap.ts` = ~635 total lines.

---

### Phase MM5 — Mobile adaptation

**Scope:** Mobile minimap sizing + tap-to-toggle gesture + full-screen modal on mobile. Integrates with mobile UX execution plan Phase MX3 (layout zones).

**Goal:** The minimap works correctly on a 375 px wide mobile viewport. Joystick and touch hotbar are not occluded.

**Files:**
- `src/ui/minimap.ts` — extend MM4:
  - `MinimapOptions.mobile` variant: smaller corner size (~100×100 px), adjusted position (top-right, shifted left to avoid `touchIcons.ts` cluster)
  - Mobile overlay: `_overlayContainer` covers full canvas (no partial-coverage); close button (×) at top-right
  - Tap gesture: `_cornerContainer.interactive = true`; `on('pointerdown', toggleOverlay)` for mobile; this is consistent with how `touchIcons.ts` handles tap events
- `main.ts`:
  - `MinimapOptions` conditional: `Mobile.isActive ? mobileMinimapOpts : desktopMinimapOpts`
  - No touch-gesture conflict: tap on minimap corner is distinct from joystick bottom-left and hotbar bottom-right; safe zones verified per mobile UX layout

**Smoke test:** On 375 px viewport (browser devtools mobile emulation), minimap visible top-right, not occluded by joystick or hotbar. Tap minimap opens full overlay. Tap close button closes. `npm run build` passes.

**Dependencies:** MM4 complete + mobile UX execution plan Phase MX3 layout zones complete (`canonical/story/mobile-ux-execution-plan-2026-05-17.md` Phase MX3).

**Line-count estimate:** ~635 + ~80 new lines in `minimap.ts` (mobile branch) + ~20 integration lines in `main.ts` = ~735 total lines.

---

### Phase MM6 — Polish

**Scope:** Fog-of-war reveal animation, zoom controls on overlay, opacity setting, player-dot pulse animation, smooth aggro-state transitions.

**Goal:** Map feels alive and polished, not functional-but-static.

**Files:**
- `src/ui/minimap.ts` — extend MM5:
  - Fog reveal: rooms start at low alpha (dormant = 10% opacity), fade to full opacity when aggro activates. `setRoomAggro()` triggers a tween on the room's Graphics alpha over 0.3s.
  - Player dot pulse: scale oscillates 1.0 → 1.2 → 1.0 over 1s. Simple sin-based tick in `update()`.
  - Overlay zoom (MM6+): `+` / `-` keys or pinch gesture adjust scale factor within [0.5×, 2.0×] range; scroll recenters on player.
  - Opacity setting: `MinimapOptions.alpha` applied to `_cornerContainer.alpha`; user-configurable in a future settings panel (not in MM6 scope itself — surfaced as observation).
  - Annotation (if scoped — see B6): long-press on overlay places a small marker; array of `{x, y, label}` persists until cleared.

**Smoke test:** Player dot pulses. Entering a dormant room triggers a room reveal fade. Overlay zoom in/out works with + / - keys. `npm run build` passes.

**Dependencies:** MM5 complete + gandalf A4/A5/A6 spec available.

**Line-count estimate:** ~735 + ~150 new lines (fog/pulse/zoom) = ~885 total lines in `minimap.ts`.

---

### Phase summary table

| Phase | Goal | New files | Main.ts changes | Smoke test | Dependencies |
|---|---|---|---|---|---|
| MM1 | Data layer + transform math | `src/ui/minimap.ts` (skeleton) | None | Build passes; transform verified in console | None |
| MM2 | Corner minimap MVP | extend MM1 | ~30 lines | Visible minimap; player/monster dots | MM1 |
| MM3 | Full-overlay toggle | extend MM2 | ~15 lines | M-key toggle works | MM2 |
| MM4 | Iconography pass | extend MM3 | None | Gear drops + tiers + exit marker | MM3 + gandalf A3 |
| MM5 | Mobile adaptation | extend MM4 | ~20 lines | Works on 375 px viewport | MM4 + mobile UX MX3 |
| MM6 | Polish (fog, pulse, zoom) | extend MM5 | None | Fog reveal; dot pulse; zoom | MM5 + gandalf A4/A5/A6 |

---

## § 13 — Out-of-scope deferrals (drax B6)

**Multi-floor map (D2 act-overview style):**
VS2a is a single-floor linear dungeon. Multi-floor with a floor-select UI (D2-style Act overview, PoE-style area map) is a Phase-3 feature if the dungeon topology ever gains a floor axis. The `Dungeon` interface in `topology.ts` would need a `floors: Floor[]` wrapper; the minimap would need a floor-selection control. Explicitly out of scope. When multi-floor lands in topology, the minimap refactor is a separate dispatch.

**Map sharing / streaming:**
No mechanic planned. Solo gameplay only (`project_design_intent.md` confirms: solo gameplay only). Out of scope permanently unless Matt explicitly revisits.

**Procedural room-reveal animations beyond fog-clear:**
Animated room-shape reveals (e.g., the walls of a room "drawing themselves" on the minimap as the player explores) are a Phase-3 polish item. The fog-opacity fade in MM6 is the MVP reveal. Full procedural drawing is an overengineering call at VS2a/VS2b density.

**Click-to-move via minimap:**
D2 allowed clicking the automap to move to a position. This is an interaction-model decision for gandalf A4. Engineering note: if approved, `click-on-overlay → map-space position → world-space position → set as lmbMoveTarget` is approximately 5 lines in `main.ts`. Very cheap if the design calls for it. Deferred to MM6 polish phase.

**Player-placed annotations:**
Last Epoch supports player map annotations. Scoped as a MM6 stretch feature. If included: a `annotations: { worldX, worldY, label?: string }[]` array in `Minimap` class, persisted to `localStorage` (key: `reincarnated_map_annotations_<dungeonId>`). The dungeon ID changes each gauntlet start, so annotations reset each run — appropriate for a roguelike-adjacent game.

**Minimap in non-combat screens:**
The minimap is a combat HUD element. It does not appear during `season_menu` or `selecting` screens. The dungeon doesn't exist yet in those states (`_dungeon === null`), so the `null` guard in `main.ts` handles this automatically.

**Radar-ping / off-screen monster indicators:**
Some ARPGs pulse the minimap edge when an off-screen threat activates. This is a Phase-3 polish item. Not in MM1-MM6 scope.

---

## § 14 — Open questions for Matt

*[This section compiled by whichever stream ships last, per dispatch protocol. Gandalf sections 1-7 pending. Questions below are drax-stream engineering questions; gandalf will add design questions from A1-A6 when their stream completes.]*

### Engineering open questions (drax)

**OQ-1 — Default mode per platform:** Should the corner minimap be visible by default on first launch, or opt-in? For VS2b, default-on is the recommendation (per ARPG genre canon: minimap is always visible), but if Matt wants it gated behind a tutorial moment ("you've discovered the map"), it requires a `_minimapUnlocked` flag in the game state. Engineering-trivial either way; needs a design call.

**OQ-2 — Pause-on-overlay (gameplay stops when full-screen map is open?):** Per ARPG canon, gameplay continues. But if Matt prefers pause (for mobile usability where two-hand play is harder), the flag `_mapOverlayOpen` is checked in the fight-state input-processing block. Decision affects the interaction feel significantly. Recommend no-pause (genre canon), but surfacing for explicit approval.

**OQ-3 — Fog of war vs full-reveal:** The engineering plan implements aggro-state-based room coloring (dormant = dark fill, active/cleared = brighter fill), which effectively IS fog of war (you can't see the room shape until you've been near it because all rooms are pre-drawn but dim). True fog = rooms are hidden until the player enters. Which model: tint-fog (always visible, but dark) or hide-fog (rooms not drawn until visited)? Tint-fog is simpler and matches D2's feel; hide-fog matches PoE's feel. Gandalf A2 covers this; surfacing here for cross-check.

**OQ-4 — M key availability:** M is not currently bound in `main.ts` during combat. Confirming it's available for minimap toggle. (I is inventory, C is character sheet, H is combat log, Escape is system, Space is dodge.) M is free.

**OQ-5 — Minimap in the between-wave overlay:** During `gState === 'pack_dying'` and `gState === 'door_active'`, the minimap is relevant (player is walking to the exit; the map shows where the door is). The current plan keeps the minimap active in these states. The between-wave overlay (`createBetweenWaveOverlay`) covers the center of the screen; the corner minimap in the top-right is not occluded. Confirming this is correct behavior.

**OQ-6 — Minimap assets needed (OBSERVATION for Phase-2 acquisitions queue):** The engineering plan uses Pixi `Graphics` primitives exclusively — no external sprite assets needed for MM1-MM5. MM4+ iconography uses the same `Graphics` shapes as the HUD (consistent with existing glyph-drawing in `combatHud.ts`). If Matt later wants pixel-art minimap icons (styled map markers, treasure-chest symbols, etc.) instead of geometric primitives, those would be new assets. Surfacing as an OBSERVATION: no blocker, but if the art direction calls for it, add to the Phase-2 acquisitions queue alongside the tileset work.

---

*Drax stream complete. Sections 8-14 authored. Gandalf sections 1-7 pending. Tag `drax/v1.7-arpg-map-overlay-engineering-plan-1` applied at commit.*
