# AGENT_STATE — Glance (drax web seam)

> Checkpoint for the Glance app (`glance/app` + `glance/parser`) — the derived-from-canon
> project-state web app. Owner: drax. This is the meta-repo's glance-seam continuity file
> (glance lives here, not in loadout/demo). Contract:
> `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`.

## Current version — v1.9 (nine pages)

Tag: `glance/v1.9-reference-trio-1`. Nine pages:
`/engine · /story · /game · /content-emission · /kits · /minigames · /coordinates · /atlas · /mechanics`.

### v1.9 — kit-design reference TRIO (§7.7) — LANDED 2026-07-11

Three pages added (`/coordinates` + `/atlas` + `/mechanics`), render-only, ZERO new parse shapes.

- **Parser:** new `REFERENCES` doc class (parallel to `PIPELINES`) — `parseReference` +
  `extractSections`. Reads `substrate-coordinates.md` (9 §), `mechanical-reality.md` (9 §),
  `projection-atlas.md` (6 §). Same §2.7 `parseFlow`; carries each `## §N` body verbatim.
- **Quiet-bar honesty:** `parseReference` feeds `parseFlow` an EMPTY queue set → every stage
  derives `quiet`. WHY: the payload tables carry first cells that match the row-ID grammar
  (`L0`..`L4`, numbered walker rows) — running `parseQueues` over them would wrongly model payload
  rows and color the bar (the "do NOT parse payload / do NOT invent coloring" violation). Empty
  queues is the faithful fix. Verified: all 24 stages across the trio render `quiet`.
- **App:** `ReferencePage` + `ReferenceFlowLead` + `ReferenceSections` + `TripleLawLinks` +
  `ReferenceTileRow`. New `SectionMd` renderer in `md.tsx` (tables → HTML tables, fences → `<pre>`,
  prose → paragraphs) — DISPLAY FIDELITY, never a semantic parse.
- **Open-question calls (documented per dispatch):**
  1. Index tile treatment → LEAN grouped "kit-design reference" tile row (`ReferenceTileRow`),
     compact link tiles, NOT full state cards (§7.7 rule 5 delegated to drax; all-quiet cards waste
     Tier-0 pixels). /atlas centered with a teal accent as the connective PROJECTION page.
  2. Nav order → seated adjacent at the END of the nav in read-as-one-instrument order
     (coordinates → atlas → mechanics), behind a subtle `sm:`-only divider marking them a distinct
     kind. `PAGE_ORDER` reflects this.
- **`/atlas` NO occupancy:** the §2 projection table renders byte-verbatim (confirmed
  `sec.body === source slice`); REALIZED ATLAS harness not built (§7.7 rule 7). Never hand-derived.
- **Type-map change:** `PAGE_TRACKER` + `PAGE_FLOW_SOURCE` loosened to `Partial<Record<PageId,…>>`
  (reference pages have no backing tracker/flow-source); consumers gate on `isReferencePage()`
  before any lookup.

## Active TODO(drax) overrides

- None in the trio. (Pre-existing: `/kits` feed-2 seam — per-kit cert auto-join awaits star-lord's
  `emission-runs-snapshot.json` export; v1 renders doc truth only. Unchanged this session.)

## Build / CI / deploy state

- Smoke: `npm run build` (parse fail-loud → tsc → vite) GREEN. `npm run preview` serves root +
  routes + `state.json` (all three references present). CI report-mode parse exit 0, MALFORMED 0.
- 12 dangling gates-on = pre-existing visible debt (proxy-P0/P1/P2, launch-scope-planning, etc.),
  NOT from the trio. 0 dangling flow-refs.
- **NOT deployed this session** — production Vercel deploy is Matt-gated (ADR-006). Deploy from
  meta-repo ROOT (`npx vercel deploy --prod --yes`); Root Directory = `glance/app`; SPA rewrite in
  `vercel.json` (unchanged — no routing config touched, so no re-smoke required beyond the local
  preview above).

## Files (this session)

- `glance/parser/parse.mjs` — `REFERENCES` class + `parseReference` + `extractSections`; empty-queue
  quiet-bar law; references hoisted into `state.json` + report banner.
- `glance/app/src/state.ts` — `ReferenceId` / `Reference` / `ReferenceSection` types; trio pages in
  `PageId`/`PAGE_ORDER`/`PAGE_LABEL`; `REFERENCE_PAGES` / `isReferencePage` / `PAGE_REFERENCE` /
  `TRIPLE_LAW` / `TRIPLE_LAW_SIBLINGS`; `PAGE_TRACKER`/`PAGE_FLOW_SOURCE` → Partial.
- `glance/app/src/md.tsx` — `SectionMd` verbatim-payload renderer.
- `glance/app/src/App.tsx` — `ReferencePage` + helpers; landing tile row; nav divider; Partial guards.
- `glance/README.md` — v1.9 section + parser read-set.
