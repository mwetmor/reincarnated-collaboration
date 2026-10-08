#!/usr/bin/env python3
"""BV2F PT (R-C9-247) PROTOTYPE, OFF the build: the Tier-B DEV-23 stitch with v1's 256-px linear overlap ramp replaced by
a SHORT HAND-OVER at the strip's far end -- the neighbour's OWN pixels are kept across the overlap and the ramp to the
chunk runs only over the last K px before the context boundary (the image model softens its redraw of the pasted strip;
v1's full-width ramp ends on that soft redraw exactly where the chunk's crisp new paint begins). Proposed DEV-25.
    python3 fid/pt/tools/handover_proto.py <cfg.json> <out.png> <K>"""
import os, sys
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
st = os.path.join(FID, "v1tools", "tierB", "conductor_scripts", "guided_stitch.py")
K = int(sys.argv[3])
src = open(st).read()
a = "up = np.linspace(0, 1, OV, endpoint=False) + 0.5/OV\n"
assert src.count(a) == 1
src = src.replace(a, "up = np.clip((np.arange(OV) + 0.5 - (OV - %d)) / %d.0, 0.0, 1.0)   # PROTO DEV-25: hand-over over the last K px\n" % (K, K))
for a2 in ("        if c < COLS-1: wx[W-OV:] *= up[::-1]\n", "        if r < ROWS-1: wy[H-OV:] *= up[::-1]\n"):
    assert src.count(a2) == 1
    src = src.replace(a2, a2.replace("up[::-1]", "(1.0 - up)"))   # PROTO: the partition of unity for an asymmetric ramp
sys.argv = [st, sys.argv[1], sys.argv[2]]
exec(compile(src, st, "exec"), {"__name__": "__main__", "__file__": st})
