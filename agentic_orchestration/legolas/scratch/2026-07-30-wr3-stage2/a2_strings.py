#!/usr/bin/env python3
import sys, re, pathlib
b = pathlib.Path(sys.argv[1]).read_bytes()
for m in re.finditer(rb'[ -~]{4,}', b):
    print(f"{m.start():#08x}  {m.group().decode('latin-1')}")
