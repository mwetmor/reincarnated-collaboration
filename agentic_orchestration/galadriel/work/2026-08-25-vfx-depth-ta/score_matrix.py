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
try:                                  # our own legs, same operators, same bars
    D.update(json.load(open("out/ours_depth.json")))
except OSError:
    pass
U, P, A, N = "UNCERTAIN", "PRESENT", "ABSENT", "n/e"

def f(x, d=float("nan")):
    try:
        v = float(x)
        return v if math.isfinite(v) else d
    except (TypeError, ValueError):
        return d


# ⚑ AXIS-CONDITIONING REFUSAL GATE — added AFTER the first five reference rows
# returned, and it makes the matrix claim LESS, not more.
#
# On every reference leg the head and the tail came back EQUAL to the third
# decimal (whirlwind 0.0123 / 0.0121; melee_strike 0.0732 / 0.0762; GTC 0.0057 /
# 0.0057) across five clips with wholly different content. That is not five
# measured absences; it is the signature of a split that is ARBITRARY -- and the
# reason is visible in the same table: the reference cores are nearly ROUND
# (elongation 1.48-1.83) because, with no fx-off control (sec 1.4), the largest
# connected component is a blob of effect + character + enemies rather than a
# directional effect. A principal axis on a round blob is ill-conditioned, so
# "head" and "tail" are two arbitrary ends of a meaningless line.
#
# The bar is taken from the CONTROLS, not from the data: both synthetic arms sat
# at elongation ~2.5 (comet 2.49, bar 2.45), which is the regime in which F1/F2/F3
# were validated at all. Below 2.0 the operator is outside its validated envelope
# and must REFUSE.
#
# Stated plainly because a post-hoc gate deserves the suspicion: this was added
# after seeing results, and it is CONSERVATIVE in direction -- it converts five
# ABSENT cells into NOT-EVALUABLE cells and issues no new PRESENT anywhere. A
# false ABSENT on "the references have no hot leading head" would have gone
# straight into a spec.
AXIS_MIN_ELONG = 2.0

def axis_conditioned(s):
    e = f(s["F3_width"]["elongation_med"])
    if not math.isfinite(e) or e < AXIS_MIN_ELONG:
        return False, "core is near-round (elongation %.2f < %.1f): principal axis ill-conditioned, head/tail split arbitrary" % (e if math.isfinite(e) else float('nan'), AXIS_MIN_ELONG)
    return True, ""

def call_F1(s):
    okc, why = axis_conditioned(s)
    if not okc: return N, why
    h = f(s["F1_head"]["head_white_frac_p90"]); t = f(s["F1_head"]["tail_white_frac_p90"])
    lk = f(s["F1_head"]["lead_known_frac"], 0.0)
    if lk < 0.20: return U, "direction of travel unresolvable on %.0f%% of frames" % (lk*100)
    if not math.isfinite(h): return U, "no measurable core"
    if h >= 0.15 and h >= 3*max(t, 1e-6): return P, "head_white %.3f vs tail %.3f" % (h, t)
    if h < 0.02: return A, "head_white %.3f (null=0.000)" % h
    return U, "head_white %.3f between bars" % h

def call_F2(s):
    okc, why = axis_conditioned(s)
    if not okc: return N, why
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
    okc, why = axis_conditioned(s)
    if not okc: return N, why
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
    fr = f(sc["scar_frac"]); ov = f(sc["scar_over_control"]); ct = f(sc["control_frac"])
    # ⚑ REFUSAL GATE, added when the FIRST real row came back. On the panning D3
    # whirlwind the operator's own PRE-EVENT control term read 0.717 -- 72% of the
    # disc "changed" between two frames that bracket no event at all. That is
    # integer-shift registration error over a 40-frame baseline on a camera moving
    # 5 px/frame, not a scar. The synthetic control read control_frac = 0.000. So
    # a control above 0.10 means the baseline is gone and the operator has no
    # signal left to report -- it must REFUSE, not return a ratio. Same shape as
    # the sec 5.6 dead-denominator gate: a statistic that does not evaluate is not
    # a statistic that evaluates to zero.
    if ct > 0.10: return N, "NOT EVALUABLE: pre-event control %.3f (pan residue swamps the baseline)" % ct
    if fr >= 0.005 and ov >= 3: return P, "scar %.4f of disc, %.0fx control" % (fr, ov)
    if fr < 0.001: return A, "scar %.4f" % fr
    return U, "scar %.4f, %.1fx control" % (fr, ov)

def call_F6b(s, ser):
    """⚑ SIGNED, from the per-frame series -- not from the summary.

    The summary reported |radial| via absmax, and the FIRST real row showed why
    that is unusable: the D3 whirlwind read near +0.317 and far +0.670 at impact.
    The validated discriminator (first reading sec 2.3) is a SIGN PATTERN -- a
    lens is near-POSITIVE / far-NEGATIVE, a camera dolly is the exact opposite --
    and taking an absolute value destroys precisely the term that separates a
    distortion field from a camera push. Reporting "distortion PRESENT" off an
    absolute value is the forgery the affine model was built to prevent, arriving
    one level up in the aggregation.
    """
    if ser is None: return U, "series unavailable"
    sm = [f(x, 0.0) for x in ser["spec_mass"]]
    if not sm: return U, "no series"
    k = max(range(len(sm)), key=lambda j: sm[j])
    lo, hi = max(k-3, 0), min(k+4, len(sm))
    nr = [f(x) for x in ser["radial_coh_near"]]; fr_ = [f(x) for x in ser["radial_coh_far"]]
    cand = [(abs(nr[j]), j) for j in range(lo, hi) if math.isfinite(nr[j])]
    if not cand: return U, "radial refused at impact (zero-magnitude residual)"
    j = max(cand)[1]
    near, far = nr[j], fr_[j]
    med = [v for v in nr if math.isfinite(v)]
    med = sorted(med)[len(med)//2] if med else float("nan")
    tag = "near %+.3f / far %+.3f (clip med %+.3f)" % (near, far, med)
    if abs(near) < 0.10: return A, tag
    if math.isfinite(far) and (near > 0) == (far > 0):
        return U, tag + " — SIGNS AGREE: cannot separate a lens from a camera push"
    if near >= 0.35 and math.isfinite(far) and far < 0:
        return P, tag + " — lens-consistent (validated sig 0.51-0.99)"
    return U, tag

def shake_localisation(s, ser):
    """Is the shake CONCENTRATED at the impact, or spread through the clip?

    A genuine impact quake is an impulse with a decay. A following camera over a
    3D scene manufactures high-frequency translation everywhere -- and my pan-null
    is a RIGID pan, which cannot model that. So localisation is the term that
    separates them, and without it an F7 PRESENT on a moving-camera clip is not
    reportable.
    """
    if ser is None: return float("nan"), float("nan")
    import numpy as np
    tx = np.array([f(x) for x in ser["cam_tx"]]); ty = np.array([f(x) for x in ser["cam_ty"]])
    sm = np.array([f(x, 0.0) for x in ser["spec_mass"]])
    g = np.isfinite(tx) & np.isfinite(ty)
    if g.sum() < 24: return float("nan"), float("nan")
    from scipy import ndimage as ndi
    hp = np.hypot(tx[g] - ndi.median_filter(tx[g], size=9, mode="nearest"),
                  ty[g] - ndi.median_filter(ty[g], size=9, mode="nearest"))
    base = float(np.median(hp)); mad = float(np.median(np.abs(hp - base))) or 1e-9
    bar = max(base + 6.0*mad, 0.5)
    spikes = np.nonzero(hp >= bar)[0]
    if spikes.size == 0: return 0.0, float("nan")
    k = int(np.argmax(sm[g])); win = 8   # +/- 8 frames @30fps ~ +/-0.27 s
    inwin = int(np.sum(np.abs(spikes - k) <= win))
    expected = spikes.size * (2*win+1) / len(hp)
    return float(inwin/spikes.size), float(inwin/max(expected, 1e-9))

def call_F7(s):
    sh = s["F7_shake"]
    if not sh: return U, "camera unsolved"
    p = f(sh["hf_p99_px"]); n = sh["n_shake_frames"]
    if p >= 1.0 and n >= 3: return P, "hf_p99 %.2f px, %d spike frames" % (p, n)
    if p < 0.5: return A, "hf_p99 %.2f px (pan-null=0.00)" % p
    return U, "hf_p99 %.2f px, %d spikes" % (p, n)

FAM = [("F1 hot head", call_F1), ("F2 gradient", call_F2), ("F3 var width", call_F3),
       ("F4 sparks", call_F4), ("F5 smoke vol", call_F5), ("F6a scar", call_F6a),
       ("F6b impact-distort", None), ("F7 shake", call_F7)]

rows = {}
for row, d in D.items():
    if "error" in d: rows[row] = {"error": d["error"]}; continue
    s = d["summary"]
    try:
        ser = json.load(open("out/series_%s.json" % row))
    except OSError:
        ser = None
    r = {n: dict(zip(("call", "why"), (fn(s) if fn else call_F6b(s, ser))))
         for n, fn in FAM}
    loc, enr = shake_localisation(s, ser)
    r["F7 shake"]["localisation"] = loc
    r["F7 shake"]["impact_enrichment"] = enr
    if r["F7 shake"]["call"] == P:
        cap = f(s["F7_shake"]["pan_mean_px"], 0.0)
        if cap > 0.5 and (not math.isfinite(enr) or enr < 2.0):
            r["F7 shake"]["call"] = U
            r["F7 shake"]["why"] += " — camera pans %.2f px/fr and spikes are NOT impact-concentrated (enrichment %.1fx); rigid pan-null cannot model a 3D tracking camera" % (cap, enr)
    sc = s["F4_sparks"]
    r["F4 sparks"]["capped"] = bool(f(sc.get("sat_count_med"), 0) >= 400)
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
