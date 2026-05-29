# Findings Note — 2026-05-29 — Cascade-R3 Instance 6 #5 Framing Audit + Cumulative Canonical Record

**Reviewer:** jack-ryan
**Severity:** WARN (wave-close; path recommendation: PASS-with-INFO + cascade-resumption-4 fire)
**Scope:** Disc #42a Q1-Q6 framing audit on Phase 4 → Phase 5 disconnect + 5-surface cumulative pattern assessment + canonical pattern record draft
**Authority:** Matt 2026-05-29 evening late "why not also fire jack ryan? and rocket?" + gandalf parallel fan-out directive
**Disciplines applied:** #11, #14, #41, #42a, #43, #45
**Principles applied:** 1, 2, 3, 6

---

## § 1 — Disc #42a Q1-Q6 Framing Audit: Phase 4 → Phase 5 Disconnect

### Empirical baseline (established from cascade empirical chain)

Before applying the Q-audit, the empirical state must be reported as found (survey-mode: what IS).

**Phase 4 archive:** 34 kits. Composition: s0=18, s1=9, s2=7. These are the Pareto-2 winners selected by the (bc_cell_id, cultural_lineage_canonical) partition gate per Amendment 6 Sub-fix 2.

**Phase 5 PM-1 input (s6c-phase-5-entry-gate-content.json):** input_cardinality=598. Composition: 13 base _s2 kits (S1_ prefixed) + 585 _s2 variant kits (investment profile × T4 strategy enumeration). All 598 are _s2 lineage exclusively. s0 and s1 kits: ZERO.

**Cross-reference empirical verification** (jack-ryan live query against kit_archive.db + phase5_faction_clusters.json, 2026-05-29):

- Archive kits in Phase 5 PM-1 input: **6 of 34** (17.6% of archive; 2.9% of Phase 5 input)
- The 6 archive kits in Phase 5 are all _s2 kits: they appear because Phase 5 consumes ALL _s2 kits, not because it consumes the archive
- Archive s0 kits in Phase 5: 0. Archive s1 kits in Phase 5: 0
- Of 7 archive _s2 kits, 6 appear in Phase 5 (1 archive _s2 kit absent from Phase 5 — `S1_endgame_bc_ranged_medium_variable_int_light_s0` — was verified not _s2; correction: `S1_endgame_bc_ranged_medium_variable_int_light_s2` is in Phase 5 but a distinct kit `S1_endgame_bc_ranged_medium_variable_int_light_s0` is in archive and not in Phase 5)
- Phase 5 PM-1 input = Phase 3 _s2 output (base kits + variants), NOT Phase 4 archive output
- PM-1 cluster members: 208 unique IDs appearing in 598 total slots (195 IDs appear in 3 clusters each = soft cluster membership pattern)

**The disconnect (stated plainly):** Phase 4 Pareto-2 archive exists, has 34 quality-selected kits across 3 substrate samples. Phase 5 PM-1 ignores 28 of 34 archive kits. Phase 5 PM-1 receives 208 unique IDs of which 202 are NOT in the archive. The architectural claim that "Phase 4 archive variant preservation feeds Phase 5 PM-1 substrate-led emergence" is empirically refuted at the input layer of this production run.

---

### Q1 — Load-bearing framing assumption

**Assumption under audit:** Amendment 6 Sub-fix 2 claims Pareto-2 lineage partition preserves substrate-distinct winners + feeds substrate-led emergence at PM-1.

**Finding:** The assumption has TWO components that must be evaluated separately:

*Component A (archive construction):* Sub-fix 2 correctly preserves substrate-distinct winners INTO the Phase 4 archive. Archive = 34 kits, substrate-distinct by lineage partition. This component HOLDS empirically.

*Component B (archive→PM-1 consumption):* "feeds substrate-led emergence at PM-1" assumes the archive is the input to Phase 5 PM-1 clustering. This component DOES NOT HOLD empirically. Phase 5 PM-1 consumes Phase 3 _s2 output (598 kits), not Phase 4 archive (34 kits). The archive is a quality-selection layer whose output does not flow to PM-1 in this production run.

**Q1 verdict:** FRAMING FAILURE at Component B. The load-bearing assumption "archive feeds PM-1" is empirically refuted by input_cardinality=598 (Phase 3 output scale, not archive scale) and by direct kit-id cross-reference (6 of 34 archive kits appear in Phase 5 due to incidental _s2 overlap, not due to archive consumption).

---

### Q2 — Cheapest empirical refutation

**The cheapest empirical refutation** is the one-step comparison already executed:

1. Count Phase 5 input_cardinality (598) vs Phase 4 archive count (34) — orders of magnitude different
2. Cross-reference kit IDs: Phase 5 member_kit_ids are ALL _s2 or _s2_variant; Phase 4 archive contains 18 s0 + 9 s1 + 7 s2

This refutation was available at Phase 5 entry gate inspection (Amendment 5 Matt-gate telemetry file). The s6c-phase-5-entry-gate-content.json shows `halt_reason: "Amendment 5 Matt-gate at Phase 5 entry"` and `input_cardinality=598` — observable before any Phase 5 LLM calls fired.

**Q2 verdict:** Cheapest empirical refutation was in-scope at Phase 5 entry gate. Disc #42a Q2 discipline would have caught this before Phase 5 execution if applied at the Phase 5 entry gate inspection step.

---

### Q3 — Semantic stability of "Phase 4 archive feeds Phase 5 PM-1 input"

**Semantic audit across cascade architecture vocabulary:**

| Document | Stated relationship | Semantic held? |
|---|---|---|
| S3 completion record (rocket) | "Phase 4 archive variant preservation" + AG-2 PASS: "PM-1 receives base (~18-54) + variant (~102-132) = >>24" | "Receives" was stated as projection; AG-2 verified cardinality was sufficient — but AG-2 verified PM-1 cardinality generally, not specifically that PM-1 consumes the archive |
| S3 math note | "PM-1 input cardinality >> 24 SPARSITY_TIER_GMM_BIC threshold → GMM BIC-selected" | Cardinality claim was met (598 >> 24), but the cardinality source is Phase 3, not Phase 4 |
| Amendment 6 Sub-fix 2 spec | "Pareto-2 archive partition by (BC × cultural_lineage_canonical)" | Pareto archive is correctly built; not stated explicitly that PM-1 consumes archive (ambiguous) |
| Cascade architecture (Recognition record § 2.1) | Phase 3 PM-1 multimodal clustering — Built; firing | Recognition record does not specify Phase 3 vs Phase 4 as PM-1 input source |

**Semantic stability finding:** The phrase "Phase 4 archive feeds Phase 5 PM-1" was carried implicitly through the cascade architecture design — the cascade chain (phases 2→3→4→5) implies each phase feeds the next. But the actual data flow may be Phase 3 → Phase 5 (bypassing Phase 4 archive as PM-1 input), with Phase 4 serving a separate purpose (quality gate / long-term archive / wave-close selection). The semantic gap is real: "archive" carries two possible meanings — (a) the quality-selection store that PM-1 consumes, OR (b) the quality-selection store that persists cross-season winners for future use. The empirical data is consistent with interpretation (b) but not (a).

**Q3 verdict:** SEMANTIC INSTABILITY. "Phase 4 archive feeds Phase 5" could hold at two different semantic layers (PM-1 clustering input vs cross-season archival quality gate) with different architectural implications. The current production run operationalizes meaning (b) — archive as long-term quality gate — with Phase 3 _s2 output as PM-1 input.

---

### Q4 — Measurement context

**Q4 asks:** Phase 4 archive measurement is at Pareto-2 selection layer; Phase 5 PM-1 input measurement is at multimodal clustering layer. Were these the SAME measurement context per cascade architecture spec?

**Finding:** They are DIFFERENT measurement contexts:

- Phase 4 archive measurement context: quality gate (q1-q5 Pareto-2 selection + crowding + covariance audit). Selects the "best" kits from Phase 3.
- Phase 5 PM-1 measurement context: clustering input (all available _s2 kits, not quality-filtered). Provides population diversity to PM-1 for emergent faction discovery.

These are architecturally separable functions: quality archival vs population clustering. The S3 dispatch and math note verified that PM-1 input cardinality was sufficient (>> 24) but measured cardinality from Phase 3 projection (102-132 projected shipped variants), which implicitly assumed Phase 3 output = PM-1 input. The Phase 4 archive was not the measurement context for PM-1 input — Phase 3 was.

**Q4 verdict:** MEASUREMENT CONTEXT MISMATCH. The cascade architecture appears to have two data paths to Phase 5: (a) Phase 4 archive (quality-selected 34 kits) and (b) Phase 3 full _s2 output (598 kits). The production run used path (b). Whether path (a) is the intended design or an aspirational future state is the architectural question requiring rocket investigation (parallel dispatch).

---

### Q5 — Calibration scope of "substrate-led emergence" at PM-1 input

**Q5 asks:** Per Recognition record cascade architecture, what was the calibration scope for "substrate-led emergence" at PM-1 input?

**Finding:** The Recognition record (§ 1.1 Step D) describes Phase 3 PM-1 multimodal clustering with "Clusters emerge mathematically; substrate votes; PM-1 is the math hotspot." The cascade architecture spec does not restrict PM-1 input to Phase 4 archive specifically — it describes PM-1 as operating on "multiple kits sharing substrate-thematic-identity-adjacency cluster into emergent faction."

If PM-1 operates on 598 _s2 kits (Phase 3 output) rather than 34 archive kits (Phase 4 output), the substrate-led emergence promise may still hold — Phase 3 _s2 kits carry substrate metadata (cultural_lineage_canonical, element, bc_axis signature). The cluster output (4 factions, GMM_k4, input_cardinality=598) does reflect substrate-led clustering by element distribution and BC axis signature (verified in phase5_faction_clusters.json).

**Q5 verdict:** CALIBRATION SCOPE IS AMBIGUOUS but not necessarily failed. Substrate-led emergence at PM-1 may hold whether the input is Phase 3 _s2 (598) or Phase 4 archive (34). The calibration question is whether PM-1 operating on 598 unfiltered kits produces BETTER or WORSE substrate-led emergence than operating on 34 quality-selected archive kits. This is an empirical question for rocket's code investigation + gamora's Phase 3 gate analysis.

---

### Q6 — Semantic stability of "preservation" in architectural-commitment language

**Q6 asks:** Amendment 6 spec: "Phase 4 archive variant preservation" — did "preservation" mean preserved-FOR-Phase-5-input OR preserved-AS-decorative-output?

**Finding:** The S3 completion record at AG-2 states: "PM-1 cardinality >>24 → GMM BIC-selected; Instance 6 degenerate k=3 fallback ELIMINATED." The AG-2 gate was satisfied because PM-1 input_cardinality=598 >> 24. But this cardinality came from Phase 3 _s2 output (585 variants + 13 base), not from Phase 4 archive (34). The archive "preservation" of variant diversity was demonstrated to exist in the archive — but whether that preserved archive actually FED PM-1, or whether Phase 3 output fed PM-1 in parallel, is the architectural question.

If "preservation" = "archive the Pareto-2 winners for long-term quality tracking across seasons" (decorative-for-PM-1), then the architecture works as-is: Phase 3 provides PM-1 population; Phase 4 provides quality gate; Phase 5 consumes Phase 3 for diversity + (optionally) Phase 4 for quality-rep selection.

If "preservation" = "ensure Phase 4 output feeds Phase 5 PM-1 with diverse, quality-selected representatives" (load-bearing-for-PM-1), then Sub-fix 2's archive building is architecturally correct but the wire-up to Phase 5 PM-1 input is missing.

**Q6 verdict:** ARCHITECTURAL-COMMITMENT LANGUAGE IS AMBIGUOUS. "Preservation" carried the implicit meaning of "preserved for Phase 5 consumption" in the dispatch framing but the production run reveals "preserved as archive output" may be the actual semantics. This is precisely the Instance 4 pattern (same phrase; different scope across contexts) extended to the "preservation → fed to PM-1" commitment.

---

### Q1-Q6 Summary

| Q | Finding | Severity |
|---|---|---|
| Q1 | Load-bearing assumption fails at Component B (archive feeds PM-1). Phase 3 output feeds PM-1. | WARN |
| Q2 | Cheapest empirical refutation available at Phase 5 entry gate (input_cardinality=598 vs archive=34) | WARN — was not applied |
| Q3 | Semantic instability: "archive feeds PM-1" vs "archive is quality gate; Phase 3 feeds PM-1" | WARN |
| Q4 | Measurement context mismatch: Phase 4 = quality selection context; Phase 5 PM-1 = clustering input context — different data paths | WARN |
| Q5 | Calibration scope ambiguous but not failed: substrate-led emergence may hold at either input scale | INFO — empirical question for rocket/gamora |
| Q6 | Architectural-commitment language: "preservation" ambiguous (fed-to-PM-1 vs archived-as-output) | WARN — Instance 4 pattern recurrence |

**Q1-Q6 overall verdict:** FRAMING AUDIT FINDS A GENUINE ARCHITECTURAL DISCONNECT. This is not a code bug in the conventional sense — Sub-fix 2's archive construction logic is correct. The gap is at the wire-up layer: the S3 math note and completion record verified PM-1 input cardinality sufficiency via Phase 3 projection, implicitly treating Phase 3 output as PM-1 input without explicitly verifying the Phase 4 → Phase 5 data flow. The result: Sub-fix 2 Pareto-2 archive is decorative for the CURRENT production run's PM-1 clustering.

---

## § 2 — Cumulative Instance 6 Cascade-R3 Pattern Assessment + Wave-Close Blocker Assessment

### 5-surface cumulative table

| # | Surface | Resolution | Pattern type | Layer |
|---|---|---|---|---|
| 1 | Wave B phantom-component | CLOSED by S5/S5b | component-existence-context | Implementation layer |
| 2 | Variant Pareto-dominance at S6c gate content | Pre-ratified per Recognition record A3 H0 | inheritance-vs-rejection | Architectural layer |
| 3 | `emit_skills_for_kit` deterministic (namespace-only "distinct skill trees") | PASS-with-INFO (Amendment 6 Sub-fix 3 Gate-2) | structural-vs-behavioral | Implementation layer |
| 4 | chain_2.element metadata-only for hybrid kits | SYSTEMIC; CLOSED by Amendment 7a (behavioral fix) | structural-vs-behavioral | Implementation layer |
| 5 | Phase 4 Pareto-2 archive bypassed by Phase 5 PM-1 input | UNDER INVESTIGATION (this session) | layer-isolation-vs-integration | Architectural wire-up layer |

### Pattern analysis

**Surfaces 1, 3, 4** share a common structure: code was authored at a structural layer (component created, namespace created, field assigned) but the behavioral layer (component invoked, content varied, element populated) was not wired. Each surface was discovered by empirical grep/query (not theoretical deduction). Surfaces 3 and 4 are the structural-vs-behavioral sub-pattern; Surface 1 is the component-existence sub-pattern.

**Surface 2** is architecturally different: it is a design question (H0/H1 hypothesis testing) that was correctly handled by pre-ratification via the Recognition record Amendment 3 mechanism. Not a failure mode.

**Surface 5** (this session) is structurally distinct from 1/3/4: it is a LAYER-ISOLATION-VS-INTEGRATION gap. Phase 4 archive exists as a quality-selection layer. Phase 5 PM-1 operates as a population-clustering layer. The architectural design implies Phase 4 feeds Phase 5. The production wire-up has Phase 3 feeding Phase 5 while Phase 4 operates as a parallel quality-gate store. This is not a missing behavioral implementation (unlike 3/4); it is a pipeline integration question — which layer provides PM-1 input, and is Phase 4 archive output consumed by Phase 5 at all.

### Gandalf's "BEYOND SYSTEMIC" assessment — framing audit

Gandalf's characterization "pattern is now BEYOND SYSTEMIC" must be evaluated against the Disc #42a Q1-Q6 lens.

**What is systemic:** The recurring pattern that architectural claims about "diversity" or "contribution" or "feeding" cascade layers hold at a structural layer (archive exists, kits are selected, archive is populated) but not at the behavioral/integration layer (PM-1 receives archive output, archive shapes faction clustering) is a genuine pattern. Five surfaces in one work-week is empirically significant per Disc #14 (empirical-evidence-gated ratification threshold).

**What is NOT systemic in the catastrophic sense:** Each surface was caught and resolved before it propagated to player-facing output. Surface 1 was caught before A2-1 RE-FIRE-3 fired. Surfaces 3 and 4 were caught at Gate-2 within the same session batch. Surface 5 is being caught NOW, before the Cycle 14 v1 wave-close is tagged. The discipline (Disc #42a) is operating as designed — catching architectural-commitment gaps before production consequences.

**Is the pattern BEYOND SYSTEMIC in the sense of "requires architectural reconception"?** The Q1-Q6 audit suggests Surface 5 reveals a genuine architectural ambiguity (Phase 3 vs Phase 4 as PM-1 input source) that has not been resolved in the cascade architecture spec. This is worth a design-discussion note — but it is not evidence that the architecture is fundamentally wrong. It is evidence that the Phase 4 → Phase 5 data flow specification was underspecified.

### Wave-close blocker assessment

**Is this a Cycle 14 v1 wave-close BLOCKER?**

Assessment: **NOT a wave-close BLOCKER for the current production run, but REQUIRES explicit resolution before Cycle 14 v1 close can be tagged.**

Rationale:

1. The Cycle 14 v1 close criterion is: "3 LLM production seasons emit ≥12/18 shipped_worthy + 3× Gate-2 PASS + A/B comparison filed + Disciplines #41-#46 batched canonical-write + Matt v1 tag ratification" (per decisions-log D9/D4 RATIFIED close-criteria).

2. The current production run (A2-1 RE-FIRE-3) has Phase 5 LLM outputs that are based on Phase 3 _s2 input (598 kits), not Phase 4 archive input (34 kits). The faction clusters produced (Hallowed Strike Vanguard, Ashwind Pyre Wardens, Ashfield Ember Wardens, Stormcall Chain Wardens) represent genuine substrate-led clustering over the _s2 population — the quality of these outputs is empirically assessable at Gate-2.

3. Whether the faction emergence would be BETTER with Phase 4 archive as PM-1 input is unknown without empirical comparison. Phase 4 archive (34 kits, quality-selected, multi-lineage) might produce more diverse faction clusters than Phase 3 _s2 full-population (598 kits, all _s2, variant-dominated). OR Phase 3 _s2 might produce better population coverage. This is a calibration question (Disc #5 right tool for the validation question).

4. The S3 acceptance gate AG-2 ("PM-1 cardinality >>24 → GMM BIC-selected; degenerate k=3 fallback ELIMINATED") was satisfied at the Phase 5 entry gate — PMI received 598 kits and used GMM_BIC (confirmed). The degenerate k=3 fallback risk that S3 was designed to prevent was correctly prevented.

5. The Sub-fix 2 archive work is NOT decorative in the sense of "wasted effort." The archive serves as:
   - The long-term quality tracking store across seasons (cross-season Pareto maintenance)
   - The wave-close selection mechanism for "which kits make it to the formal archive"
   - The A/B comparison protocol's canon for the current wave (per `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md`)

   Sub-fix 2 is load-bearing for wave-close canonical quality, even if not currently wired as PM-1 input.

**Assessment of "decorative" claim:** gandalf's characterization of "Amendment 6 Sub-fix 2 Pareto-2 work decorative for player-facing output" is partially correct at the level of the CURRENT PRODUCTION RUN's Phase 5 PM-1 clustering. Sub-fix 2 archive output was NOT consumed by PM-1 in this run. However, "decorative" overstates the impact — the archive serves the A/B comparison protocol and cross-season quality tracking, which are load-bearing for Cycle 14 v1 close even if not for PM-1 clustering input.

**Path recommendation: see § 4.**

---

## § 3 — Canonical Pattern Record Draft for Wave-Close

### Pattern name

**"Architectural-layer isolation vs integration gap" — Phase pipeline data flow specification gap**

This is distinct from the previously documented "structural-vs-behavioral variation gap" (Surfaces 3+4). The structural-vs-behavioral gap is about components that exist structurally but don't deliver behavioral output. The layer-isolation-vs-integration gap is about pipeline stages that are individually correct but whose inter-stage data flow was not explicitly specified or verified.

### Discipline locus

**Disc #42a Instance 6 #5 sub-case** — adds a sixth sub-case to the framing-audit case architecture:

| # | Context-type | Instance | Framing-audit failure mode |
|---|---|---|---|
| 1 | Measurement-context | Instance 1 | Production dispatch fires against measurement-layer artifact |
| 2 | Semantic-stability | Instance 2 | Same metric name; different semantics across context |
| 3 | Calibration-scope | Instance 3 | Calibration derived from subset; applied to broader scope |
| 4 | Architectural-commitment | Instance 4 | Same closure phrase; different scope across deliberation contexts |
| 5 | Component-existence | Instance 6 | Taxonomy describes built component; component never built |
| 6 | **Layer-isolation-vs-integration** | **Instance 6 #5** | **Pipeline stage output not wired to downstream stage input; each stage verified individually correct; inter-stage data flow unverified** |

### Canonical pattern record text (draft for wave-close write)

**Sub-case: Layer-isolation-vs-integration gap**

**Definition:** A pipeline architecture with stages A → B → C is designed such that A's output feeds B's computation, which feeds C's output. Each stage is individually verified (unit-tested, smoke-tested, completion-recorded). The inter-stage data flow (specifically: does B receive A's output as its input?) is NOT explicitly verified at any acceptance gate. The result: B may operate correctly but on a different input source than A's output, making A's quality work effectively invisible to B's processing in the current production run.

**Distinguishing features vs component-existence (Instance 6 #5 vs #1):**
- Component-existence: the component does NOT EXIST at all (Wave B: zero grep matches)
- Layer-isolation-vs-integration: BOTH layers exist and work correctly; the DATA FLOW between them was not wired/verified

**Distinguishing features vs structural-vs-behavioral (Surfaces 3+4):**
- Structural-vs-behavioral: the component exists and IS wired, but outputs structurally identical content where content-level variation was assumed
- Layer-isolation-vs-integration: the output of layer A exists and is correct, but layer B receives its input from a DIFFERENT source (not layer A)

**Catch mechanism:** Disc #42a Q4 (measurement context) — verify that the measurement context for downstream stage (Phase 5 PM-1 input_cardinality=598) matches the output context of the upstream stage (Phase 4 archive=34). When these are orders-of-magnitude different, Q4 should flag.

**Canonical example:** Cascade-R3 Sub-fix 2 Pareto-2 archive (Phase 4 output=34 quality-selected kits) vs Phase 5 PM-1 input (598 Phase 3 _s2 kits). Phase 4 archive built correctly; Phase 5 PM-1 clustering correct on its input; inter-stage wire-up unverified at acceptance gates.

**Prevention prescription:** At any pipeline acceptance gate for stage N, add explicit verification: "What is the input to stage N? Does it come from stage N-1's output? How many items?" Cross-reference upstream stage's output count with downstream stage's input count at the acceptance gate. When the pipeline has N stages, the acceptance gate for stage K should verify input_cardinality matches stage K-1 output_cardinality (or explicitly documents the reason for a different input source).

### Disc #42a amendment vs new Disc #50

**Recommendation: Disc #42a amendment (Q4 elaboration), not new Disc #50.**

The layer-isolation-vs-integration sub-case extends Q4 (measurement context) with a pipeline-specific prescription. It does not require a new discipline number — it is a natural elaboration of Q4's "measurement context" concept applied to multi-stage pipeline data flow. A new discipline (#50) would be appropriate if the pattern is architecturally distinct enough to require separate trigger conditions and stop conditions. At this time, the Q4 elaboration is sufficient.

**Draft Q4 amendment for Disc #42a:**

Add to Q4: "For multi-stage pipeline stages: verify the input to this stage comes from the expected upstream stage's output. When input_cardinality is orders-of-magnitude different from upstream stage output count, stop and verify the data flow source explicitly. The gap may be intentional (pipeline stage serves different function than PM-1 input) OR may indicate a missing wire-up."

---

## § 4 — Path Recommendation

### Recommendation: PASS-with-INFO + cascade-resumption-4 fire

**NOT a Cycle 14 v1 wave-close BLOCKER.** Here is the reasoning:

**Arguments for PASS-with-INFO (not BLOCK):**

1. The current production run (A2-1 RE-FIRE-3) has produced valid Phase 5 LLM outputs. Phase 5 PM-1 operated on 598 _s2 kits and produced 4 coherent factions (GMM_BIC_selected, no degenerate fallback, Wave B fired for 13 kits per wave_b_kit_count in faction_clusters.json). These outputs are empirically assessable at Gate-2.

2. The Sub-fix 2 "decorative" characterization applies only to THIS RUN's PM-1 clustering. The archive is load-bearing for the A/B comparison protocol and cross-season quality tracking.

3. The degenerate k=3 fallback was eliminated (GMM_BIC confirmed). The PM-1 clustering degradation that S3 was designed to prevent did NOT occur — it was prevented by Phase 3 variant cardinality (598 >> 24), not by Phase 4 archive size.

4. The Cycle 14 v1 close criterion does not specify "Phase 4 archive feeds Phase 5 PM-1" — it specifies "3 LLM production seasons emit ≥12/18 shipped_worthy." Whether those shipped_worthy kits come from Phase 5 input derived from Phase 3 or Phase 4 is not a stated close criterion.

5. Rocket's parallel investigation (code-level) will determine whether Phase 4 archive IS wired to Phase 5 PM-1 or whether Phase 3 is the intended input. If Phase 3 → Phase 5 is the INTENDED architectural design (archive as quality-gate-only, not PM-1 input), then this is not a gap at all — it is the correct architecture, with Sub-fix 2 serving its intended cross-season archival role.

**Arguments against BLOCK:**

A BLOCK would require that the current production run's output is architecturally invalid and cannot support Cycle 14 v1 close. This is not established: the faction outputs are substrate-led (verified by element distribution + BC axis signature in cluster output), the GMM is properly selected (not degenerate), and Wave B fired against the cluster representatives. The substrate-led emergence promise is functioning at the PM-1 layer for this run.

**What cascade-resumption-4 should address (if rocket investigation confirms gap):**

If rocket's code investigation confirms that Phase 4 archive output is NOT wired as PM-1 input (i.e., Phase 3 → Phase 5 is the current implementation), cascade-resumption-4 should:

1. Decide (Matt design call): is Phase 4 archive the intended PM-1 input, or is Phase 3 _s2 output the intended PM-1 input?
   - If Phase 4 intended: wire Phase 4 archive output → Phase 5 PM-1 input; re-fire A2-1 RE-FIRE-4 on the archive-input path
   - If Phase 3 intended: document explicitly in cascade architecture spec; Sub-fix 2 archive purpose = cross-season quality tracking only (not PM-1 input); Cycle 14 v1 close can proceed on current architecture
   - If both intended (hybrid): Phase 4 archive provides quality-rep representatives; Phase 3 _s2 provides population coverage; PM-1 receives the union — design this explicitly

2. Canonical spec update: amend cascade architecture recognition record § 2.1 to explicitly state the PM-1 input source (Phase 3 _s2 vs Phase 4 archive vs union)

**Cascade-resumption-4 trigger condition:** ONLY if rocket confirms Phase 4 → Phase 5 wire-up is missing AND Matt design call elects Phase 4 as intended PM-1 input source. If Matt confirms Phase 3 → Phase 5 is intended, close with canonical spec update only — no re-fire needed.

**If cascade-resumption-4 fires:** scope is narrow — wire Phase 4 archive output to Phase 5 PM-1 input (one code change at wave5_season_orchestrator.py), re-fire Phase 5 only (no Phase 2-4 re-fire needed; archive already built). Estimated ~0.5-1d rocket implementation + Gate-2 + LLM re-fire cost.

---

## § 5 — Disciplines Canonical-Write Candidacy Notes for Cycle 14 Wave-Close

The following items accumulate to the Cycle 14 wave-close canonical-write queue from this analysis and the 3 prior Gate-2 findings:

### From this session (Surface 5 / § 3 above):

1. **Disc #42a Q4 elaboration — pipeline layer-isolation-vs-integration gap** (jack-ryan seam): Add pipeline data flow verification prescription to Q4. Sub-case name: "Layer-isolation-vs-integration gap." Draft text per § 3 above.

### Carried forward from prior Gate-2 findings (Amendment 6 + Amendment 7):

2. **Disc #42a Instance 6 sub-case: structural-vs-behavioral variation gap** (jack-ryan seam): Three cascade-r3 surfaces (phantom-component, namespace-only, chain_elements metadata-only) collectively constitute the structural-vs-behavioral sub-case. Amendment 7a as counter-example (behavioral content variation confirmed).

3. **Paired-joint-sampling discipline candidate** (jack-ryan + gandalf seam): Per Amendment 6 Gate-2 § 4 and Amendment 7 Gate-2 § 4.

4. **Bound 4 criterion "(4)" language reconciliation** (gandalf seam): "skill_tree variation enters Pareto via quality vectors" → namespace-only variation per Amendment 6 Sub-fix 3.

5. **DEX Option C attribute-system lock closure** (gandalf seam): attribute-system-2026-05-24.md § 2.1 "Lock at Stage 0 design call" retroactively EXECUTED in Amendment 7.

6. **Math note § 1.3 seeding description clarification** (rocket seam): `_draw_cell_elements` single batch `random.sample()` vs per-sample-idx framing.

7. **Disc #49 candidate (oversized-file operational safety)** (jack-ryan seam): Carved from Disc #48 R48.1/R48.2/R48.3 per prior Pattern E Gate-2.

8. **Disc #42a Instance 7 — founding-incident-confounding-attribution** (jack-ryan seam): Disc #48 R48.4/R48.5 retirement founding case; sixth context-type for framing-audit.

9. **Cascade architecture PM-1 input source explicit documentation** (gandalf seam): Recognition record § 2.1 amendment to state PM-1 input source explicitly (Phase 3 _s2 vs Phase 4 archive vs union design decision).

### Priority order for wave-close write:

- P1 (load-bearing): Disc #42a Q4 pipeline elaboration + structural-vs-behavioral sub-case (#1 + #2)
- P2 (design clarity): PM-1 input source documentation (#9) — depends on rocket + Matt design call
- P3 (housekeeping): #3-#8 items above

---

## § 6 — Surface Conditions Assessment

| Condition | Triggered? | Action |
|---|---|---|
| Recommendation: Cycle 14 v1 wave-close BLOCKER | **NO** — current run output is empirically valid; PM-1 clustering correct on its input; faction outputs substrate-led | PASS-with-INFO + cascade-r4 (conditional) |
| Disc #42a framing-audit catches 6th pattern instance | **YES** — layer-isolation-vs-integration gap is new sub-case | Documented in § 3; Disc #42a Q4 amendment candidate |
| Effort exceeds ~1h | NO — within ~45-60min scope | — |

**No BLOCK issued. No halt condition triggered.**

---

## References

**Empirical data files reviewed:**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/s6c-phase-5-entry-gate-content.json` — Phase 5 entry gate (input_cardinality=598)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` — PM-1 cluster output (208 unique IDs; 598 total members)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/kit_archive.db` — Phase 4 archive (34 kits: s0=18, s1=9, s2=7)

**Prior Gate-2 findings reviewed:**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-gate-2-pattern-e-review.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-amendment-6-gate-2-pattern-e-review.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-amendment-7-gate-2-pattern-e-review.md`

**Design docs reviewed:**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` — Disc #42a pushback memo + 5-context-type architecture
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — Recognition record (Amendment 3 H0/H1)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-29-jack-ryan-cycle-14-cascade-resumption-3-instance-6-5-framing-audit-and-cumulative-canonical-record.md` — Authoritative dispatch

**Engine commit reviewed (Amendment 7a):**
- `5b76790` — `rocket/v1.0-cascade-r3-amendment-7a-skillemissionconfig-chain-elements-1` — chain_2.element behavioral fix (Instance 6 #4 CLOSED)

**Live queries executed (jack-ryan):**
- `kit_archive.db` — 34 rows; s0/s1/s2 distribution; cross-reference with phase5_faction_clusters.json
- Python analysis confirming 6 of 34 archive kits appear in Phase 5 (incidental _s2 overlap, not archive-feed)
- Cluster member uniqueness (208 unique IDs appearing in 598 total slots via soft cluster membership)
