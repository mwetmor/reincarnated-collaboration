# Finding — 2026-06-17 — star-lord-kpm-export-reinterpret

**Reviewer:** jack-ryan
**Severity:** PASS (INFO-level note only)
**Target:** commit `fd770ab`, tag `star-lord/v-kpm-export-reinterpret-1` (not pushed)
**Developer:** star-lord
**Principles applied:** #1 (math-before-code provenance), #3 (cross-seam impact), #4 (decisions-log as truth); Discipline #12 (semantic-shift provenance)

## What I found
The commit reinterprets the KPM export magnitude on `ExportSimCyclingRecord` from rooms/min to mobs/min, discharging my own Gate-2 action item from `2b8b502` (decisions-log ~line 34). I verified it is genuinely docstring/comment-only: isolating the diff to non-comment lines shows the four KPM field declarations (`tier_1_kpm: float`, `tier_2_kpm: float | None = None`, `sg1_kpm_in_band: str | None = None`, `sg1_kpm_observed: float | None = None`) are byte-for-byte unchanged in name, type, default, and ordering — only trailing comments and the class docstring changed. `schemas.py` parses clean post-edit. The six per-shell band pairs cited in the docstring (open_arena [9.90,15.53], chokepoint_corridor [11.65,15.88], magic_pack [6.06,11.43], elite_pack [5.65,10.00], boss_with_adds [2.49,3.78], mini_boss [0.57,3.30]) match the live gamora-wired `ENCOUNTER_COHORT_KPM_BAND` in `gauntlet_sim.py:316-322` exactly, per-shell cohort-replicated across 4 cohorts as documented. star-lord correctly cites `ENCOUNTER_COHORT_KPM_BAND` and NOT the parallel `SPATIAL_ENCOUNTER_KPM_BAND` sibling (the Balanced-only spatial RESOLVE instrument) — no constant-confusion. Upstream anchors §v1.74 (numerator fix) and §v1.76 (band wire-in) both exist in `simulation/MIGRATION.md` and say exactly what's claimed. Smoke arithmetic reproduces: 2.844 ∈ [2.49,3.78] PASS, legacy 69.0 rejects. No consumer breaks: the only engine consumer is `season_exporter.py` (`model_validate`, immune to comment changes); zero demo/loadout consumers of the record or any KPM field, confirming the "drax NONE" consumer table.

## Rationale
Principle #3 cross-seam impact: a docstring/comment-only change cannot alter Pydantic field validation, JSON shape, or any downstream read — the only risk surface was a factual mismatch between the annotated unit/band and the gamora-wired source, which I checked field-for-field and confirmed correct. Discipline #12 provenance is clean: the semantic shift is attributed to its gamora origin commits (`1032560`/`92c040f`) with MIGRATION authority citations, and star-lord's export entry documents the reinterpretation without claiming ownership of the values. Principle #4: this closes my own outstanding action item; the discharge is faithful to the action's wording.

## Action
- [x] Developer: action item from `2b8b502` line 34 DISCHARGED. No further work required.
- [ ] Matt: nothing to escalate. Tag is not pushed (Matt-gated per ADR-006); push remains the only open authorization.

INFO note (non-blocking): the §v1.79 MIGRATION entry's "155/155 prior tests PASS" line and the commit message / AGENT_STATE "199/199" line are inconsistent test-count framings (prior-suite vs full-seam). Cosmetic — does not affect the verdict — but tighten on next touch for provenance hygiene.

## References
- `src/reincarnated/export/schemas.py` (ExportSimCyclingRecord docstring + KPM field comments)
- `src/reincarnated/export/MIGRATION.md` §v1.79-kpm-export-reinterpret
- `src/reincarnated/export/AGENT_STATE.md` (2026-06-17 checkpoint)
- `src/reincarnated/simulation/gauntlet_sim.py:206-323` (live ENCOUNTER_COHORT_KPM_BAND; mobs/min values confirmed)
- `src/reincarnated/simulation/MIGRATION.md` §v1.74 (line 7785), §v1.76 (line 7822)
- gamora commit `92c040f` (Stage-2d band wire-in), `1032560` (Stage-2a numerator)
- `src/reincarnated/export/season_exporter.py:1000-1069` (only engine consumer; model_validate)
