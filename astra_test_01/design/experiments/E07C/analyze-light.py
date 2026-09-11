from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent/'evidence/batch-02';im=lambda name:np.array(Image.open(p/(name+'.png')).convert('RGB')).astype(int);off,on=im('light-neutral-off'),im('light-neutral-on');mask=(off-on).max(2)>2;rows=[]
for light in ['warm','cool']:
 a,b=im('light-'+light+'-on'),im('light-'+light+'-off');gain=(a-on)[mask];delta=(b-a)[mask];rows.append({'light':light,'shadow_pixels':int(mask.sum()),'mean_point_gain_while_shadowed':gain.mean(0).tolist(),'minimum_point_gain':int(gain.min()),'mean_directional_darkening':delta.mean(0).tolist(),'minimum_directional_darkening':int(delta.min()),'pass':bool(mask.sum()>20 and gain.max()>2 and gain.min()>=0 and delta.min()>=0 and delta.mean()>1)})
r={'records':rows,'checks':{'point_retained_while_directional_removed':all(x['pass']for x in rows)},'scope':'Image-consistency probe in the point-light pool. Shadow mask is selected from the neutral on/off difference; these are not additional independent CPU witnesses. Independent source witness matrix is recorded separately.'};(p/'light-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
