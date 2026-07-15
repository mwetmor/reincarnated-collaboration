# Atlas interactive Glance package — r7 restyle + semantic hooks + interactive page (spec)

**Date:** 2026-07-15
**Author:** gandalf (SPEC-AUTHOR / SCENEWRIGHT)
**Status:** v1.1 — cut on Matt's directive package 2026-07-15 ("When Drax moves it to PRD…" + three functional effects). One marked veto point (§1). **§8 v1-zoom amendment added same date on Matt's two-bound ruling.**
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

- **D1-a Legend band.** The legend moves OUT of the chart stage into a normal-flow band between the page header and the chart, top-left aligned. It never overlays the SVG canvas at any viewport width. (§4's "top-left" is satisfied at page level.)
- **D1-b Highlight-cost law (amends §4).** Class-highlight cost must scale with CLASS SIZE, never with artifact size:
  - Per-mark stroke halos remain ONLY for classes ≤ ~600 marks (live singles 383, condensations 86, graveyard 37) and for the single-selection halo (1). Unchanged visual law: stroke-only ≤ 0.75px, zero fill mutation, zero dimming.
  - **Ground classes (Ghosts = meso + drill-in, 46k) highlight by LAYER GROUP** — one compositor-level emphasis on `#layer-ghosts, #layer-drillin` (e.g., `filter: brightness(~1.3) saturate(~1.2)` tuned per canvas; galadriel's terrainBlur already proves layer-level filters on this artifact). One selector, one composited surface, no 46k per-element strokes. Design meaning: the ground WAKES AS GROUND — legible emphasis, no rim-mush.
  - Injected-CSS churn: the `<style>` text changes only when legend/selection state changes (semantically necessary); each change must now be O(class) to recalc.
- **D1-c Pivot memoization law.** Group-children computation cached per (level-order, node-path) — cache invalidated only on reorder/data change; leaf-index lookup maps memoized per items array (kills per-selection findIndex sweeps); `React.memo` on leaf/group rows; virtualizer scroll state rAF-throttled; CSS containment (`contain: layout style`) on the table region so table renders never invalidate the SVG region's style scope.
- **D1-d Perf budgets (acceptance, profiled receipts before/after on the prod build):** any legend toggle INCLUDING Ghosts ≤ 50ms main-thread block, visual settle ≤ 150ms; any selection change ≤ 50ms script+style; table scroll ≥ 50fps sustained (no frame > 32ms over 3s); route interactive < 1.5s; zero long-tasks > 200ms after mount through a full #34 roundtrip.
- **Fallback ladder (fires ONLY if D1-b/c still miss budgets; Matt's feature-latitude spent in this order):** (1) ghost leaf-list pagination ("show next 500") inside virtualized nodes → (2) ghost core-axis pivot flattened to a filter-chip list. Kit-side features and bidirectional wiring are never on the ladder.
- **D1-e Axis-pole vocabulary in the pivot (Matt 2026-07-15 second message).** The pivot's compass group labels change to the ACTUAL pole names. Mapping (artifact ground truth = the r7 rails, NOT the `axis_names` strings, which carry no sign convention): **EAST (x≥0) = PERFORM** (right rail) · **WEST = DEPLOY** (left rail) · **NORTH (world y≥0) = LAUNCH** (top strip; screen-y is inverted) · **SOUTH = EMBODY** (bottom pocket). Group labels render the pole name in the chart's case (UPPER) with a muted single-letter compass gloss (e.g., `PERFORM · E`) so the leaf rows' quadrant codes (EN/ES/WN/WS) stay legible; level labels become `Axis-X (DEPLOY | PERFORM)` / `Axis-Y (LAUNCH | EMBODY)`. **Inversion guard (the skin-bug class):** a unit test derives the expected sign→pole mapping FROM the vendored SVG (right-rail text ⇒ positive-x pole; top-strip text ⇒ positive-y pole) and asserts the pivot's mapping against it — never trust a hand-typed constant alone.
- **D1-f Fluid page width (Matt 2026-07-15 second message).** The atlas route's container cap (`max-w-6xl` = 1152px) is REMOVED — the page goes fluid to the browser window at every resolution, with 16–24px gutters. Chart stage scales to container width (viewBox-driven; aspect preserved); legend band, pivot table, selection summary, and provenance panel span the same fluid width. Scope: the atlas route only — other Glance routes keep their own layout.

### 9.1 Acceptance additions

41. **legend-band:** legend bbox ∩ SVG canvas bbox = ∅ at 360/768/1280/1920px widths; banner headline fully visible.
42. **highlight-cost:** Ghosts toggle produces ZERO per-mark stroke rules; per-mark rules exist only for ≤600-mark classes + selection; budgets D1-d met with profiler receipts.
43. **pivot-memo:** re-render of the expanded tree performs zero re-grouping (cache hits proven by counter in dev instrumentation, stripped or gated in prod); reorder invalidates correctly (drag case still exact).
44. **no-regression:** acceptance 32/34/35 receipts re-demonstrated post-fix; 36–40 (zoom) unaffected; all tests green.
45. **axis-pole-vocabulary:** pivot group labels show DEPLOY/PERFORM/LAUNCH/EMBODY per the D1-e mapping; the SVG-derived inversion-guard test passes (and fails on a deliberately flipped mapping); quadrant codes in leaf rows unchanged.
46. **fluid-width:** at 1440/1920/2560px viewports the atlas container width = viewport minus gutters (no fixed cap); chart + table + bands span it; no horizontal scrollbar at any tested width.

---

## Cross-references

`2026-07-11-atlas-chart-renderer-spec.md` §§7–10 (render law; r7 amends presentation) · `atlas-edition2.json` ghost_field (core_order, drill_in, denominators) · tracker SESSION-DELTA -l (Edition-II audit) · Matt directive message 2026-07-15 (this package's authority).

Tracker-delta: new gap — r7 + interactive-page package specced, gated on Edition-II render verify → current-to-end-state-engine, SESSION-DELTA -m.

Tracker-delta (v1.1 zoom amendment): new gap — v1 zoom (§8) specced on Matt's two-bound ruling, build gated on wiring-pass verify → current-to-end-state-engine, SESSION-DELTA -q.

---

**Signed:** gandalf (SPEC-AUTHOR / SCENEWRIGHT)
**For:** the atlas chart's first interactive product surface — four-class legibility, honest ground/figure separation, and a pivot table that lets Matt walk the lattice.
