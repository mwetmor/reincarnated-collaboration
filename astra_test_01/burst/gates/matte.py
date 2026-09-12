"""Literal run_02 character matte; opt-in detached-particle preservation.
Native alpha retains dark interiors. Default dust filtering matches run_02.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

def extract(image, preserve_particles=False):
    a = np.array(image.convert('RGBA')).astype(float)
    native = bool('A' in image.getbands() and np.mean(a[..., 3] == 0) > .01)
    if native:
        method = 'native alpha'
        out = a.astype(np.uint8)
    else:
        rgb = a[..., :3]
        border = np.concatenate([rgb[:10].reshape(-1,3),rgb[-10:].reshape(-1,3),
                                 rgb[:,:10].reshape(-1,3),rgb[:,-10:].reshape(-1,3)])
        green_fraction = float(np.mean((border[:,1] > 210) &
                                       (border[:,0] < 45) & (border[:,2] < 45)))
        if green_fraction < .95:
            raise ValueError(f'No native alpha or uniform green plate: border green fraction {green_fraction:.4f}')
        excess = rgb[...,1] - np.maximum(rgb[...,0],rgb[...,2])
        alpha = np.clip(1 - excess / 255, 0, 1)
        alpha[excess <= 12] = 1
        alpha[excess >= 250] = 0
        clean = (rgb - (1-alpha[...,None])*np.array([0,255,0])) / np.maximum(alpha[...,None],1e-6)
        out = np.dstack([np.clip(clean,0,255),alpha*255]).round().astype(np.uint8)
        method = 'green excess matte + inverse straight-alpha compositing'
    # Remove only detached alpha dust, never dark character pixels.
    labels, n = ndimage.label(out[...,3] >= 128)
    counts = np.bincount(labels.ravel())
    counts[0] = 0
    main_component = int(counts.argmax())
    support = ndimage.binary_dilation(labels == main_component, iterations=3)
    dust = int(np.count_nonzero((out[...,3]>0) & ~support))
    if not preserve_particles:
        out[~support] = 0
    else:
        dust = 0
    out[out[...,3] == 0, :3] = 0
    mask = out[...,3] >= 128
    if mask.sum() < 100:
        raise ValueError('Empty extracted subject')
    return Image.fromarray(out), {'method':method, 'removed_background_or_detached_alpha_dust_pixels':dust,
                                'native_input_alpha':native}


def remove_chroma_key(image, preserve_particles=False):
    return extract(image, preserve_particles=preserve_particles)[0]
