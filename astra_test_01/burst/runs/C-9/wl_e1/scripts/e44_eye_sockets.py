# EYE SOCKETS for camera-facing glow sprites (stage J, conductor: the brow hides the slit from the 53-deg camera). The two eye
# points are found from the helm's own EMISSION texture: helm vertices whose UV samples the emission mask (> 0.5) in the upper
# half of the slit; split left/right of the helm's centre line; each centroid pushed FORWARD (his +Z) by --ahead m. Written in
# the Head bone's REST-LOCAL frame (what a runtime BoneAttachment3D on 'Head' takes) and in model space.
#   python3 e44_eye_sockets.py <helm.glb> <emission.png> <out.json> [--ahead 0.02] [--size 0.05]
import sys, os, json, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; HELM, EMP, OUT = a[:3]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
AHEAD = float(opt('--ahead', '0.02')); SIZE = float(opt('--size', '0.05'))
js, b = L.load_glb(HELM); G, _ = W.globals_(js); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
V = W.skin_rest(js, b, mn, G); pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
uv = L.read_accessor(js, b, pr['attributes']['TEXCOORD_0'])
em = np.asarray(Image.open(EMP).convert('L')).astype(float) / 255.0; H_, W_ = em.shape
e = em[np.clip((uv[:, 1] * H_).astype(int), 0, H_ - 1), np.clip((uv[:, 0] * W_).astype(int), 0, W_ - 1)]
P = V[e > 0.5]; top = P[:, 1] > np.percentile(P[:, 1], 55); P = P[top]; cx = float(np.median(V[:, 0]))
rootn = [i for i in range(len(js['nodes'])) if all(i not in nd.get('children', []) for nd in js['nodes'])][0]
K = float(np.cbrt(np.linalg.det(G[rootn][:3, :3])))          # the root's scale (1.96 export: 0.01 x 1.153)
hi = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}['Head']; Hinv = np.linalg.inv(G[hi])
eyes = {}
for side, sel in (('eye_L', P[:, 0] > cx), ('eye_R', P[:, 0] < cx)):
    c = P[sel].mean(0)
    # v2: IN FRONT OF THE VISOR SURFACE, not of the slit's own vertices -- v1 put the sockets 1.4-1.9 cm INSIDE the helm (the slit
    # is recessed), so depth-tested sprites never showed. z = the helm's frontmost surface within 2 cm (x) / 1 cm (y) + AHEAD.
    nb = (np.abs(V[:, 0] - c[0]) < 0.02) & (np.abs(V[:, 1] - c[1]) < 0.01)
    c[2] = float(V[nb, 2].max()) + AHEAD                      # model space (metres), his forward +Z
    eyes[side] = dict(model_m=np.round(c, 4).tolist(), head_local=np.round((Hinv @ np.append(c, 1.0))[:3], 5).tolist(), verts=int(sel.sum()))
rep = dict(bone='Head', ahead_m=AHEAD, sprite_size_m=SIZE, eyes=eyes, separation_m=round(float(np.linalg.norm(np.array(eyes['eye_L']['model_m']) - np.array(eyes['eye_R']['model_m']))), 4),
           note='camera-facing (billboard), unshaded, ADDITIVE, depth-tested (the helm hides them from behind); hot near-white core; slow subtle flicker')
json.dump(rep, open(OUT, 'w'), indent=1); print(json.dumps(rep))
