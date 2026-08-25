#!/usr/bin/env python3
"""
frame_forensics_run.py -- first reading, dispatch 2026-08-25 frame-forensics.

Legs:
  R   reference   D3 Whirlwind, Blizzard 2012 master, 1280x720 vp6f, 374 fr
  O   ours        Step-2 render (today), 1920x1080 h264, 60 fps
  O'  transcode-null: O pushed through R's degradation (downscale to R's
      native raster + re-encode at R's bitrate class)

THE TRANSCODE-NULL IS THE POINT OF THIS RUNNER.
    The dispatch asks whether a compressed 720p YouTube-class reference and a
    clean 1080p Godot render are comparable at all. That question cannot be
    answered by inspecting the two legs; it needs a third leg that differs from
    one of them ONLY by the encode gap. O' is that leg. For any series X:

        readable(X)  requires  |X(R) - X(O)|  >>  |X(O) - X(O')|

    If the encode gap moves a series as much as the content gap does, the series
    cannot carry the comparison and no number it produces should be reported as
    a difference between the effects. This is a comparability test with a
    measured denominator, not an opinion about compression.
"""

import json
import os
import resource
import subprocess
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame_forensics as ff   # noqa: E402

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "work", "2026-08-25-frame-forensics")
WORK = os.path.abspath(WORK)
MEDIA = os.path.join(WORK, "media")
OUT = os.path.join(WORK, "out")

REF = os.path.join(MEDIA, "whirlwind_d3_2012.flv")
GODOT = "/Users/admin/Games/reincarnated-godot/harness_logs"
OURS = os.path.join(GODOT, "mp4_review_2026-08-25_v3", "06_melee_combo_CATHEDRAL.mp4")
OURS_DASH = os.path.join(GODOT, "mp4_review_2026-08-25_v3", "01_dash_attack_CATHEDRAL.mp4")
WW7 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "captures", "2026-08-16-sb1-gate2-clip",
    "ww7-gate2-cadence-ab-plk0665-1920x1080.mp4")
WW7 = os.path.abspath(WW7)

NULL = os.path.join(MEDIA, "ours_melee_transcode_null_1280x720.mp4")


def make_transcode_null(src, dst):
    """Push our render through the reference's degradation.

    Reference measured profile (ffprobe, RT-4 and re-measured today):
        1280x720, 4,405,912 bit/s over 12.479 s, VP6F, 30000/1001 fps.
    We cannot encode VP6F with a modern ffmpeg and would not want to -- the aim
    is not codec cosplay, it is to impose a COMPARABLE RATE-DISTORTION BUDGET on
    the same raster. So: same raster, same fps, and h264 held to the reference's
    measured bitrate with a hard cap.
    """
    if os.path.exists(dst):
        return dst
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", src,
         "-vf", "scale=1280:720:flags=bicubic,fps=30000/1001",
         "-c:v", "libx264", "-b:v", "4405k", "-maxrate", "4405k",
         "-bufsize", "8810k", "-pix_fmt", "yuv420p", "-an", dst],
        check=True)
    return dst


def summarise(res: ff.ClipResult, fps: float) -> dict:
    S = res.series
    out = {"meta": res.meta, "derived": res.derived}

    band = np.array(S["band_frac"], dtype=float)
    novel = np.array(S["novel_frac"], dtype=float)
    active = novel > (np.nanmedian(novel) + 1e-9)
    if active.sum() < 8:
        active = novel > 0

    out["D1_detail_energy"] = {
        "band_labels": ["b0_finest_1px", "b1_2px", "b2_4px", "b3_8px",
                        "b4_16px", "b5_32px", "b6_residual_coarse"][:band.shape[1]],
        "band_frac_mean_all_frames": [round(float(v), 5) for v in np.nanmean(band, axis=0)],
        "band_frac_mean_active_frames": [round(float(v), 5)
                                         for v in np.nanmean(band[active], axis=0)],
        "fine_share_b0b1_active": round(float(np.nanmean(band[active][:, :2].sum(axis=1))), 5),
        "band_total_mean": round(float(np.nanmean(S["band_total"])), 6),
        "n_active_frames": int(active.sum()),
    }

    out["D2_colour"] = {
        "hue_circmean_mean": round(float(np.nanmean(S["hue_circmean"])), 5),
        "hue_circmean_std": round(float(np.nanstd(S["hue_circmean"])), 5),
        "hue_circvar_mean": round(float(np.nanmean(S["hue_circvar"])), 5),
        "sat_mean": round(float(np.nanmean(S["sat_mean"])), 5),
        "val_mean": round(float(np.nanmean(S["val_mean"])), 5),
        "spectrum_hue": ff.temporal_spectrum(np.array(S["hue_circmean"]), fps),
        "spectrum_sat": ff.temporal_spectrum(np.array(S["sat_mean"]), fps),
        "spectrum_val": ff.temporal_spectrum(np.array(S["val_mean"]), fps),
        "spectrum_novelfrac": ff.temporal_spectrum(novel, fps),
    }

    out["D3_intermittency"] = {
        "spec_frac_mean": round(float(np.nanmean(S["spec_frac"])), 7),
        "spec_frac_max": round(float(np.nanmax(S["spec_frac"])), 7),
        "spec_mass_mean": round(float(np.nanmean(S["spec_mass"])), 7),
        "peaks_spec_mass": ff.peak_intervals(S["spec_mass"], fps),
        "peaks_novel_frac": ff.peak_intervals(novel, fps),
        "spectrum_spec_mass": ff.temporal_spectrum(np.array(S["spec_mass"]), fps),
    }

    def A(k):
        return np.array(S[k], dtype=float)

    bgr, nrr = A("resid_bg_median"), A("resid_near_median")
    rcn, rcf = A("radial_coh_near"), A("radial_coh_far")
    ev = A("flow_tiles_evaluable")
    tx, ty, dv = A("cam_tx"), A("cam_ty"), A("cam_divergence")
    gmag = np.hypot(tx, ty)

    def q(a, p):
        a = a[np.isfinite(a)]
        return round(float(np.percentile(a, p)), 5) if a.size else None

    out["D4_flow"] = {
        "camera_translation_median_px_per_frame": round(float(np.nanmedian(gmag)), 4),
        "camera_translation_p95_px_per_frame": q(gmag, 95),
        "camera_divergence_median": round(float(np.nanmedian(dv)), 6),
        "camera_divergence_p95": q(dv, 95),
        "tiles_evaluable_mean": round(float(np.nanmean(ev)), 4),
        "resid_bg_median_px": round(float(np.nanmedian(bgr)), 4),
        "resid_bg_p95_px": q(bgr, 95),
        "resid_near_median_px": round(float(np.nanmedian(nrr)), 4),
        "resid_near_over_bg": round(float(np.nanmedian(nrr) / np.nanmedian(bgr)), 4)
        if np.isfinite(np.nanmedian(bgr)) and np.nanmedian(bgr) > 0 else None,
        # ---- THE S-4(ii) ANSWER LIVES HERE ----
        # radial coherence of the AFFINE-RESIDUAL background displacement about
        # the effect centroid. Camera zoom has already been removed by the
        # affine fit, so a non-zero far-field value cannot be the camera.
        "radial_coh_near_mean": round(float(np.nanmean(rcn)), 4),
        "radial_coh_near_sem": round(float(np.nanstd(rcn) /
                                           max(np.sqrt(np.isfinite(rcn).sum()), 1)), 4),
        "radial_coh_far_mean": round(float(np.nanmean(rcf)), 4),
        "radial_coh_far_sem": round(float(np.nanstd(rcf) /
                                          max(np.sqrt(np.isfinite(rcf).sum()), 1)), 4),
        "n_frames_radial_near_evaluable": int(np.isfinite(rcn).sum()),
        "n_frames_radial_far_evaluable": int(np.isfinite(rcf).sum()),
    }
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    make_transcode_null(OURS, NULL)

    legs = [
        ("R_reference_d3_whirlwind", REF, 30000 / 1001),
        ("O_ours_melee_combo_cathedral", OURS, 30.0),
        ("Oprime_transcode_null", NULL, 30000 / 1001),
        ("O60_ours_melee_combo_60fps", OURS, 60.0),
        ("W_ww7_arena_cadence", WW7, 30.0),
        ("O_ours_dash_attack_cathedral", OURS_DASH, 30.0),
    ]

    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "primary_raster": list(ff.PRIMARY), "legs": {}}

    for label, path, fps in legs:
        print(f"[leg] {label} @ {ff.PRIMARY} {fps:.3f}fps", flush=True)
        r = ff.analyse(path, label, ff.PRIMARY[0], ff.PRIMARY[1], fps)
        report["legs"][label] = summarise(r, fps)
        with open(os.path.join(OUT, f"series_{label}.json"), "w") as fh:
            json.dump({"meta": r.meta, "derived": r.derived,
                       "series": r.series}, fh)
        print(f"       frames={r.meta['n_frames_analysed']} "
              f"rss={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.0f}MB",
              flush=True)

    # ---- RESOLUTION LADDER: is any of this portable across raster? ----------
    print("[ladder] running resolution ladder", flush=True)
    ladder = {}
    for label, path, fps in [("R_reference_d3_whirlwind", REF, 30000 / 1001),
                             ("O_ours_melee_combo_cathedral", OURS, 30.0)]:
        ladder[label] = {}
        for (w, h) in ff.LADDER:
            r = ff.analyse(path, label, w, h, fps)
            s = summarise(r, fps)
            ladder[label][f"{w}x{h}"] = {
                "D1_fine_share_b0b1_active": s["D1_detail_energy"]["fine_share_b0b1_active"],
                "D1_band_frac_active": s["D1_detail_energy"]["band_frac_mean_active_frames"],
                "D3_spec_frac_mean": s["D3_intermittency"]["spec_frac_mean"],
                "D3_events_per_s": s["D3_intermittency"]["peaks_spec_mass"]["events_per_s"],
                "D2_hue_circmean": s["D2_colour"]["hue_circmean_mean"],
                "D2_sat_mean": s["D2_colour"]["sat_mean"],
                "D4_resid_bg_median_px": s["D4_flow"]["resid_bg_median_px"],
                "D4_radial_coh_far": s["D4_flow"]["radial_coh_far_mean"],
                "D4_tiles_evaluable": s["D4_flow"]["tiles_evaluable_mean"],
                "derived_tau_spec": r.derived["tau_spec"],
                "derived_noise_mad": r.derived["noise_mad_luma"],
            }
            print(f"       {label} {w}x{h} done", flush=True)
    report["resolution_ladder"] = ladder
    report["wall_s"] = round(time.time() - t0, 1)
    report["peak_rss_mb"] = round(
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)

    with open(os.path.join(OUT, "reading.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps({k: report["legs"][k]["D1_detail_energy"]
                      for k in report["legs"]}, indent=2))
    print("wall", report["wall_s"], "rss_mb", report["peak_rss_mb"])


if __name__ == "__main__":
    main()
