"""W intent on our clean alpha masks, with explicit provisional/identity limits.

Ground proximity defines stance for registered in-place sprites: the reference
plate's stationary-x selector is unsuitable for scrolling planted feet. Frozen
landmark extraction and temporal identity tracking are reused without edits.
"""
import json
import numpy as np
from PIL import Image
from .common import result
from oracle.motion_map import frame_paths, alpha_box
from oracle.walk_landmarks import figure_mask, track_landmarks_otsu_stance_lineage
from oracle.walk_curves import measure_sequence, bob


def evaluate(frames_dir, bands_walk_row, phase_table):
    row = bands_walk_row; b = row.get('bands', row)
    alpha_box(frames_dir)  # registered 512 alpha/key validation
    paths = frame_paths(frames_dir)
    if len(paths) != 12 or len(phase_table) != 12:
        raise ValueError('gait intent requires 12 frames and 12 candidate phases')
    masks = []
    for path in paths:
        with Image.open(path) as im: masks.append(figure_mask(np.array(im.convert('RGBA'))))
    seq = track_landmarks_otsu_stance_lineage(masks)
    data = measure_sequence(seq)
    s = data['summary']; results = []
    def add(name, value, threshold=None, op='<=', unit='fraction_H', detail=None):
        note = dict(detail or {})
        note['committed'] = row.get('committed') is True
        r = result(name, frames_dir, value, threshold, op=op, unit=unit,
                   notes=json.dumps(note, allow_nan=False, sort_keys=True))
        if row.get('committed') is not True: r['passed'] = None
        results.append(r)
    def bounded(name, value, band):
        for key, op in [('floor','>='),('ceiling','<=')]:
            if band.get(key) is not None:
                add(name+'_'+key, value, band[key], op, detail=band)
    bounded('W1', s['W1'], b.get('W1',{}))
    # Phases are explicit candidate labels; compare both the full schedule and
    # extrema phase sets against the row, without rotating or fitting the cycle.
    actual = [p.get('phase') if isinstance(p,dict) else p for p in phase_table]
    expected = [p.get('phase') for p in row.get('phase_table', [])]
    valid = all(p in ('CONTACT','DOWN','PASSING','UP') for p in actual)
    ext = bob([d['head_top_y'] for d in seq], s['H_median'], [{'phase':p} for p in actual])['W2']
    w2 = b.get('W2', {})
    w2 = w2.get('bands', w2.get('value', w2))
    match = None
    if valid and len(expected)==12 and all(p is not None for p in expected) and w2:
        match = actual == expected and all(
            {p['phase'] for p in ext[k]} == {p['phase'] for p in w2.get(k, [])} for k in ('min','max'))
    add('W2', match, True, '==', 'phase_match', dict(observed_extrema=ext, expected_extrema=w2,
        candidate_phases=actual, expected_phases=expected, inferred_contact_phases=data['phase_table']))
    add('W3a', s['W3a'], b.get('W3a',{}).get('ceiling',.35))
    bounded('W3c', s['W3c'], dict(floor=2,ceiling=3))
    add('W4', s['W4'], 2, '==', 'minima_count')
    # Never guess which screen track holds the weapon. Both hypothetical role
    # screens are numeric; the actual per-arm role gate requires assignment.
    assignment = b.get('W5_role_limits',{}).get('assignment') or row.get('arm_roles',{})
    if isinstance(assignment,dict) and 'weapon_arm' in assignment:
        assignment = {side:role for role,side in assignment.items()}
    for side in ('L','R'):
        value = (s.get('W5') or {}).get(side)
        role = assignment.get(side) if isinstance(assignment,dict) else None
        limits = {'free_arm':dict(floor=.08,ceiling=.20), 'weapon_arm':dict(floor=.03,ceiling=None)}
        if role in limits:
            bounded('W5_'+side, value, limits[role])
        else:
            add('W5_'+side, value, detail=dict(reason='anatomical arm role unassigned',
                free_arm_limits=limits['free_arm'], weapon_arm_limits=limits['weapon_arm'],
                identity_note=s.get('identity_note')))
    add('W6', s['W6'], .75, '>=', 'opposed_fraction', dict(per_arm=s.get('W6_per_arm'),
        minimum_opposed_frames=9,total_frames=12,identity_note=s.get('identity_note')))
    scroll = (s.get('sole_scroll') or {}).get('planted_scroll_lineage',{})
    limit = b.get('planted_sole_slip',{}).get('ceiling')
    for side in ('L','R'):
        info = scroll.get(side,{})
        add('planted_sole_slip_'+side, info.get('slip_rms_px_per_frame'), limit,
            unit='px_per_frame', detail=dict(info, reason='no registered slip ceiling' if limit is None else None))
    return results
