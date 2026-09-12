"""Shared color math and display reduction; result envelope is gates.common.result.
Color constants: IEC sRGB / CIE D65, not learned thresholds. display_scale is a
uniform factor in (0,1]; no upscaling. Alpha support threshold is caller-set.
"""
import json
import numpy as np
from PIL import Image
from gates.common import rgba, result

ALPHA_MIN=128  # Opaque-core calibration: same support convention as gate library.
LUMA=np.array([.2126,.7152,.0722])

def image_array(image,display_scale=None):
    im=rgba(image)
    if display_scale is not None:
        if not 0<display_scale<=1:raise ValueError('display_scale must be in (0,1]')
        im=im.resize(tuple(max(1,round(v*display_scale)) for v in im.size),Image.Resampling.LANCZOS)
    return np.array(im)

def scaled_mask(mask,shape):
    a=np.asarray(mask)
    if a.shape==tuple(shape):return a.astype(bool)
    return np.array(Image.fromarray(a.astype('uint8')*255).resize((shape[1],shape[0]),Image.Resampling.NEAREST))>0

def lab(rgb):
    a=np.asarray(rgb,float)/255
    linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
    xyz=linear@np.array([[.4124564,.3575761,.1804375],[.2126729,.7151522,.0721750],[.0193339,.1191920,.9503041]]).T
    xyz=xyz/np.array([.95047,1,1.08883]);delta=6/29
    f=np.where(xyz>delta**3,np.cbrt(xyz),xyz/(3*delta**2)+4/29)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],axis=-1)

def swatches(values):
    return np.array([[int(s[i:i+2],16) for i in (1,3,5)] for s in values],float)

def report(id,subject,value,threshold=None,op='<=',unit='',metrics=None,reason=''):
    notes=json.dumps({'metrics':metrics or {},'reason':reason},allow_nan=False,sort_keys=True)
    # Do not let shared helper infer a verdict on unclassifiable inputs.
    r=result(id,subject,value,None if reason else threshold,op,unit,notes)
    if reason:r['threshold']=threshold;r['passed']=None
    return r
