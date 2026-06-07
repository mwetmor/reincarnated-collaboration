# Criterion 3.7 STRETCH — 3D Cosmograph Viability

**Verdict:** IN PROGRESS — three-tier data generated; interactive Niagara + FPS pending
**Date:** 2026-06-06 Session 1 + 2026-06-07 Session 2
**Session 2 update:**
- Three-tier star data generated (Tier 1: 100 / Tier 2: 1,000 / Tier 3: 15,000 stars)
- Niagara system architecture finalized per amended scope
- Interactive editor needed for system authoring + FPS measurement
**Amendment:** gandalf 2026-06-07 direct relay — three-tier scale progression per Phase A empirical data
**Amendment record:** `agentic_orchestration/mantis/notes/2026-06-07-amendment-criterion-37-scale-progression.md`
**Legolas FAB survey:** CONSUMED from `agentic_orchestration/legolas/research/ue-fab-cosmograph-vfx-survey-2026-06-06/short-list.md` (commit f989302)

---

## Amendment (gandalf 2026-06-07)

Original 100-star spec predates Phase A empirical data:
- Phase A: **570 primitives + 1,000 PROVISIONAL constellations** at /forge
- Drax Mode B Phase 2: **~15,000 nodes** (1,000 constellations × ~15 primitive instances)
- 100-star test: no signal about production behavior at real scale

**Three-tier scope:**
| Tier | Scale | Label | Purpose |
|---|---|---|---|
| 1 | 100 stars | BASELINE | Original spec; data point; skip if not started |
| 2 | 1,000 stars | PRODUCTION-MIN | /forge PROVISIONAL count; primary pass/fail evidence |
| 3 | 15,000 stars | PRODUCTION-ASPIRATIONAL | Mode B Phase 2 target; FPS distribution + LOD findings |

---

## Session 2 deliverables (2026-06-07)

### Three-tier star data — ALL GENERATED

Script: `agentic_orchestration/mantis/scripts/generate_cosmograph_star_data.py` (multi-tier)
Output location: `C:\dev\reincarnated-unreal\Reincarnated\Content\Data\CosmographSpike\`

| Tier | File | Stars | Edges | File size |
|---|---|---|---|---|
| 1 (BASELINE) | `cosmograph_tier1_000100stars.json` | 100 | 200 | 48 KB |
| 2 (PRODUCTION-MIN) | `cosmograph_tier2_001000stars.json` | 1,000 | 2,000 | 456 KB |
| 3 (PRODUCTION-ASPIRATIONAL) | `cosmograph_tier3_015000stars.json` | 15,000 | 15,000 | 5.9 MB |

**Tier 1 bounds:** X[-26.7, 31.6] Y[-30.8, 27.2] Z[-26.2, 31.9] UU
**Tier 2 bounds:** X[-67.3, 80.8] Y[-77.4, 68.3] Z[-67.3, 80.7] UU
**Tier 3 bounds:** X[-198.8, 238.9] Y[-228.6, 201.8] Z[-198.8, 238.9] UU

**Cluster layout (consistent across all tiers — scales proportionally):**
| Cluster | Archetype | Element | Tier1 | Tier2 | Tier3 |
|---|---|---|---|---|---|
| A | Ember | fire | 17 | 167 | 2,500 |
| B | Tide | water | 17 | 167 | 2,500 |
| C | Dusk | shadow | 17 | 167 | 2,500 |
| D | Stone | earth | 17 | 167 | 2,500 |
| E | Thunder | lightning | 16 | 166 | 2,500 |
| F | Zephyr | wind | 16 | 166 | 2,500 |

**Substrate-led discipline:** all position coordinates are deterministic archetype-cluster geometry (UMAP-analogue). No stars manufactured to fill aesthetic gaps.

### Niagara system architecture — FINALIZED (all tiers)

The same `NS_CosmographPointCloud` Niagara system handles all three tiers via User Parameter arrays. Blueprint loads the appropriate tier JSON and sets array sizes dynamically.

#### Emitter A — Star positions (N sprites, tier-dependent)

```
Module: Initialize Particle (Spawn Count = star_count from JSON)
Position source: UNiagaraDataInterfaceArrayFunctionLibrary::SetNiagaraArrayVector
  ArrayName: "StarPositions" (TArray<FVector> from JSON x/y/z)
Sprite Renderer:
  Material: M_StarSprite_Emissive (Unlit, Additive blend)
  Size: StarSizes[i] * 2.0 (Tier-dependent: T1=1.5, T4=3.0 UU)
  Color: StarColors[i] (TArray<FLinearColor> from color_hue per star)
  Brightness: StarBrightness[i] * tier_exposure_scale
```

**Niagara array size limits:** UE 5.7 Niagara supports up to ~50K particles per emitter comfortably. Tier 3 at 15K is well within this limit. Performance is the constraint, not array size.

#### Emitter B — Constellation lines (M edges, tier-dependent)

```
Module: Spawn Per Frame (edge_count from JSON)
Ribbon Renderer (straight lines — tension 1.0):
  Edge pairs: from Emitter A particle index pairs (via Particle Attribute Reader)
  Width: 0.3 UU (subtle)
  Material: M_ConstellationLine_Emissive (Unlit, Additive, thin)
  Opacity: 0.3 (foreground guide, not primary data)
```

**Edge count scaling:**
- Tier 1: 200 edges
- Tier 2: 2,000 edges
- Tier 3: 15,000 edges (capped at 1 cross-link per star to avoid edge explosion)

#### LOD architecture (Tier 3 critical)

Per gandalf amendment + drax Mode B Phase 2 LOD spec:

```
LOD Level 0 (low zoom, camera dist > 500 UU):
  → 6 centroid sprites only (1 per cluster) + 6 connecting lines
  → Niagara Scalability Group 0: Spawn Count = 6

LOD Level 1 (mid zoom, camera dist 200-500 UU):
  → Cluster-level constellation shape (30-50 representative stars per cluster)
  → Niagara Scalability Group 1: Spawn Count = 300

LOD Level 2 (high zoom, camera dist < 200 UU):
  → Full individual stars + all constellation edges
  → Niagara Scalability Group 2: Spawn Count = full tier count
```

**Implementation:** `r.Niagara.QualityLevel 0/1/2` maps to Niagara Scalability Groups. Blueprint reads camera distance → calls `SetNiagaraVariableInt("LODLevel", level)` → Niagara emitter uses conditional spawn count.

---

## 0. Context from prior research

Two legolas research deliverables inform this criterion:

1. **`2026-06-02-constellation-form-ue-techniques/synthesis.md`** — core technique:
   - Dual-renderer Niagara: Emitter A (star sprites) + Emitter B (constellation lines via Ribbon)
   - Blueprint → Niagara User Parameter binding fully supported, per-tick updatable
   - EmergenceAlpha DMI pattern for substrate→visual binding

2. **`2026-06-06/short-list.md` (legolas FAB survey)** — atmospheric assets:
   - Asset 1: Epic Niagara Examples Pack (FREE, UE 5.7) — foundation
   - Asset 2: VDB Nebula by Arghanion (FREE, 5.3+) — volumetric backdrop
   - Asset 5: LENS FLARE VFX ($29.99, UE 5.7 CONFIRMED) — per-star brightness (paid)

---

## Acceptance criteria (amended three-tier)

| Tier | Test | Target | Pass condition |
|---|---|---|---|
| 1 | PC FPS at native | >=60fps | Sustained at 100 stars + lines + nebula |
| 1 | Cosmos register | Subjective | Matt + gandalf: "does it feel like a cosmos?" |
| 2 | PC FPS at native | >=60fps | Sustained at 1,000 stars + lines + nebula |
| 2 | Mobile FPS proj. | >=30fps | 720p scalability Medium via mobile preview |
| 3 | PC FPS distribution | Record actual | Expected <60fps without LOD; report distribution |
| 3 | LOD architecture | Document | What config achieves centroid→full reveal per Mode B spec |
| All | Substrate-led | Confirmed | Positions from data, not manufactured |

---

## Niagara performance expectations

| Tier | Stars | Edges | PC FPS expected | Mobile projected | Notes |
|---|---|---|---|---|---|
| 1 | 100 | 200 | ~60fps | OK | Well within UE5.7 Niagara envelope |
| 2 | 1,000 | 2,000 | ~60fps | Borderline | Ribbon renderer scales linearly |
| 3 | 15,000 | 15,000 | ~20-40fps (no LOD) | Not viable (no LOD) | LOD required for 60fps |

**LOD architecture** (Tier 3 without LOD likely ~20-40fps on PC; with LOD Level 0 → ~60fps):
- No LOD: 15K sprites + 15K ribbon segments; GPU-bound on particle render
- LOD 0 (6 centroids): ~60fps → cosmograph viable at overview zoom
- LOD 1 (300 stars): ~60fps → viable at mid zoom  
- LOD 2 (15K): ~20-40fps → detail zoom (acceptable at hover/inspect, not constant)

---

## Asset acquisition (Session 2 status)

### Free-path (no Matt auth needed)
- [ ] Asset 1 — Epic Niagara Examples Pack: add via Epic Launcher
- [ ] Asset 2 — VDB Nebula: add from FAB (free)

### Paid-path (pending Matt auth)
- [ ] Asset 5 — LENS FLARE VFX ($29.99, UE 5.7 CONFIRMED)

---

## Interactive session plan (next session — ~3-5 hours per amendment)

1. Install Assets 1+2 (free) via Epic Launcher — ~15 min
2. Create level `TestCosmograph_Spike_37` — ~10 min
3. Author `NS_CosmographPointCloud` Niagara system (Emitters A+B + LOD scalability groups) — ~90 min
4. Author `M_StarSprite_Emissive` + `M_ConstellationLine_Emissive` — ~20 min
5. Author `BP_CosmographTest` (JSON ingestion + tier selection + Niagara binding) — ~30 min
6. Place Heterogeneous Volumes actor (VDB nebula) — ~15 min
7. Run each tier in PIE:
   - Tier 1 (100): `stat unit` FPS → screenshot cosmos register
   - Tier 2 (1,000): `stat unit` FPS → screenshot → mobile preview FPS
   - Tier 3 (15,000): `stat unit` FPS at each LOD level → screenshot
8. Document FPS distribution per tier per LOD
9. Screenshot 3 tiers for gandalf cosmos register review
10. Total estimate: ~3.5-5 hours

---

*Criterion 3.7 status: IN PROGRESS — three-tier data generated (Session 2 empirical). LOD architecture designed. Interactive session needed: Niagara authoring + FPS measurement at Tier 1/2/3.*
*Substrate-led discipline: CONFIRMED at data layer. Visual confirmation pending.*
*Amendment source: gandalf 2026-06-07 direct relay — see amendment record.*
