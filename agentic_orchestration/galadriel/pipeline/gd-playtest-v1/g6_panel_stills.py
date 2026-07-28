#!/usr/bin/env python3
"""
G-6 pass 4: run the T-A PlayStats panel reader over the STILLS (not the video).

Purpose: place every skill-window / character-window still on the run's
`play_time` axis, so a skill allocation read from a still can be dated. The
panel reader is the one built + calibrated for this footage in the T-A ledger
work; the stills are the same 1920x1080 UI, so it applies unchanged.

usage: g6_panel_stills.py <frame_id...>   (or --all-ui)
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from panel_ocr import PanelReader  # noqa: E402

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
MODEL = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
             "galadriel/captures/2026-07-26-gd-playtest-v1/panel-ocr-model.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames", nargs="*", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default="g6-panel-stills.json")
    a = ap.parse_args()
    if a.all:
        ids = sorted(int(f.name[12:-5]) for f in SRC.iterdir()
                     if f.name.startswith("Screenshot (") and f.name.endswith(").png"))
    else:
        ids = a.frames
    r = PanelReader(str(MODEL))
    recs = {}
    for i in ids:
        with Image.open(SRC / f"Screenshot ({i}).png") as im:
            arr = np.asarray(im.convert("RGB"))
        rec = r.read(arr)
        recs[i] = rec
        pt = rec.get("play_time")
        print(f"f{i:4d}  status={rec['status']:8s} play_time={pt} "
              f"lvl={rec.get('max_level')} kills={rec.get('kills')} "
              f"deaths={rec.get('deaths')} pots={rec.get('health_potions')}/"
              f"{rec.get('mana_potions')} skills={ {k: v['count'] for k, v in rec.get('skills', {}).items()} }",
              flush=True)
    with open(OUT / a.out, "w") as f:
        json.dump(recs, f, indent=1)


if __name__ == "__main__":
    main()
