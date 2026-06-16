# Dispatch — 2026-06-16 — gamora (lead) + rocket — Convergence retirement (recompose machinery + ARCHETYPE_TEMPLATES/TIER_SCALING/BIAS)

**From:** knight-rider
**To:** gamora (lead — owns balance_loop recompose machinery) + rocket (generation-side ARCHETYPE_TEMPLATES consumers)
**Approved by:** Matt 2026-06-16 (ruling 2: "Convergence retirement, own forward dispatch, sequenced — queued, not deferred-forever. Remove balance_loop's recompose machinery + the ARCHETYPE_TEMPLATES/TIER_SCALING/BIAS consumers. Delete it all.").
**Status:** ⏸️ QUEUED — sequenced; NOT yet fired. **Carries a COORDINATION GATE with BC-cutover Stage 3 (below) — resolve before firing.**
**Estimated effort:** ~1–1.5 day (math-note on convergence impact + recompose-machinery removal + generation-consumer cleanup + full-season validation + Gate-2)
**Acceptance:** balance_loop's recompose secondary loop is gone; `ARCHETYPE_TEMPLATES` / `TIER_SCALING_BANDS` / `BIAS_PREFERRED` / `BIAS_PENALIZED` have no remaining consumers and are deleted; a full season generates + simulates end-to-end through the 2D spatial path with no recompose loop; engine green.

## Context
The B14.5 recompose secondary loop consults `ARCHETYPE_TEMPLATES`/`TIER_SCALING_BANDS`/`BIAS_*` (from `generation/b6_archetype_templates.py`) at `simulation/balance_loop.py:2426`. Matt has ruled the recompose machinery part of the retired b6 archetype processes. **Retiring it changes convergence for every class** — this is a balance change, so math-note-first (Disc #1) + full-season validation + Gate-2 + gandalf endorse (convergence shape is experiential).

## ⚠️⚠️ COORDINATION GATE — `ARCHETYPE_TEMPLATES` is ALSO the BC-cutover Stage-3 deletion target
CHANGELOG 2026-06-14: BC-coordinate-identity cutover **Stage 3** "physically deletes `ARCHETYPE_TEMPLATES`/`ARCHETYPE_ROLE_PRIORITY`/`_PLAYER_CONTROLLER_ARCHETYPES`/`legacy_archetype_shim`/V-D1..V-D6." That stage is HELD/pending (`2026-06-14-rocket-bc-coordinate-cutover-stage-3.md`). **This dispatch and BC-Stage-3 target the SAME symbol from opposite seams.** They MUST be reconciled before either fires — options KR will pin with Matt:
- (a) MERGE: fold BC-Stage-3's ARCHETYPE_TEMPLATES deletion into this convergence-retirement dispatch (one coordinated removal).
- (b) ORDER: convergence-retirement removes the balance_loop consumer first, BC-Stage-3 removes the generation consumers + the definition last.
Do NOT double-author the deletion. Generation-side ARCHETYPE_TEMPLATES consumers (`class_generator`, `archetype_composer`, `bc_target_source`, `stat_allocator`, `skill_tree`, `weapon_identity`, `composed_kit_adapter`) overlap heavily with BC-cutover scope — confirm which belong to this dispatch vs. BC-Stage-3.

## Scope (gamora lead)
- Remove balance_loop's recompose secondary-loop machinery + the `:2426` import.
- Math-note the convergence-shape impact BEFORE code (which classes shift, by how much, against the spatial sim).
- Full-season end-to-end validation through the 2D spatial path with no recompose loop.

## Scope (rocket)
- After the BC-Stage-3 coordination is pinned: remove/coordinate the generation-side `ARCHETYPE_TEMPLATES`/`TIER_SCALING`/`BIAS` consumers; delete the definitions in `b6_archetype_templates.py`.
- When this + AOE-reconciliation have removed the last consumer, **physically delete `b6_archetype_templates.py`** (the tail of whichever lands last).

## Gate
math-note Gate-1 (jack-ryan, convergence-impact) → Gate-2 (clean-build + full-season-spatial-green + convergence-shape within ruled tolerance) → gandalf endorse (experiential convergence shape).

## Sequencing
QUEUED after the b6-gen deletion + AOE-reconciliation, AND after the BC-Stage-3 coordination decision. Do not fire blind.
