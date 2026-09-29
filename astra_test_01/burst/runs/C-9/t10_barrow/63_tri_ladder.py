#!/usr/bin/env python3
"""C-9 T10-1d: find the SMALLEST triangle count that still holds the silhouette.

    python3 63_tri_ladder.py [asset ...]

The Barrow spends 15.8 ms a frame at 1080p and 1.14 M of that is prop triangles, doubled
by the hull ink pass. So the question is not "does 10k look fine" but "what is the least
each asset can be given before its outline moves", asked once per asset and answered with
the same instrument for all of them: IoU against the UNREDUCED Tripo build through the play
camera, 12 azimuths at pitch 52.954, accept at >= 0.97.

A LADDER, NOT A NUMBER, because the assets are not alike and one budget for all of them is
a guess wearing a decimal point. The stones are convex lumps and lose nothing; the birch is
bare twigs a few millimetres thick and every collapse eats one. 24k already measured the
birch at 0.9364 -- BELOW the gate before the ladder starts -- so for that asset the honest
output is the curve and the count where it plateaus, not a pass. An asset that cannot reach
the gate is reported as not reaching it, with what it did reach, rather than quietly
accepted at the top of the ladder.
"""
import json
import pathlib
import shutil
import subprocess
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import importlib.util

_s = importlib.util.spec_from_file_location("chk", HERE / "62_reduce_v2_check.py")
chk = importlib.util.module_from_spec(_s)
_s.loader.exec_module(chk)

V2 = HERE / "reduced_v2"
LAD = HERE / "kit_work" / "ladder"
GATE = 0.97
LADDER = [10000, 14000, 20000, 28000, 40000, 56000, 80000]
# What the file being REPLACED scores, from reduce_v2_report.json. A replacement that
# scores below this is not an improvement, whatever it costs.
CURRENT_IOU = {k: v["iou_vs_unreduced_play"]["current_mean"]
               for k, v in json.loads((V2 / "reduce_v2_report.json").read_text())
               .get("assets", {}).items()}


def reduce_to(src, dst, tris):
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["blender", "--background", "--python", str(HERE / "55_kit_reduce.py"),
                    "--", str(src), str(dst), str(tris), "1024"],
                   check=True, capture_output=True)


def iou_vs_src(asset, glb, tag):
    chk.probe(chk.ASSETS[asset], chk.WORK / ("%s_src" % asset))
    out = LAD / ("probe_%s_%s" % (asset, tag))
    chk.probe(glb, out)
    d1 = {int(p.stem.split("az")[1]): p
          for p in (chk.WORK / ("%s_src" % asset)).glob("*_az*.png")}
    d2 = {int(p.stem.split("az")[1]): p for p in out.glob("*_az*.png")}
    ks = sorted(set(d1) & set(d2))
    xs = [chk.iou(chk.sil(d1[k]), chk.sil(d2[k])) for k in ks]
    return round(float(np.mean(xs)), 4), round(float(np.min(xs)), 4)


def main() -> int:
    want = sys.argv[1:] or list(chk.ASSETS)
    rep = {}
    f = LAD / "tri_ladder.json"
    LAD.mkdir(parents=True, exist_ok=True)
    if f.exists():
        rep = json.loads(f.read_text())
    for a in want:
        src = chk.ASSETS[a]
        curve, chosen = rep.get(a, {}).get("curve", {}), None
        for t in LADDER:
            if str(t) in curve:
                m, mn = curve[str(t)]["mean"], curve[str(t)]["min"]
            else:
                g = LAD / ("%s_%d.glb" % (a, t))
                reduce_to(src, g, t)
                m, mn = iou_vs_src(a, g, str(t))
                curve[str(t)] = {"mean": m, "min": mn}
            print("   %-12s %6d tris  IoU %.4f (min %.4f)%s"
                  % (a, t, m, mn, "  <= ACCEPT" if m >= GATE and chosen is None else ""))
            if m >= GATE and chosen is None:
                chosen = t
                break
        rep[a] = {"curve": curve, "gate": GATE, "accepted_tris": chosen,
                  "reached_gate": chosen is not None,
                  "best_mean": max(v["mean"] for v in curve.values()),
                  "best_tris": int(max(curve, key=lambda k: curve[k]["mean"]))}
        if chosen is None:
            # DO NOT FALL BACK TO THE BEST IoU. The first version of this line did, and on
            # the birch -- the only asset that misses the gate -- it picked 80,000
            # triangles: the most expensive rung, for the asset placed ELEVEN times, in a
            # pass whose entire purpose is cutting triangles. 880k scene triangles to buy
            # 0.9663, against a whole-scene budget of 1.235M. Defensible line, wrong answer,
            # and it would have shipped quietly because "best" reads like "right".
            #
            # When the gate is unreachable the choice is a trade, so it is made on value and
            # against the file being replaced: the cheapest rung that BEATS THE CURRENT
            # FILE's own IoU. Anything that scores below what is already shipping is not a
            # candidate at any price.
            cur_iou = CURRENT_IOU.get(a)
            cands = [(int(k), v["mean"]) for k, v in curve.items()
                     if cur_iou is None or v["mean"] > cur_iou]
            pick = min(cands)[0] if cands else rep[a]["best_tris"]
            rep[a]["pick_rule"] = ("cheapest rung beating the current file (%.4f)" % cur_iou
                                   if cur_iou else "best available")
            rep[a]["picked_tris"] = pick
            rep[a]["current_file_iou"] = cur_iou
            print("   %-12s DID NOT REACH %.2f on this ladder; best %.4f at %d tris. "
                  "Picked %d (IoU %.4f) -- cheapest that beats the current file's %.4f."
                  % (a, GATE, rep[a]["best_mean"], rep[a]["best_tris"], pick,
                     curve[str(pick)]["mean"], cur_iou or -1))
        else:
            pick = chosen
            rep[a]["picked_tris"] = pick
            rep[a]["pick_rule"] = "cheapest rung at or above the %.2f gate" % GATE
        f.write_text(json.dumps(rep, indent=1) + "\n")
        shutil.copy(LAD / ("%s_%d.glb" % (a, pick)), V2 / ("%s.glb" % a))
        print("   %-12s -> reduced_v2/%s.glb at %d tris" % (a, a, pick))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
