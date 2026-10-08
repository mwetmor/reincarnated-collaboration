# R-C9-233 step 0: a UV-space CLASS texture for her body (one shell: face, hair and body in one mesh, one 2048 atlas), so a
# Godot probe can tell, per rendered pixel, FACE SKIN from FRONT HAIR from the rest of the HAIR from everything else.
#   R = face skin   non-hair, y 1.45-1.67 m, z > 0.03 m (the front of the head; the neck's front stops at the chin, 1.45)
#   G = front hair  hair (r140 island mask) with triangle-centroid z > 0.035 m -- R-C9-152's own "front hair" cut
#   B = other hair  the rest of the r140 hair mask (crown, back, braid)
# Rasterised per TRIANGLE (centroid class) into UV space at the atlas size. Also writes a hide mask (front hair only)
# and a vertex-count check against r140's mask (same topology as ss138a, only the morphs differ).
#   python3 r233_01_class_tex.py <body.glb> <hair_mask.npy> <out_class.png> [--preview sheet.png]
import sys, os, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
P, HM, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
js, b = L.load_glb(P); G, _ = W.globals_(js)
mi = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
V = W.skin_rest(js, b, mi, G)
pr = js['meshes'][js['nodes'][mi]['mesh']]['primitives'][0]
UV = L.read_accessor(js, b, pr['attributes']['TEXCOORD_0'])
IDX = L.read_accessor(js, b, pr['indices']).astype(int).reshape(-1, 3)
hair = np.load(HM)
assert len(hair) == len(V), (len(hair), len(V))
N = 2048
C = V[IDX].mean(1)
hv = hair[IDX].sum(1) >= 2
face = (~hv) & (C[:, 1] > 1.45) & (C[:, 1] < 1.67) & (C[:, 2] > 0.03)
front = hv & (C[:, 2] > 0.035)
other = hv & ~front
img = Image.new('RGB', (N, N), (0, 0, 0)); d = ImageDraw.Draw(img)
cnt = {}
for name, sel, col in (('other_hair', other, (0, 0, 255)), ('front_hair', front, (0, 255, 0)), ('face', face, (255, 0, 0))):
    cnt[name] = int(sel.sum())
    for t in np.nonzero(sel)[0]:
        uv = UV[IDX[t]] % 1.0
        d.polygon([(float(u * N), float(v * N)) for u, v in uv], fill=col)
img.save(OUT)
print('verts', len(V), 'tris', len(IDX), cnt)
if '--preview' in sys.argv:
    tex = Image.open(OUT).resize((1024, 1024), Image.NEAREST)
    tex.save(sys.argv[sys.argv.index('--preview') + 1])
