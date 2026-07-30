#!/usr/bin/env python3
"""
WR2-ENCGEO-2026-07-29 / F-WR2-5 pursuit diagnostic — READ-ONLY instrument.

Decomposes "the boss is pinned to the player" into its SPEED half and its AI half, measured
from the banked AFTER traces. NO simulation runs, NO writes into src/.

Lives outside src/ executed paths (gamora notes support dir) per the battery-instrument
precedent (wr1_envelope_spec_support/).

────────────────────────────────────────────────────────────────────────────────
§0. VALIDATION GATES (Discipline #11/#12) — run FIRST, before any new number is trusted.

  V1  watch-seed footer: pre / boss/B / seed 74000802 -> elapsed_s == 37.0
  V2  pre-leg elapsed_s means: boss/A == 32.04, boss/B == 48.92 (battery-of-record §4.2)
  V3  S-1 over all 450 AFTER traces: pair_samples == 292305, violations == 0,
      worst_slack_m == -0.000989...  (reimplemented from the cell-B predicate, §S1 below)
  V4  nova firings: 132 total (44 per leg), attack_id containing ":nova:"

If any gate fails the instrument aborts. The new metrics are only emitted on a clean sweep.

────────────────────────────────────────────────────────────────────────────────
§1. JOIN FACTS (inherited from Cell BAT WARN-4, MIGRATION §6)

  - header record (`record_type: "header"`) carries `entities[]` with `entity_id`,
    `is_player`, `entity_radius_m`, `movement_speed_ms`, `skills[]`.
  - the g5 header (`record_type: "g5_header"`) carries `g5.opposition_roster[]`; the BOSS is
    the roster entry with `tier == "boss"`, joined to an entity_id by
    `entity_id.startswith(record.replace("/", "_"))`. Tick records do NOT carry `is_player`
    or `is_boss` — the join must go through the header.
  - tick records (`record_type: "tick"`) carry per-entity `x_m`, `y_m`, `heading_rad`,
    `alive`, `commit_state`, `commit_skill_idx`, `ailments`.
  - telegraph events: `record_type: "event"`, `event: "telegraph"`, with `attack_id`,
    `attacker_id`, `fire_tick`, `wind_up_s`, `shape`, `radius_m`, `origin_{x,y}_m`.
    The nova filter is `":nova:" in attack_id` (Cell BAT WARN-4 completeness-checked).

────────────────────────────────────────────────────────────────────────────────
§2. MEASURES

Let the emitted tick sequence be k = 0..N-1 with times t_k, boss centres b_k, player
centres p_k. Steps are indexed by k -> k+1 and only formed where BOTH ticks have the boss
and the player alive.

  dt_k    = t_{k+1} - t_k
  s_k     = |b_{k+1} - b_k|                       boss realized displacement (m)
  cap_k   = v_boss * dt_k                         the per-tick displacement CAP
  u_k     = s_k / cap_k                           SPEED UTILIZATION, dimensionless
  moving  = s_k > MOVE_EPS (1e-9 m)

  The engine's mob law (spatial_engine._navigate_entity, read-only reference):
      d = |target - b_k| ; speed = v_boss*dt ; factor = min(speed/d, 1.0)
      b_{k+1} = b_k + (target - b_k) * factor
  so u_k == 1.0 EXCEPT on the arrival tick (where the boss would overshoot the target and
  instead lands exactly on it), on a leash/fear/hard-CC early return (s_k == 0), and after
  the body-separation solver / arena clamp perturb the landing point.

  HEADING PURITY. Two candidate reference directions, because the answer depends on the
  intra-tick phase order (mob-navigate vs player-move) and I refuse to assume it:
      theta_pre_k  = angle( b_{k+1}-b_k , p_k   - b_k )   player position BEFORE the step
      theta_post_k = angle( b_{k+1}-b_k , p_{k+1} - b_k )  player position AFTER the step
  Both in degrees on [0,180]. Whichever concentrates at 0 identifies the read. A turn-rate
  limit, an acceleration ramp, or a lead/lag would all show as a fat right tail.

  SEPARATION. d_k = |b_k - p_k|. Contact geometry on this fixture:
      C_body  = r_boss + r_player = 1.5 + 0.5 = 2.0 m      the S-1 floor (bodies touching)
      C_reach = boss_melee_range_m + r_player = 2.0 + 0.5 = 2.5 m
                the boss's melee GATE under body_separation_v2 (spatial_engine:2645,
                `nearest_dist <= range_m + nearest_target.entity_radius`) — the `bsep`
                flag is ON in every leg name, so 2.5 is the live threshold.
  Reported contact fractions at three epsilons on C_body (0.01 = the S-1 tolerance,
  0.05, 0.25) plus the reach fraction at C_reach.

  KITE WINDOWS. A kite window is a maximal run of consecutive ticks with d_k > C_reach —
  i.e. the player is outside the boss's melee gate and the boss cannot hit. Reported as a
  count per fight plus durations in seconds. Also counted at the looser C_body+0.25.

  ATTACK-COMMIT. The boss's `commit_state` per tick, cross-tabbed against moving/stationary,
  and the boss displacement inside its own telegraph wind-up windows [onset_tick, fire_tick].

  ESCAPES. For each nova firing: d at onset, d at fire, min d in window, boss path length,
  player path length, net closure d_onset - d_fire, and closure rate.
"""

from __future__ import annotations

import glob
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict
from typing import Any, Optional

BAT = os.path.expanduser(
    "~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after"
)
LEGS = {
    "pre": "g5_m4cadence_nova_mitR2proxy_tg_dec_bsep_mv2_ntv2",
    "post": "g5_r3arm_m4cadence_nova_mitR3_tg_dec_bsep_mv2_ntv2",
    "pre_endpoint": "g5_m4cadence_nova_mitR2proxyresistslow_tg_dec_bsep_mv2_ntv2",
}
WATCH_SEED = 74000802
S1_TOL_M = 0.01
MOVE_EPS = 1e-9
EPS_LIST = [0.01, 0.05, 0.25]


# ─────────────────────────────────────────────────────────────── trace loading

def load_trace(path: str) -> dict[str, Any]:
    header = None
    g5h = None
    footer = None
    ticks: list[dict] = []
    events: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rt = rec.get("record_type")
            if rt == "header":
                header = rec
            elif rt == "g5_header":
                g5h = rec
            elif rt == "tick":
                ticks.append(rec)
            elif rt == "event":
                events.append(rec)
            elif rt == "footer":
                footer = rec
    return {"path": path, "basename": os.path.basename(path), "header": header,
            "g5_header": g5h, "footer": footer, "ticks": ticks, "events": events}


def identify(tr: dict) -> dict[str, Any]:
    """Header join: player id, boss id, radii, movement speeds, boss melee range."""
    hdr = tr["header"]
    ents = {e["entity_id"]: e for e in hdr["entities"]}
    player_ids = [e["entity_id"] for e in hdr["entities"] if e.get("is_player")]
    if len(player_ids) != 1:
        raise ValueError(f"{tr['basename']}: expected exactly 1 is_player, got {player_ids}")
    pid = player_ids[0]

    boss_id = None
    roster = (tr["g5_header"] or {}).get("g5", {}).get("opposition_roster", [])
    boss_records = [r["record"] for r in roster if r.get("tier") == "boss"]
    for rec in boss_records:
        prefix = rec.replace("/", "_")
        cands = [eid for eid in ents if eid.startswith(prefix)]
        if len(cands) == 1:
            boss_id = cands[0]
            break
    return {
        "player_id": pid,
        "boss_id": boss_id,
        "boss_records": boss_records,
        "radii": {eid: float(e["entity_radius_m"]) for eid, e in ents.items()},
        "speeds": {eid: e.get("movement_speed_ms") for eid, e in ents.items()},
        "skills": {eid: e.get("skills", []) for eid, e in ents.items()},
    }


# ───────────────────────────────────────────────────────── validation gate S-1

def s1_trace(tr: dict, radii: dict[str, float]) -> dict[str, Any]:
    worst = float("inf")
    worst_at = None
    n_pairs = 0
    n_viol = 0
    for rec in tr["ticks"]:
        live = [e for e in rec.get("entities", []) if e.get("alive")]
        for a in range(len(live)):
            ea = live[a]
            ra = radii[ea["entity_id"]]
            for b in range(a + 1, len(live)):
                eb = live[b]
                rb = radii[eb["entity_id"]]
                d = math.hypot(ea["x_m"] - eb["x_m"], ea["y_m"] - eb["y_m"])
                slack = d - (ra + rb)
                n_pairs += 1
                if slack < worst:
                    worst = slack
                    worst_at = {"tick": rec.get("tick"), "a": ea["entity_id"],
                                "b": eb["entity_id"], "d_m": d, "contact_m": ra + rb}
                if slack < -S1_TOL_M:
                    n_viol += 1
    return {"pair_samples": n_pairs,
            "worst_slack_m": (None if worst == float("inf") else worst),
            "worst_at": worst_at, "violations": n_viol}


# ────────────────────────────────────────────────────────────── the F-5 measures

def angle_between(ax: float, ay: float, bx: float, by: float) -> Optional[float]:
    na = math.hypot(ax, ay)
    nb = math.hypot(bx, by)
    if na <= 0.0 or nb <= 0.0:
        return None
    c = (ax * bx + ay * by) / (na * nb)
    c = max(-1.0, min(1.0, c))
    return math.degrees(math.acos(c))


def runs_above(flags: list[bool]) -> list[int]:
    """Lengths (in ticks) of maximal runs of True."""
    out = []
    n = 0
    for f in flags:
        if f:
            n += 1
        elif n:
            out.append(n)
            n = 0
    if n:
        out.append(n)
    return out


def measure_fight(tr: dict) -> Optional[dict[str, Any]]:
    ids = identify(tr)
    pid, bid = ids["player_id"], ids["boss_id"]
    if bid is None:
        return None
    v_boss = ids["speeds"].get(bid)
    v_play = ids["speeds"].get(pid)
    r_boss = ids["radii"][bid]
    r_play = ids["radii"][pid]
    boss_skills = ids["skills"].get(bid, [])
    melee_ranges = [s["range_m"] for s in boss_skills if s.get("geometry") == "point"]
    melee_r = min(melee_ranges) if melee_ranges else 2.0
    c_body = r_boss + r_play
    c_reach = melee_r + r_play

    # per-tick series where both alive
    T: list[float] = []
    K: list[int] = []
    B: list[tuple[float, float]] = []
    P: list[tuple[float, float]] = []
    CS: list[str] = []
    BH: list[Optional[float]] = []
    AIL: list[int] = []
    for rec in tr["ticks"]:
        blk = {e["entity_id"]: e for e in rec.get("entities", [])}
        eb, ep = blk.get(bid), blk.get(pid)
        if eb is None or ep is None:
            continue
        if not (eb.get("alive") and ep.get("alive")):
            continue
        K.append(rec["tick"])
        T.append(float(rec["t_s"]))
        B.append((eb["x_m"], eb["y_m"]))
        P.append((ep["x_m"], ep["y_m"]))
        CS.append(eb.get("commit_state") or "unknown")
        BH.append(eb.get("heading_rad"))
        AIL.append(len(eb.get("ailments") or []))
    n = len(T)
    if n < 2:
        return None

    sep = [math.dist(B[i], P[i]) for i in range(n)]

    utils: list[float] = []
    disp: list[float] = []
    th_pre: list[float] = []
    th_post: list[float] = []
    dts: list[float] = []
    moving_flags: list[bool] = []
    residual_after_step: list[float] = []   # d_{k+1} - the distance the boss "wanted"
    commit_move = defaultdict(lambda: {"ticks": 0, "moving": 0, "disp_sum": 0.0,
                                       "util_sum": 0.0, "util_n": 0})
    for k in range(n - 1):
        dt = T[k + 1] - T[k]
        dts.append(dt)
        dx, dy = B[k + 1][0] - B[k][0], B[k + 1][1] - B[k][1]
        s = math.hypot(dx, dy)
        disp.append(s)
        mv = s > MOVE_EPS
        moving_flags.append(mv)
        cap = (v_boss or 0.0) * dt
        u = (s / cap) if cap > 0 else None
        if u is not None:
            utils.append(u)
        st = CS[k]
        cm = commit_move[st]
        cm["ticks"] += 1
        cm["disp_sum"] += s
        if mv:
            cm["moving"] += 1
        if u is not None:
            cm["util_sum"] += u
            cm["util_n"] += 1
        if mv:
            a1 = angle_between(dx, dy, P[k][0] - B[k][0], P[k][1] - B[k][1])
            a2 = angle_between(dx, dy, P[k + 1][0] - B[k][0], P[k + 1][1] - B[k][1])
            if a1 is not None:
                th_pre.append(a1)
            if a2 is not None:
                th_post.append(a2)
        residual_after_step.append(sep[k + 1])

    # contact / reach fractions
    contact = {}
    for eps in EPS_LIST:
        thr = c_body + eps
        contact[f"body_plus_{eps}"] = sum(1 for d in sep if d <= thr) / n
    reach_flags = [d <= c_reach for d in sep]
    frac_reach = sum(reach_flags) / n

    # kite windows: player OUTSIDE the boss's melee gate
    kite_ticks = [not f for f in reach_flags]
    kite_runs = runs_above(kite_ticks)
    dt_nom = statistics.median(dts) if dts else 0.1
    kite_runs_s = [r * dt_nom for r in kite_runs]
    loose_flags = [d > (c_body + 0.25) for d in sep]
    loose_runs = runs_above(loose_flags)

    # ── boss telegraph wind-up windows (does the boss stop to attack?)
    tick_index = {k: i for i, k in enumerate(K)}
    boss_tg = [e for e in tr["events"]
               if e.get("event") == "telegraph" and e.get("attacker_id") == bid]
    # REALIZED ring delivery — the boss-sourced circle-geometry damage event. Measured, not
    # assumed to coincide with the telegraph's declared `fire_tick`: on this fixture it does
    # NOT (see the md note §6.2). The escape window's TRUE closing edge is this tick.
    ring_hits = [e for e in tr["events"]
                 if e.get("event") == "damage" and e.get("source_id") == bid
                 and e.get("geometry") == "circle"]
    windows = []
    for e in boss_tg:
        t0, t1 = e.get("tick"), e.get("fire_tick")
        if t0 is None or t1 is None:
            continue
        i0 = tick_index.get(t0)
        i1 = tick_index.get(t1)
        if i0 is None or i1 is None or i1 <= i0:
            continue
        seg_disp = sum(disp[i] for i in range(i0, min(i1, len(disp))))
        seg_ticks = i1 - i0
        p_disp = sum(math.dist(P[i], P[i + 1]) for i in range(i0, min(i1, n - 1)))
        w = {
            "attack_id": e.get("attack_id"),
            "is_nova": ":nova:" in (e.get("attack_id") or ""),
            "shape": e.get("shape"),
            "radius_m": e.get("radius_m"),
            "wind_up_s": e.get("wind_up_s"),
            "onset_tick": t0, "fire_tick": t1, "window_ticks": seg_ticks,
            "window_s": (T[i1] - T[i0]),
            "boss_path_m": seg_disp,
            "boss_moving_ticks": sum(1 for i in range(i0, min(i1, len(moving_flags)))
                                     if moving_flags[i]),
            "boss_mean_util": (statistics.fmean([utils[i] for i in range(i0, min(i1, len(utils)))])
                               if min(i1, len(utils)) > i0 else None),
            "player_path_m": p_disp,
            "d_onset_m": sep[i0], "d_fire_m": sep[i1],
            "d_min_in_window_m": min(sep[i0:i1 + 1]),
            "d_max_in_window_m": max(sep[i0:i1 + 1]),
            "net_closure_m": sep[i0] - sep[i1],
            "closure_rate_ms": ((sep[i0] - sep[i1]) / (T[i1] - T[i0])) if T[i1] > T[i0] else None,
            "boss_commit_states": dict(Counter(CS[i0:i1 + 1])),
            # for a nova: was the boss itself inside its own ring footprint at fire?
            "boss_dist_to_origin_at_fire_m": (
                math.dist(B[i1], (e["origin_x_m"], e["origin_y_m"]))
                if e.get("origin_x_m") is not None else None),
            "player_dist_to_origin_at_onset_m": (
                math.dist(P[i0], (e["origin_x_m"], e["origin_y_m"]))
                if e.get("origin_x_m") is not None else None),
            "player_dist_to_origin_at_fire_m": (
                math.dist(P[i1], (e["origin_x_m"], e["origin_y_m"]))
                if e.get("origin_x_m") is not None else None),
        }
        # realized closing edge
        if ring_hits:
            rh = min(ring_hits, key=lambda h: abs((h.get("tick") or 0) - t1))
            ir = tick_index.get(rh.get("tick"))
            w["realized_delivery_tick"] = rh.get("tick")
            w["realized_delivery_lag_ticks"] = (
                (rh.get("tick") - t1) if rh.get("tick") is not None else None)
            w["realized_delivered_hp"] = rh.get("delivered")
            w["telegraph_declared_damage"] = e.get("damage_amount")
            if ir is not None:
                w["d_at_realized_delivery_m"] = sep[ir]
                w["player_dist_to_origin_at_realized_delivery_m"] = (
                    math.dist(P[ir], (e["origin_x_m"], e["origin_y_m"]))
                    if e.get("origin_x_m") is not None else None)
                w["player_ever_outside_ring_in_window"] = (
                    any(math.dist(P[i], (e["origin_x_m"], e["origin_y_m"])) > (e["radius_m"] or 0.0)
                        for i in range(i0, ir + 1))
                    if e.get("origin_x_m") is not None and e.get("radius_m") else None)
                w["player_max_dist_to_origin_in_window_m"] = (
                    max(math.dist(P[i], (e["origin_x_m"], e["origin_y_m"]))
                        for i in range(i0, ir + 1))
                    if e.get("origin_x_m") is not None else None)
        windows.append(w)

    # boss committed-tick census over the whole fight
    commit_tab = {k: {"ticks": v["ticks"], "moving_ticks": v["moving"],
                      "frac_moving": (v["moving"] / v["ticks"]) if v["ticks"] else None,
                      "mean_disp_m": (v["disp_sum"] / v["ticks"]) if v["ticks"] else None,
                      "mean_util": (v["util_sum"] / v["util_n"]) if v["util_n"] else None}
                  for k, v in commit_move.items()}

    return {
        "trace": tr["basename"],
        "player_id": pid, "boss_id": bid,
        "v_boss_ms": v_boss, "v_player_ms": v_play,
        "speed_ratio_boss_over_player": ((v_boss / v_play) if (v_boss and v_play) else None),
        "r_boss_m": r_boss, "r_player_m": r_play,
        "boss_melee_range_m": melee_r,
        "c_body_m": c_body, "c_reach_m": c_reach,
        "ticks_both_alive": n, "steps": n - 1,
        "dt_median_s": dt_nom, "dt_distinct": sorted(set(round(x, 6) for x in dts)),
        "elapsed_s": (tr["footer"] or {}).get("elapsed_s"),
        "winner": (tr["footer"] or {}).get("winner"),
        # (2) utilization
        "util": summarize(utils),
        "util_moving_only": summarize([u for u, m in zip(utils, moving_flags) if m]),
        "frac_steps_moving": (sum(moving_flags) / len(moving_flags)) if moving_flags else None,
        "frac_steps_util_ge_0999": (sum(1 for u in utils if u >= 0.999) / len(utils)
                                    if utils else None),
        "frac_steps_util_ge_099": (sum(1 for u in utils if u >= 0.99) / len(utils)
                                   if utils else None),
        "boss_path_m": sum(disp),
        # (3) heading purity
        "theta_pre_deg": summarize(th_pre),
        "theta_post_deg": summarize(th_post),
        "frac_theta_pre_le_1deg": (sum(1 for a in th_pre if a <= 1.0) / len(th_pre)
                                   if th_pre else None),
        "frac_theta_post_le_1deg": (sum(1 for a in th_post if a <= 1.0) / len(th_post)
                                    if th_post else None),
        # (4) separation
        "sep": summarize(sep),
        "contact_fractions": contact,
        "frac_ticks_within_melee_gate": frac_reach,
        # (5) kite windows
        "kite_windows_n": len(kite_runs),
        "kite_windows_s": kite_runs_s,
        "kite_total_s": sum(kite_runs_s),
        "kite_frac_of_fight": (sum(kite_runs) / n) if n else None,
        "loose_windows_n": len(loose_runs),
        "loose_total_s": sum(r * dt_nom for r in loose_runs),
        "boss_commit_state_table": commit_tab,
        # (6) telegraph windows
        "boss_telegraph_windows": windows,
        "boss_telegraph_n": len(boss_tg),
        "boss_nova_n": sum(1 for e in boss_tg if ":nova:" in (e.get("attack_id") or "")),
        "boss_ailment_ticks": sum(1 for a in AIL if a > 0),
    }


def summarize(xs: list[float]) -> Optional[dict[str, float]]:
    if not xs:
        return None
    s = sorted(xs)
    def q(p):
        if len(s) == 1:
            return s[0]
        i = p * (len(s) - 1)
        lo, hi = int(math.floor(i)), int(math.ceil(i))
        return s[lo] + (s[hi] - s[lo]) * (i - lo)
    return {"n": len(s), "min": s[0], "p05": q(0.05), "p25": q(0.25), "median": q(0.50),
            "mean": statistics.fmean(s), "p75": q(0.75), "p95": q(0.95), "max": s[-1]}


def pool(xs: list[float]) -> Optional[dict[str, float]]:
    return summarize([x for x in xs if x is not None])


# ────────────────────────────────────────────────────────────────────── driver

def main() -> int:
    out: dict[str, Any] = {
        "instrument": "wr2_f5_pursuit.py",
        "run_id": "WR2-ENCGEO-2026-07-29",
        "finding": "F-WR2-5",
        "mode": "READ-ONLY over banked AFTER traces; no simulation executed",
        "battery_root": BAT,
        "legs": LEGS,
        "movement_speed_provenance": {
            "note": ("Recovered by read-only source inspection; NOT inferred from the traces. "
                     "The two sides of the ratio have DIFFERENT provenance."),
            "player_5.75": {
                "site": "spatial_gauntlet/spatial_engine.py:7311",
                "expression": 'float(class_dict.get("movement_speed", 5.75))',
                "classification": ("INFO-1's ungraded engine default. The kitcal werewolf kit "
                                   "declares no `movement_speed`, so the player takes 5.75 from "
                                   "the fallback. `kitcal_g5_harness.py:941` labels exactly this "
                                   'case `movement_speed_provenance = "engine-default-ungraded"`.'),
            },
            "boss_4.025": {
                "site": "spatial_gauntlet/kitcal_g5_scenarios.py:620",
                "expression": '"movement_speed": 5.75 * float(row.run_speed)',
                "classification": ("GRADED from the GD record: 5.75 (sim base pace) x the "
                                   "pak-adjusted `run_speed` multiplier. 4.025 / 5.75 = 0.70 "
                                   "exactly, so the boss record's run_speed is 0.70. Consumed via "
                                   "combatant.py:1342 `getattr(monster, 'movement_speed', 5.75)`."),
            },
            "escort_4.0825": {
                "site": "same as boss",
                "classification": "run_speed 0.71 on both escort records.",
            },
            "consequence": ("The ratio 0.70 is a graded number OVER an ungraded one. The "
                            "denominator is a default, not a measurement of the werewolf."),
        },
        "mob_navigation_law": {
            "note": "Read-only reference for what the utilization/heading measures are measuring.",
            "site": "spatial_gauntlet/spatial_engine.py:_navigate_entity (:1881), move block :2129-2156",
            "law": ("dx,dy = target - b ; d = |dx,dy| ; if d > 0.001: speed = v*dt "
                    "[x decrepify x chill] ; factor = min(speed/d, 1.0) ; "
                    "b += (dx,dy)*factor ; heading = atan2(dy,dx) ; then arena clamp."),
            "target_for_melee_boss": ("`nav_target` = the allegiance-filtered, taunt-weighted "
                                      "NEAREST enemy's CURRENT position (:5378-5384). No lead, "
                                      "no lag, no smoothing."),
            "call_gating": ("`_navigate_entity(mob, ...)` is called for every alive mob EVERY "
                            "tick, unconditionally within the mob-movement phase. Early returns "
                            "exist only for hard-CC, leash, and fear-flee. There is no "
                            "attack-commit branch and no acceleration/turn-rate state."),
            "melee_range_gate": ("spatial_engine.py:2645 under `body_separation_v2` (the `bsep` "
                                 "flag, ON in all three leg names): "
                                 "`nearest_dist <= range_m + nearest_target.entity_radius` -> "
                                 "2.0 + 0.5 = 2.5 m is the live threshold."),
            "body_separation_split": ("spatial_engine.py `_body_separation_split`: area-weighted, "
                                      "so the 1.5 m boss absorbs 0.10 of any overlap correction "
                                      "and the 0.5 m player absorbs 0.90."),
        },
    }

    # ── load every AFTER trace once (450), keep boss traces resident
    all_traces: dict[str, list[str]] = {}
    for leg, d in LEGS.items():
        all_traces[leg] = sorted(glob.glob(os.path.join(BAT, d, "traces", "*.jsonl")))
    total = sum(len(v) for v in all_traces.values())
    print(f"[load] {total} AFTER traces across {len(LEGS)} legs", file=sys.stderr)

    # ══ V3 : S-1 sweep over ALL traces (the heavy gate) ══
    s1_pairs = 0
    s1_viol = 0
    s1_worst = float("inf")
    s1_worst_row = None
    s1_traces = 0
    # ══ V4 : nova firing census ══
    nova_per_leg: Counter = Counter()
    nova_traces_per_leg: dict[str, set] = defaultdict(set)
    # ══ V1/V2 : footers ══
    elapsed: dict[tuple[str, str], list[float]] = defaultdict(list)
    watch_elapsed = None

    boss_measures: dict[str, list[dict]] = defaultdict(list)

    for leg, paths in all_traces.items():
        for p in paths:
            tr = load_trace(p)
            ids = identify(tr)
            r = s1_trace(tr, ids["radii"])
            s1_traces += 1
            s1_pairs += r["pair_samples"]
            s1_viol += r["violations"]
            if r["worst_slack_m"] is not None and r["worst_slack_m"] < s1_worst:
                s1_worst = r["worst_slack_m"]
                s1_worst_row = {"leg": leg, "trace": tr["basename"], **r["worst_at"]}
            base = tr["basename"]
            cell = base.split("__")[0]
            arm = base.split("__")[1]
            cellkey = f"{cell}/{arm}" if arm != "none" else cell
            f = tr["footer"] or {}
            if f.get("elapsed_s") is not None:
                elapsed[(leg, cellkey)].append(float(f["elapsed_s"]))
            nv = sum(1 for e in tr["events"]
                     if e.get("event") == "telegraph" and ":nova:" in (e.get("attack_id") or ""))
            if nv:
                nova_per_leg[leg] += nv
                nova_traces_per_leg[leg].add(base)
            if leg == "pre" and base == f"boss__B__seed{WATCH_SEED}.jsonl":
                watch_elapsed = f.get("elapsed_s")
            if cell == "boss":
                m = measure_fight(tr)
                if m is not None:
                    m["leg"] = leg
                    m["cell"] = cellkey
                    m["seed"] = int(base.split("seed")[1].split(".")[0])
                    boss_measures[leg].append(m)

    gates = {
        "V1_watch_seed_footer": {
            "expect": 37.0, "got": watch_elapsed,
            "pass": watch_elapsed is not None and abs(watch_elapsed - 37.0) < 1e-6,
            "exhibit": f"pre / boss/B / seed{WATCH_SEED}",
        },
        "V2_pre_leg_elapsed_means": {},
        "V3_s1_sweep": {
            "traces": s1_traces, "expect_traces": 450,
            "pair_samples": s1_pairs, "expect_pair_samples": 292305,
            "violations": s1_viol, "expect_violations": 0,
            "worst_slack_m": (None if s1_worst == float("inf") else s1_worst),
            "expect_worst_slack_m": -0.000989,
            "worst_at": s1_worst_row,
        },
        "V4_nova_firings": {
            "per_leg": dict(nova_per_leg), "total": sum(nova_per_leg.values()),
            "expect_total": 132, "expect_per_leg": 44,
            "traces_per_leg": {k: len(v) for k, v in nova_traces_per_leg.items()},
        },
    }
    for cellkey, expect in (("boss/A", 32.04), ("boss/B", 48.92)):
        vals = elapsed[("pre", cellkey)]
        got = statistics.fmean(vals) if vals else None
        gates["V2_pre_leg_elapsed_means"][cellkey] = {
            "expect": expect, "got": got, "n": len(vals),
            "pass": got is not None and abs(round(got, 2) - expect) < 0.005,
        }
    gates["V3_s1_sweep"]["pass"] = (
        s1_traces == 450 and s1_pairs == 292305 and s1_viol == 0
        and s1_worst is not None and abs(s1_worst - (-0.000989)) < 5e-7
    )
    gates["V4_nova_firings"]["pass"] = (
        sum(nova_per_leg.values()) == 132
        and all(v == 44 for v in nova_per_leg.values())
    )
    gates["all_pass"] = (
        gates["V1_watch_seed_footer"]["pass"]
        and all(v["pass"] for v in gates["V2_pre_leg_elapsed_means"].values())
        and gates["V3_s1_sweep"]["pass"] and gates["V4_nova_firings"]["pass"]
    )
    out["validation_gates"] = gates
    for k, v in gates.items():
        if isinstance(v, dict):
            print(f"[gate] {k}: pass={v.get('pass')}", file=sys.stderr)
    print(f"[gate] ALL_PASS={gates['all_pass']}", file=sys.stderr)

    # ── per-leg + pooled F-5 metrics
    out["per_fight"] = {leg: ms for leg, ms in boss_measures.items()}
    pooled: dict[str, Any] = {}
    flat = [m for ms in boss_measures.values() for m in ms]
    for leg in list(LEGS) + ["POOLED"]:
        ms = flat if leg == "POOLED" else boss_measures.get(leg, [])
        if not ms:
            continue
        wins = [w for m in ms for w in m["boss_telegraph_windows"]]
        novas = [w for w in wins if w["is_nova"]]
        pooled[leg] = {
            "fights": len(ms),
            # (1) speed ratio
            "speed_ratio_distinct": sorted({m["speed_ratio_boss_over_player"] for m in ms}),
            "v_boss_distinct": sorted({m["v_boss_ms"] for m in ms}),
            "v_player_distinct": sorted({m["v_player_ms"] for m in ms}),
            # (2) utilization
            "util_pooled_mean_of_fight_means": pool([m["util"]["mean"] for m in ms
                                                     if m["util"]]),
            "util_moving_only_pooled": pool([m["util_moving_only"]["mean"] for m in ms
                                             if m["util_moving_only"]]),
            "frac_steps_moving": pool([m["frac_steps_moving"] for m in ms]),
            "frac_steps_util_ge_0999": pool([m["frac_steps_util_ge_0999"] for m in ms]),
            "util_min_over_fights": min((m["util"]["min"] for m in ms if m["util"]),
                                        default=None),
            "util_max_over_fights": max((m["util"]["max"] for m in ms if m["util"]),
                                        default=None),
            # (3) heading purity
            "theta_pre_mean": pool([m["theta_pre_deg"]["mean"] for m in ms
                                    if m["theta_pre_deg"]]),
            "theta_pre_max_over_fights": max((m["theta_pre_deg"]["max"] for m in ms
                                              if m["theta_pre_deg"]), default=None),
            "theta_post_mean": pool([m["theta_post_deg"]["mean"] for m in ms
                                     if m["theta_post_deg"]]),
            "theta_post_max_over_fights": max((m["theta_post_deg"]["max"] for m in ms
                                               if m["theta_post_deg"]), default=None),
            "frac_theta_pre_le_1deg": pool([m["frac_theta_pre_le_1deg"] for m in ms]),
            "frac_theta_post_le_1deg": pool([m["frac_theta_post_le_1deg"] for m in ms]),
            # (4) separation
            "sep_min_over_fights": min((m["sep"]["min"] for m in ms if m["sep"]), default=None),
            "sep_mean": pool([m["sep"]["mean"] for m in ms if m["sep"]]),
            "sep_max_over_fights": max((m["sep"]["max"] for m in ms if m["sep"]), default=None),
            "sep_median": pool([m["sep"]["median"] for m in ms if m["sep"]]),
            "contact_frac_body_plus_001": pool([m["contact_fractions"]["body_plus_0.01"]
                                                for m in ms]),
            "contact_frac_body_plus_005": pool([m["contact_fractions"]["body_plus_0.05"]
                                                for m in ms]),
            "contact_frac_body_plus_025": pool([m["contact_fractions"]["body_plus_0.25"]
                                                for m in ms]),
            "frac_ticks_within_melee_gate": pool([m["frac_ticks_within_melee_gate"]
                                                  for m in ms]),
            # (5) kite windows
            "kite_windows_per_fight": pool([float(m["kite_windows_n"]) for m in ms]),
            "kite_window_durations_s": summarize([d for m in ms for d in m["kite_windows_s"]]),
            "kite_total_s_per_fight": pool([m["kite_total_s"] for m in ms]),
            "kite_frac_of_fight": pool([m["kite_frac_of_fight"] for m in ms]),
            "fights_with_zero_kite_windows": sum(1 for m in ms if m["kite_windows_n"] == 0),
            # (6) telegraph / escape
            "boss_telegraph_windows_n": len(wins),
            "boss_nova_windows_n": len(novas),
            "nova_boss_path_m": summarize([w["boss_path_m"] for w in novas]),
            "nova_player_path_m": summarize([w["player_path_m"] for w in novas]),
            "nova_boss_moving_frac": summarize([w["boss_moving_ticks"] / w["window_ticks"]
                                                for w in novas if w["window_ticks"]]),
            "nova_boss_mean_util": summarize([w["boss_mean_util"] for w in novas
                                              if w["boss_mean_util"] is not None]),
            "nova_d_onset_m": summarize([w["d_onset_m"] for w in novas]),
            "nova_d_fire_m": summarize([w["d_fire_m"] for w in novas]),
            "nova_d_max_in_window_m": summarize([w["d_max_in_window_m"] for w in novas]),
            "nova_net_closure_m": summarize([w["net_closure_m"] for w in novas]),
            "nova_closure_rate_ms": summarize([w["closure_rate_ms"] for w in novas
                                               if w["closure_rate_ms"] is not None]),
            "nova_window_s": summarize([w["window_s"] for w in novas]),
            "nova_player_d_to_origin_onset_m": summarize(
                [w["player_dist_to_origin_at_onset_m"] for w in novas
                 if w["player_dist_to_origin_at_onset_m"] is not None]),
            "nova_player_d_to_origin_fire_m": summarize(
                [w["player_dist_to_origin_at_fire_m"] for w in novas
                 if w["player_dist_to_origin_at_fire_m"] is not None]),
            "nova_boss_d_to_origin_fire_m": summarize(
                [w["boss_dist_to_origin_at_fire_m"] for w in novas
                 if w["boss_dist_to_origin_at_fire_m"] is not None]),
            "nova_radius_distinct": sorted({w["radius_m"] for w in novas
                                            if w["radius_m"] is not None}),
            "nova_realized_delivery_lag_ticks": summarize(
                [w["realized_delivery_lag_ticks"] for w in novas
                 if w.get("realized_delivery_lag_ticks") is not None]),
            "nova_realized_delivered_hp": summarize(
                [w["realized_delivered_hp"] for w in novas
                 if w.get("realized_delivered_hp") is not None]),
            "nova_telegraph_declared_damage": summarize(
                [w["telegraph_declared_damage"] for w in novas
                 if w.get("telegraph_declared_damage") is not None]),
            "nova_d_at_realized_delivery_m": summarize(
                [w["d_at_realized_delivery_m"] for w in novas
                 if w.get("d_at_realized_delivery_m") is not None]),
            "nova_player_d_to_origin_at_realized_delivery_m": summarize(
                [w["player_dist_to_origin_at_realized_delivery_m"] for w in novas
                 if w.get("player_dist_to_origin_at_realized_delivery_m") is not None]),
            "nova_player_max_d_to_origin_in_window_m": summarize(
                [w["player_max_dist_to_origin_in_window_m"] for w in novas
                 if w.get("player_max_dist_to_origin_in_window_m") is not None]),
            "nova_firings_where_player_left_the_ring": sum(
                1 for w in novas if w.get("player_ever_outside_ring_in_window") is True),
            "nova_firings_assessed_for_ring_exit": sum(
                1 for w in novas if w.get("player_ever_outside_ring_in_window") is not None),
            # commit-state census pooled
            "boss_commit_states_seen": sorted({s for m in ms
                                               for s in m["boss_commit_state_table"]}),
            "boss_commit_state_pooled": _pool_commit(ms),
        }
    out["pooled"] = pooled

    # watch-seed exhibit
    exhibit = [m for m in boss_measures.get("pre", [])
               if m["seed"] == WATCH_SEED]
    out["watch_seed_exhibit"] = {m["cell"]: m for m in exhibit}

    dest = os.path.expanduser(
        "~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/"
        "2026-07-30-wr2-f5-pursuit-diagnostic.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=False)
    print(f"[write] {dest}", file=sys.stderr)
    return 0 if gates["all_pass"] else 2


def _pool_commit(ms: list[dict]) -> dict[str, Any]:
    agg: dict[str, dict[str, float]] = defaultdict(
        lambda: {"ticks": 0.0, "moving_ticks": 0.0, "disp_sum": 0.0})
    for m in ms:
        for st, v in m["boss_commit_state_table"].items():
            agg[st]["ticks"] += v["ticks"]
            agg[st]["moving_ticks"] += v["moving_ticks"]
            agg[st]["disp_sum"] += (v["mean_disp_m"] or 0.0) * v["ticks"]
    return {st: {"ticks": int(v["ticks"]), "moving_ticks": int(v["moving_ticks"]),
                 "frac_moving": (v["moving_ticks"] / v["ticks"]) if v["ticks"] else None,
                 "mean_disp_m": (v["disp_sum"] / v["ticks"]) if v["ticks"] else None}
            for st, v in agg.items()}


if __name__ == "__main__":
    sys.exit(main())
