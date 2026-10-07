#!/usr/bin/env python3
"""C-9 T10-2 step 4 -- THE PAINTED BARROW'S DATA: everything the scene wears, read off the painting
and measured, into godot/data/painted/ (raw PNG/float bytes named .bin, sha256 in manifest.json).

    python3 tools/paint_world_prep.py

Reads the accepted paint-over (sha256 eecb42661af490dd...), work/light/lit_guide.png (the blockout
re-rendered as its own light, tools/capture_light.gd), take/ (step 3), take/build/ (step 4 B) and
work/bakes/ (step 4 B). Writes:
  painting.bin          the painting's own PNG bytes, unchanged: the primitives, mound, birches
  ground_inpainted.bin  the painting with the TUFTS THE 3D HEATHER REPLACES taken out of the ground
                        (push-pull fill), so a spray pushed aside by him leaves no painted twin
  lit.bin               the painting's direct-sun share (lit_guide R), half resolution, 8-bit
  bakes/<id>.bin        the 25 real models' bakes (work/bakes/<id>.png), unchanged
  heather.json          the 977 instances: [x, z, height_m, class, mul r, g, b] -- mul is the
                        painting beneath the spray over the mean of all of them (linear)
  snow_grid.bin         the snow's depth multiplier and trodden amount on a 0.1 m grid over the
                        field, from the painted splat (float32: all mul, then all trod)
  manifest.json         every file's sha256, the measured shadow multiplier, the field's frame
and take/build/painted_prep.json: the measurements (the painter's shadow against the render's;
the tuft self-test against step 3; the inpaint; the heather colours; the snow grid).
"""
import hashlib
import json
import math
import os
import shutil

import numpy as np
from PIL import Image
from scipy import ndimage

# BV2F Tier-B (fid/v1tools/ALLOWLIST.md): frame + painting from $BV2F_FRAME_GRID; unset = v1's own values.
_FG = json.load(open(os.environ["BV2F_FRAME_GRID"])) if os.environ.get("BV2F_FRAME_GRID") else {}   # BV2F
BF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAINTING = os.path.join(BF, _FG.get("painting", os.path.join("paint", "barrow_full_painted.png")))   # BV2F Tier-B
PAINT_SHA_PREFIX = _FG.get("painting_sha_prefix", "eecb42661af490dd")   # BV2F Tier-B
LIT = os.path.join(BF, "work", "light", "lit_guide.png")
OUT = os.path.join(BF, "godot", "data", "painted")
TAKE = os.path.join(BF, "take")
L = json.load(open(os.path.join(BF, "godot", "data", "barrow_full_layout.json")))
GW = L["frame"]["guide_window"]
U0, V1 = GW["u"][0], GW["v"][1]
W, H = GW["px"]
PPM = float(_FG.get("px_per_m_across", 100.617553710938))   # BV2F Tier-B
PITCH = math.radians(float(_FG.get("pitch_deg", 52.95354112560294)))   # BV2F Tier-B
PXV, PXH = PPM * math.sin(PITCH), PPM * math.cos(PITCH)
C47, S47 = math.cos(math.radians(float(_FG.get("yaw_deg", 47.0)))), math.sin(math.radians(float(_FG.get("yaw_deg", 47.0))))   # BV2F Tier-B (name kept: v1 yaw 47)
# the installed Barrow's snow per ground class (barrow_world.SNOW_BY_CLASS), unchanged
SNOW_BY_CLASS = {"snow": (1.00, 0.00, 0.00), "path": (0.36, 0.12, 0.85), "rock": (0.45, 0.46, 0.00),
                 "heather": (0.22, 0.70, 0.00), "ice": (0.00, 0.00, 0.00)}
HEATHER_STEM_MUL = (1.622, 1.254, 0.534)     # the installed Barrow's stem grade: the first guess
# THE SPRAYS' ONE GRADE, calibrated by the overlay check on the pixels both the render and the
# painting call heather (tools/overlay_check.py "colour_on_both_linear": painting over render)
# pass 1 (the installed grade, 1.622/1.254/0.534): the sprays' own colour 0.366/0.152/0.051
# against the painted tufts beneath them 0.282/0.123/0.054 -> x 0.7715/0.8059/1.0631
HEATHER_ALBEDO_MUL = (round(1.622 * 0.7715, 4), round(1.254 * 0.8059, 4), round(0.534 * 1.0631, 4))
HEATHER_ALBEDO_MUL_WHY = ("the installed Barrow's stem grade (1.622, 1.254, 0.534) x the overlay check's first "
                          "calibration (0.7715, 0.8059, 1.0631): the sprays' own colour onto the painted tufts beneath them")


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def l2s(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def uv_of_px(x, y, h=0.0):
    return U0 + x / PPM, V1 - (y + h * PXH) / PXV


def px_of_uv(u, v, h=0.0):
    return (u - U0) * PPM, (V1 - v) * PXV - h * PXH


def xz_of_uv(u, v):
    return u * C47 - v * S47, -u * S47 - v * C47


def _up2(a, shape):
    """Bilinear x2 upsampling to `shape` (pixel centres aligned): a nearest repeat here is what
    made the first fill BLOCKY -- 8 px squares of one colour in every large hole."""
    h, w = shape
    ys = (np.arange(h) + 0.5) / 2.0 - 0.5
    xs = (np.arange(w) + 0.5) / 2.0 - 0.5
    y0 = np.clip(np.floor(ys).astype(int), 0, a.shape[0] - 1)
    x0 = np.clip(np.floor(xs).astype(int), 0, a.shape[1] - 1)
    y1 = np.clip(y0 + 1, 0, a.shape[0] - 1)
    x1 = np.clip(x0 + 1, 0, a.shape[1] - 1)
    ty = np.clip(ys - np.floor(ys), 0, 1)[:, None, None]
    tx = np.clip(xs - np.floor(xs), 0, 1)[None, :, None]
    top = a[y0][:, x0] * (1 - tx) + a[y0][:, x1] * tx
    bot = a[y1][:, x0] * (1 - tx) + a[y1][:, x1] * tx
    return top * (1 - ty) + bot * ty


def push_pull(img, known):
    """Fill the unknown pixels from the known ones: a pyramid of weighted means down (push), then
    each level's holes filled from the coarser one, upsampled bilinearly (pull). Smooth, and no seam
    at the hole's edge -- the known pixels are never touched."""
    levels = []
    c = img * known[..., None]
    w = known.astype(np.float64)
    while min(w.shape) > 4:
        levels.append((c, w))
        h2, w2 = (w.shape[0] + 1) // 2 * 2, (w.shape[1] + 1) // 2 * 2
        cp = np.zeros((h2, w2, 3)); wp = np.zeros((h2, w2))
        cp[:c.shape[0], :c.shape[1]] = c; wp[:w.shape[0], :w.shape[1]] = w
        c = cp.reshape(h2 // 2, 2, w2 // 2, 2, 3).sum((1, 3))
        w = wp.reshape(h2 // 2, 2, w2 // 2, 2).sum((1, 3))
    fill = c / np.maximum(w, 1e-9)[..., None]
    for c, w in reversed(levels):
        up = _up2(fill, w.shape)
        mine = c / np.maximum(w, 1e-9)[..., None]
        a = np.clip(w, 0.0, 1.0)[..., None]
        fill = mine * a + up * (1.0 - a)
    return np.where(known[..., None], img, fill)


def tuft_classes(P8, ground):
    """Step 3's tuft classifier (take_from_paint.py (b)), verbatim: rust heather and dark shrub."""
    f = P8.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    lum = f.mean(-1)
    sat = (f.max(-1) - f.min(-1)) / np.maximum(f.max(-1), 1.0)
    heather = (r > g) & (g > b) & (r - b > 42) & (sat > 0.24) & (lum < 212) & ground
    shrub = (lum < 128) & (b < r + 6) & (g >= r - 12) & ~heather & ground
    return heather, shrub


def id_index():
    """The ID render's placement index per pixel (0 = ground), and the index -> placement table."""
    IDS = json.load(open(os.path.join(TAKE, "ids", "ids.json")))
    ID8 = np.asarray(Image.open(os.path.join(TAKE, "ids", "ids.png")).convert("RGB")).astype(np.int32)
    is_pl = ID8[..., 2] > 100
    idx = np.where(is_pl, np.clip(np.round((ID8[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
                   + np.clip(np.round((ID8[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
    return idx, {int(k): v for k, v in IDS["placements"].items()}


def main():
    os.makedirs(os.path.join(OUT, "bakes"), exist_ok=True)
    sha = sha_file(PAINTING)
    assert sha.startswith(PAINT_SHA_PREFIX), "not the accepted paint-over: %s" % sha[:16]
    P8 = np.asarray(Image.open(PAINTING).convert("RGB"))
    assert P8.shape[:2] == (H, W)
    Plin = s2l(P8.astype(np.float64) / 255.0)
    rep = {"_what": "C-9 T10-2 step 4: the painted Barrow's data, measured (tools/paint_world_prep.py)",
           "painting_sha256": sha}
    man = {"_what": "what the painted Barrow wears (godot/data/painted/), every file's sha256 -- the scene checks each one as it loads it",
           "painting": {}, "bakes": {}}

    # ---- the ID render: which pixel is ground, which a piece (step 3's own decode) ----------------
    idx, _ = id_index()
    ground = idx == 0

    # ---- the tufts: step 3's classifier, re-run, and checked against step 3's own counts --------
    heather, shrub = tuft_classes(P8, ground)
    T3 = json.load(open(os.path.join(TAKE, "take_report.json")))["tufts"]
    rep["tufts_self_test"] = {"heather_px": [int(heather.sum()), T3["heather_px"]], "shrub_px": [int(shrub.sum()), T3["shrub_px"]],
                              "PASS": int(heather.sum()) == T3["heather_px"] and int(shrub.sum()) == T3["shrub_px"],
                              "_": "[this run, step 3's take_report] -- the same classifier on the same painting"}
    assert rep["tufts_self_test"]["PASS"], rep["tufts_self_test"]
    tuft_px = ndimage.binary_opening(heather | shrub, iterations=1)

    # ---- the painting's light: lit_guide.png, decoded --------------------------------------------
    LG = s2l(np.asarray(Image.open(LIT).convert("RGB")).astype(np.float64) / 255.0)
    assert LG.shape[:2] == (H, W)
    castG, ndlB = LG[..., 1], LG[..., 2]
    # THE DIRECT SUN, AS A SHARE OF FLAT SUNLIT GROUND'S: the cast shadow times N.L over flat ground's
    # N.L (sin 55). Not the ramp's band (R): flat sunlit snow sits at 0.82 of the band's range there
    # (the band edge is placed just above flat ground, on purpose), and his shadow must darken flat
    # sunlit snow by the WHOLE painted shadow, a flank by part of it, a face turned away by none.
    litR = castG * np.clip(ndlB / math.sin(math.radians(55.0)), 0.0, 1.0)

    # ---- ground classes, per guide pixel (step 3's ground_uv raster, 20 px/m) --------------------
    GU = np.asarray(Image.open(os.path.join(TAKE, "ground", "ground_uv.png")))
    if GU.ndim == 3:
        GU = GU[..., 0]
    gu_meta = json.load(open(os.path.join(TAKE, "take_report.json")))["ground"]
    gpx = gu_meta["px_per_m"]
    ys, xs = np.mgrid[0:H, 0:W]
    uu, vv = uv_of_px(xs + 0.5, ys + 0.5)
    gi = np.clip(((uu - U0) * gpx).astype(int), 0, GU.shape[1] - 1)
    gj = np.clip(((V1 - vv) * gpx).astype(int), 0, GU.shape[0] - 1)
    gcls = GU[gj, gi]
    snow_open = ground & (gcls == 0)

    # ---- THE PAINTER'S SHADOW, measured: open snow in the render's cast shadow against open snow
    # in full sun, away from the pieces and the tufts (the painting's blue dabs are texture, in both)
    clear = snow_open & ~ndimage.binary_dilation(tuft_px | ~ground, iterations=12)
    sh_set = clear & (castG < 0.08) & (litR < 0.08)
    lt_set = clear & (castG > 0.98) & (litR > 0.98)
    med_sh = np.median(Plin[sh_set], axis=0)
    med_lt = np.median(Plin[lt_set], axis=0)
    mul = med_sh / med_lt
    # per chunk, to show it is one colour and not a regional accident
    per_chunk = {}
    for ch in L["frame"]["chunks"]["list"]:
        x0, y0, x1, y1 = ch["px"]
        a = sh_set[y0:y1, x0:x1]
        bm = lt_set[y0:y1, x0:x1]
        if a.sum() > 2000 and bm.sum() > 2000:
            per_chunk[ch["key"]] = [round(float(v), 3) for v in
                                    np.median(Plin[y0:y1, x0:x1][a], axis=0) / np.median(Plin[y0:y1, x0:x1][bm], axis=0)]
    # AND WHERE THE PAINTER PUT THEM: each open-snow pixel's position on the lit -> shadow axis,
    # smoothed past the dabs (a 21 px median), against the render's cast shadow. RECALL is the
    # question (is every shadow he will be darkened in painted as one?); precision is low by
    # construction -- the painter's snow is washed with blue hollows no object casts
    ax = med_sh - med_lt
    s = ((Plin - med_lt) @ ax) / float(ax @ ax)
    s = ndimage.median_filter(s.astype(np.float32), size=21)
    painted_sh = (s > 0.5) & snow_open
    render_sh = (castG < 0.5) & snow_open
    inter = float((painted_sh & render_sh).sum())
    union = float((painted_sh | render_sh).sum())
    near = float((painted_sh & ndimage.binary_dilation(render_sh, iterations=10)).sum())
    rep["shadow"] = {
        "painted_shadow_over_painted_light_linear": [round(float(v), 4) for v in mul],
        "as_srgb_on_lit_snow": {"lit": [int(round(float(v) * 255)) for v in l2s(med_lt)],
                                "shadow": [int(round(float(v) * 255)) for v in l2s(med_sh)]},
        "pixels": {"shadow": int(sh_set.sum()), "lit": int(lt_set.sum())},
        "per_chunk_linear": per_chunk,
        "painted_vs_rendered_shadow_on_open_snow": {
            "recall_rendered_shadow_painted_as_shadow": round(inter / max(float(render_sh.sum()), 1.0), 4),
            "precision": round(inter / max(float(painted_sh.sum()), 1.0), 4), "iou": round(inter / max(union, 1.0), 4),
            "painted_shadow_within_10px_of_a_rendered_one": round(near / max(float(painted_sh.sum()), 1.0), 4),
            "painted_px": int(painted_sh.sum()), "rendered_px": int(render_sh.sum()),
            "_read": "recall: the share of the render's cast shadow the painter painted as shadow -- where the SUN's real shadow will darken him; the rest of the painted blue is the snow's own washes (hollows, dabs), which no object casts",
            "_instrument": "painted: a pixel's position on the lit->shadow colour axis > 0.5 after a 21 px median; rendered: the blockout's own cast shadow (lit_guide G < 0.5); open snow only"},
        "_use": "his shadow on the painted world = this multiplier (PaintedWorld.shadow_mul), where the painting shows sun (lit.bin)"}
    man["shadow_mul"] = {"linear": [round(float(v), 4) for v in mul], "_": "measured: the painting's shadowed open snow over its sunlit open snow (median, linear)"}

    # ---- the painting, as is ------------------------------------------------------------------
    shutil.copyfile(PAINTING, os.path.join(OUT, "painting.bin"))
    man["painting"] = {"file": "painting.bin", "sha256": sha, "px": [W, H], "_": "the accepted paint-over's own PNG bytes"}
    man["ground_as_painted"] = dict(man["painting"])

    # ---- the ground, the tufts taken out ------------------------------------------------------
    hole = ndimage.binary_dilation(tuft_px, iterations=2) & ground
    # THE DONORS ARE GROUND: a hole beside a rock must not fill with the rock's colour (the first
    # fill bled grey rock into every tuft at a rock's foot)
    filled = np.where(hole[..., None], push_pull(Plin, ground & ~hole), Plin)
    G8 = (l2s(filled) * 255.0 + 0.5).astype(np.uint8)
    gp = os.path.join(OUT, "ground_inpainted.bin")
    Image.fromarray(G8, "RGB").save(gp, format="PNG", compress_level=6)
    man["ground_inpainted"] = {"file": "ground_inpainted.bin", "sha256": sha_file(gp), "px": [W, H],
                               "_": "the painting with the tufts the 3D heather replaces filled from the ground round them"}
    rep["inpaint"] = {"px": int(hole.sum()), "share_of_ground": round(float(hole[ground].mean()), 4),
                      "method": "push-pull pyramid fill (bilinear pull; donors: ground pixels only; known pixels untouched), linear light; the tuft mask dilated 2 px for its ink"}

    # ---- the light map, half resolution ---------------------------------------------------------
    lr = litR.reshape(H // 2, 2, W // 2, 2).mean((1, 3))
    lp = os.path.join(OUT, "lit.bin")
    Image.fromarray((np.clip(lr, 0, 1) * 255.0 + 0.5).astype(np.uint8), "L").save(lp, format="PNG")
    man["lit"] = {"file": "lit.bin", "sha256": sha_file(lp), "px": [W // 2, H // 2],
                  "_": "the painting's direct sun as a share of flat sunlit ground's: lit_guide G x min(B / sin 55, 1), 8-bit, half resolution"}

    # ---- the 25 bakes ---------------------------------------------------------------------------
    BR = json.load(open(os.path.join(TAKE, "build", "bake_report.json")))
    ids = sorted(BR["pieces"].keys()) if "pieces" in BR else sorted(
        k for k in BR if isinstance(BR[k], dict) and "unseen_after_fill" in json.dumps(BR[k]))
    for pid in ids:
        src = os.path.join(BF, "work", "bakes", "%s.png" % pid)
        dst = os.path.join(OUT, "bakes", "%s.bin" % pid)
        shutil.copyfile(src, dst)
        man["bakes"][pid] = {"file": "bakes/%s.bin" % pid, "sha256": sha_file(dst)}
    rep["bakes"] = len(man["bakes"])
    assert len(man["bakes"]) == 25, len(man["bakes"])

    # ---- the heather: the 954 + 23 sprays, ON the painted tufts, each coloured by the tufts under it
    # step 4 B placed them by DENSITY (a jittered grid, keep probability from the tuft cover): right
    # in number and in mean cover, and the overlay check (step 5, first pass) measured what that
    # means pixel by pixel -- 39% of the drawn heather landed on a painted tuft, the rest on snow
    # beside it, where a spiky spray reads as a second plant. So the same counts are re-placed by
    # GREEDY COVER: each spray where its screen footprint covers the most painted tuft not yet
    # covered (4 px cells), the shrub's 23 on the juniper first, then the heather's 954.
    HI = json.load(open(os.path.join(TAKE, "build", "heather_instances.json")))
    cs = 4
    Hc, Wc = H // cs, W // cs
    def cells(m):
        return m[:Hc * cs, :Wc * cs].reshape(Hc, cs, Wc, cs).mean((1, 3))
    rows, cols, counts = [], [], []
    placed_px = {}
    remaining = {"heather": cells(heather & tuft_px), "shrub": cells(shrub & tuft_px)}
    for ci, cls in ((1, "shrub"), (0, "heather")):
        c = HI["classes"][cls]
        hgt = float(c["height_m"])
        n_want = int(c["count"])
        # the spray's screen footprint (BarrowHeather.spray_mesh at this height: LOW AND WIDE,
        # ~1.55x its height across -- ~0.47 m at 0.30): an ellipse ~23 x 22 px at 0.30 m
        rx = 0.78 * hgt * PPM
        ry = 0.5 * (hgt * PXH + 1.55 * hgt * PXV)
        R = remaining[cls].copy()
        kx, ky = max(int(round(2 * rx / cs)), 1), max(int(round(2 * ry / cs)), 1)
        ex, ey = rx / cs, ry / cs
        got = 0
        while got < n_want:
            score = ndimage.uniform_filter(R, size=(ky, kx), mode="constant")
            j, i = np.unravel_index(int(np.argmax(score)), score.shape)
            if score[j, i] <= 1e-6:
                break
            y0, y1 = max(int(j - ey), 0), min(int(j + ey) + 1, Hc)
            x0, x1 = max(int(i - ex), 0), min(int(i + ex) + 1, Wc)
            yy, xx = np.mgrid[y0:y1, x0:x1]
            ell = ((xx - i) / ex) ** 2 + ((yy - j) / ey) ** 2 <= 0.8 ** 2
            R[y0:y1, x0:x1][ell] = 0.0
            cx, cy = (i + 0.5) * cs, (j + 0.5) * cs
            u, v = uv_of_px(cx, cy, hgt * 0.5)
            x, z = xz_of_uv(u, v)
            # the colour: the painted tufts under the footprint (full resolution), linear
            X0, X1 = int(max(cx - rx, 0)), int(min(cx + rx + 1, W))
            Y0, Y1 = int(max(cy - ry, 0)), int(min(cy + ry + 1, H))
            YY, XX = np.mgrid[Y0:Y1, X0:X1]
            fel = ((XX + 0.5 - cx) / rx) ** 2 + ((YY + 0.5 - cy) / ry) ** 2 <= 1.0
            tm = fel & tuft_px[Y0:Y1, X0:X1]
            if tm.sum() < 12:
                tm = fel & ground[Y0:Y1, X0:X1]
            cols.append(Plin[Y0:Y1, X0:X1][tm].mean(axis=0))
            counts.append(int(tm.sum()))
            rows.append([round(float(x), 4), round(float(z), 4), hgt, ci])
            got += 1
        placed_px[cls] = {"placed": got, "wanted": n_want, "footprint_px": [round(2 * rx, 1), round(2 * ry, 1)],
                          "tuft_cells_covered_share": round(1.0 - float(R.sum()) / max(float(remaining[cls].sum()), 1e-9), 4)}
    cols = np.array(cols)
    mean = cols.mean(axis=0)
    rel = cols / mean
    for rw, m in zip(rows, rel):
        rw += [round(float(m[0]), 4), round(float(m[1]), 4), round(float(m[2]), 4)]
    json.dump({"_what": "the 3D heather: the 954 heather sprays and 23 shrub clumps of take/build/heather_instances.json, RE-PLACED on the painted tufts (greedy cover), each coloured by the painting's tufts beneath it",
               "columns": ["x", "z", "height_m", "class (0 heather, 1 shrub)", "mul_r", "mul_g", "mul_b"],
               "_mul": "linear: the painting's tuft pixels under the spray's screen footprint, over the mean of all sprays",
               "painted_mean_linear": [round(float(v), 5) for v in mean], "placement": placed_px, "rows": rows},
              open(os.path.join(OUT, "heather.json"), "w"))
    man["heather"] = {"file": "heather.json", "count": len(rows), "albedo_mul": list(HEATHER_ALBEDO_MUL),
                      "_albedo_mul": HEATHER_ALBEDO_MUL_WHY}
    rep["heather"] = {"instances": len(rows), "placement": placed_px,
                      "painted_mean_linear": [round(float(v), 5) for v in mean],
                      "painted_mean_srgb": [int(round(float(v) * 255)) for v in l2s(mean)],
                      "rel_mul_p10_p50_p90": [[round(float(np.percentile(rel[:, k], q)), 3) for q in (10, 50, 90)] for k in range(3)],
                      "tuft_px_per_spray_median": int(np.median(counts))}

    # ---- the snow's depth grid over its field, from the painted splat ----------------------------
    rb = L["frame"]["reach_box"]
    cu = [xz_of_uv(u, v) for u in rb["u"] for v in rb["v"]]
    pad = 1.5
    xmn, xmx = min(p[0] for p in cu) - pad, max(p[0] for p in cu) + pad
    zmn, zmx = min(p[1] for p in cu) - pad, max(p[1] for p in cu) + pad
    side = max(xmx - xmn, zmx - zmn)
    cx, cz = (xmn + xmx) / 2, (zmn + zmx) / 2
    area = [round(cx - side / 2, 3), round(cz - side / 2, 3), round(side, 3), round(side, 3)]
    SP = np.asarray(Image.open(os.path.join(TAKE, "build", "barrow_full_splat_painted.bin")).convert("RGBA")).astype(np.float64) / 255.0
    so = L["regions"]["splat"]["origin_xz"]
    smpp = L["regions"]["splat"]["m_per_px"]
    cell = 0.1
    nx = int(math.ceil(side / cell)) + 1
    gx0, gz0 = area[0], area[1]
    zz, xx = np.mgrid[0:nx, 0:nx]
    X = gx0 + xx * cell
    Z = gz0 + zz * cell
    si = np.clip(((X - so[0]) / smpp).astype(int), 0, SP.shape[1] - 1)
    sj = np.clip(((Z - so[1]) / smpp).astype(int), 0, SP.shape[0] - 1)
    w = SP[sj, si]                                   # path, rock, heather (B shrub), ice
    wsnow = np.clip(1.0 - w.sum(-1), 0.0, 1.0)
    rng = np.random.default_rng(91127)
    def smooth_noise(scale_m):
        n0 = rng.random((nx, nx))
        s_ = ndimage.gaussian_filter(n0, sigma=scale_m / cell, mode="wrap")
        return (s_ - s_.mean()) / (s_.std() * 6.0) + 0.5
    nv = np.clip(smooth_noise(1.4) * 0.7 + smooth_noise(0.45) * 0.3, 0.0, 1.0)
    mulg = np.zeros((nx, nx))
    trod = np.zeros((nx, nx))
    for k, (name, wk) in enumerate((("snow", wsnow), ("path", w[..., 0]), ("rock", w[..., 1]),
                                    ("heather", w[..., 2]), ("ice", w[..., 3]))):
        m_, patch, tr = SNOW_BY_CLASS[name]
        keep = np.clip((nv - (patch - 0.08)) / 0.16, 0.0, 1.0) if patch > 0 else 1.0
        keep = keep * keep * (3 - 2 * keep) if patch > 0 else 1.0
        mulg += wk * m_ * keep
        trod += wk * tr
    gridp = os.path.join(OUT, "snow_grid.bin")
    np.concatenate([mulg.astype("<f4").ravel(), trod.astype("<f4").ravel()]).tofile(gridp)
    man["snow"] = {"area_xz": area, "field_px": 768, "trail_px": 1024,
                   "grid": {"file": "snow_grid.bin", "sha256": sha_file(gridp), "origin_xz": [gx0, gz0], "cell_m": cell,
                            "nx": nx, "nz": nx, "_layout": "float32 little-endian: nx*nz depth multipliers (row = z), then nx*nz trodden amounts"},
                   "_": "the installed Barrow's SNOW_BY_CLASS on the painted splat; the field covers the reach box + 1.5 m (world xz, square)"}
    rep["snow"] = {"area_xz": area, "grid_cells": nx * nx, "mean_mul": round(float(mulg.mean()), 4),
                   "bare_share_mul_under_0.125": round(float((mulg < 0.125).mean()), 4)}

    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    json.dump(rep, open(os.path.join(TAKE, "build", "painted_prep.json"), "w"), indent=1)
    print(json.dumps({k: rep[k] for k in ("tufts_self_test", "shadow", "inpaint", "heather", "snow")}, indent=1)[:4000])


WEB = os.path.join(BF, "godot", "data", "painted_web")
WEB_MAX_PX = 4096          # WebGL2's safe texture size: every phone GPU the page may meet takes it
WEB_BAKE_PX = 512          # a baked piece stands 40-110 px tall on a phone's 3D frame
WEB_LIT_SCALE = 4          # the light map is smooth: a quarter of the guide (1344 x 832)
WEB_WEBP_Q = 90


def web():
    """THE PHONE PAGE'S DATA, from the desktop's (run main() first): the painting within 4096 px and
    the bakes at 512, both lossy WebP at q90; the light map at a quarter; the snow grid and the
    heather as they are. Each file's sha256 in painted_web/manifest.json, and what the downsizing
    cost, measured, in take/build/painted_web_prep.json."""
    os.makedirs(os.path.join(WEB, "bakes"), exist_ok=True)
    man = json.load(open(os.path.join(OUT, "manifest.json")))
    rep = {"_what": "C-9 T10-2: the painted Barrow's phone data (tools/paint_world_prep.py --web), and what the downsizing cost",
           "from": "godot/data/painted/manifest.json"}
    P = Image.open(os.path.join(OUT, man["painting"]["file"])).convert("RGB")
    k = WEB_MAX_PX / float(max(P.size))
    wsz = (int(round(P.size[0] * k)), int(round(P.size[1] * k)))
    Pw = P.resize(wsz, Image.LANCZOS)
    pp = os.path.join(WEB, "painting.bin")
    Pw.save(pp, format="WEBP", quality=WEB_WEBP_Q, method=6)
    # THE COST, measured: the phone painting decoded and set against the desktop painting brought
    # to the same size (the downsizing alone is the resampling; the WebP is the rest)
    dec = np.asarray(Image.open(pp).convert("RGB")).astype(np.float64)
    ref = np.asarray(Pw).astype(np.float64)
    rep["painting"] = {"px": list(wsz), "scale": round(k, 4), "bytes": os.path.getsize(pp),
                       "desktop_png_bytes": os.path.getsize(os.path.join(OUT, man["painting"]["file"])),
                       "webp_q": WEB_WEBP_Q, "webp_vs_lossless_same_size_mean_abs": round(float(np.abs(dec - ref).mean()), 3)}
    wm = {"_what": man["_what"] + " -- THE PHONE PAGE'S (tools/paint_world_prep.py --web)", "bakes": {}}
    wm["painting"] = {"file": "painting.bin", "sha256": sha_file(pp), "px": list(wsz),
                      "_": "the accepted paint-over within %d px, lossy WebP q%d" % (WEB_MAX_PX, WEB_WEBP_Q)}
    wm["ground_as_painted"] = dict(wm["painting"])
    L_ = Image.open(os.path.join(OUT, man["lit"]["file"]))
    lw = (W // WEB_LIT_SCALE, H // WEB_LIT_SCALE)
    lp = os.path.join(WEB, "lit.bin")
    L_.resize(lw, Image.BILINEAR).save(lp, format="PNG")
    wm["lit"] = {"file": "lit.bin", "sha256": sha_file(lp), "px": list(lw), "_": man["lit"]["_"] + " -- a quarter, for the phone"}
    bsum = 0
    for pid, b in man["bakes"].items():
        src = Image.open(os.path.join(OUT, b["file"])).convert("RGB").resize((WEB_BAKE_PX, WEB_BAKE_PX), Image.LANCZOS)
        dst = os.path.join(WEB, "bakes", "%s.bin" % pid)
        src.save(dst, format="WEBP", quality=WEB_WEBP_Q, method=6)
        wm["bakes"][pid] = {"file": "bakes/%s.bin" % pid, "sha256": sha_file(dst)}
        bsum += os.path.getsize(dst)
    rep["bakes"] = {"count": len(wm["bakes"]), "px": WEB_BAKE_PX, "bytes": bsum}
    for f in ("snow_grid.bin", "heather.json"):
        shutil.copyfile(os.path.join(OUT, f), os.path.join(WEB, f))
    wm["shadow_mul"] = man["shadow_mul"]
    wm["heather"] = man["heather"]
    wm["snow"] = json.loads(json.dumps(man["snow"]))
    # the phone's field and trail: 512 px each, as the installed Barrow's phone build (its trail at
    # 512 over 34 m; here 9.2 cm texels over 47 m) -- the bake is GDScript on one wasm thread
    wm["snow"]["field_px"] = 512
    wm["snow"]["trail_px"] = 512
    json.dump(wm, open(os.path.join(WEB, "manifest.json"), "w"), indent=1)
    tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(WEB) for f in fs)
    rep["total_bytes"] = tot
    json.dump(rep, open(os.path.join(TAKE, "build", "painted_web_prep.json"), "w"), indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    import sys
    if "--web" in sys.argv:
        web()
    else:
        main()
