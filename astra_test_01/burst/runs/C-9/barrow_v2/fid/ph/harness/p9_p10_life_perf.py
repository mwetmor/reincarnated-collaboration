#!/usr/bin/env python3
"""P9 (LIFE, mechanical -- Gate-1 W-7/I-2) and P10 (DESKTOP PERFORMANCE) -- constraint rows: a v1 positive control
where v1 has the system, RED shown once; negative control for P9 = R-C9-158 (no heather wind, no moving water, no
snow trail).

P9a HEATHER SWAY   renders/life_<x>: f0, f1 (static play camera, 0.5 s apart, him absent, falling snow hidden) and
                   hide_heather (heather shadow-only). Heather mask = |f0 - hide_heather| > 12 (dilated 2 px).
                   sway = mean |f1 - f0| (0-255) on the mask; noise = the same off the mask (static ground).
                   PASS: sway >= 3 x noise AND sway >= 0.25 x v1's sway. RED: v1 with the wind held (--no-wind).
P9b WATER FLOW     (in-engine, BINDING) the same pair inside the water mask (|f0 - hide_water| > 6): flow >= 3 x noise.
                   RED: the sea with its motion layers hidden, two frames 0.5 s apart (hide_water, hide_water_b).
                   (film, DISCARDED at calibration -- see results) two frames 0.5 s apart from a walk/pan film, registered by phase correlation (an ortho pan is
                   a pure translation), residual on the painted-water class (Lab L < 40, b < -3) vs residual on snow:
                   flow ratio = water / snow residual; PASS: ratio >= 2. Positive: R-C9-159's film (DEV-5's animated
                   sea); NEGATIVE: R-C9-158's film. v1 has no open water (N/A).
P9c FLOE UV DRIFT  floe_m0/m1 (the floes wearing an 8 px checker marker, 0.5 s apart) + hide_floe. Per floe: the
                   silhouette's displacement (mask centroid) minus the marker texture's displacement (phase correlation
                   inside the floe): a REST-POSE UV moves the marker with the floe (drift 0). PASS: median drift
                   <= 0.25 px. v1 has no floes (N/A); R-C9-159 is the RED (painting projected through the camera
                   onto bobbing floes: "the painting slides with them", barrow_v2_sw.gd FLOE_BOB).
P9d SNOW TRAIL     coverage = share of the walkable floor inside the SnowField's area (level data: snow.area_xz) --
                   where his trail can exist at all. PASS >= 0.99 (v1: 1.00). R-C9-158 has no SnowField: 0 (RED).
P10 PERFORMANCE    renders/perf_<x>/perf.json (ph_life.gd perf: Forward+ desktop, 1920 x 1080, vsync off, uncapped,
                   him walking a 4-point loop, 900 frames): PASS p99 <= 16.7 ms (plan § 4 P10; the plan's 10.9-12.4 ms
                   target is WITHDRAWN, Gate-1 W-2). RED: v1 with a 20 ms busy-wait per frame (--burn-ms 20).
"""
import math
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

R = PH / "renders"


def _d(a, b):
    return np.abs(a - b).mean(-1)


def sway(dirp):
    f0, f1 = load_rgb(dirp / "f0.png"), load_rgb(dirp / "f1.png")
    hh = load_rgb(dirp / "hide_heather.png")
    m = ndimage.binary_dilation(_d(f0, hh) > 12, iterations=2)
    d = _d(f1, f0)
    out = {"heather_px": int(m.sum()), "sway": round(float(d[m].mean()), 3) if m.any() else 0.0,
           "noise": round(float(d[~m].mean()), 3)}
    if (dirp / "hide_water.png").exists():
        w = _d(f0, load_rgb(dirp / "hide_water.png")) > 6
        w &= ~m
        out["water_px"] = int(w.sum())
        out["flow"] = round(float(d[w].mean()), 3) if w.any() else 0.0
        if (dirp / "hide_water_b.png").exists():          # RED pair: the sea without its motion layers, 0.5 s apart
            d2 = _d(load_rgb(dirp / "hide_water_b.png"), load_rgb(dirp / "hide_water.png"))
            out["flow_static_sea_RED"] = round(float(d2[w].mean()), 3) if w.any() else 0.0
            out["noise_static_sea"] = round(float(d2[~w & ~m].mean()), 3)
    return out


def phase_shift(a, b):
    A = np.fft.fft2(a - a.mean())
    B = np.fft.fft2(b - b.mean())
    Rr = A * np.conj(B)
    Rr /= np.abs(Rr) + 1e-9
    r = np.fft.ifft2(Rr).real
    y, x = np.unravel_index(np.argmax(r), r.shape)
    if y > a.shape[0] // 2:
        y -= a.shape[0]
    if x > a.shape[1] // 2:
        x -= a.shape[1]
    return int(y), int(x)


def film_water_times(mp4, n=3, step=1.0):
    """the n frames (sampled every `step` s) with the largest painted-water share -- chosen by the class, not by eye"""
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                               capture_output=True, text=True).stdout.strip())
    shares = []
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp4), "-vf", "fps=%g,scale=480:-1" % (1 / step), "%s/s%%04d.png" % td], check=True)
        for i, f in enumerate(sorted(pathlib.Path(td).glob("s*.png"))):
            lab = rgb_to_lab(load_rgb(f))
            shares.append((float(((lab[..., 0] < 40) & (lab[..., 2] < -3)).mean()), i * step))
    shares = [x for x in shares if x[1] + 0.6 < dur]
    shares.sort(reverse=True)
    return [t for sh, t in shares[:n] if sh >= 0.02], [round(sh, 3) for sh, t in shares[:n]]


def film_flow(mp4, t0, dt=0.5):
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate((t0, t0 + dt)):
            subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", str(mp4), "-frames:v", "1", "%s/f%d.png" % (td, i)], check=True)
        a, b = load_rgb(td + "/f0.png"), load_rgb(td + "/f1.png")
    dy, dx = phase_shift(luma(a), luma(b))
    H, W = a.shape[:2]
    ys, xs = slice(max(dy, 0), H + min(dy, 0)), slice(max(dx, 0), W + min(dx, 0))
    ys2, xs2 = slice(max(-dy, 0), H + min(-dy, 0)), slice(max(-dx, 0), W + min(-dx, 0))
    A, B = a[ys, xs], b[ys2, xs2]
    lab = rgb_to_lab(ndimage.gaussian_filter(A, (3, 3, 0)))
    water = (lab[..., 0] < 40) & (lab[..., 2] < -3)
    snow = (lab[..., 0] > 80) & (lab[..., 2] > -6)
    water = ndimage.binary_erosion(water, iterations=6)
    snow = ndimage.binary_erosion(snow, iterations=6)
    d = _d(A, B)
    wr = float(d[water].mean()) if water.sum() > 2000 else None
    sr = float(d[snow].mean()) if snow.sum() > 2000 else None
    return {"film": str(mp4.name), "t": t0, "shift_px": [dy, dx], "water_px": int(water.sum()), "water_resid": None if wr is None else round(wr, 3),
            "snow_resid": None if sr is None else round(sr, 3), "ratio": None if (wr is None or not sr) else round(wr / sr, 3)}


def floe_drift(dirp):
    m0, m1 = load_rgb(dirp / "floe_m0.png"), load_rgb(dirp / "floe_m1.png")
    hf = load_rgb(dirp / "hide_floe.png")
    k0 = ndimage.binary_opening(_d(m0, hf) > 20, iterations=1)
    k1 = ndimage.binary_opening(_d(m1, hf) > 20, iterations=1)
    lab, n = ndimage.label(k0)
    drifts = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None:
            continue
        piece0 = lab[sl] == i + 1
        if piece0.sum() < 1500:
            continue
        y0, y1 = max(sl[0].start - 8, 0), sl[0].stop + 8
        x0, x1 = max(sl[1].start - 8, 0), sl[1].stop + 8
        p0, p1 = k0[y0:y1, x0:x1], k1[y0:y1, x0:x1]
        c0, c1 = ndimage.center_of_mass(p0), ndimage.center_of_mass(p1)
        sil = (c1[0] - c0[0], c1[1] - c0[1])
        core = ndimage.binary_erosion(p0 & p1, iterations=4)
        if core.sum() < 500:
            continue
        a = luma(m0[y0:y1, x0:x1]) * core
        b = luma(m1[y0:y1, x0:x1]) * core
        ty, tx = phase_shift(b, a)
        drifts.append(math.hypot(sil[0] - ty, sil[1] - tx))
    return {"floes_measured": len(drifts), "median_drift_px": round(float(np.median(drifts)), 3) if drifts else None,
            "max_drift_px": round(float(np.max(drifts)), 3) if drifts else None}


def poly_area_inside_rect(poly, rect, step=0.25):
    from matplotlib.path import Path
    x0, z0, w, h = rect
    p = Path(np.array(poly))
    xs = np.arange(min(q[0] for q in poly), max(q[0] for q in poly), step)
    zs = np.arange(min(q[1] for q in poly), max(q[1] for q in poly), step)
    X, Z = np.meshgrid(xs, zs)
    pts = np.c_[X.ravel(), Z.ravel()]
    inside = p.contains_points(pts)
    inr = (pts[:, 0] >= x0) & (pts[:, 0] <= x0 + w) & (pts[:, 1] >= z0) & (pts[:, 1] <= z0 + h)
    return float((inside & inr).sum() / max(inside.sum(), 1))


def trail():
    C47, S47 = math.cos(math.radians(47)), math.sin(math.radians(47))
    v1man = jload(BF / "godot/data/painted/manifest.json")["snow"]
    disc = [(7 * math.cos(a), 1 + 7 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 128)]
    v1poly = [(u * C47 - v * S47, -u * S47 - v * C47) for u, v in disc]          # uv -> world xz
    lvl = jload(BF / "godot/data/barrow_v2_sw/level.json")
    bx = lvl["box"]                       # R-C9-159 built only the SW section: its floor = the layout floor inside its box
    from matplotlib.path import Path
    fl = np.array(lvl["floor_polygon_xz"])
    xs, zs = np.meshgrid(np.arange(bx["x0"], bx["x1"], 0.25), np.arange(bx["y0"], bx["y1"], 0.25))
    pts = np.c_[xs.ravel(), zs.ravel()]
    inside = Path(fl).contains_points(pts)
    ax, az, aw, ah = lvl["snow"]["area_xz"]
    inr = (pts[:, 0] >= ax) & (pts[:, 0] <= ax + aw) & (pts[:, 1] >= az) & (pts[:, 1] <= az + ah)
    cov159 = float((inside & inr).sum() / max(inside.sum(), 1))
    return {"v1": {"coverage": round(poly_area_inside_rect(v1poly, v1man["area_xz"]), 4), "area_xz": v1man["area_xz"], "floor": "arena disc r 7 m"},
            "159": {"coverage": round(cov159, 4), "area_xz": lvl["snow"]["area_xz"], "floor": "layout floor inside the section box"},
            "158": {"coverage": 0.0, "evidence": "R-C9-158 ran outside v1's engine: no SnowField (charter § 9 C-2; plan C3)"}}


def perf(dirp):
    p = dirp / "perf.json"
    if not p.exists():
        return None
    d = jload(p)
    return {"p50_ms": round(d["p50_ms"], 2), "p99_ms": round(d["p99_ms"], 2), "max_ms": round(d["max_ms"], 2), "burn_ms": d.get("burn_ms"),
            "renderer": d.get("renderer"), "pass": d["p99_ms"] <= 16.7}


if __name__ == "__main__":
    out = {"p9": {}, "p10": {}}
    s = {k: sway(R / ("life_" + k)) for k in ("v1", "v1_nowind", "v159") if (R / ("life_" + k) / "f1.png").exists()}
    if "v1" in s:
        bar = 0.25 * s["v1"]["sway"]
        for k, v in s.items():
            v["sway_pass"] = v["sway"] >= 3 * v["noise"] and v["sway"] >= bar
            if "flow" in v:
                v["flow_pass"] = v["flow"] >= 3 * v["noise"]
            if "flow_static_sea_RED" in v:
                v["flow_static_sea_pass"] = v["flow_static_sea_RED"] >= 3 * v["noise_static_sea"]
        out["p9"]["a_heather_sway"] = {"bar": "sway >= 3 x noise and >= %.3f (0.25 x v1)" % bar, "rows": s}
    else:
        out["p9"]["a_heather_sway"] = {"pending": "renders/life_* not yet captured", "rows": s}
    films = {"159": B2 / "section_v1cam/look/R-C9-159_v2sw_coast_walk.mp4",
             "159_lead": B2 / "section_v1cam/look/R-C9-159_v2sw_coast_walk_lead.mp4",
             "158": B2 / "section_sw/look/R-C9-158_section_sw_coast_pan.mp4",
             "158_v2": B2 / "section_sw/look/R-C9-158_section_sw_coast_pan_v2.mp4"}
    fr = {}
    for k, mp4 in films.items():
        ts, sh = film_water_times(mp4)
        rows = [film_flow(mp4, t) for t in ts]
        ratios = [r["ratio"] for r in rows if r["ratio"] is not None]
        fr[k] = {"water_share_top": sh, "rows": rows, "median_ratio": round(float(np.median(ratios)), 3) if ratios else None,
                 "pass": bool(ratios) and float(np.median(ratios)) >= 2.0}
    out["p9"]["b_water_flow_film_DISCARDED"] = {
        "why": "cannot separate the positive (R-C9-159's animated sea, median ratio 1.7-1.8) from the negative "
               "(R-C9-158, 1.38) on compressed, panning films -- discarded at calibration; the binding P9b instrument is "
               "the in-engine static pair (life_<x>: flow on the water mask vs noise; RED = the same sea with its motion "
               "layers hidden, hide_water vs hide_water_b)", "bar_was": "ratio >= 2", "rows": fr}
    fd = R / "life_v159"
    out["p9"]["c_floe_drift"] = floe_drift(fd) if (fd / "floe_m1.png").exists() else {"pending": "life_v159 not yet captured"}
    if "median_drift_px" in out["p9"]["c_floe_drift"] and out["p9"]["c_floe_drift"]["median_drift_px"] is not None:
        out["p9"]["c_floe_drift"]["pass"] = out["p9"]["c_floe_drift"]["median_drift_px"] <= 0.25
    t = trail()
    for v in t.values():
        v["pass"] = v["coverage"] >= 0.99
    out["p9"]["d_snow_trail_coverage"] = t
    for k in ("v1", "v1_burn", "v159"):
        out["p10"][k] = perf(R / ("perf_" + k))
    print(json.dumps(out, indent=1)[:4000])
    dump(out, str(PH / "results/p9_p10.json"))
