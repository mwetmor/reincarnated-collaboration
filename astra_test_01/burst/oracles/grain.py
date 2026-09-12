"""O8 windowed radial power spectrum in cycles per SOURCE pixel.
source_px is source canvas width (or [width,height]); frequency bands use a
fixed source-Nyquist grid. profile_bins=32 is resolution, not a gate. Distance
threshold requires same-source/display-size anchor calibration; absent anchor
produces descriptive profile with null verdict. Alpha edges use Hann taper.
"""
from .common import *

def band_energy(rgb,alpha,source_px,*,anchor_profile=None,threshold=None,profile_bins=32,display_scale=None,subject=''):
    a=image_array(rgb,display_scale);m=scaled_mask(np.asarray(alpha)>0,a.shape[:2]);h,w=m.shape
    if not m.any():return report('O8',subject,None,threshold,reason='Empty foreground')
    source=np.array([source_px,source_px] if np.isscalar(source_px) else source_px,float)
    if source.shape!=(2,) or np.any(source<=0) or profile_bins<2:raise ValueError('Invalid source dimensions or bin count')
    lum=a[...,:3]@LUMA/255
    field=(lum-float(lum[m].mean()))*m*np.outer(np.hanning(h),np.hanning(w))
    power=abs(np.fft.fft2(field))**2
    fy=np.fft.fftfreq(h,d=source[1]/h);fx=np.fft.fftfreq(w,d=source[0]/w)
    radius=np.hypot(fy[:,None],fx[None,:]);edges=np.linspace(0,.5,profile_bins+1)
    sums=np.histogram(radius,bins=edges,weights=power)[0];n=np.histogram(radius,bins=edges)[0]
    profile=np.divide(sums,n,out=np.zeros_like(sums),where=n>0)
    if profile.sum()<=0:return report('O8',subject,None,threshold,reason='No spectral energy')
    profile/=profile.sum();distance=None
    if anchor_profile is not None:
        anchor=np.asarray(anchor_profile,float)
        if anchor.shape!=profile.shape or not np.isfinite(anchor).all() or np.any(anchor<0) or anchor.sum()<=0:raise ValueError('Invalid anchor profile')
        distance=float(np.linalg.norm(profile-anchor/anchor.sum()))
    return report('O8',subject,distance,threshold,unit='profile_l2',metrics={'source_px':source.tolist(),'frequency_edges_cycles_per_source_px':edges.tolist(),'profile':profile.tolist(),'sampled_bins':(n>0).tolist()})
