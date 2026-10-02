# bm_mx STAGE 3 fix (cell-pack gate EDGE_TOUCH, pack d2-ww-barb-mx ca3adf370): a one-shot that TRAVELS (S&S death: the fall carries
# his hips 1.19 m back; at 2.15 s the chest is 1.32 m out, the sword tip 2.66 m, past the +-2.54 m canvas). The D5 de-root rule
# (55_clip_graft +deroot / 45_deroot_trim): the hips' horizontal first-to-last line is removed, the oscillation about it kept --
# then RECENTRED (49's rule) so the clip's hips track is centred on the rest position: offset = -(min + max)/2 of the de-rooted
# track, per axis. Only the Hips TRANSLATION output changes (a new accessor on the same input); every rotation, the weapon keys
# (the floor clamp's turns) and the vertical untouched. Reports the hips' and the far blade's reach before/after.
#   python3 bm14_deroot.py <in.glb> <out.glb> <clip> [--json f]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
IN, OUT, CLIP = sys.argv[1:4]
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']; h = nid['Hips']
G0, _ = W.globals_(js); P = G0[m['parent'][h]]; Pi = np.linalg.inv(P)
an = next(x for x in js['animations'] if x['name'] == CLIP)
ch = next(c for c in an['channels'] if c['target']['node'] == h and c['target']['path'] == 'translation'); s = an['samplers'][ch['sampler']]
tt = L.read_accessor(js, bn, s['input'])[:, 0]; T = L.read_accessor(js, bn, s['output']).astype(float)
pw = np.array([(P @ np.r_[x, 1.0])[:3] for x in T]); rest = G0[h][:3, 3]
def reach(M, clip):
    out = []
    for t in tt:
        G = C.globals_at(M, clip, float(t)); r = max(np.hypot(G[i][0, 3], G[i][2, 3]) for i in G if i in nid.values())
        out.append(r)
    return float(max(out)), float(tt[int(np.argmax(out))])
before = reach(m, CLIP)
u = ((tt - tt[0]) / max(tt[-1] - tt[0], 1e-9))[:, None]; tr = pw[-1] - pw[0]
pw2 = pw - u * np.array([tr[0], 0.0, tr[2]])
for k in (0, 2): pw2[:, k] += rest[k] - (pw2[:, k].min() + pw2[:, k].max()) / 2
T2 = np.array([(Pi @ np.r_[x, 1.0])[:3] for x in pw2])
an['samplers'].append({"input": s['input'], "output": CH.add_accessor(js, bn, T2, "VEC3"), "interpolation": s.get('interpolation', 'LINEAR')}); ch['sampler'] = len(an['samplers']) - 1
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
after = reach(C.model(OUT), CLIP)
rep = dict(clip=CLIP, travel_removed_m=[round(float(tr[0]), 3), round(float(tr[2]), 3)], hips_track_after_m=dict(x=[round(float(pw2[:, 0].min()), 3), round(float(pw2[:, 0].max()), 3)], z=[round(float(pw2[:, 2].min()), 3), round(float(pw2[:, 2].max()), 3)]),
           joint_reach_before_m=[round(before[0], 3), before[1]], joint_reach_after_m=[round(after[0], 3), after[1]])
r = L.lint(OUT); print(json.dumps(rep), '| lint', r['verdict'], r['fails'][:2])
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
