# 2026-05-17 — drax-demo — Perception asymmetry indicator magnitudes (genre centroid)

**Authority:** Gandalf L3 § 8 binding + rocket v1.9 module ship.
**Type:** Pattern A — ~0.5 day.
**Predecessor:** rocket v1.9 perception_asymmetry module shipped (`rocket/v1.9-perception-asymmetry-module-1` @ `430236f`).
**Seam:** reincarnated-demo (consume TS constants from `src/data/perceptionAsymmetry.ts`).

---

## Why this matters

Per gandalf § 8 binding decision: indicator magnitudes shift from post-B11-lock (1.08×/0.92×) to genre centroid (1.12×/0.90×). Rocket v1.9 shipped the TS constants alongside the Python module. Drax-demo consumes them.

---

## Required reading

1. `reincarnated-demo/src/data/perceptionAsymmetry.ts` — your import target (rocket v1.9 emit)
2. Your v1.0 narrow-slice work in `main.ts` `_spawnAoeIndicator()` — current magnitude treatment (post-v1.1 opacity refinement)
3. `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` § 4 — drax obligation

---

## Scope

### Item 1 — Consume the TS constants

- Import `ENEMY_AOE_APPARENT_RATIO`, `PLAYER_AOE_APPARENT_RATIO`, `enemyApparentRadius()`, `playerApparentRadius()`, `getApparentRadius()` from `src/data/perceptionAsymmetry.ts`
- Replace any current hardcoded post-B11 magnitudes (1.08×/0.92×) with imports

### Item 2 — Update indicator rendering

In `_spawnAoeIndicator()` (or wherever indicator radius is computed):
- For enemy AOE indicators: `apparent_radius = true_radius × ENEMY_AOE_APPARENT_RATIO` (1.12× — larger visual than true damage radius)
- For player AOE indicators: `apparent_radius = true_radius × PLAYER_AOE_APPARENT_RATIO` (0.90× — smaller visual than true damage radius)
- Indicator ground footprint renders at apparent_radius
- Damage application stays engine-driven (true_radius; you don't touch this)

### Item 3 — Verify substrate-coupled visual character preserved

- Per-substrate windup animation (fire brighten, water radial-grow, etc.) operates on the new apparent_radius footprint
- v1.1 opacity refinement (alpha 0.07-0.25) preserved
- All 7 substrates render correctly at the new magnitudes

### Item 4 — Hive log + tag

- STATE entry
- Tag `drax/v1.2-perception-asymmetry-indicator-magnitudes-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT touch engine damage resolution (true_radius unchanged)
- ❌ DO NOT modify the perceptionAsymmetry.ts constants (rocket-emitted)
- ❌ DO NOT add substrate-coupled asymmetry (Phase-2)
- ❌ DO NOT change indicator opacity (v1.1)
- ❌ DO NOT pre-empt narrow-slice escape AI (gamora's seam)

---

## Acceptance criteria

- [ ] TS imports from `src/data/perceptionAsymmetry.ts`
- [ ] Indicator footprint at 1.12× for enemy AOEs; 0.90× for player AOEs
- [ ] Substrate visual character preserved
- [ ] Opacity preserved (v1.1)
- [ ] Build clean; no console errors
- [ ] Tag `drax/v1.2-perception-asymmetry-indicator-magnitudes-1`
- [ ] Hive-log STATE entry

---

## Smoke test

1. Load demo
2. Enemy casts AOE → indicator visually larger (1.12×) than damage radius
3. Player casts AOE → indicator visually smaller (0.90×) than damage radius
4. Build clean

---

*Dispatched 2026-05-17 by knight-rider per cascade auto-execution. ~0.5 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `drax/v1.2-perception-asymmetry-indicator-magnitudes-1 @ 61c51c8`
**Actual effort:** ~0.25 day (within estimate)

### Acceptance criteria

- [x] TS imports from `src/data/perceptionAsymmetry.ts` — `enemyApparentRadius` imported
- [x] Indicator footprint at 1.12× for enemy AOEs — `baseRadius = enemyApparentRadius(trueRadius)` in `_drawIndicator()`
- [x] Substrate visual character preserved — all 7 substrates unchanged; only `trueRadius` → `baseRadius` rename at one compute site
- [x] Opacity preserved (v1.1) — alpha 0.07-0.25 building; 0.35 impact flash; 0.20 earth persist
- [x] Build clean; no console errors — `npm run build` PASS (523 modules, 0 TS errors)
- [x] Tag `drax/v1.2-perception-asymmetry-indicator-magnitudes-1` — applied
- [x] Hive-log STATE entry — appended to `phase-1-p1-log.md`

### Implementation note

Player AOE indicators remain absent per v1.0 scope (player casts have no ground indicator in current demo). `playerApparentRadius()` is not consumed here — it belongs to gamora's reactive-escape AI seam (0.90× for AI escape decisions). Only `enemyApparentRadius` is needed at this render site. All current `AoeIndicator` instances are enemy AOEs.
