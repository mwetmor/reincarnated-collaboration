# E1 modular gear: helm, pauldrons + chest (skinned from the nearest body point, D7's method), and the CAPE
# as a PANEL-SPLIT SKIN (R-C9-113's 3D note: no cloth sim on the 24-bone rig): the cape is CUT along two slits from the hem
# up to the hips (the sheet's construction) into a BACK panel and LEFT / RIGHT panels; above the hips it hangs from the
# spine (weights from the nearest body point), below, the back panel follows the Hips and each side panel follows ITS OWN
# thigh (blended up to 0.5 by the knee) -- no panel is weighted to both thighs, so none can stretch across them at a stride.
# Each piece exported ALONE with the armature (no animations: the body's clips are never re-exported through Blender).
#   blender -b -noaudio --python e13_gear.py -- <body.glb> <outdir> --pieces helm,pauldrons,chest,cape [--json f]
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("e13_gear.py")][0])); sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]; BODYGLB, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
WANT = opt('--pieces', 'helm,pauldrons,chest,cape').split(',')
ROOT = os.path.dirname(HERE); PIECES = os.path.join(ROOT, 'pieces'); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODYGLB)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]: bpy.data.objects.remove(o, do_unlink=True)
arm.animation_data.action = None
for pb in arm.pose.bones: pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(body[0]); blo = BV.min(0); BH = float(BV[:, 2].max() - blo[2])
bonew = lambda n: np.array(arm.matrix_world @ arm.pose.bones[n].head)
rep = dict(body_height_m=round(BH, 4), pieces={})
def weld(pc):
    bm = bmesh.new(); bm.from_mesh(pc.data); n0 = len(bm.verts); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    n1 = len(bm.verts); bm.to_mesh(pc.data); bm.free(); pc.data.update(); return n0, n1
def export(pc, nm):
    bpy.ops.object.select_all(action='DESELECT'); pc.select_set(True); arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    p = os.path.join(OUT, 'wl_%s.glb' % nm)
    bpy.ops.export_scene.gltf(filepath=p, export_format='GLB', use_selection=True, export_animations=False,
                              export_image_format='JPEG', export_jpeg_quality=92)
    return p
def world(pc):
    co = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get('co', co)
    return co.reshape(-1, 3) @ np.array(pc.matrix_world.to_3x3()).T + np.array(pc.matrix_world.translation)
FACES = dict(helm=24000, pauldrons=24000, chest=30000, cape=30000)
OFFS = dict(helm=0.006, pauldrons=0.010, chest=0.008, cape=0.012)
for nm in WANT:
    before = set(sc.objects)
    pc = G.import_piece(os.path.join(PIECES, '%s_iso.glb' % nm), before)
    w0 = weld(pc); f0 = len(pc.data.polygons); G.decimate(pc, FACES[nm])
    P, pushed = G.clear_body(pc, tree, OFFS[nm])
    r = dict(faces=[f0, len(pc.data.polygons)], welded=w0, pushed=int(pushed), offset_m=OFFS[nm])
    if nm in ('helm', 'pauldrons', 'chest'):   # helm skinned too: its gorget follows the neck, the horns take the head's weights
        r['skinned'] = int(G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)); r['mode'] = 'skin (nearest body point)'
    else:  # CAPE: panels
        Pw = world(pc); zf = (Pw[:, 2] - blo[2]) / BH
        cx = float(np.median(BV[:, 0]))
        band = (zf > 0.2) & (zf < 0.4); wdt = np.percentile(Pw[band, 0], 98) - np.percentile(Pw[band, 0], 2)
        SLIT = 0.215 * wdt; HIP = float((bonew('Hips')[2] - blo[2]) / BH); GAP = 0.010
        # cut: delete faces whose centre lies in a slit band below the hips
        bm = bmesh.new(); bm.from_mesh(pc.data); bm.faces.ensure_lookup_table()
        Mw = np.array(pc.matrix_world)
        kill = []
        for f in bm.faces:
            c = Mw[:3, :3] @ np.array(f.calc_center_median()) + Mw[:3, 3]
            if (c[2] - blo[2]) / BH < HIP - 0.02 and abs(abs(c[0] - cx) - SLIT) < GAP: kill.append(f)
        bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(pc.data); bm.free(); pc.data.update()
        Pw = world(pc); zf = (Pw[:, 2] - blo[2]) / BH; xs = Pw[:, 0] - cx
        # SPLIT, not just cut: the slit band left faces bridging the panels after decimation (stride test v2: edges stretched
        # 14x). Every edge whose two ends lie on different panels below the hips is split, so the panels are separate surfaces.
        _pan = np.where(xs > SLIT, 1, np.where(xs < -SLIT, -1, 0))
        bm = bmesh.new(); bm.from_mesh(pc.data); bm.edges.ensure_lookup_table()
        _cut = [e for e in bm.edges if _pan[e.verts[0].index] != _pan[e.verts[1].index] and max(zf[e.verts[0].index], zf[e.verts[1].index]) < HIP]
        bmesh.ops.split_edges(bm, edges=_cut); bm.to_mesh(pc.data); bm.free(); pc.data.update()
        Pw = world(pc); zf = (Pw[:, 2] - blo[2]) / BH; xs = Pw[:, 0] - cx
        r_split = len(_cut)
        # FLARE (stride test v1: the back foot came through the back panel at the run's kick-back): below the hips the back
        # panel stands further off his legs, growing to FLARE m at the hem -- a cape that hangs free of the legs, as A1 drew it.
        FLARE = float(opt('--flare', '0.10'))
        _back = np.abs(xs) <= SLIT
        _u = np.clip((HIP - zf) / max(HIP - zf.min(), 1e-6), 0, 1)
        _d = np.where(_back, FLARE * _u, 0.5 * FLARE * _u)
        # stage G: the SIDE panels also stand OUT sideways (each away from the midline), growing to SIDE m at the hem -- the
        # stride test found legs poking their OWN side panel most (the panels hung against the thighs: 4.8% poke at rest)
        SIDE = float(opt('--side', '0.0'))
        _x = np.where(_back, 0.0, np.sign(xs) * SIDE * _u)
        Mi = np.linalg.inv(np.array(pc.matrix_world)); co = Pw + np.c_[_x, _d, np.zeros_like(_d)]
        pc.data.vertices.foreach_set('co', (co @ Mi[:3, :3].T + Mi[:3, 3]).ravel()); pc.data.update(); Pw = world(pc)
        r_flare = dict(flare_m=FLARE, side_m=SIDE, split_edges=r_split)
        # PANEL PER VERTEX FROM ITS FACES, not its position: a split leaves two copies of a boundary vertex at ONE position, and a
        # position rule gave both copies the same panel (e18: back-panel faces still pulled by a thigh, 5-7x). Each copy takes
        # the panel of the faces that use it.
        _fl = {}
        for poly in pc.data.polygons:
            cxp = float(np.mean([xs[v] for v in poly.vertices]))
            lab = 1 if cxp > SLIT else (-1 if cxp < -SLIT else 0)
            for v in poly.vertices: _fl.setdefault(v, []).append(lab)
        panel = np.array([max(set(_fl.get(i, [0])), key=_fl.get(i, [0]).count) for i in range(len(xs))])   # +1 his LEFT (+X), -1 RIGHT, 0 back
        # top: nearest-body weights; blend to the panel rule between HIP+0.15 and HIP
        for n in names:
            if n not in pc.vertex_groups: pc.vertex_groups.new(name=n)
        top = np.zeros((len(Pw), len(names)), np.float32)
        for i, p in enumerate(Pw):
            hit = tree.find_nearest(Vector(p.tolist()))
            if hit[0] is None: continue
            t = BT[hit[2]]; top[i] = W[t].mean(0)
        ni = {n: i for i, n in enumerate(names)}
        # TORSO BONES ONLY: the cape's upper edge lies beside his A-pose arms, and nearest-body weights there picked up the
        # arms -- the first stride test measured edges stretched 30x as the arms swung (e15). A cape hangs from the shoulders.
        TORSO = [n for n in ('Hips', 'Spine', 'Spine01', 'Spine02', 'neck') if n in ni]   # shoulders out too: e18 found 5-7x stretch where the walk's shoulder roll met the Hips
        keep = np.zeros(len(names), bool); keep[[ni[n] for n in TORSO]] = True; top[:, ~keep] = 0
        top[top.sum(1) <= 0, ni['Spine02']] = 1.0
        top /= np.maximum(top.sum(1, keepdims=True), 1e-9)
        # SMOOTH TOP (e18 v3: neighbouring top vertices took Spine or Spine02 from whichever body triangle was nearest, and the
        # walk's torso twist pulled them 3-6x apart). A cape hangs from the shoulder line: the top is Spine02 above HIP+0.20,
        # blending linearly to the Hips at the hip line -- one smooth field, no per-vertex jumps.
        _v = np.clip((zf - HIP) / 0.20, 0, 1)
        top[:] = 0; top[:, ni['Spine02']] = _v; top[:, ni['Hips']] = 1 - _v
        low = np.zeros_like(top)
        THIGH = float(opt('--thigh', '0.5')); RAMP = opt('--ramp', 'knee')   # stage G (b): 'hem' = a linear ramp hip -> hem reaching THIGH at the hem
        u = (np.clip((HIP - zf) / max(HIP - zf.min(), 1e-6), 0, 1) if RAMP == 'hem' else np.clip((HIP - zf) / 0.30, 0, 1)) * THIGH
        low[:, ni['Hips']] = 1.0
        for side, leg in ((1, 'LeftUpLeg'), (-1, 'RightUpLeg')):
            k = panel == side
            low[k, ni[leg]] = u[k]; low[k, ni['Hips']] = 1.0 - u[k]
        b = np.clip((zf - HIP) / 0.15, 0, 1)[:, None]                      # 1 = top rule, 0 = panel rule
        Wc = b * top + (1 - b) * low
        for gi, n in enumerate(names):
            idx = np.where(Wc[:, gi] > 0.002)[0]
            for i in idx: pc.vertex_groups[n].add([int(i)], float(Wc[i, gi]), 'REPLACE')
        m = pc.modifiers.new('arm', 'ARMATURE'); m.object = arm
        both = int(((Wc[:, ni['LeftUpLeg']] > 0) & (Wc[:, ni['RightUpLeg']] > 0)).sum())
        r.update(mode='panel-split skin', slit_x_m=round(float(SLIT), 4), hips_zf=round(HIP, 3), slit_faces_cut=len(kill),
                 panel_verts=dict(back=int((panel == 0).sum()), left=int((panel == 1).sum()), right=int((panel == -1).sum())),
                 verts_on_both_thighs=both, thigh=THIGH, ramp=RAMP, **r_flare)
    G.align_space(pc, body[0]); pc.name = nm
    r['file'] = export(pc, nm)
    rep['pieces'][nm] = r; print('GEAR', nm, json.dumps(r))
    bpy.data.objects.remove(pc, do_unlink=True)
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
