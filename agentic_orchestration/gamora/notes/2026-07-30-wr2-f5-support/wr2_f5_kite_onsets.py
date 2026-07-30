#!/usr/bin/env python3
"""
F-WR2-5 supplement — WHERE the kite windows fall, and the nova-window tick alignment.

Read-only, self-contained. Answers:
  (a) is the single conceded kite window the OPENING approach, or is it mid-fight?
  (b) what creates the 2nd window in the minority of fights?
  (c) do the theta_pre outliers coincide with a body-separation shove (a step that ENDS at
      the S-1 floor, where the solver's 0.10 area-weighted correction on the boss rotates
      the realized displacement off the pursuit ray)?
  (d) the nova window's tick alignment vs the kite window.
"""
from __future__ import annotations

import glob
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict

BAT = os.path.expanduser(
    "~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after"
)
LEGS = {
    "pre": "g5_m4cadence_nova_mitR2proxy_tg_dec_bsep_mv2_ntv2",
    "post": "g5_r3arm_m4cadence_nova_mitR3_tg_dec_bsep_mv2_ntv2",
    "pre_endpoint": "g5_m4cadence_nova_mitR2proxyresistslow_tg_dec_bsep_mv2_ntv2",
}


def rows(path):
    hdr = g5 = None
    ticks, events, footer = [], [], None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        rt = r.get("record_type")
        if rt == "header":
            hdr = r
        elif rt == "g5_header":
            g5 = r
        elif rt == "tick":
            ticks.append(r)
        elif rt == "event":
            events.append(r)
        elif rt == "footer":
            footer = r
    return hdr, g5, ticks, events, footer


def main():
    out = {"instrument": "wr2_f5_kite_onsets.py", "mode": "READ-ONLY", "legs": {}}
    pooled_first_onset = []
    pooled_first_end = []
    pooled_second_onset = []
    pooled_window_specs = Counter()
    theta_outlier_at_floor = 0
    theta_outlier_total = 0
    per_fight = []

    for leg, dirname in LEGS.items():
        for path in sorted(glob.glob(os.path.join(BAT, dirname, "traces", "boss__*.jsonl"))):
            hdr, g5, ticks, events, footer = rows(path)
            ents = {e["entity_id"]: e for e in hdr["entities"]}
            pid = next(e["entity_id"] for e in hdr["entities"] if e.get("is_player"))
            roster = g5["g5"]["opposition_roster"]
            bid = None
            for r in roster:
                if r.get("tier") == "boss":
                    pre = r["record"].replace("/", "_")
                    c = [e for e in ents if e.startswith(pre)]
                    if len(c) == 1:
                        bid = c[0]
                        break
            if bid is None:
                continue
            r_b, r_p = ents[bid]["entity_radius_m"], ents[pid]["entity_radius_m"]
            v_b = ents[bid]["movement_speed_ms"]
            melee = min([s["range_m"] for s in ents[bid]["skills"]
                         if s.get("geometry") == "point"] or [2.0])
            c_body, c_reach = r_b + r_p, melee + r_p

            K, T, B, P = [], [], [], []
            for t in ticks:
                blk = {e["entity_id"]: e for e in t["entities"]}
                eb, ep = blk.get(bid), blk.get(pid)
                if not eb or not ep or not (eb.get("alive") and ep.get("alive")):
                    continue
                K.append(t["tick"]); T.append(t["t_s"])
                B.append((eb["x_m"], eb["y_m"])); P.append((ep["x_m"], ep["y_m"]))
            if len(K) < 2:
                continue
            sep = [math.dist(B[i], P[i]) for i in range(len(K))]
            out_gate = [d > c_reach for d in sep]

            # maximal runs of out_gate with their tick bounds
            runs = []
            i = 0
            while i < len(out_gate):
                if out_gate[i]:
                    j = i
                    while j + 1 < len(out_gate) and out_gate[j + 1]:
                        j += 1
                    runs.append({"start_tick": K[i], "end_tick": K[j],
                                 "start_t_s": T[i], "end_t_s": T[j],
                                 "ticks": j - i + 1,
                                 "duration_s": round(T[j] - T[i] + (T[1] - T[0]), 6),
                                 "d_at_start_m": sep[i], "d_max_m": max(sep[i:j + 1]),
                                 "is_opening": K[i] == K[0]})
                    i = j + 1
                else:
                    i += 1
            if runs:
                pooled_first_onset.append(runs[0]["start_t_s"])
                pooled_first_end.append(runs[0]["end_t_s"])
            if len(runs) > 1:
                pooled_second_onset.append(runs[1]["start_t_s"])
            pooled_window_specs[
                (len(runs), tuple(r["is_opening"] for r in runs))] += 1

            # (c) theta outliers vs body-separation floor
            for k in range(len(K) - 1):
                dx, dy = B[k + 1][0] - B[k][0], B[k + 1][1] - B[k][1]
                s = math.hypot(dx, dy)
                if s <= 1e-9:
                    continue
                wx, wy = P[k][0] - B[k][0], P[k][1] - B[k][1]
                nw = math.hypot(wx, wy)
                if nw <= 0:
                    continue
                c = max(-1.0, min(1.0, (dx * wx + dy * wy) / (s * nw)))
                th = math.degrees(math.acos(c))
                if th > 5.0:
                    theta_outlier_total += 1
                    if sep[k + 1] <= c_body + 0.01:
                        theta_outlier_at_floor += 1

            novas = [e for e in events if e.get("event") == "telegraph"
                     and ":nova:" in (e.get("attack_id") or "")]
            per_fight.append({
                "leg": leg, "trace": os.path.basename(path),
                "c_body_m": c_body, "c_reach_m": c_reach, "v_boss_ms": v_b,
                "elapsed_s": footer.get("elapsed_s"), "winner": footer.get("winner"),
                "n_out_of_gate_windows": len(runs), "windows": runs,
                "nova_onset_ticks": [e["tick"] for e in novas],
                "nova_fire_ticks": [e["fire_tick"] for e in novas],
                "first_tick_at_gate": next((K[i] for i, f in enumerate(out_gate) if not f), None),
                "first_t_s_at_gate": next((T[i] for i, f in enumerate(out_gate) if not f), None),
                "first_tick_at_body_floor": next(
                    (K[i] for i, d in enumerate(sep) if d <= c_body + 0.01), None),
                "first_t_s_at_body_floor": next(
                    (T[i] for i, d in enumerate(sep) if d <= c_body + 0.01), None),
                "spawn_sep_m": sep[0],
                "last_tick_t_s": T[-1],
            })

    def summ(xs):
        if not xs:
            return None
        s = sorted(xs)
        return {"n": len(s), "min": s[0], "median": s[len(s) // 2],
                "mean": statistics.fmean(s), "max": s[-1],
                "distinct": sorted(set(round(x, 6) for x in s))[:12]}

    out["first_window_onset_t_s"] = summ(pooled_first_onset)
    out["first_window_end_t_s"] = summ(pooled_first_end)
    out["second_window_onset_t_s"] = summ(pooled_second_onset)
    out["window_shape_census"] = {f"n={k[0]} opening_flags={k[1]}": v
                                  for k, v in pooled_window_specs.items()}
    out["theta_gt_5deg_steps"] = theta_outlier_total
    out["theta_gt_5deg_steps_ending_at_body_floor"] = theta_outlier_at_floor
    out["theta_outlier_floor_frac"] = (theta_outlier_at_floor / theta_outlier_total
                                       if theta_outlier_total else None)
    out["first_t_s_at_gate"] = summ([f["first_t_s_at_gate"] for f in per_fight
                                     if f["first_t_s_at_gate"] is not None])
    out["first_t_s_at_body_floor"] = summ([f["first_t_s_at_body_floor"] for f in per_fight
                                           if f["first_t_s_at_body_floor"] is not None])
    out["spawn_sep_m"] = summ([f["spawn_sep_m"] for f in per_fight])
    out["nova_onset_ticks_distinct"] = sorted(
        {t for f in per_fight for t in f["nova_onset_ticks"]})
    out["nova_fire_ticks_distinct"] = sorted(
        {t for f in per_fight for t in f["nova_fire_ticks"]})
    out["per_fight"] = per_fight

    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "wr2_f5_kite_onsets_output.json")
    json.dump(out, open(dest, "w", encoding="utf-8"), indent=1)
    for k in ("first_window_onset_t_s", "first_window_end_t_s", "second_window_onset_t_s",
              "window_shape_census", "theta_gt_5deg_steps",
              "theta_gt_5deg_steps_ending_at_body_floor", "theta_outlier_floor_frac",
              "first_t_s_at_gate", "first_t_s_at_body_floor", "spawn_sep_m",
              "nova_onset_ticks_distinct", "nova_fire_ticks_distinct"):
        print(k, "=", json.dumps(out[k]))
    print("[write]", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
