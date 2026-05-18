# 2026-05-18 — drax-demo — v1.20 multi-fix: mobile touch zones (P0) + Holy Controller black-box (4th attempt) + door icon fit + first-tileset swap + pimen warnings cleanup

**Authority:** Matt L3 verbatim 2026-05-18 playtest:
- *"re-fire rocket regen"* — separate dispatch
- *"would like to try the first tileset as I never saw that one"* — Block 4
- *"please the door icon it doesnt fit the doorway"* — Block 3
- *"good play test results: Audio works - both VFX and music"* ✅ v1.18.5 confirmed
- *"One more Holy Controller issue (still have the black box)"* — Block 2
- *"more console error logs"* (DevTools screenshot Image #17) — Blocks 2 + 5
- Plus drax v1.19.5 audit § 4 P0 — Block 1
- Plus Matt Q-NEW decisions 2026-05-18:
  - Q-NEW-1 portrait canvas: DEFER to v1.21 — not in this dispatch
  - Q-NEW-2 orientation overlay: INVERT — show "rotate to portrait" on landscape — **Block 6 (new)**
  - Q-NEW-3 multi-touch: under auto-cast, skill-arc taps are rare; verify but don't block

**Type:** Pattern B multi-block; ~3-4 hours.
**Predecessor:** drax v1.19 mobile drawer/modal + v1.19.5 mobile-readiness audit complete.
**Status:** 🟢 **ACTIVE — fire after rocket regen detached. Drax idle.**

---

## Why this matters

Audio + most VFX now working post-v1.18.5. The remaining VS2a-blocker bugs in this dispatch are:
- P0 mobile touch zones (audit § 4) — 15-line fix unlocks the entire mobile touch layer; without it, mobile playtest is impossible
- Holy Controller "black box" — precise console diagnostic (texture frame error) pins the root cause this time
- Door icon visual mismatch — small polish but Matt-flagged
- First-tileset swap — Matt wants to see the alternate CraftPix dungeon pack he's never seen
- Pimen metadata.json warnings — 6 packs producing console noise; gracefully handled but unprofessional in console

These five together close out almost all visual + interaction polish on the demo before fresh-season playtest.

---

## 🎯 PRECISE DIAGNOSTIC FROM MATT'S CONSOLE SCREENSHOT (Image #17)

### Holy Controller black-box — PRECISE this time

Console shows TWO `Error: Texture Error: frame does not fit inside the base Texture dimensions:` errors at `Texture.ts:661`, immediately after:
- `[frostwindz-class-archetype] archetype=holy_caster slot=A`
- `[frostwindz-class-archetype] archetype=holy_caster slot=C`
- `[ability-vfx] geometry=self_buff element=holy sprite=spell_attack_up_001 duration=1.20s`

The texture errors:
1. `X: 276 + 46 = 322 > 320 or Y: 0 + 64 = 64 > 128` — frame at x=276,w=46 on a 320-wide texture (2px overflow)
2. `X: 535 + 107 = 642 > 640 or Y: 0 + 128 = 128 > 128` — different sprite, also 2px overflow

When Pixi rejects a frame as "doesn't fit base texture," the resulting sprite typically renders as a black/broken rect. **This is the Holy Controller black box.**

The relevant SPEC entry (`src/visuals/spriteVfx.ts:72`):
```typescript
self_buff: { category: 'Fantasy%20Spells', effect: 'spell_attack_up_001', frameCount: 18, scale: 1.5, physColor: 'yellow', posMode: 'caster' },
```

Holy Controller fires a `self_buff`-geometry ability → sprite `spell_attack_up_001` is loaded → frame math at frame index 18 (the LAST frame) computes a rect that's 2px past the sheet width → texture error → black render.

Two hypotheses to investigate:
1. **frameCount = 18 is wrong** — sheet actually has 17 frames, and frame 18 indexes past the right edge
2. **frame width/height is computed wrong** — `frameW = sheetW / frameCount` rounds up to 18px (or whatever) and stacks 18 × computed-width past sheet edge by 2px

Likely fix: lower `frameCount: 18` → `17` (or whatever the actual frame count of `spell_attack_up_001.png` is). Verify via PIL or by reading the PNG file dimensions divided by the per-frame width.

### Pimen metadata.json missing — 6 packs

Console shows 6 warnings:
- `[pimen-vfx] dark-spell-effect — metadata.json not found or parse error`
- `[pimen-vfx] buff-n-debuff-vfx-pack-01 — metadata.json not found or parse error`
- `[pimen-vfx] buff-n-debuff-vfx-pack-02 — metadata.json not found or parse error`
- `[pimen-vfx] battle-vfx-hit-spark — metadata.json not found or parse error`
- `[pimen-vfx] battle-vfx-projectile — metadata.json not found or parse error`
- `[pimen-vfx] pixel-battle-effects — metadata.json not found or parse error`

Followed by: `[pimen-vfx] prewarm complete — 112 anim slots cached` — graceful handling. These 6 packs don't have generated metadata.json sidecars; the loader falls back to defaults. Two fix paths:
- **(a)** Generate metadata.json for the 6 packs (via PIL: scan PNG dimensions, write `{"frames": N, "frameW": W, "frameH": H, "scale": S}` sidecar) — proper fix
- **(b)** Suppress the warning log at the loader if the pack has a known-default mapping — minimal cleanup

Recommend (a) for the 6 packs to silence the console + make the default values explicit/discoverable. ~15 min PIL script.

---

## Required reading

1. **Mobile audit § 4 — v1.20 follow-on scope** — `agentic_orchestration/research/curated/mobile-readiness-audit-2026-05-18.md` § 4 (P0 items 1+2)
2. **Audit § 3 — hitR() helper pattern** — same doc; ~15 lines of code spec inline
3. **spriteVfx.ts:72** — self_buff SPEC entry (spell_attack_up_001 frameCount=18)
4. **spriteVfx.ts SPEC map general** — see how `ring` entry was added at v1.18.5; same pattern for the fix
5. **`src/visuals/dungeonTileset.ts`** — tileset routing + 3 CraftPix packs (298079 PRIMARY, 125640, 169442)
6. **Elrond dungeon-tileset manifest** — `agentic_orchestration/research/curated/dungeon-tileset-subset-vs2a-2026-05-17.jsonl` (3 WIRE-NOW rows — identifies the "first" tileset Matt has never seen)
7. **Door rendering in demo** — drax to investigate; not located by knight-rider; possibly part of room/encounter renderer
8. **Pimen loader** — `src/visuals/pimenVfx.ts:458` (warning emit site); `src/visuals/pimenVfx.ts:463` (prewarm complete site)
9. **typography.ts `font()` helper** — the pattern hitR() will mirror

---

## Scope — five fix blocks

### Block 1 — Mobile touch zones (P0 from audit § 4)

**1.1 — Author `hitR()` helper.** In `src/mobile/typography.ts` (alongside existing `font()` helper), add:

```typescript
/**
 * Hit-zone radius scaler. Mirrors font(N) pattern.
 *
 * Mobile canvas-space radii must be MULTIPLIED by MOBILE_FONT_SCALE (4.8 on a
 * 375px viewport against a 1800px canvas) so the resulting touch zone reaches
 * the canon 88px CSS floor / 110-125px centroid.
 *
 * Desktop: passes through unchanged.
 *
 * @param cssTarget the desired CSS-px hit radius (canon: 88 floor, 110-125 centroid, 140 most-tapped)
 */
export function hitR(cssTarget: number): number {
  return Mobile.isActive ? cssTarget * MOBILE_FONT_SCALE : cssTarget;
}
```

**1.2 — Expand HIT_R in 5 touch files.** Visual radii (BTN_R/ICON_R/POT_R/etc.) **stay at current values** — only HIT_R changes:

| File | Current HIT_R | New HIT_R | Canon target (CSS) |
|---|---|---|---|
| `src/mobile/touchIcons.ts` | 36 | `hitR(88)` | 88 minimum |
| `src/mobile/touchHotbar.ts` | 52 | `hitR(110)` | 110-125 centroid |
| `src/mobile/touchPotions.ts` | 38 | `hitR(140)` | 140 (most-tapped) |
| `src/mobile/touchTargetBtn.ts` | 38 | `hitR(88)` | 88 minimum |
| `src/mobile/joystick.ts` | R_OUTER=80, zone=+20 → eff=100 | adjust to effective `hitR(150)` | 150 outer (genre canon) |

**1.3 — LMB tap-to-target forgiveness.** In `_handleLmbClick()` (or wherever CLICK_HIT_RADIUS=50 is used for enemy hit-testing on touch), branch:
```typescript
const clickRadius = Mobile.isActive ? CLICK_HIT_RADIUS * MOBILE_FONT_SCALE : CLICK_HIT_RADIUS;
// Or: clickRadius = hitR(75); // 75px CSS canon for touch tap-to-target
```

**1.4 — Multi-touch sanity (Q-NEW-3 verification).** No code change required, but during smoke add `console.log` for simultaneous pointer events on joystick + skill arc, confirm both fire independently. If cross-fire observed, add pointerId-guard at appropriate handler.

**OUT OF SCOPE for v1.20 (Q-NEW-1 only; canvas remap deferred to v1.21):**
- ❌ Do NOT remap canvas to 944×1800 portrait (Q-NEW-1 Matt L3: DEFER to v1.21)

**Q-NEW-2 IN SCOPE (Block 6 below):** orientation overlay invert per Matt L3 lock.

**Q-NEW-3 (multi-touch):** Matt note 2026-05-18: *"under auto-cast, skill-arc taps are rare; verify but don't block."* — keep current architecture; add the console-log smoke verify; do not add pointerId-guard unless cross-fire actually observed.

### Block 2 — Holy Controller black-box (4th attempt; precise diagnostic)

**2.1 — Verify frame count.** Find the actual PNG file at:
`public/assets/.../Fantasy%20Spells/spell_attack_up_001.png` (or wherever the SPEC route resolves it).

Use PIL or read PNG header to get sheet width. Divide by per-frame width (typical: 64 or 80 or 96). The truth-table for SPEC `frameCount` is `floor(sheetW / frameW)`. The currently-declared `frameCount: 18` may overshoot the actual frame count by 1 (producing the 2px overflow Matt's console showed).

**2.2 — Fix the SPEC entry.** At `src/visuals/spriteVfx.ts:72`, update `frameCount` to the verified value. Also verify `scale: 1.5` rendering against a holy_controller class smoke-cast.

**2.3 — Check the second texture error.** The console showed TWO errors:
- 1st: X 276+46=322 > 320 — width 320 sheet
- 2nd: X 535+107=642 > 640 — width 640 sheet

These are TWO different sprites with the same root cause (frameCount > actual frames). Identify the second sprite via:
- Add temporary `console.log(spec.effect, baseTexture.width, frameW, frameCount)` at the SpriteVfx slice path
- Run a smoke-encounter touching multiple holy abilities; capture which sprite the 2nd error refers to
- Fix that SPEC entry too

**2.4 — Hardening: clamp frameCount.** As defense in depth, in the slicer, do:
```typescript
const safeFrames = Math.min(spec.frameCount, Math.floor(baseTexture.width / frameW));
if (safeFrames !== spec.frameCount) {
  console.warn(`[ability-vfx] frameCount clamped ${spec.effect}: declared=${spec.frameCount} actual=${safeFrames}`);
}
```
Prevents future spec drift from producing texture errors.

**2.5 — Smoke verify Holy Controller no longer black-boxes.** Run a holy_controller class encounter; verify all skills render visible VFX (no black rects).

### Block 3 — Door icon fit

Matt: *"please the door icon it doesnt fit the doorway"*

Investigate:
- Locate door/doorway rendering in encounter/gauntlet/room code (knight-rider could not find an explicit `Door` or `createDoor` function in `src/visuals/` or `src/encounter/` — likely embedded in room renderer or wave-transition logic)
- Determine: is "door icon" the room-transition / wave-exit door sprite? Or an inventory/UI icon?
- Most likely: the wave-exit/room-transition door drawn at the room boundary doesn't visually fit the doorway opening (size mismatch, or anchor offset off)
- Fix: align sprite size/anchor to the actual doorway gap dimensions

If unable to repro from code alone, add a `console.log` near the door render to inspect coordinates + size, run dev-server, find the visual mismatch, and correct.

### Block 4 — First-tileset swap (EARLIER VENDOR, NOT a different CraftPix pack)

Matt (clarified 2026-05-18): *"For item 4, switch from craft pix to the earlier vendor"*

**This is a vendor swap, not a pack swap.** Current state: all dungeon floor tiles come from CraftPix (vendor) — pack 298079 plates.png since drax v1.17. The pre-CraftPix demo state used a different vendor for floor/dungeon tiles.

**Archaeology required.** Investigate git history to identify the earlier-vendor floor tileset:

```bash
# Pre-v1.13 (before drax/v1.13 wired CraftPix dungeon tilesets), what was the floor source?
git log --oneline --all --diff-filter=A -- 'src/visuals/' | head -20
# Look for commits like: v0.9-partial (first per-season floor + walls), v0.7 (combatant rendering),
# and the earliest "floor" or "dungeon" or "tileset" wiring.
git show 7a45e56 --stat | head -30   # v0.9-partial: per-season floor + walls + ambient particles
git show <earlier-floor-commit>:src/visuals/<floor-file>.ts | head -50
```

The earlier vendor is **not** DireDungeon (DerNachbar — that's loot-tileset only; checked: `DireDungeonItemsTileset_by_DerNachbar` is items/loot, not floor). It's likely either:
- A vendor pack from `public/assets/` that pre-dates the CraftPix dungeon tileset wiring (e.g., earliest tileset file in git)
- An older itch.io / OGA / earlier-acquired pack that the v0.9-partial commit referenced
- Possibly Pixogen / Pimen / Frostwindz / CreativeKind if any of them ship dungeon-floor tiles

**Implementation:**
1. Identify the earlier-vendor floor tileset by git archaeology
2. If the asset is still in `public/assets/`, verify it's loadable + the floor sheet has tileable rows
3. Add a `FLOOR_TILE_DESC_EARLIER_VENDOR` parallel to the existing `FLOOR_TILE_DESC` in `dungeonTileset.ts`
4. Switch the active floor source via a single constant flip at the top of the file:
   ```typescript
   const ACTIVE_FLOOR_VENDOR: 'craftpix-298079' | 'earlier-vendor' = 'earlier-vendor';
   ```
5. Both paths stay in code; Matt can flip the constant to compare. CraftPix path stays for revert/A-B.

**If the earlier vendor's asset is no longer on disk** (purged in a safety snapshot or never tracked): note it in the completion record + flag for elrond to re-acquire. Do NOT silently fall back to a different CraftPix pack — Matt explicitly wants the earlier-vendor look.

**Acceptance:** Matt sees the pre-CraftPix-era floor in dev-server. Vendor name + asset path documented in completion record. CraftPix path preserved.

### Block 6 — Orientation overlay invert (Q-NEW-2 Matt L3 LOCKED 2026-05-18)

Matt verbatim 2026-05-18: *"QNew 2 - yes show 'rotate to portrait' if they try to go to landscape"*

Per Matt L3 Path A portrait-primary canon lock (2026-05-17) + Q-NEW-2 (2026-05-18): the orientation overlay must invert so that **landscape orientation triggers the overlay** and the message instructs the player to rotate to **portrait**. Three coupled files:

**6.1 — `src/mobile/orientationOverlay.ts`:**
- Detection: change `window.matchMedia('(orientation: portrait)')` to `window.matchMedia('(orientation: landscape)')` (show overlay WHEN landscape)
- Message text: change "Best experienced in landscape / Please rotate your device" to **"Best experienced in portrait / Please rotate your device to portrait"**
- Keep current visual treatment (DOM overlay above canvas; dimissable on orientation change)

**6.2 — `src/mobile/mobile.ts`:**
- Change `screen.orientation.lock('landscape')` to `screen.orientation.lock('portrait')` (or remove the lock entirely and rely on the overlay for guidance — Matt's intent is "show the message," not "force-lock," so either works; recommend `lock('portrait')` since it's the post-Q-NEW-2 canonical direction)
- On iOS Safari `lock()` rejects silently — keep `.catch()` in place

**6.3 — `public/manifest.json`:**
- Change `"orientation": "landscape"` → `"orientation": "portrait"`
- PWA install / standalone mode will then default to portrait

**6.4 — Smoke verify:**
- Dev-server in DevTools: switch device to portrait — overlay should be absent (game playable)
- Switch device to landscape — overlay should appear with "rotate to portrait" message
- Build clean

**Important coupling with Q-NEW-1 deferral:** v1.20 canvas is still 1800×944 landscape internally. The overlay tells the player to rotate to portrait, but the canvas-internal HUD positions are landscape-calibrated. In practice: on a real phone in portrait, the landscape canvas will letterbox with large top + bottom black bars (canvas aspect 1.91 vs portrait phone aspect ~0.46). Game is playable in this letterbox state — joystick / arc / potions / globes all visible — but it's a stopgap until v1.21 portrait canvas remap. Note this trade-off in completion record.

### Block 5 — Pimen metadata.json warnings cleanup

6 pimen packs missing metadata.json sidecars. Fix path (a) preferred — generate the sidecars:

For each of the 6 packs at `public/assets/pimen/<pack-name>/`:
- Scan the PNG files (use PIL or Pixi probe in a Node script)
- Write a `metadata.json` sidecar with `{frames, frameW, frameH, scale, anim_name}` per the pimen loader's expected schema
- Verify with dev-server: console no longer warns "metadata.json not found or parse error" for these 6 packs

If sidecar schema is non-trivial / requires content judgement (e.g., distinguishing which PNG is which animation in a multi-file pack), fall back to fix path (b): downgrade the warning log to `console.debug` for these 6 packs only (whitelisted in pimenVfx.ts) — accepts the noise-level reduction without authoring proper sidecars.

---

## Acceptance criteria

- [ ] Block 1: `hitR()` helper authored in typography.ts; HIT_R expanded across 5 touch files; LMB tap-to-target forgiveness branched; build clean
- [ ] Block 1: device-emulation smoke verifies hit zones now feel reasonable (DevTools mobile emulation; visual touch zones unchanged)
- [ ] Block 2: spell_attack_up_001 frameCount verified against actual PNG; SPEC fixed; 2nd texture error sprite identified + fixed; frameCount-clamp hardening added; Holy Controller smoke shows no black box
- [ ] Block 3: door icon fits doorway (size/anchor aligned)
- [ ] Block 4: alternate CraftPix dungeon tileset (likely 125640) is active and renders cleanly; 298079 path preserved for revert
- [ ] Block 5: 6 pimen metadata.json warnings silenced (either via sidecar authoring or whitelist downgrade)
- [ ] Block 6: orientationOverlay.ts inverted; mobile.ts lock flipped; manifest.json orientation field flipped; landscape→portrait overlay verified in DevTools
- [ ] `npm run build` clean
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.20-mobile-touch-zones-plus-holy-controller-plus-door-icon-plus-first-tileset-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT remap canvas to 944×1800 portrait — Q-NEW-1 deferred to v1.21 own dispatch
- ❌ DO NOT remap canvas to 944×1800 portrait — Q-NEW-1 pending; recommended defer to v1.21 own dispatch
- ❌ DO NOT change the visual button radii (BTN_R/ICON_R/POT_R/etc.) — only hit-zones change in Block 1
- ❌ DO NOT delete the 298079 tileset path in Block 4 — only flip the active constant
- ❌ DO NOT re-enable dungeon objects (Matt L3 v1.18.6 removed; canon)
- ❌ DO NOT re-enable stairs (Matt L3 v1.18.5 removed; canon)
- ❌ DO NOT push tag (ADR-006)
- ❌ DO NOT pre-empt drax v1.20+ chierit monster wiring (queues after)
- ❌ DO NOT pre-empt drax v1.21+ icons/credits/schema (queues after; props portion cancelled)

---

## Coordination

- **Predecessors:** drax v1.19 + drax v1.19.5 audit complete
- **Parallel-safe with:** rocket regen 002016 re-fire (different repo)
- **Triggers downstream:**
  - v1.21 portrait canvas remap (pending Q-NEW-1 Matt L3)
  - v1.21 orientation overlay decision (pending Q-NEW-2 Matt L3)
  - Chierit monster wiring (queued next)
  - v1.22+ icons + credits + schema (from elrond v1.11 handoff brief; props portion cancelled per v1.18.6)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 playtest feedback + drax v1.19.5 audit § 4. ~3-4h drax. Append completion record + Holy Controller root-cause + 2nd-error sprite name + door-fit diagnosis + which tileset selected when done.*

---

## Completion record

*(drax appends here when done)*
