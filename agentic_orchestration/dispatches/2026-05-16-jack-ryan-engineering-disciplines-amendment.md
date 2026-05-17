# Dispatch — 2026-05-16 — jack-ryan — Engineering-disciplines.md amendment: codify #13a + #13b + #14 + terminology lock (per form-bias batch Entry 4)

**From:** knight-rider (authored per form-bias 5-entry batch Entry 4 implementation cascade item: "Jack-ryan authors the discipline entries in `engineering-disciplines.md` per ADR-002 documentation pattern. ~1 session of authoring.")
**To:** jack-ryan (working-agreement steward; DEV-MODE authoring per ADR-002 documentation pattern)
**Approved by:** Matt at 2026-05-16 Day 4 (form-bias batch committed `5d51b5a`; Entry 4 is the locked decision; this dispatch is the operational implementation)
**Status:** PENDING — ACTIVE
**Estimated effort:** ~1 session (~2-3h); documentation authoring per the locked Entry 4 framing
**Acceptance:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md` extended with 3 new disciplines (#13a / #13b / #14) + terminology lock formalized; existing 12 disciplines preserved; cross-references to Entry 4 decisions-log entry + the form-bias-cadence-strategy doc + the pre-llm-substrate-inventory.md terminology-lock authoritative source; intermediate commit (no tag).

---

## Context — what Entry 4 of the form-bias batch decided

Per the 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) Entry 4:

> **Decision:** Three new engineering disciplines are codified for inclusion in `reincarnated-engine/design/working-agreement/engineering-disciplines.md`, extending the current set of 12 with three additions. Jack-ryan authors the discipline entries themselves per the engineering-disciplines authorship discipline (#1 — math-before-code; #11 — attribution; etc. — knight-rider drafts decision; jack-ryan authors discipline text).

The 3 new disciplines (per Entry 4 framing):

1. **#13a — Implementation-vs-intent drift**
2. **#13b — Outcome attribution opacity**
3. **#14 — Internal-vs-generative schema separation**

Plus the **terminology lock** is formalized (skew off-limits; drift narrow-use; bias qualified-only).

**Source-of-truth for the discipline statements:** Entry 4 of the form-bias batch is the locked decision; your job is the documentation authoring per ADR-002 pattern. Entry 4's text is comprehensive; this dispatch operationalizes the codification.

## What this dispatch does

### Step 1 — Author Discipline #13a entry

Per Entry 4 of the form-bias batch:

**Statement:** Code states X; canonical doc states Y. Observable from code-reading alone. No telemetry needed. No measurement needed. **The code IS the evidence.**

Author the discipline entry following the existing 12 disciplines' format pattern in `engineering-disciplines.md`:
- Discipline name + brief statement
- Why it matters (operational triggers + rationale)
- Operational example (Cluster E in the form-bias work)
- Triggerable Gate-1 question (per Entry 4)
- Cross-references (Entry 4; doc 37 § 9.1 original draft; form-bias 5-entry batch)

### Step 2 — Author Discipline #13b entry

Per Entry 4 of the form-bias batch:

**Statement:** Per-variable convergence contribution unknown without ablation. This is not "drift" — it is *unmeasured composition*. An epistemic gap, not a behavioral one. **Discipline #13b is not actionable through process gates; it is actionable only through targeted empirical experiments.**

Author per the same format:
- Discipline name + brief statement
- Why it matters (the form-bias work surfaced 5 aggregate convergence-shape observations; none have per-variable evidence)
- Operational example (the terminology lock; Cluster B observations as "convergence-shape observations, not attributions")
- Triggerable Gate-1 question (per Entry 4)
- Cross-references

### Step 3 — Author Discipline #14 entry

Per Entry 4 of the form-bias batch:

**Statement:** Internal data structures (e.g., the canonical-four substrate) must be hidden from LLM-visible surfaces. Per-instance vocabulary fills the LLM-visible slot. The cipher architecture (doc 37 § 6) is the canonical example of this discipline applied to one specific seam.

Author per the same format:
- Discipline name + brief statement
- Why it matters (Cluster E universal LLM-drift surface; the 6 named drift sites)
- Operational example (any future LLM prompt-construction site that re-introduces canonical-four-flavored labels)
- Triggerable Gate-1 question (per Entry 4)
- Cross-references

### Step 4 — Formalize the terminology lock

Per Entry 4 of the form-bias batch + `canonical/story/pre-llm-substrate-inventory.md` § 3 (authoritative source):

Add a "Terminology Lock" section (or equivalent) to `engineering-disciplines.md` capturing:

- **Skew** is off-limits in form-bias work + downstream design until per-variable evidence exists. Skew requires decomposition. Use "the engine has a structural-presupposition toward X" (claimable from code) OR "the convergence shape observed is X" (claimable from telemetry) — never the conjunction.
- **Drift** is reserved for code-vs-intent comparisons (Discipline #13a's narrow legitimate use).
- **Bias** is permissible only when qualified ("the substrate has a structural-presupposition bias toward humanoid X" — qualified to a structural claim; not an outcome claim). **Unqualified "bias" (e.g., "the engine has a bias toward fire") is not permitted; the structural-presupposition or convergence-shape qualifier is load-bearing.**

This lock is operative across all design docs, decisions-log entries, and dispatch authoring going forward.

### Step 5 — Preserve existing 12 disciplines

Verify the existing 12 disciplines (#1-#12) are preserved unchanged. The 3 new disciplines + terminology lock are ADDITIVE; no rewriting of #1-#12.

### Step 6 — Cross-references

Each new discipline entry should cross-reference:
- Entry 4 of the form-bias 5-entry batch (committed `5d51b5a`)
- `canonical/story/form-bias-cadence-strategy.md` § 1.3 + § 2.1 (analysis source)
- `canonical/story/pre-llm-substrate-inventory.md` § 3 (terminology-lock authoritative source)
- 2026-05-08 doc 37 § 9.1 + § 9.2b (original drafts; Entry 4 codifies + splits them)

### Step 7 — Commit + AGENT_STATE

- Commit the `engineering-disciplines.md` amendment (the engineering repo; `reincarnated-engine/design/working-agreement/engineering-disciplines.md`)
- AGENT_STATE.md (if applicable for jack-ryan; check working-agreement conventions)
- No intermediate tag (documentation amendment; tag-less per working-agreement convention)
- Completion record at bottom of this dispatch filled

## Cross-seam considerations

- **All seams:** the new disciplines apply at Gate-1 review for any future dispatch touching code-vs-canonical-doc fidelity (rocket schemas, star-lord prompts, drax displays, gamora sim, elrond catalogue, etc.)
- **Knight-rider:** future dispatch authoring includes the triggerable Gate-1 questions in required-reading section where relevant
- **Gandalf:** the terminology lock is operative across all design docs going forward (your discipline-text authoring should be terminology-lock-compliant by example)

## Out of scope (explicit)

- **NO design-decision changes.** Entry 4 of the form-bias batch is the locked decision; your job is documentation authoring only.
- **NO rewriting of disciplines #1-#12.** Additive only.
- **NO new disciplines beyond #13a + #13b + #14.** If you observe gaps during authoring, surface as future-discipline candidates; do NOT codify unilaterally.
- **NO Gate-1-process changes.** The new disciplines extend the gate-question pool but don't change the gate-process itself.
- **NO terminology lock extensions** beyond the 3 terms (skew / drift / bias) named in Entry 4. If you observe other terminology requiring lock, surface as a finding for future Matt-decision.

## Required reading

- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 4 is your source-of-truth for the discipline statements + terminology lock
- `canonical/story/form-bias-cadence-strategy.md` § 1.3 + § 2.1 (analysis source)
- `canonical/story/pre-llm-substrate-inventory.md` § 3 (terminology-lock authoritative source)
- 2026-05-08 doc 37 § 9.1 + § 9.2b (original drafts)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (your target file; preserve existing 12 disciplines)
- `agentic_orchestration/REVIEW_PROCESS.md` (ADR-002 documentation pattern context)

## Acceptance criteria

- [ ] Discipline #13a entry authored in engineering-disciplines.md (statement + rationale + operational example + Gate-1 question + cross-references)
- [ ] Discipline #13b entry authored (same format)
- [ ] Discipline #14 entry authored (same format)
- [ ] Terminology Lock section authored (skew off-limits; drift narrow-use; bias qualified-only)
- [ ] Existing 12 disciplines preserved unchanged
- [ ] All 3 new entries cross-reference Entry 4 + form-bias-cadence-strategy.md + pre-llm-substrate-inventory.md + doc 37 § 9.1/§ 9.2b
- [ ] Commit landed on main with descriptive message
- [ ] Knight-rider notified at completion

## Tag policy

No tag (documentation amendment; working-agreement convention).

---

## Completion record

**Completed:** 2026-05-16
**Commit hash:** `4259969`
**Notes for knight-rider:**

All acceptance criteria met:

- [x] Discipline #13a entry authored (statement + rationale with 4 empirical instances + Cluster E operational example + Gate-1 question + cross-references)
- [x] Discipline #13b entry authored (statement + form-bias 5-observation rationale + gamora V2.1 emission-gap empirical example + Gate-1 question + cross-references)
- [x] Discipline #14 entry authored (statement + Cluster E 6-site table rationale + operational example + what-is-not-permitted list + Gate-1 question + cross-references)
- [x] Terminology Lock section authored (skew off-limits; drift narrow-use; bias qualified-only; structural-presupposition and convergence-shape permitted alternatives; table format per pre-llm-substrate-inventory.md § 3 pattern)
- [x] Existing disciplines #1-#12 preserved unchanged (additive only; verified via section-heading scan)
- [x] All 3 new entries cross-reference decisions-log `5d51b5a` + form-bias-cadence-strategy.md + pre-llm-substrate-inventory.md + doc 37 § 9.1/§ 9.2b
- [x] Commit `4259969` landed on main with descriptive message
- [x] No intermediate tag (documentation amendment per working-agreement convention)

**One authoring decision:** Discipline #13b includes the gamora V2.1 emission-gap example per the dispatch's operational telemetry note. The example illustrates the epistemic-gap framing cleanly: aggregate symptom (missing emission fields) was observable; per-construction-site attribution required targeted empirical inspection. The example was cited alongside the form-bias convergence-shape observations as a parallel instance from a different domain, which strengthens generalizability.

**File amended:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
