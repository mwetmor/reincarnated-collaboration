# D2 shared fitting. Used by the swap renderer and by the hand-off exporter, so
# both bind a piece the same way.
#
# WHY INLINE. The first design exported each fitted piece as its own skinned
# GLB and re-imported it to assemble. Every piece came back collapsed into a
# 2 mm speck -- in the FILE's vertex data, not on import -- because a skinned
# glTF round trip does not preserve a mesh that carries its own object
# transform, and applying the transform before export did not save it either.
# Fitting in the same session that renders removes the round trip and the
# failure mode with it. The hand-off is exported ONCE, from the assembled
# scene, rather than piece by piece and re-imported.
import bpy, os
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree


def body_sampler(body):
    body.data.calc_loop_triangles()
    co = np.empty(len(body.data.vertices) * 3)
    body.data.vertices.foreach_get("co", co)
    BV = (co.reshape(-1, 3) @ np.array(body.matrix_world.to_3x3()).T
          + np.array(body.matrix_world.translation))
    BT = np.array([list(t.vertices) for t in body.data.loop_triangles])
    names = [g.name for g in body.vertex_groups]
    W = np.zeros((len(BV), len(names)), np.float32)
    for vi, v in enumerate(body.data.vertices):
        for ge in v.groups:
            W[vi, ge.group] = ge.weight
    tree = BVHTree.FromPolygons([Vector(p) for p in BV.tolist()],
                                [list(map(int, f)) for f in BT])
    return BV, BT, names, W, tree


def import_piece(path, existing):
    bpy.ops.import_scene.gltf(filepath=path)
    added = [o for o in bpy.context.scene.objects if o not in existing]
    meshes = [o for o in added if o.type == 'MESH' and len(o.data.vertices) > 200]
    for o in [o for o in added if o not in meshes]:
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    pc = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return pc


def decimate(pc, faces):
    n0 = len(pc.data.polygons)
    if n0 > faces:
        bpy.ops.object.select_all(action='DESELECT')
        pc.select_set(True); bpy.context.view_layer.objects.active = pc
        m = pc.modifiers.new('dec', 'DECIMATE'); m.ratio = faces / n0
        bpy.ops.object.modifier_apply(modifier='dec')
    return n0, len(pc.data.polygons)


def clear_body(pc, tree, offset):
    """Push the piece out along its normals, then out of anything still inside.
    The piece was cut from a build of the DRESSED body and the body beneath is
    a different generation, so they interpenetrate before anything animates."""
    pc.data.calc_loop_triangles()
    co = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get("co", co)
    P = co.reshape(-1, 3)
    nm = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get("normal", nm)
    P = P + nm.reshape(-1, 3) * offset
    pushed = 0
    for i, p in enumerate(P):
        hit = tree.find_nearest(Vector(p.tolist()))
        if hit[0] is None:
            continue
        if (Vector(p.tolist()) - hit[0]).dot(hit[1]) < 0:
            P[i] = np.array((hit[0] + hit[1] * offset).to_tuple()); pushed += 1
    pc.data.vertices.foreach_set("co", P.ravel()); pc.data.update()
    return P, pushed


def align_space(pc, body):
    """Move the piece into the BODY's object space and give it the body's
    transform and parenting.

    Meshy's rigged GLB carries a 0.01 object scale on the skinned mesh -- the
    vertex data is 100x life size and the object shrinks it back. A piece built
    in metres, parented to that armature, is therefore scaled by 0.01 and
    collapses to a 1.7 cm speck sitting at the ankles. That is what made every
    fitted piece vanish, and it read as a broken glTF round trip because the
    exported file inherited the same collapse.

    A skinned mesh must share its body's space exactly, so the data is moved
    into it rather than the object being given a compensating transform."""
    M = body.matrix_world.copy()
    Mi = M.inverted()
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    P = co.reshape(-1, 3)
    Pw = P @ np.array(pc.matrix_world.to_3x3()).T + np.array(pc.matrix_world.translation)
    Pl = Pw @ np.array(Mi.to_3x3()).T + np.array(Mi.translation)
    pc.data.vertices.foreach_set("co", Pl.ravel())
    pc.data.update()
    pc.parent = body.parent
    pc.matrix_parent_inverse = body.matrix_parent_inverse.copy()
    pc.matrix_basis = body.matrix_basis.copy()
    return Pw


def skin_to_body(pc, P, BV, BT, names, W, tree, arm):
    for n in names:
        if n not in pc.vertex_groups:
            pc.vertex_groups.new(name=n)
    ok = 0
    for i, p in enumerate(P):
        hit = tree.find_nearest(Vector(p.tolist()))
        if hit[0] is None:
            continue
        t = BT[hit[2]]
        q = np.array(hit[0].to_tuple())
        a0, b0, c0 = BV[t[0]], BV[t[1]], BV[t[2]]
        n = np.cross(b0 - a0, c0 - a0)
        A2 = float(np.dot(n, n)) or 1e-12
        w = np.clip([np.dot(np.cross(b0 - q, c0 - q), n) / A2,
                     np.dot(np.cross(c0 - q, a0 - q), n) / A2, 0.0], 0, 1)
        w[2] = max(0.0, 1.0 - w[0] - w[1])
        w = w / max(w.sum(), 1e-9)
        wv = w[0] * W[t[0]] + w[1] * W[t[1]] + w[2] * W[t[2]]
        s = wv.sum()
        if s <= 0:
            continue
        wv /= s
        for gi in np.where(wv > 0.002)[0]:
            pc.vertex_groups[names[gi]].add([i], float(wv[gi]), 'REPLACE')
        ok += 1
    m = pc.modifiers.new('arm', 'ARMATURE'); m.object = arm
    return ok


def bone_bind(pc, arm, bones, split):
    parts = [pc]
    if split:
        bpy.ops.object.select_all(action='DESELECT')
        pc.select_set(True); bpy.context.view_layer.objects.active = pc
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
        parts = [o for o in bpy.context.selected_objects if o.type == 'MESH']
    out = []
    for o in parts:
        cv = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", cv)
        ctr = (cv.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
               + np.array(o.matrix_world.translation)).mean(0)
        best = min(bones, key=lambda bn: np.linalg.norm(
            ctr - np.array(arm.matrix_world @ arm.pose.bones[bn].head)))
        g = o.vertex_groups.new(name=best)
        g.add(list(range(len(o.data.vertices))), 1.0, 'REPLACE')
        m = o.modifiers.new('arm', 'ARMATURE'); m.object = arm
        out.append((o, best))
    return out


def socket_weapon(pc, arm, bone, length, grip, axis_hint=None, extra_rot=None,
                  lateral=0.0):
    """Scale a weapon to a real length, lay it along the bone, put its GRIP on
    the bone's head, and parent it there.

    The long axis and which end is the head are MEASURED from the mesh's own
    cross-section profile rather than assumed: a Tripo build arrives
    height-normalised and yawed, so 'up' means nothing until it is measured.
    """
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    V = (co.reshape(-1, 3) @ np.array(pc.matrix_world.to_3x3()).T
         + np.array(pc.matrix_world.translation))
    span = V.max(0) - V.min(0)
    la = int(np.argmax(span)) if axis_hint is None else axis_hint
    s = length / max(span[la], 1e-9)
    V = V * s
    # which end is the head? the fatter one, by cross-section
    t = (V[:, la] - V[:, la].min()) / max(V[:, la].max() - V[:, la].min(), 1e-9)
    oth = [i for i in range(3) if i != la]
    def bulk(m):
        q = V[m][:, oth]
        return float(np.prod(q.max(0) - q.min(0))) if m.sum() > 10 else 0.0
    head_max = bulk(t > 0.75) > bulk(t < 0.25)
    # weapon-local frame: L along the long axis pointing TOWARDS the head
    L = np.zeros(3); L[la] = 1.0 if head_max else -1.0
    gp = V[:, la].min() + grip * (V[:, la].max() - V[:, la].min()) if head_max else \
         V[:, la].max() - grip * (V[:, la].max() - V[:, la].min())
    origin = np.array([np.median(V[:, oth[0]]), 0.0, 0.0])
    ctr = V.mean(0).copy(); ctr[la] = gp
    V = V - ctr
    pb = arm.pose.bones[bone]
    bh = np.array(arm.matrix_world @ pb.head)
    by = np.array((arm.matrix_world.to_3x3() @ pb.y_axis).normalized())
    bx = np.array((arm.matrix_world.to_3x3() @ pb.x_axis).normalized())
    bz = np.array((arm.matrix_world.to_3x3() @ pb.z_axis).normalized())
    R = np.stack([bx, by, bz], 1)           # weapon axes -> bone axes
    M = np.zeros((3, 3))
    M[:, la] = by
    o0, o1 = oth
    M[:, o0] = bx
    M[:, o1] = bz
    if not head_max:
        M[:, la] *= -1
    if extra_rot is not None:
        M = np.array(extra_rot) @ M
    V = V @ M.T + bh + by * 0.0 + bx * lateral
    pc.data.vertices.foreach_set("co", V.ravel())
    pc.matrix_world = Matrix.Identity(4)
    pc.data.update()
    g = pc.vertex_groups.new(name=bone)
    g.add(list(range(len(pc.data.vertices))), 1.0, 'REPLACE')
    m = pc.modifiers.new('arm', 'ARMATURE'); m.object = arm
    return dict(scale=round(float(s), 5), long_axis="XYZ"[la],
                head_end="max" if head_max else "min", bone=bone,
                length_m=length, grip_frac=grip)
