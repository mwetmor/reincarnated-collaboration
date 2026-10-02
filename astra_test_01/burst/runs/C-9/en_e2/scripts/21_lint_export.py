# Export lint for character GLBs. STANDING CHECK -- run on every character
# export from now on.
#
#   python3 scripts/21_lint_export.py <a.glb> [<b.glb> ...] [--json out.json]
#
# Reads the SHIPPED FILE, not Blender's interpretation of it. That distinction
# is the point: the 1.176 Hips scale that made the barbarian's idle 17.6%
# bigger than his walk was present and correct in Blender -- it was Meshy's
# library clip carrying a height retarget for its own 1.70 m rig -- and nothing
# on the authoring side was going to call it wrong. Only a check that asks
# "what does this file tell a consumer to do" catches it.
#
# RULES
#   FAIL  any joint scale track that leaves 1.0 by more than 1e-3, in any clip.
#         A skeleton-root scale track multiplies the whole character; that is
#         never animation, it is always a retarget artefact.
#   WARN  a clip whose first-frame root height differs from the node's rest
#         translation by more than 5%. Legitimate for a crouch or a jump start,
#         so it warns rather than fails -- but it is how a re-grounded clip
#         announces itself.
#   WARN  net root HORIZONTAL travel over 0.05 m in a non-locomotion clip.
#   FAIL  a clip whose root NEVER comes within 0.25 m of its rest position,
#         horizontally. Added 2026-09-29 (attack_lab): the travel rule asks whether
#         a clip MOVES, first frame to last, and a de-rooted clip does not move -- it
#         just stands somewhere else. idle_armed stood 1.10 m off, run_armed 1.83 m,
#         attack_chop 0.49 m, and every blend in or out of them dragged the figure
#         across the ground by the difference. A lunge STARTS at the rest position, so
#         "never within" separates the two: the three displaced clips never come nearer
#         than 0.367 m, and every other clip passes within 0.069 m.
#         Added after the scene found idle_armed drifting 0.8994 m over its own
#         loop and attack_chop 0.7519 m -- root motion in clips nobody thought
#         had any, in a file this lint had already passed. It checked root
#         HEIGHT and never once looked sideways.
#   WARN  a clip whose root-height BAND does not overlap any other clip's band.
#         Added after the fact, because the rule above does not discriminate:
#         on the broken file it fired on attack, idle and run, and only one of
#         the three was a defect -- a check that flags the innocent alongside
#         the guilty has not told you anything. The band rule fires on exactly
#         one clip of the broken file (idle, 99.7-103.1, overlapping nothing)
#         and on none of the fixed file. A crouch or a lunge still SHARES
#         ground with the other clips; a retargeted one does not.
#   FAIL  SKELETON IDENTITY (T12 rank 1, 2026-09-29): every skinned file carries the BASE RIG
#         -- Meshy's 24 joints then weapon_r and weapon_l, in exactly BASE_RIG's order -- with
#         weapon_r a child of RightHand and weapon_l of LeftHand. gear.gd binds a piece only
#         when its bone list equals the body's, order included, and a re-export that drops or
#         reorders the weapon bones would otherwise pass silently and lose the weapon channel.
#         Fix: scripts/52_weapon_bones.py (the export chain runs it after every export).
#         Off only for RAW library fetches (31_meshy_fetch lints Meshy's own 24-joint rig).
#   FAIL  WEAPON REST: weapon_r / weapon_l's rest (local to the hand) must equal the recorded mount
#         (work/weapon_mount.json, written by 52_weapon_bones.py --record) within 1 um -- or be
#         coincident with the hand when no mount is recorded. A piece bound to the weapon bone in
#         one file and drawn on the body's weapon bone from another only lines up if they agree.
#   FAIL  SOURCE FIDELITY (T12, N-C9-ASSEMBLE-DISTORTION, 2026-09-30): every clip the provenance
#         registry (work/clip_sources.json) gives a GLB source must still move like it -- within
#         0.10 of the rest hips-to-head at EVERY frame, joints in the hips' physical frame
#         (56_clip_fidelity.py), after its named edits -- and that source must be on THIS body's
#         rig (rest pose within 0.01). Found: every armed clip D2 shipped was fetched for the
#         other T8 candidate's skeleton and pose-copied onto this one by 33_assemble's Blender
#         merge; they were 0.15-0.26 off, their hips turning up to 104 deg away from the source's.
#         WARN for a `legacy` clip (unused, slated for removal). Only when the file carries clips
#         the registry names, so a raw library fetch or another character's file is not judged by it.
#   FAIL  SOURCE GRID / LOOP SEAM (N-C9 loop check, 2026-09-30): every registry clip marked "loop"
#         keys on its source's OWN key times (no resampling) and closes -- pose(0) against pose(T)
#         within 5 mm and 1 deg (56_clip_fidelity.seams; s17_loop_closure.py's definition). Found:
#         the T8 walk popped 9.96 cm / 11.3 deg at every wrap and the run hitched (its first interval
#         29% of normal) -- the D2 merge had cut Meshy's 30 fps keys on a 24 fps grid from t = 0. No
#         exceptions (coordinator 2026-09-30): a loop whose source grid cannot be read FAILS, and a source
#         that is not periodic (text-to-motion) is BLENDED on its own keys (58_loop_blend.py), not excused.
import json, struct, sys
import numpy as np

BASE_RIG = ("Hips", "LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase", "RightUpLeg", "RightLeg",
            "RightFoot", "RightToeBase", "Spine02", "Spine01", "Spine", "LeftShoulder", "LeftArm",
            "LeftForeArm", "LeftHand", "weapon_l", "neck", "Head", "head_end", "headfront",
            "RightShoulder", "RightArm", "RightForeArm", "RightHand", "weapon_r")
# weapon_l right after LeftHand and weapon_r after RightHand: Blender's exporter writes joints
# depth-first, so this is the only order that survives a Blender round trip
WEAPON_REST_TOL_M = 1e-6
WEAPON_PARENT = (("weapon_r", "RightHand"), ("weapon_l", "LeftHand"))

SCALE_TOL, ROOT_TOL = 1e-3, 0.05
ROOT_TRAVEL_TOL = 0.05          # metres of horizontal drift allowed off-locomotion
ROOT_OFFSET_TOL = 0.25          # a clip whose root never comes this near its rest spot
CT = {5120: ('b', 1), 5121: ('B', 1), 5122: ('h', 2), 5123: ('H', 2),
      5125: ('I', 4), 5126: ('f', 4)}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def load_glb(path):
    raw = open(path, 'rb').read()
    assert raw[:4] == b'glTF', "%s is not a GLB" % path
    off, js, bin_ = 12, None, b''
    while off < len(raw):
        ln, ty = struct.unpack_from('<II', raw, off)
        blob = raw[off + 8:off + 8 + ln]
        if ty == 0x4E4F534A:
            js = json.loads(blob)
        elif ty == 0x004E4942:
            bin_ = blob
        off += 8 + ln + (-ln % 4)
    return js, bin_


def read_accessor(g, bin_, idx):
    """Decode one accessor, honouring byteStride. A tightly packed reshape is
    right for most exports and silently wrong for interleaved ones."""
    acc = g['accessors'][idx]
    n, ncomp = acc['count'], NC[acc['type']]
    fmt, sz = CT[acc['componentType']]
    if 'bufferView' not in acc:
        return np.zeros((n, ncomp), dtype=np.float64)
    bv = g['bufferViews'][acc['bufferView']]
    base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    stride = bv.get('byteStride') or ncomp * sz
    out = np.empty((n, ncomp), dtype=np.float64)
    for i in range(n):
        out[i] = struct.unpack_from('<%d%s' % (ncomp, fmt), bin_, base + i * stride)
    return out


def _q2m(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def _trs(nd):
    if 'matrix' in nd:
        return np.array(nd['matrix'], float).reshape(4, 4).T
    M = np.eye(4)
    M[:3, :3] = _q2m(nd.get('rotation', [0, 0, 0, 1])) @ np.diag(nd.get('scale', [1, 1, 1]))
    M[:3, 3] = nd.get('translation', [0, 0, 0])
    return M


def _mount(path=None):
    """The recorded mount: a weapon_mount.json BESIDE the file (a staged set carries its own), else
    the pipeline's work/weapon_mount.json, else none (the weapon bones must be coincident)."""
    import os
    for p in ([os.path.join(os.path.dirname(os.path.abspath(path)), "weapon_mount.json")] if path else []) + \
            [os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "weapon_mount.json")]:
        if os.path.exists(p):
            rec = json.load(open(p))
            # W: weapon_r's rest (the T12 seat); WL (JOIN-1, 59_offhand_mount.py): weapon_l's, when an off-hand
            # weapon is mounted -- otherwise weapon_l stays coincident with its hand
            return {"weapon_r": np.array(rec["W"], float), "weapon_l": np.array(rec["WL"], float) if "WL" in rec else None}
    return None


def lint(path, skeleton=True):
    g, bin_ = load_glb(path)
    nodes = g.get('nodes', [])
    name = lambda i: nodes[i].get('name', 'node%d' % i)
    # up axis: glTF is Y-up by convention, and both exporters here honour it.
    UP = 1
    # every node's rest translation, and who its children are
    rest = {i: np.array(nd.get('translation', [0, 0, 0]), dtype=np.float64)
            for i, nd in enumerate(nodes)}
    parent = {}
    for i, nd in enumerate(nodes):
        for c in nd.get('children', []):
            parent[c] = i
    # the skeleton root: a joint of some skin with no joint parent
    joints = set()
    for sk in g.get('skins', []):
        joints.update(sk.get('joints', []))
    roots = [j for j in joints if parent.get(j) not in joints]
    # metres per glTF unit: the product of the scales on the root joint's
    # ancestors. READ, never assumed -- this rig's is 0.010882 (Meshy's 0.01
    # object scale times the T8 fit to a 1.85 m body), and a hard-coded 0.01
    # would understate every drift by 8.8%.
    MPU = 1.0
    if roots:
        _k = parent.get(roots[0])
        while _k is not None:
            MPU *= float(nodes[_k].get('scale', [1, 1, 1])[1])
            _k = parent.get(_k)
    fails, warns, clips = [], [], {}
    if skeleton:
        for sk in g.get('skins', []):
            jn = tuple(name(j) for j in sk.get('joints', []))
            if jn != BASE_RIG:
                miss = [n for n in BASE_RIG if n not in jn]
                extra = [n for n in jn if n not in BASE_RIG]
                fails.append(
                    "%s: SKELETON IDENTITY -- %d joints%s%s%s; the base rig is %d in a fixed order. "
                    "gear.gd will not bind a piece whose bone list differs from the body's: run "
                    "scripts/52_weapon_bones.py" % (path.split('/')[-1], len(jn),
                    (", missing %s" % miss) if miss else "", (", extra %s" % extra) if extra else "",
                    ", order differs" if not miss and not extra else "", len(BASE_RIG)))
        mount = _mount(path)
        for wn, hn in WEAPON_PARENT:
            wi = [i for i, nd in enumerate(nodes) if nd.get('name') == wn]
            if wi and (parent.get(wi[0]) is None or name(parent[wi[0]]) != hn):
                fails.append("%s: SKELETON IDENTITY -- %s is not a child of %s"
                             % (path.split('/')[-1], wn, hn))
            if wi:
                mounted = mount is not None and mount.get(wn) is not None
                want = mount[wn] if mounted else np.eye(4)
                got = _trs(nodes[wi[0]])
                # compare where the rest frame puts points 10 cm out along each axis (metres)
                probe = np.array([[0, 0, 0, 1], [10, 0, 0, 1], [0, 10, 0, 1], [0, 0, 10, 1]], float).T
                dev = float(np.abs((got - want) @ probe).max()) * MPU
                if dev > WEAPON_REST_TOL_M:
                    fails.append("%s: WEAPON REST -- %s's rest is %.3g m from the %s (tolerance 1 um)"
                                 % (path.split('/')[-1], wn, dev, "recorded mount" if mounted else "hand (coincident)"))
    for an in g.get('animations', []):
        cn = an.get('name', '?')
        rec = dict(scale_tracks={}, root_height=None, root=None)
        for ch in an.get('channels', []):
            tgt = ch.get('target', {})
            nidx, pth = tgt.get('node'), tgt.get('path')
            if nidx is None or pth not in ('scale', 'translation'):
                continue
            smp = an['samplers'][ch['sampler']]
            vals = read_accessor(g, bin_, smp['output'])
            if pth == 'scale' and nidx in joints:
                dev = float(np.abs(vals - 1.0).max())
                if dev > SCALE_TOL:
                    rec['scale_tracks'][name(nidx)] = dict(
                        max_deviation=round(dev, 6),
                        value=[round(float(v), 6) for v in vals[0]],
                        constant=bool(np.abs(vals - vals[0]).max() < 1e-6))
                    fails.append(
                        "%s: clip '%s' scales joint '%s' by %s (deviation %.4f "
                        "> %.0e)" % (path.split('/')[-1], cn, name(nidx),
                                     np.round(vals[0], 4).tolist(), dev, SCALE_TOL))
            if pth == 'translation' and nidx in roots:
                # horizontal drift: glTF is Y-up, so X and Z are the ground plane
                net = float(np.hypot(vals[-1][0] - vals[0][0],
                                     vals[-1][2] - vals[0][2]))
                rec['root_travel_units'] = round(net, 3)
                is_loco = any(k in cn.lower() for k in
                              ('walk', 'run', 'strafe', 'sprint', 'jog', 'dodge'))
                rec['locomotion'] = is_loco
                if not is_loco and net * MPU > ROOT_TRAVEL_TOL:
                    warns.append(
                        "%s: clip '%s' drifts %.3f m horizontally over its own "
                        "length (%.1f units) and is not locomotion -- a clip that "
                        "walks away from where it started"
                        % (path.split('/')[-1], cn, net * MPU, net))
                # WHERE the clip stands, not only whether it moves
                hz = np.hypot(vals[:, 0] - rest[nidx][0], vals[:, 2] - rest[nidx][2]) * MPU
                rec['root_offset_m'] = dict(closest=round(float(hz.min()), 4),
                                            mean=round(float(hz.mean()), 4),
                                            first=round(float(hz[0]), 4))
                if float(hz.min()) > ROOT_OFFSET_TOL:
                    fails.append(
                        "%s: clip '%s' stands %.3f m from the rest position and never "
                        "comes nearer than %.3f m -- a consumer stands the body at the "
                        "origin, so this clip is drawn away from its own capsule and every "
                        "blend in or out of it drags the figure across the ground"
                        % (path.split('/')[-1], cn, float(hz.mean()), float(hz.min())))
                rec['root'] = name(nidx)
                rec['root_height'] = dict(
                    first=round(float(vals[0][UP]), 4),
                    min=round(float(vals[:, UP].min()), 4),
                    max=round(float(vals[:, UP].max()), 4),
                    rest=round(float(rest[nidx][UP]), 4))
                r = float(rest[nidx][UP])
                if abs(r) > 1e-9:
                    d = abs(float(vals[0][UP]) - r) / abs(r)
                    if d > ROOT_TOL:
                        warns.append(
                            "%s: clip '%s' starts root '%s' at %.3f against rest "
                            "%.3f (%.1f%% > %.0f%%)" % (path.split('/')[-1], cn,
                            name(nidx), vals[0][UP], r, d * 100, ROOT_TOL * 100))
        clips[cn] = rec
    # cross-clip: a clip whose root-height band is disjoint from every other
    bands = {c: (v['root_height']['min'], v['root_height']['max'])
             for c, v in clips.items() if v['root_height']}
    for c, (lo, hi) in bands.items():
        if len(bands) < 3 or (hi - lo) < 1e-9:
            continue
        if not any(o != c and not (hi < blo or bhi < lo)
                   for o, (blo, bhi) in bands.items()):
            warns.append(
                "%s: clip '%s' root height %.1f-%.1f overlaps NO other clip "
                "(%s) -- the clip is not standing on the same ground as the "
                "rest of the set" % (path.split('/')[-1], c, lo, hi,
                ", ".join("%s %.1f-%.1f" % (o, b[0], b[1])
                          for o, b in sorted(bands.items()) if o != c)))
    # SOURCE FIDELITY -- the provenance registry's clips, against their library sources
    if skeleton:
        try:
            import importlib, os as _os
            sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
            F = importlib.import_module("56_clip_fidelity")
            reg = F.registry()
            if any(c in clips for c in reg.get("clips", {})):
                for r in F.check(path, reg):
                    st = r.get("status")
                    if st == "FAIL":
                        fails.append("%s: SOURCE FIDELITY -- clip '%s' is %.3f hips-to-head from %s at %.2f s (%s); limit %.2f%s"
                                     % (path.split('/')[-1], r['clip'], r['err_max'], r['source'], r['worst_t'], r['worst_joint'],
                                        F.LIMIT, "; its hips turn %.0f deg off the source's" % r['hips_deg_max'] if r['hips_deg_max'] > 1 else ""))
                    elif st == "RIG":
                        fails.append("%s: SOURCE FIDELITY -- clip '%s''s source %s was fetched for ANOTHER RIG (rest pose %.3f hips-to-head "
                                     "from this body's): re-fetch it on this body's rig" % (path.split('/')[-1], r['clip'], r['source'], r['rest_match']))
                    elif st == "LEGACY":
                        warns.append("%s: SOURCE FIDELITY -- clip '%s' is legacy (%s)" % (path.split('/')[-1], r['clip'], r.get('note', '')))
        except Exception as e:  # the lint must not die on its own instrument
            warns.append("%s: SOURCE FIDELITY not measured: %s" % (path.split('/')[-1], e))
        # LOOP SEAM / SOURCE GRID -- the registry's loops close, on their sources' own keys
        try:
            import importlib, os as _os
            sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
            F = importlib.import_module("56_clip_fidelity")
            reg = F.registry()
            if any(c in clips for c in reg.get("clips", {})):
                for r in F.seams(path, reg):
                    fn = path.split('/')[-1]
                    if r['grid_status'] == "FAIL":
                        fails.append("%s: SOURCE GRID -- loop '%s' is RESAMPLED: %s (re-cut it on the source's own keys: 55_clip_graft.py)"
                                     % (fn, r['clip'], r.get('grid_note', '')))
                    elif r['grid_status'] != "PASS":
                        fails.append("%s: SOURCE GRID -- loop '%s': its source grid cannot be checked (%s) -- every loop names a readable "
                                     "source or grid_source, no exceptions" % (fn, r['clip'], r['grid_status']))
                    if r['seam_status'] == "FAIL":
                        fails.append("%s: LOOP SEAM -- loop '%s' does not close: pose(0) vs pose(T) %.4f m (%s) / %.2f deg, limit %.3f m / %.1f deg; "
                                     "first interval %.2f of the median (a source that is not periodic is blended: 58_loop_blend.py)"
                                     % (fn, r['clip'], r['closure_m'], r['closure_joint'], r['closure_deg'], F.SEAM_M, F.SEAM_DEG, r['first_frac']))
        except Exception as e:
            warns.append("%s: LOOP SEAM not measured: %s" % (path.split('/')[-1], e))
    return dict(file=path, roots=[name(r) for r in roots],
                joints=len(joints), clips=clips,
                morphs=sorted({k for m in g.get('meshes', [])
                               for k in (m.get('extras', {}) or {}).get('targetNames', [])}),
                fails=fails, warns=warns,
                verdict=("FAIL" if fails else "WARN" if warns else "PASS"))


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    out = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
    res = []
    for p in a:
        r = lint(p)
        res.append(r)
        print("\n=== %s" % p)
        print("  roots: %s   joints: %d   clips: %s" %
              (r['roots'], r['joints'], sorted(r['clips'])))
        if r['morphs']:
            print("  morphs: %s" % r['morphs'])
        for cn in sorted(r['clips']):
            c = r['clips'][cn]
            rh = c['root_height']
            print("  %-16s root_h first=%-8s min=%-8s max=%-8s rest=%-8s  scale=%s"
                  % (cn, rh['first'] if rh else '-', rh['min'] if rh else '-',
                     rh['max'] if rh else '-', rh['rest'] if rh else '-',
                     c['scale_tracks'] or 'ok'))
        for f in r['fails']:
            print("  FAIL  %s" % f)
        for w in r['warns']:
            print("  WARN  %s" % w)
        print("  VERDICT: %s" % r['verdict'])
    if out:
        json.dump(res, open(out, 'w'), indent=1)
    sys.exit(1 if any(x['fails'] for x in res) else 0)
