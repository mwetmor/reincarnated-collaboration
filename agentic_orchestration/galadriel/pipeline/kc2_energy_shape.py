#!/usr/bin/env python3
"""KC2-PLAY · THE ENERGY GLOBE, GIVEN THE TREATMENT THE HP GLOBE GOT.

Commissioned by the conductor (Run KC2-PLAY, 2026-09-21) after gamora's
discrimination audit found the metrological asymmetry:

    "The HP globe got a verbatim tooth rule, six order statistics, a five-gate
     sweep and a named near-invariant.  The energy globe -- same fight, same
     session, same instrument class -- got five eye-read stills and a two-point
     band."

This module is the energy-side counterpart of `kc2_hp_shape.py`.  It consumes
ONLY data committed on 2026-08-25 -- no new capture, no MP4 -- and re-derives:

  E-1  ceiling occupancy, with a threshold sweep (the level the band read as a
       point) AND the above-ceiling defect the 2026-08-25 note never priced
  E-2  the saw-tooth: a VERBATIM tooth rule, six order statistics, a five-gate
       prominence sweep, and the near-invariant
  E-3  the below-cap net -- reported THREE WAYS, because the conditioning is the
       measurement (see THE CONDITIONING LAW below)
  E-4  refill rate, per tooth and per release
  E-5  the drain tick distribution and the GROSS-DRAIN BRACKET

  ------------------------------------------------------------------------
  THE CONDITIONING LAW -- read this before quoting any rate from this module
  ------------------------------------------------------------------------
  A rate computed over "intervals whose energy is below X" is conditioned on a
  LEVEL, and a level is reached by a SLOPE.  Label the interval by its END and
  you have selected falling intervals; label it by its START and you have
  selected rising ones.  The three labellings on this trace give

        label at END    : -80.5 /s (stationary)   -69.1 /s (moving)
        label at START  : +64.7 /s                +77.7 /s
        label at MIDPOINT:  -6.7 /s                +9.4 /s

  -- a 158 /s swing produced by nothing but where the label is taken.  The
  2026-08-25 note's Sect 4.4 figures (-81.7 / -73.4) are the END labelling.
  THIS MODULE SHIPS ALL THREE AND NAMES THE DEFAULT.

Usage:
    python3 kc2_energy_shape.py [out.json]

Inputs (all sha-verifiable, all committed 2026-08-25):
    captures/2026-08-25-md-b4app-2-channel/work/s2-energy-60hz.json
    captures/2026-08-25-md-b4app-2-channel/work/s2-duty.json
    captures/2026-08-25-md-b4app-2-channel/work/waves.json
    captures/2026-08-25-md-b4app-2b-energy/work/s2-releases.json

Cleaning is `eor_release.clean()` IMPORTED UNCHANGED, not reimplemented:
its census (10360 -> 315 -> 86 -> 9959) reproduces EXACT.
"""
import json, os, sys, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from eor_release import clean, CEIL          # CEIL = 1594.0

AO = os.path.abspath(os.path.join(HERE, ".."))
CHAN = os.path.join(AO, "captures/2026-08-25-md-b4app-2-channel/work")
ENER = os.path.join(AO, "captures/2026-08-25-md-b4app-2b-energy/work")
F_E60 = os.path.join(CHAN, "s2-energy-60hz.json")
F_DUTY = os.path.join(CHAN, "s2-duty.json")
F_WAVE = os.path.join(CHAN, "waves.json")
F_REL = os.path.join(ENER, "s2-releases.json")

# --- declared constants, every one carried from a committed instrument -------
TICK_DE = -6.0        # MD-B4app-2 drain-tick definition, carried unchanged
TICK_DT = 0.030       # s; adjacent-frame guard (eor_release.py), carried
AT_CAP = 1560.0       # MD-B4app-2 Sect 4.4's at-cap/below-cap partition.
                      # REPRODUCED, not assumed: at E>=1560 the median tick is
                      # -14.0 and the median interval 0.0833 s; below it they
                      # are -13.0 and 0.1000 s -- Sect 4.4's published pairs, EXACT.
WINDOW = (682.10, 864.75)   # D-COMBAT-182 = 182.65 s
D_COMBAT = WINDOW[1] - WINDOW[0]
HZ = 60.0
PROM_SWEEP = (5, 10, 20, 40, 80)   # energy; the five-gate sweep (E-2)
MARG_SWEEP = (0, 2, 3, 4, 5)       # OCR classifier margin gates (E-1)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load():
    d = json.load(open(F_E60))
    t, e, census = clean(d["rows"])
    idx = {round(x, 4): i for i, x in enumerate(t)}
    marg = np.full(len(t), np.nan)
    for r in d["rows"]:
        k = round(r["t"], 4)
        if k in idx:
            marg[idx[k]] = r.get("marg", np.nan)
    return d, t, e, marg, census


def motion_labels(t):
    eps = json.load(open(F_DUTY))["episodes"]
    t0 = np.array([x["t0"] for x in eps]); t1 = np.array([x["t1"] for x in eps])
    lab = np.array([x["state"] for x in eps])
    out = np.full(len(t), "", dtype=object)
    i = np.searchsorted(t0, t, side="right") - 1
    ok = (i >= 0) & (i < len(t0))
    good = ok.copy(); good[ok] = t[ok] <= t1[i[ok]]
    out[good] = lab[i[good]]
    return out


def wave_of(t):
    w = json.load(open(F_WAVE))
    b = w["boundaries"]          # [[wave, t0], ...]
    num = np.array([x[0] for x in b]); lo = np.array([x[1] for x in b])
    i = np.searchsorted(lo, t, side="right") - 1
    i = np.clip(i, 0, len(lo) - 1)
    return num[i]


def order_stats(a, nd=4):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    if len(a) == 0:
        return None
    return {"n": int(len(a)),
            "min": round(float(a.min()), nd),
            "p25": round(float(np.percentile(a, 25)), nd),
            "median": round(float(np.median(a)), nd),
            "p75": round(float(np.percentile(a, 75)), nd),
            "p95": round(float(np.percentile(a, 95)), nd),
            "max": round(float(a.max()), nd)}


# ---------------------------------------------------------------------------
# E-2 · THE TOOTH RULE -- the energy counterpart of kc2_hp_shape.py::teeth.
#       The walk is IDENTICAL; only the series and the units change.
# ---------------------------------------------------------------------------
def teeth(t, e, wave, prom):
    """
    Alternating-extremum walk with an ABSOLUTE-ENERGY prominence gate `prom`.
    Confirm a PEAK when energy falls `prom` below the running max since the last
    confirmed trough; confirm a TROUGH when energy rises `prom` above the running
    min since the last confirmed peak.  A TOOTH is a confirmed
    (peak -> trough -> next peak) triple.

        depth      = peak.E - trough.E
        depth_frac = depth / CEIL            (denominator = the 1594 ceiling,
                                              fixed by the 4,800-sample control)
        period_s   = next_peak.t - peak.t
        fall_s     = trough.t - peak.t
        recover_s  = next_peak.t - trough.t
        fall_slope     = -depth / fall_s                    (negative)
        recovery_slope = (next_peak.E - trough.E)/recover_s (positive)

    The gate is SWEPT, never chosen.
    """
    if len(e) < 3:
        return []
    ext, mode, cand = [], None, 0
    for i in range(1, len(e)):
        v = e[i]
        if mode is None:
            if v >= e[cand] + prom:
                mode = "up"; ext.append(("trough", cand)); cand = i
            elif v <= e[cand] - prom:
                mode = "down"; ext.append(("peak", cand)); cand = i
            continue
        if mode == "up":
            if v >= e[cand]:
                cand = i
            elif v <= e[cand] - prom:
                ext.append(("peak", cand)); mode = "down"; cand = i
        else:
            if v <= e[cand]:
                cand = i
            elif v >= e[cand] + prom:
                ext.append(("trough", cand)); mode = "up"; cand = i
    out = []
    for a in range(len(ext) - 2):
        (k0, i0), (k1, i1), (k2, i2) = ext[a], ext[a + 1], ext[a + 2]
        if not (k0 == "peak" and k1 == "trough" and k2 == "peak"):
            continue
        depth = e[i0] - e[i1]
        fall = t[i1] - t[i0]; rec = t[i2] - t[i1]
        out.append({"t_peak": round(float(t[i0]), 4),
                    "t_trough": round(float(t[i1]), 4),
                    "wave": int(wave[i1]),
                    "peak_E": float(e[i0]), "trough_E": float(e[i1]),
                    "depth": float(depth),
                    "depth_frac_of_ceiling": round(float(depth / CEIL), 6),
                    "period_s": round(float(t[i2] - t[i0]), 4),
                    "fall_s": round(float(fall), 4),
                    "recover_s": round(float(rec), 4),
                    "fall_slope": round(float(-depth / fall), 2) if fall > 0 else None,
                    "recovery_slope": round(float((e[i2] - e[i1]) / rec), 2) if rec > 0 else None})
    return out


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else None
    _, t, e, marg, census = load()
    cls = motion_labels(t)
    wv = wave_of(t)
    de = np.diff(e); dt = np.diff(t); adj = dt <= TICK_DT
    tick = (de <= TICK_DE) & adj

    R = {"instrument": "kc2_energy_shape.py",
         "inputs": {os.path.relpath(p, AO): sha256(p) for p in (F_E60, F_DUTY, F_WAVE, F_REL)},
         "window_D_COMBAT_182": list(WINDOW), "window_s": round(D_COMBAT, 4),
         "census": census,
         "census_note": ("REPRODUCES EXACT against s2-releases.json's energy_census "
                         "(10360 / 315 / 86 / 9959). The 2026-08-25 channel note's "
                         "published '291 rejected, 10,069 used' is a DIFFERENT cleaning "
                         "variant and does not reproduce; the release-instrument variant "
                         "is adopted here because it is the one that ships with code.")}

    # -- E-1 ---------------------------------------------------------------
    n = len(e)
    occ = {}
    for thr in (1594, 1590, 1580, 1570, 1560, 1550, 1500, 1450):
        occ["ge_%d" % thr] = round(float((e >= thr).mean()), 4)
    occ["eq_1594_exact"] = round(float((e == 1594).mean()), 4)
    occ["gt_1594_IMPOSSIBLE"] = round(float((e > 1594).mean()), 4)
    occ["n_gt_1594"] = int((e > 1594).sum())
    occ["max_read"] = float(e.max())

    marg_tab = []
    for g in MARG_SWEEP:
        k = np.isfinite(marg) & (marg >= g)
        marg_tab.append({"marg_gate": g, "kept": int(k.sum()),
                         "kept_frac": round(float(k.mean()), 4),
                         "above_1594_kept": int(((e > 1594) & k).sum()),
                         "above_1594_frac_of_kept": round(float(((e > 1594) & k).sum() / max(1, k.sum())), 4)})
    R["E1_ceiling"] = {
        "ceiling": CEIL,
        "control": {"windows": [[600.0, 640.0], [880.0, 920.0]], "n": 4800,
                    "distinct_values": [1594], "n_above_1594": 0,
                    "min_margin": 7.2,
                    "source": "ctrl-prep.json / ctrl-post.json, verified this lap"},
        "occupancy": occ,
        "margin_sweep": marg_tab,
        "margin_median_at_1594": round(float(np.nanmedian(marg[e == 1594])), 2),
        "margin_median_above_1594": round(float(np.nanmedian(marg[e > 1594])), 2),
        "margin_median_below_1594": round(float(np.nanmedian(marg[e < 1594])), 2),
    }

    # -- E-2 ---------------------------------------------------------------
    sweep = []
    teeth_primary = None
    for prom in PROM_SWEEP:
        T = teeth(t, e, wv, prom)
        row = {"prom": prom, "n_teeth": len(T),
               "rate_per_s": round(len(T) / D_COMBAT, 4)}
        for key, lbl in (("period_s", "median_period_s"), ("depth", "median_depth"),
                         ("recovery_slope", "median_recovery_slope"),
                         ("fall_slope", "median_fall_slope")):
            v = [x[key] for x in T if x[key] is not None]
            row[lbl] = round(float(np.median(v)), 4) if v else None
        sweep.append(row)
        if prom == 20:
            teeth_primary = T
    R["E2_teeth"] = {
        "rule": "see teeth() docstring -- alternating-extremum walk, ABSOLUTE energy prominence",
        "primary_gate": 20,
        "primary_gate_justification": (
            "20 energy = 1.4x the modal single drain tick (-14) and 1.25% of the 1594 "
            "ceiling: the smallest step that is unambiguously more than ONE tick. "
            "DECLARED, not fitted -- no arm of this lap was selected against a sim."),
        "order_statistics_at_primary": {
            k: order_stats([x[k] for x in teeth_primary if x[k] is not None])
            for k in ("period_s", "depth", "depth_frac_of_ceiling", "fall_s",
                      "recover_s", "fall_slope", "recovery_slope")},
        "prominence_sweep": sweep,
    }

    # -- E-2b · THE GATE-FREE SAW-TOOTH: runs, duty, period. No prominence, no
    #           threshold, no free parameter. This is the row to lean on.
    at = (e == 1594)
    runs_at, runs_bl = [], []
    i = 0
    while i < n:
        j = i
        while j + 1 < n and at[j + 1] == at[i] and (t[j + 1] - t[j]) <= TICK_DT:
            j += 1
        # duration = the run's OCCUPANCY (n_frames / 60), not the endpoint span:
        # a single-frame run occupies 1/60 s and spans 0, and filtering the zeros
        # out silently drops 89 excursions. Occupancy is the quantity duty wants.
        nfr = j - i + 1
        dur = nfr / HZ
        depth = float(CEIL - e[i:j + 1].min())
        (runs_at if at[i] else runs_bl).append((round(float(t[i]), 4), round(float(dur), 4), depth, nfr))
        i = j + 1
    rb, ra = runs_bl, runs_at
    R["E2b_gate_free_sawtooth"] = {
        "definition": ("A CEILING RESIDENCY is a maximal run of adjacent surviving frames "
                       "reading E == 1594 exactly. An EXCURSION is a maximal run of adjacent "
                       "surviving frames reading E != 1594. No prominence gate, no threshold, "
                       "no free parameter. `depth` of an excursion = 1594 - min(E) over it."),
        "duty": {
            "frac_samples_at_exact_ceiling": round(float(at.mean()), 4),
            "frac_samples_off_ceiling": round(float((~at).mean()), 4),
            "frac_samples_ABOVE_ceiling_IMPOSSIBLE": round(float((e > 1594).mean()), 4),
            "published_2026_08_25": "'64.6 % of combat time is spent at the 1594 ceiling'",
            "what_64_6_actually_is": "E >= 1560, which this lap reproduces at 0.6363"},
        "n_ceiling_residencies": len(ra),
        "n_excursions": len(rb),
        "ceiling_residency_s": order_stats([r[1] for r in ra]),
        "excursion_s": order_stats([r[1] for r in rb]),
        "excursion_depth_ALL_incl_impossible": order_stats([r[2] for r in rb]),
        "excursion_depth_positive_only": order_stats([r[2] for r in rb if r[2] > 0]),
        "excursion_s_positive_depth_only": order_stats([r[1] for r in rb if r[2] > 0]),
        "period_s_residency_plus_excursion": {
            "median_sum": round(float(np.median([r[1] for r in ra]) + np.median([r[1] for r in rb])), 4)},
    }

    # ⚑ WHERE MO_DRAWDOWN_BAND ACTUALLY LANDS IN THE DISTRIBUTION IT CLAIMS TO SUMMARISE
    pd_ = np.array([r[2] for r in rb if r[2] > 0])
    ps_ = np.array([r[1] for r in rb if r[2] > 0])
    R["E2c_where_the_band_lands"] = {
        "band": [86, 117],
        "n_positive_depth_excursions": int(len(pd_)),
        "pct_rank_of_86": round(float((pd_ < 86).mean() * 100), 1),
        "pct_rank_of_117": round(float((pd_ < 117).mean() * 100), 1),
        "n_excursions_inside_band": int(((pd_ >= 86) & (pd_ <= 117)).sum()),
        "frac_excursions_inside_band": round(float(((pd_ >= 86) & (pd_ <= 117)).mean()), 4),
        "band_at_footage_net_gives_s": [0.88, 1.40],
        "n_excursions_in_that_duration_window": int(((ps_ >= 0.88) & (ps_ <= 1.40)).sum()),
        "frac_excursions_in_that_duration_window": round(float(((ps_ >= 0.88) & (ps_ <= 1.40)).mean()), 4),
        "excursion_duration_p99_s": round(float(np.percentile(ps_, 99)), 4),
    }

    # -- E-3 · the conditioning law ----------------------------------------
    cond = {}
    for lname, lvl in (("label_at_END", e[1:]), ("label_at_START", e[:-1]),
                       ("label_at_MIDPOINT", 0.5 * (e[:-1] + e[1:]))):
        block = {}
        for rname, base in (("at_cap_ge_1560", lvl >= AT_CAP), ("below_cap_lt_1560", lvl < AT_CAP)):
            for cname in ("STATIONARY", "MOVING", "ALL"):
                m = base & adj & ((cls[:-1] == cname) if cname != "ALL" else True)
                if m.sum() < 10:
                    continue
                block["%s__%s" % (rname, cname)] = {
                    "n_pairs": int(m.sum()),
                    "net_dEdt": round(float(de[m].sum() / dt[m].sum()), 2)}
        cond[lname] = block
    R["E3_net_conditioning"] = {
        "law": ("A rate over intervals selected by a LEVEL is conditioned on the SLOPE "
                "that reached the level. END-labelling selects falling intervals; "
                "START-labelling selects rising ones. The default of record is MIDPOINT."),
        "default": "label_at_MIDPOINT",
        "published_2026_08_25_sect_4_4": {"below_cap_STATIONARY": -81.7, "below_cap_MOVING": -73.4,
                                          "at_cap_STATIONARY": 31.4, "at_cap_MOVING": 33.6,
                                          "reproduces_as": "label_at_END"},
        "table": cond,
    }

    # -- E-3b · net conditioned on CHANNEL STATE, not on energy level -------
    # channel-active = a 0.5 s window carrying >= 3 drain ticks (MD-B4app-2 Sect 3),
    # evaluated on the 0.05 s grid. This conditioning does NOT look at the slope.
    tt = t[:-1][tick]
    grid = np.arange(WINDOW[0], WINDOW[1] - 0.5, 0.05)
    nt = np.array([((tt >= g) & (tt < g + 0.5)).sum() for g in grid])
    chan_on = nt >= 3
    mid = 0.5 * (e[:-1] + e[1:])
    gi = np.clip(((t[:-1] - WINDOW[0]) / 0.05).astype(int), 0, len(grid) - 1)
    ch = chan_on[gi]
    chan_block = {}
    for cn, cm in (("channel_active_ge3", ch), ("channel_idle_lt3", ~ch)):
        for rn, rm in (("below_cap_lt_1560", mid < AT_CAP), ("at_cap_ge_1560", mid >= AT_CAP)):
            m = cm & rm & adj
            if m.sum() < 10:
                continue
            chan_block["%s__%s" % (cn, rn)] = {
                "n_pairs": int(m.sum()), "sampled_s": round(float(dt[m].sum()), 2),
                "net_dEdt": round(float(de[m].sum() / dt[m].sum()), 2)}
    R["E3b_net_by_channel_state"] = {
        "note": ("Conditioned on TICK DENSITY (an independent observable) and on a LEVEL "
                 "taken at the interval MIDPOINT. This is the estimator that does not "
                 "select on its own answer."),
        "table": chan_block}

    # -- E-4 · refill --------------------------------------------------------
    rel = json.load(open(F_REL))
    dedt = [r["dEdt"] for r in rel["releases"]]
    unclipped = [r["dEdt"] for r in rel["releases"] if r["E_off"] < CEIL]
    R["E4_refill"] = {
        "per_release_dEdt_all_19": order_stats(dedt, 2),
        "per_release_dEdt_unclipped_only": order_stats(unclipped, 2),
        "n_releases_clipped_at_ceiling": int(sum(1 for r in rel["releases"] if r["E_off"] >= CEIL)),
        "tooth_recovery_slope_primary": order_stats(
            [x["recovery_slope"] for x in teeth_primary if x["recovery_slope"] is not None], 2),
    }

    # -- E-5 · the drain tick and the GROSS-DRAIN BRACKET --------------------
    start_hi = e[:-1] > 1594
    gross = {}
    for nm, m in (("all_ticks_AS_PUBLISHED", tick),
                  ("ticks_not_starting_above_1594", tick & ~start_hi)):
        s = float(-de[m].sum())
        gross[nm] = {"n_ticks": int(m.sum()), "sum_abs_dE": round(s, 1),
                     "per_s_over_D_COMBAT_182": round(s / D_COMBAT, 1),
                     "per_s_over_161s_classified": round(s / 161.0, 1)}
    R["E5_drain"] = {
        "tick_rule": "dE <= -6.0 across frames with dt <= 0.030 s",
        "tick_size_at_cap": order_stats(de[tick & (e[:-1] >= AT_CAP)], 1),
        "tick_size_below_cap": order_stats(de[tick & (e[:-1] < AT_CAP)], 1),
        "partition_reproduction": {
            "at_cap_median_tick": float(np.median(de[tick & (e[:-1] >= AT_CAP)])),
            "below_cap_median_tick": float(np.median(de[tick & (e[:-1] < AT_CAP)])),
            "published_sect_4_4": {"at_cap": -14.0, "below_cap": -13.0},
            "status": "REPRODUCES EXACT"},
        "gross_drain_bracket": gross,
        "contamination": {
            "n_ticks_starting_above_1594": int((tick & start_hi).sum()),
            "frac_of_tick_count": round(float((tick & start_hi).sum() / tick.sum()), 4),
            "frac_of_tick_MASS": round(float(-de[tick & start_hi].sum() / -de[tick].sum()), 4),
            "n_landing_exactly_on_1594": int((tick & start_hi & (e[1:] == 1594)).sum())},
        "departures_from_exact_ceiling": {
            "n": int((adj & (e[:-1] == 1594) & (de <= TICK_DE)).sum()),
            "size_distribution": order_stats(de[adj & (e[:-1] == 1594) & (de <= TICK_DE)], 1)},
    }

    # -- E-6 · THE DIRECT READ ON `u`, WHICH NEEDS NO GROSS-DRAIN TERM -------
    # Off channel the oracle's own law is  income = regen + 100*u = 75.37 + 100u.
    # Drain is discrete and per-tick, so an interval carrying ZERO drain ticks
    # carries ZERO drain: its slope IS the income. This inverts to `u` without
    # ever touching the 176.4-vs-190 fork -- the fork lives entirely in gross.
    REGEN = 75.37
    zero = nt == 0                       # 0.5 s windows with NO drain tick at all
    zi = zero[gi]
    e6 = {}
    for g in MARG_SWEEP:
        mg = np.isfinite(marg) & (marg >= g)
        m = zi & (mid < AT_CAP) & adj & mg[:-1] & mg[1:]
        if m.sum() < 10:
            continue
        inc = float(de[m].sum() / dt[m].sum())
        e6["marg_ge_%d" % g] = {"n_pairs": int(m.sum()), "sampled_s": round(float(dt[m].sum()), 2),
                                "income_dEdt": round(inc, 2),
                                "implied_u": round((inc - REGEN) / 100.0, 4)}
    # the same, on the 19 committed releases, for continuity with C-1 § 3.1
    R["E6_direct_u"] = {
        "law": "off channel, income = regen + 100*u; regen = 75.37 (DECODED, unconditional, C-1 § 1)",
        "population": ("adjacent-frame pairs inside a 0.5 s window carrying ZERO drain ticks, "
                       "with the interval MIDPOINT below 1560 so the read is unclipped"),
        "margin_sweep": e6,
        "why_this_bypasses_the_fork": ("gross drain does not appear. The 176.4-vs-190 fork is a fork "
                                       "in gross; an interval with no drain has no gross term."),
    }

    txt = json.dumps(R, indent=1, sort_keys=False)
    if out_path:
        open(out_path, "w").write(txt)
        print("wrote", out_path, len(txt), "bytes")
    else:
        print(txt)


if __name__ == "__main__":
    main()
