# DISPATCH — Gamora Cycle 14 A2-1 Cascade-Resumption-2 Step 1 (Concern #3 Caller-Graph Audit + P3a Viability Check)

**Authored:** 2026-05-29 (Mode A Phase A2 cascade-resumption-2; Concern #3 resolution authorization § 3.1)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** gamora (engine simulation + spirit-guide seam owner; `simulation/`)
**Pattern:** Pattern A-deep audit-only dispatch (caller-graph enumeration + method-signature viability check + brief output); ~15-30min wall-clock per authorization § 3.1
**Expected effort:** ~15-30min (read-only audit; no code-touch)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-29 in-session direction (Concern #3 resolution authorization § 3.1 + pre-ratified contingent decision-tree § 3.2) + hive-mind decision-routing (in-scope cascade-resumption-2 work; seam-owner does audit; KR routes per § 3.2 matrix WITHOUT re-surfacing to Matt) + R48.4 single-seam

---

## 0. CONTEXT (read first — 3 min)

### 0.1 Cascade-resumption-2 entry lineage

| # | Event | Status |
|---|---|---|
| Cascade-resumption-1 Step 1-4 (Concerns #1 + #2) | gamora Step 1 ✅ + rocket Step 2 ✅ + jack-ryan Step 3 ✅ + rocket Step 4 ❌ MATERIAL FAIL | Concerns #1 + #2 RESOLVED; Concern #3 surfaced |
| KR Matt-surface (Concern #3) | collab `1a8f12c` | Cascade HALTED per resolution plan § 3 second-material-fail clause |
| Concern #3 resolution authorization (Matt-ratified) | `agentic_orchestration/gandalf/notes/2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md` (collab `0ba55b2`) | Pre-ratified contingent decision-tree per § 3.2 matrix |
| Cascade-resumption-2 fire prompt | `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-cascade-resumption-2-fire-prompt.md` (collab `bd846b6`) | KR cascade-drive through Cycle 14 end |
| **Cascade-resumption-2 Step 1 (THIS DISPATCH)** | this dispatch | ⏳ PENDING — Concern #3 caller-graph audit |

### 0.2 Concern #3 — technical specification (KR-verified empirically)

**The bug (KR-confirmed at phase7_bridge.py:313-387 + gauntlet_sim.py:1068-1076):**

| Site | What happens |
|---|---|
| `phase7_bridge.py:340` | Phase 7 runs **1 cohort per kit** (single `gauntlet_archetype`, by Phase 7 design via `cohorts=[gauntlet_archetype]` in `legendary_config`) |
| `phase7_bridge.py:368` | Phase 7 reads `enc_passed = round(quality_report.mean_encounters_passed_per_kit)` |
| `gauntlet_sim.py:1068-1076` | Mean computed iterating over **ALL 4 `COHORT_ARCHETYPES`** with `statistics.mean(all_enc_pass_counts)` where 3 unrun cohorts contribute 0 |

Net: when Phase 7 runs 1 cohort, mean = `actual_pass_count / 4` → pass_rate = mean / 18 ≤ 0.167 universally → Phase 7 mechanical-gate threshold (P7_GAUNTLET_PASS_FLOOR = 0.70) far above ceiling → 18/18 TIER_1_REJECT regardless of synthetic-kit KPM achievement (Step 1 KPM recalibration is empirically intact; Concern #3 masks Step 1's effect).

### 0.3 Locked direction (Matt 2026-05-29 — Path A audit-then-route)

Per Concern #3 authorization § 3.1: audit BEFORE choosing P3a vs P3c. Audit findings determine routing per § 3.2 matrix. KR routes WITHOUT re-surfacing to Matt EXCEPT for Case C + Case E combined (neither path clean) OR unexpected audit-finding pattern (per § 4).

- **P3a** (surgical Phase 7 bridge): access `kit_results[0].encounters_passed(gauntlet_archetype)` directly at `phase7_bridge.py:368` (replacing `mean_encounters_passed_per_kit` extraction)
- **P3b** (semantic-level change) — **REJECTED per authorization § 8 as bug-fix path** — Phase 7 gate semantics locked at `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md`; P3b reserved as separable Pattern B post-cascade-close
- **P3c** (upstream architectural): divide aggregate by `len(p7_cohorts_actually_run)` instead of fixed `COHORT_ARCHETYPES` count at `gauntlet_sim.py:1068-1076`

### 0.4 Disc #42a framing-audit at dispatch consumption

KR's authoring applied Q1-Q6. Gamora should re-apply at consumption:

- **Q1 — load-bearing framing assumption:** "Caller-graph audit + method-signature viability check on `gauntlet_sim.GauntletQualityReport.mean_encounters_passed_per_kit` is sufficient to determine the architecturally-honest routing between P3a (surgical Phase 7 bridge) and P3c (upstream architectural fix at source)."
- **Q2 — refutation evidence in scope:** the audit IS the refutation evidence; enumerated callers + per-caller divisor-dependency semantics + P3a method viability check
- **Q3 — refutation surface-able cheaply:** yes — read-only audit at gamora's seam-internal tooling (`grep -rn "mean_encounters_passed_per_kit"` in engine + read related code paths); ~15-30min wall-clock
- **Q4 — measurement context match:** the audit measures what the callers actually require (divisor=4 vs divisor=actual-count semantics) AND whether the P3a method exists with the right signature; both are direct empirical measurements
- **Q5 — calibration scope match:** the audit's scope (callers of `mean_encounters_passed_per_kit` in the engine codebase) matches the impact scope of either P3a or P3c fix
- **Q6 — semantic stability of "caller graph" + "P3a viability":** "caller graph" = all sites in `engine/` that read `GauntletQualityReport.mean_encounters_passed_per_kit` (or accessor equivalent); "P3a viability" = does `kit_results[0].encounters_passed(gauntlet_archetype)` exist + accept archetype param OR is it accessible via existing accessor pattern

If any framing refutes, SURFACE TO KR before audit fire.

### 0.5 Audit-output downstream consumption (KR routing per § 3.2 matrix)

KR consumes audit findings and routes per the matrix:

| Caller graph | P3a method viability | KR action |
|---|---|---|
| Single (only Phase 7) | viable | **P3c** (preferred); fallback **P3a** if P3c blocks |
| Single (only Phase 7) | non-viable | **P3c** (forced) |
| Multi, all full-set | viable | **P3c** (preferred); fallback **P3a** if P3c blocks |
| Multi, all full-set | non-viable | **P3c** (forced) |
| Multi, some partial-set + divisor-dependent | viable | **P3a** (surgical) + P3c-tech-debt-flag for Cycle 14+ |
| Multi, some partial-set + divisor-dependent | non-viable | **SURFACE to Matt queue** — neither path clean; design call required (per authorization § 4) |

Gamora produces the audit findings + per-caller semantic-equivalence assessment; KR makes the routing call.

---

## 1. THE TASK

**Enumerate all callers of `gauntlet_sim.GauntletQualityReport.mean_encounters_passed_per_kit` (or equivalent accessor), determine per-caller semantic dependency on divisor=4 dilution vs divisor=actual-count equivalent, and audit method signature for P3a viability check. Produce brief audit-findings report.**

### 1.1 Pre-flight (REQUIRED before audit fire)

1. **Disc #48 R48.5 vm_stat check:** confirm > 1 GB free + reclaimable (KR pre-flight at Step 1 entry showed ~2.84 GB available; verify still holds at moment-of-fire)
2. **Disc #48 R48.4 single-seam confirm:** no other sub-agent in-flight; only this dispatch's gamora running
3. **Engine state confirm:** HEAD at `98e1825` (rocket A2-1 RE-FIRE attempt 2 AGENT_STATE post-FAIL); Step 1 + Step 2 prior cascade commits + tags intact (`gamora/v2.13-a2-1-step-1-synthetic-kit-kpm-recalibration-1`, `rocket/v1.1-a2-1-step-2-faction-visibility-visible-1`)
4. **Verify Concern #3 sites haven't drifted:** read `phase7_bridge.py` lines 313-387 + `gauntlet_sim.py` lines 1060-1080 to confirm the bug specification at § 0.2 matches current HEAD

### 1.2 Audit scope (per Concern #3 authorization § 3.1)

**Scope item 1 — caller-graph enumeration:**

- `grep -rn "mean_encounters_passed_per_kit" ~/Games/reincarnated-engine/src/`
- For each match: identify the caller (file + line + function + dispatch context)
- Distinguish: (a) the producer (`gauntlet_sim.py:1068-1076` — assignment site) (b) the consumer (`phase7_bridge.py:368` — current known) (c) any additional consumers

**Scope item 2 — per-caller semantic-equivalence assessment:**

For each consumer caller:
- Does it always populate all 4 `COHORT_ARCHETYPES` in its `run_gauntlet_sim()` invocation (via `legendary_config["cohorts"]`)? OR does it sometimes populate a subset (like Phase 7's `[gauntlet_archetype]` 1-cohort case)?
- Does it depend on divisor=4 dilution semantics (i.e., would divisor=actual-count change its acceptance criterion)? OR is divisor=actual-count semantically equivalent for its use?
- Capture the caller's intent from comments + docstrings + dispatch references

**Scope item 3 — P3a method-signature viability check:**

For the candidate replacement `kit_results[0].encounters_passed(gauntlet_archetype)`:
- Does the method `encounters_passed()` exist on the kit_result object type (likely `KitResult` or `GauntletKitResult` per `gauntlet_sim.py`)?
- Does it accept an archetype parameter (cohort string) to filter by cohort?
- Is the return type compatible (int or float — count of encounters passed for that cohort)?
- If method doesn't exist as-is, is there an existing accessor that exposes the same data (e.g., `kit_results[0].encounters_passed_by_cohort[gauntlet_archetype]` dict-access pattern)?

**Scope item 4 — secondary observations capture:**

- Note any related Disc #40 scaffold patterns surfaced during audit (e.g., other aggregate-metric extraction sites with similar cohort-divisor risk)
- Note any related Disc #11 hygiene observations (e.g., comments/docstrings out of date with code)
- These are INFO-class for completion record; do NOT fix in this audit dispatch (audit-only scope)

### 1.3 Acceptance criterion (per Concern #3 authorization § 3.1)

- ✅ Complete caller-graph enumeration (all consumers of `mean_encounters_passed_per_kit` accessor enumerated with file+line+function+dispatch context)
- ✅ Per-caller semantic-equivalence assessment (divisor=4 dependency vs divisor=actual-count equivalence per caller)
- ✅ P3a method-signature viability check (existence + signature + return-type compatibility)
- ✅ Brief output at `agentic_orchestration/gamora/notes/2026-05-29-concern-3-caller-graph-audit.md`
- ✅ Disposition recommendation per § 3.2 matrix (gamora indicates which case the audit findings map to)
- ✅ Disc #42a Q1-Q6 framing-audit self-verification at audit completion
- ✅ Auto-commit per CLAUDE.md addendum 2026-05-25
- ✅ Do NOT push — KR fires push after A2-2 Gate-2 PASS per per-workstream pattern
- ✅ NO CODE-TOUCH — this is audit-only

### 1.4 Brief output format (per Concern #3 authorization § 3.1)

Output at `agentic_orchestration/gamora/notes/2026-05-29-concern-3-caller-graph-audit.md` with:

1. **VERDICT** — single-line: "Concern #3 caller-graph audit complete; routing recommendation per § 3.2 matrix: Case [A/B/C/D/E]; KR action: [P3a/P3c/Surface]"
2. **Caller-graph table** — enumerated consumers with file+line+function+dispatch context
3. **Per-caller semantic-equivalence assessment table** — divisor=4 dependency vs divisor=actual-count equivalence per caller
4. **P3a method-signature viability check** — existence + signature + return-type compatibility; example code snippet if helpful
5. **Disposition mapping to § 3.2 matrix** — which case (A/B/C/D/E) the audit maps to; rationale
6. **Disc #42a Q1-Q6 self-audit** — verify audit captures what dispatch asked
7. **Secondary observations** — Disc #40 + Disc #11 patterns surfaced (INFO-class; not fixed in this dispatch)
8. **Cross-references** — Concern #3 authorization + dispatch + cascade-resumption-2 fire prompt + engine files audited
9. **Sign-off** — gamora + date + completion timestamp

### 1.5 Completion-record format (append to this dispatch)

Append a `## Completion record` section with:

1. **VERDICT** — single line: audit complete + § 3.2 matrix mapping + KR-recommended action
2. **Audit-findings brief path** — full file path
3. **Caller-graph summary** — count of consumers + brief enumeration
4. **P3a viability** — viable / non-viable + rationale
5. **§ 3.2 matrix case mapping** — A / B / C / D / E + rationale
6. **Disc #42a Q1-Q6 self-audit** — all 6 questions + verdicts
7. **Disc #48 R48.4/R48.5 verification** — no other sub-agent in-flight; vm_stat captured
8. **Engine + collab commits** — gamora audit-brief commits
9. **Telemetry output paths** — N/A (no telemetry; audit-only)
10. **Any anomalies surfaced** during audit

---

## 2. CROSS-SEAM CONTRACT CHANGE? (Principle 6)

**No** — audit-only; no production code change. Findings consumed downstream by KR for routing per § 3.2 matrix; downstream gamora P3a or P3c fix dispatch will surface any cross-seam contract change at that dispatch's authoring.

---

## 3. QUALITY CRITERION (KR OP § 3.11)

**Game-quality goal:** produce architecturally-honest routing decision between P3a (surgical Phase 7 bridge fix) and P3c (upstream architectural fix at gauntlet_sim source) by empirical caller-graph audit, avoiding cross-seam blast from P3c if non-Phase-7 callers depend on divisor=4 semantics, while also avoiding leaving the architectural footgun at source if no callers depend on it.

**Refutation conditions:**
- Caller graph reveals unexpected pattern not enumerated in § 3.2 matrix — refute = SURFACE TO KR before continuing audit (pre-ratification doesn't cover unenumerated case per authorization § 4)
- P3a method viability fails AND caller graph shows Case C (multi-caller partial-set + divisor-dependent) — refute = SURFACE TO KR (Case C + Case E combined; neither path clean per § 3.2 / § 4)
- Dispatch framing pre-commits to a decision Matt has not ratified — NO (Path A audit-then-route Matt-ratified per Concern #3 authorization § 3.1 + § 3.2)
- Dispatch introduces pre-authored taxonomy without justification (#41 candidate) — N/A
- Dispatch introduces scaffold value not flagged as pending-decision (#40) — N/A (audit-only; no code change introducing scaffold)

If any refutation condition triggers, SURFACE TO KR before continuing audit.

---

## 4. OUT OF SCOPE

- ❌ Any code-touch (this is audit-only; downstream gamora P3a/P3c fix dispatch will do the code change after KR routes)
- ❌ Phase 7 mechanical-gate architectural redesign (P3b — REJECTED as bug-fix path per authorization § 8)
- ❌ Star-lord cost-tracker wire-up (Step 3 of cascade-resumption-2; star-lord scope)
- ❌ Jack-ryan Gate-2 (Step 4)
- ❌ rocket A2-1 RE-FIRE-2 (Step 5)
- ❌ Doc 48 class-roster A/B comparison execution (A2-5 scope; gandalf)
- ❌ Disciplines #41/#44/#45/#46 batched canonical-write (A2-6 scope; jack-ryan)
- ❌ Cohesion-threshold (`cohesion_judge_confidence >= 0.75`) recalibration — capture-and-watch only
- ❌ Player-facing faction-architecture commitments — deferred-commitments recognition record stands
- ❌ Decisions-log canonical writes — jack-ryan owns; deferred to Matt re-engage
- ❌ Phase 5 placeholder bug investigation (Path E REJECTED earlier; Concern #2 resolved Path D)
- ❌ Cycle 16+ BC axis expansion impl
- ❌ Pushing without KR coordination
- ❌ Parallel sub-agent fan-out under R48.4

---

## 5. RISKS + COMPLICATIONS

- **Audit-finding Case C + Case E combined:** if caller graph shows multi-caller partial-set + divisor-dependent semantics AND P3a method non-viable — SURFACE TO KR per authorization § 4 (Matt design call required)
- **Unexpected audit-finding pattern:** if caller graph or method-signature shows pattern not enumerated in § 3.2 matrix — SURFACE TO KR per authorization § 4 (pre-ratification doesn't cover)
- **Secondary observations volume:** if Disc #40 / Disc #11 secondary patterns surface in unexpected volume during audit, capture in INFO section of completion record but DO NOT scope-expand audit (audit-scope limited to Concern #3 routing decision)

---

## 6. URGENCY + SEQUENCING

**Fires under R48.4 single-seam IMMEDIATELY (cascade halted at Step 4 fail; cascade-resumption-2 Step 1 is the unblock).** Subsequent cascade-resumption-2 steps fire serially per fire prompt sequence:

- Step 2 KR routes per § 3.2 matrix (no sub-agent; KR decision)
- Step 2.5 gandalf gate (i) preliminary assessment (sub-agent; reads on-disk cascade artifacts; ~30-60min)
- Step 3 gamora P3a/P3c fix (sub-agent)
- Step 4 star-lord cost-tracker wire-up (sub-agent)
- Step 5 jack-ryan Gate-2 (sub-agent; Pattern E)
- Step 6 rocket A2-1 RE-FIRE-2 (sub-agent)
- Step 7+ cascade through A2-2 → A2-7

A2-1 Step 1 audit PASS → KR routes Step 2 + queues gandalf gate (i) + queues gamora Step 3 fix.

A2-1 Step 1 audit returns Case C + Case E combined OR unexpected pattern → SURFACE TO KR per authorization § 4 (Matt design call).

---

## 7. SURFACING-TO-KR PROTOCOL

Append completion record (interim OR final) at any of:

- ✅ Caller-graph enumeration complete + P3a viability check complete + § 3.2 matrix mapping clear → normal close (KR routes per matrix)
- ⚠️ Audit-finding Case C + Case E combined → SURFACE IMMEDIATELY before continuing (authorization § 4)
- ⚠️ Audit-finding unexpected pattern (not in § 3.2 matrix) → SURFACE IMMEDIATELY before continuing (authorization § 4)
- ⚠️ Disc #42a Q1-Q6 framing-audit refutes pre-imposed assumption → SURFACE IMMEDIATELY
- ⚠️ Disc #48 R48.5 mid-audit RAM pressure (< 500 MB) → pause + SURFACE (unlikely for read-only audit)
- 🚨 Substantial unexpected failure mode → SURFACE IMMEDIATELY

---

## 8. REFERENCES

- `agentic_orchestration/gandalf/notes/2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md` — authoritative Concern #3 resolution authorization + pre-ratified contingent decision-tree (§ 3.1 audit + § 3.2 matrix + § 4 surface-edge-cases)
- `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-cascade-resumption-2-fire-prompt.md` — KR cascade-drive prompt
- `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` — original Phase A2 resolution plan (Steps 1-5+; § 3 surface conditions carry forward; § 1.5 D13 parallel-fire)
- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-a2-1-step-4-refire-post-step1-step2.md` — A2-1 RE-FIRE attempt 2 dispatch + completion record (FAIL diagnosis at § Completion record § 15 — Concern #3 surface)
- `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Phase A1 closure record + Matt 3-gate authorization
- `agentic_orchestration/cycle-14-hive-mind-state.md` — Wave 5 state (cascade halted; resumption-2 in-flight)
- `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` — Disc #42a Q1-Q6 architectural argument
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` lines 313-387 — Concern #3 consumer site (`_run_gauntlet_for_kit` + line 368 extraction)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` lines 1060-1080 — Concern #3 producer site (`mean_encounters_passed_per_kit` compute with 4-cohort iteration + fixed divisor)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — § v1.57 (cascade-resumption-1 Step 1)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` line 3536 — D9 ratified close-criterion LOCKED
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1/#5/#11/#21/#22/#40/#42a/#48 active
- `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` — Phase 7 gate semantics LOCKED (P3a/P3c preserve; P3b would change semantic but REJECTED)
- Engine HEAD: `98e1825` (rocket A2-1 RE-FIRE attempt 2 AGENT_STATE post-FAIL); tag `rocket/v1.2-a2-1-refire-2-season-001-fail-0`

---

**KR signature:** authored per Phase A2 cascade-resumption-2 authorization + R48.4 single-seam (gamora alone) + Disc #42a meta-observation 5 self-vigilance (Concern #3 sites verified at engine HEAD via Read of phase7_bridge.py:313-387 + gauntlet_sim.py:1060-1080; bug specification at dispatch § 0.2 matches current code) + auto-commit per CLAUDE.md addendum 2026-05-25.

This dispatch is the cheapest empirical refutation of "what is the cleanest architectural fix for Concern #3 — surgical Phase 7 bridge (P3a) or upstream architectural fix at gauntlet_sim source (P3c)?" — caller-graph audit + method-signature viability check at gamora's seam-internal cost (no LLM spend; ~15-30min wall-clock; read-only).

A2-1 cascade-resumption-2 Step 1 audit PASS = Concern #3 routing decision unblocked + KR routes per § 3.2 matrix → cascade-resumption-2 proceeds Step 2 (KR routing) → Step 2.5 (gandalf gate (i) preliminary assessment) → Step 3 (gamora P3a/P3c fix) → Step 4 (star-lord cost-tracker) → Step 5 (jack-ryan Gate-2) → Step 6 (rocket A2-1 RE-FIRE-2) → cascade through A2-2 → A2-7 toward Cycle 14 v1 MVP D9 close.
