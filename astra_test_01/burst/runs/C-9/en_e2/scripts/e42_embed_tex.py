# DEFECT FIX (found stage J, 2026-10-01): the shipped body GLB carried Tripo's FLAT texture -- the stage-D painted bake
# (work/tex_final.png) was used by every render script by override and NEVER written into the file. This replaces the body's
# base-colour image bytes with the painted texture (binary patch: a new bufferView, the image pointed at it).
#   python3 e42_embed_tex.py <in.glb> <out.glb> <tex.png>
import sys, os, io, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
from PIL import Image
IN, OUT, TEX = sys.argv[1:4]
js, b = L.load_glb(IN); bn = bytearray(b)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
mat = js['materials'][js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]['material']]
ti = mat['pbrMetallicRoughness']['baseColorTexture']['index']; ii = js['textures'][ti]['source']; im = js['images'][ii]
old = im.get('mimeType'); bio = io.BytesIO(); Image.open(TEX).convert('RGB').save(bio, 'JPEG', quality=92); data = bio.getvalue()
off = W.append(bn, data); js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
im['bufferView'] = len(js['bufferViews']) - 1; im['mimeType'] = 'image/jpeg'
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
js2, b2 = L.load_glb(OUT); bv = js2['bufferViews'][js2['images'][ii]['bufferView']]
a = np.asarray(Image.open(io.BytesIO(b2[bv['byteOffset']:bv['byteOffset'] + bv['byteLength']])).convert('RGB').resize((512, 512))).astype(float)
t = np.asarray(Image.open(TEX).convert('RGB').resize((512, 512))).astype(float)
print('embedded %s (%d KB, was %s); mean abs diff vs the painted texture %.2f' % (os.path.basename(TEX), len(data) // 1024, old, np.abs(a - t).mean()))
