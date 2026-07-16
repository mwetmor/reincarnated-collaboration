# Atlas interactive Glance package — r7 restyle + semantic hooks + interactive page (spec)

**Date:** 2026-07-15
**Author:** gandalf (SPEC-AUTHOR / SCENEWRIGHT)
**Status:** v1.2 — cut on Matt's directive package 2026-07-15 ("When Drax moves it to PRD…" + three functional effects). One marked veto point (§1). **§8 v1-zoom amendment added same date on Matt's two-bound ruling. §9 D1 defect pass added on Matt's live-page defect report; D1-e/f (axis-pole vocabulary, fluid width) + D1-g/h/i (ghost axes as columns, build provenance names, community vocabulary builds/build-families) folded from Matt's second + third messages same date.**
**Authority:** Matt 2026-07-15 — black-copy lead · axis-title overlap fix · live/ghost color separation · basic selectable legend w/ slim highlight · hierarchical pivot table w/ chart wiring. PRD ship of this package pre-authorized by the same message. **v1 zoom (§8): Matt 2026-07-15 — "max zoom out would allow view of the full horizon-line and max zoom in would allow ease of selection for a single kit/ghost."**
**Companion docs:** `2026-07-11-atlas-chart-renderer-spec.md` (render law §§7–10; this note amends presentation + adds hooks as r7) · `research/curated/atlas/atlas-edition2.json` (data of record) · Glance app (`reincarnated-loadout` seam, drax).

---

## 0. Scope, seams, sequencing

Three seams: **galadriel** (r7 SVG restyle + semantic hooks), **drax** (interactive Glance page: legend, highlights, pivot table, black-skin lead), **gandalf** (this spec; verification at each hop).

**Sequencing (single-variable discipline):** the in-flight Edition-II render completes and verifies FIRST — it is the data-correctness baseline, and its acceptance-23 FIT byte-regression vs r6 is only provable on an unchanged visual grammar. r7 then restyles on FROZEN Edition-II data (its own regression law: geometry/coords byte-frozen vs Edition-II render; fills/strokes/layout re-baselined). Data-change and style-change never share a render.

Chain: Edition-II verify → **r7 render** → gandalf verify → **drax interactive build** → PRD (black copy leads) → **v1 zoom pass** (§8, a discrete pass AFTER the wiring pass verifies — single-variable discipline). Drax MAY begin the pivot-table component + data-slim script in parallel against `atlas-edition2.json` (data model is render-independent); interactive wiring waits for r7 hooks.

## 1. Four-class visual encoding (Matt fork — resolved with lean; VETO POINT)

Matt: live kits and ghosts are both grey, size-only distinct — confusing; "change the live kits color or the ghosts color." Ruling lean (proceed unless Matt vetoes):

**CORRECTED 2026-07-15 (against the Edition-II render + Matt's screenshot):** Condensations on this chart are the six NAMED groups (WHIRLWIND / TOTEM-SENTRY / TRAP-MINE / CHANNELED-BEAM / AURA / MINION-PET) and are ALREADY colored per-group. The grey-on-grey confusion is specifically **SINGLE (non-condensation) live kits vs ghosts** — both grey, split only by size. Encoding:

- **Ghosts KEEP grey** — they are ground (feasible-but-unlit lattice); ground recedes. Their aggregation grammar (log₂ size-step) is unchanged. Drill-in sub-glyphs stay subordinate-grey — but with a **visible-minimum prominence** (Matt 2026-07-15: the drilled dark beyond the whirlwind/beam kits must be legible at overview scale; a chart that hides its own P-DF-1 finding fails — this floor lands in the Edition-II render fix pass, not r7).
- **SINGLE live kits TAKE color** — figure advances. One saturated hue per skin, distinct from all six condensation group hues, from the death-class label accents, from ghost grey, from chrome; legible at smallest radius on both skins (galadriel proposes exact values).
- **Condensation members KEEP their six group colors** (already separable; unchanged).
- **Graveyard** keeps its † treatment (already separable).
- Basic-legend semantics (§4): "Live Kits" toggles singles + condensation members (all live marks); "Condensations" toggles the six groups' members; "Graveyard" the †s; "Ghosts" the meso + drill-in ground.

Rationale (genre-standard figure/ground): every ARPG overlay that works — D3 map pins, PoE atlas watchstones — colors the live layer and greys the potential layer, never the reverse. The four classes map 1:1 to Matt's basic-legend vocabulary (§4).

## 2. Axis title/description layout fix (r7)

The r2 explainer glosses + pole titles collide at the left/right margins (Matt observation; pole labels anchor at canvas edge x≈1498). Fix is **layout-only**: all content-locked strings (r2 lock) survive VERBATIM — the lock is on strings, not coordinates.

Directive: pole titles + their gloss blocks move to reserved margin bands that cannot intersect the plot rect or each other (corner blocks or out-of-plot rails; galadriel proposes exact geometry). Acceptance: bbox-intersection = zero between any two text blocks and between text and plot marks, both skins; content-locked strings grep verbatim.

## 3. Semantic hooks (r7 — enables ALL interactivity)

Ground truth (gandalf probe, r6 SVG): zero `class=`, zero `<g id=`. Flat SVG. Amendment:

1. **Layer groups:** `<g id="layer-ghosts">`, `layer-drillin`, `layer-graveyard`, `layer-live`, `layer-chrome`.
2. **Per-mark data attributes:** `data-el` ∈ {live, condensation, graveyard, ghost}; live/graveyard marks carry `data-kit` (kit_id; condensations carry `data-kits` member list); ghost glyphs carry `data-core` (7-tuple, `|`-joined, emitted core_order) + `data-mult`.
3. **§4c law extends:** hook values are emitted-field copies, never renderer inventions. Byte-determinism double-render law carries.
4. The SVG at rest remains a print-grade static artifact — hooks are inert attributes; NO scripts inside the SVG.

## 4. Basic legend + slim class-highlight (drax page)

- **Top-left BASIC legend**, four entries in Matt's vocabulary: **Condensations, Live Kits, Graveyard, Ghosts.** Sits above/beside existing chrome; does not displace the emitted in-SVG legend.
- Each entry **toggleable (multi-select).** Selecting a class highlights ALL its members: **stroke halo ≤ 0.75px, no fill change, no dimming of non-selected marks** — "very slim, almost non-existent; dots never obscured." Dark canvas: pale luminous stroke; light canvas: dark ink stroke. **(Skin-naming correction 2026-07-15: galadriel's `instrument` skin is the LIGHT canvas `#f7f8fa`; `archive` is the DARK one — verified against the Edition-II SVGs. All skin selection downstream binds to CANVAS, never to skin name.)**
- Implementation: page-injected CSS targeting the §3 layer groups / `data-el` — the vendored SVG bytes are untouched at rest.

## 5. Hierarchical pivot table (drax page, below chart)

**Data:** build-time derivative `atlas-interactive.json`, generated by a Glance build script FROM the vendored `atlas-edition2.json` by **copy/group of emitted fields only** (no invention; build-fail guard on missing/renamed fields — same guard class as the provenance JSON). Contents: per-kit rows {kit_id, class live|graveyard, condensation membership, x, y, quadrant}; per-ghost-cell rows {core 7-tuple, depth, x, y, quadrant}; pole vocabulary. **Quadrant = sign pair of (x, y) under the established region names EN / ES / WN / WS.** Full 7.5MB atlas JSON is NOT shipped to the client.

**Default pivot hierarchy:**

```
Axis-X (WEST | EAST)
└─ Axis-Y (NORTH | SOUTH)        ← combined ⇒ the four quadrants
   └─ Kits | Ghosts
      ├─ Kits → Live Kits | Graveyard
      │        └─ Live Kits → Condensations | Single
      └─ Ghosts → the 7 core axes as pivot levels (default order = emitted core_order;
                  leaf = feasible cell row w/ depth; progressive disclosure only —
                  never a flat 11,160-row render; virtualized)
```

**Drag-to-reorder pivot levels** — any level may move above/below others (Matt's case: Condensations above the axis levels ⇒ condensation groups spanning all quadrants). Leaf rows: kit rows (kit_id + class + condensation) / ghost cell rows (tuple + depth).

**Selection wiring (bidirectional):** chart mark click → table drills open the path to that kit and scrolls to its row; table row click → chart applies the slim halo to that mark and scrolls/pans it into view. Single selected-kit at a time; independent of §4 class toggles.

## 6. Page composition + PRD

- **Black copy LEADS** the atlas page — selected by CANVAS (dark), which in galadriel's file naming is the **`archive`** skin (naming correction, §4); the white (`instrument`) skin sits behind the existing toggle. render-provenance.json carries an explicit skin→canvas mapping so drax's wiring cannot invert. Edition-I stays as the archived second lens per current page structure.
- Provenance JSON carries render commit + data commit + P-DF-1 verdict (existing law) + interactive-data build hash.
- PRD ship of this package: pre-authorized (Matt 2026-07-15). Collab-repo push remains separately Matt-gated.

## 7. Acceptance additions (r7 + page)

29. **restyle-regression:** all mark coordinates/geometry byte-frozen vs Edition-II baseline render; only fills/strokes/text-layout/hooks re-baselined (whitelist enumerated in r7 cut).
30. **overlap-zero:** no text-block bbox intersects another text block or the plot rect, both skins; content-locked strings verbatim.
31. **hooks-integrity:** hook counts reconcile with emitted counts (506 points classed; ghost glyph count matches aggregation); hook values grep-match emitted fields; doctored-input (a hook value absent from atlas-edition2.json) → HALT.
32. **legend-highlight:** all four classes toggle; halo ≤ 0.75px; zero fill mutations; multi-select works.
33. **pivot-conformance:** default hierarchy as §5; drag-reorder incl. the condensations-above-axes case; ghost branch virtualized; build-fail guard demonstrably fires on a doctored field rename.
34. **wiring-roundtrip:** chart→table drill+scroll and table→chart halo+pan, demonstrated on one live kit, one condensation member, one graveyard kit.
35. **black-lead:** instrument skin default at PRD; skin toggle preserved; anti-stale greps carry.

36.–40. **v1 zoom** — §8.5 (zoom-bounds-derived · halo-screen-constancy · gesture-perf · state-independence · clip-tracks-view).

---

## 8. v1 Zoom — viewBox lens on the inlined artifact (Matt 2026-07-15, two-bound ruling)

**Authority:** Matt 2026-07-15 — *"max zoom out would allow view of the full horizon-line and max zoom in would allow ease of selection for a single kit/ghost."* Page-level capability, drax seam. **Zero renderer changes** — gandalf probes (same date, r7 archive SVG + e21 render script) establish both preconditions in the shipped artifact:

- The charted-horizon polyline is emitted from the **FULL world hull** (24 projected points incl. closing; px bbox **x[43.1, 1725.5] × y[−1.7, 1363.3]** — exceeds the frozen frame on ALL FOUR edges; it is the SVG's only dashed polyline, dasharray `7 5`), with `planeClip` trimming at paint time only.
- Beyond-frame glyphs are **emitted-and-masked, never dropped** (render law line ~514: "CLIPPED … never dropped"; e21 counts `ghost_clipped` 27 + `sub_clipped` 1,130). Everything zoom-out reveals already sits in the DOM behind `planeClip`.

**Sequencing:** fires as a **discrete pass AFTER the §§3–7 wiring pass verifies** (single-variable discipline; NOT folded into the in-flight wiring brief). Ships preview-first → gandalf verify → promotion, per standing discipline.

### 8.1 Interaction grammar

Wheel (cursor-anchored) · pinch · drag-pan · **+/− buttons** (×1.5 steps) · double-click zoom-in step at cursor · **reset** · keyboard `+`/`−`/`0`. Continuous scale S clamped to **[S_min, S_max]** (§8.2). Implementation: viewBox arithmetic on the inlined `<svg>`; hand-rolled or `svg-pan-zoom` (tiny) at drax's option — **no d3-class dependency** for ~200 lines of window math.

### 8.2 The two bounds — derived from the mounted artifact, never hardcoded

The page derives both bounds from the inlined SVG DOM at mount (the artifact of record — §4c never-invent extended to page constants: copy the artifact, don't restate it). Exactly ONE design constant is named: **TARGET_D = 24 screen px**, the comfortable pointer-target diameter.

- **S_min (zoom-out floor) = Matt's full-horizon view.** Aspect-fit scale of union(canvas 0,0–1600,1200 ∪ hull-polyline px bbox) + 24px margin. Reference on Edition-II r7: union x[0, 1725.5] × y[−1.7, 1363.3] ⇒ **S_min ≈ 0.85×**. Acceptance meaning: at S_min every hull point is in-viewport — **the dashed line closes on screen.**
- **S_max (zoom-in ceiling) = Matt's single-mark selection ease.** `S_max = TARGET_D / (2 · r_min_selectable)`, where r_min_selectable = min radius among **selection-wirable** marks only — `[data-kit]` circles + `[data-core]` meso ghosts. Drill-in glyphs are EXCLUDED (unwirable, §5 ruled seam B — the 1.37px drill floor does not drag the ceiling). Reference: min meso-ghost r = **1.45px** ⇒ **S_max ≈ 8.3×** (min selectable mark renders ≈ TARGET_D; kit points at r=3 render ≈ 50px).

### 8.3 Clip-tracks-view (one rule, all states)

While any zoom/pan state is active, the page sets the `planeClip` rect to the current viewBox; **reset restores the emitted rect verbatim.** Consequences: zoom-out reveals the full charted horizon + the 27/1,130 masked marks ("looking past the map edge"); panning to the frame edge zoomed-in reveals the same, honestly; chrome paints above throughout (paint order unchanged — beyond-frame marks pass UNDER the r7 axis rails). Wrapper background = canvas hex from provenance `skin_canvas_map`, so the exposed surround blends seamlessly. This is runtime DOM state in the same law-class as §4's injected CSS — **the vendored SVG bytes are untouched at rest.**

### 8.4 Composition with standing law

- **Halo screen-constancy:** the injected halo CSS adds `vector-effect: non-scaling-stroke` — the ≤0.75px halo law is a SCREEN-perceptual cap ("almost non-existent") and must hold at 8× exactly as at 1×. Stroke-only law carries; zero fill mutation; zero dimming. (Marks carry no native strokes — fills are group-inherited — so the vector-effect touches halos only.)
- **Gesture perf (46.5k marks):** CSS transform on the wrapper DURING the gesture (compositor-only), a single viewBox write + clip update on gesture-settle; wheel rAF-throttled. No per-frame viewBox writes.
- **Table→chart pan** (§5 wiring) upgrades from scrollIntoView to **lens-pan**: center the mark at current S; if its rendered diameter < TARGET_D/2, raise S to that mark's ease-scale (≤ S_max). Deterministic.
- **Chrome under zoom = v1 option-1** (whole-SVG lens; chrome slides off-view when deep in the plane, returns on reset). Fixed-chrome zoom is r8 territory (needs zoom-cooperative rails from galadriel) — out of v1 scope by design.
- Selection + legend toggles are zoom-independent state; **skin flip preserves the lens.**

### 8.5 Acceptance additions

36. **zoom-bounds-derived:** S_min shows all hull points + full canvas in-viewport; S_max renders the min selectable mark ≥ TARGET_D; both bounds provably derived from the mounted artifact (a doctored-radius probe shifts S_max with zero code change).
37. **halo-screen-constancy:** halo ≤ 0.75 SCREEN px at S_min / 1× / S_max; stroke-only; zero fill mutation; zero dimming.
38. **gesture-perf:** transform-during-gesture + settle-write demonstrated on the full 46.5k-mark artifact; no continuous viewBox writes.
39. **state-independence:** legend + selection survive zoom/pan; skin flip preserves the lens; reset restores the emitted viewBox AND the emitted planeClip rect verbatim.
40. **clip-tracks-view:** beyond-frame marks + the closed horizon visible whenever the view exceeds the plane rect; the on-disk SVG byte-untouched (checksum before/after a zoom session).

---

## 9. D1 defect pass — legend band + highlight-cost law + pivot memoization (Matt 2026-07-15, live-page defects)

**Authority:** Matt 2026-07-15 — "the legend on the top-left is covering the title" + "the pivot table makes the page run very slowly, stutter and even time out… I am ok with changing the pivot features." **Gandalf diagnosis (from the shipped `cd7f387` bytes):** (1) the Ghosts legend class per-mark halos 46,006 circles and every selection change swaps the injected `<style>`, forcing style-recalc across the 46.5k-node SVG — the stutter/freeze; (2) pivot grouping is lazy but UNCACHED — every render re-walks the 11,666-item array per expanded node; (3) the legend is absolutely positioned inside the chart stage over the SVG banner. **Design ruling: no pivot-feature cuts** — the §4 per-mark-halo law was a gandalf misjudgment at ground-class scale; the fix is better design, not less feature.

**Sequencing:** fires AFTER the in-flight v1 zoom pass returns + verifies (same files; single-variable). Re-profiles WITH zoom present.

- **D1-a Legend band.** The legend moves OUT of the chart stage into a normal-flow band between the page header and the chart, top-left aligned. It never overlays the SVG canvas at any viewport width. (§4's "top-left" is satisfied at page level.) **Same-class check for the zoom controls (the §8 pass placed them `absolute right-3 top-3`):** they remain chart-affixed (zoom chrome belongs on the chart — map/dashboard convention), but if they overlap banner chrome at any tested width, drop their vertical offset below the banner strip.
- **D1-b Highlight-cost law (amends §4).** Class-highlight cost must scale with CLASS SIZE, never with artifact size:
  - Per-mark stroke halos remain ONLY for classes ≤ ~600 marks (live singles 383, condensations 86, graveyard 37) and for the single-selection halo (1). Unchanged visual law: stroke-only ≤ 0.75px, zero fill mutation, zero dimming.
  - **Ground classes (Ghosts = meso + drill-in, 46k) highlight by LAYER GROUP** — one compositor-level emphasis on `#layer-ghosts, #layer-drillin` (e.g., `filter: brightness(~1.3) saturate(~1.2)` tuned per canvas; galadriel's terrainBlur already proves layer-level filters on this artifact). One selector, one composited surface, no 46k per-element strokes. Design meaning: the ground WAKES AS GROUND — legible emphasis, no rim-mush.
  - Injected-CSS churn: the `<style>` text changes only when legend/selection state changes (semantically necessary); each change must now be O(class) to recalc.
- **D1-c Pivot memoization law.** Group-children computation cached per (level-order, node-path) — cache invalidated only on reorder/data change; leaf-index lookup maps memoized per items array (kills per-selection findIndex sweeps); `React.memo` on leaf/group rows; virtualizer scroll state rAF-throttled; CSS containment (`contain: layout style`) on the table region so table renders never invalidate the SVG region's style scope.
- **D1-d Perf budgets (acceptance, profiled receipts before/after on the prod build):** any legend toggle INCLUDING Ghosts ≤ 50ms main-thread block, visual settle ≤ 150ms; any selection change ≤ 50ms script+style; table scroll ≥ 50fps sustained (no frame > 32ms over 3s); route interactive < 1.5s; zero long-tasks > 200ms after mount through a full #34 roundtrip.
- **Fallback ladder (fires ONLY if D1-b/c still miss budgets; Matt's feature-latitude spent in this order):** (1) ghost leaf-list pagination ("show next 500") inside virtualized nodes → (2) ghost core-axis pivot flattened to a filter-chip list. Kit-side features and bidirectional wiring are never on the ladder.
- **D1-e Axis-pole vocabulary in the pivot (Matt 2026-07-15 second message).** The pivot's compass group labels change to the ACTUAL pole names. Mapping (artifact ground truth = the r7 rails, NOT the `axis_names` strings, which carry no sign convention): **EAST (x≥0) = PERFORM** (right rail) · **WEST = DEPLOY** (left rail) · **NORTH (world y≥0) = LAUNCH** (top strip; screen-y is inverted) · **SOUTH = EMBODY** (bottom pocket). Group labels render the pole name in the chart's case (UPPER) with a muted single-letter compass gloss (e.g., `PERFORM · E`) so the leaf rows' quadrant codes (EN/ES/WN/WS) stay legible; level labels become `Axis-X (DEPLOY | PERFORM)` / `Axis-Y (LAUNCH | EMBODY)`. **Inversion guard (the skin-bug class):** a unit test derives the expected sign→pole mapping FROM the vendored SVG (right-rail text ⇒ positive-x pole; top-strip text ⇒ positive-y pole) and asserts the pivot's mapping against it — never trust a hand-typed constant alone.
- **D1-f Fluid page width (Matt 2026-07-15 second message).** The atlas route's container cap (`max-w-6xl` = 1152px) is REMOVED — the page goes fluid to the browser window at every resolution, with 16–24px gutters. Chart stage scales to container width (viewBox-driven; aspect preserved); legend band, pivot table, selection summary, and provenance panel span the same fluid width. Scope: the atlas route only — other Glance routes keep their own layout.
- **D1-g Ghost core axes become COLUMNS, not pivot levels (Matt 2026-07-15 third message).** The 7 `ghost:<axis>` levels leave the default pivot hierarchy AND the drag-chip list; the default levels become the five structural ones (axis-x → axis-y → entity → kit-liveness → kit-condensation). Ghost leaf rows render in the virtualized grid with **seven core-axis columns** (movement · delivery · treatment · function · proxy · activation · dependency — `core_order` verbatim) + the existing depth / lit / kit_count. Build (kit) leaf rows share the grid; the seven axis columns show `—` for builds — per-kit single-valued core codes DO NOT EXIST in the emitted data (kit axis coding upstream is multi-valued curation; never invent a single value). **Vocabulary correction for the record:** the semantic axes number SEVEN (the core tuple); the "14" on the provenance panel is `retained_dims` — the frozen SVD basis dimensionality, not per-row data. Perf note: dropping seven ghost pivot levels erases most deep-tree grouping cost for the 11,160-row branch — composes with D1-c.
- **D1-h Build provenance names (Matt 2026-07-15 third message).** Build leaf rows (live + graveyard + family members) display `folk_name — game year (patch)` instead of the kit_id slug: e.g. `Arrow Storm Warden — Chronicon 2020`. Data path: a **one-shot read-only sidecar** exported from `research/curated/corpus.db` `canon_corpus` (columns: kit_id, folk_name, game, era_year, stabilization_patch) → vendored as a build input in the loadout repo (provenance header: source DB path + exact query + export date) → joined on kit_id by the slim-builder. The FROZEN `atlas-edition2.json` is untouched; no re-render. Coverage receipts (2026-07-15 probe): folk_name 606/606, game 606/606, era_year 486/606 (~80% — rows without a year show name — game only), stabilization_patch **17/606** (shown only where curated; the patch back-fill is an elrond curation-queue item, NOT a D1 blocker). Zero invention: every displayed string is a copy of a corpus field; missing fields render nothing, never a guess.
- **D1-i Community vocabulary — "builds" / "build families" (Matt 2026-07-15 third message: "We will think of them internally as kits, but to the community they are builds").** ALL user-visible page strings on the atlas route swap: kit(s) → **build(s)**; condensation(s) → **build family / build families** (group prefix `Condensation: X` → `Family: X`; page title `Kit Atlas` → `Build Atlas` (interim — superseded by the §9.2 naming ruling: D2-d swaps to **`Build Horizon`**); legend `Live Kits` → `Live Builds`, `Condensations` → `Build Families`; pivot level labels + hints + selection captions accordingly). **Internal identifiers are UNTOUCHED** — `kit_id`, `data-kit`, TypeScript types, emitted field names, test ids all stay kits (Matt's internal/community split, verbatim). Machine-verbatim provenance receipt strings (emitted keys like `counts.active`) stay technical; human-readable labels around them use community vocabulary. **Known interim seam:** the vendored SVG plate bakes ONE visible `CONDENSATIONS` ledger heading (+1 lowercase) — accepted for this pass; an **E2.2 plate-vocabulary relabel** (galadriel, presentation-only on frozen geometry) is registered as the follow-up.

### 9.1 Acceptance additions

41. **legend-band:** legend bbox ∩ SVG canvas bbox = ∅ at 360/768/1280/1920px widths; banner headline fully visible.
42. **highlight-cost:** Ghosts toggle produces ZERO per-mark stroke rules; per-mark rules exist only for ≤600-mark classes + selection; budgets D1-d met with profiler receipts.
43. **pivot-memo:** re-render of the expanded tree performs zero re-grouping (cache hits proven by counter in dev instrumentation, stripped or gated in prod); reorder invalidates correctly (drag case still exact).
44. **no-regression:** acceptance 32/34/35 receipts re-demonstrated post-fix; 36–40 (zoom) unaffected; all tests green.
45. **axis-pole-vocabulary:** pivot group labels show DEPLOY/PERFORM/LAUNCH/EMBODY per the D1-e mapping; the SVG-derived inversion-guard test passes (and fails on a deliberately flipped mapping); quadrant codes in leaf rows unchanged.
46. **fluid-width:** at 1440/1920/2560px viewports the atlas container width = viewport minus gutters (no fixed cap); chart + table + bands span it; no horizontal scrollbar at any tested width.
47. **ghost-axes-as-columns:** default pivot levels are exactly the five structural ones; `ghost:*` levels absent from the drag-chip list; ghost leaf rows show all 7 core-axis columns whose values match the emitted core tuple (spot-check ≥5 rows against `atlas-interactive.json`); build rows show `—` in axis columns.
48. **build-provenance-names:** build leaf rows show `folk_name — game year (patch)`; exact coverage on the atlas 506 reported in the return (folk_name expected 506/506; year ~80%; patch only where curated); sidecar file carries the provenance header; zero invented strings (audit: every displayed name/year/patch traces to a corpus row).
49. **community-vocabulary:** case-insensitive DOM text audit of the atlas route finds zero user-visible `kit(s)` / `condensation(s)` strings EXCEPT (a) the baked SVG plate text (interim, E2.2 registered) and (b) machine-verbatim provenance receipt keys; internal identifiers (data-kit, kit_id, types, tests) unchanged.

---

## 9.2 D2 extension pass — the FULL 14-axis columns for builds (Matt 2026-07-15 fourth message)

**Authority:** Matt 2026-07-15 — "there are 7 axes for ghosts and 14 for live kits/builds, right? If so, then we need the 14 for the kits/builds." **VERIFIED CORRECT** (gandalf probe, same date): `canon_engine_key.cell_key` is `kit_id` + a **14-part coordinate** (sample: `d2-wl-fire|walk|at-target|var|ground_targeted_circle|damage|none|mitigate|unknown|solo|ranged|med|instant|active|one-shot`); per-axis engine-key coverage 534–610 of 618 rows; the MCA loadings' coordinate families (geometry, economy, defense, amp, commit, range … beyond the meso 7) and the exact-lattice raw 990,186,120 (vs meso raw 12,474) corroborate. **This SUPERSEDES D1-g's "builds show `—` in axis columns" ruling** — that ruling was scoped to the emitted atlas JSON, which was the wrong surface; the corpus/engine-key IS the kit-grain coding surface.

**Sequencing:** fires AFTER the D1 pass returns + verifies (same grid/pivot files; single-variable). D1's `—` state is a known-interim, not a defect.

- **D2-a Sidecar widens to the 14-axis key.** The D1-h sidecar export extends: `canon_engine_key.cell_key` (split into named parts) + the engine-key named columns as label truth (`geometry_value`, `ctrl_treatment`, `ctrl_function`, `delivery_value`, `activation_val`, `dependency_val`, `economy_model`, `def_bin`, plus `canon_corpus` `attr_val/range_val/tempo_val/amp_val/proxy_val/commit_val`). **The 14 axis NAMES + part-order must be DERIVED from the engine-key schema and/or the emitter (`research/scripts/build_atlas_json_edition2.py`) with a receipt — never hand-typed without one** (same inversion-guard discipline as D1-e).
- **D2-b Union-grid column law.** Leaf-grid axis columns = UNION of the ghost meso-7 and the build 14. An axis SHARES a column iff the name matches at both grains (movement, treatment, function, proxy, activation, dependency are the expected shared six); vocabulary-distinct axes are NOT merged without an emitter-proven mapping (kit-grain `geometry` ≠ meso `delivery` unless the emitter's kit→meso mapping proves the collapse). Meso-only columns (delivery) populate for builds ONLY via the emitter's kit→meso cell mapping where the kit is mapped (the 108 `unmapped_pending_curation` kits show `—` there). Kit-only axes show `—` on ghost rows. `unknown` is a CURATED VALUE and renders literally — distinct from missing (`—`).
- **D2-c Presentation.** Axis columns grouped: shared six first, then meso-only, then kit-only; header tooltips name axis + grain. Horizontal scroll INSIDE the table region permitted at narrow widths (the fluid page never scrolls horizontally — acceptance 46 holds). Virtualization holds ≥50fps with the wider rows.

### Acceptance additions (D2)

50. **build-14-axis-columns:** ≥5 spot-checked build rows show axis codes matching their `cell_key` verbatim; per-axis coverage on the atlas 506 reported in the return.
51. **shared-column honesty:** no column mixes grain vocabularies without a named receipt (the emitter line/table proving the mapping); the axis-name/part-order derivation receipt included.
52. **no-regression:** 41–49 re-demonstrated (spot), all tests green, budgets D1-d still met with the wider grid.

**Naming ruling (Matt 2026-07-15 fifth message → RULED same session): the community-facing display name is "Build Horizon."** ("I like Build Horizon. It's very clear and descriptive.") Chosen to avoid the PoE "Atlas of Worlds" collision; ties to the plate's ratified CHARTED HORIZON vocabulary and the artifact's `beyond_horizon` provenance fields. **D2-d (this pass):** page title string `Build Atlas` → `Build Horizon` (one-string swap; D1-i's title was interim). Internals (`atlas*` files, types, JSON, routes, ids) stay `atlas` per the internal/community split. The vendored plate's baked heading adopts "Build Horizon" in the registered E2.2 relabel (galadriel).

53. **display-name:** page title reads **Build Horizon**; zero occurrences of user-visible "Atlas" as the surface's name on the route (machine-verbatim provenance receipt strings exempt); internals still `atlas*` (spot-check `data-kit`, route path, file names unchanged).

---

## 9.3 D3 UX pass — simple filters replace pivots · fixed zoom at derived S_max (Matt 2026-07-15 sixth message)

**Authority (verbatim):** *"can you please change the pivots to simple filters? The table looks nice but the pivots are getting in the way."* + *"we should remove the zoom function and just have the zoom auto-set to the max zoom parameter available now. I like that zoom ratio, but the zoom functionality is awkward on the browser and the screen square doesn't work right, so just adjust to that level of zoom."*

**Sequencing:** fires AFTER D2 verify + promotion (both done — PRD serves D2). Same files; single-variable UX pass. PREVIEW only; promotion by alias after gandalf verify, per standing law.

**This pass SUPERSEDES:** §5's hierarchical-pivot interaction model (drag-reorder levels, progressive-disclosure tree, condensations-above-axes) and §8's v1 zoom interaction grammar (wheel/pinch/double-click zoom, drag-pan, ±/reset controls, clip-tracks-view runtime mutation). **This ruling is the spec-supersession authority for retiring their interaction tests.** What it does NOT touch: the D2 union leaf grid (Matt: "the table looks nice" — grouped header, grain tints, shared-5/meso-2/kit-9 law, `unknown` vs `—`, tooltips all stand verbatim), the legend + class-highlight CSS, selection summary, provenance panel, skin toggle, chart↔table wiring intent, and §8.2's BOUND DERIVATION (S_max stays load-bearing — see D3-b).

- **D3-a Filters replace pivots.** The pivot apparatus retires from the page: `PivotLevelBar` (drag-reorder), the `PivotBranch`/`PivotRow` expansion tree, `buildDefaultLevels`/`PivotGrouper` grouping engine, Reset order / Collapse all. In its place: a **filter bar** — one simple control per STRUCTURAL dimension, exactly the five that were pivot levels:
  1. **Axis-X pole** — All | `DEPLOY · W` | `PERFORM · E` (predicate: x sign; labels from the inversion-guarded `AXIS_POLES`, never retyped)
  2. **Axis-Y pole** — All | `LAUNCH · N` | `EMBODY · S` (world-y sign; screen-y inversion already baked into emitted y)
  3. **Entity** — All | Builds | Ghosts
  4. **Liveness** — All | Live Builds | Graveyard
  5. **Family** — All | Single | one entry per distinct `condensation` value ENUMERATED FROM THE EMITTED ROWS (sorted; never a hand-typed list)
  **Composition law:** AND across controls; a row that a non-All filter does not apply to FAILS that filter (picking Graveyard shows graveyard builds only — ghosts drop; picking a Family shows that live family only). Default = All on every control. A result-count readout updates live (`N builds · M ghost cells shown`), and the zero-result state is HONEST: an empty-state line + one-click **Clear filters** (no fake rows, no silent fallback).
  **The body becomes ONE flat table:** the SAME D2 union grid (LeafGridHeader + LeafRow + VirtualizedLeafList, untouched cell semantics) over the filtered items — builds first, then ghosts, each in emitted order (no invented ranking). The table heading drops the word "pivot" (community vocab: builds/ghost cells; exact string drax latitude). Dead grouping code + its tests are REMOVED with an in-repo supersession note citing this section (do not leave the engine orphaned); `AXIS_POLES`/`pivotPoleMapping` + the inversion guard + `buildProvenanceName`/`leafKey`/column model all SURVIVE (filters + grid consume them).
- **D3-b Fixed zoom at the derived S_max; zoom UI removed.** All zoom interaction goes: `AtlasZoomControls`, wheel/pinch/double-click zoom, drag-pan gesture code, gesture-transform runtime, reset, and the clip-tracks-view runtime mutation (the "screen square" behavior Matt flagged). The chart mounts at a FIXED scale = **S_max, still DERIVED from the mounted artifact bytes at runtime** (`TARGET_D / (2 · r_min_selectable)` via `deriveBounds` on the fetched markup — §8.2's derivation law holds; **no hardcoded scale constant anywhere**; a doctored radius in the source shifts the mount scale with zero code change). At S_max every selection-wirable mark renders at ≥ TARGET_D by construction, so no ease-scale logic survives — table→chart becomes pan-only.
  **Navigation = NATIVE browser scrolling.** The inlined SVG renders at (stage width × S_max) inside a bounded-height, `overflow-auto` two-axis scroll stage (stage height ≈ viewport-proportioned; drax latitude; `overscroll-behavior: contain`). The SVG's emitted `viewBox` + `planeClip` serve **VERBATIM and are never mutated at runtime** (byte-equal in DOM to the vendored artifact — stronger than §8.3's reset-restores-verbatim). `touch-action` restored to normal so touch/trackpad scroll the stage natively. Initial scroll position = plane-rect center. Highlight CSS + click delegation are unchanged (same inlined DOM, same hooks).
  **Wiring under the new model:** table→chart row click = selection halo + `scrollTo` arithmetic centering the mark (canvas coords → rendered px; pure, testable). Chart→table mark click = selection + reveal the row in the flat table — **if the item fails the active filters, the filters RESET to All (deterministic), then scroll** (no silent non-reveal).

### Acceptance additions (D3)

54. **filters-replace-pivots:** level bar / drag-reorder / expansion tree GONE; five filter controls render with values enumerated from emitted data only (pole labels === `AXIS_POLES` receipts; Family options === distinct emitted `condensation` values + Single); AND composition demonstrated (≥3 combined-filter spot checks with hand-counted expected Ns); zero-result state + Clear filters demonstrated.
55. **flat-table-keeps-D2-grid:** the filtered body is the SAME D2 union grid (shared-5/meso-2/kit-9 columns, grain tints, tooltips, `unknown` vs `—`) — acceptance 50–52 spot re-demonstrated on the flat surface; virtualization holds with All/All (11,666 rows) at ≥50fps.
56. **wiring-survives:** table→chart click halos + centers the mark at fixed S; chart→table click reveals + scrolls the row, resetting filters to All first iff the item was filtered out; selection ring + aggregate-cells caption unchanged.
57. **fixed-zoom-at-S_max:** zero zoom UI on the page (controls, wheel/pinch/dblclick zoom, drag-pan, reset); mount scale receipt in the return shows S_max derived at runtime from the artifact (`r_min_selectable` + formula), no scale literal in source; initial position = plane center.
58. **native-scroll + verbatim-artifact:** the stage scrolls natively on both axes (wheel, trackpad, touch); DOM `viewBox` + `planeClip` byte-equal to the vendored SVG at all times (no runtime mutation); highlight + click delegation function while scrolled.
59. **test-supersession + no-regression:** lens-INTERACTION + pivot-GROUPING tests retired citing §9.3 (this Matt ruling); bound-DERIVATION tests (`parseViewBox`/`parsePlaneClipRect`/`parseHullBbox`/`minSelectableRadius`/`deriveBounds`/S_max formula) + axis-inversion guard + sidecar-join + community-vocabulary + highlight tests KEPT green; full suite green; D1-d budgets hold (scroll-fps on the ~8× surface reported).

---

## 9.4 D4 correction pass — chart mounts at the FULL-HORIZON FIT, not S_max (Matt 2026-07-15 seventh message)

**Authority (verbatim):** *"The table is PERFECT! The Atlas chart is completely wrong. Instead of setting the atlas zoom to just barely encompass all of the horizon, it's super-zoomed into a small set of ghost cells."*

**Correction of record (gandalf misread, owned):** D3-b mapped Matt's "max zoom parameter available" to **S_max** (the zoom-IN ceiling). Matt meant the zoom-OUT limit — the view that *just barely encompasses all of the horizon* = the **fit view** (the old S_min bound: `union(canvas ∪ hull-bbox) + FIT_MARGIN`, aspect-pinned). D3-b's fixed-S_max stage + scroll-navigation model is **SUPERSEDED by this section.** **D3-a (filters + flat table) is Matt-RATIFIED ("PERFECT") and MUST NOT be touched** — zero diffs to `AtlasBuildTable.tsx`, the filter model, or the column model.

- **D4-a The chart is a STATIC full-horizon map.** At markup inline (initial mount AND each skin flip), set the SVG `viewBox` **and** the `planeClip` rect **ONCE** to the DERIVED fit box — computed from the mounted artifact bytes via the EXISTING pure derivation (`parseViewBox` + `parseHullBbox` + `unionBbox` + `padBbox(FIT_MARGIN)`, aspect-pinned to native 4:3, centered on the union — exactly the old lens's S_min view). No literals anywhere; a doctored hull in the source shifts the mount box with zero code change. Static thereafter: no zoom, no pan, no scroll interaction of any kind (zoom UI already gone per D3-b — that half of D3-b stands).
- **D4-b Stage model reverts to page flow.** The bounded-height `overflow-auto` scroll stage is REMOVED — back to `w-full h-auto` block flow (the whole horizon is visible at fluid width; height follows the fit-box aspect). `overscroll-behavior` + stage-scroll styles die. The hull dashes render FULLY VISIBLE, including their beyond-canvas extent (the planeClip mount-write is what reveals plane-layer content outside the emitted clip — same mechanism as the old lens's clip-tracks-view, applied once).
- **D4-c Verbatim-law amendment.** §9.3's "viewBox + planeClip serve VERBATIM, never mutated" is AMENDED by this ruling: **one mount-time configuration write to the derived fit box is lawful (it IS the ruled view); no interaction-driven mutation after mount.** In-file supersession note citing §9.4 where the old assertion lived (code comment + test).
- **D4-d Wiring on the map.** Chart→table unchanged (mark click → selection + reveal row, filter-reset-then-scroll law intact). Table→chart: row click halos the mark; if the chart region is scrolled out of the page viewport, `scrollIntoView` the CHART REGION (page-level; there is no stage scroll). Accepted consequence, named: at fit scale the smallest marks render below TARGET_D — the TABLE is the precision selection surface; the chart is the overview map with halo feedback. `useAtlasStage`'s scroll-navigation math (`centerScroll`, scroll-fraction resize logic) retires or repoints accordingly.

### Acceptance additions (D4)

60. **fixed-full-horizon-view:** chart mounts showing the ENTIRE horizon (hull dashes fully visible, incl. beyond-canvas extent); DOM `viewBox` + `planeClip` equal the DERIVED fit box (receipt: box numbers + the implied S_min value + the derivation call path); re-applied on skin flip; no scroll stage, no zoom UI, page flows `w-full h-auto`.
61. **table-untouched + wiring:** `git diff` shows ZERO changes to `AtlasBuildTable.tsx` / filter model / column model; both wiring directions demonstrated on the fit view (halo lands on the correct mark; filter-reset drill intact; table→chart brings the chart region into viewport when scrolled away).
62. **supersession + no-regression:** byte-verbatim assertions repointed to "mount-config box, static after mount" with §9.4 notes; retired/repointed tests listed; full suite green; budgets hold (page-interactive, long-tasks; no scroll-fps claim needed — nothing scrolls).

---

## 9.5 D5 — the SCREEN BOX resizes to the mount geometry (Matt 2026-07-15 eighth message)

**Authority (verbatim):** *"Ok the zoom is perfect, but the 'screen box' now needs to be resized to fit the current zoom."* The zoom (D4 fit mount) is RATIFIED; only the frame resizes.

**Defect (ground-truthed on PRD by gandalf playwright probe before this cut):** D4 wrote viewBox + planeClip to the fit box (`-79.2367 -25.74 1884.0133 1413.01`) but left TWO frame elements at the emitted canvas geometry:
1. **The canvas PLATE rect** — direct child of the svg, `x=0 y=0 w=1600 h=1200 fill=#0e1016`. The visible dark plate ends at the canvas edge while content renders past it on the page background (hull marks to x≈1725.5/y≈1363.3, pole-rail glosses, footer denominator strings — confirmed off-plate in the probe's corner crop). Asymmetric page-background bands sit inside the frame: left 79.24u · top 25.74u · right 204.78u · bottom 187.27u.
2. **The svg element's width/height presentation attrs** (`1600`/`1200`) — the inlined svg renders at fixed 1600×1200 CSS px regardless of container (probe: rendered bbox w=1600 at a 1440px viewport → horizontal page overflow).

- **D5-a Plate follows the mount box.** The §9.4 D4-a mount-time write EXTENDS to the canvas plate rect: same moment (initial mount + each skin flip), same derived fit box, x/y/w/h set alongside viewBox + planeClip. Identification is STRUCTURAL and fail-loud: *the direct-child `rect` of the svg whose width/height equal the parsed native canvas dims (already available as `bounds.native` from `deriveBounds`) and which carries a fill* — that is the plate. Zero candidates or >1 candidates → loud error (no guess, no fill-literal matching, no positional index). After the write: every mark/rail/dash/banner/footer sits ON the plate; plate edge == clip edge == frame edge — the screen box fits the current zoom.
- **D5-b The svg element sizes to its container.** In the same write-set, the inlined svg's `width`/`height` presentation attrs are removed (CSS `w-full h-auto` block flow + the viewBox's 4:3 aspect govern rendered size — D4-b's page-flow model, now actually responsive). No fixed-px rendering; no horizontal page overflow at ANY viewport width. The FROZEN source SVGs stay byte-untouched — all writes are DOM-side at mount, exactly D4's mechanism.
- **D5-c Law + tests.** §9.4 D4-c's "one mount-time configuration write" amends to **one mount-time configuration WRITE-SET** (viewBox · planeClip · plate rect · svg sizing) — still static after mount, still ZERO literals: the doctored-hull probe extends to the plate (enlarged hull vertex in the source → wider fit box → plate follows, zero code change). D3-a remains untouchable: zero diffs to `AtlasBuildTable.tsx` / filter model / column model.

### Acceptance additions (D5)

63. **plate==box:** DOM plate rect x/y/w/h == planeClip == viewBox == the derived fit box (receipt: the four attr sets + the structural-identification path); NO page-background band inside the frame; NO mark/rail/footer renders off-plate (corner-crop screenshot receipt); re-applied identically on skin flip.
64. **no-fixed-px:** svg width/height attrs absent after mount; rendered width tracks the container with 4:3 held (receipts at 1440 / 1280 / 375 — zero horizontal page overflow at every width); both frozen SVG sha256 UNCHANGED.
65. **supersession + no-regression:** §9.4 write-set comments/tests cite §9.5; doctored-hull probe extended to the plate; fail-loud plate-identification test present (ambiguous-candidate fixture RAISES); full suite green; table/filter/column files ABSENT from the diff; both wiring directions (halo + filter-reset drill + chart-region scrollIntoView) re-demonstrated on the resized frame.

---

## Cross-references

`2026-07-11-atlas-chart-renderer-spec.md` §§7–10 (render law; r7 amends presentation) · `atlas-edition2.json` ghost_field (core_order, drill_in, denominators) · tracker SESSION-DELTA -l (Edition-II audit) · Matt directive message 2026-07-15 (this package's authority).

Tracker-delta: new gap — r7 + interactive-page package specced, gated on Edition-II render verify → current-to-end-state-engine, SESSION-DELTA -m.

Tracker-delta (v1.1 zoom amendment): new gap — v1 zoom (§8) specced on Matt's two-bound ruling, build gated on wiring-pass verify → current-to-end-state-engine, SESSION-DELTA -q.

Tracker-delta (v1.2 D1 amendment): new gaps — D1 defect pass specced (D1-a…D1-i: legend band, highlight-cost law, pivot memoization, budgets, axis-pole vocab, fluid width, ghost-axes-as-columns, build provenance names w/ corpus sidecar, community vocabulary builds/build-families) + two registered follow-ups (E2.2 plate-vocabulary relabel — galadriel; stabilization_patch back-fill 17/606 — elrond curation queue) → current-to-end-state-engine, SESSION-DELTA -s.

Tracker-delta (naming ruling): closed decision — community-facing surface name RULED "Build Horizon" (Matt 2026-07-15); D2-d one-string title swap + E2.2 plate adoption → current-to-end-state-engine, SESSION-DELTA -s addendum.

Tracker-delta (v1.4 D3 amendment): new gap — D3 UX pass specced on Matt's pivots→filters + fixed-zoom rulings (§9.3; supersedes §5 pivot interaction + §8 zoom grammar; D2 grid untouched), build fired to drax, PREVIEW-gated → current-to-end-state-engine, SESSION-DELTA -w.

---

**Signed:** gandalf (SPEC-AUTHOR / SCENEWRIGHT)
**For:** the atlas chart's first interactive product surface — four-class legibility, honest ground/figure separation, and a pivot table that lets Matt walk the lattice.
