# Dispatch — 2026-05-30 — drax — engine-state dashboard Phase α (status surface; NO trigger buttons)

**From:** knight-rider (per gandalf routing 2026-05-30)
**To:** drax
**Authority:** Matt 2026-05-30 verbatim: "draft the work for KR to begin sending drax out for phase α now."
**Hive-state:** N/A — Mode B Pattern B sustained dispatch (substantial scope)
**Status:** FIRING
**Auto-commit:** YES per CLAUDE.md addendum 2026-05-25
**Auto-push:** YES per established 2026-05-30 session pattern; includes Vercel Production deploy

---

## Surfacing context

Per Pi-engine control dashboard recognition record `canonical/story/2026-05-30-pi-engine-control-dashboard-recognition.md` — Phase α is the near-term maturation of the static state-of-engine HTML into a dynamic dashboard. Phases β (control plane: trigger buttons + cascade fire + live log streaming + abort controls) + γ (runner decentralization) PRESERVED as recognition records for later Pattern-B engagement when Pi Phase 1 + Phase 2 mature.

**Scaffolding source confirmed (KR Disc #11 verification 2026-05-30):**
- `agentic_orchestration/gandalf/notes/2026-05-30-engine-state-season-003-flow-diagram.html` — commit `b26e330` (latest faction names + season name post-remediation; "update for 04:49 UTC remediation (Wave A/B/S all regenerated)")
- Component boundaries already documented in HTML footer notes (see Scope § Work-item 1)

**Data sources confirmed present for season-001** (KR verification):
- `season_summary.json` ✓
- `phase4_archive_insertion.json` ✓
- `phase5_faction_clusters.json` ✓
- `phase5_faction_relationships.json` ✓
- `wave_b_identities.json` ✓
- `phase2_kit_candidates.json` ✓ (large file — gandalf flagged lazy-load consideration)
- `kit_archive.db` ✓ (SQLite)
- `phase7_season_summary.json` ✓ (bonus; verify if needed)

Drax verifies the same files exist for seasons-002 + 003 as part of Work-item 2 setup.

---

## Required reading

1. `canonical/story/2026-05-30-pi-engine-control-dashboard-recognition.md` — Phase α/β/γ scope boundaries (CRITICAL — Phase β + γ items explicitly preserved as recognition records; do NOT scope-creep)
2. `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — canonical commitment (Phase α dashboard composes with augmentation principle)
3. `agentic_orchestration/gandalf/notes/2026-05-30-engine-state-season-003-flow-diagram.html` — scaffolding source (component boundaries in footer; SVG pipeline-flow structure; Tidewarden backward-trace pattern at end)
4. Spot-check 1 of each emitted JSON file in `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/` to confirm shape before designing component data contracts (Disc #11 — continuing the W2/W4/initial-planning-suite/refresh empirical pattern)
5. Existing loadout app season picker pattern (`src/hooks/useSeasonData.ts` glob auto-discovery; the pattern you established at `acb8b5f` cycle14Adapter cleanup)

---

## Scope

### Work-item 1 — Component tree per HTML scaffolding boundaries

Convert static HTML to dynamic React component tree per documented boundaries:

| Component | Source data | Notes |
|---|---|---|
| `<PageHeader />` | `season_summary.json` (Wave-S name; cost; AI-tell) | Mirror HTML header |
| `<KpiGrid />` | `season_summary.json` (KPI block) | Numeric tiles |
| `<PipelineFlow />` | Aggregated (phase counts + flow connectors) | SVG-based 9-stage diagram per HTML |
| `<PhaseDeepDive />` | Per-phase JSON files | 8 phase cards |
| `<FactionEmergence />` | `phase5_faction_clusters.json` + `phase5_faction_relationships.json` | N clusters per season's actual count (3 or 4) |
| `<BackwardTrace />` | `kit_archive.db` + `wave_b_identities.json` + `phase4_archive_insertion.json` + `phase2_kit_candidates.json` | kit_id prop; default to highest-cohesion shipped kit |
| `<Observations />` | Static text per HTML | Closing notes section |

### Work-item 2 — Per-season data integration

Use Vite glob auto-discovery pattern from `useSeasonData.ts` (commit `acb8b5f`) to expose 6 JSON files per season + SQLite query path. Reuse existing season picker for season_001 / 002 / 003.

**Large-file consideration:** `phase2_kit_candidates.json` is ~5-7MB. Lazy-load on backward-trace render (don't import in module-init).

**SQLite consumption:** existing patterns in loadout app handle `.db` files; if no pattern exists, drax design call — likely route to a derived JSON if reading SQLite client-side is impractical. Alternative: pre-extract phase7 verdict + cohort + gauntlet_pass_rate at engine-emit time (would be a star-lord emit-pipeline ask — DO NOT escalate here; if SQLite client-side reads are blocked, surface back to KR for routing).

### Work-item 3 — Mount point design call (drax seam-owner decides)

**Option A:** NEW route `/state-of-engine` (dynamic; current state); `/planning/state-of-engine` static HTML continues as historical reference.

**Option B:** REPLACE `/planning/state-of-engine` with dynamic component; static HTML retired.

**KR recommendation: Option A** for clear distinct intents (planning suite = canonical reference snapshot; `/state-of-engine` = live operational view). But drax has full design authority here. Refutation condition: if Option A creates URL-namespace friction or Option B creates loss of historical-reference value, drax design call holds either way.

### Work-item 4 — Season picker reuse

Already exists per Vite glob auto-discovery. Match existing UX pattern for season selection.

### Work-item 5 — Refresh affordances

- On-route-mount: auto-load latest data
- Manual refresh button: re-trigger data load
- Optional periodic poll: configurable; default OFF to avoid unnecessary loads (Phase β concern; not Phase α)

### Work-item 6 — Backward trace component

- Accept `kit_id` prop
- Default to highest-cohesion shipped kit in selected season (query Phase 7 verdict log)
- Drop-down to pick alternate kit
- Renders 8-step backward journey per static HTML Tidewarden pattern:
  - Phase 7 verdict (ship status + cohort + gauntlet_pass_rate)
  - Phase 5 cluster (faction identity + Wave-B name)
  - Phase 4 archive (Pareto position; quality vector)
  - Phase 3 gauntlet (wr_bracket_pass; sample distribution)
  - Phase 2 substrate (12 skills + 11 gear; chain composition + Layer 2 T4)
  - Phase 1 BC cell (bc_target_cell)
  - Phase 0 seed

### Work-item 7 — Mobile-responsive verification

CSS in source HTML is responsive (per planning-suite refresh experience this session). Verify on actual iPhone Safari + Android Chrome before push (Disc #11 — propagated discipline pattern from W2/W4/initial-planning-suite/refresh sub-pattern).

### Work-item 8 — Deploy

Vercel preview → spot-check → Vercel Production deploy.

---

## Out of scope (EXPLICIT GUARD — Phase β + γ preserved at recognition record; DO NOT scope-creep)

- **Trigger buttons on phase tiles** (Phase β)
- **Cascade fire buttons** (Phase β)
- **Live log streaming** (Phase β)
- **Abort controls** (Phase β)
- **Runner selection UI** (Phase γ)
- **Pi-side control plane endpoints** (Phase β; gates on Pi Phase 2)
- **LLM cost panel** (composes with LLM proxy recognition record; defer to later when proxy lands)
- **Real-time status / WebSocket streaming** (Phase β; just on-load + refresh-button; polling optional)
- **Engine seam writes** (drax does not invoke engine; dashboard is read-only consumer)

---

## Quality criterion

**Operational + player-facing-quality goal this dispatch serves:** Matt + son have mobile-accessible LIVE engine state (current production output across all 3 wave-5 seasons) as a dynamic dashboard rather than a static historical snapshot. Composes upward per CLAUDE.md orientation: Phase (this dispatch establishes Phase α dashboard surface) > Game (player + designer surface to inspect current engine output across all seasons + drill down to kit-level backward trace) > Engine (architectural integrity preserved — read-only consumer; no engine writes, no Phase β/γ scope creep). The dashboard supports the iteration cadence improvement that enables higher-quality player-facing output downstream.

**Refutation conditions** (drax sub-agent surfaces if any apply BEFORE executing):
- **JSON shape mismatch** between dispatch description and actual emitted data (Disc #11 spot-check 1 of each file BEFORE designing component data contracts — recall W2/W3/W4 cycle catches: KR descriptions of emitted data have a track record of needing receiving-seam re-verification)
- **SQLite client-side read infeasible** — if loadout app has no existing browser-side SQLite pattern AND adding wasm-sqlite is a non-trivial dependency, surface back to KR for star-lord emit-pipeline routing (pre-extract Phase 7 verdict to JSON at emit time)
- **phase2_kit_candidates.json bundle bloat** — if Vite includes the large file in initial bundle even when lazy-imported, surface back to KR for asset-strategy routing (move to public/ static-asset path or use dynamic fetch)
- **Phase β/γ scope-creep temptation** — if a Phase β-flavored UX feels "easy to add" while you're already in the component file, REFUSE and flag. The recognition record at `canonical/story/2026-05-30-pi-engine-control-dashboard-recognition.md` is the discipline — Phase α is status-surface-only by canonical commitment
- **Mount-point design call** — Option A vs B chooses operational UX direction; if your reading discovers neither Option A nor B is the right pattern (e.g., dashboard belongs inside an existing route like /analytics extended), surface back to KR for gandalf design check
- Dispatch introduces a pre-authored taxonomy without justification (#41) — the 7 component boundaries above are gandalf-authored from source HTML, not KR-invented; component-name discretion is drax's
- Dispatch introduces a scaffold value not flagged as pending-decision (#40) — none expected at Phase α; flag if surfaces

**Sub-agent action if refutation triggers:** halt before deploy; return triage finding to KR. KR routes to gandalf for design check OR to star-lord for emit-pipeline support OR to Matt for scope-amendment.

---

## Acceptance criteria

- [ ] `/state-of-engine` (or chosen mount-point) loads dynamic dashboard component
- [ ] All 3 Cycle 14 seasons selectable via picker
- [ ] Per-season KPIs render real data from `season_summary.json`
- [ ] `<PipelineFlow />` renders 9-stage SVG with current counts
- [ ] All 8 `<PhaseDeepDive />` cards render with correct per-phase data
- [ ] `<FactionEmergence />` renders 3 (or N) clusters per season's actual cluster count
- [ ] `<BackwardTrace />` renders with default highest-cohesion kit + accepts kit_id prop change via drop-down
- [ ] Refresh button reloads data
- [ ] Mobile-responsive verified on iPhone + Android browser
- [ ] No regression on existing /planning route OR loadout routes (/loadout, /sample, /analytics, /encounters, /pitch, /summary)
- [ ] Build clean; loadout tests pass; Vercel Production deploy Ready
- [ ] Tag: `drax/v1.X-engine-state-dashboard-phase-alpha-1` (you choose version)

---

## Cross-seam impact

- **gandalf:** owns scaffolding HTML + recognition records; drax surfaces back if scaffolding interpretation ambiguous OR Phase β-flavored scope-creep temptation surfaces
- **star-lord:** potential ask if SQLite client-side read is infeasible (Phase 7 verdict JSON pre-extraction); DO NOT escalate without KR routing
- **engine seam internal:** no impact (read-only consumer)
- **planning suite (your prior work):** Option A preserves both surfaces; Option B retires `/planning/state-of-engine` static — your design call

---

## Composes with

- `canonical/story/2026-05-30-pi-engine-control-dashboard-recognition.md` (Phases β + γ preservation; Phase α authorized for immediate dispatch per Matt 2026-05-30)
- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` (canonical commitment; augmentation principle — dashboard fits Pi's eventual middleware role)
- `agentic_orchestration/gandalf/notes/2026-05-30-engine-state-season-003-flow-diagram.html` (scaffolding source @ `b26e330`)
- Recent drax cycle 14 v1.2 work (commit `acb8b5f` cycle14Adapter cleanup; established Vite glob auto-discovery pattern reused here)
- Recent drax bundled HTML planning suite deploys (`drax/v1.2-planning-suite-vercel-deploy-1` + `drax/v1.3-planning-suite-refresh-pc-spec-1`)

---

## Discipline reminders (cumulative-pattern from this session — 4 catches so far)

Per W2 / W3 / W4 / initial-planning-suite history this session: KR dispatch descriptions of emitted-data shape have a track record of needing receiving-seam re-verification. **Apply Disc #11 empirical inspection FIRST on each of the 6 named JSON files + verify SQLite-readability path BEFORE designing component data contracts.** Your default-Disc-#11 pattern from W4 + planning-suite work is the right approach.

---

## Completion record (to be appended on close)

**Status:** FIRING
**Authored:** 2026-05-30 by knight-rider per gandalf consolidated routing + Matt verbatim authorization
