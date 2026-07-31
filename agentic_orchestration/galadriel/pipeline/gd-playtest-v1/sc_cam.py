#!/usr/bin/env python3
"""SHADOW-CAL: the GAL-CAM pinhole camera, as usable geometry.

Reads the banked operand family from
  captures/2026-07-30-gal-cam/godot-spec.json
(5 members: 2.5 / 16 / 50 / 84 / 97.5 percentile of the axis-ratio posterior)
and exposes project / unproject-to-ground / solve-height.

CONVENTION
----------
World: X right, Y up, Z away-from-camera (up-screen).  Ground plane Y = 0.
Look-at at the world origin; camera at C = (0, D sin(th), -D cos(th)).
Screen: 1920x1080, principal point (960, 540), y down.

PRESENTATION GEOMETRY ONLY.  No sim semantics.
"""
import json
import math
import os

import numpy as np

SPEC = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "captures", "2026-07-30-gal-cam", "godot-spec.json",
)
PX0, PY0 = 960.0, 540.0
NOMINAL = 2  # index of the p50 family member


class Cam:
    def __init__(self, pitch_deg, focal_px, dist_m):
        self.th = math.radians(pitch_deg)
        self.f = float(focal_px)
        self.D = float(dist_m)
        st, ct = math.sin(self.th), math.cos(self.th)
        self.st, self.ct = st, ct
        self.C = np.array([0.0, self.D * st, -self.D * ct])
        self.fwd = np.array([0.0, -st, ct])
        self.right = np.array([1.0, 0.0, 0.0])
        self.up = np.array([0.0, ct, st])

    # ---------- forward ----------
    def project(self, P):
        P = np.atleast_2d(np.asarray(P, float))
        v = P - self.C
        s = v @ self.fwd
        x = PX0 + self.f * (v @ self.right) / s
        y = PY0 - self.f * (v @ self.up) / s
        out = np.stack([x, y], -1)
        return out[0] if out.shape[0] == 1 else out

    # ---------- inverse, onto the ground ----------
    def unproject_ground(self, xy):
        xy = np.atleast_2d(np.asarray(xy, float))
        dx = (xy[:, 0] - PX0) / self.f
        dy = -(xy[:, 1] - PY0) / self.f
        d = (self.fwd[None, :]
             + dx[:, None] * self.right[None, :]
             + dy[:, None] * self.up[None, :])
        t = -self.C[1] / d[:, 1]
        P = self.C[None, :] + t[:, None] * d
        return P[0] if P.shape[0] == 1 else P

    # ---------- height of a point standing over a known ground base ----------
    def solve_height(self, base_xz, y_screen):
        """base_xz = (X, Z) ground point; y_screen = screen row of the top.
        Returns the world height h of that top above the ground."""
        Bx, Bz = base_xz
        w = Bz - self.C[2]
        q = (PY0 - float(y_screen)) / self.f
        a = -w * (self.st - q * self.ct) / (q * self.st + self.ct)
        return a + self.C[1]

    # ---------- ground scale at a screen row (for reporting) ----------
    def ground_scale(self, x, y, eps=0.5):
        p0 = self.unproject_ground([[x, y]])
        px = self.unproject_ground([[x + eps, y]])
        py = self.unproject_ground([[x, y + eps]])
        gx = eps / np.linalg.norm(px - p0)
        gy = eps / np.linalg.norm(py - p0)
        return float(gx), float(gy)


def family(path=SPEC):
    with open(path) as fh:
        s = json.load(fh)
    return [Cam(s["pitch_deg"][i], s["focal_px"][i], s["cam_dist_m"][i])
            for i in range(len(s["pitch_deg"]))], s


def nominal(path=SPEC):
    fam, _ = family(path)
    return fam[NOMINAL]


if __name__ == "__main__":
    fam, spec = family()
    c = fam[NOMINAL]
    print(f"nominal: pitch {math.degrees(c.th):.2f} deg  f {c.f:.1f} px  "
          f"D {c.D:.2f} m  C {c.C.round(3)}")
    # reproduce GAL-CAM's own anchors as a self-check
    P = np.array([spec["player_dX_m"][NOMINAL], 0.0, spec["player_dZ_m"][NOMINAL]])
    print("player anchor reprojects to", c.project(P).round(1), " (GAL-CAM: 962, 595)")
    gx, gy = c.ground_scale(962, 595)
    print(f"ground scale at the player row: g_x {gx:.2f} px/m  "
          f"g_y {gy:.2f} px/m   (GAL-CAM: 54.47 / 44.44)")
    for y in (0, 595, 1079):
        gx, gy = c.ground_scale(960, y)
        print(f"  row {y:4d}: g_x {gx:.2f}")
    # round trip
    g = c.unproject_ground([[962.0, 595.0]])
    print("unproject(962,595) ->", np.round(g, 3), "reproject ->",
          c.project(g).round(2))
    h = c.solve_height((g[0], g[2]), 595 - 100)
    print(f"a top 100 px above the anchor's feet = {h:.3f} m tall")
