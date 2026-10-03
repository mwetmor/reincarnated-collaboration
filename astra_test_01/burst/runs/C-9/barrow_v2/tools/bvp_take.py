#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): THE TAKE -- the painted plate cut into what kc2_play draws.

    python3 tools/bvp_take.py stitch                 paint/barrow_v2_painted.png (RGBA; alpha = painted coverage)
    python3 tools/bvp_take.py groups                 take/ids/ids_groups.json (which features become cutouts)
    python3 tools/bvp_take.py ids CAPDIR             take/ids/ids.png + gid.png (the ID capture, assembled + decoded)
    python3 tools/bvp_take.py tiles                  take/ground/tiles/*.png + take/ground/tiles.json
    python3 tools/bvp_take.py cut                    take/cutouts/*.png + take/cutouts/cutouts.json
    python3 tools/bvp_take.py classmap               take/ground_class/*
    python3 tools/bvp_take.py anchors                take/doors.json
Frame: paint/frame_bvp.json (tools/bvp_frame.py). Sim frame: +x east, +y SOUTH, metres, origin = player start.

THE DRAW MODEL (kc2_play: World/Ground under World/Actors, Actors y_sort_enabled):
  * the GROUND layer = the tiles: the whole painting, tall pieces included. Wherever a tall piece can
    hide an actor, its CUTOUT is drawn over him by y-sort, so the ground's copy of it never shows on
    top of him; where he stands in front, he covers both copies.
  * a CUTOUT is a tall piece cut from the painting at its own geometry (the ID render), SLICED into
    vertical strips STRIP_M wide. Each strip's sort point is the FRONT (largest-y, camera-side) edge
    of the piece's footprint inside that strip, on the z = 0 plane: an actor whose ground y is smaller
    (north of the front edge, i.e. behind) draws under the strip; larger (in front) draws over it.
    Slicing makes a long diagonal piece (a palisade run, the hall's long wall) sort correctly along
    its whole length; actors never stand inside a footprint (every tall piece is outside the floor).
"""
import hashlib, json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
A9 = os.path.join(os.path.dirname(BV2), "artifacts")
PAINT = os.path.join(BV2, "paint")
TAKE = os.environ.get("BVP_TAKE", os.path.join(BV2, "take"))     # override for dry runs only
FR = json.load(open(os.path.join(PAINT, "frame_bvp.json")))
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
P = FR["px_per_m"]; X0, Y0 = FR["origin_px"]; W, H = FR["size_px"]
A = math.radians(FR["pitch_deg"]); S, C = math.sin(A), math.cos(A)
STRIP_M = 2.0
TALL_M = 0.8              # a piece at least this tall that stands outside the floor is a cutout
FEATHER_PX = 3            # the cut's outward grace (the painter's line wanders off the greybox edge)
PAINTED = os.environ.get("BVP_PAINTED", os.path.join(PAINT, "barrow_v2_painted.png"))
Image.MAX_IMAGE_PIXELS = None


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def px(x, y, z=0.0):
    return X0 + P * x, Y0 + P * S * y - P * C * z


def sim_of_px(X, Y):                     # on the z = 0 plane
    return (X - X0) / P, (Y - Y0) / (P * S)


# --------------------------------------------------------------------------------------- stitch
def stitch():
    cfg = json.load(open(os.path.join(PAINT, "cfg_barrow_v2.json")))
    Pf, COLS, ROWS, SKIP = cfg["prefix"], cfg["cols"], cfg["rows"], set(cfg.get("skip", []))
    CW, CH, SX, SY = 1536, 1024, 1280, 768; OV = CW - SX

    def src(k):
        for d in (f"{Pf}-{k}-r3", f"{Pf}-{k}-r2", f"{Pf}-{k}-r1", f"{Pf}-{k}"):
            p = os.path.join(A9, d, f"{Pf}-{k}.png")
            if os.path.exists(p):
                return p
    acc = np.zeros((H, W, 3), np.float32); wsum = np.zeros((H, W), np.float32)
    up = (np.arange(OV) + 0.5) / OV
    used = {}
    for r in range(ROWS):
        for c in range(COLS):
            k = f"{c}_{r}"
            if k in SKIP:
                continue
            p = src(k)
            if p is None:
                sys.exit(f"chunk {k} is not painted")
            used[k] = {"file": os.path.relpath(p, BV2), "sha256": sha(p)}
            im = np.asarray(Image.open(p).convert("RGB"), np.float32)
            assert im.shape == (CH, CW, 3), (k, im.shape)
            has = lambda cc, rr: 0 <= cc < COLS and 0 <= rr < ROWS and f"{cc}_{rr}" not in SKIP
            wx, wy = np.ones(CW, np.float32), np.ones(CH, np.float32)
            if has(c - 1, r): wx[:OV] *= up
            if has(c + 1, r): wx[CW - OV:] *= up[::-1]
            if has(c, r - 1): wy[:OV] *= up
            if has(c, r + 1): wy[CH - OV:] *= up[::-1]
            w = np.outer(wy, wx)
            acc[r * SY:r * SY + CH, c * SX:c * SX + CW] += im * w[..., None]
            wsum[r * SY:r * SY + CH, c * SX:c * SX + CW] += w
    cov = wsum > 1e-6
    rgb = np.where(cov[..., None], acc / np.maximum(wsum, 1e-6)[..., None], 0).clip(0, 255).round().astype(np.uint8)
    out = np.dstack([rgb, (cov * 255).astype(np.uint8)])
    Image.fromarray(out, "RGBA").save(PAINTED, optimize=False)
    pv = Image.fromarray(rgb); pv.thumbnail((2400, 2400)); pv.save(os.path.join(PAINT, "barrow_v2_painted_preview.jpg"), quality=86)
    json.dump({"painted": os.path.relpath(PAINTED, BV2), "sha256": sha(PAINTED), "size_px": [W, H], "chunks": used,
               "weights": "linear ramps across the 256 px overlaps, only toward PAINTED neighbours; normalised per pixel",
               "coverage_frac": float(cov.mean())}, open(os.path.join(PAINT, "stitch_report.json"), "w"), indent=1)
    print(PAINTED, "sha256", sha(PAINTED), "coverage", round(float(cov.mean()), 4))


# --------------------------------------------------------------------------------------- groups
GROUND_KINDS = {"drift_berm", "trodden_snow", "pressure_ridge", "scree", "heather", "ash_heap", "shingle_tongue",
                "pebble", "rock_slab", "floe", "fallen_stone", "grave_marker", "beam", "driftwood", "stream_bank"}


def groups():
    out, i = [], 1
    by = {}
    for f in L["features"]:
        if f["kind"] in GROUND_KINDS or not str(f.get("placement", "")).startswith("OUTSIDE"):
            continue
        h = float(f["z_top_m"]) - float(f["z_bottom_m"])
        if f["kind"] in ("cliff", "cave"):
            continue      # below the lip on screen; no actor ever stands south of it -> ground layer
        if h < TALL_M and f["kind"] not in ("door", "porch"):
            continue
        g = {"mound": "barrow", "door": None, "hall": "hall", "porch": "hall", "wreck": "wreck", "mast": "wreck"}.get(f["kind"], f["id"])
        if f["kind"] == "door":
            g = "barrow" if f["id"] == "barrow_door" else "hall"
        by.setdefault(g, []).append(f["id"])
    for g, ids in by.items():
        out.append({"idx": i, "group": g, "match": ids}); i += 1
    assert i < 256
    os.makedirs(os.path.join(TAKE, "ids"), exist_ok=True)
    p = os.path.join(TAKE, "ids", "ids_groups.json")
    json.dump(out, open(p, "w"), indent=1)
    print(p, len(out), "groups")


# --------------------------------------------------------------------------------------- ids
def ids(capdir):
    info = json.load(open(os.path.join(capdir, "ids_tiles.json")))
    T = info["tile"]
    plate = Image.new("RGB", (W, H))
    for t in info["tiles"]:
        plate.paste(Image.open(os.path.join(capdir, t["file"])).convert("RGB"), tuple(t["px"]))
    plate.save(os.path.join(TAKE, "ids", "ids.png"))
    a = np.asarray(plate).astype(np.int32)
    gi = ((a[..., 0] - 8 + 8) // 16) + 16 * ((a[..., 1] - 8 + 8) // 16)
    gi[(a[..., 2] < 150)] = 0
    Image.fromarray(gi.astype(np.uint8)).save(os.path.join(TAKE, "ids", "gid.png"))
    G = json.load(open(os.path.join(TAKE, "ids", "ids_groups.json")))
    cnt = {g["group"]: int((gi == g["idx"]).sum()) for g in G}
    json.dump({"tiles_from": capdir, "groups_hit_by_mesh": info.get("groups_hit"), "px_by_group": cnt},
              open(os.path.join(TAKE, "ids", "ids_report.json"), "w"), indent=1)
    print("ids:", {k: v for k, v in cnt.items() if v}, "missing:", [k for k, v in cnt.items() if not v])


# --------------------------------------------------------------------------------------- tiles
def tiles():
    im = Image.open(PAINTED)
    d = os.path.join(TAKE, "ground", "tiles"); os.makedirs(d, exist_ok=True)
    rows = []
    for t in FR["tiles"]:
        x0, y0, x1, y1 = t["px"]
        p = os.path.join(d, f"ground_{t['id']}.png")
        im.crop((x0, y0, x1, y1)).save(p)
        ox, oy = sim_of_px(x0, y0)
        rows.append({"id": t["id"], "file": f"tiles/{os.path.basename(p)}", "sha256": sha(p), "plate_px": [x0, y0, x1, y1],
                     "size_px": [x1 - x0, y1 - y0], "origin_sim_m": [round(ox, 5), round(oy, 5)]})
    man = {
        "_what": "barrow_v2 painted GROUND tiles for kc2_play's World/Ground layer (under the y-sorted Actors). Lane BVP, drax.",
        "frame": "sim: +x east, +y SOUTH, metres, origin = player start; tiles lie on the z = 0 plane",
        "projection": "kc2play_projection.gd: screen_x = ppm*x, screen_y = ppm*sin(a)*y - ppm*cos(a)*z; pitch %.10f, zero yaw" % FR["pitch_deg"],
        "px_per_m_x": P, "px_per_ground_m_y": P * S, "authored_ppm": P,
        "place_rule": "a tile's TOP-LEFT pixel corner sits at m_to_px(origin_sim_m.x, origin_sim_m.y) (z = 0); draw it at scale ppm_runtime / authored_ppm (ZOOM-GD 75.668 -> 0.75203; plate/HOUSE-authored 100.6176 -> 1.0)",
        "plate_origin_px": FR["origin_px"], "plate_size_px": FR["size_px"], "tile_px": FR["tile"],
        "alpha": "255 where painted; 0 only outside the painted envelope (never on screen: the envelope is the floor + the ZOOM-GD half window + 1.5 m)",
        "painting_sha256": sha(PAINTED), "tiles": rows,
    }
    json.dump(man, open(os.path.join(TAKE, "ground", "tiles.json"), "w"), indent=1)
    print(len(rows), "tiles")


# --------------------------------------------------------------------------------------- cut
def dense(poly, step=0.1, closed=True):
    pts = []
    n = len(poly)
    for i in range(n if closed else n - 1):
        a, b = poly[i], poly[(i + 1) % n]
        m = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for k in range(m):
            pts.append((a[0] + (b[0] - a[0]) * k / m, a[1] + (b[1] - a[1]) * k / m))
    if not closed:
        pts.append(tuple(poly[-1]))
    return np.array(pts)


def floor_mask():
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([px(p[0], p[1]) for p in L["floor"]["polygon"]], fill=255)
    return np.asarray(m) > 0


def cut():
    G = json.load(open(os.path.join(TAKE, "ids", "ids_groups.json")))
    gid = np.asarray(Image.open(os.path.join(TAKE, "ids", "gid.png")))
    paint = np.asarray(Image.open(PAINTED).convert("RGBA"))
    fl = floor_mask()
    feats = {f["id"]: f for f in L["features"]}
    d = os.path.join(TAKE, "cutouts"); os.makedirs(d, exist_ok=True)
    rows, groups_out = [], []
    SW = STRIP_M * P
    objs = ndimage.find_objects(gid)
    for g in G:
        sl = objs[g["idx"] - 1] if g["idx"] - 1 < len(objs) else None
        if sl is None:
            groups_out.append({"group": g["group"], "px": 0, "note": "not in the ID render"}); continue
        pad = FEATHER_PX + 2
        ry0, ry1 = max(0, sl[0].start - pad), min(H, sl[0].stop + pad)
        rx0, rx1 = max(0, sl[1].start - pad), min(W, sl[1].stop + pad)
        m = ndimage.binary_dilation(gid[ry0:ry1, rx0:rx1] == g["idx"], iterations=FEATHER_PX)
        alpha = np.where(m, paint[ry0:ry1, rx0:rx1, 3], 0).astype(np.uint8)
        pnt = paint[ry0:ry1, rx0:rx1, :3]; flr = fl[ry0:ry1, rx0:rx1]
        # the sort polygon(s): footprints of the group's features; the cliff also takes the lip
        pts = [dense(feats[i]["footprint"]) for i in g["match"] if i in feats]
        if g["group"] == "sea_cliff":
            pts.append(dense(L["land"]["cliff_lip"], closed=False))
            pts.append(dense(L["stair"]["flight"]["polygon"]))
        pts = np.concatenate(pts) if pts else None
        ys, xs = np.nonzero(alpha)
        gx0, gx1 = int(xs.min()) + rx0, int(xs.max()) + 1 + rx0
        k0 = int(math.floor((gx0 - X0) / SW)); k1 = int(math.floor((gx1 - 1 - X0) / SW))
        for k in range(k0, k1 + 1):
            sx0 = max(gx0, int(round(X0 + k * SW))); sx1 = min(gx1, int(round(X0 + (k + 1) * SW)))
            if sx1 <= sx0:
                continue
            sub = alpha[:, sx0 - rx0:sx1 - rx0]
            yy = np.nonzero(sub.any(1))[0]
            if yy.size == 0:
                continue
            y0c, y1c = int(yy.min()), int(yy.max()) + 1
            xa, xb = sim_of_px(sx0, 0)[0], sim_of_px(sx1, 0)[0]
            sel = pts[(pts[:, 0] >= xa) & (pts[:, 0] <= xb)] if pts is not None else np.zeros((0, 2))
            if sel.size == 0 and pts is not None:
                mid = (xa + xb) / 2
                sel = pts[np.argsort(np.abs(pts[:, 0] - mid))[:3]]
            ay = float(sel[:, 1].max())
            ax = (xa + xb) / 2
            AX, AY = px(ax, ay)
            crop = np.dstack([pnt[y0c:y1c, sx0 - rx0:sx1 - rx0], sub[y0c:y1c]])
            name = f"{g['group']}__s{k:+03d}".replace("+", "p").replace("-", "m")
            p = os.path.join(d, name + ".png")
            Image.fromarray(crop, "RGBA").save(p)
            ov = int(((sub[y0c:y1c] > 0) & flr[y0c:y1c, sx0 - rx0:sx1 - rx0]).sum())
            Y0c = y0c + ry0
            rows.append({"id": name, "group": g["group"], "file": f"cutouts/{name}.png", "sha256": sha(p),
                         "plate_px_topleft": [sx0, Y0c], "size_px": [sx1 - sx0, y1c - y0c],
                         "sort_point_sim_m": [round(ax, 4), round(ay, 4)],
                         "sort_point_plate_px": [round(AX, 2), round(AY, 2)],
                         "texture_offset_px": [round(sx0 - AX, 2), round(Y0c - AY, 2)],
                         "strip_x_m": [round(xa, 4), round(xb, 4)],
                         "over_floor_px": ov, "over_floor_ground_m2": round(ov / (P * P * S), 3)})
        tot_ov = sum(r["over_floor_px"] for r in rows if r["group"] == g["group"])
        groups_out.append({"group": g["group"], "features": g["match"], "px": int((alpha > 0).sum()),
                           "strips": sum(1 for r in rows if r["group"] == g["group"]),
                           "over_floor_ground_m2": round(tot_ov / (P * P * S), 3)})
    man = {
        "_what": "barrow_v2 CUTOUT plates: tall pieces cut from the painting at their own geometry, sliced into %.1f m vertical strips, each with its own sort point (lane BVP, drax)" % STRIP_M,
        "draw_rule": ("Sprite2D (centered = false) as a child of the y-sorted Actors node; node.position = m_to_px(sort_point_sim_m) (z = 0, the same law as an actor's ground point); "
                      "texture offset = texture_offset_px * (ppm_runtime / authored_ppm); scale = ppm_runtime / authored_ppm. Y-sort then compares ground y with the actors' ground y."),
        "authored_ppm": P, "px_per_ground_m_y": P * S, "strip_m": STRIP_M, "feather_px": FEATHER_PX,
        "over_floor": "pixels of a cutout drawn over the walkable floor's z = 0 footprint (pieces SOUTH of the floor rise over it on screen; that is why they sort)",
        "painting_sha256": sha(PAINTED), "groups": groups_out, "cutouts": rows,
    }
    json.dump(man, open(os.path.join(TAKE, "cutouts", "cutouts.json"), "w"), indent=1)
    print(len(rows), "cutout strips in", len([g for g in groups_out if g.get("strips")]), "groups")


# --------------------------------------------------------------------------------------- classmap
def classmap():
    gj = json.load(open(os.path.join(BV2, "greybox", "ground_class_map.json")))
    src = os.path.join(BV2, gj["png"])
    d = os.path.join(TAKE, "ground_class"); os.makedirs(d, exist_ok=True)
    cm = Image.open(src)
    cm.save(os.path.join(d, "ground_class_sim.png"))
    # the same classes on the plate grid (z = 0), 1/4 plate resolution, nearest
    k = 4
    Wq, Hq = W // k, H // k
    Xs = (np.arange(Wq) * k + k / 2 - X0) / P
    Ys = (np.arange(Hq) * k + k / 2 - Y0) / (P * S)
    e = gj["extent_sim_m"]; ppm = gj["px_per_m"]
    a = np.asarray(cm)
    ci = np.clip(((Xs - e["x0"]) * ppm).astype(int), 0, a.shape[1] - 1)
    ri = np.clip(((Ys - e["y0"]) * ppm).astype(int), 0, a.shape[0] - 1)
    pl = a[ri[:, None], ci[None, :]]
    Image.fromarray(pl.astype(np.uint8)).save(os.path.join(d, "ground_class_plate_q4.png"))
    out = dict(gj)
    out.update({"_what": "barrow_v2 ground class map for surface-aware VFX (carried over from lane BX, unchanged values)",
                "sim_png": "ground_class_sim.png", "sim_png_sha256": sha(os.path.join(d, "ground_class_sim.png")),
                "plate_png": "ground_class_plate_q4.png", "plate_png_px_per_m_x": P / k, "plate_png_px_per_ground_m_y": P * S / k,
                "plate_png_origin_px": [X0 / k, Y0 / k], "source": os.path.relpath(src, BV2)})
    out.pop("png", None); out.pop("png_sha256", None)
    json.dump(out, open(os.path.join(d, "ground_class.json"), "w"), indent=1)
    print("classmap ok", (Wq, Hq))


# --------------------------------------------------------------------------------------- doors
def anchors():
    feats = {f["id"]: f for f in L["features"]}
    cen = lambda fid: np.mean(np.array(feats[fid]["footprint"], float), 0).tolist() if fid in feats else None
    st = L["stair"]
    deliver = {
        "p01": ("wreck_hull", "the wreck: up through the shore ice / over the low rail", cen("wreck_hull")),
        "p02": ("barrow_door", "the barrow door: mist, then rising from the grave-ground", cen("barrow_door")),
        "p03": ("sea_cave_stair", "the sea cave: up the stair to the top landing", np.mean(np.array(st["top_landing"]["polygon"], float), 0).tolist()),
        "p04": ("hall_porch", "the hall's great door (porch): out of the smoke", feats.get("hall_porch", {}).get("mouth_centre") or cen("hall_great_door")),
        "p05": ("mere", "the frozen mere: 4 s of cracks, then bursting through the ice (ground art)", None),
        "p06": ("fallen_gable", "the fallen gable: up out of the ash", cen("fallen_gable")),
    }
    rows = []
    for a in L["anchors"]["points"]:
        fid, what, emit = deliver[a["id"]]
        r = {"id": a["id"], "anchor_sim_m": [a["x"], a["y"]], "anchor_plate_px": [round(v, 2) for v in px(a["x"], a["y"])],
             "scatter_disc_m": 8.0, "deliverer": fid, "how": what}
        if emit:
            r["deliverer_point_sim_m"] = [round(emit[0], 4), round(emit[1], 4)]
            r["deliverer_point_plate_px"] = [round(v, 2) for v in px(*emit)]
        rows.append(r)
    json.dump({"_what": "barrow_v2 door anchors: the six spawn anchors of record (layout_v2.json anchors.points, the pack's sg1 rows) and the painted deliverer for each",
               "doors": rows}, open(os.path.join(TAKE, "doors.json"), "w"), indent=1)
    print("doors ok")


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"stitch": stitch, "groups": groups, "tiles": tiles, "cut": cut, "classmap": classmap, "anchors": anchors,
     "ids": lambda: ids(sys.argv[2])}[cmd]()
