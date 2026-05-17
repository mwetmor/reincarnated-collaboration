# Dispatch — 2026-05-16 — drax — Character call-site wiring + Pixogen Lite Void Shield + attribution credits (VS2a presentation completion)

**From:** knight-rider (authored per drax character-track ingest completion scope-boundary + Matt Path A Pixogen decision 2026-05-16)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (Path A confirmed for Pixogen Lite acceptance)
**Status:** PENDING — ACTIVE
**Estimated effort:** 1-2 sessions (~2-4h); combined Pattern A dispatch closes 3 small VS2a presentation gaps simultaneously.
**Acceptance:** chierit characters render in active demo render path (replaces archetypeRenderer primitives for player classes); Pimen Lite Void Shield wired into ELEMENT_SLOT_MAP for void element; attribution credits added per license obligations (chierit CC-BY-4.0 + Pixogen AFGameAssets attribution-required); smoke verifies visible chierit characters + void VFX in demo; intermediate tag.

---

## Why this dispatch exists — closes 3 VS2a presentation gaps

### Gap 1 — Chierit characters not in active render path

Per drax character-track ingest pipeline completion (`drax/v0.18-character-track-ingest-pipeline @ 529139e`), the `characterSprites.ts` renderer module is complete + tested (24 unit tests pass) BUT NOT yet called from `sprites.ts` or `main.ts`. Active render path still uses archetypeRenderer primitives. Player classes display as primitives instead of chierit characters.

### Gap 2 — Void column unblocked by Pixogen Lite

Per Matt Path A decision (2026-05-16): accept Pixogen Lite (free; 1 Void Shield effect) for VS2a void column closure. License verified clean (AFGameAssets / Antoine Fauville — attribution-required; commercial use OK; modification OK; Pixi.js runtime tinting explicitly permitted per § 2.A.4).

Asset location: `/Users/admin/Games/reincarnated-demo/public/assets/PixelArtRPGVFXLite/Textures/Void/VoidShield_Lite.png` (64×64; 6 frames per pack docs; 1 effect)

Technology substrate (Full pack only) deferred to VS2b per Matt Path A choice.

### Gap 3 — Attribution credits not yet in demo

Per CC-BY-4.0 (chierit Elementals) + AFGameAssets license (Pixogen) attribution requirements + Discipline #11 (attribution clarity), the demo needs a credits surface (About panel / credits screen / etc.) listing:
- chierit Elementals (CC-BY-4.0)
- Antoine Fauville / AFGameAssets (Pixogen Pixel Art RPG VFX Lite)
- GandalfHardcore Samurai (if used in VS2a — note Matt downloaded but per drax v0.18 scope, deferred; verify if Samurai gets used in this dispatch)
- Future Pimen attribution (per Pimen license terms — verify whether attribution required; AFGameAssets distinct from Pimen vendor unless they're the same entity)

## What this dispatch does

### Step 1 — Chierit call-site wiring (active render path)

Update `~/Games/reincarnated-demo/src/sprites.ts` (or `main.ts` per drax's seam decision — `characterSprites.ts` is the module to integrate):

1. Replace archetypeRenderer primitive rendering for player-class combatants with `characterSprites.ts` calls
2. Per-class element resolution → ELEMENT_CHARACTER_MAP lookup → render chierit sprite
3. Animation state transitions integrate with existing per-room aggro state machine (idle when not engaged; run during movement; attack_basic during cast; take_hit during damage; death during defeat)
4. Graceful fallback: if element has no chierit mapping (kinetic / status fallback), use existing primitive renderer
5. Preserve all existing combatant lifecycle behavior (HP / death / respawn etc.)

### Step 2 — Pixogen Lite Void Shield ELEMENT_SLOT_MAP entry

Update `~/Games/reincarnated-demo/src/visuals/pimenVfx.ts` (or analogous module — your call on placement; Pixogen ≠ Pimen vendor but the ELEMENT_SLOT_MAP pattern is shared):

1. Add `void` entry to ELEMENT_SLOT_MAP referencing `PixelArtRPGVFXLite/Textures/Void/VoidShield_Lite.png` (6 frames; 64×64)
2. If pimenVfx.ts is Pimen-specific, create parallel `pixogenVfx.ts` module + register it in the VFX dispatcher
3. Animation state: 6-frame loop OR one-shot (verify from pack docs)
4. Smoke verify: void-element class cast events trigger Void Shield render instead of Super Pixel Effects fallback

### Step 3 — Attribution credits surface

Add credits surface to demo:

1. Create or extend existing About / Credits screen (drax's call on placement — likely a settings panel or game-start splash)
2. Required entries:
   - **"VFX assets by Antoine Fauville / AFGameAssets"** (per Pixogen license § 3.A.1) — include URI to license OR pack page
   - **"Character sprites by chierit (CC-BY 4.0)"** (per CC-BY 4.0 license)
   - **"Samurai prototype sprite by GandalfHardcore"** (if Samurai used in active render path; defer if not used per drax v0.18 deferral)
3. Format: simple text list; production polish deferred to feedback-layer art track
4. Verify license URIs are correct + functional links

### Step 4 — Optional: Samurai light integration

Matt downloaded GandalfHardcore Samurai despite my prior recommendation to skip (mid-pixel register; not canonical). Per drax v0.18 deferral, Samurai is NOT wired yet. **Drax discretion**: if scope allows in this dispatch, light-wire as NPC placeholder OR enemy prototype for monster-track-pending state. If scope creeps, defer Samurai to follow-on dispatch.

### Step 5 — Tests + smoke + visual verification

- Existing 232+ tests preserved
- Unit tests for call-site wiring (sprites.ts + main.ts changes; mock combatant data; verify characterSprites.ts called)
- Unit tests for void slot resolution
- Smoke: load test season; verify visible chierit characters for player classes + void VFX renders for void-element casts
- `npm run build` PASS
- Per Discipline #2 + #11

### Step 6 — Friction findings + completion

- Update `~/Games/reincarnated-demo/CHARACTER_TRACK_INTEGRATION_NOTES.md` with call-site wiring findings
- File `~/Games/reincarnated-demo/CREDITS_ATTRIBUTION_NOTES.md` (or fold into existing notes file) documenting attribution surface + license URI references
- Tag `drax/v0.19-character-wire-up-void-attribution`
- AGENT_STATE.md updated
- Completion report to knight-rider

## Cross-seam considerations

- **Engine (rocket/gamora/star-lord)**: READ-ONLY; no engine changes (presentation layer only)
- **Elrond**: Pixogen catalogue record needs `license_unverified: true` → `false` + `consumption_hold: HOLD` → `APPROVED-WITH-ATTRIBUTION` flag update (separate small elrond dispatch knight-rider will route)
- **Legolas**: Pixogen findings-summary doc needs license_terms_verbatim update (separate small legolas commission)
- **Gandalf**: design-lineage owner of style register; if chierit characters visually drift from HD-2D register at scale, surface as finding (post-acquisition visual inspection)
- **Knight-rider**: notify at completion; closes 3 VS2a presentation gaps in a single dispatch

## Out of scope (explicit)

- **NO Pixogen Full pack purchase or Technology substrate work** (Matt Path A choice; Technology stays VS2b)
- **NO new chierit features beyond call-site wiring** (renderer is already feature-complete)
- **NO new monster sprites** (separate; monster-track scout returned; acquisitions are separate decisions)
- **NO room/hallway changes** (separate)
- **NO B11 demo changes** (already complete)
- **NO engine schema changes** (presentation layer only)
- **NO Pimen license re-verification** (Matt's downloads = implicit acceptance; if attribution required for Pimen, surface)
- **NO chierit per-character-variant customization** (chierit ships pre-styled; not Mana Seed paper-doll work)
- **NO procedural-asset generation**
- **NO new Pixogen assets beyond Void Shield from Lite pack**

## Required reading

- Your prior `drax/v0.18-character-track-ingest-pipeline @ 529139e` (scope-boundary source)
- `/Users/admin/Games/reincarnated-demo/CHARACTER_TRACK_INTEGRATION_NOTES.md` (your prior findings)
- `/Users/admin/Games/reincarnated-demo/public/assets/PixelArtRPGVFXLite/License.txt` (Pixogen license terms; cite in credits)
- `/Users/admin/Games/reincarnated-demo/public/assets/PixelArtRPGVFXLite/ReadMe.txt` (Pixogen pack contents)
- chierit license: CC-BY-4.0 (cite in credits)
- Your prior `pimenVfx.ts` ELEMENT_SLOT_MAP pattern (`drax/v0.14-pimen-element-slot-map-real-mapping @ 7fba617`)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #11 (attribution: license compliance for chierit + Pixogen)

## Acceptance criteria

- [ ] chierit characters render in active demo render path (replaces primitives for player classes)
- [ ] characterSprites.ts called from sprites.ts / main.ts (was wired-but-not-called pre-this-dispatch)
- [ ] Pixogen Lite Void Shield wired into ELEMENT_SLOT_MAP (or equivalent void slot)
- [ ] Void-element class casts trigger Void Shield render (not Super Pixel Effects fallback)
- [ ] Credits surface present in demo with required attribution entries
- [ ] Existing 232+ tests preserved + new wiring tests pass
- [ ] npm run build PASS
- [ ] CHARACTER_TRACK_INTEGRATION_NOTES.md updated
- [ ] CREDITS_ATTRIBUTION_NOTES.md filed (or folded into existing)
- [ ] Intermediate tag `drax/v0.19-character-wire-up-void-attribution` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `drax/v0.19-character-wire-up-void-attribution` at the commit closing wiring + smoke pass.

---

## Completion record

**Completed:** 2026-05-16

**Intermediate tag:** `drax/v0.19-character-wire-up-void-attribution @ 3256656`

**Call-site wiring approach:**
Integration embedded in `sprites.ts` `createCombatantSprite()` (not in main.ts). Accepts optional `element`
param; calls `createCharacterSprite(element)` when element has chierit mapping. `charSprite` stored in
`CombatantSprite` interface. `tickCombatantAnimation()` ticks it and maps demo states → chierit anim states.
Primitive `body` Graphics hidden (`.visible = false`) once `charSprite.ready = true`. Fallback (kinetic/status)
is automatic — `hasCharacterSprite()` returns false → `charSprite = null` → primitive renders unchanged.
`signalCharacterTakeHit()` exported; called from `showImpact()` on damage hits.
`prewarmCharacterSpriteCache()` called at gauntlet start.

**Void slot resolution status:**
New module `src/visuals/pixogenVfx.ts` created. `resolvePixogenLiteSlot('void', geometry)` returns
VoidShield_Lite.png slot for all geometry types. Sprite is 64x384 vertical strip (6 frames × 64px).
`spawnPixogenLiteVfx()` dispatches void VFX. `spriteVfx.ts` dispatch chain updated: Pixogen Lite → Pimen → Super
Pixel Effects. Void-element class casts will now trigger VoidShield_Lite.png instead of Super Pixel Effects fallback.

**Credits surface location:**
`src/ui/creditsOverlay.ts` — `CreditsToggle` class. Toggle with F1 in-game.
Required entries present:
- "Character sprites — Elementals by chierit" (CC-BY 4.0, https://chierit.itch.io/)
- "VFX sprites — Pixel Art RPG VFX Lite by Antoine Fauville / AFGameAssets" (AFGameAssets license, https://afgameassets.itch.io/pixel-art-rpg-vfx)
Deferred entries: Pimen per-pack (license terms pending), GandalfHardcore Samurai (not wired).
Reference doc: `CREDITS_ATTRIBUTION_NOTES.md`

**Samurai integration scope:** DEFERRED. Same decision as v0.18. Mid-pixel register, no engine element
mapping, monster-track scout not returned. Samurai available at `public/assets/GandalfHardcore Samurai/`.

**Notes for knight-rider:**
- All 3 VS2a presentation gaps closed in this dispatch.
- 253/253 tests pass (21 new). `npm run build` PASS, TypeScript clean.
- Acceptance criteria met: chierit in render path, void VFX wired, credits overlay present.
- Elrond action needed: Pixogen catalogue record — `license_unverified: true` → `false`,
  `consumption_hold: HOLD` → `APPROVED-WITH-ATTRIBUTION` (per dispatch cross-seam note).
- Legolas action needed: Pixogen findings-summary doc update with license_terms_verbatim.
- Known visual item (not blocking): chierit sprite scale (0.35) needs playtest visual inspection tuning.
  Matt can adjust in `src/visuals/characterSprites.ts` CHIERIT_FRAME_W/H and sprite.scale.set() line.
- Known limitation: take_hit animation state has no linger timer (resets on next frame).
  Post-VS2a item — see AGENT_STATE.md open items.
- Pixogen Full (Technology substrate) stays VS2b per Matt Path A.
- Void column is closed for VS2a. vortex_pull Pixogen Black Hole effect stays VS2b (Full pack not purchased).
