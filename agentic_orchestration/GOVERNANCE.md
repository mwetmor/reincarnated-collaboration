# GOVERNANCE.md — Reincarnated agentic team

**Status:** Founding charter, active 2026-05-13
**Format:** Lightweight ADRs — Decision / Context / Alternatives / Consequences

ADRs codify the **non-negotiable structure** of the team. Process details (workflows, review steps) live in `REVIEW_PROCESS.md`. Operational specifics (scope maps, startup manifests, tactics) live in `AGENTS.md`.

---

## ADR-001 — Team topology + cycle-trimming as primary goal

**Decision:** The team consists of 6 entities (Matt + knight-rider + jack-ryan + rocket + gamora + star-lord + drax). The team's primary purpose is **trimming dev cycles**, not maximizing parallelism.

**Context:** Solo development hit four recurring bottlenecks: context-load tax per new session, cross-seam misalignment, Matt as review bottleneck, late-caught design-principle violations. Pure parallelism doesn't fix these and adds coordination overhead.

**Alternatives considered:**
- Max-parallelism (N independent devs) — adds merge conflicts + makes Matt a worse bottleneck
- Pair-programming pattern (2 agents tightly coupled) — too little throughput across the engine's 4 distinct seams
- Hub-and-spoke (1 orchestrator + on-demand specialists) — this is essentially what we chose, formalized

**Consequences:** Specialization with deep context + durable handoffs + tiered review. Agents run on-demand, not constantly. Coordination through knight-rider + durable artifacts, not real-time chat.

---

## ADR-002 — Tiered approval authority

**Decision:** jack-ryan has approval authority for documentation-only changes, test additions, dependency patch/minor bumps, and within-seam refactors (no API change). Matt approves cross-seam schema changes, new ADRs, milestone tags, and anything jack-ryan escalates as BLOCK.

**Context:** Every decision routing through Matt was the single biggest cycle-time drain observed during May 2026 development pushes. Many decisions are routine and don't need architectural judgment.

**Alternatives considered:**
- All approvals through Matt — observed bottleneck, rejected
- All approvals delegated — too much risk; some decisions need architectural eyes
- Multi-tier with knight-rider also approving — complicates authority chain unnecessarily

**Consequences:** Matt's review queue stays focused on architectural calls. jack-ryan's authority is bounded but real. Any developer can request Matt review by escalating; jack-ryan can request Matt review by tagging BLOCK.

---

## ADR-003 — Per-seam tag prefix

**Decision:** Intermediate (developer-tagged) tags carry a seam prefix: `<seam>/v<X.Y>-<feature>-<n>`. Milestone (Matt-approved) tags drop the prefix: `v<X.Y>-<feature>`.

**Context:** With 4 developers tagging in the same engine repo, collisions are inevitable on the existing `v1.3-b10-1-structure` style. Per-seam prefixing decouples developer pace from milestone cadence.

**Alternatives considered:**
- Single shared tag namespace — risks collision + makes it ambiguous who tagged what
- Per-developer prefix (`gamora-v1.3-...`) — overloads naming; agent identity is metadata, not version semantics
- Per-task ticket prefix (B10/B11/B14) — works for engine but doesn't accommodate cross-cutting work

**Consequences:** Tag history shows seam authorship at a glance. Milestone tags remain the canonical reference points in canonical/ docs and decisions-log.

---

## ADR-004 — Cross-seam handoff via MIGRATION.md

**Decision:** When a developer makes a change that affects another seam's consumers, they write a `MIGRATION.md` in their own seam's root **before** tagging. Downstream consumers read it as part of their startup manifest.

**Context:** B14.5 and B10.1 work surfaced multiple cases where one seam's schema changed and downstream consumers had to do archaeology to figure out what shifted. Discipline #12 (semantic-shifting fixes need explicit framing) addresses this within a single seam; MIGRATION.md extends it across seams.

**Alternatives considered:**
- Verbal/chat coordination — doesn't persist across sessions
- Single shared CHANGELOG.md — too noisy; each consumer only cares about their upstream
- Full ADR per change — too heavy for routine schema migrations

**Consequences:** Each developer's seam has a `MIGRATION.md` (or a `migrations/` folder for multiple). knight-rider verifies cross-seam changes have one before allowing tag.

---

## ADR-005 — Git commit gate

**Decision:** All engine work begins with a clean git state. Agents do not begin work if `git status` shows uncommitted changes. If state is dirty, agent flags to Matt before any other action.

**Context:** Existing convention (working branch `stage-a2` in reincarnated-engine). Mid-flight state is risky — easy to commit half-baked work or to lose work to merge conflicts.

**Alternatives considered:**
- Auto-stash + restore — risks data loss on stash drop
- Agent-creates-feature-branch immediately — adds branch sprawl; current branching model is trunk-based on stage-a2

**Consequences:** Each session starts predictably. If Matt has WIP, agent waits. If state is clean, agent proceeds.

---

## ADR-006 — External system writes require explicit per-statement authorization

**Decision:** Read-only by default for databases (telemetry.db, research.db), APIs, cloud SDKs, file systems beyond agent scope, process spawning, messaging, credential mutation. Each write operation requires Matt's per-statement authorization. Authorization does not persist across sessions.

**Context:** External writes are high-blast-radius operations. A bad DB schema migration or accidental file deletion can destroy hours of regen work. Agent autonomy must stop at write boundaries.

**Alternatives considered:**
- Allowlist of known-safe write operations — drifts over time; allowlist gets stale
- Session-scoped authorization — too permissive; one bad call can compound
- Read-only enforced absolutely — blocks legitimate work like committing telemetry results

**Consequences:** Slight friction on every external write. Matt makes the call each time. Trade-off accepted for safety.

---

## ADR-007 — Survey-mode behavioral constraint

**Decision:** When an agent is asked to survey, inventory, or describe state: report what EXISTS. Do NOT interleave "should" statements with descriptive findings. "What is" and "what's wrong" are separate outputs.

**Context:** Repeatedly observed during pre-bootstrap sessions: a request for "what's in this directory" returned a mix of file listing + critique + suggestions. The descriptive content got contaminated with prescription. Matt has to mentally separate the two.

**Alternatives considered:**
- Free-form responses — already observed to be too noisy
- Two-pass (survey first, opinion later only if asked) — adopted

**Consequences:** Survey requests get plain reports. Opinion only when explicitly asked. Reduces noise in the orchestrator's context channel.

---

## ADR-008 — Canonical naming collision resolution

**Decision:** Two directories share the name `canonical/`:
- `reincarnated-engine/src/reincarnated/canonical/` — the **engine's internal canonical library** (pre-built reference data: ability templates, geometry palette, role taxonomies). Owned by rocket. Read by generation pipeline at runtime.
- `reincarnated-collaboration/canonical/` — the **design-discussion docs** (numbered files like 28-engine-arpg-rebalance-design.md). Owned by jack-ryan. Read by humans + agents at session start.

Always reference these by full path when ambiguity is possible.

**Context:** The naming collision is real and not changing. Renaming either is high-touch (touches imports, references throughout docs, git history). Better to document the convention.

**Alternatives considered:**
- Rename engine's internal canonical to `engine-canonical/` or `reference-library/` — too disruptive; touches many imports
- Rename collaboration's design docs to `design/` — but engine repo already has its own `design/` folder for ADRs and working agreement

**Consequences:** All agent definitions reference by full path. AGENTS.md Section 3 documents which agent owns which. New team members onboard via AGENTS.md.

---

## How to extend this charter

New ADRs added as `## ADR-009 — <title>` etc. Numbering monotonic. Don't renumber on insertion; if an ADR is superseded, leave it and add a new one that says "Supersedes ADR-XXX."

Material changes to existing ADRs: add an `### Update <date>` subsection rather than editing the original. Charter is append-only history.

---

## References

- `AGENTS.md` — operational scope map, startup manifests, cycle-trimming tactics
- `REVIEW_PROCESS.md` — change lifecycle, file-type rules, gate protocols
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — the 12 disciplines (especially #1 math-before-code, #2 smoke-test, #11 attribution, #12 semantic-shifting)
- `reincarnated-engine/design/decisions/decisions-log.md` — single source of truth for engine design state
