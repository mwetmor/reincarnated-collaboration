"""Estimate framing scale from the hood contour, independent of body pose."""
import numpy as np
from scipy import ndimage


def hood_profile(image):
    mask=np.array(image.convert('RGBA'))[...,3]>=128
    ys,xs=np.where(mask)
    # Above the shoulders, hood and staff are separate alpha components.
    upper=mask.copy();upper[int(ys.min()+.28*(ys.max()-ys.min())):]=False
    labels,_=ndimage.label(upper);counts=np.bincount(labels.ravel());counts[0]=0
    hood=labels==counts.argmax();y0=int(np.where(hood)[0].min())
    widths=[]
    for y in range(y0,mask.shape[0]):
        row=hood[y];edges=np.diff(np.r_[False,row,False].astype(int));starts=np.where(edges==1)[0];ends=np.where(edges==-1)[0]
        widths.append(float(max(ends-starts)) if len(starts) else 0)
    return y0,np.array(widths)


def fit_scale(source,approved,batch=False):
    top,profile=hood_profile(source);ref_top,ref=hood_profile(approved)
    offsets=np.arange(9,39,dtype=float)
    target=np.interp(offsets,np.arange(len(ref)),ref)
    nominal=approved.width/source.width
    candidates=np.linspace(nominal*(.25 if batch else .65),min(1,nominal*1.3),801 if batch else 401)
    scores=[]
    for scale in candidates:
        widths=np.interp(offsets/scale,np.arange(len(profile)),profile)*scale
        scores.append(float(np.mean((widths-target)**2)))
    index=int(np.argmin(scores));scale=float(candidates[index]);rmse=float(np.sqrt(scores[index]))
    if index in [0,len(candidates)-1] or rmse>8:
        raise ValueError(f'Hood scale fit requires visual review: rmse={rmse:.2f}')
    return scale,{'method':'least-squares hood contour width at 9–38 output px below hood top; body/feet excluded',
                  'source_hood_top':top,'reference_hood_top':ref_top,'scale':scale,'nominal_canvas_scale':nominal,'hood_width_rmse_px':rmse}
