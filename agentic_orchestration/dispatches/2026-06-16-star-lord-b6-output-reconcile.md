# Dispatch — 2026-06-16 — star-lord — EXCISE b6 output references + reconcile MIGRATION

**From:** knight-rider
**To:** star-lord (output / export / telemetry seam)
**Approved by:** Matt 2026-06-16 (relayed via gandalf dispatch to KR). **SETTLED — do NOT route back for design pushback or re-validation.**
**Estimated effort:** ~2–3 hours (b6 excise in season_writer + MIGRATION reconcile + smoke)
**Acceptance:** `output/season_writer.py` no longer emits/branches on b6; `export/MIGRATION.md` reconciled with the upstream sim + generation deletions; season export round-trips clean without the b6 path. jack-ryan Gate-2 two-witness passes.

## Context — settled deletion, not a fork

Matt has RETIRED the 1D battle sim and the b6 archetype processes. The 2D spatial sim is the sole battle simulation; b6 archetype kits are no longer generated. Your seam is the **last leg** of the deletion: remove b6 from the output/export path and reconcile the migration record so the export contract matches the new upstream reality.

## Deletion surface (confirmed on disk; YOU pin exact calls)

### EXCISE b6 references
- `output/season_writer.py` — KR grep confirmed b6 references here. Remove the b6 branch; keep the non-b6 emission path intact.

### RECONCILE
- `export/MIGRATION.md` — reconcile against gamora's `simulation/MIGRATION.md` and rocket's `generation/MIGRATION.md`. Document the export-contract effect: b6 archetype no longer appears in season JSON; any fields keyed on the retired 1D-sim/proxy-1D path removed or redirected to the spatial path.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**YES — cross-seam, downstream end.** You consume from simulation (gamora) and generation (rocket). **Read BOTH `simulation/MIGRATION.md` and `generation/MIGRATION.md` FIRST** — they author before you. Your job is to make the export contract honest about the deletions, not to invent new contract. If a season-JSON field is now orphaned by the 1D-sim deletion, remove it and note in `export/MIGRATION.md`.

**Telemetry note:** the spatial sim has its own telemetry (`simulation/spatial_gauntlet/spatial_telemetry.py` — gamora's). Confirm season export reads from the spatial telemetry path, not any deleted 1D telemetry surface. If there's a dangling 1D-telemetry read in your seam, excise it.

## Sequencing across seams
1. gamora — FIRST (kernel + balance_loop rewire + MIGRATION.md).
2. rocket — SECOND (generation b6 delete + MIGRATION.md).
3. **star-lord (you) — THIRD / LAST.** Read both MIGRATIONs; excise output b6; reconcile export MIGRATION.
4. jack-ryan Gate-2 across the full set.

If either upstream MIGRATION isn't on disk when you start, surface the sequencing gap — do NOT self-author the upstream contract. Hold until they land.

## Out of scope (do NOT do)
- Do NOT touch simulation or generation files.
- Do NOT add proxy telemetry export for the forward-work proxy cycle — that is a SEPARATE dispatch sequenced after this deletion.
- Do NOT re-run any prove-then-delete probe.

## Tag intent
`star-lord/v1.1-b6-output-reconcile` (seam-prefixed).

## Gate
jack-ryan Gate-2 on the deletion commits (two-witness: clean-build + season-export-round-trips-green). gandalf design-endorse NOT required (Matt-settled).
