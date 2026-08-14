#!/usr/bin/env python3
"""KC2-PM4 Lap S — THE VIDEO-GEOMETRY LIMB (b) + the wave-advance falsification arm of limb (c).

MEASURED QUANTITIES
  (b1) FIRST-APPEARANCE RADIUS.  A nameplate track's BIRTH radius from the player, in ground px
       and in metres at BOTH edges of the R-PM4-43 bracket [119.0, 125.0] gpx/m.
  (b2) FRUSTUM LIMIT.  The maximum ground radius the referent's camera can contain at all, both
       geometric (screen box) and empirical (observed plate extent).
  (b3) ARENA BOUNDS.  Hull of the integrated player trajectory and of the entity cloud.
  (b4) ARRIVAL CURVES.  Living-plate count vs time since each wave increment.
  (c1) WAVE-ADVANCE FALSIFICATION.  Minimum living-plate count in a window ENDING at each wave
       increment.  A plate PROVES a living body, so `min >= 1` PROVES the board was never empty.

BOUND DIRECTIONS (pre-registered, § 3.0 of PREREGISTRATION.md)
  * plate absence does NOT prove body absence  ->  counts are LOWER bounds
  * nameplates render only inside the frustum  ->  first-appearance radius is RIGHT-CENSORED,
    i.e. a LOWER bound on the body's true spawn distance
  * the integrated trajectory is subject to INTEGRATION DRIFT over 11,024 frames.  Drift INFLATES
    apparent extent, so the trajectory hull is NOT a lower bound and is graded INDICATIVE.  This
    is a self-caught correction against the pre-registration's § 3.0 third bullet; see findings.

READ-ONLY.  OUTCOME-FIREWALLED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap S.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import sys

import numpy as np

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
NOTES = META / "agentic_orchestration" / "legolas" / "notes"
LAPH2 = NOTES / "2026-08-13-kc2-pm4-lap-h2-video-match"
LAPR = NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact"
OUT = NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance"

PLATES = LAPR / "method" / "plates60_lapH2.npy"
CAM = LAPH2 / "method" / "camera_translation_60fps_683-866.npy"
PINNED = {
    str(PLATES): "28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df",
    str(CAM): "029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33",
}

# ── carried constants, each with its emitting lap named (NOTE-9) ─────────────────────────────
K_GROUND = 0.537                      # OBS-H2-8 isometric ground compression
PLAYER_PLATE_ANCHOR = (960.0, 429.0)  # Lap R's own gate, reused unchanged
PLAYER_GATE = (50.0, 16.0)
FIGHT_T0, FIGHT_T1 = 683.0, 864.0
WAVE_START = {151: 683.0, 152: 698.6, 153: 714.9, 154: 729.8, 155: 744.0,
              156: 760.2, 157: 780.4, 158: 799.7, 159: 812.7, 160: 839.0}
WAVE_END = {w: (WAVE_START[w + 1] if w < 160 else FIGHT_T1) for w in WAVE_START}
SCREEN = (1920.0, 1080.0)

# ── PRE-REGISTERED thresholds (PREREGISTRATION.md § 3.1, § 4.1) ──────────────────────────────
G_MAX_PRIMARY, G_MAX_SWEEP = 60.0, (40.0, 60.0, 90.0)
N_MIN_PRIMARY, N_MIN_SWEEP = 6, (3, 6, 12)
H_GAP_PRIMARY, H_GAP_SWEEP = 6, (3, 6, 12)
PXM_LO, PXM_HI = 119.0, 125.0          # R-PM4-43 part 2 bracket.  BOTH EDGES ALWAYS.
DELTA_PRIMARY, DELTA_SWEEP = 3.0, (1.0, 3.0, 5.0)
SIM_SPAWN_RADIUS_M = 45.06             # the commission's comparator.  Never an input.
FPS = 60.0
FRAME_DT = 1.0 / FPS


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wave_of(t: float):
    for w in sorted(WAVE_START, reverse=True):
        if t >= WAVE_START[w]:
            return w
    return None


# ══════════════════════════════════════════════════════════════════════════════════════════════
def load_frames():
    """-> (times, player_xy per time, list of monster (x,y) per time)."""
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
    return times, P, M


def offsets(times, P, M):
    """Player-relative GROUND offsets per instant: (dx, dy/K)."""
    out = []
    for t in times:
        px, py = P[t]
        out.append(np.array([[x - px, (y - py) / K_GROUND] for x, y in M.get(t, ())],
                            dtype=np.float64).reshape(-1, 2))
    return out


def track(times, offs, g_max, n_min, h_gap):
    """Greedy nearest-neighbour association in the player-relative ground frame.

    A track carries (birth_index, last_index, last_xy, n_frames).  Association is one-to-one and
    greedy on ascending distance; unmatched detections open new tracks; tracks unmatched for more
    than `h_gap` frames close.  Returns closed tracks meeting `n_min`.
    """
    live, done = [], []
    for i, pts in enumerate(offs):
        used = set()
        pairs = []
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
        for j in range(len(pts)):
            if j in used:
                continue
            live.append(dict(birth=i, last=i, n=1, xy=tuple(pts[j]),
                             r0=float(np.hypot(*pts[j])),
                             rmin=float(np.hypot(*pts[j]))))
        keep = []
        for tr in live:
            if i - tr["last"] > h_gap:
                done.append(tr)
            else:
                keep.append(tr)
        live = keep
    done.extend(live)
    return [t for t in done if t["n"] >= n_min]


# ══════════════════════════════════════════════════════════════════════════════════════════════
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 100)
    print("KC2-PM4 LAP S — VIDEO GEOMETRY (limb b) + WAVE-ADVANCE FALSIFICATION (limb c video arm)")
    print("=" * 100)
    for p, want in PINNED.items():
        got = sha256(p)
        assert got == want, f"HALT (GL-6): {p} digest {got} != {want}"
        print(f"  EXACT  {got}  {pathlib.Path(p).name}")

    times, P, M = load_frames()
    offs = offsets(times, P, M)
    ta = np.asarray(times)
    counts = np.array([len(o) for o in offs], dtype=np.int32)
    print(f"\n  instants with a detected player plate in {FIGHT_T0}-{FIGHT_T1} s : {len(times)}")
    print(f"  living monster plates in those instants                     : {int(counts.sum())}")

    res = {"pinned": {k: sha256(k) for k in PINNED}, "n_instants": len(times),
           "px_per_m_bracket": [PXM_LO, PXM_HI], "sim_spawn_radius_m": SIM_SPAWN_RADIUS_M}

    # ── (b2) FRUSTUM LIMIT ───────────────────────────────────────────────────────────────────
    ax, ay = PLAYER_PLATE_ANCHOR
    geo = {"left_gpx": ax, "right_gpx": SCREEN[0] - ax,
           "up_gpx": ay / K_GROUND, "down_gpx": (SCREEN[1] - ay) / K_GROUND}
    geo["min_gpx"] = min(geo.values())
    allo = np.vstack([o for o in offs if len(o)])
    emp = {"max_abs_dx_gpx": float(np.abs(allo[:, 0]).max()),
           "max_abs_dy_gpx": float(np.abs(allo[:, 1]).max()),
           "max_radius_gpx": float(np.hypot(allo[:, 0], allo[:, 1]).max()),
           "p99_radius_gpx": float(np.percentile(np.hypot(allo[:, 0], allo[:, 1]), 99))}
    print("\n  ── (b2) FRUSTUM LIMIT ──")
    print(f"    geometric, from the player plate anchor {PLAYER_PLATE_ANCHOR} on {SCREEN}:")
    for k, v in geo.items():
        print(f"       {k:16s} {v:8.1f} gpx   = {v/PXM_HI:6.2f} m (HI edge) .. {v/PXM_LO:6.2f} m (LO edge)")
    print(f"    empirical, over {len(allo)} observed monster plates:")
    for k, v in emp.items():
        print(f"       {k:20s} {v:8.1f} gpx   = {v/PXM_HI:6.2f} m .. {v/PXM_LO:6.2f} m")
    res["frustum_geometric_gpx"] = geo
    res["frustum_empirical_gpx"] = emp
    res["frustum_min_m"] = {"lo_edge_119": geo["min_gpx"] / PXM_LO, "hi_edge_125": geo["min_gpx"] / PXM_HI}
    res["frustum_max_observed_m"] = {"lo_edge_119": emp["max_radius_gpx"] / PXM_LO,
                                     "hi_edge_125": emp["max_radius_gpx"] / PXM_HI}

    # ── (b1) FIRST APPEARANCE — primary + sweep ──────────────────────────────────────────────
    print("\n  ── (b1) FIRST-APPEARANCE RADIUS ──")
    sweep_rows, primary_tracks = [], None
    for gm in G_MAX_SWEEP:
        for nm in N_MIN_SWEEP:
            for hg in H_GAP_SWEEP:
                trs = track(times, offs, gm, nm, hg)
                r0 = np.array([t["r0"] for t in trs])
                row = dict(G_MAX=gm, N_MIN=nm, H_GAP=hg, n_tracks=len(trs),
                           r0_median_gpx=round(float(np.median(r0)), 2),
                           r0_p95_gpx=round(float(np.percentile(r0, 95)), 2),
                           r0_max_gpx=round(float(r0.max()), 2),
                           r0_p95_m_lo=round(float(np.percentile(r0, 95)) / PXM_LO, 3),
                           r0_p95_m_hi=round(float(np.percentile(r0, 95)) / PXM_HI, 3),
                           primary=(gm == G_MAX_PRIMARY and nm == N_MIN_PRIMARY
                                    and hg == H_GAP_PRIMARY))
                sweep_rows.append(row)
                if row["primary"]:
                    primary_tracks = trs
                print(f"    G_MAX={gm:5.0f} N_MIN={nm:3d} H_GAP={hg:3d} -> {len(trs):5d} tracks  "
                      f"birth-r median {row['r0_median_gpx']:7.1f} gpx  p95 {row['r0_p95_gpx']:7.1f} gpx "
                      f"= {row['r0_p95_m_lo']:5.2f}-{row['r0_p95_m_hi']:5.2f} m"
                      f"{'   <-- PRIMARY' if row['primary'] else ''}")
    res["first_appearance_sweep"] = sweep_rows

    # per-track emission at PRIMARY
    with open(OUT / "pm4s_first_appearance.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["track_id", "wave", "t_birth_s", "t_last_s", "n_frames",
                    "r_birth_gpx", "r_birth_m_lo119", "r_birth_m_hi125",
                    "r_min_gpx", "r_min_m_lo119", "r_min_m_hi125",
                    "at_frustum_boundary", "G_MAX", "N_MIN", "H_GAP", "basis"])
        bnd = 0.95 * geo["min_gpx"]
        for i, tr in enumerate(sorted(primary_tracks, key=lambda x: x["birth"])):
            tb, tl = float(ta[tr["birth"]]), float(ta[tr["last"]])
            atb = int(tr["r0"] >= bnd)
            bnd_hit = atb
            w.writerow([f"T{i+1:05d}", wave_of(tb), round(tb, 4), round(tl, 4), tr["n"],
                        round(tr["r0"], 2), round(tr["r0"] / PXM_LO, 4), round(tr["r0"] / PXM_HI, 4),
                        round(tr["rmin"], 2), round(tr["rmin"] / PXM_LO, 4),
                        round(tr["rmin"] / PXM_HI, 4), bnd_hit,
                        G_MAX_PRIMARY, N_MIN_PRIMARY, H_GAP_PRIMARY,
                        "Lap H-2 nameplate census, player-relative ground offsets"])
    r0p = np.array([t["r0"] for t in primary_tracks])
    res["first_appearance_primary"] = dict(
        n_tracks=len(primary_tracks),
        median_gpx=round(float(np.median(r0p)), 2),
        p95_gpx=round(float(np.percentile(r0p, 95)), 2), max_gpx=round(float(r0p.max()), 2),
        median_m=[round(float(np.median(r0p)) / PXM_LO, 3), round(float(np.median(r0p)) / PXM_HI, 3)],
        p95_m=[round(float(np.percentile(r0p, 95)) / PXM_LO, 3),
               round(float(np.percentile(r0p, 95)) / PXM_HI, 3)],
        max_m=[round(float(r0p.max()) / PXM_LO, 3), round(float(r0p.max()) / PXM_HI, 3)],
        frac_at_frustum_boundary=round(float((r0p >= 0.95 * geo["min_gpx"]).mean()), 4))
    fa = res["first_appearance_primary"]
    print(f"\n    PRIMARY: {fa['n_tracks']} tracks; birth radius median {fa['median_gpx']} gpx "
          f"= {fa['median_m'][1]}-{fa['median_m'][0]} m;  p95 = {fa['p95_m'][1]}-{fa['p95_m'][0]} m; "
          f"MAX = {fa['max_m'][1]}-{fa['max_m'][0]} m")
    print(f"    fraction of births at >=95 % of the frustum limit: {fa['frac_at_frustum_boundary']}")

    # ── (b3) ARENA BOUNDS ────────────────────────────────────────────────────────────────────
    print("\n  ── (b3) ARENA BOUNDS (integrated; see drift caveat) ──")
    cam = np.load(CAM)
    m = (cam[:, 0] >= FIGHT_T0) & (cam[:, 0] <= FIGHT_T1)
    d = cam[m]
    arena_rows = []
    for sign, label in ((-1.0, "player=-cumsum(camera)"), (+1.0, "player=+cumsum(camera)")):
        X = sign * np.cumsum(d[:, 1])
        Y = sign * np.cumsum(d[:, 2]) / K_GROUND
        pl_w, pl_h = float(X.max() - X.min()), float(Y.max() - Y.min())
        pl_diam = float(np.hypot(pl_w, pl_h))
        # entity hull: nearest camera sample to each plate instant
        idx = np.clip(np.searchsorted(d[:, 0], ta), 0, len(d) - 1)
        ex, ey = [], []
        for k, o in enumerate(offs):
            if not len(o):
                continue
            ex.append(X[idx[k]] + o[:, 0])
            ey.append(Y[idx[k]] + o[:, 1])
        EX, EY = np.concatenate(ex), np.concatenate(ey)
        en_w, en_h = float(EX.max() - EX.min()), float(EY.max() - EY.min())
        en_diam = float(np.hypot(en_w, en_h))
        arena_rows.append(dict(convention=label, player_w_gpx=pl_w, player_h_gpx=pl_h,
                               player_diag_gpx=pl_diam, entity_w_gpx=en_w, entity_h_gpx=en_h,
                               entity_diag_gpx=en_diam))
        print(f"    {label:26s} player box {pl_w:7.0f} x {pl_h:7.0f} gpx  diag {pl_diam:7.0f} "
              f"= {pl_diam/PXM_HI:6.2f}-{pl_diam/PXM_LO:6.2f} m")
        print(f"    {'':26s} entity box {en_w:7.0f} x {en_h:7.0f} gpx  diag {en_diam:7.0f} "
              f"= {en_diam/PXM_HI:6.2f}-{en_diam/PXM_LO:6.2f} m")
    # the conservative reading: the SMALLER of the two sign conventions
    cons = min(arena_rows, key=lambda r: r["entity_diag_gpx"])
    res["arena"] = dict(rows=arena_rows, conservative_convention=cons["convention"],
                        entity_diag_gpx=cons["entity_diag_gpx"],
                        entity_diag_m=[cons["entity_diag_gpx"] / PXM_LO,
                                       cons["entity_diag_gpx"] / PXM_HI],
                        player_diag_m=[cons["player_diag_gpx"] / PXM_LO,
                                       cons["player_diag_gpx"] / PXM_HI],
                        grade="INDICATIVE — integrated trajectory, drift INFLATES extent; "
                              "NOT a lower bound.  Self-caught departure from PREREG § 3.0.")
    with open(OUT / "pm4s_arena_bounds.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "convention", "value_gpx", "value_m_lo119", "value_m_hi125",
                    "grade", "basis"])
        for r in arena_rows:
            for q in ("player_diag_gpx", "entity_diag_gpx", "player_w_gpx", "player_h_gpx",
                      "entity_w_gpx", "entity_h_gpx"):
                w.writerow([q, r["convention"], round(r[q], 2), round(r[q] / PXM_LO, 4),
                            round(r[q] / PXM_HI, 4), "INDICATIVE",
                            "cumsum of Lap H-2 camera_translation_60fps; integration drift INFLATES"])
        for k, v in geo.items():
            w.writerow([f"frustum_geometric_{k}", "n/a", round(v, 2), round(v / PXM_LO, 4),
                        round(v / PXM_HI, 4), "MEASURED",
                        f"screen {SCREEN}, player plate anchor {PLAYER_PLATE_ANCHOR}, K={K_GROUND}"])
        for k, v in emp.items():
            w.writerow([f"frustum_empirical_{k}", "n/a", round(v, 2), round(v / PXM_LO, 4),
                        round(v / PXM_HI, 4), "MEASURED",
                        "observed extent of 98,794 monster nameplates, player-relative ground frame"])

    # ── (b4) ARRIVAL CURVES ──────────────────────────────────────────────────────────────────
    print("\n  ── (b4) PER-WAVE ARRIVAL ──")
    arr = {}
    for wv in sorted(WAVE_START):
        t0, t1 = WAVE_START[wv], WAVE_END[wv]
        sel = (ta >= t0) & (ta < t1)
        c = counts[sel]
        tt = ta[sel] - t0
        peak = int(c.max()) if len(c) else 0
        def first_at(frac):
            hit = np.where(c >= frac * peak)[0]
            return round(float(tt[hit[0]]), 3) if len(hit) else None
        arr[wv] = dict(span_s=round(t1 - t0, 3), peak_plates=peak,
                       t_peak_s=round(float(tt[int(np.argmax(c))]), 3) if len(c) else None,
                       t_to_50pct_peak_s=first_at(0.5), t_to_90pct_peak_s=first_at(0.9),
                       mean_plates=round(float(c.mean()), 3), min_plates=int(c.min()),
                       plates_at_t0=int(c[0]))
        a = arr[wv]
        print(f"    w{wv}  span {a['span_s']:6.2f} s  peak {a['peak_plates']:3d} @ {a['t_peak_s']:6.3f} s  "
              f"t->50%% {a['t_to_50pct_peak_s']}  t->90%% {a['t_to_90pct_peak_s']}  "
              f"min {a['min_plates']}  at-increment {a['plates_at_t0']}")
    res["arrival"] = arr

    # ── (c1) WAVE-ADVANCE FALSIFICATION ──────────────────────────────────────────────────────
    print("\n  ── (c1) WAVE-ADVANCE FALSIFICATION ──")
    print("    rule (pre-registered): a plate PROVES a living body, so min-count >= 1 over the")
    print("    window ENDING at the increment PROVES the board was never empty there.")
    adv = {}
    for delta in DELTA_SWEEP:
        rows = []
        for wv in sorted(WAVE_START):
            if wv == 151:
                continue                       # 151 is the run start, no preceding wave in frame
            t_inc = WAVE_START[wv]
            sel = (ta >= t_inc - delta) & (ta <= t_inc)
            c = counts[sel]
            rows.append(dict(wave=wv, t_inc=t_inc, n_frames=int(sel.sum()),
                             min_plates=int(c.min()) if len(c) else None,
                             mean_plates=round(float(c.mean()), 2) if len(c) else None))
        allpos = all(r["min_plates"] is not None and r["min_plates"] >= 1 for r in rows)
        adv[delta] = dict(rows=rows, all_windows_nonempty=allpos)
        tag = "  <-- PRIMARY" if delta == DELTA_PRIMARY else ""
        print(f"    Delta = {delta:4.1f} s : min plate count per increment "
              f"{[r['min_plates'] for r in rows]}  -> board never empty in ALL windows: "
              f"{allpos}{tag}")
    gmin = int(counts.min())
    nzero = int((counts == 0).sum())
    print(f"\n    GLOBAL over the whole fight {FIGHT_T0}-{FIGHT_T1} s: min plate count = {gmin}; "
          f"instants with ZERO living plates = {nzero}/{len(counts)} "
          f"({nzero/len(counts):.4%}) = {nzero*FRAME_DT:.2f} s")
    res["wave_advance"] = {str(k): v for k, v in adv.items()}
    res["global_min_plate_count"] = gmin
    res["global_zero_plate_instants"] = nzero
    res["global_zero_plate_seconds"] = round(nzero * FRAME_DT, 3)

    with open(OUT / "pm4s_video.json", "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=float)
    print(f"\n  wrote {OUT/'pm4s_first_appearance.csv'}")
    print(f"  wrote {OUT/'pm4s_arena_bounds.csv'}")
    print(f"  wrote {OUT/'pm4s_video.json'}")


if __name__ == "__main__":
    sys.exit(main())
