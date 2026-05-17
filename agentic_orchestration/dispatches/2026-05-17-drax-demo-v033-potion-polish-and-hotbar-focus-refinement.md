# 2026-05-17 — drax-demo — v0.33 Potion polish + Skill hotbar focus refinement

**Authority:** Matt L3 disposition 2026-05-17 (playtest post-v0.32 feedback).
**Type:** Pattern B (long task) — ~1-2 hours estimated (2 substantive HUD improvements).
**Predecessor:** drax v0.32 HUD layout swap (just shipped).
**Seam:** reincarnated-demo (Pixi.js) — HUD overlay layer; PotionHud + combatHud.ts.
**Status:** AUTO-SPAWN — drax-demo idle; spawn immediately.

---

## Why this matters

Matt's playtest feedback post-v0.32:

> *"Potion UI = ALMOST PASS. Move the potions just slightly to the right of where they are.. just a hair. And give them bottle icons that are much larger and put the count of potions inside of the bottles."*

> *"For skill hotbar, we're getting much better. I like the large size box for the ULT. I like the icons, but make the icons fit the boxes. Make the icons draw all focus and have the text appear just below the icons as if they were character health under a character. Color code the inner filled shape of the icons to the element."*

Two HUD polish surfaces. Both lean toward **visual prominence + readability** — bigger icons, less reliance on text-as-overlay, integrated quantity-in-vessel for potions, element-color extending from frame INTO the inner glyph.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your v0.32 STATE entry (most recent)
2. `reincarnated-demo/src/ui/potionHud.ts` — your v0.32 work (x=132 anchor)
3. `reincarnated-demo/src/ui/combatHud.ts` — your v0.28 hotbar work (substrate frames + tier badges + radial sweeps + tooltips + slot sizing)
4. Color palette per substrate (from v0.28): fire `#E85D24`, water `#3B8EE0`, earth `#8B5A2B`, wind `#A3D9E0`, lightning `#F2D027`, holy `#F5D061`, shadow `#3D2C4E`

---

## Scope (2 items)

### Item 1 (HIGH) — Potion HUD polish

**Three changes:**

#### 1a. Slight right-shift

- Move PotionHud container x from 132 → approximately **148-160** (a "hair" to the right — fine-tune visually)
- Maintain bottom anchor (y unchanged)
- Verify no collision with DiabloHud HP globe (x=76, y=880, radius=58) at new position

#### 1b. Larger bottle icons

- Bottle icon size: increase by **~50-80%** over current (current is small icon + text label combo)
- Use a proper bottle silhouette glyph (Pixi `Graphics` flask/potion-bottle shape, OR existing sprite if available)
- Make the bottles visually prominent — they should read at-a-glance from peripheral vision
- Maintain pair layout: health [Q] potion + mana [E] potion side-by-side or stacked

#### 1c. Quantity count INSIDE the bottle (integrated)

- Current pattern: bottle icon + "x3" text label next to/below it
- New pattern: render the count INSIDE the bottle silhouette
  - Number renders centered inside the bottle's body region
  - Number is large + readable (bold; ~16-20pt for visual weight in the larger bottle)
  - Color: contrasts cleanly against bottle interior color (e.g., dark number on light bottle interior; or light number on dark bottle interior)
  - At zero quantity: show "0" inside the bottle, with bottle rendered in greyed-out state (~50% alpha)
  - At full quantity: bottle interior shows the count crisply
- Key binding label [Q] / [E] remains below or to the side of the bottle — small, readable, secondary to the bottle visual itself
- Mouse-clickable hit-area covers the entire bottle (preserve v0.27 + v0.29 click handlers)

**Visual hierarchy:** bottle = primary visual identity; count = secondary integrated info; key binding = tertiary subtle text label.

### Item 2 (HIGH) — Skill hotbar focus refinement

**Three changes:**

#### 2a. Fit icons to boxes (inner glyph expansion)

- Current state per v0.28: icons render inside SLOT_W 124 × SLOT_H 98 boxes with substrate-colored frame (2.5-3px border)
- The inner skill glyph likely doesn't fill the full available interior (frame eats some + glyph has its own internal padding)
- **Fix:** scale up the inner skill glyph to fill the box's available interior (leaving only the frame's 2.5-3px border + ~1-2px breathing room)
- For BASIC + STANDARD + AOE + UTILITY slots: glyph fills box at 1.0x interior
- For ULTIMATE slot (1.15x at v0.28): glyph fills ULTIMATE box at same 1.0x interior — so ULT glyph reads visibly larger than other glyphs
- Verify glyph aspect ratio remains correct (don't distort)

#### 2b. Color-code INNER filled shape to element

- Current state per v0.28: substrate color applies to the OUTER FRAME only; inner glyph is presumably neutral/grayscale or generic
- **Fix:** apply substrate color to the **inner filled shape** of the icon (the glyph fill, not just the frame)
- Per-substrate inner-fill color: same palette as the frame (fire orange, water blue, etc.)
- **Visual treatment options (pick one):**
  - **Option A (high contrast):** glyph fill = substrate color at 80-90% saturation; glyph outline = darker variant or neutral. Reads as "element-saturated icon."
  - **Option B (gradient):** glyph fill = substrate color gradient (lighter at top to darker at bottom, like a glassy element); maintains depth.
  - **Option C (substrate-coherent palette):** use both substrate primary + secondary accent from v0.28 palette table (fire primary `#E85D24` + accent `#FFC857`) for two-tone glyph fills.
- Use your aesthetic judgment; the load-bearing requirement is "inner glyph reads as element-colored, not just the frame."

#### 2c. Text below icons (like nameplate under character)

- Current state per v0.28: key-binding labels (1-9, etc.) are on the icon corner (likely top-right or similar)
- Matt's request: text moves to **below** the icons, "as if they were character health under a character"
- **Fix:**
  - Move key-binding label from inside/on-the-icon → to a position **just below the icon's bottom edge** (~2-4px below)
  - Label remains readable (~12-14pt; bold)
  - Multiple text rows OK if needed (e.g., key binding on row 1; cooldown numeric on row 2 if you want to display it)
  - Maintain visual hierarchy: icon dominates; text below is supportive
- This frees the icon corner from text overlay → glyph reads cleaner / larger / more focus-drawing

**Visual hierarchy after these changes:** ULT box = biggest visual weight; substrate-colored frame + substrate-colored inner glyph; tier badge in icon corner; cooldown radial overlay; text below icon (key bind + optional cooldown numeric); tooltip on hover unchanged.

---

## Out of scope (DO NOT)

- ❌ DO NOT change tier badge logic (BASIC/ULTIMATE/AOE/UTILITY inference unchanged from v0.28)
- ❌ DO NOT change cooldown radial sweep logic (v0.28 unchanged)
- ❌ DO NOT change tooltip content (v0.28 unchanged)
- ❌ DO NOT touch v0.31 dodge state machine
- ❌ DO NOT touch v0.32 HUD layout positions for DesktopHudIcons (top-left corner stays as-is)
- ❌ DO NOT modify engine, simulation, or loadout files
- ❌ DO NOT extend scope to other HUD polish noticed
- ❌ DO NOT pre-empt v1.0 narrow-slice render work (separate dispatch; AOE indicators + engine-coupled dodge come later)

---

## Acceptance criteria

- [ ] PotionHud shifted slightly right (~148-160 x)
- [ ] Bottle icons noticeably larger (~50-80% increase)
- [ ] Potion count rendered INSIDE each bottle (no separate "x3" label)
- [ ] Zero-quantity state: "0" inside greyed-out bottle (v0.29 persistent visibility preserved)
- [ ] Skill icon inner glyph fills box interior (frame + 1-2px breathing only)
- [ ] Inner glyph substrate-color-coded (your choice of A/B/C visual treatment)
- [ ] Key-binding label moved to BELOW icon (no longer on-icon corner)
- [ ] ULT icon visibly more prominent due to expanded inner glyph
- [ ] No regression on tier badges / cooldown radial / tooltips / mouse hover
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Tag `drax/v0.33-potion-polish-and-hotbar-focus-refinement-1`
- [ ] Hive-log STATE entry

---

## Smoke test expectation

1. Load demo → potions are visually prominent at slight-right bottom-left; count clearly visible inside each bottle
2. Hotbar shows: substrate-frame border + element-colored inner glyph + tier badge + cooldown radial; key binding below
3. ULTIMATE slot visibly biggest with most prominent glyph + ornate frame
4. Test 2-3 classes from different substrates → each substrate reads visibly different at-a-glance via both frame AND inner glyph color
5. Hover skill → tooltip still appears with all v0.28 info
6. Click potion → use fires; count decrements visibly inside bottle
7. Build clean

---

## Math-before-code requirements

N/A — UI visual polish.

---

## Tag intent

`drax/v0.33-potion-polish-and-hotbar-focus-refinement-1` — single commit ship.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 disposition. Estimated 1-2 hours. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Commit:** `6c15a3e`
**Tag:** `drax/v0.33-potion-polish-and-hotbar-focus-refinement-1`
**Build:** `npm run build` PASS — TypeScript clean, Vite 22.26s

### Acceptance criteria status

- [x] PotionHud shifted slightly right (~148-160 x) — shipped at x=155
- [x] Bottle icons noticeably larger (~50-80% increase) — oval body ry=22 (vs. r=6 circles); ~65% taller
- [x] Potion count rendered INSIDE each bottle (no separate "×N" label) — bold 17pt Text anchored at body oval center
- [x] Zero-quantity state: "0" inside greyed-out bottle (v0.29 persistent visibility preserved) — bottle 0.45 alpha, count 0.55 alpha
- [x] Skill icon inner glyph fills box interior (frame + 1-2px breathing only) — PAD = framePx + 2
- [x] Inner glyph substrate-color-coded (Option C two-tone: primary fill + secondary accent lines)
- [x] Key-binding label moved to BELOW icon (no longer on-icon corner) — HOTBAR_Y raised 20px, labels in container coords below box
- [x] ULT icon visibly more prominent due to expanded inner glyph — innerGlyph.alpha pulses at ready
- [x] No regression on tier badges / cooldown radial / tooltips / mouse hover — all v0.28 logic preserved
- [x] Demo build clean (`npm run build`); no console errors
- [x] Tag `drax/v0.33-potion-polish-and-hotbar-focus-refinement-1` applied
- [x] Hive-log STATE entry appended

### Implementation notes

**PotionHud:** `_drawBottle()` function draws the flask silhouette each render call (body ellipse + neck rect + cap rounded-rect + glass shimmer highlight + white outline). Bottle size constants: `BTL_BODY_RX=17, BTL_BODY_RY=22, BTL_NECK_H=12, BTL_CAP_H=4` — total height ~62px. Hit-areas cover full `BTL_HIT_H` extent. `update()` calls `_drawBottle()` to redraw at appropriate alpha on each inventory change.

**AbilityHotbar:** `_drawInnerGlyph()` dispatches on `GlyphShape` (5 archetypes: burst/beam/arc/zone/point). Shape mapped from `geometry_type` via `_geometryToGlyph()`. Key labels are `Text` objects added to `this.container` (not to `bg`), positioned at `y = slotY + slotH + 3`. `HOTBAR_Y` adjusted upward by `KEY_LABEL_BELOW_H = 20`. Unused `deduplicateSkillNames` import removed.

— drax
