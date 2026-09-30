#!/usr/bin/env python3
"""C-9 T10-2 -- THE PAINTED BARROW'S PHONE PAGE, MEASURED AGAINST THE DESKTOP. drax.

    python3 tools/web_compare.py

Collects, into take/build/web_vs_desktop.json:
  the PROBES that decided the web path (work/probe/): the two suns' masks on Compatibility, and the
    MultiMesh vertex-colour trap;
  the SAME FRAMES on both renderers (godot/tools/capture_painted.gd --stills --quiet, desktop Forward+
    against Compatibility on ANGLE/Metal with the web branches and the phone data): mean |difference|
    per still, 0-255;
  the THREE MEETING RULES on both: his shadow's core on the painting (--shadow-test, the paint sun's
    setting in use), him darkened in ring_m55's painted shadow (--stills), the trail polish (--trail);
  the PAGE in the browser (tools/web_painted_test.js at 844 x 390 CSS px @3x, Chrome's GPU): the first
    download (brotli, as Vercel serves it: tools/web_br_server.js's log), the load at 40 Mbit/s, the
    frame rate by phase.
"""
import glob
import json
import os
import re

import numpy as np
from PIL import Image

BF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(BF, "captures", "painted")
CMP = os.path.join(CAP, "web_cmp")


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def rgb(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float64)


def shadow_core(folder, cfg, him_px):
    hx, hy = him_px
    x0, y0, x1, y1 = int(hx - 150), int(hy - 250), int(hx + 350), int(hy + 150)
    on = s2l(rgb(os.path.join(folder, "shadow_%s_on.png" % cfg))[y0:y1, x0:x1] / 255.0)
    off = s2l(rgb(os.path.join(folder, "shadow_%s_off.png" % cfg))[y0:y1, x0:x1] / 255.0)
    ratio = on / np.maximum(off, 1e-4)
    lum = ratio @ np.array([0.2126, 0.7152, 0.0722])
    aff = lum < 0.95
    core = lum <= np.percentile(lum[aff], 25)
    return {"px_darkened_over_5pct": int(aff.sum()), "core_ratio_linear": [round(float(v), 3) for v in ratio[core].mean(0)]}


def trail(folder):
    U, M1, ID = (rgb(os.path.join(folder, n)) for n in ("trail_untouched.png", "trail_mode1.png", "trail_id.png"))
    M0 = rgb(os.path.join(folder, "trail_mode0.png"))
    t = (ID[..., 0] > 8) | (ID[..., 1] > 8)
    out = {"trail_px": int(t.sum())}
    for nm, M in (("first_version", M0), ("polish", M1)):
        d = M[t] - U[t]
        out[nm] = {"mean_signed_rgb": [round(float(x), 2) for x in d.mean(0)], "mean_abs": round(float(np.abs(d).mean()), 2)}
    return out


def main():
    out = {"_what": "C-9 T10-2: the painted Barrow's phone page (/playtest/barrow-painted/), measured against the desktop"}
    pr = {}
    for f in ("probe_paint_light_compat.json", "probe_mm_compat.json", "probe_mm_fwd.json"):
        p = os.path.join(BF, "work", "probe", f)
        if os.path.exists(p):
            pr[f] = json.load(open(p))
    out["probes"] = pr
    stills = {}
    for p in sorted(glob.glob(os.path.join(CMP, "desk", "*.png"))):
        n = os.path.basename(p)[:-4]
        w = os.path.join(CMP, "web", n + ".png")
        if not os.path.exists(w):
            continue
        d = rgb(w) - rgb(p)
        stills[n] = {"mean_abs_0_255": round(float(np.abs(d).mean()), 2),
                     "mean_signed_rgb": [round(float(x), 2) for x in d.reshape(-1, 3).mean(0)]}
    out["same_frames_web_minus_desktop"] = stills
    rules = {}
    dj = json.load(open(os.path.join(CMP, "desk", "capture_painted.json")))
    wj = json.load(open(os.path.join(CMP, "web", "capture_painted.json")))
    rules["b_him_in_a_painted_shadow_over_in_sun_linear"] = {
        "desktop": dj["him_in_a_painted_shadow"]["shadow_over_sun_linear"],
        "web": wj["him_in_a_painted_shadow"]["shadow_over_sun_linear"]}
    ds = json.load(open(os.path.join(CAP, "capture_painted.json")))
    ws = json.load(open(os.path.join(CMP, "web_shadow", "capture_painted.json")))
    rules["a_his_shadow_core_on_the_painting_linear"] = {
        "painters_own": [0.4188, 0.5479, 0.8918],
        "desktop_G": shadow_core(CAP, "G_ortho68_blur06", ds.get("shadow_test", {}).get("him_screen_px", [960, 595])),
        "web_G": shadow_core(os.path.join(CMP, "web_shadow"), "G_ortho68_blur06", ws["shadow_test"]["him_screen_px"])}
    rules["c_no_static_shadow_on_the_painting"] = {
        "compatibility_probe_painted_receiver": pr.get("probe_paint_light_compat.json", {}).get("light_layers", {}).get("probes", {}),
        "_read": "painted_under_STATIC_shadow reads as painted_open (the static caster leaves it untouched); painted_under_HIM_shadow darkens"}
    rules["trail_polish"] = {"desktop": trail(os.path.join(CAP, "trail")), "web": trail(os.path.join(CMP, "web_trail"))}
    out["meeting_rules"] = rules
    runs = {}
    for p in sorted(glob.glob(os.path.join(CAP, "web_test", "w40*", "report.json"))):
        r = json.load(open(p))
        runs[os.path.basename(os.path.dirname(p))] = {
            "in_page_ms_from_navigation": r["in_page_ms_from_navigation"],
            "fps_samples": [(s["phase"], s["fps"]) for s in r["fps_samples"]],
            "errors": len(r["errors"]), "gear_tap_changed_clip_set": r["gear_tap_changed_clip_set"],
            "webgl_renderer": r["webgl_renderer"], "canvas_px": r["canvas_px"]}
    sent = {}
    for l in open(os.path.join(CAP, "web_test", "br_server.log")):
        m = re.search(r' (/playtest/barrow-painted/\S*) ae="[^"]*" sent=(\d+) (\S+)', l)
        if m:
            sent[m.group(1).split("/")[-1] or "index.html"] = int(m.group(2))
    out["page"] = {"first_download_bytes_brotli": sum(sent.values()), "files": sent,
                   "_instrument": "tools/web_br_server.js (brotli q4 on .wasm/.pck/.js/.html, as Vercel measured) serving the staged page; tools/web_painted_test.js: Chrome, its GPU (ANGLE on Metal, Apple M2 -- NOT a phone), 844 x 390 CSS px at devicePixelRatio 3, touch, the network throttled through CDP to 40 Mbit/s and 20 ms, the cache off; fps from the scene's own [fps] line every 2 s. The test takes a full-canvas screenshot in each phase, and the single low samples fall on those moments",
                   "runs_at_40_mbit": runs}
    out["phone_data"] = json.load(open(os.path.join(BF, "take", "build", "painted_web_prep.json")))
    json.dump(out, open(os.path.join(BF, "take", "build", "web_vs_desktop.json"), "w"), indent=1)
    print(json.dumps({"stills": stills, "rules": {k: v for k, v in rules.items() if k != "c_no_static_shadow_on_the_painting"},
                      "first_download_MB": round(sum(sent.values()) / 1e6, 2)}, indent=1))


if __name__ == "__main__":
    main()
