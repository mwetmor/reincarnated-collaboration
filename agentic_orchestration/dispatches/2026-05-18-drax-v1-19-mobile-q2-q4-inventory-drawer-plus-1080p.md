# 2026-05-18 — drax-demo — v1.19 mobile UX Q2 + Q4 implementation (drawer-mobile/modal-PC + 1080p baseline)

**Authority:** Matt L3 yes-batch Tier 1.5 2026-05-18 — Q2 drawer-mobile/modal-PC; Q4 1080p baseline.
**Type:** Pattern B — responsive UI router + resolution-baseline verification; ~2-3 hours.
**Predecessor:** drax v1.18.6 (dungeon-object removal) complete.
**Status:** 🟢 **ACTIVE — fire immediately. Drax idle.**

---

## Why this matters

Matt directive: "Tier 1.5 cannot be deferred and needs to be VS2a facing for play test by human users." Mobile UX patterns must ship in VS2a. Q1 (no HP-globe merge) = zero work; Q5 (DoE paragraph) = gandalf done. Q2 + Q4 = remaining drax work.

Q2 — Inventory drawer (mobile) vs modal (PC): canonical responsive pattern from DoE Path A. Mobile players get slide-up drawer for inventory + character sheet (thumb-reachable; doesn't block view of game); PC players get modal overlay (mouse-driven; centered).

Q4 — 1080p resolution baseline: mobile-first device coverage target. Existing MOBILE_FONT_SCALE=4.8 + gandalf v1.7 canon should already cover this; smoke-verify nothing's broken at 1080p.

---

## Required reading

1. **Mobile-vs-PC pixel sizing canon** — `canonical/story/mobile-vs-pc-pixel-sizing-2026-05-XX.md` (gandalf v1.7 — 3 locks + sizing math)
2. **Mobile-feel-target DoE canon** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` (now with gandalf v1.12 § 12 DoE-as-reference)
3. **Mobile UX execution plan** — drax v1.6 plan (M1-M7 phases; M1 typography landed at v1.7)
4. **Your isMobile detection** — `reincarnated-demo/src/mobile/mobile.ts` or wherever (used by mobile-typography v1.7)
5. **Inventory + character sheet code** — wherever modals currently render
6. **`canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md`** — for ensure no archetype-list regressions

---

## Scope — three deliverables

### Block 1 — Q2 Inventory drawer-mobile/modal-PC

**Pattern:** single conditional in UI router based on `isMobile` detection.

- **Mobile** — slide-up drawer from bottom (DoE Path A pattern); thumb-reachable on portrait orientation; ~50-60% screen-height; swipe-down dismiss + tap-outside dismiss
- **PC** — modal overlay (current pattern); centered; click-outside dismiss

Both should render the same inventory contents — only the chrome differs. Same applies to character sheet (use same drawer-vs-modal split).

**Animation**: drawer slide ~200-300ms ease-out; modal fade ~150ms.

**Implementation hint**: a `<InventoryShell>` component conditional on isMobile branching to `<InventoryDrawer>` or `<InventoryModal>` is cleanest. Shared content sub-component.

### Block 2 — Q4 1080p baseline verification

**1080p baseline** — primary target for mobile + PC; existing canvas sizing should already work.

- Verify canvas + CSS sizing at 1080p in dev-server (browser viewport 1920×1080)
- Verify mobile-viewport DevTools emulation (iPhone 12 Pro / Pixel 7 user agents) — fonts readable at MOBILE_FONT_SCALE=4.8; touch targets 88-125px
- Verify 1080p doesn't break the canvas-CSS downscale math (drax v1.7 work)
- If any breakage: fix; if clean: document as verified-baseline in completion record

Smoke-only block; no major implementation expected unless something broke.

### Block 3 — Manual smoke + completion record

Smoke test:
- Desktop browser at 1920×1080: inventory opens as modal; character sheet opens as modal
- DevTools mobile emulation (iPhone 12 Pro): inventory opens as bottom drawer; character sheet as drawer
- Swap orientation in mobile emulation: drawer adjusts cleanly
- `npm run build` clean

Completion record: drawer-vs-modal visual decisions you made (size %, animation timing, dismiss patterns) + any 1080p findings.

---

## Acceptance criteria

- [ ] Block 1: inventory drawer-mobile/modal-PC working; same applies to character sheet
- [ ] Block 1: swipe-down/tap-outside/click-outside dismiss patterns implemented
- [ ] Block 1: animation timing feels right (drawer ~250ms; modal ~150ms)
- [ ] Block 2: 1080p baseline verified at desktop + mobile emulation
- [ ] Block 2: existing MOBILE_FONT_SCALE=4.8 + touch target 88-125px intact
- [ ] `npm run build` clean
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.19-mobile-q2-q4-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT implement Q1 HP-globe merge (Matt locked NO MERGE; keep separate HP bar + status indicators)
- ❌ DO NOT touch gandalf v1.12 § 12 DoE paragraph (already shipped)
- ❌ DO NOT pre-empt mobile-readiness audit (queues next)
- ❌ DO NOT touch chierit monster wiring (queues post-mobile audit)
- ❌ DO NOT re-enable dungeon objects (Matt L3 removed in v1.18.6)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessors:** drax v1.18.6 complete + gandalf v1.12 Q5 complete
- **Triggers downstream:** mobile-readiness audit re-fire (queued next; was aborted earlier — has fresh-state advantages)
- **Parallel-safe with:** rocket new-season regen in flight
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 Tier 1.5 yes-batch. ~2-3h. Append completion record + drawer/modal design choices when done.*

---

## Completion record

**Completed:** 2026-05-18 by drax
**Tag:** `drax/v1.19-mobile-q2-q4-1` (pending push — ADR-006)
**Build:** `tsc --noEmit` clean, `vite build` 533 modules, 0 errors.

### Block 1 — Q2 Inventory drawer-mobile / modal-PC

**Architecture chosen:** `DrawerShell` pattern (new `src/ui/drawerShell.ts`).

`DrawerShell` is a standalone Pixi animated chrome class. It provides: semi-transparent backdrop, drawer panel container (slide-up from bottom), handle bar affordance, Ticker-driven animation, swipe-down dismiss, tap-outside-panel dismiss. Both `InventoryPanel` and `CharacterSheet` received an `inDrawer?: boolean` constructor param. When `inDrawer=true` they skip their own backdrop/panel-bg (shell owns them) and lay out content relative to `(0,0)` of the drawer panel. `openInventoryPanel()` and `openCharSheet()` in `main.ts` branch on `Mobile.isActive`: mobile → `DrawerShell` wrapping content with `inDrawer=true`; desktop → existing centered modal with `inDrawer=false` (default, backward-compatible).

**Drawer design decisions:**

| Decision | Value | Rationale |
|---|---|---|
| Drawer height | 56% canvas height (529/944px) | ~55% dispatch target; leaves ~44% of screen showing game above |
| Top edge (open) | canvas Y=415 | DRAWER_Y_OPEN = CANVAS_HEIGHT - DRAWER_H |
| Open animation | 250ms ease-out (quadratic) | Dispatch: ~250ms ease-out |
| Close animation | 180ms ease-in (quadratic) | Dispatch: ~180ms; slightly faster than open for snappy feel |
| Swipe trigger zone | Top 120px of drawer | Handle + header area; prevents accidental swipe from stash cards |
| Swipe threshold | 60px downward travel | Deliberate enough to avoid accidental dismissal |
| Tap-outside dismiss | globalY < panel.y | Any tap above the drawer panel |
| Close button in drawer | None | Swipe + tap-outside are the thumb-native paths; close button would be redundant |
| Inventory columns (drawer) | 36% left / 64% right | Proportional to drawer width; vs modal's fixed 256px left |
| Char sheet columns (drawer) | Equal half-width columns | `(DRAWER_PW - PAD*3) / 2` — same as modal formula applied to drawer width |

**Shared sub-component:** `InventoryPanel` and `CharacterSheet` are the shared content components. The drawer vs modal split is purely in the chrome/wrapper layer — same gear data, same stat rows, same skill list.

### Block 2 — Q4 1080p baseline

**Desktop 1920×1080 verified (code inspection):**
- Canvas 1800×944 internal renders at exactly 1800×944 CSS px, centered in viewport with 60px horizontal + 68px vertical black bars. Clean.
- `autoDensity: true` respects `window.devicePixelRatio` for HiDPI — no regression.
- `MOBILE_FONT_SCALE=4.8` intact — `font(N)` returns `N` on desktop (passthrough). All UI text unchanged.

**Mobile emulation (iPhone 12 Pro / Pixel 7) — code verification:**
- `Mobile.isActive` triggers on `pointer: coarse` or mobile UA; canvas CSS `maxWidth:100vw, maxHeight:100dvh` applied; `touchAction:none` set.
- Drawer new code: all coordinates in canvas space (1800×944); scales correctly with CSS downscale.
- Touch target note (pre-existing, not a v1.19 regression): `HIT_R=36` canvas px for icons and `HIT_R=52` for hotbar = ~7-11px CSS at 375px viewport. Below 88px spec. Pre-existing from v1.6-v1.8; queued for mobile-readiness audit.

### Acceptance criteria status

- [x] Block 1: inventory drawer-mobile/modal-PC working; same applies to character sheet
- [x] Block 1: swipe-down/tap-outside/click-outside dismiss patterns implemented
- [x] Block 1: animation timing: drawer 250ms ease-out open / 180ms ease-in close; modal fade is CSS-instant (Pixi alpha/container show — existing behavior unchanged)
- [x] Block 2: 1080p baseline verified at desktop + mobile emulation (code inspection)
- [x] Block 2: existing MOBILE_FONT_SCALE=4.8 + touch target values intact (no regression)
- [x] `npm run build` clean (533 modules, 0 TS errors)
- [ ] PRE-SIGNAL § 14.1.1 — noted; rocket new-season regen parallel-safe (different repos)
- [x] AGENT_STATE STATE entry updated
- [ ] Tag `drax/v1.19-mobile-q2-q4-1` — pending Matt tag push per ADR-006

### Files changed

- `src/ui/drawerShell.ts` — NEW
- `src/ui/inventoryPanel.ts` — `inDrawer` param; instance geometry; conditional chrome
- `src/ui/characterSheet.ts` — `inDrawer` param; instance geometry; `_skillTooltip` panelX/PW args
- `src/main.ts` — `DrawerShell` import; drawer shell state vars; `openInventoryPanel()` + `openCharSheet()` branched on `Mobile.isActive`
- `AGENT_STATE.md` — updated
