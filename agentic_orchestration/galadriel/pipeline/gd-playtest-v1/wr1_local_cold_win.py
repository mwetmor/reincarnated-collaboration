import subprocess, sys, numpy as np, json
video="/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
ss,dur,X,Y,W,H,out = float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),sys.argv[7]
cmd=["ffmpeg","-nostdin","-hide_banner","-loglevel","error","-ss",str(ss),"-i",video,"-t",str(dur),
     "-vf",f"fps=60,crop={W}:{H}:{X}:{Y}","-pix_fmt","rgb24","-f","rawvideo","-"]
n=W*H*3; p=subprocess.Popen(cmd,stdout=subprocess.PIPE,bufsize=n*4); rows=[];i=0
while True:
    b=p.stdout.read(n)
    if len(b)<n: break
    a=np.frombuffer(b,dtype=np.uint8).reshape(H,W,3).astype(np.int16)
    R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]
    hard=(B>140)&(B-R>55)&(B>=G-10); soft=(B>70)&(B-R>22)&(B>=G-14)
    rows.append(dict(pts=round(ss+i/60.0,4),hard=int(hard.sum()),soft=int(soft.sum()))); i+=1
p.stdout.close();p.wait(); json.dump(rows,open(out,"w")); print(len(rows))
