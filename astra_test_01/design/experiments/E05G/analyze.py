from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
r=Path(__file__).parent;out=r/'evidence/batch-03';asset=json.loads((r/'gear.asset.json').read_text());records=[]
for i,f in enumerate(asset['frames']):
 for head in ['hidden','head']:
  src=np.array(Image.open(r/f['reference_'+('hidden'if head=='hidden'else'head')+'_path']))
  base=np.array(Image.open(r/f['body_path']));occ=(src[:,:,3]>0)|(base[:,:,3]>0)
  for bg in ['dark','light','blue']:
   a=np.array(Image.open(out/f'{i}-{head}-{bg}-layered.png')).astype(int)[:,:,:3];b=np.array(Image.open(out/f'{i}-{head}-{bg}-reference.png')).astype(int)[:,:,:3];e=abs(a-b)[occ]
   records.append({'pose':f['id'],'head':head,'bg':bg,'occupied_pixels':int(occ.sum()),'mean_abs_rgb':float(e.mean()),'fraction_pixels_error_gt8':float((e.max(1)>8).mean()),'max':int(e.max()),'p95':float(np.percentile(e.max(1),95)),'pass':bool(e.mean()<=1 and (e.max(1)>8).mean()<=.02)})
a=np.array(Image.open(out/'bad-shift.png')).astype(int)[:,:,:3];b=np.array(Image.open(out/'4-head-dark-reference.png')).astype(int)[:,:,:3];occ=(np.array(Image.open(r/asset['frames'][4]['reference_head_path']))[:,:,3]>0);e=abs(a-b)[occ];bad={'mae':float(e.mean()),'fraction_gt8':float((e.max(1)>8).mean()),'caught':bool(e.mean()>1 or (e.max(1)>8).mean()>.02)}
result={'records':records,'bad20sourcepx':bad,'checks':{'all_composites':all(x['pass']for x in records),'bad_shift_rejected':bad['caught']},'scope':'Actual native512x512 Pixi canvas buffer; errors over source occupied sprite pixels, not canvas background'}
(out/'pixel-validation.json').write_text(json.dumps(result,indent=2)+'\n')
sheet=Image.new('RGB',(900,580),(24,35,49));d=ImageDraw.Draw(sheet)
for i in range(6):
 for j,mode in enumerate(['layered','reference']):
  im=Image.open(out/f'{i}-hidden-dark-{mode}.png');sheet.paste(im.crop((175,135,325,315)),(i%3*300+j*150,i//3*280+35))
 d.text((i%3*300,i//3*280+8),asset['frames'][i]['id']+' | layers / full')
sheet.save(out/'comparison-hidden.png')
print({'checks':result['checks'],'max_mae':max(x['mean_abs_rgb']for x in records),'max_fraction':max(x['fraction_pixels_error_gt8']for x in records),'bad':bad})
