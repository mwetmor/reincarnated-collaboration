"""Where each clip puts the hips relative to the RIG ORIGIN -- the point the scene's body
stands on. My earlier root_path.py measured each clip against ITS OWN first frame, which
cannot see a clip that is displaced as a whole."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gltf_anim import clips, load
M = 0.0108823
for path in sys.argv[1:]:
    js, _ = load(path)
    C = clips(path)
    # the rest translation of Hips, for reference
    hips_node = next(n for n in js['nodes'] if n.get('name') == 'Hips')
    rest = np.array(hips_node.get('translation', [0, 0, 0]))
    print("%s   Hips REST translation %s units" % (path.rsplit('/', 1)[-1], np.round(rest, 2)))
    for name in sorted(C):
        ch = C[name].get('Hips', {}).get('translation')
        if ch is None:
            continue
        t, v, _ = ch
        up = 1 if abs(rest[1]) >= max(abs(rest[0]), abs(rest[2])) else int(np.argmax(np.abs(v.mean(axis=0))))
        hz = [i for i in range(3) if i != up]
        h = v[:, hz] * M
        d = np.linalg.norm(h, axis=1)
        print("  %-30s start %.3f m  end %.3f m  from origin: min %.3f  max %.3f  mean %.3f" % (
            name, d[0], d[-1], d.min(), d.max(), d.mean()))
