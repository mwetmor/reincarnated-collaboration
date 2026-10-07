#!/usr/bin/env python3
"""W-4(2) (charter § 15.1): the MINIMUM PILOT WINDOW, in canvases on bv2art's 5 x 5 grid, that yields a 40-trial
content-controlled P11 ABX set for the home ground (start, ring, mere, barrow door).

Method -- the fixed generator's own selection logic (p11_abx.build, R-C9-171 fixes) run WITHOUT images:
  * v1 pool: the real v1 crops (p11_abx.crops_controlled on v1ref + PT's six HEAD stills).
  * candidate pool, per window: the painted window does not exist yet, so a crop's class comes from LV's class map
    (guide_art/class_art.png) and ID render (ids_art.png) at the same pixels (the guide is at play zoom, 100.6 px/m):
      excluded (build-specific, R-C9-171): any sea > 1 %, any char/ash/passage_dark > 1 %, any wreck / longhall /
        fallen_gable / cliff_faces id;
      snow = snow+mound+path >= 0.80 and shrub < 0.01; ice = ice+stream+shore_ice >= 0.40 and shrub < 0.01;
      heather = shrub >= 0.12 and snow-like >= 0.40 (the pixel classifier's thresholds, mapped to classes).
    Rock / standing stone / wood need a v1 class mask too, which v1's stills do not have: those classes cannot be
    class-matched and do not count.
  * the window is covered by play-camera stills (1920 x 1080, centre exclusion 30-66 % x 30-80 % as the generator),
    crops 256 px at stride 64, wholly inside the window; all candidate crops share one location space (absolute px).
  * the window must contain the home ground: the start (uv 0,0), every ring stone, the mere polygon, the barrow door.
Windows are tried in order of canvas count; the answer is the first with 40 trials AND 10 repeats (seed 168, as built).
  p11_window.py  -> results/p11_window_bv2art.json"""
import itertools
import math
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p11_abx as X
import p11_pairs as P

GA = FID / "lv/guide_art"
ART = FID / "lv/art"
CROP, STRIDE = P.CROP, P.STRIDE
SNOW_LIKE = ("snow", "mound", "path")
ICE_LIKE = ("ice", "stream", "shore_ice")
EXCL_CLS = ("char", "ash", "passage_dark")
EXCL_IDS = ("wreck", "longhall", "fallen_gable", "cliff_faces")


def class_and_ids():
    man = jload(GA / "guide_manifest.json")
    cls = np.asarray(Image.open(GA / "class_art.png"))
    names = man["class"]["classes"]
    a = np.asarray(Image.open(GA / "ids_art.png").convert("RGB")).astype(np.int32)
    ids = (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]
    excl_ids = [int(k) for k, v in man["id_table"].items() if v["id"] in EXCL_IDS]
    return cls, names, ids, excl_ids, man


def integral(m):
    return np.pad(m.astype(np.int64).cumsum(0).cumsum(1), ((1, 0), (1, 0)))


def box(ii, x, y, w=CROP, h=CROP):
    return int(ii[y + h, x + w] - ii[y, x + w] - ii[y + h, x] + ii[y, x])


def classify_cells(cls, names, ids, excl_ids):
    idx = {n: i for i, n in enumerate(names)}
    I = {}
    for grp in ("snow", "ice", "shrub", "sea", "excl"):
        if grp == "snow":
            m = np.isin(cls, [idx[n] for n in SNOW_LIKE])
        elif grp == "ice":
            m = np.isin(cls, [idx[n] for n in ICE_LIKE])
        elif grp == "shrub":
            m = cls == idx["shrub"]
        elif grp == "sea":
            m = cls == idx["sea"]
        else:
            m = np.isin(cls, [idx[n] for n in EXCL_CLS])
        I[grp] = integral(m)
    I["exid"] = integral(np.isin(ids, excl_ids))
    return I


def crop_class(I, x, y):
    A = CROP * CROP
    f = {k: box(v, x, y) / A for k, v in I.items()}
    if f["sea"] > 0.01 or f["excl"] > 0.01 or f["exid"] > 0:
        return None
    if f["shrub"] >= 0.12 and f["snow"] >= 0.40:
        return "heather"
    if f["shrub"] < 0.01 and f["snow"] >= 0.80:
        return "snow"
    if f["shrub"] < 0.01 and f["ice"] >= 0.40:
        return "ice"
    return None


def window_pool(I, rect):
    x0, y0, x1, y1 = rect
    W, H = x1 - x0, y1 - y0
    nx, ny = max(1, math.ceil(W / 1920)), max(1, math.ceil(H / 1080))
    fx = [x0 + (W - 1920) * i / max(nx - 1, 1) for i in range(nx)] if W > 1920 else [x0 + (W - 1920) / 2]
    fy = [y0 + (H - 1080) * j / max(ny - 1, 1) for j in range(ny)] if H > 1080 else [y0 + (H - 1080) / 2]
    seen = set()
    pool = []
    for sx in fx:
        for sy in fy:
            cx0, cx1, cy0, cy1 = sx + 0.30 * 1920, sx + 0.66 * 1920, sy + 0.30 * 1080, sy + 0.80 * 1080
            for y in range(int(sy) - int(sy) % STRIDE, int(sy + 1080 - CROP) + 1, STRIDE):
                for x in range(int(sx) - int(sx) % STRIDE, int(sx + 1920 - CROP) + 1, STRIDE):
                    if x < max(x0, sx) or y < max(y0, sy) or x + CROP > min(x1, sx + 1920) or y + CROP > min(y1, sy + 1080):
                        continue
                    if x < cx1 and x + CROP > cx0 and y < cy1 and y + CROP > cy0:
                        continue
                    if (x, y) in seen:
                        continue
                    seen.add((x, y))
                    k = crop_class(I, x, y)
                    if k:
                        pool.append({"src": "cand_window.png", "rect": [x, y, CROP, CROP], "class": k})
    return pool, {"stills": nx * ny}


def simulate(v1, cd, seed=168):
    """p11_abx.build's selection, verbatim in logic, no image I/O"""
    rng = np.random.default_rng(seed)
    by = lambda pool, k: [c for c in pool if c["class"] == k]
    classes = [k for k in X.ALLOWED if len(by(v1, k)) >= 2 and len(by(cd, k)) >= 2]
    if not classes:
        return 0, 0, {}
    w = np.array([min(len(by(v1, k)), len(by(cd, k))) for k in classes], float)
    w /= w.sum()
    used_v1, used_cd, used_x, trials = [], [], [], []
    xs = ["v1"] * (X.N_TRIALS // 2) + ["cand"] * (X.N_TRIALS // 2)
    rng.shuffle(xs)
    tries = 0
    while len(trials) < X.N_TRIALS and tries < 5000:
        tries += 1
        k = classes[rng.choice(len(classes), p=w)]
        a = X._pick(by(v1, k), rng, used_v1 + used_cd)
        b = X._pick(by(cd, k), rng, used_v1 + used_cd + [a] if a else used_cd, trial=(a,))
        if a is None or b is None:
            continue
        xsrc = xs[len(trials)]
        x = X._pick(by(v1, k) if xsrc == "v1" else by(cd, k), rng, used_x, X.X_OVERLAP, trial=(a, b))
        if x is None:
            continue
        used_v1.append(a)
        used_cd.append(b)
        used_x.append(x)
        trials.append({"class": k, "v1": a, "cand": b, "x": x, "x_from": xsrc})
    reps = 0
    rx = []
    for i in rng.permutation(len(trials)):
        if reps >= X.N_REPEAT:
            break
        t = trials[i]
        pool = by(v1, t["class"]) if t["x_from"] == "v1" else by(cd, t["class"])
        x2 = X._pick(pool, rng, used_x, X.X_OVERLAP, trial=(t["v1"], t["cand"], t["x"]))
        if x2 is None:
            continue
        used_x.append(x2)
        reps += 1
    from collections import Counter
    return len(trials), reps, dict(Counter(t["class"] for t in trials))


def home_ground(man):
    L = jload(ART / "layout_bv2art.json")
    env = man["envelope"]
    u0, v1 = env["u"][0], env["v"][1]
    px = lambda u, v, z=0.0: ((u - u0) * PPM_V1, (v1 - v) * 80.3076 - z * 60.6137)
    pts = {"start": [px(0.0, 0.0)]}
    ring = [p for p in L["placements"] if p["id"].startswith(("stone_", "fallen_stone"))]
    pts["ring"] = [px(*p["uv"], h) for p in ring for h in (0.0, p["size_m"]["h"])]
    pts["mere"] = [px(u, v) for u, v in L["regions"]["mere"]]
    door = next(o for o in jload(GA / "declared_openings.json")["openings"] if o["id"] == "barrow_door")
    pts["barrow_door"] = [tuple(door["centre_px"])] + [tuple(c) for c in door.get("corners_px", {}).values()]
    return pts, [p["id"] for p in ring]


def main():
    cls, names, ids, excl_ids, man = class_and_ids()
    I = classify_cells(cls, names, ids, excl_ids)
    v1 = [c for p in P.V1_STILLS if p.exists() for c in X.crops_controlled(p)]
    pts, ring_ids = home_ground(man)
    allp = [q for v in pts.values() for q in v]
    need = (min(q[0] for q in allp), min(q[1] for q in allp), max(q[0] for q in allp), max(q[1] for q in allp))
    cols, rows = man["cols"], man["rows"]
    cands = []
    for c0, c1 in itertools.combinations_with_replacement(range(cols), 2):
        for r0, r1 in itertools.combinations_with_replacement(range(rows), 2):
            rect = (1280 * c0, 768 * r0, 1280 * c1 + 1536, 768 * r1 + 1024)
            if rect[0] <= need[0] and rect[1] <= need[1] and rect[2] >= need[2] and rect[3] >= need[3]:
                cands.append(((c1 - c0 + 1) * (r1 - r0 + 1), (c0, c1, r0, r1), rect))
    cands.sort()
    rows_out = []
    answer = None
    for n, (c0, c1, r0, r1), rect in cands:
        pool, meta = window_pool(I, rect)
        t, rp, bycls = simulate(v1, pool)
        from collections import Counter
        r = {"canvases": n, "cols": [c0, c1], "rows": [r0, r1], "dims": "%dx%d" % (c1 - c0 + 1, r1 - r0 + 1), "rect_px": rect,
             "stills": meta["stills"], "cand_pool": dict(Counter(c["class"] for c in pool)), "trials": t, "repeats": rp, "by_class": bycls,
             "ok": t >= X.N_TRIALS and rp >= X.N_REPEAT}
        rows_out.append(r)
        print(r)
        if r["ok"] and answer is None:
            answer = r
        if answer and n > answer["canvases"]:
            break
    res = {"_what": "W-4(2): the minimum pilot window for a 40-trial content-controlled P11 (home ground), bv2art 5x5 grid",
           "home_ground_px_bbox": [round(v) for v in need], "ring_placements": ring_ids,
           "v1_pool": dict(__import__("collections").Counter(c["class"] for c in v1)), "windows_tried": rows_out, "minimum": answer,
           "caveat": "candidate classes come from the class map, not painted pixels; the painted pilot must be re-checked with "
                     "the real generator (UNDERPOWERED guard) before the judge"}
    dump(res, str(PH / "results/p11_window_bv2art.json"))
    print("MINIMUM:", answer)


if __name__ == "__main__":
    main()
