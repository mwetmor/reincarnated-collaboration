# T8 (R-C9-69): matte the NB-1 base-body sheet (plate lost -> segmentation matte via fal BiRefNet v2),
# split the 2x2 grid, and lay each view on a white 1024x1024 canvas at ONE common scale with soles on one baseline.
import sys, json, hashlib, urllib.request, fal_client, numpy as np
from PIL import Image
v=sys.argv[1] if len(sys.argv)>1 else 'a'
src=f'../artifacts/NB-1/NB-1_{v}.png'
url=fal_client.upload_file(src)
r=fal_client.subscribe('fal-ai/birefnet/v2',arguments={'image_url':url,'model':'General Use (Heavy)','operating_resolution':'2048x2048','output_format':'png','refine_foreground':True})
import subprocess; subprocess.run(['curl','-s','-L','-o',f'nb1_{v}_rgba.png',r['image']['url']],check=True)
im=Image.open(f'nb1_{v}_rgba.png').convert('RGBA'); W,H=im.size; a=np.asarray(im)[...,3]
print('matte',im.size,'alpha>0 frac %.3f'%((a>0).mean()))
quads={'front':(0,0),'right':(1,0),'back':(0,1),'left':(1,1)}   # (col,row): TL front, TR right side, BL back, BR left side
boxes={}
for name,(c,rw) in quads.items():
    q=im.crop((c*W//2,rw*H//2,(c+1)*W//2,(rw+1)*H//2)); qa=np.asarray(q)[...,3]>128
    ys,xs=np.where(qa)
    # largest connected blob only (drop stray matte specks): keep rows/cols of the main mass
    boxes[name]=(q,(xs.min(),ys.min(),xs.max()+1,ys.max()+1))
hmax=max(b[3]-b[1] for _,b in boxes.values()); S=0.88*1024/hmax; base=int(1024*0.94)
meta={}
for name,(q,(x0,y0,x1,y1)) in boxes.items():
    fig=q.crop((x0,y0,x1,y1)); w,h=fig.size; fig=fig.resize((max(1,round(w*S)),max(1,round(h*S))),Image.LANCZOS)
    can=Image.new('RGB',(1024,1024),(255,255,255)); px=(1024-fig.size[0])//2; py=base-fig.size[1]
    can.paste(fig,(px,py),fig); can.save(f'nb_{v}_{name}.jpg',quality=95)
    meta[name]=dict(src_box=[int(x0),int(y0),int(x1),int(y1)],height_px_src=int(y1-y0),scale=S,placed=[px,py,*fig.size])
    print(name,'src h',y1-y0,'placed',px,py,fig.size)
json.dump(dict(sheet=src,sha256=hashlib.sha256(open(src,'rb').read()).hexdigest(),matte='fal-ai/birefnet/v2 General Use (Heavy)',views=meta),open(f'views_{v}.json','w'),indent=1)
