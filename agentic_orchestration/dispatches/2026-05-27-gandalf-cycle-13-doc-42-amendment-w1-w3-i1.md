# Dispatch — 2026-05-27 — gandalf — Cycle 13 Doc 42 Amendment (W1 + W3 + I1 per Gate-1 Verdict)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-27 — Cycle 13 framing brief § 4.1 KR autonomous + jack-ryan Wave 1 Gate-1 verdict PASS-with-WARN (commit `54bf1b8`) requesting 3 specific amendments + Matt verbatim "Resume Wave 0 → Wave 1 dispatch sequencing"
**Estimated effort:** 30-60 min (3 small amendments to doc 42 sections)
**Acceptance:** 3 amendments landed (W1 § 2 normalization claim + W3 § 1 SC-4 expansion citation + I1 § 9 W1.6 D9 clarification); tagged commit; unblocks rocket Wave 1 implementation dispatch authoring

## Context

Jack-ryan Wave 1 Gate-1 critique on doc 42 (commit `54bf1b8`; finding at `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-gate-1-doc-42-critique.md`) returned **PASS-with-WARN** with 3 amendments requested:

- **W1 (REQUIRED before rocket W1.2 schema implementation fires):** doc 42 § 2 claims affinity matrix "sums to 100% per slot already." Empirically FALSE — raw tier-weight sums range 190-255 per slot (not 100%). The correct interpretation (50/30/15/5 as relative weights normalized per § 9.2 step 2) is present but contradicted by the § 2 claim. Foreseeable rocket implementation error.

- **W3 (KR-elected to include in this amendment for cleaner canonical state):** SC-4 expansion research (`agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md`) not cited in doc 42 § 1 companion-docs list. Wave-1-informing 9-category verification result IS load-bearing for the Discipline #23 Q2 framing-audit; citation chain should be present.

- **I1 (small clarification):** W1.6 sub-wave table in § 9 erroneously includes D9 (element/mechanic-gating gear-affix trait surface) which § 8 text correctly defers to Wave 4. W1.6 = D8 ONLY per § 8 text. Minor inconsistency between table and text.

Jack-ryan explicit next-action for KR: "Route W1 to gandalf (doc 42 § 2 normalization claim amendment — minor rewrite); With W1 resolved, author rocket Wave 1 implementation dispatch."

This dispatch bundles W1 + W3 + I1 (small atomic gandalf amendment pass; quick turnaround).

## Required reading before starting

1. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-gate-1-doc-42-critique.md` (jack-ryan Gate-1 critique with W1+W2+W3+I1+I2 specifics)
2. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` (YOUR doc to amend; specifically § 1 + § 2 + § 9 W1.6 sub-wave table + § 9.2 step 2 affinity normalization spec)
3. `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` (legolas SC-4 expansion to cite per W3)
4. `agentic_orchestration/operating-procedures/gandalf.md` (canonical-doc-format authority)

## Math-before-code (canonical amendment; no code)

NOT applicable.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Doc 42 amendments are canonical-text refinements; no schema / fixture / boundary mutation.

## Scope

### W1 — § 2 affinity matrix normalization claim correction (REQUIRED)

- [ ] Amend doc 42 § 2 to remove or correct the claim that the affinity matrix "sums to 100% per slot already"
- [ ] State correctly: raw tier-weight sums vary per slot (190-255 range); the 50/30/15/5 weights are RELATIVE weights to be normalized per § 9.2 step 2 normalization procedure
- [ ] Cross-reference § 9.2 step 2 explicitly so rocket implementation knows to normalize
- [ ] Verify § 9.2 step 2 normalization spec is correct (this is the load-bearing implementation guidance; rocket uses this)

### W3 — § 1 SC-4 expansion citation (KR-elected)

- [ ] Add citation for `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` to § 1 companion-docs list
- [ ] Brief annotation: "legolas SC-4 expansion; 9-category architectural verification + 5th Scaling-interaction synergy candidate + Pattern 9+10 degenerate-state catalog candidates; Wave-1-informing for 9-category compose-check; Wave-2-informing for synergy taxonomy + degenerate-state extension; Wave-4-informing for sim degenerate-state detection methodology"

### I1 — § 9 W1.6 sub-wave table clarification

- [ ] Amend § 9 W1.6 sub-wave table to remove D9 (element/mechanic-gating gear-affix trait surface) reference
- [ ] Restate W1.6 = D8 ONLY (minimum-viable intrinsic trait pool implementation per Verdict D.1) — aligns with § 8 text which already correctly defers D9 to Wave 4
- [ ] Verify no other table/text inconsistency in W1.6 scope

### Acceptance criteria

- [ ] All 3 amendments (W1 + W3 + I1) landed in doc 42
- [ ] No regression in other doc 42 sections (do not amend beyond W1/W3/I1 scope)
- [ ] Tagged commit per gandalf convention: `gandalf: Cycle 13 doc 42 amendment — W1 § 2 normalization clarity + W3 § 1 SC-4 expansion citation + I1 § 9 W1.6 D9 clarification (per jack-ryan Gate-1 verdict 54bf1b8)`
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- W2 (prefix/suffix binary schema field as REQUIRED W1.2 deliverable) — per jack-ryan next-action sequence, W2 folds into rocket Wave 1 implementation dispatch (KR work post-amendment) NOT into doc 42 amendment
- I2 (Disciplines #27 / #31 / #32 absent from doc 42 § 11) — correct scope; jack-ryan INFO observation; Wave 2 dispatch will invoke; NOT doc 42 amendment
- Re-litigating doc 42 architectural commitments (amendments are surgical)
- Modifying doc 40 / doc 41 (separate canonical authority)
- Re-running Wave 0 work
- Production code modifications

## Open questions for the agent to resolve

- W1 amendment phrasing — your wording; aim for clarity that the 50/30/15/5 are relative weights NOT absolute percentages summing to 100; explicit reference to § 9.2 step 2 normalization
- W3 citation depth — brief annotation per scope above OR fuller compose-statement; recommend brief per atomic-amendment scope
- I1 verification — beyond W1.6 D9 fix, spot-check W1.7 + W1.8 tables for similar inconsistencies (within minutes; optional)

## References

- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-gate-1-doc-42-critique.md` (Gate-1 critique source)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` (YOUR doc; amendment target)
- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` (SC-4 expansion; W3 citation)
- `agentic_orchestration/operating-procedures/gandalf.md` (canonical authority)

---

**Cycle:** 13
**Wave:** 1 amendment (post-Gate-1 PASS-with-WARN)
**Gates:** rocket Wave 1 implementation dispatch authoring (KR fires post-amendment with W2 + I1 + I2 amendments folded into rocket dispatch)
**Priority:** P1 — small amendment; gates Wave 1 rocket implementation
