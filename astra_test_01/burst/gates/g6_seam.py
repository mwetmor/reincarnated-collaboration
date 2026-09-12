"""Report literal G6 and median-internal G6b without substituting either."""
import json
import numpy as np
from .common import pair_differences, result

def evaluate(frames, subject=''):
    if len(frames)<3:
        return [result(k,subject,notes='UNEVALUABLE: at least three frames required') for k in ('g6_seam','g6b')]
    pairs=pair_differences(frames); values=[p['canvas'] for p in pairs]
    return [result(k,subject,values[-1],threshold,unit='rgb_mad',notes=json.dumps({'definition':definition,'adjacent_and_seam':pairs}))
            for k,threshold,definition in [('g6_seam',min(values[:-1]),'literal minimum internal'),('g6b',float(np.median(values[:-1])),'median internal')]]


def g6c(frames, subject='', animation='walk'):
    """Walk seam (N-1,0) vs half-cycle homologue (N/2-1,N/2).

    No mirroring, alignment or phase search. Zero/zero has ratio 1; positive/zero
    has JSON-null ratio with an explicit infinite flag and a false comparison.
    Idles delegate to unchanged G6b and identify the fallback in notes.
    """
    if animation == 'idle':
        r = dict(evaluate(frames, subject)[1])
        r['id'] = 'g6c'
        r['notes'] = 'idle fallback to G6b; '+r['notes']
        return r
    if animation != 'walk':
        return result('g6c', subject, notes='UNEVALUABLE: walks only; idle uses G6b')
    n = len(frames)
    if n < 4 or n % 2:
        return result('g6c', subject, notes='UNEVALUABLE: even walk cycle of at least four frames required')
    pairs = pair_differences(frames)
    seam = pairs[-1]['canvas']; homologue = pairs[n//2-1]['canvas']
    ratio = seam/homologue if homologue else (1. if seam == 0 else None)
    r = result('g6c', subject, ratio, 1.25, unit='ratio',
        notes=json.dumps(dict(seam_pair=[n-1,0], homologue_pair=[n//2-1,n//2],
            seam_mad=seam, homologue_mad=homologue, ratio_infinite=homologue==0 and seam>0,
            comparison='seam MAD <= 1.25 * half-cycle homologue MAD')))
    r['passed'] = bool(seam <= 1.25*homologue)
    return r


G6c = g6c
evaluate_g6c = g6c
