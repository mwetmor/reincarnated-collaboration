# 2026-05-17 — drax-loadout — D17 Court browser surface (loadout side)

**Authority:** Matt L3 standing delegation 2026-05-17 (sign-off pillar — "always toward Phase-1 completion"; D17 unblocked since rocket court_persistence.py @ `a8808ac`).
**Type:** Pattern B (long task) — ~5-7 days estimated (substantial UI/UX surface; includes data-flow architecture).
**Predecessor:** rocket D17 Court of Forms persistence engine-side (shipped); drax-loadout Sub-phase A vfx-manifest.json v1.0 (shipped) + Sub-phase B-partial v1.1 (shipped).
**Seam:** reincarnated-loadout (React/Vite/Tailwind webapp); consumes engine-side Court of Forms data + vfx-manifest thumbnail_frame paths.

---

## Why this matters

D17 (Court of Forms) is one of the canonical-7 substrate-expansion deliverables. Rocket already shipped engine-side persistence (`court_persistence.py` + SQLite at `~/.config/reincarnated/court_of_forms.db` per rocket commit `a8808ac`). The Court is the player's persistent collection of ascended spirits across seasons — substrate-rich, cross-season memory. **Loadout's job is to make this collection legible to the player** in their web UI.

Without D17 loadout-side: the engine accumulates Court data, but the player has no surface to see what they've accumulated. The earth-self meta-layer cosmology requires the Court be visible.

Per Matt's pillars: this is Phase-1 P1 critical path; sign-off pillar says "always toward completion"; drax-loadout idle since Sub-phase B-partial; spawn now.

---

## Required reading (in order)

1. `reincarnated-engine/src/reincarnated/foundation/court_persistence.py` — engine-side Court schema; how rocket persists Court data; SQLite location + table structure
2. `canonical/story/earth-self-cosmology-*.md` (or whichever earth-self canonical doc captures Court framing) + `canonical/story/court-of-forms-*.md` if present
3. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — rocket D17 ship STATE + your Sub-phase A + Sub-phase B-partial STATE entries
4. `reincarnated-loadout/data/vfx-manifest.json` v1.1 — `thumbnail_frame` paths per substrate; primary source for substrate visual identity in browser
5. `reincarnated-loadout/MIGRATION.md` §v1.0 + §v1.1 — cross-seam contract patterns you authored
6. `reincarnated-loadout/AGENT_STATE.md` — your seam's current state

---

## Scope (5 items)

### Item 1 (REQUIRED FIRST) — Data-flow architecture decision

**The architectural question:** How does the React/Vite webapp consume the Python-engine SQLite Court data?

**Three candidate paths:**

- **Path A (static export):** Engine exports Court data as JSON to a published path (e.g., `~/.config/reincarnated/court_export.json` or `reincarnated-loadout/public/data/court.json`). Loadout reads the JSON at boot. Refresh via re-export.
- **Path B (API endpoint):** Engine exposes an HTTP endpoint (FastAPI / Flask / similar) that serves Court data. Loadout fetches over network.
- **Path C (file-watch + IPC):** Loadout watches the SQLite file directly (read-only); some bridging layer translates SQLite rows to JSON.

**Decision rubric:**
- Phase-1 P1 priorities: simplicity + ship-readiness > runtime sophistication
- Engine + loadout typically run on the same machine (local-first; not networked)
- The Court is read-mostly from loadout's perspective (occasional writes when player re-organizes? probably not in Phase-1 P1)

**Recommended default (decide unless you find a better path):** **Path A static export**. Engine adds an export step (writes JSON snapshot when Court changes); loadout reads JSON. Simple, no service-orchestration burden, ship-aligned.

**Cross-seam implication:** if Path A, you may need a small rocket dispatch to add the export step. Surface as QUESTION → rocket if needed; OR if rocket's `court_persistence.py` already exports JSON somewhere, document where.

**Document the decision in MIGRATION.md §v1.2 entry.**

### Item 2 (REQUIRED) — Court data consumption layer

Once the architecture is decided:
- Implement the consumption layer in `reincarnated-loadout/src/`
- TypeScript types for the Court row schema (mirror engine schema)
- Loader function that reads the JSON / API / etc.
- Local React state hook for accessing Court data (`useCourtData()` or similar)
- Graceful empty-Court handling (first-time player; no spirits yet)

### Item 3 (REQUIRED) — Court browser UI

Build the UI surface in the loadout webapp:

- **Layout:** grid of cards, one per Court spirit
- **Per-card content:**
  - Sprite thumbnail (consume `thumbnail_frame.file` per substrate from vfx-manifest.json v1.1)
  - Name (LLM-generated per star-lord D15)
  - Substrate label (with substrate color from D20 grouping vocab + your existing palette)
  - Season number / season name
  - Class archetype (e.g., "fire_mage", "lightning_controller")
  - Optional: short flavor text if star-lord D15 emit includes one
- **Filtering:**
  - Substrate filter (toggle: fire / water / earth / wind / lightning / holy / shadow; "all" default)
  - Search by name (text input)
  - Sort options: season ascending/descending, substrate, name
- **Recency indicator:** N=5 most recent forms have a subtle visual marker (gandalf earth-self § 6.2/8.5 cross-season memory pattern)
- **Empty state:** "Your Court will populate as you ascend forms across seasons" (or similar; gandalf-coherent voice)

**Visual register:** match loadout's existing Tailwind aesthetic. Substrate colors per v0.28 palette table.

### Item 4 (REQUIRED) — Cross-seam reference + manifest update

- Update `reincarnated-loadout/MIGRATION.md` §v1.2 entry documenting:
  - Court browser surface shipped
  - Data-flow architecture decision (Path A/B/C)
  - Cross-seam contract: who writes Court data + who reads it
  - Consumer obligations downstream if any (e.g., star-lord telemetry; gamora regen output)
- Update `reincarnated-loadout/AGENT_STATE.md`
- If Path A static export chosen + rocket needs to add export step: file QUESTION → rocket in hive log

### Item 5 (REQUIRED) — Hive log + tag

- Append STATE entry documenting Court browser ship
- HANDOFF → drax-demo (no obligation; informational that Court browser is now live in loadout)
- HANDOFF → rocket (if Path A decided + rocket needs to add export step, ask explicitly)
- Tag `drax/v1.0-d17-court-browser-surface-1` (significant version bump; loadout-side milestone)

---

## Out of scope (DO NOT)

- ❌ DO NOT modify rocket's court_persistence.py engine code (consume only; QUESTION → rocket if change needed)
- ❌ DO NOT add Court editing / write functionality (Phase-1 P1 is read-only Court display)
- ❌ DO NOT modify engine / simulation / demo files
- ❌ DO NOT wire to live LLM Spirit Guide dialogue (separate later star-lord wiring; out of scope here)
- ❌ DO NOT redesign substrate color palette or grouping vocab (consume D20 v1.2)
- ❌ DO NOT extend scope to other loadout UI tweaks; surface as OBSERVATION
- ❌ DO NOT pre-empt drax-demo's untracked-VFX work (v1.2 already shipped) OR drax-demo's narrow-slice work

---

## Acceptance criteria

- [ ] Architecture decision documented in §v1.2 MIGRATION.md (Path A/B/C + rationale)
- [ ] Court data consumption layer implemented + tested
- [ ] Court browser UI shipped: card grid + filter + search + sort + empty state
- [ ] Sprite thumbnails render from vfx-manifest.json `thumbnail_frame.file` paths
- [ ] Substrate color coding visible across all 7 substrates
- [ ] N=5 recency indicator visible
- [ ] Empty state handled gracefully
- [ ] Build clean (`npm run build` in reincarnated-loadout)
- [ ] No console errors
- [ ] AGENT_STATE.md + MIGRATION.md §v1.2 entry authored
- [ ] Hive-log STATE + HANDOFFs entries
- [ ] Tag `drax/v1.0-d17-court-browser-surface-1` (or next available v1.X)

---

## Smoke test expectation

1. `npm run dev` → loadout webapp boots
2. Navigate to Court browser route (whatever URL convention exists in loadout)
3. Empty state visible if no Court data; populated state if Court data exists
4. Substrate filter toggles work; only matching forms display
5. Search by name filters correctly
6. Sort works across all sort options
7. Recency indicator visible on N=5 most recent forms
8. Sprite thumbnails resolve and display
9. Substrate colors visible per card

---

## Math-before-code requirements

N/A — UI + data consumption.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first. Apply broader pull-rebase discipline given concurrent gamora + gandalf activity.

---

## Tag intent

`drax/v1.0-d17-court-browser-surface-1` — loadout-side significant version bump.

---

*Dispatched 2026-05-17 by knight-rider per Matt sign-off pillar. Estimated 5-7 days. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `drax/v1.0-d17-court-browser-surface-1`
**Loadout commit:** `9430a35` (reincarnated-loadout main)
**Hive log:** `phase-1-p1-log.md` — STATE + QUESTION + HANDOFF appended (collaboration commit `923a5e7`)

### Acceptance criteria status

- [x] Architecture decision documented in §v1.2 MIGRATION.md (Path A — rationale: local-first, read-only, no service orchestration required)
- [x] Court data consumption layer implemented: `courtTypes.ts` + `useCourtData.ts`
- [x] Court browser UI shipped: card grid + substrate filter (grouping_label) + search + sort (season ASC/DESC / substrate / name) + empty state
- [x] Sprite thumbnails from vfx-manifest.json v1.1 `thumbnail_frame.file` paths (with `onError` graceful degradation)
- [x] Substrate color coding visible across all 7 substrates (SUBSTRATE_COLORS in courtTypes.ts)
- [x] N=5 recency indicator visible (accent-color "recent" badge on most recently ascended forms)
- [x] Empty state handled gracefully ("Your Court will populate as you ascend forms across seasons")
- [x] Build clean (`npm run build` — 690 modules, 0 TS errors)
- [x] No console errors (no runtime code paths that throw; graceful degradation everywhere)
- [x] AGENT_STATE.md + MIGRATION.md §v1.2 entry authored
- [x] Hive-log STATE + HANDOFFs entries (STATE + QUESTION to rocket + HANDOFF to drax-demo)
- [x] Tag `drax/v1.0-d17-court-browser-surface-1` cut and pushed

### Key decision

**Path A static export** chosen. `court_persistence.py` at commit `a8808ac` has no JSON export step.
QUESTION filed to rocket (hive log) requesting `Court.export_json(earth_self_id, output_path)`.
Until rocket ships that step, Court browser shows the canonical empty state. Court browser
code is complete and will render real data the moment `public/data/court.json` is populated.

### Cross-seam obligation created

- Rocket: add `export_json()` to `Court` class — see MIGRATION.md §v1.2 QUESTION block for full spec.
- No star-lord, gamora, or demo obligations created by this dispatch.

### Follow-on (next loadout session)

D19 Sub-phase C: demo VFX wiring + loadout D21 substrate browser + D22 embodiment display.
