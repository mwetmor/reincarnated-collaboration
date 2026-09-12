"""O7 luminance-weighted gradient azimuth; x-right, y-up, UL=135 degrees.
Calibration: tolerance and minimum resultant length must be set from shaded
anchor planes; default min_resultant=0 only excludes undefined zero vectors.
Silhouette boundary is eroded by one display pixel (named parameter) to avoid
mistaking the alpha edge for shading. Texture can confound this proxy.
"""
from scipy import ndimage
from .common import *

def azimuth(rgb,alpha,mask=None,*,key_azimuth_deg=135,tolerance=None,min_resultant=0,erosion_px=1,display_scale=None,subject=''):
    a=image_array(rgb,display_scale);m=scaled_mask(np.asarray(alpha)>0,a.shape[:2])
    if mask is not None:m &= scaled_mask(mask,m.shape)
    if erosion_px:m=ndimage.binary_erosion(m,iterations=erosion_px)
    if not m.any():return report('O7',subject,None,tolerance,reason='Empty interior')
    lum=a[...,:3]@LUMA/255;gx=ndimage.sobel(lum,axis=1)/8;gy=-ndimage.sobel(lum,axis=0)/8
    mag=np.hypot(gx,gy);weights=lum*mag;total=float(weights[m].sum())
    z=np.sum((gx[m]+1j*gy[m])*lum[m])
    if total<=0:return report('O7',subject,None,tolerance,reason='No luminance gradient')
    resultant=float(abs(z)/total)
    if resultant<=min_resultant:return report('O7',subject,None,tolerance,metrics={'resultant':resultant},reason='Ambiguous gradient directions')
    angle=float(np.degrees(np.angle(z))%360);error=float(abs((angle-key_azimuth_deg+180)%360-180))
    return report('O7',subject,error,tolerance,unit='degrees',metrics={'azimuth_deg':angle,'dispersion':1-resultant,'resultant':resultant})
