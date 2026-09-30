# T12 ranks 1 and 2: WEAPON BONES on every exported file -- and, with --roll, the axe's MOUNT as
# the rest of its bone. A binary glTF patch: nothing is re-exported through Blender, so nothing
# the patch does not name can change.
#
#   python3 scripts/52_weapon_bones.py --out <dir> <body.glb> <piece.glb> ... [--roll <deg>] [--json f]
#
# RANK 1 (always). `weapon_r` is added under RightHand and `weapon_l` under LeftHand in EVERY file,
# appended to the skin's joints in that order, so the body and every piece carry the identical
# 26 joints -- gear.gd compares the name lists, order included. A weapon piece (every vertex 100%
# on one hand) is rebound to its hand's weapon bone. Without --roll the bones are COINCIDENT with
# the hands (identity local, the hand's own inverse bind matrix): a rebind that moves nothing,
# proved per file by skinning every vertex at rest both ways.
#
# RANK 2 (--roll). weapon_r's rest becomes the axe's MOUNT: origin at the grip (the haft's own
# cross-section at the fist's centroid), +Y along the haft to the head, +Z toward the edge. The
# axe is re-seated onto it by the grip calibration G -- rotation Q about the grip P, in
# RightHand's local frame -- which is DERIVED HERE from the files, the way the D2 pipeline derives
# the fist (gearlib.hand_frame): the haft turned (shortest arc) onto the fist's CHANNEL, the
# across-palm axis of the hand vertices, which is also the axis grip_R closes round. The one free
# number is the roll about the haft; it is fitted in attack_lab against the strike clips
# (tools/grip_solve.gd) and passed in. Then
#     IBM_w = inverse(W) x IBM_hand        v' = inverse(IBM_hand) x G x IBM_hand x v
# so the axe draws at  hand x G  in every pose and weapon_r pivots at the grip. The axe_edge
# marker is re-parented under weapon_r and moved by G with the blade. weapon_l stays coincident:
# the shield's grip was fitted on its own (shield_centre_grip) and is not part of this.
import json, math, os, struct, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
L = __import__('21_lint_export')
R = __import__('49_recentre')

WEAPON_BONES = (("weapon_r", "RightHand"), ("weapon_l", "LeftHand"))
# THE BASE RIG'S JOINT ORDER is the order Blender's glTF exporter writes -- depth-first, so each
# weapon bone right after its hand. Measured: a 26-joint body with the weapon bones appended at the
# end came back from one Blender round trip with weapon_l moved up behind LeftHand. Every script
# after 15 re-exports through Blender, so only this order survives the chain.
BASE_RIG = L.BASE_RIG


def q2m(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def m2q(m):
    t = np.trace(m)
    if t > 0:
        s = math.sqrt(t + 1.0) * 2
        return np.array([(m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s, 0.25 * s])
    i = int(np.argmax(np.diag(m)))
    if i == 0:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        return np.array([0.25 * s, (m[0, 1] + m[1, 0]) / s, (m[0, 2] + m[2, 0]) / s, (m[2, 1] - m[1, 2]) / s])
    if i == 1:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        return np.array([(m[0, 1] + m[1, 0]) / s, 0.25 * s, (m[1, 2] + m[2, 1]) / s, (m[0, 2] - m[2, 0]) / s])
    s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
    return np.array([(m[0, 2] + m[2, 0]) / s, (m[1, 2] + m[2, 1]) / s, 0.25 * s, (m[1, 0] - m[0, 1]) / s])


def axis_angle(axis, ang):
    a = np.asarray(axis, float); a = a / np.linalg.norm(a)
    x, y, z = a * math.sin(ang / 2)
    return q2m((x, y, z, math.cos(ang / 2)))


def arc(u, v):
    """Shortest-arc rotation taking unit u onto unit v."""
    u = u / np.linalg.norm(u); v = v / np.linalg.norm(v)
    c = float(np.dot(u, v)); ax = np.cross(u, v); s = float(np.linalg.norm(ax))
    if s < 1e-12:
        return np.eye(3)
    return axis_angle(ax / s, math.atan2(s, c))


def trs(nd):
    M = np.eye(4)
    if 'matrix' in nd:
        return np.array(nd['matrix'], float).reshape(4, 4).T
    S = np.diag(list(nd.get('scale', [1, 1, 1])) + [1.0])
    Rm = np.eye(4); Rm[:3, :3] = q2m(nd.get('rotation', [0, 0, 0, 1]))
    T = np.eye(4); T[:3, 3] = nd.get('translation', [0, 0, 0])
    return T @ Rm @ S


def set_trs(nd, M):
    """Rigid-times-uniform-scale M -> the node's TRS (the markers carry a uniform scale)."""
    sc = float(np.cbrt(np.linalg.det(M[:3, :3])))
    Rm = M[:3, :3] / sc
    nd.pop('matrix', None)
    nd['translation'] = [float(x) for x in M[:3, 3]]
    nd['rotation'] = [float(x) for x in m2q(Rm)]
    nd['scale'] = [sc, sc, sc]


def globals_(js):
    nodes = js['nodes']
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    G = {}

    def g(i):
        if i in G:
            return G[i]
        m = trs(nodes[i]) if parent.get(i) is None else g(parent[i]) @ trs(nodes[i])
        G[i] = m
        return m
    for i in range(len(nodes)):
        g(i)
    return G, parent


def mat_list(js, bin_, acc):
    a = L.read_accessor(js, bin_, acc)
    return [np.array(r, float).reshape(4, 4).T for r in a]


def append(bin_, data):
    off = len(bin_) + (-len(bin_) % 4)
    bin_.extend(b'\x00' * (off - len(bin_)))
    bin_.extend(data)
    return off


def skin_rest(js, bin_, mesh_node, gl):
    """Every vertex of a skinned mesh node, skinned at REST: sum_w globalRest(j) x IBM(j) x v."""
    nd = js['nodes'][mesh_node]
    sk = js['skins'][nd['skin']]
    ibm = mat_list(js, bin_, sk['inverseBindMatrices'])
    pr = js['meshes'][nd['mesh']]['primitives'][0]['attributes']
    V = L.read_accessor(js, bin_, pr['POSITION']).astype(np.float64)
    J = L.read_accessor(js, bin_, pr['JOINTS_0']).astype(int)
    W = L.read_accessor(js, bin_, pr['WEIGHTS_0']).astype(np.float64)
    Vh = np.c_[V, np.ones(len(V))]
    out = np.zeros((len(V), 3))
    for k in range(4):
        for jj in np.unique(J[:, k]):
            sel = (J[:, k] == jj) & (W[:, k] > 0)
            if not sel.any():
                continue
            M = gl[sk['joints'][jj]] @ ibm[jj]
            out[sel] += (Vh[sel] @ M.T)[:, :3] * W[sel, k:k + 1]
    return out


def hand_points(js, bin_, hand, wmin=0.30):
    """A mesh's vertices weighted to `hand` above wmin, in that hand's LOCAL frame (IBM x v)."""
    nd = next(n for n in js['nodes'] if 'skin' in n and 'mesh' in n)
    sk = js['skins'][nd['skin']]
    names = [js['nodes'][j]['name'] for j in sk['joints']]
    jh = names.index(hand)
    ibm = mat_list(js, bin_, sk['inverseBindMatrices'])[jh]
    pr = js['meshes'][nd['mesh']]['primitives'][0]['attributes']
    V = L.read_accessor(js, bin_, pr['POSITION']).astype(np.float64)
    J = L.read_accessor(js, bin_, pr['JOINTS_0']).astype(int)
    W = L.read_accessor(js, bin_, pr['WEIGHTS_0']).astype(np.float64)
    w = ((J == jh) * W).sum(axis=1)
    P = (np.c_[V, np.ones(len(V))] @ ibm.T)[:, :3]
    return P[w > wmin], P


def mount(body, axe, roll_deg):
    """The grip calibration and the weapon bone's rest, in RightHand's local frame."""
    (jb, bb), (ja, ba) = body, axe
    hand, _ = hand_points(jb, bb, "RightHand")
    C = hand.mean(0)
    _, _, vt = np.linalg.svd(hand - C, full_matrices=False)
    along = vt[0] if abs(vt[0] @ C) > abs(vt[1] @ C) else vt[1]
    along = along * (1.0 if along @ C > 0 else -1.0)
    rest = [v for v in vt if abs(v @ along) < 0.9]
    channel = rest[0] / np.linalg.norm(rest[0])
    _, A = hand_points(ja, ba, "RightHand", wmin=-1.0)
    c = A.mean(0)
    _, _, vt2 = np.linalg.svd(A - c, full_matrices=False)
    H = vt2[0]
    mk = next(i for i, n in enumerate(ja['nodes']) if n.get('name') == 'axe_edge')
    edge = trs(ja['nodes'][mk])[:3, 3]            # local to its parent, RightHand
    if (edge - c) @ H < 0:
        H = -H
    s0 = (C - c) @ H
    sec = A[np.abs((A - c) @ H - s0) * 0.010882345 < 0.03]
    P = sec.mean(0)
    E = (edge - P) - ((edge - P) @ H) * H
    E /= np.linalg.norm(E)
    T = channel if channel @ H >= 0 else -channel
    Q1 = arc(H, T)
    E1 = Q1 @ E
    N1 = np.cross(T, E1)
    phi = math.radians(roll_deg)
    E2 = math.cos(phi) * E1 + math.sin(phi) * N1
    Q = axis_angle(T, phi) @ Q1
    G = np.eye(4); G[:3, :3] = Q; G[:3, 3] = P - Q @ P
    X = np.cross(T, E2)
    W = np.eye(4); W[:3, 0] = X; W[:3, 1] = T; W[:3, 2] = E2; W[:3, 3] = P
    return dict(G=G, W=W, P=P, H=H, T=T, E=E, E2=E2, C=C, channel=channel, along=along,
                seat_turn_deg=math.degrees(math.acos(max(-1, min(1, H @ T)))),
                haft_to_hand_axis_deg_before=math.degrees(math.acos(max(-1, min(1, H @ along)))),
                haft_to_hand_axis_deg_after=math.degrees(math.acos(max(-1, min(1, T @ along)))),
                fist_centroid_off_haft=float(np.linalg.norm((C - P) - ((C - P) @ H) * H)))


def reorder(js, bin_, ibm_list):
    """Put the skin's joints in BASE_RIG order: the joint list, the inverse bind matrices (a new
    accessor) and every JOINTS_0 index of every mesh using the skin. Returns the permutation."""
    sk = js['skins'][0]
    names = [js['nodes'][j]['name'] for j in sk['joints']]
    assert sorted(names) == sorted(BASE_RIG), "not the base rig's joint set: %s" % names
    perm = [names.index(n) for n in BASE_RIG]           # new position -> old index
    inv = {old: new for new, old in enumerate(perm)}
    sk['joints'] = [sk['joints'][o] for o in perm]
    ibm2 = [ibm_list[o] for o in perm]
    data = b''.join(struct.pack('<16f', *M.T.reshape(-1)) for M in ibm2)
    off = append(bin_, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126,
                            "count": len(ibm2), "type": "MAT4"})
    sk['inverseBindMatrices'] = len(js['accessors']) - 1
    if perm == list(range(len(perm))):
        return perm
    done = set()
    for nd in js['nodes']:
        if nd.get('skin') is None or 'mesh' not in nd:
            continue
        for pr in js['meshes'][nd['mesh']]['primitives']:
            ai = pr['attributes'].get('JOINTS_0')
            if ai is None or ai in done:
                continue
            done.add(ai)
            acc = js['accessors'][ai]
            bv = js['bufferViews'][acc['bufferView']]
            base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
            assert acc['componentType'] == 5121, "JOINTS_0 must be unsigned byte"
            stride = bv.get('byteStride') or 4
            for i in range(acc['count']):
                for c in range(4):
                    o = base + i * stride + c
                    bin_[o] = inv[bin_[o]]
    return perm


def patch(path, out, mt=None):
    js, bin0 = L.load_glb(path)
    bin_ = bytearray(bin0)
    nodes = js['nodes']
    assert len(js['skins']) == 1, "one skin per file expected"
    sk = js['skins'][0]
    names = [nodes[j]['name'] for j in sk['joints']]
    assert not any(n in names for n, _ in WEAPON_BONES), "%s already has weapon bones" % path
    gl0, parent = globals_(js)
    mesh_node = next(i for i, n in enumerate(nodes) if 'skin' in n and 'mesh' in n)
    before = skin_rest(js, bytes(bin_), mesh_node, gl0)
    ibm = mat_list(js, bytes(bin_), sk['inverseBindMatrices'])
    # which hand, if any, carries the whole mesh
    pr = js['meshes'][nodes[mesh_node]['mesh']]['primitives'][0]['attributes']
    Jv = L.read_accessor(js, bytes(bin_), pr['JOINTS_0']).astype(int)
    Wv = L.read_accessor(js, bytes(bin_), pr['WEIGHTS_0']).astype(np.float64)
    weapon_of = None
    for wn, hn in WEAPON_BONES:
        jh = names.index(hn)
        if (((Jv == jh) * Wv).sum(axis=1) >= 0.999).all():
            weapon_of = (wn, hn)
    new_ibm = list(ibm)
    added = {}
    for wn, hn in WEAPON_BONES:
        ih = sk['joints'][names.index(hn)]
        nd = {"name": wn}
        Wl = np.eye(4)
        if mt is not None and wn == "weapon_r":
            Wl = mt['W']
            set_trs(nd, Wl)
            nd['scale'] = [1.0, 1.0, 1.0]
        nodes.append(nd)
        iw = len(nodes) - 1
        nodes[ih].setdefault('children', []).append(iw)
        sk['joints'].append(iw)
        new_ibm.append(np.linalg.inv(Wl) @ ibm[names.index(hn)])
        added[wn] = (iw, len(sk['joints']) - 1, hn)
    # the extended inverse bind matrices, as a NEW accessor (the old one is left unreferenced)
    data = b''.join(struct.pack('<16f', *M.T.reshape(-1)) for M in new_ibm)
    off = append(bin_, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126,
                            "count": len(new_ibm), "type": "MAT4"})
    sk['inverseBindMatrices'] = len(js['accessors']) - 1
    rep = {"file": os.path.basename(path)}
    if weapon_of:
        wn, hn = weapon_of
        jh, jw = names.index(hn), added[wn][1]
        acc = js['accessors'][pr['JOINTS_0']]
        bv = js['bufferViews'][acc['bufferView']]
        base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
        stride = bv.get('byteStride') or 4
        assert acc['componentType'] == 5121
        n = 0
        for i in range(acc['count']):
            for c in range(4):
                o = base + i * stride + c
                if bin_[o] == jh:
                    bin_[o] = jw; n += 1
        rep["rebound"] = {"from": hn, "to": wn, "slots": n}
        if mt is not None and wn == "weapon_r":
            # re-seat: v' = inverse(IBM_hand) x G x IBM_hand x v, normals by its rotation
            Gb = np.linalg.inv(ibm[jh]) @ mt['G'] @ ibm[jh]
            for key in ("POSITION", "NORMAL"):
                a_ = js['accessors'][pr[key]]
                bv2 = js['bufferViews'][a_['bufferView']]
                b2 = bv2.get('byteOffset', 0) + a_.get('byteOffset', 0)
                st2 = bv2.get('byteStride') or 12
                V = L.read_accessor(js, bytes(bin_), pr[key]).astype(np.float64)
                if key == "POSITION":
                    V2 = (np.c_[V, np.ones(len(V))] @ Gb.T)[:, :3]
                    a_['min'] = [float(x) for x in V2.min(0)]; a_['max'] = [float(x) for x in V2.max(0)]
                else:
                    Rn = Gb[:3, :3] / np.cbrt(np.linalg.det(Gb[:3, :3]))
                    V2 = V @ Rn.T
                    V2 /= np.linalg.norm(V2, axis=1, keepdims=True)
                for i in range(len(V2)):
                    struct.pack_into('<3f', bin_, b2 + i * st2, *V2[i])
            rep["reseated_vertices"] = int(a_['count'])
        # markers ride with the weapon: re-parent under the weapon bone, moved by G (rank 2)
        for i, nd in enumerate(nodes):
            if parent.get(i) == sk['joints'][jh] and 'mesh' not in nd and i not in sk['joints'] and nd.get('name') not in dict(WEAPON_BONES):
                old = trs(nd)
                Wl = mt['W'] if (mt is not None and wn == "weapon_r") else np.eye(4)
                Gl = mt['G'] if (mt is not None and wn == "weapon_r") else np.eye(4)
                set_trs(nd, np.linalg.inv(Wl) @ Gl @ old)
                nodes[sk['joints'][jh]]['children'].remove(i)
                nodes[added[wn][0]].setdefault('children', []).append(i)
                rep.setdefault("markers_moved", []).append(nd.get('name'))
    rep["order_before"] = [nodes[j]['name'] for j in sk['joints']]
    reorder(js, bin_, new_ibm)
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    gl1, _ = globals_(js)
    after = skin_rest(js, bytes(bin_), mesh_node, gl1)
    d = np.linalg.norm(after - before, axis=1) if len(before) else np.zeros(1)
    rep["rest_displacement_m"] = {"max": float(d.max()), "median": float(np.median(d))}
    rep["joints"] = [nodes[j]['name'] for j in sk['joints']]
    R.write_glb(out, js, bin_)
    res = L.lint(out)
    rep["lint"] = {"verdict": res["verdict"], "fails": res["fails"], "warns": len(res["warns"])}
    return rep


MOUNT_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "weapon_mount.json")


def recorded_mount():
    """The axe's mount (rank 2) once one is recorded -- weapon_r's rest W and the re-seat G, both in
    RightHand's local frame -- so a re-export gets the same mount the staged files carry."""
    if not os.path.exists(MOUNT_JSON):
        return None
    m = json.load(open(MOUNT_JSON))
    return {"W": np.array(m["W"], float), "G": np.array(m["G"], float)}


def snap(path, out=None, tol_m=1e-7):
    """Set each weapon bone's rest EXACTLY to the base rig's (coincident with its hand, or the
    recorded mount for weapon_r) and its inverse bind matrix to match. A Blender round trip leaves
    them ~8 um off (measured: weapon_l 7.96e-06 m after one), which the lint's 1 um rule would
    fail on every re-export; the weapon moves by that much and no more."""
    js, b = L.load_glb(path)
    b = bytearray(b)
    nodes = js['nodes']
    sk = js['skins'][0]
    names = [nodes[j]['name'] for j in sk['joints']]
    ibm = mat_list(js, bytes(b), sk['inverseBindMatrices'])
    mt = recorded_mount()
    gl, parent = globals_(js)
    mpu = float(np.cbrt(abs(np.linalg.det(gl[sk['joints'][0]][:3, :3] @ np.linalg.inv(trs(nodes[sk['joints'][0]])[:3, :3]))))) or 1.0
    moved = {}
    for wn, hn in WEAPON_BONES:
        iw, ih = names.index(wn), names.index(hn)
        want = mt['W'] if (mt is not None and wn == "weapon_r") else np.eye(4)
        got = trs(nodes[sk['joints'][iw]])
        probe = np.array([[0, 0, 0, 1], [10, 0, 0, 1], [0, 10, 0, 1], [0, 0, 10, 1]], float).T
        dev = float(np.abs((got - want) @ probe).max()) * mpu
        if dev > tol_m:
            nd = nodes[sk['joints'][iw]]
            if np.allclose(want, np.eye(4)):
                for key in ('matrix', 'translation', 'rotation', 'scale'):
                    nd.pop(key, None)
            else:
                set_trs(nd, want)
                nd['scale'] = [1.0, 1.0, 1.0]
            ibm[iw] = np.linalg.inv(want) @ ibm[ih]
            moved[wn] = dev
    if not moved:
        return {"file": os.path.basename(path), "action": "present"}
    data = b''.join(struct.pack('<16f', *M.T.reshape(-1)) for M in ibm)
    off = append(b, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126,
                            "count": len(ibm), "type": "MAT4"})
    sk['inverseBindMatrices'] = len(js['accessors']) - 1
    js['buffers'][0]['byteLength'] = len(b) + (-len(b) % 4)
    R.write_glb(out or path, js, b)
    print("  52_weapon_bones: %s -- weapon rest snapped to the base rig (%s)"
          % (os.path.basename(path), ", ".join("%s %.2g m" % kv for kv in moved.items())))
    return {"file": os.path.basename(path), "action": "snapped", "moved_m": moved}


def ensure(path, out=None):
    """IDEMPOTENT, and the EXPORT CHAIN'S HOOK: 15_export_scene and every script that re-exports a
    GLB through Blender call this on what they wrote, before their lint. A file that already
    carries the weapon bones is left alone; one that lost them (a fresh export) gets them back,
    with the recorded mount if there is one. The lint's skeleton-identity rule then fails anything
    this could not make right -- a re-export that REORDERED the bones, say -- so nothing is lost
    silently."""
    js, _ = L.load_glb(path)
    skins = js.get('skins', [])
    if not skins:
        return {"file": os.path.basename(path), "action": "no skin"}
    have = all(any(js['nodes'][j].get('name') == wn for j in sk['joints']) for sk in skins for wn, _ in WEAPON_BONES)
    if have:
        names = tuple(js['nodes'][j]['name'] for j in skins[0]['joints'])
        if names == BASE_RIG:
            return snap(path, out)
        # a Blender round trip (or anything) reordered them: put them back, nothing else changes
        js2, b2 = L.load_glb(path)
        b2 = bytearray(b2)
        ibm = mat_list(js2, bytes(b2), js2['skins'][0]['inverseBindMatrices'])
        reorder(js2, b2, ibm)
        js2['buffers'][0]['byteLength'] = len(b2) + (-len(b2) % 4)
        R.write_glb(out or path, js2, b2)
        print("  52_weapon_bones: %s -- joints put back in base-rig order" % os.path.basename(path))
        snap(out or path)
        return {"file": os.path.basename(path), "action": "reordered"}
    rep = patch(path, out or path, recorded_mount())
    rep["action"] = "added"
    print("  52_weapon_bones: %s -- weapon bones added (rest displacement max %.3g m)"
          % (rep["file"], rep["rest_displacement_m"]["max"]))
    return rep


def main():
    a = sys.argv[1:]
    outd = a[a.index('--out') + 1]
    roll = float(a[a.index('--roll') + 1]) if '--roll' in a else None
    outj = a[a.index('--json') + 1] if '--json' in a else None
    skip = {outd, str(roll) if roll is not None else None, outj}
    files = [x for x in a if x.endswith('.glb') and x not in skip]
    os.makedirs(outd, exist_ok=True)
    mt = None
    rep = {"roll_deg": roll, "files": {}}
    if roll is not None:
        body = next(f for f in files if os.path.basename(f).startswith('nb-body'))
        axe = next(f for f in files if os.path.basename(f) == 'axe.glb')
        mt = mount(L.load_glb(body), L.load_glb(axe), roll)
        rep["mount"] = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in mt.items()}
        if '--record' in a:
            json.dump({"roll_deg": roll, "W": mt['W'].tolist(), "G": mt['G'].tolist(),
                       "frame": "RightHand local (the frame the skin's inverse bind maps into), glTF units",
                       "written_by": "52_weapon_bones.py --roll %s --record" % roll}, open(MOUNT_JSON, 'w'), indent=1)
            print("recorded the mount in %s (ensure() and the lint read it)" % MOUNT_JSON)
        print("mount: seat turn %.1f deg (haft to the hand axis %.1f -> %.1f), roll %+.1f; grip %s; fist centroid %.4f units off the haft"
              % (mt['seat_turn_deg'], mt['haft_to_hand_axis_deg_before'], mt['haft_to_hand_axis_deg_after'], roll,
                 np.round(mt['P'], 3).tolist(), mt['fist_centroid_off_haft']))
    for f in files:
        r = patch(f, os.path.join(outd, os.path.basename(f)), mt)
        rep["files"][r["file"]] = r
        print("  %-12s joints %d (%s) %s | rest displacement max %.3g m | lint %s, %d fails"
              % (r["file"], len(r["joints"]), ",".join(r["joints"][-2:]),
                 ("rebound %s->%s (%d slots)%s" % (r["rebound"]["from"], r["rebound"]["to"], r["rebound"]["slots"],
                  (", re-seated %d vertices" % r["reseated_vertices"]) if "reseated_vertices" in r else "")) if "rebound" in r else "no weapon",
                 r["rest_displacement_m"]["max"], r["lint"]["verdict"], len(r["lint"]["fails"])))
    ref = next(iter(rep["files"].values()))["joints"]
    same = all(r["joints"] == ref for r in rep["files"].values())
    rep["skeleton_identity"] = same
    print("skeleton identity across %d files: %s (%d joints)" % (len(files), "PASS" if same else "FAIL", len(ref)))
    if outj:
        json.dump(rep, open(outj, 'w'), indent=1)
    assert same


if __name__ == '__main__':
    main()
