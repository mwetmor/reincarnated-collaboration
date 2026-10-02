import sys, math
sys.path.insert(0, sys.argv[1])
import rj_arms as R
LOG=[]
orig=R.RJFold.is_opportunity
def iso(self, eng, aid, prof, tick):
    X=self._x(aid) if self.any else None
    before=(X["m"] if X else None, eng._ge_state.get(aid,{}).get("mode"))
    r=orig(self, eng, aid, prof, tick)
    X=self._x(aid)
    after=(X["m"], eng._ge_state.get(aid,{}).get("mode"))
    if before!=after and len(LOG)<4000:
        me=self._pos(aid); p=R.REG.player_xy
        d=math.hypot(me[0]-p[0],me[1]-p[1]) if me and p else -1
        S=eng._ge_state[aid]["S"]
        LOG.append((tick,aid,before,after,round(d,2), round(S.reach_m,2) if S else None, X["kind"], R.REC.get(self._rec(aid),{}).get("randomRepositionChance")))
    return r
R.RJFold.is_opportunity=iso
res=R.run_arm(sys.argv[2],(0,))
import collections
c=collections.Counter((b,a) for _,_,b,a,*_ in LOG)
for k,v in c.most_common(30): print(v,k)
# RFA episodes for 3 actors
seen=0
ids=[l[1] for l in LOG if l[3][0]=='R']
for aid in list(dict.fromkeys(ids))[:4]:
    print('---',aid)
    for l in LOG:
        if l[1]==aid: print(l)
