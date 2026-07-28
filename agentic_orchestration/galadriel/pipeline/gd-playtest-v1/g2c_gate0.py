#!/usr/bin/env python3
"""G-2c GATE 0 -- two reproductions, asserted before any measurement fires.

GATE 0a -- the 106-window derivation, re-run from the T-A ledger through the
committed `tb_windows.py` logic (harness-v1: encounter = maximal run of kill
events with internal gaps <= 5.0 s, pad 3.0 s), compared field-by-field
against the committed T-B artifact. Same gate G-2b asserted; re-asserted here
because G-2c reads the same windows.

GATE 0b -- the DROP EVENTS, re-derived WITH TIMESTAMPS from the committed
per-frame series (`tb-intake-frames.jsonl.gz`). The committed
`tb-intake-windows.json` carries `drops` as bare magnitudes with no time
attached; question 2 of this pass needs each drop's time and its EHP
denominator, so the delta loop of `tb_intake.py` is replayed verbatim
(ADJ_TOL 0.2001 s, loading-break splitting via `stretches`, adjacency-only
pairs). The replay is only admissible if it reproduces every committed
per-window quantity it touches: n_pairs, n_bridged_pairs, delta_covered_s,
intake_hp, healed_hp, n_drops, n_heals, drop_max, drop_p50, and the drops
multiset IN ORDER. Any mismatch aborts.

Nothing is interpolated. The frames file already carries the post-demotion
series (TRUNC / OCRSPIKE frames have hp=None and their refusal code), so the
replay inherits the committed refusals rather than re-deriving them.
"""
import gzip
import json
import os
import statistics as st
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tb_windows as TW  # noqa: E402
from tb_intake import ADJ_TOL, FPS, stretches  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TA = os.path.join(ROOT, "captures", "2026-07-26-gd-playtest-v1",
                  "ta-full-2fps-gated.csv")
TB = os.path.join(ROOT, "captures", "2026-07-26-gd-playtest-v1-tb")
OUT = os.path.join(ROOT, "captures", "2026-07-28-gd-playtest-v1-g2c")


def gate0a():
    rows = TW.load(TA)
    ev = TW.kill_events(rows)
    groups = TW.segment(ev)
    pts = TW.interp_play_time(rows)
    wins = []
    for i, g in enumerate(groups):
        a, b = g[0]["pts_s"], g[-1]["pts_s"]
        pt0, d0 = TW.nearest_pt(pts, a)
        pt1, d1 = TW.nearest_pt(pts, b)
        wins.append(dict(
            eng_id=i, pts_start=a, pts_end=b, dur_s=round(b - a, 3),
            n_events=len(g), kills=sum(x["delta"] for x in g),
            play_time_start=pt0, play_time_end=pt1,
            pt_carrier_dist_s=round(max(d0, d1), 2),
            regime=TW.regime_of(pt0),
            cap_start=round(max(0.0, a - TW.PAD), 3), cap_end=round(b + TW.PAD, 3),
            cap_dur=round((b + TW.PAD) - max(0.0, a - TW.PAD), 3)))
    ref = json.load(open(os.path.join(TB, "tb-engagement-windows.json")))
    rw = ref["windows"]
    assert len(wins) == len(rw) == 106, (len(wins), len(rw))
    diffs = []
    for a, b in zip(wins, rw):
        for k in a:
            if a[k] != b[k]:
                diffs.append((a["eng_id"], k, a[k], b[k]))
    durs = [w["dur_s"] for w in wins]
    rep = dict(
        n_engagements=len(wins),
        n_kill_event_samples=len(ev),
        n_multi_kill_samples=sum(1 for e in ev if e["delta"] > 1),
        total_kills=sum(e["delta"] for e in ev),
        dur_median=st.median(durs), dur_mean=round(st.mean(durs), 3),
        dur_max=max(durs),
        by_regime={r: dict(n=sum(1 for w in wins if w["regime"] == r),
                           kills=sum(w["kills"] for w in wins
                                     if w["regime"] == r))
                   for r in ("R1", "R2", "R3")},
        field_diffs_vs_committed=diffs)
    ok = (not diffs and len(wins) == 106 and rep["dur_median"] == 4.5
          and rep["dur_max"] == 37.5 and rep["total_kills"] == 880)
    rep["PASS"] = ok
    return rep


def replay_drops(series):
    """Verbatim replay of tb_intake.py's delta loop, retaining timestamps."""
    brks = stretches(series)
    ok = [s for s in series if s["st"] == "OK"]

    def in_break(t0, t1):
        return any(not (t1 <= b[0] or t0 >= b[1]) for b in brks)

    intake = healed = 0
    drops, heals = [], []
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
            drops.append(dict(t=b["t"], mag=-d, hp_before=a["hp"],
                              hp_after=b["hp"], dt=round(dt, 4)))
        elif d > 0:
            healed += d
            heals.append(dict(t=b["t"], mag=d))
    return dict(intake_hp=intake, healed_hp=healed, drops=drops, heals=heals,
                delta_covered_s=round(covered_s, 3), n_pairs=pairs,
                n_bridged_pairs=bridged,
                unreadable_break_s=round(sum(b[1] - b[0] for b in brks), 2))


def gate0b():
    frames = {}
    with gzip.open(os.path.join(TB, "tb-intake-frames.jsonl.gz"), "rt") as fh:
        for line in fh:
            s = json.loads(line)
            frames.setdefault(s["eng"], []).append(s)
    for e in frames:
        frames[e].sort(key=lambda s: s["t"])
    W = json.load(open(os.path.join(TB, "tb-intake-windows.json")))["windows"]
    mism, out = [], {}
    for w in W:
        e = w["eng_id"]
        ser = frames.get(e, [])
        r = replay_drops(ser)
        mags = [d["mag"] for d in r["drops"]]
        checks = dict(
            n_frames=(len(ser), w["n_frames_decoded"]),
            intake_hp=(r["intake_hp"], w["intake_hp"]),
            healed_hp=(r["healed_hp"], w["healed_hp"]),
            n_drops=(len(mags), w["n_drops"]),
            n_heals=(len(r["heals"]), w["n_heals"]),
            drops=(mags, w["drops"]),
            drop_max=(max(mags) if mags else 0, w["drop_max"]),
            drop_p50=(int(np.median(mags)) if mags else 0, w["drop_p50"]),
            delta_covered_s=(r["delta_covered_s"], w["delta_covered_s"]),
            n_pairs=(r["n_pairs"], w["n_pairs"]),
            n_bridged_pairs=(r["n_bridged_pairs"], w["n_bridged_pairs"]),
            unreadable_break_s=(r["unreadable_break_s"],
                                w["unreadable_break_s"]))
        for k, (a, b) in checks.items():
            if a != b:
                mism.append(dict(eng_id=e, field=k, replay=a, committed=b))
        out[e] = r
    return dict(n_windows=len(W), n_mismatches=len(mism),
                mismatches=mism[:40], PASS=(len(mism) == 0)), out


def main():
    a = gate0a()
    b, drops = gate0b()
    rep = dict(gate0a_window_derivation=a, gate0b_drop_replay=b,
               PASS=bool(a["PASS"] and b["PASS"]))
    os.makedirs(OUT, exist_ok=True)
    json.dump(rep, open(os.path.join(OUT, "g2c-gate0.json"), "w"), indent=1)
    if not rep["PASS"]:
        print("GATE 0 FAILED", json.dumps(rep, indent=1)[:4000])
        sys.exit(2)
    # timestamped drop ledger, one row per admissible negative delta
    with open(os.path.join(OUT, "g2c-drops.jsonl"), "w") as fh:
        for e in sorted(drops):
            for d in drops[e]["drops"]:
                fh.write(json.dumps(dict(eng_id=e, **d)) + "\n")
    print("GATE 0 PASS")
    print(json.dumps({k: v for k, v in a.items()
                      if k != "field_diffs_vs_committed"}, indent=1))
    print("gate0b: %d windows, %d mismatches" % (b["n_windows"],
                                                 b["n_mismatches"]))
    print("drops written: %d" % sum(len(drops[e]["drops"]) for e in drops))


if __name__ == "__main__":
    main()
