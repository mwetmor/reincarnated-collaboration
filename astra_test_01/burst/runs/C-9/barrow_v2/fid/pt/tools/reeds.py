#!/usr/bin/env python3
"""BV2F lane PT, DEV-21 (R-C9-205 (1)): THE REEDS -- the painting's OWN reed tufts at the mere / stream edges, cut out
as alpha cards (v1's heather-card method, cliffside3d/tools/barrow_heather_cards.py, re-run on the pilot painting) and
each stood back on the TRUE ground under its own base (DEV-18's ray / heightfield fixed point), to sway in the gusts.
    python3 fid/pt/tools/reeds.py [--config fid/pt/pilot/fe_prep.json] [--dry]
No v1 reed or grass CARD exists in barrow_full (its only grass is R-C9-158's cone blades, a negative control); v1's
heather-card mechanism is reused, so the reeds cost 0 images: the card IS the painted reed, at the painting's own scale
(no resampling: a tuft wider or taller than a tile is not a card).

WHICH TUFTS. Straw (Lab: 32 < L* < 90, b* > 12, a* < 12 -- straw-gold, not rust; a heather clump's lit tips can
pass it, hence the dark-ring test) on LAND ids, within NEAR_M of the mere / stream ids; closed 2 px; a component is a tuft when it is 80-6000 px,
at most TILE-2 px each way, not cut by the frame, at least 55% straw, its 6 px ring at most 12% dark (L* < 30: a heather clump's body -- its lit tips pass the straw colour). Its base = the mean x of its bottom 3 px rows.
ALPHA (v1's rule): 1 on the tuft, 0 on snow (bright and low-chroma, or the blue of snow / ice in shadow), a 1 px
half-alpha feather where not snow.
OUT (into the painted data dir): reeds_atlas.bin (the atlas's PNG bytes, as every painted texture ships) + reeds.json
(rows [x, z, ground_h, w_m, h_m, base_u, u0, v0, u1, v1]); the manifest gains "reeds" (file shas). Report: fid/pt/dev21/.
"""
import hashlib, json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_a = sys.argv[1:]
CFG = json.load(open(_a[_a.index("--config") + 1] if "--config" in _a else os.path.join(FID, "pt", "pilot", "fe_prep.json")))
DRY = "--dry" in _a
P_ = lambda v: v if os.path.isabs(v) else os.path.join(FID, v)
OUT = P_(CFG["out"])
REP_DIR = os.path.join(FID, "pt", "dev21")
U0, V1 = float(CFG["frame"]["u0"]), float(CFG["frame"]["v1"])
W, H = int(CFG["frame"]["px"][0]), int(CFG["frame"]["px"][1])
PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
PXV, PXH = PPM * math.sin(PITCH), PPM * math.cos(PITCH)
C47, S47 = math.cos(math.radians(47.0)), math.sin(math.radians(47.0))
TILE = 128
NEAR_M = 2.5
DARK_RING_MAX = 0.12
STRAW_L, STRAW_B, STRAW_A, DARK_L = (32, 90), 12, 12, 30
WATER_IDS = ["ground_ice", "ground_stream"]
LAND_IDS = ["ground_snow", "ground_shrub", "ground_mound", "ground_path"]


def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def srgb_to_lab(rgb):          # barrow_heather_cards.py, verbatim
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def uv_of_px(x, y, h=0.0):     # bv2f_prep.py (paint_world_prep.py:75)
    return U0 + x / PPM, V1 - (y + h * PXH) / PXV


def xz_of_uv(u, v):            # bv2f_prep.py (paint_world_prep.py:83)
    return u * C47 - v * S47, -u * S47 - v * C47


def main():
    P8 = np.asarray(Image.open(P_(CFG["painting"])).convert("RGB"))
    assert P8.shape[:2] == (H, W)
    IDS = json.load(open(P_(CFG["ids_dir"]) + "/ids.json"))
    ID8 = np.asarray(Image.open(P_(CFG["ids_dir"]) + "/ids.png").convert("RGB")).astype(np.int32)
    is_pl = ID8[..., 2] > 100
    idx = np.where(is_pl, np.clip(np.round((ID8[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
                   + np.clip(np.round((ID8[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
    idx_of = {v["id"]: int(k) for k, v in IDS["placements"].items()}
    water = np.isin(idx, [idx_of[i] for i in WATER_IDS if i in idx_of])
    land = np.isin(idx, [idx_of[i] for i in LAND_IDS if i in idx_of])
    near = ndimage.distance_transform_edt(~water) <= NEAR_M * PPM
    L = srgb_to_lab(P8.astype(np.float64) / 255.0)
    l, aa, bb = L[..., 0], L[..., 1], L[..., 2]
    c = np.hypot(aa, bb)
    straw = (l > STRAW_L[0]) & (l < STRAW_L[1]) & (bb > STRAW_B) & (aa < STRAW_A)
    snow = ((l > 74) & (c < 17)) | ((l > 52) & (bb < -3) & (c < 22))
    dark = (l < DARK_L) & land
    reg = straw & land & near
    reg = ndimage.binary_closing(reg, iterations=2) & land & near & ~snow
    # the ground under each base: DEV-18's ray / heightfield fixed point (bv2f_prep.py, heather_on_terrain)
    Lv = json.load(open(P_(CFG["flat"]["level"])))
    hf = Lv["sim"]["heightfield"]
    Hf = np.fromfile(os.path.join(os.path.dirname(P_(CFG["flat"]["level"])), hf["file"]), "<f4").reshape(hf["shape"])
    ex = hf["extent_sim_m"]

    def ground_h(u_, v_):
        return float(Hf[int(np.clip((-v_ - ex["y0"]) * hf["px_per_m"], 0, Hf.shape[0] - 1)),
                        int(np.clip((u_ - ex["x0"]) * hf["px_per_m"], 0, Hf.shape[1] - 1))])
    lab_r, n = ndimage.label(reg)
    cands, rej = [], {"area": 0, "size": 0, "frame": 0, "straw_share": 0, "heather_body": 0}
    for i, sl in enumerate(ndimage.find_objects(lab_r), start=1):
        if sl is None:
            continue
        m = lab_r[sl] == i
        area = int(m.sum())
        h_px, w_px = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if area < 80 or area > 6000:
            rej["area"] += 1
            continue
        if w_px + 4 > TILE - 2 or h_px + 4 > TILE - 2 or w_px < 6 or h_px < 8:
            rej["size"] += 1
            continue
        if sl[0].start <= 3 or sl[1].start <= 3 or sl[0].stop >= H - 3 or sl[1].stop >= W - 3:
            rej["frame"] += 1
            continue
        ss = float(straw[sl][m].mean())
        if ss < 0.55:
            rej["straw_share"] += 1
            continue
        # NOT A HEATHER CLUMP'S LIT TIPS: a reed tuft stands in snow / on rock; heather's pale sprig tips sit on the
        # clump's dark body (L* < 42) -- a tuft whose 6 px ring is more than DARK_RING_MAX dark is heather, not reed
        y0r, y1r = max(sl[0].start - 6, 0), min(sl[0].stop + 6, H)
        x0r, x1r = max(sl[1].start - 6, 0), min(sl[1].stop + 6, W)
        big = np.zeros((y1r - y0r, x1r - x0r), bool)
        big[sl[0].start - y0r:sl[0].stop - y0r, sl[1].start - x0r:sl[1].stop - x0r] = m
        ring = ndimage.binary_dilation(big, iterations=6) & ~big
        dk = float(dark[y0r:y1r, x0r:x1r][ring].mean()) if ring.any() else 1.0
        if dk > DARK_RING_MAX:
            rej["heather_body"] += 1
            continue
        cands.append({"i": i, "sl": sl, "area": area, "straw": ss})
    cands.sort(key=lambda d: (d["sl"][0].start, d["sl"][1].start))
    acc = np.isin(lab_r, [d["i"] for d in cands])
    cols = 16
    nrow = max((len(cands) + cols - 1) // cols, 1)
    atlas = np.zeros((nrow * TILE, cols * TILE, 4), np.uint8)
    rows, tiles = [], []
    for t, d in enumerate(cands):
        sl = d["sl"]
        y0, y1 = max(sl[0].start - 2, 0), min(sl[0].stop + 2, H)
        x0, x1 = max(sl[1].start - 2, 0), min(sl[1].stop + 2, W)
        m = lab_r[y0:y1, x0:x1] == d["i"]
        alpha = (m & ~snow[y0:y1, x0:x1]).astype(np.float64)
        alpha = np.maximum(alpha, 0.5 * (ndimage.binary_dilation(alpha > 0.5, iterations=1) & ~snow[y0:y1, x0:x1]))
        crop = np.dstack([P8[y0:y1, x0:x1], (alpha * 255).astype(np.uint8)])
        hh, ww = crop.shape[:2]
        r_, cc = divmod(t, cols)
        ox = cc * TILE + (TILE - ww) // 2
        oy = r_ * TILE + (TILE - hh)                  # base on the tile's bottom edge (v1)
        atlas[oy:oy + hh, ox:ox + ww] = crop            # the painting's own pixels, unresampled
        ys, xs = np.nonzero(m)
        bot = ys >= ys.max() - 2
        bx_px = float(x0 + xs[bot].mean() + 0.5)
        by_px = float(y0 + ys.max() + 1.0)              # the tuft's foot: the bottom edge of its lowest row
        gh = 0.0
        for _ in range(16):
            u, v = uv_of_px(bx_px, by_px, gh)
            gh = 0.5 * gh + 0.5 * ground_h(u, v)
        u, v = uv_of_px(bx_px, by_px, gh)
        x, z = xz_of_uv(u, v)
        base_u = (bx_px - x0) / ww
        # the card's own rest = the painting: its quad spans [x0, x1) x [y0, y1) on screen with its base at (bx_px, by_px)
        # -> the card is (y1 - by_px) px below the foot too (the 2 px apron): carried as a downward offset
        below_m = (y1 - by_px) / PPM
        uvr = [ox / atlas.shape[1], oy / atlas.shape[0], (ox + ww) / atlas.shape[1], (oy + hh) / atlas.shape[0]]
        rows.append([round(x, 4), round(z, 4), round(gh, 4), round(ww / PPM, 4), round(hh / PPM, 4), round(base_u, 4),
                     round(below_m, 4)] + [round(q, 6) for q in uvr])
        tiles.append({"src_box_px": [int(x0), int(y0), int(x1), int(y1)], "area_px": d["area"],
                      "straw_share": round(d["straw"], 3), "foot_px": [round(bx_px, 1), round(by_px, 1)]})
    # the heather's 3D sprays that stand on these tufts (prep's heather classifier also passes straw): measured, stated
    hj = json.load(open(os.path.join(OUT, "heather.json")))
    reg_d = ndimage.binary_dilation(acc, iterations=6)
    on_reed = 0
    for r in hj["rows"]:
        u = (r[0] * C47 - r[1] * S47)
        v = -(r[0] * S47 + r[1] * C47)
        gh = float(r[7]) if len(r) > 7 else 0.0
        px = (u - U0) * PPM
        py = (V1 - v) * PXV - (gh + 0.5 * float(r[2])) * PXH
        if 0 <= px < W and 0 <= py < H and reg_d[int(py), int(px)]:
            on_reed += 1
    rep = {"_what": "BV2F PT DEV-21: the reeds (fid/pt/tools/reeds.py)", "painting_sha256": sha_file(P_(CFG["painting"])),
           "tufts": len(rows), "components": int(n), "rejected": rej, "reed_px": int(acc.sum()), "candidate_px": int(reg.sum()),
           "straw_px_near_water_on_land": int((straw & land & near).sum()),
           "heather_sprays_standing_on_reed_tufts": [on_reed, len(hj["rows"])],
           "atlas_px": [int(atlas.shape[1]), int(atlas.shape[0])],
           "h_m": [round(float(np.min([r[4] for r in rows])), 3), round(float(np.max([r[4] for r in rows])), 3)] if rows else None,
           "ground_h_m": [round(float(np.min([r[2] for r in rows])), 3), round(float(np.max([r[2] for r in rows])), 3)] if rows else None,
           "tiles": tiles}
    os.makedirs(REP_DIR, exist_ok=True)
    Image.fromarray(np.where(acc[..., None], P8, (P8 * 0.35).astype(np.uint8))[::2, ::2]).save(os.path.join(REP_DIR, "reed_mask_preview.jpg"), quality=80)
    if not DRY:
        ap = os.path.join(OUT, "reeds_atlas.bin")
        Image.fromarray(atlas, "RGBA").save(ap, format="PNG")
        jp = os.path.join(OUT, "reeds.json")
        json.dump({"_what": "DEV-21: the painting's own reed tufts as cards at the mere / stream edges (fid/pt/tools/reeds.py)",
                   "columns": ["x", "z", "ground_h", "w_m", "h_m", "base_u", "below_m", "u0", "v0", "u1", "v1"],
                   "rows": rows}, open(jp, "w"), indent=0)
        mp = os.path.join(OUT, "manifest.json")
        man = json.load(open(mp))
        man["reeds"] = {"file": "reeds.json", "sha256": sha_file(jp), "atlas": {"file": "reeds_atlas.bin", "sha256": sha_file(ap),
                        "px": [int(atlas.shape[1]), int(atlas.shape[0])]}, "count": len(rows),
                        "_": "DEV-21 (R-C9-205): the painting's own reed tufts, cut as cards (v1's heather-card method), each on its ground"}
        json.dump(man, open(mp, "w"), indent=1)
        rep["atlas_sha256"], rep["json_sha256"] = man["reeds"]["atlas"]["sha256"], man["reeds"]["sha256"]
    json.dump(rep, open(os.path.join(REP_DIR, "reeds_report.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k != "tiles"}))


if __name__ == "__main__":
    main()
