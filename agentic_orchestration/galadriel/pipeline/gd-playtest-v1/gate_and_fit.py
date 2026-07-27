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

    # --- two-clock divergence + break location ---------------------------
    # d = play_time - pts. Within a slope-1 segment d is constant, but
    # `play_time` is rendered as INTEGER seconds and sampled at 2 fps, so the
    # measured d dithers over a ~1 s band. A raw threshold on consecutive
    # samples therefore invents breaks out of dither. d is smoothed with a
    # rolling median first, and only shifts above the dither floor are called.
    #
    # HONEST LIMIT: gandalf measured one real zone transition costing exactly
    # 1 s. A 1 s loss is INDISTINGUISHABLE from the dither band at this sample
    # rate. Breaks below BREAK_MIN_S are not located individually; they are
    # absorbed into the cumulative divergence curve, which remains exact at
    # its endpoints. Locating them needs native-rate sampling around candidate
    # transitions (a T-C ask), not a smarter filter on T-A.
    BREAK_MIN_S = 1.5
    MED_W = 15
    div = [(r["pts_s"], r["play_time"] - r["pts_s"])
           for r in rows if r.get("play_time") is not None]
    segments, breaks, divergence, clock_note = [], [], [], {}
    if div:
        pts_a = np.array([p for p, _ in div])
        d_a = np.array([d for _, d in div], dtype=float)
        k = min(MED_W, len(d_a) if len(d_a) % 2 else len(d_a) - 1)
        if k >= 3:
            pad = k // 2
            padded = np.pad(d_a, pad, mode="edge")
            med = np.array([np.median(padded[i:i + k]) for i in range(len(d_a))])
        else:
            med = d_a
        divergence = [{"pts_s": float(p), "divergence_s": round(float(m), 2)}
                      for p, m in zip(pts_a[::20], med[::20])]
        # Step detection: `d` is a monotone-decreasing STEP function plus
        # dither, so a break is a SUSTAINED drop, not a single-sample one.
        # Compare the median of a window BEFORE each candidate against the
        # median AFTER it. The earlier running-minimum tracker silently
        # followed the staircase down and reported zero breaks across a
        # divergence that demonstrably fell by ~78 s.
        W = 40                       # 20 s either side at 2 fps
        cand = [(float(np.median(med[i - W:i]) - np.median(med[i:i + W])), i)
                for i in range(W, len(med) - W)]
        cand = [c for c in cand if c[0] >= BREAK_MIN_S]
        cand.sort(key=lambda t: -t[0])
        chosen = []
        for drop, i in cand:                    # non-maximum suppression
            if all(abs(i - j) > W for _, j in chosen):
                chosen.append((drop, i))
        chosen.sort(key=lambda t: t[1])

        prev_i = 0
        for drop, i in chosen:
            segments.append({"pts_start": float(pts_a[prev_i]),
                             "pts_end": float(pts_a[i]),
                             "offset_s": round(float(np.median(med[prev_i:i])), 2)})
            breaks.append({"pts_s": float(pts_a[i]), "lost_s": round(drop, 2)})
            prev_i = i
        segments.append({"pts_start": float(pts_a[prev_i]),
                         "pts_end": float(pts_a[-1]),
                         "offset_s": round(float(np.median(med[prev_i:])), 2)})

        total_loss = float(med[0] - med[-1])
        located = float(sum(b["lost_s"] for b in breaks))
        clock_note = {
            "total_divergence_loss_s": round(total_loss, 2),
            "located_in_breaks_s": round(located, 2),
            "unlocated_residual_s": round(total_loss - located, 2),
            "break_floor_s": BREAK_MIN_S,
            "note": ("Losses below the floor are REAL but individually "
                     "unresolvable at 2 fps with an integer-second play_time. "
                     "They are absorbed into the cumulative divergence curve, "
                     "which stays exact at its endpoints. Resolving them needs "
                     "native-rate sampling around candidate transitions."),
        }

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
        "clock_accounting": clock_note,
        "divergence_curve": divergence,
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
    if clock_note:
        print(f"  divergence fell {clock_note['total_divergence_loss_s']}s total; "
              f"{clock_note['located_in_breaks_s']}s located in breaks, "
              f"{clock_note['unlocated_residual_s']}s below the "
              f"{clock_note['break_floor_s']}s floor")
    for b in breaks:
        print(f"    break at pts={b['pts_s']:.1f}s  play_time lost {b['lost_s']:.1f}s")
    print("deaths:", deaths)
    print("level-ups:", [(l["level"], l["play_time"]) for l in levels])


if __name__ == "__main__":
    main()
