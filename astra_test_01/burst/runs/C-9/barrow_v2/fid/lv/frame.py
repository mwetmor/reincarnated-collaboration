#!/usr/bin/env python3
"""BV2F lane LV, Phase 0.2 (DEV-4, plan C6): THE frame fix -- the ONE place the sim -> world transform lives.

layout_v2.json and sketch A are composed for a YAW-0 camera (layout_v2.json "camera": screen_x = ppm*x,
screen_y = ppm*sin(a)*y - ppm*cos(a)*z; sim +x east = screen-right, sim +y SOUTH = screen-down).
v1's engine (runs/C-9/barrow_full/godot/scripts/barrow_full.gd:44-45, 246-268) keeps its camera at
pitch 52.95354112560294, YAW 47. R-C9-159 placed the sim frame unrotated in that world (Godot X = x,
Z = y; barrow_v2_sw.gd header) and so saw the site 47 deg off sketch A's composition.

The fix: rotate the SITE by the camera yaw, leave the camera (and heather card basis, suns, snow, pen)
untouched:

    world = R_y(+47 deg) . (x, z, y)          Godot axes: X right, Y up, Z; R_y = Basis(Vector3.UP, +47 deg)

    R_y(t) = [[ cos t, 0, sin t],
              [   0,   1,   0  ],
              [-sin t, 0, cos t]]

so sim +x (east) -> (cos47, 0, -sin47) = v1's u_hat (screen-right on the ground, barrow_full.gd:76) and
sim +y (south) -> (sin47, 0, cos47) = -v_hat (screen-down on the ground, barrow_full.gd:77).
A model's Godot yaw rotates with it: rot_y_world = rot_y_sim + 47 deg.

Twin: fid/lv/frame.gd (same constants, same formulas). Proof: fid/lv/test_frame.py.
"""
import math

PL_YAW_DEG = 47.0                      # barrow_full.gd:45 -- v1's camera yaw, UNCHANGED
PL_PITCH_DEG = 52.95354112560294       # barrow_full.gd:44
PPM = 100.617553710938                 # barrow_full.gd:43 (plate scale)
FRAME_YAW_DEG = +PL_YAW_DEG            # the site's rotation; the SIGN is what test_frame.py proves

_c = math.cos(math.radians(FRAME_YAW_DEG))
_s = math.sin(math.radians(FRAME_YAW_DEG))


def sim_to_world(x, y, z=0.0, yaw_deg=FRAME_YAW_DEG):
    """sim (x east, y south, z up) -> Godot world (X, Y up, Z) in v1's level, rotated by the camera yaw."""
    c, s = (_c, _s) if yaw_deg == FRAME_YAW_DEG else (math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg)))
    return (c * x + s * y, z, -s * x + c * y)


def world_to_sim(X, Y, Z):
    """inverse: Godot world -> sim (x, y, z)."""
    return (_c * X - _s * Z, _s * X + _c * Z, Y)


def rot_y_to_world(rot_y_sim_deg):
    """a model's Godot rotation_degrees.y in the sim frame (layout 'godot_rot_y_deg') -> in v1's world."""
    return rot_y_sim_deg + FRAME_YAW_DEG


def v1_camera_basis(pitch_deg=PL_PITCH_DEG, yaw_deg=PL_YAW_DEG):
    """v1's camera, exactly as barrow_full.gd:_build_camera builds it: f = (-sin y cos p, -sin p, -cos y cos p),
    look_at with world up. Returns (right, up, forward) unit vectors in Godot world axes."""
    p, y = math.radians(pitch_deg), math.radians(yaw_deg)
    f = (-math.sin(y) * math.cos(p), -math.sin(p), -math.cos(y) * math.cos(p))
    # look_at: back = -f; right = up_world x back (normalised); up = back x right
    b = (-f[0], -f[1], -f[2])
    r = (b[2], 0.0, -b[0])                                  # (0,1,0) x b
    n = math.hypot(r[0], r[2]); r = (r[0] / n, 0.0, r[2] / n)
    u = (b[1] * r[2] - b[2] * r[1], b[2] * r[0] - b[0] * r[2], b[0] * r[1] - b[1] * r[0])
    return r, u, f


def project_v1(P, ppm=PPM):
    """orthographic screen offset (px, +x right, +y DOWN) of world point P relative to the world origin."""
    r, u, _ = v1_camera_basis()
    return (ppm * (P[0] * r[0] + P[1] * r[1] + P[2] * r[2]),
            -ppm * (P[0] * u[0] + P[1] * u[1] + P[2] * u[2]))


def project_yaw0_layout(x, y, z=0.0, ppm=PPM, pitch_deg=PL_PITCH_DEG):
    """layout_v2.json's own camera law (the frame sketch A was composed in)."""
    a = math.radians(pitch_deg)
    return (ppm * x, ppm * math.sin(a) * y - ppm * math.cos(a) * z)
