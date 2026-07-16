# elrond charge — Tier-3 REFIT CANDIDATE 1: full re-derivation on the 628-active corpus (Lost Ark + pull live)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Authority:** Matt 2026-07-16 (verbatim): *"Let's keep Edition 3, and then run the full Tier 3 with Last Ark and Pull/Gravity. It's important that we get this right, and I want to see both versions so we cna make a decision."*
**Ultra-think record:** `agentic_orchestration/gandalf/notes/2026-07-16-tier3-refit-and-polish-spec.md` (read §§1–3 first)
**Charter law:** `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §6–§7 — this is a **comparison EXPERIMENT, not an Edition.** The string "Edition IV"/"edition4" appears NOWHERE in code, artifacts, stamps, or logs. Naming: **`Refit-Candidate-1`** / `atlas-refit-candidate-1.*` / scripts `*_refit_candidate_2026_07_16.py`.

## Iron laws

1. **Edition III is read-only.** No write touches `atlas-edition3.json`, `atlas.json`, `atlas-edition2.json`, the frozen-fit CSV, or any served artifact. The candidate emits ALONGSIDE.
2. **Same methodology, grown corpus.** Fork `agentic_orchestration/research/scripts/atlas_derivation_2026_07_14.py` → `atlas_refit_candidate_2026_07_16.py`. The pre-registered method (MCA indicator SVD, Greenacre correction, MFA block weighting, FUSE_MIN=10, MASK set, parallel-analysis retention, SEED=20260714, gates A–D) is UNCHANGED. If the grown corpus forces a methodology deviation → HALT + surface; never improvise.
3. **The lattice does not move.** Register v1.3 denominators (767,411,820 exact / 11,160 meso / 1,314 sealed / pull 1,080+54) byte-identical. The refit changes the FIT layer only. Corpus census unchanged — zero new rows this pass.

## R0 — game-code normalization (your parked to-do, now load-bearing)

Active set carries long-form codes that orphan against `FRANCHISE_ROLLUP` (stage-0 would HALT): `lost-ark` (62 active), `diablo-4` (1), `diablo-3` (1), `diablo-immortal` (1). Normalize `canon_corpus.game` → short codes `la` / `d4` / `d3` / `di` (matches kit_id prefixes + existing rollup convention). Idempotent migration script + your curation-log convention. Post-assert: every distinct `game` in the active set is short-code. (`mcd` is already its short code — leave.) Also sweep non-active rows for the same long forms so the table converges on one convention; log counts.

## R1 — fork the derivation

Changes vs the 2026-07-14 script — ONLY these:

- Stage-0 N assertion: re-derive expected N from the predicate first (recon says **628**); assert against YOUR derived number, report it.
- `FRANCHISE_ROLLUP` += `"la": "LostArk"`, `"mcd": "mcd"`. If stage-0 still finds an orphan game → HALT + surface (don't silently extend).
- **PULL pre-assert:** function=pull count among actives ≥ FUSE_MIN. Recon says exactly **10 = FUSE_MIN** — zero margin. If it would fuse, the run's purpose dies → HALT + surface. Do NOT lower FUSE_MIN.
- Melee: per-field parse (function vs delivery vs range — never LIKE; recon's `%|melee|%` hit 271 via range collisions). Report delivery=melee active count; if ≥10 it earns a fit column organically (no special-casing) — flag it, since it may partially close the MELEE ghost-image collapse downstream.
- Gate-A labels: same 86-kit CSV; assert all 86 present in the active set (they are).
- Output paths → refit-candidate names, written alongside in `agentic_orchestration/research/curated/atlas/`.
- **Gates A–D re-run and REPORT** (old thresholds): they are EVIDENCE for Matt's adoption decision, not emission blockers. A gate failure does not halt emission; it goes in red ink at the top of your report.
- Runtime: N grew 1.34× — the permutation/bootstrap/Leiden/LCA stages will take longer. Run the single entrypoint, capture the full report; be patient, don't trim iteration counts.

## R2 — supplementary projection (graveyard)

Project the projectable negatives (recon: still **37**) into the NEW retained space via the same CA supplementary transition formula → refit tombstone coordinates. Re-assert the count.

## R3 — ghost field, refit basis

Fork the ghost-field module (edition3 wraps edition2 — fork at the machinery level, `ghost_field_refit_candidate_1.py`): project the SAME register v1.3 lattice through the NEW basis column coordinates. **Un-mask `pull`** (it now has a fit column — the fit2reg function image becomes real). If delivery=melee earned a column, un-mask it likewise and report the unmapped/off-plane count change. Lit census read live (unchanged corpus). Denominators asserted byte-identical to v1.3.

## R4 — emit

`atlas-refit-candidate-1.json` — **schema-compatible with `atlas-edition3.json`** (same top-level keys: `basis` / `counts` / `loadings` / `points` / `ghost_field` / `register_ref` + stamps) so galadriel's render fork consumes it with minimal changes. Stamps: `atlas_version: "Refit-Candidate-1"`, `ghost_field.edition: "Refit-Candidate-1"`, an explicit `unratified_comparison_artifact: true` field, `emitted_alongside: "atlas-edition3.json (served truth; Matt comparison pending)"`. Counts: active 628 / supplementary 37 / total 665. Also emit `refit-candidate-1-coordinates.csv` (kit_id, x, y, game, gateA_group, supplementary) for diffing.

## R5 — comparison report (THE decision surface)

`agentic_orchestration/research/curated/atlas/refit-candidate-1-comparison-report.md`, numbers only (I synthesize the reading):

1. Procrustes congruence + RMS displacement (plane-diameter-normalized) on the 469 shared actives vs their Edition-I coordinates (`atlas-coordinates-active.csv`); top-20 movers table (kit_id, old xy, new xy, distance).
2. Axis identity: post-alignment correlation of refit dim1/dim2 vs Edition-I dim1/dim2 — the "did the axes survive?" numbers.
3. Inertia + retained-dims comparison (parallel-analysis outcome vs Edition I).
4. LA landings: the 4 Destroyer skill-grain kits each with 5 nearest active neighbors; the 58 class-grain kits summarized (centroid, spread, which gateA/condensation neighborhoods they fall into).
5. The 10 pull kits at honest coordinates: pairwise spread — do they cohere as a region?
6. Fuse-table delta: levels fused at 469 but un-fused at 628 (and vice versa).
7. Gates A–D: Edition-I values vs refit values, PASS/FAIL both columns.
8. Ghost-field deltas: pull-lit cells masked→honest coordinate shift; unmapped/off-plane count changes.
9. Six condensation (gateA) centroid shifts.

## R3-ADDENDUM — drill-in + beyond-horizon on the refit plane (gandalf, same day, Matt follow-up: "will this automatically account for live kits beyond the meso horizon and the drill-in?")

What recomputes automatically in your fork: lattice re-projection, lit census, the ghost-horizon hull (computed-not-constant), beyond-horizon membership (all actives vs the NEW hull), P-DF-1 re-scoring (û from refit loadings). What does NOT: the **drill-in region pin.** `build_drill_in` is pinned to "EAST-half (projected x≥0; PERFORM side) — slates #1 ES + #2 EN" — an Edition-I empirical choice, not a general densify-where-kits-overshoot algorithm. Therefore:

1. **Axis-sign alignment (methodology-neutral, MANDATORY before region-pinned machinery):** MCA/SVD axis sign is arbitrary. Align refit dim1/dim2 SIGNS to Edition-I orientation by max-|correlation| (pure reflection; never a rotation of the fit). Report the alignment applied. Without this, "EAST-half x≥0 = PERFORM side" can silently mean the opposite side of the refit plane.
2. **Drill-in fork runs the pinned EAST-half region VERBATIM** (like-for-like mechanics; promoted vocabulary auto-follows the refit fit's geometry+commit column levels — report any vocabulary delta from fusing changes).
3. **R5 gains section 10 — beyond-horizon census on the refit plane:** N beyond-horizon kits (Edition-era baseline: 14) + full kit list with positions + per-quadrant/per-direction overshoot breakdown (max overshoot distance + direction) + coverage verdict: does the EAST-half drill-in still cover the û overshoot (P-DF-1 verdict as evidence), and is there overshoot in directions the pinned region does NOT cover (enumerate — this is the input to a possible drill-in-expansion pass).
4. **Do NOT design new drill-in slates in this pass.** The census report decides whether the candidate plate needs a drill-in-expansion pass before Matt's comparison — gandalf's call at the verify gate.

## Return contract

- Paths of everything (scripts, JSON, CSV, report, migration log) + a numbers-first summary in your return text (≤40 lines).
- Auto-commit the collab repo (scripts + artifacts + logs; corpus.db stays gitignored — the migration LOG is the record). **NO push.**
- HALT conditions: unexpected orphan game · pull fuses · any write to an edition3/served artifact · methodology deviation required · gate machinery errors (as opposed to gate FAILs, which report).
