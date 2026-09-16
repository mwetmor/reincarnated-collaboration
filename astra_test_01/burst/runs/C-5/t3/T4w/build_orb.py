"""T4w metadata re-bake; existing pixel-union grouping is preserved below."""
from pathlib import Path
import copy
import hashlib
import json
import math
import tempfile
import numpy as np
from PIL import Image
from export.effect_kit import build, load_kit, orb_schedule_report


def original_pixel_union_grouping(src, d, w):
    # Reuse all T4r pixels: deterministic nearest-angle unions turn 22 masks into 16
    # motion groups. No coverage is discarded, bridged, recoloured or resampled.
    record=json.loads((src/d['pieces']['source']).read_text());folder=w/'grouped_pieces';folder.mkdir(exist_ok=True)
    with Image.open(src/'pieces'/record['peak_index']) as im:peak=np.array(im)
    groups=[]
    for item in record['pieces']:
     with Image.open(src/'pieces'/item['mask']) as im: rgba=np.array(im)
     groups.append({'ids':[item['id']],'rgba':rgba,'angle':item['radial_angle_deg']%360})
    while len(groups)>16:
     groups.sort(key=lambda g:g['angle']);a=min(range(len(groups)),key=lambda i:(groups[(i+1)%len(groups)]['angle']-groups[i]['angle'])%360);b=(a+1)%len(groups)
     ga,gb=groups[a],groups[b];rgba=ga['rgba'].copy();mask=gb['rgba'][...,3]>0;rgba[mask]=gb['rgba'][mask]
     ys,xs=np.nonzero(rgba[...,3]);angle=math.degrees(math.atan2(ys.mean()-record['centre'][1],xs.mean()-record['centre'][0]))%360
     groups=[g for i,g in enumerate(groups) if i not in [a,b]]+[{'ids':ga['ids']+gb['ids'],'rgba':rgba,'angle':angle}]
    new=[];union=np.zeros_like(peak);provenance=[]
    for i,g in enumerate(sorted(groups,key=lambda g:g['angle'])):
     rgba=g['rgba'];ys,xs=np.nonzero(rgba[...,3]);weights=rgba[...,3][ys,xs].astype(float);cx=np.average(xs,weights=weights);cy=np.average(ys,weights=weights);j=np.argmin((xs-cx)**2+(ys-cy)**2);pivot=[int(xs[j]),int(ys[j])];name='piece_%03d.png'%(i+1)
     Image.fromarray(rgba).save(folder/name);mask=rgba[...,3]>0;union[mask]=rgba[mask]
     new.append(dict(id=i+1,mask=name,pivot=pivot,area_px=len(xs),dominant_band=int(np.bincount((rgba[...,0][mask]//85).astype(int),minlength=4).argmax()),radial_angle_deg=i*22.5,radial_distance_px=math.hypot(cx-record['centre'][0],cy-record['centre'][1])))
     provenance.append({'id':i+1,'source_ids':g['ids']})
    assert np.array_equal(union,peak)
    Image.fromarray(peak).save(folder/record['peak_index']);record['pieces']=new
    (folder/'pieces.json').write_text(json.dumps(record,indent=2)+'\n')
    (w/'piece_grouping.json').write_text(json.dumps({'source_count':22,'motion_groups':16,'union_exact':True,'groups':provenance},indent=2)+'\n')
    return folder, record


def rebake(root):
    work=root/'runs/C-5/t3/T4w'
    kit=root/'runs/C-5/vfx_kits/v9/frozen_orb_e3'
    corrected=root/'runs/C-5/artifacts/T4v/frozen_orb_spec_corrected_R-C5-72.json'
    literal=root/'runs/C-5/specs/frozen_orb.json'
    corrected_bytes=corrected.read_bytes()
    data=json.loads((kit/'kit.json').read_text())
    data['skill_spec']=json.loads(corrected_bytes)
    data['orb'].pop('interval_frames',None)
    data['orb']['interval_frames_choices']=[2,3]
    data['phases']['travel']['speed_px_s']=data['skill_spec']['mechanics']['speed_px_s']
    data.pop('distance_fields')
    for phase in data['phases'].values():
        phase['sheet']=str(kit/phase['sheet'])
        for frame in phase['frames']:frame['file']=str(kit/frame['file'])
    for role in ('body','shard'):data['orb'][role]['png']=str(kit/data['orb'][role]['png'])
    data['pieces']['source']=str(kit/data['pieces']['source'])
    data['layers']['decal']['file']=str(kit/data['layers']['decal']['file'])
    with tempfile.TemporaryDirectory(prefix='rebake-',dir=work) as temp:
        staging=Path(temp)/'kit'
        result=build(data,staging)
        # Compare every runtime asset before publishing only kit.json.
        original={p.relative_to(kit) for p in kit.rglob('*') if p.is_file()}
        rebuilt={p.relative_to(staging) for p in staging.rglob('*') if p.is_file()}
        assert original==rebuilt, (original-rebuilt,rebuilt-original)
        for rel in sorted(original-{Path('kit.json')}):
            assert (kit/rel).read_bytes()==(staging/rel).read_bytes(), str(rel)
        load_kit(staging)
        literal.write_bytes(corrected_bytes)
        (kit/'kit.json').write_bytes((staging/'kit.json').read_bytes())
    report=orb_schedule_report(load_kit(kit))
    (work/'rebake.json').write_text(json.dumps({'build':result,'schedule':report,'all_non_metadata_bytes_identical':True},indent=2)+'\n')
    return report


if __name__=='__main__':
    print(json.dumps(rebake(Path(__file__).resolve().parents[4]),indent=2))
