#!/usr/bin/env python3
"""KC2-PM4 Lap AC — FORK (a) leg A-2b: THE PERSISTENCE DISCRIMINATOR.

⚑ WHY THIS LEG EXISTS.  `D-AC-2`, my own defect, disclosed before any claim rested on it.
Leg A-2 graded `F-AC-3` DECISIVE-POSITIVE — 210 off-centre GREEN bar detections over 95 of
362 sampled frames.  Direct visual inspection of the two densest frames (evidence/) refuted
it: those detections are GREEN VFX PLUMES, and the white "(cur/max)" text that satisfied
`bars.find_bars`'s text gate belongs to nearby genuine RED nameplates.  `F-AC-3`'s functional
cannot separate a friendly nameplate from a green VFX run standing under a red plate's text.
The criterion is graded AS WRITTEN and then QUARANTINED; this leg is the discriminator that
the written one lacked.

THE DISCRIMINATOR.  A nameplate belongs to a body and therefore PERSISTS: it reappears one
frame later within the same association gate the pinned tracker uses.  A VFX plume that
happens to form a 3-row run of bar-like width does not.  Frame-to-frame persistence is
measured for THREE populations in THE SAME FRAMES:

    RED plates              -- the counted population; the REFERENCE
    PLAYER-gated GREEN      -- a known-real nameplate; the POSITIVE CONTROL
    off-centre GREEN        -- the population under test

  MEASURED QUANTITY : fraction of detections at frame i that have a detection of the same
                      class within `gate = 30.0` ground px at frame i+1 (60 fps).
  GATE PROVENANCE   : `d1b.track`'s own default `gate=30.0`, imported by identity — not a
                      threshold invented for this leg.
  BOUND DIRECTION   : persistence is a LOWER bound on reality (a real plate can drop out);
                      high persistence cannot be manufactured by frame-local noise.

READ-ONLY on the MP4.  OUTCOME-FIREWALLED.  NO SIM ARTIFACT IS OPENED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import numpy as np

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4ac_lib_2026_08_16 import (                                           # noqa: E402
    OUT, VIDEO, FIGHT_T0, K_GROUND, PLAYER_XLEFT_LO, PLAYER_XLEFT_HI,
    PREREG_SHA, verify_pinned, verify_prereg, sha256, dump_csv, import_h2_bars, wave_of,
)
from pm4ac_green_census_2026_08_16 import HUD, in_hud, W_PX, H_PX                # noqa: E402

# ── DECLARED BEFORE THIS LEG RAN (post-hoc to F-AC-3, and labelled so everywhere) ───────────
N_BURSTS = 20
BURST_STRIDE_S = 9.0                 # 683.0 + k*9.0, k = 0..19  -> last burst at 854.0 s
BURST_FRAMES = 15                    # 0.25 s of consecutive 60 fps frames
GATE_GPX = 30.0                      # d1b.track's own default, imported by identity
#: the leg's criterion, fixed before the numbers.
PERSIST_RATIO_REAL = 0.50            # off-centre green >= 0.50 x red  => REAL entity population
MIN_TEST_DETECTIONS = 30
MIN_REF_DETECTIONS = 300


def burst_frames(t0: float, n: int):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", str(VIDEO),
           "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W_PX * H_PX * 3)
    nb = W_PX * H_PX * 3
    i = 0
    while i < n:
        raw = p.stdout.read(nb)
        if len(raw) < nb:
            break
        yield t0 + i / 60.0, np.frombuffer(raw, dtype=np.uint8).reshape(H_PX, W_PX, 3)
        i += 1
    p.stdout.close()
    p.wait()


def detect(bars, a):
    out = {"red": [], "green_player": [], "green_off": []}
    for b in bars.find_bars(a, mask_fn=bars.red_mask, y0=60, y1=975, minw=14, maxw=90):
        if in_hud(b["x_c"], b["y"]):
            continue
        out["red"].append((b["x_left"] + 36.0, b["y"]))
    for b in bars.find_bars(a, mask_fn=bars.green_mask2, y0=60, y1=975, minw=14, maxw=90):
        if in_hud(b["x_c"], b["y"]):
            continue
        key = ("green_player" if PLAYER_XLEFT_LO <= b["x_left"] <= PLAYER_XLEFT_HI
               else "green_off")
        out[key].append((b["x_left"] + 36.0, b["y"]))
    return out


def persistence(A, B):
    """(n_tested, n_with_successor) between two consecutive frames' detections of one class."""
    if not A or not B:
        return len(A), 0
    a = np.array(A, dtype=float)
    b = np.array(B, dtype=float)
    d = np.hypot(a[:, None, 0] - b[None, :, 0], (a[:, None, 1] - b[None, :, 1]) / K_GROUND)
    return len(A), int((d.min(axis=1) <= GATE_GPX).sum())


def main():
    print("=" * 100)
    print("KC2-PM4 LAP AC — FORK (a) leg A-2b — THE PERSISTENCE DISCRIMINATOR (D-AC-2 repair)")
    print("=" * 100)
    print(f"  EXACT  {verify_prereg(PREREG_SHA)}  prereg.md")
    for ln in verify_pinned():
        print(ln)
    print(f"\n  {N_BURSTS} bursts x {BURST_FRAMES} frames at 60 fps, starts "
          f"{FIGHT_T0} + k*{BURST_STRIDE_S} s   gate {GATE_GPX} gpx (d1b.track default)")

    bars = import_h2_bars()
    tot = {k: [0, 0] for k in ("red", "green_player", "green_off")}
    rows = []
    for k in range(N_BURSTS):
        t0 = FIGHT_T0 + k * BURST_STRIDE_S
        seq = list(burst_frames(t0, BURST_FRAMES))
        dets = [(t, detect(bars, a)) for t, a in seq]
        per = {c: [0, 0] for c in tot}
        for i in range(len(dets) - 1):
            for c in tot:
                n, h = persistence(dets[i][1][c], dets[i + 1][1][c])
                per[c][0] += n
                per[c][1] += h
        for c in tot:
            tot[c][0] += per[c][0]
            tot[c][1] += per[c][1]
        rows.append(dict(burst=k, t_start=round(t0, 4), wave=wave_of(t0),
                         n_frames=len(dets),
                         red_tested=per["red"][0], red_persist=per["red"][1],
                         green_player_tested=per["green_player"][0],
                         green_player_persist=per["green_player"][1],
                         green_off_tested=per["green_off"][0],
                         green_off_persist=per["green_off"][1]))
        print(f"  burst {k:2d} t={t0:7.1f} (w{wave_of(t0)})  red {per['red'][1]}/{per['red'][0]}"
              f"   player-green {per['green_player'][1]}/{per['green_player'][0]}"
              f"   off-green {per['green_off'][1]}/{per['green_off'][0]}")

    def frac(c):
        return round(tot[c][1] / tot[c][0], 6) if tot[c][0] else None

    p_red, p_pl, p_off = frac("red"), frac("green_player"), frac("green_off")
    print(f"\n  RED (reference)          : {tot['red'][1]}/{tot['red'][0]} = {p_red}")
    print(f"  PLAYER GREEN (pos.ctrl)  : {tot['green_player'][1]}/{tot['green_player'][0]} = {p_pl}")
    print(f"  OFF-CENTRE GREEN (test)  : {tot['green_off'][1]}/{tot['green_off'][0]} = {p_off}")

    evaluable = (tot["green_off"][0] >= MIN_TEST_DETECTIONS
                 and tot["red"][0] >= MIN_REF_DETECTIONS)
    ctrl_ok = (p_pl is not None and p_red is not None
               and p_pl >= PERSIST_RATIO_REAL * p_red)
    if not evaluable:
        verdict = "UNREACHED (population non-emptiness clause)"
    elif not ctrl_ok:
        verdict = "INCONCLUSIVE (positive control failed — the instrument is suspect)"
    elif p_off >= PERSIST_RATIO_REAL * p_red:
        verdict = "REAL-ENTITY-POPULATION"
    else:
        verdict = "VFX-ARTEFACT"
    print(f"\n  ratio off-green/red = "
          f"{round(p_off / p_red, 6) if p_red else None}   "
          f"positive-control ratio = {round(p_pl / p_red, 6) if p_red else None}")
    print(f"  LEG A-2b VERDICT: {verdict}")

    res = dict(
        lap="AC", fork="a", leg="A-2b",
        why="D-AC-2 repair: F-AC-3's functional cannot separate a friendly nameplate from a "
            "green VFX run standing under a red plate's white text (refuted by direct visual "
            "inspection, evidence/crop-702-cluster.png and evidence/crop-700-cluster.png)",
        declared_post_hoc=True,
        prereg_sha256=PREREG_SHA,
        design=dict(n_bursts=N_BURSTS, burst_stride_s=BURST_STRIDE_S,
                    burst_frames=BURST_FRAMES, fps=60.0, gate_gpx=GATE_GPX,
                    gate_provenance="d1b.track default `gate=30.0`, imported by identity"),
        populations=dict(
            red=dict(tested=tot["red"][0], persisted=tot["red"][1], persistence=p_red,
                     role="REFERENCE — the population the occupancy bracket counts"),
            green_player=dict(tested=tot["green_player"][0], persisted=tot["green_player"][1],
                              persistence=p_pl, role="POSITIVE CONTROL — a known-real plate"),
            green_offcentre=dict(tested=tot["green_off"][0], persisted=tot["green_off"][1],
                                 persistence=p_off, role="UNDER TEST"),
        ),
        criterion=f"REAL-ENTITY-POPULATION iff persistence(off-green) >= "
                  f"{PERSIST_RATIO_REAL} x persistence(red)",
        population_non_emptiness=dict(require_test_ge=MIN_TEST_DETECTIONS,
                                      test=tot["green_off"][0],
                                      require_ref_ge=MIN_REF_DETECTIONS, ref=tot["red"][0],
                                      evaluable=bool(evaluable)),
        positive_control_passed=bool(ctrl_ok),
        ratio_offgreen_over_red=round(p_off / p_red, 6) if p_red else None,
        ratio_playergreen_over_red=round(p_pl / p_red, 6) if p_red else None,
        verdict=verdict,
        bound_direction="persistence is a LOWER bound on reality; frame-local noise cannot "
                        "manufacture it",
        firewall="no simulation artifact opened; no sim grade computed",
    )
    d, n = dump_csv(OUT / "pm4ac_green_persistence.csv", rows,
                    ["burst", "t_start", "wave", "n_frames", "red_tested", "red_persist",
                     "green_player_tested", "green_player_persist", "green_off_tested",
                     "green_off_persist"])
    res["emitted"] = {"pm4ac_green_persistence.csv": dict(sha256=d, rows=n)}
    print(f"\n  pm4ac_green_persistence.csv  rows={n}  sha256={d}")
    q = OUT / "pm4ac_green_persistence.json"
    q.write_text(json.dumps(res, indent=2, sort_keys=True, default=str))
    print(f"  pm4ac_green_persistence.json sha256={sha256(q)}")


if __name__ == "__main__":
    main()
