#!/usr/bin/env python3
"""
CA-guides-v1 post pass: stitch the Godot tiles, snap the id mask to the legend, derive the
walkable and window-hole masks, decode the depth, MEASURE the crown clearance and the
walkable occlusion, cut the chunk grid, and render the overview + in-game framings.
"""
import json, math, os, hashlib, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

PROJ = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cathedral_greybox"
TILES = "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/ca_tiles"
OUT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/CA-guides-v1"
os.makedirs(OUT, exist_ok=True)

SPEC = json.load(open(PROJ + "/cathedral_spec.json"))
GEOM = json.load(open(PROJ + "/geometry.json"))
CANV = json.load(open(PROJ + "/canvas.json"))
REG = json.load(open(PROJ + "/registration.json"))
LEG = GEOM["legend"]
NAME = {e["index"]: e["name"] for e in LEG}
IDX = {e["name"]: e["index"] for e in LEG}
W, H = CANV["canvas_px"]
OSX, OSY = CANV["origin_screen_px"]
PPM, PXG, PXE = CANV["ppm"], CANV["pxg"], CANV["pxe"]
RV, DV = CANV["r_plan_NE"], CANV["d_plan_NW"]
VIEW_W, VIEW_H = SPEC["runtime_camera"]["view_px"]
ANC_X, ANC_Y = SPEC["runtime_camera"]["anchor_px"]
WALL_RISE = CANV["wall_rise_built_m"]
WALL_RISE_DECLARED = SPEC["elevation"]["wall_rise_m"]

H_MIN, H_MAX = -8.0, 64.0          # must match height.gdshader

def stitch(kind, mode="RGB"):
    im = Image.new(mode, (W, H))
    for t in CANV["tiles"]:
        p = "%s/%s_%s.png" % (TILES, kind, t["name"])
        im.paste(Image.open(p).convert(mode), tuple(t["origin_px"]))
    return im

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def world_to_plate(x, y, z=0.0):
    sx = PPM * (x*RV[0] + y*RV[1]) - OSX
    sy = -(PXG * (x*DV[0] + y*DV[1]) + PXE * z) - OSY
    return sx, sy

# ----------------------------------------------------------------- 1. ID MASK
print("stitching id ...")
idrgb = np.asarray(stitch("id"), dtype=np.uint8)
pal = np.array([e["rgb"] for e in LEG], dtype=np.int32)
packed = (idrgb[..., 0].astype(np.uint32) << 16) | (idrgb[..., 1].astype(np.uint32) << 8) | idrgb[..., 2]
uniq, inv = np.unique(packed, return_inverse=True)
uc = np.stack([(uniq >> 16) & 255, (uniq >> 8) & 255, uniq & 255], -1).astype(np.int32)
du = ((uc[:, None, :] - pal[None, :, :]) ** 2).sum(-1)
lut = du.argmin(1).astype(np.uint8)
maxerr = int(np.sqrt(du.min(1)).max())
cls = lut[inv].reshape(H, W)
print("  distinct rendered colours: %d (legend has %d)" % (len(uniq), len(LEG)))
_present = set(np.unique(cls).tolist())
_missing = [e["name"] for e in LEG if e["index"] not in _present]
print("  legend classes with no visible pixel: %s" % (_missing or "none"))
print("  id snap: max distance from a legend colour = %d (0 = byte-exact)" % maxerr)
Image.fromarray(np.stack([pal[cls][..., i].astype(np.uint8) for i in range(3)], -1)).save(OUT + "/ortho_canvas_v1_id.png")

walk_ids = [e["index"] for e in LEG if e["walkable"]]
walkable = np.isin(cls, walk_ids)
Image.fromarray((walkable * 255).astype(np.uint8)).save(OUT + "/ortho_canvas_v1_walkable.png")
window = (cls == IDX["opening_to_outside"])
Image.fromarray((window * 255).astype(np.uint8)).save(OUT + "/ortho_canvas_v1_window_holes.png")

# ----------------------------------------------------------------- 2. GUIDE
print("stitching guide ...")
guide = stitch("guide")
g = np.asarray(guide).copy()
# every opening to the outside, and everything beyond the architecture, is flat pure #00ff00
g[(cls == IDX["opening_to_outside"]) | (cls == IDX["void_outside_frame"])] = (0, 255, 0)
guide = Image.fromarray(g)
guide.save(OUT + "/ortho_canvas_v1_guide.png")

# ----------------------------------------------------------------- 3. DEPTH
print("stitching height ...")
hr = np.asarray(stitch("height"), dtype=np.uint32)
raw = hr[..., 0] * 256 + hr[..., 1]
fg = (cls != IDX["void_outside_frame"]) & (cls != IDX["opening_to_outside"])
t = raw.astype(np.float64) / 65535.0
elev_m = H_MIN + t * (H_MAX - H_MIN)
depth = np.full((H, W), 65535, dtype=np.uint16)
val = np.clip((elev_m - H_MIN) * 1000.0, 0, 65000)
depth[fg] = val[fg].astype(np.uint16)
Image.fromarray(depth, mode="I;16").save(OUT + "/ortho_canvas_v1_depth_mm.png")

# verify the decode against geometry we KNOW: floor planes must read 8000 mm (elevation 0)
floor_ids = [IDX[n] for n in ("nave_floor", "crossing_floor", "transept_floor", "chancel_floor")]
fl = np.isin(cls, floor_ids)
floor_med = float(np.median(depth[fl])) if fl.any() else float("nan")
wallpx = (cls == IDX["wall_rising"])
wall_max = float(depth[wallpx].max()) if wallpx.any() else float("nan")
print("  depth decode check: floor median %.1f mm (expect 8000)  wall max %.1f mm (expect %.0f)"
      % (floor_med, wall_max, (WALL_RISE - H_MIN) * 1000))

# ----------------------------------------- 4. CROWN CLEARANCE, MEASURED ON PIXELS
# The question is NOT "where is the topmost masonry row on the plate" -- the plate is cropped to
# the rising walls, so that is row 0 by construction and answers nothing. The question is: over
# EVERY camera position the clamp allows, what is the HIGHEST POINT OF THE BUILDING that lands
# inside the 1920x1080 frame? If that maximum is below the crown, no crown is ever visible.
from scipy import ndimage
BLK = 8
def blockmax(a, fill):
    hh, ww = (H // BLK) * BLK, (W // BLK) * BLK
    return a[:hh, :ww].reshape(hh//BLK, BLK, ww//BLK, BLK).max((1, 3))
def blockany(a):
    hh, ww = (H // BLK) * BLK, (W // BLK) * BLK
    return a[:hh, :ww].reshape(hh//BLK, BLK, ww//BLK, BLK).any((1, 3))

elev = np.where(fg, elev_m, -1000.0).astype(np.float32)
E8 = blockmax(elev, -1000.0)
W8 = blockany(walkable)
V8 = blockany(cls == IDX["void_outside_frame"])
FR = (VIEW_H // BLK + 1, VIEW_W // BLK + 1)              # 136 x 241 blocks, rounded UP
maxE = ndimage.maximum_filter(E8, size=FR, mode="constant", cval=-1000.0)
# frame centre for a player at plate (px,py) is (px - (ANC_X - VIEW_W/2), py - (ANC_Y - VIEW_H/2))
shift = (int(round(-(ANC_Y - VIEW_H/2)/BLK)), int(round(-(ANC_X - VIEW_W/2)/BLK)))
centres = np.roll(W8, shift, axis=(0, 1))
vis_max_elev = float(maxE[centres].max())
frames_union = ndimage.maximum_filter(centres.astype(np.uint8), size=FR,
                                      mode="constant", cval=0).astype(bool)
crown_clear_m = WALL_RISE - vis_max_elev
# THE CROWN TEST proper. "Highest point in frame" measures the wall FACE too, which is supposed
# to be in frame. A CROWN pixel is the wall's TOP SURFACE: rendered masonry within 0.5 m of the
# built rise. If no crown block lies inside the union of reachable frames, no camera position in
# the clamp can show a crown.
masonry = (cls == IDX["wall_rising"]) | (cls == IDX["pier"]) | (cls == IDX["clerestory_tracery"])
crown_px = masonry & (elev_m >= WALL_RISE - 0.5) & fg
C8 = blockany(crown_px)
crown_blocks_total = int(C8.sum())
crown_blocks_in_frame = int((C8 & frames_union).sum())
print("  CROWN TEST: crown pixels on the plate %d (blocks %d); blocks inside ANY reachable "
      "frame: %d" % (int(crown_px.sum()), crown_blocks_total, crown_blocks_in_frame))
wy, wx = np.nonzero(walkable)
p_x0, p_x1, p_y0, p_y1 = int(wx.min()), int(wx.max()), int(wy.min()), int(wy.max())
clamp_px = [p_x0 - ANC_X, p_y0 - ANC_Y, p_x1 - ANC_X + VIEW_W, p_y1 - ANC_Y + VIEW_H]
print("  CROWN CLEARANCE (measured over every camera position in the clamp, %d px blocks)" % BLK)
print("    highest point of the building that ever lands in frame: %.3f m" % vis_max_elev)
print("    rising-wall crown: %.3f m  ->  CLEARANCE %.3f m (crown never enters a frame)"
      % (WALL_RISE, crown_clear_m))
print("    analytic bound: anchor %d px / %.4f px per elevation m = %.4f m of wall above the "
      "player's own plan position" % (ANC_Y, PXE, ANC_Y/PXE))

# ----------------------------------------- 5. WALKABLE OCCLUSION, MEASURED
area_plan = REG["walkable_area_raster_m2"]
px2_per_m2 = PPM * PXG
area_screen_m2 = walkable.sum() / px2_per_m2
print("  WALKABLE: plan %.3f m2 -> on screen %.3f m2  (%.3f %% hidden by masonry)"
      % (area_plan, area_screen_m2, 100.0 * (1 - area_screen_m2 / area_plan)))
per_class = {}
for e in LEG:
    if not e["walkable"]: continue
    per_class[e["name"]] = round(float((cls == e["index"]).sum()) / px2_per_m2, 3)

# ----------------------------------------- 6. VOID INSIDE THE ACTUAL FRAME UNION
void_in_reach = float((frames_union & V8).sum()) / float(frames_union.sum())
print("  void (un-architected background) inside the UNION OF REACHABLE FRAMES: %.3f %%"
      % (100*void_in_reach))

# ----------------------------------------------------------------- 7. CHUNKS
CW, CH_ = 1536, 1024
OVL = 256
SW, SH = CW - OVL, CH_ - OVL
ncols = max(1, math.ceil((W - OVL) / SW))
nrows = max(1, math.ceil((H - OVL) / SH))
fgmask = fg
order, dropped = [], []
kept = {}
step = 0
for r in range(nrows):
    for c in range(ncols):
        ox, oy = c*SW, r*SH
        sub = fgmask[oy:oy+CH_, ox:ox+CW]
        frac = float(sub.mean()) if sub.size else 0.0
        nm = "cath_%d_%d" % (r, c)
        if frac < 0.01:
            dropped.append(dict(chunk=nm, index=[r, c], origin_px=[ox, oy], fg_fraction=round(frac, 4)))
            continue
        kept[(r, c)] = nm
for r in range(nrows):
    for c in range(ncols):
        if (r, c) not in kept: continue
        step += 1
        nm = kept[(r, c)]
        ox, oy = c*SW, r*SH
        after = [kept[k] for k in ((r, c-1), (r-1, c)) if k in kept]
        corner = [kept[k] for k in ((r-1, c-1), (r-1, c+1)) if k in kept]
        sub = fgmask[oy:oy+CH_, ox:ox+CW]
        cd = os.path.join(OUT, "chunks")
        os.makedirs(cd, exist_ok=True)
        gcrop = guide.crop((ox, oy, ox+CW, oy+CH_))
        gcrop.save("%s/%s_guide.png" % (cd, nm))
        icrop = Image.fromarray(np.stack([pal[cls[oy:oy+CH_, ox:ox+CW]][..., i].astype(np.uint8)
                                          for i in range(3)], -1))
        icrop.save("%s/%s_id.png" % (cd, nm))
        Image.fromarray((walkable[oy:oy+CH_, ox:ox+CW]*255).astype(np.uint8)).save("%s/%s_mask.png" % (cd, nm))
        Image.fromarray(depth[oy:oy+CH_, ox:ox+CW], mode="I;16").save("%s/%s_depth.png" % (cd, nm))
        Image.fromarray((window[oy:oy+CH_, ox:ox+CW]*255).astype(np.uint8)).save("%s/%s_window.png" % (cd, nm))
        wsub = walkable[oy:oy+CH_, ox:ox+CW]
        cl = CANV["clamp"]["plate_rect_px"]
        in_clamp = not (ox+CW <= cl[0] or ox >= cl[2] or oy+CH_ <= cl[1] or oy >= cl[3])
        order.append(dict(step=step, chunk=nm, index=[r, c], origin_px=[ox, oy],
                          in_camera_clamp=bool(in_clamp),
                          size_px=[CW, CH_], fg_fraction=round(float(sub.mean()), 4),
                          walkable_fraction=round(float(wsub.mean()), 4),
                          window_fraction=round(float(window[oy:oy+CH_, ox:ox+CW].mean()), 4),
                          paint_after=after, corner_overlaps_already_painted=corner,
                          files=dict(guide="chunks/%s_guide.png" % nm, id="chunks/%s_id.png" % nm,
                                     mask="chunks/%s_mask.png" % nm, depth="chunks/%s_depth.png" % nm,
                                     window="chunks/%s_window.png" % nm)))
print("  chunks: grid %dx%d, kept %d, dropped %d, of which %d inside the camera clamp"
      % (nrows, ncols, len(order), len(dropped), sum(1 for o in order if o["in_camera_clamp"])))

chunks = dict(
    ruling="R-C9-43 / R-C9-44 / R-C9-45 -- CA-GREYBOX-V1",
    canvas_px=[W, H], chunk_px=[CW, CH_], step_px=[SW, SH], overlap_px=[OVL, OVL],
    camera_clamp_plate_rect_px=CANV["clamp"]["plate_rect_px"],
    in_camera_clamp_note="chunks with in_camera_clamp=false lie entirely ABOVE the rect the "
                         "runtime camera can ever show at plate scale. They carry the triforium "
                         "and clerestory the rulings author; paint them only if the zoom ruling "
                         "changes (see README).",
    keep_rule="architecture fraction >= 1 % (foreground = not void, not an opening to outside)",
    px_per_m=PPM, projection=SPEC["projection"],
    origin_screen_px=[OSX, OSY],
    depth_format=dict(png="16-bit greyscale (uint16)",
                      unit="millimetres of ELEVATION, datum 8.000 m BELOW the arena floor plane",
                      decode="elevation_m = value/1000 - 8.000",
                      floor_plane=8000, wall_crown=int((WALL_RISE - H_MIN)*1000),
                      not_foreground=65535,
                      why_not_cliffside_convention=(
                          "the cliffside's 'mm below local rim' has no referent indoors, and the "
                          "arena guide lineage already declared 'mm of elevation'. That convention "
                          "cannot encode the crypt, which goes 6 m BELOW the floor plane, so the "
                          "datum is dropped 8 m and the floor plane reads 8000.")),
    guide_rule="shaded ortho tiles; every opening to the OUTSIDE and every un-architected "
               "background pixel is flat pure #00ff00 (becomes alpha; the parallax stack shows through)",
    guide_legend={e["name"]: dict(id_rgb=e["rgb"], guide_grey=e["guide_grey"], walkable=e["walkable"])
                  for e in LEG},
    paint_order_rule="row by row, top to bottom, left to right; a chunk is painted after its left "
                     "and above neighbours (when kept)",
    paint_order=order, dropped=dropped)
json.dump(chunks, open(OUT + "/chunks_v1.json", "w"), indent=1)
json.dump(dict(legend=LEG,
               window_hole_rule="id class 'opening_to_outside' (#00ff00 in the id mask) -- the "
                                "triforium open bays, the whole clerestory, the west-top breach "
                                "and the north chancel breach. 'void_outside_frame' (0,200,0) is "
                                "background, NOT a window.",
               note="id colours are flat index colours, NEAREST only. Snap readback to the nearest "
                    "legend colour; this build measured max distance %d (0 = byte-exact)." % maxerr),
          open(OUT + "/legend_v1.json", "w"), indent=1)

# ----------------------------------------------------------------- 8. OVERVIEW
print("overview ...")
ov = np.asarray(guide).copy()
greenish = (cls == IDX["opening_to_outside"]) | (cls == IDX["void_outside_frame"])
ov[greenish] = (38, 30, 46)
ov[cls == IDX["opening_to_outside"]] = (74, 58, 96)
big = Image.fromarray(ov)
OVW = 2600
scale = OVW / W
ov_img = big.resize((OVW, int(H*scale)), Image.LANCZOS).convert("RGB")
dr = ImageDraw.Draw(ov_img)
try: F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
except Exception: F = ImageFont.load_default()
try: Fs = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
except Exception: Fs = F

def mark(x, y, z, label, dx=12, dy=-10, col=(255, 210, 60)):
    px_, py_ = world_to_plate(x, y, z)
    px_, py_ = px_*scale, py_*scale
    dr.ellipse([px_-5, py_-5, px_+5, py_+5], outline=col, width=3)
    dr.text((px_+dx, py_+dy), label, fill=col, font=Fs,
            stroke_width=3, stroke_fill=(0, 0, 0))

RMx = SPEC["room"]
HWm = RMx["limb_half_m"]; XW, YS, XE, YN = RMx["bbox_m"]
mark(0, 0, 0, "CROSSING / demon-gate crater  r 4.5 m")
mark(*SPEC["spawn"]["player_spawn_m"], 0, "PLAYER SPAWN (south facade)")
for e in SPEC["entrances"]:
    mark(e["centre_m"][0], e["centre_m"][1], 0, e["id"], col=(120, 200, 255))
mark(0, 17.5, 1.2, "DAIS", col=(255, 130, 210))
mark(0, YN, 17.0, "EMPTY CROSS MOUNT", col=(255, 255, 255))
for g_ in REG["spawn_galleries"]:
    mark(g_["centre_m"][0], g_["centre_m"][1], (g_["z"][0]+g_["z"][1])/2,
         "gallery spawn", dx=10, dy=-24, col=(120, 255, 170))
for p in REG["pools"]:
    if p["verdict"] == "KEEP":
        mark(p["arena_m"][0], p["arena_m"][1], 0, "pool %s KEEP" % p["id"], col=(255, 120, 255))

# compass + scale bar
cxp, cyp = OVW - 250, 150
for ang, lab in ((0, "N"), (90, "E"), (180, "S"), (270, "W")):
    a = math.radians(ang)
    ex, ey = math.sin(a), math.cos(a)        # (east, north)
    sxp = PPM*(ex*RV[0] + ey*RV[1])*scale*0.55
    syp = -(PXG*(ex*DV[0] + ey*DV[1]))*scale*0.55
    dr.line([cxp, cyp, cxp+sxp, cyp+syp], fill=(255, 220, 90), width=3)
    dr.text((cxp+sxp*1.3-8, cyp+syp*1.3-12), lab, fill=(255, 220, 90), font=F,
            stroke_width=3, stroke_fill=(0, 0, 0))
bar_m = 10.0
bx0, by0 = 60, int(H*scale) - 70
dr.line([bx0, by0, bx0 + PPM*bar_m*scale, by0], fill=(255, 255, 255), width=5)
dr.text((bx0, by0-34), "10 m along screen-east (ppm %.3f px/m)" % PPM, fill=(255, 255, 255),
        font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
dr.text((60, 40), "CATHEDRAL ARENA GREY BOX  CA-guides-v1", fill=(255, 255, 255), font=F,
        stroke_width=3, stroke_fill=(0, 0, 0))
dr.text((60, 78), "ortho, yaw 45 (camera SE -> NW), pitch 52.9535, ppm 100.6176 | room %.3f x %.3f m, "
                  "walkable %.1f m2 | nave %.2f m wide, walls %.0f m"
        % (RMx["extent_ew_m"], RMx["extent_ns_m"], RMx["walkable_area_target_m2"],
           RMx["limb_width_m"], WALL_RISE),
        fill=(220, 220, 230), font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
ov_img.save(OUT + "/overview_flat_v1.png")

# ----------------------------------------------------------------- 9. FRAMINGS
NAVE_W = SPEC["room"]["limb_width_m"]
ZOOM = dict(
    frame_ground_depth_m=VIEW_H / PXG,
    frame_screen_width_m=VIEW_W / PPM,
    nave_wall_to_wall_along_view_axis_m=NAVE_W * abs(DV[1]),
    ppm_to_fit_both_nave_walls=VIEW_H / (NAVE_W * abs(DV[1]) * math.sin(math.radians(SPEC["projection"]["alpha_deg"]))),
    ppm_to_see=SPEC["camera_clamp"]["ppm_that_would_reveal"],
)
ZOOM["person_px_to_fit_both_nave_walls"] = 130.0 * ZOOM["ppm_to_fit_both_nave_walls"] / PPM
ZOOM["person_px_at"] = {k: 130.0 * v / PPM for k, v in ZOOM["ppm_to_see"].items()}
FIT_PPM = ZOOM["ppm_to_see"]["clerestory_bottom"]
FIT = PPM / FIT_PPM        # >1: how much wider a view the fit scale shows

def framing(name, wx_, wy_, title):
    px_, py_ = world_to_plate(wx_, wy_, 0.0)
    out = {}
    for tag, zoom in (("plate", 1.0), ("fit", FIT)):
        cw, ch = int(round(VIEW_W*zoom)), int(round(VIEW_H*zoom))
        ax_, ay_ = ANC_X*zoom, ANC_Y*zoom
        x0 = int(round(px_ - ax_)); y0 = int(round(py_ - ay_))
        crop = Image.new("RGB", (cw, ch), (0, 255, 0))
        sx0, sy0 = max(x0, 0), max(y0, 0)
        sx1, sy1 = min(x0+cw, W), min(y0+ch, H)
        if sx1 > sx0 and sy1 > sy0:
            crop.paste(guide.crop((sx0, sy0, sx1, sy1)), (sx0-x0, sy0-y0))
        sub = cls[max(y0,0):max(y0,0)+ch, max(x0,0):max(x0,0)+cw]
        hasw = (sub == IDX["wall_rising"]).any()
        top_wall = int(np.argmax((sub == IDX["wall_rising"]).any(1))) if hasw else -1
        maxe = float(elev_m[max(y0,0):max(y0,0)+ch, max(x0,0):max(x0,0)+cw][
                     fg[max(y0,0):max(y0,0)+ch, max(x0,0):max(x0,0)+cw]].max())
        img = crop.resize((VIEW_W, VIEW_H), Image.LANCZOS) if zoom != 1.0 else crop
        d = ImageDraw.Draw(img)
        hpx = 130.0 / zoom
        d.ellipse([ANC_X-11, ANC_Y-7, ANC_X+11, ANC_Y+7], outline=(255, 60, 60), width=3)
        d.rectangle([ANC_X-13, ANC_Y-hpx, ANC_X+13, ANC_Y], outline=(255, 60, 60), width=3)
        d.text((ANC_X+20, ANC_Y-hpx-4), "player %.0f px" % hpx, fill=(255, 60, 60), font=Fs,
               stroke_width=3, stroke_fill=(0, 0, 0))
        d.text((24, 20), title, fill=(255, 255, 255), font=F, stroke_width=3, stroke_fill=(0, 0, 0))
        if zoom == 1.0:
            d.text((24, 56), "PLATE SCALE, 1:1 -- exactly what the 2D runtime camera shows today "
                             "(ppm %.4f, anchor %d,%d)" % (PPM, ANC_X, ANC_Y),
                   fill=(210, 210, 220), font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
        else:
            d.text((24, 56), "FIT SCALE, ppm %.3f (player %.0f px) -- the zoom at which the "
                             "clerestory sill enters frame. NOT the runtime today." % (FIT_PPM, hpx),
                   fill=(160, 230, 255), font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
        d.text((24, 92), "highest building point in this frame: %.2f m   |   rising masonry "
                         "reaches frame row %s" % (maxe, top_wall if hasw else "n/a (none in frame)"),
               fill=(255, 220, 90), font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
        img.save(OUT + "/framing_%s_%s.png" % (name, tag))
        out[tag] = dict(frame_rect_px=[x0, y0, x0+cw, y0+ch], highest_point_in_frame_m=maxe,
                        topmost_rising_masonry_row=top_wall)
    return dict(name=name, player_m=[wx_, wy_], plate_px=[px_, py_], **out)

frames = [
    framing("south_entry", SPEC["spawn"]["player_spawn_m"][0], SPEC["spawn"]["player_spawn_m"][1],
            "SOUTH ENTRY -- the player at the spawn, looking up the nave"),
    framing("mid_nave_crossing", 0.0, -7.0,
            "MID-NAVE AT THE CROSSING -- the demon-gate crater ahead"),
    framing("near_dais", 0.0, 13.0, "NEAR THE DAIS -- the apse and the empty cross mount ahead"),
]
for f in frames:
    print("  framing %-18s player (%6.2f,%7.2f)  plate: highest point %5.2f m  |  fit: %5.2f m"
          % (f["name"], f["player_m"][0], f["player_m"][1],
             f["plate"]["highest_point_in_frame_m"], f["fit"]["highest_point_in_frame_m"]))
print("  ZOOM: a %dx%d frame at plate scale covers %.3f m of ground along the view axis; the two "
      "nave walls are %.3f m apart along it" % (VIEW_W, VIEW_H, ZOOM["frame_ground_depth_m"],
                                                ZOOM["nave_wall_to_wall_along_view_axis_m"]))
print("        ppm to fit both nave walls: %.3f (player %.0f px)"
      % (ZOOM["ppm_to_fit_both_nave_walls"], ZOOM["person_px_to_fit_both_nave_walls"]))
for k in ZOOM["ppm_to_see"]:
    print("        ppm to bring %-18s into frame: %7.3f (player %3.0f px)"
          % (k, ZOOM["ppm_to_see"][k], ZOOM["person_px_at"][k]))

# ----------------------------------------------------------------- 10. MANIFEST
outs = {}
for fn in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, fn)
    if os.path.isfile(p) and fn.endswith(".png"):
        outs[fn] = dict(sha256=sha(p), bytes=os.path.getsize(p))
meas = dict(
    id_snap_max_distance=maxerr,
    legend_classes_with_no_visible_pixel=_missing,
    depth_floor_median_mm=floor_med, depth_wall_max_mm=wall_max,
    depth_expected_floor_mm=8000, depth_expected_wall_mm=(WALL_RISE - H_MIN)*1000,
    clamp_px=clamp_px,
    clamp_rule=CANV["clamp"]["rule"],
    crown_clearance=dict(
        method="block-max elevation (%d px blocks) under a sliding 1920x1080 frame, evaluated at "
               "every camera centre the clamp allows" % BLK,
        highest_building_point_ever_in_frame_m=vis_max_elev,
        rising_wall_crown_m=WALL_RISE,
        rising_wall_crown_declared_m=WALL_RISE_DECLARED,
        clearance_m=crown_clear_m,
        crown_pixels_on_plate=int(crown_px.sum()),
        crown_blocks_on_plate=crown_blocks_total,
        crown_blocks_inside_any_reachable_frame=crown_blocks_in_frame,
        crown_test="PASS" if crown_blocks_in_frame == 0 else "FAIL",
        analytic_bound_m=ANC_Y/PXE,
        analytic_bound_note="at plate scale a 1080 frame with the anchor at row %d can show at "
                            "most %.4f m of elevation above the player's own plan position, and "
                            "less as the wall recedes; so any wall above that is off the top."
                            % (ANC_Y, ANC_Y/PXE)),
    walkable_area_plan_m2=area_plan, walkable_area_on_screen_m2=area_screen_m2,
    walkable_occlusion_loss_pct=100.0*(1 - area_screen_m2/area_plan),
    walkable_class_area_on_screen_m2=per_class,
    rise_test=REG["rise_test"],
    void_fraction_inside_frame_union_pct=100*void_in_reach,
    framings=frames,
    zoom_analysis=ZOOM,
    chunk_grid=[nrows, ncols], chunks_kept=len(order), chunks_dropped=len(dropped),
    chunks_in_clamp=sum(1 for o in order if o["in_camera_clamp"]),
    camera_clamp_plate_rect_px=CANV["clamp"]["plate_rect_px"],
    wall_rise_built_m=CANV["wall_rise_built_m"], wall_rise_solved_m=CANV["wall_rise_solved_m"],
    plate_top_elevation_m=CANV["plate_top_elevation_m"],
)
json.dump(dict(measurements=meas, outputs=outs), open(OUT + "/measurements_v1.json", "w"), indent=1)
print("\nwrote", OUT)
