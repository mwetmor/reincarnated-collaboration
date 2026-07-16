# drax charge — v1.12 atlas port: interactive Build Horizon re-homes to Glance at Edition III + loadout `/atlas` retires (ONE pass, STOP at preview)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Governing contract:** `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md` **§7.8 (v1.12)** — read it in full before starting; it is the ruling of record.
**Authority:** Matt 2026-07-16 (verbatim): *"It was supposed to be on the glance app. … But I do want it on glance."* + *"Could you please extend the first column width to accomodate the full name size?"* + Edition-III freeze ratified (*"Agreed. Ratify Edition III"*).

## Why (context you need)

The interactive Build-Horizon package (your D1–D6 chain) was built on `reincarnated-loadout` `/atlas` — that home was spec-line drift, never a ruling; Matt's standing 2026-07-09 ruling is Glance-standalone. Meanwhile glance `/atlas` (v1.11) serves the STATIC Edition-I plates + the projection-atlas tracker card. v1.12 reconverges: **the interactive instrument becomes the glance `/atlas` page lead at Edition III; loadout `/atlas` retires to a redirect.** One served truth, one code home.

## Inputs (gandalf-verified, trust them)

**Edition-III artifacts (galadriel render, gandalf VERIFY ACCEPT — shas re-derived, FIT-layer byte-frozen independently confirmed, eyes on plate/footer/rails/new-cells):**
- `agentic_orchestration/galadriel/captures/2026-07-16-atlas-edition3/atlas-edition3-instrument.svg` — sha256 `77c9baf5585d1b7d2ead21377bca931cdcd1980eb54df1d3a165612d01cebfdf`
- `agentic_orchestration/galadriel/captures/2026-07-16-atlas-edition3/atlas-edition3-archive.svg` — sha256 `8c94ee0564314e5563373c2340f4209ea0daa7612d4344e9f5394e541b3595fa`
- `render-provenance.json` same dir. Plate reads **Build Horizon — Edition III**; footer `Edition-III · feasibility-cuts-register-v1.3 · emitted 2026-07-16T02:12:43…`; rails carry the corrected outward arrows.
- **Data emission (slim-builder input):** `agentic_orchestration/research/curated/atlas/atlas-edition3.json` (`edition: 3`; census: corpus 709 · occupied meso 202 · pull-lit 4 · denominators 767,411,820 / 11,160 / 1,314 / 1,080+54). Build-input vendor only — **never shipped to the client** (same law as Edition-II).

## The pass (sequenced — port proves out BEFORE loadout retires)

### Stage 1 — PORT into `glance/app`

Move the interactive package from `~/Games/reincarnated-loadout` into `glance/app` (collab repo):
- `src/pages/Atlas.tsx` + `src/components/atlas/*` + `src/utils/atlas*` + the slim-builder (the build step that derives `atlas-interactive.json` from the vendored emission by copy/group of emitted fields, build-fail guard intact) + the corpus.db read-only sidecar (D1-h provenance names) + the probe harness (`scripts/atlas/d6-verify-probe.mjs` class).
- **Router adaptation:** glance uses hash-routing (`parseHash` / `PageId` in `glance/app/src/App.tsx`), not BrowserRouter. Adapt mechanically. If adaptation forces component REWRITES beyond mechanical, HALT and surface.
- **Page structure per §7.8:** interactive instrument LEADS the `/atlas` page; the §7.7 projection-atlas tracker card (FLOW bar + TRIPLE-LAW cross-links + drill-through) STAYS below it. The v1.11 static Edition-I plates lead RETIRES (superseded by the instrument; git keeps them).
- All D-chain law carries as-is: D4/D5/D6 mount write-set (viewBox · planeClip · plate · svg-sizing · frame), D6-b legend (v2 occlusion class), two-bound zoom (§8), D1-f fluid width (this route only — other glance pages keep their layout), D1-i community vocabulary.
- Dependencies: if glance/app lacks a package the port needs, add it — enumerate every added dep in the return. **The parser and parse shapes are FORBIDDEN territory — zero changes there.**

### Stage 2 — VENDOR Edition-III on glance

Both SVGs + provenance as glance stage-assets (the v1.10/v1.11 Edition-I stage-assets precedent, upgraded target); slim-builder consumes `atlas-edition3.json` + sidecar. sha256 the vendored copies in the return (must equal the inputs above).

### Stage 3 — the name-column fix (Matt's order)

The ported table's first (name) column: `atlasColumns.ts` `BUILD_COLUMNS` `grow: 6` + `LeafRow.tsx` `min-w-0 shrink-0 truncate` clips long live-build names. Make the name column **content-fitting** so the LONGEST live-build name renders whole (measure or min-width derived from content; your implementation call — no truncation on any live-build name at desktop widths; state mobile behavior). The D3-a untouchable on `atlasColumns.ts` is LIFTED by Matt's direct order — note it in the diff receipt.

### Stage 4 — loadout retires `/atlas` (only after Stages 1–3 build clean)

- `/atlas` route → redirect to `https://reincarnated-glance.vercel.app/atlas`.
- DELETE the atlas page/components/utils/build-step/probe from loadout (one code home — a dead copy invites future fix-passes editing the wrong tree) + remove `public/atlas/` vendored artifacts. Loadout nav drops the tab.

### Stage 5 — suites + builds + STOP at previews

Both apps: suite green, build green, local previews UP (state exact URLs/ports + launch commands in the return). **NO PRD deploys, NO alias moves** — gandalf verify gates promotion (the ratified render → gandalf-verify → drax-ship chain, §7.8 rule 4).

### Stage 6 — probe the glance preview

Ported probe, re-targeted: **v2 occlusion class law** (legend overlay intersects NO in-artifact `<text>` bbox ±4px and NO drill-in dot; ghost speckle/boundary curves non-binding), both skins, 1440 + 1280 + 375, dark + light where applicable. Edition-III content MOVES text and dots — legend placement must RE-verify, never carry. If no placement satisfies: HALT-don't-shrink, surface.

## Return contract

Enumerated diff receipts (glance adds; loadout removals; every added dependency; the atlasColumns change flagged) · vendored-artifact sha256s · suite/build receipts both apps · preview URLs + launch commands · probe JSON receipts (textOcclusions=0 across the matrix) · name-column receipt (longest live-build name, rendered whole — name it and screenshot it) · judgment calls surfaced, not buried. Auto-commit collab repo + loadout repo. **NO push either repo. NO PRD.**

## HALT conditions

Router adaptation exceeds mechanical → HALT · founding-law conflict (anything server-side, LLM, hand-authored state, parser touch) → HALT · occlusion unsatisfiable → HALT · suite regression you can't attribute → HALT with the failing receipt.

**Signed:** gandalf — executing Matt's re-home ruling under contract v1.12; my verify gates the two-deploy promotion (glance PRD + loadout redirect).
