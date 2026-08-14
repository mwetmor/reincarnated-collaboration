#!/usr/bin/env python3
"""kc2_clk2_align.py — SB-1 Cell CLK-2 item 1. THE DISCRIMINATOR.

    python3 kc2_clk2_align.py <probe-out-dir> <n-passes> <preroll>

WHY THIS TOOL EXISTS
--------------------
A2g-r's FG-10 leg 1 reported "3 distinct states, ALL 320 frames disagree
INCLUDING frame 0". That sentence has two mutually exclusive readings and the
gate cannot tell them apart:

  E1  AN INDEX SHIFT.  Two passes wrote a different number of frames before the
      shot began (a startup-frame-count difference), the preroll prune removed a
      fixed 60 from each, and the two lists are therefore MISALIGNED. Every
      index disagrees while every PICTURE is identical, one slot over.

  E2  A PIXEL DIFFERENCE.  The frames really are different pictures at the same
      index — a renderer first-use cost, the family CLK-1 convicted one level
      down.

E1 and E2 predict opposite things about ONE measurable quantity: the best
alignment offset between two disagreeing passes. This tool measures it. If the
best offset is non-zero and agreement at that offset is near-total, E1 is
convicted and no pixel forensics are needed at all. If the best offset is zero,
E1 is dead and the cell goes hunting in pixels with one hypothesis eliminated
for the price of arithmetic already on disk.

NOTE-82: every quantity below is printed with the name it was pre-registered
under, and no quantity wears two names.
"""
import sys
import os
import itertools
from collections import Counter


def read(path):
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return fh.read().split()


def best_offset(a, b, window=8):
    """Q3/Q4 — the shift k maximising agreement between a[n] and b[n+k]."""
    best = (0, -1)
    for k in range(-window, window + 1):
        hit = 0
        tot = 0
        for n in range(len(a)):
            m = n + k
            if 0 <= m < len(b):
                tot += 1
                if a[n] == b[m]:
                    hit += 1
        if tot and hit > best[1]:
            best = (k, hit)
    return best


def main():
    outdir, npass, preroll = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    raw = {p: read(f"{outdir}/pass-{p}.raw.sha") for p in range(1, npass + 1)}
    prn = {p: read(f"{outdir}/pass-{p}.sha") for p in range(1, npass + 1)}

    print("  Q1 frames_written_per_pass : "
          + "  ".join(f"p{p}={len(raw[p])}" for p in range(1, npass + 1)))
    print("  after-prune frame counts   : "
          + "  ".join(f"p{p}={len(prn[p])}" for p in range(1, npass + 1)))
    q1 = {len(raw[p]) for p in raw}
    print(f"  ⚑ Q1 IDENTICAL ACROSS PASSES: {'YES' if len(q1) == 1 else 'NO — ' + str(sorted(q1))}")

    # --- distinct states over the pruned (deliverable-aligned) lists ---------
    import hashlib
    states = {}
    for p in range(1, npass + 1):
        h = hashlib.sha256(("\n".join(prn[p]) + "\n").encode()).hexdigest()
        states.setdefault(h, []).append(p)
    print(f"\n  distinct states across {npass} passes: {len(states)}")
    for h, ps in states.items():
        print(f"    {h[:16]}…  passes {ps}")

    if len(states) == 1:
        print("\n  ⚑ VERDICT: leg reproduces. Nothing to align.")
        return 0

    # --- Q5 disagreeing indices at offset 0 ---------------------------------
    bad = sorted({i for a, b in itertools.combinations(prn.values(), 2)
                  for i in range(min(len(a), len(b))) if a[i] != b[i]})
    n_min = min(len(v) for v in prn.values())
    print(f"\n  Q5 disagreeing_frame_indices_at_offset_0: {len(bad)} of {n_min}"
          + (f"  (first {bad[:8]} … last {bad[-3:]})" if bad else ""))

    # --- Q3/Q4 THE DISCRIMINATOR --------------------------------------------
    print("\n  ⚑ Q3/Q4 ALIGNMENT TEST — E1 (index shift) vs E2 (pixel difference)")
    print("     pair        best_offset   matched/overlap   at_offset_0")
    e1_votes = 0
    for i, j in itertools.combinations(range(1, npass + 1), 2):
        a, b = prn[i], prn[j]
        k, hit = best_offset(a, b)
        overlap = sum(1 for n in range(len(a)) if 0 <= n + k < len(b))
        at0 = sum(1 for n in range(min(len(a), len(b))) if a[n] == b[n])
        frac = hit / overlap if overlap else 0.0
        flag = ""
        if k != 0 and frac > 0.99:
            flag = "  <-- E1: SAME PICTURES, SHIFTED"
            e1_votes += 1
        print(f"     p{i}/p{j}       {k:+d}            {hit}/{overlap} ({frac:.4f})"
              f"        {at0}/{min(len(a), len(b))}{flag}")

    # also run the test on the RAW (unpruned) lists — the prune itself could be
    # the thing that misaligns, and that distinction matters for the fix
    print("\n     …the same test on the RAW (unpruned) lists:")
    for i, j in itertools.combinations(range(1, npass + 1), 2):
        a, b = raw[i], raw[j]
        if not a or not b:
            continue
        k, hit = best_offset(a, b)
        overlap = sum(1 for n in range(len(a)) if 0 <= n + k < len(b))
        frac = hit / overlap if overlap else 0.0
        print(f"     p{i}/p{j} RAW   {k:+d}            {hit}/{overlap} ({frac:.4f})")

    print()
    if e1_votes:
        print("  ⚑ VERDICT: E1 CONVICTED on "
              f"{e1_votes} pair(s) — the disagreement is an INDEX SHIFT, not a pixel defect.")
    else:
        print("  ⚑ VERDICT: E1 DEAD — offset 0 is the best alignment. The frames are")
        print("     genuinely different pictures at the same index (E2).")

    # --- which frames to keep (charter rule d) ------------------------------
    reps = [ps[0] for ps in states.values()]
    idx = bad[0] if bad else 0
    print(f"\n  KEEP-FRAME PLAN (charter rule d): index {idx} from passes {reps}")
    print(f"     source file per pass: pass-N/frame{idx + preroll:08d}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
