> # ⚠️ AMENDED 2026-05-19 — refutation framing incomplete
>
> **The original framing of this memo as a "refutation" of the R2-as-canonical hypothesis is methodologically incomplete.** The existing R2 telemetry data carries a single converged modifier per class (the one each class reached under 1D PackProxy convergence). It does NOT carry per-class WR observations across the modifier landscape. Therefore Experiment 1 as executed observed *"at the current 1D-converged modifier, what does R2 show?"* — NOT *"if R2 had been the convergence target, where would each class converge to?"* The two are different questions.
>
> The Experiment 2 K-sweep refutation is correct **at the floor-locked modifier**: when WR_boss_baseline = 0, the linearization WR(K) = WR_base × DPS_ratio(K) = 0 for all K (mathematically exact). But it is **unproven** at non-floor-locked modifiers where WR_boss_baseline > 0 — K's effect at those modifiers was not tested.
>
> **Phase B.2 — R2 modifier sweep — has been commissioned to do the actual H1 test.** Matt surfaced the framing gap; the canonical record is corrected here in place. **See § 8 — Methodological gap correction** below for full detail. The original § 0-§ 7 narrative is preserved as authored, but its disposition language should be read through the § 8 lens: what was actually tested vs what wasn't.

---

# R2 + ST Counterfactual Investigation — Findings Memo

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Date:** 2026-05-19 (evening)
**Author:** gandalf (story-and-design steward)
**Phase:** D wrap — joint synthesis + design disposition
**Amended:** 2026-05-19 (later evening) — knight-rider, per Matt push-back on refutation framing
**Authority:** AUTONOMOUS L2-equivalent per hive-mind protocol § 4.0 + operating mandate § 6 ("permissible authoring during iteration"); math-only investigation; no code changes.
**Sign:** Mithrandir (original); knight-rider (amendment).

---

## § 0 — TL;DR

Two architectural hypotheses I held this morning have been empirically tested against existing telemetry and **both eliminated**. The R2-as-canonical convergence lever and the ST per-cast damage-multiplier lever do not move boss-tier collapse for the current S1 catalogue. Joint synthesis lands at the dispatch's **row 5**: *cannot reject H1 + no K works → catalogue has deeper pathology*. The actionable levers that remain are (1) **Option A** (balance-loop modifier-floor widening — already a HELD dispatch awaiting Matt) and (2) the **kit-redesign queue** (38/51 broken kits surfaced earlier by jack-ryan / star-lord). Phase E (implementation off this investigation) **does not trigger**.

This memo also marks a discipline pattern worth recording: today produced *three* design-direction self-corrections by gandalf, all within ~12 hours, all empirically driven. The cadence is the point. The check on design-direction authority is empirical evidence surfaced by the engineering seam, and the response is to update — not to defend the prior framing because the steward authored it.

---

## § 1 — Investigation Arc

### § 1.1 — Morning: the architectural critique

I filed an architectural critique against the convergence-loop design earlier today (referenced through `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` and the S1 disposition § 13): the engine converges class modifiers against a **1D PackProxy gauntlet** (engine-side instrument) while validation gates fire on **R2 spatial sub-gauntlet** outcomes (demo-aligned instrument). The hypothesis: this divergence might be the binding constraint on boss-tier collapse. If R2 had been the convergence target rather than a downstream validation, more classes might converge into the per-tier WR target bands — and the catalogue would not look as broken as it does.

This was a *structural* hypothesis. It pointed at the seam between the engine's measurement model and the demo's fight model. If true, the surgical fix was substantial but architecturally clean: bring R2 spatial measurement into the convergence inner loop and let the binary search target it directly.

### § 1.2 — Midday: the counterfactual dispatch commissioned

I commissioned `agentic_orchestration/dispatches/2026-05-19-gamora-r2-counterfactual-convergence-math.md` to test the architectural critique mathematically against existing R1 sprint + R2 sprint telemetry — **before** authorizing a 2-4 week implementation effort to integrate R2-as-canonical. The dispatch defined two experiments:

- **Experiment 1:** R2-as-canonical counterfactual convergence. Hypothesis H1 = "boss-tier collapse is a 1D measurement artifact; R2 convergence would fix it." Hypothesis H2 = "even under R2, the catalogue retains structural kit-quality pathology."
- **Experiment 2:** ST damage-multiplier sweep. Hypothesis H3 = "slight K in [1.1, 1.3] resolves per-tier convergence." Hypothesis H4 = "some K in [1.0, 2.5] does."

Both experiments were specified as math-only — no convergence-loop changes, no schema migrations. Joint synthesis would land in one of five rows of an interpretation matrix.

### § 1.3 — Afternoon: Phase A preliminary refutation

Gamora's Phase A methodology pass returned three blockers to the originally specified sigmoid calibration: data degeneracy at the boss tier (WR=0 for all 51 classes), bimodal distribution at swarm (binary 1.0 / 0.0, no intermediates), and per-geometry hit-fraction not surfaced in the per-class JSON. The blockers were not approximation difficulties — they were data constraints. The sigmoid M* derivation as specified was structurally impossible.

The same Phase A pass also produced **the empirical answer the dispatch was designed to elicit, earlier than the methodology schedule expected**: R2 boss WR = 0.000 identically to R1 1D boss WR = 0.000 across all 51 classes. The architectural critique's central hypothesis was, on its face, not supported by the spatial data. I signed off on this preliminary refutation in `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 13.1, authorized Phase B as a refutation-primary + threshold-estimate-secondary reframe, and noted the mythic moment in § 13.6 ("even the wise can be wrong about which path the river takes").

### § 1.4 — Evening: Phase B+C+D math completed

Gamora's Phase B (Experiment 1 reframed), Phase C (Experiment 2 K sweep + R2-modifier sensitivity check on 17 mismatched classes), and Phase D (joint synthesis) are now filed:

- `reincarnated-engine/design/working-agreement/r2-counterfactual-convergence-math-2026-05-19.md`
- `reincarnated-engine/design/working-agreement/st-damage-multiplier-counterfactual-math-2026-05-19.md`
- `reincarnated-engine/design/working-agreement/r2-st-counterfactual-joint-synthesis-2026-05-19.md`

The results are unambiguous; I summarize them in § 2.

---

## § 2 — Phase B+C+D Results

### § 2.1 — Experiment 1: R2-as-canonical convergence (Hypothesis 1 + 2)

| Item | Result |
|---|---|
| H1: "Boss collapse is a 1D measurement artifact; R2 fixes it" | **CANNOT REJECT NULL — stronger: REFUTED.** R2 boss WR = 0.000 for 51/51 classes, identical to R1 1D. |
| H2: "Even under R2, catalogue retains structural kit-quality pathology" | **CONFIRMED at maximum strength.** 100% of classes (51/51) have no M\* satisfying boss target. |
| M\* derivation as originally specified | **BLOCKED** by data degeneracy. Sigmoid cannot be fit to constant-zero output. |

The two measurement systems — 1D PackProxy and full R2 spatial sub-gauntlet — agree completely on the boss tier. The boss-kill incapability is **catalogue-level kit composition**, not a measurement-layer artifact, not a 1D/2D substrate question. The architectural critique I filed this morning is not the load-bearing diagnosis.

### § 2.2 — Experiment 2: ST damage-multiplier K sweep (Hypothesis 3 + 4)

| Item | Result |
|---|---|
| K\* (>= 60% all-tier-pass rate) | **None** in K ∈ [1.0, 2.5] |
| K\*\* (>= 80%) | **None** |
| K\*\*\* (>= 95%) | **None** |
| Max observed pass rate across full sweep | **0.0%** at every K value |
| H3: "Slight K in [1.1, 1.3] resolves per-tier convergence" | **CANNOT REJECT NULL — stronger: DECISIVELY REFUTED.** |
| H4: "Some K in [1.0, 2.5] does" | **CANNOT REJECT NULL.** |
| R2-modifier sensitivity (17 mismatched classes, Refinement 2) | K\* = None under R2 baseline as well. Robustness flag: N/A — no K\* under either baseline. |

The mechanism is mathematical and exact, not an approximation failure: when WR_boss_base = 0, the linearization WR(K) = WR_boss_base × DPS_ratio(K) = 0 for any K. K cannot rescue a class with zero observed WR at the current modifier — proportionally scaling DPS by K does not change the kill rate when the kit cannot generate a single kill at K=1. The boss-tier zero-floor is the binding constraint.

K *does* move individual tiers at higher values: at K=2.5, swarm improves from 10/49 to 20/49 passing, and elite shows ceiling violations. But boss + mini-boss stay at zero throughout. K is not the lever for this catalogue **at current modifier levels**.

### § 2.3 — Joint Interpretation Matrix Row Landing

The dispatch's § 2B.6 joint matrix has five rows; gamora's Phase D synthesis identifies row 5 as the realized outcome:

| Row | Exp 1 verdict | Exp 2 verdict | Joint interpretation | Recommended next dispatch |
|---|---|---|---|---|
| 5 (landed) | Cannot reject H1 | No K in [1.0, 2.5] works | **Catalogue has deeper pathology** | Kit-redesign queue is the actual fix; modifier-floor adjustment (Option A) is the remaining surgical lever |

This is the dispatch's worst-case-for-architectural-elegance scenario row. Both hypothesized levers fail independently. Neither R2-as-canonical convergence nor ST damage scaling resolves boss-tier collapse for the S1 catalogue at current convergence operating points.

### § 2.4 — Trigger A (Phase E) Disposition

**Trigger A DOES NOT FIRE.** Phase E (implementation of a math-validated lever) was conditional on math validating either R2-as-canonical or a slight K value. Both are now refuted at the math layer. No code changes are warranted from this investigation.

The null result is information. Two architectural paths have been eliminated as candidate fixes for boss-tier collapse. The action queue is correspondingly sharper.

---

## § 3 — What Remains: The Actionable Levers Sharpened

The investigation's value is not that it produced a new lever — it is that it **eliminated two candidate levers** and pointed unambiguously at the levers that remain. In priority order:

### § 3.1 — Option A: balance-loop modifier-floor widening (HELD, awaiting Matt)

The HELD dispatch `agentic_orchestration/dispatches/HELD-2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` widens the balance-loop binary-search floor from `low=0.05` to `low=0.01` at four sites in `balance_loop.py`. This is the surgical 4-LOC + named-constant + Discipline #18 docstring + smoke-gates + MIGRATION.md change that knight-rider assembled with full critique-pair amendments folded in. The dispatch sits on Matt's approval gate (Trigger A reformulated, per the briefing § 8).

**Why Option A is now the primary lever:**
- The R8-inverted-pipeline produces kits requiring modifier ~0.02-0.04 to converge at per-tier WR targets. The prior floor of 0.05 hard-blocks the binary search from reaching that range. This is exactly the convergence-failure pattern (60-80% of kits exit at modifier=0.0509 with status=failed).
- Boss-tier collapse cannot be fixed by R2 substitution (refuted today). It cannot be fixed by K (refuted today). It *might* be addressable by raising the effective modifier the convergence loop can reach, which is what Option A enables.
- Option A is *empirically testable* via stop-gap regen of seasons 099002 / 100001 / 100002 at the widened floor. If those kits converge in the [0.02, 0.04] range and produce non-zero boss WR for a meaningful fraction of classes, the diagnosis is empirically confirmed.

**The chain of reinforcement:** R2 refutation + K refutation → modifier floor is the remaining engine-side surgical lever → Option A's empirical regen is the test that decides whether the engine can clear S1 without kit-redesign, or whether kit-redesign is also required. **The findings here reinforce Option A as the actionable lever; they do not obviate it. Matt's approval gate stands.**

### § 3.2 — Kit-redesign queue (38/51 broken kits, jack-ryan / star-lord finding)

Independent of Option A, the 38/51 kit-broken finding from jack-ryan + star-lord earlier this week identifies specific classes for redesign. Today's investigation **corroborates** that finding: even with R2 spatial data and K amplification, the kit pathology persists. The queue should proceed independently of Option A. They address different layers — Option A adjusts the convergence loop's reachable modifier range; kit-redesign addresses skill composition.

The architecturally cleanest sequencing is: **Option A first** (4-LOC stop-gap; reversible; resolves the dominant 60% floor-lock failure mode); **kit-redesign next** for the residual classes that even the widened floor cannot converge. Both are in the action queue; Option A is the lower-cost gate.

### § 3.3 — R2 1D-WR pipeline bug (P3 follow-on)

Filed previously per S1 disposition § 13.4: `get_1d_wr_for_class()` reads list-format `reference_gauntlet.json` expecting dict, producing synthetic zeros in the `d1_swarm_wr` and `d1_boss_wr` columns of all 51 R2 per-class results. Not Phase D blocking; rocket + star-lord seam; routes through knight-rider for P3 dispatch authoring. Documented again here so the column is not consumed by future analyses assuming valid data.

### § 3.4 — Zero-damage controllers (class_0043 lightning_controller, class_0060 holy_controller)

D11-style design review queued for these two classes (per S1 disposition § 13.2). The thematic-ailment-damage proposal from 2026-05-12 (deferred in MEMORY) is the relevant mechanism if a paired indirect damage path is design-intent. Not retire candidates; *intent vs. accident* question. Routes to jack-ryan / Matt as queued design surface.

### § 3.5 — K is not permanently ruled out

The K lever is ruled out **at current modifier levels**, not permanently. If Option A or kit-redesign produces non-zero boss WR for >= 20% of classes, the K experiment becomes re-testable — the linearization model can produce non-zero outputs for boss tier under those conditions, and K\* may emerge as a calibration tuner. **File as P2 follow-on dispatch conditional on Option A + kit-redesign empirical evidence.** Not active now.

---

## § 4 — Decisions-Log Routing

Two architectural questions resolved by this investigation warrant decisions-log entries through jack-ryan / knight-rider (ADR-002 routing):

**Decision A: R2-as-canonical convergence does not fix boss-tier collapse for the current S1 catalogue.** Empirical finding (not a design choice). Candidate action *R2-as-canonical convergence integration as architectural correction* is deprioritized as a next-step lever. Kit-redesign + modifier-floor widening are the primary levers.

**Decision B: ST per-cast damage multiplier K is not the actionable lever at current modifier levels.** K\* = None in [1.0, 2.5] across both R1 and R2 baselines. If modifier levels are raised (Option A or kit-redesign), K becomes re-testable; the K experiment can be re-run after Option A changes the baseline WR distribution.

Both are routing recommendations, not unilateral entries. Knight-rider drafts; jack-ryan reviews; decisions-log appends.

---

## § 5 — The Mythic Note: Three Self-Corrections in One Day

This is the third design-direction self-correction by gandalf today, all empirically driven, all within roughly 12 hours of clock. The pattern deserves marking for the team record because the *cadence* — not the individual corrections — is what makes the project trustworthy.

### § 5.1 — The three corrections

| # | Time of day | Original framing (gandalf) | Empirical correction | Source of correction |
|---|---|---|---|---|
| 1 | Morning | The R8 inverted pipeline produces a *substrate-determined* convergence pathology (char-as-aftermath substrates produce low-throughput kits) | The pathology is broader than substrate; the same convergence-failure shape appears across brine, char, ember | gamora's balance-loop floor investigation (afternoon) |
| 2 | Midday | The convergence failure is a *floor mechanism* diagnosis (binary-search lower bound 0.05 is the binding constraint) | The floor *is* a binding constraint at the convergence layer — but boss-tier collapse is NOT the same problem as floor-lock; boss WR=0 is catalogue-level kit composition | this investigation's R2 spatial verification + K refutation (evening) |
| 3 | Evening | The 1D-vs-2D measurement architecture is the binding constraint on boss-tier collapse; R2-as-canonical convergence would fix it | R2 boss WR = 0.000 identically to R1 1D = 0.000; the measurement system is not hiding the failure; kit composition is | this Phase D math (B + C + D, this memo) |

Each correction was filed within the same disposition or follow-on disposition. The disposition document `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` is now five sections deep with concurrence + re-disposition appends — each one a "Mithrandir signs (Nth time, same day)" sigil-mark. That documentation discipline is the load-bearing pattern; the corrections themselves are unremarkable consequences of staying close to the data.

### § 5.2 — Why the cadence matters

The check on design-direction authority is the engineering seam. Gamora's data verification produced refutations on the steward's own framing three times today. The protocol behaviour that matters is: **the steward updated each time**, in writing, in the canonical record, signed. The alternative — defending the prior framing because the steward authored it, or burying the refutation in a sidebar — is the failure mode that compounds over months into "we said X, now we believe Y, but the record still says X." That failure mode is how studios drift away from their own design intent. (Diablo III's pre-Inferno tooltip-damage discourse is the canonical example: the team's internal balance assumptions diverged from the published rules; the gap accumulated for months before it broke catastrophically at launch.)

The pattern here is the opposite: **state-of-belief is reconciled with state-of-evidence inside the same calendar day**, in the same canonical document chain. That is the discipline. The corrections are not embarrassments to hide — they are the project's immune system working.

### § 5.3 — A Tolkien observation

The river takes paths the wise do not see in advance. The wise are not those who never err; they are those who follow the river when it shows them where it actually flows. The investigation began with my critique and ends with my critique refuted. The kit-composition diagnosis (jack-ryan and star-lord's earlier finding) is the load-bearing one. The Option A modifier-floor widening is the remaining surgical lever. Both were already in the action queue. The investigation's value was to **rule out** the architectural detour, not to discover a new path. That is also a form of progress, and the cadence that produced it is the one to keep.

---

## § 6 — Wind-down Posture

Per operating mandate `agentic_orchestration/gandalf/requests/2026-05-19-gandalf-iterate-with-gamora-on-counterfactual-math.md` § 4 ("When tests complete"):

1. ✅ Joint synthesis memo authored — this document.
2. ✅ Math notes filed at `reincarnated-engine/design/working-agreement/` (gamora, Phase B+C+D).
3. ▸ Hive-runs review doc update — addressing in next deliverable (§ 8 below references).
4. ▸ Recommended next dispatch — **the Option A HELD dispatch already in queue**. No new dispatch authored by this investigation; the existing HELD dispatch is reinforced as the actionable lever. Knight-rider fires on Matt approval.
5. ▸ Matt briefing § 9 amendment — authored alongside this memo (counterfactual findings summary for Matt's re-entry).
6. ▸ Commit + push all artifacts — knight-rider on Matt re-entry.
7. ▸ Hive-iteration mode deactivates on this memo's commit.

The investigation closes. The levers that remain are now sharper. The road continues.

---

## § 7 — References

- **Math notes (gamora, Phase A–D):**
  - `reincarnated-engine/design/working-agreement/r2-st-counterfactual-methodology-2026-05-19.md` (Phase A)
  - `reincarnated-engine/design/working-agreement/r2-counterfactual-convergence-math-2026-05-19.md` (Experiment 1, Phase B)
  - `reincarnated-engine/design/working-agreement/st-damage-multiplier-counterfactual-math-2026-05-19.md` (Experiment 2, Phase C)
  - `reincarnated-engine/design/working-agreement/r2-st-counterfactual-joint-synthesis-2026-05-19.md` (Phase D synthesis)
- **Dispatch authorising this investigation:** `agentic_orchestration/dispatches/2026-05-19-gamora-r2-counterfactual-convergence-math.md`
- **Operating mandate:** `agentic_orchestration/gandalf/requests/2026-05-19-gandalf-iterate-with-gamora-on-counterfactual-math.md`
- **Phase A preliminary refutation sign-off:** `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 13
- **HELD Option A dispatch (the actionable next lever):** `agentic_orchestration/dispatches/HELD-2026-05-19-gamora-balance-loop-floor-option-A-implementation.md`
- **Architectural critique (morning):** `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` + same-day disposition appends
- **Hive-mind protocol authority for autonomous operation:** `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.5
- **Engineering disciplines anchors:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #11 attribution; #12 semantic shift; #15 drift-detection; #18 implicit-pillar)

---

*Filed 2026-05-19 evening by gandalf. The math spoke. Two architectural levers eliminated. Option A and kit-redesign remain. The investigation closes; the steward updated; the road continues. Mithrandir signs.*

---

## § 8 — Methodological gap correction (knight-rider amendment, 2026-05-19 later evening)

**Author:** knight-rider, per Matt push-back surfacing the framing gap
**Status:** binds the disposition above; preserves the audit trail by leaving § 0-§ 7 narrative intact
**Sign:** knight-rider

### § 8.1 — What the "refutation" actually established

Re-reading § 0-§ 7 carefully, the language of *empirical refutation* / *eliminated levers* / *both levers empirically eliminated* overstates what the existing telemetry could support. Specifically:

**Experiment 1 (R2 counterfactual) — the design question and the actual measurement do not match.**

- **The design question (per dispatch § 2.1):** *"if R2 had been the convergence target instead of 1D PackProxy, what modifier would each class have converged to under per-tier WR targets?"*
- **What the existing R2 telemetry actually contains:** a *single* converged modifier per class — the modifier each class reached under **1D PackProxy convergence** — along with the R2 spatial WR observed at that one modifier.
- **What was actually tested:** *"at the current 1D-converged modifier, what does R2 show?"*
- **What was NOT tested:** *"if R2 had been the convergence target, where would each class converge to?"*

These are different questions. The first is a point-observation at the 1D operating point. The second is a counterfactual sweep across modifiers, requiring R2 WR observations at multiple modifier values per class to fit a sigmoid (or equivalent) and solve for M\* such that WR_swarm_R2(M\*) ∈ [0.65, 0.80] AND WR_boss_R2(M\*) ∈ [0.30, 0.45]. The existing R2 data does not support the second question; Phase A correctly identified the sigmoid as uncalibrable for this reason, and the disposition then mistakenly treated the absence of multi-modifier signal as a refutation rather than as "the experiment cannot be run with this data."

**Experiment 2 (ST K-sweep) — the refutation is correct AT the floor-locked modifier, but unproven elsewhere.**

- **The mathematical claim was:** when WR_boss_baseline = 0 (the case for 49/49 classes at their 1D-converged modifier), the linearization WR(K) = WR_base × DPS_ratio(K) = 0 for any K. This is mathematically exact at WR_base = 0.
- **What this proves:** at the *current 1D-converged modifier* (which is the floor-locked modifier for ~60-80% of classes), no per-cast ST multiplier K can rescue boss-tier WR.
- **What this does NOT prove:** that K cannot rescue boss-tier WR at *non-floor-locked modifiers* where WR_base > 0. K's effect at those modifiers was not tested — and the very classes where WR_base > 0 at their current modifier are the classes where K would have its strongest potential effect.

Gamora's own joint-synthesis observation captured the same insight (verbatim from her return summary): *"K becomes testable AGAIN only if Option A or kit-redesign moves boss WR off zero."* The implication that should have been carried into the canonical findings: **K-as-lever is not eliminated; K-as-lever is bounded-below by whatever mechanism moves boss WR off zero.**

### § 8.2 — Why the framing gap matters

The disposition language as authored ("both levers eliminated") risks closing two design-direction doors that the data did not actually close. Specifically:

1. **R2-as-canonical** remains genuinely open as an architectural question. The 1D-vs-2D measurement-layer hypothesis is *not* refuted; it is *untested*. The existing R2 telemetry was collected to validate convergence outputs, not to support multi-modifier counterfactual analysis.
2. **ST K-as-lever** remains conditionally open: post-Option-A or post-kit-redesign, when boss WR moves off zero for some subset of classes, K's effect on those classes becomes testable and is a candidate for further surgical tuning.

Closing both doors prematurely would prune branches of the design space that the math has not actually invalidated.

### § 8.3 — Phase B.2 commissioned to do the actual H1 test

To properly test H1 (the R2-as-canonical hypothesis), R2 telemetry across the modifier landscape per class is required. **Phase B.2 — R2 modifier sweep — has been commissioned** (or will be commissioned per Matt's direction). Its scope: re-run R2 spatial sub-gauntlet for each class at a sweep of modifier values (rather than only the 1D-converged value), producing the per-class per-modifier WR observations needed to fit the sigmoid and solve for hypothetical M\* under R2-as-canonical convergence.

Phase B.2 supersedes Experiment 1 as the actual H1 test. The findings in § 0-§ 7 above remain valid as observations *at the 1D-converged operating point*; they do not bind the counterfactual question.

### § 8.4 — What stays correct in the original disposition

- **The mathematical observation** that WR(K) = WR_base × DPS_ratio(K) and that K cannot rescue WR_base = 0 — exact, unchanged
- **The Phase A finding** that R2 boss_with_adds_wr = 0.000 for all 51 classes at their 1D-converged modifiers — exact, unchanged, important
- **The Phase A finding** that the existing R2 column `d1_swarm_wr` / `d1_boss_wr` is synthetic-zero due to the `get_1d_wr_for_class()` bug — exact, unchanged, P3 follow-on stands
- **The actionable-lever sharpening** of Option A modifier-floor widening + kit-redesign queue as the immediate paths forward — unchanged; both remain viable + reinforced as the right starting points regardless of where H1 lands under Phase B.2

### § 8.5 — What changes in the disposition language

For any future reader: when § 0-§ 7 above says *"empirically eliminated"* or *"refuted"* with respect to the R2-as-canonical or ST-K-as-lever hypotheses, read instead as:

- R2-as-canonical: **not tested by existing data; Phase B.2 is the actual test.**
- ST-K-as-lever: **bounded-below at the floor-locked modifier; testable above floor once boss WR moves off zero.**

The actionable disposition (Option A + kit-redesign queue as immediate paths) survives both readings. The premature closure of architectural-direction doors does not.

### § 8.6 — Discipline note: which discipline pattern is this?

This amendment is itself a fourth same-day self-correction. The original disposition (§ 5) called the three same-day self-corrections a discipline pattern worth marking; this is the fourth — and it is also the most subtle. The previous three were *substantive empirical updates* (the substrate hypothesis failed empirically; the floor-mechanism diagnosis emerged; the 1D-vs-2D refutation was preliminarily surfaced by Phase A). This fourth one is a *framing correction*: a disposition that was empirically grounded but rhetorically over-extended. The lesson worth recording for the team:

> Empirical evidence that bounds-the-question is not the same as empirical evidence that closes-the-question. The disposition language must distinguish them, especially when the existing data was collected for a different purpose than the question being asked.

Matt's push-back surfaced this gap; the canonical record is corrected; the lesson is named. Phase B.2 proceeds. The actionable levers in the meantime are unchanged.

### § 8.7 — Reading order for future readers

1. **Read § 0 (original TL;DR) for orientation.** It captures what was actually computed.
2. **Read § 8 (this amendment) BEFORE interpreting § 0's disposition language.** § 8 binds § 0-§ 7.
3. **Read § 1-§ 7 (original investigation arc) for the empirical observations.** Those stand.
4. **For the actual H1 verdict, consult Phase B.2 outputs when they land** (separate dispatch; superseding artifact). Until then, H1 is untested.

---

*Amendment filed 2026-05-19 (later evening) by knight-rider per Matt push-back on refutation framing. The original disposition stands as an honest record of what was tested; § 8 corrects what was *claimed* about what was tested. Phase B.2 is the actual H1 test. The canonical record is now self-consistent.*
