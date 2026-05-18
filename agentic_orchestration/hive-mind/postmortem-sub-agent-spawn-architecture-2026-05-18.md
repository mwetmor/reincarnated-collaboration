# Postmortem — Sub-Agent Spawn Architecture (2026-05-18)

**Status:** Operational postmortem. Captures two architectural failures observed today + the root-cause analysis + recommended hive-mind protocol amendments + pattern prescriptions for future sprints.

**Author:** gandalf (synthesis), based on:
- Matt's diagnostic observation (2026-05-18 evening) — *"Overnight Knight-Rider could not call sub agents as he was a sub agent himself"*
- Empirical evidence from morning-briefing-2026-05-19 L3-2 entry + this evening's galadriel spawn failure

**Audience:** knight-rider (primary — owns the hive-mind protocol); jack-ryan (secondary — discipline-amendment territory); all agents (general awareness for future sprint authoring).

**Authorship discipline:** observational + diagnostic; recommends protocol amendments rather than unilaterally changing canon. Knight-rider drafts amendments; Matt approves; the hive-mind protocol doc gets the amendment ratified per ADR-002 convention.

---

## § 0 — TL;DR

Two architectural failures observed within ~12 hours:

1. **Overnight knight-rider could not spawn parallel sub-agent specialists.** Sprint dispatches sat unfired through the night despite being perfectly authored on disk. Knight-rider had no Task-tool / subagent-spawn capability in its session.
2. **Custom agents defined in `.claude/agents/` (e.g., galadriel) are not callable via Task tool subagent_type spawning.** They are only callable as top-level `claude --agent <name>` launches.

**Root cause (both):** The harness has *two different agent-invocation modes* with *different capabilities and different registries*, and the hive-mind protocol I authored assumed they were uniform. They are not.

| Invocation mode | Triggered by | Capabilities | Registry visibility |
|---|---|---|---|
| **Top-level session** | Matt running `claude --agent <name>` in a terminal | Full tool set, including subagent-spawn Task tool | Sees built-in agents + custom `.claude/agents/*.md` files |
| **Sub-agent spawn** | Another agent calling Task tool with `subagent_type=<name>` | Reduced tool set, NO further subagent-spawn capability | Sees only built-in agent types; custom agents invisible |

**Practical consequence:** ANY orchestration model that assumes a sub-agent can itself spawn further sub-agents is structurally broken. ANY orchestration model that assumes custom-defined agents are spawnable as sub-agents is structurally broken.

**Recommended hive-mind protocol amendments** (per § 4 below):
- Knight-rider operates ONLY as Matt-launched top-level session
- Specialists requiring production-state writes are Matt-launched top-level sessions
- Sub-agent spawn is reserved for analysis-only work (research, surveys, design critique)
- Custom agents are top-level-launch-only; do not invoke them via subagent_type Task call

---

## § 1 — The two failures observed today

### § 1.1 — Failure 1: Overnight knight-rider sub-agent spawn unavailable

**When:** 2026-05-18 ~03:30 local Matt time (overnight sprint activation).
**Where:** `agentic_orchestration/hive-mind/morning-briefing-2026-05-19.md` L3-2 entry (full disposition recorded there).
**What:**

Knight-rider authored the overnight sprint invocation (`agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md`) — the sprint design assumed knight-rider would spawn drax / galadriel / star-lord / elrond / jack-ryan as parallel sub-agents to execute the 8 queued dispatches autonomously through the night while Matt slept.

When knight-rider opened its session and attempted to fire specialists, the Task tool / subagent-spawn capability was simply not available. From the morning-briefing record:

> *"The Task tool / subagent-spawn mechanism is not available in this knight-rider session — only deferred tools related to background-shell-stopping, worktree-management, and web-fetch are surfaced; no Task-equivalent tool exists for spawning gandalf, drax, star-lord, elrond, or jack-ryan as parallel subagents."*

**Outcome:** The 8 sprint dispatches sat on disk perfectly authored. None executed through the night. Morning Matt opened individual specialist terminals manually; specialists executed the queued dispatches in a compressed morning window.

**Matt's diagnosis (2026-05-18 evening, definitive):**

> *"'Overnight Knight-Rider' could not call sub agents as he was a sub agent himself."*

Matt's reading is correct. Knight-rider was being invoked via `claude --agent knight-rider` — but the harness was treating that invocation as a sub-agent spawn (or as a session with reduced capabilities matching sub-agent spawn). The full top-level capability set wasn't present.

### § 1.2 — Failure 2: Custom-agent registry asymmetry

**When:** 2026-05-18 evening (post-meeting, during VS2a close-out work).
**Where:** This (gandalf) session attempting to spawn galadriel via Task tool.
**What:**

Gandalf attempted to fire galadriel as a background sub-agent to execute her capture-pipeline dispatch:

```
Agent({
  description: "Galadriel: capture pipeline + DoE state-matched captures",
  subagent_type: "galadriel",
  prompt: "[full dispatch context]",
  run_in_background: true,
})
```

The harness returned:

> *"Agent type 'galadriel' not found. Available agents: claude, claude-code-guide, drax, elrond, Explore, gamora, gandalf, general-purpose, jack-ryan, knight-rider, legolas, Plan, rocket, star-lord, statusline-setup, vercel:ai-architect, vercel:deployment-expert, vercel:performance-optimizer"*

But the galadriel agent definition file exists at `/Users/admin/Games/reincarnated-collaboration/.claude/agents/galadriel.md` (Matt-approved 2026-05-18 morning, committed at `85a4629`). And `claude --agent galadriel` works correctly at top-level launch — Matt has galadriel open in a separate terminal as a top-level session right now.

**The two agent-discovery mechanisms are not the same:**
- Top-level launch sees the `.claude/agents/` directory and registers custom agents
- Sub-agent spawn uses a fixed built-in registry that excludes custom agents

**Outcome:** Galadriel could not be spawned as a background sub-agent. Mitigation: Matt's already-open top-level galadriel terminal handles the work, gating only on explicit "proceed" from Matt.

### § 1.3 — Compounded effect

These two failures share a root cause but show up in two different operational scenarios:

- **Failure 1** breaks *autonomous-orchestration sprints* — any model where knight-rider (or any other agent) runs through the night executing queued work via sub-agent spawn
- **Failure 2** breaks *custom-agent integration* — any model where a newly-commissioned agent (galadriel today; potentially others later) is fired via subagent_type spawn from an existing session

Together: the assumption that *"any agent can spawn any other agent"* — implicit in the hive-mind protocol's coordination model — is wrong. The actual capability is constrained:

- **Top-level → sub-agent (built-in only):** works
- **Top-level → sub-agent (custom):** FAILS
- **Sub-agent → sub-agent (any type):** FAILS (no Task tool available)

---

## § 2 — Root cause analysis

The harness's design intent (inferred) is reasonable:

- Sub-agents are *delegated work* — they execute a defined task and return results to the spawning session. Allowing arbitrarily-deep sub-agent recursion creates control-flow + auditability problems (cost attribution, error propagation, debugging across spawn levels).
- Restricting custom-agent visibility to top-level launch is *probably* defensive — prevents a sub-agent from being silently augmented with custom code/persona that wasn't sanctioned at session start.

These are defensible design choices at the harness layer. The problem is not with the harness — it's that **the hive-mind protocol I authored didn't reflect these constraints accurately**.

The protocol's coordination-matrix assumed knight-rider as a *general-purpose orchestrator* with arbitrary spawn capability. The actual capability of knight-rider as a sub-agent is *narrower* — coordination via filesystem + hive log, not via direct agent invocation.

**The diagnostic pattern is generalizable:** assume the harness has *exactly the capabilities you've empirically observed*, not the capabilities the documentation or convention suggests. Protocols authored to ideal-capability assumptions will encounter exactly the empirical-capability mismatches that this postmortem documents.

---

## § 3 — The structural lesson — agent invocation modes are NOT uniform

The hive-mind protocol needs to recognize that agents exist in TWO modes with different capabilities:

### § 3.1 — Top-level session (full capability)

**How invoked:** Matt runs `claude --agent <name>` in a terminal.
**Tool availability:** Full set including Task tool (can spawn sub-agents). Bash, Read, Write, Edit, git, web, etc.
**Agent registry visibility:** Built-in agents + custom agents in `.claude/agents/*.md`.
**Use cases:**
- Long-running specialist work (drax shipping demo code; rocket regenerating seasons; star-lord building pipelines)
- Production-state-writing work (any git commit + push; any database write; any file system mutation in production paths)
- Multi-hour autonomous work
- Anything that needs to spawn analysis sub-agents itself

### § 3.2 — Sub-agent spawn (reduced capability)

**How invoked:** Another session calls Task tool with `subagent_type=<name>`.
**Tool availability:** REDUCED — no Task tool available; cannot spawn further sub-agents. Other tools (Bash, Read, etc.) may also be more constrained.
**Agent registry visibility:** Built-in agent types ONLY; custom `.claude/agents/*.md` agents invisible.
**Use cases:**
- Analysis-only work (Legolas Mode A research; Explore-style codebase surveys)
- Time-bounded delegated tasks
- Single-author deliverables that return results to the spawning session

### § 3.3 — The capability matrix

| Operation | Top-level can do? | Sub-agent can do? |
|---|---|---|
| Read codebase, run bash | ✅ | ✅ |
| Write to non-production paths (agentic_orchestration/, canonical/story/) | ✅ | ✅ |
| Write to production paths (engine src, demo src, loadout src) | ✅ | ✅ (observed, though risk-elevated) |
| Git commit + push | ✅ | ✅ (observed) |
| Spawn further sub-agents (Task tool) | ✅ | ❌ |
| Invoke built-in subagent types | ✅ | ❌ |
| Invoke custom-defined agents | ✅ (top-level launch) | ❌ |
| Run long-duration work (hours) | ✅ | ⚠️ Harness timeout risk (see bulk_reroll death) |
| Maintain session state across multi-turn interaction with Matt | ✅ | ❌ (one-shot return) |

**Capability that empirically WORKED for production-state-writing sub-agents today:**
- star-lord (built-in agent type) fired as background sub-agent successfully executed image-gen pipeline + git push (commits `97cbaaf`, `b563134`)
- drax (built-in agent type) fired as background sub-agent successfully built React components + git push (commit `ea434d4`)

**Capability that empirically DID NOT work:**
- galadriel (custom agent) fired as sub-agent → "Agent type not found"
- knight-rider (built-in) fired as sub-agent attempted to spawn further sub-agents → no Task tool available
- bulk_reroll background Python process running under sub-agent → silent termination at harness timeout (~10 min)

---

## § 4 — Recommended hive-mind protocol amendments

These are *recommendations*, not unilateral changes. Knight-rider owns the protocol; this postmortem surfaces what to amend; the formal amendment lands via knight-rider authoring + Matt approval per ADR-002.

### § 4.1 — Amendment A: Knight-rider invocation discipline

**Current implicit assumption:** Knight-rider can be invoked autonomously via sub-agent spawn for overnight orchestration sprints.

**Amended:** Knight-rider operates ONLY as Matt-launched top-level session. Autonomous-orchestration sprints (the "Matt-AFK overnight" model) require knight-rider to have been launched at top-level BEFORE Matt steps away. Sub-agent-spawned knight-rider is not a supported mode.

**Practical implication for sprint authoring:** sprint invocations addressed to knight-rider should explicitly assume top-level invocation; should NOT specify "knight-rider spawns specialists as sub-agents" as a coordination mechanism.

### § 4.2 — Amendment B: Specialist invocation discipline

**Current implicit assumption:** Any specialist (drax, rocket, gamora, star-lord, elrond, gandalf, jack-ryan, galadriel) can be invoked via sub-agent spawn for any kind of work.

**Amended:** Production-state-writing work (git commits to production paths; database writes; engine/demo/loadout code changes) should be executed in Matt-launched top-level specialist sessions. Sub-agent spawn of specialists is permitted but DISCOURAGED for production-write work; PREFERRED for analysis-only delegated tasks (research, design surveys, validation passes).

**Practical implication:** the multi-terminal pattern (Matt opens drax + rocket + star-lord + elrond in 4 separate terminals; each runs as a top-level session reading dispatches from filesystem) is the canonical execution pattern. Sub-agent spawn is the *exception*, used for: (a) analysis-only work (Legolas research, gandalf surveys), (b) one-shot delegated tasks that don't need multi-turn dialogue with Matt, (c) work where the sub-agent's failure or silent death is acceptable.

### § 4.3 — Amendment C: Custom-agent invocation discipline

**Current implicit assumption:** Custom-defined agents in `.claude/agents/` are uniformly callable.

**Amended:** Custom-defined agents are TOP-LEVEL-LAUNCH-ONLY. Do not attempt to invoke via Task tool's `subagent_type` parameter — the registry asymmetry will return "Agent type not found." When commissioning a new custom agent, the commission MUST include a launch protocol that names "Matt opens a fresh terminal and runs `claude --agent <name>`."

**Practical implication:** the galadriel commission should have included explicit instruction: *"Galadriel is invoked at top-level only via `cd ~/Games/reincarnated-collaboration && claude --agent galadriel`. Do not spawn galadriel via Task subagent_type — this will fail with 'Agent type not found.'"* Future custom-agent commissions follow this pattern.

### § 4.4 — Amendment D: Autonomous-sprint architecture revision

**Current implicit model:** Knight-rider (top-level) authors sprint invocation; spawns specialists as parallel sub-agents to execute through night; Matt sleeps.

**Amended autonomous-sprint architecture options:**

**Option α — Manual top-level fanout.** Matt opens N terminals at sprint-start, each launching the relevant specialist at top-level. Knight-rider in an N+1th terminal coordinates by reading hive log + writing dispatch files. Matt-time-at-start; autonomy-thereafter. **This is the realistic pattern for solo-dev capacity.**

**Option β — Scheduled top-level fanout.** Use the `schedule` skill or `CronCreate` to fire specialist sessions at staggered top-level invocations through the night. Each specialist reads its queued dispatch, executes, exits. Coordination via filesystem. **Best for sequential / serial work; less good for parallel cross-seam coordination.**

**Option γ — Dispatch-queue mode with morning execution.** Knight-rider (top-level) authors dispatches through the night; specialists pick them up in morning execution windows (Matt launches them then). **What actually happened on 2026-05-18 — recovers gracefully from spawn failure but loses the autonomous-overnight benefit.**

**Option δ — Hybrid: top-level orchestrator + analysis-only sub-agents.** Knight-rider (top-level) does its own coordination work; spawns sub-agents only for ANALYSIS work (e.g., "Legolas, scout this question") not for production work. Production work waits for top-level specialist sessions to pick up dispatches. **Realistic + safe.**

**Recommendation:** the hive-mind protocol should formally name Option δ as the canonical pattern, with α and β as escalations when sustained autonomous overnight work is genuinely needed.

---

## § 5 — Tonight's mitigation pattern (acknowledged inconsistency)

Tonight (2026-05-18 evening) the two close-out tasks were dispatched via two different patterns:

- **star-lord** (multi-season encounter analytics) — fired as background sub-agent from this gandalf session. Violates the recommendation in § 4.2. **Pragmatic decision:** star-lord is a built-in agent type; background sub-agent spawn has been observed to work for production-write work (this morning's image-gen pipeline ran successfully via this pattern); the close-out work is path-agnostic and time-pressured.
- **galadriel** (capture pipeline) — running as Matt-launched top-level session in separate terminal. Conforms to § 4.3 and § 4.2.

**The inconsistency is honestly named.** Star-lord's background-spawn pattern is *expedient* tonight; future sprints should default to Matt's-terminal-as-top-level pattern. If star-lord's background work tonight halts or fails, the fallback is exactly: Matt opens a star-lord top-level terminal and re-runs the dispatch.

This mirrors the canonical pattern from CLAUDE.md:

```bash
# Coordinator session (start of day)
cd ~/Games/reincarnated-collaboration && claude --agent knight-rider

# Specialist sessions (task work)
cd ~/Games/reincarnated-engine && claude --agent gamora       # or rocket, star-lord
cd ~/Games/reincarnated-loadout && claude --agent drax        # or reincarnated-demo
```

The pattern was already documented; the hive-mind protocol just didn't honor it. Amendment D § 4.4 formalizes the protocol to match the documented launch convention.

---

## § 6 — Related observations (worth surfacing as separate findings)

### § 6.1 — Harness timeout for long-running sub-agents

The bulk_reroll_anatomy.py background process running under a sub-agent died silently after ~10 minutes (post-hoc diagnosed by star-lord as harness timeout). The agent didn't crash; the agent harness terminated it. **Implication:** sub-agent invocations have an implicit duration ceiling significantly lower than top-level sessions. Long-running work (hours) is structurally unsuited to sub-agent spawn.

This is a third axis of capability asymmetry — sub-agents have time-bounded execution windows that top-level sessions don't share. Should be noted in any protocol amendment.

### § 6.2 — Cost/attribution friction across spawn modes

Sub-agent spawns return results as opaque text to the spawning session; the spawning session can't directly observe cost ledger entries, intermediate artifacts, or partial progress. Today's image-gen pipeline correctly logged cost via the ledger file (filesystem-mediated), but mid-run progress observability required out-of-band file polling (`ls _reroll_all/*/*.png | wc -l`). This is fine for short tasks; awkward for hours-long work. Top-level sessions don't have this asymmetry.

### § 6.3 — Knight-rider role at top-level vs sub-agent — actual capability delta

Top-level knight-rider has the Task tool; sub-agent knight-rider does not. The protocol-level *role* of knight-rider (read-everything, write-coordination-docs, orchestrate-via-dispatches) is theoretically identical across modes, BUT the *mechanism* differs: top-level knight-rider can fire analysis sub-agents (Legolas, Explore); sub-agent knight-rider cannot. Worth noting in the role definition itself, not just the protocol.

---

## § 7 — Open questions for follow-up

1. **Does jack-ryan-as-Gate-2-gatekeeper change under these constraints?** Jack-ryan reviews work; if jack-ryan is to be invoked as a sub-agent for a review pass, the same capability constraints apply (no Task spawning; harness timeout). Worth jack-ryan's review of his own role under the constraints.

2. **Is there a way to test sub-agent vs top-level capability at session start?** A "capability probe" early in any agent's session that surfaces what tools are actually available — would prevent the runtime-discovery-of-missing-capability surprise.

3. **Should custom-agent commissions include a launch-protocol section?** Galadriel's commission (in the overnight sprint invocation § 4) did not name "top-level launch only." Future commissions should. A template amendment.

4. **How does this interact with the `schedule` / `CronCreate` / wakeup tools?** Scheduled work IS top-level launch (fresh session per fire); should naturally avoid the sub-agent constraints. Worth verifying empirically before relying on it for autonomous-overnight sprints.

5. **Does any of this change with future harness versions?** This postmortem captures the constraints AS OF 2026-05-18. The harness evolves; future versions may relax or change these constraints. Worth re-validating quarterly.

---

## § 8 — Cross-references

- `agentic_orchestration/hive-mind/morning-briefing-2026-05-19.md` — original L3-2 entry surfacing Failure 1 empirically
- `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` — the overnight sprint invocation that assumed the broken capability
- `.claude/agents/galadriel.md` — the custom agent file that exists on disk but is invisible to sub-agent spawn
- `CLAUDE.md` (project root) — the documented launch convention that the protocol should honor
- `agentic_orchestration/AGENTS.md` — agent topology + scope map (may benefit from amendment naming top-level-vs-sub-agent capability)
- `canonical/story/apex-director-debrief-2026-05-18.md` § 6 — the discipline-floor that this postmortem informs ("DO NOT pivot Phase-1 P1 scope on reactive feedback alone" applies to architectural pivots too — this postmortem recommends amendments, not unilateral protocol changes)

---

## § 9 — Provenance

- **Observation date:** 2026-05-18 (both failures within a 12-hour window)
- **Diagnostic credit:** Matt — *"'Overnight Knight-Rider' could not call sub agents as he was a sub agent himself"* — definitive root-cause naming
- **Empirical evidence:**
  - Morning-briefing-2026-05-19 L3-2 (Failure 1 record)
  - Gandalf session 2026-05-18 evening Agent() invocation returning "Agent type 'galadriel' not found" (Failure 2 record)
  - Bulk_reroll_anatomy.py silent termination at ~10 min (Failure 3-ish; § 6.1 observation)
- **Author:** gandalf, 2026-05-18 evening, post-meeting close-out window
- **Status:** observational postmortem; recommendations to be ratified by knight-rider + Matt per ADR-002 amendment convention
- **Routing:** knight-rider (primary recipient — owns the hive-mind protocol amendments); jack-ryan (secondary — discipline-amendment territory); all agents (general awareness)

---

*Authored 2026-05-18 evening by gandalf, per Matt directive. Captures two architectural failures + root cause + recommended protocol amendments. The hive-mind protocol I authored assumed a uniform agent-invocation capability that does not exist; this postmortem names the asymmetry honestly so the next sprint architecture can be designed against the harness as it actually is, not as I imagined it. Mithrandir signs.*
