#!/usr/bin/env python3
"""BV2F lane PT, Phase 2' (R-C9-191): bake every real model the pilot shows from the PILOT PAINTING, through the game
camera, with v1's own bake -- v1's tools/bake_heroes.py logic (barrow_full/tools/bake_heroes.py:25-90), copied, running
the FROZEN Tier-A tools unchanged via fid/v1tools/v1run.py against the pilot root (fid/pt/pilot/root):
  1. tierA/barrow_full/tools/hero_surface.py   -> root/work/surf_<id>.npz, layout_<id>.json (the plate's camera cell)
  2. tierA/barrow_full/tools/t5_06b_bake.py    -> root/work/bakes/<id>.png  (--sheet <id>:painting, --erode 2: v1's args)
  3. v1's numbers: self-test, unseen before / after the in-island fill, texels painted from an occluder.
DEV-19 (R-C9-194): each instance's texture SIZE is scaled to its silhouette's painted px -- v1's fixed 1024 under-samples
a silhouette up to 25x v1's largest. The frozen hero_surface.py takes --size (and t5_06b_bake.py reads the size from the
surface file), so this is USAGE of the frozen tools, not a patch: after a 1024 pass, an instance whose baked density
(PH p1_density: painting px/m x sqrt(seen texels / silhouette px)) is below the painting's is re-surfaced and re-baked at
the next power of two >= 1024 x ratio.
Writes fid/pt/pilot/bake_report.json (PH's P1 input).
    python3 fid/pt/tools/pt_bake.py
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = os.path.join(FID, "v1tools")
PILOT = os.path.join(FID, "pt", "pilot")
ROOT = os.path.join(PILOT, "root")
PAINT = os.path.join(PILOT, "painting.png")
RUN = [sys.executable, os.path.join(V, "v1run.py"), "--root", ROOT]


PPM = 100.617553710938


def surface_pass(size, only=None):
    a = RUN + ["tierA/barrow_full/tools/hero_surface.py", "--size", str(size)] + (["--only", ",".join(only)] if only else [])
    r = subprocess.run(a, cwd=ROOT, capture_output=True, text=True)
    open(os.path.join(ROOT, "work", "hero_surface_%d.log" % size), "w").write(r.stdout + r.stderr)
    if r.returncode != 0:
        sys.exit("hero_surface FAILED: " + r.stderr[-800:])
    return json.load(open(os.path.join(ROOT, "work", "surface_report.json")))


def main():
    subprocess.run(["bash", os.path.join(V, "verify.sh")], check=True)
    os.makedirs(os.path.join(ROOT, "work", "bakes"), exist_ok=True)
    surf = surface_pass(1024)
    ids = sorted(surf)
    sizes = {i: 1024 for i in ids}
    rep0 = bake_all(ids, surf, sizes)
    # DEV-19: the second pass, per instance
    up = {}
    for id_, v in rep0["pieces"].items():
        if v.get("bake") == "FAILED":
            continue
        seen = v["texels_on_mesh"] * (1 - v["unseen_before_fill_pct"] / 100.0)
        ratio = PPM / (PPM * math.sqrt(seen / max(v["surface"]["silhouette_px_in_cell"], 1)))
        if ratio > 1.0:
            up[id_] = 1024 * 2 ** int(math.ceil(math.log2(ratio)))
    for size in sorted(set(up.values())):
        group = [i for i, s in up.items() if s == size]
        s2 = surface_pass(size, group)
        for i in group:
            surf[i] = s2[i]
            sizes[i] = size
    rep = bake_all(ids, surf, sizes, only=list(up)) if up else rep0
    if up:
        for i in ids:
            if i not in up:
                rep["pieces"][i] = rep0["pieces"][i]
    rep["dev19_sizes"] = {i: sizes[i] for i in ids if sizes[i] != 1024}
    for i, v in rep["pieces"].items():
        if v.get("bake") != "FAILED":
            seen = v["texels_on_mesh"] * (1 - v["unseen_before_fill_pct"] / 100.0)
            v["texture_px"] = sizes[i]
            v["baked_ppm_seen"] = round(PPM * math.sqrt(seen / max(v["surface"]["silhouette_px_in_cell"], 1)), 1)
    ok = [v for v in rep["pieces"].values() if v.get("bake") != "FAILED"]
    rep["summary"] = {"baked": len(ok), "failed": [k for k, v in rep["pieces"].items() if v.get("bake") == "FAILED"],
                      "unseen_after_fill_pct_median": round(float(np.median([v["unseen_after_fill_pct"] for v in ok])), 2) if ok else None,
                      "unseen_after_fill_pct_max": round(float(max(v["unseen_after_fill_pct"] for v in ok)), 2) if ok else None,
                      "min_baked_ppm_seen": min(v["baked_ppm_seen"] for v in ok)}
    json.dump(rep, open(os.path.join(PILOT, "bake_report.json"), "w"), indent=1)
    print("baked %d of %d; DEV-19 sizes %s; min baked ppm (seen) %.1f" % (len(ok), len(ids), rep["dev19_sizes"], rep["summary"]["min_baked_ppm_seen"]))


def bake_all(ids, surf, sizes, only=None):
    rep = {"_what": "BV2F PT pilot: every real model in the pilot window baked from the pilot painting with v1's t5_06b_bake (frozen, Tier A)",
           "bake_script": "fid/v1tools/tierA/barrow_full/tools/t5_06b_bake.py (sha in SHA256SUMS; = v1 barrow_full/tools/t5_06b_bake.py)",
           "texture_px": "per instance (DEV-19): see pieces.<id>.texture_px", "pieces": {}}
    for id_ in (only or ids):
        out = os.path.join(ROOT, "work", "bakes", "%s.png" % id_)
        r = subprocess.run(RUN + ["tierA/barrow_full/tools/t5_06b_bake.py", os.path.join("work", "surf_%s.npz" % id_), out,
                                  "--sheet", "%s:%s" % (id_, PAINT), "--erode", "2"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            rep["pieces"][id_] = {"surface": surf[id_], "bake": "FAILED", "stderr": r.stderr[-600:]}
            print("%-34s BAKE FAILED: %s" % (id_, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "?"))
            continue
        br = json.load(open(os.path.join(ROOT, "work", "bake_report_%s.json" % id_)))
        S = np.load(os.path.join(ROOT, "work", "surf_%s.npz" % id_))
        on = int((S["tex_tri"] >= 0).sum())
        L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % id_)))["cells"]["guide"]
        x0, y0, w, h = L["rect"]
        al = np.array(Image.open(os.path.join(ROOT, "work", "_cells_%s" % id_, "cell_guide.png")).convert("RGBA"))[:, :, 3]
        painted = np.array(Image.open(out.replace(".png", "_mask.png")))[::-1] > 0
        yy, xx = np.where(painted & (S["tex_tri"] >= 0))
        pw = S["tex_pos"][yy, xx].astype(np.float64)
        px = np.round((pw - L["aim"]) @ np.array(L["screen_right"]) * L["px_per_m"] + w / 2.0).astype(int)
        py = np.round(h / 2.0 - (pw - L["aim"]) @ np.array(L["screen_up"]) * L["px_per_m"]).astype(int)
        occ = int((al[np.clip(py, 0, h - 1), np.clip(px, 0, w - 1)] == 96).sum())
        test = [ln for ln in r.stdout.splitlines() if "self-test" in ln]
        rep["pieces"][id_] = {
            "surface": surf[id_],
            "self_test": test[0].split("self-test")[-1].strip() if test else "?",
            "texels_on_mesh": on,
            "unseen_before_fill_pct": br["unseen_pct"],
            "unseen_after_fill_pct": round(100.0 * br["still_bare"] / max(on, 1), 3),
            "filled_in_island": br["filled"], "islands": br["islands"],
            "painted_from_an_occluder_pct": round(100.0 * occ / max(on, 1), 3),
            "silhouette_px_in_cell": surf[id_].get("silhouette_px_in_cell"),
            "texture": os.path.relpath(out, FID)}
        print("%-34s self-test %-40s unseen %6.2f%% -> %6.2f%%  occluder %.2f%%" % (
            id_, rep["pieces"][id_]["self_test"][:40], br["unseen_pct"], rep["pieces"][id_]["unseen_after_fill_pct"],
            rep["pieces"][id_]["painted_from_an_occluder_pct"]))
    return rep


main()
