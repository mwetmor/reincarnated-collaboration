#!/usr/bin/env python3
"""C-9: collect the cut Grok RUN cells into a manifest this project can build from.

The conductor's runs/C-9/artifacts/knight_cells_manifest.json is READ-ONLY for this
seam and carries walk + idle only, so the run cells get their own manifest HERE, in the
same schema, and tools/build_knight_frames.py merges the two. Nothing is written into
artifacts/.

Scans runs/C-9/p7/<D>_run/ (and <D>_run_p<N>/ if a forced-period cut was needed),
prefers the forced cut when both exist, and reads the stride period out of the cut's
own REGISTRATION.json rather than assuming it -- series.json holds the per-frame
tracking (head_top_y, sole_y, bbox ...) and has no period at all; asking it for one
returns None quietly and the manifest then records every stride as 0 frames.

A direction with no cut is simply absent from the manifest -- NOT filled in with a
neighbour or a mirror. W_run is absent today because the clip generation failed
(p7_run.log: "CLIP W_run ok=false ... probe=" with an empty probe), and a knight whose
W run is quietly some other direction's pixels is worse than one who falls back to his
own walk and says so.
"""
import json
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
RUNS = PROJ.parents[2]
P7 = RUNS / "runs" / "C-9" / "p7"
OUT = PROJ / "frames" / "knight_run_cells.json"
DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]


def main():
    cells, missing, notes = {}, [], {}
    for d in DIRS:
        cands = sorted(P7.glob("%s_run_p*" % d)) + [P7 / ("%s_run" % d)]
        pick = None
        for c in cands:
            if (c / "registration.json").exists() and list((c / "frames" / "run" / d).glob("*.png")):
                pick = c
                break
        if pick is None:
            missing.append(d)
            continue
        reg = json.loads((pick / "registration.json").read_text())
        frames = sorted((pick / "frames" / "run" / d).glob("run_%s_*.png" % d))
        rest = pick / "frames" / "rest" / d / ("rest_%s.png" % d)
        if len(frames) != 12 or not rest.exists():
            missing.append(d)
            notes[d] = "incomplete cut: %d frames, rest=%s" % (len(frames), rest.exists())
            continue
        period = reg.get("period") or {}
        if not period.get("frames"):
            missing.append(d)
            notes[d] = "cut has no period in registration.json"
            continue
        cells["run_%s" % d] = {
            "frames": [str(p.relative_to(RUNS)) for p in frames],
            "rest": [str(rest.relative_to(RUNS))],
            "stride_native_frames": int(period.get("frames", 0) or 0),
            "fps_source": float(reg.get("fps_out", 24)),
        }
        notes[d] = "%s  period %s frames (%s, confidence %.2f)" % (
            pick.name, period.get("frames"), period.get("source"),
            float(period.get("confidence", 0.0)))
    OUT.write_text(json.dumps({
        "note": ("C-9 knight RUN cells, cut by tools/cut_run_clips.sh from "
                 "runs/C-9/xvideo/in/<D>_run.mp4 with the frozen oracle.video_cut. "
                 "Written by tools/build_run_manifest.py; merged with the conductor's "
                 "walk/idle manifest by tools/build_knight_frames.py."),
        "cells": cells, "missing_directions": missing, "per_direction": notes,
    }, indent=1))
    print("run cells: %d/%d  missing %s" % (len(cells), len(DIRS), missing or "none"))
    for d in DIRS:
        if d in notes:
            print("  %-3s %s" % (d, notes[d]))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
