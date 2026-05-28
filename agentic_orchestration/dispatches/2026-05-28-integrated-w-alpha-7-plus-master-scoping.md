# DISPATCH — Integrated W-α7+ Master Scoping — Cycle 14 v1 Architectural Close (6-Phase Decomposition)

**Authored:** 2026-05-28 evening
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipients:** gandalf (Phase 2 design lead) + rocket (Phase 3 P1+P2 implementation) + gamora (Phase 3 BASE re-derivation + Phase 4 multi-dim calibration + Phase 5 BVV update + Wave 5 RE-FIRE) + drax (Phase 5/6 loadout UI revival) + jack-ryan (Gate-1 of this master + Phase 6 disciplines canonical-batch + parallel retirements throughout)
**Pattern:** Pattern B master scoping (~14-22d total; replaces separate Option B + prior W-α7 work)
**Status:** PENDING — fires jack-ryan Gate-1 on receipt; Phase 2 gandalf design fires in PARALLEL per Matt explicit authorization (does not gate on Gate-1)
**Authority:** Matt 2026-05-28 evening RATIFICATION AMENDMENT — integrated W-α7+ scope absorbs case 9 + case 10 + case 11 + case 12

---

## 0. AUTHORITY + ARCHITECTURAL RECOGNITION

**Matt 2026-05-28 evening D1+D2+D3+D4+D5 RATIFICATION AMENDMENT** verbatim:

**Architectural recognition:**
- Path α delivered **1.24× cross-path parity at FIXED character profile**
- Investment-scaling architecture gap surfaced subsequently shows Path α's calibrated BASE_DAMAGE_L50 values are SCAFFOLD per Discipline #39 — calibrated at "implicit no-investment" profile which is about to change
- Solving symptom (Option B per-encounter-type bands at fixed profile) AND root (W-α7 investment scaling + base value recalibration) in PARALLEL = double calibration work + risk surface at seam

**Path α work status (D1 RATIFIED):**
- **KEEP:** W-α1 (damage formula Direction A) / W-α2 (ceiling Option B Remove) / W-α3 Phase 1 (unified calibration architecture) / W-α4 (BVV harness infrastructure) / W-α5 (canonical retirements + **Discipline #47 LOAD-BEARING**)
- **SCAFFOLD:** W-α3 Phase 2 calibrated BASE_DAMAGE_L50 values + scale_factor (superseded by integrated recalibration under multi-profile)
- **EMPIRICAL WAYPOINT:** 1.24× cross-path parity confirms unified-formula approach works; re-verified under multi-profile

**Tag retained (D3):** `v1-cycle-14-bounded-viability-substrate-led`.

**Case 12 acknowledged (D4):** Path α calibrated BASE_DAMAGE values recognized as scaffold once investment scaling architecture was discovered. Mode A design-dialog drift catch.

**Coordination penalty acknowledged (D5):** ~0.5d cost to pause Option B in-flight; offset by ~2-3d savings + architectural cleanliness + closed risk surface at seam.

---

## 1. INTEGRATED 6-PHASE DECOMPOSITION

### Phase 1 — Pause Option B; design integrated scope (~1d) — KR

**Status: IN PROGRESS THIS TURN.** Actions:
1. ✅ Author this master scoping (integrated W-α7+ replaces separate Option B + W-α7 work)
2. ✅ Mark superseded dispatches with SUPERSEDED status header (audit trail preserved):
   - `2026-05-28-w-alpha-6-gamora-per-encounter-type-bands.md` — SUPERSEDED; Phase 1/2 input
   - `2026-05-28-w-alpha-7-master-scoping-investment-scaling.md` — SUPERSEDED; replaced by this
3. ✅ Hive-mind state updated with integrated W-α7+ + cases 10+12 register

**W-α6 in-flight work absorbed as Phase 1/2 input per Matt D1:**
- ENCOUNTER_COHORT_KPM_BAND 24-cell table (engine `7acf66c`) — values RECALIBRATED under integrated multi-profile in Phase 3+4; structure persists
- GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 retired as operative gate (NAMED DECISION per jack-ryan INFO)
- Math note + MIGRATION.md § v1.44 + gauntlet_sim/t4_sim_cycling/unified_calibration_loop changes preserved
- Case 10 forensic (fight-engine 0.1s timing floor mechanism) = Phase 3 design constraint

**Jack-ryan Gate-1 verdicts from prior W-α7 master scoping (preserved + integrated):**
- Amendment #1 (gandalf formula-composition check) → Phase 2 gandalf requirement
- Amendment #2 NODE_MAX path → VERIFIED at `reincarnated-loadout/src/data/cycle13Types.ts:255` ✅
- Amendment #3 (profile semantic definitions) → Phase 2 gandalf requirement
- Rocket Amendment (math note application order) → Phase 3 rocket math note requirement
- Drax Amendment (tag v1.2) → Phase 5/6 drax tag
- Case 11 Mode A canonical extension → doc 51 sufficient (no Discipline #48 mint)
- Scope-absorption-ceiling → formally absorbed via Matt's 6-phase decomposition

### Phase 2 — Investment scaling design (~1.5-2.5d) — gandalf seam lead; PARALLEL with Gate-1

**Owner:** gandalf (design + canonical author; Tier-A)
**Consultation:** rocket (formula structure feasibility) + gamora (calibration anchor + per-tier ratio preservation)

**Scope:**
- **Pattern 1 active skill damage scaling formula specification** — gandalf canonical authority on structural intent (e.g., additive `base × (1 + c × n)` vs multiplicative variants vs threshold-shaped; Discipline #47 verification that formula keeps peak KPM ratios within [1.5, 2.0] × cohort median at max investment — jack-ryan Gate-1 Amendment #1 fold-in)
- **Pattern 2 passive skill effect scaling formula specification** — same architecture review per pattern; gandalf canonical authority
- **Calibration anchor decision** — max-investment OR midpoint OR per-pattern-distinct anchor; rationale captured for Phase 3 implementation + Phase 4 multi-dim calibration target
- **Per-tier ratio preservation: 1:1.5:2.17:4.0** (Matt Phase 2 spec verbatim) — T1:T2:T3:T4 calibrated ratio sequence; Phase 3 BASE re-derivation must preserve this ratio under investment scaling
- **Per-encounter-type band design integrated** — was Option B; now integrated. ENCOUNTER_COHORT_KPM_BAND structure from W-α6 preserved; values recalibrated under multi-dim space
- **Profile semantic definitions (Jack-ryan Gate-1 Amendment #3)** — conceptual labels: low / mid / max / mixed-profile (numeric thresholds = Phase 3+4 gamora seam discretion)
- **6-pattern canonical doc** at `canonical/<NN>-investment-scaling-6-pattern-architecture-2026-05-28.md` (suggested 51) capturing Patterns 1+2 detailed semantics for Phase 3 + Patterns 3-6 (threshold unlocks / QoL modifiers / synergy bonuses / resource economy modifiers) canonical-locked for Cycle 15+ implementation

**Cross-references:** doc 50 (bounded-viability); doc 47 § 3 (4 damage-scaling paths); NODE_MAX at `reincarnated-loadout/src/data/cycle13Types.ts:255` (Jack-ryan Amendment #2 source-verified).

**Acceptance:** canonical doc landed + cross-references updated + Discipline #45 vocabulary grep PASS + formula structures specified + per-tier ratio preservation criterion locked.

**Tag:** `gandalf/v1.14-w-alpha-7-plus-phase-2-investment-scaling-canonical-1`.

### Phase 3 — Integrated implementation (~3-5d) — rocket + gamora; SEQUENTIAL post Phase 2

**Owner:** rocket (P1+P2 implementation in per_skill_emitter + damage_resolver) + gamora (per-encounter bands in gauntlet_sim + BASE_DAMAGE_L50 re-derivation + scale_factor re-derivation; case 10 timing-floor encounter HP rebalancing)

**Sub-streams:**

**Phase 3a — rocket Pattern 1 implementation:**
- Active skill damage scaling per gandalf canonical formula (Phase 2 lock)
- `per_skill_emitter.py` + `damage_resolver.py` touched
- Math note (Discipline #1) at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-plus-phase-3-pattern-1-2026-05-28.md`
- **Application-order specification (jack-ryan Gate-1 amendment):** `base × damage_modifier × (1 + c × n)` vs `base × (1 + c × n) × damage_modifier` — rocket math note resolves explicitly + addresses W-α3 calibration composition
- MIGRATION.md
- Tag: `rocket/v1.9-w-alpha-7-plus-pattern-1-1`

**Phase 3b — rocket Pattern 2 implementation (parallel with 3a or sequential per rocket seam discretion):**
- Passive skill effect scaling per gandalf canonical formula
- Same composition framing as 3a
- Tag: `rocket/v1.10-w-alpha-7-plus-pattern-2-1`

**Phase 3c — gamora encounter HP rebalancing (case 10 resolution):**
- Per-encounter HP factors in `endgame_mob_stat_profile.py` adjusted to escape fight-engine 0.1s timing floor for low-HP encounter types (open_arena/chokepoint/magic_pack/elite_pack)
- mini_boss + boss_with_adds factor ranges re-evaluated to ensure T4 specialization peaks at 1.5-2.0× cohort median become achievable
- Cross-seam ADR-004 touch (generation seam rocket-owned; gamora touches per existing case 8 ANCHOR INTENTS precedent)
- Math note + MIGRATION.md
- Tag: `gamora/v2.9-w-alpha-7-plus-phase-3-encounter-hp-rebalance-1`

**Phase 3d — gamora BASE_DAMAGE_L50 re-derivation:**
- Under new W-α7+ formulas + new encounter HP + per-investment-profile reference targets
- Replaces W-α3 Phase 2 calibrated values (scaffold per Matt D1)
- Math note + MIGRATION.md
- Tag: `gamora/v2.10-w-alpha-7-plus-phase-3-base-rederivation-1`
- **SEQUENTIAL post Phase 3c (jack-ryan Gate-1 Amendment):** BASE_DAMAGE_L50 re-derivation CONSUMES updated encounter HP factors from 3c; Phase 3d CANNOT begin until Phase 3c is tagged. Re-deriving BASE values against in-flight or pre-3c HP factors produces invalid calibration anchor.

**Phase 3 close signal:** all 4 sub-streams tagged + AGENT_STATE.md updated; downstream Phase 4 consumes. **Note (jack-ryan Gate-1 Amendment):** Phase 3c → Phase 3d ordering is a HARD DEPENDENCY; the four sub-streams are NOT fully parallel. 3a + 3b + 3c may parallel-fire post Phase 2 canonical lock; 3d fires sequentially after 3c close signal.

### Phase 4 — Multi-dimensional calibration (~2-4d) — gamora

**Scope:**
- Calibration target: bounded-viability across **paths × cohorts × encounter_types × investment_levels** = 4 × 4 × 6 × ~4-profile = ~384-cell space
- Binary search across expanded space (per Matt Phase 4 spec)
- Verify cross-path parity ≤1.5× at multiple investment profiles per doc 50 § 4.1
- Reuses `unified_calibration_loop.py` Phase 1+2 architecture (W-α3 Phase 1 KEEP) + extends to multi-dim
- **Discipline #1.1 pre-fire resource-bounds projection:** 384-cell sweep at W-α6 actual ~5.4s / 13,440-fight sweep extrapolated = ~few minutes max; project explicitly in math note (Matt D4 over-projection watch surface continues)
- Math note at `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-7-plus-phase-4-multi-dim-calibration-2026-05-28.md`
- Tag: `gamora/v2.11-w-alpha-7-plus-phase-4-multi-dim-calibration-1`

**Acceptance:** scale_factor + BASE values converged; per-encounter bands populated under multi-profile; cross-path parity ≤1.5× preserved at each profile.

### Phase 5 — BVV harness update + Wave 5 re-fire (~3-4d) — gamora + drax parallel

**Phase 5a — gamora BVV harness multi-dim update:**
- Harness measures across multi-dimensional space (paths × cohorts × encounter_types × investment_levels)
- Per-profile compound_pass + aggregate compound_pass
- Extends `bounded_viability_validation.py` (W-α4 harness KEEP); preserves Track 1 partition utility reuse per Matt D3 from Gate-7 (now superseded but pattern persists)
- Tag: `gamora/v2.12-w-alpha-7-plus-phase-5a-bvv-multi-dim-1`

**Phase 5b — drax loadout UI revival (parallel with 5a):**
- NODE_MAX surfaces become MECHANICALLY MEANINGFUL post-Phase-3 implementation
- Loadout UI displays investment-scaled output (per-skill point delta visible)
- Drax workstream revives from DEFERRED status (W-α7-drax in prior scoping)
- Tag: `drax/v1.2-w-alpha-7-plus-phase-5b-loadout-investment-ui-1` (jack-ryan Gate-1 Amendment: confirmed v1.2 next available)
- Cross-seam coordination: drax consumes rocket P1+P2 schema additions per Phase 3 MIGRATION.md

**Phase 5c — gamora Wave 5 RE-FIRE:**
- Full production season under composite engine state: **Path α + integrated W-α7+ + R5-Plus scrub + Phase 5 LLM naming**
- Bundle Gate-2 multi-coverage = jack-ryan reviews per-target satisfaction across multi-dim space
- KR fires Wave 5 RE-FIRE post Phase 5a + Phase 4 compound_pass=True
- Tag: `gamora/v2.13-w-alpha-7-plus-phase-5c-wave-5-refire-1`

**Bundle Gate-2 trigger (jack-ryan; ~0.25d):** full cross-stream coherence + Discipline #47 verification + decisions-log batch entry

### Phase 6 — Final close (~3-5d) — jack-ryan + gandalf + Matt

**Phase 6a — jack-ryan disciplines #41-#46 batched canonical-write (post Wave 5 Gate-2; Matt D10 Gate-5 precedent):**
- Canonical-write batched at Cycle 14 v1 close (not interspersed)
- Tag: `jack-ryan/v1.9-w-alpha-7-plus-phase-6a-disciplines-batch-1`

**Phase 6b — gandalf A/B comparison (post Wave 5 RE-FIRE):**
- 6-measurement-dimension A/B comparison (Matt 2026-05-27 Wave 5 pre-ratification #3)
- Comparison artifact at `agentic_orchestration/gandalf/notes/`
- Tag: `gandalf/v1.15-w-alpha-7-plus-phase-6b-a-b-comparison-1`

**Phase 6c — Matt v1 ratification:**
- Final review of Cycle 14 v1 close artifacts
- Matt cuts `v1-cycle-14-bounded-viability-substrate-led` tag
- Discipline #47 enforcement final confirmation (5/5 targets simultaneously satisfied)

---

## 2. JACK-RYAN PARALLEL RETIREMENTS (W-α5-style throughout all phases)

**Owner:** jack-ryan (canonical-write seam)
**Effort:** ~0.5d total across phases

- Decisions-log entries: case 9 final close (W-α6 retired + integrated absorption) + case 10 (timing-floor barrier; Phase 3 resolution) + case 11 (investment scaling design-dialog) + case 12 (BASE values as scaffold; integrated reframe)
- Cross-references throughout master scoping + Phase artifacts
- Discipline #39 framework continued maturation: cases 11+12 design-dialog layer extension (doc 51 sufficient per prior Gate-1)
- Per-phase Gate-2 verification (not full Gate-2 disposition; targeted sub-stream verification)

---

## 3. CROSS-STREAM SEQUENCING + COORDINATION

```
Phase 1 (KR; this turn)
  ↓
Phase 2 (gandalf; PARALLEL with Gate-1 per Matt explicit auth)
  ↓
Phase 3 [3a + 3b + 3c + 3d] (rocket + gamora; parallel + intra-stream coord)
  ↓
Phase 4 (gamora; sequential)
  ↓
Phase 5 [5a + 5b + 5c] (gamora + drax parallel; 5c sequential after 5a + Phase 4)
  ↓
Phase 6 [6a + 6b + 6c] (jack-ryan + gandalf + Matt; mostly sequential)

Parallel throughout:
- Jack-ryan retirements (~0.5d total)
```

---

## 4. CYCLE 14 V1 CLOSE TRAJECTORY

| Phase | Effort | Calendar |
|---|---|---|
| Phase 1 (KR pause + reframe) | ~1d | Day 0-1 |
| Phase 2 (gandalf design + consultation) | ~1.5-2.5d | Days 1-3 |
| Phase 3 (integrated implementation) | ~3-5d | Days 3-8 |
| Phase 4 (multi-dim calibration) | ~2-4d | Days 8-12 |
| Phase 5 (BVV harness + drax UI + Wave 5 RE-FIRE) | ~3-4d | Days 12-15 |
| Phase 6 (final close + Matt v1) | ~3-5d | Days 15-20 |
| Jack-ryan retirements (parallel) | ~0.5d | Days 1-15 |

**Total: ~14-22d from this ratification.** Path α 4-6 week budget intact (~42 calendar days; ~22-28 days margin if v1 lands Day 14-22).

---

## 5. GATE-1 ACCEPTANCE CRITERIA (jack-ryan DESIGN-MODE)

This master scoping is the integrated successor to two prior dispatches (W-α6 + prior W-α7). Specific verification:

- Per-phase scope adequacy (Phase 1-6 framing matches Matt RATIFICATION AMENDMENT verbatim)
- W-α6 work-product absorption framing — values recalibrated under integrated multi-profile; structure persists. Adequate?
- Case 10 timing-floor constraint integration into Phase 3c (gamora encounter HP rebalancing) — sufficient?
- Case 12 BASE values scaffold resolution via Phase 3d (BASE re-derivation) — clean?
- Jack-ryan Gate-1 prior verdict fold-ins — all 5 amendments integrated correctly?
- Cross-seam coordination: 4-seam parallel + intra-phase coordination — adequate signal mechanisms?
- Discipline #47 enforcement at each phase — bounded-viability decision-gate check satisfied at design-time?
- Discipline #1.1 resource-bounds projections at Phase 3+4 — adequate given W-α3+W-α6 ~800-1200× over-projection pattern?
- Wave 5 RE-FIRE composite (Path α + integrated W-α7+ + R5-Plus + Phase 5 LLM naming) — coordination mechanism adequate?
- Bundle Gate-2 trigger at Phase 5c — fires only after Phase 4 compound_pass=True + Phase 5a multi-dim harness ready + Phase 5b drax UI parallel landed?

**Return: PASS / PASS-WITH-AMENDMENTS / BLOCK. Phase 2 fires in PARALLEL with Gate-1 per Matt explicit auth (does not gate).**

---

## 6. RISKS + COMPLICATIONS

- **Phase 2 + Gate-1 parallelism:** if Gate-1 surfaces amendments to Phase 2 scope (e.g., formula structure question), gandalf may need to absorb mid-execution. Established cadence supports.
- **Phase 3 case 10 encounter HP rebalancing:** invalidates W-α3 Phase 2 calibration anchor (scaffold per Matt D1); is the correct integration path
- **Phase 3 cross-seam coordination:** gamora touches `endgame_mob_stat_profile.py` (rocket-owned) per case 8 ANCHOR INTENTS precedent; MIGRATION.md captures
- **Phase 4 multi-dim calibration combinatorial space:** ~384 cells; W-α6 ~5.4s actual scales to ~few minutes; projection in math note
- **Phase 5 Wave 5 RE-FIRE composition:** 4-vector composite (Path α + W-α7+ + R5-Plus + Phase 5 LLM naming); KR authors readiness checklist at Bundle Gate-2 (jack-ryan Gate-1 prior recommendation)
- **Case 13+ probability:** integrated reframe absorbs cases 9+10+11+12 but framework may catch additional drift during execution; each follows Gate-N → Matt cadence
- **Drax revival coordination:** drax workstream DEFERRED throughout Path α; reactivates Phase 5b; communication mechanism via dispatch + MIGRATION.md
- **Sustained-intensity threshold (Matt D2):** 14-22d total at upper-mid of 4-6 week budget; re-evaluation hook applies if cases extend further

---

## 7. URGENCY + KR ROUTING

**Cycle 14 v1 close trajectory ~14-22d from this ratification.** Phase 1 completes this turn; Phase 2 fires parallel with Gate-1; Phase 3+ fires post Gate-1 PASS + Phase 2 canonical lock.

**KR immediate next actions:**
1. ✅ Phase 1 master scoping authored (this dispatch)
2. ⏳ Mark superseded dispatches with SUPERSEDED status header (next; quick edits)
3. ⏳ Commit + push Phase 1 artifacts
4. ⏳ Fire jack-ryan Gate-1 (background; ~15-20min)
5. ⏳ Fire gandalf Phase 2 in PARALLEL (does not gate on Gate-1 per Matt explicit auth)

**Cycle 14 case register status (post-evening-ratification):**
- Cases 1-7: Mode A engine empirical-execution layer
- Case 8: Mode B canonical scaffold resolution
- Case 9: Mode A engine empirical-execution layer (gauntlet encounter coverage; W-α6 partial-resolved; final resolution integrated W-α7+ Phase 3)
- Case 10: Mode A engine empirical-execution layer (fight-engine timing floor; integrated W-α7+ Phase 3c+3d absorbs)
- Case 11: Mode A design-dialog layer (investment scaling gap)
- Case 12: Mode A design-dialog layer (BASE values scaffold; integrated reframe resolution)

---

**KR signature:** authored per Matt 2026-05-28 evening D1+D2+D3+D4+D5 RATIFICATION AMENDMENT verbatim 6-phase decomposition + jack-ryan Gate-1 prior verdict fold-ins + W-α6 work-product preservation + cases 10+12 absorption + Path α KEEP/SCAFFOLD/EMPIRICAL framing. Integrated successor to W-α6 + prior W-α7 master scoping (both superseded). Phase 2 gandalf design fires PARALLEL per Matt explicit authorization. Q10 quality > timeline + architectural-honesty path + closed risk surface at seam between symptom and root.

---

## Completion record — Phase 3d (gamora)

**Completed:** 2026-05-28
**Agent:** gamora
**Commit:** `978a39e` — W-α7+ Phase 3d — BASE_DAMAGE_L50 re-derivation + TIER_COEFFICIENTS architecture correction
**Tag:** `gamora/v2.10-w-alpha-7-plus-phase-3-base-rederivation-1`

### Deliverables

1. **Math note (Discipline #1):** `simulation/math/w-alpha-7-plus-phase-3d-base-rederivation-2026-05-28.md` — §§ 1-10 complete including §10 actuals post-convergence
2. **TIER_COEFFICIENTS updated** to doc 51 §5.1 spec `{1: 1.00, 2: 1.50, 3: 2.17, 4: 4.00}` in `generation/per_skill_emitter.py` + `simulation/damage_resolver.py` (Discipline #12)
3. **BASE_SPELL_DAMAGE_L50 = 20726.5 (all 4 tiers, uniform)** in `generation/per_skill_emitter.py` — W-α3 per-tier scaffold superseded
4. **BASE_PHYSICAL_DAMAGE_L50 = 48467.0 (all 4 tiers, uniform)** in `generation/per_skill_emitter.py`
5. **_BASE_SPELL_DAMAGE_FALLBACK = 20726.5 (all tiers)** + **_BASE_SPELL_DAMAGE_FALLBACK_DEFAULT = 20726.5** in `simulation/damage_resolver.py`
6. **`_patch_kits_option_a()`** added to `simulation/unified_calibration_loop.py`; binary search loop updated to apply Option A patch before each iteration
7. **MIGRATION.md §v1.46 filed** — two semantic shifts documented; star-lord seam: no action required
8. **AGENT_STATE.md updated** with Phase 3d status + commit hash + tag

### Acceptance criteria — all PASS

| Criterion | Result |
|---|---|
| Cross-path parity ≤1.5× | 1.290× PASS |
| Per-tier ratio 1:1.50:2.17:4.00 (±5%) | Exact mathematical identity PASS |
| Calibration convergence ≤5% delta | KPM=73.17, delta=2.44% PASS |
| Option A calibration anchor applied | _patch_kits_option_a() installed PASS |
| Zero new test regressions | 101/101 PASS (1 pre-existing only) PASS |

### Discipline #12 semantic shifts declared

1. TIER_COEFFICIENTS: `{1.00, 1.15, 1.35, 2.00}` → `{1.00, 1.50, 2.17, 4.00}` — inter-tier KPM progression semantics shift; historical fight results under old coefficients carry old semantics
2. BASE values uniform: W-α3 per-tier calibrated values replaced with uniform Phase 3d values — W-α3 Phase 2 scaffold superseded

### Phase 3 sequence status

Phase 3a (Pattern 1) + 3b (Pattern 2) + 3c (encounter HP) + 3d (BASE re-derivation): all COMPLETE. Phase 3 sequence fully closed. Phase 4 multi-dim calibration can fire.
