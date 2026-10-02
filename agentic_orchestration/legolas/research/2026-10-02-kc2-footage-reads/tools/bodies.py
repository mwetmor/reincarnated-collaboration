import json, numpy as np, collections
cam=np.load('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/method/camera_translation_60fps_683-866.npy')
ct=np.concatenate([cam[:,0],[cam[-1,0]+1/60]]); cx=np.concatenate([[0],np.cumsum(cam[:,1])]); cy=np.concatenate([[0],np.cumsum(cam[:,2])])
def W(t,x,y): return x-np.interp(t,ct,cx), y-np.interp(t,ct,cy)
frames=json.load(open('cen_all.json'))
M=json.load(open('lineup_matched.json'))
WB=[(151,682.6),(152,698.6),(153,714.9),(154,729.8),(155,744.0),(156,760.2),(157,780.4),(158,799.7),(159,812.7),(160,839.0),(161,864.8)]
def wave_of(t):
    for (w,a),(w2,b) in zip(WB,WB[1:]):
        if a<=t<b: return w
res={}
for w in range(151,161):
    keep={r['max'] for r in M[str(w)] if r['n']>=3}
    obs=collections.defaultdict(list)
    for f in frames:
        if wave_of(f['t'])!=w: continue
        for q in f['txt']:
            if q['max'] in keep and q['green']<=q['red']:
                x0,y0,x1,y1=q['box']; wx,wy=W(f['t'],(x0+x1)/2,y1)
                obs[q['max']].append((f['t'],wx,wy/0.537,q['cur']))
    out={}
    for mx,L in obs.items():
        tracks=[]
        for t,x,y,c in sorted(L):
            best=None;bd=1e9
            for tr in tracks:
                lt,lx,ly,lc=tr[-1]
                dt=t-lt
                if dt<=0 or dt>2.0: continue
                if c>lc*1.03+0.01*mx: continue   # HP cannot rise much (regen allowance)
                d=np.hypot(x-lx,y-ly)
                if d<120+250*dt and d<bd: bd=d;best=tr
            if best is None: tracks.append([(t,x,y,c)])
            else: best.append((t,x,y,c))
        n2=sum(1 for tr in tracks if len(tr)>=2)
        out[mx]=dict(tracks=len(tracks),tracks2=n2,full_onsets=sum(1 for tr in tracks if tr[0][3]>=0.98*mx))
    res[w]=out
json.dump({str(w):{str(k):v for k,v in d.items()} for w,d in res.items()},open('bodies.json','w'),indent=1)
for w,d in res.items():
    print(w, {k:(v['tracks2'],v['tracks']) for k,v in sorted(d.items(),key=lambda kv:-kv[0])})
