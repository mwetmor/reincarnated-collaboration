"""Read glTF/GLB animation channels directly -- no Blender, no Godot, nothing imported.

What a clip IS, key by key: sampler times, interpolation, and every rotation and
translation value, so a source clip and the shipped clip can be compared on the data
itself rather than on how an engine happens to play them."""
import json, struct, sys
import numpy as np

CT = {5126: ('f', 4), 5123: ('H', 2), 5125: ('I', 4), 5121: ('B', 1)}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}

def load(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[:4] == b'glTF'
    off = 12
    js, bin_ = None, None
    while off < len(data):
        ln, ty = struct.unpack_from('<II', data, off)
        chunk = data[off + 8: off + 8 + ln]
        if ty == 0x4E4F534A: js = json.loads(chunk)
        elif ty == 0x004E4942: bin_ = chunk
        off += 8 + ln
    return js, bin_

def accessor(js, bin_, i):
    a = js['accessors'][i]
    bv = js['bufferViews'][a['bufferView']]
    fmt, sz = CT[a['componentType']]
    n = NC[a['type']]
    start = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    stride = bv.get('byteStride', sz * n)
    out = np.empty((a['count'], n), dtype=np.float64)
    for k in range(a['count']):
        out[k] = struct.unpack_from('<' + fmt * n, bin_, start + k * stride)
    if a.get('normalized') and fmt != 'f':
        out /= float({'H': 65535, 'B': 255, 'I': 4294967295}[fmt])
    return out[:, 0] if n == 1 else out

def clips(path):
    """{clip: {bone: {'rotation': (times, values, interp), 'translation': ...}}}"""
    js, bin_ = load(path)
    names = [n.get('name', 'node%d' % i) for i, n in enumerate(js['nodes'])]
    out = {}
    for an in js.get('animations', []):
        c = {}
        for ch in an['channels']:
            tgt = ch['target']
            if 'node' not in tgt: continue
            s = an['samplers'][ch['sampler']]
            t = accessor(js, bin_, s['input'])
            v = accessor(js, bin_, s['output'])
            interp = s.get('interpolation', 'LINEAR')
            if interp == 'CUBICSPLINE':        # [in-tangent, value, out-tangent] per key
                v = v.reshape(len(t), 3, -1)[:, 1, :]
            c.setdefault(names[tgt['node']], {})[tgt['path']] = (t, v, interp)
        out[an.get('name', 'anim')] = c
    return out

def qangle(a, b):
    """Angle in degrees between consecutive quaternions, sign-agnostic (the SHORTEST
    rotation between them), plus whether the raw 4-vectors point opposite ways."""
    d = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
    return np.degrees(2.0 * np.arccos(min(1.0, abs(d)))), d < 0.0
