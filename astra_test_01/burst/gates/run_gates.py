"""CLI and regression measurements. Never loads implicit annotation/config files.
Optional reviewed contacts/root/plant data can be supplied to run() as dictionaries.
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
if __package__ in (None,''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from gates.common import DIRS, COUNTS, rgba, measure, difference, pair_differences, result
from gates.register import frame_contacts
from gates import g1_height,g2_pivot,g3_light,g5_drift,g6_seam,g9_alpha,drift48,silhouette64


def measurements(frames_dir, regions=None):
    """Regenerate legacy height/pivot/drift/seam values from actual PNGs.
    regions keys are relative animation/direction/filename paths. The regression
    lock is never used as an annotation or as a source of computed values.
    """
    root=Path(frames_dir); directions={}; regions=regions or {}
    for d in DIRS:
        animations={}
        for anim,count in COUNTS.items():
            files=sorted((root/anim/d).glob('*.png')); rows=[]
            for f in files:
                im=rgba(f);r=measure(im);r['file']=f.relative_to(root).as_posix()
                try:
                    p=frame_contacts(im,regions.get(r['file']))
                    r.update(sole_points=p,sole_midpoint_error=np.abs(np.mean(p,axis=0)-[256,400]).tolist())
                except ValueError as e: r['contact_error']=str(e)
                rows.append(r)
            item={'frames':rows,'available':len(files),'required':count}
            if anim in ('idle','walk') and len(files)==count:
                item['adjacent_and_seam']=pair_differences(files)
                cast=root/'cast'/d/f'cast_{d}_05.png'
                if cast.exists(): item['cross_cast_05']=difference(files[0],cast)
            animations[anim]=item
        directions[d]={'animations':animations}
    return {'directions':directions}


def regression_diff(actual, expected, tolerance=1e-3):
    """Every recorded height, pivot XY, pair MAD (canvas/union), cross MAD.
    Returns precise differences rather than modifying measurements to match.
    """
    diffs=[]; compared=0
    def compare(path,a,b):
        nonlocal compared
        if isinstance(b,list):
            if not isinstance(a,list) or len(a)!=len(b):
                diffs.append(dict(path=path,expected=b,actual=a));return
            for i,v in enumerate(b):compare(f'{path}/{i}',a[i],v)
        elif isinstance(b,dict):
            for k,v in b.items():compare(f'{path}/{k}',a.get(k) if isinstance(a,dict) else None,v)
        else:
            compared+=1
            if a is None or abs(a-b)>tolerance:diffs.append(dict(path=path,expected=b,actual=a,delta=None if a is None else a-b))
    for d,r in expected['directions'].items():
        for anim,item in r['animations'].items():
            got=actual['directions'][d]['animations'][anim];prefix=f'{d}/{anim}'
            compare(prefix+'/available',got['available'],item['available'])
            by_name={Path(x['file']).name:x for x in got['frames']}
            for row in item['frames']:
                name=Path(row['file']).name; other=by_name.get(name,{})
                for key in ('height','sole_points','sole_midpoint_error'):
                    if key in row:compare(f'{prefix}/{name}/{key}',other.get(key),row[key])
            for key in ('adjacent_and_seam','cross_cast_05'):
                if key in item:compare(prefix+'/'+key,got.get(key),item[key])
    return dict(tolerance=tolerance,compared=compared,differences=diffs,within_tolerance=not diffs)


def run(frames_dir,master,regions=None,anchors=None,plants=None,dark_threshold=None):
    root=Path(frames_dir); rows=[];regions=regions or {};anchors=anchors or {};plants=plants or {}
    master=rgba(master)
    for d in DIRS:
        for anim,count in COUNTS.items():
            files=sorted((root/anim/d).glob('*.png')); subject=f'{anim}/{d}'
            rows.append(result('frame_count',subject,len(files),count,op='==',unit='frames'))
            for f in files:
                key=f.relative_to(root).as_posix();im=rgba(f)
                rows.extend([g1_height.evaluate(im,master,key),g3_light.evaluate(im,key),
                             g2_pivot.root_anchor(anchors.get(key),key),g2_pivot.visible_midpoint(im,key,regions.get(key)),
                             silhouette64.evaluate(im,master,key)])
                rows.extend(g9_alpha.evaluate(im,key,dark_threshold))
            if anim in ('idle','walk'):
                if len(files)==count:
                    cast=root/'cast'/d/f'cast_{d}_05.png';cast=cast if cast.exists() else None
                    rows.extend([g5_drift.evaluate(files,cast,subject),drift48.evaluate(files,cast,subject)])
                    rows.extend(g6_seam.evaluate(files,subject))
                else:
                    for id in ('g5_drift','drift48','g6_seam','g6b'):
                        rows.append(result(id,subject,notes='UNEVALUABLE: incomplete sequence'))
                plant=g2_pivot.planted_trajectory(subject=subject,**plants.get(subject,{}))
                rows.extend(plant if isinstance(plant,list) else [plant])
    return rows


def main():
    p=argparse.ArgumentParser();p.add_argument('--frames-dir',required=True);p.add_argument('--master',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();rows=run(a.frames_dir,a.master);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(rows,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':main()
