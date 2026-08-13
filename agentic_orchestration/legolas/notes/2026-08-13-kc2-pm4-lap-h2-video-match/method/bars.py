"""Nameplate health-bar detector — the Lap H-2 tracking instrument.

WHY this beats silhouette tracking (Lap H's approach):
  * nameplates are drawn in the UI layer, OVER all world VFX  -> defeats confound C2
  * corpses carry NO nameplate                                -> defeats confound C1
  * the bar is a saturated-red 3px-tall horizontal run, ~72 px wide at full width
  * the accompanying "(cur/max)" text is a per-monster identity token
  * bar screen position = monster screen position + a per-monster constant vertical
    offset (nameplate anchors above the head) -> horizontal displacement is exact,
    vertical displacement is exact up to that constant

CAVEAT (NOTE-9): nameplate presence is a LOWER BOUND on living monsters. Grim Dawn
draws plates for on-screen hostiles, but the exact display rule (radius / cap /
recently-damaged) is not decoded here. Absence of a plate is NOT proof of absence
of a living monster; presence of a plate IS proof of a living monster.
"""
import numpy as np
from PIL import Image

BAR_H = 3          # measured: bars are 3 scanlines tall
MIN_W = 34         # px; reject short red VFX runs
MAX_W = 90

def red_mask(a):
    R,G,B = a[...,0].astype(int), a[...,1].astype(int), a[...,2].astype(int)
    return (R>110)&(R>G*2.2+20)&(R>B*2.2+20)

def green_mask(a):
    R,G,B = a[...,0].astype(int), a[...,1].astype(int), a[...,2].astype(int)
    return (G>110)&(G>R*1.6+20)&(G>B*2.0+20)

def _runs(row, minw, maxw):
    idx = np.nonzero(row)[0]
    if len(idx)==0: return []
    out=[]; s=idx[0]; p=idx[0]
    for x in idx[1:]:
        if x-p<=2: p=x; continue
        if minw<=p-s+1<=maxw: out.append((s,p))
        s=x; p=x
    if minw<=p-s+1<=maxw: out.append((s,p))
    return out

def find_bars(a, mask_fn=red_mask, y0=60, y1=1000, minw=MIN_W, maxw=MAX_W):
    """returns list of dicts: x_left,x_right,x_c,y,w"""
    m = mask_fn(a)
    cand={}
    for y in range(y0,y1):
        for (s,e) in _runs(m[y], minw, maxw):
            cand.setdefault(y,[]).append((s,e))
    # require the run to persist over >=3 consecutive rows with >=70% x-overlap
    bars=[]
    used=set()
    for y in sorted(cand):
        for (s,e) in cand[y]:
            if (y,s,e) in used: continue
            rows=[(y,s,e)]
            yy=y+1
            while yy in cand:
                hit=None
                for (s2,e2) in cand[yy]:
                    ov=min(e,e2)-max(s,s2)
                    if ov > 0.7*min(e-s,e2-s2): hit=(s2,e2); break
                if hit is None: break
                rows.append((yy,hit[0],hit[1])); used.add((yy,hit[0],hit[1])); yy+=1
            if BAR_H<=len(rows)<=6:
                xs=int(np.median([r[1] for r in rows])); xe=int(np.median([r[2] for r in rows]))
                bars.append(dict(x_left=xs,x_right=xe,x_c=(xs+xe)/2.0,
                                 y=rows[0][0]+len(rows)/2.0,w=xe-xs+1,rows=len(rows)))
    # NAMEPLATE-TEXT GATE: a genuine health bar always carries the white "(cur/max)"
    # string immediately above it. Bright red VFX runs do not. MEASURED text band:
    # dy = -31..-21 relative to the bar's top scanline (profiled on frame 783.000,
    # five bars, all five peak in that band and are empty outside it).
    W = (a[...,0]>150)&(a[...,1]>150)&(a[...,2]>145)
    keep=[]
    for b in bars:
        yb=int(b['y']); xc=int(b['x_c'])
        y0t=max(0,yb-34); y1t=max(1,yb-18)
        x0t=max(0,xc-95); x1t=min(a.shape[1],xc+96)
        b['txt']=int(W[y0t:y1t, x0t:x1t].sum())
        if b['txt']>=70: keep.append(b)
    bars=keep
    # dedupe overlapping detections
    bars.sort(key=lambda b:(b['y'],b['x_left']))
    out=[]
    for b in bars:
        if any(abs(b['y']-o['y'])<6 and abs(b['x_c']-o['x_c'])<25 for o in out): continue
        out.append(b)
    return out

if __name__=='__main__':
    import sys
    a=np.array(Image.open(sys.argv[1]))
    for b in find_bars(a):
        print(f"x[{b['x_left']:4d},{b['x_right']:4d}] xc={b['x_c']:7.1f} y={b['y']:6.1f} w={b['w']:3d} rows={b['rows']}")


# ---- player plate ------------------------------------------------------------
# MEASURED (frame 700.000, native): the player's own nameplate bar is GREEN
# rows 428-431 at RGB ~ (120,240,35) with the white "(20,005/20,005)" string at
# rows 402-409 -- i.e. same geometry as a monster plate but green instead of red.
# Monster plates are red; therefore green == player, unambiguously.
def green_mask2(a):
    R,G,B = a[...,0].astype(int), a[...,1].astype(int), a[...,2].astype(int)
    return (G>90)&(G>R*1.25+15)&(G>B*1.8+15)

def find_player_bar(a):
    m = green_mask2(a)
    best=None
    for y in range(200,900):
        for (s,e) in _runs(m[y], 22, 90):
            # need >=2 consecutive rows
            ok=False
            for (s2,e2) in _runs(m[y+1], 18, 92):
                if min(e,e2)-max(s,s2) > 0.6*min(e-s,e2-s2): ok=True; break
            if not ok: continue
            W=(a[...,0]>150)&(a[...,1]>150)&(a[...,2]>145)
            xc=(s+e)//2
            txt=int(W[max(0,y-34):y-18, max(0,xc-95):xc+96].sum())
            if txt<70: continue
            cand=dict(x_left=s,x_right=e,x_c=(s+e)/2.0,y=y+1.0,w=e-s+1,txt=txt)
            if best is None or cand['w']>best['w']: best=cand
    return best
