# Dispatch — 2026-06-01 — gandalf — WS1.AP-FU: § 7.1 column-header label-cell inversion fix

**From:** knight-rider (post-wave orchestrator)
**To:** gandalf (canonical-doc steward) → jack-ryan Gate-2 approves
**Approved by:** jack-ryan WS1.AP Gate-2 finding (PASS-with-WARN; Path A explicit recommendation for column-header swap)
**Workstream tag:** `WS1A.Q18-amendment-pass-FU-section-7.1`
**Phase / phase-gate:** WS1.AP-FU (follow-on to WS1.AP; closes the WS1A.Q18 amendment chain)
**Estimated effort:** ~10 minutes (Path A column-header swap + amendment-pass-record entry)
**Acceptance:** § 7.1 column-header labels corrected + amendment-pass-record entry + jack-ryan Gate-2 approval

---

## 1. Context

WS1.AP Gate-2 closed PASS-with-WARN. Jack-ryan independent verification surfaced that canonical lock § 7.1 is NOT a readability sub-surface (as initially deferred to readability decision) — it's a label-cell inversion bug.

**The bug:**
- Column labeled "substrate-silent" has per-row cells summing to 19 (= actual modern-scientific count per pool.json)
- Column labeled "designer-curation-modern-scientific" has per-row cells summing to 23 (= actual substrate-silent count per pool.json)
- The previous amendment-pass corrected the TOTAL row to "57/19/23/1/9" — but per pool.json ground truth, the correct totals are "57/23/19/1/9"
- The per-row cells are TRUE (matching pool.json per-primary tag counts); the COLUMN HEADERS are SWAPPED

**Path A fix (jack-ryan recommendation; lower-risk):** swap the two column headers labeled "substrate-silent" and "designer-curation-modern-scientific" in § 7.1. The per-row cells become correctly labeled; total row corrects to "57/23/19/1/9" matching pool.json arithmetic.

---

## 2. Authoritative reading

1. **THE doc under amendment:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 7.1
2. **Jack-ryan WS1.AP Gate-2 finding (binding source):** `agentic_orchestration/qa/findings/2026-06-01-ws1-ap-amendment-pass-gate-2.md`
3. **Migrated pool.json (ground truth for per-primary tag counts):** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json`
4. **Workstream queue:** `agentic_orchestration/post-q18-workstream-queue-2026-06-01.md`
5. **canonical-doc-format skill** (amendment-pass-record protocol)

---

## 3. Scope

### 3.1 Path A — column header swap

In canonical lock § 7.1 lineage-tag distribution table:
- Swap column header label `substrate-silent` ↔ `designer-curation-modern-scientific`
- Per-row cells remain unchanged (they're correct against pool.json per-primary tag counts)
- Total row after swap reads: 57/23/19/1/9 = 100 rotating + 9 physical = 109 (matches pool.json arithmetic)
- Update any cross-references in § 7.1 closer or adjacent paragraphs to reflect corrected column ordering

### 3.2 Amendment-pass-record entry

Append entry to canonical lock § 0.1 amendment-pass-record:

| Date | Author | Amendment | Reason |
|---|---|---|---|
| 2026-06-01 | gandalf | § 7.1 column header swap (`substrate-silent` ↔ `designer-curation-modern-scientific`) per WS1.AP Gate-2 PASS-with-WARN follow-on (Path A) | Label-cell inversion bug: per-row cells matched pool.json ground truth but column headers were swapped; total row correction propagated the inversion in the prior amendment-pass. Path A swap preserves per-row cell accuracy + corrects column labels + corrects total row to 57/23/19/1/9. |

### 3.3 Cross-reference verification

After swap, verify:
- § 7 lineage-tag aggregate (table) cross-references § 7.1 correctly
- Any prose surrounding § 7.1 that names specific column counts is consistent
- PG-3 § 5 aggregate (already corrected at WS1.AP to 57/23/19/1/9=109) remains consistent
- Wave-close record § 5 lineage-tag reconciliation note remains consistent

---

## 4. Authoring discipline

- Path A swap is editorial documentation-only; no architectural intent change
- Architecture A LOCKED unchanged; per-primary verbatim entry lists unchanged; lineage aggregates unchanged (the 57/23/19/1/9 distribution is the AS-MIGRATED ground truth)
- Single commit recommended

---

## 5. Decision authority

Per jack-ryan WS1.AP Gate-2: Path A is the explicit recommendation. Per ADR-002 direct-approval authority on documentation-only changes: amendment-pass-FU authorship is gandalf seam authority; jack-ryan approves at Gate-2.

If you observe the label-cell inversion is non-trivial to fix via Path A (e.g., per-row cells DON'T match pool.json upon detailed audit; the actual ground truth differs from what jack-ryan asserted), surface to KR via report-back — do NOT silently adopt Path B (re-author per-row cells) without ratification.

---

## 6. Acceptance criteria

- [ ] § 7.1 column headers swapped (Path A)
- [ ] Per-row cells verified against pool.json (no change needed if jack-ryan's arithmetic holds)
- [ ] Total row corrected to 57/23/19/1/9 = 100 rotating + 9 physical = 109
- [ ] Amendment-pass-record entry added to § 0.1 per § 3.2
- [ ] Cross-references verified per § 3.3
- [ ] Auto-commit per CLAUDE.md addendum 2026-05-25
- [ ] Completion record appended to dispatch

---

## 7. Cross-seam contract change? (Principle 6)

**Answer:** NOT applicable. Documentation-only editorial correction; no engine substrate / schema / pool.json content / telemetry / loadout modified.

---

## 8. Out of scope

- Re-authoring per-row cells (Path B) — surface to KR if Path A insufficient
- Re-architecting § 7.1 table — out-of-scope; minimal correction only
- Other amendment-pass items beyond § 7.1 (WS1.AP closed everything else)
- WS1A.3/4 prerequisites (vfx_coverage_manifest extension is separate workstream)

---

## 9. References

- **Jack-ryan WS1.AP Gate-2 finding (binding):** `agentic_orchestration/qa/findings/2026-06-01-ws1-ap-amendment-pass-gate-2.md`
- **Canonical lock under amendment:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 7.1
- **Pool.json ground truth:** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json`
- **Workstream queue:** `agentic_orchestration/post-q18-workstream-queue-2026-06-01.md`

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**§ 7.1 column header swap applied:** yes/no
**Per-row cells verified against pool.json:** yes (no change needed) / amended
**Total row corrected to 57/23/19/1/9:** yes
**Amendment-pass-record entry added:** yes
**Cross-references verified:** yes
**Commit:** path + commit
**Routing back to KR:** "proceed to jack-ryan Gate-2 minimal verification" / specific issue
```

After your completion, KR routes jack-ryan Gate-2 minimal verification. On Gate-2 PASS, WS1.AP-FU CLOSED and WS1A.Q18 amendment-pass chain fully resolved.

---

**End of WS1.AP-FU dispatch.**
