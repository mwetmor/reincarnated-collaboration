#!/usr/bin/env python3
"""KC2-PM4 Lap AC — FORK (b) + FORK (c) + leg A-3.

  (b)  REFERENT MONSTER RING-RESIDENCE from the pinned Lap H-2 nameplate census:
       per-body ring-entry time, ring-exit time, residence duration, truncation-flagged.
  (c)  THE EXIT-CHANNEL SPLIT: alive-vs-death-candidate, and a frozen-counterfactual
       partition of WHO MOVED at each observed ring exit.
  A-3  the emplacement signature in the RED population (CORROBORATIVE, never dispositive).

  MEASURED QUANTITY : for each tracked red nameplate, the maximal runs of consecutive
                      observed 60 fps instants whose plate anchor lies within R_gpx of the
                      player's plate anchor (ground plane de-projected by K=0.537).
  BOUND DIRECTION   : plate presence PROVES a living body; plate absence does NOT prove
                      absence (occlusion, VFX saturation, plate suppression).  Every count
                      is a LOWER BOUND and every residence a TRUNCATED observation.
                      ONE-DIRECTIONAL, declared.  (bars.py:12-15, NOTE-9)

READ-ONLY.  OUTCOME-FIREWALLED — no simulation artifact of any kind is opened.
NO SIM GRADE IS COMPUTED ANYWHERE IN THIS FILE.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4ac_lib_2026_08_16 import (                                           # noqa: E402
    OUT, LAPR, FIGHT_T0, FIGHT_T1, WAVE_START, WAVE_END, K_GROUND, DT, FPS,
    RING_RUNGS, RING_PRIMARY, R_CONTACT_VISUAL, GAP_JOIN_S,
    STATIONARY_NET_GPX, STATIONARY_MIN_S, EDGE_MARGIN_PX, REDETECT_WINDOW_S,
    REDETECT_ABORT_FRAC, F_AC_1_TOL, F_AC_1_MIN_OBS, F_AC_1_MIN_INTERVALS,
    F_AC_2_MIN_DECIDABLE, F_AC_2_SHARE_PASS, EXIT_SPEED_HALFWIN_S, SMOOTH_FRAMES,
    PREREG_SHA, verify_pinned, verify_prereg, sha256, dump_csv, quantiles,
    load_plates, load_camera, player_plates, import_h2_tracker, wave_of, ground_dist,
)

FRAME_W, FRAME_H = 1920.0, 1080.0


# ══════════════════════════════════════════════════════════════════════════════════════════════
def pinned_bracket():
    """Read the pinned occupancy bracket BY IDENTITY out of pm4r_contact_occupancy.csv.

    Rows `at_sim_D_ENGAGE_M_2.400` are the ONLY like-for-like rungs for a 2.400 m ring on
    referent pixels (prereg § 2.1).  Read, never re-derived.
    """
    import csv
    out = {}
    with open(LAPR / "pm4r_contact_occupancy.csv") as fh:
        for row in csv.DictReader(fh):
            if row["scope"] == "at_sim_D_ENGAGE_M_2.400":
                out[float(row["R_gpx"])] = dict(
                    dry_fraction=float(row["dry_fraction"]),
                    mean_occupancy=float(row["mean_occupancy"]),
                    basis=row["basis"],
                )
    return out


def build_world(d1b, R, cam):
    """d1b.world() imported BY IDENTITY; d1b.load() (which reads /tmp) is never called."""
    ct = cam[:, 0]
    cx = np.concatenate([[0.0], np.cumsum(cam[:, 1])])
    cy = np.concatenate([[0.0], np.cumsum(cam[:, 2])])
    ctt = np.concatenate([ct, [ct[-1] + 1 / FPS]])
    W, _pw_ground = d1b.world(R, ctt, cx, cy)
    return W, ctt, cx, cy


def player_world(P, ctt, cx, cy):
    """Player PLATE anchor in the world frame: screen minus cumulative camera translation.

    Uses the DETECTED plate anchor (not a fixed screen constant) so that the world-frame
    separation is numerically identical to the screen-frame ring metric.  prereg § 8.1 note 4.
    """
    ts = np.array(sorted(P))
    CX = np.interp(ts, ctt, cx)
    CY = np.interp(ts, ctt, cy)
    return {round(float(t), 4): (P[round(float(t), 4)][0] - CX[i],
                                 P[round(float(t), 4)][1] - CY[i])
            for i, t in enumerate(ts)}


def intervals_from(flags, times, join_s=GAP_JOIN_S):
    """Maximal runs of True joined across observed-time gaps < `join_s`.

    Returns list of (i_start, i_end_inclusive, n_internal_gaps).  The DEFAULT gap rule is
    pm4r_contact_2026_08_14.py:112 / :136, imported by identity in form, and is the
    PRE-REGISTERED functional (prereg § 4.3).  A wider `join_s` is used only for the
    explicitly-labelled post-hoc sensitivity ladder in § 4.3b of the findings.
    """
    out = []
    i = 0
    n = len(flags)
    while i < n:
        if not flags[i]:
            i += 1
            continue
        j = i
        gaps = 0
        while j + 1 < n and flags[j + 1]:
            if (times[j + 1] - times[j]) >= join_s:
                break
            if (times[j + 1] - times[j]) > DT * 1.5:
                gaps += 1
            j += 1
        out.append((i, j, gaps))
        i = j + 1
    return out


def plate_continuity(W, t0, t1):
    """The OBSTACLE, measured: what fraction of monster plates at instant t have a plate
    within the tracker's own association gate at t + 1/60?

    This is the identity-continuity ceiling of the whole pinned pipeline.  It is not an
    assumption and it is not an estimate: it is counted, over the same corpus.
    """
    ts = sorted(t for t in W if t0 <= t <= t1)
    tot = hit = 0
    n_missing_pairs = 0
    for i in range(len(ts) - 1):
        if abs(ts[i + 1] - ts[i] - DT) > 1e-3:
            n_missing_pairs += 1
            continue
        A = np.array([(o[0], o[1]) for o in W[ts[i]]])
        B = np.array([(o[0], o[1]) for o in W[ts[i + 1]]])
        if len(A) == 0 or len(B) == 0:
            continue
        d = np.hypot(A[:, None, 0] - B[None, :, 0], (A[:, None, 1] - B[None, :, 1]) / K_GROUND)
        tot += len(A)
        hit += int((d.min(axis=1) <= 30.0).sum())
    return dict(n_instants=len(ts), n_plates_tested=int(tot), n_with_successor=int(hit),
                continuity=round(hit / max(tot, 1), 6),
                gate_gpx=30.0, gate_source="d1b.track default `gate=30.0`",
                n_instant_pairs_not_adjacent=int(n_missing_pairs))


# ══════════════════════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 100)
    print("KC2-PM4 LAP AC — FORK (b) ring residence · FORK (c) exit channel · leg A-3")
    print("=" * 100)
    print(f"  EXACT  {verify_prereg(PREREG_SHA)}  prereg.md")
    for ln in verify_pinned(skip_video=True):
        print(ln)

    res = {
        "lap": "AC",
        "forks": ["b", "c", "A-3"],
        "prereg_sha256": PREREG_SHA,
        "bound_direction": "plate presence proves a living body; plate absence does NOT prove "
                           "absence -> counts are LOWER BOUNDS and residences are TRUNCATED "
                           "observations (bars.py:12-15, NOTE-9). ONE-DIRECTIONAL.",
        "firewall": "no simulation artifact opened; no sim grade computed",
    }

    d1b = import_h2_tracker()
    R = load_plates()
    cam = load_camera()
    P = player_plates(R)
    W, ctt, cx, cy = build_world(d1b, R, cam)
    PW = player_world(P, ctt, cx, cy)

    obs_times = sorted(t for t in P if FIGHT_T0 <= t <= FIGHT_T1)
    N_obs = len(obs_times)
    obs_set = set(obs_times)
    print(f"\n  instants with a detected PLAYER plate in [{FIGHT_T0}, {FIGHT_T1}] : {N_obs}")
    print(f"  monster plate rows : {int((R[:,1]==0).sum())}   player plate rows : "
          f"{int((R[:,1]==1).sum())}")
    res["n_observed_instants"] = N_obs
    res["n_monster_plate_rows"] = int((R[:, 1] == 0).sum())
    res["n_player_plate_rows"] = int((R[:, 1] == 1).sum())

    # ── TRACKING, per contiguous wave window (prereg § 4.1) ──────────────────────────────────
    print("\n--- tracking (d1b.track imported BY IDENTITY, per contiguous wave window) ---")
    all_tracks = []          # (track_id, wave, points array)
    wave_win = {}
    for w in sorted(WAVE_START):
        # ⚑ D-AC-1 (self-caught by the assertion below, before any number was reported).
        # d1b.track's own window test is `t0-1e-6 <= t <= t1+1e-6` — INCLUSIVE at BOTH ends —
        # so an instant landing exactly on a wave boundary is tracked in BOTH adjacent waves
        # and its plates are counted twice (16 plate-instants over the 9 internal boundaries).
        # The tracker is imported BY IDENTITY and is NOT modified; the window handed to it is
        # made half-open instead, which is a caller-side choice, not an instrument change.
        t0 = WAVE_START[w]
        t1 = WAVE_END[w] - (DT / 2.0) if w < 160 else WAVE_END[w]
        wave_win[w] = (t0, t1)
        trs = d1b.track(W, t0, t1)
        trs = sorted(trs, key=lambda x: (-len(x["p"]), x["p"][0][0]))
        for idx, tr in enumerate(trs, start=1):
            p = np.array(tr["p"], dtype=float)     # t, wx, wy, sx, sy, w
            all_tracks.append((f"W{w}-T{idx:03d}", w, p))
        print(f"  wave {w}  span {t0:7.1f}-{t1:7.1f}  tracks {len(trs):4d}  "
              f"plate-instants {sum(len(t['p']) for t in trs):6d}")
    print(f"  TOTAL tracks {len(all_tracks)}  plate-instants "
          f"{sum(len(p) for _, _, p in all_tracks)}")
    res["n_tracks"] = len(all_tracks)
    res["n_tracked_plate_instants"] = int(sum(len(p) for _, _, p in all_tracks))
    assert res["n_tracked_plate_instants"] == int(((R[:, 1] == 0)
                                                   & (R[:, 0] >= FIGHT_T0)
                                                   & (R[:, 0] <= FIGHT_T1)).sum()), \
        "HALT: tracking lost or duplicated plate instants"

    # ── THE OBSTACLE, MEASURED FIRST (prereg § 4.4 identity-continuity limit) ────────────────
    print("\n--- identity continuity of the pinned census (the obstacle, counted) ---")
    cont = plate_continuity(W, FIGHT_T0, FIGHT_T1)
    print(f"  monster plates with a successor within {cont['gate_gpx']:.0f} gpx one frame later: "
          f"{cont['n_with_successor']}/{cont['n_plates_tested']} = {cont['continuity']:.4f}")
    res["plate_continuity"] = cont

    # per-track observed arrays, cached once and reused by every rung and both join rules
    cache = {}
    for tid, w, p in all_tracks:
        ts = p[:, 0]
        keep = np.array([round(float(t), 4) in obs_set for t in ts])
        if keep.any():
            cache[tid] = (ts[keep], p[keep, 3], p[keep, 4], p[keep, 1], p[keep, 2])

    tdur = np.array([float(p[-1, 0] - p[0, 0]) for _, _, p in all_tracks])
    res["track_length_census"] = dict(
        n_tracks=len(all_tracks),
        duration_s=quantiles(list(tdur)),
        n_ge_1s=int((tdur >= 1.0).sum()), n_ge_2s=int((tdur >= 2.0).sum()),
        n_ge_4s=int((tdur >= 4.0).sum()), n_ge_8s=int((tdur >= 8.0).sum()),
        note="the tracker's identity horizon. d1b.track defaults gate=30.0 gpx, maxgap=12 "
             "instants (0.2 s). A body whose plate is undetected for more than maxgap starts a "
             "NEW track: track count is an UPPER bound on bodies, track duration a LOWER bound "
             "on body lifetime.",
    )
    print(f"  tracks {len(all_tracks)}  median duration {np.median(tdur):.4f} s  "
          f">=1 s: {(tdur>=1.0).sum()}  >=8 s: {(tdur>=8.0).sum()}  max {tdur.max():.3f} s")

    # ── FORK (b) — ring intervals at every rung, under BOTH join rules ───────────────────────
    #   rule A = GAP_JOIN_S = 0.05 s   -> THE PRE-REGISTERED FUNCTIONAL (prereg § 4.3)
    #   rule B = BRIDGE_S   = 0.2 s    -> POST-HOC SENSITIVITY, labelled as such everywhere.
    #        0.2 s is not a free parameter: it is d1b.track's own `maxgap=12` instants, the
    #        horizon beyond which the imported tracker itself refuses to assert identity.
    BRIDGE_S = 12.0 * DT
    print("\n--- FORK (b): ring intervals ---")
    rung_list = list(RING_RUNGS) + [R_CONTACT_VISUAL]
    interval_rows = []
    per_rung = {}
    per_rung_bridged = {}
    per_track_ring = {}

    def build(RC, join_s, tag):
        rows = []
        n_frames_in_ring = 0
        ptr = {}
        for tid, w, p in all_tracks:
            if tid not in cache:
                continue
            tt, sx, sy, wx, wy = cache[tid]
            pl = np.array([P[round(float(t), 4)] for t in tt])
            d = np.hypot(sx - pl[:, 0], (sy - pl[:, 1]) / K_GROUND)
            inr = d <= RC
            n_frames_in_ring += int(inr.sum())
            if not inr.any():
                continue
            idx = np.flatnonzero(inr)
            ptr[tid] = dict(track_id=tid, wave=w,
                            ring_body_time_s=round(int(inr.sum()) * DT, 4),
                            ring_span_s=round(float(tt[idx[-1]] - tt[idx[0]]), 4),
                            n_ring_frames=int(inr.sum()),
                            t_first_in_ring=round(float(tt[idx[0]]), 4),
                            t_last_in_ring=round(float(tt[idx[-1]]), 4),
                            track_duration_s=round(float(tt[-1] - tt[0]), 4))
            win0, win1 = wave_win[w]
            for (a, b, gaps) in intervals_from(inr, tt, join_s=join_s):
                t_entry, t_exit = float(tt[a]), float(tt[b])
                cl, cr, reason = False, False, []
                if a == 0:
                    cl = True
                    reason.append("wave_window_start" if float(tt[0]) <= win0 + DT * 1.5
                                  else "track_birth")
                elif (tt[a] - tt[a - 1]) >= join_s:
                    cl = True
                    reason.append("unobserved_gap_before")
                if b == len(tt) - 1:
                    cr = True
                    reason.append("wave_window_end" if float(tt[-1]) >= win1 - DT * 1.5
                                  else "track_end")
                elif (tt[b + 1] - tt[b]) >= join_s:
                    cr = True
                    reason.append("unobserved_gap_after")
                rows.append(dict(
                    track_id=tid, wave=w, R_gpx=RC, join_rule=tag,
                    t_entry=round(t_entry, 4), t_exit=round(t_exit, 4),
                    residence_s=round(t_exit - t_entry, 4),
                    body_time_s=round((b - a + 1) * DT, 4),
                    n_frames=int(b - a + 1), n_internal_gaps=int(gaps),
                    censor_left=int(cl), censor_right=int(cr),
                    censor_reason="|".join(reason) if reason else "",
                    r_at_entry=round(float(d[a]), 2), r_at_exit=round(float(d[b]), 2),
                    r_min=round(float(d[a:b + 1].min()), 2),
                    track_t_start=round(float(tt[0]), 4), track_t_end=round(float(tt[-1]), 4),
                    track_duration_s=round(float(tt[-1] - tt[0]), 4),
                    idx_entry=int(a), idx_exit=int(b), n_obs_track=int(len(tt)),
                ))
        return rows, n_frames_in_ring, ptr

    for RC in rung_list:
        rows, nfr, ptr = build(RC, GAP_JOIN_S, "A_prereg_0.05s")
        per_rung[RC] = dict(rows=rows, n_frames_in_ring=nfr)
        per_track_ring[RC] = ptr
        rows_b, nfr_b, _ = build(RC, BRIDGE_S, "B_bridged_0.2s")
        per_rung_bridged[RC] = dict(rows=rows_b, n_frames_in_ring=nfr_b)
        assert nfr == nfr_b, "HALT: join rule changed the in-ring frame count"
        interval_rows += rows + rows_b
        unc = [r["residence_s"] for r in rows if not r["censor_left"] and not r["censor_right"]]
        allr = [r["residence_s"] for r in rows]
        print(f"  R={RC:6.1f} gpx : {len(rows):5d} intervals · "
              f"median(all) {np.median(allr) if allr else float('nan'):.4f} s · "
              f"median(uncensored, n={len(unc)}) "
              f"{np.median(unc) if unc else float('nan'):.4f} s · "
              f"body-time {nfr*DT:8.2f} s  ·  bridged n={len(rows_b)}")

    # ── F-AC-1 — TRACKER FIDELITY against the pinned bracket ─────────────────────────────────
    print("\n--- F-AC-1 (tracker fidelity: my decomposition vs the PINNED occupancy) ---")
    bracket = pinned_bracket()
    fac1 = dict(window=f"[{FIGHT_T0}, {FIGHT_T1}] restricted to the {N_obs} instants with a "
                       f"detected player plate (pm4r_contact_2026_08_14.py:58)",
                functional="L_recon(RC) = sum(n_frames over intervals) / N_obs  [bodies]  vs "
                           "pinned mean_occupancy at the same RC",
                population_non_emptiness=dict(
                    require_N_obs_ge=F_AC_1_MIN_OBS, N_obs=N_obs,
                    require_intervals_at_primary_ge=F_AC_1_MIN_INTERVALS,
                    intervals_at_primary=len(per_rung[RING_PRIMARY]["rows"])),
                tolerance=F_AC_1_TOL, rungs={})
    evaluable = (N_obs >= F_AC_1_MIN_OBS
                 and len(per_rung[RING_PRIMARY]["rows"]) >= F_AC_1_MIN_INTERVALS)
    ok_all = True
    for RC in RING_RUNGS:
        L_recon = per_rung[RC]["n_frames_in_ring"] / N_obs
        L_pin = bracket[RC]["mean_occupancy"]
        rel = L_recon / L_pin - 1.0
        ok = abs(rel) <= F_AC_1_TOL
        ok_all &= ok
        fac1["rungs"][str(RC)] = dict(L_recon=round(L_recon, 6), L_pinned=L_pin,
                                      rel_dev=round(rel, 8), pass_=bool(ok))
        print(f"  R={RC:6.1f} : L_recon {L_recon:.6f}  L_pinned {L_pin:.4f}  "
              f"rel {rel:+.6f}  {'PASS' if ok else 'FAIL'}")
    fac1["verdict"] = ("UNREACHED (population non-emptiness clause)" if not evaluable
                       else ("PASS" if ok_all else "FAIL"))
    print(f"  F-AC-1 VERDICT: {fac1['verdict']}")
    res["F_AC_1"] = fac1

    # ── FORK (b) quantiles, per rung and per wave ────────────────────────────────────────────
    print("\n--- FORK (b): residence quantiles (every duration +-1 frame = +-0.0167 s) ---")
    resid = {}
    for RC in rung_list:
        rows = per_rung[RC]["rows"]
        allr = [r["residence_s"] for r in rows]
        unc = [r["residence_s"] for r in rows
               if not r["censor_left"] and not r["censor_right"]]
        bt_all = [r["body_time_s"] for r in rows]
        cens = sum(1 for r in rows if r["censor_left"] or r["censor_right"])
        entry = {
            "R_gpx": RC,
            "n_intervals": len(rows),
            "n_censored_either_side": cens,
            "censored_fraction": round(cens / len(rows), 6) if rows else None,
            "n_left_censored": sum(1 for r in rows if r["censor_left"]),
            "n_right_censored": sum(1 for r in rows if r["censor_right"]),
            "n_with_internal_gap": sum(1 for r in rows if r["n_internal_gaps"] > 0),
            "n_touching_wave_boundary": sum(
                1 for r in rows if "wave_window_start" in r["censor_reason"]
                or "wave_window_end" in r["censor_reason"]),
            "residence_all": quantiles(allr),
            "residence_uncensored_only": quantiles(unc),
            "body_time_all": quantiles(bt_all),
            "distinct_bodies_with_ring_time": len({r["track_id"] for r in rows}),
        }
        # per wave
        pw = []
        for w in sorted(WAVE_START):
            ww = [r for r in rows if r["wave"] == w]
            wobs = [t for t in obs_times if WAVE_START[w] <= t < WAVE_END[w]]
            pw.append(dict(
                wave=w, n_intervals=len(ww),
                n_distinct_bodies={r["track_id"] for r in ww}.__len__(),
                n_observed_instants=len(wobs),
                observed_fraction=round(len(wobs) / max((WAVE_END[w] - WAVE_START[w]) / DT, 1), 4),
                median_residence_s=round(float(np.median([r["residence_s"] for r in ww])), 4)
                if ww else None,
                p90_residence_s=round(float(np.percentile([r["residence_s"] for r in ww], 90)), 4)
                if ww else None,
                total_body_time_s=round(sum(r["body_time_s"] for r in ww), 3),
            ))
        entry["per_wave"] = pw
        resid[str(RC)] = entry
        q = entry["residence_all"]
        print(f"  R={RC:6.1f} : n={q['n']:5d}  median {q['median']:.4f}  p75 {q['p75']:.4f}  "
              f"p90 {q['p90']:.4f}  p95 {q['p95']:.4f}  max {q['max']:.4f}  "
              f"mean {q['mean']:.4f} s   censored {entry['censored_fraction']:.3f}")
    res["residence"] = resid

    # ── THE RESIDENCE LADDER — three nested functionals, ALL MEASURED, NONE ESTIMATED ────────
    # Under intermittent detection a single body's ring occupancy is chopped into pieces.  How
    # many pieces depends entirely on how long an unobserved gap one is willing to bridge, and
    # NO value of that parameter is decoded.  So the answer is published as a LADDER whose rungs
    # are monotone by construction and whose two ends are both measured:
    #     W_A   (join 0.05 s, PRE-REGISTERED) -- a LOWER bound: dropouts split real residences
    #     W_B   (join 0.20 s = the tracker's own maxgap, POST-HOC) -- an intermediate rung
    #     W_span(first-in-ring .. last-in-ring within a track) -- an UPPER bound: it bridges
    #            everything inside a track, INCLUDING genuine exit-and-re-entry
    # ⚑ W_B and W_span were computed AFTER seeing W_A's fragmentation.  That is stated here and
    # in the findings; neither replaces the pre-registered functional.
    print("\n--- FORK (b): THE RESIDENCE LADDER (lower / intermediate / upper, all measured) ---")
    ladder = {}
    for RC in rung_list:
        a_all = [r["residence_s"] for r in per_rung[RC]["rows"]]
        b_all = [r["residence_s"] for r in per_rung_bridged[RC]["rows"]]
        spans = [v["ring_span_s"] for v in per_track_ring[RC].values()]
        btime = [v["ring_body_time_s"] for v in per_track_ring[RC].values()]
        # the ancestor's own identity-holding sub-population (d1final.py:8 filter, >= 1.0 s)
        sp_long = [v["ring_span_s"] for v in per_track_ring[RC].values()
                   if v["track_duration_s"] >= 1.0]
        bt_long = [v["ring_body_time_s"] for v in per_track_ring[RC].values()
                   if v["track_duration_s"] >= 1.0]
        ladder[str(RC)] = dict(
            R_gpx=RC,
            rung_A_prereg_join_0p05s=quantiles(a_all),
            rung_B_bridged_join_0p20s=quantiles(b_all),
            rung_C_track_ring_span=quantiles(spans),
            per_track_ring_body_time=quantiles(btime),
            identity_held_subpopulation_track_ge_1s=dict(
                n_tracks=len(sp_long),
                ring_span=quantiles(sp_long), ring_body_time=quantiles(bt_long),
                selection="tracks whose observed lifetime >= 1.0 s — d1final.py:8's own filter, "
                          "applied here as a DECLARED SURVIVORSHIP SELECTION, not as the answer"),
            bounds_direction="rung A is a LOWER bound on per-body residence (detector dropouts "
                             "split real residences); rung C is an UPPER bound (it bridges "
                             "genuine exit-and-re-entry inside one track). The referent's "
                             "per-body ring residence lies between them AT THIS RESOLUTION.",
        )
        print(f"  R={RC:6.1f} : A median {ladder[str(RC)]['rung_A_prereg_join_0p05s']['median']:.4f} "
              f"(n={ladder[str(RC)]['rung_A_prereg_join_0p05s']['n']})  ->  "
              f"B median {ladder[str(RC)]['rung_B_bridged_join_0p20s']['median']:.4f} "
              f"(n={ladder[str(RC)]['rung_B_bridged_join_0p20s']['n']})  ->  "
              f"C median {ladder[str(RC)]['rung_C_track_ring_span']['median']:.4f} "
              f"(n={ladder[str(RC)]['rung_C_track_ring_span']['n']})")
        print(f"{'':16}A p90 {ladder[str(RC)]['rung_A_prereg_join_0p05s']['p90']:.4f}   "
              f"B p90 {ladder[str(RC)]['rung_B_bridged_join_0p20s']['p90']:.4f}   "
              f"C p90 {ladder[str(RC)]['rung_C_track_ring_span']['p90']:.4f}")
    res["residence_ladder"] = ladder

    # ── FORK (c) — exit channel at the PRIMARY rung ──────────────────────────────────────────
    print(f"\n--- FORK (c): exit channel at the PRIMARY rung R={RING_PRIMARY} ---")
    def exits_for(rows, RC, tag):
        out = []
        for r in rows:
            if r["censor_right"]:
                continue                                # exit not observed
            tid = r["track_id"]
            tt, sx, sy, wx, wy = cache[tid]
            b = r["idx_exit"]
            t_i, t_e = float(tt[b]), float(tt[b + 1])
            pi = PW[round(t_i, 4)]
            pe = PW[round(t_e, 4)]
            mi = (float(wx[b]), float(wy[b]))
            me = (float(wx[b + 1]), float(wy[b + 1]))
            r_actual = ground_dist(me[0], me[1], pe[0], pe[1])
            r_player_frozen = ground_dist(me[0], me[1], pi[0], pi[1])
            r_monster_frozen = ground_dist(mi[0], mi[1], pe[0], pe[1])
            pf_in = r_player_frozen <= RC
            mf_in = r_monster_frozen <= RC
            if mf_in and not pf_in:
                bucket = "MONSTER_SUFFICIENT"
            elif pf_in and not mf_in:
                bucket = "PLAYER_SUFFICIENT"
            elif not pf_in and not mf_in:
                bucket = "EITHER_SUFFICIENT"
            else:
                bucket = "NEITHER_SUFFICIENT"
            # ⚑ by construction censor_right == 0 implies an OBSERVED plate at t_first_out, and
            # a plate PROVES a living body (bars.py:14-15). Every exit in this table is therefore
            # a DECODED-POSITIVE alive exit at the exit instant. DEATH is never claimed here.
            continues_after = (b + 2) <= len(tt) - 1
            t_track_end = float(tt[-1])
            ends_soon = (t_track_end - t_e) <= REDETECT_WINDOW_S
            ex, ey = float(sx[b + 1]), float(sy[b + 1])
            near_edge = (ex < EDGE_MARGIN_PX or ex > FRAME_W - EDGE_MARGIN_PX
                         or ey < EDGE_MARGIN_PX or ey > FRAME_H - EDGE_MARGIN_PX)
            out.append(dict(
                track_id=tid, wave=r["wave"], R_gpx=RC, join_rule=tag,
                t_entry=r["t_entry"], t_exit_last_in=round(t_i, 4), t_first_out=round(t_e, 4),
                residence_s=r["residence_s"],
                r_actual=round(r_actual, 2),
                r_player_frozen=round(r_player_frozen, 2),
                r_monster_frozen=round(r_monster_frozen, 2),
                bucket=bucket, life_at_exit="EXIT_ALIVE",
                track_continues_after_exit=int(continues_after),
                track_end_within_1s_of_exit=int(ends_soon),
                t_track_end=round(t_track_end, 4),
                near_screen_edge_at_exit=int(near_edge),
                censor_left=r["censor_left"],
                track_duration_s=r["track_duration_s"],
            ))
        return out

    from collections import Counter
    exit_rows = exits_for(per_rung[RING_PRIMARY]["rows"], RING_PRIMARY, "A_prereg_0.05s")
    # robustness: the same partition under the bridged join and at the two other rungs.
    robust = {}
    for tag, store in (("A_prereg_0.05s", per_rung), ("B_bridged_0.2s", per_rung_bridged)):
        for RC in RING_RUNGS:
            er = exits_for(store[RC]["rows"], RC, tag)
            c2 = Counter(r["bucket"] for r in er)
            nd = c2["PLAYER_SUFFICIENT"] + c2["MONSTER_SUFFICIENT"]
            robust[f"{tag}|R{RC}"] = dict(
                n_observed_exits=len(er), counts={k: int(v) for k, v in c2.items()},
                decidable=int(nd),
                share_player=round(c2["PLAYER_SUFFICIENT"] / nd, 6) if nd else None)
    res["F_AC_2_robustness"] = robust
    print("  robustness of the partition across rungs and join rules:")
    for k in sorted(robust):
        v = robust[k]
        print(f"    {k:<26} exits {v['n_observed_exits']:4d}  decidable {v['decidable']:4d}  "
              f"share_player {v['share_player']}")
    bc = Counter(r["bucket"] for r in exit_rows)
    n_dec = bc["PLAYER_SUFFICIENT"] + bc["MONSTER_SUFFICIENT"]
    print(f"  observed exits : {len(exit_rows)}")
    for k in ("PLAYER_SUFFICIENT", "MONSTER_SUFFICIENT", "EITHER_SUFFICIENT",
              "NEITHER_SUFFICIENT"):
        print(f"    {k:<20} {bc[k]:5d}  "
              f"({bc[k]/max(len(exit_rows),1):.4f} of observed exits)")
    share_player = (bc["PLAYER_SUFFICIENT"] / n_dec) if n_dec else None
    fac2 = dict(
        window=f"all ring intervals at R={RING_PRIMARY} over [{FIGHT_T0}, {FIGHT_T1}], "
               f"observed (non-right-censored) exits only",
        functional="share_player = PLAYER_SUFFICIENT / (PLAYER_SUFFICIENT + MONSTER_SUFFICIENT); "
                   "EITHER_/NEITHER_ published separately and never folded in",
        population_non_emptiness=dict(require_decidable_ge=F_AC_2_MIN_DECIDABLE,
                                      decidable=int(n_dec)),
        counts={k: int(v) for k, v in bc.items()},
        n_observed_exits=len(exit_rows),
        share_player=round(share_player, 6) if share_player is not None else None,
        criterion=f"PASS iff share_player >= {F_AC_2_SHARE_PASS}",
    )
    if n_dec < F_AC_2_MIN_DECIDABLE:
        fac2["verdict"] = "UNREACHED (population non-emptiness clause)"
    else:
        fac2["verdict"] = "PASS" if share_player >= F_AC_2_SHARE_PASS else "FAIL"
    print(f"  share_player = {share_player}   F-AC-2 VERDICT: {fac2['verdict']}")
    res["F_AC_2"] = fac2

    # death-discriminator bound (prereg § 5.1)
    n_ends_soon = sum(r["track_end_within_1s_of_exit"] for r in exit_rows)
    n_edge = sum(r["near_screen_edge_at_exit"] for r in exit_rows)
    res["exit_life_bounds"] = dict(
        n_observed_exits=len(exit_rows),
        n_track_ends_within_1s_of_exit=int(n_ends_soon),
        frac_track_ends_within_1s=round(n_ends_soon / max(len(exit_rows), 1), 6),
        n_near_screen_edge_at_exit=int(n_edge),
        note="every observed exit is EXIT_ALIVE at the exit instant BY CONSTRUCTION (a "
             "non-right-censored exit requires an observed plate at t_first_out, and a plate "
             "proves a living body). The alive/dead question therefore attaches to the TRACK's "
             "own end, not to the exit; DEATH is never claimed, only DEATH-CANDIDATE.",
    )

    # right-censored intervals = the exits we could NOT observe; these carry the death signal
    rc_rows = [r for r in per_rung[RING_PRIMARY]["rows"] if r["censor_right"]]
    rc_reasons = Counter(
        ("track_end" if "track_end" in r["censor_reason"] else
         "wave_window_end" if "wave_window_end" in r["censor_reason"] else
         "unobserved_gap_after")
        for r in rc_rows)
    res["right_censored_exits"] = dict(
        n=len(rc_rows), by_reason={k: int(v) for k, v in rc_reasons.items()},
        note="a ring interval ending because the TRACK ends (plate gone, never re-associated) "
             "is a DEATH-CANDIDATE: corpses carry no nameplate (Lap H-2 OBS-H2-1), but plate "
             "loss is equally consistent with occlusion, plate suppression, screen exit or a "
             "tracker identity break. DEATH IS NOT CLAIMED.",
    )
    print(f"  right-censored (unobserved) exits: {len(rc_rows)}  {dict(rc_reasons)}")

    # player ground speed at exits vs fight-wide (context, never a substitute)
    ct = cam[:, 0]
    spd = np.hypot(cam[:, 1], cam[:, 2] / K_GROUND) * FPS
    k = np.ones(SMOOTH_FRAMES) / SMOOTH_FRAMES
    spd_s = np.convolve(spd, k, mode="same")
    at_exit = []
    for r in exit_rows:
        m = (ct >= r["t_first_out"] - EXIT_SPEED_HALFWIN_S) & \
            (ct <= r["t_first_out"] + EXIT_SPEED_HALFWIN_S)
        if m.any():
            at_exit.append(float(spd_s[m].mean()))
    mfw = (ct >= FIGHT_T0) & (ct <= FIGHT_T1)
    res["player_speed_context"] = dict(
        units="ground px/s (NOT converted to m/s; the metre anchor is Lap H-2's DECLARED GAP "
              "OBS-H2-9 and is carried as a bracket, never a scalar)",
        at_exits=quantiles(at_exit),
        fight_wide=quantiles(list(spd_s[mfw])),
        halfwin_s=EXIT_SPEED_HALFWIN_S, smooth_frames=SMOOTH_FRAMES,
    )
    print(f"  player smoothed ground speed (gpx/s): at exits median "
          f"{res['player_speed_context']['at_exits'].get('median')}  vs fight-wide median "
          f"{res['player_speed_context']['fight_wide'].get('median')}")

    # ── LEG A-3 — emplacement signature in the RED population ────────────────────────────────
    print("\n--- leg A-3: world-stationary long-lived RED tracks (CORROBORATIVE only) ---")
    trk_rows = []
    for tid, w, p in all_tracks:
        t = p[:, 0]
        wx, wy = p[:, 1], p[:, 2]
        dur = float(t[-1] - t[0])
        net = ground_dist(wx[-1], wy[-1], wx[0], wy[0])
        step = np.hypot(np.diff(wx), np.diff(wy) / K_GROUND)
        path = float(step.sum())
        rad = float(np.hypot(wx - wx.mean(), (wy - wy.mean()) / K_GROUND).max())
        trk_rows.append(dict(
            track_id=tid, wave=w, t_start=round(float(t[0]), 4), t_end=round(float(t[-1]), 4),
            duration_s=round(dur, 4), n_frames=int(len(t)),
            net_world_disp_gpx=round(net, 2), path_world_gpx=round(path, 1),
            max_radius_about_mean_gpx=round(rad, 2),
            stationary_candidate=int(dur >= STATIONARY_MIN_S and net <= STATIONARY_NET_GPX),
        ))
    cand = [r for r in trk_rows if r["stationary_candidate"]]
    # ⚑ POPULATION NON-EMPTINESS (R-PM4-72 part 4 / D-I27-2): a zero here is only a measurement
    # if the DURATION half of the predicate has a non-empty population to test.  Both halves are
    # reported separately so this row cannot be green (or red) by construction.
    long_enough = [r for r in trk_rows if r["duration_s"] >= STATIONARY_MIN_S]
    still_enough = [r for r in trk_rows if r["net_world_disp_gpx"] <= STATIONARY_NET_GPX]
    min_net_among_long = (min(r["net_world_disp_gpx"] for r in long_enough)
                          if long_enough else None)
    max_dur_among_still = (max(r["duration_s"] for r in still_enough)
                           if still_enough else None)
    print(f"  tracks {len(trk_rows)}   stationary candidates "
          f"(dur >= {STATIONARY_MIN_S} s and net <= {STATIONARY_NET_GPX} gpx): {len(cand)}")
    print(f"  population non-emptiness: tracks with dur >= {STATIONARY_MIN_S} s = "
          f"{len(long_enough)} (min net disp among them {min_net_among_long} gpx); "
          f"tracks with net <= {STATIONARY_NET_GPX} gpx = {len(still_enough)} "
          f"(max duration among them {max_dur_among_still} s)")
    for r in sorted(cand, key=lambda z: -z["duration_s"])[:12]:
        print(f"    {r['track_id']:<11} w{r['wave']} {r['t_start']:8.2f}-{r['t_end']:8.2f} "
              f"dur {r['duration_s']:6.2f} s  net {r['net_world_disp_gpx']:7.2f} gpx  "
              f"path {r['path_world_gpx']:8.1f} gpx  maxrad {r['max_radius_about_mean_gpx']:7.2f}")
    res["leg_A3"] = dict(
        thresholds=dict(STATIONARY_NET_GPX=STATIONARY_NET_GPX,
                        STATIONARY_MIN_S=STATIONARY_MIN_S),
        n_tracks=len(trk_rows), n_candidates=len(cand),
        population_non_emptiness=dict(
            n_tracks_duration_ge_threshold=len(long_enough),
            min_net_world_disp_among_them_gpx=min_net_among_long,
            n_tracks_net_le_threshold=len(still_enough),
            max_duration_among_them_s=max_dur_among_still,
            note="both halves of the conjunctive predicate are reported over their own "
                 "populations so a zero cannot be green-by-absence (D-I27-2's lesson)."),
        candidates=[dict(track_id=r["track_id"], wave=r["wave"], duration_s=r["duration_s"],
                         net_world_disp_gpx=r["net_world_disp_gpx"],
                         path_world_gpx=r["path_world_gpx"]) for r in
                    sorted(cand, key=lambda z: -z["duration_s"])[:40]],
        grade="CORROBORATIVE, never dispositive (prereg § 3.4): a world-stationary red track is "
              "consistent with an emplacement AND with a monster that does not move; the world "
              "frame is a cumulative camera sum whose drift is validated only locally, so this "
              "leg is scoped WITHIN a wave.",
    )

    # ── LEG A-3b — THE MOBILE-PET SIGNATURE IN THE RED POPULATION ────────────────────────────
    # Declared POST-HOC (after leg A-3's stationary census returned zero and after D-AC-2/D-AC-3
    # removed the green channel as a discriminator).  Leg A-3 can only see FIXED emplacements.
    # The referent's kit also carries MOBILE summons — Lap G § 115-116: `summon_celestialguardian1`
    # (petLimit 2) and `itemskillsgdx1/relics/summondeathstalker` (petLimit 1), i.e. AT MOST THREE
    # concurrent player pets.  A red-plated pet follows its owner, so it would appear as a
    # long-lived track spending most of its life inside the melee ring.
    #   BOUND, not identification: this leg can produce a measured NEGATIVE (no such track) or a
    #   CANDIDATE SET.  Pixels cannot name a body, so it may never say "this track IS a pet".
    print("\n--- leg A-3b: mobile-pet signature (long-lived tracks resident at the ring) ---")
    PET_MIN_DUR_S = 4.0
    ptr = per_track_ring[RING_PRIMARY]
    long_tracks = [(tid, w, p) for tid, w, p in all_tracks
                   if float(p[-1, 0] - p[0, 0]) >= PET_MIN_DUR_S]
    a3b = []
    for tid, w, p in long_tracks:
        dur = float(p[-1, 0] - p[0, 0])
        rb = ptr.get(tid, {}).get("ring_body_time_s", 0.0)
        a3b.append(dict(track_id=tid, wave=w, duration_s=round(dur, 3),
                        ring_body_time_s=round(rb, 3),
                        ring_fraction=round(rb / dur, 4) if dur > 0 else None))
    a3b.sort(key=lambda r: -(r["ring_fraction"] or 0))
    n_hi = sum(1 for r in a3b if (r["ring_fraction"] or 0) >= 0.5)
    print(f"  tracks with duration >= {PET_MIN_DUR_S} s : {len(a3b)}  (population non-empty)")
    print(f"  of those, ring_fraction >= 0.50 : {n_hi}")
    print(f"  top 8 by ring fraction:")
    for r in a3b[:8]:
        print(f"    {r['track_id']:<11} w{r['wave']} dur {r['duration_s']:6.2f} s  "
              f"ring {r['ring_body_time_s']:6.2f} s  frac {r['ring_fraction']:.4f}")
    res["leg_A3b"] = dict(
        declared_post_hoc=True,
        rationale="leg A-3 can only see FIXED emplacements; the referent kit also carries at "
                  "most THREE concurrent MOBILE pets (Lap G § 115-116). A red-plated pet would "
                  "be a long-lived track resident at the ring.",
        min_duration_s=PET_MIN_DUR_S, R_gpx=RING_PRIMARY,
        population_non_emptiness=dict(n_tracks_ge_min_duration=len(a3b)),
        n_with_ring_fraction_ge_0p5=int(n_hi),
        max_ring_fraction=a3b[0]["ring_fraction"] if a3b else None,
        top_candidates=a3b[:20],
        grade="BOUND, never identification — pixels cannot name a body (NOTE-9).",
    )

    # ── EMIT ─────────────────────────────────────────────────────────────────────────────────
    icols = ["track_id", "wave", "R_gpx", "join_rule", "t_entry", "t_exit", "residence_s",
             "body_time_s", "n_frames", "n_internal_gaps", "censor_left", "censor_right",
             "censor_reason", "r_at_entry", "r_at_exit", "r_min", "track_t_start",
             "track_t_end", "track_duration_s", "n_obs_track"]
    d1, n1 = dump_csv(OUT / "pm4ac_ring_intervals.csv", interval_rows, icols)
    ecols = ["track_id", "wave", "R_gpx", "join_rule", "t_entry", "t_exit_last_in",
             "t_first_out", "residence_s", "r_actual", "r_player_frozen", "r_monster_frozen",
             "bucket", "life_at_exit", "track_continues_after_exit",
             "track_end_within_1s_of_exit", "t_track_end", "near_screen_edge_at_exit",
             "censor_left", "track_duration_s"]
    d2_, n2 = dump_csv(OUT / "pm4ac_ring_exits.csv", exit_rows, ecols)
    tcols = ["track_id", "wave", "t_start", "t_end", "duration_s", "n_frames",
             "net_world_disp_gpx", "path_world_gpx", "max_radius_about_mean_gpx",
             "stationary_candidate"]
    d3, n3 = dump_csv(OUT / "pm4ac_tracks.csv", trk_rows, tcols)
    res["emitted"] = {
        "pm4ac_ring_intervals.csv": dict(sha256=d1, rows=n1),
        "pm4ac_ring_exits.csv": dict(sha256=d2_, rows=n2),
        "pm4ac_tracks.csv": dict(sha256=d3, rows=n3),
    }
    print(f"\n  pm4ac_ring_intervals.csv  rows={n1}  sha256={d1}")
    print(f"  pm4ac_ring_exits.csv      rows={n2}  sha256={d2_}")
    print(f"  pm4ac_tracks.csv          rows={n3}  sha256={d3}")

    p = OUT / "pm4ac_residence.json"
    p.write_text(json.dumps(res, indent=2, sort_keys=True, default=str))
    print(f"  pm4ac_residence.json      sha256={sha256(p)}")


if __name__ == "__main__":
    main()
