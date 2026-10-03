# MX audition: largest world joint difference (m) between two clips of one GLB at the first clip's keys (graft self-check).
#   python3 scripts/mx_cmp.py <glb> <clipA> <clipB>
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'en_e2', 'scripts')); C = __import__('s17_loop_closure')
m = C.model(sys.argv[1]); a, b = sys.argv[2], sys.argv[3]
T = sorted({float(t) for ch in m['anims'][a].values() for t in ch[0]}); w = 0
names = ['Hips', 'Head', 'LeftHand', 'RightHand', 'LeftFoot', 'RightFoot', 'LeftForeArm', 'RightForeArm', 'LeftLeg', 'RightLeg']
for t in T:
    A, B = C.globals_at(m, a, t), C.globals_at(m, b, t)
    w = max(w, max(float(np.linalg.norm(A[m['nid'][n]][:3, 3] - B[m['nid'][n]][:3, 3])) for n in names))
print('CMP %s vs %s: %d keys, largest joint difference %.4f m' % (a, b, len(T), w))
