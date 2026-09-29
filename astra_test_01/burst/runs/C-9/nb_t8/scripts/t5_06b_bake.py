# C-9 T5 step 2, part two: bake painted sheets into the UV texture.
#
#   python3 scripts/06b_bake.py <surface.npz> <out.png>
#           --sheet <layout_name>:<painted.png> [--sheet ...] [--erode 2]
#
# Nothing here knows what a manticore is. A sheet is a layout of per-cell
# cameras plus the image painted over it; a body painted in separate armour
# pieces is more sheets, not more code.
#
# WEIGHT = texel density x facing^4. Facing alone cannot choose between two
# cameras pointed the same way, which is exactly the case that matters: a head
# close-up and a whole-body view see the face at the SAME angle, so facing
# would blend two independent paintings of it 50/50. Density -- screen pixels
# per texel -- is the thing that differs, and it is what "this camera saw the
# face better" actually means.
#
# THE MATTE IS THE RENDER'S OWN ALPHA, eroded. Astra's plate comes back lost
# often enough that segmenting the paint is not a dependency worth having, and
# the geometry already knows where the creature is. The erode also absorbs the
# ink line's own wander -- measured at 2-3 px, scattering in direction rather
# than agreeing, which is what a hand-drawn outline does.
#
# AVERAGING HAPPENS IN LINEAR LIGHT. The sheets are 8-bit sRGB; averaging those
# code values directly darkens every blend between two views, worst exactly
# where two cameras overlap at equal weight.
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
NPZ, OUT = a[0], a[1]
SHEETS = [a[i + 1] for i, v in enumerate(a) if v == "--sheet"]
ERODE = int(a[a.index("--erode") + 1]) if "--erode" in a else 2


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def l2s(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


S = np.load(NPZ)
SIZE = int(S["size"][0])
tex_tri, tex_pos, tex_nrm = S["tex_tri"], S["tex_pos"], S["tex_nrm"]
uv_area, V, TRI = S["uv_area"], S["V"], S["TRI"]
ON = tex_tri >= 0
print("surface %dx%d, %.2f%% of texels on the mesh, %d tris"
      % (SIZE, SIZE, 100 * ON.mean(), len(TRI)))

acc = np.zeros((SIZE, SIZE, 3), np.float64)
wsum = np.zeros((SIZE, SIZE), np.float64)
rep = {"erode_px": ERODE, "size": SIZE, "sheets": {}}
for spec in SHEETS:
    name, png = spec.split(":", 1)
    L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % name)))
    IMG = s2l(np.array(Image.open(png).convert("RGB"), np.float32) / 255.0)
    print("sheet %-4s %s" % (name, os.path.basename(png)))
    rep["sheets"][name] = {}
    for d, c in L["cells"].items():
        x0, y0, w, h = c["rect"]
        ppm = c.get("px_per_m", L["px_per_m"])
        right, up = np.array(c["screen_right"]), np.array(c["screen_up"])
        aim = np.array(c["aim"])
        if "view_dir" in c:
            vdir = np.array(c["view_dir"], float)
        else:
            el = np.radians(c.get("elevation_deg", L["elevation_deg"]))
            az = np.radians(c["azimuth_deg"])
            vdir = np.array([np.sin(az) * np.cos(el), np.cos(az) * np.cos(el),
                             np.sin(el)])
        al = np.array(Image.open(os.path.join(
            ROOT, "work", "_cells_%s" % name, "cell_%s.png" % d)
        ).convert("RGBA"))[:, :, 3] > 8
        mt = ndimage.binary_erosion(al, iterations=ERODE) if ERODE else al
        # SELF-TEST: does the stored camera reproduce its own render?
        #
        # NOT by comparing bounding boxes. That was the first version and it
        # failed on the first cell that was not whole-body -- a head close-up
        # crops the torso away by design, so the projected bbox of every vertex
        # spans far outside a cell whose alpha stops at its own edge, and it
        # reported 798 px of "error" against a camera that was correct. The
        # premise was wrong, not the camera.
        #
        # What IS true for every cell, cropped or not: on a closed mesh, any
        # vertex that projects INSIDE the cell must land on a lit pixel, since
        # the silhouette is the outline of all of them. Hit rate answers the
        # question for a close-up and a full view alike.
        sx = (V - aim) @ right * ppm + w / 2.0
        sy = h / 2.0 - (V - aim) @ up * ppm
        ix0, iy0 = np.round(sx).astype(int), np.round(sy).astype(int)
        ins = (ix0 >= 0) & (ix0 < w) & (iy0 >= 0) & (iy0 < h)
        alp = ndimage.binary_dilation(al, iterations=1)   # 1 px for rounding
        hit = float(alp[iy0[ins], ix0[ins]].mean()) if ins.any() else 0.0
        err = 1.0 - hit
        assert hit > 0.97, (
            "%s/%s: only %.2f%% of the %d vertices that project inside this "
            "cell land on the render's silhouette -- the stored camera does "
            "not reproduce its own render" % (name, d, 100 * hit, int(ins.sum())))
        vis = S["vis_%s_%s" % (name, d)]
        P2 = np.stack([(V[TRI[:, k]] - aim) @ right * ppm for k in range(3)], 1)
        Q2 = np.stack([h / 2.0 - (V[TRI[:, k]] - aim) @ up * ppm for k in range(3)], 1)
        scr = 0.5 * np.abs((P2[:, 1] - P2[:, 0]) * (Q2[:, 2] - Q2[:, 0]) -
                           (P2[:, 2] - P2[:, 0]) * (Q2[:, 1] - Q2[:, 0]))
        dens = scr / np.maximum(uv_area, 1e-9)
        good = ON & vis[np.maximum(tex_tri, 0)]
        yy, xx = np.where(good)
        pw, nn = tex_pos[yy, xx].astype(np.float64), tex_nrm[yy, xx].astype(np.float64)
        px = (pw - aim) @ right * ppm + w / 2.0
        py = h / 2.0 - (pw - aim) @ up * ppm
        ix, iy = np.round(px).astype(int), np.round(py).astype(int)
        ok = (ix >= 0) & (ix < w) & (iy >= 0) & (iy < h)
        ok &= mt[np.clip(iy, 0, h - 1), np.clip(ix, 0, w - 1)]
        f = nn @ vdir
        ok &= f > 0.05
        yy, xx, ix, iy = yy[ok], xx[ok], ix[ok], iy[ok]
        wg = (f[ok] ** 4) * dens[tex_tri[yy, xx]]
        col = IMG[y0 + iy, x0 + ix]
        np.add.at(acc, (yy, xx), col * wg[:, None])
        np.add.at(wsum, (yy, xx), wg)
        rep["sheets"][name][d] = dict(texels=int(ok.sum()), vertex_miss=round(float(err), 5),
                                      mean_density=round(float(dens[tex_tri[yy, xx]].mean()), 3))
        print("   %-9s %7d texels   density %8.3f px/texel   self-test %.3f%% "
              "of in-cell vertices on silhouette"
              % (d, ok.sum(), dens[tex_tri[yy, xx]].mean(), 100 * hit))

painted = wsum > 0
tex = np.zeros((SIZE, SIZE, 3), np.float32)
tex[painted] = (acc[painted] / wsum[painted][:, None]).astype(np.float32)
unseen = ON & ~painted
rep["unseen_pct"] = round(100 * float(unseen.sum()) / max(int(ON.sum()), 1), 4)
print("\nUNSEEN %.3f%% of on-mesh texels painted by no camera (%d of %d)"
      % (rep["unseen_pct"], int(unseen.sum()), int(ON.sum())))

# fill inside the texel's OWN UV island -- a connected component of the UV
# coverage, so no rig and no part list: the same operation for a manticore and
# for a barbarian's separate armour pieces. Filling across islands would drag a
# paw's colour onto a face that happens to sit beside it in the atlas.
lab, nlab = ndimage.label(ON, np.ones((3, 3), int))
print("  %d UV islands" % nlab)
# ONE distance transform, not 600 dilations. The iterative version rolled a
# 50 MB array four times per step for six hundred steps -- 120 GB of memory
# traffic to fill a few percent of texels. EDT with return_indices gives every
# bare texel its nearest painted texel in a single pass; the island label is
# then checked on the RESULT, so a texel whose nearest neighbour lies in
# another chart is left bare rather than being given a paw's colour for a face.
out = tex.copy()
tgt = ON & ~painted
_, (iy, ix) = ndimage.distance_transform_edt(~painted, return_indices=True)
src_ok = tgt & (lab[iy, ix] == lab) & (lab > 0)
out[src_ok] = tex[iy[src_ok], ix[src_ok]]
cur = painted | src_ok
filled = int(src_ok.sum())
bare = int((ON & ~cur).sum())
rep.update(islands=int(nlab), filled=int(filled), still_bare=bare,
           uv_coverage_pct=round(100 * float(ON.mean()), 3))
print("  filled %d texels inside their island, %d still bare" % (filled, bare))
# bleed a few px past the chart so bilinear sampling at seams finds colour
for _ in range(6):
    s = np.zeros((SIZE, SIZE, 3), np.float32); n = np.zeros((SIZE, SIZE), np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        sh, shm = np.roll(np.roll(out, dy, 0), dx, 1), np.roll(np.roll(cur, dy, 0), dx, 1)
        s[shm] += sh[shm]; n[shm] += 1
    g = (~cur) & (n > 0)
    out[g] = s[g] / n[g][:, None]
    cur |= g
Image.fromarray((l2s(out) * 255 + 0.5).astype(np.uint8)).transpose(
    Image.FLIP_TOP_BOTTOM).save(OUT)
# the painted mask travels with the texture: the A/B agreement check needs the
# true overlap, and "where did a camera actually put paint" is not recoverable
# from the finished texture once the fill has run
Image.fromarray((painted * 255).astype(np.uint8)).transpose(
    Image.FLIP_TOP_BOTTOM).save(OUT.replace(".png", "_mask.png"))
np.save(OUT.replace(".png", "_raw.npy"), tex.astype(np.float16))  # half: disk is tight and this is a scratch comparison array
np.save(OUT.replace(".png", "_wsum.npy"), wsum.astype(np.float32))
json.dump(rep, open(os.path.join(
    ROOT, "work", "bake_report_%s.json"
    % os.path.basename(OUT).replace(".png", "")), "w"), indent=1)
print("wrote %s" % OUT)
