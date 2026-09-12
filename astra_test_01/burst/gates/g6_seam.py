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
