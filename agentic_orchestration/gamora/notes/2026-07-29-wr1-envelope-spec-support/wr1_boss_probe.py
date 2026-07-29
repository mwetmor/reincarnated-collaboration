import json, glob, os, math
from collections import defaultdict
BASE="/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2"
LEGS={"pre":"g5_m4cadence_nova_mitR2proxy_tg","pre_endpoint":"g5_m4cadence_nova_mitR2proxyresistslow_tg","post":"g5_r3arm_m4cadence_nova_mitR3_tg"}
def pctl(v,q):
    v=sorted(v); return v[max(1,math.ceil(q*len(v)))-1] if v else None
per_fight=[]; allsep=[]; corner=0; fights=0
nova_positions=[]
for leg,d in LEGS.items():
    for p in sorted(glob.glob(os.path.join(BASE,d,"traces","boss__*.jsonl"))):
        arm=os.path.basename(p).split("__")[1]
        hdr=None; ticks=[]; tele=[]
        for line in open(p):
            r=json.loads(line)
            rt=r["record_type"]
            if rt=="header": hdr=r
            elif rt=="tick": ticks.append(r)
            elif rt=="event" and r.get("event")=="telegraph": tele.append(r)
        pid=next(e["entity_id"] for e in hdr["entities"] if e.get("is_player"))
        bid=next(e["entity_id"] for e in hdr["entities"] if e["entity_id"].startswith("boss"))
        aw=hdr["frame"]["arena_width_m"]; ah=hdr["frame"]["arena_height_m"]
        rad={e["entity_id"]:(e.get("entity_radius_m") or 0.) for e in hdr["entities"]}
        seps=[]; cticks=0; pt=0
        for t in ticks:
            m={e["entity_id"]:e for e in t["entities"]}
            pe=m.get(pid); be=m.get(bid)
            if pe and pe.get("alive"):
                pt+=1; rr=rad[pid]
                if abs(pe["x_m"]-rr)<1e-6 and abs(pe["y_m"]-rr)<1e-6: cticks+=1
            if pe and be and pe.get("alive") and be.get("alive"):
                seps.append(math.hypot(pe["x_m"]-be["x_m"], pe["y_m"]-be["y_m"]))
        if seps:
            allsep+=seps
            per_fight.append(dict(leg=leg,arm=arm,med=pctl(seps,.5),p95=pctl(seps,.95),mx=max(seps),mn=min(seps),
                                  corner_frac=cticks/max(1,pt)))
        fights+=1
        for tg in tele:
            if tg.get("radius_m"):
                nova_positions.append((tg["origin_x_m"],tg["origin_y_m"],tg["radius_m"]))
print("boss fights:",fights)
print("player<->BOSS separation, pooled over all entity-ticks (n=%d):"%len(allsep))
for q in (0.05,0.25,0.5,0.75,0.95,0.99): print("   p%.0f = %.3f"%(q*100,pctl(allsep,q)))
print("   min %.3f  max %.3f  mean %.3f"%(min(allsep),max(allsep),sum(allsep)/len(allsep)))
print("per-fight median of player<->boss sep: med=%.3f max=%.3f"%(pctl([r['med'] for r in per_fight],.5),max(r['med'] for r in per_fight)))
print("per-fight max     of player<->boss sep: med=%.3f max=%.3f"%(pctl([r['mx'] for r in per_fight],.5),max(r['mx'] for r in per_fight)))
cf=[r['corner_frac'] for r in per_fight]
print("fraction of player ticks in SW CORNER (both x=r and y=r): med=%.3f max=%.3f  fights>0: %d/%d"%(pctl(cf,.5),max(cf),sum(1 for x in cf if x>0),len(cf)))
print("nova telegraph origins: n=%d  radius set=%s"%(len(nova_positions),sorted({round(r,3) for _,_,r in nova_positions})))
xs=[x for x,_,_ in nova_positions]; ys=[y for _,y,_ in nova_positions]
print("  origin x range %.3f..%.3f  y range %.3f..%.3f"%(min(xs),max(xs),min(ys),max(ys)))
print("  nova FOOTPRINT extent (origin +/- 12m): x %.3f..%.3f  y %.3f..%.3f"%(min(xs)-12,max(xs)+12,min(ys)-12,max(ys)+12))
