# DISPATCH — W-α2 gamora — KPM Ceiling Raise/Remove

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** gamora (simulation seam; gauntlet_sim.py KPM ceiling owner)
**Pattern:** Pattern B (~0.5-1d; ceiling raise or remove decision + empirical anchor + math note)
**Status:** PENDING — fires on jack-ryan Gate-1 PASS
**Authority:** Matt 2026-05-28 Path α RATIFICATION + doc 50 LOAD-BEARING + master scoping § 2.2 W-α2

---

## 0. AUTHORITY + CONTEXT

**Matt 2026-05-28 Path α directive verbatim** (cycle-14-hive-mind-state.md § "MATT GATE-6 RATIFICATION REVERSAL LOCKED"):
> *"Engine KPM ceiling 600.0 raised or removed (currently hides over-tuning)"*

**Empirical anchor — current state:** INT/WIS saturate the 600.0 KPM ceiling on 4 of 6 encounter types per Matt empirical evidence. Ceiling artificially caps KPM signal, masking the actual damage output range. Path α requires uncapped empirical signal for W-α3 reference-target derivation (per jack-ryan Gate-1 Amendment 1 of master scoping).

doc 50 § 4.3 target 3: **No kit saturates ceiling on any encounter type** — saturation_count = 0 across 108 cells.

---

## 1. SCOPE

### 1.1 Architectural choice (gamora seam discretion)

Two valid paths per master scoping § 2.2:

**Option A — Raise ceiling.** Choose a new ceiling value that ensures no kit saturates under post-Path-α refactor expected KPM range. Derive empirically from W-α4 baseline + projected post-refactor population DPS distribution.

**Option B — Remove ceiling entirely.** Update gate semantics in `gauntlet_sim.py` to not apply any KPM ceiling. Doc 50 target 3 then trivially satisfies (no ceiling = no saturation). Saturation gate becomes vestigial.

Gamora seam discretion. **Decision rule:** whichever choice cleaner architecturally + better-coheres with W-α4 harness Target 3 check + W-α3 reference-target needs.

### 1.2 If Option A (raise ceiling): empirical derivation

Compute new ceiling from:
- Current post-rebase population DPS distribution per `option-f-track-1-post-rebase-telemetry.json`
- Projected post-Path-α population DPS (per doc 50 § 4.1 target ≤1.5× variance) — gamora projection within reasonable bounds
- Headroom factor: 1.5-2× projected max DPS per encounter type

Math note (Discipline #1) at `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-2-kpm-ceiling-raise-remove-2026-05-28.md`:
- Cite doc 50 § 4.3 as canonical authority
- Show empirical signal + projected post-Path-α distribution
- Derive new ceiling OR justify removal (with vestigial-gate retirement plan if Option B)
- Sensitivity analysis: what if projected DPS ranges are 2× higher than expected? Ceiling adequacy preserved?

### 1.3 If Option B (remove ceiling): gate-semantic update

Update `gauntlet_sim.py` to retire the 600.0 ceiling. Audit downstream consumers of `saturation_flag` per W-α4 harness `bounded_viability_validation.py` Target 3 check. Coordinate W-α4 harness Target 3 semantics: with no ceiling, saturation_count is trivially 0 — Target 3 PASS becomes structural, not measured.

### 1.4 Coordination with W-α3

**Critical micro-dependency per master scoping Amendment 1:** W-α3 reference target lock awaits W-α2 empirical ceiling output (W-α3 harness authoring can proceed in parallel; reference target value does not commit until W-α2 lands).

**Coordination signal:** gamora commits + pushes W-α2 close (ceiling raised/removed + math note + harness adjustment); gamora W-α3 dispatch reads AGENT_STATE.md + absorbs ceiling signal.

### 1.5 W-α4 harness coordination

W-α4-gamora harness (`bounded_viability_validation.py`) has `kpm_ceiling: float | None` parameter. Option A path = pass new ceiling value; Option B path = pass `None`. Gamora confirms parameter usage at W-α2 close + W-α4 harness re-run for new baseline.

### 1.6 Acceptance criterion

**Path α joint criterion:** harness re-run with new ceiling value + post-Path-α refactor returns `compound_pass=True`.

**W-α2 isolated acceptance:**
- Option A or B chosen + executed
- Math note authored
- `gauntlet_sim.py` updated per chosen Option
- W-α4 harness Target 3 semantics confirmed
- AGENT_STATE.md updated
- Tag: `gamora/v2.5-w-alpha-2-kpm-ceiling-1`

### 1.7 MIGRATION.md

Section update in `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.X (next available; coordinate sequencing with W-α3 if both fire in same wave).

---

## 2. REQUIRED READING

LOAD-BEARING canonical:
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — § 4.3 target 3 (saturation_count = 0)
- `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` § 2.2 W-α2 specifications + Amendment 1 W-α3 micro-dependency

Empirical anchors:
- `agentic_orchestration/cycle-14-wave-5-season-001/bounded-viability-validation-baseline-2026-05-28.json` (W-α4 smoke baseline; Target 3 PASS via KPM=0 artifact)
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json` (population DPS distribution)
- Matt empirical evidence: INT/WIS saturate 600.0 ceiling on 4/6 encounter types

Engine source:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` — current 600.0 ceiling implementation
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` — W-α4 harness `kpm_ceiling` parameter
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — recent sections (§§ v1.34-v1.40)

Disciplines:
- #1 math-before-code, #11 empirical inspection, **#47 bounded-viability decision gate** (verify chosen option satisfies doc 50 § 4.3 + supports targets 1-2-4-5)

---

## 3. OUT OF SCOPE — explicit

- **Do NOT modify damage formulas.** W-α1 rocket scope.
- **Do NOT implement unified calibration pass.** W-α3 separate gamora dispatch.
- **Do NOT modify W-α4 validation harness implementation.** Parameter usage update only.
- **Do NOT modify doc 50.** Gandalf seam authority.

---

## 4. RISKS + COMPLICATIONS

- **Option A vs Option B trade-off.** Option A preserves existing gate-semantic infrastructure; Option B simplifies but retires a gate. Both valid; gamora seam decision.
- **Coordination with W-α3 reference target.** Master scoping Amendment 1 sequences this correctly; ensure gamora W-α3 dispatch absorbs W-α2 close signal before reference target commits.
- **W-α4 harness Target 3 semantics under Option B:** structural PASS rather than measured PASS. Document explicitly in math note so downstream readers don't misinterpret.

---

## 5. URGENCY

**W-α2 is the shortest-pole work-stream in Path α** (~0.5-1d). Fires PARALLEL with W-α1 + W-α3 post-W-α4 lock.

Fire ASAP on jack-ryan Gate-1 PASS.

---

**KR signature:** authored per Matt 2026-05-28 Path α RATIFICATION directive verbatim + master scoping § 2.2 W-α2 specifications + Amendment 1 micro-dependency on W-α3. Gamora seam authority on Option A/B choice; auto-commit + auto-push.
