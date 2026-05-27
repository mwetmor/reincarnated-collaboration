# Framing-Audit Discipline — Candidate (Discipline #42)

> **STATUS:** CURRENT — gandalf-authored discipline candidate. Matt 2026-05-27 ratified the underlying orientation shift (Quality-Orientation Shift Five-Moves Package Move 2). Routes to jack-ryan for canonical-write at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #42.

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "commit to all 5 moves; sequence per your recommendation" per quality-orientation-shift package
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-quality-orientation-shift-five-moves-package.md` (parent package; Move 2 deliverable)
- `.claude/agents/gandalf.md` OP § 4.1 (Pattern A-deep three-question framing-audit precedent — this candidate generalizes it to all sub-agents)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (target for canonical-write)

---

## 0. TL;DR

**Discipline #42 candidate — Framing-audit at sub-agent dispatch consumption.**

Before executing any dispatch, sub-agents run a three-question framing-audit against the dispatch's load-bearing assumptions. If the audit surfaces refutation evidence sufficient to reframe the work, sub-agent files a Framing-Refusal (Discipline #44 candidate — Move 3 deliverable) rather than executing the work as-framed.

This generalizes the Pattern A-deep three-question framing-audit (gandalf OP § 4.1, established 2026-05-23) to ALL sub-agent dispatch consumption — not just gandalf Pattern A-deep verdicts.

---

## 1. Discipline statement (proposed canonical text)

> **Discipline #42 — Framing-audit at sub-agent dispatch consumption.**
>
> Before executing any dispatch, sub-agents MUST run the three-question framing-audit:
>
> - **Q1:** What load-bearing framing assumptions does this dispatch depend on?
> - **Q2:** What evidence currently in hand (or surfaceable in current scope) could refute these assumptions?
> - **Q3:** If refutation evidence exists or is plausible from current scope, is the right move to refine the framing rather than execute the work as-framed?
>
> If Q3 returns YES → sub-agent files a Framing-Refusal (Discipline #44 candidate — Framing-Refusal authority) rather than executing. If Q3 returns NO → sub-agent proceeds with execution, recording in the dispatch's completion artifacts that framing-audit fired and returned NO.
>
> Composes with Discipline #18 (math-before-code at hotspots) — the framing-audit fires at every dispatch; Discipline #18 fires at every math hotspot. Composes with Discipline #40 (scaffold-with-pending-decision) — if the framing-audit surfaces a scaffold value not flagged as pending-decision, sub-agent EITHER executes with flagging OR files Framing-Refusal.

---

## 2. Why this discipline is needed

Three concrete recent failures demonstrate the failure mode (per parent package § 1):

1. **Wave 0.5 Track D content emission** — rocket implemented 12-skill 3-chain 4-tier grid because dispatch said "minimum viable per-skill content." Acceptance criteria met. Game quality not served (locked scaffold drift contradicting doc 40 § 8.3).
   - **Framing-audit Q1 would have surfaced:** dispatch presupposes "minimum viable = 3-chain grid"
   - **Framing-audit Q2 would have surfaced:** doc 40 § 8.3 + D69 + D83 specify variable 3-or-4 chains with branching
   - **Framing-audit Q3 would have returned:** YES — refine framing to "minimum viable + canonical-compliant chain architecture"
   - Cost-avoidance: 1 week scaffold-drift corrective work + Path A revert

2. **Wave 1.5 Stage 2 doc 48 canonical lock** — sub-agent gandalf curated 10-class roster because dispatch said "curate canonical class roster from substrate evidence." Acceptance criteria met. Game quality not served (re-introduced rigid form retired by week's prior work).
   - **Framing-audit Q1 would have surfaced:** dispatch presupposes "classes exist as fixed taxonomy"
   - **Framing-audit Q2 would have surfaced:** substrate-led discipline implies "substrate clusters; design follows"
   - **Framing-audit Q3 would have returned:** YES — refine framing to "should classes be fixed taxonomy OR substrate-emergent?"
   - Cost-avoidance: Path A revert of engine `0a5a4f2` + Stage 3 re-implementation under Option α

3. **The general pattern:** sub-agents inherit dispatch framing faithfully; framing flaws bake into engine code; reverts compound.

---

## 3. Operational hook

**When this discipline fires:**

- At dispatch consumption (every sub-agent receiving a dispatch from KR)
- At session-start (sub-agents resuming work from a prior session check current state against framing-audit)
- At wave-resume (sub-agents resuming mid-wave check whether intervening events changed framing)

**Three-question protocol (verbatim, identical to gandalf OP § 4.1):**

| Q | Question |
|---|---|
| **Q1** | What load-bearing framing assumptions does this work depend on? |
| **Q2** | What evidence currently in hand (or surfaceable in current scope) could refute these assumptions? |
| **Q3** | If refutation evidence exists or is plausible from current scope, is the right move to refine the framing rather than execute the work as-framed? |

**Output recording:**

Sub-agents record framing-audit output in dispatch completion artifacts. Minimum fields:
- Framing-audit fired: yes/no (must be yes; "no" is non-compliance)
- Q1 load-bearing assumptions identified: [list 2-5]
- Q2 refutation evidence: [list or "none surfaced"]
- Q3 outcome: PROCEED / FRAMING-REFUSAL filed at [path]

---

## 4. Composition with related disciplines

### 4.1 Discipline #11 (empirical inspection over assumption)

Framing-audit Q2 IS empirical inspection — sub-agent inspects current-state evidence (canonical docs, substrate data, prior commits) rather than ASSUMING dispatch framing is correct. Discipline #42 is the dispatch-time operationalization of #11.

### 4.2 Discipline #13 (implicit-pillar drift)

Framing-audit catches implicit-pillar drift cases. If dispatch presupposes an implicit pillar (e.g., "10 classes is the right roster size") that contradicts canonical pillars (e.g., "substrate votes; design follows"), Q3 returns YES.

### 4.3 Discipline #18 (math-before-code at hotspots)

Composes — Discipline #18 fires at MATH hotspots; Discipline #42 fires at EVERY dispatch. Where they overlap (math hotspot dispatches), both apply: framing-audit on the dispatch + math-before-code on the methodology.

### 4.4 Discipline #39 (no synthetic-stub-as-permanent-fallback)

Framing-audit Q1 explicitly checks for synthetic-stub-as-permanent-fallback patterns. If dispatch presupposes a stub that will become permanent, Q3 returns YES.

### 4.5 Discipline #40 (scaffold-with-pending-decision)

Framing-audit Q1 explicitly checks for scaffold values. If dispatch introduces a scaffold without flagging it as pending-decision, Q3 returns YES.

### 4.6 Discipline #41 candidate (pre-authored taxonomy interrogation)

Framing-audit Q1 explicitly checks for pre-authored taxonomies in generative systems. If dispatch presupposes a pre-authored taxonomy without explicit justification of why substrate-emergence is insufficient, Q3 returns YES.

### 4.7 Discipline #43 candidate (design-quality audit at wave-close)

Discipline #42 fires at DISPATCH CONSUMPTION (sub-agent inbound); Discipline #43 fires at WAVE-CLOSE (gandalf post-wave audit). Together they catch framing flaws BEFORE execution (Discipline #42) and DRIFT AFTER execution (Discipline #43).

### 4.8 Discipline #44 candidate (Framing-Refusal authority)

If framing-audit Q3 returns YES, sub-agent files a Framing-Refusal per Discipline #44 candidate. Discipline #42 is the AUDIT; Discipline #44 is the AUTHORITY to refuse based on audit output.

---

## 5. Operational impact

### 5.1 Per-dispatch cost

~5-10 minutes per dispatch added to sub-agent session-start. Sub-agents document framing-audit output in dispatch completion record. Cost is fixed per dispatch regardless of dispatch size.

### 5.2 Reduced-revert benefit

Each framing-audit that catches a framing-flaw saves ~1-7 days of revert + re-implementation work. Empirically: 3 of last week's failure modes (Wave 0.5 / Wave 1.5 Stage 2 / KR over-asking pattern) would each have been caught at framing-audit if Discipline #42 had been in force.

Cost-benefit at current observed failure rate: ~1-2 framing-flaw catches per cycle × ~3-day average revert avoided = ~3-6 days/cycle benefit at ~5 min × 10 dispatches/cycle = ~50 min/cycle cost. ~30-60x leverage.

### 5.3 Initial friction (early cycles)

Initially sub-agents will trigger framing-audit Q3 = YES more often than steady-state. This is healthy — sub-agents internalizing the new discipline. Friction stabilizes as KR-side dispatch authoring improves (Move 1 quality-criterion sections give sub-agents better framing to audit against).

---

## 6. Per-agent OP amendments (cross-seam delivery)

Each sub-agent's OP gets a new § "Framing-audit at session-start" with consistent text:

```markdown
## § X — Framing-audit at session-start (Discipline #42)

Before executing any dispatch (incoming sub-agent invocation OR session-resume),
run the three-question framing-audit:

- Q1: What load-bearing framing assumptions does this dispatch depend on?
- Q2: What evidence currently in hand could refute these assumptions?
- Q3: If refutation evidence exists, is the right move to refine the framing
     rather than execute the work as-framed?

Record framing-audit output in dispatch completion artifacts. If Q3 returns YES,
file a Framing-Refusal per Discipline #44 (do NOT execute the work as-framed).

Discipline #42 reference: engineering-disciplines.md § Discipline #42.
Composes with: #11, #13, #18, #39, #40, #41, #43, #44.
```

**Target files (10 agent OPs):**
- `.claude/agents/gandalf.md` (already has Pattern A-deep precedent; consolidate)
- `.claude/agents/knight-rider.md`
- `.claude/agents/rocket.md`
- `.claude/agents/gamora.md`
- `.claude/agents/star-lord.md`
- `.claude/agents/elrond.md`
- `.claude/agents/drax.md`
- `.claude/agents/legolas.md`
- `.claude/agents/jack-ryan.md`
- `.claude/agents/galadriel.md`

Each amendment ~10 min. KR routes the amendments per Move 2 sequencing.

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Discipline #42 candidate authored; routes to jack-ryan for canonical-write at engineering-disciplines.md
**Authority:** Matt 2026-05-27 ratification per quality-orientation-shift package Move 2
**Composition:** with gandalf OP § 4.1 (Pattern A-deep precedent) + Disciplines #11/#13/#18/#39/#40/#41/#43/#44 (full discipline-stack composition)

**For:** the canonical-write of Discipline #42 (Framing-audit at sub-agent dispatch consumption) — operationalizes the three-question framing-audit at every dispatch boundary, not just at Pattern A-deep verdicts. Catches framing flaws BEFORE execution bakes them into engine code. ~30-60x leverage on cost-of-implementation vs cost-of-revert-avoided. Routes to jack-ryan for engineering-disciplines.md amendment.

**Signed:** gandalf (story-and-design steward)
