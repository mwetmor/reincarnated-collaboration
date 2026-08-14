#!/usr/bin/env python3
"""
kc2_preroll_depth.py — SB-1 Cell CLK-2 firing #3, item A. THE NOTE-90 DIAGNOSTIC.

    python3 kc2_preroll_depth.py --preroll 60 --label "canon/on/full" \
        [--json OUT.json] a.raw.sha b.raw.sha c.raw.sha ...

⚑ WHY THIS EXISTS. FG-10 prunes the tick-frozen preroll and *then* compares, so
  it is structurally blind to the region where 100 % of KC2's observed run-to-run
  variance lives. Eleven consecutive passes were green post-prune while the
  pre-prune lists differed on nearly every one. NOTE-90: a gate that only records
  its own verdict records nothing about its margin.

  This reads the PRE-PRUNE per-frame digest lists of N passes of one leg and
  reports how DEEP into the preroll the run-to-run divergence reached. That
  number is the margin between a harmless transient and an escape into the
  certified span.

⚑ REPORTING-ONLY, AND THAT IS A DESIGN DECISION, NOT AN OVERSIGHT (CLK-2-2(3i)).
  Nothing here can turn a leg red. The gate's red condition stays exactly what it
  was — the measured span, digest-identical across passes — because a depth-based
  red would redden a harmless deep-preroll draw while the certified bytes still
  reproduce, and the escape that actually matters already reds the existing
  condition by definition.

⚑ LINE NUMBERING, STATED ONCE SO IT IS NOT TWO QUANTITIES WEARING ONE NAME
  (NOTE-82). `line1` is 1-INDEXED into the raw list (line 1 = the first frame the
  movie writer emitted); the preroll is lines 1..PREROLL. `index0` is the
  0-INDEXED frame number, i.e. the N in frame%08d.png. index0 = line1 - 1. The
  landing notes quote depth in line1 ("line 21 of 60"); the keep-frame filenames
  quote index0.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path


def read_list(p: Path) -> list[str]:
    return p.read_text().split()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lists", nargs="+", type=Path)
    ap.add_argument("--preroll", type=int, required=True)
    ap.add_argument("--label", default="leg")
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    names = [p.name for p in args.lists]
    runs = [read_list(p) for p in args.lists]
    lens = [len(r) for r in runs]
    if any(n == 0 for n in lens):
        print(f"FG10DEPTH label={args.label} status=EMPTY_LIST")
        return 2

    pairs = []
    preroll_diff: set[int] = set()      # 0-indexed
    overall_diff: set[int] = set()
    for (ia, a), (ib, b) in itertools.combinations(list(enumerate(runs)), 2):
        common = min(len(a), len(b))
        bad = [i for i in range(common) if a[i] != b[i]]
        pre = [i for i in bad if i < args.preroll]
        post = [i for i in bad if i >= args.preroll]
        preroll_diff.update(pre)
        overall_diff.update(bad)
        pairs.append({
            "a": names[ia], "b": names[ib],
            "compared_frames": common,
            "n_differ": len(bad),
            "preroll_n_differ": len(pre),
            "preroll_deepest_line1": (max(pre) + 1) if pre else None,
            "preroll_lines1": [i + 1 for i in pre],
            "measured_n_differ": len(post),
            "measured_first_index0": min(post) if post else None,
        })

    # ⚑ NOTE-72, CAUGHT BY THIS TOOL'S OWN CONTROL. With fewer than two passes
    #   there are no pairs, and "no divergence found" would be the same sentence
    #   the tool prints when it genuinely compared and found agreement. Those are
    #   two different verdicts and they must not share a line.
    measurable = len(runs) >= 2
    deepest_pre = (max(preroll_diff) + 1) if preroll_diff else None
    rep = {
        "label": args.label,
        "measurable": measurable,
        "preroll_frames": args.preroll,
        "n_passes": len(runs),
        "lists": names,
        "list_lengths": lens,
        "list_lengths_all_equal": len(set(lens)) == 1,
        # --- the standing diagnostic -------------------------------------
        "preroll_deepest_divergence_line1": deepest_pre,
        "preroll_margin_frames": ((args.preroll - deepest_pre) if deepest_pre else args.preroll)
        if measurable else None,
        "preroll_n_lines_that_ever_differ": len(preroll_diff),
        "preroll_lines_that_ever_differ": sorted(i + 1 for i in preroll_diff),
        # --- restated for the keep-frame path and for honesty ------------
        "overall_deepest_divergence_index0": (max(overall_diff) if overall_diff else None),
        "overall_first_divergence_index0": (min(overall_diff) if overall_diff else None),
        "measured_span_n_frames_that_ever_differ":
            len([i for i in overall_diff if i >= args.preroll]),
        "measured_span_identical": (not any(i >= args.preroll for i in overall_diff))
        if measurable else None,
        "pairs": pairs,
    }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(rep, indent=2) + "\n")

    # ⚑ NOTE-81: no %e, and nothing that reads as prose with a technical-looking
    #   middle. One human line, one machine line, both fully substituted.
    if not measurable:
        human = (f"    DEEPEST-PREROLL-DIVERGENCE: NOT MEASURABLE — {len(runs)} pass, no pairs "
                 f"to compare. This is not a green reading.")
    elif deepest_pre is None:
        human = (f"    DEEPEST-PREROLL-DIVERGENCE: NONE — all {args.preroll} preroll frames "
                 f"identical across {len(runs)} passes (margin {args.preroll} of {args.preroll})")
    else:
        human = (f"    DEEPEST-PREROLL-DIVERGENCE: line {deepest_pre} of {args.preroll} "
                 f"(margin {args.preroll - deepest_pre} frames to the measured span); "
                 f"{len(preroll_diff)} preroll lines ever differ")
    print(human)
    if measurable:
        print(f"    measured span: "
              f"{'IDENTICAL' if rep['measured_span_identical'] else str(rep['measured_span_n_frames_that_ever_differ']) + ' FRAMES DIFFER'}"
              f"   overall deepest differing index0: {rep['overall_deepest_divergence_index0']}")
    print("FG10DEPTH label=%s measurable=%s deepest_line1=%s margin=%s n_pre=%s measured_identical=%s "
          "overall_deepest_index0=%s overall_first_index0=%s" % (
              args.label,
              "yes" if measurable else "NO",
              deepest_pre if deepest_pre is not None else "none",
              rep["preroll_margin_frames"],
              len(preroll_diff),
              "yes" if rep["measured_span_identical"] else "no",
              rep["overall_deepest_divergence_index0"]
              if rep["overall_deepest_divergence_index0"] is not None else "none",
              rep["overall_first_divergence_index0"]
              if rep["overall_first_divergence_index0"] is not None else "none",
          ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
