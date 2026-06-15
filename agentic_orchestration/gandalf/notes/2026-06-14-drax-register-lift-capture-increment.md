# drax Godot spike — register-2 LIFT + CAPTURE increment

**Type:** spike-increment brief / design-spec hand-off (gandalf seam → drax).
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 (Pattern-B) — "Let's have drax set it up." Parallel/independent of the KR weapon-as-identity track.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-14-drax-godot-vertical-slice-spike-brief.md` — the full vertical-slice spike. THIS is the lift+capture increment of it, authored after the compose/retarget cruxes cleared and the POLYGON + particle-fx assets loaded.
**Rubric source:** parent brief § 1 (galadriel's acceptance rubric) — the pass bar below is verbatim from it.

---

## 0. TL;DR — what + why

The prior spike already cleared the **engineering** cruxes: modular compose-from-DB, auto-animation retarget, and the composed **knight** whose graphical register Matt approved (`harness_logs/10_composed_knight_render.png`, scene `scenes/composed_render.tscn`). Project runs **Godot 4.6** — so the parent brief's version-pin crux (#106073 / pin-4.2.2 default) is **empirically resolved in the most favorable direction**; do NOT re-litigate it.

What the spike has **not** built is the **register-2 LIFT** — and per galadriel's benchmark that lift is **~70% of perceived premium (40% lighting + 30% VFX)**. The first renders are flat "does the mesh pose" proofs. This increment builds the lift and **captures it against the rubric** so gandalf can rule the parent spike's A-vs-B question:

> **A** = register-1 modular geometry, lifted in lighting+VFX+material-shading, reaches register-2 (premium-stylized) → cheap modular roster holds.
> **B** = it does not → selective per-part hand-painting added on top.

**One-line move:** drop the composed knight into a dark POLYGON dungeon room, light it for *mood*, fire 2–3 particle FX as hero-skill stand-ins, and capture **multi-frame / short video of live dark-dungeon combat** (NOT stills) → hand to galadriel for rubric scoring → gandalf interprets A-vs-B.

---

## 1. Current state — what exists, what's loaded (live-verified 2026-06-14)

**Already built (build ON these, don't redo):**
- `scenes/composed_render.tscn` + `scripts/render_composed.gd` — the composed Human base body via `SidekickCharacter.combine()`, spirit-swapped to the Starter knight outfit, on a fixed 2.5D ARPG camera + key/fill rig, dark env (`Color(0.08,0.09,0.13)`), filmic tonemap, `glow_enabled`. **This is your starting scene.**
- `scenes/baked_form_01.scn` (2.2 MB) — a baked composed form, if you want a static body to drop in without re-composing at runtime.
- `addons/sidekick_creator/` — the modular compose addon; `addons/godot-sqlite/` — DB access (already exercised).

**Just loaded by Matt (the lift materials):**
- **particle-fx** (Godot-NATIVE, 4.5 → loads in your 4.6) at `Assets/Synty/polygon-starter/particle-fx/Assets/Particle_FX/` — **14 ready `GPUParticles3D` scenes** in `Prefabs/FX/`: `FX_Fire_Large_01`, `FX_Fire_Medium_01`, `FX_Fire_Small_01`, `FX_Smoke_01`, `FX_Fog_01`, `FX_Dust_01`, `FX_Dust_Soft_01`, `FX_Ember`(material), `FX_Sun_Beam_01`, `FX_Snow_01`, `FX_Rain_01`, `FX_Leaves_01`, `FX_Flies_01`, `FX_Candle_Flame_01`. Plus `Materials/WorldEnvironment.tres`.
- **POLYGON Starter** (raw FBX) at `Assets/Synty/polygon-starter/SourceFiles/FBX/` — environment + prototype blocks for the stage: `SM_Generic_Ground_0{1-4}`, `SM_Generic_Mountains_*`, `SM_Generic_Small_Rocks_0{1-5}`, `SM_Generic_Tree_*`, and `SM_PolygonPrototype_Buildings_*` (blocks, floors, walls, columns, stairs, ramps) for graybox dungeon geometry, plus props (`SM_PolygonPrototype_Prop_Crate_03`, `_Sword_01`, etc.).

---

## 2. FIRST: the particle import fix (do this before anything else)

The FX scenes reference materials at **`res://Assets/Particle_FX/Materials/...`** (project-root-relative — the pack's authored paths), but the pack is nested at `Assets/Synty/polygon-starter/particle-fx/Assets/Particle_FX/`. **Those refs will NOT resolve until you relocate.**

**Cleanest fix:** move the `Particle_FX/` folder up to **`res://Assets/Particle_FX/`** (project root) so the authored `res://Assets/Particle_FX/...` paths resolve natively, then let Godot re-import. (Alternative — re-path every `ext_resource` — is tedious; relocation is the move.) The pack's own nested `project.godot` is irrelevant once the folder lives in the main project; ignore/delete it. Same for POLYGON: pull only the **specific FBX you need** from `SourceFiles/FBX/`; do NOT import the whole nested Unity/unidot structure.

Confirm `.gitignore` still excludes the Synty source (`/Assets/Synty/` is ignored) — but if you relocate `Particle_FX/` to `res://Assets/Particle_FX/`, that path is OUTSIDE the ignore rule. **Do not git-track raw Synty assets** (license: no sharing source outside the team). Either keep the relocated `Particle_FX/` git-ignored too, or relocate a *working copy* and add an ignore rule. Flag this in your report so we keep the repo license-clean.

---

## 3. The build (the lift recipe)

**Stage:** graybox a small dark dungeon room from POLYGON prototype blocks (floor + walls + a couple columns) OR a rocky outdoor pocket (ground + rocks + dead trees). Either reads as "dark ARPG encounter." Replace the placeholder `BoxMesh` ground in `composed_render.tscn` with real POLYGON geometry.

**Body:** the **composed knight** (re-compose via `render_composed.gd`'s path, or drop `baked_form_01.scn`). **Judge the register off THIS** — not the POLYGON "Bean" characters (those are capsule placeholders; ignore them entirely).

**Lighting (40% — the biggest lever):** dramatic key + rim against dark ambient. Push the existing dark env darker; one strong key (warm or cold) raking across the knight, a rim to pop the silhouette, low fill. Use `Materials/WorldEnvironment.tres` as a starting env if it's richer than the inline one. Light for **MOOD, not visibility** (galadriel: the dramatic-dark palette scored highest of eleven reference frames). Glow/bloom ON (`WorldEnvironment` glow).

**VFX (30% — highest leverage, most under-represented in stills):** wire **2–3 of the FX scenes as hero-skill stand-ins** firing near/around the knight — e.g. `FX_Fire_Large_01` as a cast burst at the weapon, `FX_Smoke_01` + `FX_Fog_01` for atmosphere drift, `FX_Ember`/`FX_Dust` for ambient life. At least ONE FX fully juiced as the "S-tier hero skill" bloom moment — this single element does the most for perceived register. Generic FX is fine (see § 5); the axis is what we're proving.

**Camera:** keep the existing **fixed 2.5D ARPG** camera. The register reads through THIS frame; lock it.

**Material-shading (20%):** the Synty albedo is flat per-face — if cheap, drop a gradient/light-responsive touch so it clears the flat-color floor under the dramatic light. This is a threshold, not a detail grind; lighting + VFX matter more. Don't chase mesh detail (galadriel: detail-density is the WRONG lever).

---

## 4. The capture (galadriel F1 — load-bearing; this is what the whole increment is FOR)

**Stills UNDER-represent VFX, the highest-leverage axis. Capture MOTION.**

- Render a **multi-frame image sequence** (≈60–120 frames) from the fixed camera of the scene **alive** — particles animating, fog drifting, the hero-skill FX igniting → peak bloom → dissipating. If `ffmpeg` is available, assemble to a short mp4/gif; if headless animated capture is awkward, at MINIMUM capture **4–6 distinct frames across the FX lifecycle** (pre-ignition / ignition / peak bloom / smoke-drift / settle) so the VFX axis is represented across time, per galadriel F1.
- Output to `harness_logs/` (sequence) — name them clearly (e.g. `11_lift_capture_NN.png` + `11_lift_capture.mp4` if assembled).
- Capture the dark-mood lit state, NOT a bright "show the geometry" state.

---

## 5. What NOT to do (guardrails)

- **Do not** judge the body off POLYGON Bean characters — composed knight only.
- **Do not** element-couple the particles to our 8-element system yet — that mapping (fire-FX→fire skills etc.) is a later pass. ANY juiced FX firing in-frame proves the axis for this spike.
- **Do not** self-score against the rubric — galadriel scores (CV-assisted lighting/VFX + manual material/geometry); gandalf interprets A-vs-B. You build + capture + report.
- **Do not** chase mesh/detail density — wrong lever.
- **Coordinate-clean (light touch, per parent § 4):** wire FX attach points sanely (BoneAttachment3D / scene-node, not hard-coded legacy labels). For stand-in FX this is minor — just don't bake in coupling we'd have to delete later.

---

## 6. The pass bar (galadriel's rubric — for context; you don't score, you build TO it)

Composite mean **≥ 3.6/5**, with **lighting ≥ 4 AND VFX ≥ 4 MANDATORY:**

| Axis | Target | Instrument |
|---|---|---|
| Lighting drama | manual ≥ 4 | LDR ≥ 115, SHF ≥ 30% dark-mood (CV) |
| VFX presence | manual ≥ 4 | ≥ 1 hero-skill bloom, HLF ≥ 1.5% (CV) |
| Material-shading | manual ≥ 4 | gradient/light-response, not flat per-face |
| Geometry register | manual ≥ 3 | low-poly fine; silhouettes legible |

This tells you where to spend effort: lighting + VFX are the mandatory gates.

---

## 7. Done / routing / HALT

- **drax:** § 2 import fix → § 3 build → § 4 capture; commit to the `reincarnated-godot` repo (auto-commit authorized, in-scope). **Then HALT and report back:** (a) what you built (scene path), (b) where the captures are, (c) the particle-import outcome + any git-license note, (d) any crux finding (4.6 behavior, retarget/compose surprises, perf on the 8GB M2 if you hit it). Do NOT self-score.
- **galadriel:** scores the captures against § 6 (next, after drax reports).
- **gandalf:** interprets the score → **A holds / B needed** ruling → then the canonical `style-register.md` register-taxonomy re-carve fires (recognition → validate → commit).

---

**Signed:** gandalf, 2026-06-14
**For:** the register-2 lift + capture increment — build the lighting+VFX+material lift on the already-composed knight in a dark POLYGON dungeon, fix the particle-import path, and capture live dark-dungeon-combat motion against galadriel's rubric so the parent spike's A-vs-B question can be ruled.
