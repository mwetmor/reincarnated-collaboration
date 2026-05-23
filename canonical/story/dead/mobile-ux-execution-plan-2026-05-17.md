# Mobile UX Execution Plan — 2026-05-17

> **STATUS:** DEAD BRANCH (primary framing superseded — D1 PC/console-first lock 2026-05-23; mobile-port deferred to +6 months) — do NOT consult as current truth. See `canonical/00-ground-state.md`

**Authority:** Drax (drax). Pattern B engineering-plan artifact. Commissioned 2026-05-17 by knight-rider per Matt L3.
**Scope window:** VS2b territory or later — NOT VS2a-gating. This document is the plan; implementation fires via separate dispatches.
**Commission:** `agentic_orchestration/dispatches/2026-05-17-drax-demo-mobile-ux-research-and-plan-commission.md`
**Gandalf sizing canon consumed:** `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (shipped — live numbers used below; no `<gandalf-pending>` placeholders needed).
**Tag:** `drax/v1.6-mobile-ux-research-and-plan-1`
**Status:** Canonical plan. Implementation dispatches reference this doc phase-by-phase.

---

## § 1 — Executive summary

Demo1 playtest revealed mobile is unusable on phones: all text is unreadable (class names, gear names, flavor text, damage numbers, combat log — all hardcoded at desktop 8-16px), screen layout overlaps on phone aspect ratios, and two critical input gaps (no dash button, no manual targeting) prevent ARPG-competent play. The existing `src/mobile/` directory ships a solid foundation (joystick, touch hotbar, touch potions, touch icons, target-cycle button) but it is not yet a complete or legible mobile experience. This plan decomposes the full rework into 7 sequential phases (M1–M7), ordered by dependency. Phase M1 is the unblocking phase: a font-size constants module consumed by all later phases. Phases M2–M4 deliver the three critical input + readability gaps Matt flagged. Phases M5–M7 complete the panel redesigns, layout safe-area pass, and gesture polish. The plan consumes gandalf's sizing canon directly; no `<gandalf-pending>` stubs required. Matt reads this plan and decides when to authorize M1 dispatch.

---

## § 2 — Mobile-gap audit matrix

### § 2.1 — Per-file capability inventory: `src/mobile/`

**`mobile/mobile.ts`**
- Mobile detection via `pointer: coarse` media query + UA string check. Reliable.
- Canvas CSS scaling: sets `max-width:100vw`, `max-height:100dvh`, `object-fit:contain`. Works; does NOT set safe-area insets — notch / Dynamic Island / Android nav-bar insets are unhandled.
- Orientation lock: deferred to first touchstart; fires `screen.orientation.lock('landscape')`. Correct pattern for iOS user-gesture requirement.
- `clientToCanvas(clientX, clientY)`: converts CSS-space pointer coordinates to canvas-internal 1800×944 space. Used correctly by all mobile components.
- `pointerConsumedByUI` flag + `consumePointer()` / `resetPointerConsumed()`: prevents LMB-click-to-move from double-firing when a UI element handles the same touch. Architecture is correct; all mobile components call `consumePointer()` on their touches.
- **Gap:** No `env(safe-area-inset-*)` injection. Notch / home-bar area bleeds into joystick and icon positions on iPhone X+.

**`mobile/joystick.ts`**
- Virtual joystick at canvas coords (180, 700). R_OUTER=80 (160px diameter), R_INNER=30 (60px diameter).
- Pointer capture via canvas `pointerdown` + window `pointermove` / `pointerup` — correct cross-browser pattern.
- Returns normalized (nx, ny) vector; animated snap-back on thumb release (RETURN_DUR=0.15s).
- Gandalf canon: R_OUTER should be 75 (150px diameter) — current 80 is at upper edge of cluster; 75 is centroid. Minimal change.
- **Gap (minor):** R_OUTER=80 vs canon 75. Functional; not blocking.
- **Gap (position):** JOY_CX=180, JOY_CY=700 — needs safe-area inset compensation on notched phones so the joystick doesn't bleed under the system chrome.

**`mobile/orientationOverlay.ts`**
- Portrait-mode overlay: DOM-based full-screen div, `display:flex` when `(orientation:portrait)`. Text "ROTATE YOUR DEVICE". Z-index 9999 above canvas.
- Works correctly. Font sizes 64px (icon), 18px (bold text), 13px (sub) — readable.
- **Gap (minor):** "Best experienced in landscape" suggests landscape-forced; some phones may not support orientation lock (especially iOS on iPhone with rotation locked at system level). Overlay handles the fallback gracefully (stays visible until user physically rotates).

**`mobile/touchHotbar.ts`**
- 6 circular buttons in bottom-right arc. BTN_R=42 (84px visual diameter), HIT_R=52 (104px touch zone).
- Arc positions hardcoded at BTN_POS array: (1690,752), (1660,670), (1618,598), (1565,538), (1502,492), (1432,462).
- Element color per skill.canonical_element; cooldown overlay; cooldown numeric label (14pt); energy cost label (9pt).
- Skill name abbreviation: 3-letter element code, 11pt monospace. Not skill name.
- Slot badge: 8pt.
- Gandalf canon: 120px circular touch targets (radial arc). Current HIT_R=52 (104px) is at the lower edge of the 110–125px canon centroid; acceptable but slightly small.
- **Gap:** No dash button in this arc. Dash is separate from the skill arc on desktop (Shift/Space). Mobile needs a dedicated touch button.
- **Gap:** Skill abbreviation shows element code, not skill name. Arguably intentional (no room at 42px radius for a full name) — fine at this size.

**`mobile/touchIcons.ts`**
- Three icons at top: Inventory (x=60), Character (x=120), Combat Log (x=1740). ICON_Y=60. ICON_R=26 (52px diameter), HIT_R=36 (72px touch zone).
- Procedural glyphs: bag (inventory), bust (character), scroll (log).
- **Gap:** ICON_R=26 (52px diameter) is below Apple HIG minimum 44dp = 88px at 2x. HIT_R=36 is 72px — also below floor. Gandalf canon: ICON_R should be 44 (88px diameter). Current implementation is too small for reliable tap.
- **Gap:** Icons at y=60 may overlap with system status bar (time/battery/signal) on phones without safe-area insets applied.

**`mobile/touchPotions.ts`**
- HP potion at (1498, 668), Mana at (1498, 742). POT_R=28 (56px visual), HIT_R=38 (76px touch zone).
- Visual radius 56px is below the 110–125px action-touch canon centroid; still above the 88px floor when you count the hit radius.
- **Gap:** HIT_R=38 (76px) is below the 88px Apple HIG floor. Gandalf canon: HIT_R should be ~50 (100px effective touch zone), with POT_R scaled to ~35 (70px visual).
- **Gap:** Potion buttons positioned at x=1498 — this is very close to the TouchHotbar skill arc (BTN_POS slot 4 is at x=1502, y=492). The arc extends from y=462 to y=752; potions at y=668 and y=742 may visually overlap the arc. Needs layout audit.

**`mobile/touchTargetBtn.ts`**
- Target-cycle button at (1408, 705). BTN_R=28 (56px visual), HIT_R=38 (76px touch zone).
- Shows 6-character truncation of current target name as hint below.
- Implements target cycling (rotate through alive pack members).
- **Gap:** Touch zone 76px is below the 88px floor. Minor refine needed.
- **Gap:** Cycling is the only targeting mode. No tap-to-directly-select a specific enemy. This is the "manual targeting" gap Matt flagged.

### § 2.2 — Gap matrix (full)

| Capability | Desktop today | Mobile today | Gap |
|---|---|---|---|
| Movement input | WASD / LMB-click-to-move | Virtual joystick | No gap — joystick ships and works |
| Targeting | Mouse hover (auto-selects nearest on LMB) | TouchTargetBtn cycle | Partial — cycle exists; no tap-to-directly-select enemy |
| Dash | Space bar | None | MISSING — no mobile dash button |
| Skill activation | Number keys 1-6 / hotbar click | TouchHotbar 6-button arc | No gap — ships and works |
| Potion use (health) | Q key or click | TouchPotions HP button | Ships; touch zone 76px below floor; minor refine |
| Potion use (mana) | E key or click | TouchPotions Mana button | Ships; touch zone 76px below floor; minor refine |
| Inventory open | I key or DesktopHudIcons click | TouchIcons bag icon | Ships; ICON_R too small (52px vs 88px floor); minor refine |
| Character sheet open | C key or DesktopHudIcons click | TouchIcons bust icon | Ships; same size gap as above |
| Combat log toggle | H key or DesktopHudIcons click | TouchIcons scroll icon | Ships; same size gap |
| Portrait guard | n/a | orientationOverlay.ts | Ships; works |
| Damage text legibility | 15px normal / 20px crit | Inherits desktop sizes | MISSING — unreadable on phone (need 24–32px) |
| Status text legibility | 12px | Inherits desktop sizes | MISSING — unreadable on phone (need 18–22px) |
| Combat log text | 9.5px | Inherits desktop sizes | MISSING — unreadable; need full redesign |
| Character sheet | 640×560 modal, 9-13px text | Inherits desktop, not adapted | MISSING — doesn't fit phone screen; text 9–13px unreadable |
| Inventory panel | 700×500 modal, 8.5–12px text | Long-press tooltip partial | Partial — long-press tooltip ships; panel layout not mobile-adapted; text too small |
| Gear tooltip | Hover (desktop) | Long-press 400ms (ships in inventoryPanel.ts) | Partial — logic ships; typography too small |
| HUD globes (HP/MP) | DiabloHud 116px diameter globes | Inherits desktop — no mobile layout | Layout gap — globes centered at canvas edges (x=76, x=1724), positioned at y=880; may work at phone viewport scale but no integration with touch-potion merge (see gandalf §7 Q1) |
| Safe-area insets | N/A (desktop) | Not applied | MISSING — notch / Dynamic Island / nav-bar unhandled; joystick + icons could be obscured |
| Tap-to-move (alt movement) | LMB click-to-move | Not on mobile (joystick only) | Defer (see § 8 out-of-scope) |
| Gear drop interaction | Click to inspect | Touch to inspect (no explicit mobile path) | Defer (see § 8) |
| Font constants module | Hardcoded throughout all src/ | No mobile overrides | MISSING — foundational gap; precondition for all legibility fixes |

---

## § 3 — Touch input architecture

### § 3.1 — Targeting: recommendation and rejected alternatives

**Recommended: tap-to-lock-then-auto-engage (Eternium pattern)**

On touch, tapping directly on a visible enemy locks that enemy as the primary target. The target-lock indicator (described below) makes the selection visible. Once locked, the player's skills auto-engage the locked target when fired from the TouchHotbar. If the locked target dies, the system auto-advances to the nearest remaining enemy (current auto-target behavior). The existing TouchTargetBtn cycle remains as a secondary fallback (cycle through enemies when no direct tap is available).

**Why this pattern:**

The Diablo Immortal "tap-to-target-then-tap-again-to-attack" pattern requires two discrete taps per attack cycle. In a fast-paced gauntlet ARPG with limited hotbar space this creates friction. Torchlight Infinite's "drag-to-cycle-target" uses a drag gesture that conflicts with the joystick zone. Eternium's tap-to-lock is the cleanest for our input model: the joystick handles movement, the skill arc handles ability fire, and a direct enemy tap handles targeting — no gesture vocabulary conflicts.

**Rejected alternatives:**
- Diablo Immortal tap-to-target-then-tap-again: two-action attack-cycle; too much friction given our 6-ability hotbar.
- Torchlight drag-to-cycle: drag gesture conflicts with joystick zone and skill arc zone.
- Auto-nearest only (current): sub-optimal (Matt's direct complaint); no player agency on target selection.

**Implementation sketch (Phase M3):**
- Add `pointerdown` handler to the enemies/pack layer in main.ts. Hit test incoming touch coordinate (via `Mobile.clientToCanvas`) against each pack member's hitbox (extend the existing `CLICK_HIT_RADIUS=50` or use gandalf's canon 75px for mobile).
- If a pack member is hit: set `primaryActorIdx` to that enemy; call `Mobile.consumePointer()` to prevent LMB-move from also firing.
- Target-lock indicator: a pulsing ring around the locked enemy (reuse element-color from the combatant's dominant element; 2px stroke, r = enemy_radius + 12).
- Auto-advance on target death: existing behavior in `_getPrimaryTarget()` already returns nearest alive enemy when `primaryActorIdx` is out of range. Preserve.

### § 3.2 — Dash: mobile touch button

**Placement:** Bottom-right cluster, attached to the TouchHotbar arc. The skill arc currently occupies x~1432–1690 (right side) at y~462–752. The natural placement for a dash button is below/beside the arc, distinct from the skill slots but within right-thumb reach. Proposed: x=1700, y=840 — just to the lower-right of the HP globe (globe at x=1724, y=880; the globe's visual frame extends to ~y=830, so y=840 puts the dash button above the globe without overlap).

**Glyph:** Running-figure silhouette — identical to the existing `DashCooldownHud` in `dashCooldownHud.ts`. Reuse `_drawRunningFigure()` logic. The mobile button visually matches the desktop dash indicator.

**Size:** Touch zone 110px diameter (HIT_R=55). Visual radius ~50px (r=50). Matches gandalf canon for high-frequency action buttons (110–125px centroid).

**Cooldown indicator:** Same radial sweep pattern as desktop `DashCooldownHud`. The button dims to 0.65 alpha during cooldown with numeric countdown. Fires `_startDodge()` (the same function hooked to Space on desktop).

**Gesture:** Single tap. No hold or swipe needed — dash should be instant-response.

**Implementation sketch (Phase M2):**
- New file `src/mobile/touchDashBtn.ts`. Pattern matches `touchTargetBtn.ts` (single circular button, pointer event handling, `Mobile.consumePointer()` call, flash timer, `update(cooldownRemaining, totalCooldown, dt)` method).
- Constructor accepts `onDash: () => void` callback (maps to `_startDodge()` in main.ts).
- main.ts: instantiate alongside other mobile UI in the `if (Mobile.isActive)` block; pass dash callback; update in tick loop.

### § 3.3 — Manual movement vs auto-pathing

Virtual joystick exists and is the primary movement input. Tap-to-move is NOT recommended for mobile. The joystick-plus-ability-arc layout follows the dual-stick ARPG canon (Diablo Immortal, Torchlight Infinite, Genshin Impact) and is what the kiting math in `movement-speed-baseline.md` assumes. Adding tap-to-move would conflict with tap-to-target (the tap gesture is reserved for targeting from § 3.1). Dual-stick only; deferred in the tap-to-move line item.

### § 3.4 — Gesture vocabulary (complete contract)

| Gesture | Reserved for | Notes |
|---|---|---|
| Single tap on enemy sprite | Target-lock (Phase M3) | Consumes pointer; does not also fire skill |
| Single tap on skill arc button | Fire skill at current target | Existing behavior |
| Single tap on dash button | Execute dash | Phase M2 |
| Single tap on potion buttons | Use potion | Existing behavior |
| Single tap on top-row icons | Open panel (inv / char / log) | Existing behavior |
| Single tap on target-cycle btn | Cycle to next enemy | Existing behavior |
| Long press (400ms) on inventory item | Show gear tooltip | Existing behavior (`_addLongPress` in inventoryPanel.ts) |
| Joystick drag (left thumb zone) | Movement | Existing behavior |
| Double tap on enemy | NOT reserved (avoid) | Reserve for future "priority target" marking or leave unused |
| Two-finger pinch | NOT reserved in current scope | Camera zoom is out of scope; do not implement |
| Swipe from edge | NOT reserved | System-gesture conflict risk; avoid |

---

## § 4 — Screen layout remap

### § 4.1 — Safe areas

The canvas already uses `max-width:100vw`, `max-height:100dvh`, `object-fit:contain` (set by `mobile.ts`). What's missing is safe-area-inset compensation for the UI elements positioned within the canvas. Since the canvas is CSS-scaled with `object-fit:contain`, the visual canvas area may not start at (0,0) of the viewport — there are letterbox bars. The canvas `getBoundingClientRect()` is already used for `clientToCanvas()` coordinate conversion, which correctly handles the letterbox. The remaining gap is that HUD elements placed near canvas edges may be visually obscured by the device's system chrome (notch, Dynamic Island, home indicator, Android nav bar).

**Implementation approach (Phase M6):**
- Read `window.visualViewport` (or `env(safe-area-inset-*)` via a hidden DOM probe element) to determine safe-area insets in CSS pixels.
- Convert insets to canvas-space using the same `clientToCanvas` ratio.
- Pass canvas-space insets to all HUD components as constants at init time. Components shift their anchors inward by the inset amount.
- Components affected: joystick (bottom-left), dash button (bottom-right), potion buttons (bottom-right), top-row icons (top corners), TouchHotbar arc (bottom-right).

### § 4.2 — HUD zone layout (landscape phone — secondary orientation; portrait diagram TBD per § 4.3 amendment)

> **AMENDED 2026-05-17:** Mobile orientation is now **portrait-primary** (per § 4.3 amendment + `agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md`). The landscape diagram below is retained as the **secondary-orientation reference**. The **portrait HUD zone diagram is TBD** — drax authors it in the M5/M6 portrait-layout dispatch when it fires VS2b. See § 4.3 for the contents specification.

```
+--[BAR: HP | LVL | RES]----------------------------------+
|  [INV] [CHR] [LOG]          [WAVE STATUS]          (top)|
|                                                          |
|                   GAMEPLAY FIELD                         |
|                   (clear center)                         |
|               damage text overlays here                  |
|                                                          |
|   JOYSTICK              [TGT-CYCLE] [POT-HP] [POT-MP]  |
|  (bottom-left)                                           |
|                         [SKILL-1]                        |
|                   [SKILL-2]  [SKILL-5]                  |
|  [HP-GLOBE]     [SKILL-3]  [SKILL-6]   [RES-GLOBE]     |
|                   [SKILL-4] [DASH]                      |
+---------------------------------------------------------(bottom)
```

Zone breakdown (canvas-space, 1800×944 internal, landscape):

| Zone | Position | What lives there |
|---|---|---|
| Top strip (y=0–80) | full width | Wave status label (center-top); top-left icons (x=40–180, y=40–80); |
| Bottom-left (x=0–360, y=620–944) | left thumb | VirtualJoystick (center ~180,700); HP globe (x=76, y=880) |
| Bottom-right (x=1200–1800, y=400–944) | right thumb | TouchHotbar arc; DashBtn; TouchPotions; TouchTargetBtn; Resource globe (x=1724, y=880) |
| Center (x=360–1440, y=80–820) | gameplay | Clear for characters, monsters, VFX. Damage text floats here |
| Status overlay (floats in center) | mid-screen | Floating damage numbers, status text; NO-FLY zone: avoid y>820 (HUD) and x<360 or x>1440 |

**Anti-overlap rules:**
- Floating damage text `spawnFloatingNumber()` x-range must avoid x<200 (joystick zone) and x>1400 (skill arc zone) when emitted by the player. Enemy damage text is fine anywhere in the center field.
- TouchTargetBtn (1408, 705), TouchPotions HP (1498, 668) and Mana (1498, 742), and TouchHotbar arc slot 4 (1502, 492) currently have y-proximity issues. Phase M6 layout pass resolves these.
- The HP/Resource globes sit at the very bottom edge (y=880, r=58 → visual top at y=822). The skill arc's lowest point is at slot 0 (y=752). Gap between arc and globes is 70px — acceptable but tight on smaller phones after safe-area inset.

### § 4.3 — Orientation

**AMENDED 2026-05-17 (Matt L3 lock; DoE feel-target cascade — `agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md`):**

**Portrait-primary, landscape-secondary.** Mobile target is portrait orientation. Landscape support is retained as a polish-phase item, not a v1 requirement.

**Rationale.** The DoE reference (Dungeon of Exile, Matt's 2026-05-17 play session) is portrait-only; the ARPG-mobile cluster (Diablo Immortal portrait-primary, Torchlight Infinite portrait-primary, Eternium portrait, Dungeon Hunter 6 portrait) converges on portrait orientation. Thumb-reach ergonomics and notification-overlay coexistence favor portrait. Full provenance: `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 7.1.

**Implications for this plan:**

- `orientationOverlay.ts` logic **inverts** — currently blocks portrait; should block landscape (or warn-but-allow) as the polish-phase mobile-secondary path. M6 layout-pass dispatch carries the inversion.
- HUD zone layout (§ 4.2) currently diagrams landscape phone. **Portrait diagram is TBD** — authored by drax in the M5/M6 portrait-layout dispatch when it fires VS2b. The landscape diagram is retained as the secondary-orientation reference; the portrait diagram becomes primary.
- All Phase M2-M7 dispatches (§ 7) target portrait viewport first when they fire VS2b; landscape adaptations are an opt-in polish-phase task.
- Touch-target sizing canon (per `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 4.3) is unchanged — portrait orientation does not change finger ergonomics; the 88 px floor and 110-125 px action centroid remain.

**Pending M5/M6 portrait-diagram contents (forward-flag for M5/M6 dispatch):**

The portrait HUD zone diagram should specify (derived from DoE screenshot per `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 2):

- Top strip: rift name banner + corner minimap (top-left, attached); HP bar attached to minimap module; timer below; return-to-city portal top-right
- Mid: gameplay field; floating damage numbers; resource bar overhead on player sprite (not in HUD)
- Bottom: character portrait (bottom-left, with red-dot loot-equip affordance); currency display (bottom-center-left); skill bar (bottom-center, 3-5 slots); ultimate (right of skill bar); **heal button** (bottom-right corner; cooldown-gated per canonical-32 § 13.1, single button, no potion-stack count); objective counter + XP bar at very bottom edge
- HP placement: forward-flagged in `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 7.4 — recommend top-left attached-to-minimap (DoE pattern) over bottom-corner globe (D-series). Not locked in this dispatch; surface to drax M5/M6 portrait-layout dispatch.

---

## § 5 — Typography table

Gandalf's sizing canon is live; all desktop values sourced from source audit in this session. Mobile recommendations apply when `Mobile.isActive`.

**Reference anchors (gandalf canon + Apple HIG + ARPG mobile survey):**
- Apple HIG body minimum: 11pt = 14px
- Material Design body minimum: 14sp
- ARPG mobile damage text: Diablo Immortal 20–32px (cluster centroid 24px normal, 32px crit)
- ARPG mobile body / tooltip: 14–18px
- Pixi.js DPR note: Pixi v7/v8 does not auto-apply `devicePixelRatio` to Text objects. On a 3× DPI phone, a `fontSize:15` Text renders at 15 canvas-space pixels, which after CSS downscaling (canvas is 1800px wide, phone is 375px CSS) displays at ~3.1 CSS pixels — genuinely unreadable. The fix is to set font sizes high enough in canvas-space that after CSS scaling they read at the equivalent of the desired pt/dp value. **Formula:** `canvas_px = target_dp × (canvas_width / viewport_width_css) × DPI_scale_factor`. At 1800px canvas / 375px CSS viewport / 2× DPI: `canvas_px = target_dp × 4.8×`. A 14dp target = 67px canvas-space. This is why Matt reports "impossible to read" — current 9–15px canvas-space fonts render at 1.9–3.1 CSS pixels on a phone. The fix is a responsive font-size system that multiplies base sizes by ~5× on mobile. The exact multiplier varies by device; a reasonable conservative estimate for "normal 375px-CSS-width phone" is 5×.

| Text element | Desktop canvas-px | Recommended mobile canvas-px | Notes |
|---|---|---|---|
| Class name (in HUD / char sheet header) | 13px | 60–65px | Currently `nameT` in `characterSheet.ts` at 13px; bold |
| Class name (archetype label) | 10px | 48px | `archT` in characterSheet.ts at 10px |
| Element / energy descriptor line | 9px | 44px | `dimT` in characterSheet.ts at 9px |
| Gear name (inventory equipped card) | 11px bold | 52px bold | `nameLbl` in inventoryPanel.ts at 11px |
| Gear name (stash card) | 9.5px bold | 46px bold | `nameLbl` stash card at 9.5px |
| Gear flavor text (epic/legendary tooltip) | 8.5px italic | 40px italic | `ft` in `_makeCompareTooltip` at 8.5px |
| Spirit Guide signal | 8px | 38px | `sgLbl` at 8px |
| Skill name (hotbar tooltip, char sheet) | 10px | 48px | tooltip in characterSheet.ts |
| Skill name (TouchHotbar abbreviation) | 11px | 52px | currently shows element code, not name |
| Skill cost label (TouchHotbar) | 9px | 44px | `costLabel` in touchHotbar.ts |
| Damage number (normal hit) | 15px | 72px | `spawnFloatingNumber` at 15px |
| Damage number (crit) | 20px bold | 96px bold | spawnFloatingNumber crit at 20px |
| Damage number (miss) | 13px | 64px | spawnFloatingNumber miss at 13px |
| Heal number | 15px | 72px | same as damage normal |
| Status text ("Resisted!", etc.) | 12px | 58px | `spawnStatusText` at 12px |
| Combat log line text | 9.5px | 46px | `style` in combatLog.ts `_rebuild()` |
| Combat log toggle button | 9px | 44px | `label` in `_makeToggleBtn()` |
| Section headers (char sheet) | 9px letter-spaced | 44px | `_head()` / `_headWide()` in characterSheet.ts |
| Stat row values (char sheet) | 9px | 44px | `_row()` in characterSheet.ts |
| Globe numeric label (DiabloHud) | 13px bold | 60px bold | `_label` in diabloHud.ts |
| Hotbar cooldown label (TouchHotbar) | 14px | 68px | `cooldownLabel` in touchHotbar.ts |
| Key hint label ([Q], [E], [SHIFT]) | 8–9px | Hide on mobile or 40px | key hints are keyboard-irrelevant on mobile; hide or replace with icon |
| Inventory title "INVENTORY" | 12px | 58px | title in inventoryPanel.ts |
| "GAME PAUSED" note | 10px | 48px | pauseNote in inventoryPanel.ts |
| Close button label | 9px | 44px | close btn in characterSheet.ts |
| Wave status label | 13px | 62px | waveLabel in combatHud.ts CombatStatus |
| Phase/sub label | 10px | 48px | phaseLabel in combatHud.ts |
| Result overlay title (VICTORY/DEFEATED) | 48px | 96px | already large; mild boost for phone |
| Result overlay hint text | 16px | 76px | "Press R or click to try again" |

**Implementation architecture (Phase M1):**
Create `src/ui/typography.ts` exporting a single `font(basePx: number): number` function that returns `basePx` on desktop and `basePx * MOBILE_FONT_SCALE` on mobile. `MOBILE_FONT_SCALE` = 4.8 (conservative; calibratable). All `new TextStyle({ fontSize: N })` calls replace `N` with `font(N)`. Desktop rendering is pixel-identical (function returns basePx unchanged); mobile rendering reads correctly.

---

## § 6 — Panel redesigns

### § 6.1 — Combat log

**Desktop today:** Floating panel anchored to top-right (x=LOG_X, y=50). Width 280px, max 16 lines × 16px line height. Default closed (v1.5). Toggle via H key / top-right icon.

**Mobile redesign:**
- **Default closed**: preserved from v1.5.
- **Open state**: full-width bottom sheet occupying bottom ~40% of screen (y=570–944 in canvas space). Slides up from bottom edge when toggled. Dismisses by tapping outside the panel or tapping the toggle icon again.
- **Typography**: font scale per § 5 table (9.5px → ~46px canvas-space). At 46px, the panel fits ~8 lines in the 40% bottom-sheet area. Reduce MAX_LINES to 8 on mobile (or provide a scrollable view; Phase M5 calls this out).
- **Line height**: 46px font at 1.3 leading = ~60px per line. 8 lines × 60px = 480px — fits in the 374px bottom area only at reduced line count; recommend 6 lines visible at once with smooth scroll.
- **Scroll behavior**: on mobile, combat log content scrolls vertically (newest at bottom). Swipe-up within the panel scrolls older entries. Pixi does not have native scroll; implement via a masked Container with `y` offset driven by pointer drag within the panel bounds.
- **Dismissal**: tap outside the panel area OR tap the log icon again.
- **Open/close gesture**: tap top-row LOG icon (TouchIcons) — existing wiring.

### § 6.2 — Character sheet

**Desktop today:** 640×560 centered modal with two-column layout. Text 9–13px. Close via C key or close button.

**Mobile redesign:**
- **Full-screen modal**: occupy 90% of canvas area (1620×850 in canvas space, centered). Dark semi-transparent backdrop preserved.
- **Tab navigation**: instead of the two-column layout (CLASS IDENTITY / COMBAT STATS side by side), use two tabs — "STATS" and "ABILITIES". Tabs rendered as a top strip of two large buttons within the panel. Font scale per § 5.
- **STATS tab**: scrollable container. Sections: Class Identity → Base Attributes → Combat Stats → Element Resistances → Active State. All in single column. Content scrolls vertically (swipe gesture within panel).
- **ABILITIES tab**: scrollable list of skills (same `_skillRow` data but at mobile font size). No hover tooltips; long-press (400ms) on a skill row opens the skill tooltip as a sub-overlay.
- **Close gesture**: large "X" button at top-right (minimum 88px touch zone per gandalf floor). Tap or C key.
- **Pause indicator**: preserved — game is paused while char sheet is open.

### § 6.3 — Inventory panel

**Desktop today:** 700×500 centered modal. Two-section layout (equipped left, stash grid right). Text 8.5–12px. Long-press tooltip already wired via `_addLongPress` in inventoryPanel.ts.

**Mobile redesign:**
- **Full-screen modal**: occupy 90% of canvas area.
- **Tab navigation**: two tabs — "EQUIPPED" (4 gear slots, full-column cards) and "STASH" (2-column grid at mobile card sizes).
- **EQUIPPED tab**: 4 slot cards stacked vertically. Each card taller (≥120px canvas space) to accommodate mobile font sizes. Unequip button: minimum 88px touch zone.
- **STASH tab**: 2-column grid. Card size: ~220×120px canvas space (from current 86px height, scaled for readability). Equip button: 88px minimum touch zone. Gear name 46px bold. Spirit Guide signal 38px. Tier badge 38px.
- **Long-press tooltip**: existing `_addLongPress` wiring preserved. 400ms threshold unchanged. Tooltip text scaled to mobile font sizes.
- **Scroll behavior**: both tabs scroll vertically when content overflows. Same masked Container + pointer-drag scroll pattern as combat log.
- **Close gesture**: top-right X button (88px minimum). I key still works.
- **Gear tooltip position**: tooltip anchors to the card being long-pressed. Ensure it doesn't bleed off-screen edges (existing clamping logic in `_makeCompareTooltip` handles x; add y-clamp for mobile).

---

## § 7 — Phased execution plan

> **AMENDED 2026-05-17:** Phases M2-M7, when they fire VS2b, target **portrait-primary** viewport per § 4.3 amendment. Phase M1 (Typography foundation) is orientation-agnostic and is unchanged. Landscape support adaptations migrate to a polish-phase track; they are not in the v1 mobile target. Provenance: `agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md`.

### Phase M1 — Typography foundation

**What it does:** Establishes the font-size constants module (`src/ui/typography.ts`) and replaces all hardcoded `fontSize` values across `src/` with `font(N)` calls. Mobile receives scaled sizes per the § 5 table; desktop is pixel-identical.

**Files touched:**
- `src/ui/typography.ts` (new — ~30 lines)
- `src/abilities/vfx.ts` — `spawnFloatingNumber` (lines 68–70), `spawnStatusText` (line 92)
- `src/ui/combatLog.ts` — `_rebuild()` style (line 112), toggle button (line 80)
- `src/ui/combatHud.ts` — `CombatStatus` wave/phase labels (lines 831, 836); result overlay (lines 803, 810); skill tooltip (lines 349–354); cooldown label (line 557); key label (line 568)
- `src/ui/characterSheet.ts` — `_t()` helpers, `_head()`, `_row()`, `_skillRow()`, `_skillTooltip()`, all fontSize references (~20 call sites)
- `src/ui/inventoryPanel.ts` — title, section headers, card names, spirit guide labels, feedback label, button labels (~15 call sites)
- `src/ui/potionHud.ts` — count text (fontSize 17), key hints (fontSize 9)
- `src/ui/dashCooldownHud.ts` — cd label (fontSize 14), key hint (fontSize 8)
- `src/ui/diabloHud.ts` — globe numeric label (fontSize 13), type label (fontSize 8)
- `src/ui/hud.ts` — loading screen labels
- `src/mobile/touchHotbar.ts` — name abbreviation (11), cost label (9), badge (8), cooldown label (14)
- `src/mobile/touchTargetBtn.ts` — label (9)
- `src/mobile/touchPotions.ts` — count text (13)
- `src/mobile/touchIcons.ts` — no text labels currently; no changes needed here

**Line-count estimate:** ~200 lines changed (mostly 1-line font size replacements); ~30 lines added (typography.ts).

**Dependencies:** None. This phase is the unblocking prerequisite for all others.

**Risks:**
- MOBILE_FONT_SCALE hardcoded at 4.8 is a calibration estimate based on 375px CSS / 1800px canvas. Actual phones vary. The constant needs a playtest calibration pass (Phase M7 polish). 4.8 is "likely readable" not "perfectly tuned."
- Pixi.js Text objects with very large font sizes (72–96px canvas-space) may have rendering artifacts on some GPUs. Smoke test on actual phone required.
- Word-wrap widths in combatLog, characterSheet, inventoryPanel were tuned for small text in fixed-size panels. Mobile panels resize; word-wrap widths need mobile variants (tracked as a dependency in Phase M5).

**Smoke-test plan:**
- `npm run build` PASS (0 TS errors)
- Desktop dev server: launch demo, render one frame, confirm HUD/log/panels visually identical to pre-M1
- Mobile (375px viewport or real phone): confirm damage numbers, combat log, and skill tooltips are legible

---

### Phase M2 — Mobile dash button

**What it does:** Creates the missing dash touch button for mobile. Tapping it fires `_startDodge()` with cooldown indicator.

**Files touched:**
- `src/mobile/touchDashBtn.ts` (new — ~100 lines, pattern: touchTargetBtn.ts + DashCooldownHud running figure)
- `src/main.ts` — instantiate `_touchDashBtn` in `if (Mobile.isActive)` block; pass dash callback; call `_touchDashBtn.update()` in tick loop alongside `dashCooldownHud.update()`

**Line-count estimate:** ~100 lines new; ~15 lines in main.ts.

**Dependencies:** None on M1 (can ship independently); but M1 should ship first so button labels inherit mobile font scale.

**Risks:**
- Dash button placement at (1700, 840) is close to the resource globe (x=1724, y=880). On small phones after CSS downscaling, the visual gap between button and globe frame may appear tight. Adjust position in M2 if smoke test confirms overlap.
- On phones without orientation lock support, portrait-mode users see the orientation overlay (handled by orientationOverlay.ts). No M2 risk.

**Smoke-test plan:**
- Mobile: tap dash button → character performs dash animation, cooldown radial appears, button dims
- Confirm button does not overlap with ability arc or potion buttons in 375px viewport

---

### Phase M3 — Manual targeting (tap-to-lock)

**What it does:** Adds tap-to-directly-select an enemy on mobile. Tapping an enemy sprite locks it as the primary target. Visual target-lock ring appears around the locked enemy. Existing cycle button is preserved as fallback.

**Files touched:**
- `src/main.ts` — add tap-to-target handler in `if (Mobile.isActive)` section; render target-lock ring (procedural Graphics, redrawn each tick when `primaryActorIdx` is set and `Mobile.isActive`)

**Line-count estimate:** ~60 lines in main.ts.

**Dependencies:** None on M1/M2; can be developed in parallel. However, shipping after M1 is preferred so that any in-combat status text from the new targeting system inherits mobile font sizes.

**Risks:**
- Touch hit-testing must use gandalf's 75px forgiveness radius (vs desktop's 50px `CLICK_HIT_RADIUS`) because fingers occlude the target more than a cursor. This means large packs can have overlapping hit zones; resolve by "nearest enemy to tap point" semantics (same as click-to-attack today, just extend to target-lock first instead of attack-immediately).
- Target-lock ring must not be confused for an AOE indicator. Use a distinct visual style: dashed or double-stroke ring with the enemy's element color (not the AOE indicator's solid fill pattern).

**Smoke-test plan:**
- Mobile: tap visible enemy → lock ring appears, skills auto-engage that enemy when fired
- Tap a different enemy → lock transfers
- Locked enemy dies → system auto-advances to nearest alive enemy, lock ring transfers

---

### Phase M4 — Damage text and floating text legibility

**What it does:** Applies the M1 typography module specifically to damage/status floating text. M1 already replaces font sizes in `vfx.ts`; Phase M4 is the calibration and testing phase for that specific system, plus ensuring the spawn positions don't overlap the HUD zones defined in § 4.

**Files touched:**
- `src/abilities/vfx.ts` — verify M1 font scale applied correctly to `spawnFloatingNumber` and `spawnStatusText`; add `Mobile.isActive` guard to x-jitter range (current `(Math.random() - 0.5) * 28` is fine at PC scale; at 5× canvas-font, jitter should also be proportional — `jitter × MOBILE_FONT_SCALE`)
- `src/main.ts` — add HUD no-fly zone clamp to floating number spawn positions when `Mobile.isActive` (avoid x<200 and x>1400 for player-emitted text)

**Line-count estimate:** ~20 lines in vfx.ts; ~10 lines in main.ts.

**Dependencies:** M1 must ship first (M4 is a calibration + no-fly-zone pass on top of M1).

**Risks:**
- Very large font sizes (72–96px canvas-space) for crit numbers may visually crowd the gameplay field. MOBILE_FONT_SCALE may need a separate lower value for damage text specifically (e.g., 3.5× instead of 4.8×). Calibrate during smoke test.

**Smoke-test plan:**
- Mobile: fight a wave; confirm damage numbers are readable; confirm they do not overlap the skill arc or joystick; crit numbers are visibly larger than normal hits

---

### Phase M5 — Panel redesigns (combat log, char sheet, inventory)

**What it does:** Implements the three panel redesigns described in § 6. Full-screen modal layouts, tab navigation for char sheet and inventory, bottom-sheet for combat log, scrollable containers.

**Files touched:**
- `src/ui/combatLog.ts` — add `if (Mobile.isActive)` branch in constructor and `toggle()` for bottom-sheet layout; add scroll implementation
- `src/ui/characterSheet.ts` — add `if (Mobile.isActive)` branch; tab navigation; scrollable column layout; long-press on skill row for tooltip
- `src/ui/inventoryPanel.ts` — add `if (Mobile.isActive)` branch; tab navigation (EQUIPPED / STASH); scrollable stash grid; larger card heights

**Line-count estimate:** ~300 lines across the three files (largest phase).

**Dependencies:** M1 must ship first (font scale). M5 is independent from M2, M3, M4.

**Risks:**
- Pixi.js scroll implementation (masked Container + pointer drag) is custom code with no built-in momentum/elasticity. Needs careful pointer event handling (distinguish scroll drag from skill-fire tap). Pattern exists in `_addLongPress` — extend to a scroll gesture.
- Panel word-wrap widths need mobile-specific values. The current `wordWrapWidth` constants are tuned for the fixed panel widths (640px, 700px). Mobile full-screen panels are ~1620px wide; word-wrap needs to be set accordingly in the `if (Mobile.isActive)` path.
- Three-panel scope in one dispatch is large; if any single panel requires deep structural changes, consider splitting M5 into M5a (combat log) and M5b (char sheet + inventory) to keep dispatch size manageable.

**Smoke-test plan:**
- Mobile: open combat log → bottom sheet slides up; content readable; tap outside dismisses
- Mobile: open character sheet → full-screen modal; STATS and ABILITIES tabs work; scroll works
- Mobile: open inventory → full-screen modal; EQUIPPED and STASH tabs work; long-press tooltip works

---

### Phase M6 — Layout safe-area pass

**What it does:** Injects safe-area inset compensation so that joystick, dash button, potion buttons, and top-row icons are not obscured by notch / Dynamic Island / Android nav bar. Also performs a final layout audit of the bottom-right HUD cluster (skill arc, potion buttons, target-cycle button, dash button) to resolve any spacing collisions identified during M2–M4 smoke tests.

**Files touched:**
- `src/mobile/mobile.ts` — add `safeAreaInsets: {top, right, bottom, left}` property; populate via DOM probe at init
- `src/mobile/joystick.ts` — consume `Mobile.safeAreaInsets.bottom` + `Mobile.safeAreaInsets.left` to offset JOY_CY and JOY_CX
- `src/mobile/touchHotbar.ts` — consume `Mobile.safeAreaInsets.right` + `Mobile.safeAreaInsets.bottom` to offset BTN_POS array
- `src/mobile/touchIcons.ts` — consume `Mobile.safeAreaInsets.top` to offset ICON_Y
- `src/mobile/touchPotions.ts` — consume `Mobile.safeAreaInsets.right` + `Mobile.safeAreaInsets.bottom` to offset HP_X/HP_Y/MAN_X/MAN_Y
- `src/mobile/touchDashBtn.ts` (Phase M2) — consume insets
- `src/mobile/touchTargetBtn.ts` — consume `Mobile.safeAreaInsets.right`

**Line-count estimate:** ~80 lines across files.

**Dependencies:** M2 must ship first (touchDashBtn needs inset consumption). M6 is a pass across all mobile UI.

**Risks:**
- `env(safe-area-inset-*)` is a CSS variable; reading it from JavaScript requires a DOM probe (insert a hidden `<div>` with `padding: env(safe-area-inset-bottom)` and read back `getComputedStyle`). This pattern works on iOS Safari and modern Android Chrome but may return 0 on some browsers. Fallback: assume 0 inset (equivalent to current behavior).
- Conversion from CSS px insets to canvas-space units must account for the same scaling ratio used in `clientToCanvas()`. The formula is: `canvas_inset = css_inset × (CANVAS_WIDTH / canvas_rect.width)`. This must be computed after the canvas is rendered (not at module eval time).

**Smoke-test plan:**
- iPhone with notch or Dynamic Island: all HUD elements visible and not obscured
- iPhone without notch (older): behavior identical to pre-M6 (zero insets, no visual change)
- Android with nav bar: bottom HUD elements shift upward by nav bar height

---

### Phase M7 — Gesture polish

**What it does:** Calibration pass, long-press tooltip refinements, and any gap items surfaced during M1–M6 smoke tests. This is the "finish line" phase before VS2b mobile milestone.

**Contents:**
- MOBILE_FONT_SCALE calibration: adjust constant based on playtest feedback from M1/M4 smoke tests; per-element scale overrides if some text types need different scaling
- Long-press tooltip improvements: consistent tooltip panel style across inventory items, skill rows, and any new long-press targets added in M5
- TouchIcons ICON_R resize: from current r=26 to r=44 (88px diameter per gandalf canon § 3.2 table) — this was deferred from initial M1 scope to keep phases clean; belongs in M7 alongside other size-refinement items
- TouchPotions HIT_R resize: from HIT_R=38 to ~HIT_R=50 per gandalf canon; POT_R ~35
- Joystick minor refine: R_OUTER 80→75, R_INNER 30→28 per gandalf canon
- Double-tap and pinch: confirm these are not accidentally triggering any behavior; add explicit `preventDefault()` guards if needed
- Install hint timing: confirm `Mobile.showInstallHint()` delay (4000ms) is appropriate; adjust if needed

**Files touched:** `src/mobile/touchIcons.ts`, `src/mobile/touchPotions.ts`, `src/mobile/joystick.ts`, `src/ui/typography.ts` (MOBILE_FONT_SCALE value), any files from M1–M6 with smoke-test feedback items.

**Line-count estimate:** ~100 lines total (scattered small adjustments).

**Dependencies:** All of M1–M6 must ship.

**Smoke-test plan:**
- Full mobile playthrough, landscape phone, real device if possible
- All text legible
- All touch targets hit reliably
- No HUD overlap
- Dash, targeting, skills, potions all operational
- No unintended double-tap or pinch behavior

---

## § 8 — Out-of-scope deferrals

These items surfaced during planning and are explicitly deferred to post-mobile-V1 or separate workstreams:

| Item | Reason deferred |
|---|---|
| Native shell wrapper (Capacitor / Cordova) | Separate workstream; deployment infra decision (Matt-gated). Phase-2-of-mobile. |
| Haptic feedback | Phase-3 polish; requires native shell or Vibration API; not blocking demo playability |
| Push notifications | Out of demo scope entirely |
| Platform store submission (iOS App Store / Google Play) | Separate workstream; legal/billing/review pipeline; not a drax concern |
| Anti-cheat / device fingerprinting | Out of demo scope |
| Tap-to-move (alternative to joystick) | Conflicts with tap-to-target gesture (§ 3.4 vocabulary). Joystick-only is the locked recommendation (dual-stick ARPG canon). If Matt wants tap-to-move as an option, it requires a separate gesture-vocabulary decision and a new dispatch. |
| Camera zoom-in (1.33× per gandalf canon § 3.4) | Load-bearing world-scale change; affects all rendering not just UI. Separate dispatch required; involves sprite-shrink via `WORLD_SCALE_MOBILE` constant. Deferred to post-M7. |
| World-sprite shrink (0.75× per gandalf canon § 3.1) | Same as camera zoom; tied to world-scale implementation; separate dispatch. |
| HP/MP globe merge with potion button | Gandalf § 7 Q1 open question. Recommend deferring until Matt decides (DI-style merge vs. separate). Current separate approach works on mobile. |
| iPad / tablet layout | Out of scope (gandalf notes 0.85–0.90× scalar vs phone's 0.75×); separate commission when iPad becomes target. |
| Portrait mode support | Orientation-locked to landscape; not planning to change without Matt direction. |
| Gear drop tap interaction (on-ground items) | Current auto-pickup (1.8s) makes this less urgent. Tap-to-inspect gear drops would be a separate Phase-M-followon item. |

---

## § 9 — Coordination notes with gandalf commission

Gandalf's commission (`2026-05-17-gandalf-mobile-pc-pixel-sizing-ratios-commission.md`) shipped before this commission completed. The plan document at `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` is authoritative and has been fully consumed. No `<gandalf-pending>` placeholders remain.

**Key numbers consumed from gandalf:**

| Parameter | Gandalf canon | Used where in this plan |
|---|---|---|
| Ability touch target diameter | 120px (radial arc) | TouchHotbar BTN_R target; Phase M7 notes |
| Potion button touch zone | 140px diameter | TouchPotions HIT_R refine target; Phase M7 |
| Top-row icon touch zone | 88px diameter floor | TouchIcons ICON_R refine; Phase M7 |
| Dash icon touch zone | 110px | TouchDashBtn HIT_R=55; Phase M2 |
| Touch forgiveness radius | 75px | Phase M3 tap-to-target hit zone |
| Joystick outer | 150px (r=75) | Phase M7 minor refine |
| Joystick inner | 56px (r=28) | Phase M7 minor refine |
| Sprite shrink scalar | 0.75× | Camera/world-scale deferred (§ 8) |
| Camera zoom | 1.33× | Camera/world-scale deferred (§ 8) |
| PIXELS_PER_METER | 48 — UNCHANGED | Confirms no engine-side changes needed for mobile |

**Legolas Mode B sub-commission** (`agentic_orchestration/research/commissions/2026-05-17-gandalf-to-legolas-mobile-arpg-pixel-survey.md`) is in-flight per gandalf's note. If Legolas returns values that shift cluster centroids by ±15% or more, gandalf authors a v1.7b refinement. Drax consumes any table updates during Phase M7 calibration. No blocker.

---

## § 10 — Risks and open questions for Matt

### Risks

**R1 — MOBILE_FONT_SCALE calibration.** The 4.8× scale factor is computed for a 375px-CSS-width phone at 2× DPI. Actual phones range from 360px to 430px CSS width at 2× and 3× DPI. A single multiplier will be slightly off on any given device. Mitigation: Phase M7 is a calibration pass. Intermediate phases use 4.8× as a "definitely readable" value; it may render text slightly large on some phones — preferable to too small.

**R2 — Pixi.js large-text rendering.** Very large Pixi Text objects (72–96px canvas-space) can exhibit subpixel aliasing on some GPU/browser combinations. If this surfaces during smoke tests, the fix is to use Pixi's `resolution` property on the Text object (set to `window.devicePixelRatio`). This is a known Pixi pattern but adds a small GPU memory overhead per text object. Manageable.

**R3 — Panel scroll implementation (Phase M5) is custom code.** There is no built-in Pixi scroll widget. The masked-Container + pointer-drag-to-scroll pattern is doable but requires careful event handling to not conflict with skill taps and long-press tooltips. If Phase M5 runs long, split into M5a/M5b.

**R4 — Right-thumb cluster crowding.** The bottom-right quadrant is doing a lot of work: 6 skill buttons in arc + 1 dash button + 2 potion buttons + 1 target-cycle button + 1 resource globe. On a small phone this cluster may be difficult to navigate without mis-taps even with proper touch zones. The Phase M6 layout pass and M7 calibration should surface this. May require a layout rethink (e.g., merge potions into a smaller cluster, or move target-cycle to the top-right area) based on real playtest.

**R5 — HP/MP globe vs potion-button merge (open design question).** Gandalf § 7 Q1 raises this: Diablo Immortal merges the HP globe with the potion-tap affordance. If Matt wants this on mobile, it changes Phase M2/M6 scope. Current plan keeps them separate (preserving existing architecture). Drax can implement the merge; it would replace TouchPotions with a merged globe-tap system.

### Open questions for Matt

**Q1 — When should mobile implementation begin?** This plan targets VS2b territory. If Matt wants to accelerate any phase into VS2a, Phase M1 (typography foundation) is the safest acceleration candidate — it's purely additive (no behavioral change on desktop), and its output enables all subsequent phases.

**Q2 — HP/MP globe + potion-tap merge?** See R5 above. Diablo Immortal does this; it saves right-thumb real estate. Drax recommends leaving it separate for now (simpler, working, established UX), but Matt should weigh in before Phase M2/M6 locks the layout.

**Q3 — Dungeon of Exile reference playtest?** Gandalf § 7 Q5 surfaces this. If Matt has recent Dungeon of Exile mobile experience, a paragraph on what specifically feels right would let Drax tune layout and feel toward that target rather than the Diablo Immortal centroid.

**Q4 — Skill name vs element abbreviation in TouchHotbar?** Current TouchHotbar shows 3-letter element code (e.g., "FIR", "WAT") instead of skill name. This is compact and works at 42px button radius. Post-M1 typography scale, the button is larger; a 2–4 character skill-name abbreviation would fit. Matt's call on whether skill name or element label is more useful to see at a glance.

**Q5 — Phase M5 split decision?** If the panel redesigns in Phase M5 feel too large for a single dispatch, recommend splitting: M5a = combat log (simpler), M5b = char sheet + inventory (heavier). Would rather split than underdeliver.

---

*Authored 2026-05-17 by drax. Plan doc filed. Tag `drax/v1.6-mobile-ux-research-and-plan-1` to follow. Awaiting Matt's authorization to proceed with Phase M1 dispatch when VS2b window opens.*
