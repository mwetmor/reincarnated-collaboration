# Canonical reference docs

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Created 2026-05-12** as a split from `../collaboration-handoff/` to separate **active reference documents** (this folder) from **historical / working-discussion archives** (`../collaboration-handoff/`).

These docs are the **load-bearing references** for ongoing engine work + design decisions. Read these first; everything else is context.

## Read order — first time

1. **`29-design-overview.md`** — strategic anchor. Scope, two-engine architecture, four-track work model. **Start here.**
2. **`16-project-roadmap.md`** — Track A stage sequencing (A1-A7) + interleaved playtest cycles + operational principles (refactor-not-rewrite, legacy preservation, single-season-per-playtest rule).
3. **`28-engine-arpg-rebalance-design.md`** — full engine queue. Every B-item (B1-B15) with scope, cost, co-dependencies, demo follow-on notes. **This is the engineering spec.**
4. **`33-progression-skeleton.md`** — locked-only summary of all 12 progression-design sections. Quick-reference for anything that must be true post-Stage-A7.

## Read order — for deeper context

5. **`32-progression-design.md`** — full progression-design discussion (12 sections, 54+ LOCKED entries). Reference when 33's summary needs unpacking.
6. **`30-engine-explainer-current.md`** — engine as it ships in demo1 v1.2. Current-state baseline that Stage A2 refactors.
7. **`31-engine-explainer-future.md`** — engine target state after Track A closes. What we're building toward.
8. **`09-geometry-palette-discussion.md`** — geometry palette decisions (2026-05-08 base + Revision 2026-05-11 B11 expansion + B13 active mobility additions).
9. **`17-gear-and-spirit-guide-design.md`** — gear architecture; Spirit Guide engine API. Has a 2026-05-12 updates section at top capturing Section 5 closures.
10. **`19-llm-call-map.md`** — Anthropic API call inventory; per-season call counts; cost-monitoring queries.

## Operational

11. **`35-stage-a2-cli-prompt.md`** — copy-paste-ready CLI agent prompt for beginning Stage A2 work. Includes orientation, constraints, engineering disciplines, pending decisions.
12. **`36-b14-5-cli-prompt.md`** — copy-paste-ready CLI agent prompt for beginning B14.5 (recompose-first iterative tuning loop) work. Picks up after `v1.3-b6-generator-validated` lands. Includes nested-loop architecture lock, math-before-code discipline (from KI-B6-1 learnings), 5 open implementation questions for user resolution.

## What's NOT here (in `../collaboration-handoff/`)

The historical/working-discussion folder contains:
- Phase 0-era discussion docs (01-context, 02-doc-maintenance, 03-architectural-proposal, 04-decision-options, 05-action-plan, 08-decomposition-report, 10-decision-log-entry-dimensional-generation)
- Trial-room + class-scoping design discussion (06)
- CLI prompts for past phases (07, 11-15, 18, 20, 23, 24)
- Phase 1 polish + Phase 2/3 prompts (12-15)
- Priority 02 gear CLI prompts (18, 20)
- Three.js demo planning artifacts (22, 25-27)
- Morning orientation snapshots (21)
- README for that historical folder

Those docs are reference material for understanding HOW we got here, but they're not load-bearing for ongoing engineering. Most are CLI prompts that have already been executed; the outputs landed in the canonical docs (this folder), the engine repo, or the demo repo.

## Doc numbering scheme

Numbers preserved from the original `../collaboration-handoff/` layout so cross-references throughout the engine repo, demo repo, and memory files don't break. The numbering doesn't indicate read order anymore — the gaps (between 19 and 28; between 28 and 35) just reflect which docs were canonical vs historical.

## Pending docs (referenced but not yet drafted)

- **`34-earth-meta-layer.md`** — Earth Self meta-layer full design doc; deferred until Matt shares additional notes. Initial design intent captured in `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_earth_meta_layer.md`. Lives in `../collaboration-handoff/` once drafted (or moves to canonical/ if it becomes load-bearing for active work).

## Last major update

**2026-05-12** — cohesion audit + Stage restructure (A1-A7 with interleaved playtests) + operational principles (refactor-not-rewrite, legacy preservation, single-season-per-playtest) + this canonical/ folder split.

Previous milestones:
- 2026-05-11/12: Progression design (Sections 1-12) fully resolved; 54+ LOCKED entries
- 2026-05-11: B11 geometry palette expansion (16 → 25 active); Earth meta-layer reveal
- 2026-05-11: B13 active mobility extension (25 → 30 active); doppelganger mechanic; body-swap pool model
- 2026-05-11: demo1 v1.2 shipped to Vercel
- 2026-05-10: Priority 02 gear closed; demo1 plan locked
- 2026-05-08: Dimensional generation Option C adopted (Phases 1-3 merged; Phase 4-5 deferred)
