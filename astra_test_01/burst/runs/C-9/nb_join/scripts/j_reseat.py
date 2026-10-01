# THE HAFT RE-SEAT (R-C9-115, the conductor 2026-10-01: "rotate each weapon's mount relative to its hand bone -- the haft
# turning inside a closed fist -- pitching the tip toward his facing; no joint change at all").
#
#   python3 scripts/j_reseat.py <hold body.glb> <out body.glb> --deg 30 [--t 0.5] [--json f]
#
# Each weapon bone's REST rotation (its mount: the weapon's seat in the fist; a child of the hand) is turned about the
# GRIP (the weapon joint's own origin, inside the fist) by --deg, about the axis (weapon axis x his forward +Z), the axis
# and the sense evaluated on his battle stance (idle_guard at --t with the hold's guard layers) and expressed in the
# hand's frame, so the same seat holds in every state. Nothing else changes: no joint, no clip key, no morph. Every clip
# that does not key the weapon bone carries the new seat; the death / war cry clamps key it and keep their own.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts")); sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts"))
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = sys.argv[1:]; HB, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
DEG = float(opt('--deg', '30')); T0 = float(opt('--t', '0.5')); FWD = np.array([0.0, 0, 1])
m = C.model(HB); nid = m['nid']; P = m['parent']; N = len(m['nodes'])


def locals_of(clip, t):
    loc = {i: [np.array(v, float) for v in m['rest'][i]] for i in range(N)}
    for (n, p), (tt, vv) in m['anims'][clip].items():
        k = int(np.argmin(np.abs(tt - t))); loc[n][{'translation': 0, 'rotation': 1, 'scale': 2}[p]] = np.array(vv[k], float)
    return loc


loc = locals_of('idle_guard', T0)
for sd, bones in (('R', ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]), ('L', ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand"])):
    g = locals_of('join_guard_%s_idle' % sd, 0.0)
    for b in bones: loc[nid[b]] = g[nid[b]]
G = {}
def gg(i):
    if i in G: return G[i]
    tr, q, s = loc[i]; M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
    G[i] = M if P.get(i) is None else gg(P[i]) @ M
    return G[i]
for i in range(N): gg(i)
nrm = lambda X: X / np.linalg.norm(X, axis=0)
js, b0 = L.load_glb(HB); rec = {}
for w in ('weapon_r', 'weapon_l'):
    i = nid[w]; Rw = nrm(G[i][:3, :3]); Y = Rw[:, 1]; ax = np.cross(Y, FWD); ax /= np.linalg.norm(ax)
    Rh = nrm(G[P[i]][:3, :3])
    Rnew = Rh.T @ W.axis_angle(ax, math.radians(DEG)) @ Rw            # the new seat, in the hand's frame
    q = [float(x) for x in W.m2q(Rnew)]
    before = math.degrees(math.acos(max(-1, min(1, float(Y @ FWD))))); after = math.degrees(math.acos(max(-1, min(1, float((W.axis_angle(ax, math.radians(DEG)) @ Y) @ FWD)))))
    rec[w] = dict(rest_rotation_was=js['nodes'][i].get('rotation'), rest_rotation_now=q, tip_forward_idle_deg=[round(before, 1), round(after, 1)])
    js['nodes'][i]['rotation'] = q
bn = bytearray(b0)
while len(bn) % 4: bn.append(0)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
rep = dict(tool="scripts/j_reseat.py", ruling="R-C9-115", deg=DEG, body=os.path.basename(HB), weapons=rec)
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
print(json.dumps(rep))
