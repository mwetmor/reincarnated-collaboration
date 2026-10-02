"""Known-stationary calibration (KP-221 R6): the Carnivorous Plant (ControllerStationaryMonster,
never moves) measured through the Lap H-2/R plate pipeline: plates60 detections, camera trace,
d1b.track linking (gate 30 gpx, gap 12), 15-frame boxcar, still = speed < 50 gpx/s."""
import numpy as np, json, sys
import d1b
K=0.537
R=np.load('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-r-locomotion-contact/method/plates60_lapH2.npy')
cam=np.load('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/method/camera_translation_60fps_683-866.npy')
ct=np.concatenate([cam[:,0],[cam[-1,0]+1/60]]); cx=np.concatenate([[0],np.cumsum(cam[:,1])]); cy=np.concatenate([[0],np.cumsum(cam[:,2])])
W,pw=d1b.world(R,ct,cx,cy)
F=json.load(open('cen_all.json'))
PLANT={272948,278543,273975}
seeds=[]
for f in F:
    for q in f['txt']:
        if q['max'] in PLANT:
            x0,y0,x1,y1=q['box']; seeds.append((f['t'],(x0+x1)/2,y1+21,q['max']))
out={}
for name,(t0,t1) in {'w151_692_698':(692.0,698.0),'w153_719_729':(719.0,729.0)}.items():
    tr=d1b.track(W,t0,t1)
    lab=[]
    for k,T in enumerate(tr):
        p=np.array(T['p'])  # t,wx,wy,sx,sy,w
        hits=0; fps=set()
        for (ts,xs,ys,mx) in seeds:
            if not (t0<=ts<=t1): continue
            j=np.argmin(np.abs(p[:,0]-ts))
            if abs(p[j,0]-ts)<0.01 and np.hypot(p[j,3]-xs,p[j,4]-ys)<14: hits+=1; fps.add(mx)
        if hits: lab.append((k,hits,sorted(fps),len(p)))
    res=[]
    for k,h,fps,n in lab:
        p=np.array(tr[k]['p']); t=p[:,0]; wx=p[:,1]; wy=p[:,2]/K
        rec=dict(track=k,seed_hits=h,fingerprints=fps,frames=n,t0=float(t[0]),t1=float(t[-1]))
        if n>=17:
            ker=np.ones(15)/15
            sx=np.convolve(wx,ker,'same'); sy=np.convolve(wy,ker,'same')
            dt=np.gradient(t); vx=np.gradient(sx)/dt; vy=np.gradient(sy)/dt
            sp=np.hypot(vx,vy)[7:-7]
            step=np.hypot(np.diff(wx),np.diff(wy))
            rec.update(still_frac=float((sp<50).mean()), speed_med=float(np.median(sp)), speed_p90=float(np.percentile(sp,90)),
                pos_sd_gpx=[float(np.std(wx)),float(np.std(wy))], pos_range_gpx=[float(np.ptp(wx)),float(np.ptp(wy))],
                jump_frac_gt12=float((step>12).mean()), screen_x=[float(p[:,3].min()),float(p[:,3].max())], screen_y=[float(p[:,4].min()),float(p[:,4].max())],
                range_to_player_gpx_med=float(np.median([np.hypot(p[i,3]-960,(p[i,4]-544)/K) for i in range(n)])))
        res.append(rec)
    out[name]=res
json.dump(out,open('plant_calibration.json','w'),indent=1)
for k,v in out.items():
    print(k)
    for r in v: print('  ',{a:(round(b,3) if isinstance(b,float) else b) for a,b in r.items()})
