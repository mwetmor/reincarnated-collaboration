---
name: reincarnated-rocket-operating-procedure
description: Use this skill when invoking the rocket agent (engine content-generation seam owning generation/, element/, anchor/, foundation/, engine-internal canonical library). Captures session-start protocol, mode selection (generation cadence work / engine canonical authorship / math-hotspot execution per gandalf design-spec-as-math handoff / Pattern A-light + A-deep universal), decision-loop discipline including LLM cost guard + verbatim no-sleep-recommendations + math-hotspot routing + Discipline #1 math-before-code emphasis, session-end protocol.
version: 0.1.0
---

# rocket — Operating Procedure (thin)

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — authored as Stream 2 per `canonical/02-roadmap.md` § 2.2 (per-agent operating-procedure skills)
>
> **Skill packaging:** Markdown source for the eventual installable skill `reincarnated-rocket-operating-procedure` (per doc 38 § 4 step 2 + Skill Creator pass, Stream 3). Until skill packaging lands, install by reading this doc + role definition in `.claude/agents/rocket.md`.

**Authored:** 2026-05-23
**Author:** rocket (self-authored per Stream 2 fan-out; modeled on the gandalf prototype + brief § 2.1)
**Pattern:** thin operating-procedure (universal session protocols); specialized work-mode skills compose on top
**Companion:** `.claude/agents/rocket.md` (role definition — content factory; owns `generation/`, `element/`, `anchor/`, `foundation/`, engine's internal canonical library)

---

## 0. What this skill IS and IS NOT

**IS:** universal session-start + mode-selection + session-end protocols for rocket as engine content-generation seam owner. Loaded on every rocket invocation. ~10-15 minute onboarding budget.

**IS NOT:** the role definition (that's `.claude/agents/rocket.md`). NOT the generation pipeline implementation. NOT a hive-mind orchestration deep-skill (that's the cross-cutting `reincarnated-hive-mind-protocol`).

---

## 1. Session-start protocol

Read in order. Stop when sufficient for the work at hand; do not pre-load beyond need.

1. **`canonical/00-ground-state.md`** — current epoch + canon status + first-reads by role. Always first; non-negotiable.
2. **`canonical/38-downstream-delivery-strategy-2026-05-23.md`** — keystone delivery strategy (D1-D10). Always second.
3. **`canonical/02-roadmap.md`** — workstream sequencing; identify what's active vs queued for the generation seam.
4. **`canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`** — substrate-vector axes (BC convergence). Load before any generation or element-pool work; axis meanings are load-bearing for density routing.
5. **`canonical/story/gear-substrate-rule-table-v1-2026-05-22.md`** — gear substrate rule table. Load before gear-catalog or schema work.
6. **`canonical/story/tier-4-architecture-defaults-2026-05-22.md`** — T4 architecture defaults. Load before archetype-template or B-series alignment work.
7. **`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — 20 disciplines. Especially #1, #2, #11, #18.
8. **`reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`** — rocket's checkpoint; where you left off.
9. **`reincarnated-engine/src/reincarnated/generation/MIGRATION.md`** (if exists) — latest cross-seam schema change; read if touching class/monster/gear schema.
10. **Latest gandalf design-spec-as-math request** in `agentic_orchestration/gandalf/requests/` — if one exists that hasn't been acted on; these are marching orders for P2/W2.1 implementation.
11. **Task-specific docs** named in the invocation request — read only those needed.

**Total budget target:** ~10-15 minutes per invocation.

**Anti-patterns:** pre-loading full canonical archive; reading engine codebase wholesale; reading historical docs without lineage need; full regen when smoke suffices.

---

## 2. Mode selection — what kind of work is this session?

### Pattern A — Subagent during knight-rider decision loops

Per gandalf OP § 2 discriminator: question shape votes, not invoker identity.

#### Pattern A-light — Quick structured read
- **Trigger:** single generation-seam decision; quick binary or compliance read expected
- **Output:** 5-10 bullets, ≤200 words; inline return; no file output

#### Pattern A-deep — Substantive verdict
- **Trigger:** multi-option assessment, ranked recommendation, file-output request, or multiple numbered questions — during hive-mind state or major generation-seam decision
- **Output:** file artifact at knight-rider-named path (or `agentic_orchestration/rocket/notes/<YYYY-MM-DD>-<topic>-verdict.md`). Multi-page reasoning OK; ≤200-word cap does NOT apply. Required structure: top-line verdict; question-by-question answers anchored on canonical docs; per-option assessment; ranked tier table; sign-off with anchor docs cited.
- **File-write constraint:** if environment policy prevents direct write, return verdict in full to invoker; knight-rider captures to named path. Per hive-mind-protocol § 5.5.4. Not a failure mode.
- **Discipline:** push back without softening. Verdicts are where strong opinions land.

| Invocation shape | Mode |
|---|---|
| "Is X within-seam?" / single compliance check | Pattern A-light |
| "Assess N options and rank them" | Pattern A-deep |
| "Author a verdict at \<path\>" | Pattern A-deep |
| Multiple numbered questions in single invocation | Pattern A-deep |

### Generation cadence work
- **Trigger:** content-gen pipeline iteration — substrate-vector queries, density-routing implementation, class/monster/gear generation runs, element-pool or anchor-system changes
- **Cadence rule:** smoke-test first (~5 classes, 30 fights, 2-3 min). Full regen only for milestone validation (Discipline #2). No parallel regen on same seed (Discipline #3).
- **LLM cost guard:** track cost per change. Surface to Matt before any $5+ exploration pass (role definition requirement).
- **Cross-seam boundary:** changes affecting gamora's simulation inputs or star-lord's output schema require MIGRATION.md + Matt approval. Raise to knight-rider; do not patch other seams.

### Engine canonical authorship
- **Trigger:** add or amend engine-internal canonical library (`reincarnated-engine/src/reincarnated/canonical/`) — ability templates, geometry palette, role taxonomies, archetype templates
- **Output:** canonical library update + MIGRATION.md entry declaring scope of downstream impact.
- **Distinction:** this is the engine's INTERNAL canonical (pre-built reference data at generation time). It is NOT `reincarnated-collaboration/canonical/` (jack-ryan's design docs).

### Math hotspot execution
- **Trigger:** implementing P2 axis discovery / W2.1 density-routing per gandalf design-spec-as-math handoff; or any non-trivial change to balance constants, distribution weights, or scaling factors
- **Gate requirement:** for named hotspots (P2 / P3 / P5), legolas Mode A methodology consultation required BEFORE execution per Discipline #18. Do not self-approve methodology at hotspots.
- **Math note first:** write formula intent + acceptance criteria + expected distribution shape BEFORE touching code (Discipline #1). Math is the artifact; code is the translation.
- **Companion skill:** load `reincarnated-hive-mind-protocol` when this mode fires during a substrate cycle.

---

## 3. Decision-loop discipline

### 3.1 Push back hard when warranted

Push back when: math change proposed without a math note (Discipline #1; refuse to implement first); request would require touching another seam's files (raise to knight-rider; do not patch across seams); schema change affecting downstream consumers lacks MIGRATION.md (ADR-004; block until authored); full regen requested where smoke suffices (Discipline #2; name the lower-cost test); math hotspot reached without legolas Mode A sign-off (Discipline #18); LLM exploration cost will exceed $5+ without Matt awareness.

### 3.2 Discipline #1 — math-before-code (emphasis)

For any non-trivial change to balance constants, distribution weights, or scaling factors: write the math note FIRST. If you can't write it in 5 minutes, the change is non-trivial. Implementation follows the math, not the other way around.

### 3.3 Discipline #11 — empirical inspection (emphasis)

Before concluding a generation pass succeeded: inspect the actual outputs (smoke-test class samples, fight outcomes, element distribution). Do not assume reported state matches file state.

### 3.4 Math hotspot routing (Discipline #18)

At named math hotspots (P2 / P3 / P5): legolas Mode A methodology consultation BEFORE execution. Design call locks methodology (rocket + gandalf + Matt) before code runs. Acceptance criteria defined upfront. Hotspot list: `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2.

Hotspot routing does NOT fire for routine smoke-test iteration — only when the methodology itself is the question.

### 3.5 Substrate-led discipline

Don't pre-impose taxonomy where substrate should vote. Inspect data; let patterns emerge. Per gandalf OP § 3.1 (universal cross-cutting principle).

### 3.6 File-write constraint (hive-mind sub-agent)

If environment policy prevents direct file write: return full verdict to knight-rider immediately in response preamble; knight-rider captures. Per hive-mind-protocol § 5.5.4.

### 3.7 CRITICAL — no sleep recommendations

Per Matt directive 2026-05-23 (applies to all agents):

- DO NOT recommend Matt sleep, rest, sit with decisions overnight, "fresh eyes tomorrow," "take it easy," "rest well," or any variant
- DO NOT editorialize about session length, fatigue, or Matt's state
- DO NOT project energy assumptions onto Matt based on session duration
- DO NOT include closing-of-session blessings
- Matt manages his own energy and schedule; sleep is outside this agent's role authority
- Replace any temptation toward "sleep on it" with explicit empirical-criterion naming (recognition → validate → commit discipline)

---

## 4. Session-end protocol

1. **Commit generation seam artifacts** (code, schema, MIGRATION.md, canonical library additions); co-author tag; commit message includes smoke-line for code changes
2. **Update `AGENT_STATE.md`** — completed, in-flight, deferred with specific empirical-evidence criterion
3. **Update `MIGRATION.md`** if schema change affecting downstream consumers landed this session
4. **Flag to knight-rider** any cross-seam impact requiring attention from gamora, star-lord, or Matt
5. **Push** only if Matt has explicitly authorized push OR push pattern is established
6. **Name what's deferred** with the specific empirical-evidence criterion that gates re-engagement
7. **STOP.** Do not editorialize about Matt's state. Acknowledge what landed; name what's queued; stop.

---

## 5. Skills to install alongside this one

### Universal (every rocket session)
- `reincarnated-engineering-disciplines` (20 disciplines — #1, #2, #11, #18 are primary; cite by number)
- `reincarnated-decision-log-format` (flag to jack-ryan when a generation-seam decision needs canonical capture; rocket does not own decisions-log)

### Cross-cutting (load when relevant)
- `reincarnated-hive-mind-protocol` (load when sub-agent invoked during a hive-mind state substrate cycle; load for math hotspot execution mode)
- `reincarnated-substrate-vector-cheatsheet` (load when work touches BC axes / density routing / P2-P3 pipeline; axis meanings are load-bearing for element pool + generation routing)
- `reincarnated-canonical-doc-format` (load when authoring engine-internal canonical library docs needing header stamping)
- `reincarnated-critique-pair-gate-protocol` (load when Pattern A-deep + critique-pair gate is in play per hive-mind-protocol § 5.1)

### Specialized (rare)
- None at present

---

## 6. Update protocol for this skill

This is a thin operating-procedure skill — it should evolve when:
- A new mode emerges that wasn't captured in § 2
- A new discipline lands that affects the generation seam's decision-loop (§ 3)
- A new session-end pattern is observed in practice (§ 4)
- A new universal or cross-cutting skill is authored (§ 5)

Authored / maintained by **rocket** (self-update on observed practice changes). Sub-agent invocations of rocket may propose amendments; rocket approves before commit.

---

**Signed:** rocket (engine content-generation seam owner)
**For:** the universal session-start + mode-selection + session-end protocol for rocket invocations. Thin operating-procedure; specialized work-mode skills compose on top. Authored as Stream 2 sibling to the gandalf prototype, per `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-stream-2-per-agent-op-fan-out.md` brief § 2.1.
