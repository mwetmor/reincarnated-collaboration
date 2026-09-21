#!/usr/bin/env python3
"""mask_from_paint.py — THE BOUNDARY, DERIVED FROM A PASSED PAINTING.

Run KC2-PLAY, Wave 2 scene instruments. Author: drax (presentation seam), 2026-09-20.
Deterministic. numpy + scipy + PIL only. NO model calls, NO network, NO writes under
astra_test_01/ (every input there is opened read-only).

AUTHORITY
---------
KP-19 (Matt): ART LEADS THE BOUNDARY. The video-measured ring is a suggestion; the painting
places the structures; the playable boundary is DERIVED FROM THE PAINTING and the runtime
reads that mask. KP-20: each painting Matt passes is registered by SHA and the runtime loads
the boundary derived from THAT sha only — the sha IS the edge. The T-B grader refuses any
arena-sensitive row unless the telemetry header carries the mask's AREA + MAX CHORD, so both
are computed here and printed in mask_manifest.json.

METHOD — my P0-c clause-1 instrument (b1a_manifest.json :: mask_from_paint.instrument)
--------------------------------------------------------------------------------------
 1. Key the outside green WITH A TOLERANCE. Neither proof is exact #00FF00 (B1a 0.0001 %,
    B1d 0.0002 %), so the key is a BAND, measured not assumed: greenness
    g_dom = G - max(R, B); the keyed fraction is flat across g_dom in [40, 200] (B1a
    9.27 % -> 9.06 %; B1d 5.06 % -> 4.86 %), i.e. everything between the band edges is the
    anti-aliased fringe, ~0.2 pp wide. --green-dom sits in the middle of that plateau at 120
    and the derived boundary is insensitive to it. The plateau table is printed every run.
 2. Close then open at --morph-m, a radius in METRES (elliptical structuring element, since
    px/m differs by axis: 100.62 east, 80.31 south). Kills speckle without eating detail.
 3. Largest connected walkable component SEEDED AT THE GATE.
 4. Fill enclosed pockets.
 5. Pools: the suggested discs are read from the id mask (class #FF0000) and fitted in
    METRIC space by a Kasa circle fit on the boundary pixels that are NOT on the frame —
    an area-equivalent radius would be wrong here because the one suggested disc in this
    chunk is CLIPPED by the west frame edge, and an arc still determines a circle (fit
    residual is reported: on B1a's id mask it is 2.7 mm rms, and the same fit including the
    frame pixels is 0.66 m rms, which is why they are excluded).

    HOW I DECIDE WHETHER THE PAINTING MOVED A POOL — by OVERLAP, never by proximity.
    Molten hazard is keyed strictly (saturation >= --hazard-sat, R >= --hazard-r,
    G-B >= --hazard-gb, luminance >= --hazard-luma), closed at --hazard-close-m to join the
    filaments lava is drawn as into one field, and kept at >= --hazard-min-m2.
      - painted molten covers >= --hazard-frac of the disc's in-chunk area
            -> CONFIRMED BY PAINT; the disc is re-fitted to what the painter actually drew.
      - otherwise -> UNMOVED, the suggestion STANDS, flagged UNCONFIRMED_BY_PAINT.
    I do NOT relocate a hazard to the nearest fire I can find. A proximity rule did exactly
    that in the first cut of this script — it teleported the west pool 14 m onto a brazier —
    and inventing a hazard position is content synthesis, which is not mine to do. Every
    molten field that overlaps NO suggested disc is listed instead as
    `painted_hazards_claimed_by_no_suggested_pool`: data for the conductor and Matt.
 6. Emit walkable.json in the lane's exporter shape (runs/C-7/cliffside_v45/parallax/
    walkable.json: canvas_size / walkable / blocked / spawn / bounds / figure_height_px),
    plus a `pools` extension key — pools are damage FIELDS, not obstacles, so they must not
    ride in `blocked` where `is_walkable` would refuse them.

USAGE
  python3 mask_from_paint.py --painting <p.png> --label B1d --out <dir> \
      --id-mask <b1a_id_1536x1024.png> [flags]

OUTPUTS (under --out)
  walkable.json        exporter shape + pools
  boundary_overlay.png painting + derived boundary + pools drawn
  walkable_mask.png    the binary mask (feeds crack_check.py --floor-mask)
  mask_manifest.json   painting sha256, every parameter, area_m2, max_chord_m
"""

import argparse
import hashlib
import json
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

# --- plate law (frozen; drax b1a_manifest.json :: chunk) ------------------------------
PX_E = 100.617553710938
PX_S = 80.307624765
GATE_PX = (768.0, 798.72)
FIGURE_HEIGHT_PX = 115          # b1a_manifest :: scale_figure.height_px (115.1748), rounded
POOL_RGB = (255, 0, 0)          # id-mask pool class
LUMA = np.array([0.2126, 0.7152, 0.0722])


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ellipse(rx, ry):
    rx = max(1, int(round(rx))); ry = max(1, int(round(ry)))
    y, x = np.mgrid[-ry:ry + 1, -rx:rx + 1]
    return (x * x) / float(rx * rx) + (y * y) / float(ry * ry) <= 1.0


def moore_trace(mask):
    """Ordered outer contour (Moore-neighbour tracing, clockwise). Deterministic."""
    H, W = mask.shape
    ys, xs = np.nonzero(mask)
    i = int(np.argmin(ys.astype(np.int64) * W + xs))
    start = (int(ys[i]), int(xs[i]))
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    p = start
    b = (start[0], start[1] - 1)
    contour = [start]
    limit = 8 * (H + W) * 4 + 16 * mask.sum() ** 0.5
    while len(contour) < max(10000, limit):
        k = dirs.index((b[0] - p[0], b[1] - p[1]))
        moved = False
        for t in range(1, 9):
            d = dirs[(k + t) % 8]
            q = (p[0] + d[0], p[1] + d[1])
            if 0 <= q[0] < H and 0 <= q[1] < W and mask[q]:
                pb = dirs[(k + t - 1) % 8]
                b = (p[0] + pb[0], p[1] + pb[1])
                p = q
                moved = True
                break
        if not moved:
            break
        if p == start:
            break
        contour.append(p)
    return contour


def rdp(pts, eps):
    """Ramer-Douglas-Peucker on a list of (x, y). Iterative; pts in METRIC space."""
    if len(pts) < 3:
        return list(pts)
    keep = np.zeros(len(pts), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    P = np.asarray(pts, float)
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = P[i], P[j]
        ab = b - a
        n = np.hypot(*ab)
        seg = P[i + 1:j]
        if n < 1e-12:
            d = np.hypot(*(seg - a).T)
        else:
            d = np.abs(ab[0] * (a[1] - seg[:, 1]) - (a[0] - seg[:, 0]) * ab[1]) / n
        m = int(np.argmax(d))
        if d[m] > eps:
            keep[i + 1 + m] = True
            stack.append((i, i + 1 + m))
            stack.append((i + 1 + m, j))
    return [tuple(P[i]) for i in np.nonzero(keep)[0]]


def hull(pts):
    """Andrew monotone chain convex hull."""
    P = sorted(set(map(tuple, pts)))
    if len(P) < 3:
        return P

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def kasa_circle(xs_m, ys_m):
    """Least-squares circle fit (Kasa) in metric space. Works on an ARC, which matters:
    the one suggested pool disc in this chunk is clipped by the west frame edge.
    Returns (cx, cy, r, resid_rms, resid_max) — the residuals are how the caller knows
    whether the fit meant anything."""
    A = np.column_stack([xs_m, ys_m, np.ones_like(xs_m)])
    b = xs_m ** 2 + ys_m ** 2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx = float(sol[0] / 2.0)
    cy = float(sol[1] / 2.0)
    r = float(np.sqrt(max(sol[2] + cx * cx + cy * cy, 0.0)))
    res = np.hypot(xs_m - cx, ys_m - cy) - r
    return cx, cy, r, float(res.std()), float(np.abs(res).max())


def px2m(x, y):
    return ((x - GATE_PX[0]) / PX_E, (y - GATE_PX[1]) / PX_S)


def m2px(x, y):
    return (GATE_PX[0] + x * PX_E, GATE_PX[1] + y * PX_S)


def main():
    ap = argparse.ArgumentParser(description="derive the playable boundary from a passed painting (KP-19/KP-20)")
    ap.add_argument("--painting", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--id-mask", default=None, help="chunk id mask PNG (pool class #FF0000)")
    ap.add_argument("--green-dom", type=float, default=120.0,
                    help="green key band: keyed iff G - max(R,B) >= this. Middle of the "
                         "measured plateau; the run prints the plateau so the choice is checkable.")
    ap.add_argument("--morph-m", type=float, default=0.10,
                    help="close/open radius in METRES")
    ap.add_argument("--simplify-m", type=float, default=0.05,
                    help="RDP tolerance in METRES")
    ap.add_argument("--hazard-sat", type=float, default=0.65)
    ap.add_argument("--hazard-r", type=float, default=225.0)
    ap.add_argument("--hazard-gb", type=float, default=50.0)
    ap.add_argument("--hazard-luma", type=float, default=150.0)
    ap.add_argument("--hazard-close-m", type=float, default=0.15,
                    help="close the molten key at this radius: lava is painted as filaments, "
                         "and a field is what the player stands in")
    ap.add_argument("--hazard-min-m2", type=float, default=0.3)
    ap.add_argument("--hazard-frac", type=float, default=0.25,
                    help="fraction of a suggested disc's in-chunk area that painted molten "
                         "must cover for the painting to CONFIRM (and re-fit) that pool")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    img = Image.open(a.painting).convert("RGB")
    W, H = img.size
    rgb = np.array(img).astype(np.float64)
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    g_dom = G - np.maximum(R, B)

    # --- 1. the green key, measured -----------------------------------------------------
    plateau = {str(int(t)): round(float((g_dom >= t).mean()) * 100, 4)
               for t in (40, 60, 80, 100, 120, 150, 180, 200, 220)}
    exact = float(((R == 0) & (G == 255) & (B == 0)).mean()) * 100
    keyed = g_dom >= a.green_dom
    kp = keyed[np.nonzero(keyed)]
    band = {
        "rule": "keyed iff G - max(R,B) >= green_dom",
        "green_dom": a.green_dom,
        "exact_00ff00_pct": round(exact, 4),
        "keyed_pct": round(float(keyed.mean()) * 100, 4),
        "plateau_pct_by_threshold": plateau,
        "plateau_width_pp": round(plateau["40"] - plateau["200"], 4),
        "keyed_rgb_ranges": {
            "R": [int(R[keyed].min()), int(R[keyed].max())],
            "G": [int(G[keyed].min()), int(G[keyed].max())],
            "B": [int(B[keyed].min()), int(B[keyed].max())],
        } if keyed.any() else None,
    }
    print(f"[{a.label}] green key: exact #00FF00 {exact:.4f} %  |  keyed at g_dom>={a.green_dom:.0f}: "
          f"{100*keyed.mean():.3f} %  |  plateau {plateau['40']:.3f} % (40) -> {plateau['200']:.3f} % (200), "
          f"width {band['plateau_width_pp']:.3f} pp")

    # --- 2. morphology in metres --------------------------------------------------------
    se = ellipse(a.morph_m * PX_E, a.morph_m * PX_S)
    walk = ~keyed
    walk = ndi.binary_closing(walk, structure=se)
    walk = ndi.binary_opening(walk, structure=se)

    # --- 3. largest component seeded at the gate ----------------------------------------
    lab, n = ndi.label(walk)
    gx, gy = int(round(GATE_PX[0])), int(round(GATE_PX[1]))
    seed_lab = int(lab[gy, gx])
    seed_note = "gate pixel"
    if seed_lab == 0:
        ys, xs = np.nonzero(walk)
        d = (xs - gx) ** 2 + (ys - gy) ** 2
        i = int(np.argmin(d))
        seed_lab = int(lab[ys[i], xs[i]])
        seed_note = f"gate pixel not walkable; nearest walkable px ({int(xs[i])},{int(ys[i])})"
    sizes = ndi.sum(walk, lab, range(1, n + 1))
    comp = (lab == seed_lab)
    largest_lab = int(np.argmax(sizes)) + 1 if n else 0
    gate_is_largest = (seed_lab == largest_lab)

    # --- 4. fill enclosed pockets -------------------------------------------------------
    before = int(comp.sum())
    comp = ndi.binary_fill_holes(comp)
    pockets_px = int(comp.sum()) - before

    area_m2 = float(comp.sum()) / (PX_E * PX_S)

    # --- boundary polygon ---------------------------------------------------------------
    contour = moore_trace(comp)
    cm = [px2m(x + 0.5, y + 0.5) for (y, x) in contour]
    simp_m = rdp(cm, a.simplify_m)
    if simp_m[0] != simp_m[-1]:
        simp_m.append(simp_m[0])
    poly_px = [[round(v, 2) for v in m2px(x, y)] for (x, y) in simp_m]

    hm = hull(simp_m)
    max_chord_m = 0.0
    chord_pts = None
    for i in range(len(hm)):
        for j in range(i + 1, len(hm)):
            d = float(np.hypot(hm[i][0] - hm[j][0], hm[i][1] - hm[j][1]))
            if d > max_chord_m:
                max_chord_m, chord_pts = d, (hm[i], hm[j])

    # --- 5. pools -----------------------------------------------------------------------
    pools, hazard_blobs, unclaimed = [], [], []
    mx = rgb.max(2); mn = rgb.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1.0), 0.0)
    lum = rgb @ LUMA
    haz = ((sat >= a.hazard_sat) & (R >= a.hazard_r) &
           (G - B >= a.hazard_gb) & (lum >= a.hazard_luma))
    haz = ndi.binary_closing(haz, structure=ellipse(a.hazard_close_m * PX_E,
                                                    a.hazard_close_m * PX_S))
    hl, hn = ndi.label(haz, structure=np.ones((3, 3)))
    min_haz_px = a.hazard_min_m2 * PX_E * PX_S
    haz_fields = {}
    for i in range(1, hn + 1):
        m = (hl == i)
        if m.sum() < min_haz_px:
            continue
        ys, xs = np.nonzero(m)
        cx_m, cy_m = px2m(float(xs.mean()), float(ys.mean()))
        haz_fields[i] = m
        hazard_blobs.append({"id": int(i), "area_px": int(m.sum()),
                             "area_m2": round(float(m.sum()) / (PX_E * PX_S), 3),
                             "centroid_m": [round(float(cx_m), 3), round(float(cy_m), 3)],
                             "r_equiv_m": round(float(np.sqrt(m.sum() / np.pi / (PX_E * PX_S))), 3)})
    claimed = set()

    if a.id_mask:
        idm = np.array(Image.open(a.id_mask).convert("RGB"))
        pm = np.all(idm == np.array(POOL_RGB, dtype=idm.dtype), axis=2)
        plab, pn = ndi.label(pm)
        for i in range(1, pn + 1):
            m = (plab == i)
            in_chunk_px = int(m.sum())
            edge = m & ~ndi.binary_erosion(m)
            ys, xs = np.nonzero(edge)
            on_frame = (xs == 0) | (xs == W - 1) | (ys == 0) | (ys == H - 1)
            use = ~on_frame
            fit_pts = (xs[use], ys[use]) if use.sum() >= 12 else (xs, ys)
            fx, fy = px2m(fit_pts[0].astype(float), fit_pts[1].astype(float))
            cx_m, cy_m, r_m, rms, rmax = kasa_circle(fx, fy)
            clipped = bool(on_frame.any())

            # OVERLAP, not proximity. See the module docstring.
            ov_px = {j: int((mm & m).sum()) for j, mm in haz_fields.items()}
            ov_total = sum(ov_px.values())
            ov_frac = ov_total / float(in_chunk_px) if in_chunk_px else 0.0
            confirming = [j for j, v in ov_px.items() if v > 0]
            if ov_frac >= a.hazard_frac and confirming:
                union = np.zeros_like(m)
                for j in confirming:
                    union |= haz_fields[j]
                    claimed.add(j)
                ue = union & ~ndi.binary_erosion(union)
                uys, uxs = np.nonzero(ue)
                ufx, ufy = px2m(uxs.astype(float), uys.astype(float))
                cx_m, cy_m, r_m, rms, rmax = kasa_circle(ufx, ufy)
                decision = (f"CONFIRMED BY PAINT — painted molten covers {100*ov_frac:.1f} % "
                            f"(>= {a.hazard_frac:.0%}) of the suggested in-chunk area; "
                            f"re-fitted to painted fields {sorted(confirming)}")
            else:
                decision = (f"UNMOVED — suggestion stands. UNCONFIRMED_BY_PAINT: painted "
                            f"molten covers {100*ov_frac:.1f} % of the suggested in-chunk "
                            f"area (< {a.hazard_frac:.0%}). No position is invented.")
            ys2, xs2 = np.nonzero(m)
            pools.append({
                "id": f"pool_{i}",
                "centre_m": [round(cx_m, 3), round(cy_m, 3)], "r_m": round(r_m, 3),
                "centre_px": [round(float(v), 2) for v in m2px(cx_m, cy_m)],
                "rx_px": round(r_m * PX_E, 2), "ry_px": round(r_m * PX_S, 2),
                "fit": "Kasa least-squares circle on non-frame boundary px, metric space",
                "fit_resid_rms_m": round(rms, 4), "fit_resid_max_m": round(rmax, 4),
                "suggested_px_in_chunk": in_chunk_px,
                "suggested_m2_in_chunk": round(in_chunk_px / (PX_E * PX_S), 3),
                "in_chunk_extent_m": [round(float(px2m(xs2.min(), 0)[0]), 3),
                                      round(float(px2m(xs2.max(), 0)[0]), 3),
                                      round(float(px2m(0, ys2.min())[1]), 3),
                                      round(float(px2m(0, ys2.max())[1]), 3)],
                "clipped_by_frame": clipped,
                "painted_molten_overlap_frac": round(ov_frac, 4),
                "decision": decision,
            })
    for hb in hazard_blobs:
        if hb["id"] not in claimed:
            unclaimed.append(hb)

    # --- 6. emit ------------------------------------------------------------------------
    walkable_json = {
        "canvas_size": [W, H],
        "walkable": [poly_px],
        "blocked": [],
        "spawn": [round(GATE_PX[0], 2), round(GATE_PX[1], 2)],
        "bounds": [0, 0, W, H],
        "figure_height_px": FIGURE_HEIGHT_PX,
        "pools": [{"centre_px": p["centre_px"], "rx_px": p["rx_px"], "ry_px": p["ry_px"],
                   "centre_m": p["centre_m"], "r_m": p["r_m"], "id": p["id"]} for p in pools],
    }
    wp = os.path.join(a.out, "walkable.json")
    json.dump(walkable_json, open(wp, "w"), indent=1)

    Image.fromarray((comp * 255).astype(np.uint8)).save(os.path.join(a.out, "walkable_mask.png"))

    ov = img.copy()
    d = ImageDraw.Draw(ov, "RGBA")
    d.line([tuple(p) for p in poly_px], fill=(255, 0, 255, 255), width=5)
    for p in pools:
        cx, cy = p["centre_px"]
        d.ellipse([cx - p["rx_px"], cy - p["ry_px"], cx + p["rx_px"], cy + p["ry_px"]],
                  outline=(255, 64, 64, 255), width=5)
    for hb in unclaimed:
        cx, cy = m2px(*hb["centroid_m"])
        rr = hb["r_equiv_m"]
        d.ellipse([cx - rr * PX_E, cy - rr * PX_S, cx + rr * PX_E, cy + rr * PX_S],
                  outline=(255, 200, 0, 220), width=3)
    d.ellipse([GATE_PX[0] - 10, GATE_PX[1] - 10, GATE_PX[0] + 10, GATE_PX[1] + 10],
              fill=(0, 255, 255, 255))
    d.rectangle([6, 6, 1180, 118], fill=(0, 0, 0, 215))
    for i, line in enumerate([
        f"BOUNDARY DERIVED FROM THE PAINTING (KP-19)   {a.label}   sha {sha256(a.painting)[:16]}...",
        f"green key g_dom>={a.green_dom:.0f} ({100*keyed.mean():.2f} % keyed)   morph {a.morph_m} m   "
        f"simplify {a.simplify_m} m   pockets filled {pockets_px} px",
        f"AREA {area_m2:.2f} m2    MAX CHORD {max_chord_m:.2f} m    vertices {len(poly_px)}",
        "magenta = derived boundary   red = pool (suggested/derived)   yellow = painted hazard "
        "claimed by no suggested pool   cyan = gate",
    ]):
        d.text((14, 14 + i * 26), line, fill=(255, 255, 255, 255))
    op = os.path.join(a.out, "boundary_overlay.png")
    ov.save(op)

    manifest = {
        "generated": "2026-09-20",
        "author": "drax (presentation seam) — run KC2-PLAY W2 scene instruments",
        "authority": "KP-19 (art leads the boundary) + KP-20 (the sha IS the edge)",
        "label": a.label,
        "painting": os.path.abspath(a.painting),
        "painting_sha256": sha256(a.painting),
        "painting_bytes": os.path.getsize(a.painting),
        "painting_size_px": [W, H],
        "id_mask": os.path.abspath(a.id_mask) if a.id_mask else None,
        "id_mask_sha256": sha256(a.id_mask) if a.id_mask else None,
        "plate": {"px_per_m_east": PX_E, "px_per_m_south": PX_S, "gate_px": list(GATE_PX)},
        "green_key": band,
        "parameters": {
            "green_dom": a.green_dom, "morph_m": a.morph_m,
            "morph_se_px": [int(round(a.morph_m * PX_E)), int(round(a.morph_m * PX_S))],
            "simplify_m": a.simplify_m,
            "hazard_key": {"sat_min": a.hazard_sat, "R_min": a.hazard_r,
                           "G_minus_B_min": a.hazard_gb, "luma_min": a.hazard_luma,
                           "close_m": a.hazard_close_m, "min_m2": a.hazard_min_m2},
            "pool_confirm_overlap_frac": a.hazard_frac,
        },
        "component": {
            "seed": seed_note, "components_found": int(n),
            "gate_component_is_largest": bool(gate_is_largest),
            "pockets_filled_px": pockets_px,
            "walkable_px": int(comp.sum()),
            "walkable_fraction_of_frame": round(float(comp.sum()) / (W * H), 5),
        },
        "METRICS_FOR_THE_T_B_HEADER": {
            "area_m2": round(area_m2, 3),
            "max_chord_m": round(max_chord_m, 3),
            "max_chord_endpoints_m": [[round(v, 3) for v in chord_pts[0]],
                                      [round(v, 3) for v in chord_pts[1]]] if chord_pts else None,
            "boundary_vertices": len(poly_px),
        },
        "pools": pools,
        "painted_hazard_blobs": hazard_blobs,
        "painted_hazards_claimed_by_no_suggested_pool": unclaimed,
        "outputs": {
            "walkable.json": sha256(wp),
            "boundary_overlay.png": sha256(op),
            "walkable_mask.png": sha256(os.path.join(a.out, "walkable_mask.png")),
        },
        "caveats": [
            "The boundary is ONLY as tight as the painter's green. Clause 1 of the instrument "
            "asks for flat #00FF00 OUTSIDE the nave; in this proof the green covers the far "
            "background only, so every near structure the painter drew INSIDE the frame "
            "(piers, arcade, rubble talus, breach debris) falls inside the derived walkable "
            "region. The derived area is therefore an UPPER BOUND on the playable floor, not "
            "the playable floor. Tightening it needs either more green from the painter or a "
            "second declared key for painted structure.",
        ],
    }
    mp = os.path.join(a.out, "mask_manifest.json")
    json.dump(manifest, open(mp, "w"), indent=1)

    print(f"[{a.label}] components {n}, gate seed {'largest' if gate_is_largest else 'NOT largest'}, "
          f"pockets filled {pockets_px} px")
    print(f"[{a.label}] AREA {area_m2:.3f} m2   MAX CHORD {max_chord_m:.3f} m   "
          f"boundary vertices {len(poly_px)}   walkable {100*comp.sum()/(W*H):.2f} % of frame")
    for p in pools:
        print(f"[{a.label}] {p['id']}: centre {p['centre_m']} m  r {p['r_m']} m  "
              f"clipped={p['clipped_by_frame']}  {p['decision']}")
    if unclaimed:
        print(f"[{a.label}] painted hazards claimed by NO suggested pool: "
              f"{[(u['id'], u['centroid_m'], u['area_m2']) for u in unclaimed]}")
    print(f"  -> {wp}\n  -> {op}\n  -> {mp}")


if __name__ == "__main__":
    main()
