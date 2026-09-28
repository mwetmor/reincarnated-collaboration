# C-9 meshy_t2 step 2: put the manticore into the pipeline's canonical frame and
# measure every landmark a quadruped rig needs, from the geometry.
#
#   blender -b -noaudio --python scripts/02_orient.py -- <model.glb> <out.blend> <out.json> <viewdir>
#
# Canonical frame (the same one 04_render.py assumes for the knight):
#   Z up, the character FACING +Y, standing on z = 0, real scale in metres.
#
# Nothing about the incoming file is assumed:
#  * UP is decided by counting LEG CLUSTERS. Slice the bottom 12 % of each
#    candidate axis and count connected blobs in the plan view: a standing
#    quadruped has FOUR, and no other axis does. (The density test in step 1
#    could not separate X from Z -- 0.808 vs 0.815 -- so it is not used.)
#  * HEAD vs TAIL along the long axis by cross-section bulk (step 1: 1.696 vs
#    0.013, decisive).
#  * SCALE from withers height, not from the bbox: the bbox top is the man's
#    HEAD, which is held above the back, so scaling on it would make the animal
#    short. Withers = the back surface over the front legs.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix

a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUTBLEND, OUTP = a[0], a[1], a[2]
VIEWDIR = a[3] if len(a) > 3 else None
TARGET_WITHERS_M = 1.00          # "a large wolf, shoulder height about 1.0 m"


def verts_world(objs):
    out = []
    for o in objs:
        M = o.matrix_world
        co = np.empty(len(o.data.vertices) * 3)
        o.data.vertices.foreach_get("co", co)
        co = co.reshape(-1, 3) @ np.array(M.to_3x3()).T + np.array(M.translation)
        out.append(co)
    return np.vstack(out)


def blob_count(P, axis, frac=0.12, grid=48):
    """How many separate blobs does the bottom `frac` of `axis` make in plan?"""
    lo, hi = P[:, axis].min(), P[:, axis].max()
    sel = P[P[:, axis] < lo + frac * (hi - lo)]
    o = [i for i in range(3) if i != axis]
    if len(sel) < 20:
        return 0, 0
    u = sel[:, o]
    umin, umax = u.min(0), u.max(0)
    s = (u - umin) / np.maximum(umax - umin, 1e-9) * (grid - 1)
    occ = np.zeros((grid, grid), bool)
    occ[s[:, 0].astype(int), s[:, 1].astype(int)] = True
    # 4-connected flood fill
    seen = np.zeros_like(occ); n = 0; big = 0
    for i in range(grid):
        for j in range(grid):
            if occ[i, j] and not seen[i, j]:
                st = [(i, j)]; seen[i, j] = True; sz = 0
                while st:
                    x, y = st.pop(); sz += 1
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        p, q = x + dx, y + dy
                        if 0 <= p < grid and 0 <= q < grid and occ[p, q] and not seen[p, q]:
                            seen[p, q] = True; st.append((p, q))
                if sz >= 3:
                    n += 1; big = max(big, sz)
    return n, big


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=SRC)
    sc = bpy.context.scene
    objs = [o for o in sc.objects if o.type == 'MESH']
    P = verts_world(objs)
    rep = {}

    # ---- UP by leg-blob count --------------------------------------------
    span = P.max(0) - P.min(0)
    blobs = {}
    for ax in range(3):
        n, big = blob_count(P, ax)
        blobs["XYZ"[ax]] = dict(blobs=n, biggest_cells=big, span=round(float(span[ax]), 4))
    rep["up_by_leg_blobs"] = blobs
    up = min(range(3), key=lambda ax: (abs(blobs["XYZ"[ax]]["blobs"] - 4), -span[ax]))
    rep["up_axis"] = "XYZ"[up]
    long_axis = int(np.argmax(span))
    rep["long_axis"] = "XYZ"[long_axis]
    width_axis = [i for i in range(3) if i not in (up, long_axis)][0]

    # ---- head end along the long axis (bulk) -----------------------------
    t = (P[:, long_axis] - P[:, long_axis].min()) / max(span[long_axis], 1e-9)
    k = 0.15
    bulk_lo = np.prod(P[t < k][:, [width_axis, up]].max(0) - P[t < k][:, [width_axis, up]].min(0))
    bulk_hi = np.prod(P[t > 1 - k][:, [width_axis, up]].max(0) - P[t > 1 - k][:, [width_axis, up]].min(0))
    head_low = bulk_lo > bulk_hi
    rep["head_end"] = dict(low=bool(head_low), bulk_low=round(float(bulk_lo), 5),
                           bulk_high=round(float(bulk_hi), 5))

    # ---- build the transform: up->+Z, long->+Y with the HEAD at +Y -------
    # basis columns: new X = width, new Y = long (flipped if the head is low),
    # new Z = up. Determinant forced to +1 so the mesh is not mirrored.
    B = np.zeros((3, 3))
    B[width_axis, 0] = 1.0
    B[long_axis, 1] = -1.0 if head_low else 1.0
    B[up, 2] = 1.0
    if np.linalg.det(B) < 0:
        B[:, 0] *= -1
    Rm = Matrix(B.T.tolist())          # world -> canonical
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = Rm.to_4x4() @ o.matrix_world
    P = verts_world(objs)
    # drop to the ground and centre laterally on the body's own midline
    P2 = P.copy()
    dz = -P2[:, 2].min()
    dx = -float(np.median(P2[:, 0]))
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = Matrix.Translation(Vector((dx, 0.0, dz))) @ o.matrix_world
    P = verts_world(objs)

    # ---- withers: the top of the back over the front legs ----------------
    # front-leg band = the Y range of the two front paws (found below), but the
    # withers can be read first as the back surface just BEHIND the neck: take
    # the Y slice 0.55..0.70 of the way from tail to head and its highest
    # BODY vertex (the head/mane is further forward and is excluded by the
    # slice, which is why the slice is used rather than the bbox).
    ymin, ymax = P[:, 1].min(), P[:, 1].max()
    L = ymax - ymin

    def band(a0, a1):
        m = (P[:, 1] >= ymin + a0 * L) & (P[:, 1] <= ymin + a1 * L)
        return P[m]

    prof = []
    for i in range(40):
        s = band(i / 40.0, (i + 1) / 40.0)
        prof.append(dict(i=i, y0=round(float(ymin + i * L / 40), 4), n=len(s),
                         ztop=round(float(s[:, 2].max()), 4) if len(s) else 0.0,
                         zbot=round(float(s[:, 2].min()), 4) if len(s) else 0.0,
                         xext=round(float(s[:, 0].max() - s[:, 0].min()), 4) if len(s) else 0.0))
    rep["profile_canonical"] = prof

    # ---- paws: cluster the bottom slab in plan ---------------------------
    zlo = P[:, 2].min(); zhi = P[:, 2].max()
    foot = P[P[:, 2] < zlo + 0.09 * (zhi - zlo)]
    paws = []
    if len(foot) > 20:
        pts = foot[:, :2]
        # split left/right on x = 0, then front/back on the y median of each side
        for sx, msk in (("r", pts[:, 0] > 0), ("l", pts[:, 0] <= 0)):
            side = foot[msk]
            if len(side) < 10:
                continue
            ym = np.median(side[:, 1])
            for sy, m2 in (("f", side[:, 1] > ym), ("h", side[:, 1] <= ym)):
                g = side[m2]
                if len(g) < 5:
                    continue
                paws.append(dict(name=sy + sx, n=len(g),
                                 x=round(float(g[:, 0].mean()), 4),
                                 y=round(float(g[:, 1].mean()), 4),
                                 z=round(float(g[:, 2].min()), 4),
                                 xr=[round(float(g[:, 0].min()), 4), round(float(g[:, 0].max()), 4)],
                                 yr=[round(float(g[:, 1].min()), 4), round(float(g[:, 1].max()), 4)]))
    rep["paws_model_units"] = paws

    # withers from the back line over the front paws
    fy = np.mean([p["y"] for p in paws if p["name"][0] == "f"]) if paws else ymin + 0.65 * L
    hy = np.mean([p["y"] for p in paws if p["name"][0] == "h"]) if paws else ymin + 0.25 * L
    w = band((fy - ymin) / L - 0.04, (fy - ymin) / L + 0.06)
    # exclude the neck/mane: keep only vertices whose |x| shows a BODY cross
    # section (the mane is wide too), so instead take the back surface at the
    # midline: |x| < 0.06 of the width, highest z, within the slice just BEHIND
    # the front legs.
    wb = band((fy - ymin) / L - 0.10, (fy - ymin) / L - 0.01)
    mid = wb[np.abs(wb[:, 0]) < 0.08 * (P[:, 0].max() - P[:, 0].min())]
    withers = float(mid[:, 2].max()) if len(mid) else float(w[:, 2].max())
    hb = band((hy - ymin) / L - 0.02, (hy - ymin) / L + 0.09)
    midh = hb[np.abs(hb[:, 0]) < 0.08 * (P[:, 0].max() - P[:, 0].min())]
    croup = float(midh[:, 2].max()) if len(midh) else 0.0

    rep["model_units"] = dict(
        bbox_lo=[round(float(v), 5) for v in P.min(0)],
        bbox_hi=[round(float(v), 5) for v in P.max(0)],
        body_len_y=round(float(L), 5),
        withers_z=round(withers, 5), croup_z=round(croup, 5),
        head_top_z=round(float(zhi), 5),
        front_paw_y=round(float(fy), 5), hind_paw_y=round(float(hy), 5))

    S = TARGET_WITHERS_M / withers
    rep["scale_factor"] = round(S, 6)
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = Matrix.Scale(S, 4) @ o.matrix_world
    P = verts_world(objs)
    rep["metres"] = dict(
        withers_m=round(float(TARGET_WITHERS_M), 4),
        croup_m=round(croup * S, 4),
        head_top_m=round(float(P[:, 2].max()), 4),
        nose_to_tailtip_m=round(float(P[:, 1].max() - P[:, 1].min()), 4),
        width_m=round(float(P[:, 0].max() - P[:, 0].min()), 4),
        paws=[dict(name=p["name"], x=round(p["x"] * S, 4), y=round(p["y"] * S, 4))
              for p in paws])

    bpy.ops.wm.save_as_mainfile(filepath=OUTBLEND)
    json.dump(rep, open(OUTP, "w"), indent=1)
    print("up=%s long=%s head_low=%s  scale x%.4f" % (rep["up_axis"], rep["long_axis"],
                                                      head_low, S))
    print("blobs:", {k: v["blobs"] for k, v in blobs.items()})
    print("metres:", json.dumps(rep["metres"], indent=1))

    # ---- optional: three ortho views so the orientation can be SEEN -------
    if VIEWDIR:
        os.makedirs(VIEWDIR, exist_ok=True)
        for o in objs:
            for slot in o.material_slots:
                m = slot.material
                if not m or not m.use_nodes:
                    continue
                nt = m.node_tree
                out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
                em = nt.nodes.new('ShaderNodeEmission')
                bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if bsdf and bsdf.inputs['Base Color'].links:
                    nt.links.new(bsdf.inputs['Base Color'].links[0].from_socket, em.inputs['Color'])
                nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
        cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
        sc.collection.objects.link(cam); sc.camera = cam
        cam.data.type = 'ORTHO'
        ctr = Vector(((P[:, 0].min() + P[:, 0].max()) / 2, (P[:, 1].min() + P[:, 1].max()) / 2,
                      (P[:, 2].min() + P[:, 2].max()) / 2))
        ext = max(P.max(0) - P.min(0)) * 1.1
        cam.data.ortho_scale = ext
        sc.render.resolution_x = 700; sc.render.resolution_y = 700
        sc.render.film_transparent = True
        sc.view_settings.view_transform = 'Standard'
        for nm, d in (("right_+X", Vector((1, 0, 0))), ("front_-Y", Vector((0, -1, 0))),
                      ("top_+Z", Vector((0, 0, 1)))):
            pos = ctr + d * 10
            cam.location = pos
            cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y' if nm != "top_+Z" else 'Z').to_euler()
            sc.render.filepath = os.path.join(VIEWDIR, "ortho_%s.png" % nm)
            bpy.ops.render.render(write_still=True)
        json.dump(dict(centre=[round(v, 4) for v in ctr], ortho_scale=round(ext, 4)),
                  open(os.path.join(VIEWDIR, "views.json"), "w"), indent=1)


main()
