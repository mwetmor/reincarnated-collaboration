#!/usr/bin/env python3
"""Fold .anm CallbackPoint/CreateEntity events into the threat-grammar tables. READ-ONLY."""
import json,csv
EV=json.load(open("anm_events.json"))
FPS=30.0
def key(ref):
    r=(ref or "").lower().replace("\\","/")
    return r[len("creatures/"):] if r.startswith("creatures/") else r

def grammar(anmref):
    """-> dict of event-derived timing for one clip, or None."""
    e=EV.get(key(anmref))
    if not e: return None
    fr=e["frames"]; evs=e["events"]
    def fnum(x):
        try: return int(x)
        except: return None
    hits=sorted(f for f in (fnum(v.get("frame")) for v in evs
                if v["type"]=="CallbackPoint" and v.get("name","").endswith(("Hit",))) if f is not None)
    ai=sorted(f for f in (fnum(v.get("frame")) for v in evs
                if v["type"]=="CallbackPoint" and v.get("name")=="AllowInterrupt") if f is not None)
    swon=sorted(f for f in (fnum(v.get("frame")) for v in evs
                if v["type"]=="CallbackPoint" and v.get("name","").startswith("Swipe") and not v.get("name","").endswith("Off")) if f is not None)
    swoff=sorted(f for f in (fnum(v.get("frame")) for v in evs
                if v["type"]=="CallbackPoint" and v.get("name","").endswith("Off")) if f is not None)
    ps_s=sorted(f for f in (fnum(v.get("frame")) for v in evs
                if v["type"]=="CallbackPoint" and v.get("name","").endswith("Start") and v.get("name","").startswith("PS")) if f is not None)
    ps_e=sorted(f for f in (fnum(v.get("frame")) for v in evs
                if v["type"]=="CallbackPoint" and v.get("name","").endswith("End") and v.get("name","").startswith("PS")) if f is not None)
    fx=sorted((fnum(v.get("frame")), v.get("entity","")) for v in evs if v["type"]=="CreateEntity" and fnum(v.get("frame")) is not None)
    d=dict(anm_frames=fr, anm_dur_s=round(fr/FPS,4),
        hit_frames="|".join(str(x) for x in hits), n_hits=len(hits),
        windup_s=round(hits[0]/FPS,4) if hits else "",
        windup_frac=round(hits[0]/fr,4) if hits and fr else "",
        recovery_s=round((fr-hits[-1])/FPS,4) if hits else "",
        intra_clip_hit_gap_s=round((hits[-1]-hits[0])/(len(hits)-1)/FPS,4) if len(hits)>1 else "",
        allow_interrupt_frame=ai[0] if ai else "",
        root_lock_s=round((ai[0] if ai else fr)/FPS,4),
        root_lock_frac=round((ai[0] if ai else fr)/fr,4) if fr else "",
        root_lock_grade="MEASURED-ALLOWINTERRUPT" if ai else "MEASURED-NO-INTERRUPT-POINT(full-clip lock)",
        swipe_on_frames="|".join(str(x) for x in swon),
        swipe_off_frames="|".join(str(x) for x in swoff),
        active_window_s=round((swoff[-1]-swon[0])/FPS,4) if swon and swoff else "",
        ps_window_s=round((ps_e[-1]-ps_s[0])/FPS,4) if ps_s and ps_e else "",
        fx_first_frame=fx[0][0] if fx else "",
        fx_first_onset_s=round(fx[0][0]/FPS,4) if fx else "",
        fx_entities="|".join(sorted({f[1].rsplit("\\",1)[-1] for f in fx})),
        n_events=len(evs))
    return d

EVCOLS=list(grammar("creatures/enemies/slith/anm/slith01_attack_01.anm").keys())

# --- monster table: basic attack clip 1 (the primary swing)
M=list(csv.DictReader(open("tg_monster_timing.csv")))
nm=0
for r in M:
    a=(r.get("basic_attack_anims") or "").split("|")[0]
    g=None
    if a:
        # need full path: recover from anim table
        g=None
    r["_a"]=a
# resolve full paths via the anim tables again
from tg_lib import E3
full={}
for r in M:
    t=r.get("anim_table")
    if not t: continue
    tr,_=E3.merged(t)
    if not tr: continue
    a=tr.get("unarmedAttackAnim1")
    if isinstance(a,str): full[r["record"]]=a
for r in M:
    g=grammar(full.get(r["record"],"")) if r["record"] in full else None
    for c in EVCOLS: r["basic_"+c]= (g or {}).get(c,"")
    r.pop("_a",None)
    if g: nm+=1
ks=[]
for r in M:
    for k in r:
        if k not in ks: ks.append(k)
with open("tg_monster_timing.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=ks); w.writeheader(); [w.writerow({k:r.get(k,"") for k in ks}) for r in M]
print("tg_monster_timing.csv:",len(M),"rows,",len(ks),"cols | basic-clip grammar resolved:",nm)

# --- slot table
S=list(csv.DictReader(open("tg_attack_slots.csv")))
# need full anm path per slot -> re-resolve from special_anm basename against EV index
base={}
for k in EV: base.setdefault(k.rsplit("/",1)[-1],[]).append(k)
ns=0
for r in S:
    b=r.get("special_anm") or ""
    g=None
    if b and b.lower() in base:
        cands=base[b.lower()]
        g=grammar(cands[0]) if len(cands)>=1 else None
    for c in EVCOLS: r[c]=(g or {}).get(c,"")
    if g: ns+=1
ks=[]
for r in S:
    for k in r:
        if k not in ks: ks.append(k)
with open("tg_attack_slots.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=ks); w.writeheader(); [w.writerow({k:r.get(k,"") for k in ks}) for r in S]
print("tg_attack_slots.csv:",len(S),"rows,",len(ks),"cols | slot-clip grammar resolved:",ns)
