import sys,struct,re,json,collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
ROOT="/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/"
ARCS={"base":"resources/Creatures.arc","gdx1":"gdx1/resources/Creatures.arc",
      "gdx2":"gdx2/resources/Creatures.arc","gdx3":"gdx3/resources/Creatures.arc",
      "sm_mod":"mods/survivalmode/resources/Creatures.arc"}
BLOCK=re.compile(rb'([A-Za-z]{4,20})\r?\n\{\r?\n((?:[ \t]*[A-Za-z]+[ \t]*=[ \t]*[^\r\n]*\r?\n)+)\}')
KV=re.compile(rb'[ \t]*([A-Za-z]+)[ \t]*=[ \t]*(?:"([^"]*)"|([^\r\n]*))')
out={}; btype=collections.Counter(); cbname=collections.Counter(); nofile=0
for tag,rel in ARCS.items():
    try: a=ArcArchive(ROOT+rel)
    except Exception: continue
    for n in a.names():
        if not n.lower().endswith(".anm"): continue
        k=n.lower()
        if k in out: continue
        try: b=a.read_file(n)
        except Exception: continue
        if b[:3]!=b"ANM": continue
        f4,fr,fps,slen=struct.unpack_from("<IIII",b,4)
        evs=[]
        for m in BLOCK.finditer(b):
            t=m.group(1).decode("latin-1")
            if t not in ("CallbackPoint","CreateEntity","SoundEvent","Sound","Effect","Trigger"): continue
            d={}
            for kv in KV.finditer(m.group(2)):
                key=kv.group(1).decode("latin-1")
                val=(kv.group(2) or kv.group(3) or b"").decode("latin-1").strip()
                d[key]=val
            btype[t]+=1
            if t=="CallbackPoint" and "name" in d: cbname[d["name"]]+=1
            evs.append({"type":t,**d})
        if not evs: nofile+=1
        out[k]={"tag":tag,"bones":f4,"frames":fr,"fps":fps,"events":evs}
print("anm indexed:",len(out),"| with zero events:",nofile)
print("block types:",btype.most_common())
print("\ncallback name vocabulary (top 45):")
for a_,b_ in cbname.most_common(45): print(f"  {b_:6d}  {a_}")
print("\ndistinct callback names:",len(cbname))
json.dump(out,open("anm_events.json","w"))
