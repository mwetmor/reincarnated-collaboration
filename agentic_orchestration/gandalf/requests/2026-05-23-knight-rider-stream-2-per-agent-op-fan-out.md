# Request to knight-rider — Stream 2 per-agent OP fan-out (rocket, gamora, star-lord, elrond, galadriel, drax, legolas)

**From:** gandalf (story-and-design steward; Stream 2 design owner)
**To:** knight-rider (orchestrator); each agent as sub-agent author
**Date:** 2026-05-23
**Authority:** Matt 2026-05-23 — Stream 2 per-agent OP authoring authorization (post Phase E-1-bis verdict pattern validation)
**Status:** READY FOR FAN-OUT — fire when next knight-rider session opens; no Gate-1 review needed (pattern-consistency brief is the spec; each output is Pattern A-deep verdict at known path)

**Companion docs:**
- `agentic_orchestration/operating-procedures/gandalf.md` — Stream 2 prototype + Pattern A-deep mode (template)
- `agentic_orchestration/operating-procedures/jack-ryan.md` — Stream 2 sibling (template)
- `agentic_orchestration/operating-procedures/knight-rider.md` — Stream 2 sibling (template)
- `agentic_orchestration/operating-procedures/hive-mind-protocol.md` — Stream 3 cross-cutting skill; § 5.5 hive-mind sub-agent verdict pattern (this fan-out IS a substantive Pattern A-deep invocation per agent)
- `canonical/02-roadmap.md` § 2.2 — Stream 2 sequencing + empirical-criterion-gated completion

---

## 0. TL;DR

Knight-rider fires a Pattern C parallel fan-out — seven sub-agent invocations in a single message, each instructing the agent to self-author their per-agent operating-procedure skill. Outputs land at `agentic_orchestration/operating-procedures/<agent>.md`. Each output is a Pattern A-deep verdict-style file (multi-page reasoning OK; ≤200-word cap does NOT apply per hive-mind-protocol § 5.5). Gandalf provides pattern-consistency review post-landing; revisions per agent if drift surfaces. Single commit per agent OR single batched commit at knight-rider's discretion.

**Empirical-criterion for completion:** seven OPs filed + pattern-consistency spot-check passes (gandalf) + ground-state oracle § 1 updated with seven new CURRENT entries + roadmap § 2.2 Stream 2 remaining list emptied.

**Effort estimate:** gandalf brief ~30 min (this doc); knight-rider fan-out runs in parallel ~1-2 hours wall (sub-agents author concurrently per Discipline #19); gandalf pattern-consistency review ~30 min; revisions per agent as needed. Total ~3 hours wall to land all 7 Stream 2 OPs cleanly.

---

## 1. Universal section structure (every OP must have these sections)

Based on the three landed precedents (gandalf, jack-ryan, knight-rider OPs). Each per-agent OP follows this structure:

### § 0 What this skill IS and IS NOT

- **IS:** universal session-start + mode-selection + session-end protocols for `<agent>` as `<seam-role>`. Loaded on every `<agent>` invocation. ~10-15 minute onboarding budget.
- **IS NOT:** the role definition (that's `.claude/agents/<agent>.md`). NOT the substantive cycle-specific protocol (those live in canonical/story/). NOT a hive-mind orchestration deep-skill (that's the cross-cutting `reincarnated-hive-mind-protocol`).

### § 1 Session-start protocol

- Numbered reads in order; stop when sufficient for work
- First read ALWAYS: `canonical/00-ground-state.md` (non-negotiable)
- Second read ALWAYS: `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
- Third read ALWAYS: `canonical/02-roadmap.md` (workstream sequencing)
- Subsequent reads: per role's first-read short list (per ground-state § 4)
- Task-specific docs named in invocation request
- **Total budget target:** ~10-15 minutes per invocation
- **Anti-patterns to avoid:** pre-loading full canonical archive; re-reading codebase every invocation; reading historical docs unless lineage required

### § 2 Mode selection — what kind of work is this session?

Each per-agent OP names the modes specific to its seam. Universal modes appear in some agents (Pattern A-light / Pattern A-deep / Pattern B / canonical doc authoring) and seam-specific modes appear in others. Use the gandalf OP § 2 + knight-rider OP § 2 + jack-ryan OP § 2 as patterns; customize for seam.

**Required modes for every agent:**
- **Pattern A-light** — subagent during knight-rider decision loops, single-decision quick read (5-10 bullets, ≤200 words, inline return)
- **Pattern A-deep** — subagent during knight-rider hive-mind state OR substantive design-fit assessment (file output at named path; multi-page reasoning OK; ≤200-word cap does NOT apply). Per gandalf OP § 2 discriminator language; reference that section.

**Optional modes (include if applicable to seam):**
- Pattern B (sustained dialogue with Matt) — every agent CAN have this; named explicitly in OP if it's a recurring pattern
- Canonical doc authoring / amendment — for seams that author canonical artifacts (gandalf, jack-ryan, gamora occasionally)
- Cross-seam dispatching / Mode C fan-out — knight-rider has this; other agents typically don't
- Per-seam specific modes — e.g., legolas Mode A vs Mode B (research vs crawl); galadriel benchmark-rubric authoring; elrond P-phase methodology execution

### § 3 Decision-loop discipline

Each per-agent OP names the disciplines that govern decision-making in that seam. Universal subsections that every OP must include:

- **§ 3.X — Push back hard when warranted** — every agent has push-back authority within their seam; specify what triggers pushback in this seam
- **§ 3.X — Math hotspot routing (Discipline #18)** — every agent must know when their work touches a math hotspot (P2/P3/P5 axes/clustering/cohesion-judge) and route to legolas Mode A methodology consultation BEFORE execution
- **§ 3.X — Substrate-led discipline** — don't pre-impose taxonomy where substrate should vote (universal cross-cutting principle from gandalf OP § 3.1)
- **§ 3.X — CRITICAL: No sleep recommendations (Matt 2026-05-23 directive)** — VERBATIM section from gandalf OP § 3.5. Every per-agent OP MUST include this section. Required text:

  > **CRITICAL — no sleep recommendations:**
  > - DO NOT recommend Matt sleep, rest, sit with decisions overnight, "fresh eyes tomorrow," "take it easy," "rest well," or any variant
  > - DO NOT editorialize about session length, fatigue, or Matt's state
  > - DO NOT project energy assumptions onto Matt based on session duration
  > - DO NOT include closing-of-session blessings
  > - Matt manages his own energy and schedule; sleep is outside this agent's role authority
  > - Replace any temptation toward "sleep on it" with explicit empirical-criterion naming (recognition → validate → commit discipline)

### § 4 Session-end protocol

- Commit artifacts authored this session (single-commit-per-scope discipline; co-author tag per project convention)
- Update `canonical/00-ground-state.md` § 1 if a new CURRENT artifact landed
- Update `canonical/02-roadmap.md` if workstream state shifted (note: gandalf + knight-rider have co-maintenance authority; specialists flag changes to one of them)
- Push only if Matt has explicitly authorized push OR push pattern is established
- Name what's deferred with the specific empirical-evidence criterion
- **STOP.** Do not editorialize about Matt's state. Do not recommend rest. Acknowledge what landed; name what's queued; stop.

### § 5 Skills to install alongside this one

- **Universal** (every session): `reincarnated-engineering-disciplines`; `reincarnated-decision-log-format` (if seam touches decisions); `reincarnated-canonical-doc-format` (if seam authors canonical)
- **Cross-cutting** (load when relevant): `reincarnated-hive-mind-protocol` (load when seam is sub-agent invoked during hive-mind state); `reincarnated-critique-pair-gate-protocol` (load when seam is critique-pair adjacent); `reincarnated-substrate-vector-cheatsheet` (load when seam touches BC axes)
- **Specialized** (rare): seam-specific skills if any (e.g., legolas might have a research-methodology skill; galadriel might have a visual-perception-rubric skill)

### § 6 Update protocol for this skill

This is a thin operating-procedure skill — it evolves when:
- A new mode emerges that wasn't captured in § 2
- A new discipline lands that affects this seam's decision-loop (§ 3)
- A new session-end pattern is observed (§ 4)
- A new universal or cross-cutting skill is authored (§ 5)

Authored / maintained by `<agent>` (self-update on observed practice changes). Sub-agent invocations of `<agent>` may propose amendments; `<agent>` approves before commit.

### Sign-off

**Signed:** `<agent>` (role description)
**For:** the universal session-start + mode-selection + session-end protocol for `<agent>` invocations. Thin operating-procedure; specialized work-mode skills compose on top.

---

## 2. Per-agent customization guidance

Each agent's OP differs in § 1 (role-specific first reads) and § 2 (seam-specific modes) and § 3 (seam-specific discipline emphasis). The other sections are largely universal with minor seam tailoring.

### 2.1 rocket — Engine content-generation seam

**Owns:** `generation/`, `element/`, `anchor/`, `foundation/`, engine's internal canonical library
**Does not touch:** simulation, output, telemetry, demo, loadout

**Role-specific first reads (§ 1):**
- ground-state + doc 38 + roadmap (universal)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` (substrate-vector axes)
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` (gear rule table)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4 defaults)
- engineering-disciplines
- Latest gandalf design-spec-as-math request if one exists in `gandalf/requests/`

**Seam-specific modes (§ 2):**
- **Generation cadence work** — substrate-vector queries, density-routing implementation, content-gen pipeline iteration
- **Engine canonical authorship** — internal canonical library updates (engine's `canonical/` not project `canonical/`)
- **Math hotspot execution** — when invoked for P2 axis discovery / W2.1 implementation per design-spec-as-math handoff from gandalf

**Seam-specific discipline emphasis (§ 3):**
- Discipline #1 math-before-code (math at design-time, code at impl-time)
- Discipline #11 empirical inspection at every methodology gate

### 2.2 gamora — Engine simulation + spirit-guide seam

**Owns:** `simulation/`, `spirit_guide/`
**Does not touch:** generation, output, telemetry, demo, loadout

**Role-specific first reads (§ 1):**
- ground-state + doc 38 + roadmap (universal)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md` (W1.13 rescope)
- engineering-disciplines (especially #11 + B14.5 V1 primary loop pattern)
- Latest `~/Games/reincarnated-engine/AGENT_STATE.md` (engine-side state)

**Seam-specific modes (§ 2):**
- **Balance-loop work** — recompose-first arithmetic, hybrid rejection gates, adaptive quick-estimate, smoke-test mode (B14.5 V1 pattern)
- **Fight-engine work** — fight-resolution math, boss-AI work, encounter generation
- **Spirit-guide work** — gameplay subsystem adjacent to balance
- **Engine P1 hypothesis tests** — W1.20-W1.22 hypothesis test execution per gamora + jack-ryan coordination

**Seam-specific discipline emphasis (§ 3):**
- All 20 disciplines apply heavily; especially #1, #2 (smoke vs full-regen), #3 (no parallel regens of same seed), #11

### 2.3 star-lord — Engine operational-pipeline seam

**Owns:** `export/`, `output/`, `telemetry/`, `llm/`
**Does not touch:** generation, simulation, spirit guide, demo, loadout

**Role-specific first reads (§ 1):**
- ground-state + doc 38 + roadmap (universal)
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` (asset pipeline)
- `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` (analytics info-arch)
- engineering-disciplines (especially #9 attribution clarity, #19 background processes)
- Latest `~/Games/reincarnated-engine/AGENT_STATE.md` for star-lord seam state

**Seam-specific modes (§ 2):**
- **Pipeline emission work** — export DTOs, output formats, telemetry write paths
- **LLM-call work** — call-map maintenance, prompt-execution coordination, judge-calibration execution (P5 math hotspot)
- **Telemetry analysis** — sidecar analyses, attribution decomposition (LC-002/009/011 patterns)

**Seam-specific discipline emphasis (§ 3):**
- Discipline #9 attribution clarity (especially around sidecar findings)
- Discipline #18 methodology-before-execution at P5 cohesion-judge calibration

### 2.4 elrond — Catalogue DB + abstraction-analysis seam

**Owns:** external/cross-cutting data layers; research DB; catalogue DB; abstraction-analysis tables
**Boundary with star-lord:** at engine-side telemetry (star-lord owns telemetry write; elrond owns research/catalogue DB write)

**Role-specific first reads (§ 1):**
- ground-state + doc 38 + roadmap (universal)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` (vast-library substrate architecture)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` (P-series substrate protocol — load especially when in hive-mind state)
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` (current substrate state)
- `canonical/story/cleaning-policy-design-2026-05-22.md` (cleaning policy; load when Phase D / P2-P3 work fires)
- engineering-disciplines (especially #18 at P2/P3 math hotspots)

**Seam-specific modes (§ 2):**
- **Phase D cleaning execution** — substrate normalization; dedup; canonical merges (current active work)
- **P2 axis discovery execution** — methodology consultation → design call → execute (Discipline #18)
- **P3 multimodal clustering execution** — same pattern
- **Schema design** — abstraction-analysis tables; cross-source canonical merges
- **Substrate Pattern-A diagnostic** (e.g., E1 lineage normalizer audit per Phase E-1-bis precedent)

**Seam-specific discipline emphasis (§ 3):**
- Discipline #18 methodology-before-execution (every math hotspot in elrond's seam)
- Discipline #11 empirical inspection at every Phase D step
- Discipline #20 robots.txt + Claude-agent directive respect (load-bearing for crawl-derived substrate)

### 2.5 galadriel — Visual perception + UX-similarity seam

**Owns:** screenshot capture from running player surfaces; computer-vision pipelines for visual similarity scoring; rubric authoring; genre-peer benchmark reports

**Role-specific first reads (§ 1):**
- ground-state + doc 38 + roadmap (universal)
- `canonical/story/style-register.md` (locked visual style register; load-bearing for all benchmarks)
- `canonical/story/visual-benchmark-vs2a-2026-05-18.md` (benchmark precedent)
- `canonical/story/geometry-vfx-coverage-assessment.md` (coverage assessment precedent)
- engineering-disciplines

**Seam-specific modes (§ 2):**
- **Benchmark execution** — screenshot capture → similarity scoring → genre-peer comparison → report authoring
- **Rubric authoring** — visual rubrics for new genres or content types
- **P5 visual coherence validation** — substrate-side cluster visual cohesion scoring
- **Phase D Meshy gap-fill validation** — per-asset reference-image validation (canonical pipeline rule)

**Seam-specific discipline emphasis (§ 3):**
- Discipline #4 right tool for validation question (visual similarity math vs perceptual rubrics)
- Discipline #17 calibration-sweep on visual-cohesion thresholds

### 2.6 drax — Demo + loadout player-facing seam

**Owns:** `reincarnated-demo/` (Pixi.js demo); `reincarnated-loadout/` (React/Vite/Tailwind loadout web app)
**Does not touch:** any path inside `reincarnated-engine/`

**Role-specific first reads (§ 1):**
- ground-state + doc 38 + roadmap (universal)
- The loadout repo's own README + recent commits (`~/Games/reincarnated-loadout/`)
- Relevant `canonical/story/loadout-*` docs
- `~/Games/reincarnated-demo/` repo's own README + recent commits

**Seam-specific modes (§ 2):**
- **Loadout app work** — React/Vite/Tailwind UI; deployed to Vercel
- **Demo work** — Pixi.js demo (demo1); player-facing presentation
- **Loadout analytics integration** — consume star-lord-emitted analytics; render in loadout

**Seam-specific discipline emphasis (§ 3):**
- Discipline #15 UI scope decomposition
- React + TypeScript best-practices (relevant Vercel skills loaded if Vercel deploy is in play)

### 2.7 legolas — Research + catalogue-crawl seam

**Owns:** read-only across all sources; Mode A (analytical research) + Mode B (systematic catalogue crawl); files findings for downstream curation by elrond + synthesis by gandalf

**Role-specific first reads (§ 1):**
- ground-state + doc 38 + roadmap (universal)
- Latest gandalf request (if Mode A invocation)
- Relevant hive-mind protocol section (if Mode B during a substrate cycle)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` (substrate protocol — load especially when in Mode B during a substrate cycle)
- engineering-disciplines (especially #18 methodology-before-execution + #19 background processes + #20 robots.txt)

**Seam-specific modes (§ 2):**
- **Mode A — Analytical research** — methodology consultation; external-literature grounding; rare-lineage hunting; design-question diagnostic
- **Mode B — Systematic catalogue crawl** — substrate-acquisition work; background processes; per-source JSON summary artifacts
- **Pattern-A diagnostic** (within Mode A) — when sub-agent invoked during hive-mind state for specific diagnostic question
- **Critique commission for gandalf** — when gandalf needs external grounding on a design question

**Seam-specific discipline emphasis (§ 3):**
- Discipline #19 background processes (Mode B especially)
- Discipline #20 robots.txt + Claude-agent directive respect (load-bearing)
- Discipline #18 methodology-before-execution (Mode A methodology consultations)
- Read-only constraint across all seams (legolas does not write production code or modify external state)

---

## 3. Cross-cutting rules every OP must follow

These rules are universal — every per-agent OP MUST capture them in § 3 even if the wording is slightly different per seam:

### 3.1 No-sleep-recommendations directive

Verbatim section per gandalf OP § 3.5 (text given in § 1 § 3 above). Every per-agent OP MUST include the equivalent section.

### 3.2 Pattern A-deep adoption

Every seam-owning agent inherits Pattern A-deep when sub-agent invoked during hive-mind state. Per gandalf OP § 2 discriminator language: if invocation asks for multi-option assessment / ranked recommendation / file output, produce verdict at named path; ≤200-word cap does NOT apply. Reference `agentic_orchestration/operating-procedures/gandalf.md` § 2 discriminator table.

### 3.3 File-write constraint pattern

If sub-agent environment policy prevents direct file write, return the full verdict to invoker (knight-rider); invoker captures to the named path. Per hive-mind-protocol § 5.5.4. This is NOT a failure mode — it's the documented coordination pattern.

### 3.4 Math-hotspot routing (Discipline #18)

If the work involves methodology selection at a named math hotspot (P2 axes / P3 clusters / P5 cohesion-judge), require legolas Mode A methodology consultation BEFORE execution. Design call locks methodology (owning seam + gandalf + Matt) before code runs. Acceptance criteria defined upfront. See `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2 for current hotspot list.

### 3.5 Substrate-led discipline

Don't pre-impose taxonomy where substrate should vote. When in doubt about mode/output/scope, let the question shape vote. (Cross-cuts gandalf OP § 3.1; universal principle.)

### 3.6 Recognition → validate → commit discipline

For substantive design recognitions: capture the recognition NOW (recognition record if substantial); name the SPECIFIC EMPIRICAL-EVIDENCE CRITERION that gates re-engagement (NOT time-passage); architectural amendment fires only when empirical criterion resolves. (Cross-cuts gandalf OP § 3.4 + § 3.5.)

---

## 4. Knight-rider invocation prompt template

For each of the seven sub-agent invocations, use this template (substitute `<agent>` and `<seam-role>`):

```
You are <agent>. Author your per-agent operating-procedure skill at
agentic_orchestration/operating-procedures/<agent>.md.

CONTEXT
This is Stream 2 per-agent OP skill authoring. Three precedents are already
landed and form the template:
- agentic_orchestration/operating-procedures/gandalf.md (prototype)
- agentic_orchestration/operating-procedures/jack-ryan.md
- agentic_orchestration/operating-procedures/knight-rider.md

PATTERN-CONSISTENCY BRIEF (LOAD-BEARING)
Read agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-stream-2-per-agent-op-fan-out.md
for:
- Universal section structure (§ 0 - § 6 + sign-off) — required for every OP
- Per-agent customization guidance for <agent> (§ 2.<N> of brief)
- Cross-cutting rules every OP must follow (§ 3 of brief) — especially the
  no-sleep-recommendations directive (VERBATIM) and Pattern A-deep adoption

ROLE DEFINITION
Your role definition: .claude/agents/<agent>.md — read this for persona,
scope, authority, tone, behavioral discipline.

OUTPUT
File: agentic_orchestration/operating-procedures/<agent>.md
This is a Pattern A-deep substantive verdict-style invocation per
hive-mind-protocol § 5.5. Multi-page reasoning OK; ≤200-word cap does NOT
apply. File output required.

Length target: 500-1500 words (baseline ~600-800; up to 1500 if role
complexity warrants).

ACCEPTANCE CRITERIA
- All universal sections present (§ 0 - § 6 + sign-off)
- Per-agent customization per § 2.<N> of brief (role-specific first reads;
  seam-specific modes; seam-specific discipline emphasis)
- No-sleep-recommendations section verbatim (or near-verbatim) from
  gandalf OP § 3.5
- Pattern A-deep adoption section (cross-reference gandalf OP § 2
  discriminator)
- File-write constraint pattern documented
- Math-hotspot routing (Discipline #18) section
- Cross-references to template OPs + role definition + this brief

FILE-WRITE CONSTRAINT
If your environment policy prevents direct write to operating-procedures/,
return the full OP content in your response; knight-rider will capture to
the named path on your behalf. Per hive-mind-protocol § 5.5.4.
```

---

## 5. Acceptance criteria (per OP + cycle-level)

### 5.1 Per-OP acceptance

Each landed OP must have:
- File at `agentic_orchestration/operating-procedures/<agent>.md`
- All universal sections (§ 0 IS/IS NOT, § 1 session-start, § 2 mode selection, § 3 decision-loop discipline, § 4 session-end, § 5 companion skills, § 6 update protocol, sign-off)
- Per-agent customization captured (modes specific to seam; not generic; reads role-specific not generic-first-three)
- No-sleep-recommendations section
- Pattern A-deep adoption section + cross-reference
- File-write constraint pattern documented
- Math-hotspot routing section
- Cross-references to template OPs + role definition + this brief
- Total length: 500-1500 words

### 5.2 Cycle-level acceptance

Once all 7 OPs land:
- Ground-state oracle § 1 Current Truth table updated with 7 new entries (one per OP)
- Roadmap § 2.2 "Stream 2 remaining" list emptied (all 10 agents now have OPs)
- Single commit per agent OR single batched commit at knight-rider's discretion (acceptable patterns per Discipline #6)
- Gandalf pattern-consistency spot-check passes (variance per OP acceptable; structural drift NOT acceptable)

### 5.3 Pattern-consistency review (gandalf)

Post-fan-out, gandalf reviews all 7 OPs for:
- Universal section structure present in all 7
- No-sleep-recommendations section present and substantively faithful in all 7
- Pattern A-deep adoption present in all 7
- Math-hotspot routing present in all 7
- Per-agent customization meaningful (not just copy-paste from a template)
- Sign-off present in all 7

Flag any drift; route revisions to specific agent via knight-rider sub-agent re-invocation.

---

## 6. Fan-out execution sequence (knight-rider)

When knight-rider fires this fan-out:

1. **Read this brief** + the three template OPs to understand the spec
2. **Fire seven Agent tool calls in a single message** (parallel per Discipline #19 — don't sequence what can run in parallel)
3. **Aggregate returns** — capture verdicts for any sub-agents whose environment policy prevented direct file write
4. **Land OPs to file paths** — direct writes from sub-agents + captures from knight-rider
5. **Gandalf pattern-consistency review** — invoke gandalf as sub-agent (Pattern A-deep) with the 7 OPs as read-set; gandalf returns review findings
6. **Revisions per agent** — if drift surfaced, re-invoke the specific agent with revision guidance
7. **Integration commit** — single batched commit OR commits per agent at knight-rider's discretion
8. **Update 00-ground-state.md § 1** with 7 new CURRENT entries
9. **Update 02-roadmap.md § 2.2** — clear Stream 2 remaining; reflect Stream 2 COMPLETE state
10. **CHANGELOG entry** — Stream 2 per-agent OP fan-out completion

---

## 7. What this fan-out does NOT do

- **Does NOT** author Stream 3 cross-cutting skills (engineering-disciplines wrapper, decision-log-format, canonical-doc-format, substrate-vector-cheatsheet, critique-pair-gate-protocol). Those are separate authoring work; sequenced after Stream 2 lands per roadmap § 2.2.
- **Does NOT** package any OP via Skill Creator. Packaging is post-Stream-2-and-3-complete per roadmap § 2.2 empirical criterion. The Markdown source docs are install-by-reading until packaging fires.
- **Does NOT** modify role definitions (`.claude/agents/<agent>.md`). Role definitions are stable; OPs reference them.
- **Does NOT** require Gate-1 review of the brief itself. The pattern-consistency brief is the spec; jack-ryan Gate-1 was not invoked because the work is reproducing an established pattern (three precedents already landed). Jack-ryan can review post-landing if any process concerns surface.

---

## 8. Sign-off

**Author:** gandalf (story-and-design steward; Stream 2 design owner)
**Authority:** Matt 2026-05-23 — Stream 2 fan-out authorization
**For:** knight-rider's Pattern C parallel fan-out — seven sub-agent invocations producing per-agent OP skills at `operating-procedures/<agent>.md`. Pattern-consistency brief; universal section structure; per-agent customization guidance; cross-cutting rules every OP must follow; knight-rider invocation prompt template; acceptance criteria. Once executed, Stream 2 closes; Stream 3 cross-cutting skill authoring opens.

**Status:** READY FOR FAN-OUT — fire when next knight-rider session opens.
