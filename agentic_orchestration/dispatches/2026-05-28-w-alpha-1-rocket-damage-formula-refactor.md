# DISPATCH — W-α1 rocket — Damage Formula Refactor (Path α Architectural Commit)

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** rocket (foundation seam; generation; damage formulas across 4 damage-scaling paths)
**Pattern:** Pattern B (~3-5d; architectural refactor + math note + integration testing + harness re-run)
**Status:** PENDING — fires on jack-ryan Gate-1 PASS
**Authority:** Matt 2026-05-28 Path α RATIFICATION + doc 50 LOAD-BEARING + W-α4 stream complete (harness operational)

---

## 0. AUTHORITY + LOAD-BEARING INPUT

**Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL** — Path α RATIFIED. **bounded-viability-with-specialization** design directive locked. doc 50 LOAD-BEARING at `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` (gandalf `fe0b4a7` + `gandalf/v1.13`).

**Discipline #47 LANDED** (jack-ryan W-α5c `deadd26`): bounded-viability decision gate framework — any kit-population balance change is evaluated against doc 50 § 4 5 targets at design-time.

**W-α4-gamora harness operational** at engine `b0dd455` + tag `gamora/v2.4-w-alpha-4-bounded-viability-harness-1`. Smoke baseline FAIL captured as gap-sizing signal for your refactor.

W-α1 is the **longest-pole + most-architecturally-significant work-stream** in Path α — the damage formula refactor closes the structural root cause of the 365× cross-path imbalance.

---

## 1. SCOPE

### 1.1 Architectural choice (rocket seam discretion per master scoping Gate-1 ruling)

Two architectural directions are valid per master scoping § 2.2 + jack-ryan Gate-1 ruling on W-α1 latitude:

**Direction A — Unified damage formula.** Single base damage formula across all 4 damage-scaling paths (STR-physical / DEX-physical / INT-magical / WIS-faith per doc 47 § 3). Per-path scaling differences expressed via attribute-scaling coefficients on a common base. Closes two-path divergence structurally — STR/INT differ in attribute coefficient, not formula architecture.

**Direction B — Recalibrated per-path formulas.** Preserve 4 distinct per-path formulas; recalibrate each path's base values such that population-DPS variance ≤1.5× across paths. Two-path divergence closed via calibration alignment, not formula unification.

**Rocket seam discretion** on Direction choice. Decision rule: whichever Direction more cleanly satisfies doc 50 § 4 target 1 (base DPS variance ≤1.5×) AND preserves doc 47 § 3 mechanical-substrate partition AND minimizes downstream system-inheritance risk (gear scaling, T4 capstones, attribute scaling cited at master scoping § 1.3 anticipated scaffold-drift areas).

Rocket math note (Discipline #1) captures the chosen Direction + rationale + sensitivity analysis.

### 1.2 Empirical signal (W-α4 baseline)

Current state per W-α4 baseline + post-rebase telemetry:
- INT/WIS magical path: ~297,000 HP/s population-median Balanced DPS at L50 (SC-7 calibrated mult=93.8×)
- STR/DEX physical path: ~3,750 HP/s population-median Balanced DPS at L50 (SC-6b uncalibrated)
- **Population-DPS ratio: 79×** (population-median framing) or **365×** (per-encounter-type elite_pack framing)

**Target: max(path_medians) / min(path_medians) ≤ 1.5** per doc 50 § 4.1.

### 1.3 File ownership (rocket seam)

Damage formula sources (verify against current engine state at dispatch execution):
- `~/Games/reincarnated-engine/src/reincarnated/foundation/` — substrate constants (SC-6b `base_physical_damage_l50`; SC-7 `BASE_SPELL_DAMAGE_L50`)
- `~/Games/reincarnated-engine/src/reincarnated/element/` — element-specific damage scaling (per damage-scaling path)
- `~/Games/reincarnated-engine/src/reincarnated/anchor/` — anchor-specific damage contribution
- `~/Games/reincarnated-engine/src/reincarnated/generation/` — damage formula composition at kit generation

Rocket seam discretion on file-level decomposition; primary anchor is doc 47 § 3 4-damage-path canonical authority.

### 1.4 Coordination with W-α3 (gamora unified calibration)

W-α3 calibrates AGAINST W-α1 output. Sequencing:
- W-α1 lands new damage formulas (Direction A or B)
- W-α3 re-runs unified calibration pass against new formulas
- W-α3 reference target lock awaits W-α2 ceiling signal per master scoping Amendment 1

**Coordination signal:** rocket commits + pushes W-α1 close (formulas + tag); gamora reads AGENT_STATE.md + W-α3 dispatch absorbs new formula state.

**Cross-stream coherence note (jack-ryan Gate-1 amendment):** W-α1 math note MUST include a one-paragraph "cross-stream coherence check" identifying which W-α3 calibration architecture (α single ref target / β per-path ref targets / γ joint optimization) is most compatible with chosen Direction (A unified / B recalibrated per-path) and flagging any convergence concerns. Rationale: 2×2×3 = 12 configurations in space; two risk pairs flagged by jack-ryan: (a) Direction B × Option α may not converge within ≤1.5× variance (per-path formulas converging to single ref from different architectures); (b) Direction A × Option β degenerates gracefully (unified base → ref targets resolve to same value) but math note confirms degenerate case explicitly. Cross-stream coherence analysis stays in rocket's math note (sets formula architecture; W-α3 calibrates against it); does not pre-empt gamora's seam discretion on Option α/β/γ. Jack-ryan Gate-2 verifies coherence claim against W-α3's actual choice.

### 1.5 Cross-seam coordination

- **Generation seam (rocket internal):** if W-α1 touches kit generation (kit damage values per skill), MIGRATION.md § v1.X within generation seam internal
- **Simulation seam (gamora):** if W-α1 affects damage application at runtime (gauntlet sim damage resolution), MIGRATION.md § v1.X cross-seam to gamora; ADR-004 required
- **Telemetry seam (star-lord):** if substrate constants change (SC-6b / SC-7 retirement or replacement), MIGRATION.md § v1.X cross-seam to star-lord; coordination on substrate-carried fields

### 1.6 Acceptance criterion

**Path α close criterion (jointly with W-α2 + W-α3):** `run_bounded_viability_validation_harness(smoke=False)` against post-refactor engine returns `compound_pass=True`. All 5 doc 50 § 4 targets simultaneously satisfied.

**W-α1 isolated acceptance (within Path α):**
- Direction A or B implemented
- Math note (Discipline #1) authored + sensitivity analysis included
- Population-DPS ratio across 4 damage-scaling paths ≤1.5× at L50 (target 1 satisfied independently)
- Integration with existing kit generation + simulation seams verified
- Tag: `rocket/v1.8-w-alpha-1-damage-formula-refactor-1` (rocket seam discretion)

### 1.7 Anticipated scaffold-drift coordination

Per master scoping § 1.3 — likely surface areas:
- **T4 capstone scaling** — if T4 skill values inherit from base damage formula, T4 may need parallel adjustment
- **Gear scaling** — gear affixes calibrated against pre-refactor damage formulas may need MIGRATION
- **Attribute scaling** — STR/DEX/INT/WIS scaling tables may need parallel adjustment
- **Defense formulas** — armor/resistance computations may need re-balance

Each surfaced case follows Gate-N → Matt cadence. Discipline #47 enforcement: balance changes affecting any of doc 50 § 4 5 targets require explicit ratification.

**Discipline #47 re-check on each scaffold-drift case (jack-ryan Gate-1 amendment):** any scaffold-drift case that affects a doc 50 § 4 5 target must be explicitly evaluated against all 5 targets before Gate-N closes. Prevents implicit assumption that T4/gear/defense/attribute drift cases are pure implementation matters; ensures cross-target coherence preserved as adjacent architectural truths surface.

### 1.8 AGENT_STATE + tag

- AGENT_STATE.md updated post-completion
- Tag: `rocket/v1.8-w-alpha-1-damage-formula-refactor-1`
- Auto-commit + auto-push per CLAUDE.md addendum + Cycle 14 per-workstream push pattern

---

## 2. REQUIRED READING

LOAD-BEARING canonical:
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — § 4 (5 design targets) + § 5 (validation framing) + § 6 (Path β rejection rationale; do NOT preserve underlying damage formula imbalance) + § 8.1 (W-α1 forward-link)
- `canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 (4 damage-scaling paths mechanical partition; load-bearing for Direction-choice rationale)

Path α context:
- `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` (full master scoping; § 2.2 W-α1 specifications; § 1.3 anticipated scaffold-drift)
- `agentic_orchestration/dispatches/2026-05-28-w-alpha-4-gamora-validation-harness.md` (W-α4-gamora harness reference)
- `agentic_orchestration/dispatches/2026-05-28-w-alpha-5-jack-ryan-canonical-retirements.md` (W-α5 retirements context)
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-6 RATIFICATION REVERSAL LOCKED 2026-05-28"

Empirical anchors:
- `agentic_orchestration/cycle-14-wave-5-season-001/bounded-viability-validation-baseline-2026-05-28.json` (W-α4 smoke baseline)
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json` (post-rebase empirical 79× gap)
- `agentic_orchestration/cycle-14-wave-5-season-001/boss-hp-rebase-empirical-dps-telemetry.json` (population DPS sweep)

Engine source (current state):
- Foundation / element / anchor / generation files per rocket seam familiarity
- Substrate constants: SC-6b `base_physical_damage_l50` (rocket Wave 0.5 backfill at `3c95883`); SC-7 `BASE_SPELL_DAMAGE_L50` (gamora calibrated at `e7af7db` mult=93.8×)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` (W-α4 harness; use to validate at refactor close)

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code (mandatory math note), **#1.1 pre-fire resource-bounds projection** (jack-ryan Gate-1 amendment: correct citation — prior draft incorrectly cited #18.1), #11 empirical inspection, #39 framework (Mode B canonical scaffold resolution context), #40 case (c) (if canonical-lock retraction surfaces), #45 vocabulary lock, **#47 bounded-viability-with-specialization decision gate** (enforce 5-target check at design-time)

---

## 3. OUT OF SCOPE — explicit

- **Do NOT modify gauntlet sim KPM ceiling.** W-α2 gamora scope.
- **Do NOT implement new calibration pass.** W-α3 gamora scope.
- **Do NOT modify W-α4 validation harness.** Gamora seam authority.
- **Do NOT modify doc 50.** Gandalf seam authority.
- **Do NOT modify Phase 7 doc.** HISTORICAL status; jack-ryan W-α5b lifecycle completed.
- **Do NOT pre-author Cycle 15 commitments.** Cycle 15 scope undetermined post Path α.

---

## 4. RISKS + COMPLICATIONS

- **Direction A vs Direction B trade-off is architecturally substantial.** Document rationale carefully in math note; jack-ryan Gate-2 will review against doc 50 § 4 targets + doc 47 § 3 partition preservation.
- **Anticipated scaffold-drift cases.** Per master scoping § 1.3, T4 capstones / gear scaling / attribute scaling are likely surface areas. Each surfaces as Gate-N → Matt cadence; do NOT pre-empt by re-scoping W-α1.
- **Cross-seam coordination.** If W-α1 touches simulation seam damage application, gamora must absorb at W-α3 reference target lock (already-sequenced via Amendment 1 W-α2 dependency). If W-α1 touches telemetry seam substrate fields, star-lord engagement may be needed (Cycle 14 substrate evolution).
- **Discipline #18.1 pre-fire resource projection:** if refactor requires regeneration of substrate (e.g., re-running Wave 0.5 against new formulas), peak memory + wall-time must be projected against host RAM.
- **Discipline #47 enforcement.** At design-time, verify proposed Direction satisfies doc 50 § 4 5 targets (or document which targets remain gated on W-α2 + W-α3 closure). Jack-ryan Gate-1 enforces this.

---

## 5. URGENCY

**W-α1 is the longest-pole work-stream in Path α** (~3-5d realistic per master scoping). Fires PARALLEL with W-α2 + W-α3 post-W-α4 lock.

Cycle 14 v1 close trajectory ~4-6 weeks from Path α firing. Each day of W-α1 delay shifts close-trajectory.

Fire ASAP on jack-ryan Gate-1 PASS.

---

**KR signature:** authored per Matt 2026-05-28 Path α RATIFICATION + doc 50 LOAD-BEARING + Discipline #47 enforcement + W-α4 harness operational + master scoping § 2.2 W-α1 architectural latitude ruling. Rocket seam authority for architectural Direction choice; auto-commit + auto-push per Cycle 14 cadence.
