#!/usr/bin/env python3
"""C-9 R-C9-61 (T3): make the Meshy rigged knight shippable as a REAL-TIME character.

    /Applications/Blender.app/Contents/MacOS/Blender --background \
        --python tools/build_knight3d.py

Meshy hands back one 10.5 MB GLB PER CLIP -- rigged / idle / walk / run / attack --
each carrying a full copy of the same 115,345-triangle mesh and the same 2048x2048
texture, for a total of 52 MB to deliver four animations.  Shipping that as-is would
roughly double the web route's payload (keeper.pck is 31 MB) to show one test figure.

So this does four things, and all four are measured rather than assumed:

  MERGE      one armature, one mesh, four animations.  The five files share an
             identical 24-bone rig, so an action from one plays on another's armature
             unchanged -- actions address bones by NAME, and the names match.  Each
             lands on its own NLA track so the exporter emits it as its own clip.

  DECIMATE   115,345 -> ~18,000 triangles.  The figure is composited into a 512x512
             cell in a 2D scene; at that size the extra 97,000 triangles are not
             visible, they are just payload.  Collapse-decimate carries the vertex
             groups, so the skinning survives.

  SHADE SMOOTH   not cosmetic: the ink line is an INVERTED HULL, which pushes each
             vertex along its normal.  Split normals would tear that hull open at
             every shading seam.  Smoothing is free here because the base pass is
             UNLIT -- normals do not reach the lit result at all, so the only thing
             this changes is whether the outline is watertight.

  SHRINK TEX 2048x2048 -> 1024 (knight) / 512 (pollaxe), PNG -> JPEG.  The knight's
             texture is RGB with no alpha channel (checked, not presumed), so JPEG
             loses nothing that is being used.

The pollaxe stays a SEPARATE mesh, which is what makes it attachable to a hand bone.

Writes godot/models/knight_t3.glb, godot/models/pollaxe_t3.glb, and
tools/knight3d_build.json -- the measurements the runtime needs (figure height, sole
height, hand-bone rest position) so the camera and the weapon mount are derived from
this build instead of being typed in twice.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

RUN = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
SRC = os.path.join(RUN, "meshy_t1")
PROJ = os.path.join(RUN, "chartest", "godot")
OUT = os.path.join(PROJ, "models")
TOOLS = os.path.join(RUN, "chartest", "tools")

TARGET_TRIS = 18000
POLLAXE_TRIS = 4000
KNIGHT_TEX = 1024
POLLAXE_TEX = 512

# Which file each clip comes from, and what the game calls it.  attack.glb ships two
# actions -- the 3.03 s 'retarget_clip' is the swing; 'clip0' is the same 0.07 s stub
# rigged.glb carries -- so the clip is named explicitly rather than taken by position.
#
# TWO SETS, because the weapon decides which locomotion is right:
#   k_*  Meshy's MOTION LIBRARY -- generic human locomotion, both arms swinging free.
#        Correct for the knight with no weapon; a haft welded to that wrist windmills.
#   c_*  Meshy TEXT-TO-MOTION carry clips, same rig, right hand up at chest for a
#        polearm. Correct for the knight carrying the pollaxe.
# The attack exists only once, so it serves both.
CLIPS = [
    ("k_idle", "idle.glb", "Armature|Idle|baselayer"),
    ("k_walk", "walk.glb", "Armature|walking_man|baselayer"),
    ("k_run", "run.glb", "Armature|running|baselayer"),
    ("k_attack", "attack.glb", "retarget_clip"),
    ("c_idle", "carry_idle.glb", "retarget_clip"),
    ("c_walk", "carry_walk.glb", "retarget_clip"),
    ("c_run", "carry_run.glb", "retarget_clip"),
]


def wipe():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def imp(path):
    """Import a GLB and return (armature, [meshes]) of just what it added."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    added = [o for o in bpy.data.objects if o not in before]
    arm = next((o for o in added if o.type == "ARMATURE"), None)
    meshes = [o for o in added if o.type == "MESH"]
    return arm, meshes, added


def tri_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def decimate(ob, target):
    n = tri_count(ob)
    if n <= target:
        return n, 1.0
    ratio = target / float(n)
    bpy.context.view_layer.objects.active = ob
    m = ob.modifiers.new("dec", "DECIMATE")
    m.decimate_type = "COLLAPSE"
    m.ratio = ratio
    m.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=m.name)
    return tri_count(ob), ratio


def base_image(ob):
    """The base-colour image actually feeding this mesh's material.

    Meshy writes the colour map into BOTH baseColorTexture and emissiveTexture; the
    importer therefore leaves two image nodes on the graph.  Picking 'the first image'
    would be a coin toss between two names for one map, so take the image wired to
    Base Color and fall back to Emission only if that socket is bare.
    """
    mat = ob.data.materials[0]
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    for socket in ("Base Color", "Emission Color"):
        if bsdf is None or socket not in bsdf.inputs:
            continue
        links = bsdf.inputs[socket].links
        if links and links[0].from_node.type == "TEX_IMAGE":
            return links[0].from_node.image
    return next((n.image for n in nt.nodes if n.type == "TEX_IMAGE" and n.image), None)


def flatten_material(ob, img, name):
    """Replace Meshy's emissive+specular material with base-colour-only.

    Godot's importer maps this to a StandardMaterial3D whose albedo_texture is the one
    map, which is all the runtime wants -- it overrides the shading to unlit anyway.
    Leaving Meshy's KHR_materials_specular (specularColorFactor 2.0) in place would
    hand Godot a material whose highlights fight the unlit override.
    """
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.9
    ob.data.materials.clear()
    ob.data.materials.append(mat)
    return mat


def shrink(img, size, quality=88):
    was = tuple(img.size)
    if max(was) > size:
        img.scale(size, size)
    img.file_format = "JPEG"
    img.pack()
    return was, tuple(img.size)


def action_fcurves(act):
    """Every fcurve in an action, on both action APIs.

    Blender 4.4 introduced SLOTTED actions and 5.x removed Action.fcurves outright, so
    the curves now live at action.layers[].strips[].channelbags[].fcurves.  Worth a
    helper rather than a version check at the call site: the old attribute did not
    start returning wrong answers, it stopped existing, which is the failure mode that
    is safe to paper over.
    """
    if hasattr(act, "fcurves"):
        return list(act.fcurves)
    out = []
    for layer in getattr(act, "layers", []):
        for strip in getattr(layer, "strips", []):
            for cb in getattr(strip, "channelbags", []):
                out.extend(cb.fcurves)
    return out


def dedrift(arm, act):
    """Make a clip play IN PLACE without flattening the motion inside it.

    Meshy's clips carry root translation on Hips.  Two different things live in that
    channel and they must not share a fate:

      OSCILLATION -- the vertical bob, and the lateral weight shift (the attack's is
        64 cm peak-to-peak, which is what a two-handed pollaxe swing costs).  This is
        the animation.  Zeroing the channel to force "in place" would delete it and
        leave a figure that swings from the shoulders with a nailed-down pelvis.

      DRIFT -- net displacement from the first key to the last.  The attack ends 9.7 cm
        forward of where it began; the walk ends 0.5 cm across.  In a 2D scene the
        BODY's position is the Keeper's, so any net travel here is the 3D figure
        walking away from its own feet.

    Subtracting a straight ramp from first key to last removes exactly the second and
    leaves exactly the first, and it makes every looping clip close on itself.  The
    vertical channel is left alone -- a figure is allowed to end a crouch lower than it
    started, and the aim point is what puts the soles on the floor.

    Which channel is vertical is taken from the BONE'S REST BASIS, not from the size of
    the numbers in the channels.  The first version of this ranked the three channels by
    mean magnitude, expecting the vertical one to sit near the 80-100 the glTF file
    shows for hip height.  It does not: a Blender pose-bone location is a DELTA FROM
    REST in bone-local space, so all three channels hover near zero and the ranking had
    no signal to rank.  It duly returned an answer anyway -- a different "up" axis for
    each of the four clips of a single rig (2, 1, 1, 0), which is how it was caught.
    The rest basis is a real measurement with a real gradient, and the verticality
    figures are reported so a tilted root shows up instead of being averaged away.
    """
    loc = {}
    for fc in action_fcurves(act):
        if fc.data_path == 'pose.bones["Hips"].location':
            loc[fc.array_index] = fc
    if len(loc) < 3:
        return {"status": "no Hips location channel"}
    bone = arm.data.bones.get("Hips")
    if bone is None:
        return {"status": "no Hips bone"}
    basis = (arm.matrix_world @ bone.matrix_local).to_3x3()
    vert = [abs(basis.col[i].normalized().z) for i in range(3)]
    up = max(range(3), key=lambda i: vert[i])
    out = {"up_channel": up,
           "axis_verticality": [round(v, 4) for v in vert],
           "removed_cm": {}}
    for i, fc in loc.items():
        if i == up:
            continue
        ks = fc.keyframe_points
        if len(ks) < 2:
            continue
        f0, f1 = ks[0].co.x, ks[-1].co.x
        drift = ks[-1].co.y - ks[0].co.y
        out["removed_cm"][str(i)] = round(drift, 4)
        if abs(drift) < 1e-9 or f1 <= f0:
            continue
        for k in ks:
            d = drift * (k.co.x - f0) / (f1 - f0)
            k.co.y -= d
            # move the handles by the same amount, so the curve's SHAPE is untouched
            k.handle_left.y -= d
            k.handle_right.y -= d
        fc.update()
    return out


def assign(arm, act):
    """Make `act` the armature's active action on both action APIs."""
    if arm.animation_data is None:
        arm.animation_data_create()
    arm.animation_data.action = act
    if hasattr(arm.animation_data, "action_slot"):
        try:
            arm.animation_data.action_slot = act.slots[0]
        except Exception:
            pass


def trim_to_whole_strides(act, f0, lag, strides):
    """Cut a locomotion clip back to a whole number of strides so it can LOOP.

    The carry walk holds 3.52 strides and the carry run 2.6.  Played as a loop, the
    last frame is half a stride away from the first, so the figure snaps mid-step
    every time round -- once every four seconds, on the clip a player watches most.
    Dropping the partial stride costs half a second of motion and buys a seam.
    Returns the number of keyframes removed, so a no-op is visible as a no-op.
    """
    keep_to = f0 + int(strides) * lag
    if int(strides) < 1:
        return {"trimmed": False, "why": "less than one whole stride"}
    removed = 0
    for fc in action_fcurves(act):
        doomed = [k for k in fc.keyframe_points if k.co.x > keep_to + 0.001]
        for k in reversed(doomed):
            fc.keyframe_points.remove(k)
            removed += 1
        fc.update()
    return {"trimmed": removed > 0, "keys_removed": removed,
            "kept_strides": int(strides), "kept_to_frame": keep_to}


def stride_seconds(arm, act, locomotion):
    """How long ONE STRIDE of this clip lasts, measured from a foot's height.

    WHY NOT THE CLIP LENGTH.  Retiming locomotion to the Keeper's cadence means
    matching time per STRIDE, not per file.  The motion-library walk is 1.03 s and
    the text-to-motion carry walk is 3.97 s; scaling both whole clips onto the
    Keeper's 0.58 s stride would run the carry walk at nearly four times speed.

    A foot's vertical track rises and falls once per stride, so the stride is that
    signal's period.

    HOW THE PERIOD IS FOUND, and why the obvious way does not work.  The first
    version took the argmax of an autocorrelation over lags 6..n/2 and returned
    0.25 s -- lag 6, the FLOOR OF ITS OWN SEARCH RANGE -- for every clip it claimed
    to measure, including a 4 s walk.  Autocorrelation decays smoothly from 1 at
    lag 0, so its maximum over any range that starts near zero is the start of the
    range; and normalising by the whole signal's energy while summing only the
    overlap made short lags look better still.  The argmax was answering "which lag
    is smallest", which it did correctly.  That is the third time on this project a
    period measurement has returned a search bound for every input.

    So: normalise each lag against the energy of the two windows it actually
    compares, wait for the correlation to fall below zero -- past the self-similarity
    shoulder, where a genuine repeat must live -- and take the peak AFTER that.

    CONFIDENCE TRAVELS WITH THE NUMBER.  A clip holding a single stride has nothing
    to correlate against and no period to find; that is not a failure, and it must
    read as "one stride, whole clip" rather than as a fitted cadence.
    """
    total = (act.frame_range[1] - act.frame_range[0]) / 24.0
    if not locomotion:
        return {"status": "not a locomotion clip", "strides": 1,
                "seconds": round(total, 4), "confidence": None}
    bone = arm.pose.bones.get("RightToeBase") or arm.pose.bones.get("RightFoot")
    if bone is None:
        return {"status": "no foot bone", "strides": 1, "seconds": round(total, 4)}
    assign(arm, act)
    f0, f1 = [int(round(v)) for v in act.frame_range]
    n = f1 - f0 + 1
    h = []
    for fr in range(f0, f1 + 1):
        bpy.context.scene.frame_set(fr)
        bpy.context.view_layer.update()
        h.append((arm.matrix_world @ bone.matrix).translation.z)
    mean = sum(h) / n
    x = [v - mean for v in h]
    if sum(v * v for v in x) <= 1e-12:
        return {"status": "foot does not move", "strides": 1,
                "seconds": round(total, 4), "confidence": 0.0}

    def r_at(lag):
        m = n - lag
        if m < 8:
            return -2.0
        a = sum(x[i] * x[i + lag] for i in range(m))
        ea = sum(x[i] * x[i] for i in range(m))
        eb = sum(x[i + lag] * x[i + lag] for i in range(m))
        d = (ea * eb) ** 0.5
        return -2.0 if d <= 1e-12 else a / d

    lags = list(range(2, max(3, n // 2 + 1)))
    r = [r_at(k) for k in lags]
    first_neg = next((i for i, v in enumerate(r) if v < 0.0), None)
    if first_neg is None:
        # never decorrelates: one stride or less, nothing to find
        return {"status": "no repeat within the clip (one stride)", "strides": 1,
                "seconds": round(total, 4), "confidence": round(max(r), 3) if r else 0.0}
    tail = r[first_neg:]
    best_i = max(range(len(tail)), key=lambda i: tail[i])
    lag = lags[first_neg + best_i]
    conf = tail[best_i]
    per = lag / 24.0
    # Accept on THREE agreeing facts, not one threshold. The carry run peaks at 0.394 --
    # under any round number one would pick, and pointing at a 0.71 s stride repeating
    # four times in a 3 s clip, which is a run. A bare cutoff would have called that
    # aperiodic and played the run four times too slow; a cutoff low enough to admit it
    # would admit noise. Correlation, human plausibility and a repeat count are
    # independent, and noise does not satisfy all three.
    plausible = 0.35 <= per <= 1.6
    repeats = total / per
    if not (conf >= 0.35 and plausible and repeats >= 2.0):
        return {"status": "no periodicity (using whole clip)", "strides": 1,
                "seconds": round(total, 4), "confidence": round(conf, 3),
                "rejected": {"lag_frames": lag, "implied_stride_s": round(per, 4),
                             "plausible_human_stride": plausible,
                             "repeats": round(repeats, 2)}}
    return {"status": "ok", "strides": round(total / per, 2), "seconds": round(per, 4),
            "confidence": round(conf, 3), "lag_frames": lag,
            "plausible_human_stride": bool(0.35 <= per <= 1.6)}


def bbox_world(ob):
    pts = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def build_knight(report):
    wipe()
    arm, meshes, _ = imp(os.path.join(SRC, "rigged.glb"))
    if arm is None or not meshes:
        raise SystemExit("rigged.glb gave no armature/mesh")
    body = meshes[0]
    # the stub action rigged.glb carries is not a clip anyone plays
    if arm.animation_data and arm.animation_data.action:
        arm.animation_data.action = None
    for a in list(bpy.data.actions):
        bpy.data.actions.remove(a)

    lo, hi = bbox_world(body)
    report["figure_height_m"] = round(hi.z - lo.z, 6)
    report["sole_z_m"] = round(lo.z, 6)
    report["mesh_bbox_m"] = {"lo": [round(v, 4) for v in lo], "hi": [round(v, 4) for v in hi]}

    # --- collect the four clips onto this one armature ----------------------
    bones = {b.name for b in arm.pose.bones}
    report["clips"] = []
    for game_name, fname, action_name in CLIPS:
        path = os.path.join(SRC, fname)
        if not os.path.exists(path):
            report["clips"].append({"name": game_name, "status": "source missing"})
            continue
        keep = set(bpy.data.objects)
        keep_actions = set(bpy.data.actions)
        arm2, _m2, added = imp(path)
        got = [a for a in bpy.data.actions if a not in keep_actions]
        act = next((a for a in got if a.name == action_name), None)
        if act is None:
            # names can pick up a .001 suffix when a same-named action already exists
            act = next((a for a in got if a.name.startswith(action_name)), None)
        if act is None:
            report["clips"].append({"name": game_name, "status": "action %r not found; saw %s"
                                    % (action_name, [a.name for a in got])})
        else:
            act.name = game_name
            act.use_fake_user = True
            # Measure on THE CLIP\'S OWN ARMATURE (arm2), never on the base one.
            # Assigning a foreign action to the base armature looked equivalent and is
            # not: on Blender 4.4+ slotted actions the slot binding does not follow, so
            # the base armature quietly kept playing the PREVIOUS clip and c_walk was
            # measured against c_idle\'s motionless foot -- "no periodicity", confidence
            # -0.035, on a walk whose hip track is visibly periodic. Sampling the
            # armature the importer bound the action to makes that class of mistake
            # impossible rather than merely unlikely: that armature has no other action.
            locomotion = game_name.endswith("walk") or game_name.endswith("run")
            stride = stride_seconds(arm2 if arm2 is not None else arm, act, locomotion)
            if locomotion and stride.get("status") == "ok" \
                    and stride.get("strides", 0) >= 2 \
                    and abs(stride["strides"] - round(stride["strides"])) > 0.12:
                stride["loop_fix"] = trim_to_whole_strides(
                    act, int(round(act.frame_range[0])), stride["lag_frames"],
                    stride["strides"])
                stride["seconds_after_trim"] = round(
                    (act.frame_range[1] - act.frame_range[0]) / 24.0, 4)
            # Which bones does this action actually address?  An action built for a
            # different rig would import fine and animate nothing; this is the check
            # that the rigs really are the same one.
            addressed = set()
            for fc in action_fcurves(act):
                if 'pose.bones["' in fc.data_path:
                    addressed.add(fc.data_path.split('"')[1])
            fs, fe = act.frame_range
            report["clips"].append({
                "name": game_name, "source": fname, "action": action_name,
                "frames": [round(fs, 2), round(fe, 2)],
                "seconds": round((fe - fs) / 24.0, 4),
                "bones_addressed": len(addressed),
                "bones_unknown_to_rig": sorted(addressed - bones),
                "in_place": dedrift(arm, act),
                "stride": stride,
                "status": "ok",
            })
        for o in added:
            if o not in keep:
                bpy.data.objects.remove(o, do_unlink=True)
        for a in got:
            if a is not act:
                bpy.data.actions.remove(a)

    # --- NLA tracks: one per clip, so the exporter emits one animation each --
    if arm.animation_data is None:
        arm.animation_data_create()
    for t in list(arm.animation_data.nla_tracks):
        arm.animation_data.nla_tracks.remove(t)
    for a in sorted(bpy.data.actions, key=lambda x: x.name):
        tr = arm.animation_data.nla_tracks.new()
        tr.name = a.name
        tr.strips.new(a.name, int(a.frame_range[0]), a)
        tr.mute = False

    # --- geometry + material ------------------------------------------------
    for o in bpy.data.objects:
        o.select_set(False)
    before_tris = tri_count(body)
    after_tris, ratio = decimate(body, TARGET_TRIS)
    bpy.context.view_layer.objects.active = body
    body.select_set(True)
    bpy.ops.object.shade_smooth()
    img = base_image(body)
    was, now = shrink(img, KNIGHT_TEX)
    flatten_material(body, img, "knight_t3")
    report["knight"] = {"tris_before": before_tris, "tris_after": after_tris,
                        "decimate_ratio": round(ratio, 5),
                        "tex_before": list(was), "tex_after": list(now),
                        "shading": "smooth (for a watertight inverted-hull outline)"}

    # hand bone rest position, in the mesh's own space -- the pollaxe mount
    for bone_name in ("RightHand", "LeftHand"):
        b = arm.data.bones.get(bone_name)
        if b is not None:
            head = arm.matrix_world @ b.head_local
            tail = arm.matrix_world @ b.tail_local
            report.setdefault("bones", {})[bone_name] = {
                "head_m": [round(v, 4) for v in head],
                "tail_m": [round(v, 4) for v in tail],
                "length_m": round((tail - head).length, 4),
            }

    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, "knight_t3.glb")
    bpy.ops.export_scene.gltf(
        filepath=out, export_format="GLB",
        export_image_format="JPEG", export_jpeg_quality=88,
        export_animation_mode="ACTIONS", export_animations=True,
        export_bake_animation=True, export_optimize_animation_size=True,
        export_skins=True, export_apply=False, export_yup=True)
    report["knight"]["glb"] = out
    report["knight"]["glb_mb"] = round(os.path.getsize(out) / 1e6, 2)

    # Sidecar the runtime reads for per-clip cadence. Written here because the stride
    # is a property of the ANIMATION, measured where the animation is; making the
    # runtime re-derive it would be a second implementation free to disagree.
    clips_json = {
        "note": "C-9 R-C9-61 T3. Per-clip stride lengths measured by "
                "tools/build_knight3d.py from a foot's vertical track. `seconds` is ONE "
                "STRIDE, not the clip length -- the library walk and the text-to-motion "
                "carry walk hold different numbers of strides in the same gait.",
        "clips": {c["name"]: c.get("stride", {}) for c in report["clips"]
                  if c.get("status") == "ok"},
    }
    with open(os.path.join(PROJ, "frames", "knight_t3_clips.json"), "w") as fh:
        json.dump(clips_json, fh, indent=1)


def build_pollaxe(report):
    wipe()
    _a, meshes, _ = imp(os.path.join(SRC, "pollaxe.glb"))
    ob = meshes[0]
    lo, hi = bbox_world(ob)
    before = tri_count(ob)
    after, ratio = decimate(ob, POLLAXE_TRIS)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_smooth()
    img = base_image(ob)
    was, now = shrink(img, POLLAXE_TEX)
    flatten_material(ob, img, "pollaxe_t3")
    out = os.path.join(OUT, "pollaxe_t3.glb")
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB",
                              export_image_format="JPEG", export_jpeg_quality=88,
                              export_animations=False, export_apply=False,
                              export_yup=True)
    # The haft's axis and length, so the runtime mount is derived, not guessed.
    span = hi - lo
    axis = "XYZ"[max(range(3), key=lambda i: span[i])]
    report["pollaxe"] = {
        "tris_before": before, "tris_after": after, "decimate_ratio": round(ratio, 5),
        "tex_before": list(was), "tex_after": list(now),
        "bbox_lo_m": [round(v, 4) for v in lo], "bbox_hi_m": [round(v, 4) for v in hi],
        "long_axis_blender": axis, "length_m": round(span[max(range(3), key=lambda i: span[i])], 4),
        "origin_is_mid_shaft": bool(abs(lo[2] + hi[2]) < 0.1 * span[2]),
        "glb": out, "glb_mb": round(os.path.getsize(out) / 1e6, 2),
    }


def main():
    report = {"note": "C-9 R-C9-61 T3 runtime-3D knight build. Written by "
                      "tools/build_knight3d.py (Blender %s)." % bpy.app.version_string,
              "source": SRC}
    build_knight(report)
    build_pollaxe(report)
    with open(os.path.join(TOOLS, "knight3d_build.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print("\n=== T3 build ===")
    print("knight  %6d -> %6d tris   tex %s -> %s   %.2f MB"
          % (report["knight"]["tris_before"], report["knight"]["tris_after"],
             report["knight"]["tex_before"], report["knight"]["tex_after"],
             report["knight"]["glb_mb"]))
    print("pollaxe %6d -> %6d tris   tex %s -> %s   %.2f MB"
          % (report["pollaxe"]["tris_before"], report["pollaxe"]["tris_after"],
             report["pollaxe"]["tex_before"], report["pollaxe"]["tex_after"],
             report["pollaxe"]["glb_mb"]))
    print("figure %.4f m, sole z %.4f m" % (report["figure_height_m"], report["sole_z_m"]))
    print("  %-9s %-9s %-8s %-9s %s" % ("clip", "length", "strides", "stride s", "confidence"))
    for c in report["clips"]:
        s = c.get("stride", {})
        print("  %-9s %7.3f s %7s %9s   %-6s  %s"
              % (c["name"], c.get("seconds", 0.0), s.get("strides", "?"),
                 s.get("seconds", "?"), s.get("confidence", "?"), s.get("status", "")))
    src_mb = sum(os.path.getsize(os.path.join(SRC, f)) for _n, f, _a in CLIPS
                 if os.path.exists(os.path.join(SRC, f))) / 1e6
    print("delivered as %.1f MB of per-clip GLBs; shipping %.2f MB"
          % (src_mb, report["knight"]["glb_mb"] + report["pollaxe"]["glb_mb"]))


if __name__ == "__main__":
    main()
