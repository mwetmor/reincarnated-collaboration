# drax Godot vertical-slice spike — brief

**Type:** spike brief / design-spec hand-off (gandalf seam → drax, via KR sequencing).
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 (Pattern-B) — style-register pivot to Godot 3D + fixed 2.5D camera; "start the godot prep in parallel"; **Synty Sidekick validated as the player base ("it is perfect!")**.
**Both empirical gates IN:** legolas (asset ecosystem + AI-gen reality) + galadriel (visual-register benchmark + acceptance rubric). This brief is authored *after* both returned, per the recognition record's § 6 sequencing.
**Companion docs:**
- `canonical/story/style-register.md` § "Register pivot" — the locked pivot this spike validates.
- `agentic_orchestration/gandalf/notes/2026-06-14-godot-pivot-modular-asset-strategy-and-dual-machine-workflow-recognition.md` — modular-asset strategy + dual-machine workflow.
- `agentic_orchestration/gandalf/notes/2026-06-14-stage-3-bc-cutover-scoping-ruling.md` § 4 — the drax co-brief (Pixi sweep + Godot coordinate-clean).
- legolas: `agentic_orchestration/research/knowledge/godot-3d-pivot/2026-06-14-godot-3d-asset-ecosystem-and-ai-gen.md`.
- galadriel: 3D-stylized-ARPG reference set + register-metrics (collab commit `bdd0ebc`) + the acceptance rubric (§ 1 below).

---

## 0. What this spike proves (the A-vs-B resolver)

The pivot locked Godot 3D + a fixed 2.5D camera but left ONE question spike-gated: **does register-1 modular geometry (Synty/Quaternius — flat per-face color), lifted uniformly in the shader + GI-lighting + VFX layer, reach perceived register-2 (the Torchlight Infinite / Last Epoch "premium stylized" look)?**

- **YES → Path A holds.** Cheap modular geometry + a controllable global lift = coherent premium roster. We never touch Path B.
- **NO → Path B.** Selective per-part hand-painting (bounded by part-count, not form-count) is added on top of A.

galadriel's benchmark already predicts YES (premium ≈ **~40% lighting + ~30% VFX + ~20% material-shading-above-the-flat-floor + ~10% geometry**; the cheapest-geometry reference — Torchlight Infinite — read the MOST premium of eleven frames). **This spike is the proof on our own hardware + content** — the validate step before the canonical register-taxonomy re-carve commits.

## 1. The acceptance target (galadriel's rubric — the pass bar)

Scored on four axes; **composite mean ≥ 3.6/5, with lighting ≥ 4 AND VFX ≥ 4 MANDATORY:**

| Axis | Target | Instrument |
|---|---|---|
| **Lighting drama** | manual ≥ 4 | LDR ≥ 115, SHF ≥ 30% dark-mood (CV-assisted) |
| **VFX presence** | manual ≥ 4 | ≥ 1 hero-skill bloom, HLF ≥ 1.5% (CV-assisted) |
| **Material-shading quality** | manual ≥ 4 | gradient/light-response, NOT flat per-face (manual-led; F2) |
| **Geometry register** | manual ≥ 3 | low-poly fine; silhouettes legible (manual) |

**NOT targets:** high high-frequency-detail / strong-edge%. Premium ≠ detail-density — chasing mesh detail is the wrong lever (galadriel's load-bearing finding).

**Capture protocol (galadriel F1 — load-bearing):** stills UNDER-represent VFX, the highest-leverage axis. Capture **multi-frame / short video of live dark dungeon-combat** — skills firing, particles alive, fog moving — NOT static screenshots. Light for mood (the dramatic-dark palette scored highest), not for visibility.

## 2. The build recipe (Path A first)

**Player + humanoid NPCs/summons (the validated-easy case):**
- Player from **Synty Sidekick** (Matt-validated; runtime part-swap API). Humanoid NPCs/summons from the **Synty family** (POLYGON range, shared palette atlas) → automatic in-frame coherence + a single whole-roster lift.
- Import path: FleMo93 Blender→Godot plugin OR Unidot importer + ufbx (material-rewiring expected — legolas).
- Shared **MasterSkeleton** + skin-sharing + `BoneAttachment3D` weapon/gear sockets (the auto-animation retarget spine).

**The lift (the layer we control — where register-2 is won):**
- **GI lighting:** SDFGI (real-time) or baked lightmaps; dramatic key/rim + dark ambient; Forward+ renderer for the PC-validate-high preset.
- **VFX (highest leverage):** `GPUParticles3D` + a hero-skill bloom via `WorldEnvironment` glow. At least one S-tier hero skill fully juiced — this single element does the most for perceived register.
- **Material-shading:** a gradient/light-responsive shader over Synty's flat albedo — clear the flat-color floor (a threshold, not a detail grind).

**The non-humanoid long-pole (the hard case — do NOT skip):**
- Include **at least one non-humanoid SKELETAL form** (quadruped or serpentine — from an available creature pack, e.g. KayKit / Synty POLYGON Dungeon creatures) to test whether a non-humanoid form holds **register-coherence beside the Synty-family humanoids in-frame.** This is where the form-bias discipline (doc 37) AND the register-feasibility question both bite hardest.
- Flag the **non-skeletal forms** (slime / swarm / cloud-being — squash-stretch / blend-shape / procedural, no shared rig) as the SECOND-tier hard case the spike's findings inform; not required in the first slice.

**Camera:** fixed 2.5D ARPG — `Camera3D` at a fixed Diablo-ish angle (orthographic or slight perspective). Lock it; the register reads through THIS frame, not a free camera.

## 3. The three crux de-risks (the spike's real engineering value)

1. **Auto-animation retarget.** Prove a Synty-family modular mesh retargets onto the shared MasterSkeleton and plays a shared animation set — the "can't hand-rig infinity" crux the 2D path fought. Low-poly geometry retargets MORE cleanly (legolas) — favorable, but PROVE it, don't assume it.
2. **Godot-version pin (bug #106073).** The skeleton bone-renaming bug breaks modular multi-skeleton imports in 4.3–4.4 (fix targeted 4.5, ETA unconfirmed). **Default: pin Godot 4.2.2** (known-good for modular). Alternatives the spike evaluates: 4.4 with single-skeleton-per-file imports (the workaround) OR wait-for-4.5. The spike CONFIRMS the viable import path on a chosen version before the pipeline commits to it.
3. **Dual-machine workflow loop.** Verify **low-Mac-edit → high-PC-validate** on real hardware: ONE Godot project git-synced; per-machine render presets (`mac-dev-low` Compatibility/Mobile + reduced viewport + shadows/particles off; `pc-validate-high` Forward+/full GI/VFX/fog) toggled by a git-ignored local config; build/script/lay-out on the Mac (8GB M2) at low settings → push → PC (RTX 4060 Ti) pulls + renders high. Confirm display-streaming (Sunshine/Moonlight or Parsec) lets Matt SEE the high output without walking to the PC. Cheap to verify now; expensive to discover broken later.

## 4. Coordinate-clean discipline (co-brief with the drax demo-VFX sweep)

Per the Stage-3 scoping ruling § 4: the Godot build keys class VFX overlays on the **bc coordinate, never the legacy label** — from the first frame. drax is already sweeping the Pixi demo's label-coupling (`main.ts` 1509/2108/2243) as a Stage-3 prereq; same move, same agent. Build Godot coordinate-clean so the new surface never re-imports the smuggling trap the cutover is spending three stages to delete.

## 5. Done / routing

- **drax:** builds the slice (§ 2 recipe), de-risks the three cruxes (§ 3), captures multi-frame/video (§ 1).
- **galadriel:** scores the captures against the § 1 rubric (CV-assisted lighting/VFX + manual material-shading/geometry).
- **gandalf:** interprets the score → **A holds / B needed** ruling; THEN the canonical `style-register.md` register-taxonomy re-carve fires (recognition → validate → **commit**).
- **KR:** sequences the drax queue (Stage-3 demo-VFX pre-check + this spike, co-briefed § 4); sequences the galadriel scoring pass; brings the A-vs-B result back for the canonical commit.

---

**Signed:** gandalf, 2026-06-14
**For:** the drax Godot vertical-slice spike — prove whether Synty-family register-1 modular geometry, lifted in the GI-lighting + `GPUParticles3D`-VFX + material-shading layer and framed through the fixed 2.5D camera, reaches galadriel's measured register-2 bar (lighting ≥ 4 + VFX ≥ 4 mandatory, composite ≥ 3.6/5) on our own hardware, captured as live dark-dungeon-combat video; de-risk the auto-animation retarget, the #106073 version pin, and the dual-machine workflow loop; and build coordinate-clean so the new surface never re-imports the label trap.
