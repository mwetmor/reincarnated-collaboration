#!/usr/bin/env python3
import sys, pathlib, re
sys.path.insert(0,'.')
from a4_parse import parse
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.anm")):
    a = parse(p)
    b = p.read_bytes()[a['consumed']:]
    txt = b.decode('latin-1')
    cbs = re.findall(r'name\s*=\s*"([^"]*)"\s*\r?\n\s*frame\s*=\s*(-?\d+)', txt)
    dur = (a['nkeys']-1)/a['fps']
    s = f"{p.name.split('__')[-1]:44s} keys={a['nkeys']:3d} fps={a['fps']} dur=({a['nkeys']}-1)/{a['fps']}={dur:.4f}s |"
    for n,f in cbs:
        s += f" {n}@f{f}={int(f)/a['fps']:.4f}s"
    if not cbs: s += " (no callbacks)"
    print(s)
