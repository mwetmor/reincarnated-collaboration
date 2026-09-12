"""O2 alpha-composited figure vs supplied ground, sRGB luma on 0..255.
Calibration: min_delta is bible/anchor supplied; sign +1 lighter / -1 darker.
Spread is population standard deviation; no hidden separation threshold.
"""
from .common import *

def separation(rgba,background_rgb,*,sign=1,min_delta=None,alpha_min=ALPHA_MIN,display_scale=None,subject=''):
    if sign not in (-1,1):raise ValueError('sign must be -1 or 1')
    a=image_array(rgba,display_scale);m=a[...,3]>=alpha_min
    if not m.any() or m.all():return report('O2',subject,None,min_delta,reason='Need foreground and outside-alpha samples')
    bg=np.asarray(background_rgb,float)
    if bg.shape!=(3,):raise ValueError('background_rgb must be RGB')
    w=a[...,3:4]/255;lum=(a[...,:3]*w+bg*(1-w))@LUMA
    delta=float(lum[m].mean()-lum[~m].mean())
    return report('O2',subject,sign*delta,min_delta,op='>=',unit='luma',metrics={'inside_mean':float(lum[m].mean()),'inside_spread':float(lum[m].std()),'outside_mean':float(lum[~m].mean()),'outside_spread':float(lum[~m].std()),'sign':int(np.sign(delta)),'delta':delta})
