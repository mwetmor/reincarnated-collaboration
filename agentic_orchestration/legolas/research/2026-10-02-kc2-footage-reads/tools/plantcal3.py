"""Identity-certain stationary calibration: the plant's own (cur/max) fingerprint at 60 fps,
camera-compensated exactly as Lap H-2 d1b.world, then the referent's velocity rule
(15-frame boxcar, np.gradient, still < 50 gpx/s) on segments with gaps <= 12 frames."""
import numpy as np, json, glob
K=0.537
cam=np.load('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/method/camera_translation_60fps_683-866.npy')
ct=np.concatenate([cam[:,0],[cam[-1,0]+1/60]]); cx=np.concatenate([[0],np.cumsum(cam[:,1])]); cy=np.concatenate([[0],np.cumsum(cam[:,2])])
F=[]
for f in sorted(glob.glob('cal/c_*.json')): F+=json.load(open(f))['frames']
F.sort(key=lambda f:f['t'])
out={}
for win,(a,b,fps_) in {'w151_692_698':(692,698,(272948,278543)),'w153_719_729':(719,729.2,(273975,))}.items():
    res=[]
    for mx in fps_:
        obs=[]
        for f in F:
            if not a<=f['t']<=b: continue
            for q in f['txt']:
                if q['max']==mx and q['red']>=q['green']:
                    x0,y0,x1,y1=q['box']; t=f['t']
                    obs.append((t,(x0+x1)/2-np.interp(t,ct,cx),(y1+21-np.interp(t,ct,cy))/K,(x0+x1)/2,y1+21))
        # link into bodies by world proximity (gate 90 gpx, gap 0.5 s)
        tracks=[]
        for o in obs:
            best=None;bd=1e9
            for tr in tracks:
                if o[0]-tr[-1][0]>0.5 or o[0]==tr[-1][0]: continue
                d=np.hypot(o[1]-tr[-1][1],o[2]-tr[-1][2])
                if d<90 and d<bd: bd=d;best=tr
            (best.append(o) if best is not None else tracks.append([o]))
        for tr in tracks:
            tr=np.array(tr)
            if len(tr)<30: continue
            t=tr[:,0]; fi=np.round((t-a)*60).astype(int)
            # segments with gaps <= 12 frames, interpolate to 60 fps grid
            segs=np.split(np.arange(len(fi)),np.where(np.diff(fi)>12)[0]+1)
            still=[];spd=[]
            for s in segs:
                if len(s)<20: continue
                g=np.arange(fi[s[0]],fi[s[-1]]+1)
                wx=np.interp(g,fi[s],tr[s,1]); wy=np.interp(g,fi[s],tr[s,2])
                if len(g)<17: continue
                ker=np.ones(15)/15
                sx=np.convolve(wx,ker,'same')[7:-7]; sy=np.convolve(wy,ker,'same')[7:-7]
                v=np.hypot(np.gradient(sx),np.gradient(sy))*60
                spd+=list(v); still+=list(v<50)
            md=np.median(tr[:,1]),np.median(tr[:,2])
            r=np.hypot(tr[:,1]-md[0],tr[:,2]-md[1])
            rng=np.median(np.hypot(tr[:,3]-960,(tr[:,4]-544)/K))
            step=np.hypot(np.diff(tr[:,1]),np.diff(tr[:,2]))[np.diff(fi)==1]
            res.append(dict(fingerprint=mx,readouts=len(tr),t=[float(t[0]),float(t[-1])],coverage=round(len(tr)/((t[-1]-t[0])*60+1),2),
                still_frac=round(float(np.mean(still)),3) if still else None, n_vel_frames=len(still),
                speed_med_gpx_s=round(float(np.median(spd)),1) if spd else None,
                world_resid_med_gpx=round(float(np.median(r)),1),world_resid_p90_gpx=round(float(np.percentile(r,90)),1),
                step_gt12_frac=round(float((step>12).mean()),3) if len(step) else None,
                range_plate_to_player_gpx_med=round(float(rng)),cam_travel_px=[round(float(np.ptp(np.interp(t,ct,cx)))),round(float(np.ptp(np.interp(t,ct,cy))))]))
    out[win]=res
json.dump(out,open('plant_calibration_60fps.json','w'),indent=1)
for k,v in out.items():
    print(k)
    for r in v: print('  ',r)
