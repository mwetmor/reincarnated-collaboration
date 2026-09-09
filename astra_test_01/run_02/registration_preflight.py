"""Preparation for future runs; never modifies frozen checkpoint evidence.

Use separately reviewed sole ROIs in the full source image. A clipped or empty
region is an error, not an inferred contact. This does not validate walking roots.
"""
import numpy as np


def sole_contacts(image, regions):
    mask = np.array(image.convert('RGBA'))[..., 3] >= 128
    points = []
    if len(regions) != 2:
        raise ValueError('Exactly two reviewed sole regions are required')
    for x0, y0, x1, y1 in regions:
        if not (0 <= x0 < x1 <= image.width and 0 <= y0 < y1 <= image.height):
            raise ValueError('Sole region outside image')
        roi = mask[y0:y1, x0:x1]
        yy, xx = np.where(roi)
        if not len(yy):
            raise ValueError('Empty sole region')
        bottom = int(yy.max())
        if bottom >= roi.shape[0] - 1:
            raise ValueError('Sole region clips the contact; review the region')
        low_x = xx[yy >= bottom - 1]
        if low_x.min() == 0 or low_x.max() == roi.shape[1] - 1:
            raise ValueError('Sole region clips the contact horizontally')
        points.append([float(np.median(low_x) + x0), float(bottom + y0)])
    return points


def measured_anchor(image, regions):
    return np.mean(sole_contacts(image, regions), axis=0).tolist()


def preflight(image, regions, pivot=(256, 400), tolerance=4):
    points = sole_contacts(image, regions)
    midpoint = np.mean(points, axis=0)
    error = np.abs(midpoint - pivot)
    return {'points': points, 'midpoint': midpoint.tolist(),
            'error_xy': error.tolist(), 'pass': bool((error <= tolerance).all())}
