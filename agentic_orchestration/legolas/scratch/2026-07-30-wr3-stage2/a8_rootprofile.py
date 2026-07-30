#!/usr/bin/env python3
import sys, pathlib, math
sys.path.insert(0,'.')
from a4_parse import parse
a = parse(sys.argv[1])
root = a['bones'][0]
print(f"{pathlib.Path(sys.argv[1]).name} bone={root[0]} keys={a['nkeys']} fps={a['fps']}")
prev = None
for i,k in enumerate(root[1]):
    x,y,z = k[0],k[1],k[2]
    d = math.dist((x,y,z), prev) if prev else 0.0
    print(f"  f{i:03d} t={i/a['fps']:.4f}s  pos=({x:8.4f},{y:8.4f},{z:8.4f})  step={d:7.4f}  cum={math.dist((x,y,z),(root[1][0][0],root[1][0][1],root[1][0][2])):8.4f}")
    prev = (x,y,z)
