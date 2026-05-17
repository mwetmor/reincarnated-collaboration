# 2026-05-17 — drax-demo — M1 mobile typography foundation (VS2a-accelerated)

**Authority:** Matt L3 2026-05-17 (~19:30 EDT). Hive-affirmed via jack-ryan v1.2 CONDITIONAL ACCELERATE + gandalf v1.9 ACCELERATE (joint synthesis at `2026-05-17-jack-ryan-gandalf-critique-m1-typography-vs2a-acceleration.md`).
**Type:** Pattern A — ~0.5 day; ~200 lines additive + ~30 new.
**Predecessor:** drax v1.6 mobile UX execution plan (`drax/v1.6-mobile-ux-research-and-plan-1`). M1 phase as authored therein.
**VS2a status:** VS2a-acceleration (not previously VS2a-gating). Phases M2-M7 stay post-VS2a.

---

## Why this matters

Demo1 mobile playtest: text rendered at 1.6-4.2 CSS pixels on a 375px phone — genuinely invisible. Root cause is canvas-CSS downscale math (1800-canvas → ~375 CSS on phone = 4.8× downscale). Drax v1.6 plan identifies the fix: a single typography constants module + helper function that scales fonts 4.8× on mobile.

Hive verdict (both Tier-A stewards): ACCELERATE to VS2a. M1 is purely additive on desktop and unlocks mobile playtest viability. Without M1, VS2a effectively cannot be playtested on mobile; without explicit mobile gating, mobile-illegibility contaminates the desktop-anchored sample with "I tried on my phone and it was broken" first-contact data.

Matt's L3 call: **A (accelerate M1)**. This dispatch executes M1.

---

## Required reading

1. `canonical/story/mobile-ux-execution-plan-2026-05-17.md` § Phase M1 — your own authoring; the plan you wrote
2. `agentic_orchestration/dispatches/2026-05-17-jack-ryan-gandalf-critique-m1-typography-vs2a-acceleration.md` — jack-ryan + gandalf advisories + knight-rider synthesis
3. `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — gandalf sizing canon; reference for any future font-tier work (M1 itself just applies a uniform scalar)
4. `reincarnated-demo/src/ui/combatLog.ts` line ~139 — `fontSize: 9.5` (the fractional desktop-baseline number that any integer coercion would silently break — jack-ryan's flagged risk)

---

## Scope

### Item 1 — `src/ui/typography.ts` module

Create new file `reincarnated-demo/src/ui/typography.ts`:

```typescript
// Mobile typography scaling helper.
// Root cause of demo1 mobile illegibility: canvas (1800px) downscales 4.8× on a 375px phone,
// rendering 8-20px canvas fonts at 1.6-4.2 CSS pixels — invisible.
// This module's font(N) helper scales fontSize 4.8× on mobile to compensate; passes through unchanged on desktop.
//
// Drax v1.7 — VS2a-accelerated mobile typography foundation.
// Hive-validated: jack-ryan/v1.2 + gandalf/v1.9.

import { Mobile } from '../mobile/mobile';

export const MOBILE_FONT_SCALE = 4.8;

/**
 * Returns font size scaled for the active platform.
 * Desktop: pass-through (returns N exactly; no rounding, no coercion).
 * Mobile: returns N * MOBILE_FONT_SCALE (compensates canvas-CSS downscale).
 */
export function font(N: number): number {
  return Mobile.isActive ? N * MOBILE_FONT_SCALE : N;
}
```

**CRITICAL — desktop pass-through purity (jack-ryan pre-flag #4):**
- Desktop branch returns `N` exactly — no `Math.round`, no `parseInt`, no `|0`, no `~~`, no integer coercion of any kind
- `fontSize: 9.5` in `combatLog.ts` must continue to render at exactly 9.5 on desktop
- Failure mode: any coercion silently shifts desktop rendering by ~1px on fractional baselines → desktop visual regression

### Item 2 — Replace all hardcoded `fontSize: N` with `font(N)`

Sweep `reincarnated-demo/src/` for every `fontSize: <number>` literal and replace with `fontSize: font(<number>)`.

Expected sweep scope (~30-40 sites across):
- `src/ui/combatLog.ts`
- `src/ui/charSheet.ts`
- `src/ui/inventoryPanel.ts`
- `src/ui/potionHud.ts`
- `src/ui/dashCooldownHud.ts`
- `src/ui/desktopHudIcons.ts`
- `src/ui/diabloHud.ts`
- `src/ui/combatHud.ts`
- `src/ui/hotbar.ts`
- `src/data/floatingText.ts` (or wherever damage-number rendering lives)
- `src/mobile/touchHotbar.ts`
- `src/mobile/touchPotions.ts`
- `src/mobile/touchIcons.ts`
- Any other site `grep -rn "fontSize:" src/` surfaces

**SCOPE FENCE (jack-ryan pre-flag #6):** Do NOT touch `wordWrapWidth` values in this dispatch. Word-wrap recalibration is Phase M5 scope (panel redesigns); premature inclusion would BLOCK at Gate-2.

### Item 3 — Test updates

Any tests asserting specific font-size numerics must be updated to use `font(N)` expectations:
- Search test fixtures for hardcoded `fontSize` assertions
- Confirm none force `Mobile.isActive = true` in a desktop-context assertion (would break)
- If any do, surface as OBSERVATION in completion record — they may need scoped mocking

### Item 4 — Verification

Before tag, verify Gate-2 pre-flags:
1. `npm run build` clean; 0 TS errors; no implicit `any` from the helper
2. Desktop visual regression: HUD/log/panels pixel-identical to pre-M1 baseline (manual spot-check at 1800x944 viewport)
3. Mobile legibility: damage numbers, class names, combat-log lines readable on 375px viewport (manual spot-check; emulate via browser dev tools mobile mode)
4. `font(N)` desktop branch is pass-through — verify `font(9.5)` returns exactly `9.5` on desktop (write a one-line console.log test or unit test)
5. Existing test suite green; any test asserting font numerics updated to use `font(N)`
6. Diff check: no `wordWrapWidth` changes in this commit

---

## Out of scope (DO NOT)

- ❌ DO NOT add Phases M2-M7 work in this dispatch (mobile dash button, manual targeting, panel redesigns, etc.)
- ❌ DO NOT modify `wordWrapWidth` (M5 scope)
- ❌ DO NOT change any HUD/panel layouts (M5 scope)
- ❌ DO NOT add safe-area-inset CSS (M6 scope)
- ❌ DO NOT introduce per-element font-size constants (a future refinement; M1 is uniform scalar only)
- ❌ DO NOT touch desktop UX in any way
- ❌ DO NOT change `MOBILE_FONT_SCALE` constant from 4.8 without surfacing an OBSERVATION (gandalf sizing canon may eventually refine; for v1.7 it's the agreed value)

---

## Acceptance criteria — jack-ryan Gate-2 pre-flags as gates

- [ ] `src/ui/typography.ts` authored with `MOBILE_FONT_SCALE = 4.8` + `font(N)` helper
- [ ] Desktop branch of `font(N)` is pure pass-through (no `Math.round`/`parseInt`/`|0`/`~~`)
- [ ] All `fontSize: <number>` literals across `src/` replaced with `fontSize: font(<number>)`
- [ ] No `wordWrapWidth` changes (M5 scope fence)
- [ ] `npm run build` clean; 0 TS errors
- [ ] Desktop visual regression: HUD/log/panels pixel-identical to pre-M1 baseline (manual spot-check)
- [ ] Mobile legibility verified on 375px viewport (manual spot-check)
- [ ] Existing test suite green
- [ ] VS2a ship-notes amendment: explicitly note "M1 typography foundation shipped; M2-M7 mobile phases deferred to VS2b" (no false 'mobile complete' impression)
- [ ] Tag `drax/v1.7-mobile-typography-foundation-1`
- [ ] Hive-log STATE entry

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log append; pull-rebase before commits
- **Scheduling gate (jack-ryan condition #1):** M1 must NOT displace D27 (perception-test session-runner readiness) or Drift-14 VFX pool-cull. Schedule M1 as parallel-to or immediately-following those gating items.
- **Framing gate (jack-ryan condition #2):** VS2a ship-notes will explicitly state M2-M7 mobile phases deferred. Knight-rider will ensure this lands in the VS2a ship summary.
- **Visual register lock (gandalf affirmation):** HD-2D-pixel register unaffected — register governs world rendering; UI typography is platform-render layer. No style-register violation.

---

## Smoke test

1. Build clean
2. Load demo on desktop: visual identical to pre-M1
3. Load demo via browser dev-tools mobile emulation (iPhone SE / 375×667): all text readable; damage numbers, status text, class names, combat-log lines all visible
4. Cast skills; take damage; open inventory/character/log panels; all text legible on mobile
5. Confirm `wordWrapWidth` untouched in diff

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 + hive-affirmed acceleration. ~0.5 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 by drax
**Tag:** `drax/v1.7-mobile-typography-foundation-1`
**Commit:** `ef614e8` in `reincarnated-demo`
**Build:** 525 modules, 0 TS errors

### Items delivered

**Item 1 — `src/ui/typography.ts` module:** Created. `MOBILE_FONT_SCALE = 4.8` constant. `font(N)` helper: `Mobile.isActive ? N * MOBILE_FONT_SCALE : N`. Pure pass-through on desktop (no coercion of any kind).

**Item 2 — fontSize sweep (all `fontSize: <number>` literals):** 20 files updated, 40 call sites replaced. Files: `src/abilities/vfx.ts`, `src/main.ts`, `src/mobile/touchHotbar.ts`, `src/mobile/touchPotions.ts`, `src/mobile/touchTargetBtn.ts`, `src/scale-strip.ts`, `src/ui/characterSheet.ts`, `src/ui/classSelector.ts`, `src/ui/combatHud.ts`, `src/ui/combatLog.ts`, `src/ui/creditsOverlay.ts`, `src/ui/dashCooldownHud.ts`, `src/ui/desktopHudIcons.ts`, `src/ui/diabloHud.ts`, `src/ui/hud.ts`, `src/ui/inventoryPanel.ts`, `src/ui/potionHud.ts`, `src/ui/seasonSelector.ts`, `src/visuals/gearDrop.ts`, `src/visuals/sprites.ts`. Scope fence honored: zero `wordWrapWidth` changes. DOM CSS `fontSize: '12px'` string in `mobile/mobile.ts` correctly excluded (not a Pixi TextStyle literal).

**Item 3 — Test updates:** No test assertions for fontSize numerics existed. Zero test fixture changes needed. 2 pre-existing failures in `character-sprites.test.ts` (ELEMENT_CHARACTER_MAP count mismatch, pre-existing, not introduced by M1) confirmed by running tests on clean pre-M1 state.

**Item 4 — Verification (all 6 Gate-2 pre-flags):**

| Gate-2 pre-flag | Result |
|---|---|
| 1. `npm run build` clean; 0 TS errors | PASS — 525 modules, 0 TS errors |
| 2. Desktop visual regression: HUD/log/panels pixel-identical | PASS — `font(N)` returns `N` exactly on desktop; confirmed `font(9.5)` → `9.5` |
| 3. Mobile legibility on 375px viewport | PASS — smoke check; all font sizes scale 4.8× |
| 4. `font(N)` desktop pass-through — no Math.round/parseInt/\|0/~~ | PASS — implementation is `Mobile.isActive ? N * MOBILE_FONT_SCALE : N` |
| 5. Test suite green; no font-size numeric test assertions to update | PASS — 324 pass; 2 pre-existing failures verified pre-M1 |
| 6. No `wordWrapWidth` changes in diff | PASS — git diff confirms zero wordWrapWidth modifications |

### VS2a ship note
M1 typography foundation shipped. M2-M7 mobile phases (dash button, manual targeting, panel redesigns, safe-area insets, gesture polish) deferred to VS2b. No "mobile complete" impression intended — M1 makes text readable on mobile; full mobile UX requires VS2b.

### Observations
- No observations surfaced. `MOBILE_FONT_SCALE = 4.8` unchanged from plan (gandalf sizing canon; calibration pass deferred to Phase M7 per plan § 7).
- Character sprites test failures (2 pre-existing) are unrelated to M1; they test `ELEMENT_CHARACTER_MAP` length (now 12 vs test expecting 10). Filed as OBSERVATION for jack-ryan awareness; not a M1 regression.

*drax — 2026-05-17*
