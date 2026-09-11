from pathlib import Path
import numpy as np,json,sys
from PIL import Image
p=Path(__file__).resolve().parent;batch=sys.argv[1]if len(sys.argv)>1 else'batch-01';out=p/'evidence'/batch;rows=[]
def load(folder,h,mode):return np.array(Image.open(folder/f'idle-000-h{h:03}-{mode}.png').convert('RGBA')).astype(float)/255
def over(a,b):
 aa=a[:,:,3:4];ba=b[:,:,3:4];al=aa+ba*(1-aa);return np.concatenate(((a[:,:,:3]*aa+b[:,:,:3]*ba*(1-aa))/np.maximum(al,1e-10),al),2)
def comp(a,bg):return a[:,:,:3]*a[:,:,3:4]+np.array(bg)/255*(1-a[:,:,3:4])
conditions=['cached16','raw','partition-over','partition']if batch=='batch-01'else['partition'];hs=[45,225]if batch=='batch-01'else list(range(0,360,45))
for condition in conditions:
 folder=p.parent/'E05A/evidence/batch-02'if condition=='cached16'else out/('partition'if condition.startswith('partition')else'raw')
 for h in hs:
  for head in [True,False]:
   body=load(folder,h,'base-nohair');ref=load(folder,h,'full-head'if head else'full-hidden');keys=['armor-layer','head-layer']if head else['hair-layer','armor-layer'];layers=[load(folder,h,key)for key in keys]
   if condition=='partition':
    mask=load(folder,h,'body-mask-head'if head else'body-mask-hidden')[:,:,3:4];rgb=body[:,:,:3]*mask;alpha=mask.copy()
    for layer in layers:rgb+=layer[:,:,:3]*layer[:,:,3:4];alpha+=layer[:,:,3:4]
    result=np.concatenate((rgb/np.maximum(alpha,1e-10),np.clip(alpha,0,1)),2)
   else:
    result=body
    for layer in layers:result=over(layer,result)
   for bgname,bg in [('dark',[24,35,49]),('light',[230,223,209]),('blue',[20,81,163])]:
    a=comp(result,bg);b=comp(ref,bg);mask=(ref[:,:,3]>0)|(result[:,:,3]>0);e=abs(a-b)[mask]*255;rows.append({'condition':condition,'heading':h,'head':head,'bg':bgname,'mae':float(e.mean()),'fraction_gt8':float((e.max(1)>8).mean()),'pass':bool(e.mean()<=1 and (e.max(1)>8).mean()<=.02)})
   if condition=='partition':Image.fromarray(np.uint8(np.clip(comp(result,[24,35,49]),0,1)*255)).save(out/f'diagnostic-h{h:03}-{head}-partition.png')
summaries={c:{'checks':len([r for r in rows if r['condition']==c]),'failures':sum(not r['pass']for r in rows if r['condition']==c),'worst_mae':max(r['mae']for r in rows if r['condition']==c),'worst_fraction':max(r['fraction_gt8']for r in rows if r['condition']==c)}for c in conditions};(out/'source-analysis.json').write_text(json.dumps({'records':rows,'summaries':summaries,'scope':'Diagnostic CPU premultiplied composites at native source153.9px body axis, not GPU/50px qualification'},indent=2)+'\n');print(summaries)
