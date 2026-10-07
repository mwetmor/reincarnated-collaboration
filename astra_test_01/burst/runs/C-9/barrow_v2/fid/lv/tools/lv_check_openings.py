#!/usr/bin/env python3
"""BV2F LV, R-C9-177 CHECK (a) (Phase 1 DoD): every deliverer opening must have VISIBLE projected area at the play camera.

    LV_VARIANT=v7c python3 fid/lv/tools/lv_check_openings.py [--render]

--render runs the frozen Tier-B capture_ids (through godot_run.sh, lv_guide_run.sh IDS_ONLY=1) twice per guide section with
the level's opening PROBES (scripts/bv2f/bv2f_level.gd _build_probes): BV2F_PROBES=with (everything drawn: what the play
camera sees of each opening) and BV2F_PROBES=only (the probes alone: the unoccluded reference). The guide camera IS the play
camera (orthographic, pitch 52.95, yaw 47, 100.6 px/m), so a probe's pixels are its projected area at the play camera.

Per opening: visible px (with), reference px (only), visible projected m2 (px / 100.6^2), % of its own unoccluded
projection, its FRONTAL area (w x h for a door; the patch for the open-to-sky probes), and whether a vertical opening FACES
the camera (a door seen from behind shows the back of its probe -- that is not the opening, so it scores 0).
PASS = visible m2 > 0 for all six.  -> fid/lv/<guide dir>/check_a.json + check_a.md"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
VAR = os.environ.get("LV_VARIANT", "v7b")
GD = os.path.join(LV, "guide" if VAR == "v7b" else "guide_" + VAR)
BF = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", VAR))
PPM = 100.617553710938
sys.path.insert(0, HERE)
import lv_openings as OPN  # noqa: E402


def run(mode):
    env = dict(os.environ, LV_VARIANT=VAR, IDS_ONLY="1", BV2F_PROBES=mode, BV2F_OUT_SUFFIX="probe_%s_" % mode)
    r = subprocess.run(["bash", os.path.join(HERE, "lv_guide_run.sh")], env=env, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        sys.exit("[check_a] HALT: capture_ids failed (%s): %s" % (mode, r.stderr[-400:]))


def count(mode, lvl):
    tot = {}
    for s in lvl["frame"]["sections"]:
        d = os.path.join(GD, "probe_%s_%s" % (mode, s["id"]))
        fg = json.load(open(os.path.join(LV, VAR, "frame_grid_%s.json" % s["id"])))
        pad = int(fg.get("pad_px", 0))
        sw, sh = s["px"]
        a = np.asarray(Image.open(os.path.join(d, "ids.png")).convert("RGB")).astype(np.int32)[pad:pad + sh, pad:pad + sw]
        code = a[..., 0] * 65536 + a[..., 1] * 256 + a[..., 2]
        ij = json.load(open(os.path.join(d, "ids.json")))
        for rec in ij["placements"].values():
            if not rec["id"].startswith("probe_"):
                continue
            r, g, b = rec["rgb"]
            tot[rec["id"][6:]] = tot.get(rec["id"][6:], 0) + int((code == r * 65536 + g * 256 + b).sum())
    return tot


def main():
    lvl = json.load(open(os.path.join(BF, "level.json")))
    if "--render" in sys.argv:
        run("with")
        run("only")
    w, o = count("with", lvl), count("only", lvl)
    rows = []
    for op in lvl["sim"]["openings"]:
        pr = op.get("probe")
        if pr is None:
            continue
        oid = op["id"]
        faces = OPN.faces_camera(pr)                                       # ONE rule, shared with declared_openings.json
        vis_px = w.get(oid, 0) if faces else 0
        ref_px = o.get(oid, 0)
        rows.append({"opening": oid, "anchor": op["point"], "probe": pr["type"], "faces_camera": faces,
                     "visible_px": vis_px, "reference_px": ref_px, "visible_m2": round(vis_px / PPM ** 2, 2),
                     "reference_m2": round(ref_px / PPM ** 2, 2), "pct_of_unoccluded": round(100.0 * vis_px / ref_px, 1) if ref_px else 0.0,
                     "frontal_m2": pr["frontal_m2"], "pct_of_frontal": round(100.0 * (vis_px / PPM ** 2) / pr["frontal_m2"], 1) if pr["frontal_m2"] else 0.0,
                     "PASS": vis_px > 0})
    ok = len(rows) == 6 and all(r["PASS"] for r in rows)
    out = {"_what": __doc__.strip().splitlines()[0], "variant": VAR, "pass": ok, "rows": rows,
           "units": "m2 = projected (screen) square metres at the play camera (px / 100.6^2); frontal = the opening's own area"}
    json.dump(out, open(os.path.join(GD, "check_a.json"), "w"), indent=1)
    md = ["| Opening (anchor) | Probe | Faces camera | Visible m² | % of unoccluded | Frontal m² | % of frontal | |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append("| %s (%s) | %s | %s | %.2f | %.1f | %.1f | %.1f | %s |" % (r["opening"], r["anchor"], r["probe"], "yes" if r["faces_camera"] else "**NO**",
                  r["visible_m2"], r["pct_of_unoccluded"], r["frontal_m2"], r["pct_of_frontal"], "PASS" if r["PASS"] else "**FAIL**"))
    open(os.path.join(GD, "check_a.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))
    print("[check_a] %s: %s" % (VAR, "PASS" if ok else "FAIL"))


if __name__ == "__main__":
    main()
