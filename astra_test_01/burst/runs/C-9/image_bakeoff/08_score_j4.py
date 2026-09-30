#!/usr/bin/env python3
"""C-9 image bake-off, JOB 4: blockout paint-over -- does the painting keep every shape?

    python3 08_score_j4.py

The prompt asks for one thing above all: "Keep EVERY shape exactly where it is and the same
size, so the painting lines up with IMAGE 1 when overlaid." So the score is about the GUIDE's
shapes, one by one, against the painting's edges -- not about how pretty the painting is.

SHAPES are cut from the guide itself (IBO-J4-2_1_canvas.png, the ring-centre chunk). It is a
lit greybox render: 92.7% flat ground (200,192,184), about 2% soft blue-violet GROUND shadow,
and the objects -- grey stone faces, dark ink outlines, and blue-grey SHADOWED faces inside
the stones. The two blues share a hue; they differ in TEXTURE: a shadow cast on the snow is a
smooth wash, a stone's shadowed face is hatched. So: object = not ground AND not (bluish and
smooth), closed and hole-filled, components of 150 px or more. The small figure is found as
the component nearest the arena centre (0, 1) m and is scored the other way round.

    boundary_recall  per shape: the share of its outline with a painted edge within 4 px
                     (edges = the painting's top 12% of gradient magnitude, per image, so a
                     softer or harder hand is not penalised for its contrast)
    chamfer_px       per shape: mean distance from its outline to the nearest painted edge,
                     capped at 25
    kept             boundary_recall >= 0.5
    figure_out       the figure's region (dilated 6 px) carries no more than 2x the edge
                     density of the painting's own open snow -- i.e. it was painted OUT
    arena_clutter    painted-edge density over the guide's OPEN ground inside the arena disc
                     (r 7 m about (0, 1) m) -- "keep the open ground inside the ring clear"
    best_shift       the integer shift (+-12 px) that maximises mean boundary recall; a large
                     one means the painting slid, which "lines up when overlaid" forbids
"""
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
C9 = HERE.parent
GUIDE = C9 / "artifacts/CS9-guides/IBO-J4-2_1_canvas.png"
PAINTS = {"astra_a": C9 / "artifacts/IBO-J4/IBO-J4_a.png", "astra_b": C9 / "artifacts/IBO-J4/IBO-J4_b.png",
          "nb_a": HERE / "out/J4_nb_a.png", "nb_b": HERE / "out/J4_nb_b.png",
          "nbp_a": HERE / "out/J4_nbp_a.png", "nbp_b": HERE / "out/J4_nbp_b.png"}
# ground (u, v) -> chunk 2_1 pixels: x = (u + 28.715) * 100.6176 - 2560, y = (17.7203 - v) * 80.3076 - 768
def uv2px(u, v):
    return (u + 28.715) * 100.6176 - 2560, (17.7203 - v) * 80.3076 - 768


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def shapes(g):
    """Objects = clusters of the render's INK. Every object in the greybox carries a dark ink
    outline and a cast shadow carries none, so the ink IS the set of edges the painting has to
    keep -- and the shadows, which the prompt asks to be painted 'short and soft', are not
    shapes to be matched. The first version segmented by colour; a shadow's soft rim survived
    the smooth-blue test and hole-filling pulled every stone's shadow into its outline, which
    would have charged a painter for doing what the prompt asked."""
    g = g.astype(np.float32)
    ink = g.mean(-1) < 70
    # disk(6), not disk(2): at 2 px a stone's outline and its own shade hatching fell into
    # separate clusters (11 "shapes" that were 7 objects, fragments of 48-93 ink px), and a
    # fragment's recall is noise
    lab, n = ndimage.label(ndimage.binary_dilation(ink, disk(6)))
    keep = []
    for i in range(1, n + 1):
        if (ink & (lab == i)).sum() >= 40:
            keep.append(i)
    ground = np.abs(g - np.array([200, 192, 184])).max(-1) <= 18
    return lab, keep, ground, ink


def edges(rgb, pct=92):
    """THIN, STRONG edges: non-maximum suppression along the gradient, then the top 8% of
    gradient magnitude. The first version kept the top 12% un-thinned and dilated it 4 px, and
    in a textured painting that covers almost the whole frame -- Astra scored 1.000 recall,
    which was the texture, not the registration. Thin edges at 2 px tolerance, with a chance
    baseline beside them, can tell the two apart."""
    L = ndimage.gaussian_filter(rgb.astype(np.float32).mean(-1), 1.2)
    gx, gy = ndimage.sobel(L, 1), ndimage.sobel(L, 0)
    gm = np.hypot(gx, gy)
    ang = (np.rad2deg(np.arctan2(gy, gx)) + 180) % 180
    q = ((ang + 22.5) // 45).astype(int) % 4          # 0: horizontal grad, 1: 45, 2: 90, 3: 135
    offs = {0: (0, 1), 1: (-1, 1), 2: (1, 0), 3: (1, 1)}
    nms = np.zeros_like(gm, bool)
    for k, (dy, dx) in offs.items():
        a = np.roll(np.roll(gm, dy, 0), dx, 1)
        b = np.roll(np.roll(gm, -dy, 0), -dx, 1)
        nms |= (q == k) & (gm >= a) & (gm >= b)
    return nms & (gm > np.percentile(gm, pct))


def main() -> None:
    g = np.asarray(Image.open(GUIDE).convert("RGB"))
    H, W = g.shape[:2]
    lab, keep, ground, ink = shapes(g)
    fx, fy = uv2px(0.0, 1.0)
    cents = {i: ndimage.center_of_mass(lab == i) for i in keep}
    fig_id = min(keep, key=lambda i: np.hypot(cents[i][1] - fx, cents[i][0] - fy))
    shp = [i for i in keep if i != fig_id]
    bnd = {i: (lab == i) & ink for i in shp}                  # the outline IS the ink
    figm = ndimage.binary_fill_holes(ndimage.binary_dilation(lab == fig_id, disk(8)))
    yy, xx = np.mgrid[0:H, 0:W]
    ax, ay = uv2px(0.0, 1.0)
    arena = (((xx - ax) / (7 * 100.6176)) ** 2 + ((yy - ay) / (7 * 80.3076)) ** 2) <= 1
    open_ar = arena & ground & ~figm
    ov = g.copy()
    for i in shp:
        ov[bnd[i]] = [255, 0, 0]
    ov[figm & ~ndimage.binary_erosion(figm, disk(2))] = [0, 160, 255]
    Image.fromarray(ov).save(HERE / "j4_shapes_debug.png")
    info = {"shapes": len(shp), "figure_component": int(fig_id),
            "shape_ink_px": {int(i): int(bnd[i].sum()) for i in shp},
            "shape_centres": {int(i): [round(float(cents[i][1])), round(float(cents[i][0]))] for i in shp}}
    print("guide: %d shapes + the figure (component %d)" % (len(shp), fig_id))
    rep = {"_guide": info}
    for name, p in PAINTS.items():
        rp = np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS))
        E = edges(rp)
        best = (-1, 0, 0)
        for dy in range(-12, 13, 3):
            for dx in range(-12, 13, 3):
                Es = np.roll(np.roll(E, dy, 0), dx, 1)
                Ed = ndimage.binary_dilation(Es, disk(2))
                rec = np.mean([Ed[bnd[i]].mean() for i in shp])
                if rec > best[0]:
                    best = (rec, dy, dx)
        Ed = ndimage.binary_dilation(E, disk(2))
        dist = ndimage.distance_transform_edt(~E)
        per = {}
        for i in shp:
            r_ = float(Ed[bnd[i]].mean())
            # CHANCE: the same outline moved 60 px left and 20 up -- into lit open snow, since
            # the sun is upper-left and every shadow falls the other way -- scored the same way.
            # What a painting's texture gives any outline for free.
            sb = np.roll(np.roll(bnd[i], -20, 0), -60, 1)
            ch = float(Ed[sb].mean()) if sb.any() else 0.0
            per[int(i)] = {"recall": round(r_, 3), "chance": round(ch, 3), "lift": round(r_ - ch, 3),
                           "chamfer_px": round(float(np.minimum(dist[bnd[i]], 25).mean()), 2),
                           "kept": (r_ >= 0.40) and (r_ - ch >= 0.20)}
        # INVENTED CONTENT. The guide says most of this chunk is open snow; the prompt says
        # keep the open ground clear. Edge density cannot see a tarn or a path -- they are big
        # and smooth -- so the question is asked in colour: over the guide's OPEN GROUND (not
        # objects, not shadows, not the figure), what share of the painting is NOT snow?
        # Snow = light and unsaturated, or a pale blue-violet snow shadow. The first J4 pass
        # scored Pro 6/6 on shapes while it had painted a tarn, a path, a mound and cairns
        # across the arena -- the stones were kept and everything around them was not.
        rph = np.asarray(Image.fromarray(rp).convert("HSV")).astype(np.float32)
        Lp, Sp, Hp = rp.astype(np.float32).mean(-1), rph[..., 1] / 255, rph[..., 0] * 360 / 255
        snowp = ((Lp > 165) & (Sp < 0.20)) | ((Lp > 120) & (Hp > 190) & (Hp < 280) & (Sp < 0.35))
        gshadow = (g[..., 2].astype(np.float32) - (g[..., 0].astype(np.float32) + g[..., 1]) / 2 > 5)
        openg = ground & ~gshadow & ~figm & ~ndimage.binary_dilation(np.isin(lab, keep), disk(10))
        invented = float((~snowp)[openg].mean())
        invented_arena = float((~snowp)[openg & arena].mean())
        open_snow = ground & ~arena & ~figm
        dens_snow = float(E[open_snow].mean()) if open_snow.any() else float(E[ground].mean())
        dens_fig = float(E[figm].mean())
        rep[name] = {"size": list(Image.open(p).size),
                     "shapes_kept": sum(v["kept"] for v in per.values()), "shapes_total": len(per),
                     "mean_recall": round(float(np.mean([v["recall"] for v in per.values()])), 3),
                     "mean_chance": round(float(np.mean([v["chance"] for v in per.values()])), 3),
                     "mean_chamfer_px": round(float(np.mean([v["chamfer_px"] for v in per.values()])), 2),
                     "figure_edge_density": round(dens_fig, 3), "open_snow_edge_density": round(dens_snow, 3),
                     "figure_out": bool(dens_fig <= 2 * max(dens_snow, 1e-3)),
                     "arena_clutter": round(float(E[open_ar].mean()), 3),
                     "open_ground_not_snow": round(invented, 3),
                     "arena_open_ground_not_snow": round(invented_arena, 3),
                     "best_shift_px": [best[1], best[2]], "recall_at_best_shift": round(best[0], 3),
                     "per_shape": per}
        r = rep[name]
        print("%-8s kept %d/%d  recall %.3f (chance %.3f)  chamfer %.1f px | figure out %s | open ground NOT snow %.3f (arena %.3f) | best shift %s -> %.3f | %s"
              % (name, r["shapes_kept"], r["shapes_total"], r["mean_recall"], r["mean_chance"], r["mean_chamfer_px"],
                 r["figure_out"], invented, invented_arena, r["best_shift_px"],
                 r["recall_at_best_shift"], r["size"]))
    (HERE / "score_j4.json").write_text(json.dumps(rep, indent=1) + "\n")


if __name__ == "__main__":
    main()
