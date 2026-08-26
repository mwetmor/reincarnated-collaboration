#!/usr/bin/env python3
"""G-5 CONSUMABILITY CHECK — does the 3-D tracking-camera null actually load
into galadriel's F7 operator, and does the matched pair separate?

  python3 evidence/g5-consumability-check.py

⚑ WHAT THIS IS, AND WHAT IT IS NOT.

  IS:   evidence that the harness capability drax was asked for WORKS — the
        clips decode, `frame_forensics_depth.analyse_depth()` accepts them
        without modification, `F7_shake` comes back populated on every leg, and
        the authored-shake positive control separates from its matched null.
        That is a BUILDER verifying his own deliverable is consumable.

  IS NOT: the F7 floor. Naming "the reference-leg shake bar is X px" from this
        output would be the presentation seam writing a measurement seam's
        ruling — and worse, writing it from ONE ladder at ONE speed under ONE
        camera. The floor is galadriel's, off her own run, in her own note. The
        numbers below exist so she knows the instrument is worth pointing at
        something, not so she can skip pointing it.

⚑ AND THE LADDER IS NOT A SUBSTITUTE FOR THE REFERENCE LEGS EITHER. Every leg
  here is rendered at the ratified `player_lock` pose (pitch 52.95, fov_v 31.79,
  k=0.665). A reference gameplay clip has its own cam geometry; `--pitch`,
  `--fov` and `--plk` on the harness exist so that a later cell can re-render
  the null at a reference's approximate pose. Until that is done, the transfer
  of this floor to a reference leg is an ASSUMPTION and is named as one here.
"""

import json
import os
import sys

PIPELINE = os.path.expanduser(
    "~/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline")
HERE = os.path.dirname(os.path.abspath(__file__))
CAPTURE = os.path.dirname(HERE)

sys.path.insert(0, PIPELINE)
import frame_forensics_depth as F  # noqa: E402

LEGS = ["N0-flat", "N1-low", "N2-mid", "N3-high", "N4-high-spring", "P1-shake"]

KEYS = ["pan_mean_px", "hf_median_px", "hf_p99_px", "hf_max_px",
        "shake_bar_px", "n_shake_frames", "shake_frame_frac", "hf_to_pan_ratio"]

rows = []
for leg in LEGS:
    clip = os.path.join(CAPTURE, "g5-camnull-%s-1920x1080.mp4" % leg)
    if not os.path.exists(clip):
        print("MISSING %s" % clip)
        continue
    res = F.analyse_depth(clip, leg)
    shake = res["summary"]["F7_shake"]
    if shake is None:
        print("!!! %s — F7_shake came back None (fewer than 24 finite frames). "
              "The clip is NOT consumable and that is the finding." % leg)
        continue
    man_path = os.path.join(HERE, "g5-manifest-%s.json" % leg)
    man = json.load(open(man_path))
    gt = man["ground_truth"]
    rows.append({
        "leg": leg,
        "relief": man["params"]["relief"],
        "cam_mode": man["params"]["cam_mode"],
        "authored_shake_px": man["params"]["shake_px_analysis_at_subject"],
        "no_shake_authored": man["no_shake_authored"],
        "gt_true_motion_px_min_mean": gt["true_motion_px_min_mean"],
        "gt_true_motion_px_max_mean": gt["true_motion_px_max_mean"],
        "gt_parallax_spread_px_mean": gt["parallax_spread_px_mean"],
        "F7_shake": {k: shake[k] for k in KEYS if k in shake},
        "n_frames_analysed": res["meta"]["n_frames_analysed"],
    })

out = os.path.join(HERE, "g5-consumability-check.json")
with open(out, "w") as fh:
    json.dump({
        "what": "G-5 consumability check — NOT the F7 floor",
        "operator": ("frame_forensics_depth.analyse_depth(...)"
                 "['summary']['F7_shake'], unmodified"),
        "rows": rows,
    }, fh, indent=2)

hdr = ("%-16s %-7s %-9s %8s | %8s %8s | %9s %9s %8s %7s"
       % ("leg", "relief", "cam", "authored", "gt_min", "gt_spread",
          "hf_p99", "shake_bar", "n_spike", "pan"))
print(hdr)
print("-" * len(hdr))
for r in rows:
    s = r["F7_shake"]
    print("%-16s %-7s %-9s %8.2f | %8.3f %8.3f | %9.4f %9.4f %8d %7.3f"
          % (r["leg"], r["relief"], r["cam_mode"], r["authored_shake_px"],
             r["gt_true_motion_px_min_mean"], r["gt_parallax_spread_px_mean"],
             s["hf_p99_px"], s["shake_bar_px"], s["n_shake_frames"],
             s["pan_mean_px"]))
print()
print("json -> %s" % out)
print("REMINDER: this is a consumability receipt. The F7 floor is galadriel's "
      "to state from her own run.")
