import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, collections, statistics, csv
from d4_lib import load_trace, FPS
frames=load_trace(); ks=sorted(frames)
fig,ax=plt.subplots(3,1,figsize=(11,9.5))
t0,t1=744.60,747.70
xs=[frames[k][0] for k in ks if t0<=frames[k][0]<=t1]
ys=[frames[k][1] for k in ks if t0<=frames[k][0]<=t1]
ax[0].plot(xs,ys,'-o',ms=2.5,lw=0.8,color='#b03030')
ax[0].set_title('EVIDENCE 1 - DoT tick train, eor-test-2 t=744.82-747.48: 27 ticks at 100 ms cadence,\n'
                'amplitude FLAT at 13-15 HP/tick for 2.667 s. Sawtooth = DoT tick down, regen up.',fontsize=9)
ax[0].set_ylabel('player HP (printed)'); ax[0].grid(alpha=.3)
seq=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        d=frames[ks[i]][1]-frames[ks[i-1]][1]
        if -40<=d<=-1: seq.append((ks[i],-d))
g=collections.Counter()
for a,b in zip(seq,seq[1:]):
    if 1<=b[0]-a[0]<=14: g[b[0]-a[0]]+=1
tot=sum(g.values())
ax[1].bar(list(g),[g[k] for k in g],color='#305090')
ax[1].axvline(6,color='r',ls='--',lw=1.2)
ax[1].set_title(f'EVIDENCE 2 - inter-event gap, DoT-SCALE events only (1-40 HP): sharp mode at 6 frames = 100.0 ms\n'
                f'(26.1% of {tot} gaps; 5 and 7 are the +/-1-frame sampling jitter of a 10 Hz clock at 60 fps)',fontsize=9)
ax[1].set_xlabel('gap (frames @60fps)'); ax[1].set_ylabel('count'); ax[1].grid(alpha=.3)
# panel 3 : before/after-application scatter
BA=[(500,710),(120,115),(115,160),(160,320),(160,140),(140,110),(260,245),(245,400),(400,390),
    (390,360),(360,690),(280,670),(470,590),(590,410),(220,740),(420,690)]
b=[x for x,_ in BA]; a=[y for _,y in BA]
ax[2].scatter(b,a,c=['#c03030' if y>x else '#3060a0' for x,y in BA],s=45,zorder=3)
lim=max(max(b),max(a))*1.08
ax[2].plot([0,lim],[0,lim],'k--',lw=1,label='no change (refresh-only prediction)')
ax[2].plot([0,lim],[0,2*lim],':',color='#888',lw=1,label='2x (one same-magnitude instance added)')
ax[2].set_xlim(0,lim); ax[2].set_ylim(0,lim*1.05)
ax[2].set_xlabel('DoT rate BEFORE application (HP/s)'); ax[2].set_ylabel('DoT rate AFTER (HP/s)')
ax[2].set_title('EVIDENCE 3 - before/after a direct hit (= a DoT application event), n=16.\n'
                '9 up / 7 down. Rises are LARGE (to 3.4x); falls are SMALL. Suggestive of addition,\n'
                'but the applied TYPE is unattributable, so (a) vs (c) vs (b)+new-type cannot be separated.',fontsize=9)
ax[2].legend(fontsize=7.5,loc='upper left'); ax[2].grid(alpha=.3)
plt.tight_layout(); plt.savefig('evidence/d4-tick-structure.png',dpi=110)
print('saved')
