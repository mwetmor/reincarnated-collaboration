# Skill handoff — 2026-06-14 (knight-rider)

## Session focus: BC-coordinate-identity cutover — full three-stage program LANDED + PUSHED

Orchestrated the complete, ratified three-stage BC-coordinate cutover (gandalf §7 design call, Matt-authorized 2026-06-14). The program substitutes the `bc_target` 8-tuple for the legacy `{element}_{role}` archetype label as the shared identity currency across generation↔simulation. **All three stages landed, all gates cleared, pushed to origin (both repos).** The water_mage 1/29 landmine that originated the program is dissolved.

## What the program did (the arc)

- **Stage 1 (rocket, generation):** generation now composes every class FROM `bc_target` via `compose_kit`; `KitConstraintError → 5-skill fallback` structurally removed; `bc_target` first-class on `PlayerClass`; internal legacy-format label bridge (OUTPUT only). PARTIAL — 16/21 elemental coords cutover; 5 physical coords ride resident legacy path (loud-logged) until pool-expansion sub-stage. Tag `rocket/v1.0-bc-coordinate-cutover-stage-1-partial` (`62a18bc`, already on origin pre-session).
- **Stage 2 (gamora, simulation):** AI keys on coordinate bins, not label (`bc_target_role_priority`, takes only the 8-tuple). `ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES` DEMOTED-to-fallback (Matt directive), not deleted. Behavior-preserving on 16 elemental. Tag `gamora/v-bc-coordinate-cutover-stage-2-1` (`f494f5e`, already on origin pre-session).
- **Stage 3 (rocket, deletion — THE GOAL):** NARROW irreversible cut. Pinned set `{G1 ARCHETYPES_FORBIDDEN_CLOSE_RANGE, G9 legacy_archetype_shim}` + co-requisite shim-test block physically deleted (7 files, +113/-388). R-4 noqa corrections. Elemental-path lock now structural. Tag `rocket/v1.1-bc-coordinate-cutover-stage-3` (`695b70f`, pushed this session).

## Gate discipline (prove-then-delete worked exactly as designed)

- Three read-only prereqs cleared before the irreversible cut: gamora zero-label proof (`8ab02c0`, ELEMENTAL_LEAK=0/PHYSICAL_LEAK=0/PASS), drax demo-VFX sweep (`aaab426`, no Pixi coupling breaks), rocket+gamora reference-audits (`5a4005c`/`8ab02c0`) pinning the exact set.
- gandalf consolidated adjudication (`b5af4b9`) reconciled TWO empirically-wrong priors my synthesis surfaced: (1) R-1 — `legacy_archetype_shim` was HELD as physical infra but is dead on both paths → re-ruled DELETE-now; (2) the demoted tables serve only monsters+experimental (a permanent bc_target-absent population) → reframed PERMANENT-HELD, not Stage-3b-deletable. Convening gandalf ONCE for consolidation (not twice) is the gate working.
- **jack-ryan Stage-3 Gate-2: PASS-WITH-AMENDMENTS, no BLOCK** (`72721f6`). Verified at source: deletion is exactly the pinned set, no scope creep; HELD set intact (incl. G7's `balance_loop.py` R-2 cross-seam consumers untouched); behavior-identical (pre/post proof both 0/0/0/PASS); pre-existing 19 `test_range_profile.py` failures confirmed genuinely pre-existing (`git diff 8ab02c0 695b70f -- tests/test_range_profile.py` EMPTY); collection clean (5810/0). Dangling docstrings classified COSMETIC/non-gating.

## Push (Matt authorized "Go on both and Push")

- ENGINE: `f494f5e..695b70f` (Stage-3 tail: cut + both gating audits) + tag `rocket/v1.1-bc-coordinate-cutover-stage-3`. Stage 1/2 tags already on origin.
- COLLAB: `5e36337..72721f6` (gandalf scoping ruling + adjudication, drax sweep, Godot spike brief, gamora audit note, my Stage-3 dispatch, jack-ryan Gate-2 finding).
- Both repos verified 0 unpushed. Dirty cycle-14 telemetry working files untouched (unrelated, pre-existing).

## Deferred / open (carry-forward)

- **Stage 3b (DEFERRED, task #16):** generation-seam-only — delete physical fallback fork machinery (G4 `classify_archetype` / G5 `archetype_composer` / G7 `ARCHETYPE_TEMPLATES` / G8 `B6KitBuilder`). Re-open criterion = physical-pool expansion landing. G7 carries cross-seam HOLD-SIM gate (R-2, `balance_loop.py`).
- **Physical-pool expansion (DEFERRED):** own Matt-gated effort post-Stage-3, own gate (math note + gandalf spec + jack-ryan Gate-2). The 5 physical coords ride legacy until this lands.
- **Doc-only cleanup (task #17, non-blocking):** 4 stale `legacy_archetype_shim.py` docstring pointers (`b6_archetype_templates.py:15,:326`, `archetype_composer.py:15`, `bc_target_composer.py:880`). jack-ryan pre-approved doc-only follow-up per ADR-002. Route to rocket Pattern-A when convenient. `b6_archetype_templates.py:326` removal-banner now ripe.
- **Non-blocking flags awaiting Matt disposition:** task #8 `class_balance_results` energy-calibration aggregate gap (would be v2.18 additive ALTER TABLE + recorder wiring, ADR-006); task #9 pre-existing b11 geometry smoke failure (rocket seam / physical-fork related); A3 calibration gate (separate, generation/shim-side).

## Routing notes for next session

- The 19 `test_range_profile.py` failures are EXPECTED until physical-pool expansion (content assertion `physical_warrior` vs `physical_grappler`, Stage-1 physical deferral). Not a regression — do not chase.
- gandalf also authored a drax Godot vertical-slice spike brief this session (`7f66b1c`) + Synty-Sidekick-goblins monster-roster amend (`5e36337`) — co-briefed with the Pixi sweep (VFX keys on coordinate, never label). Godot is a SPIKE, Pixi remains the live surface.
