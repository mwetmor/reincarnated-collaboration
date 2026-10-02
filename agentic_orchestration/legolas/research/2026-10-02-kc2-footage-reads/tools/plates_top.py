import subprocess, numpy as np, json, sys
from PIL import Image
V='../ref.mp4'; W,H=1920,1080
t0,t1,fps=682.5,866.0,10
cmd=['ffmpeg','-v','error','-ss',str(t0),'-t',str(t1-t0),'-i',V,'-vf',f'fps={fps},crop=640:150:640:0','-f','rawvideo','-pix_fmt','rgb24','-']
p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
N=640*150*3; i=0; rows=[]; import os; os.makedirs('top2',exist_ok=True)
while True:
    raw=p.stdout.read(N)
    if len(raw)<N: break
    a=np.frombuffer(raw,np.uint8).reshape(150,640,3).astype(int)
    t=round(t0+i/fps,2)
    band=a[50:80,200:440]
    gold=((band[...,0]>150)&(band[...,1]>110)&(band[...,2]<100)&(band[...,0]-band[...,2]>80)).sum()
    rows.append((t,int(gold)))
    if gold>25: Image.fromarray(a.astype(np.uint8)).save(f'top2/t{t:.1f}.png')
    i+=1
json.dump(rows,open('top_presence.json','w'))
print(i, sum(1 for r in rows if r[1]>60))
