import numpy as np, sys, json
sys.path.insert(0,'/tmp/pm4h2')
from d1b import *

WAVES=[(151,688.0,698.5),(152,699.0,714.7),(153,715.2,729.5),(154,730.2,743.8),
       (155,744.3,760.0),(156,760.5,780.2),(157,780.7,799.5),(158,800.0,812.5),
       (159,813.0,838.8),(160,839.3,864.0)]
V_STILL   = 50.0     # ground px/s  (monster world-speed histogram: mode 0-40, floor ~46 at p25)
R_CONTACT = 150.0    # ground px    (visual calibration, frames 783.0 / 824.4)
MIN_STALL = 1.5      # s
MIN_LAT   = 1.0      # s

def spans(mask, minlen):
    out=[];i=0
    while i<len(mask):
        if mask[i]:
            j=i
            while j<len(mask) and mask[j]: j+=1
            if (j-i)>=minlen: out.append((i,j))
            i=j
        else: i+=1
    return out

def classify(k):
    t=k['t']; spd=k['spd']; r=k['r']; vt=k['vt']; vr=k['vr']; blk=k['blocked']
    n15=int(MIN_STALL*FPS); n10=int(MIN_LAT*FPS)
    ev={}
    # STALL: still + blocked + outside contact
    m_st=(spd<V_STILL)&blk&(r>R_CONTACT)
    st=spans(m_st,n15)
    # LATERAL: blocked, outside contact, moving, tangential-dominant
    m_lat=blk&(r>R_CONTACT)&(spd>V_STILL)&(vt>np.abs(vr))
    la=spans(m_lat,n10)
    la=[(a,b) for (a,b) in la if np.trapezoid(vt[a:b],t[a:b])>=100.0]
    ev['stall_spans']=[(float(t[a]),float(t[b-1]-t[a])) for a,b in st]
    ev['lat_spans']=[(float(t[a]),float(t[b-1]-t[a]),float(np.trapezoid(vt[a:b],t[a:b]))) for a,b in la]
    ev['blocked_frac']=float(blk.mean()); ev['r_med']=float(np.median(r))
    ev['r0']=float(r[0]); ev['r1']=float(r[-1]); ev['spd_med']=float(np.median(spd))
    ev['vt_med']=float(np.median(vt)); ev['vr_med']=float(np.median(vr))
    ev['contact_frac']=float((r<=R_CONTACT).mean())
    ev['dur']=float(t[-1]-t[0])
    if st and la: lab='MIXED'
    elif st: lab='R1-STALLED-BEHIND'
    elif la: lab='R2-LATERAL-RESOLVED'
    elif ev['contact_frac']>0.5: lab='IN-CONTACT'
    elif np.median(vr)>60: lab='APPROACH-DIRECT'
    elif ev['blocked_frac']<0.2: lab='UNBLOCKED-NO-TEST'
    else: lab='INDETERMINATE'
    return lab,ev

if __name__=='__main__':
    R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
    rows=[]
    for wave,t0,t1 in WAVES:
        trs=track(W,t0,t1)
        idx=0
        for tr in sorted(trs,key=lambda x:-len(x['p'])):
            if len(tr['p'])<int(1.5*FPS): continue
            k=kinematics(tr,pw,W)
            if k is None: continue
            lab,ev=classify(k)
            idx+=1
            rows.append(dict(track_id='W%d-T%02d'%(wave,idx),wave=wave,
                             t_start=float(tr['p'][0][0]),t_end=float(tr['p'][-1][0]),
                             n_frames=len(tr['p']),label=lab,**ev))
    json.dump(rows,open('/tmp/pm4h2/d1rows.json','w'),indent=1)
    import collections
    c=collections.Counter(r['label'] for r in rows)
    print('tracks >=1.5 s:',len(rows))
    for k2,v in c.most_common(): print('  %-22s %d'%(k2,v))
    print()
    print('per wave:')
    for wave,_,_ in WAVES:
        cc=collections.Counter(r['label'] for r in rows if r['wave']==wave)
        print('  w%d  n=%2d  %s'%(wave,sum(cc.values()),dict(cc)))
