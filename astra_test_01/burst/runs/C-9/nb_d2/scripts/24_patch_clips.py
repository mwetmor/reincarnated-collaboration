# Patch a character GLB's animation tracks in place: neutralise joint scale
# tracks, and shift a clip's root translation to re-ground it.
#
#   python3 scripts/24_patch_clips.py <in.glb> <out.glb> \
#           --scale-to-one --shift <clip>:<dz_metres> [...]
#
# WHY A BINARY PATCH AND NOT A BLENDER ROUND TRIP. The body GLB is 21 MB and
# almost all of it is the painted texture. Re-importing and re-exporting to
# change two animation tracks re-encodes that texture and rebuilds every mesh,
# morph and skin -- a large blast radius to fix 291 floats. This rewrites the
# two accessors the change actually touches and copies everything else byte for
# byte. The float32 values are overwritten in place, so no offset moves.
#
# The metre->glTF conversion is READ FROM THE FILE (the accumulated node scale
# on Hips' ancestors), not assumed, and the result is verified by measuring the
# feet in Blender afterwards. This rig's factor is 0.010883 = 0.01 x 1.85/1.70:
# Meshy's 0.01 object scale times the T8 hand-off's fit to a 1.85 m body. A
# hard-coded 0.01 would have been wrong by 8.8% and would still have looked
# roughly right.
import json, struct, sys
import numpy as np

CT = {5120: ('b', 1), 5121: ('B', 1), 5122: ('h', 2), 5123: ('H', 2),
      5125: ('I', 4), 5126: ('f', 4)}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def split_glb(raw):
    assert raw[:4] == b'glTF'
    off, js, jsrange, binrange = 12, None, None, None
    while off < len(raw):
        ln, ty = struct.unpack_from('<II', raw, off)
        if ty == 0x4E4F534A:
            js = json.loads(raw[off + 8:off + 8 + ln])
            jsrange = (off + 8, ln)
        elif ty == 0x004E4942:
            binrange = (off + 8, ln)
        off += 8 + ln + (-ln % 4)
    return js, jsrange, binrange


def acc_offsets(g, idx, binstart):
    """Byte offset of every element of an accessor, honouring byteStride."""
    acc = g['accessors'][idx]
    n, ncomp = acc['count'], NC[acc['type']]
    fmt, sz = CT[acc['componentType']]
    assert acc['componentType'] == 5126, "only float accessors are patched"
    bv = g['bufferViews'][acc['bufferView']]
    base = binstart + bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    stride = bv.get('byteStride') or ncomp * sz
    return [base + i * stride for i in range(n)], ncomp


def main():
    src, dst = sys.argv[1], sys.argv[2]
    shifts = {}
    for i, x in enumerate(sys.argv):
        if x == '--shift':
            k, v = sys.argv[i + 1].split(':')
            shifts[k] = float(v)
    raw = bytearray(open(src, 'rb').read())
    g, _, (binstart, binlen) = split_glb(raw)
    nodes = g['nodes']
    name = lambda i: nodes[i].get('name', 'node%d' % i)
    parent = {}
    for i, nd in enumerate(nodes):
        for c in nd.get('children', []):
            parent[c] = i
    joints = set()
    for sk in g.get('skins', []):
        joints.update(sk.get('joints', []))
    roots = [j for j in joints if parent.get(j) not in joints]
    assert len(roots) == 1, "expected one skeleton root, got %s" % roots
    ROOT = roots[0]

    # metres per glTF unit for the root joint: the product of the scales on
    # every ancestor above it. Read, not assumed.
    f, k = 1.0, parent.get(ROOT)
    chain = []
    while k is not None:
        s = nodes[k].get('scale', [1, 1, 1])
        chain.append((name(k), s))
        f *= float(s[1])
        k = parent.get(k)
    print("root joint '%s'; ancestor scales %s -> %.8f m per glTF unit"
          % (name(ROOT), chain, f))

    # how many channels reference each accessor -- never patch a shared one
    ref = {}
    for an in g.get('animations', []):
        for ch in an.get('channels', []):
            ref[an['samplers'][ch['sampler']]['output']] = \
                ref.get(an['samplers'][ch['sampler']]['output'], 0) + 1

    did = []
    for an in g.get('animations', []):
        cn = an.get('name', '?')
        for ch in an.get('channels', []):
            t = ch.get('target', {})
            nidx, pth = t.get('node'), t.get('path')
            if nidx is None:
                continue
            out = an['samplers'][ch['sampler']]['output']
            if pth == 'scale' and nidx in joints and '--scale-to-one' in sys.argv:
                offs, ncomp = acc_offsets(g, out, binstart)
                cur = struct.unpack_from('<%df' % ncomp, raw, offs[0])
                if max(abs(c - 1.0) for c in cur) <= 1e-3:
                    continue
                assert ref[out] == 1, "accessor %d is shared" % out
                for o in offs:
                    struct.pack_into('<%df' % ncomp, raw, o, *([1.0] * ncomp))
                did.append("%s/%s scale %s -> 1.0 (%d keys)"
                           % (cn, name(nidx), [round(c, 6) for c in cur], len(offs)))
            if pth == 'translation' and nidx == ROOT and cn in shifts:
                offs, ncomp = acc_offsets(g, out, binstart)
                assert ref[out] == 1, "accessor %d is shared" % out
                d = shifts[cn] / f          # metres -> glTF units, up axis is Y
                b4 = struct.unpack_from('<3f', raw, offs[0])
                for o in offs:
                    v = list(struct.unpack_from('<3f', raw, o))
                    v[1] += d
                    struct.pack_into('<3f', raw, o, *v)
                af = struct.unpack_from('<3f', raw, offs[0])
                did.append("%s/%s translation.y %+.4f glTF units (%+.5f m); "
                           "first key %.4f -> %.4f (%d keys)"
                           % (cn, name(nidx), d, shifts[cn], b4[1], af[1], len(offs)))
    for x in did:
        print("  patched %s" % x)
    assert did, "nothing patched -- check the clip names"
    open(dst, 'wb').write(bytes(raw))
    print("wrote %s (%.2f MB), same byte length as input: %s"
          % (dst, len(raw) / 1e6, len(raw) == len(open(src, 'rb').read())))


if __name__ == '__main__':
    main()
