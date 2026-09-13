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


_LUMA = np.array([0.2126, 0.7152, 0.0722])


def _edge_input(rgba, bg):
    a = image_array(rgba)
    background = np.asarray(bg, dtype=float)
    if background.shape != (3,) or not np.isfinite(background).all() or np.any((background < 0) | (background > 255)):
        raise ValueError('bg must contain three finite RGB values in 0..255')
    alpha = a[..., 3].astype(float) / 255
    composite = a[..., :3].astype(float)*alpha[..., None] + background*(1-alpha[..., None])
    return a, composite @ _LUMA


def _edge_report(name, value, unit, notes, **metrics):
    # Descriptive instruments: no committed threshold, hence no verdict.
    return dict(id='matte_quality.'+name, subject='', passed=None, value=value,
                threshold=None, op='<=', unit=unit, evidence=[], notes=notes,
                metrics=metrics)


def rim_luma_excess(rgba, bg=(58, 63, 74)):
    """Mean composite partial-band luma minus opaque interior-ring luma.

    Luma uses Rec.709 weights on 0..255 display RGB (no linearization).
    The ring consists of alpha=255 pixels at Euclidean distance 1..3 pixels
    from the partial band. Empty bands/rings return value=None, never zero.
    """
    a, luma = _edge_input(rgba, bg)
    partial = (a[..., 3] > 0) & (a[..., 3] < 255)
    ring = np.zeros(partial.shape, dtype=bool)
    if partial.any():
        distance = ndimage.distance_transform_edt(~partial)
        ring = (a[..., 3] == 255) & (distance >= 1) & (distance <= 3)
    band_mean = float(luma[partial].mean()) if partial.any() else None
    ring_mean = float(luma[ring].mean()) if ring.any() else None
    value = band_mean-ring_mean if band_mean is not None and ring_mean is not None else None
    notes = 'Partial-alpha composite mean minus opaque ring mean; Euclidean 1–3 px; Rec.709 display luma.'
    if value is None:
        notes += ' UNEVALUABLE: missing partial-alpha band or opaque interior ring.'
    return _edge_report('rim_luma_excess', value, 'luma_0_255', notes,
                        partial_band_pixels=int(partial.sum()), opaque_ring_pixels=int(ring.sum()),
                        partial_band_mean=band_mean, opaque_ring_mean=ring_mean, bg=list(bg))


def alpha_area(rgba):
    """Integrated alpha area, in equivalent fully opaque pixels."""
    a = image_array(rgba)
    return _edge_report('alpha_area', float(a[..., 3].astype(float).sum()/255),
                        'opaque_pixel_equivalents', 'Sum of alpha/255; transparent pixels contribute zero.',
                        support_pixels=int(np.count_nonzero(a[..., 3])),
                        opaque_pixels=int(np.count_nonzero(a[..., 3] == 255)))


def direct_luminance_fringe(rgba, untrimmed_rgba=None, bg=(58, 63, 74)):
    """Mean positive composite-luma excess on the PRE-TRIM partial band.

    Compare to the nearest opaque reference pixel. Both the donor RGB and
    denominator come from untrimmed_rgba, so erosion cannot redefine either.
    For an untrimmed input the reference may be omitted; trimmed callers MUST
    supply the original matte. Removed pixels are composited as background.
    """
    a, luma = _edge_input(rgba, bg)
    reference = a if untrimmed_rgba is None else image_array(untrimmed_rgba)
    if a.shape != reference.shape:
        raise ValueError('Untrimmed/matte canvas mismatch')
    band = (reference[..., 3] > 0) & (reference[..., 3] < 255)
    opaque = reference[..., 3] == 255
    value = None
    if band.any() and opaque.any():
        nearest = ndimage.distance_transform_edt(~opaque, return_distances=False, return_indices=True)
        donor_luma = reference[..., :3].astype(float) @ _LUMA
        excess = luma[band]-donor_luma[nearest[0][band], nearest[1][band]]
        value = float(np.maximum(excess, 0).mean())
    notes = ('R-52: average over the PRE-TRIM partial-alpha band, replacing a post-trim '
             'denominator; frozen nearest-opaque reference RGB; positive Rec.709 composite-luma excess.')
    if untrimmed_rgba is None:
        notes += ' Input treated as untrimmed; trimmed callers must supply untrimmed_rgba.'
    if value is None:
        notes += ' UNEVALUABLE: missing pre-trim partial band or opaque donor.'
    return _edge_report('direct_luminance_fringe', value, 'luma_0_255', notes,
                        pre_trim_band_pixels=int(band.sum()),
                        surviving_band_pixels=int(np.count_nonzero(band & (a[..., 3] > 0))),
                        reference_supplied=untrimmed_rgba is not None, bg=list(bg))
