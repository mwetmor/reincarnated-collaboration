# Per-clip size + ground measurement on a shipped character GLB.
#
#   blender -b -noaudio --python scripts/23_measure_clips.py -- <x.glb> [--json f]
#            [--fix]   also apply strip+reground in Blender and report the delta
#
# Reports THREE things per clip, because silhouette height alone cannot tell a
# bent knee from a resized body:
#   height   top-of-head to lowest foot -- what the player sees, pose + size
#   spans    rigid bone-to-bone distances -- size ONLY. A uniform scale moves
#            these; no pose can. This is what convicts or acquits.
#   feet     lowest foot height per frame -- grounding
import bpy, json, os, sys
import numpy as np
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("23_measure_clips.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
CLIP = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
FIX = '--fix' in a

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
MASKS = {ob.name: G.foot_verts(ob) for ob in body}
CLIPS = [ac for ac in bpy.data.actions if ac.name != 'shield_carry_L']


def rest():
    arm.animation_data.action = None
    for pb in arm.pose.bones:
        pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()
    w = np.vstack([G.world_verts(o) for o in body])
    return dict(height=round(float(w[:, 2].max() - w[:, 2].min()), 4),
                floor=round(float(w[:, 2].min()), 4),
                hips_z=round(float((arm.matrix_world @
                                    arm.pose.bones['Hips'].matrix).translation.z), 4),
                spans=G.bone_span(arm))


def survey(tag):
    out = {}
    for ac in CLIPS:
        arm.animation_data.action = ac
        f0, f1 = (int(round(x)) for x in ac.frame_range)
        mid = (f0 + f1) // 2
        rows = []
        for f in range(f0, f1 + 1):
            sc.frame_set(f)
            bpy.context.view_layer.update()
            lo, hi = [], []
            for ob in body:
                w = G.world_verts(ob)
                hi.append(w[:, 2].max())
                if len(MASKS[ob.name]):
                    lo.append(w[MASKS[ob.name]][:, 2].min())
            rows.append((f, float(min(lo)), float(max(hi)),
                         float((arm.matrix_world @
                                arm.pose.bones['Hips'].matrix).translation.z)))
        fz = np.array([r[1] for r in rows])
        hz = np.array([r[2] - r[1] for r in rows])
        sc.frame_set(mid)
        bpy.context.view_layer.update()
        out[ac.name] = dict(
            frames=[f0, f1], mid=mid,
            foot=dict(min=round(float(fz.min()), 4), max=round(float(fz.max()), 4),
                      spread_cm=round(float(fz.max() - fz.min()) * 100, 2)),
            height=dict(min=round(float(hz.min()), 4), max=round(float(hz.max()), 4),
                        median=round(float(np.median(hz)), 4),
                        at_mid=round(float(hz[mid - f0]), 4)),
            hips_z=dict(min=round(float(min(r[3] for r in rows)), 4),
                        max=round(float(max(r[3] for r in rows)), 4)),
            spans_at_mid=G.bone_span(arm))
        s = out[ac.name]
        print("  %-6s %-8s height %.4f..%.4f (mid %.4f)  feet %+.4f..%+.4f  "
              "spans %s" % (tag, ac.name, s['height']['min'], s['height']['max'],
                            s['height']['at_mid'], s['foot']['min'],
                            s['foot']['max'],
                            {k: v for k, v in s['spans_at_mid'].items()}))
    return out


R = rest()
print("REST height %.4f m, floor %+.4f, hips %.4f, spans %s"
      % (R['height'], R['floor'], R['hips_z'], R['spans']))
before = survey('before')
res = dict(file=CLIP, rest=R, before=before)

if FIX:
    st = G.strip_bone_scale(bpy.data.actions)
    print("stripped: %s" % json.dumps(st))
    gr = {}
    for ac in [x for x in bpy.data.actions if x.name in st]:
        gr[ac.name] = G.reground_from_feet(arm, body, ac)
        print("  re-grounded %s by %+.5f m (world); basis delta %s over %d keys; "
              "feet %+.4f..%+.4f -> %+.4f..%+.4f, worst %.2f cm"
              % (ac.name, gr[ac.name]['dz'], gr[ac.name]['basis_delta'],
                 gr[ac.name]['keys'], gr[ac.name]['before']['min'],
                 gr[ac.name]['before']['max'], gr[ac.name]['after']['min'],
                 gr[ac.name]['after']['max'], gr[ac.name]['after']['worst_cm']))
    res.update(stripped=st, grounded=gr, after=survey('after'))

if OUTJ:
    json.dump(res, open(OUTJ, 'w'), indent=1)
    print("wrote %s" % OUTJ)
