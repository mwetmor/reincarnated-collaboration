import numpy as np, subprocess, os, sys
from PIL import Image
V="/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"
a=np.load('work/cam2.npy'); T=a[:,0]; DX=a[:,1]; DY=a[:,2]
def stab(tag, s, e, cw=1000, ch=780, bx=460, by=150, step=2):
    outdir=f'work/{tag}'; os.makedirs(outdir, exist_ok=True)
    tmp=f'work/_tmp_{tag}'; os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp): os.remove(os.path.join(tmp,f))
    subprocess.run(['ffmpeg','-v','error','-ss',str(s),'-t',str(e-s),'-i',V,'-vf','fps=4','-start_number','0',f'{tmp}/n%03d.png'],check=True)
    files=sorted(os.listdir(tmp))
    idx0=int(round((s-683)/0.25))
    cx=cy=0.0
    for k,fn in enumerate(files):
        if k>0:
            j=idx0+k-1
            if 0<=j<len(DX):
                cx+=DX[j]; cy+=DY[j]
        if k%step: continue
        ox=int(round(bx+4*cx)); oy=int(round(by+4*cy))
        ox=max(0,min(1920-cw,ox)); oy=max(0,min(1080-ch,oy))
        im=Image.open(os.path.join(tmp,fn)).crop((ox,oy,ox+cw,oy+ch))
        im.convert('RGB').save(f'{outdir}/{tag}_{s+k*0.25:.2f}.jpg', quality=72)
    for f in os.listdir(tmp): os.remove(os.path.join(tmp,f))
    os.rmdir(tmp)
    print(tag, 'done', sorted(os.listdir(outdir)))
if __name__=='__main__':
    stab(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
