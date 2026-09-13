"""C-3 VFX lifecycle instruments; literal G6 never replaced by G6b.

Energy is sum(alpha * Rec.709 luma of straight RGB), in byte-luma units.
Only floating-point roundoff is tolerated in monotonic curves. Symmetry is
reported without a verdict: the contract supplies no committed symmetry band.
"""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

from gates.g6_seam import evaluate as seam_evaluate
from oracles.pse_check import check as pse_check

COUNTS = {'cast': 8, 'travel': 6, 'impact': 10}
CAST_FPS = 20
FINAL_ALPHA_FRACTION = .005
LUMA = np.array([.2126, .7152, .0722])
BACKGROUND = (58, 63, 74)
ENERGY_ROUNDOFF_REL = 1e-12


def _frames(frames):
    """Read paths, Pillow RGBA images, or uint8 RGBA arrays without mutation."""
    if isinstance(frames, (str, Path)):
        frames = sorted(Path(frames).glob('*.png'))
    arrays = []
    for frame in frames:
        if isinstance(frame, (str, Path)):
            with Image.open(frame) as im:
                a = np.array(im)
        else:
            a = np.asarray(frame)
        if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] != 4 or min(a.shape[:2]) < 1:
            raise ValueError('Nonempty uint8 RGBA frames required')
        if arrays and a.shape != arrays[0].shape:
            raise ValueError('All frames must have the same canvas')
        arrays.append(a)
    return arrays


def _result(name, subject, value=None, threshold=None, op='<=', unit='', **details):
    passed = None
    if value is not None and threshold is not None:
        passed = bool({'<=': lambda: value <= threshold,
                       '>=': lambda: value >= threshold,
                       '==': lambda: value == threshold}[op]())
    return dict(id=name, subject=subject, passed=passed, value=value,
                threshold=threshold, op=op, unit=unit, evidence=[],
                notes=json.dumps(details, sort_keys=True, allow_nan=False))


def _fps(fps):
    if isinstance(fps, bool) or not math.isfinite(float(fps)) or float(fps) <= 0:
        raise ValueError('fps must be finite and positive')
    return float(fps)


def _emission(frame):
    return frame[..., :3].astype(float) * (frame[..., 3:4].astype(float)/255.)


def sequence_pse(frames, fps, subject='', loop=False):
    """Temporal screen over the review background; loops include seam events.

    A loop is repeated for at least two seconds plus its closing first frame.
    Viewport is the actual frame canvas, not an assumed larger game viewport.
    The inherited spatial-pattern instrument remains explicitly unevaluable.
    """
    fps = _fps(fps)
    frames = _frames(frames)
    rgb = [np.rint(_emission(a) + np.asarray(BACKGROUND)*
                   (1-a[..., 3:4].astype(float)/255)).clip(0, 255).astype(np.uint8)
           for a in frames]
    if loop and rgb:
        rgb = rgb * max(2, math.ceil(2*fps/len(rgb))) + rgb[:1]
    return pse_check(rgb, fps, subject=subject)


def _curve(energy, module):
    if not energy or max(energy) <= 0:
        return _result('vfx.energy_curve', module, reason='No emissive energy')
    peak = int(np.argmax(energy))
    tolerance = max(energy)*ENERGY_ROUNDOFF_REL
    delta = np.diff(energy)
    violations = int(np.count_nonzero(delta[:peak] < -tolerance) +
                     np.count_nonzero(delta[peak:] > tolerance))
    peak_count = sum(abs(e-energy[peak]) <= tolerance for e in energy)
    violations += int(peak in (0, len(energy)-1)) + int(peak_count != 1)
    violations += int(energy[0] >= energy[peak]-tolerance)
    violations += int(energy[-1] >= energy[peak]-tolerance)
    return _result('vfx.energy_curve', module, violations, 0, unit='violations',
                   energy=energy, peak_index=peak, peak_count=peak_count,
                   roundoff_relative=ENERGY_ROUNDOFF_REL,
                   definition='One interior peak; nondecreasing rise, nonincreasing release; endpoints below peak')


def evaluate(module, frames, fps):
    """Return §1 envelopes for count, lifecycle, and temporal PSE quantities."""
    if module not in COUNTS:
        raise ValueError('module must be cast, travel, or impact')
    fps = _fps(fps)
    frames = _frames(frames)
    rows = [_result('vfx.frame_count', module, len(frames), COUNTS[module],
                    op='==', unit='frames')]
    if module == 'cast':
        rows.append(_result('vfx.fps', module, fps, CAST_FPS, op='==', unit='fps'))
    energy = [float((_emission(a)@LUMA).sum()) for a in frames]
    if module in ('cast', 'impact'):
        rows.append(_curve(energy, module))
    if module == 'impact':
        alpha = [float(a[..., 3].sum()) for a in frames]
        peak = max(alpha, default=0.)
        fraction = alpha[-1]/peak if peak else None
        rows.append(_result('vfx.final_alpha_fraction', module, fraction,
                            FINAL_ALPHA_FRACTION, unit='fraction_of_peak_alpha',
                            alpha_sum=alpha, peak_alpha_sum=peak,
                            reason=None if peak else 'No nonzero alpha peak'))
    if module == 'travel':
        rows.extend(seam_evaluate([Image.fromarray(a) for a in frames], subject=module))
        scores, imbalance, centroids = [], [], []
        for a in frames:
            emission = _emission(a)
            total = float(emission.sum())
            if not total:
                scores.append(None); imbalance.append(None); centroids.append(None)
                continue
            # Sum |top-bottom mirror| / sum of both: 0 identical, 1 disjoint.
            scores.append(float(np.abs(emission-emission[::-1]).sum()/(2*total)))
            field = emission.sum(axis=2)
            h = field.shape[0]
            top, bottom = field[:h//2].sum(), field[(h+1)//2:].sum()
            imbalance.append(float(abs(top-bottom)/total))
            centroids.append(float((field*np.arange(h)[:, None]).sum()/total))
        measured = [s for s in scores if s is not None]
        rows.append(_result('vfx.top_bottom_mirror_diff', module,
                            max(measured) if measured else None, unit='normalized_emission_L1',
                            per_frame=scores, top_bottom_energy_imbalance=imbalance,
                            vertical_emission_centroid=centroids,
                            proposed=True, committed=False,
                            reason='Report only: no committed symmetry threshold; 0 identical, 1 disjoint'))
    rows.append(sequence_pse(frames, fps, module, loop=module == 'travel'))
    return rows
