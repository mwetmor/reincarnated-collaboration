# DISPATCH — Gandalf Doc 51 Scope-Completeness Amendment Batch (§ 9 + § 10)

**Authored:** 2026-05-28 evening
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** gandalf (design seam; doc 51 canonical author)
**Pattern:** Pattern A (~30-45min; canonical amendment via Discipline #40 case (c) extension since doc 51 is LOAD-BEARING)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 evening D1+D2+D3+D4 RATIFICATION — doc 51 scope-completeness amendment batch

---

## 0. AUTHORITY + CONTEXT

**Matt finding:** rocket Phase 3a coordination signal "`skill.investment_points` must be set to 15" is vague on WHICH skills. Doc 51 § 6.3 defers numeric thresholds to gamora seam, but doesn't specify per-profile investment distribution rules. **Phase 4 multi-profile sweep needs distribution rules locked before it fires.**

**Phase 3d gamora HALTED** (TaskStop clean) — was firing without explicit Option A/B + distribution rules signal per Matt D3. Will re-fire post your amendment lock with explicit coordination signal.

**Discipline #48 candidate VALIDATED at N=2** per Matt: both scope-completeness gaps (investment scaling gap = case 11 → integrated W-α7+ scope; doc 51 § 10 distribution rules gap = case 13 → this amendment) were caught by Matt manual audit. Discipline #48 enforcement would catch pre-ratification.

---

## 1. SCOPE — what gandalf amends

### 1.1 Doc 51 § 9 amendment — KNOWN-GAP cross-node prerequisite unlocks (Matt D1)

Per Matt: this is from a PRIOR EXCHANGE between you and Matt where T4_UNLOCK_THRESHOLD = 0.70 was discussed. You have context; KR does not. Per Matt verbatim:

> *"D1 — Doc 51 amendment § 9: KNOWN-GAP cross-node prerequisite unlocks (T4_UNLOCK_THRESHOLD = 0.70 acknowledgment + Cycle 15+ deferral) [from prior exchange]"*

**Author § 9 capturing:**
- KNOWN-GAP framing (per your prior exchange context)
- T4_UNLOCK_THRESHOLD = 0.70 acknowledgment
- Cycle 15+ deferral rationale
- Cross-references to relevant doc 51 sections + downstream consumers

### 1.2 Doc 51 § 10 amendment — Investment profile distribution rules (Matt D2)

**Author § 10 with 3 sub-sections:**

**§ 10.1 — Calibration anchor profile decision (gamora discretion + gandalf recommendation):**
- **Option A — All-skills-max:** every skill at NODE_MAX (15 active / 5 passive). Maximal upper-bound profile; assumes player has saturated all investment slots.
- **Option B — Realistic-max:** specialization-aware (e.g., one skill at 15/15; remaining skills at lower investment; respects per-class skill-budget limits). Reflects actual endgame loadout patterns.
- **Trade-offs to document:** Option A is structurally cleaner (multiplier=1.0 by construction across all skills); Option B is genre-realistic but introduces per-profile variance complexity at calibration anchor
- **Gandalf recommendation:** capture YOUR design-side recommendation (and rationale) in § 10.1. Gamora retains seam discretion per Matt D2, but gandalf's recommendation provides the design anchor.

**§ 10.2 — Multi-profile distribution rules for low / mid / max / mixed:**
- **low-profile** (<~25% budget): specific distribution rule (e.g., "all skills at points=0" OR "first-tier skills at floor; later tiers at zero" OR alternative). Specify the algorithm.
- **mid-profile** (~25-75% budget): specific distribution rule (e.g., "uniform across all skills" OR "prioritize-by-tier" OR alternative)
- **max-profile** (≥~75% budget): specific distribution rule (e.g., "Option A all-max" OR "Option B specialization-saturated" OR derived from § 10.1 anchor decision)
- **mixed-profile**: rule for atypical builds (e.g., "one skill at max + remaining at zero" OR "two skills at mid + remaining at zero" OR alternative)

**§ 10.3 — Per-profile point allocation algorithm:**
- Concrete algorithm or procedure gamora's Phase 4 multi-dim sweep uses to construct each profile's investment distribution
- Includes: profile → skills → per-skill investment_points mapping; constraints (NODE_MAX active/passive); validation rules
- Cross-references Pattern 1 + Pattern 2 max-investment construction property (doc 51 § 7) — confirms allocation algorithm preserves the construction

### 1.3 Out of scope

- Numeric profile thresholds (low/mid/max percentages) — gamora seam discretion per doc 51 § 6.3
- Per-class skill-budget specifics — out of doc 51 scope (lives in separate canonical OR gamora seam implementation)
- Patterns 3-6 unlocks beyond T4 (Cycle 15+ canonical-locked per D1 § 9)
- Bundle Gate-2 verification of § 9/§ 10 amendments — fires post Phase 4 close

---

## 2. DISCIPLINE #40 CASE (c) FRAMING

Doc 51 STATUS is **CURRENT (LOAD-BEARING)** as of `ba1c4e7`. Amendment via Discipline #40 case (c) extension protocol (NOT retraction; this is scope-completeness fold-in to existing canonical):

- Capture trigger explicitly (Matt 2026-05-28 evening D1+D2 RATIFICATION)
- New §§ 9 + 10 added (do NOT modify §§ 1-8 except header references)
- Header amendment: tag this as "second iteration" of doc 51 (first iteration = `ba1c4e7` Phase 2 lock; this iteration = § 9 + § 10 additions)
- Cross-references in doc 50 § 4.7 + doc 47 § 3 forward-link blocks updated if applicable
- Discipline #45 vocabulary grep re-audit on new content

**Tag suggestion:** `gandalf/v1.15-doc-51-scope-completeness-amendment-batch-1` (your seam discretion).

---

## 3. REQUIRED READING

- Doc 51 current state: `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` (your Phase 2 authoring; full re-read for amendment composition)
- Master scoping: `agentic_orchestration/dispatches/2026-05-28-integrated-w-alpha-7-plus-master-scoping.md` § 1 Phase 3+4 (downstream Phase 4 distribution rules consumer)
- Phase 3a rocket coordination signal (verbatim in hive-mind state): "skill.investment_points must be set to 15..." (vague-on-which-skills)
- Phase 3b rocket Pattern 2 close (passive baking architecture)
- Phase 3c gamora encounter HP rebalance close (Phase 3d anchor)
- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` (Pattern 1 + 2 constants per gandalf canonical)
- `~/Games/reincarnated-engine/src/reincarnated/generation/skill_schema.py` (investment_points fields)
- Hive-mind state: `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT 2026-05-28 EVENING DOC 51 SCOPE-COMPLETENESS AMENDMENT BATCH"
- Discipline #40 case (c) procedure per `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## 4. ACCEPTANCE + DELIVERABLE

| # | Artifact | Location |
|---|---|---|
| 1 | Doc 51 § 9 KNOWN-GAP T4_UNLOCK_THRESHOLD acknowledgment authored | doc 51 append |
| 2 | Doc 51 § 10.1 calibration anchor profile (Option A vs B + gandalf recommendation) | doc 51 append |
| 3 | Doc 51 § 10.2 multi-profile distribution rules (low/mid/max/mixed) | doc 51 append |
| 4 | Doc 51 § 10.3 per-profile point allocation algorithm | doc 51 append |
| 5 | Header amended ("second iteration"; new sections referenced) | doc 51 head |
| 6 | Discipline #45 vocabulary grep re-audit on new content | sign-off block updated |
| 7 | Cross-reference verification (doc 50 § 4.7 + doc 47 § 3 still valid; no breaking changes) | doc-internal verification |
| 8 | Tag `gandalf/v1.15-doc-51-scope-completeness-amendment-batch-1` cut | engine commit |

**Auto-commit + auto-push** per CLAUDE.md addendum.

**Effort estimate:** ~30-45min per Matt.

---

## 5. KR ROUTING POST-AMENDMENT-LOCK

On your tag fire:
1. KR re-fires Phase 3d gamora with explicit **Option A vs B coordination signal** per § 10.1 lock (your recommendation + gamora final decision)
2. KR fires Phase 4 gamora with **per-profile distribution rules** per § 10.2 + per-profile point allocation per § 10.3 — gamora doesn't have to guess
3. Phase 4 + Phase 5 + Phase 6 continue per master scoping cadence

---

**KR signature:** authored per Matt 2026-05-28 evening D1+D2+D3+D4 RATIFICATION + Discipline #40 case (c) extension protocol for LOAD-BEARING canonical amendment + Discipline #48 candidate validation at N=2 (Phase 6a disciplines batch consideration). Phase 3d gamora halted clean (no commits); re-fires post your amendment lock with explicit coordination signal.
