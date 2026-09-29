# T8: re-place each matted view at a PER-VIEW scale to one common height (main blob only; matte specks excluded).
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
v=sys.argv[1]; im=Image.open(f'nb1_{v}_rgba.png').convert('RGBA'); W,H=im.size
meta=json.load(open(f'views_{v}.json')); quads={'front':(0,0),'right':(1,0),'back':(0,1),'left':(1,1)}
TARGET=int(0.88*1024); base=int(1024*0.94); sheet=Image.new('RGB',(2048,512),(255,255,255))
for i,(name,(c,rw)) in enumerate(quads.items()):
    q=im.crop((c*W//2,rw*H//2,(c+1)*W//2,(rw+1)*H//2)); a=np.asarray(q)[...,3]
    lab,n=ndimage.label(a>128); sizes=ndimage.sum(a>128,lab,range(1,n+1)); mask=(lab==1+int(np.argmax(sizes)))
    ys,xs=np.where(mask); x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
    arr=np.asarray(q).copy(); arr[...,3]=np.where(ndimage.binary_dilation(mask,iterations=2),arr[...,3],0); q=Image.fromarray(arr,'RGBA')
    fig=q.crop((x0,y0,x1,y1)); w,h=fig.size; S=TARGET/h; fig=fig.resize((round(w*S),TARGET),Image.LANCZOS)
    can=Image.new('RGB',(1024,1024),(255,255,255)); px=(1024-fig.size[0])//2; py=base-TARGET; can.paste(fig,(px,py),fig); can.save(f'nb_{v}_{name}.jpg',quality=95)
    meta['views'][name].update(src_box=[int(x0),int(y0),int(x1),int(y1)],height_px_src=int(h),scale=S,placed=[px,py,*fig.size],blobs=int(n))
    sheet.paste(can.resize((512,512)),(i*512,0)); print(name,'h',h,'scale %.3f'%S,'blobs',n)
meta['normalisation']='per-view scale to a common height, main blob only'
json.dump(meta,open(f'views_{v}.json','w'),indent=1); sheet.save(f'nb_{v}_views_check.png')
