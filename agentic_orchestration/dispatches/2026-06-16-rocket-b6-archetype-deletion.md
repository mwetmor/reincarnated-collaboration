# Dispatch — 2026-06-16 — rocket — DELETE the b6 archetype processes (generation seam)

**From:** knight-rider
**To:** rocket (generation seam)
**Approved by:** Matt 2026-06-16 (relayed via gandalf dispatch to KR). **SETTLED — do NOT route back for design pushback or re-validation.**
**Estimated effort:** ~0.5 day (deletion + branch excise + sidecar cleanup + smoke)
**Acceptance:** the b6 archetype generator is gone; the b6 branch is excised from the kit-composition path; the modules' non-b6 function is intact; generation produces kits end-to-end without the b6 path; engine imports + runs. jack-ryan Gate-2 two-witness passes.

## Context — settled deletion, not a fork

Matt has RETIRED the b6 archetype processes alongside the 1D battle sim. Debate is closed. b6 was "the tier-completeness net" measured through the 1D sim — and the 1D-measured premise is exactly what is being retired. **Your own `b6-deletion-prereq-A-thin-pool-stress-run` dispatch (2026-06-15) is now MOOTED** — it stress-tested the thin pool to decide whether b6 could be removed. That fork is closed: b6 is removed regardless. Do not re-run it. **This deletion is NOT gated on cond.5, b6-parity, thin-pool-stress, or any prior gate.**

## Deletion surface (confirmed on disk; YOU pin exact file-vs-excise calls)

### DELETE (the b6 archetype generator)
- `generation/b6_archetype_templates.py`
- `generation/b6_kit_builder.py` *(KR grep found this second b6 file — gandalf's dispatch listed only `b6_archetype_templates.py`; you confirm whether `b6_kit_builder.py` is wholly b6-only and deletable, or needs partial excise.)*

### EXCISE the b6 branch (keep each module's non-b6 function)
KR grep for `b6` across generation/foundation hit:
- `generation/composed_kit_adapter.py`
- `generation/d10_kit_constraints.py`
- `generation/ability_grammar.py`
- `generation/archetype_composer.py` *(not in gandalf's list — verify + excise if b6-bearing)*
- `generation/weapon_envelope_composer.py` *(not in gandalf's list — verify + excise if b6-bearing)*
- `generation/class_generator.py` *(not in gandalf's list — verify + excise if b6-bearing)*
- `generation/bc_target_source.py` *(not in gandalf's list — verify; this is BC-coordinate machinery, may legitimately reference b6 in a comment/bridge — judge per-call)*
- `foundation/role_loader.py`

Remove the b6 PATH; keep the modules' non-b6 function. Where a b6 reference is a now-dead label/comment vs. a live branch, judge per-call.

### Engine canonical sidecars (rocket's internal canonical library)
- Remove b6 entries in `canonical/sidecars/atomic_substrate_registry_v1.json`
- Remove b6 entries in `canonical/sidecars/emit_substrate_registry.py`

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**YES — cross-seam.** Removing b6 archetype generation changes the kits generation hands to simulation (gamora) and what flows downstream to output (star-lord). **Read `simulation/MIGRATION.md` (gamora authors it FIRST)** to align on the b6 contract removal, then **write/append `generation/MIGRATION.md`** documenting: b6 archetype kits no longer generated; any loadout dict keys that change shape; sidecar registry entries removed. star-lord reads both before its output excise.

## Sequencing across seams
1. gamora — FIRST (1D kernel + balance_loop rewire + sim-side b6 excise + MIGRATION.md).
2. **rocket (you) — SECOND.** Read gamora's MIGRATION; delete generation b6; write your MIGRATION.
3. star-lord — output b6 excise (reads both MIGRATIONs).
4. jack-ryan Gate-2 across the full set.

If gamora's MIGRATION isn't on disk yet when you start, that's a Mac-side sequencing gap — surface it, don't self-author the sim-side contract. You can begin the unambiguous deletes (`b6_archetype_templates.py`, sidecar entries) in parallel; hold the cross-seam loadout-shape excise until gamora's MIGRATION lands.

## Preserve the design history
If you own any b6 math/design notes, stamp `STATUS: HISTORICAL` (do not delete) — same pattern as the simulation/math/ notes.

## Out of scope (do NOT do)
- Do NOT touch simulation files (gamora's seam) or `output/season_writer.py` (star-lord's).
- Do NOT re-run thin-pool-stress / cond.5 / any prove-then-delete probe.
- Do NOT add proxy SKILLS to chain/skill generation yet — that is the SEPARATE forward-work dispatch (sequenced after this deletion). This dispatch is deletion-only.

## Tag intent
`rocket/v1.1-b6-archetype-deletion` (seam-prefixed).

## Gate
jack-ryan Gate-2 on the deletion commits (two-witness: clean-build + generation-produces-kits-green). gandalf design-endorse NOT required for the deletion (Matt-settled).
