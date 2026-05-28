# DISPATCH — W-α3 gamora — Unified Calibration Pass (Replaces SC-6b + SC-7)

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** gamora (simulation seam; calibration loops; SC-7 binary search retirement target)
**Pattern:** Pattern B (~2-3d; harness authoring parallel; reference target lock awaits W-α2 ceiling signal per master scoping Amendment 1)
**Status:** PENDING — fires on jack-ryan Gate-1 PASS
**Authority:** Matt 2026-05-28 Path α RATIFICATION + master scoping § 2.2 W-α3 + Amendment 1 micro-dependency

---

## 0. AUTHORITY + LOAD-BEARING CONTEXT

**Matt 2026-05-28 Path α directive verbatim:**
> *"New unified calibration pass (replaces SC-6b + SC-7 with single reference target)"*

**Critical sequencing per master scoping Amendment 1:**
> *"Reference target lock requires W-α2 ceiling signal (W-α3 harness authors in parallel; reference target value does not commit until W-α2 empirical ceiling output lands). Discipline #1 math-before-code: reference target derivation must be grounded in uncapped empirical signal, not artifact-capped data."*

W-α3 calibration architecture supersedes:
- **SC-6b** `base_physical_damage_l50` (rocket Wave 0.5 backfill at `3c95883`; uncalibrated against boss HP per case 8 finding)
- **SC-7** `BASE_SPELL_DAMAGE_L50` (gamora binary-search calibrated at `e7af7db` mult=93.8×; single-class single-archetype calibration; per-encounter-type populations still saturated/REJECTED)

Both substrate constants retire OR get replaced by unified pass.

---

## 1. SCOPE

### 1.1 Unified calibration architecture

Replace `sc7_calibration_loop.py` SC-7 binary search + SC-6b uncalibrated baseline with **single unified calibration pass** that ties damage formulas (post-W-α1 refactor) to encounter HP scaling + boss HP factor range.

Architecture options (gamora seam discretion):

**Option α — Single reference target tied to encounter HP at L50.** Calibrate base damage such that population-median DPS achieves target KPM on a reference encounter type (likely Balanced cohort × elite_pack or comparable mid-tier encounter).

**Option β — Per-damage-scaling-path reference target with unified architecture.** Each of 4 damage paths calibrates to its own reference target within ≤1.5× variance per doc 50 § 4.1. Preserves doc 47 § 3 mechanical partition.

**Option γ — Joint calibration against W-α4 harness 5 targets directly.** Iterative calibration loop optimizes against all 5 doc 50 § 4 targets simultaneously rather than single reference.

Gamora math note (Discipline #1) captures chosen architecture + sensitivity analysis.

### 1.2 Sequencing (critical)

**Phase 1 — Harness authoring (parallel with W-α2):** gamora authors new calibration pass implementation. May begin immediately on dispatch fire. Reference target value parameter remains placeholder.

**Phase 2 — Reference target lock (gated on W-α2 + W-α1):**
- W-α2 ceiling signal lands → ceiling-uncapped empirical population DPS distribution available
- W-α1 damage formula refactor lands → new formula architecture defined
- Reference target value commits per chosen calibration architecture (α/β/γ)
- Calibration pass runs against post-W-α1 + post-W-α2 engine state

**Phase 3 — Validation via W-α4 harness:** `run_bounded_viability_validation_harness(smoke=False)` post-calibration confirms `compound_pass=True`.

### 1.3 SC-6b + SC-7 retirement coordination

**SC-7 (`BASE_SPELL_DAMAGE_L50`):** `sc7_calibration_loop.py` binary search retired or extended with W-α3 mode per gamora seam discretion. Either:
- Retire `sc7_calibration_loop.py` entirely; new implementation at `~/Games/reincarnated-engine/src/reincarnated/simulation/unified_calibration_loop.py` (suggested)
- Extend `sc7_calibration_loop.py` with W-α3 unified-pass entry point; SC-7 single-class binary search becomes historical

**SC-6b (`base_physical_damage_l50`):** unified pass calibrates this value (or its post-W-α1 successor) against new reference target. If W-α1 Direction A (unified formula), SC-6b becomes attribute-coefficient on common base; if W-α1 Direction B (recalibrated per-path), SC-6b retains per-path baseline + unified calibration.

**Track 1 partition utilities (`_partition_kits_by_damage_scaling_path`, `_get_kit_damage_scaling_path`):** PERSIST per Matt D3 RATIFICATION. W-α3 reuses unchanged.

### 1.4 Math note + MIGRATION.md

**Math note required at:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-3-unified-calibration-pass-2026-05-28.md`
- Architecture choice (α/β/γ) + rationale
- Reference target derivation from W-α2 ceiling signal + post-W-α1 damage formulas
- Sensitivity analysis: reference target variance ±20%; convergence properties
- SC-6b + SC-7 retirement / supersession provenance

**MIGRATION.md § v1.X** (next available; coordinate sequencing with W-α2 if both fire close together):
- SC-6b + SC-7 retirement / supersession record
- New unified calibration pass introduced
- Cross-references to doc 50 + master scoping + W-α2 + W-α1

### 1.5 Acceptance criterion

**Path α joint criterion:** `run_bounded_viability_validation_harness(smoke=False)` against post-Path-α refactor returns `compound_pass=True`.

**W-α3 isolated acceptance:**
- Unified calibration pass implemented
- Reference target locked per chosen architecture
- SC-6b + SC-7 retirement/supersession documented
- Math note authored
- Tag: `gamora/v2.6-w-alpha-3-unified-calibration-1`
- Auto-commit + auto-push per CLAUDE.md addendum

---

## 2. REQUIRED READING

LOAD-BEARING:
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — § 4 (5 design targets) + § 5 (per-damage-scaling-path cohorts for v1)
- `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` § 2.2 W-α3 + Amendment 1 critical sequencing

Path α coordination:
- `agentic_orchestration/dispatches/2026-05-28-w-alpha-1-rocket-damage-formula-refactor.md` (W-α1 post-refactor formulas)
- `agentic_orchestration/dispatches/2026-05-28-w-alpha-2-gamora-kpm-ceiling-raise-remove.md` (W-α2 ceiling signal)
- `agentic_orchestration/dispatches/2026-05-28-w-alpha-4-gamora-validation-harness.md` (W-α4 harness for validation)

Engine source:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/sc7_calibration_loop.py` — current SC-7 binary search + Track 1 partition utilities
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` — W-α4 harness
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` — W-α2 ceiling target
- `~/Games/reincarnated-engine/src/reincarnated/foundation/` — SC-6b + SC-7 substrate constants
- `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_mob_stat_profile.py` — encounter HP scaling (post boss-HP-rebase at `d83049a`)

Historical precedent:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/sc-7-base-spell-damage-l50-calibration-2026-05-28.md` (SC-7 calibration math note; superseded by W-α3)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/boss-hp-rebase-case-8-resolution-2026-05-28.md` (case 8 math note; load-bearing for encounter HP scaling)

Disciplines:
- #1 math-before-code (mandatory math note), #11 empirical inspection, #18.1 pre-fire resource projection (calibration sweep wall-time), **#47 bounded-viability decision gate** (verify reference target derivation supports all 5 doc 50 § 4 targets)

---

## 3. OUT OF SCOPE — explicit

- **Do NOT modify damage formulas.** W-α1 rocket scope.
- **Do NOT modify gauntlet sim KPM ceiling.** W-α2 separate gamora dispatch.
- **Do NOT modify W-α4 validation harness implementation.** W-α3 reads harness `kpm_ceiling` parameter post-W-α2.
- **Do NOT modify Track 1 partition utilities.** Persist per Matt D3 RATIFICATION.
- **Do NOT modify endgame_mob_stat_profile.py boss HP factor range.** Calibrated at case 8 `d83049a`; HISTORICAL anchor only.

---

## 4. RISKS + COMPLICATIONS

- **Phase 2 reference target lock dependency on W-α1 + W-α2.** Critical: do NOT commit reference target value until BOTH W-α1 lands AND W-α2 ceiling signal lands. Discipline #1 math-before-code violation otherwise.
- **Architecture α/β/γ choice.** All three valid; gamora seam discretion. Document rationale; jack-ryan Gate-2 reviews against doc 50 § 4 + #47 enforcement.
- **SC-7 retirement vs extension trade-off.** Gamora seam discretion; both valid. `sc7_calibration_loop.py` carries Track 1 partition utilities that MUST persist; extension preserves backward-compat; retirement clean-breaks.
- **Pre-fire resource projection per Discipline #18.1.** Unified calibration pass may iterate multiple sims; project wall-time + memory against host RAM.
- **W-α4 harness Target 3 semantics under W-α2 Option B (no ceiling).** Coordinate at W-α3 reference target lock; if ceiling removed, reference target derivation uses uncapped DPS directly.

---

## 5. URGENCY

**W-α3 ~2-3d; mid-pole work-stream in Path α.** Fires PARALLEL with W-α1 + W-α2 (Phase 1 harness authoring); reference target lock Phase 2 sequences post W-α1 + W-α2.

Cycle 14 v1 close trajectory ~4-6 weeks from Path α firing.

Fire ASAP on jack-ryan Gate-1 PASS.

---

**KR signature:** authored per Matt 2026-05-28 Path α RATIFICATION directive verbatim + master scoping § 2.2 W-α3 + Amendment 1 critical Phase 2 sequencing. Gamora seam authority on architecture α/β/γ choice + SC-7 retirement/extension; auto-commit + auto-push.
