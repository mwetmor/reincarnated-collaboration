import sys,struct,json,collections,statistics
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
ARCS={"base":"resources/Creatures.arc","gdx1":"gdx1/resources/Creatures.arc",
      "gdx2":"gdx2/resources/Creatures.arc","gdx3":"gdx3/resources/Creatures.arc",
      "sm_mod":"mods/survivalmode/resources/Creatures.arc"}
ROOT="/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/"
out={}
h4=collections.Counter(); h12=collections.Counter(); nm=collections.Counter()
for tag,rel in ARCS.items():
    try: a=ArcArchive(ROOT+rel)
    except Exception as e: print("SKIP",tag,e); continue
    anm=[x for x in a.names() if x.lower().endswith(".anm")]
    print(f"{tag:7s} entries={len(a.names()):6d} anm={len(anm):5d}")
    for n in anm:
        try: b=a.read_file(n)
        except Exception: continue
        if b[:3]!=b"ANM": continue
        ver=b[3]
        f4,f8,f12,slen=struct.unpack_from("<IIII",b,4)
        name=b[20:20+slen].decode("latin-1")
        h4[f4]+=1; h12[f12]+=1; nm[name]+=1
        out.setdefault(n.lower(),{"tag":tag,"ver":ver,"f4":f4,"frames":f8,"fps":f12,"ctrl":name,"size":len(b)})
print("\ntotal anm indexed:",len(out))
print("offset4 histogram (top10):",h4.most_common(10))
print("offset12 (fps?) histogram:",h12.most_common(10))
print("ctrl-name histogram (top5):",nm.most_common(5))
json.dump(out,open("anm_index.json","w"))
# regression size ~ frames within a single creature dir (constant skeleton)
byd=collections.defaultdict(list)
for k,v in out.items(): byd[k.rsplit("/",1)[0]].append(v)
good=0;bad=0;slopes=[]
for d,vs in byd.items():
    if len(vs)<4: continue
    xs=[v["frames"] for v in vs]; ys=[v["size"] for v in vs]
    if len(set(xs))<3: continue
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sxx=sum((x-mx)**2 for x in xs); sxy=sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    if sxx==0: continue
    b1=sxy/sxx; b0=my-b1*mx
    ss=sum((y-my)**2 for y in ys); rs=sum((y-(b0+b1*x))**2 for x,y in zip(xs,ys))
    r2=1-rs/ss if ss else 1
    slopes.append((d,len(vs),round(b1,1),round(b0,1),round(r2,4)))
    if r2>0.98: good+=1
    else: bad+=1
print(f"\nper-creature-dir size~frames regressions: {len(slopes)} dirs | r2>0.98: {good} | r2<=0.98: {bad}")
slopes.sort(key=lambda t:t[4])
print("worst 8:",*slopes[:8],sep="\n  ")
print("median r2:",round(statistics.median(s[4] for s in slopes),5))
