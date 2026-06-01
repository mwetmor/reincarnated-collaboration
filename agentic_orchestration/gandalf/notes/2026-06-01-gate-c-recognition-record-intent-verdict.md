# Gate (c) Recognition-Record Intent Verdict — Phase 4 → Phase 5 Disjoint at Swift Closure

**Date:** 2026-06-01
**Author:** gandalf (story-and-design steward; recognition-record author)
**Status:** Pattern A-deep verdict — design-intent authority on the 2026-06-01 gauntlet-metrics-as-provisional-hypotheses recognition record
**Authority:** seam-owner decision per hive-mind decision-routing § 3.9 (recognition-record design intent is gandalf's seam); Matt last-resort escalation
**Composes with:** `canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` (commit `daa1c98`); `agentic_orchestration/gandalf/notes/2026-05-29-phase-4-phase-5-disjoint-population-bug-surface.md`; `agentic_orchestration/star-lord/notes/2026-06-01-wave-5-swift-closure-cohesion-judge-surface.md` (commit `6593626`); `agentic_orchestration/gamora/notes/2026-06-01-wave-5-swift-closure-archive-snapshot-stable.md` (commit `16ce0bf`)

---

## 0. TL;DR — verdict

**Verdict: OPTION 2 — Path X structural fix required before star-lord cohesion judge fires.**

The recognition record's "fire AS-IS" intent applies to **metric-axis provisionality**, NOT to **structural-input correctness**. § 4.2 explicitly preserves "engine architecture (the gauntlet structural sieve remains valid; the Pareto-2 reduction methodology remains valid; only the metric-axis validity is in question)." A Phase 5 cohesion judge that clusters a population disjoint from the Phase 4 Pareto-2 archive does NOT cluster the wave-5 archive — it clusters a different artifact. PROVISIONAL marker discipline cannot retroactively cover an input-population mismatch; that is a category error.

Gamora's separability framing is correct in its sphere ("closure question separates from architectural decision") but mis-applies to Gate (c) specifically. The Wave B / X/Y/Z election is genuinely separable from closure; **Path X is not.** Path X is the precondition that makes the Phase 5 cohesion judge output meaningful as a wave-5 snapshot artifact. Without it, "fire AS-IS" produces an output whose claimed identity (cluster taxonomy over the wave-5 archive) does not match its actual identity (cluster taxonomy over ~208 `_s2`-only variants).

**Operational consequence:** KR authors a sequenced rocket/gamora Path X dispatch BEFORE re-engaging star-lord. Wave-close timeline extends ~1-2 engineering days. Star-lord cohesion judge fires AFTER Path X lands. Recognition-record substrate-led discipline at the validation-metric layer is preserved; recognition-record structural-integrity presumption at § 4.2 is honored rather than overridden.

**Empirical-criterion gate for Path X completion** (per the four-question structure below, Q3): code at `wave5_season_orchestrator.py:825-836` reads Phase 4 archive output as Phase 5 PM-1 input; smoke test confirms `len(Phase 5 PM-1 input) == 34` and kit_ids match Phase 4 archive's 34; PM-1 sparsity branch verified at n=34 (k may drop to 2 or 3; that is acceptable and informative).

---

## 1. Re-reading the recognition record in light of Gate (c)

The Gate (c) question is precisely the right question to ask of the recognition record. Star-lord's pre-fire inspection caught the framing dependency the record presumes but does not name explicitly. Re-reading § 4.2 verbatim:

> "Engine architecture (the gauntlet structural sieve remains valid; the Pareto-2 reduction methodology remains valid; only the metric-axis validity is in question)."

This sentence is load-bearing. The recognition record carves the design space into two layers:

1. **Metric-axis layer** (KPM thresholds, cohort taxonomy, winning criteria, BVV thresholds, encounter representativeness) — PROVISIONAL; designer-asserted; awaiting playtest validation
2. **Structural layer** (Pareto-2 reduction methodology, gauntlet structural sieve, Phase boundaries, cross-phase consumption contracts) — PRESERVED as valid; not in question

The "fire AS-IS" instruction in § 4.3 operates on the metric-axis layer. It says: stop iterating the metrics toward convergence; lock the current snapshot. It does NOT say: tolerate structural breakage at phase boundaries because the metric layer is already provisional.

If the recognition record had intended to authorize Option 1 (fire against the structurally-disjoint population), it would have had to explicitly demote the Phase 4 → Phase 5 consumption contract from "structural layer" to "metric-axis layer." It does not do this. It does the opposite: § 4.2 names the Pareto-2 reduction methodology specifically as preserved-and-valid. The Pareto-2 reduction methodology IS the Phase 4 archive; consuming a different population at Phase 5 means the Pareto-2 reduction methodology is doing no work at the cohesion-judge layer.

**The recognition record presumed structural integrity at the Phase 4 → Phase 5 boundary.** That presumption was correct as design intent and incorrect as empirical state. Star-lord's Gate (c) surface caught the gap. The right resolution is to make the empirical state match the design intent, not to retroactively re-frame the design intent to absorb the empirical state.

This is itself a Disc #42a framing-audit observation, applied to the recognition record's own framing. Q3 answer: yes, the right move is to refine execution sequencing (Path X first) rather than execute as-currently-framed (Option 1).

---

## 2. The four questions answered

### Q1 — Does "fire AS-IS" in recognition § 4.3 wave-5 close dispatch include the structural-disjoint code path as currently constituted?

**No.** "Fire AS-IS" carries METRIC-axis provisionality, not STRUCTURAL-axis tolerance. Star-lord's CONDITIONAL on Gate (c) is correctly surfaced; the recognition record presumed § 4.2 structural integrity, which is empirically absent in code at `wave5_season_orchestrator.py:825-836`. Option 1 would produce a Phase 5 output whose claimed identity (cluster taxonomy over the wave-5 Phase 4 archive) does not match its actual identity (cluster taxonomy over ~208 `_s2`-only variants). That is not a provisionality issue; that is a category-mismatch issue. PROVISIONAL markers cannot cover it.

### Q2 — If Option 1: how does PROVISIONAL marker propagate to cluster identity inheritance?

**N/A under the verdict** (Option 2 selected). However, for completeness on why Option 1 was rejected: the recognition § 3.1 Disc #41 amendment candidate frames substrate-led discipline as applying at TWO layers — substrate-input layer AND validation-metric layer. Path X relates to neither. Path X is at the **inter-phase consumption layer** — the contract that Phase 5 reads Phase 4's output. That is a structural layer, not a metric-validity layer.

If we had attempted to absorb Option 1 under the PROVISIONAL marker, we would have implicitly extended Disc #41 to a THIRD layer (inter-phase consumption contracts), which would conflate "metric is provisional" with "input population is wrong." Those are different failure modes with different empirical-validation gates. Conflating them weakens the discipline rather than strengthening it. Star-lord's surface note caught this explicitly: "structural integrity ≠ metric-validity... cohesion judge fires against wrong input — that's a different kind of provisionality." That distinction is correct and load-bearing.

### Q3 — If Option 2: empirical-criterion gate for Path X completion

Three checks, all required before star-lord re-fires:

**Check (i) — code-level**: `wave5_season_orchestrator.py:825-836` consumes Phase 4 archive output as Phase 5 PM-1 input. Empirically: the assignment to `surviving_kit_datas` reads from the Phase 4 archive Pareto-2 winners (the 34 kit_ids in gamora's archive-stable note), NOT from `passing_kits + variant_passing_rows`.

**Check (ii) — smoke test**: post-Path-X, run Phase 5 PM-1 against snapshot Phase 4 archive. Verify:
- `len(Phase 5 PM-1 input) == 34`
- Set of kit_ids in PM-1 input == set of kit_ids in Phase 4 archive (per gamora's enumerated list)
- PM-1 sparsity branch behavior at n=34: cluster count may drop from k=4 to k=2 or k=3; this is EXPECTED and acceptable (per my 2026-05-29 surface § 3 lean caveat 1). Cluster count drop is informative, not a failure mode.

**Check (iii) — BC-axis coverage smoke**: Phase 4 archive's 34 kits span all 8 elements per Amendment 7 verification (gandalf 2026-05-29 surface § 3 caveat 3). Verify that the post-Path-X Phase 5 PM-1 input preserves 8-element coverage. If 8-element coverage degrades to <6 elements, surface as a Path X regression and re-evaluate Path Y or Hybrid X+Y. (I expect this to pass cleanly; flagging as a verification gate, not a likely failure.)

**No BC-axis check substitutes for fixing Path X.** There is no smoke-test or BC-axis verification that would confirm the existing code path's disjoint output is acceptable as the wave-5 snapshot. The disjoint is structural; only structural correction resolves it.

### Q4 — Composition with gamora's separability framing

Gamora's framing is partially correct and partially mis-applied.

**Correct application** (the separability framing as authored): the recognition-record swift-closure decision IS separable from the broader Wave B / Path X / Path Y / Path Z architectural election. The recognition record closes the gauntlet-iteration-to-convergence question; it does not adjudicate the architectural surfaces beneath. Cycle 15+ canonical workstreams can address those architectural questions independently. On this, gamora is right.

**Mis-application** (extending separability to Gate (c) specifically): closure CANNOT separate from the Phase 4 → Phase 5 input-consumption contract, because the wave-5 closure artifact set INCLUDES the Phase 5 cohesion judge output. If that output is generated over a population disjoint from the closed Phase 4 archive, the artifact set is internally incoherent — Phase 4 archive and Phase 5 cohesion clusters claim to describe the wave-5 snapshot but describe disjoint populations. A wave closure that ships internally incoherent artifacts is not a valid closure; it is a deferred-debt closure that downstream consumers will have to untangle.

The distinction gamora's framing missed: the Wave B architectural-decision and the Path X structural-fix have different relationships to wave-5 closure. **Wave B is a separable architectural decision** (it concerns long-arc engine design and can be decided post-wave-close). **Path X is a wave-close prerequisite** (it concerns whether the wave-5 snapshot artifact set is internally coherent). The two are not equivalent on the separability axis.

This composes with my 2026-05-29 surface note § 3 gandalf-lean: "Path X (Phase 5 PM-1 input = Phase 4 archive output) with caveats." That lean was correct then and remains correct now. The recognition record was authored against the assumption that Path X had landed or would land; star-lord's pre-fire inspection caught that the assumption did not hold empirically.

**Does separability conflict with the substrate-led discipline extension at the validation-metric layer?**

No — they operate at different layers. Substrate-led at the validation-metric layer (recognition § 3.1) is about whether KPM thresholds, cohort taxonomy, etc. are designer-asserted vs playtest-validated. Path X is about whether the Phase 4 → Phase 5 consumption contract is structurally honored. They are orthogonal. Honoring Path X does not affect the Disc #41 amendment candidate; deferring Path X does not strengthen the Disc #41 amendment candidate. They are independent disciplines.

---

## 3. Why Option 2 over Option 1 — design-intent grounding

Three grounding observations from inside the recognition record's intent:

### 3.1 The recognition record protects the meaning of "snapshot"

The recognition record's load-bearing word is **snapshot**. It carries a precise design meaning: the wave-5 artifact set is locked at current state, treated as provisional working-state, and downstream consumers read PROVISIONAL markers at the metric-axis layer. For "snapshot" to carry this meaning, the artifact set must be internally coherent. A snapshot whose Phase 4 archive and Phase 5 cohesion clusters describe disjoint populations is not a snapshot of one thing — it is two artifacts laminated together that claim a shared identity they don't have.

If we accept Option 1, "snapshot" becomes a label that hides incoherence rather than naming a coherent locked state. Downstream consumers (rocket pattern library Phase A; Cycle 15+ workstreams) will encounter the incoherence and have to litigate it later. That defers cost, doesn't eliminate it, and weakens the discipline word "snapshot" for future use.

### 3.2 The PROVISIONAL marker is a metric-axis discipline, not a catchall

The PROVISIONAL marker discipline was authored with a specific scope: it tags artifacts whose VALIDITY-AS-GROUND-TRUTH awaits empirical playtest validation. The empirical-validation gate is manifestation-milestone-enabled playtest. That gate validates: do the KPM predictions match playtest KPM? Do the cohort archetype labels match playtest experience? Do the BVV thresholds hold under actual play?

The gate does NOT validate: did Phase 5 cohesion judge cluster the right population? That is not a question playtest can answer. Playtest cannot retroactively repair an input-population mismatch. So the manifestation-milestone gate is not a valid validation instrument for Option 1's failure mode.

If we attempt to absorb Option 1 under PROVISIONAL, we use a marker whose validation instrument does not apply. That dilutes the marker's meaning and creates a class of "PROVISIONAL" artifacts that no future playtest can validate-or-refute. Star-lord's gate-(c) framing caught this: "that's a different kind of provisionality." The right discipline is to NOT mark structural-disjoint-input-population artifacts as PROVISIONAL, because PROVISIONAL implies a validation path that does not exist for them.

### 3.3 The recognition record was authored to STRENGTHEN substrate-led discipline, not to absorb engineering debt

Matt 2026-05-31 verbatim framing: "the mathematical tests we used were created without evidence of validity." The recognition is about validity-of-metrics-as-ground-truth. It is not about: "wave-5 has accumulated structural debt and we should ship as-is to close." If we accept Option 1, we covertly extend the recognition record from "we recognize gauntlet metrics are provisional" to "we recognize gauntlet metrics are provisional AND we tolerate Phase 4 → Phase 5 disjoint input populations because the metrics are provisional anyway." That extension was not authorized by Matt's 2026-05-31 surfacing and is not the discipline the recognition record canonicalizes.

The recognition record's own framing-audit observation (§ 3.2) applied substrate-led discipline at a higher layer of rigor than the engine currently honors. Option 1 would do the opposite at the structural layer — accept a lower bar for structural integrity than the engine has historically honored. That is asymmetric. The right discipline application is consistent rigor: Option 2 strengthens both the validation-metric layer (recognition § 3.1) AND the inter-phase consumption contract (Path X).

---

## 4. Operational consequence — what KR does now

1. **Author a sequenced rocket/gamora Path X dispatch.** Scope per gandalf 2026-05-29 surface note § 2 Path X spec: change `wave5_season_orchestrator.py:825-836` to read Phase 4 archive output as Phase 5 PM-1 input. Estimated effort per my prior lean: ~1-2hr rocket (code change + PM-1 sparsity branch verification + ~5-10 new tests). Composition with Amendment 7a if still in-flight: independent; can land in same dispatch or sequentially.

2. **Empirical-criterion gate** (per § 2 Q3 above): three checks (code-level + smoke test + BC-axis coverage). All three must pass before star-lord re-engages.

3. **Re-engage star-lord** with confirmation: Path X has landed; Phase 4 → Phase 5 consumption contract structurally honored; pre-fire Gate (c) now PASS; cohesion judge fires.

4. **Wave-close documentation amendment** (jack-ryan, when canonical write fires): wave-close canonical write notes that Path X landed as part of swift-closure execution; the disjoint population issue surfaced by gandalf 2026-05-29 is resolved at the structural layer; PROVISIONAL marker applies at the metric-axis layer per recognition record.

5. **Wave-close timeline impact**: extends by ~1-2 engineering days for Path X. This is acceptable. The swift-closure recognition's primary value-creation is freeing the team from converging-against-unvalidated-metrics, which was a multi-week opportunity cost. Adding ~1-2 days for Path X to preserve artifact coherence is a small overhead against that gain.

6. **What does NOT happen**: the broader Wave B election is NOT forced now. Path Y (variant emission extension) and Path Z (variants enter Pareto archive) remain Cycle 15+ canonical-write candidates per my 2026-05-29 surface note § 3 caveat 2. Path X alone is sufficient for wave-5 closure coherence; the broader architectural decisions can land at their natural cadence.

---

## 5. Composition with cumulative Disc #42a Instance 6 framing

Per my 2026-05-29 surface note § 4, this issue was provisionally classified as Instance 6 #5 (Phase 4 → Phase 5 disjoint population). The wave-close canonical write (jack-ryan) should now resolve the classification:

- **If wave-close closes with Path X landed**: classify as Instance 6 #5 (architectural-parallelism-with-implementation-gap; resolved at code level via Path X during swift-closure execution; Disc #42a framing-audit application worked as intended — pre-fire empirical inspection caught the gap before fire)
- **The framing-audit performed by star-lord at Gate (c) is itself a Disc #42a Instance 6 confirmation**: pre-fire gate caught the framing assumption (recognition § 4.2 structural-integrity presumption) before execution could fire against the unresolved structural condition. This is exactly the discipline pattern Disc #42a was authored to produce.

This composes with the recognition record's § 3.1 Disc #41 amendment candidate observation: substrate-led discipline applies at multiple layers; the same empirical-rigor standard. Star-lord's Gate (c) surface is a working example of Disc #42a operating at exactly the validation gate where the recognition record's framing presumption interfaced with empirical code state.

---

## 6. What this verdict does NOT do

- Does NOT amend the recognition record. The recognition record's § 4.2 structural-integrity preservation language is correct as-written; this verdict clarifies its scope (structural integrity at the inter-phase consumption contract was presumed; the presumption must be empirically honored before the swift-closure path completes).
- Does NOT resolve the Wave B election. Wave B / Path Y / Path Z remain Cycle 15+ architectural canonical-write candidates. Path X is the only structural fix required for wave-5 coherence.
- Does NOT amend Disc #41 substrate-led discipline. The Disc #41 amendment candidate at recognition § 3.1 stands independently; jack-ryan ratifies at appropriate gate.
- Does NOT amend Phase 5 cohesion judge methodology. Methodology preserved per recognition § 4.2 and per star-lord dispatch § 2.2.
- Does NOT change PROVISIONAL marker schema design. Star-lord retains seam authority on schema details (per dispatch Q1).
- Does NOT block gamora seam-owner framing in general. The separability framing is correct for the broader architectural decisions; this verdict scopes its mis-application to Gate (c) specifically.

---

## 7. Sign-off

**Verdict:** Option 2 — Path X structural fix required before star-lord cohesion judge fires.

**Empirical-criterion gate for Path X completion**: code-level fix at `wave5_season_orchestrator.py:825-836` + smoke test confirming Phase 5 PM-1 input identical to Phase 4 archive (n=34, matching kit_id set) + BC-axis coverage smoke (8-element coverage preserved post-Path-X).

**KR next action**: author sequenced rocket/gamora Path X dispatch; coordinate empirical-criterion gate verification; re-engage star-lord with confirmation post-Path-X-land.

**Authority preserved**: recognition record § 4.2 structural-integrity preservation language; star-lord Gate (c) framing-audit surface as Disc #42a Instance 6 confirmation; gandalf 2026-05-29 surface note § 3 Path X lean; gamora seam separability framing on the broader architectural decisions (Wave B / Y / Z); Matt last-resort escalation reserved.

**Composition**: this verdict is a Pattern A-deep design-intent verdict per gandalf OP § 4; commits locally per CLAUDE.md auto-commit addendum; no push (gate honored).

**Commit reference** (to be appended post-commit): TBD
