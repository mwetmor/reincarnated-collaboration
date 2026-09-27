#!/usr/bin/env python3
"""C-9 probe R-C9-34: a 2D PUPPET RIG of the East-facing knight, cut from the painted
still, as an alternative to the Grok-generated E walk/idle cells.

WHY A RIG.  Every generative repaint of this knight -- image edits, then the Grok video
clips -- eroded the painter's hand or drifted (helm and visor change between frames of
one clip).  A rig moves the PAINTED PIXELS THEMSELVES: nothing can drift, because
nothing is repainted.  And because the motion is AUTHORED rather than sampled, the
stride is solved against this build's own walk speed, so the planted foot does not
slide -- it is planted by construction, not by luck.

INPUT (read-only):
    runs/C-9/artifacts/seeds/seed_E.png   1024x1536, flat #00ff00 plate, true side view,
                                          facing screen-right, pollaxe in the near hand.

OUTPUT (all inside runs/C-9/cliffside_B/):
    sprites_rig_E/<part>.png      the cut parts
    sprites_rig_E/contact.png     labelled contact sheet of the split + the joints
    scenes/knight_rig_E.tscn      Skeleton2D/Bone2D rig + baked walk/idle AnimationPlayer
    frames/knight_rig_E.json      every measured number behind the above

NO GENERATIVE AI.  Where a part reveals pixels the still hides, the fill is MECHANICAL
and recorded in the JSON's "fills".  Anything that could not be filled mechanically
would be listed in "stopped" and left undone rather than invented.
"""
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

PROJ = Path(__file__).resolve().parent.parent
SEED = PROJ.parent / "artifacts" / "seeds" / "seed_E.png"
OUT_SPR = PROJ / "sprites_rig_E"
OUT_SCN = PROJ / "scenes" / "knight_rig_E.tscn"
OUT_JSON = PROJ / "frames" / "knight_rig_E.json"
FIT_JSON = PROJ / "frames" / "knight_fit.json"
SLIDE_JSON = PROJ / "frames" / "knight_foot_slide.json"
GAPFILL = PROJ / "frames" / "knight_rig_gapfill.npz"

# ---------------------------------------------------------------------------
# JOINTS, in seed_E.png pixels, read off the painting.
#   neck      under the gorget, where the surcoat collar begins
#   shoulder  behind the surcoat -- the near UPPER ARM is not painted anywhere in this
#             still, so it is a BONE WITH NO SPRITE.  Nothing is invented for it.
#   elbow     the couter's dome centre;  grip  the fist's centre on the shaft
#   hip       under the fauld;  knee  the poleyn's dome centre
#   ankle     top of the sabaton's ankle lames, above the heel
# ---------------------------------------------------------------------------
J = {
    "neck":        (437, 574),
    "torso":       (437, 782),
    "hip":         (438, 830),
    "shoulder":    (455, 632),
    "elbow":       (492, 712),
    "grip":        (585, 676),
    "knee":        (420, 1012),
    "ankle":       (408, 1215),
    "skirt_back":  (400, 756),
    "skirt_front": (468, 776),
}
FAR_DARKEN = 0.85      # the far side of a symmetric harness, 15% down in value
# The still puts the far sabaton 115 seed px above the near one -- a wide stance in
# depth, held for a portrait.  A WALK tracks its feet nearly in line, and carrying the
# portrait's spread into the cycle floats the far knee up beside the tabard as a lump.
# So the rig uses a pelvis-width depth offset instead: 32 seed px, ~3.5% of his height.
FAR_OFFSET_SEED = (10, -32)
RES = 2.0              # texels per canvas pixel in the part PNGs

# SWING-FOOT CLEARANCE, rig px. This is the single biggest lever on how high the knight
# picks his knees up, and the first value (11.0) was chosen by eye and was far too big:
# 11 px on a 194 px figure is 5.7% of his height, where a walking human clears the
# ground by about 1.5%. The THIGH bone -- hip to knee -- is what a viewer reads as
# "marching", and the keyed thigh range came out at 84.9 deg against a human walk's
# 40-50. (Checked for angle wrap first: the largest step between adjacent keys is
# 19.4 deg, and a 2*pi wrap would show ~360, so it was real geometry, not atan2.)
SWING_LIFT = 4.0

# Width of the hip-height smoothing window, as a fraction of the cycle. 6% is two keys
# either side at the walk's 32 -- enough to carry the hip across a stance handover, far
# too short to flatten the bob the plant derives.
HIP_SMOOTH_FRAC = 0.06

# --- THE JOINT FILLS (R-C9-40) ---------------------------------------------
# HIP_CAP_SEED is the radius, in seed px, of the disc each thigh carries at its hip
# socket.  It is not an eyeballed number: tools/render_rig_E.py rasterises the shipped
# scene and reports the largest ENCLOSED HOLE within 22 rig px of each joint, over
# every frame of every clip, and this is the smallest radius that drives all four leg
# joints to 0 in walk, run and idle.  38 seed px is 8.5 rig px on a 194 px figure --
# a cuisse top, and it lives behind the tabard and the torso, so it is only ever seen
# in the slot between the two hanging flaps, which is exactly where the gap opened.
HIP_CAP_SEED = 38
# The sabaton's working range, used to measure what the greave must cover.  Slightly
# wider than the gaits actually reach, so retuning the roll cannot silently outrun the
# fill that was built for it.
ANKLE_PHI_RANGE = (-66.0, 32.0)
KNEE_PHI_RANGE = (-6.0, 88.0)
# Disc radii, seed px, for the knee and ankle bosses. Sized by the render probe, not by
# eye: these are the smallest that drive every leg joint's enclosed-hole measure to 0.
KNEE_DISC_SEED = 34
ANKLE_DISC_SEED = 34
# Both are ENVELOPES the plates are cut to cover, not measurements of the gaits.  main()
# asserts afterwards that every keyed frame of every clip lies inside them and stops the
# build if not -- so retuning a gait cannot quietly outrun the fill that was built for
# the old one.  That failure would be invisible in every number this script prints.

# --- RUN -------------------------------------------------------------------
# The scene runs at 494 canvas px/s on the Keeper's 0.5517 s run stride, which is a
# step of 0.91 of this knight's figure height. There is no way to cover that with a
# foot on the ground throughout, so the run has a real FLIGHT phase: each foot is
# planted RUN_STANCE of the cycle and the remaining 1 - 2*RUN_STANCE is air. 0.30
# keeps the planted ankle's sweep inside the leg's reach without folding the knight
# into a crouch -- at 0.34 the hip has to drop 25 rig px (13% of his height) to stay
# in reach, at 0.30 it is 19.
RUN_STANCE = 0.30
RUN_LIFT = 10.0          # knees higher than the walk's 4.0, per the brief
RUN_LEAN_DEG = 7.0       # forward lean, +ve leans east (screen-clockwise, y down)
# The haft carried sloped across the body, head up and back over the near shoulder.
RUN_POLLAXE_DEG = 34.0
# ... and the far hand brought ACROSS onto the shaft for a two-handed carry. These are
# rotations of the painted far-arm plate only; nothing new is drawn.
RUN_FAR_ARM_BASE = {"arm_f_up": math.radians(-42.0),
                    "arm_f_lo": math.radians(64.0),
                    "hand_f": math.radians(12.0)}


# ---------------------------------------------------------------------------
def key_plate(path):
    """Key the flat #00ff00 plate and despill.

    The plate has a one-pixel antialias ramp against the figure, so the key is a RAMP,
    not a threshold: greenness = G - max(R,B) is 255 on the plate and negative on the
    knight; alpha falls from 1 to 0 across greenness 40 -> 120.  Measured on this file:
    1.38M px at greenness 255, 8.3k px below -100, and ~3.1k px in the whole transition
    band -- so the ramp only ever touches the silhouette's own edge.
    """
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    greenness = G - np.maximum(R, B)
    alpha = np.clip((120.0 - greenness) / 80.0, 0, 1)
    mx = np.maximum(R, B)
    G2 = np.where(G > mx, mx, G)
    return np.dstack([R, G2, B, alpha * 255.0]).astype(np.uint8)


def figure_metrics(mask, open_w, sole_min_run, body_pt):
    """Helm crown and sole rows for a knight who is carrying a pollaxe.

    build_knight_frames.py's rule -- a 1xN horizontal opening, then every component at
    least 5% of the largest -- deletes the SHAFT but then readmits the AXE HEAD, which
    the opening had correctly disconnected: for idle_E it returns crown row 188, which
    is the top of the axe blade, not of the helm (the helm crowns at 201).  The check
    ran and returned the wrong answer.  So this keeps only the component that CONTAINS
    THE BODY -- `body_pt` -- which is what "the figure's head" actually means.

    open_w must exceed the shaft's width and stay under the gorget's: 45 px in the
    1024x1536 seed, 11 px in a 512 cell.
    """
    opened = ndimage.binary_opening(mask, np.ones((1, open_w), bool))
    lab, _ = ndimage.label(opened)
    tag = lab[body_pt[1], body_pt[0]]
    if tag == 0:
        raise SystemExit("figure_metrics: body point %s is not on the figure" % (body_pt,))
    crown = int(np.nonzero(lab == tag)[0].min())
    sole = None
    for y in range(mask.shape[0] - 1, -1, -1):
        xs = np.nonzero(mask[y])[0]
        if len(xs) == 0:
            continue
        best, s, p = 1, xs[0], xs[0]
        for x in xs[1:]:
            if x > p + 2:
                best = max(best, p - s + 1)
                s = x
            p = x
        if max(best, p - s + 1) >= sole_min_run:
            sole = y
            break
    return crown, sole


# ---------------------------------------------------------------------------
def cut(rgba):
    """The split, decided from the pixels.  See the run report for the reasoning; the
    short version is that this harness tells you where to cut: plate armour articulates
    at overlapping lames, so every cut is placed INSIDE an overlap the painter already
    drew (cuisse over poleyn over greave over sabaton; couter over vambrace), and the
    upper plate is drawn in front of the lower one."""
    H, W = rgba.shape[:2]
    A = rgba[..., 3].astype(np.float32) / 255.0
    R, G, B = [rgba[..., i].astype(np.float32) for i in range(3)]
    fig = A > 0.5
    # CLOTH vs STEEL by SATURATION, not by per-hue thresholds.  The surcoat is the only
    # coloured thing on him and it is painted at saturation 0.72-0.97 (median, sampled
    # over the blue panel, the striped flap and the back flap); the plate runs 0.09-0.15.
    # Per-hue thresholds (B - max(R,G) > 35 and friends) lost the tabard's own SHADOWED
    # blue, which then fell through into the leg layer -- a hatched wedge of surcoat
    # rode on the thigh sprite and swung with it.
    mx = np.maximum(np.maximum(R, G), B)
    mn = np.minimum(np.minimum(R, G), B)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1.0), 0.0)
    cloth = fig & (sat > 0.35)
    cloth = ndimage.binary_closing(cloth, np.ones((5, 5), bool))
    cloth = ndimage.binary_opening(cloth, np.ones((5, 5), bool))
    lab_c, n_c = ndimage.label(cloth)
    if n_c:
        keep = [i + 1 for i, v in enumerate(ndimage.sum(cloth, lab_c, range(1, n_c + 1))) if v > 500]
        cloth = np.isin(lab_c, keep)          # drop rivet-and-outline speckle
    cloth &= fig
    steel = fig & ~cloth
    yy, xx = np.mgrid[0:H, 0:W]

    def poly(pts):
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
        return np.asarray(m) > 128

    P = {}
    # THE WEAPON, as a connected component rather than an x threshold.  A threshold
    # ("everything right of the shaft") silently loses the pieces of the pollaxe that
    # reach back OVER the body: the rear hammer at x505-570/y360-420 landed in the HEAD
    # layer and the brass ferrule at y1270-1305 landed in the TABARD layer, and both
    # cuts returned cleanly while doing it.  So: cut the fist band out, label what is
    # left, and take the components that hold the shaft above and below the fist.  The
    # whole weapon then rides with the gauntlet as ONE layer, and the shaft is never
    # cut behind the fist, so no shaft fill is needed anywhere.
    fist_box = (xx >= 552) & (xx <= 645) & (yy >= 618) & (yy <= 730)
    lab, _ = ndimage.label(fig & ~fist_box)
    weapon = np.zeros_like(fig)
    for probe in [(592, 260), (592, 900), (660, 400)]:      # shaft top, shaft bottom, blade
        tag = lab[probe[1], probe[0]]
        if tag:
            weapon |= (lab == tag)
    P["hand_pollaxe"] = weapon | (fig & fist_box)

    P["head"] = fig & (yy <= 582) & ~P["hand_pollaxe"]
    P["arm_near_lo"] = (steel & poly([(462, 646), (556, 620), (602, 662), (600, 716),
                                      (556, 744), (506, 750), (464, 730)])
                        & ~P["hand_pollaxe"] & ~P["head"])
    # the two hanging tabard flaps: cloth, below the belt, above the hem
    flap = cloth & (yy > 748) & (yy < 1000) & ~P["hand_pollaxe"]
    P["skirt_back"] = flap & (xx < 442)
    P["skirt_front"] = flap & (xx >= 442)

    far_foot_ghost = (xx > 448) & (yy > 1076) & (yy < 1194)   # the still's far sabaton
    leg = steel & ~P["hand_pollaxe"] & ~P["arm_near_lo"] & ~cloth
    P["leg_near_thigh"] = leg & (yy > 836) & (yy <= 1062) & ~far_foot_ghost & (xx > 356)
    P["leg_near_shin"] = leg & (yy > 1050) & (yy <= 1208) & ~far_foot_ghost
    P["leg_near_foot"] = leg & (yy > 1198)

    for k in list(P):
        P[k] = drop_specks(P[k])
    claimed = np.zeros_like(fig)
    for k in P:
        claimed |= P[k]
    P["torso"] = drop_specks(fig & ~claimed & ~far_foot_ghost & (yy <= 852))
    dropped = int((fig & ~claimed & ((yy > 852) | far_foot_ghost)).sum())
    return P, dropped, far_foot_ghost


def materialise(rgba, mask, feather=1.0):
    a = rgba.astype(np.float32).copy()
    m = ndimage.gaussian_filter(mask.astype(np.float32), feather)
    a[..., 3] = a[..., 3] * np.clip(m * 1.4, 0, 1)
    return a


def drop_specks(mask, frac=0.02):
    """Remove disconnected crumbs a threshold leaves behind, so a part is one plate."""
    lab, n = ndimage.label(mask)
    if n <= 1:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    keep = [i + 1 for i, v in enumerate(sizes) if v >= frac * sizes.max()]
    return np.isin(lab, keep)


def clone_up(arr, rows, band=4):
    """Mechanical under-hem fill: extrude the part's own WIDEST near-top row upward.

    Extruding the literal topmost row is wrong here: at the cut line the tabard covers
    almost all of the cuisse, so the topmost row is a narrow sliver and cloning it grew
    a spike instead of a hip.  The widest row in the first 60 is the plate at its full
    width, which is what is actually hidden under the hem.

    STILL USED for the arm (whose shoulder end is a short, nearly-unrotated stub).  It
    is NOT used for the thigh any more -- see hip_cap() for why a rectangle is the
    wrong shape at a joint that swings 75 deg.
    """
    cover = (arr[..., 3] > 8)
    ys = np.nonzero(cover.any(1))[0]
    if len(ys) == 0 or rows <= 0:
        return arr
    top = int(ys[0])
    widths = cover[top:top + 60].sum(1)
    best = top + int(np.argmax(widths))
    src = arr[best:best + band].copy()
    out = arr.copy()
    for i in range(1, rows + 1):
        y = top - i
        if y < 0:
            break
        out[y] = src[(i - 1) % band]
    return out


def hip_cap(arr, hip, radius, band=6, look=70):
    """Grow the cuisse's hidden upper end into a SOLID DISC CENTRED ON THE HIP SOCKET.

    THE BUG THIS FIXES (Matt, R-C9-40): "the legs detach at the thigh from the body and
    move as ghosts."  The thigh's hip end is under the tabard in the still, so it has to
    be filled.  clone_up() filled it by extruding the plate's widest row straight up --
    a RECTANGLE.  A rectangle rotated about a point inside it sweeps its corners away
    from the socket, and the thigh swings 75 deg in the walk and 99 deg in the run, so
    at the stride extremes the fill rotated clear of the hip and daylight opened between
    the tabard hem and the cuisse.  The thigh then read as a separate floating piece --
    a leg walking along beside the knight rather than under him.

    A DISC CENTRED ON THE PIVOT IS THE ONE SHAPE A ROTATION ABOUT THAT PIVOT CANNOT
    MOVE.  Whatever angle the thigh reaches, the same pixels cover the socket, so the
    join cannot open -- not "does not, at the angles we sampled", but cannot, for the
    same reason a wheel's hub stays put.  The radius is not guessed: it is measured by
    tools/render_rig_E.py, which rasterises the shipped scene and reports the largest
    enclosed hole at each joint.

    The fill is MECHANICAL.  The disc (and the vertical bridge from the disc down to
    the plate's own top, so no slit is left between them) is painted from the cuisse's
    own widest plate band, tiled vertically and clamped horizontally to the nearest
    column that has plate.  No pixel is invented; every one is the painter's.
    """
    H, W = arr.shape[:2]
    cover = arr[..., 3] > 8
    ys = np.nonzero(cover.any(1))[0]
    if len(ys) == 0:
        return arr, 0
    top = int(ys[0])
    widths = cover[top:top + look].sum(1)
    best = top + int(np.argmax(widths))
    src = arr[best:best + band].copy()
    src_cols = np.nonzero(cover[best:best + band].any(0))[0]
    xlo, xhi = int(src_cols.min()), int(src_cols.max())

    hx, hy = int(round(hip[0])), int(round(hip[1]))
    yy, xx = np.mgrid[0:H, 0:W]
    disc = ((xx - hx) ** 2 + (yy - hy) ** 2) <= radius * radius
    # bridge: in every column the disc touches, close the run between the disc's
    # bottom and the plate's own topmost pixel, so cap and plate are one solid piece
    fill = disc.copy()
    for x in range(max(0, hx - radius), min(W, hx + radius + 1)):
        dcol = np.nonzero(disc[:, x])[0]
        if len(dcol) == 0:
            continue
        pcol = np.nonzero(cover[:, x])[0]
        if len(pcol) == 0:
            continue
        a, b = int(dcol[-1]), int(pcol[0])
        if b > a:
            fill[a:b + 1, x] = True
    fill &= ~cover
    out = arr.copy()
    tys, txs = np.nonzero(fill)
    cx = np.clip(txs, xlo, xhi)
    out[tys, txs] = src[(hy - tys) % band, cx]
    out[tys, txs, 3] = 255.0
    return out, int(fill.sum())


def paint_from_seed(arr, rgba, mask):
    """Add a measured region to a plate, painted with the still's own pixels there.

    Only where the still is actually opaque: the harvest maps rendered canvas pixels
    back through a bone, and a couple of px of rounding at the silhouette's edge would
    otherwise pull background in and leave a fringe of keyed green on the plate.
    """
    new = mask & (arr[..., 3] <= 8) & (rgba[..., 3] > 128)
    out = arr.copy()
    ys, xs = np.nonzero(new)
    out[ys, xs] = rgba[ys, xs].astype(np.float32)
    out[ys, xs, 3] = 255.0
    return out, int(new.sum())


def joint_disc(arr, rgba, joint, radius):
    """Fill a SOLID DISC centred on a joint, from the still's own pixels there.

    Give BOTH plates of a joint the same disc about the same pivot and the join cannot
    open inside that radius, whatever the relative angle: a disc centred on a pivot is
    the one shape a rotation about that pivot leaves where it was, so the parent's disc
    and the child's disc occupy the same ground at every frame.  Under the still the
    knee, the ankle and the hip are all solid armour, so the disc is painted with the
    seed's own pixels at those coordinates -- at the painted pose it lies exactly on
    what it covers and cannot be seen; it only shows as the plate that was already
    there, once the limb has swung off it.
    """
    H, W = arr.shape[:2]
    jx, jy = int(round(joint[0])), int(round(joint[1]))
    yy, xx = np.mgrid[0:H, 0:W]
    disc = ((xx - jx) ** 2 + (yy - jy) ** 2) <= radius * radius
    new = disc & (arr[..., 3] <= 8) & (rgba[..., 3] > 128)
    out = arr.copy()
    ys, xs = np.nonzero(new)
    out[ys, xs] = rgba[ys, xs].astype(np.float32)
    out[ys, xs, 3] = 255.0
    return out, int(new.sum())


def joint_cover(front_arr, rgba, front_mask, back_mask, joint, phi_range,
                window=110, steps=21):
    """Grow the FRONT plate of a joint by exactly what the BACK plate's swing exposes.

    Plate armour overlaps in one direction -- cuisse over poleyn over greave over
    sabaton -- so at every joint one plate is in front and it is that one's job to hide
    the seam.  In the still the overlap is only as deep as the painter needed for a
    standing figure: 11 seed px at the knee, and at the ankle a straight cut 62 px wide
    with the pivot at one END of it.  That is enough for a pose and nowhere near enough
    for a 100 deg knee bend or an articulating foot, so daylight opens behind the joint
    and the limb below it reads as a separate piece.

    So: rotate the back plate about the joint through its whole working range and, at
    each angle, collect the ENCLOSED background -- background with figure on every side.
    Their union is precisely the region the front plate has to own; nothing more is
    added, and the measurement is redone whenever the range changes.

    The fill takes the STILL'S OWN pixels at those coordinates -- that region is solid
    armour in the painting -- so at the painted angle the extension lies pixel for pixel
    on what it covers and cannot be seen.  It only ever appears as the plate that was
    always there, once the limb has swung off it.
    """
    H, W = front_mask.shape
    ax, ay = joint
    need = np.zeros((H, W), bool)
    yy, xx = np.mgrid[0:H, 0:W]
    near = ((xx - ax) ** 2 + (yy - ay) ** 2) <= window * window
    for i in range(steps):
        phi = math.radians(phi_range[0] + (phi_range[1] - phi_range[0]) * i / (steps - 1.0))
        c, s = math.cos(-phi), math.sin(-phi)          # inverse rotation for sampling
        sx = c * (xx - ax) - s * (yy - ay) + ax
        sy = s * (xx - ax) + c * (yy - ay) + ay
        ix = np.clip(np.round(sx).astype(np.int32), 0, W - 1)
        iy = np.clip(np.round(sy).astype(np.int32), 0, H - 1)
        union = front_mask | back_mask[iy, ix]
        lab, _ = ndimage.label(~union)
        border = set(np.unique(lab[0])) | set(np.unique(lab[-1])) | \
            set(np.unique(lab[:, 0])) | set(np.unique(lab[:, -1]))
        border.discard(0)
        holes = (~union) & ~np.isin(lab, list(border))
        need |= holes & near
    need = ndimage.binary_closing(need, np.ones((7, 7), bool))
    need = ndimage.binary_dilation(need, np.ones((3, 3), bool)) & ~front_mask
    out = front_arr.copy()
    ys, xs = np.nonzero(need)
    if len(ys) == 0:
        return out, 0, (0, 0)
    out[ys, xs] = rgba[ys, xs].astype(np.float32)
    out[ys, xs, 3] = 255.0
    return out, int(need.sum()), (int(ys.min()), int(ys.max()))


def lower_hull(mask):
    """The sabaton's SOLE, as the lower convex hull of its silhouette, heel to toe.

    This is where the heel-toe angles come from.  They are not chosen: the painter drew
    this sabaton with a rounded heel, a rockered sole and a long poulaine beak, and the
    angles a foot must pass through to roll over that shape ARE the shape's own tangent
    angles.  Reading them off the hull means the roll cannot drive the sole through the
    ground or lift it off, because the ground is the hull's own tangent line.

    Screen y is down, so "lower" is MAXIMUM y and the hull is the chain that bulges
    downward; concave dents in the painted outline (the notch between heel and instep)
    are skipped, which is correct -- a dent never touches the ground.
    """
    ys, xs = np.nonzero(mask)
    pts = {}
    for x, y in zip(xs, ys):
        if x not in pts or y > pts[x]:
            pts[x] = y
    P = sorted(pts.items())
    hull = []
    for p in P:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            # keep p if (hull[-2] -> hull[-1] -> p) turns downward (convex from below)
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) >= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    return [(float(x), float(y)) for x, y in hull]


def resample_hull(hull, ankle, scale, n=96, smooth=9):
    """Hull -> (arc lengths, ankle-relative rig-px points, smoothed tangent angles).

    The tangent is smoothed because the hull of a PIXEL mask is a staircase of short
    segments whose angles jump; an unsmoothed tangent makes the foot flick between
    facets mid-stance.  The smoothing window is a fraction of the sole, so the roll
    reads as a rocker rather than as a polygon.
    """
    P = [((x - ankle[0]) * scale, (y - ankle[1]) * scale) for x, y in hull]
    seg = [math.dist(P[i], P[i + 1]) for i in range(len(P) - 1)]
    cum = [0.0]
    for s in seg:
        cum.append(cum[-1] + s)
    total = cum[-1]
    out_s = [total * i / (n - 1) for i in range(n)]
    out_p, out_t = [], []
    for s in out_s:
        j = min(max(np.searchsorted(cum, s) - 1, 0), len(seg) - 1)
        f = (s - cum[j]) / max(seg[j], 1e-9)
        out_p.append((P[j][0] + (P[j + 1][0] - P[j][0]) * f,
                      P[j][1] + (P[j + 1][1] - P[j][1]) * f))
        out_t.append(math.atan2(P[j + 1][1] - P[j][1], P[j + 1][0] - P[j][0]))
    k = max(1, smooth)
    sm = [sum(out_t[max(0, i - k):min(n, i + k + 1)]) /
          len(out_t[max(0, i - k):min(n, i + k + 1)]) for i in range(n)]
    return out_s, out_p, sm


def hull_at(S, Pts, Tan, s):
    """Linear lookup of (contact point, tangent angle) at arc length s."""
    s = min(max(s, S[0]), S[-1])
    i = min(max(int(np.searchsorted(S, s)) - 1, 0), len(S) - 2)
    f = (s - S[i]) / max(S[i + 1] - S[i], 1e-9)
    p = (Pts[i][0] + (Pts[i + 1][0] - Pts[i][0]) * f,
         Pts[i][1] + (Pts[i + 1][1] - Pts[i][1]) * f)
    return p, Tan[i] + (Tan[i + 1] - Tan[i]) * f


def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def foot_low(Pts, phi):
    """Lowest (max y) point of the rotated sole, ankle-relative.  Used to keep the
    swinging foot out of the ground and to check the planted one does not sink."""
    return max(rot(p, phi)[1] for p in Pts)


def darken(arr, f=FAR_DARKEN):
    out = arr.astype(np.float32).copy()
    out[..., :3] *= f
    return out


# ---------------------------------------------------------------------------
def keeper_run_stride(proj):
    """The Keeper's RUN stride in seconds, read from frames/keeper.tres.

    Read rather than hardcoded for the same reason the walk cadence is: if her run is
    ever re-tuned the knight follows it. Matches EVERY animation block and then filters
    by name -- restricting the name inside the pattern lets the non-greedy body run
    across the blocks that do not match and absorb their frames.
    """
    text = (proj / "frames" / "keeper.tres").read_text()
    body = text[text.index("[resource]"):]
    pattern = r'\{"frames": \[(.*?)\], "loop": \w+, "name": &"([^"]+)", "speed": ([0-9.]+)\}'
    for frames, name, speed in re.findall(pattern, body, re.S):
        if name == "run_E":
            return frames.count("ExtResource") / float(speed)
    raise SystemExit("keeper.tres: no run_E animation")


def two_bone_ik(hip, ankle, l1, l2, knee_front=True):
    """Solve knee position for a 2-bone chain.  Returns (knee, reachable)."""
    dx, dy = ankle[0] - hip[0], ankle[1] - hip[1]
    d = math.hypot(dx, dy)
    reachable = d <= l1 + l2 - 1e-6
    d = min(d, l1 + l2 - 1e-4)
    if d < 1e-6:
        d = 1e-6
    a = (d * d + l1 * l1 - l2 * l2) / (2.0 * d)
    h2 = max(l1 * l1 - a * a, 0.0)
    h = math.sqrt(h2)
    ux, uy = dx / d, dy / d
    px, py = hip[0] + a * ux, hip[1] + a * uy
    # perpendicular; +x side is "knee forward" for a figure facing screen-right
    nx, ny = -uy, ux
    if (nx < 0) == knee_front:
        nx, ny = -nx, -ny
    return (px + h * nx, py + h * ny), reachable


def ang(p, q):
    return math.atan2(q[1] - p[1], q[0] - p[0])


# ---------------------------------------------------------------------------
def main():
    rgba = key_plate(SEED)
    fit = json.loads(FIT_JSON.read_text())
    slide = json.loads(SLIDE_JSON.read_text())

    node_scale = fit["knight"]["scale"]             # 0.7276...
    pivot = [-v for v in fit["knight"]["offset"]]   # (256.511, 395.1875) cell px
    walk_px_s = float(slide["walk_px_s"])           # 247 canvas px/s
    stride_T = float(fit["keeper_walk_stride_seconds"]["E"])   # 0.57971 s
    run_px_s = float(json.loads((PROJ / "parallax" / "parallax.json").read_text())
                     ["movement"]["run_px_s"])                 # 494 canvas px/s
    run_T = keeper_run_stride(PROJ)                            # 0.55172 s, read not assumed

    # REGISTRATION.  The rig must be the same knight, the same size, standing on the
    # same spot as the Grok E cells -- otherwise pressing G would show a size or
    # position change and the A/B would be measuring the wrong thing.  So it is
    # registered directly against sprites_knight/rest/idle_E.png, helm crown to sole,
    # rather than against knight_fit's mean figure height (which is the 16-cell mean
    # and, for the E-facing cells, is measured to the axe blade -- see figure_metrics).
    seedmask = rgba[..., 3] > 128
    crown, sole = figure_metrics(seedmask, 45, 60, (437, 900))
    ref = np.asarray(Image.open(PROJ / "sprites_knight" / "rest" / "idle_E.png"))[..., 3] > 128
    ref_crown, ref_sole = figure_metrics(ref, 11, 12, (250, 330))
    s = float(ref_sole - ref_crown) / float(sole - crown)      # seed px -> cell px
    ref_foot_cx = float(np.nonzero(ref[ref_sole - 6:ref_sole + 1])[1].mean())
    seed_foot_cx = float(np.nonzero(seedmask[sole - 6:sole + 1])[1].mean())
    target_h = float(ref_sole - ref_crown)

    def R(p):
        """seed px -> rig-local px (cell units; origin = the sprite's foot pivot)."""
        return ((p[0] - seed_foot_cx) * s + (ref_foot_cx - pivot[0]),
                (p[1] - sole) * s)

    Jr = {k: R(v) for k, v in J.items()}
    far_off = (FAR_OFFSET_SEED[0] * s, FAR_OFFSET_SEED[1] * s)

    # ---------------- cut + fill ----------------
    P, dropped, ghost = cut(rgba)
    OUT_SPR.mkdir(exist_ok=True)
    parts, fills = {}, {}
    for name in ["head", "torso", "skirt_back", "skirt_front", "arm_near_lo",
                 "hand_pollaxe", "leg_near_thigh", "leg_near_shin", "leg_near_foot"]:
        parts[name] = materialise(rgba, P[name])

    # THE HIP JOIN.  Each thigh gets a solid disc centred on ITS OWN hip socket -- the
    # near one on J["hip"], the far one on the hip offset into depth -- because the far
    # thigh is the same plate hung on a bone 32 seed px up and 10 forward, and capping
    # it at the near socket would leave its own socket a third of a cap-radius bare.
    # THE KNEE.  The poleyn is in front of the greave, so the poleyn owns the bend.  In
    # the still the cuisse overlaps the greave by 11 seed px -- fine for a man standing,
    # not remotely enough for the 100 deg knee the run reaches, where the back of the
    # bend opened a triangle of daylight big enough to cut the shin off from the thigh.
    # Matching discs on both sides of the knee and the ankle.  The joint_cover fills
    # below then add whatever the swing exposes OUTSIDE those radii.
    disc_n = {}
    parts["leg_near_thigh"], disc_n["thigh_knee"] = joint_disc(
        parts["leg_near_thigh"], rgba, J["knee"], KNEE_DISC_SEED)
    parts["leg_near_shin"], disc_n["shin_knee"] = joint_disc(
        parts["leg_near_shin"], rgba, J["knee"], KNEE_DISC_SEED)
    parts["leg_near_shin"], disc_n["shin_ankle"] = joint_disc(
        parts["leg_near_shin"], rgba, J["ankle"], ANKLE_DISC_SEED)
    parts["leg_near_foot"], disc_n["foot_ankle"] = joint_disc(
        parts["leg_near_foot"], rgba, J["ankle"], ANKLE_DISC_SEED)
    fills["leg_joint_discs"] = (
        "solid discs from the still's own pixels on BOTH plates of each leg joint: "
        "knee r=%d seed px (%d px into the cuisse, %d into the greave), ankle r=%d "
        "(%d into the greave, %d into the sabaton). Matching discs about a shared pivot "
        "cannot be separated by a rotation about it."
        % (KNEE_DISC_SEED, disc_n["thigh_knee"], disc_n["shin_knee"], ANKLE_DISC_SEED,
           disc_n["shin_ankle"], disc_n["foot_ankle"]))

    knee_back = P["leg_near_shin"] | P["leg_near_foot"]
    parts["leg_near_thigh"], n_knee, knee_box = joint_cover(
        parts["leg_near_thigh"], rgba, P["leg_near_thigh"], knee_back,
        J["knee"], KNEE_PHI_RANGE, window=150)
    fills["leg_near_thigh_knee"] = (
        "cuisse extended over the greave by %d px (seed rows %d..%d) -- the union, over "
        "the knee's %+.0f..%+.0f deg working range, of the pixels the poleyn seam leaves "
        "bare; painted with the still's own pixels at those coordinates."
        % (n_knee, knee_box[0], knee_box[1], KNEE_PHI_RANGE[0], KNEE_PHI_RANGE[1]))

    bare_thigh = parts["leg_near_thigh"]
    far_hip = (J["hip"][0] + FAR_OFFSET_SEED[0], J["hip"][1] + FAR_OFFSET_SEED[1])
    parts["leg_near_thigh"], n_near = hip_cap(bare_thigh, J["hip"], HIP_CAP_SEED)
    far_thigh, n_far = hip_cap(bare_thigh, far_hip, HIP_CAP_SEED)
    fills["leg_near_thigh"] = (
        "hip end grown into a SOLID DISC of radius %d seed px centred on the hip socket "
        "%s (%d px filled), painted from the cuisse's own widest plate band, tiled "
        "vertically and clamped to the nearest column with plate. A disc centred on the "
        "pivot is invariant under rotation about it, so the socket stays covered at every "
        "angle of the walk and the run -- this replaces a rectangular clone_up whose "
        "corners swung clear of the socket and let the thigh read as detached."
        % (HIP_CAP_SEED, J["hip"], n_near))
    parts["arm_near_lo"] = clone_up(parts["arm_near_lo"], 14)
    fills["arm_near_lo"] = ("couter end cloned 14 rows upward -- the upper arm is behind "
                            "the surcoat in the still")

    # THE ANKLE JOIN.  The shin/sabaton cut is a straight line 62 seed px wide with the
    # ankle pivot at its BACK end, so once the foot articulates (it did not before) the
    # forward end of that cut swings up to 26 px clear of the greave.  The greave is the
    # piece in front (cuisse over poleyn over greave over sabaton), so the greave is what
    # must cover it.  The extension is not guessed: the foot is rotated through its whole
    # working range and the pixels that go bare are collected.
    parts["leg_near_shin"], n_ank, ank_box = joint_cover(
        parts["leg_near_shin"], rgba, P["leg_near_shin"], P["leg_near_foot"],
        J["ankle"], ANKLE_PHI_RANGE)
    fills["leg_near_shin"] = (
        "greave extended over the instep by %d px -- the union, over the sabaton's whole "
        "%+.0f..%+.0f deg working range, of the pixels that the shin/sabaton seam leaves "
        "bare; seed rows %d..%d. Painted with the STILL'S OWN pixels at those coordinates "
        "(the instep, un-moved), so at the painted angle the extension is invisible."
        % (n_ank, ANKLE_PHI_RANGE[0], ANKLE_PHI_RANGE[1], ank_box[0], ank_box[1]))

    # THE MEASURED FILL.  tools/harvest_gaps.py rasterises the shipped scene, finds the
    # background that ends up ENCLOSED by figure -- which is what "the leg has come away
    # from the body" is, in pixels -- and maps each such pixel back through its bone into
    # these seed coordinates.  Everything above is a model of where a cutout leg ought to
    # come apart; this is where it does.  Build, harvest, build again: the loop ends when
    # the harvest is empty, and frames/knight_rig_gapfill.npz is the record of it.
    gapfill = {}
    if GAPFILL.exists():
        gapfill = dict(np.load(GAPFILL))
        for nm, keyed in (("leg_near_thigh", "leg_near_thigh"),
                          ("leg_near_shin", "leg_near_shin")):
            if keyed in gapfill:
                parts[nm], n = paint_from_seed(parts[nm], rgba, gapfill[keyed])
                fills[nm + "_measured"] = (
                    "%d px added where the RENDERED rig actually opened an enclosed hole "
                    "at this joint, over every frame of walk, run and idle "
                    "(tools/harvest_gaps.py); painted with the still's own pixels." % n)
        if "leg_far_thigh" in gapfill:
            far_thigh, n_ft = paint_from_seed(far_thigh, rgba, gapfill["leg_far_thigh"])
            fills["leg_far_thigh_measured"] = "%d px, measured as above on the far side" % n_ft
    # THE BACKDROP.  One rigid plate on the hip bone, drawn behind every other part, so
    # the slot between the two tabard flaps and the space between the legs are never
    # empty.  Its shape is the measured hip region (harvest_gaps.py) unioned with the
    # slot itself, clipped to what the tabard hangs over; its pixels are the still's own
    # at those coordinates -- which there is the inside of the surcoat and the top of
    # the thighs -- put a third down in value, because what you are seeing through a gap
    # in a man's clothing is in shadow. Nothing is invented and nothing of him is hidden:
    # it is the LAST thing drawn under, so it can only ever appear where there was a hole.
    bd = np.zeros(P["torso"].shape, bool)
    if "body_backdrop" in gapfill:
        bd |= gapfill["body_backdrop"]
    yy0, xx0 = np.mgrid[0:bd.shape[0], 0:bd.shape[1]]
    bd |= (xx0 >= 424) & (xx0 <= 470) & (yy0 >= 836) & (yy0 <= 995)
    bd &= (yy0 >= 800) & (yy0 <= 1005) & (xx0 >= 356) & (xx0 <= 545)
    backdrop = np.zeros_like(parts["torso"])
    bys, bxs = np.nonzero(bd & (rgba[..., 3] > 128))
    backdrop[bys, bxs] = rgba[bys, bxs].astype(np.float32)
    backdrop[bys, bxs, 3] = 255.0
    parts["body_backdrop"] = darken(backdrop, 0.68)
    fills["body_backdrop"] = (
        "NEW PART. %d px on the hip bone at the bottom of the z order: the measured hip "
        "region plus the slot between the tabard flaps (x424-470, y836-995), seed rows "
        "%d..%d, painted with the still's own pixels and darkened x0.68. The torso plate "
        "stops 22 px below the hip and the tabard is two separate hanging flaps, so "
        "below the belt the only thing between the flaps was the legs themselves -- part "
        "them and the background showed through the knight."
        % (len(bys), bys.min() if len(bys) else 0, bys.max() if len(bys) else 0))

    far_shin = parts["leg_near_shin"]
    if "leg_far_shin" in gapfill:
        far_shin, n_fs = paint_from_seed(far_shin, rgba, gapfill["leg_far_shin"])
        fills["leg_far_shin_measured"] = "%d px, measured as above on the far side" % n_fs

    for a, b, src in [("leg_near_thigh", "leg_far_thigh", far_thigh),
                      ("leg_near_shin", "leg_far_shin", far_shin),
                      ("leg_near_foot", "leg_far_foot", parts["leg_near_foot"])]:
        parts[b] = darken(src)
        fills[b] = "copy of %s, value x%.2f (symmetric harness; far side in shade)%s" % (
            a, FAR_DARKEN,
            "; hip disc re-centred on the far socket %s" % (far_hip,) if b.endswith("thigh") else "")
    parts["arm_far_lo"] = darken(parts["arm_near_lo"])
    fills["arm_far_lo"] = "copy of arm_near_lo, value x%.2f" % FAR_DARKEN

    H, W = rgba.shape[:2]
    yy = np.mgrid[0:H, 0:W][0]
    fist_mask = P["hand_pollaxe"] & (yy >= 618) & (yy <= 728)
    fist = materialise(rgba, fist_mask)
    SHAFT = (572, 616)
    for y in range(618, 729):
        strip = fist[y, SHAFT[0] - 14:SHAFT[0]]
        if strip[..., 3].max() > 8:
            reps = int(np.ceil((SHAFT[1] - SHAFT[0]) / 14.0))
            fist[y, SHAFT[0]:SHAFT[1]] = np.tile(strip, (reps, 1))[:SHAFT[1] - SHAFT[0]]
    parts["hand_far"] = darken(fist)
    fills["hand_far"] = ("gauntlet band y618-728 with the pollaxe shaft column x572-616 "
                         "removed and the hole closed by tiling the fist's own plate from "
                         "x558-572 across it; value x%.2f" % FAR_DARKEN)

    # ---------------- write part PNGs, at RES texels per canvas pixel -------
    f_px = s * node_scale * RES            # seed px -> part-PNG texel
    sprite_scale = 1.0 / (node_scale * RES)  # part-PNG texel -> rig (cell) px
    meta = {}
    for name, arr in sorted(parts.items()):
        a8 = np.clip(arr, 0, 255).astype(np.uint8)
        ys, xs = np.nonzero(a8[..., 3] > 4)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        crop = Image.fromarray(a8[y0:y1, x0:x1], "RGBA")
        w2, h2 = max(1, int(round((x1 - x0) * f_px))), max(1, int(round((y1 - y0) * f_px)))
        crop.resize((w2, h2), Image.LANCZOS).save(OUT_SPR / ("%s.png" % name))
        cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        meta[name] = {"seed_rect": [x0, y0, x1, y1], "png_size": [w2, h2],
                      "centre_rig": list(R((cx, cy)))}

    # ---------------- contact sheet ----------------
    COLORS = {"head": (232, 214, 128), "torso": (92, 160, 240), "skirt_back": (204, 96, 204),
              "skirt_front": (240, 144, 64), "arm_near_lo": (64, 216, 120),
              "hand_pollaxe": (236, 84, 84), "leg_near_thigh": (152, 152, 255),
              "leg_near_shin": (104, 104, 212), "leg_near_foot": (56, 56, 168)}
    lab = np.zeros((H, W, 3), np.uint8)
    lab[ghost & (rgba[..., 3] > 128)] = (70, 70, 70)
    for k, c in COLORS.items():
        lab[P[k]] = c
    base = np.asarray(Image.open(SEED).convert("RGB")).astype(np.float32)
    blend = (base * 0.35 + lab.astype(np.float32) * 0.65).astype(np.uint8)
    blend[(rgba[..., 3] <= 128)] = (18, 18, 24)
    sheet = Image.fromarray(blend).crop((300, 380, 720, 1320)).resize((420 * 2, 940 * 2), Image.LANCZOS)
    d = ImageDraw.Draw(sheet)
    for k, (px, py) in J.items():
        X, Y = (px - 300) * 2, (py - 380) * 2
        d.ellipse([X - 7, Y - 7, X + 7, Y + 7], outline=(255, 255, 255), width=3)
        d.text((X + 11, Y - 7), k, fill=(255, 255, 255))
    sheet.save(OUT_SPR / "contact.png")

    # =====================================================================
    # THE GAITS.  Solved, not drawn: the planted ankle is DRIVEN backward at exactly
    # the scene's own speed for that gait, and the leg angles come from 2-bone IK
    # against it.  The foot cannot slide, because sliding is not representable in this
    # parameterisation.  WALK and RUN differ only in their parameters.
    # =====================================================================
    l1 = math.dist(Jr["hip"], Jr["knee"])
    l2 = math.dist(Jr["knee"], Jr["ankle"])
    Lmax = (l1 + l2) * 0.998
    ankle_h = -Jr["ankle"][1]                        # ankle height above the ground
    hip_h_paint = -Jr["hip"][1]

    # THE SOLE.  The sabaton's lower convex hull, ankle-relative, in rig px: the curve
    # the foot rolls on.  Everything about the heel-toe -- its angles, its timing, the
    # fact that it neither sinks nor floats -- comes off this one measurement.
    # read off the FINAL sabaton, not the cut mask: the ankle disc changes the silhouette
    # a little at the heel, and a sole line taken before the fill would be a sole line
    # the drawn foot does not have -- a few px of sink at heel strike, invisible to
    # every number here and visible on screen.
    SOLE_S, SOLE_P, SOLE_T = resample_hull(
        lower_hull(parts["leg_near_foot"][..., 3] > 128), J["ankle"], s)
    sole_deg = [round(math.degrees(-t), 2) for t in SOLE_T]

    # THE FAR ARM.  The only arm the painter drew is the near one, bent, gripping the
    # haft.  The far arm is that same plate, darkened, and it must not be left in the
    # gripping pose -- it holds nothing.  These constant offsets swing it down so it
    # hangs along the far side of the body, where it is mostly behind the torso and
    # shows only at the back of its swing.  Rotation of the painter's own pixels; no
    # new pixels anywhere.
    FAR_ARM_BASE = {"arm_f_up": math.radians(30.0),
                    "arm_f_lo": math.radians(81.0),
                    "hand_f": math.radians(-111.0)}

    rest = {
        "thigh": ang(Jr["hip"], Jr["knee"]),
        "shin": ang(Jr["knee"], Jr["ankle"]),
        "foot": 0.0,
        "torso": 0.0, "head": 0.0, "skirt_b": 0.0, "skirt_f": 0.0,
        "arm_up": ang(Jr["shoulder"], Jr["elbow"]),
        "arm_lo": ang(Jr["elbow"], Jr["grip"]),
        "hand": 0.0,
    }

    def s_at_phi(phi_deg):
        """Arc length along the sole whose (smoothed) tangent puts the foot at this
        angle.  phi is measured from the PAINTED pose, which is the pose whose rockered
        forefoot is flat on the ground -- so -18 really is 'toe up 18 degrees off flat'
        and +30 really is 'toe down 30', the way the brief states them."""
        want = -math.radians(phi_deg)
        best, bs = None, 1e9
        for s, t in zip(SOLE_S, SOLE_T):
            if abs(t - want) < bs:
                bs, best = abs(t - want), s
        return best

    def author_gait(px_s, stride_T, stance_frac, swing_lift, nominal_drop,
                    lean_deg, tabard_deg_front, tabard_deg_back, arm_near_deg,
                    arm_far_deg, pollaxe_deg, far_arm_base, lag_s,
                    roll_phi=(-18.0, 30.0), swing_clear=2.0, N=32):
        """Solve one gait. Returns (times, tracks, hip_positions, stats).

        stance_frac is the fraction of the cycle ONE foot is planted.  0.5 is a walk
        with no double support; below 0.5 the two stances no longer fill the cycle and
        the difference is FLIGHT -- which is what makes a run possible at all here.
        The scene's run speed is 494 px/s against a 0.5517 s stride, so a step is
        0.91 of this knight's figure height: there is no way to cover that with a foot
        on the ground the whole time, and no amount of animation polish substitutes for
        the flight phase.  During flight no leg constrains the hip, so the hip rises to
        its nominal height on its own -- the run's bounce is the same derived quantity
        the walk's much smaller bob is, not a curve laid on top.
        """
        v_rig = px_s / node_scale                    # canvas px/s -> rig px/s
        travel = v_rig * stride_T * stance_frac      # body travel during one stance
        hip_h_nom = hip_h_paint - nominal_drop
        lean = math.radians(lean_deg)
        ts = [stride_T * i / N for i in range(N + 1)]

        # --- HEEL-TOE, AS A ROLL ---------------------------------------------
        # Matt: "the feet should not be flat -- they need to move up and down."  The
        # old rig held the sabaton at a fixed world angle for the whole cycle
        # (d["leg_ft"] = -sh), so the foot was a rigid paddle that never articulated.
        #
        # The fix is not a rotation curve laid on top of the old ankle path.  The foot
        # ROLLS over its own sole: the contact walks forward along the sabaton's lower
        # convex hull from heel to beak, the foot's angle at every instant is whatever
        # makes the hull TANGENT at the contact lie flat on the ground, and the ankle
        # is then placed by that contact rather than driven directly.  Three things
        # follow for free, none of them tuned:
        #   * the heel-toe angles are the painted sabaton's own tangent angles;
        #   * the sole can neither sink into the ground nor float above it, because
        #     the ground IS the tangent line;
        #   * NO SLIP.  Rolling without slipping means the ground distance covered
        #     equals the arc length rolled, so the material point at the contact has
        #     zero world velocity -- which is the same guarantee the old ankle-pinned
        #     parameterisation gave, made at the point that is actually touching.
        # The previous attempt at heel-toe was rejected because pivoting over the toe
        # made the reach worse.  It does the opposite here: the ankle RISES over the
        # rolling forefoot in late stance (+11 rig px at toe-off), which is reach the
        # leg gets back, and the roll itself carries A of the step, so the ankle's own
        # rig-local sweep shrinks from `travel` to `travel - A`.
        s0, s1 = s_at_phi(roll_phi[0]), s_at_phi(roll_phi[1])
        A_roll = s1 - s0

        def stance_pose(u, ground_y):
            """u in [0,1] across the stance.  Returns (ankle, phi, contact)."""
            sg = s0 + (s1 - s0) * u
            c, tau = hull_at(SOLE_S, SOLE_P, SOLE_T, sg)
            phi = -tau
            r = rot(c, phi)
            # contact's rig-local x: it rolls forward by (sg - s0) in WORLD while the
            # body moves forward by travel*u, so in the body's frame it goes backward
            # by (travel*u - (sg - s0)).
            cxr = (sg - s0) - travel * u
            return (cxr - r[0], ground_y - r[1]), phi, (cxr, ground_y)

        # WHERE THE STEP SITS UNDER THE BODY.  The old rig centred the ankle's sweep on
        # the hip's x, which is the obvious choice and is not the best one once the foot
        # articulates: the two ends of the stance are no longer equally expensive.  At
        # heel strike the ankle is LOW (8.9 rig px above the ground, because this
        # sabaton's heel sits close under the ankle), so reaching forward costs the leg
        # a lot of its length; at toe-off the ankle has risen to 27.5, so reaching
        # backward is nearly free.  A symmetric sweep therefore spends the leg's reach
        # on the expensive end and wastes it on the cheap one, and the hip has to drop
        # to pay for it.
        #
        # So the placement is SOLVED, not centred: scan the fore-aft offset and keep the
        # one that maximises the lowest height the supporting leg allows -- i.e. the one
        # that makes the crouch as small as this leg length and this step length permit.
        # Bounded to a quarter of the sweep, because past that the knight stops looking
        # like he is walking through his step and starts looking like he is shuffling
        # behind it.
        _xs = [stance_pose(i / 24.0, 0.0)[0][0] for i in range(25)]
        _mid = (min(_xs) + max(_xs)) / 2.0
        _span = max(_xs) - min(_xs)

        def _min_hh(rc):
            m = 1e9
            for i in range(41):
                a, _phi, _c = stance_pose(i / 40.0, 0.0)
                dx = a[0] + (Jr["hip"][0] - rc) - Jr["hip"][0]
                m = min(m, math.sqrt(max(Lmax * Lmax - dx * dx, 1.0)) - a[1])
            return m

        _cands = [_mid + k * _span * 0.01 for k in range(-25, 26)]
        roll_centre = max(_cands, key=_min_hh)
        plant_bias = roll_centre - _mid

        def ankle_traj(phase, ground_y, x_off):
            """0 .. stance_frac = PLANTED (rolling); the rest is swing/flight."""
            shift = Jr["hip"][0] + x_off - roll_centre
            if phase < stance_frac:
                u = phase / stance_frac
                a, phi, _ = stance_pose(u, ground_y)
                return (a[0] + shift, a[1]), phi, True
            u = (phase - stance_frac) / (1.0 - stance_frac)
            a1, phi1, _ = stance_pose(1.0, ground_y)     # toe-off
            a0, phi0, _ = stance_pose(0.0, ground_y)     # next heel strike
            e = u * u * (3 - 2 * u)
            # the toe comes up EARLY in the swing (it has to clear), then the foot is
            # carried at the landing angle -- so the angle curve finishes at 55% and
            # holds, rather than easing across the whole swing.
            q = min(1.0, u / 0.55)
            phi = phi1 + (phi0 - phi1) * (q * q * (3 - 2 * q))
            x = a1[0] + (a0[0] - a1[0]) * e
            lift = math.sin(math.pi * u) ** 1.4 * swing_lift
            y = a1[1] + (a0[1] - a1[1]) * e - lift
            # and the swinging sole must not scrape: the foot's own lowest point,
            # at THIS angle, is what has to clear the ground -- not the ankle.
            y = min(y, ground_y - swing_clear - foot_low(SOLE_P, phi))
            return (x + shift, y), phi, False

        frames = []
        hip_limit = []
        contact_keys = []
        clamped = 0
        min_clear = 1e9
        for tt in ts:
            ph = (tt / stride_T) % 1.0
            a_n, phi_n, st_n = ankle_traj(ph, 0.0, 0.0)
            a_f, phi_f, st_f = ankle_traj((ph + 0.5) % 1.0, far_off[1], far_off[0])
            for a, phi, gy, st in ((a_n, phi_n, 0.0, st_n), (a_f, phi_f, far_off[1], st_f)):
                if not st:
                    min_clear = min(min_clear, gy - (a[1] + foot_low(SOLE_P, phi)))
            ph_n = ph
            if ph_n < stance_frac:
                _u = ph_n / stance_frac
                _sg = s0 + (s1 - s0) * _u
                _c, _tau = hull_at(SOLE_S, SOLE_P, SOLE_T, _sg)
                _cx = (_sg - s0) - travel * _u + (Jr["hip"][0] - roll_centre)
                contact_keys.append([round(_c[0], 4), round(_c[1], 4), 1, round(_cx, 4)])
            else:
                contact_keys.append([0.0, 0.0, 0, 0.0])
            # The hip sits at the nominal height unless the SUPPORTING leg cannot reach
            # its ankle from there.  Solving hh out of |hip - ankle| <= Lmax, with the
            # far leg's own ground line folded in via goff:
            #     hh <= sqrt(Lmax^2 - dx^2) - (ankle_y - goff)
            # So the bob/bounce is DERIVED FROM THE PLANT, never added on top of it.
            # BOTH LEGS, ALWAYS -- not just the planted one.  Restricting the reach
            # clamp to the supporting leg makes the binding constraint CHANGE IDENTITY
            # in a single frame at each stance handover, and because the two legs stand
            # on ground lines 7.1 rig px apart (the depth offset) the two constraints do
            # not agree there: the hip stepped 2.32 rig px -- the whole bob -- in one
            # physics frame, twice per stride.  A swinging leg's foot is lifted and near
            # the body, so its constraint is slack and does not bind; including it costs
            # nothing and makes the handover continuous, because at the moment of
            # handover the outgoing and incoming constraints are both evaluated and the
            # min passes smoothly from one to the other.
            hh = hip_h_nom
            for (a, st, goff, xoff) in ((a_n, st_n, 0.0, 0.0),
                                        (a_f, st_f, far_off[1], far_off[0])):
                dx = abs(a[0] - (Jr["hip"][0] + xoff))
                hh = min(hh, math.sqrt(max(Lmax * Lmax - dx * dx, 1.0)) - (a[1] - goff))
            if hh < hip_h_nom - 1e-6:
                clamped += 1
            hip_limit.append(hh)
            hip = (Jr["hip"][0], -hh)
            hip_f = (hip[0] + far_off[0], hip[1] + far_off[1])
            k_n, ok_n = two_bone_ik(hip, a_n, l1, l2)
            k_f, ok_f = two_bone_ik(hip_f, a_f, l1, l2)
            w = 2.0 * math.pi * ph
            frames.append(dict(t=tt, ph=ph, hip=hip, hip_f=hip_f, a_n=a_n, a_f=a_f,
                               k_n=k_n, k_f=k_f, phi_n=phi_n, phi_f=phi_f,
                               torso=lean + math.radians(1.6) * math.sin(w),
                               head=-0.55 * math.radians(1.6) * math.sin(w) - lean * 0.5,
                               arm_n=math.radians(arm_near_deg) * math.sin(w + math.pi),
                               arm_f=math.radians(arm_far_deg) * math.sin(w),
                               reach_ok=(ok_n and ok_f)))

        # THE HIP'S BOB SNAPPED, and it had to be fixed before anything could be
        # asserted against it.  The reach clamp is evaluated against whichever leg is
        # planted, and the two legs stand on ground lines 7.1 rig px apart (the depth
        # offset), so at each stance handover the binding constraint changes in one
        # frame and the hip stepped 2.12 rig px -- nearly the whole 2.32 px bob, in a
        # single physics frame, twice per stride.  Measured, not suspected.
        #
        # Smoothing the height outright is NOT safe: the clamp is what keeps the
        # planted foot within the leg's reach, and a hip smoothed UPWARD past it would
        # lift the foot off the ground -- trading a visible snap for an invisible
        # float.  So the smoothing is applied and then the limit is re-imposed:
        # hh = min(smoothed, limit).  The curve follows the limit's lower envelope
        # exactly where the leg is at full stretch, and rises smoothly instead of
        # stepping where the constraint hands over.  Reach is still guaranteed by
        # construction, because the last operation is the constraint itself.
        if hip_limit:
            M = len(hip_limit) - 1                      # the last key repeats the first
            k = max(1, int(round(HIP_SMOOTH_FRAC * M)))
            sm = []
            for i in range(M):
                w = [hip_limit[(i + q) % M] for q in range(-k, k + 1)]
                sm.append(sum(w) / len(w))
            sm.append(sm[0])
            hip_snap_before = max(abs(hip_limit[i + 1] - hip_limit[i]) for i in range(M))
            for i, f in enumerate(frames):
                hh2 = min(sm[i], hip_limit[i])
                f["hip"] = (f["hip"][0], -hh2)
                f["hip_f"] = (f["hip"][0] + far_off[0], -hh2 + far_off[1])
                f["k_n"], _ok = two_bone_ik(f["hip"], f["a_n"], l1, l2)
                f["k_f"], _ok2 = two_bone_ik(f["hip_f"], f["a_f"], l1, l2)
            hip_snap_after = max(abs(frames[i + 1]["hip"][1] - frames[i]["hip"][1])
                                 for i in range(M))
        else:
            hip_snap_before = hip_snap_after = 0.0

        # THE TABARD.  Conductor's physics spec: rigid above the belt; below it a damped
        # pendulum from the hip line, lagging 0.08-0.12 s, one settle per stride, never
        # upward.  Implemented as a BAKED lag: the near thigh's world angle, delayed
        # around the loop, three-tap smoothed (that is the damping), scaled to the hem
        # swing.  Baked rather than sprung so the movies and the foot-slide measurement
        # are reproducible frame for frame.
        thigh_w = [ang(f["hip"], f["k_n"]) - rest["thigh"] for f in frames[:-1]]

        def lagged(i):
            x = (i - lag_s / stride_T * N) % N
            i0, i1 = int(math.floor(x)) % N, int(math.ceil(x)) % N
            fr = x - math.floor(x)
            return thigh_w[i0] * (1 - fr) + thigh_w[i1] * fr

        raw = [lagged(i) for i in range(N)]
        damp = [(raw[(i - 1) % N] + 2 * raw[i] + raw[(i + 1) % N]) / 4.0 for i in range(N)]
        peak = max(abs(v) for v in damp) or 1.0
        for i, f in enumerate(frames):
            v = damp[i % N] / peak
            f["skirt_f"] = math.radians(tabard_deg_front) * v
            f["skirt_b"] = math.radians(tabard_deg_back) * v

        pollaxe = math.radians(pollaxe_deg)

        def local_tracks(fr):
            """world deltas -> local bone rotations (2D: world = parent world + local)."""
            d = {}
            d["torso"] = fr["torso"]
            d["head"] = fr["head"] - fr["torso"]
            d["skirt_b"] = fr["skirt_b"] - fr["torso"]
            d["skirt_f"] = fr["skirt_f"] - fr["torso"]
            d["arm_n_up"] = fr["arm_n"] - fr["torso"]
            d["arm_n_lo"] = 0.0
            # the haft holds its carried angle in WORLD space, as a carried haft does:
            # 0 = upright, and the run carries it sloped across the body
            d["hand"] = pollaxe - fr["arm_n"]
            d["arm_f_up"] = fr["arm_f"] - fr["torso"] + far_arm_base["arm_f_up"]
            d["arm_f_lo"] = far_arm_base["arm_f_lo"]
            d["hand_f"] = -fr["arm_f"] + far_arm_base["hand_f"]
            for tag, hipp, kn, an, phi in (
                    ("n", fr["hip"], fr["k_n"], fr["a_n"], fr["phi_n"]),
                    ("f", fr["hip_f"], fr["k_f"], fr["a_f"], fr["phi_f"])):
                th = ang(hipp, kn) - rest["thigh"]
                sh = ang(kn, an) - rest["shin"]
                d["leg_%s_th" % tag] = th
                d["leg_%s_sh" % tag] = sh - th
                # the sabaton's WORLD angle is phi (0 = the painted pose), so its
                # local rotation is phi minus the shin's world angle.  The old rig
                # wrote -sh here, which held the foot world-flat all cycle: a paddle.
                d["leg_%s_ft" % tag] = phi - sh
            return d

        tracks = {k: [] for k in local_tracks(frames[0])}
        hip_positions = []
        for fr in frames:
            for k, v in local_tracks(fr).items():
                tracks[k].append(v)
            hip_positions.append((fr["hip"][0] - Jr["hip"][0], fr["hip"][1] - Jr["hip"][1]))

        lo = min(q[1] for q in hip_positions)
        hi = max(q[1] for q in hip_positions)
        th_rng = math.degrees(max(tracks["leg_n_th"]) - min(tracks["leg_n_th"]))
        a_xs = [f["a_n"][0] for f in frames]
        phis = [f["phi_n"] for f in frames]
        # contact slide: the designated contact point's rig-local x must be the exact
        # straight line the roll defines.  Re-derived here from the FRAMES rather than
        # from the equation that produced them, so an error in the composition of
        # rotation and translation would show up as a nonzero residual.
        slide = 0.0
        for i in range(N + 1):
            ph = (ts[i] / stride_T) % 1.0
            if ph >= stance_frac:
                continue
            u = ph / stance_frac
            sg = s0 + (s1 - s0) * u
            c, tau = hull_at(SOLE_S, SOLE_P, SOLE_T, sg)
            r = rot(c, -tau)
            want = (sg - s0) - travel * u + (Jr["hip"][0] - roll_centre)
            slide = max(slide, abs((frames[i]["a_n"][0] + r[0]) - want))
        stats = {
            "px_s_canvas": px_s, "px_s_rig": v_rig, "stride_seconds": stride_T,
            "stance_fraction": stance_frac,
            "flight_fraction": round(max(0.0, 1.0 - 2.0 * stance_frac), 4),
            "body_travel_per_stride_canvas_px": px_s * stride_T,
            "step_length_canvas_px": px_s * stride_T / 2.0,
            "step_length_figure_heights": round(px_s * stride_T / 2.0 / (target_h * node_scale), 3),
            "ankle_sweep_rig_px": round(max(a_xs) - min(a_xs), 3),
            "ankle_sweep_canvas_px": round((max(a_xs) - min(a_xs)) * node_scale, 3),
            "body_travel_per_stance_rig_px": round(travel, 3),
            "sole_roll_rig_px": round(A_roll, 3),
            "sole_roll_fraction_of_stance_travel": round(A_roll / travel, 4),
            "plant_bias_rig_px": round(plant_bias, 3),
            "plant_bias_note": "fore-aft offset of the stance from a sweep centred on "
                               "the hip; solved to maximise the supporting leg's lowest "
                               "allowed hip height (-ve = the step sits further back)",
            "heel_toe": {
                "phi_heel_strike_deg": round(math.degrees(stance_pose(0.0, 0.0)[1]), 2),
                "phi_toe_off_deg": round(math.degrees(stance_pose(1.0, 0.0)[1]), 2),
                "phi_min_deg": round(math.degrees(min(phis)), 2),
                "phi_max_deg": round(math.degrees(max(phis)), 2),
                "ankle_height_heel_strike_rig_px": round(-stance_pose(0.0, 0.0)[0][1], 2),
                "ankle_height_mid_stance_rig_px": round(-stance_pose(0.5, 0.0)[0][1], 2),
                "ankle_height_toe_off_rig_px": round(-stance_pose(1.0, 0.0)[0][1], 2),
                "ankle_rise_at_toe_off_rig_px":
                    round(-stance_pose(1.0, 0.0)[0][1] + stance_pose(0.5, 0.0)[0][1], 2),
                "min_swing_ground_clearance_rig_px": round(min_clear, 3),
                "contact_slide_rig_px": round(slide, 5),
                "contact_local_rig_px": contact_keys,
                "ankle_stance_world_travel_canvas_px": round(
                    (lambda w: max(w) - min(w))(
                        [f["a_n"][0] * node_scale + px_s * stride_T * (f["ph"] % 1.0)
                         for f in frames if (f["ph"] % 1.0) < stance_frac]), 3),
                "ankle_travel_note":
                    "the ANKLE is no longer world-fixed during stance and must not be "
                    "asserted to be: the foot rolls, so the ankle travels forward over "
                    "it by about the sole's arc and rises 13 rig px at toe-off. That is "
                    "the gait working. The planted-point test is contact_local_rig_px.",
                "contact_local_note":
                    "per keyed frame: [x, y, planted] in the NEAR FOOT BONE's own frame "
                    "(origin = the ankle, rest orientation), plus its EXPECTED rig-local x. "
                    "While planted this point is "
                    "the one touching the ground, so its WORLD x is what must not move -- "
                    "not the ankle's. tools/probe_rig.gd transforms it through the live "
                    "bone chain and measures it in Godot.",
                "note": "phi is the sabaton's WORLD angle, 0 = the painted pose "
                        "(forefoot flat); -ve = toe up, +ve = toe down",
            },
            "swing_lift_rig_px": swing_lift,
            "hip_height_painted_rig": hip_h_paint, "hip_height_nominal_rig": hip_h_nom,
            "crouch_rig_px": round(max(q[1] for q in hip_positions), 3),
            "crouch_canvas_px": round(max(q[1] for q in hip_positions) * node_scale, 3),
            "hip_min_height_rig_px": round(hip_h_paint - max(q[1] for q in hip_positions), 3),
            "hip_snap_max_per_key_rig_px_before_smoothing": round(hip_snap_before, 4),
            "hip_snap_max_per_key_rig_px": round(hip_snap_after, 4),
            "hip_travel_rig_px": round(hi - lo, 3),
            "hip_travel_canvas_px": round((hi - lo) * node_scale, 3),
            "frames_hip_clamped_by_reach": clamped, "samples": N,
            "forward_lean_deg": lean_deg, "pollaxe_carry_deg": pollaxe_deg,
            "thigh_rotation_range_deg": round(th_rng, 2),
            "tabard": {"model": "baked lagged+damped pendulum from the near thigh",
                       "lag_s": lag_s, "hem_deg_front": tabard_deg_front,
                       "hem_deg_back": tabard_deg_back},
        }
        return ts, tracks, hip_positions, stats

    ts, walk_tracks, hip_pos, walk_stats = author_gait(
        px_s=walk_px_s, stride_T=stride_T, stance_frac=0.5, swing_lift=SWING_LIFT,
        nominal_drop=8.0, lean_deg=0.0, tabard_deg_front=6.0, tabard_deg_back=4.0,
        arm_near_deg=2.0, arm_far_deg=7.0, pollaxe_deg=0.0,
        far_arm_base=FAR_ARM_BASE, lag_s=0.10,
        # heel strike toe-up 18 deg, toe-off toe-down 30 -- the brief's band, and both
        # are angles this sabaton's own sole actually reaches (its hull runs -51..+38).
        roll_phi=(-18.0, 30.0), swing_clear=1.6)

    run_ts, run_tracks, run_hip_pos, run_stats = author_gait(
        px_s=run_px_s, stride_T=run_T, stance_frac=RUN_STANCE, swing_lift=RUN_LIFT,
        nominal_drop=4.0, lean_deg=RUN_LEAN_DEG, tabard_deg_front=11.0,
        tabard_deg_back=8.0, arm_near_deg=1.5, arm_far_deg=4.0,
        pollaxe_deg=RUN_POLLAXE_DEG, far_arm_base=RUN_FAR_ARM_BASE, lag_s=0.08,
        # A jog lands on the FOREFOOT, so the run rolls only the front of the sole:
        # it picks the ground up at -4 deg (all but flat) rather than on the heel, and
        # pushes off harder, to +34.
        roll_phi=(-4.0, 34.0), swing_clear=2.4,
        # 48 keys, not the walk's 32. The run's stance is only 0.165 s -- ten physics
        # frames -- and the leg angles are nonlinear in time, so linear interpolation
        # between 32 keys left up to 4.8 canvas px of apparent slide inside a stance
        # that is exact by construction. More keys, less interpolation error.
        N=48)

    # The plates were cut to cover a stated envelope of joint angles.  Check the gaits
    # actually stayed inside it; a gait that leaves it is covered by nothing and would
    # show up only as a hole on screen.
    env = []
    for nm, tr in (("walk", walk_tracks), ("run", run_tracks)):
        for tag in ("n", "f"):
            for jn, key, rng in (("knee", "leg_%s_sh" % tag, KNEE_PHI_RANGE),
                                 ("ankle", "leg_%s_ft" % tag, ANKLE_PHI_RANGE)):
                lo = math.degrees(min(tr[key]))
                hi = math.degrees(max(tr[key]))
                env.append({"clip": nm, "side": tag, "joint": jn,
                            "deg": [round(lo, 2), round(hi, 2)], "envelope": list(rng)})
    bad = [e for e in env if e["deg"][0] < e["envelope"][0] - 0.5
           or e["deg"][1] > e["envelope"][1] + 0.5]
    if bad:
        for e in bad:
            print("  ENVELOPE  %-4s %s %-5s reaches %7.2f..%7.2f deg, cut for %s"
                  % (e["clip"], e["side"], e["joint"], e["deg"][0], e["deg"][1],
                     e["envelope"]))
        raise SystemExit("joint angles outside the envelope the plates were cut for "
                         "-- widen the constant and rebuild")

    # ---------------- idle: 2.0 s breath, feet fixed ----------------
    IDLE_T, NI = 2.0, 24
    idle_tracks = {k: [] for k in walk_tracks}
    idle_hip = []
    for i in range(NI + 1):
        u = i / NI
        b = math.sin(2 * math.pi * u)
        idle_hip.append((0.0, -0.45 * (0.5 - 0.5 * math.cos(2 * math.pi * u))))
        t_d = math.radians(0.55) * b
        for k in idle_tracks:
            idle_tracks[k].append(0.0)
        idle_tracks["torso"][-1] = t_d
        idle_tracks["head"][-1] = math.radians(0.35) * b - t_d
        idle_tracks["arm_n_up"][-1] = math.radians(0.9) * b - t_d
        idle_tracks["hand"][-1] = -math.radians(0.9) * b + math.radians(0.3) * math.sin(4 * math.pi * u)
        idle_tracks["arm_f_up"][-1] = math.radians(0.7) * b - t_d + FAR_ARM_BASE["arm_f_up"]
        idle_tracks["arm_f_lo"][-1] = FAR_ARM_BASE["arm_f_lo"]
        idle_tracks["hand_f"][-1] = -math.radians(0.7) * b + FAR_ARM_BASE["hand_f"]
        idle_tracks["skirt_f"][-1] = math.radians(0.3) * b - t_d
        idle_tracks["skirt_b"][-1] = math.radians(0.25) * b - t_d
        # the far leg keeps the painting's own offset stance; both feet stay put
    idle_times = [IDLE_T * i / NI for i in range(NI + 1)]

    # =====================================================================
    # scene file
    # =====================================================================
    BONES = [
        # name, parent, rig position of the joint
        ("hip", None, Jr["hip"]),
        ("leg_n_th", "hip", Jr["hip"]),
        ("leg_n_sh", "leg_n_th", Jr["knee"]),
        ("leg_n_ft", "leg_n_sh", Jr["ankle"]),
        ("leg_f_th", "hip", (Jr["hip"][0] + far_off[0], Jr["hip"][1] + far_off[1])),
        ("leg_f_sh", "leg_f_th", (Jr["knee"][0] + far_off[0], Jr["knee"][1] + far_off[1])),
        ("leg_f_ft", "leg_f_sh", (Jr["ankle"][0] + far_off[0], Jr["ankle"][1] + far_off[1])),
        ("torso", "hip", Jr["torso"]),
        ("head", "torso", Jr["neck"]),
        ("skirt_b", "torso", Jr["skirt_back"]),
        ("skirt_f", "torso", Jr["skirt_front"]),
        ("arm_n_up", "torso", Jr["shoulder"]),
        ("arm_n_lo", "arm_n_up", Jr["elbow"]),
        ("hand", "arm_n_lo", Jr["grip"]),
        ("arm_f_up", "torso", (Jr["shoulder"][0] - 6 * s, Jr["shoulder"][1])),
        ("arm_f_lo", "arm_f_up", (Jr["elbow"][0] - 6 * s, Jr["elbow"][1])),
        ("hand_f", "arm_f_lo", (Jr["grip"][0] - 6 * s, Jr["grip"][1])),
    ]
    bpath, bpos = {}, {}
    for name, par, pos in BONES:
        bpath[name] = name if par is None else bpath[par] + "/" + name
        bpos[name] = pos

    # part -> (bone, z).  Painter's order, far side first.
    SPRITES = [
        # the backdrop is first and lowest: it can only ever be seen through a hole
        ("body_backdrop", "hip", -1),
        ("leg_far_foot", "leg_f_ft", 0), ("leg_far_shin", "leg_f_sh", 1),
        ("leg_far_thigh", "leg_f_th", 2),
        ("hand_far", "hand_f", 3), ("arm_far_lo", "arm_f_lo", 4),
        ("leg_near_foot", "leg_n_ft", 5), ("leg_near_shin", "leg_n_sh", 6),
        ("leg_near_thigh", "leg_n_th", 7),
        ("skirt_back", "skirt_b", 8), ("skirt_front", "skirt_f", 9),
        ("torso", "torso", 10), ("head", "head", 11),
        ("arm_near_lo", "arm_n_lo", 12), ("hand_pollaxe", "hand", 13),
    ]

    def fmt(v):
        """Always emit a FLOAT literal.

        Two traps here, both live.  (1) "%.5f" % 10.0 -> "10.00000", and
        .rstrip("0") eats the integer's zero too: 10.0 would be written as "1".
        (2) A value that trims to a bare "0" or "-1" parses out of the .tscn as an
        INT, and Godot's animation mixer then blends that track in integer space --
        the knight's thigh rotation came back as exactly -1.0 rad where the track
        interpolated -0.69832, and the leg pose snapped between whole radians while
        the animation clock ran perfectly.  The instrument said the animation was
        correct (it was) and the applied value was wrong.  A trailing ".0" costs two
        bytes per key and closes both.
        """
        s = "%.5f" % v
        if "." in s:
            s = s.rstrip("0")
            if s.endswith("."):
                s += "0"
        return s

    L = []
    n_res = len(SPRITES) + 4
    L.append('[gd_scene load_steps=%d format=3]\n' % n_res)
    for i, (nm, _, _) in enumerate(SPRITES):
        L.append('[ext_resource type="Texture2D" path="res://sprites_rig_E/%s.png" id="%d_%s"]'
                 % (nm, i + 1, nm))
    L.append('[ext_resource type="Script" path="res://scripts/knight_rig.gd" id="99_rig"]')
    L.append("")

    def anim(name, length, times, tracks, hip_positions):
        out = ['[sub_resource type="Animation" id="Animation_%s"]' % name,
               'resource_name = "%s"' % name,
               "length = %s" % fmt(length),
               "loop_mode = 1"]
        idx = 0
        out.append('tracks/%d/type = "value"' % idx)
        out.append("tracks/%d/imported = false" % idx)
        out.append("tracks/%d/enabled = true" % idx)
        out.append('tracks/%d/path = NodePath("Skel/%s:position")' % (idx, bpath["hip"]))
        out.append("tracks/%d/interp = 1" % idx)
        out.append("tracks/%d/loop_wrap = true" % idx)
        out.append("tracks/%d/keys = {" % idx)
        out.append('"times": PackedFloat32Array(%s),' % ", ".join(fmt(t) for t in times))
        out.append('"transitions": PackedFloat32Array(%s),' % ", ".join("1" for _ in times))
        out.append('"update": 0,')
        out.append('"values": [%s]' % ", ".join(
            "Vector2(%s, %s)" % (fmt(bpos["hip"][0] + dx), fmt(bpos["hip"][1] + dy))
            for dx, dy in hip_positions))
        out.append("}")
        idx += 1
        # EVERY bone gets a track in EVERY clip, including the ones that hold still.
        # Dropping a clip's all-zero tracks looks like a saving and is a bug: idle had
        # no leg tracks, so stopping mid-stride left the legs frozen in the walk pose
        # while the breath played on top -- the knight's sole sat 16 cell px off the
        # ground and the probe read it as a registration failure.  An animation must
        # state the whole pose, not the part of it that changes.
        for bone in sorted(tracks):
            vals = tracks[bone]
            out.append('tracks/%d/type = "value"' % idx)
            out.append("tracks/%d/imported = false" % idx)
            out.append("tracks/%d/enabled = true" % idx)
            out.append('tracks/%d/path = NodePath("Skel/%s:rotation")' % (idx, bpath[bone]))
            out.append("tracks/%d/interp = 1" % idx)
            out.append("tracks/%d/loop_wrap = true" % idx)
            out.append("tracks/%d/keys = {" % idx)
            out.append('"times": PackedFloat32Array(%s),' % ", ".join(fmt(t) for t in times))
            out.append('"transitions": PackedFloat32Array(%s),' % ", ".join("1" for _ in times))
            out.append('"update": 0,')
            out.append('"values": [%s]' % ", ".join(fmt(v) for v in vals))
            out.append("}")
            idx += 1
        return out

    L += anim("walk", stride_T, ts, walk_tracks, hip_pos) + [""]
    L += anim("run", run_T, run_ts, run_tracks, run_hip_pos) + [""]
    L += anim("idle", IDLE_T, idle_times, idle_tracks, idle_hip) + [""]
    L.append('[sub_resource type="AnimationLibrary" id="AnimationLibrary_rig"]')
    L.append('_data = {')
    L.append('"idle": SubResource("Animation_idle"),')
    L.append('"run": SubResource("Animation_run"),')
    L.append('"walk": SubResource("Animation_walk")')
    L.append('}')
    L.append("")

    L.append('[node name="KnightRigE" type="Node2D"]')
    L.append('script = ExtResource("99_rig")')
    L.append("")
    L.append('[node name="Skel" type="Skeleton2D" parent="."]')
    L.append("")
    for name, par, pos in BONES:
        parent = "Skel" if par is None else "Skel/" + bpath[par]
        ppos = (0.0, 0.0) if par is None else bpos[par]
        lx, ly = pos[0] - ppos[0], pos[1] - ppos[1]
        L.append('[node name="%s" type="Bone2D" parent="%s"]' % (name, parent))
        L.append("position = Vector2(%s, %s)" % (fmt(lx), fmt(ly)))
        L.append("rest = Transform2D(1, 0, 0, 1, %s, %s)" % (fmt(lx), fmt(ly)))
        L.append("")
    for nm, bone, z in SPRITES:
        c = meta[nm]["centre_rig"]
        bp = bpos[bone]
        L.append('[node name="S_%s" type="Sprite2D" parent="Skel/%s"]' % (nm, bpath[bone]))
        L.append("z_index = %d" % z)
        L.append("position = Vector2(%s, %s)" % (fmt(c[0] - bp[0]), fmt(c[1] - bp[1])))
        L.append("scale = Vector2(%s, %s)" % (fmt(sprite_scale), fmt(sprite_scale)))
        L.append('texture = ExtResource("%d_%s")' % ([x[0] for x in SPRITES].index(nm) + 1, nm))
        L.append("")
    L.append('[node name="Anim" type="AnimationPlayer" parent="."]')
    L.append('root_node = NodePath("..")')
    # PHYSICS callback mode (0), not the default idle (1).  The whole claim of this rig
    # is that the planted foot moves backward at exactly the speed the BODY moves
    # forward, and the body is moved by keeper.gd in _physics_process.  On the idle
    # clock the two run on different schedules: measured headless, the pose held still
    # for three frames and then jumped, and the planted foot drifted 55.6 px per stance
    # against 1.7 px when the same clip is sampled in lockstep.  A plant is a
    # physics-coupled property and has to be animated on the physics tick.
    L.append("callback_mode_process = 0")
    L.append('libraries = {')
    L.append('"": SubResource("AnimationLibrary_rig")')
    L.append('}')
    L.append("")
    OUT_SCN.write_text("\n".join(L))

    # ---------------- report ----------------
    rep = {
        "note": "C-9 probe R-C9-34: 2D puppet rig of the E knight, cut from seed_E.png.",
        "seed": {"crown": crown, "sole": sole, "figure_h_px": sole - crown},
        "ref_cell_idle_E": {"crown": ref_crown, "sole": ref_sole, "figure_h_px": target_h,
                            "foot_band_cx": ref_foot_cx},
        "transform": {"seed_to_cell": s, "node_scale": node_scale,
                      "pivot_cell": pivot, "sprite_scale": sprite_scale,
                      "png_texels_per_seed_px": f_px, "texels_per_canvas_px": RES,
                      "ref_foot_cx_cell": ref_foot_cx, "seed_foot_cx": seed_foot_cx},
        "joints_seed": J, "joints_rig": Jr,
        "far_side": {"offset_seed_px": FAR_OFFSET_SEED, "offset_rig_px": far_off,
                     "darken": FAR_DARKEN},
        "parts": meta, "fills": fills, "stopped": [],
        "dropped_px": dropped,
        "walk": walk_stats,
        "run": run_stats,
        "idle": {"seconds": IDLE_T, "samples": NI},
        "joint_envelope": env,
        "hip_cap_seed_px": HIP_CAP_SEED,
        "knee_disc_seed_px": KNEE_DISC_SEED,
        "ankle_disc_seed_px": ANKLE_DISC_SEED,
        "sole_tangent_deg_heel_to_toe": [sole_deg[0], sole_deg[-1]],
    }
    OUT_JSON.write_text(json.dumps(rep, indent=1))
    print("rig scale seed->cell %.6f   sprite_scale %.5f" % (s, sprite_scale))
    print("figure height in cell px %.2f (target %.2f)" % ((sole - crown) * s, target_h))
    print("thigh %.2f  shin %.2f  ankle_h %.2f rig px  (painted hip height %.2f)"
          % (l1, l2, ankle_h, hip_h_paint))
    for nm, s in (("walk", walk_stats), ("run", run_stats)):
        print("  %-4s %6.1f px/s  stride %.4f s  stance %.2f  flight %.2f"
              % (nm, s["px_s_canvas"], s["stride_seconds"], s["stance_fraction"],
                 s["flight_fraction"]))
        print("       step %6.2f canvas px (%.2f figure heights)  ankle sweep %6.2f canvas px"
              % (s["step_length_canvas_px"], s["step_length_figure_heights"],
                 s["ankle_sweep_canvas_px"]))
        print("       hip travel %5.2f rig / %5.2f canvas px   reach-clamped %d/%d   "
              "thigh range %5.1f deg   lean %.0f deg   haft %.0f deg"
              % (s["hip_travel_rig_px"], s["hip_travel_canvas_px"],
                 s["frames_hip_clamped_by_reach"], s["samples"] + 1,
                 s["thigh_rotation_range_deg"], s["forward_lean_deg"],
                 s["pollaxe_carry_deg"]))
    print("wrote", OUT_SCN, OUT_JSON)


if __name__ == "__main__":
    main()
