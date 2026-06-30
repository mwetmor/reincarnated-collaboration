# Godot Asset-Gap Strategy — Equipment Catalogue (#2) & VFX (#3)

**Project:** Godot ARPG + AI asset pipeline
**Audience:** Claude orchestrator / designer / judge team (local Mac)
**Scope:** Two confirmed gaps. Maps/biomes (Synty) and base characters are fine and out of scope.
**Headline:** Neither gap is an *import/engine-reconfiguration* problem. Both route around forking Godot. #2 is a pipeline-attachment problem; #3 is a re-authoring problem.

---

## Why we are NOT reconfiguring Godot to read UE/Unity packs

Settled in prior discussion, restated so the team doesn't relitigate it:

- UE `.uasset` / Unity `.prefab` are **engine-baked object graphs**, not portable data. Reading them "natively" means reimplementing the referencing engine's runtime inside Godot — a forever-chasing reimplementation of two proprietary moving targets.
- **VFX has no portable format at all.** A Niagara / VFX-Graph effect is executable behavior bound to that engine's renderer, not data to translate.
- **Licensing wall:** UE Marketplace/Fab and Unity Asset Store licenses generally grant use *within that engine's runtime only*. Loading them into Godot is usually outside license regardless of technical feasibility. (Synty is the permissive exception we already exploit — raw FBX, friendly terms. Check every other pack per-license before any effort.)

Conclusion: build pipeline tooling, not an engine fork.

---

# #2 — Equipment Catalogue (body armor / helmets)

## Diagnosis
This is **not** an import problem — glTF/FBX already import fine. It is an **attachment + rig-consistency + volume** problem. We want a large AI-generated catalogue of armor/helmets that mount correctly on existing characters.

## Mechanism (native Godot, zero engine changes)
- **Helmets / pauldrons / weapons →** rigid mesh parented to a `BoneAttachment3D` on the named bone (head, shoulder, hand). Trivial and native.
- **Body armor (deforming) →** skinned mesh that shares the character's `Skeleton3D`, weighted to the same bones so it deforms with animation.

The hard part is **rig consistency**: every generated piece must attach to the *same* socket points, and skinned pieces must weight to the *same* skeleton. Solve this once, scale to 400+ pieces.

## The build: a Meshy→Godot equipment-mounting addon
A Godot editor addon that turns "a folder of generated meshes" into "mounted, materialized, validated equipment":

1. **Ingest** — watch a folder; import each FBX/glTF.
2. **Classify** — read a naming convention or sidecar JSON (`slot: head|torso|legs|...`) from the serial engine.
3. **Mount** — rigid pieces → spawn `BoneAttachment3D` on the slot's bone and parent the mesh; skinned pieces → bind to the shared `Skeleton3D`.
4. **Materialize** — apply the StyleProfile-driven material (this is the existing "one-shader-400-profiles" parametric thread, repointed at equipment).
5. **Validate** — auto-check: does it attach without error? Does a skinned piece reference the canonical skeleton? Bounds sane vs. the body? Reject + log failures for the judge.

## Where the Claude team plugs in
- **Designer** — generates the slot/StyleProfile sidecar JSON the addon consumes; proposes parametric variation across the catalogue.
- **Orchestrator** — runs catalogue batch jobs; manages versioned equipment pools (same pattern as seasonal map pools).
- **Judge** — grades each mounted piece against its StyleProfile + a fit check (no clipping into the body at rest pose). **Narrow, well-posed task** — not holistic level grading.

## The one rule that makes this scale
**Lock a canonical skeleton + named socket contract first.** Every Meshy generation request must target that rig. If pieces are generated against drifting skeletons, mounting breaks and no addon saves it. Rig contract → then volume.

---

# #3 — VFX (the real bottleneck)

## Diagnosis
Two walls at once: **content scarcity** (few usable Godot VFX packs) and a **tooling ceiling** (Godot's particle authoring lags Niagara / VFX Graph). The Godot core team itself acknowledges the gap — the particles maintainer has stated the goal is to reduce the "gotchas" Godot puts in front of technical artists, with visual-shader support for process materials and more spawn options on the wishlist, and notably **no contributor is specifically dedicated to particles**, so no timeline. So the lag is real and won't close soon on its own.

There is **no fork-Godot fix** — a Niagara effect is renderer-bound behavior, not importable data. The durable win is two stacked moves: harvest portable *ingredients*, and *re-author* the simulation with AI.

## Move A — Texture-driven VFX (highest leverage, do this regardless)
The thing that makes a premium VFX pack look premium is mostly its **flipbook sheets, gradient ramps, noise textures, and meshes** — all portable PNG/mesh data, often legally usable as raw art. The simulation is the *cheap* part; the textures carry the quality.

Modern good-looking Godot VFX workflow:
- High-quality **flipbook / noise textures** → `GPUParticles3D`.
- `ParticleProcessMaterial` for behavior, **or** a custom `ShaderMaterial` applied across all particles for anything non-trivial (the process material alone hits a ceiling fast).
- Flipbook animation is driven via the particle material's animation frames (h-frames / v-frames / loop) matched to the sheet layout.
- **Sub-emitters** for layered effects (e.g. sparks spawning smoke), now supported in Godot 4.
- Default to GPU particles (Vulkan/GLES3); keep `CPUParticles3D` only as a low-end fallback, **not** a 1:1 fallback — feature parity is no longer maintained.

## Move B — The Opus VFX-Translation Agent (the new tool)
Converts our **selection** problem into a **generation** capability. It does not import effects — it **re-authors** them to spec in Godot terms. Slots directly into the existing orchestrator/designer/judge loop.

### Input contract (any one, or combined)
- **Reference video / GIF** of the target effect (e.g. a Niagara effect recording).
- **Parameter intent** — structured description: emission shape, rate, lifetime, velocity, color-over-life, size-over-life, forces (gravity/turbulence), blend mode, flipbook sheet dims.
- **Text intent** — "a sharp electric arc impact, blue-white core, fast decay, secondary ember sparks."
- **Available ingredients** — the harvested flipbook/noise textures + meshes from Move A.

### Output contract (what the agent must emit)
A self-contained Godot effect:
- A `GPUParticles3D` node config (amount, lifetime, one_shot, local_coords, draw order).
- A `ParticleProcessMaterial` **or** a custom `ShaderMaterial` (`shader_type spatial; render_mode unshaded` baseline for stylized; richer shader when normal/motion maps are involved).
- Texture assignments wired to the Move-A ingredient library.
- Optional **sub-emitter** child node(s) for layered behavior.
- Saved as a reusable `.tscn` the game instances at runtime.

### Judge loop (this is why the agent is well-posed)
The judge renders the emitted effect and grades it **against the reference** — a narrow, concrete comparison (silhouette, color ramp, timing, density), unlike vague "does this look AI-made" level grading. Cross-model judging is fine here; the task is tight enough that model choice matters less than the reference anchor. Iterate: judge feedback → agent adjusts process-material/shader params → re-render.

### Why it fits our existing pipeline
Same "AI builds the parts, not the level" pattern from the map doc. The agent produces reusable effect `.tscn`s offline; the game instances them at runtime. No live AI in the hot path.

## Platform caveat (bake into agent output rules)
GPU particles that look right on desktop Vulkan can render invisibly on GLES/mobile/web — usually process-mode/pause-tree interaction, GLES feature limits, or visibility/layer-mask mismatches. If we ever target those platforms, the agent's output contract must include a mobile-safe profile, and we smoke-test "particles visible" on a real device. (Likely irrelevant for a desktop ARPG, but recorded so it isn't rediscovered painfully.)

---

# End-to-end: how both gaps sit in the pipeline

```
OFFLINE (AI + human, batched)
│
├── #2 EQUIPMENT
│     Meshy gen (against canonical rig) ──► Designer writes slot/StyleProfile JSON
│        └► Equipment-Mounting Addon: ingest→classify→mount→materialize→validate
│             └► Judge: per-piece StyleProfile + fit check
│                  └► VERSIONED EQUIPMENT POOL  (.tscn / scene library)
│
├── #3 VFX
│     Move A: harvest flipbooks/noise/meshes (portable, license-checked)
│        └► VFX-Translation Agent (reference/params/text + ingredients)
│             └► emits GPUParticles3D + ProcessMaterial/Shader (+sub-emitters) .tscn
│                  └► Judge: render vs. reference (silhouette/color/timing/density)
│                       └► VERSIONED VFX LIBRARY (.tscn)
│
▼
RUNTIME (deterministic, no live AI)
   Character + mounted equipment from pool   +   VFX .tscn instanced on events
        → on the procedurally-assembled act from the map pipeline
```

---

# Next steps (ordered by leverage)

1. **Lock the canonical skeleton + named-socket contract.** Blocks all of #2. Do first.
2. **Build the equipment-mounting addon** against that rig; prove it on ~5 helmets + 2 body pieces before scaling.
3. **Harvest a VFX ingredient library** (Move A) — flipbooks, noise, gradients, meshes; license-check each source.
4. **Stand up the VFX-Translation Agent** on one effect end-to-end (text intent → `.tscn` → judge vs. reference) before scaling the catalogue.
5. **Repoint the judge** to per-asset tasks for both tracks (StyleProfile+fit for #2; render-vs-reference for #3).
6. Version both output libraries the same way as the seasonal map pools, so a season swaps art across maps, equipment, and VFX coherently.
