# AGENT_STATE — Glance (drax web seam)

> Checkpoint for the Glance app (`glance/app` + `glance/parser`) — the derived-from-canon
> project-state web app. Owner: drax. This is the meta-repo's glance-seam continuity file
> (glance lives here, not in loadout/demo). Contract:
> `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`.

## Current version — v1.10 (nine pages; /atlas gains the RULED plane)

Tag: `glance/v1.10-atlas-plane-1`. Nine pages unchanged:
`/engine · /story · /game · /content-emission · /kits · /minigames · /coordinates · /atlas · /mechanics`.

### v1.10 — RULED V1.2 Stratified Plane View on /atlas (PHASE 1) — LANDED 2026-07-13

Surfaces the Q19-LOCKED plane (Matt ruled Q19 LOCKED 2026-07-13) as a DB-derived static
asset on the `/atlas` (PROJECTION) page. ZERO new parse shapes — a render/layout addition.

- **Asset staging (`glance/app/scripts/stage-assets.mjs`):** copies the committed
  `agentic_orchestration/gandalf/views/v1-plane/plane_view_v1_2_stratified.svg` →
  `public/atlas/plane_view_v1_2_stratified.svg` on every build, and emits
  `public/atlas/plane-provenance.json` with a GIT-DERIVED `source_commit` (never hand-typed).
  Single source of truth stays gandalf's committed render; an upstream re-render flows
  through on the next push. KEPT SEPARATE from the parser — the parser's charter is
  `canonical/**` truth-model only; asset provisioning is not truth-path.
- **Build wiring:** `build` = `parse && stage-assets && tsc && vite build`;
  `build:preview` mirrors it. New `stage-assets` npm script. `dev` NOT wired (run
  `npm run stage-assets` once before `npm run dev` if the plane is needed in dev).
- **App (`src/App.tsx`):** new `AtlasPlaneView` component, gated on
  `reference.id === 'atlas'` (the connective PROJECTION page only). Renders the vector
  SVG (`<img>`, `w-full min-w-[640px]` inside `overflow-x-auto` = phone-first horizontal
  scroll, no clip) + an "open full-size ↗" link for pinch-zoom + a provenance stamp:
  "RULED V1.2 · Q19 LOCKED 2026-07-13 · generator render_v1_2_stratified.py · source
  commit <8-char sha linked to GitHub>". Fetches plane-provenance.json (falls back to
  known constants if absent). Placed after the STATUS banner, before the quiet FLOW nav.
- **CONTRACT-ADJACENT (§7.7 rule 7):** rule 7 says /atlas renders NO occupancy numbers —
  because it forbids HAND-derived occupancy (dual-source-of-truth failure class). This
  raster is DB-DERIVED (`render(corpus.db)`, same class as `chart = render(atlas.json)`),
  so it honors the provenance law. No parse grammar touched → no jack-ryan §2 gate.
  SURFACED to KR/gandalf/jack-ryan for awareness (drax made the render call per commission).
- **Smoke:** `npm run build` GREEN (parse green, stage-assets ran, tsc + vite built).
  Preview served root + `/atlas` (200 via SPA rewrite) + SVG (200 `image/svg+xml` 259859 B)
  + provenance JSON (source_commit 62183c1a). Bundle carries AtlasPlaneView. No routing
  config touched (vercel.json unchanged) → no re-smoke beyond preview.
- **NOT deployed** — production Vercel deploy is Matt-gated (ADR-006). Awaiting Matt go.

### PHASE 2 v3 (ONE kit per dot — nearest-dot hover) — BUILT 2026-07-13

Matt: "show one kit at a time, depending on which dot you hover over" (replaces v2's
scrollable per-cell kit list). Per-dot hover needs each on-screen dot bound to a specific
kit — which the CELL-addressed JSON alone cannot do. Solved IN-LANE by reading the render's
OWN dot coordinates back from the committed SVG (same faithful method as the cell-geometry
read galadriel verified for v2), NOT invented coordinates.

- **Position binder (`stage-assets.mjs` → `plane_dot_positions.json`, schema
  `atlas-plane-dot-positions/v1`):** parses the committed SVG's `<g PathCollection>` `<use>`
  elements (each carries a dot's EXACT pixel x/y). Attribution: **glyph → kind** (circle
  `me898b4409d` = corpus · star `m219d2e7fba` = mint · diamond `md1ae64e445` = amp-null
  sliver), **centroid-y sort → stratum** (FLAT always above SPIKY above VAR), **kit-order
  within a scatter group** (render scatters each cell+stratum in `corpus_kits` order;
  `build_dot_records` iterates the same order — verified in `assign_all`). **Fail-loud
  per-group COUNT reconciliation** against the JSON: 463/463 grid dots bound exactly
  (455 corpus circles + 6 mint stars + 2 sliver diamonds). If a future re-render breaks any
  assumption the count check throws → stage-assets WARNs and skips the positions file → app
  DEGRADES to the cell-level list (never emits silently-wrong bindings). matplotlib orders
  SVG groups by GLOBAL zorder (all corpus first, then mint/diamond) — so binding classifies
  each group independently (glyph+geometry), NOT by doc order.
- **Sliver honesty:** the render draws ONE diamond per cell aggregating all its amp-unkeyed
  kits (render line ~622), so dots sharing a marker (`shared_marker:true`) surface together
  in a small list titled "these kits share one marker (amp-unkeyed)". Current data: 2 such
  dots, each alone in its cell → each shows as a single kit.
- **App (`AtlasInteractivePlane` rewrite):** one transparent capture `<rect>` over the plane;
  `onPointerMove`/`onPointerDown` → viewBox coords (linear map, img+overlay share viewBox) →
  **nearest positioned dot within radius** (`DOT_HIT_R2 = 20²` vb units); a sky highlight
  ring marks the resolved dot; popover shows that ONE kit (title = `TITLE_REGISTER` register,
  detail = `public_label` + cell tags). Empty space / axis margins → nothing. UNMAPPED strip
  UNCHANGED (text region, not plotted per-dot) → keeps its cell-level list popover from
  `plane_dots_v1_2.json`. Two-register split + negative_canon/cell_confident treatments
  carried over from v2.
- **Data flow:** app now fetches BOTH `plane_dot_positions.json` (grid per-dot) and
  `plane_dots_v1_2.json` (strip list). `.vercelignore` UNCHANGED — positions file is derived
  at build from already-allowlisted sources; git-ignored under `public/atlas/`.
- **Smoke:** `npm run build` GREEN (parse green, stage-assets emitted "+ dot positions",
  tsc clean, vite built). Preview served root 200 + positions JSON 200 `application/json` +
  SVG 200. dist carries `plane_dot_positions.json` (463 dots).
- **galadriel visual pass (2026-07-13):** items 1–5 PASS — per-dot hover resolves the nearest
  dot; highlight ring is pixel-perfect (0.000 vb offset — the render's own coords used
  directly, no scale-transform drift); popover shows ONE real build name + mono public_label
  + cell tags; cursor-move changes which dot is ringed; UNMAPPED strip still a list. Caught a
  mobile defect (item 6): a left-side dot's popover CLIPPED off the left edge at 375px.
- **Clamp refix (commit `7edfd5f3`):** measure the rendered plane px width (`planeW`) and
  clamp the card center so half its width stays inside, in plane px space (replaces the fixed
  12%/88% that couldn't account for the ~272px card). galadriel RE-VERIFIED PASS — left dot
  now on-screen (title complete), right dot on-screen after horizontal scroll, desktop
  mid-plane still centered (0px shift). The earlier right "dead-zone" = cursor at the viewport
  boundary (plane is wider than 375px and scrolls), NOT a code bug.
- **Preview (Matt-gated for prod, ADR-006):** latest fixed build —
  `https://reincarnated-glance-frfn98i8m-matthew-wetmore-s-projects.vercel.app/#/atlas`
  (positions + root both 200). Commits: `d815fd0b` (v3 per-dot) + `7edfd5f3` (clamp refix).
- **NOT promoted to prod** — awaiting Matt go.

### PHASE 2 v2 (per-cell hover/tap POPOVER) — BUILT + galadriel-verified 2026-07-13

Matt's two changes: removed the docked cell-explorer panel ("let the plane breathe"); added
a small popover anchored to a cell hotspot showing real build names.

- **`AtlasInteractivePlane`** (replaces `AtlasCellExplorer`/`CellPanel`): a transparent `<svg>`
  overlay (SAME viewBox as the committed matplotlib render) places per-cell hotspot `<rect>`s
  over the 21 movement×delivery cells + the UNMAPPED strip. Hover/tap/focus → popover.
- **Geometry read DIRECTLY from the render's cell-background paths** (fill #0f1218): col-0 left
  x=110.542, row-0 (FREE-MOVE) top y=169.239, pitch 103.68, box 99.533. NOT a reconstructed
  affine. (First attempt used the rounded-rect M-start = cell BOTTOM edge → +1-row offset;
  galadriel caught it, fixed to true corners, re-verified 0.00 offset both corner cells.)
- **`PlanePopover`:** single kit → title = configured register + `public_label` + cell tags;
  multi-kit cell/strip → title = cell address, lists kits.
- **Two-register split → ONE field:** `TITLE_REGISTER: keyof PlaneDot = 'display_name'` (flip to
  `'public_display_name'` = one-line change; falls back to `public_label` so a flip never renders
  blank). NEVER renders `dot_id`.
- **Treatments:** `negative_canon` (d2-sacrifice) → muted "historical exhibit" + "negative canon"
  tag; `cell_confident:false` (45 roster + strip) → "position provisional" note (names final,
  movement-axis position S7-pending).
- **Data:** `plane_dots_v1_2.json` (gandalf commit 17885eb7, 515 dots + `display_name`): 463 grid
  + 52 strip. stage-assets copies it; `.vercelignore` allowlists it; `public/atlas/` git-ignored.
- **Verified:** build GREEN; galadriel visual pass PASS (alignment 0.00 offset, popover real names,
  no docked panel, mobile 375px popover on-screen). Commits `123abaab` (v2) + `836ae8fa` (align fix).
- **Deployed to PREVIEW only** — Matt decides prod promotion (ADR-006).

### PHASE 2 (interactive mouseover) — BUILT 2026-07-13, awaiting deploy go

Both upstream gates cleared: (a) gandalf per-dot JSON + `public_label` derivation (commit
`6968c793`, `plane_dots_v1_2.json`, schema `atlas-plane-dots/v1.2`, 508 dots); (b) elrond
S1 P5 `era_year` (524/524). Spec: `agentic_orchestration/drax/notes/2026-07-13-atlas-plane-phase2-mouseover-spec.md`
(the pixel-hover assumption there is SUPERSEDED — the shipped JSON is CELL-addressed, no x/y).

- **CELL-addressed, not pixel-addressed.** The JSON carries `cell {movement, delivery, amp}`
  with NO coordinates. So we did NOT fake hover hotspots on the static raster (that would
  invent coordinates the truth model does not contain). Instead: a faithful data-driven
  **cell grid** — 4 movement rows (FREE-MOVE / WALK / ROOTED / unmapped) × 8 delivery
  columns (+ unmapped) — rendered straight from the JSON. Tap/hover a cell → panel lists its
  kits grouped by amp stratum, each by its **`public_label`** (NEVER `dot_id`).
- **Staging:** `stage-assets.mjs` now copies `plane_dots_v1_2.json` → `public/atlas/` (WARN,
  not fatal, if absent — SVG still renders). `.vercelignore` allowlists the JSON source so
  it uploads on remote builds. `public/atlas/` now git-ignored (derived, single-source-of-truth).
- **Honesty affordances (per data contract):** occupancy counts DERIVED live from JSON (never
  hardcoded); roster overlay dots (`movement:null`, 45) sit in a labelled **S7-pending** band —
  names final, only movement-axis POSITION awaits S7; `cell_confident:false` dots marked `◇`;
  `negative_canon:true` wired to a muted "historical exhibit" style (0 in corpus yet — lights
  up when the negative catalogue lands).
- **Components:** `AtlasCellExplorer` + `CellPanel` in `src/App.tsx`, siblings of `AtlasPlaneView`,
  rendered below the SVG + provenance stamp on `/atlas` only.
- **Smoke:** `npm run build` GREEN; staged `dist/atlas/plane_dots_v1_2.json` (508 dots) served
  200 `application/json`; root route 200.
- **NOT deployed** — Matt decides preview vs prod + galadriel visual check (ADR-006).

### v1.9 — kit-design reference TRIO (§7.7) — LANDED 2026-07-11

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
