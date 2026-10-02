# so_mx R-C9-133/134: the BLOCK RAISE clip knight.gd needs (it measures the LeftHand's rise to its peak in clips_armed.block
# and plays raise_s / lower_s over that span). Built from two held clips on the SAME D7-idle body (identical keys):
#   <from>  idle        -- D7 idle, arms world-held at the sword-and-shield idle's neutral pose (e32)
#   <to>    block_idle  -- D7 idle, arms world-held at the sword-and-shield block-idle pose (e32), the shield up
# block(t) = <from>(t) with the ARM CHAINS' local rotations slerped to <to>(t) by smoothstep(t / RAISE), held after RAISE,
# over [0, LEN]. The torso and legs are D7 idle's (upright), so the raise is the arms only.
#   python3 so16_block_raise.py <in.glb> <out.glb> [--from idle] [--to block_idle] [--name block] [--raise 0.35] [--len 0.6]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); R_ = __import__('49_recentre'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; IN, OUT = a[0], a[1]
opt = lambda k, d: a[a.index(k) + 1] if k in a else d
FR, TO, NAME = opt('--from', 'idle'), opt('--to', 'block_idle'), opt('--name', 'block')
RAISE, LEN = float(opt('--raise', 0.35)), float(opt('--len', 0.6))
ARMS = ("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "RightShoulder", "RightArm", "RightForeArm", "RightHand")
js, b = L.load_glb(IN); b = bytearray(b); nm = {n.get('name'): i for i, n in enumerate(js['nodes'])}
A = {an['name']: an for an in js['animations']}
def chans(an):
    out = {}
    for c in an['channels']:
        s = an['samplers'][c['sampler']]
        out[(c['target']['node'], c['target']['path'])] = (L.read_accessor(js, bytes(b), s['input'])[:, 0], L.read_accessor(js, bytes(b), s['output']))
    return out
cf, ct = chans(A[FR]), chans(A[TO])
def slerp(q0, q1, u):
    q0 = q0 / np.linalg.norm(q0); q1 = q1 / np.linalg.norm(q1); d = float(q0 @ q1)
    if d < 0: q1, d = -q1, -d
    if d > 0.9995: q = q0 + u * (q1 - q0); return q / np.linalg.norm(q)
    th = np.arccos(d); return (np.sin((1 - u) * th) * q0 + np.sin(u * th) * q1) / np.sin(th)
arm_nodes = {nm[x] for x in ARMS}
ch, sm = [], []
def acc(arr, typ):
    arr = np.asarray(arr, np.float32); data = arr.tobytes(); off = W.append(b, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    x = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if typ == 'SCALAR': x['min'] = [float(arr.min())]; x['max'] = [float(arr.max())]
    js['accessors'].append(x); return len(js['accessors']) - 1
times = None
for (node, path), (tt, vv) in cf.items():
    keep = tt <= LEN + 1e-6; t2 = tt[keep]; v2 = vv[keep].copy()
    if node in arm_nodes and path == 'rotation' and (node, path) in ct:
        tt2, vt = ct[(node, path)]
        assert np.allclose(tt2[:len(tt)], tt), "the two held clips must share their keys"
        for k, t in enumerate(t2):
            u = min(t / RAISE, 1.0); u = u * u * (3 - 2 * u)
            v2[k] = slerp(vv[keep][k], vt[keep][k], u)
    ti = acc(t2.reshape(-1), 'SCALAR')
    sm.append({"input": ti, "output": acc(v2, 'VEC4' if path == 'rotation' else 'VEC3'), "interpolation": "LINEAR"})
    ch.append({"sampler": len(sm) - 1, "target": {"node": node, "path": path}})
    times = t2
js['animations'] = [x for x in js['animations'] if x['name'] != NAME] + [{"name": NAME, "channels": ch, "samplers": sm}]
js['buffers'][0]['byteLength'] = len(b); R_.write_glb(OUT, js, b)
print(json.dumps(dict(out=OUT, clip=NAME, frm=FR, to=TO, raise_s=RAISE, len_s=float(times[-1]), keys=int(len(times)))))
