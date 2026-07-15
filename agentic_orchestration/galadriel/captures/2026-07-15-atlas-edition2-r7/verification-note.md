# The Atlas of Kits — EDITION II · r7 RESTYLE + SEMANTIC-HOOKS verification note

**EDITION II r7 (2026-07-15, spec `2026-07-15-atlas-interactive-glance-spec` §§1-3, §7 acc 29-31).**
Restyle + semantic-hooks pass on FROZEN e21 geometry. Data of record `atlas-edition2.json` READ-ONLY,
unchanged this pass. Every mark coordinate/geometry is BYTE-FROZEN vs the e21 baseline (fb951b39);
ONLY fills/strokes/text-layout/hook-attributes re-baseline. The e21 pipeline + captures are the
FREEZE RECORD (untouched). Determinism: double-render byte-equal, both skins.

## r7 — the three items (spec §§1-3)

**§1 · Four-class visual encoding.** SINGLE (non-condensation) live kits TAKE COLOR — figure over the
grey ground. **Chosen live-single hue** (fill change only; geometry byte-frozen):
- **instrument (LIGHT #f7f8fa):** `#50991f` — chartreuse-lime, H≈96° S0.80 V0.60, fill-opacity 0.95.
- **archive (DARK #0e1016):** `#7cd143` — chartreuse-lime, H≈96° S0.68 V0.82, fill-opacity 0.92.

  H≈96° sits in the **121° dead-zone** between CH-BEAM gold (43.5°) and AURA teal-green (164.6°):
  **min hue-clearance 52.5°** from EVERY one of the six condensation hues (WHIRLWIND 14.4° · CH-BEAM
  43.5° · AURA 164.6° · TOTEM 206.4° · TRAP 268.8° · MINION 331.0°), and distinct from the death-class
  accents (tombInk desaturated H221 / tombUnknownInk H16-24), ghost grey, and chrome. Legible at the
  3px live radius: contrast-vs-canvas 3.34 (light) / 10.01 (dark). Ghosts KEEP grey (radii untouched —
  the E2.1 drill floor is undisturbed); condensation members KEEP their six group colors; graveyard
  keeps †.

**§2 · Axis title/gloss layout fix (LAYOUT-ONLY).** e21 rendered all four pole titles + r2 glosses
INSIDE the plot rect (x∈[96,1504], y∈[132,1104]) → every one intersected the plot rect + data field
(Matt's margin collision; acceptance-30 fail). Relocated to reserved margin bands (content-locked
strings survive VERBATIM — the lock is on strings, not coordinates):
- **PERFORM →** RIGHT rail x[1504,1600], rotated -90° (reads bottom→top), centered cyMid=618 (title inner x=1546, gloss outer x=1561).
- **← DEPLOY** LEFT rail x[0,96], rotated -90°, centered cyMid=618 (title inner x=54, gloss outer x=39).
- **↑ LAUNCH** TOP strip y=120 (band y[106,131], below deriv-gloss / above plot), horizontal, title+gloss combined single line, centered cxMid=800.
- **EMBODY ↓** BOTTOM-center pocket x[703,916] (between the two ledger columns), title y=1119 (cap-top ≈1106.5 > plot-bottom 1104), gloss wrapped 2 lines @14px pitch (y=1134,1148), FULL string in a `<title>` for the verbatim grep.

**§3 · Semantic hooks (enables downstream interactivity).** Five layer groups + per-mark data
attributes (EMITTED-FIELD COPIES, never renderer inventions; §4c law). SVG at rest is print-grade
static — hooks are inert attributes, NO scripts inside the SVG.
- Layers: `<g id="layer-drillin">`, `layer-ghosts`, `layer-live`, `layer-graveyard`, `layer-chrome` (each ×1).
- `data-el` ∈ {live, condensation, graveyard, ghost} on every mark. live+graveyard carry `data-kit`
  (kit_id); condensation carry `data-kit` + `data-kits` (`|`-joined member list); meso ghost glyphs
  carry `data-core` (emitted 7-tuple, core_order emit order, `|`-joined) + `data-mult` (multiplicity).

## r7 — WHITELIST (the ONLY channels that re-baseline; everything else byte-frozen vs e21)
1. **single-kit fill** grey → chartreuse-lime (both skins; the `<g fill>` group attr — the circle strings themselves are frozen).
2. **five `<g id=layer-*>` wrappers** (structural grouping; no transforms → no coordinate change).
3. **data-* hooks** — data-el / data-kit / data-kits / data-core / data-mult (inert attributes on existing marks).
4. **four pole title+gloss margin-band relocations** (text x/y/anchor/transform re-layout; strings verbatim).
5. **horizon-vs-drill hairline paint order** — splitting the drill into its own layer moves it before the ghost/horizon layer; the horizon dashed line now paints over the drill sub-ground (both chrome-quiet; drill stays below the meso glyphs — the load-bearing subordination is preserved).

## r7 — geometry-freeze proof (independent of the acceptance harness)
Byte-identical between e21 and r7, BOTH skins: 469 point circles (cx,cy,r,title) · 46,005 ground
circles (cx,cy,r) · 37 tombstones (x,y,title) · the CHARTED HORIZON hull polyline points. No mark
moved. (`r7-restyle-regression` asserts this in-suite; the note's claim is separately re-verified.)

## r7 — hook-count reconciliation (spec §7 acc-31)
- `data-el="live"` = **383** (== emitted single kits) · `data-el="condensation"` = **86** (== emitted condensation members) · `data-el="graveyard"` = **37** (== emitted corpses).
- **506 points classed** = 383 + 86 + 37 = 506 (== active 469 + supplementary 37).
- `data-el="ghost"` = **46006** = 7128 meso ghost glyph positions (7,128) + 38878 drill glyph entries (38,878).
- Every `data-kit` / `data-kits` member ⊂ emitted kit_id set; every `data-core` ⊂ emitted feasible-cell core set (grepped). Doctored-input (a hook value absent from atlas-edition2.json) → HALT (verified by `r7-hooks-doctored-halt`).

## r7 — FLAGGED (flag-don't-invent seams surfaced, not invented)
- **§3.2 aggregate-core representative-cell resolution.** 1,656 of the 7,128 meso ghost glyphs aggregate
  coincident feasible cells with DIFFERING cores (max mult 8). A single glyph cannot carry all member
  cores, and §4c forbids synthesizing a tuple. `data-core` copies the **representative cell's** 7-tuple
  — the FIRST feasible cell (emitted array order) landing in that raster bucket. Deterministic (emit
  order is fixed), a VERBATIM emitted 7-tuple of a real cell at that exact position. Flagged for the
  drax pivot: the ghost branch keys on the emitted `feasible_cells`, not on `data-core` alone, so all
  member cores at a position remain reachable in the pivot data.
- **§3.2 drill-glyph no-emitted-core.** The emitted `sub_feasible_glyph_field` entries carry
  {x, y, multiplicity} ONLY — no core tuple. Drill glyphs therefore carry `data-el="ghost"` + `data-mult`
  but NO `data-core` (no emitted field to copy; §4c forbids inventing one). Downstream drill-branch
  interactivity keys on position + the emitted drill_in ledger, not on a per-glyph core.

**The six E2.1 fixes (spec §10.8 a-f) — carried forward on the frozen geometry:**
- **(a) CHARTED HORIZON** — the dashed line redefined to hull(meso-feasible ∪ drill-in sub-feasible),
  clipped at the frozen frame. Renamed CHARTED HORIZON (Matt veto-pending — string swappable via
  LINE_NAME). Gloss carries charted-space semantics + grain asymmetry (east charted to
  geometry×commit drill-in depth; west meso grain; beyond: uncharted). Beyond-horizon N recomputes
  vs the NEW hull: **14 → 0** (the charted horizon now encloses ALL settled kits — the P-DF-1 finding
  realized; the affirmative charted-reach line carries it on the LINE, the beyond line zero-case-omits).
- **(b) Drill-in prominence floor** — radius floor 1.25px + compressed log₂ step (0.30→0.12) → min
  drill radius **1.37px** (was 0.75, sub-pixel); fill-contrast floor vs canvas both skins (instrument
  1.179, archive 1.323) — each above canvas, below the meso-ghost. Subordination order preserved on
  BOTH channels; the drill-in dots now read at overview scale.
- **(c) Banner relabel** — leads with the chart's own edition ("Edition II lattice · basis: Edition-I
  (frozen 2026-07-14) · …"); the r-series contradictory "Edition 1 · frozen" lead is gone; every
  locked substring verbatim.
- **(d) Provenance dedupe** — footer edition token deduped ("Edition-II · Edition II" → one).
- **(e) Skin→canvas map** — render-provenance.json gains an explicit skin→canvas map so drax binds to
  CANVAS, never name. Skins NOT renamed.
- **(f) Chrome-uniqueness + bottom-band overlap** — every visible chrome string ×1 per skin; zero
  text-bbox overlap in the below-plane ledger band + footer, both skins.

**Rendered by:** galadriel/pipeline/atlas-edition2-r7-render.mjs (deterministic; no wall-clock — all stamps from atlas-edition2.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas-edition2.json (elrond; gandalf audit-grade ACCEPT — READ-ONLY this pass)
**r7 geometry-freeze baseline:** 2026-07-15-atlas-edition2-e21 (fb951b39) — ALL mark geometry byte-frozen vs this (acceptance-29); e21 pipeline + captures UNTOUCHED (the freeze record)
**FIT-layer coord baselines:** r6 (2026-07-15-atlas-edition1-r6-legibility, coord+title tuple) AND e21 (geometry byte-freeze) — points + tombstones coordinate-identical to BOTH
**atlas_version:** Edition-II · **edition:** II · **iteration:** r7 · **register:** feasibility-cuts-register-v1.2
**basis frozen:** 2026-07-14 · **inertia:** 8.36% · **retained dims:** 14
**emitted_at (from atlas):** 2026-07-15T19:20:12.237153+00:00 · **emitter:** agentic_orchestration/research/scripts/build_atlas_json_edition2.py

## Acceptance tally
- **ACCEPTANCE: 41/41 PASS** (0 fail) · **SMOKE: 17/17 PASS**
- **P-DF-1 VERDICT: PASS** (S_max 2.84105203 > K_max 1.87424756; falsified=false) — top-level mirror `p_df_1_verdict`=PASS. NOT falsified — the registered prediction holds; INTERIOR-1 stays closed (no new fuel).
- **Edition-II suite (22-28) + re-instantiated priors (§7/§9): all covered.** Priors 1-18 re-run against
  Edition-II artifacts; the three intra-edition frozen-layer regressions (r2/r3.2/r5) are RETIRED across
  the edition boundary (§10.4.3) and REPLACED by acceptance 23 (fit-layer-regression vs r6). r4-horizon +
  r4-headline-pair + r5-beyond-horizon re-instantiate (computed-not-constant, edition-safe). r6 legibility
  criteria adapt to the below-plane ledger band (`E2-belowplane-ledger-band`).

## Outputs
- instrument: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-r7/atlas-edition2-instrument.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-r7/atlas-edition2-instrument.png`
- archive: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-r7/atlas-edition2-archive.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-r7/atlas-edition2-archive.png`

## Edition-II acceptance criteria (22-28, spec §10.6)
- **#22 register-v1.2-derivation** — new exact + meso denominators independently re-derived (audit bar = v1/v1.1); pull-slice vetted (new_law_needed=0, no HALT); register=v1.2.
- **#23 fit-layer-regression** — basis + 506 point coords + tombstones + content-locked strings byte-identical to r6 (the FIT freeze; the load-bearing edition check).
- **#24 lattice-integrity** — depth Σ == new exact denom; lit census reproduces from corpus keys; unmapped + off-plane registers enumerated (MCD 94 disclosed).
- **#25 pull-slice-lit-integrity** — every lit pull cell traces to an EXISTING re-keyed kit; ZERO mcd-lit; doctored-input HALT (mcd forced past gate + pull new-law).
- **#26 drill-in-conformance** — sub-cells EAST-half only; grain-scoped seal enums with doctored proofs BOTH grains (RED-3- surfaces at drill-in; NOT at meso).
- **#27 P-DF-1-scored** — verdict emitted mechanically (this note + provenance JSON).
- **#28 edition-stamp + anti-stale greps** — "Edition II" + v1.2 both skins; Edition-I denoms only in labeled lineage; "422,445,240" absent; content-locked strings verbatim.

## FIT-LAYER FREEZE (acceptance 23 — the load-bearing edition check)
- **Independently re-verified at the artifact level:** atlas.json[basis] == atlas-edition2.json[basis] AND
  atlas.json[points] == atlas-edition2.json[points] — byte-identical (JSON.stringify compare). The 14-dim
  basis, all 506 point coordinates, axis names (PERFORM <-> DEPLOY · EMBODY <-> LAUNCH), tombstone death
  classes, RIDER-1 (8.36% / 14 dims): untouched.
- **Rendered-geometry freeze:** the 506 point circles + 37 tombstone daggers extracted from the Edition-II
  SVGs are BYTE-IDENTICAL to the committed r6 Edition-I SVGs (both skins). The frozen INPUT renders to the
  frozen point/tombstone geometry byte-for-byte. Whitelisted to re-render: the LATTICE layer (§10.4.3).

## LATTICE RE-EMISSION (wholesale — this is what makes it an edition)
- **Ghost field (meso):** 11,160 feasible meso cells (Edition-I: 10,080) · 193 lit by the census (Edition-I: 192) · 108 unmapped pending curation.
- **Denominators re-derived (§10.1.5):** exact 767,411,820 (Edition-I 693,146,160); depth Σ 767,411,820 == exact == depth_sum_check 767,411,820. Meso 11,160 feasible + 1,314 sealed. Meso sealed split: L1 756 + L2 558 == 1,314.
- **Coincident aggregation:** 11,160 cells → 7,128 distinct glyph positions (max multiplicity 8); size-stepped deterministically, NO jitter.
- **Ghost cells clipped (out-of-frame):** 27 (all unlit=true) — CLIP DISCLOSURE rendered, count from the render pass.
- **Ghost horizon (recomputed):** hull vertex count **23** (Edition-I: 23) — the computed-not-constant law (§9.4.1/§9.5) pays off across the edition boundary. East reach world x=2.3100 < settled east x=1.6276 (EAST gap=-0.6824).
- **Beyond-horizon (recomputed):** N=**0** active kits beyond the ghost hull () — recomputed from the NEW field; matches the emitted `p_df_1.n_beyond_horizon_kits`. Position ≠ membership (7-core meso blindness).

## PULL SLICE (§10.1 — the +`pull` function level)
- **pull_slice:** 1,080 feasible + 54 sealed (all L2-summon-implies-proxy) · **2 lit pull cells**.
- **new_law_needed=0** (pull vets under the RATIFIED ledger — ZERO new laws; L1′ cannot seal pull; L2 seals SUMMON×solo×pull=54). `halt`=false.
- **The 2 lit pull cells trace to EXISTING corpus kits re-keyed on intrinsic evidence** (census-freeze: zero NEW rows this edition):
    - `["FREE-MOVE","ZONE","damage","pull","solo","active","one-shot"]`
  - `["WALK","NOVA","control","pull","solo","active","one-shot"]`
  These are the `d3-zbarb` (Wrenching Smash rune) + `di-cyclone-monk-pvp` (skill-level) re-keys — both PRESENT as active points, both NON-mcd. Positions frozen, lighting moves (C3 precedent).
- **ZERO mcd-lit:** 0 mcd- points on the plane (all 94 held off-plane by the movement=blank gate). Doctored-input HALT proven (mcd forced past the gate + pull new-law both HALT loud).

## EAST-HALF DRILL-IN (§10.3 — promoted geometry×commit sub-cells)
- **region:** EAST-half (projected x>=0; PERFORM side) — slate #1 ES + #2 EN (one drill-in serves both) · **promoted pair:** geometry×commit · **local-first law** (EAST-half only; edition-wide is ~21× the glyph field, unvettable in one pass).
- **5,068 parent cells** → **172,312 sub-feasible** + **10,136 RED-3- sealed** (5,068 × 36 = 182,448 total sub-grid).
- **Sub-feasible arrives PRE-AGGREGATED** as `sub_feasible_glyph_field`: 38,878 entries {multiplicity, x, y}, Σmultiplicity=172,312 (== n_sub_feasible 172,312). Rendered as VISUALLY SUBORDINATE supplementary GROUND (zero-mass §10.3.4): re-aggregated to 38,878 SVG-raster glyph positions (max mult 35), drawn BENEATH the meso ghost at reduced prominence (drillR + drillOp << ghostR + ghostOp), CLIPPED to the frame (1,130 clipped).
- **Sub-sealed ledger (§10.4.2):** `RED-3-movement-damage-carveout` (dash_attack×channel) 5,068 · `RED-3-movement-damage-carveout` (dash_attack×wind-up) 5,068 — Σ 10,136 == n_sub_sealed. **RED-3′ surfaces ONLY at this grain** — a VISIBLE sub-cell seal, netted-out of meso depth. Meso sealed cut_ids stay {L1-, L2-}; RED-3- at meso REFUSES loud (doctored proof).

## OFF-PLANE CORPUS (§10.4.4 — new mandatory ledger line)
- **disclosure (verbatim, emitted):** "94 gear-grain kits (mcd-) sit in the corpus off-plane — classless gear carries no movement identity at kit grain; admission is a deferred grain ruling."
- **N = 94** gear-grain (mcd-) kits held off-plane (== `gate_rejected_keyed`); computed from the emitter's gate rejections, never hard-coded. Classless gear carries no movement identity at kit grain — admission is a deferred grain ruling (the 94 stay atlas-invisible this edition).

## DENOMINATOR SUPERSESSION (§10.1.5 — labeled lineage)
- **superseded (Edition I), rendered ONLY in the labeled lineage line:** 693,146,160 exact · 10,080 meso feasible · 1,260 meso sealed.
- **anti-stale grep (acceptance 28):** "693,146,160" and "10,080" appear ONLY inside the labeled superseded-lineage line (stripped-of-lineage body carries neither). "422,445,240" absent ENTIRELY.

## P-DF-1 (§10.5 — scored mechanically at render)
- **prediction:** EAST drill-in (geometry×commit) extends the dark BEYOND the whirlwind/beam kits along û=normalize(mean(c_whirlwind, c_channel)).
- **VERDICT: PASS** — S_max **2.84105203** (argmax x=1.85239877, y=-2.15412247) > K_max **1.87424756** (the max beyond-horizon reach along û). falsified=**false**. û=[0.6502, -0.7598].
- **machine-readable verdict is in the render provenance JSON** (`p_df_1` block). The east drill-in extends the dark BEYOND the whirlwind/beam kits along û — the registered prediction holds.

## EDITION STAMP (§10.4.5)
- Footer (both skins): "Edition-II · Edition II · feasibility-cuts-register-v1.2 · …". Edition-I renders remain archived untouched (r1..r6 captures).

## RENDER-FORM SEAMS (flagged per brief — where §10 left the form unspecified)
- **SEAM (flagged, resolved): the Edition-II ledger volume vs the r6 in-plane occlusion guard.** §10 does
  not spec a render form for a ledger this large. The r6 in-plane lower-right plaque held ~6 lines and
  cleared the §9.6.4.21 occlusion guard because the east-gap lower-right has only ~3 settled POINTS.
  Edition-II's lattice ledger carries ~16 accounting lines (pull slice · drill-in ground · sub-sealed
  RED-3′ · off-plane corpus · superseded lineage, atop the r6 set). A plaque holding all of it grows UP
  into the dense settled archipelago and occludes **4 settled POINTS + thousands of ghost-glyph centers**
  — the occlusion guard (correctly) HALTS, and it MUST (occluding a settled point behind a legend is the
  dishonesty the guard exists to stop). **Resolution (following established grammar, not invented):**
  §9.2.4 already rules "sealed = a margin/legend LEDGER, never on-plane"; the r4/r5/r6 `<title>` pattern
  already carries long disclosure sentences whole. So the WHOLE ledger moves to the BELOW-PLANE MARGIN band
  (y > plane bottom 1104) — the chrome band the census/headline/coverage lines already occupy, where nothing
  can occlude a data mark (all data is inside the frame). Each entry renders a compact VISIBLE SUMMARY +
  the FULL contiguous emitted string in a `<title>` (present for the whole-grep acceptance AND for hover).
  **Consequence:** no in-plane plaque, so the r6 plaque-geometry criteria (occlusion-guard, footer-plaque
  re-anchor) become MOOT and are re-instantiated as `E2-belowplane-ledger-band` — a STRONGER guarantee
  (zero plaque over ground at all; census footer at the plane right edge; full strings in `<title>`). This
  is the ONE render-form seam §10 left open; it is resolved by the established grammar, not new grammar.
- **No other seam required new grammar.** Pull cells → existing ghost-glyph grammar (they live in
  feasible_cells). Drill-in sub-feasible → existing coincident-aggregation + log₂ size-step at reduced
  prominence. Sub-sealed → existing off-plane chrome ledger. Off-plane corpus / superseded lineage →
  existing disclosure-line grammar. Horizon + beyond-horizon + clip → existing computed-not-constant paths.

## Layout calls / judgment made (Edition II)
- **Drill-in layer ORDER (render-form choice, established grammar):** the promoted sub-cells are the FINEST
  ground (a finer resolution of the feasible dark), so they draw FIRST in LAYER 0 (beneath the meso ghost
  glyphs), at reduced prominence — the eye reads meso ghost OVER the drill-in dust. Zero-mass: sx/sy is the
  frozen point-projection; the drill-in never moves the frame; the planeClip trims EAST-half sub-cells that
  project beyond it. The drill-in glyphs carry no data claim (they are ground); the sub-sealed ledger (the
  RED-3′ seals) is off-plane chrome, cut_ids verbatim.
- **Below-plane ledger (see render-form seam above).** Two columns in the ~84px below-plane band: left =
  r4 census/headline/coverage + core ghost accounting; right = the Edition-II lattice ledger (compact
  summaries + `<title>` full strings). No plaque; zero occlusion.
- **Footer stamp honest + E2.1-d deduped + E2.1-f trimmed.** The footer stamps a single "Edition-II"
  token (E2.1-d dedupe removed the redundant "· Edition II"); the visible stamp is trimmed to
  edition · register · emitted · skin (E2.1-f: clears the right census footer — no bottom-band
  overlap); the full emitter + render-script provenance lives in render-provenance.json.

## Layout calls inherited (frozen / unchanged)
- **FROZEN PLANE BOUNDS:** world bounds from POINTS ONLY (min/max over all 506 + 6% pad) — byte-identical to r6, so the 506 point SVG coordinates never move. Ghost + drill-in are zero-mass ground; they do NOT rescale the plane.
- **Ghost as GLYPHS never regions (§9.2.2):** ghost + drill-in are `<circle>` marks only — no Voronoi, no hatching, no painted boundaries. RIDER-1 continuum discipline; over-claim discipline shared with F-1.
- **GRAVEYARD (F-1):** 37 per-corpse tombstones with cause-of-death labels; never danger shading. Death classes: extrinsic-content-mix:3, extrinsic-itemization:7, extrinsic-no-lever:4, extrinsic-split-scaling:3, extrinsic-tuning:7, intrinsic-red:12, system-evidence:1.
- **Two skins, one layout engine:** ghost coordinate+status fingerprint identical across skins (MATCH); point fingerprint identical (MATCH). Skins vary only ink/opacity chrome; the 23-vertex hull, drill-in glyphs, and ledger are one code path.
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal (verified across separate process invocations).

## Provenance law
chart = render(atlas-edition2.json). No number/label/coordinate originates outside an atlas-edition2.json
field. Layout is computed; content is not. Edition-II honors this: the ghost hull's 23
vertices + beyond-horizon N=0 are COMPUTED from the emitted Edition-II field (the
computed-not-constant law pays off across the edition boundary); the pull-slice / drill-in / off-plane /
superseded / P-DF-1 numerals are all rendered from emitted fields; the drill-in glyph field is emitted
pre-aggregated and re-aggregated by the frozen projection. Content-locked disclosure copy (pole glosses,
horizon label, beyond-horizon sentence, off-plane disclosure) is carried VERBATIM. The renderer computes
layout; it never invents content.

## Acceptance tests
- [PASS] **point-counts** — active=469 (exp 469), supp=37 (exp 37), total=506 (exp 506)
- [PASS] **grouped-count** — grouped=86 (exp 86)
- [PASS] **ghost-counts** — feasible=11160 (== emitted meso_feasible 11160), sealed=1314 (== emitted meso_sealed 1314)
- [PASS] **ghost-lit-conformance** — feasible lit=true 193 == emitted lit_cells 193
- [PASS] **ghost-depth-sum** — Σdepth=767,411,820 == depth_sum_check 767,411,820 == denom 767,411,820
- [PASS] **sealed-cut_id-conformance** — all 1314 sealed cut_ids in {L1-,L2-}: L1-treatment-function-coherence, L2-summon-implies-proxy
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
- [PASS] **r3.2-clip-disclosure** — clip line present both skins (count=27, from render pass; all clipped cells unlit=true)
- [PASS] **r3-coverage-callout** — active 469 + denom 767,411,820 present both skins
- [PASS] **r3-sealed-ledger** — sealed 1,314 + cut ids [L1-treatment-function-coherence, L2-summon-implies-proxy] present both skins
- [PASS] **ghost-glyphs-not-regions** — ghost is <circle> glyphs; no polygon/pattern/region fills
- [PASS] **fit-layer-regression** — instrument: point-circles BYTE-FROZEN (469/469), tombstones BYTE-FROZEN (37/37), fit-explainer-strings PRESENT | archive: point-circles BYTE-FROZEN (469/469), tombstones BYTE-FROZEN (37/37), fit-explainer-strings PRESENT
- [PASS] **r4-horizon** — envelope=true, exact-label=true, computed-not-constant: removed extreme drill corner @ (1.9200,-2.0800) ×1; charted hull CHANGED (canonical 23 vtx)
- [PASS] **r4-headline-pair** — lead present=true, ratios match indep (lit 1.7%, density 2.4)=true, 693M in secondary only=true
- [PASS] **r5-beyond-horizon** — charted N=0 (indep=0, expected=0); beyond-line-omitted(zero-case)=true; charted-reach-line-present=true; computed-not-constant: added east kit @ (2.5,-2.3): BEYOND_N 0→1; beyond line appears both skins=true; meso-cross-check N=14==14=true
- [PASS] **E2-belowplane-ledger-band** — footer@plane-right(1504.00)=true; zero-occlusion(true) [instrument: below-plane-plaques=0(want 0), max-data-mark-y=825.4<=1112=true | archive: below-plane-plaques=0(want 0), max-data-mark-y=825.4<=1112=true]; full-strings-in-title=true
- [PASS] **register-v1.2-derivation** — denom Σdepth=767,411,820==exact 767,411,820==sum_check 767,411,820 (true); meso 11,160+1,314==raw 12,474 (true); L1 756+L2 558==1314 (true); register=feasibility-cuts-register-v1.2, new_law=0, halt=false
- [PASS] **lattice-integrity** — depthΣ==exact(true); lit 193==emitted 193(true); off-plane N=94 disclosed(true); unmapped 108 enumerated(true)
- [PASS] **pull-slice-lit-integrity** — lit-pull-cores==tuples(true); re-keys d3-zbarb+di-cyclone exist & non-mcd(true); mcd-on-plane=0 → ZERO mcd-lit(true); doctored HALT(a) mcd-forced=true(code 2); doctored HALT(b) new-law=true(code 2)
- [PASS] **drill-in-conformance** — EAST-half PARENTS (region "EAST-half (projected x>=0; PERFORM side) — slate #1 ES + #2 EN (one drill-in serves both)"=true, 5,068 parents, projected-x>=0=true); sub-cells overshoot west 10,232/38,878 glyphs (P-DF-1 displacement mechanism — EXPECTED, not gated); sub-sealed Σ10,136==10,136(true); RED-3-@drill-in rendered(true); RED-3-NOT@meso(true); doctored HALT meso-RED3=true(code 2); doctored HALT drill-bogus=true(code 2)
- [PASS] **P-DF-1-scored** — verdict=PASS (top-level=PASS, consistent=true); falsified=false; S_max=2.84105203 > K_max=1.87424756; mechanism-consistent=true
- [PASS] **edition-stamp+anti-stale-greps** — edition-stamp(II + v1.2)=true; Edition-I denoms only-in-lineage=true; 422445240-absent=true; content-locked-strings-verbatim=true
- [PASS] **E2.1-b-drill-prominence-floor** — radius floor: min drill r=1.37px (>=1.30, was 0.75)=true; log₂ step monotone (1.37<1.44<1.63)=true; radius order drill<ghost all mult=true; contrast: instrument: drill C=1.179(floor 1.12, hit=true) < ghostDark 1.246 < ghostLit 2.086, order=true | archive: drill C=1.323(floor 1.2, hit=true) < ghostDark 1.343 < ghostLit 2.228, order=true
- [PASS] **E2.1-c-banner-relabel** — leads-with-chart-edition+basis-demoted=true; old "Edition 1 · frozen" lead gone=true; locked substrings verbatim=true
- [PASS] **E2.1-d-provenance-dedupe** — instrument: edition-token-count=1 (want 1) [Edition-II×1, "·Edition II"×0] | archive: edition-token-count=1 (want 1) [Edition-II×1, "·Edition II"×0]
- [PASS] **E2.1-e-skin-canvas-map** — instrument→{light,#f7f8fa}=true; archive→{dark,#0e1016}=true; skins-not-renamed(instrument,archive)=true
- [PASS] **E2.1-f-chrome-uniqueness+bottom-band-overlap** — chrome-uniqueness(each visible string ×1 both skins)=true; below-band+footer zero-bbox-overlap=true
- [PASS] **r7-restyle-regression** — geometry byte-frozen vs e21 (fb951b39); whitelist=fill+layer-g-ids+data-hooks+pole-relayout+horizon-z. instrument: points(469)=FROZEN tombs=FROZEN ground(46005)=FROZEN hull=FROZEN | archive: points(469)=FROZEN tombs=FROZEN ground(46005)=FROZEN hull=FROZEN
- [PASS] **r7-overlap-zero** — instrument: axis∩plot=0 rail-viol=0 locked-missing=0 axis-mutual=0 | archive: axis∩plot=0 rail-viol=0 locked-missing=0 axis-mutual=0
- [PASS] **r7-hooks-integrity** — instrument: live 383/383=true cond 86/86=true grave 37/37=true classed 506/506=true ghost 46006/46006=true layers-missing=none badKit=none badCore=none badMember=none | archive: live 383/383=true cond 86/86=true grave 37/37=true classed 506/506=true ghost 46006/46006=true layers-missing=none badKit=none badCore=none badMember=none
- [PASS] **r7-hooks-doctored-halt** — injected data-kit="zz-ghost-kit-not-emitted" (absent from atlas-edition2.json) → integrity check REJECTS (computed-not-blind)

## Smoke tests
- [PASS] **WHIRLWIND x>0 (PERFORM)** — x=0.8191
- [PASS] **WHIRLWIND y<0 (EMBODY)** — y=-1.0816
- [PASS] **TOTEM-SENTRY x<0 (DEPLOY)** — x=-0.7307
- [PASS] **charged-dash near WHIRLWIND condensation** — poe1-charged-dash dist=0.209 (< 0.848 = 20% diag)
- [PASS] **all lit ghost glyphs inside plane frame (not clipped)** — 192 lit glyph positions, all in-frame=true
- [PASS] **coincident-projection aggregation active** — max multiplicity=8 (aggregated 11160 cells -> 7128 glyph positions)
- [PASS] **ghost hull is a small polygon** — hull vertex count=23
- [PASS] **CHARTED horizon east reach EXCEEDS settled kits (P-DF-1 realized)** — charted hull east x=2.3100 > settled-active east x=1.3903 (+0.9197) [meso-only east was 1.2581 < settled 1.6276]
- [PASS] **headline lit-fraction ≈ 1.7% (Edition-II)** — lit fraction=1.7% (193/11160)
- [PASS] **headline density ≈ 2.4 kits/cell** — density=2.4 (469/193)
- [PASS] **meso-hull beyond-N == 14 (frozen receipt, §9.5.1)** — meso-hull N=14 active kits beyond the MESO-only reach
- [PASS] **CHARTED-hull beyond-N == 0 (drill-in encloses settled kits)** — charted-hull N=0 active kits beyond the charted reach
- [PASS] **meso-beyond group profile (10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral)** — WHIRLWIND=10, CHANNELED-BEAM=3, NEUTRAL=1 (CHANNELED-BEAM:3, NEUTRAL:1, WHIRLWIND:10)
- [PASS] **point-in-charted-hull: ALL actives INSIDE (N==0)** — 0 beyond / 469 active = 0.0% (the charted horizon encloses the whole settled archipelago)
- [PASS] **E2 below-plane ledger header present** — ledger header rendered below plane
- [PASS] **E2 footer census at plane right edge** — census end-anchor x=1504.00 == plane-right 1504.00
- [PASS] **E2 drill-in subordinate ground rendered** — 38,878 emitted glyph-field entries → 38,878 aggregated drill glyphs (Σmult=172,312)
