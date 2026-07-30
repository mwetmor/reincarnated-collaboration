#!/usr/bin/env python3
import struct, sys, pathlib
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.anm")):
    b = p.read_bytes()
    a,c,d = struct.unpack_from("<III", b, 4)
    nl, = struct.unpack_from("<I", b, 16)
    print(f"{p.name:60s} h1={a:5d} h2={c:5d} h3={d:5d}  size={len(b):8d}  firstbone={b[20:20+nl].decode('latin-1')}")
