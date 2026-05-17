# 2026-05-17 — drax-loadout — Website refresh with new seasons + seasonal analytics

**Authority:** Matt L3 2026-05-17 (~21:45 EDT). Gamora's standard-demo regen completed; demo SEASON_IDS micro-task firing in parallel. Loadout web app should also refresh to expose the new 5-season roster alongside the historical 5 seasons.
**Type:** Pattern B — ~0.5-1 day; React/Vite web app work in drax-loadout's seam.
**Predecessors:**
- Gamora regen complete @ `reincarnated-engine/output/standard-demo-regen-2026-05-17/` (5 seasons 002011-002015)
- Drax-demo SEASON_IDS pointer update in flight (different drax instance; demo-side)
- Drax-loadout D17 Court browser ship @ `drax/v1.0-d17-court-browser-surface-1`

---

## Why this matters

Loadout is the web app where players study seasonal analytics + browse the Court of Forms (D17) + explore class loadouts + see sample seasons. With the canonical-7 substrate expansion landing (5 new seasons with all 7 substrates), the loadout web app should:

1. **Expose the new seasons** to its data layer (alongside historical 001001-005)
2. **Refresh seasonal analytics** to show comparison data across all 10 seasons (or 5 new + 5 historical, however you scope)
3. **Keep historical content intact** — don't replace; add alongside

Matt's exact frame: *"add the new content and new seasonal analytics alongside the historical."*

---

## Required reading

1. `reincarnated-loadout/src/pages/Analytics.tsx` — current analytics page
2. `reincarnated-loadout/src/pages/Encounters.tsx`, `Loadout.tsx`, `Sample.tsx`, `CourtBrowser.tsx` — current page surface
3. `reincarnated-loadout/src/data/types.ts` — `seasonId` typing
4. `reincarnated-loadout/src/data/` — current data loading patterns (how loadout fetches season data)
5. `reincarnated-loadout/public/data/` — current static-data state (court.json from D17)
6. `reincarnated-engine/output/standard-demo-regen-2026-05-17/regen_summary.json` — substrate distribution + new season IDs (data to expose)
7. `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/manifest.json` (and 012/013/014/015) — per-season manifests for analytics
8. `reincarnated-demo/public/seasons/` — drax-demo will be populating with same source data via parallel SEASON_IDS micro-task

---

## Scope

### Item 1 — Expose new seasons to loadout data layer

Mirror the data pattern drax-demo uses. Likely options:
- **A. Copy season JSONs into loadout's public/data/** — symmetric with drax-demo's public/seasons/; loadout fetches from its own filesystem path
- **B. Loadout reads from drax-demo's public/seasons/ via shared static asset directory** — requires deployment coordination; not currently set up
- **C. New seasonal endpoint or static-data module** — e.g., `public/data/seasons/` with manifest.json + per-season subfolders

**Recommended: A** (matches the static-data pattern you already use for `court.json`). Copy `season_002011-002015` from engine staging to `reincarnated-loadout/public/data/seasons/` and expose via a data loader hook (similar pattern to `useCourtData`).

Strategy: **ADDITIVE** — also copy `season_001001-005` if they're not already in loadout's data (or add a manifest pointer to them); the historical seasons stay available.

### Item 2 — Seasonal analytics refresh

`Analytics.tsx` currently shows analytics — likely for one season or aggregate. Refresh to:
- **Per-season summary cards** — one per season (10 total now); display: season_id, theme, substrate count, archetype count, convergence rate, validation status (PASS/FAIL)
- **Cross-season comparison view** — substrate distribution heatmap across all 10 seasons; convergence rate trendline (S1-S5 historical vs S11-S15 new); archetype prevalence shifts
- **New-substrate highlight** — flag the 3 new substrates (lightning/holy/shadow) appearing in seasons 002011-002015 but not 001001-005 — diegetic-load-bearing for canonical-7 ship narrative
- **Visual register** — match existing loadout aesthetic (HD-2D-pixel + Tailwind UI; whatever exists today)

If `Analytics.tsx` is greenfield-low-effort, you have latitude on what charts/cards land. Surface tradeoffs in completion record.

### Item 3 — Other page updates (light touch)

- **Loadout.tsx** — season selector should include new 002011-005 IDs alongside historical
- **Encounters.tsx** — same (if it has season selector)
- **Sample.tsx** — same
- **CourtBrowser.tsx** — unchanged (player Court state is season-agnostic; D17 surface already shipped)

### Item 4 — Build + smoke

- `npm run build` clean
- Manual smoke: load all 5 pages; verify seasonal data renders; verify historical seasons still accessible; verify new seasons render with their canonical-7 substrate variety
- No regression on D17 Court browser (court.json bootstrap path)

### Item 5 — Vercel deployment note (if applicable)

If loadout deploys to Vercel automatically on push, ensure the new public/data/seasons/ payload doesn't push the bundle over Vercel size limits. If size is borderline, flag as OBSERVATION; don't unilaterally restructure deployment.

### Item 6 — Hive log + tag

- PRE-SIGNAL § 14.1.1 (drax-demo SEASON_IDS + drax-demo step-3 both in flight on different repos; loadout repo is independent — race risk is on collab repo only)
- STATE entry: 10 seasons live in loadout; analytics page refresh shipped; canonical-7 narrative now playable in browser
- Tag `drax/v1.1-loadout-website-refresh-new-seasons-and-analytics-1` (loadout seam)

---

## Out of scope (DO NOT)

- ❌ DO NOT modify drax-demo (separate drax instance is handling SEASON_IDS + step-3 VFX)
- ❌ DO NOT change court.json or D17 Court browser logic (intact)
- ❌ DO NOT pre-empt M2-M7 mobile UX work (post-VS2a)
- ❌ DO NOT add new pages beyond Analytics refresh (existing 5 pages get content updates only)
- ❌ DO NOT modify engine-side season data (consume staged output as-is)
- ❌ DO NOT promote to milestone tag (this is a content refresh; pre-D10 shim regen; not VS2a ship)

---

## Acceptance criteria

- [ ] season_002011-005 data exposed to loadout data layer
- [ ] Historical season_001001-005 preserved/accessible
- [ ] Analytics.tsx refreshed with per-season cards + cross-season comparison + canonical-7 highlight
- [ ] Loadout/Encounters/Sample pages reflect new season selector options
- [ ] D17 Court browser intact
- [ ] `npm run build` clean
- [ ] Manual smoke verified
- [ ] Tag `drax/v1.1-loadout-website-refresh-new-seasons-and-analytics-1`
- [ ] Hive-log STATE entry

---

## Smoke test

1. `npm run build` clean
2. Load loadout in browser
3. Navigate Analytics: see all 10 seasons with their data; compare convergence rates; spot new substrates highlighted
4. Navigate Loadout: pick a season_00201x class; explore loadout
5. Navigate Encounters / Sample: same selector now lists new seasons
6. Navigate Court: D17 surface intact; renders court.json (or empty-state if no export yet)

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log appends; pull-rebase before collab-repo commits
- **Parallel work:** drax-demo SEASON_IDS + drax-demo step-3 VFX both in flight (different repo) — no merge conflicts but hive log is shared
- **Vercel deploy:** if your push triggers Vercel deploy, you'll see preview-URL output; note it in completion record

---

*Dispatched 2026-05-17 by knight-rider per Matt L3. ~0.5-1 day. Append completion record when done.*
