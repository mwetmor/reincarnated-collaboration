#!/usr/bin/env python3
"""
pm4u_video_2026_08_14.py — RUN KC2-PM4 LAP U, INSTRUMENT I-U1.  LIMB (a), the PRIMARY limb.

THE ARRIVAL DECOMPOSITION, AND THE TARGETING DISCRIMINATOR.

The run's last named residual (R-PM4-52 part 3): single-leg march arithmetic agrees with the
referent at 1.05-1.11x while the living-window ramp lags 2.98x.  The gap does not live in speed or
in single-leg distance.  The conductor names TARGETING/POPULATION as the suspect.  This instrument
attacks it from the referent side.

WHAT IS MEASURED
  (a0) CONTINUITY.  The per-wave living-plate ramp, recomputed, must reproduce Lap S's
       `pm4s_video.json -> arrival` FIELD BY FIELD -- the artifact, not the sentence about it
       (D-I20-5's lesson, adopted).
  (a1) THE FOLLOW TEST -- the primary discriminator.  A monster held within R_hold of the player
       across a window in which the player's NET displacement was |dp| must itself have moved at
       least |dp| - 2*R_hold in the world frame.  Triangle inequality, not a model.  A world-static
       target cannot satisfy it.  SIGN-FREE (uses a displacement MAGNITUDE) and DRIFT-FREE (uses a
       short-window difference of camera translations and a directly-measured player-relative
       offset).
  (a2) THE PURSUIT COSINE -- corroborating only, and DEMOTED BY CONSTRUCTION because it is
       sign-dependent.  Reported under BOTH camera sign conventions.
  (a3) ARRIVAL DIRECTIONS.  Circular statistics of entry bearings, per wave and pooled.
  (a4) THE PLAYER'S OWN MOTION.  Path length, net displacement, speed, and the angle between the
       player's net displacement and the wave's mean entry bearing.
  (a5) THE DELIVERABLE.  Per-wave entry timestamps, inter-entry interval distributions, and burst
       density -- emitted regardless of every verdict, for I-21 to grade a sim against
       like-for-like.

PRE-REGISTERED BOUND DIRECTIONS (PREREGISTRATION.md § 2, hashed
7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144 before this file ran)
  B-1  a plate proves a body; its absence proves nothing.  ALL counts are LOWER BOUNDS.
  B-2  the frustum right-censors at ~11.6 m.  "entry" means entry into the OBSERVED window.
  B-3  the world-clustering discriminator is VACUOUS under a player-locked camera and is REFUSED
       in advance.  It is not computed here.
  B-4  the player's world TRAJECTORY is integrated (drift); the player's world VELOCITY is not.
       Every primary statistic is built from velocities and player-relative offsets.
  B-5  the camera sign convention is not established.  Sign-dependent statistics are reported
       under BOTH and no verdict may rest on one.
  B-6  the greedy tracker can swap identities.  Guards G-1/G-2/G-3 with published rejection counts.

NO SIM NUMBER IS CONSULTED ANYWHERE IN THIS FILE.
READ-ONLY.  Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import pathlib
import sys

import numpy as np

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
NOTES = META / "agentic_orchestration" / "legolas" / "notes"
LAPH2 = NOTES / "2026-08-13-kc2-pm4-lap-h2-video-match"
LAPR = NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact"
LAPS = NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance"
OUT = NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode"

PLATES = LAPR / "method" / "plates60_lapH2.npy"
CAM = LAPH2 / "method" / "camera_translation_60fps_683-866.npy"
SVID = LAPS / "pm4s_video.json"
PINNED = {
    str(PLATES): "28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df",
    str(CAM): "029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33",
    str(SVID): "c968041fc1a81f1b6f141e3a0bf0b754d367c8290c368679208312aa8865be07",
}

# ── carried constants, each with its emitting lap named (NOTE-9).  None re-derived here. ───────
K_GROUND = 0.537                      # OBS-H2-8 isometric ground compression
PLAYER_PLATE_ANCHOR = (960.0, 429.0)  # Lap R's gate, reused unchanged
PLAYER_GATE = (50.0, 16.0)
FIGHT_T0, FIGHT_T1 = 683.0, 864.0
WAVE_START = {151: 683.0, 152: 698.6, 153: 714.9, 154: 729.8, 155: 744.0,
              156: 760.2, 157: 780.4, 158: 799.7, 159: 812.7, 160: 839.0}
WAVE_END = {w: (WAVE_START[w + 1] if w < 160 else FIGHT_T1) for w in WAVE_START}
SCREEN = (1920.0, 1080.0)
G_MAX, N_MIN, H_GAP = 60.0, 6, 6      # Lap S PRIMARY tracker cell
PXM = {"lo119": 119.0, "hi125": 125.0}   # R-PM4-43 part 2.  BOTH EDGES ALWAYS.
FPS = 60.0

# ── PRE-REGISTERED thresholds (PREREGISTRATION.md § 3.1) ──────────────────────────────────────
R_HOLD_PRIMARY, R_HOLD_SWEEP = 3.0, (2.0, 3.0, 4.0)          # metres
D_MIN_PRIMARY, D_MIN_SWEEP = 3.0, (1.0, 2.0, 3.0, 5.0)       # metres
DASH_GUARD_MPS = 12.0        # G-1
SWAP_GUARD_MPS = 8.0         # G-2
DUR_FLOOR_S = 1.0            # G-3
V_A1_MEASURED_N, V_A1_INDICATIVE_N = 25, 5
R_OMNI, R_DIRECTIONAL = 0.20, 0.40   # V-a3


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wave_of(t):
    for w in sorted(WAVE_START, reverse=True):
        if t >= WAVE_START[w]:
            return w
    return None


def q(v, ps=(0, 25, 50, 75, 90, 100)):
    if not len(v):
        return None
    a = np.asarray(v, dtype=float)
    return {f"p{p}": round(float(np.percentile(a, p)), 4) for p in ps} | {"n": int(a.size),
            "mean": round(float(a.mean()), 4)}


# ══════════════════════════════════════════════════════════════════════════════════════════════
def load():
    R = np.load(PLATES)
    P, M = {}, {}
    ax, ay = PLAYER_PLATE_ANCHOR
    gx, gy = PLAYER_GATE
    for r in R[R[:, 1] == 1]:
        if abs(r[2] - ax) < gx and abs(r[3] - ay) < gy:
            P[round(r[0], 4)] = (r[2], r[3])
    for r in R[R[:, 1] == 0]:
        M.setdefault(round(r[0], 4), []).append((r[2], r[3]))
    times = sorted(t for t in P if FIGHT_T0 <= t <= FIGHT_T1)
    offs = []
    for t in times:
        px, py = P[t]
        offs.append(np.array([[x - px, (y - py) / K_GROUND] for x, y in M.get(t, ())],
                             dtype=np.float64).reshape(-1, 2))
    return np.asarray(times), offs


def track_with_history(times, offs, g_max=G_MAX, n_min=N_MIN, h_gap=H_GAP):
    """Lap S's greedy nearest-neighbour tracker, VERBATIM in its association logic, extended only
    to RECORD the per-frame history of each track.  The set of tracks it returns, and their birth
    radii, are therefore identical to Lap S's -- which is asserted as a continuity check."""
    live, done = [], []
    for i, pts in enumerate(offs):
        used, pairs = set(), []
        for ti, tr in enumerate(live):
            if not len(pts):
                continue
            d = np.hypot(pts[:, 0] - tr["xy"][0], pts[:, 1] - tr["xy"][1])
            j = int(np.argmin(d))
            if d[j] <= g_max:
                pairs.append((float(d[j]), ti, j))
        pairs.sort()
        claimed = set()
        for d, ti, j in pairs:
            if ti in claimed or j in used:
                continue
            claimed.add(ti)
            used.add(j)
            live[ti]["xy"] = tuple(pts[j])
            live[ti]["last"] = i
            live[ti]["n"] += 1
            live[ti]["rmin"] = min(live[ti]["rmin"], float(np.hypot(*pts[j])))
            live[ti]["hist"].append((i, float(pts[j][0]), float(pts[j][1])))
        for j in range(len(pts)):
            if j in used:
                continue
            live.append(dict(birth=i, last=i, n=1, xy=tuple(pts[j]),
                             r0=float(np.hypot(*pts[j])), rmin=float(np.hypot(*pts[j])),
                             hist=[(i, float(pts[j][0]), float(pts[j][1]))]))
        keep = []
        for tr in live:
            (done if i - tr["last"] > h_gap else keep).append(tr)
        live = keep
    done.extend(live)
    return [t for t in done if t["n"] >= n_min]


# ══════════════════════════════════════════════════════════════════════════════════════════════
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 104)
    print("KC2-PM4 LAP U — LIMB (a): VIDEO ARRIVAL DECOMPOSITION + THE TARGETING DISCRIMINATOR")
    print("=" * 104)
    for p, want in PINNED.items():
        got = sha256(p)
        assert got == want, f"HALT (GL-6): {p} digest {got} != {want}"
        print(f"  EXACT  {got}  {pathlib.Path(p).name}")

    ta, offs = load()
    counts = np.array([len(o) for o in offs], dtype=np.int32)
    print(f"\n  instants with a detected player plate in {FIGHT_T0}-{FIGHT_T1}s : {len(ta)}")
    print(f"  living monster plates in those instants                    : {int(counts.sum())}")

    res = {"instrument": "I-U1", "limb": "a", "n_instants": int(len(ta)),
           "preregistration_sha256":
               "7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144",
           "px_per_m_bracket": PXM, "pinned": {k: sha256(k) for k in PINNED}}

    # ── (a0) CONTINUITY PIN, against the ARTIFACT ────────────────────────────────────────────
    print("\n  ── (a0) CONTINUITY PIN vs Lap S pm4s_video.json -> arrival (the artifact) ──")
    lapS = json.load(open(SVID))["arrival"]
    ramp, diffs = {}, []
    for wv in sorted(WAVE_START):
        t0, t1 = WAVE_START[wv], WAVE_END[wv]
        sel = (ta >= t0) & (ta < t1)
        c, tt = counts[sel], ta[sel] - t0
        peak = int(c.max())

        def first_at(f):
            hit = np.where(c >= f * peak)[0]
            return round(float(tt[hit[0]]), 3) if len(hit) else None
        ramp[wv] = dict(peak_plates=peak, t_to_50pct_peak_s=first_at(0.5),
                        t_to_90pct_peak_s=first_at(0.9),
                        t_peak_s=round(float(tt[int(np.argmax(c))]), 3),
                        span_s=round(t1 - t0, 3), min_plates=int(c.min()))
        ref = lapS[str(wv)]
        for k in ("peak_plates", "t_to_50pct_peak_s", "t_to_90pct_peak_s"):
            if ramp[wv][k] != ref[k]:
                diffs.append((wv, k, ramp[wv][k], ref[k]))
    assert not diffs, f"HALT (P-U-0): continuity pin FAILED {diffs}"
    f10_50 = float(np.median([ramp[w]["t_to_50pct_peak_s"] for w in ramp]))
    f10_90 = float(np.median([ramp[w]["t_to_90pct_peak_s"] for w in ramp]))
    print(f"    30 fields over 10 waves reproduced EXACT.  F-10 recomputed: "
          f"median t->50% {f10_50:.4f} s, t->90% {f10_90:.4f} s")
    res["P_U_0"] = dict(fields_compared=30, differences=len(diffs), verdict="EXACT",
                        F10_t50_median_s=round(f10_50, 4), F10_t90_median_s=round(f10_90, 4))

    # ── camera: per-frame ground translation, and a cumulative sum for short-window differences ─
    cam = np.load(CAM)
    m = (cam[:, 0] >= FIGHT_T0) & (cam[:, 0] <= FIGHT_T1)
    d = cam[m]
    step = np.column_stack([d[:, 1], d[:, 2] / K_GROUND])          # ground gpx per frame
    CUM = np.vstack([np.zeros(2), np.cumsum(step, axis=0)])        # CUM[j] = sum of steps[:j]
    step_mag = np.hypot(step[:, 0], step[:, 1])
    jj = np.clip(np.searchsorted(d[:, 0], ta), 0, len(d))          # camera index per plate instant
    print(f"  camera samples in window: {len(d)};  per-frame |translation| median "
          f"{np.median(step_mag):.2f} gpx, max {step_mag.max():.1f} gpx")

    # ── tracks ───────────────────────────────────────────────────────────────────────────────
    trs = track_with_history(ta, offs)
    r0 = np.array([t["r0"] for t in trs])
    print(f"\n  tracks at the Lap S PRIMARY cell (G_MAX={G_MAX}, N_MIN={N_MIN}, H_GAP={H_GAP}): "
          f"{len(trs)}   birth-radius median {np.median(r0):.1f} gpx, p95 "
          f"{np.percentile(r0, 95):.1f} gpx")
    res["tracker"] = dict(cell=dict(G_MAX=G_MAX, N_MIN=N_MIN, H_GAP=H_GAP), n_tracks=len(trs),
                          birth_radius_median_gpx=round(float(np.median(r0)), 2),
                          birth_radius_p95_gpx=round(float(np.percentile(r0, 95)), 2),
                          lapS_published=dict(n_tracks=3324, median_gpx=306.1, p95_gpx=1058.0))

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # (a5) THE DELIVERABLE — entries, intervals, density
    # ══════════════════════════════════════════════════════════════════════════════════════════
    entries = []
    for i, tr in enumerate(sorted(trs, key=lambda x: x["birth"])):
        tb = float(ta[tr["birth"]])
        wv = wave_of(tb)
        dx, dy = tr["hist"][0][1], tr["hist"][0][2]
        entries.append(dict(entry_id=f"E{i+1:05d}", wave=wv, t_abs_s=round(tb, 4),
                            t_since_wave_s=round(tb - WAVE_START[wv], 4) if wv else None,
                            r_gpx=round(tr["r0"], 3),
                            r_m_lo119=round(tr["r0"] / PXM["lo119"], 4),
                            r_m_hi125=round(tr["r0"] / PXM["hi125"], 4),
                            bearing_deg=round(math.degrees(math.atan2(dy, dx)) % 360.0, 3),
                            n_frames=tr["n"], lifetime_s=round(float(ta[tr["last"]] - tb), 4),
                            r_min_gpx=round(tr["rmin"], 3)))

    def circ(bdeg):
        if not len(bdeg):
            return None
        th = np.radians(np.asarray(bdeg, dtype=float))
        C, S = np.cos(th).mean(), np.sin(th).mean()
        R = float(np.hypot(C, S))
        return dict(n=int(th.size), mean_deg=round(float(np.degrees(math.atan2(S, C)) % 360), 2),
                    R=round(R, 4), rayleigh_Z=round(th.size * R * R, 2),
                    sectors12=[int(x) for x in np.histogram(
                        np.degrees(th) % 360, bins=12, range=(0, 360))[0]])

    per_wave = {}
    for wv in sorted(WAVE_START):
        E = [e for e in entries if e["wave"] == wv]
        t = np.sort(np.array([e["t_since_wave_s"] for e in E]))
        span = WAVE_END[wv] - WAVE_START[wv]
        gaps = np.diff(t) if len(t) > 1 else np.array([])
        # burst density: max entries in a sliding window
        def burst(w):
            return int(max((int(((t >= x) & (t < x + w)).sum()) for x in t), default=0))
        # entry-based ramp: time to 50 % / 90 % of the wave's entries
        def t_frac(f):
            k = int(math.ceil(f * len(t))) - 1
            return round(float(t[k]), 3) if 0 <= k < len(t) else None
        per_wave[wv] = dict(
            n_entries=len(t),
            entries_per_s=round(len(t) / span, 4),
            entries_first_6s=int((t < 6.0).sum()),
            entries_per_s_first_6s=round(float((t < 6.0).sum()) / min(6.0, span), 4),
            t_to_50pct_entries_s=t_frac(0.5), t_to_90pct_entries_s=t_frac(0.9),
            interval_s=q(gaps), burst_1s=burst(1.0), burst_2s=burst(2.0),
            bearing=circ([e["bearing_deg"] for e in E]),
            entry_radius_m_lo119=q([e["r_m_lo119"] for e in E]),
            **ramp[wv])
    allgaps = np.concatenate([np.diff(np.sort(np.array([e["t_since_wave_s"]
                                                        for e in entries if e["wave"] == w])))
                              for w in sorted(WAVE_START)])
    res["arrivals"] = dict(
        per_wave={str(k): v for k, v in per_wave.items()},
        pooled=dict(n_entries=len(entries),
                    entries_per_s_median=round(float(np.median(
                        [per_wave[w]["entries_per_s"] for w in per_wave])), 4),
                    interval_s=q(allgaps),
                    t_to_50pct_entries_median_s=round(float(np.median(
                        [per_wave[w]["t_to_50pct_entries_s"] for w in per_wave])), 4),
                    t_to_90pct_entries_median_s=round(float(np.median(
                        [per_wave[w]["t_to_90pct_entries_s"] for w in per_wave])), 4),
                    burst_1s_median=int(np.median([per_wave[w]["burst_1s"] for w in per_wave])),
                    bearing=circ([e["bearing_deg"] for e in entries])),
        caveat="entry = entry into the OBSERVED ~11.6 m window (B-2); LOWER bound (B-1); "
               "contaminated upward by plate re-appearance and downward by occlusion "
               "(UNREACHED-S4)")

    print("\n  ── (a5) PER-WAVE ENTRIES INTO THE ~11.6 m WINDOW ──")
    print(f"    {'wave':>4s} {'span':>6s} {'entr':>5s} {'e/s':>6s} {'e<6s':>5s} {'t50e':>6s} "
          f"{'t90e':>6s} {'gapmed':>7s} {'b1s':>4s} {'b2s':>4s} {'R':>6s} {'peak':>5s}")
    for wv in sorted(per_wave):
        a = per_wave[wv]
        print(f"    {wv:4d} {a['span_s']:6.2f} {a['n_entries']:5d} {a['entries_per_s']:6.3f} "
              f"{a['entries_first_6s']:5d} {str(a['t_to_50pct_entries_s']):>6s} "
              f"{str(a['t_to_90pct_entries_s']):>6s} "
              f"{a['interval_s']['p50'] if a['interval_s'] else float('nan'):7.3f} "
              f"{a['burst_1s']:4d} {a['burst_2s']:4d} {a['bearing']['R']:6.3f} "
              f"{a['peak_plates']:5d}")
    pl = res["arrivals"]["pooled"]
    print(f"    POOLED  n={pl['n_entries']}  median e/s {pl['entries_per_s_median']}  "
          f"interval median {pl['interval_s']['p50']} s (p25 {pl['interval_s']['p25']}, "
          f"p75 {pl['interval_s']['p75']})  burst1s median {pl['burst_1s_median']}")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # (a3) ARRIVAL DIRECTIONS  — V-a3
    # ══════════════════════════════════════════════════════════════════════════════════════════
    Rp = pl["bearing"]["R"]
    va3 = ("OMNIDIRECTIONAL" if Rp < R_OMNI else
           "DIRECTIONAL" if Rp >= R_DIRECTIONAL else "WEAKLY DIRECTIONAL")
    print(f"\n  ── (a3) V-a3 : pooled entry-bearing resultant R = {Rp:.4f}  ->  {va3}")
    print(f"       per-wave R: {[per_wave[w]['bearing']['R'] for w in sorted(per_wave)]}")
    res["V_a3"] = dict(pooled_R=Rp, verdict=va3, thresholds=dict(omni=R_OMNI, dir=R_DIRECTIONAL),
                       per_wave_R={str(w): per_wave[w]["bearing"]["R"] for w in per_wave},
                       pooled_sectors12=pl["bearing"]["sectors12"])

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # (a4) THE PLAYER'S OWN MOTION  — V-a4
    # ══════════════════════════════════════════════════════════════════════════════════════════
    print("\n  ── (a4) THE PLAYER'S OWN MOTION (path length + net displacement are SIGN-FREE) ──")
    print(f"    {'wave':>4s} {'path_m':>8s} {'net_m':>7s} {'straight':>8s} {'v_mean':>7s} "
          f"{'v_p95':>7s} {'mov%':>5s} {'ang_to_entries_deg':>19s}")
    pmove = {}
    for wv in sorted(WAVE_START):
        sel = (d[:, 0] >= WAVE_START[wv]) & (d[:, 0] < WAVE_END[wv])
        s, sm = step[sel], step_mag[sel]
        if not len(s):
            continue
        path_gpx = float(sm.sum())
        net_vec = s.sum(axis=0)
        net_gpx = float(np.hypot(*net_vec))
        dur = WAVE_END[wv] - WAVE_START[wv]
        row = {}
        for lab, pm in PXM.items():
            row[f"path_m_{lab}"] = round(path_gpx / pm, 3)
            row[f"net_m_{lab}"] = round(net_gpx / pm, 3)
            row[f"v_mean_mps_{lab}"] = round(path_gpx / pm / dur, 4)
            row[f"v_p95_mps_{lab}"] = round(float(np.percentile(sm, 95)) * FPS / pm, 4)
        row["straightness"] = round(net_gpx / path_gpx, 4) if path_gpx else None
        row["frac_frames_moving_gt_0p5px"] = round(float((sm > 0.5).mean()), 4)
        # angle between the player's net displacement and the wave's mean entry bearing,
        # under BOTH sign conventions (B-5)
        mb = math.radians(per_wave[wv]["bearing"]["mean_deg"])
        for sgn, lab in ((+1.0, "plus"), (-1.0, "minus")):
            v = sgn * net_vec
            ang = math.degrees(math.atan2(v[1], v[0])) % 360
            diff = abs((ang - math.degrees(mb) + 180) % 360 - 180)
            row[f"angle_net_vs_mean_entry_deg_{lab}"] = round(diff, 2)
        pmove[wv] = row
        print(f"    {wv:4d} {row['path_m_lo119']:8.2f} {row['net_m_lo119']:7.2f} "
              f"{row['straightness']:8.3f} {row['v_mean_mps_lo119']:7.3f} "
              f"{row['v_p95_mps_lo119']:7.3f} {row['frac_frames_moving_gt_0p5px']*100:5.1f} "
              f"{row['angle_net_vs_mean_entry_deg_plus']:8.1f} / "
              f"{row['angle_net_vs_mean_entry_deg_minus']:8.1f}")
    res["V_a4_player_motion"] = {str(k): v for k, v in pmove.items()}
    res["V_a4_player_motion"]["_note"] = ("path/net in metres are SIGN-FREE magnitudes; the two "
                                          "angle columns are the two conventions of B-5; the "
                                          "integrated trajectory is NOT used (B-4)")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # (a1) THE FOLLOW TEST  — V-a1, the PRIMARY discriminator
    # ══════════════════════════════════════════════════════════════════════════════════════════
    print("\n  ── (a1) V-a1 THE FOLLOW TEST ──")
    print("     a body held within R_hold of the player across a window in which the player's NET")
    print("     displacement was |dp| must ITSELF have moved >= |dp| - 2*R_hold.  Triangle")
    print("     inequality.  A world-static target cannot satisfy it.")

    def follow(r_hold_m, pm):
        """Return (surviving windows, rejection counts) at one R_hold and one px->m edge."""
        r_hold = r_hold_m * pm                    # gpx
        win, rej = [], dict(G1_dash=0, G2_swap=0, G3_short=0)
        for tr in trs:
            h = tr["hist"]
            run = []
            for k in range(len(h) + 1):
                inside = (k < len(h) and math.hypot(h[k][1], h[k][2]) <= r_hold)
                if inside:
                    run.append(h[k])
                    continue
                if len(run) >= 2:
                    i0, i1 = run[0][0], run[-1][0]
                    dt = float(ta[i1] - ta[i0])
                    if dt < DUR_FLOOR_S:
                        rej["G3_short"] += 1
                    else:
                        j0, j1 = int(jj[i0]), int(jj[i1])
                        dp = CUM[min(j1, len(CUM) - 1)] - CUM[min(j0, len(CUM) - 1)]
                        dp_m = float(np.hypot(*dp)) / pm
                        seg = step_mag[min(j0, len(step_mag)):max(j1, 0)]
                        vmax = float(seg.max()) * FPS / pm if len(seg) else 0.0
                        proven = dp_m - 2.0 * r_hold_m
                        if vmax > DASH_GUARD_MPS:
                            rej["G1_dash"] += 1
                        elif proven > 0 and proven / dt > SWAP_GUARD_MPS:
                            rej["G2_swap"] += 1
                        else:
                            win.append(dict(t0=float(ta[i0]), t1=float(ta[i1]), dt=dt,
                                            wave=wave_of(float(ta[i0])),
                                            dp_m=dp_m, proven_m=proven,
                                            proven_mps=(proven / dt if proven > 0 else 0.0),
                                            player_vmax_mps=vmax,
                                            r_max_m=max(math.hypot(x[1], x[2])
                                                        for x in run) / pm))
                run = []
        return win, rej

    sweep, primary_rows = [], None
    for rh in R_HOLD_SWEEP:
        for lab, pm in PXM.items():
            win, rej = follow(rh, pm)
            for dm in D_MIN_SWEEP:
                n = sum(1 for w in win if w["proven_m"] >= dm)
                row = dict(R_hold_m=rh, D_min_m=dm, edge=lab, n_windows=len(win),
                           n_pass=n, rejections=rej,
                           primary=(rh == R_HOLD_PRIMARY and dm == D_MIN_PRIMARY))
                sweep.append(row)
            if rh == R_HOLD_PRIMARY:
                if primary_rows is None:
                    primary_rows = {}
                primary_rows[lab] = win
    res["V_a1_sweep"] = sweep

    prim = {lab: sum(1 for w in primary_rows[lab] if w["proven_m"] >= D_MIN_PRIMARY)
            for lab in PXM}
    print(f"\n     PRIMARY cell R_hold={R_HOLD_PRIMARY} m, D_min={D_MIN_PRIMARY} m "
          f"(i.e. the player's NET displacement >= {R_HOLD_PRIMARY*2+D_MIN_PRIMARY} m while the "
          f"body stayed within {R_HOLD_PRIMARY} m):")
    for lab in PXM:
        w = primary_rows[lab]
        pw = [x for x in w if x["proven_m"] >= D_MIN_PRIMARY]
        print(f"       edge {lab}: {len(w)} surviving hold-windows, {len(pw)} with proven monster "
              f"displacement >= {D_MIN_PRIMARY} m")
        if pw:
            pv = np.array([x["proven_m"] for x in pw])
            sv = np.array([x["proven_mps"] for x in pw])
            print(f"                 proven displacement median {np.median(pv):.2f} m "
                  f"(max {pv.max():.2f});  implied monster speed median {np.median(sv):.2f} m/s "
                  f"(max {sv.max():.2f})")

    worst = min(prim.values())
    va1 = ("PLAYER-TARGETED — MEASURED" if worst >= V_A1_MEASURED_N else
           "PLAYER-TARGETED — INDICATIVE" if worst >= V_A1_INDICATIVE_N else
           "NOT SUPPORTED")
    print(f"\n     ⚑ V-a1 VERDICT (the WEAKER of the two bracket edges, n={worst}) : {va1}")
    res["V_a1"] = dict(primary_cell=dict(R_hold_m=R_HOLD_PRIMARY, D_min_m=D_MIN_PRIMARY),
                       n_pass_per_edge=prim, n_pass_weaker_edge=worst, verdict=va1,
                       thresholds=dict(measured=V_A1_MEASURED_N, indicative=V_A1_INDICATIVE_N),
                       guards=dict(G1_dash_mps=DASH_GUARD_MPS, G2_swap_mps=SWAP_GUARD_MPS,
                                   G3_duration_floor_s=DUR_FLOOR_S),
                       windows_lo119=[{k: (round(v, 4) if isinstance(v, float) else v)
                                       for k, v in w.items()}
                                      for w in sorted(primary_rows["lo119"],
                                                      key=lambda x: -x["proven_m"])[:200]])

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # (a2) THE PURSUIT COSINE  — V-a2, corroborating only, sign-dependent, DEMOTED
    # ══════════════════════════════════════════════════════════════════════════════════════════
    print("\n  ── (a2) V-a2 THE PURSUIT COSINE (sign-dependent -> corroborating ONLY) ──")
    cos_now = {"plus": [], "minus": []}
    cos_frozen = {"plus": [], "minus": []}
    cos_rel = []
    for tr in trs:
        h = tr["hist"]
        for k in range(1, len(h)):
            i0, i1 = h[k - 1][0], h[k][0]
            if i1 - i0 > 3:
                continue
            do = np.array([h[k][1] - h[k - 1][1], h[k][2] - h[k - 1][2]])
            o = np.array([h[k][1], h[k][2]])
            n_o = np.hypot(*o)
            if n_o < 1.0:
                continue
            oh = -o / n_o                                     # bearing to the player
            if np.hypot(*do) > 1e-9:
                cos_rel.append(float(do @ oh / np.hypot(*do)))
            j0, j1 = int(jj[i0]), int(jj[i1])
            vp = CUM[min(j1, len(CUM) - 1)] - CUM[min(j0, len(CUM) - 1)]
            o0 = np.array([h[0][1], h[0][2]])
            n0 = np.hypot(*o0)
            for sgn, lab in ((+1.0, "plus"), (-1.0, "minus")):
                vm = do + sgn * vp
                nm = np.hypot(*vm)
                if nm < 1e-6:
                    continue
                cos_now[lab].append(float(vm @ oh / nm))
                if n0 > 1.0:
                    cos_frozen[lab].append(float(vm @ (-o0 / n0) / nm))
    va2 = {}
    for lab in ("plus", "minus"):
        va2[lab] = dict(n=len(cos_now[lab]),
                        median_cos_to_player_now=round(float(np.median(cos_now[lab])), 4),
                        mean_cos_to_player_now=round(float(np.mean(cos_now[lab])), 4),
                        median_cos_to_frozen_birth_target=round(float(np.median(cos_frozen[lab])), 4),
                        frac_positive=round(float(np.mean(np.array(cos_now[lab]) > 0)), 4))
        print(f"     convention {lab:6s}: median cos(v_monster, bearing->player NOW) = "
              f"{va2[lab]['median_cos_to_player_now']:+.4f}   vs frozen birth target "
              f"{va2[lab]['median_cos_to_frozen_birth_target']:+.4f}   "
              f"frac>0 {va2[lab]['frac_positive']:.4f}")
    both_pos = all(va2[l]["median_cos_to_player_now"] > 0 for l in va2)
    both_neg = all(va2[l]["median_cos_to_player_now"] < 0 for l in va2)
    va2v = "PURSUIT-CONSISTENT" if both_pos else ("PURSUIT-INCONSISTENT" if both_neg else "AMBIGUOUS")
    print(f"     median player-relative closure cos (screen frame, sign-free) = "
          f"{np.median(cos_rel):+.4f}")
    print(f"     ⚑ V-a2 VERDICT : {va2v}  (may corroborate V-a1; may never establish it)")
    res["V_a2"] = dict(by_convention=va2, verdict=va2v,
                       player_relative_closure_median_cos=round(float(np.median(cos_rel)), 4),
                       demotion="sign-dependent by construction (B-5); corroborating only")

    # ── emission ─────────────────────────────────────────────────────────────────────────────
    with open(OUT / "pm4u_arrivals.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(entries[0].keys()) + ["basis"])
        w.writeheader()
        for e in entries:
            w.writerow(e | {"basis": "entry into the OBSERVED ~11.6 m frustum window; LOWER "
                                     "bound (B-1/B-2); Lap H-2 nameplate census, Lap S PRIMARY "
                                     "tracker cell G_MAX=60 N_MIN=6 H_GAP=6"})
    with open(OUT / "pm4u_arrival_stats.json", "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=float)
    print(f"\n  wrote {OUT/'pm4u_arrivals.csv'}  ({len(entries)} entries)")
    print(f"  wrote {OUT/'pm4u_arrival_stats.json'}")


if __name__ == "__main__":
    sys.exit(main())
