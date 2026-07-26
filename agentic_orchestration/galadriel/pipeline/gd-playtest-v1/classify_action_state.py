#!/usr/bin/env python3
"""
Classify the player's Action-State value word per frame and reduce to episodes.

Input: the JSON emitted by player_action_state.py.

The value word can be visually contaminated by other entities' overlay lines
and by floating damage numerals that overlap it from the right. Classification
therefore matches only the LEFT-most columns of the word's ink profile, which
is where the contamination is not. Frames whose best match is below threshold
are emitted as UNREADABLE -- never guessed (D-2 discipline: mark, don't infer).
"""

import argparse
import json

import numpy as np

# Left-edge column count used for matching. Short enough to sit inside the
# shortest label ("Idle", ~27 px) and to avoid right-side overlap contamination.
NCOL = 22


def profile_from_sig(sig, width, ncol=NCOL):
    """Re-expand the stored 24-bin signature back onto a pixel grid and take
    the first `ncol` columns."""
    sig = np.asarray(sig, dtype=float)
    xs = np.linspace(0, width - 1, len(sig))
    grid = np.arange(width)
    full = np.interp(grid, xs, sig)
    if width < ncol:
        full = np.pad(full, (0, ncol - width))
    return full[:ncol]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-corr", type=float, default=0.90)
    args = ap.parse_args()

    rows = json.load(open(args.inp))
    ok = [r for r in rows if r.get("found") and "sig" in r]

    # Exemplars: harvested from the run itself by width class, then labelled by
    # human read of the native-resolution colour crop (galadriel, 2026-07-26).
    bands = {"Idle": (24, 31), "Move": (36, 42), "Attack": (44, 52)}
    exemplars = {}
    for name, (lo, hi) in bands.items():
        members = [r for r in ok if lo <= r["width"] <= hi]
        if not members:
            continue
        P = np.array([profile_from_sig(r["sig"], r["width"]) for r in members])
        exemplars[name] = np.median(P, axis=0)

    def classify(r):
        p = profile_from_sig(r["sig"], r["width"])
        best, bestc = None, -2.0
        for name, e in exemplars.items():
            if np.std(p) < 1e-6 or np.std(e) < 1e-6:
                continue
            c = float(np.corrcoef(p, e)[0, 1])
            if c > bestc:
                best, bestc = name, c
        return (best, bestc) if bestc >= args.min_corr else ("UNREADABLE", bestc)

    out = []
    for r in rows:
        rec = {"i": r["i"], "t": r["t"]}
        if r.get("found") and "sig" in r:
            lab, c = classify(r)
            rec["state"] = lab
            rec["corr"] = round(c, 3)
        else:
            rec["state"] = "NO_ID"
        out.append(rec)

    # Episode reduction: maximal runs of a single state. UNREADABLE / NO_ID
    # frames inside a run do not break it if the run resumes with the same
    # state within 4 frames (~67 ms) -- shorter than any animation.
    episodes = []
    cur = None
    gap = 0
    for rec in out:
        s = rec["state"]
        if s in ("UNREADABLE", "NO_ID"):
            gap += 1
            if cur and gap > 4:
                episodes.append(cur)
                cur = None
            continue
        if cur and cur["state"] == s:
            cur["t_end"] = rec["t"]
            cur["n"] += 1
            gap = 0
        else:
            if cur:
                episodes.append(cur)
            cur = {"state": s, "t_start": rec["t"], "t_end": rec["t"], "n": 1}
            gap = 0
    if cur:
        episodes.append(cur)

    for e in episodes:
        e["dur"] = round(e["t_end"] - e["t_start"], 4)

    json.dump({"frames": out, "episodes": episodes}, open(args.out, "w"))

    from collections import Counter
    cnt = Counter(r["state"] for r in out)
    print("frame states:", dict(cnt))
    for st in ("Attack", "Move", "Idle"):
        eps = [e for e in episodes if e["state"] == st]
        tot = sum(e["dur"] for e in eps)
        print(f"{st:10s} episodes={len(eps):3d}  total={tot:6.2f}s  "
              f"durs={[round(e['dur'],2) for e in eps]}")


if __name__ == "__main__":
    main()
