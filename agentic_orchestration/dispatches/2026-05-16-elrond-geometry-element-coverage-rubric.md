# Dispatch — 2026-05-16 — elrond — Geometry × element coverage matrix rubric (per gandalf geometry-coverage commission Track 3)

**From:** knight-rider (authored per gandalf 2026-05-16 geometry-VFX-coverage-investigation commission `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` Track 3)
**To:** elrond
**Approved by:** Matt at 2026-05-16 Day 4 explicit batch directive ("author geometry dispatches")
**Status:** PENDING — ACTIVE (legolas geometry-signature re-pass completed 2026-05-16 Day 4; 100 packs classified across 9 vendor sidecar files at `agentic_orchestration/research/catalogue/<vendor>/geometry-signatures-2026-05-16.jsonl`; this dispatch unblocked).
**Estimated effort:** ~1-2 sessions (~4-8h per gandalf commission); rubric design + execution.
**Acceptance:** Geometry × element coverage matrix authored at `agentic_orchestration/research/curated/geometry-element-coverage-matrix-2026-05-16.md`. Per-cell vendor coverage classified CRITICAL (zero vendors) / SINGLE-POINT-OF-FAILURE (one vendor) / HEALTHY (multi-vendor). Gandalf consumes for Track 4 gap-severity assessment.

---

## Context — what this dispatch does

Per gandalf's 2026-05-16 geometry-VFX-coverage-investigation commission Track 3 — and following the legolas geometry-signature re-pass (Tracks 1+2 consolidated; dispatch at `dispatches/2026-05-16-legolas-geometry-signature-re-pass.md`):

Once legolas's per-vendor sidecar files exist (containing `geometry_signatures: [...]` arrays per pack), this dispatch builds the **geometry × element coverage matrix** that gandalf's Track 4 gap-severity assessment operates against.

**The matrix structure:**

Rows: geometry types (30 from `canonical/09-geometry-palette-discussion.md`: current 16 + B11's 9 + B13's 5)
Columns: element / substrate tags (Pimen's 9 + the cipher-width-locked classical-element set + any per-vendor element-equivalent fields)

Per cell `(geometry_i, element_j)`: count of vendors supplying packs whose geometry_signatures include `geometry_i` AND whose substrate-tag includes `element_j`. Classify per gandalf:

- **CRITICAL** (zero vendor coverage) — must be addressed before B11 ship; e.g., `projectile_fire` is core to fire-mage classes; if no vendor ships it usably, B11 cannot ship fire-mage classes
- **SINGLE-POINT-OF-FAILURE** (one vendor coverage) — acquisition risk; if that vendor unavailable, gap reverts to CRITICAL
- **HEALTHY** (multi-vendor coverage) — safe; alternative sources available

## What this dispatch produces

Single document at `agentic_orchestration/research/curated/geometry-element-coverage-matrix-2026-05-16.md`.

Structure:

### Section 1 — Rubric design

Document the rubric you apply:
- Supply-side input: per-vendor sidecar JSONLs (legolas Track 1+2 output) + per-vendor JSONLs' element/mechanic fields
- Element vocabulary: which element-axis values are matrix columns? (Pimen's 9 substrate tags is the baseline; cross-vendor `vendor_mechanic_tags` from Step B amendment C.1 may expand the column set)
- Geometry vocabulary: 30-target list from `canonical/09-geometry-palette-discussion.md` (current 16 + B11's 9 + B13's 5)
- Cell classification thresholds: zero / one / multi-vendor per gandalf
- Edge-case handling: `geometry_uncertain` tagged packs (do they count toward coverage? how?); packs with no element-tag (e.g., kinetic-only); packs spanning multiple elements

### Section 2 — Per-cell coverage matrix

Present as a 30 × N table (where N = element-vocabulary count; likely 10-15 elements per the post-Step-B substrate):

| | fire | water | earth | wind | ice | holy | dark | thunder | acid | (other) |
|---|---|---|---|---|---|---|---|---|---|---|
| impact_burst | (vendor count) | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| projectile_straight | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

Classify each cell per the rubric (CRITICAL / SPF / HEALTHY); use color/symbol convention if possible (e.g., 🔴 CRITICAL / 🟡 SPF / 🟢 HEALTHY).

### Section 3 — Per-element gap summary

Per element column: how many CRITICAL cells; how many SPF cells; observation on element coverage breadth.

### Section 4 — Per-geometry gap summary

Per geometry row: how many CRITICAL element-pairings; how many SPF element-pairings; observation on geometry coverage breadth.

### Section 5 — CRITICAL gap enumeration (the load-bearing output for gandalf Track 4)

Enumerate explicitly:
- Every `(geometry, element)` cell classified CRITICAL
- Brief context per gap: which classes / kits / scenarios depend on this cell?
- Recommendation for prioritization (e.g., "fire impact_burst is foundational to fire-mage primary attacks; high priority")

### Section 6 — SINGLE-POINT-OF-FAILURE gap enumeration

Enumerate cells with single-vendor coverage:
- Vendor name + their pack(s) covering the cell
- Acquisition-risk note (e.g., "Pixogen license-unverified per Step B C.2 flag — Pixogen-covered cells have higher SPF risk")

### Section 7 — Recommendation summary for gandalf

Concise summary for gandalf's Track 4 gap-severity assessment:
- Total CRITICAL cells (by count + per-element / per-geometry breakdown)
- Total SPF cells
- HEALTHY-vs-non-HEALTHY ratio
- Any methodology flags surfaced (e.g., elements that don't fit cleanly; geometries that overlap; rubric-extension recommendations)

## Cross-seam considerations

- **Legolas:** READ-ONLY consumer of legolas's sidecar JSONLs from the parallel dispatch. Your output depends on legolas's completion; per HELD-on-prior framing, your dispatch fires after legolas completes.
- **Gandalf:** primary downstream consumer of your matrix output. Gandalf's Track 4 gap-severity assessment operates on your Section 5 + Section 7 outputs.
- **Knight-rider:** notify at completion; gandalf assessment fires post-your-completion.
- **Rocket / gamora:** READ-ONLY; their B11 engine + sim phases proceed in parallel without dependency on this dispatch.
- **Drax:** their B11 demo integration is HELD pending gandalf's Track 4 assessment (which depends on YOUR rubric output).

## Out of scope (explicit)

- **NO new vendor crawls.** Operates on legolas's sidecar JSONLs + existing per-vendor catalogues only.
- **NO gap-severity assessment.** That's gandalf's Track 4 deliverable. Your output is the matrix + enumeration; gandalf does the prioritization + recommendation per CRITICAL gap.
- **NO B11 dispatch authoring** or roadmap amendments.
- **NO recommendations on additional vendor sweeps** beyond surfacing SPF risk in Section 6 + CRITICAL gap enumeration in Section 5. (Track 4 gandalf surfaces per-gap mitigation options A-D per the commission.)
- **NO geometry-vocabulary or element-vocabulary extensions** beyond what legolas's sidecars + existing catalogues support. If gaps in the vocabulary surface, flag in Section 7 as rubric-extension recommendations; do NOT extend without gandalf input.
- **NO modifications to legolas's sidecar files or existing per-vendor JSONLs.** Read-only.

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` (the commission; Track 3 your scope)
- `agentic_orchestration/dispatches/2026-05-16-legolas-geometry-signature-re-pass.md` (upstream dispatch; your input substrate is its output)
- Per-vendor sidecars at `agentic_orchestration/research/catalogue/<vendor>/geometry-signatures-2026-05-16.jsonl` (legolas's output; your primary input)
- `canonical/09-geometry-palette-discussion.md` (geometry vocabulary source-of-truth)
- `canonical/story/drift-audit.md` Drift-11 entry (gandalf filed; pattern context)
- 9 vendor catalogues at `agentic_orchestration/research/catalogue/<vendor>/full-2026-05-16.jsonl` (element/mechanic fields are matrix-column inputs)
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (cross-vendor substrate; informs element-vocabulary for matrix columns)
- Your own Step A methodology smoke test (`agentic_orchestration/qa/findings/2026-05-16-elrond-step-a-methodology-smoke-test.md`) — methodology baseline
- Your own emergent-grouping analysis (inline in 2026-05-16 agent return) — substrate context

## Acceptance criteria

- [ ] Section 1 (rubric design) documented
- [ ] Section 2 (per-cell coverage matrix) complete; 30 × N table classified per cell
- [ ] Section 3 (per-element gap summary) complete
- [ ] Section 4 (per-geometry gap summary) complete
- [ ] Section 5 (CRITICAL gap enumeration) — load-bearing for gandalf Track 4; explicit per-cell context + prioritization recommendation
- [ ] Section 6 (SPF gap enumeration) — vendor + acquisition-risk notes per cell
- [ ] Section 7 (recommendation summary for gandalf) — concise; ready for Track 4 consumption
- [ ] Matrix filed at `agentic_orchestration/research/curated/geometry-element-coverage-matrix-2026-05-16.md`
- [ ] Knight-rider notified at completion; gandalf Track 4 fires next

## Tag policy

No tag (analytical/research output; not a code change).

---

## Completion record

**Completed:** 2026-05-16 (this session)
**Matrix path:** `agentic_orchestration/research/curated/geometry-element-coverage-matrix-2026-05-16.md` (664 lines)
**CRITICAL cell count:** 280 of 420 (67%)
**SPF cell count:** 73 of 420 (17%)
**HEALTHY cell count:** 67 of 420 (16%)
**Methodology flags surfaced:** 8 (per matrix Section 7.5)

1. `projectile_homing` and `aura_directional` likely vocabulary-collapse candidates (zero attestations across 100 packs; either visually-indistinguishable from sibling types or behavior-distinctions invisible in static VFX)
2. `melee_cleave` likely redundant with `melee_arc` (all "cleave" candidates classified as melee_arc by legolas)
3. B13 defensive-mobility geometries (`roll`, `parry_active`, `block_active`, `iframe_dash`) categorically uncovered because the 9 surveyed vendors are VFX-pack vendors, not character-animation vendors (Mixamo-class) — distinct vendor crawl scope recommended for B13 mobility VFX
4. Status and void columns are structurally narrow (status by structure; void by Pixogen license-dependency)
5. Acid is the most fragile classical element (all 6 covered cells are Pimen-SPF; zero HEALTHY cells)
6. Coverage matrix understates kinetic-melee coverage — element-bound melee is mostly SPF (class-archetype-bound), but kinetic-column melee is HEALTHY at 4 vendors
7. Mega-pack contributions inflate Pimen's apparent coverage by ~10-15 cells
8. ~30-40% of pack rows carry `geometry_uncertain` tags — high-confidence-only re-run would drop HEALTHY count by ~15-20%

**Notes for knight-rider:**

- Track 3 complete; gandalf Track 4 gap-severity assessment can now fire.
- Tier F geometries (Section 7.4) are the most urgent attention items — 7 always-CRITICAL geometries: leap_strike, roll, parry_active, block_active (effectively), iframe_dash, melee_cleave, projectile_homing, aura_directional.
- Pixogen license verification is the single highest-leverage decision affecting matrix health (void-column collapse risk if license fails).
- Per-element priority order in Section 7.3 — acid (0 HEALTHY) and void (1 HEALTHY, Pixogen-conditional) are the weakest classical/cross-cutting columns.
- Per-pack evidence preserved upstream in the 9 vendor sidecars and cross-vendor substrate inventory — this matrix is a roll-up.
- 4 rubric-extension recommendations parked in Section 7.6 (confidence-weighting, per-archetype rubric, multi-pack-kit rubric, license-stratified rubric, pack-format compatibility rubric) — none implemented; await gandalf direction.
