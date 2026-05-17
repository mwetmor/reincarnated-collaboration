# 2026-05-17 — drax-demo — v0.31 Dodge cooldown reset bug + VFX timing fix

**Status:** QUEUED — auto-spawn after `drax/v0.30-wall-trap-fix-1` (or whatever v0.X-tag it ships under) lands.
**Authority:** Matt L3 disposition 2026-05-17 (playtest observations on v0.26 cosmetic dodge primitive).
**Type:** Pattern A (short task) — ~30-60 minutes estimated (two targeted fixes on existing code).
**Predecessor:** drax v0.30 wall-trap fix (in queue).
**Seam:** reincarnated-demo (Pixi.js) — your existing v0.26 dodge code; no engine, simulation, or loadout work.

---

## Why this matters

Matt's playtest observation on the v0.26 cosmetic dodge:
> *"Regarding the dodge roll. It works once only. Is there a cooldown? I cannot dodge a second time at all. And it seems like there is a cool lightning effect attached to the dodge, but the lightning dodge VFX fires too late, after the dodge happened and seems odd."*

Two distinct bugs in your v0.26 implementation:
1. **Dodge cooldown never resets** — works once, then permanently blocked. v0.26 spec was 0.75s cooldown; should be tappable repeatedly with that interval.
2. **Element-colored particle VFX timing** — particles render AFTER the dash completes instead of DURING the dash interpolation. v0.26 spec was "5 fading element-colored circle particles per frame during dash" — emphasis on "during."

Both are localized targeted fixes on your existing code (no scope expansion).

---

## Required reading (in order)

1. Your v0.26 work in `reincarnated-demo/src/main.ts` (~line 590, ~line 1770, ~line 2050 per your v0.26 completion record) — dodge state machine + VFX particle spawn
2. `reincarnated-demo/src/input/input.ts` — Shift binding from v0.26
3. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — this dispatch context + Matt's observation

---

## Scope (2 bug fixes)

### Item 1 (HIGH) — Dodge cooldown reset bug

**Symptom:** First Shift-press triggers dodge. Subsequent Shift-presses do nothing — even after >0.75s elapsed. State appears permanently locked after first use.

**Hypotheses (in likelihood order):**

1. **Cooldown timer never decrements** — `_dodgeCooldown` is set to 0.75 on dodge trigger but never reduced in the per-frame update loop. Audit the frame-update path for the dodge state machine.
2. **`_dodgeAvailable` flag stuck false** — flag set to false on dodge trigger; cleanup callback at dodge-end fails to reset it.
3. **Dodge state remains "active"** — `_dodgeActive` flag set true on dodge trigger; cleanup at dash-end (after 0.18s) fails to set false; subsequent inputs see "already dodging" and short-circuit.
4. **Dash duration timer counts up but exit-condition compares against wrong value** — e.g., `dodgeElapsed >= dodgeDuration` check uses stale constant.

**Fix:**
- Audit the dodge state machine: trigger → active-dash → cleanup → cooldown-tick → ready
- Verify each state transition fires correctly
- Ensure cooldown ticks DOWN on each frame's `deltaTime`; when it hits 0, dodge becomes available again
- Specifically verify `clearUI()` cleanup path from v0.26 doesn't permanently kill state if invoked unexpectedly
- Add console.log instrumentation if needed for diagnosis (remove or gate behind a DEBUG flag before ship)
- Smoke test: tap Shift; wait 1s; tap Shift again; second dodge should fire. Tap Shift rapidly: only first within cooldown window should fire.

### Item 2 (MEDIUM) — VFX timing fix (particles during dash, not after)

**Symptom:** Element-colored particle VFX is visible but renders at the wrong time — after the dash motion completes, particles appear at the player's post-dash position instead of trailing behind during the dash interpolation.

**Hypothesis:** Particle spawn callback is registered at dash-end completion event instead of inside the per-frame dash interpolation loop. Result: 5 particles spawn at end-of-dash position, fade from there.

**Fix:**
- Audit the particle spawn logic: when does it fire? Should be: during dash interpolation (the 0.18s ease-out animation), spawning particles each frame at the *current* interpolated player position.
- Move the spawn call (if mis-placed) from end-of-dash callback to per-frame inside the dash-active update path.
- Particles should trail BEHIND the player as the player moves forward, creating a motion-streak read
- Each particle's lifetime: ~150-300ms (long enough to be visible after the dash ends, since particles continue fading from their spawn position)
- Color: continue to use element-colored per active class's substrate (this part likely works; the timing fix is the load-bearing change)

**Visual smoke:** Tap Shift while moving; observe element-colored particles trailing the player along the dash path (multiple positions over the dash duration), not bunched at end-position.

---

## Out of scope (DO NOT)

- ❌ DO NOT redesign the dodge mechanic (this is targeted bug-fix on cosmetic v0.26)
- ❌ DO NOT add i-frames, damage prevention, or engine integration (canonical engine-coupled dodge is queued separately per gandalf L3 narrow slice work)
- ❌ DO NOT change the Shift key binding or direction-priority logic
- ❌ DO NOT modify v0.27/v0.28/v0.29/v0.30 work
- ❌ DO NOT extend scope to other dodge-related polish (substrate-VFX-coupling animation hooks come later in drax narrow-slice work per gandalf § 5.1)
- ❌ DO NOT touch engine, simulation, or loadout files

---

## Acceptance criteria

- [ ] Multiple consecutive dodges work (tap Shift, wait 1s+, tap again — both fire)
- [ ] Rapid taps within cooldown window correctly suppress all but the first
- [ ] After Nth dodge, N+1th dodge still works (no permanent lock after first use)
- [ ] Element-colored particles spawn DURING the dash (multiple positions along the dash path)
- [ ] Particles trail behind player; no clump at end-position
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Tag `drax/v0.32-dodge-cooldown-and-vfx-timing-fix-1` (or next available v0.X-tag)
- [ ] Hive-log STATE entry documenting root cause of cooldown bug + particle timing fix

---

## Smoke test expectation

1. Load demo
2. Tap Shift → dodge fires; element-colored particles trail player along dash path
3. Wait 1 second → tap Shift again → second dodge fires cleanly
4. Tap Shift rapidly 5 times within 0.5s → first fires; others suppressed (no error)
5. Continue dodging across 30s+ of play → no permanent lock; cooldown works reliably
6. Particles look right (trail not clump)

---

## Math-before-code requirements

N/A — bug-fix on existing UI code.

---

## Tag intent

`drax/v0.32-dodge-cooldown-and-vfx-timing-fix-1` (or next available v0.X-tag).

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

*Queued 2026-05-17 by knight-rider per Matt L3 disposition. Spawn after v0.30 ships. Estimated 30-60 min. Append completion record when done.*

---

## Completion record

**Status:** COMPLETE
**Date:** 2026-05-17
**Agent:** drax
**Commit:** `ed37a2a`
**Tag:** `drax/v0.31-dodge-cooldown-and-vfx-timing-fix-1`
**Actual time:** ~25 min

### Bug 1 — Cooldown never resets

Root cause: `_tickDodge` was called at the game-loop call site only when `_dodge.active` was true (`if (_dodge.active) _tickDodge(...)`). After the dash completes, `_dodge.active = false` and `_dodge.cooldown = 0.75` are set inside `_tickDodge`. On all subsequent frames, the call-site guard prevents `_tickDodge` from running, so the cooldown counter never decrements — permanently locking the dodge state.

Fix: removed `if (_dodge.active)` guard at call site. `_tickDodge` now runs unconditionally every frame. The cooldown tick at the top of `_tickDodge` runs whether or not active; the function early-returns after the cooldown tick when not active (movement interpolation and particle spawn are skipped). Change: 1 line at call site (removed guard); added inline comment explaining why the always-tick pattern is required.

### Bug 2 — VFX clump at endpoint

Root cause: `_spawnDodgeTrail(playerPos.x, playerPos.y, ...)` was called AFTER `playerPos` was updated to the new interpolated position within `_tickDodge`. Every frame's particles appeared at the player's current forward position, not behind them. The final frame's particle cluster (at the dash endpoint, most recently spawned) was the most visually prominent and lingered, creating the "fires after the dodge" read.

Fix: capture `trailX = playerPos.x`, `trailY = playerPos.y` BEFORE the interpolation update, then pass `trailX/trailY` to `_spawnDodgeTrail`. Particles now spawn at the player's prior-frame position, producing a streak of fading circles behind the dash direction across the ~11 frames of the 0.18s dash.

### Smoke test

`npm run build` PASS. TypeScript clean. Vite 16.20s. No console errors during build.

### Acceptance criteria verified (at code level)

- Multiple consecutive dodges: cooldown now decrements; second+ dodges fire after 0.75s
- Rapid taps within cooldown: `_startDodge` guard `if (_dodge.active || _dodge.cooldown > 0) return` still blocks; only first fires
- No permanent lock: confirmed — `_dodge.cooldown` decrements to 0 each frame after dash
- Particles spawn DURING dash: `_spawnDodgeTrail` called inside `_tickDodge` while active, per-frame
- Particles trail behind: pre-update position captured as `trailX/trailY`; spawn at prior position
- Build clean: PASS
