"""MODEL-COUPLED green-plate matte health; re-validate on EVERY drift alarm.

Calibrated descriptively on the two X1 props, not used as a shipping threshold.
Spill: fraction of subject alpha>0 pixels with G-max(R,B)>tol.
Halo: mean positive green excess in a halo_width_px (default 2) band outside
alpha>=128, restricted to remaining alpha>0; removed pixels contribute zero.
Particle-loss proxy: source green-excess-derived alpha mass in 0<alpha<128
removed by the matte, divided by that source partial-alpha mass. This proxy
also includes near-green plate deviations and AA edges; it is NOT semantic
particle ground truth. No true-particle preservation verdict without labels.
"""
import numpy as np
from scipy import ndimage
from oracles.common import image_array,report


def measure(rgba,green_plate,tol=20,*,halo_width_px=2,subject='',
            max_spill_fraction=None,max_edge_halo=None,max_particle_loss=None):
    if tol<0 or type(halo_width_px) is not int or halo_width_px<1:
        raise ValueError('Invalid matte quality parameters')
    matte=image_array(rgba);source=image_array(green_plate)
    if matte.shape!=source.shape:raise ValueError('Source/matte canvas mismatch')
    rgb=matte[...,:3].astype(float);alpha=matte[...,3].astype(float)
    excess=np.maximum(rgb[...,1]-np.maximum(rgb[...,0],rgb[...,2]),0)
    support=alpha>0;core=alpha>=128
    band=ndimage.binary_dilation(core,iterations=halo_width_px)&~core
    spill=float(np.mean(excess[support]>tol)) if support.any() else None
    # Zero-alpha RGB is undefined; it must never create a halo signal.
    halo=float(np.mean(np.where(support,excess,0)[band])) if band.any() else None
    raw=source[...,:3].astype(float)
    green=raw[...,1]-np.maximum(raw[...,0],raw[...,2])
    source_alpha=np.clip(255-green,0,255)
    source_alpha[green>=250]=0;source_alpha[green<=12]=255
    partial=(source_alpha>0)&(source_alpha<128)
    mass=float(source_alpha[partial].sum())
    removed=float(np.maximum(source_alpha-alpha,0)[partial].sum())
    loss=removed/mass if mass else None
    rows=[report('matte_quality.spill',subject,spill,max_spill_fraction,unit='fraction',
            metrics={'tol':tol,'subject_pixels':int(support.sum())},reason='Empty alpha subject' if spill is None else ''),
          report('matte_quality.edge_halo',subject,halo,max_edge_halo,unit='green_excess_0_255',
            metrics={'band_pixels':int(band.sum()),'halo_width_px':halo_width_px},reason='No exterior edge band' if halo is None else ''),
          report('matte_quality.particle_loss',subject,loss,max_particle_loss,unit='source_partial_alpha_mass_fraction',
            metrics={'source_partial_alpha_mass':mass,'removed_partial_alpha_mass':removed,
                     'model_coupled':True,'includes_plate_residuals':True},
            reason='No source partial alpha mass' if loss is None else '')]
    return rows


evaluate=measure
