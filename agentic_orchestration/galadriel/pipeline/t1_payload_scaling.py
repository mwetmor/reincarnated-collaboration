#!/usr/bin/env python3
"""T-1 — payload-scaling of shape-descriptor dispersion. SYNTHETIC ONLY.

Zero corpus data in the loop. No mask is read; no A-6 null population is
touched. The ONLY thing taken from the corpus is the payload LADDER (the five
published row medians of `authored_px`), which is a scalar per row.

The descriptor operator is IMPORTED VERBATIM from
`reincarnated-godot/scripts/s2b_xrow_rows37.py` rather than retyped, so this
instrument and the scored one are literally the same function.

TWO CONDITIONS, and the second is the point:

  A  PURE-QUANTISATION.  k arms are the SAME shape at the SAME scale, differing
     only by sub-pixel PHASE (fractional-pixel centre offset). True shape
     difference is EXACTLY ZERO by construction, so every unit of dispersion is
     discretisation. Prediction under counting noise: slope -0.5, no floor.

  B  PERTURBED.  k arms differ by rotation ~U(-2,+2) deg and scale ~U(-1,+1) %
     on top of phase -- the magnitude of genuine inter-element variation.
     Prediction under a SUPERPOSITION account: falls as n^-0.5 while
     quantisation dominates, then PLATEAUS at a floor set by the real shape
     difference, which is n-INDEPENDENT.

  A vs B is therefore the discriminator on KR's section 11.2 superposition, not
  merely on the payload hypothesis. A alone confirms the mechanism exists; only
  B-plateauing-above-A shows signal and noise coexist and separate by their
  n-dependence.

REPLICATION.  k is held at 4 -- the corpus's own cohort size -- because the
quantity being modelled is a 4-arm null. But a 4-arm null is 6 pairs and is
itself a noisy ESTIMATE, so the whole 4-arm draw is repeated R times with
independent phases (and, in B, independent perturbations) and the MEDIAN null is
reported. This changes the precision of the estimate, not the estimand.

galadriel, 2026-08-25.
"""
import importlib.util
import itertools
import json
import math
import os
import sys

import numpy as np

# ---- import the scored instrument's descriptors() verbatim ------------------
_OP = os.path.expanduser("~/Games/reincarnated-godot/scripts/s2b_xrow_rows37.py")
_spec = importlib.util.spec_from_file_location("_xrow", _OP)
_xrow = importlib.util.module_from_spec(_spec)
sys.modules["_xrow"] = _xrow
_spec.loader.exec_module(_xrow)
descriptors = _xrow.descriptors
DIST_KEYS = _xrow.DIST_KEYS

# ---- the corpus's own payload ladder (published row medians of authored_px) --
LADDER = [1740, 2700, 5446, 11475, 22117, 127747]
K_ARMS = 4
REPLICATES = 60
SEED = 20260825

# ---- shape families ---------------------------------------------------------
# r(theta) = R * f(theta) in a frame anisotropically scaled by (ax, ay), with an
# optional set of disjoint LOBES at fixed relative offsets. Shape is held
# EXACTLY constant across the ladder -- only R changes -- so every descriptor is
# analytically scale-invariant and all measured dispersion is discretisation.
#
# `scatter` exists so that `largest_component_frac` is IN the experiment. Its
# lobes are deliberately sized far from the 0.01*n significance gate (each ~20 %
# of n) so that `significant_components` stays constant at 5 and the GATE
# mechanism is NOT admitted into a test of the PAYLOAD mechanism. Those are two
# mechanisms both keyed to small n and they are not pooled here.
FAMILIES = {
    #             ax    ay    harmonics: (order, amp, phase)          lobe offsets (in R units)
    "blob":     (1.00, 1.00, [(3, 0.18, 0.7), (5, 0.09, -1.2)], None),
    "elongate": (3.20, 0.55, [(2, 0.10, 0.3), (7, 0.05, 1.1)], None),
    "lobed":    (1.00, 1.00, [(5, 0.42, 0.0), (2, 0.07, 0.4)], None),
    "scatter":  (1.00, 1.00, [(3, 0.15, 0.2)],
                 [(0.0, 0.0), (3.1, 0.9), (-2.8, 1.4), (1.2, -3.0), (-1.5, -2.6)]),
}

_AREA_CACHE = {}


def _f(theta, harm):
    v = np.ones_like(theta)
    for order, amp, ph in harm:
        v = v + amp * np.cos(order * theta + ph)
    return v


def _unit_area(fam):
    if fam in _AREA_CACHE:
        return _AREA_CACHE[fam]
    ax, ay, harm, lobes = FAMILIES[fam]
    t = np.linspace(0.0, 2.0 * math.pi, 200001)
    a = ax * ay * 0.5 * float(np.trapezoid(_f(t, harm) ** 2, t))
    a *= (len(lobes) if lobes else 1)
    _AREA_CACHE[fam] = a
    return a


def _fmax(fam):
    ax, ay, harm, lobes = FAMILIES[fam]
    return float(_f(np.linspace(0, 2 * math.pi, 20001), harm).max())


def rasterise(fam, target_n, rot_deg, scale, phase):
    ax, ay, harm, lobes = FAMILIES[fam]
    R = math.sqrt(target_n / _unit_area(fam)) * scale
    reach = _fmax(fam) * max(ax, ay)
    if lobes:
        reach += max(math.hypot(*o) for o in lobes)
    half = int(math.ceil(R * reach)) + 4
    g = np.arange(-half, half + 1, dtype=np.float64)
    X, Y = np.meshgrid(g - phase[0], g - phase[1])
    a = math.radians(rot_deg)
    ca, sa = math.cos(a), math.sin(a)
    xr, yr = X * ca + Y * sa, -X * sa + Y * ca     # into shape frame
    m = np.zeros(X.shape, dtype=bool)
    for ox, oy in (lobes or [(0.0, 0.0)]):
        xs = (xr - R * ox) / ax
        ys = (yr - R * oy) / ay
        r = np.hypot(xs, ys)
        th = np.arctan2(ys, xs)
        m |= (r <= R * _f(th, harm))
    return m


def run(condition, rng):
    """Returns median-over-replicates nulls and raw per-descriptor dispersions."""
    null_reps = {(f, n): [] for f in FAMILIES for n in LADDER}
    raw_reps = {k: {(f, n): [] for f in FAMILIES for n in LADDER} for k in DIST_KEYS}
    n_actual = {(f, n): [] for f in FAMILIES for n in LADDER}

    for _ in range(REPLICATES):
        arms = []
        for fam in FAMILIES:
            for n_t in LADDER:
                for _k in range(K_ARMS):
                    ph = (float(rng.random()), float(rng.random()))
                    if condition == "A":
                        rot, scl = 0.0, 1.0
                    else:
                        rot = float(rng.uniform(-2.0, 2.0))
                        scl = float(rng.uniform(0.99, 1.01))
                    d = descriptors(rasterise(fam, n_t, rot, scl, ph))
                    if d is None:
                        continue
                    arms.append({"family": fam, "rung": n_t, **d})

        M = np.array([[a[k] for k in DIST_KEYS] for a in arms], dtype=float)
        mu, sd = M.mean(axis=0), M.std(axis=0)
        sd[sd < 1e-9] = 1.0
        Z = (M - mu) / sd

        for fam in FAMILIES:
            for n_t in LADDER:
                idx = [i for i, a in enumerate(arms)
                       if a["family"] == fam and a["rung"] == n_t]
                if len(idx) < 2:
                    continue
                ds = [float(np.linalg.norm(Z[i] - Z[j]))
                      for i, j in itertools.combinations(idx, 2)]
                null_reps[(fam, n_t)].append(float(np.mean(ds)))
                n_actual[(fam, n_t)].append(
                    float(np.mean([arms[i]["authored_px"] for i in idx])))
                for key in DIST_KEYS:
                    v = [arms[i][key] for i in idx]
                    raw_reps[key][(fam, n_t)].append(float(np.std(v, ddof=1)))
    return null_reps, raw_reps, n_actual


def loglog(xs, ys):
    xs = np.log(np.asarray(xs, dtype=float))
    ys = np.asarray(ys, dtype=float)
    ok = ys > 1e-12
    if ok.sum() < 3:
        return None, None
    xs, ys = xs[ok], np.log(ys[ok])
    s = float(np.polyfit(xs, ys, 1)[0])
    return s, float(np.corrcoef(xs, ys)[0, 1])


def main():
    out = {"ladder": LADDER, "k_arms": K_ARMS, "replicates": REPLICATES,
           "seed": SEED, "families": list(FAMILIES), "operator_source": _OP,
           "conditions": {}}
    med = {}
    for cond in ("A", "B"):
        rng = np.random.default_rng(SEED + (0 if cond == "A" else 1))
        null_reps, raw_reps, n_actual = run(cond, rng)
        print("\n================ CONDITION %s (%s) ================" % (
            cond, "pure quantisation, zero true shape difference"
            if cond == "A" else "+/-2 deg, +/-1 % genuine variation"))
        print("%-9s %8s %10s %10s %10s" % ("family", "rung", "null_med", "p25", "p75"))
        per_fam, med[cond] = {}, {}
        for fam in FAMILIES:
            xs, ys = [], []
            for n_t in LADDER:
                v = null_reps[(fam, n_t)]
                if not v:
                    continue
                m = float(np.median(v))
                print("%-9s %8d %10.4f %10.4f %10.4f" % (
                    fam, n_t, m, np.percentile(v, 25), np.percentile(v, 75)))
                xs.append(float(np.median(n_actual[(fam, n_t)])))
                ys.append(m)
                med[cond][(fam, n_t)] = m
            s, r = loglog(xs, ys)
            monotone = all(ys[i] >= ys[i + 1] for i in range(len(ys) - 1))
            ratio = ys[0] / ys[-1] if ys[-1] > 0 else None
            per_fam[fam] = {"slope": s, "r": r, "ratio_small_over_large": ratio,
                            "monotone": monotone, "nulls": ys, "n": xs}
            print("  -> %-9s slope=%.3f  r=%.3f  1.7k/128k=%.2fx  monotone=%s"
                  % (fam, s, r, ratio, monotone))

        print("\n  per-descriptor RAW within-rung dispersion (median over "
              "replicates, pooled over families), log-log slope vs n:")
        per_desc = {}
        for key in DIST_KEYS:
            xs, ys = [], []
            for n_t in LADDER:
                vals = [np.median(raw_reps[key][(f, n_t)])
                        for f in FAMILIES if raw_reps[key][(f, n_t)]]
                vals = [v for v in vals if v > 1e-12]
                if vals:
                    xs.append(n_t)
                    ys.append(float(np.mean(vals)))
            if len(xs) < 3:
                print("    %-24s  CONSTANT (zero dispersion at every rung)" % key)
                per_desc[key] = {"slope": None, "note": "constant"}
                continue
            s, r = loglog(xs, ys)
            ratio = ys[0] / ys[-1] if ys[-1] > 0 else None
            per_desc[key] = {"slope": s, "r": r, "ratio": ratio,
                             "raw": dict(zip(map(str, xs), ys))}
            print("    %-24s slope=%7.3f  r=%7.3f  1.7k/128k=%7.2fx"
                  % (key, s, r, ratio))
        out["conditions"][cond] = {"per_family": per_fam, "per_descriptor": per_desc}

    print("\n================ A vs B : the SUPERPOSITION test ================")
    print("A and B are independent RNG streams. Noise and a genuine shape")
    print("difference are independent contributions to a Euclidean distance, so")
    print("they add in QUADRATURE, not linearly:  B^2 = A^2 + S^2.")
    print("S = sqrt(B^2 - A^2) is the signal term. A superposition predicts S is")
    print("FLAT in n (slope ~0) while A falls as n^-0.5.\n")
    print("%-9s %8s %9s %9s %9s %8s" % ("family", "rung", "A(noise)", "B(sig+n)",
                                        "S=sqrt", "B/A"))
    supo = {}
    for fam in FAMILIES:
        ns, S = [], []
        for n_t in LADDER:
            a, b = med["A"].get((fam, n_t)), med["B"].get((fam, n_t))
            if a is None or b is None:
                continue
            s_q = math.sqrt(b * b - a * a) if b > a else 0.0
            print("%-9s %8d %9.4f %9.4f %9.4f %7.2fx"
                  % (fam, n_t, a, b, s_q, b / a if a else float("nan")))
            ns.append(n_t)
            S.append(s_q)
        if not ns:
            continue
        pos = [(n, s) for n, s in zip(ns, S) if s > 1e-9]
        s_sl, s_r = (loglog([p[0] for p in pos], [p[1] for p in pos])
                     if len(pos) >= 3 else (None, None))
        a_sl = out["conditions"]["A"]["per_family"][fam]["slope"]
        supo[fam] = {"S": S, "S_slope": s_sl, "S_r": s_r, "A_slope": a_sl,
                     "B_over_A_at_max_n": med["B"][(fam, LADDER[-1])] /
                     med["A"][(fam, LADDER[-1])]}
        verdict = ("SUPERPOSITION: noise falls at %.2f, signal floor is FLAT (%.2f)"
                   % (a_sl, s_sl) if (s_sl is not None and abs(s_sl) < 0.25)
                   else "signal term not separable at this perturbation")
        print("  -> %-9s S: %.4f (1.7k) -> %.4f (128k), slope %s | A slope %.3f"
              "\n     %s" % (fam, S[0], S[-1],
                            "%.3f" % s_sl if s_sl is not None else "n/a",
                            a_sl, verdict))
    out["superposition"] = supo

    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "t1_payload_scaling_result.json")
    with open(dst, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print("\nwrote %s" % dst)


if __name__ == "__main__":
    main()
