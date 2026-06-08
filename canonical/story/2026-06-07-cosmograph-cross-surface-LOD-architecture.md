# Cosmograph Cross-Surface LOD Architecture — Lock

**STATUS:** CURRENT (load-bearing architectural commitment from 2026-06-07 forward)
**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward)
**Authority:** gandalf cross-cutting design authority composing drax /forge Phase 2 (Gate-2 PASS-with-INFO `cb2d60d`) + mantis spike Session 3 (port-workstream-gating-verdict spike-overall GREEN `c169515`)
**Type:** load-bearing cross-surface architectural commitment — locks centroid-first LOD vocabulary across both cosmograph surfaces (drax /forge 2D web + mantis UE 3D production)
**Companion docs:**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (LOD architecture is what makes spherical-shell + 1000+ corpus tractable at production scale)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 (primitive-as-star + kit-as-constellation substrate lock; LOD operates over this)
- `canonical/story/2026-06-06-cosmograph-phase-a-creation-moment-wave-close.md` § 7 (drax /forge Phase A foundation)
- `agentic_orchestration/qa/findings/2026-06-07-drax-cosmograph-a-b-spike-gate-2.md` (drax Phase 2 LOD operational at `/forge`)
- `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/port-workstream-gating-verdict.md` § "Architectural surfaces for gandalf review" #1 (cross-surface LOD vocabulary alignment surfaced for lock)

---

## 0. TL;DR

Both cosmograph surfaces — drax 2D `/forge` web + mantis 3D UE production — independently arrived at **centroid-first LOD vocabulary** through empirical perf + UX validation. This doc LOCKS that vocabulary cross-surface as a single coherent architectural commitment. Player experience is consistent across both surfaces: zoomed-out view shows constellation-centroid markers; zoomed-in view reveals per-primitive-star detail. Same mental model; different rendering targets.

**Three-level LOD vocabulary LOCKED across both surfaces:**

- **Level 0 (zoomed-out / overview):** macro centroids visible. Drax 2D: constellation-centroid dots at 1.0× zoom. Mantis UE 3D: 6 mechanic-family centroids OR faction halos at default sphere-overview distance.
- **Level 1 (mid zoom):** constellation-level structure visible. Drax 2D: bounded cluster outlines + constellation centroids at ~1.5-2.0× zoom. Mantis UE 3D: ~300-500 constellation-centroid markers + faction halo overlays.
- **Level 2 (drilled-in):** per-primitive detail. Drax 2D: full per-primitive star reveal within constellations at ≥2.0× zoom. Mantis UE 3D: full N primitive-stars visible within lassoed/hovered/proximate region.

LOD transitions are **smooth + continuous** (not snap-toggles). Player's zoom action progressively reveals detail without modal mode-switches.

---

## 1. Why cross-surface lock matters

### 1.1 Same substrate, different render targets

Both surfaces consume the same substrate (atomic-substrate-registry primitives + hypothesis-flow constellations + cosmograph-pivot kit-as-constellation lock). Both implement the kit-as-discovery metaphor. Both serve player exploration of substrate space. They differ in rendering technology + dimensionality + player context:

- **drax /forge 2D:** functional substrate-exploration surface; substrate analysis + lasso lookup; lives in browser; player accesses outside creation moment for form-swaps + browsing
- **mantis UE 3D:** aesthetic-immersive creation moment surface; spherical shell + 3D nebula context; lives in UE game; player encounters at first creation moment + reincarnation events

If the LOD vocabularies diverge between surfaces, player learns two mental models for the same conceptual interaction. Confusing + inelegant. **Cross-surface lock prevents drift.**

### 1.2 Both surfaces independently chose centroid-first

This is the key empirical signal that validates the lock: drax and mantis arrived at centroid-first LOD independently through different drivers.

**Drax /forge Phase 2 (live in production):**
- Driver: visual-readability + perf at 1000-constellation × 15-primitive corpus (~15K nodes)
- Solution: centroid dots at default zoom; constellation-bound reveal at zoom ≥2.0×
- Empirical validation: 60 FPS both modes at full corpus per jack-ryan Gate-2 PASS-with-INFO
- Reference: `compute-constellation-layout.py` LOD threshold logic

**Mantis UE 3D Session 3 (spike-overall GREEN):**
- Driver: Niagara perf at 15K sprites in 3D Tier 3 testing
- Solution: Level 0 = 6 centroids (mechanic-family); Level 1 = 300 (mid-density); Level 2 = full N
- Empirical validation: spike-overall verdict GREEN per port-workstream-gating-verdict
- Reference: NS_CosmographPointCloud + LOD architecture documented in criterion-3-7-stretch findings

**Convergence is substrate-led** — both surfaces faced the same fundamental constraint (~15K nodes is the realistic production scale; rendering all at once is wasteful + visually noisy) and arrived at the same architectural solution. That's the strongest validation we get short of playtest. Lock now; refine later if playtest evidence emerges.

---

## 2. The architecture

### 2.1 Three-level LOD vocabulary

**Level 0 — Macro overview (default zoom):**

Player sees the most condensed compositional structure. Goal: gestalt + macro pattern signal.

- **What renders:** mechanic-family centroids (6 per Phase A clustering) OR faction overlays (7 attribute-group halos per Phase A) OR small set of representative constellation-centroid markers
- **Spatial intent:** player can see "fire region" vs "shadow region" vs "physical region" at a glance; element-tinting + faction-halo color encoding dominant
- **Cognitive load:** minimal — small N visible objects; player orients themselves in the substrate landscape
- **Interaction:** click-faction-halo → zoom into faction; click-mechanic-centroid → zoom into mechanic family; lasso polygon → zooms in on lassoed region
- **Performance budget:** trivial on both surfaces

**Level 1 — Mid zoom (constellation visible):**

Player sees constellation-level structure. Goal: differentiated kit selection.

- **What renders:** constellation-centroid markers (one per kit) within the zoomed region; bounded-cluster outlines; faction halo + mechanic-family color encoding preserved at element-region scale
- **Spatial intent:** player sees "these are the constellations in this region; that one is bigger; that one is more strongly fire-aligned"
- **Cognitive load:** medium — 100s of visible constellation markers; player narrows toward specific kits
- **Interaction:** click-constellation-marker → highlight + side panel; lasso polygon → select constellations within polygon; further zoom-in → Level 2
- **Performance budget:** medium — sprite/marker count grows; manageable on PC; mobile may benefit from sub-region culling

**Level 2 — Drilled-in (per-primitive detail):**

Player sees individual primitive-stars within constellations. Goal: substrate-level analysis + refined selection.

- **What renders:** full per-primitive-star detail within constellations in the zoomed region; constellation-bounds soft; element-tinting at primitive level; brightness encoding for BDI ω+τ weights (load-bearing primitives glow brighter)
- **Spatial intent:** player sees "this constellation has these specific primitives; that fire-star is load-bearing; that wind-star is supporting"
- **Cognitive load:** high — many visible primitives; player engages substrate-analytical mode
- **Interaction:** primitive-hover surfaces primitive metadata; lasso polygon at this level selects individual primitives (not whole constellations); analyst-mode interactions
- **Performance budget:** highest — full per-primitive rendering; LOD-mandatory for full-corpus visibility; mantis-validated achievable in UE with viewport-scoped culling

### 2.2 LOD transitions

**Smooth + continuous** — NOT snap-toggles. Player's zoom action (scroll / pinch / camera-distance) progressively reveals detail. Each LOD level fades into the next over a zoom range; never modal mode-switches.

**Drax 2D /forge:** zoom threshold at ~1.5-2.0× scale triggers the centroid→full-detail reveal; opacity blending during transition.

**Mantis UE 3D:** camera-distance threshold per LOD level; mantis's Level 0/1/2 transitions managed via Niagara emitter visibility per camera distance; smooth opacity fade during transitions.

### 2.3 Lasso behavior across LOD levels

Lasso semantics shift per LOD level (substrate-correct per Discipline #25):

- **Level 0 lasso:** selects mechanic-families / faction-overlays; coarse-grained selection
- **Level 1 lasso:** selects whole constellations within polygon; per-kit composite-score lookup (constellation-overlap algorithm per `2026-06-06-cosmograph-star-granularity-verdict.md` § 4.3)
- **Level 2 lasso:** selects individual primitives within polygon; substrate-analytical selection (advanced player use)

Cross-surface consistency: same lasso semantics whether player is on drax /forge or mantis UE 3D. Player learns once.

### 2.4 Spirit form transformation at each LOD level (UE 3D specific)

For the Earth-avatar creation moment scene specifically (per `2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md`), the ambiguous spirit form responds to lasso selection at each LOD level:

- **Level 0 lasso → spirit transforms toward faction-level identity** (e.g., "STR-warrior archetype" + faction-tinted aura; still ambiguous individual identity)
- **Level 1 lasso → spirit transforms toward specific constellation** (full kit visual emerging; constellation-anchored identity)
- **Level 2 lasso → spirit fine-tunes on primitive-level selection** (advanced refinement; rare-use path)

This composes the LOD architecture with the dual-path creation mechanism — LOD provides the natural zoom-in flow as player narrows from broad exploration to specific selection.

---

## 3. Cross-surface vocabulary table

Single source of truth for LOD vocabulary across both surfaces:

| Level | Player concept | Drax /forge 2D | Mantis UE 3D | What spirit form does (UE 3D) |
|---|---|---|---|---|
| 0 | "Show me the landscape" | Centroid dots at 1.0× zoom; faction-halo overlays; mechanic-family color regions | 6 mechanic-family centroids OR faction halos at default sphere-overview camera distance | Faction-level identity (e.g., warrior aura; ambiguous individual) |
| 1 | "Show me the choices" | Constellation-bound reveal + centroid markers at ~1.5-2.0× zoom | ~300-500 constellation-centroid markers + faction overlays at mid camera distance | Specific constellation identity (full kit visual emerging) |
| 2 | "Show me the details" | Full per-primitive stars within constellations at ≥2.0× zoom | Full N primitive-stars within proximate region | Fine-tuned primitive-level refinement (advanced) |

---

## 4. Composition with prior commitments

### 4.1 Earth-avatar creation moment architecture (2026-06-07)

This LOD architecture is what makes the dual-path creation mechanism work at production scale. Without LOD:
- 1000+ constellations × 15+ primitives = ~15K visible nodes; visual noise at default zoom
- Player can't intuit kit boundaries; lasso behavior unclear at uniform-detail level
- Cosmograph aesthetic-immersive surface fails to read as discrete kit-as-discovery

With LOD:
- Level 0 default: player sees vast sky structured by element-region + faction-overlay (vast-night-sky emotional resonance)
- Path L (lasso) at any LOD level returns intelligible selection
- Path I (drop ingredients) at Level 1 highlights constellation-level convergence; at Level 2 surfaces specific primitive-level matches
- Spirit form transformation at each LOD level provides continuous compositional feedback

### 4.2 Cosmograph-pivot § 9 substrate lock

LOD operates OVER the primitive-as-star + kit-as-constellation substrate. Substrate is unchanged at each LOD level — what changes is what's RENDERED, not what EXISTS. Substrate truth at geometry layer (Discipline #41 substrate-led) preserved at every LOD level.

### 4.3 Mantis spike Session 3 perf data

Empirical perf validation for UE 3D LOD architecture per mantis Session 3:
- Tier 1 (100 stars): trivial perf
- Tier 2 (1000 stars): trivial perf
- Tier 3 (15,000 stars): 15-25ms GPU, 40-67 FPS, LOD required for 60fps
- LOD architecture (Level 0 = 6 centroids / Level 1 = 300 / Level 2 = full N) confirmed sustains 60fps at production scale

### 4.4 Drax /forge Phase 2 LOD operational

Empirical validation for 2D web LOD architecture per jack-ryan Gate-2 PASS-with-INFO at `cb2d60d`:
- LOD operational: dots at normalizedZoom < 2.0; full star clusters at ≥ 2.0
- Single-frame visibility toggle, no redraw
- 60 FPS confirmed in both modes
- Production deployed at `https://reincarnated-loadout.vercel.app/forge` (constellation default) + `https://reincarnated-loadout.vercel.app/forge?view=primitive` (analyst toggle)

### 4.5 WS2 commission scoping inherits

Per `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4 WS2 rendering layer port: this cross-surface LOD lock is inherited as design intent. WS2 mantis UE production rendering implements the Level 0/1/2 architecture; cross-references drax /forge implementation for consistency.

---

## 5. Empirical-evidence triggers for refinement

The vocabulary lock is appropriate NOW based on convergent empirical evidence from both surfaces. Refinement may be appropriate if:

### 5.1 Playtest evidence surfaces LOD-vocabulary friction

WS2 prototype playtest data may reveal:
- Player confusion at LOD transitions (snap-feel; opacity-fade inadequate)
- Player expectation that lasso behavior is uniform across LOD levels (current design has lasso semantics shift per level)
- Cross-surface inconsistency from drax to mantis surfaces feels awkward

If any of these surface: amend this lock based on playtest evidence; preserve substrate-led discipline at refinement.

### 5.2 Production effects stack changes LOD perf calculus

When WS2 mantis implementation adds full effects stack (VDB nebula + ribbon edges + emissive materials), perf budget tightens. Mantis Session 3 noted ~5-9ms additional cost — may push 15K-sprite scenario to ~20-25ms (40-50 FPS uncapped). LOD architecture may need additional Level granularity OR more aggressive Level 0 condensation. Empirical-evidence trigger: WS2 implementation perf profiling.

### 5.3 Mobile platform constraints (D8 canonical 38)

Mobile port (D8 mobile-polish phase) likely needs MORE aggressive LOD than PC. Mantis Session 3 flagged LOD as "required for mobile" — specific mobile LOD tuning is WS5 scope.

### 5.4 Beyond 500-constellation vertical-slice scale

Vertical-slice spike uses 500 PROVISIONAL constellations per Matt 2026-06-07 conservative scoping. If vertical slice validates well, scale-up to 1000+ at WS2 production fires; LOD architecture may need further tuning at scale. Empirical-evidence trigger: WS2 production perf at full-corpus scale.

---

## 6. What this architecture LOCKS

1. **Three-level LOD vocabulary** (Level 0 / Level 1 / Level 2) shared across both surfaces. LOCKED.
2. **Centroid-first at Level 0** (macro centroids visible by default; not per-primitive detail). LOCKED.
3. **Smooth + continuous transitions** (not modal mode-switches). LOCKED.
4. **Lasso semantics shift per level** (Level 0 selects faction; Level 1 selects constellation; Level 2 selects primitive). LOCKED.
5. **Substrate truth preserved at every LOD level** (LOD changes rendering, not substrate). LOCKED.
6. **Spirit form transformation responds to lasso at each LOD level** (Earth-avatar creation moment compose). LOCKED.
7. **Player learns LOD vocabulary once** — same mental model on drax /forge 2D + mantis UE 3D. LOCKED.

---

## 7. What this architecture does NOT specify (deferred)

- Specific zoom thresholds (drax used 2.0×; mantis used camera-distance specifics) — surface-specific tuning OK
- Specific Level 1 mid-density count (drax: varies with zoom region; mantis: ~300-500) — surface-specific tuning OK
- Specific transition opacity-fade curves — surface-specific aesthetic OK
- Specific LOD UX trigger gestures (mouse-scroll / pinch-zoom / camera-orbit-distance) — surface-specific input modality OK
- Specific mobile LOD tuning (D8 / WS5 scope)
- Specific full-effects-stack perf budget allocation (WS2 production scope)

These are surface-specific implementations of the cross-surface architectural vocabulary lock. Implementations may diverge in tuning; vocabulary (Level 0/1/2 + centroid-first + smooth-transitions + lasso-semantics) does not.

---

## 8. Decisions-log entry recommendation

This architectural commitment WARRANTS a decisions-log entry per decision-log-format skill (architectural commitment YES). It's the second cross-workstream instance of LOD-architecture discipline emerging (founding instance was drax Phase 2; second is mantis Session 3 convergence). Per jack-ryan Gate-2 PASS-with-INFO on drax: "discipline candidate queued for second-instance activation." **This is the second-instance activation.**

Recommended decisions-log entry:

```
2026-06-07: Cosmograph cross-surface LOD architecture locked (Level 0/1/2 centroid-first)

Decision: Three-level LOD vocabulary (Level 0 macro centroids / Level 1 constellation visible / Level 2 per-primitive detail) locked cross-surface for both drax /forge 2D web cosmograph + mantis UE 3D production cosmograph. Centroid-first at default zoom; smooth+continuous transitions; lasso semantics shift per level; substrate truth preserved at every level.

Reasoning: Both surfaces independently arrived at centroid-first LOD through different drivers (drax: visual-readability + perf at 15K nodes; mantis: Niagara perf at 15K sprites Tier 3). Convergent empirical evidence validates the architecture. Cross-surface lock prevents player learning two mental models for same interaction.

Alternatives considered: per-surface independent LOD vocabularies (rejected — cross-surface inconsistency cost > implementation flexibility benefit); uniform-detail at all zoom levels (rejected — visual noise + perf cost at production scale); modal mode-switches between LOD levels (rejected — UX friction at transitions).

Status: LOCKED — load-bearing cross-surface architectural commitment. WS2 commission scoping inherits as design intent.

Related: canonical/story/2026-06-07-cosmograph-cross-surface-LOD-architecture.md (this doc); canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md (LOD makes spherical-shell tractable at scale); canonical/story/2026-06-05-cosmograph-pivot.md § 9 (substrate lock LOD operates over); agentic_orchestration/qa/findings/2026-06-07-drax-cosmograph-a-b-spike-gate-2.md (drax LOD operational); agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/port-workstream-gating-verdict.md (mantis LOD validated).

Discipline candidate ratified: "Cross-surface architectural-vocabulary lock when convergent empirical evidence from independent surfaces validates the same architecture" — founding instance is this LOD lock.
```

---

## 9. Sign-off

**Authored:** gandalf 2026-06-07 per cross-cutting design authority composing drax /forge Phase 2 + mantis spike Session 3 empirical convergence.

**Authority:** gandalf cross-cutting design authority + Matt 2026-06-07 sequenced approval of Tier 1 close-out work (this doc + jack-ryan Gate-2 + decisions-log batched entries).

**Cross-references locked:** drax Gate-2 finding `cb2d60d` + mantis port-workstream-gating-verdict at `c169515` + Earth-avatar creation-moment architecture at `d3ced92`.

**End of cross-surface LOD architecture lock.**
