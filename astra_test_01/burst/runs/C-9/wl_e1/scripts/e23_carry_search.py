# READY-DIAGONAL CARRY SEARCH (free: every key of every clip already fetched on his rig). For a candidate arm pose (the arm
# chain's LOCAL rotations from <clip>@<t>), apply it to the target clips (idle, walk, run) and measure, per target key, in
# his ROOT frame (forward +Z, up +Y; metres, his 1.96 m scale): the haft from the left fist through the right fist (e12's
# grip: the head lies beyond the right fist, 0.57 m to its centre), its elevation and its bearing off forward, the head's
# height, the fists' separation and vertical stack (|dy| / separation), and both fists' forwardness.
# Score: head forward (bearing |.| <= 35 deg), head at shoulder height (1.45-1.75 m), elevation 15-50 deg, fists 0.25-0.55 m
# apart and NOT stacked (|dy|/sep < 0.7), the fists in front of the chest.
import sys, os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
ARMS = ("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "RightShoulder", "RightArm", "RightForeArm", "RightHand")
BODY = os.environ.get('E1_BODY', 'export/final/wl_body.glb'); K = 1.96 / 1.70; HEADC = 1.45 - 0.68 - 0.20
m = C.model(BODY); nid = m['nid']
jb, bb = L.load_glb(BODY)
cR = W.hand_points(jb, bb, 'RightHand', 0.6)[0].mean(0); cL = W.hand_points(jb, bb, 'LeftHand', 0.6)[0].mean(0)
# SOURCES IN THE BODY'S OWN LOCAL FRAMES (v2): the candidates are GRAFTED onto his rig first (55_clip_graft, world-space
# transfer) -- v1 read the library GLB's local rotations directly, and Meshy's local rests are not the body's, so its
# predictions did not survive e09_hold (walk predicted 35 deg / head 1.66 m, measured -12 deg / 1.00 m).
SG = C.model('work/_srcs.glb')
srcs = {c[4:]: dict(SG, anims={c: SG['anims'][c]}) for c in SG['anims'] if c.startswith('src_')}
def keytimes(ch): return sorted({float(t) for v in ch.values() for t in v[0]})
def armpose(ms, clip, t):
    out = {}
    for j in ARMS:
        n = ms['nid'][j]
        if (n, 'rotation') not in ms['anims'][clip]: out[nid[j]] = m['rest'][nid[j]][1]; continue
        tt, vv = ms['anims'][clip][(n, 'rotation')]
        i = int(np.argmin(np.abs(tt - t))); out[nid[j]] = vv[i]
    return out
def measure(target, pose):
    ch = dict(m['anims'][target]); rows = []
    for n, q in pose.items(): ch[(n, 'rotation')] = (np.array([0.0]), np.array([q]))
    mm = dict(m, anims={target: ch})
    for t in keytimes(m['anims'][target])[::3]:
        G = C.globals_at(mm, target, t); root = G[[i for i in range(len(m['nodes'])) if m['parent'].get(i) is None and m['nodes'][i].get('name') == 'Armature'][0]]
        Ri = np.linalg.inv(root)
        R = (Ri @ G[nid['RightHand']] @ np.r_[cR, 1])[:3];  # (v2 fix: v1 scaled R by K twice -- a 15% error that moved the haft)
        Lf = (Ri @ G[nid['LeftHand']] @ np.r_[cL, 1])[:3]
        # root frame is in rig units (cm): to metres at 1.96 m
        R = R * 0.01 * K; Lf = Lf * 0.01 * K
        chest = (Ri @ G[nid['Spine02']])[:3, 3] * 0.01 * K
        d = R - Lf; sep = float(np.linalg.norm(d)); u = d / max(sep, 1e-9); head = R + u * HEADC
        elev = math.degrees(math.asin(np.clip(u[1], -1, 1))); bear = math.degrees(math.atan2(u[0], u[2]))
        rows.append(dict(t=t, sep=sep, stack=abs(d[1]) / max(sep, 1e-9), elev=elev, bear=bear, head_y=float(head[1]), head_fwd=float(head[2]),
                         fist_fwd=float(min(R[2], Lf[2]) - chest[2])))
    return rows
def score(rows):
    s = 0
    for r in rows:
        s += (abs(r['bear']) <= 35) + (1.45 <= r['head_y'] <= 1.80) + (15 <= r['elev'] <= 50) + (0.22 <= r['sep'] <= 0.6) + (r['stack'] < 0.7) + (r['fist_fwd'] > 0.05)
    return s / (6.0 * len(rows))
res = []
for name, ms in srcs.items():
    clip = list(ms['anims'])[0]
    for t in keytimes(ms['anims'][clip])[::2]:
        pose = armpose(ms, clip, t)
        per = {tg: measure(tg, pose) for tg in ('idle', 'walk', 'run')}
        sc = float(np.mean([score(v) for v in per.values()])); pts = {tg: round(score(v), 3) for tg, v in per.items()}
        med = {tg: {k: round(float(np.median([r[k] for r in v])), 3) for k in ('sep', 'stack', 'elev', 'bear', 'head_y', 'fist_fwd')} for tg, v in per.items()}
        res.append(dict(src=name, t=round(t, 4), score=round(sc, 3), per_target=pts, med=med))
res.sort(key=lambda r: -r['score'])
json.dump(res, open('work/carry_search.json', 'w'), indent=1)
for tg in ('idle', 'walk', 'run'):
    b = sorted(res, key=lambda r: -r['per_target'][tg])[:3]
    for r in b: print('BEST', tg, r['src'], r['t'], r['per_target'][tg], r['med'][tg])
for r in res[:12]: print(r['src'], r['t'], r['score'], r['med']['idle'], r['med']['run']['bear'], r['med']['walk']['bear'])
