# WHIRLWIND v7 POSE (ruling R-C9-108; Matt: "simply use a slightly extended version of the current battle stance ... this
# shouldn't be so complex and difficult"). NO SOLVER. One frame of his battle stance, two joint edits per arm, nothing else.
#
#   python3 scripts/j_whirl7_pose.py <hold body.glb> <out pose.json> [--t 0.5] [--shoulder 15] [--elbow 15]
#
#   1. POSE: the JOIN hold's idle as shipped -- idle_guard at --t, the hold's guard_R_idle / guard_L_idle layers at weight 1
#      ("pose" time, filter_from all_clips: each layer's four arm bones take the guard clip's value, an un-keyed one REST).
#      That one frame is the whole body: legs, torso, head, both arms, both weapons (the weapon bones at their mount rest).
#   2. EXTEND, the same two edits on both arms, mirrored, every other bone untouched:
#      a. SHOULDER: the upper arm (Left/RightArm) raised FORWARD by --shoulder deg: a world rotation about his
#         side-to-side axis (the levelled shoulder line) through the shoulder joint -- flexion only, no turn in or out.
#      b. ELBOW: the bend OPENED by --elbow deg about the elbow's own hinge (the normal of the upper-arm / forearm plane,
#         at the stance's own bend) -- no other axis.
#      The hand keeps its rotation relative to the forearm, so each weapon rides along exactly as it sits in the stance.
#   Out: every node's local TRS (j_whirl5.py reads it), the edit record, and the before / after angles as measured.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts")); sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts"))
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, OUT = a[0], a[1]
opt = lambda k, d=None: float(a[a.index(k) + 1]) if k in a else d
T0, SH, EL = opt('--t', 0.5), math.radians(opt('--shoulder', 15)), math.radians(opt('--elbow', 15))
m = C.model(BODY); nid = m['nid']; P = m['parent']; N = len(m['nodes'])


def locals_of(clip, t):
    loc = {i: [np.array(v, float) for v in m['rest'][i]] for i in range(N)}
    for (n, p), (tt, vv) in m['anims'][clip].items():
        k = int(np.searchsorted(tt, t - 1e-6)); k = min(max(k, 0), len(tt) - 1)
        if 0 < k and tt[k] > t:
            u = (t - tt[k - 1]) / (tt[k] - tt[k - 1]); v0, v1 = np.array(vv[k - 1], float), np.array(vv[k], float)
            if p == 'rotation':
                if v0 @ v1 < 0: v1 = -v1
                v = (1 - u) * v0 + u * v1; v = v / np.linalg.norm(v)
            else:
                v = (1 - u) * v0 + u * v1
        else:
            v = np.array(vv[k], float)
        loc[n][{'translation': 0, 'rotation': 1, 'scale': 2}[p]] = v
    return loc


ARMS = {'R': ["RightShoulder", "RightArm", "RightForeArm", "RightHand"], 'L': ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand"]}
loc = locals_of('idle_guard', T0)
for s_, bones in ARMS.items():                                         # the hold's guard layers at weight 1
    g = locals_of('join_guard_%s_idle' % s_, 0.0)
    for b in bones: loc[nid[b]] = g[nid[b]]


def globals_of(loc):
    G = {}
    def gg(i):
        if i in G: return G[i]
        tr, q, s = loc[i]; M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if P.get(i) is None else gg(P[i]) @ M
        return G[i]
    for i in range(N): gg(i)
    return G


def nrm(X):
    return X / np.linalg.norm(X, axis=0)


def set_world_rot(loc, G, i, Rw):
    """the bone's local rotation such that its world rotation is Rw (its translation and scale kept)"""
    Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3)
    loc[i] = [loc[i][0], np.array(W.m2q(Rp.T @ Rw), float), loc[i][2]]


def measure(G):
    La, Ra = G[nid['LeftArm']][:3, 3], G[nid['RightArm']][:3, 3]; md = (La + Ra) / 2; lt = La - Ra; lt[1] = 0; lt /= np.linalg.norm(lt)
    fw = np.cross(lt, [0.0, 1, 0]); hw = float(np.linalg.norm((La - Ra)[[0, 2]])) / 2
    out = {}
    for s_, sg in (('R', -1), ('L', 1)):
        sh, el, wr = (G[nid[b]][:3, 3] for b in ARMS[s_][1:])
        up, fo = (el - sh) / np.linalg.norm(el - sh), (wr - el) / np.linalg.norm(wr - el)
        out[s_] = dict(upper_arm_forward_deg=round(math.degrees(math.atan2(float(up @ fw), float(-up[1]))), 1),
                       elbow_bend_deg=round(math.degrees(math.acos(max(-1, min(1, float(up @ fo))))), 1),
                       fist_side=round(float((G[nid['weapon_' + s_.lower()]][:3, 3] - md) @ lt) * sg / hw, 3),
                       grip_y_m=round(float(G[nid['weapon_' + s_.lower()]][1, 3]), 3))
    return out, lt, fw


G = globals_of(loc); before, lt, fw = measure(G)
for s_ in ('R', 'L'):                                                  # a. the shoulder: forward flexion about the shoulder line
    G = globals_of(loc); i = nid[ARMS[s_][1]]
    Rflex = W.axis_angle(lt, -SH)                                       # about +left by -angle: a hanging arm swings FORWARD (asserted)
    set_world_rot(loc, G, i, Rflex @ nrm(G[i][:3, :3]))
for s_ in ('R', 'L'):                                                  # b. the elbow: opened about its own hinge
    G = globals_of(loc); sh, el, wr = (G[nid[b]][:3, 3] for b in ARMS[s_][1:])
    up, fo = (el - sh) / np.linalg.norm(el - sh), (wr - el) / np.linalg.norm(wr - el)
    hinge = np.cross(up, fo); hinge /= np.linalg.norm(hinge)           # +angle about it bends further; -angle opens
    i = nid[ARMS[s_][2]]
    set_world_rot(loc, G, i, W.axis_angle(hinge, -EL) @ nrm(G[i][:3, :3]))
G = globals_of(loc); after, _, _ = measure(G)
for s_ in ('R', 'L'):
    d_f = after[s_]['upper_arm_forward_deg'] - before[s_]['upper_arm_forward_deg']; d_e = before[s_]['elbow_bend_deg'] - after[s_]['elbow_bend_deg']
    assert SH == 0 or d_f > 0, ("the shoulder edit did not raise the arm forward", s_, d_f)
    assert EL == 0 or abs(d_e - math.degrees(EL)) < 0.5, ("the elbow edit did not open the bend by the asked angle", s_, d_e)
rep = dict(method="one frame of his battle stance + two joint edits per arm (no solver): see the header", ruling="R-C9-108",
           body=os.path.basename(BODY), stance=dict(clip="idle_guard", t=T0, layers=["guard_R_idle (join_guard_R_idle, weight 1)", "guard_L_idle (join_guard_L_idle, weight 1)"]),
           edits=dict(shoulder_forward_deg=math.degrees(SH), elbow_open_deg=math.degrees(EL), shoulder_axis="the levelled shoulder line (his side-to-side)",
                      elbow_axis="the elbow's hinge: the normal of the upper-arm / forearm plane at the stance's bend", others="untouched"),
           before=before, after=after,
           locals={m['nodes'][i].get('name'): dict(t=[float(v) for v in loc[i][0]], r=[float(v) for v in loc[i][1]], s=[float(v) for v in loc[i][2]]) for i in range(N)})
json.dump(rep, open(OUT, 'w'), indent=1)
print(json.dumps(dict(before=before, after=after)))
