# DISPATCH — Gamora T1 Measurement-Context Amendment to BVV Harness (A1 Election Implementation)

**Authored:** 2026-05-28 (Mode A A1-sequence item 1; post Matt A1 election)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** gamora (simulation seam; bounded_viability_validation + t4_sim_cycling + unified_calibration_loop)
**Pattern:** Pattern A-light (harness amendment + smoke verification + brief report)
**Expected effort:** ~30 min
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 A1 election lock (`agentic_orchestration/gandalf/notes/2026-05-28-a1-election-addendum.md`) + KR Mode A charge

---

## 0. CONTEXT (read first — 3 min)

Mode A Dispatch 3 (Phase 4 RE-RUN-4 verification) returned **FAIL** 0/7 profiles, surfacing two anomalies:

- **Anomaly A — T1 measurement-context framing surface** (this dispatch addresses): BVV anchor (base context, no DDA override) T1 = 1.1442 PASS; 7-profile sweep (DDA-active) T1 at max_a = 2.425 FAIL. Same target name; different measurement context; different semantic.
- **Anomaly B — T2 profile-aware band lower-bound calibration gap** (dispatch #2 addresses sequentially after this dispatch closes)

Matt elected A1 disposition this session per `agentic_orchestration/gandalf/notes/2026-05-28-a1-election-addendum.md`:

**T1 close-criterion measured at BASE CONTEXT (DDA off).** Original semantics restored. DDA-context divergence is design-intent (in-game Primary T4 Capstone at preferred_encounter_type by design produces path-asymmetry, which T4 close-criterion measures, and which is canonically deferred to Cycle 16+ via BC axis expansion). T1 measures cross-path equity at the layer where equity belongs — raw cohort DPS BEFORE in-game Primary T4 Capstone amplification.

**Amended Path α v1 close-criterion (locked; engine readiness gate for Wave 5 production):** T1-base-context + T2-all-profiles + T3 + T5 = 4/4 required. T4 explicitly deferred to Cycle 16+ via BC axis expansion.

**Mode A 2-phase framing (Matt-ratified 2026-05-28):** Phase A1 = current 6-dispatch sequence (Path α v1 closure — engine readiness gate); Phase A2 = Wave 5 production cascade (3 LLM seasons + Gate-2 each + A/B + disciplines batch + Matt tag — Cycle 14 v1 MVP closure per D9). This dispatch is Phase A1 Dispatch 1.

**Discipline #42 framing-audit operationally active:** OP § 4.1 Q1/Q2/Q3 + measurement-context subaudit Q4/Q5/Q6 at each dispatch consumption gate (per gandalf pushback memo § 6). Operate under it; do NOT block on jack-ryan canonical ratification (sequenced at Mode A dispatch #5).

---

## 1. REQUIRED READING

LOAD-BEARING:
- `agentic_orchestration/gandalf/notes/2026-05-28-a1-election-addendum.md` — A1 election lock + canonical layer separation + dispatch sequence + naming-amendment candidate
- `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` — Discipline #42 architectural case (Instances 1+2+3 + first canonical precedent); operational rules in § 6
- `agentic_orchestration/gandalf/notes/2026-05-28-phase-4-rerun-3-adjudication.md` — parent adjudication (R1/R2/R3/R4 disposition + Read B; load-bearing context)
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT A1 ELECTION LOCKED 2026-05-28" + § "MODE A DISPATCH 1 (A1 sequence)"
- `agentic_orchestration/cycle-14-wave-5-season-001/bounded-viability-validation-baseline-2026-05-28.json` (BVV anchor format — for understanding the existing harness output shape)
- `agentic_orchestration/cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-4-amended-close-criterion-telemetry.json` (RE-RUN-4 7-profile sweep — the empirical state needing T1 amendment)

Engine source:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` (BVV harness — T1 measurement entry point)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/unified_calibration_loop.py` (Phase 4 sweep harness — RE-RUN-4 entry point; engine `28a5518` is the current state)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` (fight-context injection of DDA; understand the DDA toggle surface)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` (DDA mechanic at `:248-256` + `:404`; understand DDA application gate)

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 (math-before-code), #1.1 (resource-bounds), #1.2 (math-note code-citation), #5 (right tool), #12 (semantic-shift declaration), #18 (math hotspot consultation), #40 (scaffold-value flagging), #42 candidate (framing-audit), #47 candidate (host-RAM-aware)

---

## 2. SCOPE

### 2.1 Amendment goal

**Make T1 measurement explicit at base-context (DDA off) under the amended close-criterion.** The BVV harness + Phase 4 sweep harness should compute T1 at a measurement mode that disables the in-game Primary T4 Capstone DDA amplification — i.e., raw cross-path DPS equity BEFORE DDA application.

**T2, T3, T5 unchanged** — they continue to measure under existing semantics (T2 zero-KPM across all encounter types; T3 saturation structural; T5 floor). Only T1 measurement-context shifts.

**T4 (Secondary T4 specialization) continues to be measured-for-record only** — DROPPED as close-gate per amended criterion. T4 measurement may continue under existing DDA-active context (since it specifically measures the cohort-relative peak surface that DDA contributes to); this is pre-Cycle-16 baseline data for the BC axis expansion design call.

### 2.2 Implementation flexibility — gamora seam authority

You decide the implementation shape. Three candidate shapes (NOT exhaustive; choose what's cleanest):

| Shape | Description | Pros / Cons |
|---|---|---|
| **(I) Flag-gated T1 sub-pass** | BVV harness fires a T1-specific "base-context sub-pass" with DDA disabled at damage_resolver entry, computes T1 from that pass, returns T1. T2/T3/T4/T5 continue under DDA-active main pass | Cleanest semantic separation; ~2× cost for T1 measurement but T1 is cheap; preserves all existing measurement infrastructure |
| **(II) Explicit context-toggle parameter** | Add `t1_measurement_context: Literal["base", "dda_active"] = "base"` to BVV harness API; document semantics; default "base" per A1 election | Smaller code change; downstream consumers (Phase 4 sweep) pick context; Discipline #12 epoch break candidate but cheap |
| **(III) Disable DDA application during T1 cohort sampling** | At the cohort-DPS-sampling stage, set `combatant.t4_current_encounter_type = None` to deactivate DDA; T1 sees raw DPS; T2/T3/T4/T5 continue with DDA active at full simulation | Requires precise sampling-stage hook; risks confusing T1 sampling state from production state |

**Constraint:** must NOT break currently-passing T2/T3/T5 at BVV anchor (those PASS post-R3-hotfix). T4 measurement-for-record continues but is not gated. The amendment SHOULD make Phase 4 sweep harness consume the new T1 measurement context correctly (so RE-RUN-5 at Mode A Dispatch 3-of-A1-sequence verifies amended criterion correctly).

### 2.3 Smoke verification

After implementation:
- **BVV anchor:** verify T1 = ~1.1442 (matches Mode A Dispatch 2 attested value at base context); T2 = 0, T3 PASS, T5 = 0
- **Single-profile smoke at max_a:** verify T1 at base context ≈ BVV anchor value (1.1442 ± measurement-noise); T2/T3/T5 unchanged

Full 7-profile RE-RUN-5 sweep is Mode A Dispatch 3 (sequenced AFTER your Dispatch 2 band lower-bound recalibration); this dispatch's smoke is single-profile.

### 2.4 Math note + MIGRATION + AGENT_STATE

**Math note:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/t1-base-context-amendment-2026-05-28.md`. Cover:
- § 1: A1 election context + canonical layer separation (cite gandalf addendum)
- § 2: design choice — which implementation shape (I/II/III) selected + rationale
- § 3: code locations changed (file:line citations per Discipline #1.2)
- § 4: smoke verification results (BVV anchor + max_a single-profile)
- § 5: composition preservation verification (T2/T3/T5 unchanged at BVV anchor)
- § 6: Discipline #12 semantic-shift declaration (T1 measurement context now explicit; previous implicit context retired)
- § 7: cross-references to gandalf A1 addendum + framing-audit pushback memo + adjudication

**MIGRATION.md:** § v1.55 (or next available) — T1 measurement-context amendment; close-criterion semantic shift; downstream consumer notes (Phase 4 sweep harness, future close-criterion records).

**AGENT_STATE.md:** updated checkpoint with T1 base-context amendment completion record.

### 2.5 Tag + acceptance

- Tag: `gamora/v2.10-t1-base-context-amendment-1` (per CLAUDE.md tag conventions)
- Auto-commit per CLAUDE.md addendum (authorized cycle work-product)
- Push remains Matt-explicit-authorization

---

## 3. OUT OF SCOPE

- ❌ Anomaly B / R3-prime hotfix Component B (Mode A Dispatch 2-of-A1-sequence; sequenced AFTER this dispatch closes)
- ❌ Phase 4 RE-RUN-5 full 7-profile sweep (Mode A Dispatch 3-of-A1-sequence; sequenced AFTER #1 + #2)
- ❌ Canonical close-criterion capture (Mode A Dispatch 4; gandalf)
- ❌ Jack-ryan Gate-2 review (Mode A Dispatch 5)
- ❌ Path α v1 closure record + Wave 5 production cascade entry pre-scope (Phase A1 Dispatch 6; KR — per ITEM 2 amendment)
- ❌ Wave 5 production cascade itself (Phase A2; post Matt 3-gate surface at A1-A2 phase boundary)
- ❌ Any code change to in-game Primary T4 Capstone DDA mechanic (architecture preserved per Read B)
- ❌ Any code change to in-game Secondary T4 Capstone variants (Cycle 16+ deferred)
- ❌ T4 close-criterion measurement-mode change (T4 measured-for-record; DDA-active context fine)
- ❌ R1 / R2 / R4 work (all adjudicated)
- ❌ Pushing without KR coordination
- ❌ Deferred follow-on items (rocket naming consistency at `mechanic_alteration.py:1066`; jack-ryan Gate-2 follow-on)

---

## 4. RISKS + COMPLICATIONS

- **Discipline #42 Q4 measurement-context verification:** the amendment IS the measurement-context fix. Q4 is the EXPLICIT subject; gate passes automatically. (Self-audited at KR dispatch-authoring; not a gamora concern.)
- **Discipline #42 Q1-Q3 at YOUR dispatch consumption gate:** apply Q1/Q2/Q3 to the implementation choice (I/II/III). If you discover a framing assumption KR or gandalf got wrong (e.g., maybe T1 actually was always base-context and the DDA divergence we attributed was a different bug; maybe the BVV harness already exposes a base-context T1 sub-pass), surface BEFORE firing the amendment. Cheapest-empirical-refutation per OP § 4.1.
- **Discipline #12 epoch break:** the amendment is a Discipline #12 semantic-shift (T1 measurement context now explicit; previously implicit/context-dependent). Declare in math note + MIGRATION.md.
- **Discipline #18 methodology consultation hotspot:** the choice between shapes (I), (II), (III) is a methodology choice. Your seam authority. If load-bearing methodology question surfaces (e.g., "is disabling DDA at sampling-stage semantically equivalent to base-context full simulation?"), surface to KR for potential gandalf Pattern A-light consultation. Do NOT autonomously invoke gandalf per Mode A single-seam sequencing.
- **Discipline #47 candidate active:** R47.1-R47.5 per gandalf incident note § 6. No recursive grep without `find -size +100M`. No parallel sub-agent invocations from within your session. Pre-flight `vm_stat` before any sweep that allocates > 500 MB.
- **Discipline #1.1 pre-fire resource-bounds projection:** expected allocation small (BVV anchor + max_a single-profile smoke ~10s wall each); `vm_stat` pre-flight; abort if memory unsafe and surface to KR.
- **Phase 4 sweep harness coordination:** the Phase 4 sweep harness (RE-RUN-4 telemetry came from this) must consume the new T1 measurement context correctly at RE-RUN-5 fire. Verify the sweep harness picks up the amendment OR document handoff requirements for Mode A Dispatch 3 (gamora session continuity).
- **Smoke-test resource-scaling (Discipline #2.1):** smoke gates must include resource scaling. BVV anchor smoke + max_a single-profile smoke is cheap (~10-15s each).

---

## 5. URGENCY + SEQUENCING

**Fires FIRST in Mode A A1-sequence** — sets the measurement framework for #2 (Anomaly B band lower-bound recalibration) and #3 (Phase 4 RE-RUN-5 verification). Sequenced FIRST to avoid interaction between T1 amendment and band-calibration changes.

**Single-seam sequencing per R47.4 preserved.** Your session is the only sub-agent active; no parallel work fires.

**KR will fire Mode A Dispatch 2 (R3-prime hotfix Component B) on receipt of your completion record.**

---

## 6. SURFACING-TO-KR PROTOCOL

Surface back to KR via completion record on this dispatch when:
- ✅ Amendment implemented + smoke verified — normal close (KR fires Dispatch 2)
- ⚠️ Implementation shape (I/II/III) requires methodology consultation exceeding seam authority — KR routes Pattern A-light gandalf consultation
- 🚨 Framing-audit Q1/Q2/Q3 surfaces an assumption KR or gandalf got wrong — surface IMMEDIATELY (per A1 charge surface-to-Matt protocol "framing-audit findings catching pre-imposed assumption failure")
- 🚨 Existing BVV harness already supports base-context T1 (no amendment needed) — surface for KR to fast-forward to Dispatch 2
- 🚨 BVV harness amendment surface requires touching cross-seam code (rocket / star-lord territory) — surface to KR for cross-seam coordination

Per Matt 2026-05-23 hive-mind decision-routing: seam-owner decides in-scope work; Matt is LAST-resort escalation. You have full authority within your seam to choose between shapes (I) / (II) / (III) subject to the constraint envelope at § 2.2.

---

**KR signature:** authored per Matt A1 election lock + KR Mode A hive-mind charge + Disc #47 R47.4 single-seam sequencing + Disc #42 Q1-Q6 framing-audit at dispatch-authoring gate (self-audited PASS). This is the cleanest first step in the A1 sequence — make T1 measurement explicit at base-context per restored semantics; preserves layer separation that Reincarnated's design depends on (per gandalf addendum § 7 design-lead conviction).

---

## Completion record

(gamora appends here)
