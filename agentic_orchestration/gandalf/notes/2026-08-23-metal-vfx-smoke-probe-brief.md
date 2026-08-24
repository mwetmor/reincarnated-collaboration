# Metal VFX Smoke Probe — drax diagnostic brief

> **STATUS:** READY FOR LAUNCH (KR sequences, or Matt launches drax directly per the gamora-wave
> precedent). **Bounded diagnostic — no rulings required to fire.** Author: gandalf, 2026-08-23.
> Born of Matt's PC-SSH-tunnel question; governed by ruling **R-1(a)** (Matt 2026-08-23): Mac
> Metal stays renderer of record for the prototype era; this probe supplies the empirical answer
> to whether Metal is actually a constraint for VFX work — *before* any cross-host infrastructure
> is considered.

## Purpose

Two questions, answered with numbers and captures, not impressions:

1. **Feature integrity:** does the Metal renderer fail or visibly degrade any effect class we own
   (GPUParticles collision/turbulence, additive/blend stacking, trail meshes, beam shaders,
   soft-particle depth fade)?
2. **Throughput:** per-effect render wall-time under the standard capture harness — would a
   VFX bake-off cadence (many candidate renders per session) actually bottleneck on this machine?

## Scope + method (drax, `reincarnated-godot/`)

1. **Select ~8–12 worst-case effects** from the owned packs — deliberately the heaviest, not a
   fair sample: `BinbunVFX/` (fire/ice/poison/beam/smoke/loot), `PolygonArsenal/effects`,
   `brackeys_vfx_bundle/particles`, `Particle_FX`, `Synty/particle-fx-shapes`,
   `ThirdParty/rpicster-vfx-textures`. Pick for GPU-feature diversity, note the selection rationale.
2. **Mount each in a minimal isolated probe scene** — fixed camera, neutral floor, one effect per
   scene. NEW scenes only; zero contact with SB-1 surfaces or existing `run_*.sh` instruments.
3. **Render via the standard instrument pattern:** `--rendering-driver metal` (headless remains
   FORBIDDEN for renders per repo law), Movie Maker PNG → ffmpeg h264 → **SHA-256 determinism ×2 +
   ffprobe gates** — the probe uses the house evidence chain, it doesn't invent a lighter one.
4. **Record per effect:** wall-time (scene load / render / encode split if cheap), determinism
   result, any visual anomaly (missing particles, wrong blending, z-fighting, color shift).
5. **MoltenVK cross-check (suspects only):** any Metal-suspect result gets the SAME scene
   re-rendered on the Mac with `--rendering-driver vulkan`; side-by-side capture pair filed. This
   disambiguates "our scene is wrong" from "Metal quirk" without any PC involvement.
6. **Findings table** + captures filed for galadriel consumption.

## Constraints

- Read-only on `Assets/`; new probe scenes + one new probe instrument script only.
- No modification of existing instruments (they are pre-registered gates — U-7(b) law).
- No SB-1 collision: separate scene paths, separate capture dirs.

## Deliverable + downstream

`drax` findings note + capture set → feeds the **VFX archetype-binding run charter P0-b**
(same date, gandalf notes) and the **R-1 empirical track**. Revisit-trigger it arms: only a
concrete Metal feature failure OR wall-times that measurably bottleneck bake-off cadence reopens
the cross-host (PC/Vulkan) question — otherwise the tunnel stays retired.
