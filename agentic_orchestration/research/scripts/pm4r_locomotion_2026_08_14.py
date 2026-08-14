#!/usr/bin/env python3
"""KC2-PM4 Lap R — LIMB B: video locomotion sampling.

  B.1  player MOVEMENT EPISODES from the Lap H-2 camera-translation trace (camera is
       measured rigidly player-locked, so camera translation IS player world displacement)
  B.2  DETECTOR VALIDATION against an independent second instrument (raw-luminance NCC
       template match vs the trace's FFT phase correlation on gradient magnitude)
  B.3  MOVEMENT-WHILE-CHANNELING, decoded from the referent's own frames (two observables:
       player-outgoing FCT persistence + player-centred channel-VFX ring persistence)
  B.4  wave-spawn-to-first-CONTACT latency from the Lap H-2 nameplate census

Every threshold pre-registered: PREREGISTRATION.md sha256 dc49d0ba...cec10.
READ-ONLY.  OUTCOME-FIREWALLED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4r_lib_2026_08_14 import (                                             # noqa: E402
    LAPH2, OUT, VIDEO, K_GROUND, PLAYER_SCREEN, FIGHT_T0, FIGHT_T1,
    WAVE_START, WAVE_END, V_ON_PRIMARY, V_ON_SENSITIVITY, V_OFF_RATIO,
    SMOOTH_FRAMES, MIN_EPISODE_S, VALIDATION_SEED, VALIDATION_N_PER_CLASS,
    VALIDATION_DT_S, VALIDATION_CLASS_CUT_GPX, VALIDATION_PASS_AGREE,
    VALIDATION_PASS_MEDIAN_RELERR, CHANNEL_N_EPISODES, CHANNEL_SAMPLE_FPS,
    RING_ANNULUS_PX, RING_CONTROL_ANNULUS_PX, CHANNEL_CONTINUES_FRAC,
    CHANNEL_INTERRUPTED_RATIO, R_CONTACT_GPX, R_CONTACT_SENSITIVITY,
    ground_speed, rolling_median, episodes, wave_of, verify_pinned, sha256, dump_csv,
    classify, colour_class, parse_damage, p_out,
)

WORK = pathlib.Path("/tmp/pm4r")
PLATES = OUT / "method" / "plates60_lapH2.npy"
PLATES_SHA = "28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df"

#: NCC validation terrain patches — fixed screen positions, all >= 400 px from the player's
#: pinned ground point (958,544) and inside the Lap H-2 terrain band y in [100,860].
PATCHES = [(180, 180, 200, 150), (1520, 180, 200, 150),
           (180, 640, 200, 150), (1520, 640, 200, 150)]


# ══════════════════════════════════════════════════════════════════════════════════════════════
def gray(t: float) -> np.ndarray:
    """One frame at time t as a greyscale array.  Read-only on the MP4."""
    p = WORK / "val" / f"g_{t:.4f}.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", str(VIDEO),
                        "-frames:v", "1", "-vf", "format=gray", "-y", str(p)], check=True)
    return np.asarray(Image.open(p).convert("L"))


def ncc_best(a: np.ndarray, b: np.ndarray, patch, coarse=6, span=252):
    """Independent instrument: normalised cross-correlation template match, raw luminance.
    Coarse-to-fine.  Returns (dx, dy, peak)."""
    x, y, w, h = patch
    tpl = a[y:y + h, x:x + w].astype(np.float64)
    tpl -= tpl.mean()
    tn = np.sqrt((tpl ** 2).sum())
    if tn < 1e-9:
        return 0.0, 0.0, 0.0
    H, W = b.shape

    def score(dx, dy):
        xx, yy = x + dx, y + dy
        if xx < 0 or yy < 0 or xx + w > W or yy + h > H:
            return -2.0
        win = b[yy:yy + h, xx:xx + w].astype(np.float64)
        win -= win.mean()
        wn = np.sqrt((win ** 2).sum())
        return -2.0 if wn < 1e-9 else float((tpl * win).sum() / (tn * wn))

    best = (0, 0, -2.0)
    for dy in range(-span, span + 1, coarse):
        for dx in range(-span, span + 1, coarse):
            c = score(dx, dy)
            if c > best[2]:
                best = (dx, dy, c)
    bx, by, bc = best
    for dy in range(by - coarse, by + coarse + 1):
        for dx in range(bx - coarse, bx + coarse + 1):
            c = score(dx, dy)
            if c > bc:
                bx, by, bc = dx, dy, c
    return float(bx), float(by), bc


def ring_ratio(t: float):
    """Player-centred channel-VFX probe.  Mean luminance in the ground-plane elliptical annulus
    RING_ANNULUS_PX about the player's pinned ground point, over the same in a far control
    annulus.  NOTE-9: pixels cannot name WHICH skill draws a ring."""
    g = gray(t).astype(np.float64)
    H, W = g.shape
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.hypot(xx - PLAYER_SCREEN[0], (yy - PLAYER_SCREEN[1]) / K_GROUND)
    inner = (r >= RING_ANNULUS_PX[0]) & (r < RING_ANNULUS_PX[1])
    outer = (r >= RING_CONTROL_ANNULUS_PX[0]) & (r < RING_CONTROL_ANNULUS_PX[1]) & (yy < 900)
    return float(g[inner].mean()), float(g[outer].mean()), float(g[inner].mean() / max(g[outer].mean(), 1e-6))


def ocr_frames(paths):
    out = []
    if not paths:
        return out
    B = 12
    for i in range(0, len(paths), B):
        chunk = [str(p) for p in paths[i:i + B]]
        r = subprocess.run(["/tmp/pm4n/ocr"] + chunk, capture_output=True, text=True)
        out += [ln.split("\t") for ln in r.stdout.splitlines() if ln.count("\t") >= 6]
    return out


def pout_present(times, tag):
    """Extract frames at `times`, OCR them, apply the pre-registered P-OUT predicate.
    Returns {t: bool}."""
    d = WORK / tag
    d.mkdir(parents=True, exist_ok=True)
    paths = []
    for t in times:
        p = d / f"f_{t:.4f}.png"
        if not p.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", str(VIDEO),
                            "-frames:v", "1", "-y", str(p)], check=True)
        paths.append(p)
    rows = ocr_frames(paths)
    tmap = {str(p): t for p, t in zip(paths, times)}
    cache = {}
    obs = []
    for f in rows:
        path, text, conf, bx, by, bw, bh = f[0], f[1], f[2], *map(float, f[3:7])
        if path not in cache:
            cache.clear()
            cache[path] = np.asarray(Image.open(path).convert("RGB"))
        im = cache[path]
        H, W, _ = im.shape
        x0, x1 = int(bx * W), int((bx + bw) * W)
        y1, y0 = int((1 - by) * H), int((1 - by - bh) * H)
        x0, x1, y0, y1 = max(0, x0), min(W, x1), max(0, y0), min(H, y1)
        if x1 <= x0 or y1 <= y0:
            continue
        px = im[y0:y1, x0:x1].reshape(-1, 3).astype(float)
        sel = px[px.sum(1) >= np.percentile(px.sum(1), 88)]
        r, g, b = sel.mean(0)
        cls = classify(text, bx, by)
        obs.append(dict(frame=tmap[path], t_sec=tmap[path], text=text, cls=cls,
                        colour_class=colour_class(r, g), bbox_x=round(bx, 5), bbox_y=round(by, 5),
                        damage=parse_damage(text) if cls in ("crit", "bare", "crit_garbled") else None))
    hits, _ = p_out(obs, len(times))
    hitt = {h["frame"] for h in hits}
    return {t: (t in hitt) for t in times}


# ══════════════════════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 100)
    print("KC2-PM4 LAP R — LIMB B — video locomotion sampling")
    print("=" * 100)
    for ln in verify_pinned():
        print(ln)
    got = sha256(PLATES)
    assert got == PLATES_SHA, f"HALT: plates60 digest {got}"
    print(f"  EXACT  {got}  plates60_lapH2.npy")

    res = {}

    # ── B.1 movement episodes ────────────────────────────────────────────────────────────────
    cam = np.load(LAPH2 / "method" / "camera_translation_60fps_683-866.npy")
    t, v_raw = ground_speed(cam)
    v = rolling_median(v_raw, SMOOTH_FRAMES)
    m = (t >= FIGHT_T0) & (t <= FIGHT_T1)
    t, v, v_raw = t[m], v[m], v_raw[m]
    span = float(t[-1] - t[0])
    print(f"\n--- B.1 movement episodes ---")
    print(f"  camera trace: {len(t)} frames @60 fps, t={t[0]:.2f}..{t[-1]:.2f} ({span:.2f} s)")
    print(f"  smoothed ground speed percentiles (gpx/s): "
          + " ".join(f"p{q}={np.percentile(v, q):.0f}" for q in (10, 25, 50, 75, 90, 99)))

    ep_by_thr = {}
    for von in V_ON_SENSITIVITY:
        eps = episodes(t, v, von)
        tot = sum(b - a for a, b in eps)
        ep_by_thr[von] = eps
        print(f"  V_ON={von:>5.0f} gpx/s (V_OFF={von*V_OFF_RATIO:.0f}) : "
              f"{len(eps):>3} episodes, total {tot:7.2f} s = {tot/span:.4f} of fight, "
              f"median {np.median([b-a for a,b in eps]):.2f} s, "
              f"longest {max(b-a for a,b in eps):.2f} s")

    eps = ep_by_thr[V_ON_PRIMARY]
    rows = []
    for i, (a, b) in enumerate(eps):
        sel = (t >= a) & (t <= b)
        dur = b - a
        # net displacement across the episode = vector sum of per-frame camera translations
        mm = (cam[:, 0] >= a) & (cam[:, 0] <= b)
        net = float(np.hypot(cam[mm, 1].sum(), cam[mm, 2].sum() / K_GROUND))
        path = float(np.hypot(cam[mm, 1], cam[mm, 2] / K_GROUND).sum())
        rows.append(dict(
            episode_id=i, v_on_gpx_s=V_ON_PRIMARY, t_start=round(a, 4), t_end=round(b, 4),
            duration_s=round(dur, 4), wave=wave_of(a), wave_at_end=wave_of(b),
            mean_speed_gpx_s=round(float(v[sel].mean()), 2),
            peak_speed_gpx_s=round(float(v[sel].max()), 2),
            path_len_gpx=round(path, 1), net_displacement_gpx=round(net, 1),
            straightness=round(net / path, 4) if path > 0 else None,
        ))
    tot = sum(r["duration_s"] for r in rows)
    res["episodes"] = dict(
        v_on_primary=V_ON_PRIMARY, n=len(rows), total_moving_s=round(tot, 3),
        moving_fraction=round(tot / span, 6), span_s=round(span, 3),
        median_duration_s=round(float(np.median([r["duration_s"] for r in rows])), 4),
        longest_s=round(max(r["duration_s"] for r in rows), 4),
        stationary_fraction=round(1 - tot / span, 6),
        sensitivity={str(k): dict(n=len(vv), total_s=round(sum(b - a for a, b in vv), 3),
                                  frac=round(sum(b - a for a, b in vv) / span, 6))
                     for k, vv in ep_by_thr.items()},
    )
    # longest stationary spans
    gaps = []
    prev = t[0]
    for a, b in eps:
        if a - prev > 0:
            gaps.append((prev, a, a - prev))
        prev = b
    if t[-1] - prev > 0:
        gaps.append((prev, t[-1], t[-1] - prev))
    gaps.sort(key=lambda z: -z[2])
    res["longest_stationary_spans"] = [dict(t_start=round(g[0], 3), t_end=round(g[1], 3),
                                            duration_s=round(g[2], 3), wave=wave_of(g[0]))
                                       for g in gaps[:10]]
    print(f"  PRIMARY (V_ON=200): {len(rows)} episodes, moving fraction "
          f"{res['episodes']['moving_fraction']:.4f}, median {res['episodes']['median_duration_s']:.2f} s, "
          f"longest {res['episodes']['longest_s']:.2f} s")
    print("  longest STATIONARY spans (V_ON=200):")
    for g in res["longest_stationary_spans"][:6]:
        print(f"    {g['t_start']:.2f} .. {g['t_end']:.2f}  {g['duration_s']:.2f} s  (wave {g['wave']})")

    # per-wave episode summary
    pw = []
    for w in sorted(WAVE_START):
        a, b = WAVE_START[w], WAVE_END[w]
        ww = [r for r in rows if a <= r["t_start"] < b]
        sel = (t >= a) & (t < b)
        mv = float(((v[sel] >= V_ON_PRIMARY).sum()) / max(sel.sum(), 1))
        pw.append(dict(wave=w, span_s=round(b - a, 3), n_episodes=len(ww),
                       moving_frame_frac=round(mv, 4),
                       total_episode_s=round(sum(x["duration_s"] for x in ww), 3),
                       median_episode_s=(round(float(np.median([x["duration_s"] for x in ww])), 3)
                                         if ww else None)))
    res["per_wave_movement"] = pw
    print("  per-wave:  " + "  ".join(f"w{r['wave']}:{r['n_episodes']}ep/{r['moving_frame_frac']:.2f}"
                                      for r in pw))

    # ── B.2 detector validation ──────────────────────────────────────────────────────────────
    print(f"\n--- B.2 detector validation (independent NCC, seed={VALIDATION_SEED}) ---")
    rng = np.random.default_rng(VALIDATION_SEED)
    in_ep = np.zeros(len(t), dtype=bool)
    for a, b in eps:
        in_ep |= (t >= a) & (t <= b)
    ok = (t >= FIGHT_T0 + 1) & (t <= FIGHT_T1 - 1)
    mov_idx = np.flatnonzero(in_ep & ok)
    sta_idx = np.flatnonzero((~in_ep) & ok)
    pick = np.concatenate([rng.choice(mov_idx, VALIDATION_N_PER_CLASS, replace=False),
                           rng.choice(sta_idx, VALIDATION_N_PER_CLASS, replace=False)])
    vrows, agree, relerrs = [], 0, []
    for k, i in enumerate(pick):
        t0 = float(t[i])
        t1 = t0 + VALIDATION_DT_S
        cls_trace = "moving" if k < VALIDATION_N_PER_CLASS else "stationary"
        mm = (cam[:, 0] >= t0) & (cam[:, 0] < t1)
        trace_d = float(np.hypot(cam[mm, 1].sum(), cam[mm, 2].sum() / K_GROUND))
        a, b = gray(t0), gray(t1)
        cand = [ncc_best(a, b, p) for p in PATCHES]
        dx, dy, pk = max(cand, key=lambda z: z[2])
        ncc_d = float(np.hypot(dx, dy / K_GROUND))
        cls_ncc = "moving" if ncc_d >= VALIDATION_CLASS_CUT_GPX else "stationary"
        ag = cls_trace == cls_ncc
        agree += ag
        rel = abs(ncc_d - trace_d) / max(trace_d, 1e-6)
        if cls_trace == "moving":
            relerrs.append(rel)
        vrows.append(dict(t=round(t0, 4), class_trace=cls_trace, class_ncc=cls_ncc, agree=int(ag),
                          trace_disp_gpx=round(trace_d, 2), ncc_disp_gpx=round(ncc_d, 2),
                          ncc_peak=round(pk, 4), rel_err=round(rel, 4)))
        print(f"  {t0:8.3f}  trace={cls_trace:<10} ncc={cls_ncc:<10} "
              f"trace_d={trace_d:7.1f} ncc_d={ncc_d:7.1f} peak={pk:.3f} {'OK' if ag else 'DISAGREE'}")
    med = float(np.median(relerrs)) if relerrs else float("nan")
    verdict = ("PASS" if (agree >= VALIDATION_PASS_AGREE and med <= VALIDATION_PASS_MEDIAN_RELERR)
               else "FAIL")
    print(f"  agreement {agree}/20 (need >= {VALIDATION_PASS_AGREE}) · "
          f"median relative magnitude error on MOVING {med:.4f} "
          f"(need <= {VALIDATION_PASS_MEDIAN_RELERR}) -> {verdict}")
    res["validation"] = dict(rows=vrows, n_agree=int(agree), n=20,
                             median_rel_err_moving=round(med, 5), verdict=verdict,
                             pass_criterion=dict(min_agree=VALIDATION_PASS_AGREE,
                                                 max_median_rel_err=VALIDATION_PASS_MEDIAN_RELERR))

    # ── B.3 movement-while-channeling ────────────────────────────────────────────────────────
    print(f"\n--- B.3 movement-while-channeling ({CHANNEL_N_EPISODES} fastest episodes) ---")
    fastest = sorted(rows, key=lambda r: -r["mean_speed_gpx_s"])[:CHANNEL_N_EPISODES]
    mov_times = []
    for r in fastest:
        n = max(2, int(r["duration_s"] * CHANNEL_SAMPLE_FPS))
        mov_times += [round(r["t_start"] + j / CHANNEL_SAMPLE_FPS, 4)
                      for j in range(n) if r["t_start"] + j / CHANNEL_SAMPLE_FPS <= r["t_end"]]
    mov_times = sorted(set(mov_times))
    # matched STATIONARY control: same count, drawn from the longest stationary spans
    sta_times = []
    for g in res["longest_stationary_spans"]:
        n = max(2, int(g["duration_s"] * CHANNEL_SAMPLE_FPS))
        sta_times += [round(g["t_start"] + j / CHANNEL_SAMPLE_FPS, 4)
                      for j in range(n) if g["t_start"] + j / CHANNEL_SAMPLE_FPS <= g["t_end"]]
    sta_times = sorted(set(sta_times))[:len(mov_times)]
    print(f"  sampling {len(mov_times)} MOVING frames and {len(sta_times)} STATIONARY control "
          f"frames at {CHANNEL_SAMPLE_FPS:.0f} fps")

    pm = pout_present(mov_times, "chan_mov")
    ps = pout_present(sta_times, "chan_sta")
    fm = sum(pm.values()) / max(len(pm), 1)
    fs = sum(ps.values()) / max(len(ps), 1)
    rm = [ring_ratio(x)[2] for x in mov_times]
    rs = [ring_ratio(x)[2] for x in sta_times]
    print(f"  player-outgoing FCT present : MOVING {sum(pm.values())}/{len(pm)} = {fm:.4f}  |  "
          f"STATIONARY {sum(ps.values())}/{len(ps)} = {fs:.4f}   ratio {fm/max(fs,1e-9):.4f}")
    print(f"  channel-VFX ring ratio      : MOVING median {np.median(rm):.4f}  |  "
          f"STATIONARY median {np.median(rs):.4f}")

    if fm >= CHANNEL_CONTINUES_FRAC and np.median(rm) >= np.median(rs) * 0.9:
        cverdict = "CONTINUES"
    elif fs > 0 and fm < CHANNEL_INTERRUPTED_RATIO * fs:
        cverdict = "INTERRUPTED"
    else:
        cverdict = "UNDECIDED"
    print(f"  VERDICT (pre-registered rule): {cverdict}")

    witnessed = sorted([x for x, hit in pm.items() if hit])
    res["channeling"] = dict(
        verdict=cverdict, n_moving_frames=len(pm), n_stationary_frames=len(ps),
        fct_present_moving_frac=round(fm, 5), fct_present_stationary_frac=round(fs, 5),
        fct_ratio=round(fm / max(fs, 1e-9), 5),
        ring_ratio_moving_median=round(float(np.median(rm)), 5),
        ring_ratio_stationary_median=round(float(np.median(rs)), 5),
        ring_ratio_moving_p25_p75=[round(float(np.percentile(rm, 25)), 4),
                                   round(float(np.percentile(rm, 75)), 4)],
        ring_ratio_stationary_p25_p75=[round(float(np.percentile(rs, 25)), 4),
                                       round(float(np.percentile(rs, 75)), 4)],
        episodes_probed=[dict(episode_id=r["episode_id"], t_start=r["t_start"], t_end=r["t_end"],
                              mean_speed_gpx_s=r["mean_speed_gpx_s"], wave=r["wave"])
                         for r in fastest],
        witnessed_frames_t_sec=witnessed,
        witnessed_frames_frame_no=[int(round(x * 60.0)) for x in witnessed],
        note9="pixels cannot name WHICH skill draws the ring; ceiling is 'a player-centred "
              "channel VFX persists', never 'eyeofreckoning1 specifically persists'",
    )
    print(f"  witnessed movement-with-damage instants: {len(witnessed)}  "
          f"(60 fps frame numbers in JSON)")
    if witnessed:
        print("    first 12: " + ", ".join(f"t={x:.2f}/f{int(round(x*60))}" for x in witnessed[:12]))

    # channelling flag on each episode row
    hitset = set(witnessed)
    for r in rows:
        ts = [x for x in mov_times if r["t_start"] <= x <= r["t_end"]]
        r["channel_probed"] = int(bool(ts))
        r["channel_frames_sampled"] = len(ts)
        r["channel_frames_with_player_damage"] = sum(1 for x in ts if x in hitset)
        r["channeling_visible"] = ("" if not ts else
                                   int(r["channel_frames_with_player_damage"] > 0))

    # ── B.4 spawn-to-first-contact from the nameplate census ─────────────────────────────────
    print(f"\n--- B.4 wave-spawn-to-first-CONTACT (nameplate census; every count a LOWER BOUND) ---")
    R = np.load(PLATES)
    P = {}
    for r in R[R[:, 1] == 1]:
        if abs(r[2] - 960) < 50 and abs(r[3] - 429) < 16:
            P[round(r[0], 4)] = (r[2], r[3])
    M = R[R[:, 1] == 0]
    bym = {}
    for r in M:
        bym.setdefault(round(r[0], 4), []).append((r[2], r[3]))
    lat = []
    for w in sorted(WAVE_START):
        t0, t1 = WAVE_START[w], WAVE_END[w]
        row = dict(wave=w, t_wave_increment=t0)
        for RC in R_CONTACT_SENSITIVITY:
            first = None
            for tt in sorted(k for k in bym if t0 <= k <= t1):
                pl = P.get(tt)
                if pl is None:
                    continue
                if any(np.hypot(x - pl[0], (y - pl[1]) / K_GROUND) <= RC for x, y in bym[tt]):
                    first = tt
                    break
            row[f"t_first_contact_R{int(RC)}"] = first
            row[f"latency_plate_R{int(RC)}_s"] = (round(first - t0, 3) if first is not None else None)
        lat.append(row)
        print(f"  wave {w}  incr {t0:7.1f}  latency R120={row['latency_plate_R120_s']}  "
              f"R150={row['latency_plate_R150_s']}  R180={row['latency_plate_R180_s']}")
    res["spawn_to_first_contact_plate"] = lat

    # ── emit ─────────────────────────────────────────────────────────────────────────────────
    cols = ["episode_id", "v_on_gpx_s", "t_start", "t_end", "duration_s", "wave", "wave_at_end",
            "mean_speed_gpx_s", "peak_speed_gpx_s", "path_len_gpx", "net_displacement_gpx",
            "straightness", "channel_probed", "channel_frames_sampled",
            "channel_frames_with_player_damage", "channeling_visible"]
    d, n = dump_csv(OUT / "pm4r_movement_episodes.csv", rows, cols)
    print(f"\npm4r_movement_episodes.csv  rows={n}  sha256={d}")
    res["emitted"] = {"pm4r_movement_episodes.csv": {"sha256": d, "rows": n}}
    pathlib.Path("/tmp/pm4r/limb_b.json").write_text(json.dumps(res, indent=2, default=str))
    print("limb_b.json written")


if __name__ == "__main__":
    main()
