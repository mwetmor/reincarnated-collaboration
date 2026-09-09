"""Measure prepared frames and independently locate sole contacts in review ROIs."""
import argparse
import datetime
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw
from pipeline import ROOT, CONFIG, measure, save_json


def contact(image, regions):
    from registration_preflight import preflight
    try:
        result = preflight(image, regions)
        result['max_error'] = max(result['error_xy'])
        result['valid'] = True
        return result
    except ValueError as exc:
        return {'pass': False, 'valid': False, 'points': [],
                'max_error': None, 'error': str(exc)}


def checkpoint(attempt):
    out=ROOT/'evidence'/f'checkpoint_{attempt}'
    if out.exists():raise ValueError('Immutable checkpoint already exists; do not overwrite evidence')
    out.mkdir(parents=True)
    regions=json.loads((ROOT/'contact_regions.json').read_text())
    visual=json.loads((ROOT/'visual_review.json').read_text())
    sheet=Image.new('RGBA',(4096,512));overlay=Image.new('RGBA',(4096,544),(20,25,34,255))
    rows={}
    for i,d in enumerate(CONFIG['directions']):
        path=ROOT/'prepared'/d/'frame.png';im=Image.open(path)
        row=measure(im);row['contact']=contact(im,regions[d]);rows[d]=row
        dest=out/d;dest.mkdir();shutil.copyfile(path,dest/'frame.png')
        shutil.copyfile(ROOT/'prepared'/d/'metrics.json',dest/'metrics.json')
        sheet.paste(im,(512*i,0));overlay.alpha_composite(im,(512*i,32))
        draw=ImageDraw.Draw(overlay);ox=512*i
        draw.text((ox+12,10),d,fill='white')
        draw.line((ox+246,432,ox+266,432),fill='#ff5577',width=2)
        draw.line((ox+256,422,ox+256,442),fill='#ff5577',width=2)
        for x,y in row['contact']['points']:draw.ellipse((ox+x-2,y+30,ox+x+2,y+34),fill='#44ddbb')
        x,y=row['light_centroid'];draw.ellipse((ox+x-3,y+29,ox+x+3,y+35),fill='#ffd477')
        x0,y0,x1,y1=row['bbox'];draw.rectangle((ox+x0,y0+32,ox+x1,y1+32),outline='#b7bec8')
    for r in rows.values():
        r['height_deviation_pct']=100*(r['height']/rows['S']['height']-1)
    gates={
        '1_height':all(abs(r['height_deviation_pct'])<=3 for r in rows.values()),
        '2_pivot':all(r['contact']['pass'] for r in rows.values()),
        '3_light':all(r['light_pass'] for r in rows.values()),
        '4_right_hand':visual['right_hand_pass'],
        '7_downscale_read':visual['downscale_pass'],
        'alpha_format':all(r['transparent_fraction']>.5 and r['border_alpha_max']==0 and r['green_contaminated_pixels']==0 for r in rows.values()),
        'unique_directions':visual['unique_directions_pass']}
    result={'attempt':attempt,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'status':'PASS' if all(gates.values()) else 'FAIL','gates':gates,'directions':rows,'visual':visual}
    sheet.save(out/'turnaround.png');sheet.resize((512,64),Image.Resampling.LANCZOS).save(out/'turnaround_64px.png')
    sheet.resize((1024,128),Image.Resampling.LANCZOS).save(out/'contact.png');overlay.save(out/'overlay.png')
    save_json(out/'checks.json',result);shutil.copyfile(ROOT/'contact_regions.json',out/'contact_regions.json')
    print(json.dumps({'status':result['status'],'gates':gates,'directions':{d:{'height':r['height'],'light':r['light_pass'],'contact':r['contact']} for d,r in rows.items()}},indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--attempt',type=int,required=True,choices=[1,2]);args=p.parse_args();raise SystemExit(checkpoint(args.attempt))
