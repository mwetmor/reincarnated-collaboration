# AGENTS.md — Reincarnated synthetic engineering team

**Status:** Active as of 2026-05-13; expanded 2026-05-16 (6 → 9 entities — added gandalf, legolas, elrond); galadriel topology row added 2026-05-23 (active visual-perception steward, per Matt 2026-05-23 confirmation)
**Senior Architect (human):** Matt
**Purpose:** Synthetic engineering team that trims dev cycles via specialization + durable handoffs + tiered review. Operates across the Reincarnated multi-repo ecosystem.

> **Orientation:** **Engine first. Game second. Phase third.** (ratified Matt 2026-05-27 per `gandalf/notes/2026-05-27-quality-orientation-shift-kr-kicker.md` § 2)
> - **Engine** = architectural integrity (substrate-led discipline; canonical docs; mathematical primitives; discipline-stack composition)
> - **Game** = player-facing quality (playable, balanced, thematically coherent characters; meaningful seasonal journey)
> - **Phase** = operational unit (waves, dispatches, sidecars, gate verdicts)
> - **Conflict resolution:** engine > game > phase
>
> Composes with Discipline #1 (math-before-code) + #11 (empirical inspection) + #25 (substrate semantic-layer rep-audit) + #40 (scaffold-with-pending-decision). Every agent's OP carries the orientation phrase per Move 5 cross-seam delivery. KR dispatches carry quality-criterion section per KR OP § 3.11 (Move 1). Sub-agents run framing-audit per Discipline #42 candidate (Move 2; jack-ryan ratification firing). Sub-agents may file Framing-Refusal per Discipline #44 candidate (Move 3; jack-ryan ratification firing).

---

## 1. Why this team exists

The Reincarnated project spans 3 repos (`reincarnated-engine`, `reincarnated-demo`, `reincarnated-loadout`) plus a meta-repo (`reincarnated-collaboration`) of design docs. Solo work hit four recurring bottlenecks:

1. **Context-load tax** — each new CLI session spent 5–15 min re-reading docs to get current
2. **Cross-seam misalignment** — schema changes in one area broke consumers silently
3. **Review bottleneck** — every decision routed through Matt, blocking ship cadence
4. **Rework from late-caught design-principle violations** — issues found at full-regen stage when fixing at design stage costs ~10× less

This team is structured to attack all four. It is **not** primarily about parallelism — parallelism without coordination ADDS overhead. It's about specialization with deep context, durable handoffs that kill re-archaeology, and review delegation that drains the human queue.

---

## 2. Team topology — 12 entities (Matt + 11 Mac-resident agents)

> **The PC-resident team retired 2026-06-30** (UE cancelled in favor of Godot-on-Mac). Single-host now.
>
> **Model re-pin + legolas role split — 2026-07-24 (Matt-ratified, commit `57172ddb`).** Claude Opus 5 launched at Opus 4.8's exact price point, making the upgrade cost-neutral; the team moved to it except one deliberate cheap lane. `legolas` split into two agents on two models along the known/unknown boundary. **The Model column below is a MIRROR — `.claude/agents/<name>.md` frontmatter is the source of truth.** This column had silently drifted from the live pins before the 2026-07-24 audit (it listed five agents as Sonnet who were actually on Opus 4.8); if they disagree again, the frontmatter wins and this table is the bug.

### The team (12 entities)

| Entity | Role | Model | Writes production code? |
|---|---|---|---|
| **Matt** (Senior Architect) | Final approval; design direction | (human) | No (reviews) |
| `knight-rider` | Orchestrator / Communicator | **Opus 5** | **No** — coordinates only |
| `jack-ryan` | Analyst / QA — technical critique side | **Opus 5** | **No** — reviews + maintains design docs |
| `gandalf` | Story and Design Steward — generative critique side | **Opus 5** | **No** — design docs and pushback only |
| `rocket` | Developer (content generation) | **Opus 5** | Yes |
| `gamora` | Developer (simulation + spirit guide) | **Opus 5** | Yes |
| `star-lord` | Developer (output / telemetry / LLM) | **Opus 5** | Yes |
| `drax` | Developer (presentation: demo + loadout + godot) | **Opus 5** | Yes |
| `legolas` | **UNKNOWN-RESEARCHER** — open questions, primary-source probes, format reverse-engineering, feasibility lanes; escalation receiver for the crawler | **Opus 5** | **No** — read-only research output |
| `legolas-crawler` | **KNOWN-CRAWLER** — systematic extraction at volume against MAPPED sources only (known source + known schema + known procedure) | **Haiku 4.5** | **No** — read-only extraction output |
| `elrond` | Data Steward — external + cross-cutting data layers | **Opus 5** | **No** — schemas, curation, abstraction analysis |
| `galadriel` | Visual Perception and UX-Similarity Steward — screenshot capture, computer-vision pipelines, similarity scoring, benchmark reports against genre-peer references | **Opus 5** | **No** — read-only across production code; writes pipeline scripts + rubrics + benchmark evidence inside her own working tree |

**The known/unknown research split (Matt ruling, 2026-07-24).** The research seam divides on whether the territory is mapped. `legolas` establishes method where none exists; `legolas-crawler` executes method at volume where it does. *He finds out how; the crawler does it at volume.* The cheap lane is safe only under two conditions written into its charter: (1) the **non-improvisation law** — it HALTs and escalates rather than guessing, and a HALT is a success, not a failure; (2) the **TSR-4 tier-2 dependency** — it may only feed lanes carrying in-pipe mechanical asserts on every row. An unguarded lane does not get the cheap crawler. Both exist because the failure mode of cheap extraction is plausible-looking wrong rows — this project's defining hazard, per the grimtools-60-rank vs `.arz`-26-rank contradiction that founded the TRUE-SOURCES program.

**Critique-pair pattern:** jack-ryan (technical/process) and gandalf (thematic/experiential) form the critique pair for major decisions. Pattern E autonomous-pair ratification fires within the trio (knight-rider + the pair).

**Research + data pattern:** legolas (raw research and crawl) and elrond (curation and abstraction analysis) form the knowledge-acquisition pair. Commissions flow from knight-rider or gandalf.

### Authority tiers (codified 2026-05-16)

| Tier | Entities | Authority profile |
|---|---|---|
| **A — Senior critics/stewards** | gandalf, jack-ryan | Non-implementing. Recommend, push back, gate design decisions. Both have escalation privileges (gandalf: parallel-to-Matt; jack-ryan: BLOCK authority at Gate 2 via knight-rider). Hold cross-cutting canonical-write authority. |
| **B — Orchestrator** | knight-rider | Coordinates all seams; never owns files; never critiques design. |
| **C+ — Implementers with steward authority** | elrond, galadriel | elrond owns concrete artifacts (schemas, databases, curation) with steward authority *within data domain*. galadriel owns visual-perception artifacts (capture pipeline, rubrics, similarity scoring, benchmark reports) with steward authority *within visual-perception domain*. Neither critiques outside their domain; escalation through knight-rider only (galadriel does NOT have parallel-escalation privilege — that's gandalf's asymmetry). |
| **C — Implementers/specialists** | rocket, gamora, star-lord, drax, legolas, legolas-crawler | Own concrete seam work; dispatched; produce artifacts; report completion. Escalation through knight-rider only. |

### Viability-gate workflow (catalogue work)

When `legolas-crawler` brings back a catalogue sample (viability-gate sample phase), knight-rider invokes a **three-track parallel review**:

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

### drax — Presentation (demo + loadout + godot 3D prototype)

**Owns:**
- `reincarnated-demo/` entire repo (Pixi.js, rendering, HUD, audio)
- `reincarnated-loadout/` entire repo (React/Vite/Tailwind, Vercel deploy, Page 1/2/3)
- `reincarnated-godot/` entire repo (Godot 4.x / GDScript 3D-scene presentation prototype, Mac-resident; Synty POLYGON assets, Forward+/Metal renderer, baked `.tscn` scenes, MP4 walkthrough harness; the enchanted-forest ravine combat level) — added by Matt-approved scope amendment 2026-06-21

**Does NOT touch:** any path in reincarnated-engine/

**Seam — Godot/Mac 3D prototype:** drax owns `reincarnated-godot/` (the Godot / Mac 3D presentation prototype). *(The former Unreal/PC seam — mantis, `reincarnated-unreal/` — was retired 2026-06-30 when UE work was cancelled in favor of Godot-on-Mac.)*

**Note:** Three different stacks (Pixi.js vs React/Vite vs Godot/GDScript). Drax context-switches between them per task. Demo + loadout consume engine output as read-only data; the Godot prototype is a 3D-scene presentation experiment.

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
- `reincarnated-collaboration/canonical/reap-die-rise-story/` — the STORY spec home (story, lore, dramatic-themes artifacts). (The old `canonical/story/` subdirectory dissolved 2026-07-01 in the canonical reorg; lineage in git.)
- New design docs in the spec folders (`canonical/reap-die-rise-{story,engine}/`) authored going forward; doc 37 was the last numbered doc authored before gandalf existed (the numbered spine now lives in `reap-die-rise-engine/`)
- Design-direction recommendations to knight-rider and Matt
- `agentic_orchestration/gandalf/pushback/` — substantial pushback memoranda when proposed work threatens story / design coherence / player experience
- His own design-lineage + working notes at `agentic_orchestration/gandalf/notes/` (the Phase-2 `gandalf-design-lineage.md` retired to git-lineage in the 2026-07-01 purge; kernels survive in `reap-die-rise-story/style-register.md`)

**Does NOT touch:** production code (any seam); dispatches (knight-rider); decisions-log direct writes (recommends; Matt approves; knight-rider drafts); engineering-disciplines (jack-ryan); existing canonical/ docs (09, 16, 17, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37 — original authorship retained until next major edit); engine's internal canonical library (rocket).

**Authority:** parallel-escalation privilege — can recommend rescoping to knight-rider AND Matt simultaneously. This asymmetry with jack-ryan is intentional: design escalations more often need Matt's direct input than technical critiques.

**Operating modes:**
- Pattern A subagent: knight-rider invokes during decision loops for structured thematic/experiential critique
- Pattern B terminal: Matt opens for sustained design dialogue (the form-bias deep dive of 2026-05-14 is the prototype)

### legolas — UNKNOWN-RESEARCHER · legolas-crawler — KNOWN-CRAWLER

> **Split 2026-07-24 (Matt ruling).** One scout became two agents on two models. The old **Mode A → `legolas`** (Opus 5); the old **Mode B → `legolas-crawler`** (Haiku 4.5). Historical references to "legolas" and "Mode A" resolve to `legolas`; "Mode B" references route to the crawler.

**`legolas` (UNKNOWN-RESEARCHER, Opus 5) owns:**
- `research/knowledge/` — analytical findings, primary-source probes, feasibility investigations
- `research/commissions/` — shared inbox (commissions to either agent land here)
- **Lane establishment** — determining whether a NEW source is crawlable *at all* and by what method. Probing structure, defeating formats, judging agent-fetchability. Files written here are marked `lane-establishment`.
- **Escalation intake** — receives every crawler HALT; rules the lane re-mappable / degraded / dead

**`legolas-crawler` (KNOWN-CRAWLER, Haiku 4.5) owns:**
- `research/catalogue/<source>/` — raw extraction, findings-summaries, sidecars
- `research/commissions/*-crawler-halt-*.md` — its HALT notes
- Carries the crawl contract: viability-gate protocol, score-don't-filter principle, standard metadata fields, crawl discipline, parallelism conventions

**Neither touches:** production code; dispatches; canonical/; decisions-log; engineering-disciplines; engine telemetry DB; data curation (Elrond's territory).

**The boundary:** *legolas finds out how; the crawler does it at volume.* Work is the crawler's only when source, schema, AND procedure are all known. If method must be invented, format defeated, viability determined, or ambiguity judged — it is legolas's.

**Two laws binding the cheap lane:** (1) **non-improvisation** — on any unmodeled condition the crawler HALTs and escalates rather than guessing; a HALT is a success. (2) **TSR-4 tier-2 dependency** — the crawler may only feed lanes with in-pipe mechanical asserts live on every row; an unguarded lane does not get the cheap crawler.

Multiple crawler instances may run in parallel for catalogue-scale work; coordinate via filename conventions; append-only.

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
- With `legolas-crawler`: commissions catalogue crawls; provides curation feedback when raw extraction has structural issues. With `legolas`: commissions lane establishment when a source's method is unknown
- With Gandalf: receives abstraction-analysis commissions when design questions need empirical grounding

### galadriel — Visual Perception and Benchmark Steward

**Owns:**
- `agentic_orchestration/galadriel/` — full working tree (mirrors `legolas/` and `elrond/` convention)
  - `reference-images/` — curated genre-peer reference frames (Matt-captured + public-source per provenance rules)
  - `captures/` — demo + loadout screenshots, organized by date / viewport / state
  - `rubrics/` — multi-axis scoring rubrics for visual surfaces
  - `reports/` — benchmark reports and comparison studies
  - `pipeline/` — screenshot-capture harness code (Playwright/Puppeteer/sharp/pHash)
- Reference-image `MANIFEST.md` — provenance + state-description registry
- Benchmark reports — `agentic_orchestration/galadriel/reports/visual-benchmark-<topic>-<date>.md` co-authored with gandalf; register-qualifying conclusions fold into `canonical/reap-die-rise-story/style-register.md`

**Does NOT touch:** production code (any seam); dispatches (knight-rider); decisions-log (jack-ryan); canonical-story authorship alone (benchmark reports co-authored with gandalf); reference-image sourcing from outside-Matt sources without explicit pre-authorization.

**Sub-agent invocation: HARD NO** (amended 2026-05-19 per Matt directive). Surface cross-domain requests to gandalf or knight-rider via hive-log REQUEST entry.

**Cross-seam coordination:**
- With gandalf: tight critique-pair. Galadriel produces evidence (screenshots, scores, comparisons); gandalf interprets in design-meaning terms. Co-authored benchmark reports.
- With drax: evidence supply. Galadriel surfaces visible dissonances; drax decides whether/how to address in implementation. May consult drax on capture-pipeline hooks (debug-state URL params).
- With knight-rider: receives dispatch-level work; surfaces capture-pipeline blockers as FRICTION.

---

## 3.5 Mathematical Layer (cross-cutting; no dedicated agent)

Math work is **distributed by data-locality**, not owned by a single agent. Each seam handles the math native to its data + tooling:

| Math work-type | Owning seam | Examples |
|---|---|---|
| **Design-spec-as-math** — axis meanings, formula intent, architectural defaults, design-intent expressed as algebraic structure | **gandalf** | BDI ω/τ tables, BC axes lock, T4 architecture defaults, gear-substrate rule table, build-defining resonance formula |
| **Statistical methodology on catalogue data** — dimensionality reduction, factor analysis, clustering, embedding-space operations | **elrond** | P2 axis discovery, P3 multimodal clustering, abstraction-analysis tables |
| **Simulation-side math** — balance loops, convergence algorithms, fight-resolution math, recompose-first arithmetic | **gamora** | B14.5 V1 primary loop, W0.10 boss-AI math, multi-dim convergence algorithm |
| **Telemetry statistics** — distributions, aggregates, derived metrics, anomaly detection, judge calibration | **star-lord** | LC-002/009/011 attribution analysis, sidecar findings, distribution audits |
| **Visual perception math** — image-similarity scoring, embedding-based comparison, perceptual-distance metrics | **galadriel** | Visual benchmarking vs genre-peer references, perception-test scoring |
| **External-literature methodology research** — when methodology selection requires graduate-level stats grounding beyond the seam's native depth | **legolas** (UNKNOWN-RESEARCHER) | Methodology consultations for P2/P3/P5 math hotspots |

**Math hotspots** (methodology-choice moments where external-literature rigor is required before execution) are explicitly named in the P-phase protocols. Current named hotspots are P2 axis discovery, P3 multimodal clustering, and P5 cohesion-judge validation. See `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2 for the living list and the design-call requirements per hotspot.

**Routing rule:** when math work could plausibly land in multiple seams, knight-rider dispatches per data-locality. When in doubt, gandalf advises on routing.

**Discipline guard:** Discipline #18 (methodology-before-execution) governs math-hotspot execution — methodology selection is made via `legolas` (UNKNOWN-RESEARCHER) research + design call BEFORE execution, not derived FROM execution. See `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 18.

**Rationale for no dedicated mathematician agent:** math is cross-cutting (not seam-shaped); volume is bounded (consultation-volume, not full-time-agent volume); the failure surface is methodology selection (already addressable via gandalf + Matt + `legolas`); adding agents adds the documentation/scope-policing/cross-reference load already-diagnosed as a team slowdown root cause (per 2026-05-23 morning diagnosis). Re-evaluation triggers documented in the math-seam note § 4.2.

---

## 4. The seven cycle-trimming tactics

These are **mandatory practices** for every agent. The team's whole reason to exist is wired through them.

### Tactic 1 — Per-agent startup manifest (above)

Every developer agent has a 3–4 file startup-read list. **Read these first, every session.** Skip the rest of the codebase tour. Saved time: ~5–10 min/session.

**Universal first-read pair (added 2026-05-23 per gandalf onboarding-shrink + jack-ryan PASS-WITH-AMENDMENTS):** every agent reads these two BEFORE any role-specific reads:

1. `canonical/00-ground-state.md` — ground-state oracle (current epoch, current canon, dead branches, single-source-of-truth contracts in ~1500 words). Gandalf maintains; updates on epoch shifts. See § 4 First-reads-by-role for per-agent shrunken Phase-1 read lists.
2. `canonical/38-downstream-delivery-strategy-2026-05-23.md` — keystone delivery strategy (D1–D10 lock).

After these two, role-specific reads per `canonical/00-ground-state.md` § 4. **The archive is consulted on-demand, NOT pre-loaded** — `grep` and `read` specific docs as the task requires; do not re-walk the historical archive on every invocation. Aggregate per-invocation read-budget target: 10–15 minutes (down from 60–120 min pre-shrink).

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
