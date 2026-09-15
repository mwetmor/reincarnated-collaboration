"""T4d clean-plate white measurements, in percent of a native 960x540 crop.

White is exactly HSV V > .95 and S < .20. Attributable pixels are white in
an effect capture and NOT white at the same pixel in its clean plate. This
spatial difference never cancels new white against baseline white that vanished.
The peak is the FIRST maximum attributable-white frame; total and baseline at
that SAME frame are reported. Clip means are arithmetic frame means, including
empty frames. No threshold on an acceptable white percentage is invented.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

from oracle.vfx_measure import _row

CROP_WH = (960, 540)


def _rgb(source):
    if isinstance(source, (str, Path)):
        with Image.open(source) as im:
            if im.mode not in ('RGB', 'RGBA'):
                raise ValueError('capture must be RGB or opaque RGBA')
            a = np.array(im)
    elif isinstance(source, Image.Image):
        a = np.array(source)
    else:
        a = np.asarray(source)
    if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] not in (3, 4):
        raise ValueError('capture must be uint8 RGB or opaque RGBA')
    if a.shape[2] == 4 and np.any(a[..., 3] != 255):
        raise ValueError('capture must be composited over its clean plate (opaque alpha)')
    return a[..., :3]


def crop_bounds(impact_xy, canvas_wh):
    """Native crop; nearest integer centre via floor(x+.5), no clamp/padding."""
    if len(impact_xy) != 2 or any(isinstance(x, (bool, np.bool_)) or not math.isfinite(x) for x in impact_xy):
        raise ValueError('impact_xy must be a finite pair')
    cx, cy = (math.floor(float(x)+.5) for x in impact_xy)
    w, h = CROP_WH
    x, y = cx-w//2, cy-h//2
    if x < 0 or y < 0 or x+w > canvas_wh[0] or y+h > canvas_wh[1]:
        raise ValueError('centred 960x540 crop is outside capture; no padding or clamping')
    return [x, y, x+w, y+h]


def white_mask(rgb):
    """Exact integer equivalent of V > .95 and S < .20; no HSV rounding."""
    rgb = _rgb(rgb).astype(np.int16)
    hi, lo = rgb.max(axis=-1), rgb.min(axis=-1)
    return (hi > .95*255) & (5*(hi-lo) < hi)


def _counts(total, baseline, attributable, removed, denominator):
    return {name: {'pixels': float(n) if isinstance(n, (float, np.floating)) else int(n),
                   'percent': float(n)*100/denominator}
            for name, n in [('total', total), ('baseline', baseline),
                            ('attributable', attributable), ('removed_baseline', removed)]}


def measure(plate, frames, impact_xy, subject='white'):
    """Measure aligned fixture captures. A fixed clean plate pairs with all frames.

    ``frames`` is a nonempty iterable of paths, PIL images or uint8 captures.
    Caller supplies the actual flash/cast captures; this tool never synthesizes
    flash-off, simultaneous or staggered cases from a single captured run.
    """
    clean = _rgb(plate)
    box = crop_bounds(impact_xy, (clean.shape[1], clean.shape[0]))
    x0, y0, x1, y1 = box
    baseline = white_mask(clean[y0:y1, x0:x1])
    base_n = int(baseline.sum())
    denominator = CROP_WH[0]*CROP_WH[1]
    series = []
    for index, source in enumerate(frames):
        capture = _rgb(source)
        if capture.shape != clean.shape:
            raise ValueError('plate and effect capture dimensions must agree')
        mask = white_mask(capture[y0:y1, x0:x1])
        row = _counts(mask.sum(), base_n, np.count_nonzero(mask & ~baseline),
                      np.count_nonzero(baseline & ~mask), denominator)
        row['frame'] = index
        series.append(row)
    if not series:
        raise ValueError('at least one effect capture is required')
    peak_index = max(range(len(series)), key=lambda i: series[i]['attributable']['pixels'])
    mean = _counts(*(np.mean([r[k]['pixels'] for r in series])
                     for k in ('total', 'baseline', 'attributable', 'removed_baseline')), denominator)
    evidence = [str(plate)] if isinstance(plate, (str, Path)) else []
    return dict(subject=subject, crop_origin_xy=box[:2], crop_bounds_xyxy=box,
                crop_wh=list(CROP_WH), impact_xy=list(map(float, impact_xy)),
                denominator_px=denominator, classifier='V > 0.95 and S < 0.20',
                attribution='effect_white AND NOT clean_plate_white; exact spatial differencing',
                peak_rule='first maximum attributable white; all peak quantities at that frame',
                mean_rule='arithmetic mean over every captured frame', n_frames=len(series),
                peak=series[peak_index], mean=mean, per_frame=series,
                results=[_row('white_'+kind, subject, value, 'percent_of_crop',
                              'Measurement only; no white budget supplied.', evidence)
                         for kind, value in [('peak', series[peak_index]), ('mean', mean)]])


def measure_cases(cases):
    """Mapping label -> {plate, frames, impact_xy, flash, cast_pattern}.

    Optional labels/metadata identify flash on/off and synchronised/staggered
    four-cast captures. Missing cases remain absent, never inferred as zero.
    """
    if not cases:
        raise ValueError('at least one case is required')
    results = {}
    for name, case in cases.items():
        result = measure(case['plate'], case['frames'], case['impact_xy'], subject=name)
        result['flash'] = case.get('flash')
        result['cast_pattern'] = case.get('cast_pattern')
        result['cast_count'] = case.get('cast_count')
        results[name] = result
    return results


def baseline(plate, impact_xy, subject='empty_crop'):
    """The clean crop itself: attributable white is identically zero."""
    return measure(plate, [plate], impact_xy, subject)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path, help='JSON mapping of named capture cases')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args(argv)
    data = measure_cases(json.loads(args.manifest.read_text()))
    text = json.dumps(data, indent=2, allow_nan=False)+'\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
