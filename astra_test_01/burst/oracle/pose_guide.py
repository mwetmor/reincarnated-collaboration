"""Pillow line guides drawn from dope-sheet numbers, never reference pixels.

Walk returns a name->PIL Image mapping; caller owns output directory. H_px is a
numeric unit conversion, not an image resize. Soles use a bottom-center anchor.
Idle overlays two explicitly derived chest outlines on an unchanged base.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_erosion

SOLE_COLORS = ((25,100,210,255),(200,60,100,255))


def render_walk_guide(walk_sheet, H_px, canvas=512):
    if not math.isfinite(H_px) or H_px<=0: raise ValueError('H_px must be positive finite')
    if type(canvas) is not int or canvas<32: raise ValueError('canvas must be integer >=32')
    if walk_sheet.get('kind')!='walk' or len(walk_sheet.get('frames',[]))!=12:
        raise ValueError('12-frame walk sheet required')
    ground=round(canvas*.88);center=canvas//2
    output={}
    for row in walk_sheet['frames']:
        im=Image.new('RGBA',(canvas,canvas),'white');d=ImageDraw.Draw(im)
        d.line((0,ground,canvas-1,ground),fill=(125,125,125,255))
        d.text((8,8),f"{row['frame']:02d} {row['phase']}",fill='black')
        radius=max(3,round(.055*H_px)); top=round(ground-row['head_height_H']*H_px)
        if top<0 or top+2*radius>=canvas: raise ValueError('head outside guide canvas')
        d.ellipse((center-radius,top,center+radius,top+2*radius),outline='black',width=2)
        half=max(2,round(.035*H_px));thick=max(2,round(.015*H_px))
        for j,(side,sole) in enumerate(row['soles'].items()):
            x=round(center+sole['x_H']*H_px);y=round(ground-sole['height_H']*H_px)
            if not (half<=x<canvas-half and thick<=y<canvas): raise ValueError('sole outside guide canvas')
            d.rectangle((x-half,y-thick,x+half,y),outline=SOLE_COLORS[j],width=2)
            d.text((x-half,y-thick-13),side,fill=SOLE_COLORS[j])
        output[f"walk_{row['frame']:02d}.png"]=im
    return output


def render_idle_guide(idle_sheet, base_rgba):
    if idle_sheet.get('kind')!='idle': raise ValueError('idle sheet required')
    if isinstance(base_rgba,Image.Image): im=base_rgba.convert('RGBA').copy()
    else: im=Image.fromarray(np.asarray(base_rgba,dtype=np.uint8)).convert('RGBA')
    mask=np.array(im)[...,3]>=128;y,x=np.where(mask)
    if not len(x): raise ValueError('base alpha is empty')
    y0,y1=int(y.min()),int(y.max()+1); H=y1-y0
    top=round(y0+.18*H);bottom=round(y0+.45*H)
    chest=mask[top:bottom];edge=chest & ~binary_erosion(chest)
    ys,xs=np.where(edge)
    if not len(xs): raise ValueError('empty chest band')
    center=(xs.min()+xs.max())/2; radius=max(1,(xs.max()-xs.min())/2)
    values=[row['chest_dw_H'] for row in idle_sheet['frames']]
    overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
    for delta,color in zip((min(values),max(values)),SOLE_COLORS):
        for yy,xx in zip(ys,xs):
            new_x=round(xx+((xx-center)/radius)*delta*H/2)
            if 0<=new_x<im.width:d.point((new_x,int(yy+top)),fill=color)
    im.alpha_composite(overlay)
    return im
