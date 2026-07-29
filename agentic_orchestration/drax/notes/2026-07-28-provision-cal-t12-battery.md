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

*(filled at exit)*

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

*(in progress)*
