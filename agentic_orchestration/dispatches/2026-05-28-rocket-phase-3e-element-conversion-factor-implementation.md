# DISPATCH — Phase 3e rocket — element_conversion_factor Implementation (Case 16 Resolution)

**Authored:** 2026-05-28 evening late
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** rocket (foundation seam; damage_resolver.py:618 TODO replacement)
**Pattern:** Pattern B (~1.5-2d projected; ~half-day Discipline #1.1 compression likely)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 evening late D1+D2+D3+D4+D5 RATIFICATION — Option A case 16 resolution

---

## 0. AUTHORITY + CONTEXT

**Matt 2026-05-28 evening late D1 RATIFIED Option A** verbatim — case 16 element_conversion_factor stub absorbed into Cycle 14 (not deferred Cycle 15). Reasoning:

- Case 16 = Discipline #39 scaffold-with-pending-decision (engine TODO at `damage_resolver.py:618`)
- Pattern of Cycle 14 catches (16 prior cases): all engine-execution scaffolds resolved mid-cycle
- CLAUDE.md "Engine first. Game second. Phase third." — case 16 = engine integrity gap
- Bounded-viability-with-specialization directive (doc 50) requires T4 specialization peaks empirically verified
- v1 tag accuracy: `bounded-viability-substrate-led` requires full BVV PASS to ship

**D2 RATIFIED — Cycle 14 v1 close-criterion UNCHANGED: full 5/5 BVV PASS required.**

---

## 1. SCOPE

### 1.1 Read T4 conversion mechanic spec

Source candidates (canonical doc precedence):
- `canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 (damage routing; 4 damage-scaling paths)
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` (composition with doc 51 § 4.7)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` (T4 capstone mechanic if specified)
- Engine sources for element catalog + T4 variant definitions

If T4 conversion mechanic spec is NOT canonically locked, rocket consults gandalf (Tier-A canonical-write) for design intent before implementing. Discipline #47 design-time check — element conversion is balance-affecting; must satisfy doc 50 § 4 5 targets.

### 1.2 Map T4 variant ID → element_conversion factor per element pair

For each T4 capstone variant in current kit population:
- Identify the source element + target element pair
- Derive element_conversion factor (may be 1.0 if no conversion; may be variable per element pair if elemental advantage/resistance applies)
- Document mapping in math note

### 1.3 Implement at damage_resolver.py:618

**Current state:** `element_conversion_factor = 1.0  # TODO` (gamora Phase 4 forensic confirmed)

**Replace TODO with real conversion logic:**
- Function or lookup table consuming T4 variant ID + relevant element-pair context
- Returns appropriate element_conversion factor
- Composes cleanly with existing damage formula (W-α1 Direction A unified parity 2.337 preserved; Pattern 1 multiplier from Phase 3a + tier_coeff from Phase 3d)
- Application order per Phase 3a precedent: `base × damage_modifier × investment_multiplier × (1 + gear_pct) × element_conversion × tier_coeff`

### 1.4 Unit tests + integration tests

- Unit: per-variant element_conversion factor lookup
- Integration: smoke fight with at least 2-3 distinct T4 variants per damage path; verify T4 KPM differentiation (not identical across variants per Phase 4 finding)
- Verify composition with Pattern 1 multiplier × BASE × TIER_COEFFICIENT preserves doc 51 § 7 max-investment construction property

### 1.5 Math note (Discipline #1)

At `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-7-phase-3e-element-conversion-factor-implementation-2026-05-28.md`:
- Cite case 16 forensic (gamora Phase 4 hand-back)
- T4 conversion mechanic spec citation
- T4 variant → element_conversion factor mapping
- Composition verification with Phase 3a/3b/3c/3d state
- Discipline #1.1 pre-fire resource projection
- Discipline #12 semantic shift declaration if applicable (replacing TODO sentinel with real logic)
- Cite doc 51 § 7 max-investment construction property preservation

### 1.6 MIGRATION.md

Section in `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.48 (or next available):
- Element conversion factor introduced (replaces TODO stub)
- T4 variant → factor mapping documented
- Cross-references to doc 47 § 3 + doc 51 § 7 + Phase 4 telemetry
- Star-lord seam: assess whether telemetry schema needs T4 variant tracking (likely no per case 16 Cycle 15-defer pattern; verify)

### 1.7 Acceptance + tag

- damage_resolver.py:618 TODO replaced with real logic
- Unit + integration tests PASS
- Math note + MIGRATION.md filed
- T4 variants produce DIFFERENTIATED KPM (not identical per case 16 finding)
- Tag: `rocket/v1.11-element-conversion-factor-1`
- AGENT_STATE.md updated; Phase 4 RE-RUN consumes

**Auto-commit + auto-push.**

---

## 2. REQUIRED READING

LOAD-BEARING:
- `canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 (damage routing primary anchor)
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4 (5 design targets)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` (Patterns 1+2 composition + § 7 max-investment construction)

Phase 4 forensic (case 16 anchor):
- Gamora Phase 4 completion record at `dispatches/2026-05-28-integrated-w-alpha-7-plus-master-scoping.md` (completion record appended)
- Hive-mind state § "PHASE 4 MULTI-DIM CALIBRATION COMPLETE 2026-05-28 EVENING — CASE 16 EMERGED"
- Telemetry artifact at `agentic_orchestration/cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-multi-dim-sweep-telemetry.json`

Engine source:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` (line 618 TODO target + surrounding composition)
- T4 variant definitions wherever they live (rocket seam discretion to locate; gandalf consultation if not found)
- Element catalog + element-pair definitions

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1, #1.1, #11, #12, #39, #47

---

## 3. OUT OF SCOPE

- BVV harness re-run (gamora Phase 4 RE-RUN handles)
- T4 capstone design changes (Cycle 15+ territory; this dispatch ONLY implements conversion mechanic per spec)
- Element catalog modifications (out of W-α7+ scope)
- Patterns 3-6 (Cycle 15+ canonical-locked)

---

## 4. RISKS + COMPLICATIONS

- **T4 conversion mechanic spec absent or ambiguous:** if canonical doesn't define element_conversion mechanic explicitly, gandalf consultation required. Discipline #47 design-time check is gandalf seam authority.
- **Cross-seam impact:** if T4 conversion affects telemetry seam, star-lord MIGRATION.md cross-reference required.
- **Discipline #1.1 over-projection pattern:** ~1.5-2d Matt-projected; recent pattern suggests ~few hours actual.
- **Integration with Phase 3a/3b/3c/3d:** verify composition preserved (W-α1 parity 2.337 + Pattern 1+2 multipliers at max-investment=1.0 + TIER_COEFFICIENTS {1.00, 1.50, 2.17, 4.00}).

---

## 5. URGENCY

**Phase 5 + Phase 6 cascade gates on Phase 4 RE-RUN PASS, which gates on this Phase 3e close.** Fire ASAP.

Effort estimate per Matt D3: ~1.5-2d projected; ~half-day under Discipline #1.1 compression pattern.

---

**KR signature:** authored per Matt 2026-05-28 evening late D1+D2+D3 RATIFICATION (Option A) + case 16 forensic + gamora Phase 4 hand-back + § 10.8.5 escalation routing absorbed into engine fix. v1 close-criterion 5/5 PASS unchanged; T4 specialization (doc 50 § 4.4 Target 4) restored via this implementation.

---

## Completion record

**Status:** PARTIAL — dispatch guard clause § 1.1 fired; implementation BLOCKED pending gandalf design lock.

**Date:** 2026-05-28
**Agent:** rocket

### What was completed

**Discipline #1 math note:** authored at `simulation/math/w-alpha-7-phase-3e-element-conversion-factor-implementation-2026-05-28.md`

Key analytical findings:
1. `element_conversion_factor` numeric value is NOT canonically locked in doc 47, doc 50, doc 51, mechanic_alteration.py, t4_wireup.py, or combatant.py. Guard clause triggered.
2. Flat-factor cancellation proof: a flat per-path element_conversion_factor F cannot produce Target 4 specialization peaks. Within each damage_scaling_path cohort (str_physical / dex_physical / int_magical / wis_faith), ALL kits in season 001 share the same source element (str=earth, dex=wind, int=fire, wis=water). F scales kit_KPM and cohort_median proportionally → ratio unchanged → Target 4 cannot fire from factor alone.
3. Two-part root cause identified:
   - Part 1 (rocket seam): damage_resolver.py:618 TODO stub — must be replaced with wired logic
   - Part 2 (gamora seam): `_build_real_player_class()` in season_generation_pipeline.py does NOT pass `alteration_fields` to combatant construction → T4 ELEMENT_CONVERSION element-tag override never applied during Phase 4 gauntlet runs → even with Part 1 fixed, Phase 4 RE-RUN sees no T4 differentiation
4. Phase 3d calibration was T4-naive (T4 alteration not wired into gauntlet combatants during Phase 3d BASE re-derivation)

**Gandalf consultation request filed:** `agentic_orchestration/gandalf/requests/2026-05-28-rocket-element-conversion-factor-design-lock-request.md`

**AGENT_STATE.md updated:** Phase 3e blocking state captured.

### What is blocked

- damage_resolver.py:618 implementation
- Unit tests (test_element_conversion_factor_*)
- Integration smoke fight with T4 variant differentiation
- MIGRATION.md § v1.48
- Tag rocket/v1.11-element-conversion-factor-1

### Unblocking path

Gandalf design lock on:
- Q1 (PRIMARY): What is the numeric value of element_conversion_factor for ELEMENT_CONVERSION T4?
- Q2: Is this the specialization mechanism, or does specialization emerge from Phase 3d base_at_max?
- Q3: Does PoE Avatar of Fire analogy include numeric fire-bonus?

Post-gandalf-lock: rocket Part 1 estimated 1-2 hours. Phase 4 RE-RUN dispatch must include gamora Part 2 wiring (T4 alteration fields into gauntlet combatants).

### Scope note for Phase 4 RE-RUN dispatch

Phase 4 RE-RUN dispatch (gamora, post-Phase-3e-close) must include:
- Wire T4 alteration fields into `_build_real_player_class(kit, t4_variant)` via `alteration_fields` parameter
- Run Phase 4 sweep once per profile × T4 variant (currently skips T4 variants — comment at unified_calibration_loop.py:2408)
- Re-derive BASE values under T4 context if element-affinity shift changes effective damage (depends on gandalf Q2)

This is a gamora-seam scope addition that was missed in the original Phase 4 implementation. Case 16 cannot be resolved by rocket alone.
