# Bake the Meteor's STAFF motion into cast_meteor as a weapon_r rotation track -- in glTF space.
#
#   python3 scripts/s13_meteor_track.py <in body.glb> <out body.glb> [--lean 30] [--json f]
#
# The rule, chosen by measurement (scripts/s12_measure.py; 638 verts inside her with pass 1's staff,
# 103 with the seated one, 32 upright, 8 grazes <= 1.1 cm with this):
#   w    = smoothstep of the fist's height from the shoulder (0) down to the hips (1)
#          SEATED while the fist is high -- the shaft across the fist clears a raised arm, where an
#          upright staff runs down through it -- and UPRIGHT as it comes down, a stamp
#   lean = 30 deg x (smoothstep of her head's drop from standing to 0.90 m), LATERAL to her right:
#          in the ground-slam crouch her head is over the fist and her thighs in front of it, and a
#          forward lean ran the staff through the thighs (44 -> 134 verts)
#   staff turn = slerp(identity, arc(shaft -> lean-tilted vertical), w), about the grip
#
# Written in glTF space because it must land AFTER 52_weapon_bones: a Blender export re-orders
# the joints by hierarchy and undoes the appended weapon_r / weapon_l.
# Every OTHER clip gains a one-key weapon_r track at its rest rotation. Godot keeps a bone's last
# value when the next clip has no track for it, so without these the staff would stay in the
# Meteor's last pose after it ends.
#
# THE GROUND (--staff): the grip sits at the staff's MIDDLE (weapon_r local y -87.1..+87.7 cm), and
# in the slam the fist comes down to 0.22 m -- which put the butt 0.54 m UNDER the snow. The first
# film showed it: a stub of staff sticking out of the ground. So the Meteor also gets a weapon_r
# TRANSLATION track that slides the staff up THROUGH the hand, along its own axis, exactly as far
# as keeps the butt at the ground (GROUND_M) -- the butt planted, the hand driven down the shaft:
# a stamp. Only in the slam (SLAM_CW); never past 10 cm from the butt; nothing while the butt is up.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
a = sys.argv[1:]
SRC, DST = a[0], a[1]
LEAN = float(a[a.index('--lean') + 1]) if '--lean' in a else 30.0
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
STAFF = a[a.index('--staff') + 1] if '--staff' in a else None
GROUND_M = -0.03                  # butt may sink this far INTO the snow (y = 0 is her feet's ground):
                                  # a stamped staff bites into snow, and every cm of slide spared keeps
                                  # the butt's knob off her toe (the slide first grazed it 1.15 cm)
SLAM_CW = 0.5                     # slide only in the SLAM (crouch weight >= this): in the opening
                                  # stance the butt sits 4-9 cm in the snow beside her right foot, and
                                  # sliding it up there put its knob 6.8 cm into her shin (measured)
js, bin0 = L.load_glb(SRC)
bin_ = bytearray(bin0)
nodes = js['nodes']
name = {i: n.get('name') for i, n in enumerate(nodes)}
nid = {v: k for k, v in name.items()}
parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
wr = nid['weapon_r']
REST = {i: (np.array(n.get('translation', [0, 0, 0]), float), np.array(n.get('rotation', [0, 0, 0, 1]), float),
            np.array(n.get('scale', [1, 1, 1]), float)) for i, n in enumerate(nodes)}


def mat(t, q, s):
    M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = t; return M


def globals_at(local):
    G = {}
    def g(i):
        if i in G: return G[i]
        t, q, s = local.get(i, REST[i])
        m = mat(t, q, s)
        G[i] = m if parent.get(i) is None else g(parent[i]) @ m
        return G[i]
    for i in range(len(nodes)): g(i)
    return G


rotonly = lambda M: M[:3, :3] / np.linalg.norm(M[:3, :3], axis=0)
smooth = lambda x: (lambda c: c * c * (3 - 2 * c))(min(1.0, max(0.0, x)))
G0 = globals_at({})
HEAD_REST = G0[nid['Head']][1, 3]
BUTT_U = None                     # butt along weapon_r's local +Y, in local units (negative)
if STAFF:
    sj, sb = L.load_glb(STAFF)
    sk_ = sj['skins'][0]; jn = [sj['nodes'][j].get('name') for j in sk_['joints']]
    ibm = L.read_accessor(sj, sb, sk_['inverseBindMatrices']).reshape(-1, 4, 4)[jn.index('weapon_r')].T
    sp = L.read_accessor(sj, sb, sj['meshes'][0]['primitives'][0]['attributes']['POSITION'])
    ql = (ibm @ np.c_[sp, np.ones(len(sp))].T).T[:, :3]
    BUTT_U = float(ql[:, 1].min())
    print("staff along weapon_r +Y: butt %.2f .. crown %.2f local units" % (BUTT_U, float(ql[:, 1].max())))
anim = next(an for an in js['animations'] if an.get('name') == 'cast_meteor')
chans = {}
times = None
for ch in anim['channels']:
    t = ch['target']; smp = anim['samplers'][ch['sampler']]
    tt = L.read_accessor(js, bin_, smp['input'])[:, 0]
    vv = L.read_accessor(js, bin_, smp['output'])
    chans[(t['node'], t['path'])] = (tt, vv)
    if times is None or len(tt) > len(times):
        times, tin = tt, smp['input']


def sample(tt, vv, t):
    i = int(np.clip(np.searchsorted(tt, t), 0, len(tt) - 1))
    return vv[i]


out_q, out_t, rep = [], [], []
for t in times:
    local = {}
    for (n, p), (tt, vv) in chans.items():
        tr, q, s = local.get(n, REST[n])
        v = sample(tt, vv, t)
        if p == 'translation': tr = v
        elif p == 'rotation': q = v
        elif p == 'scale': s = v
        local[n] = (np.array(tr, float), np.array(q, float), np.array(s, float))
    Gt = globals_at(local)
    Rh = rotonly(Gt[nid['RightHand']])
    Rw = rotonly(Gt[wr])
    s_ = Rw @ np.array([0.0, 1.0, 0.0])                       # the shaft, to the crown (glTF, Y up)
    y = lambda n: Gt[nid[n]][1, 3]
    w = smooth((y('RightArm') - y('RightHand')) / max(y('RightArm') - y('Hips'), 1e-6))
    cw = smooth((HEAD_REST - y('Head')) / max(HEAD_REST - 0.90, 1e-6))
    o = Gt[nid['RightArm']][:3, 3] - Gt[nid['LeftArm']][:3, 3]; o[1] = 0.0
    o = o / max(np.linalg.norm(o), 1e-9)
    th = math.radians(LEAN) * cw
    tgt = np.array([0.0, 1.0, 0.0]) * math.cos(th) + o * math.sin(th)
    ax = np.cross(s_, tgt); sn = np.linalg.norm(ax); cs = float(np.clip(s_ @ tgt, -1, 1))
    ang = math.atan2(sn, cs) * w
    Rq = np.eye(3) if sn < 1e-9 else W.axis_angle(ax / sn, ang)[:3, :3]
    new_local = Rh.T @ (Rq @ Rw)                              # weapon_r's LOCAL rotation under RightHand
    q = W.m2q(new_local); q = q / np.linalg.norm(q)
    if out_q and float(np.dot(q, out_q[-1])) < 0: q = -q     # keep the track continuous for slerp
    out_q.append(q)
    slide_m = 0.0; butt_y = None
    if BUTT_U is not None:
        su = float(np.linalg.norm(Gt[nid['RightHand']][:3, 0]))          # metres per local unit
        sh2 = (Rh @ new_local) @ np.array([0.0, 1.0, 0.0])               # the turned shaft, world
        grip = Gt[wr][:3, 3]
        butt_y = float(grip[1] + sh2[1] * BUTT_U * su)
        if butt_y < GROUND_M and sh2[1] > 0.2 and cw >= SLAM_CW:
            slide_m = min((GROUND_M - butt_y) / sh2[1], -BUTT_U * su - 0.10)
        out_t.append(REST[wr][0] + new_local @ np.array([0.0, slide_m / su, 0.0]))
    rep.append(dict(t=round(float(t), 4), w=round(w, 3), crouch=round(cw, 3), turn_deg=round(math.degrees(ang), 2),
                    butt_y_m=None if butt_y is None else round(butt_y, 4), slide_m=round(slide_m, 4)))


def add_accessor(arr, typ):
    data = np.asarray(arr, np.float32).tobytes()
    off = W.append(bin_, data)
    js['bufferViews'].append(dict(buffer=0, byteOffset=off, byteLength=len(data)))
    acc = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(len(arr)), type=typ)
    if typ == 'SCALAR':
        acc['min'] = [float(np.min(arr))]; acc['max'] = [float(np.max(arr))]
    js['accessors'].append(acc)
    return len(js['accessors']) - 1


anim['samplers'].append(dict(input=tin, output=add_accessor(np.array(out_q), 'VEC4'), interpolation='LINEAR'))
anim['channels'].append(dict(sampler=len(anim['samplers']) - 1, target=dict(node=wr, path='rotation')))
if out_t:
    anim['samplers'].append(dict(input=tin, output=add_accessor(np.array(out_t), 'VEC3'), interpolation='LINEAR'))
    anim['channels'].append(dict(sampler=len(anim['samplers']) - 1, target=dict(node=wr, path='translation')))
rest_q = REST[wr][1]
rest_t = REST[wr][0]
others = []
for an in js['animations']:
    if an is anim or any(c['target'].get('node') == wr for c in an['channels']):
        continue
    ti = an['samplers'][0]['input']
    t0 = float(L.read_accessor(js, bin_, ti)[0, 0])
    inp = add_accessor(np.array([[t0]]), 'SCALAR')
    an['samplers'].append(dict(input=inp, output=add_accessor(np.array([rest_q]), 'VEC4'), interpolation='STEP'))
    an['channels'].append(dict(sampler=len(an['samplers']) - 1, target=dict(node=wr, path='rotation')))
    if out_t:
        an['samplers'].append(dict(input=inp, output=add_accessor(np.array([rest_t]), 'VEC3'), interpolation='STEP'))
        an['channels'].append(dict(sampler=len(an['samplers']) - 1, target=dict(node=wr, path='translation')))
    others.append(an.get('name'))
js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
while len(bin_) % 4: bin_.append(0)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(DST, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bin_)))
    f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bin_), b'BIN\x00')); f.write(bytes(bin_))
print("cast_meteor: weapon_r track, %d keys, turn %.1f..%.1f deg; one-key rest tracks on %s"
      % (len(out_q), min(r['turn_deg'] for r in rep), max(r['turn_deg'] for r in rep), others))
if out_t:
    sl = [r for r in rep if r['slide_m'] > 0]
    print("  ground: butt lowest %.3f m before the slide; slid at %d of %d keys, up to %.3f m (%.2f..%.2f s)"
          % (min(r['butt_y_m'] for r in rep), len(sl), len(rep), max([r['slide_m'] for r in rep] or [0]),
             sl[0]['t'] if sl else 0, sl[-1]['t'] if sl else 0))
Lr = L.lint(DST)
print("lint %s, %d fails; clips %s" % (Lr['verdict'], len(Lr['fails']), sorted(Lr['clips'])))
if OUTJ:
    json.dump(dict(rule=dict(lean_deg=LEAN, lean_dir="lateral, her right", head_crouch_m=0.90,
                             ground=dict(butt_units=BUTT_U, ground_m=GROUND_M) if BUTT_U is not None else None), keys=rep),
              open(OUTJ, 'w'), indent=1)
