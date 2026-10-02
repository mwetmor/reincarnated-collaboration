# STAGE J/R-C9-123 (B): graft a renamed Mixamo GLB (e40a) onto HIS rig -- 55_clip_graft's world-space transfer, plus a REST
# ALIGNMENT per joint, because Mixamo rests in a T-pose and he rests in an A-pose (55's own check refuses any rest more than
# 0.01 off, rightly, for Meshy sources). For each joint i:  Q_i = the shortest arc taking HIS rest bone direction (joint -> its
# child, world) onto the SOURCE's rest bone direction; then
#     R_body_world(t) = dW(t) . Q_i . R_body_rest_world,    dW(t) = R_src_world(t) . R_src_rest_world^-1
# so his bone points where the source bone points at every frame (twist about the bone carried by dW). Leaves (hands, feet's
# toes, head) take their parent's Q. Q = identity when the rests already agree, so a Meshy source grafts exactly as 55 does
# (the self-test: --selftest grafts a Meshy clip both ways and reports the largest joint difference).
#   python3 e40b_mixamo_graft.py graft <body.glb> <out.glb> name=<src.glb>[@t0:t1][+loop][+deroot] ... [--json f]
#   python3 e40b_mixamo_graft.py selftest <body.glb> <meshy_clip.glb>
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
G55 = __import__('55_clip_graft'); W = __import__('52_weapon_bones')
CHILD = {"Hips": "Spine02", "Spine02": "Spine01", "Spine01": "Spine", "Spine": "neck", "neck": "Head", "Head": "head_end",
         "LeftShoulder": "LeftArm", "LeftArm": "LeftForeArm", "LeftForeArm": "LeftHand", "RightShoulder": "RightArm", "RightArm": "RightForeArm",
         "RightForeArm": "RightHand", "LeftUpLeg": "LeftLeg", "LeftLeg": "LeftFoot", "LeftFoot": "LeftToeBase", "RightUpLeg": "RightLeg",
         "RightLeg": "RightFoot", "RightFoot": "RightToeBase"}
_joints = G55.joints
def joints(js):
    j = _joints(js)
    return j if j else [nd.get('name') for nd in js['nodes'] if nd.get('name') in set(CHILD) | set(CHILD.values())]
G55.joints = joints
_orig = G55.retarget
def retarget(body_js, src_js, src_bin, anim, times, skip_scale=True):
    bname = {nd.get('name'): i for i, nd in enumerate(body_js['nodes'])}; sname = {nd.get('name'): i for i, nd in enumerate(src_js['nodes'])}
    Gb0, bpar = G55.world_rest(body_js); Gs0, _ = G55.world_rest(src_js)
    Q = {}
    for n, c in CHILD.items():
        if n in bname and c in bname and n in sname and c in sname:
            db = Gb0[bname[c]][:3, 3] - Gb0[bname[n]][:3, 3]; ds = Gs0[sname[c]][:3, 3] - Gs0[sname[n]][:3, 3]
            Q[n] = W.arc(db / np.linalg.norm(db), ds / np.linalg.norm(ds)) if np.linalg.norm(db) > 1e-9 and np.linalg.norm(ds) > 1e-9 else np.eye(3)
    for n in ("LeftHand", "RightHand", "LeftToeBase", "RightToeBase", "head_end"):
        p = {"LeftHand": "LeftForeArm", "RightHand": "RightForeArm", "LeftToeBase": "LeftFoot", "RightToeBase": "RightFoot", "head_end": "Head"}[n]
        Q[n] = Q.get(p, np.eye(3))
    rot = G55.rot
    _wr = G55.world_rest
    # wrap: substitute the body's rest world rotations by Q . R_rest for the transfer, keep the parents' chain consistent
    common = [n for n in G55.joints(body_js) if n in sname]
    trk = G55.tracks(src_js, src_bin, anim); hips_b, hips_s = bname['Hips'], sname['Hips']
    low = lambda G, nm: min(G[nm[f]][1, 3] for f in G55.FEET)
    k = (Gb0[hips_b][1, 3] - low(Gb0, bname)) / (Gs0[hips_s][1, 3] - low(Gs0, sname))
    order, seen = [], set()
    def visit(i):
        if i in seen: return
        p = bpar.get(i)
        if p is not None and body_js['nodes'][p].get('name') in common: visit(p)
        seen.add(i); order.append(i)
    for n in common: visit(bname[n])
    out = {n: [] for n in common}; hips_T = []
    for t in times:
        Gs, _ = G55.globals_from(src_js, G55.local_mats(src_js, trk, t, skip_scale)); Rw = {}
        for i in order:
            n = body_js['nodes'][i]['name']
            dW = rot(Gs[sname[n]]) @ rot(Gs0[sname[n]]).T
            Rw[i] = dW @ Q.get(n, np.eye(3)) @ rot(Gb0[i])
            p = bpar.get(i); Rp = Rw[p] if p in Rw else rot(Gb0[p])
            out[n].append(W.m2q(Rp.T @ Rw[i]))
        d = (Gs[hips_s][:3, 3] - Gs0[hips_s][:3, 3]) * k; pb = Gb0[hips_b][:3, 3] + d; P = Gb0[bpar[hips_b]]
        hips_T.append((np.linalg.inv(P) @ np.append(pb, 1.0))[:3])
    return common, out, np.array(hips_T), k
G55.retarget = retarget
if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'graft':
        outj = a[a.index('--json') + 1] if '--json' in a else None
        specs = [x for x in a[3:] if '=' in x and not x.startswith('--')]
        G55.graft(a[1], a[2], specs, outj, allow_mismatch=True)
    elif a[0] == 'selftest':
        body, src = a[1], a[2]
        G55.retarget = _orig; G55.graft(body, os.path.join(os.path.dirname(HERE), 'work', '_e40_ref.glb'), ['x=%s' % src])
        G55.retarget = retarget; G55.graft(body, os.path.join(os.path.dirname(HERE), 'work', '_e40_new.glb'), ['x=%s' % src])
        C = __import__('s17_loop_closure'); ma, mb = C.model(os.path.join(os.path.dirname(HERE), 'work', '_e40_ref.glb')), C.model(os.path.join(os.path.dirname(HERE), 'work', '_e40_new.glb'))
        tt = sorted({float(t) for v in ma['anims']['x'].values() for t in v[0]})[::5]; worst = 0
        for t in tt:
            A_, B_ = C.globals_at(ma, 'x', t), C.globals_at(mb, 'x', t)
            worst = max(worst, max(float(np.linalg.norm(A_[i][:3, 3] - B_[i][:3, 3])) for i in A_))
        print('SELFTEST: largest joint difference vs 55_clip_graft = %.6f (rig units)' % worst)
