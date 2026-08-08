#!/usr/bin/env python3
"""D10 — the +121 % term: level-indexed passive characterLifeModifier. READ-ONLY."""
import sys; sys.path.insert(0,".")
import lib2
E2=lib2.E2
def ev(e,L): return eval(str(e).replace("^","**").replace("charLevel",f"({L})"),{"__builtins__":{}},{})

print("=== armorbase0N characterLifeModifier around rank index 100..112 ===")
for n in range(1,8):
    p=f"records/skills/nonplayerskills/passive/armorbase0{n}.dbr"
    r,ow=E2.merged(p)
    if not r: continue
    v=r.get("characterLifeModifier")
    if isinstance(v,list):
        print(f"  armorbase0{n}  own={ow}  len={len(v)}  idx100..112 = {v[100:113]}")
    else:
        print(f"  armorbase0{n}  own={ow}  lifeMod={v}")

print("\n=== which passive each anchor carries, and at what skill level ===")
ANCH=["records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr",
      "records/creatures/enemies/devotion/aetherialphantom_h01.dbr",
      "records/creatures/enemies/aetherialcorruption_c01_summon.dbr",
      "records/creatures/enemies/hero/basilisk_h02.dbr",
      "records/creatures/enemies/hero/swampcrab_h03.dbr",
      "records/creatures/enemies/swampcrab_a00_summon.dbr",
      "records/creatures/enemies/livingplant_a01.dbr",
      "records/creatures/enemies/hero/chthonianfiend_h05.dbr"]
for p in ANCH:
    r,_=E2.merged(p)
    print(f"\n  {p}")
    for i in range(1,30):
        sn=r.get(f"skillName{i}"); sl=r.get(f"skillLevel{i}")
        if not sn: continue
        s,_=E2.merged(sn)
        if not s: continue
        lm=s.get("characterLifeModifier")
        if lm is None: continue
        if isinstance(lm,list):
            for L in (107,108):
                idx=int(ev(sl,L))-1 if sl else 0
                val = lm[idx] if 0<=idx<len(lm) else None
                print(f"      skill{i:<2} {sn.split('/')[-1]:32s} lvl({L})={ev(sl,L):7.3f} -> idx {idx:3d} lifeMod {val}")
        elif lm:
            print(f"      skill{i:<2} {sn.split('/')[-1]:32s} lifeMod(scalar) {lm}")
