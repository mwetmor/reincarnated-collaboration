# so_mx (R-C9-131): a LINT copy of a grafted body that also carries the ORIGINAL Meshy clips it replaced, renamed ref_<name>,
# so j_joint_lint can LEARN each hinge's natural direction from Meshy-native motion (--ref) while linting the Mixamo grafts.
# Both files must share the node array (the graft only appends animations). Not a ship file.
#   python3 so05_ref_clips.py <grafted.glb> <original.glb> <out.glb> idle,walk,run,hit,death
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); R_ = __import__('49_recentre'); W = __import__('52_weapon_bones')
G, O, OUT, CL = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(',')
js, b = L.load_glb(G); b = bytearray(b); jo, bo = L.load_glb(O)
assert [n.get('name') for n in js['nodes']] == [n.get('name') for n in jo['nodes']], "node arrays differ"
for an in jo['animations']:
    if an['name'] not in CL: continue
    sm = []
    for s in an['samplers']:
        ns = {}
        for k in ('input', 'output'):
            acc = jo['accessors'][s[k]]; arr = L.read_accessor(jo, bo, s[k]).astype(np.float32)
            data = arr.tobytes(); off = W.append(b, data)
            js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
            a = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": acc['count'], "type": acc['type']}
            if acc['type'] == 'SCALAR': a['min'] = [float(arr.min())]; a['max'] = [float(arr.max())]
            js['accessors'].append(a); ns[k] = len(js['accessors']) - 1
        ns['interpolation'] = s.get('interpolation', 'LINEAR'); sm.append(ns)
    js['animations'].append({"name": "ref_" + an['name'], "channels": [dict(c) for c in an['channels']], "samplers": sm})
js['buffers'][0]['byteLength'] = len(b); R_.write_glb(OUT, js, b)
print(OUT, [a['name'] for a in js['animations']])
