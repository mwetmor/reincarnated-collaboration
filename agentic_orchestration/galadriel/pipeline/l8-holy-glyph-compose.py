#!/usr/bin/env python3
"""L8 HOLY glyph candidate composition.

Draws three HOLY glyph candidates to the measured Synty INTERFACE_Fantasy_Warrior_HUD
style contract (see agentic_orchestration/galadriel/notes/2026-07-28-l8-holy-glyph-candidates.md
section 2), and emits _Clean / _Stroke / _Underlay layers for each plus a dark-composited
contact sheet alongside the five ruled glyphs.

All geometry is drawn at 4x supersample then box-downsampled, matching the pack's
anti-aliased vector-export edge quality. Rings are faceted polygons (12-14 gon), never
circles, per pack DNA.

Run:  python3 agentic_orchestration/galadriel/pipeline/l8-holy-glyph-compose.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = "/Users/admin/Games/reincarnated-collaboration"
PACK = os.path.join(
    ROOT,
    "matt_notes_handoff_docs/recent-synty-packs/INTERFACE_Fantasy_Warrior_HUD/Source_Sprites/Sprites",
)
OUT = os.path.join(ROOT, "agentic_orchestration/galadriel/captures/2026-07-28-l8-holy-glyph")
CAND = os.path.join(OUT, "candidates")
WORK = os.path.join(OUT, "work")

SIZE = 256
SS = 4  # supersample factor
C = SIZE * SS / 2.0  # supersampled centre
DARK = (35, 35, 45)


# ---------------------------------------------------------------- geometry helpers


def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def faceted_ring(d, cx, cy, r_out, r_in, sides=12, phase=0.0):
    """Faceted annulus: outer n-gon minus inner n-gon. Pack DNA is polygonal, not round."""
    outer = [pol(cx, cy, r_out, phase + 360.0 * i / sides) for i in range(sides)]
    inner = [pol(cx, cy, r_in, phase + 360.0 * i / sides) for i in range(sides)]
    d.polygon(outer, fill=255)
    d.polygon(inner, fill=0)


def taper_ray(d, cx, cy, deg, r0, r1, w0, w1, fill=255):
    """Tapered radial ray: quad from (r0,w0) to (r1,w1) along `deg` from centre."""
    a = math.radians(deg)
    ux, uy = math.sin(a), -math.cos(a)
    px, py = uy, -ux  # perpendicular
    pts = [
        (cx + ux * r0 - px * w0 / 2, cy + uy * r0 - py * w0 / 2),
        (cx + ux * r0 + px * w0 / 2, cy + uy * r0 + py * w0 / 2),
        (cx + ux * r1 + px * w1 / 2, cy + uy * r1 + py * w1 / 2),
        (cx + ux * r1 - px * w1 / 2, cy + uy * r1 - py * w1 / 2),
    ]
    d.polygon(pts, fill=fill)


def new_canvas():
    img = Image.new("L", (SIZE * SS, SIZE * SS), 0)
    return img, ImageDraw.Draw(img)


def finish(mask):
    """Downsample the supersampled alpha mask into a white-on-transparent RGBA icon."""
    a = mask.resize((SIZE, SIZE), Image.LANCZOS)
    rgba = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    rgba.putalpha(a)
    return rgba


# ---------------------------------------------------------------- candidates


def candidate_a():
    """H-A 'Radiant Disc'.

    Lineage: outer sunburst geometry of Icons_Status/..._Fortified01 (the only bold-weight
    radiant form in the pack) + the sun-ring proportions of FantasyWarrior/Tracery_Circle04
    (thin gold line-art, redrawn at glyph weight). Rays are DETACHED from the ring by a
    negative-space gap -- the gap is Cold01/Air02 DNA and is what separates this from
    Fortified01 (whose burst is one connected solid star).
    """
    img, d = new_canvas()
    s = SS
    faceted_ring(d, C, C, 64 * s, 38 * s, sides=12, phase=15.0)
    for i in range(8):
        deg = 45.0 * i
        taper_ray(d, C, C, deg, 76 * s, 104 * s, 34 * s, 8 * s)
    return img


def candidate_b():
    """H-B 'Ascendant Halo'.

    Lineage: a faceted open halo (Cursed02's angular-hexagon ring logic, flattened to a
    perspective lozenge) over three light shafts abstracted from
    FX/SPR_FX_FantasyWarrior_Beams01 (soft shaft plate -> flat chunky silhouette).
    Shafts FLARE downward from the halo (narrow at the ring, wide and flat-cut at the
    bottom) so the mark reads as grace descending, and so they cannot be mistaken for
    Element_Earth02's upward leaf-blade cluster.
    """
    img, d = new_canvas()
    s = SS

    # halo: faceted lozenge ring, 14-gon squashed vertically
    cx, cy = C, 58 * s
    rx_o, ry_o, rx_i, ry_i = 66 * s, 30 * s, 45 * s, 12 * s
    sides = 14
    outer = [
        (cx + rx_o * math.sin(math.radians(360.0 * i / sides + 12.86)),
         cy - ry_o * math.cos(math.radians(360.0 * i / sides + 12.86)))
        for i in range(sides)
    ]
    inner = [
        (cx + rx_i * math.sin(math.radians(360.0 * i / sides + 12.86)),
         cy - ry_i * math.cos(math.radians(360.0 * i / sides + 12.86)))
        for i in range(sides)
    ]
    d.polygon(outer, fill=255)
    d.polygon(inner, fill=0)

    # five descending shafts, ragged/staggered bottoms and uneven widths, per Beams01's
    # irregular shaft plate. Staggering is what keeps this off a solid flaring cone.
    y_top = 108 * s
    #        dx_top dx_bot w_top w_bot y_bot
    shafts = [
        (0, 0, 24, 32, 232),
        (-36, -50, 15, 20, 206),
        (36, 50, 15, 20, 214),
        (-64, -86, 11, 15, 178),
        (64, 86, 11, 15, 168),
    ]
    for dx_top, dx_bot, w_top, w_bot, y_b in shafts:
        xt, xb = C + dx_top * s, C + dx_bot * s
        y_bot = y_b * s
        d.polygon(
            [
                (xt - w_top * s / 2, y_top),
                (xt + w_top * s / 2, y_top),
                (xb + w_bot * s / 2, y_bot),
                (xb - w_bot * s / 2, y_bot),
            ],
            fill=255,
        )
    return img


def candidate_c():
    """H-C 'Dawn Rise'.

    Lineage: FX/SPR_FX_FantasyWarrior_HalfCircle01 (the arc plate) resolved into a solid
    faceted dome, fanned with FX/Beams01-derived tapered shafts. Asymmetric-vertical
    silhouette family, same as Attack01 and Down01. No closed ring anywhere -- deliberately
    the furthest of the three from the consecrate ritual-circle.
    """
    img, d = new_canvas()
    s = SS
    cx, cy = C, 214 * s
    r_dome = 58 * s

    # faceted dome (upper half of a 14-gon), sat on a flat base
    pts = []
    n = 14
    for i in range(n + 1):
        a = math.radians(-90 + 180.0 * i / n)
        pts.append((cx + r_dome * math.cos(a), cy + r_dome * math.sin(a) * 1.0))
    pts += [(cx + r_dome, cy), (cx - r_dome, cy)]
    d.polygon(pts, fill=255)

    # fanned tapered shafts
    fan = [(0, 172), (-28, 158), (28, 158), (-56, 126), (56, 126), (-80, 105), (80, 105)]
    for deg, reach in fan:
        taper_ray(d, cx, cy, deg, (r_dome / s + 14) * s, reach * s, 32 * s, 9 * s)
    return img


# ---------------------------------------------------------------- layer synthesis


def make_layers(clean):
    """Emit (_Clean, _Stroke, _Underlay) matching the pack's three-layer convention.

    Measured off Cold01: Stroke = silhouette + dilated dark-grey sticker halo (bbox grows
    194x222 -> 222x252, i.e. ~14px dilation); Underlay = silhouette + soft offset shadow
    (bbox -> 206x234, offset ~ +6,+5).
    """
    a = np.array(clean.getchannel("A"))

    # Stroke: round-dilate alpha by ~13px (blur+low threshold gives an isotropic dilation,
    # unlike a square MaxFilter kernel which boxes the corners), tint dark, clean on top.
    halo = Image.fromarray(a).filter(ImageFilter.GaussianBlur(9))
    halo = halo.point(lambda v: 255 if v > 34 else 0)
    halo = halo.filter(ImageFilter.GaussianBlur(1.1))
    stroke = Image.new("RGBA", clean.size, (0, 0, 0, 0))
    tint = Image.new("RGBA", clean.size, (58, 58, 58, 255))  # sampled off Cold01_Stroke halo
    tint.putalpha(halo)
    stroke = Image.alpha_composite(stroke, tint)
    stroke = Image.alpha_composite(stroke, clean)

    # Underlay: soft offset shadow
    sh = Image.fromarray(a).filter(ImageFilter.GaussianBlur(5))
    sh = sh.point(lambda v: int(v * 0.62))  # Cold01_Underlay shadow alpha p50 ~64
    shifted = Image.new("L", clean.size, 0)
    shifted.paste(sh, (6, 5))
    under = Image.new("RGBA", clean.size, (0, 0, 0, 0))
    st = Image.new("RGBA", clean.size, (10, 11, 13, 255))  # sampled off Cold01_Underlay
    st.putalpha(shifted)
    under = Image.alpha_composite(under, st)
    under = Image.alpha_composite(under, clean)
    return clean, stroke, under


def metrics(clean):
    a = np.array(clean.getchannel("A"))
    m = a > 128
    ys, xs = np.nonzero(m)
    from scipy import ndimage

    dt = ndimage.distance_transform_edt(m)
    return {
        "coverage_pct": round(float(m.mean()) * 100, 1),
        "bbox_w": int(xs.max() - xs.min() + 1),
        "bbox_h": int(ys.max() - ys.min() + 1),
        "dt_p50": round(float(np.percentile(dt[m], 50)), 1),
        "dt_p90": round(float(np.percentile(dt[m], 90)), 1),
    }


# ---------------------------------------------------------------- contact sheet

RULED = [
    ("freeze", "Icons_Status/ICON_FantasyWarrior_Status_Cold01_Clean.png"),
    ("physical", "Icons_Status/ICON_FantasyWarrior_Status_Attack01_Clean.png"),
    ("consecrate", "FX/SPR_FX_FantasyWarrior_RitualCircle01.png"),
    ("knockback", "Icons_Status/ICON_FantasyWarrior_Status_Down01_Clean.png"),
    ("shadow", "Icons_Status/ICON_FantasyWarrior_Status_Cursed02_Clean.png"),
    ("air", "Icons_Elements/ICON_FantasyWarrior_Element_Air02_Clean.png"),
]


def font(sz):
    for p in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def contact_sheet(cands, path):
    """Row 1: the five ruled + consecrate. Row 2: HOLY candidates. Row 3: 32px legibility strip."""
    CELL, PAD, LBL = 150, 12, 20
    cols = 6
    W = PAD + cols * (CELL + PAD)
    H = PAD + 2 * (CELL + LBL + PAD) + (48 + LBL + PAD) + 30
    sheet = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(sheet)
    f = font(13)
    fh = font(15)

    d.text((PAD, PAD - 2), "RULED FIVE (+consecrate)  —  the family HOLY must sit in",
           fill=(150, 190, 230), font=fh)
    y = PAD + 20
    for i, (name, rel) in enumerate(RULED):
        x = PAD + i * (CELL + PAD)
        im = Image.open(os.path.join(PACK, rel)).convert("RGBA")
        im.thumbnail((CELL, CELL), Image.LANCZOS)
        sheet.paste(im, (x + (CELL - im.width) // 2, y + (CELL - im.height) // 2), im)
        d.text((x, y + CELL + 3), name, fill=(190, 190, 200), font=f)

    y2 = y + CELL + LBL + PAD
    d.text((PAD, y2 - 2), "HOLY CANDIDATES  —  Matt rules", fill=(230, 200, 130), font=fh)
    y2 += 20
    for i, (name, clean, _) in enumerate(cands):
        x = PAD + i * (CELL + PAD)
        im = clean.copy()
        im.thumbnail((CELL, CELL), Image.LANCZOS)
        sheet.paste(im, (x + (CELL - im.width) // 2, y2 + (CELL - im.height) // 2), im)
        d.text((x, y2 + CELL + 3), name, fill=(230, 200, 130), font=f)

    y3 = y2 + CELL + LBL + PAD
    d.text((PAD, y3 - 2), "32 px LEGIBILITY STRIP  —  ruled five then candidates",
           fill=(150, 190, 230), font=fh)
    y3 += 22
    x = PAD
    for name, rel in RULED:
        im = Image.open(os.path.join(PACK, rel)).convert("RGBA").resize((32, 32), Image.LANCZOS)
        sheet.paste(im, (x, y3), im)
        x += 44
    x += 40
    for name, clean, _ in cands:
        im = clean.resize((32, 32), Image.LANCZOS)
        sheet.paste(im, (x, y3), im)
        x += 44
    sheet.save(path)
    return path


def main():
    for p in (CAND, WORK):
        os.makedirs(p, exist_ok=True)

    builds = [
        ("H-A_radiant-disc", candidate_a),
        ("H-B_ascendant-halo", candidate_b),
        ("H-C_dawn-rise", candidate_c),
    ]
    cands = []
    for name, fn in builds:
        clean = finish(fn())
        cl, st, un = make_layers(clean)
        base = os.path.join(CAND, f"ICON_Holy_{name}")
        cl.save(base + "_Clean.png")
        st.save(base + "_Stroke.png")
        un.save(base + "_Underlay.png")
        print(name, metrics(clean))
        cands.append((name, clean, st))

    print(contact_sheet(cands, os.path.join(OUT, "contact_sheet.png")))


if __name__ == "__main__":
    main()
