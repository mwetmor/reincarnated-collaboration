# Dispatch — 2026-05-27 — elrond — Cycle 14 SC-6 substrate weapon stat audit + enrichment

**From:** knight-rider
**To:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratified — sidecar list confirmed including SC-6)
**Estimated effort:** ~6-10 hours audit + enrichment (depends on enrichment depth)
**Acceptance:** substrate weapon library audited for the per-skill-damage-scaling-required fields; enrichment landed where gaps exist; audit + enrichment report filed at `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md`

## Context

Cycle 14 Wave 0.5 implements doc 47 damage scaling architecture (physical / magical / hybrid routing). Per framing brief § 3.3 substrate weapon binding output, the character JSON's `gear_representative.main_weapon` will gain new fields including `base_physical_damage` / `spell_damage_modifier` / `element_affinity_modifiers` / `to_skill_level_modifiers` / `attribute_requirement` / `weapon_type_family`.

For rocket to emit these fields at Wave 0.5 Phase 2c substrate binding, the substrate weapon library MUST EXPOSE these stats. If the substrate library is missing any of these stats, the binding output will fall back to nulls or defaults, breaking doc 47's per-attribute weapon profile architecture (e.g., wooden staff should have low base_physical_damage but high spell_damage_modifier; greatsword should have high base_physical_damage but low spell_damage_modifier).

This sidecar gates Wave 0.5 (per framing brief § 5 SC-6 entry: "Wave 0.5 gate"). Elrond audits the substrate library for stat-exposure coverage; enriches where gaps exist; reports audit + enrichment outcome so rocket + gamora know which fields are population-ready when Wave 0.5 implementation fires.

The substrate library lives in catalogue DB (elrond's seam). The cross-seam boundary with rocket (engine consumer) is at the Phase 2c substrate selection query → rocket reads stat-exposed substrate rows. Cross-seam contract change WILL occur if elrond adds new columns to substrate weapon tables — MIGRATION.md required per ADR-004.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — particularly § 3 (per-attribute weapon profile) + § 2 (damage formulas reference the audited stats) + § 5 (doc 40 amendments — implications for substrate stat exposure)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — Option α martial 5-tuple / Option β caster attribute-level / Option C cross-attribute ω-penalty
- `canonical/story/skill-system-2026-05-24.md` — composition pattern + tier_coefficient
- `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system + per-attribute weapon expectations
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (stat-range bounds — substrate stats respect bounds)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 3.3 (substrate weapon binding output spec) + § 5 SC-6
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 Wave 0.5
- `.claude/skills/reincarnated-elrond-operating-procedure` — Mode + procedure
- Substrate library DB schema (current state) — elrond inspects directly via DB query

## Math-before-code

This is data-architecture work, not math hotspot per se. Elrond's audit + enrichment is the prerequisite for rocket + gamora's Wave 0.5 implementation; without stat exposure, doc 47 formulas have nothing to scale from. The audit is methodology-validation-at-source — does the substrate library carry the stats doc 47 requires?

## Cross-seam contract change? (Principle 6 gate)

Does this dispatch add, modify, rename, or remove any field on:
- A telemetry schema table — **NO**
- A fight_log dict key — **NO**
- A loadout dict key — **NO** (substrate library schema is elrond's seam; binding to character JSON is rocket's Wave 0.5 work)
- An export packet structure — **NO**
- Any other inter-seam fixture dict — **POSSIBLY** (substrate library schema is the contract elrond → rocket; enrichment adds new columns)

**If YES (enrichment adds new columns):** MIGRATION.md required per ADR-004; cross-seam round-trip smoke at Wave 0.5 when rocket consumes new columns; round-trip clause = "rocket Phase 2c substrate query consumes new substrate columns; per-character gear_representative.main_weapon contains base_physical_damage / spell_damage_modifier / etc. fields with non-null values for the substrate rows that drove selection."

**This dispatch authorizes elrond to write MIGRATION.md for the substrate library schema extension if enrichment adds new columns.** Capture the new columns + schema rationale + downstream consumer expectations (rocket Phase 2c at Wave 0.5).

## Scope

- [ ] Audit substrate weapon library DB schema for current stat exposure
- [ ] Map current schema fields against doc 47 § 3 required stats:
  - [ ] `base_physical_damage` (numeric; per-weapon)
  - [ ] `spell_damage_modifier` (pct; per-weapon; varies by weapon_type_family)
  - [ ] `element_affinity_modifiers` (dict of element → pct; per-weapon)
  - [ ] `to_skill_level_modifiers` (count; per-weapon; varies by weapon_type_family)
  - [ ] `attribute_requirement` (enum: STR / DEX / INT / WIS; per-weapon)
  - [ ] `weapon_type_family` (enum: martial-heavy / martial-light / ranged / caster-arcane / caster-faith / hybrid)
- [ ] For each missing field, design enrichment approach (default value rules / per-weapon-type computed rules / per-row manual annotation / source-data-extraction)
- [ ] Apply enrichment to substrate library (additive schema extension; preserves existing data)
- [ ] Write MIGRATION.md per ADR-004 if schema extended
- [ ] File audit + enrichment report at `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` per § 7 below
- [ ] Append completion record to this dispatch file
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] Audit complete — each of 6 doc-47-required fields confirmed present or marked as gap
- [ ] Enrichment landed for gaps (either schema extension + data backfill OR rationale for why this field can be computed from existing data at rocket Phase 2c query time)
- [ ] MIGRATION.md authored if schema extended; cross-references doc 47 + framing brief + this dispatch
- [ ] Audit report filed at `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` per § 7 below
- [ ] Round-trip smoke: substrate library query (or DB inspection) confirms post-enrichment all 6 fields populate for representative weapon rows spanning each weapon_type_family
- [ ] Completion record appended

## Out of scope (explicit non-goals)

- Do NOT touch character JSON output schema — that's rocket's seam at Wave 0.5 Phase 2c
- Do NOT touch damage_resolver — that's gamora's seam at Wave 0.5
- Do NOT touch the substrate library acquisition pipeline (Phase 1 substrate import) — this is post-import enrichment work only
- Do NOT touch other substrate library tables (gear modifiers / set definitions / etc.) — weapon stats only this dispatch
- Do NOT recompute per-level scaling — Cycle 14 v1 is L50 cap baseline only per doc 41 § 4 #1
- Do NOT enter Phase D cleaning execution mode (per elrond OP) — this is targeted stat audit + enrichment

## Open questions for elrond to resolve

- **Q-SC6-1**: Are the 6 required fields naturally derivable from existing substrate library columns (e.g., weapon_type → attribute_requirement is a lookup; weapon_type → base_physical_damage range can be a per-type baseline) OR does the substrate library need per-weapon-row stat exposure? Elrond decides per audit findings + records rationale.
- **Q-SC6-2**: For `element_affinity_modifiers` — does the substrate library carry per-weapon element affinity OR is this a generated-at-binding-time stat (e.g., "fire wand" gets +%fire affinity at binding)? Elrond decides per substrate semantics + records rationale.
- **Q-SC6-3**: How should `to_skill_level_modifiers` be exposed — per-weapon static value (substrate library) OR per-rarity-tier roll at gear instance gen time (rocket Wave 0.5)? Elrond + rocket coordinate at audit-report time; if rocket needs to be looped in, elrond commissions Pattern-A sub-agent query OR coordinates via knight-rider.
- **Q-SC6-4**: For `weapon_type_family` — is the existing substrate library's weapon_type column the same granularity as doc 47's `weapon_type_family` (martial-heavy / martial-light / ranged / caster-arcane / caster-faith / hybrid) OR does mapping work need to happen? Elrond decides + records mapping table if needed.

## References

- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile spec) + § 2 (formulas)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (Option α / β / C cell-type matching)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (stat-range bounds; substrate stats respect bounds)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 3.3 + § 5 SC-6
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 Wave 0.5 substrate weapon binding output
- `agentic_orchestration/GOVERNANCE.md` ADR-004 (cross-repo coordination + MIGRATION.md requirement)
- Engineering disciplines #11 + #18 + cross-seam interface discipline
