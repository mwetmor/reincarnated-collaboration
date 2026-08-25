#!/usr/bin/env python3
"""w2_castmix.py — per-slot cast census CONDITIONED ON CHANNEL-ACTIVE.

galadriel / visual-perception seam.  KC2 LIFT RUN, R-L5-1 / gamora's
`ABS-W2-CAST-MIX` honest-fail.  Both seats hit the same wall from opposite
directions: 0.15 = sum_s m_s * rate_s is ONE equation in THREE unknowns, and the
missing datum is the cast MIX -- specifically P(channel-active | cast) per slot,
because a cast made while the channel is not running cannot interrupt it and does
not belong in an interrupt rate's denominator.

Re-query of committed artefacts.  NO new footage, NO new capture.

ACTIVE(cast) := lag_into_gap_s <= W, i.e. the last energy drain tick preceding the
cast fell within W seconds of it.  Evaluated STRICTLY BEFORE the cast so it cannot
be contaminated by whatever silence the cast itself opens -- a forward-looking
definition would classify every interrupting cast as "channel inactive" and
manufacture the opposite answer.  W pre-registered at 0.35 s with sensitivity at
0.25 / 0.50 s.

  run <s2c-attrib.json> <out.json>
"""
from __future__ import annotations

import json
import sys

RATES = {"L": 0.385, "2": 0.136, "3": 0.000}     # MD-B4app-2c V2 per-slot rates
INCUMBENT = 0.15                                  # M-POL-2 row 7 uniform approximation
W_PRIMARY = 0.35
W_SENS = [0.25, 0.50]


def census(rows, W):
    slots = sorted({r["slot"] for r in rows})
    out = {}
    for s in slots:
        rs = [r for r in rows if r["slot"] == s]
        act = [r for r in rs if r["lag_into_gap_s"] is not None and r["lag_into_gap_s"] <= W]
        ai = [r for r in act if r.get("release_matched")]
        out[s] = {
            "n_cast": len(rs),
            "n_channel_active": len(act),
            "P_channel_active_given_cast": round(len(act) / len(rs), 4) if rs else None,
            "n_interrupt_all": sum(1 for r in rs if r.get("release_matched")),
            "n_interrupt_among_active": len(ai),
            "rate_unconditional": round(sum(1 for r in rs if r.get("release_matched")) / len(rs), 4) if rs else None,
            "rate_among_active": round(len(ai) / len(act), 4) if act else None,
        }
    return out


def run(path, out):
    d = json.load(open(path))
    rows = d["converse"]
    res = {"source": path, "window": d["window"], "n_casts": d["n_casts"],
           "per_slot_casts_as_filed": d["per_slot_casts"],
           "W_primary_s": W_PRIMARY, "definition":
               "ACTIVE(cast) := lag_into_gap_s <= W (last drain tick before the cast)",
           "by_W": {}}

    for W in [W_PRIMARY] + W_SENS:
        c = census(rows, W)
        n_all = sum(v["n_cast"] for v in c.values())
        n_act = sum(v["n_channel_active"] for v in c.values())
        mix_u = {s: round(v["n_cast"] / n_all, 4) for s, v in c.items()}
        mix_a = {s: round(v["n_channel_active"] / n_act, 4) for s, v in c.items()} if n_act else {}
        rec_u = sum(mix_u[s] * RATES.get(s, 0.0) for s in c)
        rec_a = sum(mix_a.get(s, 0.0) * RATES.get(s, 0.0) for s in c)
        # per-slot rates recomputed ON THE ACTIVE SUBSET, then remixed
        rec_a_own = sum(mix_a.get(s, 0.0) * (c[s]["rate_among_active"] or 0.0) for s in c)
        res["by_W"][str(W)] = {
            "per_slot": c,
            "n_casts_total": n_all, "n_casts_channel_active": n_act,
            "P_channel_active_pooled": round(n_act / n_all, 4),
            "mix_unconditional": mix_u,
            "mix_channel_active": mix_a,
            "sum_mix_x_publishedrate_unconditional": round(rec_u, 4),
            "sum_mix_x_publishedrate_activeMix": round(rec_a, 4),
            "sum_activeMix_x_activeRate": round(rec_a_own, 4),
            "incumbent_uniform": INCUMBENT,
        }
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
