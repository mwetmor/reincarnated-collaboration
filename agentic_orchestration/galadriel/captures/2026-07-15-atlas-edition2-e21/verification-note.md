# The Atlas of Kits — EDITION II · FIX PASS (E2.1) verification note

**EDITION II FIX PASS — E2.1 (2026-07-15, spec §10.8).** Presentation-only iteration on FROZEN
Edition-II data (`atlas-edition2.json` READ-ONLY). Fired by Matt's two rulings on the ebb18784
render + gandalf's DRIFT-CRITIC verify findings. An edition changes the LATTICE; an rN or a fix-pass
discloses/corrects chrome + presentation on existing ground. The FIT layer (basis + 469 point coords
+ 37 tombstones + fit-explainer) stays BYTE-FROZEN vs r6 AND vs ebb18784.

**The six fixes (spec §10.8 a-f):**
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

**Rendered by:** galadriel/pipeline/atlas-edition2-e21-render.mjs (deterministic; no wall-clock — all stamps from atlas-edition2.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas-edition2.json (elrond; gandalf audit-grade ACCEPT — READ-ONLY this pass)
**FIT-layer freeze baselines:** r6 (2026-07-15-atlas-edition1-r6-legibility) AND ebb18784 (2026-07-15-atlas-edition2) — points + tombstones byte-identical to BOTH (independently verified)
**Pre-fix record (untouched):** 2026-07-15-atlas-edition2 (ebb18784)
**atlas_version:** Edition-II · **edition:** II · **iteration:** E2.1 · **register:** feasibility-cuts-register-v1.2
**basis frozen:** 2026-07-14 · **inertia:** 8.36% · **retained dims:** 14
**emitted_at (from atlas):** 2026-07-15T19:20:12.237153+00:00 · **emitter:** agentic_orchestration/research/scripts/build_atlas_json_edition2.py

## Acceptance tally
- **ACCEPTANCE: 37/37 PASS** (0 fail) · **SMOKE: 17/17 PASS**
- **P-DF-1 VERDICT: PASS** (S_max 2.84105203 > K_max 1.87424756; falsified=false) — top-level mirror `p_df_1_verdict`=PASS. NOT falsified — the registered prediction holds; INTERIOR-1 stays closed (no new fuel).
- **Edition-II suite (22-28) + re-instantiated priors (§7/§9): all covered.** Priors 1-18 re-run against
  Edition-II artifacts; the three intra-edition frozen-layer regressions (r2/r3.2/r5) are RETIRED across
  the edition boundary (§10.4.3) and REPLACED by acceptance 23 (fit-layer-regression vs r6). r4-horizon +
  r4-headline-pair + r5-beyond-horizon re-instantiate (computed-not-constant, edition-safe). r6 legibility
  criteria adapt to the below-plane ledger band (`E2-belowplane-ledger-band`).

## Outputs
- instrument: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-e21/atlas-edition2-instrument.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-e21/atlas-edition2-instrument.png`
- archive: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-e21/atlas-edition2-archive.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-e21/atlas-edition2-archive.png`

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
- [PASS] **E2-belowplane-ledger-band** — footer@plane-right(1504.00)=true; zero-occlusion(true) [instrument: below-plane-plaques=0(want 0), max-data-mark-y=1051.9<=1112=true | archive: below-plane-plaques=0(want 0), max-data-mark-y=1051.9<=1112=true]; full-strings-in-title=true
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
