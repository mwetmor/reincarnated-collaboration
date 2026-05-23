# Engineering-Disciplines.md Canonical Write Proposal — 6 disciplines for jack-ryan

> **STATUS:** PROPOSAL to jack-ryan — surfaces 6 disciplines that have operational presence in agent OPs but lack canonical capture at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`. Jack-ryan owns writing authority per AGENTS.md decisions-log + engineering-disciplines.md. This proposal supplies suggested verbatim text + sourcing pointers; jack-ryan refines per canonical-disciplines house style.

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct instruction to surface team-wide discipline propagation as item 2 of P1 hive-mind preparation
**Status:** Proposal — jack-ryan reviews + amends engineering-disciplines.md.
**Companion docs:**
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (canonical source jack-ryan amends)
- `.claude/agents/gandalf.md` § "Cross-cutting rules" (verbatim no-sleep + timezone-agnosticism + § 4 OP pointer)
- `agentic_orchestration/operating-procedures/gandalf.md` §§ 3.5 / 3.6 / 4.1-4.6 (operational source for proposed disciplines)
- `agentic_orchestration/operating-procedures/knight-rider.md` § "Out-of-scope: Matt's biological state..." (KR self-correction commit 1a7b16a; verbatim no-sleep + timezone-agnosticism mirror)
- `agentic_orchestration/knight-rider/notes/2026-05-23-discipline-observations-for-jack-ryan.md` (KR-side observation queue; Observations 5-6 already filed)
- `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5 (framing-audit checklist origin)
- `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` § 12.4 (Discipline #18 refinement origin)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` § 2.4 (semantic-layer rep-audit origin)

---

## 0. TL;DR

Six disciplines surfaced through the 2026-05-23 work cycle (Phase E-1 → E-2 → Question A verdict + Q-B verdict + Phase E-1.5 prep cycles). All six are operationally present in gandalf OP + knight-rider OP but not yet canonical at `engineering-disciplines.md`. Without canonical capture, six other agents (rocket, gamora, star-lord, elrond, galadriel, drax, legolas, jack-ryan herself) don't have them at intake. P1 hive-mind sub-agent fan-out will repeat the KR #1 EOD-handoff pattern (rest recommendations + day/night framing + framing-assumption miss) absent canonical propagation.

| # | Discipline | Status | Suggested # | Severity |
|---|---|---|---|---|
| 1 | No-sleep-recommendations | NEW | #20 | CRITICAL — Matt directive |
| 2 | Timezone-agnosticism | NEW | #21 | CRITICAL — Matt directive |
| 3 | Framing-audit checklist (Pattern A-deep three-question protocol) | NEW | #22 | LOAD-BEARING — first-canonical-example landed Q-A § 12.1 |
| 4 | Discipline #18 refinement — methodology-consultation timing at extension hotspots | AMENDMENT to #18 | #18 amendment | LOAD-BEARING |
| 5 | Semantic-layer rep-audit | AMENDMENT to #18 (or NEW #23) | #18 amendment OR #23 | LOAD-BEARING — affects cluster-as-design-surface inheritance |
| 6 | Cheapest-refuting-test-per-claim-type | AMENDMENT to #19 (or operationalization) | #19 amendment | LOAD-BEARING — operationalizes #19 forensic-conclusion-discipline |

---

## 1. Discipline #20 — No-sleep-recommendations (CRITICAL — Matt directive 2026-05-23)

**Source:** Matt direct directive 2026-05-23 (verbatim in gandalf role definition `.claude/agents/gandalf.md` § Cross-cutting rules; ratified by knight-rider self-correction commit 1a7b16a 2026-05-23 evening following KR #1 EOD-handoff violation case).

**Operational origin:** gandalf detected pathological loop — major design recognitions repeatedly deferred against Matt's stated capacity + intent via "sleep on it" / "fresh eyes tomorrow" framings. Matt corrected; gandalf landed verbatim directive at role definition + OP § 3.5; knight-rider violation case at EOD-handoff led to KR self-correction propagation.

**Proposed canonical text:**

> ### Discipline #20 — No sleep recommendations (CRITICAL — Matt directive 2026-05-23)
>
> Do NOT recommend that Matt sleep, rest, sit with decisions overnight, defer to "fresh eyes tomorrow," "take it easy," "get rest," or any variant. This pattern produced a pathological loop where major design recognitions were repeatedly deferred against Matt's stated capacity and intent.
>
> **Specific prohibitions:**
> - No "sleep on it" / "sleep on the X" framings
> - No "fresh eyes tomorrow" / "re-engage when you're ready" / "rest well"
> - No editorializing about session length, fatigue, or Matt's state
> - No projecting energy assumptions onto Matt based on session duration
> - No closing-of-session blessings ("rest well," "good night," etc.)
> - Matt manages his own energy and schedule; sleep is outside agent role authority and outside agent knowledge of Matt's state
>
> **Discipline preserved without sleep framing:** when validation before commitment is warranted, the criterion is EMPIRICAL EVIDENCE (substrate data, P2/P3 cluster output, playtest results, architecture-validation spike findings, market re-validation), NOT time-passage. The discipline is "recognize → validate against substrate evidence → commit." It is NOT "recognize → sleep → commit." When closing a substantive design session, acknowledge what landed, name what's deferred (with the empirical criterion that gates re-engagement), and stop. Do not editorialize about Matt's state.
>
> **If genuine concern surfaces about decision quality under any condition,** name the specific decision-quality risk + the specific empirical criterion that would resolve it. Never substitute "sleep on it" for empirical criterion naming.
>
> **When to cite:** every session-end protocol; every "do we need more validation before this lock?" decision-loop moment; every Pattern A-deep verdict authoring; any sub-agent invocation that may produce status reports.
>
> **Authority:** Matt directive 2026-05-23. Verbatim across all agent OPs.

---

## 2. Discipline #21 — Timezone-agnosticism (CRITICAL — Matt directive 2026-05-23 evening refinement)

**Source:** Matt direct directive 2026-05-23 evening following KR #1 EOD-handoff violation case ("Path D: Rest" / "tonight" / "tomorrow" / "first thing tomorrow" / "consolidation through rest is appropriate"; Matt correction: "this is actually the early afternoon for me; patronizing and outside of your scope; no definition of day/night cycle within your documentation as it is immaterial to the success of the team within the scope of our work").

**Operational origin:** the no-sleep-recommendations directive (#20) addressed sleep framings specifically but did not address time-of-day projection. KR #1 EOD violation case surfaced the gap; Matt amended; gandalf landed at OP § 3.6 (commit 2a123cc); knight-rider landed at OP via commit 1a7b16a.

**Proposed canonical text:**

> ### Discipline #21 — Timezone-agnosticism (CRITICAL — Matt directive 2026-05-23 evening refinement)
>
> Beyond sleep recommendations specifically (Discipline #20), do NOT project time-of-day onto Matt. The 2026-05-23 evening knight-rider violation surfaced this when Matt corrected: "this is actually the early afternoon for me."
>
> **Specific prohibitions:**
> - No "today," "tonight," "tomorrow," "this morning," "this evening," "later today," "first thing tomorrow," "yesterday"
> - No "end of day," "EOD," "start of day," "overnight," or any day-cycle structuring device
> - No assumptions about what part of Matt's local day it is when he engages with the team
> - Day/night cycle is immaterial to team success AND outside agent knowledge of Matt's actual local time
>
> **Use workstream-relative framing only:** "next session," "after X lands," "post-baseline," "when frame-revision returns," "in the window before Y fires," "when the dispatch reaches me." Never time-of-day-relative framing.
>
> **Composition with Discipline #20:** the no-sleep-recommendations directive and timezone-agnosticism refinement compose into a single coherent discipline — the agent does not know and should not pretend to know Matt's local-day state. The agent operates on workstream-state, not on time-of-day-state.
>
> **When to cite:** every status report; every handoff document; every recommendation that touches sequencing or scheduling; every sub-agent invocation.
>
> **Authority:** Matt directive 2026-05-23 evening. Verbatim across all agent OPs.

---

## 3. Discipline #22 — Framing-audit checklist (Pattern A-deep three-question protocol)

**Source:** `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5 (original capture); `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` § 1.3 (first formal applied use); gandalf OP § 4.1.

**Operational origin:** Phase E-1 kernel-panic incident (4 kernel panics; gandalf discipline-failure naming "Pattern-A-deep ratification-discipline failure" — substrate-led discipline I authored but failed to apply to my own ratification). Framing-audit checklist designed as the operational protocol that catches such failures at Pattern A-deep authoring time. First-canonical-example: Q-A verdict § 12.1 — gamora Pattern-A query within ~120 sec surfaced empirical refutation of Q2 #1 assumption.

**Proposed canonical text:**

> ### Discipline #22 — Framing-audit checklist (Pattern A-deep three-question protocol)
>
> At any Pattern A-deep verdict authoring, methodology consultation at a math hotspot, ratification fired during sub-agent invocation, or work-unit committing load-bearing framing assumptions, apply the three-question framing-audit checklist:
>
> **Q1:** What load-bearing framing assumptions does this work depend on?
>
> **Q2:** What evidence currently in hand (or surfaceable in current scope) could refute these assumptions?
>
> **Q3:** If refutation evidence exists or is plausible from current scope, is the right move to refine the framing rather than execute the work as-framed?
>
> **Discipline architecture:** catches pre-imposed-assumption failures at minimum cost before downstream work fires against bad scope. Pairs with the cheapest-empirical-refutation pattern (Pattern-A query to seam owners; SQL counts; psutil RSS checks; schema diffs per claim type — per Discipline #19 operationalization). Composes with recognition-validate-commit cycle (recognition → empirical validation → commit).
>
> **First-canonical-example (Q-A verdict § 12.1):** Q-A verdict's § 1.3 framing-audit Q2 #1 hypothesized W1.13 H1-H5 baseline results might be available. Pattern-A query to gamora returned in ~120 sec with empirical refutation — H1-H5 has NOT been run; gamora seam idle post-LC-011; three upstream prerequisites unmet. Cycle: Pattern-A query → ~120 sec surface → ~30 min addendum capture → framework intactness preserved → no Pattern-B dispatches fired against bad-assumption scope.
>
> **When to cite:** Pattern A-deep verdict authoring (mandatory); math-hotspot methodology consultation (mandatory per Discipline #18); critique-pair Gate-1 reviews (recommended); recognition-validate-commit cycle gates.
>
> **Authority:** Gandalf surface 2026-05-23; first applied use Q-A verdict § 1.3 + § 12.1 demonstration.

---

## 4. Discipline #18 amendment — Methodology-consultation timing at extension hotspots

**Source:** Q-A verdict § 12.4 (gamora Pattern-A query surface, 2026-05-23 evening); gandalf OP § 4.2.

**Operational origin:** Q-A verdict scoped legolas Mode A consultation BEFORE gamora executes H8/H9. Gamora surface revealed H1-H5 baseline hasn't run; therefore legolas would consult without empirical signal-to-noise data from baseline. Refinement: at extension hotspots, consultation fires AFTER baseline lands.

**Proposed canonical text (as amendment to existing Discipline #18):**

> ### Discipline #18 amendment — Methodology-consultation timing at extension hotspots (2026-05-23 refinement)
>
> Discipline #18 (methodology-before-execution at math hotspots) preserves its principle: methodology consultation required BEFORE specialist execution.
>
> **Refinement:** at **extension-of-existing-framework math hotspots** (where the extension builds on a baseline framework whose empirical results inform the extension's methodology choice), methodology consultation for the extension fires AFTER the baseline framework's empirical results land where possible, not before. Empirical signal-to-noise data from baseline informs extension methodology choice. Consultation-in-the-dark on extensions is the failure mode this refinement guards against.
>
> **Example:** BDI H8/H9/H8.diff (Q-A verdict extensions of BDI H1-H5 framework) — legolas Mode A consultation fires AFTER H1-H5 baseline lands from gamora, with effect sizes + variance + signal-to-noise data available; THEN consultation produces methodology recommendations grounded in empirical baseline rather than projected scale estimates.
>
> **When to cite:** any math-hotspot methodology consultation that extends an existing framework's hypothesis tests; any case where baseline empirical data exists or is imminent.

---

## 5. Discipline #18 or #23 — Semantic-layer rep-audit (Discipline #18 amendment candidate OR new discipline)

**Source:** `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` § 2.4 (meta-record from 9.11-G work); gandalf OP § 4.4.

**Operational origin:** Phase E-2 cluster labeling + 9.11-G marginal-lineage records surfaced that substrate-tagging cross-contamination produces clusters that pass geometry-purity gates (94.4% purity on Cluster 87) but contain Mode-B-content (Modern Argentine military firearms tagged south_american_indigenous geographically). Substrate-led discipline catches this at geometry layer but NOT at semantic layer.

**Proposed canonical text** (jack-ryan decides whether this is a Discipline #18 amendment OR new Discipline #23):

> ### Discipline #18 or #23 — Semantic-layer rep-audit (substrate-vote binding asymmetry)
>
> The substrate's vote is binding **at the geometry layer** (clustering algorithm output) but NOT necessarily binding **at the semantic layer** (cultural-tradition interpretation of cluster identity). Semantic-layer use of substrate output requires rep-audit at firing.
>
> **Operational check at every semantic-inheritance decision:**
> - Pull top-5 hdbscan_native reps (or equivalent representative sample) for the candidate cluster
> - Verify reps match the semantic interpretation the downstream design surface inherits
> - If reps contradict interpretation (e.g., cluster labeled "S. American Indigenous Contemporary Shotgun Cluster" at 94.4% purity has reps = Modern Argentine/Brazilian military firearms), do NOT inherit the cluster's lineage tag as cultural-tradition substrate
> - Document the rep-audit finding in receiving artifact's notes
>
> **The 4-mode tagging-vocabulary collapse pattern** (per marginal-lineage meta-record § 1.1):
> - Mode A (intended): weapon-making cultural tradition of origin
> - Mode B (artifact): geographic region of origin or deployment
> - Mode C (artifact): naming-allusion to an indigenous people in a modern-context item
> - Mode D (artifact): cross-tagged metadata error
>
> Rep-audit catches Mode B/C/D content that lineage-purity score alone passes.
>
> **When to cite:** any downstream design surface that inherits cluster identity as cultural-tradition substrate; any Fate-genre faction-architecture work; any Phase E-3 cluster-as-design-surface mapping; any T4-B catalogue substrate-anchoring decision; any cohesion-judge LLM-naming pass on substrate-tagged input.

---

## 6. Discipline #19 amendment — Cheapest-refuting-test-per-claim-type (operationalization)

**Source:** KR #2 § 8.7 tracking-doc + marginal-lineage meta-record § 2.4 + KR #1 9.11-G work + KR #2 Observation 6.

**Operational origin:** Discipline #19 (forensic-conclusion-discipline) was scoped to require named cheapest-refuting-test per claim. KR #2 + jack-ryan operationalization clause fold specified per-claim-type defaults: memory → psutil RSS-check; methodology → next-tier-larger sample run; substrate → SQL count; cross-seam → schema diff. This amendment captures the operationalization at canonical layer.

**Proposed canonical text (as amendment to existing Discipline #19):**

> ### Discipline #19 amendment — Cheapest-refuting-test-per-claim-type (2026-05-23 operationalization)
>
> Discipline #19 (forensic-conclusion-discipline) preserves its principle: forensic claims must name the cheapest refuting test that could falsify them.
>
> **Operationalization (per-claim-type defaults surfaced through 2026-05-23 work cycle):**
>
> | Claim type | Cheapest refuting test |
> |---|---|
> | Memory / resource consumption | `psutil` RSS-check polling during execution; OS panic-log inspection post-incident |
> | Methodology effect-size at scale | Next-tier-larger sample run; sample-size analysis with effect-size target |
> | Substrate count / coverage | SQL count query against authoritative source; row-level spot-sample |
> | Cross-seam contract | Schema diff between producing seam output and consuming seam input expectation |
> | Framing assumption (per Discipline #22 framing-audit) | Pattern-A query to seam owner; rep-audit on substrate output; quick targeted diagnostic |
> | Cluster semantic interpretation | Top-N rep-audit per Discipline #23 semantic-layer rep-audit |
>
> Forensic claims without a named per-claim-type refuting test are **forensic hypotheses**, not forensic conclusions. The discipline forbids stamping a hypothesis as conclusion in handoff documents, status reports, or commit messages.
>
> **When to cite:** every forensic claim in incident triage; every handoff that asserts a state without empirical verification; every status report at sub-agent invocation; every Pattern A-deep verdict authoring (cite as the empirical-evidence criterion behind each claim).

---

## 7. Cross-cutting team-wide propagation requirements

These six disciplines need propagation across all agent OPs after canonical write lands. **This proposal does not itself propagate** — it surfaces the discipline texts for jack-ryan canonical capture. Per-agent OP propagation is item 3 (separate proposal).

| Agent | Disciplines needing OP propagation |
|---|---|
| jack-ryan | All 6 (including her own intake) |
| rocket | All 6 |
| gamora | All 6 |
| star-lord | All 6 |
| elrond | All 6 |
| galadriel | All 6 |
| drax | All 6 |
| legolas | All 6 |

Gandalf + knight-rider already have all 6 in their OPs (gandalf at OP §§ 3.5 / 3.6 / 4.1-4.6; knight-rider at KR OP via self-correction commit 1a7b16a + KR #2 tracking-doc cross-references). The other 8 agents are unaware.

---

## 8. Sequencing relative to P1 hive-mind

These canonical writes gate P1 hive-mind sub-agent fan-out quality. Without them:
- Sub-agent invocations during P1 hive-mind risk repeating KR #1 EOD-handoff violation pattern
- Framing-audit checklist isn't operational across all sub-agents
- Semantic-layer rep-audit isn't operational at downstream cluster-consuming work
- Methodology-consultation-timing refinement isn't operational at legolas Mode A invocations

**Recommended sequencing per gandalf P1 hive-mind prep recommendation:**

1. Jack-ryan invoked for canonical write at engineering-disciplines.md (this proposal as starting point)
2. Per-agent OP propagation fires (item 3 proposal forthcoming)
3. Hive-mind protocol amendment incorporates the new disciplines (item 4 forthcoming; gandalf authoring)
4. P1 hive-mind fires post-(1)+(2)+(3)+T4-B catalogue lock+weapon-substrate-conclusion

---

## 9. What this proposal does NOT do

- Does not write engineering-disciplines.md directly (jack-ryan owns canonical write authority)
- Does not commit the proposed disciplines to specific numbering (#20, #21, etc. are suggestions; jack-ryan decides final placement + numbering per existing canon house style)
- Does not propagate to per-agent OPs (separate work-unit — item 3 proposal)
- Does not amend the hive-mind protocol (separate work-unit — item 4)
- Does not pre-commit to "semantic-layer rep-audit is a Discipline #18 amendment vs new #23" — jack-ryan decides

---

## 10. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct instruction to surface team-wide discipline propagation as item 2 of P1 hive-mind preparation
**Status:** Proposal — jack-ryan reviews + amends engineering-disciplines.md.
**Routing:** Via knight-rider to jack-ryan when next invocation fires.

---

**Signed:** gandalf
**For:** the six discipline-canonical-write proposals jack-ryan integrates at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`. Suggested verbatim text + sourcing pointers + numbering proposals; jack-ryan refines per canonical house style + commits canonical write.
