import json, glob, os, math
BASE="/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2"
LEGS={"pre":"g5_m4cadence_nova_mitR2proxy_tg","pre_endpoint":"g5_m4cadence_nova_mitR2proxyresistslow_tg","post":"g5_r3arm_m4cadence_nova_mitR3_tg"}
def pctl(v,q):
    v=sorted(v); return v[max(1,math.ceil(q*len(v)))-1] if v else float('nan')
rows=[]
for leg,d in LEGS.items():
    for p in sorted(glob.glob(os.path.join(BASE,d,"traces","*.jsonl"))):
        tier=os.path.basename(p).split("__")[0]
        hdr=None; ticks=[]; ftr=None
        for line in open(p):
            r=json.loads(line); rt=r["record_type"]
            if rt=="header": hdr=r
            elif rt=="tick": ticks.append(r)
            elif rt=="footer": ftr=r
        pid=next(e["entity_id"] for e in hdr["entities"] if e.get("is_player"))
        rr=next((e.get("entity_radius_m") or 0.) for e in hdr["entities"] if e["entity_id"]==pid)
        aw=hdr["frame"]["arena_width_m"]; ah=hdr["frame"]["arena_height_m"]
        pts=[]
        for t in ticks:
            m={e["entity_id"]:e for e in t["entities"]}
            e=m.get(pid)
            if e and e["alive"]: pts.append((t["t_s"],e["x_m"],e["y_m"]))
        if len(pts)<3: continue
        dur=ftr["elapsed_s"]
        def pinned(x,y):
            return abs(x-rr)<1e-6 or abs(x-(aw-rr))<1e-6 or abs(y-rr)<1e-6 or abs(y-(ah-rr))<1e-6
        t_pin=None
        for (t,x,y) in pts:
            if pinned(x,y): t_pin=t; break
        pinned_s = (pts[-1][0]-t_pin) if t_pin is not None else 0.0
        # free-phase net drift: from the position of peak-approach (max dist travelled toward mobs)
        # use t=1.5s..t_pin window if available, else whole free phase
        free=[q for q in pts if t_pin is None or q[0]<=t_pin]
        drift=0.0
        if len(free)>=3 and free[-1][0]-free[0][0]>0.3:
            # net drift measured on the second half of the free phase (post-contact)
            h=free[len(free)//2:]
            dt=h[-1][0]-h[0][0]
            if dt>0: drift=math.hypot(h[-1][1]-h[0][1],h[-1][2]-h[0][2])/dt
        obs_diag=math.hypot(max(q[1] for q in pts)-min(q[1] for q in pts),
                            max(q[2] for q in pts)-min(q[2] for q in pts))
        rows.append(dict(tier=tier,leg=leg,dur=dur,t_pin=t_pin,pinned_s=pinned_s,
                         pinned_frac=pinned_s/dur if dur else 0,drift=drift,
                         obs_diag=obs_diag, extra=drift*pinned_s))
for tier in ["trash","champion","mixed_pack","boss"]:
    rs=[r for r in rows if r["tier"]==tier]
    npin=sum(1 for r in rs if r["t_pin"] is not None)
    print("== %s  n=%d  fights_where_player_hits_a_wall=%d (%.0f%%)"%(tier,len(rs),npin,100*npin/len(rs)))
    print("   duration s        : med %.1f  p95 %.1f  max %.1f  min %.1f"%(pctl([r['dur'] for r in rs],.5),pctl([r['dur'] for r in rs],.95),max(r['dur'] for r in rs),min(r['dur'] for r in rs)))
    if npin:
        pr=[r for r in rs if r["t_pin"] is not None]
        print("   t_first_wall_touch: med %.1f s   pinned_seconds med %.1f  pinned_fraction med %.2f"%(
            pctl([r['t_pin'] for r in pr],.5),pctl([r['pinned_s'] for r in pr],.5),pctl([r['pinned_frac'] for r in pr],.5)))
        print("   post-contact net drift m/s: med %.3f"%pctl([r['drift'] for r in pr],.5))
        print("   observed diag med %.2f -> UNBOUNDED-EXTRAPOLATED diag med %.2f  p95 %.2f  max %.2f"%(
            pctl([r['obs_diag'] for r in rs],.5),
            pctl([r['obs_diag']+r['extra'] for r in rs],.5),
            pctl([r['obs_diag']+r['extra'] for r in rs],.95),
            max(r['obs_diag']+r['extra'] for r in rs)))
