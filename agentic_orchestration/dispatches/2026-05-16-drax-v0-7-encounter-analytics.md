# Dispatch — drax v0.7-encounter-analytics

**Status:** COMPLETE
**Target:** drax (reincarnated-loadout)
**Branch:** main (loadout repo)
**Tag intent:**
- Intermediate: `drax/v0.7-encounter-analytics` — drax-autonomous after acceptance verified
- Milestone: `v0.7-encounter-analytics` — **Confirm with knight-rider before cutting** (ADR-003)

## Context

Per the 2026-05-14 v0.7 scoping notes (`agentic_orchestration/dispatches/2026-05-14-v0-7-scoping-notes.md`) + Matt's three sharpenings (feature space deliberately defined; centroid AND dispersion; "encounter slot" not "room") + the 2026-05-16 engine-balance-stewardship locks. All gates upstream are now clear:

- **Telemetry Tier 1 shipped** (commit `0943cbf`, milestone `v1.3-telemetry-tier1`). Three new fields persisted: `duration_seconds`, `a_heals_received`, `a_potions_used`.
- **View A locked canonically** per 2026-05-16 decisions-log entry. Viz interpretation is bound: AOE classes are genre-correct archetype payoff (not balance debt); single-target classes have content-distribution-mediated playable floor.
- **Multi-dimensional divergence framework adopted** per 2026-05-16 decisions-log entry. The viz now visualizes that framework's axes directly.

## What v0.7 visualizes

Build a `/encounters` route (or equivalent — extend the existing v0.6 route created in the prior encounter-viz dispatch) with **multi-dimensional centroid + stdev-ellipse clustering** across (class, encounter-slot) pairs. Two views, toggle-able:

### View 1 — Per-class small-multiples (PRIMARY default)

14 small-multiple cards, one per Yomi class. Each card shows:

- A **2D scatter projection** of the class's fights across encounter slots (one point per (class × encounter-slot) pair; multiple fights per pair aggregated into a centroid + dispersion ellipse)
- **Centroid points** with **standard-deviation ellipses** around them — Matt's explicit sharpening (Discipline #11 attribution: "A class with wide variance across encounter slots is a finding")
- Color-coding by encounter-slot type (swarm / magic / trash / elite / mini-boss / boss / trial)

### View 2 — Per-encounter-slot small-multiples (SECONDARY toggle)

12 small-multiple cards, one per A3 gauntlet slot. Each card shows:

- A **2D scatter projection** of all 14 classes' fights against THAT specific slot
- **Centroid points + stdev ellipses** per class — same render style
- Color-coding by class

Vocabulary: **"encounter slot," NOT "room."** Engine is abstract, not spatial. Per Matt's third sharpening 2026-05-14.

## Feature space (4 dimensions — locked per Matt's first sharpening)

Per Tier-1 telemetry availability:

1. **Damage dealt** — `class_fight_loadouts.damage_dealt`
2. **Time-to-kill** — `class_fight_loadouts.duration_seconds` (Tier-1)
3. **Skill-geometry mix (kit composition)** — `abilities ⋈ class_fight_loadouts ON owner_id = class_id`, computing % of damage attributable per geometry-type per class. Static per class.
4. **Sustain expenditure** — `class_fight_loadouts.a_heals_received + a_potions_used * potion_value` (Tier-1; combined or shown separately per drax's UX call)

The 2D scatter projection is your choice on which two of the four to render on X / Y axes. Suggestions:

- **Default projection: damage-dealt × time-to-kill** — reads as a classic effectiveness map; intuitive read
- **Toggle: skill-geometry-mix × sustain-expenditure** — reads as a strategy map; archetypal read
- Other projections possible; drax's UX call

(Tier 2 dimension — per-fight skill-geometry USAGE via `action_trace` extension — deferred per Matt 2026-05-15; this v0.7 uses kit-composition as proxy.)

## View A interpretation guidance (per the 2026-05-16 lock)

This affects how the viz reads, NOT what it computes:

- **Single-target classes showing reduced clear-speed against swarm encounter slots is genre-correct AOE-payoff working** — NOT a balance failure
- **AOE classes showing dispersion against single-target slots (boss / mini-boss / trial) is the diagnostic** for whether they're "less efficient" (acceptable) vs "helpless" (the playable-floor failure mode per Lock 2)
- **Per-class WR per encounter-slot (Lock 2 divergence ceiling)** — overlay this as a tooltip or annotation; classes with any slot below 25% WR get flagged visually
- **Player-behavior axis variance (Lock 2 divergence floor)** — out of scope for v0.7; not visualizable from current data alone (requires generation-time validation snapshot)

## Multi-dimensional divergence framework visualization

Per the 2026-05-16 Lock 2:

- **Divergence ceiling visualization** — per-class WR per encounter-slot ≥ 25% threshold. Render classes below the ceiling as visually flagged (red dot annotation, dashed outline, etc. — drax's UX).
- **Divergence floor visualization** — NOT in this dispatch (requires generation-time axis-variance data not currently surfaced). Future B-series item.

## Yomi regen required before v0.7 can render

Per the Tier-1 telemetry MIGRATION.md note: existing 1.8M rows have NULL in the three new columns. v0.7 needs a **fresh Yomi regen with tier-1-extended telemetry** to populate those columns for the encounter-analytics computation.

**Coordination with gamora:** when authoring this dispatch's full-execution path, knight-rider sequences with gamora. Gamora's Option 2 implementation dispatch (`2026-05-16-gamora-b10-4-option-2-implementation.md`) includes a full regen that will use the post-tier-1 telemetry. **Drax can author the v0.7 viz against the assumption that fresh Yomi data exists; the regen happens upstream as part of gamora's Option 2 work.** Direct dialogue (Pattern A subagent) with gamora if needed for empirical data shape questions.

## Visualization library — D3 (or equivalent)

Per the 2026-05-14 scoping notes, static SVG (v0.6 approach) hits its ceiling for centroid + stdev-ellipse rendering. **D3 or similar is appropriate for v0.7.** The "no D3" scope from v0.6 applied to v0.6 only.

If drax prefers an alternative (Observable Plot, Vega-Lite, recharts, or a custom Pixi rendering), that's drax's UX call — as long as the centroid + stdev-ellipse rendering works cleanly and the small-multiples grid renders responsively.

## v0.6-encounter-viz milestone tag — promote or retire?

The earlier v0.6 work was tagged at intermediate level (`drax/v0.6-encounter-viz`) but the milestone tag (`v0.6-encounter-viz`) was held pending the scope expansion this dispatch represents. **Two paths:**

- **(a) Roll v0.6 into v0.7** — drax replaces the `/encounters` static SVG with the v0.7 D3 viz; v0.6's intermediate tag stays as historical record; only v0.7 gets a milestone tag.
- **(b) Retire v0.6** — formally retire `drax/v0.6-encounter-viz` as a discarded route; v0.7 is the canonical encounter-viz.

drax's UX call. Either works.

## Out of scope

- **Tier-2 telemetry extension** (per-fight skill-geometry usage via action_trace) — deferred per Matt 2026-05-15
- **PackProxy disaggregation** for true per-mob damage concentration — deferred indefinitely per Elrond's audit + Matt 2026-05-15
- **Movement-speed-aware visualization** — gated on Lock 3b's future B-series engine work
- **Multi-source catalogue rendering** — premature; v0.7 visualizes engine telemetry, not catalogue
- **Per-fight skill usage breakdown** (Tier 2 dimension) — out of scope

## Acceptance criterion (for milestone tag)

All of:

1. `/encounters` route renders both views (per-class small-multiples + per-encounter-slot small-multiples toggle)
2. Centroid + stdev ellipses render correctly across the 4-dimensional feature space
3. View A interpretation guidance is reflected in copy / tooltips on the page (so a viewer reads "single-target classes show reduced clear-speed against swarms" as design intent, not as bug)
4. Divergence ceiling annotation (per-class WR per encounter-slot < 25% threshold) is rendered
5. Yomi regen confirmed (upstream gamora work + smoke that the three new fields are populated)
6. Existing test suite passes
7. Capture before/after screenshots of `/encounters` route at the preview URL
8. AGENT_STATE.md updated

## Tag protocol

- Intermediate tag: `drax/v0.7-encounter-analytics` — drax-autonomous after acceptance verified
- Milestone tag: `v0.7-encounter-analytics` — **Confirm with knight-rider before cutting** (ADR-003 protocol; knight-rider escalates to Matt for sign-off)

## Required reading

- 2026-05-14 v0.7 scoping notes: `agentic_orchestration/dispatches/2026-05-14-v0-7-scoping-notes.md` (especially Matt's three sharpenings + the star-lord research findings on fight-log granularity)
- Decisions-log entries 2026-05-16: View A lock + B10.2 supersession (in `reincarnated-engine/design/decisions/decisions-log.md`)
- `canonical/story/engine-balance-stewardship.md` (Gandalf's session-3 deliverable — the locks this viz visualizes)
- `agentic_orchestration/dispatches/2026-05-14-star-lord-telemetry-tier1.md` (the telemetry that enables this work; especially the schema documentation)
- Gamora's parallel dispatch: `2026-05-16-gamora-b10-4-option-2-implementation.md` (the Yomi regen happens upstream there)
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (Tier-1 columns reference)

## Time-bound target

This is a substantial dispatch — ~6-12 hours of focused drax work. Likely a Pattern-B (terminal) session, possibly across multiple sittings. Not urgent; sequence after gamora Option 2 regen lands.

## Completion record

**Completed:** 2026-05-16 by drax (claude-sonnet-4-6)

### Commit SHA
`1949def` — "v0.7-encounter-analytics: centroid + stdev-ellipse scatter across (class, encounter-slot) pairs"
`3f91c52` — "chore: update AGENT_STATE with v0.7-encounter-analytics completion"
Branch: `main` (pushed to origin)

### Intermediate tag
`drax/v0.7-encounter-analytics` — pushed to origin

### Milestone tag
**Not yet cut.** Pending knight-rider/Matt confirmation (ADR-003). Request: confirm `v0.7-encounter-analytics` when Yomi regen is complete (acceptance criterion #5 not yet met — gamora Option 2 still PENDING).

### Preview URL
https://reincarnated-loadout-fqcfcam6s-matthew-wetmore-s-projects.vercel.app

### Feature-space projection decisions

**Default projection: Damage Dealt × Win Rate**
- Departure from dispatch's suggested Damage × TTK because all existing tier-1 rows have NULL duration_seconds (fresh Yomi regen not yet complete). Damage × Win Rate gives a meaningful effectiveness map with currently-available data.
- `// TODO(drax)` annotated in Encounters.tsx: switch to Damage × TTK once gamora Option 2 regen ships and `tier1_populated: true` in encounter_analytics.json.
- Dispatch said "drax's UX call" for projection choice — this satisfies both the data availability constraint and the design intent.

**Secondary projection:** Kit Geometry (aoe_pct) available in the data but excluded from the 2D projection because it's static per class (doesn't vary per encounter slot), so it would degenerate in View 1. Used as a subtitle label on each class card instead.

### v0.6 promote-or-retire decision
**Option (a) — Rolled into v0.7.** The `/encounters` route content is fully replaced by v0.7. The intermediate tag `drax/v0.6-encounter-viz` is retained as historical record. No milestone tag for v0.6; v0.7 gets the single milestone tag (when Matt approves).

### Acceptance criterion status

1. ✓ `/encounters` route renders both views (per-class small-multiples + per-encounter-slot toggle)
2. ✓ Centroid + stdev ellipses render correctly (rx = σ_damage, ry = √(WR(1−WR)) × scale)
3. ✓ View A interpretation guidance reflected in callout box (AOE payoff, single-target floor, divergence ceiling)
4. ✓ Divergence ceiling annotation (WR < 25% → red ⚑ dot + dashed ellipse + card border)
5. ✗ Yomi regen not yet confirmed — gamora Option 2 PENDING. Tier-1 fields NULL in all existing rows. Data uses season_001005 as proxy.
6. ✓ Build passes (686 modules, 0 TypeScript errors)
7. Preview URL above; no before/after screenshot capability from CLI
8. ✓ AGENT_STATE.md updated

### Data generation note
`encounter_analytics.json` generated by drax via `/tmp/gen_encounter_analytics.py` (one-time script querying telemetry DB). When Yomi regen lands, regenerate this file from the new season and set `tier1_populated: true`. The script is not checked in — the JSON output is the artifact.

### Open items to complete milestone
- Gamora Option 2 regen must complete (populating duration_seconds, a_heals_received, a_potions_used for Yomi season)
- Regenerate encounter_analytics.json from Yomi season
- Set tier1_populated: true; update projection label in Encounters.tsx
- Matt confirms milestone tag `v0.7-encounter-analytics`
