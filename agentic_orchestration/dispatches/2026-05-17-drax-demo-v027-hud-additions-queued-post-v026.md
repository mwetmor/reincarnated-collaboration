# 2026-05-17 — drax-demo — v0.27 HUD additions (potion + inventory + character icons)

**Status:** QUEUED — to spawn after `drax/v0.26-followup-ui-cleanup-and-dodge-primitive-1` ships.
**Authority:** Matt L3 disposition 2026-05-17 (focused playtest test 6 follow-up; HUD readability).
**Type:** Pattern B (long task) — ~1-2 hours estimated.
**Predecessor:** drax v0.26 (in flight).
**Seam:** reincarnated-demo (Pixi.js) — UI overlay + input bindings.

---

## Why this matters

Matt focused-playtest test 6 follow-up: HUD needs persistent on-screen indicators for potions + inventory + character pane access. ARPG-canonical readability. Mouse-clickable if possible.

These are pure HUD additions — no engine integration needed. Potion quantity can placeholder against a static count if no engine potion system exists yet; the icon + key-binding + click-to-open shape matters more than the underlying potion mechanic for this dispatch.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your v0.26 ship STATE + this dispatch context
2. `reincarnated-demo/src/main.ts` — your v0.25 `_syncUiToScreen()` helper (HUD additions follow the same pattern: counter-offset against `app.stage`)
3. `reincarnated-demo/src/visuals/sprites.ts` — your v0.25 + v0.26 label/bar work (HUD items live in the same UI overlay layer)
4. `reincarnated-demo/AGENT_STATE.md` — your seam's current state

---

## Scope (3 HUD items)

### Item 1 — Potion icon + quantity indicator

**Fix:**
- Add a potion icon to the HUD (typically bottom-left or near the skill hotbar)
- Show quantity as numeric overlay (e.g., "x3")
- Key binding label: typically **Q** for potion-use in ARPGs (D2 / D3 / PoE convention); pick what feels natural and not collision-conflicting with existing bindings
- Display the key-binding label next to or below the icon (small text, readable but not dominant)
- **Mouse-clickable:** clicking the icon attempts to use a potion (same behavior as pressing the key binding)
- **Engine integration is optional for this dispatch:**
  - If a potion system exists in the engine/season data, wire to it
  - If not, placeholder with a static quantity (e.g., 5) + a no-op on use (or "TODO(drax) — wire to engine potion system when implemented")
- Visual: use a simple potion sprite (Pixi `Sprite` or `Graphics`-drawn). Can be a placeholder shape (small red bottle silhouette) if no proper sprite exists yet.

### Item 2 — Inventory icon + key binding + click-to-open

**Fix:**
- Add an inventory icon to the HUD (typically near potion icon, often a bag/backpack glyph)
- Key binding label: typically **I** or **Tab** for inventory in ARPGs
- Display key-binding label next to the icon
- **Mouse-clickable:** clicking the icon opens the inventory pane (same behavior as pressing the key)
- **Engine integration is optional:**
  - If demo already has an inventory pane that opens on a key press, just add the icon + key-binding label + click-to-open
  - If no inventory pane exists, the icon + key binding + click can placeholder open an empty pane with "TODO(drax) — inventory pane content"
- Pane behavior: clicking the icon a second time (or pressing the key again) closes the pane (toggle)

### Item 3 — Character icon + key binding + click-to-open

**Fix:**
- Add a character-sheet icon to the HUD (typically near inventory, often a person silhouette or stylized figure glyph)
- Key binding label: typically **C** for character sheet in ARPGs
- Display key-binding label next to the icon
- **Mouse-clickable:** clicking the icon opens the character pane (same behavior as pressing the key)
- **Engine integration is optional:**
  - If demo already has a character pane that opens on a key press, just add the icon + key-binding label + click-to-open
  - If no character pane exists, the icon + key binding + click can placeholder open an empty pane with "TODO(drax) — character pane content (stats / traits / etc.)"
- Pane behavior: toggle on repeat input

---

## Layout suggestion

HUD bottom-left arrangement (suggestion; you have layout judgment):

```
[Potion x3 | Q]  [Inventory | I]  [Character | C]                                                            [Hotbar 1-9]
```

Or stacked vertically along the left side. Either works; pick what reads cleanly on the chierit sprite scale.

---

## Out of scope (DO NOT)

- ❌ DO NOT implement engine-side potion system, inventory contents, or character sheet contents (icon + key-binding + click-to-open scope only)
- ❌ DO NOT modify the skill hotbar (v0.25 already pinned)
- ❌ DO NOT redesign the dodge VFX from v0.26 (cosmetic placeholder is intentional)
- ❌ DO NOT extend scope to other HUD additions (minimap, buff/debuff icons, etc.) — surface as OBSERVATION for future dispatch
- ❌ DO NOT touch engine, simulation, or loadout files

---

## Acceptance criteria

- [ ] Potion icon + quantity + key-binding label visible in HUD; mouse-clickable
- [ ] Inventory icon + key-binding label visible in HUD; mouse-clickable opens/closes pane
- [ ] Character icon + key-binding label visible in HUD; mouse-clickable opens/closes pane
- [ ] HUD items pin to viewport (use `_syncUiToScreen()` pattern from v0.25)
- [ ] Key bindings do not collide with existing inputs (hotbar 1-9, LMB, Space dodge, etc.)
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Tag `drax/v0.27-hud-additions-potion-inventory-character-1`
- [ ] Hive-log STATE entry

---

## Smoke test expectation

1. Load demo → 3 HUD icons visible (potion, inventory, character) with key-binding labels
2. Click potion icon → potion use attempted (or no-op placeholder); icon shows quantity
3. Click inventory icon → inventory pane opens; click again → closes
4. Click character icon → character pane opens; click again → closes
5. Press key bindings → same behavior as clicks
6. HUD items stay pinned across map transitions + window resize

---

## Math-before-code requirements

N/A — UI overlay; no engine math.

---

## Tag intent

`drax/v0.27-hud-additions-potion-inventory-character-1` — single-commit ship preferred.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

*Queued 2026-05-17 by knight-rider per Matt L3 disposition. Spawn after v0.26 ships. Estimated 1-2 hours. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Commit:** `ba75e76`
**Tag:** `drax/v0.27-hud-additions-potion-inventory-character-1`
**Hive log:** STATE entry appended to `phase-1-p1-log.md`

### Acceptance criteria — all satisfied

- [x] Potion icon + quantity + key-binding label visible in HUD; mouse-clickable
- [x] Inventory icon + key-binding label visible in HUD; mouse-clickable opens/closes pane
- [x] Character icon + key-binding label visible in HUD; mouse-clickable opens/closes pane
- [x] HUD items pin to viewport (`_syncUiToScreen()` pattern — all items in `_layers.ui`)
- [x] Key bindings do not collide (Q=health potion, E=mana potion, I=inventory, C=character — no conflict with 1-9, Space, LMB, Shift)
- [x] Demo build clean (`npm run build`): 521 modules, 0 errors
- [x] Tag `drax/v0.27-hud-additions-potion-inventory-character-1`
- [x] Hive-log STATE entry

### Implementation notes

**Potion HUD (src/ui/potionHud.ts):** `PotionHud` constructor extended with optional `onHealthClick` / `onManaClick` callbacks. Each potion row wrapped in an interactive Container with invisible hit-area, cursor pointer, and hover highlight. Key hints updated to bracket style `[Q]` / `[E]`. Mobile path passes `undefined` (TouchPotions continues to handle touch). Potion use logic extracted into `_handleHealthPotionUse()` + `_handleManaPotionUse()` in main.ts — shared by key handler and click callback, both call `_touchPotions?.update(potions)` so mobile HUD stays in sync.

**DesktopHudIcons (new: src/ui/desktopHudIcons.ts):** Two icon+label buttons: bag icon (inventory, `[I]`) and bust icon (character, `[C]`). Positioned `x=132, y=CANVAS_HEIGHT-105` (immediately right of PotionHud's 110px box). Desktop-only: instantiated at gauntlet start with `!Mobile.isActive` guard, destroyed in `clearUI()` alongside DiabloHud.

**Key bindings:** No changes needed — Q/E/I/C were already wired in `_handlePotionInput()` and the keyboard scan loop. The new icons are purely additive click targets for the same logic.
