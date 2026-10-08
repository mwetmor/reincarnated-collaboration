# R-C9-237 step 2: the hood's INNER surfaces (r233_05's linings + r233_08's scalp: primitives 2..N of the hood mesh) moved
# into their OWN mesh on their OWN node, "hood_lining", skinned with the same skin, wearing a copy of the hood's material
# named "hood_lining". Why: the game binds every MeshInstance3D of a gear GLB as that piece (gear.gd), and gives each its
# own ramp material (PaintStack.adopt_character) -- so the live code can put the web pen's THIN class on the lining alone
# (by the node's name) while the hood's shell keeps its full outline. Geometry, UVs, joints and weights are byte-for-byte
# the same accessors; nothing else in the file changes.
#   python3 r237_02_split_lining.py <hood_in.glb> <hood_out.glb> [--first 2]
import sys, os, json, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); R_ = __import__('49_recentre')
IN, OUT = sys.argv[1], sys.argv[2]
FIRST = int(sys.argv[sys.argv.index('--first') + 1]) if '--first' in sys.argv else 2
js, b = L.load_glb(IN)
ni = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
nd = js['nodes'][ni]; mesh = js['meshes'][nd['mesh']]
prims = mesh['primitives']
assert len(prims) > FIRST, len(prims)
inner = prims[FIRST:]; mesh['primitives'] = prims[:FIRST]
mat = copy.deepcopy(js['materials'][inner[0].get('material', 0)]); mat['name'] = 'hood_lining'
js['materials'].append(mat); mi = len(js['materials']) - 1
for p in inner:
    p['material'] = mi
js['meshes'].append({"name": "hood_lining", "primitives": inner})
new = {"name": "hood_lining", "mesh": len(js['meshes']) - 1, "skin": nd['skin']}
for k in ('translation', 'rotation', 'scale', 'matrix'):
    if k in nd:
        new[k] = copy.deepcopy(nd[k])
js['nodes'].append(new); nn = len(js['nodes']) - 1
parent = next((i for i, n in enumerate(js['nodes']) if ni in n.get('children', [])), None)
if parent is not None:
    js['nodes'][parent]['children'].append(nn)
else:
    for sc in js['scenes']:
        if ni in sc['nodes']:
            sc['nodes'].append(nn)
R_.write_glb(OUT, js, b)
print(json.dumps({"in": IN, "out": OUT, "shell_prims": FIRST, "lining_prims": len(inner), "lining_node": nn,
                  "parent": parent, "material": "hood_lining"}))
