#!/usr/bin/env python3
"""SHADOW-CAL controls for SC-4.

POSITIVE: a synthetic scene of boxes on textured ground, all shadowed from ONE
known azimuth at a known ratio, rendered through the GAL-CAM pinhole.  SC-4 must
return that azimuth.

NULL: the SAME scene with the shadows removed (occluders only, flat lighting).
SC-4 must NOT return a confident azimuth -- if it does, its "measurement" on the
footage is an artefact of the occluders' own shapes, not of any light.

SECOND NULL: the same scene with each box given its OWN random shadow azimuth.
The instrument must report a large circular spread.
"""
import argparse
import math

import numpy as np
from scipy import ndimage

import sc_cam
import sc_ray
from sc_synth import box_points, rasterise


def scene(cam, az_deg, ratio=1.15, n_box=26, seed=3, per_box_random=False,
          with_shadow=True, shape=(1080, 1920)):
    rng = np.random.default_rng(seed)
    # textured ground
    g = rng.normal(78, 13, (shape[0] // 8, shape[1] // 8))
    g = ndimage.zoom(g, 8, order=3)[:shape[0], :shape[1]]
    g += rng.normal(0, 3.5, shape)
    img = np.clip(np.stack([g * 0.95, g, g * 0.85], -1), 5, 250)
    figs = np.zeros(shape, bool)
    shas = np.zeros(shape, bool)
    for i in range(n_box):
        sx = rng.uniform(220, 1700)
        sy = rng.uniform(240, 860)
        gp = cam.unproject_ground([[sx, sy]])
        h = rng.uniform(1.5, 2.6)
        w = rng.uniform(0.4, 0.9)
        d = rng.uniform(0.3, 0.7)
        P = box_points((float(gp[0]), float(gp[2])), h, w=w, d=d)
        figs |= rasterise(cam, P)
        if with_shadow:
            aa = math.radians(rng.uniform(0, 360) if per_box_random else az_deg)
            S = P.copy()
            S[:, 0] += P[:, 1] * ratio * math.cos(aa)
            S[:, 2] += P[:, 1] * ratio * math.sin(aa)
            S[:, 1] = 0.0
            shas |= rasterise(cam, S)
    shas &= ~figs
    img[shas] *= 0.42
    img[figs] = img[figs] * 0.25 + np.array([120, 105, 95]) * 0.75
    return np.clip(img, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=None)
    a = ap.parse_args()
    cam = sc_cam.nominal()
    print(f"{'control':<34}{'kept':>6}{'azimuth':>10}{'sd':>8}{'R':>8}  verdict")
    for truth in (-150.0, -90.0, 20.0, 140.0):
        img = scene(cam, truth)
        D = sc_ray.dipoles(img, cam)
        keep = [d for d in D if d["amp"] >= 0.055]
        m, sd, Rl = sc_ray.circ([d["phi"] for d in keep], [d["amp"] for d in keep])
        err = (m - truth + 180) % 360 - 180
        print(f"POSITIVE truth {truth:+7.1f}{'':<12}{len(keep):>6}{m:>10.2f}"
              f"{sd:>8.2f}{Rl:>8.3f}  err {err:+.2f} deg")
        if a.outdir:
            from PIL import Image
            Image.fromarray(img).save(f"{a.outdir}/ctrl_pos_{int(truth)}.jpg",
                                      quality=88)
    img = scene(cam, 0.0, with_shadow=False)
    D = sc_ray.dipoles(img, cam)
    keep = [d for d in D if d["amp"] >= 0.055]
    if len(keep) >= 8:
        m, sd, Rl = sc_ray.circ([d["phi"] for d in keep], [d["amp"] for d in keep])
        print(f"{'NULL  no shadows at all':<34}{len(keep):>6}{m:>10.2f}"
              f"{sd:>8.2f}{Rl:>8.3f}  <- must be diffuse")
    else:
        print(f"{'NULL  no shadows at all':<34}{len(keep):>6}{'':>10}{'':>8}{'':>8}"
              f"  <- nothing survived the gate")
    img = scene(cam, 0.0, per_box_random=True)
    D = sc_ray.dipoles(img, cam)
    keep = [d for d in D if d["amp"] >= 0.055]
    m, sd, Rl = sc_ray.circ([d["phi"] for d in keep], [d["amp"] for d in keep])
    print(f"{'NULL  per-box random azimuth':<34}{len(keep):>6}{m:>10.2f}"
          f"{sd:>8.2f}{Rl:>8.3f}  <- must be diffuse")
    if a.outdir:
        from PIL import Image
        Image.fromarray(img).save(f"{a.outdir}/ctrl_null_random.jpg", quality=88)
        Image.fromarray(scene(cam, 0.0, with_shadow=False)).save(
            f"{a.outdir}/ctrl_null_noshadow.jpg", quality=88)
