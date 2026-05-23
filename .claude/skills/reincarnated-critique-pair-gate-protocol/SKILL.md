---
name: reincarnated-critique-pair-gate-protocol
description: Use this skill when authoring dispatches, invoking Gate 1 (DESIGN-MODE pre-fire review) or Gate 2 (DEV-MODE post-output review with BLOCK authority), applying critique-pair Pattern E autonomous-pair ratification under Matt pre-authorization, or in critique-pair-adjacent work. Captures critique-pair structure (gandalf design + jack-ryan process), 5 review principles (math-before-code + smoke-gate + cross-seam impact + decisions-log as truth + severity matters + cross-seam round-trip + catalogue per-product-line register), Gate 1 / Gate 2 framework with common catches + finding-file format + severity classification (INFO/WARN/BLOCK), dispatch patterns A/B/C/E in critique-pair sense, Pattern-letter terminology disambiguation (critique-pair Pattern A vs OP Pattern A), ADR-002 tiered approval table.
version: 0.1.0
---

# reincarnated-critique-pair-gate-protocol — Cross-cutting Reference Skill

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — Stream 3 cross-cutting reference skill per `canonical/02-roadmap.md` § 2.2
>
> **Skill packaging:** Markdown source for the eventual installable skill `reincarnated-critique-pair-gate-protocol` (per doc 38 § 4 step 2 + Skill Creator pass).

**Authored:** 2026-05-23
**Author:** gandalf (cross-cutting Stream 3 authoring; co-owned with jack-ryan as critique-pair members)
**Authoritative sources:**
- `agentic_orchestration/REVIEW_PROCESS.md` (5 review principles + Gate 1 / Gate 2 framework)
- `agentic_orchestration/dispatches/README.md` (dispatch authoring template)
- `agentic_orchestration/GOVERNANCE.md` (founding ADRs; ADR-002 tiered approval authority)

**Pattern:** universal reference wrapper; load when authoring or reviewing dispatches, when invoking Gate 1 / Gate 2, when applying critique-pair Pattern E under Matt pre-authorization, or when in critique-pair-adjacent work
**Companion skills:** `reincarnated-engineering-disciplines`; `reincarnated-decision-log-format`; `reincarnated-canonical-doc-format`; `reincarnated-hive-mind-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** the universal reference for the critique-pair structure (gandalf + jack-ryan as paired critique members), Gate 1 (DESIGN-MODE) and Gate 2 (DEV-MODE) review framework, the 5 review principles, the dispatch patterns (A/B/C/E in critique-pair sense), and the autonomous-pair ratification protocol under Matt pre-authorization. Loaded by any agent authoring a dispatch, invoking a gate, OR being sub-agent invoked by jack-ryan / gandalf for critique-pair review.

**IS NOT:** the substantive principles themselves (those live in `REVIEW_PROCESS.md`; ALWAYS the canonical source). NOT the per-agent OP discriminator for Pattern A-light vs Pattern A-deep (that's per-agent OP language; this skill clarifies the critique-pair sense vs the OP sense — see § 6 for terminology disambiguation). NOT the dispatch authoring template (that's `dispatches/README.md`).

---

## 1. The critique-pair structure

**Members:** gandalf (design steward) + jack-ryan (process gatekeeper).

**Role asymmetry:**
- **jack-ryan** owns process-side critique — Gate 1 (DESIGN-MODE peer) + Gate 2 (DEV-MODE gatekeeper with BLOCK authority); decisions-log writing authority
- **gandalf** owns design-side critique — thematic / experiential / design-coherence pushback; story/lore coherence; canonical-doc authoring

**Pairing:** when a decision warrants both process AND design critique, both members invoked (in parallel when independent; sequentially when one's output is the other's input).

**Outside the pair:** Matt (final approval); knight-rider (orchestration; routes critique-pair invocations; NOT a critique-pair member).

---

## 2. The 5 review principles (REVIEW_PROCESS.md § 1)

Every Gate 1 and Gate 2 review applies these:

| # | Principle | Gate 1 question | BLOCK trigger |
|---|---|---|---|
| 1 | **Math-before-code on non-trivial changes** (Discipline #1) | "What math did you do before coding this?" | Implementation without math justification |
| 2 | **Smoke-gate before commit** (Discipline #2) | "Where's the smoke-test output for this commit?" | Commit without smoke-test evidence + no skip-reason |
| 3 | **Cross-seam impact called out** (ADR-004 + Discipline #12) | "Does this change touch any consumer's interface?" | Cross-seam change without MIGRATION.md before tagging |
| 4 | **Decisions-log is single source of truth** | "Which decisions-log entry justifies this approach?" | Implementation that conflicts with locked decision without superseding |
| 5 | **Severity matters; escalation is normal** (INFO < WARN < BLOCK) | (applies per-finding) | (escalation classification, not a gate trigger) |
| 6 | **Cross-seam contract changes require round-trip discipline** | "Does this dispatch include a cross-seam round-trip smoke test OR explicit not-applicable justification?" | Cross-seam contract change with neither clause in acceptance criteria |
| 6b | **Catalogue dispatches require per-product-line register validation** (soft gate) | "Does this catalogue dispatch instruct per-product-line `deliverable_register` recording?" | WARN only (not BLOCK); risk accumulates over time |

---

## 3. Gate 1 — DESIGN-MODE (pre-fire review)

**When:** knight-rider authors a dispatch; before firing to a specialist
**Mode:** jack-ryan as peer collaborator with knight-rider (NOT gatekeeper); gandalf may be invoked in parallel for design-side concerns
**Output:** PASS / PASS-WITH-AMENDMENTS / BLOCK (with rationale + remediation if BLOCK)
**Time:** fast (~2 min for routine dispatches; longer for novel architecture)
**Goal:** catch process violations before they become work-blocking at Gate 2

**Common Gate-1 catches:**
- Missing math justification (Principle 1)
- Conflict with decisions-log (Principle 4)
- Ambiguous cross-seam scope (Principle 3)
- Cross-seam contract change without round-trip discipline (Principle 6)
- LLM prompt-construction site exposing internal schema labels (Discipline #14)
- Outcome-attribution claim without ablation evidence (Discipline #13b)

**Routing:** knight-rider invokes jack-ryan as sub-agent OR Matt approves directly when Gate-1 review skipped (Matt has authority to skip; typical for routine pattern-reproducing work)

---

## 4. Gate 2 — DEV-MODE (post-output review)

**When:** specialist ships a commit to `agentic_orchestration/qa/pending/`
**Mode:** jack-ryan as gatekeeper with BLOCK authority
**Output:** finding file at `agentic_orchestration/qa/findings/<date>-<work-item>.md` with severity (INFO / WARN / BLOCK) + rationale + action
**Time:** batched (typically every few hours OR before any milestone tag)
**Goal:** catch discipline violations + drift before milestone tag

**Common Gate-2 findings:**
- Smoke-test output missing on commit (Principle 2)
- MIGRATION.md missing on cross-seam touch (Principle 3)
- Cross-seam round-trip evidence missing (Principle 6)
- Decisions-log update missing on architectural lock
- Discipline #10 attribution violation (multiple things changed; can't isolate effect)

**Severity:**
- **INFO** — note for archaeology; no remediation required
- **WARN** — remediation suggested; not blocking ship
- **BLOCK** — remediation required before milestone tag fires; Matt-only override

---

## 5. Critique-pair dispatch patterns (A / B / C / E)

Per hive-mind-protocol § 5 + dispatches/README.md precedents:

### Pattern A — Design + Implementation critique (parallel)

Specialist implements; another specialist (or gandalf for design dimension) critiques in parallel. Used when execution is well-scoped but design or methodology dimension warrants concurrent review.

**Example:** P1.5 feature extraction — rocket implements; gandalf reviews feature-class coverage; legolas Mode A reviews methodology rigor.

### Pattern B — Spec + Review (Gate-1 dispatch pattern)

Specifier authors dispatch spec; reviewer (typically jack-ryan in DESIGN-MODE) reviews BEFORE execution fires. Standard Gate-1 invocation.

**Example:** P2 axis discovery — elrond authors math note + dispatch; jack-ryan Gate-1 review (Discipline #1, #11, #18 compliance); Matt amendments; FIRE-READY.

### Pattern C — Critique-pair memo (sustained dialogue)

Sustained design dialogue captured as memo. Used for design-call phases (P4 cluster labeling) and per-iteration learnings.

**Example:** P4 cluster semantic labeling — gandalf + Matt design call; jack-ryan reviews artifact post-session.

### Pattern E — Critique-pair Gate-2 ratification (autonomous-pair)

Under Matt pre-authorization, jack-ryan + gandalf can ratify minor closeouts WITHOUT Matt direct approval. Used for cumulative closeouts where the substantive work is already complete and the critique-pair concurs.

**Example:** W0.7 cumulative Gate-2 close-out 2026-05-22 (per `agentic_orchestration/dispatches/2026-05-22-critique-pair-post-recovery-w07-gate2-w113-rescope-p0-close.md` § 2).

**Pre-authorization required.** Matt must explicitly authorize Pattern E for the specific scope before critique-pair ratifies.

---

## 6. Terminology disambiguation — Pattern A in different contexts

Pattern letters are used differently across docs. Disambiguating:

| Context | Pattern A means |
|---|---|
| **Critique-pair (this skill § 5, hive-mind-protocol § 5)** | Design + Implementation parallel critique |
| **Per-agent OP § 2 (gandalf, jack-ryan, others)** | Sub-agent invocation by knight-rider; split into Pattern A-light (≤200 words inline) and Pattern A-deep (file artifact verdict) |

**Resolution:** when in doubt, name the context explicitly. "Critique-pair Pattern A" vs "OP Pattern A" disambiguates clearly. Both usages are durable — they describe different work shapes and don't conflict in practice.

Similarly:
- **Pattern B (critique-pair)** = Spec + Review (Gate-1 dispatch pattern)
- **Pattern B (gandalf OP)** = sustained terminal dialogue with Matt

Always name the context.

---

## 7. When to load this skill

| Trigger | Load |
|---|---|
| Authoring a dispatch | Always (Principle 1-6 govern; Gate-1 review may fire) |
| Invoking Gate 1 review | Always (jack-ryan in DESIGN-MODE) |
| Invoking Gate 2 review | Always (jack-ryan in DEV-MODE with BLOCK authority) |
| Pattern E ratification (autonomous-pair) | Always (Matt pre-authorization required) |
| Critique-pair sub-agent invocation | Always |
| Routine within-seam work with no cross-seam touch | Optional |

---

## 8. ADR-002 tiered approval authority (quick reference)

Per `agentic_orchestration/GOVERNANCE.md`:

| Decision type | Approver |
|---|---|
| Routine within-seam implementation | Specialist directly |
| Cross-seam contract change | Matt (per Principle 3 + ADR-004) |
| Architectural commitment | Matt |
| Discipline ratification | Matt (jack-ryan recommends) |
| Milestone tag | Matt |
| Intermediate tag (per-seam prefix) | Specialist directly |
| Decisions-log entry | jack-ryan writes; Matt approves architectural ones |
| Canonical doc authoring | gandalf primary; jack-ryan reviews process-side |
| Pattern E ratification (autonomous-pair) | jack-ryan + gandalf under Matt pre-authorization |

---

## 9. Update protocol for this skill

This skill evolves when:
- A new principle is ratified (extend § 2 with row)
- A new pattern letter is established (extend § 5)
- A new ratification protocol lands (extend § 5 / § 8)
- Gate cadence changes
- ADR-002 authority table updates

Authored / maintained by **gandalf** (cross-cutting Stream 3 owner) co-owned with **jack-ryan** (critique-pair process side); jack-ryan reviews process amendments before commit.

---

**Signed:** gandalf (cross-cutting Stream 3 reference-skill author; co-owned with jack-ryan)
**For:** the universal reference for critique-pair structure (gandalf + jack-ryan), Gate 1 (DESIGN-MODE) and Gate 2 (DEV-MODE) review framework, the 5 review principles, the dispatch patterns (A/B/C/E in critique-pair sense), the autonomous-pair ratification protocol, ADR-002 tiered approval authority, and Pattern-letter terminology disambiguation across contexts. Authoritative source for substantive principle definitions remains `agentic_orchestration/REVIEW_PROCESS.md`.
