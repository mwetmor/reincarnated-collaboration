#!/usr/bin/env python3
"""probe10 (WR1 E-2/E-3) — closing probes.
(a) timeBetweenAttacks: which skill Classes carry it, all 4 archives
(b) characterBaseAttackSpeedTag ladder: value census on weapons + which classes use which
(c) defensiveAbsorption / defensiveProtection field carriers (E-2 mitigation inputs)
(d) player armour item defensiveProtection sample + the pak for players. Read-only."""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
archives=[(p.name,ArzArchive(p)) for p in ARZS]

print("### (a) timeBetweenAttacks by skill Class (all archives)")
c=collections.Counter(); ex={}; vals=collections.defaultdict(set)
for name,a in archives:
    for rp in a.records:
        if not rp.startswith('records/skills/'): continue
        rec=a.read_record(rp)
        tb=rec.get('timeBetweenAttacks')
        if tb is None: continue
        cl=rec.get('Class') or a.record_type(rp)
        c[cl]+=1; ex.setdefault(cl,f"[{name}] {rp}")
        vals[cl].add(tb if not isinstance(tb,list) else tuple(tb))
for cl,n in c.most_common():
    v=sorted(vals[cl], key=str)
    print(f"  {cl:32s} n={n:4d} values={v[:8]}")
    print(f"      e.g. {ex[cl]}")

print("\n### (b) characterBaseAttackSpeedTag census on weapons")
tagc=collections.Counter(); tagex={}
for name,a in archives:
    for rp in a.records:
        rt=a.record_type(rp)
        if not rt.startswith('Weapon'): continue
        rec=a.read_record(rp)
        t=rec.get('characterBaseAttackSpeedTag')
        if t is None: continue
        tagc[(rt,t)]+=1; tagex.setdefault((rt,t),rp)
for (rt,t),n in sorted(tagc.items(), key=lambda x:(x[0][0],x[0][1])):
    print(f"  {rt:26s} {t:34s} n={n:5d}  e.g. {tagex[(rt,t)]}")

print("\n### (c) defensiveAbsorption carriers (non-zero), sample of 25")
seen=0
for name,a in archives:
    for rp in a.records:
        rec=a.read_record(rp)
        v=rec.get('defensiveAbsorption')
        if v in (None,0,0.0): continue
        if isinstance(v,list) and not any(v): continue
        print(f"  [{name}] {rp:74s} defensiveAbsorption={v if not isinstance(v,list) else v[:5]}")
        seen+=1
        if seen>=25: break
    if seen>=25: break

print("\n### (d) player pak (balancingadjustment_mp+difficulty_players01)")
T="records/game/balancingadjustment_mp+difficulty_players01.dbr"
for name,a in archives:
    if T in a.records:
        rec=a.read_record(T)
        print(f"  [{name}] {T}")
        for k in sorted(rec):
            v=rec[k]
            if isinstance(v,list) and not any(x for x in v if isinstance(x,(int,float)) and x): continue
            if isinstance(v,(int,float)) and v==0: continue
            print(f"    {k:44s} {v!r}")
        break

print("\n### (e) sample player armour: defensiveProtection + slot")
for t in ["records/items/gearchest/c001_chest.dbr","records/items/gearhead/c001_head.dbr"]:
    for name,a in archives:
        if t in a.records:
            rec=a.read_record(t)
            print(f"  [{name}] {t} class={rec.get('Class')} itemSkillLevel? ")
            for k in sorted(rec):
                if re.search(r'defensiveProtection|defensiveAbsorption|itemClassification|levelRequirement|Class$', k):
                    print(f"    {k:40s} {rec[k]!r}")
            break
