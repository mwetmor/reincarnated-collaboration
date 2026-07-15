# AGENT_STATE — Glance (drax web seam)

> Checkpoint for the Glance app (`glance/app` + `glance/parser`) — the derived-from-canon
> project-state web app. Owner: drax. This is the meta-repo's glance-seam continuity file
> (glance lives here, not in loadout/demo). Contract:
> `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`.

## Current version — v1.11 (/atlas leads with Atlas Edition-I ghost-field projection)

Tag: `glance/v1.11-atlas-edition1-ghost-1`. Nine pages unchanged.

### Atlas Edition-I r4 (ghost-horizon) + r5 (beyond-horizon) — RE-SHIPPED to /atlas PRD 2026-07-15

Two same-day re-ships under Matt's STANDING PRD auth for the ratified render→gandalf-verify→drax-ship
chain. Both are pure re-vendors of the SAME `atlas.json` (data commit `d0b2a025` UNCHANGED throughout);
only the render source dir + `collab_render_commit` moved. No parse-shape change, no code change beyond
the stage-assets vendoring pointer + provenance comment. gandalf verified each render before ship.

- **r4 (ghost-horizon), render commit `c27d7af7`** — repointed stage-assets vendoring from r3.2
  (`53db59a2`) to the r4-horizon capture. Strictly-additive chrome on r3.2: dashed ghost-horizon
  envelope + mandatory disclosure label; coverage callout re-led with the 1.9%-lit / 2.4-kits-per-lit
  headline pair. All frozen layers byte-identical vs r3.2. Deploy `dpl_9r4BWTciRWML8b8mzJFmdPBYz3xU`,
  READY/production, aliased canonical. Live SHA-256 == r4 source (served unmodified); horizon label +
  1.9% headline confirmed on the deployed instrument. Commit `2baa188d`.
- **r5 (beyond-horizon), render commit `0175faa5`** — repointed vendoring from r4 (`c27d7af7`) to the
  r5-beyond-horizon capture (`2026-07-15-atlas-edition1-r5-beyond-horizon`). r5 adds ONE wrapped
  microcopy line to the GHOST FIELD ledger plaque in both skins (beyond-horizon disclosure: "14 settled
  kits stand beyond the horizon — …"). gandalf-verified strictly-additive: single diff hunk, plaque rect
  grew upward 48px, nothing else moved; all data layers byte-identical to r4. Deploy
  `dpl_7VgezhpYZqnYqgG3wRWoTbwRDzjb`, READY/production, aliased canonical
  `https://reincarnated-glance.vercel.app`. Live receipts: served instrument SVG (200, `image/svg+xml`,
  668193 B) contains `14 settled kits stand beyond the horizon`; provenance JSON reports
  `collab_render_commit: "0175faa5"` + full `source_commit 0175faa5…` + r5 source paths +
  `collab_data_commit d0b2a025` (unchanged). BYTE-EQUALITY: prod-served SVGs SHA-256 == galadriel source
  (instrument `99f00c47…` · archive `6f5c16ed…`). `/atlas` SPA route 200. Commit: this session.

- **RE-SHIP MECHANISM (the load-bearing r4 lesson set — follow exactly for future re-vendors):**
  1. **The REAL vendoring seam is `glance/app/scripts/stage-assets.mjs` (`EDITION1_DIR_REL`)** — repoint
     the hardcoded capture path + bump `collab_render_commit` there. `public/atlas/` is git-ignored and
     RE-STAGED on every build; a bare byte-copy into `public/` (or `dist/`) does NOT survive `npm run
     build` — it gets overwritten by stage-assets. Change the source, then rebuild.
  2. **STALE-PREBUILT TRAP (my first r4 attempt shipped stale assets this way):** the authoritative
     prebuilt tree is `.vercel/output/static/` at the **collab meta-repo ROOT**
     (`/Users/admin/Games/reincarnated-collaboration/.vercel/`), NOT `glance/app/.vercel/`. Both dirs
     exist and both link the SAME project (`prj_R6SCwuSmezW19HPOLWKoJfMCxeYx`, root dir `glance/app`), so
     prebuilding/syncing at the app level looks right but deploys the OLD root tree. FIX: after `npm run
     build` in `glance/app`, `rm -rf` + re-`cp -R glance/app/dist/. → ROOT .vercel/output/static/`, then
     `npx vercel deploy --prebuilt --prod --yes` from the collab ROOT (NOT from glance/app — the linked
     Root Directory `glance/app` double-appends if cwd is already there). config.json (SPA rewrite:
     filesystem handle + `/(.*)`→`/index.html`) and builds.json (target=production, no error nodes) at
     the ROOT are already correct and reused as-is. `vercel build` itself is unusable here (`spawn sh
     ENOENT`) — assemble/sync the Build Output API v3 static tree by hand.

### v1.11 — Atlas Edition-I (r3.2 ghost-field) on /atlas — LANDED + DEPLOYED 2026-07-15

Ships galadriel's two verified deterministic Edition-I SVGs (the PCA-PROJECTION
instrument: 469 settled kits as a lit archipelago in the 10,080-cell feasible dark, with
the new ghost field + sealed ledger + census) to the `/atlas` (PROJECTION) page as the
LEAD, above the existing RULED V1.2 plane. Matt-authorized direct-to-PRD deploy of the
GLANCE APP (2026-07-15 verbatim: "have Drax launch this to the Glance Vercel app directly
to PRD"). Chain leg 3 of the Q30-ratified 3-leg chain. ZERO new parse shapes — a
render/layout addition (same class as v1.10).

- **VENDORED, not committed:** the collab meta-repo is NOT pushed where Vercel builds, so
  `stage-assets.mjs` copies the two committed SVGs from the galadriel capture dir into
  `public/atlas/` on every build (gitignored — single source of truth stays upstream; no
  duplicated committed binary). Provenance: render commit `53db59a2` / data commit
  `d0b2a025` (named in the stage-assets comment + the provenance JSON + the page stamp).
- **Provenance-law compliance (binding):** chart = render(atlas.json). The SVGs are served
  UNMODIFIED (byte-copy — never hand-edited, never scraped). The page's SURROUNDING copy
  cites ONLY numbers READ BACK FROM atlas.json (via `atlas-edition1-provenance.json`,
  emitted by stage-assets.mjs from the ghost_field/counts/denominators fields) — never a
  value scraped from the SVG, never a hand-typed constant. If atlas.json re-emits, the
  copy follows. Emitter integrity guard in stage-assets: `exact_post_red_law` must ==
  `depth_sum_check` or the build fails (refuse to stage a mislabeled chart).
- **Numbers on the page (all atlas.json-emitted):** 469 active · 693,146,160 feasible
  exact-grain (THE denominator) · 10,080 feasible meso cells · 192 lit · 1,260 sealed.
  Anti-drift greps on page source CLEAN: no season-N, no "2.57" as content, no
  "422,445,240". (The "2.57" substrings inside the SVG are SVG coordinate values, e.g.
  `cy="422.57"` — galadriel's own `R2-no-2.57-numeral` acceptance test already verified
  2.57 absent AS CONTENT; we serve the SVG unmodified.)
- **App (`src/App.tsx`):** new `AtlasEdition1View` component, gated on
  `reference.id === 'atlas'`. **Instrument skin = working default** (light), **archive skin
  = showpiece** reachable via an in-header SKIN TOGGLE (instrument ↔ archive) — my
  contract lean, exercised as-is. Renders the served SVG (`<img>`, `w-full min-w-[720px]`
  inside `overflow-x-auto` = phone-first horizontal scroll, no clip on 375px) + open-full-
  size (skin toggle live in the modal) + a provenance stamp naming both collab commits +
  the git-derived render commit + PCA inertia/dims. Explainer cites only the five
  atlas.json numbers; every content-locked element (RIDER-1 badge, explainer trio, census
  line, clip-disclosure line, coverage callout, sealed ledger, graveyard) is baked INTO
  the SVG (galadriel FULL-ACCEPT verified) and served un-obscured — never restated.
- **In-seam counters exercised (contract page-composition is my seam):** (1) LEAD ORDER —
  Edition-I placed ABOVE the RULED V1.2 plane (it is the newer PROJECTION-of-record; the
  3×7 grid stays as a complementary second lens, not deleted). (2) SKIN default =
  instrument, per Matt's counterable lean; kept it. (3) No occupancy HAND-derived (§7.7
  rule 7 honored) — Edition-I is `render(atlas.json)`, same DERIVED class as the plane's
  `render(corpus.db)`; the chart's numbers are emitted, never page-computed.
- **Smoke:** `npm run build` GREEN (parse GREEN, stage-assets vendored both skins + denom
  693146160, tsc + vite built). Preview served root + `/atlas` (200 SPA rewrite) +
  instrument SVG (200 `image/svg+xml` 665944 B) + archive SVG (200 `image/svg+xml`
  666120 B) + provenance JSON (200, all 5 numbers). Skin bg confirmed (instrument #f7f8fa
  / archive #0e1016). `vercel.json` UNCHANGED (no routing config touched) → SPA rewrite
  proven identical to production.

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
- **DEPLOYED TO PRODUCTION 2026-07-13** (Matt authorized per ADR-006): live at
  `https://reincarnated-glance.vercel.app/#/atlas` (canonical alias root + positions both
  200; deployment `reincarnated-glance-2bic3csus`). Commits: `d815fd0b` (v3 per-dot) +
  `7edfd5f3` (clamp refix). No routing/vercel.json change (no re-smoke beyond preview needed).

### PHASE 2 v4 (dual axes + interactive full-size) — BUILT + galadriel-verified 2026-07-13

Matt (four-part request): "remove the new legend … instead list each word as a secondary
axis on the right … change the horizontal axis titles on the left from horizontal to
vertical, this way we don't reduce atlas space … make the mouse-over work in the
'open-full-size' view … then move to PRD and then push." All four done IN-LANE (app
overlay only — the render was NOT touched).

- **(a) StratificationLegend REMOVED** — the right-hand legend box (v-just-prior, preview
  `reincarnated-glance-dgptuhaq5`, never prod) is gone, along with its `STRATA_BANDS` const.
- **(b) RIGHT secondary axis (amp strata):** FLAT / SPIKY / VAR drawn as live SVG `<text>`
  to the right of the grid, one triple PER movement row, each aligned to that cell's three
  amp-bands (`bandCenterY(ri,si) = CELL_Y0 + ri·PITCH + BOX·(2si+1)/6`). Faint divider line
  at `GRID_R+4`. Colour `#8AA0BC` (== render per-stratum count colour).
- **(c) LEFT movement labels HORIZONTAL→VERTICAL (space reclaimed):** the render bakes the
  movement labels horizontally in a ~110px left margin. Rather than re-render (out of lane +
  fragile — see NOTE), reclaimed IN-LANE: cropped the baked left margin out of the viewBox
  (`VB_X = CELL_X0 - LEFT_GUTTER`), masked residual with a `#0B0D10` rect over the row band,
  redrew `⇢⇢ FREE-MOVE / ⇢ WALK / ✕ ROOTED` VERTICALLY (rotate -90°) in a 30px gutter. Net:
  plane grid GAINS width. galadriel measured row-center dy = 0.0/0.0/0.0.
- **(d) Interactive full-size view:** "open full-size ↗" is now a BUTTON (was an `<a>` to the
  raw static SVG) opening a full-viewport modal that renders the SAME `AtlasInteractivePlane`
  — hover/tap works there too. Esc + "close ✕" dismiss.
- **Refactor:** `<img>` + separate overlay `<svg>` UNIFIED into ONE `<svg>` with
  `<image href=svgUrl>` + all overlays sharing one coordinate system (cannot drift). Wrapper
  uses `aspect-ratio: VB_W/VB_H`; pointer math + popover anchors rebased onto the cropped
  viewBox (`vbX = VB_X + …·VB_W`; `xPct = (px-VB_X)/VB_W`).
- **NOTE (why NOT a render change):** re-running `render_v1_2_stratified.py` is fragile for
  the binder — dots are deterministic (byte-identical re-render, verified) BUT matplotlib
  glyph IDs + clip-path IDs are NON-deterministic (`me898b4409d`→different each run), and the
  binder anchors on those IDs; a render geometry change would also shift every hardcoded app
  geometry constant + invalidate galadriel's 0.00-offset. So the axis relabel stays app-side.
  (Render remains gandalf-owned, untouched.)
- **Smoke:** `npm run build` GREEN (parse green · stage-assets green · tsc green, no unused ·
  vite built). Preview 200 root + positions + SVG. galadriel PASS all 4 items, desktop 1280 +
  mobile 375 (mask #0B0D10 exact, 9 strata labels band-aligned gapDelta ≤0.1px, hover + modal
  both interactive). No routing/vercel.json change → no re-smoke beyond preview.
- **DEPLOYED TO PRODUCTION + PUSHED 2026-07-13** (Matt authorized: "move to PRD and then
  push") — see deploy state below.

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
- **CURRENT PRODUCTION = Atlas Edition-I r5 (beyond-horizon), 2026-07-15.** Deploy
  `dpl_7VgezhpYZqnYqgG3wRWoTbwRDzjb` (`reincarnated-glance-l5pitb5s5…`), READY, target
  production, aliased to canonical `https://reincarnated-glance.vercel.app`. Render commit
  `0175faa5` · data commit `d0b2a025`. Live receipts: instrument SVG 200 `image/svg+xml`
  668193B contains `14 settled kits stand beyond the horizon` · archive SVG 200 668387B ·
  `/atlas` 200 (SPA rewrite) · provenance JSON `collab_render_commit "0175faa5"`. BYTE-EQUALITY:
  prod SVGs SHA-256 == galadriel r5 source (instrument `99f00c47…` · archive `6f5c16ed…`).
  Prior PRD deploys same day: r4 `dpl_9r4BWTciRWML8b8mzJFmdPBYz3xU` (render `c27d7af7`) ·
  v1.11 r3.2 `dpl_6bwdofFTU9g4VR3zLkV3CUz3pp8k` (render `53db59a2`). All under Matt's standing
  render→gandalf-verify→drax-ship PRD auth.
- **DEPLOY-PATH LEARNING (load-bearing — the collab repo is now UNPUSHED per Matt):** a
  normal `npx vercel deploy --prod` triggers a REMOTE Vercel build that runs the parser +
  stage-assets on Vercel's servers — which FAILS because the meta-repo is not pushed where
  Vercel builds (stage-assets can't find the vendored SVGs / capture dir; parser can't find
  `canonical/**`). The v1.10 deploy worked only because the repo was pushed then. NOW the
  correct path is a PREBUILT deploy: `npm run build` locally (where the capture dir exists
  and stage-assets vendors the SVGs into `dist/`), copy `dist/` → `.vercel/output/static/`,
  write `.vercel/output/config.json` (`{version:3, routes:[{handle:filesystem},{src:"/(.*)",
  dest:"/index.html"}]}` — the SPA rewrite), set `.vercel/output/builds.json` target=production
  (no error nodes), then from meta-repo ROOT run `npx vercel deploy --prebuilt --prod --yes`.
  NOTE: run from ROOT (not glance/app) — the linked project's Root Directory `glance/app`
  double-appends if cwd is already glance/app. `vercel build` itself is unusable in this
  environment (`spawn sh ENOENT`); assemble the Build Output API v3 tree by hand.

## Files (this session)

- `glance/parser/parse.mjs` — `REFERENCES` class + `parseReference` + `extractSections`; empty-queue
  quiet-bar law; references hoisted into `state.json` + report banner.
- `glance/app/src/state.ts` — `ReferenceId` / `Reference` / `ReferenceSection` types; trio pages in
  `PageId`/`PAGE_ORDER`/`PAGE_LABEL`; `REFERENCE_PAGES` / `isReferencePage` / `PAGE_REFERENCE` /
  `TRIPLE_LAW` / `TRIPLE_LAW_SIBLINGS`; `PAGE_TRACKER`/`PAGE_FLOW_SOURCE` → Partial.
- `glance/app/src/md.tsx` — `SectionMd` verbatim-payload renderer.
- `glance/app/src/App.tsx` — `ReferencePage` + helpers; landing tile row; nav divider; Partial guards.
- `glance/README.md` — v1.9 section + parser read-set.
