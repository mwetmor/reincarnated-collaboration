# Finding — 2026-05-25 — drax v2_narrow gear-pool + analytics

**Reviewer:** jack-ryan
**Severity:** INFO (two minor observations; no blocking issues)
**Verdict:** PASS-with-INFO
**Target:** commit `352436c` — reincarnated-loadout main (pushed to origin; Vercel auto-deployed)
**Developer:** drax
**Principles applied:** Principle 2 (smoke-gate), Principle 3 (schema boundary), Principle 6 (cross-seam impact), Principle 5 (severity triage)
**Dispatch reference:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-25-drax-v2-narrow-gear-pool-and-analytics-investigation.md`

---

## What I found

### Item 1 — Per-season gear-pool refactor (Approach A)

Root cause correctly identified and fixed. `useSeasonData.ts` now globs `../../data/*/gear_pool.json` (eager) via `gearPoolModules` and resolves per-season via `resolveGearPool(folderKey)`. `SeasonData` interface extended with `gearPool: GearPoolEntry[]` — additive, backward-compatible. `Loadout.tsx` and `Sample.tsx` both remove the hardcoded Yomi import and consume `season?.gearPool ?? []`. `GearGrid.tsx` hardcoded "Yomi Season" subtitle is fully removed (grep confirmed: no residual string in component).

Spot-check results:
- `data/season_002328/gear_pool.json` EXISTS — Yomi gear resolves via glob, no regression.
- `data/v2_narrow/gear_pool.json` ABSENT — `resolveGearPool()` returns `[]`; GearGrid renders empty slots. Correct null state for a narrow milestone with no generated gear pool.
- `Sample.tsx` line 233 confirms `const gearPool = season?.gearPool ?? [];` pattern (not hardcoded).
- No "Yomi Season" string remains in GearGrid.tsx.

### Item 2 — Analytics Engine v2 section

`isEngineV2Season(id)` predicate at SeasonSummaryCards.tsx:126 is a simple string equality check (`id === 'v2_narrow'`). v2_narrow correctly excluded from `historicalCards` filter (line 133-135). New amber-styled "Engine v2 — Narrow Milestone" section present at lines 192-207.

`seasonLabel('v2_narrow')` returns `'Narrow v1.0'` (useAnalytics.ts:128). ClassIcon.tsx iconMap entry `'v2_narrow': 'season-v2-narrow'` added with `onError` hide guard.

v2_narrow manifest data shape spot-check:
- `manifest_version: "1.3"`, `season_id: "v2_narrow"`, `anchor.name: "Moctezuma"` — present.
- `validation_passed: true`, `summary.convergence_failures: 0` — present.
- `season_theme_element: "physical"` — present.
- Class spot-check (`class_0001.json`): `dominant_element: "physical"`, `engine_version: "v2.0"`, `balance_metadata` fully populated. All analytics-required fields present.

Data shape is valid. Analytics presentation fix is correct.

### Smoke gate

Build: 813 modules, 0 TS errors per drax commit message + AGENT_STATE.md. Drax ran build twice (initial + post-GearGrid edit). No TS errors reported; this is the extent of verifiable smoke evidence from the artifact record (no CI output available for independent verification, consistent with prior Gate-2 pattern for loadout seam).

### Cross-seam impact

- No engine code amended.
- No new schema definitions — `SeasonData.gearPool: GearPoolEntry[]` is additive to an existing interface; all consumers guarded (`?? []`).
- No MIGRATION.md required — within-seam UI consumption change only; no contract change to external consumers of the loadout app.
- No decisions-log conflicts detected.

---

## Rationale

### INFO-1 — `isEngineV2Season` predicate is hardcoded string equality

`isEngineV2Season(id: string): boolean` is implemented as `id === 'v2_narrow'`. This is correct for the current narrow milestone. However, if Cycle 13 ships a second Engine v2 season with a different ID (e.g., `v2_elemental`), the predicate silently excludes it — falling back to `historicalCards` again. The function name implies a general test ("is this an engine v2 season?") but the implementation is a point check.

This is a known-forward limitation, not a current defect. The TODO(drax) annotations already track gear-pool cleanup; this is a parallel tracking note. No action required before merge.

Cite: Discipline 10 (attribution clarity — the predicate's name slightly overclaims its scope).

### INFO-2 — Decisions-log entry advisable for per-season gear-pool architecture

Approach A (per-season dynamic glob as the canonical gear-pool consumption pattern) is a structural architectural decision: all future seasons are expected to ship their own `gear_pool.json`, and the glob is the resolution mechanism. This pattern supersedes the prior hardcoded Yomi import. It warrants a decisions-log entry noting: (a) glob-per-season as the canonical pattern, (b) empty array as the correct null state for pre-gear-pool seasons, (c) TODO(drax) annotations as the cleanup tracker.

The "Engine v2 milestone" analytics category is a narrower presentation decision, not architecturally novel enough to warrant a standalone decisions-log entry — it follows the existing Yomi-section pattern. The gear-pool architecture change is the one worth logging.

Cite: Discipline 7 (capture decision telemetry — design decisions should be traceable).

---

## Action

- [ ] drax (INFO-1, optional): Consider renaming `isEngineV2Season` to `isV2NarrowSeason` or adding a comment noting it is currently a point-check, not a general engine-version predicate. Low priority — defer to next loadout session if convenient.
- [ ] knight-rider or jack-ryan (INFO-2, low priority): Add decisions-log entry for per-season gear-pool glob as canonical consumption pattern. Suggested entry: "Per-season gear-pool consumption via Vite glob (useSeasonData.ts) — Approach A — established as canonical pattern for all future seasons; empty-array fallback for seasons without gear_pool.json is the correct null state." Jack-ryan can author this directly per tiered approval authority (within-seam; no cross-seam impact).
- [ ] Matt: no action required. Both items are INFO; nothing blocks production. v2_narrow is live at `https://reincarnated-loadout.vercel.app`.

---

## References

Files reviewed:
- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts` — SeasonData.gearPool extension (lines 191-199)
- `/Users/admin/Games/reincarnated-loadout/src/hooks/useSeasonData.ts` — gearPoolModules glob + resolveGearPool (lines 14-29)
- `/Users/admin/Games/reincarnated-loadout/src/pages/Loadout.tsx` — season.gearPool consumption (lines 26-28, 359-364)
- `/Users/admin/Games/reincarnated-loadout/src/pages/Sample.tsx` — season.gearPool consumption (lines 15-17, 232-236)
- `/Users/admin/Games/reincarnated-loadout/src/components/GearGrid/GearGrid.tsx` — subtitle removal verified (grep confirmed absent)
- `/Users/admin/Games/reincarnated-loadout/src/hooks/useAnalytics.ts` — seasonLabel mapping (line 128)
- `/Users/admin/Games/reincarnated-loadout/src/components/analytics/SeasonSummaryCards.tsx` — isEngineV2Season + Engine v2 section (lines 123-128, 130-207)
- `/Users/admin/Games/reincarnated-loadout/src/components/ui/ClassIcon.tsx` — v2_narrow iconMap entry (lines 28-30)
- `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/manifest.json` — data shape verification
- `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/classes/class_0001.json` — class data shape spot-check
- `/Users/admin/Games/reincarnated-loadout/AGENT_STATE.md` — drax session checkpoint
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-25-drax-v2-narrow-gear-pool-and-analytics-investigation.md` — dispatch + completion record
