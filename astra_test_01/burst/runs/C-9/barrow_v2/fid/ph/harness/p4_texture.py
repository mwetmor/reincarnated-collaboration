#!/usr/bin/env python3
"""P4 -- PER-CLASS TEXTURE STATISTICS of the static surfaces AS DISPLAYED (100.6 screen px/m), against v1.

Classes (plan § 4 P4): snow, rock, wood, ice; new barrow_v2 classes (sea, shingle) take the class-agnostic
cellularity detector only (Gate-1 W-7) -- no v1 class is near enough to name.
  v1 source: the painting (unlit statics: the displayed texel IS the painting's, P3 measures the residual), classes
             from v1's own instruments, read-only (tools/paint_world_prep.py id_index + tuft_classes; step 3's
             ground layout take/ground/ground_uv.png): rock = outcrop, shore_rock, stone_tall/mid/short, lintel, post;
             wood = log; snow = open-snow ground less tufts; ice = ice ground. Units = the 16 paint chunks.
  R-C9-159: ground = its painting magnified x2 (bilinear, as the GPU displays a 50.3 px/m texture at 100.6),
             classes from its own ground guide (guide2/v2sw_guide.png, Lab rules: water L<40 | ice b<-6 |
             snow L>=78 | other = shingle and cliff backs); models (rock: cliffplain/crag/cavecliff/staircliff;
             wood: wreck2) from the PH render (renders/v159: render where it differs from hide_<group>), magnified x2.
Three statistics per class sample (pixels eroded 3 px from the class edge):
  (1) Lab HISTOGRAM distance -- Hellinger distance between the sample's 3-D Lab histogram (L 0-100, a -20..30,
      b -30..40; 10 bins each) and v1's POOLED histogram of that class.
  (2) SPECTRUM SHAPE distance -- RMS difference, over periods 4-32 px, of the mean mean-removed log radial power
      spectrum of 64 px windows lying >= 90% inside the class, against v1's pooled class spectrum.
  (3) CELLULARITY -- per 64 px window (>= 90% static-surface pixels, any class), the largest excess of log power in
      the 6-20 px period band over a power law fitted on periods 3-6 and 20-40 px; the sample's score is the
      95th percentile over its windows. (plan: "spectral peak at 6-20 px period")
  ** (3) IS DISCARDED (calibration 2026-10-06, rule "re-instrumented or discarded; never threshold-tuned"): it cannot
     see a mechanism-faithful constructed failure -- PATCHWORK ROCK below scores p95 0.417 on rock windows against
     v1 rock's own 0.402 and the bar 0.681; a +-15% Voronoi tone stamp scores 0.391. It is still computed and
     reported (non-binding) because R-C9-159's bakes do score higher (median 0.30-0.52 vs v1 bakes 0.11), but an
     instrument that cannot see its own constructed failure decides nothing. Cellularity has NO binding instrument
     in this harness; P11 (the blind judge) is the remaining guard. New classes (sea, shingle) therefore have no
     P4 statistic until the conductor names a nearest v1 class (W-7).
THRESHOLDS from v1's own chunk-to-chunk spread: (1),(2) the max over v1 chunks of the chunk's distance to the
pooled v1 class built WITHOUT that chunk (leave-one-out); (3) the max over v1 chunks of the chunk's score.
PASS per class: every statistic <= its v1 bar. Row PASS: every class passes.
CONSTRUCTED FAILURES: (a) PATCHWORK ROCK -- v1 rock pixels re-assembled from a Voronoi field of 12 px cells, each
cell taken from one of four differently offset copies of the painting (the facing^4 blend of four separately painted
views, in miniature); (b) RE-LIT ROCK -- v1 rock pixels
darkened by 30% in linear light and cooled (x 0.88, 0.95, 1.08): the painted light lit a second time.
"""
import argparse
import importlib.util
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

LAB_RANGE = ((0, 100), (-20, 30), (-30, 40))
NB = 10
WIN = 64
CLASSES = ["snow", "rock", "wood", "ice"]


def _pw():
    spec = importlib.util.spec_from_file_location("pw_v1_readonly", BF / "tools/paint_world_prep.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)            # module level reads the layout only; main() is never called
    return m


def lab_hist(lab):
    h, _ = np.histogramdd(lab.reshape(-1, 3), bins=NB, range=LAB_RANGE)
    return h / max(h.sum(), 1)


def hellinger(p, q):
    return float(np.sqrt(0.5 * ((np.sqrt(p) - np.sqrt(q)) ** 2).sum()))


def windows(mask, frac=0.9, step=WIN):
    H, W = mask.shape
    ii = ndimage.uniform_filter(mask.astype(np.float32), WIN)
    out = []
    for y in range(WIN // 2, H - WIN // 2, step):
        for x in range(WIN // 2, W - WIN // 2, step):
            if ii[y, x] >= frac:
                out.append((y - WIN // 2, x - WIN // 2))
    return out


def spectrum_shape(gray, wins):
    if not wins:
        return None
    acc = []
    for y, x in wins:
        per, pw = radial_spectrum(gray[y:y + WIN, x:x + WIN])
        sel = (per >= 4) & (per <= 32)
        lp = np.log10(pw[sel] + 1e-9)
        acc.append(lp - lp.mean())
    return np.mean(acc, 0)


def cell_excess(gray, wins):
    out = []
    for y, x in wins:
        per, pw = radial_spectrum(gray[y:y + WIN, x:x + WIN])
        lp = np.log10(pw + 1e-9)
        lf = np.log10(1.0 / per)
        fit = ((per >= 3) & (per < 6)) | ((per > 20) & (per <= 40))
        band = (per >= 6) & (per <= 20)
        a, b = np.polyfit(lf[fit], lp[fit], 1)
        out.append(float((lp[band] - (a * lf[band] + b)).max()))
    return out


def stats(img, masks, static_mask):
    """img: display-scale RGB; masks: class -> bool mask; static_mask: all static pixels (for cellularity)."""
    lab = rgb_to_lab(img)
    gray = luma(img)
    res = {}
    for c, m in masks.items():
        m2 = ndimage.binary_erosion(m, iterations=3)
        if m2.sum() < 20000:
            continue
        res[c] = {"px": int(m2.sum()), "hist": lab_hist(lab[m2]), "spec": spectrum_shape(gray, windows(m2))}
    ce = cell_excess(gray, windows(static_mask))
    return res, (float(np.percentile(ce, 95)) if ce else None), len(ce)


# ------------------------------------------------------------------ v1
def v1_classes(P8=None):
    PW = _pw()
    if P8 is None:
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
    gi = np.clip(((uu - PW.U0) * 20).astype(int), 0, GU.shape[1] - 1)
    gj = np.clip(((PW.V1 - vv) * 20).astype(int), 0, GU.shape[0] - 1)
    gcls = GU[gj, gi]
    cls_of = {k: v["class"] for k, v in table.items()}
    rock_ids = [k for k, c in cls_of.items() if c in ("outcrop", "shore_rock", "stone_tall", "stone_mid", "stone_short", "lintel", "post")]
    wood_ids = [k for k, c in cls_of.items() if c == "log"]
    masks = {"rock": np.isin(idx, rock_ids), "wood": np.isin(idx, wood_ids),
             "snow": ground & (gcls == 0) & ~tufts, "ice": ground & (gcls == 4) & ~tufts}
    static = ~tufts & ~np.isin(idx, [k for k, c in cls_of.items() if c == "birch"])
    return masks, static


def v1_chunks():
    return [(c["key"], c["px"]) for c in jload(BF / "paint/cfg_barrow_full.json")["chunks"]]


def v1_pool(P=None, masks=None, static=None):
    P = load_rgb(BF / "paint/barrow_full_painted.png") if P is None else P
    if masks is None:
        masks, static = v1_classes()
    per = {}
    for key, (x0, y0, x1, y1) in v1_chunks():
        sub = {c: m[y0:y1, x0:x1] for c, m in masks.items()}
        per[key] = stats(P[y0:y1, x0:x1], sub, static[y0:y1, x0:x1])
    return per


def pooled(per, cls, exclude=None):
    hs = [(r[0][cls]["hist"], r[0][cls]["px"]) for k, r in per.items() if k != exclude and cls in r[0]]
    ss = [r[0][cls]["spec"] for k, r in per.items() if k != exclude and cls in r[0] and r[0][cls]["spec"] is not None]
    if not hs:
        return None, None
    h = sum(a * n for a, n in hs) / sum(n for _, n in hs)
    return h / h.sum(), (np.mean(ss, 0) if ss else None)


def v1_bars(per):
    bars = {}
    for c in CLASSES:
        dh, ds = [], []
        for k, r in per.items():
            if c not in r[0]:
                continue
            ph, ps = pooled(per, c, exclude=k)
            if ph is None:
                continue
            dh.append(hellinger(r[0][c]["hist"], ph))
            if ps is not None and r[0][c]["spec"] is not None:
                ds.append(float(np.sqrt(np.mean((r[0][c]["spec"] - ps) ** 2))))
        if dh:
            bars[c] = {"hist": max(dh), "spec": max(ds) if ds else None, "n_chunks": len(dh)}
    bars["cellularity"] = max(r[1] for r in per.values() if r[1] is not None)
    return bars


def score(sample, per, bars):
    res, cell, nwin = sample
    out = {"classes": {}, "cellularity_p95": None if cell is None else round(cell, 3), "cell_windows": nwin}
    ok = True
    for c, r in res.items():
        if c not in bars:
            out["classes"][c] = {"px": r["px"], "note": "no v1 class -- cellularity only (W-7)"}
            continue
        ph, ps = pooled(per, c)
        dh = hellinger(r["hist"], ph)
        dspec = float(np.sqrt(np.mean((r["spec"] - ps) ** 2))) if (r["spec"] is not None and ps is not None) else None
        p = dh <= bars[c]["hist"] and (dspec is None or bars[c]["spec"] is None or dspec <= bars[c]["spec"])
        out["classes"][c] = {"px": r["px"], "hist_dist": round(dh, 3), "hist_bar": round(bars[c]["hist"], 3),
                             "spec_dist": None if dspec is None else round(dspec, 3),
                             "spec_bar": None if bars[c]["spec"] is None else round(bars[c]["spec"], 3), "pass": p}
        ok = ok and p
    cp = cell is None or cell <= bars["cellularity"]
    out["cellularity_bar"] = round(bars["cellularity"], 3)
    out["cellularity_pass_DISCARDED_non_binding"] = cp
    out["pass"] = ok                      # (3) cellularity DISCARDED at calibration -- see the docstring
    return out


# ------------------------------------------------------------------ R-C9-159
def v159_samples(render_dir=None):
    """R-C9-159 as displayed: its render at the paint frame (statics as played; models where the PH render shows them,
    the painted ground elsewhere), magnified x2 to play zoom (bilinear, as the GPU shows a 50.3 px/m texture at
    100.6). Classes = P3's R-C9-159 masks (p3_residual.v159_rows: model families from |render - hide_<group>| less
    the animated sea; ground classes from 159's own guide): rock = the rock bakes + the reused v1-kit stone bakes;
    wood = wreck2 + log; snow, ice = ground; shingle + cliff-back = no v1 class (W-7); the sea is DEV-5 water."""
    import p3_residual as P3
    rd = pathlib.Path(render_dir) if render_dir else None
    if rd is None or not (rd / "render.png").exists():
        R = load_rgb(BF / "godot/data/barrow_v2_sw/painted/ground.png")
        gd = load_rgb(B2 / "section_v1cam/guide2/v2sw_guide.png")
        lab = rgb_to_lab(ndimage.gaussian_filter(gd, (4, 4, 0)))
        L, b = lab[..., 0], lab[..., 2]
        M = {"snow": (L >= 78) & (b >= -6), "ice": (L >= 40) & (b < -6), "shingle+cliff-back": (L >= 40) & (L < 78) & (b >= -6)}
        static = L >= 40
        have = False
    else:
        R = load_rgb(rd / "render.png")
        _, M3 = P3.v159_rows(rd)
        M = {"rock": M3["rock (cliffplain, crag, cavecliff, staircliff bakes)"] | M3["v1-kit stones (v1 bakes)"],
             "wood": M3["wood (wreck2 bake, v1 log bake)"], "snow": M3["ground: snow"], "ice": M3["ground: ice"],
             "shingle+cliff-back": M3["ground: shingle + cliff back"]}
        static = np.zeros(R.shape[:2], bool)
        for m in M.values():
            static |= m
        have = True
    up = lambda a: np.asarray(Image.fromarray(a.astype(np.uint8)).resize((a.shape[1] * 2, a.shape[0] * 2), Image.BILINEAR), np.float32)
    upm = lambda m: np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((m.shape[1] * 2, m.shape[0] * 2), Image.NEAREST)) > 127
    Ru, Mu, Su = up(R), {k: upm(v) for k, v in M.items()}, upm(static)
    out = {}
    H, W = Ru.shape[:2]
    for y0 in range(0, H - 1023, 1024):
        for x0 in range(0, W - 1535, 1536):
            sl = (slice(y0, y0 + 1024), slice(x0, x0 + 1536))
            out["%d_%d" % (x0 // 1536, y0 // 1024)] = stats(Ru[sl], {k: v[sl] for k, v in Mu.items()}, Su[sl])
    return out, have


def constructed(per_v1_masks):
    masks, static = per_v1_masks
    P = load_rgb(BF / "paint/barrow_full_painted.png")
    rng = np.random.default_rng(159)
    H, W = P.shape[:2]
    # (a) PATCHWORK: a Voronoi field of 12 px mean cells; each cell's texels taken from one of FOUR differently
    #     offset copies of the painting -- the facing^4 blend of four separately painted views, in miniature
    n = int(H * W / 144)
    pts = np.c_[rng.integers(0, H, n), rng.integers(0, W, n)]
    lab = np.zeros((H, W), np.int32)
    lab[pts[:, 0], pts[:, 1]] = np.arange(1, n + 1)
    _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    cell = lab[iy, ix]
    src = rng.integers(0, 4, n + 1)
    m = masks["rock"]
    A = P.copy()
    for s_, (dy, dx) in enumerate(((0, 0), (37, -53), (-61, 29), (83, 71))):
        mm = m & (src[cell] == s_)
        A[mm] = np.roll(P, (dy, dx), (0, 1))[mm]
    B = P.copy()
    lin = srgb_to_lin(P[m]) * 0.7 * np.array([0.88, 0.95, 1.08])
    B[m] = np.clip(np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.clip(lin, 0, None) ** (1 / 2.4) - 0.055) * 255, 0, 255)
    return {"patchwork_rock": A, "relit_rock": B}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--render159", default=str(PH / "renders/v159"))
    a = ap.parse_args()
    masks, static = v1_classes()
    P = load_rgb(BF / "paint/barrow_full_painted.png")
    per = v1_pool(P, masks, static)
    bars = v1_bars(per)
    out = {"bars_from_v1": {c: ({k: (round(v, 3) if isinstance(v, float) else v) for k, v in b.items()} if isinstance(b, dict) else round(b, 3))
                            for c, b in bars.items()}}
    # v1 itself, per chunk (each chunk is scored against the pooled v1 -- LOO is how the bar was set)
    v1rows = {k: score(r, per, bars) for k, r in per.items()}
    out["v1"] = {"pass": all(r["pass"] for r in v1rows.values()), "chunks": v1rows}
    s159, have_models = v159_samples(a.render159)
    r159 = {k: score(r, per, bars) for k, r in s159.items()}
    out["159"] = {"pass": all(r["pass"] for r in r159.values()), "models_included": have_models, "chunks": r159}
    for name, img in constructed((masks, static)).items():
        rows = {}
        for key, (x0, y0, x1, y1) in v1_chunks():
            sub = {c: m[y0:y1, x0:x1] for c, m in masks.items()}
            rows[key] = score(stats(img[y0:y1, x0:x1], sub, static[y0:y1, x0:x1]), per, bars)
        out["constructed_" + name] = {"pass": all(r["pass"] for r in rows.values()), "chunks": rows}
    for k in [k for k in out if k != "bars_from_v1"]:
        rows = out[k]["chunks"]
        fails = [(ck, c) for ck, r in rows.items() for c, v in r["classes"].items() if v.get("pass") is False]
        cf = [ck for ck, r in rows.items() if not r["cellularity_pass_DISCARDED_non_binding"]]
        print("P4 %-26s class fails %-3d (discarded cellularity over-bar %-3d) -> %s" % (k, len(fails), len(cf), "PASS" if out[k]["pass"] else "FAIL"))
    print("bars:", out["bars_from_v1"])
    dump(out, str(PH / "results/p4.json"))
