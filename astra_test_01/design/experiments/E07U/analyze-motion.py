from pathlib import Path
import json,numpy as np
p=Path(__file__).resolve().parent;b=p/'evidence/batch-02';r=json.loads((b/'motion-validation.json').read_text());rows=[]
for v in r['videos']:
 t=v['timeline'];intervals=np.diff([x['elapsed_s']for x in t])*1000;durations=[x['composition_ms']for x in t];opening=len({x['progress']for x in t if x['state']=='opening'and 0<x['progress']<1});closing=len({x['progress']for x in t if x['state']=='closing'and 0<x['progress']<1});rows.append({'faction':v['faction'],'opening_samples':opening,'closing_samples':closing,'frame_interval_median_ms':float(np.median(intervals)),'frame_interval_p95_ms':float(np.percentile(intervals,95)),'composition_median_ms':float(np.median(durations)),'composition_p95_ms':float(np.percentile(durations,95)),'pass':opening>=20 and closing>=20})
x={'records':rows,'checks':{'twenty_partial_samples_each':all(x['pass']for x in rows)},'scope':'This local Chrome/headless recording only; minimum PC and fullscreen target still undecided.'};(b/'motion-analysis.json').write_text(json.dumps(x,indent=2)+'\n');print(x)
