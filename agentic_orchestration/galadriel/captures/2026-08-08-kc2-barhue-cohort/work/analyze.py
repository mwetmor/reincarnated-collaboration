#!/usr/bin/env python3
"""Per-fingerprint hue verdicts inside the fourth-extraction cohort windows."""
import json
import sys
from collections import defaultdict

import numpy as np

# fourth extraction § 1.1 / § 1.2: t0 and the cohort window END offset
WAVES = {151: (682.10, 5.97), 152: (698.38, 10.23), 153: (714.83, 8.60),
         157: (780.30, 8.63), 158: (799.43, 8.33)}


def load(w):
    return json.load(open(f"hue-w{w}.json"))["s"]


def cohort(w, full=False):
    t0, dur = WAVES[w]
    s = load(w)
    if full:
        return s
    return [x for x in s if t0 <= x["t"] <= t0 + dur]


def report(w, full=False):
    t0, dur = WAVES[w]
    s = cohort(w, full)
    per = defaultdict(lambda: {"v": defaultdict(int), "cur": set(), "t": [],
                               "box": [], "g": [], "r": []})
    for x in s:
        p = per[x["max"]]
        p["v"][x["hue"]] += 1
        if x["cur"] is not None:
            p["cur"].add(x["cur"])
        p["t"].append(x["t"])
        p["box"].append(x["box"])
        p["g"].append(x["g"])
        p["r"].append(x["r"])
    rows = []
    for mx, p in per.items():
        tot = sum(p["v"].values())
        kind = max(p["v"], key=p["v"].get)
        bx = np.array(p["box"])
        cx = (bx[:, 0] + bx[:, 2]) / 2
        cy = (bx[:, 1] + bx[:, 3]) / 2
        rows.append({
            "max": mx, "hue": kind, "n": tot,
            "purity": round(p["v"][kind] / tot, 3),
            "votes": dict(p["v"]),
            "t0": round(min(p["t"]) - t0, 2), "t1": round(max(p["t"]) - t0, 2),
            "ncur": len(p["cur"]),
            "curmin": min(p["cur"]) if p["cur"] else None,
            "curmax": max(p["cur"]) if p["cur"] else None,
            "xspan": int(cx.max() - cx.min()), "yspan": int(cy.max() - cy.min()),
            "modebox": max(set(map(tuple, p["box"])), key=list(map(tuple, p["box"])).count),
            "modebox_n": list(map(tuple, p["box"])).count(
                max(set(map(tuple, p["box"])), key=list(map(tuple, p["box"])).count)),
            "gmean": round(float(np.mean(p["g"])), 1),
            "rmean": round(float(np.mean(p["r"])), 1),
        })
    rows.sort(key=lambda r: r["t0"])
    return rows


if __name__ == "__main__":
    full = "--full" in sys.argv
    for w in [int(a) for a in sys.argv[1:] if a.isdigit()]:
        t0, dur = WAVES[w]
        print(f"\n===== WAVE {w}  t0={t0}  window +0.00..+{dur}"
              f"{'  [FULL CENSUS SPAN]' if full else ''} =====")
        print(f"{'max HP':>10} {'hue':>5} {'n':>4} {'pur':>5} "
              f"{'arr':>6} {'last':>6} {'ncur':>4} {'xsp':>4} {'ysp':>4} "
              f"{'modebox_n':>9}  {'g':>5} {'r':>5}  votes")
        for r in report(w, full):
            print(f"{r['max']:>10,} {r['hue']:>5} {r['n']:>4} {r['purity']:>5.2f} "
                  f"{r['t0']:>+6.2f} {r['t1']:>+6.2f} {r['ncur']:>4} "
                  f"{r['xspan']:>4} {r['yspan']:>4} {r['modebox_n']:>9}  "
                  f"{r['gmean']:>5.1f} {r['rmean']:>5.1f}  {dict(r['votes'])}")
