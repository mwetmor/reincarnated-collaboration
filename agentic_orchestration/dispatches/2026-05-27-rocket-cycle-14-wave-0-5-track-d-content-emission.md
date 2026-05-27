# Dispatch — 2026-05-27 — rocket — Cycle 14 Wave 0.5 Track D content gap closure (rocket scope)

**From:** knight-rider
**To:** rocket (engine content-generation seam owner)
**Approved by:** Matt 2026-05-27 (framing brief Q1-Q11 RATIFIED in full; Wave 0.5 LOAD-BEARING per framing brief § 2 + § 3)
**Estimated effort:** 1-2 weeks anchor (per framing brief Q10 quality > timeline; extends as needed)
**Acceptance:** Wave 0.5 rocket-seam scope items complete; jack-ryan Gate-2 PASS; cross-seam round-trip smoke with gamora damage_resolver + elrond SC-6b substrate enrichment

## Context

Cycle 14 Wave 0.5 closes the Track D content gap that Cycle 13 left open. Per framing brief § 2 Wave 0.5, this wave produces:

- **Elements expansion** — 4 → 7 elements (lightning / holy / shadow unlock)
- **Per-skill mechanical content emission** — chain T1-T3 + T4 capstones emit with full schema including `damage_scaling_type` per doc 47
- **Substrate weapon binding output** — `gear_representative.main_weapon` persists substrate weapon binding with stat exposure per doc 47 § 3

These three items are **rocket-seam scope** within Wave 0.5. Gamora-seam scope (damage scaling routing + synthetic_mode RETIREMENT) fires in parallel via separate dispatch. Elrond-seam scope (SC-6b substrate enrichment + MIGRATION.md) fires in parallel via separate dispatch.

**Wave 0.5 is the SUBSTANTIVE delivery point that Cycle 13 close was originally framed as.** Without these three items landing cleanly, downstream waves (concentration architecture Wave 1-2; Phase 5 cohesion-judge LLM Wave 3-5) have no real content substrate to cohere over.

**LOAD-BEARING discipline lock (Matt Q4 verbatim):** `synthetic_mode=True` is RETIRED ABSOLUTELY at Wave 0.5 close. This is gamora's seam, but rocket's per-skill emission feeds the real-content fight execution that replaces synthetic stubs. Discipline #39 (RATIFIED via SC-1) is the canonical lock.

**Cycle 13 season DISREGARDED (Matt Q9 verbatim):** Cycle 14 Wave 5 generates FRESH roster. Rocket per-skill emission targets the Wave 5 fresh roster generation pipeline, not Cycle 13 character regeneration.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — particularly § 2 (three scaling types) + § 3 (per-attribute weapon profile) + § 4 (formulas — informs rocket per-skill `damage_scaling_type` emission)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (Layer 1 stat-range bounds — substrate stats + skill outputs respect bounds)
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid; Cycle 14 v1 uses L50 cap baseline only (per-level deferred)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — AS AMENDED by SC-2 gandalf (commit `f56ce8b`): § 0.1 amendment-pass-record; D7/D9/D33/D38/D49/D50/D51/D52/D54/D55/D56/D63-D86 inheritance from doc 46 + doc 47
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern (element × geometry × tempo × amplitude × tier_coefficient + algorithmic mechanic-alteration)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — Option α / β / C cell-type matching
- `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system (STR / INT / WIS / DEX)
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` — legolas SC-5 research (Appendix A: doc 47 formula amendments table; Appendix B: framing-audit; **consume Appendix A recommendations for damage_scaling_type emission**)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` — SC-6 audit (per-field disposition table; **consume Path A architecture for substrate weapon binding output**)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` — RATIFIED authority + § 2 Wave 0.5 + § 3 detail + § 6 synthetic_mode regression risk lock
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 Wave 0.5 + § 5 disciplines
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #11 + #18 + #19 + #33 (stat-range bounds) + #38 (damage-scaling-path) + #39 (no-synthetic-stub-as-permanent-fallback)
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-hive-mind-protocol`

## Math-before-code

Per Discipline #18 (methodology-before-execution) + Discipline #1 (math-before-code) — three math-notes recommended BEFORE implementation:

1. **Per-skill mechanical content emission math-note** — at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-0-5-per-skill-emission-math-2026-05-27.md` documenting:
   - Schema per `GeneratedSkill` (framing brief § 3.2 spec)
   - `damage_scaling_type` assignment rule (consume SC-5 Appendix A — magical formula pool modifiers; physical formula reorder element_conversion)
   - `scaling_attribute` assignment (per skill element + geometry + tier)
   - tier_coefficient consumption per skill-system § 8

2. **Substrate weapon binding output math-note** — at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-0-5-substrate-binding-math-2026-05-27.md` documenting:
   - Phase 2c substrate selection query against `weapon_knowledge_entries.v1_scope=1` (2,293 rows)
   - Field-by-field mapping from `weapon_sim_props` columns (SC-6b enriched) → character JSON `gear_representative.main_weapon`
   - Path A consumption: `weapon_sim_props.base_physical_damage_l50 × damage_amplitude_min/max` lottery at binding time

3. **Elements expansion math-note** (light) — at `~/Games/reincarnated-engine/src/reincarnated/element/math/wave-0-5-elements-expansion-math-2026-05-27.md` documenting:
   - VALID_SLOTS expansion from 4 to 7 (fire + wind + water + earth + lightning + holy + shadow)
   - Foundation instantiation with 7 rotating substrates
   - element_biases verification for lightning / holy / shadow per BC attribute

Math-notes are jack-ryan Gate-1 inputs.

## Cross-seam contract change? (Principle 6 gate)

**YES** — Wave 0.5 rocket scope adds NEW fields to character JSON output:

**Per-skill fields (new):**
- `skill_id` / `chain_id` / `tier` / `name` (placeholder pre-Phase-5) / `role` / `canonical_element` / `geometry_type` / `timing` / `damage_multiplier` / `energy_cost` / `cooldown_seconds` / `damage_scaling_type` (doc 47 enum) / `scaling_attribute` (STR/DEX/INT/WIS) / `tier_coefficient` / `bc_axis_contribution` / `effects` (placeholder) / `hybrid_pattern` (nullable) / `hybrid_balance_factor` (nullable)

**Substrate weapon binding fields (new):**
- `gear_representative.main_weapon.substrate_weapon_id` / `substrate_canonical_name` / `base_physical_damage` / `spell_damage_modifier` / `element_affinity_modifiers` / `to_skill_level_modifiers` / `attribute_requirement` / `weapon_type_family`
- Similar new fields on `secondary_item` for off-hand category

**MIGRATION.md REQUIRED** per ADR-004 — author at `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md § Wave 0.5` (or rocket-OP-preferred location) capturing:
- New character JSON fields + schema rationale + downstream consumer expectations (gamora damage_resolver consuming `damage_scaling_type` + `scaling_attribute`; star-lord Track C transform consuming substrate weapon binding fields at Wave 5)
- Round-trip clause: "rocket Phase 2c substrate query → character JSON `gear_representative.main_weapon` contains all 8 substrate weapon fields; gamora damage_resolver routes per skill's `damage_scaling_type`; star-lord Track C transform consumes new fields per loadout-app season schema."

## Scope

- [ ] **Pre-implementation** — author 3 math-notes per § Math-before-code above; route to jack-ryan Gate-1 review (DESIGN-MODE)
- [ ] **Wait** for elrond SC-6b schema extension landed at `weapon_sim_props` (or coordinate parallel implementation with elrond if your bandwidth permits — rocket can scaffold per-skill emission + elements expansion FIRST, then integrate substrate binding output when elrond's columns land)

### Item 1 — Elements expansion (~2-4 hours)

- [ ] Inspect `~/Games/reincarnated-engine/src/reincarnated/element/selector.py:49` `VALID_SLOTS = ("fire", "wind", "water", "earth")` legacy fallback
- [ ] Amend `season_generation_pipeline.py:w5r1_generate_kit_candidates` (or equivalent) to instantiate Foundation with all 7 rotating substrates
- [ ] Pass Foundation through to element selector via `select_seasonal_elements(...)` call
- [ ] Verify `element_biases.py` defines couplings for lightning / holy / shadow per BC attribute
- [ ] Test: generate test season; verify all 7 elements available; subsequent generations exercise lightning / holy / shadow at substrate-led rates

### Item 2 — Per-skill mechanical content emission (~2-5 days)

- [ ] Implement Phase 2a per-chain per-node skill emission per `skill-system-2026-05-24.md` § 1 (10-15 nodes per kit; mechanic-altering passives; per-tier organization)
- [ ] Each skill emits with `GeneratedSkill` schema per framing brief § 3.2 (full field list including `damage_scaling_type` + `scaling_attribute` + `tier_coefficient` + `hybrid_pattern` + `hybrid_balance_factor`)
- [ ] Placeholder names pre-Phase-5 LLM coalescence (e.g., "Earth Chain 1 - T1 Active 1") — Wave 3 cohesion-judge LLM replaces placeholders with real flavor
- [ ] Schema match v2_narrow_phase_5 `classes.json` `skills[]` lineage where applicable
- [ ] Loadout-app season schema compatible (cross-reference star-lord Track C transform contract)
- [ ] T4 capstones emit per chain with existing T4 algorithm output structure
- [ ] Apply SC-5 Appendix A recommendations: magical formula REFINE (pool modifiers into one additive sum); physical formula MINOR REORDER (element_conversion before tier_coefficient); off-hand integration into modifier pools

### Item 3 — Substrate weapon binding output (~1-2 days; coordinated with elrond SC-6b)

- [ ] Phase 2c substrate weapon selection result persists to character JSON
- [ ] `gear_representative.main_weapon` includes all 8 substrate weapon fields per SC-6 audit § 2 dispositions:
  - `substrate_weapon_id` (from `weapon_knowledge_entries.id`)
  - `substrate_canonical_name` (from `weapon_knowledge_entries.canonical_name`)
  - `base_physical_damage` (from `weapon_sim_props.base_physical_damage_l50 × damage_amplitude lottery` per Path A)
  - `spell_damage_modifier` (from `weapon_sim_props.spell_damage_modifier_pct`)
  - `element_affinity_modifiers` (from `weapon_sim_props.element_affinity_modifiers_json` OR Phase 2c regex-derive if elrond defers to rocket)
  - `to_skill_level_modifiers` (from `weapon_sim_props.to_skill_level_modifier_static` for unique/named OR rocket per-instance roll for category)
  - `attribute_requirement` (from `weapon_sim_props.primary_stat`)
  - `weapon_type_family` (from `weapon_sim_props.weapon_type_family`)
- [ ] Similar for `secondary_item` for off-hand category items per `off-hand-items-2026-05-24.md`
- [ ] Cross-seam round-trip smoke with elrond SC-6b enrichment columns

### Wave 0.5 closure

- [ ] MIGRATION.md authored per § Cross-seam contract change
- [ ] AGENT_STATE.md updated (generation/AGENT_STATE.md)
- [ ] jack-ryan Gate-2 review of rocket Wave 0.5 outputs
- [ ] Tag: `rocket/v1.5-wave-0-5-track-d-content-emission` (or rocket-OP-preferred tag)
- [ ] Append completion record to this dispatch file
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] Elements expansion: 7 elements available; test season exercises lightning/holy/shadow at substrate-led rates
- [ ] Per-skill emission: chain T1-T3 + T4 capstones emit with full `GeneratedSkill` schema; `damage_scaling_type` populated; `scaling_attribute` populated; placeholder names retained for Phase 5 LLM coalescence
- [ ] Substrate weapon binding: all 8 substrate weapon fields populate on `gear_representative.main_weapon` for representative characters spanning all weapon_type_family values
- [ ] Cross-seam round-trip: gamora damage_resolver consumes `damage_scaling_type` + `scaling_attribute`; star-lord Track C transform (future Wave 5+ work) consumes new substrate weapon fields cleanly
- [ ] MIGRATION.md authored
- [ ] AGENT_STATE.md updated
- [ ] Math-notes authored + jack-ryan Gate-1 PASS pre-implementation
- [ ] jack-ryan Gate-2 PASS post-implementation
- [ ] Completion record appended

## Out of scope (explicit non-goals)

- Do NOT implement damage_resolver / fight engine code (gamora's seam at Wave 0.5)
- Do NOT touch substrate library DB schema (elrond's seam at SC-6b)
- Do NOT touch synthetic_mode flag (gamora's seam at Wave 0.5 RETIREMENT)
- Do NOT touch concentration architecture amendments (rocket Wave 1-2 scope)
- Do NOT touch cohesion-judge LLM (gandalf + star-lord + rocket Wave 3 scope)
- Do NOT implement per-level scaling formulas — Cycle 14 v1 is L50 cap baseline only per doc 41 § 4 #1
- Do NOT regenerate Cycle 13 season (`cycle-13-mechanical-season-001` DISREGARDED per Q9 — fresh Cycle 14 roster at Wave 5)
- Do NOT regress to `synthetic_mode=True` as a time-pressure response — Q10 says extend timeline, not regress (Discipline #39 load-bearing)

## Open questions for rocket to resolve

- **Q-W05-R1**: Coordinate with elrond SC-6b on Path A vs Path B architectural call (audit recommends Path A). Pattern-A sub-agent query at SC-6b kickoff. If Path B chosen, rocket implements engine-side L50 calibration constants table.
- **Q-W05-R2**: For `element_affinity_modifiers` — substrate-side LLM-assisted derivation (SC-6b) OR Phase 2c regex-derive at binding time (rocket scope expansion). Rocket + elrond coordinate at SC-6b kickoff.
- **Q-W05-R3**: For `to_skill_level_modifiers` on category-tier weapons — per-rarity roll formula. Rocket defines + records math.
- **Q-W05-R4**: Hybrid skill `hybrid_pattern` + `hybrid_balance_factor` field population — what hybrid patterns emit for v1 Cycle 14 vs deferred to v1.1+? Rocket decides per `gandalf` math-hotspot consultation OR records as deferred.

## Hive-mind decision-routing reminder

Per Matt 2026-05-23 directive (hive-mind protocol § 4) + scope-doc § 4.1: rocket is autonomous within rocket seam. Cross-seam questions route to seam-owners via Pattern-A sub-agent query (e.g., gamora for damage_resolver expectations; elrond for SC-6b schema details; gandalf for hybrid pattern design; star-lord for Track C transform contract). Matt is LAST-resort escalation.

## References

- `canonical/47-damage-scaling-architecture-2026-05-27.md` (formulas + per-attribute weapon profile)
- `canonical/46-concentration-architecture-2026-05-27.md` (Layer 1 stat-range bounds)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (as amended at `f56ce8b`)
- `canonical/41-progression-framework-2026-05-27.md`
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` (legolas SC-5)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (SC-6 audit)
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md` (parallel SC-6b dispatch)
- `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-14-wave-0-5-damage-routing-synthetic-retirement.md` (parallel gamora dispatch)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 + § 3 + § 6
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 + § 5
- Engineering disciplines #11 + #18 + #19 + #33 + #38 + #39
- Hive-mind protocol § 4 (decision-routing) + § 7 (math hotspots)
