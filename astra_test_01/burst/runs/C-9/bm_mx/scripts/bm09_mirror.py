# bm_mx STAGE 3 (R-C9-133, dual wield): MIRROR across his sagittal plane, in WORLD space, per key -- no solver.
# Each joint's rotation AWAY FROM REST in world (dW = R_world(t) . R_world_rest^-1) is reflected through the plane x = 0 of his rest
# frame (S = diag(-1, 1, 1): he faces +Z, his left is +X):  dW' = S . dW . S  -- a proper rotation -- and put on the PARTNER joint:
#     R_world_partner(t) = dW'_joint(t) . R_world_rest_partner
# then back to local under the (already rewritten) parent. Exact for bone directions and twist when the rest pose is mirror-symmetric
# (his A-pose: the rest-asymmetry is reported as rest_asym_m, the largest |x_L + x_R| / |y,z| difference over the arm joints).
#   arm   <in> <out> arm  <clip,clip>   the LEFT arm chain (LeftShoulder..LeftHand) takes the mirrored RIGHT arm on each clip's own keys
#                                       (the off-hand carry: the left fist carries the axe as the right carries the sword). Binary patch:
#                                       new output accessors on the same inputs; every other channel untouched; the loop seam kept.
#         --frame chest: mirror RELATIVE TO THE CHEST (Spine) instead of the root -- each arm joint's rotation away from rest is taken
#                           in the chest's frame (A = R_spine^-1 . R), reflected through the chest's rest sagittal plane, and put back on
#                           the chest as it is at that key. Needed when the source torso is TURNED (the axe pack walks bladed, chest
#                           14-23 deg off his root): a root-plane mirror then pulls the left clavicle in (shoulder width 0.48-0.64 of rest).
#   full  <in> <out> full <src>:<dst>   a new clip <dst> = <src> mirrored whole (every L/R pair swapped, centre joints reflected, the hips'
#                                       world position reflected): the off-hand version of a one-handed attack.
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT, MODE, ARG = a[0], a[1], a[2], a[3]
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']
S = np.diag([-1.0, 1.0, 1.0])
def rot(M): R = M[:3, :3]; return R / np.cbrt(np.linalg.det(R))
G0, _ = W.globals_(js); R0 = {n: rot(G0[i]) for n, i in nid.items()}
skin = {js['nodes'][j]['name'] for j in js['skins'][0]['joints']}
partner = lambda n: n.replace('Left', '#').replace('Right', 'Left').replace('#', 'Right')
ARM_R = ['RightShoulder', 'RightArm', 'RightForeArm', 'RightHand']; ARM_L = [partner(x) for x in ARM_R]
asym = max(abs(G0[nid[l]][0, 3] + G0[nid[r]][0, 3]) + np.linalg.norm(G0[nid[l]][1:3, 3] - G0[nid[r]][1:3, 3]) for l, r in zip(ARM_L, ARM_R))
asym *= 1.0   # world metres (the Armature carries the scale)
parent = m['parent']
def mirrored_world(G, n):
    src = partner(n) if partner(n) in nid else n
    dW = rot(G[nid[src]]) @ R0[src].T
    return S @ dW @ S @ R0[n]
CHEST = '--frame' in a and a[a.index('--frame') + 1] == 'chest'
Cr0 = R0['Spine']; Sc = Cr0.T @ S @ Cr0
def mirrored_chest(G, n):
    src = partner(n); Ct = rot(G[nid['Spine']])
    dA = (Ct.T @ rot(G[nid[src]])) @ (Cr0.T @ R0[src]).T
    return Ct @ (Sc @ dA @ Sc) @ (Cr0.T @ R0[n])
def write_clip(an, newq, newT=None):
    for (node, path), q in newq.items():
        ch = next((c for c in an['channels'] if c['target']['node'] == node and c['target']['path'] == path), None)
        q = np.array(q)
        if path == 'rotation':
            for i in range(1, len(q)):
                if np.dot(q[i], q[i - 1]) < 0: q[i] = -q[i]
        s = an['samplers'][ch['sampler']]
        an['samplers'].append({"input": s['input'], "output": CH.add_accessor(js, bn, q, "VEC4" if path == 'rotation' else "VEC3"), "interpolation": "LINEAR"})
        ch['sampler'] = len(an['samplers']) - 1
rep = dict(mode=MODE, frame='chest' if CHEST else 'root', rest_asym_m=round(float(asym), 4), clips={})
if MODE == 'arm':
    for clip in ARG.split(','):
        an = next(x for x in js['animations'] if x['name'] == clip)
        tt = m['anims'][clip][(nid['LeftArm'], 'rotation')][0]
        out = {(nid[n], 'rotation'): [] for n in ARM_L}
        for t in tt:
            G = C.globals_at(m, clip, float(t)); Rw = {}
            for n in ARM_L:
                Rw[n] = mirrored_chest(G, n) if CHEST else mirrored_world(G, n); p = parent[nid[n]]
                Rp = Rw[js['nodes'][p]['name']] if js['nodes'][p]['name'] in Rw else rot(G[p])
                out[(nid[n], 'rotation')].append(W.m2q(Rp.T @ Rw[n]))
        write_clip(an, out); rep['clips'][clip] = dict(keys=len(tt), joints=ARM_L)
elif MODE == 'full':
    src, dst = ARG.split(':'); an0 = next(x for x in js['animations'] if x['name'] == src)
    tin = an0['samplers'][an0['channels'][0]['sampler']]['input']; tt = L.read_accessor(js, bn, tin)[:, 0]
    joints = [n for n in nid if n in skin and (nid[n], 'rotation') in m['anims'][src]]
    order = []; seen = set()
    def visit(i):
        if i in seen: return
        if parent.get(i) is not None and js['nodes'][parent[i]]['name'] in joints: visit(parent[i])
        seen.add(i); order.append(i)
    for n in joints: visit(nid[n])
    q = {n: [] for n in joints}; hipsT = []; h = nid['Hips']; P = G0[parent[h]]
    for t in tt:
        G = C.globals_at(m, src, float(t)); Rw = {}
        for i in order:
            n = js['nodes'][i]['name']; Rw[n] = mirrored_world(G, n); p = parent[i]
            Rp = Rw[js['nodes'][p]['name']] if js['nodes'][p]['name'] in Rw else rot(G[p])
            q[n].append(W.m2q(Rp.T @ Rw[n]))
        pw = G[h][:3, 3].copy(); pw[0] = -pw[0]; hipsT.append((np.linalg.inv(P) @ np.r_[pw, 1.0])[:3])
    ch, sm = [], []
    for n in joints:
        qq = np.array(q[n])
        for i in range(1, len(qq)):
            if np.dot(qq[i], qq[i - 1]) < 0: qq[i] = -qq[i]
        sm.append({"input": tin, "output": CH.add_accessor(js, bn, qq, "VEC4"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": nid[n], "path": "rotation"}})
    sm.append({"input": tin, "output": CH.add_accessor(js, bn, np.array(hipsT), "VEC3"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": h, "path": "translation"}})
    js['animations'] = [x for x in js['animations'] if x['name'] != dst] + [{"name": dst, "channels": ch, "samplers": sm}]
    rep['clips'][dst] = dict(source_clip=src, keys=len(tt), joints=len(joints))
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
r = L.lint(OUT); rep['lint'] = r['verdict']; print(json.dumps(rep), r['fails'][:2])
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
