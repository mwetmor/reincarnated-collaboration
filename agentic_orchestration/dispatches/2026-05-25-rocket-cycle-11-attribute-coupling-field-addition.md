# Dispatch — 2026-05-25 — rocket — Cycle 11 attribute_coupling field addition (Wave 2; M4 unblock)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-25 P2c "Approved" (M4 ratified — implementation unblock follows from M4 ratification per scope-discipline § 5.3 in-scope default)
**Estimated effort:** ~1-2 hours
**Acceptance:** `attribute_coupling: list[str]` field added to PlayerClass schema + emitted in class_generator; star-lord serialization auto-pass-through; round-trip smoke PASS

---

## Context

Drax M4 dispatch (Wave 1 fire) ESCALATED — pre-implementation verification confirmed `attribute_coupling` field is NOT PRESENT anywhere (ZERO matches across 11 seasons + engine source + loadout types.ts). The drax loadout scoping memo § 4.3 claim that M4 was "data already present / zero-dependency" was incorrect. M4 in fact requires a generation-seam follow-on to source the data.

Per hive-mind decision-routing § 4, the seam-owner for what class data lives on PlayerClass is **rocket** (generation seam). This dispatch routes the field-addition work to rocket; star-lord's existing class JSON serializer auto-picks-up the new schema field; then drax M4 refires as ~1-2 hour pure display work.

This is Cycle 11 Wave 2 firing in parallel with drax M1/M2/M5 dispatch (which consumes the Wave 1 star-lord schema extensions).

## Required reading before starting

- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m4-attribute-coupling-labels.md` § Completion record (escalation details + drax's verification findings)
- `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § M4 specification (what drax expected to display)
- `~/Games/reincarnated-engine/src/reincarnated/generation/class_schema.py` (current PlayerClass schema)
- `~/Games/reincarnated-engine/src/reincarnated/generation/class_generator.py` (class assembly path)
- Per drax memo § M4: expected data shape `attribute_coupling: ["STR", "DEX"]` — array of stat names indicating which primary stats scale skills for the class

## Math-before-code

**Coupling derivation question — rocket judgment:**

Attribute coupling is a function of class design. Two derivation paths:

**Path A — Derived from existing class attributes:**
- Coupling inferred from `stat_distribution` (the highest-allocated stats are the coupling stats) + `archetype_tag` + `dominant_element`
- Pros: zero new design surface; uses what's already canonical
- Cons: may not match intuitive design intent (e.g., a wisdom-allocated class with fire dominant_element — does coupling lean to WIS or INT?)

**Path B — Explicit canonical coupling per archetype:**
- Each archetype_tag has a canonical coupling pair (or singleton) defined in canonical data
- Pros: explicit design intent; matches loadout language
- Cons: new canonical surface; requires gandalf design input for canonical archetype→coupling mapping

**Recommended (rocket-can-decide): Path A (derived).** Use `stat_distribution` to identify the top-2 allocated attributes per class; emit those as `attribute_coupling: list[str]`. If `stat_distribution` is highly imbalanced (single dominant stat), emit a single-element list. This is the minimum-scope, zero-design-surface path; covers v1 display need; can be refactored to Path B later if gandalf surfaces a design preference.

Document the derivation logic in math-note alongside the existing § 8 math-note.

**Stat-name convention:** match the existing canonical stat names. Likely `strength`, `dexterity`, `intelligence`, `wisdom`, `constitution`, `charisma` (or whatever 6 the engine already uses). Pass-through as strings.

## Cross-seam contract change? (Principle 6 gate)

**YES.** This adds a 5th field to the class JSON export packet. Affects:
- Star-lord export packet (auto-pass-through via existing class_schema.py → season_writer.py serialization, but verify)
- Loadout app consumption (drax M4 refire will consume)

**Round-trip smoke REQUIRED.** Add to acceptance criteria:
- Round-trip smoke: PlayerClass with `attribute_coupling` populated → class JSON written via season_writer → loadout-consumption fixture parses `attribute_coupling` field → list of strings verified

**MIGRATION.md REQUIRED** per ADR-004 — rocket appends to `generation/MIGRATION.md` OR star-lord's `export/MIGRATION.md` § v1.3 (rocket coordinates with star-lord). Document: 5th field addition; consumer compat (null-safe — class without coupling emits empty list `[]` or `null`); derivation logic note.

## Scope

- [ ] Add `attribute_coupling: list[str]` field to PlayerClass dataclass in `class_schema.py`
- [ ] Implement derivation logic in class_generator.py (Path A — derived from stat_distribution top-2 + handling edge cases)
- [ ] Math-note appended documenting derivation logic
- [ ] Verify star-lord serialization auto-picks-up (run season_writer smoke; check field present in JSON output)
- [ ] Round-trip smoke (class JSON written → loadout fixture parses field)
- [ ] MIGRATION.md updated (rocket coordinates with star-lord — recommend appending to star-lord's existing § v1.3 OR adding § v1.4 in generation/MIGRATION.md)
- [ ] AGENT_STATE.md updated
- [ ] Tag: `rocket/v0.0-cycle-11-attribute-coupling-field-2026-05-25`

## Acceptance criteria

- [ ] `attribute_coupling` field present in PlayerClass schema + emitted by class_generator
- [ ] Field appears in class JSON output via season_writer
- [ ] Round-trip smoke PASS (loadout fixture reads field)
- [ ] No regression in existing class JSON consumers
- [ ] No regression in existing PlayerClass generation pipeline
- [ ] MIGRATION.md updated
- [ ] Math-note updated

## Out of scope (explicit non-goals)

- DO NOT design a canonical archetype→coupling mapping (Path B) — defer to v1.1+ if gandalf surfaces a design preference
- DO NOT change `stat_distribution` semantics (consume as-is)
- DO NOT change PlayerClass JSON export for other fields
- DO NOT touch drax loadout-side display (separate refire after this lands)
- DO NOT touch the BC-shift validation sweep (rocket Wave 1 background process still running)

## Open questions for the agent to resolve

- Path A vs Path B derivation choice (rocket judgment per math-before-code analysis above; recommend Path A)
- Single-stat-coupled vs always-pair: if stat_distribution is highly imbalanced, does coupling emit `["intelligence"]` (single) or `["intelligence", "wisdom"]` (paired with next-highest)? Rocket judgment per design intent.
- Field-presence on classes with empty/uniform stat_distribution — empty list `[]` or `null`? Either valid; pick one + document in MIGRATION.md for loadout null-safe consumption.

## References

- M4 escalation record: `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m4-attribute-coupling-labels.md` § Completion record
- Drax memo M4 spec: `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § M4
- Star-lord schema extensions (Wave 1 PASS): `agentic_orchestration/dispatches/2026-05-25-star-lord-cycle-11-schema-extensions.md` § Completion record + `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.3
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 1 (KR autonomous-scope authority for in-scope follow-on dispatches)
- Scope-discipline § 5.3 (ambiguity defaults in-scope): `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md`

---

## Completion record

**Completed:** 2026-05-25
**Tag shipped:** `rocket/v0.0-cycle-11-attribute-coupling-field-2026-05-25`
**Commit:** `eef66b1`

**Derivation chosen:** Path A — `_derive_attribute_coupling()` extracts top-2 stats by allocated value from `StatDistribution`. Ties broken by canonical stat order `[strength, dexterity, intelligence, wisdom, vitality]`. Always emits exactly 2 stat name strings. Never null, never empty list.

**Round-trip smoke:** 5/5 PASS (Discipline #11 empirical inspection)
- `class_generator.generate()` → `PlayerClass.attribute_coupling` = 2-element `list[str]` confirmed
- `_class_to_dict()` → field present in output dict confirmed
- `_validate_class_export()` boundary check PASS (field in `_REQUIRED_CLASS_KEYS`)
- Disk JSON write + `json.load()` roundtrip → field present, correct shape, valid stat names confirmed
- Archetypes tested: fire_mage (seed 42), water_controller (99), fire_mage/rage (7), wind_caster (13), earth_controller (200)

**Regression tests:** 48/48 PASS (test_cycle11_schema_extensions_round_trip.py 40/40 + test_w02_archetype_label_round_trip.py 8/8)

**MIGRATION.md written:** Yes — `src/reincarnated/generation/MIGRATION.md` § [2026-05-25]

**Math note updated:** Yes — `src/reincarnated/generation/math/algorithm-section-8-v1-implementation-2026-05-25.md` § A1 appended (Path A derivation formula, edge cases, code citations per Discipline #1.2)

**Files changed:**
- `src/reincarnated/generation/class_schema.py` — `attribute_coupling: list[str] = []` field added to `PlayerClass`
- `src/reincarnated/generation/class_generator.py` — `_STAT_TIEBREAK_ORDER` + `_derive_attribute_coupling()` added; wired into `generate()`
- `src/reincarnated/output/season_writer.py` — field emitted in `_class_to_dict()`; added to `_REQUIRED_CLASS_KEYS`

**Notes for drax M4 refire:**
- Field is now present in all newly-generated class JSON as `"attribute_coupling": ["stat_a", "stat_b"]`
- Always 2 elements, always valid stat name strings from `{strength, dexterity, intelligence, wisdom, vitality}`
- Legacy class JSON (pre-Cycle-11 seasons) will NOT have this key — drax should guard with `cls.attribute_coupling ?? []`
- No star-lord ExportClass action required for M4 — field flows through season_writer path; drax reads class JSON directly
- BC-shift validation sweep (Wave 1 background, PID 79520) is independent — untouched per out-of-scope clause
