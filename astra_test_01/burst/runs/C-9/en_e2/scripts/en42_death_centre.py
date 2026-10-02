# EN-E2 round 6: a long full-length death FALL can overrun the 768 cell sideways (the brute's Pro Magic death backward: 7 px margin at E/W).
# Instead of shrinking the body (a size call), the fall is CENTRED: the Hips' ground track gets a smoothstep-ramped horizontal offset, 0 at the
# first key (the standing pose stays exactly on the anchor) to -c at the last key, c = the horizontal centre of the FINAL pose's joint box
# (head, hands, feet: the corpse ends centred on the anchor instead of lying out to one side). The fall still travels, only less far.
#   python3 scripts/en42_death_centre.py <in.glb> <out.glb> [--clip death] [--frac 1.0] [--tip units] [--json f]
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre'); G55 = __import__('55_clip_graft'); C = __import__('s17_loop_closure')
a = sys.argv[1:]; IN, OUT = a[0], a[1]
CLIP = a[a.index('--clip') + 1] if '--clip' in a else 'death'; FR = float(a[a.index('--frac') + 1]) if '--frac' in a else 1.0
m = C.model(IN); ts = sorted({float(t) for v in m['anims'][CLIP].values() for t in v[0]})
Gl = C.globals_at(m, CLIP, ts[-1]); P = np.array([Gl[i][:3, 3] for i in Gl if i in m['joints']])
# round 6 fix: the joint box misses the HANDS' reach (the brute's fist runs 0.47 units past its wrist): add each hand's tip, along the
# forearm->hand direction, --tip units (the en34 tip / the export factor)
TIP = float(a[a.index('--tip') + 1]) if '--tip' in a else 0.0
nid = {m['nodes'][i].get('name'): i for i in m['joints']}
for h, fa in (('RightHand', 'RightForeArm'), ('LeftHand', 'LeftForeArm')):
    d_ = Gl[nid[h]][:3, 3] - Gl[nid[fa]][:3, 3]; P = np.vstack([P, Gl[nid[h]][:3, 3] + TIP * d_ / max(np.linalg.norm(d_), 1e-9)])
c = np.array([(P[:, 0].max() + P[:, 0].min()) / 2, 0.0, (P[:, 2].max() + P[:, 2].min()) / 2]) * FR
js, b = L.load_glb(IN); bn = bytearray(b)
idx = {n.get('name'): i for i, n in enumerate(js['nodes'])}; hips = idx['Hips']
G0, par = G55.world_rest(js); Pinv = np.linalg.inv(G0[par[hips]])
an = next(x for x in js['animations'] if x['name'] == CLIP)
ch = next(x for x in an['channels'] if x['target']['node'] == hips and x['target']['path'] == 'translation')
s = an['samplers'][ch['sampler']]; t = np.asarray(L.read_accessor(js, bn, s['input'])).reshape(-1); v = np.asarray(L.read_accessor(js, bn, s['output'])).copy()
u = (t - t[0]) / max(t[-1] - t[0], 1e-9); w = u * u * (3 - 2 * u)
# the scene root's scale (e19) is above the armature: c is in the SCENE's metres; convert through the inverse of the parent's world matrix
d_local = (Pinv[:3, :3] @ (-c))
v = v + w[:, None] * d_local[None, :]
arr = v.astype(np.float32); data = arr.tobytes(); off = W.append(bn, data)
js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": "VEC3"})
s['output'] = len(js['accessors']) - 1
js['buffers'][0]['byteLength'] = len(bn); R_.write_glb(OUT, js, bn)
m2 = C.model(OUT); Gl2 = C.globals_at(m2, CLIP, ts[-1]); P2 = np.array([Gl2[i][:3, 3] for i in Gl2 if i in m2['joints']])
rep = dict(clip=CLIP, final_box_centre_before_m=[round(float(x), 4) for x in c[[0, 2]]], frac=FR,
           final_joint_box_x=[round(float(P2[:, 0].min()), 3), round(float(P2[:, 0].max()), 3)], final_joint_box_z=[round(float(P2[:, 2].min()), 3), round(float(P2[:, 2].max()), 3)])
print('CENTRE', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
