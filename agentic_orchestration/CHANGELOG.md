# CHANGELOG — Reincarnated synthetic engineering team

This log records **team-level events** — agent additions, ADR additions/amendments, process changes, scope re-allocations. It does NOT log routine developer commits (those live in their respective git repos).

---

## 2026-05-19 (later evening) — AMENDMENT: R2+ST counterfactual refutation framing was overreach

**Event:** Matt push-back on the entry below ("Investigation COMPLETE") surfaced that the disposition language overstated what existing telemetry could support. The "both levers empirically eliminated" framing closed two architectural-direction doors that the data did not actually close.

**What was overstated:**

- **Experiment 1 (R2-as-canonical) was NOT TESTED.** The existing R2 telemetry carries a single converged modifier per class — the one each class reached under 1D PackProxy convergence. It does NOT carry per-class WR observations across the modifier landscape. The investigation observed *"at the 1D-converged modifier, what does R2 show?"* — NOT *"if R2 had been the convergence target, where would each class converge to?"* The latter requires multi-modifier R2 data per class to fit a sigmoid and solve for hypothetical M\*. Phase A correctly identified the sigmoid as uncalibratable; the disposition then mistakenly treated absence-of-multi-modifier-signal as refutation rather than "the experiment cannot be run with this data."

- **Experiment 2 (ST K-sweep) refutation is correct AT the floor-locked modifier, but UNPROVEN above.** When WR_boss_baseline = 0, the linearization WR(K) = WR_base × DPS_ratio(K) = 0 for any K (mathematically exact). But the very classes where WR_base > 0 at their current modifier — including any class converging above the floor — are exactly where K would have its strongest potential effect, and K's effect at those modifiers was not tested. K-as-lever is not eliminated; it is bounded-below by whatever moves boss WR off zero.

**What stays correct in the original entry:** the mathematical observation about WR_base = 0; the Phase A finding that R2 boss_with_adds_wr = 0.000 for all 51 classes at their 1D-converged modifiers; the `get_1d_wr_for_class()` bug finding; the actionable-lever sharpening (Option A + kit-redesign queue remain the right immediate paths under either reading); the joint matrix row 5 interpretation insofar as it captures "at the 1D operating point" observations.

**What was commissioned to correct the gap:** **Phase B.2 — R2 modifier sweep.** Re-run R2 spatial sub-gauntlet for each class at a sweep of modifier values (rather than only the 1D-converged value), producing the per-class per-modifier WR observations needed to fit the sigmoid and solve for hypothetical M\* under R2-as-canonical convergence. Until Phase B.2 lands, H1 remains untested.

**Artifacts amended in place (audit trail preserved):**

- `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` — top banner + new § 8 ("Methodological gap correction") binding the disposition language in § 0-§ 7
- `agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html` — top banner + new Part 2.B.5.amend section + Decision #1 inline correction; document status bumped to v1.3
- This CHANGELOG entry

**Discipline pattern (fourth same-day self-correction):** the previous three same-day self-corrections were substantive empirical updates. This fourth is a *framing correction* — a disposition that was empirically grounded but rhetorically over-extended. The team lesson: *empirical evidence that bounds-the-question is not the same as empirical evidence that closes-the-question.* The disposition language must distinguish them, especially when existing data was collected for a different purpose than the question being asked.

**Trigger A queue impact:** unchanged. Option A modifier-floor widening remains the actionable next step under either reading of the counterfactual evidence. Matt's approval gate stands. The corrected disposition does not change Decision #1's recommendation; it sharpens the rationale for *why* Option A leads (it's the prerequisite that moves boss WR off zero, making K-as-lever testable for the subset of classes that would benefit).

---

## 2026-05-19 — R2+ST Counterfactual Math Investigation COMPLETE (gamora Phases B+C+D)

> **⚠️ AMENDED — see entry above ("AMENDMENT: refutation framing was overreach").** The "Investigation COMPLETE" language and the "both levers empirically eliminated" framing in this entry overstate what the data supported. Read this entry through the amendment lens. Specifically: "R2-as-canonical convergence would not have moved boss-tier collapse" is true *at the 1D operating point* but does not bind the counterfactual; the counterfactual is the question Phase B.2 actually tests.

**Event:** Gamora completed Phases B, C, and D of the R2+ST counterfactual math investigation commissioned by gandalf this morning and authorized in § 13.1 of the S1-firstbatch-fail disposition. Three math notes filed. Trigger A does not fire. Joint matrix row 5.

**Experiment 1 (R2 convergence counterfactual):** PRIMARY FINDING: R2 spatial boss WR = 0.000 identically to R1 1D boss WR = 0.000 for all 51 classes. R2-as-canonical convergence would not have moved boss-tier collapse for this catalogue. Matt's architectural critique ("tuning against 1D while gating on R2 is counterproductive") is not empirically supported; the spatial measurement replicates the same zero-kill-rate pathology as the 1D measurement. The kit-composition diagnosis is corroborated, not undermined. SECONDARY FINDING: R2 swarm WR is bimodal (38/51 WR=1.0, 13/51 WR=0.0); threshold between pass/fail is kit-composition-driven, not modifier-driven.

**Experiment 2 (ST damage multiplier K sweep):** K* = None. K** = None. K*** = None. All-tier-pass rate = 0.0% at every K in [1.0, 2.5] (31 values). Structural blocker: boss WR = 0.000 for 49/49 eligible classes. The linearization model WR(K) = WR_base * DPS_ratio(K) returns 0 for all K when WR_base = 0. Per-cast DPS scaling cannot rescue a zero-kill-rate tier at the current modifier floor.

**Sensitivity subsection (R2-modifier baseline for 17 mismatched classes):** K* = None under R2 baseline for all computable cases (same structural blocker). Robustness flag: N/A — no K* exists to characterize robustness of.

**Joint synthesis matrix:** Row 5 — "cannot reject H1 + no K works + catalogue has deeper pathology." Both hypothesized levers (R2-as-canonical + ST scaling) insufficient for current catalogue at current modifier levels.

**Trigger A:** DOES NOT FIRE. Phase E (ST multiplier implementation) does not proceed.

**Recommended next dispatches:** (1) Option A HELD dispatch for Matt approval (modifier floor adjustment); (2) Kit-redesign queue continuation (jack-ryan / star-lord); (3) P3 R2 bug fix `get_1d_wr_for_class()` (rocket + star-lord); (4) D11 design review for zero-damage classes (class_0043, class_0060).

**Math notes filed:**
- `design/working-agreement/r2-counterfactual-convergence-math-2026-05-19.md` (Experiment 1)
- `design/working-agreement/st-damage-multiplier-counterfactual-math-2026-05-19.md` (Experiment 2 + sensitivity)
- `design/working-agreement/r2-st-counterfactual-joint-synthesis-2026-05-19.md` (Phase D joint synthesis)

**Routing:** gamora → knight-rider → gandalf for Phase D final summary + Trigger A gate disposition.

---

## 2026-05-19 — VS2a S1 arc CLOSED at Trigger A — Option A balance-loop floor widening queued for Matt approval

**Event:** End-of-day wind-down by knight-rider at Matt "please wind down" re-entry. The autonomous VS2a S1 arc converged onto one queued decision after ~8 hours of work:

**Arc summary:** S1 first-batch (rocket; season_100001 char) PASSed cohesion (gandalf 4.83) but FAILed mechanics (gamora canonical R1 0/11 boss). Methodology-conflation audit (jack-ryan) refuted transposition hypothesis + named knight-rider's dispatch authoring as failure point of origin. Substrate-prior retry path tested with seed 100002 (ember PREFER-list) — also 80% floor-lock, weakening gandalf's substrate hypothesis. Knight-rider routed gandalf for re-disposition; gandalf took ownership of category error ("a cohesion-layer truth applied as a mechanics-layer prediction"), withdrew retries 2+3, pivoted to balance-loop floor-mechanism investigation. Gamora investigation diagnosed root cause: B14.5 V1 recompose trigger fires correctly but at modifier=0.0509 all kits win 98-100% → levers produce delta=0 → loop exits as `failed_regenerate`. Architectural failure mode: recompose's signal range [0.30, 0.70] is unreachable when floor=0.05 blocks the search. Recommended Option D (widen floor 0.05→0.01 now + re-condition recompose-trigger this week).

**Critique-pair concurrence #2:** gandalf CONCUR + structural amendment (stage A and B as separate Matt approvals); jack-ryan Gate 1 APPROVE WITH AMEND + 4 process amendments (diagnostic-only temporal gate, blocking test-assertion audit, MIGRATION.md required, smoke gate A4 prerequisite for B).

**Trigger A activation:** Matt briefing § 8 assembled with one-sentence framing + decisions-log text + 6 decision items + HELD implementation dispatch (all critique-pair amendments folded in; fire-on-approval). Path-a hand-redesign held in reserve. Retry-3 withdrawn.

**Bonus empirical:** retry-2 (re-fired under nohup polling) produced 11/11 (100%) convergence failures across 4 distinct failure signatures (floor-lock dominant ~60%; mid-stuck, ceiling-lock, severe-floor-lock minority). Third data point at >70% floor-lock across three substrates (char 72.7%, ember 80%, ember 100%). Substrate hypothesis empirically refuted.

**Team rhythm:** three critique-pair invocations in one day, all productive. Gandalf took explicit ownership of a category error (Mithrandir's "I did this to myself" in disposition § 9.8). Jack-ryan's audit traced back to knight-rider's dispatch authoring discipline (Fix 4 acknowledged). Autonomous mode handled hard failure cleanly; Matt re-enters to a fully-prepared decision packet.

**Tags fired today:** rocket/v1.22-s1-first-batch-regen, gamora/v1.12-r1-sprint-s1-firstbatch, vs2a/v0.1-geometry-type-schema-shipped, vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue (engine); vs2a/v0.6-b6-skilltree-ui-decomposition (demo).

**Skill handoff updated:** `agentic_orchestration/skill_handoff_2026-05-19.md` — wind-down section appended with full arc summary + queued decisions + next-session focus.

**Matt opens first:** `agentic_orchestration/matt-briefing-2026-05-19-s1-firstbatch-fail-disposition.md` § 8.

---

## 2026-05-19 — VS2a S1 first-batch FAIL + critique-pair dispositions (gandalf design + jack-ryan process)

**Event:** S1 first-batch validation gate on season_100001 returned a split verdict:

- **Cohesion (criterion 3) PASS** at 4.83/5.0 (gandalf judgment; exceeds R8 inverted A/B benchmark of 4.77). Season_100001 surfaced as candidate cohesion-5 anchor referent.
- **Mechanics (criteria 1+2) FAIL** under canonical R1 sprint by gamora — 0/11 boss kills (0.000 WR); only 1/11 at mini_boss kill-rate threshold. Statistically indistinguishable from shipped catalogue kit-broken subset.

Critique-pair fired in parallel:

**Gandalf disposition** (`canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md`): Option 1 + Option 4 SELECTED. 5-season regen authorization WITHDRAWN. season_100001 prose retained as cohesion-5 anchor referent; mechanical substrate discarded. Retry path: 3-seed serial budget (100002, 100003, 100004) under substrate-archetypal-stance prior — prefer wind/ember/grit/brine-action; reject char/pall/miasma/rime + aftermath/mourning anchor framing + >50% convergence_failures. Path-a fallback (hand-redesign) activates automatically if all 3 retries fail. Major design insight surfaced: substrate-archetypal-stance is a real design lever; battlefield-clerical canonical rosters (char) have low damage-throughput convention; force/strike/ignite substrates (wind/ember/grit) have higher native throughput.

**Jack-ryan DEV-MODE Gate 2 audit** (`agentic_orchestration/qa/pending/2026-05-19-s1-measurement-discrepancy-audit.md`): transposition hypothesis REFUTED. Root cause is **methodology conflation**, not cross-season copy-paste. Rocket used convergence-time kill-rate estimates (floor modifier, N=30, NO disposition-3 calibration) as proxy for canonical R1 sprint measurements. Disciplines violated: #11 (empirical inspection over assumption), #10 (attribution clarity), #2 (smoke vs full milestone). **Failure point of origin: knight-rider's dispatch authoring** — § 2.4 underspecified the measurement instrument. Four process fixes recommended:

1. Gate criterion must specify instrument, not just threshold
2. Convergence-time estimates must be labeled provisional, not gate-eligible
3. Gate 2 audit before knight-rider fires any first-batch PASS tag
4. Dispatch author (knight-rider) responsible for instrument specification

BLOCK on the PASS claim, not on the work quality. First-batch FAIL is the correct starting state for an iterative sprint. Matt review warranted for the BLOCK severity + future-dispatch standard adoption.

**Knight-rider operational consolidation:**

- Retry dispatch authored: `agentic_orchestration/dispatches/2026-05-19-rocket-plus-gandalf-vs2a-S1-retry-with-seed-constraint.md` — incorporates gandalf § 2.3 substrate prior + jack-ryan § 2.4-bis instrument specification + § 7 process-fix enforcement
- Retry 1 fired to rocket (seed 100002; agentId on file). Serial execution per Discipline #3.
- Matt briefing on deck for natural wind-down re-entry; autonomous execution continues per "do not stop unless I intervene" directive.

**Outstanding tag amendment:** `rocket/v1.22-s1-first-batch-regen` (already pushed) does not claim PASS semantics — it marks the intermediate seam state. The PASS claim lives in the dispatch completion record + AGENT_STATE; both are to be amended by rocket per Fix 2 (convergence-summary heading) during the retry.

---

## 2026-05-19 — VS2a tag-fire batch (intermediate milestones; autonomous-op tag-fire authority per ADR-006 amendment)

**Event:** Knight-rider fired four intermediate milestone tags during autonomous-operation execution:

- `vs2a/v0.1-geometry-type-schema-shipped` @ `cd6e5dd` (engine) — F1 close; star-lord schema 2.13 + geometry_type_source round-trip; 79/79 tests PASS
- `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` @ `155e1f2` (engine) — Stage 1 R2-RT v3 PARTIAL-CLOSE per gandalf § 5.3 routing-to-S1 OR-clause; CD-variance domination finding (Drift-17 Layer 4); Stage 2 on S1 regenerated catalogue queued
- `vs2a/v0.6-b6-skilltree-ui-decomposition` @ `08a9f325e` (demo) — F4 close; drax B6 skill-tree UI surface decomposition (design dispatch + prototype shipped; § 7 data contract surfaced to S2)
- `rocket/v1.22-s1-first-batch-regen` @ `f609928` (engine) — S1 first-batch regen; season_100001 generated under R8 `inverted` pipeline; 4/5 first-batch validation criteria PASS (cohesion pending gandalf judgment)

**Rationale (per ADR-006 amendment under autonomous-operation authority):** Developers surface tag-fire requests via AGENT_STATE; knight-rider fires + pushes under pre-approval-batch authority. Matt re-enters only at wind-down.

**In-flight at this moment:**
- Background agent `a263f7a885ae19bfb` — gamora R1 sprint re-run on regenerated catalogue (validation gate criteria 1+2 confirmation at bigger N + includes SMOKE_CLASS_IDS metadata-sampling fix per rocket B6 pre-work audit flag)
- Background agent `a5683abd1cbb8dc88` — gandalf cohesion judging on season_100001 (criterion 3; R8 6-facet rubric; ≥ 4.0 threshold)

**Next gated work (held pending notifications):**
- Full 5-season regen (rocket; gated on validation gate PASS)
- Stage 2 R2-RT v4 on S1 catalogue (gamora; gated on full regen)
- S3 sim MS extension (gamora; independent of S1; C1 cascade ready; held to avoid sim-code collision with in-flight R1 sprint re-run)
- S2 B6 main work (rocket + gamora; gated on S1 full regen)
- L1 demo regen / VS2a SHIP GATE (star-lord + gamora; gated on all VS2a upstream)

---

## 2026-05-19 — Stage A2 PRE-APPROVAL BATCH authored (full 7-dispatch set; VS2A → VS2B → Stage A2 continuation per Matt directive)

**Event:** Per Matt directive 2026-05-19 ("approved, proceed all the way through Stage A2"), knight-rider authored the complete Stage A2 closeout dispatch set alongside VS2a + VS2b pre-approval batches. Combined 25-dispatch production sprint under one Matt approval.

**Seven Stage A2 dispatches authored:**

1. **A1 — gamora — B7 gear-percentile variance gate** — engine-only sim; gates catalogue stability across gear rolls; tag `stage-a2/v0.1`
2. **A2 — rocket + gamora + drax — B12 full audit** — boots/gloves/belt slot expansion + +% MS affixes + hard-cap + UI; cross-seam contract change; tag `stage-a2/v0.2`
3. **A3 — rocket + gamora — B13 post-narrow-slice** — 5 defensive mobility geometries (`roll`/`defensive_dash`/`strafe_mode`/`blink`/`dodge_stance`) + mini-boss/boss strategic escape AI + archetype-emergence observability + trait-pool extension; tag `stage-a2/v0.3`
4. **A4 — gamora — B14 multi-band convergence sim** — extends B14.5 V1 canonical balance-loop pattern; riskiest piece; rollback to `v1.3-b14-5-primary-loop` available; tag `stage-a2/v0.4`
5. **A5 — rocket + drax — B16 loot drop architecture** — drop rules + auto-pickup + visual layer per A6 framework; **Drift-12 candidate filing**; tag `stage-a2/v0.5`
6. **A6 — gandalf — Stage A2 design watch-items framework** — single framework covering B12 visual/UX + B13 telegraph-art convention + B16 loot visual layer; Drift-12 filing; tag `stage-a2/v0.6`
7. **A7 — gandalf + knight-rider + Matt — Playtest Cycle 1** — three phases: autonomous prep + Matt-gated execution + autonomous disposition; substrate = VS2a regen season_001003 + VS2b regen season_001005; tag `stage-a2/v1.0-stage-a2-ship` (Stage A2 CLOSED)

**Combined sprint inventory (consolidated):**
- VS2a: 12 production dispatches (F1-F4 + F5 + F6 + F6-D + R2-RT + S1 + S2 + S3 + L1)
- VS2b: 6 production dispatches (V1-V6)
- Stage A2: 7 production dispatches (A1-A7)
- TOTAL production: **25 dispatches**
- In-flight VS2a continuations: C1-C4 (4 items)
- Matt-gated wind-down items: M1 (Drift-15 selection) + M2 (engine-rebuild playtest tags) + A7-exec (Playtest Cycle 1 execution) = 3 items
- GRAND TOTAL: **32 roadmap items** locked under pre-approval-batch

**Estimated duration:** ~10-16 weeks wall from VS2a L1 ship through Stage A2 v1.0 ship, depending on parallel execution + Matt wind-down session cadence.

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9 through Stage A2 closeout. Matt re-enters at wind-down (his discretion) for M1 + M2 + A7-exec triple-gated step (Drift-15 pack + engine-rebuild playtest tags + Stage A2 Playtest Cycle 1 — all addressable in single Matt session).

**Forward routing post-Stage-A2:**
- Stage A3 (B9 series; ~4-6 weeks; design fully resolved 2026-05-12 in file 32) — pre-approval-batch decision DEFERRED to Matt at next wind-down session
- Stage A4 (B5 + B15) / A5 / A6 / A7 (progression system) — further deferred
- Playtest Cycles 2-4 — gandalf authors rubrics per A7 template; Matt-gated execution

**Pre-approval surface (Matt's three-doc review):**
- `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md` (12 dispatches)
- `agentic_orchestration/hive-mind/vs2b-pre-approval-batch-2026-05-19.md` (6 dispatches)
- `agentic_orchestration/hive-mind/stage-a2-pre-approval-batch-2026-05-19.md` (7 dispatches; consolidated combined view in § 6)

**Authority:** Matt directive 2026-05-19 (VS2A → VS2B → Stage A2 pre-approval continuation); knight-rider operationalization + dispatch authoring under autonomous-mode authority.

---

## 2026-05-19 — VS2b PRE-APPROVAL BATCH authored (full 6-dispatch set; VS2A → VS2B continuation per Matt directive)

**Event:** Per Matt directive 2026-05-19 ("approved, proceed with VS2A → VS2B"), knight-rider authored the complete VS2b dispatch set alongside the VS2a pre-approval batch. Pre-approval-batch mode extended through VS2b. Combined VS2a + VS2b = 18 dispatches; Matt approves one batched sprint plan; no Matt-engagement between batches.

**Six VS2b dispatches authored:**

1. **V1 — rocket — `embodiment_narrative_beat` schema field** — per `canonical/story/embodiment-display-loadout.md` § 15; Discipline #14 generative-side schema; two-stage migration; tag `vs2b/v0.1`
2. **V2 — star-lord — LLM beat-generation call orchestration** — folds into Stage 2 cosmological-vocabulary pipeline as follow-on; anti-bias scaffolding per Discipline #14 candidate; tag `vs2b/v0.2`
3. **V3 — drax — loadout embodiment-narrative-display surface** — per spec § 15 + § 13 implementation cascade; loadout-first; Diablo III class-select reference; tag `vs2b/v0.3`
4. **V4 — gandalf — chierit element-reconciliation (small ~30 min)** — closes VS2a + VS2b chierit watch-items; element-only mapping decision + physical/hybrid fallback; tag `vs2b/v0.4`
5. **V5 — drax + elrond — full Pimen catalogue integration** — extends VS2a C2 (11/13 GREEN-list) to full coverage; tag `vs2b/v0.5`
6. **V6 — star-lord + gamora — VS2b ship gate (regen season_001005)** — fresh regen demonstrates cipher migration + embodiment-axis + embodiment-narrative display + Pimen full integration; tag `vs2b/v1.0-vs2b-ship` (VS2b CLOSED)

**Roadmap-drift surfaced + flagged:** `canonical/16-project-roadmap.md` § VS2b lists some items as "in-flight" or "dispatch not yet authored" that have shipped per dispatch completion records. Stage 1 (rocket) + Stage 2 vocab + Stage 3 engine + Stage 3 drax all shipped 2026-05-16. Roadmap doc amendment forward-flagged to gandalf at next pass. Scope-of-work-vs2b § 1 captures ground truth.

**Combined VS2a + VS2b inventory:**
- VS2a: 12 dispatches (F1-F4 + F5 + F6 + F6-D + R2-RT + S1 + S2 + S3 + L1)
- VS2b: 6 dispatches (V1-V6)
- In-flight: C1-C4 (continue per AGENT_STATE)
- Matt-gated: M1 (Drift-15 selection) + M2 (engine-rebuild playtest tags)
- TOTAL: 24 roadmap items locked under pre-approval-batch

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9. Matt re-enters only at wind-down (his discretion). Post-VS2b: Stage A2 closeout pre-approval-batch decision DEFERRED to Matt at next wind-down session.

**Pre-approval surface (Matt's one-doc review):**
- `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md` (12 dispatches)
- `agentic_orchestration/hive-mind/vs2b-pre-approval-batch-2026-05-19.md` (6 dispatches)
- `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` + `coordination-matrix-vs2b.md` (companion plans)

**Authority:** Matt directive 2026-05-19 (VS2A → VS2B pre-approval continuation); knight-rider operationalization + dispatch authoring under autonomous-mode authority.

---

## 2026-05-19 — VS2a PRE-APPROVAL BATCH authored (full 12-dispatch set; per Matt directive)

**Event:** Per Matt directive 2026-05-19 ("Batch all of VS2a now so I can approve everything in advance"), knight-rider authored the full VS2a dispatch set (12 dispatches total) for Matt's pre-approval review before autonomous execution proceeds. After Matt's review + approval, no further Matt-engagement is required until wind-down (M1 + M2 + retrospective).

**Eight additional dispatches authored (sibling to F1+F2+F3+F4 from earlier today):**

5. **F5 — legolas + gandalf — VS2a Drift-14 pool × VFX-catalogue mapping audit** — Mode A audit + gandalf re-scoring + culled-pool summary; gates: F3 framework lands; tag: `vs2a/v0.10-drift14-audit-complete`
6. **F6 — legolas — VS2a Drift-15 environment-tileset Track A sweep** — Mode B catalogue crawl across Tier-1 pixel-art vendors; gates: F3 framework lands; tag: `vs2a/v0.11-drift15-track-a-complete`
7. **F6-D — drax — VS2a Drift-15 Track D environment-tileset integration** — renderer extension + pack manifest consumption; gates: M1 Matt-selection at wind-down; tag: `vs2a/v0.16-drift15-drax-integration-complete`
8. **R2-RT — gamora — VS2a R2 H1 re-validation under explicit geometry_type** — R2 disposition § 3.2 forward-routed re-test under ORIGINAL variance ≥ 0.10 threshold; gates: F1 acceptance complete; tag: `vs2a/v0.2-r2-h1-revalidated`
9. **S1 — rocket + gandalf consult — VS2a kit-redesign sprint (3-branch per F2 path)** — three-branch pre-authored dispatch (hand-redesign / R8-inversion / hybrid); gates: F2 + F1 land; tag: `vs2a/v0.7-kit-redesign-sprint-complete`
10. **S2 — rocket + gamora — VS2a B6 main work (tree structure + tree-aware convergence)** — per `canonical/28` B6 extension; gates: F2 + rocket pre-work + S1 partial; tag: `vs2a/v0.8-b6-main-work-complete`
11. **S3 — gamora — VS2a Gate-3b sim MS extension** — sim consumer of engine-emitted JSON MS values; gates: rocket schema-default + star-lord export-DTO (C1 in-flight cascade); tag: `vs2a/v0.9-sim-ms-gate3b-complete`
12. **L1 — star-lord + gamora — VS2a demo regen on single season (SHIP GATE)** — full integrated stack demonstration; gates: F1 + F4 + S1 + S2 + S3 + C1 + C2 + C3 + F5; tag: `vs2a/v1.0-vs2a-ship`

**Pre-approval surface for Matt review:** `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md` — full inventory + DAG + activation-gate map + Matt-approval pattern (what Matt approves; what Matt may amend; what Matt does NOT need to approve under autonomous-mode).

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9 (Matt re-enters only at wind-down). Pre-approval-batch mode is the Matt-side preference shift: Matt reviews the whole sprint plan up front, then walks away knowing every dispatch is locked.

**M1 + M2 Matt-gated items unchanged:** Drift-15 Matt-selection at wind-down; engine-rebuild playtest tag firings v0.12 + v0.16. F6-D drax integration is pre-authored but HELD post-M1.

**Authority:** Matt directive 2026-05-19 (pre-approval-batch mode); knight-rider operationalization + dispatch authoring under autonomous-mode authority.

---

## 2026-05-19 — VS2a first-fire batch DISPATCHED (F1 + F2 + F3 + F4 authored)

**Event:** Knight-rider authored four VS2a first-fire dispatches under AUTONOMOUS-OPERATION (continuation of engine-rebuild close → VS2a sequencing per dispatch § 6.5 explicit ordering). All four fire immediately; no upstream gating on each other beyond F3 → F5/F6 (second-fire batch). C1–C4 in-flight continuations independent. M1 + M2 Matt-gated items HELD for wind-down.

**Dispatches authored (`agentic_orchestration/dispatches/`):**

1. **F2 — gandalf — VS2a kit-redesign approach Gate-1 decision** (`2026-05-19-gandalf-vs2a-kit-redesign-approach-decision.md`) — HIGHEST leverage; gates S1 + S2. Decision: hand-redesign (a) vs R8-inversion (b) vs hybrid (c). Acceptance: `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` + tag `vs2a/v0.5-kit-redesign-approach-decided`.
2. **F1 — rocket + star-lord — VS2a `geometry_type` per-skill schema field** (`2026-05-19-rocket-plus-star-lord-vs2a-geometry-type-schema.md`) — engine-rebuild R2 H1 fall-out per gandalf R2 disposition § 3.1 + jack-ryan Q1 disposition. Schema additive-nullable → non-null post-backfill. MIGRATION.md required at both seams. Round-trip smoke per Principle 6. Acceptance: tag `vs2a/v0.1-geometry-type-schema-shipped`.
3. **F3 — gandalf — Drift-14 + Drift-15 design framework** (`2026-05-19-gandalf-vs2a-drift14-15-framework.md`) — gates F5 + F6 legolas commissions. Drift-15 framework includes EXPLICIT autonomous-vs-Matt-gated step separation (Tracks A+B autonomous; Track C HELD for wind-down per M2 pattern; Track D post-Matt). Acceptance: framework docs + drift-audit.md updates + tags `vs2a/v0.3` + `vs2a/v0.4`.
4. **F4 — drax — VS2a B6 skill-tree UI surface decomposition** (`2026-05-19-drax-vs2a-b6-skilltree-ui-decomposition.md`) — closes fifth P6 instance (engine emits tree data; demo has no rendering surface). Drax authors design dispatch + ships prototype. Acceptance: design doc + prototype + tag `vs2a/v0.6-b6-skilltree-ui-decomposition`.

**Second-fire (gated on F3):** F5 (legolas Mode A Drift-14 pool × VFX-catalogue mapping audit) + F6 (legolas Mode B Drift-15 environment-tileset sweep Track A).

**In-flight continuations (specialist independent; no knight-rider dispatch):** C1 movement-speed baseline + C2 B11 GREEN-list VFX + C3 chierit character rendering + C4 Pimen curation pipeline.

**Matt-gated (HELD for wind-down):** M1 (Drift-15 Matt-selection per Track C) + M2 (engine-rebuild playtest tags `v0.12-r5-hypothesis-test-passed` + `v0.16-r4-hypothesis-test-passed`).

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9 (inherited from engine-rebuild protocol into VS2a per scope-of-work § 6). No L3-to-Matt during operation. Matt re-enters only at wind-down.

**Authority:** Matt directive 2026-05-19 (autonomous-operation continuation); knight-rider operationalization + dispatch authoring under launch-dispatch § 6.5 routing.

---

## 2026-05-19 — Engine-rebuild batch CLOSED (`hive-rebuild/v1.0-engine-rebuild-complete` fired across all 4 repos)

**Event:** Engine-rebuild hive-mind session completed under AUTONOMOUS-OPERATION mode. Knight-rider proceeds immediately to VS2a per dispatch § 6.5 explicit ordering; Matt does NOT return to loop (wind-down trigger remains exclusively Matt's explicit declaration per protocol § 4.9).

**Tag fired:** `hive-rebuild/v1.0-engine-rebuild-complete` across all 4 repos under "operational-completion category-of-completion" framing per gandalf disposition `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md` (Option γ).
- Engine: at `bb013b7` (gamora R2 production graduation; substrate-completion commit)
- Collab: at `9391b22` (gandalf disposition commit)
- Demo: at `542f1115b` (latest HEAD; R4 v0.15 operational already tagged)
- Loadout: at `ec73ea7` (latest HEAD)

**Workstream completion table:**
| WS | Status | Hyp tag |
|---|---|---|
| R1 — Per-tier balance | CLOSED | `v0.3` (4-sub-claim category-of-completion) |
| R2 — Spatial sub-gauntlet | CLOSED | `v0.14` (Option D instrument-limited PASS) |
| R3 — Per-skill range + AI schema | CLOSED | `v0.6` |
| R4 — Demo collision + leash + range | OP-COMPLETE; PLAYTEST-PENDING | `v0.16` HELD (Matt-gated) |
| R5 — Demo AI parity | OP-COMPLETE; PLAYTEST-PENDING | `v0.12` HELD (Matt-gated) |
| R7 — AI catalogue source-of-truth | CLOSED | `v0.7` |
| R8 — Season-as-emergent-output | CLOSED | `v0.10` + `v0.11` (Sub-case 3 disposition) |

5 of 7 CLOSED; 2 of 7 OP-COMPLETE with playtest-pending tags HELD for Matt wind-down session. Notional `hive-rebuild/v1.1-engine-rebuild-final` fires when v0.12 + v0.16 resolve.

**R-series disposition arc (4 dispositions; category-of-completion pattern established):**
- R1 Blocker 3 — gandalf — "70% pass-rate" retired; 4 sub-claims (GATE WORKS + REACHABLE + KIT-BROKEN SURFACE + QUEUE EXISTS); kit-redesign queue authored as VS2a handoff (`canonical/story/r1-kit-redesign-queue-2026-05-19.md`)
- R8 Sub-case 3 — gandalf — `inverted` as default; `inverted_no_naming` deferred behind template-distribution repair; `canonical/19-llm-call-map.md` Phase A swap
- R2 H1 Option D — gandalf — variance ≥ 0.10 threshold preserved as VS2a re-test target once `geometry_type` per-skill schema field lands (instrument-limited by name-heuristic 43/3/4 sample imbalance)
- v1.0 Option γ — gandalf — operational-completion framing; playtest-pending tags HELD; roadmap continuation unblocked

**Engine-rebuild fall-out items routed to VS2a:**
1. `geometry_type` per-skill schema field (rocket + star-lord) — re-enables R2 H1 under original threshold
2. Kit-redesign queue execution (~20-30 mediocre + ~10-15 broken classes) (rocket + gandalf consult) — intersects with B6 main work
3. Spatial boss recalibration if needed (gamora; may be VS2b)
4. Template-distribution repair (rocket; LOW; capacity-when-available)
5. `--anchor-id` CLI flag (rocket; deferred)
6. R1 second-pass calibration knobs (gamora; deferred — boss reachability stable per N=60 Test 3)

**Items completed this session that were on the R-disposition forward-routing list (removed from VS2a queue):**
- `seasonal_dominant_element` write-back gap fix (rocket commit `9f6e4e6`)
- R8 Test 5 multi-shot stability execution (Jaccard 1.00 on `inverted/season_099002`)

**Operating-mode metrics:**
- Matt escalations: 0
- Hard BLOCKs by jack-ryan: 0
- WARN findings resolved in-session: 4
- Structural blockers surfaced + dispositioned: 3
- Gandalf disposition decisions: 4
- Canonical-doc amendments authored: 8+
- Transient infrastructure failures recovered: 1 (rocket API overloaded_error → re-fire)
- Specialist sessions: ~33
- Tags shipped + pushed: 15
- Push hard-constraint violations: 0
- Elapsed wall time: activation 04:26Z → batch close ~07:05Z (~2h 40min; ~7h cumulative specialist time)

**Closeout state-of-hive:** `agentic_orchestration/hive-mind/state-of-hive-2026-05-19-engine-rebuild-v1.0.md` (knight-rider authored at batch close per dispatch § 6.5 step 3). Mid-day snapshot at `state-of-hive-2026-05-19-engine-rebuild-mid-day.md` for full chronological detail.

**Authority:** Matt directive 2026-05-19 (autonomous-operation launch); gandalf v1.0 disposition; knight-rider operationalization + state-of-hive closeout authorship.

---

## 2026-05-19 — Engine-rebuild hive ACTIVATED (second hive-mind invocation; AUTONOMOUS-OPERATION mode)

**Event:** Knight-rider activated the **engine-rebuild hive-mind session** per Matt directive 2026-05-19 + gandalf-authored launch dispatch (`agentic_orchestration/dispatches/2026-05-19-knight-rider-engine-rebuild-launch.md`, commit `d49c587`). This is the **second hive-mind activation** (first was 2026-05-17 Phase-1 P1; mission completed + archived).

**Mission scope:** Seven workstreams closing the gauntlet-simulator gaps diagnosed 2026-05-18 + running the season-as-emergent-output A/B test:
- **R1** Per-tier balance targets (gamora; 1–2 wk)
- **R3** Per-skill range + AI behavior schema migration (rocket + star-lord + elrond; 2–4 wk)
- **R7** AI catalogue source of truth (rocket + star-lord; 2–3 wk parallel with R3)
- **R8** Season-as-emergent-output A/B (rocket + star-lord + gandalf; 1–2 wk)
- **R5** Demo AI parity audit (drax; 1 wk, queued behind R3)
- **R2** 2D spatial sub-gauntlet (gamora + star-lord; 3–5 wk, queued behind R3)
- **R4** Demo collision + leash + range (drax; 2–3 wk, queued behind R3)

**Out of scope:** R6 Host-Calibration (Pattern-B parked per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`); Pattern-B commercial-direction work; Phase-1 P1 re-work.

**First-fire batch (parallel, dispatches authored):** R1 + R3 + R7 + R8. R5 + R2 + R4 queued behind R3.

**Critical operational change vs 2026-05-17 protocol:** **AUTONOMOUS OPERATION** per protocol § 4.0. No L3-to-Matt escalation during operation. SME agents decide within their seams; gandalf decides cross-cutting design/canonical/architectural; knight-rider decides orchestration/sequencing. Matt re-enters **only** at wind-down — engine-rebuild completion does NOT trigger wind-down; flow continues onto VS2a → VS2b → Stage A2 per Matt roadmap-continuation directive (launch dispatch § 6.5).

**Commit + push authority extended** per launch dispatch § 6.6 (ADR-006 amendment extension): knight-rider may commit + push on major milestone achievement and hypothesis-test passage without per-action authorization. Hard constraints retained (no force-push, no hook bypass, explicit refspec, summary from live git state).

**Mechanics inheritance:** All operating mechanics from `canonical/story/archived/hive-mind-protocol-2026-05-17.md` §§ 3–11 inherit by reference; engine-rebuild protocol specifies what's distinct (mission scope, coordination matrix, autonomous-operation amendment, galadriel sub-agent restriction).

**Galadriel sub-agent restriction in effect** per protocol § 7 + amendment to `.claude/agents/galadriel.md` (already authored 2026-05-19 per Matt directive). Galadriel does NOT invoke sub-agents during the hive; surfaces requests via hive log REQUEST entry.

**Pre-rebuild safety baseline tagged + pushed across all 4 repos:**
- `hive-rebuild/v0.0-pre-engine-rebuild`
- collaboration `d49c587`, engine `89f83c2`, demo `59b933031`, loadout `ec73ea7`

**Operational artifacts committed:** activation commit `edeeea8` (collaboration repo, main, pushed):
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` (append-only hive log with activation STATE + 4 HANDOFF entries)
- `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md`
- `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md`
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-19-engine-rebuild.md`
- 4 first-fire dispatches at `agentic_orchestration/dispatches/`:
  - `2026-05-19-gamora-R1-per-tier-balance-targets.md`
  - `2026-05-19-rocket-plus-star-lord-plus-elrond-R3-schema-migration.md`
  - `2026-05-19-rocket-plus-star-lord-R7-ai-catalogue-source-of-truth.md`
  - `2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md`

**Authority:** Matt directive 2026-05-19 (autonomous-operation launch); gandalf protocol + solutions doc + Pattern-B PARKED thread (commit `d49c587`); knight-rider operationalization.

**Tag namespace:** `hive-rebuild/v0.<N>-<milestone>` (distinct from `hive/v0.<N>` used for Phase-1 P1).

---

## 2026-05-18 — hive-log STATE: star-lord multi-season encounter analytics complete — telemetry.db backfilled for 6 seasons + MS/AOE schema extended

**Event:** star-lord completed dispatch `2026-05-18-star-lord-fights-jsonl-ingest-plus-multi-season-encounter-analytics`. Matt L3 authorized "fire star-lord on Path A."

**Block 1 — fights.jsonl ingest:** New script `scripts/ingest_fights_jsonl_to_telemetry.py` (engine). Backfilled `class_fight_loadouts`, `abilities`, and `monsters` in `telemetry.db` for 6 seasons: 002011, 002012, 002013, 002014, 002015, and 002328. Total: 609,800 fight rows. Row counts match class-phase JSONL counts exactly. Idempotency smoke-tested (drop-and-replace pattern for fight rows; INSERT OR IGNORE for abilities/monsters). Geometry_type derived via `derive_geometry_type()` 3-layer cascade (same as D10 generation). All V2.x spatial columns NULL for backfilled rows — fights.jsonl has no positional data.

**Block 2 — multi-season encounter analytics:** 6 per-season `encounter_analytics_NNNNNN.json` files landed in `reincarnated-loadout/data/`. Existing `encounter_analytics.json` (season_001005) renamed to `encounter_analytics_001005.json` for naming consistency (original retained).

**Block 3 — MS/AOE radius bands:** Extended `gen_encounter_analytics.py` with two new per-class fields. `movement_speed_band` (slow/medium/fast, per-season 33rd/67th percentile). `aoe_radius_band` (tight/medium/wide, same). AOE radius sourced from canonical geometry-type default table (B11 math note) — per-skill spatial radius params do not exist in class JSON. Documented in output JSON and MIGRATION.md v1.15.

**Findings:** All D10 seasons have uniform movement_speed=8.0 m/s — MS bands degenerate (all "slow"). season_002328 predates movement_speed field (NULL). AOE-vs-monster-position correlation not possible from existing data — no spatial data in fights.jsonl. Flagged to knight-rider for future instrumentation dispatch.

**Engine commit:** `d85fb45`, `89f83c2` — pushed to main. **Loadout commit:** `9b23382` — pushed to main.
**Tag:** `star-lord/v1.8-fights-jsonl-ingest-plus-multi-season-encounter-analytics-plus-ms-aoe-bands-1`
**MIGRATION.md:** v1.15 appended.

**drax v1.18 Block 2 status:** UNBLOCKED. Per-season encounter_analytics files ready for consumption.

---

## 2026-05-18 — hive-log STATE: star-lord bulk re-roll resume complete — 12 missing portraits generated; total 24/24 in `_reroll_all/`

**Event:** Resumed `bulk_reroll_anatomy.py` after prior run died silently at 12/24. Patched script with skip-if-exists idempotency guard, then ran to completion synchronously.

**Root cause (prior silent death):** Script had no skip-if-exists check — re-running from scratch would have re-generated already-complete images. The silent kill was most likely a process-level timeout or OOM from the agent harness after the 12th sequential gpt-image-1 API call (~10 min elapsed). No retry or resume path existed in the original script. Idempotency patch closes the gap.

**12 images generated this session:**
- `season_002011/pitch-smuggler.png` (fire mage)
- `season_002013/shaft-diver.png` (physical hunter — canary slug skipped per brief)
- `season_002014/` — all 5: plague-wind-censer, plague-lantern-bearer, chalk-handed-quarantine-warden, quarantine-lector, plague-diver
- `season_002015/` — all 5: marble-tongued-royal-scribe, banished-royal-herald, windborne-herald-of-the-fractured-court, mad-kings-lector, exiles-gauntlet

**Cost this session:** 12 × $0.04 = $0.48. Ledger total: $2.16. Sprint ceiling remaining: $12.84.

**Script patched + committed:** `fix(star-lord): bulk_reroll_anatomy.py idempotency — skip existing files` — commit `55fa186` on `reincarnated-engine/main`.

**Constraints honored:** pitchData.ts NOT touched. Images NOT pushed. Originals at `season_<id>/<slug>.png` NOT disturbed.

**Status: READY FOR GANDALF CURATION.** All 24/24 portraits now present in `_reroll_all/`. Gandalf curates winners, wires pitchData.ts, and pushes.

Output dir: `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_all/`
Cost ledger: `/Users/admin/Games/reincarnated-loadout/public/pitch/cost-ledger.json`

---

## 2026-05-18 — hive-log STATE: Canary reroll complete — ready for gandalf curation

**Event:** Star-lord completed anatomy-correction re-roll for Canary of the Drowned Seam (Hero of the Engine). All 3 existing Canary images had hand-anatomy failures (canonical + preflight: 3 fingers; attempt-1: 4 distorted fingers). 4 new attempts generated with progressively stronger anatomy interventions.

**Files generated (all OK, $0.04 each):**
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-1.png` — original composition + aggressive anatomy negatives embedded in prompt
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-2.png` — pose change: flame hovering above open palm (summoned, not grasped — eliminates grip failure mode)
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-3.png` — pose change: hand at side, flame floats behind shoulder near canary (hand minimized in focal area)
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-4.png` — tight chest-up portrait: hand and flame both below bottom frame edge (hand problem eliminated entirely)

**Cost:** $0.16 total (4 × $0.04). Ledger total now $1.20. Sprint ceiling remaining: $13.80.

**Constraints honored:** pitchData.ts NOT touched. Images NOT pushed. Existing _preflight/ and season_002013/ files NOT disturbed.

**Status: READY FOR GANDALF CURATION.** Gandalf reviews all 4, picks winner, wires into pitchData.ts and triggers push as part of swap commit.

Script preserved at: `/Users/admin/Games/reincarnated-engine/scripts/pitch/canary_reroll.py`

---

## 2026-05-18 evening — Overnight autonomous sprint ACTIVATED (mobile-playable + loadout analytics + visual benchmark)

**Event:** Matt-authorized single-night autonomous sprint launched within Phase-1 P1 hive-mind operating mode. Invocation authored by gandalf 2026-05-18 evening per Matt directive; knight-rider engaged at session-open and activated per § 11 checklist.

**Three tracks active:**
- **Track A — Mobile-playable demo (local-dev path).** v1.20 + v1.21 already shipped; D11.5 debug-state URL hook + mobile-render validation queued.
- **Track B — Loadout analytics suite iteration-1.** Gandalf IA → star-lord + elrond data manifests (parallel) → drax implementation → Vercel preview auto-deploy.
- **Track C — Visual benchmark pilot (galadriel commission).** State-matched captures vs Matt's 7-image DoE reference set; rubric authoring; first-pass benchmark report.

**Galadriel — new agent commission.** Sixteenth agent role: visual perception and UX-similarity steward (Tier C+; mirrors elrond/legolas conventions). Persona: Galadriel, keeper of the Mirror. Owns `agentic_orchestration/galadriel/`. **Status: deferred to morning Matt approval** — `.claude/agents/galadriel.md` write was denied by harness at activation; full agent-file draft preserved at `agentic_orchestration/galadriel/AGENT-DRAFT.md` for clean drop-in (see morning-briefing L3-1). Track C work proceeds under deferred-agent-creation workaround (gandalf + drax co-author).

**Protocol amendments for single-night cadence (per invocation § 5):**
- Hive log entries every 30 minutes minimum per active seam
- Two state-of-hive snapshots (midpoint + end-of-sprint) vs daily
- DECISION entries can be 1-sentence rationale during sprint
- Per-seam intermediate tags optional; only morning-checkpoint tag required (`sprint/v0.1-mobile-analytics-benchmark-2026-05-18`)
- Knight-rider expanded L2.5 authority within § 6 pre-authorization matrix; L3 items queue to `morning-briefing-2026-05-19.md`
- Halt-condition discipline preserved (queue-for-morning is not failure)

**Dispatches authored at activation (8 total):**
- `2026-05-18-gandalf-loadout-analytics-suite-information-architecture.md` (Track B.5; critical-path BLOCKER)
- `2026-05-18-drax-debug-state-url-hook-D11-5-plus-mobile-render-validation.md` (Track A.2 + D11.5)
- `2026-05-18-star-lord-loadout-analytics-data-manifest-engine-side.md` (Track B.6 engine-side)
- `2026-05-18-elrond-loadout-analytics-data-manifest-catalogue-side.md` (Track B.6 catalogue-side)
- `2026-05-18-drax-plus-star-lord-vercel-deployment-asset-pipeline-options-paper.md` (§ 2.4 scoping)
- `2026-05-18-drax-galadriel-workaround-capture-pipeline-and-state-matched-captures.md` (Track C pipeline)
- `2026-05-18-drax-loadout-analytics-suite-iteration-1.md` (Track B.7 implementation)
- `2026-05-18-gandalf-plus-drax-visual-benchmark-report-vs2a.md` (Track C.13 report)
- `2026-05-18-jack-ryan-overnight-sprint-watchpoints.md` (continuous-observation)

**Pre-authorization matrix § 6 verified.** HARD NOs honored: no vendor acquisitions, no `git push --force`, no Vercel demo deployment (scope-only paper), no CLAUDE.md / AGENTS.md modifications, no Phase-1 P1 scope changes, no load-bearing canonical-doc amendments.

**Sprint activation commit:** `72495b8` (hive-log STATE + 8 dispatches + morning-briefing + galadriel working tree).

---

## 2026-05-17 — drax v1.16.1 HOTFIX: wave-progression hang + audio/VFX gap

**Event:** Matt L3 playtest on drax v1.16 revealed two critical blockers in VS2a demo.

**Bug 2 (wave-hang) root cause:** v1.16 `gauntletFromRecipe()` paired 2 pack-proxies per wave (3 × 16-mob rooms). The `allPackDead` condition (`pack.every(m => !m.combatant.isAlive)`) stalls when any mob survives outside its anchor room — mobs halt pursuit at room edge per `shouldHaltPursuit()`, leaving the player in `fighting` state indefinitely. Additionally: 8 total waves vs. 7-room dungeon caused `roomForWave(dungeon, 8) = undefined` — act-boss wave 2 had no room anchor. **Fix: Reshape A** — 1 pack-proxy per wave (6 × 8 mobs), extending to 11 total waves + 11-room dungeon plan.

**Bug 1 (audio gap) root cause:** AudioContext suspended before user gesture. Howler v2.2 auto-resumes its own context, but our Web Audio API Tier-1 procedural context (`getAudioCtx()`) is a separate `AudioContext` that does not. **Fix:** `_hookAudioContextResume()` explicitly resumes both contexts on first `mousedown`/`keydown`/`touchstart`.

**Diagnostic logging added** throughout both subsystems (grep `[diag]` tag) for Matt's re-playtest DevTools session.

**Commit:** `430a9f4` (reincarnated-demo); **tag:** `drax/v1.16.1-hotfix-wave-hang-plus-audio-vfx-gap-1`
**Dispatch:** `2026-05-17-drax-v1-16-1-hotfix-wave-hang-plus-audio-vfx-gap.md` — completion record appended.

Format: reverse chronological, dated entries with brief rationale.

---

## 2026-05-17 — Phase-1 P1 hive-mind mode ACTIVATED

**Event:** Matt directive 2026-05-17 ("100% heads down development work across the entire team and rebuild the engine from the ground up to achieve full Phase-1 P1 before demo VS2a. ... All in perfect harmony. Let's take this on as a hive mind.") triggered Phase-1 P1 hive-mind operating mode per gandalf invocation request `agentic_orchestration/gandalf/requests/2026-05-17-knight-rider-phase-1-p1-full-overhaul-coordination.md` + operating protocol `canonical/story/hive-mind-protocol-2026-05-17.md`.

**Standard mode SUSPENDED for duration of Phase-1 P1.** Specialists operate under distributed authority (L1 in-seam; L2 cross-seam via knight-rider; L3 architectural to Matt). Jack-ryan continuous-observation replaces Gate-1/Gate-2 retrospective review. Per-dispatch authorization gating removed; specialists execute against the scope-of-work continuously. Gandalf continuously available for design-direction.

**Pre-Phase-1 P1 baselines tagged** (local; not pushed per ADR-006 pending Matt authorization):
- engine: `hive/v0.0-pre-phase-1-p1 @ f9c363e`
- demo: `hive/v0.0-pre-phase-1-p1 @ 692c555`
- loadout: `hive/v0.0-pre-phase-1-p1 @ 90db544`

**Hive operational artifacts authored at activation** (knight-rider; per invocation § 4):
- `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` — 27-deliverable executable plan with per-seam tasking + critical-path identification + in-flight work disposition (fold/pause/standalone) + risk register + ship-gate criteria
- `agentic_orchestration/hive-mind/coordination-matrix.md` — seam × deliverable matrix; cross-seam dependency DAG; concurrent-edit hot-spots; MIGRATION.md cadence
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` — append-only hive log; activation entry + per-seam initial tasking distribution
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-17.md` — activation-day digest

**Per-seam initial tasking distributed** (per scope-of-work § 2):
- Rocket: Deliverable 1 (substrate identity loader + 7-YAML extraction) — Layer-1 foundation
- Gamora: Deliverable 7 math note (resistance matrix 7×7; Discipline #1 load-bearing) + cut pending Gate 3b tag
- Star-lord: Deliverable 6 PLAN + scoping doc (LLM prompt structure refactor — highest unknown)
- Drax: Deliverable 27 session-runner readiness + Deliverable 19 planning
- Jack-ryan: continuous-observation rhythm setup + baseline test-suite snapshot
- Gandalf: continuous design-direction availability + Deliverable 20 (grouping-vocab extension; 1 day; gates D6 implementation)

**Standing Matt-disposition queue (surfaced in activation broadcast):**
1. Vendor acquisitions (CraftPix premium + Fellor Crystal + Frostwindz Deathbringer) — blocks D19 implementation
2. VFX scene-needs spec micro-decisions (gandalf open thread) — fold into activation discussion
3. Hive activation timing (knight-rider recommendation: STAGED)
4. Push authorization for 3 baseline tags to origin

**Ship gate (per scope-of-work § 6):** `v1.0-phase-1-p1` tag cut Matt-approved when all 27 deliverables ship + diversity-architecture dominant-cluster success criterion validates + cross-doc updates land + test suite GREEN + retrospective authored.

**Estimated duration:** 8-12 weeks per gandalf invocation; knight-rider re-scopes after Week-1 seam assessments.

**Files updated:** This CHANGELOG entry; hive-mind/ directory created with 4 artifacts; 3 baseline tags created locally (not yet pushed). No agent-definition or governance-doc changes; hive-mode operates over baseline topology per protocol § 2.2.

---

## 2026-05-17 — Substrate-expansion Branch A confirmed: canonical-four → 6 (Phase-1 P1); vocab freeze standing constraint

**Event:** Gandalf 2026-05-17 escalation on substrate-level genre-positioning surfaced the canonical-four (fire/water/earth/wind) substrate as below-ARPG-genre-floor. Compounding evidence: Case D Fire_Lord thunder math-impossibility resolved Day-4 via mini-boss tier-bump was a symptom of missing substrate, not an isolated case; legolas Track A REVERSE TIER 1 expansion candidates concentrate in beyond-canonical-four substrates (5 of 5: holy/electric/poison/void/shadow); spirit-swap differentiation as load-bearing per 2026-05-08 design intent argues for >4 archetype identities; earth-meta-layer / ascended-spirit / Earth-self thematic framing aligns naturally with luminance axis (Solo Leveling, Bleach, Mushoku Tensei healing-light reference cluster); ARPG-vs-JRPG Day-4 commitment direction.

**Decision (Matt-confirmed Branch A 2026-05-17; gandalf design doc landed `1df535b`):** Expand canonical-four → 6 substrates in Phase-1 P1. Substrate naming + light/dark treatment LOCKED per gandalf design doc:
- + **`lightning`** as own substrate (not wind-flex). Genre-canon across D2-D4/PoE/Last Epoch/Grim Dawn. Closes Case-D pattern at substrate level.
- + **`holy`** and **`shadow`** as TWO distinct substrates (PAIRED-LUMINANCE-AXIS, not collapsed single-luminance). Rationale: paired-opposition mirrors Mirror/Body-swap/Passage triadic cosmology; ARPG-genre archetype fidelity (D2 Paladin vs Necromancer; D4 Necromancer-vs-Holy); legolas reverse-audit shows distinct VFX coverage for holy-radiance vs shadow-tendril.
- Defer poison/acid (earth-flex adequate; Phase-2 candidate).
- Decline void (anti-substrate; boss-exclusive only via trial-room gallery permit).
- VS2a/VS2b ship on canonical-four explicitly. NO scope creep into in-flight visual surfaces.
- Final substrate set (6): **fire / water / earth / wind / lightning / holy / shadow** (Phase-1 P1 target state).

**Standing constraints in effect:**

1. **Vocab freeze (operational ask #1, Matt-authorized 2026-05-17):** seven substrate-distinct entries MUST NOT be promoted to allow-list under wind/earth flex pending Phase-1 P1 substrate landing:
   - **thunder, lightning, bolt** (electric substrate; will land at expansion)
   - **holy, divine** (light substrate)
   - **shadow, umbra** (dark substrate)
   - Any future pool-promotion dispatch (rocket, knight-rider-authored, or otherwise) MUST check against this freeze list before recommending allow-list promotion under canonical-four flex
   - Freeze duration: until Phase-1 P1 substrate-expansion dispatch chain ships

2. **Rocket Drift-14 pool-cull dispatch — HOLD LIFTED 2026-05-17 (post-design-doc-landing); awaits Matt fire-approval:**
   - At `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`
   - Substrate-expansion design doc landed (commit `1df535b`); HOLD condition satisfied
   - Amendment scope: D1 rubric extension ships `substrate_native` as third dimension alongside `canonical_pair_leak` + `vfx_catalogue_mapping_clean`
   - **Pool D1 re-score scopes 156 entries across full 6-substrate target state** (fire/water/earth/wind/lightning/holy/shadow), per gandalf substrate-expansion doc § 5.2
   - **CRITICAL: vocab freeze REMAINS ACTIVE during re-score.** Re-score scopes the TARGET STATE the freeze will lift to (when Phase-1 P1 substrate-expansion ships). The 7 frozen entries (thunder/lightning/bolt/holy/divine/shadow/umbra) re-score to substrate-native primary slots BUT do not lift to allow-list until Phase-1 P1 activates the 6-substrate runtime.
   - VS2a/VS2b runtime selection stays canonical-four-bounded (selector allow-list filter unchanged)

**Phase-1 P1 dispatch chain (queued per gandalf cascade order; knight-rider sequences after decisions-log entry lands per gandalf recommendation to draft post-rocket-Drift-14-fire):**

Cascade order per gandalf substrate-expansion doc § 6:
1. ✅ Design doc COMMITTED (`1df535b` 2026-05-17)
2. **Decisions-log entry** (knight-rider drafts AFTER rocket Drift-14 fires so log references unified state; gandalf reviews)
3. **Rocket Drift-14 amendment fires** (awaits Matt approval)
4. **Pool D1 re-score** (within Drift-14 dispatch; scopes 6-substrate target state)
5. **VS2a + VS2b ship on canonical-four** (unchanged; substrate-orthogonal)
6. **Phase-1 P1 dispatch chain:**
   - Rocket: resistance-matrix extension 4×4 → 6×6 (engine-side; symmetry + paired-luminance valence handling per design doc)
   - Rocket: substrate-coherent generation rules
   - Jack-ryan: resist-matrix-extension review (Discipline #1 math-before-code; stress-test on architectural assertion)
   - Gamora: balance-loop modifier table extension + spirit-swap differentiation math validation for **3 new substrate-archetypes (lightning + holy + shadow)** — paired-luminance means holy + shadow are distinct classes, not merged (per gandalf doc § 5.2 correction)
   - Drax: loadout + demo surface updates for 6-substrate selection (deferred to Phase-1 P1, NOT VS2a/VS2b)
   - Star-lord: LLM prompt-template extension for 6-substrate vocabulary
   - Elrond: D1 pool schema extension for `substrate_native` flag + trait-architecture extension (3 new class trait pools per dual-source design 2026-05-12)
   - Gear-affix gating extension (rocket; D1 affix pool expansion across 6 substrates)
7. **Revisit poison/acid as P2 candidate** post-Phase-1 P1

**Freeze enforcement infrastructure (advisory; gandalf surface 2026-05-17):**
- Consider adding `freeze_list` check to dispatch-authoring Gate 1 checklist (knight-rider territory)
- Consider adding `freeze_list` check to pool-curation Gate 2 review (jack-ryan territory)
- Optional: rocket Drift-14 amendment could include `freeze_list_member` boolean as fourth D1 dimension (surface to rocket scoping as side-note, not blocking)
- Gandalf will audit pool weekly during Phase-1 P1 as backstop

**Vendor acquisitions (Matt-authorized 2026-05-17 — VFX track per gandalf Track B Section 3 + Matt override on Frostwindz; ENVIRONMENT track per legolas Mode B sweep):**

**VFX track:**
- **CraftPix premium (wood-nature substrate)** — ACQUIRE HIGH PRIORITY. Gates earth-slot rebuild after biological-organic cluster cull (+5-8 allow-list entries projected: root/bark/leaf/petal/vine/moss/lichen/wood).
- **Fellor Crystal pack (gem cluster)** — ACQUIRE MED PRIORITY. Reinforces 13-entry crystal/gem/precious-metal cluster the cull KEEPS.
- **Frostwindz Deathbringer (bone)** — ACQUIRE per Matt override 2026-05-17. Gandalf Track B initially DEFER'd citing canonical-four-bounded biological-organic drift concern. Matt reframe: under expanded 6-substrate cosmology (Branch A above), bone/death/skeleton VFX has natural home in **shadow substrate** (necromancy / lich / shadow-monarch / earth-meta-layer ascended-spirit register) — not forced into earth-flex where the drift concern lives. Sequencing: acquire alongside Phase-1 P1 substrate-expansion dispatch chain so VFX assets land on disk before shadow-substrate selector/render wiring needs them.

**Environment tileset track (Matt-authorized 2026-05-17 post-legolas Mode B sweep):**
- **Foozle Lucifer Dungeon** — ACQUIRE IMMEDIATELY (FREE CC0). Drax pipeline-testing baseline; cost-free option-value; 32×32 retro register acceptable as pipeline baseline pending HD-2D-quality VS2a pack acquisition.
- **Kokoro Reflections Reaper Tileset** — ACQUIRE ($9.99). Death/undead palace/fog theme; 48×48 exact-meter-fit; HD-2D-ADJACENT (gandalf visual inspection needed before VS2a commit).
- **Kokoro Reflections Phoenix Tileset** — ACQUIRE ($9.99). Fire/volcanic palace/lava theme; 48×48 exact-meter-fit; HD-2D-ADJACENT.
- **Kokoro Reflections Naga Tileset** — ACQUIRE ($8.99; richest content 13 MB). Serpentine/water palace/marble theme; 48×48 exact-meter-fit; HD-2D-ADJACENT.

Total environment track cost: ~$29 ($28.97 + free baseline). Kokoro Reflections vendor has 2 additional themed palace packs not surfaced by name in legolas Mode B Top-5 (legolas surfaced 3 of 5; remaining 2 can surface in next legolas session if Matt wants full 5-pack acquisition).

**Downstream cascade for environment tileset acquisitions:**
1. Matt action: license/cost payment for the 3 Kokoro packs
2. Asset download + on-disk placement at `~/Games/reincarnated-demo/public/assets/<vendor>/<pack>/`
3. Drax ingest-pipeline extension for environment tilesets (separate knight-rider-authored dispatch; analogous to monster-ingest pipeline)
4. Gandalf Track B environment-tileset framework authoring (next session per per-seam discipline; gandalf visual-inspect Kokoro samples; Matt VS2a selection)
5. Drax integration: room/hallway renderer extension consuming environment-pack manifest at season-load time (Phase-1 P1 timeline per gandalf commission Track D)

**Files updated:** This CHANGELOG entry; rocket Drift-14 dispatch HOLD note. Gandalf design doc + decisions-log entry pending. Gandalf substrate-expansion design doc should cross-reference Frostwindz acquisition as already-in-hand dark-substrate VFX precedent.

**Cross-references:** Drift-14 cascade (Track A original + Track B + Track A REVERSE); Case D math-impossibility (Fire_Lord V1 mini-boss tier-bump per gandalf 8a89d1b § Case 4); Drift-15 commission (8a89d1b); Engine Option C 4-phase plan (substrate expansion sits Phase-1 P1, not VS2a/VS2b in-scope); Trait architecture 2026-05-12 (dual-source design extends naturally to 6 with per-class intrinsic pool authoring cost noted).

---

## 2026-05-16 — Dispatch Gate-1 rubric codified for knight-rider self-discipline

**Event:** Matt and knight-rider reconciled Gate-1 application during Day-4 close. Strict reading of `knight-rider.md` (Dispatch authoring requirements) says every Pattern B dispatch routes through jack-ryan DESIGN-MODE before publishing. In practice during fast-moving sessions, knight-rider had been bypassing this when Matt's directive was explicit.

**Decision:** Accept the practical cadence; codify the rubric for when Gate-1 IS required so the bypass isn't ad-hoc.

**INVOKE jack-ryan Gate 1 when ANY of:**
- Cross-seam empirical/code investigation (math-before-code per Discipline #1)
- Strategy doc that will produce decisions-log entries
- Conflict-risk with locked decisions or canonical docs
- Specialist work >2-3 hours of complex scope (cost of misdirection is high)
- Schema migrations affecting multiple consumers
- Matt's directive is loose (knight-rider inferring scope, not executing instruction)

**BYPASS when ALL of:**
- Matt's directive is explicit and well-scoped
- Single-seam ownership, clear authority
- Reversible / low blast radius
- No new design positions encoded
- Specialist has straightforward execution path

**Retrospective application** (Day-4 session): 7 of 9 bypasses were principled; 2 of 9 (gandalf form-bias-cadence strategy + star-lord tier-1 coverage investigation) should have invoked Gate 1. The two misses were in the highest-stakes categories — strategy doc + cross-seam empirical — which is exactly where the rubric now triggers INVOKE.

**Operational cost of Gate 1:** ~15-30 min for a Pattern A subagent of jack-ryan with the draft dispatch as the prompt. Cheap insurance against multi-hour specialist misdirection.

**Files updated:** No agent-definition files touched (the rubric is in this CHANGELOG; knight-rider applies via self-discipline). If the rubric proves stable through subsequent sessions, fold into `knight-rider.md` Dispatch authoring requirements as a formal section.

---

## 2026-05-16 — Dispatch-flow discipline reinforced: flagged-but-not-dispatched items route through knight-rider

**Event:** During Day 4, star-lord performed an opportunistic session-scan pass and autonomously executed the `summary_formatter.py` `actual_winrate` → `convergence_winrate` fix that gamora had flagged as a cross-seam item. The fix was technically correct — in-seam (star-lord owns `output/`), mathematically grounded by B10.4 Option 2 semantics, Discipline #12 honored via explicit comment — but bypassed the dispatch flow.

**Why this matters:** The team's review process depends on every substantive change being attributed to a knight-rider-authored dispatch with explicit acceptance criteria, required-reading, and (where applicable) Gate 1 review. Specialists picking up flagged-but-not-dispatched items breaks the audit trail:
- Lost attribution — work appears in commits but doesn't trace to a dispatch
- Missed Gate 1 — Matt's pre-execution awareness is bypassed
- Audit gap — the retrospective can't reconstruct "what was approved when"

**Rule, normative across all specialist agents:** if a specialist notices an open item in a handoff, an AGENT_STATE cross-seam flag, or any carry-forward queue that is in their seam but has no knight-rider-authored dispatch, **they do NOT pick it up autonomously**. They surface it to knight-rider and request a dispatch. The cost of asking is tiny.

**Knight-rider's role:** when a specialist surfaces a flagged item, knight-rider's response is usually inline-rapid — a small dispatch authored in the same conversation turn. The bottleneck is not authoring time; it's attribution discipline.

**Files updated:** `.claude/agents/star-lord.md` (added the rule under Agent-specific rules). The rule should propagate to other specialist agents (rocket, gamora, drax, elrond, legolas) the next time their definitions are touched — non-blocking sweep.

---

## 2026-05-16 — Parallel-session `git add -A` race condition (new failure mode)

**Event:** During Day 4, knight-rider staged a decisions-log.md edit + L157 cosmetic fix on the engine repo, then ran `git commit` with a substantive multi-line message documenting the 7-entry batch landing. The commit failed with `nothing added to commit but untracked files present`. Investigation showed that star-lord's parallel session — running in another terminal at the exact moment — had executed its own commit (`9e3a458 chore: update AGENT_STATE — c1f02ca hardening + research-db cleanup complete`) which **swept knight-rider's staged decisions-log changes into star-lord's commit**.

**Functional outcome:** All decisions-log content landed correctly on main (the diff in `9e3a458` matches what knight-rider staged exactly). But attribution is ambiguous: the commit message describes star-lord's AGENT_STATE work, while the diff contains the gate-cleared decisions-log batch. Knight-rider's intended commit message — which would have made the landing visibly attributable in git log — was lost. No corrective action taken because `9e3a458` is already pushed to `origin/main` and amending would require force-push.

**Root cause:** Star-lord (or its commit helper) used a wide staging pattern (`git add -A` or `git add .`) that picked up any staged changes in the working tree rather than naming specific files. Combined with two terminals committing to the same repo in the same minute, this guaranteed cross-session contamination.

**Mitigation going forward:**
1. **Specialists must stage by explicit file path** — `git add path/to/file` not `git add -A` / `git add .` / `git commit -am`. Already mentioned in knight-rider's commit protocol but never required of specialists. This makes it normative for all agents.
2. **Knight-rider should not commit engine files while another agent session is committing in the same repo.** When both are running concurrently, knight-rider waits for the other session to settle (or dispatches the commit to the specialist instead of doing it directly).
3. **Specialist commit messages should describe ONLY their own staged changes** — if the message says "chore: update AGENT_STATE" but the diff also touches `decisions-log.md`, that's a smoke signal worth checking pre-commit.
4. **Consider a pre-commit hook** that lists changed files vs the commit message to catch attribution mismatches. Out of scope for today; flagged for future tooling work.

**Files updated:** No new files. Lesson captured here + in `skill_handoff_2026-05-16.md`.

---

## 2026-05-16 — Catalogue work patterns codified: authority tiers, viability gate, score-don't-filter

**Event:** Three structural patterns governing the new agents' catalogue work were locked. These extend the team's operating discipline and address concrete failure modes surfaced during the demo1 phase.

**Pattern 1 — Authority tiers explicit.** The team now has four authority tiers codified in AGENTS.md:
- Tier A: senior critics/stewards (gandalf, jack-ryan) with escalation privileges
- Tier B: orchestrator (knight-rider)
- Tier C+: implementers with steward authority within their domain (elrond — data architecture)
- Tier C: implementers/specialists (Guardians + legolas)

Elrond explicitly sits at C+, not A. He owns data architecture within his seam authoritatively but does not critique outside it. Escalation through knight-rider only; no parallel-to-Matt privilege.

**Pattern 2 — Viability gate for catalogue work.** Before any full Legolas catalogue crawl, a three-track sample review:
- Structural (elrond) — metadata, schema-fit, license, decomposition signal
- Wiring (drax) — pixi.js consumption viability
- Design (gandalf) — thematic and style-register coherence

All three must pass. Addresses the demo1 failure mode where agents brought back sprites that couldn't be wired due to missing body/head/weapon decomposition.

**Pattern 3 — Score-don't-filter for catalogue data.** Legolas crawls widely; assets are scored by style register as curated metadata; the locked style register becomes a **consumption-time filter**, not a crawl-scope constraint. Preserves pivot flexibility — if engine/story/design/experience needs shift the style register, the catalogue already contains the data.

**Elrond's first major task locked:** comprehensive data-architecture audit before any new schema work. Audit covers all data stores across all four repos; produces baseline at `research/curated/data-architecture-audit-<date>.md`; grounds all subsequent Elrond work.

**Files updated:** `gandalf.md` (style-register scope addition); `legolas.md` (viability-gate protocol + score-don't-filter + expanded metadata schema); `elrond.md` (authority tier C+ codified; data-architecture audit as first task; viability-gate structural-track role); `AGENTS.md` (authority tiers + viability-gate + score-don't-filter as team-level patterns).

**Files created:** `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (external research contribution captured as durable knowledge — Tier 1/2/3 element vocabulary, source list, style-register observations).

---

## 2026-05-16 — Three agents added: gandalf, legolas, elrond (6 → 9 entities)

**Event:** The synthetic engineering team expanded from 6 entities to 9, adding generative-side design critique, research, and data stewardship capabilities.

**Agents added:**

- **`gandalf`** (Opus) — Story and Design Steward. Generative-side peer to jack-ryan. Pushes back hard on design drift; recommends thematic and player-experience improvements proactively. Layered persona: White Wizard, cross-development-house veteran (anime/isekai houses, founding Diablo team across all four PC titles + Immortal). Has parallel-escalation privilege — can recommend rescoping to knight-rider AND Matt simultaneously. Two-phase onboarding (read project + immediate preliminary deliverable, then post-Legolas-research updated deliverable).

- **`legolas`** (Sonnet) — Researcher and Scout. Two modes: Mode A analytical research (web, genre knowledge, design retrospectives); Mode B systematic catalogue crawl (2D sprite libraries, Unity Asset Store, etc.). Read-only across all sources; outputs structured findings to `agentic_orchestration/research/`.

- **`elrond`** (Opus) — Data Steward. Owns external/cross-cutting data layers (research DB, catalogue DB, abstraction-analysis tables). Schema design, curation, emergent-grouping analysis. Boundary with star-lord at engine-side telemetry — coordination via ADR-004 (MIGRATION.md).

**Rationale:**

- The form-bias deep dive (2026-05-14) surfaced a real gap on the generative-side of design critique. Jack-ryan stress-tests technical/process; nothing in the prior team stress-tested thematic/experiential dimensions. Gandalf fills this gap.
- The catalogue-based form-bias resolution path (Matt's 2026-05-16 design decision, captured in doc 37 update) requires systematic asset-library crawling at scale plus emergent-grouping abstraction analysis. Legolas + Elrond are the right shape for this work.
- Knight-rider's research-pass improvisations (dispatching star-lord for the fight-log granularity research; ad-hoc Explore agents) were filling a Legolas-shaped gap. Now those passes route through the correct owner.

**Structural patterns established:**

- **Critique-pair pattern:** jack-ryan + gandalf form the two-sided critique pair (technical/process + thematic/experiential). Knight-rider invokes both during decision loops when appropriate.
- **Research + data pattern:** legolas + elrond form the knowledge-acquisition pair. Commissions flow from knight-rider or gandalf; raw output → curated structure → abstraction analysis.
- **Gandalf's parallel-escalation asymmetry** with jack-ryan is intentional and codified. Design issues escalate to Matt directly; technical issues route through knight-rider. Revisit if asymmetry causes friction.

**Files created:**
- `.claude/agents/gandalf.md`
- `.claude/agents/legolas.md`
- `.claude/agents/elrond.md`
- `agentic_orchestration/research/` directory tree (subdirs: knowledge/, catalogue/, commissions/, curated/, scripts/) with README

**Files updated:**
- `agentic_orchestration/AGENTS.md` — topology 6 → 9 entities; new seam descriptions
- `canonical/37-form-bias-diagnosis-and-recovery.md` — catalogue design decision incorporated (Matt's 2026-05-16 update)

**Immediate next step:** gandalf first-invocation Phase 1 (read project + produce preliminary bullet-point deliverable across Overall Game Design, Player Journey, Storytelling/Dramatic Themes). Phase 2 follows after Legolas Mode-A research returns.

---

## 2026-05-16 — Catalogue-based form-bias resolution path (doc 37 update)

**Event:** Matt locked a design decision that reshapes the form-bias work's empirical resolution path.

**Decision:** The 3-consumer CV-3D-generation approach (file 29's highest-risk item) is replaced as the primary path by a **catalogue-based mapping** approach for both 2D and 3D content. Crawl all major 2D sprite libraries + Unity Asset Store; build catalogue database with per-asset metadata (cost, license, dimensions, style); analyze for emergent groupings; use groupings as the engine's embodiment vocabulary.

**Rationale:**
- Validates against demo1's already-working JSON-to-sprite mapping pattern
- Retires the highest-risk CV-3D-generation item
- Makes form-bias resolution **empirical** rather than aspirational — abstractions are derived from what catalogues actually contain, not from what designers wish existed
- Quality gate: ~25% seasonal failure rate acceptable; non-conforming seasons discarded; one-week cohesion floor sufficient (not perfect form match)

**Implications:**
- Closes doc 37 § 10.2 open #4 ("Unit of embodiment variation") empirically
- Provides empirical grounding mechanism for doc 37 § 6 cipher architecture
- Structurally enforces Discipline #13 — catalogue IS the structural constraint, not a conversational pillar that can drift
- Spins up the legolas + elrond agent pair to execute the research and analysis

**Status:** Active; doc 37 updated; legolas + elrond agents created to execute.

---

## 2026-05-16 — Permission allowlist switched to bypassPermissions mode

**Event:** `~/.claude/settings.json` `defaultMode` switched from `"acceptEdits"` to `"bypassPermissions"`.

**Change:** All permission prompts now skipped globally. Deny list (18 destructive operation patterns) still enforced. Allow list retained as documentation of expected normal operations.

**Rationale:** Routine permission prompts were creating significant workflow friction without commensurate safety benefit. The deny list is the actual safety floor — it catches the operations that matter (force-push, hard-reset, rm-rf, sudo, dd, mkfs, chown/chgrp, force-clean, force-delete-branch). Everything else is friction.

**One-time activation:** First session after the change requires user acceptance of the bypass-mode confirmation dialog. Subsequent sessions don't re-prompt.

**Reversibility:** Trivial — revert to `"acceptEdits"` or `"default"` if the bypass mode produces unexpected behavior.

---

## 2026-05-15 — Form-bias structural diagnosis captured (doc 37 draft 2)

**Event:** Major design conversation between Matt and knight-rider produced a structural diagnosis of humanoid-form bias in the engine, with five positions locked in conversation and six open questions identified.

**Artifact:** `canonical/37-form-bias-diagnosis-and-recovery.md` (draft 2) — incorporates jack-ryan Gate 1 PASS WITH FLAGS findings and Matt's position-locks.

**Locked positions (in doc 37 draft 2):**
- Position C — slot-as-functional-mechanic + embodiment-as-narrative-skin
- Position (ii) — abstracted mechanical signatures; cipher = resistance-translation only
- Smart-loot in-season + spirit-conversion post-Phase-0
- Three body-swap gear rules (Trial / doppelganger / death)
- Ailment-damage-signatures re-activated as load-bearing dependency under Position (ii)

**Diagnosis framing:** This is **structural realignment to realize latent design intent**, not a pivot — the project name "Reincarnated," the Spirit Guide module name, and the originating isekai premise all carried non-humanoid intent that drifted humanoid via implementation defaults. Per jack-ryan WARN 1: scope is multi-seam schema migration (ADR-004 territory), not documentation cleanup.

**Rationale:** Catching structural drift before it ossifies into more seasons of generation. The diagnosis surfaced two engineering-discipline candidates (#13 implicit-pillar drift, #14 internal-vs-generative schema separation) — both have multiple empirical instances in the project, strengthening the case for codification.

**Status:** Working positions captured; **next steps gated on Matt's cadence choice (Option I/II/III)**. Decisions-log entries + Discipline #13/#14 drafts queued.

---

## 2026-05-15 — Discipline #13 + #14 candidates surfaced

**Event:** Two engineering-discipline candidates emerged from the form-bias diagnosis with multiple independent empirical instances.

**#13 — Implicit-pillar drift.** Design intent that isn't structurally enforced drifts during implementation. Counter: pillars must be structurally enforced (schema, tests, dispatch acceptance criteria, or decisions-log entries). *"We agreed in conversation"* is not enforcement.

**#14 — Internal-vs-generative schema separation (reviewable check).** When introducing or modifying any LLM-visible category, the prompt-construction code must not expose canonical mechanical labels — per-instance vocabulary only.

**Empirical instances backing the candidates:**
- Spirit-swap as non-humanoid pillar → drifted humanoid via gear/class axes
- Form-agnosticism implicit in project name → drifted humanoid via implementation defaults
- Canonical four = "Earth-realm cipher only" → leaked into seasonal flavor surfaces
- D1 rubric = "Earth-realm humanoid-fantasy element naming" → never named, drifted unexamined

**Status:** Drafted in doc 37; pending Matt approval for `engineering-disciplines.md` addition.

---

## 2026-05-15 — Permission allowlist consolidated to user-level

**Event:** `~/.claude/settings.json` updated with comprehensive permission rules covering all four repos in the Reincarnated ecosystem.

**Change:** 98 allow rules + 18 deny rules + `defaultMode: "acceptEdits"` + `additionalDirectories` covering reincarnated-collaboration, reincarnated-engine, reincarnated-demo, reincarnated-loadout.

**Rationale:** Per-repo `settings.local.json` files had accreted ad-hoc allows over many sessions, with inconsistent coverage. User-level consolidation applies uniformly across all agents and all repos. Destructive operations (force-push, hard-reset, rm-rf, etc.) remain denied — safety preserved.

**Impact:** Reduces routine prompts for all future agent sessions. Sessions running at the time of the change did NOT pick up the new rules; only new sessions get the benefit. Per-repo `settings.local.json` files retained (additive to user-level).

---

## 2026-05-15 — Dispatch protocol gaps surfaced (two process flags)

**Event:** Two distinct dispatch-pickup failure modes were exposed during Day 2 execution. Both warrant template fixes in `agentic_orchestration/dispatches/README.md`.

**Failure 1 — Grep-heuristic false positive (drax).** Drax used `grep -l "## Completion record"` to detect completed dispatches at session start. The dispatch template contains `## Completion record` as a section header for instructions to be filled in — the grep matched the literal header regardless of whether anyone had filled it in. Drax silently skipped the v0.5.1 dispatch and started Tier 3 housekeeping; self-corrected after Matt prompted.

**Failure 2 — HELD-status language ambiguity (drax v0.6).** The v0.6-encounter-viz dispatch was marked **HELD** in the prior session's handoff. Drax read "HELD" as *"wait for the metric data that may inform the mechanism viz"* and executed anyway (interpretation: the dispatch's actual scope didn't depend on the metric data, so HELD didn't apply to it specifically). Work was sound; process miss only.

**Fix to land in dispatches/README.md:**
1. Add explicit `**Status:** PENDING` header to dispatch template — flips to `COMPLETE` only when completion record is filled in. Agents check `Status:` field, not section-header presence.
2. HELD-dispatch language must explicitly state: *"Do not execute. Knight-rider will confirm when this dispatch is active."* No ambiguity.

**Status:** Captured but not yet implemented across template + existing dispatches. ~30 min of work for the next session.

---

## 2026-05-14 — Tag protocol clarified: milestone tags require knight-rider confirmation at closure

**Event:** ADR-003 tag protocol tightened based on Day 1 operating experience.

**Ruling (Matt, 2026-05-14):** Milestone tags (no seam prefix, e.g., `v1.3-b10-2-pack-proxy`) require developer to **pause and confirm with knight-rider before cutting the tag**. Knight-rider escalates to Matt if the scope warrants it. Upfront dispatch approval is NOT sufficient on its own — confirmation is required at closure time.

**What triggered this:** gamora tagged `v1.3-b10-2-pack-proxy` on dispatch-approval authority without a closure check-in. Tag was retrospectively valid (dispatch named it as acceptance criterion and Matt approved the dispatch), but the process gap was identified.

**Going forward:** All dispatch scope checklists will include an explicit "Confirm with knight-rider before cutting milestone tag" item. Seam-prefix intermediate tags (e.g., `gamora/v1.3-b10-2-pre-impl`) remain developer-autonomous.

---

## 2026-05-14 — Working branch convention updated: stage-a2 → main (engine)

**Event:** Matt directed that all engine development continue on `main` going forward. `stage-a2` branch is retired as the active working branch.

**Change:** `CLAUDE.md` §Key conventions updated — "Working branch (engine): `stage-a2`" → "Working branch (engine): `main`".

**Rationale:** Engine was already on `main` at Day 1 startup (post-B10.1 merge). Aligning the documented convention to reality avoids ambiguity for all agents reading CLAUDE.md. Existing tags (e.g., `v1.3-b10-1-structure`, `v1.3-b14-5-secondary-loop`) remain valid; new tags will be cut from `main`.

**Impact:** All specialist agents (gamora, rocket, star-lord) should treat `main` as the base branch. Tag protocol (seam-prefix intermediates, Matt-approved milestones) unchanged.

---

## 2026-05-13 — Team established (Day 0)

**Event:** Founding of the 6-entity synthetic engineering team.

**Entities:**
- Matt (Senior Architect, human)
- knight-rider (Opus, orchestrator)
- jack-ryan (Sonnet, analyst/QA)
- rocket (Sonnet, content generation)
- gamora (Sonnet, simulation + spirit_guide)
- star-lord (Sonnet, output/telemetry/llm)
- drax (Sonnet, presentation: demo + loadout)

**Founding documents:**
- `AGENTS.md` — topology, scope map, 7 cycle-trimming tactics
- `GOVERNANCE.md` — 8 founding ADRs
- `REVIEW_PROCESS.md` — 5 principles + change lifecycle + file-type rules
- `skill_handoff_2026-05-13.md` — Day 0 project state snapshot
- `.claude/agents/<name>.md` — 6 agent definition files

**Rationale:** Solo development hit four recurring bottlenecks (context-load tax, cross-seam misalignment, Matt as review bottleneck, late-caught design-principle violations). The team is structured to attack all four via specialization + durable handoffs + tiered review. Primary goal: trim dev cycles. Secondary goal: enable parallelism across genuinely independent seams.

**Pre-history:**
- 2026-05-12 — first BOOTSTRAP_AGENTIC_TEAM.md drafted in `~/Games/reincarnated-collaboration/`. Initial bootstrap session run, partially completed (6 agent files drafted), then terminated. Partial state cleaned and backed up to `.bootstrap-backup-2026-05-13/agents-partial/`.
- 2026-05-13 — strategic review identified that the bootstrap's seam-split had three issues (no loadout owner, star-lord seam too wide, no cycle-trimming tactics). Path B (direct artifact drafting with Matt review) chosen to address.

**Initial state of project:**
- Engine on `stage-a2` branch, tag `v1.3-b14-5-secondary-loop` + `v1.3-b10-1-structure`
- Loadout production URL live at `https://reincarnated-loadout.vercel.app`, tag `v0.3.3-sample-gear`
- Demo (demo1) shipped 2026-05-08
- Most recent season: Yomi (`season_002328`), validation passed
- 12 engineering disciplines codified
- Decisions-log captures all locked design decisions

**Next milestone:** First operational session (planned for 2026-05-14). Two candidate first tasks: gamora B10.2 + drax loadout gear effects. Both have clear scope and contained risk.

---

## How to extend

Append entries above this section. Date format: `YYYY-MM-DD`. Title format: brief noun phrase describing the event. Body: what changed, why, references.

Examples of events that warrant an entry:
- New ADR adopted or existing ADR amended
- Agent added, removed, or scope re-allocated
- Tactic adoption confirmed or revised (e.g., "MIGRATION.md pattern proved valuable in 5 of 5 cross-seam changes — keep")
- Authority delegation expanded or restricted
- New repo added to team scope

Examples of events that do NOT warrant an entry (these belong in their respective git repos):
- Individual feature commits
- Bug fixes
- Routine deploys
- Per-seam tag events (unless milestone level)
