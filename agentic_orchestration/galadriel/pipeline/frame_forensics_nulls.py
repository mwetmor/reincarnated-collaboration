#!/usr/bin/env python3
"""
frame_forensics_nulls.py -- the two nulls that decide whether the headline is real.

The primary reading returns a very large gap between the reference and our
render on novelty-based series. Before that gap can be attributed to the
EFFECTS, two rival explanations have to be measured and subtracted, because
either one on its own is large enough to produce the whole thing.

  NULL 1 -- THE PAN NULL.  The reference's camera translates at a measured
      5.98 px/frame at 1280x720. Ours is measured at EXACTLY 0.000. Every series
      here is built on a motion-compensated local plate, and motion compensation
      is never perfect: integer shift rounding, resampler ringing, and genuine
      parallax in a 3D scene all leave residue that reads as novelty. A moving
      camera therefore manufactures novelty out of a STATIC WORLD.
      Test: pan our own clip at the reference's measured rate and re-measure. If
      the gap collapses, the instrument was reporting the camera.

  NULL 2 -- THE ENCODE NULL (transcode-null, in the main runner). The reference
      is a 4.4 Mbit/s 2012 VP6 encode; ours is a 13 Mbit/s h264. Compression
      noise is itself novelty.

⚑ WHY THIS FILE EXISTS AT ALL. The dispatch's refutation conditions include
  "this dispatch must not pre-commit to the conclusion that our renders lack
  depth." The single most likely way to violate that honestly-but-wrongly is to
  report a 100x+ novelty ratio that is mostly camera motion. The nulls are how
  that violation is prevented by measurement instead of by good intentions.
"""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame_forensics as ff   # noqa: E402
import frame_forensics_run as fr   # noqa: E402

import numpy as np

PAN_RATE_PX_PER_FRAME = 5.977   # MEASURED on the reference at 1280x720, not chosen
PAN_AMPLITUDE_PX = 300


def make_pan_null(src, dst, rate=PAN_RATE_PX_PER_FRAME, amp=PAN_AMPLITUDE_PX):
    """Crop a 1280x720 window out of our 1920x1080 render and translate it at the
    reference's measured rate.

    The path is a TRIANGLE wave, not a sinusoid, because a triangle has CONSTANT
    speed and the quantity being matched is speed. A sinusoid would spend most of
    its time slower than the reference and under-state the null.

    Direction is horizontal-only. The reference's motion is not purely
    horizontal, so this null is a LOWER BOUND on pan-induced novelty: a diagonal
    pan crosses more texture per frame than a horizontal one of the same speed.
    Under-stating the null is the conservative direction -- it can only make our
    render look WORSE, never better, so it cannot flatter us.
    """
    if os.path.exists(dst):
        return dst
    period = 4.0 * amp / rate
    x_expr = f"320+(abs(mod(n*{rate},{2*2*amp})-{2*amp})-{amp})"
    # ⚑ fps=30 MUST PRECEDE crop. The crop filter's `n` counts the frames it is
    #   HANDED, and the source is 60 fps. With `crop,fps` the pan advanced by
    #   n*rate on every SOURCE frame and the decimated output moved 2*rate --
    #   MEASURED at 11.999 px/frame against a 5.977 target, exactly 2x.
    #   A null that is twice as strong as the thing it is nulling is not a
    #   conservative null, it is a broken one: it would have "proved" the
    #   artefact dominates by inflating the artefact. Caught because the
    #   instrument REPORTS the camera translation it fitted rather than trusting
    #   the value that was requested -- the same NOTE-97 discipline drax applies
    #   to render dimensions (name what you GOT, never what you ASKED FOR).
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", src,
         "-vf", f"fps=30,crop=1280:720:x='{x_expr}':y=180",
         "-c:v", "libx264", "-crf", "12", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-an", dst], check=True)
    print(f"[pan-null] rate={rate} px/frame, amplitude=+/-{amp} px, "
          f"triangle period={period:.1f} frames")
    return dst


def main():
    out = {}
    pan = os.path.join(fr.MEDIA, "ours_melee_pan_null_1280x720.mp4")
    make_pan_null(fr.OURS, pan)

    legs = [
        ("O_static_baseline", fr.OURS, 30.0),
        ("O_PANNULL_at_reference_rate", pan, 30.0),
        ("R_reference", fr.REF, 30000 / 1001),
    ]
    for label, path, fps in legs:
        print(f"[null-leg] {label}", flush=True)
        r = ff.analyse(path, label, 1280, 720, fps)
        S = r.series
        nf = np.array(S["novel_frac"], dtype=float)
        ne = {k: float(np.median([v[1][k] for v in S["neff_sweep"]]))
              for k in ("2", "6", "12")}
        rb = np.array(S["resid_bg_median"], dtype=float)
        rcf = np.array(S["radial_coh_far"], dtype=float)
        # ⚑ radial coherence is only meaningful where there IS a residual to be
        #   coherent. Below the sub-pixel floor the direction of a ~0 vector is
        #   arbitrary and its mean is not an estimate of anything.
        gate = rb > 0.25
        out[label] = {
            "noise_mad": r.derived["noise_mad_luma"],
            "tau_novelty": r.derived["tau_novelty"],
            "tau_spec": r.derived["tau_spec"],
            "novel_frac_p50": float(np.percentile(nf, 50)),
            "novel_frac_p90": float(np.percentile(nf, 90)),
            "n_eff_median": ne,
            "cam_translation_px_per_frame":
                float(np.nanmedian(np.hypot(S["cam_tx"], S["cam_ty"]))),
            "resid_bg_median_px": float(np.nanmedian(rb)),
            "radial_coh_far_ALL": float(np.nanmean(rcf)),
            "radial_coh_far_GATED": float(np.nanmean(rcf[gate & np.isfinite(rcf)]))
                if (gate & np.isfinite(rcf)).sum() >= 8 else None,
            "n_frames_gated": int((gate & np.isfinite(rcf)).sum()),
            "n_frames_total": int(len(nf)),
        }
        print("   ", json.dumps(out[label]), flush=True)

    with open(os.path.join(fr.OUT, "nulls.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    b, p, r = (out["O_static_baseline"], out["O_PANNULL_at_reference_rate"],
               out["R_reference"])
    print("\n=== PAN NULL VERDICT INPUTS (no verdict rendered here) ===")
    print(f"novel_frac p50 : ours static {b['novel_frac_p50']:.5f}  "
          f"ours PANNED {p['novel_frac_p50']:.5f}  reference {r['novel_frac_p50']:.5f}")
    print(f"  content gap  |R - O|      = {abs(r['novel_frac_p50']-b['novel_frac_p50']):.5f}")
    print(f"  PAN artefact |O_pan - O|  = {abs(p['novel_frac_p50']-b['novel_frac_p50']):.5f}")
    print(f"  ratio content/pan         = "
          f"{abs(r['novel_frac_p50']-b['novel_frac_p50'])/max(abs(p['novel_frac_p50']-b['novel_frac_p50']),1e-9):.2f}")


if __name__ == "__main__":
    main()
