"""Refine chroma-edge alpha for known blue frost, preserving body/native alpha."""
import numpy as np
from PIL import Image

def refine_blue_edges(original,matte):
    if 'A' in original.getbands() and (np.array(original)[...,3]==0).mean()>.01:
        return matte,{'blue_glow_edge_refinement_pixels':0,'reason':'native alpha retained'}
    raw=np.array(original.convert('RGB')).astype(float);out=np.array(matte)
    red,green,blue=raw.transpose(2,0,1)
    edge=(out[...,3]>0)&(out[...,3]<255)&(blue>red+5)&(green>np.maximum(red,blue)+12)
    # Blue-glow foreground prior G≈0.55B+0.45R, applied only to keyed edges.
    # The original neutral-green-excess matte assumes G=max(R,B), turning blue
    # emission fringes cyan; that prior is unsuitable for frost.
    alpha=np.clip(1-(green-.55*blue-.45*red)/255,0,1)
    color=(raw-(1-alpha[...,None])*[0,255,0])/np.maximum(alpha[...,None],1e-6)
    corrected=np.dstack([color,alpha*255]).round().clip(0,255).astype('uint8')
    out[edge]=corrected[edge];out[out[...,3]==0]=0
    return Image.fromarray(out),{'blue_glow_edge_refinement_pixels':int(edge.sum()),'foreground_prior':'G=0.55B+0.45R only on partial-alpha blue chroma edges; opaque body unchanged'}
