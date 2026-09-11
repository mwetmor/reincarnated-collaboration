from pathlib import Path
from PIL import Image
import json,hashlib,math,gzip,numpy as np
HERE=Path(__file__).resolve().parent
source=HERE.parent/'E05B';m=json.loads((source/'walk.asset.json').read_text())
if(HERE/'walk-atlas.png').exists():raise RuntimeError('Refuse overwrite')
items=[];hidden={}
for i,f in enumerate(m['frames']):
 im=Image.open(source/f['source_path']).convert('RGBA');a=np.array(im);mask=a[:,:,3]>0;ys,xs=np.where(mask);crop=[max(0,int(xs.min())-2),max(0,int(ys.min())-2),min(im.width,int(xs.max())+3),min(im.height,int(ys.max())+3)]
 outside=a.copy();outside[crop[1]:crop[3],crop[0]:crop[2]]=0;assert not np.any(outside[:,:,3]);flat=outside.reshape(-1,4);indices=np.where(np.any(flat[:,:3]!=0,axis=1))[0];hidden[str(i)]=[[int(j),*[int(v)for v in flat[j,:3]]]for j in indices];items.append({'index':i,'source':im,'crop':crop,'image':im.crop(crop)})
x=y=rowh=0
for a in sorted(items,key=lambda a:-a['image'].height):
 w,h=a['image'].size
 if x+w+4>1024:y+=rowh;x=0;rowh=0
 a['rect']=[x+2,y+2,w,h];x+=w+4;rowh=max(rowh,h+4)
height=2**math.ceil(math.log2(y+rowh));atlas=Image.new('RGBA',(1024,height),(0,0,0,0))
for a in items:atlas.paste(a['image'],a['rect'][:2])
atlas.save(HERE/'walk-atlas.png');ahash=hashlib.sha256((HERE/'walk-atlas.png').read_bytes()).hexdigest();checks={};new=json.loads(json.dumps(m));new['id']='controlled-wizard-walk-packed';new['path_base']='./';new['packing']='Fully transparent exterior trimmed; original RGBA pixels copied exactly; no resampling or art repair';new['original_manifest']='../E05B/walk.asset.json'
for item in items:
 i=item['index'];old=m['frames'][i];f=new['frames'][i];x,y,w,h=item['rect'];crop=item['crop'];patch=atlas.crop((x,y,x+w,y+h));rebuilt=Image.new('RGBA',item['source'].size,(0,0,0,0));raw=np.array(rebuilt);flat=raw.reshape(-1,4);
 for j,r,g,b in hidden[str(i)]:flat[j]=[r,g,b,0]
 rebuilt=Image.fromarray(raw);rebuilt.paste(patch,crop[:2]);checks[str(i)+'_reconstruct_RGBA']=np.array_equal(np.array(rebuilt),np.array(item['source']));f['source_native_frame']={'path':'../E05B/'+old['source_path'],'sha256':old['sha256'],'size':[512,512]};f['source_path']='walk-atlas.png';f['sha256']=ahash;f['atlas_coordinates']={'x':x,'y':y,'width':w,'height':h};f['crop_origin']=crop[:2];f['pivot']=[old['pivot'][j]-crop[j]for j in range(2)];checks[str(i)+'_pivot_identity']=all(f['pivot'][j]+crop[j]==old['pivot'][j]for j in range(2))
checks['no_rect_overlap']=all(i==j or a['rect'][0]+a['rect'][2]<=b['rect'][0]or b['rect'][0]+b['rect'][2]<=a['rect'][0]or a['rect'][1]+a['rect'][3]<=b['rect'][1]or b['rect'][1]+b['rect'][3]<=a['rect'][1] for i,a in enumerate(items)for j,b in enumerate(items));checks['bounds']=all(x>=0 and y>=0 and x+w<=1024 and y+h<=height for x,y,w,h in[a['rect']for a in items])
first=items[0];x,y,w,h=first['rect'];checks['bad_rect_caught']=not np.array_equal(np.array(atlas.crop((x+1,y,x+w+1,y+h))),np.array(first['image']));checks['bad_pivot_caught']=new['frames'][0]['pivot'][0]+first['crop'][0]+1!=m['frames'][0]['pivot'][0];checks['bad_fps_caught']=abs(48/59-.8)>1e-8;checks['timing_retained']=new['fps']==60 and len(new['frames'])==48 and new['duration_s']==.8
new['source_authoring']['path']='../E05B/'+m['source_authoring']['path']
new['archival_hidden_rgb_path']='outside-rgb.json.gz'
with gzip.open(HERE/'outside-rgb.json.gz','wt',encoding='utf8')as archive:json.dump({'format':'frame index to [linear pixel index,R,G,B] outside retained crop; source width512; alpha0','frames':hidden},archive,separators=(',',':'))
(HERE/'walk.asset.json').write_text(json.dumps(new,indent=2)+'\n');r={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'atlas_dimensions':[1024,height],'original_uncompressed_RGBA_bytes':48*512*512*4,'atlas_uncompressed_RGBA_bytes':1024*height*4,'note':'Texel allocation arithmetic, not observed GPU-driver memory or production capacity','atlas_sha256':ahash,'atlas_file_bytes':(HERE/'walk-atlas.png').stat().st_size}
(HERE/'evidence/packing-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k!='checks'}));assert all(checks.values())
