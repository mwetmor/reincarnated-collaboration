# ARCHITECT-Effectiveness Ledger (LIVING)

**STATUS:** LIVING CROSS-SEAM ARTIFACT — born 2026-06-30 (Matt: *"store the results from the jack-ryan invocations against the effectiveness of the Gandalf ARCHITECT role written docs when he follows up on them… complete the loop so that both you and I can derive learnings from this scoring and improve future architecture/design by adding rules as we go along."*).

**What it is:** the **closed learning loop** on gandalf's ARCHITECT-role foresight. Every ARCHITECT pass makes a *falsifiable* claim about a run it gated. After the run executes, **jack-ryan scores whether the foresight held** — and the recurring failure-shapes become new rules that make the next ARCHITECT pass sharper.

**Ownership (the conflict-managed split):**
- **gandalf (CANON-STEWARD, proposer + subject):** authors the ARCHITECT passes being scored; *proposes* this scaffold + rubric; *executes* row-prep (pre-fills the "what the pass claimed" columns). **gandalf does NOT score gandalf.** Scoring gandalf's own foresight would be rule-maker = rule-subject — the developer↔judge signature the role-separation verdict named (`agentic_orchestration/gandalf/notes/2026-06-30-role-separation-verdict.md § 1` cluster III).
- **jack-ryan (disinterested judge, scorer + ratifier):** *owns* the SCORE columns (Coverage / Classification / Utility / Verdict / Miss-log); *ratifies* this rubric (symmetry with jack-ryan owning engineering-disciplines — `canonical-doc-format.md § 6.7`). jack-ryan's grade is the durable one; gandalf's row-prep is just the setup.
- **Matt:** reads the LEARNINGS section at session start/end; approves promotion of a recurring miss-class into a standing ARCHITECT rule.

> **Ratification status:** **RATIFIED by jack-ryan 2026-06-30 with two MANDATORY amendments (folded below)** — `agentic_orchestration/jack-ryan/notes/2026-06-30-governance-ratification-s15-and-architect-ledger.md` + two decisions-log entries. The four dimensions, the miss-class enum, and the ≥2 promotion threshold stand as proposed. The amendments close the same leak both governance items had: the escape-hatch (a substrate-emergent excuse) must be **earned by reference-checkable evidence, not granted by the rule-subject's assertion.** Cross-ref: `matt_decision_needed/` is the *decision* queue; this is the *foresight-quality* ledger. Different instruments.
>
> **jack-ryan MANDATORY amendments (2026-06-30):**
> - **M1 — pre-run-knowability discriminator (closes the carve-out loophole).** A miss is `unforeseeable_substrate_emergent` **only if it required a NAMED run-produced empirical result** that could not exist pre-run. If the scorer cannot name that input, the miss **defaults to `foreseeable_missed`.** Ambiguity resolves *against* the rule-subject (gandalf), never for. Without this, "substrate-emergent" becomes a blanket excuse for real foreseeable misses.
> - **M2 — scorer framing-audit reflex (Discipline #42).** Before reading gandalf's pre-prepped CLAIM columns, **jack-ryan independently re-derives the decision list from canon.** This prevents the CLAIM pre-prep from anchoring the score — the scorer's decision-enumeration must be independent, or the "Coverage" metric measures gandalf's self-report, not reality.
> - **INFO (folded):** D1 denominator = *foreseeable* decisions hit (substrate-emergent decisions sit outside the ratio, neither credit nor debit); a ≥2 promotion cluster must share a **root-shape**, not merely the same enum tag; D3 Utility stays qualitative (not forced numeric).

---

## The loop (4 steps)

1. **gandalf fires an ARCHITECT pass** (`▶ ROLE: ARCHITECT`) at a run-authorization boundary (or on Matt's explicit "ARCHITECT pass on X" handle — OP § 2). The pass runs the **open-questions gate**: enumerate every decision the run will hit → classify each **RESOLVED / GATED+TRACKED (named empirical criterion) / OPEN** → surface OPEN Matt-gated forks to `matt_decision_needed/`. **gandalf pre-preps a ledger row** capturing what the pass *claimed* (the CLAIM columns).
2. **The run executes** — specialists build; jack-ryan Gate-2 reviews the build.
3. **jack-ryan follows up** (at Gate-2 or a dedicated pass) and **scores the ARCHITECT pass against what the run ACTUALLY hit** — filling the SCORE columns + the Miss-log. This is the "jack-ryan invocation results" Matt named.
4. **Patterns across rows** (recurring miss-classes) → **candidate rules** in the LEARNINGS section → Matt approves → the rule folds into the ARCHITECT-pass discipline (OP § 2 / § 4). The loop tightens.

**The falsifiable claim an ARCHITECT pass makes** (what the score tests):
- **Completeness:** "these are ALL the design/Matt-gated decisions this run will hit." → falsified by a decision the run hit that the pass didn't list.
- **Classification:** "each listed decision is correctly RESOLVED / GATED+TRACKED / OPEN." → falsified by a RESOLVED item that re-opened, or a GATE whose empirical criterion was wrong.
- **Prioritization:** "the run can safely fire with the OPEN items gated, not blocking." → falsified by the run stalling on a gated item, or a mis-gated item that blocked/mis-steered it.

---

## The rubric (jack-ryan scores; gandalf-proposed, PENDING ratification)

| Dimension | Tests which claim | Score |
|---|---|---|
| **D1 — Coverage** | Completeness | `foreseen ÷ FORESEEABLE decisions the run hit` (per jack-ryan INFO — substrate-emergent decisions sit outside the ratio). 1.0 = the pass listed every foreseeable decision the run hit. Scorer re-derives the decision list from canon *independently* before reading gandalf's CLAIM (M2). |
| **D2 — Classification accuracy** | Classification | of the foreseen decisions, fraction correctly classed (RESOLVED didn't re-open; GATE criterion held; OPEN genuinely needed Matt). |
| **D3 — Utility** | Prioritization | did the gate prevent stalls? Did the run fire cleanly on the gated set, or did a mis-gated item block / mis-steer it? (qualitative + stall-count) |
| **Verdict** | roll-up | **HELD** (foresight substantially complete; no expensive misses) / **PARTIAL** (useful but material misses) / **DRIFTED** (missed decisions that stalled or mis-steered the run). |

**The Miss-log carries the learning.** For every decision the run hit that the pass **missed** or **mis-classed**, jack-ryan logs a row tagged with a **miss-class** (the extensible enum below — grows like the OP § 4.3 flag enum). Recurring miss-classes are what get promoted to rules.

**Miss-class enum (starter — extensible):**

| Miss-class | Meaning | Is it a foresight failure? |
|---|---|---|
| `unforeseeable_substrate_emergent` | the decision only surfaced because substrate voted unpredictably | **NO** — substrate-led discipline says this is expected; NOT a demerit |
| `foreseeable_missed` | the decision was knowable pre-run from canon/spec; the pass should have caught it | **YES — the core learning case** |
| `misclassed_resolved_reopened` | pass marked RESOLVED; the run re-opened it | YES |
| `misclassed_gate_criterion_wrong` | pass GATED+TRACKED but named the wrong empirical criterion | YES |
| `misprioritized_gated_but_blocked` | pass judged safe-to-gate; the item actually blocked the run | YES |
| `scope_boundary_error` | the decision belonged to a different run/seam than the pass assumed | YES |

**Discipline:** `unforeseeable_substrate_emergent` misses do NOT count against the ARCHITECT pass — foreseeing substrate emergence would violate the very substrate-led discipline the project runs on. Only the *foreseeable* miss-classes drive rule-generation. A pass that "missed" only substrate-emergent decisions still scores **HELD**. **Guard (jack-ryan M1):** a miss earns the `unforeseeable_substrate_emergent` tag ONLY if jack-ryan can name the run-produced empirical result it required; absent that named input, the miss **defaults to `foreseeable_missed`** (ambiguity resolves against gandalf, never for). The carve-out is earned by evidence, not granted by assertion.

---

## THE LEDGER (one row per ARCHITECT pass; gandalf pre-preps CLAIM, jack-ryan fills SCORE)

| # | ARCHITECT pass (date + run gated) | CLAIM: decisions listed / resolve-gate-open split | SCORE: D1 / D2 / D3 | Verdict | Miss-log (jack-ryan) |
|---|---|---|---|---|---|
| — | *(none yet — the ARCHITECT role-tag was created 2026-06-30 this same session; no ARCHITECT pass has yet gated a run. First entry lands when the first sustained run is ARCHITECT-gated and then jack-ryan-scored.)* | — | — | — | — |

> **Honesty note (survey-mode):** born empty on purpose. No ARCHITECT pass has fired against a run yet, so there is nothing real to score. Fabricating a retro-entry would poison the loop's first data point. The **first genuine candidate** is likely the perception-asymmetry dispatch (`matt_decision_needed/` Q1) — *if* Matt authorizes it as a run, it should be ARCHITECT-gated first, then this ledger gets row #1 when jack-ryan follows up at its Gate-2.

---

## LEARNINGS → RULES (the payoff — Matt + gandalf read; Matt approves promotion)

*Recurring miss-classes graduate here into candidate standing rules for future ARCHITECT passes. Empty until the ledger has enough rows to show a pattern (≥2 instances of the same foreseeable miss-class = a candidate rule). Each promoted rule cross-refs into OP § 2 (ARCHITECT trigger) or § 4 (operational protocols).*

| Candidate rule | Driven by (miss-class × N) | Status |
|---|---|---|
| *(none yet — needs ≥2 rows showing a repeated `foreseeable_missed` / mis-class pattern)* | — | — |

**Promotion protocol:** a miss-class recurring ≥2× → gandalf drafts a candidate rule ("ARCHITECT passes must additionally check X before gating") → jack-ryan reviews (disinterested) → Matt approves → rule folds into OP § 2/§ 4 + this table marks it PROMOTED with the OP cross-ref. This is Matt's "adding rules as we go along."

---

**Cross-references:**
- `agentic_orchestration/operating-procedures/gandalf.md § 2` — the ARCHITECT role-tag, its run-authorization-boundary trigger, and the open-questions gate this ledger scores
- `agentic_orchestration/gandalf/notes/2026-06-30-role-separation-verdict.md § 1` (cluster III) + `§ 3` — why gandalf proposes but jack-ryan scores (rule-maker ≠ rule-subject)
- `agentic_orchestration/operating-procedures/canonical-doc-format.md § 6.7` — governance rule-ownership routes to jack-ryan (the symmetry this ledger inherits)
- `canonical/matt_decision_needed/` — the *decision* queue the ARCHITECT pass feeds (this ledger scores the *foresight*, not the decisions)

**Signed:** gandalf (CANON-STEWARD, proposer), 2026-06-30. Scaffold proposed; **scoring + ratification owned by jack-ryan.** The queue tracks what Matt owes; the trackers track what the work owes; this ledger tracks *how good gandalf's foresight was* — and turns its own misses into the next season's rules.
