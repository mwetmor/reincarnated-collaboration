#!/usr/bin/env python3
"""List a Godot 4 .pck's file table (pack format 3): one path a line. C-9 fences use it instead of grepping
the pck's bytes (a path named in a script or the uid cache is not a packed file)."""
import struct, sys
f = open(sys.argv[1], 'rb')
magic, ver, ma, mi, pa, flags = struct.unpack('<4sIIIII', f.read(24))
assert magic == b'GDPC' and ver == 3, (magic, ver)
file_base, dir_off = struct.unpack('<QQ', f.read(16))
f.seek(dir_off)
n = struct.unpack('<I', f.read(4))[0]
for _ in range(n):
    L = struct.unpack('<I', f.read(4))[0]
    path = f.read(L).rstrip(b'\0').decode()
    f.read(16 + 16 + 4)
    print(path)
