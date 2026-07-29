import json, os, math
BASE="/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/g5_m4cadence_nova_mitR2proxy_tg/traces"
p=os.path.join(BASE,"boss__B__seed74000802.jsonl")
hdr=None; ticks=[]
for line in open(p):
    r=json.loads(line); rt=r["record_type"]
    if rt=="header": hdr=r
    elif rt=="tick": ticks.append(r)
pid=next(e["entity_id"] for e in hdr["entities"] if e.get("is_player"))
pts=[]
for t in ticks:
    m={e["entity_id"]:e for e in t["entities"]}
    if m[pid]["alive"]: pts.append((t["t_s"],m[pid]["x_m"],m[pid]["y_m"]))
print("first 40 player positions (0.1s ticks):")
for i in range(0,40): print("  %5.1f (%7.3f,%7.3f)"%pts[i])
# speeds
sp=[math.hypot(pts[i+1][1]-pts[i][1],pts[i+1][2]-pts[i][2])/(pts[i+1][0]-pts[i][0]) for i in range(len(pts)-1)]
moving=[s for s in sp if s>1e-6]
print("player speed: n_moving_ticks=%d/%d  max=%.4f  median_moving=%.4f"%(len(moving),len(sp),max(sp),sorted(moving)[len(moving)//2]))
# path length and net displacement
plen=sum(math.hypot(pts[i+1][1]-pts[i][1],pts[i+1][2]-pts[i][2]) for i in range(len(pts)-1))
print("path length=%.2f m  net displacement=%.2f m  duration=%.1f s"%(plen,math.hypot(pts[-1][1]-pts[0][1],pts[-1][2]-pts[0][2]),pts[-1][0]))
# when does it first reach corner
for i,(t,x,y) in enumerate(pts):
    if abs(x-0.5)<1e-6 and abs(y-0.5)<1e-6:
        print("first corner-pin at t=%.1f s (%.1f%% into the fight); pinned for %.1f s"%(t,100*t/pts[-1][0],pts[-1][0]-t)); break
