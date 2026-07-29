#!/usr/bin/env python3
"""WR1-ENV: room-sizing envelope extraction from banked WR1-BATTERY-2 traces.

READ-ONLY over the engine tree. Emits JSON to stdout.
Instrument: this script. Substrate: g5-replay-trace/v1 JSONL, 450 traces.
"""
import json, math, os, sys, glob
from collections import defaultdict

BASE = "/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2"
LEGS = {
    "pre": "g5_m4cadence_nova_mitR2proxy_tg",
    "pre_endpoint": "g5_m4cadence_nova_mitR2proxyresistslow_tg",
    "post": "g5_r3arm_m4cadence_nova_mitR3_tg",
}


def pct(sorted_vals, q):
    """nearest-rank percentile, 1-based, k = ceil(q*m)."""
    m = len(sorted_vals)
    if m == 0:
        return None
    k = max(1, math.ceil(q * m))
    return sorted_vals[k - 1]


def summarize(vals):
    v = sorted(vals)
    if not v:
        return None
    return {
        "n": len(v),
        "min": round(v[0], 3),
        "median": round(pct(v, 0.50), 3),
        "p95": round(pct(v, 0.95), 3),
        "max": round(v[-1], 3),
        "mean": round(sum(v) / len(v), 3),
    }


def analyze_trace(path):
    header = None
    g5 = None
    footer = None
    ticks = []
    telegraphs = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rt = r["record_type"]
            if rt == "header":
                header = r
            elif rt == "g5_header":
                g5 = r
            elif rt == "footer":
                footer = r
            elif rt == "tick":
                ticks.append(r)
            elif rt == "event" and r.get("event") == "telegraph":
                telegraphs.append(r)

    ents = {e["entity_id"]: e for e in header["entities"]}
    player_id = next(e["entity_id"] for e in header["entities"] if e.get("is_player"))
    radii = {eid: e.get("entity_radius_m", 0.0) or 0.0 for eid, e in ents.items()}

    # --- occupancy point sets ---
    # spawn footprint: every entity occupies its spawn point at t=0 regardless of
    # whether it survives frame 0 (it stands there before the first resolution).
    spawn_pts = [(e["spawn_x_m"], e["spawn_y_m"], radii[e["entity_id"]],
                  bool(e.get("is_player"))) for e in header["entities"]]

    pts = list(spawn_pts)          # (x, y, radius, is_player)
    player_pts = [p for p in spawn_pts if p[3]]
    mob_pts = [p for p in spawn_pts if not p[3]]
    seps = []

    for t in ticks:
        pos = {}
        for e in t["entities"]:
            if not e.get("alive"):
                continue
            eid = e["entity_id"]
            p = (e["x_m"], e["y_m"], radii.get(eid, 0.0), eid == player_id)
            pos[eid] = p
            pts.append(p)
            (player_pts if p[3] else mob_pts).append(p)
        if player_id in pos:
            px, py = pos[player_id][0], pos[player_id][1]
            for eid, p in pos.items():
                if eid == player_id:
                    continue
                seps.append(math.hypot(p[0] - px, p[1] - py))

    def bbox(points, inflate):
        if not points:
            return None
        if inflate:
            xs0 = [p[0] - p[2] for p in points]
            xs1 = [p[0] + p[2] for p in points]
            ys0 = [p[1] - p[2] for p in points]
            ys1 = [p[1] + p[2] for p in points]
        else:
            xs0 = xs1 = [p[0] for p in points]
            ys0 = ys1 = [p[1] for p in points]
        return (max(xs1) - min(xs0), max(ys1) - min(ys0))

    w_c, d_c = bbox(pts, False)
    w_i, d_i = bbox(pts, True)
    pw, pd = bbox(player_pts, False)
    mb = bbox(mob_pts, False)
    mw, md = mb if mb else (0.0, 0.0)

    # nova telegraph reach
    nova_radii = [tg["radius_m"] for tg in telegraphs
                  if tg.get("radius_m") is not None]
    shapes = sorted({tg.get("shape") for tg in telegraphs})

    return {
        "fight_key": header.get("fight_key"),
        "arena_w": header["frame"]["arena_width_m"],
        "arena_h": header["frame"]["arena_height_m"],
        "n_entities": len(ents),
        "elapsed_s": footer["elapsed_s"],
        "winner": footer["winner"],
        "envelope_w_center": w_c,
        "envelope_d_center": d_c,
        "envelope_span_center": max(w_c, d_c),
        "envelope_diag_center": math.hypot(w_c, d_c),
        "envelope_w_infl": w_i,
        "envelope_d_infl": d_i,
        "envelope_span_infl": max(w_i, d_i),
        "player_w": pw, "player_d": pd, "player_span": max(pw, pd),
        "mob_w": mw, "mob_d": md, "mob_span": max(mw, md),
        "sep_median": pct(sorted(seps), 0.50) if seps else None,
        "sep_p95": pct(sorted(seps), 0.95) if seps else None,
        "sep_max": max(seps) if seps else None,
        "nova_radii": nova_radii,
        "telegraph_shapes": shapes,
        "n_telegraph": len(telegraphs),
    }


def main():
    rows = []
    for leg, d in LEGS.items():
        for path in sorted(glob.glob(os.path.join(BASE, d, "traces", "*.jsonl"))):
            fn = os.path.basename(path)[:-6]
            tier, arm, seedtok = fn.split("__")
            rec = analyze_trace(path)
            rec.update({"leg": leg, "tier": tier, "arm": arm,
                        "seed": int(seedtok.replace("seed", ""))})
            rows.append(rec)

    out = {"n_traces": len(rows), "by_tier": {}, "by_tier_leg": {}, "nova": {}}

    def block(rs):
        return {
            "n_fights": len(rs),
            "envelope_span_center_m": summarize([r["envelope_span_center"] for r in rs]),
            "envelope_span_inflated_m": summarize([r["envelope_span_infl"] for r in rs]),
            "envelope_w_center_m": summarize([r["envelope_w_center"] for r in rs]),
            "envelope_d_center_m": summarize([r["envelope_d_center"] for r in rs]),
            "envelope_diag_center_m": summarize([r["envelope_diag_center"] for r in rs]),
            "player_span_m": summarize([r["player_span"] for r in rs]),
            "mob_span_m": summarize([r["mob_span"] for r in rs]),
            "sep_median_of_fight_medians_m": summarize([r["sep_median"] for r in rs if r["sep_median"] is not None]),
            "sep_p95_per_fight_m": summarize([r["sep_p95"] for r in rs if r["sep_p95"] is not None]),
            "sep_max_per_fight_m": summarize([r["sep_max"] for r in rs if r["sep_max"] is not None]),
            "elapsed_s": summarize([r["elapsed_s"] for r in rs]),
            "n_entities": summarize([float(r["n_entities"]) for r in rs]),
            "winners": {w: sum(1 for r in rs if r["winner"] == w) for w in sorted({r["winner"] for r in rs})},
        }

    tiers = sorted({r["tier"] for r in rows})
    for t in tiers:
        out["by_tier"][t] = block([r for r in rows if r["tier"] == t])
        for leg in LEGS:
            sub = [r for r in rows if r["tier"] == t and r["leg"] == leg]
            if sub:
                out["by_tier_leg"][f"{t}/{leg}"] = block(sub)
    # boss split by arm
    for arm in ("A", "B"):
        sub = [r for r in rows if r["tier"] == "boss" and r["arm"] == arm]
        if sub:
            out["by_tier_leg"][f"boss/arm_{arm}"] = block(sub)

    allnova = [x for r in rows for x in r["nova_radii"]]
    out["nova"] = {
        "distinct_telegraph_radii_m": sorted(set(round(x, 4) for x in allnova)),
        "n_radius_bearing_telegraphs": len(allnova),
        "telegraph_shapes_seen": sorted({s for r in rows for s in r["telegraph_shapes"] if s}),
        "telegraphs_per_fight_by_tier": {t: summarize([float(r["n_telegraph"]) for r in rows if r["tier"] == t]) for t in tiers},
    }
    out["arena"] = {"width_m": rows[0]["arena_w"], "height_m": rows[0]["arena_h"]}
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
