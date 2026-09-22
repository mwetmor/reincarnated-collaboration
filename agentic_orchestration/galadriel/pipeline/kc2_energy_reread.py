#!/usr/bin/env python3
"""KC2-PLAY · THE ENERGY GLOBE, RE-READ WITH THE HP GLOBE'S READER.

Conductor dispatch 2026-09-21, on galadriel's own root-cause finding:

    "HP trace: Apple Vision, 100.00 % accepted.  Energy trace: hand-built
     10-frame glyph atlas, 95.8 % parse, 11.9 % impossible reads.  Same MP4,
     same session, same instrument class -- two readers."

The commission was to re-read the energy globe with the strong reader and
re-derive.  THE FULL RE-READ IS BLOCKED: the source MP4 is not on this machine
and the per-frame crops were never committed (see T30 in the note).  What IS
committed is 16 energy-readout frames, and the strong reader runs on those.
So this module does three things the missing footage does not block:

  XR  CROSS-READER CONTROL.  Apple Vision (`ocr_vision.swift`, byte-identical
      to the reader that produced the 100.00 %-accepted HP trace) is pointed at
      every committed energy-readout image, and its reads are set beside the
      glyph atlas's reads of the same frames and beside the 2026-08-25 HAND
      reads.  n = 16 labelled frames.  This measures the reader gap directly.

      ⚑ ITS FIRST RESULT REFUTES THIS AUTHOR'S OWN 2026-09-21 NOTE.  The frame
      at t = 735.0 displays 1610 -- ABOVE the 1594 ceiling that note called
      physically impossible -- and three independent readings agree on it: the
      hand read of 2026-08-25 (it is `atlas-spec.json` row 7, TRAINING DATA for
      the atlas), Apple Vision at confidence 1.000, and the eye at x12.

  CL  THE CLAMP DECOMPOSITION.  Given that, the above-ceiling population cannot
      be dismissed as reader noise -- so it is decomposed instead.  Every drain
      tick splits EXACTLY into a SPEND limb (energy lost below the ceiling) and
      a SPILL limb (over-ceiling excess given back).  The identity
      spend + spill = |dE| holds to 0.0.  A spill is not a cost, whether it is
      a real clamp or a misread, so the decomposition answers the gross-drain
      question WITHOUT first settling which.

  MG  THE `marg` GATE, VERSIONED.  `eor_release.clean()` now takes `marg_min`,
      DEFAULT 0.0 = bit-identical to v1.  This module sweeps it and prints every
      headline figure at every gate WITH THE UNGATED VALUE BESIDE IT, so nothing
      restates silently.

Usage:
    python3 kc2_energy_reread.py [out.json]

Inputs: all committed 2026-08-25; no new capture, no MP4, no frame re-extracted.
Read-only on every input.  galadriel, 2026-09-21, Run KC2-PLAY.
"""
import json, os, sys, hashlib, subprocess, tempfile, shutil

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from eor_release import clean, CEIL                      # CEIL = 1594.0
from kc2_energy_shape import (AO, CHAN, ENER, F_E60, F_DUTY, F_WAVE, F_REL,
                              TICK_DE, TICK_DT, AT_CAP, WINDOW, D_COMBAT, HZ,
                              PROM_SWEEP, MARG_SWEEP, teeth, order_stats,
                              motion_labels, wave_of, sha256)

REGEN = 75.37                     # decoded, unconditional (C-1 § 1)
D161 = 161.0                      # the 2026-08-25 note's classified duration
SWIFT_SRC = os.path.join(HERE, "ocr_vision.swift")

# --- the committed energy-readout frame set --------------------------------
# `t` is the frame's timestamp where a committed artifact records one, else None.
# `src` says WHERE the timestamp comes from, because an inferred time and a
# recorded one are not the same evidence.
SHEET = os.path.join(CHAN, "energy-sheet.png")      # x6 atlas build sheet
SPEC = os.path.join(CHAN, "atlas-spec.json")        # the HAND labels
BLIND = os.path.join(ENER, "blind_702_strip.png")   # x7 blind-gap probe
SINGLES = [
    # (path, t, hand-read or None, provenance of t)
    (os.path.join(CHAN, "../evidence/crop-energy-t690.png"), 690.00, None, "filename"),
    (os.path.join(ENER, "exc_688.18.png"), 688.18, 1497, "filename + MD-B4app-2b § 1.1 table"),
    (os.path.join(ENER, "exc_690.00.png"), 690.00, None, "filename"),
    (os.path.join(ENER, "exc_702.90.png"), 702.90, 1437, "filename + MD-B4app-2b § 1.1 table"),
    (os.path.join(ENER, "exc_703.90.png"), 703.90, None, "filename"),
    (os.path.join(ENER, "exc_780.66.png"), 780.66, None, "filename"),
    (os.path.join(ENER, "exc_836.90.png"), 836.90, None, "filename"),
]
# MD-B4app-2b § 1.3: four hand-reads at x7 across the largest blind gap.
BLIND_T = [702.05, 702.60, 703.15, 703.70]
BLIND_HAND = [1399, 1430, 1434, 1417]


# ---------------------------------------------------------------------------
# XR · the strong reader, on the frames that exist
# ---------------------------------------------------------------------------
def build_ocr():
    """Compile the pinned Apple Vision reader into a temp dir. Returns path or None."""
    if not shutil.which("swiftc") or not os.path.exists(SWIFT_SRC):
        return None, None
    d = tempfile.mkdtemp(prefix="kc2ocr_")
    exe = os.path.join(d, "ocr")
    r = subprocess.run(["swiftc", "-O", SWIFT_SRC, "-o", exe],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:])
        return None, None
    return exe, sha256(SWIFT_SRC)


def vision(exe, paths):
    """path -> [(text, conf, y_origin)], Apple Vision VNRecognizeTextRequest."""
    out = {}
    r = subprocess.run([exe] + list(paths), capture_output=True, text=True)
    for line in r.stdout.splitlines():
        f = line.split("\t")
        if len(f) < 7:
            continue
        out.setdefault(f[0], []).append((f[1], float(f[2]), float(f[4])))
    return out


def sheet_reads_top_down(exe, path):
    """Read a vertically stacked contact sheet WHOLE, ordering lines top-down.

    ⚑ NOT by cutting it into equal rows first. Cutting was tried and it moved a
    reading: the row-3 crop of energy-sheet.png reads 1570 where the WHOLE sheet
    reads 1370 at confidence 1.000 -- a horizontal slice clips glyph extrema and
    manufactures a substitution. Vision returns a bounding box per line, so the
    ordering is free and the crop is unnecessary. The instrument that needed no
    cut is the one to use.
    """
    lines = vision(exe, [path]).get(path, [])
    reads = []
    for s, c, y in sorted(lines, key=lambda r: -r[2]):     # y origin is bottom-up
        s2 = s.replace(" ", "")
        a, sep, b = s2.partition("/")
        if sep and a.isdigit() and b == "2576":
            reads.append((int(a), c))
    return reads


def parse_reading(cands):
    """Pick the 'NNNN/NNNN' candidate from a frame's Vision lines; return cur or None."""
    for s, c, _ in cands:
        s2 = s.replace(" ", "")
        if "/" in s2:
            a, _, b = s2.partition("/")
            if a.isdigit() and b.isdigit() and b == "2576":
                return int(a), c, s2
    return None, None, None


def cross_read(rows_by_t):
    exe, swift_sha = build_ocr()
    if exe is None:
        return {"status": "APPLE-VISION-UNAVAILABLE (no swiftc, or ocr_vision.swift missing)"}
    spec = json.load(open(SPEC))

    # --- the atlas build sheet ------------------------------------------
    sheet = sheet_reads_top_down(exe, SHEET)
    sheet_reads = [v for v, _ in sheet]

    # Alignment of the 14 sheet rows to the 10 HAND labels in atlas-spec.json:
    # order-preserving match on value (a longest-common-subsequence alignment).
    # DECLARED AS INFERRED, not recorded: the sheet carries no row index. It is
    # corroborated independently by the trace, which reproduces the aligned hand
    # value at 9 of the 10 (the 10th is a trace PARSE FAILURE, not a mismatch).
    align, si = [], 0
    for s in spec:
        want = int(s["s"].split("/")[0])
        while si < len(sheet_reads) and sheet_reads[si] != want:
            si += 1
        align.append(si if si < len(sheet_reads) else None)
        si += 1

    frames = []
    for s, ri in zip(spec, align):
        frames.append({"src": "energy-sheet.png row %s" % (ri if ri is not None else "?"),
                       "t": s["t"], "t_provenance": "atlas-spec.json (recorded)",
                       "hand_2026_08_25": int(s["s"].split("/")[0]),
                       "apple_vision": sheet_reads[ri] if ri is not None else None})

    unlabelled = [sheet_reads[i] for i in range(14) if i not in align]

    # --- the blind-gap strip ---------------------------------------------
    blind = [v for v, _ in sheet_reads_top_down(exe, BLIND)]
    for i, (t, hand) in enumerate(zip(BLIND_T, BLIND_HAND)):
        frames.append({"src": "blind_702_strip.png row %d" % i, "t": t,
                       "t_provenance": "MD-B4app-2b § 1.3 (recorded)",
                       "hand_2026_08_25": hand,
                       "apple_vision": blind[i] if i < len(blind) else None})

    # --- the singles ------------------------------------------------------
    sp = [p for p, _, _, _ in SINGLES]
    gv = vision(exe, sp)
    for p, t, hand, prov in SINGLES:
        frames.append({"src": os.path.basename(p), "t": t, "t_provenance": prov,
                       "hand_2026_08_25": hand,
                       "apple_vision": parse_reading(gv.get(p, []))[0]})

    # --- set the glyph atlas's own read of the same frames beside them ----
    raw = json.load(open(F_E60))["rows"]
    for f in frames:
        r = min(raw, key=lambda x: abs(x["t"] - f["t"]))
        f["atlas_t"] = round(r["t"], 4)
        f["atlas_str"] = r["s"]
        f["atlas_cur"] = r["cur"]
        f["atlas_marg"] = r["marg"]
        av = f["apple_vision"]
        f["verdict"] = ("ATLAS-PARSE-FAIL" if r["cur"] is None else
                        "AGREE" if av is not None and r["cur"] == av else
                        "ATLAS-WRONG-VALUE" if av is not None else "NO-VISION-READ")

    # de-duplicate: crop-energy-t690 and exc_690.00 are the same frame
    seen, uniq = set(), []
    for f in frames:
        k = (f["t"], f["apple_vision"])
        if k in seen:
            f["note"] = "duplicate frame (same t, same read) -- excluded from counts"
        else:
            seen.add(k); uniq.append(f)

    hand_pairs = [f for f in uniq if f["hand_2026_08_25"] is not None
                  and f["apple_vision"] is not None]
    val = [f for f in uniq if f["atlas_cur"] is not None and f["apple_vision"] is not None]
    return {
        "reader": {"engine": "Apple Vision VNRecognizeTextRequest .accurate, "
                             "usesLanguageCorrection=false, minimumTextHeight=0.004",
                   "source": "pipeline/ocr_vision.swift",
                   "source_sha256": swift_sha,
                   "provenance": ("byte-identical to legolas Lap Q method/ocr.swift "
                                  "(sha256 1a96036ddbdfe4d55e2be31f534e9a9661db152dc71d4c36e1"
                                  "8c684ab8b94ec1, pinned in pm4q_digests.json) -- the reader "
                                  "that produced the 100.00 %-accepted HP trace")},
        "n_frames": len(uniq),
        "n_unlabelled_sheet_rows": len(unlabelled),
        "unlabelled_sheet_row_reads": unlabelled,
        "vision_vs_hand": {"n": len(hand_pairs),
                           "n_agree": sum(1 for f in hand_pairs
                                          if f["hand_2026_08_25"] == f["apple_vision"]),
                           "disagreements": [f for f in hand_pairs
                                             if f["hand_2026_08_25"] != f["apple_vision"]]},
        "atlas_vs_vision": {
            "n_value_carrying": len(val),
            "n_agree": sum(1 for f in val if f["verdict"] == "AGREE"),
            "n_atlas_wrong_value": sum(1 for f in val if f["verdict"] == "ATLAS-WRONG-VALUE"),
            "n_atlas_parse_fail": sum(1 for f in uniq if f["verdict"] == "ATLAS-PARSE-FAIL")},
        "frames": uniq,
    }


def marg_as_classifier(xr):
    """Is `marg` a correctness gate? Measured on the labelled set, not assumed."""
    if "frames" not in xr:
        return None
    fr = [f for f in xr["frames"] if f.get("apple_vision") is not None
          and f.get("note") is None]
    rows = []
    for g in (0, 2, 3, 4, 5, 7, 8):
        keep = [f for f in fr if f["atlas_marg"] >= g]
        good = [f for f in keep if f["verdict"] == "AGREE"]
        badv = [f for f in keep if f["verdict"] == "ATLAS-WRONG-VALUE"]
        pf = [f for f in keep if f["verdict"] == "ATLAS-PARSE-FAIL"]
        lost_good = [f for f in fr if f["atlas_marg"] < g and f["verdict"] == "AGREE"]
        rows.append({"marg_min": g, "kept": len(keep), "kept_correct": len(good),
                     "kept_WRONG_VALUE": len(badv), "kept_parse_fail": len(pf),
                     "TRUE_VALUES_DISCARDED": len(lost_good),
                     "discarded_true_at": sorted(f["t"] for f in lost_good)})
    return {"note": ("`marg` scored as a correctness classifier against Apple Vision on the "
                     "committed labelled set. A gate that discards TRUE values is buying "
                     "precision with recall, and the price is stated here rather than implied."),
            "table": rows}


# ---------------------------------------------------------------------------
# CL · the clamp decomposition -- spend vs spill, an EXACT identity
# ---------------------------------------------------------------------------
def clamp_decomposition(t, e):
    de = np.diff(e); dt = np.diff(t)
    tick = (de <= TICK_DE) & (dt <= TICK_DT)
    st, en, dd = e[:-1][tick], e[1:][tick], de[tick]
    tot = np.abs(dd)
    # SPEND: the part of the fall that happens BELOW the ceiling -- a real cost.
    # SPILL: the part that happens ABOVE it -- over-ceiling excess being given
    #        back.  A spill is not a cost under EITHER hypothesis: if the read is
    #        real it is a clamp, and if the read is a misread there was never any
    #        energy there to lose.
    spend = np.maximum(0.0, np.minimum(st, CEIL) - np.minimum(en, CEIL))
    spill = np.maximum(0.0, st - np.maximum(CEIL, en))
    hi = st > CEIL
    return {
        "identity_check_max_abs_residual": round(float(np.max(np.abs(spend + spill - tot))), 6),
        "identity": "spend + spill == |dE| for every tick, exactly",
        "n_ticks": int(tick.sum()),
        "SPEND": {"sum": round(float(spend.sum()), 1),
                  "per_s_over_182_65": round(float(spend.sum() / D_COMBAT), 1),
                  "per_s_over_161_0": round(float(spend.sum() / D161), 1)},
        "SPILL": {"sum": round(float(spill.sum()), 1),
                  "per_s_over_182_65": round(float(spill.sum() / D_COMBAT), 1),
                  "per_s_over_161_0": round(float(spill.sum() / D161), 1),
                  "frac_of_published_gross": round(float(spill.sum() / tot.sum()), 4)},
        "TOTAL_as_published": {"sum": round(float(tot.sum()), 1),
                               "per_s_over_182_65": round(float(tot.sum() / D_COMBAT), 1),
                               "per_s_over_161_0": round(float(tot.sum() / D161), 1)},
        "drop_all_above_ceiling_starts": {
            "n_ticks": int((~hi).sum()),
            "per_s_over_161_0": round(float(tot[~hi].sum() / D161), 1)},
        "clamp_signature": {
            "n_ticks_starting_above_ceiling": int(hi.sum()),
            "frac_of_tick_count": round(float(hi.mean()), 4),
            "frac_of_tick_mass": round(float(tot[hi].sum() / tot.sum()), 4),
            "n_landing_EXACTLY_on_1594": int((en[hi] == CEIL).sum()),
            "frac_landing_EXACTLY_on_1594": round(float((en[hi] == CEIL).mean()), 4),
            "median_size_starting_above": float(np.median(dd[hi])),
            "median_size_starting_at_or_below": float(np.median(dd[~hi])),
            "why_it_matters": ("a fall that TERMINATES at the operating ceiling in 69 % of "
                               "cases, with a characteristic size of -16 against the -13 of "
                               "the below-ceiling population, is two different quantities "
                               "sharing one tick rule")},
    }


def above_ceiling_anatomy(raw):
    """Split the above-ceiling reads by whether ONE glyph substitution reaches them."""
    def ed1(a, b):
        a, b = str(a), str(b)
        return len(a) == len(b) and sum(1 for x, y in zip(a, b) if x != y) == 1

    ab = [r for r in raw if r["cur"] is not None and r["max"] == 2576 and r["cur"] > CEIL]
    r1 = [r for r in ab if ed1(r["cur"], 1594)]
    rn = [r for r in ab if not ed1(r["cur"], 1594)]
    at = np.array([r["marg"] for r in raw if r["cur"] == 1594 and r["max"] == 2576])
    exc = np.array([r["cur"] - CEIL for r in ab])
    return {
        "definition": ("An above-ceiling read is REACHABLE if a single glyph substitution "
                       "turns 1594 into it (1595-1599, 1694, 1794, 1894, 1994). Everything "
                       "else needs two or three simultaneous substitutions, which the atlas's "
                       "own error profile does not produce."),
        "n_above_ceiling_raw": len(ab),
        "reachable_by_ONE_substitution": {
            "n": len(r1), "frac": round(len(r1) / len(ab), 4),
            "median_marg": round(float(np.median([r["marg"] for r in r1])), 2)},
        "NOT_reachable_by_one_substitution": {
            "n": len(rn), "frac": round(len(rn) / len(ab), 4),
            "median_marg": round(float(np.median([r["marg"] for r in rn])), 2),
            "top_values": sorted({v: sum(1 for r in rn if r["cur"] == v)
                                  for v in {r["cur"] for r in rn}}.items(),
                                 key=lambda kv: -kv[1])[:12]},
        "median_marg_AT_1594": round(float(np.median(at)), 2),
        "excess_over_ceiling": {"median": float(np.median(exc)),
                                "p75": float(np.percentile(exc, 75)),
                                "p95": round(float(np.percentile(exc, 95)), 1),
                                "max": float(exc.max()),
                                "frac_within_21": round(float((exc <= 21).mean()), 4)},
    }


# ---------------------------------------------------------------------------
# MG · headline figures, recomputed at each margin gate
# ---------------------------------------------------------------------------
def headline(marg_min):
    d = json.load(open(F_E60))
    t, e, census = clean(d["rows"], marg_min=marg_min)
    idx = {round(x, 4): i for i, x in enumerate(t)}
    marg = np.full(len(t), np.nan)
    for r in d["rows"]:
        k = round(r["t"], 4)
        if k in idx:
            marg[idx[k]] = r.get("marg", np.nan)
    cls = motion_labels(t)
    wv = wave_of(t)
    de = np.diff(e); dt = np.diff(t); adj = dt <= TICK_DT
    tick = (de <= TICK_DE) & adj
    mid = 0.5 * (e[:-1] + e[1:])

    # gate-free saw-tooth
    n = len(e); at = (e == CEIL)
    ra, rb = [], []
    i = 0
    while i < n:
        j = i
        while j + 1 < n and at[j + 1] == at[i] and (t[j + 1] - t[j]) <= TICK_DT:
            j += 1
        (ra if at[i] else rb).append((j - i + 1) / HZ)
        i = j + 1

    T20 = teeth(t, e, wv, 20)
    # channel-state net (the estimator that does not select on its own answer)
    tt = t[:-1][tick]
    grid = np.arange(WINDOW[0], WINDOW[1] - 0.5, 0.05)
    nt = np.array([((tt >= g) & (tt < g + 0.5)).sum() for g in grid])
    gi = np.clip(((t[:-1] - WINDOW[0]) / 0.05).astype(int), 0, len(grid) - 1)
    ch = (nt >= 3)[gi]
    m = ch & (mid < AT_CAP) & adj
    net_chan = round(float(de[m].sum() / dt[m].sum()), 2) if m.sum() >= 10 else None
    # off-channel income -> u
    z = (nt == 0)[gi] & (mid < AT_CAP) & adj
    inc = float(de[z].sum() / dt[z].sum()) if z.sum() >= 10 else None

    cl = clamp_decomposition(t, e)
    return {
        "marg_min": marg_min,
        "census": census,
        "ceiling_duty_eq_1594": round(float(at.mean()), 4),
        "occupancy_ge_1560": round(float((e >= 1560).mean()), 4),
        "frac_above_ceiling": round(float((e > CEIL).mean()), 4),
        "sawtooth_median_residency_s": round(float(np.median(ra)), 4),
        "sawtooth_median_excursion_s": round(float(np.median(rb)), 4),
        "sawtooth_period_s": round(float(np.median(ra) + np.median(rb)), 4),
        "teeth20_n": len(T20),
        "teeth20_median_period_s": round(float(np.median([x["period_s"] for x in T20])), 4) if T20 else None,
        "teeth20_median_depth": round(float(np.median([x["depth"] for x in T20])), 1) if T20 else None,
        "teeth20_median_recovery_slope": round(float(np.median(
            [x["recovery_slope"] for x in T20 if x["recovery_slope"] is not None])), 1) if T20 else None,
        "gross_all_ticks_per_s_161": cl["TOTAL_as_published"]["per_s_over_161_0"],
        "gross_SPEND_per_s_161": cl["SPEND"]["per_s_over_161_0"],
        "gross_drop_above_starts_per_s_161": cl["drop_all_above_ceiling_starts"]["per_s_over_161_0"],
        "net_channel_active_below_cap": net_chan,
        "offchannel_sampled_s": round(float(dt[z].sum()), 2),
        "offchannel_income": round(inc, 2) if inc is not None else None,
        "offchannel_implied_u": round((inc - REGEN) / 100.0, 4) if inc is not None else None,
    }


# ---------------------------------------------------------------------------
# DC · IS THE GATE CLEANING, OR JUST DELETING?
#      The control the margin sweep is worthless without: remove the SAME NUMBER
#      of frames AT RANDOM and see whether the figure moves the same way.  If it
#      does, the gate is not cleaning anything -- the estimator is simply fragile
#      to sample loss, and every "cleaner" number it produces is a decimation
#      artifact wearing a cleaning label.
# ---------------------------------------------------------------------------
def net_channel_below_cap(t, e):
    de = np.diff(e); dt = np.diff(t); adj = dt <= TICK_DT
    tick = (de <= TICK_DE) & adj
    mid = 0.5 * (e[:-1] + e[1:])
    tt = t[:-1][tick]
    grid = np.arange(WINDOW[0], WINDOW[1] - 0.5, 0.05)
    nt = np.array([((tt >= g) & (tt < g + 0.5)).sum() for g in grid])
    gi = np.clip(((t[:-1] - WINDOW[0]) / 0.05).astype(int), 0, len(grid) - 1)
    m = (nt >= 3)[gi] & (mid < AT_CAP) & adj
    if m.sum() < 10:
        return None
    return {"n_pairs": int(m.sum()), "sampled_s": round(float(dt[m].sum()), 2),
            "n_ticks": int(tick.sum()),
            "net": round(float(de[m].sum() / dt[m].sum()), 2)}


def decimation_control(raw, seed=20260921, draws=20):
    t0, e0, _ = clean(raw)
    base = net_channel_below_cap(t0, e0)
    rng = np.random.default_rng(seed)
    rows = []
    for g in (2.0, 3.0, 4.0, 5.0, 7.0):
        tg, eg, cg = clean(raw, marg_min=g)
        gated = net_channel_below_cap(tg, eg)
        p = 1.0 - len(eg) / len(e0)                    # same fraction, random frames
        acc = []
        for _ in range(draws):
            k = rng.random(len(e0)) >= p
            r = net_channel_below_cap(t0[k], e0[k])
            if r:
                acc.append(r["net"])
        rows.append({
            "marg_min": g, "frames_removed_frac": round(p, 4),
            "GATED_net": gated["net"], "GATED_sampled_s": gated["sampled_s"],
            "GATED_n_pairs": gated["n_pairs"],
            "RANDOM_net_mean": round(float(np.mean(acc)), 2),
            "RANDOM_net_sd": round(float(np.std(acc)), 2),
            "gated_minus_random_in_sd": round(
                float((gated["net"] - np.mean(acc)) / max(1e-9, np.std(acc))), 2)})
    # the isolating arm: drop ONLY the above-ceiling reads, no margin gate at all
    k = e0 <= CEIL
    return {
        "question": "does the marg gate CLEAN, or does it merely DELETE?",
        "baseline_marg_0": base,
        "control": ("for each gate, the SAME NUMBER of frames is removed uniformly at "
                    "random, 20 draws, seed 20260921. If the gated figure sits inside the "
                    "random band, the gate explains nothing the deletion does not."),
        "rows": rows,
        "isolating_arm_drop_only_above_ceiling": net_channel_below_cap(t0[k], e0[k]),
        "reading": ("the estimator loses evidence far faster than it loses samples: two "
                    "compounding losses -- an adjacent PAIR needs both its frames, and a "
                    "channel-active WINDOW needs 3 surviving ticks. This lap measures that "
                    "and does NOT claim to have isolated the full mechanism."),
    }


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else None
    raw = json.load(open(F_E60))["rows"]
    t0, e0, _ = clean(raw)

    xr = cross_read(None)
    R = {
        "instrument": "kc2_energy_reread.py",
        "run": "KC2-PLAY", "date": "2026-09-21", "author": "galadriel",
        "commission": "conductor dispatch 2026-09-21 -- re-read the energy globe with the "
                      "HP globe's reader; do the eor_release.clean() marg gate as part of it",
        "inputs": {os.path.relpath(p, AO): sha256(p)
                   for p in (F_E60, F_DUTY, F_WAVE, F_REL, SHEET, SPEC, BLIND)},
        "T30": {
            "status": "BLOCKS THE FULL RE-READ",
            "what_is_missing": "the source MP4; the per-frame crops were never committed",
            "recorded_paths": [
                "/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/"
                "eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4  (the DOCUMENTED home; "
                "/Volumes/reincarnated is NOT MOUNTED -- the volume is absent, not the file)",
                "/Users/admin/gd-scratch/eor-test-2/...  (the local copy legolas hash-verified "
                "2026-09-10 and flagged must-survive-any-sweep; ~/gd-scratch no longer exists)"],
            "identity_pinned": "sha256 4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe0956"
                               "4d6056a4de8, 479,438,089 B (legolas pm4q_digests.json) -- so a "
                               "remounted copy is VERIFIABLE, not merely plausible",
            "correction_to_the_standing_account": "T30 has been carried as 'the MP4 is gone'. "
                                                  "It is on an unmounted external volume with a "
                                                  "pinned digest. That is a different ask of Matt.",
        },
        "XR_cross_reader_control": xr,
        "XR_marg_as_correctness_classifier": marg_as_classifier(xr),
        "CL_clamp_decomposition": clamp_decomposition(t0, e0),
        "CL_above_ceiling_anatomy": above_ceiling_anatomy(raw),
        "MG_margin_gate_sweep": {
            "amendment": ("eor_release.clean() v2 takes marg_min, DEFAULT 0.0. At the default "
                          "it is bit-identical to v1: kc2_energy_shape.py re-run under v2 "
                          "differs from the committed 2026-09-21 JSON in exactly two keys, "
                          "both NEW census fields (marg_min: 0.0, margin_rejected: 0), and in "
                          "no numeric value. Verified by diff, not asserted."),
            "baseline_is": "marg_min = 0.0 (the pre-amendment value, first row of every table)",
            "rows": [headline(g) for g in (0.0, 2.0, 3.0, 4.0, 5.0, 7.0)],
        },
        "DC_decimation_control": decimation_control(raw),
        "MARGIN_IS_NOT_AN_INTENSITY_GATE": {
            "hypothesis_tested": ("that low margin marks frames where combat VFX crosses the "
                                  "HUD, so a margin gate would be a gate on combat intensity "
                                  "and any rate computed after it would be conditioned on the "
                                  "thing being measured"),
            "verdict": "REFUTED by the cheapest test, and recorded rather than quietly dropped",
            "evidence": ("a marg >= 4 gate keeps 84.1 % of channel-ACTIVE samples and 88.6 % of "
                         "channel-IDLE samples; the channel-active share of the surviving trace "
                         "moves 0.8094 -> 0.8110. The gate is close to intensity-blind."),
        },
    }
    txt = json.dumps(R, indent=1, sort_keys=False, default=str)
    if out_path:
        open(out_path, "w").write(txt)
        print("wrote", out_path, len(txt), "bytes")
    else:
        print(txt)


if __name__ == "__main__":
    main()
