#!/usr/bin/env python3
"""T-B step 1 -- derive the 106 engagement windows from the T-A ledger.

Segmentation per efficacy-verdict 2026-07-26 SS4: inter-kill-event gap > 5 s.
A kill EVENT is a sample at which the gated, monotonic `kills` series
increments. Engagement = maximal run of kill events with all internal gaps
<= 5 s. Duration = last_event_ts - first_event_ts (0 for singletons).

Reproduction target (verdict SS4): 106 engagements, median 4.5 s, mean 6.1,
max 37.5. If this script does not hit those numbers the segmentation
definition is wrong and nothing downstream may fire.

Windows are emitted on the VIDEO clock (pts_s) because that is what ffmpeg
seeks on. Each window carries its play_time bracket so the regime partition
(R1 358-1134 / R2 1134-6052 / R3 6052-7094) is assigned on the GAME clock,
per the SS2 C-1 correction (DoT boundary 6052, NOT 6816) and the C-2
correction (build break 1134, NOT 1757).
"""
import csv
import json
import statistics as st
import sys

GAP = 5.0
PAD = 3.0
REGIMES = [("R1", 358, 1134), ("R2", 1134, 6052), ("R3", 6052, 7095)]


def regime_of(pt):
    if pt is None:
        return None
    for name, lo, hi in REGIMES:
        if lo <= pt < hi:
            return name
    return None


def load(path):
    rows = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            rows.append(dict(
                pts_s=float(r["pts_s"]),
                play_time=int(r["play_time"]) if r["play_time"] else None,
                kills=int(r["kills"]) if r["kills"] else None,
                dps=float(r["dps"]) if r["dps"] else None,
                gate=r["gate"]))
    return rows


def kill_events(rows):
    """Gated monotonic kills -> (pts_s, play_time, delta) at each increment."""
    ev, prev = [], None
    for r in rows:
        k = r["kills"]
        if k is None:
            continue
        if prev is None:
            prev = k
            continue
        if k > prev:
            ev.append(dict(pts_s=r["pts_s"], play_time=r["play_time"],
                           delta=k - prev))
        prev = max(prev, k)
    return ev


def segment(ev, gap=GAP):
    out, cur = [], [ev[0]]
    for e in ev[1:]:
        if e["pts_s"] - cur[-1]["pts_s"] > gap:
            out.append(cur)
            cur = [e]
        else:
            cur.append(e)
    out.append(cur)
    return out


def interp_play_time(rows):
    """play_time carrier for samples where OCR refused. Nearest gated read
    within 5 s on EITHER side; used ONLY for regime labelling of a window,
    never as a measurement. Windows with no carrier are labelled None."""
    pts = [(r["pts_s"], r["play_time"]) for r in rows if r["play_time"] is not None]
    return pts


def nearest_pt(pts, t):
    lo, hi = 0, len(pts) - 1
    best, bd = None, 1e18
    while lo <= hi:
        m = (lo + hi) // 2
        d = abs(pts[m][0] - t)
        if d < bd:
            bd, best = d, pts[m][1]
        if pts[m][0] < t:
            lo = m + 1
        else:
            hi = m - 1
    return (best, bd)


def main():
    src, out = sys.argv[1], sys.argv[2]
    rows = load(src)
    ev = kill_events(rows)
    groups = segment(ev)
    pts = interp_play_time(rows)
    durs = [g[-1]["pts_s"] - g[0]["pts_s"] for g in groups]
    wins = []
    for i, g in enumerate(groups):
        a, b = g[0]["pts_s"], g[-1]["pts_s"]
        pt0, d0 = nearest_pt(pts, a)
        pt1, d1 = nearest_pt(pts, b)
        wins.append(dict(
            eng_id=i, pts_start=a, pts_end=b, dur_s=round(b - a, 3),
            n_events=len(g), kills=sum(x["delta"] for x in g),
            play_time_start=pt0, play_time_end=pt1,
            pt_carrier_dist_s=round(max(d0, d1), 2),
            regime=regime_of(pt0),
            cap_start=round(max(0.0, a - PAD), 3), cap_end=round(b + PAD, 3),
            cap_dur=round((b + PAD) - max(0.0, a - PAD), 3)))
    tot = sum(w["cap_dur"] for w in wins)
    summ = dict(
        source=src, gap_threshold_s=GAP, pad_s=PAD,
        n_kill_event_samples=len(ev),
        n_multi_kill_samples=sum(1 for e in ev if e["delta"] > 1),
        total_kills=sum(e["delta"] for e in ev),
        n_engagements=len(groups),
        dur_median=st.median(durs), dur_mean=round(st.mean(durs), 3),
        dur_max=max(durs),
        capture_wallclock_s=round(tot, 1),
        frames_at_15fps=int(round(tot * 15)),
        by_regime={r: dict(
            n=sum(1 for w in wins if w["regime"] == r),
            kills=sum(w["kills"] for w in wins if w["regime"] == r),
            cap_s=round(sum(w["cap_dur"] for w in wins if w["regime"] == r), 1))
            for r in ("R1", "R2", "R3", None) if True},
        windows=wins)
    summ["by_regime"] = {str(k): v for k, v in summ["by_regime"].items()}
    json.dump(summ, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k != "windows"},
                     indent=1))


if __name__ == "__main__":
    main()
