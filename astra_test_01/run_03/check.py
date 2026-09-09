"""Measure actual frames; missing production stays incomplete."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from animation import ROOT,measure,front_contacts,frame_contacts
DIRS=['S','SW','W','NW','N','NE','E','SE'];COUNTS={'idle':8,'walk':8,'cast':12}

def pixels(path):
    im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(20,25,34,255));bg.alpha_composite(im)
    return np.array(bg)[...,:3].astype(float),np.array(im)[...,3]>0

def difference(a,b):
    x,m=pixels(a);y,n=pixels(b);v=np.abs(x-y);u=m|n
    return {'canvas':float(v.mean()),'foreground_union':float(v[u].mean())}

def direction(d):
    result={'animations':{},'complete':True};cast=ROOT/f'character/frames/cast/{d}/cast_{d}_05.png'
    for anim,count in COUNTS.items():
        files=sorted((ROOT/'character/frames'/anim/d).glob('*.png'));rows=[]
        for f in files:
            im=Image.open(f);r=measure(im);r['file']=str(f.relative_to(ROOT));r['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
            try:
                p=frame_contacts(im,f.relative_to(ROOT));err=np.abs(np.mean(p,axis=0)-[256,400]);r.update(sole_points=p,sole_midpoint_error=err.tolist(),sole_midpoint_pass=bool((err<=4).all()))
            except ValueError as e:r.update(sole_midpoint_pass=False,contact_error=str(e))
            rows.append(r)
        valid_count=len(files)==count;result['complete'] &= valid_count
        checks={'count':valid_count,'distinct_rasters':len({r['sha256'] for r in rows})==len(rows),
                'light':bool(rows) and all(r['light_pass'] for r in rows),
                'alpha':bool(rows) and all(r['border_alpha_max']==0 and r['green_contaminated_pixels']==0 for r in rows),
                'visible_sole_midpoint':bool(rows) and all(r['sole_midpoint_pass'] for r in rows)}
        item={'available':len(files),'required':count,'checks':checks,'frames':rows}
        if anim in ['idle','walk'] and valid_count:
            pairs=[difference(files[i],files[(i+1)%count]) for i in range(count)]
            item['adjacent_and_seam']=pairs;checks['loop_seam']=pairs[-1]['canvas']<=min(p['canvas'] for p in pairs[:-1])
            if cast.exists():
                cross=difference(files[0],cast);item['cross_cast_05']=cross
                checks['drift']=all(p['canvas']<cross['canvas'] for p in pairs)
        result['animations'][anim]=item
    result['numeric_pass']=result['complete'] and all(all(a['checks'].values()) for a in result['animations'].values())
    result['qualification']='NUMERIC CHECKS ONLY: visual motion and ground-root/planted-foot interpretation remain separately reviewed'
    return result

def run():
    result={'directions':{d:direction(d) for d in DIRS},'gate2_measurement':'Visible two-sole midpoint; raw points retained. Ground/root and planted-foot sliding are separate checks.'}
    result['status']='NUMERIC_PASS' if all(r['numeric_pass'] for r in result['directions'].values()) else 'INCOMPLETE_OR_FAIL'
    (ROOT/'evidence/current_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({d:{a:item['checks'] for a,item in r['animations'].items()} for d,r in result['directions'].items() if r['complete']},indent=2))
    # Actual-source 25% contact sheet for visual review, not replacement artwork.
    for d,r in result['directions'].items():
        if not r['complete']:continue
        sheet=Image.new('RGBA',(1536,480),(20,25,34,255));draw=ImageDraw.Draw(sheet)
        for j,(anim,item) in enumerate(r['animations'].items()):
            draw.text((8,j*160+2),anim,fill='white')
            for i,row in enumerate(item['frames']):sheet.alpha_composite(Image.open(ROOT/row['file']).resize((128,128),Image.Resampling.LANCZOS),(i*128,j*160+24))
        sheet.save(ROOT/'evidence'/f'{d}_complete_contact.png')
    return result

if __name__=='__main__':run()
