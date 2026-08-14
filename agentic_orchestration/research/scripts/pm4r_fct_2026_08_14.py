#!/usr/bin/env python3
"""KC2-PM4 Lap R — LIMB A: the referent's contact/dry profile from floating-combat-text.

TWO PASSES, both pre-registered (PREREGISTRATION.md sha256 dc49d0ba...cec10):
  PASS 1  existing Lap N bytes, 95 frames @ 2.0 s cadence  (cheapest measurement, fires first)
  PASS 2  dense re-sample, 366 frames @ 0.5 s cadence      (below the measured FCT lifetime)

Emits: pm4r_fct_gaps.csv, plus JSON summary to /tmp/pm4r/limb_a.json for the findings writer.

READ-ONLY.  OUTCOME-FIREWALLED: no simulation output is opened.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4r_lib_2026_08_14 import (                                             # noqa: E402
    LAPN, OUT, FIGHT_T0, FIGHT_T1, WAVE_START, WAVE_END, SWEEP_RUNGS_S,
    FCT_LIFETIME_S, FCT_LIFETIME_BAND, classify, colour_class, parse_damage,
    p_out, gap_runs, sweep, wave_of, verify_pinned, sha256, dump_csv,
)

DENSE_TSV = pathlib.Path("/tmp/pm4r/dense_ocr.tsv")
DENSE_T0, DENSE_DT = 683.0, 0.5

_img_cache: dict = {}


def swatch(path: str, bx: float, by: float, bw: float, bh: float):
    """Lap N's colour probe, imported unchanged: mean RGB of the brightest 12 % of pixels
    inside the OCR bounding box (glyph strokes, not background)."""
    if path not in _img_cache:
        if len(_img_cache) > 4:
            _img_cache.clear()
        _img_cache[path] = np.asarray(Image.open(path).convert("RGB"))
    im = _img_cache[path]
    H, W, _ = im.shape
    x0, x1 = int(bx * W), int((bx + bw) * W)
    y1, y0 = int((1 - by) * H), int((1 - by - bh) * H)
    x0, x1 = max(0, x0), min(W, x1)
    y0, y1 = max(0, y0), min(H, y1)
    if x1 <= x0 or y1 <= y0:
        return None
    p = im[y0:y1, x0:x1].reshape(-1, 3).astype(float)
    sel = p[p.sum(1) >= np.percentile(p.sum(1), 88)]
    return sel.mean(0)


def load_pass1():
    obs = []
    with open(LAPN / "pm4n_fct_events.csv") as fh:
        for r in csv.DictReader(fh):
            obs.append(dict(
                frame=int(r["frame"]), t_sec=float(r["t_sec"]), text=r["text"],
                cls=r["cls"], colour_class=r["colour_class"],
                bbox_x=float(r["bbox_x"]), bbox_y=float(r["bbox_y"]),
                damage=(int(r["damage"]) if r["damage"] not in ("", None) else None),
            ))
    frames = sorted({o["frame"] for o in obs})
    times = [680.0 + 2.0 * f for f in frames]
    return obs, frames, times, 2.0


def load_pass2():
    raw = []
    for ln in open(DENSE_TSV):
        f = ln.rstrip("\n").split("\t")
        if len(f) >= 7:
            raw.append(f)
    obs = []
    # group by image so the PIL cache is hit once per frame
    raw.sort(key=lambda f: f[0])
    for path, text, conf, bx, by, bw, bh in raw:
        bx, by, bw, bh = map(float, (bx, by, bw, bh))
        if not path.startswith("/"):
            path = str(pathlib.Path("/tmp/pm4r") / path)
        fi = int(pathlib.Path(path).stem[1:])
        c = swatch(path, bx, by, bw, bh)
        if c is None:
            continue
        r, g, b = c
        cls = classify(text, bx, by)
        obs.append(dict(
            frame=fi, t_sec=round(DENSE_T0 + DENSE_DT * fi, 3), text=text,
            ocr_conf=float(conf), cls=cls, colour_class=colour_class(r, g),
            bbox_x=round(bx, 5), bbox_y=round(by, 5),
            damage=parse_damage(text) if cls in ("crit", "bare", "crit_garbled") else None,
            rgb_r=round(r, 1), rgb_g=round(g, 1), rgb_b=round(b, 1),
        ))
    frames = sorted({o["frame"] for o in obs})
    times = [round(DENSE_T0 + DENSE_DT * f, 3) for f in frames]
    return obs, frames, times, DENSE_DT


def analyse(tag, obs, frames, times, cadence, t_lo, t_hi):
    """The whole limb-A analysis for one pass.  Every threshold pre-registered."""
    n_frames = len(frames)
    hits, static = p_out(obs, n_frames)
    # restrict to the analysis span
    keep_f = [f for f, t in zip(frames, times) if t_lo - 1e-6 <= t <= t_hi + 1e-6]
    keep_t = [t for t in times if t_lo - 1e-6 <= t <= t_hi + 1e-6]
    hit_frames = {h["frame"] for h in hits}
    dry = [f not in hit_frames for f in keep_f]

    runs = gap_runs(keep_t, dry, cadence)
    rows = []
    for (ta, tb, n) in runs:
        # `raw`   = sample-coverage of the dry run  (n samples x cadence) -- the naive read that
        #           makes the per-gap durations sum to dry_sample_fraction * span.
        # `proven`= the interval the FCT lifetime GUARANTEES carried no landed damage:
        #           text absent at t_first..t_last  =>  nothing landed in [t_first - L, t_last],
        #           length (n-1)*cadence + L.  This is a MEASURED interval, not a "correction".
        raw_dur = n * cadence
        proven = (tb - ta) + FCT_LIFETIME_S
        w, w_end = wave_of(ta), wave_of(tb)
        rows.append(dict(
            pass_tag=tag, cadence_s=cadence,
            t_first_dry_sample=round(ta, 3), t_last_dry_sample=round(tb, 3),
            n_dry_samples=n,
            gap_raw_s=round(raw_dur, 4),
            gap_lifetime_corrected_s=round(proven, 4),
            gap_corr_lo_s=round((tb - ta) + FCT_LIFETIME_BAND[0], 4),
            gap_corr_hi_s=round((tb - ta) + FCT_LIFETIME_BAND[1], 4),
            t_proven_start=round(ta - FCT_LIFETIME_S, 3), t_proven_end=round(tb, 3),
            wave_at_start=w, wave_at_end=w_end,
            straddles_wave_boundary=int(w != w_end),
        ))
    total = t_hi - t_lo + cadence
    raw_gaps = [r["gap_raw_s"] for r in rows]
    cor_gaps = [r["gap_lifetime_corrected_s"] for r in rows]

    # UNION of the proven no-damage intervals -- merged, so overlapping proven windows are
    # never double-counted (they overlap whenever two dry runs sit < L apart).
    iv = sorted((r["t_proven_start"], r["t_proven_end"]) for r in rows)
    union, ulen = [], 0.0
    for a, b in iv:
        if union and a <= union[-1][1]:
            union[-1] = (union[-1][0], max(union[-1][1], b))
        else:
            union.append((a, b))
    ulen = sum(b - a for a, b in union)
    res = dict(
        tag=tag, cadence_s=cadence, span=[t_lo, t_hi], n_samples=len(keep_f),
        n_pout_observations=len(hits),
        n_static_positions_excluded=len(static),
        static_positions=sorted(str(s) for s in static),
        n_dry_samples=int(sum(dry)),
        dry_sample_fraction=round(float(sum(dry)) / len(keep_f), 6),
        n_gaps=len(rows),
        longest_gap_raw_s=round(max(raw_gaps), 4) if raw_gaps else 0.0,
        longest_gap_corr_s=round(max(cor_gaps), 4) if cor_gaps else 0.0,
        median_gap_raw_s=round(float(np.median(raw_gaps)), 4) if raw_gaps else None,
        total_dry_time_raw_s=round(float(sum(raw_gaps)), 4),
        total_span_s=round(total, 4),
        proven_no_damage_union_s=round(ulen, 4),
        proven_no_damage_union_frac=round(ulen / total, 6),
        n_union_intervals=len(union),
        sweep_raw=sweep(raw_gaps, total),
        sweep_lifetime_corrected=sweep(cor_gaps, total),
    )
    return rows, res, hits, dry, keep_t


def per_wave(tag, rows, hits, keep_t, dry, cadence):
    out = []
    for w in sorted(WAVE_START):
        a, b = WAVE_START[w], WAVE_END[w]
        idx = [i for i, t in enumerate(keep_t) if a <= t < b]
        if not idx:
            continue
        nd = sum(1 for i in idx if dry[i])
        wr = [r for r in rows if r["wave_at_start"] == w]
        raw = [r["gap_raw_s"] for r in wr]
        out.append(dict(
            pass_tag=tag, wave=w, t_start=a, t_end=round(b, 3), span_s=round(b - a, 3),
            n_samples=len(idx), n_dry_samples=nd,
            dry_sample_fraction=round(nd / len(idx), 6),
            n_gaps=len(wr),
            longest_gap_raw_s=round(max(raw), 4) if raw else 0.0,
            longest_gap_corr_s=round(max(raw) + FCT_LIFETIME_S, 4) if raw else 0.0,
            n_pout_events=sum(1 for h in hits if a <= h["t_sec"] < b),
        ))
    return out


def main():
    print("=" * 100)
    print("KC2-PM4 LAP R — LIMB A — referent contact/dry profile from FCT")
    print("=" * 100)
    print("\nPinned-input verification (GL-6, full 64-hex):")
    for ln in verify_pinned():
        print(ln)
    pre = pathlib.Path(OUT / "PREREGISTRATION.md")
    print(f"  EXACT  {sha256(pre)}  PREREGISTRATION.md")

    results, all_rows, all_wave = {}, [], []

    # ── PASS 1 ────────────────────────────────────────────────────────────────────────────────
    obs1, fr1, tm1, cad1 = load_pass1()
    rows1, res1, hits1, dry1, kt1 = analyse("P1_lapN_2.0s", obs1, fr1, tm1, cad1,
                                            FIGHT_T0, FIGHT_T1)
    results["pass1"] = res1
    all_rows += rows1
    w1 = per_wave("P1_lapN_2.0s", rows1, hits1, kt1, dry1, cad1)
    all_wave += w1

    # ── PASS 2 ────────────────────────────────────────────────────────────────────────────────
    obs2, fr2, tm2, cad2 = load_pass2()
    rows2, res2, hits2, dry2, kt2 = analyse("P2_dense_0.5s", obs2, fr2, tm2, cad2,
                                            FIGHT_T0, FIGHT_T1)
    results["pass2"] = res2
    all_rows += rows2
    w2 = per_wave("P2_dense_0.5s", rows2, hits2, kt2, dry2, cad2)
    all_wave += w2

    for k in ("pass1", "pass2"):
        r = results[k]
        print(f"\n--- {r['tag']}  ({r['n_samples']} samples, cadence {r['cadence_s']} s) ---")
        print(f"  P-OUT observations kept        : {r['n_pout_observations']}")
        print(f"  static positions excluded      : {r['n_static_positions_excluded']}  "
              f"{r['static_positions']}")
        print(f"  DRY samples                    : {r['n_dry_samples']}/{r['n_samples']}"
              f"  = {r['dry_sample_fraction']:.4f}")
        print(f"  gaps                           : {r['n_gaps']}   longest raw "
              f"{r['longest_gap_raw_s']} s  (L-corrected {r['longest_gap_corr_s']} s)")
        print(f"  total dry time (raw)           : {r['total_dry_time_raw_s']} s "
              f"of {r['total_span_s']} s")
        print(f"  PROVEN no-damage union         : {r['proven_no_damage_union_s']} s "
              f"= {r['proven_no_damage_union_frac']:.4f}  "
              f"({r['n_union_intervals']} merged intervals)")
        print("  SWEEP — fraction of fight time inside gaps longer than:")
        print(f"    {'rung':>7} | {'raw n':>6} {'raw frac':>10} | "
              f"{'corr n':>6} {'corr frac':>10}")
        for rung in SWEEP_RUNGS_S:
            a, b = r["sweep_raw"][rung], r["sweep_lifetime_corrected"][rung]
            resolvable = rung >= r["cadence_s"]
            mark = "" if resolvable else "   <- UNREACHED at this cadence"
            print(f"    {rung:>6.1f}s | {a['n_gaps']:>6} {a['frac_of_fight']:>10.4f} | "
                  f"{b['n_gaps']:>6} {b['frac_of_fight']:>10.4f}{mark}")

    print("\n--- per-wave (PASS 2, 0.5 s cadence) ---")
    print(f"  {'wave':>5} {'span_s':>8} {'n':>5} {'dry':>5} {'dry_frac':>9} "
          f"{'gaps':>5} {'longest_raw':>12} {'longest_corr':>13} {'events':>7}")
    for r in w2:
        print(f"  {r['wave']:>5} {r['span_s']:>8.1f} {r['n_samples']:>5} "
              f"{r['n_dry_samples']:>5} {r['dry_sample_fraction']:>9.4f} {r['n_gaps']:>5} "
              f"{r['longest_gap_raw_s']:>12.2f} {r['longest_gap_corr_s']:>13.2f} "
              f"{r['n_pout_events']:>7}")

    # ── w154 focus ────────────────────────────────────────────────────────────────────────────
    w = 154
    a, b = WAVE_START[w], WAVE_END[w]
    w154_gaps = sorted([r for r in rows2 if r["wave_at_start"] == w],
                       key=lambda z: -z["gap_raw_s"])
    results["w154"] = dict(
        wave=w, t_start=a, t_end=round(b, 3), span_s=round(b - a, 4),
        source_of_boundaries="Lap H-2 OBS-H2-6 wave-counter digit crop 52x26 @ (1582,138), +-0.25 s",
        gaps=w154_gaps,
        longest_gap_raw_s=w154_gaps[0]["gap_raw_s"] if w154_gaps else 0.0,
        longest_gap_corr_s=w154_gaps[0]["gap_lifetime_corrected_s"] if w154_gaps else 0.0,
        dry_sample_fraction=[r for r in w2 if r["wave"] == w][0]["dry_sample_fraction"],
        n_pout_events=[r for r in w2 if r["wave"] == w][0]["n_pout_events"],
    )
    print(f"\n--- WAVE 154 focus (span {a} -> {b:.1f} s = {b - a:.2f} s) ---")
    for g in w154_gaps:
        print(f"    gap {g['t_first_dry_sample']:.1f} .. {g['t_last_dry_sample']:.1f}  "
              f"raw {g['gap_raw_s']:.2f} s   L-corr {g['gap_lifetime_corrected_s']:.2f} s"
              f"{'  [straddles boundary]' if g['straddles_wave_boundary'] else ''}")
    if not w154_gaps:
        print("    (no dry gap begins inside wave 154)")

    # ── spawn-to-first-contact (FCT arm) ──────────────────────────────────────────────────────
    lat = []
    for wv in sorted(WAVE_START):
        t0 = WAVE_START[wv]
        nxt = [h["t_sec"] for h in hits2 if h["t_sec"] >= t0]
        first = min(nxt) if nxt else None
        lat.append(dict(
            wave=wv, t_wave_increment=t0,
            t_first_pout_sample=first,
            latency_fct_upper_s=(round(first - t0, 3) if first is not None else None),
            latency_fct_lower_s=(round(max(0.0, first - t0 - FCT_LIFETIME_S), 3)
                                 if first is not None else None),
        ))
    results["spawn_to_first_fct"] = lat
    print("\n--- spawn-to-first-player-damage latency (FCT arm, PASS 2) ---")
    print(f"  {'wave':>5} {'t_incr':>9} {'t_first':>9} {'upper_s':>9} {'lower_s':>9}")
    for r in lat:
        print(f"  {r['wave']:>5} {r['t_wave_increment']:>9.1f} "
              f"{(r['t_first_pout_sample'] or float('nan')):>9.1f} "
              f"{(r['latency_fct_upper_s'] or float('nan')):>9.2f} "
              f"{(r['latency_fct_lower_s'] or float('nan')):>9.2f}")

    # ── emit ──────────────────────────────────────────────────────────────────────────────────
    cols = ["pass_tag", "cadence_s", "t_first_dry_sample", "t_last_dry_sample", "n_dry_samples",
            "gap_raw_s", "gap_lifetime_corrected_s", "gap_corr_lo_s", "gap_corr_hi_s", "t_proven_start", "t_proven_end",
            "wave_at_start", "wave_at_end", "straddles_wave_boundary"]
    d, n = dump_csv(OUT / "pm4r_fct_gaps.csv", all_rows, cols)
    print(f"\npm4r_fct_gaps.csv  rows={n}  sha256={d}")
    results["emitted"] = {"pm4r_fct_gaps.csv": {"sha256": d, "rows": n}}
    results["per_wave"] = all_wave
    pathlib.Path("/tmp/pm4r/limb_a.json").write_text(json.dumps(results, indent=2, default=str))
    print("limb_a.json written")


if __name__ == "__main__":
    main()
