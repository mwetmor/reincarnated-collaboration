"""Reproducible T4d synthetic evidence and native empty-plate baseline crops.

Only writes the permitted runs/C-5/t3/T4d tree. Baselines are staged there due
to the task's later restriction on all other runs/ paths. Native authored layers
are composited at their declared offsets, with no scaling or colour transform;
these are source-plate baselines, not claimed as renderer captures with props.
"""
import hashlib
import json
import re
from pathlib import Path
import sys
import time

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oracle.white_gate import baseline,crop_bounds,measure
from oracle.event_gates import activation_expiry,field_boundary,aura_attachment,interval_cv


def main():
    out=ROOT/'runs/C-5/t3/T4d'; dest=out/'baselines';dest.mkdir(parents=True,exist_ok=True)
    source=ROOT/'runs/C-3/cliffside_v18/parallax'
    manifest=json.loads((source/'export.json').read_text())
    points={'dirt_spawn':(2285.62,2407.32),'foliage':(2400,3500)}
    settings=(source.parent/'project.godot').read_text()
    match=re.search(r'environment/defaults/default_clear_color=Color\(([^)]+)\)',settings)
    if match is None: raise ValueError('Source must declare its clear colour')
    clear=tuple(round(float(v)*255) for v in match[1].split(','))
    started=time.monotonic(); rows={}
    for name,point in points.items():
        box=crop_bounds(point,manifest['canvas_size'])
        crop=Image.new('RGBA',(960,540),clear)
        sources=[]
        layers=sorted(manifest['layers'],key=lambda layer:layer['z'])
        tiles=[dict(file='tiles/'+tile['file'],position=tile['position']) for tile in manifest['tiles']]
        foreground=Image.new('RGBA',(960,540))
        for layer in layers+tiles:
            file=source/layer['file']; x,y=map(round,layer['position'])
            with Image.open(file) as im:
                part=im.convert('RGBA').crop((box[0]-x,box[1]-y,box[2]-x,box[3]-y))
            crop=Image.alpha_composite(crop,part)
            if layer in tiles: foreground=Image.alpha_composite(foreground,part)
            sources.append(dict(path=str(file),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),offset_xy=[x,y]))
        remaining=int(np.count_nonzero(np.array(crop)[...,3]!=255))
        if remaining: raise ValueError((name,'composite still has nonopaque pixels',remaining))
        path=dest/(name+'.png');crop.convert('RGB').save(path)
        row=baseline(path,(480,270),name)
        row.update(clear_rgba=list(clear),source_crop_origin_xy=box[:2],source_impact_xy=list(point),
                   source_crop_bounds_xyxy=box,source_nonopaque_pixels=remaining,
                   foreground_nonopaque_pixels=int(np.count_nonzero(np.array(foreground)[...,3]!=255)),
                   sources=sources,baseline_kind='native source-plate reconstruction at authored layer offsets; no engine capture, camera-scroll correction or props')
        rows[name]=row
    report={'intended_path':'runs/C-5/baselines/white_baseline.json',
            'staged_because':'Later task constraint forbids writes under runs except runs/C-5/t3/T4d/',
            'baselines':rows,'wall_s':time.monotonic()-started}
    (dest/'white_baseline.json').write_text(json.dumps(report,indent=2)+'\n')
    plate=np.zeros((540,960,3),np.uint8);frame=plate.copy();frame.reshape(-1,3)[:20736]=255
    white=measure(plate,[plate,frame,plate],(480,270),'synthetic_4_percent')
    events=activation_expiry([dict(frame=f,active=10<=f<72) for f in range(80)],
                             [dict(event='contact',age_frames=10),dict(event='expire',age_frames=60)])
    acceptance={'white_synthetic':white,'late_expiry':events,
                'field_radius':field_boundary([[10,0],[0,10],[-10,0],[0,-10]],(0,0),10),
                'aura_drift':aura_attachment([[1,2],[4,6]],[[1,2],[1,2]]),
                'interval_cv':interval_cv([0,10,30]),
                'baselines':{k:{'percent':v['peak']['baseline']['percent'],'crop_origin_xy':v['source_crop_origin_xy']} for k,v in rows.items()},
                'wall_s':time.monotonic()-started}
    (out/'measurement_acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
    print(json.dumps({'baselines':acceptance['baselines'],'synthetic_white_peak':white['peak']['attributable']['percent'],
                      'late_expiry_frames':events[1]['value']['lag_frames'],'wall_s':time.monotonic()-started}))


if __name__ == '__main__': main()
