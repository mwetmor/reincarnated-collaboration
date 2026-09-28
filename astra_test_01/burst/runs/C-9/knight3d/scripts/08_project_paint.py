#!/usr/bin/env python3
"""C-9 knight3d step 3a: PROJECTION PAINT.

Puts the approved paintings on the body. Each still is projected from ITS OWN
fitted camera and ITS OWN fitted pose, because the eight stills disagree --
azimuth by -11.5 to +9.5 deg, figure scale by 8.1 % -- and projecting a still
through the average camera lands its paint on the wrong surface.

Per texel of the atlas:
  * posed world position and normal, per view (rigid pieces move by the exact
    rigid transform between the rest cloud and that view's posed cloud);
  * VISIBILITY by depth test against that view's own rendered depth buffer;
  * FACING weight max(0, n . c)^1.6 where c points toward the camera, zeroed
    below a grazing cutoff, so the view that sees a surface most squarely
    owns it;
  * the painted OUTLINE is stripped: ink-dark pixels that sit on a silhouette
    or an internal occlusion contour in THAT view are rejected, because those
    contours belong to that view only (verdict section 1, row 2). Interior
    hatching and plate lines are KEPT -- they are the painter's hand.

RP-E_a/_b (the tabard-off, far-leg-whole under-layers) are projected as two
extra E-camera sources at reduced weight, depth-tested against geometry with
the tabard removed, so they can reach what the tabard hides.

The POLLAXE is painted from the four CARDINAL views only. The diagonals do not
agree about where the haft is (work/pollaxe_consistency.json: rms 0.057 H),
and projecting a drifting haft onto a rigid mesh would smear it.

Writes out/knight_paint.png, out/paint_unseen.png, out/paint_owner.png
(which view owns each texel -- the blend seams are where that changes) and
out/paint_report.json.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knight_proxy as kp
from raster import raster, tri_normals, kabsch

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
WORK = os.path.join(K3, "work"); OUT = os.path.join(K3, "out")
MASKS = os.path.join(WORK, "masks")
SEEDS = os.path.join(ROOT, "artifacts", "seeds")
RPE = os.path.join(ROOT, "artifacts", "RP-E")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
CARDINALS = ["S", "E", "N", "W"]
SEED_FILE = {"N": "seed_N.png", "NE": "seed_NE.png", "E": "seed_E.png",
             "SE": "seed_SE.png", "S": "seed_S_v2.png", "SW": "seed_SW_v2.png",
             "W": "seed_W.png", "NW": "seed_NW.png"}
ATLAS = 2048
GRAZE = 0.18          # below this facing cosine a sample is too stretched to use
FACING_POW = 4.0   # sharp: the squarest view OWNS a surface. At 1.6 the
                   # diagonals blended their own (differently yawed) tabard
                   # art onto the same flat panel and the heraldry broke up.
DEPTH_EPS = 0.012     # metres


def view_basis(alpha, theta):
    r, u = kp.basis(alpha, theta)
    c = kp.cam_dir(alpha, theta)
    return r, u, c


def project_pts(P, alpha, theta, s, tx, ty):
    r, u, c = view_basis(alpha, theta)
    return np.stack([P @ r * s + tx, -(P @ u) * s + ty], -1), -(P @ c)


def ink_mask(rgb):
    """The register card's LINE: a crisp dark sepia-to-near-black pen line, the
    darkest mark in the image. Measured, not assumed: take the dark tail of the
    figure's own luminance."""
    lum = rgb.astype(np.float32) @ np.array([0.299, 0.587, 0.114])
    return lum, lum < 92.0


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta, ds = fit["theta_elevation_deg"], fit["downsample"]
    p0 = dict(kp.DEFAULTS); p0.update(fit["params"])
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    tri_v = A["tri_v"].astype(np.float64)
    tri_uv = A["tri_uv"].astype(np.float64)
    tri_id = A["tri_id"]
    names = [str(n) for n in A["names"]]
    NT = len(tri_v)
    print("atlas: %d triangles over %d pieces" % (NT, len(names)))

    # ---- 1. bake the atlas: which body point is each texel? ---------------
    uv_px = tri_uv * np.array([ATLAS, ATLAS])
    zdummy = np.zeros((NT, 3))
    _, tidx, _, bary = raster(uv_px, zdummy, None, ATLAS, ATLAS)
    valid = tidx >= 0
    print("atlas coverage %.1f %% of %d x %d" % (100.0 * valid.mean(), ATLAS, ATLAS))
    ty_, tx_ = np.where(valid)
    ti = tidx[valid]
    bw = bary[valid]                          # (M,3)

    # the piece each texel belongs to
    texel_piece = tri_id[ti]
    weapon_pieces = {i for i, n in enumerate(names)
                     if idx["parts"][n]["kind"] == "weapon"}
    tabard_pieces = {i for i, n in enumerate(names) if n.startswith("tabard")}
    is_weapon = np.isin(texel_piece, list(weapon_pieces))

    # ---- 2. per-view posed geometry ---------------------------------------
    rest_parts = {n: pts for n, _, pts in kp.build_parts(p0)}
    acc = np.zeros((len(ti), 3))
    accw = np.zeros(len(ti))
    best_w = np.zeros(len(ti))
    owner = np.full(len(ti), -1, np.int16)
    per_view_stats = {}

    sources = [(d, SEED_FILE[d], 1.0, False) for d in DIRS] + \
              [("E", "RP-E_a.png", 0.42, True), ("E", "RP-E_b.png", 0.42, True)]

    for si, (d, fname, wmul, is_rpe) in enumerate(sources):
        v = fit["pose_fitted"]["views"][d]
        pv = dict(p0)
        for k, dv in (v.get("delta") or {}).items():
            pv[k] = p0[k] + dv
        posed_parts = {n: pts for n, _, pts in kp.build_parts(pv)}

        # rigid transform per piece, recovered from the two point clouds
        V = tri_v.copy()
        for pid, nm in enumerate(names):
            base = nm
            if nm.startswith("pollaxe_"):
                base = None
            if base in rest_parts and base in posed_parts:
                R, t = kabsch(rest_parts[base], posed_parts[base])
                if np.abs(R - np.eye(3)).max() > 1e-9 or np.abs(t).max() > 1e-9:
                    sel = tri_id == pid
                    V[sel] = V[sel] @ R.T + t
        Nn = tri_normals(V)

        s = v["scale"] * ds; tx = v["tx"] * ds; ty = v["ty"] * ds
        img = Image.open(os.path.join(RPE if is_rpe else SEEDS, fname)).convert("RGB")
        W, H = img.size
        rgb = np.asarray(img)
        lum, ink = ink_mask(rgb)
        plate = (rgb[..., 1].astype(int) - np.maximum(rgb[..., 0], rgb[..., 2]) > 60) \
            & (rgb[..., 1] > 110)

        # TWO depth buffers, because the weapon and the body are painted from
        # different evidence. The body buffer excludes the weapon: the fitted
        # haft is NOT where the painted haft is (rms 0.057 H), so letting the
        # fitted haft occlude body texels would mask the wrong strip. Instead,
        # samples that land on the PAINTED haft are rejected using the matte
        # from 01, which is where the haft actually is.
        keep = np.ones(NT, bool)
        if is_rpe:
            keep &= ~np.isin(tri_id, list(tabard_pieces))
        keep &= ~np.isin(tri_id, list(weapon_pieces))
        xy, z = project_pts(V.reshape(-1, 3), v["alpha"], theta, s, tx, ty)
        xy = xy.reshape(NT, 3, 2); z = z.reshape(NT, 3)
        zbuf, ibuf, _, _ = raster(xy[keep], z[keep], None, W, H)
        wsel = np.isin(tri_id, list(weapon_pieces))
        wzbuf, _, _, _ = raster(xy[wsel], z[wsel], None, W, H)
        painted_axe = np.zeros((H, W), bool)
        axe_shift = (0.0, 0.0)
        if not is_rpe:
            painted_axe = np.load(os.path.join(MASKS, "%s_axe.npy" % d))
            # erode before sampling: the matte's own boundary pixels are
            # anti-aliased against the #00ff00 plate, and the row search was
            # landing on them and pulling plate green onto the haft.
            painted_axe = ndi.binary_erosion(painted_axe, np.ones((5, 5)))
            # align the fitted weapon to the PAINTED haft (a 2-D offset, per
            # view, measured -- the stills' haft does not follow the yaw)
            rmask = np.isfinite(wzbuf)
            if rmask.any() and painted_axe.any():
                ry, rx = np.where(rmask); py_, px_ = np.where(painted_axe)
                axe_shift = (float(px_.mean() - rx.mean()),
                             float(py_.mean() - ry.mean()))

        # contour zone: the silhouette, and internal occlusion edges
        filled = np.isfinite(zbuf)
        zf = np.where(filled, zbuf, 0.0)
        gz = np.hypot(ndi.sobel(zf, 0), ndi.sobel(zf, 1))
        contour = (~filled) | (gz > 0.035)
        contour = ndi.binary_dilation(contour, np.ones((9, 9)))
        reject = (ink & contour) | plate
        body_reject = reject | ndi.binary_dilation(painted_axe, np.ones((5, 5)))

        # sample per texel
        P = (bw[:, :, None] * V[ti]).sum(1)
        Nt = Nn[ti]
        pxy, pz = project_pts(P, v["alpha"], theta, s, tx, ty)
        _, _, c = view_basis(v["alpha"], theta)
        # c points from the subject TOWARD the camera, so a surface facing the
        # camera has N.c > 0. (This was written -(N.c) first, which selects
        # exactly the BACK faces: every sample was then depth-rejected by the
        # front of the same piece, and 96.5 % of the atlas came back "unseen".
        # The instrument said "unseen"; the defect was the sign.)
        face = Nt @ c
        # TWO pixel addresses per texel, because they answer different
        # questions. The DEPTH TEST must run at the texel's own projected
        # pixel (that is where the geometry is); the COLOUR LOOKUP may be
        # displaced, for weapon texels, onto the painted haft (that is where
        # the paint is). Doing both at the displaced pixel -- as this did at
        # first -- tests the depth of a place the weapon was never rendered,
        # so wzbuf is inf there and every weapon texel fails.
        gx = np.clip(np.round(pxy[:, 0]).astype(int), 0, W - 1)     # geometry
        gy = np.clip(np.round(pxy[:, 1]).astype(int), 0, H - 1)
        inside = (pxy[:, 0] >= 0) & (pxy[:, 0] < W) & \
                 (pxy[:, 1] >= 0) & (pxy[:, 1] < H)
        px, py = gx.copy(), gy.copy()                               # sampling
        body_ok = inside & (face > GRAZE) \
            & (np.abs(pz - zbuf[gy, gx]) < DEPTH_EPS) & ~body_reject[gy, gx]

        # The weapon: the fitted haft is NOT where the painted haft is (rms
        # 0.057 H), so slide each weapon texel along its own ROW to the
        # nearest painted-haft pixel -- the same height on the haft, a real
        # painted pixel, and the geometry test already passed where it stood.
        weap_ok = np.zeros(len(ti), bool)
        if (not is_rpe) and d in CARDINALS and painted_axe.any():
            plate_bad = plate | ndi.binary_dilation(plate, np.ones((3, 3)))
            sx = int(round(axe_shift[0])); sy = int(round(axe_shift[1]))
            near = np.abs(pz - wzbuf[gy, gx]) < DEPTH_EPS * 3
            cand = np.where(inside & (face > GRAZE) & near & is_weapon)[0]
            rowlist = [np.where(painted_axe[y])[0] for y in range(H)]
            for j in cand:
                yy = min(max(gy[j] + sy, 0), H - 1)
                rr = rowlist[yy]
                if len(rr) == 0:
                    continue
                want = gx[j] + sx
                k = rr[np.argmin(np.abs(rr - want))]
                if abs(int(k) - int(want)) <= 70 and not plate_bad[yy, k]:
                    px[j] = k; py[j] = yy
                    weap_ok[j] = True
        vis = np.where(is_weapon, weap_ok, body_ok & ~is_weapon)
        w = np.where(vis, np.maximum(face, 0.0) ** FACING_POW * wmul, 0.0)
        col = rgb[py, px].astype(np.float64)
        acc += w[:, None] * col
        accw += w
        better = w > best_w
        best_w[better] = w[better]
        owner[better] = si
        per_view_stats["%s:%s" % (d, fname)] = dict(
            texels_seen=int((w > 0).sum()),
            texels_owned=int((owner == si).sum()),
            rejected_outline_px=int((ink & contour).sum()),
            weapon_align_shift_px=[round(axe_shift[0], 1), round(axe_shift[1], 1)])
        print("  %-3s %-14s seen %6d texels" % (d, fname, int((w > 0).sum())))

    # ---- 3. the weapon, cardinals only ------------------------------------
    # (handled inside the loop by the is_weapon gate; the weapon's own depth
    # buffer is the weapon alone, since nothing on the body occludes a haft
    # held out in front)
    # ---- 4. resolve --------------------------------------------------------
    seen = accw > 1e-9
    col = np.zeros((len(ti), 3))
    col[seen] = acc[seen] / accw[seen, None]

    tex = np.zeros((ATLAS, ATLAS, 3), np.uint8)
    unseen = np.zeros((ATLAS, ATLAS), bool)
    cov = np.zeros((ATLAS, ATLAS), bool)
    own = np.zeros((ATLAS, ATLAS), np.int16) - 1
    tex[ty_, tx_] = np.clip(col, 0, 255).astype(np.uint8)
    cov[ty_, tx_] = True
    unseen[ty_[~seen], tx_[~seen]] = True
    own[ty_, tx_] = owner

    # Fill the unseen so a render shows no holes -- but they stay FLAGGED, and
    # the fill NEVER crosses from one piece to another. A global nearest-texel
    # fill pulled tabard blue onto plate and plate grey onto the tabard,
    # because UV islands of different pieces sit next to each other in the
    # atlas and "nearest in the atlas" is not "nearest on the body".
    pmap = np.full((ATLAS, ATLAS), -1, np.int16)
    pmap[ty_, tx_] = texel_piece
    for pid in range(len(names)):
        mine = pmap == pid
        if not mine.any():
            continue
        src = mine & ~unseen
        if not src.any():
            continue
        tofill = mine & unseen
        if not tofill.any():
            continue
        _, ind = ndi.distance_transform_edt(~src, return_indices=True)
        tex[tofill] = tex[ind[0][tofill], ind[1][tofill]]
    # bleed the texture a few px past every island so bilinear sampling at the
    # island edge does not pull in background
    for _ in range(4):
        grow = ndi.binary_dilation(cov, np.ones((3, 3))) & ~cov
        if not grow.any():
            break
        _, ind = ndi.distance_transform_edt(~cov, return_indices=True)
        tex[grow] = tex[ind[0][grow], ind[1][grow]]
        cov |= grow

    Image.fromarray(tex).save(os.path.join(OUT, "knight_paint.png"))
    Image.fromarray((unseen * 255).astype(np.uint8)).save(os.path.join(OUT, "paint_unseen.png"))
    pal = np.array([[220, 60, 60], [220, 140, 50], [230, 210, 60], [120, 200, 70],
                    [60, 190, 180], [70, 130, 220], [140, 90, 200], [220, 100, 180],
                    [150, 150, 150], [110, 110, 110]], np.uint8)
    om = np.zeros((ATLAS, ATLAS, 3), np.uint8)
    for i in range(len(sources)):
        om[own == i] = pal[i % len(pal)]
    Image.fromarray(om).save(os.path.join(OUT, "paint_owner.png"))

    # unseen, reported per piece -- these are the Astra touch-up candidates
    per_piece = {}
    for pid, nm in enumerate(names):
        m = texel_piece == pid
        if not m.any():
            continue
        per_piece[nm] = dict(texels=int(m.sum()),
                             unseen=int((~seen & m).sum()),
                             unseen_pct=round(100.0 * float((~seen & m).sum()) / int(m.sum()), 2))
    rep = dict(
        note="C-9 knight3d 3a: projection paint from the eight approved stills, "
             "each through its own fitted camera and pose, blended by facing.",
        atlas=ATLAS, triangles=NT,
        atlas_coverage_pct=round(100.0 * float(valid.mean()), 2),
        texels_total=int(len(ti)), texels_unseen=int((~seen).sum()),
        unseen_pct=round(100.0 * float((~seen).mean()), 2),
        graze_cutoff=GRAZE, facing_power=FACING_POW, depth_eps_m=DEPTH_EPS,
        sources=[dict(dir=d, file=f, weight=w, is_rpe=r) for d, f, w, r in sources],
        per_source=per_view_stats,
        per_piece_unseen=dict(sorted(per_piece.items(),
                                     key=lambda kv: -kv[1]["unseen_pct"])))
    with open(os.path.join(OUT, "paint_report.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("unseen %.2f %% of %d texels; wrote knight_paint.png" %
          (rep["unseen_pct"], len(ti)))
    for nm, v in list(rep["per_piece_unseen"].items())[:12]:
        print("   %-20s %5.1f %% unseen (%d/%d)" % (nm, v["unseen_pct"], v["unseen"], v["texels"]))


if __name__ == "__main__":
    main()
