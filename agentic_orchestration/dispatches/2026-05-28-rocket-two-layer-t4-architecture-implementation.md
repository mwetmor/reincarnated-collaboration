# DISPATCH — Rocket Two-Layer T4 Architecture Implementation (Doc 47 § 4.6 + Doc 51 § 10.7.8/10.8.9)

**Authored:** 2026-05-28 evening late
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** rocket (foundation seam; T4 catalog implementation + mechanic_alteration variants + damage_resolver per-variant magnitudes)
**Pattern:** Pattern B (~2-3hr per #1.1 compression; comprehensive T4 catalog refactor)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 evening late D1-D6 RATIFIED strategic deliberation resolution + Frenzy TRADE_OFF lock + tag intent confirmation

---

## 0. AUTHORITY + CONTEXT

**Matt 2026-05-28 evening late strategic deliberation resolution D1-D6 RATIFIED** — two-layer T4 specialization architecture absorbed via integrated cascade. **TRADE_OFF REVERSED = FRENZY** Matt-locked. **Tag intent confirmed**: `v1-cycle-14-bounded-viability-substrate-led` at Phase 6c.

**Gandalf canonical locks (READ FIRST):**
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.5 v1.2 + NEW § 4.6 — full 7-active T4 catalog spec (engine `eb5bd1b` + tag `gandalf/v1.17-doc-47-4-6-two-layer-t4-architecture-1`)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 10.7.8 + § 10.8.9 — two-layer T4 extensions
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4.7 — cross-reference update

---

## 1. SCOPE

### 1.1 NEW PRIMARY T4 strategy — DIRECT_DAMAGE_AMPLIFICATION

**Mechanic (per doc 47 § 4.6 Q6 lock):**
- 1.75× damage multiplier when fighting kit's **preferred encounter type**
- 1.0× elsewhere
- Discipline #39 scaffold with EXPLICIT CYCLE 15 RETIREMENT COMMIT (Cycle 15 P0 architectural commit replaces with natural mechanics)

**Implementation:**
- New strategy class `DirectDamageAmplificationStrategy` (or equivalent) in `mechanic_alteration.py` (or appropriate location)
- Preferred-encounter-type detection: read `kit.preferred_encounter_type` field (rocket adds to kit schema if absent; gandalf seam discretion on assignment algorithm — per gandalf § 4.6: per-kit canonical OR algorithmic via opportunity_scan OR hybrid)
- Apply at damage resolution: `damage_resolver.py` consumes preferred-encounter context; multiplies by 1.75 when encounter type matches; identity 1.0 otherwise
- Application order per Phase 3a precedent: `base × damage_modifier × investment_multiplier × (1 + gear_pct) × element_conversion × direct_damage_amp × tier_coeff` (or appropriate composition layer per gandalf canonical)
- **Constant:** `DIRECT_DAMAGE_AMPLIFICATION_MULTIPLIER = 1.75`
- **Annotated as scaffold:** module-level comment per Discipline #39 3-element framework (declaration + party + gate)

### 1.2 ELEMENT_CONVERSION variant magnitudes UPDATE (supersedes v1.1)

**Doc 47 § 4.5 v1.2 magnitudes (per gandalf):**
- `ELEMENT_CONVERSION_VARIANT_A_MAGNITUDE = 1.50` (was 1.125; Single +50% multiplicative)
- `ELEMENT_CONVERSION_VARIANT_B_MAGNITUDE = 1.25` (was 1.0; Hybrid +25% multiplicative)
- `ELEMENT_CONVERSION_VARIANT_C_MAGNITUDE = 0.25` (was 0.35; Physical 25% additive)
- **NEW:** `ELEMENT_CONVERSION_VARIANT_C_AILMENT_ENABLED = True` (or False if engine doesn't support per-element ailment) — Physical variant adds ailment effect IF engine supports per-element ailment-support flag

**Code update at `damage_resolver.py:618`** (extend rocket v1.12):
- Update magnitudes from v1.1 to v1.2 values
- Variant C additive channel: 0.25 × base_physical (was 0.35)
- IF `ELEMENT_CONVERSION_VARIANT_C_AILMENT_ENABLED`: trigger per-element ailment effect (rocket seam discretion on integration with existing ailment system — defer if engine doesn't support cleanly)

### 1.3 TRADE_OFF REVERSED = FRENZY mechanic (Matt-locked)

**Frenzy mechanic:**
- `hit_pct -30%` (multiplicative reduction OR additive subtraction per rocket seam discretion + engine convention)
- `crit_pct +30%` (multiplicative OR additive per same)
- Existing engine fields (no new infrastructure)
- Genre precedent: PoE Frenzy ("wild swing")
- Generative for Berserker / Brunhilda / Cu Chulainn / Lu Bu archetypes
- Layer 2 (Secondary/Tertiary T4 slot)

**Implementation:**
- New strategy class `TradeOffReversedFrenzyStrategy` (or extend existing TRADE_OFF strategy with REVERSE flag)
- Apply at attacker resolution: modify hit_pct + crit_pct when active
- Constants: `TRADE_OFF_FRENZY_HIT_REDUCTION = 0.30`; `TRADE_OFF_FRENZY_CRIT_BOOST = 0.30`

### 1.4 DEFENSIVE_TRADEOFF removal (Matt D3)

- Remove `DEFENSIVE_TRADEOFF` strategy class or mark as RETIRED in mechanic_alteration.py
- Update T4 catalog enumeration to exclude DEFENSIVE_TRADEOFF
- No chaos encounter signal per Matt rationale
- Cross-reference doc 47 § 4.6 catalog (DEFENSIVE_TRADEOFF absent from 7-active list)

### 1.5 GEOMETRY_COLLAPSE + RESOURCE_CONVERSION empirical inclusion (Matt D3)

- Verify existing implementations of GEOMETRY_COLLAPSE + RESOURCE_CONVERSION strategies present in mechanic_alteration.py
- If absent or incomplete, implement minimal viable mechanic per "try it out" empirical framing
- Strip-and-ship § 10.8 determines fate at Phase 4 RE-RUN-3
- Document any implementation gaps in math note

### 1.6 T4 slot assignment infrastructure (Matt D2)

- Add `kit.primary_t4` field (universal DIRECT_DAMAGE_AMP assignment)
- Add `kit.secondary_t4` field (mechanical conversion strategy per opportunity_scan)
- Add `kit.tertiary_t4` field (4-chain kits; different mechanical strategy)
- Update `_build_t4_context_configs()` (caught at Phase 4 RE-RUN bug fix) to populate variant + slot consistently
- Coordinate with gamora Phase 4 RE-RUN-3 expectations (slot-based catalog enumeration; Primary EXEMPT from strip-and-ship per § 10.8.9)

### 1.7 Math note (Discipline #1) + MIGRATION.md

**Math note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-plus-two-layer-t4-architecture-implementation-2026-05-28.md`:
- Cite gandalf doc 47 § 4.5 v1.2 + § 4.6 + doc 51 § 10.7.8/10.8.9 + doc 50 § 4.7
- DIRECT_DAMAGE_AMP implementation + scaffold annotation per Discipline #39 3-element framework
- ELEMENT_CONVERSION variant magnitude UPDATE (v1.1 → v1.2) per Phase 4 RE-RUN case 19 empirical falsification
- TRADE_OFF REVERSED Frenzy mechanic implementation
- DEFENSIVE_TRADEOFF retirement
- GEOMETRY_COLLAPSE + RESOURCE_CONVERSION empirical inclusion
- T4 slot assignment schema additions
- Composition preservation verification (W-α1 parity 2.337; TIER_COEFFICIENTS {1.00, 1.50, 2.17, 4.00}; Pattern 1+2 max=1.0; Phase 3d RE-RUN BASE values)
- Discipline #1.1 pre-fire resource projection
- Discipline #12 semantic shift declarations (v1.1 magnitudes superseded; T4 catalog restructured to two-layer)

**MIGRATION.md § v1.53** (or next available):
- Two-layer T4 architecture introduced
- DIRECT_DAMAGE_AMP scaffold + Cycle 15 retirement commit
- ELEMENT_CONVERSION variant magnitude UPDATE
- TRADE_OFF REVERSED = Frenzy
- DEFENSIVE_TRADEOFF retirement
- Schema additions (kit.primary_t4 / secondary_t4 / tertiary_t4)
- Cross-references to gandalf v1.17 canonical lock

### 1.8 Unit + integration tests

- Per-strategy mechanic verification:
  - DIRECT_DAMAGE_AMP: 1.75× at preferred-encounter; 1.0× otherwise
  - ELEMENT_CONVERSION A/B/C: new magnitudes 1.50 / 1.25 / 0.25 additive
  - TRADE_OFF Frenzy: -30% hit / +30% crit
  - GEOMETRY_COLLAPSE + RESOURCE_CONVERSION: minimal smoke per existing mechanic
- T4 slot assignment verification (Primary universal; Secondary/Tertiary per kit)
- Composition preservation per strategy (W-α1 + Phase 3d RE-RUN BASE + TIER_COEFFICIENTS + Pattern 1+2 + application order)

### 1.9 Tag + acceptance

- Tag: `rocket/v1.13-two-layer-t4-architecture-1`
- AGENT_STATE.md updated; gamora Phase 4 RE-RUN-3 consumes

**Auto-commit + auto-push** per CLAUDE.md addendum + Cycle 14 cadence.

**Effort estimate:** ~2-3hr per Matt directive; possibly faster under Discipline #1.1 compression pattern.

---

## 2. REQUIRED READING

LOAD-BEARING canonical:
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.5 v1.2 + NEW § 4.6 (gandalf v1.17 at `eb5bd1b`)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 10.7.8 + § 10.8.9
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4.7

Authority + context:
- Hive-mind state § "MATT STRATEGIC DELIBERATION RESOLUTION LOCKED 2026-05-28 EVENING LATE" + § "SUB-AGENT GANDALF CANONICAL AMENDMENTS COMPLETE" + § "MATT TRADE_OFF REVERSE LOCK 2026-05-28 EVENING LATE — FRENZY"
- Phase 4 RE-RUN forensic (case 19 empirical anchor) at hive-mind state § "PHASE 4 RE-RUN COMPLETE 2026-05-28 EVENING LATE — SCENARIO B"

Engine source:
- `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (existing strategy infrastructure; ElementConversionStrategy + DEFENSIVE_TRADEOFF + others)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` (line 618 + per-variant lookup from rocket v1.12 at `8516ce9`)
- `~/Games/reincarnated-engine/src/reincarnated/generation/skill_schema.py` (kit schema; slot fields)
- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` `_build_real_player_class()` + `_build_t4_context_configs()` (gamora Part 2 wiring at `b3214c3`)

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1, #1.1, #11, #12, #39, #45, #47

---

## 3. OUT OF SCOPE

- Phase 4 RE-RUN-3 sweep execution (gamora sub-agent post your close)
- BVV harness multi-dim extension (Phase 5a)
- Drax loadout UI revival (Phase 5b)
- Wave 5 RE-FIRE composite (Phase 5c)
- Disciplines #41-#48 batched canonical-write (Phase 6a; jack-ryan)
- A/B comparison (Phase 6b; gandalf)
- Cycle 15 P0 commit (DIRECT_DAMAGE_AMP scaffold retirement — Cycle 15 territory)

---

## 4. RISKS + COMPLICATIONS

- **preferred_encounter_type assignment algorithm:** gandalf seam discretion per § 4.6.4 — if rocket can't locate canonical assignment, consults gandalf (Pattern A subagent invocation) before locking
- **Variant C ailment integration:** per-element ailment-support engine flag — if engine doesn't cleanly support per-element ailment, set `ELEMENT_CONVERSION_VARIANT_C_AILMENT_ENABLED = False` and document deferral
- **GEOMETRY_COLLAPSE + RESOURCE_CONVERSION:** "try it out" empirical framing — minimal viable mechanic; strip-and-ship determines fate
- **Schema additions:** kit.primary_t4 / secondary_t4 / tertiary_t4 fields — coordinate with gamora `_build_t4_context_configs()` expectations
- **T4 catalog enumeration:** 7-active strategy list; ensure gamora Phase 4 RE-RUN-3 enumerates correctly (DEFENSIVE_TRADEOFF absent; 7 strategies present)
- **Composition preservation:** application order with Primary T4 multiplier + Layer 2 magnitudes — verify all variants compose cleanly with Phase 3d RE-RUN BASE + W-α1 parity + TIER_COEFFICIENTS

---

## 5. URGENCY

**Cycle 14 v1 close trajectory ~5-7d from this fire.** Phase 4 RE-RUN-3 (gamora) → Phase 5+6 cascade → Matt v1 tag ratification at Phase 6c.

Fire ASAP.

---

**KR signature:** authored per Matt 2026-05-28 evening late D1-D6 RATIFICATION + Frenzy TRADE_OFF lock + tag intent confirmation + sub-agent gandalf canonical amendments at `eb5bd1b`. Cycle 14 v1 close criterion (5/5 BVV PASS) achievable via Primary T4 universal-guarantee + Layer 2 strip-and-ship + Cycle 15+ DIRECT_DAMAGE_AMP retirement via natural mechanics. Discipline #39 Mode B scaffold pattern at design-dialog layer.

---

## Completion record

**Completed:** 2026-05-28 (continued session — context resumed)
**Agent:** rocket (Sonnet 4.6)
**Commit:** `1ac272f` on `main`
**Tag:** `rocket/v1.13-two-layer-t4-architecture-1` (pushed)

### Deliverables

1. **Math note (Discipline #1):** `src/reincarnated/generation/math/w-alpha-7-plus-two-layer-t4-architecture-implementation-2026-05-28.md` — §§ 1–8 covering all 6 scope items; DDA mechanism, v1.2 magnitudes, Frenzy, DEFENSIVE_TRADEOFF retirement, GEOMETRY_COLLAPSE/RESOURCE_CONVERSION, T4 slot schema, composition preservation.

2. **DIRECT_DAMAGE_AMPLIFICATION (Primary T4):** `damage_resolver.py` — `DIRECT_DAMAGE_AMPLIFICATION_MULTIPLIER = 1.75` constant + DDA block in `resolve_skill()` (after geo_mult). `combatant.py` — 2 new fields (`t4_preferred_encounter_type`, `t4_current_encounter_type`) + `direct_damage_amplification` handler in `from_player_class()`. `mechanic_alteration.py` — `DirectDamageAmplificationStrategy` + `PRIMARY_T4_STRATEGY` singleton + `select_primary_t4()`.

3. **ELEMENT_CONVERSION v1.2:** `damage_resolver.py` — `ELEMENT_CONVERSION_VARIANT_A_MAGNITUDE = 1.50`, `ELEMENT_CONVERSION_VARIANT_B_MAGNITUDE = 1.25` (NEW named constant), `ELEMENT_CONVERSION_VARIANT_C_MAGNITUDE = 0.25`, `ELEMENT_CONVERSION_VARIANT_C_AILMENT_ENABLED = False`. Physical + magical formula branches updated.

4. **TRADE_OFF_REVERSED_FRENZY:** `damage_resolver.py` — `TRADE_OFF_FRENZY_HIT_REDUCTION = 0.30`, `TRADE_OFF_FRENZY_CRIT_BOOST = 0.30`. `combatant.py` — `trade_off_reversed_frenzy` handler applying additive hit/crit modification at combatant init. `mechanic_alteration.py` — `TradeOffReversedFrenzyStrategy` in `REGIME_CHANGE_STRATEGIES_V1_13_LAYER2`.

5. **DEFENSIVE_TRADEOFF retirement:** Removed from `REGIME_CHANGE_STRATEGIES_V1_13_LAYER2` per Matt D3. Preserved in `combatant.py` from_player_class() for backward-compat. Constant `STRATEGY_DEFENSIVE_TRADEOFF` preserved.

6. **GEOMETRY_COLLAPSE + RESOURCE_CONVERSION:** Verified already implemented (v1 registry). `_gamora_fields_from_t4_candidate()` extended to dispatch both strategies.

7. **T4 slot schema:** `season_generation_pipeline.py` — 4 new nullable `KitCandidate` fields: `primary_t4`, `secondary_t4`, `tertiary_t4`, `preferred_encounter_type`. `_gamora_fields_from_t4_candidate()` expanded from EC-only to all-7-strategy dispatch (Discipline #12 semantic shift).

8. **Tests:** `tests/test_two_layer_t4_architecture.py` — 55 new tests (DDA, ECF v1.2, Frenzy, GEOMETRY_COLLAPSE/RESOURCE_CONVERSION, T4 slot, composition preservation, gamora dispatch, integration smoke). `tests/test_phase3e_element_conversion_factor.py` — updated for v1.2 (Variant B non-identity, ratio corrections). 296/296 T4-related tests PASS.

9. **MIGRATION.md § v1.53:** `simulation/MIGRATION.md` — 7 change categories documented; DDA gamora harness action required; epoch break documentation; downstream consumer notes.

10. **AGENT_STATE.md:** Updated checkpoint with v1.13 completion record.

### Gamora Phase 4 RE-RUN-3 handoff requirements

**Critical:** Gamora harness must inject `combatant.t4_current_encounter_type = scenario_shell_id` at fight setup before each fight where DDA is active. Without this, DDA is a silent no-op (preferred None != current None → no match). See MIGRATION.md § v1.53 for details.

**v1.2 ECF epoch break:** Any Phase 4 RE-RUN telemetry with ELEMENT_CONVERSION T4 active used v1.1 magnitudes (A=1.125, B=1.0 identity, C=0.350). Post-v1.53 Phase 4 RE-RUN-3 uses v1.2 (A=1.50, B=1.25, C=0.25). Results are NOT comparable across this boundary.

### Out-of-scope items not touched

- `simulation/` harness (`t4_current_encounter_type` injection) — gamora seam
- `_build_t4_context_configs()` gamora internal — gamora seam (doc 47 § 1.6)
- Per-element ailment infrastructure — Cycle 15 candidate per `ELEMENT_CONVERSION_VARIANT_C_AILMENT_ENABLED = False`
