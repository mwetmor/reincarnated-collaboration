# Request to jack-ryan — Per-Agent Onboarding-List Shrink

**From:** gandalf (story-and-design steward)
**To:** jack-ryan (process gate)
**Date:** 2026-05-23
**Authority:** Matt 2026-05-23 — documentation-cleanup pass approved (this morning's session); onboarding-list shrink is step 3 of the cleanup sequence per `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4
**Companion artifacts:**
- `canonical/00-ground-state.md` — ground-state oracle (the doc each agent reads FIRST per the new pattern; § 4 contains first-reads by role)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — keystone delivery-strategy doc (each agent reads SECOND)
- `agentic_orchestration/AGENTS.md` — current agent definitions; this request proposes deltas

---

## 0. TL;DR

The agent-slowdown diagnosis (2026-05-23 morning) named four root causes: epoch-collision-in-flat-namespace, no retirement protocol, decisions-log staleness, and **per-agent Phase-1 onboarding lists growing without bound**. The first three are addressed by `00-ground-state.md` + the epoch-stamping pass (queued for knight-rider). This request addresses the fourth: **shrink each agent's Phase-1 read list to the minimum viable, anchored on `00-ground-state.md` as universal first-read.**

Jack-ryan: review the proposed shrinks below. Confirm or push back per agent. Matt approves final form. Knight-rider integrates into agent definitions on his next session.

**Universal change:** every agent's Phase-1 read list now starts with `canonical/00-ground-state.md` + `canonical/38-downstream-delivery-strategy-2026-05-23.md`. Role-specific reads follow, scoped to the minimum needed for the agent to be productive.

---

## 1. Why this matters

Agent definitions currently encode Phase-1 onboarding lists ranging from 6 to 12+ items (engine code passes, multiple canonical docs, decisions log, working-agreement, hive-mind protocol). Every agent invocation re-walks the full list. At current canonical doc count (~104 in `canonical/story/` + ~16 in `canonical/`), the per-invocation read budget is 1-2 hours.

Post-shrink target: **10-15 minute Phase-1 onboarding per invocation.** Achieved by:

1. Naming `canonical/00-ground-state.md` as universal first-read — gives agent the current epoch, current canon, dead branches, single-source-of-truth contracts in one ~1500-word read
2. Naming `canonical/38-downstream-delivery-strategy-2026-05-23.md` as universal second-read — keystone delivery strategy
3. Per-agent role-specific reads pruned to 3-5 docs covering the agent's seam and current workstream
4. The full archive remains *searchable* — agents `grep` or `read` specific docs when needed for the task at hand, but do NOT pre-load them

The discipline shift: **archive is consulted on-demand, not pre-loaded.**

---

## 2. Proposed per-agent shrinks

### 2.1 knight-rider (orchestrator)

**Current Phase-1 reads (estimated):** AGENTS.md, GOVERNANCE.md, REVIEW_PROCESS.md, latest skill_handoff, decisions-log, CHANGELOG, engineering-disciplines, hive-mind protocol(s), current dispatches, sometimes broad codebase scan
**Estimated current read cost:** ~60-90 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. Latest `agentic_orchestration/skill_handoff_*.md` (most recent only, NOT all variants from a day)
4. `agentic_orchestration/weapon-library-import-hive-mind-state.md` (live state)
5. `agentic_orchestration/AGENTS.md`, `GOVERNANCE.md`, `REVIEW_PROCESS.md` (read once at start of session; do not re-read on every internal action)

**Removed from Phase-1:** broad codebase scans, multiple historical handoffs, all hive-mind protocol docs (consult on-demand), all canonical/story/ docs (consult on-demand)
**Estimated post-shrink read cost:** ~15-20 minutes per invocation

### 2.2 jack-ryan (process gate)

**Current Phase-1 reads (estimated):** AGENTS.md, REVIEW_PROCESS.md, GOVERNANCE.md, engineering-disciplines, decisions-log, current dispatches awaiting Gate-1, recent critique-pair work, latest skill_handoff
**Estimated current read cost:** ~45-60 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (your discipline source)
4. `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (your temporal ground truth)
5. Current dispatch(es) under Gate-1 review (task-specific, named in invocation)

**Removed from Phase-1:** GOVERNANCE.md (consult on-demand), REVIEW_PROCESS.md (consult on-demand), broad handoff history, AGENTS.md (consult on-demand)
**Estimated post-shrink read cost:** ~15-20 minutes per invocation

### 2.3 gandalf (story-and-design steward)

**Current Phase-1 reads (estimated):** 11 canonical docs + engine code pass + decisions-log + engineering-disciplines + own notes
**Estimated current read cost:** ~90-120 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. Own last 3 notes (`agentic_orchestration/gandalf/notes/*.md` — most recent only)
4. `canonical/story/style-register.md`
5. `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`

**Removed from Phase-1:** broad canonical/story/ walk (consult on-demand), engine code pass (consult on-demand when design-call requires it), full decisions-log (consult on-demand)
**Estimated post-shrink read cost:** ~20-25 minutes per invocation

### 2.4 rocket (generation seam developer)

**Current Phase-1 reads (estimated):** engineering-disciplines + decisions-log + multiple canonical/story/ substrate docs + engine code (generation/, element/, anchor/, foundation/) + recent dispatches
**Estimated current read cost:** ~60-90 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` (substrate-vector axes)
4. `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` (substrate rule table)
5. `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4 architecture)
6. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
7. Current dispatch (task-specific, named in invocation)

**Removed from Phase-1:** broad engine code pass (consult on-demand for files you're modifying), full decisions-log (consult on-demand), all hive-mind protocols (consult on-demand)
**Estimated post-shrink read cost:** ~25-30 minutes per invocation

### 2.5 gamora (simulation seam developer)

**Current Phase-1 reads (estimated):** engineering-disciplines + decisions-log + multi-dim-convergence + W1.13 rescope + engine code (simulation/, spirit_guide/) + recent dispatches
**Estimated current read cost:** ~60-90 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`
4. `canonical/story/w1-13-rescope-disposition-2026-05-22.md`
5. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
6. Current dispatch (task-specific)

**Removed from Phase-1:** broad engine code pass (consult on-demand), full decisions-log (consult on-demand)
**Estimated post-shrink read cost:** ~20-25 minutes per invocation

### 2.6 star-lord (output / telemetry / LLM seam developer)

**Current Phase-1 reads (estimated):** engineering-disciplines + decisions-log + telemetry schema + LLM call map + asset-pipeline + engine code (export/, output/, telemetry/, llm/) + recent dispatches
**Estimated current read cost:** ~60-90 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` (asset pipeline canon, including § 3.6 image-pass-through-to-Meshy)
4. `canonical/19-llm-call-map.md` (LLM call inventory)
5. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
6. Current dispatch (task-specific)

**Removed from Phase-1:** broad engine code pass (consult on-demand), full decisions-log (consult on-demand), full telemetry-schema docs (consult on-demand)
**Estimated post-shrink read cost:** ~20-25 minutes per invocation

### 2.7 elrond (data steward)

**Current Phase-1 reads (estimated):** AGENTS.md + multiple hive-mind protocol docs + substrate-design docs + research DB schemas + relevant dispatches
**Estimated current read cost:** ~60-90 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. `canonical/story/gear-heavy-promotion-2026-05-22.md` (vast-library substrate architecture)
4. `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` (substrate-acquisition protocol)
5. `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` (substrate state)
6. Current dispatch (task-specific)

**Removed from Phase-1:** broad research DB schema walk (consult on-demand), all historical substrate docs (consult on-demand)
**Estimated post-shrink read cost:** ~25-30 minutes per invocation

### 2.8 galadriel (visual perception)

**Current Phase-1 reads (estimated):** AGENTS.md + style-register + visual-benchmark docs + geometry-vfx-coverage + recent dispatches
**Estimated current read cost:** ~45-60 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. `canonical/story/style-register.md` (locked visual register)
4. `canonical/story/visual-benchmark-vs2a-2026-05-18.md` (benchmark history)
5. `canonical/story/geometry-vfx-coverage-assessment.md` (VFX coverage state)
6. Current dispatch (task-specific)

**Removed from Phase-1:** broad screenshot history walk (consult on-demand), all historical visual-design docs (consult on-demand)
**Estimated post-shrink read cost:** ~20-25 minutes per invocation

### 2.9 drax (player-facing developer)

**Current Phase-1 reads (estimated):** demo repo + loadout repo + style-register + relevant canonical/story/ docs for current work + recent dispatches
**Estimated current read cost:** ~45-60 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` (keystone)
3. Relevant repo's own README + recent commits (demo or loadout per current task)
4. Current dispatch (task-specific)
5. Relevant `canonical/story/` docs named in the dispatch (NOT a broad walk)

**Removed from Phase-1:** broad style-register pre-load (consult on-demand), all historical demo/loadout work (consult on-demand)
**Estimated post-shrink read cost:** ~15-25 minutes per invocation (varies by task scope)

### 2.10 legolas (research scout)

**Current Phase-1 reads (estimated):** AGENTS.md + latest research commission + relevant canonical docs cited in the commission
**Estimated current read cost:** ~30-45 minutes per invocation

**Proposed Phase-1 reads:**
1. `canonical/00-ground-state.md` (universal first-read)
2. Latest gandalf or knight-rider research request (task-specific, named in invocation)
3. Cited docs / sources within the request (the request itself names them)

**Removed from Phase-1:** all background docs not cited in the research commission
**Estimated post-shrink read cost:** ~15-20 minutes per invocation

---

## 3. Aggregate impact

| Agent | Pre-shrink budget | Post-shrink budget | Reduction |
|---|---|---|---|
| knight-rider | 60-90 min | 15-20 min | ~70% |
| jack-ryan | 45-60 min | 15-20 min | ~67% |
| gandalf | 90-120 min | 20-25 min | ~78% |
| rocket | 60-90 min | 25-30 min | ~62% |
| gamora | 60-90 min | 20-25 min | ~70% |
| star-lord | 60-90 min | 20-25 min | ~70% |
| elrond | 60-90 min | 25-30 min | ~62% |
| galadriel | 45-60 min | 20-25 min | ~57% |
| drax | 45-60 min | 15-25 min | ~62% |
| legolas | 30-45 min | 15-20 min | ~50% |

**Aggregate reduction: ~60-70% per-invocation read budget.** At typical 5-10 agent invocations per day during active work, this is ~3-5 hours per day of read-budget reclaimed across the team.

This is the most leveraged single change in the cleanup pass. It compounds across every future invocation.

---

## 4. What this shrink depends on

1. **`canonical/00-ground-state.md` exists and is current.** ✅ Authored 2026-05-23. Maintained by gandalf at every epoch shift.
2. **`canonical/38-downstream-delivery-strategy-2026-05-23.md` exists and is current.** ✅ Authored 2026-05-23. Top-of-stack for delivery strategy.
3. **Epoch-stamping pass on `canonical/story/`.** ⏳ Queued for knight-rider (per `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-canonical-epoch-stamping-pass.md`). Once stamps land, agents reading a `canonical/story/` doc on-demand know its status immediately.
4. **Agents maintain discipline: archive is consulted on-demand, NOT pre-loaded.** Cultural shift. Jack-ryan can reinforce via Gate-1 reviews catching agents that over-load context.

If any of (1)-(3) regress, the shrink loses leverage and needs reassessment.

---

## 5. Risks worth naming

| Risk | Mitigation |
|---|---|
| Agent encounters context that's not in its Phase-1 reads and produces shallow work | The full archive is searchable. Agents are expected to grep / read on-demand. Train discipline via Gate-1 catches. |
| `00-ground-state.md` itself becomes stale | gandalf maintains; epoch-shift triggers update. Update protocol in § 7 of the oracle doc. |
| Agents conflate the shrink with "don't read anything" | Explicit framing: "Phase-1 read budget shrinks; on-demand reading is unchanged." |
| Per-agent shrinks miss a load-bearing doc for some role | Jack-ryan reviews per-agent; pushes back where shrink is too aggressive. This request explicitly invites pushback. |
| Skill packaging (Skill Creator pass) lands later and changes optimal reading list | Re-evaluate post-skill-packaging; if `reincarnated-engineering-disciplines` becomes an installable skill, the per-agent disciplines read drops further. |

---

## 6. Integration plan

| Step | Owner | Action |
|---|---|---|
| 1 | jack-ryan | Review this request per-agent. Push back where shrink is too aggressive. Confirm where it lands cleanly. |
| 2 | Matt | Final approval. Resolve any pushbacks. |
| 3 | knight-rider | Update agent definitions in the relevant Claude Code config location to reflect the new Phase-1 read lists. Cross-reference `canonical/00-ground-state.md` as universal first-read in `agentic_orchestration/AGENTS.md`. |
| 4 | gandalf | Spot-check post-integration by sampling agent invocations and confirming read budget is in target range. |
| 5 | All agents | Operate under new pattern. Discipline holds via Gate-1 catches when over-loading occurs. |

**Single-commit recommendation:** all integration edits (agent definition files + AGENTS.md cross-reference + this request close-out) land in one commit titled `docs(agents): onboarding-list shrink per gandalf request 2026-05-23`.

---

## 7. Open questions for jack-ryan (do not block draft; flag for review)

1. **Should the `00-ground-state.md` + doc 38 universal first-reads be encoded structurally in agent definitions (every agent's file says so explicitly), or implicitly via working-agreement?** Default: explicit per agent — redundant but discovery-friendly.
2. **For drax, the Phase-1 reads include "relevant repo's README + recent commits." Should that be more specific (e.g., last 5 commits)?** Default: leave fuzzy; drax's task scope varies enough that fixed-count is overspecified.
3. **For star-lord, doc 3 is the asset-pipeline doc. Should we add the `canonical/19-llm-call-map.md` permanently or only when star-lord's task touches LLM calls?** Default: keep as Phase-1 for now; revisit post-skill-packaging if LLM disciplines become installable skill.
4. **Should the shrink encode a "consult on-demand" reading allowlist (canonical docs star-lord can read without explicit Gate-1 ask) vs. denylist (no-go docs)?** Default: no — trust agents to grep for what they need; the archive is implicitly allowed.
5. **For knight-rider, should the "latest `skill_handoff_*.md`" be more specific (e.g., "the file with the most recent timestamp, NOT the most recent date with intra-day variants")?** Default: yes, clarify in the integration step.

---

**Signed:** gandalf (story-and-design steward)
**For:** jack-ryan per-agent review → Matt approval → knight-rider integration of the onboarding-list shrink into agent definitions. Goal: reduce per-invocation read budget by 60-70% across the team while preserving load-bearing canon access via on-demand reading.

**Next gandalf action after acceptance:** spot-check post-integration; close out cleanup pass.
