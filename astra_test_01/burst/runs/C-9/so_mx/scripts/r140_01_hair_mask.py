# R-C9-140 (Matt): "when she wears the hood, the hair should be invisible." Find her HAIR on the body mesh (char1 is one shell:
# face, hair and body in one mesh and one 2048 atlas), by the atlas colour at each vertex's UV inside the head zone.
#   python3 r140_01_hair_mask.py <body.glb> <out.npz> [--png sheet.png]
import sys, os, io, json, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
P, OUT = sys.argv[1], sys.argv[2]
js, b = L.load_glb(P); G, _ = W.globals_(js)
mi = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
V = W.skin_rest(js, b, mi, G)
pr = js['meshes'][js['nodes'][mi]['mesh']]['primitives'][0]
UV = L.read_accessor(js, b, pr['attributes']['TEXCOORD_0'])
IDX = L.read_accessor(js, b, pr['indices']).astype(int).reshape(-1, 3)
im = js['images'][js['textures'][js['materials'][0]['pbrMetallicRoughness']['baseColorTexture']['index']]['source']]
bv = js['bufferViews'][im['bufferView']]
T = np.asarray(Image.open(io.BytesIO(b[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']])).convert('RGB')).astype(float) / 255
H_, W_ = T.shape[:2]
px = np.clip((UV[:, 0] % 1) * W_, 0, W_ - 1).astype(int); py = np.clip((UV[:, 1] % 1) * H_, 0, H_ - 1).astype(int)
# a 5x5 mean (the atlas is painted; a single texel is noisy)
acc = np.zeros((len(V), 3))
for dx in (-2, -1, 0, 1, 2):
    for dy in (-2, -1, 0, 1, 2):
        acc += T[np.clip(py + dy, 0, H_ - 1), np.clip(px + dx, 0, W_ - 1)]
rgb = acc / 25
import colorsys
hsv = np.array([colorsys.rgb_to_hsv(*c) for c in rgb])
np.savez(OUT, V=V, rgb=rgb, hsv=hsv, IDX=IDX)
print('verts', len(V), 'y>1.25:', int((V[:, 1] > 1.25).sum()))
