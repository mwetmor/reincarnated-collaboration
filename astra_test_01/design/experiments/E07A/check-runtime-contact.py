from pathlib import Path
import json,numpy as np
p=Path(__file__).resolve().parent;s=json.loads((p.parent/'E05N/evidence/source-motion.json').read_text());samples={x['frame']:x for x in s['samples']if x['clip']=='walk'};r=json.loads((p/'evidence/batch-03/playback-validation.json').read_text());out=[]
for video in r['videos']:
 if video['clip']!='walk':continue
 groups={};theta=np.deg2rad(-video['heading']);rot=np.array([[np.cos(theta),-np.sin(theta)],[-np.sin(theta),-np.cos(theta)]])
 for row in video['timeline']:
  if not 0<=row['clip_time_s']<.8:continue
  frame=row['active_frame'];src=samples[frame]
  for side,foot in src['feet'].items():
   if not foot['stance']:continue
   local=np.array(foot['world'][:2])-[2*frame/60,0];world=rot@local+row['point'];groups.setdefault((side,foot['cycle']),[]).append(world)
 metrics=[]
 for key,points in groups.items():
  a=np.array(points);drift=float(np.max(np.linalg.norm(a[:,None,:]-a[None,:,:],axis=2)));metrics.append({'side_cycle':list(key),'samples':len(a),'max_pairwise_drift_m':drift,'pass':drift<=.02})
 out.append({'outfit':video['outfit'],'groups':metrics,'pass':all(x['pass']for x in metrics)})
q={'videos':out,'scope':'Reconstructs stored source frame sole contacts (which include frame-time translation) and actual recorded runtime root; not a new mesh or pixel contact sample. Remove stored frame translation, rotate local contacts, add recorded root. Source source-motion.json hash is inherited E05N evidence.','checks':{'all_recorded_walk_contacts':all(x['pass']for x in out)}};(p/'evidence/batch-03/runtime-contact.json').write_text(json.dumps(q,indent=2)+'\n');print(q['checks'])
