# The sorceress: scene package (`?c=sorceress`)

**v2 (2026-09-30).** Every clip is now on its Meshy source's own keys, the release times are re-derived, and the walk and run speeds come from the scene's stance rule. Numbers below are v2's; `make_pkg.py` reads the v2 kit and pack index. Re-import the package; nothing else changed in its shape.

This is her slot for the painted Barrow phone page, in the scene's own shapes. It was built from D7's export and tested outside the scene. Nothing in `barrow_full/` or `cliffside3d/` was touched.

## What goes where

| This package | Install as | Read by |
|---|---|---|
| `so_d7/export/so-body.glb` | `res://models/sorceress/so-body.glb` (the `model`) | knight.gd |
| `so_d7/export/{robe,mantle,belt,bracers,circlet,staff}.glb` | `res://models/sorceress/` (the `gear_dir`) | gear.gd (each is skinned on her 26 joints) |
| `gear_manifest_sorceress.json` | `res://data/gear_manifest_sorceress.json` | gear.gd reads `pieces`; knight.gd reads `locomotion_in_place` |
| `character_sorceress.json` | her character slot (the same shape as `character.json`) | knight.gd |
| `sockets_sorceress.json` | the placeholder VFX | new code (see what knight.gd lacks, item 3) |

**Regenerate, don't edit.** After any re-export, run `python3 scene_pkg/make_pkg.py` from `so_d7/`. Every number in these files is read from her export manifest, the JOIN-1 kit's sockets or the sprite pack's measured height.

## Roles

| Role | Clip |
|---|---|
| idle | `idle` |
| walk | `walk` |
| run | `run` |
| attack (the slash key) | `cast_fireball` |
| chop | `cast_meteor` |

`hit` and `death` have no role in knight.gd. They are listed under `roles_knight_lacks`.

## The staff layers, in knight.gd's terms

`grip_R = 1` is set through `morph_rules` (`staff`).

| State | Wanted | As written | Result (scratch test, staff tilt max / vs `staff_layer.gd`) |
|---|---|---|---|
| walk | the 9-bone carry | `upper_armed` holds the spine (Spine02, Spine01, Spine, neck, Head) from `staff_carry_R`; `arm_layer_armed_R` holds the carry on the staff arm | 6.04 deg, **identical** |
| run | the 9-bone carry | same as walk | 13.39 deg, **identical** |
| idle | the 9-bone carry | same slots | 11.99 deg (designed 10.81), 5.8 deg off: the idle's own spine sway (knight.gd's upper chain plays the idle role clip in idle) |
| Fire Ball | carry on the staff arm only | `strike_release`: pose `staff_carry_R`, the 4 arm bones, `guard_throughout: [cast_fireball]` | 23.99 deg, **identical** |
| Meteor | none | not listed, so the strike owns every bone (its staff motion is baked into weapon_r) | 114.24 deg, **identical** |
| hit | chest_arm | **not expressible** | 87.06 deg raw (designed 8.27) |
| death | none (she falls with it) | **no role** | 107.69 deg (as designed) |

**Why `upper_armed` holds the spine.** The carry keeps Spine01, Spine, neck and Head at rest, and Godot's glTF import drops rest-valued tracks, so `staff_carry_R` arrives with 8 tracks for its 9 bones. `arm_layer_armed_R` takes its filter from the action's own tracks, so it cannot hold the upper spine: on its own it let the run's spine carry the staff to 32 deg. `_apply_upper` takes its filter from the locomotion clips, which is why it can hold the spine.

**`arm_layer_armed`** is the left slot. Its action is `staff_carry_R` with an empty filter. It is there only because `_build_anim_tree` builds no tree at all without it.

## What knight.gd lacks

1. **hit.** It has no hit role and no one-shot fired by the model's hit-recovery event. It also has no per-strike release bones: `strike_release.bones` is one list for every strike, and chest_arm needs Spine02 plus the arm while the Fire Ball needs the arm alone.
2. **death.** It has no role, and no one-shot that holds its last frame.
3. **A release event.** Nothing fires when a strike's position crosses `casts.<clip>.release_s`: Fire Ball 0.9333 s, Meteor 1.6333 s (v2). `strike_release.at_s` is the recovery release, which is a different thing. The placeholder VFX needs this event, at `cast_hand` for the Fire Ball and `cast_hand_meteor` for the Meteor.
4. **(Worked around) filter paths from the layered-over clips.** Taking them only from the action's own tracks is what forced the `upper_armed` route above.

## Numbers to check at launch

- **Height:** 1.6995 m in the model. At his world factor x1.25178 she stands 2.127 m (he stands 2.316 m).
- **knight.gd prints:** `ARMED`; a sync group of walk **0.9667 s** / run **0.7333 s** at **151.7 / 463.2 px/s** at the reference scale, times `figure_scale / 1.25178` live; `upper layer: ON | walk 'staff_carry_R'`; `strike release: pose 'staff_carry_R' ... guard throughout ["cast_fireball"]`.
- **Speeds:** walk **1.508 m/s** and run **4.604 m/s** (v2). These are foot-lock speeds by the scene's own stance rule (the stance side is the lower toe, and the speed is that side's foot joint), measured at the clips' own keys. They are the numbers the integration drax's feet test reads as grip. v1's walk 1.471 and run 3.986 came from a bottom-25%-of-the-ankle rule; that rule read the run 15% slow, which is why it skated at 1.148.
- **Release (v2):** the Fire Ball's left palm at 0.9333 s is at (0.066, 1.106, 0.804) m in model space. The Meteor's right palm at 1.6333 s is at (-0.272, 1.007, 0.686). Both are re-derived on the re-cut clips' own keys. v1's 0.9167 and 1.625 were one 24 fps frame early on v1's own clips.
- **Staff tilt:** the table above, per state.

## The test

`test/` is a scratch copy of the film project: `project.godot`, `staff_layer.gd` and `pkg_test.gd`, loading the export at runtime so nothing is imported. It is not the 2.3 GB film folder.

It builds her tree the way knight.gd builds it, from `character_sorceress.json`. It runs `staff_layer.gd` beside it and compares weapon_r every 1/30 s.

Results are in `test_result.json` and `test/pkg_test.log.txt`. To run it:

```
PKG=<so_d7>/scene_pkg EXP=<so_d7>/export OUT=result.json godot --headless --path test res://pkg_test.tscn
```

`staff_layer.gd` needs to sit beside `pkg_test.gd`: copy it from `so_d7/film/`.
