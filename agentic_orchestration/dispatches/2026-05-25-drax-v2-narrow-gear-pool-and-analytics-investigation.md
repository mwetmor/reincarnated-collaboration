# Dispatch — 2026-05-25 — drax — v2_narrow gear-pool consumption + analytics tab investigation

**From:** knight-rider (orchestrator)
**To:** drax (loadout app implementation seam)
**Approved by:** Matt 2026-05-25 — "gear is all from the old Yomi season" + "data ready for analytics tab? I still don't see the new season there"
**Estimated effort:** ~30-60 min combined (gear-pool fix ~15-30 min + analytics investigation ~15-30 min)
**Acceptance:** v2_narrow loadout view shows per-season gear (not Yomi); v2_narrow visible in analytics tab (or root cause documented if data shape blocks)

---

## Context (root causes — KR empirically verified)

### Issue 1: gear-pool "all from old Yomi season"

**Root cause:** `reincarnated-loadout/src/pages/Loadout.tsx` line 27 + `reincarnated-loadout/src/pages/Sample.tsx` line 16 BOTH hardcode:
```ts
import gearPoolRaw from '../../data/season_002328/gear_pool.json';
```
This is a STATIC import — used regardless of which season is selected. v2_narrow has NO gear_pool.json (rocket's deployment-shape fix didn't generate one; season_002328 is the only season with gear_pool data per star-lord MIGRATION.md v1.1).

When Matt selects v2_narrow forms, the displayed gear/secondary loot is still Yomi's gear_pool because the import is hardcoded.

### Issue 2: v2_narrow not visible in analytics tab

**Possible root causes (drax to investigate):**

KR empirical inspection of `reincarnated-loadout/src/hooks/useAnalytics.ts`:
- Function iterates all seasons from useSeasonData ✅ (v2_narrow IS included)
- `isCanonical7Season(id)` = `/^season_00201[1-5]$/.test(id)` — v2_narrow returns `false`
- `seasonLabel(id)` returns raw `id` for unknown seasons (no v2_narrow case)
- Analytics views may filter by `isCanonical7` OR by other criteria that exclude v2_narrow

KR empirical inspection of `reincarnated-loadout/src/components/analytics/SeasonSummaryCards.tsx`:
- Line 126: `const historicalCards = cards.filter((c) => !c.isCanonical7 && c.seasonId !== 'season_002328');`
- Line 128: `yomiCards` separates 002328
- v2_narrow should fall into `historicalCards` (since `isCanonical7 = false` AND `seasonId !== 'season_002328'`)

**Hypothesis:** v2_narrow IS being collected but displayed in the historical-cards section that may be off-screen, collapsed, OR Matt is looking at a specific analytics view (canonical-7 or Yomi-specific) that filters v2_narrow out.

**Alternative hypothesis:** v2_narrow's manifest.json fields don't match what useAnalytics expects (e.g., missing `dominant_element` on classes), so the season is filtered out during data-shape validation.

Drax investigates + decides root cause + appropriate fix.

---

## Required reading

**Issue 1 (gear-pool):**
- `/Users/admin/Games/reincarnated-loadout/src/pages/Loadout.tsx` lines 25-30 (the hardcoded import)
- `/Users/admin/Games/reincarnated-loadout/src/pages/Sample.tsx` lines 14-20 (same hardcoded import)
- `/Users/admin/Games/reincarnated-loadout/src/utils/synthesizeSampleLoadout.ts` (gear-pool consumer)
- `/Users/admin/Games/reincarnated-loadout/data/season_002328/gear_pool.json` (reference shape)
- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts` `GearPoolEntry` interface (line 217)

**Issue 2 (analytics):**
- `/Users/admin/Games/reincarnated-loadout/src/hooks/useAnalytics.ts` (full file — analytics aggregation logic)
- `/Users/admin/Games/reincarnated-loadout/src/components/analytics/SeasonSummaryCards.tsx` (display + filtering)
- `/Users/admin/Games/reincarnated-loadout/src/pages/Analytics.tsx` (page-level routing)
- `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/manifest.json` + `classes/class_0001.json` (v2_narrow data shape)

---

## Scope

### Item 1 — Gear-pool consumption fix (~15-30 min)

- [ ] **Decision A:** per-season dynamic gear_pool consumption (preferred long-term):
  - Refactor `useSeasonData.ts` to glob gear_pool.json per season alongside manifest.json (e.g., `../../data/*/gear_pool.json`)
  - Pass per-season gear_pool to Loadout.tsx + Sample.tsx via SeasonData
  - Remove hardcoded import; fallback to Yomi gear_pool when season lacks one OR empty array
  - Trade-off: deeper refactor; affects all gear-pool consumers
- [ ] **Decision B:** v2_narrow-specific gear-pool placeholder (preferred short-term):
  - Generate minimal gear_pool.json for v2_narrow at `data/v2_narrow/gear_pool.json` (small placeholder; can be Yomi-mirror OR empty array)
  - Keep hardcoded import but add per-season override logic
  - Trade-off: doesn't solve generally; only patches v2_narrow
- [ ] **Decision C (drax judgment):** other approach drax sees as cleaner — drax design judgment
- [ ] **Drax selects approach + documents rationale + implements**
- [ ] **Smoke-test:** select v2_narrow form in loadout; verify gear display is appropriate (whatever drax chose)

### Item 2 — Analytics tab investigation + fix (~15-30 min)

- [ ] **Probe-1:** run `npm run dev` in loadout repo, open Analytics page, check whether v2_narrow appears in any analytics card section (canonical-7 cards / Yomi cards / historical cards / archetype tables / etc.)
- [ ] **Probe-2:** inspect useAnalytics.ts output for v2_narrow specifically — does the season appear in `historicalCards`? Is its data-shape valid (manifest.anchor.name resolves? dominant_element on classes present?)
- [ ] **Probe-3:** if v2_narrow is being filtered out, identify the specific filter + decide whether:
  - (a) v2_narrow data should be amended to pass the filter (e.g., add missing dominant_element values on classes)
  - (b) filter logic should be amended to include v2_narrow as a new category (e.g., "engine v2 milestone forms")
  - (c) new analytics view added specifically for v2_narrow (separate card section like Yomi gets)
  - (d) data is correctly excluded for now; document why + flag for Cycle 13 scope
- [ ] **Drax selects approach + documents rationale + implements**
- [ ] **Smoke-test:** Analytics page renders v2_narrow OR documents why it cannot at v1 narrow

### Operational scope (all items)

- [ ] **`seasonLabel('v2_narrow')` mapping:** add to `useAnalytics.ts` line 127 area — returns "Narrow Milestone v1.0" OR similar human-readable label (drax judgment)
- [ ] **`ClassIcon.tsx` mapping:** add v2_narrow → season-icon (line 25 area) — drax judgment per existing icon convention
- [ ] **Smoke-test on loadout side:** `cd /Users/admin/Games/reincarnated-loadout && npm run build` — clean
- [ ] **No regression on existing 11 real seasons OR sample-season**
- [ ] **Commit + push** to loadout repo (Vercel auto-deploys to production per established pattern this session)
- [ ] **AGENT_STATE.md updated** at session end

## Acceptance criteria

- [ ] v2_narrow loadout view shows appropriate gear (not Yomi's hardcoded pool) — drax selects approach A/B/C + documents rationale
- [ ] Analytics tab shows v2_narrow (in appropriate card section / table / view) OR drax documents root cause + Cycle 13 escalation
- [ ] seasonLabel + ClassIcon mappings added for v2_narrow
- [ ] Build clean (0 TS errors)
- [ ] No regression on existing 11 real seasons
- [ ] Loadout commit pushed → Vercel auto-deploy fires

## Out of scope (explicit non-goals)

- **NO engine code amendments** — drax UI/data-consumption seam only
- **NO new schema changes** — consume existing types as-is; if v2_narrow data shape requires amendment to pass analytics filters, escalate to KR for routing to rocket (NOT inline drax-side data amendment)
- **NO Vercel CLI production-promote** — main-branch push auto-promotes (established this session)
- **NO restructure of other 11 real seasons**
- **NO Yomi gear_pool deletion or replacement** — Yomi remains canonical gear-pool reference; only v2_narrow's per-season behavior changes
- **NO drax design-mode toggle / badges work** — those are already shipped per `9acff0d`

## Open questions for drax to resolve

- **Item 1 approach:** A (per-season dynamic glob) vs B (v2_narrow placeholder) vs C (other) — drax judgment
- **Item 2 root cause + fix path** — drax investigates then judges
- **seasonLabel + ClassIcon values** — drax design judgment
- **Whether to add a "v2 milestone" analytics section** (like Yomi has its own section) — drax judgment

## Cross-seam coordination

- **Coordinate with rocket dispatch** at `2026-05-25-rocket-v2-narrow-weapon-category-correction.md` (firing in parallel) — rocket fixes main_weapon.category data; drax fixes gear-pool + analytics consumption. No contention; different files.
- **If analytics fix requires engine-side data shape changes,** STOP and escalate to KR — do not amend v2_narrow data files inline (that's rocket's transform-side ownership)

## References

- `agentic_orchestration/dispatches/2026-05-25-rocket-v2-narrow-loadout-deployment-shape-fix.md` (deployment-shape-fix that produced current v2_narrow structure)
- `agentic_orchestration/dispatches/2026-05-25-drax-engine-generation-run-loadout-amendments.md` (drax's prior v2_narrow-adjacent work — design-mode + badges)
- Matt 2026-05-25 verbatim: "the weapons and gear are all from the old Yomi season for some reason. Can that be fixed? I really need to see this new season's main and secondary weapons. Is there also data ready for the analytics tab btw? I still don't see the new season there."

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 gear-pool + analytics visibility need + scope-doc autonomy + skip-confirmation re-auth
**Status:** FIRE — parallel-track with rocket weapon-category correction; no contention

---

## Completion record

**Completed by:** drax
**Date:** 2026-05-25
**Commit:** `352436c` — drax(v2_narrow): per-season gear-pool consumption + analytics visibility
**Push:** `main` pushed to origin → Vercel auto-deploy fires

### Item 1 — Gear-pool fix

**Approach chosen:** A (per-season dynamic glob)

**Root cause confirmed:** `Loadout.tsx` + `Sample.tsx` both hardcoded `import gearPoolRaw from '../../data/season_002328/gear_pool.json'` as a static import. v2_narrow has no `gear_pool.json`, so all gear displays always showed Yomi gear regardless of selected season.

**Fix:**
- `src/hooks/useSeasonData.ts`: added `gearPoolModules` glob (`../../data/*/gear_pool.json`, eager); `resolveGearPool(folderKey)` returns per-season pool or empty array when absent
- `src/data/types.ts`: `SeasonData` extended with `gearPool: GearPoolEntry[]`
- `src/pages/Loadout.tsx`: hardcoded Yomi import removed; `const gearPool = season?.gearPool ?? [];`
- `src/pages/Sample.tsx`: same removal; banner text updated to not reference Yomi explicitly
- `src/components/GearGrid/GearGrid.tsx`: hardcoded "Yomi Season" subtitle removed from Gear Slots header
- `TODO(drax)` annotations added in useSeasonData + both pages for cleanup when engine ships gear pools

**Rationale for A over B:** Approach B only patches v2_narrow. Approach A fixes the root cause for all future seasons. Empty-array fallback for poolless seasons is the correct behavior (GearGrid renders empty slots — accurate, not misleading). No placeholder data needed.

**v2_narrow behavior:** `season.gearPool = []` → GearGrid shows empty gear slots. Correct — v2_narrow is a narrow milestone with no gear pool generated.

**Yomi behavior:** Unchanged. Yomi's `gear_pool.json` still resolves via the glob; `gearPool` populated as before.

### Item 2 — Analytics investigation + fix

**Root cause confirmed:** v2_narrow WAS being collected by `useSeasonData` and processed by `useAnalytics`. Data shape fully valid: `dominant_element: "physical"` on all classes, `anchor.name: "Moctezuma"`, `validation_passed: true`, `convergence_failures: 0`. NOT a data-shape problem.

v2_narrow fell into `historicalCards` (not `isCanonical7`, not `season_002328`) but the section header was "Historical (canonical-4)" — misleading — and `seasonLabel()` returned raw `"v2_narrow"` (no mapping).

**Fix chosen:** (b) filter logic amendment + (c) dedicated section (combined):
- `src/hooks/useAnalytics.ts`: `seasonLabel('v2_narrow')` => `'Narrow v1.0'`
- `src/components/analytics/SeasonSummaryCards.tsx`: `isEngineV2Season(id)` predicate (`id === 'v2_narrow'`); excluded from historicalCards; new amber-styled "Engine v2 — Narrow Milestone" section with annotation "pre-elemental · physical-only · new engine architecture"
- `src/components/ui/ClassIcon.tsx`: `'v2_narrow': 'season-v2-narrow'` entry (onError hides gracefully if SVG absent)

**Why NOT Cycle 13 deferral (option d):** Data is fully valid and already processed. Issue was presentation only. 5-line fix, no data amendments needed.

### Smoke results

- `npm run build`: 813 modules, 0 TypeScript errors — PASS (two runs: initial + GearGrid edit)
- Yomi gear pool: resolves via glob unchanged — PASS
- v2_narrow loadout: gearPool = [] → GearGrid empty slots — PASS (correct behavior)
- Analytics page: v2_narrow in "Engine v2 — Narrow Milestone" section, label "Narrow v1.0", anchor "Moctezuma", validation PASS — PASS
- 11 historical seasons: analyticsSeasons count +1 (v2_narrow now visible) — no regression
- No TypeScript errors, no new console errors expected

### Production

Main branch pushed → Vercel auto-deploy to `https://reincarnated-loadout.vercel.app` (established session pattern; no `vercel --prod` invoked by drax).
