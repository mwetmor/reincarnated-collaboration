# Dispatch — Drax Cosmograph Phase A Rendering at `/forge`

**Date:** 2026-06-06
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-06 multi-iteration design call ratifying primitive-vocabulary lock + cosmograph Phase A commission + Option B amendment (ALL constellations PROVISIONAL simulated at /forge; cycle 14 corpus stays at /loadout)
**To:** drax (loadout + demo player-surface seam)
**Cycle:** cosmograph Phase A (creation-moment manifestation milestone) — drax-side rendering build
**Type:** PIXI.JS COSMOGRAPH RENDERING + LASSO INTERACTION + PROVISIONAL VISUAL DEMARCATION + VERCEL DEPLOYMENT
**Cost budget:** $0 LLM (no LLM calls at /forge per Option B amendment + D7)
**Time budget:** ~3-5 sessions drax wall-clock (Phase 1 setup ~0.5; Phase 2 primitive-star layer ~1; Phase 3 constellation + faction layer ~1; Phase 4 lasso + side panel ~1; Phase 5 polish + deploy ~0.5-1)
**Critical anchors:**
- `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/cosmograph_README.md` (drax ingestion contract — load-bearing input)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 (architectural-anchor lock — primitive-as-star + kit-as-constellation + Option B amendment)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (Layer 0 + Layer 0.5 + derivation chains)
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` (cell schema § 3 + flag enum § 4 — flag-family side-panel reference)
- `agentic_orchestration/gandalf/notes/2026-06-06-cosmograph-star-granularity-verdict.md` (Pattern A-deep verdict — interaction model + lasso resolution algorithm § 4.3)
- `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md` (substrate-coverage honesty)
- `agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md` (predecessor elrond commission; this dispatch composes on its delivered packet)

---

## 0. TL;DR

Elrond Phase 4 packet delivered 2026-06-06: 570 primitive stars + 1000 PROVISIONAL simulated kit constellations + 7 emergent faction halos + flag-family attachments + drax ingestion contract. Drax now builds the **cosmograph rendering surface at `/forge`** in the reincarnated-loadout React/Vite app — a WebGL star-field with constellation lines, lasso interaction, faction halos, and a side panel showing primitive flag families.

**Critical scope boundaries** (Option B amendment 2026-06-06):
- ALL 1000 constellations at `/forge` are **simulated PROVISIONAL** — rendered with DOTTED/DIM line-styling + `bc_cell_NNNN_simulated` placeholder identifiers + literal narrative string `"PROVISIONAL — engine has not yet composed this pattern."` No LLM-named identities at /forge.
- Cycle 14 named-bearer corpus (Duskweaver + 36 others) **STAYS at `/loadout`** — drax does NOT touch the existing loadout-side cycle-14 surface. `/forge` and `/loadout` coexist as **forward-looking-future-engine** and **current-engine-showcase** surfaces respectively.
- Faction overlays cluster **by attribute group (STR / INT / WIS)** rather than per-element — this is what the substrate said (elrond Finding 2). Render the structure honestly.

**Five-phase execution:**
- **Phase 1** — Project setup + ingestion-contract validation + Pixi.js scaffold at `/forge` route (~0.5 session)
- **Phase 2** — Layer 0 primitive-star rendering (570 stars; brightness ∝ bdi_weight; provenance-tag visual encoding) (~1 session)
- **Phase 3** — Layer 1 constellation + Layer 2 faction halo rendering (1000 dotted constellations + 7 halos + region-label overlays) (~1 session)
- **Phase 4** — Lasso interaction + side panel + flag-enum visualization (~1 session)
- **Phase 5** — Performance pass + zoom + viewport culling + Vercel deploy (~0.5-1 session)

**Pre-fire Pattern-A query opportunity:** § 9.1 (Pixi.js-in-loadout vs alternative renderer — drax may surface preference before Phase 1 fires).

**Substrate-led discipline applied throughout:** render what the substrate says (89/11 weapon-form ratio at token level; attribute-group factional structure; provenance-tag design-history layers) — do NOT manufacture cosmetic uniformity.

**Math-before-code applied (Discipline #1):** § 6 lays out the math-hotspots (lasso polygon point-in-polygon resolution; viewport culling thresholds; performance envelope projections) BEFORE drax writes code.

**Framing-audit Q1-Q3 applied at Phase 1 start** (per OP § 4 + 2026-06-06 NA-substrate-blind recognition). See § 2.1.

---

## 1. Scope

### 1.1 What drax produces

A new route + rendering surface in the `reincarnated-loadout` React/Vite app at `/forge`, deployed to Vercel production:

| Artifact | Format | Purpose |
|---|---|---|
| `/forge` route in `reincarnated-loadout/src/pages/Forge.tsx` | React page component | Hosts the cosmograph rendering surface |
| Cosmograph rendering component (Pixi.js / WebGL canvas) | `src/components/Cosmograph/` | Star-field + constellation + halo + lasso layer rendering |
| Substrate-data loader | `src/data/cosmographData.ts` + `src/utils/parquetLoader.ts` (or JSON-converted intermediate) | Reads elrond packet artifacts; exposes typed views |
| Side panel component | `src/components/Cosmograph/SidePanel.tsx` | Lasso-resolved kit display + flag-enum visualization + provenance-tag legend |
| Region-label overlay component | `src/components/Cosmograph/RegionLabels.tsx` | BC bin sky-regions + tier bands + scaling-pattern bands + emergent mechanic-family labels |
| Faction-halo overlay component | `src/components/Cosmograph/FactionHalos.tsx` | 7 convex-hull polygon halos |
| Lasso-resolution module | `src/utils/lassoResolution.ts` | Point-in-polygon resolution per dispatch § 6.2 contract |
| Nav update | `src/components/Nav.tsx` | New "Forge" nav item linking to `/forge` |
| `MIGRATION.md` entry (loadout repo) | Cross-seam handoff per ADR-004 | Documents ingestion contract + data placement + new dependencies |

### 1.2 What drax does NOT produce in this commission

- **No changes to `/loadout`, `/kits`, `/analytics`, `/encounters`, `/court`, `/pitch`, `/state-of-engine`, `/planning`, `/sample` pages.** Cycle 14 named-bearer corpus stays at `/loadout` per Option B amendment.
- **No LLM calls or LLM-derived names rendered at `/forge`.** Per D7 + Option B amendment, every constellation displays `bc_cell_NNNN_simulated` placeholder; identity_narrative is the fixed PROVISIONAL string.
- **No q-score display anywhere in `/forge`.** Per dispatch § 1.2 of predecessor elrond commission and `cosmograph_README.md` rendering rules — all sim kit q-scores are null and must not surface.
- **No engine integration / runtime kit generation.** Drax reads the static elrond packet; cosmograph is a read-only artifact-display surface.
- **No materialization-cinematic integration.** The post-confirm Veo cinematic is parked per cosmograph-pivot record § 4.2 — empirical-evidence trigger is cosmograph lasso → resolve flow operational, which is what this commission DELIVERS but does not yet consume.
- **No demo-Pixi surface changes.** `reincarnated-demo/` is untouched.

---

## 2. Phase 1 — Project setup + ingestion-contract validation + Pixi.js scaffold

**Duration:** ~0.5 session drax
**Output:** `/forge` route renders an empty Pixi.js canvas + substrate-data loaded into memory + ingestion-contract validation report
**Discipline anchors:** framing-audit Q1-Q3 BEFORE execution (Discipline #42); math-before-code (Discipline #1); empirical inspection over assumption at parquet-schema-vs-ingestion-contract validation (Discipline #11 — see § 2.5); cross-seam impact (Discipline review-principle § 3); MIGRATION.md per ADR-004

### 2.1 Framing-audit Q1-Q3 (PRE-EXECUTION)

Per OP § 4 + 2026-06-06 NA-substrate-blind recognition, audit the commission scope BEFORE execution:

| Q | Audit question |
|---|---|
| Q1 | What load-bearing framing assumptions does this commission depend on? (elrond Phase 4 packet ingestion contract is FROZEN; Option B amendment ALL-PROVISIONAL holds; primitive-as-star + kit-as-constellation architecture per cosmograph-pivot § 9 is locked; Pixi.js is the chosen renderer per dispatch trigger language; `/forge` is in reincarnated-loadout React/Vite app not reincarnated-demo) |
| Q2 | What evidence currently in hand could refute these assumptions? (packet is delivered + read-only; Option B amendment lives in canonical/story/; renderer choice is in dispatch trigger but cross-seam mode-selection note flags it as verify-with-mode-selection — see § 9.1 Pattern-A query opportunity; loadout app currently has zero Pixi.js dependency — adding it is a real cross-seam impact) |
| Q3 | If refutation evidence exists, is the right move to refine the framing rather than execute as-framed? (Pixi.js-in-loadout is the only meaningful refinable — see § 9.1; everything else is locked) |

**Drax-side action:** if § 9.1 Pattern-A query fires, surface to gandalf within ~30 minutes via knight-rider routing. If no query fires, capture framing-audit completion in commission notes + proceed to § 2.2.

### 2.2 Loadout repo prep + Pixi.js dependency installation

Loadout app current state (verified 2026-06-06):
- React 19 + Vite 8 + TypeScript 6 + Tailwind 3 + react-router-dom 7
- recharts 3.8 (only data-viz dependency)
- No Pixi.js / Three.js / WebGL libraries

Required additions:
- `pixi.js@^7.4.2` (match version used in reincarnated-demo — `reincarnated-demo/package.json` already pins this version; consistency reduces cognitive load when both seams evolve)
- `@pixi/react@^7.1.x` recommended for React integration (Pixi v7 React bindings) — drax may select alternative React-Pixi binding if a cleaner choice exists
- Parquet reader: lightweight client-side parquet library (e.g., `parquetjs-lite` or `apache-arrow`) OR pre-convert parquet → JSON at build time via Vite plugin. See § 2.4 for recommendation.

### 2.3 `/forge` route stub

Add to `src/App.tsx`:
```
<Route path="/forge" element={<Forge />} />
```

Add to `src/components/Nav.tsx`:
- New `<NavItem to="/forge">Forge</NavItem>` placed after `<NavItem to="/state-of-engine">Engine</NavItem>` (or design-aesthetic equivalent placement; Forge is forward-looking future-engine surface, Engine is current-engine-state surface — adjacency reads correctly).

Create `src/pages/Forge.tsx` with stub component that renders:
- Page title "Forge — Substrate Cosmograph (Provisional Future-Engine View)"
- Subtitle making explicit: "All constellations on this page are SIMULATED placeholders. They show the future-engine substrate vocabulary, not real kits. Cycle 14 real kits live at [Loadout](link to /loadout)."
- Empty `<CosmographCanvas />` component placeholder (Pixi.js mount point)

### 2.4 Data placement + parquet handling

**Source data:** copy elrond packet files to `reincarnated-loadout/public/data/cosmograph/`:
- `primitive_registry.parquet` (~42 KB)
- `kit_constellations.parquet` (~339 KB)
- `flag_enum_attachments.parquet` (~56 KB)
- `region_labels.json` (~9 KB)
- `faction_overlays.json` (~54 KB)

**Recommendation — pre-convert parquet → JSON at build time:** the packet is ~500 KB total and static; adding a runtime parquet parser to the client bundle (parquetjs-lite ~150 KB) is heavier than a one-time build-time conversion script. Create `reincarnated-loadout/scripts/convert-cosmograph-data.ts` that reads the parquets and emits gzipped JSON to `public/data/cosmograph/`. Vite serves gzipped JSON natively + browser caches it. Bundle stays lean.

**Alternative (drax discretion):** if drax prefers runtime parquet loading for symmetry with future engine deliveries, use `apache-arrow` for streaming read. Surface preference in § 9.1 Pattern-A query if non-trivial.

### 2.5 Ingestion-contract validation (empirical inspection per Discipline #11)

Before Phase 2 fires, drax performs empirical inspection of the delivered substrate against the dispatch-declared ingestion contract. Discipline #11 applies: do not assume the parquet packet matches the schema this dispatch declares — verify by reading the files and asserting row counts + column populations + value ranges.

Validation checks:
1. `primitive_registry`: 570 rows present; all required columns populated; `bdi_weight ∈ [0.10, 1.00]`; `embedding_x`, `embedding_y` populated for all rows
2. `kit_constellations`: 1000 rows present; all `is_simulated=true`; all `cell_status="PROVISIONAL"`; all `kit_name == kit_id`; all `q_scores`, `pareto_rank`, `archive_status`, `gauntlet_pass_rate` null
3. `flag_enum_attachments`: 1000 rows; one per kit_id; mean `flag_count ≈ 15.6` ± 2
4. `region_labels`: bc_bin_labels.total_bins === 34; emergent_mechanic_family_labels.cluster_count === 6
5. `faction_overlays`: 7 factions with non-empty `polygon_convex_hull`

If any validation fails → drax STOPS and surfaces to gandalf via Pattern-A query (~30-min response target). Substrate-led discipline: if the substrate is malformed, do NOT manufacture a workaround at the render layer.

### 2.6 Phase 1 acceptance criteria

- `/forge` route resolves in dev server (`npm run dev` at port 5173 — `vite.dev/` shows page stub)
- Pixi.js dependency installed; bundle build succeeds (`npm run build`)
- All 5 substrate data files served from `/data/cosmograph/`
- Ingestion-contract validation report saved to commission notes (or surfaced if validation fails)
- Framing-audit Q1-Q3 captured (or Pattern-A query fired per § 9.1)
- MIGRATION.md updated in loadout repo with `/forge` route + new dependency + data placement summary

---

## 3. Phase 2 — Layer 0 primitive-star rendering

**Duration:** ~1 session drax
**Output:** 570 stars rendered with brightness gradient + element-coupling color + provenance-tag visual encoding + default-zoom-77-stars layer
**Discipline anchors:** substrate-led (#41); design-history visibility per packet README § "Design-history visibility"

### 3.1 Star rendering rules

Per `cosmograph_README.md` "Drax rendering rules" under `primitive_registry.parquet`:

| Visual property | Substrate field | Rendering rule |
|---|---|---|
| **Position** | `embedding_x`, `embedding_y` | Direct projection. Normalize UMAP coordinate range to canvas pixel space at default zoom (canvas roughly 1200×900 logical px; UMAP range typically ~10-15 units → ~80 px per UMAP unit). Center embedding centroid at canvas center. |
| **Brightness** | `bdi_weight` | `alpha = 0.35 + 0.65 × bdi_weight` (so faintest 0.10 reads at ~0.42 alpha; brightest 1.00 reads at 1.00 alpha). Render as Pixi `Graphics` filled circle OR Pixi `Sprite` of a soft-glow texture for sub-pixel star feel. |
| **Size** | `bdi_weight` × primitive_family weight | Base star radius 2-3 px; T4 strategies + capstone-keystones (`bdi_weight ≥ 0.85`) render at 5-6 px with subtle bloom filter. Retired DEFENSIVE_TRADEOFF (provenance `retired-but-preserved`; `bdi_weight=0.20`) renders at 1.5 px ghost. |
| **Color** | `element_coupling_json` + `attribute_coupling_json` | Element-coupling drives base hue (fire=warm-red; water=cyan; earth=amber-brown; wind=pale-green; lightning=violet; holy=warm-gold; shadow=deep-purple; physical=neutral-steel; DEX-marker=distinct accent per asymmetry). Attribute-coupling drives saturation/brightness modulation. Uncoupled primitives (e.g., generic geometry primitives that couple to none) render in neutral starlight white. |
| **Provenance encoding** | `provenance_tag` | Distinguishing chromatic shift per design-history layer: `CORE_14` geometries baseline color; `B11_EXPANSION` slight cyan-shift; `B13_DEFENSIVE_MOBILITY` slight green-shift; `active-v1.13` T4 strategies baseline; `retired-but-preserved` desaturated + dashed outline; `architecture_A_taxonomy_sibling_v1` (9 sub-element flavors) faint connecting filament to parent element; `deferred_placeholder_v1_2026-05-24` VIT attribute renders as faint outline only (no fill). |
| **Visibility at default zoom** | `visibility_at_default_zoom` | 77 first-class stars (true) render at all zoom levels; 493 drill stars (false) render only when zoom level > 1.5× default. |

### 3.2 Painterly cosmic aesthetic register

Per cosmograph-pivot record § 3 + § 4: the rendering aesthetic is **painterly cosmic** — the L1 apprentice Veo prompt validated this as the right register. Drax's Pixi.js rendering should:
- Use a deep-space background (near-black with subtle gradient toward navy at edges)
- Render stars with a soft-glow effect (radial alpha falloff) rather than crisp pixel disks
- Optional: faint "nebula" background field (very-low-opacity element-coupled tint regions reflecting where each element's primitive cluster sits) — this gives the sky depth without competing with the stars
- AVOID solar-system / orbital-path / hexagonal-grid visual reflexes (these were the Veo failure modes; deliberate avoidance is required since drax-rendering doesn't have those reflexes natively but cosmetic temptation may surface)

This is a **register-locked aesthetic** — Matt has ratified the painterly cosmic register at the cosmograph-pivot record level. Phase 5 polish allows refinement, but the core register is locked.

### 3.3 Performance envelope (math-before-code per Discipline #1)

**Projection for 570 stars at default zoom + 77 first-class stars at all zoom levels:**

- Pixi.js v7 with WebGL renderer comfortably renders 10,000+ sprites at 60fps on commodity hardware. 570 stars is well below threshold.
- BUT: when constellation lines (Phase 3) + lasso layer (Phase 4) + 7 halo polygons (Phase 3) render simultaneously, total draw-call count rises. Math:
  - 570 star sprites = 1 batched draw call (Pixi auto-batches sprites with same texture)
  - 1000 constellations × ~13 mean primitives per constellation × 2 endpoints per line segment ≈ 26,000 line segments worst-case. Spanning lines (constellation = lines connecting all primitives in primitive_set) at full render = expensive. **Mitigation:** render constellations only when within lasso vicinity OR at high zoom; default zoom shows constellation centroids only (1000 small dim points).
  - 7 convex-hull faction polygons = 7 fill draws + 7 stroke draws = 14 draw calls. Negligible.
- **Target frame rate:** 60fps sustained at default zoom on M1-class hardware + 2017+ Intel laptops; degrade gracefully to 30fps at higher zooms with many constellations visible.
- **Viewport culling:** at non-default zoom (zoomed in), only render primitives + constellations whose bounding box intersects the visible viewport. Pixi supports this natively via `cullable=true` on Containers + viewport-relative culling logic in render loop.

**Empirical-evidence trigger:** Phase 5 perf measurement on Vercel preview deploy — if 60fps not sustained at default zoom on baseline M1 hardware, surface to gandalf for Phase B optimization commission. Do NOT prematurely optimize in Phase A.

### 3.4 Phase 2 acceptance criteria

- 570 stars visible on canvas at correct embedding coordinates
- Default zoom shows 77 first-class stars prominently; drill stars dim/hidden until zoom > 1.5×
- Brightness gradient legible (faint vs bright differentiation clear to the eye)
- Element-coupling colors render (e.g., fire-coupled stars warm-red; water-coupled cyan) — provides intuitive sky-coloring
- Provenance-tag visual encoding present (B11_EXPANSION geometries distinguishable from CORE_14; retired DEFENSIVE_TRADEOFF visibly ghost; VIT attribute visibly faint-outline)
- Painterly cosmic aesthetic register applied (deep-space background; soft-glow stars; no solar-system reflexes)
- 60fps sustained at default zoom in Chrome on M1-class hardware

---

## 4. Phase 3 — Layer 1 constellation rendering + Layer 2 faction halo rendering + region-label overlays

**Duration:** ~1 session drax
**Output:** 1000 dotted PROVISIONAL constellations + 7 faction halos + BC bin sky-region labels + tier bands + scaling-pattern bands + 6 emergent mechanic-family centroid labels
**Discipline anchors:** Option B amendment compliance (D7 — no LLM names; explicit demarcation); substrate-coverage honesty (#59 — attribute-group factional structure rendered as substrate said it)

### 4.1 Constellation rendering rules (1000 PROVISIONAL)

Per `cosmograph_README.md` "Drax rendering rules" under `kit_constellations.parquet`:

- Each constellation = a set of LINES connecting its primitive stars (use `primitive_set_json` to compute spanning lines)
- Constellation line-style for PROVISIONAL: **DOTTED** (Pixi `Graphics` with `lineStyle({ width: 0.5, color: 0xffffff, alpha: 0.25, dash: [2, 3] })` or equivalent — visually distinct from any future "CONFIRMED" solid-line state)
- Line color: faint white at default; slight tint toward `surface_B_element_class` ("physical" → cool-neutral; "caster" → warm-element-tinted)
- Constellation centroid (`centroid_x`, `centroid_y`) = label anchor point; centroid renders as small dim circle (1.5 px, alpha 0.3)
- **NO kit_name label rendered.** The kit_name is the `bc_cell_NNNN_simulated` placeholder — visually rendering it as text would clutter the sky AND violate Option B amendment intent. On hover, the side panel shows the placeholder ID + the literal narrative string `"PROVISIONAL — engine has not yet composed this pattern."`

### 4.2 Constellation spanning-line algorithm (math-before-code per Discipline #1)

The naive approach — draw a line from every primitive to every other primitive in the kit — produces N×(N−1)/2 lines per kit. For mean 13 primitives/kit and 1000 kits = 78,000 line segments worst-case. This will not render at 60fps.

**Recommended approach — minimum spanning tree (MST) per constellation:**
- For each kit, compute MST over its primitive set using Euclidean distance in (embedding_x, embedding_y) space → N−1 edges per kit
- 1000 kits × 12 mean edges = 12,000 edges total — tractable at 60fps with batched draw
- MST produces visually coherent "constellation shapes" (paths through related primitives) rather than dense crisscross meshes

**Alternative (drax discretion):** "centroid star" pattern — draw lines from constellation centroid to each member primitive (N lines per kit) → 13,000 lines total, slightly more than MST but visually simpler. Trade-off: centroid-star pattern is uniform across all constellations (visually less distinctive); MST pattern produces constellation-character. **Lean: MST.**

**Cull-when-not-relevant:** at default zoom, render only constellation centroids (1000 dim points). Constellation lines render when (a) lasso intersects them OR (b) user zooms in OR (c) faction-overlay toggle highlights specific faction's constellations.

### 4.3 Faction-halo rendering (7 emergent factions)

Per `faction_overlays.json` schema + `cosmograph_README.md` rendering rules:

- For each of 7 factions, draw a translucent halo using `polygon_convex_hull` vertices (Pixi `Graphics.drawPolygon`)
- Halo fill color encoded by `modal_primary_element` + `modal_attribute` combination:
  - STR-modal factions (physical primary) → warm-amber/steel halo
  - INT-modal factions (fire/water/lightning/shadow primary) → blue/violet halo
  - WIS-modal factions (earth/wind/holy primary) → green/gold halo
- Halo opacity: 0.10-0.15 (subtle context; not visually competing with stars or constellations)
- Halos may overlap (factions are not strict partitions; k-means k=7 produced overlapping convex hulls)
- Faction label rendered at `centroid` coordinate, prefixed with `"[Emergent] "` per ingestion contract — uses `faction_label_placeholder` text (e.g., `"[Emergent] emergent::physical|STR|hyb22"`)

### 4.4 Substrate-coverage honesty in faction rendering (elrond Finding 2 disposition)

Per elrond's honest substrate read: the 7 emergent factions cluster **by attribute group**, not by per-element identity. This is what the substrate actually has at the current substrate snapshot. The cosmograph must render this truthfully.

**Drax-side disposition:** render the 7 attribute-group halos as the primary faction overlay. Do NOT manufacture per-element halos to balance the visual. Per Discipline #41 + #59: the substrate is the truth; if a player asks "where are the fire-faction lines?", the honest answer is "the substrate currently clusters factions by attribute group; per-element factional identity will surface post-Phase 5+ LLM cohesion clustering on the Pareto-reduced ~30-kit population per Option A iter 5 lock."

**Optional secondary overlay (drax discretion; Phase 5 polish if budget):** a toggleable "element-coupling shell" overlay that tints regions of the sky by dominant element-coupling. This is decorative + does NOT pretend to be factional. Surface as Phase B follow-on if Phase A budget tight.

### 4.5 Region-label overlay rendering

Per `region_labels.json` ingestion contract:

| Label family | Rendering rule |
|---|---|
| BC bin labels (34 total) | NOT first-class stars per ingestion contract. Render as ambient navigation overlay — subtle bounding-box outlines around primitive clusters that match each BC bin's substrate fingerprint. Label text small + low-opacity (alpha 0.4). Toggle-on optional. |
| Skill-tree tier labels (T1/T2/T3/T4) | Render as horizontal "skill-tree-depth bands" — faint horizontal stripe across the canvas labeled at left edge. T4 capstone band aligns with T4-strategy primitive cluster (extra-bright stars). |
| Scaling-pattern-per-tier labels | Same horizontal band pattern; offset slightly from tier bands. Smaller label text. |
| Chain architecture labels (3-chain / 4-chain) | Two faint vertical demarcations OR small icon glyphs in the legend area. Minimal visual weight. |
| Emergent mechanic-family labels (6 per Phase 3 clustering) | Render at each cluster's centroid (`centroid_x`, `centroid_y`) — small text reading e.g., `"emergent::damage\|close\|high"` in muted color. Reading the cluster's substrate-led label gives the player the genre vocabulary the engine learned. |

**Discoverable, not loud:** all region labels render with low default opacity (0.3-0.5); on hover/proximity, opacity bumps to 0.8. This keeps the cosmograph clean at default state + lets players discover the sky's structure on exploration.

### 4.6 Phase 3 acceptance criteria

- 1000 constellation centroids visible at default zoom (dim points)
- MST-derived constellation lines render on lasso hover OR explicit zoom-in trigger
- All constellation lines are DOTTED (not solid); visually communicates PROVISIONAL status
- 7 faction halos visible as translucent polygons; colors honor attribute-group modal mapping
- Faction label placeholders rendered with `"[Emergent] "` prefix
- Region label overlays render at low default opacity; hover brightens them
- 6 emergent mechanic-family centroid labels visible at correct cluster centroids
- 60fps sustained at default zoom; degrades gracefully under zoom-in with constellation lines visible
- Substrate-coverage honesty preserved (attribute-group factional structure NOT cosmetically manufactured to per-element)

---

## 5. Phase 4 — Lasso interaction + side panel + flag-enum visualization

**Duration:** ~1 session drax
**Output:** Interactive lasso with point-in-polygon resolution + side panel rendering lasso-matched kits with flag-family visualization
**Discipline anchors:** lasso-resolution math per dispatch § 6.2 + cosmograph-star-granularity-verdict § 4.3; D7 (no LLM-derived names in side panel)

### 5.1 Lasso interaction layer

- Player draws a closed polygon on the cosmograph by click-drag (start point sets first vertex; subsequent mouse moves extend the polygon; mouse-up closes the polygon)
- During draw: lasso polygon renders as bright translucent shape (Pixi `Graphics.drawPolygon` with thin solid border + light fill)
- On mouse-up: lasso closes; resolution algorithm fires (see § 5.2)
- Player can re-lasso freely (each new draw clears the prior selection)
- "Clear" button in side panel resets lasso state
- Optional (drax discretion): "shift-click" to add discrete primitives to the lasso set (per cosmograph-star-granularity-verdict § 4.4 DP12 lean toward click-to-add for accessibility)

### 5.2 Lasso-resolution algorithm (math-before-code per Discipline #1)

Per `cosmograph_README.md` lasso-resolution input contract + cosmograph-star-granularity-verdict § 4.3:

```
INPUT:
  lasso_polygon: Polygon (list of {x,y} vertices in cosmograph coordinate space)
  primitive_registry: 570 stars with (embedding_x, embedding_y)
  kit_constellations: 1000 kits with (centroid_x, centroid_y) + primitive_set

OUTPUT:
  matched_kits: ranked list of kit_ids whose constellation best covers lasso

ALGORITHM:
  1. Compute SET of primitive_ids whose (embedding_x, embedding_y) is inside lasso_polygon
     (point-in-polygon test — ray-casting algorithm; O(P × V) where P=570 stars, V=lasso vertices)

  2. For each kit_constellation k:
     a. coverage_fraction = |lasso_primitives ∩ k.primitive_set| / |k.primitive_set|
     b. density_score = |lasso_primitives ∩ k.primitive_set| / |lasso_primitives| (if lasso_primitives empty → 0)
     c. weight_score = sum of (bdi_weight × indicator(primitive ∈ lasso) for primitive in k.primitive_set) / sum of bdi_weight in k.primitive_set
     d. composite_score = 0.4 × coverage_fraction + 0.3 × density_score + 0.3 × weight_score

  3. Sort kits by composite_score descending; return top 3 (or top 5 if drax preference) for side panel display

EDGE CASES:
  - If lasso encloses 0 primitives → side panel: "Your lasso enclosed no primitives. Try a wider region."
  - If top-2 composite_scores within 5% of each other → side panel shows BOTH as ambiguous matches; player can narrow lasso
  - If no constellation scores ≥ 0.3 → side panel: "Your lasso falls between charted constellations. Nearest match (provisional): {top-1}"
```

**Performance projection:**
- Point-in-polygon: 570 stars × V vertices per lasso (typical V ≤ 20) = ~11,400 ray-cast tests = <1 ms in JavaScript
- Composite-score for 1000 kits: each kit has mean 13 primitives → set intersection + score computation ≈ 13,000 element checks = <2 ms
- Sort + top-N: trivial
- **Total lasso-resolution latency: <5 ms** — instant interactive feel

### 5.3 Side panel layout (right-side fixed-width column or modal)

When lasso resolves → side panel shows the top-1 (and optionally top-3) matched kits:

| Section | Content |
|---|---|
| Header | `bc_cell_NNNN_simulated` placeholder ID + status badge "PROVISIONAL" |
| Identity narrative | Literal string: `"PROVISIONAL — engine has not yet composed this pattern."` (per Option B amendment + D7) |
| Lasso match metrics | Coverage fraction + density score + composite score (visible to player as honest signal of match quality; not pretending the match is more certain than it is) |
| Surface B element class | "physical" or "caster" (informative tag; not styled as identity) |
| Primary element + attribute | From `primary_element` + `kit_attribute` (e.g., "fire / INT") |
| Hybrid flag | If `is_hybrid=true`, display "Hybrid (2 primary elements)" |
| Primitive set | List of primitive labels in the kit, with load-bearing primitives (top 3 by `bdi_weight`) highlighted. Each primitive entry shows label + family + provenance_tag if non-baseline (e.g., "B11_EXPANSION") |
| **Flag families** (per § 5.4) | Grouped flag visualization |
| Faction membership | Which of the 7 emergent factions this kit belongs to (with `"[Emergent] "` prefix on label) |

**No q-scores rendered. No pareto_rank rendered. No gauntlet_pass_rate rendered.** All these fields are null for sim kits per Option B amendment; rendering them as "—" would be honest but rendering them at all risks visual implication. Omit entirely.

### 5.4 Flag-enum side-panel grouping

Per `cosmograph_README.md` flag_enum_attachments rendering rules + hypothesis-flow doc § 4:

Group the flag_set_json into named families with visual chips:

| Group label | Flag prefix filter | Visual treatment |
|---|---|---|
| Substrate | `SUBSTRATE_ELEMENT_*`, `SUBSTRATE_ATTRIBUTE_*`, `SUBSTRATE_CULTURAL_*` | Earth-tone chips |
| T4 strategy | `T4_*` | Capstone-bright chips (gold-outline) |
| Kit architecture | `KIT_SINGLE_ELEMENT` / `KIT_HYBRID_2_ELEMENT` | Structural-blue chip |
| Validation | `VALIDATION_PROVISIONAL` (all sim kits) | Faded chip with status icon |
| Coupling | `COUPLING_LIGHT_3_LAYER` / `COUPLING_MEDIUM_4_5_LAYER` | Mechanical-grey chip |
| Variant | `VARIANT_PUSH` / `VARIANT_SPEEDFARM` / `VARIANT_BALANCED` | Brighter tactical chip; variants are player-facing concepts |
| Investment | `INVESTMENT_MEDIUM` | Default chip |
| Power plane | `PLANE_HOLDS_ACROSS_ALL` | Default chip |
| Target pattern | `TARGET_PATTERN_BOSSING` / `TARGET_PATTERN_SPEEDFARMING` / `TARGET_PATTERN_BALANCED` | Tactical chip aligned with variant |
| Cell shape | `CELL_SHAPE_SPECIALIZED` | Default chip |
| Emergent label | `EMERGENT_LABEL_AMBIGUOUS` (all sim kits — pending Phase 5+ LLM naming) | Faded chip + tooltip explaining future-naming |

Chip layout: vertical list grouped by family, each family with a small header. Hover chip → tooltip with full flag enum string + brief explanation drawn from hypothesis-flow doc § 4.

### 5.5 "Heuristic-derived vs empirical-derived" disclosure

Per ingestion contract: for sim kits, most flags are HEURISTIC-DERIVED from primitive set; they will become EMPIRICAL-DERIVED when cycle 15+ runs real kits through math validation + gauntlet + Phase 5 cohesion judge.

**Side panel disclosure:** small footnote at the bottom of the flag panel reading: `"Flags shown are heuristic-derived from the simulated primitive set. They become empirically-derived once the engine validates real kits against this substrate (cycle 15+)."`

This is **honest signal** — players who notice the flags shouldn't be misled into thinking they reflect playtest reality. The cosmograph at /forge is forward-looking; the disclosure makes that explicit at the flag layer.

### 5.6 Phase 4 acceptance criteria

- Click-drag lasso renders correctly + closes on mouse-up
- Lasso-resolution algorithm fires in <50 ms (well below interactive-feel threshold)
- Side panel shows matched kit(s) with all required sections
- All sim kits display literal narrative string + PROVISIONAL badge (no LLM-derived names)
- Flag-family chips render with correct grouping + tooltips
- Heuristic-derived disclosure footnote present
- No q-scores / no pareto_rank / no gauntlet_pass_rate visible anywhere
- Edge cases (empty lasso; ambiguous match; no-match-≥0.3) handled gracefully with explanatory side-panel text

---

## 6. Math-before-code summary (Discipline #1)

Math hotspots that drax should validate BEFORE writing code:

| Hotspot | Math projection | Drax-side validation |
|---|---|---|
| Star rendering at 570 sprites | Pixi.js v7 + WebGL: 10K+ sprites at 60fps possible; 570 sprites single batched draw call | Phase 2 acceptance — verify 60fps on M1 hardware |
| Constellation line rendering | MST approach: 1000 kits × ~12 edges = 12,000 line segments. Batched line draws scale; render constellations conditionally (lasso vicinity / zoom-in / faction-highlight) | Phase 3 acceptance — verify centroid-only render at default zoom + on-demand constellation lines |
| Faction halo polygon fill | 7 polygons × draw call = 14 draw calls. Negligible. | Phase 3 acceptance — visual + perf check |
| Lasso point-in-polygon resolution | 570 stars × ~20 vertices = ~11,400 ray-cast tests per lasso = <1 ms in JS. Composite score over 1000 kits = <2 ms. | Phase 4 acceptance — measure lasso-resolve latency |
| Viewport culling at zoom-in | Pixi `cullable=true` on Container; bounding-box intersect test per visible region | Phase 5 perf pass — verify zoom-in stays at 30fps+ on baseline hardware |
| Initial data load | ~500 KB packet (gzipped JSON ~200 KB); single fetch on `/forge` mount; parse + index in <100 ms | Phase 1 acceptance — measure load-to-first-render |

**No math hotspot requires Pattern-A query consultation a priori** (Discipline #18). All projections sit within standard envelope. If any measured performance falls outside projection by >2× in Phase 5, surface to gandalf for methodology review BEFORE optimization.

---

## 7. Cross-seam impact + Discipline anchors

### 7.1 Cross-seam impact

| Seam | Impact |
|---|---|
| **elrond** | None — packet is read-only consumption by drax |
| **rocket / gamora / star-lord** | None — engine seams untouched |
| **galadriel** | None — no CV pipeline involvement at /forge |
| **drax-demo (reincarnated-demo Pixi.js seam)** | None — /forge is loadout-side; demo Pixi work is separate. NOTE: pixi.js version `^7.4.2` matches what demo already uses; if drax wants to lift Pixi-related utility code from demo to a shared package in future, that's a cross-seam composition opportunity (Phase B follow-on; not in this commission scope) |
| **jack-ryan** | Gate-1 pre-fire review on THIS dispatch; Gate-2 post-output review on Phase 5 Vercel preview |

### 7.2 Discipline anchors (per `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`)

| Discipline | Application |
|---|---|
| #1 — Math-before-code | § 6 summary; performance projections (lasso latency, MST line counts, sprite-batching draw calls, viewport-culling thresholds) precede implementation |
| #11 — Empirical inspection over assumption | § 2.5 parquet-schema-vs-ingestion-contract validation BEFORE Phase 2 implementation; Phase 5 measured FPS vs projected FPS deviation check; lasso-resolve latency measurement vs projected <5 ms |
| #18 — Math-hotspot methodology consultation | Lasso-resolution + viewport culling are math-near; standard envelope; surface only on deviation >2× |
| #41 — Substrate-led | Render what the substrate says (attribute-group factional structure; 89/11 token ratio reflected in star coloring; provenance-tag design-history layers) |
| #42 — Framing-audit Q1-Q3 | Applied at Phase 1 start (§ 2.1) |
| #59 — Substrate-coverage honesty | Side panel discloses heuristic-derived flags; PROVISIONAL badging; substrate-coverage gaps not papered over |
| D7 (AI-tell line) | No LLM-named identities at /forge; placeholder IDs only; literal narrative string |
| ADR-004 | MIGRATION.md per cross-seam handoff in loadout repo |

---

## 8. Acceptance criteria (jack-ryan Gate-2 verification target)

### Content criteria
1. All 1000 simulated constellations display with DOTTED line-style + PROVISIONAL badge + literal narrative string `"PROVISIONAL — engine has not yet composed this pattern."`
2. NO LLM-derived kit names anywhere on /forge (every kit shows `bc_cell_NNNN_simulated` placeholder)
3. NO q-scores / NO pareto_rank / NO gauntlet_pass_rate displayed anywhere on /forge
4. 570 primitive stars render at correct embedding coordinates with bdi_weight-driven brightness gradient
5. Provenance-tag visual encoding present (retired DEFENSIVE_TRADEOFF ghost; VIT faint-outline; B11_EXPANSION distinguishable)
6. 7 faction halos render with attribute-group color mapping per elrond Finding 2 — substrate-honest, not cosmetically per-element
7. 6 emergent mechanic-family centroid labels render with substrate-led labeling (e.g., `"emergent::damage|close|high"`)

### UX criteria
8. `/forge` route resolves; "Forge" nav item present linking to it; page header explicit about PROVISIONAL forward-looking nature
9. Lasso interaction draws + closes + resolves matched constellation within <50 ms
10. Side panel renders top-1 match (or top-3 if ambiguous) with full flag-family chip layout + heuristic-derived disclosure footnote
11. `/loadout` route + all other existing pages UNCHANGED (cycle-14 corpus untouched per Option B amendment)
12. Painterly cosmic aesthetic register applied (deep-space background; soft-glow stars; no solar-system reflexes)
13. 60fps sustained at default zoom on M1-class hardware; 30fps+ under zoom-in with constellation lines visible
14. Vercel preview deploys successfully + sustains interactive frame rate in production build
15. MIGRATION.md updated in loadout repo documenting new route + Pixi.js dependency + data placement

### Substrate-honesty criteria
16. Element-coupling tinting of stars reads correctly (fire warm-red; water cyan; etc.)
17. Substrate-coverage gaps NOT cosmetically masked (attribute-group factional structure rendered as elrond Finding 2 said; no manufactured per-element halos in Phase A)
18. Surface B physical/caster classification rendered in side panel (informative; not styled as identity)

---

## 9. Pre-fire Pattern-A query opportunities

Drax is authorized to fire Pattern-A queries to gandalf BEFORE Phase 1 execution if any of the following surface:

### 9.1 Renderer choice (Pixi.js vs alternative) — REAL question

The dispatch trigger language specifies "Pixi.js (canvas/WebGL) star-field rendering" — but loadout app currently has zero Pixi.js dependency. The cross-seam mode-selection note flags this explicitly: "verify with mode selection."

**Three options drax may consider:**

| Option | Pro | Con |
|---|---|---|
| **(a) Pixi.js v7 in loadout** (recommended in this dispatch) | Matches demo Pixi version; team familiarity; mature WebGL renderer; native batching | Adds ~200-300 KB to loadout bundle; new dependency in formerly Pixi-free repo |
| **(b) Three.js** | Industry-standard 3D + 2D WebGL | Heavier; team has less Three experience; overkill for 2D scatter |
| **(c) HTML Canvas 2D API + React** | Zero new deps; lightest bundle | Less performant at scale; more code to write for batching/culling; team less familiar with manual canvas optimization |
| **(d) D3 + SVG** | Familiar React data-viz; declarative | SVG performance degrades past ~1000-3000 elements; not viable at 570 stars + 12,000 line segments |
| **(e) `react-pixi-fiber` / `@pixi/react`** (recommended React binding for option a) | Declarative React composition over Pixi v7 | Adds binding layer; usually fine |

**Recommendation in this dispatch: (a) + (e).** Matches the trigger language + Pixi already in the ecosystem (reincarnated-demo) + drax/team familiarity. But this is a **legitimate refinable decision at drax's seam authority** — if drax has strong technical reason to prefer (c) HTML Canvas 2D (e.g., bundle-size minimization), fire Pattern-A query before Phase 1.

### 9.2 Parquet handling — preference question

§ 2.4 recommends pre-converting parquet → JSON at build time. If drax prefers runtime parquet read for symmetry with future engine deliveries, fire Pattern-A query before Phase 1.

### 9.3 Constellation rendering algorithm — MST vs centroid-star

§ 4.2 recommends MST per constellation. If drax has UX-aesthetic preference for the centroid-star pattern (visually simpler uniform shapes), surface preference; not a blocker.

### 9.4 Side-panel placement — fixed column vs modal vs drawer

§ 5.3 leaves placement open. Loadout app's existing pages use fixed-width right-column layouts (`KitBrowser`, `Loadout`). Recommendation: match that convention for visual consistency. Fire Pattern-A query if alternative reads better against Forge's full-canvas rendering need.

Pattern-A query format: cheapest empirical refutation or alternative recommendation; ~30-min surface time to gandalf via knight-rider routing.

---

## 10. Commission close protocol

When Phase 5 acceptance criteria met:

1. Drax authors wave-close record at `agentic_orchestration/drax/cosmograph-phase-a-2026-06-XX/wave-close-record.md` capturing: Vercel preview URL + screenshots + perf measurements (FPS at default + zoom-in) + lasso-resolve latency measurements + any deviations from spec
2. Auto-commit work-products per CLAUDE.md team commit discipline (work-products of authorized cycle / workstream)
3. Push to remote remains Matt-explicit-authorization (default) — drax surfaces Vercel preview URL + waits for Matt push-pattern authorization OR Matt direct-confirm before pushing to production
4. Knight-rider routes Gate-2 jack-ryan acceptance verification (18-criteria checklist § 8)
5. On Gate-2 PASS → Matt signal-receive → commission CLOSED → cosmograph-pivot record updated with Phase A landing status

**Empirical-evidence triggers for downstream work:**
- If Phase A Vercel preview surfaces D7 violation OR validation muddiness OR substrate-led-discipline violation → elrond config flag flip to reduce sim count (per cosmograph-pivot § 9.4 trigger)
- If Phase A Vercel preview surfaces compelling lasso → constellation flow → re-engage gandalf for post-confirm Veo cinematic design (cosmograph-pivot § 4.2 trigger)
- If Phase A Vercel preview surfaces visualization clutter OR cognitive-load issues → Phase B optimization commission (cosmograph-star-granularity-verdict § 7.2 trigger)
- Future cycle 15+ engine regeneration against future-engine substrate → "real" kits become real constellations at /forge progressively (cosmograph-pivot § 9.4)

---

## 11. Sign-off

**Authored:** gandalf 2026-06-06 per Matt 2026-06-06 directive at dispatch fire time + elrond Phase 4 delivery + Option B amendment compliance + cosmograph-pivot § 9 architectural-anchor lock
**Authority:** Matt 2026-06-06 multi-iteration design call (primitive-vocabulary lock + cosmograph Phase A commission + Option B amendment ratification)
**Anchor evidence:** elrond Phase 4 packet (100% plausibility QA pass; Surface B 42.80/57.20 within tolerance; KMeans-k=6 emergent labels at mean purity 0.95; 7 faction halos via convex hull) + cosmograph-star-granularity-verdict Option 4 adopted + cosmograph-pivot § 9 amendment + atomic-substrate-registry CANONICAL + hypothesis-flow-pattern-library CANONICAL + Pattern-A weapon-form-ratio verdict
**Empirical-evidence trigger for commission close:** Phase 5 Vercel preview URL operational + 18-criteria Gate-2 jack-ryan acceptance PASS + Matt signal
**Cross-seam routing:** Gate-1 jack-ryan pre-fire review BEFORE Phase 1 fires (math-before-code Pixi.js perf + cross-seam ingestion contract validation + Pixi.js-in-loadout dependency-add review per standard critique-pair pattern); knight-rider routes when this spec lands and Matt + jack-ryan signal pre-fire ratification

**End of drax cosmograph Phase A commission spec.**
