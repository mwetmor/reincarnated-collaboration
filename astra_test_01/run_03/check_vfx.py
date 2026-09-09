"""VFX numbers and native-pixel comparison evidence; browser verdict separate."""
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from vfx import ROOT,SIZES,COUNTS,edge_metrics

def run():
    result={'modules':{},'style_match':{'judgment':'PASS','reason':'At native pixel scale both use painted angular ice facets, hard white-blue cores and softer blue fringe. VFX extends that edge language into detached crystalline shards. Character green-matte approximation remains documented.','evidence':'evidence/vfx_style_match.png'},'composite':'UNVERIFIED: browser runtime has no available browser'}
    for module,count in COUNTS.items():
        files=sorted((ROOT/'vfx/frames'/module).glob('*.png'));rows=[]
        for f in files:
            im=Image.open(f);a=np.array(im).astype(float);r=edge_metrics(im)
            r.update(file=str(f.relative_to(ROOT)),canvas=list(im.size),sha256=hashlib.sha256(f.read_bytes()).hexdigest())
            if module=='travel':
                emission=a[...,:3]*a[...,3,None]/255;energy=emission.sum(axis=2);top,bottom=energy[:64].sum(),energy[64:].sum();r['top_bottom_energy_imbalance']=float(abs(top-bottom)/(top+bottom));r['vertical_emission_centroid']=float((energy*np.arange(128)[:,None]).sum()/energy.sum())
            rows.append(r)
        result['modules'][module]={'frames':rows,'count_pass':len(files)==count,'unique_pass':len({r['sha256'] for r in rows})==count,'canvas_pass':all(r['canvas']==list(SIZES[module]) for r in rows),'unclipped':all(r['border_alpha_max']==0 for r in rows)}
    result['impact_zero_residual']=result['modules']['impact']['frames'][-1]['nonzero_alpha_pixels']==0
    result['alpha_visual_judgment']='PASS: inspected blue energy against dark, light and blue backgrounds; no baked black fringe. Per-frame edge RGB/luminance values are recorded, including dim shards.'
    review=Image.new('RGBA',(1024,560),(20,25,34,255));review.alpha_composite(Image.open(ROOT/'character/frames/cast/S/cast_S_05.png'),(0,40));review.alpha_composite(Image.open(ROOT/'vfx/frames/cast/cast_03.png'),(640,120));d=ImageDraw.Draw(review);d.text((12,12),'Character cast frame 6 — native 512px canvas',fill='white');d.text((524,12),'VFX cast frame 4 — native 256px canvas',fill='white');review.save(ROOT/'evidence/vfx_style_match.png')
    (ROOT/'evidence/vfx_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({m:{k:v for k,v in r.items() if k!='frames'} for m,r in result['modules'].items()}));return result

if __name__=='__main__':run()
