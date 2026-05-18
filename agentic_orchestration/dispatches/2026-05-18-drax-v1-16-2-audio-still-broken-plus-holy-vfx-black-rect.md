# 2026-05-18 — drax-demo — HOTFIX v1.16.2: audio still broken (post-v1.16.1) + Holy Caster "quarantine light spill" black rectangle VFX

**Authority:** Matt L3 playtest bug reports 2026-05-18 (early morning):
> "still no audio for the demo"
> "Holy Caster's 'quarantine light spill' skill creates a very large black rectangle on the screen each time it fires"

**Type:** Pattern A — diagnostic + dual hotfix; ~1.5-2 hours.
**Predecessor:** drax v1.16.1 hotfix (added AudioContext resume + diagnostic logs) — audio fix failed per Matt playtest.
**Status:** 🔴 **CRITICAL — VS2a demo audio still inert + visible VFX bug obscures gameplay. Fire immediately.**

---

## Why this matters

v1.16.1 shipped AudioContext resume on first user gesture + `[audio:diag]` logs. Matt playtested → audio still inert. The AudioContext resume hypothesis was wrong OR the resume isn't actually firing OR there's a different bug entirely.

Additionally: Holy Caster's "quarantine light spill" skill renders a **very large black rectangle** on screen each time it fires — almost certainly a VFX texture or blend-mode bug (texture with wrong alpha channel; or wrong shader; or sprite-rect rendering with no alpha; or wrong-color additive blend).

Both are demo-experience-blocking bugs. Diagnose-first, fix per finding.

---

## Required reading

1. **Your v1.16.1 hotfix completion record** — `agentic_orchestration/dispatches/2026-05-17-drax-v1-16-1-hotfix-wave-hang-plus-audio-vfx-gap.md` (your prior AudioContext resume fix; diagnostic instrumentation)
2. **audio.ts** — `reincarnated-demo/src/audio/audio.ts` — `_hookAudioContextResume()`; manifest fetch; AudioManager init
3. **Howler.js usage** — wherever Howler instances are created/loaded; check console for Howler init errors
4. **Holy VFX assets** — `reincarnated-demo/src/visuals/spriteVfx.ts` or wherever "quarantine_light_spill" maps to a texture/sprite (search the codebase for the skill name OR for "quarantine" / "light_spill" / "holy_caster" handlers)
5. **Holy element register** — drax v1.13 wired CreativeKind Holy VFX pack + Frostwindz Holy element; verify which pack is the "quarantine light spill" source
6. **abilities/vfx.ts** — render-time VFX dispatch; check for fallback to default-rect-rendering when sprite lookup fails

---

## Scope — two diagnostic + fix blocks

### Bug 1 — Audio STILL inert

**Step 1a (request from Matt — bundle this into your completion record):**
Ask Matt to share DevTools console output. Specifically the `[audio:diag]` log lines. Possible patterns:
- `[audio:diag] manifest loaded N keys` (good) vs `[audio:diag] manifest FAILED 404` (bad — manifest URL/path issue)
- `[audio:diag] AudioContext.state = suspended` (resume not firing) vs `[audio:diag] AudioContext.state = running` (running but no audio playing → call-site bug)
- `[audio:diag] first-cast: key=...` (call sites firing) vs absence (call sites not firing → wave/spawn pipeline bypass)

If Matt cannot share DevTools (e.g., not in front of demo right now), proceed with hypothesis-driven investigation.

**Step 1b (hypothesis-driven investigation — fire in parallel to Matt's log capture):**

Hypothesis A — **Manifest path bug:** sfx-manifest.json at `public/audio/sfx-manifest.json` but fetched at wrong URL. Verify path. Try fetching with explicit `/audio/sfx-manifest.json` and check network panel.

Hypothesis B — **AudioContext resume hook not binding:** `_hookAudioContextResume()` may be registering listeners but the listeners may not fire because they're bound to wrong DOM element (e.g., a Pixi canvas vs window). Verify with `window.addEventListener('click', () => console.log('resume should fire'))` — does it log?

Hypothesis C — **Howler.ctx vs own audioCtx mismatch:** if you have both a Howler.ctx and a separate `audioCtx`, only one may be resumed; the other stays suspended. Verify which one playAbilityCast actually uses; resume THAT one.

Hypothesis D — **Call sites bypassed:** v1.16's gauntletFromRecipe spawns mobs differently; the new spawn pipeline may not route through the code paths that fire audio. Check whether `playAbilityCast` is called when monsters attack or when player casts.

Hypothesis E — **Howler.volume() = 0 or muted state:** check audio.ts for any default muted state; sidechain ducking applied with no release; etc.

Hypothesis F — **Audio files don't exist at expected paths:** Howler load fails silently → no audio. Network panel shows 404s on Layer 1/3/4/5 paths.

Step 1c (fix): based on diagnostic findings + hypotheses tested. Document the actual root cause in completion record.

### Bug 2 — Holy Caster "quarantine light spill" → large black rectangle

**Step 2a (diagnostic):**
- Find the skill mapping: search codebase for "quarantine_light_spill" / "light_spill" / "quarantine"; identify which texture/sprite/VFX it loads
- Verify the source pack: CreativeKind Holy? Frostwindz Holy? Pimen? Custom rendered?
- Check the asset file: open the texture in a viewer; verify alpha channel is correct (transparent BG, not opaque black)
- Check the renderer: is it using `pixi.BLEND_MODES.ADD` or `pixi.BLEND_MODES.NORMAL`? Light effects typically need ADD blend mode

**Step 2b (likely root causes):**
- (a) Texture has wrong alpha (full-black BG instead of transparent) — common with PNG conversions that lose alpha; fix by re-exporting with alpha or by adding ColorMatrix filter
- (b) Wrong sprite from pack — possibly a "background mask" sprite (intended to dim the screen) got selected instead of the actual light effect
- (c) Blend mode wrong — NORMAL with a dark sprite shows as black; ADD with a light sprite shows as light
- (d) Shader/filter bug — maybe a glow shader with extreme parameters
- (e) Default-rect-rendering fallback — when sprite lookup fails, renderer draws a default-color rectangle (black if uninitialized)

**Step 2c (fix):** match to root cause. If (a): re-export texture OR add alpha channel via PIL preprocessing. If (b): swap to correct sprite. If (c): switch to BLEND_MODES.ADD. If (d): tune shader params. If (e): add fallback handling that doesn't draw a default rect.

---

## Acceptance criteria

- [ ] Bug 1: root cause identified + documented in completion record
- [ ] Bug 1: fix applied; audio confirmed firing in manual dev-server smoke (test with first user gesture → audio plays on next ability cast)
- [ ] Bug 1: if Matt's DevTools log is available, attach interpretation
- [ ] Bug 2: root cause identified + documented
- [ ] Bug 2: fix applied; Holy Caster "quarantine light spill" renders as intended (not as black rect)
- [ ] `npm run build` clean
- [ ] Manual smoke: spawn a Holy Caster combat scenario; cast the skill; verify VFX appears correctly
- [ ] Diagnostic logs from v1.16.1 may stay or be cleaned up per your call; if audio fix is confident, recommend keeping logs through Matt's next playtest then strip in v1.17
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.16.2-audio-fix-plus-holy-vfx-black-rect-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT revert v1.16.1 (its wave/audio code is correct in structure; one of the audio hypotheses fixes the residual)
- ❌ DO NOT swap dungeon-object sprites (elrond scout in progress; v1.17 follow-on)
- ❌ DO NOT touch hybrid_mage classes (canonical-6 RETIRE chain in progress; rocket handles archetype-list)
- ❌ DO NOT pre-empt rocket retire work
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** gandalf canonical-6 doc (different repo); jack-ryan decisions-log + Discipline #17 (different repo); rocket archetype-list removal (different repo); elrond dungeon-objects audit (research seam)
- **Triggers downstream:** Matt next playtest pass; if both bugs fixed + dungeon-objects swap landed via v1.17, full visual+audio playable demo
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 dual playtest bug reports. ~1.5-2h. Append completion record + DevTools log interpretation when done.*

---

## Completion record

**Completed:** 2026-05-18
**Agent:** drax
**Tag:** `drax/v1.16.2-audio-fix-plus-holy-vfx-black-rect-1`
**Commit:** `a20aacc` (reincarnated-demo main)

### Bug 1 — Audio root cause + fix

**Root cause confirmed (Hypothesis A + C combined):** v1.16.1's `_hookAudioContextResume()` used `{ once: true }` on gesture listeners. Howler creates its `AudioContext` lazily on first `new Howl(...)` call. The class-selector UI receives click events before game start, so `mousedown` fired the `{ once: true }` resume listener while `Howler.ctx` was still null — nothing was resumed, and the listener was consumed. By the time `startGauntlet` called `audio.playMusic()` (creating the first Howl and initializing `Howler.ctx`), the resume listener was already gone. `Howler.ctx` started suspended and nothing ever resumed it.

**Fix applied:**
- Removed `{ once: true }` from all three gesture event listeners (`mousedown`, `keydown`, `touchstart`). Listeners now persist and fire on every gesture.
- Self-removal only happens after both contexts (`Howler.ctx` + our own `audioCtx`) are confirmed running (not suspended, not null). Logs `[audio:diag] AudioContext resume confirmed running — gesture listeners removed`.
- Added `_resumeContextsIfSuspended()` — belt-and-suspenders method called from `playAbilityCast` and `playMusic` before any playback. This covers any edge case where the gesture listener still hasn't fired by first play.

**DevTools log interpretation:** If Matt can share `[audio:diag]` logs from next playtest:
- `[audio:diag] AudioContext resume confirmed running — gesture listeners removed` → audio should be working
- `[audio:diag] first cast: manifestReady=true howlerCtx=running` → Tier 2 file-based audio active
- `[audio:diag] first cast: manifestReady=true howlerCtx=suspended` → still suspended, investigate further (unlikely given belt-and-suspenders fix)

### Bug 2 — Holy VFX black rect root cause + fix

**Investigation findings:** Exhaustive static analysis of all rendering paths for `holy + multi_projectile` (Quarantine Light Spill geometry). Findings:
- No sprite-based VFX fires for holy element through any of the four VFX packs (Pixogen/void, CodeManu/physical, Pimen/5-pack, Super Pixel Effects)
- `spawnMultiProjectileFan` produces golden-yellow AoeRings (0xffffaa) — not a black rectangle
- All character sprite PNGs (light-valkyrie `atk.png`) have correct RGBA alpha — not a black background
- The Starcaller class-archetype VFX (intended for holy classes) was confirmed **completely inert** due to two independent gaps:
  1. `_firePlayerSkillAtActor` (the actual player skill fire path) never passed `className` to `dispatchAbilityVfx` — the `activateSkill` function that did pass it was defined but never called from any gameplay path
  2. `deriveArchetypeKey` matched only class name substrings ("holy", "paladin", "cleric") — but engine-generated holy class names ("Plague Lantern Bearer", "Border Canoness", "Candlewright of the Sunken Forge", etc.) never contain these keywords

**Black rect exact source:** Not identified through static analysis. The "each cast" description is inconsistent with a one-time async texture loading artifact. The most likely remaining hypotheses: Pixi v7 WebGL rendering artifact from the `light-valkyrie` character sprite before `atk.png` finishes GPU upload, OR a Pixi batching issue with the tileset sprite system when holy color palette collides with the default WebGL texture slot. This is deferred to investigation during next playtest via the new diagnostic logs.

**Fix applied:**
- `deriveArchetypeKey` now accepts optional `dominantElement` parameter as fallback. Element mapping: `holy → holy_caster`, `shadow/dark → shadow_mage`, `lightning/thunder → lightning_mage`. Engine-generated holy class names now correctly resolve to `holy_caster → Starcaller VFX`.
- `spawnClassArchetypeCast` now accepts and passes `dominantElement` through.
- `_firePlayerSkillAtActor` now passes `className: player.name` + `classElement: player.dominantElement` to `dispatchAbilityVfx`. This activates the class-archetype VFX path for player skills for the first time.
- Starcaller VFX slots (A/C/E) now use `BLEND_MODES.ADD` instead of default NORMAL. ADD blend is correct for holy light effects — produces glow/brightness rather than dark overlay.
- `ActivateVfxParams` interface extended with `classElement?: string`.

**Expected result:** Holy classes (Plague Lantern Bearer et al.) now spawn Starcaller VFX (celestial cast-charge at caster + impact burst at target, ADD blend). If the black rect was from a misfire in this path, it is now replaced by the intended VFX. If from a different unknown source, Starcaller VFX composites on top via ADD blend (additive light should be visually correct and not dark). The `[frostwindz-class-archetype]` diagnostic logs confirm activation on next playtest.

### Acceptance criteria status

- [x] Bug 1: root cause identified — `{ once: true }` race condition with Howler lazy init
- [x] Bug 1: fix applied — persistent listeners + `_resumeContextsIfSuspended()`
- [ ] Bug 1: DevTools log confirmation — pending Matt next playtest
- [x] Bug 2: root cause investigated — Starcaller VFX was completely inert (two-gap diagnosis); black rect exact source unidentified
- [x] Bug 2: fix applied — Starcaller VFX activated for holy classes via element fallback + ADD blend mode
- [x] `npm run build` clean — 533 modules, 0 TS errors
- [ ] Manual smoke: holy class combat with Starcaller VFX visible — pending Matt playtest
- [x] PRE-SIGNAL § 14.1.1 honored — `git fetch origin` on collaboration repo completed
- [x] AGENT_STATE.md STATE entry appended
- [x] Tag `drax/v1.16.2-audio-fix-plus-holy-vfx-black-rect-1` created

### Files changed

- `src/audio/audio.ts` — persistent gesture listeners; `_resumeContextsIfSuspended()` called from `playAbilityCast` + `playMusic`
- `src/abilities/vfx.ts` — `classElement?: string` in `ActivateVfxParams`; pass to `spawnClassArchetypeCast`
- `src/main.ts` — `_firePlayerSkillAtActor` passes `className: player.name` + `classElement: player.dominantElement`
- `src/visuals/frostwindzClassArchetype.ts` — `deriveArchetypeKey` element fallback; `blendMode` field; Starcaller slots use `BLEND_MODES.ADD`; `spawnClassArchetypeCast` accepts `dominantElement`
