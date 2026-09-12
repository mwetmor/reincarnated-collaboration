"""Idle intent measured on registered sprites; provisional rows stay report-only.

Displacement classification uses vertical profile translation and both horizontal
contour translations. Static null profiles mean zero only for identical crops.
Sole displacement is the maximum pairwise symmetric mask distance in the feet
band (includes lateral slide, vertical lift and either sole, not just centroid).
"""
import json
import numpy as np
from scipy.ndimage import distance_transform_edt
from .common import result
from oracle.idle_curves import curves
from oracle.motion_map import (alpha_box, load_frames, band_shift_y, band_edges_x,
                               frame_paths, _matted)


def _span(values):
    values = [v for v in values if v is not None]
    return float(np.ptp(values)) if values else None


def evaluate(frames_dir, bands_idle_row, label):
    row = bands_idle_row
    box = alpha_box(frames_dir)
    H = box[3]-box[1]
    frames = load_frames(frames_dir)
    data = curves(frames_dir, box, row.get('provenance', {}).get('fps', 12), ours=True)
    checks = []
    def check(name, value, threshold, op, note=''):
        r = result(name, label, value, threshold, op=op, unit='fraction_H', notes=note)
        observed = r['passed']
        if row.get('committed') is not True:
            r['passed'] = None
            r['notes'] += '; uncommitted reference row; report only'
        checks.append(r)
        return observed
    outcomes = []
    measures = {}
    for name, key in [('breath', 'breath_amplitude_H'), ('head_bob', 'head_sway_H')]:
        value = data['summary'][key]
        # The frozen static profile estimator returns null for no movement.
        if value is None:
            band = 'head' if name == 'head_bob' else 'shoulders_chest'
            x0,y0,x1,y1 = data['regions'][band]
            if all(np.array_equal(f[y0:y1,x0:x1], frames[0][y0:y1,x0:x1]) for f in frames):
                value = 0.
        b = row[key]
        measures[name] = dict(value=value, **{k:b.get(k) for k in ('floor','target','ceiling')})
        measures[name]['below_floor'] = value < b['floor'] if value is not None and b.get('floor') is not None else None
        measures[name]['panting'] = value > b['ceiling'] if value is not None and b.get('ceiling') is not None else None
        outcomes += [check(name+'_minimum', value, b.get('floor'), '>='),
                     check(name+'_maximum', value, b.get('ceiling'), '<=', 'panting above ceiling')]
    lock_eps = float(row.get('lock_eps_H', row.get('lock_eps', .004)))
    if not np.isfinite(lock_eps) or lock_eps < 0:
        raise ValueError('lock_eps must be a finite nonnegative fraction of H')
    regions = {}; classification = {'LOCK': [], 'MOTION': [], 'UNEVALUABLE': []}
    for name, bounds in data['regions'].items():
        dy = band_shift_y(frames, box, name)
        edges = band_edges_x(frames, box, name)
        x0,y0,x1,y1 = bounds
        static = all(np.array_equal(f[y0:y1,x0:x1],frames[0][y0:y1,x0:x1]) for f in frames)
        spans = [_span(dy['dy_H']), _span(edges['left_H']), _span(edges['right_H'])]
        finite = [v for v in spans if v is not None]
        displacement = 0. if static else (max(finite) if finite else None)
        category = 'UNEVALUABLE' if displacement is None else 'LOCK' if displacement <= lock_eps else 'MOTION'
        classification[category].append(name)
        regions[name] = dict(displacement_H=displacement, dy_p2p_H=spans[0],
                             left_p2p_H=spans[1], right_p2p_H=spans[2], classification=category,
                             search_limit_frames=dict(vertical=dy['search_limit_frames'], horizontal=edges['search_limit_frames']))
    mismatches = [name for category,key in [('LOCK','lock_regions'),('MOTION','motion_regions')]
                  for name in row.get(key, []) if name not in classification[category]]
    region_result = result('idle_regions', label, len(mismatches), 0, op='==', unit='regions',
                           notes=json.dumps(dict(expected_LOCK=row.get('lock_regions',[]), expected_MOTION=row.get('motion_regions',[]), mismatches=mismatches)))
    outcomes.append(region_result['passed'])
    if row.get('committed') is not True: region_result['passed'] = None
    checks.append(region_result)
    x0,y0,x1,y1 = data['regions']['feet']
    masks = [_matted(p)[0][y0:y1,x0:x1,3] >= 128 for p in frame_paths(frames_dir)]
    sole = None
    if all(m.any() for m in masks):
        distances = [distance_transform_edt(~m) for m in masks]
        sole = max(float(dist[m].max()) for dist in distances for m in masks)/H
    outcomes.append(check('idle_feet_lock', sole, .0025, '<=', 'maximum pairwise sole-band mask distance; mandatory I-1'))
    invalid = data['summary']['reason'] == 'background_motion'
    passed = None if row.get('committed') is not True or invalid or any(v is None for v in outcomes) else all(outcomes)
    payload = dict(height_px=H, box=box, **measures, regions=regions, classification=classification,
                   lock_eps_H=lock_eps, sole_displacement_H=sole, checks=checks,
                   figure_drift_px=data['figure_drift_px'], contamination=data['contamination'])
    note = 'committed reference row' if row.get('committed') is True else 'uncommitted reference row; report only'
    if invalid:
        note += '; background_motion'
        for r in checks: r['passed'] = None
    return result('idle_intent', label, value=payload, passed=passed, unit='fraction_H', notes=note)
