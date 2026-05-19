# 2026-05-18 — drax-loadout — v1.18 bundle: Encounters multi-season + skill schema-version aware rendering

**Authority:** Matt L3 afternoon 2026-05-18 — "the encounters page still does not have the latest seasons added to it (the ones we're playing in demo with light/dark/lightning/etc)." Diagnostic confirms: star-lord Path A delivered the per-season `encounter_analytics_NNNNNN.json` files (002011, 002012, 002013, 002014, 002015, 002328 all exist in `reincarnated-loadout/data/`), but `useEncounterAnalytics.ts` still has a hardcoded static import of the singular `encounter_analytics.json` (001005 data). Frontend never picked up the new files.
**Type:** Pattern B; ~2-3 hours.
**Predecessor:** Star-lord Path A SHIPPED (per-season encounter JSONs exist). drax/v1.23 R2 hybrid SHIPPED. Drax is now free of demo critical path.
**Status:** 🔴 **PROMOTED — fires next on drax-loadout. Highest-priority loadout item.**
**Tag intent:** `drax/v1.18-loadout-encounters-multi-season-plus-skill-schema-1`

---

## Why this matters

Loadout is Matt's value-story artifact for showing simulation breadth. Currently:

- **Encounters page** displays only `season_001005` data (a single season's 11 classes × 22 encounter slots). The newer D10-era seasons (002011-015) and Yomi (002328 — light/dark/lightning) — the seasons Matt is actively *playing* in the demo — are invisible on the Encounters page. The data is sitting on disk; the frontend won't read it.
- **Sample + Loadout pages** render empty skill trees for the 002011-015 classes because those classes' skill JSON lacks the `tier`, `chain_id`, and `chain_position` fields that `SkillTree.tsx` indexes by. Older schema (no tier-tree structure).

This dispatch closes both gaps in one bundle. Same repo, same session — no point splitting.

---

## Required reading

1. `reincarnated-loadout/src/hooks/useEncounterAnalytics.ts` — the static-import bug
2. `reincarnated-loadout/src/hooks/useSeasonData.ts` — pattern to follow (already uses `import.meta.glob` for season-data discovery)
3. `reincarnated-loadout/data/encounter_analytics_002011.json` — shape of per-season file (`generated_at`, `season_id`, `tier1_populated`, then `classes[]` with `class_id`, `geometry_mix`, `encounters[]`)
4. `reincarnated-loadout/src/components/SkillTree/SkillTree.tsx` — indexes by `skill.tier` + `skill.chain_id` + `skill.chain_position`; renders empty grid when these are undefined
5. `reincarnated-loadout/data/season_002011/classes/class_0001.json` — confirm: 002011-015 skills have `id`, `role`, `geometry_type`, `canonical_element`, `seasonal_element`, `effects`, BUT NO `tier`, NO `chain_id`, NO `chain_position`, NO `composition_mode`. Newer schema (002328 onwards) does have these fields.
6. `reincarnated-loadout/src/pages/Sample.tsx` + `reincarnated-loadout/src/pages/Loadout.tsx` — consumers of SkillTree; check what season-selector pattern they already use

---

## Scope — two blocks

### Block 1 — Encounters multi-season support (PRIORITY: this is the explicit Matt-L3 ask)

**Refactor `useEncounterAnalytics.ts`:**

1. Replace the static import with `import.meta.glob<{ default: EncounterAnalyticsData }>('../../data/encounter_analytics_*.json', { eager: true })`
2. Add `seasonId: string` parameter to `useEncounterAnalytics()`
3. Map the glob result keyed by season ID (extract from path: `encounter_analytics_NNNNNN.json` → `season_NNNNNN`)
4. Return the per-season `EncounterAnalyticsData` for the requested seasonId, or null if missing
5. Surface a `EncounterAnalyticsNotAvailable` state for seasons without analytics files (graceful empty state on the page, not a crash)

**Refactor `Encounters.tsx`:**

1. Read current season from the same season-selector pattern used elsewhere (check Sample.tsx / Loadout.tsx for the existing approach — likely a route param, context, or shared hook from useSeasonData)
2. If no shared season selector exists yet on the Encounters page: add one. Use the same component/idiom as the rest of the app.
3. Pass `seasonId` to `useEncounterAnalytics(seasonId)`
4. Handle the "no analytics for this season" empty state gracefully
5. Update the page-header comment (currently `// Data: season_001005 (11 classes, 22 encounter slots)`) to reflect multi-season

**Smoke (Discipline #2):**
- Default to season_001005 on first load — should render exactly as before (regression check)
- Switch to season_002011 → should render its 6 classes × N encounters
- Switch to season_002328 → should render Yomi data with light/dark/lightning classes visible
- Switch to a season with no analytics file (e.g., season_001001 if no file present) → graceful empty state

**Optional cleanup:** delete `data/encounter_analytics.json` (the unsuffixed legacy file) after confirming `encounter_analytics_001005.json` works as its replacement. Or keep both; either fine.

### Block 2 — Skill schema-version aware rendering

**Problem:** `SkillTree.tsx` indexes skills via `${skill.tier}:${skill.chain_id}` + sorts by `skill.chain_position`. For 002011-015 classes whose skills lack these fields, every slot is empty.

**Approach:** Detect schema at runtime, fall back to a flat-list view when tier/chain are absent.

1. In `SkillTree.tsx`, add a schema-detection check at the top of render: if first skill in `class.skills` has `tier === undefined && chain_id === undefined`, render in **flat-list mode** (simple grid of skill cards, no tier-tree gating).
2. Flat-list mode UX: vertical list or auto-flow grid of skill cards. No "locked at tier N" gating since the schema doesn't carry tier info.
3. Preserve full tier-tree rendering for newer-schema classes (002328 + future).
4. If feasible, surface a small badge: `legacy schema` or `flat list` so designers know visually which seasons run in which mode.

**Anti-pattern to avoid:** do NOT add fabricated tier/chain fields to the 002011-015 class JSONs at runtime. That would lie about what the data is. Two genuinely different schemas need two genuinely different render paths.

**Smoke:**
- Sample page on season_001005 (newer schema) → tier tree renders as before
- Sample page on season_002011 (older schema) → flat list of skills, no empty grid
- Sample page on season_002328 (newest schema) → tier tree renders properly
- Loadout page parity check on both schemas

---

## Acceptance criteria

- [ ] Block 1: `useEncounterAnalytics(seasonId)` reads per-season JSON via `import.meta.glob`
- [ ] Block 1: Encounters.tsx has a season selector + handles missing-analytics empty state
- [ ] Block 1: smoke verified on 3 seasons (001005 / 002011 / 002328)
- [ ] Block 2: SkillTree.tsx detects flat-vs-tier-tree schema; renders flat-list mode for 002011-015
- [ ] Block 2: smoke verified on Sample + Loadout pages across 3 schema variants
- [ ] `npm run build` clean (0 TS errors)
- [ ] AGENT_STATE checkpoint authored
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Tag `drax/v1.18-loadout-encounters-multi-season-plus-skill-schema-1`

---

## Out of scope (DO NOT)

- ❌ Regenerating any per-season `encounter_analytics_NNNNNN.json` (star-lord owns that; this dispatch only consumes)
- ❌ Authoring new analytics on the engine side (separate dispatch if needed)
- ❌ Migrating 002011-015 class JSONs to the newer tier-tree schema (would require regeneration; out of scope here — the schema-version-aware rendering is the right call instead)
- ❌ Encounters page redesign / new chart types (this is data-plumbing only; visual polish later)
- ❌ Touching demo, engine, or any other repo
- ❌ Push commits or tags (ADR-006: Matt or knight-rider per amendment)

---

## Coordination

- **Predecessor:** Star-lord Path A SHIPPED (per-season encounter JSONs exist in loadout `data/`). Drax R2 hybrid SHIPPED (demo deploy unblocked, drax queue clear).
- **Triggers downstream:**
  - Encounters page becomes Matt's actual artifact for showing simulation breadth across seasons
  - Sample/Loadout pages no longer regress on D10 classes
  - MS bands + AOE bands fields are present in the new per-season JSONs (star-lord Path A Block 3); drax can optionally surface these in Encounters page if scope-permitting; otherwise defer to v1.19
- **Parallel-safe with:** rocket re-seed 002017 (different repo), galadriel Track C captures (different repo), any star-lord follow-up

---

*Dispatched 2026-05-18 evening by knight-rider per Matt L3 verbatim afternoon "the encounters page still does not have the latest seasons added to it." Star-lord Path A data verified present in loadout `data/`. ~2-3h drax. Pattern B; append completion record + smoke evidence when done.*

---

## Completion record

*(drax appends here when done)*
