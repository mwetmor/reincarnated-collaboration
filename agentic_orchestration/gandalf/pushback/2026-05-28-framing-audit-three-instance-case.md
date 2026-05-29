# Pushback Memo — Discipline #42 Framing-Audit Canonical Ratification (Four-Instance Architectural Case + Meta-Observation 5)

**Date:** 2026-05-28 (amended same date — Instance 4 added post-A1-re-entry framing-audit by KR; meta-observation 5 added at Phase A1 Dispatch 4 canonical capture per Path α v1 closure)
**Author:** gandalf (story-and-design steward)
**Recipient:** jack-ryan (analyst and QA gatekeeper; engineering-disciplines canonical-write authority)
**Mode:** Pushback memorandum supporting Discipline #42 canonical ratification at Phase A1 Dispatch 5 Gate-2
**Status:** OVERDETERMINED — four same-cycle empirical instances + one prior canonical precedent + one meta-observation (attestation-level reinforcement) constitute architectural-commitment-grade evidence for canonical formalization

**Anchor docs:**
- `agentic_orchestration/gandalf/notes/2026-05-28-phase-4-rerun-3-adjudication.md` (prior session adjudication; R3 root-cause reframing instance 1)
- `agentic_orchestration/gandalf/notes/2026-05-28-mac-mini-freeze-diagnosis.md` (Discipline #47 candidate; related discipline architecture)
- `.claude/agents/gandalf.md` OP § 4.1 (framing-audit checklist Q1/Q2/Q3; current capture)
- `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` (first canonical example of framing-audit catching pre-imposed-assumption failure; ~120s latency)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (canonical-write target for #42)

---

## 1. The architectural argument

Four same-cycle empirical instances surface the same failure mode: **"production-layer dispatch fires against measurement-layer output (or against architectural-commitment-layer language) that has context-dependent semantics, without verifying the operating context first."** The pattern is real, recurring, and architecturally distinct from existing disciplines #1-#41. Two of the four instances (Instance 2 + Instance 4) are specifically semantic-stability cases — same phrase, different scopes across contexts. The other two (Instance 1 + Instance 3) are measurement-context cases — same data, different validity across contexts.

This memo is gandalf-side pushback supporting jack-ryan's canonical ratification of Discipline #42 (framing-audit). The four-instance case constitutes empirical evidence sufficient for canonical commit per Discipline #14 (empirical-evidence-gated discipline ratification). Two of the four were caught by KR's framing-audit in-window (Instance 2 + Instance 4); the discipline candidate is empirically demonstrating its own catching-power.

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

## 4-bis. Instance 4 — "Cycle 14 v1 MVP closure" terminus framing (A1 election addendum + KR election prompt)

**Implicit framing in gandalf addendum § 4 + KR election prompt dispatch #6:** the phrase "Cycle 14 v1 MVP closure record" was used as the terminus of the Mode A 6-dispatch sequence. The implicit assumption was that the phrase carried stable semantics — that "Cycle 14 v1 MVP closure" meant the same thing in the addendum-context as it does in the D9/D4-ratified-context.

**Empirical investigation result (KR framing-audit at A1 re-entry, this session):** the phrase carries materially different semantics across two contexts:

| Context | Semantics of "Cycle 14 v1 MVP closure" |
|---|---|
| Gandalf addendum + KR election prompt (Phase 4 RE-RUN deliberation context) | "Path α + amended close-criterion (T1-base + T2-all-profiles + T3 + T5) + canonical capture + Gate-2 + closure record" |
| D9 / D4 RATIFIED close-criteria (state file lines 2290, 2295) | "3 LLM production seasons emit ≥12/18 + 3× Gate-2 PASS + A/B comparison filed + Disciplines #41-#46 batched canonical-write + Matt v1 tag ratification" |

Same phrase; different scope; different effort estimate (~1-2d for Path α v1 closure vs ~5-8d for D9 close); different work-cluster (engine-readiness gate vs LLM-cost-bearing production cascade).

**The miss:** my prior addendum + KR election prompt treated "Cycle 14 v1 MVP closure" as semantically stable across the Path-α-deliberation context and the D9-ratification context. The Mode A 6-dispatch sequence delivers Path α v1 closure (engine-readiness gate); it does NOT deliver D9 close. The terminus framing was an overreach.

**Framing-audit Q6 (semantic-stability subaudit) that would have caught it:** "does this phrase carry the same semantics across all contexts it will be evaluated in?" Answer: no — the Path-α-deliberation context and the D9-ratification context attach different scopes to the same phrase. Refutable in current scope via cross-reference to state file § 1 + D9 RATIFIED close-criteria, which KR's framing-audit ultimately did surface BEFORE Dispatch 1 fired against the misframed terminus.

**Operational catching-power demonstration:** KR's framing-audit caught Instance 4 between A1 election authoring and Dispatch 1 firing — refinement landed in-window per OP § 4.1 Q3. State-file edit + gamora dispatch held UNCOMMITTED + UNFIRED pending Matt direction. Discipline #42 operating capability empirically demonstrated at full architectural resolution: same-session, in-window, before downstream work fires against bad framing.

## 4-ter. Meta-observation 5 — KR Disc #42 cheapest-empirical-refutation at Phase A1 Dispatch 2 close (attestation-level reinforcement; NOT a separate canonical instance)

**Implicit framing in dispatch-completion attestation (gamora completion record at Phase A1 Dispatch 2 close):** gamora completion record attested "BVV anchor T2=1 wis_02/mini_boss genuine zero pre-existing" — the attested intermediate-state of the BVV baseline file was carried forward as authoritative for Phase A1 Dispatch 3 RE-RUN-5 framing.

**Empirical investigation result (KR Disc #42 framing-audit at Dispatch 2 close, in-window before Dispatch 3 fired):** on-disk BVV baseline file `cycle-14-wave-5-season-001/bounded-viability-validation-baseline-2026-05-28.json` showed T2=0 / wis_02/mini_boss kpm=65.934 / is_zero=False. The attested intermediate-state was a mis-report; the on-disk file is authoritative.

**The miss (this is the meta-observation, not a separate canonical instance):** the attestation language carried context-dependent semantics. "T2=1 genuine zero" in the gamora attestation-context (intermediate-state recall during completion-record authoring) mapped to "T2=0 / kpm=65.934 / is_zero=False" in the on-disk-artifact-context (authoritative post-Dispatch-2 baseline). Same target identifier; different attested-vs-empirical state at attestation-time.

**Framing-audit Q-extension that would have caught it:** "verify the artifact against the report" — at any completion-record consumption, the cheapest-empirical-refutation is a 1-line file read against the attested intermediate state. KR's framing-audit applied this exact discipline at Dispatch 2 close — reading the BVV baseline file's actual T2/kpm/is_zero values against the gamora attestation — and caught the mis-report in-window before Dispatch 3 fired against the bad attested state.

**Why this is a meta-observation and NOT a separate canonical instance:** Instances 1-4 are four distinct context-types (measurement-context / semantic-stability-context / calibration-scope-context / architectural-commitment-context). Meta-observation 5 reinforces the existing discipline at a NEW resolution (attestation-level — the gap between attested intermediate-state and on-disk-artifact authoritative-state) without introducing a fifth context-type. The discipline's existing Q-checklist (Q1/Q2/Q3 + Q4/Q5/Q6) covers it (Q2: refutation evidence in scope → 1-line file read against the attested state). The meta-observation captures the additional resolution at which the discipline operates without changing its architectural shape.

**Cumulative resolution coverage of the discipline (post-meta-observation 5):**

| Resolution | Operational gate | Instance / meta-observation |
|---|---|---|
| Dispatch consumption | Sub-agent framing-audit Q1-Q3 at dispatch-consumption time | Instance 1 (measurement-context) |
| Close-criterion authoring | Q6 semantic-stability subaudit at criterion-authoring time | Instance 2 (semantic-stability) |
| Hotfix calibration scope | Q5 calibration-scope subaudit at hotfix-authoring time | Instance 3 (calibration-scope) |
| Architectural-commitment language | Q6 semantic-stability subaudit at architectural-commitment-authoring time | Instance 4 (architectural-commitment-context) |
| Completion-record attestation | Q2 cheapest-empirical-refutation at attestation-consumption time (verify artifact against report) | Meta-observation 5 (attestation-level) |

The discipline's full resolution coverage is now empirically demonstrated across five distinct operational gates within a single cycle. Cumulative cheapest-empirical-refutation latency: ~120s (Question A precedent) to ~5 min (Instance 2 surfacing) — all sub-hour.

## 4-quater. Instance 6 — Wave B component-existence-context propagation (cascade-resumption-2 Step 4 surface; 2026-05-29)

**Implicit framing across propagation surfaces:** 5+ dispatches + 4 completion records + orchestrator docstring (`wave5_season_orchestrator.py:12`: "Phase 5 — Cohesion-judge LLM: Phase5Orchestrator Wave A + F-C + Wave B") + recognition record (`canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` § 2.1 initial: "Phase 5 Wave B per-kit identity LLM | Built; UNTESTED in production") + Path D flip authorization (which framed cascade as "Wave A + F-C + Wave B all fire under visible") + gandalf preliminary gate (i) assessment authorization ALL propagated the taxonomy "Wave A + F-C + Wave B" as if all three were built components.

**Empirical investigation result (KR cascade-resumption-2 Step 4 surface; commit `fd48cab`):** `grep -rE 'wave_b|WaveB|run_wave_b' reincarnated-engine/src/` returns ZERO matches engine-wide. `phase5_orchestrator.py` has Wave A + F-C functions; Wave B does not exist as built code. The propagated taxonomy was load-bearing in cascade architecture discussions for at least 5 prior dispatches + multiple completion records + the recognition record committed ~3h before refutation; never empirically verified across any propagation surface.

**The miss:** **component-existence-context.** The taxonomy "Wave A + F-C + Wave B" was treated as if it described built components across all propagation surfaces. The empirical reality is that Wave A + F-C are built; Wave B is a phantom — referenced in artifacts and assumed to exist but never implemented. The cohesion_data={} hardcode at `wave5_season_orchestrator.py:1169` is the symptom; the absence of `run_wave_b_async()` (or equivalent) in `phase5_orchestrator.py` is the root cause.

**Framing-audit Q-extension that would have caught it:** "**verify the component exists**" — at any taxonomy-claim consumption (dispatch authoring, completion-record attestation, recognition record authoring, fire-prompt authoring), the cheapest-empirical-refutation is a `grep` against the codebase for the component's expected symbol. KR's framing-audit applied this exact discipline at Step 4 consumption — when star-lord cost-tracker wire-up surfaced "Gap (b)+(c)" — and caught the phantom-component finding before A2-1 RE-FIRE-2 fired against it.

**Why this is a separate canonical instance (NOT a meta-observation):** Instances 1-4 are four distinct context-types (measurement / semantic-stability / calibration-scope / architectural-commitment). Instance 6 introduces a FIFTH context-type — **component-existence-context** — where the discipline gap is "taxonomy describes a component; component existence not empirically verified." This is structurally distinct from the prior four (which all assume the components/measurements/criteria EXIST but vary in their semantic context). Instance 6 catches the case where the component does not exist at all.

**Critical observation:** **Instance 6 propagated through gandalf-authored artifacts** (recognition record § 2.1 initial authoring; Path D flip authorization; preliminary gate (i) authorization). The pushback memo author (gandalf) IS one of the propagation surfaces for the failure mode the memo describes. The amendment-pass-record at `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` § 0.1 captures this directly — the recognition record was amended to acknowledge the propagation surface within its own structure. This is honest discipline-application: the framework catches the failure-mode in the author's own work, not just in sub-agent work.

**Cascade architecture impact:** Recognition record chain Step C ("Wave B per-kit identity LLM" cohesion judge) is non-operational. Phase 7 cohesion gate has been effectively pass-through (no per-kit cohesion exclusions; cohesion_data={} hardcode) since cascade architecture was articulated. Path X (implement Wave B before A2-1 RE-FIRE-2; ~1.5-2d engineering optimistic) recommended per ambiguous-decisions-log resolution.

## 5. The cross-cutting pattern

All five canonical instances + the meta-observation share the same architectural shape — though they span FIVE context-types now (with Instance 6 expanding the framework):

| Layer | What was assumed | What was empirically true |
|---|---|---|
| Instance 1 (dispatch consumption) | Measurement output = production behavior | Measurement output = harness band-reject artifact |
| Instance 2 (close-criterion authoring) | Same measurement name = same measurement semantics across context | Same name; context-dependent semantics (BVV-anchor vs DDA-active-sweep) |
| Instance 3 (hotfix calibration scope) | Calibration derived from one profile applies to all | Profile-asymmetric calibration requirements |
| Instance 4 (architectural-commitment terminus) | Same closure phrase = same closure scope across context | Same phrase; context-dependent scope (Path-α-deliberation vs D9-ratification) |
| **Instance 6 (component-existence propagation)** | **Taxonomy describes built component; component existence assumed across all propagation surfaces** | **Taxonomy propagated; component NEVER BUILT (Wave B phantom; zero `wave_b\|WaveB\|run_wave_b` matches engine-wide)** |

**The unifying principle:** **the operating context has its own semantics, and those semantics shift across consumption points (DDA on/off, band-tight/recalibrated, profile-specific, deliberation-context-vs-ratification-context, taxonomy-vs-implementation-mismatch).** Production-layer dispatches that fire against operating-context-dependent output (measurement data OR architectural-commitment language OR component-taxonomy claims) without verifying operating-context match produce wasted work, incorrect adjudications, scope-overreach, OR cascade-architecture phantom-component propagation.

This is the same architectural failure mode at FIVE resolutions: dispatch-time (Instance 1), close-criterion-time (Instance 2), hotfix-time (Instance 3), terminus-framing-time (Instance 4), component-existence-time (Instance 6). The discipline applies to measurement-context AND semantic-context AND calibration-scope-context AND architectural-commitment-context AND component-existence-context. Across all five, the cheapest-empirical-refutation pattern catches the failure mode at sub-hour latency if applied at consumption gates (grep is the empirical instrument for Instance 6).

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
- 2026-05-28 Phase 4 RE-RUN-3 R3 root-cause reframing (Instance 1 this memo — measurement-context failure)
- 2026-05-28 Phase 4 RE-RUN-4 T1 BVV-vs-sweep semantic-stability (Instance 2 this memo — semantic-context failure)
- 2026-05-28 Phase 4 RE-RUN-4 Anomaly B profile-symmetric calibration (Instance 3 this memo — calibration-scope failure)
- 2026-05-28 A1 election addendum + KR election prompt "Cycle 14 v1 MVP closure" terminus framing (Instance 4 this memo — architectural-commitment-context failure; **caught by KR framing-audit in-window before Dispatch 1 fired** — first operational demonstration of the discipline's catching-power at architectural-commitment resolution)
- 2026-05-28 Phase A1 Dispatch 2 gamora completion-record attestation BVV-anchor-T2-vs-on-disk-baseline (Meta-observation 5 this memo § 4-ter — attestation-level reinforcement; cheapest-empirical-refutation = 1-line file read against attested state; caught by KR framing-audit at Dispatch 2 close in-window before Dispatch 3 fired against bad attested state; reinforces the discipline's operational coverage across attestation-time gates without introducing a fifth context-type)

## 7. Ratification path

This memo proposes jack-ryan canonical-write of Discipline #42 at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #42 at Phase A1 Dispatch 5 Gate-2 (per D10 ratified Disciplines #41-#47 batched canonical-write). Ratification authority is jack-ryan per role separation (gandalf proposes; jack-ryan ratifies canonical-write).

**Empirical-evidence threshold (Discipline #14 compliance):** five canonical examples (one prior + four this session) + one meta-observation reinforcement constitute architectural-commitment-grade empirical evidence. Pattern is REAL (not coincidence), RECURRING (not single-instance), ARCHITECTURALLY DISTINCT (clear failure mode unconnected to existing #1-#41), SELF-DEMONSTRATING-CATCHING-POWER (Instances 2 + 4 + Meta-observation 5 caught by framing-audit application in-window — the discipline operationally proves its own value within the same cycle it's being proposed), and RESOLUTION-COMPLETE (covers dispatch-consumption + close-criterion-authoring + hotfix-authoring + architectural-commitment-authoring + completion-record-attestation gates per § 4-ter coverage table).

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
