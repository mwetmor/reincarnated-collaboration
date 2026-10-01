# C-9 meshy_t2 shared primitives. Imported by every step so that "the canonical
# frame" and "the scale" mean exactly one thing across the pipeline.
#
# Canonical frame: Z up, facing +Y, feet on z = 0, midline x = 0, metres.
# Render constants: the KNIGHT's, because the two must share a world. The
# knight is 1.80 m tall and renders 198.333 px, so the world scale is
# 110.185 px/m -- and the manticore renders at that SAME px/m, which makes it
# 132 px tall rather than 198. Matching pixel HEIGHTS instead would have made a
# 1.2 m monster the size of a man.
import math
import numpy as np
from mathutils import Vector, Matrix

FRAME = 512
PX_PER_M = 198.33333333333334 / 1.80      # 110.1852, the knight's world scale
SOLE_Y = 398.0
ELEV = 19.77
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
TARGET_WITHERS_M = 1.00


def verts_world(objs):
    out = []
    for o in objs:
        M = o.matrix_world
        co = np.empty(len(o.data.vertices) * 3)
        o.data.vertices.foreach_get("co", co)
        out.append(co.reshape(-1, 3) @ np.array(M.to_3x3()).T + np.array(M.translation))
    return np.vstack(out)


def canonicalise(sc, objs):
    """Up by leg-blob count is settled in step 2 (Z, 4 blobs vs 3); here the
    cheap consequences are applied: long axis -> +Y with the bulky (head) end
    at +Y, feet to z = 0, midline to x = 0."""
    P = verts_world(objs)
    span = P.max(0) - P.min(0)
    la = int(np.argmax(span))
    t = (P[:, la] - P[:, la].min()) / span[la]
    others = [i for i in range(3) if i != la]
    bulk = [float(np.prod(P[m][:, others].max(0) - P[m][:, others].min(0)))
            for m in (t < 0.15, t > 0.85)]
    head_low = bulk[0] > bulk[1]
    B = np.zeros((3, 3)); B[0, 0] = 1.0
    B[la, 1] = -1.0 if head_low else 1.0
    B[2, 2] = 1.0
    if np.linalg.det(B) < 0:
        B[:, 0] *= -1
    R = Matrix(B.T.tolist()).to_4x4()
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = R @ o.matrix_world
    P = verts_world(objs)
    T = Matrix.Translation(Vector((-float(np.median(P[:, 0])), 0.0, -float(P[:, 2].min()))))
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = T @ o.matrix_world
    return dict(head_low=bool(head_low), bulk=[round(b, 5) for b in bulk])


def withers_break(P, nb=80):
    """Withers = the last midline topline bin before the MANE. Found as the
    single largest forward step in the topline (0.083 here, against a 0.005
    median), because on this creature the mane sits exactly over the withers
    and every "highest point above the front legs" measure returns the hair."""
    ymin, ymax = P[:, 1].min(), P[:, 1].max(); L = ymax - ymin
    hw = 0.15 * (P[:, 0].max() - P[:, 0].min()) / 2.0
    mid = P[np.abs(P[:, 0]) < hw]
    zt = []
    for i in range(nb):
        s = mid[(mid[:, 1] >= ymin + i * L / nb) & (mid[:, 1] < ymin + (i + 1) * L / nb)]
        zt.append(float(s[:, 2].max()) if len(s) else np.nan)
    zt = np.array(zt); d = np.diff(zt); ok = ~np.isnan(zt)
    i0, i1 = int(nb * 0.45), int(nb * 0.85)
    cand = [(float(d[i]), i) for i in range(i0, i1) if ok[i] and ok[i + 1]]
    brk = max(cand)[1] if cand else int(nb * 0.72)
    return float(zt[brk]), float(ymin + (brk + 0.5) * L / nb), brk, float(d[brk])


def apply_scale(sc, S):
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = Matrix.Scale(S, 4) @ o.matrix_world


def load_canonical(bpy, src):
    """Import, canonicalise, scale so the withers is 1.00 m. Returns
    (scene, [mesh objects], info)."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    sc = bpy.context.scene
    objs = [o for o in sc.objects if o.type == 'MESH']
    info = canonicalise(sc, objs)
    P = verts_world(objs)
    wz, wy, brk, step = withers_break(P)
    S = TARGET_WITHERS_M / wz
    apply_scale(sc, S)
    info.update(scale_factor=round(S, 6), withers_break_bin=brk,
                withers_raw_z=round(wz, 5), withers_y_m=round(wy * S, 5),
                topline_step_at_break=round(step, 5))
    return sc, objs, info


def vertex_colours_from_texture(obj):
    """Per-vertex base colour, sampled through the UV map.

    Used to separate the MAN's head (warm: flesh and blonde hair) from the
    hound's body (cold blue-grey). Geometry cannot do it -- the mane, the
    beard and the shoulders are one continuous surface -- but the texture can,
    and it is the same signal the eye uses.
    """
    me = obj.data
    img = None
    for slot in obj.material_slots:
        m = slot.material
        if not m or not m.node_tree:
            continue
        for n in m.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image:
                img = n.image; break
        if img:
            break
    if img is None:
        return None
    W, H = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)
    uvl = me.uv_layers.active.data
    nloop = len(me.loops)
    lv = np.empty(nloop, dtype=np.int32)
    me.loops.foreach_get("vertex_index", lv)
    uv = np.empty(nloop * 2, dtype=np.float32)
    uvl.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    u = np.clip((uv[:, 0] % 1.0) * (W - 1), 0, W - 1).astype(np.int32)
    v = np.clip((uv[:, 1] % 1.0) * (H - 1), 0, H - 1).astype(np.int32)
    c = px[v, u, :3]
    acc = np.zeros((len(me.vertices), 3), dtype=np.float64)
    cnt = np.zeros(len(me.vertices), dtype=np.int64)
    np.add.at(acc, lv, c)
    np.add.at(cnt, lv, 1)
    cnt = np.maximum(cnt, 1)
    return acc / cnt[:, None]


def unlit(objs, attr=None):
    """Emission shading; with `attr`, emit a named vertex-colour layer."""
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or not m.node_tree:
                continue
            nt = m.node_tree
            out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
            em = nt.nodes.new('ShaderNodeEmission')
            if attr:
                at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = attr
                nt.links.new(at.outputs['Color'], em.inputs['Color'])
            else:
                b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if b and b.inputs['Base Color'].links:
                    nt.links.new(b.inputs['Base Color'].links[0].from_socket, em.inputs['Color'])
            nt.links.new(em.outputs['Emission'], out.inputs['Surface'])


def place_camera(cam, az, aim_xy, aim_z, dist=20.0, elev=ELEV):
    A = math.radians(az); el = math.radians(elev)
    aim = Vector((aim_xy[0], aim_xy[1], aim_z))
    pos = aim + Vector((math.sin(A) * math.cos(el), math.cos(A) * math.cos(el),
                        math.sin(el))) * dist
    cam.location = pos
    cam.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler()
    return aim
