# Measure every clip at the ground, with and without the Hips scale track.
#
#   blender -b -noaudio --python scripts/22_ground.py -- <clip.glb> [--json out]
#
# Answers the question the fix depends on: is the idle's foot contact steady
# enough that ONE constant offset grounds the whole loop, or does it need a
# per-frame offset? Per-frame grounding is not free -- it deletes whatever
# vertical motion the clip actually has, and "keep the breathing" means not
# doing that blindly. So: measure, then choose.
import bpy, json, os, sys
import numpy as np
from mathutils import Matrix
a = sys.argv[sys.argv.index('--') + 1:]
CLIP = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)


def act_fcurves(act):
    """Blender 5.x moved fcurves into slotted action layers/strips/channelbags;
    act.fcurves is gone. Handle both so this survives the next upgrade."""
    if hasattr(act, 'layers') and len(act.layers):
        out = []
        for layer in act.layers:
            for strip in layer.strips:
                for cb in getattr(strip, 'channelbags', []):
                    out.extend(cb.fcurves)
        return out
    return list(getattr(act, 'fcurves', []))


def bone_of(fc):
    return fc.data_path.split('"')[1] if '"' in fc.data_path else '?'


def strip_bone_scale(actions):
    """Set every pose-bone scale track to 1.0. A joint scale track in a clip is
    never animation on a character like this -- it is a retarget artefact, and
    on the skeleton ROOT it silently resizes the whole body."""
    found = {}
    for act in actions:
        for fc in act_fcurves(act):
            if not fc.data_path.endswith('.scale'):
                continue
            vals = sorted({round(k.co[1], 6) for k in fc.keyframe_points})
            if all(abs(v - 1.0) <= 1e-3 for v in vals):
                continue
            found.setdefault(act.name, {}).setdefault(bone_of(fc), []).append(vals)
            for k in fc.keyframe_points:
                k.co[1] = 1.0
                k.handle_left[1] = 1.0
                k.handle_right[1] = 1.0
            fc.update()
    return found


def shift_root(act, arm, bone, dz_world):
    """Add a constant world +Z offset to a root bone's location track.

    Pose location lives in the bone's own rest basis, not in world space, so a
    raw += on the Z channel is wrong for any rig whose root bone is not axis
    aligned. Convert through the bone's rest matrix, then VERIFY by measuring
    the feet again -- the conversion is the part that looks right and isn't."""
    from mathutils import Vector
    d_a = arm.matrix_world.inverted().to_3x3() @ Vector((0.0, 0.0, dz_world))
    d_b = arm.data.bones[bone].matrix_local.to_3x3().inverted() @ d_a
    n = 0
    for fc in act_fcurves(act):
        if fc.data_path != 'pose.bones["%s"].location' % bone:
            continue
        for k in fc.keyframe_points:
            k.co[1] += d_b[fc.array_index]
            k.handle_left[1] += d_b[fc.array_index]
            k.handle_right[1] += d_b[fc.array_index]
        fc.update()
        n += len(fc.keyframe_points)
    return d_b, n


FOOT = ('LeftFoot', 'LeftToeBase', 'RightFoot', 'RightToeBase')


def foot_mask(ob):
    """Vertices whose dominant group is a foot or toe. The lowest point of the
    WHOLE mesh is usually the feet anyway -- but 'usually' is how a dropped
    hand or a hanging strap ends up defining the floor."""
    gi = {vg.index: vg.name for vg in ob.vertex_groups}
    keep = []
    for v in ob.data.vertices:
        if not v.groups:
            continue
        g = max(v.groups, key=lambda x: x.weight)
        if gi.get(g.group) in FOOT:
            keep.append(v.index)
    return np.array(keep, dtype=int)


MASKS = {ob.name: foot_mask(ob) for ob in body}
print("foot vertices: %s" % {k: len(v) for k, v in MASKS.items()})


def sample(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get('co', co)
    co = co.reshape(-1, 3)
    M = np.array(ob.matrix_world)
    w = co @ M[:3, :3].T + M[:3, 3]
    ev.to_mesh_clear()
    return w


def measure(tag):
    out = {}
    for act in bpy.data.actions:
        if act.name == 'shield_carry_L':
            continue
        arm.animation_data.action = act
        f0, f1 = (int(round(x)) for x in act.frame_range)
        rows = []
        for f in range(f0, f1 + 1):
            sc.frame_set(f)
            bpy.context.view_layer.update()
            lo, top, hips = [], [], None
            for ob in body:
                w = sample(ob)
                top.append(w[:, 2].max())
                m = MASKS[ob.name]
                if len(m):
                    lo.append(w[m][:, 2].min())
            hips = (arm.matrix_world @ arm.pose.bones['Hips'].matrix).translation
            rows.append(dict(f=f, foot=float(min(lo)), top=float(max(top)),
                             hips_z=float(hips.z)))
        fz = np.array([r['foot'] for r in rows])
        hz = np.array([r['top'] - r['foot'] for r in rows])
        out[act.name] = dict(
            frames=[f0, f1],
            foot_min=round(float(fz.min()), 4), foot_max=round(float(fz.max()), 4),
            foot_median=round(float(np.median(fz)), 4),
            foot_spread_cm=round(float(fz.max() - fz.min()) * 100, 2),
            height_min=round(float(hz.min()), 4), height_max=round(float(hz.max()), 4),
            height_median=round(float(np.median(hz)), 4),
            rows=rows)
        print("  %-8s %-9s foot %+.4f..%+.4f (median %+.4f, spread %.2f cm)  "
              "height %.4f..%.4f" % (tag, act.name, fz.min(), fz.max(),
                                     np.median(fz), (fz.max() - fz.min()) * 100,
                                     hz.min(), hz.max()))
    return out


# rest pose height, for reference
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
rw = np.vstack([sample(o) for o in body])
REST_H = float(rw[:, 2].max() - rw[:, 2].min())
print("rest pose: height %.4f m, floor at %+.4f" % (REST_H, rw[:, 2].min()))

print("BEFORE (as shipped)")
before = measure('before')

# strip every pose-bone scale track, everywhere
stripped = strip_bone_scale(bpy.data.actions)
print("stripped scale tracks: %s" % json.dumps(stripped))

print("AFTER (scale stripped, NOT yet re-grounded)")
after = measure('after')

if OUTJ:
    json.dump(dict(clip=CLIP, rest_height=round(REST_H, 4),
                   stripped=stripped, before=before, after=after),
              open(OUTJ, 'w'), indent=1)
    print("wrote %s" % OUTJ)
