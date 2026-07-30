#!/usr/bin/env python3
import sys, pathlib, struct
sys.path.insert(0,'.')
from a4_parse import parse
a = parse(sys.argv[1])
b = pathlib.Path(sys.argv[1]).read_bytes()
tail = b[a['consumed']:]
print(f"tail {len(tail)} bytes")
print(tail.hex(' '))
print("--- ascii ---")
print(''.join(chr(c) if 32 <= c < 127 else '.' for c in tail))
