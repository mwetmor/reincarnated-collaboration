# Dispatch — 2026-06-01 — jack-ryan — Gate-1 pre-fire review of IA-1 V1 baseline season generation FIRE dispatch

**From:** knight-rider (immediate-arc orchestrator)
**To:** jack-ryan (critique-pair process side)
**Approved by:** Matt 2026-06-01 strategic reset + pre-commitment ratification + Gate-1 critique-pair discipline binds before IA-1 V1 fires
**Workstream tag:** `IA-1-V1-baseline-season-generation`
**Phase / phase-gate:** Pre-IA-1-V1-fire Gate-1
**Estimated effort:** ≤30 min (Pattern A short task; pre-commitment-bounded scope)
**Acceptance:** Gate-1 finding at `agentic_orchestration/qa/findings/2026-06-01-ia-1-v1-fire-gate-1.md`

---

## 1. Context

Matt 2026-06-01 strategic reset + pre-commitment ratification authorize IA-1 V1 autonomous fire (LOCK A: rocket + star-lord autonomous on config/prompt). Sequenced pre-fire confirmations landed:
- Star-lord (commit `4a2abf2`): MINIMAL-SETUP-REQUIRED (ANTHROPIC_API_KEY + rocket entry-point)
- Rocket (commit `155b6ba`): CLI-PATH-CONFIRMED at `python -m reincarnated.cli generate-season --seed 42 --output seasons/`; smoke recommended

KR has authored the IA-1 V1 fire dispatch. This Gate-1 reviews KR's fire dispatch BEFORE star-lord executes.

---

## 2. Authoritative reading

1. **THE dispatch under review:** `agentic_orchestration/dispatches/2026-06-01-star-lord-ia-1-v1-baseline-season-generation-fire.md`
2. **Pre-commitment ratification:** `agentic_orchestration/immediate-arc-pre-commitment-ratification-2026-06-01.md`
3. **Star-lord IA-1 readiness response:** `agentic_orchestration/star-lord/notes/2026-06-01-ia-1-engine-readiness-pre-fire-response.md`
4. **Rocket IA-1 entry-point confirmation:** `agentic_orchestration/rocket/notes/2026-06-01-ia-1-entry-point-confirmation-response.md`
5. **Immediate-arc workstream queue:** `agentic_orchestration/immediate-arc-workstream-queue-2026-06-01.md`
6. **WS1A.Q18 canonical lock:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
7. **Critique-pair gate protocol:** `agentic_orchestration/operating-procedures/critique-pair-gate-protocol.md`
8. **Your OP:** `agentic_orchestration/operating-procedures/jack-ryan.md`

---

## 3. Gate-1 review checklist

### Principle 1 — Math-before-code (n/a; LLM-named season generation, not math-hotspot)

### Principle 2 — Smoke-test / quality criterion
- **Check:** dispatch § 2 names smoke-first then full discipline (per rocket recommendation)
- **Check:** smoke acceptance criteria explicit (parse cleanly, drift-14 expected, per-primary counts)

### Principle 3 — Cross-seam impact
- IA-1 V1 produces new season JSON; drax consumes via IA-3 separate workstream
- **Check:** § 5 of dispatch states NOT applicable with explicit reason; honest

### Principle 4 — Decisions-log as truth
- No decisions-log entry from V1 fire; correct

### Principle 5 — Severity matters
- Apply standard INFO / WARN / BLOCK

### Cross-seam round-trip (Principle 6)
- § 5 states "not applicable"
- **Check:** if V1 output schema differs from established Phase 5+ convention, surface

---

## 4. Specific items to verify

### 4.1 Pre-commitment scope fidelity
- [ ] Dispatch correctly invokes LOCK A (rocket + star-lord autonomous)
- [ ] Architectural escape-clause triggers § 3 cited; star-lord escalates to KR if hit
- [ ] LOCK J additive amendments cited (consumer-side prompt amendments referencing Q18 vocab autonomous)
- [ ] Drift-14 disposition aligned with strategic reset (acceptable V1 baseline; vfx_coverage_manifest DEFERRED)

### 4.2 Entry-point fidelity
- [ ] Dispatch § 2 uses rocket-confirmed CLI path: `python -m reincarnated.cli generate-season --seed 42 --output seasons/`
- [ ] Dispatch § 2 Step 2 includes `--smoke` flag per rocket recommendation
- [ ] Dispatch correctly excludes `--theme-input` and `--no-coalesce` per rocket warning

### 4.3 Execution discipline
- [ ] Dispatch sequences env-precheck → smoke → full → close-summary
- [ ] Smoke acceptance criteria specified (drift-14 expected; cohesion-judge + naming sub-pipelines fire)
- [ ] Full acceptance criteria specified (all cohorts have LLM-named identities)
- [ ] Surface-to-KR mechanism for smoke FAIL named explicitly

### 4.4 Output expectations
- [ ] Engine-repo artifact path named (`seasons/<season-id>/`)
- [ ] Meta-repo close-summary path named (`star-lord/notes/2026-06-01-ia-1-v1-close-summary.md`)
- [ ] Auto-commit + auto-push per established cycle-push pattern

### 4.5 Out-of-scope discipline
- [ ] IA-2 audit (parallel; elrond seam) explicitly out-of-scope
- [ ] IA-3 drax integration (post-V1 close) explicitly out-of-scope
- [ ] IA-1 V2 re-fire explicitly out-of-scope
- [ ] LOCK H quality discipline (gandalf audit at V2 close NOT V1) correctly deferred
- [ ] vfx_coverage_manifest extension DEFERRED per strategic reset

### 4.6 KR-cumulative-pattern-surface watch
- [ ] Dispatch does NOT pre-decide whether smoke or full will succeed
- [ ] Dispatch does NOT pre-decide V1 verdict (SUCCESS/DEGRADED/FAILURE)
- [ ] Dispatch does NOT pre-decide LLM token cost
- [ ] Dispatch honors star-lord seam authority on execution

### 4.7 Anti-patterns
- [ ] No conflation of V1 fire with V2 re-fire
- [ ] No conflation of IA-1 with IA-2 (parallel; separate seams)
- [ ] No conflation with IA-3 (depends on this output)
- [ ] No premature unblocking of long-arc deferred items

---

## 5. Gate-1 verdict format

Author finding at `agentic_orchestration/qa/findings/2026-06-01-ia-1-v1-fire-gate-1.md`:

- **Verdict:** INFO / WARN / BLOCK
- **Pre-commitment scope fidelity:** PASS / FAIL
- **Entry-point fidelity:** PASS / FAIL
- **Execution discipline:** PASS / FAIL
- **Per-section findings**
- **Remediation guidance** (if applicable)
- **PASS / PASS-with-INFO / BLOCK final classification**

If PASS / PASS-with-INFO: KR fires star-lord IA-1 V1 immediately (background per longer wall-clock).
If BLOCK: KR remediates; re-Gate-1.

---

## 6. Cross-seam contract change? (Principle 6)

**Answer:** not applicable — this Gate-1 review authors a critique-pair finding.

---

## 7. Acceptance criteria

- [ ] IA-1 V1 fire dispatch reviewed against all checklist items
- [ ] Gate-1 finding authored
- [ ] Verdict + remediation guidance (if applicable) stated
- [ ] Completion record appended

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**Verdict:** INFO / WARN / BLOCK
**Final classification:** PASS / PASS-with-INFO / BLOCK
**Finding artifact:** agentic_orchestration/qa/findings/2026-06-01-ia-1-v1-fire-gate-1.md
**Pre-commitment scope fidelity:** PASS / FAIL
**Entry-point fidelity:** PASS / FAIL
**Execution discipline:** PASS / FAIL
**Key items surfaced:** brief
**Routing back to KR:** fire star-lord IA-1 V1 / remediate first / hold
```

---

**End of jack-ryan IA-1 V1 fire Gate-1 dispatch.**
