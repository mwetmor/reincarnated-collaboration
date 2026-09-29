#!/usr/bin/env python3
"""C-9 T10 — the numbers for the barrow render stack, read off the captured frames.

WHAT IS MEASURED, AND WHY EACH IS MEASURED THE WAY IT IS

1. THE LINE'S WIDTH IN PIXELS. Three estimators are computed and ALL THREE ARE CALIBRATED
   FIRST ON SYNTHETIC STRIPS OF KNOWN WIDTH AND KNOWN ANGLE, anti-aliased the way the real
   pass anti-aliases. A line-width number is exactly the kind of thing that comes back
   cleanly and wrong: a horizontal run-length is right on a vertical line and 1.41x too big
   on a diagonal one, and nothing in the output says which you had. The calibration table is
   printed with the result so the estimator can be checked rather than believed.

2. THE LINE'S COLOUR, per pen, from THE PIXELS THAT PEN ACTUALLY PAINTED. Each pen is
   isolated by a pair of frames that differ only in that pen being drawn, so no dark pixel
   has to be guessed at. ΔE is reported as CIE76 and CIE2000.

3. MIN LUMA, WITH THE INK EXCLUDED. The ink is the darkest thing in the frame BY DESIGN --
   0.113/0.082/0.067 -- so a "darkest pixel in the frame" number measures the pen, not the
   shadow, and would fail the no-pure-black test on a stack that is behaving perfectly.

4. THE SHADOW'S HUE, from the darkest tenth of the non-ink pixels, in Lab and HSV. b* must
   come back negative for a blue-violet shadow; a black shadow has a*=b*=0, so the sign is
   the test and the magnitude is the tuning.

   usage: barrow_metrics.py --dir CAPTURE_DIR [--json OUT.json]
"""
import argparse
import json
import pathlib
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

INK_SRGB = np.array([0.113, 0.082, 0.067])
LW = np.array([0.2126, 0.7152, 0.0722])


# --- colour spaces -----------------------------------------------------------
def srgb_to_linear(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(np.maximum(c, 0), 1 / 2.4) - 0.055)


def linear_to_lab(rgb):
    """D65. rgb is (..., 3) LINEAR sRGB in 0..1."""
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = np.tensordot(rgb, m.T, axes=1)
    white = np.array([0.95047, 1.0, 1.08883])
    t = xyz / white
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(np.maximum(t, 1e-12)), t / (3 * d * d) + 4.0 / 29.0)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], axis=-1)


def de76(lab1, lab2):
    return float(np.sqrt(np.sum((np.asarray(lab1) - np.asarray(lab2)) ** 2)))


def de2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cb = (C1 + C2) / 2.0
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25.0 ** 7))) if Cb > 0 else 0.5
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2
    C1p = np.hypot(a1p, b1)
    C2p = np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2.0))
    Lbp = (L1 + L2) / 2.0
    Cbp = (C1p + C2p) / 2.0
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2.0
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2.0
    else:
        hbp = (h1p + h2p - 360) / 2.0
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dth = 30 * np.exp(-(((hbp - 275) / 25.0) ** 2))
    Rc = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25.0 ** 7)) if Cbp > 0 else 0.0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / np.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -np.sin(np.radians(2 * dth)) * Rc
    return float(np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                         + Rt * (dCp / Sc) * (dHp / Sh)))


def rgb_to_hsv_one(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    d = mx - mn
    if d == 0:
        h = 0.0
    elif mx == r:
        h = (60 * ((g - b) / d)) % 360
    elif mx == g:
        h = 60 * ((b - r) / d) + 120
    else:
        h = 60 * ((r - g) / d) + 240
    return h, (d / mx if mx > 0 else 0.0), mx


# --- the ink mask ------------------------------------------------------------
def ink_strength(on_lin, off_lin, ink_lin):
    """Per-pixel ink coverage e, from  on = (1-e)*off + e*ink, solved by least squares over
    the three channels. In LINEAR light, because that is where the mix happened."""
    d = off_lin - ink_lin                       # (...,3)
    num = np.sum((off_lin - on_lin) * d, axis=-1)
    den = np.sum(d * d, axis=-1)
    e = np.where(den > 1e-6, num / np.maximum(den, 1e-9), 0.0)
    return np.clip(e, 0.0, 1.3)


def _run_sums(e, eps=0.02):
    """For every pixel, the SUM OF e over the maximal contiguous run of ink through it --
    once along its row, once along its column. Summing e rather than counting pixels makes
    the crossing width an anti-aliased quantity, so a 1.3 px line is 1.3 and not 1 or 2."""
    h = np.zeros_like(e)
    v = np.zeros_like(e)
    # `v.T` is a VIEW, so writing through it fills `v` in e's own shape -- and `v` is what
    # must come back. Returning `v.T` returned the transpose and broke on any non-square
    # frame. It passed the calibration because the calibration used SQUARE test images,
    # where a transpose is invisible; the strips are 240x320 now for exactly that reason.
    for arr, src in ((h, e), (v.T, e.T)):
        on = src > eps
        for i in range(src.shape[0]):
            row = src[i]
            m = on[i]
            if not m.any():
                continue
            lab, n = ndimage.label(m)
            sums = ndimage.sum_labels(row, lab, index=np.arange(1, n + 1))
            arr[i][m] = sums[lab[m] - 1]
    return h, v


def width_estimators(mask, mass=None):
    """FOUR, so they can disagree in front of you -- and the first one is the only one the
    calibration table lets you quote below about 3 px.

    w_perp: a line at angle θ crossed along a ROW spans w/|sin θ| and along a COLUMN
    w/|cos θ|, so 1/h² + 1/v² = 1/w² exactly, whatever θ is. No orientation assumption, no
    discretisation floor, and the anti-aliased profile is carried through because the runs
    sum coverage instead of counting pixels.

    The other three are kept because they are the obvious ones, and the calibration shows
    what happens if you trust them: the distance transform of a ONE-PIXEL-WIDE mask is 1.0
    everywhere, so 4*mean(DT) reports 4.0 -- cleanly, for every thin line there is."""
    mask = mask.astype(bool)
    n = int(mask.sum())
    if n == 0:
        return {"pixels": 0}
    dt = ndimage.distance_transform_edt(mask)
    er = ndimage.binary_erosion(mask, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool))
    perim = int((mask & ~er).sum())
    out = {"pixels": n, "boundary_px": perim,
           "w_dt_4xmeanDT_BIASED_below_3px": round(4.0 * float(dt[mask].mean()), 3),
           "w_area_perim_2A_P_BIASED_below_2px": round(2.0 * n / perim, 3) if perim else None}
    if mass is not None:
        m = np.clip(mass, 0.0, 1.0)
        h, v = _run_sums(m)
        sel = mask & (h > 0) & (v > 0)
        if sel.any():
            w = (h[sel] * v[sel]) / np.sqrt(h[sel] ** 2 + v[sel] ** 2)
            out["w_perp_median"] = round(float(np.median(w)), 3)
            out["w_perp_mean"] = round(float(w.mean()), 3)
            out["w_perp_p10_p90"] = [round(float(np.percentile(w, 10)), 3),
                                     round(float(np.percentile(w, 90)), 3)]
        out["ink_mass_px"] = round(float(m[mask].sum()), 1)
    return out


def synth_calibration():
    """THE INSTRUMENT, ON KNOWN CASES. Strips of exact width at three angles, anti-aliased
    by supersampling, run through the identical estimators. If a column here does not
    reproduce its own header, the number it produces on the real frame is not evidence."""
    rows = []
    ss = 8
    for true_w in (1.0, 1.35, 2.0, 3.0, 4.0):
        for ang in (0.0, 27.0, 45.0, 63.0, 90.0):
            H, W = 240, 320        # NON-SQUARE on purpose: see _run_sums
            yy, xx = np.mgrid[0:H * ss, 0:W * ss]
            xc = (xx + 0.5) / ss - W / 2.0
            yc = (yy + 0.5) / ss - H / 2.0
            th = np.radians(ang)
            # distance from a line through the centre at angle `ang`
            d = np.abs(-np.sin(th) * xc + np.cos(th) * yc)
            hi = (d <= true_w / 2.0).astype(np.float64)
            e = hi.reshape(H, ss, W, ss).mean(axis=(1, 3))       # the AA profile
            est = width_estimators(e >= 0.5, mass=e)
            rows.append({"true_w_px": true_w, "angle_deg": ang, **est})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    d = pathlib.Path(a.dir)

    def load(name):
        p = d / f"{name}.png"
        if not p.exists():
            return None
        return np.asarray(Image.open(p).convert("RGB"), dtype=np.float64) / 255.0

    need = ["barrow_stack_on", "barrow_stack_off", "barrow_nograde_ink_on",
            "barrow_nograde_ink_off", "barrow_nograde_hull_off", "barrow_stack_on_nopen"]
    imgs = {n: load(n) for n in need + ["barrow_ink_off", "barrow_snow_off",
                                        "barrow_char_ramp_on", "barrow_char_ramp_off",
                                        "barrow_char_original",
                                        "barrow_wide_on", "barrow_wide_off",
                                        "barrow_fog_off", "barrow_air_off"]}
    missing = [n for n in need if imgs.get(n) is None]
    if missing:
        print("missing frames: %s" % missing, file=sys.stderr)
        return 2

    rep = {"capture_dir": str(d)}
    ink_lin = srgb_to_linear(INK_SRGB)

    # ---- 0. the instruments, on known cases --------------------------------
    rep["instrument_check"] = {
        "_what": "width estimators on synthetic AA strips of known width and angle",
        "rows": synth_calibration(),
    }
    # the luma instrument, on an image whose minimum is known by construction
    probe = np.full((16, 16, 3), 0.5)
    probe[3, 4] = [0.02, 0.02, 0.02]
    pl = srgb_to_linear(probe) @ LW
    rep["instrument_check"]["luma_known_min"] = {
        "planted_srgb": 0.02, "measured_min_linear": round(float(pl.min()), 8),
        "expected_min_linear": round(float(srgb_to_linear(0.02) * LW.sum()), 8),
    }

    # ---- 1 + 2. the two pens ------------------------------------------------
    on_ss = srgb_to_linear(imgs["barrow_nograde_ink_on"])
    off_ss = srgb_to_linear(imgs["barrow_nograde_ink_off"])
    e_ss = ink_strength(on_ss, off_ss, ink_lin)
    hull_on = srgb_to_linear(imgs["barrow_nograde_ink_off"])
    hull_off = srgb_to_linear(imgs["barrow_nograde_hull_off"])
    e_hull = ink_strength(hull_on, hull_off, ink_lin)

    pens = {}
    for nm, e, frame_lin in (("screen_space", e_ss, on_ss), ("hull", e_hull, hull_on)):
        m_full = e >= 0.97
        m_line = e >= 0.5
        entry = {"width": width_estimators(m_line, mass=np.clip(e, 0, 1))}
        if m_full.sum() >= 30:
            med_lin = np.median(frame_lin[m_full], axis=0)
            med_srgb = linear_to_srgb(med_lin)
            lab = linear_to_lab(med_lin)
            entry["delivered_colour"] = {
                "full_strength_px": int(m_full.sum()),
                "srgb": [round(float(v), 4) for v in med_srgb],
                "hex": "#%02X%02X%02X" % tuple(int(round(max(0, min(1, v)) * 255)) for v in med_srgb),
                "lab": [round(float(v), 3) for v in lab],
                "dE76_vs_nominal_ink": round(de76(lab, linear_to_lab(ink_lin)), 3),
            }
        else:
            entry["delivered_colour"] = {"full_strength_px": int(m_full.sum()),
                                         "_note": "too few full-strength pixels to quote a colour"}
        pens[nm] = entry
    rep["pens"] = pens
    if all("srgb" in pens[k]["delivered_colour"] for k in ("screen_space", "hull")):
        l1 = pens["screen_space"]["delivered_colour"]["lab"]
        l2 = pens["hull"]["delivered_colour"]["lab"]
        rep["one_pen"] = {
            "dE76_screen_vs_hull": round(de76(l1, l2), 3),
            "dE2000_screen_vs_hull": round(de2000(l1, l2), 3),
            "requirement": "dE < 5",
            "verdict": "PASS" if de76(l1, l2) < 5 else "FAIL",
            "nominal_ink_srgb": [round(float(v), 4) for v in INK_SRGB],
        }

    # ---- 3 + 4. shadows -----------------------------------------------------
    on = imgs["barrow_stack_on"]
    on_lin = srgb_to_linear(on)
    luma = on_lin @ LW
    # THE MASK COMES FROM THE DELIVERED FRAME'S OWN PAIR, not from the nograde frames.
    # stack_on minus stack_on_nopen is both pens under exactly the conditions of the frame
    # being measured -- same grade, same paper, same pose. Built from the nograde frames it
    # was a mask of a different render, and the frame's darkest pixel came back as an ink
    # pixel the mask had missed, which reads as "the shadow is nearly black" when it is not.
    nopen_lin = srgb_to_linear(imgs["barrow_stack_on_nopen"])
    e_pens = ink_strength(on_lin, nopen_lin, ink_lin)
    ink_any = ndimage.binary_dilation(e_pens >= 0.12, iterations=2)
    body = ~ink_any
    sh = {}
    sh["frame_px"] = int(luma.size)
    sh["ink_and_skirt_px"] = int(ink_any.sum())
    sh["_mask_from"] = "barrow_stack_on minus barrow_stack_on_nopen (same grade, paper and pose)"
    sh["min_luma_linear_all_px"] = round(float(luma.min()), 6)
    sh["min_luma_linear_excluding_ink"] = round(float(luma[body].min()), 6)
    sh["p001_luma_excluding_ink"] = round(float(np.percentile(luma[body], 0.01)), 6)
    sh["pure_black_px_excluding_ink"] = int((luma[body] <= 1e-6).sum())
    sh["darkest_px_srgb_excluding_ink"] = [
        round(float(v), 4) for v in on[body][np.argmin(luma[body])]]
    q = np.percentile(luma[body], 10.0)
    dark = body & (luma <= q)
    mean_lin = on_lin[dark].mean(axis=0)
    mean_srgb = linear_to_srgb(mean_lin)
    lab = linear_to_lab(mean_lin)
    h, s, v = rgb_to_hsv_one([float(x) for x in mean_srgb])
    sh["shadow_band_darkest_10pct"] = {
        "px": int(dark.sum()),
        "mean_srgb": [round(float(x), 4) for x in mean_srgb],
        "hex": "#%02X%02X%02X" % tuple(int(round(max(0, min(1, x)) * 255)) for x in mean_srgb),
        "lab_L_a_b": [round(float(x), 2) for x in lab],
        "hsv_hue_deg": round(h, 1), "hsv_sat": round(s, 3),
        "b_star_negative_means_blue": bool(lab[2] < 0),
        "verdict_cool": "PASS" if lab[2] < -2.0 else "WARN: not measurably blue",
    }
    if imgs.get("barrow_stack_off") is not None:
        off = srgb_to_linear(imgs["barrow_stack_off"])
        lo = off @ LW
        dk = lo <= np.percentile(lo, 10.0)
        ms = linear_to_srgb(off[dk].mean(axis=0))
        lb = linear_to_lab(off[dk].mean(axis=0))
        sh["stack_off_for_comparison"] = {
            "min_luma_linear": round(float(lo.min()), 6),
            "darkest_10pct_mean_srgb": [round(float(x), 4) for x in ms],
            "lab_L_a_b": [round(float(x), 2) for x in lb],
        }
    rep["shadows"] = sh

    # ---- what the stack changed, frame-wide --------------------------------
    def stats(img):
        lin = srgb_to_linear(img)
        lu = lin @ LW
        return {"mean_srgb": [round(float(x), 4) for x in img.reshape(-1, 3).mean(axis=0)],
                "mean_luma_linear": round(float(lu.mean()), 5),
                "luma_p01": round(float(np.percentile(lu, 1)), 5),
                "luma_p99": round(float(np.percentile(lu, 99)), 5)}
    rep["frames"] = {k: stats(v) for k, v in imgs.items() if v is not None}
    # WHERE HE IS, so the character comparison is measured on HIM and not on 2 million
    # pixels of unchanged snow. The rect comes from his bones via the capture's own report.
    rect = None
    bj = d / "barrow.json"
    if bj.exists():
        try:
            rect = json.loads(bj.read_text()).get("char_rect_px")
        except Exception:
            rect = None
    for pair in (("barrow_stack_on", "barrow_stack_off"),
                 ("barrow_char_ramp_on", "barrow_char_ramp_off"),
                 ("barrow_char_ramp_on", "barrow_char_original"),
                 ("barrow_char_ramp_off", "barrow_char_original"),
                 ("barrow_stack_on", "barrow_snow_off"),
                 ("barrow_stack_on", "barrow_fog_off")):
        if imgs.get(pair[0]) is None or imgs.get(pair[1]) is None:
            continue
        d1 = np.abs(imgs[pair[0]] - imgs[pair[1]])
        entry = {"mean_abs_srgb": round(float(d1.mean()), 5),
                 "px_changed_gt_2_255": round(float((d1.max(axis=-1) > 2 / 255).mean()), 4)}
        if rect and "char" in pair[0] and imgs.get("barrow_char_noknight") is not None:
            x, y, w, h = [int(v) for v in rect]
            pad = 24
            x0, y0 = max(0, x - pad), max(0, y - pad)
            x1, y1 = min(d1.shape[1], x + w + pad), min(d1.shape[0], y + h + pad)
            sub = d1[y0:y1, x0:x1]
            ca = imgs[pair[0]][y0:y1, x0:x1]     # not `a`: that is the argparse namespace,
            cb = imgs[pair[1]][y0:y1, x0:x1]     # and shadowing it broke --json at the end
            # HIS SILHOUETTE, by differencing him out of the frame -- not his bounding box.
            nk = imgs["barrow_char_noknight"][y0:y1, x0:x1]
            him = np.abs(ca - nk).max(axis=-1) > 6 / 255
            him = ndimage.binary_erosion(him, iterations=1)   # drop the anti-aliased rim
            if him.sum() < 200:
                him = np.abs(ca - nk).max(axis=-1) > 3 / 255
            ca = ca[him]
            cb = cb[him]
            la = srgb_to_linear(ca) @ LW
            lb = srgb_to_linear(cb) @ LW
            entry["on_him_only"] = {
                "rect": [x0, y0, x1 - x0, y1 - y0],
                "silhouette_px": int(him.sum()),
                "mean_abs_srgb": round(float(sub.mean()), 5),
                "mean_luma_linear_a": round(float(la.mean()), 5),
                "mean_luma_linear_b": round(float(lb.mean()), 5),
                "mean_srgb_a": [round(float(v), 4) for v in ca.mean(axis=0)],
                "mean_srgb_b": [round(float(v), 4) for v in cb.mean(axis=0)],
                "p05_luma_a": round(float(np.percentile(la, 5)), 5),
                "p05_luma_b": round(float(np.percentile(lb, 5)), 5),
                "p95_luma_a": round(float(np.percentile(la, 95)), 5),
                "p95_luma_b": round(float(np.percentile(lb, 95)), 5),
            }
        rep.setdefault("pair_deltas", {})["%s_vs_%s" % pair] = entry

    # ---- the side-by-side crop Matt is shown -------------------------------
    if rect and imgs.get("barrow_char_original") is not None \
            and imgs.get("barrow_char_ramp_on") is not None:
        x, y, w, h = [int(v) for v in rect]
        pad = 46
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1 = min(imgs["barrow_char_ramp_on"].shape[1], x + w + pad)
        y1 = min(imgs["barrow_char_ramp_on"].shape[0], y + h + pad)
        panels = [("before  (his own materials)", "barrow_char_original"),
                  ("after  (watercolour ramp)", "barrow_char_ramp_on")]
        Z = 4                                    # a 162x97 man is unreadable at 1:1 on a sheet
        crops = [Image.fromarray(
            (np.clip(imgs[k][y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)
        ).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.NEAREST) for _, k in panels]
        cw, ch = crops[0].size
        gap, band = 14, 26
        sheet = Image.new("RGB", (cw * 2 + gap, ch + band), (250, 249, 246))
        for i, c in enumerate(crops):
            sheet.paste(c, (i * (cw + gap), band))
        from PIL import ImageDraw
        dr = ImageDraw.Draw(sheet)
        for i, (lab_txt, _) in enumerate(panels):
            dr.text((i * (cw + gap) + 6, 7), lab_txt, fill=(40, 30, 26))
        sheet.save(d / "barrow_char_before_after.png")
        rep["side_by_side"] = {"file": str(d / "barrow_char_before_after.png"),
                              "crop_rect": [x0, y0, x1 - x0, y1 - y0]}

    out = json.dumps(rep, indent=1)
    if a.json:
        pathlib.Path(a.json).write_text(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
