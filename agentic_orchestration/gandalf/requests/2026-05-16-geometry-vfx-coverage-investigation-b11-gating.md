# Request to knight-rider — Geometry × Element VFX coverage investigation (B11 gating)

**From:** gandalf
**To:** knight-rider (to author dispatches per ADR-002)
**Date:** 2026-05-16 (Day 4)
**Status:** **MATT-APPROVED 2026-05-16.** Matt's directive: *"yes, block B11 on this."* B11 demo integration phase is gated on the geometry × element coverage assessment landing. Engine + sim phases of B11 may proceed in parallel; drax integration phase is the blocked step.
**Priority:** **HIGH — B11 SHIP GATE (and therefore VS2a SHIP GATE).** Surfaced by Matt 2026-05-16 directly after movement-speed-baseline lock. Catch: the substrate-realignment work has scoped element + embodiment mapping to the catalogue, but **the geometry dimension of skills has not been investigated against vendor coverage at all.** B11 ships 9 new geometries (16 → 25 active types) + B13 ships 5 more (→ 30) — if vendor VFX libraries don't ship usable assets for those geometric shapes, B11 demo integration is blocked or forced into placeholder/composite fallbacks that degrade the showcase.
**Type:** Cross-seam commission — Legolas crawl amendment + Elrond rubric + gandalf gap-severity assessment.

---

## The catch — what's missing

The catalogue work to date has captured:
- **Element/substrate** (fire, water, earth, dark, void, necrotic, crystal, etc.) — Step B Tier-1 crawl in flight
- **Embodiment-axis** (warrior/mage/rogue/hunter narrative skin) — VS2b Substrate Realignment work
- **Sub-register** (HD-2D-shaped pixel-art / retro-pixel / vector / etc.) — `style-register.md` filter
- **Canvas info** (resolution_band, sprite layout, animations_count) — Pimen JSONL schema captures partially

**The catalogue does NOT capture:**
- **Geometry signature** — is this an `impact_burst`, a `projectile_straight`, a `beam`, a `cone`, a `ground_slam`, an `aura`, a `nova`, a `chain`, a `ring`?
- **Shape class** — point / radial / directional / persistent / sustained?
- **Motion signature** — static / linear / arcing / homing / oscillating / radial-expanding?
- **Screen coverage pattern** — small_point / medium_radial / large_aoe / full_screen?
- **Composition viability** — single-effect-complete vs requires-loop vs requires-overlay vs requires-base-plus-impact?

Per the Pimen JSONL schema inspection (`research/catalogue/pimen/full-2026-05-16.jsonl`), `extraction_notes` carries narrative descriptions like *"Firebolt: 4 loopable + 6 impact"* or *"Fire breath: 3 startup + 4 repeatable + 7 ending"* — these *implicitly* describe geometries (`Firebolt` ≈ projectile_straight; `Fire breath` ≈ cone) but the geometry classification has never been extracted into a structured field.

**B11 (per `canonical/16-project-roadmap.md` § B11; ~3-4 weeks engine + demo; VS2a-gating) ships 9 new geometries:**
- `ring` (donut AOE — caster-centered or ground-targeted; per `canonical/09-geometry-palette-discussion.md` line 182)
- 8 additional AOE-coded geometries (motion-AOEs: whirlwind, dash_attack, leap_strike per file 09 line 244; plus others to be specified by rocket B11 dispatch)

**Plus parameter expansions** that change which existing vendor assets fit which generated skill:
- `collision_mode` (pass-through / first-hit / multi-hit)
- `angle_distribution` (radial / directional / sweeping)
- `sweep_shape` (linear / arcing / spiral)
- `damage_falloff` (uniform / linear / exponential)

**B13 adds 5 more defensive mobility geometries** (~25 → 30 active; per `canonical/09-geometry-palette-discussion.md` § "Revision 2026-05-11 (B13 extension)"). Deferred from VS2a per current roadmap but worth being in the geometry coverage analysis for forward-compatibility.

## The blocker structure

For each geometry × element cell in the matrix, B11 integration requires:

1. Engine generates a skill with that geometry + element (rocket/gamora — already in scope)
2. Sim handles the geometry (gamora — already in scope)
3. Demo renders the geometry (drax — VS2a scope)
4. **A vendor VFX asset exists that fits the geometry + element combination** (catalogue — THE GAP)

If a vendor ships 15 "Fire" packs but they're all impact_bursts and one chain_lightning, then a `ring_fire` skill has no asset. Drax's options at integration time become:

- **Composite from existing** — place a circular impact_burst in a ring formation. Looks janky. Not Court-tier.
- **Hand-author** — ~3-5 days per geometry × element cell. For 25 geometries × 9 elements = 225 cells (many redundant; realistic gap surface ~30-60 cells), this is months of art work the project doesn't have.
- **Ship placeholder** — generic visual that doesn't match the element register. Kills the showcase value of VS2a.
- **Defer the affected geometries** — changes B11 scope mid-flight. Last-resort.

**This must be known BEFORE drax begins B11 demo integration** so the choice is design-track, not crisis-track.

---

## What knight-rider needs to do

### Track 1 — Amend Step B Tier-1 dispatch (NOW; before Legolas un-holds it)

**Current Step B dispatch:** `agentic_orchestration/dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md`

**Add to "Output format" — Per-pack JSONL row:**

> **Geometry-signature extraction (NEW per geometry-coverage investigation 2026-05-16):** for each pack, extract a `geometry_signatures` array — list of geometry classifications evident in the pack's animations. Use the geometry vocabulary from `canonical/09-geometry-palette-discussion.md` (current 16 + B11's 9 + B13's 5 = 30 target types). For each animation in the pack, classify as: `impact_burst`, `projectile_straight`, `projectile_arcing`, `projectile_homing`, `beam_channel`, `cone`, `ground_slam_circular`, `ground_slam_directional`, `aura_radial`, `aura_directional`, `nova_radial`, `nova_wave`, `chain`, `ring`, `whirlwind`, `dash_attack`, `leap_strike`, `vortex_pull`, `summon`, `buff_self`, `debuff_target`, `melee_strike`, `melee_arc`, etc. Where unclear, tag `geometry_uncertain` with notes.

**Add to "Per-vendor crawl methodology" — Step B.2 enhancement:**

> Geometry-classification pass runs in parallel with substrate-tag extraction. Each animation gets a geometry signature; per-pack `geometry_coverage` summary lists distinct signatures present. Cross-vendor inventory adds geometry-axis coverage matrix alongside the substrate-axis coverage matrix.

**Rationale:** geometry-coverage is upstream of B11 demo integration; extracting at crawl time costs ~10–15% additional Legolas effort (estimated +1-2h per vendor); extracting post-hoc requires re-crawling. Same Mode B session that does substrate extraction does geometry extraction.

**Estimated extra Legolas lift:** ~15% over existing Step B estimate (2-4 sessions → 2.5-4.5 sessions). Marginal.

### Track 2 — Re-crawl Pimen with geometry signatures (NOW; parallel to Step B Tier-1)

Pimen full crawl already landed at `research/catalogue/pimen/full-2026-05-16.jsonl` without geometry signatures. Recommend a focused re-pass:

**Author Legolas dispatch:** Pimen re-crawl pass focused exclusively on `geometry_signatures` extraction per the Step B amendment vocabulary above. Existing JSONL stays; add a sidecar file `research/catalogue/pimen/geometry-signatures-2026-05-XX.jsonl` keyed by `asset_id` with geometry classifications.

**Estimated lift:** ~1 Legolas Mode B session (~2-4h). Pimen's catalogue is already inspected; the geometry pass is annotation, not re-discovery.

### Track 3 — Author Elrond rubric for geometry-coverage matrix

**Author Elrond dispatch:** rubric design for the geometry × element coverage matrix.

**Scope:**
- **Demand side:** the locked geometry palette (B11 target 25 types + B13 target 30 types) × the elemental substrate vocabulary (currently canonical-four + per-season vocabulary; per form-bias-cadence-strategy doc this expands post-cipher-width)
- **Supply side:** vendor JSONL `geometry_signatures` × `pimen_element` / equivalent per-vendor element fields
- **Matrix output:** per geometry × element cell, list of vendors-with-coverage; total asset count; quality flag (per-vendor Pimen-tier-grade vs sub-tier)
- **Gap identification:** cells with zero vendor coverage (CRITICAL); cells with single-vendor coverage (SINGLE-POINT-OF-FAILURE); cells with multi-vendor coverage (HEALTHY)
- **Per-cell severity scoring:** weighted by (a) geometry usage frequency in B11+B13 generator (per file 09 quotas / per-class kit composition stats from B6); (b) element prevalence (canonical-four high; per-season vocabulary lower-weight but still required)
- **Output doc:** `research/curated/geometry-element-coverage-matrix-2026-05-XX.md` consumed by gandalf for gap-severity assessment

**Estimated lift:** ~1-2 Elrond sessions (~4-8h). Consumes Legolas geometry signatures + applies rubric.

### Track 4 — Gandalf gap-severity assessment (after Elrond rubric output)

I take the matrix output and assess severity per cell:

- **CRITICAL gaps** (must be addressed before B11 ship) — e.g., `projectile_fire` is core; if no vendor ships it usably, B11 cannot ship fire-mage classes
- **TOLERABLE gaps** (compositing or geometry-substitution acceptable) — e.g., `aura_dark` may be addressable via Pimen's Buff/Debuff + Dark elemental overlay composite
- **DEFER gaps** (geometry × element combination is rare; can defer to post-VS2a) — e.g., `chain_holy` for a holy-mage-controller class that doesn't appear in any current generated season

For CRITICAL gaps, surface options:
- **Option A:** commission additional vendor research (Legolas Mode A sweep for vendors specializing in the missing geometry)
- **Option B:** request hand-author scope addition (Matt + Drax decision)
- **Option C:** revise B11 geometry palette to drop the gap-affected geometry (last-resort; affects B11 deliverable)
- **Option D:** accept composite fallback with drax sign-off on quality

**Output doc:** `canonical/story/geometry-vfx-coverage-assessment.md` — authoritative gap-severity + recommendations to Matt.

**Estimated lift:** ~2-3h gandalf. Sequenced after Elrond rubric returns.

### Track 5 — Sequencing relative to B11

**Critical path:**

```
Step B Tier-1 dispatch amendment (Track 1)
    │
    ▼
Step B Tier-1 crawl runs (Legolas) ──→ Pimen re-crawl runs in parallel (Track 2)
    │                                       │
    └────────────┬──────────────────────────┘
                 ▼
         Geometry signatures + substrate signatures both in cross-vendor inventory
                 │
                 ▼
         Elrond geometry-coverage rubric output (Track 3)
                 │
                 ▼
         Gandalf gap-severity assessment (Track 4)
                 │
                 ▼
         B11 demo integration unblocked OR scope-revision options surfaced to Matt
```

**B11 dispatch (rocket + gamora + drax)** must NOT begin demo integration phase until Track 4 closes. Engine + sim portions of B11 can begin in parallel (geometry generation + sim handling are upstream of asset integration); the drax demo integration phase is the gated step.

**Estimated total elapsed time:** ~2-3 weeks from Step B start to gandalf assessment landing. Fits within current B11 estimated 3-4 week window if Step B starts immediately (Step B is currently un-held per `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md` PASS-WITH-AMENDMENTS verdict; just needs knight-rider to integrate the C.1-C.3 amendments and notify Legolas).

### Track 6 — Brief Matt on gap-severity outcomes (when Track 4 lands)

After gap-severity assessment lands, single brief to Matt covering:
- How many CRITICAL gaps surfaced
- Per-gap recommended option (A/B/C/D from Track 4)
- Combined scope/timeline impact

If zero CRITICAL gaps, brief is informational only; B11 unblocks cleanly.

If CRITICAL gaps surface, Matt picks per-gap from options A/B/C/D; commission cascades.

---

## What this commission does NOT do

- Does not commission art creation — only investigates whether art exists
- Does not amend B11 scope unilaterally — surfaces options; Matt decides
- Does not affect Step B Tier-1 vendor list (already locked at 9-10 vendors per gate-3 review) — only amends the per-pack data extraction
- Does not require new Legolas vendor discovery — works against the already-finalized Tier-1 list
- Does not affect element/substrate-mapping work — orthogonal axis

## Cross-references

- **Geometry palette canonical:** `canonical/09-geometry-palette-discussion.md` (16 active + B11's 9 + B13's 5; vocabulary)
- **B11 scope:** `canonical/16-project-roadmap.md` § B11 + § VS2a
- **B13 scope:** `canonical/16-project-roadmap.md` § B13
- **Step B Tier-1 dispatch (to be amended):** `agentic_orchestration/dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md`
- **Step B gate-3 review (predecessor):** `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md`
- **Pimen crawl output (to be re-passed):** `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl`
- **Pimen sample review:** `agentic_orchestration/qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md` (implicit geometry classification in `extraction_notes`)
- **Form-bias context:** `canonical/story/form-bias-cadence-strategy.md` § 5.3 + § 6.1 — substrate vs vocabulary layer model; this commission identifies a *third* axis (geometry) that the model implicitly assumes but never explicitly catalogues

## Why this surfaces now and not earlier

The substrate-realignment / form-bias work has been organized around two axes: element/substrate (what fire looks like; what void looks like) and embodiment (what warrior-form looks like; what mage-form looks like). The geometry axis is the third dimension of skill VFX that the engine generates against (`projectile of fire`; `ground_slam of earth`; `beam of holy`) — orthogonal to both other axes.

It surfaces now (not earlier) because:
1. B11 is the first major palette expansion that introduces geometries beyond the engine's bootstrap-era set; until B11, the existing palette was small enough that vendor coverage was implicit and verifiable by eye
2. The Step B Tier-1 crawl is the first systematic catalogue work; this is the natural moment to add the geometry axis before the crawl runs vs after
3. Matt's direct catch in 2026-05-16 dialogue surfaced the gap as a likely B11 blocker

Closing it now costs ~15% added Legolas effort + ~1-2 Elrond sessions + ~3h gandalf. Closing it later (post-Step-B, post-Pimen, mid-B11-integration) costs a full additional crawl pass + drax integration crisis + potential B11 scope revision.

---

— gandalf, 2026-05-16 (Day 4)
