"""Named element hue bands, measured with alpha*HSV-value weights.

Dominant hue is the mode of a circular 1-degree histogram smoothed +/-5
degrees; the circular mean within that modal neighbourhood gives the angle.
Achromatic pixels have no hue and are excluded, not assigned hue zero.
"""
import numpy as np

from gates.vfx_lifecycle import _frames, _result

ELEMENT_BANDS = {'frost': (180., 230.), 'fire': (0., 45.)}
CHROMATIC_SATURATION_MIN = .15
PHYSICAL_SATURATION_MAX = .20
HUE_BIN_DEGREES = 1.
MODE_RADIUS_DEGREES = 5


def _hsv(a):
    rgb = a[..., :3].astype(float)/255
    maximum, minimum = rgb.max(axis=2), rgb.min(axis=2)
    delta = maximum-minimum
    saturation = np.divide(delta, maximum, out=np.zeros_like(delta), where=maximum > 0)
    safe = np.where(delta > 0, delta, 1)
    r, g, b = np.moveaxis(rgb, -1, 0)
    hue = np.where(maximum == r, ((g-b)/safe) % 6,
                   np.where(maximum == g, (b-r)/safe+2, (r-g)/safe+4))*60
    return hue % 360, saturation, maximum


def evaluate(frames, element='frost'):
    """Dominant emissive hue vs inclusive band; physical uses weighted saturation.

    The full chromatic emission votes for dominance. Measuring only pixels
    already inside the requested band would conceal a wrong-element effect.
    In-band energy fraction is also reported, with no invented fraction gate.
    """
    if element not in (*ELEMENT_BANDS, 'physical'):
        raise ValueError('Unknown element')
    frames = _frames(frames)
    histogram = np.zeros(360)
    circular_sin, circular_cos = np.zeros(360), np.zeros(360)
    total, sat_sum, chromatic_total, in_band = 0., 0., 0., 0.
    per_frame = []
    for a in frames:
        hue, sat, value = _hsv(a)
        weight = a[..., 3].astype(float)/255*value
        total += float(weight.sum()); sat_sum += float((weight*sat).sum())
        chromatic = (sat >= CHROMATIC_SATURATION_MIN) & (weight > 0)
        weights = weight[chromatic]; hues = hue[chromatic]
        chromatic_total += float(weights.sum())
        bins = np.floor(hues).astype(int)
        histogram += np.bincount(bins, weights=weights, minlength=360)
        circular_sin += np.bincount(bins, weights=weights*np.sin(np.deg2rad(hues)), minlength=360)
        circular_cos += np.bincount(bins, weights=weights*np.cos(np.deg2rad(hues)), minlength=360)
        if element in ELEMENT_BANDS:
            lo, hi = ELEMENT_BANDS[element]
            mass = float(weights[(hues >= lo) & (hues <= hi)].sum())
            in_band += mass
            per_frame.append(mass/float(weights.sum()) if weights.sum() else None)
    details = dict(element=element, weight='alpha*HSV_value',
                   chromatic_saturation_min=CHROMATIC_SATURATION_MIN,
                   emissive_weight=total, chromatic_weight=chromatic_total)
    if element == 'physical':
        return _result('element_hue', element, sat_sum/total if total else None,
                       PHYSICAL_SATURATION_MAX, unit='weighted_saturation',
                       **details, reason=None if total else 'No emissive energy')
    if not chromatic_total:
        return _result('element_hue', element, unit='degrees', **details,
                       reason='No chromatic emissive pixels; hue is undefined')
    smoothed = sum(np.roll(histogram, k) for k in range(-MODE_RADIUS_DEGREES, MODE_RADIUS_DEGREES+1))
    mode = int(np.argmax(smoothed))
    bins = (mode+np.arange(-MODE_RADIUS_DEGREES, MODE_RADIUS_DEGREES+1)) % 360
    z = np.sum(circular_cos[bins])+1j*np.sum(circular_sin[bins])
    dominant = float(np.rad2deg(np.angle(z)) % 360)
    if abs(dominant-360) < 1e-10:
        dominant = 0.
    lo, hi = ELEMENT_BANDS[element]
    row = _result('element_hue', element, dominant, unit='degrees', **details,
                  band_degrees=[lo, hi], in_band_fraction=in_band/chromatic_total,
                  per_frame_in_band_fraction=per_frame, histogram_bin_degrees=HUE_BIN_DEGREES,
                  modal_radius_degrees=MODE_RADIUS_DEGREES)
    row.update(threshold=[lo, hi], op='within', passed=bool(lo-1e-10 <= dominant <= hi+1e-10))
    return row
