#!/usr/bin/env python3
"""WR1-GAL-3: death-2 crossing distance + uncertainty band.

Combines the measured quantities into r (metres from player to caster at the
moment of damage application, f309085) and propagates every uncertainty by Monte
Carlo rather than quoting a point estimate.

Inputs and where each comes from:
  player ground point   (962, 602) px   median-stack of a running window, pts
                                        5138-5151, where the camera is player-
                                        locked so the player is the only sharp
                                        object; x corroborated by the dev-overlay
                                        label anchor for entity [42992]
  caster ground point   (1024.7, 568.5) px  centre of the compact nova ring at
                                        f309085/f309086 (bounded ellipse fit to
                                        the 16 spike centroids)
  k = b/a                0.60 - 0.85    ring aspect at f309085/86 + hodograph
  lance-A screen speed   13.55 px/frame  27-frame frontier track of the one
                                        long-lived projectile
Scale: s = sqrt(vx^2 + (vy/k)^2) / (14/60)   px per metre along screen X.
Then r = sqrt(dx^2 + (dy/k)^2) / s.

The k-dependence very nearly cancels between numerator and denominator because
the player offset and lance A point in similar screen directions -- that is why
the answer is robust to the pitch, which is the least well pinned input.
"""
import json

import numpy as np

N = 200000
rng = np.random.default_rng(20260729)

# --- measured inputs -------------------------------------------------------
px = rng.normal(962.0, 7.0, N)      # player ground x
py = rng.normal(602.0, 10.0, N)     # player ground y
cx = rng.normal(1024.7, 5.0, N)     # caster ground x (ring centre)
cy = rng.normal(568.5, 5.0, N)      # caster ground y
k = rng.uniform(0.60, 0.85, N)      # camera pitch ratio b/a
spd = rng.normal(13.55, 0.35, N)    # lance-A screen speed px/frame
sysf = rng.normal(1.0, 0.05, N)     # systematic on the scale (sprite lead / stall count)

UX, UY = -0.905, 0.4264             # lance-A screen unit direction
vx, vy = spd * UX, spd * UY
s = np.sqrt(vx ** 2 + (vy / k) ** 2) / (14.0 / 60.0) * sysf

dx, dy = px - cx, py - cy
rho = np.sqrt(dx ** 2 + (dy / k) ** 2)
r = rho / s

qs = [1, 2.5, 5, 16, 50, 84, 95, 97.5, 99]
out = dict(
    n=N,
    r_median_m=float(np.median(r)),
    r_mean_m=float(r.mean()),
    r_percentiles_m={str(q): float(np.percentile(r, q)) for q in qs},
    p_inside_1p804=float((r <= 1.804).mean()),
    p_in_2p50_3p919=float(((r >= 2.50) & (r <= 3.919)).mean()),
    p_inside_3p919=float((r <= 3.919).mean()),
    p_at_or_beyond_5p0=float((r >= 5.0).mean()),
    s_px_per_m_x_median=float(np.median(s)),
    s_px_per_m_y_median=float(np.median(s * k)),
)
print(json.dumps(out, indent=1))
json.dump(out, open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                    "galadriel/captures/2026-07-29-wr1-gal3/range-mc.json", "w"), indent=1)
