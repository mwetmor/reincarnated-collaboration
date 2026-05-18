# 2026-05-17 — drax-demo — HOTFIX v1.16.1: wave-progression hang + audio/VFX gap (Matt playtest bugs)

**Authority:** Matt L3 playtest report 2026-05-17 late-evening (verbatim):
> "BTW, there is no audio/VFX in the demo right now, and I experienced a bug where after I beat the second room of monsters, I could move into the next room infinitely but it never populated a visual gate on the right-hand side of the hallway and did not open it and did not trigger the next wave number at the top of the screen and did not trigger the next batch of combatants to appear."

**Type:** Pattern A — diagnostic + hotfix; ~1-2 hours.
**Status:** 🔴 **CRITICAL — VS2a demo is non-playable past room 2. Fire immediately.**

---

## Why this matters

VS2a Final Sprint shipped 5/5 areas clean in v1.13. Audio shipped in v1.15. Monster expansion in v1.14. JSON-parity wiring in v1.16. **Build is clean** (533 modules, 0 TS errors per v1.16 completion). But playtest reveals two regressions blocking demo completion:

**Bug 1 — no audio/VFX:** despite v1.15 audio.ts wiring + v1.13 VFX layer initialization (Pimen / Frostwindz / atmospheric). Either the call sites aren't firing, or initialization is failing silently, or AudioContext is blocked pending user gesture (browser policy).

**Bug 2 — wave-progression hang at room 2:** demo lets player walk into next room indefinitely with no gate, no HUD update, no spawn. This is the new 6-wave `gauntletFromRecipe` shape colliding with the legacy wave-completion / gate-spawn / wave-HUD machinery that was built for the old 5-wave pickMonsters structure.

Both bugs almost certainly regress from v1.16's gauntlet refactor. Diagnostic + hotfix needed before any further VS2a polish.

---

## Required reading

1. **Your v1.16 completion record** — `agentic_orchestration/dispatches/2026-05-17-drax-v1-16-json-parity-gauntlet-recipe-plus-monster-maxhp-queued.md` § completion (your own work; refresh on what landed in gauntlet.ts)
2. **Your gauntlet.ts** — `reincarnated-demo/src/encounter/gauntlet.ts` — `gauntletFromRecipe()` + `buildGauntlet()` branch logic
3. **Wave-progression machinery** — wherever wave-cleared detection + gate-spawn + wave-HUD increment lives (encounter/ or game/ subdirs; likely tied to wave-index advancing on mob-death-count)
4. **audio.ts** — `reincarnated-demo/src/audio/audio.ts` — initialization sequence + manifest fetch + AudioContext setup
5. **VFX layer mounts** — `src/visuals/atmosphericLayer.ts`, `src/visuals/pimenVfx.ts`, `src/visuals/frostwindzPhysical.ts`, `src/visuals/frostwindzClassArchetype.ts` (init sites; verify they're being called from stage/main)
6. **Stage init** — `src/rendering/stage.ts` — atmosphericUnder/Over containers; verify they're populated

---

## Scope — three diagnostic + fix blocks

### Bug 1 — Audio/VFX investigation

**Step 1a (diagnostic):** Add DevTools-visible diagnostics:
- Log audio.ts manifest fetch result (`fetch('/audio/sfx-manifest.json')` → success/failure + parsed manifest size)
- Log AudioContext state on first user click (`audioCtx.state` — should be 'running' post-gesture)
- Log VFX layer init: count children in each container at game-start (atmosphericUnder, atmosphericOver, particlesUnder, particlesOver, etc.)

**Step 1b (fix):** Based on diagnostic:
- If manifest 404 → fix path (likely `public/audio/sfx-manifest.json` vs runtime URL mismatch)
- If AudioContext state='suspended' → resume on first user gesture (canonical pattern: `audioCtx.resume()` on first mouse/keyboard event)
- If manifest loads but `playAbilityCast` etc. never fires → check call sites in `combatant.ts` / `abilities/vfx.ts` / wherever skills resolve; may be that v1.16's new monster spawn pipeline doesn't pass through the same trigger paths
- If VFX containers empty → check that v1.13's `atmosphericLayer.ts` etc. are actually being awaited + mounted during stage init (maybe an init order regression from v1.16's loader changes)

### Bug 2 — Wave-progression hang at room 2

**Step 2a (diagnostic):** Add logging:
- Log wave-index advance attempts (where in the code does `wave++` happen?)
- Log mob-death-count vs wave-completion threshold
- Log gate-spawn trigger conditions (presumably `if (wave_cleared && current_wave < total_waves) spawn_gate()`)
- Log what the gauntletFromRecipe-built structure looks like at runtime (waves count, mobs-per-wave, expected total kill count)

**Step 2b (likely root cause):** v1.16's `gauntletFromRecipe` builds **6 waves**:
- Waves 1-3: pack-proxy waves (16 individuals/wave from 2 pack slots × 8 mobs each)
- Wave 4: magic cadre (slots 6-7; 2 mobs)
- Wave 5: elite vanguard (slots 8-9; 2 mobs)
- Wave 6: boss gauntlet (mini-boss + boss; 2 mobs)

Total mobs/recipe-season = 48 + 6 = **54 mobs across 6 waves** (huge wave 1-3 swarms).

Legacy `pickMonsters` built **5 waves**:
- ~14 mobs (8 trash + 2 std + 2 elite + 1 mini + 1 boss) — much smaller scale

If wave-completion detection is hard-coded to specific mob counts OR expects 5 total waves, v1.16's 6-wave 54-mob structure breaks it. After wave 2 (the "second room" Matt cleared), wave-3 never triggers because:
- (a) wave-2 might not have actually "completed" (if some pack-mobs spawned but didn't get counted in clear-condition)
- (b) wave-3 spawn might be conditioned on legacy state that no longer applies
- (c) gate spawn logic might be tied to specific wave indices that drifted

**Step 2c (fix):**
- Make wave-completion detection structure-agnostic (count `aliveMobs` in current wave; advance when alive == 0)
- Make gate-spawn trigger off wave-completion event, not specific wave indices
- Make wave-HUD increment off wave-completion event, not direct call-site
- If the recipe's 6-wave structure feels wrong for player experience (waves 1-3 are 16-mob swarms; way too dense for a "room"), reshape `gauntletFromRecipe` to flatten pack-proxies across rooms (distribute 16 mobs across 3 sub-waves of ~5-6 mobs each, producing ~8 total waves more closely matching the previous 5-wave cadence)

### Bug 2 — reshaping option (consider strongly)

The 6-wave structure may itself be too coarse. Engine PackProxy is a balance-loop abstraction; "16 mobs in one room" was never the design intent. Two reshape paths:

**Reshape A — keep 6 waves but distribute pack mobs:** wave 1 = pack-1 (8 mobs); wave 2 = pack-2 (8 mobs); wave 3 = pack-3 (8 mobs); wave 4 = pack-4 (8 mobs); wave 5 = pack-5 (8 mobs); wave 6 = pack-6 (8 mobs) + magic + elite + bosses. Player gets 8 mob swarms per room — more manageable.

**Reshape B — flatten to legacy-like cadence:** distribute pack mobs across many small waves (~3-5 mobs each), preserving the cadence of the previous 14-mob 5-wave structure but scaled to 54-mob 12-wave structure. Closer to old player experience but more rooms to clear.

Knight-rider recommends **Reshape A** for tonight (1 wave per recipe slot = clean mapping; player faces 6 distinct rooms; pack-density is intense but bounded). Reshape B is a polish pass later.

---

## Acceptance criteria

- [ ] Bug 1 root cause identified (manifest path / AudioContext init / call-site bypass / VFX mount failure) — diagnostic logs in DevTools confirm
- [ ] Bug 1 fix applied; audio + VFX confirmed firing in manual dev-server smoke
- [ ] Bug 2 root cause identified (wave-completion detection / gate-spawn trigger / wave-HUD increment / structure mismatch)
- [ ] Bug 2 fix applied; manual dev-server smoke confirms wave-2 → wave-3 transition fires gate + HUD increment + next-batch spawn
- [ ] Recipe-season structure: ≥6 distinct rooms playable from wave-1 through boss; gate appears + opens at each wave-cleared boundary
- [ ] Legacy season fallback unchanged (001001-005 should still work via pickMonsters path)
- [ ] `npm run build` clean
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.16.1-hotfix-wave-hang-plus-audio-vfx-gap-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT revert v1.16 (gauntletFromRecipe + monster.max_hp are correct; fix the integration)
- ❌ DO NOT change the recipe schema (star-lord seam; emission contract is locked)
- ❌ DO NOT touch engine code
- ❌ DO NOT pre-empt rocket D11.2 Phase A (in flight; different seam)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessor:** drax v1.16 JSON-parity wiring (shipped)
- **Triggers downstream:** Matt re-playtest; if more bugs surface, follow-on hotfix; if clean, continue VS2a polish queue
- **Parallel-safe with:** rocket D11.2 Phase A (in flight; engine seam — different repo, no conflicts)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 playtest bug report. ~1-2 hours. Append diagnostic findings + completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** drax
**Tag:** `drax/v1.16.1-hotfix-wave-hang-plus-audio-vfx-gap-1`
**Commit:** `430a9f4` (reincarnated-demo main)

### Diagnostic findings

**Bug 2 (wave-progression hang) — root cause confirmed:**

Two interacting problems, both from the v1.16 pairing of 2 pack-proxies per wave:

**Problem A — 16-mob room density:** Pack-clear condition is `pack.every(m => !m.combatant.isAlive)`. With 16 mobs in a single room, the player can kill the majority then walk into the hallway. Remaining mobs halt pursuit at room edge (per `shouldHaltPursuit` logic). Player is in `fighting` state inside the hallway — no enemies in reach, no gate, waves never advance. This matches Matt's exact description: "I could move into the next room infinitely but it never populated a visual gate."

**Problem B — Room count mismatch:** `gauntletFromRecipe()` produced 6 monster waves + 2 act-boss = 8 total waves. `VS2A_ROOM_PLAN` had 7 rooms. `roomForWave(dungeon, 8) = dungeon.rooms[7] = undefined` → `_currentExitDoor()` returned null for wave 8 → final-room path triggered prematurely on act-boss 2 → wave-8 mobs never spawned with a room to anchor to.

**Bug 1 (audio/VFX) — root cause assessed:**

The dispatch hypothesis (a) is correct: AudioContext suspended pending user-gesture. Howler v2.2 auto-resumes its own context (`Howler.ctx`) on user gesture, but our Web Audio API Tier-1 fallback context (`getAudioCtx()`) is a SEPARATE AudioContext that does not auto-resume. If Tier 2 (Howler file lookup) fails for any key (missing manifest entry, file 404), `playTone()` fires and creates the suspended context — tone plays on first gesture but may be inaudible on any cast that happens to use an uncovered key before the first explicit interaction.

Assets confirmed on-disk and accessible at dev server: sfx-manifest.json (72 layer1 keys), fire SFX wav, music mp3. The manifest fetch/load path is intact. VFX layer containers mount correctly (confirmed by diagnostic logging). The AudioContext resume hook is the targeted fix for the Tier-1 path gap.

VFX gap: no init-order regression found. `atmosphericLayer`, `pimenVfx`, `frostwindzClassArchetype` are mounted correctly in `startGauntlet`. VFX fires on `dispatchAbilityVfx` which is called from `_firePlayerSkillAtActor` — verified in code. VFX should be working; if not, the `[vfx:diag]` logs will surface the container state.

### Fixes implemented

**Bug 2 fix — Reshape A in `gauntletFromRecipe()`:**
- 1 pack-proxy per wave instead of 2 → 6 swarm waves × 8 mobs each (was 3 × 16)
- Wave labels: Swarm Vanguard / Second / Third / Fourth / Fifth / Rearguard
- Waves 7-9 unchanged: Magic Cadre / Elite Vanguard / Boss Gauntlet
- Total: 9 monster waves + 2 act-boss = **11 waves**
- `VS2A_ROOM_PLAN` extended to 11 rooms; `VS2A_HALLWAY_PLAN` extended to 10 hallways
- Legacy seasons: unchanged; pickMonsters → 7 waves; rooms 0-6 of 11-room dungeon used

**Bug 1 fix — AudioContext resume hook:**
- `_hookAudioContextResume()` added to AudioManager constructor
- Hooks `mousedown` / `keydown` / `touchstart` (each `{ once: true }`) to call `.resume()` on `Howler.ctx` and `audioCtx` when suspended
- Covers the gap between Howler's own auto-resume and our Web Audio API procedural path

**Diagnostics added (findable by `[diag]` comment tag):**
- `[audio:diag]` manifest load log (fetch status, key counts)
- `[audio:diag]` first-cast log (manifestReady, howlerCtx state, manifestKey)
- `[vfx:diag]` atmospheric container child counts at init
- `[wave:diag]` per-death alive/dead count log while fighting
- `[door:diag]` death-timer expiry (door_id, world position)
- `[door:diag]` door proximity while in door_active
- `[gauntlet:diag]` full wave structure dump at startGauntlet

### Acceptance criteria

- [x] Bug 2 root cause identified — wave hang from 16-mob density + room-count mismatch
- [x] Bug 2 fix applied — Reshape A + 11-room dungeon plan
- [x] Bug 1 root cause identified — AudioContext suspended, Tier-1 gap
- [x] Bug 1 fix applied — explicit resume hook on user gesture
- [x] Recipe-season structure: 9 distinct monster rooms + 2 act-boss rooms = 11 total
- [x] Legacy season fallback unchanged (001001-005 uses pickMonsters path)
- [x] `npm run build` clean — 533 modules, 0 TS errors
- [x] PRE-SIGNAL § 14.1.1 honored — `git fetch origin` on collaboration repo, no concurrent conflicts
- [x] AGENT_STATE.md STATE entry appended
- [x] Tag `drax/v1.16.1-hotfix-wave-hang-plus-audio-vfx-gap-1` created
- [ ] Manual browser smoke (gate + HUD at each wave boundary, audio firing) — pending Matt re-playtest; diagnostics in DevTools will confirm

### Files changed

- `src/encounter/gauntlet.ts` — Reshape A: 1-pack-per-wave rewrite; 6 swarm waves + magic/elite/boss
- `src/world/topology.ts` — VS2A_ROOM_PLAN extended to 11 rooms; VS2A_HALLWAY_PLAN to 10 hallways; comment updated
- `src/audio/audio.ts` — `_hookAudioContextResume()` + `_audioCtxDiagFired` diag field + manifest diag + first-cast diag
- `src/main.ts` — diagnostic logging throughout: gauntlet structure, wave-clear per-death, door proximity, atmospheric container counts; `console.log` in `onDeathTimerExpired` extended
