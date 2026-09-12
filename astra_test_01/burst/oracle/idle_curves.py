"""Idle displacement curves and provisional summaries, without shipping verdicts.

Default eps is measured feet-energy p95, floor is 3*eps. Both may be
explicitly overridden. Period requires >=2 cycles; geometric series use
median-profile translation, while changed-pixel lineage remains available.
"""
import numpy as np
from scipy.signal import find_peaks

from gates.common import result
from .motion_map import camera_shift, load_frames, motion_energy

TAU = 12.
EPS = None
FLOOR = None
CALIBRATION = ('tau=12 max-RGB units; default eps=clip feet-energy p95; '
               'default floor=3*eps; MOTION requires strict > both. '
               'Median RGB profile-gradient displacement; apparent contour edges. '
               'No committed shipping bands.')


def amplitude(signal):
    a = np.array([v for v in signal if v is not None], dtype=float)
    a = a[np.isfinite(a)]
    return float(np.percentile(a, 95)-np.percentile(a, 5)) if a.size else None


def period(signal, fps):
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError('fps must be finite and positive')
    a = np.asarray(signal, dtype=float)
    if a.ndim != 1 or len(a) < 6 or not np.isfinite(a).all() or np.ptp(a) < 1e-12:
        return None, None, 0.
    a = a-a.mean()
    limit = len(a)//2
    values = [1.]
    for lag in range(1, limit+2):
        x, y = a[:-lag], a[lag:]
        denom = np.linalg.norm(x)*np.linalg.norm(y)
        values.append(float(np.dot(x, y)/denom) if denom > 1e-12 else 0.)
    peaks = [int(i) for i in find_peaks(values)[0] if 2 <= i <= limit]
    if not peaks:
        return None, None, 0.
    best = max(values[i] for i in peaks)
    # Earliest near-best peak avoids reporting a multiple of a repeated cycle.
    p = next(i for i in peaks if values[i] >= best-.02)
    confidence = float(np.clip(values[p], 0., 1.))
    if confidence < .3:
        return None, None, confidence
    return p, float(p/fps), confidence


def classify_regions(energy_by_region, eps=EPS, floor=FLOOR):
    if eps is None:
        eps = float(np.percentile(energy_by_region['feet'], 95))
    if floor is None:
        floor = 3*eps
    if not np.isfinite(eps) or not 0 <= eps <= 1 or not np.isfinite(floor) or floor < 0:
        raise ValueError('eps must be in [0,1]; floor must be finite and nonnegative')
    lock, motion = [], []
    for name, series in energy_by_region.items():
        a = np.asarray(series, dtype=float)
        if not a.size or not np.isfinite(a).all() or np.any((a < 0) | (a > 1)):
            raise ValueError('regional energies must be nonempty finite fractions')
        moving = amplitude(a) > eps and float(np.percentile(a, 95)) > floor
        (motion if moving else lock).append(name)
    return {'LOCK': lock, 'MOTION': motion, 'moving_count': len(motion)}


def curves(frames_dir, box, fps, tau=TAU, eps=EPS, floor=FLOOR, control_box=None, ours=False):
    frames = load_frames(frames_dir)
    data = motion_energy(frames, box, tau, control_box)
    derived_eps = float(np.percentile(data['energy_by_region']['feet'], 95))
    eps_source, floor_source = ('feet_p95' if eps is None else 'override'), ('3*eps' if floor is None else 'override')
    eps = derived_eps if eps is None else eps
    floor = 3*eps if floor is None else floor
    shifts = camera_shift(frames)
    void = [] if ours else [i for i, shift in enumerate(shifts) if np.linalg.norm(shift) > 1.]
    pf, ps, confidence = period(data['chest_dw_H'], fps)
    classification = classify_regions(data['energy_by_region'], eps, floor)
    summary = {'breath_amplitude_H': amplitude(data['chest_dw_H']),
               'breath_period_frames': pf, 'breath_period_s': ps,
               'period_confidence': confidence, 'head_sway_H': amplitude(data['head_dy_H']),
               **classification, 'passed': None}
    contaminated = data['contamination_infinite'] or (data['contamination'] is not None and data['contamination'] > .5)
    reasons = (['background_motion'] if contaminated else []) + (['camera_shift'] if void else [])
    if data['control_box'] is None:
        reasons.append('control_box_unavailable')
    summary.update({'reason': reasons[0] if reasons else None, 'reasons': reasons,
                    'contamination': data['contamination'],
                    'contamination_infinite': data['contamination_infinite']})
    note = ('VOID: camera shift >1 source pixel; numbers are diagnostic only'
            if void else 'Descriptive measurement only; no acceptance verdict')
    if contaminated:
        note = 'background_motion; control/figure median energy >0.5; ' + note
    if data['control_box'] is None:
        note = 'control_box_unavailable; ' + note
    data.update({'fps': float(fps), 'frames': len(frames), 'eps': float(eps),
                 'floor': float(floor),
                 'noise_calibration': {'feet_p95': derived_eps, 'eps_source': eps_source,
                                       'floor_source': floor_source},
                 ('figure_drift_px' if ours else 'camera_shift_px'): shifts,
                 'mode': 'ours' if ours else 'ref',
                 'void_frames': void, 'frame_status': ['VOID' if i in void else 'MEASURED'
                                                     for i in range(len(frames))],
                 'summary': summary, 'calibration_note': CALIBRATION,
                 'result': result('oracle_idle', frames_dir, notes=note, unit='fraction_H')})
    return data
