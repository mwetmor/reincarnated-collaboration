#!/usr/bin/env python3
"""C-9 T10-2 step 1 -- THE FROST KING'S BARROW, FULL AREA: the layout, from the spec table.

Contract: agentic_orchestration/gandalf/notes/2026-09-29-barrow-full-area-blockout-spec.md.
This file turns that table into ONE machine-readable layout that everything downstream reads:
the Godot scene builds from it, the top-down map is drawn from it, and the acceptance numbers
are measured against it. Nothing about the layout is decided anywhere else.

WHAT IS THE SPEC'S AND WHAT IS MINE is kept apart in the output, because the acceptance line
"every placement within 0.05 m of the spec, or the deviation reported" needs to know which
number came from gandalf's table:
  * `spec_uv`  -- the table's own number, verbatim (null for a piece the table does not place);
  * `uv`       -- the point actually used. Equal to spec_uv unless a deviation says otherwise.
Pieces the table implies but does not place (grove members, the two logs of the fallen tree,
the door posts, the shore-rock chain, the thicket band along the bounds) carry `derived_from`.

FRAME. (u, v) are true metres on the ground, +u screen-right and +v up-screen, both from the
play camera's own basis (pitch 52.95354112560294, yaw 47) projected onto the ground:
    u_hat = ( cos47, 0, -sin47)      v_hat = (-sin47, 0, -cos47)
    world = origin + u*u_hat + v*v_hat, origin = the arena centre = world (0, 0, 0).
The scene ASSERTS this basis against its live camera rather than trusting this docstring.

Outputs (all regenerated on every run; the PNGs are gitignored and this script is their source):
    ../barrow_full_layout.json            the design layout (finalize.py merges the built numbers in)
    ../godot/data/barrow_full_layout.json the copy the scene reads
    ../godot/data/barrow_full_splat.bin   the ground-tint weight map (world-xz raster), PNG bytes
"""
import hashlib
import json
import math
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
GODOT = ROOT / "godot"

# --- the frame -----------------------------------------------------------------------------
PPM = 100.617553710938                    # px per metre across the screen (the project's own)
PITCH_DEG = 52.95354112560294             # R-C9-68
YAW_DEG = 47.0
SP = math.sin(math.radians(PITCH_DEG))
CP = math.cos(math.radians(PITCH_DEG))
PX_UP = PPM * SP                          # px per ground metre up-screen = 80.3076
CY = math.cos(math.radians(YAW_DEG))
SY = math.sin(math.radians(YAW_DEG))
GUIDE_PX = (4096, 2560)
U_HALF = GUIDE_PX[0] / 2.0 / PPM          # 20.3543 m
V_HALF = GUIDE_PX[1] / 2.0 / PX_UP        # 15.9387 m
CHUNK = {"cols": 3, "rows": 3, "canvas_px": [1536, 1024], "stride_px": [1280, 768]}


def uv_to_xz(u, v):
    return (u * CY - v * SY, -u * SY - v * CY)


def xz_to_uv(x, z):
    # the (u,v)->(x,z) matrix is symmetric and orthogonal, so it is its own inverse
    return (x * CY - z * SY, -x * SY - z * CY)


def uv_to_guide_px(u, v, h=0.0):
    """A point at height h over ground (u, v), in guide pixels (x right, y down)."""
    return (GUIDE_PX[0] / 2.0 + u * PPM, GUIDE_PX[1] / 2.0 - v * PX_UP - h * PPM * CP)


def r3(x):
    return round(float(x), 4)


# --- asset sizes: barrow_assets.json (HEAD) + kit_assets.json + the welded AABBs -------------
BA = json.loads((HERE / "barrow_assets.src.json").read_text())["models"]
KA = json.loads((HERE / "kit_assets.src.json").read_text())["models"]
PITCH_STRETCH = 1.0 / CP                  # 1.660: the T10 Y stretch, before the normalise

# welded-v2 glTF AABBs (reduce_v2_report.json), for the PRE-BUILD footprint estimate only. The
# built sizes come from the LOADED AABB in Godot (the brief: "size from the LOADED AABB, not
# raw_aabb_m"), and finalize.py measures against those.
RV2 = json.loads((ROOT.parent / "t10_barrow/reduced_v2/reduce_v2_report.json").read_text())["assets"]


def est_footprint(cls):
    """(across_u, deep_v) of an upright model at the manifest's own yaw, metres. Estimate."""
    if cls in KA:
        s = KA[cls]["size_m"]
        return s[0], s[2]
    a = RV2[cls]["aabb_gltf_v2"]
    raw = [a[1][i] - a[0][i] for i in range(3)]
    m = BA[cls]
    if m["axis"] == "across":
        k = m["height_m"] / max(raw[0], raw[2])
    else:
        k = m["height_m"] / (raw[1] * (PITCH_STRETCH if m["pitch_correct"] else 1.0))
    return raw[0] * k, raw[2] * k


# --- the spec table, verbatim ----------------------------------------------------------------
MOUND = {"centre": (0.0, 11.0), "axes": (12.0, 7.0), "rise": 2.6}
DOOR_UV = (0.0, 7.5)
RING = {"centre": (0.0, 2.0), "r": 9.0}
RING_STONES = [  # theta (clockwise from +v), class, note
    (155, "stone_tall", "gate stone"), (-155, "stone_tall", "gate stone"),
    (125, "stone_mid", ""), (-125, "stone_mid", ""),
    (95, "stone_short", ""), (-95, "stone_tall", "FALLEN, lying outward"),
    (65, "stone_tall", "the raven's perch"), (-65, "stone_tall", ""),
    (40, "stone_mid", ""), (-40, "stone_mid", ""),
]
ARENA = {"centre": (0.0, 1.0), "r": 7.0}
PATH = {"points": [(0.0, -6.2), (-1.0, -10.0), (-3.0, -16.0)], "width": 4.0}
TARN = {"centre": (-13.0, -5.0), "axes": (12.0, 9.0)}
OUTCROPS = [(17, -12), (18, -3), (17, 6), (10, -15), (-19, -13), (-19, 4), (-13, 13), (13, 13)]
COVER = {"uv": (-12.0, 3.0), "size": (3.0, 2.0), "h": 1.4}
GROVES = {"G1": ((7.0, -11.0), 5), "G2": ((-10.0, 9.5), 4), "G3": ((13.0, -6.0), 4),
          "G4": ((10.0, 12.0), 3)}
FALLEN_TREE = (-7.0, -12.0)
GRAVES = [(-7.0, 11.0), (7.0, 11.0)]
CAIRNS = [(2.5, -9.0), (-5.0, -14.0), (-16.0, 1.0)]
ENTRY_GAP = [(-5.0, -16.0), (-1.0, -16.0)]

# --- the choices the table leaves to the builder (each one stated) --------------------------
# RING STONE FACING. "Carved faces toward -v (+-30 deg) so the carvings read at the play
# camera." barrow_assets.json's yaw IS the camera-facing one (matched to the identity plate
# through the play camera), so the carved face points at -v at the manifest yaw. Each stone is
# then turned 20 deg TOWARD THE RING'S AXIS -- as close to facing the ring centre as the
# tolerance allows -- and 20 rather than 30 because the manifest yaws are 15-degree-quantised
# silhouette matches: 20 + 7.5 still lands inside 30.
RING_INWARD_TURN_DEG = 20.0
# THE DOOR. Posts under the lintel's ends, 0.90 m either side of its centre along its own long
# axis: the 2.28 m lintel overhangs each ~0.43 m post by ~0.05 m. Clear opening ~1.37 m, his
# capsule is 0.70 m.
POST_OFFSET_M = 0.90
# THE PASSAGE: "3 steps down (0.2 m each) inside". An open cutting 1.40 m wide behind the door,
# threshold at y = 0, three 0.2 m risers 0.4 m apart, then the dark mouth of the passage.
PASSAGE = {"half_w": 0.70, "v0": 7.5, "v_mouth": 9.0, "threshold_to": 7.9,
           "risers_v": [7.9, 8.3, 8.7], "riser_m": 0.2,
           "_walk": "a 31-degree ramp collider under the visual steps; move_and_slide does not step UP a riser"}
BIRCH_TRUNK_R = 0.22                      # collider: the trunk, not the crown
# grove members, as offsets from the grove point; each set sums to (0, 0) so the grove's
# centroid IS the spec's point. Clusters, not rows.
GROVE_OFFSETS = {
    "G1": [(-1.35, 0.55), (0.25, 1.45), (1.55, 0.35), (0.35, -0.95), (-0.80, -1.40)],
    "G2": [(-1.00, 0.95), (0.85, 1.05), (-0.45, -0.95), (0.60, -1.05)],
    "G3": [(-1.05, 0.85), (0.95, 1.25), (1.10, -0.85), (-1.00, -1.25)],
    "G4": [(-1.25, -0.35), (0.25, 0.85), (1.00, -0.50)],
}
BIRCH_YAWS = [315, 0, 270, 45, 225, 90, 180, 135]   # varied per member, deterministic
# THE FALLEN TREE: two 2.6 m kit logs meeting at the table's point, laid along the tarn's near
# shore (the rim's tangent nearest the point is 32 deg), with a 6-degree kink so it reads as one
# trunk broken in two rather than two identical logs in a line.
LOG_ANGLES_DEG = (29.0, 35.0)
LOG_LEN = KA["log"]["size_m"][0]          # 2.6
# OUTCROPS: footprint (long, short) m, height m. "Layered masses, 4-6 m footprint, 1.5-3 m tall".
# Lower where they stand near the camera edge, so they hide less of the ground behind them.
OUTCROP_DIMS = [(5.0, 3.8, 2.2), (5.6, 4.2, 3.0), (5.0, 3.8, 2.5), (4.6, 3.6, 1.8),
                (5.0, 3.8, 2.0), (5.4, 4.0, 2.6), (5.0, 3.8, 2.8), (4.4, 3.6, 2.4)]

# --- tints (sRGB). The spec's § 4 encoding, one colour per class -----------------------------
TINTS = {
    "snow": [0.860, 0.840, 0.800],        # light warm grey
    "path": [0.580, 0.520, 0.450],        # darker brown-grey band
    "rock": [0.560, 0.555, 0.550],        # splat slot kept for the shader; unused on the ground
    "shrub": [0.520, 0.515, 0.390],       # muted green-brown patches
    "ice": [0.700, 0.775, 0.840],         # pale blue-grey
    "hero_grey": [0.600, 0.590, 0.570],   # the real models, flat grey
    "primitive_grey": [0.500, 0.480, 0.460],  # outcrops, shore rock: primitives
    "mound": [0.745, 0.725, 0.665],       # the barrow mound: a primitive, earth under thin snow
    "passage_dark": [0.120, 0.110, 0.105],
}


# --- geometry helpers ------------------------------------------------------------------------
def ring_uv(theta):
    a = math.radians(theta)
    return (RING["centre"][0] + RING["r"] * math.sin(a), RING["centre"][1] + RING["r"] * math.cos(a))


def rot(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def hull2d(pts):
    pts = sorted(set((round(p[0], 6), round(p[1], 6)) for p in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def rng_for(seed):
    return np.random.default_rng(seed)


def irregular_poly(centre, long, short, ang, rng, n=9, jit_r=0.07, jit_a=0.12):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n + rng.uniform(-jit_a, jit_a)
        r = 1.0 + rng.uniform(-jit_r, jit_r)
        p = (0.5 * long * r * math.cos(a), 0.5 * short * r * math.sin(a))
        p = rot(p, ang)
        pts.append((centre[0] + p[0], centre[1] + p[1]))
    return hull2d(pts)


def scale_poly(poly, s, about=None, shift=(0.0, 0.0), turn=0.0):
    if about is None:
        about = (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))
    out = []
    for p in poly:
        q = rot(((p[0] - about[0]) * s, (p[1] - about[1]) * s), turn)
        out.append((about[0] + q[0] + shift[0], about[1] + q[1] + shift[1]))
    return out


def centroid(poly):
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


# --- the bounds polygon ----------------------------------------------------------------------
# "A polygon through the outcrops and thickets, with the entry gap at (-5...-1, -16)." Through
# each outcrop's centre (half of every mass stands outside, so the edge is rock, not a line),
# through groves G4 and G2 beside the mound, and through the mound's own body (it is solid, so
# the wall inside it is never reached). Counter-clockwise from the entry's right post.
BOUNDS = [(-1.0, -16.0), (10.0, -15.0), (17.0, -12.0), (18.0, -3.0), (17.0, 6.0), (13.0, 13.0),
          (10.0, 12.0), (0.0, 12.5), (-6.0, 12.5), (-10.0, 9.5), (-13.0, 13.0), (-19.0, 4.0),
          (-19.0, -13.0), (-5.0, -16.0)]
# (-6, 12.5) is there for the WEST GRAVE MARKER: a straight wall from the mound to G2 crosses
# v = 10.4 at u = -7, which put (-7, 11) outside the play area while its twin at (7, 11) was
# inside. One vertex behind the mound's flank brings both in; the wall still runs behind G2.
# the entry is closed for the greybox by an EXIT line at the frame's bottom edge -- the level
# transition of the eventual game. It is the last edge, (-5,-16) -> (-1,-16).


def outward_normal_at_vertex(i):
    """Outward normal of the CCW polygon at vertex i (bisector of its two edges' normals)."""
    n = len(BOUNDS)
    a, b, c = BOUNDS[i - 1], BOUNDS[i], BOUNDS[(i + 1) % n]
    e1 = (b[0] - a[0], b[1] - a[1])
    e2 = (c[0] - b[0], c[1] - b[1])

    def nrm(e):   # outward normal of a CCW edge = the edge turned clockwise
        L = math.hypot(*e)
        return (e[1] / L, -e[0] / L)
    n1, n2 = nrm(e1), nrm(e2)
    s = (n1[0] + n2[0], n1[1] + n2[1])
    L = math.hypot(*s)
    return (s[0] / L, s[1] / L)


# --- build the placement list ----------------------------------------------------------------
def build():
    P = []            # placements
    dev = []          # deviations from the spec, each with its reason

    # MOUND
    P.append({"id": "mound", "piece": "barrow mound", "class": "mound", "kind": "structure",
              "spec_uv": list(MOUND["centre"]), "uv": list(MOUND["centre"]),
              "semi_axes": [MOUND["axes"][0] / 2, MOUND["axes"][1] / 2], "rise_m": MOUND["rise"],
              "profile": "h = rise * (1 - rho^2)^0.65, smooth: a KERBED barrow -- steep at the foot, rounded on top; the foot's vertices lie on the ellipse",
              "_profile_why": "the spec fixes the footprint (12 x 7 m) and the rise (2.6 m), not the profile. barrow_world's 1.15 meets the floor tangentially and reads as a tent-flat hump at the play camera; 0.65 keeps both numbers and puts the flanks up, which is what a barrow is",
              "exponent": 0.65, "tint": "mound", "walkable": False,
              "collider": "vertical box ring at rho 0.97, the passage mouth left open",
              "passage": PASSAGE})

    # DOOR: lintel + two posts
    lint = BA["lintel"]
    ang = math.radians(lint["yaw_deg"])
    # the lintel's long (local z) axis in world, then in (u, v)
    ax_world = (math.sin(ang), math.cos(ang))
    ax_uv = xz_to_uv(*ax_world)
    P.append({"id": "door_lintel", "piece": "door lintel", "class": "lintel", "kind": "model",
              "glb": "res://models/barrow/lintel.glb", "spec_uv": list(DOOR_UV), "uv": list(DOOR_UV),
              "yaw_world_deg": lint["yaw_deg"], "axis": "across", "target_m": lint["height_m"],
              "pitch_correct": True, "width_m": None, "hull_px": 1.1, "collider": "hull",
              "stack_on": ["door_post_L", "door_post_R"],
              "_faces": "yaw 135 is the manifest's camera-facing yaw; its long axis then lies %.1f deg off +u" %
                        math.degrees(math.atan2(ax_uv[1], ax_uv[0]))})
    for side, sgn in (("L", -1.0), ("R", 1.0)):
        uv = (DOOR_UV[0] + sgn * POST_OFFSET_M * ax_uv[0], DOOR_UV[1] + sgn * POST_OFFSET_M * ax_uv[1])
        P.append({"id": "door_post_" + side, "piece": "door post " + side, "class": "post",
                  "kind": "model", "glb": "res://models/barrow/post.glb", "spec_uv": None,
                  "uv": [r3(uv[0]), r3(uv[1])], "derived_from": "door_lintel: under its ends, %.2f m along its long axis" % POST_OFFSET_M,
                  "yaw_world_deg": BA["post"]["yaw_deg"], "axis": "height",
                  "target_m": BA["post"]["height_m"], "pitch_correct": True, "width_m": None,
                  "hull_px": 1.1, "collider": "hull"})

    # RING
    for theta, cls, note in RING_STONES:
        uv = ring_uv(theta)
        sid = "ring_%s%d" % ("p" if theta > 0 else "m", abs(theta))
        turn = -RING_INWARD_TURN_DEG if uv[0] > 0 else RING_INWARD_TURN_DEG
        e = {"id": sid, "piece": "ring stone %+d" % theta + (" (%s)" % note if note else ""),
             "class": cls, "kind": "model", "glb": "res://models/barrow/%s.glb" % cls,
             "spec_uv": [r3(uv[0]), r3(uv[1])], "uv": [r3(uv[0]), r3(uv[1])], "theta_deg": theta,
             "axis": "height", "target_m": BA[cls]["height_m"], "pitch_correct": True,
             "width_m": None, "hull_px": 1.1, "collider": "hull"}
        if theta == -95:
            # FALLEN AND LYING OUTWARD: base in the socket, top toward the outward radial, the
            # carved face turned to the centre before the fall so it lies FACE-UP. The placement
            # point is the SOCKET (the table's point); the stone's centre lies 1.35 m outward.
            out = (uv[0] - RING["centre"][0], uv[1] - RING["centre"][1])
            L = math.hypot(*out)
            out = (out[0] / L, out[1] / L)
            # the carved face starts at -v; turn it to the inward radial (-out). +beta turns -v
            # toward +u, so beta = angle from (0,-1) to (-out) measured toward +u.
            inward = (-out[0], -out[1])
            beta = math.degrees(math.atan2(inward[0], -inward[1]))
            e["yaw_world_deg"] = r3(BA[cls]["yaw_deg"] + beta)
            e["tip"] = {"outward_uv": [r3(out[0]), r3(out[1])], "face": "up",
                        "placement_point": "the socket (the stone's base end)",
                        "sink_m": 0.06}
        else:
            e["yaw_world_deg"] = r3((BA[cls]["yaw_deg"] + turn) % 360.0)
            e["_facing"] = "manifest yaw %g (carved face at -v) turned %+g toward the ring axis" % (
                BA[cls]["yaw_deg"], turn)
        P.append(e)

    # RAVEN on the +65 stone
    P.append({"id": "raven", "piece": "raven", "class": "raven", "kind": "model",
              "glb": "res://models/barrow/raven.glb", "spec_uv": None, "uv": None,
              "perch_on": "ring_p65", "yaw_world_deg": 200.0, "axis": "height", "target_m": 0.28,
              "pitch_correct": True, "width_m": None, "hull_px": 1.1, "collider": "none",
              "derived_from": "the table: 'on the +65 stone'; size 0.28 m and yaw 200 from T10_HANDOFF / barrow_world"})

    # OUTCROPS (primitives, layered)
    for i, c in enumerate(OUTCROPS):
        vi = BOUNDS.index((float(c[0]), float(c[1])))
        on = outward_normal_at_vertex(vi)
        tang = math.atan2(on[0], -on[1])          # the boundary's tangent: the normal turned 90
        long, short, h = OUTCROP_DIMS[i]
        rng = rng_for(1000 + i)
        base = irregular_poly(c, long, short, tang, rng)
        bc = centroid(base)
        # re-centre the base so its centroid IS the table's point
        base = [(p[0] - bc[0] + c[0], p[1] - bc[1] + c[1]) for p in base]
        mid = scale_poly(base, 0.70, shift=(on[0] * 0.15 * long, on[1] * 0.15 * long),
                         turn=math.radians(rng.uniform(6, 14)))
        top = scale_poly(base, 0.42, shift=(on[0] * 0.26 * long, on[1] * 0.26 * long),
                         turn=math.radians(-rng.uniform(5, 12)))
        layers = [{"poly_uv": [[r3(p[0]), r3(p[1])] for p in base], "y0": 0.0, "y1": r3(0.45 * h), "top_scale": 0.90},
                  {"poly_uv": [[r3(p[0]), r3(p[1])] for p in mid], "y0": r3(0.45 * h), "y1": r3(0.80 * h), "top_scale": 0.88},
                  {"poly_uv": [[r3(p[0]), r3(p[1])] for p in top], "y0": r3(0.80 * h), "y1": r3(h), "top_scale": 0.80}]
        P.append({"id": "outcrop_%d" % (i + 1), "piece": "outcrop %d" % (i + 1), "class": "outcrop",
                  "kind": "primitive", "spec_uv": [float(c[0]), float(c[1])], "uv": [float(c[0]), float(c[1])],
                  "footprint_m": [long, short], "height_m": h, "outward_uv": [r3(on[0]), r3(on[1])],
                  "layers": layers, "collider": "convex hull per layer",
                  "_shape": "three stacked slabs stepping OUT of the play area, so the inner face reads as a stepped rock face"})

    # COVER OUTCROP
    rng = rng_for(2000)
    cb = irregular_poly(COVER["uv"], COVER["size"][0], COVER["size"][1], 0.0, rng, n=8, jit_r=0.05)
    cc = centroid(cb)
    cb = [(p[0] - cc[0] + COVER["uv"][0], p[1] - cc[1] + COVER["uv"][1]) for p in cb]
    ct = scale_poly(cb, 0.68, turn=math.radians(8))
    P.append({"id": "cover_outcrop", "piece": "cover outcrop (the tarn fight)", "class": "outcrop",
              "kind": "primitive", "spec_uv": list(COVER["uv"]), "uv": list(COVER["uv"]),
              "footprint_m": list(COVER["size"]), "height_m": COVER["h"],
              "layers": [{"poly_uv": [[r3(p[0]), r3(p[1])] for p in cb], "y0": 0.0, "y1": 0.8, "top_scale": 0.9},
                         {"poly_uv": [[r3(p[0]), r3(p[1])] for p in ct], "y0": 0.8, "y1": COVER["h"], "top_scale": 0.85}],
              "collider": "convex hull per layer"})

    # SHORE ROCK: the tarn's W and SW rim (the table: "West and south-west rim is shore rock
    # (non-walkable)"). A chain of low slabs hugging the rim OUTSIDE the ice, overlapping so no
    # gap is wider than his 0.70 m capsule.
    tc, (ta, tb) = TARN["centre"], (TARN["axes"][0] / 2, TARN["axes"][1] / 2)
    for k, t in enumerate(range(150, 250, 12)):
        tr = math.radians(t)
        rim = (tc[0] + ta * math.cos(tr), tc[1] + tb * math.sin(tr))
        nrm = (math.cos(tr) / ta, math.sin(tr) / tb)
        L = math.hypot(*nrm)
        nrm = (nrm[0] / L, nrm[1] / L)
        tang = math.atan2(nrm[0], -nrm[1])
        rngk = rng_for(3000 + k)
        long = 1.9 + rngk.uniform(-0.2, 0.3)
        short = 1.25 + rngk.uniform(-0.15, 0.15)
        h = 0.55 + rngk.uniform(-0.12, 0.30)
        cen = (rim[0] + nrm[0] * (0.5 * short + 0.05), rim[1] + nrm[1] * (0.5 * short + 0.05))
        base = irregular_poly(cen, long, short, tang, rngk, n=8, jit_r=0.08)
        lay = [{"poly_uv": [[r3(p[0]), r3(p[1])] for p in base], "y0": 0.0, "y1": r3(h * (0.7 if k % 2 == 0 else 1.0)), "top_scale": 0.85}]
        if k % 2 == 0:
            top = scale_poly(base, 0.6, shift=(nrm[0] * 0.2, nrm[1] * 0.2), turn=math.radians(10))
            lay.append({"poly_uv": [[r3(p[0]), r3(p[1])] for p in top], "y0": r3(h * 0.7), "y1": r3(h), "top_scale": 0.8})
        P.append({"id": "shore_rock_%d" % (k + 1), "piece": "shore rock %d" % (k + 1), "class": "shore_rock",
                  "kind": "primitive", "spec_uv": None, "uv": [r3(cen[0]), r3(cen[1])], "height_m": r3(h),
                  "derived_from": "the tarn row: 'West and south-west rim is shore rock (non-walkable)' (rim angle %d deg)" % t,
                  "layers": lay, "collider": "convex hull per layer"})

    # GROVES
    yi = 0
    for g, (c, n) in GROVES.items():
        offs = GROVE_OFFSETS[g]
        assert len(offs) == n, g
        sx, sy = sum(o[0] for o in offs), sum(o[1] for o in offs)
        assert abs(sx) < 1e-9 and abs(sy) < 1e-9, (g, sx, sy)
        for j, o in enumerate(offs):
            uv = (c[0] + o[0], c[1] + o[1])
            P.append({"id": "%s_birch_%d" % (g, j + 1), "piece": "%s birch %d" % (g, j + 1), "class": "birch",
                      "kind": "model", "glb": "res://models/barrow/birch.glb", "spec_uv": None,
                      "uv": [r3(uv[0]), r3(uv[1])], "grove": g, "grove_spec_uv": list(c),
                      "derived_from": "grove %s at (%g, %g) x%d; members sum to the grove point" % (g, c[0], c[1], n),
                      "yaw_world_deg": float(BIRCH_YAWS[yi % len(BIRCH_YAWS)]), "axis": "height",
                      "target_m": BA["birch"]["height_m"], "pitch_correct": True,
                      "width_m": BA["birch"]["width_m"], "hull_px": 0.0, "mesh_mark": 0.25,
                      "collider": "trunk", "trunk_r": BIRCH_TRUNK_R})
            yi += 1

    # FALLEN TREE: two kit logs end to end, the PAIR centred on the table's point. The pair's
    # position is the midpoint of the two logs' centres (for two equal logs, the centroid);
    # with the 6-degree kink the joint then sits 0.07 m off it, which is inside the tree.
    # Log B is turned end for end (+180) so the stand-in is not one log cloned beside itself.
    C = FALLEN_TREE
    dA = (math.cos(math.radians(LOG_ANGLES_DEG[0])), math.sin(math.radians(LOG_ANGLES_DEG[0])))
    dB = (math.cos(math.radians(LOG_ANGLES_DEG[1])), math.sin(math.radians(LOG_ANGLES_DEG[1])))
    h = 0.5 * LOG_LEN
    cA = (C[0] - h * dA[0], C[1] - h * dA[1])
    cB = (C[0] + h * dB[0], C[1] + h * dB[1])
    sh = (C[0] - 0.5 * (cA[0] + cB[0]), C[1] - 0.5 * (cA[1] + cB[1]))
    J = (C[0] + sh[0], C[1] + sh[1])
    for tag, a_deg, cen, flip in (("A", LOG_ANGLES_DEG[0], cA, 0.0), ("B", LOG_ANGLES_DEG[1], cB, 180.0)):
        uv = (cen[0] + sh[0], cen[1] + sh[1])
        P.append({"id": "fallen_tree_log_" + tag, "piece": "fallen tree, log " + tag, "class": "log",
                  "kind": "kit", "glb": "res://models/barrow/kit/log.glb", "spec_uv": None,
                  "uv": [r3(uv[0]), r3(uv[1])], "pair_spec_uv": list(C), "joint_uv": [r3(J[0]), r3(J[1])],
                  "derived_from": "the fallen tree at (-7, -12): two logs end to end, the pair centred on that point",
                  "yaw_world_deg": r3(a_deg + flip), "axis": "height", "target_m": KA["log"]["height_m"],
                  "pitch_correct": False, "width_m": None, "hull_px": 1.1, "collider": "hull",
                  "_yaw": "kit yaw 0 lies along +u (baked to the play camera); +%g turns it toward +v, along the tarn's near shore%s"
                          % (a_deg, "; +180 turns it end for end" if flip else "")})

    # GRAVE MARKERS
    for i, uv in enumerate(GRAVES):
        P.append({"id": "grave_marker_%s" % ("W" if uv[0] < 0 else "E"), "piece": "grave marker (shield on spears)",
                  "class": "shield", "kind": "kit", "glb": "res://models/barrow/kit/shield.glb",
                  "spec_uv": list(uv), "uv": list(uv), "yaw_world_deg": 0.0, "axis": "height",
                  "target_m": KA["shield"]["height_m"], "pitch_correct": False, "width_m": None,
                  "hull_px": 1.1, "collider": "hull", "_yaw": "kit yaw 0 shows the painted front to the play camera"})

    # CAIRNS
    for i, uv in enumerate(CAIRNS):
        e = {"id": "cairn_%d" % (i + 1), "piece": "cairn %d" % (i + 1), "class": "cairn", "kind": "kit",
             "glb": "res://models/barrow/kit/cairn.glb", "spec_uv": list(uv), "uv": list(uv),
             "yaw_world_deg": 0.0, "axis": "height", "target_m": KA["cairn"]["height_m"],
             "pitch_correct": False, "width_m": None, "hull_px": 1.1, "collider": "hull"}
        if i == 1:
            # TURNED, NOT MOVED. (-5, -14) is 2.53 m from the path's centreline, so 0.53 m clear
            # of its 4 m band -- and at kit yaw 0 the cairn is 1.11 m across the screen, so its
            # corner reaches ~0.1 m INTO the path (rectangle estimate). Laying its long side
            # along the path (the last segment runs 71.6 deg off +u) keeps the table's point
            # and leaves 0.53 - 0.37 = 0.16 m clear. A waymarker faces the path anyway.
            seg = (PATH["points"][2][0] - PATH["points"][1][0], PATH["points"][2][1] - PATH["points"][1][1])
            e["yaw_world_deg"] = r3(math.degrees(math.atan2(-seg[1], -seg[0])))
            e["_yaw"] = "turned %.1f deg so its long side runs along the path's last segment; the point is the table's" % e["yaw_world_deg"]
        P.append(e)
    return P, dev


# --- path / region math (vectorised) ---------------------------------------------------------
def seg_dist(pu, pv, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = np.clip(((pu - ax) * dx + (pv - ay) * dy) / L2, 0.0, 1.0)
    return np.hypot(pu - (ax + t * dx), pv - (ay + t * dy)), t


def path_points_extended():
    """The table's polyline, carried on past the frame's bottom edge along its last direction so
    the trodden band leaves the picture rather than stopping at its edge."""
    pts = list(PATH["points"])
    a, b = pts[-2], pts[-1]
    d = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*d)
    pts.append((b[0] + d[0] / L * 2.5, b[1] + d[1] / L * 2.5))
    return pts


def path_dist(pu, pv):
    pts = path_points_extended()
    best = np.full(pu.shape, 1e9)
    for i in range(len(pts) - 1):
        d, t = seg_dist(pu, pv, pts[i], pts[i + 1])
        if i == 0:
            # BUTT CAP at the ring entrance: the band starts at (0, -6.2), it does not bulge
            # a round cap 2 m into the ring
            d = np.where(t <= 0.0, 1e9, d)
        best = np.minimum(best, d)
    return best


def in_poly(pu, pv, poly):
    inside = np.zeros(pu.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cond = ((y1 > pv) != (y2 > pv))
        xint = x1 + (pv - y1) * (x2 - x1) / ((y2 - y1) if y2 != y1 else 1e-12)
        inside ^= cond & (pu < xint)
    return inside


def poly_boundary_dist(pu, pv, poly, closed=True, skip_edges=()):
    best = np.full(pu.shape, 1e9)
    n = len(poly)
    for i in range(n if closed else n - 1):
        if i in skip_edges:
            continue
        d, _ = seg_dist(pu, pv, poly[i], poly[(i + 1) % n])
        best = np.minimum(best, d)
    return best


def value_noise(pu, pv, cell, seed):
    """Smooth deterministic value noise in [-1, 1] on the ground, `cell` metres per lattice step."""
    rng = rng_for(seed)
    G = rng.uniform(-1, 1, size=(97, 97))
    x = (pu / cell) + 48.0
    y = (pv / cell) + 48.0
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    fx = x - x0
    fy = y - y0
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    x0 = np.clip(x0, 0, 95)
    y0 = np.clip(y0, 0, 95)
    a = G[y0, x0]
    b = G[y0, x0 + 1]
    c = G[y0 + 1, x0]
    d = G[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def region_masks(pu, pv, P):
    """Every ground class as a boolean mask over (pu, pv). Priority ice > path > shrub > snow."""
    tc, (ta, tb) = TARN["centre"], (TARN["axes"][0] / 2, TARN["axes"][1] / 2)
    rho_t = np.hypot((pu - tc[0]) / ta, (pv - tc[1]) / tb)
    ice = rho_t <= 1.0
    pd = path_dist(pu, pv)
    path = pd <= PATH["width"] / 2.0
    arena = np.hypot(pu - ARENA["centre"][0], pv - ARENA["centre"][1]) <= ARENA["r"]
    # the ring entrance: the gap between the gate stones and a stride either side of it
    g = ring_uv(155)
    entrance = (np.abs(pu) <= g[0] + 0.3) & (np.abs(pv - g[1]) <= 1.6)

    warp = value_noise(pu, pv, 1.6, 71) * 0.45           # organic edges, +-0.45 m
    zones = {}
    # 2-3 m skirts round every outcrop (the eight and the cover outcrop): 2.5 m, warped
    sk = np.zeros(pu.shape, dtype=bool)
    for e in P:
        if e["class"] == "outcrop":
            base = [tuple(p) for p in e["layers"][0]["poly_uv"]]
            d = np.where(in_poly(pu, pv, base), 0.0, poly_boundary_dist(pu, pv, base))
            sk |= (d + warp) <= 2.5
    zones["outcrop_skirts"] = sk
    # under the groves: 1.7 m round every trunk, warped
    gv = np.zeros(pu.shape, dtype=bool)
    for e in P:
        if e["class"] == "birch":
            gv |= (np.hypot(pu - e["uv"][0], pv - e["uv"][1]) + warp) <= 1.7
    zones["under_groves"] = gv
    # the mound's base outside the ring: a 2.2 m band outside the foot, beyond the ring circle
    mc = MOUND["centre"]
    ma, mb = MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
    rho_m = np.hypot((pu - mc[0]) / ma, (pv - mc[1]) / mb)
    band = (rho_m >= 0.93) & (np.hypot((pu - mc[0]) / (ma + 2.2), (pv - mc[1]) / (mb + 2.2)) + warp * 0.08 <= 1.0)
    outside_ring = np.hypot(pu - RING["centre"][0], pv - RING["centre"][1]) > RING["r"]
    zones["mound_base_outside_ring"] = band & outside_ring
    # the tarn's far shore: the W half of a 2.8 m band round the ice (behind the shore rock)
    far = (rho_t > 1.0) & (np.hypot((pu - tc[0]) / (ta + 2.8), (pv - tc[1]) / (tb + 2.8)) + warp * 0.08 <= 1.0) \
        & (pu <= tc[0] - 1.0)
    zones["tarn_far_shore"] = far
    # ADDED: the thickets the bounds row names but the table does not place. A 3 m scrub band
    # centred on every edge of the bounds polygon except the entry.
    bd = poly_boundary_dist(pu, pv, BOUNDS, closed=True, skip_edges=(len(BOUNDS) - 1,))
    zones["thicket_band_ADDED"] = (bd + warp) <= 1.5
    shrub_zone = np.zeros(pu.shape, dtype=bool)
    for m in zones.values():
        shrub_zone |= m
    # PATCHES, not solid fills -- but few and large clearings, not a field of holes: the first
    # version (0.9 m cells, ~80% cover) read as a green sheet with snow holes punched in it
    patch = value_noise(pu, pv, 2.4, 113) > -0.72
    shrub = shrub_zone & patch
    # "Never in the arena, on the path, on the ice, or in the ring entrance"
    keep_out = arena | (pd <= PATH["width"] / 2.0 + 0.35) | ice | entrance
    shrub &= ~keep_out
    path &= ~ice
    return {"ice": ice, "path": path, "shrub": shrub, "arena": arena, "entrance": entrance,
            "zones": zones, "keep_out": keep_out}


def gauss_blur(a, sigma_px):
    r = int(math.ceil(sigma_px * 3))
    x = np.arange(-r, r + 1)
    k = np.exp(-0.5 * (x / sigma_px) ** 2)
    k /= k.sum()
    b = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, np.pad(a, r, mode="edge"))
    b = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, b)
    return b[r:-r, r:-r]


SPLAT = {"origin_xz": [-27.0, -27.0], "size_m": [54.0, 54.0], "m_per_px": 0.05}


def make_splat(P):
    n = int(round(SPLAT["size_m"][0] / SPLAT["m_per_px"]))
    ii, jj = np.meshgrid(np.arange(n), np.arange(n))       # ii = column (x), jj = row (z)
    x = SPLAT["origin_xz"][0] + (ii + 0.5) * SPLAT["m_per_px"]
    z = SPLAT["origin_xz"][1] + (jj + 0.5) * SPLAT["m_per_px"]
    pu, pv = xz_to_uv(x, z)
    M = region_masks(pu, pv, P)
    cls = np.zeros((n, n), dtype=np.uint8)                   # 0 snow
    cls[M["shrub"]] = 3
    cls[M["path"]] = 1
    cls[M["ice"]] = 4
    # four weight fields (path, rock, heather/shrub, ice); snow is 1 - sum, as the shader wants
    W = []
    for c in (1, 2, 3, 4):
        W.append(gauss_blur((cls == c).astype(np.float64), 1.6))
    W = np.stack(W, axis=-1)
    s = W.sum(axis=-1, keepdims=True)
    W = np.divide(W, s, out=W.copy(), where=s > 1.0)
    img = Image.fromarray(np.clip(np.round(W * 255.0), 0, 255).astype(np.uint8), "RGBA")
    # PNG BYTES UNDER A .bin NAME. The scene reads the raw bytes (an importer that decided this
    # was a 3D texture would compress it, and a lossy weight is a different ground class). But
    # a .png is an importable RESOURCE, and an export's include_filter ships only NON-resource
    # files -- the first app shipped the import and not the file, and the scene said so at
    # launch (splat_ok=false). A .bin is not importable, so the export ships it as it is.
    out = GODOT / "data" / "barrow_full_splat.bin"
    img.save(out, format="PNG", optimize=True)
    shares = {k: round(float((cls == v).mean()) * 100, 2) for k, v in
              (("snow", 0), ("path", 1), ("shrub", 3), ("ice", 4))}
    return {"file": "res://data/barrow_full_splat.bin", "encoding": "PNG bytes (RGBA8)", "origin_xz": SPLAT["origin_xz"],
            "size_m": SPLAT["size_m"], "m_per_px": SPLAT["m_per_px"], "px": [n, n],
            "channels": "R path, G rock (unused), B shrub (juniper and heather), A ice; snow = 1 - sum",
            "blur_sigma_m": 0.08, "class_share_pct_of_raster": shares,
            "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "_frame": "WORLD xz, not (u, v): the HEAD ground shader samples the splat axis-aligned in world"}


def chunks():
    out = []
    for r in range(CHUNK["rows"]):
        for c in range(CHUNK["cols"]):
            x0, y0 = c * CHUNK["stride_px"][0], r * CHUNK["stride_px"][1]
            x1, y1 = x0 + CHUNK["canvas_px"][0], y0 + CHUNK["canvas_px"][1]
            out.append({"key": "%d_%d" % (c, r), "px": [x0, y0, x1, y1],
                        "ground_uv": {"u": [r3((x0 - GUIDE_PX[0] / 2) / PPM), r3((x1 - GUIDE_PX[0] / 2) / PPM)],
                                      "v": [r3((GUIDE_PX[1] / 2 - y1) / PX_UP), r3((GUIDE_PX[1] / 2 - y0) / PX_UP)]}})
    return out


def design_checks(P):
    """PRE-BUILD estimates from the manifests (rectangles at the placement yaw). The acceptance
    numbers are NOT these: finalize.py measures the built meshes. These exist so a conflict is
    visible before Godot is ever started."""
    out = {}
    tc, (ta, tb) = TARN["centre"], (TARN["axes"][0] / 2, TARN["axes"][1] / 2)
    for e in P:
        if e.get("kind") in ("model", "kit") and e.get("uv") and e["class"] not in ("birch",):
            u, v = e["uv"]
            out.setdefault("arena_centre_dist", {})[e["id"]] = r3(math.dist((u, v), ARENA["centre"]))
            rho = math.hypot((u - tc[0]) / ta, (v - tc[1]) / tb)
            if rho < 1.15:
                out.setdefault("near_or_on_ice_rho", {})[e["id"]] = r3(rho)
    pu = np.array([[e["uv"][0] for e in P if e.get("uv")]])
    pv = np.array([[e["uv"][1] for e in P if e.get("uv")]])
    d = path_dist(pu, pv)[0]
    ids = [e["id"] for e in P if e.get("uv")]
    out["path_centreline_dist_lt_3m"] = {i: r3(x) for i, x in zip(ids, d) if x < 3.0}
    return out


def main():
    P, dev = build()
    splat = make_splat(P)
    g155 = ring_uv(155)
    layout = {
        "_what": "C-9 T10-2 step 1: the Frost King's Barrow, full area, blockout layout. Design numbers from the spec table; finalize.py merges in the BUILT numbers (world transforms, measured sizes and footprints) from the Godot scene.",
        "_spec": "agentic_orchestration/gandalf/notes/2026-09-29-barrow-full-area-blockout-spec.md",
        "_rulings": {"R-C9-73": "fully generated: no Synty, nothing bought",
                     "R-C9-74": "one flat play floor; elevation only by architected steps",
                     "R-C9-75": "blockout first, painted over chunk by chunk"},
        "frame": {
            "units": "metres",
            "u_hat_world": [r3(CY), 0.0, r3(-SY)], "v_hat_world": [r3(-SY), 0.0, r3(-CY)],
            "origin_world": [0.0, 0.0, 0.0],
            "world_from_uv": "x = u*cos47 - v*sin47; z = -u*sin47 - v*cos47; y = height above the floor",
            "theta": "measured clockwise from +v",
            "camera": {"projection": "orthogonal", "pitch_deg": PITCH_DEG, "yaw_deg": YAW_DEG,
                       "px_per_m_across": PPM, "px_per_ground_m_up_screen": r3(PX_UP),
                       "px_per_vertical_m": r3(PPM * CP)},
            "guide_window": {"u": [r3(-U_HALF), r3(U_HALF)], "v": [r3(-V_HALF), r3(V_HALF)],
                             "px": list(GUIDE_PX), "centre_uv": [0.0, 0.0],
                             "_px_from_uv": "x = 2048 + u*100.6176 ; y = 1280 - v*80.3076 - h*60.6175"},
            "chunks": {"cols": 3, "rows": 3, "canvas_px": CHUNK["canvas_px"],
                       "stride_px": CHUNK["stride_px"], "list": chunks(),
                       "_ground_uv": "the ground footprint of each canvas; anything standing up projects UP-screen into the chunk above"},
        },
        "tints_srgb": TINTS,
        "placements": P,
        "regions": {
            "arena": {"type": "disc", "centre_uv": list(ARENA["centre"]), "r": ARENA["r"],
                      "rule": "nothing placed; drifts <= 0.2 m (no 3D snow in the blockout)"},
            "ring": {"type": "circle", "centre_uv": list(RING["centre"]), "r": RING["r"]},
            "ring_entrance": {"type": "gap", "between": ["ring_p155", "ring_m155"],
                              "gate_centres_uv": [[r3(g155[0]), r3(g155[1])], [r3(-g155[0]), r3(g155[1])]]},
            "path": {"type": "polyline", "points_uv": [list(p) for p in PATH["points"]],
                     "extended_off_frame_uv": [[r3(p[0]), r3(p[1])] for p in path_points_extended()],
                     "width_m": PATH["width"], "caps": "butt at the ring entrance; runs off the bottom edge",
                     "rule": "path ground; nothing placed on it"},
            "ice": {"type": "ellipse", "centre_uv": list(TARN["centre"]), "axes_m": list(TARN["axes"]),
                    "walkable": True, "rule": "flat and walkable; no snow; W and SW rim is shore rock, E open"},
            "shrub_zones": {"components": ["outcrop_skirts (2.5 m)", "under_groves (1.7 m per trunk)",
                                           "mound_base_outside_ring (2.2 m)", "tarn_far_shore (2.8 m, W half)",
                                           "thicket_band_ADDED (1.5 m either side of every bounds edge but the entry)"],
                            "edge_warp_m": 0.45, "patch_cover": "~90% inside a zone, clearings on a 2.4 m lattice",
                            "never_in": ["arena", "path (+0.35 m)", "ice", "ring_entrance"],
                            "raster": "godot/data/barrow_full_splat.bin (PNG bytes), channel B"},
            "splat": splat,
        },
        "bounds": {"polygon_uv": [list(p) for p in BOUNDS], "entry_gap_uv": [list(p) for p in ENTRY_GAP],
                   "entry_edge_index": len(BOUNDS) - 1,
                   "walls": "invisible vertical boxes 0.3 m thick, 3 m tall, on every edge; the entry edge is the EXIT line (the eventual level transition)",
                   "_reads_as": "rock where an outcrop straddles it, trees at G2/G4, the mound, and the ADDED thicket band everywhere else"},
        "knight": {"spawn_uv": [-3.0, -15.0], "spawn_facing": "N",
                   "guide_uv": list(ARENA["centre"]), "guide_facing": "S",
                   "gear_stack": 4, "_gear": "full kit: helmet, bracers, byrnie, mantle, axe, shield"},
        "deviations": dev,
    }
    layout["design_checks_prebuild"] = design_checks(P)
    txt = json.dumps(layout, indent=1)
    (ROOT / "barrow_full_layout.json").write_text(txt)
    (GODOT / "data" / "barrow_full_layout.json").write_text(txt)
    print("placements:", len(P), " splat:", splat["px"], splat["class_share_pct_of_raster"])
    print(json.dumps(layout["design_checks_prebuild"], indent=1))


if __name__ == "__main__":
    main()
