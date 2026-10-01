# T12 rank 3: THE AXE ARM'S GUARD, and the weapon channel -- binary glTF patches, no Blender.
#
#   python3 scripts/54_weapon_channel.py pose    <in.glb> <out.glb> <guard_pose.json> [--block <block_pose.json>] [--bash <bash_pose.json>] [--replace] [--json f]
#   python3 scripts/54_weapon_channel.py channel <in.glb> <out.glb> <weapon_r.json>   [--replace] [--json f]
#
# POSE adds two clips (three with --block):
#   axe_guard_R   the right arm's GUARD: RightShoulder, RightArm, RightForeArm, RightHand at the
#                 pose solved by attack_lab/tools/guard_pose_solve.py (IK in the chest frame: the
#                 grip in front at belly-to-chest height, the WRIST NEUTRAL so the haft stays in the
#                 fist's channel, the forearm square to it, the haft on the guard chosen for the
#                 play camera). Two keys, STEP, like shield_guard_L; the scene layers it over the
#                 locomotion, the strafes and the block at a swept weight.
#   axe_guard_R_block  (--block) the same, solved at the BLOCK's chest: the block turns his
#                 torso ~50 deg to present the shield, and a pose held relative to the chest
#                 turns the axe out of guard with it; the scene selects it by the block weight.
#   idle_guard    the new ARMED IDLE: the unarmed idle's stance -- its legs and hips HELD at one
#                 frame (the one whose chest faces his forward) -- with its spine, neck and head
#                 motion kept but DAMPED about that frame (its "breathing"), and the right arm at
#                 the guard. The unarmed idle is NOT quiet on its own: its hips turn up to 49 deg
#                 and its chest swings over 138 deg of yaw, looking round with the feet planted.
#                 It loops seamlessly (the unarmed idle's wrap is 0.0 deg), unlike idle_armed
#                 (Spine02 34.6 deg, LeftArm 78 deg at its wrap), which it replaces.
# CHANNEL adds a weapon_r rotation track to each named clip (the residual that finishes the guard,
#   and the strikes' edge-leading curves), solved in the lab on the clips as the scene blends them.
import json, math, os, struct, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
L = __import__('21_lint_export')
R_ = __import__('49_recentre')
W = __import__('52_weapon_bones')

LOWER = ["Hips", "LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase", "RightUpLeg", "RightLeg", "RightFoot", "RightToeBase"]
SPINE = ["Spine02", "Spine01", "Spine"]
HEADS = ["neck", "Head"]
RARM = ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]


def qmul(a, b):
    x1, y1, z1, w1 = a; x2, y2, z2, w2 = b
    return np.array([w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                     w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2])


def qinv(q):
    return np.array([-q[0], -q[1], -q[2], q[3]]) / float(np.dot(q, q))


def qpow(q, k):
    q = np.asarray(q, float)
    if q[3] < 0:
        q = -q
    ang = 2 * math.acos(max(-1.0, min(1.0, float(q[3]))))
    if ang < 1e-9:
        return np.array([0, 0, 0, 1.0])
    ax = q[:3] / np.linalg.norm(q[:3])
    return np.concatenate([ax * math.sin(ang * k / 2), [math.cos(ang * k / 2)]])


def qmean(qs):
    ref = qs[0]; acc = np.zeros(4)
    for q in qs:
        acc += q if np.dot(q, ref) >= 0 else -q
    return acc / np.linalg.norm(acc)


def add_accessor(js, bin_, arr, typ):
    arr = np.asarray(arr, np.float32)
    data = arr.tobytes()
    off = W.append(bin_, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    acc = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if typ == "SCALAR":
        acc["min"] = [float(arr.min())]; acc["max"] = [float(arr.max())]
    js['accessors'].append(acc)
    return len(js['accessors']) - 1


def channel(js, bin_, anim, node, path):
    for ch in anim['channels']:
        if ch['target'].get('node') == node and ch['target'].get('path') == path:
            s = anim['samplers'][ch['sampler']]
            return L.read_accessor(js, bytes(bin_), s['input']).reshape(-1), L.read_accessor(js, bytes(bin_), s['output']), s
    return None, None, None


def pose(src, dst, pose_json, outj, block_json=None, bash_json=None, replace=False):
    js, b0 = L.load_glb(src)
    bin_ = bytearray(b0)
    nodes = js['nodes']
    idx = {n.get('name'): i for i, n in enumerate(nodes)}
    POSE_CLIPS = ("axe_guard_R", "axe_guard_R_block", "axe_guard_R_bash", "idle_guard")
    if replace:
        # --replace: the guard poses re-solved (T12_8: on the corrected clips) -- the old ones go
        js['animations'] = [a for a in js['animations'] if a['name'] not in POSE_CLIPS]
    anims = {a['name']: a for a in js['animations']}
    assert "axe_guard_R" not in anims and "idle_guard" not in anims, "already patched (use --replace)"
    P = json.load(open(pose_json))
    gp = P["pose"]
    k0 = int(P["stance"]["key"])
    rep = {"stance_key": k0, "stance_t": P["stance"]["t"]}
    # ---- axe_guard_R: two keys, STEP --------------------------------------------------------
    t_in = add_accessor(js, bin_, np.array([0.0, 1.0 / 24.0]), "SCALAR")
    an = {"name": "axe_guard_R", "channels": [], "samplers": []}
    for nm in RARM:
        q = np.array(gp[nm], float)
        out = add_accessor(js, bin_, np.array([q, q]), "VEC4")
        an["samplers"].append({"input": t_in, "output": out, "interpolation": "STEP"})
        an["channels"].append({"sampler": len(an["samplers"]) - 1, "target": {"node": idx[nm], "path": "rotation"}})
    js['animations'].append(an)
    # ---- axe_guard_R_block: the same guard in HIS frame, solved against the BLOCK's chest (the
    # block turns his torso ~50 deg to present the shield, and a chest-relative pose turns with it)
    if block_json:
        gb = json.load(open(block_json))["pose"]
        an2 = {"name": "axe_guard_R_block", "channels": [], "samplers": []}
        for nm in RARM:
            q = np.array(gb[nm], float)
            out = add_accessor(js, bin_, np.array([q, q]), "VEC4")
            an2["samplers"].append({"input": t_in, "output": out, "interpolation": "STEP"})
            an2["channels"].append({"sampler": len(an2["samplers"]) - 1, "target": {"node": idx[nm], "path": "rotation"}})
        js['animations'].append(an2)
        rep["block_pose"] = True
    # ---- axe_guard_R_bash: the guard at the SHIELD BASH's chest (the bash is a strike whose swing is
    # the shield's; the axe arm holds this pose through it -- knight.gd strike_release.guard_throughout)
    if bash_json:
        gs = json.load(open(bash_json))["pose"]
        an3 = {"name": "axe_guard_R_bash", "channels": [], "samplers": []}
        for nm in RARM:
            q = np.array(gs[nm], float)
            out = add_accessor(js, bin_, np.array([q, q]), "VEC4")
            an3["samplers"].append({"input": t_in, "output": out, "interpolation": "STEP"})
            an3["channels"].append({"sampler": len(an3["samplers"]) - 1, "target": {"node": idx[nm], "path": "rotation"}})
        js['animations'].append(an3)
        rep["bash_pose"] = True
    # ---- --extra name=pose.json (repeatable): any further pose clip of the same form (lab candidates)
    for k_, v_ in enumerate(sys.argv):
        if v_ == '--extra':
            nm_x, pj = sys.argv[k_ + 1].split('=', 1)
            gx = json.load(open(pj))["pose"]
            js['animations'] = [a_ for a_ in js['animations'] if a_['name'] != nm_x]
            anx = {"name": nm_x, "channels": [], "samplers": []}
            for nm in RARM:
                q = np.array(gx[nm], float)
                out = add_accessor(js, bin_, np.array([q, q]), "VEC4")
                anx["samplers"].append({"input": t_in, "output": out, "interpolation": "STEP"})
                anx["channels"].append({"sampler": len(anx["samplers"]) - 1, "target": {"node": idx[nm], "path": "rotation"}})
            js['animations'].append(anx)
            rep.setdefault("extra", []).append(nm_x)
    # ---- idle_guard ---------------------------------------------------------------------------
    idle = anims['idle']
    times, _, _ = channel(js, bin_, idle, idx["Hips"], 'rotation')
    n = len(times)
    t_idle = add_accessor(js, bin_, times, "SCALAR")
    ig = {"name": "idle_guard", "channels": [], "samplers": []}

    def put(node, path, vals, typ):
        o = add_accessor(js, bin_, vals, typ)
        ig["samplers"].append({"input": t_idle, "output": o, "interpolation": "LINEAR"})
        ig["channels"].append({"sampler": len(ig["samplers"]) - 1, "target": {"node": node, "path": path}})

    KSPINE = float(P.get("damp_spine", 0.25))
    KHEAD = float(P.get("damp_head", 0.30))
    touched = set()
    for ch in idle['channels']:
        node, path = ch['target']['node'], ch['target']['path']
        nm = nodes[node].get('name')
        s = idle['samplers'][ch['sampler']]
        tt = L.read_accessor(js, bytes(bin_), s['input']).reshape(-1)
        vv = L.read_accessor(js, bytes(bin_), s['output'])
        if len(tt) != n or path == "scale":
            # a channel on its own clock (the Hips scale the export left as a constant): carried as-is
            ig["samplers"].append({"input": s['input'], "output": s['output'], "interpolation": s.get('interpolation', 'LINEAR')})
            ig["channels"].append({"sampler": len(ig["samplers"]) - 1, "target": {"node": node, "path": path}})
            touched.add((nm, path))
            continue
        if nm in RARM and path == "rotation":
            q = np.array(gp[nm], float)
            put(node, path, np.tile(q, (n, 1)), "VEC4")
        elif nm in LOWER or nm not in (SPINE + HEADS):
            # held at the stance frame: the legs, the hips (rotation and translation), and every
            # bone not otherwise named (the left arm -- the shield layer owns it -- and the leaves)
            put(node, path, np.tile(vv[k0], (n, 1)), "VEC4" if path == "rotation" else "VEC3")
        else:
            # the breathing: the clip's own motion about its MEAN, damped, carried by the stance frame
            k = KSPINE if nm in SPINE else KHEAD
            if path == "rotation":
                qm = qmean([np.asarray(q, float) for q in vv])
                out = [qmul(vv[k0], qpow(qmul(qinv(qm), np.asarray(q, float)), k)) for q in vv]
                put(node, path, np.array(out), "VEC4")
            else:
                put(node, path, np.tile(vv[k0], (n, 1)), "VEC3")
        touched.add((nm, path))
    for nm in RARM:
        if (nm, "rotation") not in touched:
            put(idx[nm], "rotation", np.tile(np.array(gp[nm], float), (n, 1)), "VEC4")
    js['animations'].append(ig)
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    R_.write_glb(dst, js, bin_)
    res = L.lint(dst)
    rep.update(clips_added=["axe_guard_R", "idle_guard"] + (["axe_guard_R_block"] if block_json else []) + (["axe_guard_R_bash"] if bash_json else []),
               replaced=bool(replace), idle_keys=n, damp_spine=KSPINE, damp_head=KHEAD,
               lint=dict(verdict=res["verdict"], fails=res["fails"], warns=len(res["warns"])))
    print("pose: axe_guard_R (%d bones, 2 keys, STEP) and idle_guard (%d keys; stance key %d; spine x%.2f, head x%.2f) -> %s; lint %s, %d fails"
          % (len(RARM), n, k0, KSPINE, KHEAD, os.path.basename(dst), res["verdict"], len(res["fails"])))
    for f in res["fails"]:
        print("  FAIL " + f)
    if outj:
        json.dump(rep, open(outj, "w"), indent=1)
    assert not res["fails"]


def chan(src, dst, wr_json, outj, replace=False):
    js, b0 = L.load_glb(src)
    bin_ = bytearray(b0)
    nodes = js['nodes']
    idx = {n.get('name'): i for i, n in enumerate(nodes)}
    anims = {a['name']: a for a in js['animations']}
    wr = json.load(open(wr_json))["weapon_r"]
    wn = idx["weapon_r"]
    rep = {}
    for clip, d in wr.items():
        an = anims[clip]
        if replace:
            # --replace (T12_8: the residuals re-solved on the corrected clips): the old track goes;
            # its sampler stays behind unreferenced, which glTF allows
            an['channels'] = [ch for ch in an['channels'] if ch['target'].get('node') != wn]
        assert not any(ch['target'].get('node') == wn for ch in an['channels']), "%s already has a weapon_r track (use --replace)" % clip
        t = add_accessor(js, bin_, np.array(d["times"], float), "SCALAR")
        q = np.array(d["quats"], float)
        q /= np.linalg.norm(q, axis=1, keepdims=True)
        for i in range(1, len(q)):
            if np.dot(q[i], q[i - 1]) < 0:
                q[i] = -q[i]
        o = add_accessor(js, bin_, q, "VEC4")
        an['samplers'].append({"input": t, "output": o, "interpolation": "LINEAR"})
        an['channels'].append({"sampler": len(an['samplers']) - 1, "target": {"node": wn, "path": "rotation"}})
        rep[clip] = len(q)
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    R_.write_glb(dst, js, bin_)
    res = L.lint(dst)
    print("channel: weapon_r tracks on %d clips %s -> %s; lint %s, %d fails"
          % (len(rep), sorted(rep), os.path.basename(dst), res["verdict"], len(res["fails"])))
    for f in res["fails"]:
        print("  FAIL " + f)
    if outj:
        json.dump(dict(tracks=rep, lint=dict(verdict=res["verdict"], fails=res["fails"], warns=len(res["warns"]))), open(outj, "w"), indent=1)
    assert not res["fails"]


if __name__ == "__main__":
    a = sys.argv[1:]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    if a[0] == "pose":
        pose(a[1], a[2], a[3], outj, a[a.index('--block') + 1] if '--block' in a else None,
             a[a.index('--bash') + 1] if '--bash' in a else None, '--replace' in a)
    elif a[0] == "channel":
        chan(a[1], a[2], a[3], outj, '--replace' in a)
    else:
        sys.exit("usage: pose|channel ...")
