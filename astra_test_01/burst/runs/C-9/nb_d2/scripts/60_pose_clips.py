# POSE CLIPS: a held pose as a clip -- two keys, STEP, one rotation track per bone the pose names.
#
#   python3 scripts/60_pose_clips.py <in.glb> <out.glb> <clip>=<pose.json> ... [--json f]
#
# The pose JSON is guard_pose_solve.py's ({"pose": {bone: [x, y, z, w]}}), any bones: the JOIN-1 hold is
# two of these (join_guard_R: RightShoulder..RightHand; join_guard_L: LeftShoulder..LeftHand), layered
# by the renderer over idle/walk/run as filtered Blend2s (join_hold.json). The shape 54_weapon_channel.py
# gives axe_guard_R and shield_guard_L, so knight.gd and the JOIN renderer read it the same way. A clip of
# the same name is replaced; every other byte of the file is kept (a binary patch).
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
R_ = __import__('49_recentre')


def main():
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    specs = [x for x in a[2:] if '=' in x and not x.startswith('--')]
    js, b0 = L.load_glb(src)
    bin_ = bytearray(b0)
    nid = {n.get('name'): i for i, n in enumerate(js['nodes'])}

    def acc(arr, typ):
        arr = np.asarray(arr, np.float32)
        data = arr.tobytes()
        off = W.append(bin_, data)
        js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
        a_ = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
        if typ == "SCALAR":
            a_["min"] = [float(arr.min())]; a_["max"] = [float(arr.max())]
        js['accessors'].append(a_)
        return len(js['accessors']) - 1
    rep = {}
    t_in = acc(np.array([0.0, 1.0 / 24.0]), "SCALAR")
    for spec in specs:
        name, pj = spec.split('=', 1)
        pose = json.load(open(pj))["pose"]
        an = {"name": name, "channels": [], "samplers": []}
        for bone, q in pose.items():
            q = np.array(q, float); q /= np.linalg.norm(q)
            an["samplers"].append({"input": t_in, "output": acc(np.array([q, q]), "VEC4"), "interpolation": "STEP"})
            an["channels"].append({"sampler": len(an["samplers"]) - 1, "target": {"node": nid[bone], "path": "rotation"}})
        js['animations'] = [x for x in js['animations'] if x.get('name') != name]
        js['animations'].append(an)
        rep[name] = dict(pose=os.path.basename(pj), bones=list(pose.keys()))
        print("pose clip %-14s %d bones (2 keys, STEP) from %s" % (name, len(pose), os.path.basename(pj)))
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    R_.write_glb(dst, js, bin_)
    res = L.lint(dst)
    print("lint %s, %d fails %s" % (res['verdict'], len(res['fails']), res['fails'][:2]))
    if outj:
        json.dump(dict(clips=rep, lint=dict(verdict=res['verdict'], fails=res['fails'])), open(outj, 'w'), indent=1)


if __name__ == '__main__':
    main()
