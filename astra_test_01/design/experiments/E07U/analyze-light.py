from pathlib import Path
from PIL import Image
import json,numpy as np
p=Path(__file__).resolve().parent;b=p/'evidence/batch-02';rows=[]
for f in ['F01','F02']:
 for time in [0,.25,.5]:
  ims={k:np.array(Image.open(b/f'{f}-t{time:g}-{k}.png').convert('RGB')).astype(int)for k in ['neutral','warm','bad']};delta=abs(ims['bad']-ims['warm']).max(2);lit=abs(ims['warm']-ims['neutral']).max(2);rows.append({'faction':f,'time':time,'pixels_changed_by_omitting_leaves_gt2':int((delta>2).sum()),'lit_pixels_gt2':int((lit>2).sum()),'maximum_omission_delta':int(delta.max())})
r={'records':rows,'checks':{'closed_leaf_light_control_detected':all(x['pixels_changed_by_omitting_leaves_gt2']>10 for x in rows if x['time']==0),'warm_changes_scene':all(x['lit_pixels_gt2']>10 for x in rows)},'scope':'Whole-scene sample counts; includes all leaves. Does not isolate receiver surfaces or establish shadow precision.'};(b/'light-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
