#!/usr/bin/env python3
"""P3 -- RENDERED-VS-PAINTING RESIDUAL, PER CLASS (Gate-1 W-7). The static surfaces as the game draws them, at the
painting's own camera and pixels, against the painting: mean per-channel |render - painting| (sRGB 0-255) inside
each class eroded 2 px (misregistration at a class edge is the neighbour's colour, not this class's error -- v1's
overlay_check.py rule, unchanged). Him absent, falling snow hidden, the wind held; the 3D heather's pixels excluded
(movers, P8/P9's business).

BAR (every class): <= 15.5 -- v1's unlit-bake residual, take/build/mini_overlay.json summary.unlit_mean_abs (the same
pieces worn LIT under the ramp read 40.7: "the painted light lit a second time", build_plan.md § 4, N-C9-PAINTED-
LIGHT-RULING). v1's own per-class values are reported beside it (its projected classes read ~0, its baked ~13-14).

Inputs per level -- a PH render directory:
  v1        renders/v1/guide_as_painted.png + heather_mask.png  (barrow_full/godot/tools/capture_painted.gd --guide
            --variants as_painted --quiet, v1's own tool, run read-only with --out under fid/ph); classes from v1's
            own instruments (ID render take/ids + step 3's ground layout; paint_world_prep id_index / tuft_classes)
  R-C9-159  renders/v159/render.png + hide_<group>.png (harness/godot/ph_capture.gd); classes: each model group by
            its |render - hide_<group>| silhouette (rock: cliffplain, crag, cavecliff, staircliff; wood: wreck2, log;
            v1-kit stones: cairn, stone_tall, stone_mid), less pixels that change in >= 3 groups' frames or lie on the
            painted SEA (+4 px) -- the animated water and floes differ frame to frame and are not the hidden model;
            ground classes from 159's own ground guide (snow / ice / shingle+cliff-back), sea excluded (DEV-5 water).
CONSTRUCTED FAILURE: v1's render RE-SHADED by its own painted light map (godot/data/painted/lit.bin, the painting's
direct-sun share) -- static pixels x (lit + (1 - lit) x v1's measured painter's shadow (0.4188, 0.5479, 0.8918),
linear): the dynamic sun darkening the painted shadow side a second time.
"""
import argparse
import importlib.util
import io
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

BAR = 15.5
SHADOW_MUL = np.array([0.4188, 0.5479, 0.8918])


def resid(R, P, m):
    m2 = ndimage.binary_erosion(m, iterations=2)
    if m2.sum() < 500:
        return None
    return {"px": int(m2.sum()), "mean_abs": round(float(np.abs(R[m2] - P[m2]).mean()), 2),
            "signed_rgb": np.round((R[m2] - P[m2]).mean(0), 1).tolist()}


def verdict(rows):
    vals = {k: v["mean_abs"] for k, v in rows.items() if v}
    worst = max(vals, key=vals.get) if vals else None
    return {"classes": rows, "worst_class": worst, "value": vals.get(worst), "bar": BAR,
            "pass": all(v <= BAR for v in vals.values()), "n_over": sum(v > BAR for v in vals.values())}


def _pw():
    spec = importlib.util.spec_from_file_location("pw_v1_readonly", BF / "tools/paint_world_prep.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def v1_masks(heather_mask=None):
    PW = _pw()
    P8 = np.asarray(Image.open(PW.PAINTING).convert("RGB"))
    H, W = P8.shape[:2]
    idx, table = PW.id_index()
    ground = idx == 0
    heather, shrub = PW.tuft_classes(P8, ground)
    tufts = ndimage.binary_opening(heather | shrub, iterations=1)
    GU = np.asarray(Image.open(BF / "take/ground/ground_uv.png"))
    if GU.ndim == 3:
        GU = GU[..., 0]
    ys, xs = np.mgrid[0:H, 0:W]
    uu, vv = PW.uv_of_px(xs + 0.5, ys + 0.5)
    gcls = GU[np.clip(((PW.V1 - vv) * 20).astype(int), 0, GU.shape[0] - 1), np.clip(((uu - PW.U0) * 20).astype(int), 0, GU.shape[1] - 1)]
    groups = {"stones (baked)": {"stone_tall", "stone_mid", "stone_short", "lintel", "post"},
              "kit + raven (baked)": {"cairn", "log", "shield", "raven"},
              "rock (projected)": {"outcrop", "shore_rock"}, "mound (projected)": {"mound"}, "birches (projected)": {"birch"}}
    M = {g: np.isin(idx, [k for k, v in table.items() if v["class"] in s]) for g, s in groups.items()}
    for code, nm in ((0, "ground: open snow"), (1, "ground: path"), (3, "ground: heather ground"), (4, "ground: ice")):
        M[nm] = ground & (gcls == code) & ~tufts
    if heather_mask is not None:
        for k in M:
            M[k] &= ~heather_mask
    return M


def v1_rows(render, P, M):
    return {k: resid(render, P, m) for k, m in M.items()}


def reshade(render, M):
    lit = np.asarray(Image.open(io.BytesIO(open(BF / "godot/data/painted/lit.bin", "rb").read())).convert("L"), np.float32) / 255.0
    lit = np.asarray(Image.fromarray((lit * 255).astype(np.uint8)).resize((render.shape[1], render.shape[0]), Image.BILINEAR), np.float32) / 255.0
    lin = srgb_to_lin(render)
    f = lit[..., None] + (1 - lit[..., None]) * SHADOW_MUL
    out = lin * f
    srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * np.clip(out, 0, None) ** (1 / 2.4) - 0.055) * 255
    static = np.zeros(render.shape[:2], bool)
    for m in M.values():
        static |= m
    R2 = render.copy()
    R2[static] = np.clip(srgb[static], 0, 255)
    return R2


def v159_rows(rdir):
    rdir = pathlib.Path(rdir)
    R = load_rgb(rdir / "render.png")
    P = load_rgb(BF / "godot/data/barrow_v2_sw/painted/ground.png")
    D = {}
    for hp in sorted(rdir.glob("hide_*.png")):
        D[hp.stem[5:]] = np.abs(R - load_rgb(hp)).sum(-1) > 6
    anim = sum(v.astype(int) for v in D.values()) >= 3
    gd = load_rgb(B2 / "section_v1cam/guide2/v2sw_guide.png")
    lab = rgb_to_lab(ndimage.gaussian_filter(gd, (4, 4, 0)))
    L, b = lab[..., 0], lab[..., 2]
    sea = ndimage.binary_dilation(L < 40, iterations=4)
    heather = D.pop("heather", np.zeros(R.shape[:2], bool))
    fam = {"rock (cliffplain, crag, cavecliff, staircliff bakes)": ("cliffplain", "crag", "cavecliff", "staircliff"),
           "wood (wreck2 bake, v1 log bake)": ("wreck2", "log"), "v1-kit stones (v1 bakes)": ("cairn", "stone_tall", "stone_mid")}
    M = {}
    model = np.zeros(R.shape[:2], bool)
    for nm, gs in fam.items():
        m = np.zeros(R.shape[:2], bool)
        for g in gs:
            if g in D:
                m |= D[g]
        m &= ~anim & ~sea
        m = ndimage.binary_opening(m, iterations=1)
        M[nm] = m
        model |= m
    rest = ~model & ~anim & ~sea & ~heather
    for nm, cm in (("ground: snow", (L >= 78) & (b >= -6)), ("ground: ice", (L >= 40) & (b < -6)),
                   ("ground: shingle + cliff back", (L >= 40) & (L < 78) & (b >= -6))):
        M[nm] = rest & cm
    return {k: resid(R, P, m) for k, m in M.items()}, M


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--v1", default=str(PH / "renders/v1"))
    ap.add_argument("--v159", default=str(PH / "renders/v159"))
    a = ap.parse_args()
    out = {"bar": BAR, "bar_source": "take/build/mini_overlay.json summary.unlit_mean_abs = %s (lit: %s)" % (
        jload(BF / "take/build/mini_overlay.json")["summary"]["unlit_mean_abs"], jload(BF / "take/build/mini_overlay.json")["summary"]["lit_mean_abs"])}
    v1r = pathlib.Path(a.v1) / "guide_as_painted.png"
    if v1r.exists():
        R = load_rgb(v1r)
        P = load_rgb(BF / "paint/barrow_full_painted.png")
        hm = np.asarray(Image.open(pathlib.Path(a.v1) / "heather_mask.png").convert("L")) > 20
        M = v1_masks(ndimage.binary_dilation(hm, iterations=2))
        out["v1"] = verdict(v1_rows(R, P, M))
        out["constructed_reshade"] = verdict(v1_rows(reshade(R, M), P, M))
    else:
        out["v1"] = {"pending": "renders/v1/guide_as_painted.png not yet captured"}
    if (pathlib.Path(a.v159) / "render.png").exists():
        rows, _ = v159_rows(a.v159)
        out["159"] = verdict(rows)
    rec = jload(BF / "take/build/overlay_check.json")["variants"]["as_painted"]["per_chunk"]
    agg = {}
    for ck, cls in rec.items():
        for c, v in cls.items():
            if isinstance(v, dict) and "mean_abs_diff" in v and v.get("px"):
                agg.setdefault(c, []).append((v["mean_abs_diff"], v["px"]))
    out["v1_recorded_overlay_check_as_painted"] = {c: round(sum(m * n for m, n in l) / sum(n for _, n in l), 2) for c, l in agg.items()}
    for k in ("v1", "159", "constructed_reshade"):
        if k in out and "classes" in out[k]:
            print("P3 %-20s worst %-48s %6.2f (bar %.1f, %d over) -> %s" % (k, out[k]["worst_class"], out[k]["value"], BAR,
                                                                          out[k]["n_over"], "PASS" if out[k]["pass"] else "FAIL"))
            for c, v in out[k]["classes"].items():
                if v:
                    print("      %-50s %6.2f  (%d px)" % (c, v["mean_abs"], v["px"]))
    print("v1 recorded (overlay_check.json as_painted, px-weighted):", out["v1_recorded_overlay_check_as_painted"])
    dump(out, str(PH / "results/p3.json"))
