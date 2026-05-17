# Dispatch — 2026-05-16 — gandalf — Spatial / floor / wall data JSON-schema recommendation (Tier-1 ARPG-precedent-grounded; movement-speed-synthesis-enabling)

**From:** knight-rider (authored per Matt's 2026-05-16 Day 4 explicit directive following the B10 V2 room-cadence wiring conversation)
**To:** gandalf (primary; design-recommendation owner) + optionally **legolas** (Mode A precursor research IF gandalf surfaces specific Tier-1 ARPG spatial-data-format empirical gaps)
**Approved by:** Matt at 2026-05-16 Day 4 explicit one-liner ("Can you commission Gandalf to let you know what the most appropriate spatial / floor / wall data to build into the JSON packet (matching to Tier 1 ARPG precedent) so that we can synthesize the movement speed of Tier 1 ARPG characters and monsters? This gameplay decision should map into JSON and I want it to be exact.") + load-bearing follow-on directive (2026-05-16 Day 4): **"the movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced."** This makes the implementation cascade load-bearing-for-balance-correctness — not optional Stage A2 polish.
**Status:** PENDING — ACTIVE
**Estimated effort:** 1-2 sessions for gandalf design recommendation; +1 session legolas Mode A IF gandalf surfaces precursor-research needs; design-instinct + empirical-grounding work, not implementation work
**Acceptance:** A design-recommendation document at `canonical/story/spatial-data-jsonschema.md` (or equivalent canonical-story location gandalf picks) specifying: (a) the minimum spatial-data fields (floor, walls, obstacles, entry/exit, etc.) the engine should emit per encounter/room; (b) unit conventions (cell-grid / tile-grid / continuous coordinates / movement-speed-relative units); (c) the schema's match to Tier-1 ARPG precedent with specific citations (PoE / D2 / D3 / D4 / Last Epoch / Grim Dawn); (d) cross-seam wiring map (rocket emits → gamora consumes → star-lord exports → drax renders); (e) concrete JSON schema fragment showing the recommended packet extension; (f) strategic-axis-lock-compatibility note (per Entry 1 sub-locks of `5d51b5a`).

---

## Context — why this dispatch exists

Matt's verbatim ask (2026-05-16 Day 4):

> *"Can you commission Gandalf to let you know what the most appropriate spatial / floor / wall data to build into the JSON packet (matching to Tier 1 ARPG precedent) so that we can synthesize the movement speed of Tier 1 ARPG characters and monsters? This gameplay decision should map into JSON and I want it to be exact."*

**The triggering conversation:** B10 V2 sequential-room semantics shipped earlier today (intermediate tag `gamora/v1.3-b10-v2-sequential-room @ 9db2f5a`). When Matt asked how VS2a's PixiJS demo should wire engine-rooms into visual rooms, knight-rider's foundational answer was: **the engine has NO spatial / floor / wall data in any JSON packet. B10 V2's "room" is a logical encounter-group concept (HP/energy/cooldown carryover); not a physical room with floors/walls.** That answer revealed a structural gap: the demo must invent spatial framing because the engine doesn't supply it.

Matt's directive moves the gap from "demo invents" to "engine supplies, grounded in Tier-1 ARPG precedent." This commission is the design-recommendation step that grounds that supply.

## Current engine spatial state (gandalf's gate-3 finding, verbatim context)

Per gandalf's session-3 deliverable `canonical/story/engine-balance-stewardship.md` Gate-3:

> *"The simulation is NOT fully movement-blind. It has positional state (`range_profile`, `at_melee_range`, `CLOSE_TO_MELEE_TIME=0.5s`, teleport range-closure). But it IS movement-speed-blind in the way Q2 framing requires (no `movement_speed` parameter consumed; no kiting modeling; no L1-vs-L50 movement-speed differentiation)."*

The existing positional state is **simulator-internal** (used during fight resolution; not emitted in any JSON packet at the encounter / room / season level). The gap this commission closes: lifting spatial structure from "simulator-internal abstraction" to "engine-emitted JSON-packet schema" — at a granularity that matches Tier-1 ARPG precedent.

## Companion decisions already locked (load-bearing context)

This commission lands under multiple recent decisions:

1. **2026-05-16 engine-balance-stewardship entry (committed `5d51b5a` family)** — Lock 3 named the movement-modeling abstraction limitation explicitly + scheduled Stage A2 movement-speed-aware sim extension as a B-series item (~2-4 weeks gamora work: 4-band distance spectrum close/mid-close/mid-far/far; kiting AI; `movement_speed` parameter consumption; empirical re-validation of View A). **Your spatial-data schema recommendation is the upstream supply that Stage A2's sim extension consumes.**
2. **2026-05-16 form-bias 5-entry batch (committed `5d51b5a`)** — Entry 1 strategic-axis lock: sub-lock (a) ARPG-canon-primary at substrate-mechanical layer; sub-lock (b) Isekai-canon-primary at narrative-skin layer. Spatial data is substrate-mechanical → sub-lock (a) territory; ARPG-canon precedent is the right anchor.
3. **2026-05-16 cipher-width resolution entry (currently in qa/pending)** — Outcome 2 + Foundation L2 + per-season vocabulary coupling β. The spatial-data schema operates at the substrate-mechanical layer; the per-embodiment narrative-skin layer (Stage 4 form-bias work) layers over it for per-embodiment movement-profile variance (humanoid walk vs slime crawl vs dragon-hatchling glide).
4. **Roadmap items B12 + B13** — both deferred from VS2a per `canonical/16-project-roadmap.md`:
   - **B12** "movement speed / boots / gear slot audit" — your recommendation directly informs B12's scope-shape + sequencing
   - **B13** "active mobility + telegraphs + i-frames" — depends on the spatial-data schema being in place
   
   This commission may surface that B12 should accelerate (post-spatial-data-schema-lock) OR confirm the deferred-from-VS2a sequencing per roadmap.

## What this dispatch produces

A canonical-story document. Suggested path: `canonical/story/spatial-data-jsonschema.md` (your call on exact filename + location). Structure:

### Section 1 — Tier-1 ARPG precedent inventory

Cite specific empirical references on how Tier-1 ARPGs structure their spatial data + movement-speed conventions. Examples to investigate (your judgment on coverage breadth):

| ARPG | What to inventory |
|---|---|
| **Path of Exile** | Map tile system; unit conventions; movement_speed scaling (boot affixes; quicksilver flask); the "10% increased movement speed" stat-line baseline |
| **Diablo II** | Tile-based map system; player movement speed (walk vs run); monster movement-speed-tiers; teleport/leap mechanics |
| **Diablo III** | Instance-grid system; movement-speed cap (25% per item; total caps); monster movement-tier vocabulary |
| **Diablo IV** | Chunk-based world system; dodge mechanics; movement-speed affix tiers |
| **Last Epoch** | Map chunking; movement-skill mechanics; movement-speed scaling stats |
| **Grim Dawn** | Tile-based; movement-speed scaling; teleport/blink mechanics |

For each, surface (a) the in-game-unit convention (tiles? meters? abstract units?); (b) the movement_speed default + max scaling range; (c) how monsters' movement_speed relates to player's (tiers? ratios?); (d) what spatial data is exposed at the data-layer (modders can see this in game files) vs internal-only.

**If your existing research base doesn't cover the technical spatial-data-format specifics, surface as a precursor commission for legolas Mode A.** Legolas's existing research at `agentic_orchestration/research/knowledge/poe/`, `/diablo/`, `/arpg-adjacent/`, `/arpg-community/` is design-philosophy-level; spatial-data-format specifics may need separate Mode A research. Authoring a small "Mode A precursor: Tier-1 ARPG spatial-data-format inventory" commission is part of your dispatch (filed separately if needed).

### Section 2 — Reincarnated's current spatial state + gap analysis

Capture explicitly:
- What spatial state the engine has internally (per the gate-3 finding + any other simulator-internal positional data)
- What spatial data the engine emits in JSON packets today (per knight-rider's prior survey: NONE)
- The gap between "what we need to supply movement-speed-synthesis" and "what we currently expose"
- Anything the engine has internally that just needs lifting to JSON (low-cost gap-close) vs anything that needs new generation work (higher-cost gap-close)

### Section 3 — Recommended JSON packet schema extension

The deliverable's empirically-anchored CORE. Specify:

**Per encounter / room:**
- Floor dimensions + units (e.g., `floor_width_tiles: int`, `floor_height_tiles: int`, with `tile_size_units: "meters" | "abstract"` convention call)
- Wall layout (full geometry? simplified bounding rectangles? perimeter-only?)
- Obstacle positions (occupied tiles? collision shapes?)
- Entry / exit positions (where combatant spawns; where room transitions)
- Encounter-specific spatial constraints (e.g., elite monsters with arena-bounding walls; boss-room teleport-target positions)

**Per combatant (player + monster):**
- `movement_speed_base: float` (the player-spec / monster-spec value the simulator + renderer both consume)
- `movement_speed_scaling: list[float | dict]` (per-level scaling; per-affix scaling; per-buff scaling — your call on representation)
- `movement_profile: enum` (walking / running / crawling / floating / flying / teleporting — for embodiment-aware movement; relates to form-bias Stage 4 per-embodiment narrative-skin work)
- Relevant interaction-with-terrain modifiers (e.g., wall-clip? obstacle-occlusion? floor-affordance?)

**Format choices that bear on the recommendation:**
- Tile-grid vs continuous-coordinate vs hybrid — pick one with reasoning grounded in Section 1 precedent inventory
- Unit conventions (meters / "in-game units" / tiles — pick one)
- Coordinate system (origin location; axis directions)

**Concrete JSON schema fragment** — recommended-shape example for an encounter:

```json
{
  "encounter_id": "...",
  "spatial": {
    "floor": {"width_units": N, "height_units": M, "unit_convention": "..."},
    "walls": [...],
    "obstacles": [...],
    "entry": {"x": ..., "y": ...},
    "exit": {"x": ..., "y": ...}
  },
  "combatants": [
    {
      "id": "...",
      "spawn": {"x": ..., "y": ..."},
      "movement_speed_base": ...,
      "movement_speed_scaling": {...},
      "movement_profile": "..."
    },
    ...
  ]
}
```

Make this concrete enough to implement. Matt asked for EXACT.

### Section 4 — Cross-seam wiring map

For each seam, name:
- Rocket — generation emits these fields (which generation-side dispatch lands the implementation; what schema additions; what MIGRATION.md cross-seam contract)
- Gamora — simulation consumes them per Stage A2 Lock 3b movement-speed-aware sim extension
- Star-lord — export serializes them; telemetry may need new fields (per-encounter spatial-resolution outcomes)
- Drax — PixiJS demo renders them as visual rooms (the wiring Matt asked about earlier today)
- Legolas — if Mode A precursor research happens, file under research/knowledge/

### Section 5 — Strategic-axis-lock compatibility

Per the form-bias 5-entry batch's Entry 1 strategic-axis lock:

- **Sub-lock (a) ARPG-canon-primary at substrate-mechanical layer:** spatial data is substrate-mechanical; Tier-1 ARPG-precedent-grounding satisfies sub-lock (a). Western ARPG-audience players read tile-grids + movement-speed-affixes + boot-slot mechanics as instantly-genre-canonical.
- **Sub-lock (b) Isekai-canon-primary at narrative-skin and convergence layers:** the `movement_profile` enum (walking / crawling / floating / etc.) is the per-embodiment narrative-skin hook — the same substrate-mechanical movement_speed manifests differently per embodiment at the display + UX layer. This aligns with form-bias Stage 4 work (drax's per-embodiment narrative-skin rendering).
- **Three-layer model (Entry 2):** spatial-data schema operates at the substrate layer; per-season "floor type" (e.g., "lava floor" / "ice floor" / "fungal floor") could live at the grouping or vocabulary layer (drax + gandalf future Stage 4 decision); per-embodiment movement-profile lives at the vocabulary layer.

Confirm the schema preserves these layers cleanly (substrate ≠ vocabulary ≠ display).

### Section 6 — Implementation cascade recommendation (LOAD-BEARING per Matt's follow-on directive)

**Critical context per Matt's load-bearing directive:** "the movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced." This means:

- The gamora Stage A2 movement-speed-aware sim extension (per Lock 3b of engine-balance-stewardship) is **load-bearing for gauntlet-balance correctness** — NOT optional Stage A2 polish.
- The implementation cascade below is not a "ship-when-bandwidth-allows" sequence; it is a "ship-before-the-next-balanced-gauntlet-claim" sequence.
- Any gauntlet-balance metric established between now and the movement-speed integration is provisional and may shift when integration lands (analogous to how B10 V2 alone compressed mean |mod-1.0| from 0.82 → 0.3175 — see calibration-epoch implication in Section 7).

Given the load-bearing-for-balance constraint, in what order do the seams ship?

Suggested sequence (your call):
1. **Rocket:** schema-additive at engine generation (analogous to form-bias Stage 1 embodiment-axis additive pattern) — emits floor / wall / obstacle / spawn / movement_speed_base / movement_speed_scaling / movement_profile per the locked schema
2. **Star-lord:** export serialization + telemetry persistence (per-encounter spatial-resolution outcomes; new fields for tracking movement-speed effects on convergence)
3. **Gamora:** simulation consumes for movement-speed-aware sim extension (Stage A2 per Lock 3b) — **THIS IS THE LOAD-BEARING STEP per Matt's directive**; until this lands, the gauntlet simulation is movement-speed-blind and the calibration epoch + cipher-width metrics are subject to re-derivation post-integration
4. **Drax:** PixiJS demo renders visual rooms from the schema (VS2a OR VS2b — your call given drax bandwidth)

The cascade's "balanced gauntlet" trigger condition: post-gamora-Stage-A2-completion + post-fresh-regen-with-movement-speed-integrated. Before that trigger, all gauntlet-balance claims (modifier range, convergence WR, doppelganger gate verdicts, View-A asymmetric KPM finding) are provisional.

OR a different order based on your design-instinct, but the gamora Stage A2 step's load-bearing-ness must hold (you can re-order steps 1/2/4 relative to step 3; you cannot defer step 3 indefinitely).

Also: does this work bear on **B12** (movement speed / boots / gear slot audit) and **B13** (active mobility + telegraphs + i-frames) timing? Both are currently roadmap-deferred from VS2a per `16-project-roadmap.md`. Given the load-bearing constraint, your recommendation likely surfaces that:
- B12 accelerates to land WITH or BEFORE the gamora Stage A2 step (because boots = movement_speed mechanics; integration cycle is more efficient if boots ship alongside the core movement_speed handling)
- B13 may stay deferred (active mobility / telegraphs / i-frames are richer-than-core movement; not load-bearing for basic gauntlet balance)

Surface roadmap-amendment recommendations explicitly; knight-rider drafts the roadmap amendment based on your recommendation.

### Section 7 — Open questions surfaced by the recommendation (gandalf+team convergence checkpoint)

Things the recommendation SHOULDN'T resolve unilaterally — surface for Matt + future dispatches:

- Tile-grid vs continuous-coordinate trade-off — bear on which Tier-1 ARPG precedent dominates the genre-match (PoE/D2/Last Epoch lean tile; D4 leans continuous-chunk)
- Per-embodiment movement_profile enum values — final list lands with form-bias Stage 4 work; this commission proposes initial values
- B12 + B13 sequencing implications — informs roadmap amendments
- Procedural-vs-fixed room generation (per knight-rider's earlier sub-option A/B/C framing) — bear on whether engine emits PER-PLAYTHROUGH spatial data or PER-ROOM-TEMPLATE spatial data
- **🔴 Calibration-epoch implication (load-bearing per Matt's follow-on directive):** the current calibration epoch (committed `c000d7d`; mean |mod-1.0| ≈ 0.82) + the in-pending cipher-width entry's Outcome-2 resolution + gamora's V2 smoke compression (0.3175) + the just-fired post-B6+V2 full regen are ALL grounded in a movement-speed-blind sim. Adding movement_speed to the core sim per the load-bearing directive WILL likely re-shift modifier-range metrics (analogous magnitude to B10 V2's 61% compression). **A new calibration-epoch decisions-log entry will land post-movement-speed-integration** — knight-rider drafts. Until that lands, all current gauntlet-balance claims are provisional. Surface this implication explicitly so downstream agents (gamora B6 main, future balance-loop work) know not to over-anchor on current calibration-epoch numerics.

These are gandalf-flags-for-Matt-decision items, NOT decisions you resolve unilaterally.

## Cross-seam considerations

- **Legolas:** Mode A precursor research IF you surface specific Tier-1 ARPG spatial-data-format empirical gaps. Author the commission as part of your dispatch deliverable; knight-rider relays + activates separately.
- **Rocket, Gamora, Star-lord, Drax:** READ-ONLY consumers for this commission. Your output is the canonical recommendation; each seam's implementation lands in separate downstream dispatches (knight-rider authors per the cascade recommendation in Section 6).
- **Knight-rider:** notify at completion. Drafts the spatial-data-schema decisions-log entry to qa/pending based on your recommendation; routes through jack-ryan Gate 1 + Matt approval + commit. The schema lock becomes the cross-seam contract per ADR-002.
- **Jack-ryan:** future Gate 1 reviewer of the decisions-log entry; secondary reviewer of the canonical recommendation doc IF you want pre-decisions-log review.

## Out of scope (explicit)

- **NO implementation.** This is a design-recommendation; no code changes; no actual schema additions to any seam.
- **NO Stage A2 sim extension authoring.** That's gamora's downstream work (per Lock 3b); informed by but separate from this commission.
- **NO decisions-log entry authoring.** Knight-rider drafts after your recommendation lands.
- **NO B12 / B13 reorg.** Recommendation MAY surface roadmap-amendment implications; knight-rider handles roadmap amendments separately.
- **NO per-embodiment movement_profile final values.** Initial enum values are in scope (you propose); the final list lands with form-bias Stage 4 per-embodiment narrative-skin work.
- **NO PixiJS-rendering-side decisions.** Drax's downstream consumption is informed by your schema; drax's specific rendering choices are drax's domain.
- **NO physics simulation requirements.** The schema enables movement-speed-synthesis at the simulation-level (per Lock 3b's 4-band distance spectrum); it does NOT require full physics simulation. The schema is data; the simulator's mechanical-resolution is gamora's seam.
- **NO commitment to procedural vs fixed room generation.** Either is compatible with the schema; the procedural-vs-fixed decision is a future dispatch chain.

## Required reading

Engine + design context:
- `reincarnated-engine/design/decisions/decisions-log.md` — 2026-05-16 engine-balance-stewardship entry (Lock 3 specifically; the movement-modeling abstraction limitation source-of-truth)
- `canonical/story/engine-balance-stewardship.md` (your own session-3 deliverable; gate-3 spatial-state diagnostic verbatim)
- `canonical/story/engine-generic-meta-structure.md` (the three-layer model framing)
- `canonical/story/form-bias-cadence-strategy.md` (strategic-axis lock + cadence Option II + four sub-locks; especially § 5.1 + § 7.1 Stage 4 for per-embodiment narrative-skin context)
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 1 strategic-axis + Entry 2 three-layer model + Entry 5 cadence
- 2026-05-16 cipher-width resolution entry (currently in qa/pending at `agentic_orchestration/qa/pending/2026-05-16-decisions-log-cipher-width-resolution.md`) — for Outcome 2 + Foundation L2 + β coupling context

Roadmap + scope:
- `canonical/16-project-roadmap.md` §VS2a (current scope; B12 + B13 deferred-from-VS2a framing) + §VS2b (Substrate Realignment; relevant for spatial-schema future integration)

ARPG-precedent base (legolas's existing research; gap-flag if insufficient):
- `agentic_orchestration/research/knowledge/poe/2026-05-16-poe-design-philosophy.md`
- `agentic_orchestration/research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md`
- `agentic_orchestration/research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md`
- `agentic_orchestration/research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md`

Engine code (read-only context; understand current simulator-internal positional state):
- `reincarnated-engine/src/reincarnated/simulation/fight_engine.py` (range_profile, at_melee_range, CLOSE_TO_MELEE_TIME)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (where the simulator-internal positional state lives)

## Acceptance criteria

- [ ] Deliverable filed at `canonical/story/spatial-data-jsonschema.md` (or your chosen canonical-story location)
- [ ] All 7 sections present
- [ ] Section 1: Tier-1 ARPG precedent inventory with specific citations (NOT vague references); legolas Mode A precursor commission flagged if gaps surface
- [ ] Section 2: gap analysis grounded in engine's current spatial state (simulator-internal + JSON-emitted)
- [ ] Section 3: concrete JSON schema fragment — EXACT enough to implement (per Matt's directive)
- [ ] Section 4: cross-seam wiring map covers all 4 affected engine + demo seams
- [ ] Section 5: strategic-axis-lock-compatibility note explicit
- [ ] Section 6: implementation cascade recommendation with reasoning; B12/B13 sequencing implications named
- [ ] Section 7: open questions parking with explicit decision-dependencies
- [ ] Knight-rider notified at completion; decisions-log drafting cascade triggered

## Out of scope (explicit — repeated for emphasis)

The commission produces a DESIGN RECOMMENDATION. It does NOT:
- Implement the schema (rocket dispatch follow-on)
- Implement the sim consumption (gamora Stage A2 dispatch follow-on)
- Implement the rendering (drax dispatch follow-on)
- Author decisions-log entries (knight-rider follow-on)
- Amend the roadmap (knight-rider + Matt follow-on)
- Commit to per-embodiment movement-profile final values (form-bias Stage 4 follow-on)

The recommendation is the INPUT to those downstream dispatches; not the dispatches themselves.

---

## Completion record

**Completed:** 2026-05-16 (Day 4)
**Deliverable path:** `canonical/story/spatial-data-jsonschema.md`
**Legolas Mode A precursor commission triggered:** N (drafted as OPTIONAL Section 9 of deliverable; knight-rider routes only if Reincarnated moves toward modder-tooling territory OR Matt wants implementation-detail validation prior to gamora Stage A2 — gandalf judgment: NOT required for current schema lock; existing Legolas knowledge base is design-philosophy-sufficient)
**Tier-1 ARPG precedent vendors inventoried:** 6 (PoE / D2 / D3 / D4 / Last Epoch / Grim Dawn) — per-vendor: architecture choice, unit convention, spatial-data-exposure level, movement_speed reference, lesson-for-Reincarnated
**Schema fragment lines:** concrete-enough-to-implement per Matt's "exact" directive — full JSON shape in Section 3 with field-by-field rationale + value ranges + per-encounter-kind dimension library initial values + initial enum values for movement_profile / encounter_kind / spatial_complexity_tier / floor.shape
**Implementation cascade recommendation summary:** 6-step sequence — (1) knight-rider decisions-log entry; (2) rocket schema-additive; (3) gamora Stage A2 sim consumption (THE LOAD-BEARING STEP per Matt's directive; until this completes ALL current gauntlet-balance claims are provisional); (4) star-lord telemetry persistence (parallel-compatible); (5) drax PixiJS demo consumption (parallel-compatible with Step 3); (6) knight-rider post-integration calibration-epoch decisions-log entry. VS2a-ship gating: Steps 1+2+5. Next-balanced-gauntlet gating: Step 3.
**B12 / B13 sequencing implications surfaced:** B12 full audit (boots / gloves / belt / +%MS affixes / hard-cap) recommended for **Stage-A2-co-shipping** with gamora Stage A2 — tighter integration cycle (boots' +%MS modifier extends core movement_speed handling natively). B13 active mobility / telegraphs / i-frames recommended to **stay deferred** to current Stage A2 slot — not load-bearing for balance correctness; re-evaluate post-VS2a + post-Stage-A2 + post-full-B12.
**Open questions parked:** 8 (Q1 dimension library values; Q2 wall geometry representation; Q3 obstacle scope; Q4 movement_profile final list; Q5 spatial-block DB vs file-only; Q6 tile-grid forward-compatibility for modder tooling; **Q7 calibration-epoch implication — LOAD-BEARING per Matt's follow-on directive; current calibration epoch grounded in movement-speed-blind sim and WILL likely shift post-Step-3-integration; new calibration-epoch decisions-log entry lands post-integration per Step 6**; Q8 VS2b interaction — orthogonal)
**Notes for knight-rider:**
- Decisions-log entry should capture: (a) schema lock as cross-seam contract per ADR-002; (b) load-bearing-for-balance cascade per Section 6; (c) calibration-epoch provisional-until-Step-3 implication per Section 7 Q7; (d) B12 Stage-A2-co-shipping recommendation; (e) B13 keep-deferred recommendation; (f) reference this deliverable as authoritative
- Cross-seam dispatches needed: rocket (schema-additive emission, ~4-6h); gamora (Stage A2 sim consumption per Lock 3b, ~1.5-2 weeks — the critical path); star-lord (telemetry persistence + spatial-block DB column, ~2-3h); drax (PixiJS demo consumption, ~1-2 days — already commissioned per movement-speed-baseline; spatial-block consumption is minor additive lift)
- Roadmap amendment surface: consider promoting full B12 to Stage-A2-co-shipping (alongside gamora Step 3) — Matt-decision; knight-rider drafts
- Calibration-epoch decisions-log entry timing: post-Step-3 completion + post-fresh-regen; supersedes current epoch (c000d7d) per Matt's load-bearing directive
- Legolas Mode A precursor commission filed as Section 9 of deliverable; activation optional + Matt-discretion
