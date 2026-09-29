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


def helmet_on_key(body, helmet, arm, clearance=0.010, name="helmet_on"):
    """A shape key that compresses the hair UNDER the helmet.

    The dome was invisible because the base build's hair is a solid volume that
    the helmet sits inside: he read as wearing a brow band with red braids on
    top. Offsetting the helmet outward was the wrong fix -- it flattens the
    helmet onto the scalp. Games move the HAIR, not the hat.

    Every candidate vertex is tested by casting a ray OUTWARD from the head
    centre through it. If that ray meets the helmet, the vertex lies under the
    dome, and it is pulled back along the same ray to just inside the helmet's
    surface. A radial test is what "under the dome" actually means, and it
    leaves the braid and the beard alone by construction: they hang below the
    rim, so a ray through them does not meet the helmet.

    Returns (moved, tested, key) so the caller can report rather than assert.
    """
    from mathutils.bvhtree import BVHTree
    # matrix_world is only recomputed on depsgraph evaluation, and align_space
    # has just changed it. Without this the helmet reads at its pre-parenting
    # transform and the candidate box comes back EMPTY -- "0 of 0", which looks
    # like a wrong predicate and is a stale matrix. Third time this has bitten
    # in this run.
    bpy.context.view_layer.update()
    # THE BVH IS BUILT IN WORLD SPACE. align_space() gives every piece the
    # body's object transform, and Meshy ships that body at 0.01 scale -- so a
    # ray cast in the helmet's LOCAL space with a 1.0 distance reaches one
    # centimetre and hits nothing. The first version of this returned "0 of
    # 15523 moved", which looks exactly like a mis-aimed ray and was a unit.
    hco = np.empty(len(helmet.data.vertices) * 3)
    helmet.data.vertices.foreach_get("co", hco)
    HW = (hco.reshape(-1, 3) @ np.array(helmet.matrix_world.to_3x3()).T
          + np.array(helmet.matrix_world.translation))
    helmet.data.calc_loop_triangles()
    HT = [list(map(int, t.vertices)) for t in helmet.data.loop_triangles]
    hb = BVHTree.FromPolygons([Vector(p) for p in HW.tolist()], HT)
    hz0, hz1 = float(HW[:, 2].min()), float(HW[:, 2].max())
    C = np.array(arm.matrix_world @ arm.pose.bones["Head"].head)
    C[2] = hz0 + 0.30 * (hz1 - hz0)          # centre inside the dome, not the neck

    if not body.data.shape_keys:
        body.shape_key_add(name="Basis", from_mix=False)
    key = body.shape_key_add(name=name, from_mix=False)
    M = body.matrix_world
    Mi = M.inverted()
    co = np.empty(len(body.data.vertices) * 3)
    body.data.vertices.foreach_get("co", co)
    P = co.reshape(-1, 3)
    PW = P @ np.array(M.to_3x3()).T + np.array(M.translation)
    # candidates: at or above the helmet's rim, within its lateral reach
    cand = np.where((PW[:, 2] > hz0 - 0.01) &
                    (np.linalg.norm(PW[:, :2] - C[:2], axis=1) < 0.30))[0]
    print("      helmet world z %.3f..%.3f, ray centre %s; body z %.3f..%.3f; "
          "%d candidates" % (hz0, hz1, np.round(C, 3), PW[:, 2].min(),
                             PW[:, 2].max(), len(cand)))
    moved = 0
    for i in cand:
        v = PW[i]
        d = v - C
        L = float(np.linalg.norm(d))
        if L < 1e-5:
            continue
        dirn = d / L
        # TWO TESTS, because one radial ray is not enough. A ray from the head
        # centre through a hair vertex catches everything directly under the
        # dome, and MISSES hair that leaves the scalp at a grazing angle and
        # re-emerges through the shell further out -- which left 24% of the
        # helmet's silhouette still showing hair. The second test asks the
        # other question: is this vertex on the OUTSIDE of the helmet surface
        # and close to it? If so it is poking through, wherever the ray went.
        hit = hb.ray_cast(Vector(C.tolist()), Vector(dirn.tolist()), 1.0)
        if hit[0] is not None:
            h = float((hit[0] - Vector(C.tolist())).length)
            if L > h - clearance:
                nw = C + dirn * max(h - clearance, 0.01)
                key.data[int(i)].co = Mi @ Vector(nw.tolist())
                moved += 1
                continue
        near = hb.find_nearest(Vector(v.tolist()), 0.06)
        if near[0] is None:
            continue
        outward = (Vector(v.tolist()) - near[0]).dot(near[1])
        if outward > -clearance:
            nw = np.array((near[0] - near[1] * clearance).to_tuple())
            key.data[int(i)].co = Mi @ Vector(nw.tolist())
            moved += 1
    return moved, len(cand), key


def socket_weapon2(pc, arm, bone, length, grip, axis_world, face_world,
                   offset_world=(0, 0, 0), anchor="head"):
    """Place a weapon with an EXPLICIT orientation, at rest.

    The first version mapped the piece's LONG AXIS to the bone axis and let the
    rest follow. That is wrong for a shield, whose long axis is arbitrary --
    it is a disc, and the only direction that means anything is its NORMAL --
    and it hung the axe down past the knee. So the caller states the two
    directions that matter and they are measured on the mesh, not assumed:

      axis_world   where the weapon's own long axis should point, in world
                   space at rest. For the axe that is up, so the head is up.
                   For the shield it is the disc's normal, pointing outward.
      face_world   where the weapon's LATERAL feature should point -- the axe's
                   cutting edge, the shield's boss. Measured as the direction
                   from the long axis to the mass at the head end.

    Binding is by vertex group and an armature modifier, not by a parent
    transform, so getting the REST pose right is the whole job: the bone then
    carries it through every clip.
    """
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    V = (co.reshape(-1, 3) @ np.array(pc.matrix_world.to_3x3()).T
         + np.array(pc.matrix_world.translation))
    span = V.max(0) - V.min(0)
    la = int(np.argmax(span))
    if anchor == "normal":                 # a disc: the long axis is the THIN one
        la = int(np.argmin(span))
    s = length / max(span[int(np.argmax(span))], 1e-9)
    V = V * s
    lo, hi = V[:, la].min(), V[:, la].max()
    t = (V[:, la] - lo) / max(hi - lo, 1e-9)
    oth = [i for i in range(3) if i != la]

    def bulk(m):
        if m.sum() < 10:
            return 0.0
        q = V[m][:, oth]
        return float(np.prod(q.max(0) - q.min(0)))
    head_max = bulk(t > 0.75) > bulk(t < 0.25)
    # the lateral feature: where the mass sits at the head end, off the axis
    hm = (t > 0.70) if head_max else (t < 0.30)
    axis_mid = np.array([np.median(V[:, oth[0]]), np.median(V[:, oth[1]])])
    off = V[hm][:, oth].mean(0) - axis_mid if hm.sum() > 10 else np.array([1.0, 0.0])
    F = np.zeros(3)
    F[oth[0]], F[oth[1]] = off[0], off[1]
    if np.linalg.norm(F) < 1e-9:
        F[oth[0]] = 1.0
    F = F / np.linalg.norm(F)
    L = np.zeros(3); L[la] = 1.0 if head_max else -1.0
    # grip point along the long axis, measured from the BUTT end
    gp = (lo + grip * (hi - lo)) if head_max else (hi - grip * (hi - lo))
    ctr = np.array([np.median(V[:, 0]), np.median(V[:, 1]), np.median(V[:, 2])])
    ctr[la] = gp
    V = V - ctr
    # build the rotation: L -> axis_world, F -> face_world (orthogonalised)
    A = np.array(axis_world, float); A /= np.linalg.norm(A)
    Fw = np.array(face_world, float)
    Fw = Fw - A * float(Fw @ A)
    Fw /= max(np.linalg.norm(Fw), 1e-9)
    Tw = np.cross(A, Fw)
    Tl = np.cross(L, F)
    Msrc = np.stack([L, F, Tl], 1)
    Mdst = np.stack([A, Fw, Tw], 1)
    R = Mdst @ np.linalg.inv(Msrc)
    bh = np.array(arm.matrix_world @ arm.pose.bones[bone].head)
    V = V @ R.T + bh + np.array(offset_world, float)
    pc.data.vertices.foreach_set("co", V.ravel())
    pc.matrix_world = Matrix.Identity(4)
    pc.data.update()
    g = pc.vertex_groups.new(name=bone)
    g.add(list(range(len(pc.data.vertices))), 1.0, 'REPLACE')
    m = pc.modifiers.new('arm', 'ARMATURE'); m.object = arm
    return dict(scale=round(float(s), 5), long_axis="XYZ"[la],
                span_scaled_m=[round(float(v * s), 4) for v in span],
                bone_head=[round(float(v), 4) for v in bh],
                head_end="max" if head_max else "min", bone=bone,
                face_local=[round(float(v), 3) for v in F],
                axis_world=[round(float(v), 3) for v in A],
                face_world=[round(float(v), 3) for v in Fw])


def rescale_piece(pc, factor):
    """Scale a piece about the world origin.

    The pieces were isolated against the 1.70 m Meshy rig; the hand-off body is
    the T8 GLB at the declared 1.85 m. align_space preserves WORLD position, so
    a piece carried across keeps its 1.70 m size and floats: the helmet exported
    15 cm below the crown of the head it belongs to. The export's own scale step
    did not catch it, because that step measures the BODY -- which was already
    1.85 and needed no scaling -- and never looked at what it was scaling FOR.
    Both bodies have feet on z = 0 and midline x = 0, so a scale about the
    origin is the whole correction.
    """
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    P = co.reshape(-1, 3)
    W = P @ np.array(pc.matrix_world.to_3x3()).T + np.array(pc.matrix_world.translation)
    W = W * factor
    Mi = pc.matrix_world.inverted()
    L = W @ np.array(Mi.to_3x3()).T + np.array(Mi.translation)
    pc.data.vertices.foreach_set("co", L.ravel())
    pc.data.update()
    return factor
