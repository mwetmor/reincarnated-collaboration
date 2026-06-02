# Dispatch — 2026-06-01 — jack-ryan — Gate-1 pre-fire review of IA-3 Phase 4 V2 iteration dispatch

**From:** knight-rider (immediate-arc orchestrator)
**To:** jack-ryan (critique-pair process side)
**Approved by:** Matt 2026-06-01 strategic reset + Gate-1 critique-pair discipline before IA-3 P4 V2 fires
**Workstream tag:** `IA-3-drax-V2-iteration`
**Phase / phase-gate:** Pre-IA-3 P4 Gate-1
**Estimated effort:** ≤20 min (Pattern A; mirror of P1 V1 Gate-1)
**Acceptance:** Gate-1 finding at `agentic_orchestration/qa/findings/2026-06-01-ia-3-phase-4-gate-1.md`

---

## 1. Context

IA-1 V2 SUCCESS (season_000043; brine theme; commit `46e8165`). gandalf design-quality audit complete per LOCK H (note-only PASS-with-design-concerns; `49a3dec`). Per LOCK F MVP-discipline + zero-halt: KR routes IA-3 P4 V2 iteration (drax mirrors P1 pattern; loads V2 alongside V1; preserves V1 reference).

This Gate-1 reviews KR's IA-3 P4 V2 dispatch BEFORE drax fires.

---

## 2. Authoritative reading

1. **THE dispatch under review:** `agentic_orchestration/dispatches/2026-06-01-drax-ia-3-phase-4-v2-iteration.md`
2. **IA-1 V2 close record:** `agentic_orchestration/ia-1-v2-close-record-2026-06-01.md`
3. **IA-3 P1 close summary (precedent):** `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-1-mvp-integration-close.md`
4. **gandalf design-quality audit (note-only):** `agentic_orchestration/gandalf/notes/2026-06-01-ia-1-v1-v2-design-quality-audit.md`
5. **Pre-commitment ratification (LOCK F + LOCK G + escape clause):** `agentic_orchestration/immediate-arc-pre-commitment-ratification-2026-06-01.md`

---

## 3. Gate-1 review checklist

### Principle 1 — Math-before-code (n/a)

### Principle 2 — Smoke-test / quality criterion
- **Check:** § 6 acceptance criteria concrete (V2 data renders; V1 PRESERVED; no new UI)

### Principle 3 — Cross-seam impact
- Data-add only
- **Check:** § 5 of dispatch states "NOT applicable" honest

### Principle 4 — Decisions-log as truth
- No decisions-log entry from V2 iteration; correct

### Principle 5 — Severity matters
- Standard INFO / WARN / BLOCK

### Cross-seam round-trip (Principle 6)
- N/A data-add

---

## 4. Specific items to verify

### 4.1 LOCK F MVP-discipline (CRITICAL — same as P1 Gate-1)
- [ ] Dispatch explicitly states "EXISTING components ONLY"
- [ ] § 2.5 OUT-of-scope explicit (no new UI / no redesign)
- [ ] § 2.2 mirror of P1 V1 pattern (no new architectural moves)

### 4.2 V1 preservation discipline
- [ ] V1 season_000042 PRESERVED (do not remove from loadout/demo data dirs)
- [ ] V2 ADDED alongside V1
- [ ] § 2.2 explicit on preservation

### 4.3 V1-fix-deferral bug surface verification scope
- [ ] § 2.3 lists 3 P1-surfaced bugs (is_act_boss null; resolveElementDisplay null-guard; SeasonManifest elements non-optional)
- [ ] Drax asked to verify (persist / side-fixed / new behavior) — not pre-fix unless trivially blocking

### 4.4 LOCK G Vercel deploy discipline
- [ ] Vercel preview update named (V2 selectable in UI)
- [ ] LOCK G autonomous

### 4.5 LOCK J § 1 additive type discipline
- [ ] Type additions additive only (if any V2-specific fields)
- [ ] No removal / semantic changes

### 4.6 KR-cumulative-pattern-surface watch
- [ ] Dispatch does NOT pre-decide V1 vs V2 comparison observations (drax surfaces)
- [ ] Dispatch does NOT pre-decide whether bugs persist or side-fixed (drax verifies)
- [ ] Drax seam authority preserved

### 4.7 Anti-patterns
- [ ] No new UI / no redesign per LOCK F
- [ ] No conflation with post-immediate-arc Pattern B (separate Matt-touchpoint)
- [ ] No premature unblocking of long-arc

---

## 5. Gate-1 verdict format

Author finding at `agentic_orchestration/qa/findings/2026-06-01-ia-3-phase-4-gate-1.md`:

- **Verdict:** INFO / WARN / BLOCK
- **LOCK F MVP-discipline:** PASS / FAIL (CRITICAL)
- **V1 preservation:** PASS / FAIL
- **Bug surface verification scope:** PASS / FAIL
- **Final classification:** PASS / PASS-with-INFO / BLOCK

If PASS / PASS-with-INFO: KR fires drax IA-3 P4 immediately (background).
If BLOCK: KR remediates; re-Gate-1.

---

## 6. Cross-seam contract change? (Principle 6)

**Answer:** not applicable — Gate-1 review authors critique-pair finding.

---

## 7. Acceptance criteria

- [ ] IA-3 P4 dispatch reviewed
- [ ] Gate-1 finding authored
- [ ] Verdict + remediation guidance (if applicable)
- [ ] Completion record appended

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**Verdict:** INFO / WARN / BLOCK
**Final classification:** PASS / PASS-with-INFO / BLOCK
**Finding artifact:** agentic_orchestration/qa/findings/2026-06-01-ia-3-phase-4-gate-1.md
**LOCK F MVP-discipline:** PASS / FAIL
**V1 preservation:** PASS / FAIL
**Bug surface verification scope:** PASS / FAIL
**Key items surfaced:** brief
**Routing back to KR:** fire drax IA-3 P4 / remediate first / hold
```

---

**End of jack-ryan IA-3 P4 Gate-1 dispatch.**
