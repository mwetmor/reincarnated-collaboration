"""F-5 green-plate uniformity, calibrated descriptively on both X1 props.

min_fraction is explicitly caller-declared; no shipping threshold is inferred
from the ledger's 100%/38%. tol=8 is the registered per-channel tolerance.
Opaque subject support is alpha>=128 (the existing gate convention). Without
an annotation, infer only the largest non-key component from green excess;
this is MODEL-COUPLED and not a substitute for reviewed subject support.
"""
import numpy as np
from scipy import ndimage
from oracles.common import image_array,report


def measure(rgb, subject_alpha=None, tol=8, *, min_fraction=None, subject=''):
    if not 0<=tol<=255 or (min_fraction is not None and not 0<=min_fraction<=1):
        raise ValueError('Invalid plate threshold')
    a=image_array(rgb)[...,:3].astype(float)
    if subject_alpha is None:
        core=255-(a[...,1]-np.maximum(a[...,0],a[...,2]))>=128
        labels,_=ndimage.label(core);counts=np.bincount(labels.ravel());counts[0]=0
        mask=labels==int(counts.argmax()) if counts.max(initial=0)>0 else np.zeros(core.shape,bool)
        source='largest non-key component inferred from green excess'
    else:
        alpha=np.asarray(subject_alpha)
        if alpha.shape!=a.shape[:2]:raise ValueError('Alpha shape mismatch')
        mask=alpha if alpha.dtype==bool else alpha>=128
        source='supplied subject alpha >=128'
    plate=a[~mask]
    if not len(plate):return report('plate_uniformity',subject,None,min_fraction,op='>=',reason='No non-subject pixels')
    fraction=float(np.mean(np.all(np.abs(plate-[0,255,0])<=tol,axis=1)))
    return report('plate_uniformity',subject,fraction,min_fraction,op='>=',unit='fraction',
        metrics={'plate_mean_rgb':plate.mean(0).tolist(),'plate_sd_rgb':plate.std(0).tolist(),
                 'non_subject_pixels':len(plate),'tol':tol,'subject_support':source},
        reason='No min_fraction declared; X1 observations are not a threshold' if min_fraction is None else '')
