#!/usr/bin/env python3
"""barrow_v2 SW level (R-C9-159, lane BS): EACH MODEL PAINTED ONCE ON ITSELF -- a per-model bake on its own UVs.

    v2sw_model_bake.py views <name> <glb>         four views of the model ALONE at the game's pitch (azimuths 0/90/180/270),
                                                  a 2 x 2 sheet (1536 x 1024, #00ff00 ground) for the painter, its baked
                                                  tufts taken back to rock colour (R-C9-159 clause 4: plants are never painted)
                                                  + the bake's inputs in barrow_full/work/ (t5_06b_bake.py's convention):
                                                  surf_v2sw_<name>.npz, layout_v2sw_<name>.json, _cells_v2sw_<name>/cell_<d>.png
    v2sw_model_bake.py bake <name> <painted.png>  barrow_full/tools/t5_06b_bake.py (byte-identical, density x facing^4 in
                                                  linear light) -> barrow_full/godot/data/barrow_v2_sw/bakes/<name>.png

Everything is in the GLB's own frame (one node, no transform: the normalised builds), so the cell cameras, the
surface file and the vertices agree by construction; the bake's own self-test checks it.
"""
import json, sys, struct, io, pathlib, subprocess
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
BF = ROOT.parent / "barrow_full"
WORK = BF / "work"
OUTD = BF / "godot/data/barrow_v2_sw/bakes"
SHEETD = ROOT / "paint/v1cam/models"
PITCH = np.radians(52.95354112560294)
CW, CH = 768, 512
AZ = {"a000": 0.0, "a090": 90.0, "a180": 180.0, "a270": 270.0}
CELL_XY = {"a000": (0, 0), "a090": (768, 0), "a180": (0, 512), "a270": (768, 512)}
SIZE = 1024


def read_glb(path):
    b = open(path, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n])
    bin_off = 20 + n + 8
    blob = b[bin_off:]

    def acc(i, comp):
        a = j["accessors"][i]
        bv = j["bufferViews"][a["bufferView"]]
        dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a["componentType"]]
        k = {"SCALAR": 1, "VEC2": 2, "VEC3": 3}[a["type"]]
        off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        arr = np.frombuffer(blob, dt, a["count"] * k, off).reshape(a["count"], k) if k > 1 else np.frombuffer(blob, dt, a["count"], off)
        return arr.astype(np.float64 if dt == np.float32 else np.int64)
    p = j["meshes"][0]["primitives"][0]
    V = acc(p["attributes"]["POSITION"], 3)
    N = acc(p["attributes"]["NORMAL"], 3)
    UV = acc(p["attributes"]["TEXCOORD_0"], 2)
    I = acc(p["indices"], 1).reshape(-1, 3)
    img = None
    if j.get("images"):
        im = j["images"][0]
        bv = j["bufferViews"][im["bufferView"]]
        img = Image.open(io.BytesIO(blob[bv.get("byteOffset", 0):bv.get("byteOffset", 0) + bv["byteLength"]])).convert("RGB")
    return V, N, UV, I, img


def detuft(img):
    """the baked tufts (red, rust, orange leafy patches) back to the image's own rock colour"""
    a = np.asarray(img).astype(np.float32) / 255
    r, g, bl = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - bl) / d) % 6, np.where(mx == g, (bl - r) / d + 2, (r - g) / d + 4)) * 60
    s = d / (mx + 1e-6)
    tuft = ((h <= 38) | (h >= 330)) & (s >= 0.30) & (mx >= 0.18)
    rock = np.median(a[~tuft & (s < 0.35) & (mx > 0.25) & (mx < 0.85)], axis=0)
    from scipy.ndimage import binary_dilation, gaussian_filter
    m = gaussian_filter(binary_dilation(tuft, iterations=2).astype(np.float32), 1.5)[..., None]
    lum = a.mean(-1, keepdims=True)
    out = a * (1 - m) + (rock * (0.75 + 0.5 * lum / max(rock.mean(), 1e-3))) * m
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)), float(tuft.mean())


def cam(az_deg):
    az = np.radians(az_deg)
    vdir = np.array([np.sin(az) * np.cos(PITCH), np.sin(PITCH), np.cos(az) * np.cos(PITCH)])
    f = -vdir
    right = np.cross(f, [0, 1, 0]); right /= np.linalg.norm(right)
    up = np.cross(right, f); up /= np.linalg.norm(up)
    return vdir, right, up


def raster(P2, Z, TRI, w, h):
    """z-buffer: P2 pixel coords per vertex, Z depth (bigger = nearer). Returns tri id map, barycentrics"""
    tid = -np.ones((h, w), np.int64)
    zb = np.full((h, w), -np.inf)
    bc = np.zeros((h, w, 3))
    for t, (a, b, c) in enumerate(TRI):
        pa, pb, pc = P2[a], P2[b], P2[c]
        x0, x1 = int(max(np.floor(min(pa[0], pb[0], pc[0])), 0)), int(min(np.ceil(max(pa[0], pb[0], pc[0])), w - 1))
        y0, y1 = int(max(np.floor(min(pa[1], pb[1], pc[1])), 0)), int(min(np.ceil(max(pa[1], pb[1], pc[1])), h - 1))
        if x1 < x0 or y1 < y0:
            continue
        den = (pb[1] - pc[1]) * (pa[0] - pc[0]) + (pc[0] - pb[0]) * (pa[1] - pc[1])
        if abs(den) < 1e-12:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l1 = ((pb[1] - pc[1]) * (xs - pc[0]) + (pc[0] - pb[0]) * (ys - pc[1])) / den
        l2 = ((pc[1] - pa[1]) * (xs - pc[0]) + (pa[0] - pc[0]) * (ys - pc[1])) / den
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        if not ins.any():
            continue
        z = l1 * Z[a] + l2 * Z[b] + l3 * Z[c]
        sub = zb[y0:y1 + 1, x0:x1 + 1]
        win = ins & (z > sub)
        sub[win] = z[win]
        tid[y0:y1 + 1, x0:x1 + 1][win] = t
        bsub = bc[y0:y1 + 1, x0:x1 + 1]
        bsub[win] = np.stack([l1[win], l2[win], l3[win]], -1)
    return tid, bc


def views(name, glb):
    V, N, UV, I, img = read_glb(glb)
    # the wreck carries no tufts: its red paint and wood are not plants (detuft would grey them)
    img, tuft_frac = (img, 0.0) if name.startswith('wreck') else detuft(img)
    T = np.asarray(img).astype(np.float32) / 255
    th, tw = T.shape[:2]
    lname = "v2sw_" + name
    (WORK / f"_cells_{lname}").mkdir(parents=True, exist_ok=True)
    SHEETD.mkdir(parents=True, exist_ok=True)
    sheet = np.zeros((1024, 1536, 3), np.float32)
    sheet[..., 1] = 1.0
    aim = (V.min(0) + V.max(0)) / 2
    cells = {}
    vis = {}
    ppm = None
    cams = {d: cam(az) for d, az in AZ.items()}
    for d, (vdir, right, up) in cams.items():       # one scale for all four cells (the views share it)
        ex = (V - aim) @ right
        ey = (V - aim) @ up
        s = min(CW * 0.9 / (ex.max() - ex.min()), CH * 0.9 / (ey.max() - ey.min()))
        ppm = s if ppm is None else min(ppm, s)
    for d, (vdir, right, up) in cams.items():
        P2 = np.stack([(V - aim) @ right * ppm + CW / 2, CH / 2 - (V - aim) @ up * ppm], 1)
        Z = (V - aim) @ vdir
        tid, bc = raster(P2, Z, I, CW, CH)
        on = tid >= 0
        tt = tid[on]
        uvp = (bc[on][:, :, None] * UV[I[tt]]).sum(1)
        nrm = (bc[on][:, :, None] * N[I[tt]]).sum(1)
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9
        tx = np.clip((uvp[:, 0] % 1) * tw, 0, tw - 1).astype(int)
        ty = np.clip((uvp[:, 1] % 1) * th, 0, th - 1).astype(int)
        col = T[ty, tx] * (0.70 + 0.30 * np.clip(nrm[:, 1], 0, 1))[:, None]
        cell = np.zeros((CH, CW, 3), np.float32); cell[..., 1] = 1.0
        cell[on] = col
        x0, y0 = CELL_XY[d]
        sheet[y0:y0 + CH, x0:x0 + CW] = cell
        rgba = np.dstack([(cell * 255).astype(np.uint8), (on * 255).astype(np.uint8)])
        Image.fromarray(rgba, "RGBA").save(WORK / f"_cells_{lname}" / f"cell_{d}.png")
        v = np.zeros(len(I), bool)
        v[np.unique(tt)] = True
        vis[f"vis_{lname}_{d}"] = v
        cells[d] = {"rect": [x0, y0, CW, CH], "px_per_m": ppm, "screen_right": right.tolist(), "screen_up": up.tolist(),
                    "aim": aim.tolist(), "view_dir": vdir.tolist(), "azimuth_deg": AZ[d]}
    Image.fromarray((sheet * 255).astype(np.uint8)).save(SHEETD / f"{name}_views.png")
    json.dump({"px_per_m": ppm, "elevation_deg": float(np.degrees(PITCH)), "cells": cells, "glb": str(glb),
               "tuft_fraction_detufted": round(tuft_frac, 4)}, open(WORK / f"layout_{lname}.json", "w"), indent=1)
    # the surface file: per texel, its triangle, world position and normal (v flipped as hero_surface.py does)
    UVp = np.stack([UV[:, 0] * SIZE, (1 - UV[:, 1]) * SIZE], 1)
    tex_tri = -np.ones((SIZE, SIZE), np.int64)
    tex_pos = np.zeros((SIZE, SIZE, 3), np.float32)
    tex_nrm = np.zeros((SIZE, SIZE, 3), np.float32)
    tid, bc = raster(UVp, np.zeros(len(V)), I, SIZE, SIZE)
    on = tid >= 0
    tt = tid[on]
    tex_tri[on] = tt
    tex_pos[on] = (bc[on][:, :, None] * V[I[tt]]).sum(1)
    nn = (bc[on][:, :, None] * N[I[tt]]).sum(1)
    tex_nrm[on] = nn / (np.linalg.norm(nn, axis=1, keepdims=True) + 1e-9)
    a, b, c = UVp[I[:, 0]], UVp[I[:, 1]], UVp[I[:, 2]]
    uv_area = 0.5 * np.abs((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (c[:, 0] - a[:, 0]) * (b[:, 1] - a[:, 1]))
    np.savez_compressed(WORK / f"surf_{lname}.npz", tex_tri=tex_tri, tex_pos=tex_pos, tex_nrm=tex_nrm, uv_area=uv_area,
                        V=V, TRI=I, size=np.array([SIZE]), **vis)
    print(json.dumps({"name": name, "tris": len(I), "ppm": round(ppm, 2), "uv_cover": round(float(on.mean()), 3),
                      "tufts_detufted": round(tuft_frac, 4), "sheet": str(SHEETD / f"{name}_views.png")}))


def bake(name, painted, key):
    lname = "v2sw_" + name
    OUTD.mkdir(parents=True, exist_ok=True)
    out = OUTD / f"{name}.png"
    # the painted sheet back to 1536 x 1024 (the cells' own frame)
    p = Image.open(painted).convert("RGB")
    if p.size != (1536, 1024):
        p = p.resize((1536, 1024), Image.LANCZOS)
    tmp = WORK / f"_cells_{lname}" / "painted_1536.png"
    p.save(tmp)
    subprocess.run(["python3", str(BF / "tools/t5_06b_bake.py"), str(WORK / f"surf_{lname}.npz"), str(out),
                    "--sheet", f"{lname}:{tmp}", "--erode", "3"], check=True)
    bj = OUTD / "bakes.json"
    d = json.loads(bj.read_text()) if bj.exists() else {}
    d[key] = out.name
    bj.write_text(json.dumps(d, indent=1))
    print("baked", key, "->", out)


if __name__ == "__main__":
    if sys.argv[1] == "views":
        views(sys.argv[2], sys.argv[3])
    else:
        bake(sys.argv[2], sys.argv[3], sys.argv[4])
