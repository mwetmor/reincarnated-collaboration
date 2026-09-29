#!/usr/bin/env python3
"""C-9 T9: the bridge-frame numbers, with attribution, from the frames shot_t9b.gd saved.

    python3 tools/t9_metrics.py --frames DIR [--calibrate]

T9-0 published mean luma 87.7, near-black 19.05% and "16.21% of the frame lost more than
half its light" for the lit bridge, against a painted 113.6 / 1.70%. The tool that produced
those numbers was not kept -- nothing in the run tree computes them -- so the DEFINITION
behind them is not recoverable by reading, only by fitting. --calibrate sweeps the two
choices that a near-black percentage actually turns on (which luma, which threshold) and
reports which pair reproduces T9-0 on a re-shot baseline. Whatever it says, every state
here is measured with ONE definition, so the ATTRIBUTION between albedo and props is sound
even if the absolute numbers sit on a different definition from T9-0's.

"Lost more than half its light" is per pixel against the painted frame, which is why
shot_t9b.gd shoots the painted panel in the same run, at the same pose, at true scale.
"""
import argparse
import json
import pathlib

import numpy as np
from PIL import Image

STATES = ["lit_base", "lit_albedo", "lit_props", "lit_albedo_props",
          "noink_base", "noink_albedo_props", "flat_base", "flat_albedo"]


def luma(a: np.ndarray, how: str) -> np.ndarray:
    a = a.astype(np.float32)
    if how == "mean":
        return a.mean(-1)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def load(d: pathlib.Path, nm: str) -> np.ndarray | None:
    p = d / ("t9b_bridge_%s.png" % nm)
    return np.asarray(Image.open(p).convert("RGB")) if p.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", required=True)
    ap.add_argument("--luma", default="mean", choices=["mean", "rec709"])
    ap.add_argument("--near-black", type=float, default=24.0)
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    d = pathlib.Path(a.frames)
    painted = load(d, "painted")
    if painted is None:
        raise SystemExit("no painted reference frame in %s" % d)

    if a.calibrate:
        base = load(d, "lit_base")
        if base is None:
            raise SystemExit("no lit_base frame to calibrate against")
        print("T9-0 published: lit mean 87.7, near-black 19.05%, >half lost 16.21%;"
              " painted mean 113.6, near-black 1.70%\n")
        for how in ("mean", "rec709"):
            lp, lb = luma(painted, how), luma(base, how)
            half = float((lb < 0.5 * lp).mean() * 100)
            print("  %-7s painted mean %6.2f   lit mean %6.2f   >half lost %5.2f%%"
                  % (how, lp.mean(), lb.mean(), half))
            for t in (16, 20, 24, 28, 32, 36, 40):
                print("      near-black <%2d : painted %5.2f%%   lit %5.2f%%"
                      % (t, (lp <= t).mean() * 100, (lb <= t).mean() * 100))
        return 0

    lp = luma(painted, a.luma)
    rep = {"luma": a.luma, "near_black_threshold": a.near_black,
           "painted": {"mean_luma": round(float(lp.mean()), 2),
                       "near_black_pct": round(float((lp <= a.near_black).mean() * 100), 2)}}
    prev = None
    print("%-18s %10s %12s %14s %s" % ("state", "mean luma", "near-black", ">half lost", ""))
    print("%-18s %10.2f %11.2f%% %14s" % ("painted (ref)", lp.mean(),
                                          (lp <= a.near_black).mean() * 100, "-"))
    for s in STATES:
        img = load(d, s)
        if img is None:
            continue
        l = luma(img, a.luma)
        r = {"mean_luma": round(float(l.mean()), 2),
             "near_black_pct": round(float((l <= a.near_black).mean() * 100), 2),
             "lost_over_half_pct": round(float((l < 0.5 * lp).mean() * 100), 2),
             "median_drop_on_lit_pixels": round(float(np.median((lp - l)[l > a.near_black])), 2)}
        rep[s] = r
        # deltas against lit_base, the state every other one is a change TO -- not against
        # the previous ROW, which pairs states that change two things at once
        delta = ""
        if s != "lit_base" and "lit_base" in rep:
            bb = rep["lit_base"]
            delta = "vs lit_base: mean %+.2f  near-black %+.2f pp" % (
                r["mean_luma"] - bb["mean_luma"], r["near_black_pct"] - bb["near_black_pct"])
        print("%-18s %10.2f %11.2f%% %13.2f%%  %s"
              % (s, r["mean_luma"], r["near_black_pct"], r["lost_over_half_pct"], delta))
        prev = r

    # attribution: each step against the one thing it changed
    if "lit_base" in rep:
        b = rep["lit_base"]
        for s, what in (("lit_albedo", "albedo plate alone"), ("lit_props", "3D props alone"),
                        ("lit_albedo_props", "albedo + 3D props")):
            if s in rep:
                rep.setdefault("attribution", {})[what] = {
                    "mean_luma": round(rep[s]["mean_luma"] - b["mean_luma"], 2),
                    "near_black_pp": round(rep[s]["near_black_pct"] - b["near_black_pct"], 2),
                    "lost_over_half_pp": round(rep[s]["lost_over_half_pct"] - b["lost_over_half_pct"], 2)}
        print("\nagainst lit_base (original plate, card props):")
        for k, v in rep.get("attribution", {}).items():
            print("  %-22s mean luma %+7.2f   near-black %+6.2f pp   >half lost %+6.2f pp"
                  % (k, v["mean_luma"], v["near_black_pp"], v["lost_over_half_pp"]))

    # him, in pixels: the delivered frame with and without him
    fin = load(d, "final_noshadow_knight") if (d / "t9b_bridge_final_noshadow_knight.png").exists() \
        else load(d, "lit_albedo_props")
    nk = load(d, "final_noshadow_noknight") if (d / "t9b_bridge_final_noshadow_noknight.png").exists() \
        else load(d, "final_noknight")
    if fin is not None and nk is not None:
        m = np.abs(fin.astype(np.int16) - nk.astype(np.int16)).max(-1) > 8
        ys, xs = np.nonzero(m)
        if len(ys):
            rep["figure_pixels"] = {"screen_px_tall": int(ys.max() - ys.min() + 1),
                                    "screen_px_wide": int(xs.max() - xs.min() + 1),
                                    "px": int(m.sum())}
            print("\nhim, measured from the frame: %d px tall, %d wide"
                  % (rep["figure_pixels"]["screen_px_tall"], rep["figure_pixels"]["screen_px_wide"]))
    out = pathlib.Path(a.out) if a.out else d / "t9_metrics.json"
    out.write_text(json.dumps(rep, indent=1) + "\n")
    print("-> %s" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
