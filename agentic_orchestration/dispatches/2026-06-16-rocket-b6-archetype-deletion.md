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

### ⚠️ `b6_archetype_templates.py` is NOT cleanly deletable — surviving sim code imports two shared symbols (gamora finding 2026-06-16, MIGRATION v1.70)

gamora's empirical inspection of the surviving simulation code found `b6_archetype_templates.py` exports two symbols consumed by code that SURVIVES the deletion. A literal "delete the file" breaks the engine at import. Per Matt's own "delete so it still runs" hygiene rule, you must re-home these BEFORE/ATOMIC-WITH deleting the b6 archetype-generation logic:

1. **`AOE_GEOMETRIES` (UNCONDITIONAL re-home).** `simulation/damage_resolver.py:33` has a module-level `from ...b6_archetype_templates import AOE_GEOMETRIES`. This is a **shared AOE-geometry frozenset, NOT b6 archetype handling** — it survives. Re-home it to a non-b6 home (your call — a geometry/foundation module) and update the damage_resolver import. **If you delete `b6_archetype_templates.py` without this, the engine is un-runnable.** This is the load-bearing line.

2. **`ARCHETYPE_TEMPLATES` / `TIER_SCALING_BANDS` / `BIAS_*` (recompose-lever fork — see Matt decision below).** `simulation/balance_loop.py`'s recompose levers (the B14.5 recompose secondary loop) consult these from `b6_archetype_templates.py`. Retiring them **changes convergence for every class** — that is a balance decision, not a kernel deletion, and gamora correctly did NOT touch them.

**Net:** "delete the b6 archetype GENERATOR" ≠ "delete the file." Excise the b6 kit-generation logic; re-home the shared symbols the survivor needs.

## ⚖️ Matt decision gate — recompose levers (resolve BEFORE you delete `b6_archetype_templates.py`)

Two dispositions; KR will pin which one applies before this dispatch fires:
- **(DEFAULT) Recompose levers SURVIVE.** Re-home `ARCHETYPE_TEMPLATES`/`TIER_SCALING_BANDS`/`BIAS_*` out of the b6 file into a surviving home; balance_loop keeps consuming them; convergence UNCHANGED. Delete only the b6 archetype-generation logic + `AOE_GEOMETRIES` re-home.
- **(ALT) Recompose levers RETIRED too** (if Matt rules the recompose loop is part of "b6 archetype processes"). This is a SEPARATE forward dispatch — it changes convergence for every class and needs its own math-note + Gate-2. Do NOT fold it into this deletion unless KR explicitly tells you it's authorized.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**YES — cross-seam.** Removing b6 archetype generation changes the kits generation hands to simulation (gamora) and what flows downstream to output (star-lord). **Read `simulation/MIGRATION.md` § v1.70 (gamora authored it FIRST)** — it carries the `AOE_GEOMETRIES` contract + recompose-lever note. Then **write/append `generation/MIGRATION.md`** documenting: b6 archetype kits no longer generated; `AOE_GEOMETRIES` re-homed to `<path>`; recompose-lever disposition; any loadout dict keys that change shape; sidecar registry entries removed. star-lord reads both before its output excise.

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
