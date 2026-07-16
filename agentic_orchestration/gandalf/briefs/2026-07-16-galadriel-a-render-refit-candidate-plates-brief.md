# galadriel charge — A-render: Refit-Candidate-1 plates from the R8 furniture head (+ side-by-side composite) — STAGED

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Status:** FIRED — both gates CLEAR at gandalf's verify:
- **Gate 1: CLEAR** — B-1 fix landed (key-box hug corrected in `atlas-edition3-r8-furniture-render.mjs` `944afa98`; r8 head FINAL; v1.14 promoted).
- **Gate 2: CLEAR** — elrond addendum landed (`da992f78`: `atlas-refit-candidate-1.json` re-emitted ALIGNED, carrying `ghost_field.drill_in` + `ghost_field.p_df_1` + `plane_alignment`; gandalf artifact-level verify green).
- **Drill-in-expansion decision (gandalf, at this gate):** NOT NEEDED — §10 census: all 13 beyond-meso kits EAST-side (inside the pinned region's coverage), WEST 0, charted-hull beyond-N = 0. Comparability law satisfied; render proceeds.

**Authority:** Matt 2026-07-16 (verbatim): *"I want to see both versions so we cna make a decision."* · Ultra-think record: `agentic_orchestration/gandalf/notes/2026-07-16-tier3-refit-and-polish-spec.md` §3.

## The one law that frames everything

**This is a COMPARISON plate, not an Edition.** Title: **"Build Horizon — Refit Candidate 1"**. The strings "Edition IV"/"edition4" appear NOWHERE. The banner leads with the unratified framing (source the exact wording from the JSON's `comparison_note` / `unratified_comparison_artifact` + `emitted_alongside` stamps — render emitted fields, never invent copy). Footer stamps from `atlas-refit-candidate-1.json`. Edition III and every served artifact are READ-ONLY.

**Alignment disclosure (RULING 2026-07-16, addendum-completion brief; RATIFIED Matt 2026-07-16):** the emitted coordinates are plane-ALIGNED to Edition-I orientation (in-plane orthogonal Procrustes, rotation+reflection, no scaling — the refit plane rotated ~117° + reflected vs Edition-I). The plate MUST disclose this: a banner/gloss line built from the JSON's `plane_alignment` stamp (rotation_deg + det + "aligned to Edition-I orientation for comparison"). **Pole titles:** the refit basis carries NO ratified axis names — render the four poles as Edition-I REFERENCE orientation labels (e.g. `PERFORM → (E1 ref)` styling, your judgment on form) with one gloss stating "poles = Edition-I reference orientation; refit axes unratified." Never render the E1 names as if they were the candidate's own ratified identities. **Per-axis inertia must NOT be rendered** (the aligned x/y are not pure dims 1/2); the plane-level 8.903% figure is fine (subspace-invariant).

## Fork + input

- Fork the FINAL fixed `agentic_orchestration/galadriel/pipeline/atlas-edition3-r8-furniture-render.mjs` → `atlas-refit-candidate-1-render.mjs`.
- **Sole input:** `agentic_orchestration/research/curated/atlas/atlas-refit-candidate-1.json` (post-addendum). Point fields: `kit_id, x, y, franchise, gateA_group, supplementary`. Counts law: **628 active + 37 supplementary = 665** (assert against JSON `counts`, fail-loud).
- **IDENTICAL furniture** — the FURN table carries byte-verbatim from the r8 head (apples-to-apples: Matt compares structure, not presentation). BUILD FAMILIES key, ledger form, skins (`archive`=dark lead / `instrument`=light), all unchanged.
- Plane bounds re-derive from the refit points (the head's own points-only + 6% pad law) — the candidate has its own honest frame; do NOT force Edition-III's bounds.

## Acceptance adaptation (enumerated — the load-bearing part of this charge)

The edition3 head's acceptance/smoke machinery encodes Edition-I/III expectations. For the candidate:

1. **RETIRE (do not run):** every frozen-baseline check — fit-layer byte-freeze vs r6/e21, `basis == atlas-edition2.json[basis]` module-load assert, N==469/506 counts, Edition-III lit/census constants, edition-stamp greps. A NEW fit has no freeze baseline.
2. **RE-POINT (internal consistency, fail-loud):** points-render == JSON coords (628+37); grouped count == labelled gateA members from the JSON; ghost feasible/sealed/lit counts == JSON `ghost_field` fields; depth Σ == `depth_sum_check` == 767,411,820 (the lattice DID NOT move — this one number must equal Edition-III's); drill-in glyph Σmultiplicity == `drill_in.n_sub_feasible`; sub-sealed ledger Σ == `n_sub_sealed`; determinism double-render byte-equal; chrome-uniqueness; below-plane ledger zero-occlusion law.
3. **RECOMPUTE + CROSS-CHECK (computed-not-constant):** ghost hull, beyond-horizon N (meso + charted), P-DF-1 score — the head recomputes per its standing law and must MATCH the emitted `ghost_field.p_df_1` numbers (S_max, K_max, verdict, n_beyond_horizon_kits). Mismatch → HALT + surface (emission vs render disagreement is a finding, not a tolerance).
4. **DEMOTE to REPORTED-not-gating:** the Edition-I orientation smokes (WHIRLWIND x>0 / y<0, TOTEM x<0, charged-dash proximity). The refit rearranges the plane (Procrustes congruence 0.468; WHIRLWIND kits moved up to 50% of diameter) — these are now OBSERVATIONS for the comparison package. Print each with its refit value + old expectation, PASS/CHANGED flag. Do not gate emission on them.
5. **Anti-stale grep (new):** "Edition IV" absent · "Edition III"/"Edition-III" appears ONLY in the `emitted_alongside` provenance line, never as the plate's own identity · refit stamps present both skins.

## Outputs

- `captures/2026-07-16-atlas-refit-candidate-1/atlas-refit-candidate-1-{instrument,archive}.svg` + `.png` + `render-provenance.json` + verification-note (same conventions; note frames it as unratified comparison artifact).
- **Side-by-side composite** per skin: Edition III (final r8 plates) LEFT, Refit Candidate 1 RIGHT, same pixel scale, one labeled PNG each — the first thing Matt sees.
- Crop receipts: title band (candidate identity legible), key, one dense-region crop per plate for point-texture comparison.

## Return contract

≤30 lines: acceptance tally (re-pointed set) · cross-check verdict (render vs emitted p_df_1/hull) · demoted-smoke observations table · paths · commit hash. Auto-commit. **NO push. NO vendoring into glance/app** — the candidate is NOT served; it reaches Matt as static plates in the comparison package (interactivity follows adoption, not precedes it — spec §3).

## HALT conditions

Input JSON missing `drill_in`/`p_df_1`/`plane_alignment` (Gate 2 not actually met) · counts ≠ 628/37/665 · depth Σ ≠ 767,411,820 · render-vs-emission cross-check mismatch · any write to a served/edition3 artifact.

**Signed:** gandalf — my verify gates the comparison package.
