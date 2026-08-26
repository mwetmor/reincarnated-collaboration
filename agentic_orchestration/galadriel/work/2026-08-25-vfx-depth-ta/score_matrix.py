"""Turn out/ta_depth.json into the per-skill feature matrix.

⚑ PREREGISTERED. Every bar below is derived from out/synth_controls{2,3}.json --
the synthetic ground-truth arms -- and this file was written and committed
BEFORE the extraction run finished. No bar is fitted to a row's value.

Control anchors (positive / matched-null):
  F1 head_white_frac_p90        comet 0.539  | bar 0.000  smoke 0.003
  F2 val_slope_med              comet 0.393  | bar 0.015
     dsat = tail_sat - head_sat comet +0.345 | bar +0.021
  F3 head_tail_width_ratio_med  comet 0.746  | bar 0.944      << WEAK, 0.20 margin
     cv_width                   comet 0.283  | bar 0.305      << DISQUALIFIED (inverted)
  F4 sat_count_med              comet 26.0   | bar 7.0  scar 0.0
     sat_massfrac_p90           comet 0.208  | bar 0.030
     sat_dist_norm_p90          comet 1.84   | bar 4.01       << DISQUALIFIED (inverted)
  F5 halo_area_ratio_med        smoke 1.444  | bar 0.477      << scar 5.14 = BLOOM false-positive
     halo_softness_med          comet 8.77   | smoke 4.14     << DISQUALIFIED (inverted)
  F6a scar_over_control         scar 13886x  | scarnull 0.0
  F6b radial coherence          validated lens 0.51-0.99, refuses on null (first reading 2.3)
  F7 hf_p99_px / n_shake        shake 13.80 / 14 | pan(6px/fr) 0.000 / 0
"""
import json, math

D = json.load(open("out/ta_depth.json"))
U, P, A, N = "UNCERTAIN", "PRESENT", "ABSENT", "n/e"

def f(x, d=float("nan")):
    try:
        v = float(x)
        return v if math.isfinite(v) else d
    except (TypeError, ValueError):
        return d

def call_F1(s):
    h = f(s["F1_head"]["head_white_frac_p90"]); t = f(s["F1_head"]["tail_white_frac_p90"])
    lk = f(s["F1_head"]["lead_known_frac"], 0.0)
    if lk < 0.20: return U, "direction of travel unresolvable on %.0f%% of frames" % (lk*100)
    if not math.isfinite(h): return U, "no measurable core"
    if h >= 0.15 and h >= 3*max(t, 1e-6): return P, "head_white %.3f vs tail %.3f" % (h, t)
    if h < 0.02: return A, "head_white %.3f (null=0.000)" % h
    return U, "head_white %.3f between bars" % h

def call_F2(s):
    v = f(s["F2_gradient"]["val_slope_med"]); lk = f(s["F1_head"]["lead_known_frac"], 0.0)
    ds = f(s["F2_gradient"]["tail_sat_med"]) - f(s["F2_gradient"]["head_sat_med"])
    if lk < 0.20: return U, "direction unresolvable"
    if not math.isfinite(v) and not math.isfinite(ds): return U, "no measurable core"
    if (math.isfinite(v) and v >= 0.10) or (math.isfinite(ds) and ds >= 0.15):
        return P, "val_slope %+.3f, dsat %+.3f" % (v, ds)
    if (math.isfinite(v) and abs(v) < 0.03) and (math.isfinite(ds) and abs(ds) < 0.05):
        return A, "val_slope %+.3f, dsat %+.3f" % (v, ds)
    return U, "val_slope %+.3f, dsat %+.3f" % (v, ds)

def call_F3(s):
    r = f(s["F3_width"]["head_tail_width_ratio_med"]); lk = f(s["F1_head"]["lead_known_frac"], 0.0)
    if lk < 0.20 or not math.isfinite(r): return U, "direction unresolvable / no core"
    if r <= 0.85 or r >= 1.18: return P, "head/tail width %.3f (taper)" % r
    if 0.92 <= r <= 1.08: return A, "head/tail width %.3f (constant)" % r
    return U, "head/tail width %.3f between bars" % r

def call_F4(s):
    c = f(s["F4_sparks"]["sat_count_med"]); m = f(s["F4_sparks"]["sat_massfrac_p90"])
    if not math.isfinite(c): return U, "no components"
    if c >= 15 and m >= 0.10: return P, "%.0f satellites, massfrac %.3f" % (c, m)
    if c <= 3 and m < 0.03: return A, "%.0f satellites, massfrac %.3f" % (c, m)
    return U, "%.0f satellites, massfrac %.3f" % (c, m)

def call_F5(s):
    a = f(s["F5_smoke"]["halo_area_ratio_med"])
    if not math.isfinite(a): return U, "no halo band"
    if a >= 1.00: return P, "halo/core area %.2f" % a
    if a < 0.40: return A, "halo/core area %.2f" % a
    return U, "halo/core area %.2f" % a

def call_F6a(s):
    sc = s["F6a_scar"]
    if not sc: return N, "impact + 1.0 s lies outside the clip"
    fr = f(sc["scar_frac"]); ov = f(sc["scar_over_control"])
    if fr >= 0.005 and ov >= 3: return P, "scar %.4f of disc, %.0fx control" % (fr, ov)
    if fr < 0.001: return A, "scar %.4f" % fr
    return U, "scar %.4f, %.1fx control" % (fr, ov)

def call_F6b(s):
    i = s["F6b_impact_distortion"]; r = f(i["radial_near_at_impact"])
    if not math.isfinite(r): return U, "radial refused (zero-magnitude residual)"
    if r >= 0.35: return P, "radial %.3f at impact (lens sig 0.51-0.99)" % r
    if r < 0.10: return A, "radial %.3f at impact" % r
    return U, "radial %.3f at impact" % r

def call_F7(s):
    sh = s["F7_shake"]
    if not sh: return U, "camera unsolved"
    p = f(sh["hf_p99_px"]); n = sh["n_shake_frames"]
    if p >= 1.0 and n >= 3: return P, "hf_p99 %.2f px, %d spike frames" % (p, n)
    if p < 0.5: return A, "hf_p99 %.2f px (pan-null=0.00)" % p
    return U, "hf_p99 %.2f px, %d spikes" % (p, n)

FAM = [("F1 hot head", call_F1), ("F2 gradient", call_F2), ("F3 var width", call_F3),
       ("F4 sparks", call_F4), ("F5 smoke vol", call_F5), ("F6a scar", call_F6a),
       ("F6b impact-distort", call_F6b), ("F7 shake", call_F7)]

rows = {}
for row, d in D.items():
    if "error" in d: rows[row] = {"error": d["error"]}; continue
    s = d["summary"]
    r = {n: dict(zip(("call", "why"), fn(s))) for n, fn in FAM}
    ev = s["CV_timing"]["events"]; sp = s["CV_timing"]["spectrum"] or {}
    r["CV"] = {"cv": ev.get("cv_interval"), "events_per_s": ev.get("events_per_s"),
               "n_events": ev.get("n_events"), "mean_interval_s": ev.get("mean_interval_s"),
               "peak_over_median": sp.get("peak_over_median"),
               "dominant_hz": sp.get("dominant_hz"),
               "trip_flag": s["CV_timing"]["trip_flag"]}
    r["_impact_t"] = s["F6b_impact_distortion"]["impact_t_s"]
    r["_impact_frame"] = s["F6b_impact_distortion"]["impact_frame_idx"]
    r["_media"] = d["media"]; r["_frames"] = d["meta"]["n_frames_analysed"]
    r["_noise_mad"] = d["derived"]["noise_mad_luma"]
    rows[row] = r
json.dump(rows, open("out/feature_matrix.json", "w"), indent=2, default=str)

hdr = ["row"] + [n for n, _ in FAM] + ["CV", "ev/s", "trip"]
print("| " + " | ".join(hdr) + " |")
print("|" + "|".join(["---"]*len(hdr)) + "|")
SY = {"PRESENT": "P", "ABSENT": "A", "UNCERTAIN": "?", "n/e": "n/e"}
for row, r in rows.items():
    if "error" in r: print(f"| {row} | ERROR |"); continue
    cv = r["CV"]["cv"]
    print("| `%s` | " % row + " | ".join(SY[r[n]["call"]] for n, _ in FAM) +
          " | %s | %.2f | %s |" % ("%.3f" % cv if cv is not None else "—",
                                   r["CV"]["events_per_s"] or 0.0,
                                   "TRIP" if r["CV"]["trip_flag"] else "-"))
