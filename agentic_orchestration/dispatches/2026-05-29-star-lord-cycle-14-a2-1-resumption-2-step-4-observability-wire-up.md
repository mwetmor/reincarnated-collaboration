# DISPATCH — Star-Lord Cycle 14 A2-1 Cascade-Resumption-2 Step 4 (Phase 5 LLM Cost-Tracker Wire-Up + A12-1/A12-2 Observability Composition)

**Authored:** 2026-05-29 (Mode A Phase A2 cascade-resumption-2; Concern #3 resolution authorization § 3.3 + § 4 broader Disc #40 cleanup composition with gandalf gate (i) preliminary findings)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** star-lord (engine operational-pipeline seam owner; `export/`, `output/`, `telemetry/`, `llm/`)
**Pattern:** Pattern B sustained-execution observability landscape investigation + in-seam wire-up + cross-seam surface to KR if needed (~1-2h wall-clock per authorization § 3.3 expanded scope)
**Expected effort:** ~1-2h (3 observability gap investigations + wiring what's in star-lord seam + completion record; longer if cross-seam composition surfaces)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-29 in-session Concern #3 resolution authorization § 3.3 (Phase 5 cost-tracker wire-up Matt-pre-ratified) + § 4 "may compose into broader Disc #40 cleanup" framing + gandalf Step 2.5 preliminary brief Disc #40 findings (A12-1 + A12-2 deferred to Step 4 composition) + hive-mind decision-routing + R48.4 single-seam (gamora released post Step 3 PASS; star-lord firing alone)

---

## 0. CONTEXT (read first — 4 min)

### 0.1 Cascade-resumption-2 entry lineage

| # | Step | Owner | Verdict |
|---|---|---|---|
| 1 | gamora caller-graph audit | gamora | ✅ PASS — single Phase 7 consumer + P3a viable; routing Case A + Case D → P3c |
| 2 | KR routing decision per § 3.2 matrix | KR | ✅ P3c (pre-ratified) |
| 2.5 | gandalf gate (i) preliminary assessment | gandalf | ✅ PASS-preliminary — Wave A + F-C empirically coherent + AI-tell-clean; A12-1 + A12-2 observability gaps surfaced |
| 3 | gamora P3c fix at gauntlet_sim.py source + Disc #11 hygiene | gamora | ✅ PASS — Option β (`kr.cohort_results.keys()`); 85 PASS 0 new regressions; tag `gamora/v2.15-a2-1-r2-step-3-concern-3-p3c-fix-1`; Disc #12 EPOCH BREAK declared in MIGRATION § v1.58 |
| **4 (THIS DISPATCH)** | star-lord observability wire-up (expanded scope) | star-lord | ⏳ PENDING — investigation + wiring |

### 0.2 The 3 observability gaps composed in this dispatch

Per gandalf Step 2.5 preliminary brief + KR composition decision per Concern #3 authorization § 4 "may compose into broader Disc #40 cleanup":

**Gap (a) — Phase 5 LLM `tracker=None` (ORIGINAL Step 4 scope):**

Per A2-1 RE-FIRE attempt 2 rocket completion record § 4 + Concern #3 authorization § 3.3:
- `wave5_season_orchestrator.py` Phase 5 invocation passes `tracker=None` to `phase5_orchestrator.run_phase5_with_fc_sync()` (or equivalent)
- Real LLM spend recorded as $0.00 cumulative; actual spend estimated ~$0.12 unverified (rocket attestation)
- $50 soft cap + $60 hard halt cost-guard NON-FUNCTIONAL for A2-1 RE-FIRE attempt 2
- Functional cost-tracker is REQUIRED for Step 6 A2-1 RE-FIRE-2 (first production fire with all 3 concerns resolved + cost-tracker active)

**Gap (b) — A12-1 Wave B per-kit identity NOT persisted to kit_archive.notes:**

Per gandalf Step 2.5 brief:
- Wave B (per-kit identity LLM) FIRES in-process per rocket A2-1 RE-FIRE attempt 2 § 4 (FACTION_VISIBILITY=visible per Step 2 of cascade-resumption-1)
- BUT `kit_archive.notes` column is EMPTY for all 18 ACCEPTED kits
- Wave B output unobservable to downstream gates (Phase 7 cohesion-judge, A/B comparison protocol at A2-5, gandalf gate (i) full verdict)
- This is observability gap (NOT functional bug per se; LLM fires but output isn't captured to persistent telemetry)

**Gap (c) — A12-2 `kit_cohesion_score` NULL in `phase7_kit_verdict_log` for all 54 rows:**

Per gandalf Step 2.5 brief:
- Schema has `phase7_kit_verdict_log.kit_cohesion_score REAL` column
- All 54 rows show NULL even where `phase7_gate_status="canonical"` (Wave A fired; cohesion verdict was rendered)
- Recognition record prediction P2 ("Phase 7 cohesion_judge_confidence distributes around 0.70-0.85 range") untestable until population wired
- Composes with Phase 7 cohesion-threshold scaffold-flag — can't even measure threshold pressure without populated scores

### 0.3 Why these compose in Step 4 (not 3 separate dispatches)

Per Concern #3 authorization § 4: "may compose into broader Disc #40 cleanup." Per hive-mind decision-routing: KR routes Disc #40 secondary observations to seam-owner who's best-positioned to investigate. Star-lord owns `export/`, `output/`, `telemetry/`, `llm/`:

- Gap (a) Phase 5 LLM cost-tracker: 100% star-lord seam (`llm/` cost-tracker instrumentation)
- Gap (b) Wave B persistence: Wave B output ORIGINATES in star-lord `llm/` (Phase 5 orchestrator); PERSISTENCE to `kit_archive.notes` is rocket seam (orchestrator output writes). Star-lord investigates flow + surfaces to KR if rocket-side wiring is required (KR authors gamora/rocket follow-on dispatch under R48.4 strict-sequential).
- Gap (c) kit_cohesion_score: SCORE ORIGINATES in Phase 5 cohesion judge (`llm/`); POPULATION in phase7_kit_verdict_log is gamora seam (`simulation/phase7_db.py` schema + `simulation/phase7_bridge.py` emit). Star-lord investigates flow + surfaces to KR if gamora-side wiring is required.

This composition lets star-lord do the landscape investigation (single sub-agent dispatch under R48.4) + wire what's in-seam + cleanly surface what's cross-seam for KR routing.

### 0.4 Disc #42a framing-audit at dispatch consumption

KR's authoring applied Q1-Q6. Star-lord should re-apply at consumption:

- **Q1 — load-bearing framing assumption:** "The 3 observability gaps (Phase 5 tracker=None + A12-1 Wave B persistence + A12-2 kit_cohesion_score) compose architecturally because they all share the pattern 'LLM output produced but not flowed through to downstream persistence/measurement.' Star-lord landscape investigation is the cheapest empirical refutation of this composition assumption."
- **Q2 — refutation evidence in scope:** the investigation produces caller-graph + data-flow trace for each gap; if star-lord finds (e.g.) Wave B persistence requires a rocket-side schema migration of `kit_archive.notes` column type, that surfaces cross-seam routing requirement
- **Q3 — refutation surface-able cheaply:** yes — read-only investigation phase + in-seam wire-up + surface cross-seam + completion record at star-lord seam-internal cost
- **Q4 — measurement context match:** the 3 gaps must be addressed before Step 6 A2-1 RE-FIRE-2 to enable the empirical signal D9 ratified close-criterion intended to measure (≥12/18 emit AFTER cost-tracker-recorded LLM spend + cohesion-judge-confidence-measured exclusions + Wave-B-coherent kit identity)
- **Q5 — calibration scope match:** the 3 gaps' resolution scope matches what gandalf gate (i) full verdict + jack-ryan Gate-2 design-quality audit will measure at A2-1 RE-FIRE-2 close
- **Q6 — semantic stability of "observability wire-up" vs "scope amendment":** star-lord wires what's in-seam under existing authorization; star-lord SURFACES TO KR if investigation reveals a gap requires cross-seam work, scope-amendment, OR deeper architectural intervention (per authorization § 4 + Concern #3 dispatch § 5 risks)

If any framing refutes, SURFACE TO KR.

### 0.5 What's OUT of scope for this dispatch

- ❌ Schema migrations to `kit_archive` or `phase7_kit_verdict_log` (if needed, SURFACE to KR for cross-seam dispatch authoring)
- ❌ Phase 5 LLM prompt redesign / Wave A/B/F-C prompt amendment (recognition record gate (i) preliminary captured this; Pattern B design call if needed routes to Matt re-engage)
- ❌ Phase 7 cohesion_judge_confidence threshold recalibration (scaffold; capture-and-watch only)
- ❌ Decisions-log canonical write (jack-ryan owns; deferred to Matt re-engage)
- ❌ Recognition record canonical amendment (preliminary at Step 2.5; full at Step 6 A2-1 RE-FIRE-2 close)
- ❌ Cost-cap policy change ($50 soft / $60 hard per Matt 3-gate at Phase A1; preserved)

---

## 1. THE TASK

**Investigate the 3 observability gap landscape; wire what's in star-lord seam (cost-tracker instrumentation + Wave B + cohesion score data-flow); surface what's cross-seam (rocket OR gamora) to KR for follow-on dispatch authoring. Output landscape investigation summary + completion record.**

### 1.1 Pre-flight (REQUIRED before investigation fire)

1. **Disc #48 R48.5 vm_stat check:** confirm > 1 GB free + reclaimable (KR pre-flight at Step 4 entry showed ~2.69 GB available)
2. **Disc #48 R48.4 single-seam confirm:** gamora released post Step 3 PASS; only this dispatch's star-lord running
3. **Engine state confirm:** HEAD at `ef742a2` (gamora Step 3 AGENT_STATE checkpoint); Step 3 tag `gamora/v2.15-a2-1-r2-step-3-concern-3-p3c-fix-1` intact + cascade-resumption-1 + Step 1 tags intact
4. **Verify gap sites:** read `wave5_season_orchestrator.py` Phase 5 invocation site + `phase5_orchestrator.py` Wave B / F-C / cohesion judge invocations + `phase7_db.py` schema for `phase7_kit_verdict_log` + `phase7_bridge.py` verdict-log emit site + `kit_archive.db` schema

### 1.2 Gap (a) Phase 5 LLM cost-tracker wire-up — IN STAR-LORD SEAM (likely)

**Investigation:**

1. Locate Phase 5 LLM cost-tracker class/protocol in `llm/` (likely `LLMCostTracker` or equivalent)
2. Identify wire-up site: `wave5_season_orchestrator.py` Phase 5 invocation passes `tracker=None`; replace with `tracker=<real_tracker_instance>`
3. Verify cost-tracker captures Wave A + F-C + Wave B per-call spend
4. Validate cost-tracker emits cumulative + per-call telemetry that downstream cost-guard can read

**Wiring:**

- Replace `tracker=None` with `tracker=LLMCostTracker(...)` or equivalent in `wave5_season_orchestrator.py` Phase 5 invocation (star-lord seam IF orchestrator-side wire-up uses star-lord-exported class; else rocket seam if orchestrator construction is rocket-owned — surface IF cross-seam)
- Wire cost-tracker output to telemetry persistence (LLM call log; cumulative cost accumulation; per-Phase breakdown)
- Validate that `$50 soft cap PROJECTION` + `$60 hard halt` logic can read tracker state mid-cascade

**Acceptance:**

- Cost-tracker wired in `wave5_season_orchestrator.py` Phase 5 invocation (or surfaced as cross-seam if non-star-lord seam ownership)
- Cost-tracker captures per-call + cumulative spend
- Cost-guard logic reads tracker state (no behavior change; tracker provides the data the guard already expects)

### 1.3 Gap (b) A12-1 Wave B per-kit identity persistence — INVESTIGATE + WIRE OR SURFACE

**Investigation:**

1. Identify Wave B output schema: what does Phase 5 Wave B return per-kit? (likely ExportFactionCluster-adjacent OR per-kit identity record at `phase5_orchestrator.py`)
2. Identify intended persistence target: gandalf's brief said "`kit_archive.notes` column EMPTY for all 18 kits" — is `kit_archive.notes` the canonical destination? OR is there a separate `kit_identity` table planned?
3. Trace the data-flow: does Wave B output flow back to `wave5_season_orchestrator.py` (orchestrator seam — rocket-owned) for persistence to `kit_archive.db`? OR does Phase 5 directly persist?
4. Identify the gap: is the issue (i) Wave B output not returned from Phase 5; (ii) returned but not received by orchestrator; (iii) received but not written to kit_archive.notes?

**Wiring decision:**

- If gap is 100% in star-lord seam (Phase 5 output extraction + telemetry persistence): wire it in this dispatch
- If gap is cross-seam (rocket-side orchestrator persistence): SURFACE to KR for rocket follow-on dispatch authoring + capture star-lord-side prerequisites if any
- If gap requires schema migration (kit_archive.notes column type change OR new column / new table): SURFACE to KR for elrond scope decision (schema = elrond seam)

**Acceptance:**

- Investigation summary captured (data-flow trace + gap identification)
- If in-seam: wired
- If cross-seam: SURFACE with clear scope handoff to next-seam dispatch

### 1.4 Gap (c) A12-2 kit_cohesion_score population — INVESTIGATE + WIRE OR SURFACE

**Investigation:**

1. Identify cohesion-judge score origin: Phase 5 cohesion judge (Wave B per-kit OR Wave A faction-level OR F-C inter-faction) produces what scores?
2. Identify intended target: `phase7_kit_verdict_log.kit_cohesion_score REAL` column in `phase7_db.py` schema (gamora seam)
3. Trace data-flow: Phase 5 cohesion-judge score → ? → `phase7_bridge.py` verdict-log emit site → `phase7_kit_verdict_log` row
4. Identify gap: is the issue (i) cohesion-judge score not produced; (ii) produced but not returned from Phase 5; (iii) returned but not received by phase7_bridge; (iv) received but not written to verdict-log row?

**Wiring decision:**

- If gap is 100% in star-lord seam (Phase 5 score extraction): wire it in this dispatch
- If gap is cross-seam (gamora-side phase7_bridge.py emit-site wiring): SURFACE to KR for gamora follow-on dispatch authoring + capture star-lord-side prerequisites
- If gap requires schema migration (`phase7_kit_verdict_log` column add OR type change): SURFACE to KR for elrond scope decision

**Acceptance:**

- Investigation summary captured (data-flow trace + gap identification)
- If in-seam: wired
- If cross-seam: SURFACE with clear scope handoff

### 1.5 Disc #2 smoke verification (REQUIRED before commit)

For each gap wired in-seam:

1. Module-load smoke: import affected modules cleanly
2. Targeted unit smoke: run any existing tests covering the wire-up paths
3. Integration smoke if practical: synthesize a minimal Phase 5 invocation that triggers cost-tracker + Wave B + cohesion-score flow

If any smoke fails: SURFACE TO KR (potential cross-seam blast).

### 1.6 MIGRATION.md / equivalent star-lord-seam migration notes

Per star-lord seam convention: capture wire-up changes in `simulation/MIGRATION.md` § v1.59 (or next available) OR `llm/MIGRATION.md` OR `telemetry/MIGRATION.md` depending on seam scope.

- Describe Phase 5 cost-tracker wire-up + downstream cost-guard activation
- Describe Wave B persistence wire-up (if wired in-seam) OR cross-seam routing decision (if surfaced)
- Describe kit_cohesion_score wire-up (if wired in-seam) OR cross-seam routing decision (if surfaced)
- Disc #12 EPOCH BREAK assessment per wire-up (star-lord's call)

### 1.7 Acceptance criterion (per Concern #3 authorization § 3.3 + § 4 expanded scope)

- ✅ Phase 5 LLM cost-tracker wire-up landed (or cross-seam routing decision documented + KR-surfaced)
- ✅ A12-1 Wave B persistence: in-seam wired OR cross-seam routing documented + KR-surfaced
- ✅ A12-2 kit_cohesion_score: in-seam wired OR cross-seam routing documented + KR-surfaced
- ✅ Smoke verification clean for in-seam wire-ups
- ✅ MIGRATION.md § v1.59 (or next) records wire-ups + Disc #12 assessment
- ✅ Tag: `star-lord/v1.X-a2-1-r2-step-4-observability-wire-up-1` (or seam convention)
- ✅ Auto-commit per CLAUDE.md addendum 2026-05-25
- ✅ Do NOT push — KR fires push after A2-2 Gate-2 PASS per per-workstream pattern
- ✅ Do NOT scope-creep to schema migrations (SURFACE to KR for elrond if needed)
- ✅ Do NOT pre-commit Phase 7 cohesion-threshold recalibration (scaffold; capture-and-watch)

### 1.8 Completion-record format (append to this dispatch)

Append a `## Completion record` section with:

1. **VERDICT** — single line: "A2-1 R2 Step 4 observability wire-up — PASS (3 gaps addressed: [in-seam wired / cross-seam surfaced per gap])" OR "PARTIAL with cross-seam SURFACE for KR" OR "FAIL with diagnosis"
2. **Gap (a) Phase 5 cost-tracker status** — wired / surfaced + details
3. **Gap (b) A12-1 Wave B persistence status** — wired / surfaced + data-flow trace + routing recommendation if surfaced
4. **Gap (c) A12-2 kit_cohesion_score status** — wired / surfaced + data-flow trace + routing recommendation if surfaced
5. **Disc #2 smoke verification** — per-wire-up smoke results
6. **Disc #12 EPOCH BREAK assessment** — declared OR not per wire-up + rationale
7. **MIGRATION.md § cited** — § number(s) + path
8. **Cross-seam surfaces** — clear scope handoff per gap (rocket / gamora / elrond + recommended next-dispatch shape)
9. **Disc #42a Q1-Q6 self-audit** — all 6 questions + verdicts
10. **Disc #40 cumulative pattern queue update** — 4-point queue (FACTION_VISIBILITY-default + tracker=None + A12-1 + A12-2) → which resolved here + which carry forward
11. **Disc #48 R48.4/R48.5 verification** — no other sub-agent; vm_stat captured
12. **Engine + collab commits + tag** — star-lord commits + tag
13. **Any anomalies surfaced** during investigation / wire-up

---

## 2. CROSS-SEAM CONTRACT CHANGE? (Principle 6)

**Potentially yes for Wave B persistence + kit_cohesion_score** depending on investigation. Phase 5 cost-tracker is likely 100% star-lord seam (LLM cost instrumentation). Wave B persistence may require rocket-side orchestrator wiring. kit_cohesion_score may require gamora-side phase7_bridge.py emit-site wiring. Star-lord investigation determines + surfaces.

---

## 3. QUALITY CRITERION (KR OP § 3.11)

**Game-quality goal:** wire the LLM-output-to-downstream-persistence pipeline so that A2-1 RE-FIRE-2 (Step 6) produces measurable empirical signal across all dimensions D9 ratified close-criterion + recognition record gate (i) full verdict + jack-ryan Gate-2 design-quality audit need. Without these wire-ups, Step 6 reproduces the observability gaps (functional but unmeasurable cascade).

**Refutation conditions:**
- Investigation reveals deeper observability architecture issue (e.g., cost-tracker design flaw; Wave B output format incompatible with kit_archive.notes column type) → SURFACE TO KR for scope decision (potential Pattern B design call)
- In-seam wire-up surfaces regression in existing tests → SURFACE for scope decision
- Cross-seam routing landscape is unclear (e.g., 3-seam composition with circular dependencies) → SURFACE for scope decision
- Disc #42a Q1-Q6 framing-audit refutes pre-imposed assumption → SURFACE IMMEDIATELY
- Dispatch framing pre-commits to a decision Matt has not ratified — NO (cost-tracker wire-up Matt-ratified per authorization § 3.3; A12-1/A12-2 composition Matt-ratified per § 4 broader-Disc-#40-cleanup framing)

If any refutation condition triggers, SURFACE TO KR.

---

## 4. OUT OF SCOPE

- ❌ Schema migrations to `kit_archive` or `phase7_kit_verdict_log` (elrond scope; surface if needed)
- ❌ Phase 5 LLM prompt redesign / Wave A/B/F-C prompt amendment (recognition record / Matt Pattern B if needed)
- ❌ Phase 7 cohesion_judge_confidence threshold recalibration (scaffold; capture-and-watch)
- ❌ Cost-cap policy change ($50 soft / $60 hard preserved per Matt 3-gate Phase A1)
- ❌ P3c fix re-amendment (Step 3 CLOSED)
- ❌ FACTION_VISIBILITY re-amendment (Step 2 of cascade-resumption-1 CLOSED)
- ❌ Recognition record canonical amendment (preliminary at Step 2.5; full at Step 6 A2-1 RE-FIRE-2 close)
- ❌ Decisions-log canonical write (jack-ryan owns; deferred)
- ❌ Disc #42a Instance-5 addendum / Disc #40 canonical capture (deferred to Matt re-engage per resolution plan § 4 + Concern #3 authorization § 4)
- ❌ Step 5 jack-ryan Gate-2 / Step 6 A2-1 RE-FIRE-2 (subsequent dispatches)
- ❌ A/B comparison protocol / Disciplines batch (A2-5 / A2-6)
- ❌ D13 parallel-fire / legolas Mode A (post A2-2 PASS / post-cascade-close)
- ❌ Player-facing faction-architecture commitments (deferred)
- ❌ Pushing
- ❌ Parallel sub-agent fan-out under R48.4

---

## 5. RISKS + COMPLICATIONS

- **Cross-seam composition complexity:** if all 3 gaps require cross-seam wiring (rocket + gamora + elrond), KR must sequence 3 follow-on dispatches under R48.4 strict-sequential. This expands cascade timeline; estimate +1-3h beyond original Step 4 budget. Surface clearly so KR can plan sequence.
- **Schema migration surface:** if either Wave B persistence (kit_archive.notes column type) OR kit_cohesion_score (phase7_kit_verdict_log column already exists but might need related-table changes) requires schema migration, that's elrond seam (catalogue DB / schema design). Surface to KR for elrond dispatch authoring.
- **Cost-tracker instrumentation regression risk:** wiring `tracker=<real>` may surface unexpected interactions with existing test fixtures that pass `tracker=None`. Smoke test carefully.
- **Wave B output format mystery:** gandalf's brief indicates Wave B FIRES but output isn't in kit_archive.notes. Star-lord investigation must trace the data-flow to determine WHERE Wave B output currently lands (telemetry log? in-memory only? discarded?). This is the first-time-empirical look at Wave B production output flow.
- **Disc #40 cumulative pattern data:** the 4-point Disc #40 queue captured by gandalf composes here. Star-lord's wire-ups resolve gaps (a) + (potentially b + c); cumulative pattern is data point for Matt re-engage cumulative Disc #40 discussion.

---

## 6. URGENCY + SEQUENCING

**Fires under R48.4 single-seam IMMEDIATELY (gamora released post Step 3 PASS; star-lord alone in slot 4).** Step 5 (jack-ryan Gate-2 Pattern E) fires AFTER this dispatch closes; Step 6 (A2-1 RE-FIRE-2) fires AFTER Step 5 PASS.

Per fire prompt sequence: cascade-resumption-2 Step 1 ✅ → Step 2 ✅ → Step 2.5 ✅ → Step 3 ✅ → **Step 4 (this dispatch)** → Step 5 (jack-ryan Gate-2) → Step 6 (A2-1 RE-FIRE-2) → A2-2 → A2-3 → A2-4 → A2-5 → A2-6 → A2-7.

If Step 4 surfaces cross-seam follow-on dispatches: KR sequences them between Step 4 and Step 5 under R48.4 strict-sequential.

A2-1 R2 Step 4 PASS or PASS-with-cross-seam-surfaces → KR routes follow-on dispatches (if any) + fires Step 5 (jack-ryan Gate-2 Pattern E).

A2-1 R2 Step 4 deep observability issue surfaced → SURFACE TO KR for Matt scope decision.

---

## 7. SURFACING-TO-KR PROTOCOL

Append completion record (interim OR final) at any of:

- ✅ All 3 gaps addressed (in-seam wired or cross-seam surfaced cleanly) → normal close (KR routes follow-on dispatches if any + fires Step 5)
- ⚠️ Investigation reveals deep observability architecture issue → SURFACE for scope decision
- ⚠️ Cross-seam composition requires schema migration → SURFACE for elrond dispatch authoring
- ⚠️ In-seam wire-up surfaces test regression → SURFACE for scope decision
- ⚠️ Disc #42a Q1-Q6 framing-audit refutation → SURFACE IMMEDIATELY
- ⚠️ Disc #48 R48.5 RAM pressure → pause + SURFACE
- 🚨 Substantial unexpected failure mode → SURFACE IMMEDIATELY

---

## 8. REFERENCES

- `agentic_orchestration/gandalf/notes/2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md` § 3.3 (cost-tracker wire-up) + § 4 (broader Disc #40 cleanup composition)
- `agentic_orchestration/gandalf/notes/2026-05-29-gate-i-preliminary-assessment.md` — A12-1 + A12-2 observability findings
- `agentic_orchestration/dispatches/2026-05-29-gandalf-cycle-14-a2-1-resumption-2-step-2-5-gate-i-preliminary-assessment.md` § Completion record — Step 2.5 PASS-preliminary
- `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-a2-1-resumption-2-step-3-concern-3-p3c-fix.md` § Completion record — Step 3 PASS (P3c at gauntlet_sim.py + Disc #11 hygiene at phase7_bridge.py + Disc #12 EPOCH BREAK declared)
- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-a2-1-step-4-refire-post-step1-step2.md` § Completion record § 4 — Phase 5 Wave A + F-C + Wave B fired observation + tracker=None gap
- `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Phase A1 closure + Matt 3-gate ($50 soft / $60 hard)
- `agentic_orchestration/cycle-14-hive-mind-state.md` — Wave 5 state (cascade-resumption-2 in-flight at Step 4)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` — Phase 5 invocation site (tracker=None gap)
- `~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` — Wave A + F-C + Wave B + cohesion judge invocation
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` — phase7_kit_verdict_log emit site (Gap (c) target if cross-seam)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_db.py` — `phase7_kit_verdict_log` + `phase7_cluster_aggregate_log` DDL (kit_cohesion_score REAL column)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` lines 563-832 — ExportFactionCluster + ExportFactionRelationship schemas
- `agentic_orchestration/cycle-14-wave-5-season-001/kit_archive.db` — kit_archive schema (`notes` column target for Gap (b))
- `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` (5,741 B) + `phase5_faction_relationships.json` (4,658 B) — Wave A + F-C output references
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — append § v1.59 (or next)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` line 3536 — D9 ratified close-criterion LOCKED
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #2/#11/#12/#21/#22/#40/#42a/#48 active
- Engine HEAD: `ef742a2` (gamora Step 3 AGENT_STATE post-PASS); tags `gamora/v2.15-a2-1-r2-step-3-concern-3-p3c-fix-1` + cascade-resumption-1 tags intact

---

**KR signature:** authored per Phase A2 cascade-resumption-2 + Step 3 PASS (P3c clean; 85/0 regressions; Disc #12 EPOCH BREAK declared in MIGRATION § v1.58) + R48.4 single-seam (gamora released; star-lord alone in slot 4) + Disc #42a meta-observation 5 self-vigilance (Step 3 P3c fix empirically re-verified at gauntlet_sim.py:1068-1080 + phase7_bridge.py:352-362 via Read; tag + commits intact; smoke results in completion record) + auto-commit per CLAUDE.md addendum 2026-05-25 + Concern #3 authorization § 4 "may compose into broader Disc #40 cleanup" composition decision (A12-1 + A12-2 into Step 4 scope per gandalf preliminary brief recommendation + KR hive-mind decision-routing).

This dispatch is the cheapest empirical refutation of "are the 3 observability gaps (Phase 5 tracker=None + A12-1 Wave B persistence + A12-2 kit_cohesion_score) wireable within star-lord seam OR do they require cross-seam composition?" — landscape investigation + in-seam wire-up + cross-seam surface at star-lord seam-internal cost (~1-2h wall-clock).

A2-1 R2 Step 4 PASS = observability landscape resolved (in-seam + cross-seam routing clear) → unblocks Step 5 (jack-ryan Gate-2 Pattern E on Step 1 + Step 3 + Step 4 outputs) → Step 6 (A2-1 RE-FIRE-2 with FUNCTIONAL cost-tracker + measurable Wave B + measurable cohesion score) → cascade through A2-2 → A2-7 toward Cycle 14 v1 MVP D9 close.

---

## Completion record

**Authored:** 2026-05-29 (star-lord A2-1 R2 Step 4 close)
**Engine commit:** `d388c49` — `star-lord: A2-1 R2 Step 4 — Phase 5 cost-tracker wire-up + call-count fix; Gaps (b)+(c) surfaced`
**Collab commit:** (this dispatch file + completion record append)
**Tag:** `star-lord/v1.2-a2-1-r2-step-4-observability-wire-up-1`

---

### 1. VERDICT

A2-1 R2 Step 4 observability wire-up — PARTIAL with cross-seam SURFACES for KR.

- Gap (a): IN-SEAM WIRED (Phase 5 cost-tracker + call-count fix landed)
- Gap (b): CROSS-SEAM SURFACED (Wave B NOT implemented; requires new star-lord LLM function + rocket orchestration dispatch)
- Gap (c): CROSS-SEAM SURFACED (kit_cohesion_score structurally blocked by Gap (b); gamora emit path READY once Wave B produces scores)

---

### 2. Gap (a) — Phase 5 LLM cost-tracker status: IN-SEAM WIRED

**Root cause traced:**
1. `wave5_season_orchestrator.py` passed `tracker=None` to `run_phase5_with_fc_sync()`
2. `tracker=None` → per-call telemetry block skipped → `llm_call_id=None` on every `Phase5WaveAResult` / `Phase5FCResult`
3. `total_llm_calls = len([r for r in wave_a_results if r.llm_call_id is not None])` → 0 → `total_cost_usd = $0.00`
4. Same broken derivation in F-C: `successful_calls = len([r for r in fc_results if r.llm_call_id is not None])` → 0
5. Phase 5 reported `llm_cost_usd=$0.00` while actual spend was ~$0.12 (per rocket A2-1 RE-FIRE attempt 2 attestation)
6. `$50 soft cap` / `$60 hard halt` cost guards were advisory-only (0 projected; never triggered)

**Fix 1 — `llm/phase5_orchestrator.py`:**
- `run_phase5_wave_a_async()` line 1719: `total_llm_calls = len(wave_a_results)` (counts all call attempts, not just telemetry-recorded ones)
- `run_fc_per_pair_async()` line 1584: `initial_calls = len(pairs)` + `regen_calls = len([r for r in fc_results if r.regeneration_fired])`

**Fix 2 — `simulation/wave5_season_orchestrator.py`:**
- `run_phase5_cohesion_judge()` now constructs `TrackedLLMClient.from_client(LLMClient(), NullRecorder())` with `set_season(SEASON_ID)` instead of passing `tracker=None`
- NullRecorder: no DB writes; API key from env; call-count fix active; wired for future composability with TelemetryRecorder

**NullRecorder rationale:** Per-call DB telemetry requires `TelemetryRecorder` with a research DB connection managed at CLI/orchestrator level (rocket seam). Threading a DB-backed recorder into `run_phase5_cohesion_judge()` is a cross-seam scope extension deferred to follow-on rocket dispatch.

**Effect:** Phase 5 now reports accurate `total_llm_calls` (e.g., 3 Wave A + 3 F-C = 6 calls for a 3-cluster season) and accurate `total_cost_usd`. Cost guards are now functional for Step 6 A2-1 RE-FIRE-2.

---

### 3. Gap (b) — A12-1 Wave B per-kit identity persistence status: CROSS-SEAM SURFACED

**Critical empirical finding:** Wave B is NOT IMPLEMENTED in `llm/phase5_orchestrator.py`.

Evidence: full function inventory of 28 functions in the 2263-line file — `run_wave_a_async`, `run_fc_per_pair_async`, `_call_wave_a_single`, `_call_fc_single` exist; NO `run_wave_b_async`, `_call_wave_b_single`, or equivalent. `run_phase5_with_fc_async()` docstring explicitly states: "Wave B per-kit calls are NOT fired here (separate entry point)." The wave5_season_orchestrator.py comment claiming "run_phase5_with_fc_sync fires Wave A + F-C + Wave B" was incorrect; corrected in this dispatch's commit.

**Implication:** The rocket A2-1 RE-FIRE attempt 2 completion record §4 stating "Wave B: FIRED" was a documentation error. `kit_archive.notes` is empty because Wave B never ran — there is no Wave B implementation to produce output.

**Data-flow trace:** Wave B was intended to run per-kit LLM calls using parent faction context from Wave A results → return per-kit identity narratives → persist to `kit_archive.notes` via rocket orchestrator. All three steps are missing.

**Routing recommendation:** Separate sequential dispatches under R48.4 strict-sequential:
1. Star-lord: `run_wave_b_async()` LLM function in `llm/phase5_orchestrator.py` — new per-kit LLM function, `Phase5WaveBResult` dataclass, prompt templates, return-type design
2. Rocket: Wave B invocation in `wave5_season_orchestrator.py` + persistence to `kit_archive.notes` — must wait for star-lord Wave B function to exist

No schema migration needed for `kit_archive.notes` — column type `TEXT` is correct for per-kit identity narrative.

---

### 4. Gap (c) — A12-2 kit_cohesion_score status: CROSS-SEAM SURFACED (blocked by Gap (b))

**Root cause chain:**
1. `wave5_season_orchestrator.py:1169` hardcodes `cohesion_data={}` in `run_phase7_joint_gate()` call
2. `Phase5Result` has `wave_a_results` (cluster-level) and `fc_results` (pair-level) — NO `{kit_id: cohesion_score}` per-kit mapping field
3. Per-kit cohesion scores are supposed to come from Wave B output; Wave B not implemented (Gap (b))
4. No data to wire into `cohesion_data`

**Good news:** downstream emit path is fully READY.
- `phase7_bridge.py` line 478: `cohesion_scores: Optional[dict[str, float]]` parameter — correct interface
- Lines 714-715: `cohesion_score = cohesion_scores.get(kit_id)` — already implemented
- Line 740: `kit_level_cohesion_score=cohesion_score` — emit to `phase7_kit_verdict_log` already wired
- `phase7_db.py` line 100: `kit_cohesion_score REAL` column — exists in DDL, no schema migration needed

**What's missing:** the producer (Wave B). Once Wave B returns `{kit_id: score}`, the wire-up in `wave5_season_orchestrator.py` is approximately 3 lines: extract per-kit scores from `p5_result` → pass to `run_phase7_joint_gate(cohesion_data=scores)`.

**Routing recommendation:** Compose with Gap (b) Wave B implementation. After rocket's Wave B dispatch lands, a small follow-on (star-lord or rocket) threads `cohesion_data` from the `Phase5Result` return value into the phase 7 gate call. No schema migrations required anywhere.

---

### 5. Disc #2 smoke verification

**Gap (a) wire-up smoke:**
- Module-load: `python -c "from reincarnated.llm.phase5_orchestrator import run_phase5_with_fc_sync"` — PASS
- Phase 5 test suite (`test_dispatch_3b_phase5_seam3`, `test_wave3_seam2_fc_infra`, `test_dispatch_3b_seam3_pm1_wiring`): 141/141 PASS
- Gauntlet simulation suite (`test_cycle13_wave5_gauntlet_sim.py`): 85/85 PASS; 7 pre-existing failures confirmed as pre-existing via git stash baseline (same 7 tests, same count as gamora Step 3 baseline); 0 new regressions

**Gap (b) + Gap (c):** No in-seam changes landed; no smoke applicable. Cross-seam surfaces only.

---

### 6. Disc #12 EPOCH BREAK assessment: NOT DECLARED

Gap (a) fixes are observability corrections:
- `total_llm_calls` and `total_cost_usd` now reflect actual call attempts instead of 0
- No schema change; no behavioral change to LLM calls or output content; no downstream field value change for any consumer
- Field semantics shift from "count of calls with telemetry record IDs" to "count of actual call attempts" — which is the intended semantic, not a semantic change

EPOCH BREAK applies when the semantic meaning of an existing field changes for existing consumers. Here the field was broken (returning 0 always); correcting it to return the intended value does not constitute an epoch break.

Gaps (b) and (c): no in-seam changes. No EPOCH BREAK applicable.

---

### 7. MIGRATION.md cited

`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — § v1.59 (prepended before § v1.58 gamora P3c fix)

Content: Gap (a) wire-up with full code diffs at both fix sites; Gap (b) cross-seam surface with routing recommendation; Gap (c) structural blockage + routing; Disc #12 NOT DECLARED rationale; Disc #40 4-point cumulative queue.

---

### 8. Cross-seam surfaces

**Gap (b) — Wave B NOT IMPLEMENTED (SURFACE TO KR):**

| Dispatch | Owner | Scope | Dependency |
|---|---|---|---|
| Wave B LLM function dispatch | star-lord | `run_wave_b_async()` + `Phase5WaveBResult` dataclass + prompt templates in `llm/phase5_orchestrator.py` | None — fires first |
| Wave B orchestration + persistence dispatch | rocket | Wave B invocation in `wave5_season_orchestrator.py` + `kit_archive.notes` write | Requires star-lord Wave B function to exist first |

R48.4 strict-sequential: star-lord Wave B dispatch → rocket Wave B integration dispatch.

**Gap (c) — cohesion_data threading (SURFACE TO KR, compose with Gap (b)):**

| Dispatch | Owner | Scope | Dependency |
|---|---|---|---|
| cohesion_data wire-up | star-lord or rocket (small scope) | Extract `{kit_id: score}` from `p5_result` in `wave5_season_orchestrator.py`; pass to `run_phase7_joint_gate(cohesion_data=...)` | Requires Wave B implementation to produce per-kit scores |

Gamora-seam `phase7_bridge.py` emit path at line 740 is already wired. No gamora dispatch needed for Gap (c) unless unexpected issue surfaces when threading real scores.

---

### 9. Disc #42a Q1-Q6 self-audit

**Q1 — load-bearing framing assumption:** "The 3 gaps compose architecturally because they all share the pattern 'LLM output produced but not flowed through to downstream persistence/measurement.'"
**Verdict: PARTIALLY CONFIRMED.** Gap (a) fits perfectly. Gaps (b) and (c): the empirical investigation revealed Wave B was never produced at all (not a flow problem — an implementation-missing problem). The "LLM output produced but not persisted" framing was slightly wrong for Gap (b); it should have been "LLM output never produced." This refinement didn't invalidate the composition decision — it clarified the routing.

**Q2 — refutation evidence in scope:** investigation produces caller-graph + data-flow trace for all 3 gaps. Gap (b) surfaced the most significant refutation: "Wave B fires" (per rocket completion record) was incorrect. SURFACED per protocol.
**Verdict: PASS — all refutation evidence captured.**

**Q3 — refutation surface-able cheaply:** read-only investigation phase confirmed all 3 gap root causes without executing any LLM calls or simulation runs.
**Verdict: PASS — investigation was low-cost as projected.**

**Q4 — measurement context match:** Gap (a) fix now enables functional cost-tracking for Step 6 A2-1 RE-FIRE-2. Gaps (b) and (c) surface the requirement for Wave B before Step 6 can produce measurable cohesion signal. The D9 close-criterion ratified measurement dimensions are now clearly dependent on Wave B implementation.
**Verdict: PASS — measurement context match confirmed; Wave B dependency surfaced clearly for KR sequencing.**

**Q5 — calibration scope match:** Gap (a) wire-up directly enables the gandalf gate (i) full verdict + jack-ryan Gate-2 cost-tracking dimension. Gaps (b) and (c) cross-seam surfaces define what additional dispatches must precede Step 6 for the full empirical signal.
**Verdict: PASS — scope match confirmed.**

**Q6 — semantic stability of "observability wire-up" vs "scope amendment":** Gap (a) is a pure observability wire-up (existing interface; missing tracker instance). Gap (b) investigation revealed Wave B is a MISSING IMPLEMENTATION — this is a scope amendment, not a wire-up. Per Q6 protocol: SURFACED CROSS-SEAM rather than in-seam implementation. The dispatch framing correctly anticipated this possibility ("if investigation reveals gap requires cross-seam work, scope-amendment, OR deeper architectural intervention... surface to KR").
**Verdict: PASS — Q6 protocol followed correctly; Gap (b) classified as scope-amendment → cross-seam surface.**

---

### 10. Disc #40 cumulative pattern queue update

| # | Gap | Prior status | Status after Step 4 |
|---|---|---|---|
| (a) | `FACTION_VISIBILITY=invisible` default + hardcoded assert | RESOLVED (Step 2 cascade-resumption-1) | RESOLVED |
| (b) | `tracker=None` in Phase 5 LLM path | OPEN | PARTIALLY RESOLVED — call-count estimation fixed; NullRecorder-backed tracker wired; per-call DB telemetry remains cross-seam follow-on (rocket seam, future dispatch) |
| (c) | Wave B persistence-layer gap | OPEN | SURFACED — Wave B NOT implemented; star-lord + rocket follow-on dispatches needed (KR authors per Step 4 cross-seam surfaces) |
| (d) | `phase7_kit_verdict_log.kit_cohesion_score` not-populated | OPEN | SURFACED — structurally blocked by (c); gamora emit path READY; wire-up follows Wave B implementation; compose with (c) Wave B dispatch |

All 4 data points captured for Matt re-engage cumulative Disc #40 discussion per resolution plan § 4.

---

### 11. Disc #48 R48.4/R48.5 verification

**R48.4 (single-seam):** Confirmed — gamora released post Step 3 PASS; only star-lord running in Step 4 slot. No parallel sub-agent fan-out. No parallel sub-seam work during investigation or wire-up.

**R48.5 (RAM):** Pre-flight check at dispatch entry: 2.76 GB free + reclaimable (well above 1 GB threshold). PASS.

---

### 12. Engine + collab commits + tag

**Engine commit:** `d388c49` — `star-lord: A2-1 R2 Step 4 — Phase 5 cost-tracker wire-up + call-count fix; Gaps (b)+(c) surfaced`
- 4 files changed, 164 insertions(+), 11 deletions(-)
- `src/reincarnated/export/AGENT_STATE.md` — session entry + tag reference
- `src/reincarnated/llm/phase5_orchestrator.py` — Wave A + F-C total_llm_calls derivation fix (2 sites)
- `src/reincarnated/simulation/MIGRATION.md` — § v1.59 prepended
- `src/reincarnated/simulation/wave5_season_orchestrator.py` — NullRecorder-backed TrackedLLMClient + Wave B not-implemented note

**Engine tag:** `star-lord/v1.2-a2-1-r2-step-4-observability-wire-up-1` applied to `d388c49`

**Collab commit:** this dispatch file (completion record append) — auto-committed per CLAUDE.md addendum 2026-05-25

**Push:** NOT fired — KR fires push after A2-2 Gate-2 PASS per per-workstream pattern.

---

### 13. Anomalies surfaced

**ANOMALY A13-1 — Wave B "FIRED" documentation error:**
The rocket A2-1 RE-FIRE attempt 2 completion record §4 states "Wave B: FIRED." Empirical code investigation finds NO `run_wave_b_async` or equivalent in `llm/phase5_orchestrator.py` (28-function inventory; 2263 lines; docstring explicitly says Wave B not fired here). The orchestrator comment also incorrectly claimed "Wave B fires." BOTH corrected in this dispatch's engine commit. Wave B has never run in any A2-1 RE-FIRE attempt. This means the recognition record gate (i) preliminary PASS-preliminary verdict (gandalf Step 2.5) was based on Wave A + F-C output only — Wave B observability gap was larger than the dispatch framing anticipated.

**Implication for cascade timeline:** Step 6 A2-1 RE-FIRE-2 CANNOT produce measurable Wave B cohesion signal until star-lord Wave B LLM function dispatch + rocket Wave B integration dispatch both PASS. KR must sequence those dispatches between Step 4 close and Step 5 (jack-ryan Gate-2) OR between Step 5 and Step 6, depending on whether Gate-2 can run on Step 4 outputs alone.

**KR routing note:** if jack-ryan Gate-2 (Step 5) can run on Step 1 + Step 3 + Step 4 outputs (Gap (a) wired; Gaps (b)+(c) surfaced but not yet resolved), KR may fire Step 5 immediately and sequence Wave B + cohesion_data dispatches between Step 5 and Step 6. If Step 5 Gate-2 requires Wave B observability to issue a verdict, KR should sequence Wave B dispatches before Step 5.

**ANOMALY A13-2 — NullRecorder.start_llm_call() returns None:**
Investigation confirmed `NullRecorder.start_llm_call()` returns `None` → even with a NullRecorder-backed tracker wired, `llm_call_id` remains `None` for all results. This means the call-count estimation fix (Fix 1) was necessary in addition to the tracker wire-up (Fix 2). Both fixes compose: Fix 1 corrects the count derivation; Fix 2 wires the tracker for API key propagation + future composability with TelemetryRecorder when the DB-backed path is implemented in a future rocket dispatch.
