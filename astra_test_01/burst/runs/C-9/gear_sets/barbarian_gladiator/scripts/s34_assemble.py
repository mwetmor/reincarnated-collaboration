# R-C9-105: the champion set fitted onto the CHAMPION BODY (s31: his old skeleton, nearest-point weights) the gear way;
# one GLB per piece on his 26 joints, plus the champion body re-exported with a helmet_on key for the GALEA.
#   blender -b -noaudio --python s34_assemble.py -- <champion_body_piece.glb> <pieces_dir> <out_dir>
#   rigid      helm (Head), girdle + plaque (Hips), greaves (LeftLeg / RightLeg, split), wrists (fore-arms, split)
#   rigid-ish  chest: front and back plates on Spine02/Spine01 within 14 cm of the midline (her breastplate's v4 rule),
#              the shoulder straps keep their skin weights; Laplacian smoothed
#   skinned    pauldron (the lion pauldron + segmented manica on his right arm), wraps -- nearest-point, smoothed
#   kilt       SPLIT AT THE MIDLINE into kilt_L / kilt_R (faces by centroid), each half hung from Hips at the girdle and
#              blending to ITS OWN thigh toward the hem (UpLeg weight 0 at the top -> 0.9 at the hem), so no triangle spans
#              both thighs in a stride or the whirlwind. The seam is hidden in the fur: each half's boundary is extended
#              8 mm, so the halves overlap at the cut instead of meeting at a line.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s34_assemble.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODYP, PIECES, OUT = a[0], a[1], a[2]
os.makedirs(OUT, exist_ok=True)
rep = dict(pieces={})
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODYP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
bo = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
for o in [o for o in sc.objects if o.type == 'MESH' and o is not bo]:
    bpy.data.objects.remove(o, do_unlink=True)
if arm.animation_data:
    arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(bo)
mid_x = float(np.array(arm.matrix_world @ arm.pose.bones["Hips"].head)[0])
H = float(BV[:, 2].max() - BV[:, 2].min()); z0 = float(BV[:, 2].min())
print("champion body %.4f m, %d verts" % (H, len(BV)))


def weld(pc):
    bm = bmesh.new(); bm.from_mesh(pc.data); n0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5); n1 = len(bm.verts)
    bm.to_mesh(pc.data); bm.free(); pc.data.update(); return n0, n1


def extend_boundary(pc, dist):
    bm = bmesh.new(); bm.from_mesh(pc.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.verts.ensure_lookup_table(); bm.normal_update(); move = {}
    for e in bm.edges:
        if not e.is_boundary or not e.link_faces:
            continue
        f = e.link_faces[0]; a_, b_ = e.verts[0].co, e.verts[1].co
        o = (b_ - a_).normalized().cross(f.normal).normalized()
        if (f.calc_center_median() - (a_ + b_) * 0.5).dot(o) > 0:
            o = -o
        for v in e.verts:
            move.setdefault(v.index, Vector((0, 0, 0))); move[v.index] += o
    for vi, o in move.items():
        if o.length > 1e-9:
            bm.verts[vi].co += o.normalized() * dist
    bm.to_mesh(pc.data); bm.free(); pc.data.update(); return len(move)


def smooth_weights(pc, it=10):
    ng, nv = len(pc.vertex_groups), len(pc.data.vertices)
    Wm = np.zeros((nv, ng), np.float32)
    for v in pc.data.vertices:
        for g in v.groups:
            Wm[v.index, g.group] = g.weight
    ed = np.empty(len(pc.data.edges) * 2, int); pc.data.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    deg = np.bincount(ed.ravel(), minlength=nv).astype(np.float32)[:, None]
    for _ in range(it):
        acc = np.zeros_like(Wm); np.add.at(acc, ed[:, 0], Wm[ed[:, 1]]); np.add.at(acc, ed[:, 1], Wm[ed[:, 0]])
        Wm = 0.5 * Wm + 0.5 * np.where(deg > 0, acc / np.maximum(deg, 1), Wm)
    top = np.argsort(-Wm, axis=1)[:, :4]; keep = np.zeros_like(Wm, bool); np.put_along_axis(keep, top, True, axis=1)
    Wm = np.where(keep & (Wm > 0.002), Wm, 0.0); Wm /= np.maximum(Wm.sum(1, keepdims=True), 1e-9)
    for gi_ in range(ng):
        grp = pc.vertex_groups[gi_]; grp.remove(list(range(nv)))
        for vi in np.nonzero(Wm[:, gi_])[0]:
            grp.add([int(vi)], float(Wm[vi, gi_]), 'REPLACE')


def set_weights(pc, rows):
    """rows: list of {bone: weight} per vertex"""
    for n in names:
        if n not in pc.vertex_groups:
            pc.vertex_groups.new(name=n)
    for i, wmap in enumerate(rows):
        for g in list(pc.data.vertices[i].groups):
            pc.vertex_groups[g.group].remove([i])
        for bname, w in wmap.items():
            if w > 0.002:
                pc.vertex_groups[bname].add([i], float(w), 'REPLACE')
    m = pc.modifiers.new('arm', 'ARMATURE'); m.object = arm


made = []
SPEC = {  # name: (faces, push-off offset m, hem m, mode)
    "chest": (20000, 0.010, 0.004, "chest"), "pauldron": (22000, 0.008, 0.004, "skin"), "wraps": (14000, 0.004, 0.004, "skin"),
    "helm": (14000, 0.006, 0.0, "rigid:Head"), "girdle": (12000, 0.012, 0.004, "rigid:Hips"),
    "greaves": (14000, 0.006, 0.0, "split:LeftLeg,RightLeg"), "wrists": (8000, 0.004, 0.0, "split:LeftForeArm,RightForeArm"),
    "kilt": (30000, 0.012, 0.008, "kilt")}
for nm, (faces, offs, hem, mode) in SPEC.items():
    before = set(sc.objects)
    pc = G.import_piece(os.path.join(PIECES, nm + ".glb"), before)
    f0 = len(pc.data.polygons); wv = weld(pc); G.decimate(pc, faces)
    nb = extend_boundary(pc, hem) if hem and mode != "kilt" else 0
    P, pushed = G.clear_body(pc, tree, offs)
    info = dict(mode=mode, faces=[f0, len(pc.data.polygons)], welded=list(wv), offset_m=offs, hem_m=hem, pushed=int(pushed))
    objs = []
    if mode.startswith("rigid:"):
        bone = mode.split(":")[1]
        set_weights(pc, [{bone: 1.0}] * len(pc.data.vertices)); objs = [pc]
    elif mode.startswith("split:"):
        bones = mode.split(":")[1].split(",")
        parts = G.bone_bind(pc, arm, bones, True); objs = [o for o, _ in parts]
        info["parts"] = [(o.name, b_) for o, b_ in parts]
    elif mode == "kilt":
        # split by face centroid at the midline: two COPIES, each deleting the other side's faces (deterministic, no
        # edit-mode selection state)
        halves = []
        for keep_left in (True, False):
            o = pc.copy(); o.data = pc.data.copy(); sc.collection.objects.link(o)
            bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
            Mw_ = o.matrix_world
            kill = [f for f in bm.faces if ((Mw_ @ f.calc_center_median()).x > mid_x) != keep_left]
            bmesh.ops.delete(bm, geom=kill, context='FACES')
            loose = [v for v in bm.verts if not v.link_faces]
            bmesh.ops.delete(bm, geom=loose, context='VERTS')
            bm.to_mesh(o.data); bm.free(); o.data.update()
            for g in list(o.vertex_groups):
                o.vertex_groups.remove(g)
            for m in list(o.modifiers):
                o.modifiers.remove(m)
            halves.append(o)
        bpy.data.objects.remove(pc, do_unlink=True)
        info["halves"] = {}
        ztop = z0 + 0.585 * H; zhem = z0 + 0.33 * H
        for o in halves:
            co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co); V = co.reshape(-1, 3)
            Mw = np.array(o.matrix_world); V = V @ Mw[:3, :3].T + Mw[:3, 3]
            side = "LeftUpLeg" if np.median(V[:, 0]) > mid_x else "RightUpLeg"
            nbh = extend_boundary(o, hem)        # the seam overlap, hidden in the fur
            co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co); V = co.reshape(-1, 3) @ Mw[:3, :3].T + Mw[:3, 3]
            t = np.clip((ztop - V[:, 2]) / (ztop - zhem), 0, 1)
            rows = [{"Hips": float(1 - 0.9 * ti), side: float(0.9 * ti)} for ti in t]
            set_weights(o, rows)
            o.name = "kilt_" + side[0]
            info["halves"][o.name] = dict(verts=len(o.data.vertices), thigh=side, boundary_extended=int(nbh),
                                          ramp="Hips 1 at the girdle (zf 0.585) -> UpLeg 0.9 at the hem (zf 0.33)")
            objs.append(o)
    else:
        ok = G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
        if mode == "chest":
            gs2, gs1 = pc.vertex_groups["Spine02"], pc.vertex_groups["Spine01"]; rig = 0
            for i, p in enumerate(P):
                if abs(p[0] - mid_x) >= 0.14:
                    continue
                for g in list(pc.data.vertices[i].groups):
                    pc.vertex_groups[g.group].remove([i])
                gs2.add([i], 0.7, 'REPLACE'); gs1.add([i], 0.3, 'REPLACE'); rig += 1
            info["rigid_torso_verts"] = rig
        smooth_weights(pc, 10); info["weight_smooth"] = "numpy Laplacian x10, limit 4"
        objs = [pc]
    for o in objs:
        G.align_space(o, bo)
    if len(objs) == 1:
        objs[0].name = nm
    made.append((nm, objs))
    rep["pieces"][nm] = info
    print("  %-9s %-28s %6d -> %6d faces, pushed %d at %.3f m" % (nm, mode, f0, sum(len(o.data.polygons) for o in objs), pushed, offs))

# helmet_on on the champion body, for the GALEA (D2's method)
helm = dict(made)["helm"][0]
moved, tested, _k = G.helmet_on_key(bo, helm, arm, clearance=0.010, name="helmet_on")
rep["helmet_on"] = dict(moved=int(moved), candidates=int(tested), clearance_m=0.010)
print("  helmet_on: %d of %d crown verts moved under the galea" % (moved, tested))
for k in bo.data.shape_keys.key_blocks:
    k.value = 0.0


def export(objs, path, with_body=False):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    arm.select_set(True); bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_animations=False,
                              export_morph=True, export_image_format='AUTO')
    return round(os.path.getsize(path) / 1e6, 2)


for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
rep["files"] = {}
for nm, objs in made:
    rep["files"][nm + ".glb"] = export(objs, os.path.join(OUT, nm + ".glb"))
    print("wrote %-12s %5.2f MB" % (nm + ".glb", rep["files"][nm + ".glb"]))
bo.name = "champion_body"
rep["files"]["champion_body_piece.glb"] = export([bo], os.path.join(OUT, "champion_body_piece.glb"))
json.dump(rep, open(os.path.join(OUT, "assemble.json"), "w"), indent=1)
