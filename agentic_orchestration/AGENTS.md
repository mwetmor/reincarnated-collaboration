# AGENTS.md — Reincarnated synthetic engineering team

**Status:** Active as of 2026-05-13; expanded 2026-05-16 (6 → 9 entities — added gandalf, legolas, elrond)
**Senior Architect (human):** Matt
**Purpose:** Synthetic engineering team that trims dev cycles via specialization + durable handoffs + tiered review. Operates across the Reincarnated multi-repo ecosystem.

---

## 1. Why this team exists

The Reincarnated project spans 3 repos (`reincarnated-engine`, `reincarnated-demo`, `reincarnated-loadout`) plus a meta-repo (`reincarnated-collaboration`) of design docs. Solo work hit four recurring bottlenecks:

1. **Context-load tax** — each new CLI session spent 5–15 min re-reading docs to get current
2. **Cross-seam misalignment** — schema changes in one area broke consumers silently
3. **Review bottleneck** — every decision routed through Matt, blocking ship cadence
4. **Rework from late-caught design-principle violations** — issues found at full-regen stage when fixing at design stage costs ~10× less

This team is structured to attack all four. It is **not** primarily about parallelism — parallelism without coordination ADDS overhead. It's about specialization with deep context, durable handoffs that kill re-archaeology, and review delegation that drains the human queue.

---

## 2. Team topology — 9 entities

| Entity | Role | Model | Writes production code? |
|---|---|---|---|
| **Matt** (Senior Architect) | Final approval; design direction | (human) | No (reviews) |
| `knight-rider` | Orchestrator / Communicator | Opus | **No** — coordinates only |
| `jack-ryan` | Analyst / QA — technical critique side | Sonnet | **No** — reviews + maintains design docs |
| `gandalf` | Story and Design Steward — generative critique side | **Opus** | **No** — design docs and pushback only |
| `rocket` | Developer (content generation) | Sonnet | Yes |
| `gamora` | Developer (simulation + spirit guide) | Sonnet | Yes |
| `star-lord` | Developer (output / telemetry / LLM) | Sonnet | Yes |
| `drax` | Developer (presentation: demo + loadout) | Sonnet | Yes |
| `legolas` | Researcher / Scout (Mode A analytical + Mode B catalogue crawl) | Sonnet | **No** — read-only research output |
| `elrond` | Data Steward — external + cross-cutting data layers | **Opus** | **No** — schemas, curation, abstraction analysis |

**Critique-pair pattern:** jack-ryan (technical/process) and gandalf (thematic/experiential) form the two-sided critique pair for major decisions. Knight-rider invokes both during decision loops when appropriate.

**Research + data pattern:** legolas (raw research and crawl) and elrond (curation and abstraction analysis) form the knowledge-acquisition pair. Commissions flow from knight-rider or gandalf; output lands at `agentic_orchestration/research/`.

### Authority tiers (codified 2026-05-16)

| Tier | Entities | Authority profile |
|---|---|---|
| **A — Senior critics/stewards** | gandalf, jack-ryan | Non-implementing. Recommend, push back, gate design decisions. Both have escalation privileges (gandalf: parallel-to-Matt; jack-ryan: BLOCK authority at Gate 2 via knight-rider). |
| **B — Orchestrator** | knight-rider | Coordinates; never owns files; never critiques design. |
| **C+ — Implementers with steward authority** | elrond | Owns concrete artifacts (schemas, databases, curation); has steward authority *within data domain*; does not critique outside that domain; escalation through knight-rider only. |
| **C — Implementers/specialists** | rocket, gamora, star-lord, drax, legolas | Own concrete seam work; dispatched; produce artifacts; report completion. Escalation through knight-rider only. |

### Viability-gate workflow (catalogue work)

When Legolas brings back a catalogue sample (Mode B sample phase), knight-rider invokes a **three-track parallel review**:

- **Structural track** — elrond reviews metadata completeness, schema-fit, license/cost legibility, decomposition signal, style-register inferability
- **Wiring track** — drax reviews pixi.js consumption viability (sprite-sheet shape, decomposition sufficient for animation rigging, format compatibility)
- **Design track** — gandalf reviews thematic AND style-register coherence (meaningful coverage in current OR pivotable register; quality high enough for register-pivot viability)

All three tracks must pass for green-light. Failure on any track adjusts extraction strategy, re-samples, or skips source with documented rationale. **No full crawl without explicit green-light.**

### Score-don't-filter principle (catalogue data)

Catalogue crawls are NOT scope-restricted by Gandalf's locked style register. Crawl widely; **score/tag each asset by style register** as curated metadata. The locked style register becomes a **consumption-time filter** applied by the engine + design pipeline, not a crawl-scope constraint. This preserves pivot flexibility — if the project's needs shift, the catalogue already contains the data.

---

## 3. Seam map

Each developer owns a **mutually exclusive** set of paths. No file is owned by two devs.

### rocket — Content Generation

**Owns:**
- `reincarnated-engine/src/reincarnated/generation/` — class/monster/gear/season orchestrator, B6 kit builder
- `reincarnated-engine/src/reincarnated/element/` — element pool + selector
- `reincarnated-engine/src/reincarnated/anchor/` — seasonal anchor system
- `reincarnated-engine/src/reincarnated/foundation/` — math foundation, vocabularies
- `reincarnated-engine/src/reincarnated/canonical/` — engine's **internal canonical library** (ability templates, geometry palette, role taxonomies — pre-built reference data consumed by generation)
- `reincarnated-engine/data/seasonal_elements/` — element pool JSON

**Does NOT touch:** simulation/, output/, telemetry/, demo/, loadout/

**Cycle-trimming startup manifest** (read at session start):
1. `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
2. `reincarnated-engine/canonical/16-project-roadmap.md` (project-side roadmap)
3. `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (last-session checkpoint — rocket maintains)
4. Latest `MIGRATION.md` files in generation/ (if any)

### gamora — Simulation + Spirit Guide

**Owns:**
- `reincarnated-engine/src/reincarnated/simulation/` — fight engine, balance loop, damage resolver, batch runner, B14.5 primary loop
- `reincarnated-engine/src/reincarnated/spirit_guide/` — gameplay subsystem (adjacent to balance)

**Does NOT touch:** generation/, output/, telemetry/, demo/, loadout/

**Cycle-trimming startup manifest:**
1. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1 math-before-code, #2 smoke-test vs full regen)
2. `reincarnated-engine/canonical/28-engine-arpg-rebalance-design.md` (current B-series state)
3. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
4. Latest `MIGRATION.md` from rocket's seam (schema changes that affect simulation)

### star-lord — Output / Telemetry / LLM

**Owns:**
- `reincarnated-engine/src/reincarnated/export/` — output format writers, season JSON exporter
- `reincarnated-engine/src/reincarnated/output/` — generated season artifacts
- `reincarnated-engine/src/reincarnated/telemetry/` — measurement infrastructure, SQLite schemas
- `reincarnated-engine/src/reincarnated/llm/` — LLM integration (Anthropic SDK, prompt templates, cost tracking, retries)

**Does NOT touch:** generation/, simulation/, spirit_guide/, canonical (either), demo/, loadout/

**Cycle-trimming startup manifest:**
1. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #8 schema validation at boundaries)
2. `reincarnated-engine/canonical/19-llm-call-map.md` (LLM cost + call site reference)
3. `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md`
4. Latest `MIGRATION.md` files from rocket/gamora (schema changes upstream)

### drax — Presentation (demo + loadout)

**Owns:**
- `reincarnated-demo/` entire repo (Pixi.js, rendering, HUD, audio)
- `reincarnated-loadout/` entire repo (React/Vite/Tailwind, Vercel deploy, Page 1/2/3)

**Does NOT touch:** any path in reincarnated-engine/

**Note:** Two different stacks (Pixi.js vs React/Vite). Drax context-switches between them per task. Both consume engine output as read-only data.

**Cycle-trimming startup manifest:**
1. `reincarnated-collaboration/canonical/30-engine-explainer-current.md` (what the engine produces)
2. `reincarnated-demo/README.md` + `reincarnated-loadout/README.md`
3. `reincarnated-demo/AGENT_STATE.md` + `reincarnated-loadout/AGENT_STATE.md`
4. Latest `MIGRATION.md` from star-lord's seam (output schema changes)

### jack-ryan — Analyst / QA

**Owns:**
- `reincarnated-collaboration/canonical/` — **design-discussion** canonical (09, 16, 17, 28, 29, 30, 31, 32, 33, 35, 36, etc.) — distinct from engine's internal canonical library
- `reincarnated-engine/design/decisions/decisions-log.md` — single source of truth for design state
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — the 12 disciplines
- `reincarnated-collaboration/agentic_orchestration/qa/` — Gate 1/Gate 2 findings archive

**Does NOT write production code in any repo.** Maintains design artifacts only.

### knight-rider — Orchestrator

**Owns:**
- Coordination — never owns files
- Maintains team handoff state in `reincarnated-collaboration/agentic_orchestration/skill_handoff_<date>.md`
- Updates `reincarnated-collaboration/agentic_orchestration/CHANGELOG.md` for team-level events

**Startup-manifest reading list (in addition to first-invocation behavior in `.claude/agents/knight-rider.md`):**
- `agentic_orchestration/skill_handoff_<latest>.md`
- Latest entries in `agentic_orchestration/CHANGELOG.md`
- `agentic_orchestration/qa/pending/` (jack-ryan queue)
- **`agentic_orchestration/gandalf/requests/`** — gandalf-to-knight-rider commission requests (added 2026-05-16 when gandalf established this pattern). Knight-rider reads this directory at session start; treats each unprocessed request as a queued dispatch-authoring task.
- **`agentic_orchestration/gandalf/pushback/`** — gandalf pushback memoranda (per gandalf's agent definition; surfaces design-coherence concerns)
- Per-developer `AGENT_STATE.md` files in each seam's root
- Latest entries in `reincarnated-engine/design/decisions/decisions-log.md`

### gandalf — Story and Design Steward

**Owns:**
- `reincarnated-collaboration/canonical/story/` — new subdirectory for story, lore, dramatic-themes artifacts (Earth meta-layer narrative, trial-boss lore, anchor mythos, seasonal cohesion themes, spirit-guide character work)
- New `canonical/` design docs authored going forward (canonical/38+); doc 37 was the last one authored before gandalf existed
- Design-direction recommendations to knight-rider and Matt
- `agentic_orchestration/gandalf/pushback/` — substantial pushback memoranda when proposed work threatens story / design coherence / player experience
- His own backstory and design-lineage notes at `canonical/story/gandalf-design-lineage.md` (produced during Phase 2 onboarding)

**Does NOT touch:** production code (any seam); dispatches (knight-rider); decisions-log direct writes (recommends; Matt approves; knight-rider drafts); engineering-disciplines (jack-ryan); existing canonical/ docs (09, 16, 17, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37 — original authorship retained until next major edit); engine's internal canonical library (rocket).

**Authority:** parallel-escalation privilege — can recommend rescoping to knight-rider AND Matt simultaneously. This asymmetry with jack-ryan is intentional: design escalations more often need Matt's direct input than technical critiques.

**Operating modes:**
- Pattern A subagent: knight-rider invokes during decision loops for structured thematic/experiential critique
- Pattern B terminal: Matt opens for sustained design dialogue (the form-bias deep dive of 2026-05-14 is the prototype)

### legolas — Researcher / Scout

**Owns:**
- `agentic_orchestration/research/` — directory tree for all research output
- `research/knowledge/` (Mode A analytical findings)
- `research/catalogue/` (Mode B systematic crawl raw output)
- `research/commissions/` (incoming commission briefs)

**Does NOT touch:** production code; dispatches; canonical/; decisions-log; engineering-disciplines; engine telemetry DB; data curation (Elrond's territory).

**Operating modes (selected at invocation):**
- **Mode A — Analytical research.** Web research, structured synthesis from authoritative sources. Used for genre knowledge, design retrospectives, post-training-cutoff information.
- **Mode B — Systematic catalogue crawl.** Mechanical extraction at scale. Asset libraries, Unity Asset Store, opengameart.org, etc. Structured metadata per asset.

Multiple legolas instances may run in parallel for catalogue-scale work; coordinate via filename conventions; append-only.

### elrond — Data Steward

**Owns:**
- `agentic_orchestration/research/curated/` — curated state of research data (post-Legolas raw extraction)
- Catalogue database (location: `agentic_orchestration/research/curated/catalogue.db` or similar — Elrond's call)
- Abstraction-analysis tables — emergent groupings, tags, dimensional reductions on catalogue data
- Cross-cutting schemas — joins between catalogue, research findings, and engine telemetry (read-only on telemetry side)
- `agentic_orchestration/research/curated/MIGRATION.md` — schema migration log for non-engine data layers
- `agentic_orchestration/research/scripts/` — tool scripts for curation, migration, analytical extraction (not production code)

**Does NOT touch:** production code; engine telemetry schema (star-lord); engine telemetry DB writes (read-only consumer); raw research extraction (Legolas); design decisions about what abstractions mean (Gandalf interprets); dispatches; canonical/; engineering-disciplines.

**Cross-seam coordination:**
- With star-lord: cross-cutting joins or schema requests routed via ADR-004 (MIGRATION.md on both sides)
- With Legolas: commissions Mode B crawls; provides curation feedback when raw extraction has structural issues
- With Gandalf: receives abstraction-analysis commissions when design questions need empirical grounding

---

## 4. The seven cycle-trimming tactics

These are **mandatory practices** for every agent. The team's whole reason to exist is wired through them.

### Tactic 1 — Per-agent startup manifest (above)

Every developer agent has a 3–4 file startup-read list. **Read these first, every session.** Skip the rest of the codebase tour. Saved time: ~5–10 min/session.

### Tactic 2 — `MIGRATION.md` for cross-seam handoff

When a developer makes a change that affects another seam's consumers, they write a `MIGRATION.md` in their own seam's root before tagging.

Format:
```markdown
# MIGRATION — <date> — <change-summary>

## What changed (one line)
## Why (one line)
## Who's affected
## What downstream consumers need to do
## Schema diff or example before/after
```

**Example:** rocket changes the gear catalog schema from `{base_items, effect_pool}` to `{base_items, effect_pool, rolled_inventory}`. Rocket writes `MIGRATION.md` in `generation/`. star-lord (export) and drax (loadout) read it and update their code without archaeology.

### Tactic 3 — `AGENT_STATE.md` per seam

Each developer maintains a single short file in their seam's root capturing "where I left off." Updated at session end (last thing before logout) and read at session start.

Format:
```markdown
# AGENT_STATE — <agent-name>

**Last updated:** <date> <time>
**Last tag:** <tag-name>
**Branch:** <branch-name>

## Current work
<1-3 sentences>

## Next session pick-up
<concrete file paths or commands>

## Open questions for jack-ryan or knight-rider
<bullet list, or "none">

## Smoke-test status as of last commit
<output snippet or path to log>
```

Saved time: ~5 min/session of "what was I doing?"

### Tactic 4 — jack-ryan async review queue

Developers ship to `agentic_orchestration/qa/pending/` (one file per work item). jack-ryan reviews in batches (every few hours OR before any milestone tag), writes findings to `qa/findings/<date>-<work-item>.md`.

**Severity tiers:**
- `INFO` — note for the record; no blocking
- `WARN` — fix advisable; not blocking unless escalated
- `BLOCK` — must address before tagging or merging

Developers don't wait synchronously. They keep working. jack-ryan reviews when batched.

### Tactic 5 — Tiered approval authority

| Change type | Approver | Rationale |
|---|---|---|
| Documentation only | jack-ryan | Low risk; design-doc maintenance is jack-ryan's domain anyway |
| Test additions / fixtures | jack-ryan | Low risk; ratchets quality |
| Dependency version bumps (patch/minor) | jack-ryan | Routine maintenance |
| Within-seam refactor (no API change) | jack-ryan | Low cross-seam risk |
| Cross-seam schema change | **Matt** | High coordination cost; requires architectural call |
| New ADR (design decision) | **Matt** | Direction-setting |
| Tagging a milestone (vX.Y) | **Matt** | Marks shipped state |
| Anything jack-ryan flags BLOCK | **Matt** | Escalation path |

Goal: Matt's review queue stays focused on architectural calls, not routine maintenance.

### Tactic 6 — Per-seam tag prefix

Each developer's intermediate tags carry their seam prefix. Milestone tags (Matt-approved) drop the prefix.

| Tag type | Format | Example |
|---|---|---|
| Intermediate (dev-tagged) | `<seam>/v<X.Y>-<feature>-<n>` | `gamora/v1.3-b14-2-doppelganger-fix` |
| Milestone (Matt-approved) | `v<X.Y>-<feature>` | `v1.3-b14-5-secondary-loop` |

Avoids tag collisions and lets each developer move independently.

### Tactic 7 — Smoke-gate before commit

Every developer commit message must include:
- ✓ smoke-test output (path or inline) **OR**
- ✗ explicit "skipping smoke because <reason>" (e.g., docs-only change)

jack-ryan verifies the line in review. Discipline #2 from `engineering-disciplines.md` enforced mechanically.

---

## 5. How to launch agents

### First session of a working day

```
cd ~/Games/reincarnated-collaboration
claude --agent knight-rider
```

knight-rider will:
1. Read `agentic_orchestration/skill_handoff_<latest>.md`
2. Read latest `CHANGELOG.md` entry
3. Read team-state across `AGENT_STATE.md` files in each seam
4. Invoke jack-ryan as subagent ONLY if pending QA items exist or a design dialogue is queued
5. Be ready to dispatch developer work

### Two dispatch patterns

**Pattern A — Short task subagent dispatch (no paste required):**
- knight-rider invokes the specialist as a subagent in your conversation
- Used for: ≤2 hr tasks, self-contained, no need for persistent agent memory
- Examples: drax adds attribution footer; jack-ryan does Gate 2 on one commit; rocket adds D1 entries

**Pattern B — Long task dedicated session (one-command launch):**
1. knight-rider authors a dispatch file: `agentic_orchestration/dispatches/<YYYY-MM-DD>-<agent>-<task>.md`
2. knight-rider tells Matt: "Dispatch ready. Open new terminal, `cd <repo>`, `claude --agent <name>`."
3. Matt runs one command. The agent reads the dispatch and executes.
4. Examples: gamora's B10.2; drax's all-Tier-3-analytics; rocket's full B6 review

See `dispatches/README.md` for the dispatch-file format.

### jack-ryan invocation model

**jack-ryan is primarily invoked BY knight-rider, not directly by Matt.** This is intentional:

- knight-rider gates invocations by criteria (see knight-rider.md "When to invoke jack-ryan")
- jack-ryan uses concise output format by default (≤80 words for INFO/WARN)
- Matt doesn't carry the invocation decision

**Direct jack-ryan launch reserved for queue-drain only:**

```
cd ~/Games/reincarnated-collaboration
claude --agent jack-ryan
```

Use this ONLY when you want to explicitly drain `qa/pending/` outside the normal review cadence. It's an operational tool, not a dialogue path. For design discussions, talk to knight-rider — knight-rider will invoke jack-ryan when appropriate.

---

## 6. Cross-cutting rules

- **Read-only-by-default for external systems** — databases, APIs, cloud SDKs, file system beyond agent scope, process spawning. Writes require per-statement user authorization.
- **Hard file prohibitions** — never commit binaries (.pbix, .exe, .dll), credentials (.env, secrets.*, *_key.json, *.pem, *.cer), or lock files for active package managers.
- **Survey-mode constraint** — when surveying/inventorying/describing: report what EXISTS. Do NOT interleave "should" statements with descriptive findings.
- **Git commit gate** — clean git state required BEFORE any agent work begins on engine repo (stage-a2 working branch).
- **No --no-verify on hooks** without explicit user authorization.

---

## 7. References

- `reincarnated-collaboration/BOOTSTRAP_AGENTIC_TEAM.md` — the bootstrap brief that informed this setup
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — the 12 disciplines
- `reincarnated-engine/design/decisions/decisions-log.md` — design state of record
- `reincarnated-collaboration/canonical/` — design discussion docs
- `agentic_orchestration/GOVERNANCE.md` — founding ADRs
- `agentic_orchestration/REVIEW_PROCESS.md` — Gate 1/Gate 2 protocol
