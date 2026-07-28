#!/usr/bin/env python3
"""T-B step 2 -- damage-intake extraction over the 106 engagement windows.

INSTRUMENT
  The health-globe numerals, and nothing else. Globe FILL-FRACTION was
  REJECTED in round-1 calibration (4.6 pp of motion against a 90.5 pp null
  band). It is not consulted here, not even as a tie-break. Digit templates
  are the committed `globe-digit-templates.json`, proven at 98.2% coverage
  over the 58 s death window at 60 fps.

RATE
  15 fps. Sufficient by measurement, not by assumption: the poison DoT tick
  period measured 1.000 s (sd 0.072) over 57 identical ticks, so an intake
  event is resolved 15x over.

STANDING DISCIPLINE HONOURED HERE
  1. EVERY reader emits its own coverage. Per-window coverage, per-regime
     coverage, and a full refusal-code histogram ride with every number.
     A reader returning a plausible value without announcing coverage is the
     failure mode this program keeps catching (five D-1 instances last cycle).
  2. NO INTERPOLATION. A frame the reader could not read is a REFUSAL. It is
     never filled, never carried forward, never averaged across.
  3. NO MEASUREMENT STRETCH SPANS A LOADING SCREEN. A run of >2 s of
     no-ink frames self-identifies as a loading screen / clock break and
     splits the window into independent stretches. Deltas never cross one.
  4. Isolated OCR excursions are DEMOTED TO REFUSALS, not corrected. If
     frame i deviates hugely from both neighbours while the neighbours agree
     with each other, frame i is marked OCRSPIKE and dropped from the series.
     The count is reported; it is never silently repaired.

MEASUREMENT MODEL
  A delta is admissible only between two OK reads whose timestamps are
  <= ADJ_TOL apart and which lie in the same stretch. Negative deltas are
  intake; positive deltas are in-combat healing (all sources -- never call it
  "regen"). Everything else is uncovered time and is declared as such.
"""
import argparse
import json
import multiprocessing as mp
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from globe_ocr import CROP, mask_of, segments, iou, GlobeReader  # noqa: E402

FPS = 15.0
ADJ_TOL = 0.2001          # 3 frames at 15 fps
LOADING_MIN_S = 2.0       # >2 s of no-ink self-identifies as a loading screen
MIN_IOU = 0.72
MAX_EVERY = 5             # attempt the full "cur/max" read every Nth frame
SPIKE_ABS = 60            # HP; excursion size that triggers the spike test
SPIKE_NEIGH = 8           # HP; how closely the two neighbours must agree


def stream(video, ss, dur, fps=FPS, threads=2):
    c = CROP
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-threads", str(threads), "-ss", f"{ss:.4f}", "-i", video,
           "-t", f"{dur:.4f}",
           "-vf", f"fps={fps},crop={c['w']}:{c['h']}:{c['x']}:{c['y']}",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = c["h"] * c["w"] * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 16)
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield i, np.frombuffer(b, dtype=np.uint8).reshape(c["h"], c["w"], 3)
        i += 1
    p.stdout.close()
    p.wait()


class SubGlobeReader(GlobeReader):
    """GlobeReader.read() crops from a full frame; we already stream crops.
    Subclassed rather than editing the committed, reproducibility-verified
    globe_ocr.py."""

    def read_sub(self, sub):
        f = np.zeros((CROP["y"] + CROP["h"], CROP["x"] + CROP["w"], 3),
                     dtype=sub.dtype)
        f[CROP["y"]:, CROP["x"]:] = sub
        pair, _s, _c = self.read(f)
        return pair


BAND_MIN_H = 10           # glyph band height at native scale is 12 rows
BAND_MAX_H = 16
SLASH_IOU = 0.80


def _best_at(band, x, tl, dxs):
    """Best (iou, width, dx) for one character's template list at column x."""
    H = band.shape[0]
    bv, bw, bdx = -1.0, 0, 0
    for t in tl:
        th, tw = t.shape
        for dx in dxs:
            if x + dx < 0 or x + dx + tw > band.shape[1]:
                continue
            tt = t
            if th != H:
                tt = t[:H] if th > H else np.vstack(
                    [t, np.zeros((H - th, tw), bool)])
            v = iou(band[:, x + dx:x + dx + tw], tt)
            if v > bv:
                bv, bw, bdx = v, tw, dx
    return bv, bw, bdx


GREEDY_MIN_IOU = 0.85     # stricter than MIN_IOU: greedy is the FALLBACK path


def read_left_seg(band, tmpl):
    """Round-1's per-segment reader, unchanged. PRIMARY path.

    Kept verbatim because it is the validated one: against the committed
    60 fps death-window series it holds 89.5% coverage and 97.7% agreement.
    Replacing it wholesale with the greedy reader REGRESSED that window to
    79.9% coverage, so greedy is added as a fallback, not a replacement.
    """
    segs = [(a, b) for a, b in segments(band)
            if b - a + 1 >= 2 and band[:, a:b + 1].sum() >= 8]
    if len(segs) < 4:
        return None, 0.0, "NSEG%d" % len(segs)
    out, confs = [], []
    for a, b in segs:
        g = band[:, a:b + 1]
        best, bv = None, -1.0
        for ch, tl in tmpl.items():
            for t in tl:
                v = iou(g, t)
                if v > bv:
                    best, bv = ch, v
        if best == "/" or (b - a + 1) > 10:
            break
        if bv < MIN_IOU or best is None or not best.isdigit():
            return None, bv, "LOWCONF"
        out.append(best)
        confs.append(bv)
        if len(out) > 4:
            return None, min(confs), "TOOLONG"
    if not out:
        return None, 0.0, "NODIG"
    return int("".join(out)), min(confs), "OK"


def read_left(sub, tmpl):
    """Current-HP (left operand). Segmented primary + GREEDY fallback.

    Round-1's per-segment reader was safe "HERE and only here" (the death
    window, where the three current-HP digits are separated by >=3 blank
    columns). Over the full run it is NOT safe: the first T-B pass returned
    NODIG on 1,485 frames (7.7%), every one of them a frame where the leading
    two glyphs TOUCH -- "747/747" segments as a single 17 px blob followed by
    7 / 7 4 7, and the reader's >10 px terminator fired before it had read a
    single digit. Greedy matching at native glyph width splits the blob
    ('7' then '4', both at IoU >= 0.97) and the run is recovered.

    Terminator is the '/' template, matched at native width -- which also
    resolves the documented '/'+digit merge, because the slash template only
    needs the merged blob's first 5-6 columns.

    Band-height gate: the native glyph band is 12 rows. Frames where a bright
    golden HUD overlay swallows the glyph tops present an 6-8 row band; those
    are REFUSED (code FLASH), not read against half a glyph.
    """
    m = mask_of(sub)
    ys, xs = np.nonzero(m)
    if not len(ys):
        return None, 0.0, "NO_INK"
    y0, y1 = ys.min(), ys.max()
    h = y1 - y0 + 1
    if h > BAND_MAX_H:
        return None, 0.0, "TALL"
    if h < BAND_MIN_H:
        return None, 0.0, "FLASH"
    band = m[y0:y1 + 1]
    hp, conf, st = read_left_seg(band, tmpl)
    if st == "OK":
        return hp, conf, st
    if st.startswith("NSEG") or st == "TOOLONG":
        return hp, conf, st                        # not a merge signature
    seg_st = st
    tdig = {k: v for k, v in tmpl.items() if k.isdigit()}
    tsla = tmpl.get("/", [])
    x, xmax = int(xs.min()), int(xs.max())
    out, confs = [], []
    while x <= xmax:
        dxs = (0,) if not out else (0, 1, 2, -1)
        if out and tsla:
            vs, ws, dxs_ = _best_at(band, x, tsla, dxs)
            if vs >= SLASH_IOU:
                break                              # left operand complete
        bch, bv, bw, bdx = None, -1.0, 0, 0
        for ch, tl in tdig.items():
            v, w, dx = _best_at(band, x, tl, dxs)
            if v > bv:
                bch, bv, bw, bdx = ch, v, w, dx
        if bch is None or bv < GREEDY_MIN_IOU:
            return None, max(bv, 0.0), seg_st
        out.append(bch)
        confs.append(bv)
        x += bdx + bw
        if len(out) > 4:
            return None, min(confs), seg_st
        col = band[:, x:x + 6].sum(axis=0)
        k = 0
        while k < len(col) and col[k] == 0:
            k += 1
        if k >= 5:                                 # nothing further to read
            break
        x += k
    if not out:
        return None, 0.0, seg_st
    return int("".join(out)), min(confs), "OK_GREEDY"


def demote_truncations(series):
    """Prefix-truncation demotion -> REFUSAL (never a repair).

    Observed failure (smoke, eng 103): eight consecutive frames read `1`
    between neighbouring reads of 1407 and 1430 -- the segmenter stopped after
    the leading glyph and the reader returned a PLAUSIBLE INTEGER without
    announcing that it had truncated. That is precisely the D-1 shape this
    program keeps catching, and it would have injected a -1406 intake event
    and a +1429 heal into an engagement whose true max HP is 1600.

    Rule: a read with FEWER digits than the last accepted read, whose decimal
    string is a strict PREFIX of that read, is a truncation. Demote it. A
    genuine drop landing exactly on a decimal prefix of the prior value is a
    measure-zero coincidence against the truncation prior; and demotion costs
    a sample, whereas acceptance invents a measurement.
    """
    n, last = 0, None
    for s in series:
        if s["st"] != "OK":
            continue
        cur = str(s["hp"])
        if last is not None and len(cur) < len(last) and last.startswith(cur):
            s["st"] = "TRUNC"
            s["hp"] = None
            n += 1
            continue
        last = cur
    return n


SPIKE_MAX_RUN = 4         # <= 0.27 s; longer excursions are not excursions
SPIKE_FLANK_FRAC = 0.25   # flanks must agree to within this x the excursion


def demote_spikes(series):
    """Isolated OCR excursions -> REFUSALS (never corrections). RUN-AWARE.

    The first full pass shipped a 3-frame version of this test with a tight
    flank-agreement bound (<=8 HP) and it MISSED four real excursions, e.g.
    1600 -> 15 -> 1543 and 1511 -> 13 -> 13 -> 1375. Both are glyph-loss on a
    4-digit HP string; neither value is a prefix of its predecessor, so the
    truncation guard did not see them either; and each would have injected a
    ~1,500 HP intake event into R3 -- an entire effective health pool of
    phantom damage, in the thinnest regime, exactly where it does most harm.

    Generalised rule: a RUN of at most SPIKE_MAX_RUN consecutive OK reads,
    flanked by accepted reads a and c, is demoted when every value in the run
    deviates from BOTH flanks by >= SPIKE_ABS and the two flanks agree with
    each other to within SPIKE_FLANK_FRAC of that deviation. A player who
    genuinely lost 1,585 HP and recovered it inside 0.13 s did not happen; a
    reader that dropped two glyphs for two frames did.

    A real death is NOT caught by this: HP goes to 0 and STAYS there, so no
    flanking high read ever closes the run. The death window validates it --
    intake there is 570 HP = exactly 57 x -10 HP, the independently measured
    DoT tick count, with zero spike demotions.
    """
    idx = [i for i, s in enumerate(series) if s["st"] == "OK"]
    n, k = 0, 1
    while k < len(idx) - 1:
        a = series[idx[k - 1]]
        if a["st"] != "OK":
            k += 1
            continue
        hit = 0
        for L in range(1, SPIKE_MAX_RUN + 1):
            if k + L >= len(idx):
                break
            run = [series[idx[j]] for j in range(k, k + L)]
            c = series[idx[k + L]]
            if c["t"] - a["t"] > (L + 2) * ADJ_TOL:
                break
            dev = min(min(abs(r["hp"] - a["hp"]), abs(r["hp"] - c["hp"]))
                      for r in run)
            if dev < SPIKE_ABS:
                continue
            if abs(a["hp"] - c["hp"]) < SPIKE_FLANK_FRAC * dev:
                for r in run:
                    r["st"] = "OCRSPIKE"
                    r["hp"] = None
                n += L
                hit = L
                break
        k += hit + 1
    return n


def stretches(series):
    """Split on loading screens / clock breaks.

    Verdict SS8.5 + wind-down SS1.5: a loading screen self-identifies as a
    >2 s UNREADABLE run, and the same runs independently found the fitted
    clock breaks. No measurement stretch may span one. Any run of >2 s of
    non-OK frames is treated as a break (not only NO_INK ones) -- a transition
    that produces NODIG or LOWCONF for two seconds is no more measurable than
    one that produces black.
    """
    breaks, run0, run1, codes = [], None, None, None
    for s in series:
        if s["st"] != "OK":
            if run0 is None:
                run0, codes = s["t"], {}
            run1 = s["t"]
            codes[s["st"]] = codes.get(s["st"], 0) + 1
        else:
            if run0 is not None and (run1 - run0) > LOADING_MIN_S:
                breaks.append((run0, run1, max(codes, key=codes.get)))
            run0 = None
    if run0 is not None and (run1 - run0) > LOADING_MIN_S:
        breaks.append((run0, run1, max(codes, key=codes.get)))
    return breaks


def do_window(job):
    video, tmpl_path, w = job
    tmpl = {k: [np.array(b, dtype=bool) for b in v]
            for k, v in json.load(open(tmpl_path)).items()}
    gr = SubGlobeReader(json.load(open(tmpl_path)))
    ss, dur = w["cap_start"], w["cap_dur"]
    series, maxes, n_greedy = [], [], 0
    for i, sub in stream(video, ss, dur):
        t = round(ss + i / FPS, 4)
        hp, conf, st = read_left(sub, tmpl)
        # the greedy fallback is a READ, not a lesser read: it is folded into
        # OK for every downstream computation and its count is declared
        # separately so the two paths stay auditable.
        greedy = st == "OK_GREEDY"
        if greedy:
            st = "OK"
            n_greedy += 1
        series.append(dict(t=t, hp=hp, raw=hp, conf=round(float(conf), 3),
                           st=st, g=1 if greedy else 0))
        if st == "OK" and i % MAX_EVERY == 0:
            # full "cur/max" read on a sparse subsample; used ONLY to label
            # the window's max-HP for normalisation, never as a measurement.
            pair = gr.read_sub(sub)
            if pair is not None and pair[0] == hp:
                maxes.append(pair[1])
    n_exp = int(round(dur * FPS))
    n_trunc = demote_truncations(series)
    n_spike = demote_spikes(series)
    brks = stretches(series)
    ok = [s for s in series if s["st"] == "OK"]
    cov = len(ok) / len(series) if series else 0.0

    # deltas -- admissible only inside a stretch, between adjacent OK reads
    def in_break(t0, t1):
        return any(not (t1 <= b[0] or t0 >= b[1]) for b in brks)

    intake, healed, drops, heals = 0, 0, [], []
    covered_s, pairs, bridged = 0.0, 0, 0
    for a, b in zip(ok, ok[1:]):
        dt = b["t"] - a["t"]
        if dt > ADJ_TOL or in_break(a["t"], b["t"]):
            continue
        if dt > 1.5 / FPS:
            bridged += 1
        d = b["hp"] - a["hp"]
        pairs += 1
        covered_s += dt
        if d < 0:
            intake += -d
            drops.append(-d)
        elif d > 0:
            healed += d
            heals.append(d)
    hist = {}
    for s in series:
        hist[s["st"]] = hist.get(s["st"], 0) + 1
    rec = dict(w)
    rec.update(
        n_frames_expected=n_exp, n_frames_decoded=len(series),
        n_ok=len(ok), coverage=round(cov, 4),
        delta_covered_s=round(covered_s, 3),
        delta_coverage=round(covered_s / dur, 4) if dur else 0.0,
        n_pairs=pairs, n_bridged_pairs=bridged,
        n_ocrspike_demoted=n_spike, n_trunc_demoted=n_trunc,
        n_greedy_path=n_greedy,
        unreadable_breaks=[[round(b[0], 2), round(b[1], 2), b[2]]
                           for b in brks],
        unreadable_break_s=round(sum(b[1] - b[0] for b in brks), 2),
        refusal_hist=hist,
        hp_first=ok[0]["hp"] if ok else None,
        hp_last=ok[-1]["hp"] if ok else None,
        hp_min=min(s["hp"] for s in ok) if ok else None,
        hp_max_seen=max(s["hp"] for s in ok) if ok else None,
        max_hp_modal=(max(set(maxes), key=maxes.count) if maxes else None),
        max_hp_n_reads=len(maxes),
        max_hp_unanimity=(round(maxes.count(max(set(maxes), key=maxes.count))
                                / len(maxes), 3) if maxes else None),
        intake_hp=intake, healed_hp=healed,
        n_drops=len(drops), n_heals=len(heals),
        drop_max=max(drops) if drops else 0,
        drop_p50=int(np.median(drops)) if drops else 0,
        drops=drops)
    return rec, series


def _worker(job):
    try:
        return do_window(job)
    except Exception as e:                                # pragma: no cover
        return (dict(job[2], error=repr(e)), [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--templates", required=True)
    ap.add_argument("--windows", required=True)
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--procs", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    W = json.load(open(args.windows))["windows"]
    if args.only:
        keep = set(int(x) for x in args.only.split(","))
        W = [w for w in W if w["eng_id"] in keep]
    if args.limit:
        W = W[:args.limit]
    jobs = [(args.video, args.templates, w) for w in W]
    recs = []
    with open(args.out_prefix + "-frames.jsonl", "w") as fh, \
            mp.Pool(args.procs) as pool:
        for k, (rec, series) in enumerate(
                pool.imap_unordered(_worker, jobs, chunksize=1)):
            recs.append(rec)
            for s in series:
                s["eng"] = rec["eng_id"]
                fh.write(json.dumps(s) + "\n")
            print("  [%d/%d] eng=%d reg=%s cov=%.3f intake=%s" % (
                k + 1, len(jobs), rec["eng_id"], rec.get("regime"),
                rec.get("coverage", -1), rec.get("intake_hp")),
                file=sys.stderr, flush=True)
    recs.sort(key=lambda r: r["eng_id"])
    json.dump(dict(fps=FPS, adj_tol_s=ADJ_TOL,
                   loading_min_s=LOADING_MIN_S, min_iou=MIN_IOU,
                   windows=recs),
              open(args.out_prefix + "-windows.json", "w"), indent=1)
    tot = sum(r["n_frames_decoded"] for r in recs)
    ok = sum(r["n_ok"] for r in recs)
    print("TOTAL frames=%d ok=%d coverage=%.4f" % (tot, ok, ok / max(tot, 1)))


if __name__ == "__main__":
    main()
