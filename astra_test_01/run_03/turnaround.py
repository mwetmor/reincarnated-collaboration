"""Register existing paintings from globally visible sole contours.

Unlike run-02's crop-local occupancy, a region boundary cannot manufacture an
alpha contour here. Full-image alpha is examined before foot-specific selection.
"""
from pathlib import Path
import sys, json, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'run_02'))
from pipeline import measure
DIRS = ['S','SW','W','NW','N','NE','E','SE']
REGIONS = {
 'S': [[210,350,250,395],[265,375,305,430]],
 'SW': [[216,345,251,391],[260,380,305,430]],
 'W': [[225,370,273,398],[239,395,291,426]],
 'NW': [[199,370,248,417],[260,365,304,402]],
 'N': [[210,350,246,401],[264,360,306,417]],
 'NE': [[218,350,251,393],[253,390,305,427]],
 'E': [[236,365,278,396],[219,397,289,429]],
 'SE': [[210,350,252,394],[262,380,310,430]]}


def contacts(im, regions):
    mask = np.array(im.convert('RGBA'))[...,3] >= 128
    below = np.zeros_like(mask); below[:-1] = mask[1:]
    contour = mask & ~below
    points = []
    for x0,y0,x1,y1 in regions:
        yy,xx = np.where(contour[y0:y1,x0:x1])
        if not len(yy): raise ValueError('No visible lower contour')
        bottom = yy.max(); xs = xx[yy >= bottom-1]
        if bottom == y1-y0-1 or xs.min() == 0 or xs.max() == x1-x0-1:
            raise ValueError('Review region truncates lowest sole contour')
        points.append([float(np.median(xs)+x0),float(bottom+y0)])
    return {'points':points,'midpoint':np.mean(points,axis=0).tolist()}


def run():
    out = ROOT/'evidence/turnaround'; out.mkdir(parents=True,exist_ok=True)
    rows={}; sheet=Image.new('RGBA',(4096,512)); overlay=Image.new('RGBA',(4096,544),(20,25,34,255))
    for i,d in enumerate(DIRS):
        old=ROOT.parent/'run_02/prepared'/d; im=Image.open(old/'frame.png')
        before=contacts(im,REGIONS[d]); delta=np.rint([256,400]-np.array(before['midpoint'])).astype(int)
        aligned=Image.new('RGBA',(512,512));aligned.paste(im,tuple(delta))
        # Explicit output inspection region follows translation only; the contour
        # is re-detected on actual output pixels. Overlay must also be reviewed.
        rois=[[x0+int(delta[0]),y0+int(delta[1]),x1+int(delta[0]),y1+int(delta[1])] for x0,y0,x1,y1 in REGIONS[d]]
        after=contacts(aligned,rois); error=np.abs(np.array(after['midpoint'])-[256,400])
        metrics=measure(aligned);metrics.update({'input_contacts':before,'translation':delta.tolist(),'output_contacts':after,'contact_error_xy':error.tolist(),'pivot_pass':bool((error<=4).all()),'source_sha256':hashlib.sha256((old/'frame.png').read_bytes()).hexdigest(),'output_regions':rois})
        rows[d]=metrics
        frame=ROOT/'character/frames/idle'/d/f'idle_{d}_00.png';frame.parent.mkdir(parents=True,exist_ok=True);aligned.save(frame)
        refdir=ROOT/'references'/d;refdir.mkdir(parents=True,exist_ok=True)
        ref=Image.open(old/'reference_alpha.png');new=Image.new('RGBA',(1024,1024));new.paste(ref,tuple(delta*2));new.save(refdir/'alpha.png')
        green=Image.new('RGBA',(1024,1024),(0,255,0,255));green.alpha_composite(new);green.convert('RGB').save(refdir/'green.png')
        sheet.paste(aligned,(i*512,0));overlay.alpha_composite(aligned,(i*512,32));draw=ImageDraw.Draw(overlay);ox=i*512
        draw.text((ox+12,8),d,fill='white');draw.line((ox+248,432,ox+264,432),fill='#ff5577');draw.line((ox+256,424,ox+256,440),fill='#ff5577')
        for x,y in after['points']:draw.ellipse((ox+x-2,y+30,ox+x+2,y+34),outline='#55ffee')
    gates={'height':all(abs(r['height']/rows['S']['height']-1)<=.03 for r in rows.values()),'pivot':all(r['pivot_pass'] for r in rows.values()),'light':all(r['light_pass'] for r in rows.values()),'alpha':all(r['border_alpha_max']==0 and r['green_contaminated_pixels']==0 for r in rows.values())}
    result={'status':'AWAITING_VISUAL_REVIEW' if all(gates.values()) else 'FAIL','gates':gates,'directions':rows,'method':'Global lower alpha contour (alpha>=128), reviewed foot region, lowest-two-row median; integer translation only'}
    (out/'checks.json').write_text(json.dumps(result,indent=2)+'\n');sheet.save(ROOT/'character/turnaround.png');sheet.resize((512,64),Image.Resampling.LANCZOS).save(ROOT/'character/turnaround_64px.png');overlay.save(out/'overlay.png')
    print(json.dumps({'gates':gates,'directions':{d:{'height':r['height'],'pivot_error':r['contact_error_xy'],'translation':r['translation']} for d,r in rows.items()}},indent=2))


if __name__=='__main__':run()
