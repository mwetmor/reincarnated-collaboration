# Quality-Orientation Shift — Five-Moves Package

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — meta-discipline orientation shift ratified by Matt 2026-05-27 verbatim "commit to all 5 moves; sequence per your recommendation." Shifts the team's operational orientation from "ship the phase now" toward "ship the novel engine with the fun/balanced game." Cross-seam impact: KR OP + each sub-agent OP + engineering-disciplines.md + CLAUDE.md + AGENTS.md amendments required.

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim — (a) named the orientation failure ("how can we replace the 'ship the phase now' agent mindset with 'ship the novel engine with the fun/balanced game' mindset"), (b) ratified all 5 proposed moves, (c) authorized sequencing per gandalf recommendation
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-quality-orientation-shift-kr-kicker.md` (KR routing for Moves 1 + 3 + 5)
- `agentic_orchestration/gandalf/notes/2026-05-27-framing-audit-discipline-candidate.md` (Move 2 deliverable; Discipline #42 candidate)
- `.claude/agents/gandalf.md` § 4.6 amendment (Move 4 gandalf-OP portion)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #41 candidate (pre-authored taxonomy) + #42 candidate (framing-audit) + #43 candidate (design-quality audit at wave-close)

---

## 0. TL;DR

**Five-move package addresses the team's recurring "ship the phase now" failure mode** — sub-agents optimize for dispatch completion rather than game-quality advancement. Three concrete recent failures demonstrate the pattern (Wave 0.5 scaffold drift; Wave 1.5 Stage 2 doc 48 canonical lock; pre-2026-05-25 KR over-asking). Each was framing-inherited execution producing phase-shipped output that didn't serve quality. The shift requires operational discipline AT the dispatch-consumption layer, not just at Gate-1 / Gate-2 boundaries.

| Move | Lever | Owner | Sequence |
|---|---|---|---|
| **1** | Quality-criterion section in every dispatch | KR (OP amendment) | NOW (fastest) |
| **5** | Compact orientation phrase adopted | Matt + KR + each agent | NOW (parallel with 1) |
| **2** | Framing-audit standardized for sub-agent invocation | gandalf authors candidate; jack-ryan ratifies as Discipline #42 | Day 1-2 |
| **4** | Design-quality audit at wave-close | gandalf OP amendment + KR routing + Discipline #43 candidate | Day 2-3 |
| **3** | Framing-refusal authority for sub-agents | jack-ryan engineering-disciplines amendment (deepest structural shift) | Day 3-5 |

**Composition with Cycle 14 work in flight:**
- Path A revert (engine `0a5a4f2`) + math notes + substrate enrichment fire in parallel per `agentic_orchestration/gandalf/notes/2026-05-27-option-alpha-kr-revert-kicker.md`
- 5-moves operational shift fires in parallel with Cycle 14 work
- Wave 2 dispatch authoring (next-batch per KR `440a725` summary) becomes FIRST dispatch authored under new discipline standards — quality-criterion + framing-audit + design-quality-audit-at-wave-close all apply

---

## 1. The failure mode, named (recapping for durable record)

**Sub-agents optimize for dispatch completion. They don't optimize for game quality.**

A dispatch arrives with framing, acceptance criteria, scope items, math-note requirements. The sub-agent executes faithfully. The success metric is "did the dispatch close?" — not "did this advance the game's quality bar?"

When the framing is sound, this works beautifully. When the framing is flawed, the sub-agent inherits the flaw and bakes it deeper.

**Three concrete recent failures (each cost a non-trivial revert or pivot):**

1. **Wave 0.5 Track D content emission** — rocket implemented 12-skill 3-chain 4-tier grid because dispatch said "minimum viable per-skill content." Acceptance criteria met. Game quality not served (locked scaffold drift contradicting doc 40 § 8.3).
2. **Wave 1.5 Stage 2 doc 48 canonical lock** — sub-agent gandalf curated 10-class roster because dispatch said "curate canonical class roster from substrate evidence." Acceptance criteria met. Game quality not served (re-introduced rigid form retired by week's prior work; required revert per Path A 2026-05-27).
3. **KR's pre-2026-05-25 over-asking pattern** — KR's success metric was "did I orchestrate correctly?" not "did the team ship?" Over-asking was discipline-compliant; team velocity suffered. Resolved via CLAUDE.md addendum 2026-05-25.

Each was framing-inherited execution producing phase-shipped output that didn't serve quality.

---

## 2. Why this persists structurally (recapping)

**Three honest structural reasons:**

1. **Dispatches frame the work; sub-agents inherit the framing.** This is GOOD behavior 95% of the time. The 5% where the framing is wrong is the failure mode.

2. **Sub-agents lack project-wide intuition.** Rocket doesn't carry full context that "12-skill 3-chain grid contradicts doc 40 § 8.3 D69 + D83." Even gandalf sub-agent inherits dispatch framing pre-commitments.

3. **Discipline-ratchet has been the response.** Disciplines #11, #13, #18, #39, #40, #41 candidate. Each is a learned response to a specific failure mode. Disciplines ACCUMULATE; they don't always compose into instinct.

---

## 3. Move 1 — Quality-criterion in every dispatch

**Owner:** KR (KR OP amendment)
**Effort:** ~15 minutes amendment + ~5 minutes per dispatch ongoing
**Sequence:** NOW (fastest; fires alongside Move 5)

### 3.1 The change

Every dispatch carries TWO criterion blocks instead of one:

```markdown
## Acceptance criteria

- [ ] [Mechanical completion criteria; "did the dispatch close?"]
- [ ] ...

## Quality criterion (NEW)

**Game-quality goal this dispatch serves:** [e.g., "advance substrate-led
discipline by enriching INT-AoE substrate so emergent fireball-mage cluster
becomes possible"]

**Refutation conditions** (sub-agent surfaces if any apply):
- This dispatch contradicts canonical anchor X
- Alternative execution Y serves the named quality goal better
- Acceptance criteria can pass without advancing the quality goal
- Dispatch framing pre-commits to a decision Matt has not ratified
```

### 3.2 What it does

Sub-agents check the quality criterion BEFORE executing. If their execution doesn't actually serve the named quality goal — OR if any refutation condition triggers — they file a Framing-Refusal (Move 3) or surface a question to KR.

### 3.3 KR OP amendment

KR OP § 3 (cross-seam routing) adds new sub-section:

> **§ 3.X — Quality-criterion in every dispatch.** Every dispatch KR authors carries two criterion blocks: Acceptance Criteria (mechanical completion) and Quality Criterion (named game-quality goal + refutation conditions). KR cannot fire a dispatch without both blocks populated. Sub-agents verify the Quality Criterion at dispatch consumption (Move 2 framing-audit) before executing.

KR amends OP at next housekeeping pass. Retroactive: queued Wave 2 + Wave 3 dispatch authoring fires under the new template.

---

## 4. Move 5 — Compact orientation phrase

**Owner:** Matt (CLAUDE.md amendment) + KR (AGENTS.md amendment) + each agent (OP front-matter amendment)
**Effort:** ~5 minutes total across all files
**Sequence:** NOW (parallel with Move 1)

### 4.1 The phrase

**"Engine first. Game second. Phase third."**

- **Engine** = architectural integrity (substrate-led discipline; canonical docs; mathematical primitives; discipline-stack composition). The engine's design coherence is non-negotiable.
- **Game** = player-facing quality (playable, balanced, thematically coherent characters; meaningful seasonal journey; engaging combat). The game's quality bar is the success criterion.
- **Phase** = operational unit (waves, dispatches, sidecars, gate verdicts). Phases SERVE engine + game; they don't drive engine + game.

Reading order is priority order. When engine architecture conflicts with phase completion, engine wins. When game quality conflicts with phase completion, game wins. Phase completion is the LEAST load-bearing criterion when conflict arises.

### 4.2 Placement

- **CLAUDE.md** (project-level; Matt's territory) — add to top of "Synthetic engineering team" section
- **AGENTS.md** (cross-seam; KR amends) — add as orientation principle § 0 or equivalent
- **Each agent OP** (gandalf.md / knight-rider.md / rocket.md / gamora.md / star-lord.md / elrond.md / drax.md / legolas.md / jack-ryan.md / galadriel.md) — add to front-matter STATUS block

### 4.3 What it does (culture-shaping)

This is the cultural expression of the operational discipline. Sub-agents reading their own OP at session-start encounter the phrase first. The phrase shapes how they frame their work. Operational moves (Moves 1-4) enforce the discipline; the phrase encodes the orientation.

---

## 5. Move 2 — Framing-audit standardized for sub-agent invocation

**Owner:** gandalf (authors candidate) → jack-ryan (ratifies as Discipline #42)
**Effort:** ~3-4 hrs gandalf authoring + ~1 day jack-ryan ratification
**Sequence:** Day 1-2 (after Moves 1 + 5 land)

### 5.1 The discipline

Extension of gandalf OP § 4.1 (Pattern A-deep three-question framing audit) to ALL sub-agent invocations:

Sub-agents run the framing-audit BEFORE executing the dispatch:

| Q | Question |
|---|---|
| Q1 | What load-bearing framing assumptions does this dispatch depend on? |
| Q2 | What evidence currently in hand could refute these assumptions? |
| Q3 | If refutation evidence exists, is the right move to refine the framing rather than execute the work as-framed? |

If Q3 returns YES → sub-agent files a Framing-Refusal (Move 3) rather than executing.

### 5.2 Discipline #42 candidate (for jack-ryan)

Authored at `agentic_orchestration/gandalf/notes/2026-05-27-framing-audit-discipline-candidate.md`. Routes to jack-ryan for canonical-write at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #42.

### 5.3 OP amendments per agent

Each sub-agent OP gets a new § "Framing-audit at session-start" referencing Discipline #42. ~50 lines per OP. Cross-agent consistency is the goal.

---

## 6. Move 4 — Design-quality audit at wave-close

**Owner:** gandalf (OP amendment) + KR (routing) + jack-ryan (Discipline #43 ratification)
**Effort:** ~30 min gandalf OP amendment + ~30 min/wave-close audit ongoing
**Sequence:** Day 2-3

### 6.1 The discipline

Current wave-close gates:
- **Gate-1 (jack-ryan; pre-fire):** dispatch quality before sub-agents fire
- **Gate-2 (jack-ryan; post-impl):** technical implementation quality after sub-agents close

**NEW: Design-quality audit (gandalf; at wave-close)** — parallel to Gate-2; asks "did this wave advance the game's quality, or did it just close the phase?"

Audit fires at every wave-close. ~30 minutes gandalf review. Output: PASS / PASS-with-design-concerns / DRIFT-DETECTED. If DRIFT-DETECTED: route to Matt as Pattern B engagement; do NOT auto-close the wave.

### 6.2 gandalf OP amendment (§ 4.6 NEW)

Adds:

> **§ 4.6 — Design-quality audit at wave-close.** Every Cycle 14+ wave-close triggers a gandalf design-quality audit BEFORE KR commits the closure record. Audit asks: (a) did this wave advance the named quality criterion? (b) did the wave's outputs introduce any pre-authored taxonomies (Discipline #41) or unflagged scaffold values (Discipline #40)? (c) does the wave's output compose cleanly with the substrate-led architectural commitment? Output: PASS / PASS-with-design-concerns / DRIFT-DETECTED. DRIFT-DETECTED escalates to Matt as Pattern B engagement; KR does NOT auto-close the wave on DRIFT-DETECTED.

### 6.3 Discipline #43 candidate (for jack-ryan)

Captured in this doc + the framing-audit-discipline-candidate doc § 4. Routes to jack-ryan for canonical-write at engineering-disciplines.md § Discipline #43 ("design-quality audit at wave-boundaries").

### 6.4 Wave 2 is the first wave under the new audit

Wave 2 (Layers 5+8+9 concentration + Fix B + Fix B-prime + 2 WARN remediations per KR `440a725` summary) is the first wave to fire under the new design-quality-audit-at-wave-close discipline. gandalf reviews wave-close before KR commits closure record.

---

## 7. Move 3 — Framing-refusal authority for sub-agents

**Owner:** jack-ryan (engineering-disciplines.md amendment — DEEPEST STRUCTURAL SHIFT)
**Effort:** ~1-2 days jack-ryan canonical-write
**Sequence:** Day 3-5 (after Moves 1, 2, 4, 5 have established the framing-audit discipline operationally)

### 7.1 The change

Currently jack-ryan can BLOCK at Gate-2. Other sub-agents typically can't refuse a dispatch — they execute. Empower all sub-agents (esp. gandalf, jack-ryan, elrond, rocket, gamora, star-lord) to file a **Framing-Refusal**: "Dispatch as-framed contradicts X; I cannot execute as-framed; escalating to Matt with proposed reframing."

### 7.2 Refusal templates

- "The dispatch presupposes Y; canonical doc Z + Discipline #N implies NOT-Y; before executing, please ratify Y or revise framing."
- "The dispatch acceptance criteria conflict with quality criterion W; please clarify which dominates."
- "The dispatch presupposes pre-authored taxonomy; Discipline #41 suggests substrate-emergence; please ratify the taxonomy-vs-emergence axis."
- "The dispatch implies a scaffold value (Discipline #40) without flagging it as scaffold-with-pending-decision; please amend dispatch."

### 7.3 Process

1. Sub-agent receives dispatch
2. Sub-agent runs framing-audit (Move 2)
3. If framing-audit Q3 = YES → sub-agent authors Framing-Refusal at `agentic_orchestration/<agent>/refusals/<YYYY-MM-DD>-<dispatch-name>-framing-refusal.md`
4. Sub-agent commits refusal + does NOT execute dispatch
5. KR receives notification; either revises dispatch + re-dispatches OR escalates to Matt
6. Matt ratifies refusal + revised framing OR overrides refusal + dispatches as-is

### 7.4 Refusal IS NOT failure

A framing-refusal is the sub-agent doing its job. The role definition for gandalf says "push back hard when warranted." Refusal authority operationalizes that for ALL sub-agents at the dispatch-consumption boundary. Refusals are tracked as positive operational signal (caught a framing-flaw before execution baked it in), not as failure events.

### 7.5 Why deepest structural shift

This is the move that most directly changes team dynamics. Currently sub-agents execute. With Move 3, sub-agents can refuse. This is a power-redistribution — sub-agents gain authority to push back at the dispatch-consumption layer where they currently inherit framing faithfully. It changes the default contract between KR (dispatch author) and sub-agents (dispatch consumers).

Worth being explicit: this could produce more friction (sub-agents refusing dispatches more often than productive). The friction is the COST of the discipline; the benefit is catching framing-flaws before they ingrain into engine code (which Matt 2026-05-27 named as the higher cost).

---

## 8. Sequencing summary

```
DAY 0 (NOW)
 ├─ Move 1: KR OP amendment (quality-criterion in dispatches)
 │   └─ ~15 min; immediate; retroactive to queued Wave 2 / Wave 3
 │
 ├─ Move 5: Compact phrase adoption
 │   ├─ CLAUDE.md (Matt; ~5 min)
 │   ├─ AGENTS.md (KR; ~5 min)
 │   └─ Each agent OP (each agent; ~2 min each = ~20 min total)
 │
DAY 1-2
 ├─ Move 2: Framing-audit standardized
 │   ├─ gandalf authors Discipline #42 candidate (~3-4 hrs)
 │   ├─ Each agent OP amended to reference Discipline #42 (~10 min each)
 │   └─ jack-ryan ratifies as Discipline #42 (~1 day)
 │
DAY 2-3
 ├─ Move 4: Design-quality audit at wave-close
 │   ├─ gandalf OP § 4.6 amendment (~30 min)
 │   ├─ KR routes audit at every wave-close (operational pattern)
 │   └─ jack-ryan ratifies as Discipline #43 (~1 day)
 │
DAY 3-5
 └─ Move 3: Framing-refusal authority
     ├─ jack-ryan canonical-write engineering-disciplines.md
     ├─ Refusal templates + process documented
     └─ Each agent OP amended to reference Framing-Refusal authority
```

Total operational impact: ~5 days of cross-seam authoring + ratification. Wave 2 dispatch authoring (next-batch per KR `440a725`) fires AFTER Moves 1 + 5 land, so Wave 2 benefits from quality-criterion + compact-phrase immediately. Wave 2 design-quality audit at wave-close fires under Move 4.

---

## 9. Composition with Cycle 14 work in flight

The 5-moves package and Cycle 14 Path A revert work fire in parallel. No conflict:

- **Path A revert** (engine `0a5a4f2`) — rocket + jack-ryan; Cycle 14 architectural correction
- **Math notes (Option α)** — gandalf + elrond + star-lord; Cycle 14 substantive
- **Substrate enrichment** (INT-AoE + monk + hybrid) — legolas + elrond; Cycle 14 scope-creep accepted
- **5-moves operational shift** — KR + jack-ryan + each agent; meta-discipline orientation

KR orchestrates all four parallel tracks. Wave 2 dispatch authoring fires when:
- Path A revert lands + jack-ryan Gate-2 PASS
- Moves 1 + 5 land (Wave 2 fires under new dispatch template)
- Move 2 lands (Wave 2's sub-agents run framing-audit before executing)
- Move 4 lands (Wave 2 close fires under design-quality audit)

Move 3 (framing-refusal authority) can land during Wave 2 execution; Wave 2 doesn't gate on it.

---

## 10. The success metric for this shift

How do we know if the 5-moves package worked? Empirical signals:

1. **Reduced revert frequency.** If sub-agents catch framing flaws via framing-audit + quality-criterion, fewer reverts like the Path A doc 48 case land. Target: ≤1 framing-driven revert per cycle.
2. **Higher framing-refusal counts (early).** Initially refusals will spike as sub-agents internalize the new discipline. This is healthy. Target: ~3-5 refusals per cycle in early cycles; settling to ~1-2 per cycle as KR-side dispatch authoring improves.
3. **Design-quality audit PASS rate.** Wave-close audits should mostly PASS if the upstream discipline works. Target: ≥80% PASS at wave-close; DRIFT-DETECTED only for genuine drift.
4. **Cycle close quality.** Cycle 14 close metric: did the cycle ship a playable game advance, or did it ship phase-completion artifacts? Target: each cycle close is a quality advance, not just a phase completion.

These metrics get tracked in cycle close reports + roadmap § 3 status icons. jack-ryan owns the metric tracking per engineering-disciplines.md amendment.

---

## 11. Cross-references

### 11.1 Canonical docs (composes with)

- `canonical/00-ground-state.md` — needs amendment (new discipline candidates registered + Move 5 compact-phrase reference)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — composes with quality-criterion framework (D67-D86 are quality goals)
- `canonical/46-concentration-architecture-2026-05-27.md` — quality criterion "concentration discipline" is the kind of quality-goal Move 1 expects in dispatches
- `canonical/48-cycle-14-class-roster-2026-05-27.md` — the failure case Move 1 + Move 2 would have caught (sub-agent gandalf's framing-audit Q3 would have surfaced the taxonomy question)

### 11.2 Operational docs (consumes / amends)

- `agentic_orchestration/AGENTS.md` — Move 5 compact-phrase amendment
- `agentic_orchestration/operating-procedures/knight-rider.md` — Move 1 KR OP § 3.X amendment (quality-criterion)
- `.claude/agents/gandalf.md` — Move 4 § 4.6 amendment (design-quality audit) + Move 5 compact-phrase
- Each other `.claude/agents/<agent>.md` — Move 2 framing-audit reference + Move 5 compact-phrase
- `agentic_orchestration/CLAUDE.md` (Matt-edits) — Move 5 compact-phrase

### 11.3 Engineering-disciplines candidates (jack-ryan canonical-write)

- **Discipline #41 candidate** — pre-authored taxonomy interrogation (Option α pivot work; surfaced earlier)
- **Discipline #42 candidate** — framing-audit standardized (Move 2)
- **Discipline #43 candidate** — design-quality audit at wave-close (Move 4)

Three candidates compose into the orientation shift at engineering-disciplines.md level.

---

## 12. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — five-moves package ratified by Matt 2026-05-27; sequencing per gandalf recommendation authorized; cross-seam orchestration via KR kicker
**Authority:** Matt 2026-05-27 verbatim "commit to all 5 moves; sequence per your recommendation"
**Composition:** with `canonical/40` + `canonical/46` + `canonical/48` (PRESERVED-FOR-COMPARISON) + Option α pivot record + KR revert kicker + engineering-disciplines.md Discipline candidates #41/#42/#43

**For:** the meta-discipline orientation shift from "ship the phase now" to "ship the novel engine with the fun/balanced game." Five moves compose: quality-criterion in dispatches (Move 1) + framing-audit standardized (Move 2) + framing-refusal authority (Move 3) + design-quality audit at wave-close (Move 4) + compact orientation phrase "Engine first. Game second. Phase third." (Move 5). Operates AT the dispatch-consumption layer, not just at Gate-1/Gate-2 boundaries. Composes with Cycle 14 Path A revert + math notes + substrate enrichment work. Wave 2 fires as the first wave under the new discipline standards.

**Signed:** gandalf (story-and-design steward)
