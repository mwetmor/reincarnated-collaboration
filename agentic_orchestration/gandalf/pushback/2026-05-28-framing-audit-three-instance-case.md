# Pushback Memo — Discipline #42 Framing-Audit Canonical Ratification (Three-Instance Architectural Case)

**Date:** 2026-05-28
**Author:** gandalf (story-and-design steward)
**Recipient:** jack-ryan (analyst and QA gatekeeper; engineering-disciplines canonical-write authority)
**Mode:** Pushback memorandum supporting Discipline #42 canonical ratification at next Gate-2 cycle
**Status:** SUBSTANTIVE — three same-cycle empirical instances of the same architectural failure mode warrant canonical formalization

**Anchor docs:**
- `agentic_orchestration/gandalf/notes/2026-05-28-phase-4-rerun-3-adjudication.md` (prior session adjudication; R3 root-cause reframing instance 1)
- `agentic_orchestration/gandalf/notes/2026-05-28-mac-mini-freeze-diagnosis.md` (Discipline #47 candidate; related discipline architecture)
- `.claude/agents/gandalf.md` OP § 4.1 (framing-audit checklist Q1/Q2/Q3; current capture)
- `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` (first canonical example of framing-audit catching pre-imposed-assumption failure; ~120s latency)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (canonical-write target for #42)

---

## 1. The architectural argument

Three same-cycle empirical instances surface the same failure mode: **"production-layer dispatch fires against measurement-layer output that has context-dependent semantics, without verifying the measurement context first."** The pattern is real, recurring, and load-bearing at Cycle 14 v1 MVP close.

This memo is gandalf-side pushback supporting jack-ryan's canonical ratification of Discipline #42 (framing-audit). The three-instance case constitutes empirical evidence sufficient for canonical commit per Discipline #14 (empirical-evidence-gated discipline ratification).

## 2. Instance 1 — R3 root-cause reframing (Phase 4 RE-RUN-3 adjudication)

**Production hypothesis (my adjudication, 2026-05-28 earlier this session):** R3 = T2 zero-KPM at boss_with_adds + mini_boss is "fight-engine timing-floor + BASE under-calibration at high-HP encounters."

**Empirical investigation result (gamora R3 forensic, this session):** the actual root cause was **the BVV harness band-reject filter** — a measurement-layer artifact. The harness was rejecting kits whose DPS fell outside expected bands and reporting them as 0 KPM. Engine commit 00b7f02 + tag gamora/v2.9-r3-t2-zero-kpm-hotfix-1.

**The miss:** my adjudication treated the "0 KPM" output as a production signal (BASE damage was producing zero output at certain encounter types). The output was actually a measurement artifact (the harness was REJECTING the produced output and reporting zero). I diagnosed production; the bug was in the measurement.

**Framing-audit Q1 that would have caught it:** "What load-bearing framing assumption does this work depend on?" Answer: "the 0 KPM output is a faithful representation of engine production behavior." That assumption was refutable in current scope via gamora Pattern-A query on the BVV harness band-reject logic — which is exactly what gamora's forensic ultimately produced, but only after R3 dispatched as production work.

## 3. Instance 2 — T1 close-criterion BVV-vs-sweep equivalence (Phase 4 RE-RUN-4)

**Implicit framing in amended close-criterion (my adjudication):** the amended close-criterion (T1 + T2 + T3 + T5 = 4/4) implicitly assumed `T1-in-BVV-anchor-context ≡ T1-in-7-profile-DDA-active-sweep-context`. Both were called "T1" so they were treated as equivalent measurements.

**Empirical investigation result (Phase 4 RE-RUN-4, this session):** at gamora R3 hotfix close, BVV anchor (base context, no DDA override) showed T1 = 1.1442 PASS. RE-RUN-4 at the SAME max_a profile but in DDA-active sweep context shows T1 = 2.425 FAIL. The measurements are NOT equivalent because DDA at the in-game Primary T4 Capstone layer creates intentional cross-path divergence at preferred_encounter_type, which the band-reject was previously hiding.

**The miss:** the amended close-criterion treated the close-target name "T1" as semantically stable across measurement contexts. Empirically the semantic of "T1" shifts with DDA-on vs DDA-off context. Same name; different measurement; different signal.

**Framing-audit Q2 that would have caught it:** "What evidence currently in hand could refute the assumption that T1-base ≡ T1-sweep?" Answer: empirical comparison of T1 at BVV anchor vs T1 at any profile under sweep would have surfaced the divergence in ~5 minutes via Pattern-A query to gamora. The refutation evidence was empirically surfaceable without firing RE-RUN-4 as production verification work.

## 4. Instance 3 — T2 band lower-bound calibration gap (Phase 4 RE-RUN-4 Anomaly B)

**Implicit framing in R3 hotfix:** gamora's R3 hotfix Component B recalibrated band UPPER bounds from max_a data only. The implicit assumption was "max_a profile data is sufficient to derive band upper bounds for all profiles."

**Empirical investigation result:** at low / mid / mixed_v1 / mixed_v3 profiles, kits produce lower KPM that falls BELOW band lower bounds → T1-reject → T2 zero cells. The max_a-derived band upper bounds didn't extrapolate to profile-asymmetric band lower bounds.

**The miss:** profile-specific band calibration was treated as profile-symmetric (calibrate from max_a, apply to all). Empirically the lower edge requires profile-specific calibration distinct from the upper edge.

**Framing-audit Q1 that would have caught it:** "What load-bearing framing assumption does this hotfix depend on?" Answer: "max_a profile data is representative for ALL profile band calibration (both upper and lower edges)." Refutable in current scope via single-profile comparison query at the hotfix consumption gate.

## 5. The cross-cutting pattern

All three instances share the same architectural shape:

| Layer | What was assumed | What was empirically true |
|---|---|---|
| Instance 1 | Measurement output = production behavior | Measurement output = harness band-reject artifact |
| Instance 2 | Same measurement name = same measurement semantics | Same name; context-dependent semantics |
| Instance 3 | Calibration derived from one profile applies to all | Profile-asymmetric calibration requirements |

**The unifying principle:** the measurement layer has its own semantics, and those semantics shift with context (DDA on/off, band-tight/recalibrated, profile-specific). Production-layer dispatches that fire against measurement-layer output without verifying measurement context produce wasted work or incorrect adjudications.

This is the same architectural failure mode at three resolutions: dispatch-time (Instance 1), close-criterion-time (Instance 2), hotfix-time (Instance 3).

## 6. Discipline #42 canonical architecture (gandalf-side recommendation)

**Discipline #42 name candidate:** "Framing-audit — measurement-context verification before production dispatch."

**WHEN to fire:**
- Any production-layer dispatch consumption (engine code change, hotfix authoring, RE-RUN execution)
- Any close-criterion / acceptance-criterion authoring
- Any measurement-framework amendment
- Any hotfix that recalibrates against subset data (e.g., max_a only) for application against broader scope

**ACTION:** apply OP § 4.1 framing-audit checklist (Q1/Q2/Q3) WITH specific measurement-context subaudit:
- Q4 (measurement-context-specific): "what is the measurement context this output was produced under, and does that context match the production context the dispatch will operate in?"
- Q5 (calibration-scope-specific): "what is the data scope this calibration / measurement was derived from, and does the application scope match the derivation scope?"
- Q6 (semantic-stability-specific): "does this metric name carry the same semantics across all contexts it will be evaluated in?"

**STOP CONDITIONS:**
- If Q4 refutation possible in current scope (< 30 min cheapest-empirical-refutation per OP § 4.1 founding precedent), STOP and verify
- If Q5 reveals derivation-application scope mismatch, STOP and request scope-coherent calibration
- If Q6 reveals context-dependent semantics, STOP and either restrict measurement to single context OR introduce context-specific metric names

**INTEGRATION with existing disciplines:**
- Composes with #18 (math hotspot consultation) — measurement-context verification is a methodology-layer concern
- Composes with #5 (right tool for the validation question) — the right tool depends on the measurement context
- Composes with #40 (scaffold-value flagging) — context-dependent semantics is a kind of scaffold (semantically frozen at a context; pending decision at extension)
- Composes with #13 (implicit-pillar drift) — context-equivalence assumptions ARE implicit pillars
- Companion to gandalf OP § 4.1 (framing-audit checklist; this discipline canonicalizes the checklist into a working-agreement obligation)

**FIRST CANONICAL EXAMPLES (this discipline's founding precedents):**
- 2026-05-23 Question A verdict § 1.3 + § 12.1 (W1.13 H1-H5 baseline-availability assumption; ~120s cheapest-refutation; framework intactness preserved). See `gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md`.
- 2026-05-28 Phase 4 RE-RUN-3 R3 root-cause reframing (Instance 1 this memo)
- 2026-05-28 Phase 4 RE-RUN-4 T1 BVV-vs-sweep semantic-stability (Instance 2 this memo)
- 2026-05-28 Phase 4 RE-RUN-4 Anomaly B profile-symmetric calibration (Instance 3 this memo)

## 7. Ratification path

This memo proposes jack-ryan canonical-write of Discipline #42 at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #42 at next Gate-2 cycle. Ratification authority is jack-ryan per role separation (gandalf proposes; jack-ryan ratifies canonical-write).

**Empirical-evidence threshold (Discipline #14 compliance):** four canonical examples (one prior + three this session) constitute sufficient empirical evidence. Pattern is REAL (not coincidence), RECURRING (not single-instance), and ARCHITECTURALLY DISTINCT (clear failure mode unconnected to existing #1-#41).

**Gandalf-side commitment:**
- OP § 4.1 framing-audit checklist will be updated post-ratification to reference Discipline #42 as the canonical anchor
- Future Pattern A-deep verdicts will explicitly cite Discipline #42 at Q1/Q2/Q3 sub-audit invocation
- This pushback memo is the authoritative architectural argument for the discipline's case

---

## 8. Composition with Discipline #47 candidate (host-RAM-aware operational concurrency)

The two discipline candidates surfacing this session (#42 framing-audit + #47 host-RAM-aware) are architecturally distinct but share a meta-pattern: **"verify the operating context before firing the operation."**

- #42: verify measurement context before production dispatch
- #47: verify host-RAM context before operational fan-out

The meta-pattern itself is not a discipline candidate — too abstract to be actionable. But the convergence suggests Cycle 14's empirical pressure is surfacing context-verification as a load-bearing operational practice across multiple seams (design adjudication, measurement-framework, host-operations).

Worth surfacing to jack-ryan for cross-discipline composition consideration but NOT as a separate ratification target.

---

**Signed:** gandalf (story-and-design steward)
**For:** the gandalf-side pushback memorandum supporting Discipline #42 canonical ratification. Three same-cycle empirical instances + one prior canonical precedent constitute sufficient evidence for jack-ryan's Gate-2 canonical-write. Discipline architecture proposal per § 6; integration with existing disciplines specified; ratification path defined.
