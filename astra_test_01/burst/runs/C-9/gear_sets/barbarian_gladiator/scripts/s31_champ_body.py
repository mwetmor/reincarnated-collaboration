# R-C9-105: the CHAMPION BODY on his EXISTING skeleton -- the gear method applied to a whole body (no new rig, no clips
# fetched). The fitted Tripo build of the bare-legged champion sheet (s21_features.py: scale 1.000, anchor median 3.4 mm)
# takes its skin weights from the OLD body (nb_join/export/nb-body_join.glb, bd66432e) by nearest point, barycentric
# (gearlib.skin_to_body), then a light Laplacian smoothing (the old thighs were baggy trousers, so the nearest-point weights
# there come off a surface 2-6 cm away). The old body's grip_R / grip_L morphs are carried vertex by vertex. Optionally
# (--helmet <helm piece glb>) a helmet_on key is built for the GALEA with gearlib.helmet_on_key (D2's method).
#
#   blender -b -noaudio --python s31_champ_body.py -- <old_body.glb> <champ_fit.glb> <out_piece.glb> [--faces 110000]
#           [--helmet <helm.glb>] [--json f]
# Output: a skinned GLB (mesh + his armature, no animations), spliced into a copy of the old body by s32 (binary patch).
import bpy, bmesh, json, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s31_champ_body.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
OLD, CHAMP, OUT = a[0], a[1], a[2]
FACES = int(a[a.index('--faces') + 1]) if '--faces' in a else 110000
HELM = a[a.index('--helmet') + 1] if '--helmet' in a else None
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '.json')
rep = {}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=OLD)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
old = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
for o in [o for o in sc.objects if o.type == 'MESH' and o is not old]:
    bpy.data.objects.remove(o, do_unlink=True)
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(old)
before = set(sc.objects)
pc = G.import_piece(CHAMP, before)
bm = bmesh.new(); bm.from_mesh(pc.data); n0 = len(bm.verts)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5); bm.to_mesh(pc.data); bm.free(); pc.data.update()
f0, f1 = G.decimate(pc, FACES)
co = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get("co", co); P = co.reshape(-1, 3)
ok = G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
# light smoothing (3 iterations), keep 4 influences
ng, nv = len(pc.vertex_groups), len(pc.data.vertices)
Wm = np.zeros((nv, ng), np.float32)
for v in pc.data.vertices:
    for g in v.groups:
        Wm[v.index, g.group] = g.weight
ed = np.empty(len(pc.data.edges) * 2, int); pc.data.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
deg = np.bincount(ed.ravel(), minlength=nv).astype(np.float32)[:, None]
for _ in range(3):
    acc = np.zeros_like(Wm); np.add.at(acc, ed[:, 0], Wm[ed[:, 1]]); np.add.at(acc, ed[:, 1], Wm[ed[:, 0]])
    Wm = 0.5 * Wm + 0.5 * np.where(deg > 0, acc / np.maximum(deg, 1), Wm)
top = np.argsort(-Wm, axis=1)[:, :4]; keep = np.zeros_like(Wm, bool); np.put_along_axis(keep, top, True, axis=1)
Wm = np.where(keep & (Wm > 0.002), Wm, 0.0); Wm /= np.maximum(Wm.sum(1, keepdims=True), 1e-9)
for gi_ in range(ng):
    grp = pc.vertex_groups[gi_]; grp.remove(list(range(nv)))
    for vi in np.nonzero(Wm[:, gi_])[0]:
        grp.add([int(vi)], float(Wm[vi, gi_]), 'REPLACE')
# grip keys: displacement of the nearest OLD body vertex (world units), applied after align_space in local space
from mathutils.kdtree import KDTree
kd = KDTree(len(BV))
for i, q in enumerate(BV):
    kd.insert(Vector(q.tolist()), i)
kd.balance()
near = np.array([kd.find(Vector(p.tolist()))[1] for p in P])
Mb = np.array(old.matrix_world); kb = old.data.shape_keys.key_blocks
base = np.empty(len(old.data.vertices) * 3); kb["Basis"].data.foreach_get("co", base); base = base.reshape(-1, 3)
dW = {}
for kn in ("grip_R", "grip_L"):
    kco = np.empty(len(old.data.vertices) * 3); kb[kn].data.foreach_get("co", kco); kco = kco.reshape(-1, 3)
    d = ((kco - base) @ Mb[:3, :3].T)[near]
    # the grip closes only the HAND: restrict to vertices whose own dominant weight is that hand
    hand = names.index("RightHand" if kn == "grip_R" else "LeftHand")
    d[Wm.argmax(1) != hand] = 0
    dW[kn] = d
G.align_space(pc, old)
pc.shape_key_add(name="Basis", from_mix=False)
co = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
Mi3 = np.linalg.inv(Mb[:3, :3])
rep["keys"] = {}
for kn, d in dW.items():
    k = pc.shape_key_add(name=kn, from_mix=False); k.value = 0.0
    k.data.foreach_set("co", (co + d @ Mi3.T).ravel())
    rep["keys"][kn] = dict(verts_moved=int((np.linalg.norm(d, axis=1) > 1e-5).sum()), max_m=round(float(np.linalg.norm(d, axis=1).max()), 4))
if HELM:
    # D2's helmet_on: compress the crown hair under the helmet shell (gearlib.helmet_on_key, clearance 10 mm)
    hb = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=HELM)
    hn = [o for o in sc.objects if o not in hb]
    helm = next(o for o in hn if o.type == 'MESH' and len(o.data.vertices) > 200)
    for o in hn:
        if o.type == 'ARMATURE':
            bpy.data.objects.remove(o, do_unlink=True)
    r = G.helmet_on_key(pc, helm, arm, clearance=0.010, name="helmet_on")
    rep["keys"]["helmet_on"] = str(r)[:300]
    bpy.data.objects.remove(helm, do_unlink=True)
pc.name = "champion_body"
bpy.ops.object.select_all(action='DESELECT'); pc.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
old.select_set(False)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_animations=False, export_morph=True,
                          export_image_format='AUTO')
rep.update(dict(old_body=OLD, champ_build=CHAMP, welded=[n0, len(pc.data.vertices)], faces=[f0, f1], skinned_verts=int(ok),
                weight_smoothing=dict(iterations=3, factor=0.5, limit=4), out=OUT, mb=round(os.path.getsize(OUT) / 1e6, 2)))
json.dump(rep, open(OUTJ, "w"), indent=1)
print("CHAMP", json.dumps(rep)[:600])
