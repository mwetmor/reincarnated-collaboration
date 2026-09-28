#!/usr/bin/env python3
"""
CA-guides-v2 post pass. Stitches the five passes, derives the masks, MEASURES the crown
clearance and the pier-frame fraction, computes the FLOOR LIGHT guide (vault shadow + sunset
shafts), cuts the chunks, and renders the overview plus four PLATE-scale framings.
"""
import json, math, os, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None

import sys
VAR = "3"
PROJ = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cathedral_greybox"
OUT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/CA-guides-v3"
os.makedirs(OUT, exist_ok=True)
os.makedirs(OUT + "/chunks", exist_ok=True)

TILES = ("/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/"
         "7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/ca3_tiles")
SPEC = json.load(open(PROJ + "/cathedral_spec.json"))
GEOM = json.load(open(PROJ + "/geometry_v3.json"))
CANV = json.load(open(PROJ + "/canvas_v3.json"))
REG = json.load(open(PROJ + "/registration_v3.json"))
LEG = GEOM["legend"]
IDX = {e["name"]: e["index"] for e in LEG}
W, H = CANV["canvas_px"]
OSX, OSY = CANV["origin_screen_px"]
PPM, PXG, PXE = CANV["ppm"], CANV["pxg"], CANV["pxe"]
RV, DV = CANV["r_plan_NE"], CANV["d_plan_NW"]
VIEW_W, VIEW_H = SPEC["runtime_camera"]["view_px"]
ANC_X, ANC_Y = SPEC["runtime_camera"]["anchor_px"]
WALL_RISE = CANV["wall_rise_built_m"]
PIER_H = CANV["pier_height_m"]
SOLVE = REG["solve"]
HW = SOLVE["limb_width_m"] / 2.0
VIN = SOLVE["vessel_width_m"] / 2.0
XP = SOLVE["pier_line_x_m"]
PIER_SEC = SOLVE["pier_section_m"]
H_MIN, H_MAX = -8.0, 64.0
GREEN = (0, 255, 0)

def stitch(kind):
    im = Image.new("RGB", (W, H))
    for t in CANV["tiles"]:
        im.paste(Image.open("%s/%s_%s.png" % (TILES, kind, t["name"])).convert("RGB"),
                 tuple(t["origin_px"]))
    return im

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def world_to_plate(x, y, z=0.0):
    return (PPM*(x*RV[0] + y*RV[1]) - OSX,
            -(PXG*(x*DV[0] + y*DV[1]) + PXE*z) - OSY)

def snap(im):
    a = np.asarray(im, dtype=np.uint8)
    pk = (a[..., 0].astype(np.uint32) << 16) | (a[..., 1].astype(np.uint32) << 8) | a[..., 2]
    uq, inv = np.unique(pk, return_inverse=True)
    uc = np.stack([(uq >> 16) & 255, (uq >> 8) & 255, uq & 255], -1).astype(np.int32)
    pal = np.array([e["rgb"] for e in LEG], dtype=np.int32)
    du = ((uc[:, None, :] - pal[None, :, :])**2).sum(-1)
    return du.argmin(1).astype(np.uint8)[inv].reshape(H, W), int(np.sqrt(du.min(1)).max())

PAL = np.array([e["rgb"] for e in LEG], dtype=np.uint8)
VPAR = REG["variant_params"]
OPAC = {IDX["wall_rising_fade"]: 1.0}
for bi, (_z0, _z1, _op) in enumerate(VPAR["bands"]):
    OPAC[IDX[VPAR["ghost_classes"][min(bi, len(VPAR["ghost_classes"])-1)]]] = _op
opac_map = np.zeros(len(LEG), np.float32)
for k_, v_ in OPAC.items(): opac_map[k_] = v_
FADE_RADIUS_M = 6.0   # DECLARED: the T3m fade radius is not a ruled number. 6.0 m is about
                      # three body-widths, the distance at which a 2 m pier stops being a wall.


# ------------------------------------------------------------------ 1. PLATE
print("id ...");     cls, maxerr = snap(stitch("id"))
print("  id snap max distance from a legend colour: %d (0 = byte-exact)" % maxerr)
print("guide ...");  guide = stitch("guide")
g = np.asarray(guide).copy()
greenish = (cls == IDX["opening_to_outside"]) | (cls == IDX["void_outside_frame"])
g[greenish] = GREEN
guide = Image.fromarray(g)
guide.save(OUT + "/ortho_canvas_v2guide.png")
Image.fromarray(PAL[cls]).save(OUT + "/ortho_canvas_id.png")
walk_ids = [e["index"] for e in LEG if e["walkable"]]
walkable = np.isin(cls, walk_ids)
Image.fromarray((walkable*255).astype(np.uint8)).save(OUT + "/ortho_canvas_walkable.png")
window = cls == IDX["opening_to_outside"]
Image.fromarray((window*255).astype(np.uint8)).save(OUT + "/ortho_canvas_window_holes.png")

print("height ...")
hr = np.asarray(stitch("height"), dtype=np.uint32)
raw = hr[..., 0]*256 + hr[..., 1]
fg = ~greenish
elev_m = H_MIN + raw.astype(np.float64)/65535.0*(H_MAX - H_MIN)
depth = np.full((H, W), 65535, np.uint16)
depth[fg] = np.clip((elev_m[fg] - H_MIN)*1000.0, 0, 65000).astype(np.uint16)
Image.fromarray(depth, mode="I;16").save(OUT + "/ortho_canvas_depth_mm.png")
fl = np.isin(cls, [IDX[n] for n in ("nave_floor", "crossing_floor", "transept_floor", "aisle_floor")])
print("  depth decode check: floor median %.0f mm (expect 8000), wall max %.0f (expect %.0f)"
      % (np.median(depth[fl]), depth[cls == IDX["wall_rising"]].max(), (WALL_RISE-H_MIN)*1000))

# ------------------------------------------------------- 2. FADE + VAULT LAYERS
print("fade / vault ...")
fade_rgb = np.asarray(stitch("fade"))
fade_a = ~np.all(fade_rgb == GREEN, -1)
fade_cls, fade_err = snap(stitch("id_fade"))
Image.fromarray(np.dstack([fade_rgb, (fade_a*255).astype(np.uint8)])).save(
    OUT + "/fade_layerguide.png")
Image.fromarray((fade_a*255).astype(np.uint8)).save(OUT + "/fade_layermask.png")
arch_rgb = np.asarray(stitch("arch"))
arch_a = ~np.all(arch_rgb == GREEN, -1)
vault_rgb = np.asarray(stitch("vault"))
vault_a = ~np.all(vault_rgb == GREEN, -1)
Image.fromarray(np.dstack([vault_rgb, (vault_a*255).astype(np.uint8)])).save(
    OUT + "/overhead_vaultguide.png")
Image.fromarray((vault_a*255).astype(np.uint8)).save(OUT + "/overhead_vaultmask.png")

# ------------------------------------------------- 3. CROWN + PIER-FRAME FRACTION
BLK = 8
def ba(a):
    hh, ww = (H//BLK)*BLK, (W//BLK)*BLK
    return a[:hh, :ww].reshape(hh//BLK, BLK, ww//BLK, BLK).any((1, 3))
W8 = ba(walkable)
FR = (VIEW_H//BLK + 1, VIEW_W//BLK + 1)
shift = (int(round(-(ANC_Y - VIEW_H/2)/BLK)), int(round(-(ANC_X - VIEW_W/2)/BLK)))
centres = np.roll(W8, shift, axis=(0, 1))
frames_union = ndimage.maximum_filter(centres.astype(np.uint8), size=FR,
                                      mode="constant", cval=0).astype(bool)
masonry = (cls == IDX["wall_rising"]) | (cls == IDX["wall_rising_fade"]) | (cls == IDX["clerestory_tracery"])
crown_px = masonry & (elev_m >= WALL_RISE - 0.5) & fg
crown_in = int((ba(crown_px) & frames_union).sum())
print("  CROWN TEST (plate walls): crown blocks inside any reachable frame = %d  -> %s"
      % (crown_in, "PASS" if crown_in == 0 else "FAIL"))
# the fade pass is SHADED, so its pixels carry guide greys, not id colours. Matching id colours
# against it found nothing and reported 0 % pier coverage -- a detector aimed at the wrong pass.
# The id_fade pass is the one that answers this question.
pier_px = fade_a & (fade_cls == IDX["nave_pier"])
fadewall_px = fade_a & (fade_cls == IDX["wall_rising_fade"])
riser = ba(masonry | crown_px) | ba(pier_px)
seen = ndimage.maximum_filter(riser.astype(np.uint8), size=FR, mode="constant", cval=0).astype(bool)
n_frames = int(centres.sum())
n_with = int((centres & seen).sum())
pier_only = ndimage.maximum_filter(ba(pier_px).astype(np.uint8), size=FR,
                                   mode="constant", cval=0).astype(bool)
n_pier = int((centres & pier_only).sum())
# 100 % at the SPRITE height is partly an artifact of drawing the shaft to the canvas top.
# Measure again at the ARCHITECTURAL pier height (the vault springing), which is the arcade a
# viewer would actually read, by rasterising each pier's screen quad from z = 0 to the springing.
SPRING = REG["vault"]["vessel_spring_m"]
qcanv = Image.new("1", (W//BLK + 1, H//BLK + 1), 0)
qd = ImageDraw.Draw(qcanv)
for pr in REG["piers"]:
    if pr["corner"]: continue
    cx_, cy_ = pr["centre_m"]; hw_ = PIER_SEC/2
    pts = []
    for (ax, ay) in ((cx_-hw_, cy_-hw_), (cx_+hw_, cy_-hw_), (cx_+hw_, cy_+hw_), (cx_-hw_, cy_+hw_)):
        for zz in (0.0, SPRING):
            a, b = world_to_plate(ax, ay, zz); pts.append((a/BLK, b/BLK))
    xs_ = [q[0] for q in pts]; ys_ = [q[1] for q in pts]
    qd.polygon([(min(xs_), min(ys_)), (max(xs_), min(ys_)),
                (max(xs_), max(ys_)), (min(xs_), max(ys_))], fill=1)
q8 = np.asarray(qcanv, bool)[:centres.shape[0], :centres.shape[1]]
pier26 = ndimage.maximum_filter(q8.astype(np.uint8), size=FR, mode="constant", cval=0).astype(bool)
n_pier26 = int((centres & pier26).sum())
print("  PIER-FRAME FRACTION over %d reachable camera positions (%d px blocks):" % (n_frames, BLK))
print("    frames containing a rising pier OR rising wall : %d = %.2f %%" % (n_with, 100*n_with/n_frames))
print("    frames containing a rising PIER (sprite, to canvas top): %d = %.2f %%" % (n_pier, 100*n_pier/n_frames))
print("    frames containing a pier up to the vault springing %.0f m: %d = %.2f %%"
      % (SPRING, n_pier26, 100*n_pier26/n_frames))
void_in = float((frames_union & ba(cls == IDX["void_outside_frame"])).sum())/float(frames_union.sum())
px2 = PPM*PXG
print("  WALKABLE on screen %.3f m2 (plan %.3f) -- %.3f %% hidden; void in frame union %.3f %%"
      % (walkable.sum()/px2, SOLVE["raster_check_m2"],
         100*(1 - (walkable.sum()/px2)/SOLVE["raster_check_m2"]), 100*void_in))

# ------------------------------------------------------------ 4. FLOOR LIGHT
# The vault's shadow and the sunset SHAFTS from the west clerestory, as a greyscale floor-light
# guide. Computed, never baked as geometry (R-C9-53 cl.2).
CELL = 0.20
gx0, gx1 = -HW - 12.0, HW + 34.0
gy0, gy1 = SPEC["room"]["bbox_m"][1] - 14.0, SPEC["room"]["bbox_m"][3] + 12.0
NX = int((gx1-gx0)/CELL); NY = int((gy1-gy0)/CELL)
GXv = gx0 + (np.arange(NX)+0.5)*CELL
GYv = gy0 + (np.arange(NY)+0.5)*CELL
GX, GY = np.meshgrid(GXv, GYv, indexing="ij")

west_openings = [o for o in REG["openings"]
                 if o["band"] in ("clerestory", "triforium", "west_top_breach")
                 and o["centre_m"][0] < 0 and abs(o["centre_m"][0] + HW) < 2.5]
WALL_PLANE = -HW - 0.75
# SOLVE the sun elevation: the clerestory SILL's shaft is to land on the far (east) edge of the
# central vessel -- the classic "gold shafts rake east across the floor between the piers".
CLE_SILL = SPEC["elevation"]["clerestory"][0] + 1.5
THETA = math.degrees(math.atan2(CLE_SILL, (VIN - WALL_PLANE)))
COT = 1.0/math.tan(math.radians(THETA))
SUNSET_LOW = 12.0
sunset_land = WALL_PLANE + CLE_SILL/math.tan(math.radians(SUNSET_LOW))

shaft = np.zeros((NX, NY), np.float32)
for o in west_openings:
    y0, y1 = o["centre_m"][1] - o["width_m"]/2, o["centre_m"][1] + o["width_m"]/2
    z0, z1 = o["z"]
    x0, x1 = WALL_PLANE + z0*COT, WALL_PLANE + z1*COT
    shaft[(GX >= x0) & (GX <= x1) & (GY >= y0) & (GY <= y1)] = 1.0
# piers interrupt the beams: everything east of a pier, within its y-band, inside a beam
for pr in REG["piers"]:
    if pr["corner"]: continue
    px_, py_ = pr["centre_m"]
    shaft[(GX > px_ + PIER_SEC/2) & (np.abs(GY - py_) <= PIER_SEC/2)] = 0.0
shaft = ndimage.gaussian_filter(shaft, 1.6/CELL*0.35)
# the vault reads on the floor as the transverse ribs' banding, at the vault bay pitch
pitch = SOLVE["bay_pitches_m"]["nave_south"]
rib = 0.5 + 0.5*np.cos(2*math.pi*GY/pitch)
rib = rib**6
# ambient: brighter toward the window wall
amb = np.clip(1.0 - (GX - WALL_PLANE)/(2.2*SOLVE["limb_width_m"]), 0.0, 1.0)
Lp = np.clip(0.18 + 0.62*shaft + 0.14*amb - 0.09*rib, 0.0, 1.0)

# map to plate pixels through the plan-position solve (exact, uses the decoded elevation)
c, s = RV[0], RV[1]
sx = (np.arange(W, dtype=np.float32) + OSX)[None, :]
sy = (np.arange(H, dtype=np.float32) + OSY)[:, None]
A = sx/PPM
B = (-sy - PXE*elev_m.astype(np.float32))/PXG
Xw = A*c - B*s
Yw = A*s + B*c
ix = np.clip(((Xw-gx0)/CELL).astype(np.int32), 0, NX-1)
iy = np.clip(((Yw-gy0)/CELL).astype(np.int32), 0, NY-1)
floor_light = np.where(walkable, (Lp[ix, iy]*255).astype(np.uint8), 0)
Image.fromarray(floor_light).save(OUT + "/floor_light.png")
print("  FLOOR LIGHT: sun solved at %.2f deg elevation (west). A true sunset at %.0f deg puts the "
      "clerestory-sill shaft at x = %.1f m -- %.1f m past the east wall, i.e. outside the building."
      % (THETA, SUNSET_LOW, sunset_land, sunset_land - HW))
del A, B, Xw, Yw

# ------------------------------- 4b. EFFECTIVE FLOOR OCCLUSION (the deciding metric)
# v2 reported "3.99 % walkable occlusion" and it was measured ON THE PLATE -- after the piers
# and the vault had been moved OUT of the plate. The honest question is: standing anywhere he
# can stand, WITH the T3m fade applied, what share of the floor within 12 m of the player is
# obscured by any layer? Opacity-weighted, because a 35 % ghost is not a wall.
Z = np.load(PROJ + "/occl_v3.npz")
walkp = Z["walk"]; occl = Z["occl"]; ocen = Z["centres"]
ggx0, ggy0, gCELL = float(Z["grid"][0]), float(Z["grid"][1]), float(Z["grid"][2])
gNX, gNY = int(Z["grid"][3]), int(Z["grid"][4])
ii, jj = np.nonzero(walkp)
Xc = ggx0 + (ii+0.5)*gCELL; Yc = ggy0 + (jj+0.5)*gCELL
Zc = np.where((np.abs(Xc) <= HW) & (Yc >= 14.0), 1.2, 0.0)
sxp, syp = world_to_plate(Xc, Yc, Zc)
sxp = np.clip(sxp.astype(np.int32), 0, W-1); syp = np.clip(syp.astype(np.int32), 0, H-1)
vault_occ = np.zeros_like(walkp, np.float32)
plate_occ = np.zeros_like(walkp, np.float32)
vault_occ[ii, jj] = vault_a[syp, sxp].astype(np.float32)
plate_occ[ii, jj] = (~walkable[syp, sxp]).astype(np.float32)
static = np.maximum(vault_occ, plate_occ)
vault_floor_cov = float(vault_occ[walkp].mean())

RAD = 12.0
K = int(RAD/gCELL)
yy, xx = np.ogrid[-K:K+1, -K:K+1]
disk = (xx*xx + yy*yy)*gCELL*gCELL <= RAD*RAD
obb = []
for k in range(occl.shape[0]):
    nz = np.nonzero(occl[k])
    obb.append((nz[0].min(), nz[0].max(), nz[1].min(), nz[1].max()) if len(nz[0]) else None)
STRIDE = 10
res_w, res_h, res_nf = [], [], []
pi, pj = np.nonzero(walkp)
sel = (pi % STRIDE == 0) & (pj % STRIDE == 0)
for a_, b_ in zip(pi[sel], pj[sel]):
    i0, i1 = a_-K, a_+K+1
    j0, j1 = b_-K, b_+K+1
    if i0 < 0 or j0 < 0 or i1 > gNX or j1 > gNY: continue
    near = walkp[i0:i1, j0:j1] & disk
    n = near.sum()
    if n < 50: continue
    px_ = ggx0 + (a_+0.5)*gCELL; py_ = ggy0 + (b_+0.5)*gCELL
    acc = static[i0:i1, j0:j1].copy()
    accnf = acc.copy()
    for k in range(occl.shape[0]):
        bb = obb[k]
        if bb is None or bb[0] >= i1 or bb[1] < i0 or bb[2] >= j1 or bb[3] < j0: continue
        w_ = occl[k][i0:i1, j0:j1]
        accnf = np.maximum(accnf, w_)
        if math.hypot(ocen[k][0]-px_, ocen[k][1]-py_) <= FADE_RADIUS_M: continue
        acc = np.maximum(acc, w_)
    res_w.append(float((acc*near).sum()/n))
    res_h.append(float(((acc >= 0.999) & near).sum()/n))
    res_nf.append(float((accnf*near).sum()/n))
OCC_W = float(np.mean(res_w)); OCC_H = float(np.mean(res_h)); OCC_NF = float(np.mean(res_nf))
print("  EFFECTIVE FLOOR OCCLUSION within %.0f m, averaged over %d stands, fade at %.0f m:"
      % (RAD, len(res_w), FADE_RADIUS_M))
print("    opacity-weighted  %.2f %%   fully opaque  %.2f %%   (no fade at all: %.2f %%)"
      % (100*OCC_W, 100*OCC_H, 100*OCC_NF))
print("  VAULT floor coverage (ribs only): %.2f %% of walkable" % (100*vault_floor_cov))

# ------------------------------------------------- 4c. DEBRIS ASSERTION, ON PIXELS
deb_px = int((cls == IDX["debris"]).sum())
deb_on_walk = int(((cls == IDX["debris"]) & walkable).sum())
print("  DEBRIS on the rendered plate: %d px; overlapping a walkable pixel: %d (assert 0)"
      % (deb_px, deb_on_walk))
assert deb_on_walk == 0
brk_px = int((fade_cls == IDX["pier_break"]).sum())
print("  BLASTED CROWNS (class pier_break, where the brief calls for scorch): %d px" % brk_px)

# ----------------------------------------------------------------- 5. CHUNKS
CW, CH_, OVL = 1536, 1024, 256
SW, SH = CW-OVL, CH_-OVL
ncols = max(1, math.ceil((W-OVL)/SW)); nrows = max(1, math.ceil((H-OVL)/SH))
cl_rect = CANV["clamp"]["plate_rect_px"]
kept, order, dropped = {}, [], []
for r in range(nrows):
    for c_ in range(ncols):
        ox, oy = c_*SW, r*SH
        frac = float(fg[oy:oy+CH_, ox:ox+CW].mean())
        nm = "cath_%d_%d" % (r, c_)
        if frac < 0.01: dropped.append(dict(chunk=nm, origin_px=[ox, oy], fg_fraction=round(frac, 4)))
        else: kept[(r, c_)] = nm
step = 0
for r in range(nrows):
    for c_ in range(ncols):
        if (r, c_) not in kept: continue
        step += 1; nm = kept[(r, c_)]; ox, oy = c_*SW, r*SH
        sl = (slice(oy, oy+CH_), slice(ox, ox+CW))
        guide.crop((ox, oy, ox+CW, oy+CH_)).save("%s/chunks/%s_guide.png" % (OUT, nm))
        Image.fromarray(PAL[cls[sl]]).save("%s/chunks/%s_id.png" % (OUT, nm))
        Image.fromarray((walkable[sl]*255).astype(np.uint8)).save("%s/chunks/%s_mask.png" % (OUT, nm))
        Image.fromarray(depth[sl], mode="I;16").save("%s/chunks/%s_depth.png" % (OUT, nm))
        Image.fromarray((window[sl]*255).astype(np.uint8)).save("%s/chunks/%s_window.png" % (OUT, nm))
        Image.fromarray(floor_light[sl]).save("%s/chunks/%s_light.png" % (OUT, nm))
        Image.fromarray(np.dstack([vault_rgb[sl], (vault_a[sl]*255).astype(np.uint8)])).save(
            "%s/chunks/%s_vault.png" % (OUT, nm))
        in_clamp = not (ox+CW <= cl_rect[0] or ox >= cl_rect[2] or oy+CH_ <= cl_rect[1] or oy >= cl_rect[3])
        order.append(dict(step=step, chunk=nm, index=[r, c_], origin_px=[ox, oy], size_px=[CW, CH_],
                          in_camera_clamp=bool(in_clamp),
                          fg_fraction=round(float(fg[sl].mean()), 4),
                          walkable_fraction=round(float(walkable[sl].mean()), 4),
                          window_fraction=round(float(window[sl].mean()), 4),
                          vault_fraction=round(float(vault_a[sl].mean()), 4),
                          paint_after=[kept[k] for k in ((r, c_-1), (r-1, c_)) if k in kept],
                          corner_overlaps_already_painted=[kept[k] for k in ((r-1, c_-1), (r-1, c_+1)) if k in kept],
                          files={k: "chunks/%s_%s.png" % (nm, k) for k in
                                 ("guide", "id", "mask", "depth", "window", "light", "vault")}))
print("  chunks: grid %dx%d, kept %d, dropped %d, in clamp %d"
      % (nrows, ncols, len(order), len(dropped), sum(1 for o in order if o["in_camera_clamp"])))
json.dump(dict(ruling="R-C9-43/44/45 + R-C9-53 -- CA-GREYBOX-V2",
               canvas_px=[W, H], chunk_px=[CW, CH_], step_px=[SW, SH], overlap_px=[OVL, OVL],
               px_per_m=PPM, projection=SPEC["projection"], origin_screen_px=[OSX, OSY],
               camera_clamp_plate_rect_px=cl_rect,
               keep_rule="architecture fraction >= 1 %",
               layers=dict(plate="guide/id/mask/depth/window",
                           fade="fade_layer_v2_* -- piers and the occluding west-wall bays; NOT "
                                "in the plate, because a fading prop must have floor painted "
                                "behind it",
                           overhead="overhead_vault_v2_* and per-chunk _vault.png -- the ceiling "
                                    "layer, scroll > 1, edge-anchored (T3p)",
                           floor_light="floor_light_v2.png and per-chunk _light.png -- greyscale; "
                                       "the vault's banding and the sunset shafts. A PAINTER'S "
                                       "CUE, never geometry"),
               depth_format=dict(png="16-bit greyscale", decode="elevation_m = value/1000 - 8.000",
                                 floor_plane=8000, not_foreground=65535),
               guide_rule="every opening to the OUTSIDE and every un-architected background pixel "
                          "is flat pure #00ff00",
               guide_legend={e["name"]: dict(id_rgb=e["rgb"], guide_grey=e["guide_grey"],
                                             walkable=e["walkable"]) for e in LEG},
               paint_order_rule="row by row, top to bottom, left to right; a chunk is painted "
                                "after its left and above neighbours (when kept)",
               paint_order=order, dropped=dropped),
          open(OUT + "/chunks.json", "w"), indent=1)
json.dump(dict(legend=LEG,
               window_hole_rule="id class 'opening_to_outside' only; 'void_outside_frame' is "
                                "background, not a window",
               fade_classes=["nave_pier", "wall_rising_fade"],
               vault_classes=["vault_rib", "vault_cell"]),
          open(OUT + "/legend.json", "w"), indent=1)

# -------------------------------------------------------- 6. COMPOSITES
def composite(base_rgb, rect, vault_alpha=0.55, upper=None, fade_at=None):
    """upper: (rgb, alpha_mask) for the vertical layer -- the fade layer, or the arch layer for
    a plan-reading overview. fade_at: player (x,y) -- previews the T3m pier fade around him."""
    x0, y0, x1, y1 = rect
    out = base_rgb[y0:y1, x0:x1].astype(np.float32).copy()
    urgb, ua = upper
    ua = ua[y0:y1, x0:x1]
    urgb = urgb[y0:y1, x0:x1]
    if fade_at is not None:
        faded = np.zeros_like(ua)
        for pr in REG["piers"]:
            if pr["corner"]: continue
            cx_, cy_ = pr["centre_m"]
            if math.hypot(cx_-fade_at[0], cy_-fade_at[1]) > FADE_RADIUS_M: continue
            qs = [world_to_plate(cx_+sx*PIER_SEC/2, cy_+sy*PIER_SEC/2, zz)
                  for sx in (-1, 1) for sy in (-1, 1) for zz in (-0.3, PIER_H)]
            ax0 = int(max(min(q[0] for q in qs)-x0, 0)); ax1 = int(min(max(q[0] for q in qs)-x0, x1-x0))
            ay0 = int(max(min(q[1] for q in qs)-y0, 0)); ay1 = int(min(max(q[1] for q in qs)-y0, y1-y0))
            if ax1 > ax0 and ay1 > ay0: faded[ay0:ay1, ax0:ax1] = True
        al = opac_map[fade_cls[y0:y1, x0:x1]] * ua
        al = np.where(faded, al*0.22, al)[..., None]
        out = (1-al)*out + al*urgb
    else:
        out[ua] = urgb[ua]
    va = vault_a[y0:y1, x0:x1]
    out[va] = (1-vault_alpha)*out[va] + vault_alpha*vault_rgb[y0:y1, x0:x1][va]
    return out.astype(np.uint8)

ovbase = np.asarray(guide).copy()
ovbase[greenish] = (38, 30, 46)
ovbase[window] = (74, 58, 96)
ov = composite(ovbase, (0, 0, W, H), 0.30, upper=(arch_rgb, arch_a))
big = Image.fromarray(ov)
OVW = 2600
sc = OVW/W
img = big.resize((OVW, int(H*sc)), Image.LANCZOS).convert("RGB")
dr = ImageDraw.Draw(img)
try:
    F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
    Fs = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
except Exception:
    F = Fs = ImageFont.load_default()
def mark(x, y, z, lab, col=(255, 210, 60), dy=-10):
    a, b = world_to_plate(x, y, z); a, b = a*sc, b*sc
    dr.ellipse([a-5, b-5, a+5, b+5], outline=col, width=3)
    dr.text((a+12, b+dy), lab, fill=col, font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
mark(0, 0, 0, "CROSSING / crater r 4.5 m")
mark(*SPEC["spawn"]["player_spawn_m"], 0, "PLAYER SPAWN")
for e in SPEC["entrances"]:
    mark(e["centre_m"][0], e["centre_m"][1], 0, e["id"], col=(120, 200, 255))
mark(0, 17.5, 1.2, "DAIS", col=(255, 130, 210))
mark(0, SPEC["room"]["bbox_m"][3], 17.0, "EMPTY CROSS MOUNT", col=(255, 255, 255))
for p in REG["pools"]:
    if p["verdict"] == "KEEP":
        mark(p["arena_m"][0], p["arena_m"][1], 0, "pool %s" % p["id"], col=(255, 120, 255))
mark(-XP, -25.0, 0, "PIER ARCADE (fades)", col=(255, 150, 90))
mark(-(XP + PIER_SEC/2 + 2.25), -32.0, 0, "WEST AISLE (walkable)", col=(140, 255, 190))
cx_, cy_ = OVW-250, 150
for ang, lab in ((0, "N"), (90, "E"), (180, "S"), (270, "W")):
    a_ = math.radians(ang); ex, ey = math.sin(a_), math.cos(a_)
    dx = PPM*(ex*RV[0]+ey*RV[1])*sc*0.55; dy_ = -(PXG*(ex*DV[0]+ey*DV[1]))*sc*0.55
    dr.line([cx_, cy_, cx_+dx, cy_+dy_], fill=(255, 220, 90), width=3)
    dr.text((cx_+dx*1.3-8, cy_+dy_*1.3-12), lab, fill=(255, 220, 90), font=F,
            stroke_width=3, stroke_fill=(0, 0, 0))
bx, by = 60, int(H*sc)-70
dr.line([bx, by, bx+PPM*10*sc, by], fill=(255, 255, 255), width=5)
dr.text((bx, by-34), "10 m along screen-east (ppm %.3f)" % PPM, fill=(255, 255, 255), font=Fs,
        stroke_width=3, stroke_fill=(0, 0, 0))
dr.text((60, 40), "CATHEDRAL ARENA GREY BOX  CA-guides-v%s  --  %s" % (VAR, {
    "a": "GHOSTED SHAFTS (solid to 4 m, 35 %% above)",
    "b": "RUINED ARCADE (two thirds broken 2-7 m)",
    "c": "FEWER, SLIMMER (9.5 m bays, 1.4 m section)",
    "d": "GRADED GHOST (solid to 4 m, 0.60/0.30/0.12 by height)",
    "z": "BASELINE -- v2 as built, all piers solid full height",
    "3": "CANONICAL v3 -- ruined arcade + graded ghosts + debris (R-C9-55)"}[VAR]),
        fill=(255, 255, 255), font=F, stroke_width=3, stroke_fill=(0, 0, 0))
dr.text((60, 78), "plate + piers to the vault springing + VAULT layer at 30%% | limb %.3f m = 4.500 aisle + "
                  "2.00 pier + %.3f vessel + 2.00 + 4.500 | walkable %.1f m2 | %d piers | walls %.0f m"
        % (SOLVE["limb_width_m"], SOLVE["vessel_width_m"], SOLVE["target_m2"],
           SOLVE["n_piers"], WALL_RISE) + "  |  floor hidden within 12 m: %.1f %%" % (100*OCC_W),
        fill=(220, 220, 230), font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
img.save(OUT + "/overview_flat.png")

FRAMINGS = [
    ("south_entry", SPEC["spawn"]["player_spawn_m"][0], SPEC["spawn"]["player_spawn_m"][1],
     "SOUTH ENTRY -- the player at the spawn, looking up the nave"),
    ("mid_nave_crossing", 0.0, -7.0, "MID-NAVE AT THE CROSSING -- the crater ahead"),
    ("near_dais", 0.0, 13.0, "NEAR THE DAIS -- the apse and the empty cross mount ahead"),
    ("west_aisle", -(XP + PIER_SEC/2 + 2.25), -26.0,
     "INSIDE THE WEST AISLE -- between the pier arcade and the outer wall"),
]
frames = []
for name, wx_, wy_, title in FRAMINGS:
    px_, py_ = world_to_plate(wx_, wy_, 0.0)
    x0 = int(round(px_ - ANC_X)); y0 = int(round(py_ - ANC_Y))
    cx0, cy0 = max(x0, 0), max(y0, 0)
    cx1, cy1 = min(x0+VIEW_W, W), min(y0+VIEW_H, H)
    crop = Image.new("RGB", (VIEW_W, VIEW_H), GREEN)
    if cx1 > cx0 and cy1 > cy0:
        crop.paste(Image.fromarray(composite(np.asarray(guide), (cx0, cy0, cx1, cy1), 0.40,
                                             upper=(fade_rgb, fade_a), fade_at=(wx_, wy_))),
                   (cx0-x0, cy0-y0))
    sl = (slice(cy0, cy1), slice(cx0, cx1))
    has_pier = bool(pier_px[sl].any()); has_vault = bool(vault_a[sl].any())
    has_wall = bool(masonry[sl].any())
    d = ImageDraw.Draw(crop)
    d.ellipse([ANC_X-11, ANC_Y-7, ANC_X+11, ANC_Y+7], outline=(255, 60, 60), width=3)
    d.rectangle([ANC_X-13, ANC_Y-130, ANC_X+13, ANC_Y], outline=(255, 60, 60), width=3)
    d.text((ANC_X+20, ANC_Y-134), "player 130 px", fill=(255, 60, 60), font=Fs,
           stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((24, 20), title, fill=(255, 255, 255), font=F, stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((24, 56), "PLATE SCALE 1:1 -- plate + fade layer (piers) + vault layer at 40%%. The "
                     "T3m pier fade is PREVIEWED within %.0f m of the player." % FADE_RADIUS_M,
           fill=(210, 210, 220), font=Fs,
           stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((24, 92), "in frame:  rising pier %s   vault %s   rising wall %s"
           % ("YES" if has_pier else "no", "YES" if has_vault else "no",
              "YES" if has_wall else "no"),
           fill=(255, 220, 90), font=Fs, stroke_width=3, stroke_fill=(0, 0, 0))
    crop.save(OUT + "/framing_%s.png" % name)
    frames.append(dict(name=name, player_m=[wx_, wy_], frame_rect_px=[x0, y0, x0+VIEW_W, y0+VIEW_H],
                       pier_in_frame=has_pier, vault_in_frame=has_vault, wall_in_frame=has_wall))
    print("  framing %-18s pier=%-3s vault=%-3s wall=%-3s"
          % (name, has_pier, has_vault, has_wall))

meas = dict(
    solve=SOLVE, wall_rise=REG["wall_rise"], pier_height=REG["pier_height"],
    id_snap_max_distance=maxerr,
    crown_blocks_inside_any_reachable_frame=crown_in,
    crown_test="PASS" if crown_in == 0 else "FAIL",
    reachable_camera_positions_blocks=n_frames,
    frames_with_rising_pier_or_wall=n_with,
    frames_with_rising_pier_or_wall_pct=100*n_with/n_frames,
    frames_with_rising_pier=n_pier, frames_with_rising_pier_pct=100*n_pier/n_frames,
    frames_with_pier_to_vault_springing=n_pier26,
    frames_with_pier_to_vault_springing_pct=100*n_pier26/n_frames,
    vault_springing_m=REG["vault"]["vessel_spring_m"],
    id_fade_snap_max_distance=fade_err,
    fading_wall_pixels=int(fadewall_px.sum()),
    walkable_area_on_screen_m2=walkable.sum()/px2,
    walkable_occlusion_loss_pct=100*(1-(walkable.sum()/px2)/SOLVE["raster_check_m2"]),
    void_fraction_inside_frame_union_pct=100*void_in,
    variant=VAR, variant_params=VPAR,
    fade_preview_radius_m=FADE_RADIUS_M,
    effective_floor_occlusion=dict(
        radius_m=RAD, stands_sampled=len(res_w), fade_radius_m=FADE_RADIUS_M,
        opacity_weighted_pct=100*OCC_W, fully_opaque_pct=100*OCC_H,
        no_fade_opacity_weighted_pct=100*OCC_NF,
        definition="mean over every stand on a 2 m lattice of the walkable floor within 12 m "
                   "that any layer obscures -- plate occluders, the vault layer, and every "
                   "fading occluder more than 6 m away -- weighted by that layer's opacity. "
                   "This is the metric v2 got wrong: v2 measured the PLATE after the occluders "
                   "had left the plate."),
    vault_floor_coverage_pct=100*vault_floor_cov,
    debris=dict(pixels=deb_px, overlapping_walkable_px=deb_on_walk,
                pieces=len(REG["debris"]),
                footprint_total_m2=REG["debris_footprint_total_m2"],
                occludes_walkable_m2=REG["debris_occludes_walkable_m2"],
                rule=REG["debris_rule"]),
    break_profile=REG["break_profile"], blasted_crown_px=brk_px,
    break_fraction=REG["break_fraction"],
    floor_light=dict(sun_elevation_deg_solved=THETA, sun_azimuth="due WEST (screen upper-left)",
                     true_sunset_deg=SUNSET_LOW, sunset_shaft_lands_x_m=sunset_land,
                     model="0.18 base + 0.62 shaft (pier-shadowed) + 0.14 window-proximity "
                           "ambient - 0.09 vault-rib banding at the %.3f m bay pitch" % pitch,
                     west_openings_used=len(west_openings)),
    chunk_grid=[nrows, ncols], chunks_kept=len(order), chunks_dropped=len(dropped),
    chunks_in_clamp=sum(1 for o in order if o["in_camera_clamp"]),
    framings=frames,
    outputs={fn: dict(sha256=sha(OUT+"/"+fn), bytes=os.path.getsize(OUT+"/"+fn))
             for fn in sorted(os.listdir(OUT)) if fn.endswith(".png")})
json.dump(meas, open(OUT + "/measurements.json", "w"), indent=1)
print("\nwrote", OUT)
