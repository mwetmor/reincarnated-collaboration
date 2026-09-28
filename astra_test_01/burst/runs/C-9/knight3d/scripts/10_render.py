#!/usr/bin/env python3
"""C-9 knight3d step 3c: render the 3D body into the GAME's sprite format.

    python3 scripts/10_render.py walk E
    python3 scripts/10_render.py rest          (a static turnaround, for checking)

Game format, measured off the cells the game plays today
(cliffside_B/sprites_knight/*): 512x512 RGBA PNG, one file per frame, the sole
line at y=398, and the knight's body (helm crown to sole) 198.3 px tall, i.e.
110.18 px per metre. Rendered at 4x and box-filtered down, so the ink line has
somewhere to live.

RENDER CAMERA (R-C9-56 clause 1): the stills' own fitted elevation, 19.77 deg,
at EXACT 45-degree azimuth steps and ONE scale for all eight -- the paint is
projected through each still's own crooked camera, but the OUTPUT is on a
clean camera, so it compares fairly against Grok and the cut-out rig. The
world plate's 52.95 deg is a later question and is not used here.

THE INK LINE is drawn at render time, not sampled from the stills: the
painted outlines were stripped in 3a because they belong to one view. Here the
line is drawn around the CURRENT silhouette and the current internal occlusion
and crease edges, at the weight measured off the stills (11_measure_line.py).
"""
import json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knight_proxy as kp
import pose as PS
from raster import raster, tri_normals

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
WORK = os.path.join(K3, "work"); OUT = os.path.join(K3, "out")

# --- the game's sprite format, measured ------------------------------------
FRAME = 512
SOLE_Y = 398.0        # nominal; the true placement is calibrated below
GROK_DIR = os.path.join(ROOT, "cliffside_B", "sprites_knight")
BODY_PX = 198.33333333333334          # knight_fit.json figure_h_src_px
PX_PER_M = BODY_PX / 1.80             # 110.185
SS = 4                                # supersample
THETA = None                          # filled from the fit
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}


def load():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    tex = np.asarray(Image.open(os.path.join(OUT, "knight_paint.png")).convert("RGB"))
    unseen = np.asarray(Image.open(os.path.join(OUT, "paint_unseen.png"))) > 127
    return fit, idx, A, tex, unseen


def render_frame(tri_v, tri_uv, tri_id, tex, alpha, theta, scale, tx, ty, W, H,
                 line_px, unseen=None):
    r, u = kp.basis(alpha, theta)
    c = kp.cam_dir(alpha, theta)
    flat = tri_v.reshape(-1, 3)
    xy = np.stack([flat @ r * scale + tx, -(flat @ u) * scale + ty], -1)
    xy = xy.reshape(len(tri_v), 3, 2)
    z = (-(flat @ c)).reshape(len(tri_v), 3)
    nrm = tri_normals(tri_v)
    # attributes: u, v, nx, ny, nz
    attrs = np.zeros((len(tri_v), 3, 5))
    attrs[:, :, 0:2] = tri_uv
    attrs[:, :, 2:5] = nrm[:, None, :]
    zb, ib, ab, _ = raster(xy, z, attrs, W, H)
    solid = ib >= 0

    col = np.zeros((H, W, 3), np.uint8)
    if solid.any():
        tu = np.clip((ab[..., 0] * tex.shape[1]).astype(int), 0, tex.shape[1] - 1)
        tv = np.clip((ab[..., 1] * tex.shape[0]).astype(int), 0, tex.shape[0] - 1)
        col[solid] = tex[tv[solid], tu[solid]]

    # --- the ink line -----------------------------------------------------
    # Two kinds of edge and nothing else:
    #   SILHOUETTE  -- the figure's outer boundary, always drawn;
    #   OCCLUSION   -- where one piece passes in front of another, i.e. a real
    #                  DEPTH STEP, plus hard CREASES between surfaces meeting
    #                  at a sharp angle.
    # Written first as sobel magnitudes with low thresholds, which inked most
    # of the body: on a faceted proxy the normal gradient is large everywhere,
    # so "gn > 1.5" is not an edge detector, it is a tessellation detector.
    zf = np.where(solid, zb, np.nan)
    zmax = ndi.maximum_filter(np.nan_to_num(zf, nan=-1e9), size=3)
    zmin = ndi.minimum_filter(np.nan_to_num(zf, nan=+1e9), size=3)
    step = solid & ((zmax - np.nan_to_num(zf)) > 0.035)      # 35 mm depth jump
    n = ab[..., 2:5]
    ndot = np.ones_like(zf)
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        sh = np.roll(np.roll(n, dy, 0), dx, 1)
        ndot = np.minimum(ndot, (n * sh).sum(-1))
    crease = solid & (ndot < math.cos(math.radians(62)))
    sil = solid & ~ndi.binary_erosion(solid, np.ones((3, 3)))
    # line_px is the line's TOTAL measured width. Dilating the one-pixel
    # boundary by that much grows it on BOTH sides, so the drawn line came out
    # twice the width it was measured at -- on a 7 px haft that inked a third
    # of the shaft and turned it near-black.
    k = max(1, int(round(line_px / 2.0)))
    edge = ndi.binary_dilation(sil, np.ones((k, k)))
    inner = ndi.binary_dilation(step | crease, np.ones((max(1, k // 2),) * 2))
    edge = (edge | inner) & solid
    col[edge] = (col[edge].astype(np.int16) * 0.30 + np.array([48, 33, 26]) * 0.70
                 ).astype(np.uint8)

    out = np.zeros((H, W, 4), np.uint8)
    out[..., :3] = col
    out[..., 3] = np.where(solid, 255, 0)
    flag = None
    if unseen is not None and solid.any():
        flag = np.zeros((H, W), bool)
        flag[solid] = unseen[tv[solid], tu[solid]]
    return out, solid, flag


def downsample(img, n):
    H, W = img.shape[:2]
    a = img.reshape(H // n, n, W // n, n, img.shape[2]).astype(np.float32)
    al = a[..., 3:4] / 255.0
    rgb = (a[..., :3] * al).sum(axis=(1, 3)) / np.maximum(al.sum(axis=(1, 3)), 1e-6)
    aa = al.mean(axis=(1, 3))[..., 0] * 255.0
    out = np.zeros((H // n, W // n, 4), np.uint8)
    out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(aa, 0, 255).astype(np.uint8)
    return out


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "walk"
    dirs = [sys.argv[2]] if len(sys.argv) > 2 else ["E"]
    fit, idx, A, tex, unseen = load()
    theta = fit["theta_elevation_deg"]
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    tri_v0 = A["tri_v"].astype(np.float64)
    tri_uv = A["tri_uv"].astype(np.float64)
    tri_id = A["tri_id"]
    names = [str(n) for n in A["names"]]
    part_bone = {n: idx["parts"][n]["bone"] for n in names}
    part_kind = {n: idx["parts"][n]["kind"] for n in names}
    Jr = kp.joints(p)

    lm = json.load(open(os.path.join(OUT, "line_weight.json"))) \
        if os.path.exists(os.path.join(OUT, "line_weight.json")) else {"line_px_per_1000H": 6.0}
    line_px = lm["line_px_per_1000H"] / 1000.0 * (BODY_PX * SS)

    W = H = FRAME * SS
    scale = PX_PER_M * SS
    tx = FRAME / 2 * SS
    # GROUND-LINE CALIBRATION, measured against the cells the game plays.
    # Putting the world origin at the game's sole line is not the same thing
    # as putting the FEET there: in a 19.77-degree view a ground point 0.45 m
    # forward projects 17 px lower, so the rendered sole landed 23 px under
    # the Grok cells' and the knight would have stood below the floor.
    grok_soles = []
    for st in ("walk", "run"):
        d_ = os.path.join(GROK_DIR, st, "E")
        if not os.path.isdir(d_):
            continue
        for f in sorted(os.listdir(d_)):
            if not f.endswith(".png"):
                continue
            a_ = np.asarray(Image.open(os.path.join(d_, f)).convert("RGBA"))[..., 3] > 8
            grok_soles.append(int(np.where(a_.any(axis=1))[0].max()))
    target_sole = float(np.mean(grok_soles)) if grok_soles else SOLE_Y
    ty = SOLE_Y * SS

    src_prefix = os.environ.get("K3D_ANIM", "anim")      # "anim" or "anim_fit"
    sprite_root = os.environ.get("K3D_SPRITEDIR", "sprites")
    if what == "rest":
        seq = [(Jr, {})]
        tag = "rest"
    else:
        z = np.load(os.path.join(OUT, "%s_%s.npz" % (src_prefix, what)),
                    allow_pickle=True)
        nm = [str(x) for x in z["names"]]
        rn = [str(x) for x in z["rot_names"]]
        seq = [({k: z["joints"][i][j] for j, k in enumerate(nm)},
                {k: z["rots"][i][j].astype(np.float64) for j, k in enumerate(rn)})
               for i in range(len(z["joints"]))]
        tag = what

    # Calibration over the WHOLE cycle, not one probe frame. Calibrating on a
    # single frame leaves the cycle 3-8 px off the game's ground line whenever
    # that frame is not at the cycle's own lowest sole, which it generally is
    # not; the sole line the eye reads is the lowest one over the loop.
    soles = []
    for Jp_, ov_ in seq:
        if what == "rest":
            tvp = tri_v0
        else:
            Tp = PS.bone_transforms(Jr, Jp_, ov_)
            tvp = PS.pose_tris(tri_v0, tri_id, names, part_bone, part_kind, Tp, p)
        bigp, _, _ = render_frame(tvp, tri_uv, tri_id, tex, AZI[dirs[0]], theta,
                                  scale, tx, ty, W, H, line_px)
        sm = downsample(bigp, SS)
        soles.append(float(np.where((sm[..., 3] > 8).any(axis=1))[0].max()))
    ty -= (float(np.max(soles)) - target_sole) * SS

    stats = []
    for d in dirs:
        outdir = os.path.join(OUT, sprite_root, tag, d)
        os.makedirs(outdir, exist_ok=True)
        for i, (Jp, ov) in enumerate(seq):
            if what == "rest":
                tv = tri_v0
            else:
                T = PS.bone_transforms(Jr, Jp, ov)
                tv = PS.pose_tris(tri_v0, tri_id, names, part_bone, part_kind, T, p)
            big, solid, flag = render_frame(tv, tri_uv, tri_id, tex, AZI[d], theta,
                                            scale, tx, ty, W, H, line_px, unseen)
            small = downsample(big, SS)
            Image.fromarray(small).save(os.path.join(outdir, "%s_%s_%02d.png" % (tag, d, i)))
            ys, xs = np.where(small[..., 3] > 8)
            stats.append(dict(dir=d, frame=i, top=int(ys.min()), sole=int(ys.max()),
                              h=int(ys.max() - ys.min() + 1),
                              cx=round(float(xs.mean()), 1),
                              unseen_px_visible=int(flag.sum()) if flag is not None else 0,
                              visible_px=int(solid.sum())))
            print("  %s %s %02d  top=%3d sole=%3d h=%3d  unseen %.1f %% of visible"
                  % (tag, d, i, stats[-1]["top"], stats[-1]["sole"], stats[-1]["h"],
                     100.0 * stats[-1]["unseen_px_visible"] / max(stats[-1]["visible_px"], 1)))
    rname = "render_%s%s.json" % (tag, "_fit" if src_prefix != "anim" else "")
    with open(os.path.join(OUT, rname), "w") as f:
        json.dump(dict(note="C-9 knight3d render into the game's sprite format.",
                       frame=FRAME, sole_y=SOLE_Y, px_per_m=PX_PER_M,
                       supersample=SS, theta=theta, azimuths=AZI,
                       grok_sole_target=round(target_sole, 2),
                       ground_calibration_px=round(ty / SS - SOLE_Y, 2),
                       line_px_at_render=round(line_px, 2), frames=stats), f, indent=1)
    print("wrote", os.path.join(OUT, sprite_root, tag))


if __name__ == "__main__":
    main()
