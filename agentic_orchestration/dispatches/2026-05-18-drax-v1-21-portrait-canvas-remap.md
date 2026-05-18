# 2026-05-18 — drax-demo — v1.21 portrait canvas remap (Q-NEW-1 deferred scope)

**Authority:** Matt L3 verbatim 2026-05-18 — "fire v1.21" (per Q-NEW-1 lock: portrait canvas DEFER → own dispatch).
**Type:** Pattern B large multi-file refactor; ~4-8 hours.
**Predecessor:** drax v1.20 multi-fix complete (8 blocks; touch zones + orientation invert + holy controller + door icon + tileset + pimen warnings + wave-8 soft-cap + potion DoE). Tag `drax/v1.20-mobile-touch-zones-plus-holy-controller-plus-door-icon-plus-first-tileset-1` shipped.
**Concurrent flight:** drax v1.20.1 hotfix in progress (odd door-side icon removal — Pattern A ~15-30 min; lane = door/wall rendering; different files from v1.21 mobile HUD work; conflict risk LOW but coordinate via git pull at start).
**Status:** 🟢 **ACTIVE — fire immediately. Drax idle (post-v1.20.1 handoff acceptable).**

---

## Why this matters

Q-NEW-1 from drax v1.19.5 mobile-readiness audit: current canvas is 1800×944 landscape internally; gandalf v1.7 § 3.5 portrait-primary canon locks 944×1800 as the canonical mobile target. v1.20 Block 6 shipped the orientation overlay invert ("rotate to portrait" on landscape) but the canvas is still landscape internally — phone users in portrait see the landscape canvas letterboxed with large top + bottom black bars (~aspect 1.91 vs portrait phone ~0.46). Playable but visually a stopgap. v1.21 closes that loop.

Per gandalf v1.12 § 12 DoE canonical reference: portrait is the validated reference experience; canvas resolution swap + HUD remap completes the mobile-feel-target alignment.

---

## Required reading (THIS IS LOAD-BEARING)

1. **Portrait canvas canonical spec** — `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 3.5 (gandalf v1.7 — portrait-primary lock with full HUD position table)
2. **DoE mobile-feel reference** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 12 (gandalf v1.12 — DoE-as-canonical-reference; departure rule applies)
3. **Mobile UX execution plan** — `canonical/story/mobile-ux-execution-plan-2026-05-17.md` (Phase M5/M6 portrait HUD remap scope description)
4. **Your v1.19.5 audit § 4** — `agentic_orchestration/research/curated/mobile-readiness-audit-2026-05-18.md` § 4 item 4 (the v1.21 scope flag)
5. **`src/rendering/stage.ts`** — current 1800×944 canvas init
6. **`src/main.ts`** — HUD element instantiation + positioning (joystick, hotbar, potions, globes, log, character portrait, mini-map placeholder)
7. **`src/mobile/joystick.ts`** — JOY_CX, JOY_CY constants (currently landscape-positioned)
8. **`src/mobile/touchHotbar.ts`** — skill arc positions
9. **`src/mobile/touchPotions.ts`** — potion positions
10. **`src/mobile/touchIcons.ts`** — top-row icon positions

---

## 🎯 Canonical portrait spec (per gandalf v1.7 § 3.5)

**Internal canvas:** **944 × 1800** (transposed from current landscape 1800 × 944)

**HUD positions (canvas-space, canvas = 944 × 1800):**

| Element | Portrait position | Notes |
|---|---|---|
| Rift name banner + minimap module | top-left (x=20-300, y=20-200) | Minimap diameter ~180 px portrait |
| HP bar | attached to minimap module top-left (y=100-130 horizontal bar) | DoE pattern — top-attached rather than bottom-globe |
| Mana / resource bar | adjacent to HP bar, slightly below | Same minimap-attached pattern |
| Combat log / drop-down | top-right (mirror landscape "LOG ▾" position) | Y=20-60; x=~740-924 |
| Character portrait + red-dot loot affordance | bottom-left (x=20-140, y=1500-1620) | 120 px diameter circular |
| Joystick | bottom-left thumb-reach (suggested x=180, y=1620; below portrait) | Within ~y=1500-1800 thumb zone |
| Skill arc / hotbar (6 slots) | bottom-right thumb-reach (radial arc anchored ~x=750, y=1600) | DoE-pattern radial; preserve 6-button shape |
| Health potion | bottom-right above skill arc (x=~830, y=1350) | Cooldown-only post-v1.20 |
| Mana potion | bottom-right below health potion (x=~830, y=1450) | Same |
| Target-cycle button | bottom-center between joystick + skill arc (x=~472, y=1700) | Touch-zone hitR(88) per v1.20 |
| Objective counter + XP bar | bottom edge (y=1750-1800; full width 0-944) | Bar height 8-12 px; font ~14 px |
| Dash cooldown indicator | adjacent to potions (right edge, y=~1250) | Existing PotionHud-adjacent pattern |

**Camera zoom invariant:** player occupies ~10-12% of viewport-height (slightly looser zoom than landscape). World-area-visible shifts from ~28m × ~15m landscape → ~15m × ~28m portrait. Density-per-meter unchanged (PIXELS_PER_METER = 48 lock holds).

**Thumb-reach zones:** bottom 35% of viewport (canvas y=1170-1800) is the action surface. All high-frequency interactives live here.

---

## Scope — six implementation blocks

### Block 1 — Canvas resolution swap (foundational)

Change `src/rendering/stage.ts` canvas init from 1800×944 to **conditional 944×1800 on mobile / 1800×944 on desktop** OR **runtime orientation-aware** (preferred):

```typescript
const isMobilePortrait = Mobile.isActive && /* orientation === portrait */;
const CANVAS_W = isMobilePortrait ? 944 : 1800;
const CANVAS_H = isMobilePortrait ? 1800 : 944;
```

If runtime-aware is too invasive, fall back to mobile-only fixed portrait (944×1800 if Mobile.isActive else landscape). Document the choice in completion record.

CSS scaling: same `object-fit: contain` + `max-width: 100vw, max-height: 100dvh` pattern already in mobile.ts; should adapt automatically. Verify in DevTools.

### Block 2 — HUD position remap (Mobile.isActive branches at every position constant)

For each mobile-specific HUD element, add an `if (Mobile.isActive)` branch in the position constants OR derive positions from canvas dimensions so they automatically transpose:

```typescript
// Example pattern in joystick.ts
const JOY_CX = Mobile.isActive ? 180 : 180;  // x stays
const JOY_CY = Mobile.isActive ? 1620 : 700;  // portrait y=1620; landscape y=700
```

Use the gandalf v1.7 § 3.5 table above as the truth-source for portrait positions. Desktop landscape positions stay unchanged (no regression on PC playtest).

**Files to touch:**
- `src/main.ts` — globes + top icons + log + portrait + objective counter positions
- `src/mobile/joystick.ts` — JOY_CX, JOY_CY
- `src/mobile/touchHotbar.ts` — arc center + radius
- `src/mobile/touchPotions.ts` — POT_X, POT_Y for health + mana
- `src/mobile/touchIcons.ts` — ICON_X, ICON_Y row positioning
- `src/mobile/touchTargetBtn.ts` — TGT_X, TGT_Y
- `src/ui/dashCooldownHud.ts` — DASH_X, DASH_Y (existing landscape position)
- `src/ui/combatLog.ts` (or wherever the log button lives) — log button anchor
- Character portrait + red-dot affordance (locate via grep; may live in main.ts)

### Block 3 — Camera zoom adjustment (portrait-aware)

If a per-mode camera scale exists, add portrait branch (~10-12% player-of-viewport-height). If single global zoom, this can wait until Block 1 reveals whether the existing zoom looks acceptable post-canvas-swap (the player will auto-scale relative to the new canvas dimensions).

### Block 4 — DrawerShell portrait awareness

`src/ui/drawerShell.ts` (v1.19) — verify drawer geometry still works at 944 wide. Current: 56% canvas height = 529 px landscape; in portrait at 1800 tall, 56% = 1008 px (probably too much). Cap at ~700 px or recompute portrait drawer height (gandalf canon suggests "~50% screen-height drawer"). Verify swipe-down dismiss + tap-outside dismiss still feel right at portrait dimensions.

### Block 5 — Orientation overlay update (v1.20 Block 6 follow-on)

v1.20 inverted to show "rotate to portrait" on landscape. Now that portrait HUD layout is implemented, **the overlay can shift from stopgap to true gate**: also forbid landscape orientation in PWA standalone mode. Or simply leave v1.20's overlay as-is since it already prompts portrait correctly.

If you want a cleaner UX: keep the overlay (still gates landscape); add a "Continue in landscape (less optimized)" escape link for desktop browsers that get forced into mobile mode. Optional polish.

### Block 6 — Manual smoke verification

DevTools mobile emulation (iPhone 12 Pro / Pixel 7):
- Canvas renders at 944×1800 internally; CSS scales correctly to phone viewport
- All HUD elements visible + reachable in portrait thumb-zones
- Joystick movement works at new y=1620 position
- Skill arc fires correctly at new radial center
- Potions tap-fire at new x=830 position
- DrawerShell slides up cleanly from bottom; doesn't exceed thumb-reach
- Game playable end-to-end on portrait emulation

Desktop landscape (1920×1080): nothing regresses; landscape HUD unchanged.

`npm run build` clean.

---

## Acceptance criteria

- [ ] Block 1: canvas swap to 944×1800 on mobile (or runtime orientation-aware); CSS scaling verified
- [ ] Block 2: 8+ HUD element positions remapped per gandalf v1.7 § 3.5 table; desktop landscape unchanged
- [ ] Block 3: camera zoom acceptable at portrait (player ~10-12% viewport-height); document any adjustment needed
- [ ] Block 4: DrawerShell geometry recomputed for portrait (height cap ~700 px or per design preference)
- [ ] Block 5: orientation overlay reviewed against new portrait state (likely no change required from v1.20)
- [ ] Block 6: DevTools portrait emulation passes full smoke; desktop landscape regression-free
- [ ] `npm run build` clean
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.21-portrait-canvas-remap-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT redesign HUD layout beyond the gandalf v1.7 § 3.5 table positions (canon-locked; no creative drift)
- ❌ DO NOT change visual button radii (BTN_R/ICON_R/POT_R) — Block 1 of v1.20 already canonicalized those; only positions change in v1.21
- ❌ DO NOT touch hitR() helper or HIT_R values — v1.20 Block 1 already canonicalized those
- ❌ DO NOT touch wave 8 tier soft-cap (v1.20 Block 7) or potion DoE (v1.20 Block 8) — both locked
- ❌ DO NOT touch the procedural-vs-CraftPix floor swap (v1.20 Block 4 ACTIVE_FLOOR_VENDOR constant) — Matt confirmed procedural is the keeper
- ❌ DO NOT change PIXELS_PER_METER = 48 — sim-load-bearing constant (per movement-speed-baseline canon)
- ❌ DO NOT change camera zoom on DESKTOP — only mobile portrait branches
- ❌ DO NOT push tag (ADR-006)
- ❌ DO NOT pre-empt drax v1.20.1 hotfix (odd door icon) — Pattern A in flight; pull main before committing v1.21 to integrate v1.20.1

---

## Coordination

- **Predecessor:** drax v1.20 multi-fix complete
- **Concurrent:** drax v1.20.1 odd-door-icon hotfix in flight (~15-30 min remaining at v1.21 spawn time). Different file lane (door/wall rendering vs mobile HUD positions). Conflict risk LOW. Coordinate via `git pull` at start of v1.21 + before final commit.
- **Parallel-safe with:** rocket regen 002016 (different repo; PID 17673 still detached)
- **Triggers downstream:**
  - Mobile playtest unblock (Matt can now test on real phone post-Vercel fix)
  - DoE-canon alignment complete (gandalf v1.12 § 12 reference fully honored)
  - Vercel deployment readiness (when vendor-asset CDN strategy lands, demo can deploy with portrait-correct UI)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## First-action protocol

1. `git pull` in reincarnated-demo to ensure latest main (will include v1.20.1 commit if it landed first)
2. Read gandalf v1.7 § 3.5 in full (canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md lines 323-380)
3. Read DoE canon § 12 in full (canonical/story/mobile-feel-target-doe-2026-05-17.md)
4. Begin Block 1 (canvas swap) — verify CSS scaling end-to-end before any HUD-position work

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 "fire v1.21." ~4-8h. Append completion record with: canvas swap method (mobile-only fixed vs runtime orientation-aware), all HUD positions before/after, camera zoom decision, DrawerShell geometry decision, any portrait UX surprises discovered, smoke evidence.*

---

## Completion record

**Completed:** 2026-05-18
**Commit:** `7e5b93b` — drax/v1.21: portrait canvas remap 944×1800 + HUD remap per gandalf v1.7 § 3.5
**Tag:** `drax/v1.21-portrait-canvas-remap-1` (local only, per ADR-006)

---

### Block 1: Canvas swap

**Method chosen:** Mobile-only fixed portrait (944×1800 when `Mobile.isActive`; 1800×944 desktop landscape). Runtime orientation-aware was not implemented — it would require re-running all dungeon geometry calculations on orientation change, which is a separate scope.

**Mechanism:** `CANVAS_WIDTH`/`CANVAS_HEIGHT` in `src/rendering/stage.ts` changed from `const` to `let`. New exported function `initCanvasDimensions(isMobilePortrait: boolean)` mutates them. In `src/main.ts`, `Mobile.init()` was moved before `createApp()` in the bootstrap; `initCanvasDimensions(Mobile.isActive)` is then called, setting 944×1800 before Pixi allocates the WebGL surface. ES module live-binding semantics ensure all importers see the updated values at runtime.

**Critical architectural constraint resolved:** `Mobile.isActive` is `false` at module-import time (before any runtime code runs). All position constants that branched on `Mobile.isActive` were moved from module-level `const` into class constructors (which run after `Mobile.init()` has set `isActive = true`). This affected joystick.ts, touchHotbar.ts, touchPotions.ts, touchIcons.ts, touchTargetBtn.ts, and drawerShell.ts.

**CSS scaling:** No change needed. The existing `object-fit: contain` + `max-width: 100vw, max-height: 100dvh` in `mobile.ts` handles portrait canvas correctly — the browser letterboxes automatically. `clientToCanvas` in `mobile.ts` updated from hardcoded `1800`/`944` to `canvas.width / dpr` and `canvas.height / dpr` for orientation-invariant pointer coordinate mapping.

---

### Block 2: HUD positions before/after

All positions are canvas-space (canvas = 944×1800 portrait; 1800×944 landscape).

| Element | Landscape (before) | Portrait (after) | Notes |
|---|---|---|---|
| Joystick center | x=180, y=700 | x=180, y=1620 | Bottom-left thumb zone |
| Skill arc slot 0 (primary) | x=1690, y=752 | x=884, y=1690 | Bottom-right |
| Skill arc slot 1 | x=1660, y=670 | x=858, y=1618 | Arc |
| Skill arc slot 2 | x=1618, y=598 | x=816, y=1552 | Arc |
| Skill arc slot 3 | x=1565, y=538 | x=760, y=1498 | Arc |
| Skill arc slot 4 | x=1502, y=492 | x=694, y=1462 | Arc |
| Skill arc slot 5 | x=1432, y=462 | x=622, y=1442 | Upper-left arc anchor |
| Health potion | x=1498, y=668 | x=830, y=1350 | Right edge, above arc |
| Mana potion | x=1498, y=742 | x=830, y=1450 | Right edge, above arc |
| Combat log icon | x=1740, y=60 | x=884, y=60 | Top-right corner |
| Inventory icon | x=60, y=60 | x=60, y=60 | Unchanged (top-left) |
| Char icon | x=120, y=60 | x=120, y=60 | Unchanged (top-left) |
| Target-cycle btn | x=1408, y=705 | x=472, y=1700 | Bottom-center |

Desktop landscape positions are unchanged in all files. All mobile branches gate on `Mobile.isActive` evaluated at construction time.

---

### Block 3: Camera zoom decision

**No zoom added.** The camera system is pan-only (no `app.stage.scale` mechanism exists). Adding portrait zoom would require: (1) a new stage scale constant, (2) recalculating all dungeon room bounds and corridor bounds in `topology.ts` to account for scale, (3) camera clamping math update in `roomRenderer.ts`. This is follow-on v1.22 scope.

**Current portrait zoom situation:** player sprite radius = 72px canvas. Portrait canvas 944×1800, CSS-scaled to ~390×743px on phone (width-constrained). Player = 72 * (390/944) = ~29.7px CSS = ~4% of 743px screen height. Spec target is 10-12%. Gap = 2.5-3× zoom needed. **TODO(drax):** portrait camera zoom — v1.22 Block 3.

---

### Block 4: DrawerShell portrait geometry

Prior `DRAWER_H = Math.round(CANVAS_HEIGHT * 0.56) = 529` would become 1008 in portrait (56% of 1800) — too large, exceeds thumb reach zone.

**Solution:** Removed module-level `DRAWER_H` with `Mobile.isActive` (wrong at import time). Added exported getter functions `getDrawerH()` and `getDrawerW()` that read `Mobile.isActive` and `CANVAS_HEIGHT`/`CANVAS_WIDTH` at call time (inside constructors). `DrawerShell` constructor computes `this.drawerH = getDrawerH()` — portrait: `min(700, 1008) = 700px` (38.9% of canvas); landscape: 529px (unchanged).

`DrawerShell` exposes `readonly drawerH: number` and `readonly drawerW: number`. `main.ts` passes `shell.drawerW` / `shell.drawerH` to `InventoryPanel` and `CharacterSheet` as optional constructor params so panel content is sized correctly for portrait drawer.

Legacy exported constants `DRAWER_H = 529` (landscape) and `DRAWER_W = 1800` retained for backward compat. Swipe-down dismiss and animation all use instance `_yOpen`/`_yClosed` computed from actual portrait/landscape geometry.

---

### Block 5: Orientation overlay

No changes. v1.20 Block 6 already inverted the overlay to show "Rotate to portrait" when in landscape. With portrait now the canonical layout, the overlay is truthful: landscape = show overlay, portrait = game renders correctly. Optional "Continue in landscape" escape hatch was not added (polish-phase item).

---

### Block 6: Smoke evidence

**`npm run build` (portrait + desktop):** Clean. `tsc --noEmit` 0 errors. Vite: 533 modules transformed. Pre-existing chunk-size warning only (unchanged from v1.20).

**DevTools portrait emulation (iPhone 12 Pro 390×844):** Canvas renders at 944×1800 internally; CSS letterboxes to 390×743 with top/bottom letterbox bands (~50px each at DPR 2). All HUD elements visible in portrait layout: joystick bottom-left at y=1620, skill arc bottom-right fanning from (884,1690) to (622,1442), potions right edge at x=830, target-cycle btn bottom-center at (472,1700), icons top-row at y=60. DrawerShell opens as 700px slide-up from bottom.

**Desktop landscape (1920×1080):** All HUD positions unchanged (verified via `Mobile.isActive = false` branch in all constructors). DiabloHud globes, potionHud, dashCooldownHud, desktopHudIcons unaffected (these are desktop-only paths never touched by v1.21). `npm run build` clean.

---

### Files modified

- `src/rendering/stage.ts` — `let` canvas dims; `initCanvasDimensions()`
- `src/main.ts` — bootstrap reorder; `initCanvasDimensions()` call; shell.drawerW/H passthrough
- `src/mobile/mobile.ts` — `clientToCanvas` uses canvas.width/height/dpr
- `src/mobile/joystick.ts` — portrait y=1620 via instance `_cy`
- `src/mobile/touchHotbar.ts` — portrait BTN_POS_PORTRAIT array; instance `_pos`
- `src/mobile/touchPotions.ts` — portrait positions resolved in constructor
- `src/mobile/touchIcons.ts` — log icon x=884 portrait via constructor local
- `src/mobile/touchTargetBtn.ts` — portrait (472,1700) via constructor locals
- `src/ui/drawerShell.ts` — `getDrawerH()`/`getDrawerW()`; instance geometry; `readonly drawerH/W`
- `src/ui/inventoryPanel.ts` — optional `drawerW?`/`drawerH?` constructor params
- `src/ui/characterSheet.ts` — optional `drawerW?`/`drawerH?` constructor params
- `AGENT_STATE.md` — v1.21 STATE entry added
