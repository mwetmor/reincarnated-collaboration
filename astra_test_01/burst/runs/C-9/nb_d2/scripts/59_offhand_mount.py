# THE OFF-HAND MOUNT: weapon_l's rest becomes the axe's seat in the LEFT fist -- the right side's
# convention (52_weapon_bones.py's T12 seat), mirrored and then settled on the left hand's own channel.
#
#   python3 scripts/59_offhand_mount.py <body.glb> <axe.glb (on weapon_r)> <outdir> [--json f]
#
# writes <outdir>/nb-body.glb (weapon_l's rest = the seat, its inverse bind in every skin that lists it),
#        <outdir>/axe_l.glb   (the axe re-bound to weapon_l, its vertices placed by the seat -- the SAME axe,
#                              turned into the left hand, not mirrored: a mirror image of a bearded axe is
#                              another axe)
#        <outdir>/weapon_mount.json (W for weapon_r, unchanged; WL for weapon_l, new; both local to their hand)
#
# THE SEAT. The right mount is W (weapon_r's rest in RightHand's frame: origin at the grip, +Y along the
# haft to the head, +Z toward the edge). In skeleton space it is G_RightHand x W. Mirrored across his
# sagittal plane (x -> 2 x_hips - x): the grip point and the haft and edge directions reflect, and the
# frame is made proper again (X = Y x Z). Then, as 52 seats the right: the haft is turned (shortest arc,
# about the grip) onto the LEFT hand's own CHANNEL -- the across-palm axis of its vertices, the axis grip_L
# closes round -- because the rig is not quite symmetric (D2 measured 0.2-0.8 cm at rest) and the fist,
# not the mirror, is what the haft has to lie in. The roll about the haft is the mirror's (no free number).
# JOIN-1 (sword main hand, axe off hand): off_grip is this joint, off_tip is it + the axe's length along +Y.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
R_ = __import__('49_recentre')


def globals_rest(js):
    nodes = js['nodes']
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    G = {}
    def g(i):
        if i in G:
            return G[i]
        M = W.trs(nodes[i])
        G[i] = M if i not in parent else g(parent[i]) @ M
        return G[i]
    for i in range(len(nodes)):
        g(i)
    return G, parent


def ibm_list(js, bin_, sk):
    return [np.array(r, float).reshape(4, 4).T for r in L.read_accessor(js, bin_, sk['inverseBindMatrices'])]


def write_ibm(js, bin_, sk, ibm):
    data = b''.join(struct.pack('<16f', *M.T.reshape(-1)) for M in ibm)
    off = W.append(bin_, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": len(ibm), "type": "MAT4"})
    sk['inverseBindMatrices'] = len(js['accessors']) - 1


def set_rest(node, M):
    R = M[:3, :3] / np.cbrt(np.linalg.det(M[:3, :3]))
    node['rotation'] = [float(x) for x in W.m2q(R)]
    node['translation'] = [float(x) for x in M[:3, 3]]
    node.pop('scale', None)
    node.pop('matrix', None)


def arc(a, b):
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
    v = np.cross(a, b); c = float(a @ b)
    if np.linalg.norm(v) < 1e-12:
        return np.eye(3)
    return W.axis_angle(v / np.linalg.norm(v), math.atan2(np.linalg.norm(v), c))


def main():
    a = sys.argv[1:]
    body, axe, outd = a[0], a[1], a[2]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    os.makedirs(outd, exist_ok=True)
    js, b0 = L.load_glb(body)
    bin_ = bytearray(b0)
    nodes = js['nodes']
    nid = {n.get('name'): i for i, n in enumerate(nodes)}
    G, parent = globals_rest(js)
    A = G[nid['Armature']]; Ai = np.linalg.inv(A)
    S_ = lambda i: Ai @ G[i]                                   # skeleton space, glTF units
    Wr = W.trs(nodes[nid['weapon_r']])                          # the right seat, local to RightHand
    MR = S_(nid['RightHand']) @ Wr
    xm = float(S_(nid['Hips'])[0, 3])
    Mir = np.diag([-1.0, 1.0, 1.0])
    P = Mir @ (MR[:3, 3] - [xm, 0, 0]) + [xm, 0, 0]
    Y = Mir @ MR[:3, 1]; Z = Mir @ MR[:3, 2]
    # THE LEFT HAND'S OWN CHANNEL (52's hand_points / mount rule, on LeftHand)
    hand, _ = W.hand_points(js, bytes(bin_), "LeftHand")
    C = hand.mean(0)
    _, _, vt = np.linalg.svd(hand - C, full_matrices=False)
    along = vt[0] if abs(vt[0] @ C) > abs(vt[1] @ C) else vt[1]
    along = along * (1.0 if along @ C > 0 else -1.0)
    rest_ax = [v for v in vt if abs(v @ along) < 0.9]
    chan_l = rest_ax[0] / np.linalg.norm(rest_ax[0])           # LeftHand-local
    GL = S_(nid['LeftHand'])
    chan = GL[:3, :3] @ chan_l; chan /= np.linalg.norm(chan)
    if chan @ Y < 0:
        chan = -chan
    Cw = (GL @ np.append(C, 1.0))[:3]
    turn = arc(Y, chan)
    Y2 = turn @ Y; Z2 = turn @ Z
    Z2 = Z2 - (Z2 @ Y2) * Y2; Z2 /= np.linalg.norm(Z2)
    X2 = np.cross(Y2, Z2)
    MLs = np.eye(4); MLs[:3, 0] = X2; MLs[:3, 1] = Y2; MLs[:3, 2] = Z2; MLs[:3, 3] = P
    WL = np.linalg.inv(GL) @ MLs                               # local to LeftHand
    off_axis = float(np.linalg.norm((Cw - P) - ((Cw - P) @ Y2) * Y2))
    # the right side's same numbers, for comparison
    hr, _ = W.hand_points(js, bytes(bin_), "RightHand")
    Cr = (S_(nid['RightHand']) @ np.append(hr.mean(0), 1.0))[:3]
    off_axis_r = float(np.linalg.norm((Cr - MR[:3, 3]) - ((Cr - MR[:3, 3]) @ MR[:3, 1]) * MR[:3, 1]))
    MPU = float(np.linalg.norm(A[:3, 0]))
    rep = dict(mirror_x_units=xm, haft_turned_onto_channel_deg=math.degrees(math.acos(max(-1, min(1, float(Y @ chan))))),
               fist_centroid_off_haft_m=off_axis * MPU, right_side_fist_centroid_off_haft_m=off_axis_r * MPU,
               grip_mirror_asymmetry_note="the seat's origin is the mirrored right grip; the left fist centroid's distance off the seated haft is the check")
    print("off-hand seat: the mirrored haft turned %.2f deg onto the left hand's channel; the left fist centroid %.4f m off the haft (the right side: %.4f m)"
          % (rep['haft_turned_onto_channel_deg'], rep['fist_centroid_off_haft_m'], rep['right_side_fist_centroid_off_haft_m']))
    # ---- the body: weapon_l's rest = WL, its IBM in every skin that lists it ------------------------------
    wl = nid['weapon_l']
    set_rest(nodes[wl], WL)
    G2, _ = globals_rest(js)
    for sk in js['skins']:
        if wl not in sk['joints']:
            continue
        ibm = ibm_list(js, bytes(bin_), sk)
        ibm[sk['joints'].index(wl)] = np.linalg.inv(G2[wl])
        write_ibm(js, bin_, sk, ibm)
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    R_.write_glb(os.path.join(outd, 'nb-body.glb'), js, bin_)
    # ---- the axe on weapon_l -----------------------------------------------------------------------------
    ja, ab0 = L.load_glb(axe)
    abin = bytearray(ab0)
    an = ja['nodes']; anid = {n.get('name'): i for i, n in enumerate(an)}
    sk = ja['skins'][0]
    names = [an[j]['name'] for j in sk['joints']]
    jr, jl = names.index('weapon_r'), names.index('weapon_l')
    ibm = ibm_list(ja, bytes(abin), sk)
    # its own skeleton gets the same weapon_l rest (gear.gd compares bone NAMES; its IBM is what binds)
    set_rest(an[anid['weapon_l']], WL)
    Ga, _ = globals_rest(ja)
    new_l = np.linalg.inv(Ga[anid['weapon_l']])
    Mv = np.linalg.inv(new_l) @ ibm[jr]                        # weapon_r-local -> the seat on weapon_l, in the file's bind space
    mesh_node = next(i for i, nd in enumerate(an) if 'mesh' in nd and 'skin' in nd)
    moved = 0
    for pr in ja['meshes'][an[mesh_node]['mesh']]['primitives']:
        at = pr['attributes']
        for key in ("POSITION", "NORMAL"):
            if key not in at:
                continue
            acc = ja['accessors'][at[key]]; bv = ja['bufferViews'][acc['bufferView']]
            base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0); st = bv.get('byteStride') or 12
            V = L.read_accessor(ja, bytes(abin), at[key]).astype(np.float64)
            if key == "POSITION":
                V2 = (np.c_[V, np.ones(len(V))] @ Mv.T)[:, :3]
                acc['min'] = [float(x) for x in V2.min(0)]; acc['max'] = [float(x) for x in V2.max(0)]
                moved = len(V2)
            else:
                Rn = Mv[:3, :3] / np.cbrt(np.linalg.det(Mv[:3, :3]))
                V2 = V @ Rn.T; V2 /= np.linalg.norm(V2, axis=1, keepdims=True)
            for i in range(len(V2)):
                struct.pack_into('<3f', abin, base + i * st, *V2[i])
        # rebind weapon_r -> weapon_l
        acc = ja['accessors'][at['JOINTS_0']]; bv = ja['bufferViews'][acc['bufferView']]
        base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0); st = bv.get('byteStride') or 4
        assert acc['componentType'] == 5121
        for i in range(acc['count']):
            for c in range(4):
                if abin[base + i * st + c] == jr:
                    abin[base + i * st + c] = jl
    ibm[jl] = new_l
    write_ibm(ja, abin, sk, ibm)
    # the edge marker (and any marker under weapon_r) moves to weapon_l with the same LOCAL transform
    markers = []
    for i, nd in enumerate(an):
        if parent_of(ja, i) == anid['weapon_r'] and 'mesh' not in nd and i not in sk['joints']:
            an[anid['weapon_r']]['children'].remove(i)
            an[anid['weapon_l']].setdefault('children', []).append(i)
            markers.append(nd.get('name'))
    ja['buffers'][0]['byteLength'] = len(abin) + (-len(abin) % 4)
    R_.write_glb(os.path.join(outd, 'axe_l.glb'), ja, abin)
    # the axe's length along +Y from the grip (off_tip), in the seat's frame, metres
    V = L.read_accessor(ja, bytes(abin), ja['meshes'][an[mesh_node]['mesh']]['primitives'][0]['attributes']['POSITION']).astype(float)
    loc = (np.c_[V, np.ones(len(V))] @ new_l.T)[:, :3]
    amp = float(np.linalg.norm(Ga[anid['Armature']][:3, 0]))
    rep.update(off_tip_along_m=round(float(loc[:, 1].max()) * amp, 4), off_butt_below_m=round(float(-loc[:, 1].min()) * amp, 4),
               axe_vertices=moved, markers_moved=markers,
               edge_axis="+Z of weapon_l is the axe's cutting edge (the right seat's convention, carried through the mirror)")
    # ---- the mount record ----------------------------------------------------------------------------------
    rec_in = os.path.join(os.path.dirname(os.path.abspath(body)), 'weapon_mount.json')
    rec = json.load(open(rec_in)) if os.path.exists(rec_in) else {}
    rec['WL'] = WL.tolist()
    rec['WL_note'] = ("weapon_l's rest local to LeftHand: the axe's seat in the left fist (59_offhand_mount.py) -- the right seat W mirrored "
                      "across the sagittal plane and its haft turned onto the left hand's channel; +Y the haft to the head, +Z the edge")
    json.dump(rec, open(os.path.join(outd, 'weapon_mount.json'), 'w'), indent=1)
    res = L.lint(os.path.join(outd, 'nb-body.glb'))
    rep['body_lint'] = dict(verdict=res['verdict'], fails=res['fails'])
    print("axe_l.glb: %d vertices re-bound to weapon_l; off_tip %.4f m along +Y, the butt %.4f m below the grip; markers %s; body lint %s %s"
          % (moved, rep['off_tip_along_m'], rep['off_butt_below_m'], markers, res['verdict'], res['fails'][:2]))
    if outj:
        json.dump(rep, open(outj, 'w'), indent=1)


def parent_of(js, i):
    for p, nd in enumerate(js['nodes']):
        if i in nd.get('children', []):
            return p
    return None


if __name__ == '__main__':
    main()
