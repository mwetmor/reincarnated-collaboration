#!/usr/bin/env python3
"""C-9 knight3d: is the POLLAXE in the same place in all eight stills?

The haft is a rigid object held at one grip point. If the eight stills were
eight views of one 3D scene, the haft's screen offset from the body centreline
would be exactly

    du(alpha) = g . r(alpha) = -gx cos(alpha) + gy sin(alpha)

for ONE point g = (gx, gy) in the figure's frame. So: measure the haft offset
in every view at the fitted azimuths, fit the single best g by least squares,
and report the per-view residual. A large residual in some views and not
others says the pollaxe was drawn where it looked right rather than where the
geometry puts it -- which is the cut-out method's structure defect (Matt 3)
showing up in the source art itself.
"""
import json, os, sys
import numpy as np

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
WORK = os.path.join(ROOT, "knight3d", "work")
MASKS = os.path.join(WORK, "masks")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    rows = []
    for d in DIRS:
        body = np.load(os.path.join(MASKS, "%s_body.npy" % d))
        axe = np.load(os.path.join(MASKS, "%s_axe.npy" % d))
        ys = np.where(body.any(axis=1))[0]
        y0, y1 = int(ys.min()), int(ys.max()); H = y1 - y0 + 1
        band = body[y0 + int(.20 * H): y0 + int(.45 * H)]
        bx = float(np.where(band)[1].mean())
        row = y0 + int(.30 * H)
        ax = np.where(axe[row])[0]
        v = fit["canonical"]["views"][d]
        rows.append(dict(view=d, alpha=v["alpha"], nominal=v["nominal_alpha"],
                         du_over_H=(float(ax.mean()) - bx) / H,
                         scale=v["scale_px_per_m_fullres"], figure_h=H))

    def design(al_deg):
        a = np.radians(al_deg)
        return np.array([-np.cos(a), np.sin(a)])

    for tag, key in (("fitted azimuths", "alpha"), ("nominal azimuths", "nominal")):
        A = np.array([design(r[key]) for r in rows])
        b = np.array([r["du_over_H"] for r in rows])
        g, *_ = np.linalg.lstsq(A, b, rcond=None)
        pred = A @ g
        res = pred - b
        print("\n%s: best single grip point g = (%.4f, %.4f) H" % (tag, g[0], g[1]))
        print("  %-4s %-8s %-11s %-11s %s" % ("view", "alpha", "measured", "predicted", "residual (H)"))
        for r, p_, e in zip(rows, pred, res):
            print("  %-4s %-8.1f %+-11.4f %+-11.4f %+.4f%s" %
                  (r["view"], r[key], r["du_over_H"], p_, e,
                   "   <== " if abs(e) > 0.06 else ""))
        print("  rms residual %.4f H  (= %.0f px at the mean painted scale)" %
              (np.sqrt((res ** 2).mean()),
               np.sqrt((res ** 2).mean()) * np.mean([r["figure_h"] for r in rows])))
        if key == "alpha":
            out = dict(grip_point_over_H=[float(g[0]), float(g[1])],
                       rms_residual_over_H=float(np.sqrt((res ** 2).mean())),
                       per_view={r["view"]: dict(alpha=r["alpha"], measured=r["du_over_H"],
                                                 predicted=float(p_), residual=float(e))
                                 for r, p_, e in zip(rows, pred, res)})
    with open(os.path.join(WORK, "pollaxe_consistency.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwrote", os.path.join(WORK, "pollaxe_consistency.json"))


if __name__ == "__main__":
    main()
