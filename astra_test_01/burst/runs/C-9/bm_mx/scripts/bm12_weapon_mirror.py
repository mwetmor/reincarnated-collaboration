# bm_mx STAGE 3 (R-C9-133): the OFF-HAND AXE carried as the MIRROR of the sword. The left arm carries by the chest-frame mirror (bm09),
# but the kit's off-hand seat WL is the JOIN guard's (built for its own hold), not the mirror of the sword's seat W in a mirrored hand --
# so on the mirrored carry the axe pointed ACROSS him (walk: bearing -98 deg, the blades 2.6% overlapping). A weapon_l ROTATION key
# per key makes the axe's world frame the sword's reflected through his chest's sagittal plane (S_c R_sword S_c: a proper rotation;
# the haft along the mirrored blade, the edge along the mirrored flat's normal); the mount's translation is kept (the grip stays in
# the fist).
#   --frame root (default chest): reflect through his ROOT sagittal plane (x = 0) instead -- the axe stance's Spine bone is turned ~35 deg
#     from his facing (bladed), so a chest-plane mirror points the axe ~65 deg across him; his facing is the plane that reads in game.
#   mirror <in> <out> mirror <clip,clip>          per key (idle / walk / run: the carry clips)
#   hold   <in> <out> hold <src>@<t> <clip,clip>  the weapon_l LOCAL rotation of <src>@<t> (after its mirror keying), constant over each
#                                                 clip's keys -- for clips whose left arm is held at that carry pose (bm11)
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT, MODE = a[0], a[1], a[2]
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']
def rot(M): R = M[:3, :3]; return R / np.cbrt(np.linalg.det(R))
G0, _ = W.globals_(js); Cr0 = rot(G0[nid['Spine']]); S = np.diag([-1.0, 1.0, 1.0]); Sc = Cr0.T @ S @ Cr0
wl = nid['weapon_l']; ROOTF = '--frame' in a and a[a.index('--frame') + 1] == 'root'
def put(clip, tin, qs):
    an = next(x for x in js['animations'] if x['name'] == clip)
    qs = np.array(qs)
    for i in range(1, len(qs)):
        if np.dot(qs[i], qs[i - 1]) < 0: qs[i] = -qs[i]
    an['samplers'].append({"input": tin, "output": CH.add_accessor(js, bn, qs, "VEC4"), "interpolation": "LINEAR"})
    ch = next((c for c in an['channels'] if c['target']['node'] == wl and c['target']['path'] == 'rotation'), None)
    if ch is None: an['channels'].append({"sampler": len(an['samplers']) - 1, "target": {"node": wl, "path": "rotation"}})
    else: ch['sampler'] = len(an['samplers']) - 1
def tin_of(clip):
    an = next(x for x in js['animations'] if x['name'] == clip)
    ch = next(c for c in an['channels'] if c['target']['node'] == nid['LeftArm'] and c['target']['path'] == 'rotation')
    s = an['samplers'][ch['sampler']]['input']; return s, L.read_accessor(js, bn, s)[:, 0]
rep = dict(mode=MODE, frame='root' if ROOTF else 'chest', clips={})
def mirror_local(G):
    Ct = rot(G[nid['Spine']]); Rs = rot(G[nid['weapon_r']]); Sw = S if ROOTF else Ct @ Sc @ Ct.T   # root plane, or the chest's, now
    Ra = Sw @ Rs @ Sw; return W.m2q(rot(G[nid['LeftHand']]).T @ Ra)
if MODE == 'mirror':
    for clip in a[3].split(','):
        tin, tt = tin_of(clip); put(clip, tin, [mirror_local(C.globals_at(m, clip, float(t))) for t in tt]); rep['clips'][clip] = len(tt)
elif MODE == 'hold':
    sc, st = a[3].split('@'); q = mirror_local(C.globals_at(m, sc, float(st)))
    for clip in a[4].split(','):
        tin, tt = tin_of(clip); put(clip, tin, [q] * len(tt)); rep['clips'][clip] = len(tt)
    rep['source'] = a[3]
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
r = L.lint(OUT); print(json.dumps(rep), '| lint', r['verdict'], r['fails'][:2])
