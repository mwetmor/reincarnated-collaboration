# Autonomous-Fire Prompt Template — Operational Instrument for KR Session Entry

> **STATUS:** CANONICAL (load-bearing as of 2026-06-06) — Codifies the prompt-structure-as-operational-instrument discipline that converts standing canonical directives into autonomous-cycle execution. Empirically validated by two successful autonomous cycles: Phase A2 unattended cascade (Cycle 14 v1 MVP closure, 3 seasons production cascade, 0 Matt-touches; 2026-05-29 prompt at `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-kr-fire-prompt-handoff.md`) + Cosmograph Phase A creation-moment manifestation milestone (2026-06-06 cycle; gandalf sub-agent amendments + drax 5 phases + jack-ryan Gate-1 + Gate-2 + Vercel preview live; 0 Matt-touches during cycle execution).

**Date:** 2026-06-06
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-06 verbatim ratification: "Future autonomous fires should expect this prompt-structure-as-operational-instrument discipline. The prompt is not just a kickoff message; it's the operational specification that converts standing directives into autonomous-cycle execution."
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-kr-fire-prompt-handoff.md` — original Phase A2 prompt (canonical worked example #1)
- `canonical/story/2026-06-01-cycle-14-wave-5-swift-closure-wave-close-record.md` — Phase A2 outcome record
- `canonical/00-ground-state.md` — current truth oracle (always referenced as first read)
- `.claude/skills/reincarnated-knight-rider-operating-procedure/SKILL.md` — KR OP (consumption side)
- `.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` — gandalf OP (authoring side)

---

## 0. TL;DR

When firing knight-rider for autonomous-cycle execution at scope-above-trivial, the fire prompt is the **operational instrument** — not just a kickoff message. It carries 8 structural elements that translate standing canonical directives (hive-mind decision-routing 2026-05-23 verbatim, auto-commit addendum 2026-05-25, Discipline #42a framing-audit, Discipline #43 design-quality wave-close audit, etc.) into per-cycle execution autonomy. Without the 8 elements, KR drifts to default over-asking patterns; with them, KR executes autonomously through to wave-close with Matt-touches only at pre-declared surface conditions.

---

## 1. The 8 structural elements

Every autonomous-fire prompt at scope-above-trivial MUST carry:

### Element 1 — Mode + Phase scoping clarity

Opens with the exact operational mode + scope KR is operating in.

| Example | Source |
|---|---|
| "HIVE-MIND STATE Mode A per your operating procedure, SCOPED TO Phase A2 of the 2-phase Mode A framing (Phase A1 closed; Phase A2 = Wave 5 production cascade through Cycle 14 v1 MVP D9 close)" | Phase A2 |
| "Hive-mind state Mode B routine cross-seam dispatching SCOPED TO cosmograph Phase A creation-moment manifestation milestone" | Cosmograph Phase A |

**Why:** without explicit mode + scope, KR defaults to broad-scope orchestration mode which over-asks. Explicit scoping bounds KR's autonomous space.

### Element 2 — Required first reads in order

3-7 durable artifacts that fully onboard KR via session-start protocol. The artifacts are CHOSEN so that KR can reconstruct full session state without Matt re-explanation.

**Pattern:**
```
REQUIRED FIRST READS IN ORDER (read all N before any dispatch):

1. <durable session-state capture> — AUTHORITATIVE for gate dispositions + sequence + operational constraints
2. <KR-side prior-session boundary memo> — captures KR-side perspective
3. <closure or scope record> — locks the architectural state being inherited
4. <canonical state file> — KR-updated at session boundary
5. <relevant pushback memos or recognition records> — discipline anchors
[continue as needed; cap at 7]
```

**Why:** KR's session-start protocol requires durable artifact reads; pre-naming them prevents discovery overhead + ensures KR onboards from authoritative sources. The order matters — most-authoritative first.

### Element 3 — Locked gate dispositions

Matt-authorized pre-commitments enumerated explicitly. Each gate carries its semantic + authorization status.

**Pattern:**
```
LOCKED GATE DISPOSITIONS (Matt-authorized at session boundary):

- GATE (a) <name> — <RATIFIED / CONFIRMED / etc.> + <semantic detail>
- GATE (b) <cost cap> — $X SOFT CAP; surface to Matt queue at projected approach; do NOT hard-halt unless overshoot materially excessive
- GATE (c) <sequence> — CONFIRMED <A2-1 through A2-7> sequence
- PUSH per-workstream pattern: push after each <phase> Gate-2 PASS
- PATTERN E PRE-AUTHORIZATION for all <N> Gate-2 reviews; jack-ryan + gandalf may ratify autonomously per <unit>; Gate-2 BLOCK halts cascade + surfaces to Matt queue
```

**Why:** standing canonical directives (Matt 2026-05-23 hive-mind decision-routing; ADR-006 push-pattern; Pattern E autonomous ratification) become *executable* via explicit per-cycle pre-authorization. Without this, KR re-asks per-decision; with it, KR fires autonomously within the pre-authorized envelope.

### Element 4 — Operational constraints active

Disciplines enumerated as live operational context. Each constraint has a SEMANTIC (what it does) + a STATUS (active throughout cascade).

**Pattern:**
```
OPERATIONAL CONSTRAINTS (ACTIVE throughout cascade):

- Discipline #X <name> — <semantic; what KR does to honor it>
- Pre-flight <check> before each <fire unit> — abort to Matt queue if <condition>
- Pre-flight <maintenance> if <condition>
- Discipline #Y framing-audit applied at every dispatch consumption gate
- Discipline #Z design-quality audit applied at each Gate-2 review
- Auto-commit per CLAUDE.md addendum 2026-05-25 for work-products of authorized cascade work
```

**Why:** standing canonical disciplines + project addenda become per-cycle operational tools. KR has the disciplines AND knows they're active in this cascade.

### Element 5 — Surface conditions (positive AND negative pairing — LOAD-BEARING)

**This is the most-distinctive structural element vs default prompts.** Two paired lists.

**Pattern:**
```
SURFACE TO MATT AT (and only at):

- <Gate-2 BLOCK finding>
- <LLM soft-cap projection approach>
- <pre-flight check fail>
- <framing-audit finding catching pre-imposed-assumption failure>
- <scope-amendment request from sub-agent>
- <Matt-touch ratification gate at end>
- <substantial unexpected failure mode not covered by escalation rules>

DO NOT surface for:

- Routine in-scope sequencing decisions (KR decides per hive-mind decision-routing directive Matt 2026-05-23 verbatim)
- Auto-commit of work-products from authorized cascade work
- Per-<unit> Gate-2 PASS-with-WARN or PASS-with-INFO ratifications (Pattern E fire-and-continue)
- Per-workstream push after Gate-2 PASS (authorized)
```

**Why:** without the negative list, KR defaults to over-surfacing routine in-scope decisions. With the negative list, KR has explicit *permission to not bother Matt*. This composes with hive-mind decision-routing (Matt 2026-05-23 verbatim — seam-owner decides; Matt is LAST-resort escalation) and the auto-commit addendum.

### Element 6 — Anchors

Orientation principles — short list of canonical anchors KR operates under.

**Pattern:**
```
ANCHORS (unchanged):

- Engine first / game second / phase third
- Substrate-led discipline
- Recognition → empirical validation → commit
- Math-before-code at math hotspots
- Right tool for the validation question (Disc #5)
- <other relevant canonical anchors>
- Framing-audit at dispatch consumption (Disc #42a)
- Design-quality audit at wave close (Disc #43)
```

**Why:** anchors orient KR's decision-making under autonomy. When edge cases arise (which DO arise per cycle), KR has the orientation principles to make in-seam calls aligned with canonical commitments.

### Element 7 — First output expectation

Bounded startup behavior — exactly what KR acknowledges, verifies, and fires first.

**Pattern:**
```
YOUR FIRST OUTPUT THIS SESSION:

1. Acknowledge <cycle name> entry
2. Report pre-flight verification:
   - <vm_stat or similar host-health check>
   - <relevant artifact existence check>
   - <leftover state cleanup if needed>
   - <no active processes from prior session>
3. Author + fire <first sub-dispatch> under <constraint discipline>
4. Cascade proceeds; surface conditions per "SURFACE TO MATT AT" above
```

**Why:** without bounded first-output, KR may onboard indefinitely or fire wrong first step. Explicit first-output expectation forces decisive cycle entry.

### Element 8 — Companion artifact stack

Cross-references to the full handoff package KR consumes during session-start protocol.

**Pattern (in the prompt's footer or anchor sections):**
- gandalf resume memo (durable session-state capture)
- KR session-boundary memo (KR's prior-session checkpoint)
- canonical state file (KR-updated at session boundary)
- closure record or scope record (architectural commitment being inherited)
- relevant pushback memos / recognition records / pattern docs (discipline anchors)

**Why:** durable artifact-based handoff replaces in-context state-passing. New KR session starts cold; the artifacts ARE the state-passing mechanism. Pre-naming them makes session-start onboarding cheap + reliable.

---

## 2. When to apply

| Scope | Apply autonomous-fire template? |
|---|---|
| Multi-day production cascade (Phase A2, Cycle 14 wave 5) | YES — load-bearing |
| Multi-phase autonomous workstream (cosmograph Phase A 1-5 + Gate-2) | YES — load-bearing |
| Sub-agent fan-out involving 3+ seams | YES — load-bearing |
| Hive-mind state entry (any Mode) | YES — load-bearing |
| Single-seam single-execution short commission (~hours) | Optional — light-touch fire prompt is sufficient |
| Pattern-A query format (sub-hour empirical refutation) | NO — Pattern-A queries are different structure |
| One-shot Bash / Read tool query | NO — direct tool use; no KR involvement |

**Discriminator:** if the work requires KR to make 3+ in-seam decisions across the cycle, the 8-element template applies. If the work is one decision → one execution → close, light-touch is sufficient.

---

## 3. When NOT to apply

- Single-tool one-shot queries (Bash, Read, etc. — direct invocation)
- Pattern-A queries (cheapest empirical refutation; different format)
- Trivial dispatches (commit message authoring, single-file edits — direct)
- Sub-agent invocations from gandalf for short reconnaissance (different agent pattern)
- Matt-direct seam agent invocations (drax, elrond, etc. — those have their own session-start protocols)

---

## 4. Worked example #1 — Phase A2 unattended cascade (2026-05-29)

**Context:** Cycle 14 v1 MVP closure via 3-season production cascade. 6 dispatches in A2-1 through A2-7 sequence. Pattern E autonomous Gate-2 pre-authorization. $50 LLM soft cap.

**Outcome (per `canonical/story/2026-06-01-cycle-14-wave-5-swift-closure-wave-close-record.md`):**
- 3 seasons produced (001/002/003)
- 34 kits shipped + Phase 5 cohesion judge complete
- 21 shipped-worthy per archive telemetry
- A/B comparison filed; Disciplines batched canonical-write
- 0 Matt-touches during cascade; 1 Matt-touch at v1 tag ratification only
- Under $50 LLM soft cap

**Full prompt:** `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-kr-fire-prompt-handoff.md`

**8 elements visible:** Mode A + Phase A2 scoping (element 1) / 5 required first reads (element 2) / 3 gates + push + Pattern E (element 3) / Discipline #48 R48.4 + vm_stat + EGL log + Disc #42a + #43 + auto-commit (element 4) / SURFACE TO MATT AT + DO NOT surface for paired lists (element 5) / Engine/game/phase anchors + substrate-led + recognition-validate-commit + math-before-code + right tool + host-RAM-aware + framing-audit + design-quality (element 6) / acknowledge + pre-flight verification + fire A2-1 (element 7) / gandalf resume memo + KR session-boundary memo + state file + closure record + framing-audit pushback (element 8).

---

## 5. Worked example #2 — Cosmograph Phase A (2026-06-06)

**Context:** Creation-moment manifestation milestone. Elrond Phase 0-4 substrate-trace extraction + drax Phase 1-5 cosmograph build + jack-ryan Gate-1 + Gate-2 + Vercel preview deploy.

**Outcome:**
- Cosmograph live at `/forge` Vercel preview
- 570 substrate-led atomic stars + 1000 simulated PROVISIONAL constellations + 7 attribute-group faction halos + 6 emergent mechanic-family labels
- $0 LLM cost end-to-end
- 18/18 Gate-2 criteria PASS + family-contraction GREEN
- 0 Matt-touches during cycle execution; Matt UX testing surfaced lasso-zoom bug + pointer/grabber issue post-acceptance (handled cleanly via incremental-commit cadence on the same branch)
- Substrate-led discipline applied at every layer (primitive enumeration, faction rendering honestly per-attribute-group, mechanic-family emergent clustering, tier-band annotation-block substrate-honest call)

**Additional lessons from this cycle that strengthen the template:**

1. **Pattern-A query path back to gandalf during autonomous cycle** — elrond fired Pattern-A query mid-Phase-0 (weapon-form-ratio); gandalf sub-agent issued verdict; cycle proceeded
2. **Substrate-led correction at rendering layer** — drax tier-band substrate-honest call (annotation block vs canvas-wide) is the same discipline as kit-as-star→primitive-as-star pivot at design time
3. **Discipline #11 empirical-first inspection catches schema bugs pre-runtime** — `dominant_effect_category` corrected at Phase 3 + ingestion-contract validation at Phase 1
4. **Family-contraction audit at Gate-2** — verifying substrate-led-honest reductions (17 → 11 family enums) categorize cleanly into substrate-content / Matt-correction / D7-boundary reasons
5. **Empirical FPS measurement as Gate-2 definitive record** — math model passes; capture actuals on Vercel preview

These lessons inform Element 4 (operational constraints) + Element 5 (surface conditions: Pattern-A query path explicit) + Element 6 (anchors: substrate-led discipline at rendering layer named explicitly) in future fires.

---

## 6. The full template (copy-and-amend for new cycles)

```
KR — <cycle name> entry. You are operating in HIVE-MIND STATE
Mode <A/B> per your operating procedure, SCOPED TO <phase or milestone>.

REQUIRED FIRST READS IN ORDER (read all N before any dispatch):

1. <durable session-state capture path>
   — AUTHORITATIVE for <gate dispositions + sequence + operational
   constraints + surface conditions + first-output guidance>.

2. <KR-side prior-session boundary memo path>
   — captures KR-side perspective of <prior phase closure + this
   phase sequencing>.

3. <closure or scope record path>
   — <N sections; locks <architectural commitment> + enumerates
   <A2-1 through A2-N> sequence in § X>.

4. <canonical state file path>
   — KR-updated at session boundary; § N <state reflects prior
   phase CLOSED + this phase QUEUED-FOR-FIRE>.

5. <relevant pushback memos / recognition records / pattern docs>
   — discipline anchors operational at every dispatch consumption gate.

[6-7 if additional required reads exist; cap at 7]

LOCKED GATE DISPOSITIONS (Matt-authorized at session boundary):

- GATE (a) <name> <RATIFIED/CONFIRMED/...> <semantic detail>
- GATE (b) $X SOFT CAP for <cycle scope>; <enforcer agent> enforces;
  surface to Matt queue at projected approach; do NOT hard-halt unless
  overshoot materially excessive (>20% beyond cap)
- GATE (c) <A-1 through A-N> sequence CONFIRMED
- PUSH per-workstream pattern: push after each <unit> Gate-2 PASS
- PATTERN E PRE-AUTHORIZATION for all <N> Gate-2 reviews;
  jack-ryan + gandalf may ratify autonomously per <unit> as outputs land;
  Gate-2 BLOCK halts cascade + surfaces to Matt queue;
  PASS-with-WARN / PASS-with-INFO fire-and-continue per Pattern E

OPERATIONAL CONSTRAINTS (ACTIVE throughout cascade):

- Discipline #X <name> — <semantic>
- Pre-flight <check> before each <fire unit>; abort to Matt queue
  if <condition>
- Pre-flight <maintenance> if <condition accumulates>
- Discipline #42a framing-audit applied at every dispatch consumption gate
- Discipline #43 design-quality audit applied at each Gate-2 review
- Auto-commit per CLAUDE.md addendum 2026-05-25 for work-products of
  authorized cascade work

SURFACE TO MATT AT (and only at):

- Gate-2 BLOCK finding at any <unit>
- LLM soft-cap projection approach ($X threshold)
- Pre-flight check FAIL
- Discipline #42a framing-audit finding catching pre-imposed-assumption
  failure
- Scope-amendment request from any sub-agent
- <final Matt ratification gate>
- Any substantial unexpected failure mode not covered by escalation rules

DO NOT surface for:

- Routine in-scope sequencing decisions (you decide per hive-mind
  decision-routing directive Matt 2026-05-23 verbatim)
- Auto-commit of work-products from authorized cascade work
- Per-<unit> Gate-2 PASS-with-WARN or PASS-with-INFO ratifications
  (Pattern E fire-and-continue)
- Per-workstream push after Gate-2 PASS (authorized)

ANCHORS (unchanged):

- Engine first / game second / phase third
- Substrate-led discipline (at architecture AND rendering layers per
  2026-06-06 cosmograph Phase A cycle)
- Recognition → empirical validation → commit
- Math-before-code at math hotspots
- Right tool for the validation question (Disc #5)
- <host-RAM-aware operational concurrency / other relevant>
- Framing-audit at dispatch consumption (Disc #42a)
- Design-quality audit at wave close (Disc #43)

YOUR FIRST OUTPUT THIS SESSION:

1. Acknowledge <cycle name> entry
2. Report pre-flight verification:
   - <host-health check>
   - <relevant artifact existence check>
   - <leftover state cleanup if needed>
   - <no active sub-agent processes from prior session>
3. Author + fire <first sub-dispatch> under <constraint discipline>
4. Cascade proceeds; surface conditions per "SURFACE TO MATT AT" above

<Cycle target>: <high-level description of cycle completion criterion>.
<Cycle 15 / next-cycle entry> as next-cycle pre-scope on <this cycle>
close per recognition record at <path>.

Operate per the discipline architecture above. Drive the cascade to
<cycle close criterion>.
```

---

## 7. Cross-references

### 7.1 Composes with (existing canon)

- `CLAUDE.md` § Team commit + push discipline (auto-commit addendum 2026-05-25)
- `agentic_orchestration/GOVERNANCE.md` — ADRs including ADR-002 tiered approval + ADR-006 read-only-by-default
- `agentic_orchestration/operating-procedures/hive-mind-protocol.md` — hive-mind state entry/exit/crash recovery
- `.claude/skills/reincarnated-knight-rider-operating-procedure/SKILL.md` — KR OP (consumption discipline)
- `.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` — gandalf OP (authoring discipline)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines (#11 empirical inspection, #18 math-hotspot, #41 substrate-led, #42a framing-audit, #43 design-quality wave-close, #46 db anti-materialization, #48 host-RAM-aware, #59 substrate coverage)

### 7.2 Authoring-side discipline amendment candidates

- **Gandalf OP § 4 (operational protocols)** — amend to add § 4.x "autonomous-fire prompt authoring as operational instrument" — fires when gandalf authors a KR fire prompt at scope-above-trivial; references this canonical pattern doc as authoritative template
- **KR OP** — amend to add "expect autonomous-fire prompts at scope-above-trivial to carry the 8-element structure; surface back to gandalf via Pattern-A query if any element missing" — gives KR right to push back on under-structured fire prompts

Both amendments deferred to next OP refinement passes; this canonical pattern doc stands as the authoritative reference until OP amendments land.

### 7.3 Empirical-evidence trigger for further amendment

If future autonomous cycles surface NEW structural elements not captured here (e.g., element 9 emerges from operational use), amend this doc at first such cycle close. The 8-element structure is empirically grounded in two cycles; future cycles strengthen or amend it.

---

## 8. Sign-off

**Authored:** gandalf 2026-06-06 per Matt verbatim ratification + post-cosmograph-Phase-A cycle close evidence consolidation
**Authority:** Matt 2026-06-06 — "Future autonomous fires should expect this prompt-structure-as-operational-instrument discipline"
**Empirical foundation:** Phase A2 unattended cascade (2026-05-29 prompt → 2026-06-01 wave-close) + Cosmograph Phase A creation-moment manifestation milestone (2026-06-06 cycle)
**Routing:** authoritative template for all gandalf-authored KR fire prompts at scope-above-trivial; consumption reference for KR session-start protocol; informs gandalf OP § 4 + KR OP amendment candidates at next refinement passes

**This canonical pattern doc captures the operational instrument discipline that converts standing canonical directives into per-cycle execution autonomy. The 8 elements are load-bearing. Future autonomous fires apply them.**

**End of canonical pattern doc.**
