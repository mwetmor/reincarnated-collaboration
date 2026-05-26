# Dispatch — 2026-05-25 — rocket — Phase 5 cohesion-judge calibration + v2_narrow_phase_5 regen

**From:** knight-rider (orchestrator)
**To:** rocket (generation seam — owns generation/, element/, anchor/, foundation/, engine canonical library)
**Approved by:** Matt 2026-05-25 — gandalf parallel-track authoring complete (commit `fe9bac1`); Phase 5 calibration spec ratified as regen-gate
**Estimated effort:** ~1-2 days implementation + ~30-60 min calibration sweeps + jack-ryan Gate-2 validation
**Pattern:** Pattern B (multi-day; persistent session memory needed; design-spec-as-math per gandalf canonical authoring)

---

## Authority / context

This dispatch is the **regen-gate to fix the v2_narrow placeholder issue**. Empirical finding from gandalf design-fit pass 2026-05-25:

- 289/289 skill nodes across 35 forms are placeholders ("Chain A T1 0", "Chain B T2 1", etc.)
- All 35 forms have degenerate `balance_metadata` (actual_winrate=0.5, 1 iteration, modifier=1.0 identical)
- Layer 6 wire-up FUNCTIONAL but Phase 5 cohesion-judge ran at form-layer only, not skill-node level
- Root cause: kits are mechanically indistinguishable without real skills → balance loop trivially converges → no fight-behavior differentiation observable

**Phase 5 skill-node naming is THE gating piece for both T4 post-mortem evaluation and meaningful fight-behavior signal.**

## Authoritative spec

**PRIMARY READING (load-bearing — implement per this spec):**
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` — gandalf design-spec-as-math; ratified 2026-05-25

The spec defines:
- § 2 Per-node output schema (name + flavor_text + effect_description + thematic_tags) + LLM input context + prompt template
- § 3 Cohesion-validation rubric (5 dimensions, weighted aggregate; PASS ≥ 0.75)
- § 4 Calibration sweeps (9 parameters; smoke-then-sweep pattern)
- § 6 Acceptance criteria (12 checks; jack-ryan Gate-2 validates per checklist)

**SUPPORTING READING:**
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` — full design-fit pass findings + § 3.7 critical finding (degenerate balance_metadata across all 35 forms)
- `canonical/story/skill-system-2026-05-24.md` § 9 — spirit-guide explainer pattern (Phase 5 form-level context)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` Phase 5 Cohesion Coalescence (engine workflow position)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 5 (named-bearer discipline; § 5.4 per-season anchor variability lock)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #2 smoke-test, #17 calibration-sweep discipline, #18 methodology-before-execution

## Required reading at session start

1. Phase 5 spec (above)
2. Existing Phase 5 form-level implementation in engine (likely `~/Games/reincarnated-engine/src/reincarnated/generation/` — locate via grep for "phase_5" / "cohesion_judge" / "naming")
3. Latest decisions-log entries (engine canonical authority)
4. star-lord LLM-seam infrastructure (`src/reincarnated/llm/`) — DiskCache, telemetry, model selection
5. Existing v2_narrow run script (`scripts/v1_narrow_generation_run_2026_05_25.py` likely; rocket discretion on locate)

---

## Scope

### Implementation (per spec § 2)

- [ ] Locate existing Phase 5 form-level code path; identify extension point for skill-node-level firing
- [ ] Implement per-node Phase 5 LLM call per § 2 schema:
  - Per-node output: `SkillNodeNaming` dataclass (name + flavor_text + effect_description + thematic_tags)
  - Per-node input context: kit identity (form_name, kit_summary, element, energy_type, primary_stat, range_profile, tempo/amplitude, mechanical_substrate_triple, cultural_tradition, named_bearer, lineage) + per-node context (node_id, chain_id, tier, node_type, bc_axis_contribution, cost, cooldown_seconds, playable_at_level_1, is_t4_slot, t4_alteration) + cross-node context (chain_predecessor_names, form_previously_named_nodes)
  - Prompt template per § 2.3
- [ ] Implement cohesion-judge sub-pass per § 3:
  - 5-dimension scoring (kit-identity 0.30 + chain-progression 0.20 + mechanical-narration 0.20 + cultural-tradition 0.15 + cross-tree-thematic 0.15)
  - Aggregate cohesion_score per § 3.6
  - Acceptance thresholds: ≥ 0.75 PASS; 0.60-0.74 BORDERLINE flag; < 0.60 FAIL re-roll (max 3 attempts then placeholder + flag)
- [ ] LLM model selection — Claude 3.5 Sonnet RECOMMENDED per spec § 2.4; coordinate with star-lord LLM-seam if Haiku considered (cost-tradeoff judgment)
- [ ] Telemetry per § 6 (per-node: prompt + response + cohesion_score + attempt number + DiskCache hit/miss + cost-per-run vs G12 baseline)

### Calibration sweeps (per spec § 4)

- [ ] **Smoke-then-sweep pattern (rocket discipline #2 + #17):** fire small smoke first (3-5 forms; ~30-50 nodes); measure cohesion-score distribution + re-roll rate + observable quality BEFORE full regen
- [ ] Sweep 9 parameters per § 4 if smoke surfaces tuning need:
  1. Per-node LLM temperature (initial 0.7; range 0.5-1.0)
  2. Per-node max_tokens (initial 200; range 150-300)
  3. Cohesion-score acceptance threshold (initial 0.75; range 0.65-0.85)
  4. Re-roll attempt cap (initial 3; range 2-5)
  5. Chain-predecessor context size (initial 3; range 2-5)
  6. Cross-tree thematic context size (initial 5; range 3-10)
  7. Element + cultural-tradition prompt weight (balanced vs dominant variants)
  8. T4 slot prompting (shared vs separate template variant)
  9. Named-bearer attribution prominence (subtle / explicit / absent variants)
- [ ] Re-smoke to validate sweep choices
- [ ] Fire full regen (35 forms; ~289 nodes)

### Output versioning

- [ ] **Versioning judgment (KR pre-decision):** emit as `v2_narrow_phase_5` to preserve `v2_narrow` as historical baseline pre-Phase-5-fix. Rocket may override to `v2_narrow_v2` if cleaner. **DO NOT overwrite v2_narrow.**
- [ ] Update generation run script + emission paths accordingly
- [ ] Document version delta in run log

### Cross-seam coordination

- [ ] **star-lord LLM-seam:** model selection (Sonnet vs Haiku tradeoff) + telemetry instrumentation (per-node logging per § 6) — if star-lord coordination required, route through KR
- [ ] **drax loadout app:** spec § 8 notes "no drax work required IF rocket emission matches existing schema" — verify by inspecting loadout SkillTree components consume `name + flavor_text + effect_description` per existing schema; if rocket emission schema diverges, raise as MIGRATION.md item
- [ ] **MIGRATION.md** authored per ADR-004 (skill-node naming schema is new cross-seam data surface)

### Out of scope (per spec § 7)

- Existing Phase 5 form-level naming behavior (preserved as-is)
- Visual coalescence (Phase 6) integration (v1.1+ candidate)
- Per-form sim re-run after Phase 5 names land (independent if names don't affect mechanics)
- Cross-season cohesion (v1.1+ design)
- T4 keystone narration distinction from drax narration_metadata (separate compose layer)

---

## Acceptance criteria (per spec § 6 — jack-ryan Gate-2 validates)

- [ ] Phase 5 fires at skill-node level for ALL nodes in ALL generated forms
- [ ] Per-node output schema § 2.1 populated (name + flavor_text + effect_description + thematic_tags)
- [ ] **No placeholder strings** (e.g., "Chain A T1 0") in skill-node names; all named per Phase 5 LLM output
- [ ] Cohesion-judge fires per node + produces cohesion_score per § 3.6 weighted aggregate
- [ ] First-attempt PASS rate ≥ 70% (initial target; may calibrate per § 4 #3)
- [ ] Re-roll rate ≤ 15% (initial target; may calibrate per § 4 #4)
- [ ] Final FAIL rate (after re-rolls) ≤ 5% per generation run
- [ ] Spirit-guide explainer integrates skill-node naming where applicable (per skill-system § 9)
- [ ] LLM-call telemetry per node logged (prompt + response + cohesion_score + attempt number)
- [ ] DiskCache hits + misses logged per generation run
- [ ] Cost-per-run metric reported (compares to G12 measurement baseline)
- [ ] Cross-form name uniqueness ≥ 95% (within run, ≤ 5% duplicate skill names across kits)
- [ ] MIGRATION.md entry authored

---

## Engineering disciplines (cite at execution)

- **#1 math-before-code** — Phase 5 schema + cohesion rubric defined by gandalf spec; implement per spec exactly
- **#2 smoke-test discipline** — fire 3-5 form smoke before full 35-form regen
- **#1.1 pre-fire resource-bounds projection** — ~350 LLM calls × 1500 tokens projected; cost ~$0.50-$2.00 per run (Sonnet); declare peak before fire
- **#11 attribution clarity** — every emitted artifact has Phase 5 provenance (model + temperature + cohesion_score + attempt #)
- **#17 calibration-sweep discipline** — 9 parameters surveyed at smoke; sweep if smoke surfaces tuning need
- **#18 methodology-before-execution** — gandalf spec IS the methodology; implement per spec exactly; if spec needs amendment, route through KR back to gandalf
- **#20 row-duplication prohibition** — N/A (no density-weighted sampling here)
- **#21 no sleep recommendations** + **#22 timezone-agnosticism** — universal

## Tag / commit / push protocol

- **Tag pattern:** `rocket/v2.x-phase-5-calibration-<n>` for intermediate; final tag is `v2.0-phase-5-skill-node-naming` (Matt-approved milestone after Gate-2 PASS)
- **Commit cadence:** auto-fire per CLAUDE.md addendum (authorized cycle work; commits don't re-ask)
- **Push:** Matt-explicit-authorization (default per ADR-006); ASK at end of implementation arc, not per-commit
- **Submit to qa/pending/** when ready for Gate-2

## Completion record

When done, append to this dispatch file:
- Final tag(s)
- Smoke results + sweep decisions (which params adjusted, which kept initial)
- Final cohesion-score distribution across 35 forms
- LLM cost per run + DiskCache hit rate
- v2_narrow_phase_5 emission path
- Any deviations from spec (with reasoning)
- MIGRATION.md path
- Path to QA pending submission

**Status:** PENDING (awaiting rocket pickup)
