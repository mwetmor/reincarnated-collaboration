#!/usr/bin/env python3
"""WR1-ENV pass 2: absolute bbox coords, spawn-vs-movement decomposition,
arena-bound proximity check, per-leg/per-arm splits. READ-ONLY."""
import json, math, os, sys, glob

BASE = "/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2"
LEGS = {
    "pre": "g5_m4cadence_nova_mitR2proxy_tg",
    "pre_endpoint": "g5_m4cadence_nova_mitR2proxyresistslow_tg",
    "post": "g5_r3arm_m4cadence_nova_mitR3_tg",
}


def pct(v, q):
    m = len(v)
    return v[max(1, math.ceil(q * m)) - 1] if m else None


def summ(vals):
    v = sorted(vals)
    if not v:
        return None
    return {"n": len(v), "min": round(v[0], 3), "median": round(pct(v, .5), 3),
            "p95": round(pct(v, .95), 3), "max": round(v[-1], 3)}


def analyze(path):
    hdr = g5 = ftr = None
    ticks, tele = [], []
    for line in open(path):
        r = json.loads(line)
        rt = r["record_type"]
        if rt == "header": hdr = r
        elif rt == "g5_header": g5 = r
        elif rt == "footer": ftr = r
        elif rt == "tick": ticks.append(r)
        elif rt == "event" and r.get("event") == "telegraph": tele.append(r)

    ents = {e["entity_id"]: e for e in hdr["entities"]}
    pid = next(e["entity_id"] for e in hdr["entities"] if e.get("is_player"))
    rad = {k: (v.get("entity_radius_m") or 0.0) for k, v in ents.items()}

    spawn = [(e["spawn_x_m"], e["spawn_y_m"], rad[e["entity_id"]]) for e in hdr["entities"]]
    spawn_box = (min(p[0] for p in spawn), max(p[0] for p in spawn),
                 min(p[1] for p in spawn), max(p[1] for p in spawn))

    allp, plp, mbp = list(spawn), [], []
    for e in hdr["entities"]:
        (plp if e.get("is_player") else mbp).append(
            (e["spawn_x_m"], e["spawn_y_m"], rad[e["entity_id"]]))
    seps = []
    for t in ticks:
        pos = {}
        for e in t["entities"]:
            if not e.get("alive"): continue
            p = (e["x_m"], e["y_m"], rad.get(e["entity_id"], 0.))
            pos[e["entity_id"]] = p
            allp.append(p)
            (plp if e["entity_id"] == pid else mbp).append(p)
        if pid in pos:
            px, py = pos[pid][:2]
            for k, p in pos.items():
                if k != pid:
                    seps.append(math.hypot(p[0] - px, p[1] - py))

    def box(ps, infl=False):
        if not ps: return None
        x0 = min(p[0] - (p[2] if infl else 0) for p in ps)
        x1 = max(p[0] + (p[2] if infl else 0) for p in ps)
        y0 = min(p[1] - (p[2] if infl else 0) for p in ps)
        y1 = max(p[1] + (p[2] if infl else 0) for p in ps)
        return (x0, x1, y0, y1)

    bc = box(allp); bi = box(allp, True)
    pb = box(plp); mb = box(mbp)
    aw, ah = hdr["frame"]["arena_width_m"], hdr["frame"]["arena_height_m"]
    margin_to_arena = min(bi[0] - 0, aw - bi[1], bi[2] - 0, ah - bi[3])

    return dict(
        tier=None, elapsed_s=ftr["elapsed_s"], winner=ftr["winner"],
        n_ent=len(ents), arena=(aw, ah),
        spawn_w=spawn_box[1] - spawn_box[0], spawn_d=spawn_box[3] - spawn_box[2],
        env_x0=bc[0], env_x1=bc[1], env_y0=bc[2], env_y1=bc[3],
        env_w=bc[1] - bc[0], env_d=bc[3] - bc[2],
        env_w_i=bi[1] - bi[0], env_d_i=bi[3] - bi[2],
        env_span_i=max(bi[1] - bi[0], bi[3] - bi[2]),
        env_diag_i=math.hypot(bi[1] - bi[0], bi[3] - bi[2]),
        margin_to_arena=margin_to_arena,
        player_w=pb[1] - pb[0], player_d=pb[3] - pb[2],
        mob_w=mb[1] - mb[0], mob_d=mb[3] - mb[2],
        sep_med=pct(sorted(seps), .5), sep_p95=pct(sorted(seps), .95),
        sep_max=max(seps) if seps else None,
        nova_r=[t["radius_m"] for t in tele if t.get("radius_m") is not None],
        n_tele=len(tele),
    )


rows = []
for leg, d in LEGS.items():
    for p in sorted(glob.glob(os.path.join(BASE, d, "traces", "*.jsonl"))):
        fn = os.path.basename(p)[:-6]
        tier, arm, sd = fn.split("__")
        r = analyze(p)
        r.update(leg=leg, tier=tier, arm=arm, seed=int(sd[4:]))
        rows.append(r)


def blk(rs):
    return {
        "n": len(rs),
        "env_w_infl": summ([r["env_w_i"] for r in rs]),
        "env_d_infl": summ([r["env_d_i"] for r in rs]),
        "env_span_infl": summ([r["env_span_i"] for r in rs]),
        "env_diag_infl": summ([r["env_diag_i"] for r in rs]),
        "spawn_w": summ([r["spawn_w"] for r in rs]),
        "spawn_d": summ([r["spawn_d"] for r in rs]),
        "env_w_center": summ([r["env_w"] for r in rs]),
        "env_d_center": summ([r["env_d"] for r in rs]),
        "player_w": summ([r["player_w"] for r in rs]),
        "player_d": summ([r["player_d"] for r in rs]),
        "mob_w": summ([r["mob_w"] for r in rs]),
        "mob_d": summ([r["mob_d"] for r in rs]),
        "sep_med": summ([r["sep_med"] for r in rs if r["sep_med"] is not None]),
        "sep_p95": summ([r["sep_p95"] for r in rs if r["sep_p95"] is not None]),
        "sep_max": summ([r["sep_max"] for r in rs if r["sep_max"] is not None]),
        "elapsed_s": summ([r["elapsed_s"] for r in rs]),
        "margin_to_arena": summ([r["margin_to_arena"] for r in rs]),
        "env_x0": summ([r["env_x0"] for r in rs]), "env_x1": summ([r["env_x1"] for r in rs]),
        "env_y0": summ([r["env_y0"] for r in rs]), "env_y1": summ([r["env_y1"] for r in rs]),
        "winners": {w: sum(1 for r in rs if r["winner"] == w) for w in sorted({r["winner"] for r in rs})},
    }


out = {"n_traces": len(rows), "by_tier": {}, "splits": {}}
tiers = ["trash", "champion", "mixed_pack", "boss"]
for t in tiers:
    out["by_tier"][t] = blk([r for r in rows if r["tier"] == t])
    for leg in LEGS:
        s = [r for r in rows if r["tier"] == t and r["leg"] == leg]
        if s: out["splits"][f"{t}::{leg}"] = blk(s)
for arm in ("A", "B"):
    s = [r for r in rows if r["tier"] == "boss" and r["arm"] == arm]
    out["splits"][f"boss::arm{arm}"] = blk(s)
out["nova"] = {"radii": sorted({round(x, 4) for r in rows for x in r["nova_r"]}),
               "count": sum(len(r["nova_r"]) for r in rows),
               "count_boss": sum(len(r["nova_r"]) for r in rows if r["tier"] == "boss"),
               "fights_with_nova": sum(1 for r in rows if r["nova_r"]),
               "boss_fights": sum(1 for r in rows if r["tier"] == "boss")}
json.dump(out, sys.stdout, indent=1)
