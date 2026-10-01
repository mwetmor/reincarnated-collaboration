# JOIN HOLD v4: THE WEAPON TIPS FORWARD (ruling R-C9-115, Matt: "Get the axe and sword's blade/tip pointed more forward.
# That should be needed for all attacks and walking/running stance and carry forward to whirlwind as well").
#
#   python3 scripts/j_hold_tip.py <hold body.glb> <hold spec.json> <out body.glb> --deg 25 [--json f] [--max-wrist 30]
#
# TIP-FORWARD = the angle between each weapon's grip -> tip axis (its bone's +Y) and his FORWARD (+Z: the direction he
# faces in the game; every JOIN clip is in place, facing +Z). Smaller = more forward.
# THE EDIT, at the WRIST only: each of the six guard poses (join_guard_{R,L}_{idle,walk,run}) gets its HAND turned, in
# world, about the axis (weapon axis x forward) by --deg -- the tip swung --deg toward his forward -- evaluated on the
# state's composed pose at its reference frame (idle_guard 0.5 s; walk / run mid-cycle, the hold's sync layers on) and
# written into the guard clip as the Hand's local rotation (a guard is a single-key pose). Nothing else changes: the
# shoulder, arm and forearm keys are v3's, so the fists stay where v3 put them up to the wrist-to-grip offset.
# A WRIST MORE THAN --max-wrist deg OFF NEUTRAL (the hand's rotation off its rest; v3's guards key the wrist AT rest) is
# reported as a FAIL, not clipped.
# MEASURED per state over the cycle (the hold's own layers, Godot's mixer, the joint lint's pose code): tip-forward per
# weapon, the wrist off neutral, the weapons' closest approach (grip-to-tip segments), the fist's side along the
# shoulder line over the half-width, and the worst on-screen grip-to-tip length (the play camera, 8 headings,
# 100.617 px/m at 1x).
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RUNS = os.path.dirname(ROOT)
args = sys.argv[1:]; HB, SPEC, OUTB = args[0], args[1], args[2]
gopt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
DEG = float(gopt('--deg', '25')); MAXW = float(gopt('--max-wrist', '30')); OUTJ = gopt('--json')
SH, EL = float(gopt('--shoulder', '0')), float(gopt('--elbow', '0'))   # v5: deg (0 = no edit)
spec = json.load(open(SPEC)); lays = json.loads(json.dumps(spec['layers']))
STATE_CLIP = {k: v['clip'] for k, v in spec['states'].items()}
for ly in lays:                                                        # the lint's pose code matches layers on the CLIP name
    ly['states'] = ly['states'] + [STATE_CLIP[s_] for s_ in ly['states'] if s_ in STATE_CLIP]
TMP = OUTB + '.layers.json'; json.dump(lays, open(TMP, 'w'))


def load(body):
    g = {'__file__': os.path.join(HERE, 'j_joint_lint.py'), '__name__': 'j_joint_lint_pose'}
    src = open(os.path.join(HERE, 'j_joint_lint.py')).read()
    sys.argv = [os.path.join(HERE, 'j_joint_lint.py'), body, '--layers', TMP]
    exec(compile(src[:src.index('# ---- LEARN')], 'j_joint_lint.py', 'exec'), g)
    return g


TIP = {'weapon_r': 0.7768, 'weapon_l': 0.8089}; FWD = np.array([0.0, 0, 1])
GUARD = {(st, sd): 'join_guard_%s_%s' % (sd, st) for st in ('idle', 'walk', 'run') for sd in ('R', 'L')}
HAND = {'R': 'RightHand', 'L': 'LeftHand'}; WEAP = {'R': 'weapon_r', 'L': 'weapon_l'}


def ref_t(g, st):
    c = STATE_CLIP[st]; T = g['clip_len'](c); return 0.5 if st == 'idle' else round(0.5 * T * 30) / 30


def nrm(X):
    return X / np.linalg.norm(X, axis=0)


g = load(HB)
W = g['W']; nid = g['nid']; rest = g['rest']; P = g['parent']
new_q = {}
ARM = {'R': ('RightArm', 'RightForeArm'), 'L': ('LeftArm', 'LeftForeArm')}
for (st, sd), gc in GUARD.items():
    loc = g['pose_locals'](STATE_CLIP[st], ref_t(g, st)); G = g['globals_of'](loc)
    if DEG:
        h = nid[HAND[sd]]; Rh = nrm(G[h][:3, :3]); Y = nrm(G[nid[WEAP[sd]]][:3, :3])[:, 1]
        ax = np.cross(Y, FWD); ax = ax / np.linalg.norm(ax)
        Rw = W.axis_angle(ax, math.radians(DEG)) @ Rh                   # the tip swung DEG toward forward
        Rp = nrm(G[P[h]][:3, :3]); new_q[gc, HAND[sd]] = np.array(W.m2q(Rp.T @ Rw), float)
        loc[h] = [loc[h][0], new_q[gc, HAND[sd]], loc[h][2]]; G = g['globals_of'](loc)
    # v5 (the conductor, part 2 of R-C9-115): two named ARM edits, mirrored, measured not solved (v7's discipline):
    if SH:                                                             # the SHOULDER: the upper arm raised forward about his
        La, Ra = G[nid['LeftArm']][:3, 3], G[nid['RightArm']][:3, 3]; lt = La - Ra; lt[1] = 0; lt /= np.linalg.norm(lt)
        i = nid[ARM[sd][0]]; Rp = nrm(G[P[i]][:3, :3])                 # side-to-side axis (the levelled shoulder line)
        new_q[gc, ARM[sd][0]] = np.array(W.m2q(Rp.T @ W.axis_angle(lt, -math.radians(SH)) @ nrm(G[i][:3, :3])), float)
        loc[i] = [loc[i][0], new_q[gc, ARM[sd][0]], loc[i][2]]; G = g['globals_of'](loc)
    if EL:                                                             # the ELBOW: flexed further about its own hinge (the
        sh_, el_, wr_ = (G[nid[b]][:3, 3] for b in (ARM[sd][0], ARM[sd][1], HAND[sd]))   # forearm raised toward horizontal)
        up_, fo_ = (el_ - sh_) / np.linalg.norm(el_ - sh_), (wr_ - el_) / np.linalg.norm(wr_ - el_)
        hinge = np.cross(up_, fo_); hinge /= np.linalg.norm(hinge)
        i = nid[ARM[sd][1]]; Rp = nrm(G[P[i]][:3, :3])
        new_q[gc, ARM[sd][1]] = np.array(W.m2q(Rp.T @ W.axis_angle(hinge, math.radians(EL)) @ nrm(G[i][:3, :3])), float)
        loc[i] = [loc[i][0], new_q[gc, ARM[sd][1]], loc[i][2]]

# write the body: v3's bytes, the six guard clips re-keyed at the Hand (a single-key rotation track, replaced or added)
L = __import__('21_lint_export') if False else None
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); LX = __import__('21_lint_export')
js, b0 = LX.load_glb(HB); bn = bytearray(b0)
def put(data):
    while len(bn) % 4: bn.append(0)
    o = len(bn); bn.extend(data); return o
def acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    a_ = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: a_['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; a_['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(a_); return len(js['accessors']) - 1
for (gc, bone), q in new_q.items():
    an = next(x for x in js['animations'] if x.get('name') == gc); hn = nid[bone]
    ti = acc(np.zeros((1, 1)), 'SCALAR', True); so = acc(q.reshape(1, 4), 'VEC4')
    an['samplers'].append(dict(input=ti, output=so, interpolation='LINEAR'))
    an['channels'] = [c for c in an['channels'] if not (c['target']['node'] == hn and c['target']['path'] == 'rotation')] + \
                     [dict(sampler=len(an['samplers']) - 1, target=dict(node=hn, path='rotation'))]
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUTB, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))

# MEASURE both bodies
P_ = math.radians(52.95354112560294); VIEWS = []
for b_ in (90, 135, 180, 225, 270, 315, 0, 45):
    th = math.radians(90 - b_); c_, s_ = math.cos(th), math.sin(th)
    VIEWS.append(np.array([[c_, 0, s_], [0, 1, 0], [-s_, 0, c_]]).T @ np.array([0.0, -math.sin(P_), -math.cos(P_)]))


def segdist(p1, p2, q1, q2, n=24):
    A = [p1 + (p2 - p1) * u for u in np.linspace(0, 1, n)]; B = [q1 + (q2 - q1) * u for u in np.linspace(0, 1, n)]
    return min(float(np.linalg.norm(a_ - b_)) for a_ in A for b_ in B)


def measure(body):
    gg = load(body); out = {}
    for st in ('idle', 'walk', 'run'):
        c = STATE_CLIP[st]; rows = []
        for t in gg['frames_of'](c):
            loc = gg['pose_locals'](c, t); G = gg['globals_of'](loc)
            La, Ra = G[gg['nid']['LeftArm']][:3, 3], G[gg['nid']['RightArm']][:3, 3]; md = (La + Ra) / 2; lt = La - Ra; lt[1] = 0
            hw = float(np.linalg.norm(lt)) / 2; lt /= np.linalg.norm(lt)
            r = dict(t=t)
            seg = {}
            for sd in ('R', 'L'):
                w = gg['nid'][WEAP[sd]]; R = nrm(G[w][:3, :3]); gp = G[w][:3, 3]; tp = gp + TIP[WEAP[sd]] * R[:, 1]; seg[sd] = (gp, tp)
                r['tipfwd_' + sd] = math.degrees(math.acos(max(-1, min(1, float(R[:, 1] @ FWD)))))
                Dl = W.q2m(np.array(rest[gg['nid'][HAND[sd]]][1], float)).T @ W.q2m(np.array(loc[gg['nid'][HAND[sd]]][1], float))
                r['wrist_' + sd] = math.degrees(math.acos(max(-1, min(1, (np.trace(Dl) - 1) / 2))))
                r['fist_' + sd] = float((gp - md) @ lt) * (1 if sd == 'L' else -1) / hw
                r['px_' + sd] = min(float(np.linalg.norm((tp - gp) - ((tp - gp) @ v) * v)) for v in VIEWS) * 100.617
            r['gap'] = segdist(*seg['R'], *seg['L'])
            rows.append(r)
        A = lambda k, f: round(float(f([x[k] for x in rows])), 2)
        out[st] = dict(frames=len(rows), tip_forward_deg=dict(R=[A('tipfwd_R', min), A('tipfwd_R', max)], L=[A('tipfwd_L', min), A('tipfwd_L', max)]),
                       wrist_off_neutral_max_deg=dict(R=A('wrist_R', max), L=A('wrist_L', max)),
                       fist_side_frac=dict(R=[A('fist_R', min), A('fist_R', max)], L=[A('fist_L', min), A('fist_L', max)]),
                       weapons_closest_m=A('gap', min), screen_len_worst_px_1x=dict(R=A('px_R', min), L=A('px_L', min)))
        out[st]['wrist_verdict'] = 'PASS' if max(out[st]['wrist_off_neutral_max_deg'].values()) <= MAXW else 'FAIL'
        out[st]['gap_verdict'] = 'PASS' if out[st]['weapons_closest_m'] >= 0.22 else 'FAIL'
    return out


rep = dict(instrument="scripts/j_hold_tip.py", ruling="R-C9-115", deg=DEG, shoulder_deg=SH, elbow_deg=EL, max_wrist_deg=MAXW, hold_body=os.path.basename(HB),
           forward="+Z (his in-game facing)", reference_t={st: ref_t(g, st) for st in ('idle', 'walk', 'run')},
           v3=measure(HB), out=measure(OUTB), layers_tmp=TMP)
if OUTJ: json.dump(rep, open(OUTJ, 'w'), indent=1)
for k in ('v3', 'out'):
    for st, v in rep[k].items():
        print("%-4s %-5s tipfwd R %s L %s | wrist max R %.1f L %.1f %s | fist R %s L %s | gap %.3f %s | px R %.1f L %.1f"
              % (k, st, v['tip_forward_deg']['R'], v['tip_forward_deg']['L'], v['wrist_off_neutral_max_deg']['R'], v['wrist_off_neutral_max_deg']['L'],
                 v['wrist_verdict'], v['fist_side_frac']['R'], v['fist_side_frac']['L'], v['weapons_closest_m'], v['gap_verdict'],
                 v['screen_len_worst_px_1x']['R'], v['screen_len_worst_px_1x']['L']))
