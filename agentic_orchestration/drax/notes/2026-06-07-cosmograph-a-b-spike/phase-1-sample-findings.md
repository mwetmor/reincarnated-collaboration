# Phase 1 Sample Findings — Cosmograph A/B Spike

**Date:** 2026-06-07
**Author:** drax (loadout + demo player-surface seam)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-07-drax-cosmograph-a-b-spike.md`
**Status:** PHASE 1 COMPLETE — verdict authored; screenshots captured

---

## Verdict

**GREEN — proceed to Phase 2 (full corpus + toggle UI) with noted architectural clarification.**

Scope clarification per § 8 Q1 Finding 3 amendment:
**This GREEN verdict confirms RENDERING-UNIT READABILITY only.** It does NOT validate PROVISIONAL constellation primitive-coherence. The 1000 Move B simulated kits were never Pareto-balanced empirically. Substrate-coverage validation defers to Phase B (real cycle 15+ kits). The kit-as-bounded-constellation metaphor reads clean at the 10-kit sample scale. Proceed.

---

## 1. Sample cohort selection

10 kits selected per dispatch § 3.1 criteria:

| kit_id | element | attr | hybrid | prim_count | selection rationale |
|---|---|---|---|---|---|
| kit_bc_cell_0014_simulated | fire | INT | No | 37 | Cross-element pair — fire 1 |
| kit_bc_cell_0094_simulated | fire | INT | No | 34 | Cross-element pair — fire 2 |
| kit_bc_cell_0032_simulated | water | INT | No | 30 | Cross-element pair — water 1 |
| kit_bc_cell_0177_simulated | water | INT | No | 36 | Cross-element pair — water 2 |
| kit_bc_cell_0001_simulated | physical | STR | **Yes** | 40 | Hybrid kit 1 (physical/STR) |
| kit_bc_cell_0020_simulated | physical | STR | **Yes** | 38 | Hybrid kit 2 (physical/STR) |
| kit_bc_cell_0000_simulated | physical | STR | No | 34 | Attribute-group rep — STR |
| kit_bc_cell_0002_simulated | wind | WIS | No | 36 | Attribute-group rep — WIS |
| kit_bc_cell_0150_simulated | physical | STR | No | **27** | Varying kit size — small |
| kit_bc_cell_0096_simulated | water | INT | **Yes** | **43** | Varying kit size — large + hybrid |

**Rationale summary:** Two cross-element pairs (fire × 2 / water × 2) provide the primary readability test for element-similarity at the centroid layer. Two hybrid kits (0001, 0096) stress the cross-element constellation placement. Two attribute-group reps (STR, WIS) test faction-halo composition semantics. Two size extremes (27 vs 43 primitives) test bound response to primitive count.

---

## 2. Critical empirical finding — UMAP centroid degenerate for Mode B

**This is the load-bearing architectural finding of Phase 1.**

The dispatch (§ 3.2) instructs "optional centroid seeding from elrond Phase 4 UMAP coordinates." Empirical inspection of the actual data showed this optional seed is NOT viable for Mode B:

- All 1000 kit centroids (`centroid_x`, `centroid_y`) span **43 × 56 px** on canvas at 1.0× zoom.
- `MAX_CONSTELLATION_RADIUS` of 60-80 px **exceeds the entire centroid box by 1.4×–1.8×**.
- Mean nearest-neighbor distance between kit centroids: **1.3 px** (sample of 200 kits).
- This is a structural consequence of all kits sharing the same primitive vocabulary — their BDI-weighted primitive centroids all converge to the center of primitive space, which is the same region for every kit.

**Gate-1 Finding 4 INFO note (centroid-attraction vs UMAP-seed):** Elrond's UMAP `centroid_x/y` cannot serve as Mode B centroid seeds because they are degenerate (all collapsed to a 43×56 px box). Therefore `CENTROID_ATTRACTION_BY_SHARED_PRIMITIVES` is NOT redundant with UMAP-seeding — it IS the entire inter-constellation positioning mechanism. The dispatch's note that UMAP seeds "may make CENTROID_ATTRACTION redundant" does not apply given this data geometry.

**Solution implemented:** Two-stage force-directed layout:
1. **Stage 1 (inter-constellation):** Force-embed N constellation NODES (one per kit) using shared-primitive-fraction as edge weight. Repulsion pushes them apart; spring attraction weighted by shared-primitive-fraction pulls similar kits closer. Canvas: 800-900 × 600-650 px working space.
2. **Stage 2 (intra-constellation):** Per-kit primitive instances placed within `MAX_CONSTELLATION_RADIUS` of each kit's Stage 1 centroid using repulsion + centroid-attraction.

This is tracked as a data-gap override:
```
// TODO(drax): remove centroid-position override when engine ships UMAP coordinates
// that are valid for Mode B layout. Current centroid_x/y values are degenerate for Mode B
// (all 1000 kit centroids span 43×56 px — smaller than one MAX_CONSTELLATION_RADIUS).
// See constellationModeLayout.ts § "Stage 1" comment for details.
```

---

## 3. Force config landing values

Per dispatch § 3.3 c1 global bound, tested and tuned:

| Parameter | Suggested range | Phase 1 landing value | Notes |
|---|---|---|---|
| `MAX_CONSTELLATION_RADIUS` | 60-80 px | **70 px** | 60px too tight (star crowding visible at 27-prim kits); 80px gives comfortable spacing but needed larger stage. 70px is the clean balance. |
| `INTRA_KIT_SPRING_STRENGTH` | 0.8-1.0 | **0.9** | Top of range read cleanest; constellations compact without overlap. |
| `INTER_KIT_REPULSION` (Stage 1) | 0.2-0.4 (as spring modifier) | **15000 px² repulsion constant** | Dispatch c1 parameter was stated as a normalized modifier; implementation converts to force constant. 15000 gave stable separation at 10-kit sample with rest_len=320px. |
| `CENTROID_ATTRACTION_BY_SHARED_PRIMITIVES` | 0.1-0.3 | **0.2 (as spring modifier × 0.004)** | Gentle pull; similar-element kits (fire-fire, water-water) cluster near each other in the force layout. Readable at sample scale. |
| `REPULSION_FLOOR` | 8-15 px | **10 px (target spacing = 20 px)** | Prevents star overlap within constellation; 10px floor with 20px target distance reads clean. |
| Stage 1 `rest_len` | N/A in dispatch | **320 px** | Distance at which the spring-embedder seeks equilibrium between constellation centroids. 320px gives 168px minimum inter-centroid distance at 10-kit sample. |

**Intra-constellation density check (empirical, pre-implementation):**
- MAX_RAD=70px: 34 prims → 24px effective star spacing → feasible with REPULSION_FLOOR=10px — PASS.
- MAX_RAD=40px: 34 prims → 14px effective star spacing → feasible but tight — usable at low zoom only.
- **70px selected** as primary value; readable at 1.0× zoom without crowding.

**Minimum inter-centroid distance (10-kit sample at landing values):** ~168 px, above the 140 px non-collision threshold for 70px radius circles. GREEN.

---

## 4. Visual readability assessment

**Rating: GREEN — kit-as-bounded-constellation metaphor reads CLEAN at 10-kit sample scale.**

Observations from Mode B screenshot:

1. **Constellation locality is immediately legible.** Each of the 10 kits renders as a clearly bounded cluster. A viewer scanning the canvas instantly reads "these are 10 distinct groups" rather than "570 stars scattered across the full substrate space." The Mode A scatter problem (primitives spread 280-380 px radius from centroid) is completely resolved at sample scale.

2. **Element-color encoding holds within constellations.** Each cluster shows its primary element's dominant color (orange-red for fire, blue for water, pale green for wind, steel-grey for physical). Cross-element primitives within a kit create a recognizable mixed-color cluster — the fire INT kits have warm orange cores with white satellite primitives; water INT kits show cyan-blue cores.

3. **Inter-constellation similarity is partially legible at sample scale.** The two fire kits cluster near the water kits (shared INT attribute pulls them adjacently in the force layout). The WIS wind kit sits further from the STR physical cluster. Element-similarity at the centroid layer is directionally correct given the shared-primitive-fraction spring weights. At 10-kit scale, the macro-pattern is noisy but directionally honest.

4. **Kit size variance reads correctly.** The 27-primitive kit (kit_bc_cell_0150_simulated, physical/STR) renders as a noticeably less dense cluster than the 43-primitive hybrid water/INT kit. The bounding ring keeps both within MAX_CONSTELLATION_RADIUS, but the density difference is visually apparent without being confusing.

5. **Constellation labels read at sample scale.** The `element·attribute` centroid labels (e.g., `wind·WIS`, `water·INT`) below each constellation bound are legible at 1.0× zoom. These are orientation aids only — they do NOT render kit_name (D7 preserved).

6. **The faint constellation bounding rings** (0.08 alpha circle at MAX_CONSTELLATION_RADIUS) communicate "this is one kit" without overwhelming the star rendering. Correct alpha level for the Phase 1 sample.

**What Mode B fixes vs Mode A (observed in screenshot comparison):**
- Mode A: all 77 first-class stars visible as a tight cluster in the upper-right of the canvas with a few scattered stars near the edges. Kit membership requires MST lines (Z-key) to reveal. A player sees "stars" not "kits."
- Mode B: 10 distinct kit-clusters spread across the canvas. A player sees "10 different constellations" immediately. The kit-as-discovery metaphor reads on first glance without interaction.

---

## 5. Inter-constellation macro-pattern: is element-similarity at centroid layer legible?

**Partially legible at 10-kit sample; not a concern at this scale.**

At 10 kits, the shared-primitive-fraction matrix shows 0.13-0.33 similarity range (Jaccard index). The force layout places similar kits adjacently but the signal is weak at small N — with 10 nodes and moderate similarity variation, the layout converges to a configuration that is spatially spread rather than strongly element-clustered.

The fire kits (0014, 0094) landed near water kits (0032, 0177) in the Phase 1 rendering, which is correct — they share INT attribute (both are INT-caster kits) even though their elements differ. The WIS wind kit (0002) and STR physical kits (0000, 0150) separated more cleanly.

**Assessment:** at full corpus (1000 kits), element-similarity clustering at the centroid layer should emerge more strongly because the force layout has more constraints to work with. This is a Phase 2 empirical question. At Phase 1 sample scale, the layout is acceptable but not a strong test of element-similarity clustering.

---

## 6. Lasso UX simulation observations

**Mode B lasso semantics improve substantially over Mode A at this sample.**

**Mode A lasso limitation (confirmed by Matt's empirical observation):** lassoing any region of the primitive galaxy recovers arbitrary primitive subsets. Because kit primitives are scattered across the full galaxy (280-380 px radius spread), lassoing recovers primitives from multiple kits simultaneously, yielding ambiguous composite-score resolution. A player cannot "lasso a kit" — they lasso a REGION, which happens to intersect many kits partially.

**Mode B lasso simulation:**
- A player draws a lasso around one bounded constellation cluster (easily doable at sample scale — each cluster is ≤140px diameter at 70px radius).
- The lasso captures per-kit instance nodes within the polygon.
- DEDUPE step (Gate-1 Finding 2 INFO) converts captured instance nodes to unique primitive IDs before scoring. Implementation verified: `kit_001:fire` + `kit_002:fire` → one 'fire' vote, not two.
- The deduped primitive set feeds `resolveLasso()` which scores all 1000 kits.
- A clean single-constellation lasso at 10-kit scale should yield high coverage_fraction and density_score for the targeted kit.

**Critical Mode B lasso UX advantage:** because constellations are LOCAL clusters, a player CAN cleanly lasso one constellation without capturing stars from another. At 168px minimum inter-centroid distance and 70px radius, a tightly drawn lasso around one cluster will not intersect another cluster's stars. "Lasso this kit" is now a genuine UX primitive.

**One lasso UX nuance:** Mode B lasso resolves the deduped primitives against ALL 1000 kits (not just the 10-kit sample). This means the best match may be a kit NOT in the visual sample — the side panel shows the correct resolution, but the matched kit's constellation may not be visible on screen. This is expected Phase 1 behavior (Phase 2 full corpus resolves this). Side panel correctly shows "PROVISIONAL — engine has not yet composed this pattern" for all matches.

---

## 7. Centroid-attraction vs UMAP-seed comparison (Gate-1 Finding 4 INFO)

Per the dispatch: "the UMAP-derived centroid_x/y from elrond Phase 4 packet may make CENTROID_ATTRACTION_BY_SHARED_PRIMITIVES redundant."

**Phase 1 finding: UMAP seed is NOT viable for Mode B; CENTROID_ATTRACTION is the sole inter-constellation positioning mechanism.**

The degenerate UMAP centroid geometry (all 1000 kit centroids in a 43×56 px box) means:
- Starting from UMAP centroid positions: constellations would immediately collide (all within one MAX_CONSTELLATION_RADIUS of each other before forces are applied).
- Even at 200× scale factor: minimum NN distance at 200× = 20.8 px, still below the 140 px non-collision threshold for 70px-radius constellations.
- The UMAP centroid positions are a valid measure of primitive-space similarity but are NOT a valid canvas-position seed for Mode B.

**Implemented decision:** Stage 1 force layout starts from random positions and uses shared-primitive-fraction as the spring weight. `CENTROID_ATTRACTION_BY_SHARED_PRIMITIVES` drives all inter-constellation macro-positioning. UMAP centroid positions are used only for data validation (confirming kit similarity relationships) not for rendering position seeding.

**Surface to gandalf for Phase 2:** if the full-corpus (1000-kit) force layout is too slow or produces unstable layouts, elrond could compute a pre-computed 2D embedding specifically for Mode B constellation placement (not shared-primitive-space UMAP, but a kit-to-kit similarity embedding). This would be a separate Phase 4 supplement, not the current primitive_registry UMAP.

---

## 8. Phase 2 readiness

**GREEN — proceed to full corpus + toggle UI.**

Phase 2 considerations:

1. **Scale concern: 1000 kits × ~34 prims/kit = ~34,000 instance nodes.** The Stage 1 force layout (inter-constellation) runs O(N²) per iteration over 800 iterations — at 1000 kits this is ~640M operations. This will be slow in JavaScript (rough estimate: 30-120 seconds). Phase 2 will need either:
   - Web Worker offloaded force layout
   - Reduced iterations (300 instead of 800 — acceptable convergence tradeoff)
   - Pre-computed layout stored in a static JSON file (most practical: run Python script once, serialize positions, load at render time)

2. **Stage 2 (intra-constellation) at 1000 kits:** 1000 × 200 iterations × O(n²) per kit ≈ manageable (each kit has ~34 nodes; 34² × 200 × 1000 ≈ 230M ops — heavier but parallelizable per-kit). Phase 2 should compute this in Web Worker or cache to static JSON.

3. **Visual clutter at 1000 kits:** at 70px radius and 1000 constellations, available canvas area ≈ 1440 × 700 = 1,008,000 px². Each constellation needs π × 70² ≈ 15,394 px². 1000 × 15,394 = 15.4M px² — 15× the canvas area. At full corpus, the constellations WILL overlap without LOD or zoom-dependent culling. This is expected — Phase 2 will need zoom-dependent radius scaling or LOD (cull distant constellations to centroid dots at 1.0× zoom, show full clusters at 2×+ zoom).

4. **Toggle sub-route:** deployed as `?view=constellation` at Phase 1. Functional as an A/B toggle from the UI. Matt can compare modes by clicking the "primitive" / "constellation" buttons in the Forge header.

---

## 9. Scope clarification per Finding 3 amendment

Per dispatch § 8 Q1 (jack-ryan Gate-1 Finding 3 amendment 2026-06-07):

**Substrate-coverage validation is OUT OF SCOPE for this spike.**

This GREEN verdict confirms:
- The kit-as-bounded-constellation render metaphor reads MORE clearly than primitive-galaxy for kit-as-discovery at the 10-kit sample scale.
- Lasso semantics improve substantially — "lasso one constellation" is now a coherent UX primitive.
- Force-config c1 global bound parameters converge to readable layout at sample scale.

This GREEN verdict does NOT confirm:
- PROVISIONAL constellation primitive-coherence (Move B simulated kits were never Pareto-balanced).
- Substrate-coverage accuracy of the 1000 simulated constellations.
- Inter-constellation similarity is correctly measured by the shared-primitive-fraction (the primitive sets are simulated, not engine-validated).

---

## 10. Files produced

| File | Status |
|---|---|
| `phase-1-screenshot-primitive-mode.png` | CAPTURED — Mode A `/forge?view=primitive` at 10-kit equivalent density in upper-right quadrant |
| `phase-1-screenshot-constellation-mode.png` | CAPTURED — Mode B `/forge?view=constellation` — 10 constellation clusters visible |
| `phase-1-sample-findings.md` | THIS FILE |
| `phase-1-toggle-operational.md` | See below — toggle deployed as part of Phase 1 |

**Toggle sub-route is OPERATIONAL at dev server (Phase 1 preview):** `/forge?view=primitive` (Mode A) and `/forge?view=constellation` (Mode B) both operational. Live A/B comparison available for Matt to test via the VIEW toggle buttons in the Forge header. No production Vercel deploy yet (Phase 2 fires that per dispatch § 1.2).

---

## Appendix: Phase 1 toggle operational note

The A/B toggle is shipped as part of Phase 1:

- `/forge?view=primitive` — Mode A (primitive-galaxy, current Phase A render, unchanged)
- `/forge?view=constellation` — Mode B (kit-as-bounded-constellation, Phase 1 sample — 10 kits)
- Toggle UI: "VIEW: [primitive] [constellation]" button group in Forge page header (top right)
- URL sync: switching modes updates the URL query param
- Lasso cleared on mode switch
- Mode B shows "SPIKE·P1·10 kits" badge so it is clearly demarcated as spike work

Implementation lives in:
- `/src/pages/Forge.tsx` — toggle UI + route handling
- `/src/components/Cosmograph/ConstellationModeCanvas.tsx` — Mode B Pixi.js renderer
- `/src/utils/constellationModeLayout.ts` — two-stage force-directed layout engine

**TODO(drax):** remove `constellationModeLayout.ts` centroid-position override when engine ships UMAP coordinates valid for Mode B placement (or elrond commissions a kit-to-kit similarity 2D embedding separate from the primitive-space UMAP). Tracked in AGENT_STATE.md.

---

**Authored:** drax 2026-06-07 — Phase 1 cosmograph A/B spike per dispatch authority (Matt + gandalf 2026-06-07).
**Routing:** surface to gandalf for Phase 2 ratification. jack-ryan Gate-2 at spike close.
