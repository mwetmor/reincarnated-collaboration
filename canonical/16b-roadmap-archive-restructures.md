# 16b — Roadmap Archive: Restructures and Scope Migrations

**Purpose:** Meta-history of major roadmap restructures, scope migrations, and stage-numbering shifts. Companion to `16-project-roadmap.md` (forward-looking) and `16a-roadmap-shipped-log.md` (shipped record).

**Stewardship:** gandalf appends to this doc when a structural restructure happens. Rarely consulted; preserves audit trail for "why did this stage move?"-type questions.

---

## 2026-05-16 (Day 4) — Three-doc split (this restructure)

**Event:** `canonical/16-project-roadmap.md` had grown to 847 lines through repeated in-place edits. Mixed strategic anchor + per-stage detail + per-item commit logs + risk sections + interleaved playtest notes + retrofit annotations (*"PROMOTED 2026-05-16"*, *"split 2026-05-16"*, *"baseline subset already shipped in VS2a per 2026-05-16 split"*). Matt reported he could not parse current state from the doc.

**Decision:** Split into three docs:

1. **`16-project-roadmap.md`** — forward-looking only. Target ≤250 lines. Strategic anchor + current-quarter milestones (VS2a, VS2b) + what comes after + open decisions + cross-references. **What's actively in flight or upcoming.**
2. **`16a-roadmap-shipped-log.md`** — historical record of what's shipped, sub-progress detail, closed/locked decisions reference. Append-only by convention.
3. **`16b-roadmap-archive-restructures.md`** (this doc) — meta-history of restructures + scope migrations.

**Rationale:**
- The forward-looking roadmap is consulted multiple times per session by knight-rider, gandalf, jack-ryan during decision loops. It must be terse and current.
- Historical record matters but doesn't need to compete for visual attention against forward planning. Separation reduces cognitive load on every read.
- Append-only `16a` honors the prior doc's rule ("don't rewrite history"). The split puts that rule on a separate page rather than asking the forward-looking doc to enforce it.

**Authored by:** gandalf, on Matt's authorization at Day-4 close (immediately following the past-2-hours summary that surfaced the bloat).

**Content migration map:**

| Original section in old `16` | New home |
|---|---|
| Strategic anchor (file 29) | `16` (condensed) |
| Status snapshot | `16` (condensed; today's shipped sub-items folded into `16a` Stage A2 sub-shipped log) |
| Four-track work model | `16` (condensed) |
| Stage A1 detail | `16a` § Stage A1 |
| Stage A2 sub-progress table | `16a` § Stage A2 sub-shipped log |
| Stage A2 yellow-flag investigations | `16a` § Stage A2 yellow-flag investigations |
| Stages A3-A7 detail tables | `16a` § Stage detail (forward reference) |
| Playtest cycles 1-4 | `16` (condensed to bullet list); detail moves to `16a` per-stage |
| Substrate Realignment workstream | `16` (condensed; current stage status); historical context retained inline |
| VS2a / VS2b sections | `16` (UPDATED with today's shipped sub-items; risks condensed; design watch-items kept) |
| Parallel-execution risks (5 risks) | `16` (condensed to table) |
| Track A landing rhythm | `16` (kept) |
| Single-season-per-playtest rule | `16` (kept, condensed) |
| Refactor vs rewrite | `16` (kept, condensed) |
| Tracks B / C / D | `16` (condensed) |
| Open design decisions | `16` (kept; reorganized by what they block) |
| Closed/locked decisions list | `16a` § Closed/locked decisions reference |
| Polish / small work | `16` (kept) |
| Far-future | `16` (kept, condensed) |
| Rough timeline table | `16` (kept, simplified) |
| Memory cross-references | `16a` § Memory cross-references |
| Doc cross-references | `16` § Doc cross-references |
| How to update | `16` § How to update (forward-looking specifically) |
| Navigation (how to engine work / demo work) | `16a` § Navigation |

**Length outcome:** `16` shrank from 847 → ~250 lines forward-looking. `16a` carries shipped detail. `16b` (this doc) carries restructure meta-history.

---

## 2026-05-16 (Day 3-4) — Milestone re-targeting around VS2a + VS2b

**Event:** Matt locked a parallel-workstream mandate: *"All Substrate Realignment S1–S3 + embodiment-axis + Pimen full integration projects move as quickly as possible and in parallel so that as soon as demo VS2a ships, VS2b is right behind it, waiting as a ticket."*

**Scope migration:**
- Demo work was previously framed as "incremental demo1 refactor within each Track A stage" (LOCKED 2026-05-12).
- New framing: upcoming demo target splits into **two sequential ship milestones with parallel workstreams converging on each.**
  - **VS2a** — Gauntlet + Geometry + First Catalogue Integration. Subset of Stage A2 items + B10 V2 (promoted from deferred) + first Pimen integration.
  - **VS2b** — Substrate Realignment + Full Catalogue Integration. S1–S3 cipher migration + embodiment-narrative display + Pimen full integration. Ships 2-4 weeks after VS2a.
- Items NOT in VS2a (B7, B12 full, B13, B14, B16) defer to post-VS2a Stage A2 completion.
- Stages A3-A7 retain original sequencing but downstream of the VS2 push.

**Other 2026-05-16 promotions:**
- **B10 V2** (sequential-room semantics) — PROMOTED from deferred → in scope for VS2a. Required for the stated AOE differential goal.
- **B12 baseline subset** (movement-speed schema) — PROMOTED to VS2a; full B12 audit (boots/gloves/belt + +% MS affixes + hard-cap) remains Stage A2.
- **VS2a arena topology** — superseded single-ellipse `clampToEllipse` with Diablo/PoE square-room + rectangular-hallway model.
- **B11 demo-integration phase** — gated on geometry × element VFX coverage assessment per gandalf gap-severity work; ungated and shipped 2026-05-16.

**Rationale:** the parallel-workstream mandate addresses the form-bias work's structural timing problem — Substrate Realignment was previously framed as "interleaved with Track A stages" without a concrete ship target. Tying VS2b to a near-term ship trigger gives it operational reality.

**Authored by:** Matt directly (the parallel-workstream mandate), gandalf (the VS2a/VS2b decomposition and risk analysis), knight-rider (dispatch cascade).

---

## 2026-05-12 — Stage A1 → A7 restructure (cohesion audit)

**Event:** Original sequence was Stage A1 bug-fixes → Stage A2 content quality → Stages A3-A8 (linear ARPG-genre maturation). Cohesion audit revealed sequencing problems.

**Scope migration:**
- Engine bug fixes A1/A1b/A2/A4 folded into the ARPG-genre sprint (formerly Stage A3, now Stage A2) since that sprint regenerates all seasons anyway — avoids double-regen.
- **Stage numbering shifted down by one** for items after the original A2.
- **Playtest cycles interleaved between major stages** since most progression-design feel questions (skill tree UI, body-swap moment tension, doppelganger feel, set collection satisfaction, Spirit Guide coaching effectiveness) cannot be validated from JSON/telemetry alone.
- **B16 (loot drop architecture)** added to Stage A2 per Matt's gap-catch — Option A (full architecture, not stub).
- **B14.5 V1** (recompose-first iterative tuning loop) shipped 2026-05-12; canonical pattern locked for balance loops.
- **Progression system implementation moved to Stage A7** — design fully resolved in file 32 (all 12 sections LOCKED) + file 33 (skeleton).

**Decisions locked at this restructure:**
- Single-season-per-playtest rule
- Refactor vs rewrite (Track A is REFACTOR not rewrite)
- 3 acts locked (per-act bands A1: L1-17, A2: L18-33, A3: L34-50)
- Demo strategy: demo1 (Pixi.js) incrementally refactored — NOT rebuild demo2, NOT defer-to-Unity

**Cumulative Track A working effort:** ~29-42 weeks (Stages A1–A4 + A7 + 4 playtest cycles; A5 opportunistic; A6 deferred).

**Authored by:** Matt + knight-rider (cohesion audit + sequencing); folded into roadmap doc that day.

---

## 2026-05-11 — Roadmap full rebuild (post-demo1-ship)

**Event:** Demo1 v1.2 shipped. Pre-rebuild roadmap content was framed pre-demo1 with stale priority order and timeline.

**Scope migration:**
- Roadmap restructured around four-track work model (per file 29): Track A engine 1 maturation / Track B engine 2 prototyping / Track C engine 2 build / Track D integration + ship.
- Engine queue (file 28) mapped to concrete ship order via 7 stages with interleaved playtest cycles.
- Decisions-log entries closed (and re-cited in the rebuilt roadmap) for: dimensional generation Option C; canonical element palette; B9 endgame baseline; B9c reset model; B5 hotbar pattern; solo gameplay Phase 0.

**Authored by:** Matt + knight-rider.

---

## Future restructures

Append new entries here when a structural restructure happens. Triggers that warrant a new entry:

- A new track is added (Track E, etc.)
- Multiple stages migrate between tracks
- A milestone is added that affects per-stage sequencing across multiple sub-items
- Doc-structure changes (e.g., splitting `16a` into multiple files)
- Stewardship-model changes (e.g., transferring forward-looking roadmap from gandalf to another role)

**Don't append for:** routine sub-item ships (those go to `16a`); single-decision lands (those go to decisions-log); estimate adjustments (those go to `16` timeline table).
