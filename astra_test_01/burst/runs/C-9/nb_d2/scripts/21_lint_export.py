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
#   WARN  a clip whose root-height BAND does not overlap any other clip's band.
#         Added after the fact, because the rule above does not discriminate:
#         on the broken file it fired on attack, idle and run, and only one of
#         the three was a defect -- a check that flags the innocent alongside
#         the guilty has not told you anything. The band rule fires on exactly
#         one clip of the broken file (idle, 99.7-103.1, overlapping nothing)
#         and on none of the fixed file. A crouch or a lunge still SHARES
#         ground with the other clips; a retargeted one does not.
import json, struct, sys
import numpy as np

SCALE_TOL, ROOT_TOL = 1e-3, 0.05
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


def lint(path):
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
    fails, warns, clips = [], [], {}
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
