"""Prepared optional compositor. Production use awaits explicit user authorization.

Inputs are an approved painted base, a registered imagegen-painted variant and
a reviewed grayscale motion mask. No generated shapes, warps or pose invention.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image

def composite(base,variant,mask):
    if base.size!=variant.size or base.size!=mask.size:raise ValueError('Inputs must already share registered canvas dimensions')
    a=np.array(base.convert('RGBA'));b=np.array(variant.convert('RGBA'));m=np.array(mask.convert('L'))/255
    af=a.astype(float)/255;bf=b.astype(float)/255
    alpha=af[...,3]*(1-m)+bf[...,3]*m
    rgb=af[...,:3]*af[...,3,None]*(1-m[...,None])+bf[...,:3]*bf[...,3,None]*m[...,None]
    straight=np.divide(rgb,alpha[...,None],out=np.zeros_like(rgb),where=alpha[...,None]>0)
    out=np.dstack([straight,alpha])*255;out=np.round(out).clip(0,255).astype('uint8')
    # Exact preservation includes RGB stored under transparent base pixels.
    out[m==0]=a[m==0]
    if not np.array_equal(out[m==0],a[m==0]):raise AssertionError('Locked pixels changed')
    return Image.fromarray(out),{'locked_pixels':int((m==0).sum()),'changed_pixels':int(np.any(out!=a,axis=2).sum()),'locked_pixels_identical':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('base',type=Path);p.add_argument('variant',type=Path);p.add_argument('mask',type=Path);p.add_argument('output',type=Path);p.add_argument('--authorization',required=True,help='Actual user authorization text; do not invent authorization');a=p.parse_args()
    image,evidence=composite(Image.open(a.base),Image.open(a.variant),Image.open(a.mask));a.output.parent.mkdir(parents=True,exist_ok=True);image.save(a.output)
    evidence.update(authorization=a.authorization,inputs={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [a.base,a.variant,a.mask]})
    a.output.with_suffix('.provenance.json').write_text(json.dumps(evidence,indent=2)+'\n')
