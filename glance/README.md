# Glance

One URL that shows the true state of the project — trackers, queues, blockers,
your-move items — **derived from canon on every push, authored by no one.**

Founding principle: **the glance layer is DERIVED, never authored.** Canon stays
in git as markdown; a deterministic parser emits a state model on every push; a
thin static app renders it. **No DB, no server, no LLM anywhere in the truth path.**

Owner: drax (web seam). Contract: `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`
(§ 3 state.json) + `canonical-doc-format.md` § 7 (the five legislated shapes,
RATIFIED jack-ryan 2026-07-06) + engineering-disciplines Discipline #60 (CI-fail-loud).

## Architecture (boring on purpose)

```
push to canonical/**   →  GitHub Action  →  parser (parser/parse.mjs, deterministic)
  or flight/records-*                        ├── app/public/state.json  (§ 3 contract)
                                             ├── MALFORMED shape  → CI FAIL (file+line)  [Discipline #60]
                                             └── dangling gates-on → warning badge (not a failure)
                          →  static deploy (Vercel — the loadout stack)
```

- **`parser/parse.mjs`** — the deterministic canon → `state.json` parser. NO LLM,
  NO network, NO judgment. Reads ONLY the four `canonical/current-to-end-state/`
  trackers + `surface-ledger.md` (the fifth Tier-0 card, v1.3 §7.2) + the five
  MATT-FACING product-pipeline docs (`pipeline-*.md`, §7.5/§7.6) + the three
  kit-design reference docs (`substrate-coordinates.md` · `mechanical-reality.md` ·
  `projection-atlas.md`, §7.7 v1.9) + `canonical/matt_decision_needed/README.md` +
  `canonical/matt_to_do/README.md` + `agentic_orchestration/flight/records-*.jsonl`
  (v1.13, below). **Never touches the engine tree.**
  - `node parser/parse.mjs` — write state.json; exit 1 on any MALFORMED.
  - `node parser/parse.mjs --report` — list ALL malformed findings in one pass
    (the reconciliation surface), then exit non-zero.
- **`app/`** — Vite + React 18 + Tailwind static SPA. Renders Tiers 0–2.

## v1.13 — the fleet REAR-VIEW card on `#/fleet` (U-1 § 12.4, CURRENT)

The U-1 flight-recorder tape is **committed** (spec fork F-8), so it already lives in the
tree the Action reads on every push. The fleet card is therefore a **parser extension, not a
new pipeline** — no new data path, no new truth, no sync job, still no LLM anywhere.

- **`parser/fleet.mjs`** — folds `agentic_orchestration/flight/records-*.jsonl` into a
  **pre-aggregated `fleet` node** on `state.json` (rollups, NOT raw rows: per-workstream cost,
  per-model scorecards, per-lane rollups, month trend, verdict history, window meters). Fold
  semantics mirror `flight/schema.py` — corrections drop superseded rows from the VIEW only,
  identity folds from ENQUEUE/START with CLOSE filling nulls, SEALED means a terminal event
  exists. Where the two disagree, the Python is right and this is the bug.
- **`app/src/pages/Fleet.tsx`** — the card. **REAR-VIEW SCOPE ONLY:** history, which does not
  stale, so a push-fresh render of it is honest. **No live lanes, no IN-FLIGHT, no HEALTH** —
  a Vercel build can only see PUSHED state, and rendering lane liveness from a tape snapshot
  would be a green pixel over an unknown exit code. Those facts are Mac-local and live on the
  **local fleet board** (`agentic_orchestration/factory/ui/board.py`), which reads the disk it
  runs on. One tape, two windows: Glance is the rear-view mirror, the local board is the
  windshield.
- **Absence is legal, twice:** no `flight/` directory → `fleet: null` → the card says so; a
  tape with zero rows → every rollup renders empty and honest. Glance never breaks on a repo
  without a recorder.
- **Vendor-lane parity (AM-1):** `grok-serial` renders wherever `codex-serial` does, including
  when it has no rows — "this lane has done nothing yet" is a different fact from "this lane
  does not exist". The v1 `grok-judge` spelling folds onto the same card.

## The parse contract — the five legislated shapes (canonical-doc-format § 7)

1. **STATUS banner** — first `**STATUS:**` blockquote (stamp + date + raw line).
2. **SESSION-DELTA LOG** — `### YYYY-MM-DD — headline`, newest-first, latest governs.
3. **Queue rows** — table (or modeled bullet) whose first cell begins with a row ID,
   carrying a status prefix (`✓ ⛔ ⚖ PARKED IN-FLIGHT OPEN`).
4. **`gates-on:` tokens** — `gates-on: <token> [(qual)] [· <token> …]` (AND-semantics).
5. **Matt queues** — Q/T-style IDs in the two README indexes; struck/appendix = resolved.

### CI severity split (Discipline #60 / § 7.6) — the discipline that makes CI livable

- **MALFORMED** (exactly 3 conditions: broken table structure on an ID-bearing row;
  unparseable delta date; duplicate row ID within one board) → **CI BUILD FAILURE**, file+line.
- **UNRESOLVED** (dangling `gates-on:` token) → **warning badge** + global counter. Visible debt, not a broken build.
- **ABSENCE** is never an error — a doc with no delta log, a table that isn't a queue: fine, rendered as prose.

## v1.10 — the RULED plane on /atlas (Phase 1, CURRENT)

`/atlas` now surfaces the **RULED V1.2 Stratified Plane View** (Q19 LOCKED 2026-07-13) — the
realized projection: 3 movement rows × 7 delivery columns × amp-tempo strata.

- **DB-derived static asset.** The plane is `chart = render(corpus.db)` (generator
  `render_v1_2_stratified.py`), staged from gandalf's committed SVG by
  `glance/app/scripts/stage-assets.mjs` into `public/atlas/` on every build, with a
  git-derived provenance stamp (`plane-provenance.json`). Single source of truth stays the
  committed render — an upstream re-render flows through on the next push. The staging step
  is KEPT SEPARATE from the parser (the parser's charter is `canonical/**` truth-model only).
- **`AtlasPlaneView`** (App.tsx), gated on the atlas reference: vector SVG scaled phone-first
  (`overflow-x-auto`, horizontal scroll on narrow phones, "open full-size ↗" for pinch-zoom)
  + provenance stamp linking the source commit to GitHub. ZERO new parse shapes.
- **Reconciles with §7.7 rule 7:** rule 7 forbids HAND-derived occupancy (dual-source-of-truth
  failure). This raster is DB-DERIVED, so it honors the provenance law — a render/layout call,
  not a parse-contract change.
- **Phase 2 (interactive per-dot naming-law tooltips)** is spec'd + GATED (per-dot data JSON
  from the render + elrond S1 era_year/patch columns): see
  `agentic_orchestration/drax/notes/2026-07-13-atlas-plane-phase2-mouseover-spec.md`.

## v1.9 — the kit-design reference TRIO (§7.7, CURRENT)

Three pages added (NINE total): **`#/coordinates`** (the LATTICE — `substrate-coordinates.md`,
9 stages §0–§8), **`#/atlas`** (the PROJECTION — `projection-atlas.md`, 6 stages §0–§5),
**`#/mechanics`** (the CODEX — `mechanical-reality.md`, 9 stages §1–§9). Seated adjacent in the
nav in the read-as-one-instrument order (coordinates → atlas → mechanics), behind a subtle divider
(they are a distinct kind: kit-design reference registers, not domain/process pages).

- **Render-only, ZERO new parse shapes.** The only parser change is a parse-scope line: the three
  docs join the read set as a new doc class (`REFERENCES`, parallel to `PIPELINES`). Same §2.7
  `parseFlow` — no new grammar.
- **Quiet bars BY DESIGN (§7.7 rule 3).** These are REFERENCE REGISTERS, not process pipelines —
  no §2.3 modeled queue rows. `parseReference` feeds `parseFlow` an EMPTY queue set so every stage
  derives `quiet` (navigation, not state). Their payload tables happen to carry first cells that
  match the row-ID grammar (`L0`, numbered rows) — feeding empty queues is what keeps the bar quiet
  and honors "do NOT parse the payload / do NOT invent coloring."
- **Verbatim payload (`extractSections` + `SectionMd`).** Each `## §N` section's raw markdown body
  is carried byte-verbatim in `state.json` and rendered faithfully by `SectionMd` (tables → HTML
  tables, fences → `<pre>`, prose → paragraphs) — DISPLAY FIDELITY, never a semantic parse. The
  lattice LADDER tables, the BINDING RESOLVER walkers, and the projection table are payload.
- **TRIPLE-LAW cross-links (§7.7 rule 4).** Each page links the other two, labeled by layer:
  Coordinates "WHERE a kit can sit" (LATTICE) ↔ Atlas "how the two map" (PROJECTION) ↔ Mechanics
  "WHAT the engine expresses" (CODEX). `/atlas` is the connective page (teal accent); its two links
  are the most load-bearing.
- **Per-stage drill-through.** FLOW segment / drill-strip tap → in-page scroll to the `## §N`
  section + a GitHub deep-link to the heading line (Tier-2 provenance).
- **`/atlas` renders NO occupancy numbers (§7.7 rule 7).** The §2 projection table renders exactly
  as authored (byte-verbatim); the REALIZED ATLAS emission harness is not built — that honesty is
  the point, never hand-patched.
- **`/` landing:** a lean grouped "kit-design reference" tile row (`ReferenceTileRow`) — compact
  LINK TILES, NOT full state cards (an all-quiet flow-bar card spends Tier-0 pixels on no info;
  drax layout call per §7.7 rule 5). Header-strip counters unchanged.

## v1.5 — the FIVE-PAGE SPLIT + the KITS page (§7.4, CURRENT)

The app is a hash-routed SPA (zero router dependency — the vercel.json SPA rewrite
funnels every path to index.html, so hash routes work identically in preview + prod):

- **Landing `/`** (`Landing`): the slim index — the ORIGINAL one-screen glance, preserved.
  The tracker cards + a SIXTH card, **Kits** (`KitsIndexCard`), whose face is the PART F
  roster tallies (25 K + 6 H, per-status counts, DERIVED from the pinned rows). Each card
  taps through (surface-ledger opens the header drawer; Kits → `/kits`). Plus "Since you
  last looked".
- **Five domain pages** `#/engine · #/story · #/game · #/content-emission · #/kits`
  (`DomainPage`): the four tracker pages render their Tier-0 card EXPANDED IN PLACE —
  flow-bar lead (§2.7) → STATUS → latest delta full + older collapsed → counters → queue
  tables (in-page Tier-1). All under the § 4 supersession law. Tier-2 deep-links unchanged.
- **BOTH process pages lead flow-bar-first:** `/engine` and `/content-emission` lead with
  their `## FLOW` pipeline view. (v1.4's rule that content-emission leads with the roster
  is DEAD — the roster moved to `/kits`.)
- **`/kits` page** (`KitsPage`): LEADS with the **KIT ROSTER OF RECORD** table (`KitRoster`,
  PART F, K1–K25 + H1–H6). Promoted by SECTION-NAME PIN (the serial tracker's `F.1…`/`F.2…`
  sub-tables) — zero new parse grammar. Columns as authored: ID · ARPG Genre Canon kit ·
  BC cell/hypothesis · status · blockers/held rules. Roster count + status tallies (25 K +
  6 H = 31) in the page header; cross-doc `gates-on:` tokens (proxy-P0/P1/P2, totem-probe)
  dangle as § 2.6 warning badges. **Feed-2 seam wired (not blocked):** when star-lord's
  registry-snapshot export lands (`agentic_orchestration/run-registry/emission-runs-snapshot.json`),
  per-kit cert truth auto-joins the roster rows; v1 renders doc truth only.
- **Global header strip on EVERY page** (`HeaderStrip`): the your-move pixel
  (open matt_decision_needed — the most important pixel; never dropped) · matt_to_do ·
  surfaces-agreed ✓N/M · last-commit age · dangling (gates + flow-refs) · five-tab nav ·
  the **surface-ledger drawer** (`SurfaceLedgerDrawer`) — compact, expandable, on every page.

## The six legislated shapes (Tiers 0–2 substrate)

Shapes 1–5 (STATUS · SESSION-DELTA · queue rows · gates-on · Matt queues) + shape 6
(§2.7 FLOW — the ordered end-to-end process view; derived stage-state, most-specific-first
ref resolution, dangling-ref warning badges). Every modeled claim deep-links to file+line
on GitHub (Tier 2). Parser enforces ORDER + BANNERS only — never semantic conflict detection.

## Staged — NOT built in v1 (§ 7 of the spec; clean seams left, no implementation)

- **Tier 3 — dependency graph** (`gates-on:` tokens as a live graph). Entry criterion:
  one full board cycle where new/edited open rows carry tokens + dangling rate < ~10%.
  Seam: `state.json.dangling_gates` + every row's `gates_on[]` already carry the graph edges.
- **RUN-STATE pane** (emission runs / registry / cert status). Entry criterion: the W1 #8
  run registry exists with ≥1 registered run. Seam: a second top-level view alongside `glance`.

## Local dev

```bash
cd app
npm install
npm run parse        # regenerate public/state.json from live canon
npm run dev          # vite dev server
npm run build        # parser (fail-loud) + tsc + vite build  → dist/
npm run build:preview  # tolerant build (writes state.json even on MALFORMED) for local preview
```

## Deploy

Standalone Vercel project **`reincarnated-glance`**. Production alias:
**https://reincarnated-glance.vercel.app** . Root Directory = `glance/app`.
`vercel.json` sets the SPA rewrite (all routes → index.html) — smoke-tested
locally before every deploy (the May-12 missing-rewrite 404 lesson). Production
deploys are Matt-authorized (ADR-006).

**Deploy from the meta-repo ROOT, not from `glance/app`.** The parser's only
input is the sibling `canonical/` tree (`../../canonical` from `glance/parser/`).
A CLI deploy from `glance/app` uploads only that subdir, so the parser can't
reach `canonical/` and the build fails (`Cannot find module .../parser/parse.mjs`
/ missing canon). Deploying from root uploads the whole context; Root Directory =
`glance/app` (set on the project) makes the build + install run there while the
parser still reaches `../../canonical`.

`.vercelignore` (at meta-repo root) allowlists the context to `glance/` +
`canonical/` only — Vercel CLI deploys ignore `.gitignore`, so without it a root
deploy would upload ~4GB of untracked heavy dirs. Keep it in lockstep with the
parser's input paths.

Redeploy:

```bash
cd ~/Games/reincarnated-collaboration   # repo ROOT (project is linked here + at glance/app)
npx vercel deploy --prod --yes          # Matt-authorized; preview = drop --prod
```

The parser's git best-effort reads (`repo_sha` / `last_commit`) return null in
the Vercel build context (no `.git` there) — by design, non-fatal.

Deployment SSO-protection is disabled on the project so the URL is publicly
shareable (standalone-app ruling). Re-enabling it would gate the URL behind
Vercel login.
