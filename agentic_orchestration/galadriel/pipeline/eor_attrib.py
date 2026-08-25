#!/usr/bin/env python3
"""eor_attrib.py — MD-B4app-2c: is ONE SLOT the singular culprit for the
channel interruptions?

galadriel / visual-perception seam.  Extends MD-B4app-2b (`eor_release.py`,
`eor_cooldown.py`).  No new footage; consumes the committed traces.

Owner question (Matt, verbatim, 2026-08-25): "Have we checked for a pattern as
to a specific skill that may be the singular culprit for the 15% of cast
interrupts?"

Pre-registered hypothesis H-MC-2: slot L is the singular culprit -- substantially
all Type-B interrupts are slot-L casts, and non-slot-L casts weave under the
channel without breaking it.

Two directions, and they are NOT the same test:

  FORWARD  (MD-B4app-2b already did this):  of the 19 RELEASES, how many carry a
           cast within +/-0.25 s?  Answer there: 8.  This is P(cast | release).
  CONVERSE (this lap, and it is the decisive one):  of the 53 CASTS, how many sit
           inside a channel gap >= 0.5 s?  This is P(release | cast), and it is
           the quantity M-POL-2's `cast_interrupts_channel = 0.15` claims to be.

The cast instrument is the ACCEPTED per-slot DIMMING trace from
`eor_cooldown.py slots`, re-derived here from the committed 20 Hz JSON under the
same midpoint rule (a slot is DIM when its icon-cell max-channel mean falls below
the midpoint of that slot's own observed range; the distribution is bimodal with
an empty valley, so the midpoint is a reading of the data, not a fitted knob).
Re-derivation reproduces MD-B4app-2b § 5.3 exactly: 22 / 19 / 12 onsets on slots
2 / 3 / L.

  casts   <slots.json> <out.json>
  attrib  <energy.json> <motion.json> <waves.json> <slots.json> <releases.json> <out.json>
"""
import sys, json
import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from eor_release import clean, ticks, coverage, T_REL, COV_MIN   # noqa: E402

# ---------------------------------------------------------------------------
# cast derivation
# ---------------------------------------------------------------------------
CAST_SLOTS = ("2", "3", "L")   # slots that DIM for a cooldown, minus slot 4
# Slot 4 dims too, but its dim state carries a WHITE numeral counting down from
# ~24 s -- an active buff's remaining duration, not a cooldown.  Median dim run
# 24.40 s against 3.15 / 4.55 / 3.60 s for 2 / 3 / L.  A buff timer is not a cast.
BUFF_SLOT = "4"
ALL_SLOTS = ("1", "2", "3", "4", "5", "L", "R", "6", "7", "8", "9", "0")

# 20 Hz sampling means the first DIM frame is up to one frame LATE relative to the
# button press.  Every cast time therefore carries a +/- one-frame uncertainty and
# the converse test is run again at tc - 1 frame as a sensitivity check.
FRAME = 0.05


def slot_dim_runs(rows, hz, s):
    """DIM runs on one slot under the midpoint rule.  Returns [(t_on, dur_s)]."""
    t = np.array([r["t"] for r in rows])
    v = np.array([r[s] for r in rows], float)
    lo, hi = v.min(), v.max()
    thr = lo + 0.5 * (hi - lo)
    dim = v < thr
    runs, i = [], 0
    while i < len(dim):
        if dim[i]:
            j = i
            while j + 1 < len(dim) and dim[j + 1]:
                j += 1
            runs.append((float(t[i]), (j - i + 1) / hz))
            i = j + 1
        else:
            i += 1
    return runs, float(thr), float(lo), float(hi)


def slot_census(rows, hz):
    """Per-slot separability + whether the slot EVER dims.  The honesty rail."""
    out = {}
    for s in ALL_SLOTS:
        v = np.array([r[s] for r in rows], float)
        lo, hi = v.min(), v.max()
        rng = hi - lo
        mid = ((v > lo + 0.35 * rng) & (v < lo + 0.65 * rng)).mean() if rng else 1.0
        runs, thr, _, _ = slot_dim_runs(rows, hz, s)
        rl = [d for _, d in runs]
        out[s] = {"min": round(lo, 2), "max": round(hi, 2),
                  "median": round(float(np.median(v)), 2),
                  "range": round(rng, 2),
                  "valley_share_mid30": round(float(mid), 4),
                  "n_runs": len(runs),
                  "median_run_s": round(float(np.median(rl)), 2) if rl else None,
                  "max_run_s": round(float(max(rl)), 2) if rl else None}
    return out


# A dim run ends when the cooldown expires.  If the referent re-fires the skill
# in the same frame the cooldown clears, TWO casts merge into ONE dim run and the
# instrument undercounts.  Detected by run length, resolved by eye on the red
# cooldown NUMERAL (readable on slot L; see MD-B4app-2b § 5.1 for where it is not).
#
#   t = 797.65 slot L, dim run 7.20 s against a modal 3.60 s.  The numeral reads
#   3 / 2 / 1 at t = 798.2 / 799.5 / 800.5 and then RESETS TO 4, between t=801.15
#   (still "1") and t=801.25 (already "4").  Two casts, not one.
#   Evidence: work/Lnum_sheet.png, work/Lreset_strip.png.
#
# This is the ONLY merged run in the window: max/median dim-run ratio is 7.20/3.60
# on slot L and 1.03 on both slot 2 and slot 3.
MERGED = [{"t": 801.20, "slot": "L", "cd_s": 3.60, "eye_resolved": True,
           "t_uncertainty_s": 0.05,
           "why": "numeral reset inside the 797.65 dim run (7.20 s vs modal 3.60 s)"}]
MERGE_FLAG_RATIO = 1.5     # flag any dim run this many times the slot's median


def casts(slotp, out=None, apply_merged=True):
    S = json.load(open(slotp))
    rows, hz = S["rows"], S["hz"]
    cs, suspect = [], []
    for s in CAST_SLOTS:
        runs, thr, lo, hi = slot_dim_runs(rows, hz, s)
        med = float(np.median([d for _, d in runs]))
        for t_on, dur in runs:
            cs.append({"t": round(t_on, 4), "slot": s, "cd_s": round(dur, 3)})
            if dur > MERGE_FLAG_RATIO * med:
                suspect.append({"slot": s, "t": round(t_on, 3), "cd_s": round(dur, 3),
                                "slot_median_cd_s": round(med, 3)})
    n_raw = len(cs)
    if apply_merged:
        cs += [dict(m) for m in MERGED]
    cs.sort(key=lambda c: c["t"])
    res = {"source": slotp, "hz": hz, "window": [S["t0"], S["t1"]],
           "cast_slots": list(CAST_SLOTS), "buff_slot_excluded": BUFF_SLOT,
           "n_casts_dim_runs_only": n_raw,
           "merged_runs_flagged": suspect,
           "merged_runs_resolved_by_eye": MERGED if apply_merged else [],
           "n_casts": len(cs),
           "per_slot": {s: sum(1 for c in cs if c["slot"] == s) for s in CAST_SLOTS},
           "slot_census": slot_census(rows, hz), "casts": cs}
    if out:
        json.dump(res, open(out, "w"), indent=1)
    return res


# ---------------------------------------------------------------------------
# the two directions
# ---------------------------------------------------------------------------
def gap_containing(tk, tc):
    """(i, t_a, t_b) of the inter-tick gap holding tc, or None outside the run."""
    if tc < tk[0] or tc >= tk[-1]:
        return None
    i = int(np.searchsorted(tk, tc, side="right") - 1)
    return i, float(tk[i]), float(tk[i + 1])


def attrib(ep, mp, wp, slotp, relp, out):
    E = json.load(open(ep))
    t, e, census = clean(E["rows"])
    tk, _ = ticks(t, e)
    C = casts(slotp)
    R = json.load(open(relp))
    rel = R["releases"]

    res = {"window": R["window"], "energy_census": census, "n_ticks": int(len(tk)),
           "rule": {"T_REL_s": T_REL, "COV_MIN": COV_MIN, "FRAME_s": FRAME},
           "n_casts": C["n_casts"], "per_slot_casts": C["per_slot"],
           "slot_census": C["slot_census"]}

    # ---- FORWARD: per-release attribution ---------------------------------
    fwd = []
    for r in rel:
        near = [{"slot": c["slot"], "lag_s": round(c["t"] - r["t_on"], 3),
                 "cd_s": c["cd_s"]}
                for c in C["casts"] if abs(c["t"] - r["t_on"]) <= 0.25]
        near5 = [{"slot": c["slot"], "lag_s": round(c["t"] - r["t_on"], 3)}
                 for c in C["casts"] if abs(c["t"] - r["t_on"]) <= 0.50]
        # a cast anywhere INSIDE the release, not merely at its onset
        inside = [{"slot": c["slot"], "lag_s": round(c["t"] - r["t_on"], 3)}
                  for c in C["casts"] if r["t_on"] <= c["t"] <= r["t_off"]]
        fwd.append({"t_on": r["t_on"], "t_off": r["t_off"], "dur_s": r["dur_s"],
                    "wave": r.get("wave"), "s_since_flip": r.get("s_since_wave_flip"),
                    "type": "B" if near else "A",
                    "casts_025": near, "casts_050": near5, "casts_inside": inside})
    res["forward"] = fwd
    res["n_typeB"] = sum(1 for f in fwd if f["type"] == "B")

    # ---- CONVERSE: per-cast interruption ----------------------------------
    conv = []
    for c in C["casts"]:
        row = {"t": c["t"], "slot": c["slot"], "cd_s": c["cd_s"]}
        g = gap_containing(tk, c["t"])
        gm = gap_containing(tk, c["t"] - FRAME)   # one-frame sensitivity
        for tag, gg in (("", g), ("_m1", gm)):
            if gg is None:
                row[f"gap{tag}"] = None
                continue
            i, a, b = gg
            row[f"gap{tag}"] = round(b - a, 4)
            if tag == "":
                row["gap_t0"], row["gap_t1"] = round(a, 3), round(b, 3)
                row["gap_cov"] = round(coverage(t, a, b), 3)
                row["lag_into_gap_s"] = round(c["t"] - a, 3)
        conv.append(row)
    res["converse"] = conv

    # ---- the partition ----------------------------------------------------
    def part(rows_, key=lambda r: True):
        sel = [r for r in rows_ if key(r) and r["gap"] is not None]
        blind = [r for r in sel if r["gap"] >= T_REL and r["gap_cov"] < COV_MIN]
        hit = [r for r in sel if r["gap"] >= T_REL and r["gap_cov"] >= COV_MIN]
        g = np.array([r["gap"] for r in sel]) if sel else np.array([0.0])
        return {"n": len(sel), "n_interrupt": len(hit), "n_blind_gap": len(blind),
                "p_interrupt": round(len(hit) / len(sel), 4) if sel else None,
                "median_gap_s": round(float(np.median(g)), 4),
                "p75_gap_s": round(float(np.percentile(g, 75)), 4),
                "p90_gap_s": round(float(np.percentile(g, 90)), 4),
                "max_gap_s": round(float(g.max()), 4),
                "median_gap_s_sub_floor": round(float(np.median(
                    [r["gap"] for r in sel if r["gap"] < T_REL])), 4)
                if any(r["gap"] < T_REL for r in sel) else None,
                "interrupt_times": [r["t"] for r in hit]}

    res["partition"] = {s: part(conv, lambda r, s=s: r["slot"] == s) for s in CAST_SLOTS}
    res["partition"]["L_vs_rest"] = {
        "L": part(conv, lambda r: r["slot"] == "L"),
        "not_L": part(conv, lambda r: r["slot"] != "L")}
    res["partition"]["all"] = part(conv)

    # ---- CONVERSE, variant 2: RELEASE-MATCHED --------------------------------
    # The containing-gap rule (variant 1 above) is exposed to 20 Hz quantisation:
    # a cast one frame EARLIER than the tick that opens a release lands in the
    # sliver of gap before it and scores 0.017 s, not 0.60 s (t = 748.05 is
    # exactly this).  The symmetric definition -- "does a scored RELEASE open
    # within +/-0.25 s of this cast" -- is immune to it, uses the same population
    # the forward direction uses, and makes the two directions one number.
    W = 0.25
    for r in conv:
        m = [x for x in rel if abs(x["t_on"] - r["t"]) <= W]
        r["release_matched"] = bool(m)
        r["matched_release_t_on"] = m[0]["t_on"] if m else None
        r["matched_release_dur_s"] = m[0]["dur_s"] if m else None

    def part2(key=lambda r: True):
        sel = [r for r in conv if key(r)]
        hit = [r for r in sel if r["release_matched"]]
        sub = [r["gap"] for r in sel
               if not r["release_matched"] and r["gap"] is not None]
        return {"n": len(sel), "n_interrupt": len(hit),
                "p_interrupt": round(len(hit) / len(sel), 4) if sel else None,
                "interrupt_times": [r["t"] for r in hit],
                "interrupt_durs_s": [r["matched_release_dur_s"] for r in hit],
                "median_dur_s": round(float(np.median(
                    [r["matched_release_dur_s"] for r in hit])), 3) if hit else None,
                "noninterrupt_median_gap_s": round(float(np.median(sub)), 4) if sub else None,
                "noninterrupt_p90_gap_s": round(float(np.percentile(sub, 90)), 4) if sub else None}

    res["partition_release_matched"] = {s: part2(lambda r, s=s: r["slot"] == s)
                                        for s in CAST_SLOTS}
    res["partition_release_matched"]["not_L"] = part2(lambda r: r["slot"] != "L")
    res["partition_release_matched"]["all"] = part2()

    # ---- statistics --------------------------------------------------------
    from scipy import stats as st
    L = res["partition_release_matched"]["L"]
    NL = res["partition_release_matched"]["not_L"]
    tbl = [[L["n_interrupt"], L["n"] - L["n_interrupt"]],
           [NL["n_interrupt"], NL["n"] - NL["n_interrupt"]]]
    odds, p = st.fisher_exact(tbl, alternative="greater")
    # the null a cast must beat: a scored release opens within +/-W of ANY moment
    t0, t1 = res["window"]
    null_p = min(1.0, len(rel) * 2 * W / (t1 - t0))   # 19 x 0.5 s of 182.65 s
    res["stats"] = {
        "fisher_L_vs_notL_table": tbl, "fisher_p_one_sided": round(float(p), 6),
        "fisher_odds": None if np.isinf(odds) else round(float(odds), 3),
        "clock_null_p": round(null_p, 4),
        "binom_vs_clock_null": {
            s: round(float(st.binomtest(res["partition_release_matched"][s]["n_interrupt"],
                                        res["partition_release_matched"][s]["n"],
                                        null_p, alternative="greater").pvalue), 6)
            for s in CAST_SLOTS},
    }
    # per-slot pairwise, L vs 2 and L vs 3
    for other in ("2", "3"):
        O = res["partition_release_matched"][other]
        t2 = [[L["n_interrupt"], L["n"] - L["n_interrupt"]],
              [O["n_interrupt"], O["n"] - O["n_interrupt"]]]
        res["stats"][f"fisher_L_vs_{other}_p"] = round(
            float(st.fisher_exact(t2, alternative="greater")[1]), 6)

    # ---- baseline, and the null V1 actually has to beat ---------------------
    gaps = np.diff(tk)
    res["baseline_gap"] = {p: round(float(np.percentile(gaps, p)), 4)
                           for p in (50, 75, 90, 95, 99)}

    # LENGTH BIAS.  V1 asks "how long is the silence CONTAINING this cast".  A
    # cast placed at a random TIME lands in a long gap preferentially -- the gap
    # is sampled proportional to its own duration.  The unweighted inter-tick
    # distribution is therefore the WRONG null for V1 and makes any cast look
    # interrupting.  The duration-weighted draw is the right one.
    rng = np.random.default_rng(11)
    draws = rng.choice(gaps, size=200000, p=gaps / gaps.sum())
    res["length_biased_null"] = {
        "median_s": round(float(np.median(draws)), 4),
        "p75_s": round(float(np.percentile(draws, 75)), 4),
        "p90_s": round(float(np.percentile(draws, 90)), 4),
        "share_ge_T_REL": round(float((draws >= T_REL).mean()), 4)}
    for s in list(CAST_SLOTS) + ["all"]:
        g = np.array([r["gap"] for r in conv
                      if r["gap"] is not None and (s == "all" or r["slot"] == s)])
        res["stats"][f"MW_gap_vs_lengthbiased_null_{s}"] = {
            "greater_p": float(f"{st.mannwhitneyu(g, draws, alternative='greater').pvalue:.4g}"),
            "less_p": float(f"{st.mannwhitneyu(g, draws, alternative='less').pvalue:.4g}"),
            "median_s": round(float(np.median(g)), 4)}
    res["stats"]["binom_V1_pooled_vs_lengthbiased"] = round(float(st.binomtest(
        res["partition"]["all"]["n_interrupt"], res["partition"]["all"]["n"],
        res["length_biased_null"]["share_ge_T_REL"], alternative="greater").pvalue), 4)
    res["stats"]["binom_V2_pooled_vs_clock_null"] = float(f"{st.binomtest(
        res['partition_release_matched']['all']['n_interrupt'],
        res['partition_release_matched']['all']['n'], null_p,
        alternative='greater').pvalue:.4g}")
    json.dump(res, open(out, "w"), indent=1)
    print(f"casts {C['n_casts']}  {C['per_slot']}   typeB {res['n_typeB']}/{len(rel)}")
    print("V1 containing-gap >= %.2f s" % T_REL)
    for k in list(CAST_SLOTS) + ["all"]:
        p = res["partition"][k]
        print(f"  slot {k:>3}: n={p['n']:>2}  hit {p['n_interrupt']:>2} ({p['p_interrupt']})"
              f"  blind {p['n_blind_gap']}  median gap {p['median_gap_s']}")
    print("V2 release-matched (+/-0.25 s)")
    for k in list(CAST_SLOTS) + ["not_L", "all"]:
        p = res["partition_release_matched"][k]
        print(f"  slot {k:>4}: n={p['n']:>2}  hit {p['n_interrupt']:>2} ({p['p_interrupt']})"
              f"  dur med {p['median_dur_s']}  non-int median gap {p['noninterrupt_median_gap_s']}")
    print("stats", json.dumps(res["stats"]))


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "casts":
        r = casts(sys.argv[2], sys.argv[3]); print(json.dumps(
            {k: v for k, v in r.items() if k != "casts"}, indent=1))
    elif c == "attrib":
        attrib(*sys.argv[2:8])
    else:
        sys.exit(__doc__)
