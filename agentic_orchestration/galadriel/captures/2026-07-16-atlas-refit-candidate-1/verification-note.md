# Build Horizon — Refit Candidate 1 · UNRATIFIED COMPARISON ARTIFACT · verification note (r2)

> **THIS IS NOT AN EDITION.** It is a comparison plate for Matt's Tier-3 atlas refit **adoption decision**
> (Refit Candidate 1 — a full re-derivation of the FIT on the 628-active corpus — vs the served **Edition III**).
> The served truth (`atlas-edition3.json`) is **byte-untouched**; the interactive `/atlas` still serves it.
> The candidate reaches Matt as **static plates** (interactivity follows adoption, not precedes it). Nothing
> here is ratified. **Authority:** Matt 2026-07-16 "I want to see both versions so we cna make a decision."
> · gandalf briefs `2026-07-16-galadriel-a-render-refit-candidate-plates-brief.md` (r1) +
> `2026-07-16-galadriel-rerender-refit-plates-ledger-fix-brief.md` (r2, ledger-honesty fix).
> **r2 input:** post-fix `atlas-refit-candidate-1.json` at elrond commit **1cd7d1d0** (SHA-256 `758126a8bc55f7ee…`).

**emitted alongside:** atlas-edition3.json (served truth; Matt comparison pending)
**comparison note (emitted):** Full re-derivation of the atlas FIT on the current 628-active corpus (incl. 62 Lost Ark + pull/MELEE as live feature columns). Same pre-registered methodology, same seed 20260714. Edition III served truth is byte-untouched. This is the number surface for Matt's adoption decision (Refit Candidate 1 vs Edition III); see refit-candidate-1-comparison-report.md.

## The three laws that frame this plate

1. **Comparison, not edition.** Title reads **"Build Horizon — Refit Candidate 1"** (no "Edition" word). The
   strings "Edition IV"/"edition4" appear NOWHERE. "Edition III" appears ONLY in the emitted_alongside
   provenance line (the served-truth reference), never as this plate's own identity (anti-stale grep enforced).
2. **Plane ALIGNED to Edition-I orientation — disclosed.** Every plane coordinate (points, ghost cells,
   drill-in, hull, p_df_1) is Q-aligned to Edition-I orientation via in-plane orthogonal Procrustes (rotation+reflection), no scaling, no translation (rotation
   **-117.3477°**, det **-1**, no scaling, no translation; fit on 469 shared actives).
   The refit plane rotated ~117° + reflected vs Edition-I; reflection-only alignment was insufficient (raw
   dim1 same-index corr 0.044576). Distances/spreads/congruence/gates/plane-inertia are
   **Q-invariant**; only the arbitrary MCA/SVD orientation convention changes. **Per-axis inertia is NOT
   rendered** (the aligned x/y are not pure dims 1/2); the **plane-level 8.903%** corrected inertia IS
   rendered (subspace-invariant). Disclosed in the banner + headlined here.
3. **Poles = Edition-I REFERENCE orientation.** The refit basis carries NO ratified axis names
   (`basis.axis_names` is a {note} object). The four poles render as Edition-I reference labels
   (PERFORM/DEPLOY/LAUNCH/EMBODY, each marked **"(E1 ref)"**) + the gloss "poles = Edition-I reference
   orientation; refit axes unratified". They are never presented as the candidate's own ratified identities.

## Structure (apples-to-apples with Edition III)

- **Furniture byte-verbatim** from the FINAL FIXED r8-furniture head (`944afa98`) — Matt compares STRUCTURE,
  not presentation. The FURN factor table, BUILD FAMILIES key, ledger form, both skins carried unchanged.
- **Plane bounds** re-derived from the candidate's OWN points (points-only + 6% pad law) — the candidate has
  its own honest frame; Edition III's bounds are NOT forced.

## Render vs emission cross-check (RECOMPUTE + CROSS-CHECK — the load-bearing part)

The head recomputes the hull, the beyond-horizon N, and the P-DF-1 mechanism per its standing law and
**MATCHES the emitted `ghost_field.p_df_1`** (a mismatch is a finding → HALT, never a tolerance):

- **P-DF-1 VERDICT: PASS** — S_max **1.90823161** > K_max **1.15472813**; falsified=**false**; n_beyond_horizon_kits **13**.
- **beyond-MESO-hull N (render pass) = 13** == emitted `p_df_1.n_beyond_horizon_kits` **13** ✓ (HALT-guarded at module load).
- **charted-hull beyond-N (render pass) = 0** — the charted horizon (meso ∪ drill-in) encloses the whole settled archipelago (§10 census: all overshoot EAST-side, charted-hull beyond-N=0).
- **depth Σ = 767,411,820** == `depth_sum_check` **767,411,820** == exact_post_red_law **767,411,820** (byte-equal to Edition-III's — the lattice did not move).
- **drill-in:** Σmultiplicity **122,544** == `n_sub_feasible` **122,544**; sub-sealed Σ **6,624** == `n_sub_sealed` **6,624**; parent cells **3,312**.

## What changed vs r1 (r2 — ledger-honesty fix)

r1 rendered against `da992f78`; r2 renders against the POST-FIX emission (`1cd7d1d0`, gandalf spot-verify green). The fix (elrond, per gandalf's RULING) touched exactly TWO ghost-field ledgers; everything else about the JSON (points, coords, drill_in, p_df_1, plane_alignment, lattice, depth Σ) is byte-identical to `da992f78` (verified: remainder-hash equal). The render deltas:

1. **Footer ledger re-sourced (2 lines).** `off_plane_corpus` was STALE (byte-carried from Edition III: it declared 94 mcd gear-grain kits off-plane, but those 94 are ADMITTED on-plane in the refit). It now carries honest values (`gate_rejected_keyed 0`, `n = |kits| = 26` — the no-cell-key rows) + a grain-admission `disclosure`. The off-plane ledger line now numbers the truthful **26** and renders that disclosure VERBATIM (hover). `unmapped_pending_curation` (114) was NOT stale — the count is TRUE (lit-map census); a `disclosure` semantics field was added so "unmapped" reads as lit-map-census, not off-plane. Its verbatim disclosure now rides the feasible-line `<title>` + an inline "(lit-map census — on-plane)" gloss.
2. **Gating assert #24 RETUNED.** The old form hardcoded `offN === offPlaneN && offPlaneN === 94` — the honest emission broke it. Replaced with INTERNAL-consistency form (constants-vs-computed law): `off_plane_corpus.n === |kits|` · `gate_rejected_keyed` present · disclosure rendered verbatim. NO hardcoded census numeral (not re-pinned to 26).
3. **NEW STANDING acceptance check** (permanent, fail-loud): *ledger-vs-points consistency* — `set(off_plane_corpus.kits) ∩ set(points[].kit_id) == ∅` (off-plane means OFF-plane) · `unmapped_pending_curation` count == list length (NO disjointness assert — its members are legitimately on-plane) · every count field == its list length · every footer census string rendered matches its JSON source. This is the render-side twin of elrond's emission-side assert. A violation die()s — a ledger that contradicts its own points must never reach a plate again.
4. **r1 tension RESOLVED.** The r1 "mcd on-plane vs off-plane ledger" observation was a TENSION (CHANGED, surfaced for Matt); r2 reports it PASS — the emission was corrected, the 94 are admitted on-plane, the ledger↔coords now agree.

Full r1 re-pointed acceptance set re-ran green (determinism byte-equal, counts 628+37=665, depth Σ 767,411,820, hull/P-DF-1 render-vs-emitted cross-check, anti-stale greps) PLUS the retuned #24 PLUS the new standing check. Everything else on the plate — furniture, bounds, skins, banner, "(E1 ref)" pole labels, per-axis-inertia ban, alignment disclosure — is UNCHANGED from r1.

## Acceptance tally (re-pointed set)

- **ACCEPTANCE: 42/42 PASS** (0 fail) · **SMOKE (gating): 10/10 PASS** · **gating overall: ALL PASS**.
- **Acceptance adaptation (per brief):** frozen-baseline checks **RETIRED** (fit-freeze vs r6/e21; basis==edition2 assert; N==469/506; Edition-III lit/census constants; edition-stamp greps; edition===3). Internal-consistency checks **RE-POINTED** to the candidate's own emitted counts (fail-loud). Hull/census/P-DF-1 **RECOMPUTED + CROSS-CHECKED** vs emitted (mismatch = HALT). Edition-I orientation smokes **DEMOTED** to reported observations (below). Anti-stale greps added.

## Demoted observations (REPORTED, NOT gating)

These are refit-dependent (the plane was re-derived + Q-aligned). A **CHANGED** flag does NOT fail the run —
it is comparison evidence. **3 CHANGED** (the refit legitimately moved these).

| observation | refit value | Edition-I / Edition-III expectation | flag |
|---|---|---|---|
| mcd- gear-grain: on-plane, ledger admits (r2 fixed) | 94 mcd- kits ON-plane as active points; off_plane_corpus.gate_rejected_keyed=0 (none keyed-then-rejected), disclosure ADMITS the 94 on-plane, n=26 no-key rows genuinely off-plane — ledger↔coords CONSISTENT | Edition-III: 0 mcd- on-plane (94 held off-plane); r1: ledger claimed 94 off-plane while coords on-plane (TENSION, now fixed) | **PASS** |
| WHIRLWIND x>0 (E1 ref PERFORM side) | x=0.6475 | E1-orientation: x>0 | **PASS** |
| WHIRLWIND y<0 (E1 ref EMBODY side) | y=-0.6274 | E1-orientation: y<0 | **PASS** |
| TOTEM-SENTRY x<0 (E1 ref DEPLOY side) | x=-0.2760 | E1-orientation: x<0 | **PASS** |
| charged-dash near WHIRLWIND condensation | dist=0.131 (thr 0.843 = 20% diag) | E1: dist < 20% diag | **PASS** |
| all lit ghost cells inside candidate frame | 1 lit cell(s) just outside points-derived frame (of 202 lit glyphs); DISCLOSED on clip line | Edition-III (frozen E1 frame): 0 lit outside | **CHANGED** |
| headline lit-fraction vs Edition-III | 1.8% (202/11160) | Edition-III: 1.8% (202/11,160) | **PASS** |
| headline density vs Edition-III | 3.1 (628/202) | Edition-III: 2.3 (469/202) | **CHANGED** |
| meso-hull beyond-N (== emitted p_df_1) | 13 (== emitted p_df_1.n_beyond_horizon_kits 13) | Edition-III: 14 | **PASS** |
| meso-beyond group profile | NEUTRAL:10, WHIRLWIND:3 | Edition-III: WHIRLWIND:10, CHANNELED-BEAM:3, NEUTRAL:1 | **CHANGED** |

## Outputs

- instrument (LIGHT): `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-16-atlas-refit-candidate-1/atlas-refit-candidate-1-instrument.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-16-atlas-refit-candidate-1/atlas-refit-candidate-1-instrument.png`
- archive (DARK): `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-16-atlas-refit-candidate-1/atlas-refit-candidate-1-archive.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-16-atlas-refit-candidate-1/atlas-refit-candidate-1-archive.png`

## Provenance law

chart = render(`atlas-refit-candidate-1.json`). No number/label/coordinate originates outside an
`atlas-refit-candidate-1.json` field. Layout is computed; content is not. The ghost hull's
**25** vertices + beyond-horizon N are COMPUTED from the emitted candidate field and
cross-checked against the emitted p_df_1; the pull-slice / drill-in / off-plane / P-DF-1 numerals are all
rendered from emitted fields; the drill-in glyph field is emitted pre-aggregated and re-aggregated by the
frozen projection. Content-locked disclosure copy is carried VERBATIM. **atlas_version:** Refit-Candidate-1 ·
**edition:** Refit-Candidate-1 · **register:** feasibility-cuts-register-v1.3 · **basis frozen:** false (unratified) ·
**plane inertia:** 8.903% · **retained dims:** 17 · **emitted_at:** 2026-07-16T16:33:42.447042+00:00 ·
**emitter:** agentic_orchestration/research/scripts/build_atlas_refit_candidate_1_json.py. Determinism: sorted iteration; no RNG; no wall-clock; re-render byte-equal.

## Acceptance tests
- [PASS] **point-counts** — active=628 (exp 628, emitted 628), supp=37 (exp 37, emitted 37), total=665 (exp 665, emitted 665)
- [PASS] **grouped-count** — grouped=86 (== labelled gateA members 86; exp 86)
- [PASS] **ghost-counts** — feasible=11160 (== emitted meso_feasible 11160), sealed=1314 (== emitted meso_sealed 1314)
- [PASS] **ghost-lit-conformance** — feasible lit=true 202 == emitted lit_cells 202
- [PASS] **ghost-depth-sum** — Σdepth=767,411,820 == depth_sum_check 767,411,820 == denom 767,411,820
- [PASS] **sealed-cut_id-conformance** — all 1314 sealed cut_ids in {L1-,L2-}: L1-treatment-function-coherence, L2-summon-implies-proxy
- [PASS] **point-layout-equality** — identical point coordinate fingerprint
- [PASS] **ghost-layout-equality** — identical ghost coord+status fingerprint (both skins)
- [PASS] **determinism** — instrument:byte-equal, archive:byte-equal
- [PASS] **R2-no-2.57-numeral** — clean (naive-box 2.57 absent as content)
- [PASS] **R2ext-no-422445240** — clean (superseded denominator absent)
- [PASS] **R3-no-season-N** — clean
- [PASS] **RIDER-1-badge** — inertia_pct=8.903 + retained_dims=17 + structure_statement present both skins
- [PASS] **r2-pole-glosses** — all 4 pole glosses present both skins
- [PASS] **r2-density-legend-line** — density-field legend line present both skins
- [PASS] **r2-derivation-gloss** — derivation gloss present both skins
- [PASS] **r3-census-line** — mandatory census line present both skins
- [PASS] **r3.2-clip-disclosure** — clip line present both skins (total=287: 1 LIT + 286 unlit, from render pass; DISCLOSED honestly — lit cell(s) just outside the candidate's own points-derived frame, not rescaled)
- [PASS] **r3-coverage-callout** — active 628 + denom 767,411,820 present both skins
- [PASS] **r3-sealed-ledger** — sealed 1,314 + cut ids [L1-treatment-function-coherence, L2-summon-implies-proxy] present both skins
- [PASS] **ghost-glyphs-not-regions** — ghost is <circle> glyphs; no polygon/pattern/region fills
- [PASS] **fit-layer-internal-consistency** — RETIRED r6/e21 byte-freeze (new fit). Internal-consistency: point-circles skin-invariant=true (628==628 actives), tombstones (37==37 supp), fit-explainer-strings=true
- [PASS] **r4-horizon** — envelope=true, exact-label=true, computed-not-constant: removed extreme drill corner @ (1.2400,1.8400) ×1; charted hull CHANGED (canonical 25 vtx)
- [PASS] **r4-headline-pair** — lead present=true, ratios match indep (lit 1.8%, density 3.1)=true, 693M in secondary only=true
- [PASS] **r5-beyond-horizon** — charted N=0 (indep=0, expected=0); beyond-line-omitted(zero-case)=true; charted-reach-line-present=true; computed-not-constant: added east kit @ (2.5,-2.3): BEYOND_N 0→1; beyond line appears both skins=true; meso-cross-check N=13==emitted-p_df_1(13)=true
- [PASS] **E2-belowplane-ledger-band** — footer@plane-right(1504.00)=true; zero-occlusion(true) [instrument: below-plane-plaques=0(want 0), max-data-mark-y=1015.3<=1112=true | archive: below-plane-plaques=0(want 0), max-data-mark-y=1015.3<=1112=true]; full-strings-in-title=true
- [PASS] **register-v1.3-derivation** — denom Σdepth=767,411,820==exact 767,411,820==sum_check 767,411,820 (true); meso 11,160+1,314==raw 12,474 (true); L1 756+L2 558==1314 (true); register=feasibility-cuts-register-v1.3, new_law=0, halt=false
- [PASS] **lattice-integrity** — depthΣ==exact(true); lit 202==emitted 202(true); off-plane n=26==|kits| 26(true) gate_rejected_keyed=0 present(true) disclosure-verbatim(true); unmapped 114 enumerated(true) semantics-verbatim(true)
- [PASS] **ledger-vs-points-consistency (standing, r2)** — off-plane∩points=∅ (0 on-plane in off-list; true); unmapped count 114==|kits| 114(true), 114/114 on-plane (correct, NOT asserted disjoint); off n 26==|kits| 26(true); census-strings-verbatim both skins (off true, unmapped true)
- [PASS] **pull-slice-lit-integrity** — lit-pull-cores==tuples(true); re-keys d3-zbarb+di-cyclone exist & non-mcd(true); doctored HALT(a) mcd-forced=true(code 2); doctored HALT(b) new-law=true(code 2); [mcd-on-plane=94, gate_rejected_keyed=0 — see DEMOTED observation for the ledger↔coords agreement]
- [PASS] **drill-in-conformance** — EAST-half PARENTS (region "EAST-half (projected x>=0; PERFORM side) — slate #1 ES + #2 EN (one drill-in serves both)"=true, 3,312 parents, projected-x>=0=true); sub-cells overshoot west 4,396/31,451 glyphs (P-DF-1 displacement mechanism — EXPECTED, not gated); sub-sealed Σ6,624==6,624(true); RED-3-@drill-in rendered(true); RED-3-NOT@meso(true); doctored HALT meso-RED3=true(code 2); doctored HALT drill-bogus=true(code 2)
- [PASS] **P-DF-1-scored** — verdict=PASS (single-source); falsified=false; S_max=1.90823161 > K_max=1.15472813; mechanism-consistent=true; values-match-brief-targets(S=1.90823161,K=1.15472813,n=13)=true
- [PASS] **refit-identity+anti-stale-greps** — Edition-IV/edition4-absent=true; Edition-III-only-in-emitted_alongside=true; refit-stamps(title+unratified-banner+alignment-disclosure+v1.3)=true; content-locked-strings-verbatim=true
- [PASS] **E2.1-b-drill-prominence-floor** — radius floor: min drill r=1.37px (>=1.30, was 0.75)=true; log₂ step monotone (1.37<1.44<1.63)=true; radius order drill<ghost all mult=true; contrast: instrument: drill C=1.179(floor 1.12, hit=true) < ghostDark 1.246 < ghostLit 2.086, order=true | archive: drill C=1.323(floor 1.2, hit=true) < ghostDark 1.343 < ghostLit 2.228, order=true
- [PASS] **refit-banner-lead** — leads-with-UNRATIFIED-framing=true; no edition-stamp lead=true; locked substrings (alignment+plane-inertia) verbatim=true
- [PASS] **refit-provenance-dedupe** — instrument: version-token "Refit-Candidate-1"×1 (want 1), edition-token-leak×0 (want 0) | archive: version-token "Refit-Candidate-1"×1 (want 1), edition-token-leak×0 (want 0)
- [PASS] **E2.1-e-skin-canvas-map** — instrument→{light,#f7f8fa}=true; archive→{dark,#0e1016}=true; skins-not-renamed(instrument,archive)=true
- [PASS] **E2.1-f-chrome-uniqueness+bottom-band-overlap** — chrome-uniqueness(each visible string ×1 both skins)=true; below-band+footer zero-bbox-overlap=true
- [PASS] **geometry-skin-invariance** — RETIRED e21 byte-freeze (new fit). Skin-invariant geometry: points(628)=IDENTICAL tombs=IDENTICAL ground(41477)=IDENTICAL hull=IDENTICAL
- [PASS] **r7-overlap-zero** — instrument: axis∩plot=0 rail-viol=0 locked-missing=0 axis-mutual=0 | archive: axis∩plot=0 rail-viol=0 locked-missing=0 axis-mutual=0
- [PASS] **r7-hooks-integrity** — instrument: live 542/542=true cond 86/86=true grave 37/37=true classed 665/665=true ghost 41531/41531=true layers-missing=none badKit=none badCore=none badMember=none | archive: live 542/542=true cond 86/86=true grave 37/37=true classed 665/665=true ghost 41531/41531=true layers-missing=none badKit=none badCore=none badMember=none
- [PASS] **r7-hooks-doctored-halt** — injected data-kit="zz-ghost-kit-not-emitted" (absent from atlas-edition3.json) → integrity check REJECTS (computed-not-blind)

## Smoke tests (gating)
- [PASS] **coincident-projection aggregation active** — max multiplicity=2 (aggregated 11160 cells -> 10080 glyph positions)
- [PASS] **ghost hull is a small polygon** — hull vertex count=25
- [PASS] **CHARTED horizon east reach EXCEEDS settled kits (P-DF-1 realized)** — charted hull east x=2.0000 > settled-active east x=1.2035 (+0.7965) [meso-only east was 1.3395 < settled 1.2035]
- [PASS] **headline lit-fraction re-derived (candidate counts)** — lit fraction=1.8% (202/11160)
- [PASS] **headline density re-derived (candidate counts)** — density=3.1 (628/202)
- [PASS] **CHARTED-hull beyond-N == 0 (drill-in encloses settled kits)** — charted-hull N=0 active kits beyond the charted reach
- [PASS] **point-in-charted-hull: ALL actives INSIDE (N==0)** — 0 beyond / 628 active = 0.0% (the charted horizon encloses the whole settled archipelago)
- [PASS] **below-plane ledger header present (candidate identity)** — ledger header "Refit Candidate 1 lattice" rendered below plane
- [PASS] **footer census at plane right edge** — census end-anchor x=1504.00 == plane-right 1504.00
- [PASS] **drill-in subordinate ground rendered** — 31,451 emitted glyph-field entries → 31,451 aggregated drill glyphs (Σmult=122,544)
