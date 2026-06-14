# Celestial-Sphere Math/Transform Note + 1,005,000-Particle Root-Cause (Tier-A A1)

**STATUS:** CURRENT — Tier-A deliverable A1 for dispatch `2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md`.
**Date:** 2026-06-13
**Author:** mantis (UE 5.7 seam)
**Discipline:** #1 (math-before-code) — this note precedes any BP/Niagara edit. Silent count reduction without root-cause = Discipline #1 violation; this note IS the root-cause.
**Scope:** headless analysis only (no UE session opened; no GPU render). Source-of-truth = the JSON on disk + the `NS_CelestialSphere.uasset` binary strings + the generator/placement scripts.
**On-disk twin:** copy filed at `C:\dev\reincarnated-unreal\Reincarnated\docs\2026-06-13-celestial-sphere-math-transform.md` (UE tree not git-tracked; THIS collab-repo copy is the tracked deliverable).

---

## 1. Source data (verified, not assumed)

File: `Content/Data/CosmographSpike/cosmograph_sphere_001000stars_R8000.json`
- `star_count` = **1000**; `star_positions_flat` parses to exactly **1000** XYZ triples.
- `star_colors_flat` = **4000** floats = 1000 × **RGBA** (verified: `[1,0.3,0.05,1, ...]` — the 4th element is alpha=1.0).
- **Radius: every star is at radius exactly 8000.0 UU** (min=mean=max=8000.0). Clean sphere; no reposition-of-radius needed — only an axis transform (§ 3).
- `coordinate_space` = `{units: UE_units, origin: scene_origin (sphere center == camera position)}`.
- Discipline #40 scaffold-flagged (spherical-Fibonacci projection of spike-lineage cluster data; NOT substrate-truthful kit placement; contract 6.7 absent). Render it honestly as scaffold; never fake-as-substrate.

## 2. R = 8,000 sphere geometry (§ 2.6 spherical-shell lock)

- Stars lie on the **interior** surface of a sphere of radius **R = 8,000 UU**, centred at the scene origin, which is also the camera/avatar eye position.
- The avatar/camera looks **up** at the interior surface.
- `cap_half_angle_rad` = 0.62 (~35.5°): 6 element-clusters occupy distinct angular caps spread over the FULL sphere (below-horizon caps are INTENTIONAL — a ground-POV look-up only sees the upper hemisphere; below-horizon stars are correctly culled by the ground).
- No radial work required: positions are already at |r| = 8000. The ONLY geometric defect is the up-axis convention (§ 3).

## 3. Coordinate-convention transform — THE load-bearing geometry finding

**The generator (`spike-s5-s1/gen-sphere-stars.js`) builds the sphere with +Y as the up/overhead pole, but UE is Z-up.**

Evidence (from the generator source, not inference):
- `dirForCapIndex(i,n)` spreads cap centres using `y = 1 - (i/(n-1))*2` (the **Y** component is the elevation/pole axis).
- Per-cluster local fibonacci: `local = [sin(phi)*cos(theta), cos(phi), sin(phi)*sin(theta)]` — the cap-local "up" (cos phi) is on **Y**.
- `rotateVecToAxis(...)` rotates "around +Y" — the whole construction treats **+Y as up**.
- Empirical confirmation on the emitted JSON: stars near +0.9R cluster on **Y (98 stars)** vs Z (35) vs X (7). The dense overhead pole is **+Y**.

**UE world space is Z-up, left-handed.** If `star_positions_flat` is fed verbatim into a Niagara `Position` (world-space), the "overhead" +Y pole renders toward UE **+Y (a horizontal direction)** — so the dense cap lands on the **horizon**, not overhead. `Cam_GroundLookUp` pitches UP (toward +Z) and would see the sparse side of the distribution, not the intended cluster caps.

### Required transform (apply at consumption — at the user-param binding, NOT by rewriting the JSON)

Map source (+Y up) → UE (+Z up), preserving handedness and chirality:

```
UE.x =  src.x
UE.y =  src.z
UE.z =  src.y        // source pole +Y  ->  UE up +Z
```

This is a Y↔Z swap. It is an **orthonormal axis relabel** (a reflection-free re-basis when combined as below); to keep it a proper rotation (no mirror), apply it as a +90° rotation about the X axis:

```
Rx(+90°): (x, y, z) -> (x, -z, y)
```

Either form puts the +Y source pole at UE +Z. **Recommendation: apply `Rx(+90°)` → `(x, -z, y)`** so it is a pure rotation (determinant +1, no handedness flip). Magnitude is preserved (|r| stays 8000). Decision for the BP author: do the swap **in `BP_CelestialSphere` before `SetNiagaraArrayVector("StarPositions", ...)`**, OR set the `CelestialSphere_Sky` actor's **rotation to `Roll=0, Pitch=0, ...` with a +90° pitch about local X** so the emitter's local-space array is rotated into world. The in-BP array transform is preferred (explicit, inspectable, no actor-rotation coupling).

**Colors:** pass `star_colors_flat` straight through as `SetNiagaraArrayColor("StarColors", ...)` (RGBA, no transform).

**Sanity gate after binding (Tier-B render):** with `Cam_GroundLookUp` piloted, the 6 cluster caps should read as distinct overhead/upper-hemisphere regions; no dense cap on the horizon line; no stars at the origin.

## 4. The 1,005,000-particle root-cause — A1 (the must-document finding)

**Root cause: the celestial-sphere emitter spawns from inherited point-cloud spawn logic that is completely DECOUPLED from the 1,000-star JSON, because the `StarPositions` array was never bound.**

Chain of evidence:
1. `NS_CelestialSphere` was created by **`duplicate_asset` from `NS_CosmographPointCloud`** (`spike-s5-s1/s1-celestial-sphere.js` step S1.2). It inherited that system's emitter wholesale.
2. The array-binding step (`SetNiagaraArrayVector("StarPositions", ...)`) was **NEVER executed** — it is windowed/BP-gated (`set_niagara_parameter` has NO array support; confirmed in AGENT_STATE TODO "S1 Gate A — position-array binding" still open, and in the s1 script's WINDOWED-GATED header).
3. Therefore the emitter has **no knowledge of the 1,000 stars**. It runs its own spawn rule.
4. `NS_CelestialSphere.uasset` binary strings confirm the spawn mechanism:
   - `ENiagaraSimTarget::CPUSim` — the emitter is **CPU sim** → subject to UE's **1,000,000 CPU-particle cap** (this is the cap the live `1,005,000 vs 1,000,000` warning hit).
   - `Niagara/Modules/Emitter/SpawnBurst_Instantaneous` with `Constants.Minimal.SpawnBurst_Instantaneous.Spawn Count` + `... .Loop Count Limit`, on `ENiagara_InfiniteLoopDuration`.
5. **The 1,005,000 is a runtime-accumulated total, not a stored constant** — a scan of the uasset for `1005000`/`1000000`/`1005` as stored float32 found NONE (the rapid-iteration parameter store does not hold it as a plain aligned float). This is consistent with `1,005,000 = SpawnBurst Spawn Count × loop-instances` accumulating over the infinite-loop emitter (e.g. a per-burst count in the low thousands × many loop iterations), OR a single oversized burst — the precise arithmetic lives in the per-emitter Spawn Count default inherited from the point-cloud system and is only authoritatively readable in the Niagara editor (manual-BP step M1).

**Why it sits at the origin (the "±67 spike cloud"):** with no `StarPositions` binding, the inherited `InitializeParticle` spawns particles around the emitter/actor origin (the point-cloud system's local spawn distribution), NOT on the R=8,000 sphere. `CelestialSphere_Sky` is placed at world origin (s1 script S1.3), so the cloud sits at the origin directly under the avatar — exactly the live finding.

**The fix is NOT "reduce the spawn count."** Reducing the inherited count would still spawn an origin cloud of the wrong stars. The correct fix (and the only one that is Discipline-#1-honest):
- (a) **Bind the JSON**: expose + drive `StarPositions`/`StarColors` user-params so the emitter spawns **exactly 1,000 particles, one per JSON star, at the transformed R=8,000 positions** (spawn count becomes 1,000, sourced from the array length).
- (b) **Move to GPU sim**: the 1M cap is CPU-only; GPU sim removes the cap headroom AND is the correct target for a static positional point set read from a data interface.

Once (a)+(b) land, the count is **1,000** (one particle per star), not 1,005,000, and that reduction is a *consequence of binding the real data* — not a silent knob-turn.

## 5. CPU→GPU migration note (A2)

- Current: `ENiagaraSimTarget::CPUSim` (verified in uasset strings).
- Target: `ENiagaraSimTarget::GPUComputeSim`.
- The 1,000,000-particle cap is a **CPU-sim limit**; GPU sim is not bound by it. For 1,000 static stars GPU is not strictly required for the count, but it is the dispatch-specified target (A2) and is the right sim target for a positions-from-data-array point field with no per-frame CPU readback.
- **GPU-sim requires fixed/explicit emitter bounds** (GPU sims can't compute dynamic bounds cheaply): set Fixed Bounds to a box of half-extent ≥ R (e.g. ±8,200 UU each axis) so the sphere isn't frustum-culled. This is part of manual-BP step M2.
- **Sim-target change is NOT a bridge primitive** (no `set_niagara_sim_target` in the proven tool set) → manual-BP (M2).

## 6. Nebula cost-cut + `stat gpu` budget threshold (A7)

Cost-cut actions (from dispatch § 2 repair #1.5 — these make the nebula cheap enough to leave ON so S1 renders a real sky, retiring the session-only `r.HeterogeneousVolumes 0` band-aid):
- `r.HeterogeneousVolumes.MaxStepCount` **256 → 32**.
- Raise `r.HeterogeneousVolumes.DownsampleFactor` (e.g. 1 → 2 or 4).
- **Kill volume shadows**: `r.HeterogeneousVolumes.Shadows.Resolution` off/low (was 512).
- Trim `VolumetricFog` (lower `r.VolumetricFog.GridPixelSize` quality / disable on the nebula if redundant with the VDB).
- Cap Niagara star overdraw: small sprite size at sky distance, GPU fixed bounds (§ 5), additive-but-tiny.

**`stat gpu` budget threshold (the documented Tier-B PASS target — A7 / sam WARN-2):**
> Piloting `Cam_GroundLookUp` with the look-up view filling the screen (nebula + repositioned sphere visible), the scene must hold a **stable frame for ≥ 30 seconds with `stat gpu` total frame GPU time ≤ 16.6 ms (≥ 60 fps), and NO rising trend** in GPU time across that window (a rising trend is the pre-`D3D Device Removed` signature observed in the crash). Specifically: the `HeterogeneousVolumes` + `VolumetricFog` line items in `stat gpu` must each be bounded and flat, not climbing. Secondary acceptance: `stat unit` GPU ≤ 16.6 ms; `stat fps` ≥ 60. Hardware reference: RTX 4060 Ti (the crash was a scene-cost problem, not a hardware ceiling).

This threshold is what B2/B5 are measured against at the console. If the cost-cut does not bring GPU time under 16.6 ms / flat, the next lever is `MaxStepCount` 32 → 16 and/or `DownsampleFactor` 4 → 8 before considering disabling the volumetric nebula (which canon requires ON — radagast design-fit (a)).

## 7. D7 (A6) — confirmed headless

Stars + colors + cluster caps are **hand/JSON-authored** (generator-deterministic from spike-lineage cluster data); constellation runes/edges are JSON (`constellation_edges` in tier2). **No runtime LLM** anywhere in the render path. D7 PASS by construction.

## 8. Headless-vs-manual partition (drives the manual-BP-step list)

| Tier-A | Headless-closeable? | Disposition |
|---|---|---|
| A1 root-cause + math/transform | YES | CLOSED (this note) |
| A2 CPU→GPU sim | NO — not a bridge primitive | manual-BP M2 |
| A3 expose+drive `StarPositions`/`StarColors`; `BP_CelestialSphere` load JSON + apply Rx(+90°) | NO — `set_niagara_parameter` has no array support; BP graph authoring | manual-BP M1/M3 |
| A4 figure-lighting DIRECTION (re-aim moonlight; skylight source); no-longer-black | DIRECTION specifiable headless, but SUCCESS = Lit render (DXGI-gated); persisting unverified light mutation into a pristine level is the wrong trade | manual-BP M4 (DIRECTION pre-specified here) |
| A5 Rig A/B toggle wired + distinct poles | toggle exists (RigA/RigB tags from prior spike); distinctness is a values/temperature read = Tier-B | manual-BP M5 (wiring confirm) |
| A6 D7 | YES | CLOSED (§ 7) |
| A7 nebula cost-cut + `stat gpu` threshold | threshold DOCUMENTED headless; CVar/material apply + measure = Tier-B | threshold CLOSED (§ 6); apply = manual-BP M6 |

**Why no headless UE session was opened:** every remaining headless-*applicable* edit's success criterion is render-gated (Tier-B/DXGI). The Niagara core (A2/A3) has no headless bridge path at all. Per sam Gate-1 WARN-1 (load-bearing), when the headless path cannot complete-and-verify an edit class, STOP and hand Matt an ordered manual-BP list rather than persist unverified mutations into the pristine level. The manual-BP list is the legitimate Tier-A deliverable.
