# Dispatch — 2026-06-20 — gamora — Phase 4: Armor/resist symmetry (instrument-validity workstream)

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** Matt 2026-06-20 (autonomous instrument-validity workstream authorization)
**Estimated effort:** quarter-to-half-day (mitigation-side correction)
**Acceptance:** casters mitigate the resist they currently bypass; measure-isolated harness shows caster KPM/boss-survive coming DOWN toward the martial range, against the CURRENT (untouched) bands; math-note-first; jack-ryan Gate-2 clean.

## Authoritative spec
This is **Phase 4** of the gandalf-authored instrument-validity workstream. Read it IN FULL first:
`agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (§2 spine, §3 Phase-4 detail + GATE G5, §5 cautions).

## Context & PARALLELISM
This is the **mitigation-side** defect — confirmed via the Arm-C diagnostic STOP: armor/resist is asymmetric, casters ate ~zero resist, inflating caster bands and boss survive+kill (toward the implausible ~0.99). It is **selector-independent** and runs in **PARALLEL** with the offense-side chain (Phases 1–3). To avoid working-tree conflicts with the concurrently-running Phase 1, **this dispatch executes in an isolated git worktree of the engine repo** (KR provisions the worktree; you work on its branch). Your code edits land there; harness-result JSONs land in the collab repo as usual. KR merges your branch back to `main` before Phase 5.

## Math-before-code (Discipline #1 — REQUIRED FIRST)
Author `simulation/math/<...>-phase4-armor-resist-symmetry-2026-06-20.md` BEFORE the fix:
- Identify the exact asymmetry in code (where martial damage eats armor but caster damage bypasses resist, or whichever direction the asymmetry runs) — cite locations.
- Pre-compute the expected magnitude of the caster-side correction (how much resist they will now eat) and the expected direction of the band-delta.
- Cite code locations for every claim (Discipline #1.2).

## The work (recompose-first)
Correct the armor/resist asymmetry so casters mitigate the resist they currently bypass — symmetric with how martial damage is already mitigated by armor. **Recompose-first: activate/symmetrize the existing mitigation path; do not invent a new mitigation model.** Touch `damage_resolver.py` / `spatial_engine.py` mitigation as needed.

## Measure-ISOLATED (load-bearing, brief §5)
- **Do NOT touch** `ENCOUNTER_COHORT_KPM_BAND` or the production gate. Bands stay as-is so the mitigation-shift is visible against the CURRENT bands. Refit is Phase 5 only.
- Run on a **fresh disjoint seed base** (Discipline #3; avoid `[700000,766703]`, `[619000,684303]` AND whatever Phase 1 claims — coordinate seed base with KR so the four phases stay disjoint).
- **Semantic-shift declaration (Discipline #12):** mitigation changes the meaning of every caster KPM/DPS/boss-survive field. Declare the boundary.

## GATE G5 (AFTER measure) — report against this pre-registration
Expected: caster clear-room KPM should **DROP** (they now eat resist); caster boss survive+kill should fall from the inflated ~0.99 toward the martial range. **Report your result against this.** KR auto-resolves if caster numbers come down toward martial.
- **Flag to KR ONLY IF:** martial numbers MOVE (they already ate resist — they shouldn't shift → fix touched the wrong path), OR symmetry OVER-corrects (casters now BELOW martial → over-mitigation).

## Cross-seam contract change? (Principle 6 gate)
Mitigation is INTERNAL to the simulation seam. If any telemetry/fight_log field crossing gamora→star-lord changes, write `MIGRATION.md` per ADR-004. If not, note that explicitly.

## Out of scope (do NOT do)
- No band refit (Phase 5 only).
- No offense-side work (resource/rotation/DoT — separate dispatches).
- No over-reach beyond symmetrizing the armor/resist mitigation.

## Hand-back
Append a completion record: branch name + tag, math-note path, harness results path, G5 self-assessment vs the table, MIGRATION.md status, notes for jack-ryan Gate-2.
