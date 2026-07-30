#!/usr/bin/env python3
"""A1 — ANM v2 format probe. READ-ONLY."""
import struct, sys, pathlib
p = pathlib.Path(sys.argv[1]); b = p.read_bytes()
print(p.name, "size", len(b))
magic = b[:3]; ver = b[3]
a,c,d = struct.unpack_from("<III", b, 4)
nl, = struct.unpack_from("<I", b, 16)
name = b[20:20+nl].decode('latin-1')
print(f"magic={magic} ver={ver} h1={a} h2={c} h3={d} nameLen={nl} name={name!r}")
pos = 20+nl
print("after name, next 32 bytes:", b[pos:pos+32].hex(' '))
# try: u32 count then floats
for guess in range(0, 8):
    o = pos+guess
    vals = struct.unpack_from("<8f", b, o)
    print(f"  off+{guess}: {['%.4g'%v for v in vals]}")
