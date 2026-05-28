# DISPATCH — W-α6 gamora — Per-Encounter-Type KPM Bands (Option B Case 9 Resolution)

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** gamora (simulation seam; calibration loops; per-encounter-type extension of W-α3 architecture)
**Pattern:** Pattern B (~2-4d; per-encounter-type math note + calibration sweep × 24 cells + harness re-run + bundle Gate-2 + Wave 5 RE-FIRE prep)
**Status:** PENDING — fires on jack-ryan Gate-1 PASS
**Authority:** Matt 2026-05-28 Gate-7 D1+D2+D3+D4 RATIFICATION — Option B case 9 resolution within Cycle 14 v1

---

## 0. AUTHORITY + CONTEXT

**Matt 2026-05-28 Gate-7 D1 RATIFIED** verbatim: Option B — pull Cycle 15 Gate-3 D2 per-encounter-type bands into Cycle 14 v1. Rationale: bounded-viability-with-specialization constitutive properties (T2 floor + T4 specialization peaks) require empirical verification; tag accuracy preserved; Q10 quality > timeline; Discipline #39 Mode A case 9 resolved within cycle; C-Hybrid algorithmic discipline (Cycle 15+) measurement infrastructure depends on per-encounter bands.

**Jack-ryan Gate-7 disposition:** `agentic_orchestration/qa/pending/2026-05-28-case-9-gauntlet-encounter-coverage-gate-7-disposition.md` (commit `3512889` + tag `jack-ryan/v1.8-gate-7-case-9-disposition`).

**Case 9 forensic (jack-ryan verified):** `GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1` frozenset has exactly 2 members (`boss_with_adds`, `mini_boss`); other 4 encounter types structurally produce `tier_2_kpm=0.0`. BVV harness expects per-encounter-type bands which never been implemented.

**Cycle 15 reference clarification:** "Cycle 15 Option A" = `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` per-encounter-type bands (Gate-3 D2 ratified item). DISTINCT from retracted Gate-5 D2 Option 6 metric replacement.

---

## 1. SCOPE

### 1.1 W-α6a — Per-encounter-type KPM bands math note + canonical structure (~0.5d)

**Math note required** at `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md`:

- Cite doc 50 § 4 5 targets (T2 floor + T4 specialization explicit; T1+T3+T5 retained from W-α3)
- Derive `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` structure: 24 cells = 6 encounter types × 4 cohorts (steamroll / balanced / hard-out / soft-out)
- Reference target derivation per encounter type (gamora seam discretion; likely Balanced-cohort median per-encounter-type as primary anchor)
- Sensitivity analysis: per-cohort band width vs target satisfaction
- Cross-reference doc 47 § 3 (4 damage-scaling paths preserved via W-α1 unified formula; per-encounter-type bands measure same population against per-encounter HP distribution)

**Canonical structure update:**
- New `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` constant in `gauntlet_sim.py` OR `unified_calibration_loop.py` (gamora seam discretion)
- 6 encounter types from `endgame_encounter_catalog.py` canonical valid_shells: `open_arena / chokepoint_corridor / magic_pack / elite_pack / boss_with_adds / mini_boss`
- Replaces single `COHORT_KPM_BAND[cohort]` for eligibility check
- `GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1` frozenset retired or extended to all 6 types

### 1.2 W-α6b — Calibration sweep × 6 encounter types × 4 cohorts (~1-2d)

**Sweep architecture:**
- Reuse `unified_calibration_loop.py` Phase 1 + Phase 2 infrastructure (W-α3 architecture preserved)
- Extend Option α single-reference-target architecture to per-encounter-type reference targets
- 24 calibration cells: per-encounter × per-cohort median target derivation
- Discipline #1.1 pre-fire resource-bounds projection: per W-α3 Phase 2 actual (~28s for 6 iterations; estimate ~6× scaling = ~3min per-cohort-per-encounter, ~75min total worst case; likely much less per W-α3 over-projection pattern Matt D4 noted)

**Reuse existing calibrated BASE values** (rocket W-α1 + gamora W-α3 Phase 2):
- `BASE_PHYSICAL_DAMAGE_L50 = {T1:43703, T2:65533, T3:94629, T4:174714}` (post-W-α3-Phase-2 scale_factor=0.664063 applied to W-α1 rocket Direction A)
- `BASE_SPELL_DAMAGE_L50 = {T1:18689, T2:28034, T3:40493, T4:74757}` (same scale_factor)
- Damage formula architecture (W-α1 Direction A unified parity 2.337) UNCHANGED
- W-α6 calibrates BAND ranges, not BASE values

**Output:** 24-cell `ENCOUNTER_COHORT_KPM_BAND` populated; W-α4 harness reads from this structure for per-encounter-per-cohort comparison.

### 1.3 W-α6c — BVV harness re-run + compound_pass acceptance (~0.5d)

Run `run_bounded_viability_validation_harness(smoke=False, kpm_ceiling=None)` against fully-calibrated post-Path-α + post-Option-B engine state.

**Expected outcome:**
- T1 PASS: ~1.24× cross-path parity preserved (W-α3 Phase 2 result; not affected by per-encounter bands)
- T2 PASS: per-encounter bands enable `tier_2_kpm` population across all 6 types; zero_count → 0
- T3 PASS: structural (ceiling=None per W-α2 Option B)
- T4 PASS: specialization peaks emerge once per-encounter measurement is unblocked; each kit shows 1-2 peaks at [1.5, 2.0] cohort median ratio
- T5 PASS: floor preserved within-path-within-encounter

**Acceptance: `compound_pass=True` — PATH α + OPTION B CLOSE SIGNAL.**

**If FAIL surfaces (case 10+ probability ~30-50% per Matt D4 watch surface):** Discipline #44 framing-refusal; KR fires Gate-8 disposition.

### 1.4 MIGRATION.md + tags

- MIGRATION.md § v1.44 (next available; capture W-α6a/b/c bundle)
- Tag: `gamora/v2.8-w-alpha-6-per-encounter-type-bands-1` per gamora seam discretion
- AGENT_STATE.md updated

**Auto-commit + auto-push** per CLAUDE.md addendum.

### 1.5 Bundle Gate-2 + Wave 5 RE-FIRE coordination (OUT OF W-α6 SCOPE; gated post W-α6 compound_pass=True)

**Bundle Gate-2 (jack-ryan; ~0.25d):** post W-α6 compound_pass=True, jack-ryan performs full bundle cross-target coherence review + Discipline #47 enforcement verification + decisions-log entry.

**Wave 5 RE-FIRE (gamora; ~3-5d):** full production season under Path α + Option B + R5-Plus scrub + Phase 5 LLM naming composed engine state. Matt D4 watch surface flagged.

These fire AFTER W-α6 close; do not pre-empt within this dispatch.

---

## 2. REQUIRED READING

LOAD-BEARING:
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — § 4 5 targets verbatim
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-7 RATIFICATION LOCKED 2026-05-28" + § "W-α6 EXECUTION"
- `agentic_orchestration/qa/pending/2026-05-28-case-9-gauntlet-encounter-coverage-gate-7-disposition.md` (jack-ryan disposition; root cause verification + 5-option ranking)

Engine source:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` — `GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1` lines 180-182; gauntlet sim eligibility check; ceiling=None per W-α2
- `~/Games/reincarnated-engine/src/reincarnated/simulation/unified_calibration_loop.py` — W-α3 Phase 2 architecture; reuse + extend
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` — W-α4 harness; reads bands for per-cell comparison
- `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` — 6 canonical valid_shells
- `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_mob_stat_profile.py` — encounter HP scaling (post boss-HP-rebase `d83049a`)

Calibrated state to preserve:
- BASE_PHYSICAL_DAMAGE_L50 + BASE_SPELL_DAMAGE_L50 per W-α3 Phase 2 scale_factor=0.664063 (do NOT recalibrate)
- W-α1 Direction A unified parity 2.337 (do NOT modify)
- W-α2 ceiling=None (do NOT re-introduce)

Disciplines:
- #1 math-before-code, **#1.1 pre-fire resource-bounds projection** (likely ~75min worst case; verify per Matt D4 over-projection pattern note), #11 empirical inspection, **#47 bounded-viability decision gate** (Matt's Gate-7 RATIFICATION authorizes this work — design-time check satisfied), #45 vocabulary lock

---

## 3. OUT OF SCOPE — explicit

- **Do NOT modify W-α1 damage formulas** (Direction A unified parity preserved).
- **Do NOT modify W-α2 ceiling state** (ceiling=None preserved).
- **Do NOT modify W-α3 BASE_*_DAMAGE_L50 values** (scale_factor=0.664063 preserved; these are calibrated against unified Phase 2 target; per-encounter bands measure population against these BASE values).
- **Do NOT modify doc 50** (gandalf canonical authority).
- **Do NOT fire Bundle Gate-2 or Wave 5 RE-FIRE** (gated post W-α6 compound_pass=True; separate KR routing).
- **Do NOT pre-author Cycle 15 commitments** (Matt D3 RATIFIED Cycle 15 scope; per-encounter bands MOVED to C14 via Option B; everything else Cycle 15 territory).
- **Do NOT address C-Hybrid algorithm, pirate-faction sub-cluster naming, R5-Plus scrub, Phase 5 LLM naming** — Cycle 15 scope OR in-flight outside Path α; W-α6 is calibration extension only.

---

## 4. RISKS + COMPLICATIONS

- **Case 10 surfacing during W-α6c harness re-run** (Matt D4 watch surface; ~30-50% base rate). If `compound_pass=False` after W-α6 calibration completes, Discipline #44 framing-refusal triggers Gate-8 disposition. Document failure pattern + per-target deltas for KR routing.
- **Per-cohort band width vs target satisfaction trade-off.** Narrow bands risk T4 specialization peak failures (kits missing [1.5, 2.0] window); wide bands risk T5 floor failures. Sensitivity analysis in math note required.
- **Reference target derivation per encounter type.** Each encounter type has different HP distribution (open_arena swarm vs boss_with_adds high HP). Per-encounter Balanced-cohort median is gamora seam choice; document rationale in math note.
- **GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 retirement coordination.** If frozenset retired (vs extended), audit downstream consumers — module-load assertions at lines 180-182 + any other references.
- **Effort estimate calibration (Matt D4 watch surface).** W-α3 Phase 2 actual ~28s vs ~62min projection. W-α6 calibration sweep × 24 cells may show similar over-projection; track actual vs projected.

---

## 5. URGENCY

**Case 9 resolution is the final blocking gate to Cycle 14 v1 close.** W-α6 close + bundle Gate-2 + Wave 5 RE-FIRE = v1 tag landing. ~5-8d total to v1 from Matt Gate-7 ratification.

Fire ASAP on jack-ryan Gate-1 PASS.

---

**KR signature:** authored per Matt 2026-05-28 Gate-7 D1+D2+D3+D4 RATIFICATION + jack-ryan Gate-7 § 4 Option B + jack-ryan Gate-3 D2 prior ratification (per-encounter-type bands) + Matt D3 Cycle 15 scope clarification (per-encounter bands MOVED to C14). Discipline #47 design-time check satisfied via Matt Gate-7 RATIFICATION authority. Gamora seam authority on math note + canonical structure + calibration sweep architecture; auto-commit + auto-push per Cycle 14 cadence.

---

## Completion record

**Completed:** 2026-05-28
**Completed by:** gamora

### W-α6a — Math note
COMPLETE. Math note at `simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md`. All sections
authored including § 5.3 (Tier 1 semantic shift), § 6.3 (initial 24-cell table), § 6.4 (empirical-range
recalibration), § 9.3 (Case 10 T4 structural diagnosis), § 11 (final BVV result).
NAMED DECISION: GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 retirement documented in § 2.

### W-α6b — Calibration sweep
COMPLETE. run_per_encounter_type_band_sweep() implemented in unified_calibration_loop.py.
Full sweep: 18 kits × 6 enc types × 4 cohorts × 30 fights = 13,440 fights; 5.4s actual (projected 1.2 hrs — over-projection ×861).
Empirical Balanced medians: open_arena=600, chokepoint=600, magic_pack=600, elite_pack=461.5, boss_with_adds=73.17, mini_boss=150.
ENCOUNTER_COHORT_KPM_BAND 24-cell table installed in gauntlet_sim.py.
W-α6c recalibration: elite_pack + mini_boss bands widened to empirical-range (Discipline #12 semantic shift).

### W-α6c — BVV harness
COMPLETE. compound_pass=False (Case 10 T4 structural barrier).

| Target | Result | Metric |
|---|---|---|
| T1 DPS variance ≤1.5× | **PASS** | 1.307× |
| T2 zero_count = 0 | **PASS** | 0 cells [W-α6 primary objective MET] |
| T3 saturation = 0 | **PASS** | structural (ceiling=None) |
| T4 specialization peaks | **FAIL** | 17/18 kits no_peaks |
| T5 floor ≥30% | **PASS** | 0 violations |

### Case 10 — T4 structural barrier (Discipline #44 framing-refusal)
Fight-engine 0.1s timing floor produces uniform 600 KPM on 5/6 encounter types. Boss_with_adds
max ratio = 1.29× < 1.5× T4 threshold. T4 peaks are structurally impossible at current kit DPS
homogeneity + mob HP profile. Resolution requires Cycle 15 Track 2 D3 per-kit DPS differentiation
OR encounter HP rebalancing (W-α7+) OR T4 target redesign (gandalf canonical authority).
**KR Gate-8 routing required.**

### GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 — NAMED DECISION
Frozenset retired as operative gate. Replaced by ENCOUNTER_COHORT_KPM_BAND (all 6 types).
jack-ryan INFO observation satisfied: retirement documented in math note § 2 and gauntlet_sim.py comments.

### Files modified
- `simulation/gauntlet_sim.py` — ENCOUNTER_COHORT_KPM_BAND, Tier 1 band_override routing, GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6, method updates
- `simulation/t4_sim_cycling.py` — band_override parameter on _compute_kpm_delta, _route_tier_1, w4g1_tier_1_sweep; direct range check semantic
- `simulation/unified_calibration_loop.py` — run_per_encounter_type_band_sweep() W-α6b function
- `simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md` — math note (all sections)
- `simulation/MIGRATION.md` — § v1.44
- `simulation/AGENT_STATE.md` — updated
- `dispatches/2026-05-28-w-alpha-6-gamora-per-encounter-type-bands.md` — this completion record

### Tag
`gamora/v2.8-w-alpha-6-per-encounter-type-bands-1`

### Downstream signals required
- KR Gate-8 disposition on Case 10 T4 structural barrier
- Bundle Gate-2 (jack-ryan) gated on Case 10 resolution — NOT cleared yet
- Wave 5 RE-FIRE gated on bundle Gate-2 — NOT cleared yet
