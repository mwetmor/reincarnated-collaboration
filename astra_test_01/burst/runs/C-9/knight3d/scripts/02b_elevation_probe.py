#!/usr/bin/env python3
"""C-9 knight3d: an INDEPENDENT measurement of the camera elevation, so the
joint camera+body fit is not the only witness.

Why a second instrument. In an orthographic view of a standing figure, raising
the elevation theta foreshortens every vertical length by cos(theta) -- and the
fitter is free to rescale the figure, and free to change the body's
proportions. So theta and (body aspect ratio x per-view scale) are very nearly
degenerate, and a silhouette IoU can be flat across a wide band of theta while
LOOKING converged. That is exactly the ninth-instrument trap: the check runs,
the check passes, and the check was not answering the question.

The measurement that is NOT degenerate:

  In a PROFILE view (E, alpha=90; W, alpha=270) the screen-up axis is
      u = (-sin t, 0, cos t)     [alpha = 90]
  so a point ON THE GROUND (z = 0) at the figure's lateral offset x projects to
      v = -sin(t) * x.
  The two feet stand on the ground at different LATERAL offsets (the stance
  width). Their fore/aft stagger moves them along screen-X only. Therefore

      (vertical gap between the two soles, in a profile view)
          = (lateral stance width) * sin(theta)

  and the lateral stance width is read straight off the FRONT/BACK views
  (S, N), where the lateral axis is the screen-X axis and is NOT foreshortened.

  sin(theta) = dv_profile / dx_frontal      (both normalised by figure height)

This uses only sole positions, needs no body model, and cannot be absorbed by
a per-view scale because both quantities are normalised by the same figure
height in their own view.
"""
import json, os, sys
import numpy as np
from scipy import ndimage as ndi
from PIL import Image

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
WORK = os.path.join(ROOT, "knight3d", "work")
MASKS = os.path.join(WORK, "masks")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]


def feet(mask, frac=0.13):
    """Split the bottom `frac` of the figure into the two feet; return, for
    each, (sole row, centre column, pixel count)."""
    ys = np.where(mask.any(axis=1))[0]
    y0, y1 = int(ys.min()), int(ys.max())
    H = y1 - y0 + 1
    band = np.zeros_like(mask)
    band[y1 - int(frac * H):y1 + 1] = mask[y1 - int(frac * H):y1 + 1]
    lab, n = ndi.label(band, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        c = (lab == i)
        if c.sum() < 0.002 * mask.sum():
            continue
        yy, xx = np.where(c)
        out.append(dict(sole=int(yy.max()), cx=float(xx.mean()), area=int(c.sum()),
                        x_lo=int(xx.min()), x_hi=int(xx.max())))
    out.sort(key=lambda r: -r["area"])
    return out[:2], H, y0, y1


def main():
    res = {"note": __doc__.strip().splitlines()[0], "views": {}}
    for d in DIRS:
        m = np.load(os.path.join(MASKS, "%s_body.npy" % d))
        f, H, y0, y1 = feet(m)
        res["views"][d] = dict(figure_h=H, n_foot_blobs=len(f), feet=f)
        if len(f) == 2:
            res["views"][d]["sole_gap_px"] = abs(f[0]["sole"] - f[1]["sole"])
            res["views"][d]["sole_gap_over_H"] = abs(f[0]["sole"] - f[1]["sole"]) / H
            res["views"][d]["foot_cx_gap_over_H"] = abs(f[0]["cx"] - f[1]["cx"]) / H

    # frontal/back views give the lateral stance width; profile views the
    # vertical sole gap
    lat = [res["views"][d].get("foot_cx_gap_over_H") for d in ("S", "N")]
    lat = [v for v in lat if v]
    prof = [res["views"][d].get("sole_gap_over_H") for d in ("E", "W")]
    prof = [v for v in prof if v]
    out = {}
    if lat and prof:
        for i, dn in enumerate(("E", "W")):
            if res["views"][dn].get("sole_gap_over_H") is None:
                continue
            for j, df in enumerate(("S", "N")):
                if res["views"][df].get("foot_cx_gap_over_H") is None:
                    continue
                s = res["views"][dn]["sole_gap_over_H"] / res["views"][df]["foot_cx_gap_over_H"]
                out["%s_over_%s" % (dn, df)] = dict(
                    sin_theta=s,
                    theta_deg=float(np.degrees(np.arcsin(min(1.0, max(-1.0, s))))))
        vals = [v["theta_deg"] for v in out.values()]
        res["estimates"] = out
        res["theta_deg_mean"] = float(np.mean(vals))
        res["theta_deg_spread"] = float(np.max(vals) - np.min(vals))
    res_path = os.path.join(WORK, "elevation_probe.json")
    with open(res_path, "w") as fh:
        json.dump(res, fh, indent=1)
    for d in DIRS:
        v = res["views"][d]
        print("%-3s blobs=%d  sole_gap/H=%s  foot_cx_gap/H=%s" %
              (d, v["n_foot_blobs"],
               ("%.4f" % v["sole_gap_over_H"]) if "sole_gap_over_H" in v else "-",
               ("%.4f" % v["foot_cx_gap_over_H"]) if "foot_cx_gap_over_H" in v else "-"))
    if "estimates" in res:
        for k, v in res["estimates"].items():
            print("  %-10s sin(theta)=%.4f -> theta=%.2f deg" % (k, v["sin_theta"], v["theta_deg"]))
        print("  mean theta %.2f deg, spread %.2f deg" %
              (res["theta_deg_mean"], res["theta_deg_spread"]))
    print("wrote", res_path)

    # a picture of what was measured
    tiles = []
    for d in DIRS:
        m = np.load(os.path.join(MASKS, "%s_body.npy" % d))
        rgb = np.zeros(m.shape + (3,), np.uint8); rgb[..., 1] = m * 120
        for f in res["views"][d]["feet"]:
            rgb[f["sole"] - 3:f["sole"] + 4, f["x_lo"]:f["x_hi"] + 1] = (255, 40, 40)
        tiles.append(Image.fromarray(rgb[-560:]).resize((260, 300)))
    sheet = Image.new("RGB", (260 * 8, 300))
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * 260, 0))
    sheet.save(os.path.join(WORK, "elevation_probe.png"))


if __name__ == "__main__":
    main()


def ground_lsq():
    """Second, stronger form of the same instrument.

    Both soles are GROUND points. For a ground displacement (dx, dy) between
    the left and right sole, in a view at azimuth alpha and elevation theta:

        d(screen x) / H_view = (-dx cos a + dy sin a) / (Hb cos t)
        d(image  y) / H_view =  tan(t) * (dx sin a + dy cos a) / Hb

    With a = dx/Hb and b = dy/Hb this is three unknowns (a, b, theta) against
    two measurements in each of the views that resolve two separate feet. It
    uses ONLY ground contacts, so no body model can absorb the answer, and the
    RESIDUAL is itself the report: if one stance does not explain all eight
    views, the stills are not one stance.
    """
    import numpy as np
    from scipy.optimize import least_squares
    res = json.load(open(os.path.join(WORK, "elevation_probe.json")))
    NOM = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
    obs = []
    for d in DIRS:
        v = res["views"][d]
        if v["n_foot_blobs"] != 2:
            continue
        f = sorted(v["feet"], key=lambda r: r["cx"])      # screen-left first
        obs.append((d, np.radians(NOM[d]),
                    (f[1]["cx"] - f[0]["cx"]) / v["figure_h"],
                    (f[1]["sole"] - f[0]["sole"]) / v["figure_h"]))

    def resid(p):
        a, b, t = p
        out = []
        for d, al, du_m, dy_m in obs:
            du = (-a * np.cos(al) + b * np.sin(al)) / max(np.cos(t), 1e-3)
            dy = np.tan(t) * (a * np.sin(al) + b * np.cos(al))
            if du < 0:                                     # same pair, other order
                du, dy = -du, -dy
            out += [du - du_m, dy - dy_m]
        return out

    best = None
    for t0 in np.radians([5, 15, 25, 35]):
        for s in (1, -1):
            r = least_squares(resid, [0.21 * s, 0.02, t0],
                              bounds=([-0.6, -0.6, 0.0], [0.6, 0.6, np.radians(60)]))
            if best is None or r.cost < best.cost:
                best = r
    a, b, t = best.x
    rr = np.array(resid(best.x))
    out = dict(views_used=[o[0] for o in obs],
               stance_lateral_over_Hb=float(a), stance_foreaft_over_Hb=float(b),
               theta_deg=float(np.degrees(t)),
               rms_residual_over_H=float(np.sqrt((rr ** 2).mean())),
               per_view={o[0]: dict(d_screen_x_meas=o[2], d_image_y_meas=o[3],
                                    resid_x=float(rr[2 * i]), resid_y=float(rr[2 * i + 1]))
                         for i, o in enumerate(obs)})
    res["ground_contact_lsq"] = out
    with open(os.path.join(WORK, "elevation_probe.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print("\nground-contact least squares over %d views:" % len(obs))
    print("  theta = %.2f deg;  stance lateral %.3f Hb, fore/aft %.3f Hb;  rms residual %.4f H"
          % (out["theta_deg"], a, b, out["rms_residual_over_H"]))
    for d, v in out["per_view"].items():
        print("   %-3s meas dx=%+.4f dy=%+.4f   resid dx=%+.4f dy=%+.4f"
              % (d, v["d_screen_x_meas"], v["d_image_y_meas"], v["resid_x"], v["resid_y"]))
    return out


if __name__ == "__main__":
    ground_lsq()
