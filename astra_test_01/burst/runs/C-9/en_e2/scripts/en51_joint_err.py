# EN-E2: joint-position error of a transferred rig against a reference rig on the same skeleton (inverse bind origins, mesh units).
#   python3 scripts/en51_joint_err.py <reference.glb> <test.glb>
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
def jpos(p):
    js, b = L.load_glb(p); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n); sk = js['skins'][js['nodes'][mn]['skin']]
    I = W.mat_list(js, b, sk['inverseBindMatrices']); return {js['nodes'][j]['name']: np.linalg.inv(I[k])[:3, 3] for k, j in enumerate(sk['joints'])}
A, B = jpos(sys.argv[1]), jpos(sys.argv[2]); e = {n: float(np.linalg.norm(A[n] - B[n])) for n in A}
print('JOINT_ERR mean %.4f max %.4f (%s)' % (np.mean(list(e.values())), max(e.values()), max(e, key=e.get)))
