"""Model-free sheet dispersion: O1 Lab histogram + O5 silhouette + alpha area.

Calibration set: registered run_03 idle S frames and one mirrored outlier.
No threshold calibrated: passed remains null unless max_dispersion is declared.
Palette and silhouette blocks have unit L2 norm; area is a [0,1] canvas fraction
(not unit-normalised to 1, which would erase the measurement). Equal block
weights /sqrt(3). Center/area alignment reuses O5 descriptor semantics; absolute
alpha area stays independently visible. No per-frame artwork is transformed.
"""
import numpy as np
from scipy import ndimage
from oracles.common import image_array,lab,report
from oracles.silhouette64 import descriptor

PALETTE_BINS=8


def palette_histogram(rgba,bins=PALETTE_BINS):
    a=image_array(rgba);mask=a[...,3]>=128
    if not mask.any():raise ValueError('Empty foreground')
    if type(bins) is not int or bins<2:raise ValueError('Palette bins must be >=2')
    pixels=lab(a[...,:3])[mask]
    hist=np.histogramdd(pixels,bins=(bins,bins,bins),range=((0,100),(-128,128),(-128,128)))[0].ravel()
    return hist/np.linalg.norm(hist)


def identity_vector(rgba,*,palette_bins=PALETTE_BINS):
    a=image_array(rgba);d=descriptor(a[...,3])
    scale=(512./d['area'])**.5
    offset=np.array(d['centroid'][::-1])-np.array([63.5,63.5])/scale
    mask=ndimage.affine_transform(d['mask'].astype(float),np.eye(2)/scale,offset,
                                 output_shape=(128,128),order=0).ravel()
    mask/=np.linalg.norm(mask)
    area=float(np.sum(a[...,3].astype(float)/255)/a[...,3].size)
    return np.concatenate([palette_histogram(a,palette_bins),mask,[area]])/np.sqrt(3)


def measure(frames,*,max_dispersion=None,palette_bins=PALETTE_BINS,subject=''):
    frames=list(frames)
    if not frames:return report('sheet_consistency',subject,None,max_dispersion,reason='Empty frame set')
    try:vectors=np.stack([identity_vector(a,palette_bins=palette_bins) for a in frames])
    except ValueError as exc:return report('sheet_consistency',subject,None,max_dispersion,reason=str(exc))
    centroid=vectors.mean(axis=0);distances=np.linalg.norm(vectors-centroid,axis=1)
    return report('sheet_consistency',subject,float(distances.max()),max_dispersion,unit='identity_vector_l2',
        metrics=dict(mean_distance=float(distances.mean()),max_distance=float(distances.max()),
            farthest_frame_index=int(distances.argmax()),distances=distances.tolist(),
            palette_bins=palette_bins,frame_count=len(frames)),
        reason='No sheet threshold calibrated; run_03 idle/mirror set is descriptive only' if max_dispersion is None else '')


evaluate=measure
