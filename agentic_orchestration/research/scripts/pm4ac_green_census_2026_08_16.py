#!/usr/bin/env python3
"""KC2-PM4 Lap AC — FORK (a) leg A-2: THE GREEN-PLATE CENSUS.

THE QUESTION.  The Lap R contact-occupancy bracket counts `kind == 0` rows of the pinned
Lap H-2 nameplate census.  `extract.py:48` produces those rows from `bars.find_bars(...)`
with the DEFAULT `mask_fn = bars.red_mask`; `kind == 1` (the player) comes from
`extract.py:pbar`, which uses `bars.green_mask2` AND restricts `x_left` to [890, 960].
Colour is therefore the SOLE hostile/friendly discriminator in the whole chain — and the
player's own x-gate is precisely what would hide a friendly plate belonging to something
that is not the player.

So: does this footage draw ANY non-player nameplate in green?  The referent purchased four
Crucible defence emplacements (Lap AB § 3.4).  If friendly plates are green they were never
in the bracket; if there is no green but the player's, the bracket's summon term is not
settled by this leg and fork (a) must fall to another verdict.

  MEASURED QUANTITY : per sampled frame, the number of green-mask nameplate bars passing the
                      FULL `bars.find_bars` pipeline (3-6 row persistence, >= 70 white text
                      pixels in the measured band above the bar, dedupe), outside the four
                      `extract.py:HUD` rectangles, whose `x_left` is OUTSIDE [890, 960].
  BOUND DIRECTION   : plate presence proves a drawn plate; absence does not prove absence.
                      A zero is only a measurement if the detector demonstrably fires on this
                      footage -- hence F-AC-3's population non-emptiness clause.

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
    OUT, VIDEO, FIGHT_T0, FIGHT_T1, GREEN_SAMPLE_FPS, PLAYER_XLEFT_LO, PLAYER_XLEFT_HI,
    GREEN_MIN_PLAYER_DETECT_FRAC, PREREG_SHA, verify_pinned, verify_prereg, sha256,
    dump_csv, import_h2_bars, wave_of,
)

#: extract.py:14 — the four HUD rectangles, imported by identity (value-for-value).
HUD = [(1330, 0, 1920, 262), (0, 0, 1920, 58), (0, 980, 1920, 1080), (0, 0, 300, 120)]
W_PX, H_PX = 1920, 1080


def in_hud(x, y):
    """extract.py:15, verbatim in form."""
    return any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, y0, x1, y1) in HUD)


def frames(t0: float, dur: float, fps: float):
    """Stream raw RGB frames from the referent MP4.  READ-ONLY; nothing is written to it."""
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", str(VIDEO),
           "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W_PX * H_PX * 3)
    n = W_PX * H_PX * 3
    i = 0
    while True:
        raw = p.stdout.read(n)
        if len(raw) < n:
            break
        yield t0 + i / fps, np.frombuffer(raw, dtype=np.uint8).reshape(H_PX, W_PX, 3)
        i += 1
    p.stdout.close()
    p.wait()


def main():
    print("=" * 100)
    print("KC2-PM4 LAP AC — FORK (a) leg A-2 — THE GREEN-PLATE CENSUS")
    print("=" * 100)
    print(f"  EXACT  {verify_prereg(PREREG_SHA)}  prereg.md")
    for ln in verify_pinned():
        print(ln)

    bars = import_h2_bars()
    dur = FIGHT_T1 - FIGHT_T0
    n_expect = int(dur * GREEN_SAMPLE_FPS) + 1
    print(f"\n  window  [{FIGHT_T0}, {FIGHT_T1}] s   sample {GREEN_SAMPLE_FPS} fps   "
          f"expected frames {n_expect}")
    print(f"  detector: bars.find_bars(mask_fn=<green>, minw=14, y0=60, y1=975) — the SAME "
          f"pipeline extract.py:48 runs for the counted RED population, with the player's "
          f"x-gate REMOVED")

    rows = []
    det_rows = []
    for masks_name, mask_fn in (("green_mask2", bars.green_mask2), ("green_mask", bars.green_mask)):
        print(f"\n--- pass: {masks_name} ---")
        n_frames = 0
        n_player = 0
        n_off = 0
        n_frames_with_off = 0
        for t, a in frames(FIGHT_T0, dur, GREEN_SAMPLE_FPS):
            n_frames += 1
            got = bars.find_bars(a, mask_fn=mask_fn, y0=60, y1=975, minw=14, maxw=90)
            got = [b for b in got if not in_hud(b["x_c"], b["y"])]
            pl = [b for b in got if PLAYER_XLEFT_LO <= b["x_left"] <= PLAYER_XLEFT_HI]
            off = [b for b in got if not (PLAYER_XLEFT_LO <= b["x_left"] <= PLAYER_XLEFT_HI)]
            n_player += 1 if pl else 0
            n_off += len(off)
            n_frames_with_off += 1 if off else 0
            rows.append(dict(mask=masks_name, t_sec=round(t, 4), wave=wave_of(t),
                             n_green_total=len(got), n_green_player_gated=len(pl),
                             n_green_offcentre=len(off)))
            for b in off:
                det_rows.append(dict(mask=masks_name, t_sec=round(t, 4), wave=wave_of(t),
                                     x_left=int(b["x_left"]), x_right=int(b["x_right"]),
                                     x_c=round(float(b["x_c"]), 1), y=round(float(b["y"]), 1),
                                     w=int(b["w"]), rows=int(b["rows"]), txt=int(b["txt"])))
            if n_frames % 60 == 0:
                print(f"    t={t:7.1f}  frames={n_frames:4d}  player-plate frames={n_player:4d}  "
                      f"off-centre green detections={n_off}")
        frac = n_player / max(n_frames, 1)
        print(f"  frames sampled              : {n_frames}")
        print(f"  frames with the PLAYER plate: {n_player}  ({frac:.4f})")
        print(f"  off-centre GREEN detections : {n_off} over {n_frames_with_off} frames")
        if masks_name == "green_mask2":
            primary = dict(mask=masks_name, n_frames=n_frames, n_player_frames=n_player,
                           player_detect_frac=round(frac, 6),
                           n_offcentre_detections=n_off,
                           n_frames_with_offcentre=n_frames_with_off)

    res = dict(
        lap="AC", fork="a", leg="A-2",
        prereg_sha256=PREREG_SHA,
        window=dict(t0=FIGHT_T0, t1=FIGHT_T1, sample_fps=GREEN_SAMPLE_FPS,
                    n_frames_expected=n_expect),
        detector="bars.find_bars imported BY IDENTITY from the pinned Lap H-2 detector; the "
                 "ONLY change is the mask function and the removal of extract.py:pbar's "
                 "x_left in [890,960] player gate",
        hud_rects=HUD,
        primary=primary,
        by_mask={},
        bound_direction="plate presence proves a drawn plate; absence does not prove absence. "
                        "A zero is a measurement ONLY under the non-emptiness clause below.",
        firewall="no simulation artifact opened; no sim grade computed",
    )
    for m in ("green_mask2", "green_mask"):
        rr = [r for r in rows if r["mask"] == m]
        res["by_mask"][m] = dict(
            n_frames=len(rr),
            n_player_frames=sum(1 for r in rr if r["n_green_player_gated"] >= 1),
            n_offcentre_detections=sum(r["n_green_offcentre"] for r in rr),
            n_frames_with_offcentre=sum(1 for r in rr if r["n_green_offcentre"] >= 1),
            max_offcentre_in_one_frame=max((r["n_green_offcentre"] for r in rr), default=0),
        )

    # ── F-AC-3 ───────────────────────────────────────────────────────────────────────────────
    p = res["by_mask"]["green_mask2"]
    need = int(np.ceil(GREEN_MIN_PLAYER_DETECT_FRAC * p["n_frames"]))
    evaluable = p["n_player_frames"] >= need
    fac3 = dict(
        window=f"the {p['n_frames']} frames of [{FIGHT_T0}, {FIGHT_T1}] at "
               f"{GREEN_SAMPLE_FPS} fps",
        functional="n_frames_with_offcentre_green (green_mask2 pass)",
        population_non_emptiness=dict(
            require_player_frames_ge=need, player_frames=p["n_player_frames"],
            player_detect_frac=round(p["n_player_frames"] / max(p["n_frames"], 1), 6),
            evaluable=bool(evaluable)),
        n_frames_with_offcentre_green=p["n_frames_with_offcentre"],
        criterion=">= 1 frame with an off-centre green plate ⇒ the census is DECISIVE for "
                  "PET-EXCLUSIVE; == 0 over a detector-live population ⇒ the green channel "
                  "carries nothing but the player and fork (a) must be decided elsewhere",
    )
    fac3["verdict"] = ("INCONCLUSIVE (population non-emptiness clause)" if not evaluable
                       else ("DECISIVE-POSITIVE" if p["n_frames_with_offcentre"] >= 1
                             else "DECISIVE-NEGATIVE"))
    res["F_AC_3"] = fac3
    print(f"\n  F-AC-3: player-plate frames {p['n_player_frames']}/{p['n_frames']} "
          f"(need >= {need})  ->  {fac3['verdict']}")

    # ── EMIT ─────────────────────────────────────────────────────────────────────────────────
    d1, n1 = dump_csv(OUT / "pm4ac_green_census.csv", rows,
                      ["mask", "t_sec", "wave", "n_green_total", "n_green_player_gated",
                       "n_green_offcentre"])
    d2, n2 = dump_csv(OUT / "pm4ac_green_detections.csv", det_rows,
                      ["mask", "t_sec", "wave", "x_left", "x_right", "x_c", "y", "w", "rows",
                       "txt"])
    res["emitted"] = {"pm4ac_green_census.csv": dict(sha256=d1, rows=n1),
                      "pm4ac_green_detections.csv": dict(sha256=d2, rows=n2)}
    print(f"\n  pm4ac_green_census.csv      rows={n1}  sha256={d1}")
    print(f"  pm4ac_green_detections.csv  rows={n2}  sha256={d2}")
    q = OUT / "pm4ac_green_census.json"
    q.write_text(json.dumps(res, indent=2, sort_keys=True, default=str))
    print(f"  pm4ac_green_census.json     sha256={sha256(q)}")


if __name__ == "__main__":
    main()
