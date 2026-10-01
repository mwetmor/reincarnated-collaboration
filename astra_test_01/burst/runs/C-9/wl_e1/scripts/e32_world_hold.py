# STAGE H: the ARMS in WORLD space (55_clip_graft's transfer rule, applied to the arm chain only). The body clip (legs, hips,
# spine, head) is the upright source; the arm chain takes the G1 carry pose's WORLD orientation (in the root frame) from
# <src.glb>:<clip>@<t>, held on every key of the target: local(t) = parent_world(t)^-1 . R_world_src. So the haft keeps the
# heading and pitch the G1 carry measured (tip forward) whatever the new torso does; the fists ride the new shoulders.
# Binary patch on the target's own key times (no resample; loop seams untouched where the source pose is constant).
#   python3 e32_world_hold.py <in.glb> <out.glb> <src.glb> <srcclip>@<t> <clips> [--json f]
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
ARMS = ("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "RightShoulder", "RightArm", "RightForeArm", "RightHand")
a = sys.argv[1:]; IN, OUT, SRC, ST, CLIPS = a[:5]; sc, stt = ST.split('@'); stt = float(stt); CL = CLIPS.split(',')
rot = lambda M: M[:3, :3] / np.cbrt(np.linalg.det(M[:3, :3]))
ms = C.model(SRC); Gs = C.globals_at(ms, sc, stt)
rootS = [i for i in range(len(ms['nodes'])) if ms['parent'].get(i) is None][0]
Rws = {j: rot(Gs[rootS]).T @ rot(Gs[ms['nid'][j]]) for j in ARMS}            # source arm world rotations, root frame
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']
rootT = [i for i in range(len(m['nodes'])) if m['parent'].get(i) is None][0]
rep = dict(source='%s:%s@%.4f' % (os.path.basename(SRC), sc, stt), clips={})
for cn in CL:
    an = next(x for x in js['animations'] if x['name'] == cn)
    tt = sorted({float(t) for v in m['anims'][cn].values() for t in v[0]})
    newq = {j: [] for j in ARMS}
    for t in tt:
        G = C.globals_at(m, cn, t); world = {}
        for j in ARMS:
            pj = m['parent'][nid[j]]
            pw = world[m['nodes'][pj]['name']] if m['nodes'][pj]['name'] in world else rot(G[rootT]).T @ rot(G[pj])
            world[j] = Rws[j]; loc = pw.T @ Rws[j]; newq[j].append(W.m2q(loc))
    tin = CH.add_accessor(js, bn, np.array(tt), "SCALAR")
    for j in ARMS:
        q = np.array(newq[j]); q /= np.linalg.norm(q, axis=1, keepdims=True)
        for i in range(1, len(q)):
            if np.dot(q[i], q[i - 1]) < 0: q[i] = -q[i]
        an['channels'] = [c for c in an['channels'] if not (c['target']['node'] == nid[j] and c['target']['path'] == 'rotation')]
        o = CH.add_accessor(js, bn, q, "VEC4"); an['samplers'].append({"input": tin, "output": o, "interpolation": "LINEAR"})
        an['channels'].append({"sampler": len(an['samplers']) - 1, "target": {"node": nid[j], "path": "rotation"}})
    rep['clips'][cn] = dict(keys=len(tt))
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4)
R_.write_glb(OUT, js, bn); print(rep)
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
