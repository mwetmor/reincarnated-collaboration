# Atlas Edition-I — render verification note (r4: ghost horizon + headline coverage pair)

**r4 amendment (2026-07-15, spec §9.4):** STRICTLY-ADDITIVE chrome on top of the r3.2 render line,
fired by Matt's ratification ("I agree with all four") of gandalf's INTERIOR-1 memo review
(review-of-record: `agentic_orchestration/gandalf/design-inputs/2026-07-15-interior1-memo-review.md`).
INTERIOR-1 §3 (interior-aware placement) is REJECTED as specced; this amendment implements the memo's
§4 (horizon) and §6 (headline statistics) only. TWO changes, both skins:
  1. **GHOST HORIZON** — the convex hull of ALL 10,080 projected ghost positions (incl. the 21
     out-of-frame cells; the hull is of the lattice's REACH, then CLIPPED to the plane frame exactly
     like the ghost glyphs). Faint dashed envelope, chrome-weight, drawn BENEATH the ghost glyphs so
     it never reads as data. Mandatory label (exact string) placed adjacent to the EAST gap.
  2. **HEADLINE COVERAGE PAIR** — the coverage callout re-leads with two meso-grain statistics
     computed at render from emitted fields (lit_cells / meso_feasible, active / lit_cells). The
     exact-grain line (469 ≈ 6.8×10⁻⁵ % of 693,146,160) DEMOTES to a secondary flavor line.
Every frozen layer (points, tombstones, ghost glyph positions, sealed ledger, clip-disclosure line,
explainer trio, RIDER-1 badge) is BYTE-FROZEN vs the r3.2 baseline — verified by direct SVG diff:
the ONLY changes are the horizon chrome (added) + the re-led coverage callout (the old single line
replaced by two leads + the demoted secondary).

**r3 amendment (2026-07-15, spec §9):** the feasible-lattice GHOST FIELD renders as GROUND beneath
the settled points, fired by Matt's Q30 ruling (Q30a cut-predicate amendments ratified + Q30b zero
taste cuts). Data source: elrond ghost-field emission (`atlas.json` ghost_field block, commit
d0b2a025). EXTENDS the r2 render line: the 506 point positions, KDE terrain, condensation anchors,
graveyard tombstone layout, RIDER-1 badge, and r2 explainer trio are all FROZEN; the ghost layer is
strictly additive and drawn FIRST (bottom of stack). The 12 formerly-unknown tombstones now carry
emitted death_class verdicts.

**r3.2 amendment (2026-07-15, spec §9.2.3, r3.2/commit `7cf1eeca`):** gandalf's r3 verification verdict
was ACCEPT-WITH-ONE-AMENDMENT. The clip call on the out-of-frame ghost cells was correct (frozen plane
bounds; zero-mass ground never rescales the frame) but was disclosed only in this note — on the chart, the
GHOST FIELD ledger claimed all feasible cells without saying some project beyond the frame. §9.2.3 now binds:
any clip MUST be disclosed on-chart in the ghost ledger. FIX: a clip-disclosure microcopy line renders in the
GHOST FIELD ledger box (both skins); the count is COMPUTED FROM THE RENDER PASS (cells whose projected
position falls outside the plane rect), never hard-coded — it follows any future atlas.json change; if zero
cells clip the line is omitted entirely (no "0 clipped"). Acceptance suite gains `r3.2-clip-disclosure`.

**Rendered by:** galadriel/pipeline/atlas-edition1-render-r4.mjs (deterministic; no wall-clock — all stamps from atlas.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas.json (unchanged, elrond d0b2a025)
**Frozen-layer baseline:** agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r3-ghost (r3.2)
**atlas_version:** Edition-I · **basis frozen:** 2026-07-14 · **inertia:** 8.36% · **retained dims:** 14
**emitted_at (from atlas):** 2026-07-15T04:37:20.241687+00:00
**emitter:** agentic_orchestration/research/scripts/build_atlas_json_edition1.py

## Outputs
- instrument: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r4-horizon/atlas-edition1-instrument.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r4-horizon/atlas-edition1-instrument.png`
- archive: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r4-horizon/atlas-edition1-archive.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r4-horizon/atlas-edition1-archive.png`

## Ghost field accounting (spec §9, all from emitted fields)
- feasible meso cells: **10,080** (each {core 7-tuple, depth, kit_count, lit, x, y})
- lit by census: **192** · unmapped pending curation: **14**
- sealed meso cells (OFF-plane ledger): **1,260** — L1-treatment-function-coherence 756 · L2-summon-implies-proxy 504
- coincident-projection aggregation: 10,080 cells → **7,128** distinct glyph positions (max multiplicity 6); size-stepped deterministically, NO jitter
- ghost cells outside frozen plane box (clipped): **21** (all unlit=true; 7 distinct positions) — CLIP DISCLOSURE (r3.2, spec §9.2.3) rendered in the GHOST FIELD ledger, count from the render pass
- clip-disclosure line as rendered (both skins): **"21 unlit cells project beyond the frame (clipped, not rescaled — frame frozen to the settled points)"**
- depth Σ: **693,146,160** == depth_sum_check == post-red-law denom
- RED-3' note (emitted, drives off-plane seal semantics): RED-3' seals live at GEOMETRY drill-in, not the meso plane (geometry is a demotable non-core coord). Meso SEALED cells are L1' + L2 only. Depth badges already net out RED-3' within-cell (geometry x commit!=instant) survivors.

## Ghost HORIZON accounting (r4, spec §9.4.1 — all COMPUTED FROM THE RENDER PASS)
- **hull vertex count: 22** (convex hull of 7,128 distinct projected ghost positions, INCLUDING the 21 out-of-frame cells — the hull is of the lattice's REACH, then clipped to the plane frame)
- hull east reach (world x): **1.2581** · settled points east reach (world x): **1.6276** · **EAST gap = 0.3695** (settled kits stand east of the horizon there — the load-bearing disclosure direction)
- envelope: dashed polyline (open, closed back to first vertex), CLIPPED to plane frame via the same planeClip used by ghost glyphs; drawn BENEATH the ghost glyphs (chrome, sub-ghost — must not read as data)
- label (exact string, verbatim): **"ghost coverage limit — dark beyond this line is unmapped at meso grain, not absent."** — placed adjacent to the EAST gap, tied to the hull's east vertex by a thin dashed leader; visible two-line wrap (split at the em-dash); the exact contiguous string is carried in the envelope's `<title>` (grep-verified present both skins)
- computed-not-constant: PROVEN by the r4-horizon doctored-input test (remove the extreme corner cell → hull recomputes → CHANGES); vertices are never hard-coded

## Headline COVERAGE PAIR accounting (r4, spec §9.4.2 — ratios COMPUTED, not hard-coded)
- lead 1: **"192 / 10,080 ≈ 1.9% of feasible meso ground ever lit"** (lit_cells 192 / meso_feasible 10,080)
- lead 2: **"469 kits over 192 lit cells ≈ 2.4 kits per lit cell — the genre didn't explore; it remade."** (active 469 / lit_cells 192)
- demoted secondary (retained, no longer lead): **"469 active ≈ 6.8×10⁻⁵ % of 693,146,160 feasible exact-grain kits"** — the 693M exact-grain line; present ONLY in the secondary position (grep-verified NOT in either lead)
- anti-"422,445,240" grep: verified ABSENT (superseded denominator never appears)

## Point accounting (FROZEN from r2)
- active: **469** (neutral 383 + grouped 86) · corpses: **37** · total: **506**
- death classes: extrinsic-content-mix:3, extrinsic-itemization:7, extrinsic-no-lever:4, extrinsic-split-scaling:3, extrinsic-tuning:7, intrinsic-red:12, system-evidence:1

## Acceptance tests
- [PASS] **point-counts** — active=469 (exp 469), supp=37 (exp 37), total=506 (exp 506)
- [PASS] **grouped-count** — grouped=86 (exp 86)
- [PASS] **ghost-counts** — feasible=10080 (exp 10080), sealed=1260 (exp 1260)
- [PASS] **ghost-lit-conformance** — feasible lit=true 192 == emitted lit_cells 192
- [PASS] **ghost-depth-sum** — Σdepth=693,146,160 == depth_sum_check 693,146,160 == denom 693,146,160
- [PASS] **sealed-cut_id-conformance** — all 1260 sealed cut_ids in {L1-,L2-}: L1-treatment-function-coherence, L2-summon-implies-proxy
- [PASS] **point-layout-equality** — identical point coordinate fingerprint
- [PASS] **ghost-layout-equality** — identical ghost coord+status fingerprint (both skins)
- [PASS] **determinism** — instrument:byte-equal, archive:byte-equal
- [PASS] **R2-no-2.57-numeral** — clean (naive-box 2.57 absent as content)
- [PASS] **R2ext-no-422445240** — clean (superseded denominator absent)
- [PASS] **R3-no-season-N** — clean
- [PASS] **RIDER-1-badge** — inertia_pct=8.36 + retained_dims=14 + structure_statement present both skins
- [PASS] **r2-pole-glosses** — all 4 pole glosses present both skins
- [PASS] **r2-density-legend-line** — density-field legend line present both skins
- [PASS] **r2-derivation-gloss** — derivation gloss present both skins
- [PASS] **r3-census-line** — mandatory census line present both skins
- [PASS] **r3.2-clip-disclosure** — clip line present both skins (count=21, from render pass; all clipped cells unlit=true)
- [PASS] **r3-coverage-callout** — active 469 + denom 693,146,160 present both skins
- [PASS] **r3-sealed-ledger** — sealed 1,260 + cut ids [L1-treatment-function-coherence, L2-summon-implies-proxy] present both skins
- [PASS] **ghost-glyphs-not-regions** — ghost is <circle> glyphs; no polygon/pattern/region fills
- [PASS] **frozen-layer-regression** — instrument: point-circles FROZEN (469 pts), tombstone-positions FROZEN | archive: point-circles FROZEN (469 pts), tombstone-positions FROZEN
- [PASS] **r4-horizon** — envelope=true, exact-label=true, computed-not-constant: removed extreme cell @ (-1.0910,-1.6548) ×2; hull CHANGED (canonical 22 vtx)
- [PASS] **r4-headline-pair** — lead present=true, ratios match indep (lit 1.9%, density 2.4)=true, 693M in secondary only=true
- [PASS] **r4-frozen-layer-regression-vs-r3.2** — instrument: points FROZEN, ghost-glyphs FROZEN, tombstones FROZEN, frozen-text PRESENT | archive: points FROZEN, ghost-glyphs FROZEN, tombstones FROZEN, frozen-text PRESENT

## Smoke tests
- [PASS] **WHIRLWIND x>0 (PERFORM)** — x=0.8191
- [PASS] **WHIRLWIND y<0 (EMBODY)** — y=-1.0816
- [PASS] **TOTEM-SENTRY x<0 (DEPLOY)** — x=-0.7307
- [PASS] **charged-dash near WHIRLWIND condensation** — poe1-charged-dash dist=0.209 (< 0.848 = 20% diag)
- [PASS] **all lit ghost glyphs inside plane frame (not clipped)** — 192 lit glyph positions, all in-frame=true
- [PASS] **coincident-projection aggregation active** — max multiplicity=6 (aggregated 10080 cells -> 7128 glyph positions)
- [PASS] **ghost hull is a small polygon** — hull vertex count=22
- [PASS] **EAST gap real (ghost hull east < settled east)** — ghost hull east x=1.2581 < settled east x=1.6276 (gap=0.3695)
- [PASS] **headline lit-fraction ≈ 1.9%** — lit fraction=1.9% (192/10080)
- [PASS] **headline density ≈ 2.4 kits/cell** — density=2.4 (469/192)

## Layout calls / judgment made (r4 — the NEW calls this amendment adds)
- **Hull computed in WORLD space, drawn projected, clipped to frame (spec §9.4.1).** The convex hull is taken over the DISTINCT world positions of ALL 10,080 feasible cells (Andrew's monotone chain; deterministic sort x-asc then y-asc; ≤0 cross-product test drops collinear points → a tight 22-vertex ring). This is the lattice's true reach — it INCLUDES the 21 out-of-frame outliers. Each vertex is then projected through sx/sy and the polyline is clipped to the plane rect by the SAME planeClip that trims the ghost glyphs. Rationale: hulling in world space (not the in-frame subset) means the envelope describes the real reach; clipping (not rescaling) keeps the frozen frame. **Vertices are from the render pass — never hard-coded** (doctored-input test proves it).
- **Horizon drawn BENEATH the ghost glyphs (spec §9.4.1 "sub-ghost, chrome not data").** The envelope polyline is emitted at the TOP of the LAYER-0 clip group, BEFORE the ghost dark/lit glyph groups — so the glyphs paint OVER it. This is the judgment call that keeps it from reading as data: a limit line the eye registers as ground, not as a plotted boundary. (Consequence: the ghost glyph `<circle>` byte-strings are unchanged vs r3.2 — frozen-layer regression holds.)
- **Stroke treatment (layout call):** hairline dashed. `stroke-width` 1.1 (both skins), `stroke-dasharray` "7 5" (a long-dash reads as "limit/threshold", distinct from the zero-axis "2 6" fine-dot and the tombstone "2 2"), `stroke-linejoin=round` so hull corners don't spike. Instrument: cool gray `#93a0b3` @ 0.62 opacity. Archive: dim gilt `#5a5340` @ 0.75 — "embers at the edge of the walked dark". NO fill (a fill would assert the region-claim §9.2.2 forbids — the envelope is an open dashed line, never a shaded area).
- **Label placement (layout call — named per spec ask): adjacent to the EAST gap.** The mandatory string is anchored off the hull's EAST vertex (the greatest-projected-x vertex, computed from the render pass — not hard-coded). A thin dashed leader + a small hollow marker tie the label to that vertex; the label itself drops into the sparse lower-right interior (measured: only 3 settled points in the east-gap band) and reads right-anchored into the gap. This is the load-bearing direction: settled kits reach x=1.628, the ghost hull ends x=1.258; the two gold flame-kits visibly sit EAST of the envelope, in the "dark beyond" the label names. **Two-line visible wrap** (split at the em-dash, a natural clause break) for legibility of an 85-char disclosure sentence; the exact contiguous string lives in the polyline `<title>` so the acceptance grep matches the whole label verbatim.
- **HEADLINE PAIR re-lead (spec §9.4.2):** the two meso-grain stats now LEAD the callout (font 13.5/12, bold, ink) at lower-left; the exact-grain 693M line DEMOTES directly below at font 10, faint (`glossStyle`, `faint` ink) — retained and honest, no longer the lead. Both ratios (1.9%, 2.4) are computed from emitted fields (lit_cells/meso_feasible, active/lit_cells); the prose halves are content-locked disclosure copy (same class as the pole glosses). The 693M numeral is grep-verified ABSENT from both leads.

## Layout calls / judgment inherited (r3/r3.2 — unchanged, byte-frozen)
- **FROZEN PLANE BOUNDS (load-bearing):** world bounds computed from POINTS ONLY (min/max over all 506 + 6% pad), byte-identical to the r2 baseline — so the 506 point SVG coordinates never move. The ghost field is zero-mass ground (spec §9.1a) and must NOT rescale the plane.
- **Ghost outliers CLIPPED, not rescaled — DISCLOSED on-chart (r3.2, spec §9.2.3):** 21 feasible cells (all unlit=true, 7 distinct positions) project outside the frozen point-box. They are clipped to the plane frame via SVG clip-path. Rescaling to fit un-settled outliers would break frozen-layer regression AND shrink the settled archipelago — clip is the correct call. **The clip is no longer silent:** a disclosure line renders in the GHOST FIELD ledger (both skins), count computed FROM THE RENDER PASS (cells whose projected position falls outside the plane rect), so it follows any future atlas.json change; if zero cells clipped the line is omitted entirely (no "0 clipped"). §9.2.3: the dark the reader sees implicitly claims to be the feasible space — silent truncation is an under-claim.
- **Coincident-projection aggregation (spec §9.2.4):** cells sharing a 2-dp SVG position are merged into one glyph; radius grows by log2(multiplicity+1) (deterministic size-step, NO RNG). A merged position is LIT if ANY coincident cell is lit (census-current, spec §9.1b).
- **Ghost as GLYPHS never regions (spec §9.2.2):** ghost cells are <circle> marks only — no Voronoi, no hatching, no painted boundaries (RIDER-1 continuum discipline; over-claim discipline shared with F-1).
- **Figure-ground:** unlit ghost = the feasible dark (faint near-ground); lit ghost = a touch stronger (census-lit, still sub-point). Layer order bottom→top: unlit ghost → lit ghost → density → points → tombstones → chrome. The chart's story: settled territory is a lit archipelago in a vast feasible dark.
- **Sealed = OFF-plane LEDGER (spec §9.2.4):** 1,260 sealed cells carry NO coordinates (never projected); rendered as a chrome register with cut ids verbatim from cut_id. cut_id conformance to {L1-, L2-} is a HARD refusal gate (R4).
- **Coverage + census line:** coverage callout and mandatory census line ("ghost field lit from the current census; positions from the frozen Edition-I basis.") from emitted fields. Superseded denominator 422,445,240 grep-verified ABSENT.
- **Depth is emitted, never derived (spec §9.1d):** depth per cell rendered from the field; Σ is an emitter TEST only.
- **Two skins, one layout engine:** ghost coordinate+status fingerprint identical across skins (MATCH); point fingerprint identical (MATCH). Skins vary only ghost + horizon ink/opacity chrome. The horizon hull, label placement, and headline-pair layout are one code path — both skins carry the same 22-vertex hull and the same label anchor.
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal (verified across separate process invocations).

## Provenance law
chart = render(atlas.json). No number/label/coordinate originates outside an atlas.json field. Layout is computed; content is not. The r4 additions honor this: the ghost horizon's 22 vertices are COMPUTED from the emitted ghost field (never hard-coded — the doctored-input test proves the hull follows the data); the headline-pair ratios (1.9%, 2.4) are COMPUTED from emitted counts (lit_cells, meso_feasible, active), not literals in source; the label string and the headline prose halves are content-locked disclosure copy carried verbatim. The renderer computes layout; it never invents content.
