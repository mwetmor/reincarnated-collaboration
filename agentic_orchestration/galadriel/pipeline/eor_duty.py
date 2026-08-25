#!/usr/bin/env python3
"""MD-B4app-2 reduction: motion trace + energy trace -> move/channel duty cycle.

Consumes the two `eor_channel.py` outputs and derives, with every rule stated:

  STATIONARY / MOVING classification.  Two guards, both necessary:
    (i)  per-interval |d| below the static-mode ceiling, and
    (ii) NET displacement over a +/-w window below a shake ceiling. Grim Dawn
         applies screen-shake on heavy hits; shake is an oscillation that
         CANCELS under integration while real translation ACCUMULATES. Guard (i)
         alone would count shake as movement and inflate the moving fraction.

  EPISODES.  Maximal runs of one class, with a minimum-run filter so a single
  mis-registered sample does not split an episode. The filter length is reported.

  ENERGY SLOPE conditioned on class, and event-locked to the stop/go edges.
  This is the CHANNEL evidence: EoR publishes `176.4 Energy Cost per Second` on
  its own tooltip (read on this footage, note 2026-08-08 § 3), so a stationary
  episode that drains and a moving episode that does not is the decoded D-9 rule
  visible from outside the process.

  report <motion.json> <energy.json> <waves.json> <out.json>
"""
import sys, json
import numpy as np

STATIC_MAG = 1.0        # px; placed in the measured valley 0.3..2.0 of the mag histogram
NET_W = 0.30            # s; half-window for the net-displacement shake guard
NET_TH = 3.0            # px; net travel over 2*NET_W below this = not translating
MIN_RUN = 3             # samples; de-speckle


def load(p):
    return json.load(open(p))


def classify(mrows, hz):
    t = np.array([r["t"] for r in mrows])
    dx = np.array([r["dx"] for r in mrows])
    dy = np.array([r["dy"] for r in mrows])
    mag = np.hypot(dx, dy)
    # cumulative camera path; shake cancels, translation accumulates
    X = np.cumsum(dx); Y = np.cumsum(dy)
    k = max(1, int(round(NET_W * hz)))
    n = len(t)
    net = np.zeros(n)
    for i in range(n):
        a = max(0, i - k); b = min(n - 1, i + k)
        net[i] = np.hypot(X[b] - X[a], Y[b] - Y[a])
    moving = (mag >= STATIC_MAG) & (net >= NET_TH)
    return t, mag, net, moving


def despeckle(flags, minrun):
    f = flags.copy()
    n = len(f)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and f[j + 1] == f[i]:
            j += 1
        if (j - i + 1) < minrun and i > 0 and j < n - 1:
            f[i:j + 1] = f[i - 1]
        i = j + 1
    return f


def episodes(t, flags, hz):
    out = []
    i, n = 0, len(t)
    while i < n:
        j = i
        while j + 1 < n and flags[j + 1] == flags[i]:
            j += 1
        out.append({"t0": float(t[i]), "t1": float(t[j]) + 1.0 / hz,
                    "dur": round(float(t[j] - t[i]) + 1.0 / hz, 4),
                    "state": "MOVING" if flags[i] else "STATIONARY"})
        i = j + 1
    return out


def energy_series(erows):
    t, e = [], []
    for r in erows:
        if r.get("max") == 2576 and r.get("cur") is not None and 0 <= r["cur"] <= 2576:
            t.append(r["t"]); e.append(r["cur"])
    t = np.array(t); e = np.array(e, float)
    # single-glyph drops survive the max-check (e.g. 1501 -> 101). Reject a sample
    # more than 250 from the median of its 5 nearest surviving neighbours.
    keep = np.ones(len(e), bool)
    for i in range(len(e)):
        a = max(0, i - 2); b = min(len(e), i + 3)
        nb = np.concatenate([e[a:i], e[i + 1:b]])
        if len(nb) and abs(e[i] - np.median(nb)) > 250:
            keep[i] = False
    return t[keep], e[keep], int((~keep).sum())


def slope_at(te, ee, t0, t1):
    """least-squares dE/dt over [t0,t1]; None if <4 samples."""
    m = (te >= t0) & (te <= t1)
    if m.sum() < 4:
        return None
    x = te[m] - te[m].mean(); y = ee[m]
    return float((x * (y - y.mean())).sum() / (x * x).sum())


def report(mp, ep, wp, out):
    M = load(mp); E = load(ep)
    hz = M["hz"]
    t, mag, net, moving = classify(M["rows"], hz)
    flags = despeckle(moving, MIN_RUN)
    eps = episodes(t, flags, hz)
    te, ee, nrej = energy_series(E["rows"])

    n = len(flags)
    res = {
        "window": [M["t0"], M["t1"]],
        "hz": hz,
        "rule": {"static_mag_px": STATIC_MAG, "net_halfwindow_s": NET_W,
                 "net_threshold_px": NET_TH, "min_run_samples": MIN_RUN},
        "n_samples": n,
        "frac_moving": round(float(flags.mean()), 4),
        "frac_stationary": round(float(1 - flags.mean()), 4),
        "frac_moving_no_shake_guard": round(float((mag >= STATIC_MAG).mean()), 4),
        "energy_samples_used": len(te), "energy_samples_rejected": nrej,
    }

    # --- threshold sensitivity, so the number is not a fitted one -----------
    sens = {}
    for th in [0.3, 0.5, 1.0, 2.0, 3.0]:
        mv = (mag >= th) & (net >= NET_TH)
        sens[str(th)] = round(float(1 - despeckle(mv, MIN_RUN).mean()), 4)
    res["frac_stationary_vs_mag_threshold"] = sens
    sens2 = {}
    for nt in [0.0, 1.5, 3.0, 5.0, 8.0]:
        mv = (mag >= STATIC_MAG) & (net >= nt)
        sens2[str(nt)] = round(float(1 - despeckle(mv, MIN_RUN).mean()), 4)
    res["frac_stationary_vs_net_threshold"] = sens2

    # --- episode structure --------------------------------------------------
    for st in ("STATIONARY", "MOVING"):
        d = np.array([e["dur"] for e in eps if e["state"] == st])
        res[f"episodes_{st.lower()}"] = {
            "n": int(len(d)), "total_s": round(float(d.sum()), 2),
            "mean_s": round(float(d.mean()), 3), "median_s": round(float(np.median(d)), 3),
            "p90_s": round(float(np.percentile(d, 90)), 3), "max_s": round(float(d.max()), 3),
            "n_ge_1s": int((d >= 1.0).sum()), "n_ge_2s": int((d >= 2.0).sum()),
            "n_ge_3s": int((d >= 3.0).sum()),
            "hist_s": {k: int(v) for k, v in zip(
                ["<0.5", "0.5-1", "1-2", "2-3", "3-5", ">=5"],
                np.histogram(d, [0, .5, 1, 2, 3, 5, 1e9])[0])},
        }

    # --- energy slope by class ---------------------------------------------
    def slopes(state):
        vals, wts = [], []
        for e in eps:
            if e["state"] != state or e["dur"] < 0.5:
                continue
            s = slope_at(te, ee, e["t0"], e["t1"])
            if s is not None:
                vals.append(s); wts.append(e["dur"])
        if not vals:
            return None
        v = np.array(vals); w = np.array(wts)
        return {"n_episodes": len(v),
                "mean_dEdt": round(float(v.mean()), 2),
                "dur_weighted_dEdt": round(float((v * w).sum() / w.sum()), 2),
                "median_dEdt": round(float(np.median(v)), 2),
                "frac_negative": round(float((v < 0).mean()), 3),
                "p10": round(float(np.percentile(v, 10)), 2),
                "p90": round(float(np.percentile(v, 90)), 2)}
    res["energy_slope_stationary"] = slopes("STATIONARY")
    res["energy_slope_moving"] = slopes("MOVING")

    # --- per-wave -----------------------------------------------------------
    waves = load(wp)
    pw = []
    for i, (wv, w0) in enumerate(waves["boundaries"]):
        w1 = waves["boundaries"][i + 1][1] if i + 1 < len(waves["boundaries"]) else waves["end"]
        m = (t >= w0) & (t < w1)
        if m.sum() < 5:
            continue
        f = flags[m]
        d = np.array([e["dur"] for e in eps
                      if e["state"] == "STATIONARY" and w0 <= e["t0"] < w1])
        pw.append({"wave": wv, "t0": w0, "t1": w1, "dur_s": round(w1 - w0, 2),
                   "n": int(m.sum()),
                   "frac_stationary": round(float(1 - f.mean()), 4),
                   "n_stationary_episodes": int(len(d)),
                   "longest_stationary_s": round(float(d.max()), 2) if len(d) else 0.0,
                   "stationary_eps_per_10s": round(10.0 * len(d) / (w1 - w0), 2)})
    res["per_wave"] = pw

    # --- wave-onset behaviour: plant-through-spawn vs kite-then-plant -------
    onset = []
    for wv, w0 in waves["boundaries"]:
        m = (t >= w0) & (t < w0 + 5.0)
        if m.sum() < 10:
            continue
        f = flags[m]
        # time to first stationary run >= 0.5 s after the wave flips
        tt = t[m]; first = None
        i = 0
        while i < len(f):
            if not f[i]:
                j = i
                while j + 1 < len(f) and not f[j + 1]:
                    j += 1
                if (tt[j] - tt[i]) >= 0.5:
                    first = round(float(tt[i] - w0), 2); break
                i = j + 1
            else:
                i += 1
        onset.append({"wave": wv, "frac_stationary_first_5s": round(float(1 - f.mean()), 3),
                      "s_to_first_stop_ge_0p5s": first})
    res["wave_onset"] = onset

    json.dump({"summary": res, "episodes": eps}, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    report(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
