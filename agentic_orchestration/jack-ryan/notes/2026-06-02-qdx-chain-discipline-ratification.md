# QDX-8 wave-close — jack-ryan discipline ratification reasoning + non-ratified candidates

**Author:** jack-ryan
**Date:** 2026-06-02
**Authority:** jack-ryan discipline-canonical-write authority per AGENTS.md + GOVERNANCE.md ADR-002
**Companion write:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (amended same session)
**Cycle:** Cycle 17 QDX QD-Engine Workflow Re-Fire (wave-close QDX-8)
**Scope:** Ratification evaluation for 5 discipline candidates (#56 through #60) surfaced across QDX chain execution

---

## Summary disposition

| Candidate | Status | Outcome |
|---|---|---|
| #56 — Generator-path explicit naming | RATIFIED | Written to engineering-disciplines.md |
| #57 — Genre-aligned distribution | RATIFIED | Written to engineering-disciplines.md |
| #58 — LOCK Q ADDITIVE-ONLY zero-semantic-amendment | DECLINED (redundant) | Third founding instance added to #53 anatomy entry |
| #59 — Substrate-coverage as binding quality constraint | RATIFIED | Written to engineering-disciplines.md |
| #60 — LOCK O escape-clause-as-discipline | QUEUED | One instance; empirical-evidence trigger named below |

---

## Per-candidate rationale

### Candidate #56 — Generator-path explicit naming — RATIFIED

**Evidence sufficiency:** Three founding instances across two chains. EAA-5 v1 BLOCK (root cause was a silent BcTargetSubspaceGenerator assumption — dispatched as "fire the QD-engine workflow Phase 2" without naming the generator; 25/25 physical kits / empty skills / zero LLM calls). QDX-4 supplement (jack-ryan explicitly named the pattern, produced Options A/B/C, recommended Matt-touch as ADR-002 tier-1 architectural decision). QDX-5 dispatch (first explicit naming, satisfying the discipline before it was written).

**Composes cleanly with existing disciplines:** #41 (substrate-led) and #54 (integration-smoke-gate) both already operate at the generator-path question; #56 closes the upstream documentation gap that makes both auditable.

**No redundancy:** no existing discipline requires dispatch-level generator-class naming. The closest is #54 ("generator path is correct" as smoke criterion 1) but that is a verification gate, not a naming requirement.

**Does it generalize?** Yes. As the engine adds further generator implementations (future BcTargetSubspaceGenerator enrichment, potential hybrid generators), this discipline becomes more valuable, not less.

**RATIFIED.** Canonical write per authority.

---

### Candidate #57 — Genre-aligned distribution — RATIFIED

**Evidence sufficiency:** One empirical result (QDX-5: 43.2%/56.8%) but backed by Matt + gandalf Pattern B verbatim ratification, which is the architectural-authority level for design-philosophy disciplines. The gandalf transmission explicitly named this as a discipline candidate. The 40-45%/55-60% target is grounded in ARPG/JRPG genre precedent (PoE, FF, Diablo archetype distribution norms), not derived from internal telemetry — it is a design-intent ratification, not an empirically-discovered constraint.

**Does it generalize?** Yes. Every future kit-space-expansion fire will set element distribution parameters. Without this discipline, each fire will re-derive the genre convention question from scratch or default to uniform distribution (which Matt explicitly rejected).

**Boundary with Discipline #41:** non-overlapping. #41 governs substrate-led fill within element axis; #57 governs element-axis coverage across the roster. The QDX-5 ratification explicitly stated both apply: "substrate determines fill WITHIN each element axis; element-axis follows genre-convention distribution target."

**RATIFIED.** Canonical write per authority.

---

### Candidate #58 — LOCK Q ADDITIVE-ONLY zero-semantic-amendment integration — DECLINED (redundant)

**Evidence:** QDX-1/2/3 all delivered ADDITIVE-ONLY across three seams. Zero semantic amendments to existing public APIs. Backward-compat verified at each step. The discipline pattern is real and was exercised.

**Why not a new number:** Discipline #53 already covers ADDITIVE-AND-REVERSIBLE pre-commitment via ADDITIVE-ONLY discipline. The ADDITIVE-AND-REVERSIBLE heuristic (three questions: Is it additive? Does it preserve existing semantic behavior? Is it reversible?) is precisely the discipline QDX-1/2/3 exercised under LOCK Q. Creating #58 would be: "three seams respected #53's heuristic at QDX scale" — which is a founding instance of #53, not a distinct pattern.

**Action:** third founding instance recorded in #53 anatomy section and scope note. LOCK Q is named as the chain-level instantiation.

**DECLINED as new numbered discipline.**

---

### Candidate #59 — Substrate-coverage as binding quality constraint — RATIFIED

**Evidence sufficiency:** Three-chain empirical pattern with four qualifying instances. The pattern appeared independently in EAA-5 v1 (substrate constraint disguised as pipeline defect until root-cause analysis), QDX-4 (jack-ryan supplement explicitly introduced the "pipeline sound; substrate thin" framing), QDX-5 WARN 4 (substrate constraint produced measurable quality deficits: 24.3% fallback name rate, 11% T4 null rate, identical BC axis on all 16 physical kits), and QDX-6 strategic signal (strategic investment diagnosis quantified as "highest-leverage next-cycle investment").

**Is it load-bearing?** Yes. Without this discipline, there is a structural risk that future generation quality deficits (e.g., post-elrond-enrichment validation revealing remaining gaps) get treated as pipeline defects requiring code iteration — wasting cycles on correct code while the actual substrate gap persists. The discipline closes this misclassification risk.

**Composes cleanly:** #39 (no-synthetic-stub) prohibits the wrong response; #41 (substrate-led) establishes the correct architectural posture; #59 provides the diagnostic protocol for the quality-assessment moment when a gap is observed.

**Does it generalize?** Yes. As the kit space grows and enrichment occurs in waves, quality assessments will recur. The three-question diagnostic applies regardless of which substrate dimension is thin.

**RATIFIED.** Canonical write per authority.

---

### Candidate #60 — LOCK O escape-clause-as-discipline — QUEUED

**The one founding instance (QDX-7):**
drax explicitly deferred faction grouping in the loadout app because the per-kit `faction_id` field does not exist in the QD-engine workflow output schema. The deferred scope was correctly documented (LOCK O escape clause invocation; "engine needs per-kit faction_id field"). drax's session recorded the deferral cleanly with an explicit engine gap named.

**Why one instance is insufficient for ratification:**
The escape-clause-as-discipline pattern would generalize to: "when a MVP-discipline (LOCK O or equivalent) dispatch explicitly defers a feature citing a missing engine field, the deferral is the correct response — NOT adding the engine field as an out-of-scope scope creep OR implementing a fragile workaround." That is a real discipline. But one instance makes it difficult to know whether the characterization is correct. The boundary between "correct deferral" and "scope avoidance" needs a second case to stress-test the framing.

**Empirical-evidence trigger:**
Ratify #60 when a second cross-chain escape-clause activation meets all of:
1. A consumer-side MVP-discipline dispatch (drax, gamora consumer, or equivalent) explicitly invokes an escape clause
2. The deferral names a missing engine field or schema element (not a UX design decision)
3. The deferred feature is subsequently delivered in a follow-on workstream after the engine gap is closed (completing the loop)
4. The pattern is present in at least two independent workstreams (QDX-7 + one more)

Candidate #60 text for future ratification authoring (one-sentence summary): "When a consumer-side MVP-discipline dispatch defers a feature by invoking an escape clause, the invocation is a first-class engineering event — it should name the exact engine gap, record the deferral in the completion record, and route a follow-on workstream flag to KR for the gap-closing engine work."

**QUEUED at `qa/pending/` — no file needed; this note is the queue record.** Route to jack-ryan at next wave-close where a second escape-clause activation qualifies.

---

## Cross-chain lineage for KR wave-close record

The three ratified disciplines (#56 / #57 / #59) should be cited in the QDX-8 canonical story record as:

- **#56:** lineage = EAA chain (candidate 6, EAA-8 harvest) → QDX chain (activation via QDX-4 substrate-coverage signal + QDX-5 generator-path strategic decision) → QDX-8 ratification
- **#57:** lineage = Matt + gandalf Pattern B session 2026-06-02 (Option B4 ratification) → QDX-5 empirical confirmation → QDX-8 ratification
- **#59:** lineage = EAA-5 v1 root cause forensic → QDX-4 substrate-coverage signal → QDX-5 WARN 4 → QDX-6 strategic signal → QDX-8 ratification
- **#53 amendment:** lineage = IA chain founding instances (2026-06-01) → QDX chain third founding instance (2026-06-02; QDX-1/2/3 LOCK Q ADDITIVE-ONLY across three seams)

---

## Notes for gandalf design-quality audit

Disciplines #57 (genre-aligned distribution) and #59 (substrate-coverage binding constraint) both have design-philosophy implications beyond engineering process:

- **#57 implication for gandalf:** the 40-45% physical / 55-60% caster target is now a canonical design constraint on future kit-space-expansion fires. If a future session proposes a different distribution (e.g., higher physical for a "physical warrior season" expansion), that is a ratified-departure moment requiring a gandalf design session, not a seam-level parameter choice.

- **#59 implication for gandalf:** the QDX-6 strategic signal ("elrond substrate-enrichment is the highest-leverage next-cycle investment") is discipline-grounded: #59 names substrate enrichment as the correct response category, and QDX-5 empirically confirmed it. Gandalf may want to reference #59 when framing the elrond substrate-enrichment workstream at the design level — it provides the canonical rationale for why substrate enrichment is prioritized over pipeline iteration.

---

**End of QDX-8 discipline ratification notes.**
