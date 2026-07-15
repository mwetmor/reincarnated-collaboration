# Atlas Edition-I — render verification note (r3: ghost-field layer)

**r3 amendment (2026-07-15, spec §9):** the feasible-lattice GHOST FIELD renders as GROUND beneath
the settled points, fired by Matt's Q30 ruling (Q30a cut-predicate amendments ratified + Q30b zero
taste cuts). Data source: elrond ghost-field emission (`atlas.json` ghost_field block, commit
d0b2a025). EXTENDS the r2 render line: the 506 point positions, KDE terrain, condensation anchors,
graveyard tombstone layout, RIDER-1 badge, and r2 explainer trio are all FROZEN; the ghost layer is
strictly additive and drawn FIRST (bottom of stack). The 12 formerly-unknown tombstones now carry
emitted death_class verdicts.

**Rendered by:** galadriel/pipeline/atlas-edition1-render-r3.mjs (deterministic; no wall-clock — all stamps from atlas.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas.json
**atlas_version:** Edition-I · **basis frozen:** 2026-07-14 · **inertia:** 8.36% · **retained dims:** 14
**emitted_at (from atlas):** 2026-07-15T04:37:20.241687+00:00
**emitter:** agentic_orchestration/research/scripts/build_atlas_json_edition1.py

## Outputs
- instrument: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r3-ghost/atlas-edition1-instrument.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r3-ghost/atlas-edition1-instrument.png`
- archive: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r3-ghost/atlas-edition1-archive.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r3-ghost/atlas-edition1-archive.png`

## Ghost field accounting (spec §9, all from emitted fields)
- feasible meso cells: **10,080** (each {core 7-tuple, depth, kit_count, lit, x, y})
- lit by census: **192** · unmapped pending curation: **14**
- sealed meso cells (OFF-plane ledger): **1,260** — L1-treatment-function-coherence 756 · L2-summon-implies-proxy 504
- coincident-projection aggregation: 10,080 cells → **7,128** distinct glyph positions (max multiplicity 6); size-stepped deterministically, NO jitter
- ghost cells outside frozen plane box (clipped, all unlit): 21
- depth Σ: **693,146,160** == depth_sum_check == post-red-law denom
- coverage callout: 469 active ≈ 6.8×10⁻⁵ % of 693,146,160 feasible exact-grain kits
- RED-3' note (emitted, drives off-plane seal semantics): RED-3' seals live at GEOMETRY drill-in, not the meso plane (geometry is a demotable non-core coord). Meso SEALED cells are L1' + L2 only. Depth badges already net out RED-3' within-cell (geometry x commit!=instant) survivors.

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
- [PASS] **r3-coverage-callout** — active 469 + denom 693,146,160 present both skins
- [PASS] **r3-sealed-ledger** — sealed 1,260 + cut ids [L1-treatment-function-coherence, L2-summon-implies-proxy] present both skins
- [PASS] **ghost-glyphs-not-regions** — ghost is <circle> glyphs; no polygon/pattern/region fills
- [PASS] **frozen-layer-regression** — instrument: point-circles FROZEN (469 pts), tombstone-positions FROZEN | archive: point-circles FROZEN (469 pts), tombstone-positions FROZEN

## Smoke tests
- [PASS] **WHIRLWIND x>0 (PERFORM)** — x=0.8191
- [PASS] **WHIRLWIND y<0 (EMBODY)** — y=-1.0816
- [PASS] **TOTEM-SENTRY x<0 (DEPLOY)** — x=-0.7307
- [PASS] **charged-dash near WHIRLWIND condensation** — poe1-charged-dash dist=0.209 (< 0.848 = 20% diag)
- [PASS] **all lit ghost glyphs inside plane frame (not clipped)** — 192 lit glyph positions, all in-frame=true
- [PASS] **coincident-projection aggregation active** — max multiplicity=6 (aggregated 10080 cells -> 7128 glyph positions)

## Layout calls / judgment made (r3)
- **FROZEN PLANE BOUNDS (load-bearing):** world bounds computed from POINTS ONLY (min/max over all 506 + 6% pad), byte-identical to the r2 baseline — so the 506 point SVG coordinates never move. The ghost field is zero-mass ground (spec §9.1a) and must NOT rescale the plane.
- **Ghost outliers CLIPPED, not rescaled:** 21 feasible cells (all unlit, 7 distinct positions) project outside the frozen point-box. They are clipped to the plane frame via SVG clip-path. Rescaling to fit un-settled outliers would break frozen-layer regression AND shrink the settled archipelago — clip is the correct call.
- **Coincident-projection aggregation (spec §9.2.4):** cells sharing a 2-dp SVG position are merged into one glyph; radius grows by log2(multiplicity+1) (deterministic size-step, NO RNG). A merged position is LIT if ANY coincident cell is lit (census-current, spec §9.1b).
- **Ghost as GLYPHS never regions (spec §9.2.2):** ghost cells are <circle> marks only — no Voronoi, no hatching, no painted boundaries (RIDER-1 continuum discipline; over-claim discipline shared with F-1).
- **Figure-ground:** unlit ghost = the feasible dark (faint near-ground); lit ghost = a touch stronger (census-lit, still sub-point). Layer order bottom→top: unlit ghost → lit ghost → density → points → tombstones → chrome. The chart's story: settled territory is a lit archipelago in a vast feasible dark.
- **Sealed = OFF-plane LEDGER (spec §9.2.4):** 1,260 sealed cells carry NO coordinates (never projected); rendered as a chrome register with cut ids verbatim from cut_id. cut_id conformance to {L1-, L2-} is a HARD refusal gate (R4).
- **Coverage + census line:** coverage callout and mandatory census line ("ghost field lit from the current census; positions from the frozen Edition-I basis.") from emitted fields. Superseded denominator 422,445,240 grep-verified ABSENT.
- **Depth is emitted, never derived (spec §9.1d):** depth per cell rendered from the field; Σ is an emitter TEST only.
- **Two skins, one layout engine:** ghost coordinate+status fingerprint identical across skins (MATCH); point fingerprint identical (MATCH). Skins vary only ghost ink/opacity chrome.
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal.

## Provenance law
chart = render(atlas.json). No number/label/coordinate originates outside an atlas.json field. Layout is computed; content is not. The ghost field is a display consumer of the emitted ghost_field block — the renderer renders emitted depth/lit/coordinate/cut_id fields and never derives them.
