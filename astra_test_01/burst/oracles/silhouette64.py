"""O5 adapter: reuse gate descriptor/alignment without changing measurements.
Threshold is caller-set with approved master/idle/mirror calibration. Display
reduction precedes the existing fixed 64px measurement. Empty inputs => null.
"""
import numpy as np
from PIL import Image
from gates import silhouette64 as gate
from .common import image_array,report

def _input(a,display_scale):
    if display_scale is None or isinstance(a,dict):return a
    if isinstance(a,np.ndarray) and a.ndim==2:
        a=Image.fromarray((a*255 if a.max(initial=0)<=1 else a).astype('uint8'),'L')
    if isinstance(a,Image.Image) and a.mode=='L':
        if not 0<display_scale<=1:raise ValueError('display_scale must be in (0,1]')
        return a.resize(tuple(max(1,round(x*display_scale)) for x in a.size),Image.Resampling.LANCZOS)
    return image_array(a,display_scale)

def descriptor(alpha,display_scale=None):return gate.descriptor(_input(alpha,display_scale))
def distance(a,b,display_scale=None):return gate.distance(_input(a,display_scale),_input(b,display_scale))
def evaluate(a,b,*,threshold=None,display_scale=None,subject=''):
    try:metrics=gate.aligned_metrics(_input(a,display_scale),_input(b,display_scale))
    except ValueError as exc:return report('O5',subject,None,threshold,reason=str(exc))
    return report('O5',subject,1-metrics['aligned_iou'],threshold,unit='1-iou',metrics=metrics)
