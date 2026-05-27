# Dispatch — drax — Cycle 13 Track C (REVISED) Step 2 — Consume Normal Season + Retire Gap-Fill Tab

**Date authored:** 2026-05-27
**Authored by:** knight-rider (per Matt directive 2026-05-27 — Cycle 13 Track C REVISED)
**Status:** PENDING
**Cycle:** 13 (post-close additive scope per Matt directive)
**Track:** C REVISED Step 2 (star-lord Step 1 prerequisite COMPLETE — sentinel landed)
**Authorization:** Matt 2026-05-27 verbatim per-cycle-push authorization + Track C REVISED directive

---

## 0. Context

**Star-lord Step 1 COMPLETE** (commits engine `2b32b61` + loadout `ef7b974` + collab `fa535dd`):

- Dual-write convention chosen — `cycle-13-mechanical-season-001` lands at BOTH:
  - `reincarnated-loadout/public/seasons/cycle-13-mechanical-season-001/` (per Matt's spec; flat `classes.json` + `metadata.json` matching v2_narrow_phase_5 precedent)
  - `reincarnated-loadout/data/cycle-13-mechanical-season-001/` (hook-discoverable; `manifest.json` + `classes/<id>.json` × 16)
- 16 classes in `data/cycle-13-mechanical-season-001/classes/` (verified empirically)
- Placeholder per-skill content marked: `metadata.placeholder_skill_content: true`, `metadata.cycle_14_refresh_pending: true`, per-skill `phase5_is_placeholder: true`
- `gear_pool.json` OMITTED per existing Yomi-only convention (you may opt-in for cycle-13 if needed; gear remains in `cycle13_characters.db`)
- 53 export tests PASS engine-side; sentinel at `reincarnated-engine/src/reincarnated/export/cycle13_normal_season_export_landed.sentinel`
- MIGRATION § v1.9 (engine) + § v2.2 (loadout)

**Your task:** consume cycle-13 as a normal season on all 4 pages + retire the gap-fill tab (4cf8312) from Sample.tsx.

**The corrective architectural pass:** earlier Track B Step 2 made an assumption-architectural-choice (gap-fill tab) that turned out to be the wrong direction. Per Discipline #11, the fix is to land the correct architecture (Step 1 — normal-season integration) + retire the gap-fill cleanly (this Step 2).

---

## 1. Required reading

1. **`reincarnated-loadout/MIGRATION.md`** § v2.2 — star-lord's Step 1 consumer-contract for cycle-13 normal season
2. **`reincarnated-loadout/MIGRATION.md`** § v2.0 + § v2.1 — prior cycle13_characters.db + Sample-page consumer (the gap-fill being retired)
3. **`reincarnated-loadout/src/hooks/useSeasonData.ts`** — verify cycle-13 appears in `selectableSeasons` automatically (no code change should be needed; if hook update IS needed, that's discovery-step work)
4. **`reincarnated-loadout/data/cycle-13-mechanical-season-001/`** — the 16-class season data hook reads
5. **`reincarnated-loadout/public/seasons/cycle-13-mechanical-season-001/`** — the alternative-convention copy
6. **`reincarnated-loadout/src/pages/Sample.tsx`** — current state with the gap-fill tab toggle to retire
7. **`reincarnated-loadout/src/pages/Loadout.tsx`** — build-editor page; test cycle-13 selection here
8. **`reincarnated-loadout/src/pages/Analytics.tsx`** — analytics page; test cycle-13 selection + cohort distribution + per-character stats; optional consumption of `cycle-13-gauntlet-sim-results-2026-05-27.json` (27,360 fights / 912 encounters) if you wire it
9. **`reincarnated-loadout/src/pages/Encounters.tsx`** — encounters page; consume SC-6 endgame reference encounters + 912 empirical encounter results if accessible
10. **`reincarnated-loadout/src/components/Cycle13/`** — 4 components from gap-fill (`Cycle13SampleSection.tsx`, `Cycle13CharacterHeader.tsx`, `Cycle13SkillTree.tsx`, `Cycle13GearDisplay.tsx`) — assess retention vs cleanup (per dispatch § 2 Step 3 below)
11. **`reincarnated-loadout/src/hooks/useCycle13Data.ts`** — gap-fill hook; assess retention vs cleanup
12. **`reincarnated-loadout/scripts/export_cycle13_json.py`** — SQLite→JSON bridge from gap-fill; assess retention vs cleanup
13. **`reincarnated-loadout/public/data/cycle13/`** — 33 static JSON files from gap-fill; assess retention vs cleanup

---

## 2. Scope — sequential steps

### Step 1 — Verify hook discovery

Run loadout dev-server OR a quick test. Confirm:

- `cycle-13-mechanical-season-001` appears in `useSeasonData()` `selectableSeasons` list **automatically** (no code change required)
- Season metadata reads correctly (16 classes; `placeholder_skill_content: true`)

If the hook does NOT discover cycle-13 automatically:
- Investigate why (could be glob-pattern mismatch, file naming, or a different consumer expectation)
- Update hook minimally to discover (single-file change)
- Document the change in `loadout/MIGRATION.md` cross-referencing star-lord § v2.2

### Step 2 — Test 16-character season selection on 4 pages

Select cycle-13 on each page + verify expected behavior:

**Loadout page (`Loadout.tsx`):**
- Build editor accepts cycle-13 season
- 16 classes selectable
- Per-class skill tree renders (with placeholder skill names visible)
- Per-class gear display works
- Placeholder indicator visible (Step 4)

**Sample page (`Sample.tsx`):**
- Cycle-13 appears in the default season picker view (NOT the gap-fill tab being retired)
- Classes render correctly
- Placeholder indicator visible

**Analytics page (`Analytics.tsx`):**
- Cycle-13 cohort distribution renders (4 cohorts × 3 scopes per Block A4)
- Per-character stats from class metadata
- **Optional empirical-gauntlet-data consumption:** if you can wire the 27,360-fight gauntlet results JSON for cycle-13, render KPM per cohort × scope from empirical data. Source: `reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (canonical path post W2 fix). Requires star-lord ingest pipeline OR client-side fetch from a copied path; deferrable if heavy. Flag if deferred for future star-lord follow-on.

**Encounters page (`Encounters.tsx`):**
- Cycle-13 selectable
- Optional: consume SC-6 endgame reference encounters (18 per char × 4 cohorts = 72 unique encounter signatures, instantiated 912 times in the gauntlet) if accessible
- Optional: render 912 encounter outcomes per cohort × scope from gauntlet sim results

### Step 3 — Retire the gap-fill tab from Sample.tsx (commit 4cf8312)

**Remove:**
- `Cycle13SampleSection` import + render from `Sample.tsx`
- `sampleView` state variable (the tab toggle state)
- View toggle UI (the tabs between "Season Archive" and "Cycle 13 Characters")

**Keep (for now):**
- `useCycle13Data` hook (may be reusable for Analytics/Encounters pages with empirical data; clean up in a later pass if not)
- `Cycle13*` components (same — may be reusable; defer cleanup)
- `scripts/export_cycle13_json.py` (defer)
- `public/data/cycle13/` (defer)

**Rationale for keeping:** the gap-fill infrastructure has value for empirical-data rendering at Analytics/Encounters pages until/unless a cleaner pattern emerges. Deferred-cleanup pass post-Cycle-14 (or whenever empirical-data rendering pattern is settled).

If you opt to retire some/all of the Keep items during this dispatch, document the retention/retirement decision in loadout MIGRATION § v2.3.

### Step 4 — Display placeholder-skill-content indicator on cycle-13 season

UX requirement: player must understand cycle-13 is a temporary mechanically-validated state pending Phase 5 cohesion coalescence in Cycle 14.

Indicator placement (drax design call):
- Season-picker level: small badge/label "Skills pending Phase 5 cohesion coalescence — Cycle 14 refresh"
- OR per-skill-tooltip level: when hovering a placeholder skill, surface the `phase5_is_placeholder: true` flag with explanation
- OR both

Detection mechanism: `skills[0].phase5_is_placeholder === true` per star-lord completion record (all 16 classes qualify; flag is present on every synthesized placeholder skill).

### Step 5 — Build clean + smoke test

- `tsc -b` → 0 TS errors
- `pnpm dev` (or equivalent) → app loads
- Smoke test: at least 3 cycle-13 characters across all 4 pages (Loadout / Sample / Analytics / Encounters); coverage across attribute branches (e.g., one STR, one INT, one WIS)

### Step 6 — Tests

Add vitest tests per existing pattern (`src/__tests__/`):
- cycle-13 season appears in `selectableSeasons`
- cycle-13 class data loads correctly (16 classes; per-class skills array; placeholder flag detected)
- Gap-fill tab no longer renders on Sample.tsx (regression test)
- Placeholder indicator renders for cycle-13

### Step 7 — MIGRATION + commit + push

- `reincarnated-loadout/MIGRATION.md` new § v2.3 — drax consumer landing for cycle-13 normal season + gap-fill tab retirement + retention decisions for gap-fill components/hook
- Commit + push per Matt per-cycle-push authorization

---

## 3. Acceptance criteria

- [x] `cycle-13-mechanical-season-001` visible in normal season picker on all 4 pages
- [x] 16 characters render with chain + T4 + gear content per page
- [x] Placeholder skill names display + "Cycle 14 refresh pending" indicator visible
- [x] Gap-fill tab retired (no longer accessible on Sample.tsx)
- [x] `Cycle13SampleSection` + `sampleView` state + view toggle UI removed from `Sample.tsx`
- [x] Build clean (0 TS errors); dev-server loads; smoke test 3 chars × 4 pages
- [x] Vitest tests added per § 2 Step 6
- [x] Loadout MIGRATION § v2.3 documents drax consumer landing + retention decisions
- [x] No regressions in existing loadout test suite
- [x] WARN-pattern preservation chain maintained

---

## 4. Out-of-scope (explicit)

- **Do NOT** modify `useSeasonData.ts` beyond minimal discovery-fix if needed (consult dispatch § 2 Step 1)
- **Do NOT** modify the 16 cycle-13 source JSONs in `reincarnated-engine/output/cycle-13-mechanical-season-001/` (immutable substrate; star-lord transform layer owns the loadout-app copy)
- **Do NOT** modify the placeholder per-skill content emitted by star-lord — your job is to consume + display, not augment
- **Do NOT** delete the `cycle13_characters.db` (star-lord may still consume for analytics; assess as separate post-cycle-14 cleanup)
- **Do NOT** wire the gauntlet sim results JSON to Analytics if it requires substantial new infrastructure — flag for star-lord follow-on if deferred
- **Do NOT** deploy to Vercel production without Matt's explicit authorization (per ADR-006)
- **Do NOT** invent new placeholder UX semantics — match the `phase5_is_placeholder` flag's intent

---

## 5. Cross-seam impact

- **Star-lord-side:** prerequisite landed; nothing new required
- **Engine-side:** none
- **Loadout MIGRATION § v2.3 cross-references § v2.2** (star-lord's consumer contract) per ADR-004

If you defer the gauntlet-sim-results consumption at Analytics, flag in MIGRATION + completion record for KR to route a star-lord follow-on dispatch.

---

## 6. Discipline citations

- **#11 empirical inspection over assumption** — verify hook discovery empirically before assuming it works; verify retention/retirement of gap-fill components per actual reusability
- **#1.2 math-note code-citation** — placeholder-indicator UI placement documented in MIGRATION
- **#19 Agent-tool-not-for-waiting** — single serial test invocation; do not fire concurrent test suites
- **#21 / #22** — completion record uses workstream-relative framing

---

## 7. Completion record protocol

Append a completion record with:

- **Status:** COMPLETE
- **Hook-discovery confirmed:** yes/no (+ any minimal hook update needed)
- **Per-page verification:** which 3 cycle-13 characters smoke-tested on which pages; PASS/FAIL per page
- **Placeholder-indicator placement:** description (season-picker badge / per-skill tooltip / both)
- **Gap-fill retirement summary:** what was removed; what was kept (with rationale); whether cycle13_characters.db / useCycle13Data hook / Cycle13 components / public/data/cycle13/ retained or retired
- **Optional gauntlet-sim-data consumption:** wired or deferred (if deferred, flag for star-lord follow-on)
- **Loadout MIGRATION § v2.3 path**
- **Tests added** (count + names)
- **Build result** (TS errors / warnings count)
- **Commit SHAs**
- **WARN-pattern preservation chain status**

KR will pick up + close Cycle 13 Track C REVISED. After this completes, the cycle-13 season is fully integrated as a normal season + gap-fill tab is retired; the wind-down summary gets updated reflecting the corrective architectural pass.

---

**Authority:** knight-rider per Matt Track C REVISED directive + per-cycle-push authorization.

**Push pattern:** per Matt authorization, commit + push as work-products land.
