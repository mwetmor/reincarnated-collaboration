# DISPATCH — W-α4-gamora — Bounded-Viability Validation Harness

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** gamora (simulation seam; validation harness implementation against doc 50 design targets)
**Pattern:** Pattern B (~1-2d; harness implementation + math note + smoke tests)
**Status:** PENDING — fires on jack-ryan Gate-1 PASS
**Authority:** Matt 2026-05-28 Path α RATIFICATION + doc 50 canonical lock at meta `fe0b4a7`

---

## 0. AUTHORITY + LOAD-BEARING INPUT

**Doc 50 is LOAD-BEARING.** Canonical doc authored by gandalf at `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` (commit `fe0b4a7` + tag `gandalf/v1.13-w-alpha-4-bounded-viability-canonical-1`). **§ 4 (5 operationalized design targets with numeric criteria + validation methods) + § 5 (per-encounter-type validation framing + harness specification + cohort definition lean) + § 8.1 (W-α4-gamora forward-link) are your canonical anchors.**

Master scoping: `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` (Path α work-stream decomposition).

W-α4-gamora is the **sibling work-stream within W-α4** — sequential after gandalf canonical lock; lands BEFORE W-α1/W-α2/W-α3 fan-out fires.

---

## 1. SCOPE

### 1.1 Validation harness implementation

Implement simulation-side validation harness that runs against current engine state (and future Path α post-refactor state) producing per-kit-per-encounter-type profile satisfying all 5 doc 50 § 4 design targets.

**Architecture:**

- **Input:** current 18-kit production population (post Wave 0.5 backfill + Wave 1.5 Stage 3 Option α + current substrate state); **6 encounter types** from `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` canonical valid_shells (lines 949-952): **`open_arena / chokepoint_corridor / magic_pack / elite_pack / boss_with_adds / mini_boss`** — locked per doc 50 § 5.1 + engine catalog (jack-ryan Gate-1 Amendment 1 correction; KR speculative list contained non-existent `endgame_capstone`). Gamora verifies at harness implementation against live catalog state per Discipline #45 + Review Principle #3 (schema validation at boundaries).
- **Sweep:** per-kit at L50 against each encounter type × 4 cohorts (steamroll / balanced / hard-out / soft-out) per established Track 1 / boss HP rebase pattern
- **Output:** 108-cell matrix (18 kits × 6 encounter types) with per-cell KPM measurement + cohort medians + per-kit specialization profile + saturation count + floor violations
- **Per-cell metrics:** kit_KPM, kit_DPS, encounter_HP_consumed_per_second, cohort_median_KPM, kit_KPM / cohort_median_KPM ratio, saturation_flag (KPM >= ceiling), floor_violation_flag (ratio < 0.30)

### 1.2 5 design-target checks (canonical per doc 50 § 4)

Implement each as automated check:

1. **Base DPS variance ≤1.5× across 4 damage-scaling paths** — population-DPS sweep at L50; group kits by `damage_scaling_path` (STR-physical / DEX-physical / INT-magical / WIS-faith); compute per-path median DPS; verify max(path_medians) / min(path_medians) ≤ 1.5
2. **Every kit produces non-zero KPM on every encounter type** — across 108 cells, zero_count = 0; report cells with kit_KPM = 0
3. **No kit saturates ceiling on any encounter type** — across 108 cells, saturation_count = 0 (where saturation = kit_KPM >= ceiling at W-α2 raised/removed value)
4. **Specialization variance: each kit ~1.5-2× cohort median on 1-2 encounter types** — per-kit specialization profile per doc 50 § 4.4 verbatim (jack-ryan Gate-1 Amendment 2 precision): each kit must have **≥1 and ≤2 cells where 1.5 ≤ ratio ≤ 2.0** (the [1.5, 2.0] specialization band). Kits with 0 cells in band FAIL (no designed peak). Kits with ≥3 cells in band FAIL (over-dominant). Ratios above 2.0 are handled by Target 3 saturation check (post-W-α2 ceiling).
5. **No kit performs <30% of cohort median on any encounter type** — across 108 cells, floor_violation_count = 0 (where floor_violation = ratio < 0.30)

**Compound pass criterion:** all 5 targets simultaneously satisfied.

### 1.3 Harness API

Single entry point function returning structured validation report:

```python
def run_bounded_viability_validation_harness(
    kit_population: list[KitConfig],
    encounter_types: list[EncounterType],
    cohorts: list[CohortConfig],
    kpm_ceiling: float | None,  # None = no ceiling (W-α2 removal path)
    floor_threshold: float = 0.30,
    specialization_lower: float = 1.5,
    specialization_upper: float = 2.0,
    base_dps_variance_ceiling: float = 1.5,
) -> BoundedViabilityValidationReport:
    """
    Returns 108-cell matrix + per-target check + compound pass/fail verdict.
    """
```

Report structure:
- `cells: dict[(kit_id, encounter_type), CellResult]` — 108-cell matrix
- `target_1_dps_variance: TargetCheckResult` — pass/fail + max-path-ratio + per-path medians
- `target_2_zero_kpm_count: TargetCheckResult` — pass/fail + zero cells
- `target_3_saturation_count: TargetCheckResult` — pass/fail + saturated cells
- `target_4_specialization_profile: TargetCheckResult` — pass/fail + per-kit profile + violations
- `target_5_floor_count: TargetCheckResult` — pass/fail + floor violation cells
- `compound_pass: bool` — true iff all 5 targets pass
- `telemetry_output_path: Path` — JSON dump for downstream analysis

### 1.4 File locations + integration

**Implementation file (gamora seam discretion on exact path):**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` (suggested)
- Integrates with existing gauntlet sim infrastructure (`gauntlet_sim.py`)
- May import from `sc7_calibration_loop.py` partition utilities (`_partition_kits_by_damage_scaling_path`, `_get_kit_damage_scaling_path`) — those persist as Track 1 infrastructure per Matt D3 RATIFICATION; harness reuses

**Math note required at:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/bounded-viability-validation-harness-2026-05-28.md`
- Cite doc 50 § 4 as canonical authority for each target
- Show measurement formulas (DPS, KPM, cohort medians, ratios)
- Sensitivity analysis: what if specialization upper bound were 2.5 instead of 2.0? floor were 0.25 instead of 0.30? Discipline #1 math-before-code

**MIGRATION.md § v1.40 (or next available):**
- New simulation-side validation harness introduced
- Cross-reference to doc 50 + master scoping + W-α4-gandalf canonical lock

### 1.5 Smoke run vs current engine state (Discipline #11 empirical inspection)

Run harness against CURRENT engine state (pre-Path-α-refactor). **Expected result: FAIL on all 5 targets** (current engine produces 365× elite_pack ratio + 0.0 KPM cells + ceiling saturation per Matt empirical evidence). This is the **baseline empirical signal** that:
- Confirms harness measures what doc 50 § 4 specifies
- Quantifies the gap that W-α1/W-α2/W-α3 must close
- Sets reference baseline for post-refactor comparison

**Acceptance for W-α4-gamora close:** harness implementation + math note + smoke baseline result documented (FAIL is expected at smoke; W-α1/W-α2/W-α3 close criterion is harness PASS post-refactor).

### 1.6 AGENT_STATE + tag

- AGENT_STATE.md updated post-completion
- Tag: `gamora/v2.4-w-alpha-4-bounded-viability-harness-1` per gamora seam discretion

**Auto-commit + auto-push per CLAUDE.md addendum + Cycle 14 per-workstream push pattern.**

---

## 2. REQUIRED READING

Canonical anchor (LOAD-BEARING):
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — full doc (§ 4 design targets + § 5 validation framing + § 8.1 W-α4-gamora forward-link)

Architectural context:
- `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` (Path α work-stream decomposition + sequencing)
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-6 RATIFICATION REVERSAL LOCKED 2026-05-28" + Path α decomposition rows
- `canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 (4 damage-scaling paths mechanical partition; cross-references doc 50 forward-link)

Engine substrate:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (existing gauntlet sim infrastructure)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/sc7_calibration_loop.py` (Track 1 sweep infrastructure + partition utilities)
- `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` (6 encounter types canonical)
- `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_mob_stat_profile.py` (post-rebase boss HP at `d83049a`)
- Current kit population substrate (post Wave 0.5 + Stage 3 Option α)

Empirical context:
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json`
- `agentic_orchestration/cycle-14-wave-5-season-001/boss-hp-rebase-empirical-dps-telemetry.json`
- These provide pre-Path-α baseline numbers for harness smoke-run validation

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #11 empirical inspection, #18.1 pre-fire resource projection, #45 vocabulary lock

---

## 3. OUT OF SCOPE — explicit

- **Do not implement damage formula refactor.** W-α1 rocket scope.
- **Do not raise/remove KPM ceiling.** W-α2 gamora scope (separate dispatch).
- **Do not implement unified calibration pass.** W-α3 gamora scope (separate dispatch).
- **Do not modify doc 50.** Gandalf seam authority; W-α4-gandalf canonical lock holds.
- **Do not retire Phase 7 doc.** Jack-ryan W-α5b scope.
- **Do not run full production season.** Harness implementation + smoke baseline run only; full Wave 5 re-fire at Path α close.

---

## 4. RISKS + COMPLICATIONS

- **6 encounter types canonical source:** doc 50 § 5 (per gandalf canonical lock) is primary; verify against `endgame_encounter_catalog.py` at harness implementation. If discrepancy surfaces, gamora flags + jack-ryan resolves via Discipline #45 vocabulary lock.
- **Cohort definition lean:** gandalf locked per-damage-scaling-path cohorts for v1 Path α (4 cohorts = 4 damage paths). Verify with doc 50 § 5; clarify if cluster-based-cohort interpretation needed (gandalf deferred cluster-based to Cycle 15+).
- **Harness smoke FAIL is expected.** Discipline #44 framing-refusal does NOT apply — FAIL is the baseline diagnostic signal. Document FAIL clearly; do not interpret as harness defect.
- **Performance:** 108 cells × 4 cohort levels × multiple per-cell measurements may exceed wall-time budget. Pre-fire resource projection per Discipline #18.1; if peak time/memory exceeds host capacity, scope-reduce to representative subset for smoke; full sweep at Path α close.
- **Cross-seam read:** harness reads `endgame_encounter_catalog.py` + `endgame_mob_stat_profile.py` (rocket-owned files); MIGRATION.md notes the cross-seam read but no rocket modification needed (read-only).

---

## 5. URGENCY

**W-α4-gamora harness is the final load-bearing input before W-α1/W-α2/W-α3 parallel fan-out fires.** ~1-2d. Fire ASAP on jack-ryan Gate-1 PASS.

Cycle 14 v1 close trajectory ~4-6 weeks from Path α firing.

---

**KR signature:** authored per Matt 2026-05-28 Path α RATIFICATION + gandalf doc 50 canonical lock at meta `fe0b4a7` + master scoping § 2.1 W-α4 sibling-stream sequencing + jack-ryan Gate-1 Amendment 1 (W-α3 micro-dependency on W-α2 ceiling signal — relevant downstream context). Harness implementation is gamora seam authority; auto-commit + auto-push.
