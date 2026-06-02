# Finding — 2026-06-02 — EAA-7 engine page chronicle render

**Reviewer:** jack-ryan
**Severity:** INFO
**Target:** commit `42a0a0b` / tag `drax/v1.4-eaa-7-engine-page-chronicle-1`
**Developer:** drax
**Principles applied:** 2, 3, 6

---

## What I found

EAA-7 delivers what it promises. Commit `42a0a0b` adds three artifacts: `EngineStateChronicle.tsx`, `useKitSpaceChronicleData.ts`, and a wired update to `EngineState.tsx`. The chronicle section (§ 2) renders below the existing season pipeline (§ 1), inserting `ChronicleSection` between `EngineStatePipelineFlow` and `EngineStatePhaseDeepDive`. All six acceptance criteria are addressable from the empirical artifacts:

- **AC-1**: `EngineStateChronicle` renders `chronicle.events[]`; `ChronicleSection` handles loading/error states; the component fires on every season-selector state (season-independent fetch). PASS.
- **AC-2**: `ChronicleEventCard` renders `event_id` (bold monospace header), `event_timestamp` (formatted UTC via `formatTimestamp`), `event_scope` (dedicated card row), `kit_count` (large badge top-right), and `substrate_inputs_changed` (bulleted list row). All five required fields rendered. PASS.
- **AC-3**: `npm run build` output confirmed 0 TS errors; 1067 modules transformed. PASS.
- **AC-4**: Vercel preview READY at `https://reincarnated-loadout-madl8913m-matthew-wetmore-s-projects.vercel.app`. PASS.
- **AC-5**: this finding. PASS.
- **AC-6**: `EngineStatePipelineFlow` and all downstream sections (`EngineStatePhaseDeepDive`, `EngineStateFactionEmergence`, `EngineStateBackwardTrace`, `EngineStateObservations`) are unmodified; `ChronicleSection` is an additive insertion with its own data fetch lifecycle that does not interact with the `useEngineStateData` hook or the season selector. Backward-compat preserved. PASS.

---

## Rationale

**Principle 2 (smoke-gate before commit):** `npm run build PASS` confirmed in commit message and verified against observed output (1067 modules, 0 TS errors). Smoke-test evidence present.

**Principle 3 (cross-seam impact):** EAA-7 is consumer-only on an already-locked schema (CHRONICLE_SCHEMA.md v1.0 + `kitSpaceTypes.ts` from EAA-6). No new cross-seam contract introduced. No MIGRATION.md required. The commit message correctly notes "no new types added — reuses KitSpaceChronicle + KitSpaceChronicleEvent from EAA-6." Principle 6 round-trip-not-applicable justification: consumer reads locked schema; no new field emitted to any upstream seam.

**LOCK O compliance:** `EngineStateChronicle.tsx` adapts the `EngineStatePipelineFlow` section pattern (§ heading + description paragraph + card container). No new bespoke UI component shell introduced. `useKitSpaceChronicleData.ts` reuses the established `fetchJson` + `useState` + `useEffect` + `useCallback` pattern from `useEngineStateData.ts` and `useKitSpaceData.ts`. Pattern reuse is correct.

**Data source verified:** `public/kit-space/kit_space_chronicle.json` confirmed present with `kse_20260602_001` event. Per-kit JSON files confirmed present in `public/kit-space/kits/`.

---

## INFO items

**INFO-1** — `ChronicleSection` is mounted inside `DashboardContent`, which only renders after the season data load succeeds. If season data load fails (error state), the chronicle section is never rendered — it's gated behind the season-data success state. This is a structural quirk: the chronicle is season-independent logically, but is rendered inside the season-gated content block. The consequence is that a user who encounters a season-data load error won't see the chronicle either, even though the chronicle itself would have loaded fine.

This is not blocking for EAA-7 — the current use case (season data loads successfully) is unaffected and the EAA-7 scope is narrow. Surface for EAA-8 consideration: if the chronicle section should survive season-data errors, move `ChronicleSection` above the season-gated `DashboardContent` block or into the outer `EngineState` component that always renders.

**INFO-2** — `useKitSpaceChronicleData` does not expose a `refresh` function that connects to the parent page's existing "Refresh" button in the control bar. The existing Refresh button drives `setRefreshKey` which re-mounts `DashboardContent` with a new `key`, which does trigger re-mounting of `ChronicleSection` (and thus a new hook invocation). So refresh indirectly works via remount. Not a bug; noting it because a future explicit `refresh` wire-up may be cleaner. Deferred to EAA-8 if prioritized.

---

## Action

- [x] Drax: no blocking action required. EAA-7 PASS.
- [ ] Drax (EAA-8 candidate): consider hoisting `ChronicleSection` above the season-gated content block to preserve chronicle visibility under season-data error states (INFO-1).
- [ ] KR: route EAA-8 wave-close when ready; INFO-1 + INFO-2 queued for ratification.

---

## References

- Commit inspected: `42a0a0b` (`drax/v1.4-eaa-7-engine-page-chronicle-1`)
- `/Users/admin/Games/reincarnated-loadout/src/components/EngineState/EngineStateChronicle.tsx`
- `/Users/admin/Games/reincarnated-loadout/src/hooks/useKitSpaceChronicleData.ts`
- `/Users/admin/Games/reincarnated-loadout/src/pages/EngineState.tsx`
- `/Users/admin/Games/reincarnated-loadout/public/kit-space/kit_space_chronicle.json`
- Chronicle schema: `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`
- Type source: `reincarnated-loadout/src/data/kitSpaceTypes.ts` (EAA-6)
- Dispatch: `agentic_orchestration/dispatches/2026-06-02-eaa-6-eaa-7-drax-mvp-reframe-sequential.md` § 7
