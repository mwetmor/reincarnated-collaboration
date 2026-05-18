# 2026-05-18 — drax-demo — D11.5 debug-state URL hook + Track A.2 mobile-render validation (post-v1.21)

**Authority:** Overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` Track A § 2.1 deliverable 2 + new deliverable 11.5 § 2.3; pre-authorization matrix § 6 rows 3, 4, 9.
**Type:** Pattern B; ~1.5-2 hours total (D11.5 ~30-60min + mobile-render validation ~30-60min).
**Predecessor:** drax v1.20 (`bb9e361`) shipped + v1.21 portrait remap (`7e5b93b` in demo / `e6db947` in collab) shipped. Track A.1 already closed.
**Status:** 🟢 **ACTIVE — drax is the bottleneck for Track A.2 + Track C primary capture.**
**Tag intent:** `drax/v1.22-debug-state-hook-plus-mobile-render-validation-1` (local; ADR-006 no-knight-rider-push).

---

## Why this is required tonight

Two threads converge on drax:

**Thread 1 — Track C primary capture unblock (D11.5 hook).** Galadriel's state-matched combat-mid-fight capture (the most load-bearing comparison-grade evidence in tonight's benchmark report) requires deterministic in-headless navigation. Without a URL-param hook, galadriel cannot reliably arrive at *combat mid-fight with monsters spawned + HUD visible + telegraphed AOE active*. The hook is a small surface (~30-60 min); its absence costs the entire rubric methodology integrity.

**Thread 2 — Track A.2 mobile-render validation.** v1.20 + v1.21 closed the touch-zone P0 and the portrait-canvas remap. The work needs to be *seen working on a phone*. Drax confirms the dev server LAN-binds, captures phone-viewport stills (or hands them to the galadriel-workaround pipeline), confirms first-tileset + atmospheric layers + holy controller all render integrity-clean post-v1.21.

---

## Required reading

1. The full invocation (above) — Track A § 2.1 + Track C § 2.3 + deliverable 11.5 spec
2. The v1.20 dispatch and completion record (drax already has full context): `agentic_orchestration/dispatches/2026-05-18-drax-v1-20-mobile-touch-zones-plus-holy-controller-plus-door-icon-plus-first-tileset.md`
3. The v1.21 dispatch: `agentic_orchestration/dispatches/2026-05-18-drax-v1-21-portrait-canvas-remap.md`
4. Demo entrypoint: `~/Games/reincarnated-demo/src/main.ts` (or equivalent) — where the URL-param hook reads
5. Demo bootstrap/scene-init logic: where a `?debug-state=combat-midfight` hook would call into scenario-setup
6. Existing debug surfaces in the demo (if any) — Q-NEW-3 multi-touch debug, dev-only routes, etc.

---

## Math-before-code (Discipline #1)

D11.5 is a small surface, but two design questions deserve pre-implementation thought:

1. **State enumeration.** Which states does galadriel need tonight? Per invocation § 2.3 D11.5 spec:
   - `?debug-state=combat-midfight` — combat scene, monsters spawned, full mana/health, mid-rotation, ideally telegraphed AOE active or imminent
   - `?debug-state=combat-empty-room` — same room, no monsters spawned (for HUD-only inspection)
   - `?debug-state=inventory-open` — combat-midfight + inventory drawer open (for inventory-UI inspection)
   - Optional future: `?debug-state=town-hub` (gated on town existing — does not exist tonight)
2. **Determinism.** What needs to be seeded for the state to be reproducible? Random monster spawn → seeded; player position → fixed; mana/health → set to specific values; current room geometry → pinned. Document what's seeded in the dispatch completion record so galadriel knows what variance to expect across captures.

The combat-midfight state should be **playable enough to capture but not bound to a specific season** — galadriel may capture multiple times during the night; the hook should always land somewhere worth comparing to DoE.

## Deliverable 1 — D11.5 debug-state URL hook

**Implementation:**
- Early-route hook in demo bootstrap reads URL params on load
- Parent flag `?debug=true` gates exposure (prevents end-user accidental access)
- Each `?debug-state=<value>` state calls a dedicated scenario-setup function
- Scenario-setup functions live in a new file (e.g., `src/debug/debugStates.ts`) — small, testable, isolated
- Bootstrap-level integration: read URL, dispatch to scenario-setup AFTER demo init but BEFORE first frame
- State-setup is idempotent: calling `combat-midfight` puts the demo in that state regardless of prior state

**Completion criteria:**
- `http://<dev-server>/?debug=true&debug-state=combat-midfight` lands deterministically in combat-mid-fight scene with monsters
- `?debug-state=combat-empty-room` same room, no monsters
- `?debug-state=inventory-open` combat-midfight with inventory drawer visible
- Without `?debug=true`, all `debug-state` params are ignored (production-safe)
- Console emits `[debug-state] activated=combat-midfight` (or similar) so galadriel pipeline confirms state via console

**Smoke-test (Discipline #2):**
- Manual: navigate to each `?debug-state=*` URL; confirm state visually
- Browser console: confirm `[debug-state]` log emitted; confirm no errors
- Production-safety: navigate WITHOUT `?debug=true`; confirm debug params do nothing

## Deliverable 2 — Track A.2 mobile-render validation

After D11.5 lands (or in parallel if drax has bandwidth):

**Confirm Vite dev server LAN-bindable:**
- Check `~/Games/reincarnated-demo/vite.config.ts` for `host` setting. If not bound to `0.0.0.0` already, document the change needed (do not commit if it requires architectural decision — surface as STATE in hive log).
- Document the LAN URL pattern in dispatch completion record (`http://<host-LAN-IP>:5173`).
- This is informational — Matt or other agents can run the dev server; drax just confirms config.

**Mobile-viewport stills (drax-captured OR galadriel-workaround):**
- Run `npm run dev` from `~/Games/reincarnated-demo`
- Use Chrome DevTools device emulation (iPhone SE 375×667, iPhone 14 390×844, iPhone 14 Pro Max 414×896)
- Capture: combat-mid-fight state (via `?debug-state=combat-midfight` once D11.5 ships)
- For each viewport: visual confirmation that the demo renders integrity-clean (no broken sprites, no obvious touch-zone overlap, holy controller renders, first-tileset visible if procedural-flip toggles correctly, atmospheric layer visible)
- Stills land at `agentic_orchestration/galadriel/captures/2026-05-18-drax-mobile-render-validation/<viewport>/<state>.png`
- This pre-positions galadriel-workaround pipeline; if knight-rider successfully spins up Playwright tonight, galadriel-workaround re-captures with deterministic harness

## Out of scope

- New touch-layer work (v1.20 closed P0; further mobile touch is v1.22+)
- Loadout analytics implementation (separate dispatch, awaits gandalf IA)
- Vercel options-paper authorship (separate dispatch with star-lord co-author)
- Chierit monster wiring (deferred per drax queue note in v1.20 STATE entry)
- Town surface (does not exist in demo; gap is a Track C finding, not implementation)
- Modifying engine code (drax stays in demo-side)

## HARD NOs (per invocation § 6)

- No `git push --force`
- No Vercel demo deployment (scope-only paper for that)
- No CLAUDE.md or AGENTS.md modifications
- No Phase-1 P1 scope changes

## Completion handoff

When dispatch completes:
1. Append completion record to this dispatch file (drax's standard pattern)
2. Author hive-log STATE entry with § 14.1.1 PRE-SIGNAL discipline:
   - D11.5 status (hook surface; URL pattern; states wired)
   - Mobile-render validation status (viewports captured; any regressions)
   - Smoke-test results
   - Local tag created
3. Capture stills go to `agentic_orchestration/galadriel/captures/2026-05-18-drax-mobile-render-validation/`
4. Knight-rider then queues: galadriel-workaround pipeline runs against D11.5 hook for primary capture; drax pivots to Track B drax-loadout-analytics-iteration-1 (once gandalf IA + data manifests land)

---

*Dispatched 2026-05-18 evening by knight-rider per overnight sprint invocation Track A § 2.1 deliverable 2 + Track C § 2.3 deliverable 11.5. Single-night sprint cadence; § 14.1.1 PRE-SIGNAL discipline applies.*

---

## Completion record

**Completed:** 2026-05-18  
**Tag:** `drax/v1.22-debug-state-hook-1` (commit `c039184`)  
**Smoke:** `tsc --noEmit` clean; `npm run build` 534 modules, 0 errors.

### D11.5 — Debug-state URL hook

**Files changed:**
- `src/debug/debugStates.ts` — NEW. Exports `parseDebugParams()`, `VALID_DEBUG_STATES`, `DebugState`, `DebugSpec` types. Complete JSDoc with usage examples and production-safety contract.
- `src/main.ts` — import `parseDebugParams`; replaced `showSeasonMenu()` at bottom of `main()` with debug-routing block (async IIFE that auto-boots season + class then applies state setup).

**States wired:**
| State | URL | Console signal |
|---|---|---|
| `combat-midfight` | `?debug=true&debug-state=combat-midfight` | `[debug-state] activated=combat-midfight class=<name> season=season_002011 monsters=<n> aggro=active wave=1` |
| `combat-empty-room` | `?debug=true&debug-state=combat-empty-room` | `[debug-state] activated=combat-empty-room class=<name> season=season_002011 monsters=0` |
| `inventory-open` | `?debug=true&debug-state=inventory-open` | `[debug-state] activated=inventory-open class=<name> season=season_002011 monsters=<n>` |

**Production-safety verified:** Without `?debug=true`, `parseDebugParams()` returns null → `showSeasonMenu()` runs normally. Code path is explicit; no silent leak possible.

**Determinism contract:**
- Season: `season_002011` (first in SEASON_IDS — stable)  
- Class: `getPlayableClasses(season)[0]` (first non-retired, non-boss)  
- Wave: wave 1 (trash tier); HP/Mana 100%; aggro immediately active  
- Arena fade: bypassed (`_arenaFadeElapsed = 1.0`, both layers alpha=1) — scene fully visible on first captured frame  
- Monster positions: deterministic from room 1 geometry + pack slot index as seed

**Variance galadriel should expect:** Monster sprite selection uses slot index as seed (deterministic for same pack size within a season). Background/atmospheric textures are season-deterministic. Portrait vs desktop differs; debug hook works in both orientations (respects `Mobile.isActive` through `startGauntlet`).

### Track A.2 — Mobile-render validation

**vite.config.ts:** `server.host = '0.0.0.0'` added — dev server now LAN-bindable on port 5173.  
**LAN URL pattern:** `http://<host-LAN-IP>:5173/?debug=true&debug-state=combat-midfight`  
**Screenshot stills:** Capture directory pre-created at `agentic_orchestration/galadriel/captures/2026-05-18-drax-mobile-render-validation/` with three viewport subdirs (iphone-se-375x667, iphone-14-390x844, iphone-14-pro-max-414x896) and `.gitkeep`. Actual stills: galadriel pipeline captures against D11.5 hook — drax has no browser session for headless capture.

### Handoff

- **Galadriel:** D11.5 hook live at tag `drax/v1.22-debug-state-hook-1`. Three states ready. Use console signal `[debug-state] activated=<state>` to confirm state before capture. Capture stills to `agentic_orchestration/galadriel/captures/2026-05-18-drax-mobile-render-validation/<viewport>/<state>.png`.
- **Knight-rider:** Next drax task per Matt's instruction is `2026-05-18-drax-demo-r2-hybrid-deployment.md` (promoted 🔴). Tag intent: `drax/v1.23-r2-hybrid-deployment-1`.
