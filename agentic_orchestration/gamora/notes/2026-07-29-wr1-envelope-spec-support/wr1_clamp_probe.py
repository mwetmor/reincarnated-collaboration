import json, glob, os, math
from collections import defaultdict
BASE="/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2"
LEGS={"pre":"g5_m4cadence_nova_mitR2proxy_tg","pre_endpoint":"g5_m4cadence_nova_mitR2proxyresistslow_tg","post":"g5_r3arm_m4cadence_nova_mitR3_tg"}
EPS=1e-6
agg=defaultdict(lambda: dict(fights=0, fights_pl_clamp=0, fights_any_clamp=0,
                             pl_ticks=0, pl_clamp_ticks=0, mob_ticks=0, mob_clamp_ticks=0,
                             sides=defaultdict(int)))
for leg,d in LEGS.items():
    for p in sorted(glob.glob(os.path.join(BASE,d,"traces","*.jsonl"))):
        tier=os.path.basename(p).split("__")[0]
        hdr=None; ticks=[]
        for line in open(p):
            r=json.loads(line)
            if r["record_type"]=="header": hdr=r
            elif r["record_type"]=="tick": ticks.append(r)
        aw=hdr["frame"]["arena_width_m"]; ah=hdr["frame"]["arena_height_m"]
        rad={e["entity_id"]:(e.get("entity_radius_m") or 0.) for e in hdr["entities"]}
        pid=next(e["entity_id"] for e in hdr["entities"] if e.get("is_player"))
        a=agg[tier]; a["fights"]+=1
        plc=False; anyc=False
        for t in ticks:
            for e in t["entities"]:
                if not e.get("alive"): continue
                rr=rad[e["entity_id"]]; x,y=e["x_m"],e["y_m"]
                hit=[]
                if abs(x-rr)<EPS: hit.append("W")
                if abs(x-(aw-rr))<EPS: hit.append("E")
                if abs(y-rr)<EPS: hit.append("S")
                if abs(y-(ah-rr))<EPS: hit.append("N")
                isp = e["entity_id"]==pid
                if isp: a["pl_ticks"]+=1
                else: a["mob_ticks"]+=1
                if hit:
                    anyc=True
                    for h in hit: a["sides"][("player" if isp else "mob")+"-"+h]+=1
                    if isp: a["pl_clamp_ticks"]+=1; plc=True
                    else: a["mob_clamp_ticks"]+=1
        if plc: a["fights_pl_clamp"]+=1
        if anyc: a["fights_any_clamp"]+=1
for tier in ["trash","champion","mixed_pack","boss"]:
    a=agg[tier]
    print(f"== {tier}: fights={a['fights']} fights_with_player_at_bound={a['fights_pl_clamp']} fights_any_entity_at_bound={a['fights_any_clamp']}")
    print(f"   player ticks at bound: {a['pl_clamp_ticks']}/{a['pl_ticks']} = {100*a['pl_clamp_ticks']/max(1,a['pl_ticks']):.2f}%")
    print(f"   mob    ticks at bound: {a['mob_clamp_ticks']}/{a['mob_ticks']} = {100*a['mob_clamp_ticks']/max(1,a['mob_ticks']):.2f}%")
    print("   sides:", dict(a["sides"]))
