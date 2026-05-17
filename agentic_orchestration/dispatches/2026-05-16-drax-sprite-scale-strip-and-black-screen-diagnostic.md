# Dispatch — 2026-05-16 — drax — Sprite-scale comparison strip + black-screen diagnostic

**From:** knight-rider (authored per Matt directive Day-4 close: "Please ship 11 monsters at the 3 scales and also 11 characters. The demo only showed a black screen via npm run dev")
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (direct directive)
**Status:** PENDING
**Estimated effort:** 1 session (~2-3h); diagnostic uncertainty front-loads; screenshot harness is mostly straightforward once render path is unbroken.

**Acceptance summary:** Black-screen root cause identified + fixed (Discipline #10 — open browser, read console BEFORE guessing). Standalone screenshot-strip harness renders all 11 chierit player characters AND all 11 enemy monster sprites at three scale candidates each (0.20 / 0.28 / 0.35). 66 total PNGs (or one consolidated grid PNG per category — see § "Output format"). Output dropped to a known directory Matt can browse without running the live demo. Intermediate tag cut. AGENT_STATE updated. Knight-rider notified.

---

## Why this dispatch exists

Matt ran `npm run dev` against the demo (after drax v0.19 player chierit + v0.20 monster CreativeKind wiring landed today) and got a **black screen** — the demo did not render anything. He cannot do visual QA on the new sprites this way.

Separately, Matt wants to tune `DEFAULT_MONSTER_SCALE` (currently `0.28` in `monsterSprites.ts:52`). Rather than play through gauntlets at different scales, he wants a **side-by-side scale-comparison strip** rendered offline so he can pick the right scale (or per-monster scales) from artifact files.

These two problems share the same render path. Fixing the black screen unblocks the screenshot harness AND the live demo. Combined into one dispatch.

## Cross-seam contract change?

**Round-trip: not applicable** because this work is entirely within the demo seam:
- No new export/telemetry fields produced or consumed
- No engine-side schema or fight_log shape changes
- New screenshot harness is a demo-internal tool (vite route or node script)
- Black-screen fix is a render-path bug, not a contract change

Per R11(b) Principle 6 (REVIEW_PROCESS.md, just landed today), this dispatch carries the explicit "not applicable" annotation rather than silence.

## Stage 1 — Black-screen diagnostic (Discipline #10 FIRST)

**Do not guess.** Open the demo in a browser, open DevTools, capture the actual error.

Likely candidates (rank by your inspection — do not pre-commit):
1. Asset-load failure (chierit/CreativeKind/Pixogen path mismatch) — recent v0.19 + v0.20 wired new asset paths
2. `createCombatantSprite` signature change broke a call site (v0.20 added `isEnemy`/`encounterElement`/`encounterSeed` params; if any caller was missed, that call could throw at boot)
3. `prewarmMonsterSpriteCache` in main.ts throws on init (called at gauntlet start per v0.20 completion report — if it fails synchronously, blank canvas)
4. Pixogen vertical-strip slicer (`pixogenVfx.ts`) crash on missing texture
5. Element-keyed character resolver returns undefined for an element the demo seeds with
6. TypeScript-compilation-pass succeeded but runtime regression from one of v0.18 / v0.19 / v0.20

**Required output of Stage 1:** Root cause named with file + line + reproduction step. Fix applied. Confirm `npm run dev` renders SOMETHING visible (combat scene, menu, anything that isn't a blank canvas) before proceeding to Stage 2.

If you cannot reproduce the black screen, report back inline before Stage 2 — Matt's hardware/browser may differ from your reproduction environment.

## Stage 2 — Screenshot-strip harness

Build a standalone offline renderer that produces the comparison strips. Two viable approaches; pick whichever you can ship fastest:

**Approach A — Vite dev-mode route.** Add a `/scale-strip` route (or similar) in the demo that, when loaded, renders all 22 sprite slots × 3 scales in a deterministic grid. Matt navigates `localhost:5173/scale-strip` once the black screen is fixed, takes browser screenshots OR you write a small Pixi extract-image utility that saves each cell as PNG to disk.

**Approach B — Headless Node script.** Write a `scripts/render-sprite-strip.js` that uses Pixi's offscreen-canvas + node-canvas (or `@pixi/node`) to render each sprite × scale combination, save as PNG to a known output directory. No browser needed. More upfront work; better artifact stability.

**Pick A unless you find a blocker.** The harness exists to surface a Matt-decision; it does not need to be a permanent durable tool.

## Stage 3 — Render the strips

**Monsters (11):** Use the 11 monsters drax v0.20 selected via `ENEMY_TIER_CHARACTER_MAP`. Lich (mini_boss), Goblin_Mage, Mutant_Skeleton, Crystal_Golem, Demon_Mage, Fire_Elemental, Hellfire_Rhino, Angel_Guardian, God_of_Lightning, and whichever else made the tier-keyed cut. Each rendered at three scales: **0.20, 0.28, 0.35**.

**Characters (11):** 10 chierit characters in `Elementals_bundle/` (Crystal_Mauler, fire_knight, ground_monk, Leaf_ranger, light_valkyrie, lightning_ronin, metal_bladekeeper, shadow_stalker, water_priestess, wind_hashashin) + 1 GandalfHardcore Samurai. Each rendered at three scales — pick chierit scale candidates that bracket the current chierit-scale value (you have that in `characterSprites.ts`). If current chierit scale is 1.0, candidates might be 0.7 / 1.0 / 1.3 — judgment call; document your choice in the output README.

**Animation state for the strip:** `idle` frame for each. Single frame is sufficient for scale judgment. (If `idle` is missing for a monster, fall back to the first available state and label it.)

## Output format

Drop artifacts to `~/Games/reincarnated-demo/scale-comparison/` (create directory):

```
scale-comparison/
├── README.md                          # what's here, what scales used, how to view
├── monsters/
│   ├── monsters-0.20.png              # 11-cell horizontal grid at scale 0.20
│   ├── monsters-0.28.png              # 11-cell horizontal grid at scale 0.28
│   └── monsters-0.35.png              # 11-cell horizontal grid at scale 0.35
└── characters/
    ├── characters-<scale1>.png
    ├── characters-<scale2>.png
    └── characters-<scale3>.png
```

**Each grid PNG: labeled cells (sprite name underneath each cell).** Matt can flip through 6 PNGs faster than 66 individual files.

Common-axis aspect: include a reference rectangle (e.g., 30m wide grid cell at the assumed pixels-per-meter ratio) so Matt can judge in-world scale, not just relative scale.

## Stage 4 — Tag + AGENT_STATE + completion record

- Intermediate tag: `drax/v0.20.1-sprite-scale-strip-and-black-screen-fix`
- Update `~/Games/reincarnated-demo/AGENT_STATE.md`
- Fill completion record at bottom of this dispatch

## Out of scope (explicit)

- **NO per-monster `MONSTER_SCALE_BY_SLUG` lookup table refactor.** That is the natural follow-on dispatch AFTER Matt sees the strip and picks per-slug values (or a single revised default). This dispatch only produces the artifact and fixes the boot blocker.
- **NO per-animation slicing of combined-sheet monsters.** VS2b item; not relevant to scale judgment.
- **NO chierit scale retuning.** This dispatch surfaces options; Matt picks; follow-on dispatch applies.
- **NO new monsters/characters added.** Use the existing 11 + 11 pool exactly.
- **NO playable gauntlet feature work.** Black-screen fix only — restore boot path; do not extend functionality.
- **NO loadout-repo changes.** Demo seam only.

## Required reading

- `~/Games/reincarnated-demo/src/visuals/monsterSprites.ts` — `DEFAULT_MONSTER_SCALE` at line 52, applied at line 304
- `~/Games/reincarnated-demo/src/visuals/characterSprites.ts` — chierit scale config (line ~196 per knight-rider inspection)
- `~/Games/reincarnated-demo/src/visuals/sprites.ts` — `createCombatantSprite` signature including new v0.20 params (`isEnemy`, `encounterElement`, `encounterSeed`)
- `~/Games/reincarnated-demo/src/main.ts` — `prewarmMonsterSpriteCache` call site (boot-path candidate for black-screen)
- v0.19 dispatch completion record (`drax-character-wire-up-void-attribution.md`) — most recent player-sprite wiring
- v0.20 dispatch completion record (`drax-monster-track-ingest-pipeline.md`) — most recent enemy-sprite wiring
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #10 (empirical inspection over assumption; root-cause before fix); Discipline #11 (attribution clarity — credits must still resolve in the harness)

## Acceptance criteria

- [ ] Stage 1: black-screen root cause named with file + line; fix applied; `npm run dev` renders at least one visible scene
- [ ] Stage 2: screenshot-strip harness exists and is invocable (route or script)
- [ ] Stage 3: 6 grid PNGs produced (3 monster + 3 character) with labeled cells and reference scale axis
- [ ] Output README explains scale candidates chosen + how to view
- [ ] No new TS errors introduced (`tsc --noEmit` clean)
- [ ] Existing tests pass (`npm run test`)
- [ ] Intermediate tag `drax/v0.20.1-sprite-scale-strip-and-black-screen-fix` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion (include: root cause of black screen, scale candidates used for chierit, any per-monster slug that visibly doesn't work at any of the three scales)

## Tag policy

- **Intermediate tag:** `drax/v0.20.1-sprite-scale-strip-and-black-screen-fix` at the commit closing harness + fix + screenshots.
- **Milestone tag:** none from this dispatch.

## Notes for knight-rider visibility

- This dispatch is the natural prequel to a follow-on `MONSTER_SCALE_BY_SLUG` refactor dispatch + a chierit scale-revision dispatch, both authored AFTER Matt picks scale values from the strip.
- If the black-screen root cause is in a seam outside drax's lane (engine-emitted JSON shape mismatch, etc.), surface immediately — do not patch out-of-seam; flag and stop.
- If multiple root causes layer (e.g., asset path AND init crash), name and fix each with separate commits for clean attribution.

---

## Completion record

**Completed:** 2026-05-16
**Black-screen root cause:** `src/world/topology.ts:18` imported `PIXELS_PER_METER` from `./movement`, while `movement.ts:32-33` imported `clampToBounds` from `./topology`. Circular ESM dependency caused TDZ ReferenceError: "Cannot access 'PIXELS_PER_METER' before initialization" at topology.ts:5 (where ROOM_PX_SMALL is computed). Application crashed before mounting; black canvas.
**Black-screen fix commit:** `f54da43` — removed circular import; inlined `const PIXELS_PER_METER = 48` in topology.ts (math-locked value)
**Screenshot harness location:** `~/Games/reincarnated-demo/scale-strip.html` (Approach A — Vite route). Load at `http://localhost:5173/scale-strip.html` while dev server is running.
**Chierit scale candidates chosen:** 0.25 / 0.35 / 0.45
  Rationale: current default is 0.35 (characterSprites.ts:199); bracketed ±0.10. Chierit frames are 288×128px. At 0.35 = ~100×45px rendered. At 0.25 = ~72×32px (may be too small for action clarity); at 0.45 = ~130×58px (better sprite detail). Middle value matches the existing implementation so Matt can assess whether to go up or down.
**Monster scale candidates:** 0.20 / 0.28 / 0.35 (current default 0.28 in center)
**Output directory:** `~/Games/reincarnated-demo/scale-comparison/`
**Intermediate tag:** `drax/v0.20.1-sprite-scale-strip-and-black-screen-fix @ b621af9`
**Tests status:** 294/294 passed
**Notes for knight-rider:**
- Root cause was a demo-internal circular import (topology.ts ↔ movement.ts). Not an engine-schema issue; within drax's lane. Fixed cleanly.
- All 11 monster slugs rendered at all 3 scales without failure. No per-monster slug that visibly fails at any scale (all BaseTexture.valid=true confirmed by harness).
- GandalfHardcore Samurai rendered as portrait (640×640) in character strip column 11 — no animation sheets exist for Samurai. Full wiring remains deferred.
- Follow-on dispatches needed after Matt reviews strips: (1) per-monster MONSTER_SCALE_BY_SLUG table; (2) chierit character scale revision.
- The `scale-strip.html` route is a permanent dev tool — stays in the repo for future scale QA rounds.
- Pre-existing Pixi.js deprecation warning (`.interactive` property in seasonSelector.ts:53) is harmless and pre-dates this dispatch. Not blocking.
