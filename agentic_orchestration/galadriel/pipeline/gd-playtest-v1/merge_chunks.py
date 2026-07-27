#!/usr/bin/env python3
"""
Merge parallel T-A segment workers into one ordered sample stream.

The full run is decode-bound, not I/O-bound, once the video is local: a serial
2 fps pass over 409k frames projected to ~78 min. Splitting the timeline into
four `-ss/-t` segments and running four workers cuts that to roughly a quarter
on a 4-performance-core machine.

Segment boundaries are placed on whole seconds so the 2 fps sample grid stays
uniform across the joins. Duplicate `pts_s` (possible if two segments overlap by
a frame at a boundary) are dropped, keeping the first.

The joins are not trusted on faith: `gate_and_fit.py`'s monotonicity gate runs
over the merged stream, so a seek that landed wrong would surface as a
non-monotonic `kills`/`play_time` sample at a segment boundary rather than
being silently absorbed.
"""

import argparse
import glob
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    files = sorted(glob.glob(args.glob))
    rows = []
    for f in files:
        n = 0
        for line in open(f):
            rows.append(json.loads(line))
            n += 1
        print(f"  {f}: {n} samples")

    rows.sort(key=lambda r: r["pts_s"])
    seen, out = set(), []
    for r in rows:
        if r["pts_s"] in seen:
            continue
        seen.add(r["pts_s"])
        r["i"] = len(out)
        out.append(r)

    with open(args.out, "w") as fh:
        for r in out:
            fh.write(json.dumps(r) + "\n")

    dups = len(rows) - len(out)
    print(f"merged {len(out)} samples "
          f"({out[0]['pts_s']} -> {out[-1]['pts_s']} s), {dups} duplicate pts dropped")

    # report any gap larger than one sample period, which would indicate a
    # worker that died or a segment boundary that did not meet
    gaps = [(out[i - 1]["pts_s"], out[i]["pts_s"])
            for i in range(1, len(out))
            if out[i]["pts_s"] - out[i - 1]["pts_s"] > 0.75]
    if gaps:
        print(f"  WARNING {len(gaps)} timeline gaps > 0.75 s: {gaps[:10]}")
    else:
        print("  timeline continuous at the 0.5 s sample period")


if __name__ == "__main__":
    main()
