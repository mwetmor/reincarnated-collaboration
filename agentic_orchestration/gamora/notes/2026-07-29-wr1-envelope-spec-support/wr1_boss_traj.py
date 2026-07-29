import json, glob, os, math
BASE="/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/g5_m4cadence_nova_mitR2proxy_tg/traces"
for f in ["boss__A__seed74000802.jsonl","boss__B__seed74000802.jsonl"]:
    p=os.path.join(BASE,f); hdr=None; ticks=[]; tele=[]
    for line in open(p):
        r=json.loads(line); rt=r["record_type"]
        if rt=="header": hdr=r
        elif rt=="tick": ticks.append(r)
        elif rt=="event" and r.get("event")=="telegraph": tele.append(r)
    pid=next(e["entity_id"] for e in hdr["entities"] if e.get("is_player"))
    bid=next(e["entity_id"] for e in hdr["entities"] if e["entity_id"].startswith("boss"))
    print("==",f,"ticks",len(ticks))
    print("  telegraphs:",[(t["shape"],t.get("radius_m"),t["fire_t_s"],round(t["origin_x_m"],2),round(t["origin_y_m"],2)) for t in tele])
    for i in list(range(0,len(ticks),max(1,len(ticks)//12)))+[len(ticks)-1]:
        t=ticks[i]; m={e["entity_id"]:e for e in t["entities"]}
        pe,be=m[pid],m[bid]
        print("  t=%6.1f player(%6.2f,%6.2f) alive=%s | boss(%6.2f,%6.2f) alive=%s | sep=%6.2f"%(
            t["t_s"],pe["x_m"],pe["y_m"],pe["alive"],be["x_m"],be["y_m"],be["alive"],
            math.hypot(pe["x_m"]-be["x_m"],pe["y_m"]-be["y_m"])))
