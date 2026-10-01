# R-C9-98: clearance of a rigid prop against the posed body, over every clip (every STEP-th frame).
#   blender -b -noaudio --python s29_clearance.py -- <body.glb> <prop.glb> <out.json> [--step 2] [--clips a,b] [--ignore-bone RightHand]
# Per frame: the prop's vertices INSIDE the body (nearest posed-body point + its normal: negative side, within 5 cm), the
# prop's minimum distance to the body, and to the left and right HAND vertices specifically. --ignore-bone drops body
# vertices weighted mainly to that bone (a gripped wand is inside its own fist by design).
import bpy, json, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
BODY, PROP, OUT = a[0], a[1], a[2]
STEP = int(a[a.index('--step') + 1]) if '--step' in a else 2
CLIPS = a[a.index('--clips') + 1].split(',') if '--clips' in a else None
IGN = a[a.index('--ignore-bone') + 1] if '--ignore-bone' in a else None
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
before = set(sc.objects)
bpy.ops.import_scene.gltf(filepath=PROP)
new = [o for o in sc.objects if o not in before]
prop = next(o for o in new if o.type == 'MESH' and len(o.data.vertices) > 200)
for m in prop.modifiers:
    if m.type == 'ARMATURE':
        m.object = arm
prop.parent = body.parent; prop.matrix_world = body.matrix_world.copy()
for o in new:
    if o.type == 'ARMATURE':
        bpy.data.objects.remove(o, do_unlink=True)
gi = {g.index: g.name for g in body.vertex_groups}
dom = np.array([gi[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else "" for v in body.data.vertices])
hand = {s: np.where(dom == s + "Hand")[0] for s in ("Left", "Right")}
keep = np.ones(len(dom), bool) if IGN is None else (dom != IGN)
body.data.calc_loop_triangles()
tris = np.array([list(t.vertices) for t in body.data.loop_triangles])
tris_keep = tris[keep[tris].all(1)]


def world(o, dg):
    oe = o.evaluated_get(dg); me = oe.to_mesh()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); oe.to_mesh_clear()
    M = np.array(o.matrix_world); return co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]


rep = {}
acts = [x for x in bpy.data.actions if CLIPS is None or x.name in CLIPS]
for act in acts:
    arm.animation_data.action = act
    f0, f1 = map(int, act.frame_range)
    rows = []
    for f in range(f0, f1 + 1, STEP):
        sc.frame_set(f); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
        BW = world(body, dg); PW = world(prop, dg)
        tree = BVHTree.FromPolygons([Vector(p) for p in BW.tolist()], tris_keep.tolist())
        inside, dmin = 0, 9.0
        for p in PW[:: max(1, len(PW) // 1500)]:
            h = tree.find_nearest(Vector(p.tolist()))
            if h[0] is None:
                continue
            d = (Vector(p.tolist()) - h[0]).length; dmin = min(dmin, d)
            if (Vector(p.tolist()) - h[0]).dot(h[1]) < 0 and d < 0.05:
                inside += 1
        row = dict(f=f, inside=inside, dmin=round(dmin, 4))
        for s, ids in hand.items():
            if len(ids):
                H = BW[ids][:: max(1, len(ids) // 400)]
                P2 = PW[:: max(1, len(PW) // 800)]
                row["d_%sHand" % s] = round(float(np.min(np.linalg.norm(H[:, None, :] - P2[None, :, :], axis=2))), 4)
        rows.append(row)
    rep[act.name] = dict(frames=len(rows), inside_max=max(r["inside"] for r in rows), inside_frames=sum(r["inside"] > 0 for r in rows),
                         dmin=min(r["dmin"] for r in rows), dLeftHand=min(r.get("d_LeftHand", 9) for r in rows),
                         dRightHand=min(r.get("d_RightHand", 9) for r in rows), rows=rows)
    print("CLR %-14s frames %3d  inside max %4d (in %3d frames)  dmin %.4f  L-hand %.4f  R-hand %.4f" % (
        act.name, len(rows), rep[act.name]["inside_max"], rep[act.name]["inside_frames"], rep[act.name]["dmin"],
        rep[act.name]["dLeftHand"], rep[act.name]["dRightHand"]))
json.dump(dict(body=BODY, prop=PROP, step=STEP, sampled="prop verts ~1500 per frame", clips=rep), open(OUT, "w"), indent=1)
