# Atlas interactive Glance package — r7 restyle + semantic hooks + interactive page (spec)

**Date:** 2026-07-15
**Author:** gandalf (SPEC-AUTHOR / SCENEWRIGHT)
**Status:** v1 — cut on Matt's directive package 2026-07-15 ("When Drax moves it to PRD…" + three functional effects). One marked veto point (§1).
**Authority:** Matt 2026-07-15 — black-copy lead · axis-title overlap fix · live/ghost color separation · basic selectable legend w/ slim highlight · hierarchical pivot table w/ chart wiring. PRD ship of this package pre-authorized by the same message.
**Companion docs:** `2026-07-11-atlas-chart-renderer-spec.md` (render law §§7–10; this note amends presentation + adds hooks as r7) · `research/curated/atlas/atlas-edition2.json` (data of record) · Glance app (`reincarnated-loadout` seam, drax).

---

## 0. Scope, seams, sequencing

Three seams: **galadriel** (r7 SVG restyle + semantic hooks), **drax** (interactive Glance page: legend, highlights, pivot table, black-skin lead), **gandalf** (this spec; verification at each hop).

**Sequencing (single-variable discipline):** the in-flight Edition-II render completes and verifies FIRST — it is the data-correctness baseline, and its acceptance-23 FIT byte-regression vs r6 is only provable on an unchanged visual grammar. r7 then restyles on FROZEN Edition-II data (its own regression law: geometry/coords byte-frozen vs Edition-II render; fills/strokes/layout re-baselined). Data-change and style-change never share a render.

Chain: Edition-II verify → **r7 render** → gandalf verify → **drax interactive build** → PRD (black copy leads). Drax MAY begin the pivot-table component + data-slim script in parallel against `atlas-edition2.json` (data model is render-independent); interactive wiring waits for r7 hooks.

## 1. Four-class visual encoding (Matt fork — resolved with lean; VETO POINT)

Matt: live kits and ghosts are both grey, size-only distinct — confusing; "change the live kits color or the ghosts color." Ruling lean (proceed unless Matt vetoes):

- **Ghosts KEEP grey** — they are ground (feasible-but-unlit lattice); ground recedes. Their aggregation grammar (log₂ size-step) is unchanged. Drill-in sub-glyphs stay subordinate-grey.
- **Live kits TAKE color** — figure advances. One saturated hue family per skin (galadriel proposes exact hues; constraints: distinct from the 12 death-class label accents already in use (#e8663d, #d4a017, #c94f8a, #8e5cc4 family), from ghost grey, from chrome; legible at smallest radius on both skins).
- **Condensations** = live-hue + multiplicity ring (they ARE live kits, plural — same hue, ringed/stepped, reading "live, many").
- **Graveyard** keeps its existing distinct muted/tombstone treatment (already separable).

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
- Each entry **toggleable (multi-select).** Selecting a class highlights ALL its members: **stroke halo ≤ 0.75px, no fill change, no dimming of non-selected marks** — "very slim, almost non-existent; dots never obscured." Instrument skin: pale luminous stroke; archive: dark ink stroke.
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

- **Black copy (instrument skin) LEADS** the atlas page; archive (white) skin behind the existing toggle. Edition-I stays as the archived second lens per current page structure.
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

---

## Cross-references

`2026-07-11-atlas-chart-renderer-spec.md` §§7–10 (render law; r7 amends presentation) · `atlas-edition2.json` ghost_field (core_order, drill_in, denominators) · tracker SESSION-DELTA -l (Edition-II audit) · Matt directive message 2026-07-15 (this package's authority).

Tracker-delta: new gap — r7 + interactive-page package specced, gated on Edition-II render verify → current-to-end-state-engine, SESSION-DELTA -m.

---

**Signed:** gandalf (SPEC-AUTHOR / SCENEWRIGHT)
**For:** the atlas chart's first interactive product surface — four-class legibility, honest ground/figure separation, and a pivot table that lets Matt walk the lattice.
