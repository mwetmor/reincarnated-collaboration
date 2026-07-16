# galadriel charge — RE-RENDER: Refit-Candidate-1 plates after the ledger-honesty fix — FIRED

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Status:** FIRED — elrond fix landed (`1cd7d1d0`); gandalf spot-verify ALL GREEN (top-level byte-stable vs `da992f78`; ghost_field delta = exactly {off_plane_corpus replaced, unmapped_pending_curation_disclosure added}; 26∩points=∅; old-94 all on-plane; depth Σ 767,411,820; drill_in/p_df_1 untouched; no Edition-IV strings). Post-fix JSON is the sole input. **Delta charge:** the r1 charge (`2026-07-16-galadriel-a-render-refit-candidate-plates-brief.md`) carries the full law set and is incorporated by reference; ONLY the deltas below change.

## Why r2 exists (AMENDED after elrond's HALT — read the RULING in the fix brief)

gandalf's verify gate flagged two plate lines; elrond's re-derivation (fix brief `2026-07-16-elrond-refit-ledger-honesty-fix-brief.md` + its RULING section) resolved them asymmetrically:

- `ghost_field.off_plane_corpus` ("94 gear-grain kits (mcd-) held off-plane…") — **STALE, FALSE, fixed**: honest values `gate_rejected_keyed: 0`, `n = kits = 26` (the no-key rows), new grain-admission `disclosure` string.
- `ghost_field.unmapped_pending_curation` (114) — **NOT stale; the count is TRUE** (lit-map census: 114 kits lack `fit2reg_movement` mapping; all 114 are nonetheless plotted on-plane). Count + list unchanged; a new `disclosure` semantics field was ADDED so the line can't be misread as "off-plane."

Render head NOT at fault (law: render emitted fields, never invent copy). The re-emitted post-fix `atlas-refit-candidate-1.json` is the sole input.

## Deltas vs the r1 charge (everything else VERBATIM)

1. **Input:** the POST-FIX `atlas-refit-candidate-1.json` (gandalf will stamp the fix commit hash at fire time). All other inputs, the forked head `atlas-refit-candidate-1-render.mjs`, furniture, bounds law — unchanged.
2. **Footer ledger lines re-source** from the fixed fields. The new `off_plane_corpus.disclosure` string renders VERBATIM (it now states: 94 mcd ADMITTED at kit grain / grain ruling OPEN for Matt / 26 no-key rows off-plane). The `unmapped_pending_curation` count (114, TRUE) keeps rendering; its new `disclosure` semantics field renders (or glosses) so "unmapped" reads as lit-map-census, not off-plane — form yours, copy from the emitted field, never invented.
3. **RETUNE gating assert #24** (`atlas-refit-candidate-1-render.mjs` line ~2211): it hardcodes `offN === offPlaneN && offPlaneN === 94` — the honest ledger (gate_rejected_keyed 0; n 26) BREAKS it. Replace the constant with INTERNAL-consistency form (constants-vs-computed law): `off_plane_corpus.n === off_plane_corpus.kits.length` · `gate_rejected_keyed` present · no hardcoded census numbers anywhere in the assert. Do NOT re-pin to 26.
4. **NEW STANDING ACCEPTANCE CHECK (lands in the head permanently — this defect class must never reach a plate again):** *ledger-vs-points consistency* — fail-loud asserts before write-out: `set(ghost_field.off_plane_corpus.kits) ∩ set(points[].kit_id) == ∅` (off-plane means OFF-plane) · `unmapped_pending_curation_kits` count == list length (NO disjointness assert on this one — its members are legitimately on-plane; the lit-map predicate is orthogonal to fit membership) · every count field == its list length · every footer census string rendered on the plate matches the JSON field it sources. This is the render-side twin of elrond's emission-side assert (belt and braces at both seams).
5. **Outputs: SAME capture dir** (`captures/2026-07-16-atlas-refit-candidate-1/`), in-place refresh of plates + composites + crops (git carries r1 — git-is-archive law; Matt sees ONE canonical package dir). `verification-note.md` bumps to r2 with a short "what changed vs r1" (ledger corrections; assert #24 retune; new standing acceptance check; acceptance tally re-run). `render-provenance.json` re-stamps input hash + fix commit.
6. **Acceptance:** the full r1 re-pointed set re-runs (all of it — determinism, cross-checks, counts, depth Σ 767,411,820, anti-stale greps) PLUS the retuned #24 (3) and the new standing check (4). Expect everything green: the fix touched only `off_plane_corpus` + one added disclosure field (elrond asserts rest-of-JSON hash unchanged).

## HALT conditions (r1 set, plus)

The re-emitted JSON's bytes outside the fixed blocks differ from `da992f78`'s (cross-check against elrond's hash assert — if points/coords/drill_in/p_df_1/plane_alignment moved, STOP: that's an emission-side breach, not a render matter) · the new consistency check fails on the FIXED emission (would mean a genuinely stale third field — enumerate, surface, do not render).

## Return contract

≤20 lines: acceptance tally (incl. the new standing check) · the two re-rendered footer lines VERBATIM as they now appear on-plate · confirmation composites/crops refreshed · paths · commit hash. Auto-commit. **NO push. NO vendoring into glance/app.**

**Signed:** gandalf — the package ships only when the plate and its points tell the same story.
