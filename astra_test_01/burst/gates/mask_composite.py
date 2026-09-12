"""Region-limited RGBA replacement and the literal G12 preservation gate.

All inputs are registered 512 x 512 frames; no resizing or registration occurs.
Boxes are integer (x0, y0, x1, y1), with exclusive upper bounds. Outputs are
Pillow RGBA images and numpy boolean masks. Replacement copies all four bytes,
including transparent pixels, so a moved limb can erase its old position.

Calibration: thresh=8 (0..255 units) and dilate_px=2 are provisional synthetic
settings, exercised against block translations, alpha-only changes, threshold
boundaries and local repaint controls in test_gates_mask_composite.py. They are
not calibrated on generated candidates. Dilation uses a square neighbourhood
(Chebyshev pixel radius), clipped to the declared box AFTER dilation. Difference
is max(max-channel premultiplied RGB difference, alpha difference); hidden RGB
at alpha zero is ignored, while even black-pixel alpha changes remain visible.
The 0.99 preservation and 0.60 coverage defaults are the pre-registered SPEC
limits, not fitted thresholds. Callers overriding parameters must record them.
"""
import json
from numbers import Integral, Real

import numpy as np
from PIL import Image
from scipy import ndimage

from .common import result, rgba


def _frame(image):
    if isinstance(image, np.ndarray):
        if image.dtype != np.uint8 or image.shape != (512, 512, 4):
            raise ValueError('array frames must be uint8 RGBA with shape (512, 512, 4)')
        return image.copy()
    image = rgba(image)
    if image.size != (512, 512):
        raise ValueError('frames must be registered on a 512 x 512 canvas')
    return np.array(image)


def _number(value, name, low, high):
    if (isinstance(value, (bool, np.bool_)) or not isinstance(value, Real)
            or not np.isfinite(value) or not low <= value <= high):
        raise ValueError(f'{name} must be finite and in [{low}, {high}]')
    return float(value)


def _region(region_box):
    try:
        coords = tuple(region_box)
    except TypeError as exc:
        raise ValueError('region_box must contain four integer XYXY coordinates') from exc
    if len(coords) != 4 or any(isinstance(v, (bool, np.bool_)) or
                               not isinstance(v, Integral) for v in coords):
        raise ValueError('region_box must contain four integer XYXY coordinates')
    x0, y0, x1, y1 = map(int, coords)
    if not (0 <= x0 < x1 <= 512 and 0 <= y0 < y1 <= 512):
        raise ValueError('region_box must be nonempty and within the 512 canvas')
    region = np.zeros((512, 512), dtype=bool)
    region[y0:y1, x0:x1] = True
    return region, [x0, y0, x1, y1]


def _difference(base, variant):
    a, b = base.astype(np.int32), variant.astype(np.int32)
    rgb = np.max(np.abs(a[..., :3] * a[..., 3:4] -
                           b[..., :3] * b[..., 3:4]), axis=2) / 255.0
    return np.maximum(rgb, np.abs(a[..., 3] - b[..., 3]))


def _metrics(base, out, mask):
    identical = np.all(base == out, axis=2)
    outside = ~mask
    outside_pixels = int(outside.sum())
    mask_pixels = int(mask.sum())
    figure = base[..., 3] >= 128
    figure_pixels = int(figure.sum())
    covered = int(np.count_nonzero(mask & figure))
    changed_inside = int(np.count_nonzero(mask & ~identical))
    changed_outside = int(np.count_nonzero(outside & ~identical))
    return {
        'mask_pixels': mask_pixels,
        'mask_area_fraction': float(mask.mean()),
        'outside_mask_pixels': outside_pixels,
        'outside_mask_changed_pixels': changed_outside,
        'outside_mask_byte_identical': bool(changed_outside == 0),
        'base_preserved_fraction': (float(1 - changed_outside / outside_pixels)
                                    if outside_pixels else None),
        'changed_inside_pixels': changed_inside,
        'changed_inside_fraction': (float(changed_inside / mask_pixels)
                                    if mask_pixels else 0.0),
        'figure_pixels': figure_pixels,
        'mask_figure_pixels': covered,
        'mask_figure_fraction': float(covered / figure_pixels) if figure_pixels else None,
    }


def composite(base_rgba, variant_rgba, region_box, thresh=8, dilate_px=2):
    """Paste variant bytes only in the thresholded, dilated, box-limited mask.

    Difference seeds are selected with strict ``difference > thresh``. Dilation
    precedes box restriction, as in SPEC. Outside-box seeds may therefore grow
    into the box, but no pixel outside the box can be pasted. Dropped counts
    report both any visible out-of-box changes and those above the threshold.
    Neither input is mutated. Preservation compares all RGBA bytes, including
    hidden RGB; no alpha blending, feathering or transparent-RGB cleanup occurs.
    """
    base, variant = _frame(base_rgba), _frame(variant_rgba)
    thresh = _number(thresh, 'thresh', 0, 255)
    if (isinstance(dilate_px, (bool, np.bool_)) or
            not isinstance(dilate_px, Integral) or dilate_px < 0):
        raise ValueError('dilate_px must be a nonnegative integer')
    dilate_px = int(dilate_px)
    region, box = _region(region_box)
    delta = _difference(base, variant)
    seeds = delta > thresh
    expanded = (ndimage.binary_dilation(seeds, structure=np.ones((3, 3), bool),
                                       iterations=dilate_px) if dilate_px else seeds)
    mask = expanded & region
    out = base.copy()
    out[mask] = variant[mask]
    # This is a hard implementation invariant, independent of G12's 0.99 bar.
    assert np.array_equal(out[~mask], base[~mask]), 'outside-mask RGBA bytes changed'
    metrics = _metrics(base, out, mask)
    metrics.update({
        'region_box': box, 'thresh': thresh, 'dilate_px': dilate_px,
        'thresholded_difference_pixels': int(seeds.sum()),
        'out_of_box_changed_pixels': int(np.count_nonzero((delta > 0) & ~region)),
        'dropped_out_of_box_pixels': int(np.count_nonzero(seeds & ~region)),
        'difference_definition': 'max(abs(premultiplied RGB), abs(alpha)); 0..255',
    })
    return Image.fromarray(out), mask, metrics


def evaluate(base, out, mask, subject='', min_preserved_fraction=0.99,
             max_mask_figure_fraction=0.60):
    """G12: exact outside-mask pixel equality / all outside-mask pixels.

    Figure coverage is mask intersection with BASE alpha >=128, divided by base
    support, not canvas area or a bounding box. Coverage strictly greater than
    0.60, no base figure, or no outside pixels makes the result UNEVALUABLE.
    The numeric preservation value is retained when available even in that case.
    """
    base, out = _frame(base), _frame(out)
    min_preserved_fraction = _number(min_preserved_fraction, 'min_preserved_fraction', 0, 1)
    max_mask_figure_fraction = _number(max_mask_figure_fraction, 'max_mask_figure_fraction', 0, 1)
    mask = np.asarray(mask)
    if mask.shape != (512, 512) or mask.dtype != np.bool_:
        raise ValueError('mask must be a boolean array with shape (512, 512)')
    metrics = _metrics(base, out, mask)
    metrics['min_preserved_fraction'] = min_preserved_fraction
    metrics['max_mask_figure_fraction'] = max_mask_figure_fraction
    reason = None
    if not metrics['figure_pixels']:
        reason = 'UNEVALUABLE: base has no alpha >=128 figure support'
    elif metrics['mask_figure_fraction'] > max_mask_figure_fraction:
        reason = 'UNEVALUABLE: mask exceeds the figure coverage limit; composite meaningless'
    elif not metrics['outside_mask_pixels']:
        reason = 'UNEVALUABLE: no outside-mask pixels to measure'
    metrics['reason'] = reason
    envelope = result('g12_base_preservation', subject,
                      metrics['base_preserved_fraction'], min_preserved_fraction,
                      op='>=', unit='fraction', notes=json.dumps(metrics, sort_keys=True))
    # common.result computes a verdict whenever value and threshold exist.
    # Explicitly restore null for the independently registered coverage guard.
    if reason is not None:
        envelope['passed'] = None
    return envelope


def compose_loop(base, variants, region_boxes, thresh=8, dilate_px=2):
    """Return one (RGBA image, boolean mask, metrics) tuple per variant.

    Each frame uses the SAME base (never the previous composite), preserving
    identity without accumulating edits. Require exactly one box per variant;
    no zip truncation or implicit box broadcasting. G12 can be applied to each
    returned tuple with the caller's animation/direction/frame subject string.
    """
    variants, region_boxes = list(variants), list(region_boxes)
    if len(variants) != len(region_boxes):
        raise ValueError('one region_box is required for each variant')
    base = _frame(base)
    return [composite(base, variant, box, thresh, dilate_px)
            for variant, box in zip(variants, region_boxes)]
