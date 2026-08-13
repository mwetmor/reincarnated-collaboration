"""D1 -- world-frame monster tracks with radial/tangential decomposition.

Frames:
  screen -> world :  world_x = screen_x - CUMDX ,  world_y = screen_y - CUMDY
  (CUM* = cumulative camera translation from the 60 fps gradient-registered trace,
   validated against independent NCC terrain matching at 700.00-700.25 (88.4 vs ~93 px)
   and 805.55-805.85 (244.8 vs 236 px)).
  The player is screen-fixed, so its world position is (960 - CUMDX, 544 - CUMDY).

Ground plane: y compressed by K = 0.537 (measured from the player's own circular ground
decal at t=683.500: 80 x 43 px).  All distances below are GROUND PIXELS (x-scale).

Per track, per frame, the monster's own world velocity is decomposed against the
CURRENT player position:
    v_radial      = v . u_hat   where u_hat points from monster to player  (>0 = closing)
    v_tangential  = |v - v_radial * u_hat|                                  (sliding round)
Both are properties of the monster's motion alone -- player movement does not enter,
which is what makes this classification legal on footage where the player is moving
88% of the time.

BLOCKED predicate: another living plate B sits in the corridor between the monster A
and the player -- B closer to the player than A, perpendicular offset from the A->player
segment < CORRIDOR, and B's projection strictly between the two endpoints.
"""
import numpy as np, sys
K=0.537
FPS=60.0
PX_S, PY_S = 960.0, 544.0        # player screen ground point (measured)
PLATE_OFF  = 115.0               # player plate row 429 -> ground 544

def load():
    R=np.load('/tmp/pm4h2/plates60.npy')
    cam=np.load('/tmp/pm4h2/cam60g.npy')       # t,dx,dy,peak  (dx,dy = content shift)
    ct=cam[:,0]
    cx=np.concatenate([[0.0],np.cumsum(cam[:,1])])
    cy=np.concatenate([[0.0],np.cumsum(cam[:,2])])
    ctt=np.concatenate([ct,[ct[-1]+1/FPS]])
    return R,ctt,cx,cy

def world(R,ctt,cx,cy):
    """attach world coords to every plate row. returns dict t -> list of (wx,wy,sx,sy,w)"""
    CX=np.interp(R[:,0],ctt,cx); CY=np.interp(R[:,0],ctt,cy)
    out={}
    for i in range(len(R)):
        if R[i,1]!=0: continue
        t=round(R[i,0],4)
        out.setdefault(t,[]).append((R[i,2]-CX[i], R[i,3]-CY[i], R[i,2], R[i,3], R[i,4]))
    pw={}
    for t in out:
        j=np.searchsorted(ctt,t)
        j=min(max(j,0),len(cx)-1)
        pw[t]=(PX_S-cx[j], PY_S-cy[j])
    return out,pw

def track(W, t0, t1, gate=30.0, maxgap=12):
    ts=sorted([t for t in W if t0-1e-6<=t<=t1+1e-6])
    tracks=[]
    for ti,t in enumerate(ts):
        obs=W[t]; used=set()
        for tr in tracks:
            if ti-tr['li']>maxgap: continue
            lx,ly=tr['p'][-1][1],tr['p'][-1][2]
            best=None;bd=1e9
            for k,o in enumerate(obs):
                if k in used: continue
                d=np.hypot(o[0]-lx,(o[1]-ly)/K)
                g=gate*max(1.0,(ti-tr['li']))**0.6
                if d<bd and d<g: bd=d;best=k
            if best is not None:
                used.add(best);o=obs[best]
                tr['p'].append((t,o[0],o[1],o[2],o[3],o[4]));tr['li']=ti
        for k,o in enumerate(obs):
            if k in used: continue
            tracks.append(dict(p=[(t,o[0],o[1],o[2],o[3],o[4])],li=ti))
    return tracks

def kinematics(tr, pw, W, corridor=70.0, smooth=15):
    p=np.array(tr['p'])
    t=p[:,0]; wx=p[:,1]; wy=p[:,2]/K          # ground-plane world coords
    if len(t)<smooth+2: return None
    ker=np.ones(smooth)/smooth
    sx=np.convolve(wx,ker,mode='valid'); sy=np.convolve(wy,ker,mode='valid')
    st=t[smooth//2:len(t)-smooth//2]
    px=np.array([pw[round(tt,4)][0] for tt in st])
    py=np.array([pw[round(tt,4)][1]/K for tt in st])
    vx=np.gradient(sx,st); vy=np.gradient(sy,st)
    ux=px-sx; uy=py-sy; r=np.hypot(ux,uy)
    ux/=np.maximum(r,1e-6); uy/=np.maximum(r,1e-6)
    vr=vx*ux+vy*uy                              # >0 closing
    vt=np.abs(vx*(-uy)+vy*ux)
    spd=np.hypot(vx,vy)
    # blocked predicate per frame
    blocked=np.zeros(len(st),bool); nblk=np.zeros(len(st),int)
    for i,tt in enumerate(st):
        A=np.array([sx[i],sy[i]]); Pp=np.array([px[i],py[i]])
        d=Pp-A; L=np.hypot(*d)
        if L<1e-6: continue
        dh=d/L; n=0
        for o in W[round(tt,4)]:
            B=np.array([o[0],o[1]/K])
            if np.hypot(*(B-A))<25: continue        # itself
            s=np.dot(B-A,dh)
            if s<=20 or s>=L-20: continue
            perp=abs(np.cross(dh,B-A))
            if perp<corridor: n+=1
        nblk[i]=n; blocked[i]=n>0
    return dict(t=st,r=r,vr=vr,vt=vt,spd=spd,blocked=blocked,nblk=nblk,
                sx=sx,sy=sy,px=px,py=py,scr=p[smooth//2:len(t)-smooth//2,3:6],n=len(p))
