# 2026-05-17 — drax-demo — Mobile UX/UI research and execution-plan commission

**Authority:** Matt L3 commissioned 2026-05-17 (~16:30 EDT).
**Type:** Pattern B — research + engineering-plan commission (no production code in this dispatch; planning artifact only).
**Estimated effort:** ~1-2 days (audit + research synthesis + phased plan authoring).
**Predecessor:** drax v1.5 combat-log icon + spacebar dash (in flight at commission time).
**Sibling commission:** gandalf mobile-vs-PC pixel sizing & ratio research (`2026-05-17-gandalf-mobile-pc-pixel-sizing-ratios-commission.md`). The two commissions are complementary — gandalf provides the **sizing canon** (what dimensions everything should be on mobile); this commission provides the **engineering plan** (what files change, what new systems are needed, what order to execute). Both feed an eventual implementation dispatch.
**Scope window:** Forward-looking; output feeds future mobile execution in **VS2b territory or later** — not VS2a-gating. Plan now, execute when scheduled.

---

## Why this matters

Demo1 playtest revealed multiple mobile-killing gaps:
1. **Touch controls missing or partial** — there's `src/mobile/` infrastructure (joystick, touchHotbar, touchIcons, touchPotions, touchTargetBtn) but it doesn't cover dash, doesn't allow precise enemy targeting on touch, and auto-targets sub-optimally
2. **Screen layout designed for PC viewport** — icons and art crowd / overlap on phone aspect ratios
3. **Text completely unreadable on mobile** — class names, gear names, flavor text, damage numbers, combat log all sized for desktop and impossibly small on phone screens (Matt's direct: "humans could not possibly read any of the class names, gear names, flavor text, damage text, combat log. All of it was WAY too small on mobile")

The fix isn't a one-line CSS bump — it's a coordinated rework across input, layout, typography, and panel design. This commission produces the **plan**, decomposed into phases, so when execution fires (post-VS2a) drax executes a known-shape rollout instead of discovering scope mid-flight.

---

## Required reading (drax, before scoping)

1. `reincarnated-demo/src/mobile/` — full inventory: joystick.ts, mobile.ts, orientationOverlay.ts, touchHotbar.ts, touchIcons.ts, touchPotions.ts, touchTargetBtn.ts. **Read every file.** Write a per-file capability summary in the plan output.
2. `reincarnated-demo/src/main.ts` — search all `Mobile.isActive` branch points (you have ~15 across the file). Catalogue what's gated on mobile vs desktop today; this is your starting matrix.
3. `reincarnated-demo/src/ui/` — every panel: combatLog, charSheet, inventoryPanel, hotbar, potionHud, desktopHudIcons, dashCooldownHud, diabloHud, combatHud. For each: current font sizes, panel dimensions, mobile-readiness assessment.
4. `reincarnated-demo/src/data/` — damage-number rendering, floating-text rendering (search `FloatingText`, `damageText`); typography pipeline if any
5. Gandalf mobile pixel sizing commission (sibling, in flight): `agentic_orchestration/dispatches/2026-05-17-gandalf-mobile-pc-pixel-sizing-ratios-commission.md` — your plan should consume gandalf's eventual sizing table; reference it as upstream input
6. Any historical Matt feedback on mobile-1 playtest (search `mobile` + `playtest` in canonical/ + decisions-log)

---

## Scope

### Item 1 — Mobile-gap audit

Produce a **gap matrix** of what exists vs what's missing for full mobile coverage:

| Capability | Desktop today | Mobile today | Gap |
|---|---|---|---|
| Movement input | WASD | Virtual joystick | ✅ shipped (verify works) |
| Targeting | Mouse hover | Auto-target nearest | ❌ no manual touch-target |
| Dash | Space (v1.5) | (none) | ❌ no mobile dash button |
| Skill activation | Number keys / hotbar click | Touch hotbar | ✅ shipped (verify) |
| Potion use | Q/W or click | Touch potion icons | ✅ shipped |
| Panel open (Char/Inv/Log) | Keys C/I/H + icon click | Touch icons | Partial (verify icons exist and panels fit screen) |
| Damage text | Floating overlay | (inherits desktop) | ❌ unreadable size |
| Combat log | Floating panel | (inherits desktop) | ❌ unreadable size |
| Character sheet | Modal panel | (inherits desktop) | ❌ doesn't fit screen |
| Inventory panel | Modal panel | (inherits desktop) | ❌ doesn't fit screen |
| Gear tooltip | Hover | (none on touch) | ❌ no tap-and-hold tooltip |

(Above is illustrative; fill in real values from your audit.)

### Item 2 — Touch input architecture

For each input gap, propose a touch pattern grounded in mobile ARPG canon (Diablo Immortal, Torchlight Infinite, Eternium):

- **Targeting:** propose the canonical touch-target system. Common patterns:
  - **Tap-to-target then tap-to-attack** (Diablo Immortal)
  - **Tap-enemy-to-lock then auto-engage** (Eternium)
  - **Drag-to-cycle-target** (Torchlight Infinite mobile)
  - Recommend one; document the decision and the rejected alternatives
- **Dash:** mobile dash icon — placement (bottom-right cluster near skills, away from joystick? thumb-reach analysis), glyph (running figure consistent with desktop), input gesture (tap vs swipe). Consume `dashCooldownHud.ts` patterns from drax v1.3/v1.4.
- **Manual movement vs auto-pathing:** virtual joystick exists; assess whether tap-to-move is also needed (D-Immortal supports both). Recommend the binding.
- **Gesture vocabulary:** what gestures are reserved? (single-tap = primary attack/target; double-tap = ???; long-press = ???; two-finger pinch = camera zoom?). Propose a complete gesture-input contract.

### Item 3 — Screen layout remap

Define the mobile HUD layout (consume gandalf's sizing canon when available; reference it as a placeholder until then):

- **Safe areas:** iPhone notch / Dynamic Island, Android navigation bar, gesture-area inset on home-button-less devices
- **HUD zones:**
  - Top: minimal info bar (HP, resource, level)
  - Bottom-left: virtual joystick (left-thumb zone)
  - Bottom-right: skill hotbar + dash + potions (right-thumb zone)
  - Top-right: icon cluster (Inventory, Character, Log)
  - Mid-screen: clear for gameplay; damage text overlays here
- **Anti-overlap rules:** define no-fly zones (e.g., character sprite vertical column stays clear of HUD; floating damage text avoids hotbar zone)
- **Orientation:** demo currently uses orientationOverlay.ts (presumably forces landscape). Validate; propose any orientation-related changes
- Produce an ASCII / box-diagram of the mobile HUD layout

### Item 4 — Typography & text legibility

The biggest Matt-flagged gap. For each text element produce minimum mobile font size + style:

| Element | Current PC px | Recommended mobile px | Notes |
|---|---|---|---|
| Class name (in HUD) | ? | ?? | |
| Class name (in selection) | ? | ?? | |
| Gear name (inventory) | ? | ?? | |
| Gear flavor text | ? | ?? | |
| Skill name (hotbar tooltip) | ? | ?? | |
| Damage number (default) | ? | ?? | |
| Damage number (crit) | ? | ?? | |
| Combat log line | ? | ?? | |
| Status text (e.g., "burning") | ? | ?? | |

Reference points:
- Apple HIG minimum text: 11 pt = ~14 px (and 17 pt = ~22 px for body)
- Material Design body minimum: 14 sp
- ARPG mobile canon: damage text typically 20-32 px on mobile (D-Immortal); body 14-18; tooltip 16-20

Where Pixi.js text rendering is used, document any DPR (device-pixel-ratio) caveats — Pixi has subpixel-rendering pitfalls on mobile that demo1 may have hit.

### Item 5 — Panel redesign — char sheet, inventory, combat log

For each panel currently designed for desktop, propose the mobile variant:

- **Combat log:** desktop = floating bottom-corner panel; mobile = ? (full-screen modal? bottom-sheet that swipes up? full-screen tab?). Default-closed (per v1.5) carries forward.
- **Character sheet:** desktop = modal overlay; mobile = full-screen modal with tab navigation; legible typography per Item 4
- **Inventory panel:** desktop = grid + tooltip on hover; mobile = grid + tap-and-hold tooltip (the gesture vocabulary needs to define this); grid sizing per gandalf's icon sizing canon

Each panel proposal includes: open/close gesture, scroll behavior, dismissal, accessibility notes.

### Item 6 — Phased execution plan

Decompose the work into phases small enough that each is a single drax dispatch (~0.5-2 days). Order by dependency:

**Suggested phasing (drax tunes):**

- **Phase M1 — Typography foundation:** font-size constants module; consume gandalf's sizing canon; replace all hardcoded `fontSize` in src/ with the constants
- **Phase M2 — Mobile dash button:** touch button rigged to existing `_startDodge()`; cooldown indicator matching desktop pattern
- **Phase M3 — Manual targeting:** tap-to-target system; visual target-lock indicator; auto-target fallback when no manual lock
- **Phase M4 — Damage text & floating text legibility:** mobile-sized variants per Item 4 table
- **Phase M5 — Panel redesigns:** combat log mobile layout; char sheet mobile layout; inventory mobile layout
- **Phase M6 — Layout safe-area pass:** notch / nav-bar / safe-area-inset CSS or runtime equivalent; HUD positioning re-pin
- **Phase M7 — Gesture polish:** long-press tooltips; double-tap reserved gestures; pinch-zoom if scoped in

For each phase: file list, line-count estimate, dependencies, risks, smoke-test plan.

### Item 7 — Out-of-scope deferrals

Note any items that surface during planning that should defer to post-mobile-V1:
- Native shell wrapper (Capacitor / Cordova) — likely Phase-2-of-mobile, separate dispatch
- Push notifications / haptic feedback — phase-3 polish
- Platform store submission (iOS App Store / Google Play) — separate workstream
- Anti-cheat / device fingerprinting — out of demo scope

List these to capture them; the plan focuses on **playable mobile demo**.

### Item 8 — Coordination with gandalf commission

The plan should cite gandalf's mobile pixel sizing canon as upstream input. If gandalf's commission lands first, plug those numbers in. If your commission lands first, leave `<gandalf-pending>` placeholders in the sizing tables; the implementation dispatch fills them when both research artifacts converge.

### Item 9 — Output structure

File the plan at `canonical/story/mobile-ux-execution-plan-2026-05-17.md` (or your chosen canonical path).

Sections:
1. Executive summary (1 paragraph)
2. Mobile-gap audit matrix (Item 1)
3. Touch input architecture (Item 2)
4. Screen layout remap with diagram (Item 3)
5. Typography table (Item 4) — placeholders OK if gandalf still in flight
6. Panel redesigns (Item 5)
7. Phased execution plan (Item 6)
8. Out-of-scope deferrals (Item 7)
9. Coordination notes with gandalf commission (Item 8)
10. Risks / open questions for Matt

### Item 10 — Hive log + tag

- STATE entry with plan summary (phase count; gap matrix verdict; phase-1 entry point)
- Tag `drax/v1.6-mobile-ux-research-and-plan-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT write production code for any of these phases (planning artifact only; implementation fires when scheduled)
- ❌ DO NOT extend scope to native-shell wrapping, App Store submission, or anti-cheat
- ❌ DO NOT touch desktop UX (this commission produces mobile-side strategy only)
- ❌ DO NOT lock specific timing (mobile execution is post-VS2a; this commission produces the plan so a future dispatch can execute on a known shape)
- ❌ DO NOT change gandalf's commission scope; reference and consume only

---

## Acceptance criteria

- [ ] Mobile-gap audit complete (full per-file capability inventory)
- [ ] Touch input architecture documented (targeting, dash, movement, gesture vocabulary)
- [ ] Screen layout remap with diagram authored
- [ ] Typography table populated (with `<gandalf-pending>` placeholders if needed)
- [ ] Panel redesigns proposed (combat log, char sheet, inventory; default behaviors + gestures)
- [ ] Phased execution plan with file lists + estimates
- [ ] Out-of-scope deferrals listed
- [ ] Gandalf coordination notes captured
- [ ] Risks / open questions surfaced for Matt
- [ ] Canonical plan doc filed
- [ ] Tag `drax/v1.6-mobile-ux-research-and-plan-1`
- [ ] Hive-log STATE entry

---

## Smoke expectation

Matt reads the plan + diagram + phase list; can decide:
- Approval to proceed with phase M1 when scheduled
- Any phase reordering or de-scoping
- Whether to begin implementation pre-VS2a (likely no; post-VS2a is the target)

Drax holds the plan as authoritative; subsequent implementation dispatches reference it phase-by-phase.

---

## Coordination notes

- **No legolas sub-commission needed** — this is engineering plan, not external research; gandalf's parallel commission handles the genre-canon research input
- **No code changes** — research + plan artifact only
- **Hive log discipline:** PRE-SIGNAL per § 14.1.1 before hive-log appends
- **Verify the gandalf commission completion record before finalizing the typography table** — if gandalf ships first, your numbers are live; if not, placeholders are explicit

---

*Commissioned 2026-05-17 by knight-rider per Matt L3. ~1-2 days. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 by drax
**Tag:** `drax/v1.6-mobile-ux-research-and-plan-1`
**Plan artifact:** `/Users/admin/Games/reincarnated-collaboration/canonical/story/mobile-ux-execution-plan-2026-05-17.md`

**Acceptance criteria status:**
- [x] Mobile-gap audit complete (full per-file capability inventory — plan § 2.1)
- [x] Touch input architecture documented (targeting: Eternium tap-to-lock; dash: new touchDashBtn.ts; movement: dual-stick locked; gesture vocabulary: complete 8-row contract — plan § 3)
- [x] Screen layout remap with ASCII diagram authored (plan § 4.2)
- [x] Typography table populated — gandalf canon live, no placeholders (plan § 5)
- [x] Panel redesigns proposed (combat log: bottom-sheet; char sheet: full-screen tabs; inventory: full-screen tabs; all with gestures — plan § 6)
- [x] Phased execution plan with file lists + estimates (M1-M7; plan § 7)
- [x] Out-of-scope deferrals listed (11 items — plan § 8)
- [x] Gandalf coordination notes captured (plan § 9; sizing canon fully consumed)
- [x] Risks / open questions surfaced for Matt (5 risks, 5 questions — plan § 10)
- [x] Canonical plan doc filed at `canonical/story/mobile-ux-execution-plan-2026-05-17.md`
- [x] Tag `drax/v1.6-mobile-ux-research-and-plan-1`
- [x] Hive-log STATE entry (phase-1-p1-log.md)

**Key findings for Matt:**
Gandalf's sizing canon was complete before drax's commission finished — all `<gandalf-pending>` slots resolved with live numbers. The MOBILE_FONT_SCALE calculation shows why the demo1 playtest was unreadable: 9-15px canvas-space text renders at 1.9-3.1 CSS pixels on a 375px phone. The fix is a 4.8x scale factor applied via a new `typography.ts` constants module (Phase M1). Phase M1 is the safe VS2a-adjacent acceleration candidate if Matt wants to pull any phase forward — it is additive only with no desktop behavior change.

No production code was written. All implementation is gated on Matt's authorization to proceed with Phase M1 dispatch.
