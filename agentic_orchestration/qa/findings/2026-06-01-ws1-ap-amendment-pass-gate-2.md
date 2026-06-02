# Finding — 2026-06-01 — WS1.AP Amendment-Pass (Cardinality Correction) — Gate-2

**Reviewer:** jack-ryan
**Severity:** WARN (PASS-with-WARN)
**Target:** meta-repo `98b315d` + engine-repo `cda99a5`
**Developer:** gandalf (story-and-design steward)
**Principles applied:** 1 (math-before-code), 4 (decisions-log truth), 5 (severity matters)
**Authority:** Matt 2026-06-01 wave directive + jack-ryan WS1 Gate-2 PASS-with-WARN (ADR-002 direct-approval for documentation-only)

---

## Verdict: PASS-with-WARN

**Final classification:** PASS-with-WARN

WS1.AP closes with one explicit follow-on amendment item required before WS1A.3/4 fire. See § 7.1 below.

---

## § 3.1 Cardinality correction verification

### PG-3 ratification (Loc 1) — PASS

- § 1.9: corrected to "109 entries locked... (100 rotating + 9 physical)". PASS.
- § 5 lineage aggregate: corrected to 57/23/19/1/9=109. PASS.
- § 7 migration scope: corrected to "100 rotating-primary entry migration". PASS.
- § 9 sign-off: corrected to "109 entries committed". PASS.
- § 10 amendment-pass-record: appended with correct rationale. PASS.

### Canonical lock (Loc 2) — PASS (with § 7.1 exception — see below)

- § 0 TL;DR: "109 entries / 100 rotating". PASS.
- § 1 Architecture A definition: "7 rotating primaries ... 100 total". PASS.
- § 2.9 cardinality table: TOTAL = 109. PASS.
- § 3.3 stormtide annotation: present per dispatch § 3.3 suggested language. PASS.
- § 6.2 migration scope: "100 rotating-primary". PASS.
- § 7 lineage-tag table: aggregate row = 57/23/19/1/9=109. PASS.
- § 7.1 closing parenthetical: "100 rotating + 9 physical = 109". PASS.
- § 8.1 operational-application count: "23 entries". PASS.
- § 9.2 downstream authorization: "109 entries". PASS.
- § 10 sign-off: "109 entries committed". PASS.
- § 0.1 amendment-pass-record: present, complete, rationale correct. PASS.

**§ 7.1 exception — see § Surface 2 verdict below (FAIL on accuracy; REQUEST further amendment).**

### Wave-close record (Loc 3) — PASS

- § 0 TL;DR: "109 entries". PASS.
- § 1 Phase 5b row: "109 entries committed". PASS.
- § 2 Headline outputs: "109 entries". PASS.
- § 5 deferral list: "100 rotating-primary entry migration". PASS.
- § 5 lineage-tag reconciliation note: "57/23/19/1/9=109". PASS.
- § 7 Authority chain: "109 entries". PASS.
- § 0.1 amendment-pass-record: new row appended with correct rationale. PASS.

### Decisions-log (Loc 4) — PASS

Decision title reads "109 entries total". AMENDED 2026-06-01 annotation present under the Decision body; wording correction applied ("100 entries rotating subtotal / 109 entries total"). Architectural commitment (Architecture A LOCKED) UNCHANGED throughout. PASS.

### Engineering-disciplines.md (Loc 5) — PASS

- § Scope-note 2026-06-01: founding count corrected to 23 entries with amendment-pass note. PASS.
- § 49 founding instance (line 2371): "23 entries" with correction note. PASS.
- § Disciplines lineage (line 2643): "23 founding entries" / "57 substrate-validated entries" corrected. PASS.
- No "118 entries" wording found in this doc. PASS.

### elements.yaml (Loc 6) — PASS (NO-OP)

Spot-check confirmed: no cardinality reference present. NO-OP correctly identified. PASS.

### Ground-state oracle + roadmap (out-of-explicit-scope — see Surface 1) — PASS

Both corrected; assessed under Surface 1 verdict.

**Cardinality correction verification overall: PASS (subject to § 7.1 follow-on amendment per Surface 2 WARN)**

---

## § 3.2 Surface 1 — Out-of-explicit-scope consistency amendments

**Verdict: RATIFY**

`canonical/00-ground-state.md` oracle row (line 101, WS1A.Q18 entry): corrected to "100 entries; corrected at 2026-06-01 amendment-pass" / "109 entries total". Inline correction note included. Internally consistent with canonical lock. RATIFIED.

`canonical/02-roadmap.md` Q18 row (line 571) + Sub-phase 5f row (line 575): corrected to "109 entries... (100 rotating + 9 physical)". Inline correction note included. Rationale is sound — oracle + roadmap are consumed at every canonical-doc lookup; leaving stale wording would propagate the editorial error into WS1A.3/Q16/Q17/Q19 wave-open dispatches.

These amendments fall within dispatch § 3.1 item 6 ("any architecture-A documentation") and are consistent with Principle 4 (decisions-log and canonical-doc truth). They reduce downstream propagation risk. RATIFY. Architectural intent UNCHANGED.

---

## § 3.3 Surface 2 — § 7.1 column-header readability

**Verdict: REQUEST (follow-on amendment required before WS1A.3/4 fire)**

This is not purely a readability question. Independent arithmetic confirms a label-cell inversion:

| Column header | Per-row cell sum (as authored) | Pool.json ground truth |
|---|---:|---:|
| substrate-silent | 19 | 23 |
| designer-curation-modern-scientific | 23 | 19 |

Pool.json verification: `substrate-silent-2026-05-08-D1-pool`=23, `designer-curation-modern-scientific-overlay-2026-06-01`=19. The per-row cells in § 7.1 have these two columns inverted relative to the ground truth tags applied at migration. Gandalf's correction of the TOTAL row to "57/19/23/1/9" preserved the inversion — the correct TOTAL row should be "57/23/19/1/9".

**Consequence:** any downstream consumer reading § 7.1 to audit per-primary substrate-silent vs modern-scientific distribution will receive inverted counts. This is a factual accuracy issue, not a cosmetic readability issue.

**Required action (gandalf):** correct § 7.1 per one of two paths:

- **Path A (PREFERRED):** swap the column headers so they match the per-row cells as authored (relabel "substrate-silent" → "designer-curation-modern-scientific" and vice versa). Total row then reads 57/19/23/1/9 under the relabeled headers, which correctly associates each per-primary count with its applied tag. Add amendment-pass-record entry.

- **Path B:** re-author the per-row cells to reflect the correct per-primary distribution per pool.json, then correct the total row to 57/23/19/1/9. This requires auditing per-primary silent vs modern-sci tag counts from pool.json directly — more involved but produces a fully auditable table.

Either path resolves the inversion. Path A is lower-risk (per-row cells were authored under some consistent labeling logic; swapping headers preserves that logic).

**Blocking impact:** this follow-on amendment is REQUIRED before WS1A.3/4 fire — those workstreams will read § 7.1 to understand per-primary tag distributions. Inverted labels would produce incorrect upstream assumptions. Does NOT block WS1.AP formal close; WS1.AP closes PASS-with-WARN with this follow-on item noted.

Cite: Principle 1 (math-before-code — downstream consumers must read correct counts), Discipline #49 (substrate-silence ≠ substrate-validation — the discipline's founding-instance count must be accurately traceable per-primary).

---

## § 3.4 Surface 3 — Decisions-log amendment format

**Verdict: RATIFY Option A**

Option A (inline "AMENDED 2026-06-01" dated annotation under the Decision body) correctly applies the append-only temporal log discipline per `decision-log-format` skill § 5. The annotation preserves the original architectural commitment record, makes the editorial correction transparent, cross-references the Gate-2 finding + amendment-pass dispatch + companion doc amendments, and explicitly states that the architectural commitment (Architecture A LOCKED) is unchanged. Format is appropriate for editorial correction within an immutable entry. RATIFIED.

---

## § 3.5 Lineage tag aggregate (Ambiguity 2 verification)

Corrected aggregate per my WS1 Gate-2 ratification: 57 substrate-validated / 23 substrate-silent / 19 modern-scientific / 1 mystical-fantasy / 9 architecture-A-registry = 109.

- PG-3 § 5: reads 57/23/19/1/9=109. CONSISTENT.
- Canonical lock § 7 table aggregate row: reads 57/23/19/1/9=109. CONSISTENT.
- Pool.json ground truth: 57/23/19/1/9 (100 lock entries + 114 legacy). CONSISTENT.

Note: canonical lock § 7.1 TOTAL row reads 57/19/23/1/9 (inverted) — this is the inversion addressed under Surface 2 above.

---

## § 3.6 Stormtide annotation (Ambiguity 3 verification)

Canonical lock § 3.3 wind section: annotation present per dispatch § 3.3 suggested language: "stormtide is preserved as routing intent in the migration script (wind primary) but is not in the locked allow-list per PG-3 ratification." Wording: routing intent preserved; not in locked allow-list; future promotion criteria stated. PASS.

---

## § 3.7 Amendment-pass-record protocol verification

- Canonical lock § 0.1: amendment-pass-record table present; original wording described in Reason cell; corrections applied to main body. PASS.
- PG-3 § 10: new amendment-pass-record section appended. PASS.
- Wave-close record § 0.1: new row appended to amendment-pass-record. PASS.
- Decisions-log: inline "AMENDED 2026-06-01" annotation (Option A per Surface 3 RATIFY). PASS.
- Engineering-disciplines: inline amendment notes within scope-note + founding-instance + disciplines-lineage sections. PASS.

---

## § 3.8 Architectural intent UNCHANGED — PASS (CRITICAL)

Verified across all 8 amended doc locations:

- **Architecture A LOCKED**: unchanged in canonical lock § 0 / PG-3 § 0 / decisions-log. PASS.
- **Q18.a-e structural commitments**: unchanged — 8-primary scope / vote-grounded research / flex_slots preserved / d1_status filter / per-primary cardinality all intact. PASS.
- **Per-primary verbatim entry lists**: unchanged — 16/14/18/13/13/14/12=100 rotating + 9 physical confirmed entry-by-entry against pool.json. PASS.
- **Cull-tag dispositions**: unchanged in canonical lock § 5. PASS.
- **Discipline #49 / #50 / #51 substance**: count correction in #49 founding-instance text (24→23) is factually correct per pool.json; discipline rationale + scope unchanged. PASS.
- **Documentation-only editorial correction confirmed throughout**: no engine substrate / schema / pool.json content / telemetry / loadout modified. PASS.

All amendments are wording-only cardinality corrections. The lock itself — Architecture A, per-primary allow-lists, cull-tag dispositions, Q18.a-e commitments — is intact.

---

## Summary

| Check | Result |
|---|---|
| Cardinality correction verification (8 doc locations) | PASS (§ 7.1 exception → WARN) |
| Consistency amendments surface 1 (ground-state + roadmap) | RATIFY |
| § 7.1 readability surface 2 | REQUEST — follow-on amendment required |
| Decisions-log format surface 3 (Option A) | RATIFY |
| Lineage aggregate Ambiguity 2 (§ 3.5) | PASS |
| Stormtide annotation Ambiguity 3 (§ 3.6) | PASS |
| Amendment-pass-record protocol (§ 3.7) | PASS |
| Architectural intent UNCHANGED (§ 3.8 — CRITICAL) | PASS |

---

## Action items

- [ ] **Gandalf:** Follow-on amendment on canonical lock § 7.1 — correct label-cell inversion (Path A: swap column headers to match per-row cells; or Path B: re-author per-row cells to match correct headers). Add amendment-pass-record entry. Required before WS1A.3/4 fire.
- [ ] **KR:** WS1.AP CLOSED PASS-with-WARN. Route WS1A.3/4 unblocked subject to (1) § 7.1 follow-on amendment COMPLETE + (2) vfx_coverage_manifest prerequisite per original WS1 Gate-2 forward note.
- [ ] **KR:** Q16/Q17/Q19 unblocking is unchanged — not dependent on § 7.1 follow-on amendment.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` — reviewed (8 amended locations)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md` — reviewed
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md` — reviewed
- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` (2026-06-01 entry) — reviewed
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (§ scope-note + § 49 + § lineage) — reviewed
- `/Users/admin/Games/reincarnated-collaboration/canonical/00-ground-state.md` (line 101) — reviewed
- `/Users/admin/Games/reincarnated-collaboration/canonical/02-roadmap.md` (lines 571 + 575) — reviewed
- `/Users/admin/Games/reincarnated-engine/data/seasonal_elements/pool.json` — ground-truth verification (214 entries; 100 lock cohort; lineage distribution 57/23/19/1 confirmed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-06-01-ws1-sub-phase-5f-gate-2.md` — binding scope source (WS1 Gate-2 PASS-with-WARN)

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**For:** Gate-2 DEV-MODE review of WS1.AP gandalf amendment-pass (cardinality correction + lineage aggregate + stormtide annotation). Documentation-only scope per ADR-002 direct-approval authority.
