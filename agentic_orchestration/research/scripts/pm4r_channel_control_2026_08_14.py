#!/usr/bin/env python3
"""KC2-PM4 Lap R — B.3 ADDENDUM: the OCCUPANCY-CONDITIONED channel test.

⚑ DECLARED POST-HOC.  This instrument was NOT pre-registered.  It does NOT replace the
pre-registered B.3 verdict; it is published BESIDE it because the pre-registered rule carries a
confound the pre-registration did not anticipate, and naming the confound is worth more than
defending the rule.

THE CONFOUND: the pre-registered test compares player-outgoing-FCT presence during the 12 FASTEST
movement episodes against a stationary control.  A drop in FCT during fast relocation has TWO
possible causes and the pre-registered test cannot separate them:
    (i)  the channel stops when the player moves          <- what the test claims to measure
    (ii) there is simply nothing in reach while relocating <- a pure targeting effect

THE FIX: condition on OCCUPANCY.  The Lap H-2 nameplate census gives, at every instant, how many
living bodies sit inside the contact ring.  Restricting BOTH arms to instants with >= 1 body in
reach removes (ii) entirely, and what remains is (i).

Sample: the full dense 0.5 s pass (366 instants over the whole fight), not the 12-episode subset.
READ-ONLY.  OUTCOME-FIREWALLED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4r_lib_2026_08_14 import (                                             # noqa: E402
    LAPH2, OUT, K_GROUND, FIGHT_T0, FIGHT_T1, V_ON_PRIMARY, SMOOTH_FRAMES,
    ground_speed, rolling_median, classify, colour_class, parse_damage, p_out, sha256,
)

PLATES = OUT / "method" / "plates60_lapH2.npy"
DENSE = pathlib.Path("/tmp/pm4r/dense_ocr.tsv")
T0, DT = 683.0, 0.5
R_LIST = (150.0, 300.0)


def main():
    print("=" * 100)
    print("KC2-PM4 LAP R — B.3 ADDENDUM (DECLARED POST-HOC) — occupancy-conditioned channel test")
    print("=" * 100)

    # ── FCT presence per dense sample (the pre-registered P-OUT predicate, unchanged) ────────
    raw = [ln.rstrip("\n").split("\t") for ln in open(DENSE)]
    raw = [f for f in raw if len(f) >= 7]
    raw.sort(key=lambda f: f[0])
    cache, obs = {}, []
    for path, text, conf, bx, by, bw, bh in raw:
        bx, by, bw, bh = map(float, (bx, by, bw, bh))
        if not path.startswith("/"):
            path = str(pathlib.Path("/tmp/pm4r") / path)
        fi = int(pathlib.Path(path).stem[1:])
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
        obs.append(dict(frame=fi, t_sec=round(T0 + DT * fi, 3), text=text, cls=cls,
                        colour_class=colour_class(r, g), bbox_x=round(bx, 5), bbox_y=round(by, 5),
                        damage=parse_damage(text) if cls in ("crit", "bare", "crit_garbled") else None))
    frames = sorted({o["frame"] for o in obs})
    hits, _ = p_out(obs, len(frames))
    hitf = {h["frame"] for h in hits}

    # ── camera speed per dense sample ────────────────────────────────────────────────────────
    cam = np.load(LAPH2 / "method" / "camera_translation_60fps_683-866.npy")
    tt, vv = ground_speed(cam)
    vv = rolling_median(vv, SMOOTH_FRAMES)

    # ── plate occupancy per dense sample ─────────────────────────────────────────────────────
    R = np.load(PLATES)
    P = {}
    for r in R[R[:, 1] == 1]:
        if abs(r[2] - 960) < 50 and abs(r[3] - 429) < 16:
            P[round(r[0], 4)] = (r[2], r[3])
    M = R[R[:, 1] == 0]
    bym = {}
    for r in M:
        bym.setdefault(round(r[0], 4), []).append((r[2], r[3]))
    ptimes = np.array(sorted(P))

    rows = []
    for f in frames:
        t = round(T0 + DT * f, 3)
        if not (FIGHT_T0 <= t <= FIGHT_T1):
            continue
        i = int(np.argmin(np.abs(tt - t)))
        if abs(tt[i] - t) > 0.05:
            continue
        j = int(np.argmin(np.abs(ptimes - t)))
        tp = float(ptimes[j])
        if abs(tp - t) > 0.05:
            continue
        pl = P[round(tp, 4)]
        occ = {}
        for RC in R_LIST:
            occ[RC] = sum(1 for x, y in bym.get(round(tp, 4), ())
                          if np.hypot(x - pl[0], (y - pl[1]) / K_GROUND) <= RC)
        rows.append(dict(t=t, fct=int(f in hitf), speed=float(vv[i]),
                         moving=int(vv[i] >= V_ON_PRIMARY), **{f"occ{int(k)}": v
                                                               for k, v in occ.items()}))
    print(f"\n  joined samples (FCT x camera x plates, all within 0.05 s): {len(rows)}")

    res = {"n_samples": len(rows), "declared": "POST-HOC, not pre-registered; published beside "
                                               "the pre-registered B.3 verdict, not instead of it"}
    for RC in R_LIST:
        k = f"occ{int(RC)}"
        print(f"\n  --- conditioning on occupancy at R = {RC:.0f} ground px ---")
        print(f"    {'cell':<34} {'n':>5} {'FCT present':>12} {'rate':>8}")
        cells = {}
        for label, sel in (
            ("ALL moving", [r for r in rows if r["moving"]]),
            ("ALL stationary", [r for r in rows if not r["moving"]]),
            (">=1 body in reach & moving", [r for r in rows if r["moving"] and r[k] >= 1]),
            (">=1 body in reach & stationary", [r for r in rows if not r["moving"] and r[k] >= 1]),
            (">=2 bodies in reach & moving", [r for r in rows if r["moving"] and r[k] >= 2]),
            (">=2 bodies in reach & stationary", [r for r in rows if not r["moving"] and r[k] >= 2]),
            ("0 bodies in reach & moving", [r for r in rows if r["moving"] and r[k] == 0]),
            ("0 bodies in reach & stationary", [r for r in rows if not r["moving"] and r[k] == 0]),
        ):
            n = len(sel)
            h = sum(r["fct"] for r in sel)
            rate = h / n if n else float("nan")
            cells[label] = dict(n=n, n_fct=h, rate=round(rate, 5) if n else None)
            print(f"    {label:<34} {n:>5} {h:>12} {rate:>8.4f}")
        a = cells[">=1 body in reach & moving"]
        b = cells[">=1 body in reach & stationary"]
        if a["n"] and b["n"]:
            ratio = a["rate"] / b["rate"] if b["rate"] else float("nan")
            # Wilson 95 % CI on each rate
            def wilson(h, n, z=1.96):
                p = h / n
                d = 1 + z * z / n
                c = (p + z * z / (2 * n)) / d
                hw = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
                return round(c - hw, 4), round(c + hw, 4)
            ci_a, ci_b = wilson(a["n_fct"], a["n"]), wilson(b["n_fct"], b["n"])
            print(f"    -> conditioned ratio moving/stationary = {ratio:.4f}")
            print(f"       Wilson 95 % CI  moving {ci_a}   stationary {ci_b}   "
                  f"{'OVERLAP' if ci_a[1] >= ci_b[0] and ci_b[1] >= ci_a[0] else 'DISJOINT'}")
            cells["_conditioned_ratio"] = round(float(ratio), 5)
            cells["_wilson_moving"] = list(ci_a)
            cells["_wilson_stationary"] = list(ci_b)
            cells["_ci_overlap"] = bool(ci_a[1] >= ci_b[0] and ci_b[1] >= ci_a[0])
        res[f"R{int(RC)}"] = cells

    pathlib.Path("/tmp/pm4r/channel_control.json").write_text(json.dumps(res, indent=2, default=str))
    print("\nchannel_control.json written")


if __name__ == "__main__":
    main()
