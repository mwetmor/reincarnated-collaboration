# VS2a Scope of Work — Hive Mode (continuing from engine-rebuild closure)

**Authored:** 2026-05-19 by knight-rider at engine-rebuild v1.0 batch close (continuation per dispatch § 6.5).
**Authority:** Matt directive 2026-05-19 (autonomous-operation continues); v1.0 disposition § 5.1 (engine-rebuild → VS2a forward routing); `canonical/16-project-roadmap.md` § "VS2a — Gauntlet + Geometry + First Catalogue Integration" (gandalf-stewarded).
**Status:** **Live executable plan.** Updated by knight-rider as workstreams advance. Co-evolves with `coordination-matrix-vs2a.md`.
**Estimated duration:** ~3–4 months wall (gandalf roadmap estimate); shorter if R8-inversion path adopted for kit-redesign.
**Operating mode:** AUTONOMOUS — continues from engine-rebuild batch. No L3-to-Matt; gandalf decides cross-cutting; knight-rider sequences; specialists author code. Matt re-enters only at wind-down.
**Companion artifacts:** `coordination-matrix-vs2a.md` (per-item seam mapping + DAG); `state-of-hive-YYYY-MM-DD-vs2a.md` (daily digests starting 2026-05-20).
**Predecessor:** `scope-of-work-engine-rebuild.md` (engine-rebuild batch; CLOSED at v1.0).

---

## § 0 — TL;DR

VS2a closes the geometry + catalogue + first-playable-gauntlet integration so a player drops into a Diablo/PoE-style room sequence with tier-diverse encounters, new geometry shapes, real VFX, coherent movement, and a real skill tree. Anchored to **end-game balance state** (Matt verdict reversal 2026-05-16 Day-4 close).

**13 items total:** 6 engine-rebuild fall-outs (new this session) + 7 existing roadmap items. Some in-flight from prior sessions; some not yet dispatched.

**First-fire batch (can fire immediately, autonomously):**
- **F1** — `geometry_type` per-skill schema field (rocket + star-lord; engine-rebuild fall-out HIGH)
- **F2** — gandalf Gate-1: kit-redesign approach decision (hand-redesign vs R8-inversion vs hybrid)
- **F3** — gandalf Gate-1: Drift-14 + Drift-15 design framework + autonomous-vs-Matt-gated step separation
- **F4** — drax B6 skill-tree UI surface decomposition design dispatch (CRITICAL gap; drax-authored)
- **F5** — legolas commission: Drift-14 pool × VFX-catalogue mapping audit (Mode B catalogue crawl; gandalf design-track in parallel)
- **F6** — legolas commission: Drift-15 environment tileset catalogue sweep (Mode B; gandalf framework in parallel; Matt selection step held for wind-down)

**Second-fire batch (gated on first-batch outputs):**
- **S1** — kit-redesign sprint (rocket + gandalf consult) — gated on F2 (gandalf approach decision) + F1 (`geometry_type` schema lands)
- **S2** — B6 main work (rocket + gamora) — depends on rocket pre-work + S1 coordination
- **S3** — Gate-3b sim MS extension (gamora) — gated on rocket schema-default-update + star-lord export-DTO fix

**In-flight continuations (already underway from prior sessions):**
- **C1** — Movement-speed baseline (rocket + drax + gamora; Option-B values locked; finishing implementation)
- **C2** — B11 GREEN-list element VFX (11/13 elements; drax + elrond Pimen ingest)
- **C3** — Character-track ingest (chierit Elementals; drax)
- **C4** — Pimen curation pipeline + subset selection (elrond)

**Late-stage (after above land):**
- **L1** — Demo regen on a single season (star-lord + gamora; post-pool-cull) — **VS2a SHIP GATE**

**Matt-gated (held for wind-down):**
- **M1** — Drift-15 Matt-selection step (3 environment tilesets per Matt eye)
- **M2** — v0.12 + v0.16 engine-rebuild playtest tags (carryover from engine-rebuild)

---

## § 1 — Engine-rebuild fall-out items (new to VS2a)

### § 1.1 — F1 — `geometry_type` per-skill schema field ⭐ *fire first*

- **Owner:** rocket (schema + catalogue) + star-lord (telemetry/export adaptation)
- **Origin:** R2 H1 disposition § 3.1 + jack-ryan Q1 disposition (gate1-r2-math-note-2026-05-19.md)
- **Inputs:** R2 H1 instrument-limited finding (name-heuristic 43/3/4 sample imbalance); current `spatial_engine._determine_geometry_type()` heuristic
- **Deliverables:**
  - Add `geometry_type` enum field to skill schema (`circle / cone / line / point / mixed / none`)
  - Backfill across 5 shipped seasons (re-derivation from geometry-type defaults OR re-roll at next regen; whichever is more efficient given regen cadence)
  - Update `_determine_geometry_type()` to direct field read with name-heuristic as fallback (Pattern P7 disciplined; fail-loud on `mixed` or `none` when value should exist)
  - MIGRATION.md authored (additive nullable column; backward-compatible)
- **Hypothesis test:** Re-run R2 sub-gauntlet on re-converged season with explicit field. H1 variance ≥ 0.10 under original threshold confirms spatial signal is load-bearing as predicted (28pp delta currently observed).
- **Effort:** ~2-4 weeks parallel with kit-redesign sprint
- **Activation gate:** none — fires immediately
- **Re-test tag (post-completion):** `vs2a/v<X>-r2-h1-revalidated`

### § 1.2 — F2 — Gandalf Gate-1: kit-redesign approach decision

- **Owner:** gandalf (design steward) — Gate-1 decision
- **Origin:** R1 disposition § 8 + `canonical/story/r1-kit-redesign-queue-2026-05-19.md` § 5
- **Question:** **Should VS2a kit-redesign proceed via (a) hand-redesign of 30-40 broken/mediocre classes per § 3.1-§ 3.5 criteria, OR (b) R8-inversion regeneration of the entire catalogue from scratch under inverted pipeline, OR (c) hybrid (subset of kit-broken classes regenerated under R8-inversion; remaining mediocre classes hand-redesigned)?**
- **Why gandalf:** roadmap-shape decision affecting B6 + S1 dispatches; both paths viable; trade-offs are design (hand-redesign preserves curated kits; R8-inversion is faster + cheaper + tests R8 disposition at scale)
- **Inputs:** R1 kit-redesign queue doc § 5.3 alternative path; R8 disposition Sub-case 3 (`inverted` is default; substrate-identity confirmed); R1 sprint v3 per-class category partition (forthcoming as gamora telemetry rendered)
- **Deliverables:** decision doc at `canonical/story/vs2a-kit-redesign-approach-2026-05-XX.md` capturing:
  - Path chosen
  - Rationale
  - B6 main-work implications
  - First-batch class selection criteria
  - Validation gate (R1 sprint re-run as canonical metric)
- **Hypothesis test:** N/A (decision; not testable)
- **Effort:** 0.5-1 day gandalf
- **Activation gate:** none — gandalf fires when ready under autonomous L2-equivalent authority

### § 1.3 — F3 — Gandalf Gate-1: Drift-14 + Drift-15 design framework

- **Owner:** gandalf (design steward) — Gate-1 framework + autonomous-vs-Matt-gated step separation
- **Origin:** roadmap doc § 4 (VS2a-gating); `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md`; `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`
- **Question (Drift-14):** Decision-framework for pool × VFX-catalogue mapping (~1.5-2 days). Drift-14 closure threshold: per-season vocabulary surface free of canonical-bias residue. Roadmap calls for legolas+gandalf+rocket; this step is autonomous.
- **Question (Drift-15):** Environment tileset catalogue sweep + VS2a pack selection — Matt verdict 2026-05-17 ("This could REALLY make the difference in the demo"). Roadmap structures it as Track A legolas (Mode B; ~5-8h) → Track B gandalf framework (~2h) → Track C **Matt selection** (~30 min) → Track D drax integration (separate dispatch). **Under autonomous operation, the Matt-selection step is held for wind-down (per pattern M2 used for R4 v0.16 + R5 v0.12).** Tracks A + B fire autonomously; Tracks C + D held.
- **Deliverables:**
  - Drift-14 design framework (gandalf authors before legolas commission)
  - Drift-15 framework (gandalf authors before legolas commission) with explicit autonomous-vs-Matt-gated step separation documented
- **Hypothesis test:** N/A (framework; not testable)
- **Effort:** 0.5-1 day gandalf
- **Activation gate:** none — gandalf fires when ready

### § 1.4 — Template-distribution repair (DEFERRED — capacity-when-available)

- **Owner:** rocket (R8 pipeline)
- **Origin:** R8 disposition § 5a
- **Priority:** LOW — `inverted_no_naming` deferred pending repair; not P0
- **Activation gate:** rocket capacity post-VS2a critical path; NOT first-fire

### § 1.5 — Spatial boss recalibration (DEFERRED — may be VS2b)

- **Owner:** gamora (sim seam)
- **Origin:** R2 H1 disposition § 3.4
- **Trigger:** if post-kit-redesign spatial boss WR remains 0.000 (currently consistent with R1 kit-broken-at-boss-tier finding)
- **Activation gate:** post-kit-redesign R2 re-run; observed as needed → may surface in VS2b

### § 1.6 — `--anchor-id` CLI flag (DEFERRED)

- **Owner:** rocket (CLI surface)
- **Origin:** R8 disposition § 5d
- **Priority:** DEFERRED for future substrate-identity controlled experiments
- **Activation gate:** ad-hoc when experimental need surfaces

---

## § 2 — Existing roadmap VS2a items (per `canonical/16-project-roadmap.md`)

### § 2.1 — F4 — B6 skill-tree UI surface decomposition (CRITICAL gap)

- **Owner:** drax (presentation seam) — drax authors decomposition dispatch
- **Origin:** roadmap § "Open design decisions / 🔴 High-impact, blocks VS2a ship"; P6 forward audit
- **Issue:** Engine emits tree data; demo has NO surface to render it. Pre-condition for B6 main work shipping in playable form.
- **Deliverables:**
  - Drax dispatch authored: rendering shape decision (vertical / horizontal / radial); node icon strategy; unlock-feedback affordance; mobile-first sizing; tap-to-allocate UX
  - Prototype surface in `reincarnated-demo` per drax-decided architecture
- **Hypothesis test:** Player can comprehend skill tree on first session without explanation (deferred to Playtest Cycle 1)
- **Effort:** drax design 1-2 days; implementation 1-2 weeks
- **Activation gate:** none — fires immediately
- **Cross-references:** roadmap § "Design watch-items (gandalf)"

### § 2.2 — S1 — Kit-redesign sprint (depends on F2)

- **Owner:** rocket (catalogue) + gandalf (design consult)
- **Origin:** R1 disposition + kit-redesign queue doc § 5.1
- **Approach:** TBD per F2 decision (hand-redesign / R8-inversion / hybrid)
- **Deliverables:**
  - Audit 51 shipped classes against criteria § 3.1-§ 3.5 (range diversity; defensive layer; burst-window architecture; archetype-description alignment; energy-cycling pattern)
  - Categorize: kit-acceptable / kit-mediocre / kit-broken (per sprint v3 telemetry)
  - Redesign per F2 path
  - Re-run R1 sprint as canonical metric
- **Hypothesis test:** 70-85% pass rate on R1 sprint against redesigned catalogue (original R1 hypothesis-test threshold met at catalogue level — per kit-redesign queue § 5.1)
- **Effort:** 4-6 weeks hand-redesign; ~2-3 weeks R8-inversion regeneration (faster but higher uncertainty)
- **Activation gate:** F2 (gandalf approach decision) + F1 (`geometry_type` schema lands)
- **Items removed from queue this session:**
  - ~~`seasonal_dominant_element` write-back gap fix~~ (rocket commit `9f6e4e6` — COMPLETE)
  - ~~R8 Test 5 multi-shot stability execution~~ (Jaccard 1.00 — COMPLETE)

### § 2.3 — S2 — B6 main work (Class kit composition + Hierarchical Skill Tree)

- **Owner:** rocket (pre-work) + gamora (main work)
- **Origin:** roadmap § VS2a + `canonical/28-engine-arpg-rebalance-design.md`
- **Status:** Pre-work dispatch authored (energy-type-aware tier assignment); main work depends on pre-work
- **Question intertwined with S1:** if F2 chooses R8-inversion path, B6 main work may shape differently (skill tree emerges from converged class composition; not authored as constraint-input)
- **Deliverables:** per existing roadmap + B6 design doc
- **Hypothesis test:** per `canonical/28` B6 criteria
- **Effort:** per roadmap
- **Activation gate:** rocket pre-work complete + F2 decision (if R8-inversion path, S1 + S2 collapse into single regeneration sprint)

### § 2.4 — S3 — Gate-3b sim MS extension (VS2a-gating)

- **Owner:** gamora (sim seam)
- **Origin:** Matt verdict reversal 2026-05-16 Day-4 close (`canonical/story/movement-speed-baseline.md` § "Verdict Reversal")
- **Status:** rocket schema-default-update pending; drax demo MS pending engine-emitted JSON consumption; star-lord export-DTO fix pending
- **Deliverables:** sim consumes the same Option-B values (player 8.0 m/s; trash 5.75; fast 7.5; AI_SPEED_MULTIPLIER 0.719) as demo; engine-emitted JSON is single source
- **Hypothesis test:** sim + demo agree on movement-speed values; engine-emitted JSON drives both
- **Effort:** per roadmap
- **Activation gate:** rocket schema-default-update + star-lord export-DTO fix complete

### § 2.5 — C1 — Movement-speed baseline (in-flight; finishing implementation)

- **Owner:** rocket + drax + gamora (cross-seam)
- **Status:** Option-B values LOCKED; per-seam implementation in progress
- **Activation gate:** in-flight; no first-fire dispatch needed (specialists continue per AGENT_STATE)

### § 2.6 — C2 — B11 GREEN-list element VFX (in-flight)

- **Owner:** drax (player-presentation) + elrond (Pimen curation)
- **Status:** Pimen ingest pipeline shipping iteratively (drax/v0.13-v0.17 series)
- **Coverage target:** 11 of 13 GREEN-list elements (per roadmap)
- **Activation gate:** in-flight; specialists continue per AGENT_STATE

### § 2.7 — C3 — Character rendering for player combatants (chierit Elementals; in-flight)

- **Owner:** drax (presentation)
- **Status:** chierit Elementals zip archives acquired; per-class character rendering in progress
- **Open question (per roadmap):** element-only mapping (Fire Knight covers fire_warrior + fire_mage) vs per-archetype with placeholders. **Gandalf decision pending (parallel to F2 / F3).**
- **Activation gate:** drax continues implementation; gandalf decision lands when ready

### § 2.8 — F5 — Legolas commission: Drift-14 pool × VFX-catalogue mapping audit

- **Owner:** legolas (Mode B catalogue crawl) — knight-rider commission per F3 framework
- **Origin:** Matt verdict 2026-05-17 ("I really don't want to ship any more canonically biased seasonal themes"); commission at `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md`
- **Effort:** ~1.5-2 days
- **Activation gate:** F3 (gandalf framework lands)
- **Cross-references:** Substrate Realignment Stage 1 per-season vocabulary surface canonical-bias gap

### § 2.9 — F6 — Legolas commission: Drift-15 environment tileset catalogue sweep

- **Owner:** legolas (Mode B catalogue crawl) — Track A only under autonomous mode
- **Origin:** Matt direct catch 2026-05-17 ("the geometrically drawn 'random seasonal structures on the ground' and the geometrically drawn walls... This could REALLY make the difference in the demo")
- **Effort:** Track A ~5-8h legolas; Track B ~2h gandalf framework (per F3)
- **Activation gate:** F3 (gandalf framework lands)
- **Matt-gated step:** Track C Matt selection (~30 min) HELD for wind-down — per pattern M2 used for R4 v0.16 + R5 v0.12
- **Cross-references:** drax Track D integration is a separate downstream dispatch (~3-5 days; fires post-Matt-selection)

### § 2.10 — L1 — Demo regen on a single season (VS2a SHIP GATE)

- **Owner:** star-lord (orchestration) + gamora (sim validation)
- **Origin:** roadmap § VS2a "Ship trigger"
- **Trigger:** single regenerated season demonstrates: updated gauntlet (B6 kits + B10 V2 sequential rooms) + new geometry palette (B11 + 11 GREEN-list element VFX) + end-game-anchored movement-speed baseline + first Pimen integration + chierit character rendering — all WITHOUT override compensation
- **Activation gate:** all of F1, F4, S1, S2, S3, C1, C2, C3, F5 land + post-pool-cull state achieved
- **Note:** Drift-15 Matt-selection step (M1) NOT a hard gate for L1; L1 can ship with environment tileset deferred to follow-on (drax can ship season regen with current tilesets; Matt-selected pack lands as a separate visual update post-wind-down)

---

## § 3 — Matt-gated items (held for wind-down)

### § 3.1 — M1 — Drift-15 Matt-selection step

- **Owner:** Matt (wind-down session)
- **Origin:** F6 Track C
- **Trigger:** Matt's eye on legolas's environment-tileset candidates; selects 3 packs
- **Fires:** post-wind-down; drax Track D integration follows

### § 3.2 — M2 — Engine-rebuild playtest tags (carryover)

- **Owner:** Matt (wind-down session)
- **Origin:** v1.0 disposition § 4
- **Tags held:** `hive-rebuild/v0.12-r5-hypothesis-test-passed`, `hive-rebuild/v0.16-r4-hypothesis-test-passed`
- **Fires:** post-wind-down; notional `hive-rebuild/v1.1-engine-rebuild-final` follows

---

## § 4 — Sequencing summary

```
Week 0 (now, 2026-05-19 ~07:05Z):
  Engine-rebuild batch CLOSED at v1.0
  VS2a kickoff (this scope-of-work + coordination matrix authored)

Week 0-1 (first-fire batch, parallel):
  F1 — geometry_type schema field (rocket + star-lord)
  F2 — gandalf Gate-1: kit-redesign approach decision
  F3 — gandalf Gate-1: Drift-14 + Drift-15 framework
  F4 — drax B6 skill-tree UI decomposition dispatch
  (C1, C2, C3, C4 — in-flight; continue per AGENT_STATE)

Week 1-2 (post-F3):
  F5 — legolas Drift-14 commission (~1.5-2 days)
  F6 — legolas Drift-15 commission Track A (~5-8h)

Week 2-6 (post-F1 + F2 + F4):
  S1 — kit-redesign sprint (4-6 wk hand-redesign OR 2-3 wk R8-inversion)
  S2 — B6 main work (shape depends on F2)
  S3 — Gate-3b sim MS extension (gamora; gated on rocket + star-lord deliverables)

Week 6-10:
  R2 re-test under explicit geometry_type (engine-rebuild fall-out validation)
  vs2a/v<X>-r2-h1-revalidated tag if H1 variance ≥ 0.10 under original threshold

Week 8-12:
  C2 — B11 GREEN-list element VFX completes (Pimen)
  C3 — chierit character rendering completes
  F6 Track D drax integration (post-Matt-selection / post-wind-down)

Week 10-14:
  L1 — Demo regen on single season → VS2a SHIPS

At Matt wind-down (whenever Matt declares):
  M1 — Drift-15 Matt-selection step
  M2 — Engine-rebuild playtest tag firings (v0.12 + v0.16) + notional v1.1
  → Engine-rebuild retrospective authored
  → VS2b begins per dispatch § 6.5 stage 2
```

---

## § 5 — Roadmap continuation (post-VS2a)

Per dispatch § 6.5 explicit ordering (unchanged from engine-rebuild flow):

### § 5.1 — Stage 2: VS2b project list

- Source: `canonical/16-project-roadmap.md` § "VS2b — Substrate Realignment + Full Catalogue"
- Begins after VS2a closed
- Knight-rider authors `scope-of-work-vs2b.md` + `coordination-matrix-vs2b.md` at VS2a completion checkpoint
- Same operating pattern

### § 5.2 — Stage 3: Stage A2 phases

- Source: `canonical/16-project-roadmap.md` § "Stage A2 closeout" + `canonical/28-engine-arpg-rebalance-design.md` queue
- Begins after VS2b closed
- B7, B12 full audit, B13 (post-narrow-slice; ~25% already shipped per Phase-1 P1), B14, B16 in flight or queued

### § 5.3 — Subsequent stages

- Playtest Cycle 1 (post-Stage-A2)
- Stage A3 (B9 series)
- Playtest Cycle 2
- Stage A4 + A5 + A6 + A7 per roadmap
- Phase 0 ship-readiness assessment at Playtest Cycle 4

---

## § 6 — Mission discipline

**Scope is fluid but bounded.** VS2a scope is **per roadmap doc + engine-rebuild fall-out items** as captured here. Scope-creep protocol:

| Pressure | Default |
|---|---|
| Kit-redesign uncovers structural catalogue issues | Surface to gandalf for design judgment; gandalf decides if VS2a-blocking or VS2b/Stage-A2 routing |
| `geometry_type` re-test still fails H1 | Surface to gandalf; may indicate catalogue diversity is binding constraint, not instrument |
| B6 skill-tree UI decomposition reveals architectural conflict | drax decides within seam; if cross-seam, surfaces to gandalf |
| New canonical-doc revisions surfaced mid-VS2a | gandalf authors mid-flight amendment per protocol § 4 routing |
| Matt returns mid-VS2a with redirection | Wind-down trigger; pause VS2a; respect direction |
| Pattern-B research arrives | FILE in PARKED thread; do NOT pull focus |
| Galadriel commission requested | Knight-rider considers; sub-agent restriction in effect; gandalf or knight-rider commissions |

**Canonical-doc revisions** (kit-redesign queue, roadmap doc, decisions-log) → gandalf authors; knight-rider broadcasts; jack-ryan reviews when affecting Disciplines or decisions-log.

---

## § 7 — Open questions for gandalf (Gate-1 dispatches; gandalf decides)

| Q | Owner | Source | Priority |
|---|---|---|---|
| Kit-redesign approach (hand vs R8-inversion vs hybrid) | gandalf | F2 dispatch | HIGH — gates S1 + S2 |
| Drift-14 design framework | gandalf | F3 dispatch | HIGH — gates F5 |
| Drift-15 design framework + autonomous-vs-Matt-gated step separation | gandalf | F3 dispatch | HIGH — gates F6 |
| chierit per-archetype mapping (element-only vs per-archetype + placeholders) | gandalf | roadmap § VS2a design watch-items | MEDIUM — gates C3 polish |
| Telegraph-art convention (primitive vs vendor-sourced) | gandalf | roadmap § VS2a design watch-items | LOW — post-VS2a (B13) |
| Embodiment-narrative display first surface | gandalf | roadmap § VS2b design watch-items | LOW — VS2b territory |

---

## § 8 — Cross-references

- v1.0 engine-rebuild closure disposition: `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md`
- R2 H1 disposition: `canonical/story/r2-h1-disposition-2026-05-19.md`
- R1 kit-redesign queue: `canonical/story/r1-kit-redesign-queue-2026-05-19.md`
- R8 disposition: `canonical/story/r8-disposition-2026-05-19.md`
- Engine-rebuild solutions doc: `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md`
- Movement-speed baseline: `canonical/story/movement-speed-baseline.md`
- Pool × VFX-catalogue mapping audit request: `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md`
- Environment tileset catalogue sweep request: `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`
- Engine-rebuild scope-of-work (predecessor): `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md`
- Roadmap: `canonical/16-project-roadmap.md` § VS2a
- B6 + B10 + B11 + B12 + B13 + B14 + B16 specs: `canonical/28-engine-arpg-rebalance-design.md`
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Decisions log: `reincarnated-engine/design/decisions/decisions-log.md`
- Operating protocol (inherited): `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 autonomous-operation + § 4.9 Matt-only-at-wind-down

---

## § 9 — Tag milestone plan (VS2a namespace)

| Tag | Trigger |
|---|---|
| `vs2a/v0.0-engine-rebuild-baseline` | At VS2a kickoff (this commit) |
| `vs2a/v0.1-geometry-type-schema-shipped` | F1 lands |
| `vs2a/v0.2-r2-h1-revalidated` | R2 re-test passes under explicit field |
| `vs2a/v0.3-drift14-framework-decided` | F3 Drift-14 framework lands |
| `vs2a/v0.4-drift15-framework-decided` | F3 Drift-15 framework lands |
| `vs2a/v0.5-kit-redesign-approach-decided` | F2 decision lands |
| `vs2a/v0.6-b6-skilltree-ui-decomposition` | F4 drax dispatch lands |
| `vs2a/v0.7-kit-redesign-sprint-complete` | S1 ships |
| `vs2a/v0.8-b6-main-work-complete` | S2 ships |
| `vs2a/v0.9-sim-ms-gate3b-complete` | S3 ships |
| `vs2a/v0.10-drift14-audit-complete` | F5 ships |
| `vs2a/v0.11-drift15-track-a-complete` | F6 Track A ships |
| `vs2a/v0.12-b11-vfx-coverage-complete` | C2 ships 11/13 elements |
| `vs2a/v0.13-chierit-rendering-complete` | C3 ships |
| `vs2a/v0.14-pimen-curation-complete` | C4 ships |
| `vs2a/v1.0-vs2a-ship` | L1 demo regen ships; VS2a CLOSED |
| `vs2a/v0.15-drift15-matt-selected` (Matt-gated) | M1 — held for wind-down |
| `vs2a/v0.16-drift15-drax-integration-complete` (post-Matt) | follow-on to M1 |

Notional `vs2a/v1.1-vs2a-validated` fires when post-VS2a playtest captures land (separate from M2 engine-rebuild playtest).

---

*Filed 2026-05-19 by knight-rider at VS2a kickoff. Engine-rebuild closed; the road continues; the player is the next gate to clear.*
