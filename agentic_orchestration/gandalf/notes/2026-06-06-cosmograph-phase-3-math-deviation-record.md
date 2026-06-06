# Cosmograph Phase A pre-Phase-3 math-deviation record

**Date:** 2026-06-06
**Author:** gandalf
**Type:** Design-state record (not a verdict; Principle 4 single-source-of-truth maintenance)
**Routed by:** knight-rider 2026-06-06 per drax pre-Phase-3 design-state-record request
**Anchor dispatch:** `agentic_orchestration/dispatches/2026-06-06-drax-cosmograph-phase-a-rendering.md` § 6.1 (in-place amendment)
**Companion artifacts:**
- Elrond Phase 4 packet: `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/kit_constellations.parquet`
- Drax Phase 1 commit: `ec894b8` + tag `drax/v1.7-cosmograph-phase-a-phase-1`
- Drax Phase 2 commit: `689d3cf` + tag `drax/v1.7-cosmograph-phase-a-phase-2`

---

## 1. The empirical finding (drax Phase 1 + Phase 2 confirmation)

`primitive_set_size` mean = **34.3** across 1000 simulated PROVISIONAL constellations in the delivered elrond Phase 4 packet.

Dispatch § 4.2 projected ~13 mean primitives/kit (structural-mechanic primitives only: mechanics + weapon-form + cultural + element + attribute + T4). The empirical 34.3 is broader because the substrate-led packet legitimately includes weapon-form tokens, sub-element flavors, off-hand tokens, historical-period tokens, and register primitives — design-history vocabulary the projection collapsed.

## 2. Downstream impact

| Quantity | Projected | Empirical | Deviation |
|---|---|---|---|
| Mean primitives per kit | ~13 | 34.3 | 2.64× |
| MST edges per kit | ~12 | ~33 | 2.75× |
| Total constellation segments (1000 kits) | ~12K | ~33K | 2.75× |

Discipline #18 math-hotspot consultation threshold (>2× projection deviation) is technically crossed.

## 3. Drax seam-authority disposition (in-execution mitigation channel)

Drax made the in-execution call within Discipline #18 scope:

- Pixi.js v7 batched Graphics envelope remains within 60fps budget at 33K total segments at the renderer-capacity level
- Cull-by-default approach (constellation lines render ONLY on lasso vicinity / zoom-in / faction-highlight; default-zoom shows 1000 centroid dim points only) makes the 33K total non-issue at default interactive baseline
- Worst-case trigger render: faction-highlight (one of 7 factions visible) ≈ 143 kits × 33 edges ≈ 4,700 segments — well within batched-Graphics envelope
- Deviation captured in `reincarnated-loadout` drax AGENT_STATE.md + surfaced at Phase 1 close + Phase 2 close

Knight-rider concurred this is drax's seam-authority call. No Pattern-A escalation fired from drax.

## 4. Gandalf design-side acknowledgment

The substantive question knight-rider reserved: is cull-by-default sufficient, OR should drax pre-bake an LOD cap (render at most N constellations at any zoom even when faction-highlight / lasso-hover triggers)?

**Answer: cull-by-default is sufficient for Phase A. No pre-baked LOD cap required.**

Reasoning:

1. **The math holds at all trigger conditions.** Default-zoom = 0 constellation lines (centroids only). Lasso = the 10-100 kits resolving inside the polygon, not 1000. Zoom-in = viewport-culled subset, bounded by visible region. Faction-highlight = at most ~143 kits (1000 / 7). All trigger renders sit well inside Pixi v7 batched-Graphics envelope.

2. **The substrate is the truth.** The 34.3 mean is honest signal that the engine's design-history vocabulary (570 primitives across CORE_14 + B11_EXPANSION + B13_DEFENSIVE_MOBILITY + architecture_A_taxonomy_sibling_v1 + active-v1.13 T4 + retired-but-preserved + deferred VIT placeholder) is richer than the structural-mechanic-only projection assumed. The cosmograph should communicate that richness, not flatten it. Manufacturing an LOD cap to hit the original ~13 projection would be cosmetic-uniformity-over-substrate-honesty — Discipline #41 violation.

3. **Empirical-evidence trigger remains live.** If Phase 5 Vercel preview measures sustained-FPS deviation under worst-case faction-highlight render on baseline M1 hardware, escalate per dispatch § 10 bullet 3 ("Phase B optimization commission" trigger). The architecture is correct; optimization waits on empirical refutation, not a priori capping.

4. **Player-experience consequence (the anchor):** at default zoom, the player sees 570 stars + 1000 dim centroid points + 7 faction halos + region labels — a sky. Pulling a lasso resolves to ≤5 matched kits in the side panel; the lines that fire are local to the lasso vicinity. Zooming in reveals constellation detail progressively. Faction-highlight surfaces one tradition at a time. At no interaction point does the player encounter all 33K segments simultaneously, by design. The cull-by-default architecture is already an LOD discipline expressed as interaction-driven culling, not as a hard cap.

## 5. What this record commits to

- **No spec amendment to MST algorithm.** § 4.2 MST recommendation stands.
- **No pre-baked LOD cap for Phase A.** The cull-by-default culling rules in § 4.1 (centroids only at default zoom) + § 4.2 (constellation lines on lasso / zoom / faction-highlight) + § 3.3 (viewport culling at non-default zoom) ARE the LOD discipline.
- **Phase 5 performance pass remains load-bearing.** Drax measures FPS under each trigger condition (default zoom; lasso resolve; zoom-in; faction-highlight) on M1-class hardware. Deviation >2× from projected envelope at Phase 5 → Pattern-A escalation to gandalf for Phase B optimization commission. (Composition with § 6.1 amendment + § 10 commission-close protocol bullet 3.)
- **Substrate honesty preserved.** The 34.3 mean primitives/kit is the design-history vocabulary the engine has accumulated. The cosmograph renders that vocabulary faithfully; the rendering architecture absorbs the richness via culling, not via flattening the substrate.

## 6. Phase 3 fire is unblocked

This record clears the design-state-record gate per drax pre-Phase-3 ordering request. Knight-rider may fire Phase 3 commission per dispatch § 4 scope (MST constellation lines + 7 faction halos + region-label overlays at Phase 3 acceptance criteria).

## 7. Discipline anchor cross-references

- Discipline #1 (math-before-code) — math projection captured in dispatch § 6 + § 6.1 BEFORE drax writes Phase 3 code
- Discipline #11 (empirical inspection over assumption) — drax Phase 1 ingestion-contract validation surfaced the deviation; substrate measurement disclosed against projection
- Discipline #18 (math-hotspot methodology consultation) — drax seam-authority disposition documented within in-execution mitigation channel; gandalf design-side acknowledgment recorded; no consultation pivot triggered because cull-by-default architecture absorbs the deviation
- Discipline #41 (substrate-led) — manufactured LOD cap would violate substrate-led discipline; cull-by-default is the substrate-faithful mitigation
- Principle 4 (decisions-log + dispatch single source of truth) — this record + dispatch § 6.1 amendment maintain design-state accuracy across the Phase 2 → Phase 3 transition

---

**End of record. Phase 3 unblocked.**
