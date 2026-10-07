#!/usr/bin/env python3
"""BV2F LV 0.2: the mechanical decision (R-C9-163 I-2) + the side-by-side overlay.
Bearings of the six anchors from the start, ON SCREEN (deg CCW from screen-right): sketch A (sketch_anchor_px.json)
vs the play-camera render (Godot's own cam.unproject_position, render_<tag>.json). PASS = same cyclic order AND
every |delta| <= 15 deg. Also a similarity (scale+rotation+translation) fit of render -> sketch: the residual
rotation is the frame's orientation error in one number. Writes frame_proof/bearings.json + overlay_*.png."""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FP = os.path.join(HERE, "frame_proof")
S = json.load(open(os.path.join(FP, "sketch_anchor_px.json")))
IDS = ["p01", "p02", "p03", "p04", "p05", "p06"]


def bearings(px, start):
    return {k: math.degrees(math.atan2(-(px[k][1] - start[1]), px[k][0] - start[0])) % 360 for k in IDS}


def cyc(b):
    return [k for k, _ in sorted(b.items(), key=lambda t: t[1])]


def same_cycle(a, b):
    i = b.index(a[0])
    return a == b[i:] + b[:i]


def simfit(src, dst):
    s = np.array(src, float); d = np.array(dst, float)
    sc, dc = s.mean(0), d.mean(0)
    zs = (s - sc)[:, 0] + 1j * (s - sc)[:, 1]
    zd = (d - dc)[:, 0] + 1j * (d - dc)[:, 1]
    k = (np.conj(zs) @ zd) / (np.conj(zs) @ zs)
    res = zd - k * zs
    return math.degrees(math.atan2(-k.imag, k.real)), abs(k), float(np.sqrt(np.mean(np.abs(res) ** 2)))   # screen y down: CCW = -arg


sb = bearings(S, S["start"])
rep = {"sketch_bearing_deg": {k: round(v, 1) for k, v in sb.items()}, "sketch_cyclic_order": cyc(sb), "renders": {}}
ok_fixed = None
for tag in ("fixed", "r159"):
    R = json.load(open(os.path.join(FP, f"render_{tag}.json")))
    px = R["screen_px"]
    rb = bearings(px, px["start"])
    delta = {k: round(((rb[k] - sb[k] + 180) % 360) - 180, 1) for k in IDS}
    order_ok = same_cycle(cyc(rb), cyc(sb))
    within = all(abs(v) <= 15.0 for v in delta.values())
    rot, scale, rms = simfit([px[k] for k in ["start"] + IDS], [S[k] for k in ["start"] + IDS])
    rep["renders"][tag] = {"yaw_deg": R["yaw_deg"], "bearing_deg": {k: round(v, 1) for k, v in rb.items()}, "delta_deg": delta,
                           "cyclic_order": cyc(rb), "cyclic_order_matches": order_ok, "all_within_15": within,
                           "PASS": order_ok and within, "similarity_fit": {"rotation_deg": round(rot, 1), "scale": round(scale, 3), "rms_px_sketch": round(rms, 1)}}
    if tag == "fixed":
        ok_fixed = order_ok and within
    print(tag, json.dumps(rep["renders"][tag]))
rep["decision_I2"] = "PASS" if ok_fixed else "FAIL"
json.dump(rep, open(os.path.join(FP, "bearings.json"), "w"), indent=1)

# --- overlay images ---------------------------------------------------------------------------------------
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
    small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
except Exception:
    font = small = ImageFont.load_default()
sk = Image.open(os.path.join(HERE, "..", "..", "sites", "BV3r2-A_spawns.png")).convert("RGB")
for tag in ("fixed", "r159"):
    R = json.load(open(os.path.join(FP, f"render_{tag}.json")))
    px = R["screen_px"]
    rd = Image.open(os.path.join(FP, f"render_{tag}.png")).convert("RGB")
    H = 1024
    rd = rd.resize((round(rd.width * H / rd.height), H))
    f = H / R["viewport"][1]
    W = sk.width + rd.width + 20
    can = Image.new("RGB", (W, H + 70), (20, 20, 24))
    can.paste(sk, (0, 70)); can.paste(rd, (sk.width + 20, 70))
    d = ImageDraw.Draw(can)
    r = rep["renders"][tag]
    d.text((10, 8), f"LEFT sketch A (BV3r2-A_spawns, not to scale)   RIGHT play camera (v1 pitch 52.95, yaw 47), site yaw {R['yaw_deg']:+.0f}: "
           f"{'THE FIX' if tag == 'fixed' else 'R-C9-159 (unrotated) NEGATIVE CONTROL'}", fill=(255, 255, 255), font=small)
    d.text((10, 36), f"I-2 bearings: cyclic order {'MATCH' if r['cyclic_order_matches'] else 'MISMATCH'}; max |delta| "
           f"{max(abs(v) for v in r['delta_deg'].values()):.1f} deg  ->  {'PASS' if r['PASS'] else 'FAIL'}   "
           f"(similarity-fit rotation {r['similarity_fit']['rotation_deg']:+.1f} deg)", fill=(120, 255, 120) if r["PASS"] else (255, 110, 110), font=small)
    # rays from the start to each anchor, in each panel (sketch: gold; render: cyan) + the sketch's rays ghosted on the render
    ss = S["start"]
    so = (sk.width + 20, 0)
    rs = (px["start"][0] * f + so[0], px["start"][1] * f + 70)
    for k in IDS:
        d.line([(ss[0], ss[1] + 70), (S[k][0], S[k][1] + 70)], fill=(255, 220, 0), width=4)
        d.text((S[k][0] + 8, S[k][1] + 70 - 30), f"{k} {sb[k]:.0f}°", fill=(255, 255, 0), font=font, stroke_width=3, stroke_fill=(0, 0, 0))
        e = (px[k][0] * f + so[0], px[k][1] * f + 70)
        d.line([rs, e], fill=(0, 255, 255), width=4)
        L = 0.9 * math.hypot(e[0] - rs[0], e[1] - rs[1])
        t = math.radians(sb[k])
        d.line([rs, (rs[0] + L * math.cos(t), rs[1] - L * math.sin(t))], fill=(255, 220, 0), width=2)
        d.text((e[0] + 8, e[1] - 30), f"{k} {r['bearing_deg'][k]:.0f}° (Δ{r['delta_deg'][k]:+.0f})", fill=(0, 255, 255), font=small, stroke_width=3, stroke_fill=(0, 0, 0))
    can.save(os.path.join(FP, f"overlay_{tag}.png"))
print("decision I-2:", rep["decision_I2"])
sys.exit(0 if ok_fixed else 1)
