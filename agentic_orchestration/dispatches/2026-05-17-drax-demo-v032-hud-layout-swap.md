# 2026-05-17 — drax-demo — v0.32 HUD layout swap (potions ↔ character/inventory positions)

**Status:** QUEUED — auto-spawn after `drax/v0.31-...` (dodge cooldown + VFX timing) ships.
**Authority:** Matt L3 disposition 2026-05-17 (playtest HUD layout preference).
**Type:** Pattern A (short task) — ~15-30 minutes estimated.
**Predecessor:** drax v0.31 dodge-fix (queued).
**Seam:** reincarnated-demo (Pixi.js) — HUD positioning constants only.

---

## Why this matters

Matt's playtest layout feedback:
> *"Let's move potions to where the character and inventory icons are and move the character/inventory icons to the top-left corner of the screen."*

Pure layout reorder. After this dispatch:
- **Potions** (PotionHud) → bottom-left, in the position where character + inventory icons currently sit
- **Character + inventory icons** (DesktopHudIcons) → top-left corner of viewport

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your v0.29 STATE entry (z-order fix context) + v0.30 + v0.31 STATE entries
2. `reincarnated-demo/src/ui/potionHud.ts` — current PotionHud positioning (currently x=14, y=839 per your v0.27 layout)
3. `reincarnated-demo/src/ui/desktopHudIcons.ts` — current DesktopHudIcons positioning (currently x=132, y=CANVAS_HEIGHT-105 per your v0.27 layout)
4. `reincarnated-demo/src/main.ts` — `_syncUiToScreen()` viewport-pinning + UI layer assignment

---

## Scope

### Item 1 — Swap positions

**Move PotionHud → current DesktopHudIcons position:**
- New position: approximately x=132, y=CANVAS_HEIGHT-105 (or whatever the current DesktopHudIcons anchor is)
- Maintain potion vertical stack / row layout from v0.27 (health [Q] + mana [E] still both present)
- Mouse-clickable handlers preserved from v0.27 + v0.29
- Persistent visibility (zero-quantity greyed state) preserved from v0.29
- Z-order: ensure DiabloHud HP globe still renders BELOW potions per v0.29 fix (instantiate DiabloHud first, then PotionHud, then DesktopHudIcons — same order, just different coordinates)

**Move DesktopHudIcons → top-left corner:**
- New position: top-left corner of viewport, anchored to (x=14, y=14) or similar small inset margin
- Maintain horizontal layout: inventory icon + character icon side-by-side (or stack vertically if cleaner at top-left given less horizontal space)
- Key-binding labels preserved (I for inventory; C for character)
- Mouse-clickable handlers preserved (toggle open/close panes)
- Hover highlight preserved
- Use `_syncUiToScreen()` pattern — top-left counter-offset against `app.stage` so icons stay pinned to viewport top-left across camera pan + window resize

### Item 2 — Verify no collision with other HUD elements

- Top-left corner: confirm no existing HUD elements occupy that space
  - Hotbar is bottom-anchored (v0.25 pin)
  - DiabloHud HP globe at x=76, y=880 (bottom-left)
  - Tier badges + cooldown radials are on hotbar (bottom)
  - Tooltips are on hover (transient; not positioned at top-left)
  - Any minimap or buff/debuff UI? — if present, ensure DesktopHudIcons doesn't overlap
- Bottom-left potion position: confirm DiabloHud HP globe (DiabloHud is the HP/mana globes; PotionHud is potion icons) still renders cleanly without occlusion per v0.29 z-order fix

### Item 3 — Test

- Load demo → potions visible at new bottom-left position; inventory + character icons visible at top-left
- Click each icon → respective behavior fires (potion use; inventory toggle; character toggle)
- Resize window → both groups re-anchor correctly (potions stay bottom-left; icons stay top-left)
- Camera pan during play → HUD elements stay pinned to viewport (don't scroll with world)

---

## Out of scope (DO NOT)

- ❌ DO NOT change the hotbar (v0.28 pinning + readability stays)
- ❌ DO NOT change the DiabloHud HP/mana globes
- ❌ DO NOT modify click handlers or pane-toggle logic
- ❌ DO NOT change icon glyphs / key-binding labels
- ❌ DO NOT add new HUD elements
- ❌ DO NOT touch engine, simulation, loadout files
- ❌ DO NOT extend scope to other layout tweaks (surface as OBSERVATION)

---

## Acceptance criteria

- [ ] PotionHud now at former DesktopHudIcons position (bottom-left, x=132 area)
- [ ] DesktopHudIcons now at top-left corner (x=14, y=14 area or similar inset)
- [ ] Both groups remain mouse-clickable; pane-toggle behaviors work
- [ ] Both groups remain viewport-pinned (don't scroll with camera)
- [ ] Window-resize handling correct for both
- [ ] No HUD-element occlusion at new positions
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Tag `drax/v0.32-hud-layout-swap-1`
- [ ] Hive-log STATE entry

---

## Smoke test expectation

1. Load demo → potions visible bottom-left (slightly right of where HP globe lives); inventory + character icons visible top-left corner
2. Click potion → potion use fires
3. Click inventory icon → inventory pane opens
4. Click character icon → character pane opens
5. Resize browser window → both groups stay at their corners
6. Move character around map → HUD elements stay put (don't scroll with world)
7. Build clean

---

## Math-before-code requirements

N/A — pure coordinate change.

---

## Tag intent

`drax/v0.32-hud-layout-swap-1` — single-commit ship.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

*Queued 2026-05-17 by knight-rider per Matt L3 disposition. Spawn after v0.31 ships. Estimated 15-30 min. Append completion record when done.*

---

## Completion record

**Status:** COMPLETE
**Date:** 2026-05-17
**Agent:** drax
**Commit:** `922db45` — reincarnated-demo
**Tag:** `drax/v0.32-hud-layout-swap-1`
**Actual time:** ~15 min

### Acceptance criteria

- [x] PotionHud now at former DesktopHudIcons position (bottom-left, x=132)
- [x] DesktopHudIcons now at top-left corner (x=14, y=14)
- [x] Both groups remain mouse-clickable; pane-toggle behaviors work
- [x] Both groups remain viewport-pinned (don't scroll with camera)
- [x] Window-resize handling correct for both
- [x] No HUD-element occlusion at new positions (top-left confirmed empty)
- [x] Demo build clean (`npm run build`); no console errors
- [x] Tag `drax/v0.32-hud-layout-swap-1`
- [x] Hive-log STATE entry

### Notes

Pure coordinate change. Three files modified: `src/ui/potionHud.ts`, `src/ui/desktopHudIcons.ts`, `src/main.ts` (comments only in main.ts).

`CANVAS_HEIGHT` import removed from `desktopHudIcons.ts` (no longer needed at top-left anchor).
