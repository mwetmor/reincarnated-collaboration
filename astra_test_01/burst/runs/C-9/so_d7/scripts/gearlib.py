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
    # DROP THE SLIVERS. Decimating a two-piece mesh leaves a scatter of 1-7
    # triangle fragments -- the bracers exported as 10 objects, the pair plus
    # eight slivers totalling 17 triangles. They are not gear, they are
    # decimation debris, and every one of them becomes a node the scene has to
    # bind. Anything under 1% of the largest part goes.
    if len(parts) > 1:
        sizes = [(len(o.data.polygons), o) for o in parts]
        biggest = max(n for n, _ in sizes)
        drop = [o for n, o in sizes if n < max(0.01 * biggest, 8)]
        for o in drop:
            bpy.data.objects.remove(o, do_unlink=True)
        parts = [o for o in parts if o not in drop]
        if drop:
            print("      dropped %d sliver(s) of %d objects (largest %d tris)"
                  % (len(drop), len(sizes), biggest))
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


def axe_edge_marker(pc, arm, bone, name="axe_edge"):
    """A named empty on the cutting edge, parented to the weapon's bone.

    "The edge leads at the strike" was inferred from the head's mass
    distribution -- the vertex furthest from the hand. That is a proxy, and a
    proxy is what let a reversed pollaxe read as correct in a still. An empty
    ON the edge is the thing itself, and it travels in the GLB as a node the
    scene can read directly.

    The edge is measured: take the head end of the haft, then within it the
    vertices furthest from the haft axis -- that is the cutting arc, not the
    butt, not the socket.
    """
    # align_space has just changed this object's transform, and matrix_world is
    # only recomputed on depsgraph evaluation. Reading it stale put the edge
    # marker at 54.9 m instead of 0.549 -- a clean factor of 100, which is the
    # body's object scale, which is the same trap that collapsed every fitted
    # piece and blinded two helmet tests. Fifth time in this run; it is cheap
    # to prevent and expensive to diagnose.
    bpy.context.view_layer.update()
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    V = (co.reshape(-1, 3) @ np.array(pc.matrix_world.to_3x3()).T
         + np.array(pc.matrix_world.translation))
    bh = np.array(arm.matrix_world @ arm.pose.bones[bone].head)
    d = np.linalg.norm(V - bh, axis=1)
    head = V[d > np.percentile(d, 80)]                 # the business end
    axis = head.mean(0) - bh
    axis /= max(np.linalg.norm(axis), 1e-9)
    rel = head - bh
    lat = rel - np.outer(rel @ axis, axis)
    far = np.linalg.norm(lat, axis=1)
    edge = head[far > np.percentile(far, 85)]
    p = edge.mean(0)
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = 'PLAIN_AXES'
    e.empty_display_size = 0.05
    bpy.context.scene.collection.objects.link(e)
    e.parent = arm
    e.parent_type = 'BONE'
    e.parent_bone = bone
    b = arm.data.bones[bone]
    e.matrix_parent_inverse = Matrix.Translation(Vector((0, -b.length, 0)))
    e.matrix_world = Matrix.Translation(Vector(p.tolist()))
    return e, p, len(edge)


def grip_key(body, arm, bone, axis_pt, axis_dir, radius, name, weight_min=0.30):
    """A morph that closes a hand around a cylinder.

    This rig has NO FINGER BONES -- 24 bones, wrist straight to nothing -- so
    the hand cannot be posed. Meshy ships it open and flat from the A-pose, and
    an open flat hand can never look like it is holding anything. The fix is
    the same shape as helmet_on: move the MESH, driven by the equipment.

    Each hand vertex is pulled radially toward the weapon's own axis, weighted
    by how far it lies along the hand from the wrist -- the wrist does not move,
    the fingertips close completely. The hand's direction is measured from the
    mesh, NOT from the bone: RightHand is a childless leaf whose tail runs 24 m
    off into space, which is exactly the trap that cost a day on the knight.
    """
    gi = body.vertex_groups[bone].index
    sel, wts = [], []
    for v in body.data.vertices:
        for g in v.groups:
            if g.group == gi and g.weight > weight_min:
                sel.append(v.index); wts.append(g.weight)
                break
    if not sel:
        return None, 0, 0.0
    sel = np.array(sel)
    M = body.matrix_world
    co = np.empty(len(body.data.vertices) * 3)
    body.data.vertices.foreach_get("co", co)
    P = co.reshape(-1, 3)
    W = P @ np.array(M.to_3x3()).T + np.array(M.translation)
    wrist = np.array(arm.matrix_world @ arm.pose.bones[bone].head)
    d = np.linalg.norm(W[sel] - wrist, axis=1)
    far = W[sel][d > np.percentile(d, 75)]
    hand_dir = far.mean(0) - wrist
    hand_dir /= max(np.linalg.norm(hand_dir), 1e-9)
    hand_len = float(d.max()) or 1e-9
    A = np.array(axis_pt, float)
    U = np.array(axis_dir, float); U /= max(np.linalg.norm(U), 1e-9)
    if not body.data.shape_keys:
        body.shape_key_add(name="Basis", from_mix=False)
    key = body.shape_key_add(name=name, from_mix=False)
    Mi = M.inverted()
    moved, maxmove = 0, 0.0
    for k, vi in enumerate(sel):
        v = W[vi]
        alpha = float(np.clip(((v - wrist) @ hand_dir) / hand_len, 0.0, 1.0)) ** 1.2
        rel = v - A
        along = float(rel @ U)
        perp = rel - along * U
        r = float(np.linalg.norm(perp))
        if r < 1e-6:
            continue
        target = min(r, radius)
        newr = r * (1.0 - alpha) + target * alpha
        if abs(newr - r) < 1e-5:
            continue
        nv = A + along * U + perp * (newr / r)
        key.data[int(vi)].co = Mi @ Vector(nv.tolist())
        moved += 1
        maxmove = max(maxmove, float(np.linalg.norm(nv - v)))
    return key, moved, maxmove


def hand_frame(body, arm, bone, weight_min=0.30):
    """A fist's own axes, measured from the hand mesh.

    PCA over the hand's vertices gives three directions: along the hand
    (wrist to fingertips), ACROSS the palm -- which is the channel a gripped
    shaft runs through -- and the palm's normal. Taking the channel from the
    hand rather than from the weapon is what makes it work for both hands: the
    shield has no shaft to measure, and measuring the axe's gave a 4.7 cm
    "haft" radius because the blade sits near the fist.
    """
    gi = body.vertex_groups[bone].index
    idx = [v.index for v in body.data.vertices
           if any(g.group == gi and g.weight > weight_min for g in v.groups)]
    M = body.matrix_world
    co = np.empty(len(body.data.vertices) * 3)
    body.data.vertices.foreach_get("co", co)
    W = (co.reshape(-1, 3) @ np.array(M.to_3x3()).T + np.array(M.translation))[idx]
    c = W.mean(0)
    _, _, vt = np.linalg.svd(W - c, full_matrices=False)
    wrist = np.array(arm.matrix_world @ arm.pose.bones[bone].head)
    along = vt[0] if abs(vt[0] @ (c - wrist)) > abs(vt[1] @ (c - wrist)) else vt[1]
    along = along * (1.0 if along @ (c - wrist) > 0 else -1.0)
    rest = [v for v in (vt[0], vt[1], vt[2]) if abs(v @ along) < 0.9]
    channel = rest[0] if rest else vt[2]
    palm = np.cross(along, channel)
    return c, channel / np.linalg.norm(channel), along, palm / max(
        np.linalg.norm(palm), 1e-9)


def shaft_radius(pc, arm, bone, frac=0.30, band=0.05):
    """The radius of the weapon's SHAFT where the hand closes on it -- measured
    on the thin section near the bone, not on the whole silhouette. The blade
    sits close enough to the fist that a naive perpendicular spread there
    returned 0.0466 m: a 9 cm axe handle."""
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    V = (co.reshape(-1, 3) @ np.array(pc.matrix_world.to_3x3()).T
         + np.array(pc.matrix_world.translation))
    c = V.mean(0)
    _, _, vt = np.linalg.svd((V - c)[:: max(1, len(V) // 4000)], full_matrices=False)
    U = vt[0] / max(np.linalg.norm(vt[0]), 1e-9)
    bh = np.array(arm.matrix_world @ arm.pose.bones[bone].head)
    rel = V - bh
    along = rel @ U
    near = np.abs(along) < band
    if near.sum() < 30:
        return 0.02, U
    perp = rel[near] - np.outer(along[near], U)
    r = np.linalg.norm(perp, axis=1)
    # the SHAFT is the inner core; the blade is the outliers
    return float(np.percentile(r, 25)), U


def weapon_axis(pc, arm, bone):
    """The weapon's own long axis and a point on it, at the bone -- the channel
    a fist must close around."""
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    V = (co.reshape(-1, 3) @ np.array(pc.matrix_world.to_3x3()).T
         + np.array(pc.matrix_world.translation))
    c = V.mean(0)
    X = V - c
    u, sgl, vt = np.linalg.svd(X[:: max(1, len(X) // 4000)], full_matrices=False)
    U = vt[0] / max(np.linalg.norm(vt[0]), 1e-9)
    bh = np.array(arm.matrix_world @ arm.pose.bones[bone].head)
    # radius of the shaft near the bone: the spread perpendicular to U there
    rel = V - bh
    along = rel @ U
    near = V[np.abs(along) < 0.06]
    if len(near) > 20:
        rel2 = near - bh
        perp = rel2 - np.outer(rel2 @ U, U)
        rad = float(np.percentile(np.linalg.norm(perp, axis=1), 60))
    else:
        rad = 0.02
    return bh, U, rad


def centre_shaft_on_fist(pc, body, arm, bone, weight_min=0.30):
    """Slide a weapon along its own cross-section so its shaft axis passes
    THROUGH the fist, not beside it.

    Closing the hand is only half of "snapped to his grip": the close-ups
    showed a properly closed fist with the haft running past the knuckles.
    The weapon's ORIENTATION is deliberate -- the axe rides head-up -- so it is
    not re-aimed; it is translated perpendicular to its own shaft until the
    shaft's axis meets the centre of the hand.
    """
    co = np.empty(len(pc.data.vertices) * 3)
    pc.data.vertices.foreach_get("co", co)
    P = co.reshape(-1, 3)
    W = P @ np.array(pc.matrix_world.to_3x3()).T + np.array(pc.matrix_world.translation)
    c = W.mean(0)
    _, _, vt = np.linalg.svd((W - c)[:: max(1, len(W) // 4000)], full_matrices=False)
    U = vt[0] / max(np.linalg.norm(vt[0]), 1e-9)
    gi = body.vertex_groups[bone].index
    idx = [v.index for v in body.data.vertices
           if any(g.group == gi and g.weight > weight_min for g in v.groups)]
    Mb = body.matrix_world
    bco = np.empty(len(body.data.vertices) * 3)
    body.data.vertices.foreach_get("co", bco)
    BW = (bco.reshape(-1, 3) @ np.array(Mb.to_3x3()).T + np.array(Mb.translation))[idx]
    fist = BW.mean(0)
    # the shaft's axis near the fist, and the perpendicular offset to the fist
    rel = W - fist
    along = rel @ U
    near = np.abs(along) < 0.07
    base = W[near].mean(0) if near.sum() > 20 else c
    d = fist - base
    perp = d - (d @ U) * U
    Mi = pc.matrix_world.inverted()
    W2 = W + perp
    P2 = W2 @ np.array(Mi.to_3x3()).T + np.array(Mi.translation)
    pc.data.vertices.foreach_set("co", P2.ravel())
    pc.data.update()
    return float(np.linalg.norm(perp))


# ---- clip hygiene ---------------------------------------------------------
# Meshy's library clips arrive retargeted, and the retarget can ride in the
# clip as a JOINT SCALE. The barbarian's idle carried a constant Hips scale of
# 1.176471 -- exactly 20/17, a 1.70 m source retargeted to a 2.00 m target --
# on a rig that is 1.85 m. Hips is the skeleton root, so the whole character
# was 17.6% bigger whenever he stood still, and Matt found it by playing:
# "the walking is smaller than the running which is smaller than the idling."
#
# Nothing on the authoring side was going to call it wrong. It is valid glTF,
# it is what Meshy meant to write, and every clip looked correct on its own.
# It is only wrong RELATIVE TO THE OTHER CLIPS -- which is why the check that
# catches it (scripts/21_lint_export.py) reads the shipped file, and why the
# one that verifies the fix compares clips against each other.

def act_fcurves(act):
    """Blender 5.x moved fcurves into slotted action layers/strips/channelbags
    and removed act.fcurves. Handle both so this survives the next upgrade."""
    if hasattr(act, 'layers') and len(act.layers):
        out = []
        for layer in act.layers:
            for strip in layer.strips:
                for cb in getattr(strip, 'channelbags', []):
                    out.extend(cb.fcurves)
        return out
    return list(getattr(act, 'fcurves', []))


def strip_bone_scale(actions, tol=1e-3):
    """Set every pose-bone scale track to 1.0. Returns what it changed."""
    found = {}
    for act in actions:
        for fc in act_fcurves(act):
            if not fc.data_path.endswith('.scale'):
                continue
            vals = sorted({round(k.co[1], 6) for k in fc.keyframe_points})
            if all(abs(v - 1.0) <= tol for v in vals):
                continue
            bn = fc.data_path.split('"')[1] if '"' in fc.data_path else '?'
            found.setdefault(act.name, {}).setdefault(bn, set()).update(vals)
            for k in fc.keyframe_points:
                k.co[1] = k.handle_left[1] = k.handle_right[1] = 1.0
            fc.update()
    return {a: {b: sorted(v) for b, v in d.items()} for a, d in found.items()}


def shift_root(act, arm, bone, dz_world):
    """Add a constant world +Z offset to a root bone's location track.

    Pose location lives in the BONE'S OWN REST BASIS, not in world space, so a
    raw += on the Z channel is wrong for any rig whose root bone is not axis
    aligned -- and it would still look plausible. Convert through the bone's
    rest matrix, then VERIFY by measuring the feet again."""
    d_a = arm.matrix_world.inverted().to_3x3() @ Vector((0.0, 0.0, dz_world))
    d_b = arm.data.bones[bone].matrix_local.to_3x3().inverted() @ d_a
    n = 0
    for fc in act_fcurves(act):
        if fc.data_path != 'pose.bones["%s"].location' % bone:
            continue
        for k in fc.keyframe_points:
            k.co[1] += d_b[fc.array_index]
            k.handle_left[1] += d_b[fc.array_index]
            k.handle_right[1] += d_b[fc.array_index]
        fc.update()
        n += len(fc.keyframe_points)
    return [round(float(x), 6) for x in d_b], n


FOOT_BONES = ('LeftFoot', 'LeftToeBase', 'RightFoot', 'RightToeBase')


def foot_verts(ob, bones=FOOT_BONES):
    """Vertices whose DOMINANT group is a foot or toe. The lowest point of the
    whole mesh is usually the feet -- 'usually' is how a dropped hand or a
    hanging strap ends up defining where the floor is."""
    gi = {vg.index: vg.name for vg in ob.vertex_groups}
    keep = [v.index for v in ob.data.vertices if v.groups and
            gi.get(max(v.groups, key=lambda x: x.weight).group) in bones]
    return np.array(keep, dtype=int)


def world_verts(ob):
    """Deformed world-space vertices -- the skinned result, not the rest mesh."""
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get('co', co)
    co = co.reshape(-1, 3)
    M = np.array(ob.matrix_world)
    w = co @ M[:3, :3].T + M[:3, 3]
    ev.to_mesh_clear()
    return w


def foot_track(arm, meshes, act, masks):
    """Lowest foot height at every frame of a clip."""
    sc = bpy.context.scene
    prev = arm.animation_data.action
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    zs = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        lo = [world_verts(ob)[masks[ob.name]][:, 2].min()
              for ob in meshes if len(masks[ob.name])]
        zs.append(float(min(lo)))
    arm.animation_data.action = prev
    return np.array(zs)


def reground_from_feet(arm, meshes, act, bone='Hips', target=0.0, mode='min'):
    """Drop or lift a clip by ONE constant offset so its foot contact sits at
    `target`, derived from where the feet actually are.

    CONSTANT, not per frame. Per-frame grounding welds the feet to the floor
    and deletes whatever vertical motion the clip has -- on an idle that is the
    breathing, and the hips would gain a compensating counter-bob to pay for it.

    mode='min' puts the DEEPEST foot on the floor. mode='centre' centres the
    residual at (min+max)/2.

    CENTRE WAS THE ORIGINAL AND IT IS WRONG IN GENERAL. It was chosen against a
    single idle whose feet spanned 1.87 cm, where halving the error to +/-0.93
    cm was the whole point. Applied to clips with a real foot excursion it is a
    disaster: attack_chop's feet span -0.057 to +0.749 m (a leap), and centring
    put the planted foot 0.40 m UNDERGROUND -- taking a clip that was correct
    and breaking it. The deepest foot is the planted one, so grounding it is
    the rule that holds for an idle, a walk, a run with a flight phase and a
    leap alike.

    Not derived by dividing by the scale factor: the scale and the root
    translation came from the same retarget but they are not the same error,
    and the feet are the only ground truth available."""
    masks = {ob.name: foot_verts(ob) for ob in meshes}
    before = foot_track(arm, meshes, act, masks)
    dz = target - (float(before.min()) if mode == 'min'
                   else float(before.min() + before.max()) / 2.0)
    d_b, n = shift_root(act, arm, bone, dz)
    after = foot_track(arm, meshes, act, masks)
    return dict(dz=round(float(dz), 6), basis_delta=d_b, keys=n,
                before=dict(min=round(float(before.min()), 4),
                            max=round(float(before.max()), 4)),
                after=dict(min=round(float(after.min()), 4),
                           max=round(float(after.max()), 4),
                           worst_cm=round(float(np.abs(after).max()) * 100, 2)))


def bone_span(arm, pairs=(('LeftShoulder', 'RightShoulder'),
                          ('Head', 'head_end'),
                          ('LeftArm', 'LeftForeArm'))):
    """Distances between joint heads, in world space. THE DECISIVE INSTRUMENT
    for "is he bigger in this clip": a uniform scale changes every one of these
    and a pose change cannot change any of them, because they are rigid bone
    spans. Silhouette height mixes the two -- a bent knee shortens it just as a
    scale does -- so height alone can neither convict nor acquit."""
    bpy.context.view_layer.update()
    out = {}
    for a_, b_ in pairs:
        if a_ in arm.pose.bones and b_ in arm.pose.bones:
            pa = (arm.matrix_world @ arm.pose.bones[a_].matrix).translation
            pb = (arm.matrix_world @ arm.pose.bones[b_].matrix).translation
            out['%s-%s' % (a_, b_)] = round(float((pa - pb).length), 5)
    return out


# ---- armed carry: stop the weapon waffling in locomotion -------------------
# Matt: the axe "waffles back and forth awkwardly.. not the way someone should
# hold a weapon", and "the axe is better when idling."
#
# Measured (scripts/26_wrist.py), right wrist relative to forearm:
#   idle   71 deg/s p95, 1 reversal      <- the one he likes
#   walk  210 deg/s p95, 5 reversals
#   run   726 deg/s p95, 7 reversals
#
# The cause is that the Meshy walk and run are UNARMED motion. A free hand
# counter-rotates against the forearm through the stride; that reads as life on
# an empty hand and as flop on a rigid 0.8 m axe. So the fix is not to stop the
# arm swinging -- it is to stop the WRIST articulating independently, which is
# what a hand gripping a weapon actually does.
#
# Implemented as a blend toward a fixed carry angle rather than a hard clamp, so
# the hand keeps a little follow-through instead of looking welded.

def joint_rot(arm, child, parent):
    """Child's rotation in the parent's frame -- the joint angle, rest offset
    included. Whatever convention this uses, carry_lock must use the same one."""
    return (arm.pose.bones[parent].matrix.to_3x3().inverted()
            @ arm.pose.bones[child].matrix.to_3x3()).to_quaternion()


def mean_joint_rot(arm, act, child, parent, frames=None):
    """Average joint angle over a clip, by quaternion accumulation with sign
    alignment -- averaging raw components across a q/-q flip gives a rotation
    that is in neither half of the data."""
    sc = bpy.context.scene
    prev = arm.animation_data.action
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    acc, ref = None, None
    for f in (frames or range(f0, f1 + 1)):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        q = joint_rot(arm, child, parent)
        if ref is None:
            ref, acc = q.copy(), np.array([q.w, q.x, q.y, q.z], dtype=float)
        else:
            v = np.array([q.w, q.x, q.y, q.z], dtype=float)
            if float(np.dot(v, [ref.w, ref.x, ref.y, ref.z])) < 0:
                v = -v
            acc += v
    arm.animation_data.action = prev
    acc /= max(np.linalg.norm(acc), 1e-12)
    from mathutils import Quaternion
    return Quaternion((acc[0], acc[1], acc[2], acc[3]))


def carry_lock(arm, act, child, parent, target_q, alpha=0.85):
    """Blend a joint's rotation toward `target_q` across a whole clip.

    Two passes on purpose: READ every frame first, then write. A single pass
    would sample a hand this function has already moved, so the blend would
    compound frame over frame and drift -- and it would still produce smooth,
    plausible-looking output while doing it."""
    sc = bpy.context.scene
    prev = arm.animation_data.action
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    src, par = {}, {}
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        src[f] = joint_rot(arm, child, parent)
        par[f] = arm.pose.bones[parent].matrix.to_3x3().copy()
    pb = arm.pose.bones[child]
    pb.rotation_mode = 'QUATERNION'
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        q = src[f].slerp(target_q, alpha)
        keep = pb.matrix.translation.copy()
        m = (par[f] @ q.to_matrix()).to_4x4()
        m.translation = keep
        pb.matrix = m
        pb.keyframe_insert("rotation_quaternion", frame=f)
    arm.animation_data.action = prev
    return dict(child=child, parent=parent, alpha=alpha,
                frames=[f0, f1],
                target=[round(float(x), 6) for x in target_q])
