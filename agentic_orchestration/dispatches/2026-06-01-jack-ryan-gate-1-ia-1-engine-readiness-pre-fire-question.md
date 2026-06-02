# Dispatch — 2026-06-01 — jack-ryan — Gate-1 DESIGN-MODE pre-fire review of IA-1 engine-readiness pre-fire question dispatch

**From:** knight-rider (immediate-arc orchestrator)
**To:** jack-ryan (critique-pair process side)
**Approved by:** Matt 2026-06-01 strategic reset directive + KR critique-pair discipline binds before IA-1 fires
**Workstream tag:** `IA-1-V1-baseline-season-generation`
**Phase / phase-gate:** Pre-IA-1-pre-fire-question (Gate-1 on KR pre-fire query authoring)
**Estimated effort:** ≤1 hour (Pattern A short task; KR meta-dispatch review)
**Acceptance:** Gate-1 finding at `agentic_orchestration/qa/findings/2026-06-01-ia-1-pre-fire-question-gate-1.md`

---

## 1. Context

Matt 2026-06-01 strategic reset narrows the workstream queue to immediate-arc. IA-1 (V1 baseline engine season generation) is authorized to fire pending engine-readiness confirmation. KR has authored a pre-fire question dispatch routing to star-lord (primary) + rocket (coordination) asking: *"Can engine fire season generation NOW or is minimal setup needed?"*

This Gate-1 reviews KR's pre-fire question dispatch BEFORE it routes to star-lord + rocket.

---

## 2. Authoritative reading

1. **THE dispatch under review:** `agentic_orchestration/dispatches/2026-06-01-star-lord-rocket-ia-1-engine-readiness-pre-fire-question.md`
2. **Immediate-arc workstream queue (§ IA-1 spec):** `agentic_orchestration/immediate-arc-workstream-queue-2026-06-01.md`
3. **WS1A.Q18 canonical lock + amendment-pass closes:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
4. **WS1 sub-phase 5f migration (engine seam; substrate state):** engine commit `fcc4887`
5. **WS1 Gate-2 finding (Drift-14 forward note):** `agentic_orchestration/qa/findings/2026-06-01-ws1-sub-phase-5f-gate-2.md`
6. **Hypothesis-flow architecture (kit identity context):** `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md`
7. **Critique-pair gate protocol:** `agentic_orchestration/operating-procedures/critique-pair-gate-protocol.md`
8. **Your OP:** `agentic_orchestration/operating-procedures/jack-ryan.md`

---

## 3. Gate-1 review checklist

### Principle 1 — Math-before-code (n/a; pre-fire query is assessment-only)

### Principle 2 — Smoke-test / quality criterion
- **Check:** acceptance criteria § 8 of dispatch are concrete (readiness verdict + minimal-setup steps + drift-14 + LLM-readiness + wall-clock estimate)
- **Check:** "READY-TO-FIRE / MINIMAL-SETUP-REQUIRED / BLOCKED" verdict shape is unambiguous

### Principle 3 — Cross-seam impact
- Pre-fire question response is assessment artifact at `agentic_orchestration/star-lord/notes/`
- **Check:** § 7 of dispatch states NOT applicable for pre-fire question itself; honest
- **Check:** if minimal-setup IS named in response, that setup itself may be cross-seam → KR routes separate setup dispatch with Principle 6 assessment (dispatch correctly defers this)

### Principle 4 — Decisions-log as truth
- No decisions-log entry from pre-fire question; correct deferral

### Principle 5 — Severity matters
- Apply standard INFO / WARN / BLOCK

### Cross-seam round-trip (Principle 6)
- Pre-fire question itself is NOT cross-seam contract change
- **Check:** dispatch correctly notes that setup itself MAY be cross-seam (separate dispatch)

---

## 4. Specific items to verify

### 4.1 Pre-fire question fidelity to Matt strategic reset directive
- [ ] § 2 of dispatch transcribes Matt's verbatim pre-fire question accurately
- [ ] Specifically-assess sub-items match Matt's spec (Phase 5+ end-to-end + cohesion judge + skill-naming + faction-naming + pool.json schema + LLM-call infrastructure)

### 4.2 Seam-owner authority respect
- [ ] § 6 of dispatch correctly holds engine-readiness assessment + minimal-setup spec at star-lord seam authority
- [ ] Rocket coordination explicit (substrate-side readiness; secondary)
- [ ] Escalation path named if setup exceeds star-lord seam authority

### 4.3 Drift-14 auto-demote handling
- [ ] § 3.3 of dispatch correctly notes Drift-14 auto-demote behavior
- [ ] Strategic-reset disposition explicit (vfx_coverage_manifest extension DEFERRED; Drift-14 auto-demote acceptable for V1 baseline OR named workaround)
- [ ] Star-lord asked to assess + report (§ 4 item 5)

### 4.4 Scope-bound discipline (CRITICAL)
- [ ] § 5 of dispatch states "PRE-FIRE QUESTION, NOT EXECUTION" explicitly
- [ ] § 5 states "Minimal setup ONLY"
- [ ] § 5 states substrate state is STABLE (do NOT propose changing pool.json)
- [ ] § 5 states vfx_coverage_manifest extension OUT-OF-SCOPE per strategic reset
- [ ] Star-lord asked to surface back if Drift-14 is load-bearing (immediate-arc directive skip allowed)

### 4.5 Engine state context completeness
- [ ] § 3 of dispatch enumerates relevant post-WS1 + post-WS1.AP / WS1.AP-FU engine-side artifacts
- [ ] Pool.json v1.1 schema extension noted (4 additive fields)
- [ ] Physical taxonomy registry separate file noted
- [ ] Drift-14 forward note from WS1 Gate-2 carried forward

### 4.6 KR-cumulative-pattern-surface watch
- [ ] Dispatch does NOT pre-decide whether engine is ready (star-lord assesses)
- [ ] Dispatch does NOT pre-decide minimal-setup steps (star-lord names)
- [ ] Dispatch does NOT pre-decide LLM-call infrastructure state (star-lord assesses)
- [ ] Dispatch does NOT pre-decide V1 fire wall-clock (star-lord estimates)

### 4.7 Anti-patterns
- [ ] Dispatch does NOT declare "season fire authorized" prematurely
- [ ] No conflation of IA-1 pre-fire question with IA-1 V1 fire (separate dispatches)
- [ ] No conflation with IA-2 (separate workstream; parallel fire)
- [ ] No premature unblocking of long-arc deferred items (Q16/Q17/Q19/WS3/WS4 stay DEFERRED)

---

## 5. Gate-1 verdict format

Author finding at `agentic_orchestration/qa/findings/2026-06-01-ia-1-pre-fire-question-gate-1.md`:

- **Verdict:** INFO / WARN / BLOCK
- **Pre-fire question fidelity check:** PASS / FAIL
- **Seam-owner authority respect check:** PASS / FAIL
- **Scope-bound discipline check:** PASS / FAIL (CRITICAL — scope creep risk)
- **Per-section findings**
- **Remediation guidance** if WARN or BLOCK
- **PASS / PASS-with-INFO / BLOCK final classification**

If PASS / PASS-with-INFO: KR routes pre-fire question to star-lord + rocket immediately.
If BLOCK: KR remediates per your guidance; re-Gate-1.

---

## 6. Cross-seam contract change? (Principle 6 for THIS dispatch)

**Answer:** not applicable — this Gate-1 review authors a critique-pair finding.

---

## 7. Acceptance criteria

- [ ] IA-1 pre-fire question dispatch reviewed against all checklist items
- [ ] Gate-1 finding authored
- [ ] Verdict + remediation guidance (if applicable) stated
- [ ] Completion record appended

---

## 8. Out of scope

- IA-1 V1 fire dispatch (separate; authored on star-lord readiness confirmation)
- IA-2 dispatch (separate Gate-1 review)
- IA-3 dispatch (not yet authored; awaits IA-1 V1 close)
- Long-arc deferred items (Q16/Q17/Q19/WS3/WS4/WS1A.3/4/vfx_coverage_manifest)

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-01
**Verdict:** INFO
**Final classification:** PASS
**Finding artifact:** agentic_orchestration/qa/findings/2026-06-01-ia-1-pre-fire-question-gate-1.md
**Pre-fire question fidelity:** PASS
**Seam-owner authority respect:** PASS
**Scope-bound discipline:** PASS
**Key items surfaced:** All 7 checklist sections PASS. One INFO observation: § 8 acceptance criteria are correctly written for star-lord's response (not dispatch completion) — structurally correct, noted for audit clarity only. Drift-14 handling correctly threads "note behavior / don't pre-decide answer." No WARN or BLOCK items.
**Routing back to KR:** route pre-fire question to star-lord+rocket immediately
```

---

**End of jack-ryan IA-1 pre-fire question Gate-1 dispatch.**
