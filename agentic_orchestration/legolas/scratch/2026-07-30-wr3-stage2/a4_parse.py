#!/usr/bin/env python3
"""A4 — ANM v2 full parser. header: 'ANM'+u8 ver, u32 nBones, u32 nKeys, u32 fps,
then per bone: u32 nameLen, name, nKeys * 56-byte key. READ-ONLY."""
import struct, sys, pathlib

def parse(path):
    b = pathlib.Path(path).read_bytes()
    assert b[:3] == b"ANM"
    ver = b[3]
    nbones, nkeys, fps = struct.unpack_from("<III", b, 4)
    pos = 16
    bones = []
    for i in range(nbones):
        nl, = struct.unpack_from("<I", b, pos); pos += 4
        name = b[pos:pos+nl].decode('latin-1'); pos += nl
        keys = []
        for k in range(nkeys):
            keys.append(struct.unpack_from("<14f", b, pos)); pos += 56
        bones.append((name, keys))
    return dict(ver=ver, nbones=nbones, nkeys=nkeys, fps=fps, bones=bones,
                consumed=pos, size=len(b))

if __name__ == "__main__":
    a = parse(sys.argv[1])
    print(f"ver={a['ver']} nbones={a['nbones']} nkeys={a['nkeys']} fps={a['fps']} "
          f"consumed={a['consumed']} size={a['size']} tail={a['size']-a['consumed']}")
    want = sys.argv[2] if len(sys.argv) > 2 else None
    for name, keys in a['bones']:
        if want and want.lower() not in name.lower():
            continue
        print(f"--- bone {name!r}")
        for i, k in enumerate(keys):
            print(f"  f{i:03d} " + " ".join(f"{v:9.4f}" for v in k))
