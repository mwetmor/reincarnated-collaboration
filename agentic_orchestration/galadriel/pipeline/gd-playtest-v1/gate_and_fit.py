#!/usr/bin/env python3
"""
T-A stage 2: cross-field consistency gate, two-clock affine fit, and hard
segmentation-break location.

The gate (binding constraint from gandalf's verification note):

    No panel read is accepted on a single field. `kills`, `deaths` and
    `max_level` are monotonic non-decreasing; `play_time` is non-decreasing.
    Any sample violating monotonicity against its neighbours is REJECTED,
    not smoothed.

Rejection is implemented as a longest-non-decreasing-subsequence (LNDS) per
field: the maximal mutually-consistent set of samples is retained and every
sample outside it is marked rejected for that field. This is deterministic and
reproducible -- a second run on the same input yields the same rejection set --
and it maximises retained data without ever inventing a value.

Interpolation is deliberately NOT offered. A rejected field is emitted as null.
A missing sample is honest; a smoothed one poisons every rate derived from it.

Clocks (§3 ruling): `play_time` is the game-state clock and is the join key.
`pts_s` is the camera clock. Their difference is piecewise constant with
slope-1 segments; the breaks are zone transitions, where wallclock elapses that
`play_time` does not count.
"""

import argparse
import csv
import json

import numpy as np

MONOTONIC = ["play_time", "kills", "deaths", "max_level",
             "life_healed", "total_score"]
SKILL_KEYS = ["defaultkickattack", "defaultweaponattack", "onslaught",
              "werewolf1", "werewolf1_skill01_claws", "werewolf1_skill02_charge"]


def lnds_mask(vals):
    """Indices forming a longest non-decreasing subsequence. None values are
    excluded up front and reported as missing rather than rejected."""
    idx = [i for i, v in enumerate(vals) if v is not None]
    if not idx:
        return set()
    seq = [vals[i] for i in idx]
    n = len(seq)
    tails, tails_idx, prev = [], [], [-1] * n
    for i, v in enumerate(seq):
        lo, hi = 0, len(tails)
        while lo < hi:                      # upper bound -> non-decreasing
            mid = (lo + hi) // 2
            if tails[mid] <= v:
                lo = mid + 1
            else:
                hi = mid
        if lo > 0:
            prev[i] = tails_idx[lo - 1]
        if lo == len(tails):
            tails.append(v)
            tails_idx.append(i)
        else:
            tails[lo] = v
            tails_idx[lo] = i
    keep, k = set(), tails_idx[-1]
    while k != -1:
        keep.add(idx[k])
        k = prev[k]
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--out-summary", required=True)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.inp)]
    for r in rows:
        for k in SKILL_KEYS:
            s = r.get("skills", {}).get(k)
            r[k] = s["count"] if s else None
            r[k + "_conf"] = s["conf"] if s else 0.0

    fields = MONOTONIC + SKILL_KEYS
    keep = {f: lnds_mask([r.get(f) for r in rows]) for f in fields}

    stats = {}
    for f in fields:
        present = sum(1 for r in rows if r.get(f) is not None)
        stats[f] = {
            "present": present,
            "accepted": len(keep[f]),
            "rejected_nonmonotonic": present - len(keep[f]),
            "missing": len(rows) - present,
        }

    # gate applied
    for i, r in enumerate(rows):
        r["gate"] = "OK"
        bad = [f for f in fields if r.get(f) is not None and i not in keep[f]]
        for f in bad:
            r[f] = None
        if bad:
            r["gate"] = "REJECT:" + ",".join(bad)

    # --- two-clock affine fit -------------------------------------------
    div = [(r["pts_s"], r["play_time"] - r["pts_s"])
           for r in rows if r.get("play_time") is not None]
    segments, breaks = [], []
    if div:
        cur_d = div[0][1]
        seg_start = div[0][0]
        for pts, d in div[1:]:
            # play_time is integer seconds sampled at 2 fps, so the difference
            # dithers by +-1s within a segment; a real break is larger.
            if abs(d - cur_d) > 2.0:
                segments.append({"pts_start": seg_start, "pts_end": pts,
                                 "offset_s": round(cur_d, 2)})
                breaks.append({"pts_s": pts,
                               "lost_s": round(cur_d - d, 2)})
                cur_d = d
                seg_start = pts
            else:
                cur_d = 0.9 * cur_d + 0.1 * d
        segments.append({"pts_start": seg_start, "pts_end": div[-1][0],
                         "offset_s": round(cur_d, 2)})

    # --- hard breaks: deaths --------------------------------------------
    deaths = []
    prev = None
    for r in rows:
        d = r.get("deaths")
        if d is None:
            continue
        if prev is not None and d > prev:
            deaths.append({"deaths": d, "play_time": r["play_time"],
                           "pts_s": r["pts_s"]})
        prev = d

    levels = []
    prev = None
    for r in rows:
        v = r.get("max_level")
        if v is None:
            continue
        if prev is not None and v > prev:
            levels.append({"level": v, "play_time": r["play_time"],
                           "pts_s": r["pts_s"]})
        prev = v

    cols = (["i", "pts_s", "play_time", "gate", "L"] + MONOTONIC[1:]
            + ["health_potions", "mana_potions", "dps", "shield_block_chance"]
            + SKILL_KEYS)
    with open(args.out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    summary = {
        "n_samples": len(rows),
        "field_stats": stats,
        "clock_segments": segments,
        "clock_breaks_zone_transitions": breaks,
        "deaths": deaths,
        "level_ups": levels,
    }
    json.dump(summary, open(args.out_summary, "w"), indent=2)

    print(f"samples: {len(rows)}")
    for f in fields:
        s = stats[f]
        print(f"  {f:28s} present={s['present']:6d} accepted={s['accepted']:6d} "
              f"rejected={s['rejected_nonmonotonic']:5d} missing={s['missing']:6d}")
    print(f"clock segments: {len(segments)}  breaks: {len(breaks)}")
    for b in breaks:
        print(f"    break at pts={b['pts_s']:.1f}s  play_time lost {b['lost_s']:.1f}s")
    print("deaths:", deaths)
    print("level-ups:", [(l["level"], l["play_time"]) for l in levels])


if __name__ == "__main__":
    main()
