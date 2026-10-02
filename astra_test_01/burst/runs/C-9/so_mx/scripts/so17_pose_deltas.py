# so_mx R-C9-134: the WORLD delta (posed . rest^-1) of a bone at a clip time, read in pure glTF and handed to Blender
# (mount script so18) in Blender's world axes (x, -z, y). A prop is mounted at REST on its weapon bone; the pose it should
# look right in (the orb staff in the idle hand, the shield up in the block) is set through this delta.
#   python3 so17_pose_deltas.py <body.glb> <out.json> <name>=<bone>@<clip>@<t> ...
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
BODY, OUT = sys.argv[1], sys.argv[2]
m = C.model(BODY); G0, _ = W.globals_(L.load_glb(BODY)[0])
Cm = np.eye(4); Cm[:3, :3] = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]          # glTF -> Blender world
rep = {}
for spec in sys.argv[3:]:
    name, rest = spec.split('='); bone, clip, t = rest.split('@')
    G = C.globals_at(m, clip, float(t)); i = m['nid'][bone]
    D = G[i] @ np.linalg.inv(G0[i]); Db = Cm @ D @ np.linalg.inv(Cm)
    # her facing at that key (hips' +Z in glTF, flattened) in Blender axes
    h = m['nid']['Hips']; f = (G[h][:3, :3] @ np.linalg.inv(G0[h][:3, :3]) @ np.array([0, 0, 1.0])); f[1] = 0; f /= np.linalg.norm(f)
    rep[name] = dict(bone=bone, clip=clip, t=float(t), delta_world_blender=Db.tolist(), facing_blender=(Cm[:3, :3] @ f).tolist())
json.dump(rep, open(OUT, 'w'), indent=1); print(json.dumps({k: dict(facing=np.round(v['facing_blender'], 3).tolist()) for k, v in rep.items()}))
