#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): THE PLATE FRAME -- one projection, one pixel grid, used by the
guide, the paint chunks, the take, the tiles, the cutouts and the preview.

    python3 tools/bvp_frame.py            -> paint/frame_bvp.json (+ paint/frame_bvp_envelope.png)

Camera of record (layout_v2.json `camera`, = reincarnated-godot/kc2_runtime/play/kc2play_projection.gd):
orthographic, pitch a = 52.9535411256029 deg, ZERO yaw, camera south of its target looking north.
    plate_X = P * x                      + X0      (P = plate px per metre, 100.617553710938, R-C9-149a)
    plate_Y = P * sin(a) * y - P * cos(a) * z + Y0
x east, y SOUTH, z up, origin = player start. (X0, Y0) = the plate pixel of sim (0, 0, 0); integers.

How much to paint: the camera is centred on the player's ground point and never clamps
(kc2_play/src/kc2p_main.gd `_place_camera`), so the screen can show anything within half a window
of the walkable floor. The widest window is ZOOM-GD (1920 x 1080 at 75.668 px/m = 25.374 x 14.273
screen-metres; ZOOM-HOUSE is smaller). The ENVELOPE is the floor (z = 0) dilated by that half
window + MARGIN_M on every side, in screen metres. Paint chunks wholly outside it are skipped.
"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
CAM = L["camera"]
A = math.radians(float(CAM["pitch_deg"]))
S, C = math.sin(A), math.cos(A)
P = float(CAM["ppm_plate"])                      # 100.617553710938
PPM_GD = float(CAM["ppm_zoom_gd"])               # 75.66840334752658
HALF_W = 1920 / PPM_GD / 2                       # 12.687 screen-m
HALF_H = 1080 / PPM_GD / 2                       # 7.137 screen-m
MARGIN_M = 1.5
CW, CH, SX, SY = 1536, 1024, 1280, 768           # Astra chunk canvas and stride (guided_paint.py)
TILE = 2048


def build():
    floor = [(float(p[0]), float(p[1])) for p in L["floor"]["polygon"]]
    fx = [p[0] for p in floor]
    fys = [S * p[1] for p in floor]                  # screen-metres
    dx, dy = HALF_W + MARGIN_M, HALF_H + MARGIN_M
    sx0, sx1 = min(fx) - dx, max(fx) + dx
    sy0, sy1 = min(fys) - dy, max(fys) + dy
    need_w = math.ceil((sx1 - sx0) * P)
    need_h = math.ceil((sy1 - sy0) * P)
    cols = max(1, math.ceil((need_w - CW) / SX) + 1)
    rows = max(1, math.ceil((need_h - CH) / SY) + 1)
    W = (cols - 1) * SX + CW
    H = (rows - 1) * SY + CH
    # centre the grid on the needed box; the origin pixel is an integer
    X0 = int(round(-sx0 * P + (W - need_w) / 2))
    Y0 = int(round(-sy0 * P + (H - need_h) / 2))
    # the envelope raster at 1/16 scale: floor polygon, dilated by the half-window rectangle
    k = 16
    env = Image.new("L", (W // k + 1, H // k + 1), 0)
    ImageDraw.Draw(env).polygon([((X0 + P * x) / k, (Y0 + P * S * y) / k) for x, y in floor], fill=255)
    e = np.asarray(env) > 0
    from scipy import ndimage
    rx, ry = int(math.ceil(dx * P / k)), int(math.ceil(dy * P / k))
    e = ndimage.binary_dilation(e, structure=np.ones((2 * ry + 1, 2 * rx + 1), bool))
    chunks, skipped = [], []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = c * SX, r * SY
            sub = e[y0 // k:(y0 + CH) // k + 1, x0 // k:(x0 + CW) // k + 1]
            key = f"{c}_{r}"
            row = {"key": key, "px": [x0, y0, x0 + CW, y0 + CH],
                   "sim_x_m": [round((x0 - X0) / P, 4), round((x0 + CW - X0) / P, 4)],
                   "sim_y_m_at_z0": [round((y0 - Y0) / (P * S), 4), round((y0 + CH - Y0) / (P * S), 4)]}
            (chunks if sub.any() else skipped).append(row)
    tiles = []
    for ty in range(math.ceil(H / TILE)):
        for tx in range(math.ceil(W / TILE)):
            x0, y0 = tx * TILE, ty * TILE
            sub = e[y0 // k:(y0 + TILE) // k + 1, x0 // k:(x0 + TILE) // k + 1]
            if not sub.any():
                continue
            tiles.append({"id": f"t{tx:02d}_{ty:02d}", "px": [x0, y0, min(W, x0 + TILE), min(H, y0 + TILE)]})
    fr = {
        "_what": "barrow_v2 paint plate frame (lane BVP, drax). Every BVP pixel lives on this grid.",
        "camera_source": CAM["source"], "camera_source_sha256": CAM["source_sha256"],
        "pitch_deg": CAM["pitch_deg"], "yaw_deg": 0.0, "projection": "orthographic",
        "law": "plate_X = P*x + X0 ; plate_Y = P*sin(a)*y - P*cos(a)*z + Y0  (x east, y SOUTH, z up, metres; origin = player start)",
        "px_per_m": P, "px_per_m_x": P, "px_per_ground_m_y": P * S, "px_per_m_up": P * C,
        "origin_px": [X0, Y0], "size_px": [W, H],
        "screen_window_zoom_gd_screen_m": [2 * HALF_W, 2 * HALF_H], "margin_m": MARGIN_M,
        "envelope_rule": "floor (z=0) dilated by the ZOOM-GD half window + margin, in screen metres; the camera follows the player's ground point unclamped (kc2p_main.gd _place_camera)",
        "envelope_screen_m": {"x": [round(sx0, 3), round(sx1, 3)], "y": [round(sy0, 3), round(sy1, 3)]},
        "chunk": {"canvas": [CW, CH], "stride": [SX, SY], "cols": cols, "rows": rows,
                  "painted": len(chunks), "skipped": len(skipped)},
        "chunks": chunks, "skipped_chunks": [s["key"] for s in skipped],
        "tile": TILE, "tiles": tiles,
    }
    return fr, e, k


def to_px(fr, x, y, z=0.0):
    X0, Y0 = fr["origin_px"]
    return X0 + P * x, Y0 + P * S * y - P * C * z


def main():
    fr, e, k = build()
    out = os.path.join(BV2, "paint", "frame_bvp.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(fr, open(out, "w"), indent=1)
    W, H = fr["size_px"]
    im = Image.new("RGB", (W // k + 1, H // k + 1), (40, 48, 60))
    a = np.asarray(im).copy(); a[e] = (150, 150, 140); im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    floor = [to_px(fr, float(p[0]), float(p[1])) for p in L["floor"]["polygon"]]
    d.polygon([(x / k, y / k) for x, y in floor], outline=(0, 0, 0), fill=(225, 225, 215))
    for ch in fr["chunks"]:
        x0, y0, x1, y1 = ch["px"]; d.rectangle([x0 / k, y0 / k, x1 / k, y1 / k], outline=(200, 120, 20))
    for t in fr["tiles"]:
        x0, y0, x1, y1 = t["px"]; d.rectangle([x0 / k, y0 / k, x1 / k, y1 / k], outline=(40, 90, 200))
    for p in L["anchors"]["points"]:
        x, y = to_px(fr, p["x"], p["y"]); d.ellipse([x / k - 3, y / k - 3, x / k + 3, y / k + 3], fill=(200, 30, 30))
    im.save(os.path.join(BV2, "paint", "frame_bvp_envelope.png"))
    print(json.dumps({k2: fr[k2] for k2 in ("origin_px", "size_px", "chunk")}), "tiles", len(fr["tiles"]))
    print("skipped:", fr["skipped_chunks"])


if __name__ == "__main__":
    main()
