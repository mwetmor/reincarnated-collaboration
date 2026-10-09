#!/usr/bin/env python3
"""§ 52 (c) snow-grain FORENSIC (jack-ryan painting Gate-2 § 2(b), H-3; REPORT-ONLY, 0 images, no bar).
Discriminates H-drift (wavefront drift by INHERITANCE along the paste chain) from H-prompt (the v7.1 wording).
On each RAW canvas (the painter's direct output), the P4 snow windows (64 px, >= 90 % snow, eroded mask, as P4) are split
into PASTE-STRIP windows (wholly inside the left / top 256-px context the stager handed it) and INTERIOR windows.
Per split: spectrum rms vs v1's pooled snow spectrum (the § 3 instrument), and the signed mean log-power deviation at
FINE periods (4-8 px) and COARSE periods (16-32 px). Chain: a child's strip from parent p vs p's own interior; depth =
wavefront index (ready rule: 1 + max(left, top, top-right); pilot = 0); Spearman of interior rms vs depth.
Old 3_3 (ledger af1cbd8cf583, read-only from its generated-images path) vs 3_3-r1.
  PH_SITE=1 site_snow_forensic.py -> results/site/snow_forensic.json"""
import os
import sys

import numpy as np
from scipy import ndimage, stats

os.environ["PH_SITE"] = "1"
sys.path.insert(0, os.path.dirname(__file__))
import pilot_harness as H  # noqa
from common import *  # noqa
import p4_texture as T
import p5v2 as V
import site_domain as SD

OLD33 = pathlib.Path("/Users/admin/.codex/generated_images/01a11f08-9c03-76a1-b98a-7396b6ea4766/exec-2ba54600-176f-4693-a8d0-59b6316335ca.png")
OLD33_SHA = "af1cbd8cf583addbc1b76b9ce62672ce3b11bcc6664aa0898a2c2cf328addfce"
PILOT = {"%d_%d" % (c, r) for c in range(3) for r in range(3)}


def wave():
    w = {k: 0 for k in PILOT}
    keys = ["%d_%d" % (c, r) for r in range(5) for c in range(5)]
    while len(w) < 25:
        for k in keys:
            if k in w:
                continue
            c, r = map(int, k.split("_"))
            nb = [n for n in ("%d_%d" % (c - 1, r), "%d_%d" % (c, r - 1), "%d_%d" % (c + 1, r - 1))
                  if 0 <= int(n.split("_")[0]) < 5 and 0 <= int(n.split("_")[1]) < 5]
            if all(n in w for n in nb):
                w[k] = 1 + max([w[n] for n in nb] or [0])
    return w


def spec_parts(gray, wins, ps):
    sp = T.spectrum_shape(gray, wins)
    if sp is None:
        return None
    d = np.array(sp) - ps
    return {"n": len(wins), "rms": round(float(np.sqrt(np.mean(d ** 2))), 3),
            "fine_dev_4_8px": round(float(d[6:].mean()), 3), "coarse_dev_16_32px": round(float(d[:3].mean()), 3)}


def split(img, m, key):
    """img: 1024 x 1536 canvas; m: its snow mask (eroded); returns {'strip_left','strip_top','interior','all'}"""
    c, r = map(int, key.split("_"))
    gray = luma(img)
    wins = T.windows(m)
    left, top, inner = [], [], []
    for (y, x) in wins:
        in_top = r > 0 and y + 64 <= 256
        in_left = c > 0 and x + 64 <= 256
        if in_top:
            top.append((y, x))
        elif in_left:
            left.append((y, x))
        elif (r > 0 and y < 256) or (c > 0 and x < 256):
            continue                                   # straddles the strip edge: neither
        else:
            inner.append((y, x))
    return gray, {"strip_left": left, "strip_top": top, "interior": inner, "all": wins}


def main():
    masks_v1, static_v1 = T.v1_classes()
    per = T.v1_pool(None, masks_v1, static_v1)
    _, ps = T.pooled(per, "snow")
    cls, names = H.class_map()
    ni = {n: i for i, n in enumerate(names)}
    snow = H.ground_mask() & ~H.tufts() & (cls == ni["snow"])
    wv = wave()
    raw = {k: V.load(SD.ART / v["canvas"]) for k, v in SD.CANV.items()}
    rows = {}
    for key, (x0, y0, x1, y1) in H.CHUNKS:
        m = ndimage.binary_erosion(snow[y0:y1, x0:x1], iterations=3)
        gray, sp = split(raw[key], m, key)
        row = {"wave": wv[key], "pilot": key in PILOT, "canvas": SD.CANV[key]["canvas"]}
        for nm, w in sp.items():
            row[nm] = spec_parts(gray, w, ps)
        rows[key] = row
    # old 3_3
    assert V.sha(OLD33) == OLD33_SHA, "old 3_3 sha mismatch"
    x0, y0, x1, y1 = dict(H.CHUNKS)["3_3"]
    m = ndimage.binary_erosion(snow[y0:y1, x0:x1], iterations=3)
    g, sp = split(V.load(OLD33), m, "3_3")
    old33 = {nm: spec_parts(g, w, ps) for nm, w in sp.items()}
    # chain pairs: child's strip from parent vs parent's interior
    pairs = []
    for key, row in rows.items():
        if row["pilot"]:
            continue
        c, r = map(int, key.split("_"))
        for side, par in (("strip_left", "%d_%d" % (c - 1, r)), ("strip_top", "%d_%d" % (c, r - 1))):
            if par in rows and row.get(side) and rows[par].get("interior") and row[side]["n"] >= 5 and rows[par]["interior"]["n"] >= 5:
                pairs.append({"child": key, "parent": par, "side": side, "parent_interior_rms": rows[par]["interior"]["rms"],
                              "child_strip_rms": row[side]["rms"], "child_interior_rms": (row["interior"] or {}).get("rms"),
                              "parent_interior_fine": rows[par]["interior"]["fine_dev_4_8px"],
                              "child_interior_fine": (row["interior"] or {}).get("fine_dev_4_8px")})
    p3 = [(k, r) for k, r in rows.items() if not r["pilot"] and r.get("interior") and r["interior"]["n"] >= 10]
    sp_depth = stats.spearmanr([r["wave"] for _, r in p3], [r["interior"]["rms"] for _, r in p3]) if len(p3) >= 4 else None
    pi = [(p["parent_interior_rms"], p["child_interior_rms"]) for p in pairs if p["child_interior_rms"] is not None]
    sp_chain = stats.spearmanr(*zip(*pi)) if len(pi) >= 4 else None
    pf = [(p["parent_interior_fine"], p["child_interior_fine"]) for p in pairs if p["child_interior_fine"] is not None]
    sp_fine = stats.spearmanr(*zip(*pf)) if len(pf) >= 4 else None
    strip_le_int = [(k, r["interior"]["rms"] >= max([r[s]["rms"] for s in ("strip_left", "strip_top") if r.get(s)] or [0]))
                    for k, r in rows.items() if not r["pilot"] and r.get("interior") and any(r.get(s) for s in ("strip_left", "strip_top"))]
    out = {"_what": "s52 (c) snow-grain forensic (REPORT-ONLY; Gate-2 s2(b)); raw canvases; v1 pooled snow spectrum reference",
           "v1_snow_spec_bar_context": 0.097, "chunks": rows, "old_3_3_af1cbd8cf583": old33, "chain_pairs": pairs,
           "spearman_interior_rms_vs_wave": None if sp_depth is None else {"rho": round(float(sp_depth[0]), 3), "p": round(float(sp_depth[1]), 4), "n": len(p3)},
           "spearman_parent_interior_vs_child_interior_rms": None if sp_chain is None else {"rho": round(float(sp_chain[0]), 3), "p": round(float(sp_chain[1]), 4), "n": len(pi)},
           "spearman_parent_vs_child_interior_fine_dev": None if sp_fine is None else {"rho": round(float(sp_fine[0]), 3), "p": round(float(sp_fine[1]), 4), "n": len(pf)},
           "interior_ge_strip": strip_le_int,
           "predictions": {"H-drift": "child tracks parent (rho > 0), interior >= strip, rms rising with wave",
                           "H-prompt": "no parent/child or wave dependence among v7.1-painted chunks"}}
    dump(out, str(PH / "results/site/snow_forensic.json"))
    for k, r in rows.items():
        f = lambda s: None if not r.get(s) else (r[s]["n"], r[s]["rms"], r[s]["fine_dev_4_8px"], r[s]["coarse_dev_16_32px"])
        print(k, "w%d" % r["wave"], "L", f("strip_left"), "T", f("strip_top"), "I", f("interior"), "all", f("all"))
    print("old 3_3", old33)
    for p in pairs:
        print(p)
    print("depth", out["spearman_interior_rms_vs_wave"], "chain", out["spearman_parent_interior_vs_child_interior_rms"], "fine", out["spearman_parent_vs_child_interior_fine_dev"])


if __name__ == "__main__":
    main()
