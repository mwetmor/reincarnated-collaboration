#!/usr/bin/env python3
"""C-9 (d) -- LANE A'S METEOR FLIPBOOK (a copy of fire_bake_pack.py; what differs is marked METEOR): the kit's own
frames (godot/tools/bake_meteor.gd) into ONE atlas. METEOR: the ring and the burn are phases too (anchored at their
own centre); a frame whose pixels equal an earlier frame's (the ring's hold, the burn's 6 Hz boil) SHARES its
atlas rect -- the table still gives each tick its own entry and offset.

Fire Ball notes follow.

For every phase and tick the rig wrote S (the phase over transparent black), and for phases with MIX
layers M0 / M1 (the MIX layers alone over opaque black / white). Here:

    colour  C = S.rgb                        premultiplied: what the phase adds over black
    cover   A = 1 - (M1 - M0), mean of rgb   how much of what is under it the MIX layers hide
    a frame over any ground g:  out = C + g * (1 - A)     (the kit's own blend, 8-bit)

Each frame is trimmed to its non-zero texels, given a one-texel transparent border (a bilinear tap at
a quad's edge fades to nothing rather than into a neighbour), and packed (shelves, tallest first) into
one RGBA atlas: rgb = C, a = A. The frame table records, per frame, its atlas rect and the offset of
that rect's top-left from the phase's ANCHOR, in the kit's px (1 px = 1 px of the painted Barrow's
1920 x 1080 frame -- both are 100.62 px/m):

    travel        the projectile node (the capsule's leading tip), direction EAST (the port rotates it)
    puff          the release socket, aim EAST
    cast_floor    the caster's feet
    impact        the burst's point (where the node stopped)
    impact_floor  the burst's point
    halo          keeper.gd's halo centre (32 steps of its windup t)

and the per-tick record the port re-plays: the node's travel from the socket, the tick the burst
spawns, the trail motes' births (id, tick, origin from the node, size, band colour, phase, life).

    python3 tools/fire_bake_pack.py --bake work/fire_bake/s1b --seeds work/fire_bake/s2 [...] --out godot/data/vfx/fire_ball
"""
import argparse, hashlib, io, json, os, sys
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--bake", required=True, help="the full bake (travel, cast, halo, impact seed 1)")
ap.add_argument("--seeds", nargs="*", default=[], help="impact-only bakes, one per extra seed")
ap.add_argument("--out", required=True)
ap.add_argument("--atlas-w", type=int, default=4096)
ap.add_argument("--page-h", type=int, default=4096, help="pages (Texture2DArray layers) are at most this tall")
ap.add_argument("--report", default="")
ap.add_argument("--only", nargs="*", default=[], help="MIX: ship only these phases (e.g. travel): the rest are measured but not packed")
ap.add_argument("--name", default="meteor_a.json")
args = ap.parse_args()


def load_rgba(path):
    return np.asarray(Image.open(path).convert("RGBA"))


def frame(dir_, ph, tick, rect):
    s = load_rgba(os.path.join(dir_, "%s_%03d_S.png" % (ph, tick)))
    c = s[:, :, :3].astype(np.int32)
    m0p = os.path.join(dir_, "%s_%03d_M0.png" % (ph, tick))
    if os.path.exists(m0p):
        m0 = load_rgba(m0p)[:, :, :3].astype(np.int32)
        m1 = load_rgba(os.path.join(dir_, "%s_%03d_M1.png" % (ph, tick)))[:, :, :3].astype(np.int32)
        a = np.clip(255 - (m1 - m0), 0, 255).mean(axis=2)
        a = np.rint(a).astype(np.int32)
    else:
        a = np.zeros(c.shape[:2], np.int32)
    img = np.dstack([c, a]).astype(np.uint8)
    nz = (img.max(axis=2) > 0)
    if not nz.any():
        return None
    ys, xs = np.nonzero(nz)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    core = img[y0:y1, x0:x1]
    padded = np.zeros((core.shape[0] + 2, core.shape[1] + 2, 4), np.uint8)
    padded[1:-1, 1:-1] = core
    # the padded rect's top-left, in the rig's viewport px
    return padded, (rect[0] + x0 - 1, rect[1] + y0 - 1)


def collect(dir_, phases, anchor_of):
    log = json.load(open(os.path.join(dir_, "bake_log.json")))
    out = {}
    for row in log["ticks"]:
        for ph, rec in row.get("phases", {}).items():
            if ph not in phases or rec.get("rect") is None:
                continue
            f = frame(dir_, ph, row["tick"], rec["rect"])
            if f is None:
                continue
            img, tl = f
            ax, ay = anchor_of(ph, row)
            out.setdefault(ph, []).append({"tick": row["tick"], "img": img, "ox": tl[0] - ax, "oy": tl[1] - ay})
    return log, out


def anchor(ph, row):
    if ph == "travel":
        return row["bolt_pos"]
    if ph in ("impact", "impact_floor"):
        return row["impact"]["pos"]
    if ph == "puff":
        return row["puff"]["pos"]
    if ph == "cast_floor":
        return row["cast_floor"]["pos"]
    if ph in ("ring", "burn"):
        return row[ph]["pos"]
    raise KeyError(ph)


log1, main = collect(args.bake, ["travel", "puff", "cast_floor", "impact", "impact_floor", "ring", "burn"], anchor)
# the halo: its own log
hlog = json.load(open(os.path.join(args.bake, "halo_log.json")))
hax, hay = hlog["anchor"]
main["halo"] = []
for fr in hlog["frames"]:
    s = load_rgba(os.path.join(args.bake, "halo_%02d_S.png" % fr["i"]))
    c = s[:, :, :3]
    nz = c.max(axis=2) > 0
    ys, xs = np.nonzero(nz)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    padded = np.zeros((y1 - y0 + 2, x1 - x0 + 2, 4), np.uint8)
    padded[1:-1, 1:-1, :3] = c[y0:y1, x0:x1]
    r = fr["rect"]
    main["halo"].append({"tick": fr["i"], "t": fr["t"], "img": padded, "ox": r[0] + x0 - 1 - hax, "oy": r[1] + y0 - 1 - hay})
impacts = [main.pop("impact")]
seed_ids = [int(next(r["impact"]["seed"] for r in log1["ticks"] if "impact" in r))]
for d in args.seeds:
    lg, o = collect(d, ["impact"], anchor)
    impacts.append(o["impact"])
    seed_ids.append(int(next(r["impact"]["seed"] for r in lg["ticks"] if "impact" in r)))

# ---- the floors: ONE frame and an alpha, if the kit's frames are that frame scaled by its alpha ----
def one_frame_check(frames, alphas):
    base = frames[0]["img"].astype(np.float64)
    worst = 0.0
    for f, al in zip(frames, alphas):
        if f["ox"] != frames[0]["ox"] or f["oy"] != frames[0]["oy"] or f["img"].shape != frames[0]["img"].shape:
            # a faded frame trims tighter: compare on the base's canvas
            h, w = f["img"].shape[:2]
            dx, dy = int(round(f["ox"] - frames[0]["ox"])), int(round(f["oy"] - frames[0]["oy"]))
            canvas = np.zeros_like(base)
            canvas[dy:dy + h, dx:dx + w] = f["img"]
        else:
            canvas = f["img"].astype(np.float64)
        pred = base * (al / alphas[0])
        worst = max(worst, float(np.abs(canvas - pred).max()))
    return worst

phase_meta = {}
floor_alpha = {}
for ph, key in (("cast_floor", "cast_floor"), ("impact_floor", "impact")):
    ticks = {r["tick"]: r for r in log1["ticks"]}
    fr = main[ph]
    als = [ticks[f["tick"]][key]["alpha"] if ph == "cast_floor" else ticks[f["tick"]]["impact"]["floor_alpha"] for f in fr]
    worst = one_frame_check(fr, als)
    phase_meta[ph] = {"one_frame_check_max_abs_8bit": worst, "alphas": als}
    if worst <= 1.5:
        floor_alpha[ph] = als
        main[ph] = fr[:1]

# MIX: only the named phases ship (the timing and the motes' births stay in the record)
if args.only:
    main = {k: v for k, v in main.items() if k in args.only}
    if "impact" not in args.only:
        impacts = []
        seed_ids = []

# ---- pack: shelves, tallest first, into PAGES of at most atlas_w x page_h (one Texture2DArray) ------
entries = []
for ph, frs in main.items():
    for i, f in enumerate(frs):
        entries.append((ph, 0, i, f))
for si, frs in enumerate(impacts):
    for i, f in enumerate(frs):
        entries.append(("impact", si, i, f))
W = args.atlas_w
PH = args.page_h
# METEOR: identical frames share one rect
import hashlib as _h
digest = {}
first_of = {}
for k, e in enumerate(entries):
    key = _h.sha1(e[3]["img"].tobytes() + str(e[3]["img"].shape).encode()).hexdigest()
    if key in digest:
        first_of[k] = digest[key]
    else:
        digest[key] = k
unique = [k for k in range(len(entries)) if k not in first_of]
order = sorted(unique, key=lambda k: (-entries[k][3]["img"].shape[0], -entries[k][3]["img"].shape[1]))
# shelves over one tall strip, then whole shelves dealt to pages: the fewest pages that fit PH, and the
# lowest common page height that still fits them (the layers of a Texture2DArray are one size)
shelves = []
x = 0
for k in order:
    h, w = entries[k][3]["img"].shape[:2]
    if not shelves or x + w > W:
        shelves.append({"h": h, "items": []})
        x = 0
    shelves[-1]["items"].append((k, x))
    x += w
def deal(limit):
    out = [[]]
    hh = 0
    for sh in shelves:
        if hh + sh["h"] > limit:
            out.append([])
            hh = 0
        out[-1].append(sh)
        hh += sh["h"]
    return out
n_pages = len(deal(PH))
lo, hi = max(sh["h"] for sh in shelves), PH
while lo < hi:
    mid = (lo + hi) // 2
    if len(deal(mid)) <= n_pages:
        hi = mid
    else:
        lo = mid + 1
dealt = deal(lo)
pos = {}
used_h = []
for pg, shs in enumerate(dealt):
    y = 0
    for sh in shs:
        for (k, xx) in sh["items"]:
            pos[k] = (pg, xx, y)
        y += sh["h"]
    used_h.append(y)
H = max(used_h)
H = (H + 7) // 8 * 8
pages = [np.zeros((H, W, 4), np.uint8) for _ in used_h]
table = {}
for k in first_of:
    pos[k] = pos[first_of[k]]
for k, (ph, si, i, f) in enumerate(entries):
    pg, px, py = pos[k]
    h, w = f["img"].shape[:2]
    pages[pg][py:py + h, px:px + w] = f["img"]
    key = ph if ph != "impact" else "impact_%d" % si
    table.setdefault(key, []).append({"tick": f["tick"], "page": pg, "x": px, "y": py, "w": w, "h": h,
                                      "ox": round(float(f["ox"]), 4), "oy": round(float(f["oy"]), 4)})
for key in table:
    table[key].sort(key=lambda e: e["tick"])
used = sum(entries[k][3]["img"].shape[0] * entries[k][3]["img"].shape[1] for k in unique)

# ---- the per-tick record the port re-plays ---------------------------------------------------------
sock = log1["socket"]
travel = []
for r in log1["ticks"]:
    if r["travel_visible"]:
        travel.append({"tick": r["tick"], "dx": round(r["bolt_pos"][0] - sock[0], 4), "dy": round(r["bolt_pos"][1] - sock[1], 4),
                       "active": r["bolt_active"], "draining": r["bolt_draining"]})
first_impact = next(r for r in log1["ticks"] if "impact" in r)
births = {}
for r in log1["ticks"]:
    for m in r.get("motes", []):
        if m["id"] not in births:
            births[m["id"]] = {"id": m["id"], "birth_tick": m["birth_tick"], "origin_dx": round(m["origin"][0] - sock[0], 4),
                               "origin_dy": round(m["origin"][1] - sock[1], 4), "half_px": m["half"], "color": m["color"],
                               "phase": m["phase"], "life_s": m["life"]}
motes_path = {}
for r in log1["ticks"]:
    for m in r.get("motes", []):
        motes_path.setdefault(str(m["id"]), []).append([r["tick"], round(m["pos"][0] - sock[0], 3), round(m["pos"][1] - sock[1], 3), round(m["alpha"], 5)])
kitc = log1["kit_config"]
meta = {
    "_what": "C-9 (c): cliffside's fire_bolt_e1_B baked from its own runtime (godot/tools/bake_fire_bolt.gd in a scratch copy of C-7's "
             "cliffside_v45; the live /playtest/cliffside/ source is identical for the kit and its scripts) -- tools/fire_bake_pack.py",
    "atlas": {"w": W, "h": H, "pages": len(pages), "used_h": used_h, "texels_used": used, "fill": round(used / float(W * H * len(pages)), 4),
              "channels": "rgb = premultiplied colour over black (the kit's 8-bit sRGB values); a = MIX cover. out = rgb + ground * (1 - a)"},
    "px_per_m": 100.617553710938,
    "anchors": {"travel": "the projectile node (capsule tip), aim east", "puff": "the fall's start, aim east", "cast_floor": "the caster's feet",
                "ring": "the ring's centre (ground_dy below the burst point)", "burn": "the burn's centre (as the ring)",
                "impact": "the burst point", "impact_floor": "the burst point", "halo": "the halo centre"},
    "frames": table,
    "floor_alpha": floor_alpha,
    "phase_checks": phase_meta,
    "impact_seeds": seed_ids,
    "timing": {"ticks_per_s": 60, "impact_spawn_tick": first_impact["tick"],
               "impact_dx": round(first_impact["impact"]["pos"][0] - sock[0], 4), "impact_dy": round(first_impact["impact"]["pos"][1] - sock[1], 4),
               "travel": travel},
    "motes": {"births": sorted(births.values(), key=lambda b: b["id"]), "paths": motes_path,
              "rule": "vfx_fire_motes_fl4.gd trail mode: pos = origin + (lateral_px * (sin(phase + age*8) - sin(phase)) * 0.5, -rise_px_s * age); "
                      "alpha = 1 - age/life; a diamond of half-size half_px, additive, colour = palette band",
              "lateral_px": kitc["fire_layers"]["travel"]["trail"]["lateral_px"], "rise_px_s": kitc["fire_layers"]["travel"]["trail"]["rise_px_s"]},
    "halo": {"frames": len(main.get("halo", [])), "t_of_frame": [round(f["t"], 5) for f in main.get("halo", [])],
             "rule": "keeper.gd _update_cast_halo: live from the cast start to the release; t = ticks since start / (release ticks - 1)"},
    "kit": {"name": log1["kit"], "speed_px_s": kitc["speed_px_s"], "range_px": kitc["range_px"], "palette": kitc["palette"],
            "palette_2": kitc["palette_2"], "head_length_px": kitc["head_length_px"]},
    "bake": {"renderer": log1["renderer"], "adapter": log1["adapter"], "seed_dirs": [args.bake] + args.seeds, "dance_seed": log1["dance_seed"]},
}
os.makedirs(args.out, exist_ok=True)
files = []
exact = True
for pg, img in enumerate(pages):
    buf = io.BytesIO()
    Image.fromarray(img, "RGBA").save(buf, "WEBP", lossless=True, quality=100, method=6, exact=True)
    wb = buf.getvalue()
    name = "atlas_%d.bin" % pg
    open(os.path.join(args.out, name), "wb").write(wb)
    back = np.asarray(Image.open(io.BytesIO(wb)).convert("RGBA"))
    exact = exact and bool((back == img).all())
    files.append({"file": name, "bytes": len(wb), "sha256": hashlib.sha256(wb).hexdigest()})
meta["atlas"]["files"] = files
meta["atlas"]["format"] = "WebP lossless (exact), one per page, read by signature"
meta["atlas"]["roundtrip_exact"] = exact
meta["_what"] = ("C-9 (d): LANE A'S METEOR -- the meteor_e1 kit (VF-met head and trail on the fl6 travel layers; its impact the "
    "burst template cut from VF-met-impact-01) and its ring and burn in the kit's material, baked from the kit's own runtime "
    "(godot/tools/bake_meteor.gd, a cliffside project exported by the frozen exporter with these two kits) -- tools/meteor_bake_pack.py")
meta["timing"]["ring_dx"] = round(log1["ticks"][0]["ring"]["pos"][0] - sock[0], 4)
meta["timing"]["ring_dy"] = round(log1["ticks"][0]["ring"]["pos"][1] - sock[1], 4)
meta["timing"]["ground_dy_below_burst"] = round(log1["ticks"][0]["ring"]["pos"][1] - first_impact["impact"]["pos"][1], 4)
meta["frames_unique"] = len(unique)
meta["frames_total"] = len(entries)
meta["only_phases"] = args.only
json.dump(meta, open(os.path.join(args.out, args.name), "w"), indent=1)
counts = {k: len(v) for k, v in table.items()}
print("atlas %d page(s) of %dx%d (used rows %s), fill %.3f, %d frames %s, webp %.2f MB, roundtrip exact %s, VRAM %.1f MB" % (
    len(pages), W, H, used_h, used / float(W * H * len(pages)), sum(counts.values()), counts, sum(f["bytes"] for f in files) / 1e6, exact,
    W * H * 4 * len(pages) / 1048576.0))
print("floors as one frame:", {k: phase_meta[k]["one_frame_check_max_abs_8bit"] for k in phase_meta})
