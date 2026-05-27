# Dispatch — 2026-05-27 — rocket — Cycle 13 Wave 4 Track A Spec-Driven Gear Gen Implementation (W4R.0-W4R.7 Bundled)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-27 + jack-ryan Wave 4 Track A Gate-1 PASS-with-WARN verdict (commit `a149001`) + gandalf W1 clarification landed (commit `17ce1be`; Option A enum extension at W4R.1) + W2/I1/I3 KR fold-ins
**Estimated effort:** ~12-24 hrs bundled implementation (8 sub-waves W4R.0-W4R.7 per doc 45 § 9; smaller than Wave 1's 9 sub-waves; rocket may sub-checkpoint)
**Acceptance:** Wave 4 Track A spec-driven gear gen landed per doc 45 amended (§ 7.1 W1 resolution + § 9 sub-wave structure W4R.0-W4R.7); per-rarity gear instance generation (10 tiers) + T4-attunement content-compositional annotation + triggered-passive added skills on legendaries per D55 + modifier-surface expansion per D56 + capability toolkit legendary-exclusive (6-member enum post-W4R.1 extension) + set bonus structure + cross-cohesion validation + round-trip smoke per Principle 6 including all 10 rarity tiers

## Context

Cycle 13 Wave 4 Track A = spec-driven gear gen per framing brief § 3 Wave 4 + doc 40 § 3 + doc 45 amended (commits `a4faa20` + `17ce1be`) + jack-ryan Wave 4 Track A Gate-1 PASS-with-WARN verdict (commit `a149001`).

**Per jack-ryan Wave 4 Track A Gate-1 fold-ins (REQUIRED in THIS dispatch per next-action sequence):**

- **W1 RESOLVED (gandalf clarification commit `17ce1be` — Option A):** `MULTIPLICATIVE` is a Wave 4 `CapabilityCategory` enum extension added at W4R.1. Implementation:
  - W4R.1: extend `CapabilityCategory` enum in `partition_schema.py:376-381` to add `MULTIPLICATIVE = "multiplicative"` member; len 5→6
  - Module-load assert `assert len(CapabilityCategory) == 6` (companion to existing assertions)
  - MIGRATION.md filing per ADR-004 (enum extension is additive non-breaking schema change)
  - Doc 40 § 3.3 canonical taxonomy preserved at implementation: MULTIPLICATIVE + MECHANIC_ADJUSTING + SPATIAL_ADJUSTING + AXIS_ADJUSTING + TRIGGERED_PASSIVE + TRUE_ACTIVE = 6
  - Semantic distinction (per doc 45 amended): MULTIPLICATIVE = auto-applied passive scalar on matching T4 path; TRUE_ACTIVE = player-activated skill on skill-bar consuming additive base-skill-budget slot
  - W4R.4 acceptance criterion: capability toolkit legendary-exclusive enforcement spans 6 members (not 5)

- **W2 KR FOLD-IN (REQUIRED in W4R.3 acceptance criteria):** accessory pattern library OMITS true-active entry entirely; weapon library contains true-active entries. Rocket W4R.3 implementation must NOT generate conditional-gated stubs for accessory true-active; instead omit the entry from accessory pattern library at module-load time.

- **I1 INFO (KR FOLD-IN in W4R.3):** minimum **≥5 patterns per slot family** in W4R.3 pattern library (per jack-ryan Gate-1 I1 INFO). Verify empirically: weapon ≥5 patterns; armor ≥5; accessory ≥5.

- **I3 INFO RESOLVED:** star-lord Wave 4 export schema update LANDED (engine commit `8dbb808`; 6 fields added; 118/118 round-trip smoke PASS; W4G.5 gate cleared). Rocket Wave 4 Track A outputs (e.g., `PartitionGearInstance` with new fields) integrate with star-lord schema cleanly per § 11 6-surface coordination.

**Carryover from Wave 3 (preserved):**
- legendary_t0_5 rarity in W4R.7 round-trip smoke (all 10 rarity tiers per doc 45 § 3.1 + § 10.3 module-load assert)
- WARN-pattern PRESERVED status (per Wave 3 Gate-2 milestone); Wave 4 maintains 100% accurate post-script empirical count assertions

## Required reading before starting

1. `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` amended (W1 § 7.1 + § 9 W4R.1 + § 10.3 per commit `17ce1be`)
2. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-1-doc-45-critique.md` (Gate-1 verdict; W1+W2+I1+I3 fold-in specifics)
3. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` (Wave 3 Gate-2 PASS; WARN-pattern PRESERVED)
4. `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended (Wave 3 T4 scope-dimension; T4CandidateV2 fields)
5. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 T4 algorithm)
6. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 partition schema; gear gen consumes)
7. `canonical/41-progression-framework-2026-05-27.md` (L50 hybrid + cell × node × cohort)
8. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 + D7+D8+D33+D38+D51+D55+D56+D48-D52 (architectural foundation)
9. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 3 (Block B substantive locks)
10. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #26 + #27 + #29 + #30 + #31 + #32 + Principle 6)
11. `agentic_orchestration/operating-procedures/rocket.md` (operating procedure)
12. Existing engine code paths (Wave 1+2+3 implementation; Wave 4 Track A extends):
    - `reincarnated-engine/src/reincarnated/generation/partition_schema.py` (Wave 1; gear gen consumes; `PartitionRarity` 10-tier enum + `PartitionGearInstance`; W4R.1 enum extension target lines 376-381)
    - `reincarnated-engine/src/reincarnated/generation/partition_modifier_pool.py` (Wave 1; modifier surface)
    - `reincarnated-engine/src/reincarnated/generation/partition_roller.py` (Wave 1; modifier rolling)
    - `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (Wave 2+3; T4 attunement annotation source; T4CandidateV2)
    - `reincarnated-engine/src/reincarnated/generation/t4_scope_selector.py` (Wave 3; scope-dimension)
13. Star-lord Wave 4 export schema (engine commit `8dbb808`): `reincarnated-engine/src/reincarnated/export/` for `ExportAlterationOutput` + `ExportSimCyclingQualityReport`

## Math-before-code (#1 — REQUIRED)

Per Discipline #1 math-before-code, before W4R.1 implementation:

- [ ] Document the `CapabilityCategory` enum extension math (W1 Option A): 5 → 6 members; new MULTIPLICATIVE member semantic = auto-applied passive scalar on matching T4 path (per doc 45 § 7.1 amended)
- [ ] Document per-rarity gear instance generation math (W4R.2): per-rarity modifier count + categories rollable per doc 45 § 3.1 (10 tiers)
- [ ] Document T4-attunement annotation math (W4R.3): content-compositional model (annotation as metadata; gear content IS attunement per doc 45 § 4)
- [ ] Document triggered-passive added-skill generation math (W4R.4): per D55 high-probability calibration anchors + W2 fold-in (accessory pattern library OMITS true-active entry)
- [ ] Document modifier-surface expansion math (W4R.5): per D56 legendary-exclusive new stat types
- [ ] Document capability toolkit legendary-exclusive enforcement math (W4R.6): per 6-member enum (post-W4R.1 extension); legendary T0-T2 only
- [ ] Document set bonus structure math (W4R.7): 2pc minor always-active + 4pc full T4-attuned per closeout § 3.4
- [ ] Document cross-cohesion validation math: 4 cohorts × 10 rarity tiers × N samples per doc 45 § 9 + Wave 1 W1.7 cross-cohesion precedent

## Cross-seam contract change? (Principle 6 gate)

**Round-trip REQUIRED.** Wave 4 Track A introduces NEW schema (PartitionGearInstance with W4R.1 enum extension + uniques metadata flag `is_unique` per doc 45 § 3.2 + T4-attunement annotation per content-compositional model + triggered-passive added-skill content + set bonus rank). Composes with Wave 1 partition + Wave 2+3 T4 architecture + star-lord export schema (engine commit `8dbb808`).

**Round-trip smoke:** generate ≥N kits with full gear instance set across all 10 rarity tiers (per doc 45 § 3.1 module-load assert `len(PartitionRarity) == 10`); verify field-presence + type-consistency; verify capability toolkit legendary-exclusive enforcement (6-member enum); verify T4-attunement annotation metadata propagates; export-roundtrip via star-lord schema.

**MIGRATION.md required** per ADR-004 (enum extension W4R.1 + new fields).

## Scope (W4R.0-W4R.7 sub-wave structure per doc 45 § 9 amended)

### W4R.0 — Substrate prep + repo-scaffold

- [ ] Review Wave 1+2+3 implementation (engine commits `2aa6813` + `2445bad` + `7287b43` + `2e8bc33`); identify integration points for spec-driven gear gen
- [ ] Scaffold spec-driven gear gen modules per doc 45 § 9 W4R.0

### W4R.1 — `CapabilityCategory` enum extension + module-load assert + MIGRATION.md (per W1 Option A)

- [ ] Extend `CapabilityCategory` enum in `partition_schema.py:376-381` to add `MULTIPLICATIVE = "multiplicative"` member (len 5→6)
- [ ] Module-load assert `assert len(CapabilityCategory) == 6`
- [ ] MIGRATION.md per ADR-004 (enum extension is additive non-breaking)
- [ ] Math-note per Discipline #1 BEFORE W4R.2

### W4R.2 — Per-rarity gear instance generation (per doc 45 § 3.1; 10 tiers)

- [ ] Implement per-rarity gear instance generation algorithm across all 10 `PartitionRarity` tiers (Common / Uncommon / Rare / Epic / Legendary T0-T0.5-T1-T2 / Set T1-T2)
- [ ] Implement uniques sub-category metadata flag `PartitionGearInstance.is_unique: bool` per doc 45 § 3.2
- [ ] Per-rarity modifier count + categories rollable per doc 45 § 3.1
- [ ] Unit test: generation produces field-complete instances at all 10 tiers

### W4R.3 — T4-attunement annotation per content-compositional model (per doc 45 § 4)

**Per W2 KR fold-in (REQUIRED):** accessory pattern library OMITS true-active entry; weapon library contains.

**Per I1 KR fold-in (REQUIRED):** minimum **≥5 patterns per slot family** (weapon ≥5; armor ≥5; accessory ≥5).

- [ ] Implement T4-attunement annotation field on `PartitionGearInstance` (metadata; content-compositional per closeout § 3.4)
- [ ] Implement pattern library per slot family (weapon / armor / accessory) with minimum 5 patterns each
- [ ] **Accessory pattern library: OMIT true-active entry entirely (per W2)**; weapon pattern library: include true-active entries
- [ ] Algorithm uses annotation for drop pool restriction (D50) + spirit-guide projection (D34) + algorithm-side optimization

### W4R.4 — Triggered-passive added skills on legendaries (per D55 high-probability; updated for 6-member enum post-W4R.1)

- [ ] Implement triggered-passive added-skill generation per slot family:
  - Weapons: spawns geometric AOE on hit; thorny on hit; etc. (incl. true-active entries per W2)
  - Armor: on-being-hit triggers
  - Accessories: general passives only (NO true-active per W2)
- [ ] Probability calibration starting anchors per doc 40 D55
- [ ] Compose with capability toolkit 6-member enum (post-W4R.1)

### W4R.5 — Modifier-surface expansion at legendary (per D56)

- [ ] Implement modifier-surface expansion: legendaries unlock NEW stat types Epic cannot roll
- [ ] Per-rarity expansion specification per doc 45 § 6

### W4R.6 — Capability toolkit legendary-exclusive enforcement (per Wave 1 SC-4 Gate 5 LOCKED HYBRID + 6-member enum)

- [ ] Implement capability toolkit legendary-exclusive enforcement (multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / triggered-passive / true-active at legendary T0-T2 only per Wave 1 SC-4 Gate 5)
- [ ] All 6 enum members enforced (per W1 Option A enum extension)
- [ ] Common/uncommon/rare/epic return [] per Wave 2 W1.4 precedent

### W4R.7 — Set bonus structure (Set T1-T2 endgame-only; 4-piece per closeout § 3.4)

- [ ] Implement set bonus structure: 2pc minor always-active + 4pc full T4-attuned
- [ ] Endgame-only enforcement (Set T1-T2 only)
- [ ] Cross-cohesion validation + round-trip smoke per Principle 6

**Per carryover (REQUIRED):** legendary_t0_5 rarity in W4R.7 round-trip smoke; all 10 rarity tiers covered per doc 45 § 10.3 module-load assert.

### Discipline compose-check

- [ ] #1 math-before-code: math-note per § Math-before-code
- [ ] #1.2 code-citation: existing-code references per Discipline #1.2 (W1 Option A enum extension cites partition_schema.py:376-381)
- [ ] **#11 empirical inspection — POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE (CRITICAL — MAINTAIN WARN-pattern PRESERVED status per Wave 3 Gate-2 milestone)**
- [ ] #18 + #18.2: spec-driven gear gen consumes Wave 1 partition + Wave 2+3 T4 + SC-7 methodology
- [ ] #26 playability: cross-cohesion validation operationalizes
- [ ] #27 + #31 + #32: preserved from Wave 2+3
- [ ] #29 commitment-to-consequence: gear gen lands with consequence
- [ ] #30 sim methodology naming: composes with gamora SC-7
- [ ] Principle 6 round-trip: W4R.7 smoke PASSes (10 rarity tiers including legendary_t0_5)

## Acceptance criteria

- [ ] All 8 sub-waves W4R.0-W4R.7 land
- [ ] **W1 RESOLVED:** `CapabilityCategory` enum extended to 6 members per Option A; module-load assert PASSes; MIGRATION.md per ADR-004
- [ ] **W2 honored:** accessory pattern library OMITS true-active entry (NOT conditional-gated stub)
- [ ] **I1 honored:** minimum ≥5 patterns per slot family (weapon ≥5; armor ≥5; accessory ≥5)
- [ ] **I3 cross-seam integration:** rocket Wave 4 Track A outputs integrate with star-lord export schema (engine commit `8dbb808`); round-trip smoke verifies
- [ ] All 10 rarity tiers covered (per doc 45 § 3.1 + § 10.3 module-load assert; including legendary_t0_5 carryover)
- [ ] Round-trip smoke per Principle 6 PASSes
- [ ] MIGRATION.md updated per ADR-004
- [ ] **POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE** (WARN-pattern PRESERVED status MAINTAINED)
- [ ] Tagged commit per rocket convention: `rocket: Cycle 13 Wave 4 Track A spec-driven gear gen implementation — W4R.0-W4R.7 bundled per doc 45 amended + jack-ryan Gate-1 W1+W2+I1 folded`

## Out of scope (explicit non-goals)

- Wave 4 Track B gamora sim cycling implementation (separate dispatch in flight)
- Wave 4 Gate-2 verification (separate dispatch post-implementation)
- Wave 5 gauntlet sim + season gen + close
- Phase 5 cohesion coalescence (Cycle 14)
- Drax quality badge display (Wave 4+ planning per star-lord open flag; not actionable Wave 4 Track A)
- D25 cross-season learning (Cycle 14 retrospective per star-lord open flag)
- Telemetry DB v2.16 migration (per ADR-006)
- Modifying canonical docs (cross-seam gandalf authority)
- decisions-log entries

## Open questions for the agent to resolve

- W4R sub-wave sequencing: W4R.0 → W4R.1 (enum extension first; gates downstream) → W4R.2 (per-rarity gen) → W4R.3 (annotation + patterns per W2/I1) → W4R.4 (triggered-passive per D55) → W4R.5 (modifier-surface per D56) → W4R.6 (capability toolkit per W1) → W4R.7 (set bonus + smoke). Internal your call.
- T4-attunement annotation field-naming: follow Wave 3 scope-dimension convention OR new namespace; your seam-owner call
- MIGRATION.md scope: enum extension W4R.1 + new fields (incremental documentation); recommend minimal per Principle 6

## References

- `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` amended (commits `a4faa20` + `17ce1be`)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-1-doc-45-critique.md` (Gate-1 W1+W2+I1+I3 fold-ins)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md`
- `canonical/44+43+42+41+40` amended
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 3
- Wave 1+2+3 rocket implementation (engine commits)
- Star-lord Wave 4 export schema (engine commit `8dbb808`)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `agentic_orchestration/operating-procedures/rocket.md`

---

**Cycle:** 13
**Wave:** 4 Track A implementation (W4R.0-W4R.7 bundled)
**Gates:** Wave 4 Track A close (paired with Track B gamora sim cycling) → bundled Wave 4 Gate-2 → Wave 4 CLOSE → Wave 5 gauntlet sim + season gen + Cycle 13 close
**Priority:** P1 — critical-path Wave 4 Track A close
