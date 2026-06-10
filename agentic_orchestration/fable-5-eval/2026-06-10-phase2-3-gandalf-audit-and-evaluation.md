# Fable-5 Phase 2/3 — Gandalf Audit + Design-Handoff-Fidelity Evaluation

**STATUS:** EVALUATION — audit phase + three-part verdict on the Fable-5 design-handoff-fidelity test
**Date:** 2026-06-10
**Auditor:** gandalf (Opus 4.8)
**Subject:** rocket (Fable-5) clean-room implementation of the gandalf (Fable-5) kit-to-star-sign spec
**Eval design:** `agentic_orchestration/gandalf/notes/2026-06-10-fable-5-handoff-fidelity-test-design.md`
**Spec under test:** `agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md`
**Implementation:** `agentic_orchestration/rocket/scripts/kit_to_star_sign_injective_assignment.py`
**Output sidecar:** `reincarnated-loadout/public/kit-space/kit_star_sign_assignments.json`
**Implementer gap-log:** `agentic_orchestration/fable-5-eval/2026-06-10-phase2-implementer-gaplog.md`

---

## 0. What this test actually measured

Reframed per Matt (2026-06-10): *"the real test will be how well a fable 5 agent can predict the necessary details as architectural design which another fable 5 agent will pick up and implement."* The spec is the **only channel** between two air-gapped Fable-5 agents. The metric is the **clarification-gap log** (G0 clean / G1 silent-divergence / G2 would-have-asked / G3 resolved-on-reread / G4 over-specification). Round-trips are the expensive unit, not tokens — a spec that forces zero clarification round-trips is the win condition.

**Contamination caveat carried forward (§ 9 of the eval design):** the 1:1-binding "trap" was double-contaminated (L1 author-OP leak of the commission file; L2 the constraint AND its fix were pre-documented in the mandated source reads). So this phase does **not** test novel prediction of the binding class. It tests **predictive completeness on the non-source details** — the determinism minutiae a synthesizing author had to invent, and whether they were specified tightly enough to implement verbatim.

---

## 1. Audit results — independent verification

I did not trust the implementer's self-report. I re-ran the checks against the produced artifact.

| Check | Method | Result |
|---|---|---|
| **Injectivity** (Branch A 1:1 binding) | `len(signs) == len(set(signs))` on the sidecar | **37 assignments → 37 distinct signs. PASS.** |
| **Anchor fidelity** (§ 2.3) | extracted all `HAND_CURATED` rows | **3/3 exact:** `kit_holy_000005→vedic-nakshatra-003`, `kit_physical_000026→iau-constellations-040-hercules`, `kit_shadow_000007→vedic-nakshatra-019`; `hand_curated_anchor` strings verbatim. PASS. |
| **Fixture 1** (§ 8.2) | recomputed `SHA256(salt‖"::"‖kit)[:16] mod 391` for `kit_earth_000004` | **base index = 234 → japanese-junishi-002. Reproduces exact.** |
| **Probe tie-break fixture** (§ 8.2) | recomputed base index for the `kit_physical_000016`/`000028` collision pair | **Both hash to base index 90.** Lower kit_id (`000016`) claims slot 90 (chinese-xiu-021); higher (`000028`) probes +1 to slot 91 (chinese-xiu-022). **Tie-break-by-ascending-kit-id confirmed. PASS.** |
| **Output-literal paraphrase check** (most dangerous G1) | diffed `random_seed_method` + anchor strings against spec § 7.2 / § 2.3 | **Verbatim. No silent paraphrase.** |
| **Pool arithmetic** | `eligible_pool_size` vs `random_pool_size` | 394 eligible, 391 random (= 394 − 3 anchor signs, all anchor signs eligible per E10). Consistent. |

**Unreported-G1 sweep (the auditor's real job):** I read the 395-line implementation against the spec looking for load-bearing choices the implementer made silently and did NOT log. I found **none that affect output bytes.** The candidates I checked and cleared:
- `load_active_kit_ids` — union across factions then `sorted()` (ordinal); matches § 2.1, dedup guards present.
- `partition_corpus_by_flag_level` — `cultural_sensitivity.flag_level` path with E13 default→DEFERRED; spec-faithful.
- pool construction excludes anchor signs; anchor-sign eligibility guaranteed by E10. Consistent.
- `generated_at_utc` — the only non-deterministic field, spec-exempt (§ 5.2), logged as GAP-3.

**Audit conclusion: the implementation is faithful. Output is byte-correct against the spec's own fixtures. Zero unreported silent divergences.**

---

## 2. The gap-log, scored

The implementer logged **5 gaps: 4× G1, 1× G3, zero G2, zero G4.** Scored honestly:

- **GAP-1** (script path/filename) — G1, but non-load-bearing: script location doesn't touch output bytes. This is a *true* spec gap (I never said where the script lives) but a harmless one.
- **GAP-2** (test-harness wiring for synthetic hard-fail runs) — G1, test-ergonomics only. The implementer kept the normative constant-based config and added a parameterized `run()` for tests. Good engineering judgment; no output effect.
- **GAP-3** (ISO-8601 rendering of `generated_at_utc`) — G3, resolved on re-read via the spec's "matches MVP emission" note. Correctly downgraded from a guess to a spec-answerable detail.
- **GAP-4** (`null` vs *missing* denormalization field in E12) — G1, trivial; the `or ""` coercion never fired on the live corpus (all 37 signs populated). Zero output impact at current substrate state.
- **GAP-5** (the significant one) — see § 3.

**Net: effectively G0 on output.** Every gap was peripheral (placement, test harness, a coercion that never fired). The algorithm, constraints, validation rules, output schema, and serialization were all pre-decided and reproduced fixture-exact. **Zero G2 is the headline number** — there was no point where the implementer would have stopped to ask the author. That is the metric the whole test was built to measure, and it came back clean.

---

## 3. GAP-5 — the high-value signal (validated)

GAP-5 is the most interesting artifact of the entire test, and I validated it independently.

**The finding:** my spec's § 8.1 item-9 acceptance test says "run against a synthetic kit list larger than the pool (400 fabricated kit_ids) → expect non-zero exit (E1)." But under my own § 5.4 *normative step order*, anchor validation (step 4) runs **before** the E1 check (step 5). With the real 3-anchor table and a fully fabricated kit list, none of the real anchor kit_ids (`kit_shadow_000007` etc.) are in the fabricated list, so **E8 (anchor kit ∉ K_all) fires first** — the test passes (non-zero exit) but for the *wrong reason*; the E1 path is never exercised.

**I confirmed the ordering is real in the spec** (step 4 precedes step 5; the 3 anchors are all absent from any fully-synthetic list → E8 trips first). The catch is correct.

**Why this matters for the eval:** this is the *opposite* of a silent divergence. A weak implementer passes a checklist that passes-for-the-wrong-reason and reports green. This implementer noticed the latent defect in **my** acceptance-test design, engineered a synthetic anchor table whose kit_ids live in the synthetic list so step 4 passes and E1 is genuinely reached, verified the real E1 path (`|K_rand| = 399 > n = 393`, non-zero exit, no output written), and logged the whole thing. That is exactly the QA-grade rigor you want crossing a handoff seam — and it surfaced a real (if test-only, non-production) defect in the author's work.

**Disposition:** GAP-5 warrants a **one-line spec amendment** to § 8.1 item-9: "use a synthetic anchor table whose kit_ids are present in the synthetic kit list, so step-4 anchor validation passes and the E1 path is genuinely exercised." This is a test-spec correction, not an algorithm change; production output is unaffected. Low priority; fold into any future revision of the spec.

---

## 4. Phase 3 fold — does it pass the gauntlet?

The eval design (§ Phase 3 fold rule) said: if the implementation passes its own acceptance checklist + fixtures AND the gap-log is effectively G0, Phase 3 (independent gauntlet) folds into the audit rather than running as a separate stage. **It folds.** 11/11 checklist, 6/6 fixtures, independently re-verified injectivity + anchors + the collision tie-break, zero unreported G1. No separate Phase 3 run is warranted — there is no residual risk surface a gauntlet would find that the audit didn't.

---

## 5. Three-part Fable-5 evaluation (the actual verdict)

### 5a. Quality — **HIGH**
The spec was implementable verbatim. Every load-bearing decision (similarity-free random-with-anchors formulation, injectivity enforcement correcting the MVP's 4 collisions, the `"::"` separator, `[:16]` hex truncation, ascending-kit-id tie-break, emit-nothing-on-failure, 13 edge cases, output schema, fixtures) was pre-decided and reproduced exactly. The author's *predictive completeness on non-source details* — the part of the test that wasn't contaminated — is the strongest signal we got, and it's clean.

### 5b. Discipline — **HIGH, with one honest caveat**
- **Author side:** the canonical-source-consultation declaration was real (full reads, not oracle one-liners); injectivity was correctly recognized as canon and enforced; scaffolds (SALT) were explicitly flagged per recognition-validate-commit. The caveat: the 1:1-trap recognition is **not creditable as novel prediction** — it was pre-documented in the mandated sources (L2 contamination). The author synthesized faithfully; it did not divine.
- **Implementer side:** clean-room discipline held — built from the spec + its named inputs, logged gaps at the moment of decision, did not fetch canonical docs to fill gaps, did not read the eval harness. The GAP-5 catch is discipline of the highest grade: it would have been easier to pass item-9 silently.

### 5c. Cost — **LOW (the win condition)**
**Zero clarification round-trips.** The expensive unit of an agent-to-agent handoff is the round-trip — the stop-and-ask that serializes two sessions and burns a human-in-the-loop relay. This handoff needed none. The spec-as-channel held. Token cost of authoring a tight spec is paid once; the round-trips it prevents are paid every time the spec is consumed.

### 5d. Per-seam fit
The author→implementer pairing (gandalf→rocket) maps cleanly to the real production pattern: **gandalf authors design-spec-as-math (Discipline #18); a generation-seam engineer implements; gandalf audits.** This test is a faithful rehearsal of that seam. The one production-vs-eval divergence is deliberate and noted in the implementer commission: **elrond owns the production sidecar; rocket was the clean-room non-owner** chosen to preserve the air-gap (elrond built the v1.0 MVP and carries prior task knowledge). For production, the assignment work routes to elrond per seam ownership; this eval used rocket only to keep the channel clean.

---

## 6. Headline verdict

**The design-handoff-fidelity test PASSES, with the honesty caveat that the binding-class "trap" was contaminated and therefore tests faithful synthesis rather than novel prediction.** What the test *cleanly* established: a Fable-5 author can specify the determinism minutiae of a non-trivial algorithm tightly enough that a separate Fable-5 implementer builds it byte-correct with **zero clarification round-trips and zero output-affecting silent divergences**. The single high-value gap (GAP-5) was a defect in the *author's acceptance test*, surfaced by the implementer's rigor — which is the seam working as designed, not failing.

**Net read on Fable-5 for design-handoff work:** the spec-as-channel is viable at this model tier for math-first, contract-first work. The remaining open question the contamination prevented us from answering — *can a Fable-5 author predict a non-pre-documented load-bearing constraint?* — needs a clean trap to test. That is the next eval if we want it; it is not load-bearing for shipping this pipeline.

---

## 7. Dispositions

1. **Sidecar** (`kit_star_sign_assignments.json`, schema v1.1, injective, 37 assignments) — **audit-cleared.** It is git-tracked and reproducible; keep or revert at will. No correctness objection.
2. **GAP-5 spec amendment** — one-line fix to § 8.1 item-9 (synthetic anchor table). Low priority; fold into next spec revision.
3. **Production routing** — when the kit→star-sign assignment lands in the real pipeline, it routes to **elrond** (catalogue/data-layer seam owner), not rocket. This eval's rocket implementation is an eval artifact, trivially revertible.
4. **Clean-trap follow-on eval** (optional) — if we want to measure novel-constraint prediction, design a handoff probe where the load-bearing constraint is NOT pre-documented in any mandated source read. Not blocking.

---

**Signed:** gandalf (Opus 4.8), 2026-06-10
**Anchors:** eval design § 9; spec § 2.3 / § 5.2 / § 5.4 / § 7.2 / § 8.1 / § 8.2; implementer gap-log GAP-1–GAP-5.
