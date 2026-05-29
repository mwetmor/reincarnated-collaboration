# Phase A2 Cascade Resumption — Concern #1 + Concern #2 Resolution Plan

> **STATUS:** CURRENT (load-bearing as of 2026-05-29) — Durable resolution plan for cascade halted at A2-1 RE-FIRE MATERIAL FAIL (commit `e99b000`). Authored at Matt-surface point; ratified by Matt 2026-05-29 in-session for self-executable cascade resumption.

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — Phase A2 cascade HALTED at A2-1 RE-FIRE MATERIAL FAIL; resolution sequence below restores cascade under hive-mind decision-routing
**Authority:** Matt 2026-05-29 (this session — Path D ratified for Concern #2; Path A ratified for Concern #1; cohesion-threshold WARN-watch ratified as capture-and-watch not halt-and-surface; Disc #42a Instance-5 capture deferred to Matt re-engage)

**Companion docs (required next-KR-session first reads in order):**
1. `agentic_orchestration/knight-rider/notes/2026-05-29-phase-a1-close-phase-a2-handoff-memo.md` — Phase A1 close + Phase A2 sequencing
2. `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-unattended-cascade-resume-memo.md` — durable session-state from cascade entry
3. THIS plan (Concern #1 + #2 resolution sequence)
4. `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-cascade-resumption-fire-prompt.md` — paste-ready KR fire prompt
5. `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Phase A1 closure artifact
6. `agentic_orchestration/cycle-14-hive-mind-state.md` — live state file
7. `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` — A/B comparison protocol (runs at Wave 5 close; independent of FACTION_VISIBILITY flag)

---

## 0. Why this plan exists

A2-1 RE-FIRE returned MATERIAL FAIL at commit `e99b000`:
- Phase 7: 0/18 shipped_worthy (acceptance_rate 0.0; threshold ≥12/18)
- Phase 5: Wave A NOT FIRED ($0.00 LLM cost; placeholder mode active)

Two distinct architectural concerns surfaced; both require resolution before cascade can resume:

**Concern #1 — Phase 7 synthetic-kit KPM calibration gap.** Phase7SyntheticKit magnitude=3000 produces KPM 7-26× below W-α6 ENCOUNTER_COHORT_KPM_BAND across all 6 encounter types. Calibrated against pre-W-α6 boss-oriented cohort band; W-α6 (2026-05-28) replaced calibration; gap masked by Phase 7 import bug until A2-1-FIX cleared it.

**Concern #2 — Phase 5 LLM cohesion judge hardcoded to placeholder mode.** `wave5_season_orchestrator.py:89` `FACTION_VISIBILITY="invisible"` SKIPS Wave A (faction LLM) AND Wave B (per-kit identity LLM); hardcoded `assert` at lines 1264-1265 enforces. LLM cohesion judge NEVER exercised in current v1 production configuration. Matt directive: removal of LLM runs from v1 is off the table.

Resolution sequence below restores cascade under R48.4 single-seam discipline + hive-mind decision-routing.

---

## 1. Resolution sequence (R48.4 single-seam throughout)

### Step 1 — Concern #1 (gamora Path A — synthetic-kit KPM recalibration)

**Owner:** gamora
**Effort:** ~1-2h (math note + parameter sweep + completion record)
**Dispatch:** KR-authored under hive-mind decision-routing (in-scope orchestration)

**Work:**
- Math note: derive new Phase7SyntheticKit magnitude scaling such that synthetic KPM falls within W-α6 ENCOUNTER_COHORT_KPM_BAND across all 6 encounter types
- Parameter sweep: confirm in-band coverage at the new magnitude across the 6 encounter types
- Completion record: capture revised magnitude + sweep verification + cross-reference to W-α6 calibration anchor

**Acceptance criterion:** synthetic produces KPM in-band across 6 encounter types; ready for Phase 7 gate consumption in A2-1 RE-FIRE.

**Discipline composition:**
- Disc #1 math-before-code
- Disc #2 smoke-test before full fire
- Disc #18 math hotspot consultation (W-α6 is the calibration anchor; gamora seam-internal — no extension hotspot)
- Disc #48 R48.4 single-seam (no parallel rocket fan-out)

### Step 2 — Concern #2 (rocket Path D — flip FACTION_VISIBILITY to visible)

**Owner:** rocket
**Effort:** ~0.5-1h (single-file amendment + assert lift + docstring update + completion record)
**Dispatch:** KR-authored under hive-mind decision-routing (in-scope orchestration; Matt-ratified direction)

**Work:**
- `wave5_season_orchestrator.py:89` — flip `FACTION_VISIBILITY: str = "invisible"` to `"visible"` (Reincarnated v1 default)
- `wave5_season_orchestrator.py:1264-1266` — lift / update assert to match new default
- `wave5_season_orchestrator.py:12` — update docstring "Phase 5 — Cohesion-judge LLM: Phase5Orchestrator Wave A + F-C + Wave B (faction_visibility=visible)"
- `wave5_season_orchestrator.py:89` inline comment — update "Reincarnated v1 default; Wave A skipped" → "Reincarnated v1 default; Wave A + F-C + Wave B fire"
- `wave5_season_orchestrator.py:802-806` — update placeholder-mode commentary to reflect visible mode behavior
- Completion record: capture flag-flip + assert-lift + downstream-consumer audit (verify Phase 5 + F-C + Phase 7 consume real LLM outputs as designed)

**Acceptance criterion:** orchestrator fires Wave A + F-C + Wave B in visible mode; ExportFactionCluster populated with real LLM labels; ExportFactionRelationship records emitted; Phase 7 consumes real `cohesion_judge_confidence` scores.

**Discipline composition:**
- Disc #11 empirical inspection — verify assert lift does not break module-load assertions elsewhere
- Disc #42a framing-audit — Q1/Q2/Q3 at dispatch consumption (any other pre-imposed assumption in the orchestrator gating LLM exercise?)
- Disc #48 R48.4 single-seam (Step 1 must close before Step 2 fires)

### Step 3 — jack-ryan Gate-2 review

**Owner:** jack-ryan
**Effort:** ~0.5h (Pattern E pre-auth; PASS-with-WARN/INFO fire-and-continue)
**Trigger:** Step 1 + Step 2 completion records committed

**Work:**
- Review Step 1 + Step 2 outputs against critique-pair Gate-2 review principles
- Disc #43 design-quality audit (A1-A5) — does the work advance Cycle 14 v1 close criterion?
- Disc #42a framing-audit Q1-Q6 — any pre-imposed assumption catch?
- Verdict: PASS / PASS-with-WARN / PASS-with-INFO / BLOCK

**Pattern E pre-authorization:** PASS-with-WARN or PASS-with-INFO fire-and-continue per Phase A1 closure record § 7. BLOCK halts cascade + surfaces to Matt queue.

### Step 4 — A2-1 RE-FIRE cascade resumption

**Owner:** rocket + gamora + star-lord (LLM cost guard)
**Effort:** ~1d production
**Trigger:** Step 3 Gate-2 PASS

**Work:**
- Re-fire season_001 production under both fixes
- Phase 2-7 full pipeline; ≥12/18 emit threshold; Wave A + F-C + Wave B LLM exercised
- star-lord cost-guard projects mid-cascade; surfaces to Matt queue at $50 projection approach

**Acceptance criterion:** ≥12/18 shipped_worthy at Phase 7 + Wave A + F-C + Wave B LLM cost recorded + telemetry captured.

### Step 5 — Gate-2 + cascade through A2-2 through A2-7

Per existing Phase A2 sequence in Phase A1 closure record § 7 and resume memo § 3. Pattern E autonomous-pair ratification for each Gate-2; per-workstream push after each Gate-2 PASS.

---

## 2. Total wall-clock estimate to A2-1 RE-FIRE PASS

| Step | Effort | Cumulative |
|---|---|---|
| 1 (gamora KPM recalibration) | ~1-2h | ~1-2h |
| 2 (rocket flag flip) | ~0.5-1h | ~1.5-3h |
| 3 (jack-ryan Gate-2) | ~0.5h | ~2-3.5h |
| 4 (A2-1 RE-FIRE) | ~1d production | ~1d + 3h |

Cascade resumes within ~3-4h of next KR session firing; A2-1 RE-FIRE PASS verdict within ~1d of session entry.

---

## 3. Surface-to-Matt conditions (additions to existing $50 / R48.4 / Gate-2 BLOCK)

| Condition | Trigger | KR action |
|---|---|---|
| Cohesion-threshold scaffold-surface | Phase 7 `cohesion_judge_confidence` systematically below 0.75 across A2-1 RE-FIRE kits (scaffold-calibrated threshold; never empirically validated against real LLM scores) | Capture distribution in telemetry; surface to Matt queue IF systematic under-0.75 pattern observed (Pattern B design call for Matt re-engage); do NOT halt cascade for scattered under-0.75 (treat as scaffold-discovery; capture-and-watch) |
| A2-1 RE-FIRE second-material-fail | A2-1 RE-FIRE returns ≥1 material-fail finding distinct from Concerns #1 + #2 | Halt cascade; surface to Matt queue (no re-fire loop) |
| Wave A + F-C + Wave B cost overrun | star-lord projects cascade LLM spend toward $30/season (extrapolated 3 seasons → projected $50 approach) | Surface to Matt queue per existing $50 soft cap; do NOT hard-halt unless materially excessive (>$60 projected) |
| Step 2 framing-audit catch | Disc #42a Q1-Q6 surfaces pre-imposed assumption in orchestrator gating LLM exercise beyond FACTION_VISIBILITY | Halt cascade; surface to Matt queue |
| Step 1 or Step 2 Disc #48 R48.4 violation | Pre-flight `vm_stat` shows < 1 GB free RAM | Halt before dispatch fire; surface to Matt queue |

---

## 4. What KR will NOT do without Matt evidence

- Touch the A/B comparison protocol itself (per `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md`; runs at Wave 5 close post-cascade; independent of FACTION_VISIBILITY flag)
- Recalibrate the Phase 7 `cohesion_judge_confidence >= 0.75` threshold (scaffold-flag; Pattern B design call for Matt re-engage if systematic under-0.75 observed)
- Player-facing faction-architecture commitments (deferred-commitments recognition record at `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` stands; orchestrator flag controls generation-side LLM exercise; player-side faction surfacing is a separate seam)
- Decisions-log canonical writes beyond completion records (jack-ryan owns decisions-log writing authority; deferred to Matt re-engage)
- Disc #42a Instance-5 addendum (deferred to Matt re-engage; not blocking)
- Disc #40 scaffold-discipline data point capture (the `invisible`-default + hardcoded `assert` survived to production-fire; worth one-paragraph capture at Matt re-engage; not blocking)

---

## 5. Disciplines composition map

| Discipline | Where it applies in this plan |
|---|---|
| Disc #1 math-before-code | Step 1 gamora math note before parameter sweep |
| Disc #2 smoke-test | Step 1 sweep before A2-1 RE-FIRE consumption |
| Disc #11 empirical inspection | Step 2 rocket assert-lift verification |
| Disc #18 math hotspot consultation | Step 1 W-α6 calibration anchor (gamora seam-internal; no extension hotspot) |
| Disc #40 scaffold-flagging | Cohesion-threshold WARN-watch + assert-survival data point (capture at Matt re-engage) |
| Disc #41 substrate-led discipline | Path D respects substrate-led emergence (PM-1 multimodal clustering produces emergent factions; LLM names them; substrate-as-vote preserved) |
| Disc #42a framing-audit | Step 2 dispatch consumption Q1-Q6; Matt re-engage Instance-5 capture |
| Disc #43 design-quality wave-close audit | Step 3 jack-ryan Gate-2 A1-A5 questions |
| Disc #45 vocabulary lock | Phase 5 outputs use locked vocabulary (kit / faction / form / flavor element); no class/role/archetype non-exempt |
| Disc #46 §7 per-cell bounding | Phase 4 + Phase 7 queries per-cell bounded (no change from existing) |
| Disc #48 R48.4 single-seam | Step 1 → Step 2 → Step 3 → Step 4 strict single-seam throughout |
| Recognition → empirical validation → commit | Phase A2 IS the empirical validation gate for D9 close; this plan is the empirical-evidence-gated resumption |

---

## 6. Cross-references to other session artifacts

| Artifact | Path |
|---|---|
| Phase A2 KR fire prompt (cascade resumption — paste into new KR session) | `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-cascade-resumption-fire-prompt.md` |
| Original Phase A2 fire prompt (consumed by prior cascade-entry session) | `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-kr-fire-prompt-handoff.md` |
| Phase A2 unattended cascade resume memo | `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-unattended-cascade-resume-memo.md` |
| Phase A1 closure record | `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` |
| KR session-boundary memo | `agentic_orchestration/knight-rider/notes/2026-05-29-phase-a1-close-phase-a2-handoff-memo.md` |
| A2-1 RE-FIRE MATERIAL FAIL commit | `e99b000` (KR-authored; 2 concerns enumerated) |
| Phase 7 KPM gap rocket commit | `9f9ed28` + engine `c8586e4` + tag `rocket/v1.0-season-001-re-fire-1-fail-phase7-kpm-gap` |
| A/B comparison protocol (Wave 5 close; independent of flag) | `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` |
| Deferred-faction-commitments recognition record | `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` |
| Disc #42a pushback memo (Instance 1-4) | `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` |
| Engineering disciplines canonical | `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` |

---

## 7. Sign-off

**Authored:** gandalf (story-and-design steward) at Matt-surface resolution point for Phase A2 cascade halt
**Authority:** Matt 2026-05-29 confirmation of plan-as-drafted (Path D simple flip; cohesion-threshold capture-and-watch; Disc #42a Instance-5 deferred)
**For:** the durable resolution-plan capture; KR session-start protocol picks up via own-latest-3-notes; resolution sequence Step 1 → Step 5+ self-executable under hive-mind decision-routing with surface conditions per § 3

**Next-KR-session entry-criterion:** Matt fires new KR session with cascade-resumption fire prompt (companion path § 6). KR onboards via the 7 required first reads above. Cascade resumes Step 1 → Step 5+ per § 1 sequence. Surface to Matt queue at conditions per § 3.
