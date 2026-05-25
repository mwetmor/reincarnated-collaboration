# Dispatch — 2026-05-25 — star-lord — Cycle 11 schema extensions (4 fields)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-05-25 (P2c ratification — "Approved")
**Estimated effort:** ~1.75-3.25 days
**Acceptance:** 4 fields added to class JSON export; round-trip smoke confirms fields land in loadout-consumable shape

---

## Context

Cycle 11 v1 implementation push includes 4 schema extensions to the class JSON export bridging engine output ↔ loadout consumption. Per drax loadout scoping memo § 4.3, these fields gate downstream drax Wave-2 + Wave-3 work (M1/M2/M5 + M3/M6 respectively).

The 4 fields:

| Field | Type | Gates drax item | Source |
|---|---|---|---|
| `t4_alteration_output` | Algorithm § 8 alteration descriptor (struct per legolas methodology § 3.1 AlterationOutput) | M3 (T4 alteration + SkillTree) + M6 (T4 comparison panel) | Algorithm § 8 implementation (rocket dispatch separately) |
| `main_weapon` | Weapon descriptor (main slot per v1 substrate composition policy + Sidecar A weapon pass) | M1 (Main weapon + WeaponSlot display) | v1_scope weapon binding (substrate-curation Cycle 10 output) |
| `secondary_item` | Off-hand item descriptor (per Sidecar B off-hand substrate) | M2 (Off-hand item + OffHandSlot display) | Sidecar B off-hand substrate (Cycle 10 closed) |
| `source_library` | Substrate-source attribution string (e.g., "engine_authored_gap_fill_v1", "met_museum", "fextralife", etc.) | M5 (Provenance flag display badge) | Substrate row's existing `source` field (pass-through) |

This dispatch is fired in parallel with rocket § 8 implementation (the two converge at M3/M6 dependency). The `t4_alteration_output` field schema MUST be aligned with rocket's actual Algorithm § 8 output shape — sub-agent coordination with rocket required at schema authoring time.

This is Cycle 11 Wave 1; fired in parallel with pre-migration mitigation + Drax M4 + jack-ryan decisions-log batch + rocket § 8.

## Required reading before starting

- `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § 4.3 (schema extension specification)
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c (Matt verbatim authorization)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` § 3.1 (AlterationOutput struct shape — informs `t4_alteration_output` field schema)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 2-3 (main_weapon vs secondary_item conventions)
- `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-sidecar-b-off-hand-substrate.md` § completion record (Sidecar B output — informs `secondary_item` shape)
- `~/Games/reincarnated-engine/src/reincarnated/export/season_writer.py` (current class JSON shape)
- `~/Games/reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` (star-lord seam state)

## Math-before-code

No mathematical computation. Schema design judgment:

**`t4_alteration_output` shape** (align with rocket § 8 implementation):
- Per legolas methodology § 3.1, `AlterationOutput` is a struct containing: strategy_type (enum), strategy_params (dict), applied_axis_targets (list), η_score (float), thematic_rationale (string). Star-lord JSON shape should mirror this for round-trippability.
- **Coordination required:** star-lord MUST consult rocket sub-agent BEFORE finalizing `t4_alteration_output` JSON shape — rocket's actual struct may differ from legolas methodology proposal. Star-lord verifies via rocket sub-agent invocation OR by reading the rocket § 8 implementation dispatch acceptance criteria once authored.

**`main_weapon` + `secondary_item` shape:**
- Pass-through of substrate-row weapon descriptors. Required sub-fields: `weapon_id`, `name`, `category` (melee/polearm/ranged/firearm/...), `source_library`, `cultural_register`, `period`, `lineage` (per substrate composition policy v1 § 2-3).
- Some classes will have only `main_weapon` (no off-hand) — `secondary_item: null` valid.
- Per Matt Q3 ratification: T4 post-mortem proceeds with **main weapon only**; off-hand display added for v1.0 production launch (post-Sidecar-B-loadout-integration). Schema MUST support both fields now; M2 drax work surfaces off-hand UI later.

**`source_library` shape:**
- Simple pass-through string from substrate row's existing `source` column. Examples: `"engine_authored_gap_fill_v1"`, `"met_museum"`, `"fextralife_ds2"`, `"odin_army_tradoc"`, `"wikidata_named_weapon"`.
- Per Matt Q1 ratification: `v1_scope` flag kept INTERNAL; `source_library` (provenance badge data) is VISIBLE in loadout. This field is the visible-badge source — `v1_scope` boolean stays engine-internal.

## Cross-seam contract change? (Principle 6 gate)

**YES.** This dispatch ADDS 4 fields to the class JSON export packet, which star-lord owns. Affects:
- Star-lord export packet structure (season_writer.py output)
- Loadout app consumption (drax M1, M2, M3, M5, M6 all read these fields)
- Potentially: engine-internal class assembly (whether the fields come from rocket vs. substrate binding vs. pass-through)

**Round-trip smoke REQUIRED.** Acceptance criteria below MUST include:
- Round-trip smoke: production-path class JSON written by season_writer → consumed by loadout app fixture → field-presence + shape check on all 4 new fields → null-case smoke for classes without `secondary_item` AND classes without `t4_alteration_output` (pre-rocket-§-8 baseline)

**MIGRATION.md REQUIRED** per ADR-004 — star-lord authors a MIGRATION.md note documenting:
- 4 new fields added; consumers must handle missing-field case (additive forward-compat per Variant C precedent)
- `t4_alteration_output` shape coordinated with rocket § 8 implementation (note rocket's actual struct)
- `secondary_item: null` is a valid value for classes without off-hand

## Scope

- [ ] Add `t4_alteration_output` field to class JSON export (struct per coordination with rocket sub-agent)
- [ ] Add `main_weapon` field to class JSON export (substrate-row weapon descriptor passthrough)
- [ ] Add `secondary_item` field to class JSON export (Sidecar B off-hand passthrough; nullable)
- [ ] Add `source_library` field to class JSON export (substrate `source` column passthrough)
- [ ] Update season_writer.py emission logic
- [ ] Round-trip smoke (production-path → loadout-consumption fixture → field-presence check)
- [ ] MIGRATION.md authored per ADR-004
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `star-lord/v0.1-cycle-11-schema-extensions-2026-05-25`

## Acceptance criteria

- [ ] All 4 fields present in season_writer.py class JSON output for a smoke class
- [ ] `secondary_item: null` case smoke passes (class without off-hand)
- [ ] `t4_alteration_output` shape verified against rocket § 8 implementation OR documented as v1.1 forward-compat placeholder if rocket § 8 hasn't landed yet
- [ ] **Round-trip smoke:** production-path class JSON written → loadout-consumption fixture parses → all 4 new fields present with correct shape OR null-case handled
- [ ] MIGRATION.md authored documenting additive schema extensions + consumer compat notes
- [ ] No regression in existing class JSON consumers (loadout app stats display + analytics suite if active)

## Out of scope (explicit non-goals)

- DO NOT fire Algorithm § 8 implementation (rocket dispatch separately)
- DO NOT implement loadout-side display of new fields (drax dispatches separately M1/M2/M3/M5/M6)
- DO NOT migrate to Postgres (P2a "right moment" deferred)
- DO NOT add additional fields beyond the 4 enumerated
- DO NOT change `v1_scope` boolean visibility (Q1 RATIFIED: internal; provenance badge via `source_library` is the visible surface)
- DO NOT deploy to production Vercel (Q5 RATIFIED: preview-only for T4 post-mortem)

## Open questions for the agent to resolve

- Coordination with rocket sub-agent on `t4_alteration_output` shape — when authoring, invoke rocket sub-agent OR read rocket § 8 implementation dispatch (`2026-05-25-rocket-cycle-11-algorithm-section-8-implementation.md`) once authored. If rocket § 8 hasn't landed by the time schema work completes, use legolas methodology § 3.1 AlterationOutput struct as v1 placeholder + document forward-compat path in MIGRATION.md.
- Decision on field nullability: `secondary_item: null` (class without off-hand) is REQUIRED valid; `t4_alteration_output: null` (pre-rocket-§-8 class or class without alteration) MUST also be valid. Round-trip smoke must cover both null cases.
- Whether `main_weapon` is required-non-null OR also nullable (per v1 substrate composition policy, every class has a main weapon — likely required-non-null; star-lord verifies against substrate-binding output).

## References

- Matt verbatim: "Approved" (P2c — `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c)
- Drax loadout scoping: `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § 4.3
- Algorithm § 8 methodology: `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` § 3.1
- Sidecar B off-hand substrate: `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-sidecar-b-off-hand-substrate.md`
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 1
- ADR-004 (MIGRATION.md cross-seam): `agentic_orchestration/GOVERNANCE.md`
