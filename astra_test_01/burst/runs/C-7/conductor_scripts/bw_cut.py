# Conductor cut+measure for the Blackwater video spine (R-C7-0 gates). Conductor tooling, not lane code.
# usage: bw_cut.py <clip.mp4> <outdir>   -- ffmpeg frames -> key green -> luma -> posterise 4 planes -> gates JSON + contact sheet
import sys, subprocess, pathlib, json, numpy as np
from PIL import Image
clip, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
fr = out/'frames'; fr.mkdir(exist_ok=True)
probe = subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames,duration','-of','csv=p=0',str(clip)],capture_output=True,text=True).stdout.strip()
subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),str(fr/'f_%04d.png')],check=True)
files = sorted(fr.glob('f_*.png')); n=len(files)
W,H = Image.open(files[0]).size; fps = eval(probe.split(',')[2]) if probe else 24.0
SEED_LEVELS = np.array([0.08,0.30,0.65,0.95])   # near-black / dark / light / white (four-plane register)
rows=[]; masks=[]
for i,f in enumerate(files):
    a = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)/255
    r,g,b = a[...,0],a[...,1],a[...,2]
    plate = (g>r+0.15)&(g>b+0.15)     # HUE key (R-C7-0a): a pale-green halo is plate, not subject
    subj = ~plate
    luma = 0.299*r+0.587*g+0.114*b
    band = np.abs(luma[...,None]-SEED_LEVELS[None,None,:]).argmin(-1)
    dark = subj & (band<=1); bright = subj & (band>=2); white = subj&(band==3)
    ys,xs = np.where(subj)
    if len(xs)>50:
        x0,x1,y0,y1 = np.percentile(xs,1),np.percentile(xs,99),np.percentile(ys,1),np.percentile(ys,99)
        low = ys > y1-0.35*(y1-y0)                      # pool band = bottom 35 % of the subject rows
        px0,px1 = np.percentile(xs[low],1),np.percentile(xs[low],99)
        bw,bh = px1-px0, (y1-y0)*0.35/0.5              # width from the pool band; height estimated from the band (ellipse lower half ~ 0.5 h)
        bh = y1 - np.percentile(ys[low],1)             # crude: pool band height
    else: x0=x1=y0=y1=bw=bh=0
    fy,fx = np.where(bright); flame_top = (y0 - np.percentile(fy,1)) if len(fy)>50 else 0
    # chroma of subject (should be ~0: greyscale register)
    sat = (a.max(-1)-a.min(-1))[subj].mean() if subj.any() else 0
    rows.append(dict(i=i,t=round(i/fps,3),plate=float(plate.mean()),subj_px=int(subj.sum()),dark_px=int(dark.sum()),bright_px=int(bright.sum()),white_px=int(white.sum()),
                     dark_w=float(bw),dark_h=float(bh),dark_aspect=float((2*bh)/bw) if bw else 0,light_share=float(((band[subj]>=2).sum())/max(1,subj.sum())),flame_above=float(flame_top),sat=float(sat),
                     bands=[int((band[subj]==k).sum()) for k in range(4)]))
    masks.append(subj)
# derived gates
bright=np.array([r['bright_px'] for r in rows]); white=np.array([r['white_px'] for r in rows]); dw=np.array([r['dark_w'] for r in rows]); plate=np.array([r['plate'] for r in rows])
peak = int(white.argmax()); t_peak = peak/fps
final_w = float(np.median(dw[-int(fps):])) if n>fps else float(dw[-1])
stable_from = next((i for i,r in enumerate(rows) if i>int(0.4*fps) and r['dark_w']>=0.9*final_w), None)   # after the flash; pool at 90 % of its final width
steady = dw[stable_from: int(n*0.7)] if stable_from is not None else dw
drift = float((steady.max()-steady.min())/steady.max()) if steady.size and steady.max() else 1.0
# flicker: detrended autocorrelation of the bright-pixel count over the steady window
seg = bright[stable_from: int(n*0.75)].astype(float) if stable_from is not None else bright.astype(float)
if seg.size>20:
    k=min(9,seg.size//3|1); ma=np.convolve(seg,np.ones(k)/k,'same'); d=seg-ma; d=d-d.mean()
    ac=np.correlate(d,d,'full')[d.size-1:]; ac/=ac[0] if ac[0] else 1
    zc=next((l for l in range(1,len(ac)) if ac[l]<0),None); pk=next((l for l in range(2,len(ac)-1) if ac[l]>ac[l-1] and ac[l]>ac[l+1] and l> (zc or 1)),None)
    flick_hz = fps/pk if pk else None; coherence = float(ac[pk]) if pk else None
else: flick_hz=coherence=None
# scene cut: max frame-to-frame subject-mask change
cuts = [float(np.logical_xor(masks[i],masks[i-1]).mean()) for i in range(1,n)]
tail_static = float(np.mean(cuts[-int(fps):])) if n>fps else None
flame_ratio = float(np.max([r['flame_above'] for r in rows[stable_from:]]) / dw.max()) if stable_from is not None and dw.max() else None
gates = dict(probe=probe, frames=n, fps=fps, size=[W,H],
  plate_green_min=float(plate.min()), plate_ok=bool(plate.min()>0.5),
  final_dark_w_px=float(dw[-int(fps):].mean()) if n>fps else float(dw[-1]), final_dark_w_frac=float(dw[-int(fps):].mean()/W) if n>fps else None,
  dark_aspect_steady=float(np.median([r['dark_aspect'] for r in rows[stable_from:int(n*0.7)]])) if stable_from is not None else None,
  stable_from_s=(stable_from/fps) if stable_from is not None else None, footprint_drift=drift, footprint_ok=bool(drift<=0.15),
  white_peak_frame=peak, white_peak_s=t_peak, single_peak=bool((white>0.8*white.max()).sum()<=int(fps*0.5)),
  flicker_hz=flick_hz, flicker_coherence=coherence, flame_height_over_pool_w=flame_ratio,
  max_mask_jump=float(max(cuts)) if cuts else None, tail_mean_jump=tail_static,
  subject_sat_mean=float(np.mean([r['sat'] for r in rows])),
  light_share_steady=float(np.median([r['light_share'] for r in rows[stable_from:int(n*0.7)]])) if stable_from is not None else None,
  value_register_ok=bool(np.median([r['light_share'] for r in rows[stable_from:int(n*0.7)]])>=0.2) if stable_from is not None else None)
json.dump(dict(gates=gates,rows=rows), open(out/'measure.json','w'), indent=1)
# contact sheet: 24 frames evenly
sel = np.linspace(0,n-1,24).astype(int); th=[Image.open(files[i]).resize((W//4,H//4)) for i in sel]
sheet=Image.new('RGB',(6*W//4,4*H//4),(0,0,0))
for j,im in enumerate(th): sheet.paste(im,((j%6)*W//4,(j//6)*H//4))
sheet.save(out/'sheet.png'); print(json.dumps(gates,indent=1))
