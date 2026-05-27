# Dispatch — 2026-05-27 — elrond — Cycle 14 SC-6b substrate weapon enrichment + MIGRATION.md

**From:** knight-rider
**To:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratified; SC-6 audit completed clean; SC-6b is the deferred enrichment phase decomposed from original SC-6 scope per anti-stall recovery)
**Estimated effort:** ~14-22 hours (per SC-6 audit § 5 estimate — ~11-18 enrichment + ~1 MIGRATION.md + ~1-2 cross-seam smoke + ~1 quality verification)
**Acceptance:** substrate library schema extended per SC-6 audit § 2 per-field dispositions; data backfilled; MIGRATION.md authored per ADR-004; cross-seam round-trip smoke with rocket Phase 2c at Wave 0.5

## Context

Cycle 14 SC-6 audit (elrond) landed clean 2026-05-27 with per-field dispositions validated against doc 47 § 3 substrate weapon binding output requirements. SC-6b is the **deferred enrichment phase** decomposed from the original SC-6 scope after two stalls revealed that audit + enrichment + MIGRATION + cross-seam coordination was too large for a single dispatch.

SC-6b fires **IN PARALLEL with Wave 0.5** (rocket per-skill emission + substrate weapon binding output + gamora damage scaling routing). Elrond is in Wave 0.5 owners per framing brief § 2; SC-6b is elrond's Wave 0.5 contribution. Cross-seam coordination with rocket happens via MIGRATION.md per ADR-004 + Pattern-A sub-agent query at SC-6b kickoff (per audit § 5 recommendation: surface family-baseline LUT calibration expectations before backfill runs).

The load-bearing architectural finding (per audit § 1.6): **`damage_amplitude_min/max` is a RATIO (0.3-3.0), NOT absolute physical damage**. Doc 47 § 4.2's `weapon.base_physical_damage` formula consumes absolute HP values, not ratios. SC-6 audit recommends **Path A** — substrate library adds `base_physical_damage_l50` absolute column (per-weapon-family L50 baseline × `damage_amplitude` ratio yields the final value at gen time). SC-6b implements Path A unless rocket Pattern-A query at kickoff surfaces a reason to prefer Path B.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` — SC-6 audit report (§ 1 substrate state; § 2 per-field dispositions; § 4 cross-seam impact; **§ 5 recommended SC-6b scope** — this is the substantive spec)
- `agentic_orchestration/elrond/sc-6-progressive-findings-2026-05-27.md` — KR-authored progressive findings + DB diagnostic anchor
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6-substrate-weapon-stat-audit.md` — SC-6 audit dispatch + completion record
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile spec) + § 4 (formulas consuming the audited stats)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (stat-range bounds — substrate stats respect bounds)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 3.3 (substrate weapon binding output spec)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 Wave 0.5
- `agentic_orchestration/GOVERNANCE.md` ADR-004 (cross-repo coordination + MIGRATION.md requirement)
- `.claude/skills/reincarnated-elrond-operating-procedure`
- `.claude/skills/reincarnated-hive-mind-protocol`

## Math-before-code

Per-family L50 baseline LUT is the load-bearing calibration math. Recommend authoring a math-note at `~/Games/reincarnated-loadout/data/schema/sc-6b-baseline-lut-math-2026-05-27.md` (or elrond's preferred location) documenting:
- Per-weapon-family L50 baseline values (recommendation: greatsword ~200 / longsword ~150 / dagger ~100 / staff ~50 / wand ~40 / etc.)
- Derivation: align with doc 47 § 3.1 absolute physical-damage ranges per family (STR heavy melee 100-300; DEX light/ranged 60-150; INT/WIS casters 20-80)
- Cross-check: rocket Pattern-A query confirms engine-side calibration expectations match substrate-side baseline

## Cross-seam contract change? (Principle 6 gate)

**YES** — enrichment adds NEW columns to substrate library tables (specifically `weapon_sim_props`):

- `base_physical_damage_l50` (REAL, HP points; Path A)
- `spell_damage_modifier_pct` (REAL, percent)
- `element_affinity_modifiers_json` (TEXT, JSON `{"element": pct, ...}`)
- `to_skill_level_modifier_static` (TEXT, JSON `{"skill_type": modifier}`, NULL for category rows)
- `weapon_type_family` (TEXT, CHECK against doc 47 6-enum: martial-heavy / martial-light / ranged / caster-arcane / caster-faith / hybrid)

**MIGRATION.md REQUIRED per ADR-004** — author at `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md` (or elrond-OP-preferred location) capturing:
- New columns + schema rationale + downstream consumer expectations (rocket Phase 2c at Wave 0.5; gamora damage_resolver consuming these via rocket-emitted character JSON at Wave 0.5)
- Backfill scope (~2,293 v1_scope rows; algorithmic for 96.5%; manual review for ~81 edge cases)
- Round-trip clause: "rocket Phase 2c substrate query consumes new `weapon_sim_props` columns; per-character `gear_representative.main_weapon` contains base_physical_damage / spell_damage_modifier / element_affinity_modifiers / to_skill_level_modifiers / attribute_requirement / weapon_type_family fields with non-null values for the substrate rows that drove selection."

## Scope

- [ ] **Pre-kickoff** — invoke rocket Pattern-A sub-agent query (KR can facilitate via SendMessage if elrond requests; OR elrond invokes directly per hive-mind protocol § 4 sub-agent decision-routing): "what L50 calibration constants does engine-side damage_resolver expect from substrate base_physical_damage_l50? Does Path A substrate-side baseline align with engine assumptions OR does Path B engine-side calibration prefer?"
- [ ] Author per-weapon-family L50 baseline LUT (math-note) per § Math-before-code above
- [ ] Apply schema extension to `weapon_sim_props` (additive; ALTER TABLE ADD COLUMN for each of the 5 new columns)
- [ ] Backfill data for ~2,293 v1_scope rows:
  - [ ] `base_physical_damage_l50` — per-family baseline LUT × 1.0 (or `damage_amplitude_min/max` integrated with LUT — per audit § 2 + rocket Pattern-A clarification)
  - [ ] `spell_damage_modifier_pct` — algorithmic by `primary_stat`: INT 30-150 / WIS 30-120 / STR 0-10 / DEX 0-10 (per audit § 2 disposition)
  - [ ] `element_affinity_modifiers_json` — martial = `{}`; caster 327 rows = LLM-assisted from `canonical_name` parsing (e.g., "Rod of Icicles" → `{"water": 15}`) OR regex-based derivation OR leave NULL with rocket Phase 2c regex-derive
  - [ ] `to_skill_level_modifier_static` — NULL for `weapon_kind='category'` (1,139 rows); curated JSON for `weapon_kind IN ('unique', 'named_template')` (~969 rows); LLM-assisted authoring against mythological reference (e.g., Gáe Bolg → `{"spear": 1}`, Mjölnir → `{"hammer": 2}`)
  - [ ] `weapon_type_family` — algorithmic rule on `(primary_stat, proxy_range_class, weapon_kind_classified_subtype)` per audit § 2.1 top-20 mapping table covering 96.5%; ~81 edge cases flagged for manual review
- [ ] Author MIGRATION.md per ADR-004
- [ ] Cross-seam round-trip smoke: rocket Phase 2c at Wave 0.5 consumes new columns; verify per-character `gear_representative.main_weapon` populates all 6 fields
- [ ] Update SC-6 audit report (or sibling SC-6b implementation report) at `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6b-substrate-enrichment-implementation.md` documenting:
  - [ ] LUT values + derivation
  - [ ] Backfill algorithm per field
  - [ ] Edge-case manual review outcomes
  - [ ] Round-trip smoke result
- [ ] Append completion record to this dispatch file per dispatches/README.md
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] 5 new columns added to `weapon_sim_props` with appropriate types + CHECK constraints
- [ ] All 2,293 v1_scope rows backfilled (or explicit NULL disposition for `element_affinity_modifiers_json` martial / `to_skill_level_modifier_static` category — documented in MIGRATION.md)
- [ ] MIGRATION.md authored + cross-references doc 47 + SC-6 audit + this dispatch
- [ ] Round-trip smoke: rocket Phase 2c at Wave 0.5 produces character JSON with all 6 doc-47-required fields populated (or explicit-null with rationale)
- [ ] SC-6b implementation report filed
- [ ] Completion record appended; commit + push

## Out of scope (explicit non-goals)

- Do NOT touch character JSON output schema (rocket's seam at Wave 0.5 Phase 2c)
- Do NOT touch damage_resolver / fight engine code (gamora's seam at Wave 0.5)
- Do NOT touch substrate acquisition pipeline (Phase 1 substrate import)
- Do NOT enrich `weapons` table (5,162 rows; NOT the v1_scope substrate per SC-6 audit § 1.4 — 98.2% miss-rate)
- Do NOT recompute per-level scaling — Cycle 14 v1 is L50 cap baseline only per doc 41 § 4 #1
- Do NOT enter Phase D cleaning execution mode — targeted enrichment for SC-6b scope only
- Do NOT touch substrate clustering / labeling — orthogonal seam work
- Do NOT block on Path A vs Path B uncertainty — if rocket Pattern-A query reveals Path B is preferred, route back via KR for scope amendment

## Anti-stall discipline (per SC-6 NARROW recovery learnings)

1. **Dump intermediate findings incrementally** — write SC-6b implementation report file as you go (header + LUT + per-field section as you backfill); don't buffer for end-of-session write
2. **Per-field batching** — complete one field's backfill + report section + commit increment before moving to next; survives session boundaries
3. **For LLM-assisted enrichment (element_affinity_modifiers, to_skill_level_modifier_static on named_template rows)**: batch in chunks of ~50 rows per LLM call OR defer to a follow-on dispatch if LLM coordination is too heavy for this session
4. **If you encounter scope-expansion (e.g., realize Path B is needed, or ~81 edge cases balloon to ~500)**: STOP and surface to KR for scope amendment — do NOT push through

## Open questions for elrond + cross-seam coordination

- **Q-SC6b-1**: Path A vs Path B final architectural call (audit recommends Path A; rocket Pattern-A query at kickoff confirms or amends)
- **Q-SC6b-2**: element_affinity_modifiers_json approach — substrate-side LLM-assisted derivation vs rocket Phase 2c regex-derive at binding time. Elrond + rocket coordinate per audit § 2 row 3 disposition refinement options.
- **Q-SC6b-3**: to_skill_level_modifier_static curation — full curation of all ~927 named_template rows OR sample 100 high-quality named/unique entries first + defer remainder? Elrond decides per available bandwidth + Q10 quality > timeline.
- **Q-SC6b-4**: ~81 edge cases for weapon_type_family — manual review OR algorithmic fallback to most-common-family-by-primary_stat? Elrond decides per audit + records rationale.

## References

- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` — SC-6 audit (substantive spec basis)
- `agentic_orchestration/elrond/sc-6-progressive-findings-2026-05-27.md` — KR diagnostic anchor
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 + § 4
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 3.3 + § 5 SC-6 disposition
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 Wave 0.5
- `agentic_orchestration/GOVERNANCE.md` ADR-004 (MIGRATION.md cross-seam coordination)
- Engineering disciplines #11 + #18 + #19 + #38 (damage-scaling-path; doc 47 § 6 canonical write via SC-1)
- Hive-mind protocol § 4 (seam decision-routing) + § 10.2 (mid-phase specialist recovery)
