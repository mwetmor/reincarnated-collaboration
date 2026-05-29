# Phase 7 Mechanical Gate Investigation — Cascade-Resumption-3

**Date:** 2026-05-29
**Author:** gamora
**Authority:** Dispatch `2026-05-29-gamora-cycle-14-cascade-resumption-3-phase7-mechanical-gate-investigation.md` — Pattern A-light analytical investigation; NO code modification
**Empirical basis:** S6a smoke re-fire telemetry (`phase7_season_summary.json`) + source code trace (phase7_bridge.py, phase7_verdict.py, gauntlet_sim.py, phase7_cohort.py)

---

## § 1 — Phase 7 mechanical gate calibration formula and threshold spec

### 1.1 Two-condition mechanical pass (phase7_verdict.py § 3)

The Phase 7 mechanical gate evaluates three conjunctive conditions per kit:

1. `archive_status == 'ACTIVE'` (all 18 base kits in S6a are ACTIVE; this condition passes universally)
2. `gauntlet_pass_rate > P7_GAUNTLET_PASS_FLOOR` (0.70; strict greater-than)
3. `|gauntlet_pass_rate - cohort_midpoint| <= P7_COHORT_MIDPOINT_BAND` (0.25)

Condition 2 fires first. A kit held on condition 2 gets verdict `HELD-mechanical-fail-floor`. All 18 kits in S6a received this verdict.

### 1.2 pass_rate computation path (phase7_bridge.py § 3)

`_run_gauntlet_for_kit()` calls `run_gauntlet_sim()` with `cohorts=[gauntlet_archetype]` (single cohort per kit). After the P3c fix (cascade-resumption-2 Step 3, commit `3717a01`), the pass_rate is computed:

```
enc_total = 18   (smoke=False)
enc_passed = round(quality_report.mean_encounters_passed_per_kit)
pass_rate = enc_passed / enc_total
```

`mean_encounters_passed_per_kit` (post-P3c, for single-cohort call) = `encounters_passed(gauntlet_archetype)`.

`GauntletKitResult.encounters_passed(cohort)` = `sum(1 for r in cohort_results[cohort] if r.in_band)`.

The `in_band` flag is set in `run_gauntlet_sim()` at line ~1000:
```python
track1_in_band = arch_band_lo <= t2_kpm <= arch_band_hi
enc_result.in_band = track1_in_band
```

where `(arch_band_lo, arch_band_hi) = get_archetype_cohort_kpm_band(kit_damage_scaling_path, cohort)`.

### 1.3 damage_scaling_path in Phase 7 synthetic kit configs

The `legendary_config` dict built in `_run_gauntlet_for_kit()` (phase7_bridge.py lines 338-346) contains keys: `legendary_id`, `player_class`, `t4_config_key`, `t4_scope`, `cohorts`, `scope_projection_data`, `scope_downscale_factor`. It does NOT include `damage_scaling_path` or `_kit_obj`.

In `run_gauntlet_sim()` (gauntlet_sim.py line 831):
```python
kit_damage_scaling_path = config.get("damage_scaling_path", None)
```
This returns `None`. The kit object fallback also fails (no `_kit_obj`). Result: `kit_damage_scaling_path = '_fallback'`.

`get_archetype_cohort_kpm_band('_fallback', cohort)` falls through to the legacy `COHORT_KPM_BAND`:
- DPS-min-maxer: (82.0, 97.0)
- Balanced: (71.0, 79.0)
- Defensive: (52.0, 64.0)
- Hybrid: (64.0, 82.0)

These are narrow bands calibrated to ~75 KPM ± 10-15%. Synthetic kits span KPMs from 71 to 446 across encounter types (per PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE comments). Almost all encounters produce `in_band=False` under these narrow legacy bands.

### 1.4 Cohort midpoint calibration (phase7_verdict.py § 9)

`calibrate_cohort_midpoints(kits_by_cohort, min_sample_size=5, scaffold_default=0.85)` computes:
- If `len(pass_rates) >= 5` for a cohort: midpoint = `statistics.median(pass_rates)`
- If `len(pass_rates) < 5`: midpoint = scaffold_default (0.85); Discipline #43 audit A3 signal fires

---

## § 2 — S6a smoke telemetry analysis

### 2.1 Source telemetry

`agentic_orchestration/cycle-14-wave-5-season-001/phase7_season_summary.json` (S6a smoke re-fire, seed_base=14001, smoke=False):

```json
{
  "kits_evaluated": 18,
  "kits_shipped_worthy": 0,
  "kits_held_mechanical": 18,
  "cohort_midpoints": {
    "damage": 0.0,
    "defensive": 0.0278,
    "control": 0.85,
    "support": 0.85,
    "hybrid": 0.85
  }
}
```

### 2.2 Per-cohort kit distribution at S6a

Empirical cohort classification via `classify_kit_cohort_from_encounter_id` against `ENDGAME_ENCOUNTER_CATALOG` (18 cells):

| Cohort | Cell count | Kits in S6a (1 per cell) | >= min_sample_size (5)? | Midpoint source |
|---|---|---|---|---|
| damage | 9 | 9 | YES | empirical: median=0.0 |
| defensive | 6 | 6 | YES | empirical: median=0.0278 |
| control | 0 | 0 | NO | scaffold: 0.85 |
| support | 0 | 0 | NO | scaffold: 0.85 |
| hybrid | 3 | 3 | NO | scaffold: 0.85 |

### 2.3 What the midpoints reveal

`damage=0.0` indicates ALL 9 damage-cohort kits had `pass_rate=0.0` (i.e., `enc_passed=0` → all encounters `in_band=False` under COHORT_KPM_BAND fallback).

`defensive=0.0278` indicates `statistics.median([pass_rates for 6 kits]) = 0.0278`. This means 1 of 18 encounters returned `in_band=True` for the median kit (1/18 ≈ 0.056; some kits ~0.0, median ≈ 0.0278). Near-zero across all defensive-cohort kits.

`hybrid=0.85` (scaffold default, n=3) does NOT indicate actual kit performance — it is the scaffold fallback value for insufficient sample. However, even if hybrid kits had pass_rate=0.85, condition 2 check is `pass_rate > 0.70` which would pass — but then condition 3 band-fit check fires: `|0.85 - 0.85| = 0.0 <= 0.25` — that would PASS. However, actual hybrid kit pass_rates are unknown (no empirical evidence; n < 5 triggered scaffold).

The telemetry confirms: all 18 kits are held on `HELD-mechanical-fail-floor` (condition 2 failure). Condition 2 requires `pass_rate > 0.70`. No kit achieves this.

---

## § 3 — Sample-size requirements for calibration

### 3.1 Is the sample insufficient for midpoint calibration?

The dispatch (§ 2.1) frames the S6a scenario as "4-5 per cohort" suggesting sparse calibration. The empirical cohort distribution contradicts this: damage has 9 kits and defensive has 6 kits in S6a — both above `min_sample_size=5`. These cohorts DO produce empirical midpoints (not scaffold fallback).

The problem is that the empirical midpoints accurately reflect reality: kits genuinely have pass_rate≈0.0 under the COHORT_KPM_BAND fallback measurement. More samples do not change this.

### 3.2 Scaffold fallback for hybrid cohort (n=3)

The 3 hybrid-cohort cells (n=3 < 5) produce scaffold_default=0.85. If hybrid kits also have pass_rate≈0.0, they still fail condition 2 (`0.0 > 0.70 = False`). If they somehow had pass_rate~0.85, condition 3 would marginally pass (`|0.85 - 0.85| = 0.0`), but that requires actual KPM values landing in COHORT_KPM_BAND (64-82 KPM for Hybrid) — possible only for encounter types with KPM near this range.

The scaffold=0.85 midpoint is not the gate failure source. Gate failure is condition 2.

### 3.3 Full-season sample projection

At A2-1 RE-FIRE-3 full season: 54 cells × 3 samples = 162 base kits before WR-bracket filtering. Expected cohort distribution:
- damage (~50% of 18 cells × 9 = 9 cells): ~81 kits (well above min_sample_size=5)
- defensive (~33% × 6 = 6 cells): ~54 kits
- hybrid (~17% × 3 = 3 cells): ~27 kits

All cohorts above min_sample_size=5 at full season. Control and support would remain empty (0 cells in ENDGAME_ENCOUNTER_CATALOG map to these cohorts under current classifier predicates). The midpoints at full season are still derived from empirical pass_rates that are still≈0.0 under COHORT_KPM_BAND fallback. More kits = better statistical estimate of a genuine 0.0 signal.

---

## § 4 — Projected full-season behavior

At A2-1 RE-FIRE-3 full season:

1. All base kits run Phase 7 with `kit_damage_scaling_path='_fallback'` (same root cause)
2. `in_band = COHORT_KPM_BAND fallback` produces near-zero pass_rates across all encounter types
3. Empirical midpoints for damage and defensive remain ≈0.0 (more samples, same result)
4. Hybrid cohort produces empirical midpoint (n≈27 > 5) — also ≈0.0 or near-zero
5. Control and support remain at scaffold=0.85 (no catalog entries → no kits → n=0)
6. All kits held on `HELD-mechanical-fail-floor` (pass_rate ≈ 0.0 vs floor=0.70)
7. `shipped_worthy=0` at full season

The full-season run would produce 162 × 3 = 486 variant kits, all also held_mech. Zero generation output despite full LLM cost of ~$50. This is not a tolerable production outcome.

---

## § 5 — Verdict and recommendation

### 5.1 Verdict: (B) Genuine calibration issue

**Root cause:** Calibration target mismatch between A2-1 Step 1 and Phase 7 bridge pass_rate measurement.

- A2-1 Step 1 calibrated `PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE` to achieve `GAUNTLET_PASS = eligible_encounters_passed(cohort) >= 9`. This uses `eligible_encounters_passed` which checks T2 KPM against `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` (the 24-cell per-encounter-type table).

- Phase 7 bridge measures `pass_rate` using `encounters_passed(cohort)` which uses the `in_band` flag set by `get_archetype_cohort_kpm_band(kit_damage_scaling_path, cohort)`. Since no `damage_scaling_path` is passed in the synthetic kit config, this falls back to legacy `COHORT_KPM_BAND` (narrow 71-97 KPM range), not `ENCOUNTER_COHORT_KPM_BAND`.

- **These are two different measurement systems.** A kit that achieves `GAUNTLET_PASS` (eligible_encounters_passed >= 9 via ENCOUNTER_COHORT_KPM_BAND) can have `pass_rate=0.0` in Phase 7 bridge if its KPM values fall outside the narrower `COHORT_KPM_BAND` legacy bands.

**Why (A) is ruled out:** The sample sizes for damage (n=9) and defensive (n=6) cohorts are above `min_sample_size=5` in S6a. These cohorts produce empirical midpoints (not scaffold fallback). The midpoints are 0.0 and 0.0278 respectively — accurate reflections of genuine near-zero pass_rates. Increasing sample size to full-season cardinality produces more instances of the same near-zero pass_rate distribution. The midpoint does not improve with more samples when the underlying signal is genuinely ≈0.0.

**Why this is NOT a Phase 7 architectural concern:** The Phase 7 two-layer gate design is sound. The failure is a wiring gap in Phase 7 bridge — a missing `damage_scaling_path` in the synthetic kit config causing fallback to stale legacy bands. This is a well-bounded gamora-seam code fix.

### 5.2 Recommended fix (gamora seam; separable Pattern B dispatch)

Two acceptable fix options:

**Option α (cleanest — align measurement with calibration target):** Replace `encounters_passed(cohort)` with `eligible_encounters_passed(cohort)` in phase7_bridge `_run_gauntlet_for_kit`, and align `P7_GAUNTLET_PASS_FLOOR` to match `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6` semantics. `eligible_encounters_passed` >= 9 → pass_rate = 9/18 = 0.50. Threshold alignment: `P7_GAUNTLET_PASS_FLOOR = 0.50` (or equivalent fraction). This is a Discipline #12 semantic shift (pass_rate measurement changes) + threshold amendment. Math note required.

**Option β (minimal wiring fix):** Pass `damage_scaling_path` in the Phase 7 synthetic kit legendary config so `get_archetype_cohort_kpm_band` uses the correct archetype-level bands rather than `COHORT_KPM_BAND` fallback. However: `_ARCHETYPE_COHORT_KPM_BAND` is `None` (not populated at runtime), so this would still fall back to COHORT_KPM_BAND unless `ARCHETYPE_COHORT_KPM_BAND` is installed. This option is incomplete without accompanying Band installation.

**Option γ (direct GAUNTLET_PASS):** Phase 7 bridge evaluates `gauntlet_pass(cohort)` (boolean, already calibrated to correct criterion) and converts directly: `pass_rate = 1.0 if gauntlet_pass else 0.0`. Binary pass_rate removes midpoint-calibration complexity entirely; floor and band checks reduce to a single boolean gate. This is architecturally cleanest but changes the Phase 7 gate semantics from a continuous rate to a binary signal — requires Discipline #18 math hotspot review before adopting.

**Recommendation for S6c routing:** Option α is the clearest fix path. It aligns the measurement with the calibration target already established at A2-1 Step 1 without requiring new archetype band installation. Math note required before implementation (Discipline #1).

---

## § 6 — Risk assessment for S6c routing

### 6.1 If S6c fires WITHOUT fix (per verdict A path):

Full season produces ~162 base kits + ~810 variant kits. All held_mech at Phase 7. `shipped_worthy=0`. LLM cost ~$50 (full season). Zero generation output. This outcome is a waste of LLM spend and provides no new empirical signal beyond what S6a already established. Not recommended.

### 6.2 If fix fires before S6c (per verdict B path):

Gamora authors fix dispatch (Pattern B per complexity; ~1-2h implementation + math note + smoke). S6c fires after fix with a functioning Phase 7 mechanical gate. Expected outcome: some kits ship (gate operates on correct calibrated pass_rates). Reasonable LLM spend (~$50) with productive output.

### 6.3 Deeper architectural concern assessment (§ 6 surface conditions):

No deeper Phase 7 architectural concern triggered. The root cause is a well-bounded wiring gap (missing `damage_scaling_path` in synthetic kit config + measurement function mismatch). The two-layer gate design, cohort classifier, verdict state machine, and calibrate_cohort_midpoints are all correct. The fix is localized to `_run_gauntlet_for_kit` in phase7_bridge.py plus `P7_GAUNTLET_PASS_FLOOR` alignment in phase7_verdict.py. Not a gandalf design-spec-as-math handoff candidate.

### 6.4 Disc #42a framing-audit Q1-Q6 result

Q1 (Is the hypothesis framing substrate-led?): Yes. Investigation used telemetry evidence directly; did not pre-impose (A) or (B) prior to reading source code.
Q2 (Is "small-sample artifact" framing plausible?): Checked first. Ruled out — damage (n=9) and defensive (n=6) are above min_sample_size=5; calibration is empirical, not scaffold-based for these cohorts.
Q3 (Is (B) verdict based on traceable causal chain?): Yes. Full code path traced: synthetic kit config → damage_scaling_path=None → _fallback → COHORT_KPM_BAND → narrow legacy bands → in_band=False → enc_passed=0 → pass_rate=0.0.
Q4 (Is there evidence of framing creep?): No pre-imposed assumption surfaced; code trace drove conclusion.
Q5 (Is the fix recommendation scope-bounded?): Yes — gamora seam only; no cross-seam impact.
Q6 (Is the verdict honest about uncertainty?): Yes — hybrid cohort (n=3 < min_sample_size) produces scaffold midpoint; actual hybrid kit pass_rates unknown. This does not affect the (B) verdict because the dominant failure mode (condition 2) is established by damage and defensive cohorts with sufficient empirical sample.

---

## § 7 — Routing recommendation (KR consumption)

**Verdict: (B) Genuine calibration issue.**

**S6c routing: fix-then-fire.**

Gamora seam-owner fix dispatch (Pattern A-light to Pattern B per gamora elect):
1. Math note for fix option (Discipline #1) — Option α alignment of pass_rate measurement to eligible_encounters_passed + P7_GAUNTLET_PASS_FLOOR recalibration to match GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 semantics (0.50 or empirically derived equivalent)
2. Code fix: `_run_gauntlet_for_kit` in phase7_bridge.py + `P7_GAUNTLET_PASS_FLOOR` in phase7_verdict.py
3. Smoke: verify Phase 7 bridge produces non-zero pass_rates for ACTIVE kits after fix
4. S6c (A2-1 RE-FIRE-3) fires after fix close + smoke PASS

**No §6 surface triggers:** investigation did not reveal deeper architectural concern; effort within ~30min estimate; Disc #42a Q1-Q6 clean.
