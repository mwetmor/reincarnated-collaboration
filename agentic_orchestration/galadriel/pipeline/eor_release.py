#!/usr/bin/env python3
"""MD-B4app-2b: are the referent's CHANNEL RELEASES energy-conservation moves?

Consumes the MD-B4app-2 traces (`eor_channel.py energy` 60 Hz, `eor_channel.py
motion` 20 Hz) and tests the owner's pre-registered hypothesis H-MC-1:

    "I must have only purposefully released the whirlwind skill to conserve
     energy at certain points."  -- Matt, owner-eye checkpoint 2026-08-25

Operationalised: a RELEASE is a contiguous interval of combat carrying ZERO
drain ticks.  H-MC-1 predicts releases begin at LOW and/or STEEPLY FALLING
energy and that energy RECOVERS across them, against a null of duration-matched
non-release moments.

Three instruments' worth of care goes into the release POPULATION, because the
population is the whole result:

  1. CLEANING.  The MD-B4app-2 neighbour-median filter is carried unchanged for
     continuity, then a NEW round-trip excursion filter is applied.  The glyph
     OCR emits coherent multi-frame low excursions (e.g. 21 consecutive frames
     reading ~186 while the eye reads 1437) that a 5-neighbour median cannot
     see.  Physically an energy fall of >400 in 1/60 s that fully reverses
     within 2 s cannot be produced by drain + regen; that signature is the
     filter.  Two of these were checked by eye against magnified crops.

  2. TICK GUARD.  A drain tick requires dE <= -6 across samples that are
     genuinely ADJACENT FRAMES (dt <= 0.03 s).  Without it, a cleaning gap
     manufactures a spurious tick at its far edge.

  3. COVERAGE GUARD.  A gap in drain ticks is only a RELEASE if the energy
     trace was actually WATCHING across it.  Candidate gaps below a surviving
     -sample coverage floor are DISCARDED, not scored, and counted separately.
     Without this guard an OCR dropout reads as a release.

  releases <energy.json> <motion.json> <waves.json> <out.json>
"""
import sys, json
import numpy as np

# --- cleaning ---------------------------------------------------------------
MAX_GATE = 2576          # unreserved max, printed constantly by the HUD
NBR_DEV = 250            # MD-B4app-2 neighbour-median rejection band (carried)
EXC_DEP = 400            # energy; excursion depth from the flanking baseline
EXC_RET = 200            # energy; how close the trace must return to call it a round trip
EXC_MAX_S = 2.0          # s; longest excursion the filter will remove

# --- ticks ------------------------------------------------------------------
TICK_DE = -6.0           # MD-B4app-2 drain-tick definition (carried unchanged)
TICK_DT = 0.030          # s; adjacent-frame guard (1/60 = 0.0167)

# --- releases ---------------------------------------------------------------
T_REL = 0.50             # s; primary release floor. Natural inter-tick p99 = 0.60,
                         # p95 = 0.20, median = 0.083 -- see the sweep in the output.
COV_MIN = 0.80           # fraction of expected 60 Hz samples surviving across the gap
EDGE_PAD = 0.50          # s; gaps touching the window edge are not releases
CEIL = 1594.0            # the reserved-adjusted operating ceiling, fixed by the
                         # MD-B4app-2 non-combat control (4,800 samples, all 1594)


def clean(erows):
    """max gate -> neighbour-median -> round-trip excursion. Returns t, e, census."""
    t, e = [], []
    for r in erows:
        if r.get("max") == MAX_GATE and r.get("cur") is not None and 0 <= r["cur"] <= MAX_GATE:
            t.append(r["t"]); e.append(float(r["cur"]))
    t = np.array(t); e = np.array(e)
    n_gate = len(e)

    keep = np.ones(len(e), bool)
    for i in range(len(e)):
        a = max(0, i - 2); b = min(len(e), i + 3)
        nb = np.concatenate([e[a:i], e[i + 1:b]])
        if len(nb) and abs(e[i] - np.median(nb)) > NBR_DEV:
            keep[i] = False
    n_nbr = int((~keep).sum())
    t, e = t[keep], e[keep]

    # round-trip excursion: a run bounded by a big step out and a big step back,
    # short, and returning to where it left.
    bad = np.zeros(len(e), bool)
    i = 0
    while i < len(e) - 1:
        step = e[i + 1] - e[i]
        if abs(step) >= EXC_DEP:
            base = e[i]
            j = i + 1
            while j < len(e) - 1 and (t[j] - t[i + 1]) <= EXC_MAX_S:
                if abs(e[j + 1] - base) <= EXC_RET and abs(e[j + 1] - e[j]) >= EXC_DEP:
                    bad[i + 1:j + 1] = True
                    break
                j += 1
            i = j + 1 if bad[i + 1:j + 1].any() else i + 1
        else:
            i += 1
    n_exc = int(bad.sum())
    t, e = t[~bad], e[~bad]

    return t, e, {"max_gate_pass": n_gate, "neighbour_median_rejected": n_nbr,
                  "roundtrip_excursion_rejected": n_exc, "used": len(e)}


def ticks(t, e):
    de = np.diff(e); dt = np.diff(t)
    m = (de <= TICK_DE) & (dt <= TICK_DT)
    return t[:-1][m], de[m]


def coverage(t, a, b, hz=60.0):
    """fraction of the 1/hz samples expected in [a,b] that survived cleaning."""
    exp = max(1.0, (b - a) * hz)
    return float(((t >= a) & (t <= b)).sum()) / exp


def e_at(t, e, a, b):
    m = (t >= a) & (t <= b)
    return float(np.median(e[m])) if m.sum() else None


def slope(t, e, a, b, minn=15):
    m = (t >= a) & (t <= b)
    if m.sum() < minn:
        return None
    x = t[m] - t[m].mean(); y = e[m]
    return float((x * (y - y.mean())).sum() / (x * x).sum())


def motion_flags(mrows, hz):
    """MD-B4app-2 classification, carried verbatim from eor_duty."""
    from eor_duty import classify, despeckle, MIN_RUN
    t, mag, net, moving = classify(mrows, hz)
    return t, despeckle(moving, MIN_RUN)


def frac_moving(mt, mf, a, b):
    m = (mt >= a) & (mt < b)
    return float(mf[m].mean()) if m.sum() else None


def features(t, e, mt, mf, t_on, t_off, waves):
    d = t_off - t_on
    f = {
        "t_on": round(float(t_on), 3), "t_off": round(float(t_off), 3),
        "dur_s": round(float(d), 3),
        "cov": round(coverage(t, t_on, t_off), 3),
        "E_on": e_at(t, e, t_on, t_on + 0.15),
        "E_off": e_at(t, e, t_off - 0.15, t_off),
        "E_min_pre2s": None, "slope_in_1s": slope(t, e, t_on - 1.0, t_on),
        "slope_in_2s": slope(t, e, t_on - 2.0, t_on),
        "frac_moving": frac_moving(mt, mf, t_on, t_off),
    }
    m = (t >= t_on - 2.0) & (t <= t_on)
    if m.sum():
        f["E_min_pre2s"] = float(e.min(initial=1e9, where=m))
    if f["E_on"] is not None and f["E_off"] is not None:
        f["dE"] = round(f["E_off"] - f["E_on"], 1)
        f["dEdt"] = round(f["dE"] / d, 1)
        f["E_on_frac_ceiling"] = round(f["E_on"] / CEIL, 4)
    for wv, w0 in waves["boundaries"]:
        if t_on >= w0:
            f["wave"] = wv; f["s_since_wave_flip"] = round(float(t_on - w0), 2)
    return f


def run(ep, mp, wp, out):
    E = json.load(open(ep)); M = json.load(open(mp)); W = json.load(open(wp))
    t0, t1 = E["t0"], E["t1"]
    t, e, census = clean(E["rows"])
    tk, dtk = ticks(t, e)
    mt, mf = motion_flags(M["rows"], M["hz"])

    res = {"window": [t0, t1], "energy_census": census,
           "ticks": {"n": int(len(tk)), "median_size": float(np.median(dtk)),
                     "median_interval_s": round(float(np.median(np.diff(tk))), 4),
                     "rate_per_s": round(len(tk) / (t1 - t0), 3)},
           "rule": {"T_REL_s": T_REL, "COV_MIN": COV_MIN, "TICK_DE": TICK_DE,
                    "TICK_DT_s": TICK_DT, "CEIL": CEIL}}

    gaps = np.diff(tk)
    res["intertick_gap_percentiles"] = {p: round(float(np.percentile(gaps, p)), 4)
                                        for p in [50, 75, 90, 95, 99]}

    # ---- release population, with the coverage guard counted ---------------
    def population(T):
        kept, killed = [], []
        for i, g in enumerate(gaps):
            if g < T:
                continue
            a, b = float(tk[i]), float(tk[i + 1])
            if a < t0 + EDGE_PAD or b > t1 - EDGE_PAD:
                killed.append({"t_on": a, "t_off": b, "why": "edge"}); continue
            c = coverage(t, a, b)
            if c < COV_MIN:
                killed.append({"t_on": round(a, 3), "t_off": round(b, 3),
                               "cov": round(c, 3), "why": "coverage"}); continue
            kept.append(features(t, e, mt, mf, a, b, W))
        return kept, killed

    sweep = {}
    for T in [0.25, 0.30, 0.40, 0.50, 0.75, 1.00]:
        k, x = population(T)
        sweep[f"{T:.2f}"] = {"n_kept": len(k), "n_killed_coverage": sum(1 for q in x if q["why"] == "coverage"),
                             "n_killed_edge": sum(1 for q in x if q["why"] == "edge"),
                             "total_s": round(sum(q["dur_s"] for q in k), 2)}
    res["population_sweep"] = sweep

    rel, killed = population(T_REL)
    res["releases"] = rel
    res["releases_discarded"] = killed

    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("releases", "releases_discarded")}, indent=1))
    print(f"\nreleases kept: {len(rel)}  discarded: {len(killed)}")


if __name__ == "__main__":
    run(*sys.argv[2:6]) if sys.argv[1] == "releases" else sys.exit("usage: releases ...")
