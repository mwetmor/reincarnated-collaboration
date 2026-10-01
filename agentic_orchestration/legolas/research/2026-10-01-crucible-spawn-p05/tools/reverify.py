import sys, struct, math, collections, csv, json, hashlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import pm4t_map_v2_2026_08_14 as V2
MAPS="/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-citation/maps/"
def parse(b, start_shift):
    table, arr_off = V2.string_table(b)
    n = struct.unpack_from("<I", b, arr_off)[0]
    p = arr_off + 4
    recs=[]
    for i in range(n):
        idx = struct.unpack_from("<I", b, p)[0]
        pos = struct.unpack_from("<3f", b, p+40)
        flag = struct.unpack_from("<I", b, p+52)[0]
        size = 56 if flag==0 else 72
        recs.append(dict(i=i, idx=idx, dbr=table[idx], x=pos[0], y=pos[1], z=pos[2], guid=flag==1))
        p += size
    if start_shift:  # v2-equivalent: label of record i taken from record i+1
        for i in range(len(recs)-1): recs[i]['v2']=recs[i+1]['dbr']
    return recs
out={}
for arc,m in [('sm1','survivalworld_a'),('sm1','survivalworld_b'),('sm1','survivalworld_e'),('sm_mod','survivalworld_a')]:
    b=open(MAPS+f"{arc}/{m}.map","rb").read()
    R=parse(b,True)
    g=[r for r in R if r['guid']]
    lab=collections.Counter(r['dbr'].split('/')[-1] for r in g)
    labv2=collections.Counter(r.get('v2','').split('/')[-1] for r in g)
    pp=[r for r in R if r['guid'] and 'patrolpoint' in r['dbr']]
    cx=sum(r['x'] for r in pp)/len(pp); cz=sum(r['z'] for r in pp)/len(pp)
    print('==',arc,m,'sha256',hashlib.sha256(b).hexdigest()[:16],'records',len(R),'| GUID rows v3-labels:',dict(lab),'| v2-labels:',dict(labv2.most_common(3)))
    print('   patrol centroid (x,z)=(%.3f,%.3f) n=%d'%(cx,cz,len(pp)))
    rows=[]
    for r in R:
        n=r['dbr'].split('/')[-1]
        if n.startswith('spawnpoint0') or n.startswith('spawnbeacon') or n in ('tier16spawnpoint01.dbr','playerspawnpoint.dbr','spawnplayer.dbr') or r.get('v2','').endswith('spawnpoint05.dbr'):
            dx,dy=r['x']-cx,r['z']-cz
            rows.append(dict(arc=arc,map=m,row=r['i'],v3_label=n,v2_label=r.get('v2','').split('/')[-1],x=round(r['x'],3),z=round(r['z'],3),pack_x=round(dx,3),pack_y=round(dy,3),r_m=round(math.hypot(dx,dy),3),bearing_deg_ccw_from_px=round(math.degrees(math.atan2(dy,dx))%360,1)))
    for x in rows: print('  ',x)
    out[f'{arc}/{m}']=rows
json.dump(out,open('reverify_out.json','w'),indent=1)
