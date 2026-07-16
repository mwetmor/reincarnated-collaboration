# elrond charge — R3-ADDENDUM completion on Refit Candidate 1 (axis-sign alignment · verbatim drill-in · P-DF-1 · §10 beyond-horizon census)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Follows:** elrond's completed Tier-3 run (commit a087bfbd — R0–R5 verified PASS at gandalf's gate).
**Why this charge exists:** the original brief gained an **R3-ADDENDUM** (commit 994a1d4c, Matt follow-up: *"will this automatically account for live kits beyond the meso horizon and the drill-in?"*) AFTER the Tier-3 agent forked it — the addendum did not execute (verified: no `drill_in`, no `p_df_1`, no hull/census fields in `atlas-refit-candidate-1.json`; no §10 in the report; no alignment record). This charge completes it. Read the addendum verbatim: `agentic_orchestration/gandalf/briefs/2026-07-16-elrond-tier3-refit-candidate-brief.md` § R3-ADDENDUM.

## Iron laws (unchanged)

1. **Edition III + every served artifact READ-ONLY.** You touch ONLY refit-candidate artifacts + your fork scripts.
2. **No "Edition IV"/"edition4" anywhere.**
3. **Pure reflection, never rotation.** The refit is its own honest fit; alignment fixes the ARBITRARY MCA/SVD sign convention only.
4. **Lattice byte-identical** (v1.3 denominators re-asserted).

## A — axis-sign alignment (FIRST; everything downstream keys on it)

- On the 469 shared actives: `corr(E1_dim1, refit_dim1)` and `corr(E1_dim2, refit_dim2)` — RAW coordinates (`atlas-coordinates-active.csv` E1-frozen vs `refit-candidate-1-coordinates-active.csv`), NOT Procrustes-transformed.
- If a dim's corr < 0 → flip that dim's sign EVERYWHERE in the emitted artifacts: point x/y, loadings column coords, ghost-cell projected coords (feasible + sealed), pull/melee honest-coord tables, supplementary tombstone coords, and every coordinate CSV. Consistency assert: re-check corr post-flip > 0.
- If |corr| < 0.10 for either dim → HALT + surface (sign not determinable; don't guess). Expected from your §2: dim1 ≈ 0.64, dim2 ≈ 0.27 — both determinable.
- Stamp the JSON: `axis_sign_alignment: {dim1: {corr_before, flipped}, dim2: {corr_before, flipped}, rule: "reflection-only, max-|correlation| to Edition-I orientation"}`.
- Re-emit `atlas-refit-candidate-1.json` + all refit CSVs aligned. Then RE-RUN the comparison script so §§4/5/8/9 printed raw coordinates match the emitted artifact. State in the report: Procrustes/distance/spread numbers are reflection-invariant (unchanged); gates are fit-structure quantities (unchanged, not re-run).

## B — drill-in fork, region pin VERBATIM (after A)

- Fork the Edition-III drill-in machinery → refit version. Region pin verbatim: **"EAST-half (projected x>=0; PERFORM side)"** — meaningful only post-alignment.
- Promoted pair **geometry×commit**; the promoted vocabulary auto-follows the REFIT fit's geometry+commit column levels (your §6: `aura` un-fuses in the refit → the geometry promoted set gains a level vs Edition-III). **Report the vocabulary delta** (`promoted_geometry_levels` / `promoted_commit_levels` refit vs Edition-III lists).
- Do NOT design new slates or move the region — comparability law; expansion is gandalf's call at the verify gate.
- Emit `ghost_field.drill_in` with the EXACT Edition-III key set (schema-compatible — galadriel's render head consumes these): `emission_note, local_first_law, n_east_parent_cells, n_sub_feasible, n_sub_sealed, promoted_pair, promoted_geometry_levels, promoted_commit_levels, red3_surfaces_here, region, seal_enum, sub_feasible_glyph_field, sub_feasible_glyph_field_bin_dp, sub_feasible_glyph_field_n_distinct, sub_feasible_hull_n_vertices, sub_feasible_hull_reach, sub_sealed_ledger`.
- RED-3 seals surface at drill-in grain ONLY (same law + doctored-proof convention as Edition-III).

## C — P-DF-1 re-score

- Replicate the Edition-III `p_df_1` û construction VERBATIM against REFIT loadings (û = normalize(mean(c_whirlwind, c_channel)) as the machinery defines those column vectors). If a referenced column is absent or fused differently in the refit vocabulary such that the construction cannot run verbatim → **HALT + surface**, never improvise a substitute column.
- Emit `ghost_field.p_df_1` with the Edition-III key set: `K_max_beyond_horizon, S_argmax, S_max, consequence_if_falsified, falsified, n_beyond_horizon_kits, prediction, statement, u_direction, verdict`.

## D — report §10: beyond-horizon census on the refit plane (append to `refit-candidate-1-comparison-report.md`)

1. **Hulls (computed-not-constant, both variants like Edition-III):** meso-only hull AND charted hull (meso feasible ∪ drill-in sub-feasible), from the aligned refit ghost field.
2. **Beyond-horizon membership:** ALL 628 actives (not just the 469) vs each hull. Report: N beyond meso-hull (Edition-era baseline: 14) · N beyond charted-hull (Edition-III baseline: 0) · full kit list with positions + gateA/franchise · per-quadrant AND per-direction overshoot breakdown (max overshoot distance + direction).
3. **Coverage verdict:** does the EAST-half pinned drill-in cover the overshoot (P-DF-1 verdict as evidence)? **Enumerate any overshoot in directions the pinned region does NOT cover** — this list is the direct input to gandalf's drill-in-expansion decision.
4. NO recommendations, numbers only — gandalf synthesizes.

## Return contract

- Paths of everything; ≤30-line numbers summary: alignment corrs + flips applied · vocabulary delta · n_sub_feasible / n_sub_sealed · P-DF-1 verdict (S_max vs K_max) · meso-hull beyond-N · charted-hull beyond-N · uncovered overshoot directions (or "none").
- Auto-commit collab repo. **NO push.**
- HALT conditions: |corr| < 0.10 either dim · û construction breaks on refit vocabulary · any write to a served/edition3 artifact · lattice denominator drift.

**Signed:** gandalf — addendum enforcement at the verify gate, as recorded in the ultra-think note §3.

---

## RULING at the verify gate (gandalf, 2026-07-16 — after item-A HALT, commit 90f839de)

**Finding (elrond, correct HALT):** raw same-index corrs on the 469 shared: dim1 **+0.0446** (< 0.10 tripwire), dim2 +0.4277; cross-term |E1_d1×refit_d2| = 0.6697 — off-diagonal dominant. Optimal orthogonal refit→E1 map = **reflection + ~117° rotation (det = −1)**. The plane rotated; axes approximately swapped. Reflection-only alignment cannot anchor it.

**Ruling — item A is amended to A′ (in-plane orthogonal alignment, disclosed):**

1. Compute the optimal **orthogonal 2×2 map Q (det ±1, NO scaling, NO translation** — both fits are barycenter-origin) minimizing ‖E1 − refit·Q‖² over the 469 shared actives.
2. Apply Q to EVERY plane coordinate in the emitted artifacts: all 665 point coords, the plane coords of every loadings column category, all ghost-cell projected coords (feasible + sealed), pull/melee honest-coord tables, tombstones, every CSV. One transform, everywhere, atomically.
3. Post-alignment sanity assert: the same-index corr matrix becomes diagonal-dominant (report before/after matrices).
4. Stamp the JSON `plane_alignment: {method: "in-plane orthogonal Procrustes (rotation+reflection), no scaling", Q, rotation_deg, det, raw_corr_before, corr_after, rationale: "refit plane rotated ~117°+reflected vs Edition-I; reflection-only insufficient (raw dim1 corr 0.045); aligned for plate comparability; disclosed on-plate + reported as headline structure evidence"}`. (Replaces the `axis_sign_alignment` stamp.)
5. Items B/C/D then run VERBATIM in the aligned frame (EAST-half x≥0 pin, P-DF-1 û from aligned loadings, census in aligned frame + the frame-invariant Ns stated as such).
6. Report §2 gains the raw corr matrix + rotation angle + det as explicit numbers; §10 census unchanged in scope.

**Why this does not violate the no-rotation principle's purpose:** the law existed to prevent disguising the fit's own structure to force agreement. Distances, spreads, congruence, gates, inertia-of-plane are ALL invariant under Q; only the orientation convention (already arbitrary in MCA) changes; the rotation is disclosed on the plate and headlined in the report. Raw-axes plates would hide the geography comparison Matt ordered. Alignment here EXPOSES the rotation finding; it does not bury it.

**Invariance notes (assert, don't assume):** plane corrected-inertia 8.903% is a subspace property — invariant under Q; the per-dim split (5.15/3.75) does NOT apply to the aligned x/y and must not be rendered per-axis. P-DF-1 is internally consistent iff points, loadings, hull all carry the SAME Q.
