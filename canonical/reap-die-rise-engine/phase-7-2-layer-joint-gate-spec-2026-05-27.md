# Phase 7 2-Layer Joint-Gate Composition Spec — Cycle 14 v1

> **STATUS:** CURRENT — gandalf Seam 1 composition spec authored 2026-05-27 per dispatch `2026-05-27-phase-7-2-layer-joint-gate.md`; jack-ryan Seam 2 Discipline #18 canonical-write fires next; both seams together produce Phase 7 ready-for-Wave-5-consumption verdict-spec.
>
> **Date:** 2026-05-27
> **Author:** gandalf (story-and-design steward)
> **Status:** CURRENT — pending jack-ryan Seam 2 canonical-write at engine math/ folder
> **Authority:** Matt 2026-05-27 pre-ratification #1 (Phase 7 2-layer joint-gate thresholds LOCKED Cycle 14 v1)
> **Companion docs:**
> - `agentic_orchestration/dispatches/2026-05-27-phase-7-2-layer-joint-gate.md` — parent dispatch
> - `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 5.7 — Phase 7 canonical workflow position
> - `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` — Phase 5 per-node cohesion rubric (upstream)
> - `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes (cohort partition substrate)
> - `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` — F-5 / F-1 / D-5 references
> - `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #18 / #43 / #46
> - `agentic_orchestration/dispatches/2026-05-27-wave-5-production-season-dispatch.md` — Position B downstream consumer
>
> **Discipline #42 framing-audit fired at consumption — see § 0.1.**

---

## 0. TL;DR

Phase 7 is the per-kit acceptance gate at season-close. It evaluates each kit on TWO independent layers (mechanical + cohesion), composes both layers into a single verdict (`SHIPPED-WORTHY` / `HELD-cohesion-fail` / `HELD-mechanical-fail`), and emits the verdict + logging record for downstream Wave 5 consumption.

**Cycle 14 v1 STATIC verdict thresholds:**

| Layer | Pass criterion |
|---|---|
| **Mechanical pass** | Phase 4 `archive_status = 'ACTIVE'` AND gauntlet PASS rate >70% within ±25% of cohort midpoint per kit's cohort |
| **Cohesion pass** | Phase 5 per-node aggregate `cohesion_score ≥ 0.75` (kit-level rollup ≥ 0.75) AND `phase7_gate_status ∈ {canonical, placeholder}` |
| **Joint verdict** | mechanical PASS AND cohesion PASS → SHIPPED-WORTHY; otherwise HELD-with-reason |

**HELD verdict state machine:**

| HELD reason | Disposition | Re-entry rule |
|---|---|---|
| cohesion-fail only (mech PASS, coh FAIL) | return-to-Phase-5 with new prompt seed | max 2 retries; 3rd fail → discard |
| mechanical-fail (mech FAIL regardless of coh) | discard | no retry; Phase 4 already rejected via reject_pool |
| both fail | discard | mechanical-fail subsumes |

**Mutability:** STATIC at Cycle 14 v1. Cycle 15+ auto-tune trigger criteria specified in § 5.

---

## 0.1 Discipline #42 framing-audit (fired at dispatch consumption)

**Q1 — load-bearing framing assumptions in parent dispatch:**

1. Phase 7 evaluates per-KIT (not per-season-aggregate); each kit gets its own verdict.
2. Phase 4 archive ACCEPTED signal exists as a binary flag on each kit per-cell.
3. Phase 5 cohesion-judge output exists as a per-kit confidence/compliance score readable at Phase 7 time.
4. 5-cohort partition (Damage/Defensive/Control/Support/Hybrid) is operationally well-defined from existing BC axes.
5. Cohort midpoints are empirically calibratable from production-season data.
6. Return-to-Phase-5 with new prompt seed produces convergent re-LLM behavior (does not infinite-loop given a retry cap).
7. STATIC mutability composes with Cycle 15+ auto-tune without retrofit.

**Q2 — refutation evidence currently in hand:**

1. **(REFUTATION-FOUND-AND-ROUTED)** The parent dispatch states "ExportFactionCluster schema includes cohesion_judge_confidence + ai_tell_compliance_score fields" — verified-empirically against engine `bf7f659/src/reincarnated/export/schemas.py` (lines 542-652): those literal field names do NOT exist. Actual cohesion-bearing fields on ExportFactionCluster:
   - `cluster_compactness: float | None` (PM-1 silhouette score)
   - `cosine_similarity_max: float | None` (cross-faction diversity)
   - `diversity_flag: bool | None`
   - `phase7_gate_status: str = "placeholder"` (values: `"canonical"` or `"placeholder"`)
   - `regeneration_fired: bool | None`
   
   The `ai_tell_compliance_score` field is referenced in `agentic_orchestration/dispatches/2026-05-27-wave-3-phase-5-cohesion-judge-llm-with-f-c.md` Seam 2 as an EXPECTED ExportFactionRelationship field; not yet implemented. Resolution: this spec defines Phase 7 cohesion-layer input semantics against BOTH the per-node `cohesion_score` (per Phase 5 calibration spec § 3.6; already specified) AND the cluster-level `phase7_gate_status + cluster_compactness + diversity_flag` fields (already in `bf7f659`). The Wave 3 F-C `ai_tell_compliance_score` addition is forward-compatible (placeholder mapping in § 2.4).

2. The 5-cohort partition (Damage/Defensive/Control/Support/Hybrid) is NOT defined in any prior canonical doc. Matt's pre-ratification names it but does not operationalize. Resolution: this spec operationalizes the cohort partition from 8 locked BC axes in § 1.3 (substrate-led derivation; no new taxonomy invented).

3. `phase7_gate_status = "placeholder"` is Reincarnated v1 DEFAULT (faction_visibility = invisible). Star-lord PM-2 consultation explicitly states Phase 7 MUST accept placeholder status (schemas.py line 643). Resolution: cohesion-pass semantics in § 2 specify acceptance for BOTH `canonical` and `placeholder` states; placeholder maps to "LLM short-circuit; algorithmic cohesion only" branch.

4. Return-to-Phase-5 with new prompt seed: substrate evidence is the Phase 5 calibration spec § 3.6 re-roll mechanism (max 3 attempts per node). Phase 7 retry is at the KIT level, not the node level. Resolution: § 3 specifies kit-level retry cap (2 retries; 3rd-fail discard) explicitly distinct from node-level re-roll cap.

**Q3 — refine framing or execute?**

**Q3 = NO (proceed with execution).** Refutation evidence surfaced in Q2 is RESOLVABLE WITHIN SPEC AUTHORING — the dispatch's literal citation-error on field names is a documentation precision question, not a framing flaw. The actual data substrate (Phase 4 archive_status, Phase 5 cohesion_score per node, ExportFactionCluster cluster-level fields) is sufficient to author the joint-gate spec. The 5-cohort partition operationalization is gandalf-judgment scope per the dispatch open question Q-P7-1. Sub-agent proceeds; Q2-1 finding surfaced explicitly in § 2.4 + § 6 so future readers and jack-ryan Seam 2 see the actual schema-binding instead of the citation-shortcut.

**Framing-audit fields per Discipline #42:**

- Framing-audit fired: yes
- Q1 load-bearing assumptions identified: 7 (enumerated above)
- Q2 refutation evidence: 4 surfaced (all resolvable within scope; logged in § 2.4 + § 6)
- Q3 outcome: PROCEED

---

## 1. Mechanical pass spec

### 1.1 Inputs at Phase 7 mechanical-evaluation time

Per kit:
- `kit_id` (Phase 4 kit_archive PK)
- `bc_cell_id` (8-axis BC coordinate)
- `archive_status ∈ {'ACTIVE', 'DOMINATED', 'EVICTED'}` (Phase 4 disposition)
- `q1` win_rate_normalized (Phase 4 archive field; spatial_gauntlet/phase4_db.py § 45)
- `q2` kpm_in_band (Phase 4 archive field)
- `q3` resource_sustainability (Phase 4 archive field)
- `q4` defensive_robustness (Phase 4 archive field)
- `q5` skill_coherence (Phase 4 archive field)
- 8-axis BC coordinate (for cohort classification per § 1.3)

### 1.2 Mechanical pass criterion (formal)

```
mechanical_pass(kit) := 
    (kit.archive_status == 'ACTIVE')
    AND (gauntlet_pass_rate(kit) > 0.70)
    AND (abs(gauntlet_pass_rate(kit) - cohort_midpoint(cohort_of(kit))) <= 0.25)
```

Three conjunctive conditions. Each MUST hold for mechanical pass.

- **`archive_status == 'ACTIVE'`** — kit survived Phase 4 math gates (Pareto, crowding, Mahalanobis, KL, eviction). Note: `archive_status = 'DOMINATED'` or `'EVICTED'` means Phase 4 rejected the kit; Phase 7 inherits that verdict and emits HELD-mechanical-fail without re-evaluation (no salvage).
- **`gauntlet_pass_rate(kit) > 0.70`** — the kit, when simulated through the standard gauntlet suite (see § 1.4), passes >70% of encounters. This is a stricter floor than archive ACCEPTED; archive ACCEPTED only requires Pareto non-dominance, NOT a minimum WR floor.
- **`|gauntlet_pass_rate(kit) - cohort_midpoint(cohort)| <= 0.25`** — kit's PASS rate is within ±25% of its cohort's empirical midpoint. This is the BAND-FIT constraint: kits that pass too high (>cohort_midpoint+0.25) are degenerate-OP outliers; kits that pass too low (<cohort_midpoint-0.25) are degenerate-weak outliers.

### 1.3 Cohort partition (operational definition from 8 locked BC axes)

Per Matt 2026-05-27 pre-ratification, kits partition into 5 cohorts. No prior canonical doc defined this partition. This spec operationalizes it from the 8 locked BC axes per `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (substrate-led; no new pre-authored taxonomy per Discipline #41).

**Cohort classifier (deterministic; per kit at Phase 7 time):**

| Cohort | BC-axis predicate (priority order; first match wins) |
|---|---|
| **Support** | `engagement_profile = support` OR `resource_economy = team-resource-feeder` (multi-actor primary; per role-orientation taxonomy 2026-05-08 ratification: support is multi-actor-context-gated) |
| **Control** | `control_density = control-pure` OR (`control_density = mixed` AND damage axes show non-primary signature) |
| **Defensive** | `defensive_profile ∈ {tank, mitigator}` AND damage axes show non-primary signature |
| **Damage** | `control_density = damage-pure` AND `defensive_profile ∈ {dodger, glass}` (pure DPS focus) |
| **Hybrid** | Any kit not matching the above 4 (cross-axis cell capture per BC axes lock § 4 hybrid archetypes; absorber / regenerator / thorns / reflection / self-harmer / charm / damage-taken-converts / charge-stack / charge-up-release) |

**Cohort-assignment is single-valued per kit.** Priority order: Support → Control → Defensive → Damage → Hybrid (else). This ensures determinism and prevents double-counting. Hybrid is the residual catch-all (per BC axes lock § 4 architecture).

**Why this partition (substrate-led derivation):**
- Each predicate references LOCKED BC axes (no invented axes; no pre-authored substrate categories).
- Predicate priority handles the multi-cohort-eligibility case deterministically.
- Hybrid catches the cross-axis cells that BC axes lock § 4 already named operationally.

**Discipline #45 compliance:** No "class" / "role" / "archetype" non-exempt vocabulary. Cohort labels are 5 substrate-grouping terms; they are acceptable BC-axis groupings, not pre-authored taxonomies (Discipline #41 distinction: cohort = post-hoc aggregation of locked BC axes; class = pre-authored player-facing identity).

**Discipline #36 compliance (substrate-as-keying-source):** Cohort classifier keys on substrate dimensions (BC axes), not on substrate-anchored personage identity.

### 1.4 Gauntlet PASS rate semantics

**Definition:** `gauntlet_pass_rate(kit) = (# encounters won) / (# encounters total)` over the standard gauntlet suite simulation at Phase 4 sim time.

**Encounter inclusion:** all encounter scenarios that ran during the Phase 4 mechanical gauntlet for this kit. The gauntlet suite is defined by gamora Dispatch 3A (Phase 4 sim execution); Phase 7 consumes the result, does not re-sim.

**Source:** Phase 4 sim emits per-kit `gauntlet_pass_rate` as part of the kit's `q1` (win_rate_normalized) computation OR as a sibling column. The Seam 2 jack-ryan canonical-write at engine math/ MUST specify which column carries this exactly; if it does not currently exist as a distinct column, Seam 2 specifies the math-note addition (q1 normalization preserves pass-rate semantics; otherwise add `gauntlet_pass_rate` column to kit_archive).

**Q1-to-pass-rate mapping note:** `q1 = win_rate_normalized` per phase4_db.py line 45. "Normalized" suggests post-cohort-normalization. If `q1` is already cohort-normalized, the cohort_midpoint check is redundant (q1 is centered on midpoint by construction). Seam 2 must DISAMBIGUATE: either (a) Phase 7 consumes raw PASS rate + does its own cohort centering; or (b) Phase 7 consumes q1 with a `q1 ∈ [-1, 1]` interpretation centered on cohort midpoint and tests `|q1| <= 0.25` + raw pass rate > 0.70 separately. Recommendation: option (a) — Phase 7 reads raw `gauntlet_pass_rate` + classifies cohort + does its own midpoint check; q1 remains the Phase 4 internal normalization for Pareto math.

### 1.5 Cohort midpoint empirical calibration procedure (Q-P7-1 resolution)

**Dispatch open question Q-P7-1:** "Cohort midpoint calibration data source — Phase 4 production season required OR historical telemetry (D11+D12) sufficient?"

**Recommendation:** **HYBRID — historical telemetry as initial prior; Phase 4 first-production-season as authoritative re-calibration.**

| Stage | Data source | Cohort midpoint value |
|---|---|---|
| **Initial (pre-Wave-5)** | Historical telemetry (D11 + D12 era; ~15 seasons; per `project_b14_5_sidecar_analyses` MEMORY findings) | Per-cohort historical PASS rate median across the ~15 historical seasons; cohort-classified per § 1.3 retroactively |
| **Authoritative (post-first-Wave-5-production-season)** | First Wave 5 `cycle-14-wave-5-season-001` Phase 4 gauntlet output | Per-cohort PASS rate median over the 35-form production season; replaces the initial prior |
| **Re-calibration (per-season after the first)** | STATIC at Cycle 14 v1 — midpoints DO NOT auto-adjust per season within Cycle 14 |

**Rationale:**
- Historical telemetry exists and is cohort-classifiable retroactively (B14.5 sidecar analyses MEMORY note: hunter archetype has 1.82 modifier range; rogue/hunter low convergence iterations; per-archetype telemetry already supports cohort statistics).
- Phase 4 first-production-season provides authoritative under-Phase-4-math-gates data (D11+D12 era pre-dates Phase 4 mechanical archive math gates per `749d5aa`).
- STATIC mutability at Cycle 14 v1 means midpoints calibrate ONCE post first production season and remain locked for the cycle.

**Operational definition (Seam 2 canonical-write):**

```python
# Initial prior (pre-Wave-5):
cohort_midpoint_initial = {
    "damage":    historical_telemetry_pass_rate_median(cohort="damage", seasons=D11+D12),
    "defensive": historical_telemetry_pass_rate_median(cohort="defensive", seasons=D11+D12),
    "control":   historical_telemetry_pass_rate_median(cohort="control", seasons=D11+D12),
    "support":   historical_telemetry_pass_rate_median(cohort="support", seasons=D11+D12),
    "hybrid":    historical_telemetry_pass_rate_median(cohort="hybrid", seasons=D11+D12),
}

# Authoritative re-calibration (post first Wave 5 production season):
cohort_midpoint_v1 = {
    cohort: pass_rate_median(kits_in_cohort_in_season("cycle-14-wave-5-season-001"))
    for cohort in COHORTS
}
```

**Empirical-trigger cleanup case:** if historical telemetry returns <5 kits in any cohort (insufficient sample), that cohort's initial prior defaults to **0.85** (the mid-band PASS rate empirically observed across legacy seasons; PASS rate ranges 0.7-1.0; midpoint of valid band). Support cohort is most likely to hit this case (multi-actor context rare in historical solo-arena telemetry).

**Discipline #18 hot-spot annotation:** Cohort midpoint calibration IS a math-hotspot per Discipline #18 — methodology choice (median vs mean vs trimmed-mean vs robust estimator) is non-trivial AND execution failure is silent (a wrong midpoint produces wrong cohort-membership decisions downstream). Seam 2 canonical-write at engine math/ folder MUST specify methodology explicitly. Recommendation: **median** (robust to outliers; existing legacy telemetry has hunter 1.82 modifier-range outliers per MEMORY).

### 1.6 ±25% band semantics

**Operational:** for cohort with midpoint `m`, kit with `gauntlet_pass_rate = p` passes the band check iff `|p - m| ≤ 0.25`.

**Worked example:** if Damage cohort midpoint `m = 0.85`, the acceptable band is `[0.60, 1.10]` raw; clipped to `[max(0.70, 0.60), min(1.0, 1.10)]` = `[0.70, 1.0]` because the >70% floor also applies. Effective acceptance band for Damage cohort: `gauntlet_pass_rate ∈ [0.70, 1.0]`.

**Worked example with lower midpoint:** if Support cohort midpoint `m = 0.75` (multi-actor-context PASS rate empirically lower), acceptable band is `[0.50, 1.0]`; intersected with >70% floor = `[0.70, 1.0]`. Same effective band.

**Insight:** the >70% floor is a HARD constraint that subsumes the band's lower bound in most cohorts. The band's UPPER bound (`m + 0.25`) is the band-fit constraint that catches degenerate-OP outliers — a kit that wins 100% of encounters while its cohort averages 75% is a likely cell-mismatch or balance bug, not a legitimately strong build.

**Discipline #43 audit hook:** at Wave 5 close, gandalf design-quality audit A4 inspects whether band-rejection cases are concentrated in any cohort (signal: cohort midpoint mis-calibrated OR cohort classifier mis-partitioning).

---

## 2. Cohesion pass spec

### 2.1 Inputs at Phase 7 cohesion-evaluation time

**Per-kit (skill-node level):** Phase 5 calibration spec § 3.6 emits `cohesion_score ∈ [0, 1]` per skill node, weighted aggregate of 5 sub-rubrics. **Kit-level cohesion** is the mean cohesion_score across all skill nodes in the kit's tree, plus form-level cohesion penalties.

**Per-cluster (faction level):** ExportFactionCluster fields per `bf7f659/src/reincarnated/export/schemas.py`:
- `cluster_compactness: float | None` — PM-1 silhouette score (0.0-1.0)
- `phase7_gate_status: str` — `"canonical"` or `"placeholder"`
- `diversity_flag: bool | None` — True if cross-faction `cosine_similarity_max > 0.85`
- `cosine_similarity_max: float | None`
- `regeneration_fired: bool | None`

**Forward-compat with Wave 3 F-C addition:** the Wave 3 dispatch (`2026-05-27-wave-3-phase-5-cohesion-judge-llm-with-f-c.md`) adds `ai_tell_compliance_score` to ExportFactionRelationship (NOT ExportFactionCluster). If/when that field lands, Phase 7 cohesion pass adds a per-relationship check (§ 2.5).

### 2.2 Cohesion pass criterion (formal)

```
cohesion_pass(kit) := 
    (kit_level_cohesion_score(kit) >= 0.75)
    AND (cluster_compactness(kit.cluster) >= 0.40)
    AND (diversity_flag(kit.cluster) != True)
    AND (phase7_gate_status(kit.cluster) IN {"canonical", "placeholder"})
```

Four conjunctive conditions:

- **`kit_level_cohesion_score(kit) >= 0.75`** — the kit's mean per-node `cohesion_score` (per Phase 5 calibration spec § 3.6) meets the per-kit aggregate threshold. This is the per-kit naming/identity coherence.
- **`cluster_compactness(kit.cluster) >= 0.40`** — the kit's cluster (faction) silhouette score >= 0.40, indicating the cluster is meaningfully separable from other clusters. Threshold sourced from PM-1 math note silhouette interpretation: 0.40 is "reasonable structure"; below 0.40 indicates ambiguous cluster boundary.
- **`diversity_flag != True`** — the kit's cluster's canonical label does not collide with another cluster's label (cross-faction `cosine_similarity_max <= 0.85`). If diversity_flag is True, Phase 5 regeneration_fired SHOULD have already fired; if diversity_flag still True at Phase 7 time, cluster-naming failed.
- **`phase7_gate_status ∈ {"canonical", "placeholder"}`** — the cluster's LLM-layer status is valid. Star-lord PM-2 consultation explicitly requires Phase 7 to accept BOTH states (schemas.py line 643). Reincarnated v1 default is `"placeholder"` (faction_visibility = invisible); the cohesion-judge layer short-circuited for player-invisible factions.

### 2.3 Threshold relationship to Matt pre-ratification

Matt pre-ratification states: `ai_tell_compliance_score ≥0.7 + cohesion-judge confidence ≥0.65`.

**Mapping to actual substrate fields:**

| Matt pre-ratification term | Actual substrate field | This spec's threshold |
|---|---|---|
| `cohesion-judge confidence ≥ 0.65` | `kit_level_cohesion_score` (Phase 5 calibration spec § 3.6) | `>= 0.75` per Phase 5 spec; STRICTER than 0.65 ratification floor |
| `ai_tell_compliance_score ≥ 0.7` | Wave 3 F-C field (not yet landed); placeholder via `phase7_gate_status` accept | Forward-compat slot in § 2.5 |

**Discipline-driven decision:** retain the **stricter** Phase 5 calibration spec threshold (`>= 0.75`) instead of the Matt-ratification floor (`>= 0.65`). Rationale per Discipline #43 (design-quality audit) + Discipline #41 (no scaffold values without canonical decision): Phase 5 spec is the more recently authored canonical reference for cohesion-judge output; Matt-ratification 0.65 was a coarse-grained input prior to the per-node sub-rubric architecture being authored. The stricter threshold honors Phase 5 calibration spec acceptance criterion.

**Audit:** at Phase 7 first-Wave-5-production-season close, gandalf design-quality audit A1 verifies the 0.75 threshold produces NON-ZERO acceptance (does not starve all kits) AND NON-SATURATED acceptance (does not pass all kits). If starvation/saturation observed, recalibration trigger fires per § 5.

### 2.4 Cohesion-fail mode analysis

A kit may fail cohesion for any of four distinct reasons. Phase 7 logging MUST disambiguate (per Discipline #43 audit input requirement):

| Cohesion-fail mode | Disambiguation field | Re-entry behavior |
|---|---|---|
| **C-1 per-kit cohesion below floor** | `kit_level_cohesion_score < 0.75` | Return to Phase 5 with new prompt seed; re-name skill nodes |
| **C-2 cluster compactness below floor** | `cluster_compactness < 0.40` | Cluster-level fail; ALL kits in cluster fail simultaneously; signal to Wave 5 audit-gate that cluster is genuinely incoherent → cluster-level remediation OR discard cluster's kits |
| **C-3 cross-faction diversity collision** | `diversity_flag = True` at Phase 7 (post-regeneration) | Cluster-level fail; signal Phase 5 cluster-naming failed AFTER regeneration attempt; discard cluster's kits |
| **C-4 placeholder + canonical-required policy** | `phase7_gate_status = "placeholder"` AND profile flag requires canonical | Currently UNREACHABLE — Reincarnated v1 profile flag `faction_visibility = invisible` accepts placeholder; reserved for Cycle 15+ profiles |

**Critical disambiguation:** modes C-2 and C-3 are CLUSTER-level fails. They fail an entire cluster's worth of kits at once (typically 3-5 kits per cluster per faction-target). Mode C-1 is PER-KIT. Return-to-Phase-5 semantics differ: C-1 retries one kit's naming; C-2/C-3 retries the cluster-naming layer (or discards the cluster entirely).

**Wave 5 audit-gate composition (Position B):** when Phase 7 emits HELD-cohesion-fail at C-2 or C-3 magnitude (≥1 cluster failed), the kit-level retry path may be insufficient — cluster-level remediation may require regenerating the entire Phase 5 clustering. This composes with the Position B audit-gate at Wave 5 (`cycle-14-wave-5-season-002` etc.); see § 7.

### 2.5 Forward-compat with Wave 3 F-C addition

When the Wave 3 dispatch lands `ai_tell_compliance_score` on ExportFactionRelationship (per F-C per-pair LLM call), Phase 7 cohesion pass criterion extends to:

```
cohesion_pass_v1.1(kit) := 
    cohesion_pass(kit)  # § 2.2
    AND (∀ relationship r involving kit's cluster: r.ai_tell_compliance_score >= 0.70)
```

The 0.70 threshold maps directly to Matt pre-ratification's `ai_tell_compliance_score ≥0.7`. This is the appropriate threshold for the F-C self-assessment score (per Wave 3 dispatch + path-iii-faction-assembly-extension § 6).

**Cycle 14 v1 status:** the F-C relationship layer is `faction_visibility = invisible` for Reincarnated v1, so F-C is short-circuited. Forward-compat slot reserved; not currently consumed.

---

## 3. HELD verdict state machine

### 3.1 Verdict enum

```python
@dataclass
class Phase7Verdict:
    kit_id: str
    season_id: str
    verdict: str  # one of:
                  #   "SHIPPED-WORTHY"
                  #   "HELD-cohesion-fail-C1"  (per-kit cohesion below 0.75)
                  #   "HELD-cohesion-fail-C2"  (cluster compactness below 0.40)
                  #   "HELD-cohesion-fail-C3"  (cross-faction diversity collision)
                  #   "HELD-mechanical-fail-archive"  (archive_status != ACTIVE)
                  #   "HELD-mechanical-fail-floor"    (gauntlet_pass_rate <= 0.70)
                  #   "HELD-mechanical-fail-band"     (|pass_rate - cohort_midpoint| > 0.25)
                  #   "HELD-both-fail"                (mech and cohesion both fail)
    mechanical_pass: bool
    cohesion_pass: bool
    retry_attempt: int  # 0 = first eval; 1+ = retry from Phase 5 with new seed
    disposition: str  # "ship" | "retry-phase-5" | "discard"
    reason_detail: dict  # see § 4 logging schema
```

### 3.2 State transitions (per kit lifecycle through Phase 7)

```
Kit enters Phase 7 (retry_attempt = 0)
  │
  ├── mechanical_pass AND cohesion_pass
  │     → verdict = SHIPPED-WORTHY
  │     → disposition = "ship"
  │     → emit to Wave 5 export consumer
  │
  ├── NOT mechanical_pass (regardless of cohesion)
  │     → verdict = HELD-mechanical-fail-{archive|floor|band}
  │       OR HELD-both-fail if cohesion also fails
  │     → disposition = "discard"
  │     → log to design-quality audit per Discipline #43
  │     → NO retry (Phase 4 already rejected via reject_pool architecture)
  │
  └── mechanical_pass AND NOT cohesion_pass
        → verdict = HELD-cohesion-fail-{C1|C2|C3}
        ├── C1 (per-kit): retry_attempt < 2
        │     → disposition = "retry-phase-5" 
        │     → kit returns to Phase 5 with new prompt seed
        │     → retry_attempt += 1
        │     → re-enter Phase 7 cohesion check (mechanical already pass; cached)
        ├── C1 (per-kit): retry_attempt >= 2
        │     → disposition = "discard"
        │     → log "max-retry-exceeded" to design-quality audit
        ├── C2 / C3 (cluster-level): retry_attempt < 1
        │     → disposition = "retry-phase-5-cluster"
        │     → ENTIRE CLUSTER returns to Phase 5 PM-2 faction-label assignment
        │     → cluster regeneration_fired = True
        │     → all kits in cluster re-eval Phase 7
        │     → retry_attempt += 1 (kit-level counter; cluster-level retry counted once per kit)
        └── C2 / C3 (cluster-level): retry_attempt >= 1
              → disposition = "discard"
              → entire cluster's kits discarded
              → log "cluster-irremediable" to design-quality audit
              → signal to Wave 5 audit-gate (Discipline #43) — likely cluster-cardinality mis-calibration
```

### 3.3 Retry cap rationale (Q-P7-2 resolution)

**Dispatch open question Q-P7-2:** "Return-to-phase max retry count? If unbounded, what prevents infinite loop semantically? Recommend 2-retry cap with discard-on-3rd-fail."

**Recommendation: 2 retries per kit at C-1; 1 retry per cluster at C-2/C-3.**

| Failure mode | Retry cap | Total attempts | Rationale |
|---|---|---|---|
| C-1 per-kit | 2 retries | 3 attempts (initial + 2 retry) | Per-kit LLM cost ~$0.005-$0.05 per re-name; 3 attempts is bounded; Phase 5 calibration spec § 3.6 already uses 3-attempt re-roll for per-node naming (consistent) |
| C-2 / C-3 cluster | 1 retry | 2 attempts (initial + 1 retry) | Cluster regeneration is expensive (re-fires PM-2 LLM for entire cluster); 1 retry is bounded; if cluster genuinely irremediable, signal-to-design is more valuable than further retry |

**Why bounded retries:**
- **No-infinite-loop discipline** — unbounded retry creates degeneracy where LLM stochasticity can mask genuine cohesion failures by eventually producing a passing seed.
- **Empirical-evidence-gated** — Position B audit-gate at Wave 5 (`cycle-14-wave-5-season-002` etc.) catches systemic cohesion failures across kits as a separate signal; per-kit infinite retry would hide that signal.
- **Discipline #43 audit input** — bounded retries with logged disposition give clean signal-to-design at wave-close.

**Cluster-level fail is more severe than per-kit fail:** C-2/C-3 indicate PM-1 clustering or PM-2 naming produced incoherent factions. The 1-retry cap forces escalation to the audit layer rather than papering over the issue.

### 3.4 No silent re-roll loops (per Matt pre-ratification)

Matt pre-ratification: "NO silent re-roll loops; logged for design-quality audit per Discipline #43".

**Operational enforcement:**
- Every retry event MUST emit a Phase7RetryRecord (§ 4) to the design-quality audit log.
- Retry counts are visible to the Wave 5 audit-gate (jack-ryan Gate-2 + gandalf design-quality audit).
- Aggregate retry rate per cohort + per cluster is a key wave-close metric.
- Discipline #43 audit A1: "Did this wave advance the named quality criterion?" — high retry rates indicate cohesion-judge calibration drift or substrate-cohesion-mismatch; both are quality-criterion regressions.

---

## 4. Design-quality audit hooks (Discipline #43 composition)

Phase 7 emits to the design-quality audit log per kit + per cluster + per season. The audit consumes these records at Wave 5 close + at Phase 7 design-tuning review.

### 4.1 Per-kit log record

```python
@dataclass
class Phase7KitVerdictLog:
    # Identity
    kit_id: str
    season_id: str
    cluster_id: int
    
    # Cohort classification
    cohort: str  # "damage" | "defensive" | "control" | "support" | "hybrid"
    cohort_classifier_predicates_matched: list[str]  # for audit traceability
    
    # Mechanical layer
    archive_status: str  # "ACTIVE" | "DOMINATED" | "EVICTED"
    gauntlet_pass_rate: float
    cohort_midpoint_applied: float
    band_distance_from_midpoint: float  # signed delta
    mechanical_pass: bool
    
    # Cohesion layer
    kit_level_cohesion_score: float
    cluster_compactness: float | None
    diversity_flag: bool | None
    phase7_gate_status: str  # "canonical" | "placeholder"
    cohesion_pass: bool
    
    # Verdict
    verdict: str  # § 3.1 enum
    disposition: str  # "ship" | "retry-phase-5" | "retry-phase-5-cluster" | "discard"
    retry_attempt: int
    
    # Provenance
    phase4_completion_timestamp: str
    phase5_completion_timestamp: str
    phase7_evaluation_timestamp: str
    
    # Forward-compat (Wave 3 F-C addition)
    ai_tell_compliance_scores: list[float] | None  # null for Cycle 14 v1 (faction_visibility=invisible)
```

### 4.2 Per-cluster aggregate log record

```python
@dataclass
class Phase7ClusterAggregateLog:
    cluster_id: int
    season_id: str
    
    # Cluster-level mechanical aggregate
    member_kit_count: int
    pass_rate_distribution: dict[str, float]  # {"min": ..., "median": ..., "max": ...}
    cohort_membership_distribution: dict[str, int]  # {cohort: count}
    
    # Cluster-level cohesion
    cluster_compactness: float
    diversity_flag: bool
    phase7_gate_status: str
    regeneration_fired: bool
    
    # Verdict aggregates
    shipped_worthy_count: int
    held_cohesion_fail_count: int
    held_mechanical_fail_count: int
    retry_attempts_total: int
    
    # Drift signals (for Wave 5 audit-gate)
    cohort_concentration: dict[str, float]  # fraction per cohort
    midpoint_drift_signal: dict[str, float]  # per-cohort mean band_distance
```

### 4.3 Audit consumption protocol

At Wave 5 close, gandalf design-quality audit (Discipline #43) consumes Phase7KitVerdictLog + Phase7ClusterAggregateLog and answers:

| Question | Signal | Trigger |
|---|---|---|
| **A1: Did Phase 7 advance the named quality criterion?** | Mechanical PASS rate per cohort within target ±25% band; cohesion PASS rate non-saturated and non-starved | Fire if PASS rate <40% OR >95% across kits |
| **A2: Pre-authored taxonomy?** | Cohort classifier produced single-cohort dominant assignment (>80% kits in one cohort)? | Fire if dominant cohort >80% — substrate-led discipline implies cohort distribution should reflect substrate variety |
| **A3: Scaffold values?** | Cohort midpoints calibrated empirically from named-source (historical telemetry OR Wave 5 season-001) OR scaffold-default 0.85 used? | Fire if any cohort's midpoint was the 0.85 scaffold-default — indicates historical telemetry insufficient AND first-production-season not yet calibrated |
| **A4: Substrate-led composition?** | Did cohort classifier reference ONLY locked BC axes? | Fire if classifier added non-canonical predicate (drift detection) |
| **A5: Canonical anchors preserved?** | Phase 5 calibration spec threshold 0.75 honored; Phase 4 archive_status ACTIVE honored; ExportFactionCluster phase7_gate_status accepted | Fire if any threshold silently relaxed |

**Audit verdict outputs (per Discipline #43):**
- PASS — all A1-A5 affirmative
- PASS-with-design-concerns — A1-A5 affirmative but minor design observations
- DRIFT-DETECTED — any A1-A5 returns negative; escalate to Matt Pattern B

---

## 5. Mutability lock semantics

### 5.1 STATIC at Cycle 14 v1

Per Matt pre-ratification: "Mutability: STATIC at Cycle 14 v1; Cycle 15+ may auto-tune from production-season evidence."

**Operationally:**

| Parameter | Cycle 14 v1 value | Mutation rule |
|---|---|---|
| Gauntlet PASS floor | 0.70 | STATIC (no mutation within cycle) |
| Cohort midpoint ±band | ±0.25 | STATIC |
| Cohort midpoints | initial prior → first-Wave-5-season re-calibration → STATIC | One-time calibration; locked post-Wave-5-season-001 |
| Per-kit cohesion threshold | 0.75 | STATIC (Phase 5 calibration spec authority) |
| Cluster compactness threshold | 0.40 | STATIC |
| Diversity flag threshold | cosine_similarity_max > 0.85 (PM-2 default) | STATIC |
| Per-kit retry cap (C-1) | 2 retries | STATIC |
| Cluster retry cap (C-2/C-3) | 1 retry | STATIC |

**No silent threshold relaxation:** Discipline #43 audit fires if any threshold is silently relaxed during Cycle 14 (e.g., a Wave 5 retry attempt that bypasses cohesion floor by lowering 0.75 to 0.70 to force pass). Such relaxation requires Matt-gate Pattern B engagement.

### 5.2 Cycle 15+ auto-tune trigger criteria

Cycle 15+ MAY auto-tune from production-season evidence. Auto-tune trigger criteria:

| Trigger | Evidence required | Auto-tune scope |
|---|---|---|
| **T-1 Cohort midpoint drift** | ≥3 production seasons show cohort midpoint trending outside `[initial - 0.10, initial + 0.10]` | Recalibrate cohort midpoints from rolling-3-season median |
| **T-2 PASS rate saturation** | ≥2 seasons in a row show >95% PASS rate across all cohorts | Tighten band from ±0.25 to ±0.20; OR raise floor from 0.70 to 0.75 |
| **T-3 PASS rate starvation** | ≥2 seasons in a row show <40% PASS rate across all cohorts | Loosen band from ±0.25 to ±0.30; OR investigate Phase 4 archive ACCEPTANCE drift |
| **T-4 Cohesion threshold drift** | ≥3 seasons show cohesion_score distribution shifting (e.g., median below 0.70 OR above 0.90) | Recalibrate per Phase 5 calibration spec § 4 sweep |
| **T-5 Retry rate saturation** | ≥1 season shows aggregate retry rate >25% | Investigate cohesion-judge calibration drift; possibly re-fire Phase 5 calibration sweep |

**Auto-tune mechanism (Cycle 15+ design space):** auto-tune is NOT silent threshold mutation. It is a structured re-ratification cycle:
1. Trigger fires → gandalf design-quality audit produces drift report
2. Drift report routed to Matt Pattern B
3. Matt ratifies new thresholds OR retains existing
4. New thresholds STATIC for next cycle

**Anchored example (T-1 cohort midpoint drift):** if Damage cohort midpoint at Cycle 14 lock is 0.85 and across seasons 2/3/4 the median drifts to 0.75, T-1 fires; auto-tune recommends new lock at 0.75; Matt ratifies; Cycle 15 lock = 0.75. The 25% band stays ±0.25; only the midpoint moves.

---

## 6. D-Sharpened composition (Phase 7 evaluates ALL kits uniformly)

Per dispatch acceptance: "D-Sharpened composition (Phase 7 evaluates ALL kits uniformly regardless of substrate-anchored vs synthesized)".

**Operational:**

Phase 7 does NOT inspect `substrate_anchored_personage` (ExportFactionCluster D-Sharp-3 analytics-only field). Kit verdict criteria reference ONLY:
- mechanical layer: archive_status + gauntlet_pass_rate + cohort_midpoint
- cohesion layer: kit_level_cohesion_score + cluster_compactness + diversity_flag + phase7_gate_status

**Why this matters:** the ~32% of kits that carry a Sketch F named-personage substrate anchor (per PM-2 § 2.7) and the ~68% engine-named-original kits go through the IDENTICAL Phase 7 gate. There is no anchor-preferential path. A Moctezuma-anchored Damage-cohort kit and an engine-named-original Damage-cohort kit face the same 0.70 PASS floor + ±0.25 cohort midpoint band + 0.75 cohesion floor.

**Discipline #41 compliance:** no pre-authored named-personage taxonomy gates kit acceptance. Substrate-led: a kit's verdict depends on its BC-axis cohort classification + its actual gauntlet PASS rate + its actual cohesion_score, not on whether the engine-internal anchor happens to be a named historical figure.

**Discipline #36 compliance (substrate-as-keying-source):** Phase 7 keys on substrate dimensions (BC axes + locked Phase 5 cohesion fields), not on substrate-anchored personage identity.

**Discipline #45 compliance:** no "class" / "role" / "archetype" vocabulary in Phase 7 logic. Cohort labels are BC-axis groupings (substrate-emergent), not pre-authored player-facing taxonomy.

---

## 7. Position B Wave 5 amendment composition (Q-P7-3 resolution)

### 7.1 Position B context

Per `agentic_orchestration/dispatches/2026-05-27-wave-5-production-season-dispatch.md` (Position B amendment): Wave 5 fires single iterative generation `cycle-14-wave-5-season-001`; if audit-gate FAILS, re-generate as `cycle-14-wave-5-season-002`; up to 3 attempts; escalate Pattern B Matt at 3rd fail.

The audit-gate at Wave 5 is **jack-ryan Gate-2 + gandalf Discipline #43 design-quality audit** — DISTINCT from Phase 7 verdict.

### 7.2 Phase 7 verdict feeds INTO audit-gate (not the other way around)

**Correct mental model:**

```
Phase 2 → Phase 4 → Phase 5 → Phase 7 (per-kit verdict)
                                  │
                                  ↓ (aggregate emission)
                  Phase7ClusterAggregateLog + Phase7KitVerdictLog per season
                                  │
                                  ↓
              Wave 5 audit-gate (jack-ryan Gate-2 + gandalf #43)
                                  │
                  ┌───────────────┴───────────────┐
                  ↓                               ↓
            audit-gate PASS                 audit-gate FAIL
            → commit as canonical            → recalibrate parameters
              (cycle-14-production-           regenerate as 
              season-001)                      cycle-14-wave-5-season-002
```

**Phase 7 verdict is per-KIT.** Wave 5 audit-gate is per-SEASON.

### 7.3 Iterative audit-gate model semantic correctness

**Q-P7-3 resolution:** Phase 7 verdict semantics work cleanly in Position B iterative audit-gate model BECAUSE:

1. **Phase 7 verdicts are deterministic per kit** (given fixed inputs: archive_status, gauntlet_pass_rate, cohesion scores). Re-running Phase 7 on a re-generated season produces fresh verdicts; no state carries forward inappropriately.

2. **Retry counters are per-attempt scoped.** A `cycle-14-wave-5-season-002` regeneration starts retry_attempt = 0 for all kits; previous retries from season-001 do not accumulate.

3. **Cohort midpoint calibration anchor.** Once cohort midpoints are calibrated from season-001 (per § 1.5), seasons 002/003 USE THE SAME MIDPOINTS (STATIC lock per § 5.1). This prevents the audit-gate from being gamed by per-season midpoint drift.

4. **HELD verdicts compose with audit-gate signal:**
   - High HELD-mechanical-fail rate at season-001 → audit-gate signal: Phase 4 calibration drift OR cohort midpoint mis-calibration → recalibrate at season-002 entry
   - High HELD-cohesion-fail rate at season-001 → audit-gate signal: Phase 5 prompt calibration OR substrate-cohesion-mismatch → recalibrate prompts at season-002 entry
   - High retry rate at season-001 → audit-gate signal: cohesion-judge stability issue → re-fire Phase 5 calibration sweep at season-002 entry

5. **Audit-gate's "audit feedback informs recalibration" path uses Phase 7 aggregate logs directly.** The Phase7ClusterAggregateLog `midpoint_drift_signal` + `cohort_concentration` fields are the precise signals Wave 5 audit-gate consumes for recalibration recommendations.

### 7.4 Three-attempt-max bound

Per Position B: max 3 attempts (season-001 / -002 / -003); escalate Pattern B Matt on 3rd fail. Phase 7 verdict spec composes by emitting per-attempt aggregate logs; audit-gate sees attempt-N improvement (or lack thereof) and makes the escalation call.

**Phase 7 perspective:** Phase 7 is stateless across attempts. Each attempt receives a fresh kit population + cluster assignment from upstream Phase 2-5 regeneration; Phase 7 emits verdicts; audit-gate consumes.

---

## 8. Risks + Watch Items (per failure-modes register § 5)

This spec must guard against the following patterns (per `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md`):

### F-5 Joint-gate threshold drift (PRIMARY)

**Pattern:** Phase 7 2-layer joint-gate thresholds set too high → no kits pass → empty season. Set too low → no filtering → defeats purpose.

**Watch:**
- First Wave 5 production season measures per-cohort PASS rate; if any cohort shows 0% or 100% PASS, thresholds need calibration.
- Target 60-90% acceptance per cohort post-Phase-4-ACCEPT (cohesion is a stricter secondary filter; ~70-80% of mech-PASS kits should also cohesion-PASS).
- Per-cluster compactness threshold 0.40 should accept ~70% of PM-1 clusters (silhouette scores in 0.40-0.70 range expected per cluster math).

**Counter:**
- This spec includes empirical recalibration procedure (§ 1.5) keyed to first-Wave-5-season data.
- Discipline #11 inspection over assumption: § 4.3 audit hooks fire if PASS rate or cohesion rate hit saturation/starvation extremes.
- Matt-ratification preserved at threshold-locking time (§ 5.2 Cycle 15+ auto-tune requires Matt re-ratification).

### F-1 Math methodology drift

**Pattern:** Cohort midpoint calibration uses wrong statistical estimator (e.g., mean instead of median; vulnerability to outlier seasons).

**Watch:**
- Seam 2 jack-ryan canonical-write at engine math/ folder MUST specify median (not mean) for cohort midpoint per § 1.5 recommendation; Gate-1 reviews verify.
- If hunter-modifier-range 1.82 outliers (per MEMORY B14.5 sidecar) skew the estimator, median is robust; mean would be sensitive.

**Counter:**
- Discipline #18 math-hotspot routing — cohort midpoint calibration is a math-hotspot (multiple estimator choices; failure is silent). Seam 2 canonical-write at engine math/ MUST lock methodology.
- Audit A3 fires if methodology not explicitly named in canonical-write.

### F-7 Phase 6 implicit creep (DEFERRAL ENFORCED)

**Pattern:** Sub-agents authoring Phase 7 2-layer spec might want to add visual layer "while we're at it."

**Counter:** This spec is EXPLICITLY 2-layer (mechanical + cohesion) only. Visual layer (Phase 6) deferred to Cycle 15+ per `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 5.6 amendment. Phase 7 spec does NOT include visual gate evaluation. Cycle 15+ 3-layer extension is a separate dispatch.

### D-5 Joint-gate becoming theological (PRIMARY DESIGN-DRIFT WATCH)

**Pattern:** "all kits must pass mechanical AND cohesion AND visual" sounds clean but failure handling is unclear — if cohesion gate fails an otherwise-good kit, what happens? Re-roll? Edit? Discard?

**Counter (this spec):**
- § 3 HELD verdict state machine fully specifies disposition per HELD reason (retry / discard with bounded retry caps).
- § 4 design-quality audit hooks emit logs at every HELD verdict for design-quality review.
- NO silent re-roll loops per Matt pre-ratification + § 3.4 enforcement.

### S-4 Visual style register validation creep (DEFERRED)

**Counter (this spec):** Phase 7 cohesion layer evaluates Phase 5 cohesion-judge output ONLY (per § 2). Visual style register validation is Phase 6 territory, deferred Cycle 15+. § 2.2 cohesion criterion does NOT reference visual fields.

---

## 9. What this spec does NOT decide

- **Specific cohort midpoint NUMERIC values** — to be calibrated empirically from historical telemetry + first Wave 5 season (per § 1.5). Seam 2 jack-ryan canonical-write specifies the calibration procedure; first Wave 5 season produces the lock values.
- **Phase 4 sim mechanics** — gamora Dispatch 3A territory (`749d5aa`); Phase 7 consumes Phase 4 output.
- **Phase 5 per-node cohesion sub-rubric** — Phase 5 calibration spec § 3.6 territory; Phase 7 consumes the aggregate score.
- **Phase 6 visual layer** — deferred Cycle 15+ per doc 39 § 5.6 amendment.
- **Phase 8 export pipeline** — star-lord Track C / rocket export territory; Phase 7 verdict feeds into export selection but does not author the export logic.
- **Position B Wave 5 audit-gate execution semantics** — Wave 5 dispatch + jack-ryan Gate-2 + gandalf #43 audit territory; Phase 7 emits aggregate logs for audit-gate consumption (§ 7).
- **Cluster-level cardinality (target 3-5 factions per season)** — PM-1 math note territory.
- **Auto-tune execution at Cycle 15+** — Cycle 15+ dispatch design space; this spec specifies trigger criteria only (§ 5.2).
- **Cohesion-judge LLM model choice** — Phase 5 calibration spec § 2.4 territory; Phase 7 consumes the score.

---

## 10. Sign-off

**Author:** gandalf (story-and-design steward) 2026-05-27 Pattern-B dispatch execution (Seam 1 of 2)
**Status:** CURRENT — Seam 1 composition spec landed; awaiting Seam 2 jack-ryan Discipline #18 canonical-write at engine math/ folder
**Downstream consumers:**
- jack-ryan (Seam 2 Discipline #18 canonical-write; ~2-3 days; canonicalizes thresholds at engine math/ folder per Q-P7-3)
- gamora (Phase 7 impl consumer; separate dispatch at Wave 4/5 boundary)
- star-lord (telemetry consumer; Phase7KitVerdictLog + Phase7ClusterAggregateLog emission)
- Wave 5 audit-gate (jack-ryan Gate-2 + gandalf Discipline #43 design-quality audit)

**Framing-audit fields per Discipline #42:**
- Framing-audit fired: yes (§ 0.1)
- Q1 load-bearing assumptions: 7 identified
- Q2 refutation evidence: 4 surfaced (all resolved within spec scope; primary catch: parent dispatch cites ExportFactionCluster fields that don't exist; resolved by mapping to actual `bf7f659` field surface + Phase 5 calibration spec § 3.6 per-node aggregate)
- Q3 outcome: PROCEED (resolvable within scope; no framing-refusal)

**Discipline compliance checklist:**
- [x] Discipline #41 substrate-led (cohort partition derives from locked BC axes; no pre-authored taxonomy)
- [x] Discipline #42 framing-audit at consumption (§ 0.1)
- [x] Discipline #43 composition (§ 4 audit hooks per A1-A5; § 3.4 no-silent-re-roll)
- [x] Discipline #45 vocabulary lock (no class/role/archetype non-exempt; cohort terms are BC-axis groupings)
- [x] Discipline #46 § 7 per-cell bounding (mechanical layer queries Phase 4 archive per-cell; no global O(n²) operations)
- [x] Discipline #18 math-hotspot annotation (cohort midpoint estimator → Seam 2 canonical-write)
- [x] Discipline #36 substrate-as-keying-source (Phase 7 keys on BC axes + cohesion scores; no named-personage gating)

**Open items for Seam 2 jack-ryan canonical-write:**
- Canonicalize cohort midpoint calibration methodology (median; per § 1.5)
- Canonicalize q1-to-gauntlet_pass_rate disambiguation (per § 1.4)
- Specify engine math/ folder venue (Q-P7-3 jack-ryan judgment)
- Cross-reference Phase 4 archive ACCEPTED + Phase 5 cohesion-judge output schemas at canonical-write
- Specify Phase7KitVerdictLog + Phase7ClusterAggregateLog DDL (composes with Discipline #46 streaming + per-cell bounding)

**Cross-reference back into canonical:**
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 5.7 referenced; downstream-anchored doc
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` § 3.6 referenced; per-kit cohesion threshold 0.75 anchored
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 4 referenced; cohort partition derived
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` referenced; F-5 / F-1 / F-7 / S-4 / D-5 watches surfaced
