# Concern #3 Resolution Authorization + Pre-Ratification

> **STATUS:** CURRENT (operational dispatch authorization as of 2026-05-29) — Matt 2026-05-29 confirmed direction + pre-ratification contingent on gamora audit findings. KR consumes this artifact for cascade-resumption-2 sequence under hive-mind decision-routing. Authorization fires post-Matt-paste of new KR session prompt.

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-29 in-session direction: "Confirmed, commit the dispatch authorization. Please pre-ratify the decision for me contingent on findings."

**Companion docs (required KR first reads at consumption):**
1. `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` — original Phase A2 cascade resumption plan (Step 1-5+); cascade fired through Step 4 with material fail → Concern #3 surfaced
2. `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-cascade-resumption-fire-prompt.md` — original cascade resumption fire prompt (still authoritative for carry-forward gates)
3. THIS artifact — Concern #3 resolution authorization + contingent pre-ratification
4. The A2-1 RE-FIRE MATERIAL FAIL Matt-surface commit (KR's surface at `1a8f12c`) — captures Concern #3 technical detail + three resolution path candidates (P3a/P3b/P3c)
5. `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — recognition record; gate (i) empirical evidence accrues from cascade artifacts independent of Phase 7 disposition
6. `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Phase A1 closure record + D13 parallel-fire authorization
7. `agentic_orchestration/cycle-14-hive-mind-state.md` — canonical state file

---

## 0. TL;DR

Phase A2 cascade halted at A2-1 RE-FIRE Step 4 with Concern #3 (Phase 7 mean-encounter-extraction cohort-divisor bug; site `phase7_bridge.py:368` + `gauntlet_sim.py:1068-1076`). Matt confirmed resolution direction:

1. **Gamora audit dispatch** — enumerate callers of `gauntlet_sim.mean_encounters_passed_per_kit` (~15-30min seam-internal)
2. **Audit-finding-routed gamora fix** — P3a or P3c per pre-ratified decision-tree below
3. **Star-lord cost-tracker wire-up** — fix `tracker=None` in Phase 5 LLM path; sequential under R48.4
4. **Jack-ryan Gate-2** — Pattern E autonomous-pair pre-auth carries forward
5. **A2-1 RE-FIRE-2** — cascade resumption
6. **Gandalf gate (i) preliminary assessment** — IN THIS CONVERSATION; uses existing cascade artifacts; no R48.4 conflict (no sub-agent dispatch)

**P3b REJECTED as bug-fix path.** Phase 7 gate-semantics dialogue separable; reserved for separate Pattern B post-cascade-close if Matt elects.

**Pre-ratification (§ 3)** authorizes KR to route P3a vs P3c per gamora audit findings without re-surfacing to Matt EXCEPT for edge cases enumerated in § 4.

---

## 1. What landed (cascade halt context)

| # | Step | Owner | Verdict |
|---|---|---|---|
| 1 | gamora synthetic-kit KPM recalibration (Concern #1) | gamora | ✅ PASS (per-bc_cell_id magnitude table; 18/18 sweep in-band) |
| 2 | rocket FACTION_VISIBILITY="visible" + assert lift (Concern #2) | rocket | ✅ PASS (5 edits; Disc #11 audit clean) |
| 3 | jack-ryan Gate-2 | jack-ryan | ✅ PASS-with-INFO (3 INFOs deferred per resolution plan § 4) |
| 4 | A2-1 RE-FIRE | rocket+star-lord+gamora in-process | ❌ MATERIAL FAIL — Phase 7 0/18 |

**Why Concern #3 surfaced now:** Concerns #1 + #2 short-circuited prior FAILs before mean-aggregate computation became dispositive. With Step 1 + Step 2 architecturally clean, the aggregate-extraction bug became the next-most-load-bearing failure. Healthy issue-surfacing pattern: each layer of fix uncovered the next layer.

**Resolution plan § 3 second-material-fail clause fired correctly:** "A2-1 RE-FIRE returns ≥1 material-fail finding distinct from Concerns #1 + #2 → Halt cascade; surface to Matt queue (no re-fire loop)." KR halted; Matt-surface committed; gandalf invoked for design steward read; Matt confirmed direction.

---

## 2. Concern #3 — technical specification

### 2.1 The bug

| Site | What happens |
|---|---|
| `phase7_bridge.py:340` | Phase 7 runs **1 cohort per kit** (single gauntlet_archetype, by Phase 7 design) |
| `phase7_bridge.py:368` | Phase 7 reads `quality_report.mean_encounters_passed_per_kit` |
| `gauntlet_sim.py:1068-1076` | Mean computed iterating over **ALL 4 COHORT_ARCHETYPES** with hardcoded divisor=4 |

Net: when Phase 7 runs 1 cohort, mean = `actual_pass_count / 4` → max possible value 0.25 → Phase 7 mechanical-gate threshold above that ceiling → 18/18 TIER_1_REJECT universally regardless of synthetic-kit KPM achievement.

### 2.2 Resolution path candidates (per KR Matt-surface)

| Path | Description | Scope | Surgical risk |
|---|---|---|---|
| **P3a** | Access `kit_results[0].encounters_passed(gauntlet_archetype)` directly at Phase 7 bridge call site | Local (Phase 7 bridge only) | Lowest cross-seam blast radius; leaves underlying API footgun for future callers |
| **P3b** | Use `kit_results[0].season_emit` boolean as Phase 7 mechanical gate | Semantic-level change to Phase 7 measurement | **Design call, NOT bug-fix.** Phase 7 gate locked at `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` |
| **P3c** | Divide aggregate mean by `len(p7_cohorts_actually_run)` not fixed COHORT_ARCHETYPES count at source `gauntlet_sim.py:1068-1076` | Upstream-architectural fix | Cross-seam impact risk; need caller-graph audit before commit |

### 2.3 Secondary observation — Phase 5 LLM cost-tracker gap

`tracker=None` in Phase 5 → real LLM spend recorded as $0.00 (actual ~$0.12 unverified). $50/$60 cost guard non-functional this cascade. Actual spend tiny (~$0.12) because Phase 7 short-circuited at 0/18 before further LLM calls fired. Cap wasn't blown, but cap was advisory-only — discipline failure mode, not cost failure mode.

**Disc #40 scaffold-discipline pattern data point.** Two scaffold artifacts survived to production in one cascade: (a) `FACTION_VISIBILITY=invisible`-default + hardcoded assert (resolved Step 2); (b) `tracker=None` in Phase 5 LLM path (queued for resolution this authorization).

---

## 3. Pre-ratified contingent decision-tree (the key section)

Matt 2026-05-29 directive: "Please pre-ratify the decision for me contingent on findings."

KR routes the following per gamora audit findings WITHOUT re-surfacing to Matt:

### 3.1 Gamora audit dispatch (first sub-step)

**Owner:** gamora
**Effort:** ~15-30min seam-internal
**Authority:** KR-authored dispatch under hive-mind decision-routing (in-scope orchestration; Matt-ratified direction)

**Audit scope:**
1. Enumerate ALL callers of `gauntlet_sim.GauntletQualityReport.mean_encounters_passed_per_kit` (or equivalent method per current `gauntlet_sim.py` line 1068-1076 surface)
2. For each caller, determine: (a) does it always populate all 4 COHORT_ARCHETYPES, or sometimes a subset? (b) does it depend on divisor=4 dilution semantics, or is divisor=actual-count semantically equivalent for its use?
3. Audit method signature: does `kit_results[0].encounters_passed(gauntlet_archetype)` exist + accept archetype param (for P3a viability check)?
4. Output: brief audit findings report at `agentic_orchestration/gamora/notes/<date>-concern-3-caller-graph-audit.md`

**Audit success criterion:** complete caller-graph + per-caller semantic-equivalence assessment + P3a viability confirmation OR refutation.

### 3.2 KR contingent routing per audit findings

| Audit finding | Pre-ratified KR action | Rationale |
|---|---|---|
| **Case A — Single caller (only Phase 7 uses the method)** | **Route P3c** — gamora fix at `gauntlet_sim.py:1068-1076` (change to `len(p7_cohorts_actually_run)`-based divisor) | Removes footgun; architecturally honest; no cross-seam impact |
| **Case B — Multi-caller, all callers populate full 4-archetype cohort set in their use** | **Route P3c** — same fix at source | Semantically transparent; same divisor=4 result for full-set callers; correct divisor for Phase 7's partial-set case |
| **Case C — Multi-caller, some callers populate partial cohort sets AND depend on divisor=4 dilution semantics** | **Route P3a** — surgical Phase 7 bridge fix only; gandalf authors P3c-tech-debt-flag note for Cycle 14+ cleanup | Avoids breaking other callers; surgical scope; tech-debt explicit |
| **Case D — Method `kit_results[0].encounters_passed(gauntlet_archetype)` exists + accepts archetype param** | **P3a viable** — route P3a per Case A/B/C rules | Confirms surgical path is implementable |
| **Case E — Method doesn't exist OR doesn't accept archetype param** | **Route P3c regardless of caller count** — P3a is non-viable; fix at source | Forced architectural fix |

**Combined disposition matrix:**

| Caller graph | P3a method viability | KR action |
|---|---|---|
| Single (only Phase 7) | viable | **P3c** (preferred); fallback **P3a** if P3c blocks |
| Single (only Phase 7) | non-viable | **P3c** (forced) |
| Multi, all full-set | viable | **P3c** (preferred); fallback **P3a** if P3c blocks |
| Multi, all full-set | non-viable | **P3c** (forced) |
| Multi, some partial-set + divisor-dependent | viable | **P3a** (surgical) + P3c-tech-debt-flag for Cycle 14+ |
| Multi, some partial-set + divisor-dependent | non-viable | **SURFACE to Matt queue** — neither path clean; design call required |

### 3.3 Star-lord cost-tracker wire-up (second sub-step)

**Owner:** star-lord
**Effort:** ~30-60min seam-internal
**Authority:** Matt-pre-ratified per this authorization (composes with Concern #3 resolution; same R48.4 single-seam queue)

**Work:**
- Wire `tracker=<real_tracker_instance>` in Phase 5 LLM call path (replacing `tracker=None`)
- Validate cost-tracker captures Wave A + F-C + Wave B spend
- Per-call telemetry confirms cost-accumulation
- Disc #11 audit clean

**Fire condition:** after gamora P3a/P3c fix lands; before jack-ryan Gate-2 fires.

### 3.4 Jack-ryan Gate-2 review (third sub-step)

**Owner:** jack-ryan
**Effort:** ~half-day; Pattern E autonomous-pair pre-auth carries forward from Phase A1 closure record
**Authority:** Matt-pre-ratified per Phase A1 Gate (c)

**Work:**
- Critique-pair Gate-2 review of gamora Concern #3 fix (P3a OR P3c) + star-lord cost-tracker wire-up
- Disc #43 design-quality audit (A1-A5)
- Disc #42a framing-audit Q1-Q6
- Verdict: PASS / PASS-with-WARN / PASS-with-INFO / BLOCK

**Pattern E disposition rule:**
- PASS / PASS-with-WARN / PASS-with-INFO → fire-and-continue per Phase A1 closure record § 7 + resolution plan § 1 Step 5
- BLOCK → halt cascade + surface to Matt queue

### 3.5 A2-1 RE-FIRE-2 (cascade resumption-2)

**Owner:** rocket + gamora + star-lord (LLM cost guard now functional)
**Effort:** ~1d production
**Authority:** Matt-pre-ratified per Phase A1 Gate (c) + this authorization

**Work:**
- Re-fire season_001 production under all three concerns resolved (#1 + #2 + #3)
- Phase 2-7 full pipeline; ≥12/18 emit threshold; Wave A + F-C + Wave B LLM exercised with functional cost-tracker
- Star-lord cost-tracker projects mid-cascade; surfaces to Matt queue at $50 projection approach

**Acceptance criterion:** ≥12/18 shipped_worthy at Phase 7 + Wave A + F-C + Wave B LLM cost recorded (functional cost guard) + telemetry captured.

### 3.6 Cascade through A2-2 through A2-7

Per existing Phase A2 sequence in Phase A1 closure record § 7. D13 parallel-fire authorization activates post season_001 Gate-2 PASS (drax Vercel refresh + A/B preliminary + P1-P9 track) per resolution plan § 1.5.

---

## 4. Surface-to-Matt conditions for edge cases (additions to existing § 3 of resolution plan)

| Condition | Trigger | KR action |
|---|---|---|
| **Audit-finding Case C + Case E** (multi-caller partial-set + P3a non-viable) | Both conditions hold per audit | Halt; surface to Matt — neither P3a nor P3c clean; design call required |
| **Unexpected audit-finding pattern** | Audit surfaces patterns not enumerated in § 3.2 matrix | Halt; surface to Matt with audit findings — pre-ratification doesn't cover unenumerated case |
| **P3c-implementation cross-seam blast** | Mid-rocket-implementation, refactor surfaces unanticipated dependent code | Halt; surface to Matt for scope-amendment decision |
| **Star-lord cost-tracker wire-up reveals deeper observability gap** | Wiring `tracker=` exposes additional missing wire-ups OR tracker design issue | Surface to Matt with star-lord findings; may compose into broader Disc #40 cleanup |
| **A2-1 RE-FIRE-2 returns ANOTHER material fail** | RE-FIRE-2 has ≥1 material-fail finding distinct from Concerns #1 + #2 + #3 | Halt cascade; surface to Matt queue (no re-fire loop; existing § 3 second-material-fail clause carries forward to RE-FIRE-2) |
| **A2-1 RE-FIRE-2 returns Phase 7 PASS but Wave A LLM cohesion-judge quality is poor** | Phase 7 mechanical gate passes but cohesion outputs are incoherent (jack-ryan Gate-2 surfaces) | Pattern E BLOCK halts; surface to Matt for design call (Wave A prompt redesign or cohesion-threshold recalibration) |
| **All other resolution plan § 3 conditions** | (existing: cohesion-threshold systematic under-0.75 / LLM cost projection / framing-audit catch / R48.4 RAM-fail / Gate-2 BLOCK) | Per resolution plan § 3 unchanged |

---

## 5. Gandalf gate (i) preliminary assessment authorization

**Owner:** gandalf (in current conversation; no sub-agent dispatch)
**Effort:** ~30-60min reading cascade artifacts + producing assessment
**Authority:** Matt 2026-05-29 confirmed direction ("Authorize gandalf gate (i) preliminary assessment in this thread")
**R48.4 status:** no conflict — gandalf seam in current conversation does NOT dispatch sub-agents; uses cascade outputs that already exist on disk

**Work:**
- Read cascade artifacts: `agentic_orchestration/cycle-14-wave-5-season-001/` directory contents (ExportFactionCluster JSON + ExportFactionRelationship JSON + kit_archive per-kit identity + Phase 7 verdict log)
- Assess Wave A faction-naming coherence (are labels substrate-grounded + culturally coherent?)
- Assess Wave B per-kit identity coherence (do kit names + flavor align with mechanical content?)
- Assess F-C inter-faction relationship coherence (do relationships make cultural sense?)
- Output: gate (i) preliminary verdict at `agentic_orchestration/gandalf/notes/2026-05-29-gate-i-preliminary-assessment.md`

**Composition with recognition record:** assessment validates or refines `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` gate (i) disposition. Wave A + Wave B LLM fired in production for first time ever per Path D flip; outputs exist; Phase 7 0/18 rejection was on mechanical-gate (Concern #3 bug), not cohesion criteria.

**Assessment runs IN PARALLEL with KR coordination** of gamora audit + downstream sequence (no R48.4 conflict; different seams; gandalf works in conversation thread, KR coordinates sub-agent dispatches sequentially).

---

## 6. Composition with existing canon

| Existing artifact | Composition with this authorization |
|---|---|
| `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` | Cascade resumption-2 sequence extends resolution plan § 1 Step 4-5+ with Concern #3 resolution inserted before A2-1 RE-FIRE-2 |
| `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-cascade-resumption-fire-prompt.md` | Carry-forward gates UNCHANGED ($50 soft cap + Pattern E + R48.4 + push pattern); new authorization composes on top |
| `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` | Phase A1 close + D13 parallel-fire authorization UNCHANGED; Phase A2 trajectory adds ~3-6h wall-clock for Concern #3 resolution + cost-tracker fix |
| `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` | Gate (i) preliminary assessment fires in current conversation per § 5 of this authorization; produces preliminary verdict before A2-1 RE-FIRE-2; full gate (i) verdict awaits A2-1 RE-FIRE-2 PASS data |
| `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` | Phase 7 gate semantics PRESERVED — P3a/P3c are mechanical-extraction-bug fixes; gate threshold (gauntlet_pass_rate + cohort midpoint band ±0.25) UNCHANGED; P3b would change semantics but is REJECTED as bug-fix path |
| `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` | Disc #11 + #40 + #42a + #48 + #43 + Pattern E all carry forward per resolution plan + this authorization |

---

## 7. Discipline composition

| Discipline | Application in this authorization |
|---|---|
| **Disc #1 math-before-code** | Gamora audit findings produced before P3a/P3c fix authoring |
| **Disc #11 empirical-inspection** | Pre-ratification gated on empirical audit findings, not blind path-selection |
| **Disc #5 right tool for the validation question** | Caller-graph audit is the cheapest empirical refutation of "P3c is universally safe" assumption |
| **Disc #18 math hotspot consultation** | N/A this work — Concern #3 is implementation-mechanics, not methodology choice at hotspot |
| **Disc #40 scaffold-flagging** | `tracker=None` survival to production is Disc #40 data point; star-lord wire-up fixes the symptom; pattern data captured for Matt re-engage cumulative Disc #40 discussion |
| **Disc #41 substrate-led vocabulary lock** | No vocabulary change in this authorization |
| **Disc #42a framing-audit (Q1-Q6)** | Q1 — what does this authorization assume? (P3c is architecturally clean IF callers conform to enumerated cases; audit validates the assumption) Q2 — what could refute? (Case C + Case E combined OR unexpected patterns) Q3 — refinement is the audit step itself |
| **Disc #43 design-quality wave-close audit** | Jack-ryan Gate-2 applies A1-A5 per existing pattern; this authorization adds no new dimensions to audit |
| **Disc #48 R48.4 single-seam** | Strict sequential: gamora audit → gamora fix (P3a OR P3c) → star-lord cost-tracker → jack-ryan Gate-2 → A2-1 RE-FIRE-2 |
| **Pattern E autonomous-pair pre-authorization** | Carries forward from Phase A1 closure record + resolution plan for jack-ryan Gate-2 on this work |
| **Recognition → empirical validation → commit** | Recognition: gamora-diagnosed three paths + audit reveals truth; validation: gamora audit + jack-ryan Gate-2; commit: P3a or P3c per pre-ratification matrix |

---

## 8. What this authorization does NOT do

- Does NOT pre-ratify Phase 7 gate semantics dialogue (P3b reserved as separable Pattern B post-cascade-close)
- Does NOT modify the resolution plan § 1.5 D13 parallel-fire authorization (carries forward unchanged)
- Does NOT amend the recognition record (gandalf gate (i) preliminary assessment composes; no recognition record edits unless empirical findings warrant)
- Does NOT pre-ratify scope-amendment work surfaced from star-lord cost-tracker investigation (any deeper observability gap surfaces to Matt)
- Does NOT release jack-ryan Gate-2 from Pattern E BLOCK semantics (BLOCK still halts + surfaces)
- Does NOT collapse any of the carry-forward gates ($50 soft cap + R48.4 + push pattern remain intact)

---

## 9. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 confirmation + pre-ratification request

**Authority chain:**
- Matt 2026-05-29 evening: "Confirmed, commit the dispatch authorization. Please pre-ratify the decision for me contingent on findings."
- Composes with Phase A1 closure record Matt 3-gate authorization (RATIFIED) + resolution plan § 1.5 D13 parallel-fire RATIFIED at Gate (c)
- Composes with hive-mind decision-routing directive Matt 2026-05-23 (seam-owner decides per audit evidence; Matt is last-resort escalation)

**For:** the durable operational authorization + pre-ratified contingent decision-tree for Concern #3 resolution; KR consumes at session start; routes per § 3 audit findings WITHOUT re-surfacing to Matt EXCEPT for § 4 edge cases

**Next steps:**
1. KR fires gamora audit dispatch (~15-30min) at next available R48.4 window
2. KR routes P3a vs P3c per gamora audit findings + § 3.2 matrix
3. KR sequences star-lord cost-tracker wire-up
4. Jack-ryan Gate-2 per Pattern E pre-auth
5. A2-1 RE-FIRE-2
6. Cascade through A2-2 → A2-7 per existing Phase A2 sequence + D13 parallel track
7. In parallel: gandalf gate (i) preliminary assessment fires in current conversation thread (§ 5)
