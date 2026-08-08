#!/usr/bin/env python3
"""Same-EXACT-FRAME plate + readout census.

Why this exists rather than reusing eor_platebind.scan output. `scan` decodes with
`-ss t0 -vf fps=N`, which RESAMPLES: the frame it labels t is not guaranteed to be
the frame an exact seek to t returns. The plate crops in this touch are exact-seek
grabs, so the binding must be computed on those same exact-seek frames or the two
instruments are not talking about the same picture.

Emits, per requested t: sub-pixel plate fill edge + every readout blob on the frame
(parsed and unparsed), so an unparsed near-match cannot hide.
"""
import json
import subprocess
import sys

import numpy as np

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline")
import eor_cohort as CO      # noqa: E402
import eor_hpocr as HO       # noqa: E402

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-08-kc2-crabling-rotmouth/work")
from subpix import edge      # noqa: E402

W, H = 1920, 1080
ATLAS = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
         "galadriel/captures/2026-08-08-kc2-board-closure/work/atlas.npz")


def exact(video, t):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-frames:v", "1",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(b[:W * H * 3], np.uint8).reshape(H, W, 3)


def run(video, ts, track_x0, track_x1, x_hi, atlas):
    out = []
    for t in ts:
        fr = exact(video, t)
        xe, lp, rp = edge(fr, track_x0, x_hi)
        fp = (xe - track_x0) / (track_x1 - track_x0) if xe else None
        rows = []
        v_all = HO.white(fr)
        for (bx0, by0, bx1, by1, dens) in CO.blobs2(fr):
            s, sc, mg = HO.read_string(atlas, v_all[by0:by1 + 1, bx0:bx1 + 1])
            pe = CO.parse_ext(s)
            rows.append({"box": [bx0, by0, bx1, by1], "raw": s,
                         "kind": pe[0] if pe else None,
                         "cur": pe[1] if pe else None,
                         "max": pe[2] if pe else None,
                         "score": round(sc, 3)})
        out.append({"t": t, "edge": xe, "frac": fp, "L": lp, "R": rp, "rd": rows})
        print(f"\n=== t={t}  plate edge={xe if xe is None else round(xe,2)} "
              f"frac={fp if fp is None else round(fp,4)}")
        for r in rows:
            if r["by"] if False else True:
                pass
            f = (r["cur"] / r["max"]) if (r["cur"] is not None and r["max"]) else None
            pred = (track_x0 + f * (track_x1 - track_x0)) if f is not None else None
            d = (pred - xe) if (pred is not None and xe is not None) else None
            mark = ""
            if d is not None and abs(d) <= 1.0:
                mark = "   <== within 1.0 px of plate"
            print(f"   y={r['box'][1]:>4} x={r['box'][0]:>4} {r['raw']:>26} "
                  f"f={('%.5f' % f) if f is not None else '   -   '} "
                  f"pred_x={('%8.2f' % pred) if pred is not None else '    -   '} "
                  f"d={('%+7.2f' % d) if d is not None else '   -   '}{mark}")
    return out


if __name__ == "__main__":
    atlas = HO.load(ATLAS)
    v = "/tmp/kc2-s2.mp4"
    res = {}
    res["crabling"] = run(v, [701.7333, 701.7667, 701.8, 701.9333], 862.0, 1059.43, 1110, atlas)
    res["rotmouth"] = run(v, [704.4667, 704.5333, 704.6333], 862.0, 1059.43, 1110, atlas)
    json.dump(res, open("exactbind.json", "w"), indent=1)
