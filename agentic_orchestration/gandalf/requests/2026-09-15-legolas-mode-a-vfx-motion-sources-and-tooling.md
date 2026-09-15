# Legolas Mode A — Motion sources and tooling for stylised painted-2D VFX (runnable on this host)

**From:** gandalf (SPEC-AUTHOR / ARCHITECT — VFX workflow architecture session, 2026-09-15)
**Mode:** A (analytical research; read-only; findings only)
**Findings to:** `agentic_orchestration/legolas/research/2026-09-15-vfx-motion-sources-and-tooling/findings.md`
**Host rule (binding — Mac mini 8 GB, kernel panic 2026-09-14):** NO video decoding, NO frame extraction, NO downloads > 50 MB, one fetch at a time, ≤ 1.5 GB RSS. Reading probe. Runs AFTER the grammar probe (serial).

## Why

Diagnosis from the six-kit breadth test (dossier `agentic_orchestration/gandalf/notes/2026-09-15-vfx-workflow-architecture/00-evidence-dossier.md` § 5): in both lanes that held, *the image model supplied a still and something else supplied time* (scene: the engine; character: a video model + oracle cut). The VFX lane asked the image model for time (rows of a grid) and got poses. The architecture therefore needs a **motion source** for effects that is not the image model. This probe maps the candidates.

## Q1 — Motion-source candidates: a comparison table

For each candidate below (add any you find), report: what it produces (frames on alpha / masks / particle data / a Godot scene); whether it runs on an **Apple-silicon Mac mini, 8 GB, no discrete GPU** (VERIFIED from docs or reports); cost/licence; how *stylisation* is applied (posterise / paint-over / shader); how *timing* is controlled (curves, per-frame holds, fps); output-to-Godot path; fit to the painted-pixel register (64–128 px native shape sprites, 2–4 value bands, no white core, halo + floor light on a separate layer); the cheapest first experiment.

- **Godot 4.6 native, procedural:** `GPUParticles2D` / `CPUParticles2D` (curves, sub-emitters, trails, `fixed_fps`), CanvasItem shaders (stepped TIME, erosion by distance field, posterise, scroll noise on a painted mask), `AnimationPlayer` tweens over painted primitives, `Line2D` for chains/beams. Is there prior art for *hand-painted-look* procedural 2D VFX in Godot (godotshaders "wobbly hand-painted", stepped-time, erosion)? 
- **Sim → sheet:** EmberGen (price; Mac? — historically Windows/Linux only, VERIFY current), Blender (free; Mantaflow smoke/fire, particles, Grease Pencil; posterised/toon render → sheet — VERIFY M-series feasibility at 8 GB), Houdini Apprentice (free non-commercial; feasibility), Unity VFX Graph / Unreal Niagara (only as precedent, not tooling).
- **2D FX authoring tools that export sheets:** Pixel FX Designer (CodeManu), Juice FX, Pixel Composer, Aseprite + scripts, Effekseer (and whether its Godot 4 runtime plugin is live), Spine/After Effects-class tools (precedent only), TimelineFX, Particle Illusion.
- **Video models on a plate** (evidence, not a recommendation): does any image-to-video model produce a usable **effect** loop with clean alpha or a keyable plate from a painted still (Grok i2v is in hand at 768×1168 24 fps 6 s; Veo 3.1 `last_frame`; Kling; Seedance; Wan)? Is there research or practitioner evidence for VFX-specific video generation (TransPixeler / TransAnimate RGBA — already known; anything newer or hosted)? What are the failure modes reported (boil, hue pulsing, internal cuts)?
- **Sim-then-paint precedents:** the 80.lv EmberGen-posterised anime explosion; Fortnite "20 of ~50" frames cut from a sim; Guilty Gear Xrd stepped timing; Hades `Fx.sjson` holds; any pipeline where an *image model* paints over sim frames (research or practice) — and what held identity across frames.

## Q2 — Which candidate produces the *invariants* an ARPG VFX system needs?

Rank the candidates on: (i) **timing control** (peak in 0–1 frames, halve in 2–7, residue 15–25 %, per-frame holds — the Hades bands in `2026-09-14-vfx-oracles/findings.md`); (ii) **grammar expressiveness** (orbit-emitter, thrown-arc → ground field, chain-with-jump, beam, nova, cone, aura loop, dash, ground slam — can the tool express the *shape of motion* per grammar, parameterised by range / radius / count / duration?); (iii) **register fidelity** (can it move *painted* shapes rather than render noise?); (iv) **coherence** (one system, one stack, shared primitives tinted per element); (v) **cost per new skill** once the system exists; (vi) **host feasibility**.

## Q3 — Two bounded questions

- Godot 2D: is there a documented way to render a `GPUParticles2D`/shader effect **to a sprite sheet** (SubViewport capture at fixed fps) so a procedural effect can be *baked* and then *paint-over-stylised*, then re-imported as a flipbook? Cite the mechanism (VERIFIED) or say none.
- For a painted-pixel register at 64–128 px native: which is the better default per grammar — **flipbook of painted frames** (drawn or baked) vs **runtime composition of painted primitives** (sprites moved/rotated/scaled/eroded by the engine)? Give the tradeoff per grammar class (burst / projectile / field / chain / aura / beam) with evidence from Children of Morta, Slormancer, Hades, Dead Cells where you have it.

## Fences

Read-only; no installs, purchases, accounts; classify every claim (VERIFIED / PRACTITIONER-REPORT / INFERRED); list gaps and blocked pages. Budget ~40 min. File findings and stop.

— gandalf, 2026-09-15
