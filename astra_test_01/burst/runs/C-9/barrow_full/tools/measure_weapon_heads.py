#!/usr/bin/env python3
"""C-9 R-C9-133: the weapon HEAD of a skinned weapon GLB in its grip bone's local space -- the farthest vertex from the
grip, by the skin's own inverse bind matrix (glTF joint-local units, the frame Godot's bone pose is in) -- and its
length in metres. The whirlwind port's tip rule (whirlwind_channel.gd _weapon_head_local), for weapons the Barrow's
rig does not carry. drax.
  python3 tools/measure_weapon_heads.py GLB:BONE [GLB:BONE ...]
"""
import json
import struct
import sys

import numpy as np


def load(p):
    b = open(p, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n])
    off = 20 + n
    bn = struct.unpack("<I", b[off:off + 4])[0]
    return j, b[off + 8:off + 8 + bn]


def acc(j, bin_, i):
    a = j["accessors"][i]
    bv = j["bufferViews"][a["bufferView"]]
    dt = np.dtype({5126: "f4", 5123: "u2", 5121: "u1", 5125: "u4"}[a["componentType"]])
    nc = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}[a["type"]]
    o = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    stride = bv.get("byteStride", 0)
    if stride and stride != dt.itemsize * nc:
        raw = np.frombuffer(bin_, dtype=np.uint8, count=stride * a["count"], offset=o).reshape(a["count"], stride)
        return raw[:, :dt.itemsize * nc].copy().view(dt).reshape(a["count"], nc)
    return np.frombuffer(bin_, dtype=dt, count=a["count"] * nc, offset=o).reshape(a["count"], nc)


out = {}
for arg in sys.argv[1:]:
    p, bone = arg.rsplit(":", 1)
    j, bin_ = load(p)
    sk = j["skins"][0]
    names = [j["nodes"][i]["name"] for i in sk["joints"]]
    m = acc(j, bin_, sk["inverseBindMatrices"]).reshape(-1, 4, 4).transpose(0, 2, 1)[names.index(bone)]
    best, bd = None, -1.0
    for me in j["meshes"]:
        for pr in me["primitives"]:
            v = acc(j, bin_, pr["attributes"]["POSITION"]).astype(float)
            vl = (m @ np.c_[v, np.ones(len(v))].T).T[:, :3]
            d = np.linalg.norm(vl, axis=1)
            k = int(d.argmax())
            if d[k] > bd:
                bd, best = float(d[k]), vl[k]
    unit = 1.0 / float(np.linalg.norm(m[:3, 0]))
    out[bone] = {"glb": p, "head_local": [round(float(x), 4) for x in best], "length_m": round(bd * unit, 4), "unit_m": round(unit, 6)}
print(json.dumps(out, indent=1))
