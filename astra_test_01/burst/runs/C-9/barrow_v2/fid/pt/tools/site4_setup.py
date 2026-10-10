#!/usr/bin/env python3
"""BV2F PT R-C9-384: set up the site_ph4 BUILD dir fid/pt/site4 from the site_ph3 one (fid/pt/site), changing ONLY what the
north band changes: the plate (6656 x 4864, the ph4 painting), the frame's top edge (v1' = v1 + 768 / (ppm sin pitch)),
the data set (site_ph4: level + painted out), the chunk list (every ph3 chunk + 768 rows, + the five band chunks).
    python3 fid/pt/tools/site4_setup.py
Root stubs are APFS clones of pt/site's; the ph3 bakes are cloned into site4/root/work/bakes and only models whose plate
reaches the band are re-baked (site4_build.sh bake, PT_BAKE_ONLY)."""
import hashlib
import json
import math
import os
import shutil
import subprocess

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C9 = os.path.dirname(os.path.dirname(FID))
S3, S4 = os.path.join(FID, "pt/site"), os.path.join(FID, "pt/site4")
PPM, PITCH = 100.617553710938, math.radians(52.95354112560294)
V1, BAND = 22.36993715728635, 768
V1N = V1 + BAND / (PPM * math.sin(PITCH))
D4 = os.path.join(C9, "barrow_full/godot/data/bv2f/site_ph4")


def sub(o):
    """site_ph3 -> site_ph4 and pt/site/ -> pt/site4/ in every string"""
    if isinstance(o, dict):
        return {k: sub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sub(v) for v in o]
    if isinstance(o, str):
        return o.replace("site_ph3", "site_ph4").replace("pt/site/", "pt/site4/")
    return o


def main():
    assert abs(V1N - 31.933163591268734) < 1e-9
    os.makedirs(S4, exist_ok=True)
    # frame grid (capture_ids)
    fg = json.load(open(os.path.join(S3, "frame_grid.site.json")))
    fg = sub(fg)
    fg["_what"] = "BV2F PT SITE4 frame/grid (R-C9-384): the site_ph3 frame + a 768 px north band (6656 x 4864); scene = bv2f_pilot.tscn with BV2F_PILOT=site_ph4"
    fg["name"] = "barrow_v2 art SITE (site_ph4)"
    fg["guide_px"] = [6656, 4096 + BAND]
    fg["env"]["BV2F_PILOT"] = "site_ph4"
    fg["guide_window_uv"]["v"] = [fg["guide_window_uv"]["v"][0], V1N]
    fg["guide_window_uv"]["centre"] = [fg["guide_window_uv"]["centre"][0], (fg["guide_window_uv"]["v"][0] + V1N) / 2]
    json.dump(fg, open(os.path.join(S4, "frame_grid.site4.json"), "w"), indent=1)
    # take / prep cfgs
    for n in ("fe_take.json", "fe_prep.json"):
        c = sub(json.load(open(os.path.join(S3, n))))
        c["_what"] = c.get("_what", "") + " -> SITE4 (site_ph4, R-C9-384: + 768 px north band)"
        c["frame"]["v1"] = V1N
        c["frame"]["px"] = [6656, 4096 + BAND]
        if "chunks" in c:
            ch = []
            for k in range(5):
                ch.append({"key": "%d_N" % k, "px": [k * 1280, 0, k * 1280 + 1536, 1024], "_": "R-C9-384 band chunk"})
            for e in c["chunks"]:
                e = dict(e)
                x0, y0, x1, y1 = e["px"]
                e["px"] = [x0, y0 + BAND, x1, y1 + BAND]
                ch.append(e)
            c["chunks"] = ch
        if "flat" in c:
            c["flat"]["_pin"] = "R-C9-384: site_ph4 level (fid/lv/tools/ph4_level.py; site_ph4/level/PIN.json)"
        json.dump(c, open(os.path.join(S4, n), "w"), indent=1)
    # root stubs: clones (the frame stub carries only the camera)
    for rel in ("root/barrow_full_layout.json", "root/godot/data/barrow_full_splat.bin", "root/take/ground/splat_world.png"):
        d = os.path.join(S4, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        subprocess.check_call(["cp", "-c", os.path.join(S3, rel), d])
    # the ph3 bakes, cloned (re-baked only where a model's plate reaches the band)
    b3, b4 = os.path.join(S3, "root/work/bakes"), os.path.join(S4, "root/work/bakes")
    os.makedirs(b4, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(b3)):
        if not os.path.exists(os.path.join(b4, f)):
            subprocess.check_call(["cp", "-c", os.path.join(b3, f), os.path.join(b4, f)])
            n += 1
    # the ph3 bake report with its texture paths moved to site4 (PT_BAKE_PREV for the merge)
    br = json.load(open(os.path.join(S3, "bake_report.json")))
    br = sub(br)
    br["_r_c9_384"] = "site4: the ph3 bake report, textures cloned into pt/site4/root/work/bakes; band models re-baked and merged"
    json.dump(br, open(os.path.join(S4, "bake_report_ph3_prev.json"), "w"), indent=1)
    os.makedirs(os.path.join(D4, "painted"), exist_ok=True)
    print("site4 set up: v1'", V1N, "bakes cloned", n)


if __name__ == "__main__":
    main()
