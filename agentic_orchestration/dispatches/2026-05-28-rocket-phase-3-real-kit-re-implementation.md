# Dispatch — 2026-05-28 — rocket — Phase 3 real-kit re-implementation + synthetic_mode final retirement (Option 4b; ~3-5 days)

**From:** knight-rider
**To:** rocket (engine generation seam owner; Phase 3 + season_generation_pipeline owner)
**Approved by:** Matt 2026-05-28 verbatim Option 4b ratification per gamora Pattern A-light empirical inspection (Phase 3 not subsumed by Phase 4 + Phase 7; BC coordinate quality LOAD-BEARING; synthetic kits produce unreliable 8-axis coordinates that degrade Phase 4/7 silently)
**Estimated effort:** ~3-5 days rocket impl (Phase 3 re-implementation + synthetic_mode pipeline-layer final retirement + KPM gating restoration + D84 sub-option B initial)
**Acceptance:** Phase 3 re-implemented consuming Phase 2 staged kits + real PlayerClass instantiation + synthetic_mode fully retired at pipeline layer + KPM gating restored + D84 sub-option B operational + smoke-test against current 18 staged kits PASS + BC coordinate validity verified post Phase 3 + jack-ryan Gate-2 PASS

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** close the Discipline #39 LOAD-BEARING gap (synthetic-stub-as-permanent-fallback) by retiring `_SyntheticPlayerClass` at pipeline layer + restoring BC coordinate validity that Phase 4 + Phase 7 presuppose. Without Phase 3 real-kit re-implementation, Phase 4 math gates + Phase 7 2-layer joint-gate operate on garbage BC coordinates → silent quality degradation. Composes "Engine first. Game second. Phase third." — Phase 3 BC coordinate generation is engine-layer infrastructure protecting Phase 4 + Phase 7 quality-filter authority.

**Refutation conditions** (rocket surfaces if any apply):
- Phase 2 staged kit shape not directly consumable by Phase 3 PlayerClass instantiation (kit format vs PlayerClass expected shape mismatch)
- D84 sub-option B per-legendary cohort selection requires methodology consultation beyond your judgment (route to legolas Mode A per Discipline #18)
- KPM gating restoration breaks existing Wave 5 gauntlet sim assumptions (need re-calibration)
- BC coordinate validity verification surfaces UNEXPECTED degradation patterns vs Cycle 13 synthetic-mode baseline (would warrant Pattern A-light surface to Matt before continuing)

## Context

**Authority chain:**
- Matt 2026-05-28 verbatim Option 4b ratification
- Gamora Pattern A-light empirical verdict 2026-05-28 (SUBSUMED-with-nuance; BC coordinate quality LOAD-BEARING for Phase 4/7; synthetic kits produce unreliable 8-axis coordinates)
- Discipline #39 LOAD-BEARING (no-synthetic-stub-as-permanent-fallback; canonical at engineering-disciplines.md)
- Discipline #40 LOAD-BEARING (scaffold-with-pending-decision; canonical text)
- Phase 2 staged output at `agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` (18 kits VALID; complete kit + multi-T4 capstones + bound substrate + gear instances at all rarities)
- doc 39 § 5.3 (convergence iteration + multi-T4 sim methodology + playability gate spec)
- Phase 4 mechanical archive at engine `749d5aa` (gamora MG-1/2/3/4/5; presuppose BC coordinate validity)
- Phase 7 IMPL bridge at engine `eca0aa5` (presuppose BC coordinate validity)
- Wave 5 BLOCKER context: gamora `b5d8211` + `7b11ca9` (Phase 3 degeneracy halt diagnosis)
- Rocket prior constant fix at engine `962d795` (`_EXPECTED_ELIGIBLE_ROW_COUNT 2108 → 2314`)

**Discipline framework operating correctly per Matt observation:** this is third Cycle 14 scaffold-drift case (doc 48 VESTIGIAL + Phase 7 SPEC/IMPL split + `_SyntheticPlayerClass`). Each was a Discipline #40 gap surfaced through sub-agent execution. Wave 0.5 retirement of `synthetic_mode` flag missed pipeline-layer `_SyntheticPlayerClass` instantiation. Final retirement closes the gap.

## Required reading

- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` lines 851–949 (`_SyntheticPlayerClass`; primary fix target; lines 897-905 + 918-923 magnitude=3000)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` (gamora's orchestrator; Phase 3 invocation context)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` (Phase 2 staged output; 18 kits to consume)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 5.3 (convergence iteration + multi-T4 sim + playability gate canonical spec)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/phase4_*.py` (gamora Dispatch 3A `749d5aa`; BC coordinate consumption)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` (gamora Phase 7 IMPL `eca0aa5`; BC coordinate consumption)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #39 + #40 + #41 + #42 + #45 + #46 § 7
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines`

## Discipline #46 compliance

- Per-kit Phase 3 sim operates on **bounded substrate per BC cell** (Discipline #46 § 7 LOAD-BEARING; no unbounded cross-cell queries)
- EXPLAIN QUERY PLAN at any new DB queries
- No global fetchall over kit_archive OR weapon_knowledge_entries

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:**
  1. Phase 2 staged kit format is directly consumable by Phase 3 PlayerClass instantiation (same kit→PlayerClass path Wave 5 gauntlet proper uses)
  2. D84 sub-option B per-legendary cohort selection fits rocket judgment without legolas Mode A escalation
  3. KPM gating restoration is purely turning off synthetic_mode bypass + re-enabling existing KPM threshold logic
  4. BC coordinate validity post Phase 3 is empirically verifiable against current 18 staged kits (smoke test feasibility)
- **Q2 refutation evidence to seek:** verify Phase 2 kit format vs PlayerClass shape (read both at impl entry); verify KPM threshold logic intact in pipeline.py; smoke-test against 3-5 kit subset before full 18-kit run
- **Q3 outcome trigger:** if Phase 2 format mismatch OR KPM logic broken OR D84 methodology depth exceeds rocket scope → invoke #44 framing-refusal + surface to KR (D84 routes to legolas Mode A; format mismatch may require gandalf seam consultation)

## Scope (8 parts per Matt verbatim)

### Part 1 — Math-before-code (Discipline #1 LOAD-BEARING) (~0.5 day)

- [ ] Author math note at `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-3-real-kit-re-impl-math-2026-05-28.md`
- [ ] Algorithm spec: kit consumption → PlayerClass instantiation → simulation → KPM measurement → BC coordinate emission
- [ ] D84 sub-option B per-legendary cohort selection methodology spec
- [ ] BC coordinate validity criterion (what makes a coordinate "valid"; smoke-test acceptance threshold)
- [ ] Composition with Phase 2 output schema + Phase 4 BC coordinate consumer + Phase 7 cohort classifier
- [ ] **AMENDMENT 1 per jack-ryan Gate-1 (PASS-with-REVISIONS):** DB query pattern spec as explicit deliverable (Discipline #46 extension + #18 composition). Math note must include: per-cell bounding method + streaming vs fetchall + index verification via EXPLAIN QUERY PLAN. Per #46/#18: a math note that specifies algorithm without DB query pattern is incomplete.

### Part 2 — Phase 3 re-implementation (~1-2 days)

- [ ] Re-implement Phase 3 to consume Phase 2 staged output (`cycle-14-wave-5-season-001/phase2_kit_candidates.json`)
- [ ] Real `PlayerClass` instantiation per kit (same path Wave 5 gauntlet proper uses; NO `_SyntheticPlayerClass`)
- [ ] Phase 3 consumes Phase 2 output ONLY (NOT Phase 4 output; avoids loop dependency)
- [ ] Per-kit Phase 3 sim operates on bounded substrate per BC cell (Discipline #46 § 7)

### Part 3 — synthetic_mode final retirement at pipeline layer (~0.5 day)

- [ ] Remove `_SyntheticPlayerClass` from `season_generation_pipeline.py` lines 851-949 (or refactor with deprecation)
- [ ] Remove `synthetic_mode=True` flag paths throughout pipeline.py
- [ ] **Grep audit across ALL pipeline layers** (not just flag-level) for any remaining synthetic stubs (per Matt KR OP § 3.X observation; Wave 0.5 missed pipeline-layer)
- [ ] **AMENDMENT 3 (recommended) per jack-ryan Gate-1:** explicit file scope for grep audit: `generation/season_generation_pipeline.py` + `simulation/gauntlet_sim.py` + `simulation/t4_sim_cycling.py` + `simulation/phase7_bridge.py` + `simulation/wave5_season_orchestrator.py`. Jack-ryan empirically verified existing references in t4_sim_cycling.py + phase7_bridge.py + gauntlet_sim.py are comment-only retirement notes (non-functional); confirm during audit.
- [ ] Verify Discipline #39 LOAD-BEARING gap CLOSED via empirical grep audit

### Part 4 — Restore KPM gating per doc 39 § 5.3 playability gate (~0.5 day)

- [ ] Re-enable KPM threshold logic for non-synthetic kit gating
- [ ] Verify `TIER_1_REJECT_THRESHOLD=0.30` still meaningful under real-kit simulation
- [ ] Composition with playability semantics per doc 39 § 5.3 (skill rotation coherence; resource flow; degenerate-state detection)

### Part 5 — D84 sub-option B per-legendary cohort selection (~1-2 days)

- [ ] Implement D84 sub-option B (per-legendary cohort selection; lower-compute fallback per gamora Pattern A-light recommendation)
- [ ] Multi-T4 methodology per doc 39 § 5.3
- [ ] Cycle 15+ promotion path to hybrid-within-hybrid (architectural readiness; no impl)

### Part 6 — Phase 2 → Phase 3 data flow (~0.5 day)

- [ ] Verify Phase 3 consumes Phase 2 output schema directly
- [ ] Document data flow at math note + inline comments
- [ ] Loop dependency check: confirm Phase 3 does NOT consume Phase 4 output

### Part 7 — Smoke-test + BC coordinate validity verification (~0.5 day)

- [ ] Smoke-test against current 18 staged kits (start with 3-5 subset; expand to 18)
- [ ] Verify BC coordinate validity post Phase 3 (empirical inspection; Discipline #11)
- [ ] Verify Phase 4 + Phase 7 consume BC coordinates without degradation
- [ ] Capture telemetry: per-kit KPM distribution + BC coordinate range + cohort classification
- [ ] **AMENDMENT 2 per jack-ryan Gate-1 (PASS-with-REVISIONS) — Principle 6 round-trip clause:** `_build_legendary_config` output's `player_class` field changes from `_SyntheticPlayerClass` to real `PlayerClass`. Cross-seam consumer boundary = `combatant.from_player_class()`. Smoke-test MUST confirm real `PlayerClass` flows through `combatant.from_player_class()` without error; field-presence check passes (`stats.as_dict()`, `energy_type`, `skills`, `range_profile`). This Principle 6 round-trip clause folds into Part 7 smoke-test acceptance criterion.

### Part 8 — Incremental-write discipline + Wave 5 Option C composition (~throughout)

- [ ] Apply incremental-write per-part commit + push (Part 1 math note → commit; Part 2 re-impl → commit; Part 3 retirement → commit; Part 4 KPM → commit; Part 5 D84 → commit; Part 6 data flow → commit; Part 7 smoke → commit; final closure commit)
- [ ] Composes with Wave 5 Option C orchestration (KR fires you; you commit per-part; KR routes downstream)

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`
- [ ] Tag at completion: `rocket/v1.7-phase-3-real-kit-re-impl-1`
- [ ] All existing tests PASS (+ new smoke-test gates G-P3-*)
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-28 per-cycle push pattern

## Acceptance criteria

- [ ] Math note authored (Discipline #1)
- [ ] Phase 3 re-implemented; consumes Phase 2 output; real PlayerClass instantiation
- [ ] `_SyntheticPlayerClass` removed/deprecated at pipeline layer
- [ ] synthetic_mode grep audit CLEAN across all pipeline layers (Discipline #39 LOAD-BEARING closure)
- [ ] KPM gating restored per doc 39 § 5.3 playability semantics
- [ ] D84 sub-option B operational (per-legendary cohort selection)
- [ ] Phase 3 → Phase 2 data flow verified (no loop dependency)
- [ ] Smoke-test against 18 staged kits PASS
- [ ] BC coordinate validity verified empirically post Phase 3 (Discipline #11)
- [ ] All 8 parts committed + pushed (incremental-write discipline)
- [ ] Tag `rocket/v1.7-phase-3-real-kit-re-impl-1`
- [ ] AGENT_STATE.md updated
- [ ] Completion record + commit + push

## Out of scope

- Do NOT modify Phase 2 generation (gamora seam; Phase 2 staged output is authoritative input)
- Do NOT modify Phase 4 mechanical archive (gamora `749d5aa` LOCKED)
- Do NOT modify Phase 7 IMPL bridge (gamora `eca0aa5` LOCKED)
- Do NOT promote D84 sub-option B to hybrid-within-hybrid (Cycle 15+ scope)
- Do NOT execute Wave 5 Step 1 GENERATION continuation (gamora seam; resumes from Phase 2 staging post your landing + jack-ryan Gate-2 PASS)
- Do NOT touch ExportFactionCluster + ExportFactionRelationship schemas (star-lord seam)

## Open questions for rocket

- **Q-P3R-1:** Phase 2 staged kit format vs PlayerClass shape — direct consumable OR adapter needed? Your judgment per empirical inspection (read Phase 2 JSON + PlayerClass class at impl entry). **JACK-RYAN GATE-1 EMPIRICALLY VERIFIED 2026-05-28:** Phase 2 JSON kits contain `character_id` / `bc_tuple` / `element` / `cohort_archetype` — i.e., serialized `KitCandidate` NOT `PlayerClass`. Real `PlayerClass` is generated from `KitCandidate` inside `w5r1_generate_kit_candidates()` via generation pipeline. Real Phase 3 re-impl path: load Phase 2 JSON → reconstruct `KitCandidate` objects (OR call gen pipeline on 18 cells) → call `w5r2_gauntlet_sim_integration(kit_candidates=kits)` with real `KitCandidate` list which already builds `PlayerClass` objects internally. PlayerClass instantiation already happens inside `_build_legendary_config` → `_SyntheticPlayerClass`; the fix is replacing that with real `PlayerClass` construction via existing pipeline path.
- **Q-P3R-2:** D84 sub-option B methodology depth — your judgment OR route legolas Mode A consultation (per Discipline #18 math-hotspot)?
- **Q-P3R-3:** synthetic_mode grep audit scope — pipeline.py only OR cross-seam (gauntlet sim + bridge consumers)? Recommend cross-seam audit per Matt KR OP § 3.X observation
- **Q-P3R-4:** BC coordinate validity criterion — what makes a coordinate "valid" (range / variance / cohort consistency)? Your judgment via math note Part 1

## References

- Matt 2026-05-28 verbatim Option 4b ratification
- Gamora Pattern A-light empirical verdict (SUBSUMED-with-nuance; BC coordinate LOAD-BEARING)
- doc 39 § 5.3 (convergence iteration + multi-T4 sim + playability gate)
- Discipline #39 LOAD-BEARING (synthetic-stub retirement)
- Discipline #40 LOAD-BEARING (scaffold-with-pending-decision)
- Discipline #45 vocab lock canonical at engine `b576727`
- Discipline #46 § 7 per-cell bounding
- Wave 5 Option C orchestration (KR-routed multi-step)
- Phase 2 staged at `cycle-14-wave-5-season-001/phase2_kit_candidates.json`

---

## Completion record

(append on completion)
