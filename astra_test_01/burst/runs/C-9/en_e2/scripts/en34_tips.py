# EN-E2: the hand-TIP socket offsets of a shipped body: per hand, the farthest vertex weighted > 0.5 to that hand, along the hand bone's +Y,
# at rest, in world metres (the render_cells.gd socket rule: bone origin + along_bone_m x the bone's normalised +Y).
#   python3 scripts/en34_tips.py <body.glb> <out.json>
import sys, json, numpy as np, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
js, b = L.load_glb(sys.argv[1]); G, _ = W.globals_(js)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n); V = W.skin_rest(js, b, mn, G)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
J = np.asarray(L.read_accessor(js, b, pr['attributes']['JOINTS_0'])).astype(int); Wt = np.asarray(L.read_accessor(js, b, pr['attributes']['WEIGHTS_0']))
names = [js['nodes'][j]['name'] for j in js['skins'][0]['joints']]; out = {}
for hand in ('RightHand', 'LeftHand'):
    hi = names.index(hand); sel = (np.where(J == hi, Wt, 0)).sum(1) > 0.5; node = js['skins'][0]['joints'][hi]
    Y = G[node][:3, 1] / np.linalg.norm(G[node][:3, 1]); out[hand] = round(float(((V[sel] - G[node][:3, 3]) @ Y).max()), 4)
out['height_m'] = round(float(V[:, 1].max() - V[:, 1].min()), 4)
json.dump(out, open(sys.argv[2], 'w'), indent=1); print('TIPS', out)
