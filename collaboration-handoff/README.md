# Collaboration Handoff — Historical / Working Archive

> **🔀 Reorganization 2026-05-12:** Active reference documents (29 strategic anchor, 16 roadmap, 28 engine queue, 32+33 progression, 30+31 engine state, 09 geometry, 17 gear, 19 LLM map, 35 Stage A2 CLI prompt) have moved to **`../canonical/`**. **Start there for current work.** This folder retains historical/working-discussion artifacts that document HOW we arrived at current state but aren't load-bearing for ongoing engineering.

## What's in `../canonical/` (active reference)

If you're picking up work on Reincarnated, read those first. `../canonical/README.md` has the full read order. Quick links:

| File | Purpose |
|---|---|
| `../canonical/29-design-overview.md` | Strategic anchor — scope, two-engine architecture, four-track work model |
| `../canonical/16-project-roadmap.md` | Track A staging (A1-A7), playtest cycles, operational principles |
| `../canonical/28-engine-arpg-rebalance-design.md` | Full engine queue (B1-B15) — the engineering spec |
| `../canonical/32-progression-design.md` | Progression design (12 sections, 54+ LOCKED entries) |
| `../canonical/33-progression-skeleton.md` | Progression skeleton (immutable + decided only) |
| `../canonical/30-engine-explainer-current.md` | Current engine state (demo1 v1.2 ship) |
| `../canonical/31-engine-explainer-future.md` | Future engine state (post-Track A) |
| `../canonical/09-geometry-palette-discussion.md` | Geometry palette (2026-05-08 + B11 + B13) |
| `../canonical/17-gear-and-spirit-guide-design.md` | Gear + Spirit Guide architecture |
| `../canonical/19-llm-call-map.md` | LLM API call inventory + cost tracking |
| `../canonical/35-stage-a2-cli-prompt.md` | Copy-paste-ready CLI prompt for Stage A2 work |

## Purpose of THIS folder (historical/working)

This folder retains the **discussion artifacts** that produced canonical decisions:
- Phase 0-era architectural conversation (May 7-8, 2026)
- Dimensional generation Option C decision discussion (2026-05-08)
- CLI prompts that have already been executed (Phase 1/2/3 of dimensional refactor; Priority 02 gear; demo1 implementation)
- Trial-room + class-scoping design intent (referenced by canonical docs)
- Three.js demo planning artifacts (largely superseded by demo1 ship)
- Decision-log entries drafted here before promotion to engine-repo decisions-log
- Morning orientation snapshots from past sessions

These docs are reference material for understanding HOW we got here, but they're not load-bearing for ongoing engineering. Most CLI prompts have already been executed; the outputs landed in canonical docs, the engine repo, or the demo repo.

## What's in THIS folder

| File | Purpose | Status |
|---|---|---|
| `00-working-agreement.md` | Meta-rules for sessions in this folder (discussion only; no code in working repos) | Active reference |
| `01-context.md` | What was built and discovered May 7–8, 2026 | Historical |
| `02-doc-maintenance-required.md` | Documentation drift that motivated the 2026-05-08 maintenance pass | Historical (resolved) |
| `03-architectural-proposal.md` | The dimensional generation idea, expanded | Historical (decision landed) |
| `04-decision-options.md` | Three paths forward (A/B/C, with trade-offs) | Historical (Option C chosen) |
| `05-action-plan.md` | Original concrete steps for 2026-05-08; partially superseded | Historical |
| `06-trial-room-and-class-scoping.md` | Spirit-swap framing, form library, trial room mechanic, class scoping | Reference (some content referenced by canonical) |
| `07-cli-decomposition-prompt.md` | CLI session prompt for dimensional decomposition exercise | Executed |
| `08-decomposition-report.md` | Decomposition findings — empirical evidence informing the architectural decision | Historical |
| `10-decision-log-entry-dimensional-generation.md` | The architectural decision (Option C adopted); promoted to `engine-repo/design/decisions/decisions-log.md` (2026-05-08) | Historical |
| `11-cli-doc-maintenance-prompt.md` | CLI session prompt for doc maintenance pass | Executed 2026-05-08 |
| `12-cli-phase-1-energy-type-prompt.md` | CLI session prompt for Phase 1 of dimensional refactor | Executed |
| `13-cli-phase-1-polish-prompt.md` | CLI session prompt for Phase 1 polish | Executed 2026-05-08 |
| `14-cli-phase-2-role-orientation-prompt.md` | CLI session prompt for Phase 2 | Executed |
| `15-cli-phase-3-geometry-prompt.md` | CLI session prompt for Phase 3 | Executed |
| `18-cli-priority-02-gear-prompt.md` | CLI session prompt for Priority 02 gear | Executed (gear closed 2026-05-10) |
| `20-cli-priority-02-cp3-prompt.md` | CLI session prompt for Priority 02 CP3 | Executed |
| `21-morning-orientation-2026-05-10.md` | Morning orientation snapshot | Historical |
| `22-three-js-demo-and-data-export.md` | Three.js demo planning | Largely superseded by demo1 v1.2 ship |
| `23-cli-canonical-loadouts-and-data-export.md` | CLI session prompt for canonical loadouts + data export | Executed |
| `24-cli-demo1-implementation.md` | CLI session prompt for demo1 implementation | Executed (demo1 v1.2 shipped) |
| `25-demo-visual-content-rd.md` | R&D notes on demo visual content options | Reference |
| `26-demo-audio-content-rd.md` | R&D notes on demo audio content options | Reference |
| `27-demo-multiplayer-coop.md` | R&D notes on multiplayer / co-op design | Reference (deferred to Earth meta-layer post-Phase 0) |
| `34-earth-meta-layer.md` | **TO BE DRAFTED** when Matt shares Earth meta-layer notes; initial intent captured in `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_earth_meta_layer.md` | Pending |

## Status when this folder was created (May 8, 2026 — historical)

- Yesterday's engine work merged to main: telemetry foundation, anchor system, element system
- Physical warrior fix: in progress on `work/priority-01-physical-warrior` branch
- Monster mana economy bug: identified, root cause known, fix not yet implemented
- Dimensional generation idea: discussed in conversation, not yet documented as design proposal
- Documentation drift: substantial, queued for catch-up before any new architectural work

(Current state is captured in `../canonical/30-engine-explainer-current.md`. The above is the starting point of this folder's discussion arc.)

## How to use this folder

Most readers should NOT start here. Start in `../canonical/`. Come here when:

- You want to understand WHY a canonical decision was made (the discussion that produced it)
- You're researching past CLI prompt patterns to draft a new one
- You're looking for design intent that didn't make it into the canonical docs verbatim (e.g., trial-room + class-scoping in 06)
- You want to reference an already-executed CLI prompt as a template for new work
