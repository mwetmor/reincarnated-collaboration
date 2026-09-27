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

    parts["leg_near_thigh"] = clone_up(parts["leg_near_thigh"], 34)
    fills["leg_near_thigh"] = ("top band cloned 34 rows upward -- the cuisse's hip end is "
                               "under the tabard hem in the still")
    parts["arm_near_lo"] = clone_up(parts["arm_near_lo"], 14)
    fills["arm_near_lo"] = ("couter end cloned 14 rows upward -- the upper arm is behind "
                            "the surcoat in the still")
    for a, b in [("leg_near_thigh", "leg_far_thigh"), ("leg_near_shin", "leg_far_shin"),
                 ("leg_near_foot", "leg_far_foot")]:
        parts[b] = darken(parts[a])
        fills[b] = "copy of %s, value x%.2f (symmetric harness; far side in shade)" % (a, FAR_DARKEN)
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

    def author_gait(px_s, stride_T, stance_frac, swing_lift, nominal_drop,
                    lean_deg, tabard_deg_front, tabard_deg_back, arm_near_deg,
                    arm_far_deg, pollaxe_deg, far_arm_base, lag_s, N=32):
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
        half_step = v_rig * stride_T * stance_frac / 2.0
        hip_h_nom = hip_h_paint - nominal_drop
        lean = math.radians(lean_deg)
        ts = [stride_T * i / N for i in range(N + 1)]

        def ankle_traj(phase, ground_y, x_off):
            """0 .. stance_frac = PLANTED; the rest is swing (and flight, if any).

            The sweep is centred on the hip's own x, so mid-stance puts the ankle under
            the hip.  While planted the ankle's x is a straight line in time at exactly
            -px_s: the plant is not approximated, it IS the parameterisation.
            """
            cx = Jr["hip"][0] + x_off
            if phase < stance_frac:
                u = phase / stance_frac
                return (cx + half_step - 2.0 * half_step * u, ground_y - ankle_h), True
            u = (phase - stance_frac) / (1.0 - stance_frac)
            e = u * u * (3 - 2 * u)                  # smoothstep: stiff, no overshoot
            lift = math.sin(math.pi * u) ** 1.4 * swing_lift
            return (cx - half_step + 2.0 * half_step * e, ground_y - ankle_h - lift), False

        frames = []
        clamped = 0
        for tt in ts:
            ph = (tt / stride_T) % 1.0
            a_n, st_n = ankle_traj(ph, 0.0, 0.0)
            a_f, st_f = ankle_traj((ph + 0.5) % 1.0, far_off[1], far_off[0])
            # The hip sits at the nominal height unless the SUPPORTING leg cannot reach
            # its ankle from there.  Solving hh out of |hip - ankle| <= Lmax, with the
            # far leg's own ground line folded in via goff:
            #     hh <= sqrt(Lmax^2 - dx^2) - (ankle_y - goff)
            # So the bob/bounce is DERIVED FROM THE PLANT, never added on top of it.
            hh = hip_h_nom
            for (a, st, goff, xoff) in ((a_n, st_n, 0.0, 0.0),
                                        (a_f, st_f, far_off[1], far_off[0])):
                if not st:
                    continue
                dx = abs(a[0] - (Jr["hip"][0] + xoff))
                hh = min(hh, math.sqrt(max(Lmax * Lmax - dx * dx, 1.0)) - (a[1] - goff))
            if hh < hip_h_nom - 1e-6:
                clamped += 1
            hip = (Jr["hip"][0], -hh)
            hip_f = (hip[0] + far_off[0], hip[1] + far_off[1])
            k_n, ok_n = two_bone_ik(hip, a_n, l1, l2)
            k_f, ok_f = two_bone_ik(hip_f, a_f, l1, l2)
            w = 2.0 * math.pi * ph
            frames.append(dict(t=tt, ph=ph, hip=hip, hip_f=hip_f, a_n=a_n, a_f=a_f,
                               k_n=k_n, k_f=k_f,
                               torso=lean + math.radians(1.6) * math.sin(w),
                               head=-0.55 * math.radians(1.6) * math.sin(w) - lean * 0.5,
                               arm_n=math.radians(arm_near_deg) * math.sin(w + math.pi),
                               arm_f=math.radians(arm_far_deg) * math.sin(w),
                               reach_ok=(ok_n and ok_f)))

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
            for tag, hipp, kn, an in (("n", fr["hip"], fr["k_n"], fr["a_n"]),
                                      ("f", fr["hip_f"], fr["k_f"], fr["a_f"])):
                th = ang(hipp, kn) - rest["thigh"]
                sh = ang(kn, an) - rest["shin"]
                d["leg_%s_th" % tag] = th
                d["leg_%s_sh" % tag] = sh - th
                d["leg_%s_ft" % tag] = -sh   # sabaton stays flat to the ground: stiff
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
        stats = {
            "px_s_canvas": px_s, "px_s_rig": v_rig, "stride_seconds": stride_T,
            "stance_fraction": stance_frac,
            "flight_fraction": round(max(0.0, 1.0 - 2.0 * stance_frac), 4),
            "body_travel_per_stride_canvas_px": px_s * stride_T,
            "step_length_canvas_px": px_s * stride_T / 2.0,
            "step_length_figure_heights": round(px_s * stride_T / 2.0 / (target_h * node_scale), 3),
            "ankle_sweep_rig_px": 2 * half_step,
            "ankle_sweep_canvas_px": 2 * half_step * node_scale,
            "swing_lift_rig_px": swing_lift,
            "hip_height_painted_rig": hip_h_paint, "hip_height_nominal_rig": hip_h_nom,
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
        far_arm_base=FAR_ARM_BASE, lag_s=0.10)

    run_ts, run_tracks, run_hip_pos, run_stats = author_gait(
        px_s=run_px_s, stride_T=run_T, stance_frac=RUN_STANCE, swing_lift=RUN_LIFT,
        nominal_drop=4.0, lean_deg=RUN_LEAN_DEG, tabard_deg_front=11.0,
        tabard_deg_back=8.0, arm_near_deg=1.5, arm_far_deg=4.0,
        pollaxe_deg=RUN_POLLAXE_DEG, far_arm_base=RUN_FAR_ARM_BASE, lag_s=0.08,
        # 48 keys, not the walk's 32. The run's stance is only 0.165 s -- ten physics
        # frames -- and the leg angles are nonlinear in time, so linear interpolation
        # between 32 keys left up to 4.8 canvas px of apparent slide inside a stance
        # that is exact by construction. More keys, less interpolation error.
        N=48)

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
