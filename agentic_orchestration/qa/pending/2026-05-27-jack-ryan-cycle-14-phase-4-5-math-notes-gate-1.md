# Finding — Gate-1 DESIGN-MODE — 2026-05-27 — Cycle 14 Phase 4 + Phase 5 Math Notes Bundle

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1 pre-fire)
**Severity:** PASS-with-REVISIONS (per-note detail below)
**Target:** 7 math notes (MG-1 through MG-5 + PM-1 + PM-2) — commits `bacc38d`, `24e1001`, `aa507c3`, `dfb1562`, `211c128` (gamora) + `071de8d`, `90092d6` (gandalf)
**Developers:** gamora (Phase 4 MG-1–MG-5); gandalf (Phase 5 PM-1–PM-2)
**Principles applied:** Review Principles 1 (math-before-code), 3 (cross-seam impact), 4 (decisions-log)
**Disciplines applied:** #1 (math-before-code), #18 (methodology-before-execution), #25 (semantic-layer rep-audit), #40 (scaffold with canonical decision), #41 (pre-authored taxonomy), #42 (framing-audit), #46 (DB anti-materialization + stream)
**Gate-1 checklist source:** Discipline #46 § "When to cite" (dispatch review) + critique-pair-gate-protocol § 3

---

## Summary verdict

| Note | Verdict | Severity | Blocking? |
|---|---|---|---|
| MG-1 — Pareto Dominance | PASS | — | No |
| MG-2 — Crowding / Hypervolume | PASS-with-REVISIONS | INFO × 1 | No |
| MG-3 — Mahalanobis Distance | PASS-with-REVISIONS | WARN × 1 | No (implementation gate explicit) |
| MG-4 — KL Information Gain | PASS-with-REVISIONS | INFO × 1 | No |
| MG-5 — Eviction Rules | PASS | — | No |
| PM-1 — Multimodal Clustering | PASS-with-REVISIONS | INFO × 2 | No |
| PM-2 — Faction-Label Assignment | PASS | — | No |

**Combined bundled verdict: PASS-with-REVISIONS → route to single Matt-gate per Discipline #18.**

No BLOCK findings. All 7 notes clear Gate-1 for Matt-gate routing. PASS-with-REVISIONS items are advisory; they do not hold the Matt-gate. They are surfaced for awareness and may be addressed at Dispatch 3A/3B authoring time or absorbed as named follow-on items.

**Pattern-A consultation questions (fires at KR routing post Matt-gate PASS):**
- Q-Bundle-2 (elrond, MG-3): Gaussian covariance vs density-based — LOAD-BEARING; MG-3 implementation gates on this
- Q-Bundle-1 (elrond, MG-1/2/4): Pareto/crowding/KL methodology — advisory; does not gate implementation start
- Q-Bundle-3 (elrond, PM-1): multimodal clustering algorithm selection — gates Dispatch 3B algorithm lock
- Q-Bundle-4 (star-lord, PM-2): LLM integration cost + architecture — advisory input to Dispatch 3B

---

## Per-note findings

### MG-1 — Pareto Dominance

**What I found:**
Full Discipline #1 compliance — math specified, no implementation code. Per-cell bounding explicit at § 4 header and § 4.3 DB query (Discipline #46 § 7). Required index named (`bc_cell_id + archive_status`). Quality vector definition at § 2 with 5 objectives, dimensionality rationale, and decision criteria for revision (correlation threshold 0.85 → collapse to 3D). Framing-audit Q1/Q2/Q3 complete at § 0. Strict vs weak vs ε-dominance alternatives evaluated at § 5; decision criteria for ε-dominance deferred to elrond consultation (correctly scoped). DB query fetches ≤ 100 rows with explicit LIMIT semantics per Discipline #46 Pattern 1 exception. Composition with MG-5 documented. Pattern-A query for elrond documented per Discipline #18; DOES NOT block Gate-1.

**Discipline #46 § 7 per-cell bounding:** CONFIRMED. "Pareto dominance operates WITHIN BC cells only. The global archive is NEVER materialized for cross-cell comparison." (§ 4 header verbatim). Cell population ≤ 100 kits.

**No findings.** Verdict: **PASS**.

---

### MG-2 — Crowding Distance / Hypervolume

**What I found:**
Full Discipline #1 compliance. Per-cell bounding explicit at § 4 header (Discipline #46 § 7 cited). Two candidate algorithms with computational cost analysis and decision criteria table at § 3. Boundary-population handling at k < 6 specified (Discipline #40 scaffold parameter named). Small-population unconditional acceptance at MIN_POPULATION_FOR_DIVERSITY specified. Framing-audit Q1/Q2/Q3 complete.

**MG-2 § 5 shared DB fetch optimization (INFO):**

MG-2 § 5 documents the shared DB fetch optimization: "fetch Archive_c once at Phase 4 pipeline entry; share across MG-1, MG-2, MG-3, MG-4. Do NOT re-query for each gate." This is the correct 4-round-trips → 1 pattern per Discipline #46 Pattern 1. MG-5 § 8 (Phase 4 pipeline integration) confirms the single shared fetch. The optimization is correctly documented.

**Finding INFO-1:** The HVC (Algorithm B) computational cost estimate at § 2.2 states "O(k^{d-2} × log k) per kit" but the example computation says "O(133M) for full cell recompute." The per-kit cost is O(k^{d-2} × log k) = O(100^3 × log 100) ≈ 1.33M; the full cell recompute at k=100 would be O(100 × 1.33M) = O(133M). The note says this is "NOT per-insertion incremental without approximation" and places the decision in the elrond consultation. This is correct behavior — the note flags the computational concern and defers the algorithm decision appropriately. The INFO here is: the note's Discipline #1.1 pre-fire resource-bounds projection is light — it names cost order but doesn't project wall-clock at full-season insertion rates. This should be incorporated into Dispatch 3A acceptance criteria when HVC upgrade path is evaluated.

[SEVERITY: INFO] Cite: Discipline #1.1 (pre-fire resource-bounds projection). Recommendation: Dispatch 3A should require wall-clock timing of HVC at k=100, d=5 as part of the elrond-consultation-gated upgrade criterion, not just operation-count.

**Verdict: PASS-with-REVISIONS** (INFO advisory; does not gate Matt-gate routing).

---

### MG-3 — Mahalanobis Distance

**What I found:**
Full Discipline #1 compliance. Per-cell bounding explicit throughout (Discipline #46 § 7 cited at § 4 header). Covariance estimation with Welford incremental update, numerical stability guards (variance clamping + pseudoinverse + Tikhonov regularization options). Small-population Euclidean fallback at k < 7 (MIN_COV_POPULATION). Framing-audit Q1/Q2/Q3 complete. Pattern-A query for elrond on Q-Bundle-2 (Gaussian covariance vs density-based) documented as LOAD-BEARING per Discipline #18. The acceptance criteria explicitly state "Elrond Pattern-A consultation returns before MG-3 implementation fires (LOAD-BEARING)" — this is the correct Discipline #18 implementation gate.

**Implementation gate verified:**
MG-3 § 6 verbatim: "Consultation outcome is LOAD-BEARING for the covariance methodology decision — MG-3 implementation MUST await this consultation per Discipline #18 (methodology before execution at math hotspots). Gate-1 PASS does not unblock MG-3 implementation without this consultation." This is exact compliance with Discipline #18 extension-hotspot refinement. The gate is correctly installed.

**Finding WARN-1:** MG-3 § 4.1 Step 3 iterates all k_r in Archive_c for nearest-neighbor computation: O(k × d) per insertion. At k ≤ 100, this is trivial. However, the covariance matrix recompute (§ 4.2) uses Welford with a periodic full-recompute checkpoint every 50 insertions. The inverse computation (Σ_c^{-1}) is O(d³) = O(125) — trivially cheap. The concern is whether `Σ_c^{-1}` is cached between insertions or recomputed per insertion. The note specifies Welford UPDATE for the covariance matrix (correct) but does not specify whether the inverse is recomputed per insertion or only at the periodic checkpoint. At the periodic recompute, an O(d³) inversion is cheap. But if the implementation naively recomputes the inverse on every insertion (even with Welford update), that's an O(d³) per insertion that should be documented as cached vs recomputed. This is a minor implementation-clarity gap, not a math error.

[SEVERITY: WARN] Cite: Discipline #1 (math specification completeness). Recommendation: MG-3 should add one sentence to § 4.2 or § 4.4 stating "Σ_c^{-1} is updated at each periodic full-recompute checkpoint (every 50 insertions); between checkpoints, use the cached Σ_c^{-1} rather than recomputing per insertion." This ensures the implementation doesn't inadvertently recompute the inverse on every kit insertion. Does not block; addressed in Dispatch 3A.

**Verdict: PASS-with-REVISIONS** (WARN advisory; implementation gate for Q-Bundle-2 correctly installed; does not gate Matt-gate routing).

---

### MG-4 — KL Information Gain (Novelty Score)

**What I found:**
Full Discipline #1 compliance. Per-cell bounding explicit (Discipline #46 § 7). KL divergence direction specified with rationale (D_KL(P_c' || P_c) — "adding information" direction; alternative direction evaluated and rejected). JSD fallback for small populations (k < 20) documented with switch criterion. KDE formulation with Scott's rule bandwidth and bandwidth floor. Discrete grid evaluation at resolution=10 per dimension (10^5 cells). Normalization to [0,1] with named NOVELTY_CLAMP scaffold parameter. Smoothing approaches (KDE bandwidth floor + Laplace secondary). Framing-audit Q1/Q2/Q3 complete. Pattern-A query for elrond documented (advisory, not blocking).

**Finding INFO-2:** The discrete grid evaluation at resolution=10 produces 10^5 = 100,000 scalar evaluations per KL computation. The note correctly calls this "fast in Python/NumPy (vectorized)." However, this is a per-insertion-attempt operation — every kit entering Phase 4 triggers this KDE evaluation. At Phase 4 steady-state (many kits per season), the cumulative cost may be non-trivial. The note does not include a Discipline #1.1 pre-fire resource-bounds projection for the KDE compute at full-season insertion rates. At ~28-32 kits per season surviving to Phase 4, this is 28-32 × 100,000 = ~3M scalar ops, trivial in NumPy. But the note's context mentions Phase 4 receives kits from Phase 3 gauntlet — it's the TOTAL kit candidates evaluated (including rejects) that sets the upper bound on KL computation count, not just survivors. If Phase 3 produces O(100s) of candidate kits per season, the compute is still fast but the note should acknowledge this is insertion-attempt-count-dependent.

[SEVERITY: INFO] Cite: Discipline #1.1 (pre-fire resource-bounds projection). Recommendation: MG-4 should add one sentence noting that the 10^5-cell KDE evaluation fires once per Phase 4 insertion attempt (not per survivor); at Phase 3 generation rates (~40-100 kits attempted per season per doc 41 § 4.6 cardinality), this is still trivially fast. Accepting the advisory gap; does not gate implementation.

**Verdict: PASS-with-REVISIONS** (INFO advisory; does not gate Matt-gate routing).

---

### MG-5 — Eviction Rules

**What I found:**
Full Discipline #1 compliance. MG-5 explicitly composed as the final integrator — authored last and documents receipt of MG-1 (Pareto rank + dominated_set), MG-2 (diversity_score), MG-3 (duplicate_flag + replacement_verdict + d_nearest), MG-4 (novelty_score). Two-trigger eviction structure clean — duplicate-based (MG-3 driven; quality replacement; capacity-agnostic) vs capacity-based (cell-at-capacity; admission score vs eviction score). The semantic distinction between these triggers is explicit and well-specified.

Per-cell bounding: CONFIRMED. MG-5 § 6 contains the explicit cross-cell prohibition verbatim: "MG-5 explicitly DOES NOT: Count or compare across BC cells / Trigger global archive rebalancing / Move kits between cells / Evict from one cell to make room in another / Compute any quantity over the global archive population." (Discipline #46 § 7 LOAD-BEARING). Implementation guard documented: if implementation passes global archive, it's a Discipline #46 violation and Gate-2 BLOCK trigger.

Archive status field semantics (ACTIVE / DOMINATED / EVICTED) specified. The DOMINATED status for non-evicted dominated kits preserves archaeology without growing per-cell comparison cost (filtered at query time per `WHERE archive_status = 'ACTIVE'`). This is correct Discipline #46 Pattern 1 composition.

Complete Phase 4 pipeline integration (§ 8): 1 bounded DB read shared across MG-1/2/3/4 + 1 write transaction per insertion. 

Frontier protection for Pareto Rank 0 correctly specified: α1 × (1 - frontier_protection) where frontier_protection = 1.0 for Rank-0 → the frontier_protection term contributes 0 to eviction_score for Rank-0 kits. Correctly renders Rank-0 kits very hard to evict.

All scaffold parameters named per Discipline #40.

**No findings.** Verdict: **PASS**.

---

### PM-1 — Multimodal Clustering Algorithm

**What I found:**
Full Discipline #1 compliance — math specified, no implementation code. Discipline #46 compliance by construction (per-season ~28-32 kit population; ~30 kits × ~25 dim × float32 = ~3KB; trivially bounded; no kernel-panic risk). Five candidate algorithms (A1-A5) with per-alternative recommendation matrix. Algorithm NOT pre-committed — elrond Pattern-A consultation (Q-Bundle-3) documented per Discipline #18. Sparsity branches with explicit thresholds. Composition with Option α Note 1 framed as open question (same vs distinct algorithm class; gandalf leans Option β; correctly deferred to elrond). Discipline #25 (semantic-layer rep-audit) correctly positioned: PM-1 is geometry layer; rep-audit fires at PM-2 consumption time. Framing-audit Q1/Q2/Q3 complete at § 11. Discipline #41 compliance: global cross-season clustering explicitly rejected; per-cell faction assignment explicitly rejected; Algorithm DBSCAN rejected at gate (no target mechanism). No-classes vocabulary clean throughout.

**Finding INFO-3:** PM-1 § 2.2 lists per-kit feature material including `class_name_placeholder = {primary_stat}-{weapon_kind}-{geometry}-{lineage}` under "Kit identity placeholder (from Option α Note 4)." This placeholder uses the term `class_name_placeholder` rather than `kit_name_placeholder`. Per the no-classes architectural recommitment (gandalf 2026-05-27) and Option α Math Note 4 substantive rename from "class-naming policy" to "kit-naming policy," the field name `class_name_placeholder` is vestigial vocabulary per vocabulary lock § 2 retired terms. PM-1 § 2.2 should use `kit_name_placeholder` or `form_name_placeholder` consistent with no-classes vocabulary lock. Minor terminology drift.

[SEVERITY: INFO] Cite: no-classes architectural recommitment § 2 vocabulary lock; Discipline #41 (pre-authored taxonomy interrogation). Recommendation: PM-1 § 2.2 replace `class_name_placeholder` with `kit_name_placeholder` per vocabulary lock. Does not gate Matt-gate routing; addressed in Dispatch 3B.

**Finding INFO-4:** PM-1 § 12.2 surfaces the architectural observation that "PM-1 factions span BC cells (not confined per-cell)" — a faction clusters kits from across the BC manifold. This is CORRECT and consistent with design intent. However, the note surfaces it as an "architectural surprise" for KR awareness without explicitly verifying that elrond's Q-Bundle-3 methodology consultation will evaluate this BC-cell-spanning property. Specifically: HDBSCAN at per-kit substrate scale (Option α Note 1) operates within a single kit's BC cell substrate population. PM-1 clusters across kits from DIFFERENT BC cells. This is not a design concern (it's desired behavior per § 12.2 and engine-as-general-serial-content-product § 2.2), but the elrond consultation query (§ 7.1) should explicitly include "given that PM-1 factions span multiple BC cells in the multimodal feature space, does the choice of clustering algorithm at ~30-kit population need to account for this cross-cell provenance?" The current Q-Bundle-3 at § 7.1 does not include this provenance dimension.

[SEVERITY: INFO] Cite: Discipline #18 (methodology-before-execution; consultation query scope). Recommendation: Add one bullet to PM-1 § 7.1 Q-Bundle-3 question set: "Given that PM-1 clustering operates cross-BC-cell (factions span the BC manifold, not confined per-cell), does this cross-cell provenance affect algorithm choice or feature normalization?" Does not gate Matt-gate routing.

**Verdict: PASS-with-REVISIONS** (INFO × 2 advisory; does not gate Matt-gate routing).

---

### PM-2 — Faction-Label Assignment Policy

**What I found:**
Full Discipline #1 compliance — policy specified, no implementation code. Discipline #46 compliance: N/A direct (algorithmic policy + LLM call infrastructure); 3-5 LLM calls per season; bounded. D-Hybrid + D-Separate recommendation well-reasoned with trade-off table at § 3.6. Deterministic placeholder algorithm at § 3.4 is substrate-grounded (modal_lineage / modal_tech_level / modal_tone / dominant_element tokens from cluster reps); reproducible; Discipline #41 compliant. LLM canonical via SC-3 Pattern B (D-Separate; one call per cluster) with input fields and output schema specified at § 3.5. No-classes vocabulary clean throughout — faction labels correctly framed as "post-hoc emergent cluster identities." Discipline #41 compliance: curated faction-name pool explicitly rejected (§ 4.2) per pre-authored taxonomy prohibition; open-ended substrate-derived vocabulary adopted with THEMATIC_REGISTRY scaffolding.

**§ 2.6 vocabulary collision resolution (PM-2 Q-Bundle-5 item):** "faction-label" vs "canonical archetype-shape" vocabulary collision is cleanly resolved at § 2.6 — same thing at different referential frames (per-season vs cross-season). No conflict with no-classes vocabulary lock. Substantive resolution confirmed.

**Discipline #25 (semantic-layer rep-audit) correctly positioned:** PM-2 § 9 specifies rep-audit at LLM input composition time — verify cluster reps match the substrate evidence the LLM is asked to ground labels on, specifically guarding against Mode B/C/D marginal lineage-tagging-pattern inheritance. This is the correct discipline application.

**D7 AI-tell discipline compliance:** substrate-grounded provenance + constrained-grammar JSON + negative-example vocabulary (§ 4.4 anti-patterns: "Order of X" / "House of Y" / etc.) + cross-faction diversity check (cosine > 0.85 flagged) + human-curated THEMATIC_REGISTRY (gandalf deliverable surfaced). D7 correctly load-bearing.

**Pattern-A query for star-lord (Q-Bundle-4) documented per Discipline #18:** cost projection at Phase 5 scale + LLM call architecture composition + faction_visibility=invisible profile flag + cross-faction diversity check + latency estimate. Does not block Gate-1.

**No findings.** Verdict: **PASS**.

---

## Discipline #46 § 7 per-cell bounding — bundled verification

Per Gate-1 checklist item 1 (LOAD-BEARING):

| Note | Per-cell bounding explicit? | Global O(n²) prohibited? | Cell capacity bound stated? |
|---|---|---|---|
| MG-1 | YES — § 4 header + § 4.3 DB query | YES — "global archive is NEVER materialized" | YES — ≤ 100 kits/cell |
| MG-2 | YES — § 4 header | YES (inherits from MG-1 shared fetch) | YES — ≤ 100 kits/cell |
| MG-3 | YES — § 4 header | YES — per-cell covariance; no global covariance | YES — ≤ 100 kits/cell |
| MG-4 | YES — § 5 algorithm + per-cell KDE | YES — per-cell distribution estimate | YES — ≤ 100 kits/cell |
| MG-5 | YES — § 6 explicit prohibition list | YES — explicit cross-cell prohibition + implementation guard | YES — CELL_CAPACITY_MAX default 50 |
| PM-1 | YES — per-season ~28-32 kit population (Phase 4 eviction bounds) | YES — global cross-archive clustering rejected at § 4.4 | YES — ~30 kits per season |
| PM-2 | N/A direct (policy + LLM) | N/A | 3-5 clusters per season |

**All 7 notes: Discipline #46 § 7 per-cell bounding CONFIRMED.**

---

## Discipline #42 framing-audit — bundled verification

Per Gate-1 checklist item:

| Note | Q1 complete? | Q2 complete? | Q3 complete? |
|---|---|---|---|
| MG-1 | YES | YES | YES |
| MG-2 | YES | YES | YES |
| MG-3 | YES | YES | YES — covariance methodology explicitly flagged for elrond |
| MG-4 | YES | YES | YES |
| MG-5 | YES | YES | YES |
| PM-1 | YES (§ 11) | YES (§ 11) | YES (§ 11) — PROCEED verdict on all 4 |
| PM-2 | YES (§ 11) | YES (§ 11) | YES (§ 11) — PROCEED verdict on all 5 |

**All 7 notes: Discipline #42 framing-audit Q1/Q2/Q3 CONFIRMED.**

---

## Discipline #1 (math-before-code) — bundled verification

Per Gate-1 checklist item:

| Note | Specifies math? | Specifies alternatives? | Specifies decision criteria? | Specifies implementation code? |
|---|---|---|---|---|
| MG-1 | YES | YES (weak/ε/weighted-sum) | YES (correlation threshold 0.85) | NO |
| MG-2 | YES | YES (Algorithm A vs B) | YES (decision criteria table + upgrade trigger) | NO |
| MG-3 | YES | YES (Tikhonov vs pseudoinverse; Euclidean fallback) | YES (threshold adjustment criteria) | NO |
| MG-4 | YES | YES (KL vs JSD vs grid vs Monte Carlo) | YES (switch criterion k < 20) | NO |
| MG-5 | YES | YES (duplicate-based vs capacity-based) | YES (scoring function weights named as scaffold) | NO |
| PM-1 | YES | YES (A1-A5 recommendation matrix) | YES (sparsity branches + smoke test acceptance criteria) | NO |
| PM-2 | YES | YES (D-Det vs D-LLM vs D-Hybrid; D-Within vs D-Separate) | YES (decision table § 3.6) | NO |

**All 7 notes: Discipline #1 math-before-code CONFIRMED. No implementation code in any note.**

---

## Discipline #18 (methodology-before-execution) — Pattern-A consultation gates verified

| Note | Pattern-A documented? | Consultation blocks implementation? | Correctly scoped? |
|---|---|---|---|
| MG-1 | YES — elrond Q-Bundle-1 | NO (advisory; ε-dominance alternative) | YES |
| MG-2 | YES — elrond Q-Bundle-1 | NO (advisory; A-vs-B upgrade path) | YES |
| MG-3 | YES — elrond Q-Bundle-2 | **YES — LOAD-BEARING** (§ 6 explicit; § 7 acceptance criteria explicit) | YES |
| MG-4 | YES — elrond Q-Bundle-1 | NO (advisory; KL/JSD smoothing refinement) | YES |
| MG-5 | N/A — pure composition note | N/A | YES |
| PM-1 | YES — elrond Q-Bundle-3 | **Gates algorithm lock** (Dispatch 3B requires elrond verdict before algorithm committed) | YES |
| PM-2 | YES — star-lord Q-Bundle-4 | NO (advisory; cost projection + architecture composition) | YES |

**All Pattern-A consultations correctly documented per Discipline #18. MG-3 implementation gate is LOAD-BEARING and correctly installed. PM-1 algorithm lock gates Dispatch 3B per Discipline #18.**

---

## Discipline #41 (no-classes vocabulary) — PM-2 verification

PM-2 faction-label assignment: vocabulary clean throughout. "Post-hoc emergent cluster identities" consistently used. Curated faction-name pool rejected per § 4.2 (pre-authored taxonomy at label layer — Discipline #41 violation). No class-as-fixed-taxonomy framing anywhere in PM-2. § 2.6 vocabulary collision resolution (faction-label = canonical-archetype-shape at different frames) substantive and clean.

**PM-2 Discipline #41 CONFIRMED.**

---

## Per-Matt-gate question dispositions (for KR routing)

| Q-Bundle | Question | Gate-1 disposition | Routing recommendation |
|---|---|---|---|
| Q-Bundle-1 (gamora MG sequencing) | MG-5 last per composition? | RESOLVED by gamora — MG-5 authored last; composition explicit. No Matt-gate question. | Closed; no routing needed |
| Q-Bundle-2 (elrond MG-3 covariance methodology) | Gaussian covariance vs density-based? | **LOAD-BEARING** — MG-3 implementation gates on elrond Pattern-A return. Route elrond as sub-agent at KR ratification routing time. | Fire elrond Pattern-A (Q-Bundle-2) at ratification routing |
| Q-Bundle-3 (gandalf PM-1 algorithm vs Option α Note 1) | Same algorithm class OR distinct (Option β)? | gandalf lean is Option β (distinct algorithms per scale). jack-ryan concurs this is the right framing per population-size and feature-space mismatch. Route elrond Pattern-A (Q-Bundle-3) for methodology confirmation. | Fire elrond Pattern-A (Q-Bundle-3) at ratification routing |
| Q-Bundle-4 (star-lord PM-2 LLM cost projection) | ~$0.15-0.25/season within SC-3 envelope? | PM-2 § 3.2 cost analysis shows D-Separate adds ~$0.15-$0.25 per season; within SC-3 envelope ($0.50-$5). Advisory; route star-lord Pattern-A at ratification routing for confirmation. | Fire star-lord Pattern-A (Q-Bundle-4) at ratification routing |
| Q-Bundle-5 (faction-label vocabulary) | Curated pool vs open-ended substrate-derived? | **RESOLVED by PM-2 § 4.2.** Open-ended substrate-derived wins per Discipline #41 (curated pool = pre-authored taxonomy at label layer). Substantive rationale complete. No Matt-gate question; report as resolved. | Closed; resolved in PM-2 |

**Matt-gate routing recommendation:** Route all 7 notes as single bundled Matt-gate per Discipline #18, with the following accompanying Q-Bundle context:
- Q-Bundle-2 (LOAD-BEARING): elrond fires at ratification routing; MG-3 implementation waits
- Q-Bundle-3: elrond fires at ratification routing; PM-1 algorithm lock waits
- Q-Bundle-4: star-lord fires at ratification routing; advisory input to Dispatch 3B
- Q-Bundle-1 and Q-Bundle-5: RESOLVED; no open questions

---

## Architectural concerns (none blocking)

**Advisory 1 — MG-3 covariance inverse caching:** The WARN finding on MG-3 inverse caching is implementation-level and does not affect the mathematical specification or the Gate-1 decision. Flagged for Dispatch 3A acceptance criteria.

**Advisory 2 — PM-1 vocabulary drift:** `class_name_placeholder` term in PM-1 § 2.2 is vestigial; INFO finding. Does not affect substance or Gate-1 decision.

**Advisory 3 — PM-1 cross-BC-cell clustering provenance:** The BC-cell-spanning property of PM-1 factions is correct behavior and design-consistent. The elrond consultation query should include explicit framing of this provenance property (INFO finding). Does not affect Gate-1 decision.

**Note on PM-1 architectural surprise § 12.1 (per-season vs cross-season faction identity):** PM-1 correctly scopes per-season; Math Note 5 territory for cross-season. No action required at Gate-1; surfacing confirmed.

---

## Finding counts by severity

- **BLOCK:** 0
- **WARN:** 1 (MG-3 covariance inverse caching specification — advisory; does not block)
- **INFO:** 4 (MG-2 HVC resource-bounds; MG-4 KDE insertion-attempt scope; PM-1 vocabulary drift; PM-1 cross-BC-cell provenance in elrond query)

---

## Actions

- [ ] **KR:** Route 7-note bundle to single Matt-gate per Discipline #18 math-hotspot ratification
- [ ] **KR at ratification routing:** Fire elrond Pattern-A (Q-Bundle-2 LOAD-BEARING + Q-Bundle-3) as sub-agent per hive-mind protocol § 4.1 decision-routing
- [ ] **KR at ratification routing:** Fire star-lord Pattern-A (Q-Bundle-4) as sub-agent
- [ ] **gamora (Dispatch 3A):** Address WARN-1 — add one sentence to MG-3 § 4.2 or § 4.4 on Σ_c^{-1} caching vs per-insertion recompute; does not require re-Gate-1
- [ ] **gamora (Dispatch 3A):** Address INFO-2 — MG-4 should note that KDE evaluation fires per insertion-attempt (not per survivor); does not require re-Gate-1
- [ ] **gamora (Dispatch 3A):** Address INFO-1 — MG-2 should require wall-clock HVC timing as part of upgrade criterion at implementation time; does not require re-Gate-1
- [ ] **gandalf (Dispatch 3B):** Address INFO-3 — replace `class_name_placeholder` with `kit_name_placeholder` in PM-1 § 2.2 per vocabulary lock; does not require re-Gate-1
- [ ] **gandalf (Dispatch 3B):** Address INFO-4 — add cross-BC-cell provenance question to PM-1 § 7.1 Q-Bundle-3 for elrond consultation
- [ ] **MG-3 implementation:** Gates on elrond Q-Bundle-2 consultation return (LOAD-BEARING per Discipline #18)
- [ ] **PM-1 algorithm lock:** Gates on elrond Q-Bundle-3 consultation return (per Discipline #18)

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-1-pareto-dominance-math-2026-05-27.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-2-crowding-hypervolume-math-2026-05-27.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-3-mahalanobis-distance-math-2026-05-27.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-4-kl-information-gain-math-2026-05-27.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-5-eviction-rules-math-2026-05-27.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-1-multimodal-clustering-math-2026-05-27.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-27-phase-4-5-math-notes-bundle.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 7
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Disciplines #1, #18, #25, #40, #41, #42, #46)

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**Review date:** 2026-05-27
**Mode:** DESIGN-MODE (Gate-1 pre-fire bundled review)
**Authority:** KR autonomous Gate-1 routing per scope-doc § 4.1; Matt 2026-05-27 verbatim Path (1) + Discipline #46 confirm
