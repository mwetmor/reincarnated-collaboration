# 2026-05-18 — drax-demo — Mobile-readiness audit (QUEUED post-v1.17)

**Authority:** Matt L3 verdict 2026-05-18 — authorize when drax unblocked from v1.17 and no other priorities. DoE Path A mobile-feel target locked; pre-VS2a-sign-off mobile state needs characterization.
**Type:** Pattern A — audit + characterization + v1.18 follow-on scoping; ~1-1.5 hours.
**Predecessor (gates auto-fire):** drax v1.17 completion (auto-cast + dungeon objects + is_retired filter + abilities→skills rename).
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until drax v1.17 ships completion record. Knight-rider activates post-v1.17 + when no higher-priority drax work has been queued.**

---

## Why this matters

Demo has been built with mobile-first framing since drax v1.7 mobile typography foundation. Gandalf v1.7 mobile pixel-sizing canon + DoE Path A mobile-feel target both locked. Multiple mobile-UX questions parked awaiting decisions (Q1 HP-globe / Q2 inventory drawer / Q4 resolution / Q5 DoE paragraph). But **no actual mobile state characterization exists** — we don't know what works, what's broken, what's missing on a real device or in mobile emulation.

This audit closes that gap. Stratified output (working / likely-working-unverified / broken / missing / pending-decision) lets Matt + knight-rider plan v1.18 mobile-polish dispatch precisely instead of guessing.

---

## Required reading

1. **Mobile typography foundation** — your v1.7 completion record + `src/font.ts` (or wherever MOBILE_FONT_SCALE lives)
2. **Mobile pixel sizing canon** — `canonical/story/mobile-vs-pc-pixel-sizing-2026-05-XX.md` (gandalf v1.7; 3 locks + 5 deferred questions)
3. **DoE mobile-feel target** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` (portrait primary, cooldown heal mechanics, react-or-auto 1.2s window)
4. **DoE Path A doc cascade** — `canonical/32-progression-design.md` + `canonical/17-gear-and-spirit-guide-design.md` portrait amendments
5. **Map overlay decisions** — gandalf+drax joint research doc (continue during overlay; minimap upper-right; translucent center)
6. **Mobile UX execution plan** — your v1.6 plan (7 phases M1-M7; M1 typography landed at v1.7)
7. **Your in-codebase mobile detection logic** — search for `isMobile` / `userAgent` / `matchMedia` / `mobileCamera` / `MOBILE_*` constants

---

## Scope — six audit blocks

### Block 1 — DevTools mobile emulation baseline

Test in Chrome DevTools mobile device emulation (no real device needed):
- iPhone 12 Pro / 14 Pro user agent (iOS Safari profile)
- Pixel 7 / Galaxy S22 user agent (Android Chrome profile)
- Force-reload to ensure mobile detection paths fire
- Document: does the demo detect "mobile" correctly? Does font scaling fire? Touch targets in 88-125px range?

### Block 2 — Portrait + landscape coverage

- Portrait orientation (DoE Path A target):
  - Layout renders correctly?
  - HUD elements positioned per gandalf v1.7 canon?
  - Minimap upper-right correctly positioned per map-overlay canon?
  - Combat playable without UI obscuring action?
- Landscape orientation (fallback):
  - Layout adapts?
  - Or does it forcibly request portrait?
  - Does orientation-change handler exist?

### Block 3 — Touch input verification

- Tap-to-target works? (touch on enemy = target lock per v1.17 Option A auto-cast)
- Tap-to-move works? (touch on empty floor = move target)
- Long-press behavior? (any?)
- Multi-touch? (pinch zoom, two-finger pan — should be disabled or noop)
- Touch precision (88-125px targets per canon)
- Stat-display tap-through (does tapping HUD elements bleed into world?)

### Block 4 — Performance check

- FPS at standard combat scenario (10-16 mobs on screen) in mobile emulation
- Throttled CPU 4× slowdown in DevTools (proxy for low-end Android)
- Memory pressure (mobile emulation often has 4GB or less)
- Audio + VFX firing without judder
- Atlas / texture upload latency on first cast (mobile GPUs can choke on large texture uploads)

### Block 5 — DoE-specific gestures

Per DoE Path A canon:
- Heal cooldown: how is it bound? Tap-icon? Double-tap? Specific gesture?
- React-or-auto 1.2s window: visible feedback to player? Tappable?
- Cooldown-heal triggers on touch input correctly?
- Any DoE-spec'd gestures NOT yet wired?

### Block 6 — Mobile-specific bugs / missing affordances

Catch-all for issues that emerge during audit:
- iOS safe-area handling (notch, home indicator)
- Address-bar collapse handling on scroll
- Orientation lock vs free rotation
- Browser zoom interfering with game zoom
- PWA / add-to-home-screen support (manifest.json present? service worker?)
- Standalone-app behavior (status bar, fullscreen)
- Network-disconnect resilience (asset failures, season-load failures)

---

## Deliverables

1. **Audit doc** at `agentic_orchestration/research/curated/mobile-readiness-audit-2026-05-18.md` with:
   - Stratified findings table: working / likely-working-unverified / broken / missing / pending-decision
   - Per-block findings + screenshots from DevTools mobile emulation
   - Severity rating (P0 demo-blocking / P1 polish / P2 future)
2. **v1.18 follow-on dispatch scope** — bulleted scope for the mobile-polish dispatch that fixes P0 + P1 issues identified
3. **Matt-decisions surfaced** — any new mobile-UX questions needing Matt input (beyond the parked Q1/Q2/Q4/Q5)
4. **Hive-log STATE entry** — audit complete; v1.18 scoped; gaps enumerated
5. **AGENT_STATE STATE entry**

---

## Acceptance criteria

- [ ] Audit doc authored at named path
- [ ] All 6 blocks audited; findings documented
- [ ] DevTools mobile emulation screenshots captured for portrait + landscape (at least 4 screenshots)
- [ ] v1.18 follow-on scope authored
- [ ] Severity rating applied to every finding
- [ ] New Matt-decision items surfaced (if any) for orchestration queue
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.18-pre-mobile-readiness-audit-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT FIX issues found — this is audit-only; v1.18 follow-on dispatch implements fixes
- ❌ DO NOT modify production code (audit is read-only inspection + emulation)
- ❌ DO NOT acquire real test devices (if you have one available, use it; otherwise emulation is sufficient)
- ❌ DO NOT pre-empt new-season regen (waits on Matt authorization after canonical-6 + JSON-parity chains lock)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessor:** drax v1.17 multi-bundle completion
- **Triggers downstream:** drax v1.18 mobile-polish dispatch (knight-rider fires post-this-audit if Matt-authorized scope returns)
- **Parallel-safe with:** any in-flight non-drax work; safe to run alongside engine / research seam activity
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched (queued) 2026-05-18 by knight-rider per Matt L3 mobile-audit authorization. ~1-1.5h when activated. Append audit doc + completion record when done.*

---

## Completion record

**Completed:** 2026-05-18 by drax
**Tag target:** `drax/v1.19.5-mobile-readiness-audit-1` (local; push requires Matt authorization per ADR-006)
**Audit doc:** `agentic_orchestration/research/curated/mobile-readiness-audit-2026-05-18.md`

**All 6 blocks audited. 40 findings. Summary:**

P0 findings (5): Touch hit zones all fail (8-11 CSS px vs 88px floor); portrait canvas missing (1800×944 landscape vs 944×1800 portrait canon target).

P1 findings (12): Orientation overlay inverted (shows on portrait, instructs landscape — should be opposite); orientation lock targets landscape not portrait; no tap-to-target hit zone expansion for mobile; joystick hit zone below floor; no react-or-auto affordance; no portrait HUD layout; multi-touch not explicitly guarded; audio/VFX unverified on real device; atlas prewarm timing risk.

P2 findings (7): Service worker absent; standalone mode unverified; safe-area in-canvas compensation absent; DoE single-Healing-button not implemented (two potion buttons still shown).

WORKING (11 items): Mobile detection, font scaling, canvas CSS scaling, viewport meta, safe-area body padding, PWA manifest + icons, pinch-zoom prevention, address-bar dvh handling, auto-cast (v1.17), cooldown-heal architecture (v1.18.5), DrawerShell (v1.19).

**Root cause of all P0 touch zone failures:** canvas-space HIT_R values missing 4.8× MOBILE_FONT_SCALE compensation. ~15-line fix with `hitR()` helper unblocks the entire touch layer.

**v1.20 scope drafted in audit § 4.** Three new Matt-decision items in audit § 5.

**Triggers downstream:** v1.20 mobile-polish dispatch (knight-rider fires when Matt confirms scope from Q-NEW-1/Q-NEW-2/Q-NEW-3).
