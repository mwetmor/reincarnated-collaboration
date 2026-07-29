# PROVISION-CAL · cell PC-T12 — Tier-1 + Tier-2 battery (+ R-PC-7 texture repair)

**Run:** PROVISION-CAL (`2026-07-28-provision-cal-run-charter.md`) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Cell:** PC-T12 · **Executor:** drax (presentation seam, `reincarnated-godot`) · **Date:** 2026-07-28
**Riders:** TASK 0 = R-PC-7 texture repair + re-verdict · TASK 1 = charter §3 Tier 1 (pure-resource Layer-1 rows)
· TASK 2 = charter §3 Tier 2 (runtime GDExtensions)

**Boundary observed:** LOADS?/REACHES?, never BETTER. Scope frozen to the menu's rows. Anything discovered
outside those rows is logged in §F, never acted on.
**Instrument findings carried in from PC-W1-A:** **F8** (`godot --headless --import` rewrites `project.godot`
and prunes settings equal to engine defaults — check `git diff project.godot` after every pass) and **F9**
(deleting `.md5` does NOT force reimport on 4.6.3; only deleting the dest artifact does).

**Stack:** Godot `4.6.3.stable.official.7d41c59c4`, Forward+/Metal, macOS arm64 (Apple M2), project
`/Users/admin/Games/reincarnated-godot`.

**Write discipline:** this note is written incrementally, one section per row, so a timeout loses at most
one row.

---

## §0 — Verdict tally

**14 rows carry a verdict. 1 row deferred (out of tier). 1 re-verdict.**

| Verdict | N | Rows |
|---|---:|---|
| **LOADS-CLEAN** | **3** | 1 Compositor Lens Effects · 11 UniParticles3D · 21 GodotIK |
| **LOADS-DIRTY** | **5** | 2 GODOT-VFX-LIBRARY · 3 Godot Projectile Engine · 6 RPicster VFX textures · 7 proton_trail · 10 TrailRenderer |
| **FAILS-LOAD** | **2** | 12 Vaportrail · 14 YParticles3D |
| **EXCLUDED(licence)** | **4** | 5 godot-4-VFX-assets · 19 Godot4-OpenAnimationLibraries · 20 GodotHumanoidRetargetPlugin · 27 synty-godot-converter |
| *(deferred — editor-only ⇒ Tier 3)* | *1* | *4 Godot Shaders Library — not installed; R-PC-5 fence unspent* |
| **RE-VERDICT (R-PC-7)** | — | `SK_Chr_Werewolf_01.fbx`: **LOADS-DIRTY(missing-embedded-texture) → LOADS-CLEAN(albedo-repaired)** |

**Additionally, on a second axis the charter's Tier-1 verdict path does not have a slot for:**
**2 rows verdict `REACHES-NOT(3D surface)`** — rows 2 and 3 are entirely 2D and cannot appear at the
fixed ARPG camera, despite both being marked `EW=ALL` in the menu. See §3.2, §3.3, finding **G1**.

**Version drift since the menu's 2026-07-26 read: none.** All four Asset-Library `download_commit` SHAs
and all four release tags re-read identical on 2026-07-28 (L-C).

---

## §1 — TASK 0: R-PC-7 texture repair + re-verdict

### 1.1 — RE-VERDICT: **LOADS-CLEAN(albedo-repaired)**

`SK_Chr_Werewolf_01.fbx` re-verdicts **LOADS-CLEAN**. The albedo binding that PC-W1-A recorded as
absent is present and **rendering** — verified numerically *and* by eye.

**One correction to the cell brief, load-bearing:** the brief asked me to "verify albedo non-null on
**both** materials." The pack's own manifest forbids that. `MaterialList_PolygonWerewolf.txt`, verbatim:

```
Prefab Name: SM_Chr_Werewolf_01
    Mesh Name: SM_Werewolf_Mesh_01
        Slot: PolygonWerewolf_01_A (PolygonWerewolf_Texture_01_A)
        Slot: Eye_Glow (No Albedo Texture)
```

**`Eye_Glow` is specified to have no albedo texture.** Binding one to it would be content authoring,
which R-PC-7 explicitly excludes ("repair-to-spec, not content authoring"). So the correct repaired
state is **1 of 2 materials textured, 1 albedo-null BY SPEC** — not 2 of 2.

Slot→material assignment was decided **geometrically, not by name** (the FBX names are Maya defaults
`lambert1407/1408`, which carry no slot information):

| surface | material | verts | bbox size | UV span | ⇒ slot |
|---|---|---:|---|---|---|
| surf[0] | `lambert1407` | 12816 | **3.0513 m** | 0.0473 → 0.4989 | `PolygonWerewolf_01_A` (the body) |
| surf[1] | `lambert1408` | 48 | **0.1165 m** | 0.4838 → 0.4848 | `Eye_Glow` (11.6 cm; UV is a ~0.001 pinpoint = a flat atlas sample) |

Evidence: `/Users/admin/Games/reincarnated-godot/tmp/pct12/slotid.log`.

### 1.2 — Method (repair-to-spec, minimum judgement)

I did **not** hand-author a material. I used Godot's own `materials/extract` so the engine authored the
material from the FBX, then added exactly one line to it. Sequence:

1. **Baseline control (L-N)** — `tmp/pct12/matprobe2.gd` dumps every property differing from a virgin
   `StandardMaterial3D`, plus a standalone load of the pack PNG:
   ```
   CONTROL tex load: OK 4096x4096
     surf[0] lambert1407  albedo_texture = <null>
       NON-DEFAULT: vertex_color_use_as_albedo=true, albedo_color=(0.9063,0.9063,0.9063,0.8), emission_enabled=true
     surf[1] lambert1408  albedo_texture = <null>
       NON-DEFAULT: vertex_color_use_as_albedo=true, albedo_color=(0.6652,0.6652,0.6652,1.0), emission_enabled=true
   ```
   (`tmp/pct12/matprobe_before.log`)
2. Set `materials/extract=1` + `materials/extract_path=…/Materials`, delete the dest `.scn` (**F9**),
   reimport → Godot wrote `lambert1407.tres` / `lambert1408.tres` carrying *exactly* the non-default
   properties measured in step 1. Nothing invented.
3. Added **one property** to `lambert1407.tres`: `albedo_texture = ExtResource("1_albedo")` →
   `PolygonWerewolf_Texture_01_A.png` (`uid://7it5olafba6r`). Every other property untouched.
4. Deleted `lambert1408.tres` (spec says Eye_Glow has no albedo texture → an external override would
   be a no-op file), reverted `materials/extract` to `0` so a future reimport cannot overwrite the
   edited `.tres`, and wired the durable form instead — `_subresources.materials.lambert1407.use_external`,
   the **same shape the project already uses** on 200+ `polygon-dark-fantasy-01` imports.
5. Deleted the dest `.scn` (**F9**) and reimported.

### 1.3 — Verification

**Numeric** (`tmp/pct12/matprobe_after.log`):

```
surf[0] name=lambert1407 path=res://Assets/Synty/polygon-werewolf/SourceFiles/Materials/lambert1407.tres
  albedo_texture = res://Assets/Synty/polygon-werewolf/SourceFiles/Textures/PolygonWerewolf_Texture_01_A.png
surf[1] name=lambert1408 path=…SK_Chr_Werewolf_01.fbx::StandardMaterial3D_ic5we
  albedo_texture = <null>          <-- BY SPEC (Eye_Glow)
```

**By eye** — rendered at the fixed ARPG camera (R-6) and at a close inspection distance:
`tmp/pct12/frames/ww_after_arpg_a.png`, `tmp/pct12/frames/ww_after_close_a.png`. The close frame shows
**red tongue, cream teeth, dark nose, white eye highlight and tonally-varied grey fur** — i.e. the
4096² atlas is genuinely sampling, not merely non-null. Pre-repair this surface was flat monochrome.
Non-null was the necessary test; *this* is the sufficient one.

**Import-log delta:** PC-W1-A recorded **2 ERROR + 1 WARNING**. Post-repair (`tmp/pct12/repair_import.log`)
the `Resource file not found: res://` ERROR is gone; what remains is **1 ERROR + 1 WARNING**, both the
*same* dangling `PolygonFantasyGothic_Texture_01.psd` reference — the FBX still embeds it, Godot still
skips it, and it now has **no consequence** because the material is supplied externally. The dirt that
earned the DIRTY verdict (null albedo) is gone; the cosmetic log line is not repairable without editing
the vendor FBX, which is out of scope.

### 1.4 — What changed in `reincarnated-godot` (TASK 0)

| file | change |
|---|---|
| `Assets/Synty/polygon-werewolf/SourceFiles/Materials/lambert1407.tres` | **CREATED** (10 lines) — Godot-extracted material + one `albedo_texture` line |
| `Assets/Synty/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/SK_Chr_Werewolf_01.fbx.import` | **MODIFIED** — added a 5-line `"materials"` block to `_subresources`. `materials/extract*` and the whole `"nodes"` retarget block are byte-identical to baseline |
| `project.godot` | **F8 fired twice** (pruned `[rendering] mesh_lod/lod_change/threshold_pixels=1.0`). Restored both times; `git diff project.godot` → **empty** |
| `.godot/imported/SK_Chr_Werewolf_01.fbx-*.{scn,md5}` | regenerated. `.godot/` is gitignored — derived cache only |

Baselines for exact reversal kept at `tmp/pct12/SK_Chr_Werewolf_01.fbx.import.baseline` and
`tmp/pct12/project.godot.baseline`. **R-PC-1 honoured: `SK_Chr_Werewolf_Undead_01.fbx` untouched.**

---

## §2 — The Tier-1 instrument (charter check 9) — validated before any row was verdicted

Check 9 asks whether an effect reintroduces a temporal accumulator. **The instrument had to be proven
able to see one first (L-N), and my first attempt was blind.** That is recorded here rather than smoothed.

**Harness:** `tmp/pct12/probe_rig.gd` + `probe_rig.tscn`, run windowed at 1024² via `tmp/pct12/run.sh`.
Fixed ARPG camera **R-6 — dist 34, fov 24, yaw 47, pitch −50, aim_h 1.0** ("the camera is the judge;
you do not move the judge"). Ground plane per R-10. Glow ON at threshold 1.25 (**innocent** per L7-V);
SDFGI **OFF** for row measurement so the environment contributes zero accumulation.

**Operationalisation:** settle N frames → **pause the SceneTree** → capture frame A → wait 12 frames →
capture frame B → framediff. Under pause no simulation advances, so *any* delta is frame-history state.

**Calibration runs (all six, verbatim):**

| control | SDFGI | settle | changed_frac | max Δ | reads |
|---|---|---:|---:|---:|---|
| A — empty stage | off | 90 | **0.000000** | 0.00000 | floor: no false positive |
| A2 — empty stage | off | 4 | **0.000000** | 0.00000 | floor holds at short settle |
| **B2 — empty stage** | **on** | **4** | **0.176617** | **0.00784** | **← instrument SEES the charter's named accumulator** |
| B — empty stage | on | 90 | 0.000000 | 0.00000 | SDFGI has converged by frame 90 |
| C — screen-read quad | off | 90 | 0.000000 | 0.00000 | see boundary below |
| C2 — screen-read quad | off | 1–4 | 0.000000 | 0.00000 | see boundary below |

**Instrument boundary, named not hidden.** My intended second positive control — an opaque quad
sampling `hint_screen_texture` and blending its own previous output — **never fed back at all**:
Godot's screen-texture copy for an *opaque* material is taken before that object's own draw, so the
quad only ever read the static floor behind it (visible in `tmp/pct12/frames/ctrlC2_feedback_short_a.png`
— a flat pink rectangle, not a converging one). It is a mis-built control, not a failed detection.
Consequence: **paused-delta is validated against multi-frame-converging accumulation (SDFGI class) and
is NOT validated against a self-referential feedback loop.**

**So check 9 is decided by two detectors, and LOADS-CLEAN requires both:**
1. **Paused-delta framediff**, run at settle 90 *and* settle 4 (the short settle is where B2 proves
   sensitivity — an accumulator that has already converged by frame 90 is invisible at 90).
2. **Structural accumulator scan** — static grep of everything the row ships for
   `hint_screen_texture` · `SCREEN_TEXTURE` · `hint_depth_texture` · `BackBufferCopy` · `SubViewport` ·
   `sdfgi`, plus a runtime node census for `SubViewport`/`BackBufferCopy`. This catches exactly the
   class detector 1 cannot.

Any hit on either → `LOADS-DIRTY(accumulator: <what>)`.

---

## §3 — TASK 1: Tier 1, pure-resource rows

**Scope taken:** Layer-1 rows that ship no compiled binary. Licence-clean rows were installed and
measured; rows the menu marks unlicensed were **not installed**. **One row re-tiered:** row 12
(Vaportrail) ships a `.gdextension` + compiled framework, so it is measured in §4 (Tier 2), not here.

**Version pins — all re-read 2026-07-28, all UNCHANGED since the menu's 2026-07-26 read** (L-C
satisfied; nothing drifted under us). The four Asset-Library `download_commit` SHAs match the menu
character-for-character; the four release tags match date and version.

### 3.0 — Verdicts

| # | Row | Verdict | Earned by |
|---|---|---|---|
| 1 | Compositor Lens Effects | **LOADS-CLEAN** | §3.1 |
| 2 | GODOT-VFX-LIBRARY | **LOADS-DIRTY(uid-duplicate + screen-read shader)** · and **REACHES-NOT(3D surface)** | §3.2 |
| 3 | Godot Projectile Engine | **LOADS-DIRTY(requires-plugin-enable; autoload registers by UID)** · and **REACHES-NOT(3D surface)** | §3.3 |
| 5 | godot-4-VFX-assets (GDQuest) | **EXCLUDED(licence)** | §3.8 |
| 6 | Godot-particle-and-vfx-textures | **LOADS-DIRTY(blend-source-blocks-the-import-pass)** | §3.4 |
| 7 | proton_trail | **LOADS-DIRTY(class_name collision `Point`)** | §3.5 |
| 10 | TrailRenderer | **LOADS-DIRTY(C# samples unloadable on STANDARD build; exports `class_name Point` into the global namespace)** | §3.6 |
| 11 | UniParticles3D | **LOADS-CLEAN** | §3.7 |
| 19 | Godot4-OpenAnimationLibraries | **EXCLUDED(licence)** | §3.8 |
| 20 | GodotHumanoidRetargetPlugin | **EXCLUDED(licence)** | §3.8 |
| 27 | synty-godot-converter | **EXCLUDED(licence)** | §3.8 |
| 4 | Godot Shaders Library | **NOT MEASURED — out of tier** (editor-only ⇒ charter Tier 3). Not installed; **R-PC-5 network fence intact and never tested against**. §3.9 |

### 3.1 — Row 1 · Compositor Lens Effects (AL 5292, `ff8fb933`, MIT) — **LOADS-CLEAN**

`lens_flare_compositor_effect.gd` and `base_compositor_effect.gd` both compile; the effect
**instantiates as a real `CompositorEffect`** and attaches to a `Compositor`:

```
instantiated: CompositorEffect  is CompositorEffect: true
attached to Compositor: effects=1
glsl present: true
```

Structural accumulator scan: **CLEAN** (no screen/depth-texture read, no `BackBufferCopy`, no
`SubViewport`, no `sdfgi` in the addon or its `lens_flares.glsl`). Evidence `tmp/pct12/rowprobe2.log`.
*Honest limit:* this row has no shippable `.tscn`, so it did not go through the paused-delta framediff —
its check-9 answer rests on the structural detector alone.

### 3.2 — Row 2 · GODOT-VFX-LIBRARY (v1.0.0, MIT) — the menu's headline row, and the cell's headline finding

**Accumulator: clean.** All **32** effect scenes measured, at settle 90 **and** settle 4:
**0 nonzero paused-deltas, 32/32, both legs** (`tmp/pct12/frames/row02_settle90_batch.json`,
`row02_settle4_batch.json`). `accumulator_nodes` empty on every one.

**But the row does not reach the 3D surface, and that is categorical rather than marginal.** Runtime
node census over all 32 scenes plus a static type scan of the whole addon:

```
34 CPUParticles2D · 1 GPUParticles2D · 2 Sprite2D · 2 Node2D · 1 Camera2D
 1 StaticBody2D · 1 CollisionShape2D · 1 CanvasLayer · 18 CanvasItemMaterial
```

- **Zero `*3D` node types anywhere in the addon** (`grep -rho 'type="[A-Za-z0-9]*3D"' addons/vfx_library/` → no matches)
- **24 / 24 shaders are `shader_type canvas_item`. Zero `shader_type spatial`.**

Instantiated at the fixed ARPG camera, a `CanvasItem` does not enter the world — it draws in canvas
space. `tmp/pct12/frames/row02_settle90_magic_aura.png` shows it: a **hard-pixel smear pinned to the
top-left canvas origin**, with no relationship to the camera, the floor, or the scene. I looked at it.

The menu calls this row *"the single highest-leverage L7 row"* on the reasoning that a `.tscn` effect is
equally loadable by all three cells. **The loadability premise is correct and the conclusion does not
follow** — all three cells would equally load an effect that cannot appear in a 3D scene. Verdict
**`REACHES-NOT(3D surface — 0/32 effects contain any Node3D; 0/24 shaders are spatial)`**.

**Dirt, separately:** (a) the pack ships a **UID duplicate** between `effects/vfx_test.tscn` and
`demo/vfx_demo.tscn` — warned on every project import from now on; (b) `shaders/water.gdshader` line 15
declares `uniform sampler2D SCREEN_TEXTURE: hint_screen_texture;` and samples it at line 51 — a genuine
**screen-reading construct**, exactly the class the paused-delta detector cannot see (§2). No effect
scene uses it, but it is in the pack.

### 3.3 — Row 3 · Godot Projectile Engine (AL `53d9150a`, MIT) — **LOADS-DIRTY** + **REACHES-NOT**

First pass recorded `LOAD-NULL` on `example_1_first_pattern.tscn` with 25× `Parse Error: Identifier
"ProjectileEngine" not declared in the current scope`. **That was my install being incomplete, not the
row failing** — the row registers an autoload from its `EditorPlugin._enter_tree()`
(`plugin.gd:7: add_autoload_singleton("ProjectileEngine", …)`). With the plugin enabled in
`project.godot` and a re-import, the autoload registers and the core script compiles:
`row03 ProjectileEngine exists=true script=OK instantiable=true`. Recorded because an unenabled
install would have produced a false FAILS-LOAD (L-N).

**Dirt:** the autoload is written as `ProjectileEngine="*uid://bcvs3q3df6ql6"`, and that UID **does not
resolve** in a `--script` context — `ERROR: Unrecognized UID: "uid://bcvs3q3df6ql6"` on every headless
run. Any headless harness using this row eats that error.

**Reach:** the row is **2D-only** — `Area2D`, `Camera2D`, `CircleShape2D`, `CollisionShape2D`, `Node2D`,
`Sprite2D`, and **zero `*3D` types anywhere in the addon**. `example_6_homing.tscn` instantiates cleanly
and its census is `Camera2D:1, Node2D:6, Node:4, AudioStreamPlayer:1`. The menu lists it under
**L7 cast** with `EW=ALL`. It cannot cast anything into a 3D scene. **`REACHES-NOT(3D surface)`.**

**Accumulator: clean** (paused-delta 0 at settle 90 and 4; structural scan CLEAN).

### 3.4 — Row 6 · Godot-particle-and-vfx-textures (RPicster, CC0) — **LOADS-DIRTY(blend-source-blocks-the-import-pass)**

The textures themselves are fine. **The pack as shipped prevents them from ever being imported.**

`materials/blend_file/` contains `particles.blend` and `light_texture.blend`. Godot's `.blend` importer
requires a configured Blender install, and in its absence emits
`ERROR: Blender path is invalid or not set … Cannot configure blender path in headless mode`
(`editor_scene_importer_blend.cpp:519`) — which **aborts the import pass**. Measured both ways, same
project, same command:

| configuration | `.png.import` sidecars generated | Blender ERROR |
|---|---:|---:|
| pack installed as shipped | **0 / 134** | 1 |
| `materials/blend_file/` excluded | **134 / 134** | 0 |

With the `.blend` present, `load()` on any of its textures returns
`ERROR: No loader found for resource … (expected type: unknown)`. This is not a texture defect — it is a
**whole-project import-pass defect** that the row introduces, and it would have silently degraded every
later cell in this project.

**Installed configuration:** textures + materials **excluding** `materials/blend_file/`, which is parked
at `Assets/ThirdParty/rpicster-vfx-textures/_excluded_blend_source/blend_file/` behind a `.gdignore`.
Nothing is deleted; the files are preserved and Godot skips them. Post-exclusion: **134/134 sidecars,
0 Blender errors, 82/82 textures under `textures/` load** at 64², 224², 256², 448², 768×256, 896²,
1024² and 32×128. Structural scan **CLEAN**.

### 3.5 — Row 7 · proton_trail (MIT) — **LOADS-DIRTY(class_name collision)**

Genuinely 3D (`Node3D`, `MeshInstance3D`, `Camera3D`, `Marker3D`), and the demo scene instantiates.
But co-installed with row 10 it emits, on every load:

```
SCRIPT ERROR: Parse Error: Class "Point" hides a global script class.
   at: GDScript::reload (res://addons/proton_trail/proton_trail.gd:54)
```

`proton_trail.gd:54` declares an **inner** `class Point:`; row 10 declares a **global**
`class_name Point` (`addons/TrailRenderer/Runtime/GD/point.gd:1`). **The two rows are mutually
interfering as shipped.** Isolation measurement: with `addons/TrailRenderer` parked, `demo_trail.tscn`
loads and the collision error count drops — see §3.6 for where the fault properly sits.

**A near-miss worth recording (L-N).** On the first isolation pass the demo scene reported
`"load":"OK"` *while the collision error was still in the log* — Godot's cached global class registry
still held `Point`, the script silently failed, and the scene loaded with its script dropped. A scene
can "load" with its payload script missing. I only caught it by testing script compilation **directly**
(`tmp/pct12/scriptprobe.gd`) rather than trusting the scene-load result. Any cell that verdicts a
GDScript row on `instantiate() != null` alone is at risk of the same false CLEAN.

**Accumulator: clean** (paused-delta 0 both legs; structural scan CLEAN).

### 3.6 — Row 10 · TrailRenderer (Hyrdaboo, MIT) — **LOADS-DIRTY**, two distinct defects

1. **The samples are C# and this is the STANDARD (non-Mono) Godot build.** Both sample scenes returned
   `LOAD-NULL`: `sword_demo.tscn` line 4 references
   `res://addons/TrailRenderer/Samples/Scripts/HandController.cs`. **5 `.cs` files ship.** They cannot
   load here, ever, without switching to a Mono build. The **GDScript runtime under `Runtime/GD/` is
   fine** — `trail_renderer.gd` and `line_renderer.gd` compile and `TrailRenderer.new()` instantiates
   as a `Node3D`. So the row's *capability* is present and its *demos* are not.
2. **It publishes `class_name Point` into the global namespace** — an extremely generic name for a
   third-party addon to claim, and it is what breaks row 7 (§3.5). The fault sits here, not with
   proton_trail: an inner class is private, a global `class_name` is a landgrab.

**Accumulator: clean** (paused-delta 0 both legs; structural scan CLEAN).

### 3.7 — Row 11 · UniParticles3D (AL `7b23c222`, MIT) — **LOADS-CLEAN**

`class_name UniParticles3D extends Node3D` compiles and instantiates as a `Node3D`; **10/10 shaders are
`shader_type spatial`**; `uniparticle_preview.tscn` (an editor `Control` dock) instantiates. This row
**does** reach the 3D surface — the contrast with rows 2 and 3 is stark and it is the same "L7 particle
library" brief. Paused-delta 0 at settle 90 and 4.

Structural scan flagged `plugin.gd:95–97`, which is a **false positive** — the string
`"SubViewportContainer"` appears in an editor-dock class-name comparison, not a render path. Named so
the scan's output is not over-read.

**Watch item, not a defect:** it declares `class_name YParticlesInspectorPlugin` — the same author's
YParticles3D (row 14) is the sibling product, and the menu notes row 11 is "superseded by YParticles3D
(same author)". Row 14 fails to load (§4.2), so no collision materialised **this run**; if row 14 is
ever repaired, that collision is the first thing to re-check.

### 3.8 — EXCLUDED(licence) — 4 rows, **not installed, not downloaded, not executed**

Per the charter §5 folded lean (bulk-install CLEAN+licensed; unlicensed rows verdict `EXCLUDED(licence)`
unless Matt rules otherwise):

| # | Row | Licence field | Verdict |
|---|---|---|---|
| 5 | godot-4-VFX-assets (GDQuest) | MIT code / **CC-BY-NC-SA-4.0 art** | `EXCLUDED(licence)` — non-commercial art in a project with shipping ambitions; the menu itself lists it **reference-only** (§2.7) |
| 19 | Godot4-OpenAnimationLibraries | **NONE** | `EXCLUDED(licence)` — no licence = all rights reserved |
| 20 | GodotHumanoidRetargetPlugin | **NONE** | `EXCLUDED(licence)` |
| 27 | synty-godot-converter | **NONE** | `EXCLUDED(licence)` |

**A menu-internal discrepancy for the conductor:** menu §0 states *"Five rows have no license at all"*;
menu §5 names **three** (19, 20, 27). Only row 40 (`godot-mcp-pro extension mechanism`, which "DOES NOT
EXIST") carries a further blank licence field, making four at most. The charter §5 lean says "the 4
named exceptions + **5 unlicensed rows**". **I could not reconcile 5.** I have excluded the three
unlicensed Layer-1 rows plus row 5 on its NC-art clause, and I am naming the count mismatch rather than
picking a number.

### 3.9 — Row 4 · Godot Shaders Library — **NOT MEASURED, and the fence was never approached**

The cell brief raises R-PC-5 under Tier 1, but this row is **editor-only** (`EW=WIRE`, an in-editor
browser dock), which the charter §3 assigns to **Tier 3**. I did not install it, did not download it,
and **nothing in this cell made any request to godotshaders.com**. Every measurement in §3 and §4 ran
against locally-staged files. The R-PC-5 network-quiet fence is intact and unspent; the row carries
forward to Tier 3 with its `LOADS-DIRTY(network-by-design)` annotation still owed.

---

## §4 — TASK 2: Tier 2, runtime GDExtensions

**Rows measured:** 14 (YParticles3D), 21 (GodotIK), and **12 (Vaportrail — re-tiered from Tier 1**; the
menu classes it as a pure runtime node, but it ships `vaportrail.gdextension` and a compiled
`.framework`).

### 4.0 — `lipo -info`: **all three ship arm64. Architecture is not the problem.**

| # | Row | macOS binary | `lipo -info` |
|---|---|---|---|
| 14 | YParticles3D | `…editor.single.framework/libyparticles3d.macos.editor.single` | `x86_64 arm64` |
| 14 | YParticles3D | `…template_release.single.framework/…template_release.single` | `x86_64 arm64` |
| 12 | Vaportrail | `bin/macos/macos.framework/libvaportrail.macos.template_debug` | `x86_64 arm64` |
| 12 | Vaportrail | `bin/macos/macos.framework/libvaportrail.macos.template_release` | `x86_64 arm64` |
| 21 | GodotIK | `bin/libik.dylib` | `x86_64 arm64` |

`compatibility_minimum`: YParticles3D **4.5** · GodotIK **4.3** · Vaportrail **4.1** — all ≤ our 4.6.3.
**Menu check-7 answered: yes, the arm64 slices exist.** Two rows still fail, for a different reason.

### 4.1 — Row 21 · GodotIK (v1.3.1, MIT) — **LOADS-CLEAN**, and it is the L-N control

A successful GDExtension load is silent, so the decidable assertion is ClassDB registration:

```
row21 GodotIK -> GodotIK(parent=SkeletonModifier3D, instantiable=true),
                 GodotIKEffector(parent=Node3D, instantiable=true),
                 GodotIKConstraint(parent=Node, instantiable=true),
                 GodotIKRoot(parent=Node3D, instantiable=true)
```

**4/4 declared classes register and instantiate on Godot 4.6.3 / arm64**, and `GodotIK` derives from the
engine's native `SkeletonModifier3D` — i.e. it composes with the 4.4+ modifier stack the menu §5 notes
absorbed RenIK's territory. Zero errors attributable to this row in the import log.

**This row is the control that earns the two FAILS-LOAD verdicts below** (L-N): the GDExtension load
path on this stack is demonstrably working, in the same process, on the same run.

### 4.2 — Row 14 · YParticles3D (1.0, Unlicense) — **FAILS-LOAD(declared macOS debug slice is not in the shipped archive)**

```
ERROR: Can't open dynamic library: …/addons/yparticles3d/./bin/macos/libyparticles3d.macos.template_debug.single.framework
       … (no such file) [×6 search paths]
ERROR: Can't open GDExtension dynamic library: 'res://addons/yparticles3d/yparticles3d.gdextension'.
   at: open_library (core/extension/gdextension.cpp:741)
```

The manifest declares:
```
macos.debug   = "./bin/macos/libyparticles3d.macos.template_debug.single.framework"
macos.release = "./bin/macos/libyparticles3d.macos.template_release.single.framework"
```
The archive ships **`…editor.single.framework`** and **`…template_release.single.framework`** — and
**no `template_debug` at all**. Every editor run and every `--script` run is a debug context, so Godot
asks for the one slice that isn't there. `ClassDB.class_exists("YParticles3D")` → **false**.

**This is a packaging defect, not an architecture defect** — and the distinction matters, because
`lipo` alone would have passed this row. The `macos.release` slice does ship, so an exported release
build would presumably load it; nothing in our harness is a release build.

### 4.3 — Row 12 · Vaportrail (v0.9, MIT) — **FAILS-LOAD(manifest path ≠ shipped path)**

```
ERROR: Can't open dynamic library: …/addons/vaportrail/bin/macos/libvaportrail.macos.template_debug.framework
       … (no such file)
ERROR: Can't open GDExtension dynamic library: 'res://addons/vaportrail/vaportrail.gdextension'.
```

Manifest: `macos.debug = "bin/macos/libvaportrail.macos.template_debug.framework"`.
Archive: `bin/macos/**macos.framework**/libvaportrail.macos.template_debug`.
**The framework bundle is named `macos.framework`, not `libvaportrail.macos.template_debug.framework`.**
`ClassDB.class_exists("VaporTrail")` → **false**. Same class of defect as row 14: correct architecture,
wrong path. (Separately: the *source* repo at tag `v0.9` ships `bin/.gitignore` and **no binaries at
all** — only the release ZIP carries them, so a clone-based install cannot work either.)

Both failures are trivially recoverable by relocating a file. **I did not relocate anything** — that is
repair beyond this cell's scope and it is the conductor's call whether a repaired re-test is wanted
before the race.

---

## §5 — Exactly what changed in `reincarnated-godot` (nothing committed there)

**No commit was made in `reincarnated-godot`.** `git status --porcelain` shows **zero tracked-file
modifications**; `git diff project.godot` is **empty**.

**Created (TASK 0 — inside gitignored `/Assets/Synty/`):**
- `Assets/Synty/polygon-werewolf/SourceFiles/Materials/lambert1407.tres`

**Modified (TASK 0 — inside gitignored `/Assets/Synty/`):**
- `Assets/Synty/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/SK_Chr_Werewolf_01.fbx.import`
  (+5-line `"materials"` block in `_subresources`; baseline at `tmp/pct12/SK_Chr_Werewolf_01.fbx.import.baseline`)

**Created (TASK 1/2 — new untracked addon trees):**
- `addons/lens_effects/` · `addons/vfx_library/` · `addons/godot_projectile_engine/` ·
  `addons/proton_trail/` · `addons/TrailRenderer/` · `addons/UniParticles3D/` ·
  `addons/yparticles3d/` · `addons/libik/` · `addons/vaportrail/`
- `Assets/ThirdParty/rpicster-vfx-textures/` (textures + materials + LICENSE, **plus 134 `.png.import`
  sidecars generated by Godot**, plus `_excluded_blend_source/blend_file/` behind a `.gdignore` — §3.4)

**Created (evidence, untracked):** `tmp/pct12/` — `matprobe2.gd`, `slotid.gd`, `probe_rig.gd/.tscn`,
`batch_rig.gd/.tscn`, `rowprobe.gd`, `scriptprobe.gd`, `extprobe.gd`, `run.sh`, `batch.sh`, all `.log`
files, `frames/` (per-row PNGs + `*_batch.json`), and the two baselines.

**Touched and restored:**
- `project.godot` — **F8 fired on every one of the ~8 headless import passes**, each time pruning
  `[rendering] mesh_lod/lod_change/threshold_pixels=1.0`. Restored every time; **final state clean**.
  I also temporarily added row 3's plugin to `[editor_plugins]` to measure it (§3.3) and reverted that;
  **`project.godot` is byte-identical to `HEAD`.**
- `addons/TrailRenderer/` — parked to `/tmp` for one isolation measurement (§3.5), **restored**.

**Not touched:** `SK_Chr_Werewolf_Undead_01.fbx` (R-PC-1 honoured — not loaded, not instantiated, not
reimported). `~/Games/mcp-lab/`. Any Murzak/Pro row (Tier 4, `GATED-Q46`).

**Left enabled/disabled:** no third-party `EditorPlugin` is enabled in `project.godot`. Rows that need
enabling to function (row 3) are installed-but-inert. That is a deliberate hands-off choice on shared
state, not an oversight — flagged in §6.

---

## §6 — Findings logged for the conductor (NOT acted on)

| # | Finding | Evidence |
|---|---|---|
| **G1** | **The menu's headline L7 row is 2D.** GODOT-VFX-LIBRARY has zero `Node3D` and zero spatial shaders; at the fixed ARPG camera its effects draw as a screen-space smear at the canvas origin. Row 3 (Godot Projectile Engine, "L7 cast", `EW=ALL`) is likewise 2D-only. **Two of the eight Tier-1 rows cannot reach the L7 surface at all** — and both are marked `EW=ALL` in the menu, because loadability was read as reach. | §3.2, §3.3 |
| **G2** | **`lipo` is necessary and not sufficient.** All three GDExtensions ship arm64; two still fail, both on **packaging** (a declared macOS debug slice that isn't in the archive; a framework bundle whose name doesn't match the manifest). A check-7 that stopped at `lipo` would have passed both. | §4.0–4.3 |
| **G3** | **Rows 7 and 10 are mutually interfering as shipped.** TrailRenderer publishes `class_name Point` globally; proton_trail has an inner `class Point`. Installing both breaks proton_trail's script on every load. Generic global `class_name`s from third-party addons are a standing hazard for a project installing many rows at once. | §3.5, §3.6 |
| **G4** | **A row can break the whole project's import pass.** Row 6's two `.blend` source files abort the import pass on a Blender-less machine: **0/134** textures import with them present, **134/134** without. Any later cell that had installed row 6 as shipped would have silently lost all its textures. | §3.4 |
| **G5** | **Row 10's samples are C# and this is the STANDARD build.** 5 `.cs` files; both sample scenes `LOAD-NULL`. The GDScript runtime is unaffected. Any menu row shipping C# has this constraint and the menu does not carry a "language" column. | §3.6 |
| **G6** | **A scene can load with its script silently dropped.** `demo_trail.tscn` reported `"load":"OK"` while its root script was failing to parse from a cached global-class collision. Scene-instantiation success is **not** evidence a GDScript row works; script compilation must be asserted directly. Recommend this become a standing method note for Tier 3. | §3.5 |
| **G7** | **The check-9 paused-delta instrument has a named blind spot.** It detects multi-frame-converging accumulation (SDFGI class, validated: 0.177 changed-frac at settle 4). It cannot detect a self-referential feedback loop that converges within a few frames. Compensated here with a structural scan — which found a real `hint_screen_texture` shader in row 2 that the framediff read as clean. | §2, §3.2 |
| **G8** | **F8 is worse than "occasional".** `godot --headless --import` pruned `[rendering] mesh_lod/lod_change/threshold_pixels=1.0` from `project.godot` on **every single pass** this cell ran (~8). It is deterministic, not intermittent. Recommend a standing guard (`git checkout project.godot` after every headless import) for all remaining cells. | §5 |
| **G9** | **Row 3 registers its autoload by UID** (`ProjectileEngine="*uid://bcvs3q3df6ql6"`), which does not resolve under `--script`: `ERROR: Unrecognized UID` on every headless run. Also: the row is inert until its EditorPlugin is enabled, which is shared-`project.godot` state — a fairness question for L-H if only some arms enable it. | §3.3 |
| **G10** | **Menu count mismatch, unreconciled.** Menu §0 says five rows have no licence; menu §5 names three. Charter §5 says "the 4 named exceptions + 5 unlicensed rows". I excluded four rows and could not make the count reach five. | §3.8 |
| **G11** | **Row 11 and row 14 both declare `class_name YParticlesInspectorPlugin`** (same author). No collision materialised because row 14 fails to load. If row 14 is ever repaired, re-check this first. | §3.7 |
| **G12** | Row 2 ships a **UID duplicate** (`effects/vfx_test.tscn` vs `demo/vfx_demo.tscn`) which will warn on every project import from now on, adding to the four pre-existing duplicates PC-W1-A logged as F7. | §3.2 |


---

## §7 — Cell exit

| brief item | status |
|---|---|
| TASK 0 — re-wire albedo to the pack's own 4096² PNG, re-import (F9), verify, re-verdict | ✅ **LOADS-CLEAN(albedo-repaired)** — verified numerically and **by eye** (§1.3). One correction: the pack spec puts **1 of 2** materials under a texture, not 2 (§1.1) |
| TASK 0 — minimal diff, listed | ✅ 1 file created, 1 file modified, both inside gitignored `/Assets/Synty/` (§1.4, §5) |
| TASK 1 — Tier-1 pure-resource rows installed, instantiated at the fixed ARPG camera, double-render + framediff | ✅ 8 rows installed + 4 `EXCLUDED(licence)` uninstalled; 38 scenes measured on **two** settle legs (§3) |
| TASK 1 — check 9 (SDFGI is the accumulator, glow is innocent) | ✅ instrument calibrated in both directions **before** any verdict, blind spot named, second detector added (§2) |
| TASK 1 — R-PC-5 network fence | ✅ **never approached** — row 4 is editor-only ⇒ Tier 3, not installed, zero requests to godotshaders.com from this cell (§3.9) |
| TASK 2 — `lipo -info` → headless load → assert extension-load line | ✅ 3 rows; arm64 confirmed on all 3; **1 LOADS-CLEAN, 2 FAILS-LOAD** on packaging, not architecture (§4) |
| TASK 2 — L-N: prove the load path before recording FAILS-LOAD | ✅ GodotIK registers 4/4 classes in the same process — the control is inside the measurement (§4.1) |
| OUTPUT — incremental write, committed in the collaboration repo | ✅ created at cell start, committed after TASK 0, completed at exit |
| `reincarnated-godot` — every changed/created file listed, nothing committed there | ✅ §5. `git status` shows **zero tracked modifications**; `project.godot` byte-identical to HEAD |

**Boundary held:** LOADS?/REACHES?, never BETTER. No row was ranked, no row was repaired, no judgement
was offered on which effect looks better. Where a row was mis-tiered (12) or mis-classified (2, 3) I
report the measurement and leave the menu's amendment to legolas's seam.

---

**Signed:** drax (presentation seam), 2026-07-28.
Evidence root: `/Users/admin/Games/reincarnated-godot/tmp/pct12/`
