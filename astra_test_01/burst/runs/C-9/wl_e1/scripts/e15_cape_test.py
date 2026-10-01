# E1 CAPE STRIDE TEST: on every key of walk and run (and the attack, death), the panel-split cape against his legs.
#   STRETCH: each cape edge's length over its rest length -- a panel weighted across both thighs would stretch at the stride;
#            report max and p99 per clip.
#   POKE:    leg-mesh vertices (UpLeg/Leg/Foot weight > 0.5) that come out THROUGH the cape: nearest cape point within
#            the cape's footprint and on the cape's OUTER side (along its normal) by > 5 mm. Max share per clip.
#   blender -b -noaudio --python e15_cape_test.py -- <body.glb> <cape.glb> [--clips walk,run,attack,death] [--json f]
import bpy, bmesh, json, sys, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; BODY, CAPE = a[:2]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CLIPS = opt('--clips', 'walk,run,attack,death').split(',')
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene; FPS = sc.render.fps / sc.render.fps_base
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]: bpy.data.objects.remove(o, do_unlink=True)
body = max([o for o in sc.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
acts = {x.name: x for x in bpy.data.actions}
before = set(sc.objects); bpy.ops.import_scene.gltf(filepath=CAPE)
new = [o for o in sc.objects if o not in before]; cape = next(o for o in new if o.type == 'MESH' and o.vertex_groups)
mw = cape.matrix_world.copy()
for md in cape.modifiers:
    if md.type == 'ARMATURE': md.object = arm
cape.parent = arm; cape.matrix_parent_inverse = arm.matrix_world.inverted(); cape.matrix_world = mw
for o in new:
    if o != cape: bpy.data.objects.remove(o, do_unlink=True)
for x in list(bpy.data.actions):
    if x.name not in acts: bpy.data.actions.remove(x)
legs = set()
gi = {g.index: g.name for g in body.vertex_groups}
for v in body.data.vertices:
    for g in v.groups:
        if any(k in gi[g.group] for k in ('UpLeg', 'Leg', 'Foot', 'Toe')) and g.weight > 0.5: legs.add(v.index)
legs = np.array(sorted(legs))
cbm = bmesh.new(); cbm.from_mesh(cape.data); E = np.array([[e.verts[0].index, e.verts[1].index] for e in cbm.edges]); cbm.free()
def evalw(o):
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', co); M = np.array(o.matrix_world)
    V = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]; me.calc_loop_triangles()
    T = np.array([list(t.vertices) for t in me.loop_triangles]); oe.to_mesh_clear(); return V, T
arm.animation_data.action = None
for pb in arm.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
CV0, _ = evalw(cape); REST = True; L0 = np.linalg.norm(CV0[E[:, 0]] - CV0[E[:, 1]], axis=1); ok = L0 > 1e-5
rep = {}
CLIPS = ['__rest__'] + CLIPS
for clip in CLIPS:
    if clip == '__rest__':
        ac = None
    else:
        ac = acts[clip]; arm.animation_data.action = ac
    if ac is not None and hasattr(arm.animation_data, 'action_slot') and ac.slots: arm.animation_data.action_slot = ac.slots[0]
    if ac is None:
        arm.animation_data.action = None
        for pb in arm.pose.bones: pb.matrix_basis.identity()
    f0, f1 = ac.frame_range if ac is not None else (1.0, 1.0); st, pk = [], []
    for f in np.arange(f0, f1 + 1e-6, 1.0):
        sc.frame_set(int(f), subframe=f % 1.0)
        CV, CT = evalw(cape); BVv, _ = evalw(body)
        Ls = np.linalg.norm(CV[E[ok, 0]] - CV[E[ok, 1]], axis=1) / L0[ok]
        st.append((float(Ls.max()), float(np.percentile(Ls, 99))))
        tree = BVHTree.FromPolygons([Vector(p) for p in CV.tolist()], CT.tolist())
        lo, hi = CV.min(0), CV.max(0); n_in = 0; n_poke = 0
        for p in BVv[legs]:
            if not (lo[0] < p[0] < hi[0] and lo[2] < p[2] < hi[2]): continue
            hit = tree.find_nearest(Vector(p.tolist()))
            if hit[0] is None or (Vector(p.tolist()) - hit[0]).length > 0.10: continue
            n_in += 1
            if (Vector(p.tolist()) - hit[0]).dot(hit[1]) > 0.005: n_poke += 1
        pk.append(n_poke / max(len(legs), 1))
    st = np.array(st); k = int(np.argmax(pk))
    rep[clip] = dict(frames=len(pk), stretch_max=round(float(st[:, 0].max()), 3), stretch_p99_max=round(float(st[:, 1].max()), 3),
                     poke_max_share=round(float(max(pk)), 4), poke_worst_frame=int(f0 + k), poke_mean_share=round(float(np.mean(pk)), 4))
    print('CAPE', clip, json.dumps(rep[clip]))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
