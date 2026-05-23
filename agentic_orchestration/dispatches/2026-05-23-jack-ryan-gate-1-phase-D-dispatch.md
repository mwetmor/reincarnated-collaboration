# Dispatch — 2026-05-23 — jack-ryan — Gate-1 review of Phase D cleaning-pipeline dispatch

**From:** knight-rider
**To:** jack-ryan (DESIGN-MODE; Gate-1 critique pair)
**Approved by:** Matt 2026-05-23 (chose option (b) defer Gate-1 to Pattern-B separate session after Pattern-A attempt hit credit-ceiling)
**Estimated effort:** ~30-45 min (single Pattern-B session)
**Acceptance:** PASS / PASS-WITH-AMENDMENTS / BLOCK judgment with concrete reasoning per the 10 stress-test angles below; output committed back to this dispatch as completion record

---

## Context

Knight-rider attempted to fire you Pattern-A in the active orchestration session, but the call returned `Usage credits are required for long context requests` — credit ceiling exceeded due to accumulated session context plus the 367-line Phase D dispatch. Matt chose option (b): defer Gate-1 to a separate Pattern-B session (this one) with its own credit budget.

You are reviewing the elrond Phase D cleaning-pipeline dispatch BEFORE it fires to elrond. Phase D is the load-bearing execution work of the entire weapon-library-cleaning campaign — schema migration + 7-step cleaning pipeline + acceptance gate verification across 89,839 substrate rows.

## What to review

`agentic_orchestration/dispatches/2026-05-23-elrond-phase-D-cleaning-pipeline.md` (367 lines)

## Background context (lightweight read)

- Cycle 9 of weapon-library-import campaign. Substrate at 89,839 clean entries / 24 sources / DB 136 MB.
- Phase A (legolas) + Phase B (gandalf) + Phase B-2 (gandalf variant-cluster policy) + Phase C (Matt F1-F6 + G1-G5) all locked.
- This Phase D dispatch operationalizes all upstream decisions; it does not open new design space.
- Cross-seam: schema changes touch the DB at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (loadout-repo-owned; gitignored). ADR-004 MIGRATION.md required.

## Recommended supporting reads (skim, not full)

- `canonical/story/cleaning-policy-design-2026-05-22.md` § 4 (math-anchored thresholds — verify dispatch encodes them exactly)
- `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` (gandalf's 26-cluster policy table — verify dispatch references the policy assignments correctly)
- `agentic_orchestration/CHANGELOG.md` (top 3 entries: Cycle 9.2, 9.3, 9.4 — chronology)
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` § Cycle 9.3 (Phase A empirical baselines that Phase D must respect)

## What I want from you (10 stress-test angles)

1. **Math-before-code completeness.** Discipline #1. The dispatch requires a math note with 5 components (schema migration plan / per-step row-impact estimates / acceptance gate verification queries / idempotency guarantees / rollback plan). Is this sufficient for a 7-step DB-modification pipeline, or is something missing?

2. **Cross-seam contract handling.** ADR-004. The dispatch requires MIGRATION.md but acknowledges the loadout-repo-owned DB. Is the cross-seam analysis sufficient? Should drax be notified explicitly? Is the "verify no current consumers" requirement adequate, or does it need explicit drax-side investigation?

3. **Acceptance criteria measurability.** 10 criteria total + 4 overall acceptance gates. Are each measurable from artifacts elrond produces? The 4 gates have explicit verification methods specified — are those verification methods correct/sufficient?

4. **Sequencing dependencies.** Steps 1-7 have a stated priority order. Are there any hidden cross-step dependencies that would cause a step to fail if prior steps weren't yet executed? E.g., does Step 7 (F4 merge) actually need Step 1 (ammo tagging) to have completed, or could they run in parallel?

5. **Idempotency claims.** The dispatch asks elrond to make each step idempotent (re-runnable). Is this actually achievable for all 7 steps, or are there steps where idempotency is hard (e.g., Step 7 fuzzy merge might be sensitive to row-order)?

6. **Acceptance gate threshold consistency with gandalf's § 4.** The dispatch claims to enforce gandalf's math-anchored cleanliness bars. Spot-check that the thresholds in the dispatch match gandalf's design doc exactly (FP ≤3%/1.5%; duplication ≤4% residual / ≥92% recall; weapon_kind misclass ≤2%/5%/1%; field coverage already-met-verify-no-degradation).

7. **G1-G5 operational hooks.** The dispatch attempts to operationalize Matt's G1-G5 leans. Are all 5 hooks present + actionable? Anywhere they're missing or vague?

8. **Round-trip smoke specification.** The dispatch specifies a 10-row-per-source fixture for round-trip smoke. Is this sufficient given 24 source libraries (would yield 240 rows)? Or does it need stratification refinement?

9. **Out-of-scope completeness.** The "DO NOT" list — is it complete? What's NOT in the dispatch that elrond might be tempted to do?

10. **Pattern A vs Pattern B.** This is a Pattern-B-by-nature dispatch (3-5 day execution). Confirm Pattern B is correct and Pattern A would not work even in degraded mode.

## Output format

Append a completion record to THIS dispatch file with structure:

**JUDGMENT:** BLOCK | PASS | PASS-WITH-AMENDMENTS

**Critical issues (if BLOCK):** numbered list with specific paths to amend
**Amendments (if PASS-WITH-AMENDMENTS):** numbered list with specific text changes or additions
**Confirmation (if PASS):** one paragraph stating what passed and why

## Acceptance criteria

- [ ] All 10 stress-test angles addressed (judgment per angle even if "no issues found")
- [ ] Concrete amendments specified if PASS-WITH-AMENDMENTS (line numbers / section references in Phase D dispatch)
- [ ] Output committed as completion record appended to this dispatch file
- [ ] Round-trip: not applicable — Gate-1 critique only; no contract change
- [ ] Tag: `jack-ryan/gate-1-phase-D-2026-05-23`

## Out of scope (explicit non-goals)

- **DO NOT** execute the Phase D dispatch (that's elrond's job after Gate-1 passes)
- **DO NOT** modify gandalf's policy docs or legolas's audit deliverables
- **DO NOT** apply amendments to the Phase D dispatch yourself — surface them; knight-rider applies before firing elrond
- **DO NOT** open new design space — F1-F6 + G1-G5 are Matt-locked; gandalf's math-anchored bars are locked; your job is to stress-test the operational dispatch, not the upstream design

## References

- `agentic_orchestration/dispatches/2026-05-23-elrond-phase-D-cleaning-pipeline.md` — the dispatch under review
- `canonical/story/cleaning-policy-design-2026-05-22.md` — gandalf Phase B policy framework
- `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` — gandalf 26-cluster policy
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` — Cycle 9.4 live state
- `agentic_orchestration/CHANGELOG.md` — chronology (top 4 entries: Cycles 9.1-9.4)
- ADR-004 (cross-seam handoff via MIGRATION.md); ADR-006 (read-only by default)
- Discipline #1 (math-before-code); Discipline #11 (audit-preservation); Discipline #19 (right tool / smoke-test)

---

## What happens after you return

Knight-rider:
1. Reads your completion record
2. Applies any PASS-WITH-AMENDMENTS amendments to the Phase D dispatch
3. Updates state file + CHANGELOG with Gate-1 disposition
4. Surfaces to Matt: Phase D dispatch is Gate-1-approved and ready to fire elrond Pattern-B
5. Matt fires elrond Pattern-B in his own terminal session (separate from this one)

---

**Signed:** knight-rider (dispatch authored 2026-05-23 ~01:00 EDT; jack-ryan Gate-1 queued for next Pattern-B session)

---

## Gate-1 Completion Record — jack-ryan

**Reviewer:** jack-ryan
**Date:** 2026-05-23
**Judgment:** PASS-WITH-AMENDMENTS
**Tag to issue:** `jack-ryan/gate-1-phase-D-2026-05-23`

---

### 10-angle stress-test findings

**Angle 1 — Math-before-code completeness (Discipline #1)**
The 5-component math note requirement is structurally adequate. However, the 7 Open Questions in the dispatch are engineering-critical (especially Q1 idempotency per-step, Q2 VACUUM strategy, Q3 backup strategy, Q5 embedding model choice) and are not currently referenced inside the math note required-content block. Elrond could author a compliant 5-component math note while deferring the open questions. **Amendment required** (see Amendment 5 below).

**Angle 2 — Cross-seam contract handling (ADR-004)**
Coverage is adequate. MIGRATION.md is required; the dispatch specifies that elrond must verify (not assume) no current consumers before declaring not-applicable. The explicit check instruction ("grep/search the loadout repo for queries referencing `weapon_knowledge_entries`") is implicit in the requirement but not spelled out. The "DO NOT modify the loadout web app code (drax's seam)" clause covers the boundary. No BLOCK.

**Angle 3 — Acceptance criteria measurability**
Nine of the 10 acceptance criteria and all 4 overall gates are measurable from artifacts elrond produces. One gap: **Gate (b) specifies dedup residual-duplication check (≤4%) but does not specify the dedup recall verification (≥92%).** Recall requires a denominator — the raw duplicate count from legolas's baseline (89,839 rows / 47,586 distinct canonical_names → 42,253 duplicate rows). Without a specified verification method for the recall half of gate (b), elrond may only verify residual duplication and not recall. **Amendment required** (see Amendment 2 below).

**Angle 4 — Sequencing dependencies**
A hidden dependency exists. **Step 7 blocks on `(weapon_subclass, cultural_lineage_canonical)` to reduce comparison space from 89K² to per-bucket-N². But `cultural_lineage_canonical` defaults to 'unknown' and none of Steps 1–6 populates it.** If Step 7 fires with all rows at 'unknown', the blocking strategy collapses to a single bucket of 89K rows — the O(N²) reduction fails entirely, and the merge becomes computationally infeasible. Gandalf's § 4.38 explicitly states: "Phase D's main field-coverage work is NOT raw imputation but canonical normalization — i.e., mapping the raw `cultural_lineage_tags` string vocabulary into the canonical § 5 taxonomy. That mapping work IS load-bearing." A canonical-normalization substep is missing. **Amendment required** (see Amendment 1 below — this is the most critical amendment).

**Angle 5 — Idempotency claims**
Steps 1–6 are naturally idempotent (set-classification-if-condition is a no-op on repeat). Step 7 idempotency is correctly flagged as Open Question Q1 and deferred to elrond's math note. Step 3 archive idempotency (dump-then-archive for quarantine) needs a guard for the case where the archive file already exists. This is captured adequately via the open questions framework. No additional amendment needed; acceptable as-is.

**Angle 6 — Threshold consistency with gandalf § 4**
All thresholds match exactly:
- Gate (a): ≤ 3.0% hard / ≤ 1.5% target ✓
- Gate (b): ≤ 4.0% residual / ≥ 92% recall ✓
- Gate (c): ≥ 95% structured / ≥ 85% description / ≥ 70% cultural / ≥ 60% period ✓
- Gate (d): category↔unique ≤ 2%; category↔named_template ≤ 5%; category↔ammo ≤ 1% ✓

Step 7 acceptance uses "47% × 0.08 = 3.76%" derivation — consistent with recall-framing of the same threshold. No issues.

**Angle 7 — G1-G5 operational hooks**
All 5 present and actionable:
- G1 (WIKI-3 Gladius game-tier): Step 4, per-game named_template retention. ✓
- G2 (SOULS-1 Dagger soulslikes): Step 7, flag borderline 0.80–0.85 cases for Matt+gandalf. ✓
- G3 (AOS-2 Skull Bludgeon compound): Step 4, split into 2 children + retain compound. ✓
- G4 (RA-2 grouping threshold): Step 2, ≥3 specimens per (culture × century × broad_type). ✓
- G5 (WIKI-2 OSRS Excalibur): Step 4, keep separate as named_template. ✓

**Angle 8 — Round-trip smoke specification**
10 rows × 24 sources = 240-row fixture is adequate for structural smoke (new columns populated, view returns correctly). However, the smoke test as specified does not cover algorithmic correctness of Step 7: no known-merge pair is required in the fixture, so Step 7 could produce zero merges on the smoke data and pass. **Minor amendment** (see Amendment 3 below).

**Angle 9 — Out-of-scope completeness**
The DO NOT list covers 8 items. One gap: gandalf § 4.38 says Phase D is "NOT raw imputation" and "NOT field enrichment" — but this is stated only in the Context section, not in the explicit DO NOT list. Elrond may be tempted to backfill `description_text` for missing rows or impute `cultural_lineage_tags`. **Minor amendment** (see Amendment 4 below).

**Angle 10 — Pattern A vs Pattern B**
Pattern B is correct. Pattern A would fail because: (1) required reading alone is 828-line gandalf policy + 6 legolas audit files; (2) the 7-step pipeline execution with intermediate verification against a 136 MB database is multi-day; (3) the acceptance gates require empirical re-sampling of ~50 rows × 24 sources, generating context that exceeds a single session. Even degraded Pattern A is not viable.

---

### Amendments (knight-rider applies to Phase D dispatch before firing elrond)

**Amendment 1 — REQUIRED (Critical): Add canonical-normalization substep before Step 7**

Between Step 6 and Step 7, add a new **Step 6.5 — Canonical taxonomy normalization (`cultural_lineage_canonical`, `historical_period_canonical`, `register_canonical`)**:

> **Step 6.5 — Canonical taxonomy normalization**
>
> **Why:** Step 7 blocks on `(weapon_subclass, cultural_lineage_canonical)` to reduce comparison space from 89K² to per-bucket-N². Without `cultural_lineage_canonical` populated, all rows sit in a single 'unknown' block — blocking fails and Step 7 becomes computationally infeasible.
>
> **Per gandalf § 5 + per-source mapping table (§ 5.1):**
> Apply the 24-source mapping rules to populate `cultural_lineage_canonical` from `cultural_lineage_tags`. Apply `historical_period_canonical` from `historical_period` free-text using gandalf's § 5.2 period mapping. Apply `register_canonical` from source-library heuristic (museum/wikidata → 'historical'; game-source → 'fantasy'/'sci_fi'; OSRS named-unique → 'mythological').
>
> Set `cultural_lineage_confidence` per gandalf § 5: 1.0 (explicit structured-tag match) / 0.7 (description-regex match) / 0.5 (source-library default) / 0.3 (fallback heuristic).
>
> **Acceptance:** ≥ 70% of `v_category_sample` rows have `cultural_lineage_canonical ≠ 'unknown'` (per gandalf § 4.4 field-coverage floor, applied to the canonical column not the raw tag).

**Amendment 2 — REQUIRED: Specify dedup recall verification in Gate (b)**

In the overall acceptance gates table, Gate (b) verification column currently reads: "Post-Step-7 count of canonical rows vs distinct canonical_names."

Replace with:

> **Gate (b) dual verification:**
> (i) Residual duplication: count rows with `dedup_status='canonical'`; count distinct `canonical_name` across those rows; compute `(canonical_count / distinct_canonical_names) - 1`; must be ≤ 0.04.
> (ii) Dedup recall: raw duplicate baseline = 42,253 rows (89,839 total − 47,586 distinct names per legolas Phase A). Post-merge merged rows = count where `dedup_status='merged_into'`. Recall = merged_rows / 42,253; must be ≥ 0.92.

**Amendment 3 — Minor: Extend round-trip smoke to include merge-pair fixtures**

In the round-trip smoke requirement, add after "10-row-per-source fixture":

> Additionally include: ≥ 2 known-merge pairs (same entity across 2 source libraries; validated from legolas's named-unique verification — e.g., `Excalibur` in wikipedia vs wikidata) and ≥ 2 known-non-merge pairs (brand-prefix disambiguation cases — e.g., `Excalibur` mythological sword vs `M982 Excalibur` artillery shell). Step 7 must produce correct `dedup_status` on these fixture rows.

**Amendment 4 — Minor: Add field-enrichment prohibition to DO NOT list**

Append to the "Out of scope" DO NOT list:

> - **DO NOT** do field enrichment — do NOT backfill `description_text` for rows missing it, do NOT impute `cultural_lineage_tags`, do NOT add new source rows. Phase D is dedup + classification + normalization of existing rows only (per Context section and gandalf § 4.38).

**Amendment 5 — Minor: Link Open Questions to math note required content**

In the Math-before-code section, add after the 5-component list:

> Additionally, the 7 Open Questions listed in § Open Questions must be resolved and documented within the math note before pipeline code fires. They are not optional annexes — they are engineering decisions required for correct pipeline execution (especially Q1 idempotency, Q2 VACUUM, Q3 backup, Q5 embedding model).

---

### Summary

The Phase D dispatch is well-structured, threshold-accurate, and G1-G5 complete. The one architectural gap (Amendment 1) is load-bearing: without `cultural_lineage_canonical` populated before Step 7, the blocking strategy fails silently and the merge becomes computationally infeasible on 89K rows. This must be fixed before firing elrond.

Amendments 2-5 are correctness and clarity improvements; none are architectural blockers on their own. All 5 amendments are targeted and do not require redesign of any upstream locked decision.

**JUDGMENT: PASS-WITH-AMENDMENTS**

**Signed:** jack-ryan (Gate-1 review complete 2026-05-23; tag: `jack-ryan/gate-1-phase-D-2026-05-23`)
