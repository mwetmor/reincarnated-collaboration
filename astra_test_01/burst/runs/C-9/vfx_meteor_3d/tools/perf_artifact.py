#!/usr/bin/env python3
"""C-9 lane B: a perf record's summary (the scene's own, without the frame-by-frame arrays) into artifacts/.
   perf_artifact.py <perf.json> <out.json> <label>"""
import json, sys
d = json.load(open(sys.argv[1]))
d.pop("frames", None)
d["label"] = sys.argv[3]
json.dump(d, open(sys.argv[2], "w"), indent=1)
print("wrote", sys.argv[2])
