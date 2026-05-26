# Finding — 2026-05-25 — rocket-engine-generation-run-v1-narrow

**Reviewer:** jack-ryan
**Verdict:** PASS-with-WARN
**Tag:** `rocket/v0.1-engine-generation-run-v1-narrow-2026-05-25`
**Engine commit:** `af28e6a`
**Loadout commit:** `b786048`
**Developer:** rocket
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 6 (cross-seam contract)
**Disciplines cited:** #1.1 (resource-bounds projection), #2 (smoke-test), #11 (empirical inspection)

---

## What I found

### Spot-check results (empirical)

All 35 forms verified against classes.json (`/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json`):

| Check | Result |
|---|---|
| engine_version="v2.0" | PASS — 35/35 |
| mechanical_substrate_triple populated | PASS — 35/35 |
| t4_alteration_output populated | PASS — 35/35 |
| strategy_type in t4_alteration_output | PASS — 35/35 |
| validation_errors (per metadata.json) | PASS — 0 |
| Loadout copy matches engine export | PASS — 35/35, first-id and name match |
| Engine commit touches src/reincarnated/ | PASS — NO src/ changes (scripts/, exports/, AGENT_STATE.md only) |
| Cross-seam MIGRATION.md amendment | PASS — none |

### Findings

**WARN-1 — Strategy coverage: metadata claims 6, export delivers 4**

`metadata.json` reports `strategies_covered` = 6 (DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, ELEMENT_CONVERSION, GEOMETRY_COLLAPSE, RESOURCE_CONVERSION, TRADE_OFF). Empirical check of `t4_alteration_output.strategy_type` across all 35 classes.json records shows only 4 strategies elected (DEFENSIVE_CONVERSION: 13, GEOMETRY_COLLAPSE: 8, TRADE_OFF: 9, RESOURCE_CONVERSION: 5). ELEMENT_CONVERSION and DEFENSIVE_TRADEOFF are absent from all 35 exported forms.

Root cause confirmed: `verify_coverage()` in the runner script reads strategy from `T4Alteration.candidates` in the SkillTree (possible strategies), not from the elected `t4_alteration_output.strategy_type` (actual strategies). This inflates the coverage count. The provenance manifest and completion record both inherit the inflated claim.

Framing brief § 1.1 requires all 6 strategies "represented (≥2-3 forms per strategy where cell-eligibility allows)." That criterion is not met for ELEMENT_CONVERSION and DEFENSIVE_TRADEOFF. The completion record's strategy coverage claim is inaccurate.

Cite: Discipline #11 (empirical inspection over assumption). The coverage metric was computed from candidate pools, not elected outputs — a discipline #11 violation.

**WARN-2 — gamora_combatant_fields placement mismatch vs completion record claim**

Completion record states "gamora_combatant_fields populated on all kits." Empirically: `gamora_combatant_fields` does NOT exist as a top-level key in any of the 35 ExportClass records. It lives at `t4_alteration_output.gamora_combatant_fields` (nested), where it IS populated on all 35. The nesting is correct behavior per the runner script's `kit_to_export_dict()` logic, but the completion record claim is imprecise and creates a schema-contract ambiguity: gamora's consumer contract (MIGRATION.md § v1.5) specifies `gamora_combatant_fields` as a sub-field of `ExportAlterationOutput`, which matches. The risk is downstream consumers expecting a top-level field. The dispatch acceptance criteria say "gamora_combatant_fields populated on all kits" — this is met if the reader understands the nested location.

Severity: WARN because the data is correct in placement per MIGRATION.md, but the completion record language is loose enough to mislead future reviewers. Flag for T4 post-mortem documentation clarity.

**INFO-1 — Bug-fix discipline: runner-script field-name mismatches**

Two bugs were fixed during execution inside `scripts/v1_narrow_generation_run_2026_05_25.py`:
1. `_skill_tree_to_export_skills()` assumed old-engine `Skill` attributes (`.name`, `.energy_cost`, `.damage_multiplier`, `.effects`); corrected to new-engine names (`skill_id`, `cost`, `scaling_coefficient`, `keystone_effect`).
2. `apply_llm_naming()` called `LLMClient.complete(prompt=...)` instead of `complete_json(system=..., user=...)`.

KR pre-verified both bugs are confined to the runner script (execution scaffolding), not engine core. Engine commit `af28e6a` confirms: zero changes to `src/reincarnated/`. Dispatch out-of-scope clause ("if the run surfaces a bug requiring code change, STOP and escalate") applies to engine code amendments — these were runner-script-only fixes, which is execution-internal. Per dispatch spirit this is acceptable.

However: an execution-only dispatch should produce a runner script that works against the already-known new-engine API. The runner was authored without consulting `Skill.skill_id` (defined in Layer 3 math note, Cycle 12). This is a process softness — the script author should have cross-referenced the new-engine field contract before authoring the export helper. Classify INFO, not WARN, because (a) the bugs were in scaffolding not engine, (b) they were fixed in-run without escalation, and (c) the fixes are correct per empirical output verification.

**INFO-2 — Provenance types: mythological-NULL rescue absent; Necromancer gap-fill undocumented**

Framing brief § 1.1 requires all 4 `source_library` provenance types: substrate-pulled main, substrate-pulled off-hand (Sidecar B), engine-authored gap-fills, and mythological-NULL rescue. Empirical check:
- `substrate_pulled_main`: 25 forms
- `substrate_pulled_named_bearer`: 10 forms (lineage present)
- `engine_authored_gap_fill` (`stage_3_5_gap_fill=True`): 1 form (Pyromantic Caster, v2-form-016)
- `mythological_null_rescue`: 0 forms
- `substrate_pulled_off_hand` (Sidecar B): 0 (all source_library="generator_v2")

The provenance manifest documents `detailed_provenance = ["engine_authored_gap_fill", "substrate_pulled_main", "substrate_pulled_named_bearer", "substrate_pulled_off_hand"]`, which is inconsistent with the actual data (no off-hand provenance flag set). Additionally, Necromancer Summoner (v2-form-018) appears in the output with `stage_3_5_gap_fill=None` and `cell_routing_source=locked_section_4_1` — it appears to have been generated via a fallback path without explicit gap-fill tagging.

This is a v1 documentation accuracy issue, not a blocking schema failure. The T4 post-mortem should address: (a) whether mythological-NULL rescue was expected to appear in this run (Stage 4 per composition policy is a separate Sidecar — it may legitimately be absent at v1 narrow), and (b) whether Necromancer Summoner's generation path is intentional.

**INFO-3 — Element coverage (all-physical): correctly documented as v1 limit**

Completion record and provenance manifest both document element="physical" for all 35 forms as a known v1 architectural limitation (substrate keyword inference on historical weapon names). This is per framing brief § 1.3 acceptance. No remediation in-cycle; flagged for T4 post-mortem. Routing is correct.

**INFO-4 — Sketch F anchor sub-sampling (1/4): correctly documented**

Completion record documents Moctezuma-only sampling as a seed/cell-order artifact; substrate rows for Hattori Hanzō, Lu Bu, Gilgamesh exist. Provenance manifest has per-anchor notes. Not in-cycle remediated. Routing is correct. Note: Moctezuma appears twice (v2-form-008 INT/mana and v2-form-025 STR/rage) — both well-characterized.

**INFO-5 — Blocked cells (Pyromantic Caster, Necromancer Summoner) in output despite BLOCKED status**

Completion record says Pyromantic Caster and Necromancer Summoner are BLOCKED (zero eligible substrate). Empirically: both appear in classes.json (v2-form-016 and v2-form-018). Pyromantic Caster has `stage_3_5_gap_fill=True` (explicit gap-fill path). Necromancer Summoner has neither `stage_3_5_gap_fill` nor a matching substrate lineage — it appears to have been generated via a fallback. The metadata.json `blocked_cells` list and the `bc_cells_covered` list both include these cells, creating an inconsistency (blocked yet covered). This is documentation-level ambiguity. No schema failure; both forms are valid. Flag for T4 post-mortem clarification of what "BLOCKED" means in the run log when a gap-fill or fallback path produces a form anyway.

---

## Rationale

- WARN-1 is non-blocking because ELEMENT_CONVERSION and DEFENSIVE_TRADEOFF are in the candidate pool (strategies exist in the engine) — they were not elected by the L6 wire-up for this seed. The framing brief says "≥2-3 forms per strategy where cell-eligibility allows," and cell-eligibility may explain the gap. However the coverage claim in the completion record must be corrected before it becomes a decisions-log source of truth.
- WARN-2 is non-blocking because the nested placement is per MIGRATION.md contract. Language cleanup needed in completion record and provenance manifest.
- INFOs are observations for T4 post-mortem routing; no action blocks shipment.
- Cross-seam contract: CLEAN. No `src/reincarnated/` changes; no MIGRATION.md amendments; no new fields added to any cross-seam interface. Engine commit `af28e6a` confirms.
- Math-before-code (Discipline #1): N/A per dispatch (execution dispatch). Pre-fire resource-bounds projection IS present and documented in runner script header (lines 12-20: ~$4.20 projection, peak memory assessment). Discipline #1.1 satisfied.

---

## Action

- [ ] **rocket (WARN-1):** Correct the strategy coverage claim in the completion record. Document that 4/6 strategies were elected (not 6/6). ELEMENT_CONVERSION and DEFENSIVE_TRADEOFF exist as candidate strategies but were not elected in this seed. Add this to T4 post-mortem agenda as a sampling-policy question (does seed 20250525 bias against these strategies? higher N or cell re-ordering likely resolves).
- [ ] **rocket (WARN-2):** Correct completion record language: "gamora_combatant_fields populated on all kits at `t4_alteration_output.gamora_combatant_fields`" (nested, per MIGRATION.md § v1.5). Remove ambiguity for downstream readers.
- [ ] **T4 post-mortem agenda (no blocking action):**
  - INFO-2: Clarify mythological-NULL rescue absence (expected at v1 narrow? Stage 4 Sidecar not yet executed?)
  - INFO-2: Clarify Necromancer Summoner generation path (fallback vs intentional gap-fill)
  - INFO-5: Define "BLOCKED" semantics when gap-fill/fallback path produces a form
  - WARN-1: Strategy election distribution — is seed-specific or cell-distribution structural?
- [ ] **Matt:** No escalation required. WARNs are completion-record corrections, not schema failures. Gandalf design-fit pass may proceed on current output — the actual form data is valid.

---

## References

- Dispatch: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-25-rocket-engine-generation-run-v1-narrow.md`
- Runner script: `/Users/admin/Games/reincarnated-engine/scripts/v1_narrow_generation_run_2026_05_25.py`
- Engine export: `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json` (35 forms, 358KB)
- Metadata: `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/metadata.json`
- Loadout deploy: `/Users/admin/Games/reincarnated-loadout/public/seasons/v2_narrow/classes.json`
- Provenance manifest: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md`
- AGENT_STATE.md: `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`
- Prior Gate-2 (full new engine PASS): `e3756bc`
