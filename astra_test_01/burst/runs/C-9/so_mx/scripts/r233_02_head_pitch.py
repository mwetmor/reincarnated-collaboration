# R-C9-233 step 0 (Matt: "or maybe the character is looking down?"): her HEAD and NECK pitch per clip against the REST
# pose, pure glTF FK on the shipped body (so_mx/export/ss152b/so-body_ss152.glb), every key of every clip she plays.
# The bone's own rest-forward (her facing, glTF +Z, mapped into the bone's rest frame) is carried through the posed bone:
#   pitch_world  degrees BELOW horizontal of that forward in the scene frame (Y up) -- what the camera sees; rest = ~0
#   pitch_hips   the same with the hips' own swing removed (the head bent relative to the pelvis, not the whole body leaning)
# Positive = looking DOWN. Prints a table and writes work/r233/head_pitch.json.
#   python3 r233_02_head_pitch.py <body.glb> <out.json> [clip@t ...]   (the @t clips are the stills' shot times)
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')
m = C.model(sys.argv[1]); OUT = sys.argv[2]
shots = dict((a.split('@')[0], float(a.split('@')[1])) for a in sys.argv[3:])
CLIPS = ['idle', 'walk', 'run', 'cast_fireball_m', 'cast_meteor', 'block', 'hit']
nid = m['nid']; FWD = np.array([0.0, 0.0, 1.0])

def rest_globals():
    G = {}
    def g(i):
        if i in G: return G[i]
        tr, q, s = m['rest'][i]
        M = np.eye(4); M[:3, :3] = C.W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if m['parent'].get(i) is None else g(m['parent'][i]) @ M
        return G[i]
    for i in range(len(m['nodes'])): g(i)
    return G

def rot(M):
    R = M[:3, :3]; return R / np.linalg.norm(R, axis=0, keepdims=True)

G0 = rest_globals()
bones = {'Head': nid['Head'], 'neck': nid['neck']}
hip = nid['Hips']
fl = {k: rot(G0[i]).T @ FWD for k, i in bones.items()}

def pitch(v):
    v = v / np.linalg.norm(v); return float(np.degrees(np.arcsin(-v[1])))

rest = {k: pitch(rot(G0[i]) @ fl[k]) for k, i in bones.items()}
out = {'glb': sys.argv[1], 'rest_pitch_world_deg': rest, 'clips': {}}
print('rest pitch (should be ~0):', {k: round(v, 2) for k, v in rest.items()})
for clip in CLIPS:
    if clip not in m['anims']:
        continue
    t = np.unique(np.round(np.concatenate([v[0] for v in m['anims'][clip].values()]), 6))
    rows = []
    for x in t:
        G = C.globals_at(m, clip, float(x))
        Rh = rot(G[hip]); Rh0 = rot(G0[hip])
        r = {'t': round(float(x), 4)}
        for k, i in bones.items():
            f = rot(G[i]) @ fl[k]
            r[k + '_world'] = round(pitch(f), 2)
            r[k + '_hips'] = round(pitch(Rh0 @ Rh.T @ f), 2)
        rows.append(r)
    def stat(key):
        a = np.array([r[key] for r in rows]); return {'min': round(float(a.min()), 2), 'mean': round(float(a.mean()), 2), 'max': round(float(a.max()), 2)}
    s = {k: stat(k) for k in ('Head_world', 'Head_hips', 'neck_world', 'neck_hips')}
    if clip in shots:
        G = C.globals_at(m, clip, shots[clip]); Rh = rot(G[hip]); Rh0 = rot(G0[hip])
        s['at_shot'] = {'t': shots[clip]}
        for k, i in bones.items():
            f = rot(G[i]) @ fl[k]
            s['at_shot'][k + '_world'] = round(pitch(f), 2); s['at_shot'][k + '_hips'] = round(pitch(Rh0 @ Rh.T @ f), 2)
    out['clips'][clip] = {'keys': len(rows), 'stats': s, 'rows': rows}
    print('%-16s keys %3d  Head world mean %6.2f [%6.2f..%6.2f]  hips mean %6.2f | neck world mean %6.2f  hips %6.2f %s' % (
        clip, len(rows), s['Head_world']['mean'], s['Head_world']['min'], s['Head_world']['max'], s['Head_hips']['mean'],
        s['neck_world']['mean'], s['neck_hips']['mean'], ('| at shot ' + json.dumps(s['at_shot'])) if 'at_shot' in s else ''))
json.dump(out, open(OUT, 'w'), indent=1)
