# galadriel charge — RE-RENDER: Refit-Candidate-1 plates after the ledger-honesty fix — STAGED

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Status:** STAGED — fires when the elrond ledger fix lands AND gandalf's spot-verify of the re-emitted JSON is green. **Delta charge:** the r1 charge (`2026-07-16-galadriel-a-render-refit-candidate-plates-brief.md`) carries the full law set and is incorporated by reference; ONLY the deltas below change.

## Why r2 exists

gandalf's verify gate caught two FALSE plate lines on the r1 candidate plates — both sourced honestly by the render head from an emission that was itself stale: `ghost_field.off_plane_corpus` ("94 gear-grain kits (mcd-) held off-plane…" — all 94 are on-plane points) and `ghost_field.unmapped_pending_curation` ("…114 unmapped…" — all 114 on-plane). Render head NOT at fault (law: render emitted fields, never invent copy). elrond re-derived both ledgers emission-side (fix brief: `2026-07-16-elrond-refit-ledger-honesty-fix-brief.md`); the re-emitted `atlas-refit-candidate-1.json` is the sole input.

## Deltas vs the r1 charge (everything else VERBATIM)

1. **Input:** the POST-FIX `atlas-refit-candidate-1.json` (gandalf will stamp the fix commit hash at fire time). All other inputs, the forked head `atlas-refit-candidate-1-render.mjs`, furniture, bounds law — unchanged.
2. **Footer ledger lines re-source** from the fixed fields. The new `off_plane_corpus.disclosure` string renders VERBATIM (it now states: 94 mcd ADMITTED at kit grain / grain ruling OPEN for Matt / 26 no-key rows off-plane). If `unmapped_pending_curation` is 0, render the honest 0 per the head's footer template — do not suppress the line unless the template already drops empty clauses; never invent copy either way.
3. **NEW STANDING ACCEPTANCE CHECK (lands in the head permanently — this defect class must never reach a plate again):** *ledger-vs-points consistency* — fail-loud asserts before write-out: `set(ghost_field.off_plane_corpus.kits) ∩ set(points[].kit_id) == ∅` · `set(ghost_field.unmapped_pending_curation_kits) ∩ points == ∅` · every count field == its list length · every footer census string rendered on the plate matches the JSON field it sources. This is the render-side twin of elrond's emission-side assert (belt and braces at both seams).
4. **Outputs: SAME capture dir** (`captures/2026-07-16-atlas-refit-candidate-1/`), in-place refresh of plates + composites + crops (git carries r1 — git-is-archive law; Matt sees ONE canonical package dir). `verification-note.md` bumps to r2 with a short "what changed vs r1" (two footer ledger lines; new standing acceptance check; acceptance tally re-run). `render-provenance.json` re-stamps input hash + fix commit.
5. **Acceptance:** the full r1 re-pointed set re-runs (all of it — determinism, cross-checks, counts, depth Σ 767,411,820, anti-stale greps) PLUS the new check in (3). Expect everything green: the fix touched only the two ledger blocks (elrond asserts rest-of-JSON hash unchanged).

## HALT conditions (r1 set, plus)

The re-emitted JSON's non-ledger bytes differ from `da992f78`'s (cross-check against elrond's hash assert — if points/coords/drill_in/p_df_1/plane_alignment moved, STOP: that's an emission-side breach, not a render matter) · the new consistency check fails on the FIXED emission (would mean a third stale field — enumerate, surface, do not render).

## Return contract

≤20 lines: acceptance tally (incl. the new standing check) · the two re-rendered footer lines VERBATIM as they now appear on-plate · confirmation composites/crops refreshed · paths · commit hash. Auto-commit. **NO push. NO vendoring into glance/app.**

**Signed:** gandalf — the package ships only when the plate and its points tell the same story.
