"""Part measurements share §1 envelopes; empty masks are never accepted.
All decision thresholds are caller-set from reviewed part-mask anchors.
Centroid is relative to torso centroid, normalized by torso bbox width/height.
Mirror symmetry uses a declared axis in native pixels, or the canvas midline.
"""
from scipy import ndimage
from oracles.common import *

def _mask(mask,display_scale):
    m=np.asarray(mask,bool)
    if display_scale is None:return m
    if not 0<display_scale<=1:raise ValueError('display_scale must be in (0,1]')
    return scaled_mask(m,tuple(max(1,round(v*display_scale)) for v in m.shape))

def area(mask,*,min_area=None,display_scale=None,subject=''):
    m=_mask(mask,display_scale)
    return report('O6.area',subject,int(m.sum()) if m.any() else None,min_area,op='>=',unit='px2',reason='' if m.any() else 'Empty part')

def centroid_rel(mask,torso,*,display_scale=None,subject=''):
    m=_mask(mask,display_scale);t=_mask(torso,display_scale)
    if m.shape!=t.shape:raise ValueError('Mask shapes differ')
    if not m.any() or not t.any():return report('O6.centroid_rel',subject,None,reason='Empty part or torso')
    y,x=np.where(m);ty,tx=np.where(t)
    point=[float((x.mean()-tx.mean())/(np.ptp(tx)+1)),float((y.mean()-ty.mean())/(np.ptp(ty)+1))]
    return report('O6.centroid_rel',subject,point,unit='torso_bbox',metrics={'normalization':'torso width,height'})

def palette_distance(rgba,mask,swatches_hex,*,threshold=None,display_scale=None,subject=''):
    a=image_array(rgba,display_scale);m=scaled_mask(mask,a.shape[:2])&(a[...,3]>0)
    if not m.any() or not swatches_hex:return report('O6.palette_distance',subject,None,threshold,reason='Empty part or palette')
    d=np.linalg.norm(lab(a[...,:3])[m,None,:]-lab(swatches(swatches_hex))[None,:,:],axis=-1).min(axis=1)
    return report('O6.palette_distance',subject,float(d.mean()),threshold,unit='dE76')

def mirror_symmetry(mask_a,mask_b,*,axis_x=None,threshold=None,display_scale=None,subject=''):
    a=_mask(mask_a,display_scale);b=_mask(mask_b,display_scale)
    if a.shape!=b.shape:raise ValueError('Mask shapes differ')
    if not a.any() or not b.any():return report('O6.mirror_symmetry',subject,None,threshold,reason='Empty part')
    axis=(a.shape[1]-1)/2 if axis_x is None else axis_x*(a.shape[1]/np.asarray(mask_a).shape[1])
    flipped=ndimage.affine_transform(a.astype(float),[[1,0],[0,-1]],offset=[0,2*axis],order=0)>0
    iou=float((flipped&b).sum()/(flipped|b).sum())
    return report('O6.mirror_symmetry',subject,1-iou,threshold,unit='1-iou',metrics={'axis_x':axis,'iou':iou})
