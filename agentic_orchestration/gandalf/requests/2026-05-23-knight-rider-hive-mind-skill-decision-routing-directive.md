# Request to knight-rider — Hive-Mind Decision-Routing Directive (Matt 2026-05-23)

**From:** gandalf (story-and-design steward; capturing Matt directive)
**To:** knight-rider (orchestrator); future hive-mind-skill author
**Date:** 2026-05-23
**Authority:** Matt 2026-05-23 — direct verbal directive in session
**Status:** LOCKED — to be incorporated verbatim into the eventual `reincarnated-hive-mind-protocol` skill (Stream 3 candidate)
**Companion artifacts:**
- `agentic_orchestration/operating-procedures/knight-rider.md` § 2 Mode A + § 3.9 (immediate load-bearing application)
- `canonical/02-roadmap.md` § 2.2 (Stream 2 per-agent OP skills; this directive scopes into Stream 3 hive-mind protocol authoring)
- `agentic_orchestration/AGENTS.md` (seam ownership map — the basis for seam-routing)
- Engineering disciplines #11 (empirical inspection), #18 (methodology-before-execution), #19 (Agent-tool-not-for-waiting)

---

## 0. TL;DR

**Matt's directive (verbatim framing):**

> *"knight-rider should always call upon the agent who owns each seam for decisions during hive mind run state. Only as a last resort if no amount of collaboration will solve the problem should the decision be made to wait for Matt. During hive mind state, knight-rider should always invoke agents per seam as sub-agents."*

This locks the hive-mind decision-routing pattern: **seam-owning agent decides; Matt is last-resort escalation; sub-agent invocation is the always-channel during hive-mind state.**

---

## 1. The directive — operational specifics

### 1.1 Decision routing during hive-mind state

When a decision surfaces during an active hive-mind cycle:

| Decision touches | Decision-maker (always-first) | Sub-agent invocation pattern |
|---|---|---|
| Generation / element / anchor / foundation / engine-internal canonical | **rocket** | knight-rider invokes rocket as sub-agent |
| Simulation / spirit guide / balance / fight engine | **gamora** | knight-rider invokes gamora as sub-agent |
| Export / output / telemetry / LLM seam | **star-lord** | knight-rider invokes star-lord as sub-agent |
| Catalogue DB / abstraction-analysis / cross-cutting data | **elrond** | knight-rider invokes elrond as sub-agent |
| Visual perception / similarity scoring / benchmark rubrics | **galadriel** | knight-rider invokes galadriel as sub-agent |
| Demo / loadout / player-facing presentation | **drax** | knight-rider invokes drax as sub-agent |
| Research / catalogue crawl / external literature | **legolas** | knight-rider invokes legolas as sub-agent |
| Design intent / thematic / experiential / canonical-story coherence | **gandalf** | knight-rider invokes gandalf as sub-agent |
| Process gate / QA / discipline citation / decisions-log | **jack-ryan** | knight-rider invokes jack-ryan as sub-agent |

### 1.2 Escalation hierarchy — Matt is LAST resort

The order of escalation during a hive-mind decision:

1. **Seam-owning agent decides within their authority** — happens by default, no escalation
2. **Cross-seam collaboration via parallel sub-agent invocation** — knight-rider invokes multiple seam-owning agents in parallel; aggregates returns; synthesizes decision
3. **Critique-pair invocation if process or design concerns surface** — jack-ryan (process) and/or gandalf (design) invoked as sub-agents
4. **Re-attempt collaboration with refined framing** — if first pass didn't converge, knight-rider re-scopes the question and re-invokes
5. **Last resort — wait for Matt** — only when no amount of collaboration has resolved the question

**"Last resort" means literally last resort.** Not "I'd like Matt to weigh in." Not "this seems important enough for Matt." Matt's bandwidth is the project's scarcest resource during hive-mind cycles; he is escalation, not concurrence.

### 1.3 Sub-agent invocation is the always-channel

During hive-mind state, knight-rider's decision-relay shape is:

- **NOT:** "I think we should X because Y" → wait for Matt confirmation
- **NOT:** drafting a dispatch and waiting for Matt review before invoking the seam owner
- **IS:** `Agent({ subagent_type: "rocket", prompt: "<scoped question for seam owner>" })` → rocket returns decision → integrate → continue cycle

Sub-agent invocation pattern per knight-rider OP § 2 Mode C; parallel invocation when multiple seams touched; aggregation per Discipline #19 (don't poll, don't wait — harness notifies).

---

## 2. What this directive resolves

### 2.1 Anti-pattern: Matt-as-default-concurrer during hive-mind

Earlier patterns (pre-2026-05-23) treated Matt as the default concurrer for decisions surfacing during hive-mind state. This produces three pathologies:

- **Bandwidth saturation** — Matt becomes the bottleneck for every Wave decision; hive-mind cycle stalls between Matt sessions
- **Skill-erosion** — seam-owning agents don't exercise decision-authority within their seam; their seam-knowledge becomes underutilized
- **Decision-quality regression** — Matt's bandwidth is fixed; forcing every decision through him produces shallow per-decision reasoning

### 2.2 Anti-pattern: serial sub-agent invocation when parallel is possible

Discipline #19 already names this. The directive reinforces: parallel invocation when seam touches are independent. Don't sequence what can run in parallel.

### 2.3 Anti-pattern: knight-rider deciding solo within a seam he doesn't own

Knight-rider is orchestrator, not specialist. He does not make decisions native to rocket's, gamora's, star-lord's, etc. seams. The directive enforces: ASK the seam owner via sub-agent invocation. Don't synthesize from training-data assumptions about what the seam owner would say.

---

## 3. What this directive does NOT do

- **Does NOT** remove Matt's final decision authority. Matt remains the senior architect. Final approval on architectural commitments, milestone tags, ADRs, cross-seam schema changes still requires Matt per ADR-002.
- **Does NOT** remove jack-ryan's process-gate authority. Gate-1 dispatches still require jack-ryan review before firing; Gate-2 BLOCKs still require remediation. The directive operates WITHIN the gate structure, not around it.
- **Does NOT** remove gandalf's design-side critique-pair role. Design-side critiques during hive-mind cycles are routed via gandalf sub-agent invocation per the table in § 1.1.
- **Does NOT** apply outside hive-mind state. In non-hive-mind sessions (Pattern A subagent invocation, Pattern B dispatch, terminal dialogue), routing follows the standard escalation patterns documented in role definitions.

---

## 4. Integration plan

| Step | Owner | Action | Status |
|---|---|---|---|
| 1 | gandalf | Author this request artifact (formal directive capture) | DONE 2026-05-23 |
| 2 | gandalf | Amend `knight-rider.md` § 2 Mode A + add § 3.9 cross-referencing this directive | DONE 2026-05-23 (single batched commit with this artifact) |
| 3 | knight-rider (future) | When hive-mind skill is authored (Stream 3 candidate), incorporate this directive as a load-bearing section | QUEUED |
| 4 | jack-ryan (future) | Process-side review when hive-mind skill is authored, confirming the directive is incorporated correctly | QUEUED |
| 5 | gandalf (future) | Design-side review at same time | QUEUED |

**Empirical-evidence criterion for step 3 firing:** the hive-mind-protocol skill enters authoring (currently QUEUED post-Stream-2-completion per roadmap § 2.2).

---

## 5. Cross-references

### Canonical
- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/02-roadmap.md` § 2.2 — Stream 2 + Stream 3 sequence
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — keystone delivery strategy

### Operational
- `agentic_orchestration/AGENTS.md` — seam ownership map (basis for seam-routing in § 1.1)
- `agentic_orchestration/operating-procedures/knight-rider.md` § 2 Mode A + § 3.9 — immediate load-bearing application
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #11, #18, #19

### Related directives
- Matt 2026-05-23 no-sleep-recommendations directive (`.claude/agents/gandalf.md` Cross-cutting rules § "No sleep recommendations")
- Matt 2026-05-23 documentation-cleanup-pass authorization

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward; capturing Matt directive)
**Authority:** Matt 2026-05-23 — direct verbal directive
**For:** durable capture of the hive-mind decision-routing pattern so it lands verbatim in the eventual `reincarnated-hive-mind-protocol` skill, AND is immediately load-bearing via the knight-rider operating-procedure amendment landing in the same commit.

**Status:** LOCKED — directive does not require further design review; awaits Stream 3 hive-mind-skill authoring for full integration.
