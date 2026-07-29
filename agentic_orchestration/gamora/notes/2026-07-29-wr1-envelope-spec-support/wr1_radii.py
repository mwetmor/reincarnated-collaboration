import json, glob, os
BASE="/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2"
LEGS=["g5_m4cadence_nova_mitR2proxy_tg","g5_m4cadence_nova_mitR2proxyresistslow_tg","g5_r3arm_m4cadence_nova_mitR3_tg"]
from collections import defaultdict
d=defaultdict(set); rng=defaultdict(set); sk=defaultdict(set)
for L in LEGS:
    for p in glob.glob(os.path.join(BASE,L,"traces","*.jsonl")):
        tier=os.path.basename(p).split("__")[0]
        h=json.loads(open(p).readline())
        for e in h["entities"]:
            d[tier].add((e["entity_id"].rsplit("_",1)[0], e.get("entity_radius_m")))
            for s in e.get("skills",[]): sk[tier].add((s["geometry"], s["range_m"]))
for t in ["trash","champion","mixed_pack","boss"]:
    print("==",t)
    for eid,r in sorted(d[t]): print("   %-38s radius %.2f"%(eid,r))
    print("   R_max=%.2f  skill geometries/ranges: %s"%(max(r for _,r in d[t]), sorted(sk[t])))
