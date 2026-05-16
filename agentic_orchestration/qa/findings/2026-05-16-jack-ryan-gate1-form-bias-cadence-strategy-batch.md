# Finding — 2026-05-16 — Form-bias cadence strategy decisions-log batch (5 entries)

**Reviewer:** jack-ryan
**Severity:** WARN (no BLOCKs; two WARNs; three INFOs)
**Target:** decisions-log batch, pre-commit (Gate 1)
**Developer:** knight-rider (author)
**Principles applied:** Review Principles 1 (precision), 2 (attribution), 3 (cross-seam consistency), 5 (scope clarity)

---

## Overall verdict: PASS WITH FLAGS

Two WARNs and three INFOs. No BLOCKs. The batch is structurally sound, attribution is tight, reasoning cites strategy doc sections by number throughout, and the five entries are defensibly distinct. Flags below do not block Matt approval but two should be addressed before commit.

---

## Per-entry verdicts

| Entry | Verdict | Flags |
|---|---|---|
| 1 — Strategic-axis lock | PASS | 0 |
| 2 — Three-layer model + cipher-width framework | PASS WITH FLAGS | 1 WARN, 1 INFO |
| 3 — Four sub-locks deferred | PASS | 0 |
| 4 — Disciplines #13a/#13b/#14 + terminology lock | PASS WITH FLAGS | 1 WARN |
| 5 — Cadence Option II locked | PASS WITH FLAGS | 2 INFO |

---

## Flags

### WARN-1 (Entry 2) — Ailment-damage-signatures re-activation conflicts with live DEFERRED status

**Entry 2 line:** `Ailment-damage-signatures work re-activated as load-bearing dependency`

**Conflict:** The project memory note `project_ailment_damage_thematic.md` explicitly records this as **DEFERRED** ("revisit after B14.5 lands to see if recompose-first dissolves the need"). B14.5 has since landed (operational calibration epoch declared 2026-05-16), but no decisions-log entry or strategy-doc section formally lifts the deferral. The strategy doc (§ 9.1, rocket cascade item 4) correctly marks it "Future — ailment-damage-signatures work (re-activated per doc 37 § 6.4; load-bearing for doppelganger gate)" but Entry 2 promotes this into the normative "cipher architecture stays operative" list without the same hedging.

**Risk:** If this entry lands with "re-activated as load-bearing dependency" unqualified, future dispatches (gamora doppelganger gate; rocket ailment work) will cite it as a current lock. The memory note says it is still deferred. The strategy doc's "Future" marker is the right hedge; Entry 2 should match it.

**Required fix (before commit):** Change Entry 2's cipher architecture bullet from `Ailment-damage-signatures work re-activated as load-bearing dependency` to `Ailment-damage-signatures work re-activated as load-bearing dependency (post-B14.5 V1; formal deferral lifted per strategy doc § 9.1; awaiting B14.5 V2 / B6 scheduling)` — OR add a parenthetical matching the strategy doc's "Future" framing. Either wording removes the ambiguity.

Cite: Discipline #1 (attribution), Discipline #11 (empirical inspection over assumption), Review Principle 2 (attribution).

---

### WARN-2 (Entry 4) — Terminology lock self-application: "drift" usage in the lock definition

**Entry 4 line:** `Drift is reserved for code-vs-intent comparisons (Discipline #13a's narrow legitimate use).`

This is correct — consistent with `pre-llm-substrate-inventory.md` § 3's table. No violation there.

**However:** the Discipline #13b statement uses the phrase "outcome attribution opacity" which is fine, but the **operational example** for #13b reads: `"the word skew is off-limits until per-variable evidence exists. Drift is reserved for code-vs-intent comparisons."` This is the lock *restating itself* inside the lock definition — a minor circularity, not a contradiction. The actual risk is that the lock says `drift` is reserved for narrow use, but the terminology-lock section itself (in Entry 4) does not constrain the word "bias" to the full qualified form. It says `Bias is permissible only when qualified ("the substrate has a structural-presupposition bias toward humanoid X")` — but the entry body uses `"structural-presupposition bias toward X"` as the permitted form without specifying that unqualified "bias" is the disallowed form. In practice this will work; the issue is that the lock could be read as permitting shorthand like "has a bias toward X" without the "structural-presupposition" qualifier, which creates exactly the ambiguity it is trying to prevent.

**Required fix (before commit):** Add one sentence after the bias permission: `Unqualified use of "bias" (e.g., "the engine has a bias toward fire") is not permitted; the structural-presupposition or convergence-shape qualifier is load-bearing.`

Cite: Discipline #12 (semantic-shifting), Review Principle 1 (precision).

---

### INFO-1 (Entries 2, 3, 4) — Companion-entry cross-references are not fully bidirectional

**Observation:**
- Entry 2 lists companions: Entry 1, Entry 3, Entry 5. **Missing: Entry 4.** Entry 4 lists Entry 2 as companion; Entry 2 does not reciprocate.
- Entry 3 lists companions: Entry 1, Entry 2, Entry 5. **Missing: Entry 4.** Entry 4 does not list Entry 3 as companion either. Both are missing each other.
- Entry 4 lists companions: Entry 1, Entry 2, Entry 5. **Missing: Entry 3.** Entry 3 lists Entry 4 as companion (indirectly — Entry 3's jack-ryan note says sub-locks map to discipline enforcement); Entry 4 does not reciprocate.

**Summary of missing bidirectional links:**
- Entry 2 → Entry 4: absent
- Entry 3 → Entry 4: absent
- Entry 4 → Entry 3: absent

**Suggested fix:** Add to Entry 2's companion line: `; Entry 4 (disciplines the three-layer model enforces)`. Add to Entry 3's companion line: `; Entry 4 (disciplines the sub-lock deferred status gates)`. Add to Entry 4's companion line: `; Entry 3 (sub-locks whose deferred gates these disciplines enforce at)`.

Not blocking — Matt can still read the batch cleanly, and the gaps are small. But the cross-reference map should be symmetric before commit so downstream dispatches citing entries get the full navigation graph.

Cite: Review Principle 3 (cross-seam consistency).

---

### INFO-2 (Entry 5) — Stage 3 → Stage 4 Experiment 1 gate dependency slightly understated

**Observation:** Entry 5 says "Stage 4 starts after Stage 3 lands" and "Combine Stage 3 + Stage 4: rejected. Experiment 1's residual-bias finding gates Stage 4 content." However the stage table describes Stage 4's trigger as unlocked when Stage 3 completes, without explicitly stating that Experiment 1's residual-bias result must also be processed before Stage 4 content is *scoped* (not merely before it launches). The strategy doc (§ 7.1) is clear: if residual-bias is confirmed, anti-bias scaffolding lands before Stage 4; if negated, Stage 4 proceeds. Entry 5's table does not capture the conditional branching, only the sequential dependency.

**Risk:** Low. A future knight-rider reading Entry 5 may author Stage 4 dispatch scope before Experiment 1's result is processed, on the technically-correct reading that Stage 3 has "completed."

**Suggested fix:** In the Stage 3 row of Entry 5's four-stage table, add to "Unblocks": `Stage 4 scope authoring (conditional on Experiment 1 residual-bias result; Stage 4 content differs if bias confirmed vs negated — see strategy doc § 7.1)`.

Cite: Review Principle 1 (precision), Discipline #1 (math-before-code on design sequencing).

---

### INFO-3 (Entry 5) — Timeline estimates are unattributed to strategy doc section in entry body

**Observation:** Entry 5 gives timeline estimates: `Option II ≈ 5-8 weeks; Option I ≈ 8-12 weeks; Option III ≈ 3-5 weeks`. These are lifted from strategy doc § 7.2 but Entry 5's Reasoning section says only "Per gandalf's strategy doc § 7" — the timeline table itself appears in the entry's Decision section without a citation anchor. The "~9-entity team capacity" basis is also not attributed (it comes from strategy doc § 7.2 body text).

**Risk:** Minimal. The number is accurate; the source is clear. But timeline estimates in decisions-log entries invite audit when milestones slip; having the explicit section number next to the figure (not just in Reasoning) makes the audit cheaper.

**Suggested fix:** Add `(per strategy doc § 7.2)` inline next to the timeline figures in the Decision section.

Cite: Discipline #11 (attribution clarity), Review Principle 2.

---

## Answers to knight-rider's six cross-cutting questions

**Q1 — Entry count justification (five vs fewer):** Confirmed. Five distinct entries are correct. Entry 5 (cadence) and Entry 1 (strategic-axis) are independently cited by downstream dispatches — rocket dispatches cite Entry 1 + Entry 5 separately; star-lord dispatches cite Entry 2 + Entry 4 separately; jack-ryan future Gate 1 reviews cite Entry 3 + Entry 4 separately. Folding Entry 5 into Entry 1 would couple a "what is decided" entry (strategic-axis) with a "how to sequence the implementation" entry (cadence), breaking the single-purpose discipline that keeps decisions-log entries scannable. No push-back.

**Q2 — Discipline #13a/#13b split durability:** The split is durable. Operational triggers genuinely diverge:
- #13a fires at code-review time: "does the code match the spec?" Observable from code-reading alone, actionable through Gate-1 process.
- #13b fires only when a causal attribution claim is asserted: "is this attribution claim backed by ablation evidence?" Not observable from code; requires inspection of what is *being claimed*, not what is in the code.
These are different reviewer behaviors and different remediation paths (#13a = fix the code or update the spec; #13b = run the ablation experiment or downgrade the claim to hypothesis). The split is not documentation-only — it prevents the conflation that `pre-llm-substrate-inventory.md` § 3 explicitly records as the failure mode gandalf walked into.

**Q3 — Discipline #14 project-wide scope:** Confirmed project-wide. Strategy doc § 6.4 makes it explicit: the internal-vs-generative-schema separation pattern applies to any LLM-using seam, not only to Cluster E. Currently star-lord is the primary site; spirit-guide (per memory `project_gear_and_spirit_guide.md`) is a future candidate; any new seam that constructs LLM prompts inherits the discipline. The scope claim in Entry 4 is correct.

**Q4 — Stage 3 requires Stage 2 grouping infrastructure:** Verified. Strategy doc § 7.1 states Stage 2 verifies "the grouping layer functions; per-season grouping selection works; LLM produces coherent per-season vocabulary against grouping structure." Stage 3's cipher migration hides canonical-four from LLM and replaces with per-season vocabulary — but that per-season vocabulary must already have a grouping structure to generate against, or the cipher migration has nothing to fill the vacancy with. Stage 2 supplies the grouping layer that Stage 3's migration depends on. Reversing the order would produce a Stage 3 migration with no grouping infrastructure to generate per-season vocabulary against. The dependency is real, not a process preference. The "Stage 3 actually requires Stage 2" claim holds.

**Q5 — Terminology lock precision and "structural-presupposition bias" permissibility:** The lock language is sufficiently precise for Gate-1 application with one gap (see WARN-2 above: unqualified "bias" needs to be explicitly called out as non-permitted). The qualified form "the substrate has a structural-presupposition bias toward humanoid X" is genuinely permissible — it is claimable from code alone (the schema shape is the evidence; no convergence attribution required). The strategy doc body uses this form correctly throughout (e.g., § 2.1 Pattern P1: "the schema's shape...presupposes humanoid anatomy"; P2: "the mechanic is form-agnostic; the label carries humanoid weight"). The lock's "drift" reservation is clean. The "skew" prohibition is clean. The only gap is the unqualified "bias" shorthand risk (WARN-2).

**Q6 — Companion-entry cross-reference bidirectionality:** Three missing links found (see INFO-1 above). Entry 1 ↔ Entry 2/3/4/5: symmetric. Entry 5 ↔ Entry 1/2/3/4: symmetric. Entry 2 ↔ Entry 4: one-directional (Entry 4 references Entry 2; Entry 2 does not reference Entry 4). Entry 3 ↔ Entry 4: both missing each other. Specific fixes listed in INFO-1.

---

## Discipline compliance checks

**Discipline #1 (math-before-code):** N/A for design entries. No quantitative claims are unattributed except the timeline figures (see INFO-3) and the "~9-entity team capacity" framing. The latter is referenced as "current ~9-entity team capacity" without a source; it is a project-state observation not requiring formal attribution. No concern.

**Discipline #11 (attribution):** Each entry's Reasoning section cites specific strategy doc sections by number. Entry 1 cites § 5.1 + § 5.2 + § 5.4 + § 5.5. Entry 2 cites § 6.1 + § 6.2 + § 6.3. Entry 3 cites § 5.3 + § 6.5. Entry 4 cites § 1.3 + § 2.1 + `pre-llm-substrate-inventory.md` § 3. Entry 5 cites § 7. Attribution is clean throughout. The ailment-damage-signatures citation issue (WARN-1) is the only gap.

**Discipline #12 (semantic-shifting):** The terminology lock in Entry 4 is checked against its own constraints:
- "skew" does not appear in Entry 4's lock definition text (correct).
- "drift" appears exactly twice: once in the reserved-for definition ("code-vs-intent comparisons") and once in the #13b operational example ("drift is reserved for code-vs-intent comparisons"). Both uses are within the narrow legitimate scope. No violation.
- "bias" appears in the permitted form with "structural-presupposition" qualifier in the main definition. The gap (unqualified shorthand not explicitly prohibited) is WARN-2.
- The lock language does not use "skew" or "drift" outside the permitted narrow scope anywhere in the entry body. Compliant.

---

## Design-instinct pushback for knight-rider (pre-Matt approval surface)

One observation worth surfacing before Matt approves the batch — not a block, but a design-instinct flag:

**Entry 2's "ailment-damage-signatures re-activation" is the most load-bearing claim in the batch that was decided outside this batch.** The memory note records the feature as DEFERRED post-KI-B6-1. The strategy doc re-activates it. If that re-activation is correct (B14.5 has landed; the deferral condition has passed), then the decision to lift the deferral should be explicit — either Matt confirms it verbally in this session, or Entry 2's text adds a sentence: "Deferral lifted: B14.5 V1 primary loop has landed; the strategy doc § 9.1 re-activates ailment-damage-signatures as load-bearing for the doppelganger gate under Position (ii)." Without that explicit confirmation, a developer reading the memory note will see DEFERRED; a developer reading Entry 2 will see it as active. WARN-1 above is the process fix; this is the design-instinct note: get Matt's explicit confirmation before this lands as a commit.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-form-bias-cadence-strategy.md` — reviewed artifact
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/form-bias-cadence-strategy.md` — source truth for all five entries; §§ 5, 6, 7, 8, 9 reviewed
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/pre-llm-substrate-inventory.md` — § 3 terminology lock; §§ 10, 11 sub-lock framing
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-16-gandalf-form-bias-cadence-strategy.md` — completion record with per-question takeaways
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — current discipline set (#1–#12); target for #13a/#13b/#14 append
- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` — companion entries c000d7d (engine-balance-stewardship + calibration-epoch) confirmed present; insertion point after calibration-epoch entry confirmed
