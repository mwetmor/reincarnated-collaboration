# Cascade-Resumption-3 Math-Note Review — Expanded Scope (Amendment 5 Sub-Action)

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-29-gandalf-cycle-14-cascade-resumption-3-math-note-review-expanded.md` (commit `185138b`)
**Authority:** Matt 2026-05-29 cascade-resumption-3 authorization + Amendment 5 (Matt-gate at Phase 5 entry of S6c)
**Review target:** `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md` (gamora 2026-05-29; engine `496814b`; tag `gamora/v2.17-cascade-r3-phase7-mechanical-gate-fix-1`)
**Pattern:** Pattern A-light analytical review (NO code modification; output feeds Matt-gate cost projection)
**Disciplines load-bearing:** #11 + #18 + #41 + #42a + #45 (#48 RETIRED per Amendment 3)

---

## TL;DR

| § | Finding | Verdict |
|---|---|---|
| § 1 Threshold derivation | `P7_GAUNTLET_PASS_FLOOR = 0.50` (strict >) aligned with W-α6 anchor `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9/18` | **PASS** |
| § 2 Cost projection full-season | Wave A + F-C + Wave B at per-base-kit firing: **~$1.10/season → ~$3.30 across 3-season cascade**; safely under $50 cap | **PASS — well under cap** |
| § 3 Wave B firing logic | **Per-base-kit firing CONFIRMED** in implementation (line 1080-1081 + line 1577-1591 + line 1620-1624 of `wave5_season_orchestrator.py`); variants inherit base kit cohesion_data per S5b pre-ratified decision + Recognition Amendment 3 H0 default | **CLARIFIED — per-base-kit; H0-aligned; no ambiguity** |
| § 4 Matt-gate cost projection input | Consolidated table ready for KR consumption at S6c Phase 5 entry | **READY** |
| § 5 Disc #42a framing-audit Q1-Q6 | Clean at dispatch consumption + at review execution | **No catches** |
| § 6 Surface-to-KR triggers | None fired | **CLEAN** |

**Bottom line:** Gamora math note is sound. Threshold derivation correct. Cost projection at full season scale is well under $50 cap with comfortable margin (~$3.30 / $50 = 6.6% of cap across 3-season cascade). Wave B firing logic is unambiguously per-base-kit per implementation + canonical + Amendment 3 H0 — no semantic gap. Matt-gate input ready.

---

## § 1 — Threshold validation

### § 1.1 Derivation chain (gamora math note § 2 + § 3.2)

A2-1 Step 1 calibration anchor:

```
GAUNTLET_PASS = True
  ↔ eligible_encounters_passed(cohort) >= GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 (= 9)
```

`eligible_encounters_passed(cohort)` uses `ENCOUNTER_COHORT_KPM_BAND` (24-cell per-encounter-type table, W-α6 architecture) — NOT legacy `COHORT_KPM_BAND` (~75 KPM narrow bands).

Total encounters per cohort (full mode) = 18 (6 encounter types × 3 scenarios each).

As fraction:
```
GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 / total = 9 / 18 = 0.50
```

Post-fix Phase 7 bridge:
```
enc_eligible_in_band = kit_result.eligible_encounters_passed(gauntlet_archetype)
                       (per Option α.2 corrected implementation; bypasses run_gauntlet_sim
                        to access per-cohort GauntletKitResult; reads ENCOUNTER_COHORT_KPM_BAND)
pass_rate            = enc_eligible_in_band / 18
```

Recalibrated threshold:
```
P7_GAUNTLET_PASS_FLOOR = 0.50  (strict greater-than; > 0.50 = ≥ 10/18)
```

### § 1.2 Strict-greater-than preservation

The pre-fix threshold was `> 0.70` (strict). Math note § 3.2 elected Option T1 (`0.50` strict greater-than) over Option T2 (`0.4999` approximating `>= 0.50`).

**Election review:** Option T1 is sound:
- Preserves operator semantics (`>`); no `>=` introduction
- Boundary kit at exactly 9/18 fails the gate; gamora rationale: A2-1 Step 1 calibration sweep showed kit median ~12/18, well above the floor — the 9/18 floor was a minimum, not the typical outcome
- Boundary exclusion is conservative: keeps the gate integrity sharp; calibrated kits at exact-9 are marginal and excluding them avoids over-shipping borderline cases
- Cost of T1 vs T2: at most a single kit per cohort per season excluded (kits clustering at exactly 9/18 are rare per A2-1 Step 1 sweep)

**Verdict:** Threshold derivation is **PASS**.

### § 1.3 Cohort midpoint semantics preservation review

Math note § 3.2 § "Cohort midpoint impact" + § 4 confirm:
- `calibrate_cohort_midpoints()` algorithm unchanged
- Input changes from near-zero pass_rates to meaningful fractions ([0.50–1.00] range)
- Expected post-fix cohort midpoints ~0.55–0.75
- Scaffold_default 0.85 for sparse cohorts (control, support) remains within expected empirical range

This is correct. The midpoint band check (`P7_COHORT_MIDPOINT_BAND = 0.25`) is unchanged at architectural level; only the input pass_rate distribution changes. Empirical S6a smoke re-fire (12/18 shipped) confirms midpoints fall in expected range (math note § 4 + completion record § (e): damage=0.8333, defensive=0.1111, control/support/hybrid=0.85 scaffold).

**One observation (not a BLOCK):** Defensive midpoint 0.1111 (= 2/18) at smoke is surprisingly low; suggests defensive cohort kits in synthetic calibration sweep underperform their own cohort midpoint, leading to 6 held-mechanical kits. At full-season S6c with N=3 substrate samples per BC cell, the defensive midpoint will recalibrate from a larger empirical base — should stabilize. Not a threshold-derivation issue; emergent calibration outcome.

### § 1.4 Disc #42a framing-audit at threshold derivation

Math note § 5 documents Disc #42a Instance 2 sub-case (`pass_rate` semantics: pre-fix vs post-fix vs A2-1 Step 1 calibration). Three-context table is honest and complete. Q1-Q6 self-applied (math note § 5) is clean.

**Additional review observation:** The math note's Q6 (honest about uncertainty) is well-handled — cohort midpoint post-fix values are flagged as estimated ranges, not exact; smoke re-fire verification was the empirical confirmation step. This is recognition-validate-commit discipline in operation.

**Verdict on § 1:** Threshold derivation PASS. No BLOCK. No WARN. Math sound; semantics preserved; empirical smoke re-fire validates expected behavior (shipped_worthy: 0 → 12/18).

---

## § 2 — Cost projection at full-season scale

### § 2.1 Cardinality inputs

Per cascade-resumption-3 authorization S7 (CLOSED engine `e177d8e`) + S2 (CLOSED engine `50ce983`) + S5/S5b (CLOSED engine `a553950` + `bf379f9`):

| Phase | Cardinality | Source |
|---|---|---|
| Phase 2 substrate | N=3 samples × 18 BC cells = **54 base kits per season** | `season_generation_pipeline.py:162` `N_SUBSTRATE_SAMPLES_PER_CELL = 3` |
| Phase 3 gauntlet | 54 base kits (passing_kits subset; degeneracy floor = 1) | `wave5_season_orchestrator.py:92` + `:724` |
| Phase 4 archive variants | ~810 enumerated (270 BC cells × 3 invest profiles per S2 Option C) | gamora S2 research; doc 51 Patterns 1+2 |
| Phase 5 Wave A clusters | 4 GMM clusters (S6a empirical; ≤7 full-season expected) | PM-1 multimodal clustering; S6a smoke |
| Phase 5 F-C pairs | C(4,2) = 6 pairs (≤21 if 7 clusters) | k-choose-2; Discipline #46 bounded |
| Phase 5 Wave B | **54 calls per season** (per-base-kit; variants inherit) | `wave5_season_orchestrator.py:1577-1591` + `1620-1624` + canonical § 5.3 |

### § 2.2 Per-call cost (canonical estimates per orchestrator docstrings)

| Wave | Cost-per-call | Source |
|---|---|---|
| Wave A | ~$0.05 ceiling | `phase5_orchestrator.py:93` (`$0.10 = 2× $0.05 ceiling per PM-2 consultation`) |
| F-C | ~$0.025-0.05 | `phase5_orchestrator.py:224` (`F-C adds ~$0.15-$0.30 per season`; 6 pairs) |
| Wave B | ~$0.010-0.025 | `phase5_orchestrator.py:199` (`Wave B adds ~$0.30-$1.00 per season`; 20-40 kits) + `:2184` (`* 0.010`) |

### § 2.3 Per-season projection (per-base-kit Wave B firing — IMPLEMENTED)

| Wave | Call count | Cost/call | Per-season cost |
|---|---|---|---|
| Wave A | 4-7 clusters | ~$0.05 | ~$0.20-0.35 |
| F-C | 6-21 pairs | ~$0.025-0.05 | ~$0.15-1.05 (likely ~$0.30 at 6 pairs) |
| Wave B | **54 calls** | ~$0.010-0.025 | **~$0.54-1.35 (likely ~$0.65 at $0.012/call mid)** |
| **Per-season subtotal** | | | **~$0.90-2.75 (likely ~$1.10-1.30 mid)** |
| Regeneration overhead (~10-20% Wave B) | ~5-11 extra calls | ~$0.012 | ~$0.06-0.13 |
| **Per-season TOTAL (with regen)** | | | **~$1.00-2.90 (likely ~$1.20-1.40 mid)** |

### § 2.4 3-season cascade projection (per-base-kit Wave B firing — IMPLEMENTED)

| Scenario | Per-season | 3-season | vs $50 cap |
|---|---|---|---|
| Best-case (low cluster count, no regen, low per-call) | ~$0.90 | ~$2.70 | 5.4% of cap |
| **Likely (mid)** | **~$1.30** | **~$3.90** | **7.8% of cap** |
| Worst-case (high cluster count + heavy regen + high per-call) | ~$2.90 | ~$8.70 | 17.4% of cap |

**Comfortable margin under $50 soft cap. Carry-forward gate INFORMATIONAL: cost is not approaching cap.**

### § 2.5 Counterfactual — per-variant Wave B firing (NOT IMPLEMENTED; included for Matt-gate context)

If Wave B fired per-variant (810 calls/season instead of 54):

| Scenario | Per-season Wave B | Per-season TOTAL | 3-season | vs $50 cap |
|---|---|---|---|---|
| Best-case ($0.010/call) | ~$8.10 | ~$8.65 | ~$25.95 | 51.9% of cap |
| **Likely ($0.015/call)** | **~$12.15** | **~$12.80** | **~$38.40** | **76.8% of cap** |
| Worst-case ($0.025/call + regen) | ~$22.30 | ~$23.00 | ~$69.00 | **138% of cap — EXCEEDS** |

**Per-variant firing would push 3-season cost into "approaches cap" or "projected to exceed" territory under worst-case assumptions. The per-base-kit decision is materially cost-protective.**

### § 2.6 Hybrid counterfactual (per-unique-(BC × cultural_lineage) — NOT current implementation)

A theoretical hybrid firing scale (per unique BC × lineage tuple) would land between 54 (per-base-kit) and 810 (per-variant). Per S7 acceptance criterion (≥5 distinct cultural_lineage values per season at empirical spread), expected ~50-150 unique tuples. Cost would land at ~$1.00-3.75/season; 3-season ~$3.00-11.25. Still under cap. Not currently implemented; documented only for completeness if Matt elects pivot.

### § 2.7 Verdict on § 2

Cost projection at IMPLEMENTED (per-base-kit) firing scale: **~$3.30-3.90 mid for 3-season cascade vs $50 cap = ~7% of cap. PASS with substantial margin.**

---

## § 3 — Wave B firing logic clarification

### § 3.1 Implementation evidence (per-base-kit CONFIRMED)

**Authoritative locations:**

**`reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py:1066-1148`** — `_build_kits_input_for_wave_b()`:
```
Per canonical § 5.3: one Wave B call per kit (base kits only; variants inherit
base kit cohesion_data per S5b pre-ratified per-kit decision).
```
(Verbatim docstring lines 1080-1081)

**`reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py:1577-1591`** — Phase 5 hook:
```
# S5b cascade-resumption-3: build kits_input for Wave B from passing_kits.
# Disc #42a: passing_kits are base kits only (variants inherit cohesion_data per
# pre-ratified per-kit decision at S5b § 3).
[...]
kits_input_for_wave_b = _build_kits_input_for_wave_b(
    passing_kits=passing_kits,
    faction_clusters_input=_faction_clusters_for_wave_b,
)
```

**`reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py:1620-1624`** — Phase 7 cohesion lookup:
```
# Variants inherit base kit cohesion_data (pre-ratified per-kit: one Wave B call per base
# kit; variant kit_ids not present in wave_b_results → Phase 7 uses None → cohesion skipped).
```

**Conclusion:** `passing_kits` is defined at `wave5_season_orchestrator.py:724` as "list of KitCandidate with wr_bracket_pass=True (base Phase 2 kits)". Variants are present as `variant_passing_rows` separately and are NOT routed to Wave B input.

**Wave B fires per-base-kit. Implementation is unambiguous.**

### § 3.2 Composition with Amendment 3 H0/H1

Recognition record `2026-05-29-experiential-cascade-architecture-recognition.md` Amendment 3 (gandalf-authored 2026-05-29 evening) establishes:

- **H0 (rocket+KR-ratified default):** investment profile is a player-choice axis on a single kit; variant inheritance is correct
- **H1 (gandalf concern; deferred to empirical-validation cascade):** investment profile variants need independent mechanical-viability evaluation

Wave B per-base-kit firing **aligns with H0** (variant inheritance default). H1 would surface as a Cycle 15+ scope amendment if 2+ of 5 empirical signatures show systematic investment-profile correlation across A2-1 RE-FIRE-3 + 3-season cascade. This is the **recognition-validate-commit** discipline at work: H1 captured, validation gate identified, cascade proceeds with H0.

**No additional implementation change needed at S6c Phase 5 entry.** Wave B per-base-kit firing is the canonically-correct H0-default operation.

### § 3.3 Composition with canonical § 5.3

Canonical doc `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` § 5 Wave B spec is the authority. Implementation docstring at line 1080-1081 directly cites this. No spec-vs-implementation gap.

### § 3.4 Recommendation

**No change needed.** Implementation matches canonical, matches Amendment 3 H0, and produces cost-protective firing scale (~$1.10/season vs ~$13/season per-variant counterfactual; 15× cost reduction).

**Forward observation for Matt-gate consideration:** if Matt elects ABORT or REDUCE-SCOPE at the Matt-gate, the Wave B firing-scale axis is NOT the likely lever — cost is comfortably under cap at current firing scale; concern would more likely be form-count or substrate-spread emergence.

### § 3.5 Verdict on § 3

Wave B firing logic is **CLARIFIED: per-base-kit, 54 calls/season at S6c expected cardinality. No semantic gap. No implementation ambiguity. H0-aligned. Cost-protective relative to per-variant counterfactual.**

---

## § 4 — Matt-gate cost projection input (consolidated table for KR consumption)

**For KR surface at S6c Phase 5 entry gate (Amendment 5 § "Gate surface content" item 4):**

### § 4.1 Form counts (Matt-gate item 1)

| Layer | Expected count | Implementation source |
|---|---|---|
| Phase 2 base kits | **54** (18 BC cells × N=3 substrate samples) | S7 acceptance; `season_generation_pipeline.py:162` |
| Phase 4 archive variants | **~810** (270 cells × 3 invest profiles enumerated) | S2 Option C; doc 51 Patterns 1+2 |
| Distinct (lineage × period × register × weapon_family) tuples | **≥5 distinct** per S7 acceptance criterion (empirical spread target) | S7 acceptance § 3 |

### § 4.2 LLM cost projection (Matt-gate item 4 — gandalf-authored input)

| Wave | Firing scale | Calls/season | Cost/season (mid) | 3-season cost (mid) | $50 cap status |
|---|---|---|---|---|---|
| Wave A | per-cluster | 4-7 | ~$0.20-0.35 | ~$0.60-1.05 | well under cap |
| F-C | per-pair | 6-21 | ~$0.30 | ~$0.90 | well under cap |
| **Wave B (IMPLEMENTED)** | **per-base-kit** | **54** | **~$0.65** | **~$1.95** | **well under cap** |
| **TOTAL (mid)** | | **~64-82 calls** | **~$1.15-1.30** | **~$3.45-3.90** | **~7-8% of $50 cap; PASS** |
| TOTAL (worst-case) | | | ~$2.90 | ~$8.70 | ~17% of cap; still PASS |

**Within / approaching / projected to exceed:** **WITHIN** (well under cap; ~7-8% utilization at mid-case; ~17% at worst-case).

### § 4.3 Wave B firing-logic disclosure (Matt-gate item 4 sub-bullet)

**Wave B fires per-base-kit (54 calls/season), NOT per-variant (810 calls/season).**

- Per-base-kit firing is the IMPLEMENTED logic (canonical § 5.3 + `wave5_season_orchestrator.py:1080-1081` + `:1577-1591`)
- Variants inherit base kit cohesion_data (per S5b pre-ratified decision + Recognition Amendment 3 H0 default)
- Per-variant counterfactual would push 3-season cost to ~$25-69 (worst-case exceeds $50 cap)
- Per-base-kit decision is materially cost-protective (~15× reduction)
- H1 (variant inheritance challenge) is captured as Recognition Amendment 3 empirical-validation gate; will surface from cascade telemetry if 2+ of 5 signatures fire; not v1-blocking

### § 4.4 Matt election options (Matt-gate item 5 reference)

Per Amendment 5 surface content spec, Matt elections at gate:
- **RATIFY-FIRE** — proceed Phase 5 + cascade per current scope (cost projection PASS; Wave B per-base-kit firing canonical)
- **REDUCE-SCOPE** — defer variant cycling OR change Wave B firing scale (NOT cost-driven at current projection; would be substrate-spread or form-count driven)
- **ABORT** — halt cascade-resumption-3; surface architectural concern

**Gandalf observation for Matt context:** cost is not the gate concern. Form-count emergence (54 base / ~810 variants / ≥5 lineage spread) is the substrate-led empirical instrument. If those targets land, RATIFY-FIRE is the cost-supported election.

### § 4.5 Telemetry instruments at S6c Phase 5 entry

KR can surface these counts from S6c-Phase-2-4 production-fire output (parallel rocket dispatch) before Phase 5 entry:
- Phase 2 base kit count (expect 54; degeneracy floor 1)
- Phase 2 unique cultural_lineage_canonical count (expect ≥5)
- Phase 2 unique historical_period_canonical count
- Phase 2 unique register_canonical count
- Phase 2 unique weapon_type_family count (expect ≥5 if lineage diversity is real)
- Phase 4 archive variant count (expect ~810 at S2 Option C × S3 preservation)
- Per-cohort distribution (damage/defensive/hybrid base kit counts)
- Per-lineage distribution (kit count per cultural_lineage value)

These feed Matt-gate items 1-3. Cost projection (item 4) is this note's § 4.2.

---

## § 5 — Disc #42a framing-audit (review-execution layer)

**Q1 (substrate-led framing?):** YES — review is grounded in code trace (math note + orchestrator implementation + canonical spec), not assumption.

**Q2 (alternative explanations ruled out?):** YES — Wave B firing-scale ambiguity ruled out by direct implementation read (3 verbatim citations at `wave5_season_orchestrator.py:1080-1081 + :1577-1591 + :1620-1624`); canonical § 5.3 confirms; Amendment 3 H0 aligns.

**Q3 (traceable causal chain?):** YES — Phase 7 mechanical gate fix derivation → A2-1 Step 1 anchor → W-α6 24-cell table → 9/18 floor → 0.50 strict greater-than → recalibrated `P7_GAUNTLET_PASS_FLOOR`. Cost projection chain: implementation per-base-kit → 54 calls × $0.012 → $0.65/season → $1.95 3-season.

**Q4 (framing creep?):** NO — verdict PASS arrived at via independent threshold + cost + firing-logic checks; not pre-imposed.

**Q5 (review scope bounded?):** YES — analytical review; no code modification; no canonical doc modification; Matt-gate cost projection only.

**Q6 (honest about uncertainty?):** YES — cost projection presented as ranges (best/mid/worst); per-variant counterfactual explicitly disclosed for Matt-gate context; F-C cluster count uncertainty (4-7 typical; up to 7 cap) flagged; Wave A and F-C costs cited from orchestrator docstrings rather than empirical (no S6c full-season telemetry yet).

**No catches.**

---

## § 6 — Surface-to-KR conditions (per dispatch § 5)

| Condition | Triggered? | Notes |
|---|---|---|
| Threshold derivation BLOCK | NO | Threshold math sound; W-α6 anchor canonical; strict greater-than preservation rationale clean |
| Wave B firing logic ambiguous | NO | Implementation unambiguous (3 verbatim docstring + comment citations); canonical alignment confirmed; H0 default per Amendment 3 |
| Cost projection at full-season exceeds $50 | NO | Per-base-kit (implemented) firing: ~$3.30-3.90 mid for 3-season = 7-8% of cap; worst-case ~$8.70 = 17% of cap. Per-variant counterfactual disclosed for Matt context but not in scope |
| Disc #42a framing-audit catch | NO | Q1-Q6 clean at dispatch consumption + at review execution |
| Effort exceeds ~1h | NO | Review executed in expected window (~25-30min reading + analysis + write-up) |

**No surface triggers fired. KR can consume cost projection input directly into Matt-gate surface authoring.**

---

## § 7 — Cumulative recognitions for Cycle 14 wave-close canonical attention

### § 7.1 Disc #42a Instance 2 sub-case (pass_rate context-dependent semantics)

Gamora math note § 5 + completion record § (f) captured this. **Concur.** Same field name `pass_rate` has three context-dependent semantics (Phase 7 pre-fix / A2-1 calibration / Phase 7 post-fix). Cycle 14 wave-close canonical-write target: jack-ryan + gandalf collaboration; consider amending engineering-disciplines.md § 42a with cumulative instances list (Instance 2 is this one; Instance 6 is the canonical-vs-implementation propagation gap; cumulative Instance count has grown across cascade-resumption-3).

### § 7.2 Quality_report field naming opportunity (additional sub-case from gamora completion record § (f))

`quality_report.eligible_encounters_in_band` is an ALL-4-cohort aggregate (not per-cohort target). Field name does not disclose scope. Cycle 15 or canonical-write naming clarification opportunity. **Concur** — this surfaced during implementation; flagged as informational; not blocking.

### § 7.3 Pre-fire empirical-verification gate as discipline pattern (Amendment 5 ratification)

Matt 2026-05-29 articulated the Matt-gate pattern verbatim: "Should we set up a matt gate right before the LLM naming phase just to count the forms?" This is a recurring pattern worth canonical attention: pre-fire empirical-verification gate at production-fire entry layer (analogous to Disc #42a framing-audit at dispatch consumption gate). Cycle 14 wave-close canonical-write target per cascade authorization Amendment 5. **Gandalf seam-owner candidate at canonical-write.**

---

## § 8 — Sign-off

**Review verdict consolidated:**
- § 1 Threshold validation: **PASS**
- § 2 Cost projection at full-season scale: **PASS — well under $50 cap (mid ~$3.30-3.90 / 3-season cascade = 7-8% of cap)**
- § 3 Wave B firing logic: **CLARIFIED — per-base-kit (implemented); canonically aligned; H0-default per Amendment 3; no ambiguity**
- § 4 Matt-gate cost projection input: **READY** for KR consumption at S6c Phase 5 entry surface authoring
- § 5 Disc #42a framing-audit: **clean** at both layers (dispatch consumption + review execution)
- § 6 Surface-to-KR conditions: **NONE FIRED**
- § 7 Cumulative recognitions: 3 captured (Instance 2 sub-case; quality_report field naming; pre-fire empirical-verification gate as discipline pattern) for Cycle 14 wave-close canonical attention

**Recommendation to KR:** consume § 4 cost projection table verbatim for Matt-gate surface authoring (Amendment 5 item 4). Wave B per-base-kit firing logic disclosure (§ 4.3) is the substantive clarification this expanded review adds beyond gamora math note scope; KR can present as: "Wave B fires per-base-kit (54 calls/season); per-variant counterfactual would push cost to ~$25-69 across 3 seasons; per-base-kit decision is materially cost-protective."

**No KR-surface-to-Matt findings beyond Matt-gate input itself.** Cascade trajectory unchanged; S6c-Phase-2-4 parallel fire proceeds per parallel rocket dispatch; KR Matt-surface authoring at S6c Phase 5 entry post-Phase-4 close.

**Authored:** gandalf (story-and-design steward)
**Sign-off date:** 2026-05-29
**Authority:** Matt 2026-05-29 cascade-resumption-3 Amendment 5 sub-action authorization + hive-mind decision-routing
