> 🔄 **SUPERSEDED-BY-CONSOLIDATION 2026-06-16.** gandalf's path audit collapsed the b6-stack deletion into one outright-delete plan. The AOE turn-off is now Phase 1 of `2026-06-16-b6-stack-outright-deletion.md` (Matt's AOE-Gate preserved there). Do NOT execute this standalone. Retained as historical record.

# Dispatch — 2026-06-16 — rocket (+ gamora hand-off) — AOE-membership reconciliation → delete AOE_GEOMETRIES

**From:** knight-rider
**To:** rocket (lead — owns `geometry_derivation.py`) + gamora (hand-off — re-points the 2 live spatial consumers)
**Approved by:** Matt 2026-06-16 (ruling 1: "AOE reconciliation, own dispatch, carries a Gate"). **SETTLED scope; the canonical-membership *content* is the open question this dispatch resolves.**
**Estimated effort:** ~0.5 day (membership ruling + geometry_derivation reconcile + 2-consumer re-point + symbol delete + smoke)
**Acceptance:** a single canonical AOE-membership source lives in `geometry_derivation.py`; the 4 disputed geometries have a Matt/Gate-ratified disposition; the 2 live spatial consumers read the canonical source; `AOE_GEOMETRIES` is deleted from `b6_archetype_templates.py`; engine imports + spatial sim green.

## Context
With the b6 kit-generation path deleted (`2026-06-16-rocket-b6-archetype-deletion.md`), `AOE_GEOMETRIES` (defined `generation/b6_archetype_templates.py:385`) is an orphaned-but-live frozenset still consumed by the surviving spatial sim. Matt: **"do not delete AOE_GEOMETRIES until resolved."** It must first be promoted to a canonical home with a ratified membership, then its consumers re-pointed.

## The membership dispute (confirmed on disk — at least 3 divergent AOE-geometry frozensets)
- `generation/b6_archetype_templates.py:385` — `AOE_GEOMETRIES` (the shared one the sim consumes)
- `generation/b6_kit_builder.py:825` — `_AOE_GEOMETRIES_FOR_PRIMARY` (likely deleted with b6_kit_builder; capture its membership before deletion)
- `generation/composed_kit_adapter.py:149` — `_AOE_GEOMETRIES` (live, non-b6 generation path)

**Step 1 — rule canonical membership.** Diff the three frozensets; the "4 disputed geometries" are the entries that disagree across them. Author a math/decision note proposing the canonical AOE-membership set with rationale per disputed geometry. **This is a canonical decision → jack-ryan Gate-1 (DESIGN-MODE) before implementing** (decisions-log candidate). gandalf consult OPTIONAL if any disputed geometry has experiential/skill-feel implications.

**Step 2 — reconcile `geometry_derivation.py`.** Make `geometry_derivation.py` the single canonical AOE-membership authority. `composed_kit_adapter._AOE_GEOMETRIES` collapses to read it.

**Step 3 — re-point the 2 live spatial consumers (gamora).** Both in simulation:
- `simulation/damage_resolver.py` (import :33; uses :459, :502 for pack-proxy AOE mult)
- `simulation/combatant.py` (:693)
Re-point both to the canonical source. gamora hand-off via MIGRATION; coordinate so the pack-proxy multiplier behavior is preserved (or any change is intentional + Gate-noted).

**Step 4 — delete `AOE_GEOMETRIES`** from `b6_archetype_templates.py`. (The file itself is deleted only when convergence-retirement also removes the ARCHETYPE_TEMPLATES tables — see that dispatch.)

## Cross-seam contract change? YES
rocket reconciles geometry_derivation (generation); gamora re-points 2 simulation consumers. Both write/append their MIGRATION. star-lord's `geometry_derivation` reference in `season_writer.py` (grep hit) — verify export contract unaffected.

## Gate
**Carries a Gate (Matt-specified):** jack-ryan Gate-1 on the canonical-membership ruling (decisions-log) → jack-ryan Gate-2 on the reconciliation commits (clean-build + spatial-sim-green, pack-proxy AOE behavior preserved-or-intentionally-changed).

## Sequencing
QUEUED after `2026-06-16-rocket-b6-archetype-deletion.md` (which deletes b6_kit_builder — capture its frozenset membership first). Independent of convergence-retirement EXCEPT both must land before `b6_archetype_templates.py` is physically deleted.
