"""Deterministic synthetic O3b calibration, independent of real crop results."""
import numpy as np
from scipy import ndimage

RINGS = [(40, 48, 8), (108, 48, 14), (185, 70, 22)]

def rings(textured=False):
    y, x = np.mgrid[:144, :240]
    background = np.full(y.shape, 45.)
    if textured:
        rng = np.random.default_rng(90210)
        background += ndimage.gaussian_filter(rng.normal(0, 22, y.shape), .6)
        background += 9*np.sin(x/5)*np.cos(y/9)
    image = background.copy()
    for cx, cy, radius in RINGS:
        distance = np.abs(np.hypot(x-cx, y-cy)-radius)
        coverage = np.clip(2-distance, 0, 1)
        image = image*(1-coverage)+205*coverage
    return np.repeat(image[..., None], 3, axis=2).clip(0,255).astype('uint8')

def no_rings():
    a = np.full((192, 160, 3), 25, np.uint8)
    a[15:40, 67:92] = (180,160,130)
    a[40:115, 50:108] = (90,120,180)
    a[115:180, 50:72] = (75,90,110)
    a[115:180, 86:108] = (75,90,110)
    a[47:100, 25:50] = (130,140,150)
    a[47:100, 108:133] = (130,140,150)
    return a


def half_arcs():
    a = rings()
    for cx,cy,r in RINGS:
        a[cy:cy+r+4,cx-r-4:cx+r+5] = 45
    return a
