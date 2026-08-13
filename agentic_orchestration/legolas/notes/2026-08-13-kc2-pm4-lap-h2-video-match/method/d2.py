"""D2 -- ring density: simultaneous melee contact count.

Contact criterion: monster plate anchor within R_CONTACT ground px of the player's
plate anchor, both in the SCREEN frame (the camera is player-locked, so screen == 
player-relative), with the ground plane de-projected by K=0.537.

R_CONTACT = 150 ground px, calibrated by direct visual inspection on frames 783.000
and 824.400 (rings drawn at 100/150/200/300 ground px; bodies whose sprites abut the
player fall inside 150, the next rank sits at 200-270).  Reported alongside 120 and
180 as sensitivity.

EVERY COUNT IS A LOWER BOUND (NOTE-9): it counts monsters that carry a visible
nameplate. Nameplate presence proves a living monster; absence does not prove absence.
"""
import numpy as np, collections, sys
K=0.537
R=np.load('/tmp/pm4h2/plates60.npy')
P={}
for r in R[R[:,1]==1]:
    if abs(r[2]-960)<50 and abs(r[3]-429)<16: P[round(r[0],4)]=(r[2],r[3])
M=R[R[:,1]==0]
byt=collections.defaultdict(list)
for r in M: byt[round(r[0],4)].append((r[2],r[3]))
def counts(t0,t1,RC):
    out=[]
    for t,v in byt.items():
        if not (t0<=t<=t1): continue
        pl=P.get(t)
        if pl is None: continue
        n=sum(1 for (x,y) in v if np.hypot(x-pl[0],(y-pl[1])/K)<=RC)
        out.append(n)
    return np.array(out)
WIN=[('W151-early','wave 151',688.0,698.5),
     ('PM4H-E1','wave 151',689.0,694.0),
     ('PM4H-E2','wave 156',770.0,774.0),
     ('PM4H-E3','wave 158',810.5,813.25),
     ('PM4H-E4','wave 157',779.0,784.0),
     ('PM4H-E5','wave 158-159',813.0,817.0),
     ('PM4H-E6','wave 159-160',838.0,846.0),
     ('wave151','wave 151',688.0,698.5),('wave152','wave 152',699.0,714.7),
     ('wave153','wave 153',715.2,729.5),('wave154','wave 154',730.2,743.8),
     ('wave155','wave 155',744.3,760.0),('wave156','wave 156',760.5,780.2),
     ('wave157','wave 157',780.7,799.5),('wave158','wave 158',800.0,812.5),
     ('wave159','wave 159',813.0,838.8),('wave160','wave 160',839.3,864.0),
     ('WHOLE-FIGHT','151-160',683.0,864.0)]
print('%-13s %-12s %7s %7s  %s'%('window','wave','n_inst','max','  typical(mode/median/p90)  by R_CONTACT 120/150/180'))
rows=[]
for name,wv,t0,t1 in WIN:
    line='%-13s %-12s'%(name,wv)
    rec=dict(window=name,wave=wv,t_start=t0,t_end=t1)
    for RC in [120,150,180]:
        c=counts(t0,t1,RC)
        if len(c)==0: continue
        md=collections.Counter(c).most_common(1)[0][0]
        if RC==150:
            line+=' %7d %7d '%(len(c),c.max())
            rec.update(n_instants=len(c),max_contact=int(c.max()),typical_contact=int(md),
                       median_contact=float(np.median(c)),p90_contact=float(np.percentile(c,90)),
                       mean_contact=round(float(c.mean()),2))
        line+='  R%d:mode=%d med=%.0f p90=%.0f max=%d'%(RC,md,np.median(c),np.percentile(c,90),c.max())
        rec['max_R%d'%RC]=int(c.max()); rec['mode_R%d'%RC]=int(md)
    print(line); rows.append(rec)
import json; json.dump(rows,open('/tmp/pm4h2/d2rows.json','w'),indent=1)
