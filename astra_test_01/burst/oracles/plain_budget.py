"""O4 Sobel edge energy below edge_thresh in normalized luma (0..1).
Calibration: edge_thresh and min_plain from annotated plain/decorated anchor
patches at the declared display size. Sobel /8 normalizes its kernel gain.
"""
from scipy import ndimage
from .common import *

def plain_fraction(rgb,alpha,mask=None,edge_thresh=None,*,min_plain=None,display_scale=None,subject=''):
    if edge_thresh is None:raise ValueError('Calibrated edge_thresh required')
    a=image_array(rgb,display_scale);m=scaled_mask(np.asarray(alpha)>0,a.shape[:2])
    if mask is not None:m &= scaled_mask(mask,m.shape)
    if not m.any():return report('O4',subject,None,min_plain,reason='Empty region')
    lum=a[...,:3]@LUMA/255
    energy=np.hypot(ndimage.sobel(lum,axis=0)/8,ndimage.sobel(lum,axis=1)/8)
    value=float(np.mean(energy[m]<edge_thresh))
    return report('O4',subject,value,min_plain,op='>=',unit='fraction',metrics={'edge_thresh':edge_thresh,'mean_edge_energy':float(energy[m].mean())})
