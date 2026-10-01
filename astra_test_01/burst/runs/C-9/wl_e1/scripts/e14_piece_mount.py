# E1: give each Blender-exported gear piece the body's weapon_r REST (the mace grip, work/weapon_mount.json) and the matching
# IBM, and snap weapon_l -- so every file carries the identical 26-joint skeleton the body does (gear.gd compares lists and the
# lint's WEAPON REST row compares rests). Binary patch. Then lint each.  python3 e14_piece_mount.py <piece.glb> ...
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
Wm = np.array(json.load(open(os.path.join(os.path.dirname(HERE), 'work', 'weapon_mount.json')))['W'])
for p in sys.argv[1:]:
    W.ensure(p, p)
    js, b = L.load_glb(p); b = bytearray(b); n = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
    W.set_trs(js['nodes'][n['weapon_r']], Wm); js['nodes'][n['weapon_r']]['scale'] = [1.0, 1.0, 1.0]
    G, _ = W.globals_(js)
    sk = js['skins'][0]; names = [js['nodes'][j]['name'] for j in sk['joints']]
    ibm = W.mat_list(js, bytes(b), sk['inverseBindMatrices']); ibm[names.index('weapon_r')] = np.linalg.inv(G[n['weapon_r']])
    data = b''.join(struct.pack('<16f', *M.T.reshape(-1)) for M in ibm); off = W.append(b, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": len(ibm), "type": "MAT4"})
    sk['inverseBindMatrices'] = len(js['accessors']) - 1; js['buffers'][0]['byteLength'] = len(b) + (-len(b) % 4)
    R_.write_glb(p, js, b); W.snap(p)
    r = L.lint(p); print(os.path.basename(p), r['verdict'], r['fails'][:3])
