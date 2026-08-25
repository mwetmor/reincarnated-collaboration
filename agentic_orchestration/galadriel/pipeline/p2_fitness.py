#!/usr/bin/env python3
"""p2_fitness.py -- IS THE MULTISCALE BAND OPERATOR FIT TO CARRY P-2 (SCALE COMPOSITION)?

gandalf's R-8 routes this to me. He argues the operator is NOT disqualified for
scale composition because "scale composition is literally what it measures".
That is an argument from the operator's NAME. This tests it.

Six experiments, all analysis-only. NO capture, NO render, NO GPU.

  E1  amplitude weighting -- is band_frac a MASS statistic or an ENERGY statistic?
  E2  transfer curve -- does coarse-band share track authored coarse AREA fraction?
  E3  gameability -- what is the cheapest way to raise coarse share without volume?
  E4  raster portability -- does band_frac survive a change of capture raster?
  E5  the floor-stability reframe -- WHY is band_frac stable across floors 2..12?
  E6  sub-floor spill -- does the mask floor hide faint environmental response? (L5)
"""

import json
import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame_forensics as ff  # noqa: E402

WWCR = "/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25"
OUT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "work", "2026-08-25-p2-fitness", "out"))
os.makedirs(OUT, exist_ok=True)

MARKS = ["00-pre", "01-windup-early", "02-windup-late", "03-rising-mid",
         "04-full", "05-sustain", "06-sustain-moving", "07-release-early",
         "08-release-late", "09-off"]

rng = np.random.default_rng(20260825)


def load(p):
    return np.array(Image.open(p).convert("RGB"))


def delta_field(mark, el=None):
    fx = f"{WWCR}/t1_{el}_fxon_{mark}.png" if el else f"{WWCR}/combat_fxon_{mark}.png"
    ct = f"{WWCR}/combat_fxctl_{mark}.png"
    a, b = load(fx), load(ct)
    return np.abs(a.astype(np.int16) - b.astype(np.int16)).max(axis=2).astype(np.float32)


def bands(field):
    bf, tot = ff.laplacian_band_energy(field)
    return bf, tot


def coarse(bf):
    """gandalf's own partition, from his F-2 table: fine = b0+b1, coarse = b3+."""
    return float(sum(bf[3:]))


def fine(bf):
    return float(sum(bf[:2]))


def summarise(field, label, floor=6):
    m = field >= floor
    bf, tot = bands(field * m)
    return {"label": label, "authored_px": int(m.sum()),
            "fine_b0b1": round(fine(bf), 5), "coarse_b3plus": round(coarse(bf), 5),
            "band_frac": [round(x, 5) for x in bf],
            "energy": round(tot, 1), "mean_amp": round(float(field[m].mean()) if m.any() else 0.0, 2)}


# ===========================================================================
report = {}

# --- E1: amplitude weighting ------------------------------------------------
# A bright thin line and a faint broad volume, on one canvas.
H, W = 1080, 1920
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

line = np.zeros((H, W), np.float32)
line[540:542, 460:1460] = 200.0                    # 2 px x 1000 px bright line

vol = np.zeros((H, W), np.float32)
r = np.hypot(yy - 540, xx - 960)
vol[r < 260] = 8.0                                  # broad, faint volume
vol = gaussian_filter(vol, 12)

e1 = {}
for lab, f in (("bright_line_only", line), ("faint_volume_only", vol),
               ("line + volume", line + vol)):
    e1[lab] = summarise(f, lab, floor=2)
e1["_mass_vs_energy"] = {
    "volume_px_at_floor2": int((vol >= 2).sum()),
    "line_px_at_floor2": int((line >= 2).sum()),
    "volume_share_of_AUTHORED_PIXELS": round(float((vol >= 2).sum() /
                                                   ((vol >= 2).sum() + (line >= 2).sum())), 4),
    "volume_share_of_BAND_ENERGY": round(
        float(bands(vol * (vol >= 2))[1] /
              (bands(vol * (vol >= 2))[1] + bands(line * (line >= 2))[1])), 4),
}
report["E1_amplitude_weighting"] = e1

# --- E2: transfer curve, coarse AREA fraction -> coarse BAND share ----------
# Equal per-pixel amplitude, so this isolates SCALE from BRIGHTNESS.
AMP = 120.0
e2 = []
arc = np.zeros((H, W), np.float32)
ra = np.hypot(yy - 700, xx - 960)
arc[(ra > 318) & (ra < 322) & (yy < 700)] = AMP     # 4 px thin arc
arc_px = int((arc > 0).sum())

for frac in (0.0, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 1.0):
    # coarse disc sized so coarse_px / total_px == frac, equal amplitude
    if frac >= 1.0:
        n_arc = 0
    else:
        n_arc = arc_px
    target_coarse = int(round(frac * (n_arc / (1 - frac)))) if frac < 1.0 else 40000
    rad = max(1.0, np.sqrt(target_coarse / np.pi))
    disc = np.zeros((H, W), np.float32)
    disc[np.hypot(yy - 400, xx - 500) < rad] = AMP
    f = (arc if frac < 1.0 else np.zeros((H, W), np.float32)) + disc
    s = summarise(f, f"coarse_area_frac={frac}", floor=2)
    s["coarse_AREA_frac_authored"] = round(float((disc > 0).sum() / max(1, (f > 0).sum())), 4)
    e2.append(s)
report["E2_transfer_curve"] = e2

# --- E3: gameability --------------------------------------------------------
real = delta_field("05-sustain")
e3 = {"real_05-sustain": summarise(real, "real_05-sustain")}

# (a) add one large DULL soft quad -- a fog card. no volume, no detail.
quad = np.zeros((H, W), np.float32)
quad[420:820, 660:1260] = 30.0
quad = gaussian_filter(quad, 25)
e3["a_plus_one_dull_fog_card"] = summarise(real + quad, "real + one dull quad")

# (b) genuine volumetric dust: many overlapping puffs, matched authored px + amp
dust = np.zeros((H, W), np.float32)
for _ in range(500):
    cy, cx = rng.uniform(420, 820), rng.uniform(660, 1260)
    rr = rng.uniform(6, 22)
    dust[np.hypot(yy - cy, xx - cx) < rr] += rng.uniform(6, 20)
dust = gaussian_filter(dust, 2)
# match the quad's authored pixel count and mean amplitude for fairness
sc = (quad[quad >= 6].mean() * (quad >= 6).sum()) / max(1e-9, dust[dust >= 6].sum())
dust = dust * sc
e3["b_plus_volumetric_dust"] = summarise(real + dust, "real + volumetric dust")

# (c) THE CHEAP ONE: blur the existing effect. adds nothing at all.
for sig in (1.0, 2.0, 4.0):
    e3[f"c_blur_existing_sigma{sig}"] = summarise(gaussian_filter(real, sig),
                                                  f"blur sigma={sig}")

# (d) subtract fine detail only -- coarse share is a SHARE
lowpass = gaussian_filter(real, 3.0)
detail = real - lowpass
for keep in (1.0, 0.5, 0.25, 0.0):
    e3[f"d_keep_fine_detail_x{keep}"] = summarise(np.clip(lowpass + keep * detail, 0, None),
                                                 f"fine detail x{keep}")

# (e) render-scale exploit: render at half raster, upscale to the capture raster
half = np.array(Image.fromarray(real.astype(np.uint8)).resize((W // 2, H // 2), Image.BILINEAR))
up = np.array(Image.fromarray(half).resize((W, H), Image.BILINEAR)).astype(np.float32)
e3["e_render_scale_50pct_upscaled"] = summarise(up, "render at 50% scale, upscaled")
report["E3_gameability"] = e3

# --- E4: raster portability -------------------------------------------------
e4 = []
fx = load(f"{WWCR}/combat_fxon_05-sustain.png")
ct = load(f"{WWCR}/combat_fxctl_05-sustain.png")
for (w, h) in ((1920, 1080), (1280, 720), (960, 540), (640, 360)):
    a = np.array(Image.fromarray(fx).resize((w, h), Image.BILINEAR))
    b = np.array(Image.fromarray(ct).resize((w, h), Image.BILINEAR))
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).max(axis=2).astype(np.float32)
    s = summarise(d, f"{w}x{h}")
    s["raster"] = f"{w}x{h}"
    e4.append(s)
report["E4_raster_portability"] = e4

# --- E5: why is band_frac floor-stable? ------------------------------------
m2 = real >= 2
amps = real[m2]
order = np.argsort(amps)[::-1]
srt = amps[order]
cum = np.cumsum(srt ** 2) / np.sum(srt ** 2)
n = len(srt)
e5 = {
    "authored_px_floor2": int(n),
    "authored_px_floor6": int((real >= 6).sum()),
    "px_lost_floor2_to_6_pct": round(100 * (1 - (real >= 6).sum() / max(1, n)), 2),
    "energy_share_of_top_1pct_amplitude": round(float(cum[max(0, int(0.01 * n) - 1)]), 5),
    "energy_share_of_top_10pct_amplitude": round(float(cum[max(0, int(0.10 * n) - 1)]), 5),
    "energy_share_of_bottom_50pct_amplitude": round(float(1 - cum[max(0, int(0.50 * n) - 1)]), 6),
    "amp_p50": round(float(np.percentile(amps, 50)), 2),
    "amp_p99": round(float(np.percentile(amps, 99)), 2),
    "amp_max": round(float(amps.max()), 2),
}
report["E5_floor_stability_explained"] = e5

# --- E6: sub-floor spill (L5) ----------------------------------------------
e6 = {}
for mk in MARKS:
    fxp, ctp = f"{WWCR}/combat_fxon_{mk}.png", f"{WWCR}/combat_fxctl_{mk}.png"
    if not (os.path.exists(fxp) and os.path.exists(ctp)):
        continue
    d = delta_field(mk)
    e6[mk] = {
        "byte_identical": bool(d.max() == 0),
        "max_delta": int(d.max()),
        "px_delta_ge1": int((d >= 1).sum()),
        "px_delta_1_only": int(((d >= 1) & (d < 2)).sum()),
        "px_delta_ge2": int((d >= 2).sum()),
        "px_delta_2_to_5": int(((d >= 2) & (d < 6)).sum()),
        "px_delta_ge6": int((d >= 6).sum()),
        "px_delta_ge32": int((d >= 32).sum()),
        "faint_px_share_of_authored_at_floor1": round(
            float(((d >= 1) & (d < 6)).sum() / max(1, (d >= 1).sum())), 4),
    }
report["E6_subfloor_spill"] = e6

with open(os.path.join(OUT, "p2_fitness.json"), "w") as fh:
    json.dump(report, fh, indent=2)

# ------------------------- console ------------------------------------------
def row(s):
    return (f"  {s['label']:34s} px={s['authored_px']:>8d} "
            f"fine(b0b1)={s['fine_b0b1']:.4f}  coarse(b3+)={s['coarse_b3plus']:.4f}"
            f"  amp={s['mean_amp']:.1f}")

print("\n=== E1  AMPLITUDE WEIGHTING ===")
for k, v in report["E1_amplitude_weighting"].items():
    if k.startswith("_"):
        print(" ", k, v)
    else:
        print(row(v))

print("\n=== E2  TRANSFER CURVE  (equal amplitude; area frac -> band share) ===")
for s in report["E2_transfer_curve"]:
    print(f"  authored coarse AREA {s['coarse_AREA_frac_authored']:.3f}"
          f"  ->  coarse BAND share {s['coarse_b3plus']:.4f}   (fine {s['fine_b0b1']:.4f})")

print("\n=== E3  GAMEABILITY ===")
for k, v in report["E3_gameability"].items():
    print(row(v))

print("\n=== E4  RASTER PORTABILITY ===")
for s in report["E4_raster_portability"]:
    print(f"  {s['raster']:>10s}  fine={s['fine_b0b1']:.4f}  coarse={s['coarse_b3plus']:.4f}"
          f"  px={s['authored_px']}")

print("\n=== E5  WHY FLOOR-STABLE ===")
for k, v in e5.items():
    print(f"  {k:44s} {v}")

print("\n=== E6  SUB-FLOOR SPILL ===")
print(f"  {'mark':18s} {'byteid':>7s} {'max':>5s} {'>=1':>9s} {'==1':>9s} {'2-5':>8s} {'>=6':>8s} {'>=32':>7s}")
for k, v in e6.items():
    print(f"  {k:18s} {str(v['byte_identical']):>7s} {v['max_delta']:>5d} "
          f"{v['px_delta_ge1']:>9d} {v['px_delta_1_only']:>9d} {v['px_delta_2_to_5']:>8d} "
          f"{v['px_delta_ge6']:>8d} {v['px_delta_ge32']:>7d}")

print(f"\nwrote {os.path.join(OUT, 'p2_fitness.json')}")
