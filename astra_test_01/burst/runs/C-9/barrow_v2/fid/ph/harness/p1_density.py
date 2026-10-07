#!/usr/bin/env python3
"""P1 -- DISPLAYED TEXEL DENSITY on every static surface at the play camera.

The play camera shows PPM_V1 = 100.6176 screen px per metre (barrow_full.gd: cam.size = rows / PPM, any viewport).
A static surface's displayed ratio = PPM_V1 / (the px per metre of the painted SOURCE its texels come from):
  projection surfaces (ground, primitives): the painting frame's own ppm -- the number the projection shader is fed
      (g_frame / guide_window), i.e. literally the density the player is shown;
  baked models: min( source ppm at the instance's world scale , the bake texture's own seen-texel density ).
      v1 bakes come from the painting through the game camera: source ppm = the painting's ppm.
      R-C9-159 bakes come from 4-view model sheets: source ppm = sheet cell px_per_m (GLB-native metres)
      / the instance's scale (size / native AABB, geometric mean of the three axes, barrow_v2_sw.gd _place).
PASS: every surface ratio <= 1.05 (plan § 4 P1; v1's own value is 1.000 by construction -- the bar is v1 + 5%).
A surface that is MAGNIFIED on screen shows fewer painted texels than v1 everywhere it appears.
"""
import argparse
import glob
import math
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

BAR = 1.05


def v1_surfaces():
    L = jload(BF / "barrow_full_layout.json")["frame"]["guide_window"]
    W = L["px"][0]
    ppm_paint = W / (L["u"][1] - L["u"][0])
    out = [{"surface": "ground + 29 primitives (projection)", "kind": "projection", "source": "paint/barrow_full_painted.png",
            "source_ppm": ppm_paint}]
    br = jload(BF / "take/build/bake_report.json")
    for k, v in br["pieces"].items():
        seen = v["texels_on_mesh"] * (1 - v["unseen_before_fill_pct"] / 100.0)
        sil = v["surface"]["silhouette_px_in_cell"]
        tex_ppm = ppm_paint * math.sqrt(seen / max(sil, 1))       # texels per painted px, as linear density
        out.append({"surface": "bake " + k, "kind": "bake(painting)", "source": v["texture"],
                    "source_ppm": min(ppm_paint, tex_ppm), "painting_ppm": ppm_paint, "texture_seen_ppm": tex_ppm})
    return out


def v159_surfaces():
    lvl = jload(BF / "godot/data/barrow_v2_sw/level.json")
    sec = jload(BF / "godot/data/barrow_v2_sw/section.json")
    lay = jload(B2 / "layout_v2.json")
    F = lvl["frame"]["paint"]
    out = [{"surface": "ground (projection)", "kind": "projection", "source": "data/barrow_v2_sw/painted/ground.png",
            "source_ppm": float(F["ppm"])}]
    # instances per baked GLB (barrow_v2_sw.gd _build_placements, read not re-run)
    inst = {}
    for it in sec["instances"]["cliff"]:
        inst.setdefault("cliffplain", []).append(it["size"])
    for it in sec["instances"]["crag"]:
        inst.setdefault("crag", []).append(it["size"])
    inst.setdefault("cliffplain", []).append([5.0, 8.9, 3.2])                       # cliff_notch_v1cam
    inst["wreck2"] = [[17.0, 10.03, 6.42]]                                         # WRECK2 const
    co = sec["cave_override"]["size_m"]
    inst["cavecliff"] = [[co["w_local_x"], co["h"], co["d_local_z"]]]
    for m in lay["models"]:
        if m["id"] == "stair_cliff":
            s = m["size_m"]
            inst["staircliff"] = [[s["w_local_x"], s["h"], s["d_local_z"]]]
    for name, sizes in inst.items():
        cells = jload(BF / ("work/layout_v2sw_%s.json" % name))
        mn, mx = glb_aabb(B2 / cells["glb"])
        nat = mx - mn                                  # glTF: x, y(up), z
        br = jload(BF / ("work/bake_report_%s.json" % name))
        for i, sz in enumerate(sizes):
            sc = np.array(sz, float) / nat              # size given (w, h, d) = (x, y, z)
            s = float(np.prod(sc) ** (1 / 3))
            src = cells["px_per_m"] / s
            out.append({"surface": "bake %s #%d" % (name, i), "kind": "bake(4-view sheet)",
                        "source": "artifacts/BV2L-m-%s" % name, "source_ppm": src,
                        "sheet_ppm_native": cells["px_per_m"], "instance_scale_xyz": sc.round(3).tolist()})
    return out


def v158_surfaces():
    fr = jload(B2 / "paint/section_sw/frame_section_sw.json")
    return [{"surface": "everything static (projection of one painting)", "kind": "projection",
             "source": "paint/section_sw/section_sw_painted.png", "source_ppm": fr["px_per_m"]}]


def constructed():
    """v1 with its painting at HALF density over the same window (2688 x 1664 for 53.43 m): the raster a half-density
    paint would deliver. Declared from the raster size, not from a label."""
    s = v1_surfaces()
    L = jload(BF / "barrow_full_layout.json")["frame"]["guide_window"]
    half = (L["px"][0] // 2) / (L["u"][1] - L["u"][0])
    s[0] = dict(s[0], source="v1 painting resampled to 2688 x 1664 (constructed)", source_ppm=half)
    return s


def score(surfs):
    for s in surfs:
        s["ratio"] = PPM_V1 / s["source_ppm"]
        s["pass"] = s["ratio"] <= BAR
    worst = max(surfs, key=lambda s: s["ratio"])
    return {"value": round(worst["ratio"], 3), "worst_surface": worst["surface"],
            "n_surfaces": len(surfs), "n_fail": sum(not s["pass"] for s in surfs),
            "pass": all(s["pass"] for s in surfs), "threshold": "every static surface ratio <= %.2f" % BAR,
            "surfaces": surfs}


SETS = {"v1": v1_surfaces, "159": v159_surfaces, "158": v158_surfaces, "constructed": constructed}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="all")
    a = ap.parse_args()
    res = {k: score(f()) for k, f in SETS.items() if a.set in ("all", k)}
    for k, r in res.items():
        print("P1 %-12s worst ratio %.3f (%s)  fails %d/%d  -> %s" % (k, r["value"], r["worst_surface"], r["n_fail"],
                                                                    r["n_surfaces"], "PASS" if r["pass"] else "FAIL"))
    dump(res, str(PH / "results/p1.json"))
