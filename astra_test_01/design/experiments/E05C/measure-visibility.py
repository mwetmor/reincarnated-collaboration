from pathlib import Path
from PIL import Image
import numpy as np,json
b=Path(__file__).resolve().parent;measurement=json.loads((b/'evidence/saved-action-validation.json').read_text());render=json.loads((b/'evidence/batch-03/render.json').read_text());ratio=(50/render['source_frame_body_height_px'])**2;rows=[]
for i in range(48):
 frame=i*2;feet=measurement['samples'][frame]['feet'];row={'frame':frame,'t':frame/120,'feet':feet,'coverage':{}}
 for kind in ['short','long-control']:
  a=np.array(Image.open(b/f'evidence/batch-03/{kind}-id-{frame:03}.png').convert('RGBA'),dtype=float)/255
  row['coverage'][kind]={side:float(np.sum(np.maximum(a[:,:,channel]-a[:,:,1-channel],0)*a[:,:,3])*ratio)for side,channel in [('L',0),('R',1)]}
 rows.append(row)
result={'criterion':'Supplementary >=1 opaque-equivalent planted boot pixel at50px body. Not visual discernibility by itself.','frames':rows,'min_stance_coverage':{kind:min(r['coverage'][kind][side]for r in rows for side in ['L','R']if r['feet'][side]['stance'])for kind in ['short','long-control']}}
result['short_all_stance_pixels_present']=result['min_stance_coverage']['short']>=1;result['long_control_has_concealed_stance']=result['min_stance_coverage']['long-control']<1
(b/'evidence/visibility.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items()if k!='frames'})
