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

## 1.5 D13 parallel-fire authorization — carry-forward pointer

**Source of authority:** `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` § 7 line 142; § 8 Gate (c) RATIFIED ("D13 RATIFIED parallel-fire authorization").

**What D13 authorizes:** post season_001 Gate-2 PASS (i.e., after Step 4 A2-1 RE-FIRE produces PASS verdict + jack-ryan Gate-2 PASS at A2-2 equivalent), a **P1-P9 parallel track** fires alongside seasons 002+003 production AND the A2-5 A/B comparison phase.

**P1-P9 parallel track scope (enumerated per closure record line 142):**

| P-item | Work | Owner |
|---|---|---|
| A/B preliminary | Early A/B analysis ahead of formal A2-5 (build out comparison harness; spot-check season_001 outputs against doc 48 baseline; surface protocol-execution risks early) | gandalf |
| drax loadout sample-data wiring | Vercel-deployed loadout web app refresh consuming Wave 5 cascade outputs (kit_archive + ExportFactionCluster + ExportFactionRelationship + phase7_kit_verdict_log + phase7_cluster_aggregate_log) as updated sample data | drax |
| image pipeline auto-batch | Asset pipeline automation work (Meshy / image-pass-through pipeline tooling) | star-lord |
| H-5 hero Meshy embed | Hero-asset Meshy embedding for visual-coherence validation surface | galadriel + star-lord |
| personage coherence test | Substrate-anchored personage convergence validation (Sketch F downstream check) | gandalf + elrond |
| Drax Dispatch C/F | M-items M5 + other drax M-stream items per loadout app readiness scoping | drax |
| Sidecar G-2 | Substrate sidecar work item (elrond) | elrond |

**Discipline composition with R48.4 single-seam (Disc #48):**

D13 + R48.4 compose explicitly per closure record line 142: **"parallel work means parallel KR coordination, NOT parallel sub-agents on the constrained host."**

| Layer | Semantics |
|---|---|
| Wall-clock | Parallel tracks overlap; ~3-4d of overlap between P1-P9 items and the cascade tail (season_002 + season_003 + A2-5) |
| Sub-agent resource | Strictly single-seam — KR sequences P-items + cascade items into a single dispatch queue; each fires alone under R48.4; no parallel sub-agent fan-out on the 8 GB constrained host |
| KR coordination | KR round-robins P-items with cascade items per dispatch-queue ordering; KR-side priority: cascade integrity > P-item progress (cascade can't slip past A2-7 because P-items contend for sub-agent dispatch slot) |

**Per-track fire conditions:**
- Each P-item fires under R48.4 pre-flight (`vm_stat` > 1 GB free + EGL log clear)
- Each P-item has its own KR-authored dispatch under hive-mind decision-routing
- Each P-item completion is auto-committed per CLAUDE.md addendum 2026-05-25 (work-products of authorized cascade work)
- Pattern E pre-authorization does NOT extend to P-items (P-items are not Gate-2 reviews); P-item failures route to gandalf/jack-ryan as appropriate per critique-pair structure
- Surface to Matt at P-item BLOCK / scope-amendment-request / framing-audit catch (per existing surface conditions in this plan § 3)

**Wall-clock interaction with cascade:**

```
Step 1 (gamora KPM recalibration)              ~1-2h
  → Step 2 (rocket flag flip)                  ~0.5-1h
    → Step 3 (jack-ryan Gate-2)                ~0.5h
      → Step 4 (A2-1 RE-FIRE season_001)       ~1d
        → A2-2 (jack-ryan Gate-2 season_001)   ~half-day
          ↓
          ┌─── D13 parallel track ACTIVATES here ───┐
          │                                          │
          ↓                                          ↓
      A2-3 season_002 production + Gate-2      P1-P9 items dispatch
        → A2-4 season_003 production + Gate-2    (drax Vercel refresh among them)
          → A2-5 A/B comparison filed
            → A2-6 disciplines batched canonical-write
              → A2-7 Matt v1 tag ratification
```

**What D13 does NOT mean:**

- Does NOT permit parallel sub-agent fan-out on the constrained host (R48.4 strict)
- Does NOT release P-items from Pattern E or framing-audit disciplines
- Does NOT pre-authorize drax sample-data wiring to commit player-facing faction visibility (deferred-commitments recognition record stands — drax pulls cascade outputs as substrate data; player-facing surfacing decisions remain Matt-election territory for v1.1+)
- Does NOT collapse the cascade and the parallel track into a single closure gate — cascade closes at A2-7 Matt tag; parallel track closes per its own completion criteria (some items may carry into Cycle 14 wind-down / Cycle 15 entry)

**Why this addendum exists:**

The resolution plan § 1 Steps 1-5+ focuses on the immediate halt-recovery work. D13 parallel-fire authorization is canon per the Phase A1 closure record but was not re-stated here; explicit pointer added at Matt 2026-05-29 in-session direction so KR session-start protocol picks up D13 from this plan directly rather than relying solely on cross-reference to closure record § 7. KR reads this plan as required first read #1 per the resumption fire prompt; D13 carry-forward now lands on first-read.

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
